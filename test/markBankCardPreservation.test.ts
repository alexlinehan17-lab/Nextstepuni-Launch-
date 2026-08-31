/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 *
 * Frozen card-identity baseline. Curriculum migrations may remap topic metadata
 * but must never silently remove or replace a Mark Bank card. The hash is over
 * sorted stable card IDs, not topic IDs, so a legitimate canonical-topic
 * migration leaves this test green.
 *
 * When genuinely adding cards, update the affected count/hash only after
 * checking that all previous IDs remain present. Never refresh this baseline to
 * conceal a deletion.
 */
import { createHash } from 'node:crypto';
import { describe, expect, it } from 'vitest';
import { CARDS as BIO_HIGHER } from '../components/MarkBank/cards/biology/higher';
import { CARDS as BIO_ORDINARY } from '../components/MarkBank/cards/biology/ordinary';
import { CARDS as CHEM_HIGHER } from '../components/MarkBank/cards/chemistry/higher';
import { CARDS as CHEM_ORDINARY } from '../components/MarkBank/cards/chemistry/ordinary';
import { CARDS as PHYS_HIGHER } from '../components/MarkBank/cards/physics/higher';
import { CARDS as PHYS_ORDINARY } from '../components/MarkBank/cards/physics/ordinary';
import { CARDS as AGSCI_HIGHER } from '../components/MarkBank/cards/agricultural-science/higher';
import { CARDS as AGSCI_ORDINARY } from '../components/MarkBank/cards/agricultural-science/ordinary';
import { CARDS as BUSINESS_HIGHER } from '../components/MarkBank/cards/business/higher';
import { CARDS as BUSINESS_ORDINARY } from '../components/MarkBank/cards/business/ordinary';
import { CARDS as HOME_EC_HIGHER } from '../components/MarkBank/cards/home-economics/higher';
import { CARDS as HOME_EC_ORDINARY } from '../components/MarkBank/cards/home-economics/ordinary';
import { CARDS as ECON_HIGHER } from '../components/MarkBank/cards/economics/higher';
import { CARDS as ECON_ORDINARY } from '../components/MarkBank/cards/economics/ordinary';
import { CARDS as MATHS_HIGHER } from '../components/MarkBank/cards/maths/higher';
import { CARDS as MATHS_ORDINARY } from '../components/MarkBank/cards/maths/ordinary';
import { CARDS as CS_HIGHER } from '../components/MarkBank/cards/computer-science/higher';
import { CARDS as CS_ORDINARY } from '../components/MarkBank/cards/computer-science/ordinary';
import { CARDS as CONS_HIGHER } from '../components/MarkBank/cards/construction-studies/higher';
import { CARDS as CONS_ORDINARY } from '../components/MarkBank/cards/construction-studies/ordinary';
import { CARDS as ENG_HIGHER } from '../components/MarkBank/cards/engineering/higher';
import { CARDS as ENG_ORDINARY } from '../components/MarkBank/cards/engineering/ordinary';

const decks = [
  ['biology:higher', BIO_HIGHER, 673, '45f278ef15f8d35a8a4393a0e8d01d7e5484e73a881844880dc090daeb9ce836'],
  ['biology:ordinary', BIO_ORDINARY, 686, '5792567a2b95584be782d44956c9fe7961eeec2e061683c83f32096fdf4de55e'],
  /* 2026-08-30: chemistry 482/364 -> 486/377. SEVENTEEN cards added, none
   * removed, coverage 1088/1211 -> 1105/1211 and open asks 123 -> 106.
   *
   * They are lifted through chem_scheme.py, a reader written for this
   * subject's own five-column table after the two generic parsers were shown
   * to be unusable on it -- one flattens the columns into each other, the
   * other keys the answers to a question number it takes from whichever block
   * last looked like a heading. 1136 of the 1211 paper asks (93%) now have
   * scheme text at their own key.
   *
   * Every topic was assigned by hand. chem_topics.py suggests one and scores
   * 54% against the cards already carrying a topic, which is not good enough
   * to file by.
   *
   * Two cards were written and then withdrawn, both caught by a check rather
   * than by judgement: 2022 HL Q4(b) opens "The diagram shows the origin of
   * one of the lines in the Balmer series" and no crop of that diagram
   * exists, which card lint flagged as a ghost figure; and 2025 OL Q8(a)(iii)
   * and (iv) had already been refused by chem_2025_ol.py for pointing at a
   * reaction scheme whose only crops are truncated.
   *
   * One existing card CHANGED and is better for it: chem-2022-ol-q3-b-i was
   * carrying part (ii)'s ask welded onto its own, because the paper prints
   * (ii) and (iii) as lowercase continuations of the cue (i) ends with and
   * the census had been reading straight past them. Both are now carded in
   * their own right. */
  /* 2026-08-30 (second pass): chemistry 486/377 -> 488/379, coverage
   * 1105/1211 -> 1109/1211, open 106 -> 102. Four more, none removed.
   *
   * Two of them carry the marking scheme's own DRAWING, cropped by
   * chem_figures.py and published as a solution figure the session screen
   * holds back until the student commits -- the mechanism Economics used for
   * its worked calculations. 2021 OL Q5(d)(ii) is the case that shows why it
   * is worth doing: the scheme prints BOTH accepted dot-and-cross
   * representations of O2 side by side, with the criteria beneath them, and
   * the text layer under that picture reads "x x / O O x x x x".
   *
   * The other two came free from a fix to the reader's row clustering. A term
   * carrying a SUPERSCRIPT starts higher than the marker beside it -- the mass
   * numbers in 2022 HL Q5(d)(ii)'s alpha decay open 3.7 points above their
   * "(ii)" -- so at a 3-point tolerance the whole equation clustered into the
   * row above and was filed under (d)(i), which is "Define radioactivity".
   * Widening to 5 points (line spacing there is 13) unbled that answer and
   * made it cardable. */
  /* 2026-08-30 (figure pass): chemistry 488/379 -> 496/382, coverage
   * 1109/1211 -> 1120/1211, open 102 -> 91. Eleven more, none removed.
   *
   * Every one points at something PRINTED -- "Identify the elimination
   * reaction in the scheme", "which of A, B, C or D is a graph of the boiling
   * points" -- and could not be carded at all before, because the scheme's
   * answer to the second is the single letter "D". chem_question_figures.py
   * crops the diagram from the paper and it is bound to the card.
   *
   * The raster extractor could not have supplied these. A reaction scheme is
   * drawn in VECTOR strokes with its compound names set as ordinary text
   * beside them, so 2023 HL page 9 holds thirteen image fragments and
   * twenty-two paths for what a reader sees as one picture. The cropper
   * clusters the artwork and grows each band to the labels printed inside it.
   *
   * Where one band ends and the next begins is decided by the question's own
   * PROSE, not by a gap: 2022 HL page 5 sets a Balmer energy-level diagram
   * and a photograph of a diamond 26 points apart and they answer different
   * parts, while the reaction scheme on 2023 HL page 9 has a 23-point gap
   * inside it. A sentence printed between two runs of artwork is what makes
   * them two figures.
   *
   * Every crop was opened and looked at before it was bound, and the alt text
   * on each was written from that -- a generated description would be a guess
   * about a picture, and it is the only thing a screen reader gets. */
  ['chemistry:higher', CHEM_HIGHER, 496, 'ef4c5a891f86986b4ba3091bb89a527ac4019d01f1f2590b8c465e35f2db71cc'],
  ['chemistry:ordinary', CHEM_ORDINARY, 382, '0064364c76c789a59057490251a454723738f9db96185b4eab192638eb776440'],
  /* 2026-08-23: physics drops from 487/477 to 486/475. Three cards -- one
   * Higher (2021 q13a(v)) and two Ordinary (2022 q3(ii) and q3(viii)) -- quote
   * a stacked fraction the scheme's font renders as a diagonal slash whose
   * operands extract out of order, so "1/l" arrived as "1 l⁄". They were
   * shipping that text. build-deck.mjs now refuses any card still carrying a
   * glyph no font table resolves, and refusing beats printing the wrong
   * expression in front of a student. Recoverable once the fraction reader
   * covers the Physics papers; not a deletion of content that was correct. */
  /* 2026-08-24: physics 486/475 -> 567/563 — the backfill fleet's second
   * subject. Ten agents closed every open paper ask (card, exclusion with
   * scheme evidence, figure-needed, or named refusal); the ledger reads 95.1%
   * with the residue catalogued by kind. Two defective 2024 OL cards were
   * repaired IN PLACE (same ids): q1-v now lifts the clockwise-moments line
   * its question asks for, q10-iv the closed-pipe harmonic instead of another
   * part's answer. Nothing removed. */
  /* 2026-08-30: 569 -> 570. phys-2021-hl-q13a-v comes BACK. The unreadable-
   * glyph gate read the card's `notes` — the author's record of how the card
   * was made, which never reaches the deck and which sometimes quotes a
   * corruption as the evidence for a decision. The card was dropped for
   * containing the very thing its note exists to document. Nothing else on
   * the card changed. */
  ['physics:higher', PHYS_HIGHER, 570, '9712686995c6b73f612200773855e1054ae6a5ec13ceaf5a82427934ea590007'],
  ['physics:ordinary', PHYS_ORDINARY, 563, '67dee7bc4ede4f829b03a569374b5cf94de35dd92bed3af580263667cf2a5f40'],
  ['agricultural-science:higher', AGSCI_HIGHER, 438, '31e25662626e35ca1db55e96e1cdfe0492648666c6cd35365f2c1e6d92c35f6a'],
  ['agricultural-science:ordinary', AGSCI_ORDINARY, 431, '2dbd6e7635bb73941a16773ce9d3c654741a863280c002f783fc45cd0d7e8dbd'],
  ['business:higher', BUSINESS_HIGHER, 272, 'a61655818cee2ce61307eb08fe6dad282193791674b4e5e8a893e203b64af976'],
  ['business:ordinary', BUSINESS_ORDINARY, 334, '6d62fbc00d4b0f4c411cd23c17d76ddaa63cb066325bb2974c881c8b81073b18'],
  ['home-economics:higher', HOME_EC_HIGHER, 298, '0993532438e360013ca6930c425db0b9c398b886673a4029ad6df0c9c467b49d'],
  ['home-economics:ordinary', HOME_EC_ORDINARY, 273, '5b15bc2e07a475191deb82613d27459fa2e776a0b10a2249aaff4f11f7a7e787'],
  /* 2026-08-24: economics 234/152 -> 301/243 — the backfill campaign's
   * first subject. A ten-agent fleet authored every open paper ask; the ledger
   * (reconcile.py) now reads 100.0%: 498 covered + 160 excluded-with-evidence
   * = all 658 asks the 2021-2025 papers print. Nothing removed; all prior ids
   * remain. */
  /* 2026-08-29 (twenty-first wave): economics 377/306 -> 383/314. The TICK,
   * TABLE and OTHER buckets. Six completed tick tables and three completed
   * tables cropped as solution figures — a drawn tick keeps its glyph and loses
   * its COLUMN in extraction, and the column is the answer. Coverage 637/658 ->
   * 651/658, exclusions 21 -> 7. Nothing removed. */
  /* 2026-08-29 (twentieth wave): economics 368/299 -> 377/306. The rest of the
   * DIAGRAM bucket, Higher and Ordinary. Sixteen more model diagrams cropped
   * from the schemes and bound as solution figures. Coverage 621/658 ->
   * 637/658, exclusions 37 -> 21. Nothing removed. */
  /* 2026-08-29 (nineteenth wave): economics 368/290 -> 368/299. The first nine
   * DIAGRAM asks, all Ordinary Level. The scheme answers these graphically, so
   * the crop of its completed diagram is the card's solution figure and the row
   * carries whatever contiguous run the scheme prints. Coverage 612/658 ->
   * 621/658, exclusions 46 -> 37. Nothing removed. */
  /* 2026-08-29 (eighteenth wave): economics 364/280 -> 368/290. The
   * CHART-LOOKUP bucket, 15 asks, cleared. Six of these charts had never been
   * extracted at all — a chart drawn in vector strokes is invisible to the
   * raster extractor — so they were cropped from the paper and bound. One
   * exclusion, "2024 OL Section A Q8(i) and Q8(ii)", was a COMPOUND ref that is
   * not a census ask at all and had been inflating the exclusion count by one.
   * Coverage 598/658 -> 612/658, exclusions 60 -> 46. Nothing removed. */
  /* 2026-08-29 (seventeenth wave): economics 354/268 -> 364/280. The whole
   * WORKED-CALCULATION bucket, 23 asks, cleared. Most needed a picture and not
   * a text row: set as fractions or with superscripts, the scheme's own working
   * flattens into something not merely ugly but FALSE — the HHI reads
   * "482 + 272 + ... = 3172" once the squares are lost, the multiplier reads
   * "0.1 + 0.4 = 2", and the 2023 census percentage loses its numerator
   * outright. Thirteen crops of the scheme's working now ride with those cards
   * as solution figures, the mechanism the tick tables already use. Coverage
   * 576/658 -> 598/658, exclusions 82 -> 60. Nothing removed. */
  /* 2026-08-29 (sixteenth wave): economics 350/268 -> 354/268. Four more, all
   * two-cell diagram-and-explanation parts, plus the blank market diagram the
   * 2022 HL paper prints in the Q15(a)(iii) answer space — cropped from its
   * vector strokes, which the raster extractor cannot see. Coverage
   * 572/658 -> 576/658, exclusions 86 -> 82. */
  /* 2026-08-29 (fifteenth wave): economics 348/268 -> 350/268. Two more of the
   * diagram-and-explanation class. Coverage 570/658 -> 572/658, exclusions
   * 88 -> 86. */
  /* 2026-08-29 (fourteenth wave): economics 343/268 -> 348/268. Five cards from
   * a class I had been reading wrong. Two mark cells beside a part that asks for
   * a labelled diagram AND an explanation are the two HALVES of one ask, not two
   * candidates for one tariff — the scheme even says so ("1 mark per label = 11
   * marks"). Reported as "cannot tell which prices this part" and refused; they
   * are two rows. Coverage 565/658 -> 570/658, exclusions 93 -> 88. */
  /* 2026-08-29 (thirteenth wave): economics 342/267 -> 343/268. Two cards, both
   * unblocked by correcting a mis-keyed crop: the gender-pay-gap chart was
   * catalogued under Q15(a)(i) (which asks about MILK production) and the
   * €105.4bn expenditure pie under Q13(a)(i) (which asks about the factor of
   * production labour). Fifth and sixth such correction. Coverage 563/658 ->
   * 565/658, exclusions 95 -> 93. */
  /* 2026-08-29 (twelfth wave): economics 341/267 -> 342/267. One card: the YED
   * necessity/luxury part, carried as ONE row of ⟨6⟩ rather than split 3 and 3,
   * because the scheme prints one total over two asks and halving it would be
   * arithmetic rather than a printed split. Coverage 562/658 -> 563/658. */
  /* 2026-08-29 (eleventh wave): economics 335/263 -> 341/267. Ten cards, none
   * removed. Coverage 552/658 -> 562/658, exclusions 106 -> 96. A fourth
   * mis-keyed crop was corrected on the way (the 2025 OL HDI table, catalogued
   * under Q15 when the paper prints it on page 22 under Q14(c)). */
  /* 2026-08-29 (tenth wave): economics 325/259 -> 335/263. Fourteen cards, none
   * removed. The backfill run proper: a drafter proposes a tariff from the
   * scheme's own cells and a figure from the ref hierarchy, and every proposal
   * is checked before it is used. Coverage 538/658 -> 552/658, exclusions
   * 120 -> 106. */
  /* 2026-08-29 (ninth wave): economics 323/259 -> 325/259. Two cards added,
   * both unblocked by a TOOL fix rather than by new authoring: a crop is
   * catalogued against whatever ref the inspecting agent judged it to belong
   * to, and that is usually the parent question, so the scout's ref matching
   * had to walk the whole hierarchy instead of one level. It had been
   * reporting 43 asks as needing a crop that was never taken; the real number
   * is far smaller. Coverage 536/658 -> 538/658, exclusions 122 -> 120. */
  /* 2026-08-29 (eighth wave): economics 322/259 -> 323/259. One card added:
   * 2022 HL Section A Q7(a)(ii), the justification half of a "which chart"
   * pair. Part (i) is deliberately NOT carded — the paper prints Figure A and
   * Figure B side by side and only Figure B is catalogued, so a student would
   * be asked to choose between two charts while seeing one. Its exclusion
   * reason now says that rather than calling it a tick question. */
  /* 2026-08-29 (seventh wave): economics 320/257 -> 322/259. Four more tick
   * tables, none removed. Two of them carry a Reason column, where the scheme
   * prints prose AND states the categorisation with a drawn ✔ — extraction
   * interleaves the two into "Farmers in This is a visible export. Ireland
   * selling The money leaves Germany", so the crop is the only faithful form.
   * Coverage 531/658 -> 535/658, exclusions 127 -> 123. */
  /* 2026-08-29 (sixth wave): economics 319/253 -> 320/257. Five more tick
   * tables, none removed. Each is the scheme's completed table cropped and
   * bound as a solution figure, because the ✔ is drawn and extraction loses the
   * column it sits in. Coverage 526/658 -> 531/658, exclusions 132 -> 127. */
  /* 2026-08-29 (fifth wave): economics 317/252 -> 319/253. Three cards ADDED,
   * none removed — the first tick tables in the deck. Their ✔ is DRAWN, not set
   * in the text layer, so extraction keeps the tick and loses the column it
   * sits in, and the column is the whole answer. The scheme's completed table
   * is cropped and bound as a SOLUTION figure instead (the mechanism the Maths
   * deck already uses for 819 printed model solutions: hidden until reveal,
   * rendered large). Coverage 523/658 -> 526/658, exclusions 135 -> 132. */
  /* 2026-08-29 (fourth wave): economics 316/251 -> 317/252. Two cards ADDED,
   * none removed. Diagram parts where the paper also says "Explain" and the
   * scheme prints that explanation as prose — the drawing was never the whole
   * ask. Coverage 521/658 -> 523/658, exclusions 137 -> 135. */
  /* 2026-08-29 (third wave): economics 314/250 -> 316/251. Three cards ADDED,
   * none removed. Worked calculations whose scheme sets the fraction as a
   * stacked 2-D layout — extraction flattens it, putting the denominator after
   * the answer, so each card's note says how to read the order rather than
   * pretending the layout survived. Coverage 518/658 -> 521/658, exclusions
   * 140 -> 137. Two pre-existing cards also gained the figure they had always
   * referred to ("The diagram shows...") and card lint is now clean. */
  /* 2026-08-29 (second wave): economics 303/247 -> 314/250. Fourteen cards
   * ADDED, none removed or renamed. All thirteen came out of the exclusion
   * list, where they had been recorded as "answered by reading the chart" or
   * "the response is the worked calculation" — descriptions of the answer, not
   * blockers. The charts were already catalogued; the schemes print formula,
   * substitution and result in full. Coverage 504/658 -> 517/658, exclusions
   * 154 -> 140. The fourteenth is 2024 OL Q14(b)(ii), a tick question whose
   * paper ALSO says "explain your choice": the tick was never the whole ask,
   * and the scheme prints the explanation as ordinary prose. */
  /* 2026-08-29: economics 301/243 -> 303/247. Six cards ADDED, none removed or
   * renamed. All six are parts that had been excluded as "answered by reading
   * the chart printed with it" — which described the response and was never a
   * reason to leave the ask out, because the chart itself was already
   * catalogued with verified alt text and an md5 the build re-checks. Binding
   * it gives the student what the candidate in the hall had:
   *   econ-2021-hl-q16-a-i-trend  air passenger numbers 2017-2020
   *   econ-2023-hl-q14-a-i        monthly unemployment rate, Mar 21 - Sep 22
   *   econ-2023-ol-q14-a-i        petrol prices, Apr - Sep 2022
   *   econ-2021-ol-q14-c-i        income tax on €18,000 across five countries
   *   econ-2022-ol-seca-q6-i      peak months of unemployment, Nov 20 - Nov 21
   *   econ-2024-ol-q12-c-i        overall trend in Irish unemployment, 2022
   * The -trend suffix on the first is forced: econ-2021-hl-q16-a-i is taken by
   * a card whose citation econ_refs.py corrects to Q16(c)(i), and an id is
   * never renamed because it keys a student's review history. */
  ['economics:higher', ECON_HIGHER, 383, '5b20aa9c7995f859109e8fedd3a0c83918da8830f7669f2cfc99987768630de8'],
  ['economics:ordinary', ECON_ORDINARY, 314, '57849527e60dbbe653c00a4a050629661184c6d805e8c654fc8d0bb20334ffd0'],
  /* 2026-08-23: the two newest subjects had shipped with NO identity baseline
   * at all — found by the ratchet-soundness review, which means every earlier
   * count in this file was guarding seven decks while two rode along
   * unprotected. First recorded at their current shipped state. */
  /* 2026-08-23 (same day): maths 389/396 -> 391/398. The user caught a card
   * with no context ("find the probability..." with nothing saying 15% or 11
   * players) — the fix ships every part's paper stem, and four cards whose
   * question texts previously collided as duplicates are disambiguated by
   * their stems and now ship. Nothing was removed; all prior ids remain. */
  /* 2026-08-30: maths 387/397 -> 391/400. Not new authoring — a scheme-reader
   * repair. A Maths credit band lists the ALTERNATIVE ways to reach that rung,
   * one bullet each, and answer_rows joined every line in a band into one
   * string: 274 of 799 cards stated something the scheme never said. Fixing
   * that, recognising a bare "Partial Credit:" header, and reading the letter
   * gate case-sensitively recovered seven parts. Nothing removed. */
  /* 2026-08-30 (second pass): maths 391/400 -> 393/420. The scheme reader split
   * every page at a constant x=300; across the ten schemes the "Marking Notes"
   * header actually sits between 276 and 369. Twelve pages print it LEFT of
   * 300, so it landed in the solution column, the reader found no notes on the
   * right and skipped the page outright -- every part on it unmarked. The cut
   * is now read off each page, bounded so it can only move LEFT (see
   * mathtext.reader_cut for why moving it right loses units). Coverage
   * 881/989 -> 907/989. Nothing removed. */
  /* 2026-08-30 (third pass): maths 393/420 -> 395/424, and NINE Ordinary cards
   * REMOVED. Each was defective and is listed here rather than pinned over.
   *
   * A unit's band runs from its own Scale line and the part marker prints a
   * little above it, so the reader looked back 8 points. 2021 OL scheme page 9
   * sets Q1(d)'s marker 14.6 points above its scale, outside that window, so
   * the unit shipped LETTERLESS -- keyed as the whole of Q1, carrying a crop of
   * all four parts and a 10-mark tariff against a 30-mark question. Five cards
   * were like that (2021 OL P1 Q1, Q6, Q7, Q8 and P2 Q6) and four more cited a
   * part the paper does not print (P1 Q9(iii), P2 Q1(ii), Q4(ii), Q9(ii)).
   * The band above already identified each marker and discarded it as "the
   * next unit's"; it is now handed forward instead. Q1 is (a) 5 + (b) 5 +
   * (c) 10 + (d) 10 = the 30 the paper prints.
   *
   * That in turn showed the topic vote leaning on the welding: "Find the
   * length of the runway" files nothing, and 2021 OL P2 Q9 only ever filed
   * because its text carried the aircraft stem glued on. Where the paper's
   * wording names nothing, the SCHEME states the method and the method is the
   * topic -- Q9 files as Trigonometry from "x/(sin 47) = 260/(sin 36)".
   * Coverage 907/989 -> 916/989. */
  /* 2026-08-30 (fourth pass): maths 395/424 -> 397/435, coverage 916/989 ->
   * 939/989, and FOURTEEN cards removed. Every removal is listed below; none
   * of them cost a paper ask its coverage (checked against the census, part
   * by part, before re-pinning).
   *
   * The pass fixed ten faults in how the scheme's two-column table is read.
   * The one that mattered most is a missing SPACE: the 2021 Ordinary scheme
   * prints "Scale10D (0, 3, 5, 8, 10)" eleven times, and both the regex that
   * finds a band and the one that reads its ladder required "Scale ". So the
   * band was invisible; and once the first regex was widened the second still
   * refused what it found, "the scheme prints no ladder for this part", on
   * eleven units that print one. 2021 OL P2 Q2(b) had a marker, a printed
   * solution and a full credit ladder, and no card.
   *
   * The rest are the reader mistaking one printed thing for another:
   *   - the model solution ECHOES its part marker mid-answer ("(b) h'(x) =
   *     3(2x^2) - 2(28.5x) + 105" on 2022 HL page 20). Taken for the next
   *     unit's heading it was handed to the band below, which carried the real
   *     letter past the last band: Q7 and Q8 both lost their (c), and Q8
   *     shipped two cards claiming (b). An echo is printed at the SOLUTION
   *     indent, a heading in the marker column -- x separates them, and
   *     nothing else does.
   *   - a scheme page can hold TWO questions. Page 20 of the 2023 Higher
   *     scheme heads "Q6" at y=62 and "Q7" at y=330; the whole page was filed
   *     under Q6, so Q7(a) and Q7(b) collided with the real Q6(b).
   *   - "(i) (ii)" on one line is two ROMANS, not a letter and a roman.
   *   - "(a)(i)" then "(a)(ii)" over one scale is one unit with two romans;
   *     read as a second letter it was carried down and the band that really
   *     marks 2024 HL P2 Q7(b)(i) was keyed (a)(ii).
   *   - a band handed its letter from above met that same marker again in its
   *     own lookback and re-carried it, shifting every later letter up one:
   *     2021 OL P1 Q3, Q7 and Q8 each emitted (b) twice and dropped (c).
   *   - which letter heads the NEXT band is positional, not a distance. 2023
   *     OL page 39 sets "(a)" and "(b)" 32 points apart over ONE scale while
   *     2021 OL page 11 sets them 225 apart over two. Only the last letter
   *     above the next scale can head the next unit; the others share this
   *     band's scale, and the card now cites "Q5(a), (b)" so both are credited.
   *
   * REMOVED -- ten cited a part the paper never prints, so they were answering
   * an address that does not exist: 2021 OL P1 Q9(a), P2 Q1(c), Q3(b), Q4(a),
   * Q9(b); 2023 HL P1 Q6(a), Q9(a); 2025 OL P1 Q10(c), P2 Q9(a), Q9(b).
   * Four more are the same ask under a corrected id and are still covered:
   * 2021 OL P2 Q6(b)(ii), 2022 HL P1 Q10(c)(ii), 2023 OL P1 Q10(b)(ii),
   * 2024 OL P2 Q1(a)(ii). Open asks 73 -> 50.
   *
   * Then one more, ADDED not removed: 2025 HL scheme page 8 heads a unit
   * "(c)(d)" -- two letters on one line, over a single scale. The second went
   * into the ROMAN slot, so the card cited "Q8(c)(d)" and the paper reader,
   * asked for a part (d) underneath a letter (c), found no question text and
   * refused. It cites "Q8(c), (d)" now. 939/989 -> 941/989, open 50 -> 48. */
  ['maths:higher', MATHS_HIGHER, 398, '39e8bdf9425336b1d19f5827df8fb9b811f117781b610adf6456ed9213583d25'],
  ['maths:ordinary', MATHS_ORDINARY, 435, '1739cbe00b51bbe9aed6df6e1226780777f965ec94c9492743cf2ec8df35990e'],
  /* 2026-08-30: Computer Science opened. 259 cards, 293/484 asks covered,
   * 0 orphans, card lint clean. A new subject is pinned from its first build;
   * there is no earlier count to compare it against.
   *
   * 2026-08-30 (same day): 164/95 -> 183/102, coverage 293/484 -> 327/484.
   * The added cards carry a CROP of the program their question prints. The
   * text layer hands a listing back as "1 number = 27 2 while number < 39: 3
   * print(number, end=" ")" -- line numbers run into the code and the
   * indentation gone, which is the one thing a program cannot survive losing.
   * Nothing was removed.
   *
   * 2026-08-30 (same day): 183/102 -> 191/109, coverage 327/484 -> 343/484.
   * The figure pass was extended from programs to the TABLES and DIAGRAMS the
   * questions print, and each question now publishes one crop rather than one
   * per band -- a card cites a PART, and attaching the topmost band would have
   * shown 2022 OL Q13(b) the binary digits printed for (a).
   *
   * ONE CARD WAS REMOVED, and this is the record of it rather than a hash
   * quietly moved over the top of it: cs-2021-hl-q12. That question prints one
   * database table, then the ruled box the candidate writes in, then a SECOND
   * table, and asks about both. No single rectangle holds the two tables
   * without the blank box between them, and its parts are not priced
   * separately so the card can only cite the whole question. The card it
   * replaced carried the first table only, which is the defect this pass
   * exists to remove: a question asking about a table the student cannot see.
   * It comes back when a card can carry a figure per part.
   *
   * The same span fix took a WRONG figure off three cards that kept their
   * ids -- cs-2023-hl-q6, cs-2024-hl-q10 and cs-2025-hl-q10 were each showing
   * the listing printed for the question above them. 2024 HL Q10 asks about
   * ordering kiosks and was showing a leap-year function.
   *
   * 2026-08-30 (same day): 191/109 -> 194/111, coverage 343/484 -> 348/484.
   * The TABLE a question prints comes out of its question text the way the
   * program already did, but only where what is left still ends like a
   * sentence -- a table's labels are ordinary words that also appear in the
   * question's own prose, and cutting at the first match had left "Complete
   * the truth table for the AND logic gate, shown in". Nothing was removed.
   *
   * 2026-08-30 (same day): 194/111 -> 193/116, coverage 348/484 -> 367/484.
   * The `use` indices a card is built from select into the SCHEME's own point
   * list, so the author's filtering never reached the card: nineteen cards
   * carried a row it had already rejected, one of them opening with "Any
   * response that captures the essence of any of the following:". The indices
   * now point at the scheme's list, so the filter applies -- and the filter
   * itself was corrected in both directions. It drops the CREDIT RULE ("Each
   * correct item", "Half correct conversion of (a)", "Small calculation
   * error"), which says how much of the answer earns what and never what the
   * answer is. It no longer drops a row that is all digits, which is the
   * answer at least as often as it is noise: 2021 HL Q1 asks what a program
   * prints and the scheme states "7 3" and "6 8".
   *
   * THREE CARDS WERE REMOVED and this is the record of them:
   *   cs-2022-hl-q14-a-i and cs-2022-hl-q14-b-i -- the scheme states one
   *     thing under each of these parts, "Each correct pass", and that is a
   *     credit rule. The cards were carrying it as the answer, which tells a
   *     student nothing about what a correct pass is;
   *   cs-2025-hl-q13-b-iv -- with the indices corrected the card selects the
   *     scheme's real sixth point, and that point does not trace back to the
   *     scheme text because the reader glued a credit rule onto its end. The
   *     provenance gate refusing it is the gate working. */
  /* 2026-08-30 (same day): 193/116 -> 194/116, coverage 367/484 -> 369/484.
   * A card citing a whole question no longer presents its parts' separate
   * answers as ALTERNATIVES to one another. That said "five marks for any one
   * of these", and 2022 OL Q5 was offering "3" -- the index part (a) asks for
   * -- as an alternative to the three limitations of linear search that (b)
   * asks for. Those cards now use the new `questionTotal` tariff: one row per
   * point, no per-row value, and the question's own printed total. Nothing was
   * removed. */
  /* 2026-08-30 (same day): 194/116 -> 202/118, coverage 369/484 -> 382/484.
   * A question owns the paper from its own heading to the NEXT question's,
   * and that often runs over the page: 2021 HL Q13 prints "This question
   * continues on the next page". Matching only pages that CARRY the heading
   * missed all of that, so nine questions had no figure and could not be
   * carded. Its figure still comes from the page carrying its heading, which
   * is where the paper prints the stimulus the question is built on -- taking
   * one from a later page would put one part's listing on another's card.
   * Nothing was removed. */
  /* 2026-08-30 (same day): 202/118 -> 207/119, coverage 382/484 -> 388/484.
   * Six more asks file under a syllabus topic. Each addition to the taxonomy
   * names the learning outcome it rests on: 2.11 "the different components
   * within a computer" reaches a solid state drive, 2.16 lists "array" among
   * the data types and the papers index and slice one without ever using the
   * word, 3.2 "create a basic relational database" is where a foreign key
   * lives, 1.20 "assign roles and responsibilities within a team" is where a
   * project manager does, and 3.8 is "develop a model that will allow
   * different scenarios to be tested". Nothing was removed. */
  /* 2026-08-30 (same day): 207/119 -> 209/127, coverage 388/484 -> see below.
   * The reader sweeps the page's FURNITURE into a question block: a bare
   * "Figure 3" at the end is the caption of the picture printed beside the
   * ask, "Section B Long Questions 76 marks" is the banner of the section
   * that starts underneath, and "This question continues on the next page" is
   * an instruction about the paper. Those parts were flagged as unreviewed
   * because the text stopped without punctuation, which is exactly what a
   * caption swept onto the end looks like. The strip is self-checking: it is
   * taken only where what remains still ends like a sentence. Nothing was
   * removed. */
  ['computer-science:higher', CS_HIGHER, 209, '1030050a22b237ea5ab74477d630b55d18620313c352fe167eb91691ae933abd'],
  ['computer-science:ordinary', CS_ORDINARY, 127, '15c1f77f5c96c66290a8f9d59845a12aa4c851a8b5177410f08a651146332731'],
  ['construction-studies:higher', CONS_HIGHER, 255, 'b74a39fd589f1082d6378190aee778d528eff0968d7af0ee9144525f2e40d57b'],
  ['construction-studies:ordinary', CONS_ORDINARY, 250, 'f56985e32cc1f02a2e2f7a7eb300a44646b75cf3604a12b5a478bde2a520d2da'],
  /* 2026-08-30: Engineering opened at 66/4, covering 171 of its 806 asks.
   *
   * Same day, 66/4 -> 47/10 and 171 asks -> 101. THIRTY-TWO CARDS WERE
   * REMOVED, and this is the record of it. Twenty-one of them pointed at a
   * picture they did not carry — "Identify the hybrid vehicle configuration
   * shown opposite", with nothing opposite — which is the very defect this
   * bank was asked to sweep out of the other ten subjects. They survived
   * because the authoring guard tested the LEAF's wording while lib builds a
   * whole-question card from the key's ask with every child joined on, so the
   * reference arrived from a child the guard never read. The finished card is
   * now tested with card lint's own condition instead of an approximation of
   * it.
   *
   * The count comes back when Engineering gets a figure pass: those questions
   * print the picture, nothing has cropped it yet, and a card carrying the
   * crop is no longer a ghost. Ordinary rose 4 -> 10 in the same pass from
   * the provenance and sentence-splitting fixes. */
  // 2026-08-31: 48 -> 65. The scheme reader learned three things the Ordinary
  // and Higher tariff tables had always said and it had not read: a part's
  // rule may run over several lines and only the last carries the total
  // ("Three parts @ 3 marks" + "Three parts @ 2 marks (15)" is 15, not 6); the
  // rule may be written with its own verb in front ("Explain any two @ 7
  // marks"), which is how 2023 Ordinary Level writes every one of them; and a
  // marker is separated from its rule by a dash, which had been defeating the
  // parse of the FIRST line of every multi-line rule. 289 priced parts -> 318.
  // Two cards were REMOVED, both of them shipping page furniture as a marking
  // point: eng-2022-hl-q5-b, whose entire 18-mark answer was "Page 17", and
  // eng-2023-hl-q1-j, which paid 2 of its 5 marks for "Page 8".
  ['engineering:higher', ENG_HIGHER, 65, '7df14249e8d4802c9f32ea928a6a3e20aca67a64ed23b337290eea7c6eea0463'],
  // 2026-08-31: 10 -> 21, same reader work as Higher above. One card REMOVED:
  // eng-2021-ol-q7-c-ii asked for the electronic symbol of each component
  // named and answered "of round bars or internal diameters of holes", which
  // is a fragment of the vernier caliper answer from another part entirely.
  // 2026-08-31: 10 -> 21, same reader work as Higher above. One card REMOVED:
  // eng-2021-ol-q7-c-ii asked for the electronic symbol of each component
  // named and answered "of round bars or internal diameters of holes", which
  // is a fragment of the vernier caliper answer from another part entirely.
  ['engineering:ordinary', ENG_ORDINARY, 21, 'ebad4215e07a526701bb89c5315225e3eba52f0684e626adb0f94d706f5b33fb'],
] as const;

const identityHash = (cards: readonly { id: string }[]) => createHash('sha256')
  .update(cards.map((card) => card.id).sort().join('\n'))
  .digest('hex');

describe('Mark Bank card preservation', () => {
  it.each(decks)('%s retains its complete stable card set', (name, cards, count, hash) => {
    expect(cards.length, `${name}: card count changed`).toBe(count);
    expect(new Set(cards.map((card) => card.id)).size, `${name}: duplicate card IDs`).toBe(count);
    expect(identityHash(cards), `${name}: a card ID was removed or replaced`).toBe(hash);
  });

  it('protects the complete current bank', () => {
    expect(decks.reduce((total, [, cards]) => total + cards.length, 0)).toBe(7873);
  });
});
