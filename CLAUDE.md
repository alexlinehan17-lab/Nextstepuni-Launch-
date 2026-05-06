# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Nextstepuni is an educational platform ("Learning Lab") that teaches university-bound students advanced learning strategies through interactive modules. It's a React SPA with Firebase backend for auth and data persistence.

## Commands

```bash
npm install          # Install dependencies
npm run dev          # Start dev server (localhost:3000)
npm run build        # Production build via Vite
npm run preview      # Preview production build
```

No test runner or linter is configured. There are no test or lint commands.

## Environment

No environment variables are required for the current build. There is no active GenAI integration; see `compliance/GEMINI_AUDIT.md` for the audit trail. Any future GenAI integration must go through `compliance/AI_GOVERNANCE_SCHEDULE.md` first.

## Architecture

**Stack:** React 19 + TypeScript, Vite, Tailwind CSS (CDN), Framer Motion, Three.js (@react-three/fiber), Firebase (Auth + Firestore)

**Entry flow:** `index.html` → `index.tsx` → `App.tsx`

**App.tsx** (~310 lines) is the central orchestrator. It manages:
- Authentication state via Firebase `onAuthStateChanged`
- User progress persistence (Firestore `users/{uid}` and `progress/{uid}` collections)
- Route-like navigation via local state (no router library — views switch based on state)

**Root-level modules:**
- `moduleRegistry.ts` — Lazy-loads all 43 educational modules + InnovationZone via `React.lazy()` with default imports
- `courseData.ts` — Course metadata definitions (titles, descriptions, categories, tags) and `categoryColorMap`
- `moduleThemes.ts` — Per-color Tailwind theme objects (literal class strings required for CDN scanning)
- `types.ts` — Shared types: `ModuleProgress`, `UserProgress`, `SectionDefinition`, `ModuleTheme`

**Key components in `components/`:**
- `Auth.tsx` — Login/registration modal with Firebase Auth. Admin login uses Firebase Auth with the `admin@nextstep.app` account (password managed in Firebase Console, not in code).
- `KnowledgeTree.tsx` — Main navigation hub showing categories with activity ring progress indicators
- `Library.tsx` — Grid view of modules within a category using `BentoModuleTile` components
- `AdminDashboard.tsx` — Admin-only analytics view
- `ModuleLayout.tsx` — Shared sidebar + content layout used by all educational modules
- `ModuleShared.tsx` — Reusable UI primitives: `Highlight`, `ReadingSection`, `MicroCommitment`, `ActivityRing`
- `*Module.tsx` (43 files) — Individual educational modules, each using `ModuleLayout` with default exports

**Module component interface:**
```typescript
interface ModuleProps {
  onBack: () => void;
  progress: ModuleProgress;                        // { unlockedSection: number }
  onProgressUpdate: (progress: ModuleProgress) => void;
}
```

**7 course categories:** `architecture-mindset`, `science-growth`, `learning-cheat-codes`, `subject-specific-science`, `exam-zone`, `the-shield`, `the-launchpad`

**Navigation flow:** KnowledgeTree (category selection) → Library (module grid) → Module (content sections with progressive unlock)

## Conventions

- All components are functional with hooks; no class components
- Styling: Tailwind utility classes with dark mode (`dark:` prefix), glass-morphism effects, custom gradients
- Animations: Framer Motion wrappers (`MotionDiv`, `MotionButton` with `as any` cast)
- Reusable UI primitives in `ModuleShared.tsx`: `Highlight` (interactive tooltip), `ReadingSection` (content block), `MicroCommitment` (action prompt), `ActivityRing` (SVG progress)
- All source files carry Apache-2.0 license headers
- Constants use UPPER_SNAKE_CASE; components use PascalCase; handlers use `handle` prefix

## Notable Details

- User avatars generated via DiceBear API (`api.dicebear.com/9.x/notionists-neutral/svg`)
- Firebase config is in `firebase.ts`; hosting config in `firebase.json`
- Tailwind theme customization (fonts, colors) is in `index.html` via CDN config, not a tailwind.config file
- All module components use default exports for clean lazy-loading in `moduleRegistry.ts`

## Working With This Codebase

**Always build-check after changes.** Run `npm run build` AND `npm run lint` after any non-trivial change. Both must pass with zero errors and zero warnings (`--max-warnings 0`).

**Check for cascading effects.** After making changes to any file, verify that imports, navigation (both mobile AND desktop), and dependent components still work. Never assume a fix is isolated. Specifically: if you remove an import, grep for the name in the file to confirm it's truly unused. If you touch navigation, check both `MobileBottomNav` in App.tsx and any desktop sidebar. If you modify a hook's return type, check every consumer.

**Batch module awareness.** Changes to `ModuleLayout`, `ModuleShared`, the `ModuleTheme` type, or the module props interface can affect all 43 module files. Confirm the scope before editing.

**Tailwind CDN constraint.** Class strings must be written as full literals — never dynamically constructed (e.g. `` `bg-${color}-500` `` won't work). This is why `moduleThemes.ts` spells out every class per color. Any new theme tokens must follow this pattern.

**Creating a new module:**
1. Create `components/NewModule.tsx` — import a theme from `moduleThemes`, define `SectionDefinition[]`, use `ModuleLayout` + `ModuleShared` primitives, `export default`
2. Add a `lazy(() => import(...))` entry in `moduleRegistry.ts`
3. Add course metadata in `courseData.ts` (id, category, title, subtitle, description, sectionsCount, tags)

**Firestore security rules.** `request.resource.data` only exists for write operations. Never use it in `allow read` rules — it will silently fail all reads. Always split into separate `allow read` and `allow write` when write rules reference `request.resource.data`.

## Visual Design System — Module Components

### Core Colours

| Token | Hex | Usage |
|-------|-----|-------|
| Primary teal | `#2A7D6F` | Active states, slider thumbs, progress fills, CTA buttons, teal number badges |
| Primary teal dark | `#1a5a4e` | Button shadows, teal badge backgrounds |
| Teal light | `#e8f5f2` | Chip backgrounds, active card tints, callout backgrounds |
| Page background | `#f0f0f0` | Module page background (not the cream shell) |
| Card background | `#ffffff` | All cards without exception |
| Card border | `#1a1a1a` | Primary card border colour — thick, bold |
| Muted border | `#d0cdc8` | Secondary/inactive borders |
| Body text | `#1a1a1a` | Headings and primary text |
| Muted text | `#7a7068` | Subtitles, descriptions |
| Label text | `#9e9186` | Uppercase section labels |
| Productive blue | `#5B8FD4` | Only in productive/intrusive simulation pairs (Working Memory module) |
| Intrusive pink | `#E85D75` | Only in productive/intrusive simulation pairs — never used as general UI colour |

### What is NEVER acceptable
- Orange, amber, yellow backgrounds or buttons — any shade
- Bright green (e.g. #4ade80, #22c55e) — any shade
- Purple as a UI accent
- Red as a primary colour — only acceptable as a semantic "harmful thought" left-border accent
- Dark/near-black backgrounds (e.g. #1a1a2e, #0f2d3d) inside ANY module component
- Rainbow multi-colour card sequences (blue card, then orange card, then red card)
- Coloured card backgrounds as a general pattern — white only, with the one exception below
- Gradients on cards or backgrounds

### The One Colour Exception — Simulation Pairs Only
The blue (#5B8FD4) and pink (#E85D75) colour pair is permitted ONLY in interactive simulations that explicitly contrast productive vs intrusive cognition (e.g. Working Memory Under Threat). This is a deliberate semantic pair, not a general palette.

---

### Typography

| Element | Font | Size | Weight | Colour |
|---------|------|------|--------|--------|
| Module title | Source Serif 4 | 24–28px | 600 | #1a1a1a |
| Section heading | Source Serif 4 | 18–22px | 600 | #1a1a1a |
| Concept card term | Source Serif 4 | 15–16px | 600 | #1a1a1a |
| Body text | DM Sans | 14–15px | 400 | #3a3530 |
| Section label | DM Sans | 10–11px | 700 | #9e9186 — UPPERCASE, letter-spacing 0.12em |
| Muted description | DM Sans | 12–13px | 400 | #7a7068 |
| Score/stat number | Source Serif 4 | 32–48px | 700 | #2A7D6F |

---

### Card System

**Primary card** — default for all interactive elements:
- `background: white`
- `border: 2px solid #1a1a1a`
- `border-radius: 14–16px`
- `padding: 18–24px`

**Active/focus card** — for current input or selected state:
- `background: #e8f5f2`
- `border: 2px solid #2A7D6F`
- `border-radius: 14px`

**Muted/inactive card** — for locked or secondary states:
- `background: white`
- `border: 1.5px solid #d0cdc8`
- `border-radius: 14px`

**Callout** — for insight text, key takeaways:
- `background: #f0faf8`
- `border-left: 3px solid #2A7D6F`
- `border-radius: 0 10px 10px 0`
- `padding: 12px 16px`
- Text: italic, 14px, #1a6358

**Never**: coloured card backgrounds (blue, orange, yellow, red) as a general pattern.

---

### Buttons

**Primary CTA** — high-commitment actions only (Start session, Begin module):
- `background: #2A7D6F`
- `border-radius: 100px` (full pill)
- `border-bottom: 3px solid #1a5a4e`
- `box-shadow: 0 4px 0 #1a5a4e`
- `padding: 13px 28px`
- `font-size: 15px`, `font-weight: 600`, white text
- Press animation: `translateY(3px)`, shadow reduces

**Secondary action** — teal outline:
- `background: white`, `color: #2A7D6F`
- `border: 2px solid rgba(42,125,111,0.3)`
- `border-radius: 20px`, `padding: 10px 20px`

**Neutral action** — Reset, Cancel, inactive:
- `background: white`, `color: #7a7068`
- `border: 2px solid #d0cdc8`
- `border-radius: 20px`, `padding: 10px 20px`

**Ghost** — text-only:
- No border, no background
- `color: #9e9186`, `font-size: 13px`

**Never**: orange buttons, red buttons, multi-colour button sets where each button is a different colour.

---

### Chips & Pills

**Category chip** — above section titles:
- `background: #e8f5f2`
- `color: #1a6358`
- `border: 1px solid rgba(42,125,111,0.2)`
- `border-radius: 20px`, `padding: 4px 12px`
- Text: UPPERCASE, 10–11px, font-weight 700, letter-spacing 0.06em

**Detected/active chip** — when a quality is detected:
- `background: #e8f5f2`, `color: #1a6358`
- `border: 2px solid #2A7D6F`
- Prefix: `✓` in #2A7D6F

**Undetected/inactive chip**:
- `background: white`, `color: #b0a898`
- `border: 2px solid #d0cdc8`
- Prefix: `–` in #d0cdc8

---

### Interactive Element Patterns

**Numbered badges** (on concept cards, checklist items, stepper steps):
- Shape: circle OR rounded square (consistent within a component)
- Active/completed: `background: #2A7D6F`, white text
- Inactive/locked: `background: #d0cdc8` or `#e0dbd4`, `color: #9e9186`
- Size: 32–40px, font Source Serif 4, font-weight 700
- Never: orange, red, blue, or multi-colour numbered sequences

**Stepper/progress dots**:
- Active: `background: #2A7D6F`, size 40–44px
- Inactive: `background: #e0dbd4`, `color: #9e9186`
- Connector line: `background: #d0cdc8`, height 2px

**Sliders**:
- Thumb: teal rounded square — `#2A7D6F` ✓ (already correct in codebase — do not change)
- Track: `background: #e0dbd4`, height 6px
- Value label: `color: #2A7D6F`, never red
- Left/right endpoint labels: `color: #7a7068`, italic for example quotes

**Progress bars**:
- Fill: `background: #2A7D6F`
- Track: `background: #e0dbd4`, height 8px, border-radius full
- Percentage label: `color: #2A7D6F`
- Never: red fill (even when showing a low/warning value)

**Flip/reveal cards** (e.g. Hope Circuit Diagnostic):
- Front: white, `border: 2px solid #1a1a1a`, bold serif text centred
- Bottom label: `"TAP TO REVEAL"` — uppercase, 10px, #9e9186
- Revealed state: `background: #e8f5f2`, `border-color: #2A7D6F`

**Drag-to-reorder lists** (e.g. Pre-Drive Checklist):
- Row card: white, `border: 2px solid #1a1a1a`, `border-radius: 14px`
- Number badge: teal circle `#2A7D6F` — ALL items same colour, not rainbow
- Drag handle: `color: #d0cdc8`, left side
- Text: Source Serif 4, 16px, bold

**Connector arrows between steps** (e.g. Downward Arrow):
- Vertical line: 2px, `background: #d0cdc8`
- Chevron: inline SVG, `stroke: #2A7D6F`, strokeWidth 2.5
- Never: orange/amber arrows

---

### ConceptCardGrid — replaces ALL inline numbered lists

Whenever content has 3 or more named concepts with descriptions, use ConceptCardGrid from ModuleShared.tsx — never embed as "1) Term (description), 2) Term..." prose.

Card: white, `border: 2px solid #1a1a1a`, `border-radius: 14px`, `padding: 16–18px`
Number badge: teal circle, Source Serif 4, 14px bold, white text
Term: Source Serif 4, 15px, bold, #1a1a1a
Description: DM Sans, 12–13px, #5a5550
Highlight variant (key concept): `background: #e8f5f2`, `border: 2px solid #2A7D6F`, add "KEY LEVER" chip

---

### Tailwind CDN Constraint — Critical

All Tailwind class strings must be FULL LITERALS. Never dynamically construct classes like `bg-${color}-500` — the CDN scanner cannot detect these and they will not render. Use inline `style={{}}` props for any dynamic values (e.g. cell colours driven by state, progress bar widths, dynamic hex values).

---

### Build Verification

Always run `npm run build` after any non-trivial visual change. There are no tests or linters — the build is the only verification.

## Examiner reports library

`/examiner-reports/` holds State Examinations Commission Chief Examiner Reports and marking-scheme commentaries, structured per subject and year:

```
examiner-reports/
├── README.md
├── <subject>/
│   ├── <year>-chief-examiner.pdf      (original PDF, kebab-case subject slug)
│   ├── <year>-chief-examiner.md       (markdown extraction)
│   └── <year>-insights.md             (structured summary — schema below)
```

Multi-year syntheses use `<start-year>-<end-year>-` as the prefix (e.g. `2019-2022-chief-examiner.pdf`).

### Insights file schema

```
# [Subject] [Year] — Examiner Insights

## Source
Report type, year, level(s), original filename, renamed filename, brief
context if relevant (e.g. syllabus changes, cohort shifts).

## Common errors by question type
Broken down by paper section. For each question/area:
- Specific errors examiners flagged (with page refs)
- What separated higher-grade answers from lower-grade ones
- Direct examiner phrasing quoted where useful (with page refs)
Where the report distinguishes between Higher and Ordinary in its
commentary, preserve that distinction.

## Strategic / structural observations
Timing, question choice, rubric handling, anything about exam strategy.

## Misconceptions
Factual or conceptual errors the report flags as widespread.

## Quotable lines
2-3 examiner quotes that would land well in student-facing content
(with page refs).
```

### When to consult the library

When generating any of the following kinds of student-facing content, **read the relevant `<subject>/<year>-insights.md` file first**:

- "Common pitfalls" or "where students lose marks" sections
- `commonTraps` arrays in `data/examQuestions/<subject>.ts` entries
- `topAnswerIncludes` insights for new questions
- Subject strategy preambles in `data/examStrategy/<subject>.ts`
- Trap pattern descriptions in `data/examStrategy/trapPatterns.ts`

The insights file is the curated synthesis. The `<year>-chief-examiner.md` is there for deeper context or for pulling quotes the insights file didn't surface — read it when the insights file points at a section but doesn't quote the exact phrasing you need.

### Adding a new report

1. Drop the PDF into `/tmp/examiner-reports-batch/` (or `~/Downloads/` if staging is informal).
2. Read the cover page to determine subject, year(s), levels.
3. Move into `examiner-reports/<subject>/`, renamed to the canonical filename.
4. Convert to markdown (PyPDF2 if `pdftotext` is unavailable — see prior session for the conversion script pattern).
5. Author the insights file against the schema above.
6. Update `examiner-reports/README.md` index.

### Source types

The library holds two source types per subject/year:

- `<year>-chief-examiner.{pdf,md}` — SEC Chief Examiner's Report
- `<year>-marking-scheme.{pdf,md}` — SEC marking scheme

Both are examiner-authored and citable. Marking schemes are particularly useful for per-question rules ("Max X SRPs if…", "Apply a *", indicative material lists). Cite as `Marking scheme YYYY` inline.

## Strategiser content quality rules

Every Strategiser unit must consult the relevant report(s) in /examiner-reports/[subject]/ before generating debrief content. Cite the year inline (e.g. "Chief Examiner 2023 noted...").

Predict questions must test strategic understanding, not content knowledge. Good targets: genre identification, sub-task counting, mark allocation rules, ceiling/cap effects, time allocation, command-word interpretation. Bad: "what's the answer to part (a)" — that's content, not strategy.

Banned generic phrases (treat as failure modes — reject the draft if any appear):
- "Read the question carefully"
- "Manage your time"
- "Show your working"
- "Plan before you write"
- Any sentence that could apply to any exam in any subject

Good insights name a specific error pattern, a specific mark allocation rule, or a specific examiner observation. Examples:
- "Examiners noted in 2022 that candidates who skipped the Personal Response sub-task had their Coherence mark capped at the Purpose level."
- "1 attempt mark is awarded for writing the correct formula even if you can't complete the calculation."
- "Examiner reports flag that most lost marks on simultaneous equations come from compounded algebraic slips — substitute back into the original to catch them."

Per-question debrief is mandatory. Flat 'insights' lists are banned.

If you can't find an examiner-sourced insight for a particular point, flag it rather than filling with generic content.

### Schema enforcement

New questions in `data/examQuestions/<subject>.ts` MUST include:

- `biggestMistake`: question-level closing card (`{ title, body, source? }`)
- `predictPrompts[].debrief`: per-prompt block (`{ strategicPrinciple, commonWrongAnswer: { answer, reason, source? } }`)

Legacy fields (`topAnswerIncludes`, `commonTraps`, `markScheme`) are `@deprecated` and only present so existing questions continue rendering until migrated. Do not use them in new questions. Migration backlog: `/STRATEGISER_MIGRATION.md`.
