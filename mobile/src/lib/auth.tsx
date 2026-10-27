import * as React from "react";
import { getAuthToken, getMe, setAuthToken, type Role } from "@/lib/api";

interface AuthState {
  token: string | null;
  role: Role | null;
  loading: boolean;
  login: (token: string, role: Role) => Promise<void>;
  logout: () => Promise<void>;
}

const AuthContext = React.createContext<AuthState | null>(null);

/** Mirrors frontend/src/lib/auth.tsx's contract (token + role, persisted,
 * login/logout) — same backend-issued JWT, just stored via AsyncStorage
 * instead of localStorage (phase.md Phase 19: same auth, same backend). */
export function AuthProvider({ children }: { children: React.ReactNode }) {
  const [token, setToken] = React.useState<string | null>(null);
  const [role, setRole] = React.useState<Role | null>(null);
  const [loading, setLoading] = React.useState(true);

  React.useEffect(() => {
    getAuthToken().then(async (stored) => {
      if (!stored) {
        setLoading(false);
        return;
      }
      try {
        const me = await getMe();
        setToken(stored);
        setRole(me.role);
      } catch {
        await setAuthToken(null);
      } finally {
        setLoading(false);
      }
    });
  }, []);

  const login = React.useCallback(async (newToken: string, newRole: Role) => {
    await setAuthToken(newToken);
    setToken(newToken);
    setRole(newRole);
  }, []);

  const logout = React.useCallback(async () => {
    await setAuthToken(null);
    setToken(null);
    setRole(null);
  }, []);

  return (
    <AuthContext.Provider value={{ token, role, loading, login, logout }}>
      {children}
    </AuthContext.Provider>
  );
}

export function useAuth(): AuthState {
  const ctx = React.useContext(AuthContext);
  if (!ctx) throw new Error("useAuth must be used within AuthProvider");
  return ctx;
}
