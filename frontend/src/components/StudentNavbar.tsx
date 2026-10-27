import { Navbar } from "@/components/Navbar";
import { useStudentNavItems } from "@/lib/navItems";

/**
 * Shared Student Portal top navigation — UPDATE SDD "Student Portal —
 * Right-Side Navigation Requirement": Dashboard / Skill Gap / Preparation
 * Plan / Jobs / My Profile / Logout, positioned flush to the right side
 * of every Student Portal page's navbar, identical layout/styling on
 * every page. Every Student Portal page renders this instead of
 * separately composing `<Navbar items={useStudentNavItems()}>`, so the
 * item list and alignment can never drift between pages.
 *
 * Scope: Student Portal only — the Recruiter Portal has its own
 * equivalent `RecruiterNavbar` component (see RecruiterNavbar.tsx).
 */
export function StudentNavbar() {
  const items = useStudentNavItems();
  return <Navbar brand="LOOP-MIND" items={items} linksAlign="end" />;
}
