# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

> **Read [CONVENTIONS.md](CONVENTIONS.md) first.** It documents how the codebase *actually* works (verified against the
> code) — component architecture, the visual/aesthetic registers, the Command-Word Reflex + Catch-Up Lane question
> patterns, the design tokens, Firestore patterns, golden examples, and a "Known inconsistencies" section. This file
> (CLAUDE.md) is the project/setup guide; CONVENTIONS.md is the build-a-feature guide. **If you learn a convention or
> correction during a session, add it to CONVENTIONS.md in the same PR.**

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

## Deployment

Pushing to `main` is publishing to the **live app** — there is no separate deploy step. `.github/workflows/deploy.yml` fires on every push to `main` and deploys to Firebase Hosting live (`channelId: live`, project `nextstepuni-app`). `.github/workflows/ci.yml` (lint → typecheck → test → build) runs in parallel, *not* as a pre-deploy gate, so a broken build can reach the live site before CI finishes.

**The "ship it" command.** When the user says **"ship it"**, push the change straight to `main`:
1. Verify locally first — `npm run typecheck` + `npm run build` (plus `npm run lint` and `npm test` for non-trivial changes). If any fail, STOP and report; do not push.
2. Commit with a clear, descriptive message.
3. `git push origin main` (retry with exponential backoff on network errors).
4. Confirm to the user that it's pushed and deploying.

Treat "ship it" as the user's explicit authorization to push to `main` and deploy live. Without it, keep changes on a branch / PR as normal.

## Architecture

**Stack:** React 19 + TypeScript, Vite, Tailwind CSS (v3, compiled at build time via PostCSS + autoprefixer — `tailwind.config.ts` + `index.css`, NOT a CDN), Framer Motion, Three.js (@react-three/fiber), Firebase (Auth + Firestore)

**Entry flow:** `index.html` → `index.tsx` → `App.tsx`

**App.tsx** (~780 lines) is a **data-assembly shell**: it pulls from `useProgress()`, runs the gameplay hooks, defines the `handleX` handlers, bundles them into a `routerProps` object, and renders `<AppRouter {...routerProps}/>`. The three cross-cutting concerns live in **contexts**, not App.tsx (see CONVENTIONS.md §1):
- Authentication + the initial progress read → `contexts/AuthContext.tsx` (`onAuthStateChanged`)
- Navigation (no router; a `ViewState` reducer + History-API sync) → `contexts/NavigationContext.tsx`; the view switch is `components/AppRouter.tsx`
- Progress persistence (Firestore `users/{uid}` + `progress/{uid}`) → `contexts/ProgressContext.tsx`

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

**Module component interface** — there is **no exported `ModuleProps` type**; every module is an `FC` with this inlined 3-field signature (don't add a `ModuleProps` import):
```typescript
{
  onBack: () => void;
  progress: ModuleProgress;                        // { unlockedSection: number }
  onProgressUpdate: (progress: ModuleProgress) => void;
}
```

**5 course categories** (`CategoryType` in `KnowledgeTree.tsx`; `categoryColorMap` in `courseData.ts`): `architecture-mindset`, `science-growth`, `learning-cheat-codes`, `exam-zone`, `subject-specific-science`. (`the-shield` / `the-launchpad` appear in older docs/comments but are not real categories.)

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
