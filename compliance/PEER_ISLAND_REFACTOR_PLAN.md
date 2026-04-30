# Peer Island Refactor — Audit and Plan

NextStepUni Learning Lab — rebuild Peer Island on a minimal public projection collection

Document status: AUDIT for Alex's review — implementation paused until borderline field decision is made
Date: 2026-04-29

---

## Executive summary

The Peer Island feature is currently broken (or about to be, on next deploy)
because the Phase 1 firestore.rules remediation removed the only path that
allowed one student to read another student's `progress/{userId}` document.

This document audits the *actual* fields the feature consumes from a peer's
`progress` document today, and proposes a minimal projection collection
`/islandPublic/{uid}` that exposes only those fields, with all
performance-sensitive and academically-sensitive data filtered out.

**One borderline field is flagged for Alex's decision (`category` —
NorthStarCategory). Implementation is paused per the Phase 1 spec rule
"STOP HERE if any borderline fields were flagged."**

---

## 1. Files involved in the current Peer Island feature

| File | Role | Reads from peer's progress? |
|---|---|---|
| `hooks/usePeerIslands.ts` | Loads peer islands list | **Yes** — calls `getDoc(doc(db, 'progress', userDoc.id))` for each candidate (line 57). |
| `components/journey/PeerIslandsList.tsx` | Modal showing peer islands grid + leaderboard | No direct Firestore reads; consumes `PeerIsland[]` from the hook. |
| `components/journey/JourneyView.tsx` | Hosts the peer islands list and renders selected peer's island | No direct Firestore reads for peers; consumes the hook output. |
| `components/journey/JourneyCanvas.tsx` | 3D scene renderer | Receives placements as props; no direct reads. |
| `components/journey/hex/HexIsland.tsx` | Hex grid renderer | Receives placements as props; references `purchasedAt` for a "newly purchased" animation (lines 48, 63). |
| `firestore.rules` | Currently grants self / admin / GC reads on `progress`; previously also granted same-school peer reads (R1, removed 2026-04-29). | n/a |

The hook (`usePeerIslands`) is the single point where all peer-progress
data is loaded. The refactor target is contained.

---

## 2. Fields actually read from a peer's `progress/{uid}` today

Verified line-by-line against `hooks/usePeerIslands.ts` (lines 38–82),
`components/journey/PeerIslandsList.tsx` (lines 14–18, 67–88, 154–245), and
`components/journey/JourneyView.tsx` (lines 232, 232–250).

| Field path | Where read | What it is used for |
|---|---|---|
| `progress/{uid}.northStar.category` | usePeerIslands.ts:61 (with fallback to `islandState.category`) | Determines which "starter island" preset to render if the peer hasn't placed any items, and which water colour to use behind their island. Type: `NorthStarCategory` — values like `college`, `independence`, `prove-myself`, `creative`, `change-maker`. |
| `progress/{uid}.islandState.category` | usePeerIslands.ts:64 (fallback if `northStar.category` is missing) | Same as above. |
| `progress/{uid}.islandState.placements` | usePeerIslands.ts:62, 70, 78; PeerIslandsList.tsx:71, 72, 82, 155; JourneyView.tsx:232 | The visual island. Each placement is `{ itemId, model, type, q, r, rotation, scale, offsetX, offsetZ, purchasedAt, isStarter }`. The `purchasedAt` field per placement triggers a "newly purchased" animation (HexIsland.tsx:48,63) — useful for the *owner*, not for peers. |
| `progress/{uid}.islandState.purchaseHistory` | PeerIslandsList.tsx:16 (inside `computeIslandScore`) | Counted as a `Set` for `uniqueItems`, used to compute the leaderboard score: `score = (placementCount * 2) + (uniqueItems * 3)`. Not displayed raw; not rendered visually. |

**Fields read from `progress/{uid}` that are NOT used by the peer view**
(but currently accessible because the rules permitted full-document reads):

- `pointsData.totalEarned`, `pointsData.totalSpent`
- `gamification.unlockedAchievements`
- `studySessions[]`, `studyDebriefs[]`
- `topicMastery.{subject}.{topic}`
- `unifiedMockResults[]`
- `subjectProfile`
- `timetableCompletions`, `timetableStreak`
- `northStar.statement` (the free-text aspiration; only `.category` is used)
- `flareCounts`, `lighthouseLevel`, `rescueCount`
- `cosmeticUnlocks`
- `strategyMastery`, `sm2States`, `teachBacksSeen`, `dismissedGuides`
- per-module section unlock state
- `islandState.totalSpent`
- `islandState.lastPurchaseTimestamp`
- `islandState.claimedRewards`

These were exposed under the previous rule and are not exposed under the
proposed projection.

**Fields read from `users/{uid}` (already same-school readable, unchanged
by this refactor)**:

- `name`, `avatar`, `school`, `role`, `isAdmin` (the last two are read to
  filter out staff accounts in the hook).

---

## 3. Proposed projection: `/islandPublic/{uid}`

The proposal includes a small amount of duplication from `users/{uid}` so
that the Peer Island feature can be served by a single same-school query
against `/islandPublic` and is robust against any future tightening of the
`/users` same-school read rule.

### Schema

```
/islandPublic/{uid}: {
  // Identity (duplicated from users/{uid} for self-contained reads)
  name: string                         // = users/{uid}.name
  avatar: string                       // = users/{uid}.avatar (DiceBear seed)
  school: string                       // = users/{uid}.school (used for the same-school
                                       //   filter when the client queries this collection)

  // Visual island
  category: NorthStarCategory          // see flag in Section 4
                                       // Sourced from progress.islandState.category
                                       //   with fallback to progress.northStar.category
  placements: IslandPlacementPublic[]  // = progress.islandState.placements,
                                       //   with `purchasedAt` STRIPPED from each
                                       //   placement (see "Stripped fields" below)

  // Pre-computed metrics (avoid exposing raw signals)
  placementCount: number               // = placements.filter(p => !p.isStarter).length
                                       //   (rendered as "N pieces")
  score: number                        // = (placementCount * 2)
                                       //   + (uniqueItemCount * 3)
                                       //   where uniqueItemCount = number of distinct
                                       //   item IDs in islandState.purchaseHistory.
                                       //   Replaces raw purchaseHistory.

  // Housekeeping
  updatedAt: Timestamp                 // server timestamp, when the projection
                                       //   was last regenerated
  schemaVersion: number                // = 1, for future migration
}
```

`IslandPlacementPublic` is `IslandPlacement` minus `purchasedAt`:

```
type IslandPlacementPublic = {
  itemId: string
  model: string
  type: 'hex' | 'decoration'
  q: number
  r: number
  rotation?: number
  scale?: number
  offsetX?: number
  offsetZ?: number
  isStarter?: boolean
  // purchasedAt: REMOVED from public projection
}
```

### Stripped fields (not in the projection by design)

| Field (in source) | Why stripped |
|---|---|
| `placement.purchasedAt` | Per-placement timestamp = behavioural inference about when the student was active in-app. Only used for an owner-side "newly purchased" animation. Peers don't need to see it; that animation is for the owner. Stripping = no animation when viewing a peer's island, which is the correct behaviour anyway. |
| `islandState.purchaseHistory` (raw) | Replaced by pre-computed `score`. Raw history reveals the order and identity of *all* items the student has ever bought, including unplaced ones. Score is the only metric the leaderboard actually consumes. |
| `islandState.totalSpent`, `lastPurchaseTimestamp`, `claimedRewards` | Not consumed by the peer view today. |
| `northStar.statement` | The free-text aspiration. Not consumed by the peer view today. The `category` is enough for the visual. |
| All `progress` fields outside `islandState` and `northStar.category` | Not consumed by the peer view; not in scope. |

---

## 4. Borderline field flagged for your decision

### `category` (NorthStarCategory)

**What it is:** the student's chosen post-secondary aspiration category,
selected during onboarding (NorthStarOnboarding.tsx). Values are a fixed
enum (e.g. `college`, `independence`, `prove-myself`, `creative`,
`change-maker` — the exact list lives in `northStarData.ts`). Each category
has a distinct visual treatment (water colour, scene preset).

**Why it's currently rendered in the peer view:** the entire visual theme
of an island depends on its category. A peer viewing another's island
literally sees the category through the colour and scene. Excluding it
from the projection means we can't render any peer island.

**Why it's borderline:**

- It is genuinely personal information. Even though the categories are
  broad, "I want to prove myself" vs "I want to go to college" tells a
  peer something about a 16-year-old's identity and self-narrative.
- It is *implicitly* visible from any rendered island today. Including
  it in the projection does not increase what a peer can infer beyond
  what the visual already shows.
- Some categories may be more sensitive than others (`prove-myself`,
  `independence`) — but the data structure does not let us redact some
  values and not others without bespoke logic.

**Three possible decisions, in order of "most permissive" to "most
private":**

1. **Include `category` in the projection (default proposal).** The peer
   view continues to render with the correct theme per peer. No change
   to the user-visible feature. Privacy posture: the category was
   already implicit in the visual; making it explicit in the data
   layer doesn't add new exposure.

2. **Replace `category` with a generic theme in the projection.** The
   peer view renders all peer islands with a single neutral theme
   (e.g. always the `creative` water colour). Privacy posture: a
   peer's category is no longer derivable from their island view.
   Cost: every peer island looks the same in terms of theme; some
   visual distinctiveness is lost.

3. **Drop `category` and use a coarser axis (e.g. `themeIndex: 0..7`)
   that is generated from the uid hash rather than the real category.**
   Same privacy outcome as option 2, but each peer's island still has
   a distinct theme — just not a *meaningful* one. Privacy posture:
   strongest. Cost: a peer who knows their friend's category cannot
   confirm it from the island; mild visual decoupling from the
   onboarding choice.

**Default if you don't decide:** option 1 (include `category`). This
matches the current behaviour and is what I would ship if the audit had
not flagged the field. But the spec asked me to flag and stop, so I am.

**Your decision needed:** select 1 / 2 / 3, or write a different option.

---

## 5. Architecture decision: write path

The repository already has a `functions/src/index.ts` with two existing
Cloud Functions (`resetStudentPassword`, `changeOwnPassword`). Cloud
Functions infrastructure is therefore set up.

**Preferred path** (per the Phase 1 spec preference order): a Firestore-
triggered Cloud Function `onProgressWritten` that fires on any write to
`/progress/{uid}` and updates `/islandPublic/{uid}` with the projection.

Mechanics:

- Trigger: Firestore event `onWrite` on `progress/{uid}`.
- Read the new document, extract the relevant fields, compute `score`
  and `placementCount`, strip `purchasedAt`.
- Write the projection to `/islandPublic/{uid}` using the Admin SDK
  (which bypasses Firestore Security Rules — required because the rule
  on `/islandPublic` will be `allow write: if false` for clients).
- Idempotent: running the function twice in a row produces the same
  projection (no event log appending).
- Handles the `users/{uid}` part by also reading `users/{uid}` inside
  the function (or by doing a separate `users/{uid}` write trigger;
  see Section 6).

A second, simpler option: only project the `progress`-derived fields
and let the read path join `users/{uid}` separately. This keeps the
projection function single-source and avoids the `users` trigger. But
it sacrifices the "self-contained query" benefit of having `name` and
`avatar` in `/islandPublic`.

**Recommendation:** use the single `onWrite('/progress/{uid}')` trigger,
and inside it also read `users/{uid}` to populate the duplicated
identity fields. Add a second `onWrite('/users/{uid}')` trigger that
rewrites `/islandPublic/{uid}` if `name`, `avatar`, or `school` change
on a user with an existing projection. This keeps the projection
permanently consistent.

---

## 6. Proposed implementation steps (paused — awaiting Section 4 decision)

Once you've answered Section 4, the implementation will proceed:

### Step A — Cloud Function `onProgressWritten`

- File: `functions/src/index.ts` (append; do not replace existing
  functions).
- Trigger: `onWrite` on `/progress/{userId}`.
- Behaviour: reads the new `progress` doc and the corresponding `users`
  doc; if the user is a student (`role !== 'gc' && !isAdmin`), writes
  the projection to `/islandPublic/{userId}` using the Admin SDK.
- If the user is GC/admin, *deletes* any existing
  `/islandPublic/{userId}` (defensive).
- If the new `progress` doc has no `islandState` (student hasn't
  generated one yet), no projection is written.

### Step B — Cloud Function `onUserWritten`

- Same file, second function.
- Trigger: `onWrite` on `/users/{userId}`.
- Behaviour: if `/islandPublic/{userId}` exists, refresh its `name`,
  `avatar`, `school` fields. If user changed school, the refresh covers
  the new school correctly. If user is now a GC/admin (role flipped),
  delete the projection.

### Step C — Backfill script

- File: `scripts/backfill-island-public.ts`.
- Reads every `progress/{uid}` document, builds the projection, writes
  to `/islandPublic/{uid}`. Skips users with no `islandState`.
- Default mode: dry-run. Logs `would write N documents`.
- Real-write mode: `--apply` flag, refuses to run unless
  `FIREBASE_PROJECT=nextstepuni-app-emulator` (i.e. emulator only) or an
  explicit `--allow-production` flag is passed.
- The emulator path is the only path I will run; the production-apply
  flag exists so Alex can run it after review.

### Step D — Firestore rules update

```
match /islandPublic/{uid} {
  allow read: if request.auth != null
              && exists(/databases/$(database)/documents/users/$(request.auth.uid))
              && exists(/databases/$(database)/documents/users/$(uid))
              && get(/databases/$(database)/documents/users/$(request.auth.uid)).data.school
                 == get(/databases/$(database)/documents/users/$(uid)).data.school;
  allow write: if false;  // server-side only, via Admin SDK
}
```

The `exists()` checks are defensive: `get()` on a non-existent doc fails
the rule. We avoid that by short-circuiting on existence first.

### Step E — Refactor `usePeerIslands.ts`

- Replace the two-step query (`/users` → per-user `/progress/{uid}`)
  with a single same-school query against `/islandPublic`:

  ```
  collection(db, 'islandPublic')
  query(where('school', '==', school))
  ```

- The hook's return type (`PeerIsland[]`) is preserved so callers
  don't need to change. Internally, fields come from the projection.
- The `createStarterState` fallback (used today when a peer has a
  `northStar` but no `islandState`) becomes redundant: the projection
  will not exist until the peer has progressed at least once. We
  decide whether to render starter islands for "north-star-only"
  peers — recommendation: **do not**, because that would require a
  projection write for every onboarded student before they engage
  with the journey, and creates a cohort-enumeration vector. Peers
  who haven't started building simply don't appear in the list, which
  is the honest signal.

### Step F — Self-view path unchanged

The student's own island continues to read `/progress/{uid}` directly
(the self-read rule on `/progress` is unchanged). No projection is
read for the self view.

### Step G — Verification (manual; emulator)

1. Start emulator: `firebase emulators:start --only firestore,functions`.
2. Seed two students at School-A, one student at School-B.
3. Sign in as student A1, generate an island, verify it appears.
4. Sign in as student A2, open Peer Islands, verify A1's island
   appears with the correct theme and placements.
5. Sign in as student B1, open Peer Islands, verify neither A1 nor A2
   appear.
6. With Firestore rules tester, attempt direct write to
   `/islandPublic/{uid}` from any client identity — must be denied.
7. With Firestore rules tester, attempt direct read of
   `/islandPublic/A2` while signed in as B1 — must be denied.
8. Confirm `/progress/{uid}` reads from B1 to A1 are denied (R1
   remediation still effective).

### Step H — Compliance documentation updates

- `compliance/DPIA.md` R1: update the entry to record that the underlying
  use case has been preserved via the projection collection.
- `compliance/DPA_SCHEDULES.md` Schedule 3: add `/islandPublic` as a new
  data category, with the minimal field list above.
- `compliance/REMEDIATION_LOG.md`: append a new entry describing the
  refactor.
- `compliance/PHASE1_COMPLETE.md`: add the "Peer Island refactor —
  staged" section as required by the task.

---

## 7. Hard rules being respected

Per the task spec:

- Only `firestore.rules` (read), `functions/src/index.ts` (append),
  `hooks/usePeerIslands.ts` (refactor) and the new
  `scripts/backfill-island-public.ts` will be touched. No unrelated
  code is in scope.
- No deploy.
- No production backfill.
- No fields beyond the projection above.

---

## 8. Status

**Stopped after audit per the Phase 1 spec rule "STOP HERE if any
borderline fields were flagged."** Resume by giving me your call on
Section 4. The simplest reply: "Section 4: option 1" (or 2 or 3).

Once you reply, I'll execute Steps A–H without further confirmation.
