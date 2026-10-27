# LOOP-MIND Mobile

React Native + TypeScript + React Navigation client for LOOP-MIND — phase.md Phase 19.

It calls the **exact same backend** as the web app (`../backend`), with no second backend, no duplicated business logic, and no mobile-only product features, per phase.md's critical architecture rule for this phase.

## Run it

```bash
cd mobile
npm install
npm start
```

Then press `a` for an Android emulator, `i` for an iOS simulator, `w` for a web preview, or scan the QR code with the Expo Go app on a physical device.

## Pointing at the backend

The backend must already be running (`uvicorn backend.main:app --reload --port 8010` from the repo root).

- **Web preview / iOS simulator**: the default `http://localhost:8010/api` works as-is.
- **Android emulator**: `localhost` inside the emulator is the emulator itself, not your machine. Set:
  ```bash
  EXPO_PUBLIC_API_BASE_URL=http://10.0.2.2:8010/api npm start
  ```
- **A physical device** (Expo Go): your phone can't reach your computer's `localhost` either. Set it to your machine's LAN IP instead:
  ```bash
  EXPO_PUBLIC_API_BASE_URL=http://<your-lan-ip>:8010/api npm start
  ```

## What's here

- `src/lib/api.ts` — thin REST client mirroring `frontend/src/lib/api.ts`'s types/endpoints for the screens below.
- `src/lib/auth.tsx` — JWT session state (AsyncStorage instead of the web's localStorage), same backend-issued token.
- `src/lib/theme.ts` — the same Graphite Ink color tokens as `frontend/src/styles/agenthire-theme.css`, translated to RN `StyleSheet` values (no CSS in React Native).
- `src/navigation/` — Auth stack (Welcome → OTP) + role-based Student/Recruiter bottom-tab navigators.
- `src/screens/student/` — Dashboard, Skill Gap, Preparation Plan, Jobs (browse/apply/save/My Applications), My Profile (Overview, Skills, Recruitment History).
- `src/screens/recruiter/` — Dashboard, Jobs (read-only list), Candidates (read + Approve).

## Scope decisions (read before assuming something is missing)

- **Create Account is student-only**, same as the web app — recruiter accounts aren't self-service anywhere in this system (web included), so there's no recruiter registration screen to build here either.
- **My Profile** ports Overview, Skills and Recruitment History — the three sections that translate naturally to one scrolling phone screen. The web's other nine sections (Academics, Career & Placement, Learning & Preparation, Interview & Assessment, Professional Links, Consent, Coding Experience, Projects, Certifications) are real data behind `/students/me/*` already and could get their own mobile screens later, but weren't worth squeezing in for this pass.
- **Recruiter mobile scope is read-plus-Approve only.** spec.md never defines a mobile Recruiter Portal reference layout the way it does for every Student Portal page, so phase.md's "recruiter workflows where the mobile scope defines them" has nothing concrete to point at. Building the AI Recruitment Workflow visualization (React Flow has no React Native port), Disapprove-with-reason, Interviews, or Analytics here would be inventing mobile-only product behavior — exactly what this phase's critical rule forbids.
- **Screenshot/screen-capture protection**: phase.md asks to apply this "where the specification defines it." spec.md never actually defines a concrete screenshot-protection requirement anywhere, so nothing was implemented — adding one would be inventing a requirement, not reproducing one.
- This was built and verified via `tsc --noEmit` (clean), `expo-doctor` (17/17 checks pass), and `expo export --platform web` (bundles and serves with no errors) — there's no device/emulator in the environment that built this, so an actual on-device run is the one thing only you can verify.
