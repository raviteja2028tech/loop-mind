import * as React from "react";
import { cn } from "@/lib/cn";

/** Standard card system — spec.md §15. */
export function Card({
  className,
  flat,
  ...props
}: React.HTMLAttributes<HTMLDivElement> & { flat?: boolean }) {
  return <div className={cn("lm-card", flat && "lm-card--flat", className)} {...props} />;
}

export function CardGrid({ className, ...props }: React.HTMLAttributes<HTMLDivElement>) {
  return <div className={cn("lm-card-grid", className)} {...props} />;
}
