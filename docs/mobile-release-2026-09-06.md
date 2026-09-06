# Mobile/tablet release — 6 September 2026

## Scope

User approved the refined mobile/tablet screens and requested publication, then removed the extra Home shortcut strip and Launchpad's Recently opened list. Both are absent. Tool history is no longer collected for that removed list; the single resume destination remains. Normal navigation remains available, including the tablet sidebar, and first-use guidance points to the navigation instead of the removed strip.

This release was isolated from the dirty preview workspace onto production commit `01d54ffa`. No uncommitted curriculum, question-corpus or Mark Bank work from the preview workspace is included.

## Desktop and Study protection

`KnowledgeTree.desktop.tsx`, `Onboarding.desktop.tsx` and `ResumeCard.desktop.tsx` preserve the current production implementations, not the older preview baseline. Home's resume import points to the preserved desktop copy. Shared account changes retain production's school sign-in and registration behavior. The redesign is gated to mobile/tablet devices, not desktop window width.

Production had acquired separate Study changes while the preview was being developed. `StudySessionView.mobile.tsx` therefore preserves the exact approved setup/countdown/completion/reflection implementation, while `StudySessionView.tsx` dispatches by device and keeps the current production desktop implementation intact.

Approved mobile Study SHA-256:

```
e482dec1eea01996817f373515a70680e30646278ef293d76a95286416bb36af  components/study/StudySessionView.mobile.tsx
5de10fce9fe7de1e7e8c845489a2e21312d1ad620a63461394ebc520ff89d925  hooks/useStudySession.ts
```

## Native release preparation

- Prepared version: 1.0.4, build 7. Confirm against App Store Connect before upload.
- Bundle: `com.nextstepuni.app`; signing team: `LHTS3Y4JLJ`.
- iPhone and iPad device families. iPad supports all four orientations; iPhone retains portrait configuration.
- The orange app icon is preserved from the existing 1.0.3 (6) archive source.
- Run a fresh production build and Capacitor iOS sync before archiving. The figure-pruning script removes only the hosted corpus's generated native copy, not source content.
- Additional iPad store screenshots and App Store Connect sign-in may be required. Do not claim uploaded, submitted, approved or live until each is confirmed separately.

## Verification and publication

Preview branch: the previous 116-test mobile regression run passed. The latest section removals passed 22 focused tests before integration.

Clean production integration checks completed:

- Full repository lint: passed, zero warnings.
- App and test TypeScript checks: both passed.
- 87 tests across 15 files: passed, including both desktop and mobile Study exit/setup behavior, onboarding, account entry, Home handoffs, module navigation and Launchpad guides.
- Desktop Home/onboarding/resume source comparisons against production `01d54ffa`: passed.
- Approved mobile Study and shared session hook checksums: matched.

6 September release continuation:

- Production build passed. Native assets were synced from that build; only generated exam-figure copies were pruned (source and hosted figures remain intact).
- Browser checks: phone Launchpad and iPad Home have no horizontal overflow or broken images. The collapsed iPad sidebar had 42.5px-wide targets; a mobile-only minimum width fixes these to at least 44px. Both checked screens now report zero undersized targets.
- The approved mobile Study setup, running countdown, pause/resume and exit confirmation were exercised with the local demo account; the test start was discarded without saving.
- iPad simulator build and native launch passed. Initial signed archive passed with version 1.0.4 (7) and device families `[1, 2]`; the final archive includes the touch-target correction.
- GitHub release PR: https://github.com/alexlinehan17-lab/Nextstepuni-Launch-/pull/90. Required checks and production deployment are still pending.
- App Store Connect confirmed 1.0.3 (6) is Ready for Distribution. The 1.0.4 draft was created and release notes saved, retaining automatic release after approval and the existing rating.
- iPad screenshots are required for this newly supported device family. App-review sign-in in the simulator has been requested for an accurate Home capture. No build has yet been uploaded or submitted for review.

Build, signing, upload and publishing are verified separately below as each finishes.

Publication is not complete merely because an archive builds. GitHub/Firebase deployment, Apple upload/processing and App Review are separate statuses.
