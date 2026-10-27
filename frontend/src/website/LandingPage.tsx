import { Bot, FileText, Gauge } from "lucide-react";
import { Card, GlobalFooter, Navbar, Shell, useAuthModal, useInfoModals } from "@/components";

const FEATURES = [
  {
    icon: Gauge,
    title: "Placement Readiness",
    description: "Know your skill gaps and what to improve before you apply.",
  },
  {
    icon: FileText,
    title: "Read Job Applications",
    description:
      "Apply to real jobs when you're ready and let your profile move into the recruitment process.",
  },
  {
    icon: Bot,
    title: "AI Recruitment",
    description: "Screen, match, shortlist, and evaluate candidates with AI-assisted recruitment.",
  },
] as const;

/**
 * LOOP-MIND Page 1 — Landing Page. spec.md "LOOP-MIND — PAGE 1 SDD".
 *
 * Login opens the shared Login/Create-Account/OTP modal (phase.md Phase
 * 03). The onboarding wizard reached after a *new* account's OTP succeeds
 * (Basic Information onward) remains Phase 05 scope.
 */
export default function LandingPage() {
  const { openHelp } = useInfoModals();
  const { openLogin } = useAuthModal();

  return (
    <Shell
      navbar={
        <Navbar
          brand="LOOP-MIND"
          right={
            <>
              <button type="button" className="lm-nav-link" onClick={openLogin}>
                Login
              </button>
              <button type="button" className="lm-nav-link" onClick={openHelp}>
                Help
              </button>
            </>
          }
        />
      }
      footer={<GlobalFooter />}
    >
      <div className="flex w-full flex-1 flex-col items-center justify-center gap-10 py-10">
        <section className="mx-auto flex max-w-[720px] flex-col items-center gap-4 text-center">
          <h1>Prepare. Match. Apply. Get Ready.</h1>
          <p className="text-[15px] leading-relaxed text-[var(--text-soft)]">
            LOOP-MIND connects students with real opportunities, evaluates their readiness,
            identifies what to improve, and helps turn every application into smarter
            preparation.
          </p>
        </section>

        <Card className="mx-auto w-full max-w-[960px]">
          <div className="grid gap-8 sm:grid-cols-3">
            {FEATURES.map(({ icon: Icon, title, description }) => (
              <div key={title} className="flex flex-col items-center gap-2 text-center">
                <Icon className="size-6 text-[var(--accent)]" aria-hidden />
                <h3>{title}</h3>
                <p className="text-sm text-[var(--text-soft)]">{description}</p>
              </div>
            ))}
          </div>
        </Card>
      </div>
    </Shell>
  );
}
