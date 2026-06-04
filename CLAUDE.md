# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Nextstepuni is an educational platform ("Learning Lab") that teaches university-bound students advanced learning strategies through interactive modules. It's a React SPA with Firebase backend for auth and data persistence.

## Commands

```bash
npm install          # Install dependencies
npm run dev          # Start dev server (localhost:3000)
npm run build        # Production build via Vite (esbuild — does NOT type-check)
npm run preview      # Preview production build
npm run typecheck    # tsc --noEmit — the type gate (sets --max-old-space-size=4096)
npm run lint         # ESLint strict (--max-warnings 0) — the CI lint gate; currently clean
npm run lint:ci      # ESLint (errors fail; warnings tolerated) — legacy escape hatch
npm test             # Vitest unit/smoke tests
```

CI (`.github/workflows/ci.yml`) runs `lint` (strict, `--max-warnings 0`) → `typecheck` → `test` → `build` on every push/PR to `main`. Important: `npm run build` (Vite/esbuild) transpiles per-file and does **not** type-check — `npm run typecheck` is the real type gate (and it needs extra Node heap, hence the script flag).

## Environment

No environment variables are required for the current build. There is no active GenAI integration; see `compliance/GEMINI_AUDIT.md` for the audit trail. Any future GenAI integration must go through `compliance/AI_GOVERNANCE_SCHEDULE.md` first.

## Architecture

**Stack:** React 19 + TypeScript, Vite, Tailwind CSS (v3, compiled at build time via PostCSS + autoprefixer — `tailwind.config.ts` + `index.css`, NOT a CDN), Framer Motion, Three.js (@react-three/fiber), Firebase (Auth + Firestore)

**Entry flow:** `index.html` → `index.tsx` → `App.tsx`

**App.tsx** (~780 lines) is the central orchestrator. It manages:
- Authentication state via Firebase `onAuthStateChanged`
- User progress persistence (Firestore `users/{uid}` and `progress/{uid}` collections)
- Route-like navigation via local state (no router library — views switch based on state)

**Root-level modules:**
- `moduleRegistry.ts` — Lazy-loads ~83 registered modules (≈55 `*Module.tsx` component files; the per-subject modules all share one `SubjectModule.tsx`) + InnovationZone via `React.lazy()` with default imports
- `courseData.ts` — Course metadata definitions (titles, descriptions, categories, tags) and `categoryColorMap`
- `moduleThemes.ts` — Per-color Tailwind theme objects (literal class strings required for Tailwind's JIT content scan)
- `types.ts` — Shared types: `ModuleProgress`, `UserProgress`, `SectionDefinition`, `ModuleTheme`

**Key components in `components/`:**
- `Auth.tsx` — Login/registration modal with Firebase Auth. Admin login uses Firebase Auth with the `admin@nextstep.app` account (password managed in Firebase Console, not in code).
- `KnowledgeTree.tsx` — Main navigation hub showing categories with activity ring progress indicators
- `Library.tsx` — Grid view of modules within a category using `BentoModuleTile` components
- `AdminDashboard.tsx` — Admin-only analytics view
- `ModuleLayout.tsx` — Shared sidebar + content layout used by all educational modules
- `ModuleShared.tsx` — Reusable UI primitives: `Highlight`, `ReadingSection`, `MicroCommitment`, `ActivityRing`
- `*Module.tsx` (~55 files) — Individual educational modules, each using `ModuleLayout` with default exports

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
- Tailwind is compiled at build time (PostCSS + autoprefixer); config is `tailwind.config.ts`, directives in `index.css`. The hand-written `<style>` blocks in `index.html` are plain CSS, not Tailwind config. (A `cdn.tailwindcss.com` Workbox cache rule in `vite.config.ts` is a dead leftover — nothing loads Tailwind from a CDN.)
- All module components use default exports for clean lazy-loading in `moduleRegistry.ts`

## Working With This Codebase

**Always check after changes.** Run `npm run typecheck` AND `npm run build` after any non-trivial change (CI also runs `npm run lint` strict + `npm test`). `typecheck` must be clean (0 errors) — it's the real type gate; `build` alone does not type-check. `npm run lint` (`--max-warnings 0`) is now CLEAN and is the CI lint gate (the ~45 legacy warnings were burned down 2026-06-04) — keep it at zero; don't introduce new unused-var warnings.

**Check for cascading effects.** After making changes to any file, verify that imports, navigation (both mobile AND desktop), and dependent components still work. Never assume a fix is isolated. Specifically: if you remove an import, grep for the name in the file to confirm it's truly unused. If you touch navigation, check both `MobileBottomNav` in App.tsx and any desktop sidebar. If you modify a hook's return type, check every consumer.

**Batch module awareness.** Changes to `ModuleLayout`, `ModuleShared`, the `ModuleTheme` type, or the module props interface can affect all ~55 module files. Confirm the scope before editing.

**Tailwind JIT content-scan constraint.** Class strings must be written as full literals — never dynamically constructed (e.g. `` `bg-${color}-500` `` won't work). Tailwind's JIT scans the source files in `tailwind.config.ts`'s `content` globs for literal class strings; constructed names are invisible to it. This is why `moduleThemes.ts` spells out every class per color. Any new theme tokens must follow this pattern.

**Creating a new module:**
1. Create `components/NewModule.tsx` — import a theme from `moduleThemes`, define `SectionDefinition[]`, use `ModuleLayout` + `ModuleShared` primitives, `export default`
2. Add a `lazy(() => import(...))` entry in `moduleRegistry.ts`
3. Add course metadata in `courseData.ts` (id, category, title, subtitle, description, sectionsCount, tags)

**Firestore security rules.** `request.resource.data` only exists for write operations. Never use it in `allow read` rules — it will silently fail all reads. Always split into separate `allow read` and `allow write` when write rules reference `request.resource.data`.

## Visual Design System — Module Components

<!-- migration notes
Brand-accent pivot landed 2026-05-22:
  Old primary: teal #2A7D6F (with #1a5a4e dark, #e8f5f2 tint, #1a6358 dark text)
  New primary: orange #F26B1F (with #B54D14 dark, #FDEEDF tint, #8C3A0E dark text)
  New semantic: success green #3A8D5F (with #1F5F3E dark text, #E8F2EC tint)

Source of truth — all three layers must stay in sync when colours change:
  - design/tokens.ts            inline-style / SVG hex literals
  - tailwind.config.ts          named Tailwind tokens (accent, accentDark, success, …)
  - index.html :root            CSS variables consumed by bg-[var(--accent-hex)]

Token rename: the old `brand.teal` Tailwind token is gone. The top-level
`accent` token was the abandoned rust #CC785C pivot and is now the canonical
brand orange. Migration of the 700+ hardcoded #2A7D6F literals is happening
in phases — see git log for the per-step rollout.

Rule: orange (`accent`) is for brand accent and selected states. It does
NOT carry "good/correct/complete" semantics — use `success` for those.
The old "teal feels positive" coincidence does not carry over to orange.
-->

### Core Colours

| Token | Hex | CSS var | Tailwind | Usage |
|-------|-----|---------|----------|-------|
| Primary accent | `#F26B1F` | `--accent-hex` | `accent` | Active states, slider thumbs, progress fills, CTA buttons, accent number badges |
| Accent dark | `#B54D14` | `--accent-dark-hex` | `accentDark` | Button bottom-border + drop shadow, paired with the chunky-button language |
| Accent tint | `#FDEEDF` | `--accent-tint-hex` | `accentTint` | Chip backgrounds, active card tints, callout backgrounds |
| Accent dark text | `#8C3A0E` | `--accent-dark-text-hex` | `accentDarkText` | Italic body text inside accent callouts; readable on accent tint |
| Success | `#3A8D5F` | `--success-hex` | `success` | Positive/correct/complete states. NOT a brand colour |
| Success tint | `#E8F2EC` | `--success-tint-hex` | `successTint` | Backgrounds for success callouts and "good" pills |
| Success dark text | `#1F5F3E` | `--success-dark-text-hex` | `successDarkText` | Italic body text inside success callouts |
| Page background | `#f0f0f0` | — | — | Module page background (not the cream shell) |
| Card background | `#ffffff` | — | — | All cards without exception |
| Card border | `#1a1a1a` | — | — | Primary card border colour — thick, bold |
| Muted border | `#d0cdc8` | — | — | Secondary/inactive borders |
| Body text | `#1a1a1a` | — | — | Headings and primary text |
| Muted text | `#7a7068` | — | — | Subtitles, descriptions |
| Label text | `#9e9186` | — | — | Uppercase section labels |
| Productive blue | `#5B8FD4` | — | — | Only in productive/intrusive simulation pairs (Working Memory module) |
| Intrusive pink | `#E85D75` | — | — | Only in productive/intrusive simulation pairs — never used as general UI colour |

### Accent vs. success — the most important rule

These two colours are not interchangeable.

- **Accent (orange `#F26B1F`)** signals "this is the brand", "this is the action to take", "this is selected". Use it for primary buttons, selected cards, active tabs, focus rings, the brand number on a stat.
- **Success (green `#3A8D5F`)** signals "this is correct", "this is complete", "you got it right", "your reflection scored well". Use it for completion ticks, "Good" answer states, healthy metric zones, correct-answer feedback.

If you ever find yourself reaching for orange to mean "good" — stop, and use success instead. The fact that teal used to do double duty was a coincidence of the old palette. Orange does not carry that meaning.

### What is NEVER acceptable
- Bright/saturated extra accent colours outside the token system — any shade of amber, yellow, lime, etc., as a primary UI colour
- Bright green other than the success token (e.g. #4ade80, #22c55e) — any shade
- Purple as a UI accent
- Red as a primary colour — only acceptable as a semantic "harmful thought" left-border accent
- Dark/near-black backgrounds (e.g. #1a1a2e, #0f2d3d) inside ANY module component
- Rainbow multi-colour card sequences (blue card, then orange card, then red card)
- Coloured card backgrounds as a general pattern — white only, with the one exception below
- Gradients on cards or backgrounds
- Using the accent orange for completion/correctness — that's the success green's job

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
| Score/stat number | Source Serif 4 | 32–48px | 700 | #F26B1F |

---

### Card System

**Primary card** — default for all interactive elements:
- `background: white`
- `border: 2px solid #1a1a1a`
- `border-radius: 14–16px`
- `padding: 18–24px`

**Active/focus card** — for current input or selected state:
- `background: #FDEEDF` (accent tint)
- `border: 2px solid #F26B1F` (accent)
- `border-radius: 14px`

**Muted/inactive card** — for locked or secondary states:
- `background: white`
- `border: 1.5px solid #d0cdc8`
- `border-radius: 14px`

**Callout** — for insight text, key takeaways:
- `background: #FDEEDF` (accent tint)
- `border-left: 3px solid #F26B1F` (accent)
- `border-radius: 0 10px 10px 0`
- `padding: 12px 16px`
- Text: italic, 14px, `#8C3A0E` (accent dark text)

**Success callout** — for completion / correct / "you got it" moments:
- `background: #E8F2EC` (success tint)
- `border-left: 3px solid #3A8D5F` (success)
- `border-radius: 0 10px 10px 0`
- `padding: 12px 16px`
- Text: italic, 14px, `#1F5F3E` (success dark text)

**Never**: coloured card backgrounds outside the accent / success tint system. No blue, yellow, raw orange (use the tint), or red as card surfaces.

---

### Buttons

**Primary CTA** — high-commitment actions only (Start session, Begin module):
- `background: #F26B1F` (accent)
- `border-radius: 100px` (full pill)
- `border-bottom: 3px solid #B54D14` (accent dark)
- `box-shadow: 0 4px 0 #B54D14`
- `padding: 13px 28px`
- `font-size: 15px`, `font-weight: 600`, white text
- Press animation: `translateY(3px)`, shadow reduces

**Secondary action** — accent outline:
- `background: white`, `color: #F26B1F`
- `border: 2px solid rgba(242,107,31,0.3)`
- `border-radius: 20px`, `padding: 10px 20px`

**Neutral action** — Reset, Cancel, inactive:
- `background: white`, `color: #7a7068`
- `border: 2px solid #d0cdc8`
- `border-radius: 20px`, `padding: 10px 20px`

**Ghost** — text-only:
- No border, no background
- `color: #9e9186`, `font-size: 13px`

**Never**: multi-colour button sets where each button is a different colour. Buttons signalling "correct" or "complete" use the success token, not accent.

---

### Chips & Pills

**Category chip** — above section titles:
- `background: #FDEEDF` (accent tint)
- `color: #8C3A0E` (accent dark text)
- `border: 1px solid rgba(242,107,31,0.2)`
- `border-radius: 20px`, `padding: 4px 12px`
- Text: UPPERCASE, 10–11px, font-weight 700, letter-spacing 0.06em

**Detected/active chip** — when a quality is detected (positive feedback — use success):
- `background: #E8F2EC` (success tint), `color: #1F5F3E` (success dark text)
- `border: 2px solid #3A8D5F` (success)
- Prefix: `✓` in `#3A8D5F`

**Undetected/inactive chip**:
- `background: white`, `color: #b0a898`
- `border: 2px solid #d0cdc8`
- Prefix: `–` in #d0cdc8

---

### Interactive Element Patterns

**Numbered badges** (on concept cards, checklist items, stepper steps):
- Shape: circle OR rounded square (consistent within a component)
- Active (current step in a sequence): `background: #F26B1F` (accent), white text
- Completed (already done): `background: #3A8D5F` (success), white text
- Inactive/locked: `background: #d0cdc8` or `#e0dbd4`, `color: #9e9186`
- Size: 32–40px, font Source Serif 4, font-weight 700
- Never: multi-colour rainbow numbered sequences

**Stepper/progress dots**:
- Active step: `background: #F26B1F` (accent), size 40–44px
- Completed step: `background: #3A8D5F` (success)
- Inactive: `background: #e0dbd4`, `color: #9e9186`
- Connector line: `background: #d0cdc8`, height 2px

**Sliders**:
- Thumb: accent rounded square — `#F26B1F`
- Track: `background: #e0dbd4`, height 6px
- Value label: `color: #F26B1F`, never red
- Left/right endpoint labels: `color: #7a7068`, italic for example quotes

**Progress bars**:
- Fill (in-progress): `background: #F26B1F` (accent)
- Fill (completed): `background: #3A8D5F` (success)
- Track: `background: #e0dbd4`, height 8px, border-radius full
- Percentage label: matches the fill colour

**Flip/reveal cards** (e.g. Hope Circuit Diagnostic):
- Front: white, `border: 2px solid #1a1a1a`, bold serif text centred
- Bottom label: `"TAP TO REVEAL"` — uppercase, 10px, #9e9186
- Revealed state: `background: #FDEEDF` (accent tint), `border-color: #F26B1F`

**Drag-to-reorder lists** (e.g. Pre-Drive Checklist):
- Row card: white, `border: 2px solid #1a1a1a`, `border-radius: 14px`
- Number badge: accent circle `#F26B1F` — ALL items same colour, not rainbow
- Drag handle: `color: #d0cdc8`, left side
- Text: Source Serif 4, 16px, bold

**Connector arrows between steps** (e.g. Downward Arrow):
- Vertical line: 2px, `background: #d0cdc8`
- Chevron: inline SVG, `stroke: #F26B1F`, strokeWidth 2.5

---

### ConceptCardGrid — replaces ALL inline numbered lists

Whenever content has 3 or more named concepts with descriptions, use ConceptCardGrid from ModuleShared.tsx — never embed as "1) Term (description), 2) Term..." prose.

Card: white, `border: 2px solid #1a1a1a`, `border-radius: 14px`, `padding: 16–18px`
Number badge: accent circle `#F26B1F`, Source Serif 4, 14px bold, white text
Term: Source Serif 4, 15px, bold, #1a1a1a
Description: DM Sans, 12–13px, #5a5550
Highlight variant (key concept): `background: #FDEEDF` (accent tint), `border: 2px solid #F26B1F`, add "KEY LEVER" chip

---

### Tailwind JIT Constraint — Critical

All Tailwind class strings must be FULL LITERALS. Never dynamically construct classes like `bg-${color}-500` — Tailwind's JIT content scan cannot detect these and they will not render. Use inline `style={{}}` props for any dynamic values (e.g. cell colours driven by state, progress bar widths, dynamic hex values).

---

### Build Verification

Always run `npm run typecheck` and `npm run build` after any non-trivial visual change. Vitest smoke tests run via `npm test`; CI runs lint (strict) → typecheck → test → build.

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

## ⚠️ Exam Strategiser — REMOVED (redesign in progress)

> The Exam Strategiser tool was removed on 2026-05-31 (it had become
> overcomplicated and confusing). Deleted: `components/ExamStrategiser/`,
> `data/examStrategy/`, `data/examQuestions/`, `types/examStrategiser.ts`,
> `STRATEGISER_MIGRATION.md`. A new, simpler exam-strategy tool is being
> designed from research. The `examiner-reports/` library + the citation
> discipline above remain valid and will feed the new tool's agent-forged
> content pipeline. **Everything from here down describes the removed tool —
> kept only as redesign reference.**

## Necessary Knowledge tab (removed tool — reference only)

A third peer view inside the Exam Strategiser, alongside Practice and Trap Patterns. It teaches the *hidden curriculum* of the Leaving Cert — command words, marking-scheme grammars, time allocation, examiner pet peeves, SRPs, mark provenance, sanity checks, traps, ceilings, comparative integration, RSR section budgeting, Sciences phrase matching, Languages oral authenticity — material no syllabus covers but every Chief Examiner Report keeps complaining about.

The tab ships in **three groups with intentionally different aesthetic registers and depth**. Read the Aesthetic register section below before editing or adding modules — Stage 1 (Foundations) and Stages 2/3 (Tools / Subject Deep Dives) use different visual systems, and they shouldn't be mixed within a single module.

### Landing taxonomy (Foundations / Tools / Subject Deep Dives)

The landing is grouped into three stage clusters, mapped 1:1 to dossier interactive-concept priority:

- **Foundations (Stage 1)** — five fundamentals every LC student should learn first. Marking-grammar literacy, command-word interpretation, time-per-mark discipline, perennial CER complaints. The quieter Strategiser register.
- **Tools (Stage 2)** — five mistake-first interactives. Mark provenance, ceiling drops, sanity radar, trap detection. Bold register, animation-as-explanation.
- **Subject Deep Dives (Stage 3)** — four subject-specific simulators (English / History / Sciences / Languages). The same bold register, denser content. Where teachers can rarely reach — the precise mechanics that separate a top answer from a middle one.

The grouping reflects the dossier's E1-E22 priority ordering plus the user-facing pedagogy (literacy → interactive practice → subject-deep simulation). New modules fit into one of the three groups.

### Architecture

```
components/ExamStrategiser/
├── index.tsx                        # routes 'knowledge' view + module sub-views
└── knowledge/
    ├── NecessaryKnowledge.tsx       # tab landing — 3 groups + your-patterns panel
    ├── KnowledgeModuleShell.tsx     # Stage 1 shell (breadcrumb, why-card, summary)
    ├── QuickCheck.tsx               # Stage 1 reusable multi-choice quiz
    ├── knowledgePatterns.ts         # cross-module localStorage signals
    └── modules/
        # Stage 1 — Foundations (quieter Strategiser register)
        ├── CommandWordDecoder.tsx           # E1
        ├── PCLMAllocator.tsx                # E2 (Purpose Ceiling)
        ├── TimeAllocationCalculator.tsx     # E3 + sunk-cost simulator
        ├── ExaminerPetPeeveTrainer.tsx      # E12
        ├── MarkingSchemeGrammarExplainer.tsx
        # Stage 2 — Tools (bold instrument-panel register)
        ├── SrpIdentifier.tsx                # E10 — three-phase SRP heat map
        ├── WorkingShownAllocator.tsx        # E9 — mark provenance ribbons
        ├── SanityCheckTrainer.tsx           # E6 — absurdity radar SVG
        ├── SpotTheTrap.tsx                  # E4 — 30-sec timer + pattern card
        ├── SubTaskCeilingVisualiser.tsx     # E5 — bar-chart ceiling drop
        # Stage 3 — Subject Deep Dives
        ├── ComparativeTextsLinker.tsx       # E18 — SVG thread weaver
        ├── RsrSectionAllocator.tsx          # E19 — word-budget meter + slop
        ├── PhraseMatch.tsx                  # E17 — phrase constellation
        └── OralAuthenticityCoach.tsx        # E20 — diagnostic underline layers
```

Data lives in `data/knowledge/`:

Stage 1:
- `commandWords.ts` — 13 commands + 4 modifiers (dossier § A1)
- `examinerPetPeeves.ts` — 12 perennial peeves (§ B1-B11, § D)
- `subjectMarkingGrammar.ts` — 5 marking architectures (§ A2)
- `subjectTiming.ts` — 12 subject timing tables (§ A3)

Stage 2:
- `srpSamples.ts` — 4 paragraphs (Geo / History / Business) with per-sentence SRP classification, `developsFactor` and `buried` flag (§ A2, § B5-B7)
- `workedQuestions.ts` — 5 worked questions (Maths algebra/geometry, Chemistry mole calc, Physics mechanics, Accounting depreciation) with stepwise mark allocation, slip/blunder variants, and 5 answer paths each (§ A2)
- `sanityChecks.ts` — 12 absurdity questions (Maths / Chem / Phys / Bio) each with one correct + three absurd candidates, each absurd tagged with its primary catching check (§ C1)
- `trapCards.ts` — 15 paraphrased past-paper trap cards across 6 subjects + `TRAP_CATEGORY_LABELS` and `TRAP_CATEGORY_FIXES` lookup tables (multiple CERs)
- `ceilingScenarios.ts` — 4 cap-rule scenarios with sentence-level `isCapTrigger` flag and counterfactual `liftedScore` (§ A2, § A5, § B6, § B7)

Stage 3:
- `comparativeQuestions.ts` — 6 sample questions across 4 LC English Comparative modes (Theme/Issue, Cultural Context, General Vision, Literary Genre); each question has 3 widely-studied LC English texts (paraphrased descriptors only) plus a curated point bank of 4-6 mixed integrated/serial points with `integratedRewrite` counterfactuals (§ B1, § A5)
- `rsrConfig.ts` — 4 `RSR_SECTIONS` specs (mark-of-100 + HL/OL word ranges), 4 `SOURCE_EVAL_CHECKS` (Origin/Purpose/Value/Limitations) with signal-pattern arrays + prescriptions, 12 `SLOP_PATTERNS` regexes for Review-of-Process filler detection (§ A2, § B5)
- `phraseMatch.ts` — 18 questions across Biology / Chemistry / Physics; each question has 2-4 canonical key phrases with 3-7 acceptable paraphrases (substring-tolerant matcher) plus a model paragraph (§ B4)
- `oralCoach.ts` — language-keyed pattern banks for French / Irish / German / Spanish: `ORAL_PROMPTS` (11 sample prompts), `ROTE_PATTERNS` (~20 regexes), `TENSE_SIGNALS` (per-language tense detection patterns), `GENERIC_NOUN_SIGNALS` (~25 family/place patterns with personalisation prompts), plus paired `SAMPLE_ROTE_ANSWERS` and `POLISHED_EXEMPLARS` for the before/after view (§ B3, § B8)

Types in `types/knowledge.ts`. Every entry carries a `DossierRef { section, page, cite }` for audit traceability.

### Cross-module pattern signals (`knowledgePatterns.ts`)

Several modules write a pattern signal to `localStorage` at their closing screen. The landing reads these and surfaces them on a "Your patterns" panel above the Foundations group:

| Signal | Source module | What it captures |
|---|---|---|
| `sanityCheck` | `SanityCheckTrainer` | Weakest of the four checks (OoM / Units / Sign / Sub-Back) by accuracy across the session, plus per-check accuracy map |
| `spotTrap` | `SpotTheTrap` | Weakest trap category (modifier / plural-singular / etc.) by hit rate, plus per-category accuracy map |
| `comparative` | `ComparativeTextsLinker` | Last integration ratio (0..100) plus sample size |
| `ceiling` | `SubTaskCeilingVisualiser` | Number of cap-rule scenarios viewed (0..4) |

Storage key: `nk:patterns:v1`. Latest-write-wins per module — we keep the most recent observation, not a history. The shape is versioned so future migrations can ignore stale data cleanly. The panel renders only insights for which a signal exists; it disappears entirely when the user resets patterns or has run no modules yet.

Adding a new pattern signal: extend `PatternSignals` in `knowledgePatterns.ts`, add a `writePattern('newKey', { ... })` call inside the relevant module's closing screen, and extend `buildInsights()` in `NecessaryKnowledge.tsx` to render the new card with kicker / headline / body / openModuleId.

### Source-of-truth rule

Every claim in the Necessary Knowledge tab traces to `/docs/leaving-cert-knowledge-dossier.md`. The dossier itself draws on SEC marking schemes, Chief Examiner Reports, and NCCA documents. **Do not generate Necessary Knowledge content from your own knowledge of the Leaving Cert** — the dossier is the authority. If a claim does not appear there, flag it rather than write it.

Per-question or per-sample text that paraphrases an SEC paper must stay below the 15-words-verbatim threshold. The data files are the place where this rule is policed; if you find paraphrasing slipping above that threshold, fix the data file, not the rendering component.

### Aesthetic register — two parallel systems

**Stage 1 — Strategiser register** (quieter, matches the rest of `components/ExamStrategiser/`):
- Cards: `background: #FFFFFF`, `border: 1px solid #EDEBE8`, `border-radius: 16px`
- Highlight panels (callouts, "Why this matters", outcomes): `background: #FAF7F4`, `border: 1px solid ${ACCENT}33`
- Sliders: `accent-color: #F26B1F`
- ACCENT = `#F26B1F` (app-wide — import from `design/tokens.ts` rather than redeclaring locally)
- All Stage 1 modules share the `KnowledgeModuleShell` wrapper

**Stage 2 / Stage 3 — Brilliant.org / Mercury hybrid** (denser, more instrument-panel):
- Cards: `background: #FFFFFF`, `border: 2px solid #1a1a1a`, `border-radius: 16px`
- Cream panels: `background: #FDF8F0` for inset content (rewind tracks, paragraph displays, answer textareas)
- Inverted insight panels: `background: #1a1a1a`, `color: #FFFFFF`, `#FFD8A8` for warm highlights inside (a soft tan that pairs with the brand orange on dark surfaces — the only off-palette accent permitted there)
- ACCENT_DARK = `#B54D14`, INK = `#1a1a1a`, WARN = `#A8746E` (warm muted brown for cap/blunder semantics — **not** red)
- Stage 2/3 modules **do not use** `KnowledgeModuleShell`. They build their own minimal back-bar + hero + content stack so they can be visually denser
- Framer Motion is used freely for animation-as-explanation: provenance-trail entries, ceiling-drop springs, radar pulses, trap-reveal fades, thread weaving, bar chart drops. Animation must encode meaning — never decorate
- SVG for diagrammatic interactives: timer rings (`<circle>` with `stroke-dasharray`), absurdity radar (concentric `<rect>` rings), cap line (CSS dashed border), bar chart (`motion.div` height animations), comparative threads (cubic Bézier `<path>` with woven dips), phrase constellation (`<foreignObject>` HTML labels inside SVG starfield)
- For text-heavy diagnostic surfaces (Oral Coach), use wavy / dashed `text-decoration` underlines as the layer encoding, not coloured backgrounds — readability first

Banned palette colours (orange, amber, bright green, purple, red as a primary) apply across all three stages. Coloured left borders are banned project-wide (memory: `feedback_no_left_borders`); use background tints, full backgrounds, or dot accents instead.

### Stage 2 / Stage 3 visual primitives — what to reuse

Stage 2 and Stage 3 each introduced reusable visual idioms. Stage 3 specifically resisted lifting Stage 2 primitives into a shared `primitives/` folder because each idiom still has only one consumer; pre-emptive abstraction is more expensive than the duplication. **The threshold for lifting is the third consumer**, not the second.

| Idiom | Source module | Reusable for |
|---|---|---|
| **Three-phase student-then-examiner heat map** | `SrpIdentifier` | Any module where the educational arc is "predict → reveal → consequence". |
| **Mark-ribbon stack with running total** | `WorkingShownAllocator` | Any quantitative-marking module where steps accrue marks. The `Ribbon` component's `kind = 'earned' / 'slip' / 'blunder' / 'misread'` directly mirrors the dossier penalty grammar. |
| **Path-rewind picker with sparkline comparison** | `WorkingShownAllocator` | Any module that has multiple "what a student might do" trajectories with different scores. |
| **Absurdity radar SVG** | `SanityCheckTrainer` | Any module that needs a colour-keyed pulse around a target element. The four-check colour scheme (TEAL, TEAL_DARK, INK, WARN) is the canonical four-axis palette. |
| **Reaction-time-aware closing report** | `SanityCheckTrainer` | Any module where speed is a learning signal, not just accuracy. |
| **Three-state flip card with timer ring** | `SpotTheTrap` | Any module with a "spot it before the reveal" gameplay loop. |
| **Pattern-break interstitial every N items** | `SpotTheTrap` | Any module long enough to warrant a halfway-through pattern callout. |
| **Bar-chart ceiling drop with cap line** | `SubTaskCeilingVisualiser` | Any module visualising a marking-scheme cap or band ceiling. |
| **Sentence-level rewind sequencer** | `SubTaskCeilingVisualiser` | Any module that needs to walk a student backwards through their answer. |
| **Counterfactual lift animation** | `SubTaskCeilingVisualiser` | Any "what if you had X instead?" recovery interaction. |
| **Cross-text SVG thread weaver** | `ComparativeTextsLinker` | Any module showing relationships across N parallel columns. The cubic-Bézier with mid-point dip is the woven-feel idiom. |
| **Two-layer overlay bar (filled fill + outlined target)** | `RsrSectionAllocator` | Any module where progress vs target needs to be visible at a glance. |
| **Signal-pattern checker with prescription** | `RsrSectionAllocator` (Source Eval + Slop Detector) | Any module that detects keyword patterns in student text and surfaces examiner-voice prescriptions for misses. |
| **Phrase constellation (SVG starfield with `<foreignObject>` labels + matched-glow halos)** | `PhraseMatch` | Any module where matching against a fixed reference set is the core mechanic. |
| **Sequence-builder with model-order grading** | `PhraseMatch` (Reverse mode) | Any module where ordering matters as much as completeness. |
| **Toggleable diagnostic underline layers + tense strip** | `OralAuthenticityCoach` | Any module that overlays multiple independent diagnostic signals onto the same student text without making one cancel the others. |
| **Before/after compare (paired panes with shared diagnostic layers)** | `OralAuthenticityCoach` | Any module showing the cost/benefit of a rewrite via direct comparison. |

### Adding a new module

1. Author the data in `data/knowledge/<file>.ts`. New types go in `types/knowledge.ts`. Every entry carries a `source: DossierRef`. Re-export from `data/knowledge/index.ts`.
2. Add the module ID to `KnowledgeModuleId` in `NecessaryKnowledge.tsx` and a tile to `TILES` (set `stage: 1`, `2`, or `3`).
3. Create the component in `components/ExamStrategiser/knowledge/modules/<ModuleName>.tsx`.
   - **Stage 1 (Foundations)**: wrap in `<KnowledgeModuleShell>` with `whyThisMatters` and `summary`; close with a 3-question `<QuickCheck>`.
   - **Stage 2 / Stage 3 (Tools / Subject Deep Dives)**: build a minimal back-bar + hero + dense interactive body. Don't use the Stage 1 shell. Animation must encode meaning.
4. Wire it into `index.tsx`'s `KnowledgeModuleView` switch.
5. If the module's closing screen produces a personalised insight, add a `writePattern('<key>', { ... })` call to capture it for the cross-module "Your patterns" panel. See `knowledgePatterns.ts` for the registered keys; extend the `PatternSignals` interface and `buildInsights()` in `NecessaryKnowledge.tsx` to surface it.
6. `npm run typecheck` + `npm run build` to verify clean.
7. Commit per module if it's a significant standalone shipment.

### Stage roadmap

The dossier defines E1-E22 interactive concepts.

- **Stage 1 (shipped):** E1 Command Word Decoder, E2 PCLM Allocator, E3 Time-Allocation Calculator, E12 Examiner Pet-Peeve Trainer, Marking-Scheme Grammar Explainer.
- **Stage 2 (shipped):** E10 SRP Identifier, E9 Working-Shown Allocator, E6 Sanity-Check Trainer, E4 Spot the Trap, E5 Sub-task Ceiling Visualiser.
- **Stage 3 (shipped):** E18 Comparative Texts Linker (English), E19 RSR Section Allocator (History), E17 Marking-Scheme Phrase Match (Sciences), E20 Oral-Exam Authenticity Coach (Languages — French / Irish / German / Spanish).

### Post-Stage-3 deferred backlog

The following dossier concepts remain candidates for future expansion. Do not build pre-emptively; defer until analytics show which Stage 1-3 modules drive the most engagement and the most measurable score lift. Re-prioritise from there.

- **E22 Time-of-Day Pacing Coach** — real-time exam simulator; gives the student a paper, sets the clock, throws prompts at calculated intervals ("10 minutes left for question 3"; "you should be finishing the comparative now"). Trains internal pacing. Heavy on state management; useful only if students will commit to running a 3-hour mock inside the app.
- **E15 Genre Identifier (English Question B)** — student is given a Question B prompt; tool asks: is this a letter, blog, podcast, speech, article, diary, editorial? Shows genre conventions, length expectations, common errors per genre. Useful if Composition genre-misjudging shows up as a dominant Stage 1 pattern.
- **E13 Diagram Annotation Practice (Geography / Biology / Physics)** — student is given an unannotated diagram and a question; must drag annotation labels to correct positions. Distinguishes labelling from annotating. Heavy on diagram authoring; defer until the SRP Identifier surfaces diagram-mark patterns as a real student weak spot.
- **E11 PCLM Comment Translator (English)** — student pastes a marker comment ("Your purpose drifts in paragraph 3"); tool explains which PCLM band is affected and what to fix. Useful adjunct to the PCLM Allocator (Stage 1) once students start having mock-graded comments to feed in.

When the third consumer of any Stage 2/3 visual primitive lands, lift the primitive into `knowledge/primitives/` *before* duplicating the implementation a third time. The current modules each own their primitives inline because the implementation cost of a generic version is higher than two copies.

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
