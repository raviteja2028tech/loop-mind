import { X } from "lucide-react";
import * as React from "react";
import { cn } from "@/lib/cn";

/**
 * Free-text multi-value input (type + Enter/comma to add a chip).
 *
 * Used for open-ended list fields (technologies used, tools, skills
 * covered, coding platforms, ...) where spec.md explicitly declines to
 * define a fixed option set ("do not invent a specific fixed list as
 * user-provided") — a constrained dropdown would be less correct than
 * free entry here, not more.
 */
export function TagInput({
  value,
  onChange,
  placeholder,
}: {
  value: string[];
  onChange: (value: string[]) => void;
  placeholder?: string;
}) {
  const [draft, setDraft] = React.useState("");

  const commit = () => {
    const tag = draft.trim();
    if (tag && !value.includes(tag)) onChange([...value, tag]);
    setDraft("");
  };

  return (
    <div className={cn("lm-input flex min-h-[42px] flex-wrap items-center gap-2 py-1.5")}>
      {value.map((tag) => (
        <span
          key={tag}
          className="inline-flex items-center gap-1 rounded-md bg-[var(--surface)] px-2 py-0.5 text-xs text-[var(--text-soft)]"
        >
          {tag}
          <button
            type="button"
            onClick={() => onChange(value.filter((t) => t !== tag))}
            aria-label={`Remove ${tag}`}
          >
            <X className="size-3" />
          </button>
        </span>
      ))}
      <input
        className="min-w-[80px] flex-1 bg-transparent text-[13.5px] outline-none placeholder:text-[var(--text-mute)]"
        placeholder={value.length === 0 ? placeholder : undefined}
        value={draft}
        onChange={(e) => setDraft(e.target.value)}
        onKeyDown={(e) => {
          if (e.key === "Enter" || e.key === ",") {
            e.preventDefault();
            commit();
          } else if (e.key === "Backspace" && draft === "" && value.length > 0) {
            onChange(value.slice(0, -1));
          }
        }}
        onBlur={commit}
      />
    </div>
  );
}
