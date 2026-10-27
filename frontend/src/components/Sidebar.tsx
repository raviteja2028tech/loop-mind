import * as React from "react";
import { NavLink } from "react-router-dom";
import { cn } from "@/lib/cn";

export interface SidebarItem {
  label: string;
  to: string;
}

export interface SidebarSection {
  label?: string;
  items: SidebarItem[];
}

/** Sidebar system — spec.md §12. Used by portal pages that have one; the
 * public landing page renders the Shell without a sidebar entirely. */
export function Sidebar({ sections }: { sections: SidebarSection[] }) {
  return (
    <aside className="lm-sidebar">
      {sections.map((section, i) => (
        <React.Fragment key={section.label ?? i}>
          {section.label ? <div className="lm-sidebar__label">{section.label}</div> : null}
          {section.items.map((item) => (
            <NavLink
              key={item.to}
              to={item.to}
              className={({ isActive }) => cn("lm-sidebar__item", isActive && "is-active")}
            >
              {item.label}
            </NavLink>
          ))}
        </React.Fragment>
      ))}
    </aside>
  );
}
