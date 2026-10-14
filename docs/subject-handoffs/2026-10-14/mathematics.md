# Mathematics handoff — paused 2026-10-14

Branch `codex/mathematics-corpus-completion-20261007`, worktree
`~/Documents/Nextstepuni-Mathematics-Completion-20261007`. HEAD is the commit
that adds this file (its parent is `ecd19db19`). Nothing pushed, merged or deployed by the agent.

## State

- Runtime 2,304 Mathematics cards; baseline 1899/3476 asks covered, **0 orphans**, 1577 open.
- Atlas (reviewed question placements) 566. Ten regression files 398/398, typecheck clean (last run on `bd00f8f4b`).
- English Higher/Ordinary papers reviewed: 58 of 111 (2016–2026, plus 2025 and Foundation from earlier sessions).

## Batch 8 commits

| Commit | What |
|---|---|
| `9b48100ed` | Printed-question crops for all 575 new 2017–2020 cards (questionFigureKey). Cropper changes gated to legacy (≤2020) booklets; 2021+ crops unchanged by construction (regression 836 same / 10 pre-existing diffs, identical to the old cropper). |
| `ee1812991` | `paper.py`: the two census orphans fixed, gated to `subject == 'maths'` (Syriac-letter inline marker; wrapped "1." before "(a)"). All 82 maths papers re-parsed: only those two places change. Baseline re-measured without `--accept-regression`. |
| `5702be4f4` | 2016 HL P1 — 35 units, 14 scheme-row crops. |
| `54d31ad63` | 2016 HL P2 — 34 units, 9 scheme-row crops. |
| `855619a17` | 2016 OL P1 — 39 units, 7 scheme-row crops. |
| `bd00f8f4b` | 2016 OL P2 — 39 units, 17 scheme-row crops. |
| `ecd19db19` | WIP 2015 HL P1: generator drafted, not run (see resume point). |

## Outstanding

- 2015 HL P1 (WIP), 2015 HL P2, 2015 OL P1, 2015 OL P2.
- 53 further English papers before 2015 (and 2013 FL P1, parked). Irish-language editions deferred.

## Resume point: 2015 Higher Level Paper 1, step "scheme markdown + run generator"

`scripts/markbank/authoring/maths/review_2015_hl_p1.py` is complete as a
declaration (32 units, 300 marks; bands from the detailed marking notes,
quote check passing against a scratch extraction). Next steps, in order:

1. `python3 scripts/markbank/authoring/maths/make_scheme_md.py 2015 hl` (and `2015 ol`) — writes `examiner-reports/maths/schemes/2015-{hl,ol}.md`; link the PDFs: `ln -s $PWD/paper-trail-corpus/markingschemes/2015/LC003ALP000EV.pdf examiner-reports/maths/schemes/2015-hl.pdf` (OL: `LC003GLP000EV.pdf`). Both are gitignored.
2. Quote check: `python3 scripts/markbank/authoring/maths/review_2015_hl_p1.py /tmp/q.json && node scripts/markbank/authoring/maths/check_quotes.mjs examiner-reports/maths/schemes/2015-hl.md /tmp/q.json`.
3. Run the generator (adds the cards and the ledger `scripts/markbank/mathematics/reviews/2015-higher-p1.json`).
4. Question crops: `python3 scripts/markbank/authoring/maths_question_figures.py --sitting 2015 hl`, then open every crop; add explicit regions to `scripts/markbank/authoring/maths_qfig_overrides.json` where needed and `--replace-card <id>`.
5. Model-solution crops: fill `AFFECTED[(2015, 'hl')]` in `scheme_solution_figures.py` (every card — the 2015 model solutions are equation images), run `python3 scripts/markbank/authoring/maths/scheme_solution_figures.py 2015 hl`, check the solution/notes spans it prints, then `--write`, open every crop, fill `SCHEME_ROW_FIGURES` in the generator, re-run the generator with `MATHS_REVIEW_UPDATE=1`, and publish with `python3 scripts/markbank/authoring/maths/scheme_row_figures.py 2015 hl --publish p1` (it reads the same catalogue).
6. `python3 scripts/markbank/authoring/maths/publish_question_figures.py 2015-hl-p1`.
7. The per-paper checks below, a verification entry, commit, status update.

## Per-paper check commands (run from the worktree root)

```
node scripts/markbank/build-deck.mjs scripts/markbank/authored/maths.json
node scripts/markbank/mathematics/build-reviewed-topics.mjs && node scripts/markbank/mathematics/build-reviewed-topics.mjs --check
python3 scripts/markbank/mathematics/audit.py --check-reviewed
# tests: add the paper to test/mathematicsCorpus.test.ts (new-paper table + import) and test/markBankCardPreservation.test.ts (prefix list + identity hash)
npx vitest run test/markBankDeck.test.ts test/mathematicsCorpus.test.ts test/markBankCardPreservation.test.ts --maxWorkers=1
python3 scripts/markbank/authoring/reconcile.py maths --baseline write
git diff --check -- . ':!examiner-reports'
bash <scratchpad>/heavy.sh bash <scratchpad>/maths-light-heavy.sh <tag>   # ten regression files + typecheck, serialised
python3 scripts/markbank/authoring/maths/reproduce.py                      # every committed generator reproduces byte for byte
```

The build prints seven "missing primary source" lines for 2014/2020 Irish-language
PDFs; they predate this batch and do not fail the build.

## Open decisions and known issues

- **2015 HL P2 Q6(b) needs a decision.** The scheme marks the proof on three
  component scales (Diagram/Given 5B, Construction 5B, Proof 10C = 20 marks).
  The card model has one scale per card, the audit forbids two cards citing the
  same printed part, and the corpus test expects 300 marks per paper. Options:
  three component cards (needs distinct printed-part labels and audit/test
  support), or park the paper. Not started.
- 2015 schemes print model solutions (MathType images, unquotable text) and
  detailed marking notes separately; cards quote the notes and carry the
  combined crop. Some notes bands set maths as equation objects and cannot be
  quoted (e.g. 2015 HL P1 Q7(a)(i) "Recognises x = 0" — that card quotes its
  model solution's "⇒ d = 0"). The 2015 HL P1 Q7(b)(i) notes print 10C as
  (0, 3, 7, 10) against the table's (0, 4, 8, 10); the card follows the notes.
- `scheme_row_figures.py` `AFFECTED[(2016, 'ol')]` etc. need the paper's ledger
  present; it raises KeyError for a sitting whose ledgers are not all committed.
- Carried over: `bind-figures.mjs` crashes (TypeError at line 120,
  lettersVisible) and would restyle all of figures.json — left alone; figures
  are inserted textually by `publish_question_figures.py` and
  `scheme_row_figures.py --publish`. U+F061 deliberately unmapped. 2017 HL P1
  Q3(b) HPC d(fg(x))/dx unquotable (U+0BD9/U+0BDA). Caret-notation prompts list
  in the status file.

## Untracked / ignored inputs needed to resume

- Paper PDFs: `examiner-reports/maths/papers/2015-{hl,ol}-{100,200}-paper.pdf`
  (symlinks into `~/Documents/Nextstepuni-Launch-`), and
  `paper-trail-corpus/exampapers/2015/LC003{A,G}LP{1,2}00EV.pdf`.
- Schemes: `paper-trail-corpus/markingschemes/2015/LC003{A,G}LP000EV.pdf`.
- Crop PNG sources live in `exam-papers/maths/figures/<year>-<lv>/` (gitignored);
  published copies are committed under `public/exam-figures/maths/markbank/`.
- `public/papers/` holds local 2017/2018 PDF links for the browser check
  (uncommitted, intended); `tmp/` holds browser captures.
- The agent's QC tools (contact sheets, page maps, override builder `ov.py`)
  are in the session scratchpad and are not needed to resume: overrides are
  committed in `maths_qfig_overrides.json`.

## Shared files touched (integration)

`components/MarkBank/figures.json` (additions only, textual inserts),
`components/MarkBank/cards/sizes.json`,
`data/examTopics/mathematics-reviewed-question-runtime.json`,
`scripts/markbank/coverage-baseline.json` (maths entry only),
`scripts/markbank/authoring/paper.py` (maths-gated),
`test/markBankCardPreservation.test.ts`, `test/mathematicsCorpus.test.ts`.
