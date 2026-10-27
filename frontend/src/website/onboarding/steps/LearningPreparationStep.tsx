import * as React from "react";
import { Button } from "@/components/Button";
import { Field, Textarea } from "@/components/Input";
import { SearchableSelect } from "@/components/Select";
import { TagInput } from "@/components/TagInput";
import { getDraft, type LearningPreparation, putDraftLearningPreparation } from "@/lib/api";
import {
  ASSESSMENT_PREP_STATUS_OPTIONS,
  INTERVIEW_PREP_STATUS_OPTIONS,
  PREPARATION_STATUS_OPTIONS,
} from "@/lib/reference-data";
import type { OnboardingStepProps } from "@/website/onboarding/OnboardingModalProvider";

const EMPTY: LearningPreparation = {
  current_learning_areas: [],
  skills_currently_learning: [],
  learning_goals: [],
  areas_to_improve: [],
  current_preparation_status: null,
  previous_interview_experience: null,
  previous_assessment_experience: null,
  technical_interview_experience: null,
  coding_assessment_experience: null,
  interview_preparation_status: null,
  assessment_preparation_status: null,
};

/** spec.md SDD "LEARNING / PREPARATION" — every field optional. */
export default function LearningPreparationStep({ onBack, onContinue }: OnboardingStepProps) {
  const [data, setData] = React.useState<LearningPreparation>(EMPTY);
  const [saving, setSaving] = React.useState(false);

  React.useEffect(() => {
    getDraft().then((d) => d.learning_preparation && setData(d.learning_preparation));
  }, []);

  async function handleContinue() {
    setSaving(true);
    try {
      await putDraftLearningPreparation(data);
      onContinue();
    } finally {
      setSaving(false);
    }
  }

  return (
    <div className="flex flex-col gap-4">
      <Field label="Current Learning Areas">
        <TagInput
          value={data.current_learning_areas}
          onChange={(v) => setData((d) => ({ ...d, current_learning_areas: v }))}
          placeholder="DSA, System Design…"
        />
      </Field>
      <Field label="Skills Currently Learning">
        <TagInput
          value={data.skills_currently_learning}
          onChange={(v) => setData((d) => ({ ...d, skills_currently_learning: v }))}
          placeholder="React, Kubernetes…"
        />
      </Field>
      <Field label="Learning Goals">
        <TagInput
          value={data.learning_goals}
          onChange={(v) => setData((d) => ({ ...d, learning_goals: v }))}
          placeholder="Crack a product-based interview…"
        />
      </Field>
      <Field label="Areas They Want to Improve">
        <TagInput
          value={data.areas_to_improve}
          onChange={(v) => setData((d) => ({ ...d, areas_to_improve: v }))}
          placeholder="Communication, System Design…"
        />
      </Field>
      <Field label="Current Preparation Status">
        <SearchableSelect
          options={PREPARATION_STATUS_OPTIONS}
          value={data.current_preparation_status}
          onChange={(v) => setData((d) => ({ ...d, current_preparation_status: v }))}
          placeholder="Select…"
        />
      </Field>
      <div className="grid gap-3 sm:grid-cols-2">
        <Field label="Previous Interview Experience">
          <Textarea
            rows={2}
            value={data.previous_interview_experience ?? ""}
            onChange={(e) =>
              setData((d) => ({ ...d, previous_interview_experience: e.target.value }))
            }
          />
        </Field>
        <Field label="Previous Assessment Experience">
          <Textarea
            rows={2}
            value={data.previous_assessment_experience ?? ""}
            onChange={(e) =>
              setData((d) => ({ ...d, previous_assessment_experience: e.target.value }))
            }
          />
        </Field>
      </div>
      <div className="grid gap-3 sm:grid-cols-2">
        <Field label="Technical Interview Experience">
          <Textarea
            rows={2}
            value={data.technical_interview_experience ?? ""}
            onChange={(e) =>
              setData((d) => ({ ...d, technical_interview_experience: e.target.value }))
            }
          />
        </Field>
        <Field label="Coding Assessment Experience">
          <Textarea
            rows={2}
            value={data.coding_assessment_experience ?? ""}
            onChange={(e) =>
              setData((d) => ({ ...d, coding_assessment_experience: e.target.value }))
            }
          />
        </Field>
      </div>
      <div className="grid gap-3 sm:grid-cols-2">
        <Field label="Interview Preparation Status">
          <SearchableSelect
            options={INTERVIEW_PREP_STATUS_OPTIONS}
            value={data.interview_preparation_status}
            onChange={(v) => setData((d) => ({ ...d, interview_preparation_status: v }))}
            placeholder="Select…"
          />
        </Field>
        <Field label="Assessment Preparation Status">
          <SearchableSelect
            options={ASSESSMENT_PREP_STATUS_OPTIONS}
            value={data.assessment_preparation_status}
            onChange={(v) => setData((d) => ({ ...d, assessment_preparation_status: v }))}
            placeholder="Select…"
          />
        </Field>
      </div>

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
