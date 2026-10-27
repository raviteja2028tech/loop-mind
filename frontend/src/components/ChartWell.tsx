import * as React from "react";
import { Tooltip } from "recharts";
import { cn } from "@/lib/cn";

/** Chart well container — spec.md §25. Series colors must only ever be
 * --accent / --accent-deep / --warn (no rainbow palette). */
export const CHART_SERIES = ["var(--accent)", "var(--accent-deep)", "var(--warn)"] as const;

export function ChartWell({
  className,
  children,
}: {
  className?: string;
  children: React.ReactNode;
}) {
  return <div className={cn("lm-chart-well", className)}>{children}</div>;
}

export function ChartTooltip(props: React.ComponentProps<typeof Tooltip>) {
  return (
    <Tooltip
      {...props}
      contentStyle={{
        background: "var(--raised)",
        border: "1px solid var(--border-hi)",
        borderRadius: 8,
        color: "var(--text)",
        fontSize: 12.5,
      }}
    />
  );
}
