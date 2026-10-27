import * as React from "react";
import { cn } from "@/lib/cn";

/** Global application shell — spec.md §8-9 (fixed grid, 224px sidebar,
 * collapses to nav/main/foot at ≤880px). */
export function Shell({
  navbar,
  sidebar,
  footer,
  children,
  className,
}: {
  navbar: React.ReactNode;
  sidebar?: React.ReactNode;
  footer: React.ReactNode;
  children: React.ReactNode;
  className?: string;
}) {
  return (
    <div className={cn("lm-shell", !sidebar && "lm-shell--no-sidebar", className)}>
      <div className="lm-shell__nav">{navbar}</div>
      {sidebar ? <div className="lm-shell__side">{sidebar}</div> : null}
      <div className="lm-shell__main">
        <main className="lm-main">{children}</main>
      </div>
      <div className="lm-shell__foot">{footer}</div>
    </div>
  );
}
