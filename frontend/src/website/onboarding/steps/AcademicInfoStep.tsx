import * as React from "react";
import { Button } from "@/components/Button";
import { Field, Input } from "@/components/Input";
import { SearchableSelect } from "@/components/Select";
import { ErrorState } from "@/components/States";
import { getDraft, putDraftAcademicInfo } from "@/lib/api";
import {
  ACADEMIC_YEAR_OPTIONS,
  branchOptionsFor,
  CGPA_SCALE_OPTIONS,
  COLLEGE_OPTIONS,
  CURRENT_SEMESTER_OPTIONS,
  CURRENT_YEAR_OPTIONS,
  DEGREE_OPTIONS,
  YEAR_OPTIONS,
} from "@/lib/reference-data";
import type { OnboardingStepProps } from "@/website/onboarding/OnboardingModalProvider";

/** spec.md "Create Account -> Academic Information". Back is always
 * active; Continue only after all required fields are complete — the two
 * score fields are explicitly optional. */
export default function AcademicInfoStep({ onBack, onContinue }: OnboardingStepProps) {
  const [college, setCollege] = React.useState<string | null>(null);
  const [degree, setDegree] = React.useState<string | null>(null);
  const [branch, setBranch] = React.useState<string | null>(null);
  const [academicYear, setAcademicYear] = React.useState<string | null>(null);
  const [currentYear, setCurrentYear] = React.useState<string | null>(null);
  const [currentSemester, setCurrentSemester] = React.useState<string | null>(null);
  const [admissionYear, setAdmissionYear] = React.useState<string | null>(null);
  const [gradYear, setGradYear] = React.useState<string | null>(null);
  const [cgpa, setCgpa] = React.useState("");
  const [cgpaScale, setCgpaScale] = React.useState<string | null>(null);
  const [tenth, setTenth] = React.useState("");
  const [twelfth, setTwelfth] = React.useState("");
  const [saving, setSaving] = React.useState(false);
  const [error, setError] = React.useState<string | null>(null);

  React.useEffect(() => {
    getDraft().then((draft) => {
      const info = draft.academic_info;
      if (!info) return;
      setCollege(info.college);
      setDegree(info.degree);
      setBranch(info.branch);
      setAcademicYear(info.academic_year);
      setCurrentYear(info.current_year);
      setCurrentSemester(info.current_semester);
      setAdmissionYear(info.admission_year);
      setGradYear(info.expected_graduation_year);
      setCgpa(String(info.current_cgpa));
      setCgpaScale(info.cgpa_scale);
      if (info.tenth_score_percentage != null) setTenth(String(info.tenth_score_percentage));
      if (info.twelfth_score_percentage != null) setTwelfth(String(info.twelfth_score_percentage));
    });
  }, []);

  const canContinue =
    college &&
    degree &&
    branch &&
    academicYear &&
    currentYear &&
    currentSemester &&
    admissionYear &&
    gradYear &&
    cgpa.trim() !== "" &&
    cgpaScale;

  const handleContinue = async () => {
    if (!canContinue) return;
    setSaving(true);
    setError(null);
    try {
      await putDraftAcademicInfo({
        college: college!,
        degree: degree!,
        branch: branch!,
        academic_year: academicYear!,
        current_year: currentYear!,
        current_semester: currentSemester!,
        admission_year: admissionYear!,
        expected_graduation_year: gradYear!,
        current_cgpa: Number(cgpa),
        cgpa_scale: cgpaScale!,
        tenth_score_percentage: tenth.trim() === "" ? null : Number(tenth),
        twelfth_score_percentage: twelfth.trim() === "" ? null : Number(twelfth),
      });
      onContinue();
    } catch {
      setError("Could not save. Try again.");
    } finally {
      setSaving(false);
    }
  };

  return (
    <div className="flex flex-col gap-4">
      <div className="grid gap-4 sm:grid-cols-3">
        <Field label="College">
          <SearchableSelect
            options={COLLEGE_OPTIONS}
            value={college}
            onChange={setCollege}
            placeholder="College"
          />
        </Field>
        <Field label="Degree">
          <SearchableSelect
            options={DEGREE_OPTIONS}
            value={degree}
            onChange={(v) => {
              setDegree(v);
              setBranch(null);
            }}
            placeholder="Degree"
          />
        </Field>
        <Field label="Branch">
          <SearchableSelect
            options={branchOptionsFor(degree)}
            value={branch}
            onChange={setBranch}
            placeholder="Branch"
            disabled={!degree}
          />
        </Field>
      </div>

      <div className="grid gap-4 sm:grid-cols-3">
        <Field label="Academic year">
          <SearchableSelect
            options={ACADEMIC_YEAR_OPTIONS}
            value={academicYear}
            onChange={setAcademicYear}
            placeholder="Academic year"
          />
        </Field>
        <Field label="Current year">
          <SearchableSelect
            options={CURRENT_YEAR_OPTIONS}
            value={currentYear}
            onChange={setCurrentYear}
            placeholder="Current year"
          />
        </Field>
        <Field label="Current semester">
          <SearchableSelect
            options={CURRENT_SEMESTER_OPTIONS}
            value={currentSemester}
            onChange={setCurrentSemester}
            placeholder="Current semester"
          />
        </Field>
      </div>

      <div className="grid gap-4 sm:grid-cols-2">
        <Field label="Admission year">
          <SearchableSelect
            options={YEAR_OPTIONS}
            value={admissionYear}
            onChange={setAdmissionYear}
            placeholder="Admission year"
          />
        </Field>
        <Field label="Expected graduation year">
          <SearchableSelect
            options={YEAR_OPTIONS}
            value={gradYear}
            onChange={setGradYear}
            placeholder="Graduation year"
          />
        </Field>
      </div>

      <div className="grid gap-4 sm:grid-cols-2">
        <Field label="Current CGPA">
          <Input inputMode="decimal" value={cgpa} onChange={(e) => setCgpa(e.target.value)} />
        </Field>
        <Field label="CGPA scale">
          <SearchableSelect
            options={CGPA_SCALE_OPTIONS}
            value={cgpaScale}
            onChange={setCgpaScale}
            placeholder="Scale"
          />
        </Field>
      </div>

      <div className="grid gap-4 sm:grid-cols-2">
        <Field label="10th score in percentage (optional)">
          <Input inputMode="decimal" value={tenth} onChange={(e) => setTenth(e.target.value)} />
        </Field>
        <Field label="12th / Diploma score in percentage (optional)">
          <Input inputMode="decimal" value={twelfth} onChange={(e) => setTwelfth(e.target.value)} />
        </Field>
      </div>

      {error && <ErrorState message={error} />}

      <div className="flex justify-between">
        <Button variant="ghost" onClick={onBack}>
          Back
        </Button>
        <Button variant="primary" disabled={!canContinue || saving} onClick={handleContinue}>
          Continue
        </Button>
      </div>
    </div>
  );
}
