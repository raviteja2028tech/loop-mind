import { Plus, Trash2 } from "lucide-react";
import * as React from "react";
import { Badge } from "@/components/Badge";
import { Button } from "@/components/Button";
import { Field, Input } from "@/components/Input";
import { SearchableSelect } from "@/components/Select";
import { ErrorState } from "@/components/States";
import { type DraftSkill, getDraft, putDraftSkills } from "@/lib/api";
import {
  LEARNING_STATUS_OPTIONS,
  PROFICIENCY_OPTIONS,
  SKILL_CATEGORY_OPTIONS,
} from "@/lib/reference-data";
import type { OnboardingStepProps } from "@/website/onboarding/OnboardingModalProvider";

const emptyDraft = {
  skill_name: "",
  skill_category: null as string | null,
  proficiency: null as string | null,
  learning_status: null as string | null,
  experience_years: "",
};

/** spec.md "Create Account -> Current Skills". Multiple entries, all
 * optional overall — Continue is blocked only while a started draft entry
 * is incomplete, never merely because the list is empty.
 *
 * Student Create Account UPDATE SDD: no student account exists yet, so
 * skills have no server-assigned ids to CRUD against — the whole list is
 * held locally and saved to the registration draft as one unit on every
 * change. */
export default function CurrentSkillsStep({ onBack, onContinue }: OnboardingStepProps) {
  const [skills, setSkills] = React.useState<DraftSkill[]>([]);
  const [draft, setDraft] = React.useState(emptyDraft);
  const [evidenceDraft, setEvidenceDraft] = React.useState<Record<number, string>>({});
  const [error, setError] = React.useState<string | null>(null);

  React.useEffect(() => {
    getDraft().then((d) => setSkills(d.skills));
  }, []);

  const draftStarted =
    draft.skill_name.trim() !== "" ||
    draft.skill_category !== null ||
    draft.proficiency !== null ||
    draft.learning_status !== null ||
    draft.experience_years.trim() !== "";
  const draftComplete =
    draft.skill_name.trim() !== "" &&
    draft.skill_category &&
    draft.proficiency &&
    draft.learning_status;
  const canContinue = !draftStarted || draftComplete;

  async function persist(next: DraftSkill[]) {
    setSkills(next);
    try {
      await putDraftSkills(next);
    } catch {
      setError("Could not save. Try again.");
    }
  }

  const addSkill = async () => {
    if (!draftComplete) return;
    await persist([
      ...skills,
      {
        skill_name: draft.skill_name,
        skill_category: draft.skill_category!,
        proficiency: draft.proficiency!,
        learning_status: draft.learning_status!,
        experience_years:
          draft.experience_years.trim() === "" ? null : Number(draft.experience_years),
        evidence: [],
      },
    ]);
    setDraft(emptyDraft);
  };

  const removeSkill = async (index: number) => {
    await persist(skills.filter((_, i) => i !== index));
  };

  const submitEvidence = async (index: number) => {
    const description = evidenceDraft[index]?.trim();
    if (!description) return;
    await persist(
      skills.map((s, i) =>
        i === index ? { ...s, evidence: [...s.evidence, { description, link: null }] } : s,
      ),
    );
    setEvidenceDraft((prev) => ({ ...prev, [index]: "" }));
  };

  return (
    <div className="flex flex-col gap-4">
      {skills.length > 0 && (
        <div className="flex flex-col gap-2">
          {skills.map((skill, index) => (
            <div
              key={index}
              className="lm-card--flat rounded-[var(--radius)] border border-[var(--border)] p-3"
            >
              <div className="flex items-center justify-between gap-2">
                <div>
                  <span className="font-medium text-[var(--text)]">{skill.skill_name}</span>{" "}
                  <Badge variant="neutral">{skill.proficiency}</Badge>{" "}
                  <span className="text-xs text-[var(--text-mute)]">{skill.skill_category}</span>
                </div>
                <button
                  type="button"
                  onClick={() => removeSkill(index)}
                  aria-label="Remove skill"
                >
                  <Trash2 className="size-4 text-[var(--text-mute)]" />
                </button>
              </div>
              {skill.evidence.map((e, eIndex) => (
                <p key={eIndex} className="mt-1 text-xs text-[var(--text-soft)]">
                  → {e.description}
                </p>
              ))}
              <div className="mt-2 flex gap-2">
                <Input
                  placeholder="Add project or supporting evidence"
                  value={evidenceDraft[index] ?? ""}
                  onChange={(e) =>
                    setEvidenceDraft((prev) => ({ ...prev, [index]: e.target.value }))
                  }
                />
                <Button variant="ghost" onClick={() => submitEvidence(index)}>
                  Add
                </Button>
              </div>
            </div>
          ))}
        </div>
      )}

      <div className="lm-card--flat rounded-[var(--radius)] border border-dashed border-[var(--border-hi)] p-3">
        <div className="grid gap-3 sm:grid-cols-2">
          <Field label="Skill Name">
            <Input
              value={draft.skill_name}
              onChange={(e) => setDraft((d) => ({ ...d, skill_name: e.target.value }))}
            />
          </Field>
          <Field label="Skill category">
            <SearchableSelect
              options={SKILL_CATEGORY_OPTIONS}
              value={draft.skill_category}
              onChange={(v) => setDraft((d) => ({ ...d, skill_category: v }))}
              placeholder="Category"
            />
          </Field>
          <Field label="Proficiency">
            <SearchableSelect
              options={PROFICIENCY_OPTIONS}
              value={draft.proficiency}
              onChange={(v) => setDraft((d) => ({ ...d, proficiency: v }))}
              placeholder="Proficiency"
            />
          </Field>
          <Field label="Learning Status">
            <SearchableSelect
              options={LEARNING_STATUS_OPTIONS}
              value={draft.learning_status}
              onChange={(v) => setDraft((d) => ({ ...d, learning_status: v }))}
              placeholder="Learning status"
            />
          </Field>
          <Field label="Experience in years">
            <Input
              inputMode="decimal"
              value={draft.experience_years}
              onChange={(e) => setDraft((d) => ({ ...d, experience_years: e.target.value }))}
            />
          </Field>
        </div>
        <Button variant="ghost" disabled={!draftComplete} onClick={addSkill} className="mt-3">
          <Plus className="size-4" /> Add Skill
        </Button>
      </div>

      {error && <ErrorState message={error} />}

      <div className="flex justify-between">
        <Button variant="ghost" onClick={onBack}>
          Back
        </Button>
        <Button variant="primary" disabled={!canContinue} onClick={onContinue}>
          Continue
        </Button>
      </div>
    </div>
  );
}
