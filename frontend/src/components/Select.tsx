import * as Popover from "@radix-ui/react-popover";
import { Check, ChevronDown } from "lucide-react";
import * as React from "react";
import {
  Command,
  CommandEmpty,
  CommandGroup,
  CommandInput,
  CommandItem,
  CommandList,
} from "@/components/Command";
import { cn } from "@/lib/cn";

export interface SelectOption {
  value: string;
  label: string;
}

/**
 * Searchable dropdown — spec.md §19/global dropdown rule: "Dropdowns should
 * be searchable wherever the number of possible options makes searching
 * useful." Backs Country/State/City, Company, Role, Skill Category, etc.
 */
export function SearchableSelect({
  options,
  value,
  onChange,
  placeholder = "Select…",
  searchPlaceholder = "Search…",
  emptyText = "No matches.",
  disabled,
  className,
}: {
  options: SelectOption[];
  value: string | null;
  onChange: (value: string) => void;
  placeholder?: string;
  searchPlaceholder?: string;
  emptyText?: string;
  disabled?: boolean;
  className?: string;
}) {
  const [open, setOpen] = React.useState(false);
  const selected = options.find((o) => o.value === value);

  return (
    <Popover.Root open={open} onOpenChange={setOpen}>
      <Popover.Trigger asChild>
        <button
          type="button"
          disabled={disabled}
          aria-disabled={disabled || undefined}
          className={cn(
            "lm-select flex items-center justify-between gap-2 text-left",
            !selected && "text-[var(--text-mute)]",
            className,
          )}
        >
          <span className="truncate">{selected ? selected.label : placeholder}</span>
          <ChevronDown className="size-4 shrink-0 opacity-60" />
        </button>
      </Popover.Trigger>
      <Popover.Portal>
        <Popover.Content
          align="start"
          sideOffset={6}
          className="lm-popover z-[70] w-[min(320px,90vw)]"
        >
          <Command>
            <CommandInput placeholder={searchPlaceholder} />
            <CommandList>
              <CommandEmpty>{emptyText}</CommandEmpty>
              <CommandGroup>
                {options.map((option) => (
                  <CommandItem
                    key={option.value}
                    value={option.label}
                    onSelect={() => {
                      onChange(option.value);
                      setOpen(false);
                    }}
                  >
                    <Check
                      className={cn("size-4", option.value === value ? "opacity-100" : "opacity-0")}
                    />
                    {option.label}
                  </CommandItem>
                ))}
              </CommandGroup>
            </CommandList>
          </Command>
        </Popover.Content>
      </Popover.Portal>
    </Popover.Root>
  );
}

/** Plain dropdown for small fixed option sets (e.g. Gender) — spec.md §5
 * "Non-searchable does NOT mean empty" — still must be fully populated. */
export const SimpleSelect = React.forwardRef<
  HTMLSelectElement,
  React.SelectHTMLAttributes<HTMLSelectElement> & { options: SelectOption[]; placeholder?: string }
>(({ className, options, placeholder, ...props }, ref) => (
  <select ref={ref} className={cn("lm-select", className)} {...props}>
    {placeholder ? (
      <option value="" disabled>
        {placeholder}
      </option>
    ) : null}
    {options.map((o) => (
      <option key={o.value} value={o.value}>
        {o.label}
      </option>
    ))}
  </select>
));
SimpleSelect.displayName = "SimpleSelect";
