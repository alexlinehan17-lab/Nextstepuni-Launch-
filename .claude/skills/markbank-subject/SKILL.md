---
name: markbank-subject
description: Card a Leaving Cert subject into Mark Bank end-to-end, or audit/backfill one that shipped. Paper-anchored census first, authoring against named refusal buckets, and a reconciliation ledger plus ratchet that define done. Use for any Mark Bank subject work — new subject, "add more cards", coverage questions, or citation doubts.
---

# Mark Bank — carding a subject

## The laws

**1. The denominator is the paper, never your reader.** Every coverage failure
this bank has had — "64 cards" for Construction Studies that became 505, "15
cards" for Maths that became 785 — came from measuring against a number
produced by the same reader that was silently losing the content. Count the
paper first, independently, and report every number beside that count.

**2. A refusal message is a hypothesis, not a fact.** "The scheme prints no
tariff" was said about a document that prices every line. Demonstrate every
blocker against the PDF before believing it.

**3. Zero flags is not clean.** The census flag set only sees *internal* gaps.
Silence hid a 10-paper alternative-question loss in Construction Studies, a
wholesale Section 3 loss in Business, and ~84 uncounted Physics asks. After
the flags are worked, independently verify per paper: the first question is
Q1, the last printed question is present, a repeated number after a standalone
OR is a choice VARIANT (not a duplicate), and spot-check three covered asks
end-to-end against the raw pages.

**4. Never join paper to scheme on the part key.** The (question, letter,
roman) join agrees with wording evidence in only one subject (agsci 96%;
home-ec 0%) — schemes number sections independently of the paper. Pair with
`align.py`'s order-preserving, wording-scored alignment; pairs resting on
order alone get READ, not shipped. A wrong pairing passes every downstream
gate.

## Definition of done

`python3 scripts/markbank/authoring/reconcile.py <subject>` exits 0:

- every **leaf ask** the papers print is *covered* (a shipped card cites it,
  exactly or through the part the scheme priced it under) or *excluded* in
  `scripts/markbank/authoring/exclusions/<subject>.json` with a reason AND
  scheme evidence (exclusions are rare — drawing questions are cardable,
  split by what the scheme says: 156 cardable vs 13 not, when measured);
- zero **orphans** (citations no paper prints — the paper wins over the
  scheme when they disagree), zero unparsed, zero stale exclusions;
- every census **flag** diagnosed: reader-bug (fix it), paper-layout
  (explain it), or **SEC misprint** — the paper itself prints the wrong
  marker (2023 HL Biology prints a bold "16." where "(b)" belongs); misprints
  get an entry in `paper.py`'s `MISPRINTS` table keyed (subject, year,
  level), never a heuristic;
- the **ratchet** is regenerated: `reconcile.py --all --baseline write`, and
  `--baseline check` read before shipping. `test/markBankCoverage.test.ts`
  pins deck size + a citation hash to the committed baseline, so CI is RED
  until the re-measure happens;
- the CI gate (`lint`, `typecheck`, `test`, `build`) is clean — run
  separately, never chained with commit (chaining `npm test && git commit`
  once pushed a red main) — and a browser session sampled the cards: *it
  can't look poor.*

**Never report a card count as an endpoint.** The first report is the census
denominator; every later report is `covered/N`.

## The stages

### 0 · Admit
`python3 scripts/markbank/authoring/stage0.py` scores whether the scheme
prints answers — but the score does not decide it: **read one scheme.**
Home Economics shipped 571 cards at a 28% score while Geography was rejected
at 29%. A low score rejects the *prose* pipeline only; Maths was a hard
reject and ships through the scale/model-solution family.

### 1 · Corpus
`python3 scripts/markbank/fetch-corpus.py <subject> --schemes [--from 2016]`
— **without `--schemes` it fetches papers only.** The corpus on disk IS the
denominator's scope.

### 2 · Census — before any authoring
```
python3 scripts/markbank/authoring/paper_census.py <subject> --json census.json
```
Layout families (`SUBJECTS` in paper_census.py): **merged** (numbering runs
on across booklets — most), **papers** (components each starting at Q1 —
Maths), **sections** (numbering restarts — Business, Home Ec; the walker also
handles the headless ABQ, electives with glued "1.(a)" sub-heads, capital
markers, and instruction-page pricing lines). Work the flags, then apply
Law 3. Diagnose by printing blocks beside the raw PDF:
```python
import sys; sys.path.insert(0,'scripts/markbank/authoring')
import paper as PP
P = PP.Paper('<subject>', 2022, 'hl')       # component='100' for maths
for i, b in enumerate(P._all_blocks()): print(i, repr(str(b)[:100]))
```

### 3 · Shapes → pipeline family
`python3 scripts/markbank/authoring/shapes.py <subject>` classifies every
priced scheme line. Families: **prose bullets** (generic block parsers),
**two-half** (`cs_scheme.py`/`cs_lib.py`), **scale + model solution**
(`maths_scheme.py`/`maths_lib.py` + `mathtext.py`). Then run
`python3 scripts/markbank/append-scheme-blocks.py <subject>` once so the
provenance gate holds both renderings (9%→1% gate-failure when it was added).

### 4 · Glyph gate
`python3 scripts/markbank/authoring/derive_glyphs.py --write` re-derives the
broken-font map from glyph ids. Never hand-map; settle survivors by cropping
the glyph and looking. Fold ligatures only — `foldDigits` rewrites sub- and
superscripts and cost a Chemistry card.

### 5 · Author
- **Lift, never write** — question from the paper, marking points from the
  scheme, verbatim.
- **Pair via align.py (Law 4)**; pass the SCHEME's key to `from_run`.
- **NEVER GUESS A TARIFF** — five separate incidents. No printed tariff, no
  card. Schemes answered graphically use `tick=True/False` with the note,
  after rendering the page.
- Every refusal is a named bucket (whyopen.py pattern); attack each with the
  table below before accepting it. Colliding card ids = a keying bug, not a
  duplicate.
- **Citation grammar**: refs open `YYYY HL|OL`, then the paper's own address.
  Sections subjects prefix it (`Section 2 Q4(A)`; Home Ec electives
  `Section C E1 Q1(a)(i)`); Business's headless compulsory question is
  `ABQ`; a choice variant is `Q10-alt(…)`; a split item's name rides the ref
  suffix after an em dash (`… — safety training`) or the build drops the
  second half as a duplicate; level fields are `higher`/`ordinary`, never
  `hl`/`ol`. A card id is NEVER renamed to fix a citation — ids key student
  review history; fix the ref, supersede via adopted-ids.json.

### 6 · Figures
Check `components/MarkBank/figures.json` FIRST — a figure-blocked part is
often already catalogued. **Never re-run extract-figures.py over a catalogued
subject** (indices drift; wrong image on a card is the corruption this
pipeline exists to prevent). Re-crop with `crop-question-art.py --page N`
(name it `-art`, `--pad-top` when labels sit above the ink); drawn charts are
invisible to the raster extractor — stroke-scan every page
(`get_drawings`, `--keep-charts`). Open the PNG before writing the catalogue
entry. Aspect-audit: 2:1+ tall is usually a bad crop. A card naming letters
needs a labelKey; labelMeanings never caption the answer.

### 7 · Build + registries
`node scripts/markbank/build-deck.mjs scripts/markbank/authored/<subject>.json`
gates provenance/glyphs/tariffs/caps and ends by printing the LEDGER line.
Registrations or the deck ships empty/unguarded: the `DECKS` map in
`components/MarkBank/deck.ts`, strands/topics there, groups in
`curriculumRegistry.ts`, the id prefix in `test/markBankDeck.test.ts`, the
preservation baseline in `test/markBankCardPreservation.test.ts` (update
WITH a comment naming which cards moved and why), and a baseline entry via
the ratchet re-measure. `rebaseline.py` refuses on loss — trust it.

### 8 · Reconcile — the ledger
```
python3 scripts/markbank/authoring/reconcile.py <subject> --open
```
Caveats — reconcile's verdicts are hypotheses too: an "open" ask may sit in a
shipped range/compound card (the grammar expands `–` ranges and comma
compounds, but check); a "covered" ask granted through a parent or
whole-question rule deserves a spot-check that the card's text actually holds
it. Reconcile the **side ledgers** as well: every ref in
`<subject>-abandoned.json` needs a matching exclusions entry or it reports
OPEN forever; `-held.json`/`-skipped.json` are logs, not state — 23 of
agsci's 34 held rows were stale.

### 9 · Look at it
Dev server → Demo Account → subject → session, sampled across shapes and
levels. Mangled notation, thumbnail solutions, split part labels all shipped
once and were caught only by looking.

### 10 · Ship + record
Ratchet re-measure, full gate (unchained), commit, push (push to main
deploys). New traps go in the memory files and this skill.

## Refusal-bucket attack table

| Bucket | First moves (all have worked) |
|---|---|
| "nothing liftable" | The Model Solution / indicative-content column beside the empty notes column is the scheme's own text. Prose length tests starve on algebra — measure the line, not the squash. |
| "no question text" | Continuation pages; rubric-glued heads (with or without the full stop); axis labels and instruction pricing lines eaten as heads; ask on the line below (pull the letter's stem; clean halves separately); bare or letterspaced heads; head past a fixed window. |
| duplicate card id | A unit keyed by its NEIGHBOUR's marker (stop at a second letter; read two-line markers together); a section restart collapsing questions. |
| provenance "not found" | 2-D layout flattened: stacked fractions, columns, sub/superscripts (≤1.5pt either way), broken glyphs → re-derive, re-fold (fold forms are append-only). |
| over display cap | Split by the scheme's own groups; disclosed trimming. |
| figure refusals | Manifest first; re-crop; stroke scan; alt dropped, not mangled. |
| "half the corpus has no paper" | The subject may be sat as TWO papers, not one — History's Later Modern (SEC 004) and Early Modern (096) are set the same afternoon under ONE scheme, and the fetcher pulled one slug. Check `paperTrailData.ts` for a companion subject id before believing a half-corpus. |
| "the scheme prices the translation, so it must be liftable" | It prices the SOURCE, not an answer. Latin's scheme cuts the Latin a candidate is GIVEN into units with a mark after each ("reportatur Segestam;/2"), or prints the English of a prose composition with a per-word tariff above it, or at Ordinary a deduction table ("Major error= -3"). Measure it: count the English function words in every translation entry — 0.00 for all 48 unseen-translation asks, 0.32-0.40 for the composition asks, which is the SOURCE being English. A model solution priced per step (Applied Maths) is the opposite case and cards. |
| "the scheme prints only bands" | Sometimes true, and then the exclusion is the answer — but GENERATE the ledger from the scheme reader so its evidence is the printed line (History: 681 of 1,430). Never hand-type a large exclusions file. |
| no reprinted question to align on | Law 4 does not require align.py. Join on whatever BOTH documents print: History pairs on the topic TITLE (220/220), on the tariff (856/856 unit totals agree) and, at Ordinary, on whether the scheme's answers are found in that unit's own printed extract (116/116). |
| "the scheme prints no tariff beside the ask" | It may print the tariff as a SPLIT three levels up. A German scheme heads "TEXT I: LESEVERSTÄNDNIS (60 marks) (14, 18, 18, 10)", then "Frage 1: (14 marks: (a) 6; (b) 4; (c) 4)", then "(a) (6 marks)", then the leaf's own rate "(Any three: 3 x 2 marks)". Walk the split and CHECK each level against the one above it; a level that does not sum is a reader fault or an SEC misprint, never something to average. German pays a DESCENDING ladder too — "(Any THREE details: 7 marks: 3, 2, 2)" — which is `group.perOptionSteps`, not a flat 7/3. |
| "the answer language is a subject constant" | It is not, in a modern language. German answers TEXT I's Frage 1 in German and Questions 2-4 in English or Irish, in one comprehension, and prices the difference ("Answers in language not specified = half marks"). Read it per ASK, from the language the question is printed in, and put it on the card. |
| no reprinted question to align on | Law 4 does not require align.py. Join on whatever BOTH documents print: History pairs on the topic TITLE (220/220), on the tariff (856/856 unit totals agree) and, at Ordinary, on whether the scheme's answers are found in that unit's own printed extract (116/116). Italian has neither title nor wording and pairs on the SECTION and the ORDER inside it — safe only because two independent counts agree first: every section's tariffs sum to the total it prints on its own head, and the paper's ask count equals the scheme's, in all ten sittings and all 385 asks. |
| "which printed marker is a question?" | The page furniture answers it before any wording does. Italian rules answer lines under its questions and none under its passages, so the alternation R.R.R.R… over twenty pages says which page is which — no align.py needed, where French had to score wording. Check the running head is NOT the signal before keying on it: Italian heads one Higher question page like a page of reading. |
| the paper numbers roman-above-letter | The (letter, roman) key is not a fact about papers, it is a fact about SCIENCE papers. Latin sets "3. A. (ii) (a)" and Question 5 sets "(vi) (a)". Keep the key's shape — letter in the letter slot, roman in the roman slot, so reconcile's part matcher and every continuity check are untouched — and print the two in the PAPER's order (`ROMAN_MAJOR` in paper_census.py). Check the runs the way the paper nests them too, or every one of the ten Question 3 parts reports a roman-gap for holding "(ii)" and no "(i)". |
| the section token is a CHOICE, not a scope | Latin's "Section A"/"Section B" is a route through ONE question, and its questions run 1-5 across all of them. Checked per section, four false question-gaps a sitting; `'numbering': 'continuous'` checks the run once over the paper. |
| a marker that is not a marker | Cut markers out of a stream of PRINTED LINES, not blocks (pymupdf reads a whole comprehension — marker, passage, vocabulary, twelve questions — as one block), and take a marker only where it OPENS a line. That is what separates the rubric "Answer parts (i), (ii), and (iii)." from the parts it names, and "P. Cornelius cum omnibus matronis" from a Section P. Cluster lines by y with a TOLERANCE: the SEC does not always set the marker on its text's own baseline. |
| the scheme's answers are set in TWO COLUMNS | Read DOWN each column, then across. Bank the printed rows whole rather than one at a time, measure the boundary from the x of the SEC's own bullets, and cut each column at those bullets — every character on the card is then still the SEC's, in the order the SEC set it. Lithuanian does it with single words ("• Dingdavo • Lesdavo") and with AGREE/DISAGREE menus of wrapped sentences; read across the page all eighteen quoted sentences the SEC never printed. `append-scheme-columns.py` makes the .md the provenance gate reads agree — and where it cannot, refuse the ask: a marking point this bank cannot trace does not ship, and checking that in the AUTHORING script (against the same .md) turns seven cards the build would silently drop into seven named refusals and a ledger that closes. |
| a sub-marker that is not a roman | The third level of an address may be a DIGIT. The Baltic languages number the rows of a true/false table "1." to "5." where every science paper numbers them "(i)" to "(v)", and the paper wins over the scheme on the address. Both citation grammars (reconcile.py's PART_TOKEN and the mirror in test/markBankCoverage.test.ts) and the census's run check have to read it, or the parser stops at the digit and the card silently claims its whole LETTER. |
| the scheme numbers the same rows differently from the paper | Pair on printed ORDER, under two independent checks and never one: the two documents must print the SAME NUMBER of rows under that letter, and every pair must agree in wording. One pair failing either test abandons the whole letter rather than shifting the rest by one — an off-by-one here is a wrong verdict on a true/false row and passes every downstream gate. |
| a mangled font a glyph table cannot repair | Derive it from the LANGUAGE. Where no other PDF in the corpus shares the subset font, `derive_glyphs.py` has no clean sighting to learn from (4% repaired over Lithuanian). `lt_glyphs.py` votes per printed POSITION instead: for every word carrying a mangled character, search the clean vocabulary for words of the same length that agree on every character the text layer got right, and where they all agree on the letter standing in the hole, that is one vote. Three votes and a clear margin settles a character; the survivors get cropped at 400dpi and looked at. It reads whole words with five mangled characters in them, which no single-substitution test can. It stops at a glyph that means MORE THAN ONE letter — 2015 Czech uses one code point for ě, é and ý — and that sitting is excluded with the evidence, keyed (subject, year, level) like a misprint. |
| the scheme prices the QUESTION and none of its parts | Card at the level the scheme priced, with `tariffModel: questionTotal`. Latvian and Czech open with a vocabulary task that lists five expressions and glosses each one, and print the price once — "[5 bodů]" — on the question. Dividing by five is inventing a tariff; one card for the question with the SEC's gloss on a row per expression is not, and `questionTotal` exists for exactly that (what a student claims is bounded by the total, not by a per-row value the SEC never printed). |
| the ERA is not the YEAR | Read which printed examination a booklet is from the PAGE. Lithuanian was rebuilt in 2022 and Latvian and Czech, which share its reader, never were — so a year test sent every one of their 2022-2026 sittings looking for a section banner that is not there and censused ZERO asks in each. The banner says the paper is the new one; the number of part heads separates the three-part paper from the two-part one. |
| "the scheme prices by BAND, so nothing is liftable" | Measure it per SITTING, not per subject. Physical Education prints answers in 2024 (39 of 70 parts) and almost none in 2026 Higher (10 of 58); a verdict read off one paper is wrong for half the corpus. What separates a criterion from an answer is the examiner's own VOCABULARY — accurate, clear, some, detail, outline, definition — so a line carrying none of it, once its tariff cell is off, is an answer and a line carrying it is a grade. Two openers stay OUT of that list: "State" and "Name" open real answers ("State anxiety is an immediate emotional state..."). |
| the marks column is INSIDE the sentence it prices | The converter wraps a table cell the way the page prints it and glues the marks cell to the end of the wrapped line: "…the plane of movement provided. A 3" / "correct sporting example is used…". Undo the wrap — a continuation opens lower case, or the line above ends on a function word — keep the cell beside the part so its tariff is still read, and re-check every rebuilt line against the scheme. The BLOCK rendering append-scheme-blocks.py put at the foot of the same .md holds the cell unwrapped, so a correct join traces and a wrong one does not. Its other forms: the column glued to the FRONT of the row ("3+3+2 opponent that could improve her defence"), a bare word left behind ("marks outdoor and adventure activities"), and a ladder cut off mid-count ("2 + 2 + 2 +" for a four-row table, which says so with its dangling plus). |
| the answer is in the table's OTHER COLUMN | Matching tasks, True/False grids and complete-the-table asks are answered in a cell, and the flat text reads across: "Run a sprint, rest, receive feedback, Distributed repeat." is the SEC's prompt with the SEC's answer posted into the middle of it. `find_tables(strategy='lines')` reads the same page with the columns intact, including which column a ✓ sits in — the one thing a text layer cannot tell you. Join a table row to its scheme part by the part's OWN WORDS (the welded line still holds the prompt), and where one row matches, take the WHOLE table: a grid interleaves its columns differently line by line, and half a table is a card that prices two cells of four. And never exclude such an ask as "the scheme states no answer" — that is precisely what a reader which cannot read the column does not know. |
| an exclusion that stands on a printed answer | Audit the exclusions AGAINST THE SCHEME, not against the reader that wrote them — three of Physical Education's 469 claimed "the scheme states no answer" over an answer the SEC prints. Two cheap sweeps find them: an exclusion whose own EVIDENCE STRING carries a ✓ is answering itself (2021 OL Q3(c)), and an exclusion whose evidence carries a lead-in ("e.g.", "Accept:", "may include") or a semicolon list is one to open by hand (2022 HL Q17(d)(ii): "E.g.s: may include: Organise and administer the sport in Ireland; Train coaches for clubs; ..." — a DOUBLED lead-in no single-token pattern reads). The third had no tick and no lead-in: the answer was "1 mark" printed in the right column of a table, and the ask said so ("Indicate your answer by ticking the correct box"). |
| a card whose only marking point is a piece of the band | Twelve Physical Education cards each shipped one marking point cut out of the ladder that grades the answer. Every one is findable without reading a scheme: a row that is the sole point of its card and OPENS lower case, or opens on a band ("1-3 their impact", "4-5 organisation"), or carries an examiner verb. The five mechanisms, all worth checking in any subject: `re.I` neutering a `(?=[A-Z0-9])` lookahead so a lead-in test cuts the word off the front of a CRITERION ("Example provided but no explanation" → "provided but no explanation"); the marks cell printed between the wrapped halves of a descriptor, front or back; a comma split applied to PROSE, which keeps the pieces that fit the window and drops the rest ("...characterised by apprehension" + "fear"); an `X as Y` answer test firing on "given as to how"; and a decimal MEASUREMENT read as a numbered bullet ("49.20 seconds" → "seconds"). |
| a wrapped cross-reference read as a part head | "Explain how you would apply the practice method named by you in Question / 13 (c) (i) to improve the skill..." wraps on the word Question, so the ADDRESS opens the next printed line and reads exactly like a marker. 2025 Higher Q13(c)(i) collected every row belonging to (c)(ii) that way and shipped a card made of them, while (c)(ii) was left with no rows at all — and nothing flagged it, because both parts still existed. The line BEFORE is what separates them: a marker preceded by a line ending on "Question" is a continuation, and the address is dropped from it. |
| the ask's verb is one level up from its text | A stimulus-first question ("Figure 12 The popularity of mass participation events…") files the imperative under the STEM, not the part — 106 of Physical Education's 741 asks. Put the instruction back on the end for the CARD, and score the PAIRING against the same whole ask: six of 2022 Higher's asks paired to the question above them because a figure caption shares no word with the table that prices it. The census's own `text` is 160 characters, which is all a census needs and half of what a card needs; read the full wording off the paper. |
| a wrapped line vs a list | The SEC breaks a line for two reasons and the PDF cannot tell them apart — on 2024 Ordinary p8 the options and the continuations both start at x=115 and both stop short of the measure. Cut it BOTH ways and let the scheme's own printed count choose: join aggressively, and where that leaves fewer answers than "Three of:" asks for, re-cut minimally. |

## Debugging discipline

Print the failing case before patching. Assert the NAMED case changed before
trusting any aggregate — and diff corpus-wide after loosening anything.
Every scripted edit asserts `old in s`. Two-pass verify: fix all, re-run all,
then report. An aggregate that moved by zero can still be a swap of wins for
losses.
