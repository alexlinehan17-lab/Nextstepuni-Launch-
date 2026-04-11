# Onboarding Refresh → Login Screen Bug

**Date:** 2026-04-11
**Symptom:** Refresh at onboarding step 3 shows the login screen, not onboarding.

---

## 1. What URL is in the address bar mid-onboarding?

**Depends on whether you're running the deployed site or the dev server with local changes.**

### Deployed site (old code, pre-PR)

**URL is `/` — onboarding is never in the URL.** The old `navigateToOnboarding()` at NavigationContext.tsx:212-214 dispatched the reducer action but explicitly did NOT call `pushHistory()`:

```tsx
// OLD CODE — no pushHistory call
const navigateToOnboarding = useCallback(() => {
  dispatch({ type: 'NAVIGATE_TO_ONBOARDING' });
}, []);
```

Every other navigate function called `pushHistory()`. Onboarding was the sole exception. So the URL stays as `/` the entire time the user is in onboarding. `VALID_VIEWS` is irrelevant — serialization never runs.

### Dev server (new code, local changes)

**URL should be `/?view=onboarding`.** The new `navigateToOnboarding()` calls `navigate()` → `dispatch()`, then the URL-sync effect pushes `?view=onboarding`. `VALID_VIEWS` (NavigationContext.tsx:59-63) does include `'onboarding'`. `serializeToURL` at line 67 emits `view=onboarding` because `state.viewState !== 'tree'`.

I traced the push: redirect effect fires (App.tsx:262) → `navigateToOnboarding()` → dispatch changes `viewState` to `'onboarding'` → URL-sync effect at line 172 sees `changed = true` (prev was `'tree'`, now `'onboarding'`) → calls `pushState({..., __navSynced: true}, '', '?view=onboarding')`.

**Conclusion: if you reproduced on the deployed site, the URL was `/`, which fully explains the bug — there's nothing to hydrate from on refresh. If you reproduced on the dev server, the URL was `/?view=onboarding` and the bug has a different cause (see section 3).**

---

## 2. Render sequence on refresh, step by step

### Path A: Refresh at `/` (deployed site or if URL sync failed)

| Step | What fires | State | Renders |
|------|-----------|-------|---------|
| 1 | `getInitialState()` | `viewState='tree'` (no URL to hydrate) | — |
| 2 | First render | `userResolved=false`, `user=null`, `viewState='tree'` | **Branded spinner** |
| 3 | URL-sync effect | `replaceState({viewState:'tree', __navSynced:true}, '', '/')` | — |
| 4 | `onAuthStateChanged` fires | See section 3 for fork | — |
| 5a | Happy: user resolved | `userResolved=true`, `user` exists, `viewState='tree'` | **KnowledgeTree** |
| 5b | Unhappy: null first | Grace timer starts (500ms) | **Branded spinner** (still) |
| 5c | Grace timer fires | `userResolved=true`, `user=null` | **LoginPage** |
| 5d | Second callback with user (within 500ms) | Timer cancelled, `userResolved=true`, `user` exists | **KnowledgeTree** |
| 6a | Redirect effect | `needsOnboarding && viewState==='tree'` → `navigateToOnboarding()` | **Onboarding step 1** |

With `userResolved` + grace period: spinner holds for up to 500ms if the first callback is null, giving Firebase time to fire the real user. LoginPage only shows after the grace period expires with no user.

### Path B: Refresh at `/?view=onboarding` (new code, URL sync worked)

| Step | What fires | State | Renders |
|------|-----------|-------|---------|
| 1 | `getInitialState()` | `viewState='onboarding'` (from URL) | — |
| 2 | First render | `userResolved=false`, `viewState='onboarding'` | **Branded spinner** |
| 3 | `onAuthStateChanged` fires | — | — |
| 4a | Happy: user resolved | `userResolved=true`, `user` exists, `viewState='onboarding'` | **Onboarding step 1** |
| 4b | Unhappy: null, grace, then user | Spinner holds → `userResolved=true`, `user` exists | **Onboarding step 1** |
| 4c | Genuinely logged out | Grace expires, `userResolved=true`, `user=null` | **LoginPage** |

---

## 3. Onboarding is INSIDE the auth gate — now protected by userResolved

AppRouter.tsx:

```tsx
// Line 223 — auth gate (UPDATED: now uses userResolved)
if (!userResolved) { return <branded spinner>; }

// Line 234 — login gate
if (!user) { return <LoginPage />; }

// ... admin, GC checks ...

// Line 353 — onboarding (BELOW both gates)
if (viewState === 'onboarding') {
  return <Onboarding ... />;
}
```

**Onboarding is still behind both gates**, but the spinner now holds until `userResolved` is true. Since `userResolved` waits for either a non-null user OR the grace timer to expire, the LoginPage only appears when we're confident the user is genuinely logged out. The 500ms grace covers the Firebase token-refresh scenario.

---

## 4. The onboarding redirect logic

App.tsx:261-265 (unchanged from previous audit — still correct):

```tsx
useEffect(() => {
  if (authResolved && progressLoaded && user && !user.isAdmin &&
      user.role !== 'gc' && needsOnboarding && viewState === 'tree') {
    nav.navigateToOnboarding();
  }
}, [authResolved, progressLoaded, user, needsOnboarding, viewState]);
```

This redirect only fires when `viewState === 'tree'`. On refresh with `/?view=onboarding`, `viewState` is `'onboarding'`, so it does NOT fire. Correct.

---

## 5. Is anything overriding the URL-seeded state on mount?

Same findings as before — no code path overrides `viewState='onboarding'` on mount.

---

## Fixes applied (2026-04-11)

### Fix 1: Admin early-return (AuthContext.tsx:86-95)

Added `authResolvedRef.current = true`, `setAuthResolved(true)`, and `setUserResolved(true)` to the admin branch before the `return`. All code paths through `onAuthStateChanged` now resolve both `authResolved` and `userResolved`.

Audited every other path in the callback — the admin branch was the only early return that skipped the resolution block. All other paths (regular user success, no-user-doc/signOut, catch error, null firebaseUser) fall through to the resolution block at the end.

### Fix 2: userResolved via auth.authStateReady() (AuthContext.tsx)

Introduced `userResolved: boolean` in AuthContext.

**Initial resolution** is driven by `auth.authStateReady()` — a Firebase v12 API that resolves a promise once the persistence layer (IndexedDB) has been fully read. This guarantees the first `onAuthStateChanged` callback has the definitive auth state before `userResolved` flips true. No timers, no guessing.

```tsx
useEffect(() => {
  auth.authStateReady().then(() => {
    setUserResolved(true);
  });
}, []);
```

**Why this replaced the 500ms grace timer:** The timer was a heuristic — it guessed that Firebase would resolve within 500ms, which isn't guaranteed and adds latency for genuinely logged-out users. `authStateReady()` is Firebase's own signal that the persistence layer is ready, so it's both faster (no fixed delay) and more correct (no race condition).

**`onAuthStateChanged` is kept as the ongoing subscription** for auth changes after initial load (login, logout, token refresh). It sets `user`, `loadedData`, `isLoadingAuth`, and `authResolved` as before.

**`handleLoginSuccess` still sets `userResolved(true)` explicitly** — belt-and-braces so manual login renders the app immediately without waiting for the `onAuthStateChanged` Firestore round-trip.

**AppRouter gate changed:** `!authResolved` → `!userResolved`. Branded spinner shows until `userResolved` is true.

### Fix 3: navigateToOnboarding verified

Confirmed: `navigateToOnboarding()` (NavigationContext.tsx:281) calls `navigate()` → `dispatch()`. The URL-sync effect then pushes `?view=onboarding`. `'onboarding'` is in both the `ViewState` union (line 13) and `VALID_VIEWS` (line 61). `deserializeFromURL` reads it back on cold start.

### Fix 4: Category validation guard (AppRouter.tsx)

Added `if (!categoryTitles[currentCategory])` check before the category render branches. Garbage `cat` values now redirect to tree via `FallbackRedirect`.

---

## Test scenario traces (static analysis — code, not runtime)

### A. Refresh on step 3 of onboarding (authenticated user)

1. URL: `/?view=onboarding`
2. `getInitialState()` → `{ viewState: 'onboarding' }`
3. First render: `userResolved=false` → branded spinner
4. `onAuthStateChanged` fires with cached user (IndexedDB) → Firestore docs fetched → `setUser(sessionUser)`, `setUserResolved(true)`
5. Re-render: `userResolved=true`, `user` exists → passes auth gate
6. `viewState === 'onboarding'` → renders Onboarding (step 1 — step state is local, not in URL)
7. Redirect effect: `viewState` is `'onboarding'`, not `'tree'` → does NOT fire

**Result: spinner → onboarding (step 1).** LoginPage never shows unless the user is genuinely logged out (grace timer expires with no user).

### B. Refresh as admin user

1. URL: `/` (admin view doesn't push a specific URL in current code)
2. `getInitialState()` → `{ viewState: 'tree' }`
3. First render: `userResolved=false` → branded spinner
4. `onAuthStateChanged` fires with admin user → admin branch: `setUser({isAdmin: true})`, `setUserResolved(true)`, `setAuthResolved(true)`, return
5. Re-render: `userResolved=true`, `user.isAdmin=true` → AppRouter line 238: renders AdminDashboard

**Result: spinner → AdminDashboard.** No infinite spinner (admin bug fixed).

### C. Refresh with expired token (genuinely logged out)

1. URL: whatever it was (e.g., `/?view=module&mod=growth-mindset`)
2. `getInitialState()` → `{ viewState: 'module', currentModuleId: 'growth-mindset' }`
3. First render: `userResolved=false` → branded spinner
4. `onAuthStateChanged` fires with `null` (token expired, no cached session)
5. `isFirstCallback = true` → grace timer starts (500ms)
6. No second callback arrives → timer fires → `setUserResolved(true)`, `user` is null
7. Re-render: `userResolved=true`, `!user` → LoginPage

**Result: spinner (up to 500ms) → LoginPage.** No flash of app content — the module view never renders because `userResolved` was false during the spinner phase.

### D. Refresh on deep-linked module as authenticated user

1. URL: `/?view=module&mod=growth-mindset&cat=architecture-mindset`
2. `getInitialState()` → `{ viewState: 'module', currentModuleId: 'growth-mindset', currentCategory: 'architecture-mindset' }`
3. First render: `userResolved=false` → branded spinner
4. `onAuthStateChanged` fires with user → docs fetched → `setUser(...)`, `setUserResolved(true)`
5. Re-render: `userResolved=true`, `user` exists → passes auth gate
6. `viewState === 'module' && currentModuleId` → renders GrowthMindsetModule

**Result: spinner → module.** Correct restoration from URL.

### E. Cold load of `/?view=module&mod=growth-mindset&cat=architecture-mindset` while logged out

1. `getInitialState()` → `{ viewState: 'module', currentModuleId: 'growth-mindset', currentCategory: 'architecture-mindset' }`
2. First render: `userResolved=false` → branded spinner
3. `onAuthStateChanged` fires with `null` (no session) → first callback → grace timer starts
4. Grace timer fires (500ms) → `setUserResolved(true)`, `user` null
5. Re-render: `userResolved=true`, `!user` → LoginPage
6. User logs in → `handleLoginSuccess(user)` → `setUser(user)`, `setUserResolved(true)`
7. Re-render: `user` exists → passes auth gate
8. `viewState === 'module' && currentModuleId` → renders GrowthMindsetModule

**Result: spinner → LoginPage → (login) → module.** The URL-seeded `viewState` survives the login flow because nothing navigates away from it. The nav state is `{ viewState: 'module', currentModuleId: 'growth-mindset', ... }` throughout — only the auth gate determines what renders. No extra work needed.

**Caveat:** The `onAuthStateChanged` callback will fire after login and do its own Firestore fetches, setting `user` and `loadedData` again. The `handleLoginSuccess` call provides immediate user state so the app renders fast; the subsequent `onAuthStateChanged` callback fills in the full data (progress, profile, etc.). This double-set is benign — React batches the updates.

---

## Design note: why authStateReady() instead of a timer

The initial implementation used a 500ms grace timer to cover the case where `onAuthStateChanged` fires with `null` before the real user during token refresh. This was replaced with `auth.authStateReady()` (Firebase v12.8.0, `package.json:15`) because:

1. **No guessing.** `authStateReady()` is Firebase's own signal that the persistence layer (IndexedDB) has been fully read. It resolves at exactly the right moment — not 500ms later, not before.
2. **No latency for logged-out users.** The timer added a fixed 500ms delay before showing LoginPage to genuinely logged-out users. `authStateReady()` resolves as soon as IndexedDB confirms there's no cached session.
3. **Simpler code.** No timer ref, no cancel logic, no "is this the first callback" tracking. One `useEffect` with one `.then()`.
