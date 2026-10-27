# LOOP-MIND — SINGLE SOURCE OF TRUTH

## COMPLETE DEVELOPMENT PHASE SPECIFICATION

### Specification-Driven Development

**Specification first. Code second.**

---

# 1. DOCUMENT AUTHORITY

This document is the controlled development execution guide for building **LOOP-MIND**.

The authority hierarchy is:

```text
LOOP-MIND — SINGLE SOURCE OF TRUTH
                ↓
        PAGE / LAYOUT STRUCTURE
                ↓
        PHASE SPECIFICATION
                ↓
             DESIGN
                ↓
          DATA / LOGIC
                ↓
              CODE
                ↓
             TESTING
                ↓
       SPECIFICATION AUDIT
```

The implementation must never be driven by:

```text
Existing code
      ↓
Developer assumption
      ↓
Typical recruitment platform
      ↓
Changed specification
```

The implementation must conform to the specification.

---

# 2. ABSOLUTE DEVELOPMENT RULE

The project must be built exactly one phase at a time.

```text
One phase
    ↓
Inspect current project
    ↓
Read spec.md
    ↓
Read phase.md
    ↓
Understand current phase
    ↓
Implement ONLY current phase
    ↓
Run application
    ↓
Test current phase
    ↓
Re-read entire spec.md
    ↓
Re-read entire phase.md
    ↓
Cross-check implementation
    ↓
Find missed CURRENT-phase requirements
    ↓
Implement missed CURRENT-phase requirements
    ↓
Run application again
    ↓
Test again
    ↓
Fix only CURRENT-phase issues
    ↓
Verify future phases were NOT implemented
    ↓
Confirm phase complete
    ↓
STOP
    ↓
Wait for explicit next phase
```

A phase is **not complete because the UI is visible**.

A phase is complete only when:

* every requirement assigned to that phase is implemented;
* the implementation uses the specified data/logic;
* the specified page structure is preserved;
* required dynamic behavior works;
* required API/database/AI behavior works;
* current-phase tests pass;
* the entire `spec.md` has been reread;
* the entire `phase.md` has been reread;
* current-phase omissions have been recovered;
* future-phase functionality has not leaked into the phase.

---
CURRENT PHASE ONLY: Compare the implementation against the complete `spec.md` and `phase.md`. Identify every missing, incorrect, unauthorized, or extra CURRENT-PHASE requirement. Fix every CURRENT-PHASE issue, run the application, test again, and re-read both documents completely. Repeat until the CURRENT PHASE is fully compliant. Do NOT implement FUTURE-PHASE requirements even if discovered during the audit. The next phase is allowed ONLY after the CURRENT PHASE passes this cross-check with no remaining CURRENT-PHASE issues.


# 3. PERMANENT CODING-AGENT INSTRUCTION

This instruction must appear at the beginning of every phase execution prompt.

```text
spec.md is the SINGLE SOURCE OF TRUTH for LOOP-MIND.

Specification first. Code second.

Read spec.md completely before making changes.

Read phase.md completely before making changes.

Inspect the current repository before implementation.

Do not rely on memory, previous summaries, previous phase reports,
or assumptions about recruitment platforms.

Implement ONLY the current phase.

Do NOT implement future phases early.

Do NOT invent:
- functionality
- fields
- datasets
- dropdown values
- filters
- navigation
- pages
- routes
- AI agents
- AI decisions
- ranking algorithms
- matching rules
- business rules
- database fields
- APIs
- security mechanisms
- workflows
- UI elements
- layouts
- technologies

unless they are defined by spec.md.

Preserve every existing implementation that already complies with spec.md.

Do not rewrite compliant functionality unnecessarily.

Use dynamic/database-driven data wherever the specification requires it.

Reference/demo values are not production data.

Reference layouts are authoritative wherever the specification says
the supplied image is the reference.

Do not redesign an authoritative reference page.

Do not move cards.

Do not change section ordering.

Do not remove specified sections.

Do not add unrelated sections.

Do not move navigation.

Do not replace specified tables with cards.

Do not replace specified cards with tables.

Do not alter specified footer placement.

Do not introduce another visual language.

Student Portal and Recruiter Portal are separate functional portals.

They may share the LOOP-MIND visual system but must not contain each
other's portal functionality.

If a requirement belongs to the CURRENT phase:
    implement it now.

If a requirement belongs to a FUTURE phase:
    do not implement it now.

If something is undefined:
    do not invent it.

After implementation:
1. Run the relevant application.
2. Test the current phase.
3. Re-read the entire spec.md.
4. Re-read the entire phase.md.
5. Cross-check the implementation.
6. Recover missed current-phase requirements.
7. Run the application again.
8. Test again.
9. Fix only current-phase issues.
10. Verify future-phase features were not implemented.
11. Confirm phase completion.
12. Produce the required phase completion report.

STOP.

Do not begin the next phase automatically.
```

---

# 4. GLOBAL VISUAL RULES APPLY TO EVERY PHASE

The visual system is established once and reused throughout the project.

Every page must use the same Graphite Ink system.

```text
Base background
#0F1317
```

Required hierarchy:

```text
--bg       #0F1317
--chrome   #12171B
--surface  #161C21
--row-alt  #1A2126
--raised   #1D242A
--scrim    rgba(9, 12, 14, 0.72)
```

Borders:

```text
--border    #232B31
--border-hi #2C353B
```

Text:

```text
--text       #F2F5F4
--text-soft  #C9D2CF
--text-mute  #8A9591
```

Accent/state colors:

```text
--accent       #6FD3C0
--accent-soft  #97E2D4
--accent-deep  #3F8478
--accent-wash  rgba(111, 211, 192, 0.14)

--warn         #E0A86B
--warn-wash    rgba(224, 168, 107, 0.14)

--danger       #E77E72
--danger-wash  rgba(231, 126, 114, 0.14)
```

Typography:

```text
Primary:
Space Grotesk, Helvetica, Arial, sans-serif

Monospace:
IBM Plex Mono, ui-monospace, monospace
```

Global shapes:

```text
--radius     10px
--radius-lg  14px
```

Buttons use `8px` radius.

Navigation links use `6px` radius.

Badges use `6px` radius.

Focus ring:

```text
0 0 0 3px rgba(111, 211, 192, 0.25)
```

Global shell:

```text
grid-template-columns: 224px 1fr
grid-template-rows: auto 1fr auto

grid-template-areas:
"nav nav"
"side main"
"foot foot"
```

Minimum height:

```text
100vh
```

At `max-width: 880px`:

```text
nav
main
foot
```

The sidebar is hidden.

Navbar:

* base background;
* bottom border;
* no shadow;
* sticky;
* `z-index: 40`;
* `padding: 14px 20px`;
* `gap: 22px`;
* mark `22px × 22px`;
* mark radius `6px`;
* mark uses accent.

Sidebar:

* `--chrome`;
* right border;
* `padding: 16px 12px`;
* `gap: 4px`.

Main content:

```text
background: var(--bg)
padding: 24px
gap: 18px
display: flex
flex-direction: column
```

Footer:

```text
background: var(--chrome)
border-top: 1px solid var(--border)
padding: 16px 20px
font-size: 12px
color: var(--text-mute)
```

Standard card:

```text
background: var(--surface)
border: 1px solid var(--border)
border-radius: 14px
padding: 20px
gap: 14px
```

Card grid:

```text
repeat(auto-fit, minmax(280px, 1fr))
gap: 16px
```

Buttons:

```text
display: inline-flex
align-items: center
gap: 8px
padding: 9px 14px
border-radius: 8px
font: 500 13.5px/1 var(--font-sans)
transition: 120ms ease
```

Primary:

```text
background: var(--accent)
color: var(--bg)
```

Ghost:

```text
background: transparent
color: var(--text-soft)
border-color: var(--border-hi)
```

Danger:

```text
background: var(--danger-wash)
color: var(--danger)
border-color: var(--danger)
```

Disabled:

```text
opacity: 0.45
cursor: not-allowed
```

Inputs:

```text
width: 100%
padding: 10px 12px
background: var(--raised)
color: var(--text)
border: 1px solid var(--border-hi)
border-radius: 8px
font: 400 13.5px/1.4 var(--font-sans)
```

Modal:

```text
width: min(560px, 100%)
background: var(--raised)
border: 1px solid var(--border-hi)
border-radius: 14px
padding: 22px
```

Modal scrim:

```text
position: fixed
inset: 0
z-index: 60
background: var(--scrim)
backdrop-filter: blur(2px)
```

A modal must close through its explicitly defined close control.

Do not introduce backdrop-click closing where the specification does not define it.

React Flow:

```text
Canvas: var(--bg)
Edge: var(--border-hi)
Animated edge: var(--accent)
Controls/minimap: var(--chrome)
Workflow node: var(--raised)
```

Recharts:

```text
Chart well: var(--chrome)
Border: var(--border)
Series 1: --accent
Series 2: --accent-deep
Series 3: --warn
```

No unrelated color palette.

No second theme.

No gradients replacing the base background.

No glassmorphism.

No unrelated glow.

The visual system is fixed; page data is dynamic.

---

# 5. GLOBAL DATA RULE

Every required dataset must exist.

If a real/user-provided dataset does not exist, the project must generate a complete, realistic, meaningful, project-context-specific development dataset.

Generated data must:

* be persistent;
* be logically consistent;
* be usable for development;
* be usable for testing;
* be usable for AI/ML/DL processing;
* be replaceable later;
* not be treated as real proprietary company information.

User-provided data always has priority over generated development data.

The application must process updated/replaced datasets when they are changed.

Every dropdown, selector, filter, multi-select, autocomplete, searchable field, or similar selectable source must have appropriate data.

No required dropdown may remain:

```text
empty
placeholder-only
incomplete
unrelated
hardcoded unnecessarily
```

Dependent data must remain consistent.

---

# 6. GLOBAL DYNAMIC-DATA RULE

The following must never become permanently hardcoded production values:

* student-specific information;
* recruiter-specific information;
* company data;
* jobs;
* applications;
* candidate records;
* AI scores;
* AI statuses;
* matching factors;
* interview records;
* interview questions;
* interview states;
* preparation plans;
* skill gaps;
* readiness;
* progress;
* historical outcomes;
* recruitment analytics.

Reference screenshot values are visual references only.

---

# 7. PHASE 00 — SPECIFICATION LOCK & REPOSITORY INSPECTION

## Goal

Establish the implementation boundary before writing feature code.

## Build

Read-only.

No product implementation.

## Required work

Read the complete LOOP-MIND `spec.md`.

Identify:

* complete product scope;
* Student Portal;
* Recruiter Portal;
* authentication;
* student profile/evidence;
* company intelligence;
* readiness;
* skill gaps;
* preparation;
* jobs;
* applications;
* AI recruitment;
* human approval;
* interviews;
* outcomes;
* closed-loop intelligence;
* analytics;
* datasets;
* AI architecture;
* ML/DL architecture;
* visual system;
* reference pages;
* dynamic-data requirements;
* undefined requirements;
* excluded functionality.

Inspect the repository.

Report:

* existing files;
* existing applications;
* existing frontend;
* existing backend;
* existing database;
* existing AI service;
* existing datasets;
* existing tests;
* existing reference assets;
* missing architecture;
* conflicting implementation;
* unsupported functionality already present.

## Must NOT

Write feature code.

Create future functionality.

Modify compliant implementation.

## Verification

Produce the initial repository/specification gap report.

---

# 8. PHASE 01 — PROJECT FOUNDATION & GLOBAL DESIGN SYSTEM

## Goal

Create the technical foundation without implementing product features.

## Build

Required architecture:

```text
LOOP-MIND/
│
├── AI services/
├── ML and DL/
├── databases/
├── storage/
├── frontend/
│   ├── website/
│   ├── app/
│   └── recruiter/
├── backend/
├── specs/
├── phase.md
├── spec.md
├── README.md
├── .gitignore
└── package.json
```

The exact final repository structure must follow the current LOOP-MIND specification where already defined.

## Frontend

```text
React.js
TypeScript
Vite
Tailwind CSS
shadcn/ui
React Flow
Recharts
```

## Backend

```text
Python
FastAPI
Pydantic
SQLAlchemy
JWT
OTP
REST APIs
```

## Database

```text
SQLite
```

## Vector layer

```text
Qdrant Local
```

## AI

```text
Python
LangChain
```

## Embeddings

```text
Sentence Transformers
```

## ML

```text
pandas
NumPy
scikit-learn
```

## DL

```text
PyTorch
```

## Testing/code quality

```text
Pytest
Ruff
ESLint
Prettier
Git
GitHub
```

Docker is optional development tooling.

No n8n in the core architecture.

MongoDB is not used.

Backend JavaScript is not used.

## Build reusable foundation components

* global shell;
* navbar;
* footer;
* card;
* statistics card;
* buttons;
* inputs;
* select/dropdown;
* modal;
* table;
* badge;
* progress indicator;
* upload/dropzone;
* loading state;
* error state;
* React Flow base;
* chart well.

These are reusable foundation components, not page-specific product features.

## Done when

The frontend foundation, backend foundation, database connection, global styles and reusable primitives run successfully.

---

# 9. PHASE 02 — LANDING / PUBLIC ENTRY

## Goal

Build the public LOOP-MIND entry experience defined by the specification.

## Reference rule

Use the supplied LOOP-MIND reference layout where declared authoritative.

Preserve:

* navbar;
* logo/brand position;
* heading placement;
* supporting content;
* information/card placement;
* footer;
* spacing;
* visual hierarchy.

Do not create a new landing-page design.

## Dynamic rule

Do not hardcode user/student/recruiter production data.

## Authentication entry

The public entry must connect to the defined authentication flow only.

Do not implement unrelated authenticated functionality.

## Done when

The public entry page visually follows the supplied LOOP-MIND reference and all specified entry interactions work.

---

# 10. PHASE 03 — AUTHENTICATION & ROLE SEPARATION

## Goal

Implement authentication and establish the separation between:

```text
Student Account
      ↓
Student Portal

Recruiter Account
      ↓
Recruiter Portal
```

## Build

* mobile/required identifier input;
* OTP flow;
* JWT;
* authentication records;
* role identification;
* authorization;
* student routing;
* recruiter routing.

The backend remains Python/FastAPI.

## Critical rule

Student and Recruiter are different functional portals.

A student must not receive Recruiter Portal functionality.

A recruiter must not receive Student Portal functionality.

## Do not invent

Do not add password authentication.

Do not add social authentication.

Do not add unspecified OTP rules.

Do not invent OTP expiry, lockout, attempt limits or resend limits where undefined.

## Done when

Correct authenticated users reach the correct portal and role boundaries are enforced.

## UPDATE — Student registration no longer creates the account at OTP verification

Student Create Account UPDATE SDD §1/§3/§11-12: verifying the OTP for a student `register`
purpose no longer creates a `Student` row. It creates a `RegistrationDraft` instead (role
`registration` on the issued JWT — a third role alongside `student`/`recruiter`, authorized
only for the new `/registration/draft/*` endpoints, never the real `/students/me/*` ones) and
every onboarding step from Basic Information through Professional Links + Resume stages its
data on that draft (`backend/services/registration_service.py`), not the real profile tables.

The real `Student` account, and every one of its profile rows, is created in exactly one
place — `POST /registration/create-account`, called only from the final Recruitment History +
Consent card's "Create Account" button, and only once Basic Information and all three required
consents are present. That call migrates the draft into the real tables using the same service
functions the post-account My Profile flow uses (not a second, divergent write path), deletes
the draft, and issues a real student JWT. Recruiter registration/login are unaffected — this
applies only to the student `register` purpose.

The LinkedIn Profile option (Basic Information) is now URL-only, not pasted text: the backend
does a best-effort unauthenticated fetch of the given URL (LinkedIn requires login for real
profile data, so this typically finds little or nothing — never fabricated) and runs the
existing LinkedIn Extraction Agent over whatever text comes back.

## UPDATE — LinkedIn extraction now automatic, all-or-nothing (LinkedIn Auto-Extraction UPDATE SDD)

Extraction is no longer a separate "Continue with LinkedIn"/"Extract from LinkedIn" button —
it now fires automatically as soon as the student enters a plausible LinkedIn URL and moves
focus off the field. The shortcut is only ever treated as successful when the extraction
genuinely found at least one skill, certification, or project; a technically-successful call
that found nothing is treated exactly like a failure (SDD §8, "No Partial LinkedIn Success"),
never a partial success that leaves the student in a half-imported state. On any failure
(network error, or a successful-but-empty fetch), the LinkedIn URL is cleared both on screen
and in the stored draft, a failure message is shown, and the student is not blocked — they
continue through the normal manual account-creation flow. As before, LinkedIn extraction never
creates the permanent account by itself; the account is still only created when Create Account
is pressed after consent on the final step.

## UPDATE — Real "Sign In with LinkedIn" OAuth for identity fields (LinkedIn Profile Extraction
Implementation Specification)

A new "Connect to LinkedIn" button sits alongside the URL field (auto-extraction on blur is
unchanged, still handles skills/certifications/projects via the existing best-effort text fetch).
The button opens a popup running real LinkedIn OAuth (OpenID Connect, `openid profile email`
scopes) — the only combination LinkedIn's API actually authorizes for a general integration,
which can return name/email/photo and nothing else (never skills/projects/certifications/
education/experience, regardless of configuration). New: `backend/services/
linkedin_oauth_service.py` (authorization-code exchange, client secret stays server-side),
`GET/POST /registration/draft/linkedin/oauth-{config,callback}`, and
`frontend/src/website/LinkedInOAuthCallback.tsx` (the popup's landing page — posts `{code}` back
to the opener via `postMessage` and closes itself). Gated behind `LINKEDIN_CLIENT_ID`/
`LINKEDIN_CLIENT_SECRET` (empty by default — no real LinkedIn Developer app exists for this
project yet); until configured, the button honestly reports "not configured" rather than
appearing to work. Extracted name/email only ever pre-fill Basic Information fields the student
hasn't already typed into themselves.

---

# 11. PHASE 04 — MASTER DATA & COMPANY INTELLIGENCE DATA LAYER

## Goal

Build the data layer that all later analysis and UI functionality consumes.

## Build

Structured application data required by LOOP-MIND, including:

* students;
* recruiters;
* authentication records;
* OTP records;
* student profiles;
* academics;
* skills;
* projects;
* certifications;
* coding experience;
* resume metadata;
* jobs;
* job requirements;
* applications;
* AI matching results;
* AI status;
* human approval/disapproval;
* disapproval reasons;
* interviews;
* interview schedules;
* interview questions;
* preparation plans;
* skill gaps;
* What-If results;
* progress;
* historical records;
* recruitment outcomes.

## Company Intelligence Dataset

Build the company intelligence dataset containing the specified company intelligence such as:

* company information;
* company requirements;
* historical job requirements;
* current job requirements;
* successful candidate profiles;
* requirement patterns;
* role-specific requirements;
* skill requirements;
* experience expectations;
* evidence expectations;
* relevant project expectations;
* other defined company recruitment signals.

## Dataset architecture

```text
Dataset
   ↓
Validation
   ↓
Company Intelligence Layer
   ↓
Analysis
   ↓
Student Intelligence
   ↓
Skill Gap / Readiness / Preparation
```

The company dataset must be replaceable without rewriting the application architecture.

## Qdrant data boundary

Prepare the vector-data architecture for:

* company knowledge;
* job requirements;
* historical recruitment information;
* successful candidate information;
* student evidence;
* skill knowledge;
* interview knowledge;
* preparation resources;
* recruitment outcomes.

## Done when

The data layer exists, relationships are valid, development datasets are persistent and replaceable, and later systems can consume them dynamically.

---

# 12. PHASE 05 — STUDENT PROFILE, SKILLS & EVIDENCE

## Goal

Build the student data foundation.

## Student profile must support

* skills being learned;
* projects;
* certifications;
* academics;
* coding experience;
* other evidence.

The system evaluates evidence rather than only claimed skills.

## Dynamic source

Student information must come from the authenticated student's stored data.

No permanent student-specific demo values.

## Profile relationship

```text
Student
 ├── Profile
 ├── Skills
 ├── Projects
 ├── Certifications
 ├── Academics
 ├── Coding Experience
 ├── Resume
 ├── Evidence
 └── Progress
```

## Done when

A student's actual stored information can be consumed by subsequent intelligence systems.

## UPDATE — LinkedIn-assisted profile completion (UPDATE SDD §5-12)

Basic Information gained an optional "LinkedIn Profile" option, additive
below the existing card content. Two profile-completion paths now exist:

```text
Path A — manual entry through every remaining onboarding step (unchanged)
Path B — Basic Information -> LinkedIn Profile -> LinkedIn Profile
         Extraction Agent -> applicable skills/certifications/projects
         stored -> remaining manual steps skipped -> Recruitment
         History + Consent -> Create Account
```

The extraction agent never fabricates a value not present in the
student's own pasted profile text (no live LinkedIn fetch exists in this
environment). Academic info is not written from this path — see
`AI services/agents/linkedin_extraction_agent.py`'s module docstring.
The existing Recruitment History + Consent gate on Create Account is
unchanged; Path B still reaches it before an account can be created.

Also fixed in this update: the optional profile-photo upload (previously
failed with "Save Basic Information before uploading a photo" because the
photo was sent before the Basic Information row existed — it now uploads
right after Continue saves) and the Professional Links resume upload
(previously could silently accept a non-PDF via drag-and-drop with no
error shown — now validated client-side with a visible error state).

## UPDATE — Resume replacement reconciles stale skills/projects/certifications (Dynamic
Resume Replacement & Student Data Synchronization SDD)

`StudentSkill`/`StudentProject`/`StudentCertification` each gained a `source` column
("manual" | "resume" | "linkedin") tracking where a row came from. Resume upload/replacement
(`student_profile_service.apply_resume_extraction`) still adds whatever the new resume genuinely
contains that the student doesn't already have (tagged `source="resume"`), and now also calls a
new `reconcile_resume_derived_records` that deletes any `source="resume"` row absent from this
same fresh extraction — so a skill/project/certification dropped from a replaced resume actually
stops being current, instead of accumulating forever across every re-upload. Anything the
student entered manually, edited, attached evidence to, or uploaded a certificate file for is
immediately marked `source="manual"` (in `update_skill`, `add_skill_evidence`,
`set_certificate_file`) and is therefore never removed by a later resume replacement, nor is
anything tagged `source="linkedin"`. Skill Gap, Placement Readiness and Preparation Plan already
auto-recalculate on resume upload (an earlier update) and so already pick up the reconciled set
with no further change; historical analyses/plans and past applications' resume references are
point-in-time snapshots, unaffected by this.

## UPDATE — Manual entry dedupes too; source protection only upgrades; empty extraction never
wipes prior data (Dynamic Resume Replacement, Skill/Project/Certification Synchronization &
Source-Aware Deduplication SDD)

Three refinements: (1) `create_skill`/`create_project`/`create_certification` — used by My
Profile's manual "Add" forms directly, not only by extraction — now look up an existing
case-insensitive name match first and update it in place instead of ever creating a duplicate
row, closing the one path that could still inflate a displayed count. (2) A skill/project/
certification first seen from a resume and later independently confirmed by LinkedIn or the
student themselves now has its `source` upgraded (resume → linkedin → manual) rather than
staying `"resume"` forever — otherwise it could still be deleted by a later resume replacement
despite being LinkedIn/manually confirmed. (3) `apply_resume_extraction` now skips reconciliation
entirely when the new resume's extraction found zero skills/projects/certifications across the
board — treated as a failed/inconclusive parse rather than "this resume legitimately has none,"
so it can never wipe out valid prior resume-derived data.

---

# 13. PHASE 06 — STUDENT INTELLIGENCE MULTI-AGENT SYSTEM

## Goal

Build the first functional multi-agent system.

This is where the **first six AI agents** are built.

## Multi-Agent System 1

```text
Company Intelligence Agent
          ↓
Student Skill Analysis Agent
          ↓
Placement Readiness Agent
          ↓
Skill-Gap Analysis Agent
          ↓
Preparation Plan Agent
          ↓
What-If Analysis Agent
```

The system determines what a student needs to become ready for a target company and role.

## Exactly these six agents

### Agent 1 — Company Intelligence Agent

Analyzes:

* company requirements;
* historical requirements;
* current roles;
* recruitment patterns;
* successful candidate characteristics;
* historical recruitment outcomes.

### Agent 2 — Student Skill Analysis Agent

Analyzes:

* student skills;
* academics;
* projects;
* certifications;
* coding experience;
* evidence;
* current learning status.

### Agent 3 — Placement Readiness Agent

Compares:

```text
Student Profile
      +
Company Intelligence
      +
Target Job
      ↓
Placement Readiness
```

### Agent 4 — Skill-Gap Analysis Agent

Identifies:

* missing skills;
* weak skills;
* missing evidence;
* requirement mismatches;
* readiness gaps;
* priority gaps;
* reasons behind assessment.

### Agent 5 — Preparation Plan Agent

Generates individualized plans:

* short-term;
* medium-term;
* long-term.

Plans update when:

* student skills change;
* progress changes;
* target company changes.

### Agent 6 — What-If Analysis Agent

Handles questions such as:

```text
What should I improve first to become ready for Company X?

What happens if I learn Generative AI?

What if I complete DSA?

What should I improve first?
```

The agent uses:

* current student state;
* company requirements;
* current skill-gap context.

## RAG

RAG is required for the final LOOP-MIND architecture.

```text
Company / Recruitment / Student Data
              ↓
       Data Processing
              ↓
          Embeddings
              ↓
           Qdrant
              ↓
             RAG
              ↓
      LangChain Agents
              ↓
        AI Analysis
```

## Done when

All six agents operate as the defined Student Intelligence multi-agent system and consume actual project data.

---

# 14. PHASE 07 — STUDENT DASHBOARD

## Goal

Build the Student Portal Dashboard using the supplied reference layout.

## Reference layout rule

The layout is fixed.

The data is dynamic.

Do not:

* move cards;
* change card ordering;
* add dashboard sections;
* remove dashboard sections;
* change the number of top cards;
* replace charts;
* move the footer;
* move the navbar;
* introduce a sidebar where the reference does not have one;
* replace the dashboard with another layout.

## Target Company

The Target Company section must be dynamic.

Before selection:

```text
Target Company

Not set yet

Set a target company to get personalized
recommendations, skill analysis and preparation plan.

[ Set a target company → ]
```

After selection:

```text
Target Company

[Student's selected company]
```

The company comes from stored student data.

## Dashboard dynamic content

Student-specific:

* student information;
* target company;
* profile values;
* skill values;
* project values;
* certification values;
* readiness-related values;
* intelligence results.

## Done when

The dashboard matches the supplied reference layout and all student-specific content is database-driven.

## UPDATE — Student Dashboard SDD (skills rename, resume card, in-page readiness modal)

* "Skills Added" renamed to "Current Skills" — same dynamic `skills_count`
  value (skills from manual entry, LinkedIn extraction, and now resume
  extraction all land in the same `student_skills` table, so the count
  was already aggregating every source with no backend change needed).
* A new "Upload Your Resume" card appears in the Placement Readiness /
  Target Company / Recent Activity row, only while the student has no
  resume on file (`has_resume` on `GET /students/me/dashboard`).
  Uploading goes through the same `/students/me/resume` endpoint as the
  Professional Links onboarding step, so it can never create a duplicate
  resume record. **Superseded** by the Skill Gap/Profile Photo/Resume
  Management UPDATE SDD below: the card no longer disappears once a
  resume exists — it now always renders, switching between "Upload Your
  Resume" and "Resume Available / Replace resume" so the student always
  has a path to manage it from the Dashboard.
* Every resume upload/replacement now runs the Resume Parser Agent's real
  text-extraction capability (`extract_from_text`, using `pypdf` to read
  the PDF) and stores any new skills/certifications/projects found,
  deduped against what the student already has.
* "View Detailed Analysis" no longer navigates to the Skill Gap page
  (superseding the "Entry points" example directly below, which predates
  this update) — it opens a centered modal on the same Dashboard page,
  live-computed from the Placement Readiness Agent (+ Student Skill
  Analysis Agent) every time it opens, showing Current Skills and the
  skills backed by strong evidence. The Skill Gap page's own "Student
  Dashboard → Placement Readiness → View Detailed Analysis → Skill Gap
  Analysis" entry point (Phase 08 below) no longer applies to this
  button; Skill Gap Analysis remains reachable via its own nav item.

## UPDATE — Student Portal right-side navigation

The Student Portal's shared top navigation (Dashboard, Skill Gap,
Preparation Plan, Jobs, My Profile, Logout — `useStudentNavItems()`) is
now rendered flush to the right edge of the navbar on every Student
Portal page, via a new shared `<StudentNavbar />` component
(`frontend/src/components/StudentNavbar.tsx`) that every Student Portal
page renders instead of separately composing `<Navbar items={...}>`.
Scoped to the Student Portal only via an opt-in `linksAlign="end"` prop
on the shared `Navbar` component (new `.lm-navbar__links--end` CSS
modifier) — the Recruiter Portal's own `useRecruiterNavItems()` +
default `<Navbar>` usage is untouched.

---

# 15. PHASE 08 — SKILL GAP ANALYSIS & WHAT-IF PAGE

## Goal

Build the Skill Gap Analysis page and connect it to the Student Intelligence system.

## Entry points

Both must open the same page:

```text
Student Dashboard
      ↓
Skill Gap
      ↓
Skill Gap Analysis
```

and:

```text
Student Dashboard
      ↓
Placement Readiness
      ↓
View Detailed Analysis
      ↓
Skill Gap Analysis
```

## Exact reference structure

```text
TOP NAVBAR
------------------------------------------------

Skill Gap Analysis                     Quote Card
Description

------------------------------------------------

Target Company / Role
Overall Readiness
Quick Actions

------------------------------------------------

Skill Gap Overview
Skill Distribution
Top Priority Areas

------------------------------------------------

Filters
Search

------------------------------------------------

Skill Analysis Table

------------------------------------------------
FOOTER
```

The uploaded Skill Gap Analysis image is the authoritative layout.

Do not:

* move cards;
* change ordering;
* remove sections;
* add unrelated sections;
* replace the table;
* move Quick Actions;
* move Overall Readiness;
* move Skill Distribution;
* move Top Priority Areas;
* remove filter tabs;
* remove search;
* remove footer;
* change navbar structure.

## Dynamic content

* student data;
* target company;
* target role;
* readiness percentage;
* readiness state;
* skill counts;
* skill distribution;
* priority areas;
* skill names;
* categories;
* student levels;
* required levels;
* status;
* priority;
* resource availability;
* search results;
* filter counts.

## What-If

The What-If interface opens as a centered card/modal.

It does not navigate to another page.

```text
Try What-If Analysis

What if I learn Generative AI?

[ text input ]

[ Analyze ]
```

The analysis uses:

```text
Question
+
Student current profile/skills
+
Current Skill Gap context
      ↓
What-If Analysis
```

The result remains in the same centered card/modal.

## Done when

The reference structure is preserved, the analysis is dynamic, and What-If works against the student's current intelligence context.

## UPDATE — Skill Gap / Placement Readiness / Plan / What-If SDD

* **Missing Evidence row status**: a required skill the student meets/
  exceeds the required level for, but has no supporting evidence, now
  shows status "Missing Evidence" in the All Skills table (new
  `SkillStatus` value, new filter tab) instead of being silently shown as
  "Strong" — it already counted toward the Missing Evidence overview
  number; now the per-row status agrees with that count
  (`backend/services/skill_gap_page_service.py`).
* **Placement Readiness detail modal** (Dashboard "View Detailed
  Analysis") now shows **Ready Skills** — the Placement Readiness
  Agent's own `matched_skills` for the *currently selected target
  company/role* — instead of a company-agnostic "strong evidence"
  heuristic; also now resolves and displays the actual target role, not
  just the company (`backend/services/intelligence_service.py::
  get_placement_readiness_detail`).
* **What-If Analysis** now returns a genuinely calculated
  `current_readiness_percentage` / `projected_readiness_percentage` pair
  (the projection reruns the real Placement Readiness calculation against
  a *copy* of the student's skills with the asked-about topic
  hypothetically raised to the target role's required level — the
  student's actual stored skills are never touched) and `relevant_roles`
  (other roles at the target company whose real stored requirements
  include the topic) — both surfaced in the same centered What-If
  card/modal, in a dedicated result section
  (`AI services/agents/what_if_analysis_agent.py`).
* **Get Personalized Plan**: unchanged behavior (still generates +
  persists a versioned plan without displaying its content on this page),
  now with a "View your plan on the Preparation Plan page →" link after a
  successful generation for discoverability.

## UPDATE — Resume upload auto-refreshes Skill Gap Analysis (Student Resume Upload & Skill
Gap Automation SDD)

`POST /students/me/resume` (every upload or re-upload, from any of its existing upload
locations) now checks whether the student already has a target company selected and, if so,
immediately re-runs `intelligence_service.analyze_skill_gap` with the newly extracted
skills — the Skill Gap page picks up the change without the student needing to re-select their
target to force a recalculation. Resume-before-company (Scenario A) was already correct: the
resume is stored/extracted regardless of target state, and the existing on-demand first
analysis (triggered when a target is later chosen) already used whatever was previously
extracted. Both orderings now converge on the same result through the one existing agent
pipeline (Resume Agent → extraction → database → Skill Gap Agent → database → Skill Gap page),
with no UI-side recalculation and no hardcoded skill counts or readiness numbers.

## UPDATE — Unified Placement Readiness Percentage (Placement Readiness Percentage SDD)

Dashboard's Placement Readiness, this page's Overall Readiness and the Preparation Plan page's
Current Readiness now all read through the same shared, auto-creating backend lookup
(`intelligence_service.get_latest_skill_gap_analysis` / `get_readiness_summary`) instead of each
page running its own query against the stored SkillGapAnalysis rows — previously Dashboard's own
query wasn't even scoped to the student's *current* target company, so it could show a number
left over from a target the student had already moved on from. Every action that changes a
student's skills/evidence/projects/certifications/resume, or their target company/role (via the
Dashboard, this page, or My Profile's Career & Placement — all three write the same underlying
`StudentCareerPlacement` row), now triggers an immediate recalculation whenever a target is
already set.

## UPDATE — Skills You Have no longer reads 0 for a student with real skills (Skill Gap,
Profile Photo & Resume Management SDD)

"Skills You Have" in the overview card was `len(existing_skills)` — the count of *required*
skills the student already meets, the same number the "Already Strong" distribution bucket
measures — so it read 0 whenever none of a student's real stored skills happened to be on the
current target's specific requirement list, even with skills genuinely on file from the resume,
profile entry, or LinkedIn (all already merged into one deduplicated `StudentSkill` table at
storage time). It now counts the student's own distinct stored skills directly
(`len(student_skill_lookup(db, student_id))`), independent of the current target — "Already
Strong"/"Needs Improvement"/"Missing"/"Not Relevant" (the distribution chart) remain exactly as
before, since those four *are* meant to be target-relative.

## UPDATE — What-If Analysis: Potential Improvement shown, explicit Reset, no stale result
during loading (Skill Gap Analysis — What-If Analysis Specification)

The core simulation guarantees were already correct (`ask_what_if` only ever persists to the
separate `WhatIfResult` table; the modal's state fully resets on each open) — three display gaps
were fixed: (1) "Potential Improvement" is now shown alongside Current/Projected Readiness,
computed from the same two agent-returned numbers; (2) an explicit Reset button now clears the
modal's local question/result/error without an API call or closing the dialog; (3) the previous
answer is now cleared the instant a new analysis starts, so "Analyzing…" never sits above a stale
result. The action button is relabeled "Generate" to match this SDD's naming.

---

# 16. PHASE 09 — PREPARATION PLAN PAGE

## Goal

Build the personalized Preparation Plan page.

## Reference layout

The uploaded Preparation Plan image is authoritative.

The page structure is:

```text
TOP NAVBAR

Preparation Plan                         Quote Card
A personalized plan based on your
current year, goals and target company.

------------------------------------------------

Select Target Company       Current Readiness
[ Target Company ▼ ]              XX%

Select Target Role              Readiness Ring
[ Target Role ▼ ]                Dynamic message

Your Academic Year
[ Academic Year ▼ ]

[ Generate Preparation Plan → ]

------------------------------------------------

Year-Wise Focus
Your Goals
AI Recommendations
Detailed Preparation Plan

------------------------------------------------
FOOTER
```

Exact reference placement must be retained.

Do not:

* rearrange cards;
* move Current Readiness;
* move Year-Wise Focus;
* move Your Goals;
* move AI Recommendations;
* move Detailed Preparation Plan;
* change footer structure;
* replace the layout.

## Dynamic data

* student name;
* target company;
* target role;
* academic year;
* readiness;
* goals;
* recommendations;
* skill levels;
* target levels;
* plan dates;
* plan status;
* priority;
* resources;
* preparation-plan entries.

## Academic-year behavior

### 1st year

* longer-term fundamentals;
* learning;
* projects;
* evidence building.

### 2nd year

* deeper skills;
* projects;
* technical preparation.

### 3rd year

* company-focused skills;
* DSA;
* projects;
* assessments;
* interview preparation.

### Final year

* focused placement;
* company-specific preparation.

## Versioning

Regenerated plans create new versions.

Previous plans must not silently disappear.

Plan history is retained.

## Export

The reference contains:

```text
Export Plan ↓
```

The exported content must represent the currently displayed preparation plan.

## Done when

A student can receive a personalized, dynamic preparation plan whose content changes with the student's state and target context.

## UPDATE — Year-Wise Roadmap SDD

* **Continuous timeline fix**: every plan item previously started on the same date (the
  plan's own `created_at`), so a student's whole plan appeared to happen simultaneously.
  Each item's window now begins the day after the previous item's window ends, in the same
  priority order the Preparation Plan Agent already produces (highest-priority skill first) —
  `backend/services/preparation_plan_page_service.py::_plan_rows`.
* **Year-Wise Focus is now a roadmap, not just a caption**: below the existing year pills and
  focus text (both unchanged), the card now shows the active plan's skill sequence — numbered,
  connected steps with each skill's start/end date — reusing the same stepper visual already
  established by the Student Dashboard's "Preparation Journey" card. Changing academic year
  still works exactly as before (regenerate via the existing dropdown + Generate button); the
  roadmap reflects whichever plan is currently active.
* No backend schema changes were needed — the roadmap reuses the same `plan_items` the
  Detailed Preparation Plan table already displays, now correctly sequenced.

---

# 17. PHASE 10 — STUDENT JOBS & APPLICATION SYSTEM

## Goal

Build the Student Portal Jobs page and application workflow.

## Page

```text
Discover Opportunities
Route: /jobs
```

## Reference layout

The uploaded Jobs page is authoritative.

Preserve:

* navbar;
* Jobs active state;
* heading;
* description;
* quote card;
* summary cards;
* job listing;
* search;
* sorting;
* filters;
* job cards;
* Apply Now;
* Save;
* footer;
* spacing;
* proportions;
* visual hierarchy.

Do not redesign the page.

## Student navigation

```text
LOOP-MIND
Dashboard
Skill Gap
Preparation Plan
Jobs
My Progress
```

Where the current specification later renames My Progress to My Profile, follow the current specification.

## Dynamic jobs

Jobs must come from the database.

Do not permanently hardcode example companies or jobs.

## Search/filter

Search and filters work together.

Example:

```text
Search: Python
+
Company: Google
+
Job Type: Full-time
```

Only jobs satisfying active conditions appear.

## Save

Save is persistent.

It must survive:

* refresh;
* logout/login;
* returning to Jobs.

The saved state belongs to the logged-in student.

## Application

Student applies to a specific job.

Before application:

```text
Profile completeness validation
        ↓
Required information available?
        ├── NO → centered validation card
        └── YES
             ↓
         Apply
```

Application must be linked to:

```text
Student
   ↓
Application
   ↓
Specific Job
```

## Application fields

Where the public application specification requires:

* Name;
* Email;
* Phone;
* PDF resume.

## Done when

Students can dynamically discover jobs, save jobs persistently, satisfy application requirements, and submit applications tied to the correct job.

---

# 18. PHASE 11 — RECRUITER PORTAL FOUNDATION & DASHBOARD

## Goal

Build the separate Recruiter Portal and Recruiter Dashboard.

## Recruiter navigation

```text
LOOP-MIND | Recruiter Portal

Dashboard
Jobs
Candidates
Interviews
```

The Recruiter Dashboard reference requires the recruiter dropdown/profile element removal specified by the current LOOP-MIND requirement.

No Student Portal component may appear inside Recruiter Portal.

## Dashboard reference layout

Preserve:

* overall dashboard structure;
* navigation;
* dashboard sections;
* section order;
* card arrangement;
* table arrangement;
* application pipeline;
* quick actions;
* recent applications;
* upcoming interviews;
* recent activity;
* footer;
* dark visual system.

## Dashboard sections

The reference includes:

* statistics;
* jobs/application information;
* application pipeline;
* quick actions;
* recent applications;
* upcoming interviews;
* recent activity.

## Dynamic values

All statistics and records come from the authenticated recruiter's data.

Example screenshot values are reference values only.

## Done when

Recruiter authentication leads to the Recruiter Dashboard with the exact supplied structure and dynamically stored recruiter data.

## UPDATE — Recruiter Portal navigation right-aligned; Pending Approval metric added
(Recruiter Portal Dashboard/Job Management/Candidate Evaluation & Closed-Loop ML Workflow SDD
§1-2)

Every Recruiter Portal page (Dashboard, Job Management, Candidates, Interviews, Analytics) was
still composing its own `<Navbar brand="LOOP-MIND | Recruiter Portal" items={...}>` with no
`linksAlign` — left-aligned, unlike the Student Portal's own `StudentNavbar`. A new shared
`RecruiterNavbar` component (`frontend/src/components/RecruiterNavbar.tsx`) now backs all five
pages with `linksAlign="end"`, the exact same pattern `StudentNavbar` already uses, so the two
portals' navigation styling can never drift apart again.

The Dashboard's six required overview metrics (Total Jobs, Total Applications, Shortlisted,
Under Review, Pending Approval, Rejected) previously only had five — an AI-shortlisted
application awaiting a recruiter decision was already counted under "Shortlisted" (an existing,
still-unchanged, already-tested classification used for filtering on the Candidates page), but
had no distinct "awaiting human review" count of its own anywhere. A new shared
`application_status.is_pending_approval()` helper now feeds a `pending_approval` field on the
Dashboard's summary + Application Pipeline and the Candidates page's summary, additive to (not
replacing) the existing Shortlisted/Under Review/Rejected classification. **Superseded** by the
Recruiter Dashboard — Final Specification below: Pending Approval is removed again everywhere,
and Shortlisted/Under Review are redefined.

## UPDATE — Dashboard reverted to four cards; Shortlisted/Under Review redefined as
non-mutually-exclusive; Rejected scoped to recruiter decisions only (Recruiter Dashboard — Final
Specification)

Pending Approval is removed from the Dashboard summary, Application Pipeline, and Candidates
page summary — back to no separate card, per this spec's explicit repeated rule. The Dashboard's
first row is exactly Total Jobs / Total Applications / Shortlisted / Under Review. New shared
helpers in `application_status.py` replace `is_pending_approval`: `is_ai_shortlisted` (the
Shortlisting Agent's own `ai_status == "shortlisted"` output, independent of any human decision),
`is_awaiting_decision` (`approval is None` — true from the moment an application is created, not
tied to AI status at all), and `is_recruiter_rejected` (a human disapproval specifically, never
the AI's own "rejected" recommendation). Shortlisted and Under Review are deliberately no longer
mutually exclusive — an AI-shortlisted application awaiting a decision now correctly counts
toward both. Rejected moved out of the top summary row (kept in the Application Pipeline
breakdown) and is now scoped to recruiter disapprovals only. The Candidates page's own per-row
`bucket()`-based status column is untouched — only its Pending Approval summary card was removed.

---

# 19. PHASE 12 — RECRUITER JOB MANAGEMENT

## Goal

Build Recruiter Portal Job Management and Create New Job.

## Entry points

Job Management opens from:

```text
Recruiter Navbar
      ↓
Jobs
```

and:

```text
Recruiter Dashboard
      ↓
Create New Job
      ↓
Job Management
```

The Job Management page contains:

```text
+ Create New Job
```

inside the Your Job Postings section.

Clicking it opens a centered Create New Job card/modal.

## Reference layout

```text
LOOP-MIND | Recruiter Portal
Dashboard Jobs Candidates Interviews

------------------------------------------------

Job Management                         Quote Card
Description

------------------------------------------------

Total Jobs
Active Jobs
Paused Jobs
Total Applications

------------------------------------------------

Your Job Postings

Search
Status dropdown
+ Create New Job

------------------------------------------------

Job Table
------------------------------------------------

Footer
```

Preserve:

* overall layout;
* navbar;
* active Jobs state;
* title placement;
* description;
* quote card;
* four statistic cards;
* Your Job Postings;
* search;
* status dropdown;
* Create New Job placement;
* table;
* column order;
* View Details;
* three-dot action;
* footer;
* spacing;
* hierarchy.

## Create New Job

The recruiter must enter the job information and constraints specified by the project.

The explicitly specified fields include:

* Job Title;
* Job Role;
* Experience.

Do not invent additional fields.

## Persistence

After creation:

```text
Create Job
   ↓
Database
   ↓
Recruiter Job Management
   ↓
Student Portal Jobs
```

The same newly created job becomes available to students.

## Done when

A recruiter can create a defined job, the job is persisted, it appears dynamically in Recruiter Job Management and becomes available in Student Jobs.

---

# 20. PHASE 13 — RECRUITER CANDIDATES PAGE & RECRUITMENT AI SYSTEM

## Goal

Build the Candidates page and the second functional multi-agent system.

## Candidates entry points

```text
Recruiter Navbar
      ↓
Candidates
```

and:

```text
Recruiter Dashboard
      ↓
View All Candidates
      ↓
Candidates
```

Both must use the same candidate data.

## Reference layout

```text
LOOP-MIND | Recruiter Portal
Dashboard Jobs Candidates Interviews

Candidates                         Quote Card
Review candidates, AI evaluations,
and recruitment progress.

------------------------------------------------

Total Candidates
Shortlisted
Under Review
Rejected

------------------------------------------------

All Candidates

Search candidates by name, role, or skills...

All Jobs
All Status
All AI Evaluation
Refresh

------------------------------------------------

Candidate Table

Candidate Name
Applied Role
Applied On
AI Score
Matching Factors
Status
Action

------------------------------------------------

AI Recruitment Workflow

------------------------------------------------

Footer
```

Preserve exact structure and placement.

## Candidate source

Candidates originate from:

```text
Recruiter creates Job
      ↓
Job available in Student Portal
      ↓
Student applies
      ↓
Application created
      ↓
Candidate appears in Recruiter Candidates
```

## Candidate AI inputs

Candidate side:

* resume;
* skills;
* projects;
* relevant profile/application information.

Job side:

* job requirements;
* job constraints;
* required skills;
* role requirements;
* other recruiter-defined requirements.

## Multi-Agent System 2

```text
Resume Parser Agent
        ↓
Embedding Agent
        ↓
Matching Agent
        ↓
Shortlisting Agent
        ↓
Human Approval
        ↓
Interview Agent
        ↓
Email Agent
```

## Exactly four recruitment agents in this system

### Agent 7 — Resume Parser Agent

Input:

```text
Resume PDF
```

Output includes:

* skills;
* education;
* projects;
* experience;
* certifications;
* contact information;
* other relevant evidence.

### Agent 8 — Embedding Agent

Converts relevant recruitment/student/company information into embeddings for semantic retrieval.

### Agent 9 — Matching Agent

Compares:

```text
Candidate Profile
        VS
Job Requirements
```

and determines alignment.

### Agent 10 — Shortlisting Agent

Uses:

* resume information;
* job requirements;
* matching results;
* relevant evidence.

Produces exactly:

```text
Shortlisted
Hold
Rejected
```

These are AI recommendations.

They are not final recruitment decisions.

## AI workflow UI

The Candidates page must show:

```text
Resume Parser
      →
Embedding
      →
Matching
      →
Shortlisting
      →
Human Approval
      →
Interview
      →
Email Invitation
```

Workflow states must be dynamic.

React Flow is used for live workflow visualization.

Defined states include:

* Pending;
* Running;
* Completed;
* Failed;
* Paused;
* Approved;
* Rejected.

## Selected Candidate

The workflow area contains a selected-candidate information card with dynamic:

* candidate;
* role;
* AI score.

## Done when

A real student application can become a candidate, the AI pipeline processes that application, AI status is generated, and the recruiter can inspect the complete workflow.

---

# 21. PHASE 14 — HUMAN APPROVAL & RECRUITMENT OUTCOME

## Goal

Implement the human-in-the-loop checkpoint.

## Fundamental rule

AI never makes the final critical recruitment approval alone.

Recruiter reviews:

* candidate score;
* evidence;
* matching factors;
* AI evaluation.

## Flow

```text
AI Shortlisting
      ↓
Recruiter Review
      ↓
Approve / Disapprove
```

### Approve

```text
Human Approval
      ↓
Approved
      ↓
Interview Agent
```

### Disapprove

```text
Human Disapproval
      ↓
Disapproval Reason
      ↓
Student Portal
      ↓
Skill Gap
      ↓
Preparation Plan
      ↓
Student Improvement
```

## Important separation

AI status and human decision are separate.

For example:

```text
AI Status:
Rejected

Human Decision:
Approved
```

must remain technically distinguishable.

## Dynamic outcome

The application must preserve the relationship:

```text
Student
   ↓
Application
   ↓
Specific Job
   ↓
AI Evaluation
   ↓
Recruiter Human Approval
   ↓
Final Application Outcome
```

## Student-side result

If the application is disapproved, the student must be able to access the recorded result through the existing Jobs-page structure.

The existing Jobs layout must not be redesigned.

Only the specified application-result access is added.

The result card/modal must be centered.

It must show the recorded reason, especially a specific skill gap where that is the reason.

## Done when

Human approval is mandatory, AI recommendation remains separate, final outcomes are persisted, and student outcomes can feed back into the intelligence system.

---

# 22. PHASE 15 — INTERVIEW AGENT, INTERVIEWS PAGE & EMAIL AGENT

## Goal

Complete the approved-candidate recruitment path.

## Agent 11 — Interview Agent

Triggered after recruiter approval.

It:

* identifies the specific job role;
* understands role requirements;
* generates role-specific interview questions;
* stores generated questions;
* makes questions available from Recruiter Interviews.

The source also defines:

* evaluation criteria;
* rubrics.

## Agent 12 — Email Agent

Handles:

* interview invitation;
* interview information;
* interview-related email;
* candidate communication.

## Interviews Page

### Entry points

```text
Recruiter Navbar
      ↓
Interviews
```

and:

```text
Recruiter Dashboard
      ↓
Prepare Interview Questions
      ↓
Interviews
```

Both open the same Interviews page.

## Reference layout

Preserve:

* navbar;
* Interviews active state;
* page heading;
* description;
* quote card;
* four summary cards;
* Scheduled Interviews container;
* search;
* filters;
* Schedule Interview button;
* table;
* column arrangement;
* Recent Activity;
* footer;
* spacing;
* hierarchy;
* alignment.

## Interview lifecycle

```text
Recruiter Job
      ↓
Student applies
      ↓
Candidate
      ↓
AI evaluation
      ↓
Human approval
      ↓
Approved candidate
      ↓
Interview questions
      ↓
Interview
```

Interview states and records must be dynamic.

## Recent Activity

Must be based on actual interview events.

Examples of event types represented by the reference:

* interview questions generated;
* interview invite sent;
* interview scheduled;
* interview completed.

## Recruiter isolation

Interview records belong to the authenticated recruiter and their job postings.

A recruiter must not see another recruiter's private interview records.

## Done when

Approved candidates can flow into interview preparation, questions are generated and stored, invitations are produced, and interview records appear dynamically.

## UPDATE — Interview invitation now cites actual matched skills instead of being generic
(Recruiter Dashboard — Final Specification §6-7)

The invitation body previously never explained *why* a candidate was selected — a plain
"Congratulations, you've been selected" with no supporting detail, exactly the kind of generic
reasoning this spec forbids. The recruitment pipeline's own matching data
(`AIMatchResult.matching_factors["matched_skills"]`) was already available at the exact call site
in `interview_service.get_interview_detail` (right next to where `missing_skills` was already
being read) but never passed through. `email_agent.py`'s `compose_invitation` now accepts the
matched skills and lists them in the body ("Your profile was selected based on your demonstrated
skills relevant to this role, including: ...") whenever they exist, and simply omits that
paragraph — never fabricates one — when no matched-skills data is available for the application.

## UPDATE — Interview invitation email is now actually sent, with a real, persisted delivery status
(Recruiter Interview Invitation & Demo Email Specification)

A successful Interview Agent/Email Agent tick previously meant only that content had been
*generated* — no email was ever dispatched, and the Recruiter Portal showed nothing beyond the
checkmark. This closes that gap end to end:

* **Trigger point**: `recruiter_candidates_service.approve_candidate` now calls
  `interview_service.send_invitation_email` immediately after `generate_questions_for_approval`
  succeeds, inside the same approval event — not on a later page view, and not gated behind a
  separate "schedule interview" action (which remains its own, unaffected recruiter action).
* **Email resolution** (`application_status.resolve_recipient_email`): profile email first, then
  — only if genuinely unavailable — the email the Resume Parser Agent found literally present in
  the student's uploaded resume text (`resume_parser_agent._extract_email`, stored on
  `StudentProfessionalLinks.resume_extracted_email` by `apply_resume_extraction`). Never invents
  an address; reports `"unavailable"` when neither exists.
* **Real SMTP transport** (`backend/services/email_service.py`): `smtplib`-based, configured only
  through `EMAIL_PROVIDER`/`EMAIL_HOST`/`EMAIL_PORT`/`EMAIL_USERNAME`/`EMAIL_PASSWORD`/
  `EMAIL_FROM` in `backend/core/config.py` (env/`.env`-sourced, never hardcoded). Honestly reports
  "not configured" rather than pretending to send when the demo mailbox isn't set up.
* **Persisted delivery status**: `Interview` gained `email_status`
  (pending/sending/sent/failed), `recipient_email`, `email_source` (profile/resume/unavailable),
  `email_sent_at`, `email_error` — a real, terminal state survives a page refresh instead of being
  recomputed as a live preview. `send_invitation_email` is idempotent: once `email_status` reaches
  `"sent"`, re-approving the same application never re-sends or duplicates anything; a `"failed"`
  attempt may be retried on a later approval since nothing was ever actually delivered.
* **Interview details in the invitation** at approval time (before any scheduling exists) state
  the real, current process status ("to be scheduled — you will be contacted separately") rather
  than fabricating a type/time; once `schedule_interview` sets real values, later invitation
  previews (`get_interview_detail`) already reflect them.
* **Recruiter Portal**: the Interviews page's detail modal now shows the actual email delivery
  badge, recipient, source, and any error — not just a permanent success tick. The Candidates
  page's workflow panel gained a real "Interview & Email" card (question count, delivery badge,
  recipient) alongside the existing stage diagram, and the `email_invitation` stage's state is now
  driven by the real `email_status` (`sent`→completed, `sending`→running, `failed`→rejected)
  instead of being inferred from whether the interview happened to be scheduled.
* Both outcomes are tested (`backend/tests/test_interviews.py`): a real send with a mocked SMTP
  transport reaching `"sent"`, an unconfigured transport honestly reaching `"failed"`, the
  resume-email fallback firing only when the profile email is genuinely absent, and the
  no-email-anywhere case reporting `"unavailable"` rather than inventing an address.

## UPDATE — Sender identity, non-destructive resume-email storage & a real refresh-logout bug fix
(Email Invitation & Session Persistence Fix Specification)

Two independent fixes:

* **Sender identity** (§1.1/§3): `backend/core/config.py` gained `email_from_name`, used via
  `email.utils.formataddr` in `email_service.send_email` to produce a proper `"LOOP-MIND
  Recruiting <demo@...>"` From header — configured entirely independently of the recipient, never
  derived from or dependent on the student's own email.
* **Non-destructive resume-email storage** (§2 "must not replace an existing valid student email
  unnecessarily"): `student_profile_service.apply_resume_extraction` previously overwrote
  `StudentProfessionalLinks.resume_extracted_email` unconditionally on every resume upload,
  including clearing it to `None` when a later re-upload's extraction simply didn't happen to
  state an email. It now only ever *sets* the field when a new extraction actually finds one —
  the same "Failed Extraction Rule" precedent already established for skills/certifications/
  projects — so a valid, previously found resume email is never silently lost.
* **Real root cause of the reported "refresh logs me out" bug**: `frontend/src/lib/auth.tsx`'s
  `AuthProvider` restoration effect treated *any* failure from `GET /api/auth/me` — including a
  transient network failure to even reach the backend (e.g. a dev-server `--reload` restart
  landing exactly during a page refresh, which happens routinely in this project's own workflow)
  — as an invalid session, and deleted the stored token. That's the bug: a perfectly valid,
  non-expired token was being permanently destroyed by a momentary connectivity blip, not by an
  actual authentication failure. Investigation (`backend/routes/auth.py`'s `/me`, `backend/auth/
  dependencies.py`'s token decoding, `frontend/src/lib/api.ts`'s `localStorage`-backed token
  storage, and `RequireRole`'s wait-during-loading behavior) confirmed the rest of the
  session-persistence architecture — token storage, startup restoration, protected-route
  waiting — was already implemented correctly per this spec's §4/§5. The fix only changes the
  failure-handling branch: the token is now cleared only on an actual `401` response from the
  server (a genuinely invalid/expired session); any other failure gets one short retry, and if
  still unreachable, the user sees the landing page for that load without their stored token
  being destroyed — so the very next successful refresh restores their session normally.

## UPDATE — Real demo mailbox configured; test suite isolated from local email credentials
(Authentication Session Persistence & Complete Interview Invitation Email Pipeline SDD)

Both the session-persistence architecture and the full interview→email pipeline had already been
verified correct in the two prior updates above; this closes the one remaining gap — actual SMTP
credentials — and fixes a test-isolation defect that configuring them exposed:

* A real Gmail account + app password were configured in the developer's local `.env`
  (`EMAIL_HOST`/`EMAIL_PORT`/`EMAIL_USERNAME`/`EMAIL_PASSWORD`/`EMAIL_FROM`/`EMAIL_FROM_NAME`),
  never committed (`.env` is gitignored) and never exposed to the frontend.
* **Verified live against the running dev server**: approving a real test application produced
  `email_status: "sent"` with the correct resolved recipient and no error — confirming the entire
  chain (`approve_candidate` → `generate_questions_for_approval` → `send_invitation_email` →
  `resolve_recipient_email` → `EmailAgent.generate_interview_invitation` →
  `email_service.send_email`) genuinely delivers an email end to end, not just a status flag.
* **Test-isolation bug found and fixed**: several of the email tests added in the prior update
  (`backend/tests/test_interviews.py`) didn't explicitly force `settings`'s email fields empty —
  they relied on the ambient environment having no email configuration. Once real credentials
  existed in `.env`, `test_approval_resolves_profile_email_and_reports_transport_not_configured`
  broke, and — more seriously — every email-resolution test would have attempted a real SMTP
  connection to the developer's actual mailbox on every `pytest` run. Fixed with an `autouse`
  fixture in `backend/tests/conftest.py` (`_no_real_email_transport`) that forces email transport
  "not configured" for every test by default; the one test that specifically exercises a real send
  explicitly re-patches those fields itself and mocks `smtplib.SMTP`, so it's still the only test
  that simulates an actual send.

---

# 23. PHASE 16 — STUDENT APPLICATION OUTCOME & CLOSED-LOOP INTELLIGENCE

## Goal

Complete the two-way learning loop.

## Approved path

```text
Recruitment Outcome
       ↓
Future Recruitment Intelligence
```

## Not-approved path

```text
Skill Gaps
    ↓
Improved Preparation
    ↓
Updated Profile
```

## Complete closed loop

```text
Company Intelligence
        ↓
Student Profile
        ↓
Skill & Evidence Analysis
        ↓
Placement Readiness
        ↓
Skill Gaps
        ↓
Preparation Plan
        ↓
Student Improvement
        ↓
Job Application
        ↓
AI Recruitment
        ↓
Human Approval
      ↙       ↘
 Approved   Not Approved
     ↓           ↓
 Interview    Skill Gaps
     ↓           ↓
 Outcome    Re-prepare
      \         /
       \       /
     Updated Intelligence
            ↓
      Future Students
            ↺
```

## Historical intelligence

Recruitment outcomes contribute to:

* company intelligence;
* historical recruitment patterns;
* successful-candidate characteristics;
* future analysis.

## Placed-student knowledge

Successfully placed students may voluntarily share:

* preparation strategies;
* interview experiences;
* assessment topics;
* resources;
* lessons learned.

Personal information requires consent.

Institutional intelligence may be anonymized/aggregated.

## Done when

Both approved and not-approved recruitment outcomes can contribute to the appropriate future intelligence loop.

## UPDATE — Historical signal now also learns from not-selected candidates (Recruiter Portal
Dashboard/Job Management/Candidate Evaluation & Closed-Loop ML Workflow SDD §17-20)

`recruitment_ai_service.py`'s `_historical_signal` (the read-only, ai_score-neutral note shown
alongside a candidate's AI match result, e.g. "3 previously hired candidates for Data Engineer
also had: SQL, Python.") previously only ever looked at this recruiter's own *hired* interview
outcomes for the same job role — a real instance of "the ML system must not learn only from
successful candidates." It now also considers the same recruiter's *not-selected* outcomes for
that role, surfacing a second sentence when the current candidate shares matched skills with
previously-rejected candidates too — still purely informational, never adjusting `ai_score`, and
still scoped to the current recruiter's own historical outcomes (never another recruiter's).

---

# 24. PHASE 17 — RECRUITMENT ANALYTICS & HISTORICAL INTELLIGENCE

## Goal

Build the specified analytics layer.

## Recruiter analytics

Must support the defined areas:

* recruitment analytics;
* candidate outcomes;
* skill trends;
* recruitment-stage trends;
* historical company patterns;
* successful-candidate characteristics;
* student skill-gap trends.

## Recharts

Use the defined chart system.

Do not introduce unrelated chart colors.

## Dynamic rule

All statistics and charts derive from stored project data.

No permanent screenshot values.

## Historical data

Historical records must remain usable for:

* company intelligence;
* recruitment pattern analysis;
* outcome analysis;
* skill-gap pattern analysis.

## ML support

The specification defines scikit-learn use for:

* recruitment pattern analysis;
* candidate/job feature analysis;
* readiness-related prediction;
* historical recruitment analysis;
* candidate matching support;
* outcome analysis;
* skill-gap pattern analysis.

ML supports the AI system rather than unnecessarily replacing LangChain agents.

## DL

PyTorch may be used where learned representations/models provide value beyond conventional ML.

Do not invent a DL feature not supported by the specification.

## Done when

Specified analytics and historical intelligence are dynamically calculated from stored recruitment data.

---

# 25. PHASE 18 — MY PROFILE / STUDENT PROGRESS

## Goal

Build the student's self-service profile/progress experience defined by the current LOOP-MIND specification.

## Dynamic source

All student information must come from the authenticated student's actual stored profile.

## Profile relationship

```text
Student
 ├── Profile
 ├── Skills
 ├── Projects
 ├── Certifications
 ├── Resume
 ├── Evidence
 └── Progress
```

## Progress

Retain:

* current progress;
* preparation-plan history;
* relevant plan-change history.

## Editable/read-only behavior

Only fields explicitly defined as editable by the current LOOP-MIND specification may become editable.

Do not make unspecified fields editable.

Do not invent additional profile functionality.

## Done when

The student's profile and progress information are dynamic and correctly connected to the existing intelligence and preparation systems.

## UPDATE — Locked fields, single Save Changes, working resume/public-profile actions
(Student My Profile Page SDD)

Full Name, Degree, College/University and Branch/Department are now all locked read-only —
College/Branch join the two that were already protected, and the enforcement is server-side
(`student_profile_service.upsert_academic_info` silently ignores those fields on an update, not
just a disabled input) so a later profile edit can never overwrite the verified academic record
those came from. The page's several independent inline "Save Changes" buttons were replaced by
one, pinned to the bottom-right footer, that commits whichever section(s) currently have unsaved
edits (each section keeps its own Edit/Cancel; Skills/Projects/Certifications/Coding
Experience/Consent already save immediately per action and were left untouched). Download
Resume is now active exactly when a valid resume exists — it was previously gated on having at
least one job application and, separately, wired to the profile photo instead of the resume —
and downloads the real stored PDF through a new authenticated `GET
/students/me/resume/file` endpoint. View Public Profile now opens a real read-only preview of
the student's own stored profile data (`/app/profile/public`) instead of a permanently disabled
placeholder.

## UPDATE — Visible profile photo, photo delete, full resume management (Skill Gap, Profile
Photo & Resume Management SDD)

The profile photo now actually renders next to the student's name — it previously showed a
literal "Photo" placeholder label instead of the image, through a new authenticated `GET
/students/me/basic-info/photo/file` endpoint (the stored photo, like the resume, is a server
filesystem path with no other safe browser-reachable route). "Delete Photo"
(`DELETE /students/me/basic-info/photo`) is now available whenever a photo exists, clearing
only the photo reference — uploading afterward works exactly like the first upload. Professional
Links & Resume's Resume field gained full management (Upload when none exists, Replace,
Download, Delete via a new `DELETE /students/me/resume`) through the same endpoint and Resume
Parser Agent workflow the Dashboard's own resume card uses, so there is exactly one active
resume record regardless of which page last touched it. Delete Photo touches no other stored
profile data. **Superseded** by the Resume Lifecycle UPDATE SDD below regarding Delete Resume:
it was originally scoped to clear only the file reference, leaving resume-derived skills/
projects/certifications untouched — corrected there.

## UPDATE — Delete Resume now removes its resume-derived data; project extraction no longer
miscounts a technology line as a project (Resume Lifecycle, Exact Resume Parsing, Source-Aware
Counts & Agent Cross-Check SDD)

`DELETE /students/me/resume` now also removes every skill/project/certification still tagged
`source="resume"` (never independently confirmed by the student or LinkedIn since), the same way
a resume *replacement* removes what the old version contributed — deleting a resume is a
deliberate action with no "did parsing fail" ambiguity, so `apply_resume_extraction`'s
empty-extraction guard doesn't apply here; `reconcile_resume_derived_records(db, student_id, {})`
is called unconditionally, and a Skill Gap recalculation runs immediately if a target is set.
Manually entered and LinkedIn-derived data is never touched. Separately, `resume_parser_agent.py`'s
`_extract_from_text` previously treated every non-empty line in a resume's Projects section as
its own project — so a "Technologies: React, Node.js, MongoDB" attribute line under a project
title became a fake extra project. A new `_parse_projects` now recognizes attribute-prefixed
lines (Technologies/Tech Stack/Tools/Stack/Description/Role) as belonging to the *current*
project (technologies feed the project's own `technologies_used`) rather than starting a new
one — three real resume projects now extract as three, not eight.

## UPDATE — Unlabeled project description lines no longer counted as separate projects
(Resume Parsing, Project Counting, Replacement & Recruitment-Agent Integration Correction
Specification)

The previous fix only handled *explicitly labeled* attribute lines ("Technologies: ..."). An
unlabeled prose description directly under a project title — no blank line, no "Description:"
prefix, e.g. "Project A" followed immediately by "Built a full-stack e-commerce platform with
payment integration." — still became its own fake project. `_split_resume_sections` now
preserves blank lines within a section as boundary markers, and `_parse_projects` uses that
signal plus a short heuristic (`_looks_like_project_title`: no blank line since the last title,
and the line reads like prose — many words or ends in "."/"!") to treat such a line as the
current project's description instead of a new project. A compact one-title-per-line list with
no descriptions still correctly produces one project per line.

---

# 26. PHASE 19 — COMPLETE MOBILE APPLICATION

## Goal

Bring the specified LOOP-MIND product to the React Native application.

## Technology

```text
React Native
TypeScript
React Navigation
```

## Critical architecture rule

Use the same backend/API.

Do not create:

* second backend;
* duplicate business logic;
* separate database logic;
* mobile-only product features.

## Mobile must consume

```text
Same Backend
Same Database
Same AI Services
Same Business Rules
Same Authorization
```

## Required mobile behavior

Where specified, reproduce the same product behavior for:

* authentication;
* OTP;
* student profile;
* student dashboard;
* Skill Gap;
* Preparation Plan;
* Jobs;
* applications;
* recruiter workflows where the mobile scope defines them;
* protected information;
* progress.

## Mobile visual rule

Use the LOOP-MIND visual language.

Do not create a separate mobile product theme.

## Mobile protection

Apply the specified mobile screenshot/screen-capture protection where the specification defines it and where technically supported.

Do not claim universal device-level screenshot prevention.

## Done when

The mobile application consumes the same backend and implements the defined product behavior without creating a second architecture.

---

# 27. PHASE 20 — WEBSITE RESPONSIVE & VISUAL COMPLETION

## Goal

Perform the final website visual/responsive implementation pass.

## No new product features

This phase is not for feature expansion.

## Test viewports

* desktop;
* tablet;
* mobile-browser viewport.

## Verify every page

* Landing/public;
* authentication;
* Student Dashboard;
* Skill Gap;
* Preparation Plan;
* Jobs;
* My Profile/Progress;
* Recruiter Dashboard;
* Recruiter Jobs;
* Recruiter Candidates;
* Recruiter Interviews;
* analytics;
* AI workflow views;
* modals;
* tables;
* forms.

## Verify

* exact background;
* exact color tokens;
* typography;
* card system;
* buttons;
* inputs;
* badges;
* tables;
* modal system;
* React Flow;
* charts;
* footer;
* navigation;
* spacing;
* alignment;
* no unintended horizontal overflow.

## Critical layout rule

Responsive behavior may adapt the layout where the specification permits it.

It must not change the intended information architecture.

The authoritative desktop reference remains authoritative.

## Done when

All website pages preserve their required reference structure and operate correctly across supported viewport sizes.

---

# 28. PHASE 21 — SECURITY & AUTHORIZATION AUDIT

## Goal

Audit the implementation against the actual LOOP-MIND specification.

This is an audit phase.

Do not invent generic security requirements.

## Verify

### Authentication

```text
OTP
 ↓
JWT
```

### Student authorization

Protected student endpoints require valid authentication.

### Recruiter authorization

Recruiter-only functionality is protected.

### Portal isolation

Student cannot access Recruiter functionality.

Recruiter cannot access Student functionality outside defined shared flows.

### Data isolation

Students see their own:

* applications;
* application results;
* profile;
* preparation;
* progress.

Recruiters see their own recruitment records.

### Protected information

Protected information must not be returned to unauthorized clients.

### Dynamic-data protection

No unauthorized endpoint may expose protected data.

### AI/human boundary

AI recommendation must not bypass human approval.

### Database

Required relationships and uniqueness constraints must be enforced.

## Do not add

* unspecified authentication;
* password system;
* unrelated security products;
* unnecessary infrastructure.

## Done when

The implementation passes the specification-defined authorization and data-protection checks.

---

# 29. PHASE 22 — AI / ML / DL EVALUATION & WORKFLOW VERIFICATION

## Goal

Verify the intelligence architecture itself.

## Verify exactly 13 agents

```text
1. Company Intelligence Agent
2. Student Skill Analysis Agent
3. Placement Readiness Agent
4. Skill-Gap Analysis Agent
5. Preparation Plan Agent
6. What-If Analysis Agent

7. Resume Parser Agent
8. Embedding Agent
9. Matching Agent
10. Shortlisting Agent
11. Interview Agent
12. Email Agent

13. LinkedIn Profile Extraction Agent (UPDATE SDD §6-9 — Create Account
    Basic Information's optional LinkedIn-assisted path)
```

No unnecessary agent may be introduced. All 13 agents implement Python +
LangChain `create_agent` + Google Gemini 2.5 Flash (agents/llm.py), per
the UPDATE SDD "AI Agent Code Format Standardization".

## Verify Multi-Agent System 1

```text
Company Intelligence
      ↓
Student Skill Analysis
      ↓
Placement Readiness
      ↓
Skill Gap
      ↓
Preparation Plan
      ↓
What-If
```

## Verify Multi-Agent System 2

```text
Resume Parser
      ↓
Embedding
      ↓
Matching
      ↓
Shortlisting
      ↓
Human Approval
      ↓
Interview
      ↓
Email
```

## Verify RAG

```text
Data
 ↓
Processing
 ↓
Embeddings
 ↓
Qdrant
 ↓
RAG
 ↓
LangChain
 ↓
Agents
```

## Verify RAG knowledge sources

* company recruitment history;
* job requirements;
* successful candidate characteristics;
* student evidence;
* historical recruitment outcomes;
* assessment topics;
* interview information;
* preparation resources;
* skill-gap knowledge.

## Verify ML/DL boundary

ML:

```text
scikit-learn
pandas
NumPy
```

DL:

```text
PyTorch
```

No ML/DL model may silently replace a defined agent workflow.

## Done when

The complete AI architecture conforms to the fixed architecture and exactly 12 specialized agents exist.

## UPDATE — ML/DL Training Architecture (ML/DL Training Architecture SDD)

The `ML and DL/` directories (`datasets/`, `preprocessing/`, `ml/`, `dl/`,
`models/`, `evaluation/`) are no longer empty placeholders — they are
populated with a real, runnable pipeline that trains exclusively on
LOOP-MIND's own accumulated recruitment history, never on manually invented
or supplied data:

```text
Database -> Dataset Generation -> Preprocessing -> ML Training ->
Evaluation -> Validated Model (only if it earns acceptance) -> models/
```

* `datasets/dataset_generation/generate_recruitment_dataset.py` reads the
  application's own database directly (`backend.core.database`,
  `backend.models.jobs`, `backend.models.student_profile`) and exports one
  row per job application to `datasets/raw/recruitment_history.csv`. An
  application still in progress is exported with `final_outcome=None` and
  never assigned a fabricated outcome.
* `preprocessing/dataset_preparation/prepare_features.py` cleans, normalizes,
  and derives features (skill match ratio, AI status one-hot, etc.) into
  `datasets/processed/recruitment_features.csv`. Only applications with a
  *concluded* outcome (both hired/success and rejected/failure — never
  success-only) become labeled training rows. The same feature derivation is
  reused for inference so training and inference never diverge.
* `ml/training/train_outcome_model.py` trains a scikit-learn model
  (logistic regression or random forest) to predict recruitment outcome.
  It refuses to train — reporting `insufficient_data` instead of producing a
  meaningless model — unless at least 10 concluded examples of *both*
  outcome classes exist.
* `evaluation/metrics/evaluate.py` computes accuracy/precision/recall/F1 and
  gates model acceptance: a model below 60% accuracy is rejected, and a
  newly trained model that doesn't beat the currently validated model's
  accuracy is rejected too — a previously validated model is never silently
  replaced by a worse one.
* `models/model_store.py` persists an accepted model's artifact and metadata
  only after it passes the evaluation gate above.
* `dl/` remains intentionally unused — the current recruitment history is
  nowhere near large/complex enough to justify deep learning over the `ml/`
  model above, consistent with "Verify ML/DL boundary" §29 not requiring
  every problem to use ML, let alone DL.
* `run_training_pipeline.py` orchestrates the full loop end to end
  (`python "ML and DL/run_training_pipeline.py"`) and was verified against
  both the real dev database (correctly reports `insufficient_data` — the
  dev DB has 1 application and 0 concluded outcomes) and a synthetic 60-row
  dataset (correctly trains, evaluates, accepts, saves, and reloads a
  model). No unrelated database table was turned into a training feature —
  only the recruitment-outcome dataset above has a defined training schema.

---

# 30. PHASE 23 — FULL END-TO-END SYSTEM TESTING

## Goal

Test the complete LOOP-MIND system.

No new features.

## Complete Student Intelligence flow

```text
Authentication
      ↓
Student Profile
      ↓
Target Company / Role
      ↓
Company Intelligence
      ↓
Student Skill Analysis
      ↓
Placement Readiness
      ↓
Skill Gap
      ↓
What-If
      ↓
Preparation Plan
      ↓
Student Improvement
```

## Complete recruitment flow

```text
Student
   ↓
Jobs
   ↓
Application
   ↓
Resume
   ↓
Resume Parser
   ↓
Embedding
   ↓
Matching
   ↓
AI Shortlisting
   ↓
Recruiter Review
   ↓
Human Approval
   ↓
Interview Agent
   ↓
Email Invitation
   ↓
Interview
   ↓
Outcome
```

## Closed-loop test

```text
Recruitment Outcome
       ↓
Student
       ↓
Skill Gap
       ↓
Preparation
       ↓
Improvement
       ↓
Future Intelligence
```

## Test cases

### Student

* registration/authentication;
* profile data;
* target company;
* target role;
* skill analysis;
* readiness;
* skill gaps;
* What-If;
* preparation plan;
* plan versioning;
* jobs;
* search;
* filters;
* save;
* application;
* application result;
* profile;
* progress.

### Recruiter

* authentication;
* dashboard;
* job creation;
* dynamic job list;
* job search;
* candidate list;
* candidate filters;
* AI evaluation;
* workflow visualization;
* human approval;
* disapproval;
* interview;
* generated questions;
* invitation;
* interview status;
* analytics.

### AI

* all 12 agents;
* both multi-agent systems;
* RAG;
* Qdrant;
* embeddings;
* AI status;
* human approval boundary;
* failure states.

### Dynamic data

Test:

* no records;
* one record;
* multiple records;
* updated records;
* changed student data;
* changed company data;
* changed job data;
* changed application state.

### Reference UI

Test:

* card position;
* card ordering;
* text placement;
* button placement;
* table position;
* filter placement;
* search placement;
* footer;
* navbar;
* spacing;
* alignment.

---

# 31. PHASE 24 — FINAL SPECIFICATION COMPLIANCE AUDIT

## Goal

Final authority check.

Nothing more.

Nothing less.

## Audit every requirement

Compare implementation against the complete `spec.md`.

Audit:

* architecture;
* pages;
* routes;
* UI;
* reference layouts;
* data;
* databases;
* APIs;
* authentication;
* authorization;
* AI;
* agents;
* RAG;
* Qdrant;
* ML;
* DL;
* applications;
* recruitment workflow;
* human approval;
* interviews;
* outcomes;
* closed loop;
* analytics;
* mobile;
* responsive behavior;
* dynamic-data requirements.

## Search codebase for unsupported additions

Check for unsupported:

* password authentication;
* social login;
* invented workflows;
* invented fields;
* invented filters;
* invented navigation;
* invented AI agents;
* invented compatibility scores;
* invented personality matching;
* unsupported ranking algorithms;
* unnecessary technologies;
* MongoDB;
* Redis;
* n8n in the core architecture;
* additional vector databases;
* unnecessary microservices;
* payment functionality;
* unsupported deployment functionality;
* hardcoded production data;
* hardcoded screenshot values;
* Student/Recruiter portal leakage;
* AI final-decision logic.

## Important

Do not remove something merely because it looks unusual.

First verify whether `spec.md` requires it.

## Final result

Produce:

```text
SECTION | STATUS | ISSUES | FIXES
```

for all applicable specification sections.

Then provide:

* final PASS/FAIL;
* remaining undefined items;
* remaining blockers;
* files modified;
* tests performed;
* unsupported functionality removed;
* final compliance status.

---

# 32. PHASE COMPLETION REQUIREMENT

Every phase must finish with:

```text
PHASE: [number and name]

STATUS:
PASS / FAIL

FILES CREATED:
- ...

FILES MODIFIED:
- ...

FILES DELETED:
- ...

CURRENT-PHASE REQUIREMENTS IMPLEMENTED:
- ...

CURRENT-PHASE REQUIREMENTS VERIFIED:
- ...

TESTS PERFORMED:
- ...

TESTS PASSED:
- ...

TESTS FAILED:
- ...

ISSUES FOUND:
- ...

ISSUES FIXED:
- ...

POST-IMPLEMENTATION SPEC CROSS-CHECK:
PASS / FAIL

PHASE.MD CROSS-CHECK:
PASS / FAIL

MISSED CURRENT-PHASE REQUIREMENTS RECOVERED:
- None
or
- ...

FUTURE-PHASE FEATURES IMPLEMENTED EARLY:
NONE

REMAINING ISSUES:
- ...

PHASE COMPLETE:
YES / NO

NEXT PHASE:
DO NOT START AUTOMATICALLY.
WAIT FOR EXPLICIT NEXT-PHASE INSTRUCTION.
```

---

# 33. FINAL DEFINITIVE BUILD ORDER

```text
00  Specification Lock & Repository Inspection
01  Project Foundation & Global Design System
02  Landing / Public Entry
03  Authentication & Role Separation
04  Master Data & Company Intelligence Data Layer
05  Student Profile, Skills & Evidence
06  Student Intelligence Multi-Agent System
07  Student Dashboard
08  Skill Gap Analysis & What-If
09  Preparation Plan
10  Student Jobs & Application System
11  Recruiter Portal Foundation & Dashboard
12  Recruiter Job Management
13  Recruiter Candidates & Recruitment AI
14  Human Approval & Recruitment Outcome
15  Interview Agent, Interviews & Email Agent
16  Student Application Outcome & Closed-Loop Intelligence
17  Recruitment Analytics & Historical Intelligence
18  My Profile / Student Progress
19  Complete Mobile Application
20  Website Responsive & Visual Completion
21  Security & Authorization Audit
22  AI / ML / DL Evaluation & Workflow Verification
23  Full End-to-End System Testing
24  Final Specification Compliance Audit
```

---

# 34. EXACT AI AGENT BUILD TIMING

The agents must **not all be built at the beginning**.

Their implementation belongs to the phases where their required data and workflow become available.

```text
PHASE 06
│
├── Company Intelligence Agent
├── Student Skill Analysis Agent
├── Placement Readiness Agent
├── Skill-Gap Analysis Agent
├── Preparation Plan Agent
└── What-If Analysis Agent


PHASE 13
│
├── Resume Parser Agent
├── Embedding Agent
├── Matching Agent
└── Shortlisting Agent


PHASE 15
│
├── Interview Agent
└── Email Agent
```

The human approval checkpoint is not an AI agent.

It remains a recruiter-controlled step.

The complete AI architecture therefore becomes:

```text
                  LOOP-MIND AI
                       │
          ┌────────────┴────────────┐
          │                         │
          ↓                         ↓
 STUDENT INTELLIGENCE        AI RECRUITMENT
   MULTI-AGENT SYSTEM        MULTI-AGENT SYSTEM
          │                         │
       6 Agents                  6 Agents
          │                         │
          └────────────┬────────────┘
                       ↓
                    12 TOTAL
                       ↓
                  CLOSED LOOP
```

---

# 35. EXACT TECHNOLOGY ARCHITECTURE

```text
                    LOOP-MIND
                        │
        ┌───────────────┴────────────────┐
        │                                │
        ↓                                ↓
 Student Portal                    Recruiter Portal
        │                                │
        └───────────────┬────────────────┘
                        ↓
                  React + TypeScript
                        │
                      Vite
                        │
             Tailwind + shadcn/ui
                        │
              React Flow + Recharts
                        │
                        ↓
                  Python Backend
                        │
                     FastAPI
                        │
              Pydantic + SQLAlchemy
                        │
             ┌──────────┴──────────┐
             ↓                     ↓
          SQLite                AI Layer
             │                     │
             │                  LangChain
             │                     │
             │              ┌──────┴──────┐
             │              ↓             ↓
             │             RAG          Agents
             │              │             │
             │           Qdrant       12 Agents
             │              │
             │        Sentence Transformers
             │
             └──────────────┬──────────────┐
                            ↓              ↓
                       ML / Analytics     DL
                       scikit-learn      PyTorch
                            │              │
                            └──────┬───────┘
                                   ↓
                       Recruitment Intelligence
```

---

# 36. FINAL CLOSED-LOOP ARCHITECTURE

```text
                    COMPANY INTELLIGENCE
                            ↓
                    STUDENT PROFILE
                            ↓
                 SKILL & EVIDENCE ANALYSIS
                            ↓
                   PLACEMENT READINESS
                            ↓
                       SKILL GAPS
                            ↓
                   PREPARATION PLAN
                            ↓
                   STUDENT IMPROVEMENT
                            ↓
                     JOB APPLICATION
                            ↓
                    RESUME PROCESSING
                            ↓
                        EMBEDDING
                            ↓
                        MATCHING
                            ↓
                    AI SHORTLISTING
                            ↓
                    RECRUITER REVIEW
                            ↓
                    HUMAN APPROVAL
                       ↙          ↘
                 APPROVED       DISAPPROVED
                    ↓               ↓
             INTERVIEW AGENT    SKILL GAPS
                    ↓               ↓
              EMAIL INVITE      PREPARATION
                    ↓               ↓
                INTERVIEW       IMPROVEMENT
                    ↓               ↓
                 OUTCOME ───────────┘
                    ↓
          FUTURE RECRUITMENT
              INTELLIGENCE
                    ↓
            COMPANY INTELLIGENCE
                    ↺
```

---

# 37. NON-NEGOTIABLE IMPLEMENTATION PRINCIPLES

```text
SPECIFICATION
     ↓
DESIGN
     ↓
DATA / LOGIC
     ↓
CODE
     ↓
TEST
     ↓
COMPLIANCE
```

Never:

```text
CODE
 ↓
ASSUMPTION
 ↓
CHANGE SPEC
```

Never implement a future phase early.

Never invent an undefined requirement.

Never turn reference/demo values into production data.

Never replace dynamic data with hardcoded values.

Never redesign an authoritative reference page.

Never move a reference card merely because another arrangement appears cleaner.

Never replace a specified table with cards.

Never replace specified cards with a different component.

Never change the global visual language.

Never introduce a second Student/Recruiter visual language.

Never allow AI to make the final critical recruitment approval.

Never create more than the specified 12 AI agents.

Never create a second vector database.

Never add MongoDB.

Never add Redis.

Never add n8n to the core architecture.

Never create a second backend.

Never create separate mobile business logic.

Never silently delete historical preparation plans.

Never expose protected data merely by hiding it in the frontend.

---

# 38. FINAL STOP RULE

After each phase:

```text
IMPLEMENT
   ↓
RUN
   ↓
TEST
   ↓
READ COMPLETE SPEC
   ↓
READ COMPLETE PHASE
   ↓
CROSS-CHECK
   ↓
RECOVER MISSED CURRENT REQUIREMENTS
   ↓
RUN AGAIN
   ↓
TEST AGAIN
   ↓
VERIFY FUTURE FEATURES NOT IMPLEMENTED
   ↓
REPORT
   ↓
STOP
```

The next phase begins **only after an explicit instruction to begin it**.

The phase document must never authorize the coding agent to automatically continue to the next phase.

---

# 39. SINGLE SOURCE OF TRUTH FINAL STATEMENT

`spec.md` defines what LOOP-MIND is.

`phase.md` defines when each already-specified requirement is implemented.

The reference images define the layout wherever the LOOP-MIND specification declares them authoritative.

The code must conform to both.

```text
LOOP-MIND SPECIFICATION
          ↓
REFERENCE LAYOUT
          ↓
PHASE
          ↓
IMPLEMENTATION
          ↓
TESTING
          ↓
COMPLIANCE
```

**One phase at a time.**

**Specification first.**

**Code second.**

**No hallucinated requirements.**

**No silent scope expansion.**

**No future-phase leakage.**

**No redesign of authoritative reference layouts.**

**No hardcoded production data.**

**No AI final recruitment decision without human approval.**

**Exactly 12 specialized AI agents.**

**Two functional multi-agent systems.**

**One overall closed-loop intelligence system.**

**Stop after every phase.**
## STRICT PHASE GATE — MUST PASS BEFORE NEXT PHASE

CURRENT PHASE ONLY: Compare the implementation against the complete `spec.md` and `phase.md`. Identify every missing, incorrect, unauthorized, or extra CURRENT-PHASE requirement. Fix every CURRENT-PHASE issue, run the application, test again, and re-read both documents completely. Repeat until the CURRENT PHASE is fully compliant. Do NOT implement FUTURE-PHASE requirements even if discovered during the audit. The next phase is allowed ONLY after the CURRENT PHASE passes this cross-check with no remaining CURRENT-PHASE issues.
