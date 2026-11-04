# Arabic — the first right-to-left subject in the bank

**250 of 370 leaf asks carded, 120 excluded, 0 open.** Ten sittings, 2021-2025
at both levels. Reproduce it with:

```
python3 scripts/markbank/fetch-corpus.py arabic --schemes --from 2010 --to 2026
#   move everything outside 2021-2025 into examiner-reports/arabic/glyph-corpus/
python3 scripts/markbank/authoring/ara_glyphs.py --write     # the repair map
python3 scripts/markbank/authoring/ara_text.py --audit examiner-reports/arabic
python3 scripts/markbank/authoring/paper_census.py arabic
python3 scripts/markbank/authoring/ara_all.py --report
python3 scripts/markbank/authoring/reconcile.py arabic
```

## The paper

SEC subject 059, language letter `E`, ONE booklet at each level. There is **no
Listening Comprehension `A00`**: unlike the six modern languages already
carded, Arabic is sat as a single 2½-hour written paper. It numbers 1 to 15
straight through four printed parts, so an ask needs no section token — a
citation is `2025 HL Q11(a)`, and the part is carried only as the card's
`section` for display.

| Questions | What it is | Leaves | Marks |
|---|---|---|---|
| 1-4 | Reading comprehension, multiple choice | 4 | 4 × 5 |
| 5, 6 | Directed writing, ~40 words | 2 | 2 × 30 |
| 7, 8, 9, each أ/ب/ج | Literature — "answer any four of the nine" | 9 | 4 × 35 |
| 10-13, each أ/ب/ج/د/ه | Grammar | 20 | 4 × 15 |
| 14 | Parsing (إعراب) | 1 | 20 |
| 15 | Composition, one of six titles | 1 | 100 |
| | | **37** | **400** |

Every one of the ten sittings prints exactly that, and its tariffs sum to the
400 marks its own cover states. **10 × 37 = 370 leaf asks.**

**250 are carded**: Q1-4, where the scheme names the option it accepts and the
option's own words are lifted from the paper; Q10-13, five sub-asks each at
three marks; and Q14, whose 20 marks the scheme splits over its own four
marking points.

**120 are excluded** — Q5, Q6, the nine literature alternatives of Q7-9, and
Q15. Each prints the three-row Communication-and-Content grid against the
tariff over a list headed **"تجدر الإشارة إلى:"** ("it should be noted"),
usually with "(Responses require appropriate development or elaboration beyond
mere textual transcription)". That is the written-production exclusion the
other six modern languages carry.

`stage0.py arabic` scored **26% stated** — between Home Economics, which
shipped 571 cards at 28%, and Geography, which was rejected at 29%. As always,
the score decided nothing; reading two schemes did.

## The text layer, which is the whole story

Arabic was taken on to answer one question: does a right-to-left page survive
PDF extraction? It does, but only after four faults are undone and a fifth is
repaired from the corpus. Every one of them was found by rendering a page and
comparing it with the extraction, character by character — 2023 Higher scheme
p3, 2024 Higher scheme p4, 2023 Higher paper p4, 2025 Higher paper p4, 2025
Ordinary paper p5.

`ara_text.py` handles the first four:

1. **A ligature glyph is one glyph and several characters.** Reversing
   characters rather than glyphs made the 2023 Higher answer
   "تقود التقدم في **البلد**" read "…**البدل**" — a different word — and on the
   same page turned باحثاً into ابحثاً, يقوله into يقوهل, الاعتماد into
   الاعامتد, المخبز into اخملبز and بالله into ابلله. `get_texttrace()` is the
   only PyMuPDF call that says where a glyph begins: glyph id −1 marks a
   continuation.
2. **Numbers are left-to-right islands.** ١٩٠٨ came out ٨٠٩١. The hyphen is
   *not* part of an Arabic-Indic number run — gluing on it turned the Higher
   comprehension head "من ١-٤" into "من ٤-١".
3. **A texttrace span can straddle a justified line.** On 2025 Higher p4 one
   span holds "بالمشي" at x=265 and "ترشيد" at x=523, so reading spans as units
   moved the paragraph's first two words into the middle of the line — every
   letter right, the sentence wrong. Lines are built from glyph origins, keyed
   on the BASELINE (Arabic Typesetting sets the لمج of المجتمع three points
   above its line), with vowel marks travelling with the letter they sit on.
4. **Presentation forms, the kashida, the Persian yeh and a doubled hamza.**
   NFKC then NFC, the tatweel dropped, ی/ک/ھ folded to ي/ك/ه, and a hamza the
   shaper drew twice folded onto its carrier.

## The fifth fault, and why the evidence corpus is wider than the denominator

Word embeds each document's own SUBSET of Arabic Typesetting and writes
ToUnicode entries it cannot always supply. **32,267 glyph draws across the
corpus have no honest entry at all.**

`ara_glyphs.py` recovers them without guessing. A subset copies its `glyf`
entries verbatim, so the same character has byte-identical contours everywhere,
and a glyph one file forgot is named by the file that remembered. Keying on the
glyph *id* the way `derive_glyphs.py` does would have been wrong here — the
subsets are cut in each document's own order. Composite glyphs hash their
components **and their offsets** (without the offsets ج and خ collapse and 99
outlines came back carrying two letters); a name with several subsets keeps all
their candidate outlines and accepts only where they agree; a glyph with an
EMPTY outline is a space, not a damaged letter.

The measurement that decided the subject:

| repair map derived from | words damaged | papers unreadable |
|---|---|---|
| nothing (raw PyMuPDF) | 2,277 of 15,610 — **14.6%** | 2022 OL, 2023 HL |
| the bank's ten sittings | 1,656 of 17,803 — **9.3%** | 2022 OL, 2023 HL |
| all 33 sittings 2010-2026 | **21 of 20,670 — 0.1%** | none |

Two attacks on the residue are recorded rather than believed. Rendering the 70
unknown glyphs as crops and reading them by eye was legible but is the
hand-mapping `derive_glyphs.py` exists to stop, and the first two readings
disagreed. Solving them against the corpus's own 5,652-word clean vocabulary
gave 204 words uniquely, 427 ambiguous and 961 with no match — too thin. What
worked was **more corpus**: the Paper Trail already holds Arabic back to 2010,
and an outline the 2024 scheme never names is named by the 2013 one.

So the evidence corpus is deliberately wider than the denominator. The extra
sittings live in `examiner-reports/arabic/glyph-corpus/`, where
`paper_census.py` cannot count them, and `glyphmap-arabic.json` is committed.

At 2021-2025 the reader now leaves **21 damaged words in 20,670**, 0.0-0.4%
per file, and the census reads 370 leaf asks with 5 flags — four of them the
SEC's own one-word asks ("حال.", "مبتدأ.", "شُغف...") and the fifth its
mis-lettering of 2025 Ordinary Q13, listed in `ara_scheme.SCHEME_MISPRINTS`.

## Two SEC mis-keyings, listed and not inferred

* **`٤٠` for `٤.`** — Arabic-Indic zero is a dot and so is a full stop, so a
  question head typed with a zero is indistinguishable from one typed with a
  stop. 2022 and 2024 Higher both key their fourth question that way;
  `ara_paper.MISPRINTS` names them. A heuristic would have renumbered a genuine
  question 40.
* **`(د)` twice** — 2025 Ordinary letters Q13's fourth and fifth parts both
  (د); the paper letters them (د) and (ه) and the paper wins.
  `ara_scheme.SCHEME_MISPRINTS` names it.

## What looking at it caught

Nothing in the Mark Bank UI had ever needed to know about direction. Rendered
without one, an Arabic question puts its ellipsis at the START of the stem, its
option labels at the far right of each line and its full stops on the left —
every line's punctuation on the wrong side. The question paragraph and each
marking point now carry `dir="auto"`, which resolves to `ltr` for every Latin
card in the bank and to `rtl` here. It was only visible by opening it.
