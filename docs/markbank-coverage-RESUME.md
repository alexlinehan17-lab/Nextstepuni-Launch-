# Mark Bank coverage — where it stands

Measured with `python3 scripts/markbank/authoring/partcheck.py`. Counts *parts of
papers*, not topics: a subject is finished when every part of every 2021–2025
paper it sets is carded.

Three tools, and which one is right for a subject:

| Tool | Use it for | How it decides |
|---|---|---|
| `partcheck.py` | the five subjects whose papers parse | question text, with the citation as a fallback |
| `bus_todo.py` | Business | parts read from the scheme's own table by `bus_parts.py` |
| `econ_todo.py` | Economics | parts reconstructed from the answer booklet by `econ_auto.py` |

`partcheck` names the other two rather than printing a number it cannot stand
over. `coverage.py` is the older reference-only test and `partcheck` still calls
it, but do not read its output on its own — it counted a part as carded whenever
any card named its question.

| Subject | Parts | Covered | Open | |
|---|---:|---:|---:|---|
| Agricultural Science | 929 | 827 | 102 | 90% |
| Biology | 1121 | 947 | 174 | 85% |
| Chemistry | 630 | 535 | 95 | 85% |
| Home Economics | 179 | 170 | 9 | 95% |
| Physics | 999 | 735 | 264 | 74% |
| Business | — | — | 83 | `bus_todo.py` |
| Economics | — | — | 0 | `econ_todo.py` |

Bank total: 5,230 cards.

**Home Economics is finished bar three questions.** Of the nine `partcheck`
reports open, six are carded already under a reference it reads only partly. The
three real ones are the fabric-care-symbol questions of 2021, 2022 and 2023
Ordinary Level — the scheme gives the answers ("Hand wash only", "Do not
bleach", "drip dry") but the question is a row of symbols, and there is no
figure catalogue for that subject.

**Business is measured by `bus_todo`, not here.** `partcheck` pairs only 187 of
its parts and cannot measure 66 of those, because the paper is an answerbook.

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

Classified across the four science subjects (552 of the 561):

| | Agri | Biology | Chemistry | Physics |
|---|---:|---:|---:|---:|
| Answer is itself a drawing | 6 | 36 | 23 | 104 |
| Font-mangled in the scheme | 6 | 7 | 26 | 55 |
| No printed tariff | 24 | 32 | 12 | 12 |
| Needs a figure | 11 | 15 | 11 | 13 |
| No marking points | 9 | 20 | 2 | 10 |
| Rubric only | 0 | 9 | 0 | 15 |
| Reads authorable | 29 | 34 | 18 | 14 |

The last row is the one to be careful with. Each of those was opened and
read, and nearly all turn out to be **mispairings** the classifier cannot
see: `align_ordered` offers a Chemistry scheme part numbered 60 for a paper
that stops at 11, and hands a question about a weak acid's dissociation
constant a marking point about Rutherford's gold foil. Where the scheme does
not reprint the question above its own answer there is nothing to check the
pairing against except reading it, and that is what the last pass did.

**"No printed tariff" is a real and separate blocker**, worth 80 parts.
Biology's Ordinary Level Section C prices a whole question with a
"number of correct responses → mark" table rather than a figure per part.
Guessing the split has been the recurring error of this work — a `3+1`
against a "describe two ways" part is four marks total, not four each — so
a part whose marks are not printed is left rather than estimated.

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

## Authoring Business

Business had no script path until now — all 584 of its cards were hand written —
because `lib.Author` takes question text from the paper and Business prints its
paper as an answerbook the block parser cannot follow.

`bus_lib.Author` takes the question *and* the marking points from the scheme's
own table, which is a published SEC document, so a card built this way is still
lifted rather than written. Every such card records that in its
`schemeCitation`.

```python
A = Author(2023, 'ol')
A.card(2, 9, 'b', topic='business-5-15', concept='desk-and-field-research',
       extend=1, use=[[1, 2, 3, 4], [7, 8, 9, 10, 11, 12]], marks=[8, 7],
       notation='8m (3 + 3 + 2), 7m (3 + 2 + 2)')
```

- `use` indexes the answer lines the scheme printed under the part. A list means
  one marking point that wrapped over several lines. Indexes are never
  reindexed by `extend`, so adding one cannot move which lines a card quotes.
- `extend=n` says the question itself wrapped past its own line and the first
  `n` answer lines finish it.
- `marks` must be the split the scheme prints beside each point. These are not
  the even splits a reader would guess: 2024 and 2025 pay 7 + 3 for the first
  point and 4 + 1 for the second, so a fifteen-mark part is ten and five.
- `shared_tariff=True` where one printed tariff covers a part and its siblings;
  it requires a `notation` saying what the figure covers.

Both levels work. The Higher Level tariff table prints the question with no
answer under it — those live in support notes at the back — so `bus_parts` reads
both and merges them, question from the table and answer from the notes. The
notes are laid out differently in every year: 2023 heads them `1 (a) Explain the
term indigenous firm`, 2021 heads them `3. (i)` and carries the question number
on the end of the repeated column header, and 2025 begins them with no SECTION
heading at all and never prints a SECTION 3 one. All three forms are handled.

Of the 83 parts still open, roughly ten are worth carding. The rest are a
breakeven chart to draw, a cashflow forecast to calculate, a tick-table matching
EU policies to statements, the ABQ marking rubric about links and evaluation,
and ABQ parts whose notes run A, B and C together in one block so no reader can
tell which answer belongs to which part. Same ceiling as the science subjects.

A marking point whose lines are not contiguous in the scheme cannot be carded:
the build runs its own provenance gate on the verbatim and will drop it. 2025
Ordinary Level Q9(E) is left uncarded for exactly this reason, with a note in
the script.
