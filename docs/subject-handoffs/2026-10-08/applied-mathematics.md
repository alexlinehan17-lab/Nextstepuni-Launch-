# Applied Mathematics handoff — 2026-10-08

## Checkpoint and stop state

- Worktree: `/Users/alexlinehan/Documents/Nextstepuni-Applied-Mathematics-Completion-20261007`
- Branch: `codex/applied-mathematics-bank-atlas-20261007`
- HEAD: `812e0092f732bcfb20126d8f4534e21047d9b085` — Finalize Applied Mathematics corpus coverage and verification.
- Review base: `796355d4`. Earlier final checkpoints: `8d40a538` (2025 English), `1da3f3a8` (Irish through 2022), `f078738e` (Irish through 2026).
- Goal already **complete** before the stop instruction; leave it complete. No research, features, generation or tests started for this handoff.
- No active paper/task remains. Last browser case: **2026 Higher, Irish (`iv`), Q10, `LC020ALP000IV.pdf`**, paper PDF pages 38–40 and scheme pages 16–17, phone 390×844. Desktop 1440×1000 also passed.
- Own preview on port 5348 was stopped with Ctrl-C (session 26222, exit 130); browser session 17889 and production build session 35741 completed with exit 0. No command is awaiting completion. Other subjects' previews must not be stopped.
- Before this handoff, tracked tree was clean; only `tmp/applied-mathematics-review/` was untracked. Preserve it and ignored source PDFs. This handoff is intentionally uncommitted for the coordinating snapshot. No push, merge or deployment performed.

## Completed scope and limits

- All **33 English and 33 Irish indexed editions**, 2010–2026, reviewed against their schemes: **1,486 tasks (716 HL, 770 OL)**, with canonical curriculum/Topic Atlas mappings. This is the indexed Paper Trail corpus; **2020 Ordinary is not indexed**, so it is not claimed reviewed.
- Visual review covered 131 distinct PDFs: 66 papers and 65 schemes. **2011 Ordinary Irish uses the explicitly reviewed English scheme fallback**; no native Irish scheme is claimed.
- Irish editions introduce no additional distinct tasks; 2,972 edition/task links connect to the 1,486 canonical cards. Atlas has 318 logical printed questions, 636 language-specific question mappings; these counts are not independent evidence of completeness.
- All **383 original IDs and literal source blocks preserved**; audited runtime corrections carry original-block hashes. All 51 former drawing exclusions retired with provenance; represented by 60 separately priced cards.
- Reconciliation: 1,486/1,486 covered; zero open, orphan, unparsed, active/stale exclusions. Native crop sweep completed (240 pre-2023 regions); later booklets use reviewed full pages. 2013 OL Irish Q7 starts at y=.3975 on PDF page 4 to retain the ladder wall above the printed heading.
- No known unfinished subject authoring or validation at this HEAD. **Integration with other subject branches and validation of the combined application remain the coordinator's work.** Browser checks are representative integration cases, not a browser traversal of every card; exhaustive source review is recorded separately.

## Authoritative records and changed files

Paths below are relative to the worktree. Exact complete change inventory: `git diff --name-only 796355d4 HEAD`.

- Independent paper/scheme task ledgers: `scripts/markbank/authoring/reviewed/applied-maths/2010.json` through `2026.json`.
- Native translation ledgers: `scripts/markbank/authoring/translated/applied-maths/2010.json` through `2026.json`; crop/UI receipts: `scripts/markbank/authoring/translated/applied-maths-{crop,ui}-review.json`.
- Completion record: `scripts/markbank/applied-mathematics-review-status.json`. Exclusions: `scripts/markbank/authoring/exclusions/applied-maths.json` (`[]`) and `exclusions/resolved/applied-maths.json` (original reasons plus replacements).
- Generator/verification: `scripts/markbank/build-applied-reviewed.mjs`, `validate-applied-translation.py`, `build-deck.mjs`; `scripts/markbank/authoring/{applied_census.py,paper_census.py,reconcile.py,test_applied_reconcile.py}`; `scripts/markbank/coverage-baseline.json`.
- Runtime: `components/MarkBank/cards/applied-maths/{higher.ts,ordinary.ts,reviewed.ts,reviewed.json}`, `components/MarkBank/cards/sizes.json`, `types/markBank.ts`; `components/MarkBank/{AppliedMathematicsRubricPanel.tsx,SessionScreen.tsx,SourceMaterialReader.tsx,mark-bank-session-paper.css}`.
- Atlas/source routing: `data/examTopics/{applied-mathematics-archive-topics.json,applied-mathematics-reviewed-questions.json,registry.ts}`, `paperTrailData.ts`, `components/PaperTrail/vaultResolve.ts`; 66 hosted maps under `public/paper-answers/YYYY/LC020{A,G}LP000{EV,IV}.pdf.json` (only indexed combinations). Also `.gitignore` and `components/landing/subjectShowcase.json`.
- Tests changed: `test/{appliedMathematicsExamTopics.test.ts,appliedMathematicsTranslations.test.ts,markBankAppliedMathematics.test.tsx,markBankCardPreservation.test.ts,markBankCoverage.test.ts,paperTrailAnswers.test.ts,vaultAnchors.test.ts}`.

## Method and invariants

Read worktree `AGENTS.md` and `/Users/alexlinehan/Documents/Nextstepuni-Module-Brand-Review-20261005/AGENTS.md`. NCCA/Curriculum Online controls curriculum/year transitions; SEC paper and scheme control wording, diagrams and tariff. Visually sweep every paper and scheme, then check each independently practicable published mark boundary. Keep required steps/shared responses together; expand finite optional answer pools only. Raw selection directives must be classified. Generated counts/parser output are not independent proof.

Ledgers pin source SHA-256s, task context, scheme allocations, original corrections and canonical topic IDs. Compiler checks source identity, crop/text boundaries, selection directives, translation task/tariff correspondence and routing. Census reads independent visual ledgers, not the generated card manifest; exact IDs/refs prevent parent citations hiding missing splits. Baselines may move only after visual sweep, original preservation, zero-open/orphan reconciliation and targeted checks. Refresh crop-review ledger SHA only following actual re-review if native ledgers change. Preserve original IDs and question-map fields; do not regenerate blindly from old authoring helpers.

## Commands and last results

Run from the absolute worktree above. These are reproduction commands, **not instructions to rerun during the stop**. Use one heavy check and one preview/browser at a time.

```sh
node scripts/markbank/build-applied-reviewed.mjs
python3 scripts/markbank/authoring/reconcile.py applied-maths --open --baseline check --json tmp/applied-mathematics-review/reconciliation-final.json
python3 scripts/markbank/authoring/test_applied_reconcile.py
# Baseline was deliberately written only after required checks:
python3 scripts/markbank/authoring/reconcile.py applied-maths --baseline write
npx vitest run test/appliedMathematicsTranslations.test.ts test/markBankAppliedMathematics.test.tsx test/markBankCardPreservation.test.ts test/curriculumRegistry.test.ts test/markBankDeck.test.ts test/examTopicRegistry.test.ts test/vaultAnchors.test.ts test/paperTrailAnswers.test.ts test/vaultTopics.test.ts
npx vitest run test/vaultAnchors.test.ts
npx vitest run test/appliedMathematicsTranslations.test.ts
npx vitest run test/markBankCoverage.test.ts
npx vitest run test/subjectShowcase.test.ts
npm run typecheck
npm run typecheck:test
npm run build
git diff --check
```

- Compiler passed (`build-irish-final.log`); reconciliation passed (`reconciliation-final.json`); Python reconciliation tests: 3 passed.
- Nine-file regression initially: 3,734 passed, 1 failed because old hosted-map assertion expected 23 rather than 89. Fixed to preserve the 23 Art/Physics checks and independently validate all 66 Applied maps. Targeted rerun: **25 passed** (`vault-regression-final.log`). Eight unaffected files had passed. Combined distinct nine-file total after fix: 3,736.
- New exclusion test's TypeScript union access was fixed with card-kind and Applied-rubric narrowing. Translation rerun: **36 passed** (`translation-regression-final.log`); final test typecheck passed.
- Coverage: **157 passed**; showcase: **1 passed**. Aggregate 3,894 distinct JS tests across 11 files passed through the above runs/reruns; not a fresh all-repository suite. Both production and test typechecks passed.
- Build passed (Vite 22.81s, service worker generated), `build-final.log`; advisory large-chunk warning remains. Build updated only Applied showcase topic count 38→39. `git diff --check` passed. No unresolved known subject-specific test/build failure.

Browser commands (Chrome requires the existing outside-sandbox approval):

```sh
node tmp/applied-mathematics-review/dev.mjs
node tmp/applied-mathematics-review/browser.mjs atlas
node tmp/applied-mathematics-review/browser.mjs atlas phone
# Existing Mark Bank harness; default card/mark is a reviewed 2026 OL diagram:
node tmp/applied-mathematics-review/browser.mjs
# Parameter form: browser.mjs CARD_ID 'Published step 1' MARKS
```

Preview URL: `http://127.0.0.1:5348/tmp/applied-mathematics-review/atlas.html`; Mark Bank: `/tmp/applied-mathematics-review/preview.html?card=CARD_ID`. Native cases were 2011 OL Q1, 2013 OL Q7, 2026 OL Q8, 2026 HL Q10, each desktop/phone. Live PDFs, no network mocks; correct page counts/source callbacks and zero page errors/network failures/overflow in final cases. Initial sandbox Chrome launch failed; approved launch worked. Initial phone overflow came from preview-only diagnostic JSON; hiding that output fixed it. Desktop successes remain in `atlas-browser-final.log` (which also contains that superseded phone failure); all four phones passed in `atlas-browser-phone-final.log`. Checked-in UI receipt consolidates **all eight**; temporary `atlas-browser-results.json` contains the phone rerun only.

## Artifacts to preserve

- Entire untracked/partly ignored `tmp/applied-mathematics-review/`: source text, contact sheets, crop renders, `irish/`, `irish-crops/`, authoring helpers, browser scripts/HTML/TSX, screenshots and logs named above. Additional final logs: `typecheck-final.log`, `typecheck-test-final.log`, `coverage-regression-final.log`, `showcase-regression-final.log`, `final-regression.log`. Screenshots are SHA-pinned in the UI receipt.
- Ignored original PDFs: `examiner-reports/applied-maths/papers/YYYY-{hl,ol}-paper.pdf`, `schemes/YYYY-{hl,ol}.pdf`, `irish/YYYY-{hl,ol}-{paper,scheme}.pdf`. Required for compiler/census source validation; native 2011 OL scheme uses the English path.
- **Do not rerun `tmp/applied-mathematics-review/fetch-irish.mjs` blindly**: the former 2011 OL index fallback could overwrite the native paper with English bytes. Native PDF identity has already been corrected and checked.
- `dist/` is the successful local build, regenerable. Preserve raw sources/evidence first. Temporary scripts may contain earlier intermediate assumptions; final checked-in ledgers and compiler are authoritative.
- Easy-to-confuse corrected content: 2025 HL Q2(vi) is differential-equation v(t), while its graph is Q9(a)(ii); 2026 OL Q8(i) is M1/M2 populations, not diagrams.

## Next three actions (coordinator, after snapshot)

1. Preserve HEAD, this uncommitted handoff, all tmp evidence and ignored PDFs before moving/integrating the worktree.
2. Review/integrate the validated branch changes against the coordinating branch, reconciling shared baseline, taxonomy, source-routing, Mark Bank UI and showcase files without overwriting other subjects.
3. Once integration is authorized, run the necessary combined-state reconciliation, preservation/targeted tests, typechecks/build and source-reader smoke checks. Resume subject authoring only if integration exposes a specific evidenced gap; no new paper is queued.
