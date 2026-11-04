# Agricultural Science handoff — 8 October 2026

Paused on Alex’s explicit credit-limit instruction. Preserve all edits. No push, merge or deployment. The full subject corpus is **not complete**. This handoff records both the validated checkpoint and the unfinished local changes; do not integrate the latter as validated work.

## Location and checkpoint

- Absolute worktree: `/Users/alexlinehan/Documents/Nextstepuni-Agricultural-Science-Completion-20261007`
- Branch: `codex/agricultural-science-completion-20261007`
- HEAD: `11186156ae8b3e8b694e18b7f40cb37f31d24dce` (completed 2012 Higher English).
- Earlier checkpoints: `4c12208a` (2011 Ordinary Irish), `41f9809b` (2011 Ordinary English), `64c829c1` (2011 Higher); original base `8deb273f`.
- Exact current edition: **2012 Agricultural Science, Higher, Irish**, `LC024ALP000IV.pdf`. Whole-paper comparison completed through **Q9(e)** (boar in dry-sow accommodation; scheme PDF page 12). Current operation is edition-wide crop/binding integration, not a new question. Last command failed in `attach_sources()` on a crop-count assertion before writing the authored cards or review ledger.

## Validated HEAD versus unfinished work

At HEAD: 1,236 Mark Bank cards (636 Higher, 600 Ordinary), zero dropped; 367 additions and one correction against the original 869. All 1,174 pre-existing authored card objects were unchanged by the 2012 English addition. There are 368 reviewed practice cards, 364 task records, 368 English Atlas practice bindings and 298 Irish bindings. Logical Atlas count is 826 (458 original whole-question identities plus 368 practice cards), across 37 topics.

Nine complete edition sweeps are recorded: 2010 Higher/Ordinary English/Irish, 2011 Higher/Ordinary English/Irish, and 2012 Higher English. The committed independent census covers six editions; reconciliation checked 360 English routes, 298 translated bindings and 81 independently censused Irish routes with zero reviewed-batch issues. **62 independent census editions remained open; 708 raw selection cues remained unclassified.** There were 29 English papers and 30 Irish comparisons still to do. These are partial-work metrics, not corpus completion evidence.

Uncommitted 2012 Higher Irish work:

- All eight original paper pages and sixteen scheme pages visually inspected; scheme content is pages 3–12.
- Independently transcribed 56 base tasks / 62 routes into the source census; census generation passed. Its JSON now covers seven editions / 61 open, ahead of the other ledgers.
- New Irish authoring module contains all 62 task crop bindings, six classified raw cues, eleven additional exact source-pinned selections, and edition-specific notes. All **53 distinct paper/scheme crop pairs** were rendered and visually inspected. Neighbouring-line fragments were trimmed; changed pairs were re-rendered and inspected.
- Notes cover the stem/leaf ratio orientation, historical potassium-test wording, runners/bulbs translation, missing nitrite step, hay moisture, and “boar in heat” versus sow. English-only Q5 numbering, Q7 F1-label and Q8 numbering notes are deliberately not copied into Irish readers.
- Completion import/attachment, reconciliation scope and hosted answer override have been edited, but **generation is currently failing and no Irish Atlas bindings have been generated**.
- Last failure: `python3 scripts/markbank/authoring/agricultural_science_completion.py --write` → `AssertionError` at the new module’s `assert (len(keys),freeze(paper),freeze(scheme))==(62,42,53)`. The 42 distinct paper-crop expectation was entered without computing it and is wrong; inspect the actual deduplicated counts and pin the reviewed result. Do not remove the assertion. This failure occurred before any authored-card/review-ledger writes.
- No tests, browser run or final preservation comparison have been run on these Irish integration edits. The progress ledger still describes HEAD and must not be treated as the current uncommitted state.

## Changed files and authoritative records

Uncommitted files at pause (besides this handoff and scratch):

- `components/PaperTrail/vaultResolve.ts` — 2012 Irish hosted-answer override added.
- `scripts/markbank/authoring/agricultural_science_2012_irish.py` — new, untracked Irish module; failing crop-count assertion near its end.
- `scripts/markbank/authoring/agricultural_science_2012_hl.py` — removes Irish comparison from remaining-work text only.
- `scripts/markbank/authoring/agricultural_science_completion.py` — imports and attaches new Irish sources.
- `scripts/markbank/authoring/agricultural_science_census.py` and `scripts/markbank/authored/agricultural-science-census.json` — independently transcribed Irish denominator, generated successfully.
- `scripts/markbank/authoring/agricultural_science_reconcile.py` — includes 2012 Higher translated bindings and updates scope text; not run after these edits.

Authoritative ledgers: `scripts/markbank/authored/agricultural-science.json`, `agricultural-science-reviewed-tasks.json`, `agricultural-science-census.json`, `agricultural-science-inventory.json`, `agricultural-science-reconciliation.json`, and `agricultural-science-completion-progress.json`. Generated runtime: `data/examTopics/agricultural-science-question-runtime.json`; source answer maps live in both `scripts/paper-trail/answers/` and `public/paper-answers/`; decks are under `components/MarkBank/cards/agricultural-science/`.

## Workflow and invariants

Read root `AGENTS.md` and `/Users/alexlinehan/Documents/Nextstepuni-Module-Brand-Review-20261005/AGENTS.md`. SEC PDFs determine wording and year-specific marks; curriculum joins resolve through the existing registry by examination year. Inspect every original paper/scheme page visually, independently transcribe the denominator before authoring, classify every raw selection cue fail-closed, then attach task-specific crops and inspect the rendered results.

A card is a separately practicable task at a published mark boundary. Expand genuine finite choose-k pools mechanically; do not expand open examples, required headings, student-generated lists or examination selections between independent tasks. Preserve pooled first-correct scales and manual totals; carry required stems, shared tariffs and figures. Preserve every prior identity and content unless a separately evidenced correction is necessary. Never weaken Atlas existing-anchor protection to force regeneration.

Both 2012 Q7(a) and Q8(c) select three of four and produce four routes each. English manual totals: Q1(a)(ii) 6, Q2(a)(ii) 10, Q3 Option One (a) 11, Q6(a)(i) 10 and Q8(a) 24. Q8(a)’s 20 acceptable points exceed the UI’s 17-option cap, so retain manual criteria rather than silently truncating its menu. Shared Q4/Q9 tariffs are shown with the full first-part/header crop: each rectangle scales to full display width, so a narrow tariff-only crop becomes unreadably oversized.

Original 869-card coverage count/hash baselines remain deliberately frozen until full independent zero-open/zero-orphan reconciliation. The generic build ledger’s 96 orphan candidates / 60 parser flags are leads, not an independent completeness denominator.

2012 Irish source hashes:

- Paper: `410a5497942472fef9e31fe61aa0c7cad3aae9de6b0a074fd75f4d2e98b3ed60`
- Scheme: `1918e89a2642b7e03baecec7975d204d04e6029cc433a1a65a13f60951308aad`

## Commands for resumption (not run during this pause)

Run from the absolute worktree above, sequentially for generation:

```sh
python3 scripts/markbank/authoring/agricultural_science_completion.py --write
node scripts/markbank/build-deck.mjs scripts/markbank/authored/agricultural-science.json
python3 scripts/markbank/authoring/agricultural_science_atlas.py --write
python3 scripts/markbank/authoring/agricultural_science_inventory.py --write
python3 scripts/markbank/authoring/agricultural_science_census.py --write
python3 scripts/markbank/authoring/agricultural_science_reconcile.py --write --check-reviewed
python3 scripts/markbank/authoring/agricultural_science_completion.py --check
python3 scripts/markbank/authoring/agricultural_science_atlas.py --check
python3 scripts/markbank/authoring/agricultural_science_inventory.py --check
python3 scripts/markbank/authoring/agricultural_science_census.py --check
```

`--check-reviewed` checks only reviewed scope; default reconciliation must still fail while editions are open. Targeted regression command (including all three mandatory AGENTS suites):

```sh
npm test -- test/markBankCardPreservation.test.ts test/curriculumRegistry.test.ts test/markBankDeck.test.ts test/markBankAgriculturalScienceCompletion.test.ts test/agriculturalScienceExamTopics.test.ts
npm run typecheck
npm run typecheck:test
python3 tmp/agricultural-science-audit/render-2012-irish-pairs.py
npm run dev -- --host 127.0.0.1 --port 5273 --strictPort
node tmp/agricultural-science-audit/browser-2012-qa.mjs --irish > tmp/agricultural-science-audit/2012-higher-irish/browser.log 2>&1
```

The browser command needs normal GUI/browser execution permission: sandboxed Chrome previously failed with EPERM. It uses local original PDFs and actual VaultQuestionCard, Viewer and PDF.js. The scratch browser script now routes Irish output to its own folder and adds Q4(a)/Q9(e): 23 representative IDs at 1200/390 px = 46 planned cases. It has **not been run** for Irish. English command is the same without `--irish`, writing to `2012-higher/browser.log`.

## Last checks and limitations

Validated English checkpoint: all 164 tests across eight suites passed after two expected-count/topic-label fixes (initial run: 162 pass, two fail; targeted rerun: all 42 tests in those two suites pass). Application typecheck passed. Test typecheck has the same three pre-existing errors: `programmeAnalyticsClient.test.ts:32/56` tuple-array types and `utils/programmeAnalytics.ts:50` ImportMeta.env. Generator checks and reviewed-scope reconciliation passed at HEAD. English browser: 42 integrated-component cases, zero page errors, including reveal/hide, nonblank crops, reader zoom/toggle/return and Mark Bank manual totals. These are **not signed-in full-app navigation** tests.

Frozen coverage ratchets intentionally fail the original Agricultural Science count/hash expectations until corpus completion. Do not update them as an intermediate fix. Pending test metadata for Irish includes census open 62→61, reviewed editions 9→10 and translated bindings 298→360; inspect every expectation, preserving original baselines.

## Next three actions after explicit resumption

1. Inspect the new Irish crop maps’ actual distinct counts, correct the mistaken count assertion, and regenerate the dependent ledgers/Atlas. Verify all 1,236 authored card objects and all original 2012 Irish whole-question anchor fields survive unchanged (only intended source notes may be appended).
2. Add edition-specific regression coverage for the 62 Irish joins, correct notes/absence of English-only notes and the independent source denominator; run required targeted tests, generation checks and the 46-case Irish browser QA. Inspect representative phone/desktop screenshots. Update progress only with verified results, then make an isolated checkpoint commit if authorized by the ongoing workflow.
3. Only after the pause is lifted and this batch passes, continue 2012 Ordinary English/Irish source review. Keep remaining editions, generic-parser leads, original baselines and signed-in application navigation explicitly open.

## Scratch, dependencies and processes

Preserve the entire untracked `tmp/agricultural-science-audit/` directory. Especially:

- `2012-higher-irish/`: original-page PNGs, paired page sheets, extracted text, normalized line-bound files, and `crop-review/review-01.png` through `review-14.png` (53 crop pairs). These include the final corrected renders.
- `render-2012-irish-pairs.py`, `render-2012-pairs.py`, `browser-2012-qa.mjs`, `reader-qa.tsx`, `reader-qa.html`, and `browser-runtime/` Playwright dependency.
- `2012-higher/`: English source/crop evidence, 126 browser screenshots plus results, `tests.log`, `recheck-tests.log`, application/test typecheck logs, and `browser.log`.
- Earlier 2010/2011 audit evidence and browser scripts remain relevant; do not discard them.

`node_modules` and `paper-trail-corpus` are symlinks to `/Users/alexlinehan/Documents/Nextstepuni-Launch-/node_modules` and `/Users/alexlinehan/Documents/Nextstepuni-Launch-/paper-trail-corpus`; preserve/resolve these when snapshotting.

No generation/test/browser command was still running at pause: the latest generation command already exited 1. The recorded own Vite preview was port 5273, PID 97294 (old session 9938). A permission-approved `ps -p 97294 -o pid,ppid,command` at handoff returned only its header / exit 1: that process had already ended, so no kill was necessary. Other terminals’ processes were not touched. Goal remains paused.
