import { useNavigate } from "react-router-dom";
import type { NavItem } from "@/components";
import { useAuth } from "@/lib/auth";

/**
 * Logout nav item SDD: "Add Logout as the last option in the [Student /
 * Recruiter] Portal navigation... available on every [portal] page...
 * same existing navigation layout, styling, spacing, typography... Do
 * not modify, remove, rearrange, or redesign any existing navigation
 * options." These hooks append a single shared Logout item after each
 * portal's existing, unchanged nav items, rather than each page
 * reimplementing it — one source of truth, zero drift risk.
 *
 * Logout itself just clears the single stored session token (lib/auth.tsx)
 * and returns to the landing page — since a browser only ever holds one
 * token at a time, a student's logout can never touch a recruiter session
 * or vice versa; there is nothing shared between them to cross-contaminate.
 */
const STUDENT_NAV_ITEMS: NavItem[] = [
  { label: "Dashboard", to: "/app" },
  { label: "Skill Gap", to: "/app/skill-gap" },
  { label: "Preparation Plan", to: "/app/preparation-plan" },
  { label: "Jobs", to: "/app/jobs" },
  { label: "My Profile", to: "/app/profile" },
];

const RECRUITER_NAV_ITEMS: NavItem[] = [
  { label: "Dashboard", to: "/recruiter" },
  { label: "Jobs", to: "/recruiter/jobs" },
  { label: "Candidates", to: "/recruiter/candidates" },
  { label: "Interviews", to: "/recruiter/interviews" },
];

function useLogoutNavItem(): NavItem {
  const { logout } = useAuth();
  const navigate = useNavigate();
  return {
    label: "Logout",
    onClick: () => {
      logout();
      navigate("/", { replace: true });
    },
  };
}

export function useStudentNavItems(): NavItem[] {
  return [...STUDENT_NAV_ITEMS, useLogoutNavItem()];
}

export function useRecruiterNavItems(): NavItem[] {
  return [...RECRUITER_NAV_ITEMS, useLogoutNavItem()];
}
