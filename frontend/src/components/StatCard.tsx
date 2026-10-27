import { cn } from "@/lib/cn";

/** Statistics card — spec.md §16. */
export interface StatCardProps {
  label: string;
  value: React.ReactNode;
  accent?: boolean;
  className?: string;
}

export function StatCard({ label, value, accent, className }: StatCardProps) {
  return (
    <div className={cn("lm-stat", className)}>
      <span className="lm-stat__label">{label}</span>
      <span className={cn("lm-stat__value", accent && "lm-stat__value--accent")}>{value}</span>
    </div>
  );
}
