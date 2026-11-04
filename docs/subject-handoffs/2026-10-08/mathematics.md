# Mathematics handoff — 2026-10-08

**Paused by Alex; incomplete. Preserve all edits. No push, merge or deployment.** No subagents used.

## Workspace and exact cursor

- Worktree: `/Users/alexlinehan/Documents/Nextstepuni-Mathematics-Completion-20261007`
- Branch: `codex/mathematics-corpus-completion-20261007`
- HEAD: `49ff5053e9c785f9e538e9dd39050ef4fac6682f` (2014 Foundation Paper 1 complete), base `8deb273f`.
- Main `/Users/alexlinehan/Documents/Nextstepuni-Launch-` belongs to other subject/coordinating work; do not edit it from this task.
- **Validated but uncommitted:** 2014 Foundation English (`ev`) Paper 2, Project Maths Phase 3, `LC003BLP230EV.pdf`, scheme `LC003BLP000EV.pdf`; all Q1–7, Q8A and Q8B, Q9–10. 48 tasks, 325 offered/300 candidate marks. Generation, tests, typecheck and production build passed. `verification.json` has not yet been updated for this batch.
- **Research cursor:** 2013 Foundation English Paper 1, indexed “Paper One”, printed Project Maths Phase 2, `LC003BLP100EV.pdf`, scheme `LC003BLP000EV.pdf`. All 16 question PDF pages visually read; only scheme PDF pages **1–16** visually read, ending at Q9(a–e) model answers. Resume **scheme PDF 17, Q9(f)**, then Q10 and credit notes. No 2013 authored/review records written. Other 2013 booklets rendered but not visually inspected.

## Scope and evidence

Current Mathematics: **1,385 runtime cards** (403 HL, 436 OL, 546 FL), 1,398 authored, 13 historical authored rejects. Original 833 runtime IDs retained. Independent review: **18/111 English papers, 714 tasks**; inventory 222 physical editions, 2010–2026 including Irish. No Irish edition has a completed independent review. Counts do not establish completion.

Reviewed English: all five 2025 papers (HL P1 42/P2 43, OL P1 41/P2 42, FL 42); FL 2026 42, 2024 38, 2023 35, 2022 53, 2021 48, 2020 34, 2019 34, 2018 28, 2017 34, 2016 39, 2015 35, 2014 P1 36/P2 48. Foundation 2014–2026 reviewed. Remaining **93 English papers**, Irish equivalence/provenance, old rejects and final corpus/browser validation unfinished. Older HL/OL cards are not certified just because they exist. Some 2025 HL plaintext still relies on original crops.

Earlier implementation: original question/scheme reader; exclusive published-scale scoring plus full-credit-minus-one; calibrated PDF ruler; Foundation level/profile support; exact indexed question/scheme binding; standard/Project booklet separation; reviewed Atlas mapping. Atlas has **186 reviewed question placements**. 2014 P2 Q8 uses the existing verified combined Q8 sidecar containing both alternatives; Mark Bank keeps all seven 8A/8B tasks distinct.

## Changed files and authoritative ledgers

Uncommitted tracked files:

- `components/MarkBank/cards/maths/foundation.ts`, `components/MarkBank/cards/sizes.json`
- `data/examTopics/mathematics-reviewed-question-runtime.json`
- `scripts/markbank/authored/maths.json`
- `scripts/markbank/mathematics/audit.json`, `audit.py`, `build-reviewed-topics.mjs`
- `test/markBankCardPreservation.test.ts`, `test/markBankProfileDefaults.test.ts`, `test/mathematicsCorpus.test.ts`

Untracked: `scripts/markbank/mathematics/reviews/2014-foundation-p2-project.json`, `public/papers/`, `tmp/mathematics-ui/`, `tmp/pdfs/mathematics-review/`, this handoff. Preserve all.

Authority: SEC originals `paper-trail-corpus/{exampapers,markingschemes}/YEAR/`; exact inventory pairs `paperTrailData.ts`; independent review ledgers `scripts/markbank/mathematics/reviews/*.json`; extracts `examiner-reports/maths/schemes/`; reconciliation `scripts/markbank/mathematics/audit.json`; canonical curriculum `curriculumRegistry.ts`; Atlas taxonomy `data/examTopics/mathematics-runtime.json`.

**`verification.json` is stale at P1**: 1,337 runtime, 666 reviewed, 188 tests, old production-build status. P2 logs and this handoff supersede those current totals, not historical evidence. P2 stable-ID SHA256: `b5f19ce07aa145ca181cc69d57b907a63d13f6b3f39938fef673ed351fc9ed2f`.

## Workflow and invariants

Read worktree `AGENTS.md`, brand `/Users/alexlinehan/Documents/Nextstepuni-Module-Brand-Review-20261005/AGENTS.md`, and PDF skill. Visually sweep every question page and corresponding scheme section independently. Record hashes, inspected PDF positions, printed parts, exact bands, all source dependencies, canonical/Atlas topic IDs and raw selection decisions. Parser counts cannot certify completion. Split only at independently practicable published mark boundaries; retain all prompts under shared scales. Mechanically expand finite prompt choices, distinguish random events/answer options/open examples/methods. Preserve IDs; topic corrections are metadata-only.

Use actual indexed question/scheme pairs, not year/level alone. 2013 indexed standard files are printed Phase 2; 130/230 are Phase 3. Historical tasks map into existing registry nodes without claiming a later specification applied. Algebra: `maths-4-1` Expressions, `4-2` Equations, `4-3` Inequalities. Foundation Atlas has no indices topic: use number-systems for numeric indices, algebra for algebraic indices.

2014 P2 bands differ from P1: 5C=[0,2,4,5], 5D=[0,2,3,4,5], 10C=[0,5,7,10], 10D=[0,3,5,8,10]. Scheme PDF 47 incorrectly says Paper 1; surrounding content/summary 48 establish Paper 2. Q2(b)(ii–iv) shares 5C; Q3 median/mode shares 5C. `atlasQuestionNumber: "8"` explicitly retains the real parent anchor; do not invent dead 8A/8B jumps. Audit totals now preserve letter suffixes.

2013 P1 Q9(c), paper PDF 12, asks to test the expression using **one row of a five-row table** (posts 2–6): finite internal route candidate, inspect its marking boundary before deriving five variants. The raw scanner misses “one row”, pick/select and some “Answer six” wording; manual review remains mandatory. No 2013 scale census finished.

## Commands and last checks

All commands from the worktree; listed for resumption, not rerun at handoff:

```sh
node scripts/markbank/build-deck.mjs scripts/markbank/authored/maths.json
node scripts/markbank/mathematics/build-reviewed-topics.mjs
node scripts/markbank/mathematics/build-reviewed-topics.mjs --check
python3 scripts/markbank/mathematics/audit.py --check-reviewed
python3 scripts/markbank/mathematics/audit.py
npm test -- test/mathematicsCorpus.test.ts test/markBankCardPreservation.test.ts test/curriculumRegistry.test.ts test/markBankDeck.test.ts test/examTopicRegistry.test.ts test/markBankProfileDefaults.test.ts --maxWorkers=1
npm run typecheck
npm run build
git diff --check
```

P2 deck generation passed, 186 Atlas placements generated. Six files **193/193 tests passed**, typecheck and whitespace passed. Logs `/private/tmp/mathematics-2014-p2-{build,tests,typecheck}.log`. Already-running production build **finished successfully in 2m20s**, including service worker; only large-chunk advisory. Log `/private/tmp/mathematics-2014-production-build.log`. Its old exec session 93503 no longer exists at handoff; successful complete log is retained. Render session 93229 finished earlier. No own preview was running (5246 stopped previously); do not stop other subjects' processes.

Last browser command: `node /private/tmp/mathematics-reader-qa.mjs` (Playwright Chrome; current script targets 2020 FL map). Preview command: `npm run dev -- --host 127.0.0.1 --port 5246 --strictPort`. Harness `tmp/mathematics-ui/` supports `?session=1&card=<id>`. Requires local PDF symlinks and Vite fs allowance for symlinked dependencies; original config restored, backup `/private/tmp/mathematics-vite-config-original.ts`. Prior QA passed desktop 1440×1000/mobile 390×844: originals, zoom, close, Escape/focus, hidden scheme before reveal, exclusive 7/15 scale, zero errors; 8cm ruler measured 7.97–7.99cm at 100/125%. **No new 2014 browser pass.** Earlier backup `/private/tmp/mathematics-reader-qa-2026.mjs`.

Known full-audit failures: seven missing Irish scheme pairings (2020 FL `LC003BLP000IV.pdf`, six 2014 HL/OL/FL Project P1/P2 IV entries). All English sources available. Full audit remains incomplete and reports these; build exit 0 does not certify full reconciliation. Exact 13 rejected IDs in `audit.json`: 2021 OL P1 Q2b/P2 Q5bii; 2022 HL P2 Q2a; 2023 HL P1 Q2b/Q8bi/Q8di, P2 Q1b, OL P1 Q2aiv/P2 Q7c; 2024 HL P1 Q9bi, OL P1 Q2c/Q3a/Q10biv. P2 initial quote failure (“Identifies a triangle from diagram”) was fixed in review/authored, then regeneration passed.

## Next three actions after explicit resume

1. Preserve/integrate validated uncommitted 2014 P2 through the coordinator. Update `verification.json` from existing logs: 1,385 runtime, 714 reviewed, 193 tests, production build passed. Preserve IDs and review dates.
2. Resume **2013 FL EV Phase 2 P1 scheme PDF 17, Q9(f)**; finish scheme sweep, then author published units and Q9(c) finite routes. Inspect old-syllabus Q10 marking model before assuming scales.
3. Reconcile that paper and run appropriate targeted checks; continue outstanding exact booklets/Irish provenance and 13 rejects, then final browser/full-corpus validation. Do not claim whole-subject completion prematurely.

## Important local artifacts

`paper-trail-corpus` and `node_modules` are symlinks into the main environment. Preserve targets or recreate links. 2013 rendered sheets: `tmp/pdfs/mathematics-review/2013-foundation-{p1-standard,p1-project,p2-standard,p2-project,scheme-standard,scheme-project}-NN-NN.jpg`; only Phase 2 P1 paper 1–16 and scheme 1–16 visually read. Extracts `/private/tmp/2013-foundation-*.txt`; 2014 sheets/extracts retained too. `/private/tmp/write-2014-foundation-p1.py`, `...-p2.py` and earlier `write-*-foundation.py` are append-once historical helpers: **do not rerun**; subsequent quote fixes live in repository JSON and may not be reflected in scripts. Browser harness/PDF symlinks and tmp logs should be included in full snapshot where practical. No research or feature changes made after Alex's stop instruction.
