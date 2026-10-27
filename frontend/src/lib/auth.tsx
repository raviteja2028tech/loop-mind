import * as React from "react";
import { Navigate } from "react-router-dom";
import { ApiError, type AccountRole, getAuthToken, getMe, setAuthToken } from "@/lib/api";

interface AuthState {
  role: AccountRole | null;
  mobileNumber: string | null;
  loading: boolean;
}

interface AuthContextValue extends AuthState {
  login: (token: string, role: AccountRole, mobileNumber: string) => void;
  logout: () => void;
}

const AuthContext = React.createContext<AuthContextValue | null>(null);

/**
 * phase.md Phase 03 "role identification; authorization": tracks the
 * authenticated account's role client-side so routes can enforce that a
 * student never reaches Recruiter Portal functionality and vice versa.
 * Server-side authorization (backend.auth.dependencies.require_role)
 * remains the actual security boundary — this only drives navigation/UI.
 */
export function AuthProvider({ children }: { children: React.ReactNode }) {
  const [state, setState] = React.useState<AuthState>(() => ({
    role: null,
    mobileNumber: null,
    // Only stay in "loading" if there's a stored token to validate;
    // otherwise there's nothing to wait for.
    loading: getAuthToken() !== null,
  }));

  React.useEffect(() => {
    const token = getAuthToken();
    if (!token) return;

    let cancelled = false;
    const restore = (retriesLeft: number) => {
      getMe()
        .then((me) => {
          if (!cancelled) {
            setState({ role: me.role, mobileNumber: me.mobile_number, loading: false });
          }
        })
        .catch((err) => {
          if (cancelled) return;
          // Email Invitation & Session Persistence Fix Specification §4-5:
          // only an actual invalid/expired session (the server explicitly
          // rejecting the token) should log the user out. A transient
          // failure to even reach the backend (e.g. a dev-server restart
          // mid-refresh) must never destroy a still-valid stored token —
          // otherwise a momentary network hiccup on refresh would
          // permanently sign the user out, which is exactly the bug this
          // restoration logic exists to prevent. Such failures get one
          // short retry before giving up for this load; the token itself
          // is left intact either way, so the next real refresh can still
          // restore the session once the backend is reachable again.
          const isRejectedByServer = err instanceof ApiError && err.status === 401;
          if (isRejectedByServer) {
            setAuthToken(null);
            setState({ role: null, mobileNumber: null, loading: false });
            return;
          }
          if (retriesLeft > 0) {
            setTimeout(() => {
              if (!cancelled) restore(retriesLeft - 1);
            }, 800);
            return;
          }
          setState({ role: null, mobileNumber: null, loading: false });
        });
    };
    restore(1);

    return () => {
      cancelled = true;
    };
  }, []);

  const value = React.useMemo<AuthContextValue>(
    () => ({
      ...state,
      login: (token, role, mobileNumber) => {
        setAuthToken(token);
        setState({ role, mobileNumber, loading: false });
      },
      logout: () => {
        setAuthToken(null);
        setState({ role: null, mobileNumber: null, loading: false });
      },
    }),
    [state],
  );

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
}

export function useAuth() {
  const ctx = React.useContext(AuthContext);
  if (!ctx) throw new Error("useAuth must be used within AuthProvider");
  return ctx;
}

/** Redirects away if the authenticated account's role doesn't match. */
export function RequireRole({
  role,
  children,
}: {
  role: AccountRole;
  children: React.ReactElement;
}) {
  const auth = useAuth();
  if (auth.loading) return null;
  if (auth.role !== role) return <Navigate to="/" replace />;
  return children;
}
