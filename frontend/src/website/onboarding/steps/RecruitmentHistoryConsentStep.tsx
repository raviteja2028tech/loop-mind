import * as React from "react";
import { Button } from "@/components/Button";
import { ErrorState } from "@/components/States";
import { ApiError, createAccount, getDraft, putDraftConsent, type Consent } from "@/lib/api";
import { useAuth } from "@/lib/auth";
import type { OnboardingStepProps } from "@/website/onboarding/OnboardingModalProvider";

const EMPTY: Consent = {
  consent_use_information: false,
  consent_learning_experience: false,
  consent_anonymized_intelligence: false,
};

/**
 * spec.md SDD "RECRUITMENT HISTORY + CONSENT" — the final onboarding
 * step. Recruitment History has no manually-entered fields here: for a
 * brand-new account there genuinely is none yet (no application exists
 * to show), and once one does, it is derived live from the student's real
 * `JobApplication` records rather than duplicated into a hand-entered
 * form (see backend/schemas/profile_page.py's module docstring) — visible
 * any time from My Profile. This step's real content is Consent, plus a
 * short note on where Recruitment History will appear.
 *
 * The button reads "Create Account" — spec.md's own reference flow names
 * this as the final action, distinct from every earlier step's Continue.
 *
 * Student Create Account UPDATE SDD §10-12: this is the one place the
 * permanent student account is ever created. Before this click, only a
 * temporary registration draft exists (backend/services/
 * registration_service.py) — no real account, anywhere. Create Account
 * stays inactive until all three required consents are given, and on
 * success the registration-only token is replaced with a real student
 * token before continuing into the Student Portal.
 */
export default function RecruitmentHistoryConsentStep({ onBack, onContinue }: OnboardingStepProps) {
  const [consent, setConsent] = React.useState<Consent>(EMPTY);
  const [saving, setSaving] = React.useState(false);
  const [error, setError] = React.useState<string | null>(null);
  const auth = useAuth();

  React.useEffect(() => {
    getDraft().then((d) => d.consent && setConsent(d.consent));
  }, []);

  const hasRequiredConsent =
    consent.consent_use_information &&
    consent.consent_learning_experience &&
    consent.consent_anonymized_intelligence;

  async function handleCreateAccount() {
    if (!hasRequiredConsent) return;
    setSaving(true);
    setError(null);
    try {
      await putDraftConsent(consent);
      const result = await createAccount();
      auth.login(result.token, result.role, auth.mobileNumber ?? "");
      onContinue();
    } catch (err) {
      setError(err instanceof ApiError ? String(err.body) : "Could not create account. Try again.");
    } finally {
      setSaving(false);
    }
  }

  return (
    <div className="flex flex-col gap-4">
      <div className="lm-card--flat rounded-[var(--radius)] border border-[var(--border)] p-3">
        <p className="text-sm font-medium text-[var(--text)]">Recruitment History</p>
        <p className="mt-1 text-xs text-[var(--text-mute)]">
          Your recruitment history — companies applied to, roles, stages reached, and outcomes —
          will appear here automatically once you start applying to jobs. You can view it anytime
          from My Profile.
        </p>
      </div>

      <div className="flex flex-col gap-3">
        <p className="text-sm font-medium text-[var(--text)]">Consent & Knowledge Sharing</p>
        <ConsentToggle
          label="Consent to use relevant information"
          checked={consent.consent_use_information}
          onToggle={() =>
            setConsent((c) => ({ ...c, consent_use_information: !c.consent_use_information }))
          }
        />
        <ConsentToggle
          label="Consent for learning/recruitment experience"
          checked={consent.consent_learning_experience}
          onToggle={() =>
            setConsent((c) => ({
              ...c,
              consent_learning_experience: !c.consent_learning_experience,
            }))
          }
        />
        <ConsentToggle
          label="Consent for anonymized/aggregated intelligence"
          checked={consent.consent_anonymized_intelligence}
          onToggle={() =>
            setConsent((c) => ({
              ...c,
              consent_anonymized_intelligence: !c.consent_anonymized_intelligence,
            }))
          }
        />
      </div>

      {error && <ErrorState message={error} />}

      <div className="flex justify-between">
        <Button variant="ghost" onClick={onBack}>
          Back
        </Button>
        <Button
          variant="primary"
          onClick={handleCreateAccount}
          disabled={saving || !hasRequiredConsent}
        >
          {saving ? "Creating Account…" : "Create Account"}
        </Button>
      </div>
    </div>
  );
}

function ConsentToggle({
  label,
  checked,
  onToggle,
}: {
  label: string;
  checked: boolean;
  onToggle: () => void;
}) {
  return (
    <label className="flex items-center justify-between gap-3 text-sm text-[var(--text-soft)]">
      {label}
      <input type="checkbox" checked={checked} onChange={onToggle} className="size-4" />
    </label>
  );
}
