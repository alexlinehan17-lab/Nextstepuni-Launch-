# Irish: handoff (paused 2026-10-14)

## Where it stands

- **Worktree:** `/Users/alexlinehan/Documents/Nextstepuni-Irish-Completion-20261007`
- **Branch:** `codex/irish-corpus-completion-20261007` (not pushed by this agent)
- **HEAD:** the commit that adds this file. Its parent is the WIP commit `489fae37b`.
- **Inventory:** 34/91 components reviewed (57 pending).
- **Coverage ratchet:** 857/857 card identities. This measures identity and content only; completeness is tracked in `scripts/markbank/authored/irish-archive-inventory.json`.
- **Bank:** 1860 cards (Higher 461, Ordinary 396, Foundation 1003).
- **Atlas:** 2566 entries.
- **Hosted answer overrides:** 58.

## Commits after the integration point (303756a5e, already integrated)

| Commit | What | State |
|---|---|---|
| cb60c7cfa | 2023 HL Paper 2 | Finished, fully checked |
| 701b7e38e | 2023 OL Paper 1 | Finished, fully checked |
| 42867bb33 | 2023 OL Paper 2 | Finished, fully checked |
| 2b83b57eb | Fix: classify 46 "dhá"/"an dá" lines the 2024–2026 scans missed | Finished, checked |
| 489fae37b | **WIP**: coordinator decisions 1 and 2 | Not finished (see below) |
| (this commit) | Handoff document | — |

Integrate up to 2b83b57eb. Hold 489fae37b until it is finished.

## The five coordinator decisions of 2026-10-14

1. **Strip boxed page headings from shipped keys.** Implemented in WIP 489fae37b, not fully verified.
   - Done: `scripts/markbank/authoring/irish_furniture.py` holds 11 pinned exact strings.
   - Done: `irish_cards.py` defines `HEADING_SCOPE` with per-paper counts:
     - HL P2: 2022 = 4, 2023 = 2, 2024 = 10, 2025 = 2.
     - OL P1: 2024 = 9, 2025 = 9.
     - OL P2: 2024 = 2, 2025 = 2 in `authored.json`.
   - Done: the additions builders pin their own counts (2024 OL P2 = 2, 2025 OL P2 = 2, 2026 HL P2 = 2).
   - Done: the gate test `test/irishSchemeFurniture.test.ts`.
   - Done: the audit `irish_tools/heading_strip_audit.py 2b83b57eb` returned PASS. 1822 cards are byte-identical; 38 cards differ only by 46 pinned headings; Atlas, answer maps, tags and review records are unchanged.
   - Done: the coverage contentHash was re-measured.
   - **Left:** run the full Irish test set, eslint on the new test, typecheck, build and `regenerate.sh --check`. Then turn the WIP into its own clean commit.
2. **Replace the invented "0 gan fiúntas" Gaeilge row in 2022/2024 HL P2.** Only the helper exists (WIP).
   - Done: `irish_gaeilge.py` `lifted(scheme, 18)` returns the printed five-row table and the literature note. It is checked on both schemes: 2022 table on PDF 32 and note on PDF 27; 2024 both on PDF 27.
   - **Left:**
     - In `irish_higher_routes.py` `put()`, replace the paraphrased `award('gaeilge', …)`. That covers 10 cards for 2022 and 7 for 2024.
     - In `irish_literature_2024.py`, replace `language = award(…)`. That covers 8 cards.
     - Use `guidance=[table, note]`, `guidanceKind='quality'`, `permittedMarks=0..5`.
     - Write a correction record (card IDs, old wording, new source pages), for example via the `schemes` exports in `irish_cards.py` so that `--check` covers it.
     - Audit that only the `gaeilge` criterion of those 25 cards changed.
     - No tests pin the paraphrase.
     - Make it its own commit.
3. **Foundation count lines** ("(trí phointe eolais)" etc.). Not started.
   - Findings so far:
     - 2011–2023 ledgers are JSON review records whose makers were lost.
     - 2024 decisions live in the `selection_decisions()` dict of `irish_foundation_2024.py`; 2025 decisions are in `irish_foundation.py`.
     - 2010 and 2026 have makers in `irish_ledgers/`.
   - Plan:
     - Widen each Foundation `DIRECTIVE` with `\b(dhá|trí|ceithre|cúig)\b|\ban dá\b`.
     - Append classified records for the new lines, each tagged with its source scan, through a committed maker with `--check` that re-derives them from the papers.
     - Classify only. Report to the coordinator first if any classification shows a card is wrong.
4. **2022 HL P2 3B(a): HOLD. The decision's premise does not match the paper.**
   - 3B(a)(i) prints one question about one optional modern poem (topic irish-5-6): "Déan plé ar an úsáid a bhaineann an file as do rogha ceann amháin díobh seo a leanas … íomhánna, codarsnacht nó mothúcháin."
   - The three options are literary devices inside the same poem, not different poems or syllabus texts. All four existing cards print identical question text and share one grid.
   - Under the choose-one rule (separate cards only when the marks or the Atlas topic differ), this is one card: the live `irish-2022-hl-p2-poetry-3b-a`. The branch-only `-iomhanna`, `-codarsnacht` and `-mothuchain` would be withdrawn.
   - The coordinator needs to confirm before this is changed.
5. **Foundation W-4B variants.** Not started. Audit done:
   - 11 variant groups, 32 cards: 2010 W-5B, 2011 W-5B, 2012 W-4B, 2014 W-4B, 2016 W-4B, 2018 W-4B, 2019 W-4B, 2021 W-4B, 2022 W-4B, 2024 W-4B, 2025 W-4B.
   - In every group the printed text is identical. Only the card-added line "An rogha don chárta seo: …" differs: a tick-box date, a ticked job, or the brother/sister or aunt/uncle wording inside one printed task.
   - Under the decision, every group is an exact duplicate of printed text, so each merges to one card.
   - Foundation is not on `main`, so no aliases are needed.
   - The criteria are identical within each group.
   - Worth a quick confirmation from the coordinator, since "a different date" occurs only as a tick-box option, never in the printed question.

## Exact resume point

1. Finish decision 1:
   ```
   bash /private/tmp/claude-501/-Users-alexlinehan/38586a17-3c12-459b-ba53-aaad7142cb67/scratchpad/heavy.sh bash scripts/markbank/authoring/irish_tools/test_all.sh
   ```
   Then run eslint on `test/irishSchemeFurniture.test.ts`, typecheck, build and `regenerate.sh --check`. Turn the WIP into a clean commit; it can be squashed or amended, since the branch is not integrated past 2b83b57eb.
2. Decision 2, then 3, then 5. Decision 4 once confirmed.
3. Then 2022 HL/OL, newest first, as for 2023:
   - Extract each paper and scheme and view every page visually.
   - Write `irish_<level>_2022_p<n>.py`, adapted from the 2023 modules.
   - Add the ledger maker in `irish_ledgers/`, the hook in `irish_cards.py`, the generator in `regenerate.sh`, and a `HOSTED_ANSWER_OVERRIDES` entry.
   - Run the preservation audit and `reconcile.py irish --baseline write`.
   - Write the tests and run browser QA; one commit per paper.
   - 2022 HL P2 depends on decision 4. Its unreviewed 3A and Q4 cards still carry the legacy "cumas sásúil … 0 gan fiúntas" band, which the review replaces.

## Commands (run from the worktree)

- **Rebuild everything:** `bash scripts/markbank/authoring/irish_tools/regenerate.sh`
- **Verify byte-identical:** `bash scripts/markbank/authoring/irish_tools/regenerate.sh --check`. Stage intended changes first.
- **Full Irish tests:** `bash scripts/markbank/authoring/irish_tools/test_all.sh [logdir]`
- **Per-paper preservation:**
  ```
  python3 scripts/markbank/authoring/irish_tools/preservation.py BASE YEAR LEVEL FILEID ADDED_BANK ADDED_ATLAS PRIOR_BANK PRIOR_ATLAS PREFIX
  ```
  Prior totals are now Bank 1860 and Atlas 2566.
- **Heading strip audit:** `python3 scripts/markbank/authoring/irish_tools/heading_strip_audit.py BASE`
- **Ratchet:** `python3 scripts/markbank/authoring/reconcile.py irish --baseline write`. Add `--accept-regression` only for an intentional shrink.
- **Browser QA:** `bash scripts/markbank/authoring/irish_tools/qa.sh SPEC.json OUTDIR` (port 5703).
- Run every heavy command through the shared `heavy.sh` lock.

## Ignored inputs

- **Papers and schemes:** `paper-trail-corpus/` PDFs are gitignored and local only. SHA-256 sums are pinned in each module; a mismatch fails, and the visual review must be repeated.
- **Audio:** the official SEC listening recordings are not stored. Cards play `https://www.examinations.ie/archive/exampapers/<year>/LC001ZLP017IV.mp3`. Evidence is in `scripts/markbank/authored/irish-listening-audio-verification.json`. The 2023 recording is 1398.912031 s.
- **Session scratch:** page renders and logs under `/private/tmp/claude-501/-Users-alexlinehan/38586a17-3c12-459b-ba53-aaad7142cb67/scratchpad/irish/` are temporary. Everything needed to regenerate and audit the cards is committed.

## Integration notes

- The four finished commits after 303756a5e touch:
  - Irish card files, Atlas data (`data/examTopics`, `data/paperTrail`) and answer maps (`public/paper-anchors`, `public/paper-answers`, `scripts/paper-trail/answers`).
  - `components/PaperTrail/vaultResolve.ts`: `HOSTED_ANSWER_OVERRIDES` gains 4 entries (55 → 58).
  - `components/MarkBank/cards/irish/factory.ts` and `sizes.json`.
  - `scripts/markbank/coverage-baseline.json`, Irish entry only.
  - Shared tests: `test/vaultAnchors.test.ts`, `test/markBankCardPreservation.test.ts`, `test/markBankIrish.test.ts`, `test/irishExamTopics.test.ts`, `test/irishChoiceIsNotARoute.test.ts`, and `test/markBankCoverage.test.ts` (the Irish citation grammar admits "Tréith N").
- Expect conflicts in `vaultResolve.ts`, `sizes.json`, `coverage-baseline.json` and `markBankCardPreservation.test.ts` if other subjects changed them. Re-run `reconcile.py irish --baseline write` after merging.
- `test/musicExamTopics.test.ts` timed out at 30 s twice under machine load during the full Irish runs. It passes on its own and is not related to Irish.
