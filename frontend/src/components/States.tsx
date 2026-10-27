import { Loader2 } from "lucide-react";

/** Loading state — used while a route/section awaits API data. */
export function LoadingState({ label = "Loading…" }: { label?: string }) {
  return (
    <div className="flex items-center justify-center gap-2 py-10 text-sm text-[var(--text-mute)]">
      <Loader2 className="size-4 animate-spin" />
      {label}
    </div>
  );
}

/** Error state — used when a request fails; never fabricates data. */
export function ErrorState({
  message = "Something went wrong. Please try again.",
}: {
  message?: string;
}) {
  return (
    <div className="lm-card border-[var(--danger)]/40 text-sm text-[var(--danger)]">{message}</div>
  );
}
