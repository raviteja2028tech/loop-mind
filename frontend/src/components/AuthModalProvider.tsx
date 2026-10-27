import * as React from "react";
import { useNavigate } from "react-router-dom";
import { Button } from "@/components/Button";
import { Input } from "@/components/Input";
import { Modal } from "@/components/Modal";
import { OtpInput } from "@/components/OtpInput";
import { type AuthPurpose, ApiError, sendOtp, verifyOtp } from "@/lib/api";
import { useAuth } from "@/lib/auth";
import { useOnboardingModal } from "@/website/onboarding/OnboardingModalProvider";

type Step = "mobile" | "otp";
type MobileIssue = "not_found" | "already_exists" | null;

interface AuthModalContextValue {
  openLogin: () => void;
  openRegister: () => void;
}

const AuthModalContext = React.createContext<AuthModalContextValue | null>(null);

const RESEND_COOLDOWN_SECONDS = 30;

/**
 * Login / Create-a-Student-Profile / Enter-OTP — spec.md Page 1 SDD
 * updates. One shared modal transitions its content between steps rather
 * than stacking separate modals ("Same modal system... only their content
 * and state differ").
 *
 * Scope boundary (phase.md Phase 03): only the mobile+OTP mechanics are
 * built here. What happens after a *new* account's OTP succeeds — the
 * Basic Information onboarding wizard — is Phase 05's "Student Profile,
 * Skills & Evidence" scope, not invented here.
 */
export function AuthModalProvider({ children }: { children: React.ReactNode }) {
  const auth = useAuth();
  const navigate = useNavigate();
  const onboarding = useOnboardingModal();

  const [open, setOpen] = React.useState(false);
  const [flow, setFlow] = React.useState<AuthPurpose>("login");
  const [step, setStep] = React.useState<Step>("mobile");
  const [mobile, setMobile] = React.useState("");
  const [mobileIssue, setMobileIssue] = React.useState<MobileIssue>(null);
  const [otp, setOtp] = React.useState("");
  const [otpError, setOtpError] = React.useState(false);
  const [loading, setLoading] = React.useState(false);
  const [resendIn, setResendIn] = React.useState(0);

  const mobileValid = /^\d{10}$/.test(mobile);

  React.useEffect(() => {
    if (resendIn <= 0) return;
    const id = setInterval(() => setResendIn((s) => Math.max(0, s - 1)), 1000);
    return () => clearInterval(id);
  }, [resendIn]);

  const reset = () => {
    setFlow("login");
    setStep("mobile");
    setMobile("");
    setMobileIssue(null);
    setOtp("");
    setOtpError(false);
    setLoading(false);
    setResendIn(0);
  };

  const openLogin = () => {
    reset();
    setFlow("login");
    setOpen(true);
  };
  const openRegister = () => {
    reset();
    setFlow("register");
    setOpen(true);
  };

  const switchFlow = (nextFlow: AuthPurpose) => {
    setFlow(nextFlow);
    setStep("mobile");
    setMobileIssue(null);
  };

  const requestOtp = async () => {
    if (!mobileValid || loading) return;
    setLoading(true);
    setMobileIssue(null);
    try {
      await sendOtp(mobile, flow);
      setOtp("");
      setOtpError(false);
      setStep("otp");
      setResendIn(RESEND_COOLDOWN_SECONDS);
    } catch (err) {
      if (err instanceof ApiError && err.status === 404) setMobileIssue("not_found");
      else if (err instanceof ApiError && err.status === 409) setMobileIssue("already_exists");
    } finally {
      setLoading(false);
    }
  };

  const resend = async () => {
    if (resendIn > 0 || loading) return;
    setLoading(true);
    try {
      await sendOtp(mobile, flow);
      setOtp("");
      setOtpError(false);
      setResendIn(RESEND_COOLDOWN_SECONDS);
    } finally {
      setLoading(false);
    }
  };

  const submitOtp = (code: string, currentFlow: AuthPurpose, currentMobile: string) => {
    setLoading(true);
    verifyOtp(currentMobile, code, currentFlow)
      .then((res) => {
        auth.login(res.token, res.role, currentMobile);
        setOpen(false);
        // spec.md: a valid OTP from the Create Account side "automatically
        // proceeds" into Basic Information (still on Page 1), never into
        // the login destination — it must not navigate away at all here.
        if (currentFlow === "register") onboarding.start();
        else navigate(res.redirect);
      })
      .catch((err) => {
        if (err instanceof ApiError && err.status === 400) {
          setOtpError(true);
          setOtp("");
        }
      })
      .finally(() => setLoading(false));
  };

  const handleOtpChange = (next: string) => {
    setOtp(next);
    setOtpError(false);
    if (next.length === 4 && !loading) submitOtp(next, flow, mobile);
  };

  const value: AuthModalContextValue = { openLogin, openRegister };

  const title =
    step === "otp" ? "Enter OTP" : flow === "login" ? "Welcome" : "Create a Student Profile";

  return (
    <AuthModalContext.Provider value={value}>
      {children}

      <Modal open={open} onOpenChange={setOpen} title={title}>
        {step === "mobile" ? (
          <div className="flex flex-col gap-4">
            {flow === "login" ? (
              <p className="text-sm text-[var(--text-soft)]">Enter your details to continue</p>
            ) : (
              <p className="text-sm text-[var(--text-soft)]">Prepare. Match. Apply. Get Ready.</p>
            )}

            <div className="flex gap-2">
              <span className="lm-input flex w-16 items-center justify-center px-0 text-center">
                +91
              </span>
              <Input
                className="flex-1"
                inputMode="numeric"
                placeholder="Mobile no."
                value={mobile}
                onChange={(e) => {
                  setMobile(e.target.value.replace(/\D/g, "").slice(0, 10));
                  setMobileIssue(null);
                }}
              />
            </div>

            {mobileIssue === "not_found" && (
              <div className="lm-card--flat rounded-[var(--radius)] border border-[var(--border)] p-3 text-sm">
                <p className="text-[var(--text)]">Account Not Found</p>
                <p className="mb-2 text-[var(--text-mute)]">
                  No account exists with this mobile number.
                </p>
                <Button variant="ghost" onClick={() => switchFlow("register")}>
                  Create New Account →
                </Button>
              </div>
            )}
            {mobileIssue === "already_exists" && (
              <div className="lm-card--flat rounded-[var(--radius)] border border-[var(--border)] p-3 text-sm">
                <p className="text-[var(--text)]">Account Already Exists</p>
                <p className="mb-2 text-[var(--text-mute)]">
                  An account has already been created with this mobile number.
                </p>
                <Button variant="ghost" onClick={() => switchFlow("login")}>
                  Go to Login →
                </Button>
              </div>
            )}

            <Button
              variant="primary"
              disabled={!mobileValid || loading}
              onClick={requestOtp}
              className="justify-center"
            >
              Get OTP
            </Button>

            {flow === "login" && !mobileIssue && (
              <p className="text-center text-sm text-[var(--text-mute)]">
                Don&apos;t have account{" "}
                <button
                  type="button"
                  className="text-[var(--accent)] underline underline-offset-2"
                  onClick={() => switchFlow("register")}
                >
                  Create account
                </button>
              </p>
            )}
          </div>
        ) : (
          <div className="flex flex-col gap-4">
            <p className="text-sm text-[var(--text-soft)]">
              We&apos;ve sent a code to +91 {mobile}
            </p>

            <OtpInput value={otp} onChange={handleOtpChange} invalid={otpError} autoFocus />

            {otpError && (
              <p className="text-center text-sm text-[var(--danger)]">
                Incorrect OTP, please try again
              </p>
            )}

            <button
              type="button"
              className="text-center text-sm text-[var(--accent)] underline underline-offset-2"
              onClick={() => {
                setStep("mobile");
                setMobileIssue(null);
              }}
            >
              Incorrect mobile no.
            </button>

            <p className="text-center text-sm text-[var(--text-mute)]">
              Didn&apos;t get the code yet?{" "}
              <button
                type="button"
                disabled={resendIn > 0 || loading}
                className="text-[var(--accent)] underline underline-offset-2 disabled:cursor-not-allowed disabled:text-[var(--text-mute)] disabled:no-underline"
                onClick={resend}
              >
                {resendIn > 0 ? `Resend code (${resendIn}s)` : "Resend code"}
              </button>
            </p>
          </div>
        )}
      </Modal>
    </AuthModalContext.Provider>
  );
}

export function useAuthModal() {
  const ctx = React.useContext(AuthModalContext);
  if (!ctx) throw new Error("useAuthModal must be used within AuthModalProvider");
  return ctx;
}
