import * as React from "react";
import { Button } from "@/components/Button";
import { Field, Input } from "@/components/Input";
import { PhotoPicker } from "@/components/PhotoPicker";
import { SearchableSelect } from "@/components/Select";
import { ErrorState } from "@/components/States";
import {
  ApiError,
  extractDraftLinkedIn,
  getDraft,
  getLinkedInOAuthConfig,
  putDraftBasicInfo,
  putDraftLinkedinUrl,
  submitLinkedInOAuthCode,
  uploadDraftPhoto,
} from "@/lib/api";
import {
  cityOptionsFor,
  COUNTRY_OPTIONS,
  GENDER_OPTIONS,
  stateOptionsFor,
} from "@/lib/reference-data";
import type { OnboardingStepProps } from "@/website/onboarding/OnboardingModalProvider";

/** spec.md "Create Account -> Basic Information". No Back button here —
 * it's the first onboarding step, reached only via a valid OTP.
 *
 * Student Create Account UPDATE SDD: this step (and every other
 * onboarding step) now saves into a temporary registration draft
 * (backend/services/registration_service.py) rather than a real student
 * account — no permanent account exists until Create Account succeeds on
 * the final Consent step (see RecruitmentHistoryConsentStep.tsx). */
export default function BasicInfoStep({ onContinue, onJumpTo }: OnboardingStepProps) {
  const [fullName, setFullName] = React.useState("");
  const [day, setDay] = React.useState("");
  const [month, setMonth] = React.useState("");
  const [year, setYear] = React.useState("");
  const [gender, setGender] = React.useState("");
  const [email, setEmail] = React.useState("");
  const [country, setCountry] = React.useState<string | null>(null);
  const [state, setState] = React.useState<string | null>(null);
  const [city, setCity] = React.useState<string | null>(null);
  const [photoName, setPhotoName] = React.useState<string | null>(null);
  const [photoUploading, setPhotoUploading] = React.useState(false);
  const [saving, setSaving] = React.useState(false);
  const [error, setError] = React.useState<string | null>(null);

  // Student Create Account UPDATE SDD §5-9 + LinkedIn Auto-Extraction
  // UPDATE SDD: LinkedIn is URL-only — no pasted text, and extraction
  // starts automatically as soon as a plausible URL is entered (no
  // button to click). `linkedinDone` tracks whether extraction actually
  // found something usable, so Continue can take the LinkedIn path (skip
  // straight to Recruitment History + Consent) instead of the manual
  // path — never a partial/empty "success".
  const [linkedinUrl, setLinkedinUrl] = React.useState("");
  const [linkedinExtracting, setLinkedinExtracting] = React.useState(false);
  const [linkedinDone, setLinkedinDone] = React.useState(false);
  const [linkedinAttempted, setLinkedinAttempted] = React.useState<string | null>(null);
  const [linkedinSummary, setLinkedinSummary] = React.useState<string | null>(null);
  const [linkedinError, setLinkedinError] = React.useState<string | null>(null);

  // LinkedIn Profile Extraction UPDATE SDD: a separate, real "Sign In
  // with LinkedIn" (OpenID Connect) path for identity fields only
  // (name/email/photo) — genuinely authorized, never a scrape. Runs
  // alongside the best-effort extraction above (unchanged, still handles
  // skills/certifications/projects), not instead of it. `oauthConfigured
  // === false` means no real LinkedIn Developer app is set up for this
  // deployment yet — the button reports that honestly rather than
  // pretending to work.
  const [oauthConfigured, setOauthConfigured] = React.useState<boolean | null>(null);
  const [oauthAuthUrl, setOauthAuthUrl] = React.useState<string | null>(null);
  const [oauthConnecting, setOauthConnecting] = React.useState(false);
  const [oauthDone, setOauthDone] = React.useState(false);
  const [oauthError, setOauthError] = React.useState<string | null>(null);

  React.useEffect(() => {
    getDraft().then((draft) => {
      const info = draft.basic_info;
      if (info) {
        setFullName(info.full_name);
        const [y, m, d] = info.date_of_birth.split("-");
        setYear(y);
        setMonth(m);
        setDay(d);
        setGender(info.gender);
        setEmail(info.email);
        setCountry(info.country);
        setState(info.state);
        setCity(info.city);
      }
      if (draft.profile_photo_path) setPhotoName("Profile photo uploaded");
      if (draft.linkedin_url) setLinkedinUrl(draft.linkedin_url);
    });
    getLinkedInOAuthConfig().then((config) => {
      setOauthConfigured(config.configured);
      setOauthAuthUrl(config.authorization_url);
    });
  }, []);

  // handleOAuthCode reads fullName/email at call time via this ref so the
  // message listener below never needs to re-subscribe when they change
  // (it only ever runs once, for the one popup round-trip).
  const identityFieldsRef = React.useRef({ fullName, email });
  React.useEffect(() => {
    identityFieldsRef.current = { fullName, email };
  }, [fullName, email]);

  const handleOAuthCode = React.useCallback(
    async (code: string | null | undefined, oauthDenied?: string) => {
      setOauthConnecting(false);
      if (!code) {
        setOauthError(
          oauthDenied
            ? "LinkedIn sign-in was cancelled or access was denied."
            : "LinkedIn sign-in did not complete. You can try again or continue manually."
        );
        return;
      }
      try {
        const identity = await submitLinkedInOAuthCode(code);
        if (!identity.name && !identity.email) {
          setOauthError(
            "LinkedIn did not return any usable profile information. You can continue manually."
          );
          return;
        }
        // Only pre-fills fields the student hasn't already typed
        // something into — LinkedIn's identity is a starting point,
        // never a silent overwrite of what the student already entered.
        const current = identityFieldsRef.current;
        if (identity.name && !current.fullName.trim()) setFullName(identity.name);
        if (identity.email && !current.email.trim()) setEmail(identity.email);
        if (identity.has_photo) setPhotoName("Profile photo uploaded");
        setOauthDone(true);
        setOauthError(null);
      } catch (err) {
        setOauthError(
          err instanceof ApiError
            ? String(err.body)
            : "LinkedIn extraction failed. We could not retrieve profile information through " +
                "the authorized LinkedIn connection. You can continue creating your profile " +
                "manually."
        );
      }
    },
    []
  );

  // Popup-based OAuth: LinkedIn redirects the popup window to our own
  // /linkedin/oauth-callback page, which just posts {code} back here and
  // closes itself — the actual token exchange happens server-side in
  // handleOAuthCode above, so the LinkedIn client secret never reaches
  // the browser.
  React.useEffect(() => {
    function handleMessage(event: MessageEvent) {
      if (event.origin !== window.location.origin) return;
      if (event.data?.type !== "linkedin-oauth") return;
      void handleOAuthCode(event.data.code, event.data.error);
    }
    window.addEventListener("message", handleMessage);
    return () => window.removeEventListener("message", handleMessage);
  }, [handleOAuthCode]);

  function handleConnectLinkedIn() {
    if (!oauthAuthUrl) return;
    setOauthConnecting(true);
    setOauthError(null);
    const popup = window.open(oauthAuthUrl, "linkedin-oauth", "width=600,height=700");
    if (!popup) {
      setOauthConnecting(false);
      setOauthError("Could not open the LinkedIn sign-in window. Check your popup blocker.");
    }
  }

  const dateValid = /^\d{4}$/.test(year) && /^\d{1,2}$/.test(month) && /^\d{1,2}$/.test(day);
  const canContinue =
    fullName.trim() !== "" &&
    dateValid &&
    gender !== "" &&
    /^[^@\s]+@[^@\s]+\.[^@\s]+$/.test(email) &&
    country &&
    state &&
    city;

  // The registration draft already exists (created at OTP verification),
  // so — unlike a real student account — there's no chicken-and-egg
  // ordering problem here: the photo can upload immediately on selection.
  const handlePhoto = async (files: File[]) => {
    const file = files[0];
    if (!file) return;
    setPhotoUploading(true);
    setError(null);
    try {
      await uploadDraftPhoto(file);
      setPhotoName(file.name);
    } catch {
      setError("Could not upload photo. Try again.");
    } finally {
      setPhotoUploading(false);
    }
  };

  // LinkedIn Auto-Extraction UPDATE SDD §2/§6: extraction starts
  // immediately once a plausible LinkedIn URL is entered — no button to
  // click. §8 "No Partial LinkedIn Success": only a genuinely useful
  // extraction (at least one skill/certification/project actually found)
  // counts as success; anything else — a technical failure, or a
  // technically-successful call that found nothing — falls back to the
  // normal manual flow, and the URL is cleared so the student isn't left
  // looking at a shortcut that didn't work (§7).
  const handleLinkedInBlur = async () => {
    const url = linkedinUrl.trim();
    if (!url || linkedinDone || linkedinExtracting || linkedinAttempted === url) return;
    if (!/linkedin\.com/i.test(url)) return;

    setLinkedinAttempted(url);
    setLinkedinExtracting(true);
    setLinkedinError(null);
    setLinkedinSummary(null);
    try {
      await putDraftLinkedinUrl(url);
      const result = await extractDraftLinkedIn();
      const found = result.skills_added + result.certifications_added + result.projects_added;
      if (found === 0) {
        await putDraftLinkedinUrl("");
        setLinkedinUrl("");
        setLinkedinAttempted(null);
        setLinkedinError(
          "LinkedIn extraction failed — it didn't return any profile information to import. " +
            "You can continue filling in your profile manually below."
        );
        return;
      }
      const parts = [
        result.skills_added && `${result.skills_added} skill(s)`,
        result.certifications_added && `${result.certifications_added} certification(s)`,
        result.projects_added && `${result.projects_added} project(s)`,
      ].filter(Boolean);
      setLinkedinSummary(`Imported from LinkedIn: ${parts.join(", ")}.`);
      setLinkedinDone(true);
    } catch (err) {
      await putDraftLinkedinUrl("").catch(() => {});
      setLinkedinUrl("");
      setLinkedinAttempted(null);
      setLinkedinError(
        err instanceof ApiError
          ? String(err.body)
          : "LinkedIn extraction failed. You can continue filling in your profile manually below."
      );
    } finally {
      setLinkedinExtracting(false);
    }
  };

  const handleContinue = async () => {
    if (!canContinue || photoUploading) return;
    setSaving(true);
    setError(null);
    try {
      await putDraftBasicInfo({
        full_name: fullName,
        date_of_birth: `${year}-${month.padStart(2, "0")}-${day.padStart(2, "0")}`,
        gender,
        email,
        country: country!,
        state: state!,
        city: city!,
      });
      // LinkedIn path: applicable fields already populated, so the
      // remaining manual steps are skipped — straight to Recruitment
      // History + Consent, matching spec's own final gate (Create
      // Account stays inactive until consent is given there).
      if (linkedinDone && onJumpTo) {
        onJumpTo("recruitment-history-consent");
      } else {
        onContinue();
      }
    } catch (err) {
      setError(err instanceof ApiError ? String(err.body) : "Could not save. Try again.");
    } finally {
      setSaving(false);
    }
  };

  return (
    <div className="flex flex-col gap-4">
      <Field label="Full Name">
        <Input value={fullName} onChange={(e) => setFullName(e.target.value)} />
      </Field>

      <div>
        <label className="lm-label">Date of birth</label>
        <div className="grid grid-cols-3 gap-3">
          <Input
            placeholder="DD"
            inputMode="numeric"
            maxLength={2}
            value={day}
            onChange={(e) => setDay(e.target.value.replace(/\D/g, ""))}
          />
          <Input
            placeholder="MM"
            inputMode="numeric"
            maxLength={2}
            value={month}
            onChange={(e) => setMonth(e.target.value.replace(/\D/g, ""))}
          />
          <Input
            placeholder="YYYY"
            inputMode="numeric"
            maxLength={4}
            value={year}
            onChange={(e) => setYear(e.target.value.replace(/\D/g, ""))}
          />
        </div>
      </div>

      <div>
        <label className="lm-label">Gender</label>
        <div className="flex gap-4">
          {GENDER_OPTIONS.map((g) => (
            <label
              key={g.value}
              className="flex items-center gap-2 text-sm text-[var(--text-soft)]"
            >
              <input
                type="radio"
                name="gender"
                checked={gender === g.value}
                onChange={() => setGender(g.value)}
              />
              {g.label}
            </label>
          ))}
        </div>
      </div>

      <Field label="Profile Photo (optional)">
        <PhotoPicker
          onFiles={handlePhoto}
          trigger={
            <button type="button" className="lm-dropzone w-full text-left">
              {photoUploading
                ? "Uploading…"
                : (photoName ?? "Camera, Photos or Files — up to 1 photo")}
            </button>
          }
        />
      </Field>

      <Field label="Email Address">
        <Input
          type="email"
          placeholder="you@gmail.com"
          value={email}
          onChange={(e) => setEmail(e.target.value)}
        />
      </Field>

      <div className="grid gap-4 sm:grid-cols-3">
        <Field label="Country">
          <SearchableSelect
            options={COUNTRY_OPTIONS}
            value={country}
            onChange={(v) => {
              setCountry(v);
              setState(null);
              setCity(null);
            }}
            placeholder="Country"
          />
        </Field>
        <Field label="State">
          <SearchableSelect
            options={stateOptionsFor(country)}
            value={state}
            onChange={(v) => {
              setState(v);
              setCity(null);
            }}
            placeholder="State"
            disabled={!country}
          />
        </Field>
        <Field label="City">
          <SearchableSelect
            options={cityOptionsFor(country, state)}
            value={city}
            onChange={setCity}
            placeholder="City"
            disabled={!state}
          />
        </Field>
      </div>

      {error && <ErrorState message={error} />}

      <div className="flex flex-col gap-3 border-t border-[var(--border)] pt-4">
        <div>
          <label className="lm-label">LinkedIn Profile (optional)</label>
          <p className="text-sm text-[var(--text-soft)]">
            Provide your LinkedIn profile URL and we'll automatically retrieve and fill in the
            corresponding profile steps instead of you entering them manually.
          </p>
        </div>
        <Input
          placeholder="https://www.linkedin.com/in/your-profile"
          value={linkedinUrl}
          onChange={(e) => setLinkedinUrl(e.target.value)}
          onBlur={handleLinkedInBlur}
          disabled={linkedinDone || linkedinExtracting}
        />
        {linkedinExtracting ? (
          <p className="text-sm text-[var(--text-mute)]">Retrieving your LinkedIn profile…</p>
        ) : null}
        {linkedinError && <ErrorState message={linkedinError} />}
        {linkedinSummary && <p className="text-sm text-[var(--accent)]">{linkedinSummary}</p>}

        <div className="flex flex-col gap-2">
          {oauthConfigured === false ? (
            <p className="text-xs text-[var(--text-mute)]">
              LinkedIn sign-in isn't configured on this deployment yet, so your name/email/photo
              can't be retrieved this way — fill them in below instead.
            </p>
          ) : (
            <>
              <Button
                type="button"
                variant="ghost"
                className="self-start"
                disabled={oauthConfigured !== true || oauthConnecting || oauthDone}
                onClick={handleConnectLinkedIn}
              >
                {oauthDone
                  ? "✓ LinkedIn profile connected"
                  : oauthConnecting
                    ? "Connecting…"
                    : "Connect to LinkedIn"}
              </Button>
              <p className="text-xs text-[var(--text-mute)]">
                Signs you into LinkedIn to securely fill in your name, email, and photo — never
                your password, and never more than LinkedIn actually shares.
              </p>
            </>
          )}
          {oauthError && <ErrorState message={oauthError} />}
        </div>
      </div>

      <Button
        variant="primary"
        disabled={!canContinue || saving || photoUploading}
        onClick={handleContinue}
        className="justify-center"
      >
        Continue
      </Button>
    </div>
  );
}
