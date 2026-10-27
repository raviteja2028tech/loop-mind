import * as ProgressPrimitive from "@radix-ui/react-progress";
import { cn } from "@/lib/cn";

/** Progress indicator — spec.md §22. */
export function Progress({ value, className }: { value: number; className?: string }) {
  return (
    <ProgressPrimitive.Root value={value} className={cn("lm-progress-track", className)}>
      <ProgressPrimitive.Indicator
        className="lm-progress-fill"
        style={{ width: `${Math.max(0, Math.min(100, value))}%` }}
      />
    </ProgressPrimitive.Root>
  );
}
