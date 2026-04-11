# Innovation Zone Back Button Ping-Pong Bug

**Date:** 2026-04-11
**Symptom:** Clicking into an IZ tool, then clicking the in-app back arrow, returns to the tool grid — but clicking back again sends the user back INTO the tool. Ping-pong between tool and grid.

---

## 1. What the in-app back button calls

Two call sites in InnovationZone.tsx:

**Line 490 — Header back arrow:**
```tsx
onClick={activeTool ? () => setActiveTool(null) : onBack}
```
When a tool is active, calls `setActiveTool(null)`. When on the grid, calls `onBack` (which is `nav.goBack()` from AppRouter:208).

**Line 627 — ToolErrorBoundary onBack:**
```tsx
onBack={() => setActiveTool(null)}
```

Both call `setActiveTool(null)` — which dispatches `SET_ACTIVE_TOOL` to the reducer → creates new state with `activeTool: null` → triggers the URL-sync effect.

## 2. The URL-sync effect: push vs pop problem

NavigationContext.tsx:172-193:

```tsx
useEffect(() => {
  if (isPopstateRef.current) { isPopstateRef.current = false; return; }
  const url = serializeToURL(state);
  if (!window.history.state?.__navSynced) {
    window.history.replaceState(...);
  } else {
    const changed = prev.viewState !== state.viewState
      || prev.activeTool !== state.activeTool  // ← this triggers
      || ...;
    if (changed) {
      window.history.pushState(...);  // ← PUSHES instead of popping
    }
  }
}, [state]);
```

**The effect does NOT distinguish forward navigation from backward navigation.** Every state change that passes the `changed` check results in a `pushState`. There is no mechanism to say "this state change is a 'going back' action — pop the stack instead of pushing."

## 3. The history stack trace

```
User action          | History stack after
---------------------|-----------------------------------
Enter IZ             | [tree, innovation-zone]
Click tool (e.g. WR) | [tree, innovation-zone, innovation-zone&tool=war-room]
Click in-app back    | setActiveTool(null) → pushState → [tree, innovation-zone, innovation-zone&tool=war-room, innovation-zone]
Click in-app back    | onBack → nav.goBack() → history.back() → popstate → restores innovation-zone&tool=war-room → [tree, innovation-zone, innovation-zone&tool=war-room]
```

**Step 3 is the bug.** The in-app back arrow calls `setActiveTool(null)` which changes the state, which triggers the URL-sync effect, which PUSHES a new `innovation-zone` entry on top of the existing `innovation-zone&tool=war-room` entry. Now the stack has BOTH entries and `history.back()` ping-pongs between them.

## 4. Comparison with Library → module flow

AppRouter.tsx:208-209:
```tsx
const handleBackToTree = () => { nav.goBack(); };
const handleBackToCategory = () => { nav.goBack(); };
```

The Library/module back buttons call `nav.goBack()` which calls `window.history.back()`. This POPS the history stack (the browser fires popstate, the popstate handler restores the previous state, the URL-sync effect skips because `isPopstateRef` is true). **The stack stays clean.**

The Innovation Zone back button calls `setActiveTool(null)` which is a FORWARD navigation (dispatch + pushState) disguised as a back action. It pushes instead of popping.

## 5. Does this bug exist elsewhere?

**No.** `setActiveTool(null)` is only called in InnovationZone.tsx (lines 490, 627). Every other back button in the codebase uses `nav.goBack()` → `window.history.back()` → popstate, which correctly pops.

The Innovation Zone is the only component that has sub-navigation (activeTool) managed via `SET_ACTIVE_TOOL` dispatch rather than a full view-level navigation. It's the only place where "going back" means "change a field within the same view" rather than "go to a different view."

## 6. Fix options

**Option A — Make the in-app back button call `nav.goBack()` instead of `setActiveTool(null)`:**
When activeTool is set, clicking back should pop the history stack (which restores the previous state where activeTool was null). This matches the Library/module pattern.

Pros: Simple, consistent with every other back button.
Cons: Only works if the history stack actually has the tool-less IZ entry. If the user deep-linked directly to `?view=innovation-zone&tool=war-room`, there's no previous entry to pop to.

**Option B — Make the URL-sync effect use `replaceState` instead of `pushState` for activeTool changes within the same view:**
When only `activeTool` changes (viewState stays the same), replace the current history entry instead of pushing a new one. This means "entering a tool" replaces the IZ entry rather than adding a new one, and "leaving a tool" replaces back to the tool-less URL.

Pros: No history stack buildup.
Cons: Browser back from a tool would skip IZ entirely and go to tree (no intermediate stop at the tool grid). This might not be the desired behavior.

**Option C — Hybrid: push when entering a tool, pop when leaving:**
`setActiveTool(toolId)` pushes (current behavior, correct).
`setActiveTool(null)` calls `window.history.back()` instead of dispatching (pops the pushed entry).

Pros: History stack stays clean, browser back works correctly.
Cons: Assumes every `setActiveTool(null)` call has a matching pushed entry. If called without a prior push (e.g., on mount with no tool), it would pop to the wrong place.

**Recommended: Option A.** Change the two `setActiveTool(null)` call sites in InnovationZone.tsx to `nav.goBack()`. This is one line each, matches the pattern used everywhere else, and correctly pops the history stack. The deep-link edge case (Option A's con) is low-risk — deep-linking directly to a tool is rare, and `goBack()` would still navigate away from IZ (just to wherever the user came from before, which is fine).

---

## Resolution

Fixed in commit by replacing both `setActiveTool(null)` calls (lines 490, 627) with `nav.goBack()`.

## Test coverage gap

The nav PR manual checklist tested one-way traversals (tool → hub → tree) but not round-trips (tool → hub → tool → hub). Future nav changes need round-trip scenarios in the test plan. Specifically: enter a sub-view, go back, then press browser-back — verify the stack doesn't ping-pong.
