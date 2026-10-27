import * as React from "react";
import { Button } from "@/components/Button";
import { Field, Input } from "@/components/Input";
import { SearchableSelect } from "@/components/Select";
import { TagInput } from "@/components/TagInput";
import { type CareerPlacement, getDraft, putDraftCareerPlacement } from "@/lib/api";
import {
  cityOptionsFor,
  COUNTRY_OPTIONS,
  INTERNSHIP_INTEREST_OPTIONS,
  JOB_TYPE_PREFERENCE_OPTIONS,
  CAREER_INTEREST_OPTIONS,
  PLACEMENT_INTEREST_OPTIONS,
  PLACEMENT_STATUS_OPTIONS,
  REMOTE_ONSITE_HYBRID_OPTIONS,
  stateOptionsFor,
} from "@/lib/reference-data";
import type { OnboardingStepProps } from "@/website/onboarding/OnboardingModalProvider";

const EMPTY: CareerPlacement = {
  career_interest: null,
  target_job_role: null,
  preferred_job_domain: null,
  target_company: null,
  target_role: null,
  preferred_technology_skill_area: [],
  placement_interest: null,
  internship_interest: null,
  preferred_job_type: null,
  preferred_work_location: null,
  preferred_country: null,
  preferred_state: null,
  preferred_city: null,
  remote_onsite_hybrid: null,
  preferred_industry: null,
  placement_status: null,
};

/** spec.md SDD "CAREER / PLACEMENT" — every field optional, all fillable
 * from the same established searchable-dropdown/tag-input controls used
 * throughout onboarding. */
export default function CareerPlacementStep({ onBack, onContinue }: OnboardingStepProps) {
  const [data, setData] = React.useState<CareerPlacement>(EMPTY);
  const [saving, setSaving] = React.useState(false);

  React.useEffect(() => {
    getDraft().then((d) => d.career_placement && setData(d.career_placement));
  }, []);

  async function handleContinue() {
    setSaving(true);
    try {
      await putDraftCareerPlacement(data);
      onContinue();
    } finally {
      setSaving(false);
    }
  }

  return (
    <div className="flex flex-col gap-4">
      <div className="grid gap-3 sm:grid-cols-2">
        <Field label="Career Interest">
          <SearchableSelect
            options={CAREER_INTEREST_OPTIONS}
            value={data.career_interest}
            onChange={(v) => setData((d) => ({ ...d, career_interest: v }))}
            placeholder="Select an interest…"
          />
        </Field>
        <Field label="Target Job Role">
          <Input
            value={data.target_job_role ?? ""}
            onChange={(e) => setData((d) => ({ ...d, target_job_role: e.target.value }))}
          />
        </Field>
      </div>
      <div className="grid gap-3 sm:grid-cols-2">
        <Field label="Target Company">
          <Input
            value={data.target_company ?? ""}
            onChange={(e) => setData((d) => ({ ...d, target_company: e.target.value }))}
          />
        </Field>
        <Field label="Target Role">
          <Input
            value={data.target_role ?? ""}
            onChange={(e) => setData((d) => ({ ...d, target_role: e.target.value }))}
          />
        </Field>
      </div>
      <Field label="Preferred Technology / Skill Area">
        <TagInput
          value={data.preferred_technology_skill_area}
          onChange={(v) => setData((d) => ({ ...d, preferred_technology_skill_area: v }))}
          placeholder="Backend, Cloud, ML…"
        />
      </Field>
      <div className="grid gap-3 sm:grid-cols-2">
        <Field label="Placement Interest">
          <SearchableSelect
            options={PLACEMENT_INTEREST_OPTIONS}
            value={data.placement_interest}
            onChange={(v) => setData((d) => ({ ...d, placement_interest: v }))}
            placeholder="Select…"
          />
        </Field>
        <Field label="Internship Interest">
          <SearchableSelect
            options={INTERNSHIP_INTEREST_OPTIONS}
            value={data.internship_interest}
            onChange={(v) => setData((d) => ({ ...d, internship_interest: v }))}
            placeholder="Select…"
          />
        </Field>
      </div>
      <div className="grid gap-3 sm:grid-cols-2">
        <Field label="Preferred Job Type">
          <SearchableSelect
            options={JOB_TYPE_PREFERENCE_OPTIONS}
            value={data.preferred_job_type}
            onChange={(v) => setData((d) => ({ ...d, preferred_job_type: v }))}
            placeholder="Select…"
          />
        </Field>
        <Field label="Remote / On-site / Hybrid">
          <SearchableSelect
            options={REMOTE_ONSITE_HYBRID_OPTIONS}
            value={data.remote_onsite_hybrid}
            onChange={(v) => setData((d) => ({ ...d, remote_onsite_hybrid: v }))}
            placeholder="Select…"
          />
        </Field>
      </div>
      <div className="grid gap-3 sm:grid-cols-3">
        <Field label="Preferred Country">
          <SearchableSelect
            options={COUNTRY_OPTIONS}
            value={data.preferred_country}
            onChange={(v) =>
              setData((d) => ({
                ...d,
                preferred_country: v,
                preferred_state: null,
                preferred_city: null,
              }))
            }
            placeholder="Country"
          />
        </Field>
        <Field label="Preferred State">
          <SearchableSelect
            options={stateOptionsFor(data.preferred_country)}
            value={data.preferred_state}
            onChange={(v) => setData((d) => ({ ...d, preferred_state: v, preferred_city: null }))}
            placeholder="State"
            disabled={!data.preferred_country}
          />
        </Field>
        <Field label="Preferred City">
          <SearchableSelect
            options={cityOptionsFor(data.preferred_country, data.preferred_state)}
            value={data.preferred_city}
            onChange={(v) => setData((d) => ({ ...d, preferred_city: v }))}
            placeholder="City"
            disabled={!data.preferred_state}
          />
        </Field>
      </div>
      <div className="grid gap-3 sm:grid-cols-2">
        <Field label="Preferred Industry">
          <Input
            value={data.preferred_industry ?? ""}
            onChange={(e) => setData((d) => ({ ...d, preferred_industry: e.target.value }))}
          />
        </Field>
        <Field label="Placement Status">
          <SearchableSelect
            options={PLACEMENT_STATUS_OPTIONS}
            value={data.placement_status}
            onChange={(v) => setData((d) => ({ ...d, placement_status: v }))}
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
