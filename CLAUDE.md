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

## Module accreditation & evidence dossier

The educational modules are being reviewed for accreditation (DCU / Brian MacCraith). The governing rule for **all module content**:

> Only state or advise something where peer-reviewed literature supports it. **Never attach a citation you cannot verify points to a real, locatable paper (a resolvable DOI / database record) that genuinely supports the specific claim.** If a claim can't be backed by a verifiable source, reframe it to non-prescriptive language or cut it — never invent a citation to keep it.

Verify DOIs against CrossRef (`https://api.crossref.org/works/<doi>`) before citing; PubMed, Europe PMC and Unpaywall are available for abstracts/open-access checks. A specific figure whose primary source is paywalled and unconfirmable gets reframed to the qualitative claim the abstract supports.

**When working through OR completing a module's review, you MUST record it in the repo dossier — this is mandatory, not optional:**

1. **Dossier** — create/update `compliance/evidence/<module-slug>.md` with the verified reference table (DOIs + how each was verified) and a claim-by-claim record. This is the document reviewed for accreditation, and it must be written/updated **in the same change** as any content edit — the dossier never lags the app.
2. **Reference data** — verified sources live in `data/references/<module>.ts` (typed by `data/references/types.ts`) as an ordered list whose order defines the inline citation numbering. Surfaced in-app via `Cite` (faint superscript marker) + a module-wide **References** button that `ModuleLayout` renders when the module passes its ordered list to the `references` prop (desktop: beside the progress wheel; mobile: top of the Sections drawer). The button opens `ReferencesModal` (`components/ModuleReferences.tsx`). Do NOT use per-section "evidence" footers. Keep the in-app references and the dossier in sync.
3. **Cut log** — every removal or reframe is appended to `data/cutContent.ts` (shown on the home-sidebar **Cut Content** page), with the verbatim original, the reframed replacement, and the reason.

Pilot reference implementation: **Mastering Active Recall** (`compliance/evidence/active-recall.md`, `data/references/activeRecall.ts`). Follow its shape for subsequent modules.

## Architecture

**Stack:** React 19 + TypeScript, Vite, Tailwind CSS (v3, compiled at build time via PostCSS + autoprefixer — `tailwind.config.ts` + `index.css`, NOT a CDN), Framer Motion, Three.js (@react-three/fiber), Firebase (Auth + Firestore)

**App.tsx** (~780 lines) is a **data-assembly shell**: it pulls from `useProgress()`, runs the gameplay hooks, defines the `handleX` handlers, bundles them into a `routerProps` object, and renders `<AppRouter {...routerProps}/>`. The three cross-cutting concerns live in **contexts**, not App.tsx (see CONVENTIONS.md §1):
- Authentication + the initial progress read → `contexts/AuthContext.tsx` (`onAuthStateChanged`)
- Navigation (no router; a `ViewState` reducer + History-API sync) → `contexts/NavigationContext.tsx`; the view switch is `components/AppRouter.tsx`
- Progress persistence (Firestore `users/{uid}` + `progress/{uid}`) → `contexts/ProgressContext.tsx`

**Auth.tsx** — admin login uses Firebase Auth with the `admin@nextstep.app` account; the password is managed in the Firebase Console, not in code.

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
- Styling: the shared parts in `components/ui/` and the tokens in `index.css` (see "Visual Design System" below); Tailwind utility classes for layout, with `dark:` where a token does not already cover dark mode. No glass, no gradients
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

The whole app, modules included, is one agreed design system: "the sign-in standard", chosen by Alex on
24 November 2026 and settled screen by screen on 26 November 2026. It replaced the look this section used to
teach (orange pill buttons with a hard shadow, Source Serif headings, 2px ink cards, tinted chips, callouts
with a coloured side rail). Do not bring any of that back.

**The specification** is the design skill, `~/.claude/skills/nextstepuni-design/` (`SKILL.md`, its "Never
ship" table, and `references/`: `tokens.md`, `components.md`, `navigation.md`, `mobile.md`, `patterns.md`,
`motion.md`). Alex's rulings in `references/decisions.md` outrank everything else, this file included. Any UI
work starts there. The rules in brief:

- **One typeface**, ABC Diatype, sentence case, through the named type styles in `index.css` (`t-title`,
  `t-heading`, `t-row`, `t-body`, `t-sub`, `t-meta`, `t-label`; `t-readout` / `ui-readout` is the mono,
  Departure Mono, for timers, counters, dates and citations). Headlines are regular weight. No serif, no
  italic for emphasis, no text under 11px (11px only in the small capitals label).
- **The page is white** (dark: `#181818`). Depth is four levels: on the page (read it), a box with a 1px line
  and no shadow (press it), the one raised sheet per screen (`--lift`), and floating layers (menus, sheets,
  messages; `--float`). Content that cannot be pressed is not boxed: lay it on the page under a hairline.
- **Charcoal does the work**: one charcoal main button per view (`--action`). There is no orange button,
  fill, border, tint or tab marker. **Chosen is an ink outline** with a drawn tick (round for "pick one",
  rounded square for "pick several").
- **Orange (`--nsu-orange`, `#eb692a`) belongs to the artwork**: the Star Crew, each tool's drawing, the
  wordmark's full stop, one live word, and the student's own value in a graph. Onboarding's own pages keep
  `#f26b1f` (`--setup-orange`). **Green (`--success-hex`) is for done and correct** marks; feedback
  sentences are ink, never green text.
- **Never**: emoji, sparkle or rocket icons, an icon in a tinted tile, pills or tinted tags, a coloured
  stripe down one side of anything, gradients, glows, cream, a grey page or a grey-filled control, a hard
  offset shadow, a box inside a box, a centred pop-up card on a phone (except the two-button confirm), a
  top-right X, two leave controls on one screen, a target under 44 x 44.
- **Each screen keeps its character**: the system is the frame (bars, the one leave control, margins, type,
  buttons, chosen state, colours, safe areas); a screen's own drawing, headline, pictures and graphs stay.

**In the code** the system lives in three places; use them, never a hand-made copy:

- **Tokens**: the `:root` and `.dark` blocks at the top of `index.css` (surfaces `--surface-canvas`,
  `--surface-paper`, `--surface-soft`, `--surface-raised`; ink `--ink-primary`, `--ink-secondary`,
  `--ink-muted`; lines `--hairline`, `--outline-soft`, `--outline-strong`; `--action`; spacing `--space-*`;
  radii `--r-*`; motion `--t-*`, `--ease-*`), mirrored for TypeScript in `design/tokens.ts` and for Tailwind
  in `tailwind.config.ts`. Inside the module reader the `--module-*` names (`components/learning/`) carry the
  same roles.
- **Shared parts**: `components/ui/` (Button, TextButton, IconButton, Choice, Menu, Sheet and Confirm,
  OverScreen, Message and StandingMessage, TopBar / TabBar / PinnedFooter in `Bars.tsx`, PageHeader, Row and
  List, CheckRow, the selection bar (`HorizontalTabs`), Field and SearchField, EmptyState / LoadingShape /
  ErrorState in `States.tsx`) with `parts.css`, and the frame (`frame.css`, `Frame.tsx`), which owns the
  safe areas: only the bars, the pinned footer, sheets and full overlays touch a screen edge. When a part
  cannot do what a screen needs, extend the part (with its test), then use it.
- **Guards** that only go down: `test/colourLiterals.guard.test.ts` (a typed colour), `test/sharedParts.guard.test.ts`
  (a hand-made button, menu, pop-up or header) and `test/frameEdges.guard.test.ts` (a screen positioning
  against the raw edge). Lower a baseline with the `*_UPDATE=1` run each header describes; never raise one.

The simulation pair blue `#5B8FD4` / pink `#E85D75` remains the one sanctioned off-token pair, and only in
simulations that contrast productive and intrusive cognition (Working Memory Under Threat).

---

### ConceptCardGrid — replaces ALL inline numbered lists

Whenever content has 3 or more named concepts with descriptions, use ConceptCardGrid from ModuleShared.tsx — never embed as "1) Term (description), 2) Term..." prose.

Its look comes from the system above (no 2px ink card, no orange badge, no serif); change it in the shared
component, never per module.

---

### Tailwind JIT Constraint — Critical

All Tailwind class strings must be FULL LITERALS. Never dynamically construct classes like `bg-${color}-500` — Tailwind's JIT content scan cannot detect these and they will not render. Use inline `style={{}}` props for any dynamic values (e.g. cell colours driven by state, progress bar widths, dynamic hex values).

---

### Build Verification

Always run `npm run typecheck` and `npm run build` after any non-trivial visual change. Vitest smoke tests run via `npm test`; CI runs lint (strict) → typecheck → test → build.
