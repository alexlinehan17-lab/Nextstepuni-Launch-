# CONVENTIONS.md

How this codebase actually works, so a fresh session can build a feature **indistinguishable from existing work**.
This documents **reality** (verified against the code 2026-06-10), not aspiration. Where the code and `CLAUDE.md` /
memory disagree, both sides are named in **§9 Known inconsistencies** — no winner is picked there.

Stack: React 19 + TypeScript, Vite, Tailwind v3 (PostCSS build, **not** CDN), Framer Motion, Firebase (Auth + Firestore).

> **Maintenance rule:** if you learn a project convention or correction during a session, add it to this file in the
> same PR. This is the file that reaches a cloud session — keep it true.

---

## 1. Component architecture — how a feature is wired in

There are **three distinct kinds of thing** and they wire in differently. Know which you're building.

**A standalone VIEW** (a top-level screen). There is **no router library**. A "view" is the `ViewState` string union in
`contexts/NavigationContext.tsx`. Adding one means touching **five sites or it's unreachable**:
1. the `ViewState` union (`NavigationContext.tsx:12-16`)
2. the `VALID_VIEWS` Set (`:65-70`)
3. the `NavigationAction` union + a reducer `case` (`:107-145`)
4. a `navigateToX` `useCallback` on the context value (`:273-340`)
5. a render branch in `components/AppRouter.tsx` (`:297-644`)

Copy an existing case end-to-end (e.g. `NAVIGATE_TO_INSIGHTS`). Navigation is **`useReducer` + manual History API
sync**, not `useState`. Components never call `setViewState`; they call `const nav = useNavigation(); nav.navigateToX()`.
Each `navigateX` runs `window.scrollTo(0,0)` then dispatches; `goBack()` is `window.history.back()`. The URL is the
source of truth for deep-links (`?view=&cat=&mod=&tool=&from=journey`); state is the runtime truth. A
Firebase email-action guard (`isAuthActionRequest` in `utils/authActionLink.ts`: the `/reset-password` path, or a known `mode` + `oobCode`) skips URL-sync so the one-use `oobCode` survives.

**`AppRouter` is the single switch**, in strict precedence: Firebase email-action link (`AuthActionPage`, which dispatches on `mode`: reset password, confirm email, recover email) → `!userResolved` spinner → `!user`
LoginPage → `needsPasswordChange` → `isAdmin` AdminDashboard → `role==='gc'` GCDashboard → `needsOnboarding` Onboarding →
the per-`viewState` `if`-chain → `FallbackRedirect` to `tree`. Add new student views as another `if (viewState === 'x')`
before the fallback. Every non-eager view is `lazy(() => import('./X'))` wrapped in
`<Suspense fallback={<LoadingSpinner/>}>`; only `KnowledgeTree` + `Library` are static/eager. `AppRouter` does **zero**
data fetching — it reads contexts + a props bag and switches.

**`App.tsx` is a data-assembly shell** (not the auth/nav owner — see §9). It pulls from `useProgress()`, runs the gameplay
hooks (`useGamification`, `useStrategyMastery`, `useQuests`, `useRecommendation`…), defines every `handleX` handler,
bundles them into one `routerProps` object, and renders `<AppRouter {...routerProps}/>`. New cross-view data/handlers go
into `routerProps` (`App.tsx:603-621`) **and** the `AppRouterProps` interface (`AppRouter.tsx:109-184`).

**Provider nesting is load-bearing** (`index.tsx:47-64`): `ErrorBoundary > ToastProvider > AuthProvider >
ProgressProvider > NavigationProvider > MotionConfig > App`. `ProgressContext` and `NavigationContext`
both consume `AuthContext` — never reorder so a consumer sits above its provider.

**An educational MODULE** (~83 of them, registered in `moduleRegistry.ts`) is **not** a view. A module is reached via
`viewState='module'` + `currentModuleId`; `AppRouter` does a dictionary lookup `moduleComponents[currentModuleId]` and
renders it inside `<ModuleErrorBoundary>` + Suspense with **exactly three props** `{onBack, progress, onProgressUpdate}`.
Adding a module does **not** touch `ViewState`/`AppRouter`. Two steps:
1. `'<kebab-id>': lazy(() => import('./components/NewModule'))` in the `moduleComponents` map (default export only).
2. a metadata record in `courseData.ts` `COURSE_DEFINITIONS`. **The registry key === the courseData id.**

Per-subject modules reuse the shared `SubjectModule` via `createSubjectModule('<subjectKey>')` in `moduleRegistry.ts` —
do **not** hand-write a per-subject file.

**An Innovation-Zone TOOL** (CommandWordReflex, CatchUpLane, …) is neither a view nor a module. It's a standalone tool
body rendered inside `InnovationZone`, props `{ uid?: string; studentSubjects?: string[] }`, self-routing via local
state. See §4. Each tool entry in the `InnovationZone.tsx` tools array carries a **`curriculum` tag** — the gate hides any
tool not tagged `'both'`/`'junior'` from Junior Cycle students (`const tag = t.curriculum ?? 'senior'` — **an absent tag
defaults to `'senior'`, i.e. JC-invisible**). So a tool that surfaces `jc-` content MUST be tagged `'both'` (or `'junior'`),
or JC students can't see it. `test/jcToolVisibility.test.ts` enforces this. Subject-name matching across cycles strips the
trailing parenthetical (`baseName()` → `"Science"` matches `"Science (Junior Cycle)"`).

**Mobile nav** = `MobileBottomNav`, defined inline in `App.tsx:50-102`, 6 tabs, `createPortal`'d to `document.body`
(so a transformed ancestor can't re-anchor it), `md:hidden`, active when `tab.id===viewState`, hidden on
onboarding/module/admin/gc. Desktop nav is the Kobra sidebar, `components/navigation/NextStepUniSidebar.tsx` (grouped
items; a new destination gets an item there). The **mobile app design** (`useMobileAppDesign`: phones AND iPads, chosen by
device, not width) mounts no sidebar at any width: account, settings and secondary destinations live in
`MobileProfileSheet` (`UserProfileMenu.tsx`), opened from Home's avatar. That sheet must work at tablet widths too — iPads
have no other way in — so a new destination gets a row there as well as a sidebar item.

---

## 2. The two surface registers — ToolHeader vs SectionCard

Both are **real component files** with their own docblocks ("sister components, different surface, different role").

- **`components/ToolHeader.tsx`** — the Innovation-Zone *tile-list* / Training-Hub header. Cream ground `#FAFBF6`, **no**
  border, **no** shadow, a 108px square saturated-colour tile on the left holding a white-ink SVG, then eyebrow + serif
  title + sans subtitle. Props `{themeColor, eyebrow, title, subtitle, icon?|iconImage?|iconBlob?, className?}`.
  Consumers: `InnovationZone.tsx`, `TrainingHub.tsx`. It replaced the legacy flat-coloured banner.
- **`components/SectionCard.tsx`** — the home-dashboard nav tile (Modules / Innovation Zone / My Progress / Learning
  Paths). White card, `1px #EDEBE8` border, soft shadow, painted-blob + ink illustration tile, eyebrow/serif title/sans
  subtitle, a right arrow that slides in on hover, 2px hover-lift. Props `{eyebrow, title, subtitle, icon, onClick?,
  className?}`. Consumer: `KnowledgeTree.tsx`.

**Critical:** the IZ *content tools* (`CommandWordReflex`, `CatchUpLane`) render **neither** — confirmed they import
neither. The ToolHeader band belongs to the InnovationZone tile list, not to a tool body. Inside a tool, identity is
carried by a per-tool colour trio + the shared **`cardShell`** literal (copy verbatim):

```
w-full max-w-xl mx-auto rounded-2xl border-2 border-[#1A1A1A] dark:border-zinc-700
bg-white dark:bg-zinc-900 shadow-[4px_4px_0_0_#1A1A1A] dark:shadow-[4px_4px_0_0_#3f3f46] p-6 md:p-7
```

White card, 2px ink border, **hard 4px offset shadow (no blur)**, `rounded-2xl`. List/tile rows use the 3px-shadow
variant + `hover:-translate-y-0.5`. Each tool declares its own identity hex consts at module top (not in `design/tokens`):
CatchUpLane `CYAN #0E9AA8 / #E6F4F5 / #0A5560`; CommandWordReflex `INDIGO #6366F1 / #EEF0FF / #3730A3` (+ an amber
highlighter pair). Only `success`/`accent` come from `COLORS`.

---

## 3. The three aesthetic registers (with live exemplars)

The ExamStrategiser exemplars CLAUDE.md once named are **deleted**. The live ones:

- **Headspace — bold-colour-environment.** Each card **owns a saturated identity colour as its background** (not a
  tint/border), white text, translucent-white chips `rgba(255,255,255,0.18–0.25)`, soft circle "blob" overlays. Colours
  from the `WORLDS` palette in `components/immersiveDeck/colorWorlds.ts`. **Exemplar:**
  `components/journey/PeerIslandsList.tsx`. Use for celebratory / social / identity screens.
- **Mercury — data-dense.** White cards, restrained `1px #EDEBE8` borders, confident large numerals (`text-4xl/5xl`),
  no decoration, generous whitespace, muted neutral labels. **Exemplar:** `components/CAOPointsSimulator.tsx` (the Points
  Summary card). Note: code-Mercury is neutral + orange-accented — the memory's "lavender" is **not** in code, and purple
  is banned (§9 #7). Use for dashboards / stats.
- **Brilliant.org — mistake-first / instrument-panel.** White cards, bold `2px solid #1a1a1a` borders, radius 16,
  mistake-first pedagogy (lead with the wrong choice, visualise the mark consequence), Framer Motion where animation
  **encodes meaning**, SVG diagrammatic interactives, inset cream allowed (`#FDF8F0`). **Exemplar:**
  `components/ExamCrisisManagementModule.tsx`. Use for dense interactive learning tools + module simulators.

Cross-register primitives: `components/immersiveDeck/HybridCard.tsx` `PrimaryButton`/`SecondaryButton`;
`components/ui/PrimaryActionButton.tsx` (the IZ orange CTA). **Always import Motion from `components/Motion.tsx`**
(`MotionDiv = motion.div as any`, the React-19/Framer workaround) — never from `'framer-motion'` directly.

The IZ content tools are a de-facto **4th idiom**: the chunky `cardShell` neobrutalist look (§2), not any of the three
module registers and not `ModuleLayout`.

---

## 4. Question-display patterns — Command-Word Reflex + Catch-Up Lane

**Shared skeleton.** Both are `React.FC<{ uid?: string; studentSubjects?: string[] }>`, self-routing via local `useState`
state machines, returning early per state. Both share: the `cardShell` string, `AnimatePresence mode='wait'` over a
single `MotionDiv` keyed per item+phase, the `fade` transition `{initial:{opacity:0,y:10}, animate:{opacity:1,y:0},
exit:{opacity:0,y:-8}, transition:{duration:0.22}}`, a Higher/Ordinary toggle, and a cycle-grouped subject picker.
Typography is set **inline** (not Tailwind font classes): serif `fontFamily:"'Source Serif 4', serif"`, body
`"'DM Sans', sans-serif"`; uppercase micro-labels `text-[11px] font-bold tracking-[0.14em]` in `#9e9186`.

**Command-Word Reflex** — state `view 'home'|'play'` + `phase 'spot'|'reveal'`. The cue-detection algorithm (verbatim,
`components/CommandWordReflex/index.tsx`): split the stem `q.stem.split(/(\s+)/)` (whitespace preserved);
`const norm = (s) => s.replace(/[^a-zA-Z]/g,'').toLowerCase();`; build a `Set<number>` of cue indices by sliding a window
of the command word's tokens over the non-whitespace token positions — this supports **multi-word cues** ("Account for",
"To what extent", "Tabhair fáth amháin"). The stem renders as inline tokens in one `<p>` (18px serif); word tokens are
`<button>`s, whitespace is plain `<span>`. Correct first tap → `solve(firstTry)` where `firstTry = wrong.size===0 &&
!usedReveal`; a wrong tap adds the index to a `wrong: Set<number>` (line-through `#b0a898`); "Reveal it" sets
`usedReveal` and solves false. Reveal phase highlights the matched cue (amber `HL_BG #FDE68A / #92400E`), then a
**demand** panel (indigo tint) + a **trap** panel (amber tint, footer `{q.source} · ~{q.marks} marks at stake`).

**Catch-Up Lane** — a 5-beat machine `gist→move→check→reveal→done` (but only 3 progress dots; `check`+`reveal` share
index 2). The self-check is **local-only, never persisted**: `check` shows `check.prompt`; `reveal` shows
`check.modelAnswer` + maps `check.needed[]` to tappable tick-rows. **No correctness gate** — a student can tick zero and
still mark the topic recovered.

**Figure + SEC attribution (both tools, copy verbatim).** When `figure` exists, render a `<figure>` **above** the stem:
`2px solid #1A1A1A` border, `rounded-xl`, `<img src alt loading="lazy">`, then a `<figcaption>` carrying `figure.source`
(the `© State Examinations Commission` attribution) on the tool's tint. Assets live under
`public/exam-figures/<subjectSlug>/`, cropped via `tools/extract_exam_figure.py`. Catch-Up also renders an optional
`passage` **verbatim** in a `whitespace-pre-line` serif panel.

**Level filter (identical).** A two-segment Higher/Ordinary pill toggle; predicate
`q.level==='common' || q.level===levelFilter` so `'common'` appears at **both** levels. **Cycle grouping (verbatim
shared rule):** `cycleForSubject(id)` returns `'junior-cycle'` for `jc-`-prefixed ids else `'leaving-cert'`; the picker
splits into labelled "Junior Cycle" / "Leaving Certificate" groups **only when both cycles have content**, else a flat
list (the "no lonely header" rule). Group headers: `text-[11px] font-bold uppercase tracking-[0.14em]`, `#9e9186`.

**Schemas to match (verbatim, `types/commandWord.ts` + `types/catchUpLane.ts`):**

```ts
export type CommandLevel = 'higher' | 'ordinary' | 'common';
export interface CommandWordQuestion {
  id; subjectId; subjectLabel; level: CommandLevel; questionRef;
  stem;          // must contain commandWord verbatim so it's tappable
  commandWord; demand; trap; source; marks: number;
  figure?: { src: string; alt: string; source: string };
}

export type RecoveryLevel = 'higher' | 'ordinary' | 'common';
export interface RecoveryCard {
  id; subjectId; topicId;            // topicId = a real curriculum.ts subtopic id
  subjectLabel; topicLabel; focus?;  // focus = row label when a subtopic has >1 card
  level: RecoveryLevel;
  gist;
  oneMove: { label: string; text: string };
  check: { prompt: string; modelAnswer: string; needed: string[] };
  source; marksWeight: number;
  figure?:  { src: string; alt: string; source: string };
  passage?: { text: string; source: string };   // prose comprehension, shown verbatim
}
```

Data is **one flat exported array per tool** (`commandWordData.ts` / `catchUpLaneData.ts`) with accessors at the file
tail. Content is **source-grounded** against real `curriculum.ts` subject/subtopic ids and authored, then adversarially
verified (see `docs/launchpad-loop/*.workflow.js`). **Level purity is a hard rule and a CI guard** (`test/levelPurity.test.ts`):
an HL question must never appear at OL or vice versa.

---

## 5. Design system — tokens, fonts, borders, the Tailwind constraint

Colour comes from **one source per layer**, kept in sync: inline-style / SVG / Framer → `import { COLORS } from
'design/tokens.ts'`; Tailwind classes → named colours in `tailwind.config.ts`; CSS-var consumers
(`bg-[var(--accent-hex)]`) → the `:root` block in `index.html`. Never hardcode a hex when a token exists.

**Core tokens (`COLORS`, verbatim):** `accent #F26B1F`, `accentDark #B54D14`, `accentTint #FDEEDF`,
`accentDarkText #8C3A0E`, `success #3A8D5F`, `successTint #E8F2EC`, `successDarkText #1F5F3E`, `cream #FDF8F0`,
`creamSubtle #F9F9F7`, `border #1A1A1A` (the ink/border colour — the token key is `COLORS.border`, there is no `COLORS.ink`). Untoken'd but standard: page bg `#f0f0f0`, card `#ffffff`, muted border `#d0cdc8`,
muted text `#7a7068`, label text `#9e9186`.

**The hardest rule — accent ≠ success.** `accent #F26B1F` = brand / the action to take / selected / active / in-progress
fill / focus ring. `success #3A8D5F` = correct / complete / you-got-it / healthy zone. **Never use orange to mean
good/complete** — that's success's job.

**Typography.** Serif = **Source Serif 4** (`font-serif`) for titles, headings, concept terms, stat numbers. Sans =
**DM Sans** (`font-sans`) for body and labels. Section labels 10–11px / 700 / UPPERCASE / letter-spacing 0.12em /
`#9e9186`; stat numbers 32–48px / 700 in accent.

**Card system.** Primary card = white, `2px solid #1a1a1a`, radius 14–16, padding 18–24 (the bold ink border is the
signature). Active/selected = `accentTint #FDEEDF` + `2px solid #F26B1F`. Muted/locked = white + `1.5px solid #d0cdc8`.
Numbered badges/steppers encode state by token (active=accent, completed=success, locked=`#d0cdc8`), **never rainbow**.

**No coloured left borders — on CARDS.** Use dots, tints, fills, or coloured text instead. The **one sanctioned**
left border is the **Callout** primitive: `accentTint` bg + `border-left:3px solid #F26B1F`, radius `0 10px 10px 0`,
italic 14px `#8C3A0E` (success variant `#3A8D5F`/`#1F5F3E`). So: cards no, callouts yes (see §9 #5).

**Tailwind is a PostCSS build** (`postcss.config.js` + `tailwind.config.ts`; **no CDN** in `index.html`). JIT
class-literal constraint: never build `bg-${color}-500` in component code. `moduleThemes.ts` *can* construct theme class
strings dynamically **only** because `tailwind.config.ts` exhaustively **safelists** every shade it emits. For any value
not in the safelist, use inline `style={{}}` — that's why all dynamic hex/widths live in inline style.

**Banned in module/tool surfaces:** saturated extra accents (amber/yellow/lime/non-token orange as primary), bright green
other than `success`, purple/violet as accent, red as primary (only as a "harmful thought" marker), dark/near-black
module backgrounds, rainbow card sequences, coloured card backgrounds (white only), gradients on cards/backgrounds. The
**only** sanctioned off-token pair is the productive-vs-intrusive simulation pair `#5B8FD4` / `#E85D75` (sims only). IZ
tools each declare their own identity hex (cyan/indigo) as a deliberate self-contained exception.

`ConceptCardGrid` (`components/ModuleShared.tsx`) replaces all inline numbered lists: 3+ named concepts with descriptions
→ `ConceptCardGrid`, never `1) Term, 2) Term` prose.

---

## 6. Firestore patterns

Client initialised once in `firebase.ts`; `import { db } / { auth }` everywhere — never call `initializeApp`/
`getFirestore` yourself. `db` uses `persistentLocalCache` + `persistentMultipleTabManager` (offline-queued writes,
de-duped across tabs) — which is **why** fire-and-forget writes are safe and why `arrayUnion`/`increment` (server-resolved)
beat read-modify-write.

**One doc per user per concern, keyed by uid:** `users/{uid}` (identity: name, avatar, role, school, yearGroup,
curriculumLevel, needsPasswordChange), `progress/{uid}` (the big shared gamification doc — points, streak, achievements,
and per-tool namespaces), `responses/{uid}` (module free-text), `settings/{uid}` (UI prefs). Study sessions live in the
**subcollection** `progress/{uid}/sessions/{sessionId}`. A new gamified feature **owns one named field** on
`progress/{uid}` — do **not** add a new top-level collection.

**ModuleProgress is stored flat** at the `progress/{uid}` root, keyed by moduleId (not under a `progress` field).
Discriminant: a field is a `ModuleProgress` iff `typeof val==='object' && 'unlockedSection' in val`. `ProgressContext`
uses exactly this to rebuild the map and skip namespaced fields.

**All writes** use `setDoc(ref, partial, { merge: true })` — never plain overwrite, never `updateDoc` unless you need an
atomic dot-path delta. Write only your own key: `setDoc(doc(db,'progress',uid), { catchUpLane: next }, { merge:true })`.
Writes are **optimistic + fire-and-forget**: update React state first, then unawaited `setDoc` with
`.catch(reportSaveError('hook.save', e))`. For counters/lists use server-side `increment()` / `arrayUnion()`, not
computed numbers. Points are awarded via `pointsData:{ totalEarned: increment(n) }`, spent via dot-path
`'pointsData.totalSpent': increment(price)`, claim-once via `runTransaction`. Points + streak are **derived read-only**
from `ProgressContext` (`usePoints`/`useStreak` are thin wrappers) — never store or recompute them in a feature.

**The staleness rule (a real bug class).** A tool hook that **reads-and-writes** its own field must read fresh per mount
via `useFreshProgress(uid)` (getDoc-on-mount), **not** `useProgress()` — the IZ remounts the active tool on every nav, so
seeding from the app-start snapshot makes this-session saves vanish. Seed pattern: a `seededRef` reset on uid-change,
gate on `progressLoaded && !seededRef.current`, then `setState(saved ? {...EMPTY, ...saved} : EMPTY)`. **Golden
template:** `hooks/useHowTheyDidIt.ts`; primitive: `hooks/useFreshProgress.ts`. Hook return shape: `{ state, isLoaded,
persist/<mutators>, reload? }`; every hook takes `uid?` first and no-ops the write when uid is falsy.

`localStorage` is for device-local UI prefs only (`nextstep-settings`, `nextstep-language`; Firestore wins on conflict).
Never persist points/streak/achievement/unlock state to localStorage.

**Security-rule gotchas (`firestore.rules`).** `request.resource.data` exists **only on writes** — referencing it in an
`allow read` silently denies all reads (split read/write rules). Guard missing map fields with `('field' in
resource.data)` or `.get(field,null)` before comparing (indexed access to a missing field throws in CEL). Each
subcollection must be declared explicitly. Server-enforced invariants a feature must respect: `pointsData.totalEarned`
only increases and by ≤ +1000/write, `totalSpent` is monotone (no refunds), `unlockedAchievements` is append-only. Any
new validated field/collection needs matching rules.

---

## 7. Verification

- **`npm run build`** (vite) must pass — the headline gate to run before claiming done.
- The **real type gate** is **`npm run typecheck`** (`tsc --noEmit`) — it is **clean (0 errors)**; `build` does not
  type-check. `npm test` (vitest, 40+ tests) must also pass. CI (`.github/workflows/ci.yml`) runs
  `lint:ci → typecheck → test → build` on push/PR to `main`.
- **Do not rely on `npm run lint`** (`--max-warnings 0`) — broken with ~45 legacy warnings. Use `npm run lint:ci` or
  targeted `eslint` on changed files only.
- **Deployment is manual:** `firebase deploy --only hosting --project nextstepuni-app`. Pushing to `main` only runs CI
  (no auto-deploy) — merging to `main` is safe.

---

## 8. Golden examples — task → the one file to copy

| Task | Copy this |
|---|---|
| Add a standalone student **view** | `contexts/NavigationContext.tsx` (the `NAVIGATE_TO_INSIGHTS` case across all 5 sites) + the render branch in `AppRouter.tsx:297-345` |
| Add a bespoke educational **module** | `components/BestPossibleSelfModule.tsx` (theme import + inline `SectionDefinition[]` + `ModuleLayout`), then register in `moduleRegistry.ts` + `courseData.ts` |
| Add a per-**subject** module | register `createSubjectModule('<subjectKey>')` in `moduleRegistry.ts`; shared component is `components/SubjectModule.tsx` — don't hand-write a file |
| Build an IZ **content tool** | `components/CatchUpLane/index.tsx` (full body); diff against `components/CommandWordReflex/index.tsx` for shared skeleton vs tool-specific loop |
| Write the persistence **hook** for an IZ tool | `hooks/useHowTheyDidIt.ts` (fresh-seed + `seededRef` gate + namespaced `setDoc{merge:true}`); primitive `hooks/useFreshProgress.ts` |
| Type a card-deck tool's **data + state** | `types/catchUpLane.ts` + the flat array + tail accessors in `catchUpLaneData.ts` |
| Add **points / achievement / quest** logic | `hooks/useGamification.ts` (+ `hooks/useQuests.ts` for claim-once); respect `firestore.rules` invariants |
| Reuse a module **UI primitive** | `components/ModuleShared.tsx` (`Highlight`, `ReadingSection`, `MicroCommitment`, `ConceptCardGrid`, `ActivityRing`) — never roll your own |
| Pick the right **header** | `components/SectionCard.tsx` (dashboard tile) vs `components/ToolHeader.tsx` (IZ tile-list header) — don't add ToolHeader inside a tool body |
| Style a **Headspace** screen | `components/journey/PeerIslandsList.tsx` + `components/immersiveDeck/colorWorlds.ts` |
| Style a **Mercury** stats screen | `components/CAOPointsSimulator.tsx` |
| Style a **Brilliant.org** interactive | `components/ExamCrisisManagementModule.tsx` |
| Use the shared **CTA / Motion** primitives | `components/ui/PrimaryActionButton.tsx`; import motion via `components/Motion.tsx`, never `'framer-motion'` |
| Add an **on-paper study tool** to the Paper Trail viewer | `components/PaperTrail/textOverlay.ts` (live pdf.js text-layer scan → fractional-position tokens) + the `Tools` popover + gated tool rows in `components/PaperTrail/Viewer.tsx`; subject→dataset mapping in `components/PaperTrail/subjectMeta.ts`. Overlays position by fraction of page W/H (same convention as the answer-map anchors) so they ride zoom + virtualisation. The one-shot scan is guarded by a **ref**, not `scanState` — putting the loading state in the effect deps self-cancels the in-flight scan. Escape unwinds the open panel/menu before closing the viewer. Tools needing booklet/Storage data ship **gated OFF** (e.g. `FORMULAE_BOOKLET_LIVE`) so no dead button reaches students |
| Add **per-question topic tags** (frequency chips / cross-year jump) | Runtime: `components/PaperTrail/topics.ts` (paperKey normalise, `frequencyFor`, `siblingsFor`) reading committed `data/paperTrail/topicTags.ts`; wired in `Viewer.tsx` (Topics tool → chip per anchor + cross-year sheet) and `index.tsx` (`topics` prop + `onCrossYear`). Tags join to the answer-map anchors by question `n`, so the tool only lights when a paper has BOTH an answer map and a tag record. Generate a wave with the verify-don't-guess pipeline in `scripts/paper-trail/topic-tags/` (extract stems → classifier agents → adversarial verifier agents → `tags/<subject>.json` → `build-tags.mjs`); see `TOPICS.md`. Frequency is always phrased "N of M **tagged** years" so partial coverage stays honest |
| Show a **question as a real paper crop** (Topic Vault feed) | Runtime: `components/PaperTrail/VaultQuestionCard.tsx` derives a paper-side region via `paperRegion.ts` (`paperRegionFor`) from a lazily-fetched answer-map sidecar (`vaultResolve.ts` orders Storage sidecar → hosted `public/paper-anchors/` fallback; `isAnswerMap` shape-guards the SPA-rewrite 200). **Honesty rule: never show a crop you can't stand over** — missing sidecar / non-monotonic anchors / >`MAX_PAGES` span → `paperRegionFor` returns null and the card degrades to "open in the full paper". Generate anchors credential-free with `scripts/paper-trail/paper_anchors.py` (paper-side only, `mode:'pagejump'`, `conf<0.6`, written to `public/paper-anchors/` and served by Hosting itself). **Section-restart papers** (numbering restarts per reading text / Part) use the `armed_sectioned` detector + a `SUBJECT_ARMED_PATTERNS` entry (arm on the question-block header, disarm/`open` on the next section header, **case-sensitive** so title-case contents entries don't fire) + per-question crop-**ends** (`endP`/`endY`) that clamp each island's last question at the next boundary. Shipped: german HL, irish P2, geography Part One. **Every new anchor file is render-QA'd** (view the actual crop) before shipping — a wrong crop shown to a student is the worst failure; a missing one is acceptable. Type-split subjects (irish, geography) stay unpinned/`question` and get their armed sidecars from a second explicit `--grammar armed_sectioned` pass writing disjoint fileids. `test/vaultAnchors.test.ts` sweeps every committed sidecar; `test/paperRegion.test.ts` pins the derivation. See `scripts/paper-trail/PAPER-ANCHORS.md` |
| Add a **scheme-grounded marks breakdown** (Marking Lens) | `data/markingLens/{types,index,<subject>}.ts` + the "How the marks are given" panel in `components/PaperTrail/VaultQuestionCard.tsx`. Entries key to real tagged vault questions (`year\|level\|lang\|fileid\|n`); `notation` VERBATIM from the filed scheme in `/examiner-reports/`, `decoded` restates only the allocation, every entry cites its scheme, pitfalls only with a page-cited Chief Examiner behaviour. `test/markingLens.test.ts` machine-checks: no orphan keys, parts sum EXACTLY to totalMarks, everything cited, keys unique. Skip a question you can't source or sum — missing beats wrong. Golden file: `data/markingLens/business.ts`; dossier: `compliance/evidence/marking-lens.md` (update it in the same change as any authoring wave) |
| Open a **PDF with pdf.js** (Paper Trail viewer, Topic Atlas crops, covers) | `openPdfDocument(pdfjs, src)` from `components/PaperTrail/pdfjsLoader.ts` after `loadPdfjs()`, never `pdfjs.getDocument` directly. Every document shares one worker, and unless each document passes the resource URLs (`pdfjsResources.ts`, served by the `pdfjs-resources` plugin in `vite.config.ts`) pdf.js fetches its scan decoder through whichever document opened last, so closing that one blanks scanned crops in the others. `test/paperTrailPdfjsResources.test.tsx` fails on any direct `getDocument(` call |
| Add a **student-attempt tool** (triage / self-mark / weakness map) | Persist through `components/PaperTrail/attemptStore.ts` — localStorage keyed by `uid\|subjectId\|year\|level\|lang\|fileid` (`attemptNs`); triage ratings + self-marks live under one paper record. Triage + self-mark are tool panels in `Viewer.tsx` (self-mark control lives INSIDE the answer reveal); the cross-paper **weakness map** is `WeaknessMap.tsx` on the Paper Trail home, joining `allMarks(uid)` to topics via `topicsForPaper` and drilling with `onCrossYear`. On-palette RAG uses success/accent/**ink** (never amber/red). `Date.now()` is fine here (browser), unlike the workflow scripts |
| Surface a **citable examiner insight** | `data/paperTrail/examinerInsights.ts` — paraphrased "where marks are lost" + fix + source page, gated to subjects whose SEC Chief Examiner report is in `/examiner-reports/`. Keep verbatim quotes ≤15 words per the content rules; the card cites the page, the dossier holds the full source |
| Add a **home-level study-loop surface** (revise / review / mock / progress) | These live on the Paper Trail **home** as sibling `View` variants in `index.tsx` (`revise`, `review`, `mock`, `progress`), each a self-contained component reached by a home CTA and handing questions back through `openCrossYear` (the same cross-year jump the viewer uses). `ReviseByTopic.tsx` (browse tags by topic → drill), `ReviewSession.tsx` (SM-2 spaced recall over saved questions), `MockExamBuilder.tsx` (assemble + run a custom set), `ProgressDashboard.tsx` (one-screen aggregate). **Stores are all localStorage, per-uid, `now` injected** (never `Date.now()` inside the pure core): `reviewStore.ts` (deck + unit-tested `schedule` SM-2), `streakStore.ts` (day-log + pure `computeStreak`), `examDateStore.ts` (`daysUntil`), `mockSetStore.ts` (pure seeded `buildSet`), and the read-only aggregator `progressStats.ts` (`computeProgress`). Cross-surface derivations (weakest topic, gap breakdown) all flow from `allMarks(uid)` + `topicsForPaper`. Every pure store core carries a `test/*.test.ts`; the big views carry a `*.smoke.test.tsx`. **No fabricated content** — a "flashcard"/"mock question" is only ever a pointer to a real SEC question, its marking scheme the check. Only ever the token palette (accent/success/ink; never red/amber/blue-as-accent) |
| **Export** a printable pack (topic revision pack / mock set) | `components/PaperTrail/revisionPack.ts` — pure `buildPackHtml` (self-contained, inline-CSS, print-friendly, escapes untrusted labels) + `packFilename` slug + a thin `downloadPack` Blob wrapper. Lists **question references only** (year/level/paper/Q-number) with the SEC attribution footer — never answer text. Pass `dateIso` in; don't read the clock inside the builder |
| Add a **step after a study session** (the end-of-session quiz is the first) | Hook it in `components/study/StudySessionView.tsx` AND `StudySessionView.mobile.tsx` (near-identical copies) **after** `saveSession` + `resetSession`, gated on `savedSummary` — never before the save, which is the fragile unsaved `complete` phase behind the lost-study-time outbox. Capture what the step needs (e.g. `session.topicSelection`) in `rememberSaved`, because `resetSession` clears it. `lazy()` the step so the study room chunk stays lean. Preference = an optional `UserSettings` boolean (`studyQuiz`), read via `useSettingsContext()?.settings` (null in tests), toggled in `StudySessionSetup` and `YourSetupView`. Questions come from Mark Bank through `components/study/quiz/studyQuizPlan.ts` (`cardsForCurriculumNode` + `resolveSessionQueue`, dynamic `loadCards` only — the boot-precache guard fails the build on a static card import); its scoring is pinned to `SessionScreen`'s in `test/studyQuizPlan.test.ts`. A real session needs five minutes before it can save, so look at the page with `/study-quiz-dev.html?subject=…&level=…&theme=dark` |
| Add a **local notification** (study timer is the first) | `services/notifications.ts`: add an id to `NOTICE_IDS` and a key to `NotificationPreferences` (`types.ts`, saved in `settings/{uid}`); keep the when-to-schedule rules pure and tested like `services/studyTimerAlerts.ts`; run them from a hook like `hooks/useStudyTimerAlerts.ts`. Never prompt on launch: `scheduleLocalNotice` never asks, the student's tap does (`hooks/useStudyNotifications.ts`). See §11 |
| Get a **colour / font** token | `design/tokens.ts` (`COLORS`); `tailwind.config.ts` (class names); `index.html` `:root` (CSS vars) |
| Add/change a **security rule** | `firestore.rules` |
| Let **classmates see** part of a student's data (year islands) | Never open a peer read on `users`/`progress`. Copy an allowlisted subset into its own server-written collection: pure planner `functions/src/islandProjection.ts` (`planYearIsland`: field allowlist, caps, exclusions, owner opt-out) + `islandProjectionSync.ts` (fresh transactional, field-masked read of both sources, so an opt-out can never be overtaken by an older trigger) called from the `onProgressWritten`/`onUserWritten` triggers, which first skip writes that cannot change the projection. The rule compares the projection's OWN `school` + `yearGroup` with the requester's `users` doc, so the client query (`hooks/useYearIslands.ts`) must filter on both; add the collection to the erasure cascade and the export. Backfill with a script that runs the compiled sync (`scripts/backfill-year-islands.mjs`), never a second copy of the rules. Dev harness: `/year-islands-dev.html` (sample classmates; `?theme=dark`, `?classmates=none\|slow\|error`) |

---

## 9. Known inconsistencies

Code vs `CLAUDE.md` / memory contradictions found during the 2026-06-10 audit. Both sides named; **no winner picked** —
resolve deliberately, don't assume.

1. **Command Word Decoder location.** `CLAUDE.md` (§ Necessary Knowledge, ~lines 422-571) documents `CommandWordDecoder.tsx`
   inside the Exam Strategiser. That tree is **deleted**; the live tool is `components/CommandWordReflex/index.tsx`, a
   standalone IZ tool with its own indigo identity.
2. **Deleted exemplars.** `CLAUDE.md`'s Stage-2/3 primitives + named exemplars (`SrpIdentifier`, `SanityCheckTrainer`,
   `SpotTheTrap`, `WorkingShownAllocator`, `SubTaskCeilingVisualiser`, `ComparativeTextsLinker`) describe the deleted
   `components/ExamStrategiser/` tree. Live stand-ins: `ExamCrisisManagementModule.tsx`, `CAOPointsSimulator.tsx`,
   `PeerIslandsList.tsx`. *(These long sections are being removed from `CLAUDE.md` in this same change.)*
3. **Category count.** `CLAUDE.md` and `MEMORY.md` say **7 categories** (incl. `the-shield`, `the-launchpad`), but
   `CategoryType`, `categoryColorMap` (`courseData.ts:9-40`) and `categoryTitles` enumerate exactly **5**. `the-shield` /
   `the-launchpad` exist only as comment text and would not typecheck as a course category.
4. **Tailwind / GenAI.** `CLAUDE.md`'s old "Tailwind CDN" / "Gemini API integrated" claims are stale — the repo uses a
   PostCSS build (no CDN in `index.html`), and `firebase.ts`'s apiKey is the public Firebase web config, not a GenAI key.
   Memory is correct here; `CLAUDE.md` is not.
5. **No-coloured-left-borders.** Memory bans coloured left borders project-wide, but `CLAUDE.md`'s Callout spec **requires**
   `border-left:3px solid #F26B1F`, and ~39 live `border-l` usages exist. Code follows the Callout spec; the ban is
   effectively **card-scoped** (this doc states it that way in §5).
6. **Warm cream.** Memory bans `#FAF7F4`/`#FDF8F0` in module surfaces, yet `cream #FDF8F0` is a named token, `CLAUDE.md`
   sanctions it for inset content, and ~23 files still use it (ToolHeader's own ground is `#FAFBF6`). Intent (prefer cool
   neutrals like `#F0FAF8`) is not enforced in code.
7. **Mercury "lavender".** The Mercury memory calls for lavender accents, but live Mercury surfaces are neutral +
   orange-accented, and purple/violet is on the banned list. Copying the memory literally would introduce a banned colour.
8. **Auth/nav/progress location.** `CLAUDE.md` says App.tsx manages auth (`onAuthStateChanged`) and navigation via local
   state. **Reality:** all three are in `contexts/AuthContext.tsx`, `NavigationContext.tsx`, `ProgressContext.tsx`;
   App.tsx is a data-assembly shell.
9. **Per-module themes vs banned palette.** `moduleThemes.ts` `THEME_COLORS` defines amber/emerald/purple/lime/violet/red
   themes (safelisted in `tailwind.config.ts`), but the banned list forbids those as primary UI. They're pre-pivot legacy
   (only ~3 modules migrated to `accentTheme`); the ~75-file "green migration debt" (off-token emerald/green instead of
   `success #3A8D5F`) is the visible symptom.
10. **`moduleThemes.ts:40` comment** ("Now that Tailwind runs at build time, we can construct class strings dynamically")
    reads as if the JIT-literal constraint is lifted — it only works because the config safelists every emitted shade.
    The comment and the literal-class rule contradict on their face.
11. **Duplicate type defs.** `PointsData`/`StreakData` are declared differently in `hooks/usePoints.ts` + `hooks/useStreak.ts`
    (with `isLoaded`) vs `contexts/ProgressContext.tsx` (with `reload`), and `PointsData` a third time inlined in
    `AppRouter.tsx:115`. Two/three sources of truth for one concept.
12. **Phantom `ModuleProps`.** `CLAUDE.md` presents `interface ModuleProps {...}` as a real exported type. **None exists** —
    the 3-field signature `{onBack, progress, onProgressUpdate}` is inlined everywhere. Do **not** add a `ModuleProps`
    import.
13. **ToolHeader usage.** ToolHeader's docblock says it's "every Innovation Zone tool entry point", but the live content
    tools render no ToolHeader band at all (§2). The comment means the InnovationZone tile list, not the tool bodies.

## 10. Adding a Mark Bank subject — the deliberate-registration list

Shipping a new subject deck (done for Computer Science + Engineering, PR #56) touches every one of these,
and the test net fails loudly on the ones you forget:

1. `scripts/markbank/build-deck.mjs` — a `SUBJECTS` row (title, specVersion, specNote, figureDir).
2. `examiner-reports/<subject>/schemes/<year>-<hl|ol>.md` — the provenance gate reads these; a card whose
   marking points aren't found in its own scheme is dropped at build.
3. `components/MarkBank/figures.json` — every `figureKey` needs a manifest entry (bind-figures.mjs), and
   the build md5-checks each file on disk against it.
4. `components/MarkBank/deck.ts` — strands + `SUBJECTS` entry + `DECKS` dynamic-import pair. A subject in
   `sizes.json` but not `DECKS` shows as ready and opens empty (the Construction Studies failure).
5. `test/markBankDeck.test.ts` — deck imports into `SAMPLE_CARDS` + the topic-id `PREFIX` map (both are
   deliberate-registration guards; AgSci once shipped 733 cards outside the net).
6. `scripts/markbank/authoring/reconcile.py <subject> --baseline write` — the coverage ratchet; the paired
   test pins deck counts + content hashes to `scripts/markbank/coverage-baseline.json`.

Tariff modelling rules learned the hard way: mark values come from the scheme's printed notation, never
arithmetic ("Any three of the above or similar 2 marks each" is an `anyN` group, not six invented 1-mark
rows); a banded whole-answer tariff ("Fully correct 6 / Almost correct 4") is `questionTotal` with
`marks: null` rows; `orderedSplit`/`questionTotal` rows are menu-class (the scheme's printed candidates,
capped at `MAX_LONG_OPTION_ROWS`), while the five-row cap is for required-recall `fixed` cards only.

## 11. Device alerts — notifications and the iOS Live Activity

- **Local plugins must be registered by hand.** Capacitor 8 only auto-registers the plugins `cap sync` lists from
  `node_modules` (`packageClassList`). A plugin that lives in the app target (`StudyLiveActivityPlugin`,
  `SignInWithApplePlugin`) is registered in `ios/App/App/NextStepBridgeViewController.swift`
  (`capacitorDidLoad` → `bridge?.registerPluginInstance(...)`); `Main.storyboard` points at that class.
- **`@capacitor/local-notifications` 8.3+ prompts from `schedule()`** and, on Android 12+, opens the Alarms settings
  screen for exact alarms. `services/notifications.ts` checks permission first and only asks for exact alarms the
  student already granted; keep it that way.
- **The session engine owns device alerts.** `hooks/useStudyTimerAlerts.ts` runs inside the uid-keyed
  `StudySessionEngine`, so sign-out and a different student signing in cancel the notification and end the Live
  Activity; `nextstepuni:session-cleared` (fired by `clearLocalSessionData`) does the same without React.
- **The Live Activity** is the `StudyTimerWidget` extension (`com.nextstepuni.app.StudyTimer`) plus
  `ios/App/Shared/StudyTimerAttributes.swift`, compiled into both targets. Project changes go through
  `scripts/ios/add-study-timer-widget.rb` (xcodeproj gem), not hand edits. Its colours are fixed per colour scheme
  inside the view: asset-catalog colours were resolved in two appearances on the iOS 26 Lock Screen.
- **One timer limit across app and native UI.** `StudyActivityState.totalSeconds` includes the open-ended
  session's four-hour cap. Swift's `timerEndsAt` supplies both the system clock range and the ActivityKit
  stale deadline, including when JavaScript is suspended. A stale stopwatch says "Ready to log".
- **Accept one extension per completion.** `useStudySession` claims an extension synchronously before
  React renders again. Repeated requests must not inflate saved minutes or disagree with the deadline;
  the guard resets when the extended countdown completes. Keep interruption/relaunch regressions in
  `test/studyTimerInterruption.test.tsx` alongside extension and notification coverage.
- **Release bumps:** the extension carries its own `MARKETING_VERSION` / `CURRENT_PROJECT_VERSION` (Debug and
  Release). Bump all four with the app's or App Store Connect flags the mismatch.
- **Simulator check without an account** (Debug builds only): `xcrun simctl launch booted com.nextstepuni.app
  -NSUStudyTimerDemo '{"notifyIn":45,"remaining":1110,"mode":"running"}'` (`mode`: running, paused, countup, done;
  `roomOpen: true` suppresses the in-app banner). See `services/studyTimerDemo.ts`.

### Optional study app blocking — iPhone/iPad

- Alex approved iPhone/iPad first on 10 November. Keep the existing Study Room
  design. `StudyFocusChoice` uses its existing option row, switch and button;
  unsupported devices render nothing. No CSS, artwork or planner changes.
- `useStudyFocusSession` runs in the account-scoped session engine. Wait for
  `identityReady` before reconciling a native launch, so initial auth restoration
  does not erase saved choices. Pause, completion, discard and sign-out release
  the shield; resume/extension reschedules it. Never put this lifecycle in a view.
- `StudyFocusPlugin` uses individual Screen Time authorization on iOS 16+,
  requested only by a tap. The system picker returns opaque tokens stored in
  `group.com.nextstepuni.app.studyfocus`. Only counts/status cross the bridge;
  never upload tokens, application names or usage. The state file is excluded
  from device backups. Switching accounts or signing
  out clears choices. Revoking authorization invalidates tokens and clears them.
- `StudyFocusMonitor` is a DeviceActivity extension sharing `StudyFocusStore` and
  its file lock with the app. Register monitoring and persist the generation and
  deadline BEFORE shielding. Old callbacks cannot clear a newer generation.
  Errors release this named store only; never clear another feature's settings.
- DeviceActivity requires intervals of at least 15 minutes. For shorter sessions
  use an already-ongoing 16-minute monitoring window ending at the actual timer
  deadline. No usage events are requested. This preserves 5/10-minute sessions
  and short extensions. Validate this path on signed physical devices before
  release. Apple delivers interval callbacks when the device is in use; do not
  promise exact-second cleanup while the device is asleep.
- Run `ruby scripts/ios/add-study-focus.rb` for project updates. It provisions
  nothing and is idempotent. The app and monitor need the Family Controls
  capability and shared App Group; distribution needs Apple's approval for BOTH
  bundle IDs. Keep the monitor version/build aligned with the app. The existing
  Live Activity widget does not use Screen Time and needs no new entitlement.
- Before release: verify real picker/permission handling, blocking selected apps
  while notes remain available, 5/10/25-minute deadlines, stopwatch cap, pause,
  resume, extension, force quit, lock/unlock, denied/revoked permission, relaunch
  and account changes. Unit checks and simulator compilation are not evidence of
  Screen Time enforcement. See `test/studyFocus*.test.tsx` and the Foundation-only
  policy checks in `scripts/ios/test-study-focus.swift`.


## Dated study plan — feedback implementation, November 2026

- `useDatedStudyPlan` supplies one account-scoped dated plan to Home, Planner,
  Progress, War Room and both Study Room variants. Use `getBlockId`; never make
  `block-${index}` identities or recompute a separate timetable in an enabled consumer.
- Alex explicitly rejected the redesigned planner on 10 November. This is an
  algorithm-only change. Preserve the existing Study Room, PlannerWorkbench,
  settings, cards, typography, artwork, colours and layout. No new planner UI
  or availability questionnaire. Check all affected surfaces, not only Study Room JSX.
- Existing profile rest days and block duration feed `profilePlanSettings`. The
  former planner's lowest ceiling (360 minutes/week, at most 90/day) is retained
  as a product limit, never claimed as measured availability or a scientific dose.
  Nearer exams and longer blocks do not raise it; all seven rest days are valid.
  Previously configured explicit budgets remain bounded. The engine can deduct
  assigned work, breaks and buffer if supplied, but does not invent these inputs.
  Completed/manual tasks and their occurrence IDs survive replanning/week rollover.
- Routine opportunities stay within their own week and prefer less-loaded days;
  actual due reviews retain their dates. Keep every task's declared duration:
  leftover minutes must not silently shorten the student's chosen practice block.
  Resolve prerequisites before follow-ups. When there is room for two whole
  practice blocks, favour an early first contact and a separate later date.
  These spacing and placement rules are product policy, not an optimal-dose claim.
- Confidence, completion and independent recall are distinct signals. Canonical
  topic evidence uses the curriculum registry; Junior Cycle/LCA use subject coverage
  without borrowing senior topics. Mark Bank retains ownership of card review dates.
- `StudySessionQuiz` passes actual marked questions to `studyQuizEvidence` as each
  answer is committed, so closing partway through retains completed results.
  Aggregate once per canonical topic and quiz session; skips have no result.
  Self-assessed full marks schedule a short follow-up without increasing independent
  retrieval successes. Zero/partial marks bring practice forward. Store source and
  aggregate marks, never answer text. Ambiguous multi-topic marks remain card-only;
  do not assign a whole-question score to every topic selected for the session.
  Existing topic confidence must not erase observed quiz evidence during sync.
- `progress/{uid}/studyPlans/current` stores the bounded working plan (28 days of
  past tasks plus the current fortnight), settings and retrieval evidence. Actual
  study history stays in existing sessions/completions. Include this subcollection
  in owner rules, account erasure and exports. No points or streaks live here.
- Sync hydrates before uploading defaults. Use `mergeFields` at individual task and
  topic map entries, and at complete settings/deadline/requirement fields: ordinary
  recursive merge cannot remove a deleted date exception. Never write empty task
  maps. An account-scoped local outbox retains failed changes for retry. Separate
  tasks merge independently; concurrent edits of the same task use last server write.
- `data/studyEvidence.ts` pairs student guidance with primary studies and their
  limits. Hours, duration, priority weights and exact intervals are product policy,
  not research-proven optimal doses. Rotating school subjects is coverage, not the
  same intervention as interleaving mathematical problem types.
- Review using the existing localhost demo route in the real app. The rejected
  standalone dated-planner component and its stylesheet have been deleted.
  `study-planner-local.html` now only embeds the real app with its existing localhost
  demo mechanism. Use `?screen=planner` to inspect the original PlannerWorkbench.
- Research references: Roediger & Karpicke (2006), retrieval practice; Cepeda et al.
  (2008), spacing; Butler, Karpicke & Roediger (2008), corrective feedback; Rohrer,
  Dedrick & Stershic (2015), interleaved mathematical problems. Primary-source URLs
  and limits are preserved in `data/studyEvidence.ts`. No new panels are required.
