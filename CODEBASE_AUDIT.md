# NextStepUni Codebase Audit

**Date:** 2026-04-13
**Auditor:** Claude Code (Opus 4.6)
**Scope:** Full codebase — 242 TypeScript files, 88,624 lines of code

---

## 1. Executive Summary — Top 10 Issues

| # | Severity | Issue | Location |
|---|----------|-------|----------|
| 1 | **CRITICAL** | Notifications collection wide open — any authed user can read/write any user's notifications | firestore.rules:95-97 |
| 2 | **CRITICAL** | Progress doc has zero write validation — users can set arbitrary point totals, fake progress | firestore.rules:50 |
| 3 | **HIGH** | ModuleShowcase navigation arrows hidden on mobile with no swipe gesture | ModuleShowcase.tsx:390,399 |
| 4 | **HIGH** | 35+ catch blocks log strings without error objects — production debugging impossible | Across all hooks/ and components/ |
| 5 | **HIGH** | All 7 modals lack Escape-to-close and focus trapping | SettingsModal, NorthStarEditModal, etc. |
| 6 | **HIGH** | Three.js memory leak — cloned GLTF scenes never disposed | journey/HexTile.tsx, HexDecoration.tsx |
| 7 | **MEDIUM** | `longestStreak` never auto-updates — computeStreak doesn't return it | ProgressContext.tsx:122, timetableAlgorithm.ts |
| 8 | **MEDIUM** | GC email squatting — student can register gc-{school}@nextstep.app first | LoginPage.tsx registration flow |
| 9 | **MEDIUM** | progress/{uid} unbounded arrays (studySessions, studyDebriefs) risk 1MB limit | Across write paths |
| 10 | **MEDIUM** | 3 modules have banned coloured left borders | ElaborativeInterrogation, DigitalDistraction, ExamCrisisManagement |

---

## 2. Demo Blockers (May 15th PwC — 25 minutes live)

### Will crash visibly
- **ModuleShowcase on mobile/tablet:** Navigation arrows are `hidden md:flex` (hidden below 768px). No swipe gestures. If demoing on a tablet or the projector triggers responsive mode, the carousel has no navigation. **Fix:** Add touch swipe or show arrows on all viewports.
- **Fresh student with no subjects:** If a demo student skips onboarding, several Innovation Zone tools will show empty states or error messages (CAO Simulator, War Room, Comeback Engine require subject profile).

### Could hang or stall
- **GC Dashboard with 500+ students:** Each student triggers an individual `getDoc` for progress — 500 sequential reads. Could take 5-10 seconds on slow connection. Show a loading state prominently.
- **Broadcast to Class:** 22 students = 22 parallel transactions. Should complete in 2-3 seconds but could appear to hang if no loading indicator shows.

### Could show Firebase error toast
- **Module completion with poor connection:** `handleProgressUpdate` uses `runTransaction` which retries up to 5 times. On failure, shows "Couldn't save your progress — check your connection" toast. Ensure stable WiFi for demo.
- **Innovation Zone timetable block completion:** Uses `arrayUnion` which is reliable but still shows toast on network failure.

### Could look broken on projector resolution
- **LoginPage aurora gradient:** The left panel is `hidden md:block` — only visible above 768px. Ensure projector resolution triggers the desktop layout.
- **GC Dashboard sidebar:** Starts collapsed (60px). If the demo starts here, the sidebar labels are invisible until clicked.

### Recommended demo path (safe)
1. Login as student (pre-registered, has completed onboarding) → show KnowledgeTree
2. Open one module → show essentials mode content → complete a section
3. Show Training Hub → points, streak, quest
4. Login as GC → show dashboard overview → show student list → show calendar with events
5. Send a broadcast → switch to student → show notification bell
6. Show Innovation Zone → open one tool briefly

---

## 3. Critical (security, data loss, auth bypass)

### C1. Notifications collection wide open
**File:** `firestore.rules:95-97`
**Rule:** `allow read, write: if request.auth != null;`
**Impact:** Any authenticated student can read any other student's notifications, write fake notifications to anyone, or delete/overwrite notifications. A student at School A can write notifications to students at School B.
**Fix:** Restrict to self-read/write + GC-write using a Cloud Function for GC broadcasts instead of client-side writes.

### C2. Progress doc has no write validation
**File:** `firestore.rules:50`
**Rule:** `allow read, write: if request.auth != null && request.auth.uid == userId;`
**Impact:** A user can set `pointsData.totalEarned` to 999999, fake module completions, or write arbitrary data. No field restrictions, no type checking, no size limits.
**Fix:** Add field-level validation for critical fields (pointsData, gamification), or move points-awarding to a Cloud Function.

### C3. Flares responseCount not pinned
**File:** `firestore.rules:180-188`
**Impact:** Unlike teachbacks (which pin `helpfulCount` to `resource.data.helpfulCount + 1`), the flares update rule allows ANY value for responseCount. A peer could set it to 999.
**Fix:** Add `request.resource.data.responseCount == resource.data.responseCount + 1` constraint.

### C4. Cross-user progress write always fails silently
**File:** `hooks/useFlares.ts:443-462`
**Impact:** `rescueCount` and `lighthouseLevel` writes to another user's progress doc are blocked by Firestore rules. The feature silently doesn't work. The lighthouse level system is broken.
**Fix:** Move cross-user progress writes to a Cloud Function.

---

## 4. High (significant bugs, performance, brand violations)

### H1. Mobile carousel navigation broken
**File:** `components/ModuleShowcase.tsx:390,399`
**Issue:** Left/right arrows have `hidden md:flex` — hidden on mobile. No swipe gesture alternative. Bottom chips are the only mobile navigation.
**Fix:** Add Framer Motion drag gesture or show arrows on all viewports.

### H2. Error swallowing epidemic
**Files:** 35+ catch blocks across hooks/ and components/
**Issue:** Catch blocks log `'Failed to X:'` as a string without appending the actual error object. ~15 catch blocks are completely empty `catch {}`. Only 6 out of 70+ catch blocks show user-facing feedback.
**Fix:** Append error object to all console.error calls. Add toast notifications for user-facing operations.

### H3. No modal accessibility
**Files:** SettingsModal, NorthStarEditModal, ChangeSubjectsModal, ReflectionModal, RewardShopModal, StudyJournalModal, StudyPassportModal
**Issue:** None support Escape-to-close or focus trapping. 35+ icon-only close buttons lack `aria-label`.
**Fix:** Add `useEffect` for Escape key handler and implement focus trap.

### H4. Three.js memory leak
**Files:** `components/journey/hex/HexTile.tsx:29`, `HexDecoration.tsx:33`
**Issue:** `scene.clone(true)` creates new GPU-resident geometry and material objects that are never `.dispose()`d on unmount.
**Fix:** Add cleanup in useEffect return that traverses the cloned scene and disposes geometries/materials.

### H5. GC email squatting
**File:** `components/LoginPage.tsx`
**Issue:** A student can register with `gc-marino@nextstep.app` before the GC account is provisioned, blocking the real GC.
**Fix:** Validate email format on registration — reject emails matching `gc-*@nextstep.app` or `admin@nextstep.app`.

### H6. Coloured left borders in 3 modules (banned)
**Files:** `ElaborativeInterrogationModule.tsx:98-101,170`, `DigitalDistractionModule.tsx:150,160,170`, `ExamCrisisManagementModule.tsx:627,643,659,675,861`
**Fix:** Replace `border-l-{color}` with dots, tints, or coloured text per CLAUDE.md design rules.

### H7. LoginPage wrong background color
**File:** `components/LoginPage.tsx:33`
**Issue:** Uses `#FAFAF7` instead of the design system cream `#FDF8F0`.
**Fix:** Change `backgroundColor: '#FAFAF7'` to `backgroundColor: '#FDF8F0'`.

---

## 5. Medium (code quality, maintainability, schema drift)

### M1. longestStreak never auto-updates
**Files:** `components/timetableAlgorithm.ts`, `contexts/ProgressContext.tsx:122`
**Issue:** `computeStreak` doesn't return `longestStreak`. The context falls back to `rawProgressDoc.timetableStreak?.longestStreak` which is only written by InnovationZone. Streak shields depend on this value.
**Fix:** Have `computeStreak` track and return `longestStreak`, or write it when current streak exceeds saved longest.

### M2. progress/{uid} approaching 1MB limit
**Issue:** `studySessions` (arrayUnion, ~200 bytes each) and `studyDebriefs` (arrayUnion) grow unbounded. At 3 sessions/day for 2 years: ~219KB for sessions alone. Combined with topicMastery, islandState, gamification, timetableCompletions: risk of hitting 1MB.
**Fix:** Archive old sessions to a subcollection after N entries, or implement TTL-based cleanup.

### M3. GamificationContext is dead code
**File:** `contexts/GamificationContext.tsx`
**Issue:** Defined but not used in the provider tree (index.tsx). App.tsx manages all gamification UI state directly. Contains duplicate `grantRankUpTiles` logic (also in App.tsx:180).
**Fix:** Either integrate GamificationContext into the provider tree and remove App.tsx duplicates, or delete the context entirely.

### M4. Dead Firestore rules for streaks collection
**File:** `firestore.rules:71-73`
**Issue:** Rules exist for `streaks/{userId}` but no code reads from or writes to this collection. Streak data lives in `progress/{uid}.timetableStreak`.
**Fix:** Remove the dead rules.

### M5. Module registry/courseData mismatch
**Files:** `moduleRegistry.ts` (83 entries), `courseData.ts` (81 entries)
**Issue:** `mastering-english-protocol` and `mastering-business-protocol` are registered but have no courseData metadata. `KnowledgeCompressionModule.tsx` exists as a file but is in neither registry nor courseData.
**Fix:** Add missing courseData entries or remove orphan registrations. Delete KnowledgeCompressionModule.tsx.

### M6. setDoc inside React state updaters
**Files:** `hooks/useMockResults.ts:76-79`, `hooks/useTopicMastery.ts:81-91,99-111,114-131`
**Issue:** Firestore `setDoc` is called inside `setState(prev => { ... setDoc(...); return next; })` — side effects inside state updaters is a React anti-pattern. Could fire multiple times if React batches state updates.
**Fix:** Move `setDoc` outside the updater, after the `setState` call.

### M7. useNorthStar missing dependency
**File:** `hooks/useNorthStar.ts:15`
**Issue:** `useEffect` has `[]` deps but reads `auth.currentUser?.uid` inside. Won't re-run on user change (logout → login as different user).
**Fix:** Add `uid` parameter or use `useAuth()` and include `user?.uid` in deps.

### M8. Concurrent pointsData write hazard
**Issue:** InnovationZone writes `pointsData` as a full object (`{ totalEarned: X, totalSpent: Y }`) via `setDoc` merge, while App.tsx transaction uses dot-notation (`'pointsData.totalEarned'`). If concurrent, the full-object write clobbers the dot-notation write.
**Fix:** Use dot-notation for all pointsData writes, or use `increment()` consistently.

### M9. timetableReflections read but never written
**File:** `hooks/useGamification.ts:108`
**Issue:** Reads `data.timetableReflections` from progress doc, but no code in the codebase writes this field. The `totalReflections` gamification stat is always 0.
**Fix:** Either write timetable reflections data, or remove the stat.

### M10. Navigation state not cleared on logout
**File:** `contexts/NavigationContext.tsx`
**Issue:** When user logs out, NavigationContext state persists. If user B logs in without a page refresh, stale view state from user A may briefly persist.
**Fix:** Dispatch `NAVIGATE_TO_TREE` on logout.

---

## 6. Low (nits, polish, future-proofing)

### L1. Bonus flash comment says 15%, code uses 8%
**File:** `hooks/useGamification.ts:369`
**Fix:** Update comment to match `BONUS_FLASH_CHANCE = 0.08`.

### L2. SubjectModule lacks essentials mode
**File:** `components/SubjectModule.tsx`
**Issue:** 29 data-driven subject modules don't support essentials mode.
**Fix:** Add `useEssentialsMode()` to SubjectModule and provide shorter content in `subjectModuleData.ts`.

### L3. ErrorBoundary discards error details
**File:** `components/ErrorBoundary.tsx:24`
**Issue:** `componentDidCatch` prefixes error/info with `_` and only logs `'App error caught by boundary'`.
**Fix:** Log the actual error and errorInfo.

### L4. ErrorBoundary uses wrong accent color
**File:** `components/ErrorBoundary.tsx:57`
**Issue:** Reload button uses `#6366f1` (indigo) fallback, not teal `#2A7D6F`.
**Fix:** Change to `backgroundColor: '#2A7D6F'`.

### L5. PWA manifest invalid purpose
**File:** `vite.config.ts:27`
**Issue:** Apple touch icon has `purpose: 'apple touch icon'` which is not a valid W3C manifest purpose value.
**Fix:** Change to `purpose: 'any'`.

### L6. PWA background_color mismatch
**File:** `vite.config.ts:22`
**Issue:** `background_color: '#131311'` (dark) but app background is cream. Causes dark flash on PWA launch.
**Fix:** Change to `background_color: '#FDF8F0'`.

### L7. No Tailwind CDN offline caching
**Issue:** The service worker caches Google Fonts but not the Tailwind CDN CSS. App loses all styling offline.
**Fix:** Add a workbox runtime caching rule for `cdn.tailwindcss.com`.

### L8. jspdf not code-split
**Issue:** `jspdf` and `jspdf-autotable` are not in `manualChunks`. If statically imported, they inflate the main bundle.
**Fix:** Add to manualChunks or ensure they're only dynamically imported.

---

## 7. Architecture Observations

1. **App.tsx is still a partial god object** — manages 19 pieces of state, 8 hooks, gamification toast queue, rank detection, and multiple Firestore write handlers. The context extraction (Auth, Progress, Navigation) was effective but gamification state remains inline.

2. **Zero onSnapshot listeners** — the entire app uses one-shot reads. This is a conscious simplification that trades real-time updates for reduced complexity. The GC dashboard is the strongest candidate for eventual onSnapshot migration.

3. **progress/{uid} is a mega-document** — 27+ top-level fields plus 81 possible module progress entries. This is the biggest architectural debt. A subcollection split (sessions, debriefs → subcollections) would reduce document size and improve query flexibility, but requires migration.

4. **The essentials mode implementation is elegant** — conditional content inside each module file avoids duplication of interactive components. The `fullSectionsCount` prop for consolidated sections is a clean solution for progress tracking.

5. **The URL-sync navigation system works but is fragile** — the `isPopstateRef` flag, `__navSynced` tag, and effect-based URL sync have subtle timing dependencies. A router library would be more robust but the current implementation is functional.

6. **Context dependency graph is clean** — AuthContext → ProgressContext → hooks. No circular dependencies. The GamificationContext exists but is unused (dead code).

---

## 8. Statistics

| Metric | Value |
|--------|-------|
| TypeScript files | 242 |
| Total lines of code | 88,624 |
| JS chunks in build | 133 |
| Largest chunk | vendor-three: 1.1MB |
| Main app chunk (index) | 836KB |
| GCDashboard chunk | 552KB |
| InnovationZone chunk | 337KB |
| Runtime dependencies | 10 |
| Dev dependencies | 12 |
| `any` type usage | 27 instances |
| `@ts-ignore` / `@ts-expect-error` | 0 |
| Build warnings | 1 (chunk size warning) |
| Build errors | 0 |
| Lint warnings | 0 |
| Module components | 56 files (55 standard + SubjectModule factory) |
| Module registry entries | 83 (54 standard + 29 subject) |
| CourseData entries | 81 (52 standard + 29 subject) |
| Firestore collections with rules | 13 |
| Firestore collections without rules | 0 (default deny catches all) |
| Custom hooks | 25 |
| Context providers | 6 (Auth, Progress, Navigation, Gamification*, Innovation, Settings) |
| Essentials mode coverage | 55/56 module files (SubjectModule missing) |

*GamificationContext exists but is not in the provider tree
