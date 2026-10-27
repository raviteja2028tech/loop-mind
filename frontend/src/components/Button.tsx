import { Slot } from "@radix-ui/react-slot";
import { type VariantProps, cva } from "class-variance-authority";
import * as React from "react";
import { cn } from "@/lib/cn";

/** Button system — spec.md §17. Only these three variants exist; do not
 * introduce a new button color system. */
export const buttonVariants = cva("lm-btn", {
  variants: {
    variant: {
      primary: "lm-btn--primary",
      ghost: "lm-btn--ghost",
      danger: "lm-btn--danger",
    },
  },
  defaultVariants: {
    variant: "primary",
  },
});

export interface ButtonProps
  extends React.ButtonHTMLAttributes<HTMLButtonElement>, VariantProps<typeof buttonVariants> {
  asChild?: boolean;
}

export const Button = React.forwardRef<HTMLButtonElement, ButtonProps>(
  ({ className, variant, disabled, asChild, ...props }, ref) => {
    const Comp = asChild ? Slot : "button";
    return (
      <Comp
        ref={ref}
        className={cn(buttonVariants({ variant }), className)}
        disabled={disabled}
        aria-disabled={disabled || undefined}
        {...props}
      />
    );
  },
);
Button.displayName = "Button";
