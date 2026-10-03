# Mobile release reconciliation — 3 October 2026

Candidate: iOS 1.0.6, build 11. Upload and submission are pending App Store Connect verification.

The candidate includes main through 4859336b, including account/school registration,
Signature cards, restored onboarding/learning/Progress/Planner/Study/Paper Trail,
filled dark artwork, loading artwork and shared navigation. It adds the verified
iPhone status-bar correction described in iphone-status-bar-2026-10-03.md.

The approved 27–28 September Hosting-only UI missing from main is also restored:
Home Field notes and module cards; Focus-card Future Finder with saved answers,
bookmarks, comparisons and course details; canonical Mark Bank subject index and
compact/full-screen practice retaining draft and marking state. The source and
approval evidence are docs/session-release-2026-09-28.md and
approved-kobra-live-release-2026-09-27.md in the private Filled-Dark-Artwork checkout.
The recommendation engine, scheduler, review storage, current card IDs/content,
curriculum registry and preservation baseline are retained.

Only the approved UI is extracted from that mixed workspace. Subsequent unverified
Biology/Chemistry/Geography corpus and scoring changes, unfinished Topic Connections,
and unselected design proposals are excluded. Every published card remains
reachable through the canonical index, including archived specifications/aliases.

Editable purchased controls remain private. Only the compiled runtime, declarations
and scoped CSS are committed. Progress is added to the existing runtime exports.

Local verification: app/test TypeScript, lint, production build and whitespace checks
pass. The full 290-file suite passed 6,019 tests with one outdated Future Finder
landing assertion; the corrected four-test landing suite passes. All seven other
targeted suites pass (94 tests), including full-deck reachability, draft preservation
and saved Future Finder answers. Required card-preservation, curriculum and deck
suites pass within the full run. Three existing tests are skipped.

Fresh browser checks use the isolated local demo account. Home, Mark Bank and
Future Finder render at phone width with no page overflow or JavaScript errors.
Practice retains its draft and reveal state when expanding/contracting. An expanded
practice heading measures 84px top padding with a 62px native safe area. Screenshot
and check evidence is local in output/mobile-release/. The existing clean native
simulator checks verify the transparent status bar in both appearances.
