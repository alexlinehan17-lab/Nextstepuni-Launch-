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
`/reset-password` + `mode=resetPassword` guard skips URL-sync so the Firebase `oobCode` survives.

**`AppRouter` is the single switch**, in strict precedence: reset-password params → `!userResolved` spinner → `!user`
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
ProgressProvider > NavigationProvider > MotionConfig > PullToRefresh > App`. `ProgressContext` and `NavigationContext`
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
onboarding/module/admin/gc. There is **no desktop sidebar** — desktop nav is a `fixed top-6 right-6` floating cluster.

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
| Get a **colour / font** token | `design/tokens.ts` (`COLORS`); `tailwind.config.ts` (class names); `index.html` `:root` (CSS vars) |
| Add/change a **security rule** | `firestore.rules` |

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
