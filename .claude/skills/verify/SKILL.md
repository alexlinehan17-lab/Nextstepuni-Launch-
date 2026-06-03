---
name: verify
description: Run after any non-trivial change, before commit/deploy. Verifies the change end-to-end: gate + design/project checklists + (for substantial/UI changes) a second-agent review.
---

# verify

Verify a change end-to-end before you respond, commit, or deploy. Run **two passes**: verify → fix everything that fails → re-verify clean. Never report "done" off a single failing pass. The deterministic gate is non-negotiable; the checklists and second-agent review scale with the size of the change.

All commands assume cwd `/Users/alexlinehan/Nextstepuni-Launch-`.

## 1 — Deterministic gate (always)

Run the exact CI pipeline locally, in this order. CI (`.github/workflows/ci.yml`) runs the same four steps on every push/PR to `main`, so a clean local run = a green CI.

```bash
# 1. Lint — errors fail, legacy warnings tolerated
npm run lint:ci

# 2. Type check — THE real type gate; must print 0 errors
npm run typecheck

# 3. Tests — Vitest, single run (jsdom)
npm test

# 4. Production build — Vite/esbuild, emits dist/
npm run build
```

**What "pass" means**
- `lint:ci` — exit 0. ESLint with warnings tolerated (errors still fail).
- `typecheck` — exit 0 and **0 errors**. This is the type gate, not `build`.
- `test` — exit 0, no failing tests.
- `build` — exit 0, artifact in `dist/`.

**Caveats — read before you trust a result**
- **Heap / never bare `tsc`.** Always invoke `npm run typecheck`. It sets `--max-old-space-size=4096`; bare `tsc` OOMs at the default Node heap and gives a misleading crash.
- **`typecheck` IS the gate.** `npm run build` (esbuild) transpiles per-file and does **not** type-check. Type errors only surface in `typecheck`. After any non-trivial change run **both** `typecheck` and `build` before pushing — don't lean on CI to catch type breakage you skipped.
- **`typecheck` excludes test code.** `tsconfig` excludes `test/`, `vitest.config.ts`, `scripts/`, `functions/`. Type errors in those files won't appear in `typecheck` — validate them with `npm test`.
- **Strict lint is broken.** `npm run lint` (`--max-warnings 0`) fails on ~45 legacy unused-var warnings. Use `npm run lint:ci`. For fast iteration on just your edits, lint only changed files:
  ```bash
  npx eslint path/to/changed-file.tsx path/to/other.ts
  ```

## 2 — Design checklist (UI changes)

Pass/fail against the change. Any violation is a blocker — fix and re-run the gate.

- **Colour tokens in sync.** Accent orange `#F26B1F`, success green `#3A8D5F`. The hex literals must match across `design/tokens.ts`, `tailwind.config.ts`, and `index.html :root`. No teal `#2A7D6F` except pre-existing legacy.
- **Semantics: orange ≠ "good".** Orange = brand / action / selected (primary buttons, selected cards, active tabs, focus rings, in-progress fills). Green = correct / complete / positive (completion ticks, correct-answer feedback, healthy metrics). If you reached for orange to mean "good", switch to green.
- **Card backgrounds white only.** `#ffffff` + `border: 2px solid #1a1a1a`. No blue/yellow/amber/red/purple/lime card fills.
- **NO coloured left borders — ever.** Permanently banned. Never `borderLeft: '4px solid …'` or `border-l-4 border-…`. Use a dot indicator, a tinted fill (5–8% opacity), a top-bar accent, coloured text, or a coloured icon.
- **NO warm cream in module/analytical UI.** Ban `#FAF7F4` / `#FDF8F0` in Strategiser modules and analytical surfaces. Use cool neutrals: `#F0FAF8` light-teal callout (with `#F26B1F33` border) or pure white. Module page canvas is `#f0f0f0`. (Warm cream is fine only on the outer shell / Headspace celebration contexts.)
- **No banned colours.** No saturated amber/yellow/lime/purple/red as primary UI. No dark/near-black module backgrounds. No rainbow multi-colour card or button sequences. Numbered badges monochromatic (all accent, or accent/success for active/completed) — never orange-green-blue-yellow.
- **Reserved sim pair — `#5B8FD4` blue / `#E85D75` pink.** Per CLAUDE.md, these are reserved for productive-vs-intrusive cognitive simulation pairs (the Working Memory simulation concept) — never as general UI colour. Note the reality: `#5B8FD4` is currently unused anywhere in the codebase, and `#E85D75` has drifted — it appears in ~16 module files (`EffectiveStruggleAndGrowthModule`, `ProcrastinationModule`, `ExamCrisisManagementModule`, etc.) as a generic error/danger/negative indicator. Don't add new general-UI uses of `#E85D75`; keep new uses inside the cognitive-simulation context. A future refactor should consolidate the error-state drift.
- **Callouts use border-left, not full border.** Accent: `#FDEEDF` bg, `border-left 3px #F26B1F`, italic `#8C3A0E`. Success: `#E8F2EC` bg, `border-left 3px #3A8D5F`, italic `#1F5F3E`. (This left-accent is the one place a left edge is allowed — it is not a coloured card border.)
- **Primary CTA only for high-commitment actions.** Orange fill, pill (`border-radius 100px`), `border-bottom 3px #B54D14`, `box-shadow 0 4px 0 #B54D14`, press → `translateY(3px)`. Secondary/neutral buttons must NOT use this style.
- **No gradients** on cards, backgrounds, text, or bars (flat only). Subtle gradient is OK only inside immersive-deck colour worlds.
- **Typography.** Headings Source Serif 4 (`#1a1a1a`); body DM Sans (`#3a3530`); muted `#7a7068`; section labels `#9e9186` uppercase.
- **Tailwind JIT — full literal classes only.** Never construct `bg-${color}-500` or backtick-template class names; JIT can't scan them and they silently fail. Use inline `style={{}}` for dynamic hex/width/position values.
- **ConceptCardGrid for 3+ named concepts** (from `ModuleShared.tsx`) — never prose "1) Term… 2) Term…".
- **Animation encodes meaning** (Framer Motion / Three.js), never decorates. For learning/exam tools, prefer mistake-first pedagogy: wrong answer → commit → diagnostic visual reveal → fix.

**Immersive-deck exception — do NOT "fix".** The immersive colour-world decks — **How They Did It** (`components/HowTheyDidIt/index.tsx`) and **Career Paths** (`components/CareerPaths.tsx`), both reachable from the Innovation Zone, plus **Your Possible Life** (`components/YourPossibleLife.tsx`) — intentionally use bold colour-as-environment: full-bleed saturated colour-world cards, white text, chunky black border + hard shadow. These deliberately depart from the white-card rules above. They are *not* located inside `components/immersiveDeck/`, but they **consume** its shared primitives (`SwipeDeck`, `colorWorlds`, `Celebration`, `CountUp`) — reuse those primitives for any new colour-world deck rather than rebuilding. Never refactor these decks toward white/orange to "match" the module rules. (The `#5B8FD4`/`#E85D75` reserved pair belongs to the cognitive-simulation case above, not to these decks — don't conflate the two carve-outs.)

**What goes where (so you don't misroute a change):**
- **Module component** (`components/*Module.tsx`, ~55 of them) — white cards, accent/success rules apply in full.
- **Immersive colour-world deck** (How They Did It, Career Paths, Your Possible Life) — bold colour-as-environment; consumes `components/immersiveDeck/` primitives.
- **immersiveDeck primitives** (`components/immersiveDeck/`) — shared, presentation-only building blocks (`SwipeDeck.tsx`, `colorWorlds.ts`, `Celebration.tsx`, `CountUp.tsx`, `useDeckSound.ts`, `index.ts`); no standalone tool lives here.

## 3 — Project-correctness checklist

Non-visual checks. Apply the ones relevant to the change; each is pass/fail.

- **Firestore persistence — additive merge.** Writes must be `setDoc(doc(db,'progress',uid),{<namespace>:next},{merge:true})`. Never clobber sibling namespaces in `progress/{uid}`.
- **Firestore rules — read/write split.** Never reference `request.resource.data` inside `allow read` (it silently fails all reads). Split into separate `allow read` / `allow write` blocks when the write rule needs `request.resource.data`.
- **New Innovation Zone tool — register in all 5 spots:** (1) `InnovationZone.tsx` import, (2) `TOOL_CHROME`, (3) `tools` array, (4) `TOOL_CATEGORIES`, (5) `ToolIconBlob.tsx` union + `TOOLS` map. Reuse `components/immersiveDeck/` primitives for new colour-world decks.
- **New module — lazy-load + ModuleProps.** Register in `moduleRegistry.ts` via `lazy(() => import(...))` with a **default export**. Implement `interface ModuleProps { onBack: () => void; progress: ModuleProgress; onProgressUpdate: (progress: ModuleProgress) => void; }`. Include the Apache-2.0 header on any new source file.
- **Navigation — mobile AND desktop.** No router; nav is local state in `App.tsx`. Check both `MobileBottomNav` and desktop nav; never assume a nav fix is isolated to one surface.
- **Cascading changes.** Edits to `ModuleLayout.tsx`, `ModuleShared.tsx`, the `ModuleTheme` type, or the module props interface cascade to ~55 modules — confirm scope first, then verify with `typecheck` + `build`. Modifying a hook's return type → grep every consumer. After removing an import → grep the file to confirm it's truly unused.
- **GC ↔ student data — single source of truth.** College Compass / shared Guidance-Counsellor↔student models must read from one source-of-truth doc; never let the two views drift. Career Paths (`careerPathsData.ts`) links to CAO courses in `futureFinderData.ts` via `matchStrings` — keep that intact.
- **Exam content source-grounded + cited.** Every claim in student-facing exam content traces to `/examiner-reports/<subject>/<year>-insights.md` or `-chief-examiner.md`, cited inline. No model knowledge. Banned generic phrases: "Read the question carefully", "Manage your time", "Show your working", "Plan before you write" — anything that fits any subject. Good insights name a specific error pattern, mark rule, or examiner observation. Keep verbatim SEC paper text under the 15-words threshold. (Exam Strategiser was removed 2026-05-31; the reports library + citation discipline still stand.)
- **No GenAI integration.** There is no active GenAI. Any AI/LLM feature must go through `compliance/AI_GOVERNANCE_SCHEDULE.md` first — flag, don't ship.
- **DEIS audience.** Frame copy around autonomy, incremental progress, and belonging — not high-achievement gatekeeping.

## 4 — Second-agent review (before deploy / substantial changes)

For substantial or UI-affecting changes, get an **independent** review from an agent that did **not** write the code. Pick one:

- **Inline adversarial multi-dimension review** — fan out one reviewer per dimension (correctness, design-rules conformance, Firestore/data integrity, navigation coverage, content source-grounding). Each returns findings; then **verify every finding yourself** against the code before acting — discard the ones that don't hold up.
- **`/code-review ultra`** — the user-triggered cloud multi-agent deep review. Use for the highest-stakes changes.

Then: **fix confirmed findings → re-run Section 1 clean → re-check the relevant Section 2/3 items.** Treat a confirmed finding the same as a gate failure.

**Deploy is manual and gated on the user.** Push to `main` only runs CI (no auto-deploy). Going live is an explicit, manual step — `firebase deploy --only hosting` (→ https://nextstepuni-app.web.app) — and only on the user's explicit go-ahead. Merging to `main` is safe; deploying is not automatic.

## When to skip

Skip this skill for trivial doc/comment-only edits — README/Markdown prose, code comments, or text that touches no `.ts`/`.tsx`/config/rules. Everything else (logic, types, UI, modules, content, Firestore, nav, build/CI config) runs the full flow. When in doubt, at minimum run Section 1.
