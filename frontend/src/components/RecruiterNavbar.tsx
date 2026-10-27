import { Navbar } from "@/components/Navbar";
import { useRecruiterNavItems } from "@/lib/navItems";

/**
 * Shared Recruiter Portal top navigation — Recruiter Portal UPDATE SDD
 * §1 "Navigation": Dashboard / Job Management / Candidates / Interviews /
 * Analytics / Logout, positioned flush to the right side of every
 * Recruiter Portal page's navbar, mirroring the Student Portal's own
 * `StudentNavbar`. Every Recruiter Portal page renders this instead of
 * separately composing `<Navbar items={useRecruiterNavItems()}>`, so the
 * item list and alignment can never drift between pages.
 */
export function RecruiterNavbar() {
  const items = useRecruiterNavItems();
  return <Navbar brand="LOOP-MIND | Recruiter Portal" items={items} linksAlign="end" />;
}
