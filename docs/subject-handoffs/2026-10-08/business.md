# Business handoff — paused 2026-10-08

Alex stopped new research and feature work because of the credit limit. Preserve the full dirty snapshot; resume only when authorised. **Business is incomplete.** No commit, push, merge or deployment was performed in this worktree. Mathematics belongs to another terminal. The stored goal still names Mathematics, but user steering changed this thread to Business; `get_goal` confirmed **paused** on 2026-10-08. Do not resume or complete that stale Mathematics goal.

## Location and exact stopping point

- Worktree: `/Users/alexlinehan/Documents/Nextstepuni-Business-Completion-20261007`
- Branch: `codex/business-corpus-completion-20261007`
- HEAD: `8deb273f1b13341dcfa85204f7e4d784b638b21f`
- Last completed source review: **2020, Higher, English (`ev`), Section 1 Q1–Q10 and Section 3 Q1–Q7**, including all four Q1(B) consumer-law routes. Previously reviewed ABQ remains included.
- Next untouched review: **2021, Higher, English (`ev`), Section 1 Q1**, then Q2–Q12 and Section 3 Q1–Q8. Papers: `paper-trail-corpus/exampapers/2021/LC033ALP032EV.pdf` (Section 1, 36 pages) and `LC033ALP041EV.pdf` (Sections 2/3, 12 pages). Scheme: `paper-trail-corpus/markingschemes/2021/LC033ALP000EV.pdf` (60 pages).
- 2021 renders/text are prepared. Only Section 1 extracted text pages 1–6 and the existing-card inventory were read during preparation; **no new 2021 visual review or authoring is complete**. The 2021 ABQ was reviewed earlier.

## Completed versus unfinished

- Runtime: **1,040 cards = 706 Higher + 334 Ordinary**. All **606 original authored IDs** remain. Reviewed runtime subset: **439 = 434 new IDs + 5 corrected existing IDs**; base rubric data has 414 cards and seven route pools generate 25 cards.
- All **2010–2026 English Higher ABQs** reviewed (68 tasks). Full English Higher papers **2013–2020** reviewed: **nine documents**, because 2020 has two booklets. Full review is source-pinned in the paper ledger, not inferred from counts.
- Latest 2020 increment: 48 base tasks + four consumer-law routes = 52 new cards; with four prior ABQs, 56 reviewed runtime cards for 2020. Consumer pool chooses three of Services, Guarantees, Signs limiting consumer rights, Merchantable Quality; shared 7/7/6 marks, each route 20.
- Inventory: 96 documents, 48 English; all indexed PDFs local. Two **2020 Irish Ordinary scheme bindings** missing, rather than indexed files missing. Candidate official URL `https://www.examinations.ie/archive/markingschemes/2020/LC033GLP000IV.pdf` returned 404 on 2026-10-07; do not silently substitute an English scheme.
- Raw selection scan: 1,467 matches; **156 reviewed, 1,311 unclassified**. English Higher 2013–2020 matches classified. Normal generation deliberately fails until the remaining review is complete.
- Candidate reconciliation: **1,134/1,717 leaves covered; 583 OPEN; zero orphans/unparsed; 34 census flags**. 2020 Higher is 57/57 parser leaves. Parser coverage is only a navigation aid.
- Still unfinished: Higher short/long questions outside 2013–2020, comprehensive Ordinary paper review, Irish editions, remaining selection directives, task boundaries and flags. Existing 2021+ cards are not proof of full review. **Frozen baselines remain unchanged.**

## Authoritative data and implementation

- `scripts/markbank/authored/business.json`: original 606-card authoring source, unchanged. Preserve IDs/content unless a verified correction is recorded.
- `components/MarkBank/cards/business/rubric-authored.json`: base cards, SHA-pinned per-question reviews, mark boundaries, source pages, selection reasons and corrections.
- `components/MarkBank/cards/business/route-pools.json` + `routes.mjs`: printed finite pools and mechanical combinations. Shared unequal response tariffs stay separate from option order.
- `scripts/markbank/authored/business-paper-reviews.json`: nine full-document visual reviews, exact card/question sets, hashes and reviewed pages.
- `scripts/markbank/authored/business-selection-reviews.json`: reviewed raw matches pinned to wording/hash; finite choices reference pool IDs.
- `scripts/markbank/authored/business-corpus-inventory.json`: generated inventory; `business-completion-status.json`: latest exact checkpoint. Its `in-progress` describes corpus completeness, not permission to work while paused.
- `data/examTopics/business-source-reviewed-topics.json`: SEC-based topic corrections. Before 2020: `single`, short `1` etc versus long `S3Q1`. From 2020: short `p1/1`, long `p2/1`, ABQ `p2/ABQ`.
- `rubric.ts`, `BusinessRubricPanel.tsx`, `businessRubric.ts`, `SessionScreen.tsx`: published scoring, allowed mark steps and case-link dependencies. `SourceMaterialReader.tsx`: separate question/scheme readers, paging and zoom. `deck.ts`/`MarkBank.tsx`: additional canonical topics share one ID/progress record.
- `business_corpus_inventory.py`, `business_selection.py`, `paper_census.py`, `reconcile.py`, `build-deck.mjs`: source gates, inventory, candidate parsing and generation. `business-2013-hl-pending-review.json` is historical intermediate evidence, not the current authority.

## Method and invariants

Read repository `AGENTS.md`; for UI decisions also read `/Users/alexlinehan/Documents/Nextstepuni-Module-Brand-Review-20261005/AGENTS.md`. PDF skill was applied. Use local SEC PDFs, PyMuPDF/fitz text extraction and rendered PNGs, then visually inspect **every paper page** and relevant scheme allocations/support pages. Contact sheets are useful for blank/ruled pages; use readable single-page images for details. Counts/parser output cannot certify review.

Task unit: independently practicable published mark boundary. Retain necessary stems, exclusions, prior figures, diagrams and source pages. Required headings/comparisons remain whole; finite printed choose-k pools expand to all combinations; open examples and scheme-only alternatives do not. Pin reasons beside ambiguous selections. Resolve canonical topics through `curriculumRegistry.ts` by exam year; cross-list indivisible mixed tasks without duplicate IDs. Preserve exact source wording, hashes and all original card IDs. No baseline update until full visual review, zero-open/zero-orphan reconciliation and required checks pass. Draft generation bypasses only unclassified selection review, never stale hashes/wording.

2020 specifics: S1 Q7 statement 4 accepts **False or True**, once; cumulative short awards are 0/3/5/7/9/10. Tertiary trends accept pre-March-2020 answers. Insurance splits 6/4 and explanation supplies €28,800. Trade calculation is eight one-mark points, €108bn exports minus €113bn imports = €5bn deficit. Functional structure requires a diagram, tariff 3/3/2/2. Debt/equity evaluation only 0/2/4; guide flags contradictory control/equity example. Q7 Promotion/Place both required, 4/1/4/1 each, including evaluation. Scheme summary/support 2+3 versus 3+2 reversals are documented, not silently assigned to invented criteria.

## Commands (from this worktree; record only, do not run while paused)

```sh
python3 scripts/markbank/authoring/business_corpus_inventory.py --prepare-census
node scripts/markbank/build-deck.mjs scripts/markbank/authored/business.json --allow-incomplete-business-review
python3 scripts/markbank/authoring/reconcile.py business --json tmp/business-review/reconciliation.json > tmp/business-review/reconciliation.log 2>&1
npm test -- test/markBankBusinessCompletion.test.tsx test/businessExamTopics.test.ts test/markBankCardPreservation.test.ts test/curriculumRegistry.test.ts test/markBankDeck.test.ts test/markBankAuthoringToolkit.test.ts test/markBankSession.test.tsx test/markBankSessionPlanning.test.ts > tmp/business-review/tests.log 2>&1
npm test -- test/markBankBusinessCompletion.test.tsx > tmp/business-review/tests-2020-final.log 2>&1
npm run typecheck > tmp/business-review/typecheck.log 2>&1
npm run build > tmp/business-review/build.log 2>&1
npm run dev -- --config tmp/business-review/vite.config.ts --host 127.0.0.1 --port 5469 --strictPort
node tmp/business-review/browser.mjs
git diff --check
```

Normal generation without the draft flag must fail while selections remain unclassified. Reconciliation currently exits **120** because OPEN tasks remain. Browser script uses installed Chrome/Playwright and needs the approved escalated execution. Preview URL: `http://127.0.0.1:5469/tmp/business-review/index.html?card=bus-2020-hl-s3-q5c&theme=light`. Do not generate/edit data during browser QA (HMR interference).

Exact source-preparation pattern used: `fitz.open(pdf)`; for each page write `page.get_text()` to `2021-{s1|s23|markingschemes}-{oneBasedPage}.txt`, render `page.get_pixmap(matrix=fitz.Matrix(1.15,1.15)).save(...png)`, then inspect with `view_image`. This preparation alone is **not** review evidence.

## Last checks and process state

- Typecheck passed; production/PWA build passed in 18.09s with existing large-chunk warnings; `git diff --check` passed.
- Last eight-file test run: **331 passed, four failed**. One failure was the newly added test reading `sourceMaterial.fileid` instead of `paperFileid`; corrected, then the entire Business completion file passed **128/128**. Effective combined checkpoint: **332 pass, three unchanged frozen-baseline failures**; no second full eight-file run was claimed.
- Frozen failures: Higher expected 272 versus actual 706; total bank 10,495 versus 10,929; alias checksum count 9,727 versus 10,161. No old IDs lost; do not refresh baselines to hide incomplete corpus work.
- Seven 2020 browser scenarios passed (desktop/390px phone, light/dark): two consumer routes, trade, diagram, financing, True/False, marketing. Full scores 20/20, 20/20, 8/8, 10/10, 20/20, 10/10, 20/20; financing partial 2/20 and only 0/2/4 evaluation. PDFs, next-page navigation and zoom verified; screenshots inspected; zero page errors/document overflow. A favicon 404 is harmless.
- All generation, test, build, reconciliation, preparation and browser commands from the last work turn finished. Old Vite session was 45511 on port 5469. **Pause-time full process inventory on 2026-10-08 found no `business-review` or `5469` process**, so nothing needed termination. No other terminal/process was stopped. Goal confirmed paused.

## Next three actions — after authorised resumption

1. Visually review 2021 English Higher Section 1 Q1–Q12 against the scheme, starting at Q1. Preserve its existing 16 short-card IDs and record verified corrections; do not treat prepared text as visual review.
2. Review 2021 Section 3 Q1–Q8 and reconcile existing boundaries before mutations. Existing Q3(C) is an unexpanded choose-two EU-policy prompt; determine a preservation-safe route/legacy-ID treatment. Q6 rewards and Q7 break-even chart boundaries need particular attention. Retain the already-reviewed ABQ.
3. Classify that year's raw directives, update source-pinned question/full-paper reviews and Topic Atlas, regenerate only with the draft gate, then run reconciliation, relevant required tests and targeted browser/source QA. Continue remaining corpus review before any frozen-baseline update or completion claim.

## Ignored/local material that must travel with the snapshot

Preserve **all of `tmp/business-review/`**, especially `add-2020.py`, earlier `add-2013`–`add-2019` helpers and route helpers, `abq_authoring.py`, `browser.mjs`, `preview.tsx`, `index.html`, `vite.config.ts`; 2020/2021 page PNGs/text/contact sheets; `tests.log`, `tests-2020-final.log`, `typecheck.log`, `build.log`, reconciliation JSON/log; `2020-browser-evidence.json`, earlier year evidence and screenshots. Authoring helpers are working aids, not authorities; do not blindly rerun older helpers over later corrections. Browser helper currently targets seven 2020 scenarios.

`node_modules` and `paper-trail-corpus` are symlinks to `/Users/alexlinehan/Documents/Nextstepuni-Launch-/node_modules` and `/Users/alexlinehan/Documents/Nextstepuni-Launch-/paper-trail-corpus`. Preserve or recreate those dependencies. Ignored `examiner-reports/business/papers/` contains relative corpus links used by the parser. Playwright import path: `/Users/alexlinehan/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules/playwright/index.mjs`. Generated `dist/` is validation output, not the authoritative source.

## Dirty files at handoff (all edits preserved)

```text
M .gitignore
 M components/MarkBank/MarkBank.tsx
 M components/MarkBank/SessionScreen.tsx
 M components/MarkBank/SourceMaterialReader.tsx
 M components/MarkBank/cards/business/higher.ts
 M components/MarkBank/cards/business/ordinary.ts
 M components/MarkBank/cards/sizes.json
 M components/MarkBank/deck.ts
 M data/examTopics/registry.ts
 M index.css
 M scripts/markbank/authoring/paper_census.py
 M scripts/markbank/authoring/reconcile.py
 M scripts/markbank/build-deck.mjs
 M scripts/markbank/card-source-bindings.json
 M test/businessExamTopics.test.ts
 M test/markBankSession.test.tsx
 M types/markBank.ts
?? components/MarkBank/BusinessRubricPanel.tsx
?? components/MarkBank/businessRubric.ts
?? components/MarkBank/cards/business/route-pools.json
?? components/MarkBank/cards/business/routes.mjs
?? components/MarkBank/cards/business/rubric-authored.json
?? components/MarkBank/cards/business/rubric.ts
?? data/examTopics/business-source-reviewed-topics.json
?? examiner-reports/business/schemes/2010-hl.md
?? examiner-reports/business/schemes/2011-hl.md
?? examiner-reports/business/schemes/2012-hl.md
?? examiner-reports/business/schemes/2013-hl.md
?? examiner-reports/business/schemes/2014-hl.md
?? examiner-reports/business/schemes/2015-hl.md
?? examiner-reports/business/schemes/2016-hl.md
?? examiner-reports/business/schemes/2017-hl.md
?? examiner-reports/business/schemes/2018-hl.md
?? examiner-reports/business/schemes/2019-hl.md
?? examiner-reports/business/schemes/2020-hl.md
?? examiner-reports/business/schemes/2026-hl.md
?? scripts/markbank/authored/business-2013-hl-pending-review.json
?? scripts/markbank/authored/business-completion-status.json
?? scripts/markbank/authored/business-corpus-inventory.json
?? scripts/markbank/authored/business-paper-reviews.json
?? scripts/markbank/authored/business-selection-reviews.json
?? scripts/markbank/authoring/business_corpus_inventory.py
?? scripts/markbank/authoring/business_routes.mjs
?? scripts/markbank/authoring/business_selection.py
?? test/markBankBusinessCompletion.test.tsx
```

This handoff itself is newly added at `docs/subject-handoffs/2026-10-08/business.md`. The coordinating chat owns snapshot upload/integration; this subject agent is stopped.
