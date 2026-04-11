# Navigation Audit

**Date:** 2026-04-11
**Scope:** App.tsx, contexts/, hooks/, AppRouter.tsx, InnovationZone.tsx

---

## (a) Current Nav State Shape

```
NavigationContext (useReducer)
├── viewState: ViewState          # which screen is rendered
│   → 'tree' | 'category' | 'module' | 'innovation-zone'
│   → 'dashboard' | 'learning-paths' | 'onboarding'
│   → 'my-journey' | 'gamification-hub' | 'study-session' | 'insights'
│
├── currentCategory: CategoryType | null
│   → e.g. 'architecture-mindset', 'science-growth', etc.
│
├── currentModuleId: string | null
│   → e.g. 'growth-mindset', 'bimodal-brain', etc.
│
└── cameFromJourney: boolean
    → true when module was opened from Innovation Zone

AuthContext (useState)
├── user: SessionUser | null      # null = show login
├── isLoadingAuth: boolean        # true until first onAuthStateChanged fires
└── loadedData: AuthLoadedData    # progress, profile, etc.
```

**Architecture matches the hypothesis:** navigation is hand-rolled React state with no router library. The provider tree is:

```
index.tsx
  <AuthProvider>         ← Firebase auth listener
    <ProgressProvider>   ← syncs Firestore data after auth resolves
      <NavigationProvider>  ← useReducer for view switching
        <App />
          <AppRouter />  ← giant if/else on viewState
```

**State NOT captured by NavigationContext:**
- Innovation Zone's `activeTool` (local useState in InnovationZone.tsx:77)
- Innovation Zone's `activeFilter` (local useState in InnovationZone.tsx:463)
- Study session step/phase (local state inside StudySessionView)
- Onboarding step (local state inside Onboarding.tsx)
- Any modal open/closed state (settings, passport, north star edit, change subjects)
- Timetable block context (App.tsx:152, useState)

---

## (b) Every Setter and Where It Is Called

### NavigationContext convenience functions (defined in contexts/NavigationContext.tsx)

Each function does: `dispatch(action)` + `window.history.pushState({view, ...extra}, '')` + `window.scrollTo(0,0)`.

| Function | Pushes to history? | Called from |
|----------|-------------------|------------|
| `navigateToTree()` | Yes | App.tsx:369,394,411 |
| `navigateToCategory(cat)` | Yes | App.tsx:340, AppRouter.tsx:201 |
| `navigateToModule(id, view, cat)` | Yes | App.tsx:344, AppRouter.tsx:205 |
| `navigateToInnovationZone()` | Yes | App.tsx:347, AppRouter.tsx:210 |
| `navigateToDashboard()` | Yes | App.tsx:349, AppRouter.tsx:211 |
| `navigateToLearningPaths()` | Yes | App.tsx:351, AppRouter.tsx:212 |
| `navigateToJourney()` | Yes | App.tsx:353, AppRouter.tsx:213 |
| `navigateToGamificationHub()` | Yes | App.tsx:355, AppRouter.tsx:214 |
| `navigateToStudySession()` | Yes | App.tsx:359,364, AppRouter.tsx:217 |
| `navigateToInsights()` | Yes | App.tsx:367, AppRouter.tsx:219 |
| `navigateToOnboarding()` | **No** | App.tsx:266 |
| `goBack()` | N/A (calls history.back()) | App.tsx:427,429, AppRouter.tsx:208,209 |

### Direct history API calls outside NavigationContext

| File | Line | Call | Purpose |
|------|------|------|---------|
| App.tsx | 259 | `window.history.replaceState({ view: 'tree' }, '')` | Seeds initial history entry when user lands on tree |

### The popstate listener (NavigationContext.tsx:112-142)

Handles browser back/forward by reading `e.state.view` and dispatching the corresponding action. Uses `isPopstateRef` flag to prevent pushState during popstate handling.

### Components with internal navigation state (NOT synced to history)

| Component | State | Effect |
|-----------|-------|--------|
| InnovationZone.tsx | `activeTool` (line 77) | Which tool is open. Back button sets it to null, does NOT call history.back() |
| StudySessionView | Internal step/phase state | Multi-step flow, no history entries |
| Onboarding.tsx | Internal `step` state | Multi-step wizard, no history entries |
| FutureFinder.tsx | Internal multi-step state | Has its own back logic |

---

## (c) Auth Gate Logic

**Location:** `AppRouter.tsx:221-227`

```tsx
// Line 221
if (isLoadingAuth) {
    return <LoadingSpinner />;
}

// Line 225
if (!user) {
    return <LoginPage handleLoginSuccess={handleLoginSuccess} />;
}
```

**How `isLoadingAuth` works (AuthContext.tsx):**
- Initialized to `true` (line 67)
- Set to `false` only inside the `onAuthStateChanged` callback (line 139)
- `onAuthStateChanged` is registered once on mount (line 72)

**How `user` gets set (AuthContext.tsx):**
- `onAuthStateChanged` fires with `FirebaseUser` or `null`
- If `FirebaseUser`: fetches user doc + progress doc from Firestore, then calls `setUser(sessionUser)` (line 91-98)
- If `null`: calls `setUser(null)` (line 136)
- `isLoadingAuth` set to `false` AFTER user state is resolved (line 139)

**Sequence on page refresh (happy path):**
1. React mounts. `isLoadingAuth=true`, `user=null`, `viewState='tree'`
2. AppRouter renders `<LoadingSpinner />` (line 221)
3. Firebase SDK loads persisted auth token
4. `onAuthStateChanged` fires with valid `FirebaseUser`
5. Firestore docs fetched (user + progress)
6. `setUser(sessionUser)`, `setIsLoadingAuth(false)`
7. AppRouter re-renders: user exists, viewState='tree' -> renders KnowledgeTree

**Edge case where login page flashes:**
- Firebase Auth persistence uses IndexedDB. If the browser clears it, or on slow devices, `onAuthStateChanged` may fire with `null` first (token expired or not yet loaded), then fire again with the user after token refresh.
- In that scenario: `isLoadingAuth` is set to `false` on the FIRST `null` fire (line 139). `user` is `null`. AppRouter shows LoginPage.
- Then `onAuthStateChanged` fires AGAIN with the real user. But by then, the user has already seen the LoginPage flash.
- This is the most likely cause of Bug #2.

---

## (d) Bug Analysis

### Bug 1: Browser back button jumps to random view

**Root cause: History stack and reducer state can desync.**

1. **InnovationZone sub-views don't push history entries.** If a user navigates: Tree -> Innovation Zone -> opens War Room tool -> opens a module from there, the history stack has entries for [tree, innovation-zone, module], but the Innovation Zone's `activeTool='war-room'` is not in any history entry. Pressing back from the module goes to the `innovation-zone` history entry, but `activeTool` has been reset (component unmounted and remounted), so the user sees the tool grid, not War Room. This feels like "jumping to the wrong place."

2. **Multiple navigation paths push duplicate/conflicting entries.** Both App.tsx and AppRouter.tsx define handlers that call the same nav functions (e.g., `handleSelectModule` exists in both). When a module is opened from KnowledgeTree's recommendation card or from a MobileBottomNav interaction, the history entry may not include the correct `category` context, so back goes somewhere unexpected.

3. **`goBack()` always calls `window.history.back()` (NavigationContext.tsx:217).** This pops the browser history stack, which fires popstate, which dispatches a nav action. But if any navigation occurred that DIDN'T push history (e.g., `navigateToOnboarding`, or InnovationZone's internal tool switches), the history stack and React state are out of sync. Back will jump to whatever the previous history entry was, which may not be the "previous screen" the user expects.

**Specific files/lines:**
- NavigationContext.tsx:212-214 — `navigateToOnboarding` doesn't push history
- InnovationZone.tsx:77,357-365 — `activeTool` managed via local useState, no history push
- NavigationContext.tsx:216-218 — `goBack()` is just `window.history.back()`

### Bug 2: Browser refresh drops to login page

**Root cause: Two independent issues.**

**Issue 2a — Auth gate race condition (AuthContext.tsx:72-143):**
Firebase's `onAuthStateChanged` can fire multiple times on startup. If the first fire is `null` (token expired, network delay), `isLoadingAuth` is set to `false` at line 139, and `user` remains `null`. AppRouter then renders LoginPage (line 225). A second `onAuthStateChanged` fire with the authenticated user corrects this, but there's a visible flash of the login page.

The fundamental problem: `setIsLoadingAuth(false)` runs unconditionally at line 139, regardless of whether this is the "definitive" auth resolution or just an intermediate state.

**Issue 2b — Nav state not persisted (NavigationContext.tsx:88-93):**
Even if auth resolves correctly, `initialState` is always `{ viewState: 'tree' }`. The URL is always `/` — no query params, no path segments. On refresh, there is zero information available to restore the user's previous view. They always land on the tree, regardless of where they were.

**Specific files/lines:**
- AuthContext.tsx:139 — `setIsLoadingAuth(false)` runs on first fire regardless
- NavigationContext.tsx:88-93 — `initialState` is hardcoded to `'tree'`
- NavigationContext.tsx:145-148 — `pushHistory` only uses `history.state`, never URL

### Bug 3: Transitions land on wrong view

**Root cause: The reducer + history push are not atomic, and the fallback is aggressive.**

1. **Non-atomic dispatch + pushState.** Each convenience function in NavigationContext.tsx (e.g., `navigateToModule` at lines 163-168) first dispatches to the reducer, then pushes history. If a rapid sequence of navigations happens (e.g., double-tap on a module card), two dispatches fire before the first pushHistory runs, resulting in a history entry that doesn't match the current reducer state.

2. **AppRouter fallback (line 529).** If no `viewState` matches any `if` branch, AppRouter calls `handleBackToTree()` AND returns `<LoadingSpinner />`. This is a render-time side effect — it calls `nav.goBack()` during render, which can trigger additional re-renders and push history entries. If the app ever transiently lands in an unmatched state, this fallback kicks the user back to tree unexpectedly.

3. **Race between onboarding redirect and initial render (App.tsx:264-268).** The useEffect at line 264 checks `needsOnboarding` and calls `nav.navigateToOnboarding()`. But `needsOnboarding` is derived from auth loaded data through two sync steps (AuthContext -> ProgressContext -> App local state). If the timing is off, the user might briefly render on 'tree' before being kicked to 'onboarding', with the tree's history entry still in the stack.

**Specific files/lines:**
- NavigationContext.tsx:163-168 — dispatch and pushState are separate calls
- AppRouter.tsx:529-530 — render-time side effect calling goBack()
- App.tsx:264-268 — onboarding redirect race

---

## Summary

| Bug | Primary cause | Key file:line |
|-----|--------------|---------------|
| Back button chaos | InnovationZone sub-views don't push history; `navigateToOnboarding` doesn't push history; `goBack` always uses browser history which may be stale | NavigationContext.tsx:212, InnovationZone.tsx:77 |
| Refresh shows login | `isLoadingAuth` set false on first `onAuthStateChanged` fire (may be null); nav state never persisted to URL | AuthContext.tsx:139, NavigationContext.tsx:88 |
| Wrong view on transition | Dispatch + pushState not atomic; render-time fallback calls goBack; onboarding redirect race | AppRouter.tsx:529, NavigationContext.tsx:163 |

---

## Architecture Conformance

The architecture matches the hypothesis exactly: navigation is hand-rolled React state, never synced to the URL, with a partial (and buggy) sync to `window.history.state`. No router library is used. No flags to raise — Step 2 can proceed as planned.
