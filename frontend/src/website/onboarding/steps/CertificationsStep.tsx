import { Plus, Trash2 } from "lucide-react";
import * as React from "react";
import { Button } from "@/components/Button";
import { Field, Input } from "@/components/Input";
import { SearchableSelect } from "@/components/Select";
import { TagInput } from "@/components/TagInput";
import { getDraft, putDraftCertifications, type StudentCertification } from "@/lib/api";
import { CERTIFICATION_TYPE_OPTIONS } from "@/lib/reference-data";
import type { OnboardingStepProps } from "@/website/onboarding/OnboardingModalProvider";

type DraftCertification = Omit<StudentCertification, "id" | "certificate_file_path">;

const emptyDraft = {
  certification_name: "",
  issuing_organization: "",
  certification_type: null as string | null,
  issue_date: "",
  expiry_date: "",
  credential_id: "",
  credential_url: "",
  skills_covered: [] as string[],
};

/** spec.md SDD "CERTIFICATIONS". Certificate File upload — while
 * registering, no account exists yet to attach an uploaded file to, so
 * that control is only offered post-account-creation from My Profile;
 * every other field is available here as before.
 *
 * Student Create Account UPDATE SDD: entries have no server-assigned ids
 * yet — held locally, saved to the registration draft as one list. */
export default function CertificationsStep({ onBack, onContinue }: OnboardingStepProps) {
  const [certifications, setCertifications] = React.useState<DraftCertification[]>([]);
  const [draft, setDraft] = React.useState(emptyDraft);

  React.useEffect(() => {
    getDraft().then((d) => setCertifications(d.certifications));
  }, []);

  async function persist(next: DraftCertification[]) {
    setCertifications(next);
    await putDraftCertifications(next);
  }

  const addCertification = async () => {
    if (draft.certification_name.trim() === "") return;
    await persist([
      ...certifications,
      {
        certification_name: draft.certification_name,
        issuing_organization: draft.issuing_organization || null,
        certification_type: draft.certification_type,
        issue_date: draft.issue_date || null,
        expiry_date: draft.expiry_date || null,
        credential_id: draft.credential_id || null,
        credential_url: draft.credential_url || null,
        skills_covered: draft.skills_covered,
      },
    ]);
    setDraft(emptyDraft);
  };

  const removeCertification = async (index: number) => {
    await persist(certifications.filter((_, i) => i !== index));
  };

  return (
    <div className="flex flex-col gap-4">
      {certifications.map((cert, index) => (
        <div
          key={index}
          className="lm-card--flat flex items-start justify-between rounded-[var(--radius)] border border-[var(--border)] p-3 text-sm text-[var(--text-soft)]"
        >
          <div>
            <span className="font-medium text-[var(--text)]">{cert.certification_name}</span>
            {cert.issuing_organization && (
              <p className="text-xs text-[var(--text-mute)]">{cert.issuing_organization}</p>
            )}
          </div>
          <button
            type="button"
            onClick={() => removeCertification(index)}
            aria-label="Remove certification"
          >
            <Trash2 className="size-4 text-[var(--text-mute)]" />
          </button>
        </div>
      ))}

      <div className="lm-card--flat rounded-[var(--radius)] border border-dashed border-[var(--border-hi)] p-3">
        <div className="grid gap-3 sm:grid-cols-2">
          <Field label="Certification Name">
            <Input
              value={draft.certification_name}
              onChange={(e) => setDraft((d) => ({ ...d, certification_name: e.target.value }))}
            />
          </Field>
          <Field label="Issuing Organization">
            <Input
              value={draft.issuing_organization}
              onChange={(e) => setDraft((d) => ({ ...d, issuing_organization: e.target.value }))}
            />
          </Field>
        </div>
        <Field label="Certification Type">
          <SearchableSelect
            options={CERTIFICATION_TYPE_OPTIONS}
            value={draft.certification_type}
            onChange={(v) => setDraft((d) => ({ ...d, certification_type: v }))}
            placeholder="Type"
          />
        </Field>
        <div className="grid gap-3 sm:grid-cols-2">
          <Field label="Issue Date">
            <Input
              type="date"
              value={draft.issue_date}
              onChange={(e) => setDraft((d) => ({ ...d, issue_date: e.target.value }))}
            />
          </Field>
          <Field label="Expiry Date">
            <Input
              type="date"
              value={draft.expiry_date}
              onChange={(e) => setDraft((d) => ({ ...d, expiry_date: e.target.value }))}
            />
          </Field>
        </div>
        <div className="grid gap-3 sm:grid-cols-2">
          <Field label="Credential ID">
            <Input
              value={draft.credential_id}
              onChange={(e) => setDraft((d) => ({ ...d, credential_id: e.target.value }))}
            />
          </Field>
          <Field label="Credential URL">
            <Input
              value={draft.credential_url}
              onChange={(e) => setDraft((d) => ({ ...d, credential_url: e.target.value }))}
            />
          </Field>
        </div>
        <Field label="Skills Covered">
          <TagInput
            value={draft.skills_covered}
            onChange={(v) => setDraft((d) => ({ ...d, skills_covered: v }))}
            placeholder="AWS, Networking…"
          />
        </Field>
        <Button
          variant="ghost"
          disabled={draft.certification_name.trim() === ""}
          onClick={addCertification}
          className="mt-3"
        >
          <Plus className="size-4" /> Add Certification
        </Button>
      </div>

      <div className="flex justify-between">
        <Button variant="ghost" onClick={onBack}>
          Back
        </Button>
        <Button variant="primary" onClick={onContinue}>
          Continue
        </Button>
      </div>
    </div>
  );
}
