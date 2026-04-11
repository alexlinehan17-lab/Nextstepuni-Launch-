# Firestore Data Layer Audit

**Date:** 2026-04-11
**Scope:** All files in hooks/, contexts/, and components/ that import from firebase/firestore
**Total files audited:** 43 (24 hooks, 6 contexts, 19 components)

---

## Clarifying Questions (added 2026-04-11)

### Q1: Are the 13 unmount-unsafe hooks (H1) and the duplicate-read hooks (L3) the same set?

**No. They overlap but are different sets.**

**Unmount-unsafe callbacks (H1) — 13 hooks:**
useGCFlags, useGifts, useIslandShop, useKudos, useMockResults, useModuleResponses, useNorthStar, useQuests, useSettings, useStudySession, useTeachBack, useTopicMastery, useWeeklyChallenge

**Duplicate progress/{uid} readers (L3) — 15 hooks:**
useStreak, usePoints, useQuests, useGamification, useInsights, useRecommendation, useStrategyMastery, useWeeklyChallenge, useTopicMastery, useMockResults, useStudySession, useIslandShop, useTeachBack, useNorthStar, useFlares

**Overlap — 8 hooks** (benefit from both fixes):
useQuests, useIslandShop, useMockResults, useStudySession, useTeachBack, useTopicMastery, useWeeklyChallenge, useNorthStar

**Unmount-unsafe ONLY (read other collections, not progress) — 5 hooks:**
useGCFlags (gcFlags), useGifts (gifts), useKudos (kudos), useModuleResponses (responses), useSettings (settings)

**Duplicate-read ONLY (read-only, no write callbacks) — 7 hooks:**
useStreak, usePoints, useInsights, useRecommendation, useStrategyMastery, useGamification, useFlares

**Conclusion:** A ProgressContext refactor addresses L3 for all 15 hooks. The isMountedRef pattern addresses H1 for all 13. The 8 overlapping hooks get both fixes. But these are two separate concerns — they can't be collapsed into one refactor. The 5 non-progress hooks still need isMountedRef independently.

### Q2: Why do 15 hooks bypass the existing ProgressContext?

**ProgressContext exists but only exposes a subset of the progress doc.** It holds:
- `userProgress` (module completion state — the per-module `{unlockedSection}` objects)
- `studentProfile`, `northStar`, `timetableCompletions`
- `pointsData` (via usePoints), `streak` (via useStreak)
- Cosmetic unlocks, dismissed guides

**Fields the hooks need that are NOT in ProgressContext:**

| Field | Used by |
|-------|---------|
| `studySessions` | useStudySession, useInsights, useRecommendation, useStrategyMastery, useQuests, useWeeklyChallenge |
| `studyDebriefs` | useInsights, useQuests |
| `topicMastery` | useTopicMastery, useRecommendation, useQuests |
| `gamification` | useGamification |
| `islandState` | useIslandShop, useGamification |
| `mockResults` / `unifiedMockResults` | useMockResults, useQuests |
| `sm2States` | useDebriefSideEffects |
| `questRewards` | useQuests |
| `weeklyChallengeRewards` | useWeeklyChallenge |
| `rescueCount`, `lighthouseLevel`, `flareCounts` | useFlares |
| `teachBacksSeen` | useTeachBack |
| `strategyMastery` | useStrategyMastery |
| `timetableReflections` | useGamification |

The hooks bypass context because the fields they need don't exist in it. ProgressContext was built for the top-level App/AppRouter rendering needs (module progress, profile, points display). The deeper hooks (gamification, study sessions, topic mastery) each read the full progress doc independently to access their specific fields.

**Fix path for PR 2:** Extend ProgressContext to read the FULL progress doc once and expose the raw doc data. Each hook then reads its fields from context instead of making an independent `getDoc`. The hook's public API stays the same — consumers don't change.

### Q3: Is the zero-listeners pattern intentional or accidental?

**Accidental.** Evidence:

1. **Git history:** No commit message in the entire history mentions `onSnapshot`, `real-time`, `realtime`, or `listener` in a Firestore context. The codebase was built across ~20 feature commits, each adding one-shot reads incrementally.
2. **No code comments** discussing the tradeoff of one-shot vs real-time anywhere.
3. **`gcNotifications.ts` uses `runTransaction`** — showing awareness of advanced Firestore features — but still uses `getDoc` for reads, not `onSnapshot`.
4. **The `usePoints` hook has a manual `reload()` function** that re-fetches the doc. This is the workaround pattern for "I need fresh data but I'm not using listeners."

The app was built rapidly with one-shot reads as the simplest path each time. Nobody ever evaluated whether real-time updates were needed because the reads were "good enough" during development with <100 students.

**Recommendation (deferred to post-May 15):** The GC dashboard is the strongest candidate for `onSnapshot` — it currently loads student data once and never updates until page refresh. At 3,000 students, a GC watching their dashboard won't see new completions until they manually reload. File as GitHub issue.

---

## Race Condition Severity Ratings (for scope call)

| ID | Location | Severity | Frequency | Impact | Recommendation |
|----|----------|----------|-----------|--------|----------------|
| **C1** | App.tsx:279-315 (points race) | **CRITICAL** | Every section completion | Students lose earned points | **PR 1 — this week** |
| **C2** | AppRouter.tsx:271-278 (timetable race) | **HIGH** | Requires concurrent tabs | One completion silently lost | PR 1 or standalone — easy fix with `arrayUnion` |
| **C5** | useGamification.ts:245-316 (achievement race) | **MEDIUM** | Requires concurrent sessions detecting same achievement | Double bonus points awarded | PR 1 (same write path as C1) |
| **C3** | useDebriefSideEffects.ts:24-104 (mastery race) | **MEDIUM** | Requires two rapid debrief submissions | Topic mastery clobbered | Follow-up — lower frequency, less user-facing |
| **C4** | GCKeyEvents.tsx:71-89 (GC event race) | **LOW** | Requires two GCs editing simultaneously | School event lost | Follow-up — most schools have one GC |

---

## Executive Summary — Top 5 Findings

1. **Zero `onSnapshot` listeners in the entire codebase.** The listener-leak concern from the brief does not apply — every Firestore read is a one-shot `getDoc`/`getDocs`. This means no listener cleanup bugs, but also no real-time updates (data goes stale until the next manual refetch or page reload). This was not anticipated.
2. **Read-modify-write without transactions in 5 locations, including points and timetable completions.** Two concurrent sessions (e.g., student on phone + laptop) can clobber each other's progress. The gamification points path in App.tsx:279-332 is the highest-risk: it optimistically sets progress in React state, then writes to Firestore, then awards points via a separate `updateDoc` — a partial failure leaves points orphaned from progress.
3. **13 hooks expose fire-and-forget write callbacks with no unmount guard.** At 3,000 students these are low-risk individually (writes complete server-side regardless), but setState calls inside `.then()`/`.catch()` chains will throw React warnings and could cause subtle state corruption if the component tree has already unmounted.
4. **Unbounded collection queries in GCDashboard.tsx will break at scale.** `getDocs(query(collection(db, 'progress'), where('school', '==', school)))` fetches every student's full progress doc for the school — no limit, no pagination. At 500 students per school with ~50KB docs, that's 25MB per dashboard load.
5. **Silent error swallowing in 8+ files.** Failed Firestore writes are caught and logged to `console.error` but never surfaced to the user. At scale, "why isn't my data saving" support tickets will be untraceable.

---

## Critical Bugs (data corruption, cross-user leaks, lost writes)

### C1. Points awarded without progress saved — App.tsx:273-337

**Confidence:** Confirmed

App.tsx `handleProgressUpdate` does three sequential operations:
1. Line 279: `setUserProgress(prev => ({...prev}))` — optimistic React state update
2. Line 283: `await setDoc(progressDocRef, {[moduleId]: newProgress}, {merge: true})` — writes progress
3. Line 313-315: `await updateDoc(progressDocRef, {'pointsData.totalEarned': increment(finalPoints)})` — awards points

If step 2 succeeds but step 3 fails (network glitch), the user's progress is saved but their points are lost. The `catch` at line 333 shows a toast, but the progress write at step 2 already committed.

Conversely, if step 2 fails, the `catch` fires and steps 3+ never run — but step 1 (optimistic update) already mutated React state. The user sees the section as unlocked but it isn't persisted. On refresh, it reverts. No rollback.

**Proposed fix:** Batch the progress write and points increment into a single `writeBatch` or `runTransaction`. Roll back the optimistic update in the catch.

### C2. Read-modify-write race on timetable completions — AppRouter.tsx:268-284

**Confidence:** Confirmed

```tsx
const progressSnap = await getDoc(progressRef);
const completions = progressSnap.data().timetableCompletions || {};
const dayArr = [...(completions[dateKey] ?? [])];
if (!dayArr.includes(blockId)) dayArr.push(blockId);
await setDoc(progressRef, { timetableCompletions: updated }, { merge: true });
```

Two browser tabs completing blocks simultaneously: both read the same `completions`, both append their block, second write overwrites the first. One completion is silently lost.

**Proposed fix:** Replace with `runTransaction` or use `arrayUnion(blockId)` which is atomic.

### C3. Read-modify-write race on topic mastery — useDebriefSideEffects.ts:24-104

**Confidence:** Confirmed

Reads entire `topicMastery` object, modifies it in-memory, writes back with `merge: true`. Two concurrent debrief submissions (e.g., user completes two study sessions in quick succession) can clobber each other.

**Proposed fix:** Use `runTransaction`. The `gcNotifications.ts` file already demonstrates this pattern (line 57-68) and can serve as a template.

### C4. Read-modify-write race on GC school events — GCKeyEvents.tsx:71-89

**Confidence:** Confirmed

Same pattern: `getDoc` → modify events array → `setDoc`. Two GCs editing events simultaneously lose updates.

**Proposed fix:** Use `runTransaction`.

### C5. Cross-document race in achievement unlocking — useGamification.ts:245-316

**Confidence:** Likely

`checkAndUnlockAchievements` re-reads from Firestore (line 256) to get fresh data — good. But the save at line 296 (`saveGamificationData`) and the points award at line 304 (`updateDoc`) are separate operations. If two sessions run `checkAndUnlockAchievements` simultaneously, both could detect the same achievement as "new" and award bonus points twice.

The `checkInFlightRef` at line 246 prevents concurrent calls within the same session, but not across browser tabs/devices.

**Proposed fix:** Move achievement checking + points award into a single `runTransaction`.

---

## High-Severity Bugs (stale UI, missing cleanup, silent failures)

### H1. 13 hooks have write callbacks without unmount guards

**Confidence:** Confirmed

Every hook below returns callbacks that perform async Firestore writes, then call `setState` in `.then()`/`.catch()` chains. If the component unmounts while the write is in flight, React logs a warning and the state update is silently dropped (React 18+) — or in older React, causes a memory leak.

| Hook | Callbacks affected |
|------|--------------------|
| useGCFlags | flagStudent, unflagStudent, updateFlagNote, updateFlagPriority |
| useGifts | sendGift, markGiftPlaced |
| useIslandShop | purchaseItem, claimReward, placeGiftItem |
| useKudos | sendKudos |
| useMockResults | addMockResult, removeMockResult |
| useModuleResponses | saveResponse |
| useNorthStar | saveNorthStar |
| useQuests | claimReward |
| useSettings | updateSetting |
| useStudySession | saveSession |
| useTeachBack | submitTeachBack, markHelpful, markSeen |
| useTopicMastery | setTopicConfidence, importSyllabusTopics, bulkUpdate |
| useWeeklyChallenge | claimReward |

**Proposed fix:** Add an `isMountedRef` to each hook and guard setState calls inside async chains. The writes themselves should still complete (they're fire-and-forget to the server), but the state updates should be gated.

### H2. 4 useEffect data-loading hooks missing cancelled flags

**Confidence:** Confirmed

| Hook | Line | Issue |
|------|------|-------|
| useIslandShop | 56-91 | Async IIFE with no `cancelled` flag; setState after unmount |
| useStudySession | 64-80 | Same |
| useWeeklyChallenge | 37-100 | Same |
| useStrategyMastery | 21-108 | `compute()` called from effect with no cancellation |

These can set state after the component unmounts if the Firestore read takes longer than the component's lifetime.

**Proposed fix:** Add `let cancelled = false` + `return () => { cancelled = true }` pattern, matching the 13 hooks that already do this correctly.

### H3. Optimistic update without rollback — App.tsx:279

**Confidence:** Confirmed

```tsx
setUserProgress(prev => ({ ...prev, [moduleId]: newProgress }));  // Optimistic
try {
  await setDoc(progressDocRef, { [moduleId]: newProgress }, { merge: true });
  // ... points, achievements
} catch (error) {
  showToast('Couldn\'t save your progress', 'error');
  // ← No rollback of the optimistic update
}
```

User sees section as unlocked, toast says "couldn't save," but the UI doesn't revert. On refresh, the section reverts — a confusing split-brain experience.

**Proposed fix:** In the catch, call `setUserProgress(prev => ({ ...prev, [moduleId]: { unlockedSection: prevSection } }))` to roll back.

---

## Medium Severity (error handling, race conditions with low likelihood)

### M1. Silent error swallowing — 8+ files

**Confidence:** Confirmed

| File | Line | Pattern |
|------|------|---------|
| InnovationDataContext.tsx | 78 | `.catch(() => { ... })` — sets loading false, no error state |
| GCKeyEvents.tsx | 90 | `.catch(() => {})` — completely silent |
| useDebriefSideEffects.ts | 106-108 | `console.error` only |
| useIslandShop.ts | multiple | `.catch(console.error)` — no user feedback |
| useTopicMastery.ts | multiple | `.catch(console.error)` |
| useMockResults.ts | multiple | `.catch(console.error)` |
| useModuleResponses.ts | 53 | `.catch(console.error)` |
| AuthContext.tsx | 168 | Catch sets fallback user, no error surface |

**Proposed fix:** For critical writes (progress, points, achievements), show a toast on failure. For non-critical reads (innovation data, peer islands), a silent fallback is acceptable.

### M2. Island shop: two sequential writes without batch — useIslandShop.ts:200-203

**Confidence:** Confirmed

```tsx
await setDoc(progressRef, { islandState: newState }, { merge: true });
await setDoc(progressRef, { 'pointsData.totalSpent': increment(item.cost) }, { merge: true });
```

Two separate writes to the same doc. If the first succeeds and the second fails, the item is placed but the points aren't deducted. User gets a free item.

**Proposed fix:** Combine into a single `setDoc` with both fields, or use `writeBatch`.

### M3. useFlares.markHelpful — asymmetric cross-user write — useFlares.ts:458-471

**Confidence:** Likely

Marks a response as helpful (own doc), then tries to increment the responder's rescue count (another user's doc). If the second write fails (permission denied — Firestore rules may block cross-user progress writes), the helpful flag is set but rescue count isn't incremented.

**Proposed fix:** Accept the asymmetry (the helpful flag is the primary action) but log the failure prominently rather than silently catching.

### M4. Admin/GC student deletion — partial cleanup — AdminDashboard.tsx / GCDashboard.tsx

**Confidence:** Confirmed

```tsx
await deleteDoc(doc(db, 'progress', user.uid)).catch(() => {});
await deleteDoc(doc(db, 'users', user.uid));
```

Sequential deletes without batch. If progress delete succeeds but users delete fails, the student has a Firebase Auth account with no user doc — which hits the "no user doc" fallback path in AuthContext.

**Proposed fix:** Use `writeBatch` for atomic deletion. Also delete related docs (settings, streaks, responses, notifications) — currently orphaned.

---

## Low / Scale Concerns (cost, efficiency, refactor opportunities)

### L1. Unbounded collection query — GCDashboard.tsx

**Confidence:** Confirmed

```tsx
const q = query(collection(db, 'users'), where('school', '==', school));
const snaps = await getDocs(q);
```

Fetches ALL student docs for a school. At 500 students/school × ~2KB/doc = 1MB per load. Tolerable now, problematic at scale. The progress doc query is worse — progress docs are much larger (~50KB each with topic mastery, sessions, debriefs).

**Proposed fix:** Add `limit()` and implement cursor-based pagination. Or fetch user metadata separately from full progress docs.

### L2. No real-time listeners = stale data

**Confidence:** Confirmed

The entire codebase uses `getDoc`/`getDocs` exclusively. No `onSnapshot` anywhere. This means:
- Two browser tabs don't see each other's changes until refresh
- GC dashboard doesn't update when students complete work
- Points/streak displays can be stale for the entire session

This is a design decision, not a bug. But at 3,000 students, the GC dashboard would benefit from an `onSnapshot` listener for at least the student list.

**No immediate fix needed.** Flag for future consideration.

### L3. Multiple hooks read the same progress doc independently

**Confidence:** Confirmed

`getDoc(doc(db, 'progress', uid))` is called in: useStreak, usePoints, useQuests, useGamification, useInsights, useRecommendation, useStrategyMastery, useWeeklyChallenge, useTopicMastery, useMockResults, useStudySession, useFlares, useIslandShop — **13 hooks** reading the same document independently.

At mount time for a student viewing the tree + training hub, this could be 8-10 concurrent reads of the same doc. Firestore charges per read.

**Proposed fix (follow-up):** Centralize progress doc reading in ProgressContext. Hooks consume from context instead of making independent reads. This is an architectural change — flag for a separate PR.

### L4. GamificationContext.grantRankUpTiles — fire-and-forget without await

**Confidence:** Confirmed

```tsx
if (user) grantRankUpTiles(user.uid);  // No await, no error handling
```

If the write fails, the user doesn't get their tiles and is never told. Low-impact (cosmetic reward) but worth logging.

---

## Files Audited (43 total)

### hooks/ (24 files)
useDebriefSideEffects.ts, useFlares.ts, useGCFlags.ts, useGamification.ts, useGifts.ts, useInsights.ts, useIslandShop.ts, useKudos.ts, useMockResults.ts, useModuleResponses.ts, useNorthStar.ts, useOnlineStatus.ts, usePeerIslands.ts, usePoints.ts, useQuests.ts, useRecommendation.ts, useSettings.ts, useStrategyMastery.ts, useStreak.ts, useStudySession.ts, useTeachBack.ts, useTodaysFocus.ts, useTopicMastery.ts, useWeeklyChallenge.ts

### contexts/ (4 files with Firestore)
AuthContext.tsx, ProgressContext.tsx (imports only, no direct calls), InnovationDataContext.tsx, GamificationContext.tsx

### components/ (19 files with Firestore imports)
LoginPage.tsx, Auth.tsx, AppRouter.tsx, InnovationZone.tsx, FutureFinder.tsx, ComebackEngine.tsx, CAOPointsSimulator.tsx, AdminDashboard.tsx, GCDashboard.tsx, gc/GCKeyEvents.tsx, gc/gcNotifications.ts, gc/GCStudentDetail.tsx, SyllabusXRay.tsx, WarRoom.tsx, journey/JourneyView.tsx, SpacedRepetitionTimetable.tsx, AcademicJourneyGame.tsx, PointsPassport.tsx, study/StudySessionView.tsx

## Files Skipped

- **43 *Module.tsx files** — confirmed via `moduleRegistry.ts` that all modules use `ModuleLayout` + `ModuleShared` primitives; none import from `firebase/firestore`.
- **SettingsContext.tsx** — no Firestore imports (pure context).
- **NavigationContext.tsx** — no Firestore imports.
- **UI primitives** (ModuleLayout.tsx, ModuleShared.tsx, Toast.tsx, etc.) — no Firestore imports.

---

## Answers to Specific Audit Questions

| # | Question | Answer |
|---|----------|--------|
| 1 | Does every onSnapshot have cleanup? | **N/A — zero onSnapshot calls in the entire codebase.** |
| 2 | Do effects re-subscribe on dependency change? | Yes, hooks that depend on `uid` re-run when it changes. No listener resubscription needed (no listeners). |
| 3 | Listeners outside useEffect? | **N/A — no listeners.** |
| 4 | Cross-user data leaks from listener reuse? | **N/A — no listeners.** However, the one-shot read pattern is safe: each read uses the current `uid` from the effect closure. |
| 5 | Stale closures in onSnapshot callbacks? | **N/A.** For getDoc callbacks, most hooks use the `cancelled` flag pattern correctly. |
| 6 | Missing dependencies in write effects? | No critical cases found. Writes are in callbacks (useCallback), not effects. |
| 7 | setState after unmount in callbacks? | **Yes — 13 hooks.** See H1 above. |
| 8 | Multiple writes without batch? | **Yes — 5 locations.** See C1, C2, C3, C4, M2. |
| 9 | Optimistic updates without rollback? | **Yes — App.tsx:279.** See H3. |
| 10 | Read-modify-write needing transactions? | **Yes — 5 locations.** See C1-C5. |
| 11 | Write before listener catches up? | **N/A — no listeners.** |
| 12 | onSnapshot missing error callback? | **N/A — no onSnapshot calls.** |
| 13 | Swallowed errors? | **Yes — 8+ files.** See M1. |
| 14 | Writes on every render? | **No.** All writes are in callbacks or gated by conditions. |
| 15 | Unbounded collection queries? | **Yes — GCDashboard.tsx.** See L1. |
