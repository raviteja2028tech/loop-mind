import * as React from "react";
import { useNavigate } from "react-router-dom";
import { Modal } from "@/components/Modal";
import AcademicInfoStep from "@/website/onboarding/steps/AcademicInfoStep";
import BasicInfoStep from "@/website/onboarding/steps/BasicInfoStep";
import CareerPlacementStep from "@/website/onboarding/steps/CareerPlacementStep";
import CertificationsStep from "@/website/onboarding/steps/CertificationsStep";
import CodingExperienceStep from "@/website/onboarding/steps/CodingExperienceStep";
import CurrentSkillsStep from "@/website/onboarding/steps/CurrentSkillsStep";
import LearningPreparationStep from "@/website/onboarding/steps/LearningPreparationStep";
import ProfessionalLinksStep from "@/website/onboarding/steps/ProfessionalLinksStep";
import ProjectsStep from "@/website/onboarding/steps/ProjectsStep";
import RecruitmentHistoryConsentStep from "@/website/onboarding/steps/RecruitmentHistoryConsentStep";

const STEPS = [
  { key: "basic-info", title: "Basic Information", Component: BasicInfoStep },
  { key: "academic-info", title: "Academic Information", Component: AcademicInfoStep },
  { key: "skills", title: "Current Skills", Component: CurrentSkillsStep },
  { key: "coding-experience", title: "Coding Experience", Component: CodingExperienceStep },
  { key: "projects", title: "PROJECTS", Component: ProjectsStep },
  { key: "certifications", title: "CERTIFICATIONS", Component: CertificationsStep },
  { key: "career-placement", title: "Career / Placement", Component: CareerPlacementStep },
  {
    key: "learning-preparation",
    title: "Learning / Preparation",
    Component: LearningPreparationStep,
  },
  {
    key: "professional-links",
    title: "Professional Links + Resume",
    Component: ProfessionalLinksStep,
  },
  {
    key: "recruitment-history-consent",
    title: "Recruitment History + Consent",
    Component: RecruitmentHistoryConsentStep,
  },
] as const;

interface OnboardingModalContextValue {
  /** spec.md: "Valid 4-digit OTP -> Automatically proceed -> Basic
   * Information" — called by AuthModalProvider on successful register-OTP. */
  start: () => void;
}

const OnboardingModalContext = React.createContext<OnboardingModalContextValue | null>(null);

/**
 * Continues the Create Account flow as modals on Page 1 (spec.md: "This
 * is not a separate website page. It is another step/card/modal within
 * the existing Page 1 Create Account process") through spec.md's full
 * reference chain: Basic Information -> Academic Information -> Current
 * Skills -> Coding Experience -> Projects -> Certifications -> Career /
 * Placement -> Learning / Preparation -> Professional Links + Resume ->
 * Recruitment History + Consent -> Create Account -> Student Dashboard.
 */
export function OnboardingModalProvider({ children }: { children: React.ReactNode }) {
  const navigate = useNavigate();
  const [active, setActive] = React.useState(false);
  const [stepIndex, setStepIndex] = React.useState(0);

  const start = () => {
    setStepIndex(0);
    setActive(true);
  };

  const finish = () => {
    setActive(false);
    navigate("/app");
  };

  const goNext = () => {
    if (stepIndex >= STEPS.length - 1) finish();
    else setStepIndex((i) => i + 1);
  };

  const goBack = () => setStepIndex((i) => Math.max(0, i - 1));

  // UPDATE SDD §7/§9/§11 — LinkedIn-assisted Path B: once the extraction
  // agent has populated the applicable profile fields, the student skips
  // straight to Recruitment History + Consent rather than the remaining
  // manual steps.
  const jumpTo = (key: string) => {
    const idx = STEPS.findIndex((s) => s.key === key);
    if (idx >= 0) setStepIndex(idx);
  };

  const { title, Component } = STEPS[stepIndex];

  return (
    <OnboardingModalContext.Provider value={{ start }}>
      {children}
      <Modal
        open={active}
        onOpenChange={() => {}}
        title={title}
        hideClose
        className="max-w-[640px]"
      >
        <Component onBack={stepIndex > 0 ? goBack : undefined} onContinue={goNext} onJumpTo={jumpTo} />
      </Modal>
    </OnboardingModalContext.Provider>
  );
}

export function useOnboardingModal() {
  const ctx = React.useContext(OnboardingModalContext);
  if (!ctx) throw new Error("useOnboardingModal must be used within OnboardingModalProvider");
  return ctx;
}

export interface OnboardingStepProps {
  onBack?: () => void;
  onContinue: () => void;
  /** Jumps directly to the step with this key — used only by
   * BasicInfoStep's LinkedIn-assisted path (see jumpTo above). */
  onJumpTo?: (key: string) => void;
}
