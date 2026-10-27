import * as React from "react";
import { cn } from "@/lib/cn";

/**
 * 4-digit segmented OTP input — spec.md Enter OTP card: "_ _ _ _". Used by
 * both the Login and Create-Account OTP screens (phase.md Phase 03).
 */
export function OtpInput({
  value,
  onChange,
  invalid,
  autoFocus,
}: {
  value: string;
  onChange: (value: string) => void;
  invalid?: boolean;
  autoFocus?: boolean;
}) {
  const refs = React.useRef<(HTMLInputElement | null)[]>([]);
  const digits = React.useMemo(() => Array.from({ length: 4 }, (_, i) => value[i] ?? ""), [value]);

  const setDigit = (index: number, digit: string) => {
    const next = digits.slice();
    next[index] = digit;
    onChange(next.join(""));
  };

  return (
    <div className="flex justify-center gap-3" role="group" aria-label="Enter OTP">
      {digits.map((digit, index) => (
        <input
          key={index}
          ref={(el) => {
            refs.current[index] = el;
          }}
          autoFocus={autoFocus && index === 0}
          inputMode="numeric"
          maxLength={1}
          value={digit}
          aria-invalid={invalid || undefined}
          className={cn(
            "lm-input h-12 w-12 text-center text-lg",
            invalid && "border-[var(--danger)]",
          )}
          onChange={(e) => {
            const char = e.target.value.replace(/\D/g, "").slice(-1);
            setDigit(index, char);
            if (char && index < 3) refs.current[index + 1]?.focus();
          }}
          onKeyDown={(e) => {
            if (e.key === "Backspace" && !digits[index] && index > 0) {
              refs.current[index - 1]?.focus();
            }
          }}
          onPaste={(e) => {
            const pasted = e.clipboardData.getData("text").replace(/\D/g, "").slice(0, 4);
            if (pasted.length > 1) {
              e.preventDefault();
              onChange(pasted.padEnd(4, "").slice(0, 4));
              refs.current[Math.min(pasted.length, 3)]?.focus();
            }
          }}
        />
      ))}
    </div>
  );
}
