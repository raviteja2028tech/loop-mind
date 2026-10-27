import { Plus, Trash2 } from "lucide-react";
import * as React from "react";
import { Button } from "@/components/Button";
import { Field, Input } from "@/components/Input";
import { SearchableSelect } from "@/components/Select";
import { TagInput } from "@/components/TagInput";
import { type CodingExperience, getDraft, putDraftCodingExperience } from "@/lib/api";
import { COMPETITIVE_PROGRAMMING_OPTIONS } from "@/lib/reference-data";
import type { OnboardingStepProps } from "@/website/onboarding/OnboardingModalProvider";

type DraftEntry = Omit<CodingExperience, "id">;

const emptyDraft = {
  coding_experience: "",
  programming_languages: [] as string[],
  dsa_experience: "",
  competitive_programming: null as string | null,
  coding_platforms: [] as string[],
  github_link: "",
};

/** spec.md SDD "Coding Experience". None of its fields have a defined
 * required/optional status ("do not invent mandatory fields"), so
 * Continue is never blocked here — only multi-entry support matters.
 *
 * Student Create Account UPDATE SDD: entries have no server-assigned ids
 * yet — held locally, saved to the registration draft as one list. */
export default function CodingExperienceStep({ onBack, onContinue }: OnboardingStepProps) {
  const [entries, setEntries] = React.useState<DraftEntry[]>([]);
  const [draft, setDraft] = React.useState(emptyDraft);

  React.useEffect(() => {
    getDraft().then((d) => setEntries(d.coding_experience));
  }, []);

  const draftHasContent =
    draft.coding_experience.trim() !== "" ||
    draft.programming_languages.length > 0 ||
    draft.dsa_experience.trim() !== "" ||
    draft.competitive_programming !== null ||
    draft.coding_platforms.length > 0 ||
    draft.github_link.trim() !== "";

  async function persist(next: DraftEntry[]) {
    setEntries(next);
    await putDraftCodingExperience(next);
  }

  const addEntry = async () => {
    if (!draftHasContent) return;
    await persist([
      ...entries,
      {
        coding_experience: draft.coding_experience || null,
        programming_languages: draft.programming_languages,
        dsa_experience: draft.dsa_experience || null,
        competitive_programming: draft.competitive_programming,
        coding_platforms: draft.coding_platforms,
        github_link: draft.github_link || null,
      },
    ]);
    setDraft(emptyDraft);
  };

  const removeEntry = async (index: number) => {
    await persist(entries.filter((_, i) => i !== index));
  };

  return (
    <div className="flex flex-col gap-4">
      {entries.map((entry, index) => (
        <div
          key={index}
          className="lm-card--flat flex items-start justify-between rounded-[var(--radius)] border border-[var(--border)] p-3 text-sm text-[var(--text-soft)]"
        >
          <div>
            {entry.coding_experience && <p>{entry.coding_experience}</p>}
            {entry.programming_languages.length > 0 && (
              <p className="text-xs text-[var(--text-mute)]">
                {entry.programming_languages.join(", ")}
              </p>
            )}
            {entry.competitive_programming && (
              <p className="text-xs text-[var(--text-mute)]">
                Competitive: {entry.competitive_programming}
              </p>
            )}
          </div>
          <button type="button" onClick={() => removeEntry(index)} aria-label="Remove entry">
            <Trash2 className="size-4 text-[var(--text-mute)]" />
          </button>
        </div>
      ))}

      <div className="lm-card--flat rounded-[var(--radius)] border border-dashed border-[var(--border-hi)] p-3">
        <div className="grid gap-3 sm:grid-cols-2">
          <Field label="Coding Experience">
            <Input
              value={draft.coding_experience}
              onChange={(e) => setDraft((d) => ({ ...d, coding_experience: e.target.value }))}
            />
          </Field>
          <Field label="DSA Experience">
            <Input
              value={draft.dsa_experience}
              onChange={(e) => setDraft((d) => ({ ...d, dsa_experience: e.target.value }))}
            />
          </Field>
        </div>
        <Field label="Programming Languages">
          <TagInput
            value={draft.programming_languages}
            onChange={(v) => setDraft((d) => ({ ...d, programming_languages: v }))}
            placeholder="Python, Java, JavaScript…"
          />
        </Field>
        <div className="mt-3 grid gap-3 sm:grid-cols-2">
          <Field label="Competitive Programming">
            <SearchableSelect
              options={COMPETITIVE_PROGRAMMING_OPTIONS}
              value={draft.competitive_programming}
              onChange={(v) => setDraft((d) => ({ ...d, competitive_programming: v }))}
              placeholder="Level"
            />
          </Field>
          <Field label="Git-hub link">
            <Input
              value={draft.github_link}
              onChange={(e) => setDraft((d) => ({ ...d, github_link: e.target.value }))}
            />
          </Field>
        </div>
        <Field label="Coding Platforms">
          <TagInput
            value={draft.coding_platforms}
            onChange={(v) => setDraft((d) => ({ ...d, coding_platforms: v }))}
            placeholder="LeetCode, Codeforces…"
          />
        </Field>
        <Button variant="ghost" disabled={!draftHasContent} onClick={addEntry} className="mt-3">
          <Plus className="size-4" /> Add Entry
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
