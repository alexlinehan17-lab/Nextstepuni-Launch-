# Physical Education handoff — 2026-10-08

## Checkpoint and stop state

- Worktree: `/Users/alexlinehan/Documents/Nextstepuni-Physical-Education-Completion-20261007`
- Branch: `codex/physical-education-bank-atlas-20261007`
- HEAD/base: `796355d45a172c36212c44e7fc022edc5d79bbee`
- All subject edits are uncommitted. No push, merge or deployment performed. Preserve modified AND untracked files.
- Goal was already **complete** on October 7 and remains complete. This turn only records the checkpoint; no new paper, feature work or test suite was started.
- No command from the subject work remains running. October 8 process inspection found no `pe-review`, port `5337`, or Physical-Education-Completion process (only the inspection command itself); no preview needed stopping. Old dev session was 74116. Last typecheck session 98391 exited 0; browser session 89504 exited 0.
- Current paper/question: **none in progress**. Last authored sitting: **2026 Ordinary, English (`ev`), LC225GLP000EV.pdf**, completed through **Q18(c)(ii)**. Last browser source inspection: same sitting **Q13(d)(ii)**, original page 13 comparison figures, with case context page 10. Last validation was test-file typecheck, passed.

## Completed scope and limits

All 13 distinct English written-paper sittings present in the Paper Trail index were visually swept with their schemes: 2020 Higher only; 2021–2026 Higher and Ordinary. 524 paper pages and 536 scheme pages reviewed, including blank/project/performance/end matter to confirm scope. No 2020 Ordinary sitting exists in this corpus.

772 reviewed separately practicable tasks become **873 cards** after finite-route expansion: **443 Higher + 430 Ordinary**. Every card has a matching Topic Atlas task and canonical curriculum mapping. All **221 prior card IDs** survive (652 added). Independent generic raw-paper reconciliation: **741/741 asks covered, 0 exclusions, 0 open, 0 orphans, 0 unparsed, 0 census flags**. Parser ask count is a different unit from reviewed task/route count; it is supplemental evidence, not the completion proof.

Cards by sitting (base tasks → cards): 2020 HL 49→59; 2021 HL 56→58, OL 59→61; 2022 HL 61→78, OL 72→88; 2023 HL 54→54, OL 60→67; 2024 HL 56→56, OL 60→62; 2025 HL 60→90, OL 77→87; 2026 HL 46→48, OL 62→65.

Original passages, tables, figures and rotated charts open in a dismissible PDF reader; original marking schemes open only after reveal. Shared PE criteria/scoring UI is used by Bank and Atlas. Full-paper navigation resolves split/route identities to original parent question anchors. Score controls permit only published allocations.

**Not completed or claimed:** integration into the coordinating branch/main, conflict resolution with other subject work, commit/push/deployment. Irish (`iv`) editions remain original full papers in Paper Trail; they were not separately authored or visually reviewed for task-level Irish wording. Atlas uses one English task set for each sitting rather than counting translation duplicates. Coursework/project/performance submissions are not written-paper practice cards. Validation below applies to this worktree before integration.

## Authoritative files and invariants

- `scripts/markbank/authoring/pe_review_2020.py` and `pe_review_2021_hl.py` through `pe_review_2026_ol.py`: manually reviewed task boundaries, context, topics, allocations, allowed marks, mechanical route pools, exact raw directive scans, reasons for non-expansion, source anchors, page counts and per-question totals.
- `scripts/markbank/authoring/pe_complete.py`: source-bound generator. Asserts every corpus sitting reviewed, all old IDs retained, raw selection/pool scans unchanged, pool anchors present, tariffs/totals valid and parent answer-map anchors present.
- `scripts/markbank/authored/physical-education-reviewed-audit.json`: complete review ledger, PDF SHA-256 values, all reviewed pages, task/route inventory, retained IDs and selection rationale. Status complete is for the above scope.
- `components/MarkBank/cards/physical-education/reviewed.json`: generated Bank corpus. `higher.ts` / `ordinary.ts` are generated thin exports via `factory.ts`.
- `data/paperTrail/physicalEducationTasks.json`: generated Atlas task index; topic crosswalk remains `data/examTopics/physical-education-curriculum-crosswalk.json`.
- `scripts/markbank/coverage-baseline.json`: refreshed PE entry only after visual sweep, targeted tests, preservation and zero-open reconciliation. `scripts/markbank/authoring/exclusions/physical-education.json` is now `[]`; old rubric-only exclusions are carded.
- `scripts/markbank/authored/physical-education.json`: original legacy identity evidence; preserved unchanged. Do not regenerate old point cards over the reviewed corpus. `build-deck.mjs` explicitly routes PE generation through `pe_complete.py`.
- `test/markBankPhysicalEducation.test.tsx`: source/route/tariff/context/topic/Atlas/scoring/reader regressions; frozen hashes prove legacy IDs unchanged. Preservation and coverage tests pin final corpus.

Follow root `AGENTS.md` and `/Users/alexlinehan/Documents/Nextstepuni-Module-Brand-Review-20261005/AGENTS.md`: canonical curriculum via registry and exam year; stable specification/topic IDs; no silent card deletion; no emojis; clickable controls and strong selected states. SEC papers/schemes govern task content and marks. Use published independent mark boundaries. Expand finite choose-k pools mechanically; do not fan out compulsory headings, illustrative lists, flexible and/or, or open knowledge choices. Carry all source/context/constraints into every split route. Never replace independent visual review with counts or the same parser's census.

Source method: local original PDFs rendered with PyMuPDF/PIL into page contact sheets and extracted text; every paper and scheme page inspected visually, allocations and candidate task boundaries cross-checked, selection directives classified against raw source. PDF skill was used. Original PDF bytes remain the displayed visual authority.

## Exact commands and last evidence (run from this worktree)

Generation / raw reconciliation:

```sh
python3 scripts/markbank/authoring/pe_complete.py --write
node scripts/markbank/build-deck.mjs scripts/markbank/authored/physical-education.json
python3 scripts/markbank/authoring/reconcile.py physical-education --json tmp/pe-review/reconciliation.json --open
python3 scripts/markbank/authoring/reconcile.py physical-education --baseline check
```

Both generator entry points passed. Repeated build compared SHA-256 before/after for reviewed.json, higher.ts, ordinary.ts, audit JSON, Atlas JSON and sizes.json: all six byte-identical. Last reconciliation and baseline check passed with the zero-open figures above. Baseline write was deliberately executed once after proofs using `python3 scripts/markbank/authoring/reconcile.py physical-education --baseline write`; do not blindly refresh on integration.

Passed suites:

```sh
npm test -- --run test/markBankPhysicalEducation.test.tsx test/curriculumRegistry.test.ts test/markBankDeck.test.ts
npm test -- --run test/markBankCardPreservation.test.ts test/markBankCoverage.test.ts test/markBankPhysicalEducation.test.tsx test/paperTrailTopics.test.ts test/paperTrailNavigation.test.tsx test/paperTrailStudyLoop.smoke.test.tsx test/paperTrailViewerPreview.test.tsx test/markBankSession.test.tsx test/examTopicRegistry.test.ts test/subjectShowcase.test.ts
npm run typecheck
npm run typecheck:test
npm run build
node node_modules/eslint/bin/eslint.js components/MarkBank/PhysicalEducationRubricPanel.tsx components/MarkBank/physicalEducationScoring.ts components/PaperTrail/PhysicalEducationTaskCard.tsx components/PaperTrail/physicalEducationTasks.ts components/MarkBank/SourceMaterialReader.tsx components/PaperTrail/CropView.tsx
git diff --check
```

First suite: 3 files / 135 tests passed. Second: 10 files / 367 tests passed (PE overlaps; do not sum as unique tests). Both typechecks, focused lint and production build passed. Build emitted large-chunk warnings; no build failure. Build pre-step updated only PE showcase counts to 873/873. Complete current Bank preservation total: 19,980.

Browser (temporary harness using actual product components):

```sh
npm run dev -- --host 127.0.0.1 --port 5337 --config tmp/pe-review/vite.config.ts
node tmp/pe-review/browser.mjs
```

URL: `http://127.0.0.1:5337/tmp/pe-review/preview.html`. Browser script uses local Playwright core and Chrome for Testing paths recorded inside it. Run outside sandbox if Chrome launch requires it. Last browser result: `QA completed; errors []`; selected score computed background `rgb(237, 133, 71)` and aria-pressed true. Visually checked desktop/mobile, light/dark, original PDF and scheme reader, sideways chart, full cloze passage, constrained route and 2026 comparison figures. No mobile overflow after fixing only preview selector width.

Known failures, all resolved: initial preservation checks expected old 125/96 counts (updated only after proof); sandbox Chrome launch SIGABRT (escalated browser passed); preview harness select overflow (harness fixed, rerun passed); test-file typecheck missing Firebase backend packages (added ignored functions/node_modules symlink to installed exact firebase-admin 14.3.0 / firebase-functions 7.3.2, rerun exited 0). No known unresolved PE failure. CUA was unavailable; used Playwright. No new checks were run during this stop/handoff turn.

## Ignored/local artifacts to preserve

- `examiner-reports/physical-education/papers/YYYY-{hl,ol}-paper.pdf` and `schemes/YYYY-{hl,ol}.pdf`: all 13 source pairs; required by generator and reconciliation; hashes in audit.
- `tmp/pe-review/`: paper/scheme text extracts and contact-sheet JPGs (`YYYY-level-kind-01.jpg`, etc.); `reconciliation.json`; `preview.html`, `preview.tsx`, `vite.config.ts`, `browser.mjs`; screenshots including `source-rotated-chart.png`, `rubric-desktop.png`, `scheme-desktop.png`, `passage-mobile-dark.png`, `passage-source-mobile-dark.png`, `constrained-route-desktop-dark.png`, `2026-comparison-figures.png`, `bank-mobile-dark.png`. `browser-failure.png` is historical failure evidence, not final state. This directory is gitignored.
- `node_modules` symlink → `/Users/alexlinehan/Documents/Nextstepuni-Module-Brand-Live-20261006/node_modules`.
- `functions/node_modules` symlink → `/Users/alexlinehan/Documents/Nextstepuni-Launch-/functions/node_modules`.
- `paper-trail-corpus` symlink → `/Users/alexlinehan/Documents/Nextstepuni-Launch-/paper-trail-corpus`.
- Generated `dist/` from successful build is ignored and reproducible. Do not treat symlink destinations as owned by this worktree or modify other subject work.

## Next 3 concrete actions (coordinator, not performed here)

1. Preserve the complete dirty worktree including all untracked reviewed modules/JSON and the ignored original PDFs + `tmp/pe-review/` evidence; retain symlink targets or install equivalent dependencies.
2. Integrate PE into the coordinating branch, resolving shared-file overlaps carefully in SessionScreen, SourceMaterialReader/CropView, PaperTrail topics/navigation, rubric types, generator/reconciler, sizes/showcase and preservation/coverage baselines. Preserve other subjects' changes and recompute combined totals deliberately.
3. On the integrated result, run the listed generation/reconciliation and required targeted checks, then browser QA; compare all 873 Bank/Atlas IDs and retained 221 legacy IDs before accepting integration. Publishing is coordinator-controlled; no further subject research is pending in the reviewed English scope.

## Exact changed-file inventory at handoff

The following was captured before adding this handoff itself; `??` files are essential untracked source, not disposable output.

```text
 M .gitignore
 M components/MarkBank/SessionScreen.tsx
 M components/MarkBank/SourceMaterialReader.tsx
 M components/MarkBank/cards/physical-education/higher.ts
 M components/MarkBank/cards/physical-education/ordinary.ts
 M components/MarkBank/cards/sizes.json
 M components/PaperTrail/CropView.tsx
 M components/PaperTrail/ReviseByTopic.tsx
 M components/PaperTrail/VaultQuestionCard.tsx
 M components/PaperTrail/index.tsx
 M components/PaperTrail/topics.ts
 M components/landing/subjectShowcase.json
 M scripts/markbank/authoring/exclusions/physical-education.json
 M scripts/markbank/authoring/reconcile.py
 M scripts/markbank/build-deck.mjs
 M scripts/markbank/coverage-baseline.json
 M test/markBankCardPreservation.test.ts
 M test/markBankCoverage.test.ts
 M types/markBank.ts
?? components/MarkBank/PhysicalEducationRubricPanel.tsx
?? components/MarkBank/cards/physical-education/factory.ts
?? components/MarkBank/cards/physical-education/reviewed.json
?? components/MarkBank/physical-education-rubric.css
?? components/MarkBank/physicalEducationScoring.ts
?? components/PaperTrail/PhysicalEducationTaskCard.tsx
?? components/PaperTrail/physical-education-tasks.css
?? components/PaperTrail/physicalEducationTasks.ts
?? data/paperTrail/physicalEducationTasks.json
?? scripts/markbank/authored/physical-education-reviewed-audit.json
?? scripts/markbank/authoring/pe_complete.py
?? scripts/markbank/authoring/pe_review_2020.py
?? scripts/markbank/authoring/pe_review_2021_hl.py
?? scripts/markbank/authoring/pe_review_2021_ol.py
?? scripts/markbank/authoring/pe_review_2022_hl.py
?? scripts/markbank/authoring/pe_review_2022_ol.py
?? scripts/markbank/authoring/pe_review_2023_hl.py
?? scripts/markbank/authoring/pe_review_2023_ol.py
?? scripts/markbank/authoring/pe_review_2024_hl.py
?? scripts/markbank/authoring/pe_review_2024_ol.py
?? scripts/markbank/authoring/pe_review_2025_hl.py
?? scripts/markbank/authoring/pe_review_2025_ol.py
?? scripts/markbank/authoring/pe_review_2026_hl.py
?? scripts/markbank/authoring/pe_review_2026_ol.py
?? test/markBankPhysicalEducation.test.tsx
```
