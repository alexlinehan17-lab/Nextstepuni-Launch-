# Round-Trip Navigation Audit

**Date:** 2026-04-11
**Trigger:** IZ back button ping-pong bug — setState-as-back pattern pushed instead of popping history
**Scope:** Every back button, close button, and sub-view dismissal in the codebase

---

## Key distinction: history-backed vs local-state sub-views

The IZ bug happened because `activeTool` was migrated into NavigationContext (PR 1, nav refactor). Setting it pushes a history entry via the URL-sync effect. Clearing it also pushes instead of popping.

**Modals and local-state sub-views (SettingsModal, RewardShopModal, etc.) do NOT have this bug.** They use local `useState` which never pushes history entries. Opening a modal doesn't push, so closing it with `setState(false)` is correct — there's nothing to pop.

The bug pattern only applies to state managed through NavigationContext (which pushes history entries via the URL-sync effect).

---

## All back-button call sites

### CORRECT — uses nav.goBack() / window.history.back() (pops history)

| File:Line | Handler | Notes |
|-----------|---------|-------|
| AppRouter.tsx:208 | `handleBackToTree()` → `nav.goBack()` | Tree back button |
| AppRouter.tsx:209 | `handleBackToCategory()` → `nav.goBack()` | Category/module back button |
| AppRouter.tsx:445 | `handleBackToTree()` → `nav.goBack()` | Showcase header back |
| AppRouter.tsx:506 | `handleBackToCategory()` → `nav.goBack()` | Module error boundary back |
| AppRouter.tsx:532 | `handleBackToCategory()` → `nav.goBack()` | Module not found back |
| InnovationZone.tsx:490 | `nav.goBack()` (when tool active) / `onBack` (when on grid) | Fixed in `568af2d` |
| InnovationZone.tsx:627 | `nav.goBack()` | ToolErrorBoundary back, fixed in `568af2d` |
| ModuleLayout.tsx:184,280 | `onBack()` prop → traced to AppRouter `handleBackToCategory` → `nav.goBack()` | All 43 modules |
| Library.tsx:460 | `onBack()` prop → `handleBackToTree` → `nav.goBack()` | Library back |
| DashboardView.tsx:73 | `onBack()` prop → `nav.goBack()` | Dashboard back |
| LearningPathsView.tsx:57 | `onBack()` prop → `nav.goBack()` | Learning paths back |
| InsightsView.tsx:81 | `onBack()` prop → `nav.goBack()` | Insights back |
| TrainingHub.tsx:136 | `onBack()` prop → `nav.goBack()` | Training hub back |
| JourneyView.tsx:249 | `onBack()` prop → `nav.goBack()` | Journey back (root level) |

### CORRECT — local state, no history interaction (modals, wizards)

These use `setState(false/null)` to dismiss, but they NEVER pushed a history entry when opening, so there's nothing to pop. This is correct behavior.

| File:Line | Handler | Notes |
|-----------|---------|-------|
| Onboarding.tsx:157,942 | `setStep(s => Math.max(1, s-1))` | Onboarding wizard steps — local state |
| SubjectOnboarding.tsx:113,553 | `setStep(s => Math.max(1, s-1))` | Subject onboarding steps — local state |
| NorthStarOnboarding.tsx:80-82 | `setSubStep(s => Math.max(1, s-1))` | North star sub-steps — local state |
| SettingsModal.tsx | `onClose()` → `setSettingsOpen(false)` | Modal — never pushed history |
| StudyPassportModal.tsx:78 | `onClose()` → `setPassportOpen(false)` | Modal |
| NorthStarEditModal.tsx | `onClose()` → `setNorthStarEditOpen(false)` | Modal |
| ChangeSubjectsModal.tsx | `onClose()` → `setChangeSubjectsOpen(false)` | Modal |
| RankUpModal.tsx | `onClose()` → `setRankUpModal(null)` | Modal |
| StreakCelebration.tsx | `onDismiss()` → `setStreakCelebration(null)` | Modal |
| InnovationZone.tsx:644 | `setShowOnboarding(false)` | Subject onboarding modal — local state |
| InnovationZone.tsx:654 | `setShowJournal(false)` | Journal modal — local state |
| InnovationZone.tsx:661 | `setShowRewardShop(false)` | Shop modal — local state |
| ReflectionModal.tsx | `onCancel()` → local state | Modal |
| StudyJournalModal.tsx:99 | `onClose()` → local state | Modal |
| RewardShopModal.tsx | `onClose()` → local state | Modal |

### NEEDS REVIEW — local state sub-views that might benefit from history

These use local state for sub-view navigation within a component. They work correctly (no ping-pong) but browser-back doesn't navigate within them — the user has to use the in-app button. Low priority, not bugs.

| File:Line | Handler | Notes |
|-----------|---------|-------|
| JourneyView.tsx:146,149 | `setPeerViewMode('peer-list'/'own')` | Peer island sub-views — local state, no history entry |
| JourneyView.tsx:317 | `setPeerViewMode('peer-list')` | Back from individual peer island |
| JourneyView.tsx:426 | `setSheetOpen(false)` | Island shop drawer |
| JourneyView.tsx:563 | `setPeerViewMode('own')` | Close peer islands list |
| JourneyView.tsx:581 | `setFlareSystemOpen(false)` | Close flare system |
| FutureFinder.tsx:411-413 | `onBack()` → parent setState | Multi-step flow within IZ tool |

---

## Bugs found: 0

After distinguishing history-backed navigation (NavigationContext) from local-state sub-views, **no remaining round-trip bugs were found.** The IZ tool back button was the only case where a NavigationContext-managed field (`activeTool`) was cleared via dispatch (pushing) instead of `goBack()` (popping). That was fixed in `568af2d`.

All other sub-view dismissals use local `useState` which never interacts with the browser history stack.

## Future risk

If any new state is migrated into NavigationContext (like `activeTool` was), the same bug pattern could reappear. The rule: **any state in NavigationContext that creates a history entry when set must use `nav.goBack()` when cleared, not `dispatch(SET_X_TO_NULL)`.**
