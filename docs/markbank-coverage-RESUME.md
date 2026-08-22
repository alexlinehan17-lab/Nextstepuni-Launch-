# Mark Bank coverage — where it stands

Measured with `python3 scripts/markbank/authoring/coverage.py`. Counts *parts of
papers*, not topics: a subject is finished when every part of every 2021–2025
paper it sets is carded.

| Subject | Scheme parts | Covered | Open | |
|---|---:|---:|---:|---|
| Agricultural Science | 929 | 817 | 112 | 88% |
| Biology | 1121 | 940 | 181 | 84% |
| Business | 253 | 141 | 112 | 56% |
| Chemistry | 630 | 535 | 95 | 85% |
| Economics | 124 | 48 | 76 | 39% |
| Home Economics | 189 | 82 | 107 | 44% |
| Physics | 1014 | 732 | 282 | 73% |
| **Total** | **4260** | **3295** | **965** | |

Bank total: 5,212 cards.

## The number moved twice, downward, and both moves were corrections

It read 281 open this morning. Two faults in the measurement, not in the bank:

1. The reference test asked whether `(year, level, question, letter, None)` had
   been seen, with `letter` unset for a part printed without one — the same key
   every card added merely by naming its question. One card citing Q1(iv)
   reported all eight parts of Question 1 as carded.
2. A bare roman counted under any letter, so a card citing Q11(c)(i) covered
   Q11(b)(i).

Both are fixed. A third fix went the other way: a range reference such as
`2023 OL Q13(c)(i)–(iii)` now covers the parts *between* its ends, which gave 57
parts back.

## What the open parts actually are

Classified across the four best-measured subjects (654 of the 965):

| | Agri | Biology | Chemistry | Physics |
|---|---:|---:|---:|---:|
| Authorable | 81 | 109 | 34 | 65 |
| Answer is itself a drawing | 6 | 31 | 26 | 124 |
| Needs a figure to read | 24 | 37 | 18 | 44 |
| Font-mangled in the scheme | 3 | 2 | 17 | 37 |
| Rubric only | 0 | 2 | 0 | 12 |

**187 of them cannot become question-and-answer cards at all.** "Draw a ray
diagram", "Draw the structure of a molecule of eugenol" — the scheme's answer is
a drawing, and it extracts as `(6)`. A further 123 need a figure the catalogue
either lacks or holds only as a truncated crop marked not-live, and 59 are
equations the scheme sets in a font whose text layer reads as doubled letters.

That is the ceiling as things stand. Roughly 289 parts are reachable with the
current card format; the other 369 need either a re-cataloguing pass on the
figures or a card type that can carry a drawing.

## How to author one

Scheme-confirmed pairings first. `align_ordered` pairs the paper and the scheme
positionally, and positional pairing is not trustworthy on its own — it handed a
Rutherford-scattering answer to a question about a pendulum. Where the scheme
reprints the question cue above its own answer, the pairing confirms itself, and
that is the set to work from without opening the page.

```bash
python3 scripts/markbank/authoring/<subject-prefix>_<year>_<level>.py   # emits JSON
python3 scripts/markbank/authoring/merge.py <subject> --write           # or agsci_all.py / econ_all.py
node scripts/markbank/build-deck.mjs scripts/markbank/authored/<subject>.json
python3 scripts/markbank/authoring/rebaseline.py <subject>
npm run lint && npm run typecheck && npm test
```

Three traps worth knowing before the first refusal:

- **Physics and several Biology papers number their scheme independently of
  their paper.** 2024 HL Biology's Question 12 is the scheme's Question 3.
  Passing the paper's key returns the wrong part's points or none, which shows
  up as `IndexError` or "the scheme has no marking points for this part". Name
  the scheme's key in `from_run`.
- **Never guess a tariff.** `3+1` against a "describe two ways" part is four
  marks total, three then one — not four for each. The scheme prints it; find it
  before authoring.
- **Physics answers only trace through `source='pdf'`.** The markdown extraction
  has no points for most of that subject.

## Subjects with their own harness

`merge.py` refuses for these, because their decks are already regenerated in
full by their own scripts and merging would emit every card a second time:
Home Economics (the `he_*.py` set), Economics (`econ_all.py`), Agricultural
Science (`agsci_all.py`).

Economics, Home Economics and Business read low above because their cards cite
references in shapes `coverage.py` reads only partly — Economics was closed to
zero gaps by `econ_todo.py`, which is the authority for that subject. Treat the
four science subjects' figures as the real ones.
