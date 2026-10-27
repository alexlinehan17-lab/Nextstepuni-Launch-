# Biology handoff — 2026-10-14 (paused)

## Location and stop state

- Worktree: `/Users/alexlinehan/Documents/Nextstepuni-Biology-Audit-20261011`
- Branch: `claude/biology-audit-20261011`
- HEAD: the commit that adds this file; the last work commit before it is
  `c8384fcb6` (WIP 2018 Higher). Last complete sitting: `6e59f83ae` (2019 Higher).
- Paused on Alex's instruction to save CPU. Nothing pushed, merged or deployed.
  No dev server or browser is running (review port 5709 is free).
- The pre-existing unstaged ` D examiner-reports/biology/papers` (a symlink deletion
  in this worktree) is not mine; leave it unstaged.

## Done

- **2021–2026, both levels**: re-reviewed paper by paper and corrected in place
  (one commit per sitting, 89843f7fc … 18631734d). 1,962/1,962 asks covered at that point.
- **2020 Higher** `02f258a08` and **2020 Ordinary** `6b6a16181`: carded for the first
  time (150 and 186 cards). 6b6a16181 also fixed two 2020 Higher question-figure crops
  that stopped short of the ask, and added the gate that catches it.
- **2019 Higher** `6e59f83ae`: 148 cards. Q7(b)(iii) and (iv) are EXCLUDED: the scheme
  footnote says the SEC deemed them outside the syllabus and credited the marks to every
  candidate who attempted Q7(b). Recorded in
  `scripts/markbank/authoring/exclusions/biology.json`; the baseline was re-measured
  with `--accept-regression` (exclusions 0 -> 2). **Needs Alex's confirmation.**
- Bank state at `6e59f83ae`: Biology higher deck 1,376, ordinary 1,278; bank total
  (preservation test) **20,623**; coverage 2,379/2,381 with 2 excluded, 0 open, 0 orphans.

## Outstanding (2010–2020)

| Sitting | State |
|---|---|
| 2018 Higher | **WIP** `c8384fcb6`: ledger `bio_review_2018_hl.py` passes every gate (137 tasks -> 143 cards, 6 figures). Bank/deck not regenerated in the commit. |
| 2019 Ordinary | **Deferred — decision needed** (below). All pages read; no ledger. |
| 2018 Ordinary, 2017–2010 both levels | Not started. Schemes fetched. |

### Exact resume point — 2018 Higher

1. In `bio_review_2018_hl.py`, two asks build questions too short to stand alone
   (build-deck drops them): Q2(e) "Niche." and Q11(c)(i)2 "2. Axon". Give each its
   printed lead-in in the question text (e.g. `q=[Q2, term(2, 'Niche.', br=True)]`
   and the "Outline the role of each…" line before "2. Axon"), not only in the stem.
2. `paper_census.py`: `'biology': {'mode': 'merged', 'from': 2020, 'also': [(2019, 'hl'), (2018, 'hl')]}`.
3. `scripts/paper-trail/build-biology-exam-topic-crosswalk.mjs`: add 2018 to
   `REVIEWED_EARLIER_YEARS`.
4. Regenerate and check (below). Expected: higher deck 1,376 -> 1,519, bank 20,623 -> 20,766,
   0 dropped, 0 open. Update `test/markBankCardPreservation.test.ts` (count, id hash,
   total, `earlierHigher` 298 -> 441) and add a 2018 Higher block to
   `test/markBankBiologyReview.test.ts`.
5. The WIP runner changes (`LADDER_OF`, `Q(piece=…)`) are additive but the identity
   check has not been re-run with them: run it before committing.

### 2019 Ordinary — the decision

The 2019 OL scheme prints no per-response tariff for Q9(b)(ii)–(iv) (18 marks over 6
printed answers), Q13(c) (24 over 8; Q10–Q12(c) print "8 X 3"), Q14(a)(ii)–(v) (21 over 7)
and Q14(c) (30 over 10); Q15(c)'s "6 + 8(3)" prices nine responses but prints eight answers.
Q7(b) reconciles only if (iii) "Number of bubbles/per minute" counts as two points. The
2015–2018 OL schemes print complete tariffs, so this is 2019 OL only. Options: derive the
uniform split from the printed part totals (recorded as derived), or exclude the unpriced
parts with that evidence. The census window does not include 2019 OL, so it stays out of
coverage until decided.

## Regenerate and check

All from the worktree root. Heavy commands only through the shared lock script.

```bash
# review gates (check only), then write one sitting
python3 scripts/markbank/authoring/bio_review.py 2018 hl
python3 scripts/markbank/authoring/bio_review.py 2018 hl --write
python3 scripts/markbank/authoring/bio_tools.py scheme-md 2018 hl
python3 scripts/markbank/authoring/bio_tools.py topics 2018 hl "<adds>" [--replace]
node scripts/markbank/build-deck.mjs scripts/markbank/authored/biology.json   # watch DROPPED
node scripts/paper-trail/build-biology-exam-topic-crosswalk.mjs
python3 scripts/markbank/authoring/cardlint.py biology
python3 scripts/markbank/authoring/reconcile.py biology --open
python3 scripts/markbank/authoring/reconcile.py biology --baseline write
python3 scripts/markbank/authoring/bio_tools.py identity     # every reviewed sitting byte-identical
# reviewer views
python3 scripts/markbank/authoring/bio_tools.py cards|pointers|crops 2018 hl
# heavy (via the lock): 10 vitest files, typecheck:test, eslint, phone views on port 5709
bash <scratchpad>/heavy.sh npx vitest run test/markBankBiologyReview.test.ts \
  test/markBankCardPreservation.test.ts test/markBankDeck.test.ts test/markBankCoverage.test.ts \
  test/curriculumRegistry.test.ts test/biologyExamTopics.test.ts test/markBankContentFree.test.ts \
  test/markBankSession.test.tsx test/markBankEnglish.test.ts test/physicsExamTopics.test.ts
bash <scratchpad>/heavy.sh npm run typecheck:test
bash <scratchpad>/heavy.sh bash scripts/markbank/authoring/bio_browser/run.sh "bio-2018-hl-q3-a,bio-2018-hl-q13-b-ii:dark"
```

The preservation hash is the sha256 of the deck's sorted card ids joined by newlines.

## Sources

- Papers: `examiner-reports/biology/papers/` (2019–2020 split 038/040 booklets;
  2010–2018 single `YYYY-LL-paper.pdf`). Never commit PDFs.
- Schemes: all 22 EV schemes 2010–2020 fetched into
  `examiner-reports/biology/schemes/YYYY-hl.pdf|YYYY-ol.pdf` (PDFs gitignored; the
  `.md` beside each reviewed sitting is committed — the deck build's provenance gate reads it).
  The 2020 OL scheme cover has no level; `scheme-md` handles it.
- Census window: `scripts/markbank/authoring/paper_census.py` → `'biology': {'mode':
  'merged', 'from': 2020, 'also': [(2019, 'hl')]}` at HEAD. Widen one sitting at a time
  with `also`; move `from` back a year once both levels of it are carded.
- Generic-reader fixes still to make when reached: 2018 OL (stops after Q5), 2017 OL Q6.
  `paper.py` fixes are gated (MISPRINTS / WELDED_HEADS per sitting; BACKWARD_LETTER_IS_TEXT
  and BARE_MARKER_RUNS to Biology) and were proven byte-identical for the other subjects.

## Integration notes

- Bank total in `test/markBankCardPreservation.test.ts` is 20,623 at `6e59f83ae`; other
  subjects' branches change it too — the coordinator reconciles at merge.
- No new card aliases since 2023 (alias count 56).
- `scripts/markbank/coverage-baseline.json` Biology entry re-measured per sitting; the
  2019 HL exclusions raised `excluded` to 2.
- Finding outside Biology (not patched): the grade bar's "Not claimed yet" list
  lower-cases row wording (`components/MarkBank/SessionScreen.tsx`, the `unclaimed`
  memo), so a genotype row "Bb" shows as "bb" — the opposite allele. It affects every
  genotype row in the bank.
