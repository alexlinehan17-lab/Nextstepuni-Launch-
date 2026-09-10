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
import { CARDS as CONS_HIGHER } from '../components/MarkBank/cards/construction-studies/higher';
import { CARDS as CONS_ORDINARY } from '../components/MarkBank/cards/construction-studies/ordinary';
import { CARDS as ENGLISH_HIGHER } from '../components/MarkBank/cards/english/higher';
import { CARDS as ENGLISH_ORDINARY } from '../components/MarkBank/cards/english/ordinary';
import { CARDS as IRISH_HIGHER } from '../components/MarkBank/cards/irish/higher';
import { CARDS as IRISH_ORDINARY } from '../components/MarkBank/cards/irish/ordinary';
import { CARDS as ART_HIGHER } from '../components/MarkBank/cards/art/higher';
import { CARDS as ART_ORDINARY } from '../components/MarkBank/cards/art/ordinary';
import { CARDS as GEOGRAPHY_HIGHER } from '../components/MarkBank/cards/geography/higher';
import { CARDS as GEOGRAPHY_ORDINARY } from '../components/MarkBank/cards/geography/ordinary';
import { CARDS as COMPUTER_SCIENCE_HIGHER } from '../components/MarkBank/cards/computer-science/higher';
import { CARDS as COMPUTER_SCIENCE_ORDINARY } from '../components/MarkBank/cards/computer-science/ordinary';
import { CARDS as ENGINEERING_HIGHER } from '../components/MarkBank/cards/engineering/higher';
import { CARDS as ENGINEERING_ORDINARY } from '../components/MarkBank/cards/engineering/ordinary';
import { CARDS as RE_HIGHER } from '../components/MarkBank/cards/religious-education/higher';
import { CARDS as RE_ORDINARY } from '../components/MarkBank/cards/religious-education/ordinary';
import { CARDS as LCVP_COMMON } from '../components/MarkBank/cards/lcvp/common';
import { CARDS as HISTORY_HIGHER } from '../components/MarkBank/cards/history/higher';
import { CARDS as HISTORY_ORDINARY } from '../components/MarkBank/cards/history/ordinary';
import { CARDS as TECHNOLOGY_HIGHER } from '../components/MarkBank/cards/technology/higher';
import { CARDS as TECHNOLOGY_ORDINARY } from '../components/MarkBank/cards/technology/ordinary';
import { CARDS as FRENCH_HIGHER } from '../components/MarkBank/cards/french/higher';
import { CARDS as FRENCH_ORDINARY } from '../components/MarkBank/cards/french/ordinary';
import { CARDS as GERMAN_HIGHER } from '../components/MarkBank/cards/german/higher';
import { CARDS as GERMAN_ORDINARY } from '../components/MarkBank/cards/german/ordinary';
import { CARDS as SPANISH_HIGHER } from '../components/MarkBank/cards/spanish/higher';
import { CARDS as SPANISH_ORDINARY } from '../components/MarkBank/cards/spanish/ordinary';
import { CARDS as ITALIAN_HIGHER } from '../components/MarkBank/cards/italian/higher';
import { CARDS as ITALIAN_ORDINARY } from '../components/MarkBank/cards/italian/ordinary';
import { CARDS as RUSSIAN_HIGHER } from '../components/MarkBank/cards/russian/higher';
import { CARDS as RUSSIAN_ORDINARY } from '../components/MarkBank/cards/russian/ordinary';
import { CARDS as JAPANESE_HIGHER } from '../components/MarkBank/cards/japanese/higher';
import { CARDS as JAPANESE_ORDINARY } from '../components/MarkBank/cards/japanese/ordinary';
import { CARDS as POLISH_HIGHER } from '../components/MarkBank/cards/polish/higher';
import { CARDS as POLISH_ORDINARY } from '../components/MarkBank/cards/polish/ordinary';
import { CARDS as PORTUGUESE_HIGHER } from '../components/MarkBank/cards/portuguese/higher';
import { CARDS as PORTUGUESE_ORDINARY } from '../components/MarkBank/cards/portuguese/ordinary';
import { CARDS as ROMANIAN_HIGHER } from '../components/MarkBank/cards/romanian/higher';
import { CARDS as DUTCH_HIGHER } from '../components/MarkBank/cards/dutch/higher';
import { CARDS as LITHUANIAN_HIGHER } from '../components/MarkBank/cards/lithuanian/higher';
import { CARDS as LITHUANIAN_ORDINARY } from '../components/MarkBank/cards/lithuanian/ordinary';
import { CARDS as LATVIAN_HIGHER } from '../components/MarkBank/cards/latvian/higher';
import { CARDS as CZECH_HIGHER } from '../components/MarkBank/cards/czech/higher';
import { CARDS as ARABIC_HIGHER } from '../components/MarkBank/cards/arabic/higher';
import { CARDS as ARABIC_ORDINARY } from '../components/MarkBank/cards/arabic/ordinary';
import { CARDS as AGREEK_HIGHER } from '../components/MarkBank/cards/ancient-greek/higher';
import { CARDS as AGREEK_ORDINARY } from '../components/MarkBank/cards/ancient-greek/ordinary';
import { CARDS as MGREEK_HIGHER } from '../components/MarkBank/cards/modern-greek/higher';
import { CARDS as CLAS_HIGHER } from '../components/MarkBank/cards/classical-studies/higher';
import { CARDS as CLAS_ORDINARY } from '../components/MarkBank/cards/classical-studies/ordinary';
import { CARDS as LATIN_HIGHER } from '../components/MarkBank/cards/latin/higher';
import { CARDS as LATIN_ORDINARY } from '../components/MarkBank/cards/latin/ordinary';
import { CARDS as APPLIED_MATHS_HIGHER } from '../components/MarkBank/cards/applied-maths/higher';
import { CARDS as APPLIED_MATHS_ORDINARY } from '../components/MarkBank/cards/applied-maths/ordinary';
import { CARD_ID_ALIASES } from '../components/MarkBank/cardAliases';

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
  ['chemistry:ordinary', CHEM_ORDINARY, 380, 'f15304f5ef306c5d0002c1cacd3ce85f3d8e83ccece53772a739f7a2d9460eb8'],
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
  /* 2026-09-03: restored phys-2021-hl-q13a-v. Its valid card content had been
   * rejected only because a non-shipping author note documented corrupt OCR
   * from the preceding part. Notes are now excluded from the shipped-text
   * glyph gate; no prior Physics ID was removed or replaced. */
  ['physics:higher', PHYS_HIGHER, 570, '9712686995c6b73f612200773855e1054ae6a5ec13ceaf5a82427934ea590007'],
  ['physics:ordinary', PHYS_ORDINARY, 563, '67dee7bc4ede4f829b03a569374b5cf94de35dd92bed3af580263667cf2a5f40'],
  ['agricultural-science:higher', AGSCI_HIGHER, 438, '31e25662626e35ca1db55e96e1cdfe0492648666c6cd35365f2c1e6d92c35f6a'],
  ['agricultural-science:ordinary', AGSCI_ORDINARY, 431, '2dbd6e7635bb73941a16773ce9d3c654741a863280c002f783fc45cd0d7e8dbd'],
  ['business:higher', BUSINESS_HIGHER, 272, 'a61655818cee2ce61307eb08fe6dad282193791674b4e5e8a893e203b64af976'],
  ['business:ordinary', BUSINESS_ORDINARY, 334, '6d62fbc00d4b0f4c411cd23c17d76ddaa63cb066325bb2974c881c8b81073b18'],
  ['home-economics:higher', HOME_EC_HIGHER, 283, 'a6b8f1f2ff2f0a3da489b38f0a6b4b8fd1476e227ae23cc6753695e4e4aa53b9'],
  ['home-economics:ordinary', HOME_EC_ORDINARY, 266, '736a4e2f0ff0ee152398eab18b9096e2d8b00b8e8b9561d85944b469aceeffd7'],
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
  ['construction-studies:higher', CONS_HIGHER, 255, 'b74a39fd589f1082d6378190aee778d528eff0968d7af0ee9144525f2e40d57b'],
  ['construction-studies:ordinary', CONS_ORDINARY, 250, 'f56985e32cc1f02a2e2f7a7eb300a44646b75cf3604a12b5a478bde2a520d2da'],
  /* 2026-08-30: English 19/0 -> 210/450. Every independently selectable
   * response on all twenty 2021-2025 Higher and Ordinary papers is carded.
   * This includes all three OL prescribed-poetry Q2 alternatives per poem;
   * compulsory linked parts remain together but retain separate PCLM grids.
   * 205 cards open the real paper passage or poem in the source reader. */
  ['english:higher', ENGLISH_HIGHER, 210, '231477c3f869811a39610398ed61ff14a4f3e5f087ebaa053a5d1b8daabc3df0'],
  ['english:ordinary', ENGLISH_ORDINARY, 440, '9e667c2b7181e951fcb7b875ab7a0fb009f5db1389d75d89131dacebbc90994f'],
  /* 2026-08-30: complete Irish written-paper launch. All 400 selectable
   * responses across 2021–2025 Higher and Ordinary are present, including
   * listening audio and the real PDF pages for passages and printed poems. */
  ['irish:higher', IRISH_HIGHER, 215, '47cc840774127e9368d60a0965951e7fc39bd3a2a02c1d9fddd11738cc18255b'],
  ['irish:ordinary', IRISH_ORDINARY, 185, '34e18ac058529e14ac0337a030264ab74329f72dabdd0dee8d9b912107dd343c'],
  /* 2026-08-30: complete Art written-paper launch. All 462 separately marked
   * tasks and finite printed answer routes across 2021–2025 are present. This
   * includes all ten heading pairs for 2025 OL Q4(a), while keeping Section
   * B/C holistic descriptor essays intact and splitting only at published
   * task and mark boundaries. */
  ['art:higher', ART_HIGHER, 222, '720e68e98f7d3254af15e7834a3fdbd6098ca319d00ccce82fa570d411fb15a9'],
  ['art:ordinary', ART_ORDINARY, 240, 'fcf4b64bd5bad786856087dfc8cefdc133233a12a74516166205d1f8898e193b'],
  /* 2026-08-31: Geography now covers 2021-2026. All 563 answerable base tasks
   * are present, with every finite route expanded into a usable card. The 85
   * historical tasks whose separate OS map/aerial source is not yet held stay
   * census-held; every 2026 task ships with its complete official source set.
   * The 2021 HL Q6C choose-two audit also adds its nine missing combinations
   * while retaining the original card id for saved-progress continuity. */
  ['geography:higher', GEOGRAPHY_HIGHER, 445, '7768fb37a748daf2cda31ae9f8c97b6bb632b44f1243332ce5edfac06361bacc'],
  ['geography:ordinary', GEOGRAPHY_ORDINARY, 309, '350dc90c7120b0efe314d07115ceb88f3ea49a55d79a55b48b819c188068cee7'],
  /* Recovered from the completed Computer Science authoring branch and rebuilt
   * through the same source, tariff, figure and structural guards as every
   * other subject. */
  ['computer-science:higher', COMPUTER_SCIENCE_HIGHER, 209, '1030050a22b237ea5ab74477d630b55d18620313c352fe167eb91691ae933abd'],
  ['computer-science:ordinary', COMPUTER_SCIENCE_ORDINARY, 127, '15c1f77f5c96c66290a8f9d59845a12aa4c851a8b5177410f08a651146332731'],
  /* Engineering landed after this test's previous update. Enrol it explicitly
   * so a later regeneration cannot silently omit or replace any of its cards. */
  ['engineering:higher', ENGINEERING_HIGHER, 313, '9458ea8b7627cb8001cc6917436c2b582140ffce954b6c7d580809d6eb92c233'],
  ['engineering:ordinary', ENGINEERING_ORDINARY, 153, '05788a0b5351fd9797a97f8f01757544ebeb725d164e7b79d4b2231c71eaa379'],
  /* 2026-09-10: Religious Education, the sixteenth subject, lands complete —
   * 288 cards against the 288 asks its ten papers print, every one of them
   * added and none replacing anything. Nothing in any other deck moved. */
  ['religious-education:higher', RE_HIGHER, 135, '9a6117ccc7be90492858b10d071528bbfee33de42ec8a368c51d6e2c76c596f3'],
  ['religious-education:ordinary', RE_ORDINARY, 153, 'ebad0ef90313b7b75bfb75aecca5c93c5372ee0745f58ffc407481bf74ee5569'],
  /* 2026-09-10: LCVP's Link Modules enrolled, 321 cards, NONE removed or
   * replaced — it is a new subject and this is its first baseline. It ships
   * as ONE deck because the paper is common level: there is no Higher or
   * Ordinary sibling to pair it with, which is why it appears here once. */
  ['lcvp:common', LCVP_COMMON, 314, '2f0310a433d9736ccf8a4a7a31a816de16abeaac995c881848fc3c2f827d82d2'],
  /* Technology is the sixteenth subject and the first to be authored end to
   * end from a paper-anchored census in one pass. Enrolled explicitly so a
   * later regeneration cannot silently omit or replace any of its cards. */
  ['technology:higher', TECHNOLOGY_HIGHER, 357, 'ae8ad195ca373cef2d8923c83a848613215aa9413c2cd7bda7d6796c4d64370c'],
  ['technology:ordinary', TECHNOLOGY_ORDINARY, 359, '43e668303c30fef288ee0e09d8b5d3384105085e23cc10d288903ed29d1ab687'],
  /* 2026-09-10: History, the nineteenth subject, and the first carded
   * against TWO papers per sitting — a candidate sits either the Later
   * Modern or the Early Modern field of study, and both are now in the
   * corpus. Every card is new; none replaces anything. The Ordinary deck
   * is much the larger because Ordinary is where this paper states its
   * answers: its Part A prints five priced one-line answers per topic,
   * while Higher answers everything outside the documents question with a
   * marking ceiling and no content. */
  ['history:higher', HISTORY_HIGHER, 80, '6ab586c6a2d83048d82aab13f5c7171ebcdf02fe61532a697c39556adaa0d657'],
  ['history:ordinary', HISTORY_ORDINARY, 669, '7c781ff7d97974fe5679d021cbdf85299542783432fda549997830c5c6bcfdf9'],
  /* French is the first modern language carded, and the first subject whose
   * cards carry the passage they quote: every reading card binds the pages of
   * its own comprehension in the QUESTION paper. New subject, first baseline —
   * nothing removed and nothing replaced. */
  ['french:higher', FRENCH_HIGHER, 110, '086e17874bb4922e9b80d358f4a666c6b3383c04004f21371614476fb91df9fc'],
  ['french:ordinary', FRENCH_ORDINARY, 150, 'aab034b970b7b0313a2bb4f16da64542b2fce2482b0299e71c10ea22b111581e'],
  /* German is the second modern language carded and the twenty-second subject.
   * Its cards carry the TEXT they quote, as French's do, and each states the
   * language its own answer must be in — which differs WITHIN one reading
   * comprehension, so it cannot ride on the subject. New subject, first
   * baseline — nothing removed and nothing replaced. */
  ['german:higher', GERMAN_HIGHER, 111, '1e7b9a40d87f6aabc6a930548f04a6ecbc17c3655d973fa5ab4b75d59298672e'],
  ['german:ordinary', GERMAN_ORDINARY, 153, '1bec5e64b16fa1e80235f02dbe51f50151dabb358213a2e1265a55f5515e79d3'],
  /* Italian is the second modern language and the twenty-first subject. Every
   * card is new; none replaces anything. Like French, every reading card
   * carries the printed matter it is answered from — a passage, an
   * advertisement or a literary extract, bound to the page of the question
   * paper facing its own questions. */
  ['italian:higher', ITALIAN_HIGHER, 172, '28bebc58e0f4a6691c5d069624a0fd36fe9aced034bc8a1d03f321d54422fb64'],
  ['italian:ordinary', ITALIAN_ORDINARY, 178, 'cb669b9c536926731311350530b448e7a3d24f940e1f46bea180d351935ba9d8'],
  /* Applied Maths is the seventeenth subject and the first to straddle a
   * syllabus break: 2021-2022 are the outgoing mechanics course and 2023-2025
   * the specification first examined in 2023. Enrolled explicitly so a later
   * regeneration cannot silently omit or replace any of its cards. */
  ['applied-maths:higher', APPLIED_MATHS_HIGHER, 130, '5c8f36ba0f4214eee4269d22bcd3d20ada53f1a33820c36c0e873fe5b5afac72'],
  ['applied-maths:ordinary', APPLIED_MATHS_ORDINARY, 145, '1e39bd494a3304e1ec0b1153834dba6d7bf186d7f90ec05055024d40b869b570'],
  /* Spanish is the second modern language carded, and the first subject whose
   * cards bind a source printed in a DIFFERENT booklet: its Higher Section B
   * article is a two-page loose sheet with its own SEC file id, and those 80
   * cards carry it rather than the question paper. New subject, first baseline
   * — nothing removed and nothing replaced. */
  ['spanish:higher', SPANISH_HIGHER, 204, '2dc8d8c0e05c628ecf86b1d0fe8cd99a78460d37d47009606e3005ee8dfce5bb'],
  ['spanish:ordinary', SPANISH_ORDINARY, 143, 'f42cb5ebc5dbe2a1e959e5a71c4a72d3864eabcdc84789481716a2e98c7f6be1'],
  /* Russian is the fifth modern language and the twenty-second subject. Every
   * card is new; none replaces anything. Like French and Italian, every
   * reading card carries the printed matter it is answered from, bound to the
   * pages of the question paper it was printed on; unlike them, fourteen of
   * its cards are answered in RUSSIAN rather than in English or Irish and say
   * so on their face. */
  ['russian:higher', RUSSIAN_HIGHER, 83, '28a15e33be6d11b7077181773cc7611e2681f8c34c057fa8361077b386491392'],
  ['russian:ordinary', RUSSIAN_ORDINARY, 116, '7a1246357f052dda6f3e337e5c05b1a7df6ce1ec213f8d3eb9cb648576fa8e49'],
  /* Japanese is the twenty-second subject and the first set in a non-Latin
   * script. Every card is new; none replaces anything. Two things are true of
   * it and of no deck before it: a card may carry KANA AND KANJI, with the
   * SEC's own furigana folded into the line in brackets (ja_text.py), and the
   * answer language changes inside one question, so every card states which
   * language its answer must be in. */
  ['japanese:higher', JAPANESE_HIGHER, 339, 'a06378e0d982a6331919f663c9335bc1e9099560170ed6c98908d7b0108fc510'],
  ['japanese:ordinary', JAPANESE_ORDINARY, 261, '460f3973e9d10e7a1f5a2797fb68d0c82530b3cb70bd2eadeaec015a4a807392'],
  /* Polish is the twenty-fourth subject and the first NON-CURRICULAR EU
   * LANGUAGE in the bank — a subject with no Leaving Certificate syllabus,
   * examined against the language itself. Every card is new; none replaces
   * anything. Two things are true of it and of no deck before it: the
   * examination was REBUILT in 2022, from one 70-mark booklet sat at a single
   * level to Section A Reading and Section B Written Production at two levels
   * with a Listening Comprehension Test beside them, so one deck holds both
   * papers; and its true/false answers are read from the COLUMN the scheme's
   * tick stands in, which is the only place that answer is written down. */
  ['polish:higher', POLISH_HIGHER, 115, '3cf1b2909433bcb50931d0d7162ff44fa529ca44752a16cc50dcddcad6ffe6a5'],
  ['polish:ordinary', POLISH_ORDINARY, 122, '7b75f4690d22e1070ed66cb946f5eeeba80f3b83f73f4bc774cf9fd9d649083b'],
  /* Portuguese is the twenty-sixth subject and the second NON-CURRICULAR EU
   * LANGUAGE. Every card is new; none replaces anything. It is the first deck
   * whose two halves are priced by DIFFERENT DOCUMENTS: the 2022-2025 cards
   * take their tariff from the marking scheme, which prices every ask, and the
   * 2021 cards take it from the QUESTION PAPER's right-hand margin, because
   * the scheme of that examination prints answers with no marks anywhere in
   * it. Both are printed; neither is inferred. */
  ['portuguese:higher', PORTUGUESE_HIGHER, 94, 'af660d48d9959b5d40dffc4ea99d293223e5c62c3f3d93d95cc131ef6c386701'],
  ['portuguese:ordinary', PORTUGUESE_ORDINARY, 79, '116e68ce1fdda8fd35a294e16e7f0df8b6d71906963ea88fede497c925dfc016'],
  /* Romanian and Dutch are the twenty-seventh and twenty-eighth subjects, and
   * the first two whose whole deck is priced by the QUESTION PAPER: their
   * marking schemes print answers with no marks anywhere in them, and the
   * tariff for every card here is the "(5 puncte)" or "(1 punt)" the paper
   * sets in its own right-hand margin. Every card is new; none replaces
   * anything. Both are sat at ONE level, so each ships a Higher deck only. */
  ['romanian:higher', ROMANIAN_HIGHER, 50, 'f48554eeb516fd17cc9b89520eaf76ebe3e46c564ac0b41d0225653e225216ba'],
  ['dutch:higher', DUTCH_HIGHER, 42, '62df13c5837ef5cabcd391e637a318fc25b106bcdf90744ffdddc4d10d6a70c4'],
  /* Lithuanian, added 10 September 2026 — the second NON-CURRICULAR EU
   * LANGUAGE, and the deepest corpus in the bank: twenty-two sittings from
   * 2010 to 2026, because that is what the SEC published for it and every one
   * of them is the same examination. Every card is new; none replaces
   * anything. Its 306 cards cover 306 of the 826 asks its papers print and
   * the other 520 are excluded with the scheme's own printed line — 280
   * listening asks the recording answers, 99 written tasks answered by a
   * marking grid or a model paragraph, 35 matching tasks whose answer is a
   * letter naming a box the card cannot carry, and the rest named in
   * scripts/markbank/authoring/exclusions/lithuanian.json. It is the first
   * deck whose text needed a repair map derived from the LANGUAGE rather than
   * from a font: two of its schemes embed a subset nothing else in the bank
   * shares, and lt_glyphs.py settles their glyphs by which words they make. */
  ['lithuanian:higher', LITHUANIAN_HIGHER, 163, '8492d0ed851e7023f0daae360420bc38e6aef456cfe45b7f62efc30c8e86fba3'],
  ['lithuanian:ordinary', LITHUANIAN_ORDINARY, 143, '60d9e670bf51d7ff41846017985015d94031954562e82edeb0e6ace4b0d9e0d8'],
  /* Latvian and Czech, added 10 September 2026 on Lithuanian's reader — the
   * third and fourth non-curricular EU languages. Every card is new; none
   * replaces anything. They are the SMALLEST decks in the bank and that is
   * the measurement, not a shortfall: their seventeen sittings each print the
   * old examination whose scheme answers five of its six reading questions,
   * its commentary and its essay with continuous model prose and prices
   * nothing inside any of it. What it does price is the vocabulary task, once
   * on the question and not on its parts — so those card as `questionTotal`,
   * one card per sitting carrying the SEC's gloss for each of five
   * expressions, and every other ask is excluded with the printed line that
   * refuses it. Latvian covers 68 of its 218 paper asks and Czech 75 of 219,
   * with nothing open in either. */
  ['latvian:higher', LATVIAN_HIGHER, 20, '03f3c7fdefa700a5437e95efc5bc7ab01f544851a497f4c129f2027f9f24a957'],
  ['czech:higher', CZECH_HIGHER, 15, 'cf2e36d688faf72c658c8cb191fb3580e87ec1c934fd3a3017bdd0847a71ae56'],
  /* Classical Studies is the twenty-second subject, entered on a RE-MEASURE:
   * the bank had it recorded as rejected on a band grid that turns out to
   * belong to the Research Study Report, which is coursework, not the written
   * paper. Every card is new; none replaces anything. It is the second subject
   * to straddle a syllabus break — 2021-2022 are the ten-topic syllabus and
   * 2023-2025 the specification first examined in 2023 — and 271 of its cards
   * bind an official SEC source, most of them the accompanying Paper X of
   * photographs and images. */
  ['classical-studies:higher', CLAS_HIGHER, 240, 'c7ef8e6be63fdd3108213d5f94333eff67b067893036821eb3164bbedffe0c66'],
  ['classical-studies:ordinary', CLAS_ORDINARY, 276, '363ae6d0a26308e5c8b7459143bdbfa9c66c07f203c4125a03b67dc319ebd211'],
  /* Latin, added 10 September 2026 — the twenty-second subject, and the
   * seventh language. Every card is new; none replaces anything. Its 227
   * cards cover 237 of the 328 asks its eight papers print, and the 91 that
   * are not carded are excluded with the scheme's own printed line: every
   * TRANSLATION ask (the scheme prices the source text by segment and never
   * states a model answer) and every principal-parts and scansion ask (the
   * scheme prices them and never states them). 101 of its cards bind an
   * official SEC source — the Latin passage a comprehension is answered from,
   * or the plate pages a Question 5 photograph question is about. */
  ['latin:higher', LATIN_HIGHER, 145, '9062777f248fece7c2c345612d362a19bfd571f3461df962da78ba93b149a2c6'],
  ['latin:ordinary', LATIN_ORDINARY, 82, 'c6d74830e3497c5862cc9e9727ecd9a57bdb4d27d8ef43b87860378e63960a94'],
  /* Arabic is the twenty-third subject and the first written RIGHT TO LEFT.
   * Every card is new; none replaces anything. It cards two corners of a paper
   * that is otherwise marked by a Communication-and-Content grid: the reading
   * comprehension's multiple choice, whose option words are the paper's own,
   * and the whole of Part 3, Use of Language. Nothing about it was readable
   * until ara_text.py and ara_glyphs.py — see ARABIC.md — so a card ID here is
   * also a claim that the Arabic on it is the Arabic the SEC printed. */
  ['arabic:higher', ARABIC_HIGHER, 125, 'e28afb1be279b23f9180b61cd90115f0633c895049fef70c4e4cbd448366e301'],
  ['arabic:ordinary', ARABIC_ORDINARY, 125, 'e2ae63496b37a0f46053f3b96bffb7bb9a827e223508451dff6d8f62523e0c40'],
  /* Ancient Greek is Latin's sibling and the deepest corpus in the bank: 27
   * papers over fifteen years, 2010 to 2024. Every card is new; none replaces
   * anything. One thing is true of it and of no deck before it: every sitting
   * before 2023 sets its Greek in SPIonic, a pre-Unicode font embedded with no
   * ToUnicode map, so a card ID here is also a claim that the polytonic Greek
   * on it is the Greek the SEC printed (agr_text.py, and the audit it runs).
   * Its 383 cards cover 387 of the 758 asks its papers print; the 371 that are
   * not carded are excluded with the documents' own evidence — eleven sittings
   * for which the SEC published no scheme at all, and every translation ask,
   * whose scheme prices the SOURCE by segment and never states an answer. */
  ['ancient-greek:higher', AGREEK_HIGHER, 369, 'e42e8aed0c67f36ef470d5d75acae61736068cf28d40b6d190cd08a6a842fdc1'],
  ['ancient-greek:ordinary', AGREEK_ORDINARY, 14, 'd4d868a488b2671d8c104506674b32ef0aa33dc94a4e67974349a8b1b9132492'],
  /* Modern Greek is the second NON-CURRICULAR EU LANGUAGE in the bank and the
   * first subject in it examined at ONE level: the SEC's file letter is 'A' in
   * all sixteen sittings and there is no Ordinary paper to card. Every card is
   * new; none replaces anything. Its 79 cards cover 79 of the 142 asks its
   * papers print, and the 63 that are not carded are the two written-production
   * groups, the two sittings on which neither document states a per-question
   * tariff, and 2015, whose scheme returns no Greek at all from its text
   * layer. It is the first deck whose questions AND answers are both in the
   * language examined, so every row says so on its face. */
  ['modern-greek:higher', MGREEK_HIGHER, 79, 'd41a4a9affec25b7d9da9fac3eb514825d2d1d7da9c087c9c51bc786ee090ac3'],
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
    // 10,495 before this session, plus sixteen subjects carded in six waves:
    // Religious Education 288, LCVP 314, Technology 716, History 749,
    // French 260, Applied Maths 275, German 264, Spanish 347, Italian 350,
    // Russian 199, Japanese 600, Classical Studies 516, Latin 227,
    // Portuguese 173, Romanian 50 and Dutch 42.
    expect(decks.reduce((total, [, cards]) => total + cards.length, 0)).toBe(16_352);
    // Russian 199, Japanese 600, Classical Studies 516 and Latin 227.
    // Lithuanian 306, Latvian 20 and Czech 15 in a sixth wave:
    // 16,087 + 306 + 20 + 15.
    expect(decks.reduce((total, [, cards]) => total + cards.length, 0)).toBe(16_428);
    // Russian 199, Japanese 600, Classical Studies 516 and Polish 237.
    // Russian 199, Japanese 600, Classical Studies 516 and Arabic 250.
    // Polish 237, Arabic 250, Ancient Greek 383 and Modern Greek 79.
    expect(decks.reduce((total, [, cards]) => total + cards.length, 0)).toBe(16_549);
  });

  it('preserves every consolidated card identity through an explicit progress alias', () => {
    const liveIds = new Set(decks.flatMap(([, cards]) => cards.map(card => card.id)));
    expect(Object.keys(CARD_ID_ALIASES)).toHaveLength(34);
    for (const [oldId, canonicalId] of Object.entries(CARD_ID_ALIASES)) {
      expect(liveIds.has(oldId), `${oldId} should be withdrawn, not scheduled twice`).toBe(false);
      expect(liveIds.has(canonicalId), `${oldId} aliases missing canonical ${canonicalId}`).toBe(true);
    }
    const preNewSubjectCards = decks
      .filter(([name]) => !name.startsWith('computer-science:')
        && !name.startsWith('engineering:')
        && !name.startsWith('religious-education:')
        && !name.startsWith('lcvp:')
        && !name.startsWith('technology:')
        && !name.startsWith('history:')
        && !name.startsWith('french:')
        && !name.startsWith('german:')
        && !name.startsWith('applied-maths:')
        && !name.startsWith('spanish:')
        && !name.startsWith('italian:')
        && !name.startsWith('russian:')
        && !name.startsWith('japanese:')
        && !name.startsWith('classical-studies:')
        && !name.startsWith('latin:')
        && !name.startsWith('polish:')
        && !name.startsWith('portuguese:')
        && !name.startsWith('romanian:')
        && !name.startsWith('dutch:')
        && !name.startsWith('lithuanian:')
        && !name.startsWith('latvian:')
        && !name.startsWith('czech:')
        && !name.startsWith('arabic:')
        && !name.startsWith('ancient-greek:')
        && !name.startsWith('modern-greek:'))
      .reduce((total, [, cards]) => total + cards.length, 0);
    expect(preNewSubjectCards + Object.keys(CARD_ID_ALIASES).length).toBe(9_727);
  });

  it('adds 2026 Geography and the Q6C routes without replacing a prior card id', () => {
    const addedHigherRoutes = new Set(GEOGRAPHY_HIGHER
      .filter(card => card.id.startsWith('geography-2021-hl-p2-q6c-'))
      .map(card => card.id));
    expect(addedHigherRoutes.size).toBe(9);
    expect(identityHash(GEOGRAPHY_HIGHER.filter(card =>
      card.year <= 2025 && !addedHigherRoutes.has(card.id))))
      .toBe('db478deb519637edeacce1fd96db3cf50e893e7cf1e8a72cc28c40694b0281ea');
    expect(identityHash(GEOGRAPHY_ORDINARY.filter(card => card.year <= 2025)))
      .toBe('2f6f346262b91ac1385b55c194b7940d927c207403fa00c0ada08e087fd227a9');
  });

  it('adds the Art choose-two routes without replacing any existing card id', () => {
    const correctionIds = new Set(ART_ORDINARY
      .filter(card => card.questionRef.startsWith('2025 OL Q4(a)')
        && card.id !== 'art-2025-ol-q4-a')
      .map(card => card.id));
    expect(correctionIds.size).toBe(9);
    expect(identityHash(ART_ORDINARY.filter(card => !correctionIds.has(card.id))))
      .toBe('e5403f6e685e0133ad94ef321f97a77f96127c2ee3570395e00662d7719ddbd5');
  });
});
