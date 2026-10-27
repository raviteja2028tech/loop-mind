import * as React from "react";
import { NavLink } from "react-router-dom";
import { cn } from "@/lib/cn";

export interface NavItem {
  label: string;
  /** Omit only for an action item (e.g. Logout) that has no destination
   * route — provide `onClick` instead. */
  to?: string;
  /** Renders as inert text instead of a link — for reference nav items
   * whose destination page is a later, not-yet-built phase. */
  disabled?: boolean;
  /** Renders this item as a button that runs an action instead of
   * navigating — e.g. the Logout nav item, which ends the session rather
   * than linking to a route. Takes precedence over `to`. */
  onClick?: () => void;
}

/** Global navbar — spec.md §10-11. Sticky, sits on --bg, bottom border,
 * z-index 40. Shared by every portal; only the brand suffix and nav items
 * differ per portal. */
export function Navbar({
  brand,
  brandTo = "/",
  items = [],
  right,
  linksAlign = "start",
}: {
  brand: React.ReactNode;
  brandTo?: string;
  items?: NavItem[];
  right?: React.ReactNode;
  /** "end" pushes `items` flush to the right edge of the navbar — used
   * by the Student Portal's shared navigation (see StudentNavbar.tsx).
   * Defaults to "start" (unchanged existing behavior) everywhere else,
   * including the Recruiter Portal. */
  linksAlign?: "start" | "end";
}) {
  return (
    <nav className="lm-navbar">
      <NavLink to={brandTo} className="lm-navbar__brand">
        <span className="lm-navbar__mark" aria-hidden />
        {brand}
      </NavLink>
      {items.length > 0 ? (
        <div className={cn("lm-navbar__links", linksAlign === "end" && "lm-navbar__links--end")}>
          {items.map((item) =>
            item.disabled ? (
              <span
                key={item.label}
                className="lm-nav-link cursor-default opacity-50"
                aria-disabled="true"
              >
                {item.label}
              </span>
            ) : item.onClick ? (
              <button key={item.label} type="button" className="lm-nav-link" onClick={item.onClick}>
                {item.label}
              </button>
            ) : (
              <NavLink
                key={item.to}
                to={item.to ?? "#"}
                className={({ isActive }) => cn("lm-nav-link", isActive && "is-active")}
              >
                {item.label}
              </NavLink>
            ),
          )}
        </div>
      ) : null}
      <div className="flex items-center gap-2">{right}</div>
    </nav>
  );
}
