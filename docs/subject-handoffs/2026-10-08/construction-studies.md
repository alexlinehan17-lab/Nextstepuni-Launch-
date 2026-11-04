# Construction Studies handoff — 2026-10-08

## Stop state and exact checkpoint

- Worktree: `/Users/alexlinehan/Documents/Nextstepuni-Filled-Dark-Artwork-20260926`
- Branch: `codex/filled-dark-artwork-20260926`
- HEAD: `90efd9fcb9ee5da180e5bbbe8ebc7f0e3c6ff80f`
- Goal is **paused**, confirmed through goal tool. Stopped at Alex’s explicit credit-limit instruction. No push, merge, deploy, reset, new paper or new test suite performed for this handoff. Preserve all unrelated edits too.
- Exact checkpoint **589**: **2015 Ordinary Level, English (`ev`), main sitting, single Construction Studies theory paper `LC029GLP000EV.pdf`, Q1 drafted and validated, NOT integrated.** Next question is Q2.
- No owned preview started and no known owned running command remains. Prior runner session 17738 completed exit 0; reconciliation session 73724 completed exit 120 (open legacy coverage, described below). No browser QA performed for this subject batch; no browser command or preview shutdown is applicable.

## Completed versus unfinished

**2015 Higher English main theory only:** 102 source-reviewed cards across Q1–Q10 and the Q10 alternative, including 27 whole-question routes and 35 referenced source figures. Added to 505 preserved pre-existing Construction cards: runtime now **607 cards (357 Higher / 250 Ordinary)**, zero dropped, zero orphan/unparsed cards. Original question identities match Topic Atlas; Q10 alternatives share the original Q10 anchor. Final separate paper/tariff reconciliation passed; it was performed by the same operator, not independent human certification. Scoped legacy census: 27/27 printed asks, zero open for this Higher theory paper.

**2015 Ordinary:** all theory paper/model/tariff pages visually reviewed; intake and closed-choice ledger saved. Q1 has three draft tasks and two original source figures; source validation, 12 negative mutations, canonical IDs, claims, task groups and Atlas preflight passed. No Ordinary draft cards have been integrated. Q2–Q9 remain unauthored. Q8 requires all 126 choose-five-of-nine whole-question routes plus nine term cards. Practical components, Irish editions and remaining Construction years require their own full audits. Existing 2016–2025 cards are not certified complete. The all-subject goal remains substantially incomplete.

Q1 Ordinary invariants: part (a) 40 = best nine details ×4 + dimensions 4; (b) wall-plate strap 2; whole question 50 adds shared drawing quality 8 exactly once (`questionBonus`, allowed 0/4/6/8). Do not import Higher 3+1 tariffs or attach the shared eight to both parts. Original specifies 1:5, 30°, 2 m width, 400 mm wall / 200 mm cavity, 200×40 rafters and ceiling joists, insulation below ceiling joists, 400 mm below wall plate through ridge, three tile courses and four dimensions. Missing Atlas associations to add at integration: `construction-studies-ordinary-foundations-floors-walls`, `construction-studies-ordinary-heat-loss-insulation`.

## Authoritative evidence and workflow

Relative paths below are from the worktree. Audit root `D=docs/markbank-audit/2026-09-28`.

- Latest checkpoint: `D/construction-active-resume-2026-10-07.json`.
- Validated batch reports: `D/construction-first-validation.json`, `D/construction-q3-q6-validation.json`, `D/construction-q7-q10-validation.json`.
- Final Higher source audit: `D/construction-2015-higher-theory-final-source-audit.json`.
- Availability only, NOT completion proof: `D/construction-source-availability-2026-10-07.json` (127 local PDFs).
- Draft/source/check archives: `D/drafts/construction-2015-higher-*`, `D/drafts/construction-2015-ordinary-intake/`, `D/drafts/construction-2015-ordinary-q1-draft/`. Also see `D/CURRENT.md`.
- Runtime inputs: `scripts/markbank/authored/construction-studies.json`, `scripts/markbank/authored/construction-studies-2015-higher-reviewed.json`, `scripts/markbank/atlas-reviews/construction-studies-2015-higher.json`, `scripts/markbank/authored/construction-studies-census-repairs.json`.

Use original Paper Trail SEC papers and schemes first. Corpus: `/Users/alexlinehan/Documents/Nextstepuni-Launch-/paper-trail-corpus`. Render PDF pages/crops with PyMuPDF and visually compare printed questions, diagrams, model responses AND tariff tables. Pin hashes/pages/crops, enumerate all closed choices, preserve shared marks and all alternatives, verify source-grounded wording, canonical registry topics and exact Atlas paper/question identity. Never count inventory, placeholder cards or raw card totals as complete coverage. Preserve existing card IDs/content and preservation baseline. Source review and completion reconciliation are separate checks; both needed. No StudyClix/SimpleStudy substitution was needed.

Source files and SHA-256:

- `examiner-reports/construction-studies/papers/2015-hl-paper.pdf`: `08976c01caaf916102e5f9f0aa18a512a5bf6aa2cad2ce5320208a63970fdc13` (8 PDF pages; theory 1–5).
- `examiner-reports/construction-studies/2015-hl-marking-scheme.pdf`: `9558f06c3c50cb7c858d0b4fb299b437277c0efcd182e0811c6aff0bb7dab3ef` (48 pages; models 4–30, tariffs 32–42, practical separate 43–46).
- `examiner-reports/construction-studies/papers/2015-ol-paper.pdf`: `6a5e6c2c39fcfc5d7d3d4eebae139ed927eaaaa16fb429d0eab333c3f0d7e99f` (4 pages; theory 1–3).
- `examiner-reports/construction-studies/2015-ol-marking-scheme.pdf`: `ca21a4dccfd47aea12de99758ce82058a9b33138a0ab9742dba1197b47364e07` (32 pages; models 4–16, tariffs 17–25, practical separate 27–30).
- Byte-identical corpus counterparts: `exampapers/2015/LC029ALP000EV.pdf`, `markingschemes/2015/LC029ALP000EV.pdf` (Higher), corresponding `LC029GLP000EV.pdf` (Ordinary).

## Exact resume/check commands (recorded, NOT rerun for handoff)

Run from the worktree; mutation/integration scripts must be reviewed before any rerun.

```sh
python3 -m unittest discover -s scripts/markbank/authoring -p test_construction_2015_higher_q1_q2.py
python3 -m unittest discover -s scripts/markbank/authoring -p test_construction_census_repairs.py
python3 scripts/markbank/authoring/construction_2015_higher_q3_q6.py
python3 scripts/markbank/authoring/construction_2015_higher_q7_q10.py
node scripts/paper-trail/build-construction-studies-exam-topic-crosswalk.mjs
node scripts/markbank/build-library-topic-index.mjs
node scripts/markbank/build-deck.mjs scripts/markbank/authored/construction-studies.json
python3 scripts/markbank/authoring/reconcile.py construction-studies --json /tmp/construction586/legacy-reconciliation.json
NODE_OPTIONS=--max-old-space-size=8192 npx vitest run test/markBankConstruction2015HigherReviewed.test.ts test/constructionStudiesExamTopics.test.ts test/markBankCardPreservation.test.ts test/curriculumRegistry.test.ts test/markBankDeck.test.ts --maxWorkers=1 --testTimeout=600000
NODE_OPTIONS=--max-old-space-size=8192 npm run check:markbank-atlas -- --maxWorkers=1 --testTimeout=600000
node --max-old-space-size=12288 node_modules/typescript/lib/tsc.js --noEmit -p tsconfig.test.json
npx eslint test/markBankConstruction2015HigherReviewed.test.ts test/constructionStudiesExamTopics.test.ts test/markBankCardPreservation.test.ts test/fixtures/construction2015Reviewed.ts
# Ordinary Q1 scratch validation, already passed:
python3 /tmp/construction589-review.py
python3 /tmp/construction589-test.py
node /tmp/construction589-preflight.mjs
```

Last completed integration runner: `caffeinate -i python3 /tmp/construction586-run.py`; results `/tmp/construction586/checks.json` and per-phase logs, archived under `D/drafts/construction-2015-higher-q7-q10-integration/`.

## Last passed checks and known failures

- Latest Higher batch: **226 regression tests**, **274 Atlas tests**, Python source checks, deck generation **607 / zero dropped**, test TypeScript at 12 GB and targeted ESLint passed. Earlier Q1/Q2 batch also passed app typecheck at 12 GB and Vite build; no new full app build after Q3–Q10.
- Ordinary Q1: source validator and 12 negative mutation cases passed; preflight passed, with the two missing Atlas associations explicitly deferred until integration.
- Legacy reconciliation remains **exit 120**: 607 cards, 446/843 legacy asks, **397 OPEN**, zero orphans, zero unparsed, one census flag. The denominator includes 2010–2014 outside the active 2015–2026 scope; it is not an all-goal completion percentage.
- Resolved: 8 GB app typecheck OOM → 12 GB passed; TS union narrowing corrected. Q3–Q6 first generation dropped four cards due to duplicate figure hashes despite exit 0 → reused canonical `windows` figure, removed duplicate metadata, regenerated 568/zero dropped. The unused physical `windows-floor` PNG remains as provenance.
- Resolved: parser treated introductory Q3 A/B option numbering as question parts → source/hash-pinned census repair restored actual (a)/(b)/(c); 16 false orphans became zero. Three repair test methods passed, including drift rejection; preservation baseline unchanged.
- Resolved: Q9 whole task group exceeded five-row limit → grouped each selected junction separately plus part (b); preflight passed.
- Deck builder's inline ledger can lag because it runs before the new runtime write; final standalone reconciliation was run after generation.

## Next three actions — only after authorized resume

1. Author Ordinary Q2 from original paper page 2 and scheme pages 5/18: cavity insulation 20 + external insulation 20; part (b) two open advantages ×5 =10; whole 50. Validate source crops, tariffs, choices, registry and Atlas.
2. Continue Ordinary Q3–Q4; integrate validated Q1–Q4 as a batch, adding missing exact Atlas associations, preserving all 607 prior cards. Generate and reconcile, then run required checks sequentially; no preservation baseline reset.
3. Finish Ordinary Q5–Q9, including all 126 Q8 whole-question routes, then separately reconcile the whole theory paper. Continue other Construction components/languages/years one paper at a time; do not certify the subject from this paper alone.

## Temporary and ignored artifacts to preserve

- `/tmp/construction588/`: rendered Ordinary paper pages 1–4, scheme pages 1–32 and extracted text. Intake script `/tmp/construction588-intake.py`; source intake and selection ledger archived in `D/drafts/construction-2015-ordinary-intake/`.
- `/tmp/construction589/` and `/tmp/construction589-{draft,review,test}.py`, `/tmp/construction589-preflight.mjs`: Ordinary Q1 draft, figures, validation and preflight. Copies in `D/drafts/construction-2015-ordinary-q1-draft/`; restore referenced temporary paths or adapt archived scripts before use.
- `/tmp/construction586/`, `/tmp/construction586-run.py`: last integrated batch logs; archived as above.
- Already-executed mutation/finalizer scripts are NOT replay-safe: `/tmp/construction575-finalize.py`, `/tmp/construction580-integrate.py`, `/tmp/construction580-fix-alias.py`, `/tmp/construction580-finalize.py`, `/tmp/construction586-integrate.py`, `/tmp/construction586-finalize.py`. `/tmp/construction587-audit.py` would overwrite final audit status back to pending if replayed.
- Preserve local SEC PDFs, original crops and all draft archives even when ignored/untracked. Do not assume every dirty subject-named asset below was authored by this checkpoint (for example the dark subject artwork); retain it for coordinating snapshot.

## Exact subject-related working-tree inventory at handoff

This filtered Git inventory records modified/untracked paths; shared/global changes may additionally exist and must be preserved by the coordinating full snapshot.

```text
 M components/MarkBank/cards/construction-studies/higher.ts
 M data/examTopics/construction-studies-runtime.json
 M scripts/markbank/authored/construction-studies.json
 M scripts/markbank/authoring/paper_census.py
 M scripts/paper-trail/build-construction-studies-exam-topic-crosswalk.mjs
 M test/constructionStudiesExamTopics.test.ts
 M test/markBankCardPreservation.test.ts
?? components/MarkBank/figures-construction-studies.json
?? data/markBank/construction-studies-library-topics.json
?? docs/markbank-audit/2026-09-28/construction-2015-higher-theory-final-source-audit.json
?? docs/markbank-audit/2026-09-28/construction-active-resume-2026-10-07.json
?? docs/markbank-audit/2026-09-28/construction-first-validation.json
?? docs/markbank-audit/2026-09-28/construction-q3-q6-validation.json
?? docs/markbank-audit/2026-09-28/construction-q7-q10-validation.json
?? docs/markbank-audit/2026-09-28/construction-source-availability-2026-10-07.json
?? docs/markbank-audit/2026-09-28/drafts/construction-2015-higher-census-repair/
?? docs/markbank-audit/2026-09-28/drafts/construction-2015-higher-intake/
?? docs/markbank-audit/2026-09-28/drafts/construction-2015-higher-q1-q2/
?? docs/markbank-audit/2026-09-28/drafts/construction-2015-higher-q10-draft/
?? docs/markbank-audit/2026-09-28/drafts/construction-2015-higher-q3-draft/
?? docs/markbank-audit/2026-09-28/drafts/construction-2015-higher-q3-intake/
?? docs/markbank-audit/2026-09-28/drafts/construction-2015-higher-q3-q6-integration/
?? docs/markbank-audit/2026-09-28/drafts/construction-2015-higher-q4-draft/
?? docs/markbank-audit/2026-09-28/drafts/construction-2015-higher-q5-draft/
?? docs/markbank-audit/2026-09-28/drafts/construction-2015-higher-q6-draft/
?? docs/markbank-audit/2026-09-28/drafts/construction-2015-higher-q6-intake/
?? docs/markbank-audit/2026-09-28/drafts/construction-2015-higher-q7-draft/
?? docs/markbank-audit/2026-09-28/drafts/construction-2015-higher-q7-q10-integration/
?? docs/markbank-audit/2026-09-28/drafts/construction-2015-higher-q8-draft/
?? docs/markbank-audit/2026-09-28/drafts/construction-2015-higher-q8-intake/
?? docs/markbank-audit/2026-09-28/drafts/construction-2015-higher-q9-draft/
?? docs/markbank-audit/2026-09-28/drafts/construction-2015-ordinary-intake/
?? docs/markbank-audit/2026-09-28/drafts/construction-2015-ordinary-q1-draft/
?? examiner-reports/construction-studies/2015-hl-marking-scheme.pdf
?? examiner-reports/construction-studies/2015-ol-marking-scheme.pdf
?? examiner-reports/construction-studies/schemes/2015-hl.md
?? public/assets/dark/star-crew/subjects/construction-studies.png
?? public/exam-figures/construction-studies/markbank/construction-studies-2015-HL-q1-access-scheme.png
?? public/exam-figures/construction-studies/markbank/construction-studies-2015-HL-q1-original.png
?? public/exam-figures/construction-studies/markbank/construction-studies-2015-HL-q1-scheme.png
?? public/exam-figures/construction-studies/markbank/construction-studies-2015-HL-q10-alternative.png
?? public/exam-figures/construction-studies/markbank/construction-studies-2015-HL-q10-original.png
?? public/exam-figures/construction-studies/markbank/construction-studies-2015-HL-q10-scheme.png
?? public/exam-figures/construction-studies/markbank/construction-studies-2015-HL-q2-original.png
?? public/exam-figures/construction-studies/markbank/construction-studies-2015-HL-q3-attached-exterior.png
?? public/exam-figures/construction-studies/markbank/construction-studies-2015-HL-q3-attached-layout.png
?? public/exam-figures/construction-studies/markbank/construction-studies-2015-HL-q3-detached-exterior.png
?? public/exam-figures/construction-studies/markbank/construction-studies-2015-HL-q3-detached-layout.png
?? public/exam-figures/construction-studies/markbank/construction-studies-2015-HL-q3-garden-link.png
?? public/exam-figures/construction-studies/markbank/construction-studies-2015-HL-q3-original.png
?? public/exam-figures/construction-studies/markbank/construction-studies-2015-HL-q3-scheme.png
?? public/exam-figures/construction-studies/markbank/construction-studies-2015-HL-q4-floor.png
?? public/exam-figures/construction-studies/markbank/construction-studies-2015-HL-q4-original.png
?? public/exam-figures/construction-studies/markbank/construction-studies-2015-HL-q4-roof-floor.png
?? public/exam-figures/construction-studies/markbank/construction-studies-2015-HL-q4-roof-windows.png
?? public/exam-figures/construction-studies/markbank/construction-studies-2015-HL-q4-roof.png
?? public/exam-figures/construction-studies/markbank/construction-studies-2015-HL-q4-windows-floor.png
?? public/exam-figures/construction-studies/markbank/construction-studies-2015-HL-q4-windows.png
?? public/exam-figures/construction-studies/markbank/construction-studies-2015-HL-q5-original.png
?? public/exam-figures/construction-studies/markbank/construction-studies-2015-HL-q5-window-head.png
?? public/exam-figures/construction-studies/markbank/construction-studies-2015-HL-q6-compact.png
?? public/exam-figures/construction-studies/markbank/construction-studies-2015-HL-q6-flexible-maintenance.png
?? public/exam-figures/construction-studies/markbank/construction-studies-2015-HL-q6-original.png
?? public/exam-figures/construction-studies/markbank/construction-studies-2015-HL-q6-scheme.png
?? public/exam-figures/construction-studies/markbank/construction-studies-2015-HL-q7-original.png
?? public/exam-figures/construction-studies/markbank/construction-studies-2015-HL-q7-roof-section.png
?? public/exam-figures/construction-studies/markbank/construction-studies-2015-HL-q8-collector.png
?? public/exam-figures/construction-studies/markbank/construction-studies-2015-HL-q8-locations.png
?? public/exam-figures/construction-studies/markbank/construction-studies-2015-HL-q8-original.png
?? public/exam-figures/construction-studies/markbank/construction-studies-2015-HL-q8-scheme.png
?? public/exam-figures/construction-studies/markbank/construction-studies-2015-HL-q8-system.png
?? public/exam-figures/construction-studies/markbank/construction-studies-2015-HL-q9-original.png
?? public/exam-figures/construction-studies/markbank/construction-studies-2015-HL-q9-scheme.png
?? scripts/markbank/atlas-reviews/construction-studies-2015-higher.json
?? scripts/markbank/authored/construction-studies-2015-higher-reviewed.json
?? scripts/markbank/authored/construction-studies-census-repairs.json
?? scripts/markbank/authoring/construction_2015_higher_q10.py
?? scripts/markbank/authoring/construction_2015_higher_q1_q2.py
?? scripts/markbank/authoring/construction_2015_higher_q3.py
?? scripts/markbank/authoring/construction_2015_higher_q3_q6.py
?? scripts/markbank/authoring/construction_2015_higher_q4.py
?? scripts/markbank/authoring/construction_2015_higher_q5.py
?? scripts/markbank/authoring/construction_2015_higher_q6.py
?? scripts/markbank/authoring/construction_2015_higher_q7.py
?? scripts/markbank/authoring/construction_2015_higher_q7_q10.py
?? scripts/markbank/authoring/construction_2015_higher_q8.py
?? scripts/markbank/authoring/construction_2015_higher_q9.py
?? scripts/markbank/authoring/construction_census_repairs.py
?? scripts/markbank/authoring/test_construction_2015_higher_q1_q2.py
?? scripts/markbank/authoring/test_construction_census_repairs.py
?? test/fixtures/construction2015Reviewed.ts
?? test/markBankConstruction2015HigherReviewed.test.ts
```
