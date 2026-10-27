import { Footer } from "@/components/Footer";
import { useInfoModals } from "@/components/InfoModalsProvider";

/**
 * Recruiter Portal footer — spec.md Recruiter Dashboard §16: "Terms of
 * Use / Privacy Policy / Help" only (no Membership Plans, which is a
 * Student Portal concept). Shares the same modal system as the Student
 * Portal's GlobalFooter.
 */
export function RecruiterFooter() {
  const { openTerms, openPrivacy, openHelp } = useInfoModals();

  return (
    <Footer
      links={[
        { label: "Terms of Use", onClick: openTerms },
        { label: "Privacy Policy", onClick: openPrivacy },
        { label: "Help", onClick: openHelp },
      ]}
      copyright="LOOP-MIND ©"
    />
  );
}
