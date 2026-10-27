import * as Dialog from "@radix-ui/react-dialog";
import { X } from "lucide-react";
import * as React from "react";
import { cn } from "@/lib/cn";

/**
 * Shared modal/card foundation — spec.md §23 + Page 1 SDD "Same Modal
 * System" requirement: Help, Login, Enter OTP, Create Account, Terms,
 * Privacy, Membership Plans etc. must all share this exact mechanism
 * (scrim, centering, border, radius, raised surface, close behavior).
 *
 * Closes only through its explicit close control per phase.md §4 — no
 * backdrop-click dismissal unless a spec explicitly defines one.
 */
export function Modal({
  open,
  onOpenChange,
  title,
  children,
  closeOnOverlayClick = false,
  hideClose = false,
  className,
}: {
  open: boolean;
  onOpenChange: (open: boolean) => void;
  title?: string;
  children: React.ReactNode;
  closeOnOverlayClick?: boolean;
  /** Omit the close (X) control — used for mandatory sequential flows
   * (e.g. the onboarding wizard) where spec.md defines no exit affordance,
   * only Back/Continue. */
  hideClose?: boolean;
  className?: string;
}) {
  return (
    <Dialog.Root open={open} onOpenChange={onOpenChange}>
      <Dialog.Portal>
        <Dialog.Overlay
          className="lm-scrim"
          onClick={(e) => {
            if (!closeOnOverlayClick) e.preventDefault();
          }}
        />
        <Dialog.Content
          onPointerDownOutside={(e) => {
            if (!closeOnOverlayClick) e.preventDefault();
          }}
          onEscapeKeyDown={(e) => {
            if (!closeOnOverlayClick) e.preventDefault();
          }}
          className={cn(
            "lm-modal fixed top-1/2 left-1/2 z-[70] -translate-x-1/2 -translate-y-1/2",
            className,
          )}
        >
          <div className="mb-3 flex items-center justify-between gap-4">
            {title ? (
              <Dialog.Title asChild>
                <h3>{title}</h3>
              </Dialog.Title>
            ) : (
              <span />
            )}
            {!hideClose && (
              <Dialog.Close asChild>
                <button type="button" aria-label="Close" className="lm-nav-link !p-1.5">
                  <X className="size-4" />
                </button>
              </Dialog.Close>
            )}
          </div>
          {children}
        </Dialog.Content>
      </Dialog.Portal>
    </Dialog.Root>
  );
}
