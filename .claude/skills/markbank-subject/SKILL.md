---
name: markbank-subject
description: Card a Leaving Cert subject into Mark Bank end-to-end, or audit/backfill one that shipped. Paper-anchored census first, authoring against named refusal buckets, and a reconciliation ledger that defines done. Use for any Mark Bank subject work — new subject, "add more cards", coverage questions, or citation doubts.
---

# Mark Bank — carding a subject

## The law

**The denominator is the paper, never your reader.** Every coverage failure
this bank has had — "64 cards" for Construction Studies that became 505, "15
cards" for Maths that became 785 — came from measuring against a number
produced by the same reader that was silently losing the content. The paper is
what a student sees. Count it first, independently, and report every number
beside that denominator or not at all.

The second law follows from the first: **a refusal message is a hypothesis,
not a fact.** "The scheme prints no tariff" was said about a document that
prices every line. Every blocker must be demonstrated against the PDF before
it is believed, and every bucket of refusals attacked with the table below
before it is accepted.

## Definition of done

A subject is finished when `python3 scripts/markbank/authoring/reconcile.py
<subject>` exits 0, which means, for every paper PDF on disk:

- every **leaf ask** the papers print is *covered* (a shipped card cites it,
  exactly or through the part the scheme priced it under) or *excluded* in
  `scripts/markbank/authoring/exclusions/<subject>.json` with a reason AND the
  scheme evidence for that reason — exclusions are rare on purpose; even
  drawing questions are cardable, split by what the scheme says;
- zero **orphan** cards (a citation no paper prints — check against the PAPER,
  not the scheme; they can disagree and the paper wins);
- zero **unparsed** citations and zero stale exclusions;
- every census **flag** diagnosed (reader-bug fixed, or paper-layout explained).

Plus the gates reconcile cannot see: `npm run lint && npm run typecheck &&
npm test && npm run build` all clean, and a browser check of sampled cards —
notation legible, figures readable at size, nothing that looks poor.

**Never report a card count as an endpoint.** The first report for any subject
is the census ("the papers print N asks"); every later report is `covered/N`.
If an intermediate count would have satisfied you, the census was skipped.

## The stages

### 0 · Admit
`python3 scripts/markbank/authoring/stage0.py` scores whether the scheme
prints answers. A low score rejects the **prose** pipeline only — Mathematics
scored a hard reject and ships 785 cards through the scale/model-solution
pipeline. What stage 0 really decides is *which* pipeline family (step 3).

### 1 · Corpus
`python3 scripts/markbank/fetch-corpus.py <subject>` — papers AND schemes,
both levels, the full span (Construction Studies runs 2016–2025; default is
2021–2025). The corpus on disk IS the denominator's scope: a paper you did not
fetch is a paper you will silently not cover.

### 2 · Census — before any authoring
```
python3 scripts/markbank/authoring/paper_census.py <subject> --json census.json
```
Every leaf ask, with marks checksums and continuity flags (question-gap,
letter-gap, roman-gap, empty-leaf, marks-checksum). **Work the flags to zero
unexplained before authoring**: a flag is how every keying bug actually
presents. Diagnose by printing the reader's blocks next to the raw PDF —
observe, never reason from the aggregate:
```python
import sys; sys.path.insert(0,'scripts/markbank/authoring')
import paper as PP
P = PP.Paper('<subject>', 2022, 'hl')
for i, b in enumerate(P._all_blocks()): print(i, repr(str(b)[:100]))
```
Layout families (in `paper_census.py::SUBJECTS`): **merged** (one sitting,
numbering runs on across booklets — most subjects), **papers** (components
each starting at Q1 — Maths), **sections** (numbering restarts per section —
Business, Home Economics). A new subject that flags heavily in merged mode
probably belongs to another family or needs an adapter; extend the census, do
not hand-wave the flags.

### 3 · Shapes → pick the pipeline
`python3 scripts/markbank/authoring/shapes.py` classifies every priced scheme
line structurally. Three families exist; reuse, never rewrite:
- **prose bullets** (biology/chemistry/business style): bullet marking points
  under part headers → the generic block parsers.
- **two-half** (Construction Studies): indicative content + performance-
  criteria mark table → `cs_scheme.py` / `cs_lib.py` as the template.
- **scale + model solution** (Maths): `Scale NX (0, a, b, N)` ladders beside a
  worked solution → `maths_scheme.py` / `maths_lib.py` as the template, with
  `mathtext.py` for notation and stacked fractions.

### 4 · Glyph gate
`python3 scripts/markbank/authoring/derive_glyphs.py --write` re-derives the
broken-font repair map from glyph ids across ALL schemes on disk. Never
hand-map a glyph: settle survivors by cropping the glyph out of the page and
looking at it. The build refuses any card still carrying an unresolved glyph —
refusing beats shipping the wrong expression.

### 5 · Author
Per-paper scripts + a subject lib (copy the nearest family's). Non-negotiables:
- **Lift, never write**: question text from the paper, marking points from the
  scheme, verbatim. If either must be typed, the card is not made.
- Every refusal prints a named reason; bucket them (whyopen.py pattern) and
  attack each bucket with the table below. A bucket is only accepted after its
  members were checked against the PDF.
- Card ids collide → it is a **keying bug** (a unit named after its
  neighbour), not a duplicate. Find which unit is mislabelled.

### 6 · Figures
Crop from the paper/scheme PDF (`maths_figures.py` / `extract-figures.py`
family). Crop to the ink, exclude page furniture, audit aspect ratios (a
2:1+ tall crop is usually a bad crop), alt text from the scheme's own lines —
and dropped rather than quoted when it cannot be read cleanly. Bind via
`bind-figures.mjs`; the build refuses uninspected figures.

### 7 · Build + registries
`node scripts/markbank/build-deck.mjs scripts/markbank/authored/<subject>.json`
gates provenance (every marking point found in its own scheme), glyphs,
tariffs, display caps. Then the five registrations a subject needs or it ships
as an EMPTY deck: `DECK_SIZES` (build-written) **and** the `DECKS` map in
`components/MarkBank/deck.ts`, strands/topics in deck.ts, groups in
`curriculumRegistry.ts`, the id prefix in `test/markBankDeck.test.ts`, and the
preservation baseline in `test/markBankCardPreservation.test.ts` (update
counts WITH a comment naming exactly which cards moved and why — never to
conceal a deletion).

### 8 · Reconcile — the ledger
```
python3 scripts/markbank/authoring/reconcile.py <subject> --open
```
Work the OPEN list, the orphans, and the stale exclusions to zero. Orphans are
citation bugs (paper vs scheme numbering) as often as coverage bugs.

### 9 · Look at it
Dev server → Demo Account → the subject → run a session. Sample across
question shapes and both levels. The bar is the user's: *"it can't look
poor."* Mangled notation, thumbnail-sized worked solutions, part labels split
mid-formula — all of these shipped once and were caught only by looking.

### 10 · Ship + record
Full CI gate, commit, push (push to main deploys). Update the memory files if
a new trap or pipeline family was discovered.

## Refusal-bucket attack table

| Bucket | First moves (all have worked before) |
|---|---|
| "nothing liftable" | The Model Solution / indicative-content column beside the empty notes column is the scheme's own text — lift it. Length tests tuned for prose starve on algebra; measure the line, not the squash. |
| "no question text" | Continuation pages; head glued to the rubric; axis label eaten as a head; ask printed on the line below (pull the letter's stem, clean the halves separately); head printed without its "Q"; head past the first-6-lines window. |
| duplicate card id | A unit keyed by its NEIGHBOUR's marker (stop at a second letter, read two-line markers together); a section restart collapsing questions. |
| provenance "not found in scheme" | 2-D layout flattened: stacked fractions, columns, sub/superscripts (thresholds: smaller by ≥1.5pt, either direction), broken glyphs → re-derive map, re-fold the scheme forms (fold forms are append-only: adding one can only add matches). |
| over display cap | Split by the scheme's own groups; disclosed trimming with the note saying so. |
| figure refusals | Re-crop (furniture exclusion), re-catalogue, re-bind; alt text dropped, not mangled. |

## Debugging discipline (how the above stay fixed)

- **Print the failing case before patching.** Patch only what you have seen.
- **Assert the NAMED case changed** before trusting any aggregate; an
  aggregate that moved by zero can still hide a swap of wins for losses.
- Every scripted source edit asserts `old in s` — a silent no-op replace has
  shipped bugs twice.
- Diff corpus-wide after loosening any threshold: list what changed and check
  the changes gained only what the fix targeted.
- Two-pass verify: fix everything, re-run everything, then report.

## Reporting rules

Progress reports name three numbers and nothing else as the headline:
**paper asks (census) / covered (reconcile) / open**, plus the gate status.
Card counts appear only beside the denominator. "Done" is claimed exactly
when `reconcile.py <subject>` exits 0 and the browser check passed.
