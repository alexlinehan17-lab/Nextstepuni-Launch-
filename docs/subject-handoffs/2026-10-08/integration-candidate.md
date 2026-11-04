# Combined integration checkpoint — deliberately unpublished

The four locally complete subjects (Accounting, Applied Mathematics, PE, Politics and Society) were combined onto main `4c53706d75931fc45158866aa805446a2ab4b059` in a separate worktree. This candidate is **not validated for publication**. Alex chose to save every checkpoint on main and integrate only validated work; the credit-conservation pause therefore includes this integration attempt. No runtime changes from it are activated by the preservation PR.

## Exact saved state

- Commit: `b85e4efa320fbcdd0d0249eb95af0142ec8c0f92`.
- Original worktree: `/Users/alexlinehan/Documents/Nextstepuni-Subject-Checkpoint-20261008`.
- Branch: `codex/subject-checkpoints-20261008`.
- Four commits: Politics `c53abf2aa8ef119619d0ea9b46546e1f102d132e`; PE `c2f80a1969d83c4dc253700398dcb973a12589d9`; Applied Maths `3925afb352a737629cf5fe1a311d4a79ab64d709`; Accounting/shared integration `b85e4efa320fbcdd0d0249eb95af0142ec8c0f92`.
- `integration-candidate.bundle` contains the exact implementation and its four commits. `integration-candidate.json` pins its tree, prerequisite and hashes.
- `integration-browser-evidence.tar.gz` preserves the copied browser harnesses and screenshots for all four subjects. `integration-evidence/` preserves successful check logs and the final full-suite failure output.
- The temporary preview on port 5488 was stopped. No integration job should restart automatically. Original subject worktrees are unchanged apart from their authored handoff notes.

## Checks that passed

App TypeScript, test TypeScript and lint passed. Lint ran before copying temporary browser harnesses; the harnesses are QA-only and must stay out of the app commit. The production build passed after excluding lazy subject factories/review manifests and Atlas registries from service-worker precaching; the existing app-chunks runtime cache still caches them on use. No cache-size ceiling was raised.

The required preservation/curriculum/deck checks and affected subject tests passed in targeted runs (632 tests across the original run plus the corrected coverage rerun). The combined preserved deck count is 23,539: 19,328 prior cards plus Politics 1,086, PE 652 additional cards, Applied Maths 1,103 additional cards, and Accounting 1,370. Existing identities were checked before updating the deliberate expansion baseline.

Accounting's independent source reconciliation passed 18,624 checks across 68 editions and 1,370 tasks with zero open/orphan items. Its central coverage adapter and baseline were added without rewriting other subject baselines. PE's original factory bytes were retained because the content hash pins those bytes.

Browser checks passed against published PDFs: Accounting's 2010 Ordinary Q2 sideways tables and 2025 Higher Q8(f) graphs on desktop/phone/phone Atlas, including 300% zoom, pan, Escape and focus return; Applied Maths Mark Bank desktop/phone plus eight Atlas cases including Irish/fallback schemes; PE Atlas/Mark Bank, source rotation, passage, finite route and dark phone layouts; Politics full-app demo, question/scheme readers, phone Atlas, 286 route options, pagination to 40 and six-criterion 100/100 essay scoring. The initial local-PDF override pointed to a nonexistent mirror; it was removed and all final checks used published source URLs.

## Full-suite result and next work

`npm test` completed with **6,385 passed and 39 failed, in five files**. The failures must be resolved or reviewed before publication; do not disable tests or bump baselines simply to turn them green.

1. `test/appliedMathematicsExamTopics.test.ts`: two expectations still name 38 browse topics/20 Higher labels. The new reviewed registry adds Higher Dimensional Analysis (39 total). Confirm its canonical specification mapping and reviewed source evidence, then update the explicit expected menu deliberately.
2. `test/paperTrailAnswers.test.ts`: 34 failures, one per new Accounting hosted map. The old global shape test assumes every `n` is a numeric printed question; Accounting preserves parents 1–9 and appends independently reviewed task/route keys such as `1(a)`. Determine and enforce the extended sidecar contract: unique IDs, valid retained parents, explicit paper/scheme regions and practice-task metadata. Do not relax numeric/print-order checks for ordinary parent anchors or infer adjacent crops from overlapping task anchors.
3. `test/studyclixQuestionParity.test.ts`: one test reports 35 missing historical browse associations (21 Applied Maths, 14 PE). Applied Maths' reviewed question block in `data/examTopics/registry.ts` replaces earlier coarser associations; PE's `browseTopicIdsForQuestion` returns task tags for identities also used by unsplit parent questions. Decide from reviewed SEC evidence whether each old association should be retained as a parent browse association or explicitly corrected with evidence. Keep precise task tags, all card IDs and valid student progress. Do not blindly union incorrect tags, remove reference checks, or use commercial classifications as the authority over the SEC/canonical specification.
4. `test/vaultTopics.test.ts`: one generic expectation assumes a runtime paper has exactly the original nine rows. Accounting now retains those and adds reviewed tasks (51 in that fixture). Verify every original row survives, then assert preservation plus legitimate supplementation.
5. `test/musicExamTopics.test.ts`: one 30-second timeout in the existing 29 recovered-scheme-map reproduction test during the concurrent full run. No Music code was changed. Rerun this test in isolation to distinguish resource contention from an actual failure; do not raise its timeout without evidence.

After those decisions, rerun the changed tests plus mandatory preservation tests, app/test typechecks, lint and build. Rerun the full suite once the failures are resolved. Shared-reader changes require desktop/phone regression checks. CI must pass on current main before merging. Main automatically deploys after its own successful checks; do not claim the candidate live until verified.

## Restore without touching another checkout

From a full clone containing the preservation commit:

```sh
cd docs/subject-handoffs/2026-10-08
shasum -a 256 -c integration-candidate.sha256
cd ../../..
git bundle verify docs/subject-handoffs/2026-10-08/integration-candidate.bundle
git fetch docs/subject-handoffs/2026-10-08/integration-candidate.bundle refs/heads/codex/subject-checkpoints-20261008:refs/checkpoints/integration-20261008
git worktree add -b resume/subject-integration-20261008 ../nextstepuni-subject-integration refs/checkpoints/integration-20261008
```

Use a new directory/branch name if either already exists. Compare `git rev-parse HEAD HEAD^{tree}` with `integration-candidate.json`. Install dependencies using the candidate's lockfile. On Alex's Mac the worktree uses the existing Kobra worktree's dependency directory and the primary Launch worktree's shared `paper-trail-corpus`; these symlinks are not portable dependencies. All original subject notes remain available in the preservation checkout. Extract browser evidence only into the new worktree, adapt hard-coded Mac paths and ports, and keep scratch files out of lint/commits. Use ordinary published PDF URLs; do not set `VITE_PAPER_TRAIL_LOCAL` unless a real corpus mirror server is running.
