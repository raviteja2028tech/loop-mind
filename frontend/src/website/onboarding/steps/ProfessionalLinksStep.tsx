import * as React from "react";
import { Button } from "@/components/Button";
import { Dropzone } from "@/components/Dropzone";
import { Field, Input } from "@/components/Input";
import { ErrorState } from "@/components/States";
import {
  ApiError,
  getDraft,
  type ProfessionalLinks,
  putDraftProfessionalLinks,
  uploadDraftResume,
} from "@/lib/api";
import type { OnboardingStepProps } from "@/website/onboarding/OnboardingModalProvider";

const EMPTY: Omit<ProfessionalLinks, "resume_file_path"> = {
  github_url: null,
  linkedin_url: null,
  portfolio_website_url: null,
  coding_profile_url: null,
  other_professional_profile_url: null,
};

/** spec.md SDD "PROFESSIONAL LINKS + RESUME" — every link optional; the
 * resume itself is required elsewhere (Jobs page application flow), not
 * gated here, so onboarding can complete without one. */
export default function ProfessionalLinksStep({ onBack, onContinue }: OnboardingStepProps) {
  const [data, setData] = React.useState(EMPTY);
  const [resumeName, setResumeName] = React.useState<string | null>(null);
  const [resumeError, setResumeError] = React.useState<string | null>(null);
  const [uploadingResume, setUploadingResume] = React.useState(false);
  const [saving, setSaving] = React.useState(false);

  React.useEffect(() => {
    getDraft().then((draft) => {
      if (draft.professional_links) setData(draft.professional_links);
      if (draft.resume_file_path) setResumeName("Resume on file");
    });
  }, []);

  async function handleResume(files: File[]) {
    const file = files[0];
    if (!file) return;
    setResumeError(null);

    // Dropzone's `accept` only filters the native file picker dialog, not
    // a drag-and-drop — a non-PDF file can still reach here either way, so
    // it's checked before ever attempting the upload.
    const isPdf = file.type === "application/pdf" || file.name.toLowerCase().endsWith(".pdf");
    if (!isPdf) {
      setResumeError("Resume must be a PDF file.");
      return;
    }

    setUploadingResume(true);
    try {
      await uploadDraftResume(file);
      setResumeName(file.name);
    } catch (err) {
      setResumeError(err instanceof ApiError ? String(err.body) : "Could not upload resume.");
    } finally {
      setUploadingResume(false);
    }
  }

  async function handleContinue() {
    setSaving(true);
    try {
      await putDraftProfessionalLinks(data);
      onContinue();
    } finally {
      setSaving(false);
    }
  }

  return (
    <div className="flex flex-col gap-4">
      <div className="grid gap-3 sm:grid-cols-2">
        <Field label="GitHub URL">
          <Input
            value={data.github_url ?? ""}
            onChange={(e) => setData((d) => ({ ...d, github_url: e.target.value }))}
          />
        </Field>
        <Field label="LinkedIn URL">
          <Input
            value={data.linkedin_url ?? ""}
            onChange={(e) => setData((d) => ({ ...d, linkedin_url: e.target.value }))}
          />
        </Field>
      </div>
      <div className="grid gap-3 sm:grid-cols-2">
        <Field label="Portfolio Website URL">
          <Input
            value={data.portfolio_website_url ?? ""}
            onChange={(e) => setData((d) => ({ ...d, portfolio_website_url: e.target.value }))}
          />
        </Field>
        <Field label="Coding Profile URL">
          <Input
            value={data.coding_profile_url ?? ""}
            onChange={(e) => setData((d) => ({ ...d, coding_profile_url: e.target.value }))}
          />
        </Field>
      </div>
      <Field label="Other Professional Profile URL">
        <Input
          value={data.other_professional_profile_url ?? ""}
          onChange={(e) =>
            setData((d) => ({ ...d, other_professional_profile_url: e.target.value }))
          }
        />
      </Field>
      <Field label="Resume (PDF, optional here)">
        <Dropzone
          accept="application/pdf"
          onFiles={handleResume}
          hint={
            uploadingResume ? "Uploading…" : (resumeName ?? "Upload your resume as a PDF")
          }
        />
      </Field>
      {resumeError && <ErrorState message={resumeError} />}

      <div className="flex justify-between">
        <Button variant="ghost" onClick={onBack}>
          Back
        </Button>
        <Button variant="primary" onClick={handleContinue} disabled={saving}>
          {saving ? "Saving…" : "Continue"}
        </Button>
      </div>
    </div>
  );
}
