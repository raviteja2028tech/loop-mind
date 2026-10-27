import { type VariantProps, cva } from "class-variance-authority";
import * as React from "react";
import { cn } from "@/lib/cn";

/** Badge / pill system — spec.md §18. */
export const badgeVariants = cva("lm-badge", {
  variants: {
    variant: {
      ok: "lm-badge--ok",
      hold: "lm-badge--hold",
      rejected: "lm-badge--rejected",
      neutral: "lm-badge--neutral",
    },
  },
  defaultVariants: {
    variant: "neutral",
  },
});

export interface BadgeProps
  extends React.HTMLAttributes<HTMLSpanElement>, VariantProps<typeof badgeVariants> {}

export function Badge({ className, variant, ...props }: BadgeProps) {
  return <span className={cn(badgeVariants({ variant }), className)} {...props} />;
}
