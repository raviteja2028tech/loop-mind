# LOOP-MIND frontend

React + TypeScript + Vite. See the repo-root [`README.md`](../README.md)
for setup and the [`spec.md`](../spec.md) "MASTER VISUAL & STYLING
SPECIFICATION" for the Graphite Ink design system this app implements
(`src/styles/agenthire-theme.css`).

```bash
npm install
npm run dev
npm run build
npm run lint
npm run format
```

`src/` is organized by portal, per `phase.md` Phase 01:

- `website/` — public pages (landing, auth entry) — Phase 02
- `app/` — student portal — Phase 05+
- `recruiter/` — recruiter portal — Phase 11+
- `components/` — shared reusable primitives (Shell, Navbar, Footer, Card,
  Button, Modal, Table, etc.) built in Phase 01
- `lib/` — shared utilities (API client, class-name helper)
