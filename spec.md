# LOOP-MIND — SINGLE SOURCE OF TRUTH
## Specification-Driven Development — Code Second

**Document role:** Complete development specification derived from the uploaded LOOP-MIND MASTER PRODUCT SPECIFICATION.

**Development rule:** Specification → Design → Data/Logic → Code → Testing.

**Source boundary:** This document does not add requirements, functionality, UI elements, datasets, flows, technologies, or assumptions that are not present in the LOOP-MIND source specification.

**Reference-document role:** The uploaded ADVAITA MATRIMONY specification was used only as the requested example of specification-driven structure and strictness. Its product requirements, visual system, routes, terminology, and functionality are not imported into LOOP-MIND.

**Important:** Where the LOOP-MIND source explicitly states that a detail is undefined, it remains undefined. Where the source marks reference/demo values as non-production data, they remain reference-only. Dynamic data requirements remain dynamic.

---

# MASTER BUILD RULES

1. Specification is the source of truth.
2. Code is written only after the applicable specification is established.
3. Do not invent unspecified functionality.
4. Do not create alternative flows.
5. Do not introduce a second visual theme.
6. Do not hardcode member/student/recruiter-specific production data.
7. Preserve supplied reference-page structure, hierarchy, placement, spacing, buttons, cards, navigation, and footer wherever the source declares the reference authoritative.
8. Keep reference/demo values separate from real application data.
9. Required datasets and dropdown data must be available and dynamically loaded according to the source requirements.
10. User-provided datasets/options have priority over generated development data.
11. Generated development data must be contextual, meaningful, logically consistent, and replaceable.
12. Undefined behaviour remains undefined until explicitly specified.
13. AI does not make the final critical recruitment approval; the recruiter performs the human approval checkpoint.
14. Student and Recruiter portals are functionally separated even though they share the LOOP-MIND visual system.
15. The visual system must not drift during implementation.

---

# COMPLETE SOURCE SPECIFICATION

The following is the complete source specification, preserved page-by-page so that no requirement is silently omitted or reinterpreted.

## SOURCE PAGE 1

LOOP-MIND MASTER PRODUCT SPECIFICATION 
# LOOP-MIND — Complete Project Specification 
 
## 1. What You Are Going to Build 
 
**LOOP-MIND — an AI Recruitment Agent and Closed-Loop Campus Recruitment Intelligence 
Platform.** 
 
--- 
 
# 2. Core Platform 
 
## 2.1 Company Intelligence 
 
- Store company- and role-specific recruitment history. 
- Track recruitment stages, assessments, required skills, technical concepts, and selected-candidate 
characteristics. 
- Learn how a company's recruitment process changes over time. 
- Detect recurring recruitment patterns. 
 
## 2.2 Student Profile & Skill Evidence 
 
- A student can create their profile from the beginning of their engineering journey. 
- Add: 
  - Skills they are learning 
  - Projects 
  - Certifications 
  - Academics 
  - Coding experience 
  - Other evidence 
- The system evaluates **evidence**, not just claimed skills.

## SOURCE PAGE 2

## 2.3 Company-Specific Placement Readiness 
 
- Student selects a target company and role. 
- LOOP-MIND compares the student's current skills and evidence with: 
  - Company requirements 
  - Historical recruitment data 
  - Successful candidate profiles 
  - Recruitment patterns 
  - Current job requirements 
- Show: 
  - What the student already knows 
  - What they still need to learn 
  - Missing evidence 
  - Skill gaps 
  - Current readiness/alignment 
  - Major reasons behind the assessment. 
 
## 2.4 Year-Aware Preparation Plan 
 
- Preparation depends on the student's current academic year. 
- **1st year:** longer-term fundamentals, learning, projects, and evidence building. 
- **2nd year:** deeper skills, projects, and technical preparation. 
- **3rd year:** company-focused skills, DSA, projects, assessments, and interview preparation. 
- **Final year:** focused placement and company-specific preparation. 
- Generate personalized short- and long-term preparation plans. 
 
## 2.5 Skill-Gap & What-If Analysis 
 
- Identify the highest-impact skills the student should improve. 
- Examples:

## SOURCE PAGE 3

- Improve DSA 
  - Strengthen SQL 
  - Build a backend project 
  - Improve a programming language 
  - Practice technical interviews 
- Allow students to ask: 
  - **"What should I improve first to become ready for Company X?"** 
- Prioritize improvements based on company and historical recruitment evidence. 
 
## 2.6 Student Improvement Loop 
 
```text 
Student learns 
      ↓ 
Builds projects/evidence 
      ↓ 
Updates profile 
      ↓ 
LOOP-MIND recalculates readiness 
      ↓ 
New skill gaps are identified 
      ↓ 
Preparation plan is updated 
      ↓ 
Student improves 
      ↓ 
Loop continues 
 
``` 
 
## 2.7 Public Job Application

## SOURCE PAGE 4

- When a student is ready, they can apply for an actual job. 
- Candidate opens a public job page. 
- Submits: 
  - Name 
  - Email 
  - Phone 
  - PDF resume 
- AI recruitment workflow automatically starts. 
 
## 2.8 AI Recruitment Workflow 
 
- **Resume Parser Agent** → extracts candidate information. 
- **Embedding Agent** → embeds resume/policy information into Qdrant. 
- **Matching Agent** → compares candidate with job and company requirements using RAG. 
- **Shortlisting Agent** → produces: 
  - Shortlisted 
  - Hold 
  - Rejected 
- Rules and thresholds come from `/specs`. 
 
## 2.9 Human Approval Checkpoint 
 
- AI does not make the final critical decision alone. 
- Recruiter reviews: 
  - Candidate score 
  - Evidence 
  - Matching factors 
  - AI evaluation 
- Recruiter approves or does not approve the candidate.

## SOURCE PAGE 5

## 2.10 If Candidate Is Approved 
 
- Workflow continues. 
- **Interview Agent** generates: 
  - Interview questions 
  - Evaluation criteria 
  - Rubrics 
- **Email Agent** generates the interview invitation. 
 
## 2.11 If Candidate Is Not Approved 
 
- Do not simply end the process. 
- Identify: 
  - Why the candidate was not approved 
  - Skill gaps 
  - Missing evidence 
  - What needs improvement 
- Feed those gaps back into the student's readiness system. 
- Update the preparation plan. 
- Student improves and can continue through the same loop. 
 
## 2.12 Two-Way Learning Loop 
 
**Approved student:** 
 
```text 
Recruitment Outcome 
        ↓ 
Future Recruitment Intelligence 
 
```

## SOURCE PAGE 6

**Not-approved student:** 
 
```text 
Skill Gaps 
    ↓ 
Improved Preparation 
    ↓ 
Updated Profile 
 
``` 
 
Both paths contribute to the overall LOOP-MIND intelligence loop. 
 
## 2.13 Placed-Student Knowledge 
 
Successfully placed students can voluntarily share: 
 
- Preparation strategies 
- Interview experiences 
- Assessment topics 
- Resources 
- Lessons learned 
 
Personal information requires consent. 
 
Institutional intelligence can be anonymized/aggregated. 
 
## 2.14 Closed-Loop Intelligence 
 
```text

## SOURCE PAGE 7

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
      ↓          ↓ 
  Interview   Skill Gaps 
      ↓          ↓ 
   Outcome    Re-prepare 
      ↓          ↓ 
      └────→ Updated Intelligence 
                    ↓ 
               Future Students 
                    ↺

## SOURCE PAGE 8

``` 
 
--- 
 
# 3. Recruiter Workspace 
 
- Recruiter signup/login. 
- Create jobs. 
- Define requirements. 
- Monitor candidates. 
- View candidate evaluations. 
- Inspect AI workflows. 
- Approve candidates. 
- Review recruitment analytics. 
 
## 3.1 Live AI Workflow Visualization 
 
Render the LangGraph workflow using React Flow. 
 
Show live node states: 
 
- Pending 
- Running 
- Completed 
- Failed 
- Paused 
- Approved 
- Rejected 
 
Recruiter can visually understand where every candidate is in the workflow.

## SOURCE PAGE 9

## 3.2 Analytics & Historical Intelligence 
 
- Recruitment analytics 
- Candidate outcomes 
- Skill trends 
- Recruitment-stage trends 
- Historical company patterns 
- Successful-candidate characteristics 
- Student skill-gap trends 
 
--- 
 
 
Absolutely. I have now treated the uploaded AgentHire — Graphite Ink theme as the strict 
visual/design single source of truth for the entire LOOP-MIND website. 
LOOP-MIND — MASTER VISUAL & STYLING SPECIFICATION 
1. Non-Negotiable Global Rule 
Every single page and route must use the same Graphite Ink visual system. 
Mandatory global background 
#0F1317 
This is the page background for every page, every route, and the React Flow canvas. 
There must not be: 
• 
Different page backgrounds 
• 
Light-mode pages 
• 
Random background colors 
• 
Page-specific color themes 
• 
Gradients replacing the background 
• 
White cards/pages unless explicitly permitted by the source 
• 
A separate visual language for Student Portal 
• 
A separate visual language for Recruiter Portal 
• 
A separate visual language for public job pages

## SOURCE PAGE 10

2. Exact Design Token System 
The following values are fixed. 
Background hierarchy 
Token 
Value 
Usage 
--bg 
#0F1317 
Page, all routes, React Flow canvas 
--chrome #12171B 
Sidebar, footer, table head, chart wells 
--surface #161C21 
Cards, panels, table rows 
--row-alt #1A2126 
Zebra table rows 
--raised #1D242A 
Inputs, menus, popovers, modals, hover 
--scrim 
rgba(9, 12, 14, 0.72) Modal overlay 
The background ladder must not be arbitrarily expanded. 
 
3. Exact Border System 
Token 
Value 
--border 
#232B31 
--border-hi #2C353B 
All standard borders must use these tokens rather than arbitrary colors. 
 
4. Exact Typography Colors 
Token 
Value 
Purpose 
--text 
#F2F5F4 Primary text 
--text-soft #C9D2CF Secondary/body text 
--text-mute #8A9591 Muted text 
The muted value is explicitly the lowest legible value on --surface. 
 
5. Exact Accent & State Colors

## SOURCE PAGE 11

Token 
Value 
--accent 
#6FD3C0 
--accent-soft #97E2D4 
--accent-deep #3F8478 
--accent-wash rgba(111, 211, 192, 0.14) 
--warn 
#E0A86B 
--warn-wash 
rgba(224, 168, 107, 0.14) 
--danger 
#E77E72 
--danger-wash rgba(231, 126, 114, 0.14) 
Color philosophy 
The visual system primarily uses the Graphite + Ink + Teal accent hierarchy. 
Charts specifically use shades of the accent instead of introducing unrelated hues. 
 
6. Typography System 
Primary font 
"Space Grotesk", Helvetica, Arial, sans-serif 
Monospace font 
"IBM Plex Mono", ui-monospace, monospace 
Base typography 
Element Size Weight 
Body 
15px Normal 
H1 
34px 600 
H2 
24px 600 
H3 
18px 600 
Headings use: 
• 
--text 
• 
letter-spacing: -0.02em 
• 
line-height: 1.15 
Body uses:

## SOURCE PAGE 12

• 
line-height: 1.55 
• 
text-wrap: pretty 
• 
antialiasing 
 
7. Exact Shape System 
Token 
Value 
--radius 
10px 
--radius-lg 14px 
Focus ring 0 0 0 3px rgba(111, 211, 192, 0.25) 
Component-specific radii defined by the source must also be preserved exactly—for example, 
buttons use 8px, navbar links 6px, and badges 6px. 
 
8. Global Application Shell 
The application shell is: 
┌───────────────────────────────────────────────────────┐ 
│                       NAVBAR                          │ 
├───────────────┬───────────────────────────────────────┤ 
│               │                                       │ 
│   SIDEBAR     │                 MAIN                  │ 
│               │                                       │ 
│               │                                       │ 
├───────────────┴───────────────────────────────────────┤ 
│                       FOOTER                          │ 
└───────────────────────────────────────────────────────┘ 
Exact shell: 
grid-template-columns: 224px 1fr 
grid-template-rows: auto 1fr auto 
 
grid-template-areas: 
"nav nav" 
"side main"

## SOURCE PAGE 13

"foot foot" 
Minimum height: 
100vh 
 
9. Responsive Rule 
At: 
max-width: 880px 
the layout becomes: 
"nav" 
"main" 
"foot" 
and: 
.sidebar { 
    display: none; 
} 
This responsive behavior applies globally. 
 
10. Navbar 
The navbar must: 
• 
Sit directly on the base background 
• 
Use --bg 
• 
Have a bottom border 
• 
Have no shadow 
• 
Have no tint 
• 
Remain sticky 
• 
Use z-index: 40 
Exact spacing: 
padding: 14px 20px 
gap: 22px 
Brand mark 
width: 22px

## SOURCE PAGE 14

height: 22px 
border-radius: 6px 
background: var(--accent) 
Logo rule 
Where the actual project logo is not supplied, the logo/mark may be generated automatically at 
implementation time, but it must visually belong to this Graphite Ink system. 
It must not introduce an unrelated color palette, gradient, visual style, or branding system. 
The supplied navbar mark specification remains authoritative for the navbar mark. 
 
11. Navigation Links 
Default: 
color: var(--text-mute) 
font-size: 13.5px 
padding: 7px 12px 
border-radius: 6px 
Hover: 
background: var(--surface) 
color: var(--text-soft) 
Active: 
background: var(--raised) 
color: var(--text) 
 
12. Sidebar 
The sidebar uses: 
background: var(--chrome) 
border-right: 1px solid var(--border) 
with: 
padding: 16px 12px 
gap: 4px 
Sidebar labels 
• 
IBM Plex Mono

## SOURCE PAGE 15

• 
10px 
• 
Uppercase 
• 
Letter spacing 0.12em 
• 
--text-mute 
Sidebar items 
Default: 
color: var(--text-soft) 
font-size: 13.5px 
Hover: 
background: var(--surface) 
color: var(--text) 
Active: 
background: var(--accent) 
color: var(--bg) 
font-weight: 500 
 
13. Main Content 
background: var(--bg) 
padding: 24px 
gap: 18px 
display: flex 
flex-direction: column 
Therefore, all page content begins on the Graphite Ink base, with surfaces layered above it. 
 
14. Footer 
Footer: 
background: var(--chrome) 
border-top: 1px solid var(--border) 
padding: 16px 20px 
font-size: 12px 
color: var(--text-mute)

## SOURCE PAGE 16

Links remain muted and become --text-soft on hover. 
 
15. Cards 
Standard cards: 
background: var(--surface) 
border: 1px solid var(--border) 
border-radius: 14px 
padding: 20px 
gap: 14px 
Flat cards 
background: var(--chrome) 
Card grid 
repeat(auto-fit, minmax(280px, 1fr)) 
gap: 16px 
 
16. Statistics 
Stats use: 
background: var(--surface) 
border: 1px solid var(--border) 
border-radius: 10px 
padding: 14px 
gap: 6px 
Labels: 
• 
IBM Plex Mono 
• 
10px 
• 
Uppercase 
• 
Letter spacing 0.1em 
• 
Muted 
Values: 
24px 
font-weight: 600

## SOURCE PAGE 17

Accent values use --accent. 
 
17. Buttons 
Every button must follow the defined button system. 
Base: 
display: inline-flex 
align-items: center 
gap: 8px 
padding: 9px 14px 
border-radius: 8px 
font: 500 13.5px/1 var(--font-sans) 
Transition: 
120ms ease 
Primary 
background: var(--accent) 
color: var(--bg) 
Hover: 
background: var(--accent-soft) 
Ghost 
background: transparent 
color: var(--text-soft) 
border-color: var(--border-hi) 
Hover: 
background: var(--raised) 
color: var(--text) 
Danger 
background: var(--danger-wash) 
color: var(--danger) 
border-color: var(--danger) 
Disabled: 
opacity: 0.45

## SOURCE PAGE 18

cursor: not-allowed 
Auto-generated buttons 
Any buttons required by a page but not explicitly described in a supplied page specification must be 
generated using only these button variants and styling rules. 
No new button color system should be created. 
 
18. Badges / Pills 
Base: 
padding: 4px 9px 
border-radius: 6px 
font-family: IBM Plex Mono 
font-size: 11px 
gap: 6px 
State 
Styling 
OK 
Accent wash + accent soft 
Hold 
Warning wash + warning 
Rejected Danger wash + danger 
Neutral Raised + muted 
 
19. Forms 
Labels: 
12.5px 
--text-mute 
margin-bottom: 6px 
Inputs/selects/textareas: 
width: 100% 
padding: 10px 12px 
background: var(--raised) 
color: var(--text) 
border: 1px solid var(--border-hi) 
border-radius: 8px

## SOURCE PAGE 19

font: 400 13.5px/1.4 var(--font-sans) 
Focus 
border-color: var(--accent) 
box-shadow: var(--ring) 
Invalid 
border-color: var(--danger) 
 
20. Upload / Dropzone 
The dropzone is: 
padding: 26px 
background: transparent 
border: 1px dashed var(--border-hi) 
border-radius: 10px 
text-align: center 
font-family: IBM Plex Mono 
font-size: 12px 
color: var(--text-mute) 
Hover/active: 
border-color: var(--accent) 
color: var(--accent) 
background: var(--accent-wash) 
 
21. Tables 
Table wrapper: 
border: 1px solid var(--border) 
border-radius: 10px 
overflow: hidden 
Header: 
background: var(--chrome) 
padding: 9px 14px 
font-family: IBM Plex Mono

## SOURCE PAGE 20

font-size: 10px 
font-weight: 500 
letter-spacing: 0.1em 
text-transform: uppercase 
color: var(--text-mute) 
Rows: 
• 
Normal → --surface 
• 
Alternating → --row-alt 
• 
Hover → --raised 
• 
Borders → --border 
• 
Text → --text-soft 
 
22. Progress Indicators 
Track: 
height: 6px 
border-radius: 999px 
background: var(--border) 
Fill: 
background: var(--accent) 
border-radius: 999px 
 
23. Modal & Popover 
Scrim 
position: fixed 
inset: 0 
z-index: 60 
background: var(--scrim) 
backdrop-filter: blur(2px) 
Modal 
width: min(560px, 100%) 
background: var(--raised)

## SOURCE PAGE 21

border: 1px solid var(--border-hi) 
border-radius: 14px 
padding: 22px 
The supplied shadow must be preserved. 
Popover 
background: var(--raised) 
border: 1px solid var(--border-hi) 
border-radius: 10px 
padding: 6px 
 
24. React Flow 
React Flow must visually belong to the exact same Graphite Ink system. 
Canvas: 
background: var(--bg) 
Edges: 
stroke: var(--border-hi) 
stroke-width: 1.5 
Animated edge: 
stroke: var(--accent) 
Controls/minimap: 
background: var(--chrome) 
border: 1px solid var(--border) 
border-radius: 8px 
Workflow nodes 
min-width: 168px 
padding: 10px 12px 
background: var(--raised) 
border: 1px solid var(--border-hi) 
border-radius: 8px 
font-family: IBM Plex Mono 
font-size: 11.5px

## SOURCE PAGE 22

Node states must use the exact supplied state colors: 
• 
Pending 
• 
Running 
• 
Completed 
• 
Paused 
• 
Approved 
• 
Failed 
• 
Rejected 
 
25. Recharts 
Chart wells: 
background: var(--chrome) 
border: 1px solid var(--border) 
border-radius: 10px 
padding: 14px 
Grid: 
--border 
Axis: 
--border-hi 
Axis labels: 
--text-mute 
IBM Plex Mono 
11px 
Tooltip: 
background: var(--raised) 
border: 1px solid var(--border-hi) 
border-radius: 8px 
color: var(--text) 
Chart series 
Only the defined palette: 
series-1 → --accent

## SOURCE PAGE 23

series-2 → --accent-deep 
series-3 → --warn 
No arbitrary rainbow palette. 
 
26. Public Job Pages 
Public job pages still use the same Graphite Ink background. 
.public-page { 
    background: var(--bg); 
    min-height: 100vh; 
} 
Content: 
max-width: 720px 
margin: 0 auto 
padding: 56px 24px 80px 
gap: 24px 
So public pages do not get a separate theme. 
 
27. Scrollbars 
The scrollbar system is also fixed: 
scrollbar-color: var(--border-hi) var(--bg) 
scrollbar-width: thin 
WebKit: 
width: 10px 
height: 10px 
track: var(--bg) 
thumb: var(--border-hi) 
The supplied hover value is: 
#3A454C 
 
28. Focus & Accessibility Styling 
Focus-visible:

## SOURCE PAGE 24

outline: none 
box-shadow: var(--ring) 
border-radius: 6px 
This must remain consistent across interactive elements. 
 
29. Logos, Icons & Remaining UI Elements 
Where a specific logo/icon/button/control is not provided by the user, it may be auto-generated at 
implementation time. 
However: 
It must follow 
• 
Graphite Ink colors 
• 
Existing accent hierarchy 
• 
Existing typography 
• 
Existing border system 
• 
Existing radii 
• 
Existing visual weight 
• 
Existing dark UI language 
• 
Existing spacing principles 
It must not introduce 
• 
New primary colors 
• 
New themes 
• 
Gradients 
• 
Unrelated branding styles 
• 
Excessive glow 
• 
Glassmorphism 
• 
Unspecified visual effects 
• 
A separate Student/Recruiter design language 
The provided CSS does not specify a complete icon library or exact individual logo designs, so I will 
not falsely claim one exists. Instead, required visual elements will be generated to conform to the 
supplied system. 
 
30. Page-by-Page Enforcement

## SOURCE PAGE 25

This styling applies identically to: 
LOOP-MIND Website 
        │ 
        ├── Landing / Public Pages 
        │ 
        ├── Authentication UI 
        │ 
        ├── Student Portal 
        │ 
        ├── Recruiter Portal 
        │ 
        ├── Job Pages 
        │ 
        ├── AI / Agent Interfaces 
        │ 
        ├── Analytics 
        │ 
        ├── Workflow / React Flow 
        │ 
        ├── Tables 
        │ 
        ├── Forms 
        │ 
        ├── Modals 
        │ 
        └── All Future Pages 
The content and functionality may differ by page, but the visual language does not. 
 
31. Print Exception 
The source explicitly defines a print-mode exception: 
body, html

## SOURCE PAGE 26

background: #fff 
    color: #111 
Navbar, sidebar and footer are hidden. 
Cards, stats and tables become white with #ddd borders. 
This is the only explicitly defined white-background exception in the supplied styling specification. 
 
32. Implementation Rule 
The styling should be centralized as: 
src/styles/agenthire-theme.css 
and imported once in: 
main.tsx 
after Tailwind's base layer, exactly as specified by the source. 
 
33. Final Visual Architecture 
                    LOOP-MIND 
                       │ 
                       ↓ 
              GRAPHITE INK THEME 
                       │ 
                       ↓ 
                 #0F1317 BASE 
                       │ 
       ┌───────────────┼────────────────┐ 
       ↓               ↓                ↓ 
    CHROME           SURFACE           RAISED 
   #12171B          #161C21           #1D242A 
       │               │                │ 
 Sidebar/Footer     Cards/Panels    Inputs/Modals 
 Tables/Charts      Table Rows      Popovers/Hover 
       │               │                │ 
       └───────────────┼────────────────┘

## SOURCE PAGE 27

↓ 
                 BORDERS / INK 
                       │ 
          ┌────────────┴────────────┐ 
          ↓                         ↓ 
       #232B31                   #2C353B 
       border                   border-hi 
          │                         │ 
          └────────────┬────────────┘ 
                       ↓ 
                 TEAL ACCENT 
                       │ 
                    #6FD3C0 
                       │ 
       ┌───────────────┼───────────────┐ 
       ↓               ↓               ↓ 
     Primary        Progress       Active State 
       │ 
       ↓ 
   Accent Soft / Deep / Wash 
                       │ 
              Warning / Danger 
                       │ 
           #E0A86B / #E77E72 
Final Rule 
LOOP-MIND functionality can expand as implementation progresses, but the visual system cannot 
drift. 
The uploaded Graphite Ink specification controls: 
background + colors + typography + spacing + borders + radii + buttons + cards + badges + forms + 
tables + progress + modals + popovers + React Flow + Recharts + navbar + sidebar + footer + public 
pages + responsive behavior + scrollbars + focus states.

## SOURCE PAGE 28

If the specification does not define a particular visual detail, I will not hallucinate that it does. I will 
generate the required element only when implementation needs it, and make it conform to the 
existing Graphite Ink system. 
LOOP-MIND — PAGE 1 SDD 
Landing / Home Page 
Source of truth for this page: the provided handwritten Page 1 sketch + the previously established 
Graphite Ink visual system. 
Implementation rule: do not add functionality, text, sections, or navigation that are not defined 
here. 
 
1. Page Overview 
Property 
Specification 
Page 
Website Page 1 — Landing Page 
Purpose 
Introduce LOOP-MIND and its core capabilities 
Background 
Exactly the established Graphite Ink background #0F1317 
Layout 
Center-focused landing page 
Navbar 
Required 
Hero 
Required 
Feature Cards Required 
Footer 
Required 
Responsive 
Must follow the global Graphite Ink responsive system 
Theme 
Graphite Ink — no separate page theme 
 
2. Complete Page Structure 
PAGE 1 — LANDING PAGE 
│ 
├── NAVBAR 
│   ├── LOOP-MIND Logo / Brand 
│   ├── Login 
│   └── Help 
│

## SOURCE PAGE 29

├── MAIN CONTENT 
│   │ 
│   ├── HERO 
│   │   ├── Heading 
│   │   └── Description 
│   │ 
│   └── FEATURE CARD CONTAINER 
│       ├── Placement Readiness 
│       ├── Read Job Applications 
│       └── AI Recruitment 
│ 
└── FOOTER 
    ├── Terms of Use 
    ├── Privacy Policy 
    ├── [middle item shown in sketch] 
    ├── Membership Plans 
    ├── Help 
    └── LOOP-MIND © 
 
3. Global Background — NON-NEGOTIABLE 
The entire page must use: 
#0F1317 
This applies to: 
• 
Navbar surrounding background 
• 
Main page 
• 
Hero area 
• 
Space surrounding feature cards 
• 
Footer surrounding area 
• 
Help modal overlay's underlying page 
• 
Terms of Use card 
• 
Privacy Policy card

## SOURCE PAGE 30

• 
Membership Plans card 
• 
All responsive layouts 
Do not create another background for this page. 
The feature cards, modal/card surfaces and footer may use the already-defined Graphite Ink surface 
hierarchy, but the page itself remains #0F1317. 
 
4. NAVBAR 
The navbar follows the established Graphite Ink navbar specification. 
Left side 
[LOOP-MIND LOGO]  LOOP-MIND 
The logo shown in the sketch is only a hand-drawn placeholder. 
Logo rule 
Generate an appropriate LOOP-MIND logo/mark automatically during implementation. 
It must: 
• 
Match the Graphite Ink visual language. 
• 
Use the existing theme colors. 
• 
Match the navbar proportions. 
• 
Remain visually simple. 
• 
Not introduce a new color palette. 
• 
Not introduce gradients or an unrelated branding style. 
Right side 
Login     Help 
 
5. LOGIN 
The navbar must contain exactly: 
Login 
Important behavior 
Login acts as both: 
• 
Login 
• 
Create an Account 
The exact authentication UI/flow will be specified on the next page, so do not invent the next-page 
authentication design here.

## SOURCE PAGE 31

For Page 1, only establish the Login interaction entry point. 
 
6. HELP 
Navbar contains: 
Help 
Interaction 
When the user clicks Help: 
Help 
 ↓ 
Centered Help Card 
The card must appear on the same Page 1, rather than navigating to another page. 
Help card 
The user explicitly allows temporary content to be generated for this card. 
Therefore, implementation may provide meaningful basic content such as: 
Help 
 
Need help using LOOP-MIND? 
 
Explore Placement Readiness to understand what 
you need to improve before applying. 
 
Use Read Job Applications to discover suitable 
opportunities. 
 
AI Recruitment helps recruiters screen, match, 
shortlist and evaluate candidates. 
 
For account-related help, use Login. 
The exact temporary copy can be refined later. 
Modal behavior 
The Help card must:

## SOURCE PAGE 32

• 
Appear centered. 
• 
Use the existing Graphite Ink modal/card styling. 
• 
Use the existing raised surface. 
• 
Use the existing border system. 
• 
Use the existing scrim. 
• 
Not change the page background. 
• 
Provide an obvious way to close it. 
Do not create a separate Help page unless later specified. 
 
7. HERO SECTION 
The hero must be centered horizontally and visually positioned in the central area of the page. 
Hero heading — EXACT TEXT 
Prepare. Match. Apply. Get Ready. 
Do not rewrite, paraphrase, shorten, or add text to this heading. 
 
8. HERO DESCRIPTION 
The description shown in the sketch is: 
LOOP-MIND connects students with real opportunities, evaluates 
their readiness, identifies what to improve, and helps turn every 
application into smarter preparation. 
This text should be preserved as the page's hero description. 
Hero alignment 
        Prepare. Match. Apply. Get Ready. 
 
LOOP-MIND connects students with real opportunities, evaluates 
their readiness, identifies what to improve, and helps turn every 
application into smarter preparation. 
The complete hero block is centered. 
 
9. HERO — NO UNDEFINED CTA 
The sketch does not show a hero CTA button.

## SOURCE PAGE 33

Therefore: 
Do not add buttons such as: 
• 
Get Started 
• 
Explore 
• 
Apply Now 
• 
Learn More 
• 
Sign Up 
unless a later specification explicitly adds them. 
The existing Login navbar interaction is sufficient for the functionality currently defined. 
 
10. FEATURE SECTION 
The feature area consists of one large bordered container containing three feature cards/columns. 
The entire feature section should remain centered within the page. 
┌──────────────────────────────────────────────────────────────┐ 
│                                                              │ 
│  [Logo] Placement Readiness   [Logo] Read Job Applications   │ 
│                                                              │ 
│  description                 description                     │ 
│                                                              │ 
│                         [Logo] AI Recruitment                │ 
│                         description                          │ 
│                                                              │ 
└──────────────────────────────────────────────────────────────┘ 
The exact implementation can use a responsive 3-column layout on larger screens while preserving 
the visual relationship shown in the sketch. 

## UPDATE — Center alignment fix (UPDATE SDD §2)

The hero block and feature section were horizontally centered already
but not vertically centered as a group within the page's main content
area. LandingPage.tsx now wraps the hero section and feature card in one
flex container that centers them together, both horizontally and
vertically, within the available page height — no text, elements,
background, colours, fonts, cards, buttons, navbar, or footer changed.
 
11. FEATURE CARD 1 
Title — EXACT 
Placement Readiness 
Description — EXACT 
Know your skill gaps and what to improve before you apply.

## SOURCE PAGE 34

Behavior 
This is informational content only. 
It is NOT a button. 
It must not: 
• 
Navigate somewhere 
• 
Act as a CTA 
• 
Look like a clickable button 
• 
Contain a fake action 
 
12. FEATURE CARD 2 
Title — EXACT 
Read Job Applications 
Description — EXACT 
Apply to real jobs when you're ready and let your profile move into the recruitment process. 
Behavior 
This is informational content only. 
It is NOT a button. 
 
13. FEATURE CARD 3 
Title — EXACT 
AI Recruitment 
Description — EXACT 
Screen, match, shortlist, and evaluate candidates with AI-assisted recruitment. 
Behavior 
This is informational content only. 
It is NOT a button. 
 
14. FEATURE LOGOS / ICONS 
Each of the three feature sections has a small logo/mark in the sketch. 
The actual handwritten drawings are placeholders rather than defined production logos. 
Therefore, generate appropriate icons/marks automatically.

## SOURCE PAGE 35

Requirements 
All three must: 
• 
Match the Graphite Ink theme. 
• 
Use the established color tokens. 
• 
Have consistent visual weight. 
• 
Have consistent dimensions. 
• 
Be semantically related to their feature. 
• 
Look like one unified icon family. 
Suggested semantic direction: 
Feature 
Visual meaning 
Placement Readiness Readiness / skills / progress 
Read Job Applications Jobs / applications 
AI Recruitment 
AI / recruitment / candidate matching 
These are visual-generation directions only, not additional feature functionality. 
 
15. FEATURE CARD STYLING 
Use the previously established Graphite Ink card system. 
The feature container should use: 
• 
--surface 
• 
--border 
• 
Existing border radius 
• 
Existing spacing 
• 
Existing typography 
• 
Existing Graphite Ink accent 
Do not create a new card style. 
No excessive effects 
Do not introduce: 
• 
Glassmorphism 
• 
Neon glow 
• 
Gradient cards

## SOURCE PAGE 36

• 
Large shadows 
• 
Bright multicolor cards 
• 
Animated decorative effects 
The page should remain consistent with the Graphite Ink system. 
 
16. FEATURE TEXT HIERARCHY 
Each feature should visually follow: 
[ICON] 
 
Feature Title 
 
Feature description 
Title: 
• 
Primary text 
• 
Stronger visual weight 
Description: 
• 
Secondary text 
• 
Readable 
• 
No excessive contrast 
The exact Graphite Ink typography system must be used. 
 
17. FOOTER 
The footer must be positioned at the bottom of the page according to the global application shell. 
Critical alignment requirement 
Footer elements must be centered. 
The sketch clearly places the footer navigation in the central horizontal area. 
 
18. FOOTER TEXT 
The visible footer elements are: 
Terms of Use 
Privacy Policy

## SOURCE PAGE 37

Membership Plans 
Help 
And: 
LOOP-MIND © 
These visible texts should be preserved. 
The sketch also contains a small unclear/hand-drawn symbol between Privacy Policy and 
Membership Plans. Since its intended meaning is not identifiable from the sketch, do not invent its 
meaning or label. 
 
19. FOOTER INTERACTIONS 
The following are interactive footer items: 
Terms of Use 
Privacy Policy 
Membership Plans 
Help 
Terms of Use 
Clicking it should open a centered card/modal on the same page. 
Temporary meaningful content may be generated because the user explicitly permitted this. 
Privacy Policy 
Clicking it should open a centered card/modal on the same page. 
Temporary meaningful content may be generated. 
Membership Plans 
Clicking it should open a centered card/modal on the same page. 
Temporary content may be generated. 
Help 
Clicking it should use the same Help card behavior as the navbar Help. 
Do not create duplicate Help implementations. 
 
20. TERMS OF USE CARD 
Temporary implementation content can be generated. 
Example structure: 
Terms of Use

## SOURCE PAGE 38

LOOP-MIND provides tools and services intended to help 
students prepare for opportunities and support recruiters 
through AI-assisted recruitment workflows. 
 
Users are responsible for the information they provide 
and how they use the platform. 
 
[Close] 
This is temporary implementation content only and should not be treated as the final legal policy. 
 
21. PRIVACY POLICY CARD 
Temporary implementation content can be generated. 
Example: 
Privacy Policy 
 
LOOP-MIND may process information required to provide 
student, recruitment and platform functionality. 
 
Information should be handled according to the platform's 
applicable privacy practices. 
 
[Close] 
This is temporary placeholder content and not a final legal policy. 
 
22. MEMBERSHIP PLANS CARD 
Temporary implementation content can be generated. 
Example: 
Membership Plans 
 
LOOP-MIND membership options will be presented here.

## SOURCE PAGE 39

Membership and payment functionality will be implemented 
later as specified by the project requirements. 
 
[Close] 
Important 
Do not implement payment functionality on this page. 
The master project specification states that payments are to be implemented later. 
 
23. FOOTER HELP 
Footer Help must open the same centered Help card used by navbar Help. 
There should be: 
Navbar Help 
      ↓ 
   Help Card 
and: 
Footer Help 
      ↓ 
   Same Help Card 
Do not duplicate the card logic unnecessarily. 
 
24. CENTERING REQUIREMENTS 
This page has three explicit center requirements. 
Hero 
Horizontally centered 
Feature section 
Centered within main content 
Footer elements 
Centered horizontally 
Modal/cards 
Centered horizontally

## SOURCE PAGE 40

+ 
Centered vertically 
 
25. RESPONSIVE BEHAVIOR 
The page must remain usable on: 
• 
Desktop 
• 
Tablet 
• 
Mobile 
The global Graphite Ink responsive rule remains authoritative. 
At smaller widths: 
Navbar 
   ↓ 
Main 
   ↓ 
Footer 
The sidebar is not relevant to this public landing page. 
Feature cards may transition from: 
3 columns 
to: 
stacked / responsive layout 
as required by available width, without changing the content or visual system. 
 
26. What MUST NOT Be Added 
For this page, do not add: 
• 
Extra hero sections 
• 
Extra feature cards 
• 
Testimonials 
• 
Pricing section 
• 
Recruiter CTA 
• 
Student CTA 
• 
Login form

## SOURCE PAGE 41

• 
Registration form 
• 
Dashboard 
• 
Job search 
• 
Job listings 
• 
AI chatbot 
• 
Statistics 
• 
Testimonials 
• 
FAQ section 
• 
Newsletter 
• 
Social-media section 
• 
Additional footer sections 
unless explicitly specified later. 
 
27. Exact Page Content 
The page's defined primary text is: 
LOOP-MIND 
 
Login 
Help 
 
Prepare. Match. Apply. Get Ready. 
 
LOOP-MIND connects students with real opportunities, evaluates 
their readiness, identifies what to improve, and helps turn every 
application into smarter preparation. 
 
Placement Readiness 
Know your skill gaps and what to improve before you apply. 
 
Read Job Applications 
Apply to real jobs when you're ready and let your profile move into the recruitment process.

## SOURCE PAGE 42

AI Recruitment 
Screen, match, shortlist, and evaluate candidates with AI-assisted recruitment. 
 
Terms of Use 
Privacy Policy 
Membership Plans 
Help 
 
LOOP-MIND © 
These texts must not be unnecessarily changed. 
 
28. Visual Relationship 
The final page should conceptually be: 
┌──────────────────────────────────────────────────────────────┐ 
│  [LOGO] LOOP-MIND                              Login   Help  │ 
├──────────────────────────────────────────────────────────────┤ 
│                                                              │ 
│                                                              │ 
│              Prepare. Match. Apply. Get Ready.              │ 
│                                                              │ 
│       LOOP-MIND connects students with real opportunities,    │ 
│       evaluates their readiness, identifies what to improve, │ 
│       and helps turn every application into smarter          │ 
│       preparation.                                           │ 
│                                                              │ 
│     ┌────────────────────────────────────────────────────┐   │ 
│     │                                                    │   │ 
│     │  [ICON]              [ICON]              [ICON]    │   │ 
│     │  Placement           Read Job            AI        │   │ 
│     │  Readiness            Applications       Recruitment│  │

## SOURCE PAGE 43

│     │                                                    │   │ 
│     │  description         description         description│  │ 
│     │                                                    │   │ 
│     └────────────────────────────────────────────────────┘   │ 
│                                                              │ 
│                                                              │ 
├──────────────────────────────────────────────────────────────┤ 
│ Terms of Use   Privacy Policy   [existing unclear item]      │ 
│              Membership Plans   Help                         │ 
│                                                              │ 
│                         LOOP-MIND ©                           │ 
└──────────────────────────────────────────────────────────────┘ 
This is a structural interpretation of the supplied sketch, not permission to add unspecified content. 
 
29. Graphite Ink Enforcement 
Every component on this page must inherit the previously established Graphite Ink system: 
BACKGROUND 
#0F1317 
        ↓ 
CHROME 
#12171B 
        ↓ 
SURFACE 
#161C21 
        ↓ 
RAISED 
#1D242A 
        ↓ 
BORDERS 
#232B31 / #2C353B 
        ↓

## SOURCE PAGE 44

TEXT 
#F2F5F4 / #C9D2CF / #8A9591 
        ↓ 
ACCENT 
#6FD3C0 
        ↓ 
WARN / DANGER 
#E0A86B / #E77E72 
Typography remains: 
Space Grotesk 
+ 
IBM Plex Mono 
No page-specific theme may override this. 
 
30. Implementation Boundary 
This SDD defines Page 1 only. 
The following are intentionally left for later pages because the current sketch does not define them: 
• 
Login/create-account UI 
• 
Authentication flow 
• 
Student dashboard 
• 
Recruiter dashboard 
• 
Job application workflow 
• 
Placement readiness interface 
• 
AI recruitment interface 
• 
Membership/payment implementation 
• 
Detailed legal pages 
• 
Other application pages 
They must be specified when their respective sketches/requirements are provided. 
 
31. Final Page 1 Acceptance Criteria 
The implementation is correct only if:

## SOURCE PAGE 45

• 
Page uses exactly #0F1317 as its base background. 
• 
Graphite Ink styling is used throughout. 
• 
Navbar contains LOOP-MIND branding, Login, and Help. 
• 
Login is the entry point for both login and account creation. 
• 
Hero is centered. 
• 
Hero heading is exactly “Prepare. Match. Apply. Get Ready.” 
• 
Hero description matches the supplied text. 
• 
Three feature sections exist. 
• 
Feature titles/descriptions match the supplied text. 
• 
Feature sections are informational, not buttons. 
• 
Appropriate feature logos/icons are generated consistently. 
• 
Footer elements are centered. 
• 
Terms of Use opens a centered card. 
• 
Privacy Policy opens a centered card. 
• 
Membership Plans opens a centered card. 
• 
Navbar Help and Footer Help open the same centered Help card. 
• 
Modal/card styling follows Graphite Ink. 
• 
No unsupported sections or functionality are added. 
• 
Responsive behavior follows the established design system. 
• 
No separate background/theme is introduced. 
• 
The implementation remains inside the existing LOOP-MIND repository architecture. 
• 
spec.md and phase.md are cross-checked before implementation and after 
implementation, with the new Page 1 specification added without duplication or 
contradiction. 
LOOP-MIND — PAGE 1 SDD UPDATE 
Login Modal / Card

## SOURCE PAGE 46

This is an update to Page 1 only. The Login interaction must now follow the newly provided sketch 
exactly. The existing Page 1 landing-page structure remains unchanged except for the Login behavior 
defined below. 
 
1. Login Interaction 
On Page 1, the navbar contains: 
Login 
When the user clicks Login: 
PAGE 1 
   │ 
   └── Login 
         ↓ 
   Centered Login Card / Modal 
Mandatory behavior 
• 
The Login card/modal appears on Page 1 itself. 
• 
It must not navigate to a separate Login page. 
• 
It must use the same modal/card interaction pattern as Help. 
• 
It must appear at the center of the page. 
• 
The underlying Page 1 remains visible through the modal scrim. 
• 
It must use the existing Graphite Ink styling. 
• 
No separate login-page background or theme is permitted. 
 
2. Login Modal Structure 
The card must contain the following structure: 
┌──────────────────────────────────────────────┐ 
│                                              │ 
│                   Welcome                    │ 
│                                              │ 
│          Enter your details to continue      │ 
│                                              │ 
│       +91       Mobile no.                   │ 
│                                              │

## SOURCE PAGE 47

│                  Get OTP                     │ 
│                                              │ 
│                                              │ 
│      Don't have account   Create account     │ 
│                              ↳ on site       │ 
│                                              │ 
└──────────────────────────────────────────────┘ 
This follows the supplied sketch. 
 
3. Exact Text 
The following text must be preserved exactly as specified in the sketch: 
Welcome 
 
Enter your details to continue 
 
+91 
 
Mobile no. 
 
Get OTP 
 
Don't have account 
 
Create account 
The Create account text is presented as an underlined link in the sketch. 
Do not replace these texts with alternatives such as: 
• 
Sign in 
• 
Sign up 
• 
Continue with phone 
• 
Enter mobile number 
• 
Send OTP

## SOURCE PAGE 48

• 
Register 
 
4. Modal Heading 
The top of the card contains: 
Welcome 
It must be visually prominent within the existing Graphite Ink typography hierarchy. 
 
5. Instruction Text 
Immediately below the heading: 
Enter your details to continue 
This is descriptive text and should use the existing secondary text styling. 
 
6. Mobile Number Input 
The mobile-number input consists of two visual portions: 
+91    Mobile no. 
Country code 
Display: 
+91 
as shown in the sketch. 
Input 
The input displays: 
Mobile no. 
as its placeholder. 
The field must be styled using the existing Graphite Ink form/input specification. 
 
7. Mobile Number Validation 
The sketch explicitly specifies: 
button activates only when user enters valid 10 digit mobile no. 
Therefore: 
Initial state 
Mobile number = empty

## SOURCE PAGE 49

↓ 
Get OTP = inactive / disabled 
Valid state 
When the user enters a valid 10-digit mobile number: 
10-digit valid mobile number 
        ↓ 
Get OTP 
        ↓ 
Enabled 
Invalid state 
If the entered number is not a valid 10-digit mobile number: 
Invalid / incomplete number 
        ↓ 
Get OTP 
        ↓ 
Disabled 
Do not enable the button merely because the field is non-empty. 
 
8. Get OTP 
The card contains: 
Get OTP 
Button state 
The button must remain inactive until the mobile number satisfies the specified valid 10-digit 
requirement. 
The exact OTP-generation, verification, resend, timer, backend authentication, or subsequent OTP 
screen is not defined by this sketch. 
Therefore: 
Do not invent the OTP workflow in this SDD. 
Only the Page 1 Login-card behavior and the specified button activation rule are defined here. 
 
9. Create Account 
The bottom portion contains:

## SOURCE PAGE 50

Don't have account    Create account 
Create Account 
Create account must visually appear as an underlined link, matching the sketch. 
The sketch indicates: 
Create account 
       ↓ 
     on site 
Therefore, the interaction should remain an on-site account-creation entry point. 
The detailed Create Account page/modal/form is not defined in this sketch and must be specified 
separately before implementing that detailed flow. 
Do not invent its fields or registration process here. 
 
10. Login Card Position 
The card must be positioned: 
                    PAGE 1 
                       │ 
                       │ 
                 ┌───────────┐ 
                 │           │ 
                 │   LOGIN   │ 
                 │   CARD    │ 
                 │           │ 
                 └───────────┘ 
                       │ 
                       │ 
Mandatory 
• 
Horizontally centered 
• 
Vertically centered 
• 
Same-page modal 
• 
Same modal mechanism as Help

## SOURCE PAGE 51

11. Same Modal System as Help 
The Login card and Help card must use the same modal foundation. 
Help 
  ↓ 
Same modal system 
 
Login 
  ↓ 
Same modal system 
That means they share: 
• 
Centering behavior 
• 
Scrim 
• 
Modal positioning 
• 
Border system 
• 
Radius system 
• 
Raised surface 
• 
Focus behavior 
• 
Close behavior 
• 
Responsive behavior 
But their content is different. 
 
12. Graphite Ink Styling 
The Login card must use the already-established Graphite Ink tokens. 
Page background 
#0F1317 
Modal surface 
--raised 
#1D242A 
Border 
--border-hi 
#2C353B

## SOURCE PAGE 52

Primary text 
--text 
#F2F5F4 
Secondary text 
--text-soft 
#C9D2CF 
Muted text 
--text-mute 
#8A9591 
Accent 
--accent 
#6FD3C0 
Modal scrim 
rgba(9, 12, 14, 0.72) 
No new login-specific colors may be introduced. 
 
13. Typography 
Use the existing global typography: 
Primary 
Space Grotesk 
Monospace where appropriate 
IBM Plex Mono 
Do not introduce another font specifically for Login. 
 
14. Login Card — Visual Hierarchy 
The card should follow this hierarchy: 
Welcome 
   ↓ 
Enter your details to continue 
   ↓ 
+91   Mobile no.

## SOURCE PAGE 53

↓ 
Get OTP 
   ↓ 
Don't have account   Create account 
Spacing should be clean and consistent with the established Graphite Ink card/form spacing. 
 
15. No Additional Login Elements 
Do not add anything not shown or specified, including: 
• 
Email field 
• 
Password field 
• 
Google Login 
• 
GitHub Login 
• 
Social login 
• 
Remember Me 
• 
Forgot Password 
• 
CAPTCHA 
• 
Email OTP 
• 
Password login 
• 
Username 
• 
Extra authentication buttons 
• 
Extra text 
• 
Account type selector 
The supplied sketch specifically defines the Login card around mobile number + OTP. 
 
16. Page 1 Updated Interaction Map 
PAGE 1 — LANDING PAGE 
│ 
├── NAVBAR 
│   ├── LOOP-MIND 
│   ├── Login 
│   │     ↓

## SOURCE PAGE 54

│   │   CENTERED LOGIN MODAL 
│   │   ├── Welcome 
│   │   ├── Enter your details to continue 
│   │   ├── +91 
│   │   ├── Mobile no. 
│   │   ├── Get OTP 
│   │   │     └── Enabled only for valid 10-digit number 
│   │   └── Don't have account 
│   │       └── Create account 
│   │ 
│   └── Help 
│         ↓ 
│       CENTERED HELP MODAL 
│ 
├── HERO 
│ 
├── FEATURE INFORMATION 
│   ├── Placement Readiness 
│   ├── Read Job Applications 
│   └── AI Recruitment 
│ 
└── FOOTER 
    ├── Terms of Use 
    │     ↓ 
    │   CENTERED CARD 
    ├── Privacy Policy 
    │     ↓ 
    │   CENTERED CARD 
    ├── Membership Plans 
    │     ↓ 
    │   CENTERED CARD

## SOURCE PAGE 55

├── Help 
    │     ↓ 
    │   SAME HELP MODAL 
    └── LOOP-MIND © 
 
17. Critical Distinction 
The three feature sections on Page 1 remain: 
informational only. 
They are not buttons. 
Login is different: 
Login 
 ↓ 
Interactive 
 ↓ 
Centered modal 
Help is also interactive: 
Help 
 ↓ 
Interactive 
 ↓ 
Centered modal 
 
18. Acceptance Criteria 
Page 1 Login implementation is correct only when: 
• 
Clicking Login opens a modal/card on Page 1. 
• 
The modal is centered horizontally and vertically. 
• 
It uses the same modal system as Help. 
• 
The page behind it remains Page 1. 
• 
Background remains #0F1317. 
• 
Card uses Graphite Ink styling.

## SOURCE PAGE 56

• 
Heading says exactly Welcome. 
• 
Instruction says exactly Enter your details to continue. 
• 
Country code shows +91. 
• 
Input placeholder says exactly Mobile no.. 
• 
Get OTP exists. 
• 
Get OTP remains inactive until a valid 10-digit mobile number is entered. 
• 
Get OTP becomes active for a valid 10-digit mobile number. 
• 
Bottom text says exactly Don't have account. 
• 
Create account appears as an underlined link. 
• 
No unsupported authentication methods are added. 
• 
No separate Login page is created. 
• 
No separate background/theme is created. 
• 
Detailed OTP/account-creation flow is not invented beyond what the sketch specifies. 
• 
spec.md and phase.md are cross-checked before implementation. 
• 
After implementation, both are updated with this Login-modal requirement. 
• 
After updating, both files are cross-checked again for omissions, duplication, and 
contradictions. 
LOOP-MIND — PAGE 1 SDD UPDATE 
Enter OTP Card / Modal 
This is an additional update to Page 1. After a valid 10-digit mobile number is submitted through 
Get OTP, the Login card/modal on Page 1 is replaced by the Enter OTP card/modal. 
The OTP card must use the same centered modal/card system as Help and Login and must remain 
on Page 1. 
 
1. OTP Flow 
PAGE 1 
   │ 
   └── Login

## SOURCE PAGE 57

│ 
        └── Login Card 
              │ 
              └── Valid 10-digit mobile number 
                    │ 
                    └── Get OTP 
                          │ 
                          ▼ 
                    Enter OTP Card 
                    on SAME Page 1 
There must be no navigation to a separate OTP page. 
 
2. OTP Card Position 
The OTP card must: 
• 
Appear at the center of Page 1. 
• 
Use the same modal/card mechanism as Help. 
• 
Use the same Graphite Ink styling. 
• 
Keep the underlying Page 1 visible through the modal scrim. 
• 
Replace the Login card/modal content rather than creating an additional visible card behind 
it. 
┌──────────────────────────────────────────────┐ 
│                                              │ 
│                  Enter OTP                   │ 
│                                              │ 
│   We've sent a code to +91 [mobile number]   │ 
│                                              │ 
│                 _  _  _  _                   │ 
│                                              │ 
│                                              │ 
│       Didn't get the code yet?  Resend code  │ 
│                                              │

## SOURCE PAGE 58

└──────────────────────────────────────────────┘ 
The exact spacing/layout should follow the supplied sketch and global design system. 
 
3. Exact OTP Heading 
Display: 
Enter OTP 
Do not change this to: 
• 
Verify OTP 
• 
OTP Verification 
• 
Enter Verification Code 
• 
Verify Your Number 
 
4. Mobile Number Description 
The card must communicate that the OTP was sent to the entered number. 
The supplied sketch specifies: 
We've sent a code to +91 [user entered mobile no.] 
The actual mobile number must be dynamically taken from the number entered in the previous 
Login card. 
Example: 
We've sent a code to +91 9876543210 
Do not hard-code a particular user's number. 
 
5. OTP Input 
The OTP input must contain: 
4 digit OTP 
Visually, the sketch represents this as four separate OTP positions: 
_   _   _   _ 
The implementation should provide a proper 4-digit OTP input experience while preserving the 
four-position visual structure. 
 
6. OTP Validation 
The user explicitly specifies:

## SOURCE PAGE 59

when user enter valid OTP it should automatically move to next page or card or modal which I will 
specify later. 
Therefore: 
Valid 4-digit OTP 
       ↓ 
Automatically proceed 
       ↓ 
Next page/card/modal 
       ↓ 
Defined in a future specification 
Important 
The destination after successful OTP verification is not defined yet. 
Therefore: 
• 
Do not invent the destination. 
• 
Do not create the next page. 
• 
Do not decide whether it is a dashboard, account creation, profile, or another screen. 
• 
Keep the implementation boundary ready for the future specified destination. 
 
7. Incorrect OTP 
If the user enters an incorrect OTP, display: 
Incorrect OTP, please try again 
Mandatory placement 
The error message must appear directly under the OTP entering area. 
        _   _   _   _ 
 
Incorrect OTP, please try again 
It must not appear: 
• 
At the top of the card. 
• 
As a toast. 
• 
Outside the modal. 
• 
Under the Resend Code link.

## SOURCE PAGE 60

• 
On the Page 1 background. 
 
8. Incorrect OTP Visibility 
The error must appear only when the entered OTP is incorrect. 
Initial state: 
OTP field 
     ↓ 
No error message 
Incorrect OTP: 
OTP field 
     ↓ 
Incorrect OTP, please try again 
Do not display the error before the user submits/enters an OTP that is actually incorrect. 
 
9. OTP Retry 
After an incorrect OTP: 
Incorrect OTP, please try again 
The user must be able to try entering the OTP again. 
The error should not prevent another OTP attempt. 
The exact number of allowed attempts, lockout behavior, or account security policy is not defined in 
the supplied sketch, so none should be invented. 
 
10. Resend Code 
The OTP card contains: 
Resend code 
The sketch specifies that it should initially be inactive. 
Initial state 
Resend code 
     ↓ 
Inactive / disabled 
Timer

## SOURCE PAGE 61

The user explicitly specifies: 
30 seconds 
Therefore: 
OTP sent 
   ↓ 
30-second waiting period 
   ↓ 
Resend code becomes active 
The exact visual timer/countdown representation is not explicitly specified in the sketch, so do not 
introduce an elaborate timer design unnecessarily. 
 
11. Resend Code Behavior 
After the 30-second waiting period: 
Resend code 
     ↓ 
Active 
When clicked: 
Resend code 
     ↓ 
Send a new OTP 
     ↓ 
Same entered mobile number 
The OTP must be resent to the mobile number used in the Login card. 
The exact backend/SMS provider implementation is outside this SDD. 
 
12. Resend Timer Reset 
When Resend code is successfully activated and clicked: 
Resend code clicked 
       ↓ 
New OTP sent 
       ↓

## SOURCE PAGE 62

30-second waiting period starts again 
       ↓ 
Resend code becomes inactive 
Do not allow repeated immediate resend clicks during the waiting period. 
 
13. Change Mobile Number / Previous Login Card 
The supplied sketch shows: 
Incorrect mobile no. 
as an underlined interaction. 
The sketch also specifies: 
on click should go back to previous thing where user can change mobile no. 
Therefore: 
Incorrect mobile no. 
        ↓ 
Return to previous Login card 
        ↓ 
User can change mobile number 
Important 
It must return to the Login card on Page 1, not navigate away from Page 1. 
The previously entered mobile number may be retained in the field so the user can edit it, unless the 
later specification changes this behavior. 
 
14. Incorrect Mobile Number Link 
Display: 
Incorrect mobile no. 
as shown in the supplied sketch. 
It should be visually identifiable as an interactive text link, using the established Graphite Ink 
interaction styling. 
It is not a button. 
 
15. Complete OTP Card Content 
The defined OTP card content is:

## SOURCE PAGE 63

Enter OTP 
 
We've sent a code to +91 [user entered mobile no.] 
 
_   _   _   _ 
 
Incorrect mobile no. 
 
Didn't get the code yet? 
 
Resend code 
Where: 
• 
[user entered mobile no.] is dynamic. 
• 
Incorrect mobile no. returns to the Login card. 
• 
Resend code becomes active after 30 seconds. 
• 
Incorrect OTP error appears only after an incorrect OTP. 
 
16. Error-State Layout 
Normal state: 
┌──────────────────────────────────────────────┐ 
│                  Enter OTP                   │ 
│                                              │ 
│ We've sent a code to +91 9876543210          │ 
│                                              │ 
│             _   _   _   _                    │ 
│                                              │ 
│ Incorrect mobile no.                         │ 
│                                              │ 
│ Didn't get the code yet?  Resend code        │ 
└──────────────────────────────────────────────┘ 
Incorrect OTP state:

## SOURCE PAGE 64

┌──────────────────────────────────────────────┐ 
│                  Enter OTP                   │ 
│                                              │ 
│ We've sent a code to +91 9876543210          │ 
│                                              │ 
│             _   _   _   _                    │ 
│                                              │ 
│       Incorrect OTP, please try again        │ 
│                                              │ 
│ Incorrect mobile no.                         │ 
│                                              │ 
│ Didn't get the code yet?  Resend code        │ 
└──────────────────────────────────────────────┘ 
The error is specifically positioned under the OTP input. 
 
17. Same Modal System 
Page 1 now has three related modal states: 
Login 
  ↓ 
Login Card 
 
Help 
  ↓ 
Help Card 
 
Get OTP 
  ↓ 
Enter OTP Card 
All must share the same: 
• 
Centering 
• 
Modal container

## SOURCE PAGE 65

• 
Scrim 
• 
Border 
• 
Radius 
• 
Surface 
• 
Typography 
• 
Responsive behavior 
• 
Close behavior 
• 
Graphite Ink styling 
Only their content and state differ. 
 
18. Updated Page 1 Authentication Flow 
                    PAGE 1 
                       │ 
                       ▼ 
                    Login 
                       │ 
                       ▼ 
                ┌─────────────┐ 
                │ Login Card  │ 
                └─────────────┘ 
                       │ 
             Enter valid 10-digit 
                mobile number 
                       │ 
                       ▼ 
                    Get OTP 
                       │ 
                       ▼ 
              ┌────────────────┐ 
              │  Enter OTP     │ 
              │     Card       │

## SOURCE PAGE 66

└────────────────┘ 
                  │          │ 
             Wrong OTP    Valid OTP 
                  │          │ 
                  ▼          ▼ 
        Incorrect OTP,    Automatically 
        please try again   proceed to 
                  │        future-defined 
                  │        page/card/modal 
                  │ 
                  └── Try again 
 
Incorrect mobile no. 
          │ 
          ▼ 
   Return to Login Card 
   Change mobile number 
 
Resend code 
    │ 
    ├── Before 30 sec → Disabled 
    │ 
    └── After 30 sec → Enabled 
                         │ 
                         ▼ 
                    Resend OTP 
                         │ 
                         ▼ 
                    30-sec wait 
 
19. Styling

## SOURCE PAGE 67

The OTP card must not introduce any new styling system. 
It inherits the existing Page 1 Graphite Ink system: 
Background 
#0F1317 
 
Modal / Card 
Existing Graphite Ink raised surface 
 
Borders 
Existing Graphite Ink border tokens 
 
Primary text 
Existing Graphite Ink primary text 
 
Secondary text 
Existing Graphite Ink secondary text 
 
Accent 
Existing Graphite Ink accent 
No new: 
• 
Colors 
• 
Fonts 
• 
Gradients 
• 
Glass effects 
• 
Neon effects 
• 
Unrelated icons 
• 
Decorative backgrounds 
 
20. What Is Not Defined Yet 
Do not implement or invent: 
• 
OTP backend provider

## SOURCE PAGE 68

• 
Real SMS integration 
• 
OTP generation algorithm 
• 
OTP database/storage implementation 
• 
OTP expiry duration 
• 
Maximum OTP attempts 
• 
Account lockout 
• 
Next page after successful OTP 
• 
Create-account workflow after OTP 
• 
Profile creation 
• 
Dashboard destination 
These will be defined by subsequent specifications. 
 
21. Updated Acceptance Criteria 
• 
Get OTP opens the Enter OTP card/modal on Page 1. 
• 
OTP card is centered. 
• 
OTP card uses the same modal system as Help and Login. 
• 
Page background remains exactly the established Graphite Ink background. 
• 
Heading is exactly Enter OTP. 
• 
The entered mobile number is dynamically displayed with +91. 
• 
OTP consists of exactly 4 digits. 
• 
Valid OTP automatically proceeds to the future-defined destination. 
• 
No destination is invented at this stage. 
• 
Incorrect OTP displays exactly Incorrect OTP, please try again. 
• 
Incorrect OTP message appears only under the OTP input area when the OTP is wrong. 
• 
User can retry after an incorrect OTP. 
• 
Incorrect mobile no. returns the user to the previous Login card. 
• 
User can change the mobile number there. 
• 
Resend code is initially disabled.

## SOURCE PAGE 69

• 
Resend code becomes active after 30 seconds. 
• 
Clicking active Resend code resends OTP to the same mobile number. 
• 
Resend starts another 30-second waiting period. 
• 
No unsupported OTP functionality is invented. 
• 
No separate OTP page is created. 
• 
spec.md and phase.md must be cross-checked before implementation. 
• 
The OTP requirements must be added without duplicating existing Login specifications. 
• 
Both files must be cross-checked again after implementation for missing, repeated, or 
contradictory requirements. 
LOOP-MIND — PAGE 1 SDD UPDATE 
Create Student Profile Card / Modal 
This is an additional Page 1 update. When the user clicks Create account inside the existing Login 
card/modal, a Create a Student Profile card/modal must appear on the same Page 1. 
The existing Page 1, Login modal, and Enter OTP modal behavior remain unchanged except for this 
newly defined Create Account interaction. 
 
1. Create Account Flow 
PAGE 1 
   │ 
   └── Login 
        │ 
        ▼ 
   Login Card / Modal 
        │ 
        └── Create account 
              │ 
              ▼ 
      Create a Student Profile 
      Card / Modal 
              │

## SOURCE PAGE 70

│ 
          SAME PAGE 1 
Mandatory 
• 
No navigation to another page. 
• 
No separate Create Account page. 
• 
Card/modal must appear at the center of Page 1. 
• 
It must use the same modal/card system as Help, Login, and Enter OTP. 
• 
It must use the same Graphite Ink styling and background system. 
 
2. Create Student Profile Card 
The card must contain the title: 
Create a Student Profile 
This is the exact title shown in the supplied sketch. 
The visual structure is: 
┌──────────────────────────────────────────────┐ 
│                                              │ 
│          Create a Student Profile            │ 
│                                              │ 
│        Prepare. Match. Apply. Get Ready.     │ 
│                                              │ 
│       +91       Mobile no.                   │ 
│                                              │ 
│                 Get OTP                      │ 
│                                              │ 
└──────────────────────────────────────────────┘ 
 
3. Exact Text 
The Create Student Profile card must contain: 
Create a Student Profile 
 
Prepare. Match. Apply. Get Ready.

## SOURCE PAGE 71

+91 
 
Mobile no. 
 
Get OTP 
These texts must not be paraphrased or replaced. 
 
4. Tagline 
Directly below: 
Create a Student Profile 
display: 
Prepare. Match. Apply. Get Ready. 
This must use the same exact wording already established on Page 1. 
Do not introduce a different registration tagline. 
 
5. Mobile Number 
The card contains the same mobile-number entry structure: 
+91    Mobile no. 
Country code 
+91 
Input placeholder 
Mobile no. 
The field follows the existing Graphite Ink input styling. 
 
6. Get OTP 
The card contains: 
Get OTP 
The same validation requirement applies: 
Invalid / incomplete mobile number 
        ↓

## SOURCE PAGE 72

Get OTP disabled 
 
Valid 10-digit mobile number 
        ↓ 
Get OTP enabled 
The button must activate only when the user enters a valid 10-digit mobile number. 
 
7. Create Account OTP Flow 
The supplied sketch establishes the same mobile-number → OTP entry concept. 
Therefore: 
Create a Student Profile 
        │ 
        ▼ 
Enter valid 10-digit mobile number 
        │ 
        ▼ 
Get OTP 
        │ 
        ▼ 
Enter OTP Card / Modal 
The existing Enter OTP card/modal specification remains the authoritative OTP behavior. 
Therefore, do not create a separate inconsistent OTP design. 
The existing rules continue to apply: 
• 
4-digit OTP. 
• 
Incorrect OTP displays Incorrect OTP, please try again under the OTP input. 
• 
Valid OTP automatically proceeds to the next future-defined page/card/modal. 
• 
Resend code follows the existing 30-second rule. 
• 
Incorrect mobile no. returns to the previous mobile-number card where applicable. 
 
8. Important Authentication Distinction 
Page 1 now has two entry paths originating from Login:

## SOURCE PAGE 73

LOGIN 
 │ 
 ├── Existing user 
 │      ↓ 
 │   Login / Mobile OTP flow 
 │ 
 └── Create account 
        ↓ 
   Create a Student Profile 
        ↓ 
   Mobile number 
        ↓ 
   Get OTP 
        ↓ 
   Enter OTP 
        ↓ 
   Future-defined profile creation flow 
The detailed student-profile fields are not defined in this sketch. 
Therefore, do not invent fields such as: 
• 
Name 
• 
Email 
• 
Date of birth 
• 
Education 
• 
Skills 
• 
Resume 
• 
College 
• 
Branch 
• 
CGPA 
• 
Experience 
• 
Profile photo 
Those must be specified later.

## SOURCE PAGE 74

9. Same-Page Modal Requirement 
The complete interaction must remain within Page 1: 
┌───────────────────────────────────────────────┐ 
│                  PAGE 1                        │ 
│                                               │ 
│          [Create Student Profile]             │ 
│                 MODAL                         │ 
│                                               │ 
└───────────────────────────────────────────────┘ 
No route/page transition is required for this step. 
 
10. Modal System 
The Create Student Profile modal must use exactly the same modal foundation as: 
Help 
   ↓ 
Help Modal 
 
Login 
   ↓ 
Login Modal 
 
Get OTP 
   ↓ 
Enter OTP Modal 
 
Create account 
   ↓ 
Create Student Profile Modal 
Shared behavior: 
• 
Centered horizontally.

## SOURCE PAGE 75

• 
Centered vertically. 
• 
Same modal surface. 
• 
Same border. 
• 
Same radius. 
• 
Same scrim. 
• 
Same typography. 
• 
Same responsive behavior. 
• 
Same close behavior. 
• 
Same Graphite Ink visual language. 
 
11. Background 
The Page 1 background remains exactly the established background: 
#0F1317 
The Create Student Profile modal must not introduce a different background. 
All existing Page 1 styling remains unchanged. 
 
12. Graphite Ink Styling 
Use the existing global design tokens rather than creating a new Create Account theme. 
Page Background 
#0F1317 
 
Modal Surface 
Existing Graphite Ink raised surface 
 
Borders 
Existing Graphite Ink border system 
 
Primary Text 
Existing Graphite Ink primary text 
 
Secondary Text

## SOURCE PAGE 76

Existing Graphite Ink secondary text 
 
Accent 
Existing Graphite Ink accent 
Typography remains the established: 
Space Grotesk 
IBM Plex Mono where applicable 
Do not introduce another font or color system. 
 
13. Updated Page 1 Interaction Map 
PAGE 1 — LANDING PAGE 
│ 
├── NAVBAR 
│   ├── LOOP-MIND 
│   ├── Login 
│   │    │ 
│   │    ▼ 
│   │  LOGIN MODAL 
│   │    │ 
│   │    ├── Mobile no. 
│   │    ├── Get OTP 
│   │    │      ↓ 
│   │    │   ENTER OTP MODAL 
│   │    │ 
│   │    └── Create account 
│   │           ↓ 
│   │      CREATE STUDENT PROFILE MODAL 
│   │           │ 
│   │           ├── Prepare. Match. Apply. Get Ready. 
│   │           ├── +91 
│   │           ├── Mobile no.

## SOURCE PAGE 77

│   │           └── Get OTP 
│   │                  ↓ 
│   │             ENTER OTP MODAL 
│   │ 
│   └── Help 
│        ↓ 
│      HELP MODAL 
│ 
├── HERO 
│ 
├── FEATURE INFORMATION 
│   ├── Placement Readiness 
│   ├── Read Job Applications 
│   └── AI Recruitment 
│ 
└── FOOTER 
    ├── Terms of Use → Modal 
    ├── Privacy Policy → Modal 
    ├── Membership Plans → Modal 
    ├── Help → Same Help Modal 
    └── LOOP-MIND © 
 
14. Exact Scope of This Update 
This update defines only: 
Create account 
      ↓ 
Create a Student Profile modal 
      ↓ 
Mobile number 
      ↓ 
Get OTP

## SOURCE PAGE 78

It does not define the complete student profile creation process. 
The next stage after successful OTP verification must remain future-defined until its corresponding 
sketch/specification is provided. 
 
15. Acceptance Criteria 
• 
Clicking Create account in the Login card opens the Create Student Profile card/modal. 
• 
It appears on the same Page 1. 
• 
It is centered horizontally and vertically. 
• 
It uses the same modal system as Help, Login, and Enter OTP. 
• 
Title is exactly Create a Student Profile. 
• 
Tagline is exactly Prepare. Match. Apply. Get Ready. 
• 
Country code is exactly +91. 
• 
Mobile input placeholder is exactly Mobile no. 
• 
Get OTP exists. 
• 
Get OTP is disabled until a valid 10-digit mobile number is entered. 
• 
Valid 10-digit mobile number activates Get OTP. 
• 
Get OTP follows the existing Enter OTP flow. 
• 
Existing 4-digit OTP behavior remains authoritative. 
• 
Incorrect OTP error remains exactly Incorrect OTP, please try again and appears only 
below the OTP input. 
• 
No additional student-profile fields are invented. 
• 
No separate Create Account page is created. 
• 
No separate background or styling system is created. 
• 
The established Graphite Ink design system is preserved exactly. 
• 
spec.md and phase.md are cross-checked before implementation. 
• 
This requirement is added to the existing specification without duplicating previous 
Login/OTP requirements.

## SOURCE PAGE 79

• 
Both files are cross-checked again after implementation for omissions, duplication, and 
contradictions. 
LOOP-MIND — PAGE 1 SDD UPDATE 
Create Account → Enter OTP Modal 
This update specifically defines the OTP flow originating from the Create a Student Profile modal. It 
must use the same centered modal/card system as Help, Login, and the previously defined OTP 
modal, while the successful OTP destination is explicitly reserved for the future Create Account flow 
that you will specify later. 
 
1. Flow 
PAGE 1 
  │ 
  └── Login 
       │ 
       └── Create account 
             │ 
             ▼ 
      Create a Student Profile 
          Card / Modal 
             │ 
             │ valid 10-digit mobile no. 
             ▼ 
          Get OTP 
             │ 
             ▼ 
        Enter OTP 
        Card / Modal 
             │ 
       ┌─────┴─────┐ 
       │           │ 
   Wrong OTP    Valid 4-digit OTP 
       │           │

## SOURCE PAGE 80

▼           ▼ 
Incorrect OTP   Automatically proceed 
please try again       │ 
       │               ▼ 
       │       Next Create Account Flow 
       │       └── Defined later 
       │ 
       └── Retry 
 
2. Get OTP From Create Account Modal 
Inside the Create a Student Profile modal: 
Create a Student Profile 
 
Prepare. Match. Apply. Get Ready. 
 
+91    Mobile no. 
 
Get OTP 
When the user enters a valid 10-digit mobile number, Get OTP becomes active. 
When the user clicks: 
Get OTP 
the Create Student Profile modal transitions to the Enter OTP modal. 
 
3. Same Page Requirement 
The Enter OTP modal must appear on: 
PAGE 1 
It must not navigate to another page. 
┌─────────────────────────────────────────────┐ 
│                                             │ 
│                  PAGE 1                     │ 
│                                             │

## SOURCE PAGE 81

│             ┌───────────────┐               │ 
│             │   Enter OTP   │               │ 
│             │               │               │ 
│             │   _ _ _ _     │               │ 
│             │               │               │ 
│             └───────────────┘               │ 
│                                             │ 
└─────────────────────────────────────────────┘ 
The modal is centered both horizontally and vertically. 
 
4. Enter OTP Card Content 
The card must follow the supplied sketch: 
Enter OTP 
 
We've sent a code to +91 [entered mobile number] 
 
_   _   _   _ 
 
Incorrect mobile no. 
 
Didn't get the code yet?    Resend code 
The mobile number is dynamically populated from the Create Student Profile mobile-number input. 
 
5. OTP Input 
The OTP must be exactly: 
4 digits 
Visual representation: 
_   _   _   _ 
The user enters the OTP into the four-digit OTP input. 
 
6. Wrong OTP Behavior

## SOURCE PAGE 82

If the entered OTP is incorrect, display exactly: 
Incorrect OTP, please try again 
Mandatory placement 
The message must appear directly underneath the OTP entering area. 
        _   _   _   _ 
 
Incorrect OTP, please try again 
It must appear only when the entered OTP is wrong. 
Do not show it: 
• 
Before an OTP is entered. 
• 
While the OTP is incomplete. 
• 
As a toast. 
• 
At the top of the modal. 
• 
Outside the modal. 
• 
In the Page 1 background. 
 
7. Wrong OTP Retry 
After: 
Incorrect OTP, please try again 
the user remains inside the Enter OTP modal and can retry. 
Wrong OTP 
   ↓ 
Incorrect OTP, please try again 
   ↓ 
User enters OTP again 
No maximum-attempt or lockout behavior is defined yet, so none should be invented. 
 
8. Valid OTP Behavior 
When the user enters a: 
Valid 4-digit OTP 
the system must automatically proceed.

## SOURCE PAGE 83

Valid 4-digit OTP 
       ↓ 
Automatically proceed 
       ↓ 
Next Create Account flow 
Critical boundary 
The destination after successful OTP verification is: 
NOT DEFINED YET. 
It will be specified later by the user. 
Therefore, implementation must not invent: 
• 
Student profile fields 
• 
Dashboard 
• 
Student portal 
• 
Profile setup page 
• 
Resume upload 
• 
Education form 
• 
Skills form 
• 
Any other next screen 
The successful OTP event should simply hand off to the future-defined Create Account flow. 
 
9. Resend Code 
The existing OTP specification remains applicable. 
Didn't get the code yet?    Resend code 
Resend code is initially inactive. 
After 30 seconds, it becomes active. 
OTP sent 
   ↓ 
30-second wait 
   ↓ 
Resend code active 
When clicked:

## SOURCE PAGE 84

Resend code 
   ↓ 
New OTP sent to same mobile number 
   ↓ 
30-second waiting period starts again 
 
10. Incorrect Mobile Number 
The OTP modal retains: 
Incorrect mobile no. 
This is an interactive text link. 
When clicked: 
Incorrect mobile no. 
        ↓ 
Return to 
Create a Student Profile modal 
        ↓ 
User can change mobile number 
It must remain on Page 1. 
 
11. Modal Relationship 
There are now two distinct OTP entry contexts: 
LOGIN 
 │ 
 └── Get OTP 
       ↓ 
   Enter OTP Modal 
       ↓ 
   Future-defined login destination 
 
 
CREATE ACCOUNT

## SOURCE PAGE 85

│ 
 └── Create a Student Profile 
       │ 
       └── Get OTP 
             ↓ 
         Enter OTP Modal 
             ↓ 
         Valid OTP 
             ↓ 
       Future Create Account Flow 
The visual OTP modal system must be shared, but the successful destination depends on which flow 
initiated it. 
 
12. Create Account OTP State 
The implementation should maintain the originating flow: 
origin = Create Account 
Therefore: 
Create Student Profile 
        ↓ 
Get OTP 
        ↓ 
Enter OTP 
        ↓ 
Valid OTP 
        ↓ 
Create Account flow 
It must not accidentally send the user into the existing-user Login destination. 
 
13. Styling 
The Enter OTP modal must use the exact same established Page 1 styling system. 
No new styling is permitted.

## SOURCE PAGE 86

Background 
#0F1317 
Modal 
Use the existing Graphite Ink modal/card surface, border, radius, typography, spacing, and elevation. 
Typography 
Use the existing project typography. 
Colors 
Use only the already established Graphite Ink color tokens. 
Do not introduce a separate OTP color palette. 
 
14. Complete Create Account Flow Defined So Far 
PAGE 1 
  │ 
  ▼ 
Login 
  │ 
  ▼ 
Create account 
  │ 
  ▼ 
┌─────────────────────────────────┐ 
│     Create a Student Profile    │ 
│                                 │ 
│ Prepare. Match. Apply. Get Ready.│ 
│                                 │ 
│ +91    Mobile no.               │ 
│                                 │ 
│ Get OTP                         │ 
└─────────────────────────────────┘ 
  │ 
  │ valid 10-digit mobile number

## SOURCE PAGE 87

▼ 
┌─────────────────────────────────┐ 
│           Enter OTP             │ 
│                                 │ 
│ We've sent a code to            │ 
│ +91 [entered mobile number]     │ 
│                                 │ 
│        _   _   _   _            │ 
│                                 │ 
│ Incorrect mobile no.            │ 
│                                 │ 
│ Didn't get the code yet?        │ 
│ Resend code                     │ 
└─────────────────────────────────┘ 
  │ 
  ├── Wrong OTP 
  │      ↓ 
  │  Incorrect OTP, please try again 
  │      ↓ 
  │  Retry 
  │ 
  └── Valid 4-digit OTP 
         ↓ 
    Automatically proceed 
         ↓ 
    NEXT CREATE ACCOUNT FLOW 
         ↓ 
    TO BE SPECIFIED LATER 
 
15. What Must NOT Be Assumed 
The following remain intentionally undefined:

## SOURCE PAGE 88

• 
Exact next Create Account screen. 
• 
Student profile fields. 
• 
Profile completion process. 
• 
Account creation backend. 
• 
OTP provider. 
• 
OTP generation implementation. 
• 
OTP expiry. 
• 
Maximum attempts. 
• 
Account lockout. 
• 
Post-registration destination. 
Do not hallucinate or add any of these to the implementation. 
 
16. Acceptance Criteria 
• 
Get OTP in Create a Student Profile opens the Enter OTP modal. 
• 
Enter OTP modal appears on the same Page 1. 
• 
It is centered on the page. 
• 
It uses the same modal system as Help/Login. 
• 
OTP is exactly 4 digits. 
• 
Entered mobile number is dynamically displayed. 
• 
Wrong OTP displays exactly Incorrect OTP, please try again. 
• 
Wrong OTP message appears only under the OTP input. 
• 
User can retry after an incorrect OTP. 
• 
Valid 4-digit OTP automatically proceeds. 
• 
Successful OTP proceeds specifically into the Create Account flow. 
• 
The next Create Account flow is not invented and remains future-defined. 
• 
Incorrect mobile no. returns to the Create Student Profile modal. 
• 
User can change the mobile number. 
• 
Resend code remains inactive for 30 seconds.

## SOURCE PAGE 89

• 
Resend code becomes active after 30 seconds. 
• 
Resending starts a new 30-second waiting period. 
• 
Everything remains on Page 1. 
• 
Existing Graphite Ink background and styling are unchanged. 
• 
No separate OTP page is created. 
• 
No new colors, fonts, or visual system are introduced. 
• 
spec.md and phase.md must be cross-checked before implementation. 
• 
This update must be merged into the existing Login/Create Account/OTP specification 
without duplication. 
• 
spec.md and phase.md must be cross-checked again after implementation for 
omissions, repetition, and contradictions. 
LOOP-MIND — PAGE 1 SDD UPDATE 
Create Account → Basic Information 
This update extends the Create Account flow only. The existing Login-side OTP flow must remain 
separate, and a valid OTP entered from the Create Account side must automatically continue into 
the Create Account flow shown in the supplied sketch. 
 
1. Updated Create Account Flow 
PAGE 1 
  │ 
  ▼ 
Login 
  │ 
  ▼ 
Login Card / Modal 
  │ 
  └── Create account 
        │ 
        ▼ 
Create a Student Profile

## SOURCE PAGE 90

Card / Modal 
        │ 
        ▼ 
Enter valid mobile number 
        │ 
        ▼ 
Get OTP 
        │ 
        ▼ 
Enter OTP Card / Modal 
        │ 
        ├── Wrong OTP 
        │      ↓ 
        │  Incorrect OTP, please try again 
        │ 
        └── Valid 4-digit OTP 
               │ 
               ▼ 
        AUTOMATICALLY PROCEED 
               │ 
               ▼ 
       BASIC INFORMATION 
       Card / Modal 
               │ 
               ▼ 
       Continue 
               │ 
               ▼ 
       Next Create Account Flow 
       [To be specified later] 
Critical distinction

## SOURCE PAGE 91

LOGIN SIDE OTP 
    ↓ 
Login flow 
 
CREATE ACCOUNT SIDE OTP 
    ↓ 
Create Account flow 
    ↓ 
Basic Information 
A valid OTP from the Create Account side must never send the user into the Login flow. 
 
## UPDATE — OTP verification no longer creates the account (Student Create Account UPDATE SDD §1-3, §11-12)

A successful Create Account OTP still proceeds straight into Basic Information exactly as
below, but no permanent student account exists in the database yet at this point — only a
temporary registration draft. The information entered through Basic Information and every
following step is staged on that draft. The real account is created exactly once, at the
final "Create Account" click on the Recruitment History + Consent card, and only once Basic
Information and the required consent are both present — see that card's own SDD for the
exact rule. This does not change the modal/card mechanism or the visible flow described below.

2. Basic Information Modal 
After successful Create Account OTP verification, the same modal/card mechanism continues from 
Create Account into the Basic Information screen. 
The supplied sketch shows: 
Basic Information 
as the heading. 
It must appear as the next Create Account step. 
 
3. Basic Information — Exact Content 
The card must contain the following fields shown in the sketch: 
Basic Information 
 
Full Name 
 
Date of birth 
 
Day 
Month 
Year

## SOURCE PAGE 92

Gender 
 
○ Male 
○ Female 
○ Others 
 
Profile Photo 
 
Email Address 
 
Country 
State 
City 
 
Continue 
The wording supplied by the sketch must be preserved. 
 
4. Full Name 
Display: 
Full Name 
as the name input. 
The user must be able to enter their full name. 
No additional name fields are to be invented at this stage. 
 
5. Date of Birth 
The sketch explicitly separates the date into: 
Day 
Month 
Year 
with corresponding inputs: 
DD

## SOURCE PAGE 93

MM 
YYYY 
Therefore the implementation must provide three date components: 
Day   Month   Year 
DD     MM     YYYY 
They should be validated as a valid date rather than accepting impossible combinations. 
 
6. Gender 
The sketch provides exactly three options: 
○ Male 
○ Female 
○ Others 
These must be selectable options. 
Do not add additional gender choices unless a later specification explicitly defines them. 
 
7. Profile Photo 
The sketch marks: 
Profile Photo 
as: 
optional 
Therefore: 
Profile photo is NOT mandatory. 
The user must be able to continue without uploading a photo. 
 
8. Profile Photo — Selection Interaction 
When the user clicks the Profile Photo control, a selection interface must appear. 
The supplied reference establishes these three selection options: 
Camera 
Photos 
Files 
Therefore the selection UI must contain:

## SOURCE PAGE 94

┌─────────────────────┐ 
│     Camera         │ 
│                     │ 
│     Photos         │ 
│                     │ 
│     Files          │ 
└─────────────────────┘ 
The icons must be matched/generated according to the established LOOP-MIND visual styling. 
 
9. Profile Photo — Maximum Upload 
Only one photo may be uploaded. 
Maximum: 
1 photo 
The system must not allow: 
Photo 1 
Photo 2 
Photo 3 
... 
Only a single profile photo is permitted. 
 
10. Profile Photo — Optional + Single Constraint 
The complete rule is: 
Profile Photo 
     │ 
     ├── Skip → Allowed 
     │ 
     └── Upload 
           │ 
           └── Maximum 1 photo 
Therefore: 
• 
0 photos → valid

## SOURCE PAGE 95

• 
1 photo → valid 
• 
More than 1 photo → not allowed 
 
11. Camera 
Clicking: 
Camera 
must initiate the device camera/photo capture flow where supported. 
The resulting selection must remain limited to one photo. 
No video upload requirement is defined. 
 
12. Photos 
Clicking: 
Photos 
must allow the user to select a photo from the device's available photo/gallery source. 
Only one photo can ultimately be selected. 
 
13. Files 
Clicking: 
Files 
must allow the user to select a photo through the device/file picker. 
Only one photo can ultimately be selected. 
The supported file types and maximum file size are not defined in the supplied sketch, so do not 
invent them in the SDD. 
 
14. Email Address 
Display: 
Email Address 
with an email input. 
The sketch visually shows: 
@gmail.com 
inside the field.

## SOURCE PAGE 96

Therefore the field should communicate email-address entry while preserving the supplied 
@gmail.com visual reference. 
The exact email-domain restriction is not explicitly defined, so do not assume that only Gmail 
addresses are permitted. 
 
15. Country / State / City 
The sketch contains three dropdowns: 
Country ▼ 
State ▼ 
City ▼ 
These are contextual location selectors. 
They must be implemented as searchable dropdowns. 
 
16. Searchable Dropdown Requirement 
Each required location selector must support search: 
Country 
   ↓ 
Search 
   ↓ 
Select Country 
 
State 
   ↓ 
Search 
   ↓ 
Select State 
 
City 
   ↓ 
Search 
   ↓ 
Select City

## SOURCE PAGE 97

The user should not be forced to manually scroll through a potentially large list. 
 
17. Context-Aware Dropdown Relationship 
The dropdowns must be dependent on one another: 
Country 
   │ 
   ▼ 
State options for selected Country 
   │ 
   ▼ 
City options for selected State 
Therefore: 
Country 
Selecting a country determines the available states/regions. 
State 
Selecting a state determines the available cities. 
City 
City options must correspond to the selected state and country. 
Do not show unrelated states/cities after a parent location has been selected. 
 
18. Dataset Generation Rule 
If the required dropdown dataset is not provided by the user, the implementation may 
generate/populate a meaningful dataset automatically. 
However: 
Dataset must be generated/populated at implementation time. 
It must not be generated beforehand merely because the field exists. 
The generated dataset must be: 
• 
Meaningful to the field. 
• 
Contextually correct. 
• 
Internally consistent. 
• 
Suitable for Country → State → City relationships.

## SOURCE PAGE 98

• 
Searchable. 
Example structure: 
Country 
 ├── State / Region 
 │     ├── City 
 │     ├── City 
 │     └── City 
 └── State / Region 
       ├── City 
       └── City 
Do not create random unrelated country/state/city combinations. 
 
19. Dataset Source Boundary 
The user has not provided a specific authoritative location dataset in this specification. 
Therefore, the SDD must not claim a particular external dataset or provider. 
At implementation time, the developer may generate the required meaningful dataset according to 
the project's needs if no dataset has been supplied. 
 
20. Continue Button 
The card contains: 
Continue 
The button must activate only after all required information has been selected/entered. 
The sketch explicitly states: 
button only activated after user selecting everything required 
Therefore: 
Required information incomplete 
        ↓ 
Continue disabled 
 
Everything required completed 
        ↓

## SOURCE PAGE 99

Continue enabled 
 
21. Required vs Optional 
Explicitly defined: 
Field 
Requirement 
Full Name 
Required 
Date of birth Required 
Gender 
Required 
Profile Photo Optional 
Email Address Required 
Country 
Required 
State 
Required 
City 
Required 
Continue 
Enabled after required information is complete 
The Profile Photo is the only field explicitly marked optional in the supplied sketch. 
 
22. Basic Information Layout 
The implementation should follow the supplied composition: 
┌──────────────────────────────────────────────────────┐ 
│                                                      │ 
│                 Basic Information                    │ 
│                                                      │ 
│  Full Name                                            │ 
│  ┌──────────────────────────────────────────────┐    │ 
│  │ Full Name                                    │    │ 
│  └──────────────────────────────────────────────┘    │ 
│                                                      │ 
│  Date of birth                                       │ 
│                                                      │ 
│  Day             Month             Year              │

## SOURCE PAGE 100

│  ┌──────┐        ┌──────┐          ┌────────┐        │ 
│  │ DD   │        │ MM   │          │ YYYY   │        │ 
│  └──────┘        └──────┘          └────────┘        │ 
│                                                      │ 
│  Gender                                               │ 
│  ○ Male     ○ Female     ○ Others                    │ 
│                                                      │ 
│  Profile Photo                                       │ 
│                                                      │ 
│  Email Address                                       │ 
│  ┌──────────────────────────────────────────────┐    │ 
│  │ @gmail.com                                   │    │ 
│  └──────────────────────────────────────────────┘    │ 
│                                                      │ 
│  ┌────────────┐  ┌────────────┐  ┌────────────┐     │ 
│  │ Country ▼  │  │ State ▼    │  │ City ▼     │     │ 
│  └────────────┘  └────────────┘  └────────────┘     │ 
│                                                      │ 
│                         Continue                     │ 
│                                                      │ 
└──────────────────────────────────────────────────────┘ 
This is a structural representation; the exact visual styling must follow the established Page 1 design 
system. 
 
23. Global Styling — No Change 
This new Create Account step must use the exact same styling system already established for Page 
1. 
Page Background 
#0F1317 
 
Modal/Card 
Existing Graphite Ink surface

## SOURCE PAGE 101

Borders 
Existing Graphite Ink borders 
 
Typography 
Existing LOOP-MIND typography 
 
Buttons 
Existing LOOP-MIND button styling 
 
Inputs 
Existing LOOP-MIND input styling 
 
Dropdowns 
Existing LOOP-MIND dropdown styling 
No new visual theme is permitted. 
 
24. Icons 
The profile-photo options require matching icons: 
Camera → Camera icon 
Photos → Image/photo icon 
Files → Attachment/file icon 
They must visually belong to the same LOOP-MIND icon system. 
Do not use unrelated icon styles. 
 
25. Complete Updated Create Account Flow 
LOGIN 
 │ 
 └── Create account 
       │ 
       ▼

## SOURCE PAGE 102

CREATE A STUDENT PROFILE 
       │ 
       ├── +91 
       ├── Mobile no. 
       └── Get OTP 
              │ 
              ▼ 
          ENTER OTP 
              │ 
              ├── Wrong 
              │     ↓ 
              │  Incorrect OTP, please try again 
              │ 
              └── Valid 4-digit OTP 
                    │ 
                    ▼ 
              AUTOMATICALLY 
              PROCEED 
                    │ 
                    ▼ 
             BASIC INFORMATION 
                    │ 
                    ├── Full Name 
                    ├── Date of birth 
                    │     ├── Day 
                    │     ├── Month 
                    │     └── Year 
                    ├── Gender 
                    │     ├── Male 
                    │     ├── Female 
                    │     └── Others

## SOURCE PAGE 103

├── Profile Photo [OPTIONAL] 
                    │     ├── Camera 
                    │     ├── Photos 
                    │     └── Files 
                    │          └── Maximum 1 photo 
                    ├── Email Address 
                    ├── Country [Searchable] 
                    ├── State [Searchable] 
                    ├── City [Searchable] 
                    │ 
                    └── Continue 
                           │ 
                           ▼ 
                  NEXT CREATE ACCOUNT FLOW 
                       [DEFINED LATER] 
 
26. Important Implementation Boundaries 
Do not invent the following: 
• 
Next page after Continue. 
• 
Additional profile fields. 
• 
Additional gender options. 
• 
Profile-photo requirements. 
• 
Photo file-size limits. 
• 
Supported image formats. 
• 
Email verification flow. 
• 
Location verification. 
• 
Any additional account setup steps. 
• 
Any post-Continue workflow. 
Those remain future specifications. 
 
27. Acceptance Criteria

## SOURCE PAGE 104

• 
Valid OTP from Create Account side automatically enters Basic Information. 
• 
It never enters the Login-side destination. 
• 
Basic Information appears as the next Create Account step. 
• 
Basic Information heading is present. 
• 
Full Name field is present. 
• 
Date of birth has Day / Month / Year. 
• 
Gender has Male / Female / Others. 
• 
Profile Photo is explicitly optional. 
• 
Clicking Profile Photo shows Camera / Photos / Files. 
• 
Only one photo can be uploaded. 
• 
Zero photos is allowed. 
• 
Camera selection is supported where the device/browser permits it. 
• 
Photos selection is supported. 
• 
Files selection is supported. 
• 
Email Address field is present. 
• 
Country dropdown is searchable. 
• 
State dropdown is searchable. 
• 
City dropdown is searchable. 
• 
State options depend on selected Country. 
• 
City options depend on selected State. 
• 
Missing datasets may be meaningfully generated at implementation time. 
• 
Generated datasets must be contextually meaningful and internally consistent. 
• 
Continue remains disabled until all required information is complete. 
• 
Profile Photo does not block Continue. 
• 
No unsupported fields or workflow steps are invented.

## UPDATE — LinkedIn Profile option (UPDATE SDD §5-12; superseded by Student Create Account UPDATE SDD §5-6)

Below the existing Basic Information content (card layout otherwise
unchanged): a LinkedIn Profile option. This triggers the LinkedIn
Profile Extraction Agent (Python + LangChain + Gemini 2.5 Flash,
agents/llm.py), which maps only the skills, certifications, and
projects genuinely present onto the student's profile data — never
fabricating a value that isn't there. On success, Continue skips the
remaining manual onboarding steps and goes straight to Recruitment
History + Consent (the consent gate on Create Account is unchanged).
This is optional — a student who does not use it continues through
every step as before (Path A, unchanged).

**Superseded input mechanism**: the field originally took a pasted copy
of the student's profile text (no live LinkedIn access existed in this
environment). The Student Create Account UPDATE SDD explicitly requires
URL-only input instead — the student provides only their LinkedIn
profile URL, and the backend does a best-effort unauthenticated fetch of
that URL's public content (LinkedIn requires login for real profile
data, so this typically finds little or nothing) before handing whatever
text comes back to the same extraction agent, unchanged. No pasted text
field exists anymore.

## UPDATE — LinkedIn extraction now automatic, all-or-nothing (LinkedIn Auto-Extraction UPDATE SDD)

Extraction now starts immediately once the student enters a plausible LinkedIn URL (on the
field losing focus) — no separate "Extract"/"Continue with LinkedIn" button exists anymore.
The shortcut is only ever treated as successful when at least one skill, certification, or
project was genuinely found; a technically-successful call that found nothing is treated the
same as a failure, never a partial success. On failure (network error or nothing found), the
LinkedIn URL field is cleared (both on screen and in the stored draft) and a failure message
is shown; the student is not blocked and continues through the normal manual flow. Basic
Information's own core identity fields (name, date of birth, gender, email, location) still
require manual entry either way — LinkedIn's best-effort text fetch was never a source for
those and this update doesn't change that; only the skip of the *other* onboarding
cards (Academic Information through Professional Links + Resume) depends on a successful
extraction.

## UPDATE — Profile Photo upload fix

The optional profile-photo upload previously failed with "Save Basic
Information before uploading a photo" because the file was sent to the
backend before the Basic Information record existed. The photo is now
held client-side and uploaded immediately after Continue's save
succeeds — still optional, still exactly one photo, no other behavior
changed.

## SOURCE PAGE 105

• 
Same Page 1 modal/card visual system is maintained. 
• 
Same background is maintained. 
• 
Same fonts, colors, buttons, inputs, cards, dropdowns and icons are maintained. 
• 
spec.md and phase.md are cross-checked before implementation. 
• 
New requirements are merged without duplication. 
• 
Both files are cross-checked again after implementation for omissions, repetition and 
contradictions. 
• 
Any missing dataset is generated/populated only when this functionality is actually 
implemented, not beforehand. 
LOOP-MIND — SDD UPDATE 
Create Account — Academic Information 
This is the next Create Account step after the Basic Information card/modal. It must follow the 
same Page 1 modal/card interaction and the exact established LOOP-MIND styling/background. 
 
1. Navigation 
When the user clicks Continue on the previous Basic Information card/modal: 
Basic Information 
       │ 
       │ Continue 
       ▼ 
Academic Information 
       │ 
       ├── Back 
       │ 
       └── Continue 
              │ 
              ▼ 
       Next Create Account Flow 
       [To be specified later] 
The Academic Information card/modal appears on the same Page 1, using the same modal/card 
mechanism.

## SOURCE PAGE 106

2. Academic Information — Exact Text 
The card heading must be: 
Academic Information 
The fields shown in the supplied sketch are: 
College 
Degree 
Branch 
 
Academic year 
Current year 
Current semester 
 
Admission year 
Expected graduation year 
 
Current CGPA 
CGPA scale 
 
10th score in percentage 
12th / Diploma score in percentage 
 
Back 
Continue 
Do not replace these with different terminology. 
 
3. Academic Information Layout 
The structure should follow the supplied sketch: 
┌─────────────────────────────────────────────────────────────┐ 
│                                                             │ 
│                  Academic Information                       │

## SOURCE PAGE 107

│                                                             │ 
│       College          Degree           Branch              │ 
│          ▼               ▼                ▼                 │ 
│                                                             │ 
│       Academic year    Current year    Current semester     │ 
│              ▼              ▼                 ▼             │ 
│                                                             │ 
│       Admission year       Expected graduation year         │ 
│              ▼                       ▼                      │ 
│                                                             │ 
│       Current CGPA             CGPA scale                   │ 
│                                                             │ 
│       10th score in percentage                  optional    │ 
│                                                             │ 
│       12th / Diploma score in percentage        optional    │ 
│                                                             │ 
│                                                             │ 
│       Back                              Continue             │ 
│                                                             │ 
└─────────────────────────────────────────────────────────────┘ 
The actual UI must visually match the existing LOOP-MIND design system rather than literally 
reproducing the hand-drawn borders. 
 
4. College 
Display: 
College ▼ 
as a searchable dropdown. 
The college dataset must be relevant to the project context. 
If the user has not supplied the dataset, it may be generated/populated automatically at 
implementation time. 
Do not generate a meaningless/random list.

## SOURCE PAGE 108

5. Degree 
Display: 
Degree ▼ 
as a searchable dropdown. 
The available values must be relevant to academic profile creation. 
The dataset must be generated/populated when this functionality is implemented if no dataset has 
been supplied. 
 
6. Branch 
Display: 
Branch ▼ 
as a searchable dropdown. 
Branch options should be contextually related to the selected Degree. 
For example, the implementation must not present unrelated branch choices when the selected 
degree makes certain branches irrelevant. 
The exact branch dataset is not supplied in the sketch, so do not claim a specific predefined dataset. 
 
7. Academic Year 
Display: 
Academic year ▼ 
as a searchable/selectable dropdown. 
The available values must be meaningful for the selected academic context. 
 
8. Current Year 
Display: 
Current year ▼ 
as a selectable/searchable dropdown. 
The values should represent the student's current academic year. 
The relationship between Degree, Academic year, and Current year should remain logically 
consistent. 
 
9. Current Semester

## SOURCE PAGE 109

Display: 
Current semester ▼ 
as a selectable/searchable dropdown. 
The available semester choices must be appropriate to the selected degree/program structure. 
It must not expose arbitrary semester values unrelated to the selected academic program. 
 
10. Admission Year 
Display: 
Admission year ▼ 
as a searchable/selectable dropdown. 
The selected value must be compatible with the academic timeline. 
 
11. Expected Graduation Year 
Display: 
Expected graduation year ▼ 
as a searchable/selectable dropdown. 
The value must be contextually consistent with the selected academic program and admission 
information. 
 
12. Current CGPA 
Display: 
Current CGPA 
as an input field. 
The user must be able to enter their current CGPA. 
The value should be validated against the selected CGPA scale. 
 
13. CGPA Scale 
Display: 
CGPA scale 
as a selectable/searchable dropdown. 
The scale determines how the Current CGPA should be interpreted.

## SOURCE PAGE 110

The exact available scales are not specified in the supplied sketch, therefore do not hard-code a 
specific list into the SDD as if it were user-defined. 
The implementation may provide an appropriate dataset when this functionality is implemented. 
 
14. 10th Score 
Display exactly: 
10th score in percentage 
This field is: 
OPTIONAL 
Therefore: 
10th score provided → valid 
10th score omitted  → valid 
It must not prevent the user from continuing. 
 
15. 12th / Diploma Score 
Display exactly: 
12th / Diploma score in percentage 
This field is: 
OPTIONAL 
Therefore it must not prevent the user from continuing when left empty. 
 
16. Optional Fields 
The supplied sketch explicitly marks both of these as optional: 
10th score in percentage 
12th / Diploma score in percentage 
Therefore: 
Required academic information 
        + 
Optional 10th score 
        + 
Optional 12th / Diploma score

## SOURCE PAGE 111

The optional fields must never disable the ability to continue when all required information is 
otherwise complete. 
 
17. Searchable Dropdown System 
All dropdowns required by this screen must support search. 
This applies to: 
College 
Degree 
Branch 
Academic year 
Current year 
Current semester 
Admission year 
Expected graduation year 
CGPA scale 
The search should filter the available options rather than requiring the user to manually browse a 
large list. 
 
18. Context-Aware Dataset Generation 
The implementation must follow this rule: 
Dataset supplied by user? 
       │ 
       ├── YES 
       │    ↓ 
       │ Use supplied dataset 
       │ 
       └── NO 
            ↓ 
       Generate/populate meaningful dataset 
       at implementation time 
Datasets must be meaningful to the actual academic context. 
Examples of relationships that should be respected:

## SOURCE PAGE 112

Degree 
  ↓ 
Relevant Branches 
 
Admission Year 
  + 
Academic Program 
  ↓ 
Expected Graduation Year 
 
Current Year 
  + 
Current Semester 
  ↓ 
Academic Progress 
Do not generate datasets before implementation merely for the sake of having data available. 
 
19. Required vs Optional 
Based strictly on the supplied sketch: 
Field 
Requirement 
College 
Required 
Degree 
Required 
Branch 
Required 
Academic year 
Required 
Current year 
Required 
Current semester 
Required 
Admission year 
Required 
Expected graduation year 
Required 
Current CGPA 
Required

## SOURCE PAGE 113

Field 
Requirement 
CGPA scale 
Required 
10th score in percentage 
Optional 
12th / Diploma score in percentage Optional 
No additional required/optional status should be invented beyond this specification. 
 
20. Continue Button 
The sketch explicitly indicates: 
button only activates after user selecting everything required 
Therefore: 
Required fields incomplete 
        ↓ 
Continue = DISABLED 
 
All required fields completed 
        ↓ 
Continue = ACTIVE 
The optional fields do not affect Continue activation. 
 
21. Back Button 
The sketch explicitly states: 
Back 
↓ 
always active 
Therefore Back must always remain active. 
Clicking Back must return to the previous: 
Basic Information 
card/modal. 
It must not depend on whether the Academic Information fields are complete.

## SOURCE PAGE 114

22. Back Navigation 
Academic Information 
       │ 
       │ Back 
       ▼ 
Basic Information 
Previously entered Basic Information should not be unnecessarily discarded when navigating 
backward. 
No additional navigation behavior is specified at this stage. 
 
23. Continue Navigation 
When all required Academic Information has been completed: 
Academic Information 
       │ 
       │ Continue 
       ▼ 
Next Create Account Flow 
The next flow is not specified yet. 
Therefore do not invent the next page/card/modal. 
 
24. Same Page 1 Requirement 
This is not a separate website page. 
It is another step/card/modal within the existing Page 1 Create Account process. 
PAGE 1 
│ 
├── Login Modal 
│ 
├── Create Account Modal 
│ 
├── Create Account OTP Modal 
│

## SOURCE PAGE 115

├── Basic Information Modal 
│ 
└── Academic Information Modal  ← THIS UPDATE 
The underlying Page 1 remains the same. 
 
25. Global Styling — Strict 
The Academic Information card/modal must use exactly the same visual system already established 
for Page 1. 
No new theme is permitted. 
This includes: 
• 
Same background. 
• 
Same modal/card styling. 
• 
Same typography. 
• 
Same font treatment. 
• 
Same border treatment. 
• 
Same input styling. 
• 
Same dropdown styling. 
• 
Same button styling. 
• 
Same colours. 
• 
Same spacing language. 
• 
Same icon style. 
• 
Same interaction styling. 
The Academic Information screen must look like it belongs to the same application and same Page 1 
flow. 
 
26. No Independent Page Background 
Do not introduce a new background for this modal. 
Page 1 background 
       ↓ 
Academic Information modal 
The established Page 1 background remains unchanged.

## SOURCE PAGE 116

27. Complete Updated Flow 
PAGE 1 
 │ 
 ▼ 
Login 
 │ 
 ▼ 
Login Card / Modal 
 │ 
 └── Create account 
       │ 
       ▼ 
Create a Student Profile 
       │ 
       ▼ 
Enter OTP 
       │ 
       ├── Incorrect OTP 
       │      ↓ 
       │  Incorrect OTP, please try again 
       │ 
       └── Valid 4-digit OTP 
              │ 
              ▼ 
       Automatically proceed 
              │ 
              ▼ 
       Basic Information 
              │ 
              │ Continue 
              ▼

## SOURCE PAGE 117

Academic Information 
              │ 
              ├── Back 
              │     ↓ 
              │ Basic Information 
              │ 
              └── Continue 
                    │ 
                    ▼ 
             Next Create Account Flow 
             [To be specified later] 
 
28. Updated Acceptance Criteria 
• 
Clicking Continue from Basic Information opens Academic Information. 
• 
Academic Information appears as a card/modal on the same Page 1. 
• 
Heading is exactly Academic Information. 
• 
College exists as a searchable dropdown. 
• 
Degree exists as a searchable dropdown. 
• 
Branch exists as a searchable dropdown. 
• 
Academic year exists as a searchable dropdown. 
• 
Current year exists as a searchable dropdown. 
• 
Current semester exists as a searchable dropdown. 
• 
Admission year exists as a searchable dropdown. 
• 
Expected graduation year exists as a searchable dropdown. 
• 
Current CGPA exists. 
• 
CGPA scale exists as a selectable/searchable dropdown. 
• 
10th score in percentage exists and is optional. 
• 
12th / Diploma score in percentage exists and is optional.

## SOURCE PAGE 118

• 
Dropdown datasets are contextually meaningful. 
• 
Missing datasets are generated/populated at implementation time. 
• 
Degree/Branch relationship is context-aware. 
• 
Academic timeline selections remain contextually consistent. 
• 
Continue is disabled until all required information is completed. 
• 
Optional 10th score does not block Continue. 
• 
Optional 12th/Diploma score does not block Continue. 
• 
Back is always active. 
• 
Back returns to Basic Information. 
• 
Continue proceeds only to the next flow that will be specified later. 
• 
No future flow is invented. 
• 
Existing Page 1 background remains unchanged. 
• 
Existing Page 1 styling remains unchanged. 
• 
No new colours, fonts, themes, or visual systems are introduced. 
• 
spec.md and phase.md must be cross-checked before implementation. 
• 
Existing requirements must be preserved without duplication. 
• 
After implementation, spec.md and phase.md must be cross-checked again for 
omissions, duplication, or contradictions. 
• 
Any required dataset not supplied by the user is generated/populated only at 
implementation time. 
LOOP-MIND — SDD UPDATE 
Create Account — Current Skills 
This is the next Create Account card/modal after Academic Information. It must appear on the 
same Page 1, using the exact existing Page 1 background, modal/card system, typography, colours, 
controls, spacing language and overall styling. 
 
1. Navigation 
When the user clicks Continue from the previous Academic Information card/modal:

## SOURCE PAGE 119

Academic Information 
        │ 
        │ Continue 
        ▼ 
Current Skills 
        │ 
        ├── Back 
        │ 
        └── Continue 
              │ 
              ▼ 
       Next Create Account Flow 
       [To be specified later] 
This is another Create Account step, not a new website page. 
 
2. Current Skills — Exact Heading 
The card heading must be: 
Current Skills 
Do not rename it. 
 
3. Current Skills Card Structure 
The supplied sketch contains: 
Current Skills 
 
Skill Name 
Skill category ▼ 
Proficiency ▼ 
Learning Status ▼ 
Experience in years 
 
Evidence

## SOURCE PAGE 120

→ on click add project or supporting evidence 
 
Back 
Continue 
 
4. Skill Entry 
A skill entry consists of the following information: 
┌──────────────────────────────────────┐ 
│ Skill Name                           │ 
│                                      │ 
│ Skill category ▼                     │ 
│                                      │ 
│ Proficiency ▼                        │ 
│                                      │ 
│ Learning Status ▼                    │ 
│                                      │ 
│ Experience in years                  │ 
│                                      │ 
│ Evidence                             │ 
│ → add project or supporting evidence │ 
└──────────────────────────────────────┘ 
The implementation must preserve this structure. 
 
5. Skill Name 
Display: 
Skill Name 
as an input. 
The user enters the name of the skill. 
No specific skill list is mandated by the sketch. 
 
6. Skill Category

## SOURCE PAGE 121

Display: 
Skill category ▼ 
as a dropdown. 
It must be searchable. 
The options must be meaningful to the skill being entered. 
If a dataset is not provided by the user, the required dataset may be generated/populated at 
implementation time. 
Do not generate the dataset beforehand. 
 
7. Proficiency 
Display: 
Proficiency ▼ 
as a dropdown. 
It must be searchable/selectable. 
The available values must represent meaningful levels of skill proficiency. 
The supplied sketch does not define the exact proficiency values, so do not claim a specific fixed list 
as user-provided. 
 
8. Learning Status 
Display: 
Learning Status ▼ 
as a dropdown. 
It must be searchable/selectable. 
The values must represent meaningful learning states relevant to a student's skill. 
The exact values are not specified in the sketch and therefore must not be falsely presented as 
explicitly defined requirements. 
 
9. Experience in Years 
Display: 
Experience in years 
as an input. 
The user should be able to provide the amount of experience associated with the skill.

## SOURCE PAGE 122

The exact numeric range/format is not specified in the supplied sketch, so do not invent a specific 
range in the specification. 
 
10. Evidence 
Display: 
Evidence 
The sketch specifies: 
Evidence 
   ↓ 
on click 
   ↓ 
add project or supporting evidence 
Therefore Evidence is an interactive control. 
Clicking it must allow the user to add: 
Project 
or 
Supporting evidence 
The exact evidence-entry interface is not defined in the supplied sketch. 
Therefore, do not invent the detailed evidence workflow yet. 
 
11. Multiple Skill Entries 
The annotation beside the skill-entry section states: 
multiple entries 
optional also 
Therefore the Current Skills section must support multiple skill entries. 
Conceptually: 
Current Skills 
 
Skill Entry 1 
   ↓ 
Skill Entry 2

## SOURCE PAGE 123

↓ 
Skill Entry 3 
   ↓ 
... 
The user must not be restricted to entering only one skill. 
 
12. Skills Are Optional 
The supplied sketch indicates that the Current Skills entries are optional. 
Therefore the user must be able to proceed without being forced to create a skill entry. 
No skill entry 
     ↓ 
Allowed 
 
One skill 
     ↓ 
Allowed 
 
Multiple skills 
     ↓ 
Allowed 
Do not make Current Skills mandatory unless a later specification explicitly changes this. 
 
13. Searchable Dropdown Requirement 
The dropdowns on this card must use the established searchable-dropdown system. 
Required searchable dropdowns: 
Skill category 
Proficiency 
Learning Status 
Search must operate within the relevant option set. 
 
14. Context-Aware Dataset Generation

## SOURCE PAGE 124

If the user has not supplied datasets for the dropdowns: 
Dataset supplied? 
      │ 
 ┌────┴────┐ 
YES       NO 
 │         │ 
Use       Generate meaningful 
provided  contextual dataset 
dataset   at implementation time 
Generated data must be meaningful for: 
Skill category 
Proficiency 
Learning Status 
It must not be arbitrary filler data. 
The dataset must be generated/populated when the functionality is implemented, not beforehand. 
 
15. Back Button 
The sketch explicitly states: 
Back 
 ↓ 
always active 
Therefore: 
Back must always be active. 
Clicking Back returns to: 
Current Skills 
      │ 
      │ Back 
      ▼ 
Academic Information 
Previously entered Academic Information must not be unnecessarily discarded.

## SOURCE PAGE 125

16. Continue Button 
The sketch specifies: 
Continue 
 
button only activates only 
after user selecting 
everything required 
Therefore the implementation must determine completion based on the required information for 
the Current Skills step. 
Because the sketch indicates that Current Skills entries are optional, the absence of a skill entry must 
not itself block the flow. 
If a skill entry is created, its required fields must be completed before that entry is treated as 
complete. 
No skill entry 
      ↓ 
Continue can remain available 
provided no incomplete entry exists 
 
Skill entry started 
      ↓ 
Required information incomplete 
      ↓ 
Continue disabled 
 
Required information complete 
      ↓ 
Continue active 
The exact individual required/optional status of fields inside a created skill entry is not explicitly 
defined by the sketch, so do not invent additional validation requirements beyond what is necessary 
to prevent an incomplete created entry from being submitted. 
 
17. Multiple Entry Behaviour 
The intended structure is:

## SOURCE PAGE 126

Current Skills 
      │ 
      ├── Skill Entry 1 
      │ 
      ├── Skill Entry 2 
      │ 
      ├── Skill Entry 3 
      │ 
      └── ... 
Each entry represents a separate skill. 
Evidence belongs to the corresponding skill entry. 
 
18. Evidence Relationship 
Evidence must remain associated with the relevant skill. 
Skill A 
 └── Evidence 
      ├── Project 
      └── Supporting evidence 
 
Skill B 
 └── Evidence 
      ├── Project 
      └── Supporting evidence 
Do not create a single unrelated global evidence section. 
 
19. Same Modal/Card Behaviour 
The Current Skills interface must use the same modal/card mechanism established for the previous 
Create Account steps. 
PAGE 1 
 │ 
 └── Create Account Flow

## SOURCE PAGE 127

│ 
       ├── Basic Information 
       ├── Academic Information 
       └── Current Skills  ← current step 
The underlying Page 1 remains visible according to the established Page 1 modal behaviour. 
 
20. Global Styling — STRICT 
No new styling is permitted. 
Current Skills must use exactly the same established Page 1 design system: 
• 
Same background. 
• 
Same colours. 
• 
Same fonts. 
• 
Same typography. 
• 
Same modal/card appearance. 
• 
Same borders. 
• 
Same inputs. 
• 
Same dropdowns. 
• 
Same buttons. 
• 
Same spacing system. 
• 
Same icon style. 
• 
Same interaction states. 
• 
Same responsive behaviour pattern. 
Do not create a separate Current Skills theme. 
 
21. Complete Flow So Far 
PAGE 1 
 │ 
 ▼ 
Login 
 │ 
 ▼

## SOURCE PAGE 128

Create account 
 │ 
 ▼ 
Create a Student Profile 
 │ 
 ▼ 
Create Account OTP 
 │ 
 │ Valid 4-digit OTP 
 ▼ 
Automatically proceed 
 │ 
 ▼ 
Basic Information 
 │ 
 │ Continue 
 ▼ 
Academic Information 
 │ 
 │ Continue 
 ▼ 
Current Skills 
 │ 
 ├── Skill Name 
 ├── Skill category ▼ 
 ├── Proficiency ▼ 
 ├── Learning Status ▼ 
 ├── Experience in years 
 │ 
 ├── Evidence 
 │      └── Add project or supporting evidence

## SOURCE PAGE 129

│ 
 ├── Multiple skill entries supported 
 │ 
 ├── Skills optional 
 │ 
 ├── Back 
 │      └── Always active 
 │ 
 └── Continue 
        │ 
        ▼ 
   Next Create Account Flow 
   [To be specified later] 
 
22. Acceptance Criteria 
• 
Clicking Continue from Academic Information opens Current Skills. 
• 
Current Skills appears on the same Page 1. 
• 
Heading is exactly Current Skills. 
• 
Skill Name is present. 
• 
Skill category is present. 
• 
Proficiency is present. 
• 
Learning Status is present. 
• 
Experience in years is present. 
• 
Evidence is present. 
• 
Clicking Evidence provides the ability to add project/supporting evidence. 
• 
Multiple skill entries are supported. 
• 
Current Skills entries are optional. 
• 
Skill category is searchable.

## SOURCE PAGE 130

• 
Proficiency is searchable/selectable. 
• 
Learning Status is searchable/selectable. 
• 
Missing dropdown datasets may be generated at implementation time. 
• 
Generated datasets must be meaningful to the academic/student skill context. 
• 
Datasets must not be generated beforehand. 
• 
Back is always active. 
• 
Back returns to Academic Information. 
• 
Continue follows the established required-information activation rule. 
• 
An incomplete skill entry cannot be submitted as a completed entry. 
• 
Absence of a skill entry does not itself block the flow because skills are optional. 
• 
Evidence remains associated with its corresponding skill. 
• 
No future Create Account step is invented. 
• 
Same Page 1 background is maintained. 
• 
Same Page 1 styling is maintained without introducing new colours/fonts/themes. 
• 
spec.md and phase.md must be cross-checked before implementation. 
• 
Existing requirements must be merged without duplication. 
• 
spec.md and phase.md must be cross-checked after implementation for omissions, 
repetition and contradictions. 
• 
Any missing datasets are generated/populated only at implementation time. 
SDD — Student Profile: Coding Experience 
1. Feature Overview 
Feature Name: Coding Experience 
Flow Position: Next step after Current Skills card/modal 
Display Mode: Same centered card/modal pattern used throughout the Page 1 onboarding flow. 
Purpose: Collect the student's coding/programming experience relevant to their profile. 
The implementation must follow the existing Page 1 visual system exactly: same background, 
typography, borders, spacing language, controls, buttons, colors, card/modal treatment, and 
overall styling. No new visual style should be introduced.

## SOURCE PAGE 131

2. Entry Condition 
When the student clicks Continue on the previous Current Skills card/modal: 
Current Skills 
      ↓ 
Click Continue 
      ↓ 
Coding Experience card/modal 
The Coding Experience interface appears on the same Page 1. 
It must not navigate to a separate page at this stage. 
 
3. Coding Experience Card 
Card heading 
Coding Experience 
The heading is positioned at the top/centre area of the card consistent with the previous onboarding 
cards. 
 
4. Fields 
4.1 Coding Experience 
A field labelled: 
Coding Experience 
The source sketch shows this as an input/selection area. 
The exact underlying value options are not specified in the provided sketch, therefore do not invent 
additional requirements. 
 
4.2 Programming Languages 
Field label: 
Programming Languages 
This must be a dropdown/searchable selection control. 
The sketch explicitly shows example language options: 
• 
Python 
• 
Java 
• 
JavaScript

## SOURCE PAGE 132

• 
…… 
The control should support selecting programming languages according to the project's coding-
profile context. 
Selection behaviour 
Because the Coding Experience section represents a student's coding experience, the 
implementation should support the student's selected programming languages. 
If multiple programming languages are selected, they should remain represented within the 
field/control rather than replacing previously selected languages. 
The exact maximum number of languages is not specified in the sketch. 
 
5. DSA Experience 
Field/section: 
DSA Experience 
The sketch shows this as a selection field. 
 
5.1 Competitive Programming 
A field labelled: 
Competitive Programming 
with a dropdown/selection control. 
The sketch explicitly specifies these levels: 
• 
Beginner 
• 
Inter-mediate 
• 
Expert 
These are the selectable levels shown in the provided design. 
 
6. Coding Platforms 
Field: 
Coding Platforms 
The sketch shows multiple selection/dropdown areas associated with Coding Platforms. 
Therefore, the implementation should allow the student to provide their coding-platform 
experience. 
The exact platform list is not specified in the provided sketch, so platform names should not be 
hard-coded based on assumptions at the specification stage.

## SOURCE PAGE 133

The platform selector should be searchable and context-appropriate when implemented. 
 
7. GitHub Link 
Field: 
Git-hub link 
Provide an input for the student's GitHub profile/link. 
The field should accept a GitHub URL. 
The sketch does not specify any additional GitHub validation behaviour, so no additional validation 
requirements should be invented beyond basic valid-input handling required for implementation. 
 
8. Multiple Coding Experience Entries 
Mandatory requirement 
Multiple coding experience entries are allowed. 
The system must therefore not restrict the student to a single Coding Experience record. 
Conceptually: 
Coding Experience Entry 1 
        ↓ 
Coding Experience Entry 2 
        ↓ 
Coding Experience Entry 3 
        ↓ 
        ... 
The student should be able to maintain multiple coding-experience entries where applicable. 
Each entry follows the same Coding Experience structure defined by this SDD. 
The exact UI mechanism for adding another entry is not explicitly shown in the sketch, so do not 
introduce an unrequested button label or interaction design as a fixed requirement. 
 
9. Navigation Controls 
Back 
Button: 
Back 
Behaviour:

## SOURCE PAGE 134

Click Back 
      ↓ 
Return to previous 
Current Skills card/modal 
The Back button is shown as active in the sketch. 
 
Continue 
Button: 
Continue 
The Continue button is positioned toward the lower-right portion of the card, consistent with the 
sketch. 
It should become active only after the required information for this Coding Experience step has 
been completed. 
The exact required/optional status of every Coding Experience field is not explicitly defined in the 
provided sketch, so do not invent mandatory fields. 
 
10. Searchable Dropdown Requirement 
All dropdowns in this step that require choosing from a potentially large contextual dataset should 
be implemented as searchable dropdowns. 
This includes, where applicable: 
• 
Programming Languages 
• 
Competitive Programming level 
• 
Coding Platforms 
The available datasets/options should be generated or populated at implementation time, not pre-
generated unnecessarily beforehand. 
Any generated dataset must be: 
• 
meaningful to the Coding Experience context 
• 
internally consistent 
• 
suitable for the corresponding field 
• 
searchable 
• 
free of unrelated values 
 
11. Data Structure Concept

## SOURCE PAGE 135

The Coding Experience information should conceptually be represented as repeatable records: 
Coding Experience 
├── Coding Experience 
├── Programming Languages 
├── DSA Experience 
├── Competitive Programming 
├── Coding Platforms 
└── GitHub Link 
With multiple records permitted: 
Student 
└── Coding Experiences[] 
    ├── Coding Experience Entry 1 
    ├── Coding Experience Entry 2 
    ├── Coding Experience Entry 3 
    └── ... 
This is a structural representation only; exact backend schema/API implementation is not specified 
by the sketch and must not be fabricated at this stage. 
 
12. Visual / Styling Requirements 
This Coding Experience card must use exactly the established Page 1 design system. 
Background 
Same Page 1 background — strictly unchanged. 
Card 
• 
Same card/modal appearance 
• 
Same border treatment 
• 
Same visual language 
• 
Same positioning 
• 
Same proportions/presentation style 
• 
Same spacing principles 
Typography 
Use the same font, font sizing hierarchy, text treatment, and alignment system already established 
for Page 1.

## SOURCE PAGE 136

Controls 
All: 
• 
inputs 
• 
dropdowns 
• 
searchable dropdowns 
• 
buttons 
• 
links 
• 
validation states 
must visually match the established Page 1 styling. 
Colors 
Do not introduce new colors. 
All colors must be derived from the established Page 1 background/style system. 
Icons / Logos 
Where icons are required, automatically generate/select appropriate icons that visually match the 
established Page 1 style. 
Do not introduce unrelated branding or icon styles. 
 
13. Interaction Flow 
PAGE 1 
  │ 
  └── Current Skills Card/Modal 
          │ 
          │ Continue 
          ↓ 
  Coding Experience Card/Modal 
          │ 
          ├── Coding Experience 
          │ 
          ├── Programming Languages 
          │ 
          ├── DSA Experience

## SOURCE PAGE 137

│ 
          ├── Competitive Programming 
          │ 
          ├── Coding Platforms 
          │ 
          ├── Git-hub link 
          │ 
          ├── Multiple Coding Experience Entries 
          │ 
          ├── Back 
          │      ↓ 
          │   Current Skills 
          │ 
          └── Continue 
                 ↓ 
             Next onboarding 
             step to be specified later 
 
14. Scope Boundary 
Explicitly defined by the sketch 
• 
Coding Experience card/modal 
• 
Same Page 1 
• 
Coding Experience field 
• 
Programming Languages dropdown 
• 
Python / Java / JavaScript shown as example options 
• 
DSA Experience 
• 
Competitive Programming 
• 
Beginner / Inter-mediate / Expert 
• 
Coding Platforms 
• 
Git-hub link 
• 
Back button

## SOURCE PAGE 138

• 
Continue button 
• 
Multiple coding experience entries allowed 
• 
Searchable/contextual dropdown requirement 
• 
Existing Page 1 styling must remain unchanged 
Not specified and therefore must NOT be invented 
• 
Exact Coding Experience option list 
• 
Exact Coding Platform list 
• 
Maximum number of coding-experience entries 
• 
Exact validation rules for every field 
• 
Exact next page/step after Continue 
• 
Backend API structure 
• 
Database schema 
• 
AI processing 
• 
Scoring logic 
• 
Any additional fields not visible in the sketch 
 
15. Single Source of Truth Rule 
This SDD becomes the specification for the Coding Experience portion of Page 1. 
During implementation: 
1. Cross-check the existing spec.md. 
2. Cross-check the existing phase.md. 
3. Add only the requirements introduced by this Coding Experience design. 
4. Do not duplicate requirements already documented. 
5. Do not remove previously established Page 1 requirements. 
6. Preserve all previously established styling requirements. 
7. After implementation, cross-check the implemented result against both spec.md and 
phase.md. 
8. Any datasets required for this feature should be generated at implementation time, and 
only when required. 
9. Do not hallucinate unspecified functionality. 
10. The next onboarding behaviour remains unspecified until the next design is provided. 
SDD — PROJECTS

## SOURCE PAGE 139

1. Feature Overview 
Feature Name: Projects 
Flow Position: Next step after the previous onboarding Coding Experience card/modal. 
Display Mode: Same centered card/modal pattern used throughout the Page 1 onboarding flow. 
When the student clicks Continue on the previous card/modal, the PROJECTS card/modal must 
appear on the same Page 1. 
Coding Experience 
        ↓ 
    Continue 
        ↓ 
PROJECTS card/modal 
No separate page navigation is introduced by this requirement. 
 
2. Projects Card / Modal 
The card must contain the heading: 
PROJECTS 
The layout must follow the provided structure. 
┌──────────────────────────────────────────────────────────────┐ 
│                                                              │ 
│                         PROJECTS                             │ 
│                                                              │ 
│                                                              │ 
│ Project Name                                                 │ 
│ Project Description                                          │ 
│ Project Type                                                 │ 
│ Project Status                                               │ 
│ Start Date                                                   │ 
│ End Date                                                     │ 
│                                                              │ 
│ Technologies Used                                            │ 
│ Programming Languages                                        │ 
│ Frameworks                                                   │

## SOURCE PAGE 140

│ Tools                                                        │ 
│ Skills Demonstrated                                          │ 
│ Student's Role                                               │ 
│ Team / Individual                                            │ 
│                                                              │ 
│ GitHub Repository                                            │ 
│ Live Demo                                                    │ 
│ Project Documentation                                        │ 
│ Project Evidence                                             │ 
│                                                              │ 
│                                                              │ 
│ Back                                                   Continue│ 
│                                                              │ 
└──────────────────────────────────────────────────────────────┘ 
 
3. Project Information Fields 
The following fields must be included exactly as specified. 
Basic Project Information 
1. Project Name 
2. Project Description 
3. Project Type 
4. Project Status 
5. Start Date 
6. End Date 
Technical Information 
7. Technologies Used 
8. Programming Languages 
9. Frameworks 
10. Tools 
11. Skills Demonstrated 
Contribution Information

## SOURCE PAGE 141

12. Student's Role 
13. Team / Individual 
Project Links / Evidence 
14. GitHub Repository 
15. Live Demo 
16. Project Documentation 
17. Project Evidence 
No additional project fields should be added unless they are specified later. 
 
4. Multiple Project Entries 
Mandatory requirement 
Multiple project entries are allowed. 
The student must not be restricted to entering only one project. 
Conceptually: 
PROJECTS 
│ 
├── Project Entry 1 
├── Project Entry 2 
├── Project Entry 3 
└── ... 
Each project entry follows the same project-information structure defined above. 
The exact UI mechanism for adding another project entry is not specified in the provided design, so 
do not invent a specific button, label, or interaction for this at the specification stage. 
 
5. Navigation 
Back 
Button: 
Back 
Behaviour: 
Click Back 
     ↓

## SOURCE PAGE 142

Return to previous 
Coding Experience card/modal 
The Back control must remain consistent with the previous onboarding cards. 
 
Continue 
Button: 
Continue 
Behaviour: 
Click Continue 
     ↓ 
Proceed to the next onboarding step 
The next step is not specified yet. 
Therefore, no next-step page, card, modal, fields, or functionality should be invented. 
 
6. Contextual Searchable Inputs 
Where a project field requires selecting values from a dataset rather than entering free text, the 
appropriate control should be implemented as a searchable dropdown/selector. 
This applies where context requires selection, particularly for fields such as: 
• 
Project Type 
• 
Project Status 
• 
Technologies Used 
• 
Programming Languages 
• 
Frameworks 
• 
Tools 
• 
Skills Demonstrated 
The exact option datasets are not provided in the current design. 
Therefore: 
• 
Do not fabricate a fixed dataset in the SDD. 
• 
Generate/populate meaningful datasets at implementation time when required. 
• 
Generated values must be relevant to student projects and the specific field. 
• 
Searchability must be preserved for potentially large option sets.

## SOURCE PAGE 143

• 
Multi-selection should be supported where a field logically represents multiple 
technologies/languages/frameworks/tools/skills, but the exact UI behaviour should follow 
the eventual implementation requirements. 
 
7. Project Evidence 
The field: 
Project Evidence 
must be included as part of the project entry. 
The sketch does not specify the exact evidence-upload mechanism, file restrictions, number of 
evidence items, or supported formats. 
Therefore these details remain unspecified until explicitly defined. 
Do not invent them. 
 
8. Links 
The project contains: 
• 
GitHub Repository 
• 
Live Demo 
• 
Project Documentation 
These should provide appropriate input areas for the corresponding project resources. 
The exact validation rules for these links are not specified in the design and should not be invented 
in this SDD. 
 
9. Styling Requirements 
The Projects card/modal must use exactly the established Page 1 visual system. 
Background 
Exactly the same Page 1 background. 
No new background is permitted. 
Card / Modal 
Must match the existing onboarding card/modal styling: 
• 
same visual treatment 
• 
same border language 
• 
same proportions

## SOURCE PAGE 144

• 
same positioning 
• 
same spacing principles 
• 
same overall appearance 
Typography 
Use the established Page 1: 
• 
font 
• 
text hierarchy 
• 
sizing 
• 
weight 
• 
alignment 
• 
spacing 
No unrelated typography should be introduced. 
Colours 
Use exactly the established Page 1 colour system. 
Do not introduce arbitrary colours. 
Controls 
Inputs, dropdowns, selectors, buttons, upload controls, links, and validation states must visually 
match the established Page 1 design. 
 
10. Page 1 Behaviour 
The entire onboarding sequence continues to operate within Page 1 through centered 
cards/modals. 
PAGE 1 
 │ 
 ├── Login 
 │ 
 ├── Create Account 
 │ 
 ├── OTP 
 │ 
 ├── Basic Information 
 │

## SOURCE PAGE 145

├── Academic Information 
 │ 
 ├── Current Skills 
 │ 
 ├── Coding Experience 
 │ 
 └── PROJECTS 
       │ 
       ├── Project Entry 1 
       ├── Project Entry 2 
       ├── Project Entry 3 
       └── ... 
The Projects card/modal should therefore behave as another step in the same existing flow rather 
than creating a separate visual page. 
 
11. Data Structure Concept 
Conceptually: 
Student 
└── Projects[] 
    ├── Project 1 
    │   ├── Project Name 
    │   ├── Project Description 
    │   ├── Project Type 
    │   ├── Project Status 
    │   ├── Start Date 
    │   ├── End Date 
    │   ├── Technologies Used 
    │   ├── Programming Languages 
    │   ├── Frameworks 
    │   ├── Tools 
    │   ├── Skills Demonstrated

## SOURCE PAGE 146

│   ├── Student's Role 
    │   ├── Team / Individual 
    │   ├── GitHub Repository 
    │   ├── Live Demo 
    │   ├── Project Documentation 
    │   └── Project Evidence 
    │ 
    ├── Project 2 
    └── ... 
This is a functional representation of the requirement, not a finalized backend/database schema. 
 
12. Scope Boundary 
Explicitly defined 
• 
PROJECTS heading 
• 
Project Name 
• 
Project Description 
• 
Project Type 
• 
Project Status 
• 
Start Date 
• 
End Date 
• 
Technologies Used 
• 
Programming Languages 
• 
Frameworks 
• 
Tools 
• 
Skills Demonstrated 
• 
Student's Role 
• 
Team / Individual 
• 
GitHub Repository 
• 
Live Demo 
• 
Project Documentation 
• 
Project Evidence

## SOURCE PAGE 147

• 
Back 
• 
Continue 
• 
Multiple project entries allowed 
• 
Same Page 1 card/modal flow 
• 
Existing Page 1 styling must be preserved 
• 
Contextual searchable dropdowns where appropriate 
• 
Required datasets may be generated during implementation when needed 
Not specified 
• 
Exact Project Type options 
• 
Exact Project Status options 
• 
Exact technology/framework/tool/skill datasets 
• 
Maximum number of projects 
• 
Exact Add Project UI 
• 
Evidence upload rules 
• 
Evidence file formats 
• 
Evidence size limits 
• 
Backend schema 
• 
API endpoints 
• 
AI processing 
• 
Project scoring 
• 
Next onboarding step 
These must remain unspecified until provided. 
 
13. Single Source of Truth / Development Rule 
For implementation of this feature: 
1. Cross-check spec.md before development. 
2. Cross-check phase.md before development. 
3. Add the Projects requirements to the appropriate specification sections. 
4. Do not duplicate requirements already present. 
5. Do not remove existing requirements. 
6. Preserve all previously established Page 1 styling requirements.

## SOURCE PAGE 148

7. Implement multiple project entries. 
8. Generate required project-related datasets only at implementation time, when actually 
required. 
9. Ensure generated datasets are meaningful to the project/student context. 
10. After implementation, cross-check the implementation against both spec.md and phase.md. 
11. Update only what is newly introduced by this Projects design. 
12. Do not invent the next onboarding step until its design is provided. 
SDD — CERTIFICATIONS 
1. Feature Overview 
Feature Name: Certifications 
Flow Position: Next step after the previous Projects card/modal. 
Display Mode: Same centered card/modal pattern used throughout the Page 1 onboarding flow. 
When the student clicks Continue on the previous card/modal, the CERTIFICATIONS card/modal 
must appear on the same Page 1. 
PROJECTS 
   ↓ 
Continue 
   ↓ 
CERTIFICATIONS card/modal 
No separate page navigation is introduced by this requirement. 
 
2. Certifications Card / Modal 
The card must contain the heading exactly as: 
CERTIFICATIONS 
The structure must follow the provided design: 
┌──────────────────────────────────────────────────────────────┐ 
│                                                              │ 
│                     CERTIFICATIONS                           │ 
│                                                              │ 
│                                                              │ 
│ Certification Name                                           │ 
│ Issuing Organization                                         │

## SOURCE PAGE 149

│ Certification Type                                           │ 
│ Issue Date                                                   │ 
│ Expiry Date                                                  │ 
│ Credential ID                                                │ 
│ Credential URL                                               │ 
│ Certificate File                                             │ 
│ Skills Covered                                               │ 
│                                                              │ 
│ Back                                                  Continue│ 
│                                                              │ 
│                                                              │ 
└──────────────────────────────────────────────────────────────┘ 
 
3. Certification Information Fields 
The following fields must be included exactly as specified. 
Certification Details 
1. Certification Name 
2. Issuing Organization 
3. Certification Type 
4. Issue Date 
5. Expiry Date 
6. Credential ID 
7. Credential URL 
8. Certificate File 
9. Skills Covered 
No additional certification fields should be added unless specified later. 
 
4. Multiple Certification Entries 
Mandatory Requirement 
Multiple Certification entries are allowed. 
The student must not be restricted to a single certification.

## SOURCE PAGE 150

Conceptually: 
CERTIFICATIONS 
│ 
├── Certification Entry 1 
├── Certification Entry 2 
├── Certification Entry 3 
└── ... 
Each certification entry follows the same structure: 
Certification Entry 
├── Certification Name 
├── Issuing Organization 
├── Certification Type 
├── Issue Date 
├── Expiry Date 
├── Credential ID 
├── Credential URL 
├── Certificate File 
└── Skills Covered 
The exact UI mechanism for adding another certification entry is not specified in the provided 
design. Therefore, do not invent a specific button, label, or interaction as a fixed SDD requirement. 
 
5. Navigation 
Back 
Button: 
Back 
Behaviour: 
Click Back 
     ↓ 
Return to previous 
PROJECTS card/modal 
The Back control must remain consistent with the existing Page 1 onboarding flow.

## SOURCE PAGE 151

Continue 
Button: 
Continue 
Behaviour: 
Click Continue 
     ↓ 
Proceed to the next onboarding step 
The next step has not been specified yet. 
Therefore, no next-step page, card, modal, fields, or functionality should be invented. 
 
6. Contextual Searchable Inputs 
Where selection from a dataset is appropriate, the control should be implemented as a searchable 
dropdown/selector. 
Potential contextual selection fields include: 
• 
Issuing Organization 
• 
Certification Type 
• 
Skills Covered 
The exact datasets are not provided. 
Therefore: 
• 
Do not invent a fixed dataset in this SDD. 
• 
Generate meaningful datasets at implementation time when required. 
• 
Generated values must be relevant to student certifications. 
• 
Searchable behaviour should be used where the available dataset can be large. 
• 
Multiple selection should be supported where appropriate, particularly for Skills Covered, 
without introducing requirements beyond the field's context. 
 
7. Certificate File 
Field: 
Certificate File 
The field must be present. 
The sketch does not specify:

## SOURCE PAGE 152

• 
allowed file formats 
• 
maximum file size 
• 
number of files 
• 
upload mechanism 
• 
file validation rules 
Therefore, these details remain unspecified until explicitly provided. 
Do not hallucinate or add them to the implementation specification. 
 
8. Credential Information 
The following fields must be available: 
Credential ID 
and 
Credential URL 
They belong to each individual certification entry. 
The exact validation behaviour for these fields is not specified and must not be invented beyond 
basic implementation requirements that may be necessary later. 
 
9. Skills Covered 
Field: 
Skills Covered 
This represents the skills associated with the certification. 
The exact skill dataset is not specified. 
When implemented, required skill options may be generated/populated at implementation time, 
provided that they are meaningful and relevant to certifications and the LOOP-MIND project 
context. 
 
10. Styling Requirements 
The Certifications card/modal must use exactly the established Page 1 visual system. 
Background 
Exactly the same Page 1 background. 
No new background is permitted. 
Card / Modal

## SOURCE PAGE 153

Must match all previous Page 1 onboarding cards/modals: 
• 
same visual treatment 
• 
same border language 
• 
same positioning 
• 
same spacing principles 
• 
same proportions 
• 
same overall styling 
Typography 
Use the established Page 1: 
• 
font 
• 
text hierarchy 
• 
sizing 
• 
weight 
• 
alignment 
• 
spacing 
Colours 
Use exactly the established Page 1 colour system. 
No arbitrary or unrelated colours may be introduced. 
Controls 
Inputs, dropdowns, searchable selectors, file controls, buttons, links, and validation states must 
match the established Page 1 styling. 
 
11. Page 1 Flow 
The onboarding continues within the same Page 1 through centered cards/modals: 
PAGE 1 
 │ 
 ├── Login 
 ├── Create Account 
 ├── OTP 
 ├── Basic Information 
 ├── Academic Information

## SOURCE PAGE 154

├── Current Skills 
 ├── Coding Experience 
 ├── Projects 
 │ 
 └── Certifications 
       │ 
       ├── Certification Entry 1 
       ├── Certification Entry 2 
       ├── Certification Entry 3 
       └── ... 
The Certifications component must therefore behave as another step in the existing onboarding flow 
rather than becoming a separate visual page. 
 
12. Data Structure Concept 
Conceptually: 
Student 
└── Certifications[] 
    ├── Certification 1 
    │   ├── Certification Name 
    │   ├── Issuing Organization 
    │   ├── Certification Type 
    │   ├── Issue Date 
    │   ├── Expiry Date 
    │   ├── Credential ID 
    │   ├── Credential URL 
    │   ├── Certificate File 
    │   └── Skills Covered 
    │ 
    ├── Certification 2 
    └── ... 
This represents the requirement for repeatable certification entries.

## SOURCE PAGE 155

It is not a finalized backend/database schema. 
 
13. Scope Boundary 
Explicitly defined 
• 
CERTIFICATIONS heading 
• 
Certification Name 
• 
Issuing Organization 
• 
Certification Type 
• 
Issue Date 
• 
Expiry Date 
• 
Credential ID 
• 
Credential URL 
• 
Certificate File 
• 
Skills Covered 
• 
Back 
• 
Continue 
• 
Multiple certification entries allowed 
• 
Same Page 1 card/modal flow 
• 
Existing Page 1 styling must remain unchanged 
• 
Contextual searchable dropdowns where appropriate 
• 
Required datasets may be generated during implementation when needed 
Not specified 
• 
Maximum number of certifications 
• 
Exact Add Certification UI 
• 
Certification Type options 
• 
Issuing Organization dataset 
• 
Skills dataset 
• 
Certificate file formats 
• 
Certificate file size limits 
• 
Number of files allowed per certification 
• 
Exact validation rules

## SOURCE PAGE 156

• 
Backend schema 
• 
API endpoints 
• 
AI processing 
• 
Certification verification logic 
• 
Next onboarding step 
These remain unspecified until you provide them. 
 
14. Single Source of Truth / Development Rule 
For implementation of this feature: 
1. Cross-check spec.md before development. 
2. Cross-check phase.md before development. 
3. Add only the newly introduced Certifications requirements. 
4. Do not duplicate existing requirements. 
5. Do not remove existing requirements. 
6. Preserve every previously established Page 1 styling rule. 
7. Implement multiple certification entries. 
8. Generate required certification datasets only at implementation time, when actually 
required. 
9. Ensure generated datasets are meaningful to the LOOP-MIND student-profile context. 
10. After implementation, cross-check the implementation against both spec.md and phase.md. 
11. Update only the requirements introduced by this design. 
12. Do not invent the next onboarding step until its design is provided. 
SDD — CAREER / PLACEMENT 
1. Feature Overview 
Feature: Career / Placement Information 
Display: Same-page centered card/modal, replacing the previous card/modal in the profile-creation 
flow. 
Purpose: Collect the student's career interests and placement preferences. 
 
2. UI Structure 
┌──────────────────────────────────────────────────────────────┐ 
│                                                              │

## SOURCE PAGE 157

│                     CAREER / PLACEMENT                       │ 
│                                                              │ 
│                                                              │ 
│ Career Interest                                              │ 
│ Target Job Role                                              │ 
│ Preferred Job Domain                                         │ 
│ Target Company — Optional                                    │ 
│ Target Role                                                  │ 
│ Preferred Technology / Skill Area                            │ 
│ Placement Interest                                           │ 
│ Internship Interest                                          │ 
│                                                              │ 
│                  PLACEMENT PREFERENCES                       │ 
│                                                              │ 
│ Preferred Job Type                                           │ 
│ Preferred Work Location                                      │ 
│ Preferred Country                                            │ 
│ Preferred State                                              │ 
│ Preferred City                                               │ 
│ Remote / On-site / Hybrid                                    │ 
│ Preferred Industry                                           │ 
│ Placement Status                                             │ 
│                                                              │ 
│ Back                                             Continue     │ 
│                                                              │ 
└──────────────────────────────────────────────────────────────┘ 
 
3. Field Specification 
Field 
Type 
Required 
Career Interest 
Searchable dropdown / context-based selection Yes

## SOURCE PAGE 158

Field 
Type 
Required 
Target Job Role 
Searchable dropdown / selection 
Yes 
Preferred Job Domain 
Searchable dropdown / selection 
Yes 
Target Company 
Searchable dropdown / selection 
No 
Target Role 
Searchable dropdown / selection 
Yes 
Preferred Technology / Skill Area Searchable multi-select 
Yes 
Placement Interest 
Selection 
Yes 
Internship Interest 
Selection 
Yes 
Preferred Job Type 
Searchable dropdown / selection 
Yes 
Preferred Work Location 
Searchable dropdown / selection 
Yes 
Preferred Country 
Searchable dropdown 
Yes 
Preferred State 
Searchable dropdown 
Yes 
Preferred City 
Searchable dropdown 
Yes 
Remote / On-site / Hybrid 
Selection 
Yes 
Preferred Industry 
Searchable dropdown / selection 
Yes 
Placement Status 
Searchable dropdown / selection 
Yes 
 
4. Context-Aware Dropdown Behaviour 
All fields that require predefined choices should use searchable dropdowns generated according to 
their context. 
Geographic dependency 
Preferred Country 
       ↓ 
Preferred State 
       ↓ 
Preferred City 
The State options should correspond to the selected Country. 
The City options should correspond to the selected State. 
Career dependency

## SOURCE PAGE 159

Selections should remain contextually related: 
Career Interest 
       ↓ 
Target Job Role 
       ↓ 
Target Role 
       ↓ 
Preferred Technology / Skill Area 
       ↓ 
Preferred Industry 
The implementation should not display irrelevant options when the available choices can be 
determined from earlier selections. 
 
5. Target Company 
Target Company is explicitly optional. 
The user may: 
• 
Leave it empty. 
• 
Search for a company. 
• 
Select a company if desired. 
Leaving this field empty must not prevent Continue from becoming active, provided all other 
required fields are completed. 
 
6. Continue Button 
Initial state 
Continue = Disabled 
Activation 
The Continue button becomes active only after all required Career / Placement fields have been 
completed. 
All required fields completed 
          ↓ 
     Continue Active 
The optional Target Company does not participate in the required-field validation.

## SOURCE PAGE 160

7. Continue Action 
On clicking Continue: 
Current Career / Placement card 
              ↓ 
      Save/retain entered data 
              ↓ 
        Proceed to the 
        next profile step 
The next profile step is not specified in the provided requirements, so no specific next card/modal 
should be assumed or implemented here. 
 
8. Back Button 
The Back button is: 
Always Active 
On clicking: 
Career / Placement 
        ↓ 
Previous card/modal 
Previously entered information should be retained when returning to the previous step. 
 
9. Same-Page Card/Modal Rule 
This step follows the established profile-creation interaction: 
Page 1 
   │ 
   ├── Current card/modal 
   │ 
   └── Continue 
          ↓ 
   Replace with next card/modal 
No separate page navigation is introduced for this step.

## SOURCE PAGE 161

The card/modal remains centered on the same Page 1. 
 
10. Validation 
The system must validate all required fields before allowing progression. 
Required field missing 
        ↓ 
Continue remains disabled 
All required fields completed 
        ↓ 
Continue becomes active 
No validation requirement beyond the supplied field requirements should be added here. 
 
11. Data Handling 
The Career / Placement information should be maintained as part of the student's profile-creation 
state. 
At this stage: 
• 
Entered values must persist while navigating Back/Continue. 
• 
Optional Target Company may remain empty. 
• 
Selected dependent geographic values must remain consistent with their parent selections. 
• 
The completed information should be available to the subsequent profile-creation step. 
 
12. Flow 
Previous Card / Modal 
        │ 
        │ Continue 
        ▼ 
┌──────────────────────────────┐ 
│   CAREER / PLACEMENT         │ 
│                              │ 
│ Career Interest              │ 
│ Target Job Role              │

## SOURCE PAGE 162

│ Preferred Job Domain         │ 
│ Target Company (Optional)    │ 
│ Target Role                  │ 
│ Preferred Technology/Skill   │ 
│ Placement Interest           │ 
│ Internship Interest          │ 
│                              │ 
│ PLACEMENT PREFERENCES        │ 
│                              │ 
│ Preferred Job Type           │ 
│ Preferred Work Location      │ 
│ Preferred Country            │ 
│ Preferred State              │ 
│ Preferred City               │ 
│ Remote/On-site/Hybrid        │ 
│ Preferred Industry           │ 
│ Placement Status             │ 
│                              │ 
│ Back             Continue    │ 
└──────────────────────────────┘ 
        │ 
        ├── Back → Previous Card / Modal 
        │ 
        └── Continue → Next Profile Step 
                         (to be specified later) 
Important implementation rule 
Do not invent the next profile step after Career / Placement. The supplied specification only states 
that Continue is clicked; the actual subsequent card/modal has not yet been specified. 
SDD — LEARNING / PREPARATION 
1. Feature Overview 
Feature: Learning / Preparation 
Display: Same-page centered card/modal, continuing the existing student profile-creation flow.

## SOURCE PAGE 163

On clicking Continue from the previous card/modal, the Learning / Preparation card/modal should 
appear on the same Page 1. 
 
2. UI Structure 
┌──────────────────────────────────────────────────────────────┐ 
│                                                              │ 
│                 LEARNING / PREPARATION                       │ 
│                                                              │ 
│ Current Learning Areas                                       │ 
│ Skills Currently Learning                                    │ 
│ Learning Goals                                               │ 
│ Areas They Want to Improve                                   │ 
│ Current Preparation Status                                   │ 
│                                                              │ 
│ INTERVIEW / ASSESSMENT PREPARATION                           │ 
│                                                              │ 
│ Previous Interview Experience — Optional                    │ 
│ Previous Assessment Experience — Optional                   │ 
│ Technical Interview Experience — Optional                   │ 
│ Coding Assessment Experience — Optional                     │ 
│ Interview Preparation Status                                │ 
│ Assessment Preparation Status                               │ 
│                                                              │ 
│ Back                                              Continue   │ 
│                                                              │ 
└──────────────────────────────────────────────────────────────┘ 
 
3. Field Specification 
Field 
Input Type 
Required 
Current Learning Areas 
Searchable multi-select / context-based selection Yes

## SOURCE PAGE 164

Field 
Input Type 
Required 
Skills Currently Learning 
Searchable multi-select 
Yes 
Learning Goals 
Searchable multi-select / selection 
Yes 
Areas They Want to Improve 
Searchable multi-select 
Yes 
Current Preparation Status 
Searchable selection 
Yes 
Previous Interview Experience 
Selection / input 
No 
Previous Assessment Experience Selection / input 
No 
Technical Interview Experience Selection / input 
No 
Coding Assessment Experience Selection / input 
No 
Interview Preparation Status 
Searchable selection 
Yes 
Assessment Preparation Status Searchable selection 
Yes 
 
4. Searchable Options 
Required fields that use selectable values should have search functionality. 
The available datasets/options should be generated and populated automatically according to the 
context of the field at implementation time. 
Do not require manually hardcoded datasets to be supplied beforehand when the required dataset 
has not been provided. 
Examples of contextual relationships: 
Current Learning Areas 
        ↓ 
Skills Currently Learning 
Learning Goals 
        ↓ 
Areas They Want to Improve 
The system should keep selections relevant to the student's profile context. 
 
5. Optional Experience Fields 
The following fields are explicitly optional: 
• 
Previous Interview Experience

## SOURCE PAGE 165

• 
Previous Assessment Experience 
• 
Technical Interview Experience 
• 
Coding Assessment Experience 
The user may leave any or all of these fields empty. 
Their omission must not prevent Continue from becoming active. 
Optional field empty 
        ↓ 
No validation error 
        ↓ 
Continue can still become active 
 
6. Continue Button 
Initial State 
Continue → Disabled 
The button becomes active only when all required fields in this card/modal have been completed. 
All required fields completed 
            ↓ 
     Continue → Active 
Optional experience fields are excluded from this validation. 
 
7. Continue Action 
On clicking Continue: 
Learning / Preparation Card 
             ↓ 
     Retain entered data 
             ↓ 
       Proceed to next 
      profile-creation step 
The exact next step is not specified in the provided requirement, so no additional card/modal 
should be invented.

## SOURCE PAGE 166

8. Back Button 
Back is always active. 
Learning / Preparation 
          ↓ 
        Back 
          ↓ 
Previous Card / Modal 
Previously entered information should remain retained when the user navigates backward and then 
returns to this step. 
 
9. Same-Page Card/Modal Behaviour 
This follows the established Page 1 interaction pattern: 
Page 1 
 │ 
 ├── Previous Card / Modal 
 │ 
 │      Continue 
 │         ↓ 
 │ 
 └── Learning / Preparation Card / Modal 
The card/modal should appear centered on the same page. 
It should not navigate to a separate page solely for this step. 
 
10. Validation 
Required field missing 
        ↓ 
Continue Disabled 
All required fields completed 
        ↓ 
Continue Enabled 
Optional fields do not affect Continue activation.

## SOURCE PAGE 167

11. Data Persistence 
The entered Learning / Preparation information should remain available throughout the profile-
creation flow. 
The system should: 
• 
Retain entered values when moving Back. 
• 
Restore previously entered values when returning to this step. 
• 
Preserve optional fields when provided. 
• 
Allow optional fields to remain empty. 
• 
Maintain selected searchable values. 
 
12. Complete Flow 
Previous Card / Modal 
        │ 
        │ Continue 
        ▼ 
┌─────────────────────────────────────────────┐ 
│          LEARNING / PREPARATION             │ 
│                                             │ 
│ Current Learning Areas                      │ 
│ Skills Currently Learning                   │ 
│ Learning Goals                              │ 
│ Areas They Want to Improve                  │ 
│ Current Preparation Status                  │ 
│                                             │ 
│ INTERVIEW / ASSESSMENT PREPARATION          │ 
│                                             │ 
│ Previous Interview Experience (Optional)    │ 
│ Previous Assessment Experience (Optional)   │ 
│ Technical Interview Experience (Optional)  │ 
│ Coding Assessment Experience (Optional)    │

## SOURCE PAGE 168

│ Interview Preparation Status                │ 
│ Assessment Preparation Status               │ 
│                                             │ 
│ Back                              Continue  │ 
└─────────────────────────────────────────────┘ 
        │ 
        ├── Back 
        │     ↓ 
        │ Previous Card / Modal 
        │ 
        └── Continue 
              ↓ 
        Next Profile Step 
        (not yet specified) 
Implementation rule: Do not define, invent, or assume the profile step after Learning / Preparation 
until it is specified. 
SDD — PROFESSIONAL LINKS + RESUME 
1. Feature Overview 
Feature: Professional Links + Resume 
Flow Position: Next step after the previous Learning / Preparation card/modal. 
Display: Same centered card/modal on Page 1. 
When the student clicks Continue from the previous card/modal, this card/modal must appear on 
the same Page 1. 
Learning / Preparation 
        │ 
        │ Continue 
        ▼ 
Professional Links + Resume 
 
2. Card Structure 
The heading must be: 
PROFESSIONAL LINKS

## SOURCE PAGE 169

The card must contain the following fields exactly as specified: 
┌──────────────────────────────────────────────────────────────┐ 
│                                                              │ 
│                  PROFESSIONAL LINKS                          │ 
│                                                              │ 
│ GitHub URL                                                   │ 
│ LinkedIn URL                                                 │ 
│ Portfolio Website URL                                        │ 
│ Coding Profile URL                                           │ 
│ Other Professional Profile URL                              │ 
│                                                              │ 
│ RESUME                                                       │ 
│                                                              │ 
│ Upload Resume PDF                                            │ 
│                                                              │ 
│                                                              │ 
│ Back                                                  Continue│ 
│                                                              │ 
└──────────────────────────────────────────────────────────────┘ 
 
3. Professional Links 
The following fields must be present: 
3.1 GitHub URL 
GitHub URL 
Input for the student's GitHub profile URL. 
 
3.2 LinkedIn URL 
LinkedIn URL 
Input for the student's LinkedIn profile URL. 
 
3.3 Portfolio Website URL

## SOURCE PAGE 170

Portfolio Website URL 
Input for the student's portfolio website URL. 
 
3.4 Coding Profile URL 
Coding Profile URL 
Input for a student's coding-profile URL. 
The exact coding platform is not specified here. 
Do not assume a particular platform. 
 
3.5 Other Professional Profile URL 
Other Professional Profile URL 
Input for another professional profile URL. 
The specific platform is intentionally not defined. 
 
4. RESUME 
The section heading must be: 
RESUME 
The card must contain: 
Upload Resume PDF 
This represents the resume-upload control. 
The requirement explicitly specifies PDF. 
 
5. Resume Upload 
The student must be able to upload their resume as a PDF. 
Upload Resume PDF 
       ↓ 
Resume PDF selected 
       ↓ 
Resume associated with student profile 
The exact: 
• 
maximum file size

## SOURCE PAGE 171

• 
filename restrictions 
• 
PDF page limit 
• 
upload progress UI 
• 
replacement behaviour 
• 
parsing behaviour 
are not specified. 
Therefore, do not invent these requirements. 

## UPDATE — Resume PDF validation fix (UPDATE SDD §4)

The resume upload previously had no client-side type check and no
visible error state: a non-PDF file dropped via drag-and-drop bypassed
the file picker's PDF filter entirely and failed silently, leaving the
student thinking their resume was saved when it wasn't. The upload now
validates the file is a PDF before attempting the upload, and shows an
explicit error if the upload fails for any reason (wrong type, network).
No other Professional Links behavior changed.

## UPDATE — Resume upload auto-refreshes Skill Gap Analysis (Student Resume Upload & Skill
Gap Automation SDD §2-3/§10-11/§16)

Every resume upload/re-upload through `POST /students/me/resume` — from any of its existing
locations in the product — now also checks whether the student already has a target company
selected. If they do, the same request immediately re-runs the Skill Gap Agent
(`intelligence_service.analyze_skill_gap`) against the freshly extracted skills, so the Skill
Gap page reflects the new resume without the student needing to touch their target
company/role again to force a recalculation. If no target is selected yet, the resume is still
stored and extracted regardless (Scenario A); the existing "run the first analysis on demand
once a target is chosen" behaviour (`skill_gap_page_service.get_skill_gap_page`) already picks
up whatever was previously extracted at that point. Together these cover both orderings —
resume-then-company and company-then-resume — with the same end state: the Skill Gap page
always reflects the latest stored resume/profile data against the current target, generated by
the one existing agent-driven flow (Resume Upload → Resume Agent → Extraction → Database →
Skill Gap Agent → Skill Gap Analysis → Database → Skill Gap Page), never re-derived in the UI.
Cross-source skill dedup (Resume/Profile/LinkedIn skill of the same name counts once) and the
Supported vs. Missing Evidence status split were already handled by pre-existing extraction and
skill-gap-row logic and needed no change for this update.

## UPDATE — Real resume text extraction (Student Dashboard UPDATE SDD §5/§9)

Every resume upload or replacement through this same `POST /students/me/resume` endpoint
(from this Professional Links step, or from the Student Dashboard's own Upload Your Resume
card) now runs the Resume Parser Agent's real text-extraction capability (`pypdf` reads the
PDF's actual text; the agent maps it to skills/certifications/projects) and stores whatever it
genuinely finds, deduped against what the student already has. Education/experience are
extracted but not written to the Academic Info table, since a resume's text never reliably
supplies that table's required LOOP-MIND-specific fields (current semester, CGPA scale,
admission year) and inventing them would be fabrication.
 
6. Professional Links Input Behaviour 
The five professional-link fields are URL-oriented inputs: 
GitHub URL 
LinkedIn URL 
Portfolio Website URL 
Coding Profile URL 
Other Professional Profile URL 
The exact validation rules are not specified in the provided design. 
Therefore, the SDD does not prescribe additional URL-validation behaviour beyond what is required 
to correctly handle URL inputs. 
 
7. Continue Button 
The card contains: 
Continue 
The Continue button follows the established onboarding rule: 
Required information incomplete 
        ↓ 
Continue disabled 
 
Required information complete 
        ↓ 
Continue enabled 
The provided sketch does not explicitly identify which professional-link fields are mandatory or 
optional.

## SOURCE PAGE 172

Therefore, this SDD must not falsely mark specific link fields as required or optional. 
The exact required-field definition remains unspecified unless provided later. 
 
8. Back Button 
The card contains: 
Back 
Back must remain available according to the established onboarding navigation behaviour. 
Professional Links + Resume 
          │ 
          │ Back 
          ▼ 
Learning / Preparation 
Previously entered information should be retained when navigating backward. 
 
9. Same-Page Requirement 
This card/modal must remain part of the existing Page 1 profile-creation flow. 
PAGE 1 
 │ 
 ├── Basic Information 
 ├── Academic Information 
 ├── Current Skills 
 ├── Coding Experience 
 ├── Projects 
 ├── Certifications 
 ├── Career / Placement 
 ├── Learning / Preparation 
 │ 
 └── Professional Links + Resume 
It must not create a new standalone page. 
 
10. No Searchable Dropdowns Required

## SOURCE PAGE 173

Unlike previous steps, the supplied Professional Links + Resume design contains: 
• 
URL input fields 
• 
Resume PDF upload 
It does not specify any dropdown dataset. 
Therefore, no artificial dropdown dataset should be generated for this card. 
The previously established rule still applies generally: 
If a future field requires a dataset and the dataset has not been provided, generate meaningful 
contextual data at implementation time, not beforehand. 
 
11. Styling — STRICT 
The Professional Links + Resume card/modal must use exactly the same Page 1 styling already 
established. 
Background 
Exactly the same Page 1 background. 
No new background. 
Card 
Use the existing: 
• 
centered modal/card treatment 
• 
dimensions/proportions 
• 
border style 
• 
spacing system 
• 
visual hierarchy 
Typography 
Use the exact established: 
• 
font 
• 
text hierarchy 
• 
sizing 
• 
weight 
• 
alignment 
Colours 
Use the existing Page 1 colour system. 
No new colours.

## SOURCE PAGE 174

Controls 
All: 
• 
URL inputs 
• 
Resume upload control 
• 
Back button 
• 
Continue button 
• 
validation states 
must match the established Page 1 components. 
 
12. Data Structure Concept 
Conceptually: 
Student 
│ 
├── Professional Links 
│   ├── GitHub URL 
│   ├── LinkedIn URL 
│   ├── Portfolio Website URL 
│   ├── Coding Profile URL 
│   └── Other Professional Profile URL 
│ 
└── Resume 
    └── Resume PDF 
This is only a conceptual representation of the information collected. 
It is not a finalized database schema or API contract. 
 
13. Complete Flow 
Learning / Preparation 
        │ 
        │ Continue 
        ▼ 
┌─────────────────────────────────────────────────────────────┐

## SOURCE PAGE 175

│                  PROFESSIONAL LINKS                         │ 
│                                                             │ 
│ GitHub URL                                                  │ 
│ LinkedIn URL                                                │ 
│ Portfolio Website URL                                       │ 
│ Coding Profile URL                                          │ 
│ Other Professional Profile URL                             │ 
│                                                             │ 
│ RESUME                                                      │ 
│                                                             │ 
│ Upload Resume PDF                                           │ 
│                                                             │ 
│ Back                                             Continue   │ 
└─────────────────────────────────────────────────────────────┘ 
        │ 
        ├── Back 
        │     ↓ 
        │ Learning / Preparation 
        │ 
        └── Continue 
              ↓ 
        Next profile step 
        [Not specified yet] 
 
14. Scope Boundary 
Explicitly defined 
• 
PROFESSIONAL LINKS heading 
• 
GitHub URL 
• 
LinkedIn URL 
• 
Portfolio Website URL 
• 
Coding Profile URL

## SOURCE PAGE 176

• 
Other Professional Profile URL 
• 
RESUME heading 
• 
Upload Resume PDF 
• 
Back 
• 
Continue 
• 
Same Page 1 card/modal flow 
• 
Existing Page 1 styling 
• 
Resume specifically identified as PDF 
Not specified 
• 
Which professional links are mandatory. 
• 
Whether resume upload is mandatory. 
• 
Maximum resume file size. 
• 
Resume page limit. 
• 
Resume filename rules. 
• 
Resume replacement rules. 
• 
URL validation rules. 
• 
Specific coding-platform options. 
• 
Specific other-professional-profile options. 
• 
Resume parsing/extraction. 
• 
Resume scoring. 
• 
AI processing. 
• 
Backend/API implementation. 
• 
Next profile step. 
These must remain unspecified until explicitly defined. 
 
15. Single Source of Truth Rule 
Before implementing this card: 
1. Cross-check spec.md. 
2. Cross-check phase.md. 
3. Add only the newly specified Professional Links + Resume requirements. 
4. Do not duplicate existing requirements.

## SOURCE PAGE 177

5. Do not remove or overwrite previous requirements. 
6. Preserve the exact Page 1 background and styling system. 
7. Implement the fields exactly as specified. 
8. Do not invent unspecified validation or workflow. 
9. After implementation, cross-check the implementation against both spec.md and phase.md. 
10. Resolve omissions, duplication, or contradictions before proceeding to the next card. 
11. If a future dataset becomes necessary, generate/populate it only at implementation time 
and make it meaningful to the context. 
12. Do not define the next profile step until its design is provided. 
SDD — RECRUITMENT HISTORY + CONSENT 
1. Feature Overview 
Feature: Recruitment History + Consent 
Flow Position: Next step after the previous Professional Links + Resume card/modal. 
Display: Same centered card/modal on Page 1. 
When the student clicks Continue from the previous card/modal, the RECRUITMENT HISTORY + 
CONSENT card/modal must appear on the same Page 1. 
Professional Links + Resume 
            │ 
            │ Continue 
            ▼ 
RECRUITMENT HISTORY + CONSENT 
No separate page is introduced. 
 
2. Card Structure 
The card must contain the following two sections exactly as provided. 
┌──────────────────────────────────────────────────────────────┐ 
│                                                              │ 
│                  RECRUITMENT HISTORY                         │ 
│                                                              │ 
│ Previous Applications                                        │ 
│ Companies Applied To                                         │ 
│ Roles Applied To                                             │

## SOURCE PAGE 178

│ Recruitment Stage Reached                                    │ 
│ Assessment Participation                                     │ 
│ Interview Participation                                      │ 
│ Selection Outcome                                            │ 
│ Rejection Outcome                                            │ 
│ Hold Outcome                                                 │ 
│                                                              │ 
├──────────────────────────────────────────────────────────────┤ 
│                                                              │ 
│                 CONSENT / KNOWLEDGE SHARING                  │ 
│                                                              │ 
│ Consent to use relevant information                          │ 
│ Consent for learning/recruitment experience                  │ 
│ Consent for anonymized/aggregated intelligence               │ 
│                                                              │ 
│                    Create Account                             │ 
│                                                              │ 
└──────────────────────────────────────────────────────────────┘ 
 
3. RECRUITMENT HISTORY 
The first section heading must be: 
RECRUITMENT HISTORY 
The following fields must be included: 
1. Previous Applications 
2. Companies Applied To 
3. Roles Applied To 
4. Recruitment Stage Reached 
5. Assessment Participation 
6. Interview Participation 
7. Selection Outcome 
8. Rejection Outcome

## SOURCE PAGE 179

9. Hold Outcome 
No additional recruitment-history fields should be invented. 
 
4. Previous Applications 
Field: 
Previous Applications 
This captures whether/what previous application experience the student has. 
The exact input type and option values are not specified in the supplied design, so they must not be 
fabricated in the SDD. 
 
5. Companies Applied To 
Field: 
Companies Applied To 
This captures companies to which the student has previously applied. 
Because multiple companies may logically be represented by this field, the implementation should 
support the context of multiple values where required. 
The exact company dataset and maximum number of entries are not specified. 
 
6. Roles Applied To 
Field: 
Roles Applied To 
This captures roles associated with the student's previous applications. 
The exact role dataset is not specified. 
If selection from a dataset is implemented, it must be searchable and contextually meaningful. 
 
7. Recruitment Stage Reached 
Field: 
Recruitment Stage Reached 
This captures the recruitment stage reached in previous recruitment activity. 
The exact stage options are not specified in the provided design. 
Do not invent a fixed stage list in this SDD.

## SOURCE PAGE 180

8. Assessment Participation 
Field: 
Assessment Participation 
This captures participation in previous recruitment assessments. 
The exact input type/options are not defined in the supplied design. 
 
9. Interview Participation 
Field: 
Interview Participation 
This captures previous interview participation. 
The exact input type/options are not defined in the supplied design. 
 
10. Selection Outcome 
Field: 
Selection Outcome 
This captures selection-related outcomes from previous recruitment experiences. 
The exact values/options are not specified. 
 
11. Rejection Outcome 
Field: 
Rejection Outcome 
This captures rejection-related outcomes. 
The exact values/options are not specified. 
Do not add additional rejection categories unless they are provided later. 
 
12. Hold Outcome 
Field: 
Hold Outcome 
This captures situations where a recruitment outcome was placed on hold. 
The exact values/options are not specified.

## SOURCE PAGE 181

13. CONSENT / KNOWLEDGE SHARING 
The second section must be separated visually from Recruitment History as shown in the supplied 
design. 
Heading: 
CONSENT / KNOWLEDGE SHARING 
The following three consent items must be included: 
1. Consent to use relevant information 
2. Consent for learning/recruitment experience 
3. Consent for anonymized/aggregated intelligence 
The wording must remain exactly as specified. 
 
14. Consent Controls 
Each consent item requires an appropriate consent-selection control. 
The exact control style is not explicitly specified in the sketch. 
Therefore, the implementation should use the established Page 1 selection/control styling without 
inventing a different visual system. 
The exact mandatory/optional status of each consent item is not explicitly stated in the supplied 
design. 
Do not falsely classify them as required or optional in the SDD. 
 
15. Create Account 
The final action shown in the supplied design is: 
Create Account 
This is distinct from the earlier Continue buttons. 
The supplied design does not explicitly specify whether Create Account is immediately enabled or 
what exact validation rules determine its enabled state. 
Therefore, do not invent additional activation rules beyond the requirements that will be established 
when the account-creation completion behaviour is defined. 

## UPDATE — Create Account activation + database creation rule now defined (Student Create Account UPDATE SDD §10-12)

The account-creation completion behaviour deferred above is now defined: Create Account
stays inactive (disabled) until all three required consents on this card are given, and
becomes active only once they are. No permanent student account exists in the database
before this button is clicked — clicking it is the one point that creates the real account,
migrating everything staged during registration (Basic Information through Professional
Links + Resume) into it in one step, then continuing into the Student Portal. Every prior
step (OTP verification, Basic Information, LinkedIn retrieval, Continue on any step) only
ever touches a temporary registration draft, never the real account. 
 
16. Completion Flow 
The intended progression is: 
Professional Links + Resume 
          │

## SOURCE PAGE 182

│ Continue 
          ▼ 
RECRUITMENT HISTORY 
          │ 
          ├── Previous Applications 
          ├── Companies Applied To 
          ├── Roles Applied To 
          ├── Recruitment Stage Reached 
          ├── Assessment Participation 
          ├── Interview Participation 
          ├── Selection Outcome 
          ├── Rejection Outcome 
          └── Hold Outcome 
                    │ 
                    ▼ 
          CONSENT / KNOWLEDGE SHARING 
                    │ 
                    ├── Consent to use relevant information 
                    ├── Consent for learning/recruitment experience 
                    └── Consent for anonymized/aggregated intelligence 
                              │ 
                              ▼ 
                       Create Account 
 
17. Same Page 1 Requirement 
This card/modal remains part of the existing Page 1 onboarding flow. 
PAGE 1 
 │ 
 ├── Basic Information 
 ├── Academic Information 
 ├── Current Skills

## SOURCE PAGE 183

├── Coding Experience 
 ├── Projects 
 ├── Certifications 
 ├── Career / Placement 
 ├── Learning / Preparation 
 ├── Professional Links + Resume 
 │ 
 └── Recruitment History + Consent 
It must appear using the same centered modal/card mechanism. 
 
18. Styling — STRICT 
This card/modal must use exactly the existing Page 1 styling system. 
Background 
Same Page 1 background without modification. 
Card 
Use the same: 
• 
card/modal appearance 
• 
dimensions/proportions 
• 
border treatment 
• 
spacing 
• 
positioning 
• 
visual hierarchy 
Typography 
Use the exact established Page 1: 
• 
font 
• 
sizing 
• 
weight 
• 
hierarchy 
• 
alignment 
Colours 
Use the established Page 1 colours.

## SOURCE PAGE 184

No new colours. 
Controls 
All inputs, selections, consent controls, and the Create Account button must match the existing Page 
1 component styling. 
 
19. Dataset Generation Rule 
If any Recruitment History field requires a dataset and no dataset has been supplied: 
Dataset supplied? 
       │ 
       ├── YES → Use supplied dataset 
       │ 
       └── NO 
            ↓ 
      Generate meaningful 
      contextual dataset 
            ↓ 
      ONLY at implementation time 
Generated datasets must be meaningful to recruitment history. 
Do not create random filler values. 
No dataset should be generated beforehand merely because this screen has been specified. 
 
20. Scope Boundary 
Explicitly defined 
• 
RECRUITMENT HISTORY 
• 
Previous Applications 
• 
Companies Applied To 
• 
Roles Applied To 
• 
Recruitment Stage Reached 
• 
Assessment Participation 
• 
Interview Participation 
• 
Selection Outcome

## SOURCE PAGE 185

• 
Rejection Outcome 
• 
Hold Outcome 
• 
CONSENT / KNOWLEDGE SHARING 
• 
Consent to use relevant information 
• 
Consent for learning/recruitment experience 
• 
Consent for anonymized/aggregated intelligence 
• 
Create Account 
• 
Same Page 1 card/modal flow 
• 
Existing Page 1 styling 
• 
Contextual dataset generation when needed 
Not specified 
• 
Exact input type for each Recruitment History field. 
• 
Exact recruitment-stage options. 
• 
Exact outcome options. 
• 
Exact company dataset. 
• 
Exact role dataset. 
• 
Whether recruitment history supports multiple historical applications as separate records. 
• 
Exact consent control type. 
• 
Whether each consent is mandatory. 
• 
Create Account button activation rules. 
• 
Account creation API/backend behaviour. 
• 
Final account-creation success screen. 
• 
Any subsequent page after account creation. 
• 
AI processing or intelligence-generation behaviour. 
These remain unspecified until explicitly defined. 
 
21. Single Source of Truth / Development Rule 
Before implementing this step: 
1. Cross-check spec.md. 
2. Cross-check phase.md. 
3. Add only the newly specified Recruitment History + Consent requirements.

## SOURCE PAGE 186

4. Do not duplicate existing requirements. 
5. Do not remove existing requirements. 
6. Preserve the exact Page 1 background and styling. 
7. Do not invent unspecified field types, datasets, consent rules, or account-completion 
behaviour. 
8. Generate any missing contextual datasets only at implementation time. 
9. Ensure generated datasets are meaningful to the recruitment context. 
10. After implementation, cross-check the implementation against both spec.md and phase.md. 
11. Resolve omissions, duplication, and contradictions before proceeding. 
12. Do not invent additional onboarding screens or functionality that have not yet been 
specified. 
LOOP-MIND — STUDENT PORTAL DASHBOARD 
Software Design / UI Specification (SDD) 
1. PAGE IDENTIFICATION 
Page Name: Student Portal Dashboard 
User Type: Student 
Page Purpose: Main student dashboard displayed immediately after successful authentication or 
successful student account creation. 
Entry Conditions: 
• 
Successful login with valid OTP → open Student Dashboard. 
• 
Successful Create Account flow → open Student Dashboard. 
• 
A valid OTP entered from the Create Account flow must continue only into the Create 
Account flow, never into the Login flow. 
• 
Dashboard content must be generated from the authenticated student's actual 
database/profile data. 
 
2. REFERENCE LAYOUT REQUIREMENT 
The uploaded dashboard image is the strict visual reference for this page. 
The implementation must follow the reference exactly, including: 
• 
Overall page structure 
• 
Navbar placement 
• 
Logo placement 
• 
Navigation item placement

## SOURCE PAGE 187

• 
Greeting section 
• 
Quote card 
• 
Four top statistic cards 
• 
Three middle cards 
• 
Preparation Journey section 
• 
Upcoming Tasks section 
• 
Recommended For You section 
• 
Your Stats section 
• 
Footer 
• 
Relative widths 
• 
Card arrangement 
• 
Spacing hierarchy 
• 
Section order 
• 
Alignment 
• 
Visual hierarchy 
• 
Button placement 
• 
Text positioning 
• 
Icons/illustration placement 
• 
Progress indicators 
• 
Card proportions 
Do not redesign, rearrange, add, remove, or substitute dashboard sections. 
The reference layout should be treated as the source-of-truth layout. 
 
3. PAGE STRUCTURE 
STUDENT DASHBOARD 
│ 
├── TOP NAVBAR 
│   ├── LOOP-MIND Logo 
│   └── Navigation 
│       ├── Dashboard 
│       ├── Skill Gap

## SOURCE PAGE 188

│       ├── Preparation Plan 
│       ├── Jobs 
│       └── My Progress 
│ 
├── HEADER / WELCOME AREA 
│   ├── Student Greeting 
│   ├── Supporting Message 
│   └── Motivational Quote Card 
│ 
├── TOP SUMMARY CARDS 
│   ├── Profile Completion 
│   ├── Skills Added 
│   ├── Projects 
│   └── Certifications 
│ 
├── MAIN INSIGHT ROW 
│   ├── Placement Readiness 
│   ├── Target Company 
│   └── Recent Activity 
│ 
├── PROGRESS / TASK ROW 
│   ├── Your Preparation Journey 
│   └── Upcoming Tasks 
│ 
├── RECOMMENDATION / STATISTICS ROW 
│   ├── Recommended for You 
│   │   ├── Recommendation 1 
│   │   ├── Recommendation 2 
│   │   ├── Recommendation 3 
│   │   └── Recommendation 4 
│   │

## SOURCE PAGE 189

│   └── Your Stats 
│ 
└── FOOTER 
    ├── Terms of Use 
    ├── Privacy Policy 
    ├── Membership Plans 
    ├── Help 
    └── LOOP-MIND © 
 
4. TOP NAVBAR 
The navbar must follow the uploaded reference. 
Left Side 
Display: 
LOOP-MIND 
with the same logo/brand positioning as the reference. 
Right Navigation 
Display the following navigation items in the same order: 
1. Dashboard 
2. Skill Gap 
3. Preparation Plan 
4. Jobs 
5. My Progress 
Active State 
Dashboard must be the active navigation item when this page is open. 
The active state must visually match the reference, including its underline/active indicator. 
 
5. HEADER / WELCOME SECTION 
Immediately below the navbar, display the authenticated student's information. 
Student Greeting 
Reference: 
Hello, Akshaya B!

## SOURCE PAGE 190

However, "Akshaya B" must never be hardcoded. 
It must dynamically use the student's actual stored name. 
Dynamic Data Source 
The name must come from the authenticated student's Student Profile → Basic Information → Full 
Name. 
Example: 
Hello, {student.full_name}!   
Supporting Message 
Display: 
Keep learning, keep building. You’re one step closer to your dream career. 
This supporting message remains part of the dashboard structure. 
Important 
Student-specific information must always come from the student's database/profile. 
Do not use: 
• 
Dummy names 
• 
Hardcoded student values 
• 
Example percentages 
• 
Example counts 
• 
Random target companies 
• 
Random activities 
• 
Random recommendations 
 
6. MOTIVATIONAL QUOTE CARD 
On the right side of the welcome section, maintain the same quote-card placement shown in the 
reference. 
Reference content: 
“A year from now, you’ll wish you had started today.” 
— LOOP-MIND 
The quote card must remain in the same position and visual role. 
 
7. TOP SUMMARY CARDS 
The first major dashboard row contains exactly four cards.

## SOURCE PAGE 191

┌─────────────────┐ ┌─────────────────┐ ┌─────────────────┐ ┌─────────────────┐ 
│ Profile         │ │ Skills Added    │ │ Projects        │ │ Certifications  │ 
│ Completion      │ │                 │ │                 │ │                 │ 
│                 │ │       12        │ │        3        │ │        4        │ 
│ 70% ━━━━━━━     │ │                 │ │                 │ │                 │ 
└─────────────────┘ └─────────────────┘ └─────────────────┘ └─────────────────┘ 
The actual values must be generated from the student's database. 
 
7.1 PROFILE COMPLETION 
Display: 
Profile Completion 
Then display: 
{calculated_percentage}% 
with the progress bar shown in the reference. 
Calculation 
The percentage must be calculated from the student's completed profile fields/categories. 
Profile completion should consider the implemented Student Profile sections: 
• 
Basic Information 
• 
Academic Information 
• 
Current Skills 
• 
Coding Experience 
• 
Projects 
• 
Certifications 
• 
Career / Placement 
• 
Learning / Preparation 
• 
Professional Links / Resume 
• 
Recruitment History / Consent 
Optional fields must not unfairly reduce completion. 
For example: 
• 
Profile Photo is optional. 
• 
Optional academic scores must not be treated as mandatory.

## SOURCE PAGE 192

• 
Optional professional/recruitment information must follow its defined optional/required 
status. 
Critical Rule 
Never display a hardcoded: 
70% 
The 70% in the reference is only a visual/example value. 
 
7.2 CURRENT SKILLS

## UPDATE — renamed from "Skills Added" (Student Dashboard UPDATE SDD §4-5)

Display: 
Current Skills 
Then: 
{actual_skill_count} 
The count must be calculated from the authenticated student's stored Current Skills entries — 
now aggregated from skills added manually, from LinkedIn extraction, and from resume 
extraction alike, since all three write into the same stored skills. 
If the student has: 
Python 
Java 
SQL 
React 
the dashboard should calculate: 
Current Skills = 4 
Do not manually assign a number. 
 
7.3 PROJECTS 
Display: 
Projects 
Then: 
{actual_project_count} 
Count the student's saved project entries. 
Because the profile supports multiple project entries, every valid stored project entry should 
contribute to this count. 
 
7.4 CERTIFICATIONS

## SOURCE PAGE 193

Display: 
Certifications 
Then: 
{actual_certification_count} 
Count all valid certification entries belonging to the authenticated student. 
Because multiple certification entries are allowed, the number must be dynamically calculated. 
 
8. MAIN INSIGHT ROW 
The next row must contain exactly three sections: 
┌────────────────────────┐ ┌────────────────────┐ ┌────────────────────────┐ 
│ Placement Readiness    │ │ Target Company     │ │ Recent Activity         │ 
└────────────────────────┘ └────────────────────┘ └────────────────────────┘ 
Maintain the same arrangement and relative sizing as the uploaded reference. 
 
9. PLACEMENT READINESS CARD 
Heading 
Placement Readiness 
The card contains: 
• 
Circular readiness indicator 
• 
Readiness percentage 
• 
Status message 
• 
Supporting explanation 
• 
CTA button 
Example Reference 
68% 
 
You are on track! 
 
Keep improving your skills and 
adding more evidence to boost 
your placement readiness.

## SOURCE PAGE 194

[ View Detailed Analysis → ] 
Important 
The reference value: 
68% 
must not be hardcoded. 
It must be calculated from the authenticated student's actual profile, skills, academic information, 
coding experience, projects, certifications, career preferences, learning/preparation information, 
and other relevant student data available to the implemented readiness system. 
Status 
The message such as: 
You are on track! 
must also be generated according to the student's actual readiness score. 
Do not show the same status to every student if the underlying readiness system determines 
different states. 
 
10. TARGET COMPANY CARD 
Maintain the exact position and structure shown in the reference. 
Heading 
Target Company 
If Student Has No Target Company 
Display: 
Not set yet 
Then the supporting message: 
Set a target company to get personalized recommendations, skill analysis and preparation plan. 
Then: 
Set Target Company → 
If Student Has a Target Company 
The dashboard must display the student's actual: 
Target Company 
from: 
Student Profile → Career / Placement → Target Company

## SOURCE PAGE 195

The system must never randomly assign a company. 
 
11. RECENT ACTIVITY 
Heading 
Recent Activity 
The card contains a chronological list of the student's actual recent activities. 
Reference examples shown in the uploaded design: 
• 
Added a new skill 
• 
Updated project 
• 
Completed a learning module 
• 
Applied to a job 
These are activity types, not fixed dashboard data. 
Activities must be generated from actual events. 
Examples: 
Student added a skill 
→ Added a new skill 
Student updated a project 
→ Updated project 
Student completed a learning module 
→ Completed a learning module 
Student applied to a job 
→ Applied to a job 
Display the corresponding actual relative timestamp, such as: 
2 days ago 
3 days ago 
5 days ago 
1 week ago 
based on the actual activity timestamp. 
View All 
The View all control must remain at the same position as the reference.

## SOURCE PAGE 196

12. YOUR PREPARATION JOURNEY 
The next section must preserve the reference structure. 
Heading 
Your Preparation Journey 
Supporting Text 
Track your progress across key milestones. 
Journey Stages 
Exactly maintain the four-stage structure: 
Profile → Learn → Apply → Grow 
Stage 1 — Profile 
Label: 
Profile 
Supporting text: 
Build your profile 
Progress state must be based on the student's actual profile completion. 
 
Stage 2 — Learn 
Label: 
Learn 
Supporting text: 
Improve skills 
State must be derived from the student's actual learning/preparation progress. 
 
Stage 3 — Apply 
Label: 
Apply 
Supporting text: 
Apply to jobs 
State must reflect actual job/application activity. 
 
Stage 4 — Grow

## SOURCE PAGE 197

Label: 
Grow 
Supporting text: 
Track progress 
State must reflect actual progress information. 
Important 
The journey must not always show: 
Profile ✓ 
Learn ○ 
Apply ○ 
Grow ○ 
for every student. 
The state of each stage must be calculated from the student's actual data. 
 
13. UPCOMING TASKS 
The right side of this row contains: 
Upcoming Tasks 
with: 
View all 
at the same position as the reference. 
Tasks must be generated based on the student's actual profile and progress. 
Reference task examples: 
□ Complete your profile (Academic Details) 
□ Add at least 2 skills 
□ Explore companies 
□ Complete DSA module 
These are examples of task types. 
Dynamic Task Generation 
Possible tasks can be derived from actual incomplete student requirements, such as: 
• 
Missing Academic Details 
• 
Missing skills

## SOURCE PAGE 198

• 
Missing project evidence 
• 
Missing certification information 
• 
Incomplete career preferences 
• 
Incomplete learning information 
• 
Resume not uploaded 
• 
Preparation activities pending 
• 
Recommended learning module 
• 
Application-related action 
Critical Rule 
Do not display tasks that are irrelevant to the student's actual state. 
 
14. RECOMMENDED FOR YOU 
The bottom-left section must maintain the same placement and structure as the reference. 
Heading 
Recommended for You 
Supporting Text 
Based on your current progress and goals. 
The recommendation cards must be generated according to the student's actual: 
• 
Skills 
• 
Skill gaps 
• 
Career interests 
• 
Target role 
• 
Preferred job domain 
• 
Preferred technology/skill area 
• 
Learning goals 
• 
Preparation status 
• 
Academic information 
• 
Projects 
• 
Certifications 
• 
Placement interest 
• 
Internship interest

## SOURCE PAGE 199

14.1 FOUR RECOMMENDATION CARDS 
The reference contains four cards. 
Maintain exactly four cards in this section. 
Example structure: 
Card 1 
DSA for Placements 
Type: 
Course 
 
Card 2 
Build a Web Project 
Type: 
Project Guide 
 
Card 3 
Interview Preparation 
Type: 
Resource 
 
Card 4 
Explore Top Companies 
Type: 
Insights 
These reference examples must not be blindly hardcoded for every student. 
The actual recommendations must be selected according to the student's profile and current needs 
while preserving the exact four-card layout. 
 
15. YOUR STATS 
The bottom-right section must remain in the same position and size as the reference. 
Heading

## SOURCE PAGE 200

Your Stats 
Time Filter 
Display the same dropdown/control shown in the reference: 
Last 30 days 
The statistics must represent the authenticated student's actual activity for the selected period. 
 
16. YOUR STATS CHART 
The reference chart contains four categories: 
Skills 
Projects 
Learning 
Applications 
The implementation must preserve this four-category structure. 
Values must be dynamically calculated from the student's actual activity. 
Skills 
Number of skills added during the selected period. 
Projects 
Number of project activities/updates according to the defined statistics logic. 
Learning 
Number of learning activities/modules completed during the selected period. 
Applications 
Number of jobs applied to during the selected period. 
Critical Rule 
The reference values are illustrative only. 
Do not hardcode the displayed bar heights. 
 
17. STUDENT DATA SOURCE ARCHITECTURE 
The dashboard must be student-specific. 
Every dynamic dashboard element must identify the authenticated student's unique profile/account 
and retrieve only that student's data. 
Conceptually:

## SOURCE PAGE 201

Authenticated Student 
        ↓ 
Student ID 
        ↓ 
Student Profile / Database 
        ↓ 
Dashboard Data Aggregation 
        ↓ 
Dashboard UI 
 
18. PROFILE DATA MAPPING 
The dashboard should use the profile categories already defined in the Student Profile flow. 
Basic Information 
Used for: 
• 
Full Name 
• 
Date of Birth 
• 
Gender 
• 
Email 
• 
Location 
• 
Profile completion 
Academic Information 
Used for: 
• 
College 
• 
Degree 
• 
Branch 
• 
Academic Year 
• 
Current Year 
• 
Current Semester 
• 
Admission Year 
• 
Expected Graduation Year 
• 
CGPA

## SOURCE PAGE 202

• 
Academic progress 
• 
Profile completion 
Current Skills 
Used for: 
• 
Skills Added 
• 
Skill-related recommendations 
• 
Skill Gap 
• 
Placement Readiness 
• 
Preparation Journey 
• 
Recommended content 
Coding Experience 
Used for: 
• 
Programming languages 
• 
DSA experience 
• 
Competitive programming experience 
• 
Coding platforms 
• 
Coding-related recommendations 
• 
Placement readiness 
Projects 
Used for: 
• 
Project count 
• 
Project activity 
• 
Evidence 
• 
Skills demonstrated 
• 
Recommendations 
• 
Placement readiness 
Multiple project entries must be supported. 
Certifications 
Used for: 
• 
Certification count 
• 
Skills covered

## SOURCE PAGE 203

• 
Profile completion 
• 
Recommendations 
• 
Placement readiness 
Multiple certification entries must be supported. 
Career / Placement 
Used for: 
• 
Career interest 
• 
Target job role 
• 
Preferred job domain 
• 
Target company 
• 
Target role 
• 
Preferred technology/skill area 
• 
Placement interest 
• 
Internship interest 
• 
Job recommendations 
Placement Preferences 
Used for: 
• 
Preferred job type 
• 
Preferred work location 
• 
Preferred country 
• 
Preferred state 
• 
Preferred city 
• 
Remote / On-site / Hybrid 
• 
Preferred industry 
• 
Placement status 
Learning / Preparation 
Used for: 
• 
Current learning areas 
• 
Skills currently learning 
• 
Learning goals 
• 
Improvement areas

## SOURCE PAGE 204

• 
Preparation status 
• 
Interview preparation 
• 
Assessment preparation 
Professional Links / Resume 
Used for: 
• 
GitHub 
• 
LinkedIn 
• 
Portfolio 
• 
Coding profile 
• 
Resume availability 
• 
Profile completion 
Recruitment History 
Used for: 
• 
Applications 
• 
Recruitment stages 
• 
Assessments 
• 
Interviews 
• 
Selection outcomes 
• 
Rejection outcomes 
• 
Hold outcomes 
• 
Recruitment intelligence 
• 
Dashboard activity 
Consent 
Consent information must control whether relevant information may be used for the applicable 
learning/recruitment intelligence features. 
 
19. PROFILE PHOTO RULE 
The Student Profile allows: 
Profile Photo — Optional 
Only one photo can be uploaded. 
When the student clicks the profile-photo control, the selection options must be:

## SOURCE PAGE 205

Camera 
Photos 
Files 
The dashboard must use the student's actual profile photo if one exists. 
Do not require the photo for account/profile completion. 
 
20. SEARCHABLE DROPDOWN DATA 
All required contextual dropdowns throughout the student profile must be generated/populated 
with meaningful datasets at implementation time when the dataset is not explicitly supplied. 
Examples include: 
• 
Country 
• 
State 
• 
City 
• 
College 
• 
Degree 
• 
Branch 
• 
Academic Year 
• 
Current Year 
• 
Current Semester 
• 
Admission Year 
• 
Graduation Year 
• 
Skill Category 
• 
Proficiency 
• 
Learning Status 
• 
Programming Languages 
• 
Coding Platforms 
• 
Project Type 
• 
Project Status 
• 
Certification Type 
• 
Career-related selections 
• 
Job Type

## SOURCE PAGE 206

• 
Industry 
• 
Work Location 
• 
Placement Status 
Context Awareness 
Dependent dropdowns must respect the selected context. 
For example: 
Country 
   ↓ 
State 
   ↓ 
City 
The City list must correspond to the selected State, and the State list must correspond to the 
selected Country. 
All required searchable dropdowns must be usable and populated with meaningful data rather than 
empty placeholder lists. 
 
21. DASHBOARD DATA INTEGRITY 
The dashboard must follow this strict rule: 
Every student-specific value shown on the dashboard must be derived from the authenticated 
student's actual stored data or from a clearly defined calculation based on that data. 
Therefore, do not: 
• 
Hardcode 70% 
• 
Hardcode 68% 
• 
Hardcode 12 Skills 
• 
Hardcode 3 Projects 
• 
Hardcode 4 Certifications 
• 
Hardcode Not set yet when a target company exists 
• 
Hardcode activity history 
• 
Hardcode task completion 
• 
Hardcode statistics 
• 
Hardcode recommendations 
The values shown in the uploaded reference are visual reference values only.

## SOURCE PAGE 207

22. EMPTY / MISSING DATA BEHAVIOUR 
If a student has not supplied a particular piece of information, the dashboard must handle it 
gracefully. 
Examples: 
No Target Company 
Not set yet 
No Projects 
0 
No Certifications 
0 
No Skills 
0 
No Recent Activity 
Display an appropriate empty-state within the existing Recent Activity card without removing or 
restructuring the card. 
No Resume 
The relevant profile/task system can identify the resume as incomplete. 
Do not invent information to fill missing student data. 
 
23. AUTHENTICATION → DASHBOARD FLOW 
Login Flow 
Login 
   ↓ 
Enter Mobile Number 
   ↓ 
Get OTP 
   ↓ 
Enter OTP 
   ↓ 
Valid OTP 
   ↓

## SOURCE PAGE 208

Successful Authentication 
   ↓ 
Student Dashboard 
Create Account Flow 
Login Card / Modal 
        ↓ 
Create Account 
        ↓ 
Create Student Profile 
        ↓ 
Get OTP 
        ↓ 
Enter OTP 
        ↓ 
Valid 4-digit OTP 
        ↓ 
Automatically continue 
        ↓ 
Next Create Account Flow 
        ↓ 
Basic Information 
        ↓ 
Academic Information 
        ↓ 
Current Skills 
        ↓ 
Coding Experience 
        ↓ 
Projects 
        ↓ 
Certifications

## SOURCE PAGE 209

↓ 
Career / Placement 
        ↓ 
Learning / Preparation 
        ↓ 
Professional Links + Resume 
        ↓ 
Recruitment History + Consent 
        ↓ 
Create Account 
        ↓ 
Student Dashboard 
OTP Error 
If the entered OTP is incorrect: 
Display directly under the OTP input area: 
Incorrect OTP, please try again 
This message must appear only when the entered OTP is wrong. 
Valid OTP 
For Create Account: 
Valid 4-digit OTP 
        ↓ 
Automatically proceed 
        ↓ 
Next Create Account step 
It must never redirect to Login. 
 
24. DASHBOARD VISUAL STRUCTURE 
The final implementation must preserve this hierarchy: 
                    LOOP-MIND 
──────────────────────────────────────────────────────────── 
Dashboard | Skill Gap | Preparation Plan | Jobs | My Progress

## SOURCE PAGE 210

──────────────────────────────────────────────────────────── 
 
Hello, {Student Name}!   
Keep learning, keep building... 
 
                                      [ Motivational Quote ] 
 
──────────────────────────────────────────────────────────── 
[ Profile Completion ] [ Skills ] [ Projects ] [ Certifications ] 
──────────────────────────────────────────────────────────── 
 
[ Placement Readiness ] [ Target Company ] [ Recent Activity ] 
──────────────────────────────────────────────────────────── 
 
[          Your Preparation Journey          ] 
                                      [ Upcoming Tasks ] 
 
──────────────────────────────────────────────────────────── 
 
[             Recommended for You            ] [ Your Stats ] 
[ Card ] [ Card ] [ Card ] [ Card ]             [ Chart ] 
 
──────────────────────────────────────────────────────────── 
Terms of Use | Privacy Policy | Membership Plans | Help 
 
                         LOOP-MIND © 
──────────────────────────────────────────────────────────── 
 
25. FOOTER 
The footer must remain at the bottom in the same structure as the reference. 
Display:

## SOURCE PAGE 211

• 
Terms of Use 
• 
Privacy Policy 
• 
Membership Plans 
• 
Help 
• 
LOOP-MIND © 
No additional footer sections should be introduced. 
 
26. STRICT IMPLEMENTATION RULE 
The uploaded dashboard screenshot is the visual source of truth. 
The developer must not reinterpret the dashboard into a different design. 
Do not: 
• 
Move cards 
• 
Change section order 
• 
Add dashboard sections 
• 
Remove dashboard sections 
• 
Change the number of top cards 
• 
Change the number of recommendation cards 
• 
Replace the stats chart with another component 
• 
Move the footer 
• 
Move the navbar 
• 
Change the navigation structure 
• 
Introduce a sidebar 
• 
Turn the dashboard into a different layout 
• 
Replace cards with tables 
• 
Replace the journey with another component 
The data is dynamic; the layout is fixed. 
Core principle 
Same structure + same placement + same hierarchy + same dashboard sections, while every 
student-specific value is dynamically generated from that student's actual database/profile data. 
This is the required Student Portal Dashboard Page 1 after successful Login/Create Account 
completion. 
Yes. I understand the requirement clearly.

## SOURCE PAGE 212

From now on, for your LOOP-MIND project: 
• 
Project name: LOOP-MIND — never Advaita Matrimony. 
• 
Whatever you explain in Kannada, English, or mixed language, I will convert it into clear, 
proper English specifications. 
• 
I will preserve exactly what you specify. 
• 
I will not hallucinate missing requirements. 
• 
I will not add unrelated functionality. 
• 
I will not change your intended behavior. 
• 
If something is not specified, I will not assume it. 
• 
I will maintain your existing terminology and structure. 
• 
When you say update the specification, I will update only the relevant requirement. 
• 
Your UI/reference requirements will be treated as strict requirements, especially when you 
say “exactly the same.” 
• 
Authentication rules will be written specifically for LOOP-MIND. 
Confirmed authentication requirement for LOOP-MIND 
The previous Advaita Matrimony references are replaced with LOOP-MIND. 
                    LOOP-MIND 
                        │ 
             ┌──────────┴──────────┐ 
             │                     │ 
       CREATE ACCOUNT            LOGIN 
             │                     │ 
       Enter mobile          Enter mobile 
             │                     │ 
       Check database        Check database 
             │                     │ 
       ┌─────┴─────┐        ┌──────┴─────┐ 
       │           │        │            │ 
    EXISTS       NEW      EXISTS        NEW 
       │           │        │            │ 
       ▼           ▼        ▼            ▼ 
 Account        Send OTP  Send OTP   Account

## SOURCE PAGE 213

Already        → Verify  → Verify   Doesn't 
 Exists           OTP       OTP       Exist 
       │           │        │            │ 
       ▼           ▼        ▼            ▼ 
 Go to Login   Continue   Continue   Create Account 
Confirmed navigation 
Create Account → existing mobile number 
Account Already Exists 
An account has already been created with this mobile number. 
 
[ Go to Login → ] 
Link: 
/login 
Login → non-existing mobile number 
Account Not Found 
No account exists with this mobile number. 
 
[ Create New Account → ] 
Link: 
/register 
Confirmed database rule 
mobile_number TEXT UNIQUE NOT NULL 
The mobile number must be unique. 
Confirmed OTP rule 
For the Create Account flow: 
Valid 4-digit OTP 
        ↓ 
Automatically proceed 
        ↓ 
Next Create Account step 
It must never switch to the Login flow.

## SOURCE PAGE 214

For an incorrect OTP: 
Incorrect OTP, please try again 
must appear only under the OTP input area when the OTP is incorrect. 
I’ll follow this exact approach for all the next LOOP-MIND specifications you give me. 
LOOP-MIND — STUDENT SKILL GAP ANALYSIS PAGE 
Reference Layout + Functional Specification 
Important: This page is for LOOP-MIND, not Advaita Matrimony. 
The uploaded image is the exact visual/layout reference for this page. The implementation must 
reproduce the same structure, placement, hierarchy, spacing, card arrangement, navigation, table 
structure, and footer. 
Do not redesign, rearrange, simplify, or introduce a different layout. 
 
1. PAGE PURPOSE 
The Skill Gap Analysis page belongs to the LOOP-MIND Student Portal. 
It should show the student's skill gap based on: 
• 
Student profile data 
• 
Student's current skills 
• 
Student's skill levels 
• 
Target company 
• 
Target job role 
• 
Required skills for that target 
• 
Required proficiency levels 
• 
Skill evidence 
• 
Placement-readiness data 
All displayed student-specific values must be retrieved dynamically from the relevant 
database/profile data. 
Strict Rule 
Nothing student-specific should be hardcoded. 
For example: 
• 
Student name → database 
• 
Target company → database/student selection 
• 
Target role → database/student selection 
• 
Overall readiness → calculated/generated from actual student data

## SOURCE PAGE 215

• 
Total required skills → actual skill requirements 
• 
Skills the student has → actual profile skills 
• 
Skills to improve → actual analysis 
• 
Missing skills → actual analysis 
• 
Missing evidence → actual profile/evidence data 
• 
Skill levels → actual student data 
• 
Required levels → actual target-role/company requirements 
• 
Priority → actual skill-gap analysis 
• 
Skill distribution → actual calculated data 
• 
Top priority areas → actual analysis 
The reference image's values such as 68%, 18, 11, 7, 4, etc. are visual examples only, not fixed 
values. 
 
2. PAGE ACCESS / NAVIGATION 
The Skill Gap page must be accessible from the Student Dashboard. 
Entry Point 1 — Student Dashboard → Skill Gap 
On the Student Dashboard, there is a Skill Gap navigation/menu item. 
When the student clicks: 
Skill Gap 
→ Open the Skill Gap Analysis page. 
 
Entry Point 2 — Student Dashboard → Placement Readiness 
The Student Dashboard contains: 
Placement Readiness 
with: 
View Detailed Analysis → 
When the student clicks: 
View Detailed Analysis 
→ Open the same Skill Gap Analysis page. 

## UPDATE — Entry Point 2 superseded (Student Dashboard UPDATE SDD §10-12)

"View Detailed Analysis" no longer navigates to the Skill Gap Analysis page. It now opens a
centered modal/card overlay on the same Dashboard page, showing Current Skills and the
skills backed by strong evidence, live-computed from the Placement Readiness Agent every
time it opens. Entry Point 1 (the dedicated Skill Gap nav item) is unaffected and still opens
the full Skill Gap Analysis page as before.
 
3. ROUTING BEHAVIOR

## SOURCE PAGE 216

Both entry points must lead to the same Skill Gap Analysis page. 
Student Dashboard 
       │ 
       ├── Skill Gap 
       │      ↓ 
       │  Skill Gap Analysis 
       │ 
       └── Placement Readiness 
              ↓ 
      View Detailed Analysis 
              ↓ 
       Skill Gap Analysis 
The page must load the currently authenticated student's information. 
 
4. REFERENCE LAYOUT — MUST MATCH EXACTLY 
Use the uploaded reference image as the primary visual specification. 
The overall structure is: 
┌───────────────────────────────────────────────────────────────┐ 
│                         TOP NAVBAR                            │ 
├───────────────────────────────────────────────────────────────┤ 
│                                                               │ 
│ Skill Gap Analysis                         Quote Card         │ 
│ Description                                                     │ 
│                                                               │ 
│ ┌──────────────────────────┐ ┌───────────────┐ ┌────────────┐ │ 
│ │ Target Company / Role    │ │ Overall       │ │ Quick      │ │ 
│ │                          │ │ Readiness     │ │ Actions    │ │ 
│ └──────────────────────────┘ └───────────────┘ └────────────┘ │ 
│                                                               │ 
│ ┌──────────────────────────┐ ┌────────────────┐ ┌───────────┐ │ 
│ │ Skill Gap Overview       │ │ Skill          │ │ Top       │ │

## SOURCE PAGE 217

│ │                          │ │ Distribution   │ │ Priority  │ │ 
│ └──────────────────────────┘ └────────────────┘ └───────────┘ │ 
│                                                               │ 
│ [All Skills] [To Improve] [Missing] [Strong] [Not Relevant] │ 
│                                             [Search skills]  │ 
│                                                               │ 
│ ┌───────────────────────────────────────────────────────────┐ │ 
│ │ Skill table                                               │ │ 
│ └───────────────────────────────────────────────────────────┘ │ 
│                                                               │ 
├───────────────────────────────────────────────────────────────┤ 
│                           FOOTER                              │ 
└───────────────────────────────────────────────────────────────┘ 
The above arrangement must remain the same as the reference image. 
 
5. TOP NAVIGATION BAR 
The navbar must follow the reference image. 
Left side 
• 
LOOP-MIND logo/icon 
• 
LOOP-MIND 
Right side 
Navigation items: 
1. Dashboard 
2. Skill Gap 
3. Preparation Plan 
4. Jobs 
5. My Progress 
Active navigation 
On this page: 
Skill Gap 
must be visually highlighted as the active page.

## SOURCE PAGE 218

The reference uses the active underline/highlight beneath Skill Gap. 
 
6. PAGE HEADER 
Below the navbar: 
Main heading 
Skill Gap Analysis 
Description 
Identify the most important skills to improve for your target roles. 
This text belongs to the page structure shown in the reference. 
 
7. MOTIVATIONAL QUOTE CARD 
At the upper-right of the page header area, retain the same quote-card placement from the 
reference. 
The card contains: 
• 
Small LOOP-MIND decorative icon 
• 
Quote text 
• 
– LOOP-MIND 
The visual component and position should remain consistent with the reference. 
If quote content is later made dynamic, it must come from the appropriate system/content source 
rather than hardcoding student information. 
 
8. FIRST CONTENT ROW 
The first content row contains three sections, exactly as shown in the reference. 
┌─────────────────────────────┐ 
│ Select Target Company       │ 
│ [ Company ▼ ]               │ 
│                             │ 
│ Select Target Role          │ 
│ [ Role ▼ ]                  │ 
└─────────────────────────────┘ 
 
┌─────────────────────────────┐

## SOURCE PAGE 219

│ Overall Readiness           │ 
│                             │ 
│       [ % ]                 │ 
│                             │ 
│ You are on track!           │ 
│ supporting description      │ 
└─────────────────────────────┘ 
 
┌─────────────────────────────┐ 
│ Quick Actions               │ 
│                             │ 
│ [Get Personalized Plan →]   │ 
│ [Try What-If Analysis →]    │ 
└─────────────────────────────┘ 
 
9. TARGET COMPANY 
Label: 
Select Target Company 
Provide a searchable/selectable company control. 
The selected company must be dynamic. 
Data source 
The selected target company should come from the student's profile/career-placement information 
or the student's current selection. 
Do not permanently use: 
Google 
The Google shown in the reference is only an example. 
 
10. TARGET ROLE 
Label: 
Select Target Role 
Provide a searchable/selectable role control.

## SOURCE PAGE 220

The available roles must be generated according to the available relevant data/context. 
Do not permanently use: 
Software Engineer 
The reference value is only an example. 
Context dependency 
Target roles should correspond to the selected target company where applicable. 
 
11. OVERALL READINESS 
Card title: 
Overall Readiness 
The readiness percentage must be dynamically calculated from the student's actual information and 
skill-gap analysis. 
Example shown in the reference: 
68% 
This must not be hardcoded. 
The visual circular readiness indicator must remain in the same position and structure. 
The displayed percentage should dynamically change according to the student's actual readiness. 
 
Readiness message 
The reference contains: 
You are on track! 
and supporting text. 
The message should be determined from the student's actual readiness state where dynamic 
readiness messaging is implemented. 
Do not use a fixed message regardless of the student's actual state. 
 
12. QUICK ACTIONS 
Card title: 
Quick Actions 
Two actions are shown in the reference: 
Primary 
Get Personalized Plan →

## SOURCE PAGE 221

Secondary 
Try What-If Analysis → 
Maintain the same two-button structure and placement. 
Their functionality should operate using the student's actual skill-gap data. 
Do not replace these with unrelated actions. 
 
13. SKILL GAP OVERVIEW 
Card title: 
Skill Gap Overview 
Supporting text: 
Here's a summary of your skills for the selected role. 
The card contains four dynamic metrics. 
Metric 1 
Total Required Skills 
Value must come from the actual selected target role/company requirements. 
Metric 2 
Skills You Have 
Value must come from the student's actual profile. 
Metric 3 
Skills to Improve 
Value must come from the skill-gap analysis. 
Metric 4 
Missing Evidence 
Value must come from actual evidence/profile information. 

## UPDATE — Unified Placement Readiness Percentage (Placement Readiness Percentage SDD §1-5)

The Placement Readiness % shown on the Student Dashboard's Placement Readiness card, the Skill
Gap page's Overall Readiness, and the Preparation Plan page's Current Readiness are now
guaranteed to be the exact same number for the exact same student/target — all three now read
through one shared backend lookup (`intelligence_service.get_latest_skill_gap_analysis` /
`get_readiness_summary`) instead of each page running its own stored-row query, and that lookup
runs a fresh analysis on demand (rather than showing "no analysis") whenever one doesn't already
exist for the student's current target, so visiting any one of the three pages first no longer
produces a different number than visiting another first. Every action that can change the
underlying result — adding/editing/deleting a skill, adding skill evidence, adding/deleting a
project or certification, uploading/re-uploading a resume, running a LinkedIn extraction, or
changing the target company/role (via the Dashboard, the Skill Gap page, or Career & Placement
on My Profile — all three write the same underlying target) — now triggers an immediate
recalculation when a target is already set, so the centralized result never goes stale between
visits.

## UPDATE — Skills You Have no longer shows 0 for a student with real skills (Skill Gap,
Profile Photo & Resume Management SDD §1-3)

"Skills You Have" on the Skill Gap page's overview was computed as "how many of the target
role's required skills the student already meets at the required level" (the same count the
"Already Strong" distribution bucket correctly measures) — so it read 0 for any student whose
real, stored skills (from the resume, from profile entry, from LinkedIn — already merged into
one deduplicated set at storage time) simply didn't happen to overlap with that particular
target's specific requirement list, even though the student genuinely has skills on file. It now
counts the student's own current distinct skills directly from the database, independent of the
current target — matching this card's original definition ("Value must come from the student's
actual profile"). Missing Evidence and Skills to Improve are unchanged: they were already
correctly agent-driven, dynamically calculated from the student's actual stored evidence rather
than a blanket "no evidence" count.

## UPDATE — My Profile: visible profile photo, photo delete, and full resume management
(Skill Gap, Profile Photo & Resume Management SDD §4-9)

The profile photo now actually renders as an image next to the student's name — it previously
showed the literal placeholder text "Photo" instead of the stored image, through a new
authenticated `GET /students/me/basic-info/photo/file` endpoint (the stored photo, like the
resume, is a server filesystem path with no other safe way to reach it from the browser). A
"Delete Photo" action is now available whenever a photo exists (`DELETE
/students/me/basic-info/photo`), clearing only the photo reference. Professional Links &
Resume's Resume field now supports the same actions Dashboard's resume card does — Upload (when
none exists), Replace, Download, and Delete (`DELETE /students/me/resume`) — all through the same
`/students/me/resume` endpoint and Resume Parser Agent workflow, so My Profile and the
Dashboard's own resume card always reflect one shared active resume, never two independent
records. Deleting the photo never touches any other profile data. **Superseded** by the Resume
Lifecycle UPDATE SDD below regarding Delete Resume specifically: it was originally scoped to
clear only the file reference, leaving resume-derived skills/projects/certifications in place —
that decision is corrected there.

## UPDATE — Dashboard's Upload Your Resume card stays visible after upload (Skill Gap, Profile
Photo & Resume Management SDD §11-12)

This card previously disappeared entirely once a resume existed (`{!dashboard.has_resume ? <card> :
null}`), leaving no way to manage/replace it from the Dashboard afterward. It now always renders,
switching its heading/copy/dropzone hint between "Upload Your Resume" (no resume yet) and
"Resume Available" / "Replace resume" (one already exists) — uploading through it always goes
through the same `/students/me/resume` endpoint and Resume Parser Agent extraction as My
Profile's own resume management and the Professional Links onboarding step.

## UPDATE — Missing Evidence row status (Student Portal Skill Gap SDD §6)

A required skill the student meets or exceeds the required level for, but has no supporting
evidence, is now shown as "Missing Evidence" in the All Skills table (a new status distinct
from "Strong") rather than being silently treated as fully verified — it already counted
toward this Missing Evidence number, so the per-row status now agrees with it. Example: a
student claims Python at the required level with no supporting evidence — Python appears
as Missing Evidence, not Strong.
 
Important 
The reference values: 
18 
11 
7 
4

## SOURCE PAGE 222

must not be hardcoded. 
They are only reference values showing the intended visual presentation. 
 
14. SKILL DISTRIBUTION 
Card title: 
Skill Distribution 
Use the same donut-chart structure shown in the reference. 
The distribution must dynamically represent the student's actual skill state. 
The reference contains: 
• 
Already Strong 
• 
Needs Improvement 
• 
Missing 
• 
Not Relevant 
These categories must remain part of the displayed structure. 
 
Dynamic categories 
Already Strong 
Skills where the student's current proficiency satisfies or exceeds the required level. 
Needs Improvement 
Skills that exist in the student's profile but require additional improvement to meet the target 
requirement. 
Missing 
Required skills that the student does not currently have. 
Not Relevant 
Skills that are not applicable to the selected target context. 
The chart percentages and counts must be dynamically calculated. 
 
15. TOP PRIORITY AREAS 
Card title: 
Top Priority Areas 
Supporting text:

## SOURCE PAGE 223

These skills will have the highest impact on your placement readiness. 
Display the highest-priority skill gaps. 
The reference shows numbered entries: 
1  Data Structures & Algorithms 
2  System Design 
3  Cloud (AWS/GCP) 
4  Database / SQL 
5  Backend Development 
These are reference examples only. 
The actual skills must be generated from the student's analysis. 
 
Each priority entry 
Each row should contain: 
1. Rank number 
2. Skill name 
3. Impact level 
Example impact labels from the reference: 
• 
High Impact 
• 
Medium Impact 
The actual priority and impact must be based on the student's skill-gap analysis. 
 
16. SKILL FILTER TABS 
Below the analysis cards, maintain the same filter structure. 
Tabs: 
All Skills 
To Improve (N) 
Missing (N) 
Strong (N) 
Not Relevant (N) 
The counts must be dynamic. 
Example:

## SOURCE PAGE 224

To Improve (7) 
Missing (4) 
Strong (11) 
Not Relevant (4) 
must not be hardcoded. 
 
Tab behavior 
All Skills 
Display all analyzed skills. 
To Improve 
Display only skills categorized as requiring improvement. 
Missing 
Display only missing required skills. 
Strong 
Display skills where the student's proficiency meets/exceeds the required level. 
Not Relevant 
Display skills that are not relevant to the selected target context. 
 
17. SEARCH SKILLS 
On the right side of the filter row, retain: 
Search skills... 
with the search icon. 
The search must dynamically filter the currently displayed skills. 
Search should operate against the actual skill data. 
It must not search against a hardcoded list. 
 
18. SKILL ANALYSIS TABLE 
The table must retain the same structure shown in the reference. 
Columns:

## SOURCE PAGE 225

Column 
Skill 
Category 
Your Level 
Required Level 
Status 
Priority 
Action 
 
19. SKILL COLUMN 
Display the actual skill name. 
Example from the reference: 
Data Structures & Algorithms 
is only an example. 
Actual values must come from the student's profile and selected target requirements. 
 
20. CATEGORY COLUMN 
Display the appropriate category for each skill. 
Examples shown in the reference: 
• 
Core CS 
• 
System Design 
• 
Cloud 
• 
Database 
• 
Web Development 
These are examples. 
The actual category must correspond to the skill's stored/derived category. 
 
21. YOUR LEVEL 
Display the student's actual proficiency level for that skill. 
The reference uses levels such as:

## SOURCE PAGE 226

• 
Beginner 
• 
Intermediate 
• 
Not Started 
• 
Advanced 
The displayed value must come from the student's actual skill data. 
 
22. REQUIRED LEVEL 
Display the proficiency level required for the selected target role/company. 
This must be dynamically retrieved/generated from the relevant target requirements. 
The reference values such as: 
Advanced 
and 
Intermediate 
are examples only. 
 
23. STATUS 
Each skill must have a dynamically determined status. 
Reference statuses include: 
• 
To Improve 
• 
Missing 
The status must be generated from the comparison between: 
Student's Current Level 
        + 
Required Level 
        ↓ 
Skill Gap Analysis 
        ↓ 
Status 
 
24. PRIORITY 
Display the priority assigned to each skill.

## SOURCE PAGE 227

Reference values include: 
• 
High 
• 
Medium 
Priority must be dynamically determined from the actual skill-gap analysis. 
 
25. ACTION 
The reference contains: 
View Resources → 
for each skill. 
Maintain this action structure. 
The resources/action must correspond to the actual selected skill. 
 
26. DYNAMIC DATA REQUIREMENT 
This page must work as a real student-specific analysis page. 
The system should follow: 
Authenticated Student 
        ↓ 
Load Student Profile 
        ↓ 
Load Student Skills 
        ↓ 
Load Skill Evidence 
        ↓ 
Load Target Company 
        ↓ 
Load Target Role 
        ↓ 
Load Required Skills 
        ↓ 
Compare Current vs Required 
        ↓

## SOURCE PAGE 228

Calculate Skill Gap 
        ↓ 
Calculate Readiness 
        ↓ 
Generate Distribution 
        ↓ 
Generate Priority Areas 
        ↓ 
Render Skill Table 
 
27. NO HARDCODED STUDENT DATA 
Strictly do not hardcode values from the reference image. 
Do not hardcode: 
Google 
Software Engineer 
68% 
18 
11 
7 
4 
Data Structures & Algorithms 
System Design 
Cloud (AWS/GCP) 
Database / SQL 
Backend Development 
These are only visual/reference examples. 
The UI structure remains fixed, while the contents change according to the student. 
 
28. STUDENT-SPECIFIC DATA FLOW 
The page must use the currently authenticated student's identity/session. 
Logged-in Student

## SOURCE PAGE 229

↓ 
Student ID 
       ↓ 
Student Profile 
       ↓ 
Student Skills 
       ↓ 
Student Academic Information 
       ↓ 
Projects 
       ↓ 
Certifications 
       ↓ 
Coding Experience 
       ↓ 
Professional Links / Resume 
       ↓ 
Career / Placement Preferences 
       ↓ 
Learning / Preparation 
       ↓ 
Skill Evidence 
       ↓ 
Skill Gap Analysis 
Only relevant information required for this page should be used in the analysis. 
 
29. TARGET CONTEXT 
The analysis must be based on the selected target context. 
Target Company 
      + 
Target Job Role

## SOURCE PAGE 230

↓ 
Required Skills 
      + 
Required Proficiency 
      ↓ 
Student's Existing Skills 
      + 
Student Proficiency 
      + 
Evidence 
      ↓ 
Skill Gap Analysis 
Changing the target company or target role should update the relevant analysis dynamically. 
 
30. SEARCHABLE CONTROLS 
Where the reference uses selectable controls, use searchable controls when the dataset/context 
requires it. 
The controls must be populated from the relevant data source. 
Do not create arbitrary hardcoded dropdown values. 
 
31. RESPONSIVE BEHAVIOR 
The page should preserve the reference's visual hierarchy while adapting to screen size. 
However: 
Responsive behavior must not change the intended desktop layout structure. 
The desktop implementation should match the uploaded reference as closely as possible. 
 
32. FOOTER 
The footer must be retained exactly in the same bottom-area structure as the reference. 
Footer links: 
• 
Terms of Use 
• 
Privacy Policy

## SOURCE PAGE 231

• 
Membership Plans 
• 
Help 
Below: 
LOOP-MIND © 
Do not omit the footer. 
Do not replace it with a generic footer. 
 
33. VISUAL DESIGN REQUIREMENT 
The reference establishes the visual direction: 
• 
Dark LOOP-MIND student portal interface 
• 
Dark background 
• 
Dark cards/panels 
• 
Cyan/teal accent 
• 
Rounded cards 
• 
Thin borders 
• 
Compact dashboard spacing 
• 
Teal active states 
• 
Status badges 
• 
Circular readiness visualization 
• 
Donut skill distribution chart 
• 
Structured data table 
• 
Consistent iconography 
• 
Same navbar/footer positioning 
The implementation should visually follow the uploaded reference rather than introducing a 
different design system. 
 
34. EXACT LAYOUT PRESERVATION RULE 
This is the most important UI requirement: 
The uploaded Skill Gap Analysis image is the reference layout. Reproduce its layout, not merely its 
content. 
Do not: 
• 
Move cards

## SOURCE PAGE 232

• 
Change card ordering 
• 
Remove sections 
• 
Add unrelated sections 
• 
Replace the table with cards 
• 
Move Quick Actions 
• 
Move Overall Readiness 
• 
Move Skill Distribution 
• 
Move Top Priority Areas 
• 
Remove filter tabs 
• 
Remove search 
• 
Remove footer 
• 
Change navbar structure 
• 
Create a different dashboard layout 
The layout remains fixed. 
Only the underlying data and analysis results are dynamic. 
 
35. REFERENCE VS DYNAMIC CONTENT 
Fixed 
Page structure 
Navbar 
Navigation placement 
Page heading placement 
Quote-card placement 
Target-selection card placement 
Overall-readiness card placement 
Quick-actions card placement 
Skill-gap-overview placement 
Skill-distribution placement 
Top-priority placement 
Filter placement 
Search placement

## SOURCE PAGE 233

Table structure 
Footer structure 
Visual hierarchy 
Dynamic 
Student-specific data 
Target company 
Target role 
Readiness percentage 
Readiness state 
Skill counts 
Skill distribution 
Priority areas 
Skill names 
Skill categories 
Student levels 
Required levels 
Status 
Priority 
Resource availability 
Search results 
Filter counts 
 
36. FINAL USER FLOW 
LOGIN / OTP SUCCESS 
        ↓ 
STUDENT DASHBOARD 
        │ 
        ├───────────────┐ 
        │               │ 
        ↓               ↓ 
   Skill Gap      Placement Readiness

## SOURCE PAGE 234

│               │ 
        │      View Detailed Analysis 
        │               │ 
        └───────┬───────┘ 
                ↓ 
       SKILL GAP ANALYSIS 
                ↓ 
       Load Student Data 
                ↓ 
       Load Target Context 
                ↓ 
       Analyze Skill Gaps 
                ↓ 
       Calculate Readiness 
                ↓ 
       Display Analysis 
                ↓ 
 ┌───────────────────────────────┐ 
 │ Skill Gap Overview            │ 
 │ Skill Distribution            │ 
 │ Top Priority Areas            │ 
 │ Skill Filters                 │ 
 │ Search                        │ 
 │ Skill Analysis Table          │ 
 └───────────────────────────────┘ 
 
37. IMPLEMENTATION INSTRUCTION FOR ANTIGRAVITY 
Build the LOOP-MIND Student Portal Skill Gap Analysis page using the uploaded reference image 
as the exact UI/layout reference. 
The page must retain the same overall structure, component placement, hierarchy, navigation, 
cards, filters, search area, table, and footer shown in the reference. 
The reference image's data is not real student data and must never be hardcoded.

## SOURCE PAGE 235

Connect the page to the authenticated student's actual profile and relevant database data. 
Dynamically load the student's skills, proficiency levels, evidence, target company, target role, 
required skills, required proficiency levels, and other relevant information. Dynamically calculate and 
display the student's skill gap, readiness percentage, skill distribution, priority areas, filter counts, 
statuses, priorities, and table contents. 
The Skill Gap page must open from both: 
1. Student Dashboard → Skill Gap 
2. Student Dashboard → Placement Readiness → View Detailed Analysis 
Both must open the same Skill Gap Analysis page for the currently authenticated student. 
Maintain the reference layout exactly while making the data fully dynamic. Do not hardcode 
student-specific values and do not redesign the page. 
 
MASTER RULE 
REFERENCE LAYOUT = FIXED 
STUDENT DATA = DYNAMIC 
SKILL ANALYSIS = DYNAMIC 
TARGET CONTEXT = DYNAMIC 
NO HARDCODED STUDENT VALUES 
NO UNREQUESTED UI CHANGES 
This specification should be treated as the implementation reference for the LOOP-MIND Student 
Skill Gap Analysis page. 
LOOP-MIND — SKILL GAP ANALYSIS 
Quick Actions — Functional Specification Update 
This update applies only to the two Quick Actions shown on the Skill Gap Analysis page. 
 
1. GET PERSONALIZED PLAN 
Button 
Get Personalized Plan → 
Purpose 
This action generates a personalized preparation plan for the currently authenticated student based 
on the student's selected target context and the dynamically calculated Skill Gap Analysis. 
The plan must be generated using the information already available on the Skill Gap Analysis page, 
including the student's relevant data, selected company/role, required skills, current skills, skill gaps, 
and other applicable constraints/data. 
Flow 
Student Skill Gap Analysis

## SOURCE PAGE 236

↓ 
Student selects / has 
Target Company and/or Target Role 
        ↓ 
Skill Gap Analysis is dynamically calculated 
        ↓ 
Student clicks 
"Get Personalized Plan" 
        ↓ 
Generate Personalized Preparation Plan 
        ↓ 
Store the generated plan 
        ↓ 
Do NOT open the Preparation Plan page 
Critical Navigation Rule 
Clicking Get Personalized Plan → must NOT navigate the student to the Preparation Plan page. 
The button's purpose here is to generate and store the plan only. 
There should be no automatic page navigation to: 
Preparation Plan 
after generation. 
The generated plan belongs to the student's Preparation Plan data and can be accessed from the 
existing Preparation Plan page separately. 
 
2. PLAN GENERATION 
The generated plan must be personalized to the student's actual current state. 
It must not use a fixed/hardcoded plan. 
The generation context should be based on the dynamically available information from the Skill Gap 
Analysis. 
Student Data 
      + 
Target Company 
      +

## SOURCE PAGE 237

Target Role 
      + 
Required Skills 
      + 
Current Skills 
      + 
Skill Gaps 
      + 
Priority Areas 
      ↓ 
Personalized Plan Generation 
      ↓ 
Generated Preparation Plan 
      ↓ 
Store for that Student 
The exact plan-generation content/structure can be specified separately later. 
 
3. TRY WHAT-IF ANALYSIS 
Button 
Try What-If Analysis → 
This action is completely different from Get Personalized Plan. 
It should not generate or store the student's normal preparation plan. 
 
4. CLICK BEHAVIOR 
When the student clicks: 
Try What-If Analysis → 
open a centered card/modal on the same Skill Gap Analysis page. 
Required behavior 
Skill Gap Analysis Page 
        ↓ 
Click "Try What-If Analysis"

## SOURCE PAGE 238

↓ 
Centered What-If Card / Modal 
        ↓ 
Student enters a question 
The card/modal must appear at the center of the page. 
Do not open a separate page. 
Do not navigate away from Skill Gap Analysis. 
 
5. WHAT-IF CARD / MODAL 
The card/modal should contain a text-input area where the student can type a What-If 
question/prompt. 
Example: 
┌──────────────────────────────────────────────────────────────┐ 
│                                                              │ 
│                 Try What-If Analysis                         │ 
│                                                              │ 
│  What if I learn Generative AI?                              │ 
│                                                              │ 
│  ┌────────────────────────────────────────────────────────┐  │ 
│  │ What if I learn Generative AI?                         │  │ 
│  │                                                        │  │ 
│  └────────────────────────────────────────────────────────┘  │ 
│                                                              │ 
│                         [ Analyze ]                          │ 
│                                                              │ 
└──────────────────────────────────────────────────────────────┘ 
The exact visual styling should remain consistent with the existing LOOP-MIND Skill Gap Analysis 
page. 
 
6. WHAT-IF INPUT 
The student can enter a natural-language question such as: 
What if I learn Generative AI?

## SOURCE PAGE 239

The system should analyze the question against the student's current skill-gap context. 
The What-If analysis should determine relevant information such as: 
• 
Skills demanded for the mentioned area/domain 
• 
Relevant job opportunities/roles associated with that area 
• 
How the mentioned learning area relates to the student's current skill profile 
• 
Other relevant details resulting from the What-If analysis 
The exact response structure can be expanded later. 
 
7. WHAT-IF ANALYSIS FLOW 
Student clicks 
"Try What-If Analysis" 
        ↓ 
Centered card/modal opens 
        ↓ 
Student enters What-If question 
        ↓ 
Example: 
"What if I learn Generative AI?" 
        ↓ 
Analyze the entered question 
        + 
Student's current profile/skills 
        + 
Current Skill Gap context 
        ↓ 
Generate What-If Analysis 
        ↓ 
Display the analysis in the same 
centered card/modal 
 
8. IMPORTANT DIFFERENCE BETWEEN THE TWO ACTIONS

## SOURCE PAGE 240

Action 
Behavior 
Get Personalized Plan → Generate personalized preparation plan and store it 
Get Personalized Plan → Do NOT navigate to Preparation Plan page 
Try What-If Analysis → Open centered card/modal 
Try What-If Analysis → Student enters a natural-language What-If question 
Try What-If Analysis → Analyze the question using relevant student/skill-gap context 
Try What-If Analysis → Display the resulting analysis in the card/modal 
What-If analysis 
No separate page navigation 

## UPDATE — What-If result content + plan link (Student Portal UPDATE SDD §16-19, §11)

The What-If card's result now also shows, in a dedicated section within the same centered
card: the student's current readiness percentage vs. the genuinely recalculated projected
readiness percentage if the asked-about skill were learned to the target role's required
level (never a fabricated number, and the student's real stored skills are never modified),
plus any other roles at the target company whose real stored requirements include that
skill. After "Get Personalized Plan" succeeds, a "View your plan on the Preparation Plan
page →" link now appears — this is a student-initiated click, not automatic navigation, so
"Do NOT navigate to Preparation Plan page" above still holds for the action itself. 
 
9. STRICT IMPLEMENTATION RULE 
GET PERSONALIZED PLAN 
        ↓ 
GENERATE 
        ↓ 
STORE 
        ↓ 
STAY ON SKILL GAP PAGE 
NOT: 
GET PERSONALIZED PLAN 
        ↓ 
GENERATE 
        ↓ 
OPEN PREPARATION PLAN PAGE   ❌ 
And: 
TRY WHAT-IF ANALYSIS 
        ↓ 
OPEN CENTERED MODAL/CARD 
        ↓ 
ENTER QUESTION 
        ↓

## SOURCE PAGE 241

ANALYZE 
        ↓ 
SHOW RESULT IN MODAL/CARD 
This update should be added to the existing LOOP-MIND Skill Gap Analysis Page specification 
without changing the rest of the page layout or functionality. 
LOOP-MIND — STUDENT PORTAL 
Dashboard Updates — Footer + Target Company 
1. GLOBAL STUDENT PORTAL FOOTER 
The Student Portal footer must be exactly the same across every Student Portal page. 
This footer must use the same footer structure, placement, content, styling, spacing, and behavior 
as the footer defined for the LOOP-MIND Landing Page. 
Footer Rules 
• 
The footer must remain unchanged across all Student Portal pages. 
• 
Do not create different footer versions for different pages. 
• 
Do not add or remove footer items on individual pages. 
• 
The same footer must appear on: 
o 
Student Dashboard 
o 
Skill Gap Analysis 
o 
Preparation Plan 
o 
Jobs 
o 
My Progress 
o 
Any other Student Portal page 
• 
Footer placement must remain consistent with the reference layout. 
• 
Footer text must remain exactly the same as the Landing Page footer. 
• 
Footer styling must remain consistent with the Landing Page. 
• 
Footer navigation/interaction behavior must remain consistent throughout the Student 
Portal. 
Footer Interaction 
When a footer item is clickable: 
Student Portal Page 
        ↓ 
Click Footer Item

## SOURCE PAGE 242

↓ 
Open the corresponding content 
        ↓ 
Centered Card / Modal 
The opened card/modal must appear at the center of the page. 
The footer itself must not change when the card/modal is opened. 
No separate footer design or alternate footer content should be introduced for the Student Portal. 
 
2. TARGET COMPANY 
Location 
The Target Company section is present on the Student Dashboard. 
Reference structure: 
┌──────────────────────────────────────────────┐ 
│              Target Company                  │ 
│                                              │ 
│              Not set yet                     │ 
│                                              │ 
│   Set a target company to get personalized   │ 
│   recommendations, skill analysis and        │ 
│   preparation plan.                          │ 
│                                              │ 
│        [ Set Target Company → ]              │ 
└──────────────────────────────────────────────┘ 
The exact content shown must be based on the student's actual profile/data state. 
 
Set Target Company Action 
When the student clicks: 
Set Target Company → 
the student must be able to set their target company. 
Flow 
Student Dashboard

## SOURCE PAGE 243

↓ 
Target Company 
        ↓ 
Click "Set Target Company" 
        ↓ 
Target Company Selection 
        ↓ 
Student selects company 
        ↓ 
Save Target Company 
        ↓ 
Dashboard updates dynamically 
Company Selection 
The company selection must be dynamic. 
• 
Do not hard-code a fixed company value into the dashboard. 
• 
The available company data must come from the application's actual company 
data/database. 
• 
The student must be able to select their target company from the available company data. 
• 
Company selection should support search where applicable. 
• 
The selected company must be stored against the student's profile. 
• 
The dashboard must retrieve the student's saved target company from the database. 
 
3. DYNAMIC TARGET COMPANY STATE 
Before a company is selected 
The Target Company section should reflect that the student has not configured a target company. 
Target Company 
 
Not set yet 
 
Set a target company to get personalized 
recommendations, skill analysis and preparation plan.

## SOURCE PAGE 244

[ Set Target Company → ] 
After a company is selected 
The same dashboard section must dynamically reflect the student's selected company. 
Target Company 
 
[ Student's Selected Company ] 
 
[ ...existing dashboard content based on the student's data... ] 
The company name must never be hard-coded. 
It must be retrieved from the student's stored profile information. 
 
4. DATA-DRIVEN REQUIREMENT 
All Target Company information shown on the Student Dashboard must be generated from the 
student's actual stored data. 
Student Profile 
      ↓ 
Stored Target Company 
      ↓ 
Student Dashboard 
      ↓ 
Target Company Section 
If the student changes their target company, the dashboard must reflect the updated company 
dynamically. 
No static/demo company should be displayed as the student's target company unless that company 
is actually stored for that student. 
 
5. REFERENCE-LAYOUT RULE 
The Student Dashboard layout must remain exactly aligned with the provided reference 
dashboard. 
For this update: 
• 
Do not redesign the dashboard.

## SOURCE PAGE 245

• 
Do not move the Target Company section. 
• 
Do not change the existing dashboard card structure. 
• 
Do not change the footer layout. 
• 
Do not introduce a different footer. 
• 
Do not alter the existing page hierarchy. 
• 
Only make the Target Company functionality dynamic. 
• 
All displayed student-specific values must come from the student's actual data. 
Core principle 
Reference layout remains fixed. Data and student-specific content remain dynamic. 
FIXED 
├── Page structure 
├── Card placement 
├── Footer structure 
├── Footer content 
├── Footer placement 
└── Overall visual layout 
 
DYNAMIC 
├── Student information 
├── Target company 
├── Profile-related values 
├── Skill-related values 
├── Project-related values 
├── Certification-related values 
└── Other student-specific dashboard data 
No unsupported functionality or additional behavior should be introduced beyond the specified 
requirements. 
LOOP-MIND — GLOBAL DROPDOWN & DATASET REQUIREMENT 
This is a global requirement for the entire LOOP-MIND website. 
It applies to every portal and every page, including: 
• 
Student Portal

## SOURCE PAGE 246

• 
Recruiter Portal 
• 
Authentication flows 
• 
Profile creation/editing 
• 
Dashboard pages 
• 
Skill Gap Analysis 
• 
Preparation Plan 
• 
Jobs 
• 
My Progress 
• 
Recruiter workflows 
• 
Any future page containing dropdown/select fields 
1. Every Dropdown Must Have a Dataset 
Whenever a dropdown exists anywhere in the LOOP-MIND website: 
The implementation must provide and populate the complete, context-appropriate dataset 
automatically. 
The user will not provide the dropdown datasets separately. 
Example: 
Select Target Company 
        ↓ 
Company Dropdown Dataset 
        ↓ 
Searchable Company Options 
The implementation must create the required company dataset according to the purpose of that 
field. 
 
2. Context-Based Dataset Generation 
The dataset must be determined by the actual purpose and context of the field. 
For example: 
Target Company 
Select Target Company 
→ Dataset must contain company options, not generic or unrelated values. 
Target Job Role 
Select Target Role

## SOURCE PAGE 247

→ Dataset must contain job-role options relevant to the platform. 
Programming Languages 
Programming Languages 
→ Dataset must contain programming languages. 
Skill Category 
Skill Category 
→ Dataset must contain appropriate skill categories. 
Country 
Country 
→ Dataset must contain country options. 
State 
State 
→ Dataset must correspond to the selected country/context. 
City 
City 
→ Dataset must correspond to the selected state/country/context where applicable. 
The dataset must match the field's actual requirement. 
 
3. Searchable Dropdowns 
As a general rule: 
Dropdowns should be searchable wherever the number of possible options makes searching 
useful. 
For example: 
┌────────────────────────────────────┐ 
│ Select Target Company            │ 
├────────────────────────────────────┤ 
│ Search company...                  │ 
├────────────────────────────────────┤ 
│ Company Option                     │ 
│ Company Option                     │ 
│ Company Option                     │

## SOURCE PAGE 248

│ ...                                │ 
└────────────────────────────────────┘ 
The search must operate against the actual dataset used by that dropdown. 
 
4. Non-Searchable Dropdowns 
If a particular dropdown has a small, fixed set of options where search is unnecessary, it may remain 
a normal dropdown. 
However: 
Non-searchable does NOT mean empty or manually left for later. 
It must still contain the complete context-appropriate dataset. 
Example: 
Gender 
├── Male 
├── Female 
└── Other 
 
5. Dependent / Context-Aware Dropdowns 
Where one dropdown depends on another, the options must update dynamically. 
Example: 
Country 
   ↓ 
State 
   ↓ 
City 
The system must not display unrelated values. 
Similarly: 
College 
   ↓ 
Degree 
   ↓ 
Branch

## SOURCE PAGE 249

and wherever applicable: 
Target Company 
   ↓ 
Target Role 
The available options should be determined by the relevant stored/application data and context. 
 
6. No Placeholder-Only Dropdowns 
The following is not acceptable: 
Select Company 
with no actual options. 
Likewise, do not leave implementation placeholders such as: 
Company 1 
Company 2 
Company 3 
unless those are genuinely part of the intended dataset. 
Every dropdown must be implemented with its required data. 
 
7. Completeness Requirement 
During implementation, every dropdown/select field must be identified and checked. 
The implementation must ensure: 
ALL DROPDOWN FIELDS 
        ↓ 
Identify Context 
        ↓ 
Determine Required Dataset 
        ↓ 
Generate/Provide Dataset 
        ↓ 
Populate Dropdown 
        ↓ 
Add Search Where Appropriate

## SOURCE PAGE 250

↓ 
Add Context/Dependency Logic Where Required 
        ↓ 
Verify No Dropdown Is Missing Data 
This applies to existing fields and newly added fields. 
 
8. Important Rule for LOOP-MIND 
The user does not need to separately provide datasets for dropdowns. 
The implementation is responsible for creating the necessary datasets based on: 
• 
Field purpose 
• 
Page context 
• 
Portal context 
• 
Existing application requirements 
• 
Relationships between fields 
• 
Student/Recruiter workflows 
Core requirement 
Every dropdown across the entire LOOP-MIND website must be complete, context-appropriate, 
populated, and functional. Searchable dropdowns should be used wherever appropriate. No 
dropdown should be left without its required dataset. 
This is a global LOOP-MIND requirement, not a requirement limited to the Student Dashboard or 
any single page. 
LOOP-MIND — STUDENT PORTAL 
PREPARATION PLAN PAGE — SDD + REFERENCE LAYOUT 
1. PAGE PURPOSE 
The Preparation Plan page is a Student Portal page used to display and manage the student's 
personalized preparation plan. 
The page must: 
• 
Follow the uploaded reference image exactly in layout and structure. 
• 
Use the same section placement, card arrangement, navigation, footer placement, spacing 
hierarchy, and overall composition shown in the reference. 
• 
Keep the layout fixed. 
• 
Keep the displayed information and preparation plan fully dynamic.

## SOURCE PAGE 251

• 
Use the student's actual stored profile, skills, target company, target role, academic year, 
skill-gap analysis, and generated preparation-plan data. 
• 
Never use hard-coded student-specific values. 
 
2. PAGE OPENING / NAVIGATION 
The page must open from the Student Portal navigation. 
Student Portal Navbar 
Dashboard | Skill Gap | Preparation Plan | Jobs | My Progress 
When the student clicks: 
Preparation Plan 
the application must open the Preparation Plan page. 
Student Portal 
      ↓ 
Click "Preparation Plan" 
      ↓ 
Preparation Plan Page 
The page must use the exact reference layout provided. 
 
3. PREPARATION PLAN PAGE — REFERENCE LAYOUT 
The following structure must be preserved from the uploaded reference. 
┌──────────────────────────────────────────────────────────────────────────┐ 
│ LOOP-MIND                                      Dashboard Skill Gap       │ 
│                                                Preparation Plan Jobs    │ 
│                                                My Progress              │ 
├──────────────────────────────────────────────────────────────────────────┤ 
│                                                                          │ 
│ Preparation Plan                              [Quote / LOOP-MIND Card]  │ 
│ A personalized plan based on your current                               │ 
│ year, goals and target company.                                         │ 
│                                                                          │ 
├──────────────────────────────────────────────────────────────────────────┤

## SOURCE PAGE 252

│                                                                          │ 
│ ┌──────────────────────────────────────────────┐ ┌─────────────────────┐ │ 
│ │ Select Target Company                       │ │ Current Readiness   │ │ 
│ │ [ Target Company ▼ ]                        │ │                     │ │ 
│ │                                              │ │        XX%          │ │ 
│ │ Select Target Role                           │ │   Readiness Ring    │ │ 
│ │ [ Target Role ▼ ]                            │ │                     │ │ 
│ │                                              │ │ You are on track!   │ │ 
│ │ Your Academic Year                           │ │ Dynamic message     │ │ 
│ │ [ Academic Year ▼ ]                          │ │                     │ │ 
│ │                                              │ │                     │ │ 
│ │                    [Generate Preparation Plan →]                     │ │ 
│ └──────────────────────────────────────────────┘ └─────────────────────┘ │ 
│                                                                          │ 
├──────────────────────────────────────────────────────────────────────────┤ 
│                                                                          │ 
│ ┌────────────────────────────────────┐ ┌──────────────────────────────┐ │ 
│ │ Year-Wise Focus                    │ │ Your Goals                    │ │ 
│ │                                    │ │                              │ │ 
│ │ 1st Year ─ 2nd Year ─ 3rd Year ─ Final Year                         │ 
│ │                                    │ │ Short-Term Goals │ Long-Term│ │ 
│ │ Current year highlighted            │ │ Goals            │ Goals    │ │ 
│ │                                    │ │                  │          │ │ 
│ └────────────────────────────────────┘ └──────────────────────────────┘ │ 
│                                                                          │ 
│                                      ┌────────────────────────────────┐  │ 
│                                      │ AI Recommendations              │  │ 
│                                      │                                │  │ 
│                                      │ Recommendation 1 →             │  │ 
│                                      │ Recommendation 2 →             │  │ 
│                                      │ Recommendation 3 →             │  │

## SOURCE PAGE 253

│                                      │ Recommendation 4 →             │  │ 
│                                      │ Recommendation 5 →             │  │ 
│                                      └────────────────────────────────┘  │ 
│                                                                          │ 
├──────────────────────────────────────────────────────────────────────────┤ 
│                                                                          │ 
│ Detailed Preparation Plan                         [ Export Plan ↓ ]      │ 
│ A step-by-step plan to help you achieve your goals.                     │ 
│                                                                          │ 
│ [All] [DSA] [Development] [System Design] [Databases]                  │ 
│ [Interview Prep] [Projects] [Other]                                     │ 
│                                                                          │ 
│ ┌──────────────────────────────────────────────────────────────────────┐ │ 
│ │ Skill / Topic | Category | Current | Target | Start | End | Status │ │ 
│ │               |          | Level   | Level  | Date  | Date|        │ │ 
│ │ Priority | Resources | Action                                      │ │ 
│ ├──────────────────────────────────────────────────────────────────────┤ │ 
│ │ Dynamic preparation-plan entries                                     │ │ 
│ │                                                                      │ │ 
│ │                                              [View Plan →]           │ │ 
│ └──────────────────────────────────────────────────────────────────────┘ │ 
│                                                                          │ 
├──────────────────────────────────────────────────────────────────────────┤ 
│ Terms of Use     Privacy Policy     Membership Plans     Help            │ 
│                              LOOP-MIND ©                                  │ 
└──────────────────────────────────────────────────────────────────────────┘ 
Important: This is a structural specification of the uploaded reference. The actual implementation 
must preserve the same visual arrangement and proportions as the provided reference image, 
rather than treating this ASCII representation as a redesign. 
 
4. HEADER / NAVIGATION 
The header must remain consistent with the Student Portal.

## SOURCE PAGE 254

Left 
LOOP-MIND 
Right 
Dashboard 
Skill Gap 
Preparation Plan 
Jobs 
My Progress 
Preparation Plan must be visually indicated as the currently active page, matching the reference. 
Do not introduce a different navigation structure. 
 
5. PAGE TITLE SECTION 
Display: 
Preparation Plan 
Supporting description: 
A personalized plan based on your current year, goals and target company. 
The description can reflect the actual student's context where the existing design supports dynamic 
content, but the visual placement must remain the same. 
 
6. TOP CONFIGURATION SECTION 
The top configuration card contains: 
Select Target Company 
Select Target Company 
[ Target Company ▼ ] 
The options must come from the LOOP-MIND company dataset. 
It must be searchable where appropriate. 
The selected company must be dynamic. 
 
Select Target Role 
Select Target Role 
[ Target Role ▼ ]

## SOURCE PAGE 255

The options must come from the appropriate job-role dataset. 
The available roles must be context-aware where applicable. 
 
Your Academic Year 
Your Academic Year 
[ Academic Year ▼ ] 
The value must be based on the student's actual academic information. 
 
Generate Preparation Plan 
[ Generate Preparation Plan → ] 
This button generates or regenerates the preparation plan using the student's currently 
selected/configured information. 
 
7. CURRENT READINESS CARD 
The right-side card must remain in the same position as the reference. 
It contains: 
Current Readiness 
A circular readiness indicator: 
XX% 
and the corresponding readiness message. 
The readiness percentage must be calculated/retrieved from the student's actual LOOP-MIND data. 
It must not use a hard-coded value such as 68%. 
 
8. YEAR-WISE FOCUS 
The Year-Wise Focus section must follow the reference structure. 
Year-Wise Focus 
 
1st Year 
2nd Year 
3rd Year 
Final Year

## SOURCE PAGE 256

The student's current academic year must be reflected dynamically. 
The corresponding focus information must be generated/displayed according to the student's actual 
academic context and preparation data. 
Do not permanently hard-code one year as the active year. 

## UPDATE — Year-Wise Focus becomes a roadmap (Preparation Plan UPDATE SDD §4-9)

Below the existing year pills and focus text (both unchanged), the card now shows the active
plan's actual skill learning sequence — numbered, connected steps, each with its own real
Start Date and End Date, generated as part of the Preparation Plan (not hardcoded, not every
skill sharing the same window). Each step's window begins the day after the previous step's
window ends, so the timeline is continuous and chronologically consistent, in the same
priority order the Preparation Plan Agent already produces. This is the same data already
shown in the Detailed Preparation Plan table below, surfaced here as a roadmap.
 
9. YOUR GOALS 
The Goals section contains: 
Short-Term Goals 
Short-Term Goals 
Long-Term Goals 
Long-Term Goals 
The goals must come from the student's actual profile/preparation information. 
Where the design uses selectable goal items, their completion state must be stored dynamically. 
 
10. AI RECOMMENDATIONS 
The AI Recommendations card must remain in the same position and structure as the reference. 
The recommendations must be based on the student's actual: 
• 
Skills 
• 
Skill gaps 
• 
Target company 
• 
Target role 
• 
Academic year 
• 
Goals 
• 
Preparation requirements 
The recommendations must therefore change when the underlying student information changes. 
Do not use static recommendation values as the final implementation. 
 
11. DETAILED PREPARATION PLAN 
This is the primary plan display section. 
Heading: 
Detailed Preparation Plan

## SOURCE PAGE 257

Description: 
A step-by-step plan to help you achieve your goals. 
The plan must be dynamically populated. 
 
12. PLAN FILTERS 
The reference contains: 
All 
DSA 
Development 
System Design 
Databases 
Interview Prep 
Projects 
Other 
These filters must operate on the actual preparation-plan dataset. 
Selecting a category must display only the corresponding plan items. 
All must display all applicable plan items. 
 
13. PREPARATION PLAN TABLE 
The table structure must follow the reference. 
Columns: 
Skill / Topic 
Category 
Current Level 
Target Level 
Start Date 
End Date 
Status 
Priority 
Resources 
Action

## SOURCE PAGE 258

The values must be dynamically generated from the student's preparation plan. 
Example structure only: 
Skill / Topic 
Data Structures & Algorithms 
 
Category 
Core CS 
 
Current Level 
Student's actual level 
 
Target Level 
Required target level 
 
Start Date 
Generated/stored plan date 
 
End Date 
Generated/stored plan date 
 
Status 
Current plan status 
 
Priority 
Calculated/assigned priority 
 
Resources 
Relevant resources count/data 
 
Action 
[ View Plan → ]

## SOURCE PAGE 259

Do not hard-code the reference's sample values. 
 
14. CONNECTION WITH SKILL GAP ANALYSIS 
The Preparation Plan must integrate with the Skill Gap Analysis workflow. 
The Skill Gap page contains: 
Generate Preparation Plan 
When the student uses that functionality: 
Skill Gap Analysis 
        ↓ 
Student selects/configures required inputs 
        ↓ 
Generate Preparation Plan 
        ↓ 
Preparation Plan generated 
        ↓ 
Plan stored 
        ↓ 
Preparation Plan page displays the generated plan 
The generated plan must appear on the Preparation Plan page. 
It should not be displayed as the final plan inside the Skill Gap Analysis page. 
 
15. GENERATE PREPARATION PLAN FROM THIS PAGE 
The Preparation Plan page itself also contains: 
Generate Preparation Plan → 
This must remain functional. 
If no preparation plan has previously been generated: 
Preparation Plan Page 
        ↓ 
Click Generate Preparation Plan 
        ↓ 
Generate plan

## SOURCE PAGE 260

↓ 
Store plan 
        ↓ 
Display plan on this page 
Therefore, the student does not need to generate a plan from Skill Gap Analysis first. 
 
16. REGENERATING A PLAN 
If the student changes relevant inputs, such as: 
Target Company 
Target Role 
Academic Year 
and clicks: 
Generate Preparation Plan 
a new preparation plan must be generated based on the updated information. 
Existing Configuration 
        ↓ 
Student changes information 
        ↓ 
Generate Preparation Plan 
        ↓ 
New plan generated 
        ↓ 
New plan stored 
        ↓ 
Preparation Plan page updated 
The displayed plan must correspond to the student's latest generated plan. 
 
17. PLAN PERSISTENCE 
Generated preparation plans must be stored as application data associated with the student. 
The page must retrieve the stored plan rather than generating arbitrary static content every time the 
page loads.

## SOURCE PAGE 261

Student 
   ↓ 
Preparation Plan Data 
   ↓ 
Database / Application Storage 
   ↓ 
Preparation Plan Page 
If a plan already exists, the page should display the stored plan. 
If the student generates a new plan, the displayed plan must update to the newly generated plan 
according to the application's plan/version handling. 
 
18. VIEW PLAN ACTION 
Each preparation-plan row contains: 
View Plan → 
The action must open the corresponding plan details for that specific item. 
The details must correspond to the selected student's actual preparation-plan entry. 
 
19. EXPORT PLAN 
The reference contains: 
Export Plan ↓ 
The implementation must preserve this control and its position. 
The exported content must represent the student's currently displayed preparation plan rather than 
static reference data. 
 
20. DYNAMIC DATA REQUIREMENT 
The page must be completely data-driven. 
Examples of information that must not be hard-coded: 
Student name 
Target company 
Target role 
Academic year 
Readiness percentage

## SOURCE PAGE 262

Goals 
AI recommendations 
Skill levels 
Target levels 
Plan dates 
Plan status 
Priority 
Resources 
Preparation-plan entries 
All such information must be derived from the student's actual data and generated plan. 
 
21. GLOBAL DROPDOWN REQUIREMENT 
All dropdowns on this page must follow the global LOOP-MIND dropdown requirement. 
For example: 
Target Company 
Target Role 
Academic Year 
must have complete, context-appropriate datasets. 
The user will not provide these datasets separately. 
The implementation must provide them. 
Where appropriate: 
Dropdown 
   ↓ 
Search 
   ↓ 
Relevant dataset 
   ↓ 
Selection 
No dropdown should remain empty or placeholder-only. 
 
22. FOOTER

## SOURCE PAGE 263

The footer must be exactly the same global LOOP-MIND footer used throughout the Student 
Portal. 
It must not be redesigned specifically for this page. 
The footer must maintain: 
• 
Same structure 
• 
Same content 
• 
Same placement 
• 
Same styling 
• 
Same spacing 
• 
Same interaction behavior 
as defined for the Landing Page/global Student Portal footer. 
 
23. RESPONSIVE BEHAVIOR 
The implementation must preserve the reference page's structural hierarchy when adapting to 
different screen sizes. 
Responsive adaptation must not change the intended component hierarchy or functionality. 
The desktop reference remains the authoritative layout reference for this page. 
 
24. NON-NEGOTIABLE REFERENCE RULE 
Layout 
The uploaded Preparation Plan image is the authoritative visual reference for this page. 
Therefore: 
• 
Do not redesign the page. 
• 
Do not rearrange cards. 
• 
Do not add unrelated sections. 
• 
Do not remove reference sections. 
• 
Do not move the navigation. 
• 
Do not move the Current Readiness card. 
• 
Do not move Year-Wise Focus. 
• 
Do not move Your Goals. 
• 
Do not move AI Recommendations. 
• 
Do not move Detailed Preparation Plan.

## SOURCE PAGE 264

• 
Do not change the footer structure. 
• 
Do not substitute a different page layout. 
Data 
The layout is fixed; the content is dynamic. 
The reference's sample values are visual examples only and must not become hard-coded 
application data. 
REFERENCE IMAGE 
       │ 
       ├── Layout → FIXED 
       ├── Structure → FIXED 
       ├── Placement → FIXED 
       ├── Navigation → FIXED 
       └── Footer → FIXED 
 
STUDENT DATA 
       │ 
       ├── Company → DYNAMIC 
       ├── Role → DYNAMIC 
       ├── Academic Year → DYNAMIC 
       ├── Readiness → DYNAMIC 
       ├── Goals → DYNAMIC 
       ├── Recommendations → DYNAMIC 
       └── Preparation Plan → DYNAMIC 
This gives the implementation the required combination: the uploaded reference layout is 
preserved, while every student-specific value and generated preparation plan is data-driven. 
LOOP-MIND — Student Portal 
Jobs Page — Software Design Specification (SDD) 
Reference: The uploaded Jobs page image is the exact visual layout reference. 
The implementation must preserve the same page structure, element placement, hierarchy, spacing, 
proportions, and overall visual composition. 
Do not redesign, rearrange, add unrelated sections, or change the layout. 
All job/profile/application data must be dynamic and database-driven.

## SOURCE PAGE 265

1. Page Identity 
Page Name: Discover Opportunities 
Portal: Student Portal 
Route: /jobs 
Purpose 
The Jobs page allows a student to: 
• 
View available job opportunities. 
• 
Search for jobs. 
• 
Sort jobs. 
• 
Filter jobs. 
• 
Apply to a job. 
• 
Save/bookmark a job. 
• 
Track basic application counts through the page summary cards. 
• 
Trigger profile-completeness validation before applying. 
• 
Complete missing required profile information directly through the displayed validation card 
when necessary. 
• 
Submit the job application once all required information is available. 
 
2. Navigation Entry 
The Jobs page must open when the student clicks: 
Jobs 
from the Student Portal top navigation. 
The top navigation must retain the same structure shown in the reference image: 
LOOP-MIND                         Dashboard   Skill Gap   Preparation Plan   Jobs   My Progress 

## UPDATE — Student Portal navigation moved to the right (UPDATE SDD "Right-Side Navigation Requirement")

The Dashboard / Skill Gap / Preparation Plan / Jobs / My Profile / Logout items now render
flush to the right edge of the navbar (opposite the LOOP-MIND brand) on every Student Portal
page, via a shared `<StudentNavbar />` component. Same items, same order, same styling,
spacing, and interaction behavior — only the horizontal position within the navbar changed.
The Recruiter Portal's own navigation is unaffected.

For the current implementation: 
• 
Jobs is the active navigation item. 
• 
The active state must use the same visual treatment as the reference. 
• 
Other navigation items retain their existing functionality. 
• 
My Progress will subsequently be renamed to My Profile, as specified by the project 
requirement. 
 
3. Exact Reference Layout

## SOURCE PAGE 266

The page must follow this structure: 
┌──────────────────────────────────────────────────────────────────────────────┐ 
│ LOOP-MIND                                  Dashboard Skill Gap Preparation   │ 
│                                             Plan    Jobs   My Progress       │ 
├──────────────────────────────────────────────────────────────────────────────┤ 
│                                                                              │ 
│  Discover Opportunities                         ┌──────────────────────────┐ │ 
│  Apply to real jobs, track your applications,   │  Quote / LOOP-MIND       │ │ 
│  and get closer to your dream career.          └──────────────────────────┘ │ 
│                                                                              │ 
│ ┌────────────┐ ┌────────────┐ ┌────────────┐ ┌────────────┐                 │ 
│ │ Total Jobs │ │  Applied   │ │Under Review│ │ Shortlisted│                 │ 
│ │    120     │ │     8      │ │     5      │ │     2      │                 │ 
│ └────────────┘ └────────────┘ └────────────┘ └────────────┘                 │ 
│                                                                              │ 
│ ┌──────────────────────────────────────────────┐ ┌────────────────────────┐ │ 
│ │ Search jobs by company, role, skills...      │ │ Filters                │ │ 
│ │                                  [Search]    │ │ Company                │ │ 
│ └──────────────────────────────────────────────┘ │ Job Role               │ │ 
│ Sort by [Posted Date (Newest)]                  │ Location               │ │ 
│                                                 │ Job Type               │ │ 
│ ┌──────────────────────────────────────────────┐ │ Experience Level       │ │ 
│ │ Job Card                                    │ │                        │ │ 
│ │ Company / Job / Location / Type / Experience│ │                        │ │ 
│ │ Description                                 │ │                        │ │ 
│ │ Skills                                      │ │                        │ │ 
│ │                         [Apply Now] [Save]  │ │                        │ │ 
│ └──────────────────────────────────────────────┘ └────────────────────────┘ │ 
│                                                                              │ 
│ ┌──────────────────────────────────────────────┐                             │ 
│ │ Job Card                                    │                             │

## SOURCE PAGE 267

│ └──────────────────────────────────────────────┘                             │ 
│                                                                              │ 
│ ┌──────────────────────────────────────────────┐                             │ 
│ │ Job Card                                    │                             │ 
│ └──────────────────────────────────────────────┘                             │ 
│                                                                              │ 
├──────────────────────────────────────────────────────────────────────────────┤ 
│ Terms of Use     Privacy Policy     Membership Plans     Help               │ 
│                         LOOP-MIND ©                                          │ 
└──────────────────────────────────────────────────────────────────────────────┘ 
The above is the structural representation. The actual implementation must visually follow the 
uploaded image rather than this ASCII drawing. 
 
4. Page Header 
The left side of the header contains: 
Heading 
Discover Opportunities 
Description 
Apply to real jobs, track your applications, and get closer to your dream career. 
These texts must remain in the same positions as the reference layout. 
 
5. Quote Card 
The upper-right area contains the small quote card. 
Reference content: 
“Opportunities don’t just happen, you prepare for them.” 
 
— LOOP-MIND 
The quote card must: 
• 
Remain in the same position. 
• 
Maintain the same approximate dimensions. 
• 
Use the same visual hierarchy.

## SOURCE PAGE 268

• 
Not interfere with the job search area. 
The quote text may be treated as static UI content unless a separate dynamic quote system is 
explicitly defined later. 
 
6. Job Summary Cards 
Immediately below the header, the page contains four summary cards. 
Card 1 — Total Jobs 
Total Jobs 
120 
Card 2 — Applied 
Applied 
8 
Card 3 — Under Review 
Under Review 
5 
Card 4 — Shortlisted 
Shortlisted 
2 
Dynamic Requirement 
The numbers shown in these cards must not be hard-coded. 
They must be calculated from the logged-in student's database/application data and the currently 
available jobs. 
Conceptually: 
Total Jobs 
→ Count of available job records 
 
Applied 
→ Count of jobs applied to by the logged-in student 
 
Under Review 
→ Count of the student's applications currently under review

## SOURCE PAGE 269

Shortlisted 
→ Count of the student's applications currently shortlisted 
The exact displayed value therefore changes according to the student's actual data. 
 
7. Job Search 
The main content area contains the search bar exactly as shown in the reference. 
Search Placeholder 
Search jobs by company, role, skills, or keywords... 
The student enters a search query. 
Search must operate against available job data. 
The search should support the information represented by the placeholder: 
• 
Company 
• 
Job role 
• 
Skills 
• 
Keywords 
Search Behavior 
Example: 
Student enters: 
Software Engineer 
The job list dynamically displays matching jobs. 
Another example: 
Student enters: 
Python 
Jobs containing the relevant skill/keyword are displayed. 
Important 
The search must query/filter actual job records. 
It must not simply search a hard-coded frontend list. 
 
8. Search Button 
The reference contains a: 
Search

## SOURCE PAGE 270

button beside the search field. 
The button must execute the search using the entered search query. 
The page should retain the same visual placement as the reference. 
 
9. Sorting 
Beside the search area: 
Sort by 
[ Posted Date (Newest) ▼ ] 
The sorting control must be dynamic. 
The selected sorting option determines the order of the job results. 
The reference currently shows: 
Posted Date (Newest) 
The implementation must preserve this visual structure. 
Any additional sorting options should only be introduced if they are defined by the project 
requirements; do not invent unrelated functionality. 
 
10. Filters Panel 
The right side of the page contains the filters panel. 
The filter panel must remain in the same location and structure as the reference. 
The reference contains: 
Filters 
 
Company 
[ Search company... ] 
 
☐ Google 
☐ Microsoft 
☐ Amazon 
☐ Adobe 
☐ Flipkart 
Show more

## SOURCE PAGE 271

Job Role 
 
☐ Software Engineer 
☐ SDE Intern 
☐ Frontend Developer 
☐ Backend Developer 
☐ Data Scientist 
Show more 
 
Location 
 
☐ Bangalore 
☐ Hyderabad 
☐ Noida 
☐ Pune 
☐ Remote 
 
Job Type 
 
☐ Full-time 
☐ Internship 
☐ Part-time 
 
Experience Level 
 
☐ Entry Level 
☐ Mid Level 
☐ Senior Level

## SOURCE PAGE 272

11. Dynamic Filter Data 
All filter options must come from the available job dataset. 
They must not be hard-coded into the UI. 
For example: 
Company 
    ↓ 
Companies represented in job records 
 
Job Role 
    ↓ 
Roles represented in job records 
 
Location 
    ↓ 
Locations represented in job records 
 
Job Type 
    ↓ 
Job types represented in job records 
 
Experience Level 
    ↓ 
Experience levels represented in job records 
Therefore, if the database contains different companies or roles, the filter values automatically 
change. 
 
12. Company Search Inside Filters 
The Company filter contains: 
Search company... 
This must allow the student to search/filter the available company options. 
It must operate against the dynamic company dataset.

## SOURCE PAGE 273

13. Show More 
Where the reference shows: 
Show more 
the control must reveal additional available values for that particular filter category. 
The values displayed must come from the database/job dataset. 
No fake/static company list should be used. 
 
14. Clear All 
The filter area contains: 
Clear All 
When clicked: 
• 
All currently selected filters are removed. 
• 
The default job listing is restored. 
• 
The search query should also be cleared only if it is part of the active filter state; otherwise, 
search behavior remains separate. 
The implementation must preserve the reference placement. 
 
15. Job Listing Area 
The main left section contains the job cards. 
Each card follows the same structure as the reference. 
Example visual structure: 
┌──────────────────────────────────────────────────────────────────────┐ 
│ [Company Logo]  Software Engineer                    Posted 2 days ago│ 
│                 Google                                 [Open]         │ 
│                                                                      │ 
│                   Bangalore, India   ● Full-time   ● On-site        │ 
│                 ● Entry Level                                          │ 
│                                                                      │ 
│                 Job description...                         [Apply Now]│ 
│                                                                      │

## SOURCE PAGE 274

│                 [Data Structures] [Algorithms] [System Design]       │ 
│                 [Python] [Distributed Systems] [+3 more]             │ 
│                                                                      │ 
│                                                        [Save]         │ 
└──────────────────────────────────────────────────────────────────────┘ 
This structure must be retained for every job card. 
 
16. Job Card Data 
Each job card must display data from the corresponding job record. 
The visible information includes: 
Company Logo 
Retrieved from the job/company record. 
Job Title 
Example: 
Software Engineer 
Must come from the job record. 
Company Name 
Example: 
Google 
Must come from the job record. 
Location 
Example: 
Bangalore, India 
Must come from the job record. 
Job Type 
Example: 
Full-time 
Must come from the job record. 
Work Mode 
Example: 
On-site

## SOURCE PAGE 275

Must come from the job record. 
Experience Level 
Example: 
Entry Level 
Must come from the job record. 
Posted Time 
Example: 
Posted 2 days ago 
Must be calculated/displayed from the job's actual posting date. 
Job Status 
Example: 
Open 
Must reflect the actual job/application availability status. 
 
17. Job Description 
Each job card contains a short job description. 
The description must come from the corresponding job record. 
Do not generate a generic description merely to fill the card. 
 
18. Job Skills 
The card displays skill tags such as: 
Data Structures 
Algorithms 
System Design 
Python 
Distributed Systems 
+3 more 
These must come from the job's actual required/relevant skills. 
If the number of skills exceeds the visible card capacity: 
+3 more 
or the corresponding calculated count should be displayed.

## SOURCE PAGE 276

The number must be dynamically calculated. 
 
19. Apply Now Button 
Every available job card contains: 
Apply Now → 
The student can click this button to apply for that specific job. 
The clicked job ID must be retained throughout the application-validation process. 
 
20. Apply Flow 
When the student clicks: 
Apply Now 
the system must first validate the student's profile against the required information needed for the 
application. 
Flow 
Apply Now 
    ↓ 
Check Student Profile 
    ↓ 
Are all required application requirements available? 
    │ 
    ├── YES 
    │     ↓ 
    │  Submit Job Application 
    │ 
    └── NO 
          ↓ 
    Show Missing Information Card 
 
21. Required vs Optional Information 
The system must distinguish between: 
Required

## SOURCE PAGE 277

and: 
Optional 
profile information. 
Optional information must not prevent the student from applying. 
For example, the user explicitly identified URLs such as project-related URLs as potentially optional. 
Therefore: 
Optional information missing 
        ↓ 
Application can continue 
Required information missing: 
Required information missing 
        ↓ 
Application cannot be submitted yet 
 
22. Resume Validation 
The resume is explicitly treated as required for the application flow. 
If the student has no required resume available: 
Apply Now 
    ↓ 
Resume missing 
    ↓ 
Show missing-information card 
The card must clearly tell the student that the resume is required and needs to be 
uploaded/completed before the application can be submitted. 
 
23. Other Required Profile Information 
The same validation mechanism applies to other required profile information. 
The user specifically identified examples such as: 
• 
Required project information. 
• 
Required certification information. 
• 
Resume.

## SOURCE PAGE 278

If any required item is missing, the student must be informed before application submission. 
The validation must use the student's actual profile data. 
 
24. Missing Information Card 
When required information is missing, a card/modal must open: 
Position 
Center of the page. 
It must overlay the Jobs page while keeping the Jobs page as the underlying page. 
It must follow the same centered-card/modal interaction pattern defined for the Student Portal. 
 
25. Missing Information Card Content 
The card must clearly identify: 
What is missing 
Why it is required 
What the student needs to complete/upload 
For example, if the resume is missing: 
Required Information Missing 
 
Your resume is required to apply for this job. 
 
Please upload your resume to continue. 
 
[Upload Resume] 
If a required project is missing, the corresponding missing requirement must be displayed instead. 
Do not show missing items that are actually present in the student's database profile. 
 
26. Completion Inside the Card 
The student must be able to complete the missing requirement from the displayed card/flow. 
For example: 
Resume Missing 
       ↓

## SOURCE PAGE 279

Upload Resume 
       ↓ 
Resume stored/updated 
       ↓ 
Validation runs again 
       ↓ 
All required information available 
       ↓ 
Submit application 
The system must not require the student to manually restart the entire application process after 
completing the missing requirement. 
 
27. Application Submission 
Once all required information is available: 
Apply Now 
    ↓ 
Profile Validation 
    ↓ 
All Required Information Available 
    ↓ 
Create Job Application 
    ↓ 
Application Submitted 
The application must be associated with: 
• 
Logged-in student. 
• 
Selected job. 
• 
Application timestamp. 
• 
Current application status. 
The exact later recruiter workflow/status progression will be defined when the Recruiter Portal 
specification is provided. 
 
28. Recruiter-Side Continuation

## SOURCE PAGE 280

The submitted application becomes part of the recruitment workflow that will later be handled 
through the Recruiter Portal. 
The user-defined future workflow includes recruiter-side processing such as: 
Student applies 
      ↓ 
Recruiter receives candidate 
      ↓ 
ATS / Resume Parser / related processing 
      ↓ 
Cross-check candidate information 
      ↓ 
Shortlist / Reject / Hold 
      ↓ 
Recruiter decision / further recruitment workflow 
Recruiter Portal UI and detailed workflow are intentionally not specified here, because those 
details will be provided separately. 
 
29. Save / Bookmark Functionality 
Each job card contains: 
Save 
The purpose is to allow the student to bookmark/save a particular job. 
When clicked 
Save 
    ↓ 
Job saved to student's saved/bookmarked jobs 
The saved state must be persisted against the logged-in student's account. 
It must not be temporary frontend-only state. 
 
30. Saved Job State 
A saved job must remain associated with the student after: 
• 
Page refresh. 
• 
Logout/login.

## SOURCE PAGE 281

• 
Returning to the Jobs page. 
The UI should visually indicate that the job has already been saved. 
The Save control should therefore behave as a persistent bookmark/toggle state. 
 
31. Dynamic Job Data 
The job list must be entirely database-driven. 
The frontend must not contain a permanently hard-coded list such as: 
Google 
Microsoft 
Amazon 
Adobe 
Flipkart 
Those are only examples represented in the reference image. 
Actual jobs must come from the project's job dataset/database. 
 
32. Dynamic Student Data 
Anything related to the logged-in student must be based on that student's actual database/profile 
information. 
Examples: 
Applied count 
Under Review count 
Shortlisted count 
Saved jobs 
Application status 
Profile requirements 
Resume availability 
Project availability 
Certification availability 
No student-specific value should be arbitrarily hard-coded. 
 
33. Job Search + Filter Interaction

## SOURCE PAGE 282

Search and filters should work together. 
Example: 
Search: 
Python 
 
+ 
Company: 
Google 
 
+ 
Job Type: 
Full-time 
The displayed result should contain only jobs satisfying the active conditions. 
The result count/list should update dynamically. 
 
34. No Hard-Coded Job Counts 
Values such as: 
120 
8 
5 
2 
shown in the uploaded image are reference/example values only. 
They must not be permanently coded. 
The actual student's page may display: 
Total Jobs     46 
Applied        3 
Under Review   1 
Shortlisted    0 
or any other values based on actual database records. 
 
35. Footer

## SOURCE PAGE 283

The footer is a global Student Portal footer. 
It must be exactly the same footer used throughout the Student Portal and must not be redesigned 
independently for the Jobs page. 
Reference footer: 
Terms of Use     Privacy Policy     Membership Plans     Help 
 
                         LOOP-MIND © 
Strict Requirement 
The footer must remain: 
• 
Same structure. 
• 
Same placement. 
• 
Same typography. 
• 
Same spacing. 
• 
Same visual treatment. 
• 
Same links/text. 
• 
Same behavior. 
This footer must be reused across the Student Portal pages. 
 
36. Footer Interaction 
If a footer item opens a card/modal according to the existing Student Portal behavior, the 
card/modal must: 
Open at the center of the page 
and follow the same existing modal/card interaction pattern. 
The Jobs page must not create a different footer interaction. 
 
37. Page Layout Preservation Rule 
The uploaded image is the layout reference. 
The implementation must preserve: 
Header 
Same placement. 
Navigation 
Same placement.

## SOURCE PAGE 284

Page title 
Same placement. 
Quote card 
Same placement. 
Summary cards 
Same four-card horizontal arrangement. 
Search area 
Same placement. 
Sort control 
Same placement. 
Filters 
Same right-side panel. 
Job list 
Same left-side content area. 
Job cards 
Same card structure. 
Apply Now 
Same placement within each card. 
Save 
Same placement within each card. 
Footer 
Same bottom structure. 
 
38. Responsive Behavior 
The page should remain structurally equivalent when adapting to different screen sizes. 
Responsive behavior must not change the intended component hierarchy or functionality. 
The desktop layout shown in the uploaded image is the primary visual reference. 
 
39. Data Flow 
Student Login 
      ↓

## SOURCE PAGE 285

Authenticated Student 
      ↓ 
Load Student Profile 
      ↓ 
Load Available Jobs 
      ↓ 
Calculate Application Statistics 
      ↓ 
Render Jobs Page 
      ↓ 
Student searches / filters 
      ↓ 
Dynamic Job Results 
      ↓ 
Student clicks Apply Now 
      ↓ 
Validate Required Profile Information 
      │ 
      ├───────────────┐ 
      │               │ 
   Complete         Missing 
      │               │ 
      ↓               ↓ 
Submit          Center Card 
Application          │ 
      │          Complete Missing 
      │          Information 
      │               │ 
      │          Revalidate 
      │               │ 
      └───────→ Submit Application

## SOURCE PAGE 286

40. Save Data Flow 
Student 
   ↓ 
Clicks Save 
   ↓ 
Selected Job ID 
   ↓ 
Create/Update Saved Job Record 
   ↓ 
Persist to Database 
   ↓ 
Update Saved State in UI 
 
41. Search Data Flow 
Student enters search 
        ↓ 
Search Query 
        ↓ 
Job Dataset 
        ↓ 
Match: 
Company 
Role 
Skills 
Keywords 
        ↓ 
Filtered Job Results 
        ↓ 
Render Job Cards

## SOURCE PAGE 287

42. Filter Data Flow 
Job Dataset 
     ↓ 
Generate available filter values 
     ↓ 
Company 
Job Role 
Location 
Job Type 
Experience Level 
     ↓ 
Student selects filters 
     ↓ 
Apply selected filters 
     ↓ 
Render matching jobs 
 
43. Application Validation Data Flow 
Selected Job 
     ↓ 
Required Application Requirements 
     ↓ 
Logged-in Student Profile 
     ↓ 
Compare Required vs Available 
     ↓ 
┌──────────────────────────────┐ 
│ All requirements available?  │ 
└──────────────┬───────────────┘ 
               │ 
        ┌──────┴──────┐

## SOURCE PAGE 288

│             │ 
       YES            NO 
        │             │ 
        ↓             ↓ 
 Submit Application  Show Missing 
                    Information Card 
                         ↓ 
                   Student completes 
                         ↓ 
                     Revalidate 
                         ↓ 
                  Submit Application 
 
44. Important Implementation Rules 
Rule 1 — No hard-coded student information 
Student-specific information must come from the authenticated student's database records. 
Rule 2 — No hard-coded job listing 
Jobs must come from the job dataset/database. 
Rule 3 — No hard-coded filter values 
Filter options must be generated from the available job data. 
Rule 4 — No hard-coded statistics 
Summary numbers must be calculated from actual records. 
Rule 5 — Optional fields do not block application 
Missing optional information must not prevent applying. 
Rule 6 — Required fields block application 
Missing required information must trigger the centered missing-information card. 
Rule 7 — Resume is required 
A missing required resume must prevent submission until completed. 
Rule 8 — Application must belong to the logged-in student 
The application must be associated with the authenticated student and selected job. 
Rule 9 — Save must persist

## SOURCE PAGE 289

Saved/bookmarked jobs must persist in the database. 
Rule 10 — Recruiter workflow is separate 
The detailed Recruiter Portal workflow will be specified separately and must not be invented here. 
 
45. Reference Layout Specification 
Reference Page: Uploaded Jobs page image. 
Reference layout must be treated as the source of truth for visual structure. 
TOP NAVIGATION 
──────────────────────────────────────────────────────── 
 
PAGE HEADER 
├── Discover Opportunities 
├── Description 
└── Quote Card 
 
SUMMARY 
├── Total Jobs 
├── Applied 
├── Under Review 
└── Shortlisted 
 
MAIN CONTENT 
├── LEFT / MAIN 
│   ├── Search Bar 
│   ├── Search Button 
│   ├── Sort 
│   └── Job Cards 
│       ├── Company Logo 
│       ├── Job Title 
│       ├── Company 
│       ├── Location

## SOURCE PAGE 290

│       ├── Job Type 
│       ├── Work Mode 
│       ├── Experience Level 
│       ├── Posted Time 
│       ├── Job Status 
│       ├── Description 
│       ├── Skill Tags 
│       ├── Apply Now 
│       └── Save 
│ 
└── RIGHT 
    └── Filters 
        ├── Company 
        ├── Job Role 
        ├── Location 
        ├── Job Type 
        └── Experience Level 
 
FOOTER 
├── Terms of Use 
├── Privacy Policy 
├── Membership Plans 
├── Help 
└── LOOP-MIND © 
 
46. Final UI/UX Constraint 
Do not interpret the uploaded image as merely an inspiration. 
For this page, it is the reference layout. 
The implementation should reproduce the same: 
• 
Overall page composition 
• 
Header position

## SOURCE PAGE 291

• 
Navigation position 
• 
Card arrangement 
• 
Card proportions 
• 
Search placement 
• 
Filter placement 
• 
Job-card placement 
• 
Button placement 
• 
Footer placement 
• 
Visual hierarchy 
while making the data and behavior fully dynamic. 
In short: 
Same layout and structure as the reference. Dynamic data and functionality underneath it. No 
unnecessary redesign. No invented sections. No hard-coded student/job data. 
LOOP-MIND — STUDENT PORTAL 
MY PROFILE PAGE — SDD + REFERENCE PAGE LAYOUT 
Reference: The uploaded My Progress screenshot is the exact visual/layout reference. 
Required change: The page/navigation name “My Progress” → “My Profile”. 
Apart from this explicitly requested name change and the functional behavior described below, do 
not change the reference layout, placement, buttons, sections, or visual structure. 
 
1. PAGE IDENTITY 
Page Name 
My Profile 
Previous Name 
My Progress 
Route / Navigation 
The existing My Progress navigation item is renamed to: 
My Profile 
This change must be applied consistently across the Student Portal navigation: 
Dashboard | Skill Gap | Preparation Plan | Jobs | My Profile 
Clicking My Profile opens this page.

## SOURCE PAGE 292

2. EXACT REFERENCE PAGE LAYOUT 
The following structure must be preserved from the uploaded reference image. 
┌──────────────────────────────────────────────────────────────────────────────┐ 
│ LOOP-MIND                                      Dashboard  Skill Gap           │ 
│                                                   Preparation Plan  Jobs     │ 
│                                                               My Profile     │ 
├───────────────┬──────────────────────────────────────────────────────────────┤ 
│               │                                                              │ 
│  Overview     │  My Profile                                                  │ 
│               │  Manage your profile, track your progress, and keep your     │ 
│  Basic        │  information up to date.                                     │ 
│  Information  │                                                              │ 
│               │                         ┌─────────────────────────────────┐  │ 
│  Academics    │                         │ “A better you today, a brighter │  │ 
│               │                         │ tomorrow.”                      │  │ 
│  Skills       │                         │             — LOOP-MIND          │  │ 
│               │                         └─────────────────────────────────┘  │ 
│  Coding       │                                                              │ 
│  Experience   │  ┌──────────────────────────────┐ ┌──────────────┐           │ 
│               │  │ Student Profile              │ │ Profile      │           │ 
│  Projects     │  │                              │ │ Completion   │           │ 
│               │  │ Profile Photo                │ │              │           │ 
│  Certifications│ │ Student Name                │ │     XX%      │           │ 
│               │  │ Degree / Course             │ │              │           │ 
│  Career &     │  │ University                  │ │ View Missing │           │ 
│  Placement    │  │ Semester / Academic details │ │ Fields       │           │ 
│               │  │ Location                    │ │              │           │ 
│  Learning &   │  └──────────────────────────────┘ └──────────────┘           │ 
│  Preparation  │                                                              │ 
│               │  ┌────────────────────────────────────────────────────────┐ │ 
│  Interview &  │  │ Quick Actions                                           │ │

## SOURCE PAGE 293

│  Assessment   │  │ View Public Profile                                    │ │ 
│               │  │ Download Resume                                         │ │ 
│  Professional │  │ View Placement Readiness                                │ │ 
│  Links &      │  └────────────────────────────────────────────────────────┘ │ 
│  Resume       │                                                              │ 
│               │  ┌────────────────────────────────────────────────────────┐ │ 
│  Recruitment  │  │ Skills Added │ Projects │ Certifications │ Job          │ │ 
│  History      │  │             │          │                │ Applications  │ │ 
│               │  └────────────────────────────────────────────────────────┘ │ 
│  Consent &    │                                                              │ 
│  Knowledge    │  ┌────────────────────────────────────────────────────────┐ │ 
│  Sharing      │  │ Basic Information                               Edit    │ │ 
│               │  │                                                        │ │ 
│               │  │ Full Name | Date of Birth | Gender | Email | Mobile    │ │ 
│               │  │                                                        │ │ 
│               │  │ Profile Photo | Country | State | City | Postal Code  │ │ 
│               │  │ Current Location | Permanent Location                  │ │ 
│               │  └────────────────────────────────────────────────────────┘ │ 
│               │                                                              │ 
│               │  ┌────────────────────────────────────────────────────────┐ │ 
│               │  │ Academic Information                           Edit     │ │ 
│               │  │                                                        │ │ 
│               │  │ College/University | College Location | Degree        │ │ 
│               │  │ Branch/Department | Specialization | Academic Year    │ │ 
│               │  │ Current Year | Current Semester | Admission Year      │ │ 
│               │  │ Expected Graduation Year                                │ │ 
│               │  └────────────────────────────────────────────────────────┘ │ 
│               │                                                              │ 
│               │  ┌────────────────────────────────────────────────────────┐ │ 
│               │  │ Academic Performance                          Edit      │ │ 
│               │  │                                                        │ │

## SOURCE PAGE 294

│               │  │ Current CGPA | CGPA Scale | Semester-wise SGPA        │ │ 
│               │  │ Academic Percentage | 10th Score | 12th/Diploma Score │ │ 
│               │  │ Backlogs/Active Backlogs                               │ │ 
│               │  └────────────────────────────────────────────────────────┘ │ 
│               │                                                              │ 
│               │  ┌────────────────────────────────────────────────────────┐ │ 
│               │  │ Skills                              Edit | + Add Skill │ │ 
│               │  │                                                        │ │ 
│               │  │ Skill Name | Skill Category | Proficiency Level        │ │ 
│               │  │ Learning Status | Experience | Evidence Supporting     │ │ 
│               │  │ Skill | Action                                           │ │ 
│               │  └────────────────────────────────────────────────────────┘ │ 
│               │                                                              │ 
├───────────────┴──────────────────────────────────────────────────────────────┤ 
│ Delete Profile │                                      Cancel  Save Changes  │ 
│                                                   No changes made yet        │ 
├──────────────────────────────────────────────────────────────────────────────┤ 
│ Terms of Use   Privacy Policy   Membership Plans   Help                       │ 
│                              LOOP-MIND ©                                      │ 
└──────────────────────────────────────────────────────────────────────────────┘ 
Important layout rule 
The ASCII structure above represents the same structural arrangement as the uploaded reference: 
• 
Left sidebar 
• 
Main profile content 
• 
Top page heading 
• 
Quote card 
• 
Profile summary card 
• 
Profile completion card 
• 
Quick Actions card 
• 
Statistics cards 
• 
Basic Information section

## SOURCE PAGE 295

• 
Academic Information section 
• 
Academic Performance section 
• 
Skills section 
• 
Bottom action area 
• 
Footer 
Do not rearrange these elements. 
 
3. TOP NAVIGATION 
The top navigation remains: 
Dashboard 
Skill Gap 
Preparation Plan 
Jobs 
My Profile 
Explicit change 
My Progress 
must become: 
My Profile 
This applies throughout the Student Portal. 
Navigation behavior 
Clicking: 
My Profile 
opens the My Profile page. 
The active navigation styling remains exactly like the reference screenshot. 
 
4. LEFT PROFILE NAVIGATION 
The left-side navigation remains in the same order and position as the reference: 
Overview 
Basic Information 
Academics 
Skills

## SOURCE PAGE 296

Coding Experience 
Projects 
Certifications 
Career & Placement 
Learning & Preparation 
Interview & Assessment 
Professional Links & Resume 
Recruitment History 
Consent & Knowledge Sharing 
No additional sidebar item should be introduced unless explicitly requested. 
 
5. PROFILE DATA SOURCE 
The page must not use hardcoded student information. 
Every displayed value must be retrieved from the authenticated student's stored profile data. 
Data flow 
Authenticated Student 
        ↓ 
Student/User ID 
        ↓ 
Student Profile Data 
        ↓ 
Relevant Profile Category 
        ↓ 
My Profile UI 
For example: 
Student Name 
        ↓ 
Authenticated student's stored profile 
 
Skills 
        ↓

## SOURCE PAGE 297

Authenticated student's stored Skills records 
 
Projects 
        ↓ 
Authenticated student's stored Project records 
 
Certifications 
        ↓ 
Authenticated student's stored Certification records 
The page must display the current student's actual information. 
 
6. PROFILE SUMMARY 
The profile summary area must follow the reference layout. 
It contains: 
• 
Profile Photo 
• 
Student Name 
• 
Degree / Course 
• 
University 
• 
Semester / academic information 
• 
Location information 
The values are populated dynamically from the student's stored profile. 
Profile Photo 
The student's stored profile photo is displayed. 
The existing: 
Change Photo 
interaction remains available where shown in the reference. 
 
7. PROFILE COMPLETION 
The Profile Completion card remains in the same location and visual structure as the reference. 
The percentage must be calculated dynamically from the student's profile completion state. 
It must not be a hardcoded percentage.

## SOURCE PAGE 298

Example: 
Profile Completion 
92% 
is only an example from the reference image. 
For another student, the percentage must change according to that student's actual 
completed/required profile information. 
The: 
View Missing Fields 
button remains available as shown in the reference. 
 
8. QUICK ACTIONS 
The Quick Actions section remains in the same location and structure. 
It contains the actions shown in the reference: 
View Public Profile 
Download Resume 
View Placement Readiness 
These actions must operate using the authenticated student's own data. 
 
9. PROFILE STATISTICS 
The statistics cards remain in the same position and structure as the reference. 
The displayed values must be dynamically calculated from the student's stored records. 
The reference contains: 
Skills Added 
Projects 
Certifications 
Job Applications 
For example: 
Skills Added → count of student's skill records 
Projects → count of student's project records 
Certifications → count of student's certification records 
Job Applications → count of student's job application records

## SOURCE PAGE 299

The numbers must never be hardcoded. 
 
10. BASIC INFORMATION 
The Basic Information section remains in the exact reference position. 
The reference contains: 
Full Name 
Date of Birth 
Gender 
Email Address 
Mobile Number 
Alternate Mobile Number 
 
Profile Photo 
Country 
State 
City 
Postal/ZIP Code 
Current Location 
Permanent Location 
These values must come from the student's stored profile information. 
 
10.1 Edit Restrictions 
Certain identity/account fields must not be editable, as explicitly required. 
Examples given by the user include: 
Name 
Course 
These types of information should remain protected from ordinary profile editing where they 
originate from account/registration data. 
The implementation must follow the actual field-level editability defined by the registration/profile 
specification rather than allowing unrestricted editing. 
 
11. ACADEMIC INFORMATION

## SOURCE PAGE 300

The section remains in the same reference position. 
Fields shown in the reference: 
College/University 
College Location 
Degree 
Branch/Department 
Specialization 
Academic Year 
 
Current Year 
Current Semester 
Admission Year 
Expected Graduation Year 
The information is loaded dynamically from the student's stored academic information. 
Fields that originate from account/registration information and are explicitly non-editable must 
remain non-editable. 
 
12. ACADEMIC PERFORMANCE 
The section remains in the same reference position. 
Fields shown: 
Current CGPA 
CGPA Scale 
Semester-wise SGPA 
Academic Percentage 
10th Score 
12th/Diploma Score 
Backlogs/Active Backlogs 
The values must come from the student's stored academic-performance information. 
No sample/reference values such as: 
5.90 
7.04, 5.58...

## SOURCE PAGE 301

92% 
should be hardcoded. 
Those values in the screenshot are only reference data. 
 
13. SKILLS 
The Skills section remains exactly where it appears in the reference. 
The table structure is: 
Skill Name 
Skill Category 
Proficiency Level 
Learning Status 
Experience 
Evidence Supporting Skill 
Action 
The student's actual skills must be loaded dynamically. 
 
13.1 Add Skill 
The existing: 
+ Add Skill 
button remains. 
The student can add multiple skills. 
Therefore: 
Student 
   ↓ 
Add Skill 
   ↓ 
Skill Record 
   ↓ 
Student's Skills 
   ↓ 
Multiple Skill Records

## SOURCE PAGE 302

must be supported. 
 
13.2 Edit Skill 
Existing skill records can be edited. 
The edit action remains in the table. 
 
13.3 Delete Skill 
The existing delete action remains in the table. 
Deleting a skill must affect the student's stored skill record and consequently update the displayed 
profile data/statistics. 
 
14. PROJECTS 
Projects are part of the student's profile data. 
The student must be able to add multiple project entries. 
The project information follows the previously defined project structure: 
Project Name 
Project Description 
Project Type 
Project Status 
Start Date 
End Date 
 
Technologies Used 
Programming Languages 
Frameworks 
Tools 
Skills Demonstrated 
Student's Role 
Team / Individual 
 
GitHub Repository

## SOURCE PAGE 303

Live Demo 
Project Documentation 
Project Evidence 
The projects displayed on the profile must belong to the authenticated student. 
No project data should be hardcoded. 
 
15. CERTIFICATIONS 
The student can have multiple certification entries. 
Certification information follows the defined structure: 
Certification Name 
Issuing Organization 
Certification Type 
Issue Date 
Expiry Date 
Credential ID 
Credential URL 
Certificate File 
Skills Covered 
The profile must display the authenticated student's stored certification records. 
 
16. CAREER / PLACEMENT 
The profile must use the student's stored Career / Placement information. 
The defined information includes: 
Career Interest 
Target Job Role 
Preferred Job Domain 
Target Company 
Target Role 
Preferred Technology / Skill Area 
Placement Interest 
Internship Interest

## SOURCE PAGE 304

Placement Preferences 
Preferred Job Type 
Preferred Work Location 
Preferred Country 
Preferred State 
Preferred City 
Remote / On-site / Hybrid 
Preferred Industry 
Placement Status 
The data must remain student-specific and dynamic. 
 
17. LEARNING / PREPARATION 
The student's stored Learning / Preparation information must be used. 
Fields include: 
Current Learning Areas 
Skills Currently Learning 
Learning Goals 
Areas They Want to Improve 
Current Preparation Status 
Interview / Assessment Preparation 
Previous Interview Experience 
Previous Assessment Experience 
Technical Interview Experience 
Coding Assessment Experience 
Interview Preparation Status 
Assessment Preparation Status 
Optional fields remain optional. 
 
18. PROFESSIONAL LINKS + RESUME 
The student's stored professional links are displayed. 
GitHub URL

## SOURCE PAGE 305

LinkedIn URL 
Portfolio Website URL 
Coding Profile URL 
Other Professional Profile URL 
Resume 
Upload Resume PDF 
The student's uploaded resume must be associated with that student's profile. 
 
19. RECRUITMENT HISTORY 
The student's recruitment history is stored against their profile. 
The defined information includes: 
Previous Applications 
Companies Applied To 
Roles Applied To 
Recruitment Stage Reached 
Assessment Participation 
Interview Participation 
Selection Outcome 
Rejection Outcome 
Hold Outcome 
This data must be student-specific. 
 
20. CONSENT / KNOWLEDGE SHARING 
The student's stored consent settings must be represented. 
Consent to use relevant information 
Consent for learning/recruitment experience 
Consent for anonymized/aggregated intelligence 
These values must come from the student's actual stored consent records. 
 
21. MULTIPLE-ENTRY SUPPORT 
The following sections must support multiple records where already specified:

## SOURCE PAGE 306

Skills 
Projects 
Certifications 
Adding one record must not overwrite existing records. 
Example: 
Student 
 ├── Skill 1 
 ├── Skill 2 
 ├── Skill 3 
 │ 
 ├── Project 1 
 ├── Project 2 
 │ 
 ├── Certification 1 
 ├── Certification 2 
 └── Certification 3 
 
22. EDIT → SAVE BEHAVIOR 
The Save Changes button is initially inactive when there are no modifications. 
No changes 
      ↓ 
Save Changes = Inactive 
When the student edits or updates an editable field: 
Field changed 
      ↓ 
Unsaved changes detected 
      ↓ 
Save Changes = Active 
When the student clicks: 
Save Changes 
the changes must be persisted to the database.

## SOURCE PAGE 307

After successful saving: 
Updated data 
      ↓ 
Database 
      ↓ 
My Profile refreshed 
If there are no changes: 
Save Changes 
must remain inactive. 
 
23. CANCEL 
The existing Cancel button remains in the same position as the reference. 
Its purpose is to discard the current unsaved edits and return the page to the last saved state. 
No layout change is required. 
 
24. DELETE PROFILE / ACCOUNT 
The bottom-left: 
Delete Profile 
button remains exactly where it appears in the reference. 
When clicked, it must not immediately delete the account. 
A confirmation card/modal must open: 
                    ┌───────────────────────────────┐ 
                    │                               │ 
                    │   Are you sure you want to    │ 
                    │   delete the account?         │ 
                    │                               │ 
                    │          [ Yes ] [ No ]       │ 
                    │                               │ 
                    └───────────────────────────────┘ 
The confirmation card must appear at the: 
CENTER OF THE PAGE

## SOURCE PAGE 308

No 
Clicking: 
No 
closes the confirmation card and does not delete the account. 
Yes 
Clicking: 
Yes 
confirms account deletion. 
The student's account data must then be deleted from the database as required by the account 
deletion functionality. 
 
25. FOOTER 
The Student Portal uses the same footer as the LOOP-MIND landing page. 
The footer must remain consistent across the Student Portal pages. 
Reference footer structure: 
Terms of Use 
Privacy Policy 
Membership Plans 
Help 
 
LOOP-MIND © 
The footer must not be redesigned separately for My Profile. 
 
26. DYNAMIC DATA RULE 
This is a core implementation requirement. 
Do NOT do: 
name = "Chiranthan B S Raj" 
cgpa = 5.90 
skills = 12 
projects = 3 
certifications = 4

## SOURCE PAGE 309

applications = 8 
Instead: 
Authenticated Student 
        ↓ 
Student ID 
        ↓ 
Database 
        ↓ 
Student Profile 
        ↓ 
Dynamic UI 
Every student must see their own data. 
For example: 
Student A → Student A's profile 
Student B → Student B's profile 
Student C → Student C's profile 
 
27. REFERENCE DATA VS ACTUAL DATA 
The values visible in the uploaded screenshot are visual reference examples only. 
For example, the screenshot shows: 
Chiranthan B S Raj 
92% 
12 Skills 
3 Projects 
4 Certifications 
8 Job Applications 
These must not be treated as fixed values. 
The actual page must dynamically display the currently authenticated student's data. 
 
28. STRICT UI IMPLEMENTATION RULE 
The uploaded screenshot is the authoritative reference for the page layout.

## SOURCE PAGE 310

Maintain: 
• 
Same overall page structure 
• 
Same left sidebar placement 
• 
Same top navigation placement 
• 
Same main content arrangement 
• 
Same cards 
• 
Same section ordering 
• 
Same table positioning 
• 
Same action placement 
• 
Same bottom action area 
• 
Same footer placement 
• 
Same visual hierarchy 
• 
Same button locations 
Explicitly allowed change 
My Progress → My Profile 
Explicitly required functional changes 
Dynamic student data 
Multiple Projects 
Multiple Skills 
Multiple Certifications 
Editable allowed fields 
Protected/non-editable fields 
Dynamic Save Changes state 
Save updated data 
Cancel unsaved changes 
Delete Profile confirmation 
Complete account deletion after confirmation 
No other UI/layout change should be introduced beyond these stated requirements. 
 
29. FINAL PAGE FLOW 
Student Login / Account Creation

## SOURCE PAGE 311

↓ 
      Authentication 
             ↓ 
     Student Dashboard 
             ↓ 
       My Profile 
             ↓ 
   Load authenticated student's 
       profile information 
             ↓ 
 ┌─────────────────────────────┐ 
 │ Basic Information            │ 
 │ Academic Information         │ 
 │ Academic Performance         │ 
 │ Skills                       │ 
 │ Projects                     │ 
 │ Certifications               │ 
 │ Career & Placement           │ 
 │ Learning & Preparation       │ 
 │ Interview & Assessment       │ 
 │ Professional Links & Resume  │ 
 │ Recruitment History          │ 
 │ Consent & Knowledge Sharing  │ 
 └─────────────────────────────┘ 
             ↓ 
       Edit allowed data 
             ↓ 
       Save Changes 
             ↓ 
       Database updated 
Account deletion

## UPDATE — My Profile: locked fields, single Save Changes, working resume/public-profile
actions (Student My Profile Page SDD §6/§9/§12-13)

Save Changes is now one action pinned to the bottom-right footer (next to Delete Profile) that
commits whichever section(s) currently have unsaved edits, replacing each section's own inline
Save Changes button — each section still has its own Edit/Cancel, it just no longer saves
independently. (Skills/Projects/Certifications/Coding Experience/Consent already persist each
change immediately when the student acts, so they were never part of this — there's no draft
for a page-wide Save to batch there.) College/University and Branch/Department are now locked
read-only alongside the already-locked Full Name and Degree — enforced server-side, not just a
disabled input, so a later profile edit can never silently overwrite the verified academic
record those came from. Download Resume is now active exactly when a valid resume exists (it
was previously, incorrectly, gated on having at least one job application, and wired to the
profile photo instead of the resume) and downloads the actual stored PDF through a new
authenticated endpoint. View Public Profile now opens a real read-only preview of the same
stored profile data instead of a permanently disabled placeholder.

## SOURCE PAGE 312

Delete Profile 
      ↓ 
Confirmation Card 
      ↓ 
   ┌───────┐ 
   │ Yes   │ → Delete account/data 
   └───────┘ 
 
   ┌───────┐ 
   │ No    │ → Close card / keep account 
   └───────┘ 
This specification is for LOOP-MIND Student Portal → My Profile, not Advaita Matrimony. 
Recruiter Portal — Authentication & Dashboard Reference Specification 
1. Scope 
The Recruiter Portal is a completely separate portal from the Student Portal. 
There must be no dependency, shared portal experience, or automatic mixing of Student and 
Recruiter interfaces after authentication. 
The authentication system must determine which portal the authenticated mobile number belongs 
to and redirect the user to the corresponding portal. 
 
2. Authentication Flow 
2.1 Landing Page 
The main Landing Page contains the existing Login button. 
When the user clicks Login, the authentication flow begins. 
Login Input 
The login flow must accept: 
• 
Student Number / registered identifier 
• 
Mobile Number 
The entered mobile number must be checked against the registered accounts. 
 
2.2 Account-Type Detection 
The system must determine the account type before opening the portal.

## SOURCE PAGE 313

The registered mobile number can belong to either: 
• 
Student Account 
• 
Recruiter Account 
Student Number / Mobile Number Combination 
The authentication must validate the supplied credentials against the registered account. 
After the user submits the required details: 
1. Validate the registered mobile number. 
2. Generate/send OTP to the registered mobile number. 
3. User enters the OTP. 
4. Verify the OTP. 
5. Identify the account type associated with that verified mobile number. 
6. Redirect the user to the appropriate portal. 
 
3. Portal Routing Logic 
The routing must work as follows: 
Landing Page 
      │ 
      ▼ 
    Login 
      │ 
      ▼ 
Student Number + Mobile Number 
      │ 
      ▼ 
Validate Registered Account 
      │ 
      ▼ 
      OTP 
      │ 
      ▼ 
OTP Verification

## SOURCE PAGE 314

│ 
      ▼ 
Identify Account Type 
      │ 
      ├───────────────┐ 
      │               │ 
      ▼               ▼ 
 Student Account   Recruiter Account 
      │               │ 
      ▼               ▼ 
Student Portal    Recruiter Portal 
Important Rule 
The portal must not be selected manually by the user after OTP verification. 
The system must determine the destination from the verified registered account. 
Therefore: 
Registered Student Mobile 
        → OTP Verification 
        → Student Portal 
and 
Registered Recruiter Mobile 
        → OTP Verification 
        → Recruiter Portal 
 
4. Recruiter Account — Development/Demo Requirement 
For development and testing, a demo Recruiter account must be configured. 
The demo account must contain: 
• 
Recruiter account 
• 
Registered mobile number 
• 
OTP-based authentication 
Demo Authentication

## SOURCE PAGE 315

A development/demo Recruiter mobile number must be configured so that the complete 
authentication flow can be tested. 
Example: 
Account Type: Recruiter 
Mobile Number: [Development Demo Number] 
OTP: [Generated Development OTP] 
The implementation must use the configured demo account rather than hardcoded portal access. 
The purpose is to verify: 
Landing Page 
→ Login 
→ Recruiter Mobile Number 
→ OTP 
→ OTP Verification 
→ Recruiter Account Detection 
→ Recruiter Dashboard 
 
5. Recruiter Portal 
After successful Recruiter authentication, the user must be redirected directly to the Recruiter 
Portal Dashboard. 
The Recruiter Portal is a separate portal and must not display the Student Portal interface. 
The uploaded reference image must be treated as the exact visual reference for the Recruiter 
Dashboard. 
 
6. Reference Page Layout

## SOURCE PAGE 316



## SOURCE PAGE 317



## SOURCE PAGE 318



## SOURCE PAGE 319

The Recruiter Dashboard must preserve the reference layout as-is. 
Required Layout 
┌──────────────────────────────────────────────────────────────────────────────┐ 
│ LOOP-MIND │ Recruiter Portal                    Dashboard Jobs Candidates...│ 
├──────────────────────────────────────────────────────────────────────────────┤ 
│                                                                              │ 
│ Welcome back, Recruiter!                         Quote / Recruiter message  │ 
│ Manage your hiring process...                                                │ 
│                                                                              │ 
│ ┌──────────┐ ┌──────────────┐ ┌────────────┐ ┌────────────┐ ┌────────────┐ │ 
│ │Total Jobs│ │Applications  │ │Shortlisted │ │Under Review│ │Rejected    │ │ 
│ └──────────┘ └──────────────┘ └────────────┘ └────────────┘ └────────────┘ │ 
│                                                                              │ 
│ ┌──────────────────────────────┐ ┌──────────────────────┐ ┌───────────────┐ │ 
│ │ Your Jobs                    │ │ Application Pipeline  │ │ Quick Actions │ │ 
│ │                              │ │                      │ │               │ │ 
│ │ Job table                    │ │ Donut chart          │ │ Create Job    │ │

## SOURCE PAGE 320

│ │                              │ │                      │ │ Candidates    │ │ 
│ │                              │ │                      │ │ Interview Qs  │ │ 
│ └──────────────────────────────┘ └──────────────────────┘ └───────────────┘ │ 
│                                                                              │ 
│ ┌──────────────────────────────┐ ┌────────────────────────────────────────┐ │ 
│ │ Recent Applications          │ │ Upcoming Interviews                     │ │ 
│ │                              │ │                                        │ │ 
│ │ Candidate table              │ │ Interview table                        │ │ 
│ └──────────────────────────────┘ └────────────────────────────────────────┘ │ 
│                                                                              │ 
│ ┌──────────────────────────────────────────────────────────────────────────┐ │ 
│ │ Recent Activity                                                         │ │ 
│ │ Activity items                                                         │ │ 
│ └──────────────────────────────────────────────────────────────────────────┘ │ 
│                                                                              │ 
├──────────────────────────────────────────────────────────────────────────────┤ 
│ Terms of Use       Privacy Policy       Help                                  │ 
│                           LOOP-MIND ©                                         │ 
└──────────────────────────────────────────────────────────────────────────────┘ 
The above represents the reference structure only. The actual implementation must follow the 
uploaded reference image's visual positioning, sizing, spacing, styling and proportions. 
 
7. Header / Navigation 
The header must remain the same as the reference. 
Left Side 
The header contains: 
• 
LOOP-MIND logo 
• 
Recruiter Portal text 
Navigation 
The navigation contains: 
• 
Dashboard

## SOURCE PAGE 321

• 
Jobs 
• 
Candidates 
• 
Interviews 
Dashboard must remain the active navigation item when the Dashboard is open. 
Recruiter Dropdown — REMOVE 
The reference currently contains a right-side: 
R  Recruiter  ▼ 
This Recruiter profile/dropdown element must be completely removed. 
Do not replace it with another dropdown. 
Do not add another profile menu. 
Everything else in the header must remain unchanged. 
 
8. Dashboard Header Section 
The dashboard begins with: 
Heading 
Welcome back, Recruiter! 
Description 
Manage your hiring process and find the right talent with AI-powered insights. 
On the right side, retain the reference quote card: 
“Great teams build great products.” 
– LOOP-MIND 
The quote card's position and visual treatment must remain consistent with the reference. 
 
9. Summary Statistics Cards 
The dashboard contains five summary cards in one horizontal row. 
Card 1 — Total Jobs 
• 
Icon: Briefcase 
• 
Label: Total Jobs 
• 
Value: 8 
• 
Right-arrow indicator 
Card 2 — Total Applications

## SOURCE PAGE 322

• 
Icon: Document/Application icon 
• 
Label: Total Applications 
• 
Value: 320 
• 
Right-arrow indicator 
Card 3 — Shortlisted 
• 
Icon: Candidates/People icon 
• 
Label: Shortlisted 
• 
Value: 48 
• 
Right-arrow indicator 
Card 4 — Under Review 
• 
Icon: Clock icon 
• 
Label: Under Review 
• 
Value: 76 
• 
Right-arrow indicator 
Card 5 — Rejected 
• 
Icon: Rejection/Cross icon 
• 
Label: Rejected 
• 
Value: 196 
• 
Right-arrow indicator 
The cards must preserve the reference's: 
• 
Horizontal arrangement 
• 
Dark card background 
• 
Border treatment 
• 
Icon containers 
• 
Typography hierarchy 
• 
Spacing 
• 
Arrow positioning 
• 
Overall dimensions 
 
10. Your Jobs Section 
The left side of the next dashboard row contains Your Jobs.

## SOURCE PAGE 323

Header 
Your Jobs 
Description: 
Manage and track your job postings. 
Right side: 
• 
View all 
• 
+ Create New Job 
Job Table 
Columns: 
Column 
Job Title 
Applications 
Shortlisted 
Under Review 
Rejected 
Status 
Actions 
Reference job data: 
Job Title 
Applications Shortlisted Under Review Rejected Status 
Software Engineer 120 
18 
32 
70 
Active 
SDE Intern 
85 
12 
20 
53 
Active 
Frontend Developer 60 
10 
15 
35 
Active 
Data Analyst 
40 
8 
9 
23 
Paused 
Each row contains the corresponding action menu at the far right. 
 
11. Application Pipeline 
The center section contains Application Pipeline. 
Header 
Application Pipeline

## SOURCE PAGE 324

Description: 
Overall application status across all jobs. 
Visualization 
A donut chart must display: 
320 Applications 
The chart must represent: 
• 
Shortlisted 
• 
Under Review 
• 
Rejected 
Reference values: 
Status 
Count Percentage 
Shortlisted 
48 
15% 
Under Review 76 
24% 
Rejected 
196 
61% 
The center of the chart displays: 
320 
Applications 
 
12. Quick Actions 
The right-side panel contains Quick Actions. 
It must contain exactly these actions: 
1. Create New Job 
Button: 
Create New Job → 
With the add icon. 
2. View All Candidates 
Button: 
View All Candidates → 
With the candidates icon. 
3. Prepare Interview Questions

## SOURCE PAGE 325

Button: 
Prepare Interview Questions → 
With the document/question icon. 
The first action uses the highlighted primary-button treatment shown in the reference. 
 
13. Recent Applications 
The lower-left section contains Recent Applications. 
Header 
Recent Applications 
Right side: 
View all 
Table 
Columns: 
Column 
Candidate Name 
Job Role 
Applied On 
AI Status 
Action 
Reference data: 
Candidate 
Job Role 
Applied On AI Status 
Action 
Rahul Sharma Software Engineer 2 hours ago Shortlisted 
Review → 
Sneha Reddy SDE Intern 
5 hours ago Under Review Review → 
Arjun Verma Frontend Developer 1 day ago 
Hold 
Review → 
Kavya Nair 
Data Analyst 
1 day ago 
Rejected 
Review → 
Aditya Singh Software Engineer 2 days ago Under Review Review → 
The AI status must retain the reference's status-badge treatment. 
 
14. Upcoming Interviews

## SOURCE PAGE 326

The lower-right section contains Upcoming Interviews. 
Header 
Upcoming Interviews 
Right side: 
View all 
Table 
Columns: 
Column 
Candidate Name 
Job Role 
Date & Time 
Status 
Reference data: 
Candidate 
Job Role 
Date & Time 
Status 
Priya Mehta Software Engineer 12 Sep 2025, 10:00 AM Scheduled 
Karan Patel SDE Intern 
12 Sep 2025, 2:00 PM Scheduled 
Neha Gupta Frontend Developer 13 Sep 2025, 11:00 AM Scheduled 
Rohit Kumar Data Analyst 
14 Sep 2025, 3:00 PM Scheduled 
The status must appear using the same badge treatment as the reference. 
 
15. Recent Activity 
The bottom section spans the dashboard width. 
Header 
Recent Activity 
Description: 
Track the latest updates in your hiring process. 
Right side: 
View all 
Activity Items

## SOURCE PAGE 327

The reference contains four activity items: 
Activity 1 
New application received 
Rahul Sharma applied for Software Engineer 
2 hours ago 
Activity 2 
Candidate shortlisted 
Sneha Reddy for SDE Intern 
5 hours ago 
Activity 3 
Interview questions generated 
For Priya Mehta (Software Engineer) 
1 day ago 
Activity 4 
Job created 
Data Analyst 
2 days ago 
Each activity retains its corresponding icon and visual grouping from the reference. 
 
16. Footer 
The footer must remain exactly as part of the reference layout. 
It contains: 
• 
Terms of Use 
• 
Privacy Policy 
• 
Help 
Below these: 
LOOP-MIND © 
The footer must remain at the bottom of the page and retain the same alignment, spacing and 
styling shown in the reference. 
 
17. Visual Design Requirements

## SOURCE PAGE 328

The Recruiter Dashboard must preserve the reference design language. 
Theme 
• 
Dark overall interface 
• 
Very dark page background 
• 
Dark translucent/solid cards 
• 
Subtle borders 
• 
Cyan/teal accent color 
• 
White/light-gray primary text 
• 
Muted gray secondary text 
Components 
All dashboard components must retain the reference: 
• 
Card layout 
• 
Border radius 
• 
Borders 
• 
Shadows/glows where present 
• 
Icon containers 
• 
Typography hierarchy 
• 
Table row spacing 
• 
Status badges 
• 
Buttons 
• 
Arrow icons 
• 
Donut chart 
• 
Section spacing 
• 
Footer placement 
Responsive Behaviour 
The layout should remain structurally consistent across supported screen sizes without changing the 
information architecture. 
 
18. Dynamic Data Requirement 
The dashboard must use dynamic data. 
The displayed statistics, jobs, applications, candidates, interviews, statuses and activities must 
ultimately come from the Recruiter account's data.

## SOURCE PAGE 329

The reference values above are visual/content reference values for the supplied design and must 
not be treated as permanently hardcoded production data. 
The UI must update when the underlying Recruiter data changes. 
 
19. Strict Reference Preservation Rules 
The uploaded image is the reference for the Recruiter Dashboard. 
Keep exactly 
• 
Same overall dashboard structure 
• 
Same navigation structure 
• 
Same dashboard sections 
• 
Same section ordering 
• 
Same card arrangement 
• 
Same table arrangement 
• 
Same application pipeline position 
• 
Same quick-actions position 
• 
Same recent-applications position 
• 
Same upcoming-interviews position 
• 
Same recent-activity position 
• 
Same footer structure 
• 
Same visual hierarchy 
• 
Same overall dark theme 
Only explicitly requested removal 
Remove only: 
R  Recruiter  ▼ 
from the navbar. 
No other reference element should be removed, replaced, rearranged, or redesigned unless 
explicitly requested in a later requirement. 
 
20. Authentication-to-Dashboard Final Behaviour 
The complete development flow must therefore be: 
                    LANDING PAGE 
                         │

## SOURCE PAGE 330

▼ 
                       LOGIN 
                         │ 
                         ▼ 
             Student Number + Mobile 
                         │ 
                         ▼ 
              Registered Account Check 
                         │ 
                         ▼ 
                    Send OTP 
                         │ 
                         ▼ 
                   Enter OTP 
                         │ 
                         ▼ 
                  Verify OTP 
                         │ 
              ┌──────────┴──────────┐ 
              │                     │ 
              ▼                     ▼ 
       STUDENT ACCOUNT       RECRUITER ACCOUNT 
              │                     │ 
              ▼                     ▼ 
      STUDENT PORTAL          RECRUITER PORTAL 
                                    │ 
                                    ▼ 
                             RECRUITER DASHBOARD 
The Recruiter Dashboard must open using the uploaded reference layout, with only the Recruiter 
dropdown/profile element removed from the navbar. 
No Student Portal component should appear inside the Recruiter Portal, and no Recruiter Portal 
component should be introduced into the Student Portal.

## SOURCE PAGE 331

LOOP-MIND — Recruiter Portal: Job Management & Create New Job Specification 
1. Page Identity 
This is the Recruiter Portal — Job Management page. 
The uploaded screenshot is the authoritative visual reference for this page. 
The page must retain the same layout, structure, positioning, spacing, hierarchy, buttons, 
navigation, table structure, and overall visual appearance shown in the reference. 
Only the functionality explicitly specified below should be added. 
 
2. How the Job Management Page Opens 
The Job Management page must be accessible from both of these locations: 
A. Recruiter Navbar 
When the recruiter clicks: 
Jobs 
in the Recruiter Portal navbar: 
Dashboard | Jobs | Candidates | Interviews 
the Job Management page must open. 
B. Recruiter Dashboard — Create New Job 
The Recruiter Dashboard contains a: 
Create New Job 
button. 
When the recruiter clicks this button, the Job Management page must open. 
C. Job Management Page — Create New Job 
The Job Management page itself also contains: 
+ Create New Job 
inside the Your Job Postings section. 
Clicking this button must open the Create New Job card/modal described below. 
 
3. Reference Layout 
The uploaded screenshot must be treated as the exact reference layout. 
The page structure is: 
┌──────────────────────────────────────────────────────────────┐

## SOURCE PAGE 332

│ LOOP-MIND | Recruiter Portal                                │ 
│                         Dashboard Jobs Candidates Interviews │ 
├──────────────────────────────────────────────────────────────┤ 
│                                                              │ 
│ Job Management                              Quote Card       │ 
│ Description                                                  │ 
│                                                              │ 
├──────────────────────────────────────────────────────────────┤ 
│                                                              │ 
│ Total Jobs | Active Jobs | Paused Jobs | Total Applications │ 
│                                                              │ 
├──────────────────────────────────────────────────────────────┤ 
│                                                              │ 
│ Your Job Postings                                            │ 
│                                      Search                  │ 
│                                      All Status              │ 
│                                      Create New Job          │ 
│                                                              │ 
│ ┌──────────────────────────────────────────────────────────┐ │ 
│ │ Job Listings Table                                       │ │ 
│ │                                                          │ │ 
│ │ Job Title | Role Type | Experience | Applications | ... │ │ 
│ │                                                          │ │ 
│ └──────────────────────────────────────────────────────────┘ │ 
│                                                              │ 
├──────────────────────────────────────────────────────────────┤ 
│ Terms of Use     Privacy Policy     Help                     │ 
│                         LOOP-MIND ©                           │ 
└──────────────────────────────────────────────────────────────┘ 
Do not redesign this layout.

## SOURCE PAGE 333

4. Dynamic Job Management 
The Job Management page must be completely dynamic. 
The recruiter-created jobs must be stored in the application's database. 
The following must not be hardcoded: 
• 
Job titles 
• 
Role types 
• 
Experience 
• 
Application counts 
• 
Shortlisted counts 
• 
Under Review counts 
• 
Rejected counts 
• 
Job status 
• 
Posted date 
• 
Total Jobs 
• 
Active Jobs 
• 
Paused Jobs 
• 
Total Applications 
The values visible in the screenshot are reference/demo data only. 
 
5. Create New Job Button 
The existing button: 
+ Create New Job 
must remain in the exact location represented in the reference. 
When clicked: 
Create New Job 
       ↓ 
Open Create Job Card/Modal 
       ↓ 
Center of the Page 
The card/modal must appear in the center of the page.

## SOURCE PAGE 334

The underlying Job Management page remains visible behind it according to the application's modal 
behavior. 
 
6. Create New Job Card/Modal 
The recruiter uses this card/modal to create a new job posting. 
The recruiter must provide the required job information and constraints necessary for the job 
posting. 
The form must support the job constraints defined by the recruiter. 
The information explicitly mentioned for the form includes: 
Job Title 
Job Role 
Experience 
Job Constraints 
Additional fields should only be included where they are actually defined by the project's job 
requirements. Do not invent unspecified fields or constraints. 
 
7. Job Title 
The recruiter must be able to provide: 
Job Title 
Example: 
Software Engineer 
The example is only illustrative. 
The actual value must be entered by the recruiter and stored dynamically. 
 
8. Job Role 
The recruiter must provide/select: 
Job Role 
The role information becomes part of the created job posting. 
The available options must follow the project's dynamic dataset requirement rather than being an 
arbitrary hardcoded list. 
 
9. Experience Requirement

## SOURCE PAGE 335

The recruiter must define the required: 
Experience 
for the job. 
This information must be stored with the job posting and displayed dynamically in the Job 
Management table. 
 
10. Recruiter-Defined Constraints 
The recruiter must be able to specify the constraints applicable to the job. 
The important rule is: 
The recruiter defines the requirements/constraints for the job, and those requirements become 
part of the job posting. 
These requirements must later be available to the Student Portal's Jobs page so students can see the 
job and determine whether they can apply. 
Do not invent a fixed constraint list that was not specified. 
 
11. Job Creation 
After the recruiter provides the required information: 
Create New Job 
       ↓ 
Validate Required Information 
       ↓ 
Create Job 
       ↓ 
Store Job in Database 
       ↓ 
Job becomes available dynamically 
The newly created job must be persisted. 
It must not exist only in frontend state. 
 
12. Newly Created Job in Job Management 
After successful creation, the newly created job must appear dynamically in: 
Your Job Postings

## SOURCE PAGE 336

on the Job Management page. 
The job should contain its actual: 
• 
Job Title 
• 
Role Type 
• 
Experience 
• 
Application count 
• 
Shortlisted count 
• 
Under Review count 
• 
Rejected count 
• 
Status 
• 
Posted date 
where applicable. 
The counts must update based on actual application data. 
 
13. Job Availability in Student Portal 
A recruiter-created job must also become available in the Student Portal → Jobs page. 
Flow: 
Recruiter 
   │ 
   ▼ 
Create New Job 
   │ 
   ▼ 
Job stored in database 
   │ 
   ▼ 
Job becomes available in Student Jobs 
   │ 
   ▼ 
Student can see the job 
   │

## SOURCE PAGE 337

▼ 
Student can apply to that job 
The Student Jobs page must therefore consume the dynamically stored job data. 
There must not be a separate hardcoded job list for students. 
 
14. Cross-Portal Data Flow 
The recruiter creates the job once. 
The same stored job record must be used by both portals. 
                  DATABASE 
                     │ 
          ┌──────────┴──────────┐ 
          │                     │ 
          ▼                     ▼ 
   Recruiter Portal       Student Portal 
          │                     │ 
   Job Management           Jobs Page 
          │                     │ 
          ▼                     ▼ 
   Manage Job              View Job 
                                │ 
                                ▼ 
                             Apply 
This ensures that when a recruiter creates a new job, students can receive the same job dynamically. 
 
15. Job Application Relationship 
When a student applies to a recruiter-created job, that application must be associated with the 
corresponding job. 
This allows the Recruiter Job Management page to dynamically update: 
Applications 
Shortlisted 
Under Review

## SOURCE PAGE 338

Rejected 
for that job. 
The recruiter-side application/ATS workflow will be specified separately when the Recruiter 
Candidates page is provided. 
 
16. Existing Job Management Controls 
The following existing controls from the reference must remain: 
Search 
Search jobs by title, role, or keywords... 
Status Filter 
All Status ▼ 
Create New Job 
+ Create New Job 
Per-job action 
View Details → 
Additional action 
⋮ 
Their placement and visual structure must remain consistent with the reference. 
 
17. Statistics Cards 
The four cards remain: 
Total Jobs 
Active Jobs 
Paused Jobs 
Total Applications 
Their values must automatically update after a recruiter creates a new job. 
Example: 
Before: 
Total Jobs = 8 
 
Recruiter creates one job

## SOURCE PAGE 339

After: 
Total Jobs = 9 
The actual values must be calculated from stored data. 
 
18. Search & Filtering 
The existing search and status filtering must work against the recruiter's actual stored jobs. 
For example: 
Recruiter creates: 
Software Engineer 
 
Search: 
Software Engineer 
 
Result: 
Software Engineer 
The UI must not use a static list to simulate search results. 
 
19. Exact Reference Preservation 
The following must remain unchanged from the uploaded reference: 
• 
Overall page layout 
• 
Navbar 
• 
LOOP-MIND | Recruiter Portal 
• 
Dashboard / Jobs / Candidates / Interviews navigation 
• 
Jobs active state 
• 
Page title placement 
• 
Page description placement 
• 
Quote card 
• 
Four statistic cards 
• 
Your Job Postings section 
• 
Search box

## SOURCE PAGE 340

• 
Status dropdown 
• 
Create New Job button placement 
• 
Job table 
• 
Table column order 
• 
View Details button 
• 
Three-dot action 
• 
Footer 
• 
Overall spacing 
• 
Visual hierarchy 
• 
Card positioning 
• 
Table positioning 
The Create New Job interaction is the additional functional behavior specified here. 
 
20. Reference Data vs Actual Data 
The screenshot contains example values such as: 
Total Jobs: 8 
Active Jobs: 6 
Paused Jobs: 2 
Total Applications: 320 
and example jobs such as: 
Software Engineer 
SDE Intern 
Frontend Developer 
Data Analyst 
Backend Developer 
ML Engineer 
DevOps Engineer 
Product Analyst 
These must be treated strictly as reference/demo content. 
They must not be permanently hardcoded as the recruiter's actual jobs. 
The real interface must display the recruiter's dynamically stored data.

## SOURCE PAGE 341

21. No Unspecified Functionality 
Do not add functionality that has not been specified. 
In particular, do not invent: 
• 
Extra job fields 
• 
Extra recruiter constraints 
• 
Extra buttons 
• 
Extra table columns 
• 
Extra modal sections 
• 
Extra job actions 
• 
Extra navigation items 
• 
Additional recruiter workflows 
Those can be defined later when you provide the corresponding requirements. 
 
22. Final Development Requirement 
Build the Recruiter Portal Job Management page using the uploaded screenshot as the exact 
reference for the page layout and visual structure. The page must open when the recruiter clicks 
Jobs in the Recruiter navbar, and the Recruiter Dashboard's Create New Job entry point must also 
navigate to this Job Management page. The existing + Create New Job button on Job Management 
must open a centered Create New Job card/modal. The recruiter must be able to enter the job 
information and constraints required for the posting, including Job Title, Job Role, and Experience. 
After creation, the job must be persisted in the database and dynamically appear in the recruiter's 
Job Management page. The same newly created job must dynamically become available in the 
Student Portal Jobs page so students can apply to it. All job and application information must be 
data-driven; do not hardcode the screenshot's example values. Preserve the reference layout 
exactly and do not add or remove any other UI or functionality beyond what is explicitly specified. 
LOOP-MIND — Recruiter Portal: Candidates Page 
Structured Specification + Exact Reference Layout 
Reference source: the uploaded Candidates page screenshot. 
Important: The specification below preserves the supplied page structure, terminology, placement, 
and workflow. No additional UI sections or unrelated functionality are introduced. 
 
1. Page Identity 
Page Name: Candidates 
Portal: Recruiter Portal 
Purpose: Review and manage candidates who have applied to jobs through the LOOP-MIND Student

## SOURCE PAGE 342

Portal, view AI-based candidate evaluation/status, and continue the recruitment workflow through 
human approval, interview-question generation, and interview invitation. 
 
2. Page Entry Points 
The Candidates page must open from either of these locations: 
A. Recruiter Navbar 
Recruiter Portal navbar contains: 
• 
Dashboard 
• 
Jobs 
• 
Candidates 
• 
Interviews 
When the recruiter clicks Candidates, the Candidates page opens. 
B. Recruiter Dashboard → Quick Actions 
The Recruiter Dashboard contains: 
View All Candidates 
Clicking View All Candidates opens the same Candidates page. 
Both entry points must lead to the same Candidates page and same underlying candidate data. 
 
3. Reference Layout 
The uploaded screenshot is the primary layout reference. 
The implementation must maintain the same overall structure: 
┌──────────────────────────────────────────────────────────────────────┐ 
│ LOOP-MIND | Recruiter Portal     Dashboard Jobs Candidates Interviews│ 
│                                                     Recruiter        │ 
├──────────────────────────────────────────────────────────────────────┤ 
│                                                                      │ 
│ Candidates                                      Quote/Info Card      │ 
│ Review candidates, AI evaluations,               "Great candidates   │ 
│ and recruitment progress.                        build greater..."   │ 
│                                                                      │ 
├──────────────────────────────────────────────────────────────────────┤

## SOURCE PAGE 343

│  Total Candidates │ Shortlisted │ Under Review │ Rejected            │ 
│       320         │     48      │      76      │    196              │ 
├──────────────────────────────────────────────────────────────────────┤ 
│                                                                      │ 
│ All Candidates                                                       │ 
│ View and manage candidates across your job postings.                │ 
│                                                                      │ 
│ Search candidates │ All Jobs │ All Status │ All AI Evaluation │Refresh│ 
│                                                                      │ 
│ ┌──────────────────────────────────────────────────────────────────┐ │ 
│ │ Candidate │ Applied Role │ Applied On │ AI Score │ Matching │     │ │ 
│ │ Name      │              │            │          │ Factors  │     │ │ 
│ ├──────────────────────────────────────────────────────────────────┤ │ 
│ │ Candidate │ Role         │ Time       │ Score    │ Match    │Status│ 
│ │ Candidate │ Role         │ Time       │ Score    │ Match    │Status│ 
│ │ Candidate │ Role         │ Time       │ Score    │ Match    │Status│ 
│ └──────────────────────────────────────────────────────────────────┘ │ 
│                                                                      │ 
├──────────────────────────────────────────────────────────────────────┤ 
│ AI Recruitment Workflow                                              │ 
│ End-to-end process for each candidate.                               │ 
│                                                                      │ 
│ Resume Parser → Embedding → Matching → Shortlisting → Human Approval │ 
│                                                      → Interview      │ 
│                                                      → Email Invitation│ 
├──────────────────────────────────────────────────────────────────────┤ 
│ Terms of Use     Privacy Policy     Help                             │ 
│                         LOOP-MIND ©                                   │ 
└──────────────────────────────────────────────────────────────────────┘ 
Layout rule 
Do not redesign the page.

## SOURCE PAGE 344

The following must remain consistent with the reference: 
• 
Dark LOOP-MIND visual theme 
• 
Navbar position 
• 
Page heading position 
• 
Supporting description 
• 
Quote/information card 
• 
Four summary cards 
• 
All Candidates container 
• 
Search bar 
• 
Filter controls 
• 
Refresh button 
• 
Candidate table 
• 
AI Recruitment Workflow section 
• 
Footer 
• 
Spacing and section hierarchy 
• 
Card-based structure 
• 
Overall visual proportions 
• 
Existing button placement 
• 
Existing workflow presentation 
 
4. Navbar 
The navbar belongs to the Recruiter Portal, completely separate from the Student Portal. 
Left side 
LOOP-MIND | Recruiter Portal 
Navigation 
Dashboard 
Jobs 
Candidates 
Interviews 
Right side 
Recruiter

## SOURCE PAGE 345

▼ 
The Candidates navigation item is the active page. 
The active navigation state follows the same visual treatment shown in the reference. 
 
5. Page Header 
The main heading is: 
Candidates 
Description: 
Review candidates, AI evaluations, and recruitment progress. 
The heading and description appear on the left. 
On the right is the existing informational quote card: 
“Great candidates build greater companies.” 
— LOOP-MIND 
This card remains in the same position as the reference. 
 
6. Candidate Summary Cards 
Four summary cards are displayed directly below the page header. 
Card 1 — Total Candidates 
Total Candidates 
320 
Card 2 — Shortlisted 
Shortlisted 
48 
Card 3 — Under Review 
Under Review 
76 
Card 4 — Rejected 
Rejected 
196 
These values are dynamic in the actual implementation. 
They must represent the current candidate/application state rather than permanently hard-coded 
numbers.

## SOURCE PAGE 346

7. All Candidates Section 
Section heading 
All Candidates 
Description: 
View and manage candidates across your job postings. 
This is the primary candidate-management area. 
 
8. Candidate Search 
The page contains the reference search field: 
Search candidates by name, role, or skills... 
The recruiter can search candidates using relevant candidate information such as: 
• 
Candidate name 
• 
Applied role 
• 
Skills 
Search results must update the displayed candidate list dynamically. 
 
9. Candidate Filters 
The reference contains three filter controls. 
Filter 1 — All Jobs 
Allows the recruiter to filter candidates according to the job they applied for. 
Filter 2 — All Status 
This filter represents the candidate's AI Status. 
Important: 
The status shown in this candidate workflow is AI-generated status. 
It is not the final human recruitment decision. 
The AI status has three possible outcomes: 
Shortlisted 
Hold 
Rejected 
Filter 3 — All AI Evaluation

## SOURCE PAGE 347

Allows the recruiter to filter candidates according to their AI evaluation result. 
 
10. Refresh 
The reference contains: 
Refresh 
The recruiter can refresh the candidate data so the page reflects the latest available 
application/evaluation state. 
 
11. Candidate Data Source 
Candidates shown on this page originate from job applications submitted through the Student 
Portal. 
The relationship is: 
Recruiter creates Job 
        ↓ 
Job becomes available in Student Portal 
        ↓ 
Student views Job 
        ↓ 
Student applies 
        ↓ 
Application is created 
        ↓ 
Candidate appears in Recruiter → Candidates 
Therefore, candidates must not be manually disconnected from job applications. 
Each candidate record must be associated with the specific job/application through which the 
student applied. 
 
12. Candidate Table 
The table follows the uploaded reference structure. 
Columns

## SOURCE PAGE 348

Column 
Purpose 
Candidate Name Student/candidate who applied 
Applied Role 
Role associated with the job application 
Applied On 
When the application was submitted 
AI Score 
AI-generated candidate/job match score 
Matching Factors Main reason/factor behind the AI evaluation 
Status 
AI Status 
Action 
Recruiter action 
The reference action is: 
View Evaluation → 
There is also the existing overflow/more-action control shown at the end of each row. 
 
13. Candidate AI Evaluation 
The AI evaluation must compare: 
Candidate-side information 
Including information available from the student's application/profile, especially: 
• 
Resume 
• 
Skills 
• 
Projects 
• 
Relevant candidate information contained in the application/profile 
Job-side information 
Including: 
• 
Job requirements 
• 
Job constraints 
• 
Required skills 
• 
Role requirements 
• 
Other requirements defined by the recruiter when creating the job 
The AI evaluates the candidate against the specific job they applied for. 
 
14. AI Recruitment Pipeline

## SOURCE PAGE 349

The candidate evaluation follows the workflow shown in the reference. 
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
Interview Agent 
      ↓ 
Email Invitation 
 
15. Step 1 — Resume Parser 
When an application is received, the AI recruitment workflow first processes the candidate's resume. 
The Resume Parser extracts relevant information from the resume so it can be evaluated against the 
job requirements. 
Reference workflow status: 
Resume Parser 
Completed 
The actual status is dynamic and must represent the real processing state. 
 
16. Step 2 — Embedding 
The parsed candidate information is processed for embedding. 
Reference workflow: 
Embedding 
Completed 
The purpose within this workflow is to make the candidate information usable for the subsequent 
matching/evaluation process.

## SOURCE PAGE 350

17. Step 3 — Matching 
The candidate information is compared with the requirements of the specific job application. 
The matching process considers the candidate's available information against the recruiter's job 
requirements. 
Reference workflow: 
Matching 
Completed 
The resulting evaluation contributes to the AI Score and Matching Factors displayed in the 
Candidates table. 
 
18. Step 4 — AI Shortlisting 
The AI then produces an AI Status. 
There are exactly three AI-status outcomes described for this workflow: 
AI Status 1 
Shortlisted 
AI Status 2 
Hold 
AI Status 3 
Rejected 
These are AI-generated recommendations. 
Important distinction 
The AI status must not be treated as the final hiring decision. 
Even if the AI produces: 
Rejected 
the recruitment workflow does not automatically end there. 
The recruiter must cross-check the AI evaluation through Human Approval. 
 
19. View Evaluation Action 
When the recruiter clicks: 
View Evaluation → 
the candidate's evaluation/workflow must be made available on the same Candidates page context, 
following the existing page's workflow presentation.

## SOURCE PAGE 351

The evaluation must expose the recruitment workflow associated with the selected candidate. 
The workflow shown below the candidate table is the reference representation. 
 
20. AI Recruitment Workflow Section 
The reference contains: 
AI Recruitment Workflow 
Description: 
End-to-end process for each candidate. 
The workflow visually presents the candidate's current recruitment-processing stages. 
The stages are: 
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
The workflow must update dynamically according to the selected candidate and their actual 
processing state. 
 
21. Selected Candidate Information 
The workflow area includes a selected-candidate information card. 
Reference example: 
Selected Candidate 
Sneha Reddy

## SOURCE PAGE 352

SDE Intern 
 
AI Score 
78/100 
This information must dynamically correspond to whichever candidate/evaluation is currently 
selected. 
 
22. Human Approval 
After AI shortlisting/evaluation, the next stage is: 
Human Approval 
This is the recruiter's cross-check stage. 
The recruiter reviews the AI result and decides whether to agree with it. 
The recruiter has two decisions: 
Approve 
Disapprove 
Approve 
If the recruiter agrees with the AI evaluation: 
Human Approval 
Approved 
       ↓ 
Interview Agent 
The workflow proceeds to the interview stage. 
Disapprove 
If the recruiter disagrees with the AI evaluation: 
Human Approval 
Disapproved 
The AI recommendation is therefore not treated as the final decision without recruiter review. 
 
23. Interview Stage 
The reference calls this stage: 
Interview

## SOURCE PAGE 353

But functionally it is an Interview Agent. 
The Interview Agent is triggered after the recruiter approves the candidate through Human 
Approval. 
Its purpose is to prepare interview questions for the specific role applied for. 
For example: 
Candidate applies for: 
Software Engineer 
 
        ↓ 
 
Human Approval 
Approved 
 
        ↓ 
 
Interview Agent 
 
        ↓ 
 
Prepare interview questions 
specific to Software Engineer role 
The questions must therefore be generated according to the specific job/role associated with that 
candidate's application. 
 
24. Email Invitation 
After the interview questions are prepared, the workflow proceeds to: 
Email Invitation 
The system must use the candidate's available email information for the interview invitation. 
The email source can include: 
• 
Email information available from the student's profile/application 
• 
Email information available from the candidate's resume when applicable

## SOURCE PAGE 354

The workflow must use the available candidate email information rather than requiring a completely 
separate email entry if an applicable email already exists. 
 
25. Interview Invitation 
The final workflow stage sends an interview invitation to the candidate. 
The invitation communicates that the candidate has been invited for an interview. 
The workflow therefore becomes: 
Resume Parser 
     ↓ 
Embedding 
     ↓ 
Matching 
     ↓ 
AI Shortlisting 
     ↓ 
Human Approval 
     ↓ 
Interview Agent 
     ↓ 
Role-specific Interview Questions 
     ↓ 
Email Invitation 
 
26. Dynamic Workflow State 
The workflow must not always display every stage as completed. 
It must reflect the actual state of the selected candidate. 
For example: 
Resume Parser    → Completed 
Embedding        → Completed 
Matching         → Completed 
Shortlisting     → Completed

## SOURCE PAGE 355

Human Approval   → Under Review 
Interview        → Pending 
Email Invitation → Pending 
This follows the structure shown in the reference image. 
 
27. AI Status vs Human Decision 
This distinction is mandatory. 
AI Status 
Generated by the AI recruitment pipeline: 
Shortlisted 
Hold 
Rejected 
Human Approval 
Recruiter decision: 
Approve 
Disapprove 
Therefore: 
AI Recommendation 
       ↓ 
Recruiter Cross-check 
       ↓ 
Human Approval 
       ↓ 
Next Workflow Stage 
The AI must not silently replace the recruiter decision. 
 
28. End-to-End Recruitment Flow 
The complete functionality described across the Student and Recruiter portals is: 
Recruiter 
   ↓ 
Creates Job

## SOURCE PAGE 356

↓ 
Job appears in Student Portal 
   ↓ 
Student applies 
   ↓ 
Application reaches Recruiter Portal 
   ↓ 
Candidate appears in Candidates 
   ↓ 
Resume Parser 
   ↓ 
Embedding 
   ↓ 
Matching against Job Requirements 
   ↓ 
AI Score + Matching Factors 
   ↓ 
AI Status 
 ┌────────────┬──────────┐ 
 ↓            ↓          ↓ 
Shortlisted   Hold     Rejected 
 └────────────┴──────────┘ 
              ↓ 
       Human Approval 
          ↙       ↘ 
      Approve   Disapprove 
         ↓ 
   Interview Agent 
         ↓ 
Role-specific 
Interview Questions

## SOURCE PAGE 357

↓ 
Email Invitation 
         ↓ 
Candidate receives 
Interview Invitation 
 
29. Dynamic Data Requirements 
The Candidates page must be fully dynamic. 
The following must be generated from actual application/recruitment data: 
• 
Total Candidates 
• 
Shortlisted count 
• 
Under Review count 
• 
Rejected count 
• 
Candidate list 
• 
Applied Role 
• 
Applied On 
• 
AI Score 
• 
Matching Factors 
• 
AI Status 
• 
Selected Candidate 
• 
Workflow state 
• 
Human Approval state 
• 
Interview state 
• 
Email Invitation state 
No permanent demonstration values should control the actual production state. 
The screenshot values such as 320, 48, 76, and 196 are reference UI values, not a requirement to 
permanently hard-code those numbers. 
 
30. Reference Candidate Rows 
The uploaded reference visually demonstrates rows such as: 
Rahul Sharma

## SOURCE PAGE 358

Software Engineer 
2 hours ago 
92/100 
Strong match 
Shortlisted 
View Evaluation 
Sneha Reddy 
SDE Intern 
5 hours ago 
78/100 
Good match 
Under Review 
View Evaluation 
Arjun Verma 
Frontend Developer 
1 day ago 
74/100 
Skills match 
Hold 
View Evaluation 
Kavya Nair 
Data Analyst 
1 day ago 
45/100 
Skill gaps 
Rejected 
View Evaluation 
Aditya Singh 
Software Engineer 
2 days ago 
81/100

## SOURCE PAGE 359

Good match 
Under Review 
View Evaluation 
These are reference examples from the supplied screenshot, not fixed candidate records that must 
be hard-coded. 
 
31. Footer 
The Recruiter Candidates page uses the same footer structure visible in the supplied recruiter 
reference. 
Footer links: 
Terms of Use 
Privacy Policy 
Help 
Bottom branding: 
LOOP-MIND © 
The footer remains at the bottom of the page and follows the existing Recruiter Portal visual 
structure. 
 
32. Strict Reference Layout Rules 
The Candidates page implementation must follow these rules: 
Must remain 
• 
Same navbar structure 
• 
Same Recruiter Portal identity 
• 
Same navigation placement 
• 
Same Candidates active state 
• 
Same page heading placement 
• 
Same description placement 
• 
Same quote card placement 
• 
Same four-card summary layout 
• 
Same All Candidates section 
• 
Same search placement 
• 
Same filter placement

## SOURCE PAGE 360

• 
Same Refresh placement 
• 
Same candidate table structure 
• 
Same workflow section 
• 
Same workflow positioning 
• 
Same footer 
• 
Same dark visual design 
• 
Same card-based hierarchy 
• 
Same overall page structure 
Must be dynamic 
• 
Candidate records 
• 
Application information 
• 
AI score 
• 
Matching factors 
• 
AI status 
• 
Workflow states 
• 
Human approval state 
• 
Interview state 
• 
Email invitation state 
• 
Summary counts 
Must not be changed 
The AI Status concept must remain separate from Human Approval. 
The AI may: 
Shortlist 
Hold 
Reject 
The recruiter then cross-checks through: 
Approve 
Disapprove 
 
33. Final Page Structure 
RECRUITER PORTAL

## SOURCE PAGE 361

│ 
├── Navbar 
│   ├── LOOP-MIND | Recruiter Portal 
│   ├── Dashboard 
│   ├── Jobs 
│   ├── Candidates [ACTIVE] 
│   ├── Interviews 
│   └── Recruiter 
│ 
├── Page Header 
│   ├── Candidates 
│   ├── Description 
│   └── Quote Card 
│ 
├── Summary Cards 
│   ├── Total Candidates 
│   ├── Shortlisted 
│   ├── Under Review 
│   └── Rejected 
│ 
├── All Candidates 
│   ├── Search 
│   ├── All Jobs 
│   ├── All Status 
│   ├── All AI Evaluation 
│   ├── Refresh 
│   └── Candidate Table 
│       ├── Candidate Name 
│       ├── Applied Role 
│       ├── Applied On 
│       ├── AI Score

## SOURCE PAGE 362

│       ├── Matching Factors 
│       ├── AI Status 
│       └── Action 
│ 
├── AI Recruitment Workflow 
│   ├── Selected Candidate 
│   ├── AI Score 
│   ├── Resume Parser 
│   ├── Embedding 
│   ├── Matching 
│   ├── Shortlisting 
│   ├── Human Approval 
│   │   ├── Approve 
│   │   └── Disapprove 
│   ├── Interview Agent 
│   │   └── Role-specific Questions 
│   └── Email Invitation 
│ 
└── Footer 
    ├── Terms of Use 
    ├── Privacy Policy 
    ├── Help 
    └── LOOP-MIND © 
This is the Candidates page specification based strictly on the uploaded reference and the 
workflow you described, without introducing additional portal functionality or changing the 
supplied page structure. 
LOOP-MIND — Student Jobs: Application & Recruiter Decision Tracking 
This is an addition to the existing Student Portal Jobs page. The existing Jobs page layout and 
functionality remain unchanged except for the required application-status/result access described 
below. 
 
1. Purpose

## SOURCE PAGE 363

When a student applies for a job: 
Student applies for Job 
        ↓ 
Application reaches Recruiter Portal 
        ↓ 
AI Recruitment Workflow 
        ↓ 
Recruiter Human Approval 
        ↓ 
Approve OR Disapprove 
The student's Jobs area must allow the student to see the outcome of the jobs they have applied for. 
The important requirement is that a recruiter disapproval must not simply end the student's 
experience. 
If the recruiter disapproves the application, the student should be able to see why they were 
disapproved, particularly when the reason is a skill gap, so they can work on that gap and improve 
their preparation. 
 
2. Add Application Access to the Existing Student Jobs Page 
The existing Student Portal Jobs page remains the same. 
Add the required application-status access without redesigning the existing Jobs page. 
A suitable addition within the existing Jobs-page structure is: 
My Applications 
or an equivalent application-status access control. 
The purpose is to let the student see jobs they have already applied to and their current result. 
No unrelated functionality should be added. 
 
3. My Applications 
When the student opens the application-status area, the content must appear in the center of the 
page, following the existing LOOP-MIND modal/card visual language. 
It must display the jobs that the currently logged-in student has applied for. 
Example structure: 
┌─────────────────────────────────────────────┐

## SOURCE PAGE 364

│              My Applications                │ 
│                                             │ 
│ Job              Role          Status        │ 
│                                             │ 
│ Software         Software      Interview     │ 
│ Engineer         Engineer      Invitation    │ 
│                                             │ 
│ SDE Intern       SDE Intern    Disapproved   │ 
│                                  View Reason │ 
└─────────────────────────────────────────────┘ 
The displayed records must come from the student's actual applications. 
 
4. Application Information 
For every job the student has applied to, the student should be able to identify: 
• 
Job 
• 
Applied role 
• 
Current application result/status 
• 
Whether an interview invitation has been received 
• 
Whether the application was disapproved 
• 
Disapproval reason, when applicable 
The information must be dynamically connected to the corresponding application and recruiter 
workflow. 
 
5. Recruiter Approval Flow 
If the recruiter selects: 
Approve 
the previously defined recruiter workflow continues: 
Human Approval 
      ↓ 
Approved 
      ↓

## SOURCE PAGE 365

Interview Agent 
      ↓ 
Role-specific Interview Questions 
      ↓ 
Email Invitation 
      ↓ 
Student receives Interview Invitation 
The student's application result must reflect the progression. 
If the interview invitation has been generated/sent, the student must be able to see that an 
interview invitation is associated with that application. 
 
6. Recruiter Disapproval Flow 
If the recruiter selects: 
Disapprove 
the application must be recorded as Disapproved. 
The workflow should retain the reason for the recruiter decision. 
AI Evaluation 
      ↓ 
Human Approval 
      ↓ 
Recruiter Disapproves 
      ↓ 
Application = Disapproved 
      ↓ 
Reason recorded 
      ↓ 
Reason becomes visible to Student 
 
7. Disapproval Reason 
The student must be able to see why the application was disapproved. 
The reason should specifically explain the identified issue.

## SOURCE PAGE 366

A major example is: 
Skill Gap 
If the candidate was disapproved because the candidate does not sufficiently meet a required skill: 
Disapproved 
 
Reason: 
Skill Gap 
 
Missing / Insufficient Skill: 
System Design 
The exact reason must come from the recruitment evaluation/application decision data. 
Do not display a generic reason when a specific reason has been recorded. 
 
8. Skill-Gap Feedback 
When the reason is a skill gap, the student should be able to understand: 
• 
Which required skill was insufficient 
• 
That the skill was relevant to the applied job 
• 
Why it affected the application outcome 
Example: 
Application Status 
Disapproved 
 
Reason 
Skill Gap 
 
Skill Identified 
System Design 
 
Why 
The required skill level for the applied role 
was not sufficiently demonstrated.

## SOURCE PAGE 367

The wording should be generated from the actual evaluation/decision data rather than using hard-
coded reasons. 
 
9. Other Disapproval Reasons 
Disapproval is not necessarily limited to a skill gap. 
If another specific reason was recorded by the recruitment workflow, that reason must be shown 
instead. 
Structure: 
Application Status 
Disapproved 
 
Reason 
[Actual recorded reason] 
 
Details 
[Relevant explanation from the evaluation/decision] 
Do not invent a reason when no reason exists. 
 
10. Center-of-Page Result Card 
When the student selects an application to view its result/reason, the result must appear as a 
centered card/modal, consistent with the existing LOOP-MIND interface. 
Example: 
                    ┌──────────────────────────────┐ 
                    │     Application Result       │ 
                    │                              │ 
                    │ Software Engineer            │ 
                    │                              │ 
                    │ Status                       │ 
                    │ Disapproved                  │ 
                    │                              │ 
                    │ Reason                       │ 
                    │ Skill Gap                    │

## SOURCE PAGE 368

│                              │ 
                    │ Skill                         │ 
                    │ System Design                │ 
                    │                              │ 
                    │ [Preparation / Close]         │ 
                    └──────────────────────────────┘ 
The card must be centered on the page. 
 
11. Improvement Purpose 
The purpose of exposing the disapproval reason is to help the student improve rather than simply 
showing: 
Disapproved 
The student should understand the specific area that prevented the application from progressing. 
For a skill-gap decision: 
Job Requirement 
      ↓ 
Candidate Evaluation 
      ↓ 
Skill Gap Identified 
      ↓ 
Recruiter Disapproves 
      ↓ 
Student Sees Skill Gap 
      ↓ 
Student Prepares 
      ↓ 
Student Learns / Improves Skill 
      ↓ 
Student Becomes Better Prepared 
This creates the intended feedback loop within LOOP-MIND.

## SOURCE PAGE 369

12. Connection With Skill Gap & Preparation Plan 
The identified skill gap should remain connected to the student's existing LOOP-MIND preparation 
ecosystem. 
The student can use the identified gap to understand what needs improvement and continue 
preparing through the existing: 
• 
Skill Gap 
• 
Preparation Plan 
functionality. 
The existing pages themselves should not be redesigned as part of this requirement. 
The purpose here is only to expose the relevant application outcome and reason so the student 
knows what needs improvement. 
 
13. Interview Invitation Result 
When the recruiter approves the application and the Interview Agent completes the required 
interview preparation/invitation workflow: 
Human Approval 
      ↓ 
Approved 
      ↓ 
Interview Agent 
      ↓ 
Interview Questions Prepared 
      ↓ 
Email Invitation 
the student's application record should reflect the interview invitation outcome. 
Example: 
Software Engineer 
Applied 
 
Status: 
Interview Invitation

## SOURCE PAGE 370

View Details → 
The student should be able to distinguish this from a disapproved application. 
 
14. Application Status Lifecycle 
The student's application information should reflect the actual recruitment workflow state. 
Conceptually: 
Applied 
   ↓ 
AI Evaluation 
   ↓ 
AI Status 
   ├── Shortlisted 
   ├── Hold 
   └── Rejected 
          ↓ 
     Human Approval 
       ↙       ↘ 
   Approve    Disapprove 
      ↓           ↓ 
 Interview     Disapproved 
      ↓           ↓ 
 Invitation    Reason shown 
The AI Status and Human Decision must remain separate. 
A recruiter disapproval is a human decision and must not be confused with the AI's initial 
recommendation. 
 
15. Important Relationship 
The complete relationship between the two portals is: 
                 RECRUITER PORTAL 
                       │ 
                 Recruiter creates Job

## SOURCE PAGE 371

│ 
                       ↓ 
                 STUDENT PORTAL 
                       │ 
                  Student applies 
                       │ 
                       ↓ 
                 RECRUITER PORTAL 
                       │ 
              AI Recruitment Workflow 
                       │ 
       Resume → Embedding → Matching 
                       │ 
                  AI Status 
                       │ 
                       ↓ 
                Human Approval 
                  ↙         ↘ 
             Approve      Disapprove 
                ↓             ↓ 
        Interview Agent    Reason stored 
                ↓             ↓ 
       Email Invitation   STUDENT PORTAL 
                ↓             │ 
        STUDENT PORTAL      Student sees 
                │            disapproval 
        Interview Invite      reason 
 
16. Dynamic Data Requirement 
Everything described here must be dynamic. 
The system must not hard-code:

## SOURCE PAGE 372

• 
Applied jobs 
• 
Application results 
• 
Interview invitations 
• 
Disapproval status 
• 
Disapproval reasons 
• 
Skill gaps 
• 
Recruiter decisions 
They must be linked to: 
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
Therefore, a student must only see their own applications and their corresponding results. 
 
17. Strict UI Rule 
The existing Student Jobs page remains the reference. 
Do not replace its layout. 
Do not redesign the Jobs page. 
Only add the required application-result access and centered result card/modal. 
The existing: 
• 
Navbar 
• 
Jobs listing 
• 
Search 
• 
Filters

## SOURCE PAGE 373

• 
Job cards 
• 
Apply Now 
• 
Save 
• 
Footer 
• 
Dark LOOP-MIND styling 
• 
Existing spacing and visual language 
remain unchanged. 
The new application-result interaction must visually belong to the same existing Student Portal 
design. 
 
18. Final Functional Requirement 
The core requirement can be summarized as: 
Every student application must have a traceable outcome. If the recruiter approves the 
application, the student can receive the interview invitation through the existing interview 
workflow. If the recruiter disapproves the application, the student must be able to open a 
centered result card and see the recorded reason—especially the specific skill gap when that is the 
reason—so the student can improve that skill and prepare better for future opportunities. 
This extends the existing workflow without changing the previously defined Recruiter Candidates 
page structure. 
Recruiter Portal — Interviews Page Specification 
1. Page Identity 
Page Name: Interviews 
Portal: Recruiter Portal 
Purpose: Manage recruiter interview activities, view generated interview questions, schedule 
interviews for specific candidates, and track interview progress. 
The page must follow the uploaded reference image exactly for its visual layout, structure, spacing, 
hierarchy, cards, navigation, table structure, footer, and overall dark LOOP-MIND design. 
No unrelated UI elements should be introduced. 
 
2. Navigation Entry Points 
The Interviews page must open from both of these locations: 
A. Recruiter Navbar 
In the Recruiter Portal navbar: 
Dashboard | Jobs | Candidates | Interviews

## SOURCE PAGE 374

When the recruiter clicks Interviews, this page opens. 
B. Recruiter Dashboard 
If the Recruiter Dashboard contains the Prepare Interview Questions quick action, clicking it must 
open this same Interviews page. 
Both entry points must lead to the same Interviews page. 
 
3. Reference Layout 
The uploaded image establishes the page layout. 
Overall structure 
┌─────────────────────────────────────────────────────────────────────┐ 
│ LOOP-MIND | Recruiter Portal     Dashboard Jobs Candidates Interviews│ 
│                                                        Recruiter     │ 
├─────────────────────────────────────────────────────────────────────┤ 
│                                                                     │ 
│ Interviews                                      Quote / Message      │ 
│ Manage interview schedules, review AI-generated questions,          │ 
│ and track candidate progress.                                       │ 
│                                                                     │ 
├─────────────────────────────────────────────────────────────────────┤ 
│ Total Interviews │ Scheduled │ Completed │ Cancelled                │ 
├─────────────────────────────────────────────────────────────────────┤ 
│ Scheduled Interviews                                                │ 
│                                                                     │ 
│ Search │ All Jobs ▼ │ All Status ▼ │ Schedule Interview             │ 
│                                                                     │ 
│ Candidate | Job Role | Interview Type | Date & Time | AI Status     │ 
│           |          |                |             | Status |Action│ 
│                                                                     │ 
├─────────────────────────────────────────────────────────────────────┤ 
│ Recent Activity                                                     │ 
│                                                                     │

## SOURCE PAGE 375

│ Activity 1 │ Activity 2 │ Activity 3 │ Activity 4                  │ 
├─────────────────────────────────────────────────────────────────────┤ 
│ Terms of Use     Privacy Policy     Help                            │ 
│                         LOOP-MIND ©                                 │ 
└─────────────────────────────────────────────────────────────────────┘ 
The actual implementation must visually follow the uploaded screenshot rather than redesigning 
this structure. 
 
4. Header / Navbar 
Use the same Recruiter Portal navbar shown in the reference. 
Left side 
• 
LOOP-MIND logo 
• 
Recruiter Portal 
Navigation 
• 
Dashboard 
• 
Jobs 
• 
Candidates 
• 
Interviews 
Interviews is the active navigation item. 
The active state must use the same visual treatment as the uploaded reference. 
Right side 
• 
Recruiter profile/avatar 
• 
Recruiter name 
• 
Existing profile dropdown 
No changes to the navbar structure are required for this page. 
 
5. Page Header 
The page starts with: 
Title 
Interviews 
Description

## SOURCE PAGE 376

Manage interview schedules, review AI-generated questions, and track candidate progress. 
On the right side, retain the quote card from the reference layout: 
“Better interviews build brighter futures.” 
– LOOP-MIND 
The quote card must remain positioned exactly as shown in the reference layout. 
 
6. Interview Summary Cards 
Immediately below the header, retain the four summary cards. 
Card 1 — Total Interviews 
• 
Icon 
• 
Label: Total Interviews 
• 
Dynamic total count 
• 
Right arrow 
Card 2 — Scheduled 
• 
Icon 
• 
Label: Scheduled 
• 
Dynamic scheduled interview count 
• 
Right arrow 
Card 3 — Completed 
• 
Icon 
• 
Label: Completed 
• 
Dynamic completed interview count 
• 
Right arrow 
Card 4 — Cancelled 
• 
Icon 
• 
Label: Cancelled 
• 
Dynamic cancelled interview count 
• 
Right arrow 
These values must be calculated from the actual interview data. 
The numbers shown in the screenshot are reference/demo values only and must not be treated as 
permanent hardcoded values.

## SOURCE PAGE 377

7. Scheduled Interviews Section 
The main section is: 
Scheduled Interviews 
Description: 
View and manage all interview sessions for your job postings. 
This section must maintain the same card/container structure from the uploaded reference. 
 
8. Search 
At the top-right of the Scheduled Interviews section, retain the search field. 
Placeholder: 
Search by candidate name, job role, or skills... 
The recruiter must be able to search interview records using relevant candidate/interview 
information. 
Search results must dynamically update the interview table. 
 
9. Job Filter 
Retain the: 
All Jobs ▼ 
dropdown. 
It must contain dynamically available jobs belonging to the recruiter. 
The recruiter can select a specific job to filter the interview list. 
 
10. Status Filter 
Retain: 
All Status ▼ 
The status filter must dynamically filter interview records according to their current interview status. 
The filter must work together with search and the job filter. 
 
11. Schedule Interview Button 
Retain the reference-layout button: 
+ Schedule Interview

## SOURCE PAGE 378

This button allows the recruiter to schedule an interview. 
The scheduling must be associated with a specific eligible candidate/application. 
The implementation must not create an interview disconnected from a candidate/job application. 
 
12. Interview Table 
The table must preserve the same structure shown in the uploaded reference. 
Columns 
1. Candidate Name 
2. Job Role 
3. Interview Type 
4. Date & Time 
5. AI Status 
6. Status 
7. Actions 
 
13. Candidate Name 
Display the candidate associated with the interview. 
The candidate must come from the student application that progressed through the recruitment 
workflow. 
The interview must therefore remain connected to: 
Student 
   ↓ 
Job Application 
   ↓ 
Recruiter Review 
   ↓ 
Human Approval 
   ↓ 
Interview 
 
14. Job Role

## SOURCE PAGE 379

Display the role for which the candidate applied. 
Example from the reference: 
Software Engineer 
The value must come dynamically from the associated job posting. 
 
15. Interview Type 
Display the type of interview. 
The reference currently shows: 
Technical 
The value must be associated with the particular interview. 
 
16. Date & Time 
Display the scheduled interview date and time for that candidate. 
Example reference format: 
12 Sep 2025, 10:00 AM 
This must be dynamic. 
It must reflect the actual scheduled interview. 
 
17. AI Status 
This is an important distinction. 
The AI Status represents the state of the AI interview-question generation process. 
It is not the same thing as the interview Status. 
Possible states demonstrated by the reference include: 
• 
Questions Generated 
• 
Generating Questions 
• 
Not Started 
The implementation should use the appropriate state based on the actual interview-question 
generation workflow. 
 
18. Interview Status 
The separate Status column represents the actual interview state.

## SOURCE PAGE 380

The reference demonstrates: 
Scheduled 
Other states can exist according to the interview lifecycle, such as completed or cancelled, 
consistent with the summary cards. 
Do not merge AI Status and Interview Status. 
They are two separate pieces of information. 
 
19. Interview Questions Generation 
The interview questions are not generated merely because the recruiter opened the Interviews 
page. 
The questions are generated as part of the recruitment workflow after the candidate reaches the 
appropriate approved stage. 
The flow specified is: 
Candidate applies for job 
        ↓ 
AI evaluates candidate 
        ↓ 
AI matching / screening 
        ↓ 
AI Status 
        ↓ 
Human Approval 
        ↓ 
Recruiter approves 
        ↓ 
Interview Agent 
        ↓ 
Generate role-specific interview questions 
        ↓ 
Questions are saved against the interview/candidate 
        ↓ 
Questions become available in Interviews

## SOURCE PAGE 381

20. Role-Specific Interview Questions 
When the recruiter approves a candidate for interview, the Interview Agent must prepare interview 
questions based on the specific job role. 
For example: 
Software Engineer 
        ↓ 
Software Engineer requirements 
        ↓ 
Generate relevant technical interview questions 
The questions must therefore be tied to the particular: 
• 
Candidate 
• 
Job application 
• 
Job posting 
• 
Job role 
The system should not use one generic question set for every candidate/job. 
 
21. Generated Questions Must Be Persisted 
Once generated, the interview questions must be saved. 
Opening or refreshing the Interviews page must not regenerate the questions unnecessarily. 
The saved questions should remain associated with the relevant interview record. 
Therefore: 
Generated Questions 
        ↓ 
Save 
        ↓ 
Interview Record 
        ↓ 
View Details 
 
22. View Details Action

## SOURCE PAGE 382

Each interview row contains: 
View Details → 
This is the action through which the recruiter can inspect the particular interview. 
When clicked, the relevant interview details should become visible. 
The details must correspond only to the selected candidate/interview. 
The generated interview questions must be visible through this interview detail action. 
 
23. Interview Detail Information 
The detail view should expose the information already belonging to the selected interview, including 
the generated interview questions. 
The questions must be those generated for the selected candidate's specific job role. 
Do not display questions belonging to another candidate or another job. 
 
24. Schedule Interview Workflow 
The recruiter must be able to schedule an interview for a particular eligible candidate. 
The scheduling operation must capture the interview's: 
• 
Candidate 
• 
Job/application context 
• 
Interview type 
• 
Date 
• 
Time 
The resulting interview must then appear in the Scheduled Interviews table. 
The corresponding summary count must also update dynamically. 
 
25. Interview Lifecycle 
The overall interview lifecycle should follow the recruitment workflow already defined: 
Candidate Application 
        ↓ 
Resume Parsing 
        ↓ 
Embedding

## SOURCE PAGE 383

↓ 
Matching 
        ↓ 
AI Screening / AI Status 
        ↓ 
Human Approval 
        ↓ 
Recruiter Approves 
        ↓ 
Interview Agent 
        ↓ 
Role-Specific Questions Generated 
        ↓ 
Interview Invitation 
        ↓ 
Interview Scheduled 
        ↓ 
Interview 
        ↓ 
Completed / Cancelled 
The Interviews page is responsible for the interview-related portion of this lifecycle. 
 
26. Recent Activity 
At the bottom of the page, retain the Recent Activity section exactly in the same position and 
structure as the reference. 
Description: 
Track the latest updates on interviews. 
The reference displays activity cards such as: 
• 
Interview questions generated 
• 
Interview invite sent 
• 
Interview scheduled

## SOURCE PAGE 384

• 
Interview completed 
These activities must be dynamically derived from actual interview events. 
 
27. Recent Activity Examples 
The reference demonstrates activities such as: 
Interview questions generated 
For a particular candidate and job role. 
Interview invite sent 
For the particular candidate. 
Interview scheduled 
Showing the candidate and job role. 
Interview completed 
Showing the relevant candidate and job role. 
These are reference examples of the activity structure; actual displayed records must come from 
system data. 
 
28. Dynamic Behaviour 
The entire page must be dynamic. 
The following must not remain hardcoded: 
• 
Interview totals 
• 
Scheduled count 
• 
Completed count 
• 
Cancelled count 
• 
Candidate names 
• 
Job roles 
• 
Interview dates 
• 
Interview times 
• 
AI statuses 
• 
Interview statuses 
• 
Recent activities 
• 
Generated questions

## SOURCE PAGE 385

All should reflect the current recruiter account and its associated interview/application data. 
 
29. Recruiter Isolation 
This is a Recruiter Portal page. 
Interview records must belong to the currently authenticated recruiter. 
A recruiter must not see another recruiter's private interview records. 
The interview list should therefore be scoped to the authenticated recruiter and their job postings. 
 
30. Relationship With Candidates Page 
The Interviews page must consume the recruitment workflow produced from the Candidates page. 
The candidate should not independently appear as an interview candidate without progressing 
through the defined recruitment process. 
The intended relationship is: 
Recruiter Job 
     ↓ 
Student applies 
     ↓ 
Candidate appears in Candidates 
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
 
31. Relationship With Student Portal 
The interview created for a student must remain connected to the student's job application.

## SOURCE PAGE 386

This allows the interview/invitation status to eventually be reflected in the student-side 
job/application experience according to the recruitment workflow. 
The Interviews page itself remains part of the Recruiter Portal. 
 
32. Reference Visual Requirements 
The uploaded screenshot is the authoritative layout reference for this page. 
Maintain: 
• 
Same dark theme 
• 
Same overall page width 
• 
Same navbar position 
• 
Same header arrangement 
• 
Same title placement 
• 
Same quote card placement 
• 
Same four summary-card arrangement 
• 
Same Scheduled Interviews container 
• 
Same search placement 
• 
Same filter placement 
• 
Same Schedule Interview button placement 
• 
Same table structure 
• 
Same column arrangement 
• 
Same Recent Activity section 
• 
Same footer 
• 
Same spacing hierarchy 
• 
Same visual hierarchy 
• 
Same card-based structure 
• 
Same active navbar treatment 
• 
Same overall alignment 
Do not redesign the page. 
 
33. Footer 
The footer must remain consistent with the Recruiter Portal reference.

## SOURCE PAGE 387

Keep: 
• 
Terms of Use 
• 
Privacy Policy 
• 
Help 
• 
LOOP-MIND copyright 
The footer must remain at the bottom using the same visual treatment as the reference. 
 
34. Important Boundary 
The Interviews page should not generate interview questions simply because the recruiter navigates 
to this page. 
The generation occurs through the previously defined recruitment workflow. 
The Interviews page: 
• 
Displays saved generated questions. 
• 
Allows the recruiter to inspect them. 
• 
Allows the recruiter to schedule the relevant interview. 
• 
Tracks interview status. 
• 
Shows interview-related recent activity. 
 
35. Final Page Flow 
Recruiter Dashboard 
        │ 
        └── Prepare Interview Questions 
                    │ 
                    ▼ 
              Interviews Page 
                    │ 
                    ├── Summary Cards 
                    │ 
                    ├── Search 
                    │ 
                    ├── Job Filter

## SOURCE PAGE 388

│ 
                    ├── Status Filter 
                    │ 
                    ├── Schedule Interview 
                    │ 
                    ├── Scheduled Interviews 
                    │       │ 
                    │       └── View Details 
                    │               │ 
                    │               └── Saved AI Questions 
                    │ 
                    └── Recent Activity 
And the navbar provides the second entry point: 
Recruiter Navbar 
      │ 
      └── Interviews 
              │ 
              ▼ 
       Interviews Page 
Non-negotiable implementation rule 
The uploaded Interviews screenshot is the visual reference. The functionality described above 
must be integrated into that exact page structure without changing the reference layout or 
introducing unrelated sections. 
LOOP-MIND — Company Intelligence, Skill Gap Analysis & Preparation Plan Specification 
1. Objective 
LOOP-MIND must compare a student's current profile against company intelligence data to 
determine: 
• 
What the student already knows 
• 
What the student still needs to learn 
• 
Skill gaps 
• 
Missing evidence 
• 
Current readiness alignment

## SOURCE PAGE 389

• 
Company-specific requirements 
• 
Requirement patterns 
• 
Major reasons behind the assessment 
• 
What the student should improve first 
• 
A personalized Preparation Plan 
• 
What changes when the student asks different What-If questions 
• 
How the analysis and plan should update when the student progresses or changes the target 
company 
The system must be dynamic and data-driven. 
It must not use permanently hardcoded skill-gap results or preparation plans. 
 
2. Company Intelligence Data 
LOOP-MIND must maintain a dedicated Company Intelligence Dataset. 
This dataset is the source used for company-specific analysis. 
The dataset must contain company intelligence such as: 
• 
Company information 
• 
Company requirements 
• 
Historical job requirements 
• 
Current job requirements 
• 
Successful candidate profiles 
• 
Requirement patterns 
• 
Role-specific requirements 
• 
Skill requirements 
• 
Experience expectations 
• 
Evidence expectations 
• 
Relevant project expectations 
• 
Other company-specific recruitment signals available in the dataset 
The dataset must be structured so that it can later be replaced with an actual company dataset 
without changing the overall Skill Gap / Preparation Plan architecture. 
 
3. Initial Dataset Requirement

## SOURCE PAGE 390

Until an actual company dataset is supplied, LOOP-MIND must use a generated realistic 
demonstration Company Intelligence Dataset. 
This dataset must be: 
• 
Structured 
• 
Consistent 
• 
Realistic 
• 
Sufficient for company-specific analysis 
• 
Suitable for development/testing 
• 
Stored persistently 
• 
Replaceable later 
Important 
The generated dataset must be treated as demo/synthetic company intelligence, not as proprietary 
or officially sourced company data. 
When the actual company dataset becomes available, it must be possible to replace the generated 
dataset with the real dataset. 
 
4. Dataset Replacement Architecture 
The Company Intelligence Dataset must be separated from the application logic. 
Company Intelligence Dataset 
          ↓ 
Data Processing / Validation 
          ↓ 
Company Intelligence Layer 
          ↓ 
ML / Analysis Layer 
          ↓ 
Skill Gap Analysis 
          ↓ 
What-If Analysis 
          ↓ 
Preparation Plan 
Replacing the dataset should therefore not require rewriting:

## SOURCE PAGE 391

• 
Student Portal 
• 
Skill Gap page 
• 
Preparation Plan page 
• 
What-If interface 
• 
Progress tracking 
• 
Historical plan records 
Only the underlying company intelligence source should be replaceable. 
 
5. Student Data Source 
The second major input is the student's profile data. 
The system must use the student's existing account/profile information. 
Relevant student information can include: 
• 
Academic information 
• 
Academic year 
• 
Academic performance 
• 
Skills 
• 
Skill proficiency 
• 
Learning status 
• 
Experience 
• 
Projects 
• 
Certifications 
• 
Coding experience 
• 
Professional links 
• 
Resume 
• 
Career and placement information 
• 
Learning and preparation information 
• 
Interview/assessment information 
• 
Other profile information already captured by LOOP-MIND 
The system must compare the student's available information against the selected company's 
intelligence data.

## SOURCE PAGE 392

6. Core Comparison Engine 
The central analysis must compare: 
Company Intelligence 
        VS 
Student Profile 
The result must identify the difference between: 
Company expects 
and 
Student currently has 
This comparison drives both: 
• 
Skill Gap Analysis 
• 
Preparation Plan 
 
7. Skill Gap Analysis 
When a student selects a target company/role, LOOP-MIND must analyze the available company 
intelligence and student data. 
The Skill Gap page must dynamically display the resulting analysis. 
The analysis must determine, where supported by the available data: 
7.1 Existing Knowledge 
Skills and evidence the student already possesses that align with the company requirements. 
 
7.2 Skills Still Required 
Skills required by the selected company/role that are not sufficiently represented in the student's 
current profile. 
 
7.3 Skill Gaps 
Specific differences between the student's current capability/evidence and the company 
requirement. 
Example: 
Company Requirement: 
Advanced Data Structures & Algorithms

## SOURCE PAGE 393

Student: 
Intermediate Data Structures & Algorithms 
 
Result: 
Skill Gap identified 
The actual result must come from the comparison rather than being hardcoded. 
 
7.4 Missing Evidence 
The system must separately identify cases where the student may have a skill but lacks sufficient 
supporting evidence. 
Examples of evidence sources include: 
• 
Projects 
• 
Certifications 
• 
Resume evidence 
• 
Relevant experience 
• 
Other student profile evidence 
A missing-evidence condition must not automatically be treated as the same thing as a missing skill. 
 
7.5 Current Readiness Alignment 
The system must determine how closely the student's current profile aligns with the selected 
company/role. 
This must be dynamically calculated from the available comparison data. 
 
7.6 Major Reason Behind Assessment 
The Skill Gap Analysis must provide the major reasons supporting the assessment. 
For example, the reasoning can identify that the assessment is influenced by: 
• 
Required skills not yet demonstrated 
• 
Required proficiency not reached 
• 
Missing project evidence 
• 
Missing certification/evidence where relevant 
• 
Other company-specific requirements represented in the dataset 
The reason must be derived from the actual comparison.

## SOURCE PAGE 394

8. Target Company Context 
The Skill Gap Analysis must operate against the student's selected target company. 
The selected company must therefore be part of the analysis context. 
Conceptually: 
Student 
  + 
Target Company 
  + 
Target Role 
  + 
Company Intelligence 
       ↓ 
Skill Gap Analysis 
Changing the target company must cause a new company-specific analysis. 
 
9. Target Role Context 
Where the student selects a specific target role, the analysis must also consider the role-specific 
requirements. 
Therefore: 
Target Company + Target Role 
        ↓ 
Relevant Company Requirements 
        ↓ 
Student Comparison 
        ↓ 
Skill Gap 
The analysis must not blindly compare the student against unrelated roles. 
 
10. What-If Analysis 
The Skill Gap page must contain the previously defined:

## SOURCE PAGE 395

Try What-If Analysis 
When clicked, a centered card/modal must open on the page. 
The card must contain a text input where the student can enter a natural-language What-If question. 
Example: 
What if I learn Generative AI? 
The student can also ask other questions such as: 
What should I improve first to become ready for Company X? 
The system must analyze the student's question against the available company intelligence and 
student data. 
 
11. What-If Analysis — Example 
For: 
What if I learn Generative AI? 
The system should determine, based on the available company/role intelligence: 
• 
How Generative AI relates to the target role 
• 
Whether it is relevant to the company's requirements 
• 
What demand/significance it has within the available company intelligence 
• 
Which related skills may become important 
• 
What roles or opportunities represented in the data may be relevant 
• 
How the student's readiness could change 
• 
What additional preparation may become relevant 
Only information supported by the company intelligence and student data should be presented as 
factual. 
 
12. Different What-If Questions 
The What-If system must not be restricted to one fixed question. 
The student can ask questions such as: 
What if I learn Generative AI? 
 
What if I improve DSA first? 
 
What should I improve first to become ready for Company X?

## SOURCE PAGE 396

What if I complete this skill? 
 
What if I add a project in this domain? 
The system must interpret the student's question and perform a relevant comparison using the 
available data. 
 
13. What-If Result 
The result must appear within the same centered card/modal. 
It must not navigate the student away from the Skill Gap page. 
The result must be based on: 
Current Student State 
        + 
What-If Change 
        + 
Company Intelligence 
        ↓ 
Projected Comparison 
The What-If result must therefore distinguish between the student's current state and the 
hypothetical state. 
 
14. Preparation Plan Generation 
The Preparation Plan must be generated from the Skill Gap analysis. 
The relationship is: 
Company Intelligence 
        + 
Student Profile 
        ↓ 
Skill Gap Analysis 
        ↓ 
Prioritized Gaps 
        ↓

## SOURCE PAGE 397

Preparation Plan 
The Preparation Plan must therefore be personalized for the individual student. 
 
15. Different Students = Different Plans 
The system must not generate one universal preparation plan. 
Different students can have: 
• 
Different existing skills 
• 
Different proficiency levels 
• 
Different projects 
• 
Different evidence 
• 
Different academic stages 
• 
Different target companies 
• 
Different target roles 
• 
Different gaps 
• 
Different progress 
Therefore, their preparation plans must differ accordingly. 
 
16. Different Plan Durations 
The generated plan may have different durations depending on the student's actual requirements 
and available context. 
Examples include: 
• 
Shorter preparation plans 
• 
Longer preparation plans 
• 
Multi-month plans 
• 
Approximately one-year plans 
The duration must be determined from the student's situation and requirements rather than forcing 
every student into the same fixed duration. 
 
17. Plan Content 
The Preparation Plan must focus on the student's identified gaps and required preparation. 
The existing Preparation Plan page structure remains the reference UI.

## SOURCE PAGE 398

The generated plan must populate the existing dynamic sections, including the plan information 
already represented by the Preparation Plan reference layout. 
The system must not generate unrelated content merely to fill the page. 
 
18. Plan Updating 
Preparation Plans are versioned and updateable. 
A student's plan must not be treated as permanently fixed. 
The plan must be regenerated when meaningful inputs change. 
Examples: 
Student progress changes 
DSA progress 
      ↓ 
DSA completed 
      ↓ 
Skill Gap updated 
      ↓ 
Preparation Plan regenerated 
Target company changes 
Company X 
    ↓ 
Student changes target 
    ↓ 
Company Y 
    ↓ 
New Company Intelligence comparison 
    ↓ 
New Skill Gap Analysis 
    ↓ 
New Preparation Plan 
 
19. Progress-Based Regeneration

## SOURCE PAGE 399

If the student completes a previously identified requirement, the system must update the analysis. 
Example: 
Previous Skill Gap: 
Data Structures & Algorithms 
 
Student completes DSA 
        ↓ 
Progress reaches completion 
        ↓ 
Current student state changes 
        ↓ 
Skill Gap recalculated 
        ↓ 
Remaining gaps recalculated 
        ↓ 
Preparation Plan regenerated 
The completed item should not continue to appear as an unresolved gap merely because it existed in 
the previous plan. 
 
20. Regeneration After Student Updates 
If the student updates relevant profile information, the system must use the updated information 
for future analysis. 
Relevant changes may include: 
• 
Skill updates 
• 
Skill proficiency changes 
• 
Project additions 
• 
Certification additions 
• 
Evidence updates 
• 
Learning progress 
• 
Other relevant profile changes 
The system must not continue using stale student information for a newly generated plan.

## SOURCE PAGE 400

21. Target Company Change 
If the student changes: 
Target Company A 
        ↓ 
Target Company B 
the system must perform a new analysis. 
The new analysis must use Company B's intelligence rather than simply modifying the old Company 
A plan. 
Therefore: 
New Target Company 
        ↓ 
New Company Requirements 
        ↓ 
New Student Comparison 
        ↓ 
New Skill Gaps 
        ↓ 
New Preparation Plan 
 
22. Previous Plans Must Be Preserved 
When a plan is regenerated, the previous plan must not be silently overwritten. 
Previous plans must remain available as historical records. 
Example: 
Plan Version 1 
Company X 
        ↓ 
Student Progress 
        ↓ 
Plan Version 2 
Company X 
        ↓

## SOURCE PAGE 401

Target Company Changed 
        ↓ 
Plan Version 3 
Company Y 
All versions remain stored. 
 
23. Plan History 
The student's historical plan information must be available through the My Profile / My Progress 
area, according to the portal structure already defined. 
A dedicated historical record/list should contain each generated plan/version. 
Each historical record should retain the information required to distinguish one plan generation 
from another. 
At minimum, the history must preserve the relationship between: 
• 
Student 
• 
Target company 
• 
Target role 
• 
Plan version 
• 
Generation/update event 
• 
Plan contents 
 
24. Change History 
The system must preserve what changed between plan generations. 
For example: 
Previous Plan 
      ↓ 
Student completed DSA 
      ↓ 
New Plan 
      ↓ 
Change recorded 
Or: 
Previous Target Company:

## SOURCE PAGE 402

Company X 
 
New Target Company: 
Company Y 
 
Change recorded 
The purpose is to ensure that the student's previous preparation history is not lost. 
 
25. Plan Versioning Principle 
Every regeneration should create a new plan version rather than destroying the previous plan. 
Conceptually: 
Preparation Plan 
├── Version 1 
├── Version 2 
├── Version 3 
└── Version 4 
The newest applicable version becomes the student's current plan. 
Older versions remain historical. 
 
26. ML / Intelligence Layer 
The Company Intelligence Dataset and Student Profile Dataset feed the analysis/ML layer. 
The intended architecture is: 
Company Intelligence Dataset 
              + 
Student Profile Dataset 
              ↓ 
       Data Preparation 
              ↓ 
      Feature Extraction 
              ↓ 
      ML / Analysis Model

## SOURCE PAGE 403

↓ 
       Requirement Matching 
              ↓ 
       Gap Identification 
              ↓ 
      Readiness Assessment 
              ↓ 
       Recommendation Layer 
              ↓ 
       Preparation Plan 
 
27. ML Training Dataset 
Until the real Company Intelligence Dataset is supplied, the generated synthetic Company 
Intelligence Dataset can serve as the development/training dataset. 
The dataset must be structured consistently so that the ML pipeline can consume it. 
When an actual dataset is provided later: 
Synthetic Dataset 
       ↓ 
Replace 
       ↓ 
Actual Company Dataset 
       ↓ 
Data Validation 
       ↓ 
ML / Analysis Pipeline 
The application logic should remain unchanged wherever possible. 
 
28. Dataset Storage 
The Company Intelligence Dataset must be stored separately from frontend UI data. 
Conceptually: 
company-intelligence/

## SOURCE PAGE 404

companies/ 
    roles/ 
    requirements/ 
    historical-requirements/ 
    successful-candidates/ 
    requirement-patterns/ 
    current-jobs/ 
The exact physical storage technology should follow the project's existing backend/database 
architecture rather than introducing an unrelated storage system. 
 
29. Data Validation 
Before company intelligence is used for analysis, it must be validated. 
The system must ensure that required fields and relationships are structurally valid. 
Invalid or incomplete records must not silently produce fabricated analysis. 
If required information is unavailable, the system should indicate that the assessment is limited by 
the available data. 
 
30. No Hallucinated Company Intelligence 
The analysis layer must not invent company requirements and present them as real company facts. 
There are two clearly different cases: 
Synthetic development data 
Explicitly generated for LOOP-MIND development/testing. 
Actual company data 
Provided/imported later by the project. 
The system must preserve that distinction. 
 
31. Dynamic Data Requirement 
The following must be dynamic: 
• 
Selected company 
• 
Selected role 
• 
Company requirements 
• 
Historical requirements

## SOURCE PAGE 405

• 
Requirement patterns 
• 
Student skills 
• 
Student proficiency 
• 
Student evidence 
• 
Skill gaps 
• 
Missing evidence 
• 
Readiness 
• 
Assessment reasons 
• 
What-If results 
• 
Preparation plans 
• 
Plan duration 
• 
Plan progress 
• 
Plan versions 
• 
Plan history 
• 
Change history 
No static mock result should permanently drive the production UI. 
 
32. End-to-End Student Flow 
Student Login 
      ↓ 
Student Profile 
      ↓ 
Student selects Target Company 
      ↓ 
Student selects Target Role 
      ↓ 
Company Intelligence Retrieved 
      ↓ 
Student Profile Retrieved 
      ↓ 
Comparison / ML Analysis

## SOURCE PAGE 406

↓ 
Skill Gap Analysis 
      │ 
      ├── Existing Skills 
      ├── Required Skills 
      ├── Skill Gaps 
      ├── Missing Evidence 
      ├── Readiness Alignment 
      └── Assessment Reasons 
      │ 
      ▼ 
Student can use What-If Analysis 
      │ 
      ▼ 
Personalized Preparation Plan 
      │ 
      ▼ 
Student progresses 
      │ 
      ▼ 
Profile / progress updated 
      │ 
      ▼ 
Skill Gap recalculated 
      │ 
      ▼ 
New Preparation Plan Version 
      │ 
      ▼ 
Previous Plan preserved in history

## SOURCE PAGE 407

33. Company Change Flow 
Target Company A 
       ↓ 
Company A Intelligence 
       ↓ 
Skill Gap A 
       ↓ 
Preparation Plan A 
       ↓ 
Student changes target 
       ↓ 
Target Company B 
       ↓ 
Company B Intelligence 
       ↓ 
New comparison 
       ↓ 
Skill Gap B 
       ↓ 
Preparation Plan B 
       ↓ 
Plan A retained as historical version 
 
34. Student Progress Flow 
Current Plan 
     ↓ 
Student works on DSA 
     ↓ 
DSA completed 
     ↓ 
Student profile/progress updated

## SOURCE PAGE 408

↓ 
Current state recalculated 
     ↓ 
DSA gap resolved 
     ↓ 
Remaining gaps reprioritized 
     ↓ 
New Preparation Plan generated 
     ↓ 
Previous plan preserved 
 
35. What-If Flow 
Skill Gap Page 
      ↓ 
Try What-If Analysis 
      ↓ 
Centered What-If Card 
      ↓ 
Student enters question 
      ↓ 
"What if I learn Generative AI?" 
      ↓ 
Question interpreted 
      ↓ 
Company Intelligence + Student Data 
      ↓ 
Hypothetical comparison 
      ↓ 
Result displayed in same centered card 
For: 
What should I improve first to become ready for Company X?

## SOURCE PAGE 409

the system should similarly evaluate the student's current state and identify the highest-priority 
improvement supported by the available data. 
 
36. Preparation Plan Page Relationship 
The existing Preparation Plan page remains the destination for the generated preparation plan. 
The Skill Gap page should not display the complete Preparation Plan as a replacement for the 
Preparation Plan page. 
The previously defined behavior remains: 
• 
Get Personalized Plan generates/prepares the plan. 
• 
The generated plan is stored. 
• 
The student remains on the appropriate workflow/page rather than being unnecessarily 
redirected to a separate plan-generation screen. 
• 
The generated plan is ultimately displayed on the Preparation Plan page. 
• 
The Preparation Plan page displays the current applicable plan. 
 
37. Current vs Historical Plan 
The system must distinguish: 
Current Plan 
The latest applicable preparation plan for the student's current target and current profile state. 
Historical Plans 
Previous generated versions retained for progress/history. 
Historical Plans 
      ↓ 
Version 1 
Version 2 
Version 3 
      ↓ 
Current Plan 
Version 4 
 
38. My Profile / My Progress History 
The existing student profile/progress area must preserve the student's preparation history.

## SOURCE PAGE 410

The historical plan/change information must be connected to the student's account rather than 
being temporary frontend state. 
If the student logs out and returns later, the relevant current and historical records must still exist. 
 
39. Replaceable Intelligence Source 
The architecture must intentionally support this future workflow: 
TODAY 
 
Generated Synthetic Company Dataset 
              ↓ 
Development / Testing 
              ↓ 
ML / Analysis 
              ↓ 
Skill Gap 
              ↓ 
Preparation Plan 
 
 
LATER 
 
Actual Company Dataset 
              ↓ 
Replace Synthetic Dataset 
              ↓ 
Same Processing Architecture 
              ↓ 
ML / Analysis 
              ↓ 
Skill Gap 
              ↓

## SOURCE PAGE 411

Preparation Plan 
The system must therefore avoid coupling the UI directly to the temporary synthetic dataset. 
 
40. Reference Page Responsibilities 
Skill Gap Page 
Responsible for displaying: 
• 
Company/role context 
• 
Skill Gap Analysis 
• 
Current readiness/alignment 
• 
Missing skills 
• 
Missing evidence 
• 
Assessment reasoning 
• 
What-If Analysis 
Preparation Plan Page 
Responsible for displaying: 
• 
Current personalized preparation plan 
• 
Plan progress 
• 
Plan structure 
• 
Plan categories/items 
• 
Current preparation status 
• 
Updated generated plan 
My Profile / My Progress 
Responsible for retaining: 
• 
Student profile 
• 
Progress 
• 
Historical preparation-plan versions 
• 
Relevant plan-change history 
 
41. Core Data Relationship 
The complete system should conceptually maintain: 
Student

## SOURCE PAGE 412

│ 
   ├── Profile 
   ├── Skills 
   ├── Projects 
   ├── Certifications 
   ├── Resume 
   ├── Evidence 
   └── Progress 
          │ 
          ▼ 
     Student State 
          │ 
          │ 
          ▼ 
Target Company ──→ Company Intelligence 
          │ 
          ▼ 
    Comparison Engine 
          │ 
          ├── Skill Gaps 
          ├── Missing Evidence 
          ├── Readiness 
          └── Assessment Reasons 
          │ 
          ▼ 
   What-If Analysis 
          │ 
          ▼ 
 Preparation Plan 
          │ 
          ▼

## SOURCE PAGE 413

Plan Version History 
 
42. Non-Negotiable Requirements 
1. Company intelligence must be data-driven. 
2. A temporary synthetic dataset must be generated for development until an actual dataset 
is supplied. 
3. The synthetic dataset must be replaceable later. 
4. Student data must come from the student's actual profile/progress data. 
5. Company data and student data must be compared before generating Skill Gap results. 
6. Skill gaps must be dynamically determined. 
7. Missing evidence must be distinguished from skill gaps where the data supports that 
distinction. 
8. Readiness must be based on the comparison, not a permanently hardcoded number. 
9. Assessment reasoning must come from the comparison. 
10. What-If Analysis must operate from the current student state and company intelligence. 
11. What-If results must appear in the centered card/modal on the Skill Gap page. 
12. Preparation Plans must be personalized. 
13. Different students can receive different plans. 
14. Plans can change as the student's progress changes. 
15. Changing the target company must trigger a new company-specific analysis. 
16. Completed requirements must affect subsequent analysis. 
17. Regenerated plans must create new versions. 
18. Previous plans must not be silently deleted. 
19. Plan history must be retained. 
20. The system must remain dynamic rather than relying on permanent hardcoded demo 
results. 
21. The generated development dataset must be clearly treated as synthetic/demo 
intelligence until replaced by actual company data. 
22. No unsupported company facts should be fabricated and presented as real data. 
23. The existing Skill Gap and Preparation Plan reference layouts remain unchanged; this 
intelligence layer populates those existing UI structures rather than redesigning them. 
LOOP-MIND — FINAL BUILD TECHNOLOGY & AI SPECIFICATION 
1. Core Development Direction

## SOURCE PAGE 414

LOOP-MIND will be built as a Python-first full-stack, AI-driven student placement and recruitment 
platform. 
The system contains two completely separate portals: 
• 
Student Portal 
• 
Recruiter Portal 
Both portals share the same backend infrastructure but have separate roles, permissions, 
workflows, and UI experiences. 
The frontend uses React because the portal UI requires component-based interaction, while all 
backend, Applied AI, ML and DL logic will be Python-first. The existing specification also defines the 
architecture as Python-First Full-Stack + Applied AI. 
 
2. FINAL TECH STACK 
Frontend 
• 
React.js 
• 
TypeScript 
• 
Vite 
• 
Tailwind CSS 
• 
shadcn/ui 
• 
React Flow 
• 
Recharts 
Purpose 
• 
Student Portal UI 
• 
Recruiter Portal UI 
• 
Dashboards 
• 
Skill Gap page 
• 
Preparation Plan page 
• 
My Profile page 
• 
Jobs 
• 
Candidates 
• 
Interviews 
• 
AI workflow visualization 
• 
Charts and progress visualization

## SOURCE PAGE 415

This matches the existing project specification. 
JavaScript rule 
Do not use JavaScript for backend or AI development. 
Frontend JavaScript is unavoidable because React runs in the JavaScript ecosystem, so use: 
TypeScript instead of plain JavaScript 
Keep frontend scripting minimal and keep all business logic, AI logic, ML/DL processing and APIs in 
Python. 
 
3. Backend 
Main Stack 
• 
Python 
• 
FastAPI 
• 
Pydantic 
• 
SQLAlchemy 
• 
JWT 
• 
OTP Authentication 
• 
REST APIs 
The existing specification already defines this backend stack. 
Backend Responsibilities 
• 
Authentication 
• 
Student authentication 
• 
Recruiter authentication 
• 
OTP verification 
• 
Role identification 
• 
Authorization 
• 
Student profile management 
• 
Recruiter profile management 
• 
Job management 
• 
Job applications 
• 
Candidate management 
• 
Interview management

## SOURCE PAGE 416

• 
Skill Gap data 
• 
Preparation Plan data 
• 
Progress tracking 
• 
AI service communication 
• 
ML/DL model communication 
• 
Database operations 
• 
File handling 
• 
Resume handling 
• 
AI workflow state management 
 
4. Database Architecture 
Primary Database 
SQLite 
Use SQLite for all structured application data. 
SQLite stores 
• 
Students 
• 
Recruiters 
• 
Authentication records 
• 
OTP-related records 
• 
Student profiles 
• 
Academic information 
• 
Skills 
• 
Projects 
• 
Certifications 
• 
Coding experience 
• 
Resumes metadata 
• 
Jobs 
• 
Job requirements 
• 
Applications 
• 
AI matching results 
• 
AI status

## SOURCE PAGE 417

• 
Human approval/disapproval 
• 
Disapproval reasons 
• 
Interviews 
• 
Interview schedules 
• 
Interview questions 
• 
Preparation Plans 
• 
Skill Gaps 
• 
What-If results 
• 
Progress 
• 
Historical records 
• 
Recruitment outcomes 
The project specification explicitly defines SQLite for student, recruiter, job, application and outcome 
data. 
Vector Database 
Qdrant Local 
Qdrant is required specifically for semantic/vector retrieval used by RAG. 
It stores embeddings for: 
• 
Company knowledge 
• 
Job requirements 
• 
Historical recruitment information 
• 
Successful candidate information 
• 
Student evidence 
• 
Skill knowledge 
• 
Interview knowledge 
• 
Preparation resources 
• 
Recruitment outcomes 
The existing architecture specifies SQLite + Qdrant. 
MongoDB will not be used. 
 
5. Applied AI 
Main Framework

## SOURCE PAGE 418

LangChain 
LangChain is the core Applied AI framework. 
The AI layer will be built using: 
• 
Python 
• 
LangChain 
• 
RAG 
• 
AI Agents 
• 
Multi-Agent Systems 
• 
Tool Use 
• 
Function Calling 
• 
MCP where required 
The existing specification explicitly establishes LangChain as the core AI framework. 
 
6. LLM 
Use a free/local LLM during development. 
Priority: 
1. Local LLM where practical 
2. Free LLM providers where required 
The LLM should be accessed through the LangChain layer so the underlying model can be changed 
without redesigning the entire application. 
 
7. RAG 
RAG = Required 
RAG will connect the AI agents to the project's recruitment and company knowledge. 
Flow 
Company / Recruitment / Student Data 
                ↓ 
          Data Processing 
                ↓ 
            Embeddings 
                ↓

## SOURCE PAGE 419

Qdrant 
                ↓ 
               RAG 
                ↓ 
          LangChain Agents 
                ↓ 
        AI Analysis / Decision 
RAG will support: 
• 
Company recruitment history 
• 
Job requirements 
• 
Successful candidate characteristics 
• 
Student evidence 
• 
Historical recruitment outcomes 
• 
Assessment topics 
• 
Interview information 
• 
Preparation resources 
• 
Skill-gap knowledge 
These are the defined RAG use cases in the existing specification. 
 
8. AI AGENTS — EXACTLY 12 
No unnecessary extra agents. 
Student / Company Intelligence 
1. Company Intelligence Agent 
Analyzes: 
• 
Company requirements 
• 
Historical requirements 
• 
Current roles 
• 
Recruitment patterns 
• 
Successful candidate characteristics 
• 
Historical recruitment outcomes

## SOURCE PAGE 420

2. Student Skill Analysis Agent 
Analyzes: 
• 
Student skills 
• 
Academics 
• 
Projects 
• 
Certifications 
• 
Coding experience 
• 
Evidence 
• 
Current learning status 
 
3. Placement Readiness Agent 
Compares: 
Student Profile 
       + 
Company Intelligence 
       + 
Target Job 
       ↓ 
Placement Readiness 
Determines the student's current readiness for a company/role. 
 
4. Skill-Gap Analysis Agent 
Identifies: 
• 
Missing skills 
• 
Weak skills 
• 
Missing evidence 
• 
Requirement mismatches 
• 
Readiness gaps 
• 
Priority gaps 
• 
Reasons behind the assessment

## SOURCE PAGE 421

5. Preparation Plan Agent 
Generates an individualized preparation plan based on the detected gaps. 
Different students can receive different plans. 
Plans can be: 
• 
Short-term 
• 
Medium-term 
• 
Long-term 
The plan must update when the student's skills/progress or target company changes. 
 
6. What-If Analysis Agent 
Handles questions such as: 
What should I improve first to become ready for Company X? 
What happens if I learn Generative AI? 
What if I complete DSA? 
What should I improve first? 
The agent uses the student's current state and company requirements to generate the analysis. 
The first six agents are defined as the student/company intelligence side of the system. 
 
9. RECRUITMENT AI AGENTS 
7. Resume Parser Agent 
Extracts structured information from student resumes. 
Input: 
Resume PDF 
Output: 
Skills 
Education 
Projects 
Experience 
Certifications 
Contact Information 
Other Relevant Evidence

## SOURCE PAGE 422

8. Embedding Agent 
Converts relevant recruitment/student/company information into embeddings for semantic 
retrieval. 
 
9. Matching Agent 
Compares: 
Candidate Profile 
        VS 
Job Requirements 
and determines the degree of alignment. 
 
10. Shortlisting Agent 
Uses: 
• 
Resume information 
• 
Job requirements 
• 
Matching results 
• 
Relevant evidence 
to produce the AI Status: 
• 
AI Shortlisted 
• 
AI Hold 
• 
AI Rejected 
The recruiter then performs human cross-check/approval. 
 
11. Interview Agent 
After recruiter approval: 
• 
Identifies the specific job role 
• 
Understands role requirements 
• 
Generates role-specific interview questions 
• 
Stores generated questions 
• 
Makes them available from the Recruiter Interviews page

## SOURCE PAGE 423

12. Email Agent 
Handles recruitment communication such as: 
• 
Interview invitation 
• 
Interview information 
• 
Interview-related email 
• 
Candidate communication 
The existing specification defines these exact 12 specialized agents. 
 
10. MULTI-AGENT SYSTEMS 
Multi-Agent System 1 — Student Intelligence 
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
Purpose: 
Determine what a student needs to become ready for a target company and role. 
 
11. MULTI-AGENT SYSTEM 2 — AI Recruitment 
Resume Parser Agent 
        ↓ 
Embedding Agent 
        ↓ 
Matching Agent

## SOURCE PAGE 424

↓ 
Shortlisting Agent 
        ↓ 
Human Approval 
        ↓ 
Interview Agent 
        ↓ 
Email Agent 
Purpose: 
Process a candidate application from resume analysis through human approval and interview 
invitation. 
 
12. OVERALL CLOSED-LOOP SYSTEM 
Student Intelligence 
        ↓ 
Placement Readiness 
        ↓ 
Student Applies 
        ↓ 
AI Recruitment 
        ↓ 
Recruitment Outcome 
        ↓ 
Skill Gaps / Successful Candidate Intelligence 
        ↓ 
Company Intelligence 
        ↓ 
Student Intelligence 
        ↺ 
This creates the project's overall closed-loop intelligence architecture.

## SOURCE PAGE 425

13. HUMAN-IN-THE-LOOP 
AI does not make the final recruitment approval. 
AI Shortlisting 
       ↓ 
Recruiter Review 
       ↓ 
Approve / Disapprove 
Approve 
Human Approval 
      ↓ 
Interview Agent 
      ↓ 
Role-specific Questions 
      ↓ 
Interview Invitation 
      ↓ 
Email Agent 
Disapprove 
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
This is essential to the project's closed-loop recruitment model.

## SOURCE PAGE 426

14. ML 
Framework 
scikit-learn 
Data Processing 
pandas + NumPy 
The existing specification explicitly defines pandas/NumPy for data processing and scikit-learn for 
ML. 
ML can be used for 
• 
Recruitment pattern analysis 
• 
Candidate/job feature analysis 
• 
Readiness-related prediction 
• 
Historical recruitment analysis 
• 
Candidate matching support 
• 
Outcome analysis 
• 
Skill-gap pattern analysis 
ML should support the AI system rather than unnecessarily replace LangChain agents. 
 
15. DL 
Framework 
PyTorch 
Use DL where learned representations/models provide value beyond conventional ML. 
The project specification explicitly defines PyTorch for Deep Learning. 
 
16. ML/DL EVALUATION 
Use: 
• 
scikit-learn metrics 
• 
Custom evaluation 
• 
Pytest 
• 
AI Evaluation Dataset 
The evaluation dataset is explicitly part of the AI testing setup.

## SOURCE PAGE 427

17. DATASET ARCHITECTURE 
There are 8 core dataset categories. 
1. Company & Job Requirements Dataset 
Contains: 
• 
Companies 
• 
Roles 
• 
Required skills 
• 
Technical concepts 
• 
Job requirements 
• 
Recruitment requirements 
2. Recruitment Process & Historical Outcomes Dataset 
Contains: 
• 
Recruitment stages 
• 
Assessment results 
• 
Selection outcomes 
• 
Rejection outcomes 
• 
Historical recruitment patterns 
3. Candidate / Student Profile Dataset 
Contains: 
• 
Skills 
• 
Academics 
• 
Projects 
• 
Certifications 
• 
Coding experience 
• 
Evidence 
4. Successful Candidate Dataset 
Contains characteristics of candidates who were selected/placed. 
5. Skill & Evidence Dataset 
Contains: 
• 
Skills 
• 
Projects

## SOURCE PAGE 428

• 
Certifications 
• 
Assessments 
• 
Evidence 
6. Interview & Assessment Dataset 
Contains: 
• 
Interview questions 
• 
Assessment topics 
• 
Evaluation criteria 
• 
Rubrics 
7. Preparation & Learning Dataset 
Contains: 
• 
Skills to learn 
• 
Preparation resources 
• 
Preparation strategies 
• 
Learning plans 
8. AI Evaluation Dataset 
Used to test: 
• 
Resume parsing 
• 
Matching 
• 
Shortlisting 
• 
Skill-gap analysis 
• 
Other AI outputs 
These eight categories are already defined in the project specification. 
 
18. COMPANY DATASET DEVELOPMENT MODE 
Until the user provides a real company dataset: 
Generated realistic company data 
            ↓ 
Stored 
            ↓ 
Processed

## SOURCE PAGE 429

↓ 
ML/DL 
            ↓ 
Embeddings 
            ↓ 
Qdrant 
            ↓ 
RAG 
            ↓ 
AI Agents 
When an actual company dataset becomes available: 
Existing Generated Dataset 
          ↓ 
Replace / Update 
          ↓ 
Real Company Dataset 
          ↓ 
Same Processing Pipeline 
The architecture therefore does not need to be redesigned when real company data is introduced. 
 
19. n8n — REMOVE FROM CORE ARCHITECTURE 
Decision: Do NOT make n8n a required core technology. 
The previous specification included n8n webhooks as an automation layer. 
However, for this project it adds an unnecessary external workflow layer because the required 
workflows can be controlled directly through: 
• 
FastAPI 
• 
Python services 
• 
LangChain 
• 
Background processing 
• 
SQLite 
• 
Qdrant

## SOURCE PAGE 430

Why remove n8n? 
The project's core workflows are application-controlled: 
Student Application 
        ↓ 
FastAPI 
        ↓ 
Python AI Services 
        ↓ 
LangChain Agents 
        ↓ 
Database 
and: 
Recruiter Approval 
        ↓ 
FastAPI 
        ↓ 
Interview Agent 
        ↓ 
Email Agent 
        ↓ 
Email 
Adding n8n would introduce another system to configure, maintain and debug without being 
necessary for the core functionality. 
Therefore: 
n8n is removed from the required core stack. 
No replacement AI agent is added. 
 
20. MCP 
MCP is not an AI agent. 
It is a standardized tool/context access layer. 
For the initial development, MCP should not be forced into every agent.

## SOURCE PAGE 431

Use it only where standardized external tool access actually becomes necessary. 
The core system remains: 
LangChain 
   ↓ 
Agents 
   ↓ 
Tools / Function Calling 
   ↓ 
SQLite / Qdrant / Services 
 
21. FUNCTION CALLING 
Agents use function calling to access controlled tools. 
Example: 
Student: 
"What should I improve first for Company X?" 
              ↓ 
Placement Readiness Agent 
              ↓ 
Function Calling 
          ↙       ↘ 
 get_student()   get_company() 
      ↓               ↓ 
   SQLite          Qdrant 
          ↘       ↙ 
             RAG 
              ↓ 
      Readiness Analysis 
              ↓ 
          Final Result 
Function calling is used for: 
• 
Database retrieval

## SOURCE PAGE 432

• 
Qdrant retrieval 
• 
Search 
• 
Job search 
• 
Resume processing 
• 
Readiness calculations 
• 
Skill-gap calculations 
• 
Rules evaluation 
• 
AI service operations 
• 
Email operations 
 
22. AUTHENTICATION 
Student 
Student Number / Mobile Number 
          ↓ 
        OTP 
          ↓ 
Student Authentication 
          ↓ 
Student Portal 
Recruiter 
Registered Recruiter Mobile Number 
          ↓ 
        OTP 
          ↓ 
Recruiter Identification 
          ↓ 
Recruiter Portal 
The authentication system must identify the account type after verification and route the user to the 
correct portal. 
OTP Verified 
      ↓

## SOURCE PAGE 433

Account Type 
   ↙       ↘ 
Student   Recruiter 
   ↓          ↓ 
Student    Recruiter 
Portal      Portal 
 
23. FILE & STORAGE ARCHITECTURE 
Use the repository's dedicated storage/ directory for: 
• 
Resumes 
• 
Documents 
• 
Uploaded files 
• 
Dataset files 
• 
Other application storage 
The existing repository specification defines storage/ for files, documents, resumes, datasets and 
stored data. 
 
24. FINAL REPOSITORY STRUCTURE 
LOOP-MIND/ 
│ 
├── frontend/ 
│   ├── website/ 
│   │   ├── student/ 
│   │   ├── recruiter/ 
│   │   ├── components/ 
│   │   ├── layouts/ 
│   │   ├── pages/ 
│   │   ├── services/ 
│   │   └── ... 
│   │ 
│   └── ...

## SOURCE PAGE 434

│ 
├── backend/ 
│   ├── api/ 
│   ├── auth/ 
│   ├── models/ 
│   ├── schemas/ 
│   ├── services/ 
│   ├── routes/ 
│   └── ... 
│ 
├── databases/ 
│   ├── sqlite/ 
│   ├── qdrant/ 
│   └── ... 
│ 
├── storage/ 
│   ├── resumes/ 
│   ├── documents/ 
│   ├── datasets/ 
│   └── ... 
│ 
├── AI services/ 
│   ├── agents/ 
│   ├── multi_agent/ 
│   ├── rag/ 
│   ├── tools/ 
│   ├── function_calling/ 
│   ├── embeddings/ 
│   ├── resume_parser/ 
│   ├── matching/ 
│   ├── shortlisting/

## SOURCE PAGE 435

│   ├── interview/ 
│   ├── email/ 
│   └── ... 
│ 
├── ML and DL/ 
│   ├── datasets/ 
│   ├── preprocessing/ 
│   ├── ml/ 
│   ├── dl/ 
│   ├── models/ 
│   ├── evaluation/ 
│   └── ... 
│ 
├── phase.md 
└── spec.md 
This keeps Applied AI separate from ML/DL, exactly as requested. The existing repository definition 
similarly separates AI services/, ML and DL/, databases/, storage/, frontend/, and backend/. 
 
25. DEVELOPMENT / QUALITY TOOLS 
• 
Git 
• 
GitHub 
• 
Pytest 
• 
Ruff 
• 
ESLint 
• 
Prettier 
• 
.env 
• 
Docker — optional for local development 
The existing specification lists these development and quality tools and defines development cost as 
₹0. 
 
26. FINAL TECHNOLOGY MAP 
                    LOOP-MIND

## SOURCE PAGE 436

│ 
        ┌───────────────┼────────────────┐ 
        ↓               ↓                ↓ 
    FRONTEND         BACKEND          DATABASE 
        │               │                │ 
 React + TS          Python            SQLite 
 Vite                FastAPI           Qdrant 
 Tailwind            Pydantic 
 shadcn/ui            SQLAlchemy 
 React Flow           JWT + OTP 
 Recharts 
        │               │ 
        └───────────────┼────────────────┘ 
                        ↓ 
                  APPLIED AI 
                        │ 
                    LangChain 
                        │ 
       ┌────────────────┼────────────────┐ 
       ↓                ↓                ↓ 
     Agents          Multi-Agent        RAG 
       │              Systems             │ 
       │                │               Qdrant 
       ↓                ↓                 │ 
 Function Calling   Workflows             ↓ 
       │                         AI Knowledge 
       └───────────────┬─────────────────┘ 
                       ↓ 
                     ML/DL 
                       │ 
              ┌────────┴────────┐

## SOURCE PAGE 437

↓                 ↓ 
        scikit-learn          PyTorch 
              │                 │ 
              └────────┬────────┘ 
                       ↓ 
                Historical / 
                Recruitment 
                Intelligence 
Final fixed stack 
Layer 
Technology 
Frontend 
React.js + TypeScript 
Build 
Vite 
UI 
Tailwind CSS + shadcn/ui 
Visualization 
React Flow + Recharts 
Backend 
Python + FastAPI 
Validation 
Pydantic 
ORM 
SQLAlchemy 
Authentication 
JWT + OTP 
Main Database 
SQLite 
Vector Database 
Qdrant Local 
Applied AI 
Python + LangChain 
RAG 
LangChain + Qdrant 
Agents 
12 specialized agents 
Multi-Agent 
2 functional systems 
Closed Loop 
1 overall system 
Embeddings 
Sentence Transformers 
ML 
scikit-learn 
DL 
PyTorch

## SOURCE PAGE 438

Layer 
Technology 
Data Processing 
pandas + NumPy 
AI Testing 
Pytest + Evaluation Dataset 
Code Quality 
Ruff + ESLint + Prettier 
Version Control 
Git + GitHub 
Containers 
Docker, optional 
Automation 
No n8n in core architecture 
MongoDB 
Not used 
Backend JavaScript Not used 
Development Cost ₹0 
This keeps the implementation aligned with the existing SDD while applying your latest decisions: 
Python-first backend/AI, LangChain as the main AI framework, SQLite as the primary database, 
Qdrant only for vector/RAG needs, exactly 12 required agents, 2 functional multi-agent systems, 1 
closed-loop system, and no unnecessary n8n layer. 
LOOP-MIND — Data & Dynamic Option Generation Requirement 
• 
Every required dataset used by LOOP-MIND must exist and be usable during development. 
• 
If the user does not provide a dataset, LOOP-MIND must automatically generate a 
complete, large, realistic, meaningful, and project-context-specific dataset. 
• 
Generated datasets must match the exact requirements, workflows, student data, recruiter 
data, company intelligence, jobs, skills, preparation, AI evaluation, interviews, and other 
approved project functionality where applicable. 
• 
The generated data must not be random or generic. It must be logically consistent and 
suitable for actual development, testing, AI/ML/DL processing, comparison, matching, 
analysis, and UI rendering. 
• 
The generated datasets must be stored in the appropriate databases/ data-files area and 
used by the application. 
• 
If the user later provides an original/real dataset, the system must allow that dataset to 
replace the generated dataset without requiring the overall application architecture to be 
redesigned. 
• 
When the user modifies/replaces a dataset and runs the application, the system must 
process and use the updated dataset. 
Dynamic Dropdown & Searchable Option Generation 
• 
Every required dropdown, searchable dropdown, selector, filter, multi-select, 
autocomplete field, or similar selectable data source must have complete data.

## SOURCE PAGE 439

• 
If the user has not provided the required options/data, the system must automatically 
generate appropriate options based strictly on the relevant LOOP-MIND context. 
• 
Generated dropdown data must be: 
o 
Complete 
o 
Realistic 
o 
Context-specific 
o 
Consistent with the related datasets 
o 
Searchable where the UI requires search 
o 
Dynamically loaded rather than hardcoded unnecessarily 
• 
This applies to all required dropdowns and selectable data sources across the project, not 
only currently identified pages. 
• 
No required option set or dataset should be left empty, incomplete, placeholder-only, or 
omitted because the user did not provide the data. 
Replacement Rule 
User-provided data has priority over generated data. 
User-provided dataset/options → use directly 
No user-provided dataset/options → automatically generate complete contextual data 
User later replaces/updates the data → application uses the updated data 
This requirement applies throughout the LOOP-MIND implementation and must be followed without 
adding unrelated datasets, options, or functionality.

Yes. I reviewed the **LOOP-MIND Master Product Specification** specifically from the perspective of whether the **technology stack, AI-agent architecture, datasets, and overall system are actually appropriate for your project**.

My conclusion: **the architecture is strong and matches the project's core idea**, but there are a few things I would tighten before development. I would **not add a lot of new technologies**. Your biggest risk is not “missing technology”; it is **over-engineering the AI layer and under-specifying the data contracts, evaluation, and workflow state**.

## 1. Overall verdict

| Area                       | My assessment                               |
| -------------------------- | ------------------------------------------- |
| Frontend                   | ✅ Good                                      |
| Backend                    | ✅ Very good                                 |
| SQLite                     | ✅ Correct for current scope                 |
| Qdrant                     | ✅ Correct                                   |
| LangChain                  | ✅ Appropriate                               |
| RAG                        | ✅ Appropriate                               |
| 12 AI agents               | ⚠️ Good concept, needs strict orchestration |
| ML                         | ✅ Appropriate                               |
| Deep Learning              | ⚠️ Keep optional/use-case driven            |
| Datasets                   | ✅ Strong foundation                         |
| Function calling           | ✅ Essential                                 |
| MCP                        | ⚠️ Keep optional                            |
| n8n                        | ✅ Correctly removed                         |
| Microservices              | ✅ Correctly avoided                         |
| Redis                      | ✅ Correctly avoided for now                 |
| Security                   | ⚠️ Needs stronger specification             |
| AI evaluation              | ⚠️ Needs more explicit methodology          |
| Data versioning/provenance | ⚠️ Missing as a formal requirement          |
| Agent state/orchestration  | ⚠️ Needs explicit definition                |
| Observability/auditability | ⚠️ Needs explicit definition                |

The existing specification already makes the important architectural decision to keep the system **Python-first for backend, Applied AI, ML and DL**, while using React/TypeScript for the frontend. 

---

# 2. Tech Stack — I would keep almost all of it

Your current stack is:

### Frontend

* React.js
* TypeScript
* Vite
* Tailwind CSS
* shadcn/ui
* React Flow
* Recharts

This is a good fit because your frontend has:

* Student Portal
* Recruiter Portal
* dashboards
* tables
* cards
* charts
* progress visualization
* AI workflow visualization

The specification already assigns these technologies to those responsibilities. 

### Backend

* Python
* FastAPI
* Pydantic
* SQLAlchemy
* JWT
* OTP
* REST APIs

**Keep this.**

It is especially appropriate because you have one backend responsible for:

* authentication
* profiles
* jobs
* applications
* candidates
* interviews
* AI communication
* ML/DL communication
* file handling
* workflow state
* database operations. 

### Database

**SQLite + Qdrant is correct for the current project.**

SQLite should remain the source of truth for structured transactional data, while Qdrant should be used for semantic retrieval.

The specification explicitly separates their responsibilities. 

I would **not add MongoDB, Redis, Elasticsearch, PostgreSQL, or another vector database right now**.

That would increase complexity without being required by the current project.

---

# 3. One important architectural rule: SQLite is the source of truth

This should be made extremely explicit.

Your architecture should effectively be:

```text
                 LOOP-MIND
                     │
          ┌──────────┴──────────┐
          │                     │
      Structured             Semantic
        Data                   Data
          │                     │
       SQLite                 Qdrant
          │                     │
          └──────────┬──────────┘
                     │
                  AI Layer
                     │
          LangChain + Agents
                     │
          ┌──────────┴──────────┐
          │                     │
       Analysis             Generation
```

**Qdrant should not become the authoritative database for users, applications, jobs, approvals, etc.**

For example:

```text
Student Profile
      ↓
SQLite
      ↓
Embedding
      ↓
Qdrant
```

not:

```text
Student Profile
      ↓
Qdrant
      ↓
Application state
```

Your specification already defines SQLite for students, recruiters, jobs, applications, interviews, AI results, approvals, preparation plans, skill gaps, progress and historical records. 

That's the right architecture.

---

# 4. AI Agents — 12 is acceptable, but don't let them become 12 independent chatbots

This is probably the **most important thing I'd change conceptually**.

Your specification defines exactly 12 agents and explicitly says not to add unnecessary agents. 

That's fine.

But architecturally they should behave as **specialized capabilities inside one controlled AI system**, not 12 autonomous agents freely talking to each other.

For example:

```text
                    AI Orchestrator
                           │
       ┌───────────────────┼───────────────────┐
       │                   │                   │
 Student Intelligence   Recruitment        Interview
       │                 Intelligence          │
       │                   │                   │
       └────────────── Agent Layer ─────────────┘
                           │
                     Tools / APIs
                           │
                 ┌─────────┴─────────┐
                 │                   │
              SQLite              Qdrant
```

The specification already establishes:

```text
LangChain
   ↓
Agents
   ↓
Tools / Function Calling
   ↓
SQLite / Qdrant / Services
```

and explicitly uses function calling for database retrieval, Qdrant retrieval, job search, resume processing, readiness calculations, skill-gap calculations, rules, AI services and email operations. 

**That is exactly the direction I recommend.**

---

# 5. The 12 agents themselves make sense

The existing specification defines agents around meaningful business capabilities:

1. Company Intelligence Agent
2. Student Skill Analysis Agent
3. Placement Readiness Agent
4. Skill-Gap Analysis Agent
5. Preparation Plan Agent
6. What-If Analysis Agent

and continues with the recruitment-side agents. 

The important thing is that each agent needs:

### Input

What information it is allowed to receive.

### Tools

What functions it is allowed to call.

### Knowledge

What Qdrant collections/data it can retrieve.

### Output schema

What structured result it must return.

### Decision authority

Whether it can:

* only analyze
* recommend
* update data
* trigger another agent
* require human approval

This last part is particularly important.

---

# 6. Human approval is one of the strongest parts of your architecture

Your recruitment pipeline is:

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
Interview Agent
      ↓
Email Invitation
```

The recruiter can approve or disapprove after AI shortlisting. 

**Keep this exactly.**

I would not make the AI automatically decide final recruitment outcomes.

Your system becomes much stronger conceptually because it is:

> AI-assisted recruitment, not uncontrolled autonomous hiring.

The human approval/disapproval state and disapproval reason are already explicitly represented in SQLite. 

---

# 7. RAG — absolutely makes sense here

Unlike the separate Advaita Matrimony example, LOOP-MIND explicitly requires RAG. 

And your RAG sources are actually meaningful:

* company requirements
* job requirements
* successful candidate characteristics
* student evidence
* historical recruitment outcomes
* assessment topics
* interview information
* preparation resources
* skill-gap knowledge

That's a much better RAG use case than simply adding RAG because "AI projects need RAG."

Your architecture:

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

is appropriate. 

---

# 8. But your RAG architecture needs one missing concept: metadata

This is something I strongly recommend adding to the **specification**, not as an extra technology.

Every vectorized document/chunk should have metadata allowing the system to know where it came from.

Conceptually:

```text
Embedding
 ├── vector
 ├── document_id
 ├── source_type
 ├── company_id
 ├── job_id
 ├── student_id
 ├── skill_id
 ├── document_version
 └── timestamp
```

Why?

Suppose the agent retrieves:

> "Strong candidates for this role should know Python..."

The system needs to know:

**Where did that information come from?**

Without provenance, your RAG system becomes difficult to audit.

This is a **specification-level improvement**, not a request to add another database.

---

# 9. Your datasets are good — don't create dozens of unnecessary datasets

You already have **8 core dataset categories**:

1. Company & Job Requirements
2. Recruitment Process & Historical Outcomes
3. Candidate / Student Profile
4. Successful Candidate
5. Skill & Evidence
6. Interview & Assessment
7. Preparation & Learning
8. AI Evaluation

These are already explicitly defined. 

I would **keep these eight**.

Don't turn them into 20–30 disconnected datasets just because more datasets sound more "AI."

---

# 10. What is missing in the dataset architecture?

Not necessarily another dataset.

What's missing is **dataset governance**.

Every dataset should have a clear distinction between:

```text
RAW
 ↓
CLEANED
 ↓
NORMALIZED
 ↓
PROCESSED
 ↓
EMBEDDED
 ↓
USED BY AI
```

For example:

```text
storage/datasets/
    raw/
    processed/
    evaluation/
```

And each dataset should have:

* source
* version
* schema
* processing status
* date/version
* relationship to the application

This becomes particularly important because your specification allows realistic generated company data until real company data becomes available, after which the real dataset replaces/updates it through the same processing pipeline. 

That is a very good design.

---

# 11. Generated datasets — your existing rule is correct

This part should **not be changed**.

You don't need the user to provide every dropdown dataset.

The implementation can generate meaningful contextual datasets at implementation time where no dataset has been supplied. 

The important distinction is:

### UI examples

```text
Google
Microsoft
Amazon
```

do **not** mean:

```text
ONLY Google
Microsoft
Amazon
```

They are examples.

Your actual database should contain the required meaningful dataset.

This same principle is already established in the source specification. 

---

# 12. ML — keep it, but don't force ML everywhere

Your ML stack:

* pandas
* NumPy
* scikit-learn

is appropriate.

The specification identifies ML use cases such as:

* recruitment pattern analysis
* candidate/job feature analysis
* readiness-related prediction
* historical recruitment analysis
* matching support
* outcome analysis
* skill-gap pattern analysis. 

But there's an important architectural principle:

> **Don't use ML simply because the project contains an ML folder.**

If a deterministic calculation is sufficient, use a deterministic calculation.

If semantic reasoning is needed, use embeddings/RAG/LLM.

If statistical prediction is justified by sufficient historical data, use ML.

That separation will make the project much cleaner.

---

# 13. Deep Learning — this is the one area I'd keep very restrained

PyTorch is specified for DL. 

That's fine.

But I would **not force a custom deep-learning model into the first implementation**.

Your project already has:

```text
LLM
Embeddings
RAG
Agents
ML
```

Adding a custom DL model without a genuine training problem would just make the architecture heavier.

So:

**PyTorch stays in the stack.**

But:

**DL implementation should be use-case driven, not mandatory for every workflow.**

---

## UPDATE — ML/DL Training Architecture (ML/DL Training Architecture SDD)

§12-13 above already established the restrained philosophy — this update is
its actual implementation, not a change of direction. The `ML and DL/`
directories are populated with a real pipeline instead of remaining empty
placeholders:

```text
Database -> Dataset Generation -> Preprocessing -> ML Training ->
Evaluation -> Validated Model (only if it earns acceptance) -> models/
```

* `datasets/raw/` holds recruitment records exported straight from the
  application's own database (student, job, company, skills, matching
  score, shortlisting result, recruiter decision, interview result, final
  outcome) — never manually invented data.
* `datasets/processed/` and `preprocessing/` clean, normalize, and derive
  ML-ready features, with the identical derivation reused at inference time
  so training and inference features never diverge.
* An application only receives a `final_outcome` label once it has actually
  concluded (hired -> success; not-selected or recruiter-disapproved ->
  failure). Both outcome classes are represented in training data — never
  success-only. An in-progress application is exported for visibility but
  excluded from training rather than assigned a fabricated label.
* `ml/` trains a scikit-learn model only when at least 10 concluded examples
  of *both* outcome classes exist; otherwise the pipeline reports
  `insufficient_data` and trains nothing, rather than producing a
  meaningless model from too little history. This is expected and correct
  for a fresh/demo deployment.
* `dl/` remains unused — the current recruitment history is not sufficient
  or complex enough to justify deep learning over the `ml/` model, per §13.
* `evaluation/` evaluates every newly trained model (accuracy, precision,
  recall, F1) and gates acceptance: a model below 60% accuracy is rejected,
  and a new model that doesn't beat the currently validated model's
  accuracy is rejected too, so a previously validated model is never
  silently replaced by a worse one.
* `models/` stores an accepted model's artifact plus metadata (training
  date, feature schema, sample size, metrics) only after it clears the
  evaluation gate.
* Not every database table becomes a training feature — only the
  recruitment-outcome dataset above has a defined training schema
  (Database -> relevant historical records -> dataset generation -> defined
  training schema -> preprocessing -> training), preventing unrelated data
  from leaking into the model.
* `run_training_pipeline.py` orchestrates the full loop and was verified
  end to end against both the real dev database (correctly reports
  `insufficient_data`) and a synthetic dataset (correctly trains, evaluates,
  accepts, and persists a model).

---

# 14. MCP — keep it optional exactly as the specification says

Your specification correctly says MCP is **not an AI agent** and shouldn't be forced into every agent. 

That's correct.

Use:

```text
Agent
 ↓
Function Calling
 ↓
Internal Service
```

for normal application operations.

Use MCP only when you actually have a standardized external tool/context integration that benefits from it.

I would **not put MCP into every workflow just to say the project uses MCP.**

---

# 15. n8n — removing it was the right decision

I agree strongly with the existing decision.

The specification explicitly removed n8n from the core architecture because FastAPI, Python services, LangChain, background processing, SQLite and Qdrant can control the required workflows directly. 

For this project:

```text
FastAPI
   ↓
Python services
   ↓
Agent orchestration
   ↓
Tools
   ↓
Database / Qdrant
```

is cleaner than:

```text
FastAPI
   ↓
n8n
   ↓
webhooks
   ↓
AI
   ↓
database
```

You don't need another orchestration layer unless a real requirement emerges.

---

# 16. One thing I would add: explicit AI output schemas

This is probably the **single most important missing specification item**.

Agents should not simply return arbitrary text.

For example, Skill Gap Agent should return a structured object conceptually like:

```text
Skill Gap Result
 ├── target_role
 ├── target_company
 ├── current_skills
 ├── missing_skills
 ├── weak_skills
 ├── missing_evidence
 ├── priority_gaps
 ├── reasoning
 └── confidence
```

Similarly:

```text
Matching Result
 ├── candidate_id
 ├── job_id
 ├── score
 ├── matching_factors
 ├── gaps
 ├── evidence
 └── recommendation
```

Then the frontend displays the structured result.

This prevents:

```text
LLM → random text → frontend
```

and gives you:

```text
Agent
 ↓
Structured schema
 ↓
Validation
 ↓
Database
 ↓
Frontend
```

Pydantic is already in your backend stack, so this fits naturally. 

---

# 17. Another important missing piece: AI evaluation should be more explicit

You already have an **AI Evaluation Dataset**. 

Good.

But the specification should define that each important AI component has measurable evaluation criteria.

For example:

```text
Resume Parser
    → extraction accuracy

Matching
    → ranking quality

Shortlisting
    → precision / recall where applicable

Skill Gap
    → expert/reference agreement

RAG
    → retrieval relevance

Interview Agent
    → question relevance

Preparation Plan
    → requirement/gap coverage
```

You don't necessarily need complicated AI-evaluation infrastructure.

But the project should be able to answer:

> **How do we know this agent works correctly?**

That should be part of the SDD.

---

# 18. Security is the biggest non-AI area I would strengthen

Your authentication architecture already includes:

```text
Student / Recruiter
      ↓
Mobile
      ↓
OTP
      ↓
Account type identification
      ↓
Correct portal
```

which is defined in the project specification. 

But your SDD should make security rules explicit around:

### Authorization

A student must not access recruiter resources.

A recruiter must not access another recruiter's private data.

### Object ownership

A student should only modify/read resources they are authorized to access.

### Resume/document access

Private resumes should not become publicly accessible merely because they exist under storage.

### AI tool permissions

An agent should only be able to call tools appropriate to its role.

For example:

```text
Student Agent
   ✕ approve candidate
   ✕ modify recruiter data

Recruiter Agent
   ✕ modify student profile
   ✕ access unrelated recruiter data
```

This is especially important because you are giving agents function-calling capabilities.

---

# 19. Agent permissions should therefore be part of the SDD

I would define:

```text
Agent
 ↓
Allowed Tools
 ↓
Allowed Data
 ↓
Allowed Actions
```

Not:

```text
Agent
 ↓
Everything
```

For example:

```text
Placement Readiness Agent
 ├── get_student()
 ├── get_company()
 ├── get_job()
 ├── retrieve_skill_knowledge()
 └── calculate_readiness()
```

while it should not have:

```text
approve_candidate()
delete_account()
send_recruiter_email()
```

unless explicitly required.

Your existing function-calling architecture gives you the foundation for this. 

---

# 20. Storage architecture is correct, but don't mix datasets with application uploads conceptually

Your repository already separates:

```text
storage/
 ├── resumes/
 ├── documents/
 ├── datasets/
 └── ...
```

and the specification explicitly defines storage for resumes, documents, uploaded files and datasets. 

That's good.

I'd preserve it.

Don't start creating random folders such as:

```text
ai_data/
misc_data/
temp_data/
random_uploads/
```

unless a real requirement requires them.

---

# 21. Your repository architecture is actually good

The current structure:

```text
LOOP-MIND/
│
├── frontend/
├── backend/
├── databases/
├── storage/
├── AI services/
├── ML and DL/
├── phase.md
└── spec.md
```

is coherent and intentionally separates Applied AI from ML/DL. 

I would **not radically restructure it**.

Especially keep:

```text
AI services/
ML and DL/
```

separate because they have different purposes.

---

# 22. One thing I would NOT add

I would not add these just because they're popular:

```text
❌ MongoDB
❌ Redis
❌ Kafka
❌ Kubernetes
❌ Microservices
❌ Elasticsearch
❌ n8n
❌ Multiple vector databases
❌ Multiple LLM frameworks
❌ Multiple agent frameworks
```

Your current project does not need that complexity.

The specification itself explicitly avoids unnecessary infrastructure such as Redis and microservices and keeps the architecture relatively compact. 

---

# 23. The architecture I would lock

If I were freezing the architecture for development, I'd use:

```text
                    LOOP-MIND
                        │
          ┌─────────────┴─────────────┐
          │                           │
       Frontend                    Backend
          │                           │
 React + TypeScript              FastAPI
 Vite                             Pydantic
 Tailwind                         SQLAlchemy
 shadcn/ui                        JWT + OTP
 React Flow                       REST APIs
 Recharts                             │
          │                           │
          └──────────────┬────────────┘
                         │
                  Application Layer
                         │
             ┌───────────┴───────────┐
             │                       │
          SQLite                  Storage
             │                       │
             │                 Resumes/Documents
             │                       │
             └──────────┬────────────┘
                        │
                    AI Layer
                        │
                    LangChain
                        │
             ┌──────────┼──────────┐
             │          │          │
           RAG       Agents     ML/DL
             │          │          │
          Qdrant       Tools   scikit-learn
             │          │       PyTorch
             └────┬─────┘
                  │
          Function Calling
                  │
        Controlled AI Services
                  │
       Human Approval Where Required
```

That is enough.

---

# 24. The biggest thing your project should focus on

Your strongest differentiator is **not the number of technologies**.

It is the closed loop:

```text
Student Profile
      ↓
Skill Analysis
      ↓
Company / Job Requirements
      ↓
Placement Readiness
      ↓
Skill Gap
      ↓
Preparation Plan
      ↓
Student Improvement
      ↓
Job Application
      ↓
Resume Processing
      ↓
Matching
      ↓
AI Shortlisting
      ↓
Recruiter Review
      ↓
Human Approval
      ↓
Interview
      ↓
Recruitment Outcome
      ↓
Back to Student
      ↓
Updated Skill Gap
      ↓
Updated Preparation
```

The specification explicitly identifies the human-approval → interview → outcome → student skill-gap/preparation loop as essential to the project's closed-loop recruitment model. 

**That is the architecture I would protect above everything else.**

---

# 25. My final recommendation

### KEEP

* React
* TypeScript
* Vite
* Tailwind
* shadcn/ui
* React Flow
* Recharts
* Python
* FastAPI
* Pydantic
* SQLAlchemy
* JWT
* OTP
* SQLite
* Qdrant
* LangChain
* RAG
* Function Calling
* 12 specialized agents
* scikit-learn
* pandas
* NumPy
* PyTorch
* Git/GitHub
* Pytest
* Ruff
* ESLint
* Prettier
* Docker as optional development tooling

The existing specification supports this stack.  

### KEEP OPTIONAL

* MCP
* Deep Learning implementation
* additional external integrations

### DO NOT ADD

* n8n
* Redis
* MongoDB
* another vector DB
* microservices
* unnecessary agent frameworks
* unnecessary orchestration platforms

### STRENGTHEN IN THE SDD

These are the areas I think are genuinely worth adding:

1. **Agent input/output contracts**
2. **Agent tool permissions**
3. **RAG metadata/provenance**
4. **Dataset versioning and processing lifecycle**
5. **AI evaluation methodology**
6. **AI workflow state transitions**
7. **Authorization/access-control rules**
8. **AI/action audit trail**
9. **Clear distinction between AI recommendation and human decision**
10. **Failure/fallback behavior for AI services**

These aren't "extra features." They are the specifications that make the existing architecture **actually buildable and reliable**.

### Bottom line

**I would not change your core tech stack.**

Your architecture is already quite well aligned with LOOP-MIND. The thing I'd improve now is the **precision of the SDD around AI contracts, data lineage, permissions, evaluation, and workflow state**, rather than adding more technologies.

That will make the project **simpler, more defensible, easier to implement, and much less likely to turn into an over-engineered AI demo.**

## UPDATE — Recruiter Portal navigation right-aligned; Pending Approval metric; broadened
historical signal (Student Job Application & Recruitment Workflow SDD + Recruiter Portal
Dashboard/Job Management/Candidate Evaluation & Closed-Loop ML Workflow SDD)

An audit of the already-built end-to-end recruitment workflow (student apply → resume
processing → Matching Agent → Shortlisting Agent → Human Approval → Interview Agent → Email
Agent → student notification, plus the Recruiter Dashboard/Job Management/Candidates pages and
closed-loop historical data) against this combined SDD confirmed the large majority of it was
already correctly implemented and required no change: Apply Now's resume-exists/resume-missing
paths, the Interview Agent only ever generating questions from the approval workflow (never from
opening the Interview page), the Email Agent only ever composing an invitation once both
approval and scheduling are complete, disapproval reasons and application status always reading
from stored decision data, and Upcoming Interviews/dashboard job-application counts already
being fully database-driven. Three genuine gaps were found and fixed:

* **Recruiter Portal navigation** was still left-aligned on every recruiter page (Dashboard, Job
  Management, Candidates, Interviews, Analytics) — each composed its own `<Navbar>` without the
  `linksAlign="end"` the Student Portal's own `StudentNavbar` already uses. A new shared
  `RecruiterNavbar` component now backs all five pages, matching `StudentNavbar`'s pattern
  exactly, so the two portals' navigation can never drift again.
* **Pending Approval** was missing as its own metric everywhere this SDD calls for it (Dashboard
  Overview, Application Pipeline, Candidates summary) — an AI-shortlisted application with no
  recruiter decision yet was already counted as "Shortlisted" (a reasonable, unchanged, already-
  tested classification used for filtering elsewhere), but never surfaced as a distinct "awaiting
  human review" count. A new shared `is_pending_approval()` helper now feeds a `pending_approval`
  field on all three, additive to the existing three-bucket Shortlisted/Under Review/Rejected
  classification rather than replacing it.
* **The historical closed-loop signal** informational text shown alongside a candidate's AI
  match result (recruitment_ai_service.py's `_historical_signal`) only ever considered previously
  *hired* candidates for the same role — a real, if narrow, violation of "the ML system must not
  learn only from successful candidates." It now also surfaces the same recruiter's previously
  *not-selected* candidates for the role who shared matched skills, alongside the hired-candidate
  signal, still purely informational and never adjusting the AI score.

## UPDATE — Resume replacement now reconciles stale skills/projects/certifications, not just
adds new ones (Dynamic Resume Replacement & Student Data Synchronization SDD §1-6)

Every resume upload/replacement previously only ever *added* newly-found skills/projects/
certifications, deduped by name against whatever the student already had — it never removed
anything, so a skill or project dropped from a replaced resume (e.g. "Java" removed, "Generative
AI" added in the new version) stayed as "current" resume-derived data forever. `StudentSkill`,
`StudentProject` and `StudentCertification` now each carry a `source` column ("manual" |
"resume" | "linkedin") recording where a row came from; every resume upload/replacement still
adds whatever is newly found (tagged `source="resume"`) and now also removes any
`source="resume"` row that is no longer present in the freshly re-extracted resume — reconciling
resume-derived data to the *latest* resume exactly, per §4's example. A skill/project/
certification the student entered manually, edited by hand, attached evidence to, or uploaded a
certificate file for is marked `source="manual"` and is never touched by this reconciliation,
regardless of whether it also happens to be absent from the new resume's text — nor is anything
that came from LinkedIn. Skill Gap/Placement Readiness/Preparation Plan already recalculate
automatically after a resume change (an earlier update), so they now also reflect the reconciled
(not just appended-to) skill set; historical Skill Gap/Preparation Plan snapshots and past job
applications' resume references are unaffected, since those were already stored as independent
point-in-time records rather than live references to the current skill table.

## UPDATE — Real "Sign In with LinkedIn" for identity fields, alongside the existing best-effort
extraction (LinkedIn Profile Extraction Implementation Specification)

The previous LinkedIn mechanism (auto-triggered on blur, an unauthenticated best-effort fetch of
the pasted public URL's HTML text run through `linkedin_extraction_agent.py`) genuinely cannot
retrieve name/email/photo reliably, since LinkedIn requires authentication for that and prohibits
unauthorized scraping. A new, separate, real OAuth ("Sign In with LinkedIn", OpenID Connect) path
was added *alongside* it — a "Connect to LinkedIn" button that opens a popup where the student
signs into their own LinkedIn account and grants the `openid profile email` scopes, which is the
only combination LinkedIn's API actually authorizes for a general integration. That flow can only
ever return name, email, and a profile photo — never skills, projects, certifications, education,
or experience, regardless of configuration; those keep coming exclusively from the existing
best-effort text-fetch path and the Resume Parser Agent, unchanged.

The whole OAuth path is gated behind `LINKEDIN_CLIENT_ID`/`LINKEDIN_CLIENT_SECRET` (empty by
default, since this project has no real LinkedIn Developer app registered yet) — `GET
/registration/draft/linkedin/oauth-config` reports `configured: false` honestly when they're
unset, and the frontend shows that plainly rather than presenting a button that can't work. Once
real credentials are set (and `LINKEDIN_REDIRECT_URI` — default
`http://localhost:5180/linkedin/oauth-callback` — is registered as the app's redirect URI on
LinkedIn's Developer Portal), the button performs a genuine authorization-code exchange
server-side (`linkedin_oauth_service.py`; the client secret never reaches the browser) and only
pre-fills the Basic Information name/email fields the student hasn't already typed something
into — never a silent overwrite, and never fabricated data when a field isn't returned.

## UPDATE — Manual skill/project/certification entry now dedupes too; source protection only
ever upgrades; empty resume extraction never wipes prior data (Dynamic Resume Replacement,
Skill/Project/Certification Synchronization & Source-Aware Deduplication SDD)

Three refinements to the resume-replacement/source-tracking work from the previous update:

* **Manual entry now dedupes too.** `create_skill`/`create_project`/`create_certification` —
  called by My Profile's "Add Skill/Project/Certification" forms directly, not just by resume/
  LinkedIn extraction — previously had no duplicate-name check at all, so a student manually
  adding a skill name that already existed (e.g. one already extracted from a resume) created a
  genuine second row, inflating the displayed count. All three now look up an existing
  case-insensitively-matching row first and update it in place instead of ever creating a
  duplicate, matching the "Python = 1, not 3" requirement for every entry path, not only
  extraction.
* **Source protection now only ever upgrades, never gets stuck.** If a skill/project/
  certification is first seen from a resume (`source="resume"`, eligible for deletion on a future
  resume replacement) and a *later* extraction — LinkedIn, or the student manually touching it —
  independently confirms the same item, the existing row's source is now upgraded
  (resume → linkedin → manual, ranked in that order of protection) rather than left as `"resume"`
  forever. Without this, a skill genuinely confirmed by LinkedIn could still be deleted the next
  time the resume was replaced, simply because it happened to be recorded under the resume's
  source tag first.
* **An empty resume extraction no longer reconciles away prior data.** If a newly uploaded/
  replaced resume's text yields *zero* skills, certifications, and projects, that is now treated
  as a failed/inconclusive parse (per §26-27's "Failed Extraction Rule") rather than "the new
  resume legitimately has none" — the previous resume-derived records are left untouched instead
  of being wiped out. Reconciliation (removing resume-derived items absent from the new
  extraction) only ever runs when the new extraction found at least one item, which is the
  legitimate "this resume genuinely no longer lists X" case.

## UPDATE — Delete Resume now removes its resume-derived data; Resume Parser no longer counts a
project's "Technologies:" line as a separate project (Resume Lifecycle, Exact Resume Parsing,
Source-Aware Counts & Agent Cross-Check SDD)

Two corrections, superseding two earlier decisions from this session:

* **Delete Resume now also removes what that resume exclusively contributed.** `DELETE
  /students/me/resume` previously cleared only the file reference, deliberately leaving
  resume-derived skills/projects/certifications in place. That was wrong: deleting a resume is an
  explicit, deliberate action (unlike a failed upload, where the empty-extraction guard correctly
  protects against an ambiguous parsing failure), so it must behave like a replacement with
  nothing to replace it with — every skill/project/certification still tagged `source="resume"`
  (never independently confirmed by the student or LinkedIn since) is now removed, exactly as a
  resume replacement would remove what the *old* version contributed. Manually entered and
  LinkedIn-derived data is never touched, and a Skill Gap recalculation now runs immediately
  afterward if a target is already set.
* **The Resume Parser Agent no longer miscounts a project's technology line as its own project.**
  A resume's Projects section typically lists each project as a title line followed by attribute
  lines such as "Technologies: React, Node.js, MongoDB" — the previous line-by-line extraction
  treated every non-empty line as a separate project, so that attribute line became a fake fourth
  project. Attribute-prefixed lines (Technologies/Tech Stack/Tools/Stack/Description/Role) are now
  recognized and attached to the current project (technologies feed `technologies_used`) instead
  of starting a new one — three real projects each listing their own technologies now correctly
  extract as three projects, not eight.

## UPDATE — Unlabeled project description lines no longer counted as separate projects
(Resume Parsing, Project Counting, Replacement & Recruitment-Agent Integration Correction
Specification)

The previous fix handled a project's *explicitly labeled* attribute lines ("Technologies:
React, Node.js, MongoDB"). It did not yet handle the equally common case of an unlabeled prose
description directly under a project title with no blank line and no "Description:" prefix —
e.g. "Project A" followed immediately by "Built a full-stack e-commerce platform with payment
integration." — which still became its own fake second project. `_split_resume_sections` now
preserves blank lines within a section as explicit boundary markers (every other section's own
parsing already tolerates an empty entry as a no-op), and `_parse_projects` uses that boundary
signal together with a short heuristic (`_looks_like_project_title`: no blank line since the
last title, and the line reads like prose rather than a title — many words, or ends in "." or
"!") to recognize an unlabeled continuation line as the current project's description instead of
a new project. A compact one-title-per-line format with no descriptions at all (each short line,
no trailing punctuation) still correctly produces one project per line, since nothing about it
reads as prose.

## UPDATE — What-If Analysis: Potential Improvement shown, explicit Reset, no stale result
during loading (Skill Gap Analysis — What-If Analysis Specification)

An audit of the existing What-If Analysis card against this SDD found the core simulation
guarantees already correct — `intelligence_service.ask_what_if` only ever writes to the separate
`WhatIfResult` table, never touching `StudentSkill`/`SkillGapAnalysis`/`StudentCareerPlacement`,
and the modal's local state fully resets on each open (never leaking into the page's real Skill
Gap data) — but found three real display gaps, all fixed:

* **Potential Improvement was never shown** — only Current Readiness and Projected Readiness
  were displayed side by side, leaving the student to do the subtraction themselves. A third
  value, computed from the same two already-returned numbers (never a separate agent call or
  invented figure), now sits alongside them.
* **No explicit Reset action existed** inside the modal — the only way to clear a shown result
  before trying a different hypothetical was to close and reopen the whole dialog. A Reset button
  now clears the question/result/error locally (no API call, nothing to undo since nothing was
  ever persisted) without closing the modal.
* **A stale previous answer could remain on screen while a new question was being analyzed**,
  which could read as the fresh result before the new response arrived. The previous result is
  now cleared the moment a new analysis starts, so "Analyzing…" never sits above stale numbers.

The action button is also now labeled "Generate," matching this SDD's own naming.

## UPDATE — Recruiter Dashboard reverted to four cards with corrected, non-mutually-exclusive
semantics; interview invitation now cites actual matched skills (Recruiter Dashboard — Final
Specification)

This corrects the Pending Approval card added by an earlier update — it's now removed
everywhere (Dashboard summary, Application Pipeline, Candidates page summary). The Dashboard's
first row is exactly four cards again: Total Jobs, Total Applications, Shortlisted, Under
Review. Their definitions changed to match this spec precisely, and — critically — Shortlisted
and Under Review are no longer mutually exclusive:

* **Shortlisted** now means the Shortlisting Agent's own output (`ai_status == "shortlisted"`)
  specifically, regardless of whether a recruiter has since decided on it.
* **Under Review** now means "no recruiter decision yet," full stop — true the moment an
  application is created, before the Shortlisting Agent even runs (previously "Under Review" and
  "Shortlisted" were mutually exclusive buckets, so an AI-shortlisted application awaiting
  approval only counted toward one of them; now it correctly counts toward both).
* **Rejected** (kept in the Application Pipeline breakdown, not the four-card summary row) now
  means a recruiter's own Human-in-the-Loop disapproval specifically — never the Shortlisting
  Agent's own "rejected" recommendation, which a recruiter can still override in either
  direction.

The Candidates page's own per-candidate status column (Shortlisted/Under Review/Rejected,
reflecting the human decision specifically) is unchanged — only its "Pending Approval" summary
card was removed, since this spec's "no separate Pending Approval" rule applies everywhere.

Separately: the interview invitation email was completely generic — it never referenced *why* a
candidate was selected, exactly the "Your profile matches our requirements" filler this spec
forbids, even though the recruitment pipeline's own matching data (`matching_factors
["matched_skills"]`) was already sitting unused right next to where the invitation is composed.
The Email Agent now includes those actual matched skills in the invitation body when they exist,
and simply omits that paragraph — never invents one — when no matched-skills data is available.

CURRENT PHASE ONLY: Compare the implementation against the complete `spec.md` and `phase.md`. Identify every missing, incorrect, unauthorized, or extra CURRENT-PHASE requirement. Fix every CURRENT-PHASE issue, run the application, test again, and re-read both documents completely. Repeat until the CURRENT PHASE is fully compliant. Do NOT implement FUTURE-PHASE requirements even if discovered during the audit. The next phase is allowed ONLY after the CURRENT PHASE passes this cross-check with no remaining CURRENT-PHASE issues.

---

## UPDATE — Interview invitation email is now genuinely sent, not just composed
(Recruiter Interview Invitation & Demo Email Specification)

A "successful" Interview Agent/Email Agent status previously meant only that content had been
generated in memory during a page view — nothing was ever actually delivered, and refreshing the
Recruiter Portal never showed more than a checkmark. The full approval → interview → email
workflow this spec requires is now real end to end:

* **Approval triggers both agents in one event**: `recruiter_candidates_service.approve_candidate`
  runs the Interview Agent (question generation, already existing) and then, immediately within
  the same approval, the Email Agent's send attempt — never merely on a later page view, and never
  gated behind the separate "schedule interview" action.
* **Student email resolution** follows the required fixed priority — profile email first, then
  (only if genuinely unavailable) the email the Resume Parser Agent finds literally present in the
  uploaded resume's text — and never invents an address. The Resume Parser Agent
  (`AI services/agents/resume_parser_agent.py`) now extracts an email address from resume text
  when one is present; `apply_resume_extraction` stores it on
  `StudentProfessionalLinks.resume_extracted_email`, cleared whenever the resume itself is
  removed.
* **A real SMTP transport** (`backend/services/email_service.py`) actually sends the message,
  configured exclusively through environment variables (`EMAIL_PROVIDER`, `EMAIL_HOST`,
  `EMAIL_PORT`, `EMAIL_USERNAME`, `EMAIL_PASSWORD`, `EMAIL_FROM` — `backend/core/config.py`,
  sourced from `.env`), never hardcoded into frontend or backend source. When the demo mailbox
  isn't configured, the system honestly reports that instead of pretending to have sent anything.
* **Persisted delivery status** lives on `Interview` (`email_status`: pending/sending/sent/failed;
  `recipient_email`; `email_source`: profile/resume/unavailable; `email_sent_at`; `email_error`) —
  a real terminal state that survives a Recruiter Portal refresh rather than being recomputed live.
  Sending is idempotent: a `"sent"` status is never re-sent or duplicated by re-approving the same
  application; a `"failed"` attempt may be retried on a later approval since nothing was actually
  delivered the first time.
* **Invitation content stays application-specific and non-fabricated**: company/job/matched-skill
  data comes straight from the stored recruitment evaluation, exactly as the existing Email Agent
  already did; at approval time (before any interview has been scheduled) the "Interview Details"
  section honestly states the real process status rather than inventing a type or time, and
  automatically reflects the actual schedule once `schedule_interview` sets one.
* **Recruiter Portal** now surfaces the real outcome instead of only a tick: the Interviews page's
  interview detail view shows the actual delivery badge, recipient, source, and any failure
  reason; the Candidates page's workflow panel shows the generated question count and the same
  delivery badge/recipient next to its existing stage diagram, whose `email_invitation` stage now
  reflects the real send outcome rather than inferring one from scheduling.
* Verified with real tests, not just manual inspection: a mocked-SMTP send actually reaching
  `"sent"`, an unconfigured transport honestly reaching `"failed"` with a clear reason, the
  resume-email fallback firing only when the profile email is genuinely absent, and the
  neither-exists case reporting `"unavailable"` rather than fabricating a recipient.

---

## UPDATE — Sender identity, non-destructive resume-email storage & the actual refresh-logout root cause
(Email Invitation & Session Persistence Fix Specification)

**Email side** — two concrete additions on top of the previous update:

* A configured sender **display name** (`EMAIL_FROM_NAME`, `backend/core/config.py`), combined
  with `EMAIL_FROM` via `email.utils.formataddr` in `email_service.send_email` into a proper
  `"LOOP-MIND Recruiting <demo@...>"` From header — the sender identity is set entirely
  independently of, and never derived from, the recipient student's own email.
* `student_profile_service.apply_resume_extraction` no longer clears a previously stored
  `resume_extracted_email` just because a later resume re-upload's extraction didn't itself state
  one — it only ever *sets* the field when a new extraction genuinely finds an address, per this
  spec's explicit "must not replace an existing valid student email unnecessarily" rule (the same
  principle already applied to resume-derived skills/certifications/projects).

**Session side** — this spec described the required behavior (token persists in `localStorage`,
startup restoration via `/api/auth/me`, protected routes waiting rather than redirecting during
restoration) as if it needed to be built; investigating the actual `frontend/src/lib/auth.tsx`,
`frontend/src/lib/api.ts`, `backend/routes/auth.py`, and `backend/auth/dependencies.py` found that
architecture was **already correctly implemented** — token storage, startup restoration, and
route-guard waiting all matched this spec's own diagrams exactly, and were verified live against
the running dev server end to end. The actual, genuine bug found: `AuthProvider`'s restoration
effect treated *any* failure from `/api/auth/me` — including a transient failure to even reach the
backend (routine in this project, since the backend dev server restarts on every code change) — as
an invalid session, and deleted the stored token as a result. A perfectly valid, non-expired token
was being destroyed by a momentary connectivity blip rather than an actual authentication
rejection, which is what produced the reported "refresh sends me to the landing page" symptom. The
fix only narrows that failure-handling branch: the token is cleared only when the server explicitly
returns `401` (a genuinely invalid/expired session); every other failure gets one short retry, and
if the backend still isn't reachable, the user sees the landing page for that one load without
losing their session — the next successful refresh restores it normally. No new/duplicate
authentication mechanism was introduced; the existing JWT + `localStorage` + `/api/auth/me`
architecture is unchanged in shape.
