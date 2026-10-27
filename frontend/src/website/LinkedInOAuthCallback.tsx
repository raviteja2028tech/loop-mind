import * as React from "react";

/** LinkedIn Profile Extraction UPDATE SDD: the popup window LinkedIn's
 * OAuth authorize screen redirects back to after the student signs in
 * and approves access. This page does nothing but hand the `code` (or
 * `error`) back to the window that opened it via `postMessage`, then
 * close itself — the actual token exchange happens server-side, in the
 * opener's own authenticated call to
 * `/registration/draft/linkedin/oauth-callback`, so the client secret
 * never needs to reach the browser at all. */
export default function LinkedInOAuthCallback() {
  React.useEffect(() => {
    const params = new URLSearchParams(window.location.search);
    const code = params.get("code");
    const error = params.get("error");
    if (window.opener) {
      window.opener.postMessage(
        { type: "linkedin-oauth", code, error: error ?? undefined },
        window.location.origin,
      );
    }
    window.close();
  }, []);

  return (
    <div className="flex min-h-screen items-center justify-center p-6 text-center text-sm text-[var(--text-soft)]">
      Completing LinkedIn sign-in… you can close this window if it doesn't close automatically.
    </div>
  );
}
