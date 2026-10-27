import * as React from "react";
import { Button } from "@/components/Button";
import { Modal } from "@/components/Modal";

type InfoModal = "help" | "terms" | "privacy" | "membership" | null;

interface InfoModalsContextValue {
  openHelp: () => void;
  openTerms: () => void;
  openPrivacy: () => void;
  openMembership: () => void;
}

const InfoModalsContext = React.createContext<InfoModalsContextValue | null>(null);

/**
 * Shared Help / Terms of Use / Privacy Policy / Membership Plans modals.
 *
 * spec.md Page 1 SDD: "Navbar Help and Footer Help open the same centered
 * Help card... Do not duplicate the Help implementations." The same
 * requirement carries into every later Student Portal page via the
 * "GLOBAL STUDENT PORTAL FOOTER" update, so this lives once at the app
 * root rather than being rebuilt per page.
 *
 * All four modals use temporary placeholder content — spec.md explicitly
 * permits this ("the user explicitly allows temporary content to be
 * generated") and explicitly marks it as non-final legal/product copy.
 */
export function InfoModalsProvider({ children }: { children: React.ReactNode }) {
  const [open, setOpen] = React.useState<InfoModal>(null);
  const close = () => setOpen(null);

  const value = React.useMemo<InfoModalsContextValue>(
    () => ({
      openHelp: () => setOpen("help"),
      openTerms: () => setOpen("terms"),
      openPrivacy: () => setOpen("privacy"),
      openMembership: () => setOpen("membership"),
    }),
    [],
  );

  return (
    <InfoModalsContext.Provider value={value}>
      {children}

      <Modal open={open === "help"} onOpenChange={(o) => !o && close()} title="Help">
        <div className="space-y-3 text-sm text-[var(--text-soft)]">
          <p>Need help using LOOP-MIND?</p>
          <p>Explore Placement Readiness to understand what you need to improve before applying.</p>
          <p>Use Read Job Applications to discover suitable opportunities.</p>
          <p>AI Recruitment helps recruiters screen, match, shortlist and evaluate candidates.</p>
          <p>For account-related help, use Login.</p>
        </div>
      </Modal>

      <Modal open={open === "terms"} onOpenChange={(o) => !o && close()} title="Terms of Use">
        <div className="space-y-3 text-sm text-[var(--text-soft)]">
          <p>
            LOOP-MIND provides tools and services intended to help students prepare for
            opportunities and support recruiters through AI-assisted recruitment workflows.
          </p>
          <p>
            Users are responsible for the information they provide and how they use the platform.
          </p>
          <p className="text-xs text-[var(--text-mute)]">
            This is temporary implementation content only and should not be treated as the final
            legal policy.
          </p>
        </div>
        <div className="mt-5 flex justify-end">
          <Button variant="ghost" onClick={close}>
            Close
          </Button>
        </div>
      </Modal>

      <Modal open={open === "privacy"} onOpenChange={(o) => !o && close()} title="Privacy Policy">
        <div className="space-y-3 text-sm text-[var(--text-soft)]">
          <p>
            LOOP-MIND may process information required to provide student, recruitment and platform
            functionality.
          </p>
          <p>
            Information should be handled according to the platform&apos;s applicable privacy
            practices.
          </p>
          <p className="text-xs text-[var(--text-mute)]">
            This is temporary placeholder content and not a final legal policy.
          </p>
        </div>
        <div className="mt-5 flex justify-end">
          <Button variant="ghost" onClick={close}>
            Close
          </Button>
        </div>
      </Modal>

      <Modal
        open={open === "membership"}
        onOpenChange={(o) => !o && close()}
        title="Membership Plans"
      >
        <div className="space-y-3 text-sm text-[var(--text-soft)]">
          <p>LOOP-MIND membership options will be presented here.</p>
          <p>
            Membership and payment functionality will be implemented later as specified by the
            project requirements.
          </p>
        </div>
        <div className="mt-5 flex justify-end">
          <Button variant="ghost" onClick={close}>
            Close
          </Button>
        </div>
      </Modal>
    </InfoModalsContext.Provider>
  );
}

export function useInfoModals() {
  const ctx = React.useContext(InfoModalsContext);
  if (!ctx) throw new Error("useInfoModals must be used within InfoModalsProvider");
  return ctx;
}
