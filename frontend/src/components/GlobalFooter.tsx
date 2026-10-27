import { Footer } from "@/components/Footer";
import { useInfoModals } from "@/components/InfoModalsProvider";

/**
 * The global Landing Page + Student Portal footer — spec.md "Dashboard
 * Updates — Footer + Target Company" §1: "The footer must remain exactly
 * the same across every Student Portal page... must be exactly the same
 * as the footer defined for the LOOP-MIND Landing Page." Reused as-is by
 * every later Student Portal page; the Recruiter Portal footer (Terms of
 * Use / Privacy Policy / Help only, no Membership Plans) is a separate,
 * smaller component built in Phase 11.
 */
export function GlobalFooter() {
  const { openTerms, openPrivacy, openMembership, openHelp } = useInfoModals();

  return (
    <Footer
      links={[
        { label: "Terms of Use", onClick: openTerms },
        { label: "Privacy Policy", onClick: openPrivacy },
        { label: "Membership Plans", onClick: openMembership },
        { label: "Help", onClick: openHelp },
      ]}
      copyright="LOOP-MIND ©"
    />
  );
}
