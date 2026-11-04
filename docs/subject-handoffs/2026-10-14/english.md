# English handoff — paused 2026-10-14

- Worktree: `/Users/alexlinehan/Documents/Nextstepuni-English-Completion-20261007`
- Branch: `codex/english-corpus-completion-20261007` (not pushed by me)
- HEAD before this handoff commit: `207de82d7` (WIP, see the resume point)

## Where it stands

59 of 68 English-language (EV) papers are published from independent
reviews. Irish-version (IV) editions are deferred.

- Published 59 papers / 2,294 cards (higher 654, ordinary 1,640).
- Progress aliases 159; legacy bridge covers 650 legacy prompts.
- Coverage 2,294/2,690 asks (85.3%), 396 open, 0 orphans, 0 unparsed,
  baseline written. The denominator drops by one per printed repeat.
- Preservation pins: `english:higher` 654, `english:ordinary` 1,640;
  whole-bank total 12,139.

Done: 2010 to 2015 (all four papers), 2016 (all four), 2017 HL P1, HL P2 and
OL P1, 2018 (all four), 2021 to 2026 (all four papers each).

Outstanding (9): 2017 OL P2 (WIP), 2019 HL P1, HL P2, OL P1, OL P2, 2020
HL P1, HL P2, OL P1, OL P2.

### This round's commits (oldest first)

`4cf8bf2ce` 2024 OL P2, `de52a22a1` 2023 HL P1, `b9a709647` 2023 HL P2,
`5f565ebc9` 2023 OL P1, `3726c234c` 2023 OL P2, `55b04b61d` 2022 HL P1,
`682d4c1dc` SessionScreen grid-page label, `23c4ffbe9` 2022 HL P2,
`a93b5c8af` 2022 OL P1, `1d85e03d8` 2022 OL P2, `36eb469bd` SymbolMT glyph
repair, `79752bf4c` 2021 HL P1, `646fef5d8` 2021 HL P2, `3f33b6913` 2021 OL
P1, `b60a6ff57` 2021 OL P2, `f56b8c72c` 2016 HL P2, `c55e7e983` 2016 OL P2,
`f4cbd6a14` 2017 HL P1, `58e542f0c` 2017 HL P2, `c404e04c1` 2017 OL P1,
`207de82d7` WIP 2017 OL P2.

### Group checks already run

- 2021 group: vitest English set 9 files / 194 tests pass; browser QA
  (2021 HL P1, HL P2, OL P1, OL P2 two cards) desktop and phone all ok.
- 2016 P2 group: vitest English set 9 files / 194 tests pass; browser QA
  (2016 HL P2 unseen and Single Text 60, OL P2 unseen, Q2(iii) phrases,
  Single Text Q3) desktop and phone all ok, 10/10.
- 2017 group: per-paper checks only so far (Python English tests 80 pass,
  publisher/census/card checks pass, answer sheets viewed). Vitest set and
  browser QA not yet run for 2017.

## Exact resume point

`207de82d7` holds only the 2017 OL P2 review records. Nothing is
regenerated: the decks, pins, Atlas runtime, baseline and hosted maps match
`c404e04c1`. At this HEAD `english_publish.py` raises:

```
ValueError: english-2017-ol-p2-comparative-a-q2-b: declared printed duplicate differs from english-2017-ol-p2-comparative-a-q1-b
```

Cause: the OL comparative parser puts Q2's lead-in ("We can learn about
heroes, heroines and villains by considering how successful they are at
making decisions and taking action when necessary.") in front of every
Q2 part, (b) included. The (b) wording on paper PDF11 is otherwise the same
as Q1(b). Across 2010 to 2018, a Q2(b) card carries its Q2 lead-in wherever
one is printed (2011 A and B, 2013 A, 2015 A, 2018 B).

Decide one of these:
1. Publish both cards. Remove the `r.repeat(...)` call from
   `tmp/english-audit/record-2017-ol-p2-review.py`, delete the
   `english-2017-ol-p2-comparative-a-q2-b` entry from
   `scripts/markbank/authored/english-printed-duplicates.json`, change the
   basis text to 92 cards, and re-run the recorder. This matches how every
   other year publishes a Q2(b).
2. Treat the lead-in as question-level context and keep one card. That
   needs a parser change limited to this paper, so I would not choose it.

Then:

```
cd /Users/alexlinehan/Documents/Nextstepuni-English-Completion-20261007
python3 tmp/english-audit/record-2017-ol-p2-review.py
bash tmp/english-audit/finalize-paper.sh 2017 LC002GLP200EV.pdf
(cd scripts/markbank/authoring && python3 -m unittest discover -p 'test_english*.py')
# view tmp/english-audit/answer-sheets/2017-LC002GLP200EV.pdf.jpg (every crop top against its scheme)
bash tmp/english-audit/commit-paper.sh <message file>
```

After that, take 2019 HL P1, HL P2, OL P1 and OL P2, then 2020 HL P1, HL P2,
OL P1 and OL P2 in the same way. The recorders are written and
syntax-checked (`tmp/english-audit/record-20{19,20}-*-review.py`). They are
not legacy-served, so they need no bridge entries.

- Before finalizing 2020, add these sittings to
  `tmp/english-audit/write-marking-grids.py` SITTINGS:
  `(2020, 'higher')`: H1-H8 grid PDF47, PRIMACY; `(2020, 'ordinary')`: grid
  PDF53, PRIMACY. Check the family against the 2020 scheme pages, then run
  `python3 tmp/english-audit/write-marking-grids.py`. The 2016, 2017 and
  2019 sittings are already present and generated.
- Expect small raw-rule assertion fixes when a recorder first runs
  (normalised whitespace in hit text). Classify every raw hit; do not widen
  a rule without looking at the page.
- 2020 OL P1: t3-a-iii-b repeats t2-a-iii-b. 2019 and 2020 OL P2 have two
  repeats each. Check each repeat's texts are identical before finalizing,
  because of the lead-in trap above.
- After each OL P2, view its answer sheet. If a scheme crop starts in the
  wrong place, add an anchor to `locate_scheme_cards` in
  `scripts/paper-trail/english_p2_ol.py`, run
  `python3 scripts/paper-trail/english_p2_ol.py <year>`, and assert it in
  `test_repaired_ordinary_paper_two_scheme_crops`.
- Per year group (once), add QA cards to `CARDS` in
  `tmp/english-audit/published-browser.mjs`. The primacy buttons must be
  printed grid values: HL historical 60 uses `['10','13']`, OL 30 uses
  `['5','6']`, OL 40 uses `['6','8']`, OL 35 uses `['5','6']`. Then run:

```
bash /private/tmp/claude-501/-Users-alexlinehan/38586a17-3c12-459b-ba53-aaad7142cb67/scratchpad/heavy.sh bash -c 'cd /Users/alexlinehan/Documents/Nextstepuni-English-Completion-20261007 && npx vitest run test/markBankEnglish.test.ts test/markBankEnglishPublished.test.ts test/markBankCardPreservation.test.ts test/markBankStore.test.ts test/vaultAnchors.test.ts test/englishExamTopics.test.ts test/examTopicRegistry.test.ts test/paperTrailTopics.test.ts test/markBankCoverage.test.ts 2>&1 | grep -E "Test Files|Tests |FAIL|×"; bash tmp/english-audit/run-published-browser.sh "^2017-" 2>&1 | grep -v "^STEP"'
```

When every paper is done, run the full checks through heavy.sh: typecheck,
typecheck:test (3 errors predate this work: test/programmeAnalyticsClient.test.ts,
utils/programmeAnalytics.ts), `lint --ignore-pattern 'tmp/**'`, build, and
the broad vitest set. Then update the top checkpoint in
`docs/english-completion-RESUME.md`.

## Regenerate and check (what `finalize-paper.sh` runs)

```
python3 tmp/english-audit/write-legacy-bridge.py
python3 tmp/english-audit/sync-aliases.py
python3 scripts/markbank/authoring/english_publish.py
python3 tmp/english-audit/sync-hosted-answers.py
node scripts/paper-trail/build-english-geography-exam-topic-runtime.mjs
python3 tmp/english-audit/answer-sheets.py <year>:<fileid.pdf>
python3 tmp/english-audit/refresh-pins.py
(cd scripts/markbank/authoring && python3 reconcile.py english --baseline write)
python3 scripts/markbank/authoring/english_publish.py --check
python3 scripts/markbank/authoring/english_census.py --check
python3 scripts/markbank/authoring/english_cards.py --check
python3 scripts/paper-trail/english_p2_ol.py --check
```

`finalize-paper.sh` pipes through `head`/`tail`, so a failing publisher
does not stop the later steps. Read the output. After a failure, run
`git status` to confirm nothing downstream changed.

## Open decisions and known issues

- 2017 OL P2 Q2(b) repeat (above).
- `test_english_publish.test_unreviewed_paper_is_refused_with_its_pending_work`
  now first checks that 2017 HL P1 passes its own gate. It then strips that
  paper's scheme and visual reviews to recreate the refusal, because item 5
  leaves no unreviewed EV paper to point at (f4cbd6a14).
- `test_no_finite_decision_remains`: the 221 count is now a floor, and the
  nine 2021 OL P2 Q1(a) printed choices are asserted by name.
- Q4 "satisfied / not satisfied" scheme lists stay one card each.
- Indicative bullets that print no marker render without one (existing
  SessionScreen display; candidate UI fix, not done).
- 2018 OL P1 A(iii)(b) is printed identically under all three texts but each
  copy carries its own TEXT reader, so it is not merged (reader decision).
- Comparative combined-row corrections (HL P2 Q1(a) 30 / Q1(b) 40) are
  bridge correction records quoting the scheme rows for 2021 to 2024.
- `english:higher` / `english:ordinary` pins in
  `test/markBankCardPreservation.test.ts` exist only on this branch and are
  refreshed per paper by `tmp/english-audit/refresh-pins.py`. No pin that
  exists on main was rewritten.

## Ignored inputs needed to resume

- `tmp/english-audit/` (gitignored, about 377 MB): `review_lib.py`, the 61
  `record-*.py` recorders, `write-legacy-bridge.py`,
  `write-marking-grids.py`, `finalize-paper.sh`, `commit-paper.sh`,
  `sync-aliases.py`, `sync-hosted-answers.py`, `refresh-pins.py`,
  `answer-sheets.py`, `paper-state.py`, `raw-hits.py`, `scheme-text.py`,
  `published-browser.mjs`, `run-published-browser.sh`, `vite.qa.config.ts`,
  `markbank-preview.html`, `mirror/papers` (QA PDF mirror) and
  `all-candidates.json`.
- `paper-trail-corpus` is a symlink to
  `/Users/alexlinehan/Documents/Nextstepuni-Launch-/paper-trail-corpus`
  (exam papers and marking schemes).
- The session scratchpad
  (`/private/tmp/claude-501/-Users-alexlinehan/38586a17-3c12-459b-ba53-aaad7142cb67/scratchpad/`)
  holds `heavy.sh` (the shared heavy-check lock) and `render.py` (PyMuPDF
  page renderer).

## Integration notes

Shared files this round touched: `components/MarkBank/cardAliases.ts`
(English aliases, 159 in total), `components/MarkBank/cards/sizes.json`,
`components/MarkBank/SessionScreen.tsx` (non-consecutive grid pages are
listed, not shown as a range), `components/PaperTrail/vaultResolve.ts`
(`HOSTED_ANSWER_OVERRIDES`), `scripts/markbank/coverage-baseline.json`
(english row), `test/markBankCardPreservation.test.ts` (English pins and
the whole-bank totals 12,139 / 11,496), `scripts/paper-trail/english_p2_ol.py`
(manual scheme anchors: 2016 Comparative B, 2021 Poetry E, 2023, 2024),
`scripts/markbank/authoring/english_publish.py` and `english_full_cards.py`
(`repair_basis`, SymbolMT bullet and dash), plus English-only data under
`data/examTopics/english-*`, `scripts/markbank/authored/english-*`,
`scripts/paper-trail/answers/<year>/LC002*` and
`public/paper-answers/<year>/LC002*`.

Conflicts with other subjects are likely in `cardAliases.ts`, `sizes.json`,
`coverage-baseline.json` and the bank totals in
`markBankCardPreservation.test.ts`. Rebase, then recompute the totals from
the merged decks. Never edit a frozen hash to make a test pass.
