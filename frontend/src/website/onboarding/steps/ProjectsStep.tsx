import { Plus, Trash2 } from "lucide-react";
import * as React from "react";
import { Button } from "@/components/Button";
import { Field, Input, Textarea } from "@/components/Input";
import { SearchableSelect } from "@/components/Select";
import { TagInput } from "@/components/TagInput";
import { getDraft, putDraftProjects, type StudentProject } from "@/lib/api";

type DraftProject = Omit<StudentProject, "id">;
import {
  PROJECT_STATUS_OPTIONS,
  PROJECT_TYPE_OPTIONS,
  TEAM_OR_INDIVIDUAL_OPTIONS,
} from "@/lib/reference-data";
import type { OnboardingStepProps } from "@/website/onboarding/OnboardingModalProvider";

const emptyDraft = {
  project_name: "",
  project_description: "",
  project_type: null as string | null,
  project_status: null as string | null,
  start_date: "",
  end_date: "",
  technologies_used: [] as string[],
  programming_languages: [] as string[],
  frameworks: [] as string[],
  tools: [] as string[],
  skills_demonstrated: [] as string[],
  student_role: "",
  team_or_individual: null as string | null,
  github_repository: "",
  live_demo: "",
  project_documentation: "",
  project_evidence: "",
};

/** spec.md SDD "PROJECTS". Project Name is the only practically-required
 * field (an unnamed project can't be listed) — everything else is
 * genuinely optional per the source spec's own scope boundary. */
export default function ProjectsStep({ onBack, onContinue }: OnboardingStepProps) {
  const [projects, setProjects] = React.useState<DraftProject[]>([]);
  const [draft, setDraft] = React.useState(emptyDraft);

  React.useEffect(() => {
    getDraft().then((d) => setProjects(d.projects));
  }, []);

  async function persist(next: DraftProject[]) {
    setProjects(next);
    await putDraftProjects(next);
  }

  const addProject = async () => {
    if (draft.project_name.trim() === "") return;
    await persist([
      ...projects,
      {
        project_name: draft.project_name,
        project_description: draft.project_description || null,
        project_type: draft.project_type,
        project_status: draft.project_status,
        start_date: draft.start_date || null,
        end_date: draft.end_date || null,
        technologies_used: draft.technologies_used,
        programming_languages: draft.programming_languages,
        frameworks: draft.frameworks,
        tools: draft.tools,
        skills_demonstrated: draft.skills_demonstrated,
        student_role: draft.student_role || null,
        team_or_individual: draft.team_or_individual,
        github_repository: draft.github_repository || null,
        live_demo: draft.live_demo || null,
        project_documentation: draft.project_documentation || null,
        project_evidence: draft.project_evidence || null,
      },
    ]);
    setDraft(emptyDraft);
  };

  const removeProject = async (index: number) => {
    await persist(projects.filter((_, i) => i !== index));
  };

  return (
    <div className="flex flex-col gap-4">
      {projects.map((project, index) => (
        <div
          key={index}
          className="lm-card--flat flex items-start justify-between rounded-[var(--radius)] border border-[var(--border)] p-3 text-sm text-[var(--text-soft)]"
        >
          <div>
            <span className="font-medium text-[var(--text)]">{project.project_name}</span>
            {project.technologies_used.length > 0 && (
              <p className="text-xs text-[var(--text-mute)]">
                {project.technologies_used.join(", ")}
              </p>
            )}
          </div>
          <button
            type="button"
            onClick={() => removeProject(index)}
            aria-label="Remove project"
          >
            <Trash2 className="size-4 text-[var(--text-mute)]" />
          </button>
        </div>
      ))}

      <div className="lm-card--flat rounded-[var(--radius)] border border-dashed border-[var(--border-hi)] p-3">
        <Field label="Project Name">
          <Input
            value={draft.project_name}
            onChange={(e) => setDraft((d) => ({ ...d, project_name: e.target.value }))}
          />
        </Field>
        <Field label="Project Description">
          <Textarea
            rows={2}
            value={draft.project_description}
            onChange={(e) => setDraft((d) => ({ ...d, project_description: e.target.value }))}
          />
        </Field>
        <div className="grid gap-3 sm:grid-cols-3">
          <Field label="Project Type">
            <SearchableSelect
              options={PROJECT_TYPE_OPTIONS}
              value={draft.project_type}
              onChange={(v) => setDraft((d) => ({ ...d, project_type: v }))}
              placeholder="Type"
            />
          </Field>
          <Field label="Project Status">
            <SearchableSelect
              options={PROJECT_STATUS_OPTIONS}
              value={draft.project_status}
              onChange={(v) => setDraft((d) => ({ ...d, project_status: v }))}
              placeholder="Status"
            />
          </Field>
          <Field label="Team / Individual">
            <SearchableSelect
              options={TEAM_OR_INDIVIDUAL_OPTIONS}
              value={draft.team_or_individual}
              onChange={(v) => setDraft((d) => ({ ...d, team_or_individual: v }))}
              placeholder="Team or Individual"
            />
          </Field>
        </div>
        <div className="grid gap-3 sm:grid-cols-2">
          <Field label="Start Date">
            <Input
              type="date"
              value={draft.start_date}
              onChange={(e) => setDraft((d) => ({ ...d, start_date: e.target.value }))}
            />
          </Field>
          <Field label="End Date">
            <Input
              type="date"
              value={draft.end_date}
              onChange={(e) => setDraft((d) => ({ ...d, end_date: e.target.value }))}
            />
          </Field>
        </div>
        <Field label="Technologies Used">
          <TagInput
            value={draft.technologies_used}
            onChange={(v) => setDraft((d) => ({ ...d, technologies_used: v }))}
            placeholder="React, PostgreSQL…"
          />
        </Field>
        <Field label="Programming Languages">
          <TagInput
            value={draft.programming_languages}
            onChange={(v) => setDraft((d) => ({ ...d, programming_languages: v }))}
            placeholder="TypeScript, Python…"
          />
        </Field>
        <div className="grid gap-3 sm:grid-cols-2">
          <Field label="Frameworks">
            <TagInput
              value={draft.frameworks}
              onChange={(v) => setDraft((d) => ({ ...d, frameworks: v }))}
              placeholder="Express, Django…"
            />
          </Field>
          <Field label="Tools">
            <TagInput
              value={draft.tools}
              onChange={(v) => setDraft((d) => ({ ...d, tools: v }))}
              placeholder="Docker, Figma…"
            />
          </Field>
        </div>
        <Field label="Skills Demonstrated">
          <TagInput
            value={draft.skills_demonstrated}
            onChange={(v) => setDraft((d) => ({ ...d, skills_demonstrated: v }))}
            placeholder="System Design, REST APIs…"
          />
        </Field>
        <Field label="Student's Role">
          <Input
            value={draft.student_role}
            onChange={(e) => setDraft((d) => ({ ...d, student_role: e.target.value }))}
          />
        </Field>
        <div className="grid gap-3 sm:grid-cols-2">
          <Field label="GitHub Repository">
            <Input
              value={draft.github_repository}
              onChange={(e) => setDraft((d) => ({ ...d, github_repository: e.target.value }))}
            />
          </Field>
          <Field label="Live Demo">
            <Input
              value={draft.live_demo}
              onChange={(e) => setDraft((d) => ({ ...d, live_demo: e.target.value }))}
            />
          </Field>
        </div>
        <div className="grid gap-3 sm:grid-cols-2">
          <Field label="Project Documentation">
            <Input
              value={draft.project_documentation}
              onChange={(e) => setDraft((d) => ({ ...d, project_documentation: e.target.value }))}
              placeholder="Link to a README, doc, or write-up"
            />
          </Field>
          <Field label="Project Evidence">
            <Input
              value={draft.project_evidence}
              onChange={(e) => setDraft((d) => ({ ...d, project_evidence: e.target.value }))}
              placeholder="Link to a demo video, screenshots, etc."
            />
          </Field>
        </div>
        <Button
          variant="ghost"
          disabled={draft.project_name.trim() === ""}
          onClick={addProject}
          className="mt-3"
        >
          <Plus className="size-4" /> Add Project
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
