# Mobile and tablet screen rollout

## Scope boundary

The user explicitly limited this rollout to phones and tablets. **Desktop is off limits.** Do not apply these screen changes to desktop as a responsive redesign.

`hooks/useMobileAppDesign.ts` opts in native Capacitor apps, mobile/tablet browsers, and iPads using desktop-mode Safari (Mac platform with multi-touch). Window width alone never opts a desktop browser in. A Windows touchscreen laptop remains desktop. The local development review iframe can explicitly preview either experience; its override is disabled in production builds.

## Implemented, locally

- New mobile onboarding with account-scoped drafts, explicit levels/grades, deferred grades, editable review, count-up from confirmed current to target points, date confirmation, and the approved box-shaped study-day controls without ticks.
- Mobile Home with resume/browse actions, actual timetable blocks, and actual weekly session goals. Planned sessions open the existing Study setup.
- Single-tap module/world lists for phones and tablets, with existing brand artwork and module search.
- Mobile Launchpad task search, recent tools, readable cards and guide access.
- Mobile Progress controls, quieter panels, scope explanations and empty-state actions, retaining the existing five-mountain programme view and analytics.
- Mobile account entry and help, preserving the real authentication, registration, consent and recovery handlers.

## Desktop preservation

The original Home, resume card and onboarding implementations are retained in `KnowledgeTree.desktop.tsx`, `ResumeCard.desktop.tsx`, and `Onboarding.desktop.tsx`. Their source was checked against the pre-rollout version; the only necessary adjustment is Home importing the preserved resume card. Do not restyle these files in this rollout.

Shared account, Progress and Launchpad components branch on the device boundary: original desktop layout, copy and controls remain. Module desktop compositions remain unchanged. The initial desktop loader remains the original loader.

## Protected Study flow

No edits to the existing setup, countdown, pause/resume, completion or reflection implementation. The source checksums still match the pre-rollout baseline:

```
e482dec1eea01996817f373515a70680e30646278ef293d76a95286416bb36af  components/study/StudySessionView.tsx
5de10fce9fe7de1e7e8c845489a2e21312d1ad620a63461394ebc520ff89d925  hooks/useStudySession.ts
```

## Verification

- `npm run typecheck`: passed.
- The wider `npm run typecheck:test` also checks unrelated worktree tests. An existing error in `test/finalStudyclixExamTopics.test.ts:191` (`sourceUnavailable` is `unknown`) remains outside this rollout; that curriculum test was not edited. Unsupported query options in this rollout's tests were corrected, and the affected 42 runtime tests were rerun successfully.
- Focused lint on edited implementation and new tests: passed, zero warnings. Preserved legacy desktop files were not refactored for lint-only changes.
- 116 tests across 21 focused files: passed. Includes onboarding persistence/loading/mobile interaction, account recovery mocks, Home handoffs, native module selection and lesson navigation, Launchpad guidance, dashboard data/charts, Study exit/session behavior, device-scope regressions, mobile keyboard tabs and first-visit help.
- `npm run build`: passed. Existing large-chunk and mixed static/dynamic import warnings remain; no deployment performed.
- Browser checks used the actual app with a local Demo Account, not the static prototypes. Viewports included 320 × 568, 390 × 844, 768 × 1024, 844 × 390 and 1366 × 1024. The development device switch previews the mobile/tablet branch; it is not a physical-device test. Automated device tests also cover iPad desktop-mode Safari, Android/iPhone, native WebViews, narrow desktop windows and touchscreen Windows laptops.
- The browser review is `http://127.0.0.1:5173/mobile-review.html` while Vite is running. Use the local Demo Account, not real student records. The review HTML is not included in the production output.

## Follow-up mobile refinement and walkthrough

Issues found and fixed during the actual-app walkthrough:

- Grade Back/Next now moves through selected subjects in order. Selecting subjects no longer resets scroll or steals focus. Review Edit actions have full-sized touch targets.
- Rotation preserves in-progress answers. The local review device controls also preserve the running iframe when switching between phone/tablet sizes.
- Module lists have proper phone-side padding, a less crowded header and 44px navigation targets. Existing lesson content and progress are unchanged.
- Failed Home timetable loading has an explicit recovery state instead of an endless loader or a misleading rest day.
- The tablet/landscape Home sidebar can scroll to Settings and other lower actions.
- Tool guides and recommendations scroll inside short screens, reset their scroll position when the content changes, and expose touch-sized controls. Mobile tab bars support arrow keys, Home/End and reduced motion.
- Progress insight actions and short tab labels now have proper touch targets. First-visit captions are bounded to the viewport, and mobile help targets the visible profile action rather than a hidden sidebar button.

Walkthrough evidence:

| Area | Checked in the real local app |
| --- | --- |
| Account | Phone sign-in/registration entry and join-code help. No live account creation or recovery email sent; mocked tests cover those handlers. |
| Onboarding | Completed all seven stages, including subject levels, grades, date confirmation and boxed study days. Observed the points count-up to 256 from 200 for three confirmed subjects. Start Learning reached Home. Editing, cancelling and restoring answers worked. Grade edits survived phone landscape → tablet landscape → 320px; Cancel restored the original grade. |
| Home and modules | Correct rest-day and weekly-goal states; module/world lists; search found a real saved lesson and opened its saved section. Sidebar Settings opened in short landscape. |
| Launchpad | “past papers” found Paper Trail and Topic Atlas. Opened the real Paper Trail and confirmed it appeared in Recently opened. The guide selector jumped to Paper Trail. Both recommendation questions worked across portrait/landscape and the result opened the actual tool. |
| Progress | Overview, Study, Confidence, Practice and Milestones; subject and period filters; correct empty-state copy and retained all-subject scope where applicable. Tablet-landscape Milestones fitted without horizontal overflow. |
| Protected Study | Original setup → 45-minute revision session → coloured countdown → pause/resume → leave confirmation → Keep studying → discard without saving. Session counts remained unchanged. Existing reflection history opened. Completion/debrief behavior is covered by automated tests, not a completed browser session. |
| Existing destinations | Journey loaded; Settings opened and closed. These destinations were not redesigned. |
| Desktop | Browser confirmed the original onboarding and Home. Source comparisons confirmed the preserved desktop files still match the original versions. |

No horizontal overflow or broken images was observed in the reviewed new-screen states. The layout checker flags native checkbox inputs separately from their larger clickable labels; it is a diagnostic, not an accessibility certification. We did not exhaustively retest every existing Launchpad tool or lesson.

The local demo logged a permission-denied response for its onboarding analytics event. Onboarding still completed and entered Home; no Firebase permission rules were changed to allow demo telemetry.

## Still required before release

Test on physical iPhone/Android/iPad devices: native keyboards, safe areas/notches, app resume, gestures, reduced motion and the full completion/debrief path. A successful build and browser preview are not a physical-device sign-off. No deployment, native sync, publishing or real student-record writes were performed. Do not deploy or publish without approval.
