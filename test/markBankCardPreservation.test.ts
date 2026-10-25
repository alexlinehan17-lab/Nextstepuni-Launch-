import { CONSTRUCTION_2015_HIGHER_REVIEWED_IDS, CONSTRUCTION_2015_ORDINARY_REVIEWED_IDS } from './fixtures/construction2015Reviewed';
import { CONSTRUCTION_2026_HIGHER_REVIEWED_IDS, CONSTRUCTION_2026_ORDINARY_REVIEWED_IDS } from './fixtures/construction2026Reviewed';
import { CONSTRUCTION_2025_HIGHER_ADDED_IDS, CONSTRUCTION_2025_ORDINARY_ADDED_IDS } from './fixtures/construction2025Reviewed';
import { CONSTRUCTION_2024_HIGHER_ADDED_IDS, CONSTRUCTION_2024_ORDINARY_ADDED_IDS } from './fixtures/construction2024Reviewed';
import { CONSTRUCTION_2023_HIGHER_ADDED_IDS, CONSTRUCTION_2023_ORDINARY_ADDED_IDS } from './fixtures/construction2023Reviewed';
import { CONSTRUCTION_REVIEWED_HIGHER_ADDED_IDS, CONSTRUCTION_REVIEWED_ORDINARY_ADDED_IDS } from './fixtures/constructionReviewedPapers';
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
import { FRENCH_WRITING_CARDS } from '../components/MarkBank/cards/french/writing';
import { FRENCH_LISTENING_CARDS } from '../components/MarkBank/cards/french/listening';
import { FRENCH_CLOZE_CARDS } from '../components/MarkBank/cards/french/cloze';
import { FRENCH_READING_CARDS } from '../components/MarkBank/cards/french/reading';
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
import { CARDS as POLITICS_HIGHER } from '../components/MarkBank/cards/politics-and-society/higher';
import { CARDS as POLITICS_ORDINARY } from '../components/MarkBank/cards/politics-and-society/ordinary';
import { CARDS as ACCOUNTING_HIGHER } from '../components/MarkBank/cards/accounting/higher';
import { CARDS as ACCOUNTING_ORDINARY } from '../components/MarkBank/cards/accounting/ordinary';
import { CARD_ID_ALIASES } from '../components/MarkBank/cardAliases';
import PE_FROZEN_MANIFEST from '../scripts/markbank/authored/physical-education.json';
import businessOriginals from '../scripts/markbank/authored/business.json';
import businessReviewed from '../components/MarkBank/cards/business/rubric-authored.json';
import businessRoutePools from '../components/MarkBank/cards/business/route-pools.json';
import { expandBusinessRoutePools } from '../components/MarkBank/cards/business/routes.mjs';
import agriculturalReview from '../scripts/markbank/authored/agricultural-science-reviewed-tasks.json';
import biologyReview from '../scripts/markbank/authored/biology-review-audit.json';
import publishedEnglishHigher from '../components/MarkBank/cards/english/published-higher.json';
import publishedEnglishOrdinary from '../components/MarkBank/cards/english/published-ordinary.json';

import { CARDS as BULGARIAN_HIGHER } from '../components/MarkBank/cards/bulgarian/higher';
import { CARDS as CROATIAN_HIGHER } from '../components/MarkBank/cards/croatian/higher';
import { CARDS as DANISH_HIGHER } from '../components/MarkBank/cards/danish/higher';
import { CARDS as ESTONIAN_HIGHER } from '../components/MarkBank/cards/estonian/higher';
import { CARDS as FINNISH_HIGHER } from '../components/MarkBank/cards/finnish/higher';
import { CARDS as HUNGARIAN_HIGHER } from '../components/MarkBank/cards/hungarian/higher';
import { CARDS as MANDARIN_CHINESE_HIGHER } from '../components/MarkBank/cards/mandarin-chinese/higher';
import { CARDS as MANDARIN_CHINESE_ORDINARY } from '../components/MarkBank/cards/mandarin-chinese/ordinary';
import { CARDS as SLOVAKIAN_HIGHER } from '../components/MarkBank/cards/slovakian/higher';
import { CARDS as SLOVENIAN_HIGHER } from '../components/MarkBank/cards/slovenian/higher';
import { CARDS as SWEDISH_HIGHER } from '../components/MarkBank/cards/swedish/higher';
import { CARDS as UKRAINIAN_HIGHER } from '../components/MarkBank/cards/ukrainian/higher';
import { CARDS as DCG_HIGHER } from '../components/MarkBank/cards/dcg/higher';
import { CARDS as DCG_ORDINARY } from '../components/MarkBank/cards/dcg/ordinary';
import { CARDS as PE_HIGHER } from '../components/MarkBank/cards/physical-education/higher';
import { CARDS as PE_ORDINARY } from '../components/MarkBank/cards/physical-education/ordinary';
const decks = [
  // 2026-10-07: new Politics corpus, 17 paper/scheme pairs visually reviewed.
  // No prior Politics IDs existed. All prior subject preservation checks and
  // zero-open/zero-orphan Politics reconciliation passed before this addition.
  // 2026-10-12: 272/814 -> 263/359, deliberately. Choice is not a route: the
  // 498 per-option and per-combination cards (286 for 2023 OL Q2(d) alone,
  // 126 for 2021 OL Q1(l)) rewrote the SEC question and flooded sessions, so
  // each of their 34 printed tasks is now ONE card. None of the 498 IDs was
  // ever on main (checked against origin/main 6652f80cc), so they are removed
  // rather than aliased; every one of the other 588 Politics cards is unchanged.
  ['politics-and-society:higher', POLITICS_HIGHER, 263, '6a1acd6ec5281c832c38795ba97751babef5c5a93aa7653a0d0d4b44f79a6bfe'],
  // Then 359 -> 360: 2021 OL Q1(f)'s printed options sit under two syllabus
  // topics (2.1 civil service; 5.5 NGOs and statutory bodies), so it is one
  // card per topic (AGENTS.md); the single branch-only q1-f ID is replaced.
  ['politics-and-society:ordinary', POLITICS_ORDINARY, 360, '0e1168ab9e3d9fcc06012554ce7ed77336e61b6d00d5f197ce331a3b15cf317b'],
  /* Biology: the 1,359 IDs shipped on main before the paper-by-paper review
   * (673 Higher / 686 Ordinary) are pinned here in the frozen form, as for
   * Business, Economics and the rest: every live 2021-2025 id the review did
   * not add, plus the bio- progress alias keys (frozenIds). The live decks and
   * the review's additions are pinned in 'adds the reviewed Biology sittings'.
   * The history of the live counts: */
  /* 2026-10-11: biology higher 673 -> 861. The 2026 Higher sitting is added
   * from a paper-by-paper review (bio_review_2026_hl.py): 184 tasks at the
   * scheme's own mark boundaries, 188 cards once Q12(c)(ii) and (iii) are
   * expanded into their three printed areas each. Nothing removed: the 673
   * cards from 2021-2025 keep their identity hash, pinned below. */
  /* 2026-10-12: biology higher 861 -> 928. The 2025 Higher sitting is
   * re-reviewed paper by paper (bio_review_2025_hl.py) and corrected in
   * place: all 106 shipped 2025 ids are kept (each mapped to the task it
   * was carding, its old fields recorded in biology-review-audit.json), and
   * the 67 tasks the old cards bundled or missed ship as new ids, one of
   * them (bio-2025-hl-q9-b-ii) an authored card the build had never shipped.
   * The frozen 2021-2025 identity hash is pinned below without them. */
  /* 2026-10-12: biology higher 928 -> 956. The 2024 Higher sitting is
   * re-reviewed the same way (bio_review_2024_hl.py): 134 of its 135 shipped
   * ids are kept (121 corrected, 13 verified), 29 tasks the old cards bundled
   * or missed ship as new ids, and bio-2024-hl-q8-b2, the second half of one
   * printed task the old cards cut in two, is withdrawn with a progress alias
   * to bio-2024-hl-q8-b1. The frozen hash below restores it. */
  /* 2026-10-12: biology higher 956 -> 1019. The 2023 Higher sitting is
   * re-reviewed the same way (bio_review_2023_hl.py): all 113 shipped ids are
   * kept (105 corrected, 8 verified) and 63 tasks the old cards bundled or
   * missed ship as new ids. bio-2023-hl-q14-b-ii-fig, an authored figure twin
   * the build never shipped, is withdrawn without an alias. */
  /* 2026-10-12: biology higher 1019 -> 1067. The 2022 Higher sitting is
   * re-reviewed the same way (bio_review_2022_hl.py): all 142 shipped ids are
   * kept (all corrected) and 48 tasks the old cards bundled or missed ship as
   * new ids. Two authored cards the build never shipped are withdrawn without
   * an alias. */
  /* 2026-10-13: biology higher 1067 -> 1078. The 2021 Higher sitting is
   * re-reviewed the same way (bio_review_2021_hl.py): all 177 shipped ids are
   * kept (168 corrected, 9 verified) and 11 tasks the old cards bundled or
   * missed ship as new ids. */
  /* 2026-10-13: biology higher 1078 -> 1228. The 2020 Higher sitting, never
   * carded before, is carded from a paper-by-paper review
   * (bio_review_2020_hl.py): 149 tasks, 150 cards once Q6(f) is split into
   * its two printed disorders. Every earlier id is unchanged. */
  /* 2026-10-14: biology higher 1228 -> 1376. The 2019 Higher sitting, never
   * carded before, is carded from a paper-by-paper review
   * (bio_review_2019_hl.py): 147 tasks, 148 cards once the four printed
   * routes are split, less Q7(b)(iii) and (iv), which the SEC withdrew as
   * outside the syllabus. Every earlier id is unchanged. */
  /* 2026-10-24: biology higher 1376 -> 1519. The 2018 Higher sitting, never
   * carded before, is carded from a paper-by-paper review
   * (bio_review_2018_hl.py): 137 tasks, 143 cards once the four printed routes
   * are split. Every earlier id is unchanged. */
  /* 2026-10-25: biology higher 1519 -> 1523. 2019 Higher Q7(b)(iii) and (iv),
   * the four tasks the SEC withdrew as outside the syllabus and first kept out
   * of the bank, are carded as printed with the footnote's effect as each
   * row's note (a printed ask is never left out). Every earlier id is
   * unchanged. */
  /* 2026-10-25: biology higher 1523 -> 1664. The 2017 Higher sitting, never
   * carded before, is carded from a paper-by-paper review
   * (bio_review_2017_hl.py): 137 tasks, 141 cards once the four printed routes
   * are split. Every earlier id is unchanged. */
  /* 2026-10-25: biology higher 1664 -> 1829. The 2016 Higher sitting, never
   * carded before, is carded from a paper-by-paper review
   * (bio_review_2016_hl.py): 163 tasks, 165 cards once the two printed routes
   * are split. Every earlier id is unchanged. */
  /* 2026-10-25: biology higher 1829 -> 1983. The 2015 Higher sitting, never
   * carded before, is carded from a paper-by-paper review
   * (bio_review_2015_hl.py): 150 tasks, 154 cards once the printed routes
   * (Q7(c)(i)2 and 3, catalase or pepsin or amylase) are split. Every earlier
   * id is unchanged. */
  /* 2026-10-25: biology higher 1983 -> 2122. The 2014 Higher sitting, never
   * carded before, is carded from a paper-by-paper review
   * (bio_review_2014_hl.py): 139 tasks, 139 cards, no printed routes. Every
   * earlier id is unchanged. */
  /* 2026-10-25: biology higher 2122 -> 2261. The 2013 Higher sitting, never
   * carded before, is carded from a paper-by-paper review
   * (bio_review_2013_hl.py): 139 tasks, 139 cards; Q5 and Q6 are each one
   * whole-question card at the Section A rubric's 20. Every earlier id is
   * unchanged. */
  ['biology:higher', BIO_HIGHER, 673, '45f278ef15f8d35a8a4393a0e8d01d7e5484e73a881844880dc090daeb9ce836'],
  /* 2026-10-11: biology ordinary 686 -> 873. The 2026 Ordinary sitting is
   * added from the same review (bio_review_2026_ol.py): 183 tasks, 187 cards
   * once the four closed choose-one pools (Q7(c), Q13(b)(vi), Q16(c)(vi),
   * Q17(a)(iv)) are expanded, and one task (Q12(b)(ii)2) held over a scheme
   * misprint. Nothing removed: the 686 cards from 2021-2025 keep their
   * identity hash, pinned below. */
  /* 2026-10-12: biology ordinary 873 -> 915. The 2025 Ordinary sitting is
   * re-reviewed paper by paper (bio_review_2025_ol.py) and corrected in
   * place: 132 of its 133 shipped ids are kept, each mapped to the task it
   * was carding (old fields recorded in biology-review-audit.json), and 43
   * tasks the old cards bundled or missed ship as new ids. One shipped id,
   * bio-2025-ol-q16-ciii-fig, duplicated two cards already carding Q16(c)(iii)
   * and (iv); it is withdrawn with a progress alias to bio-2025-ol-q16-c-iii.
   * The frozen 2021-2025 identity hash is pinned below with it restored. */
  /* 2026-10-12: biology ordinary 915 -> 959. The 2024 Ordinary sitting is
   * re-reviewed the same way (bio_review_2024_ol.py): all 124 shipped ids are
   * kept (122 corrected, 2 verified) and 44 tasks the old cards bundled or
   * missed ship as new ids. */
  /* 2026-10-12: biology ordinary 959 -> 1042. The 2023 Ordinary sitting is
   * re-reviewed the same way (bio_review_2023_ol.py): all 99 shipped ids are
   * kept (98 corrected, 1 verified) and 83 tasks the old cards bundled or
   * missed ship as new ids. bio-2023-ol-q16b-ii-v-fig, an authored figure
   * twin the build never shipped, is withdrawn without an alias. */
  /* 2026-10-13: biology ordinary 1042 -> 1060. The 2022 Ordinary sitting is
   * re-reviewed the same way (bio_review_2022_ol.py): all 166 shipped ids are
   * kept (156 corrected, 10 verified) and 18 tasks the old cards bundled or
   * missed ship as new ids. bio-2022-ol-q16-a-ii-fig, an authored figure twin
   * the build never shipped, is withdrawn without an alias. */
  /* 2026-10-13: biology ordinary 1060 -> 1092. The 2021 Ordinary sitting is
   * re-reviewed the same way (bio_review_2021_ol.py): all 164 shipped ids are
   * kept (153 corrected, 11 verified) and 32 tasks the old cards bundled or
   * missed ship as new ids. Four authored figure twins the build never
   * shipped are withdrawn without an alias. */
  /* 2026-10-14: biology ordinary 1092 -> 1278. The 2020 Ordinary sitting,
   * never carded before, is carded from a paper-by-paper review
   * (bio_review_2020_ol.py): 186 tasks, 186 cards. Every earlier id is
   * unchanged. */
  /* 2026-10-24: biology ordinary 1278 -> 1404. The 2019 Ordinary sitting,
   * never carded before, is carded from a paper-by-paper review
   * (bio_review_2019_ol.py): 126 tasks, 126 cards; seven parts whose scheme
   * prints answers but no per-response tariff they fit are each one whole-part
   * card at the printed part total, every row unpriced. Every earlier id is
   * unchanged. */
  /* 2026-10-25: biology ordinary 1404 -> 1577. The 2018 Ordinary sitting,
   * never carded before, is carded from a paper-by-paper review
   * (bio_review_2018_ol.py): 173 tasks, 173 cards. Every earlier id is
   * unchanged. */
  /* 2026-10-25: biology ordinary 1577 -> 1748. The 2017 Ordinary sitting,
   * never carded before, is carded from a paper-by-paper review
   * (bio_review_2017_ol.py): 170 tasks, 171 cards once Q11(c)(iv)'s plant or
   * animal route is split. Every earlier id is unchanged. */
  /* 2026-10-25: biology ordinary 1748 -> 1914. The 2016 Ordinary sitting,
   * never carded before, is carded from a paper-by-paper review
   * (bio_review_2016_ol.py): 166 tasks, 166 cards, each of the two printed
   * routes (Q4(e) arthritis or osteoporosis, Q15(c)(vi) Parkinson's disease or
   * paralysis) authored as its own task. Every earlier id is unchanged. */
  /* 2026-10-25: biology ordinary 1914 -> 2077. The 2015 Ordinary sitting,
   * never carded before, is carded from a paper-by-paper review
   * (bio_review_2015_ol.py): 163 tasks, 163 cards, no printed routes. Every
   * earlier id is unchanged. */
  /* 2026-10-25: biology ordinary 2077 -> 2238. The 2014 Ordinary sitting,
   * never carded before, is carded from a paper-by-paper review
   * (bio_review_2014_ol.py): 161 tasks, 161 cards, no printed routes. Every
   * earlier id is unchanged. */
  /* 2026-10-25: biology ordinary 2238 -> 2395. The 2013 Ordinary sitting,
   * never carded before, is carded from a paper-by-paper review
   * (bio_review_2013_ol.py): 157 tasks, 157 cards; Section B's Q7, Q8 and Q9
   * (a) are each one whole-part card at the rubric's 6. Every earlier id is
   * unchanged. */
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
  /* 2026-09-14: 833 -> 854. The scheme reader was filing some Scale lines
   * under the wrong unit, which shifted every model-solution crop on a page
   * by one: 29 live cards showed a NEIGHBOURING part's worked solution --
   * 2021 OL P1 Q1(c)-(d), Q2(a), Q6(a)(iii), Q6(b), Q7(a)-(e), Q8(a)-(c),
   * Q9(a)(i)-(v); P2 Q1(c)(i)-(ii), Q4(a)(i)-(ii), Q9(a)(i)-(ii),
   * Q9(b)(i)-(ii); 2023 HL P1 Q6(b), Q7(a), P2 Q2(a). Each now shows its own,
   * and every changed image was opened. No card ID changed for those.
   *
   * TWO cards are REMOVED, and both carry progress through CARD_ID_ALIASES:
   * maths-2021-ol-p2-q3 was Q3(a)'s alternative marking route filed as a
   * letterless question, and maths-2021-ol-p2-q6 was Q6(b)(ii)'s own scale
   * (now the card maths-2021-ol-p2-q6-b-ii). 23 are ADDED, each an ask the
   * paper prints that had no card: 2021 HL P1 Q9(a)(i); 2021 OL P2 Q1(b)(i),
   * Q6(b)(ii); 2022 HL P2 Q2(a), Q4(a)(ii), Q8(a)(v)+(b); 2022 OL P1
   * Q5(a); 2023 HL P1 Q2(b), Q8(b), Q8(d), P2 Q1(b), Q2(b), Q8(b)(i),
   * Q8(d)(ii); 2023 OL P1 Q2(a)(iv), P2 Q7(c); 2024 HL P1 Q9(b); 2024 OL P1
   * Q2(c), Q3(a); 2025 HL P2 Q2(a)(ii), Q3(b), Q9(b); 2025 OL P1 Q3(c).
   * Seven more asks are HELD in maths_lib.HELD_UNITS with the reason
   * recorded there (a drawn answer key the cropper cannot see, or rows that
   * mix methods). Coverage 943/989 -> 974/989. */
  ['maths:higher', MATHS_HIGHER, 413, '408f77898efcdda78dee3f8243a84241f9e8a7710e146fdb4aa2fbd295536668'],
  ['maths:ordinary', MATHS_ORDINARY, 441, '94db4616bf64733c0d61293b8a7d7ade1d91c8675fbc0d1b1705dda57943e6d2'],
  ['construction-studies:higher', CONS_HIGHER, 255, 'b74a39fd589f1082d6378190aee778d528eff0968d7af0ee9144525f2e40d57b'],
  ['construction-studies:ordinary', CONS_ORDINARY, 250, 'f56985e32cc1f02a2e2f7a7eb300a44646b75cf3604a12b5a478bde2a520d2da'],
  /* 2026-08-30: English 19/0 -> 210/450. Every independently selectable
   * response on all twenty 2021-2025 Higher and Ordinary papers is carded.
   * This includes all three OL prescribed-poetry Q2 alternatives per poem;
   * compulsory linked parts remain together but retain separate PCLM grids.
   * 205 cards open the real paper passage or poem in the source reader. */
  /* 2026-10-11: English 210/440 -> 605/1571. 1,526 cards ADDED, none removed
   * or renamed: the 33 papers whose own independent review gate passes
   * (2010-2015 all four, 2016 HL/OL P1, 2018 all four, 2026 OL P2, HL P1,
   * HL P2) are published by english_publish.py as separately practicable
   * tasks and finite printed routes, each on its own year's printed grid and
   * cap rule. Every one of the 650 legacy 2021-2025 ids is unchanged; the
   * legacy-only hashes below are the previous frozen baselines verbatim. */
  /* English (2026-10-11/12). Legacy 2021-2025 cards come from authored.json;
   * independently reviewed papers are published by english_publish.py. A
   * legacy paper is published only through english-legacy-bridge.json: each
   * legacy id is kept by its reviewed card or becomes a progress alias, and
   * the legacy proof below reproduces the frozen 210/440-id hashes from live
   * plus bridged ids. A printed choice marked identically for every option is
   * one card, and a task printed twice on a paper is one card (coordinator
   * rule, 2026-10-12); the 778 route cards and 8 repeats that rule removed
   * existed only on the English branch, never on main.
   * 2026-10-23 ship: all 68 English-version papers 2010-2026 published, 2,685
   * cards (738 Higher, 1,947 Ordinary). These pins stay main's frozen 210/440
   * identities; the reviewed cards are additions on top (englishAdditionIds)
   * and the 125 bridged legacy ids withdrawn onto a reviewed card are alias
   * keys of the frozen form (frozenIds). Never rebaseline these two pins. */
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
  /* 2026-09-11: five agents, one per sitting, worked Engineering's open asks
   * against the papers. 466 cards -> 550, and coverage 585/806 -> 675/816 —
   * the denominator itself was wrong, because every paper sets Question 1
   * (a) to (m) and the reader's letter run stopped at (l).
   *
   * ELEVEN letter cards are gone and none is lost: each carried FIVE
   * questions at once, because the paper prints a cue and its five romans
   * beneath it, and each roman is now its own card. CARD_ID_ALIASES carries
   * a student's progress to the first of them.
   *
   * eng-2024-hl-q1-l is withdrawn outright: it carried Question 1(m)'s ask
   * welded onto (l)'s, which is what the letter run stopping at (l) did to
   * every paper. Read properly, (l) states one thing and files under no
   * syllabus topic.
   *
   * 2026-09-14: eng-e3/e4/e5's missing pieces, ported by hand. 550 -> 554,
   * coverage 675/816 -> 679/816. Five cards added, none replacing anything:
   * eng-2025-hl-q1-h, eng-2025-hl-q4-a-i and eng-2025-hl-q4-b-i (the 2025
   * Higher tariff grid read on its baseline, and a reviewed judgement that
   * Q1(h)'s carabiner photograph is decorative), eng-2025-ol-q7-a-i (the same
   * judgement for the sand car), and eng-2022-ol-q7-c-i -- 2022 Ordinary's
   * PCB-branch "Light bulb / L.E.D.", which the scheme answers past an OR at
   * the key its instrument (i) also uses.
   *
   * eng-2025-ol-q2-c-i is withdrawn (authoring/withdrawn/engineering.json):
   * it answered "a suitable material for EACH of the parts labelled" with
   * the seat's material alone, for a tariff read one row out of line. No
   * alias: nothing replaces it, and 2025 OL Q2(c)(i) is open again. */
  ['engineering:higher', ENGINEERING_HIGHER, 360, '923149d5876c26dbff49440de27f4899d4298005e7043a263e3377306f3ebe1e'],
  ['engineering:ordinary', ENGINEERING_ORDINARY, 194, '4db6b2da1890e2bb262ee816e1bbb8d97e86ead5cb99531609170a75594a075b'],
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
  /* 2026-09-11: Applied Maths gets the figure cropper it never had. Until
   * today the subject had ZERO figures bound while its sibling Maths had
   * 1,834, and that single absence was what 111 of its open asks were waiting
   * on. 275 cards -> 388, coverage 286/498 -> 401/498.
   *
   * Three cards are gone. am-2021-hl-2 cited a whole question while holding
   * half of it and is re-cited as am-2021-hl-2-a-i/-a-ii, with an alias
   * carrying progress. am-2023-hl-3-iv and -3-v had a "Show that" imported
   * into their stems by a page-furniture fault, which is what let them past
   * the printed-matter gate; with their own stems they are figure-blocked
   * like the rest of Question 3, and they go back to the open list. */
  // 2026-10-07: visually reviewed 2026 papers add 45 HL and 58 OL tasks;
  // 2010–2025 contain 671 HL and 712 OL reviewed tasks, including 383 explicit
  // corrections at shipped IDs. The archive review is ongoing.
  // The old 175/208 ID hashes remain independently pinned in
  // markBankAppliedMathematics.test.tsx. Older corpus completion is ongoing.
  ['applied-maths:higher', APPLIED_MATHS_HIGHER, 716, '923aa61e94606e2f17655df1359c9ea8b2f33c037200d7265459efd0e3d414a4'],
  ['applied-maths:ordinary', APPLIED_MATHS_ORDINARY, 770, '1383838e7fedf7e49fff8eb8570b0a77fa58e5139ee855474785ec46481faf21'],
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
['bulgarian:higher', BULGARIAN_HIGHER, 141, '41075c3ba6d95e9133f8d491bf0b1c6f67dcc3924b07233394f631ada612df8b'],
  ['croatian:higher', CROATIAN_HIGHER, 100, 'bdc6cbd4e562d05ebaf2ba1c42912b48982ab9a115c8bcad428f962966f78e8a'],
  ['danish:higher', DANISH_HIGHER, 79, 'bc3f4cd2777fa14b0842f6ea0c07929c989d11c8091dba4f09aea34cc38a7e67'],
  ['estonian:higher', ESTONIAN_HIGHER, 107, '541f9881661d7f5781026ae6c11d4682b7379c54c6d6927c37322ef49605b583'],
  ['finnish:higher', FINNISH_HIGHER, 90, '584277d25fa47d8b6ca5872bb6f5fc5180efd09f7d6dbf4e78550429c360b8e9'],
  ['hungarian:higher', HUNGARIAN_HIGHER, 168, '2086ae49469f6825d08c15fa521a2c896efb84000ce304d4a6c997bd729e9a9f'],
  ['mandarin-chinese:higher', MANDARIN_CHINESE_HIGHER, 114, '24bfa04b1dfe98563d61aca009f1e5ff1a9f31cbe710795faba0a8e078d05955'],
  ['mandarin-chinese:ordinary', MANDARIN_CHINESE_ORDINARY, 87, 'e2e4528196856999da743e0861f827a457555b70b5c77c7ed835d1a702fccdd9'],
  ['slovakian:higher', SLOVAKIAN_HIGHER, 140, 'e8baef98d00f5b37334847c1720b92b70fc65117eee42ead02625a180f996ebd'],
  ['slovenian:higher', SLOVENIAN_HIGHER, 23, '5a91c38d5a570c77dcec2866a705c302bc67a7b0d33bcdeea95cd249beb149f0'],
  ['swedish:higher', SWEDISH_HIGHER, 121, 'ff499eff76dc0efe1a00cf9f20f85a3f2f508c9afd5de4ec01f2f1f8da966b56'],
  ['ukrainian:higher', UKRAINIAN_HIGHER, 20, '7d38d604f1faac1ee8726f9facc9f0ab3d303b066bf610ea8e9c7de8a8d0becd'],
  /* 2026-09-11: Design & Communication Graphics, first carded. 545 cards
   * against the 478 leaf asks its 2019-2026 papers print -- 478/478 covered,
   * nothing excluded and nothing open. More cards than asks because the
   * scheme divides one printed ask into several priced units: 2021 Ordinary
   * B-3(b) is priced as "Interpenetration on Left Hand Side" and "... Right
   * Hand Side", and each is a card citing the paper's own (b). A drawing
   * subject cards because the scheme states the CRITERIA -- every card's rows
   * are the construction steps the SEC prints, at the marks the SEC prints
   * beside them.
   * Higher 302 -> 307 in the completeness audit: 2022 Higher C-5 prints
   * "Base (13)" over steps that price 4+3+2+3 = 12, and that one wrong digit
   * made every later component head read as a group inside an unpaid Base,
   * so Vertical Spindle, Vice Pivot, Lower Jaw Spindle, Clamping Jaw and
   * Rotating Boss & Dowel were never carded at all -- 31 of the question's 60
   * marks. The misprint is recorded in dcg_scheme.HEAD_MISPRINTS and the five
   * components are cards dcg-2022-hl-c5-3 .. -7. Nothing removed. */
  ['dcg:higher', DCG_HIGHER, 307, '0f693f13e6222711fc241d1d1c8c0e00d3dfd765530de8243d5117da0a1729fc'],
  ['dcg:ordinary', DCG_ORDINARY, 238, 'd0398830a5866de46dfbe76ed96ac0f924ee1764f6dad6728bc7260ae8e3e61a'],
  /* Physical Education: the 221 IDs frozen on main (125 Higher / 96 Ordinary,
   * main's original hashes) in the additive form: the frozen identity is every
   * live ID of the frozen manifest plus any Physical Education alias key, and
   * the reviewed corpus's additions are pinned separately below. 2026-10-12: a
   * printed choice is one card, so 101 branch-only route cards were withdrawn;
   * the five live route-family IDs (q15ci, q15cii 2020 HL; q14aii 2025 HL;
   * q17cii 2021 OL; q16c 2023 OL) are the collapsed cards' own IDs. */
  ['physical-education:higher', PE_HIGHER, 125, '2b937885f9ae0c9d7c2952d43c0c2cb44275bd31414d813dee6c98d20bb8525e'],
  ['physical-education:ordinary', PE_ORDINARY, 96, '9f4fab469becb01ab3ce73e4b6301a270e68ea5310bd0225322b0cb65a1ca23f'],
  // New Accounting decks, enrolled after the complete paper/scheme sweep,
  // zero-open reconciliation and legacy Atlas/answer-ID preservation passed.
  // 2026-10-12: Higher 726 -> 721, deliberately. 2022 HL Q6(c) (explain two of
  // four printed concepts) is one card, not six per-pair cards; Accounting has
  // never been on main (checked against origin/main 6652f80cc), so the six
  // withdrawn IDs are branch-only and are not aliased.
  ['accounting:higher', ACCOUNTING_HIGHER, 721, 'c602456b31e6f07e77ce952d9724b599d8793622db3f6f80a371c23bed9a3132'],
  ['accounting:ordinary', ACCOUNTING_ORDINARY, 644, '0a35e37e0360979df909459b44024d1a62b749b268594b214bf620ebaf18db86'],
] as const;

const identityHash = (cards: readonly { id: string }[]) => createHash('sha256')
  .update(cards.map((card) => card.id).sort().join('\n'))
  .digest('hex');

const idHash = (ids: readonly string[]) => createHash('sha256')
  .update([...ids].sort().join('\n'))
  .digest('hex');

/* Art keeps its 462 pre-collapse IDs frozen (222 Higher + 240 Ordinary, the
 * original identity hashes above). The one-card-per-printed-task rule withdraws
 * the per-option cards of a printed choice whose options share one Topic Atlas
 * heading, and every choose-two route; each withdrawn ID is an explicit
 * cardAliases.ts key resolving in one step to the card for its own part, so the
 * frozen identity = live 2021–2025 Art IDs + Art alias keys. Every other
 * year's papers (2026, and 2020 back towards 2010) are added on top
 * (ART_ADDED below), never folded into the frozen hashes. */
const artAliasIds = Object.keys(CARD_ID_ALIASES).filter(id => id.startsWith('art-'));
const ART_ADDED: Record<number, { higher: number; ordinary: number }> = {
  2026: { higher: 26, ordinary: 26 },
  2020: { higher: 62, ordinary: 57 },
  2019: { higher: 62, ordinary: 57 },
  2018: { higher: 62, ordinary: 57 },
  2017: { higher: 62, ordinary: 57 },
  2016: { higher: 62, ordinary: 57 },
  2015: { higher: 63, ordinary: 57 },
  2014: { higher: 65, ordinary: 57 },
  2013: { higher: 64, ordinary: 68 },
  2012: { higher: 55, ordinary: 55 },
  2011: { higher: 59, ordinary: 57 },
  2010: { higher: 58, ordinary: 57 },
};
const isArtAdded = (id: string) => Number(id.slice(4, 8)) in ART_ADDED;
const artAdded = (level: 'higher' | 'ordinary') => Object.values(ART_ADDED)
  .reduce((sum, counts) => sum + counts[level], 0);

/* Additive, alias-aware decks: the frozen set is pinned with main's own count and
 * hash, and reviewed additions are pinned separately, so a deliberate change to
 * the additions can never rewrite or hide a frozen identity. */
const peFrozen = new Set(PE_FROZEN_MANIFEST.map(card => card.id));
const peAliasIds = Object.keys(CARD_ID_ALIASES).filter(id => id.startsWith('pe-'));
// Keep the original 606 Business IDs frozen (272 Higher + 334 Ordinary, same
// count and identity hash). Source-reviewed rubric cards and expanded printed
// routes that did not exist before are tracked as explicit additions on top;
// corrected legacy cards keep their IDs and stay inside the frozen hash.
const businessOriginalIds = new Set(businessOriginals.map(card => card.id));
const businessAdditionIds = new Set([
  ...businessReviewed.cards,
  ...expandBusinessRoutePools(businessRoutePools.pools),
].map(card => card.id).filter(id => !businessOriginalIds.has(id)));
// Keep the original French count/hash frozen. Reviewed additions have their own
// source-and-route audit in frenchWriting.test.ts; never rebaseline missing IDs.
const frenchAdditionIds = new Set([
  ...FRENCH_WRITING_CARDS,
  // Reviewed corrections retain legacy IDs and remain in the frozen hash.
  ...FRENCH_READING_CARDS.filter(card => card.id.includes('-reading-')),
  ...FRENCH_CLOZE_CARDS, ...FRENCH_LISTENING_CARDS,
].map(card => card.id));
/* Economics keeps its 697 pre-review IDs frozen (383 Higher + 314 Ordinary, the
 * original identity hashes above). The paper-by-paper physical review
 * (2021-2026, English editions; Irish attachments unchanged) does two things on
 * top of that set, and nothing else:
 *   - a frozen card that was one heading of a required pair is withdrawn and its
 *     ID becomes an explicit cardAliases.ts key resolving to the combined card,
 *     so the frozen identity = live frozen IDs + Economics alias keys;
 *   - every reviewed route, split or missing task that did not exist before is
 *     an explicit addition below. An addition never reuses a frozen ID or an
 *     alias key, so the frozen hash still proves no original ID was replaced. */
const economicsAdditionIds = new Set([
  // 2021 Ordinary: 1
  'econ-2021-ol-q14-b-ii-services',
  // 2022 Higher: 4
  'econ-2022-hl-q16-b-ii-citizens', 'econ-2022-hl-sa-q4-c', 'econ-2022-hl-sa-q6-a-b',
  'econ-2022-hl-sa-q6-a-c',
  // 2022 Ordinary: 1
  'econ-2022-ol-q13-a-ii-capital',
  // 2023 Higher: 3
  'econ-2023-hl-q15-b-iii-euro-no', 'econ-2023-hl-q16-a-i', 'econ-2023-hl-sa-q10-c',
  // 2023 Ordinary: 1
  'econ-2023-ol-q13-b-ii-trade',
  // 2024 Higher: 7
  'econ-2024-hl-q11-b-i-meaning', 'econ-2024-hl-q11-c-i-diagram',
  'econ-2024-hl-q11-c-ii-diagram', 'econ-2024-hl-q11-c-iii-diagram',
  'econ-2024-hl-q14-b-i-explanation', 'econ-2024-hl-q16-b-ii-meaning',
  'econ-2024-hl-sa-q6-a-diagram',
  // 2024 Ordinary: 1
  'econ-2024-ol-q14-a-i-education',
  // 2025 Higher: 6
  'econ-2025-hl-q11-b-i-explanation', 'econ-2025-hl-q12-a-i-gdp', 'econ-2025-hl-q14-b-ii',
  'econ-2025-hl-q16-b-i-diseconomies', 'econ-2025-hl-q16-b-ii-explanation',
  'econ-2025-hl-q16-c-ii',
  // 2025 Ordinary: 4
  'econ-2025-ol-q13-b-ii-mr', 'econ-2025-ol-q13-c-i',
  'econ-2025-ol-q14-b-i-negative', 'econ-2025-ol-q14-b-i-positive',
  // 2026 Higher: 90
  'econ-2026-hl-q11-a-i', 'econ-2026-hl-q11-a-ii', 'econ-2026-hl-q11-b-i',
  'econ-2026-hl-q11-b-i-explanation', 'econ-2026-hl-q11-b-ii', 'econ-2026-hl-q11-c-i',
  'econ-2026-hl-q11-c-i-meaning', 'econ-2026-hl-q11-c-ii-agree',
  'econ-2026-hl-q11-c-ii-disagree', 'econ-2026-hl-q11-c-iii', 'econ-2026-hl-q12-a-i-exports',
  'econ-2026-hl-q12-a-i-imports', 'econ-2026-hl-q12-a-ii-benefit',
  'econ-2026-hl-q12-a-ii-challenge', 'econ-2026-hl-q12-a-iii', 'econ-2026-hl-q12-b-i',
  'econ-2026-hl-q12-b-ii', 'econ-2026-hl-q12-b-iii', 'econ-2026-hl-q12-c-i',
  'econ-2026-hl-q12-c-i-influence', 'econ-2026-hl-q12-c-ii-option-a',
  'econ-2026-hl-q12-c-ii-option-b', 'econ-2026-hl-q12-c-iii', 'econ-2026-hl-q13-a-i',
  'econ-2026-hl-q13-a-ii', 'econ-2026-hl-q13-b-i', 'econ-2026-hl-q13-b-ii',
  'econ-2026-hl-q13-b-iii', 'econ-2026-hl-q13-c-i', 'econ-2026-hl-q13-c-ii',
  'econ-2026-hl-q13-c-iii-agree', 'econ-2026-hl-q13-c-iii-disagree', 'econ-2026-hl-q14-a-i',
  'econ-2026-hl-q14-a-ii', 'econ-2026-hl-q14-a-iii', 'econ-2026-hl-q14-b-i',
  'econ-2026-hl-q14-b-ii', 'econ-2026-hl-q14-b-iii-agree', 'econ-2026-hl-q14-b-iii-disagree',
  'econ-2026-hl-q14-c-i', 'econ-2026-hl-q14-c-ii', 'econ-2026-hl-q14-c-iii',
  'econ-2026-hl-q15-a-i', 'econ-2026-hl-q15-a-ii', 'econ-2026-hl-q15-a-iii',
  'econ-2026-hl-q15-b-i', 'econ-2026-hl-q15-b-ii', 'econ-2026-hl-q15-b-iii-agree',
  'econ-2026-hl-q15-b-iii-disagree', 'econ-2026-hl-q15-c-i', 'econ-2026-hl-q15-c-ii',
  'econ-2026-hl-q15-c-iii-narrow', 'econ-2026-hl-q15-c-iii-widen', 'econ-2026-hl-q16-a-i',
  'econ-2026-hl-q16-a-ii', 'econ-2026-hl-q16-a-iii', 'econ-2026-hl-q16-b-i',
  'econ-2026-hl-q16-b-ii', 'econ-2026-hl-q16-b-iii', 'econ-2026-hl-q16-c-i',
  'econ-2026-hl-q16-c-ii', 'econ-2026-hl-q16-c-iii', 'econ-2026-hl-sa-q1-a',
  'econ-2026-hl-sa-q1-b', 'econ-2026-hl-sa-q10-a', 'econ-2026-hl-sa-q10-b',
  'econ-2026-hl-sa-q2-a-events', 'econ-2026-hl-sa-q2-a-streaming', 'econ-2026-hl-sa-q2-b',
  'econ-2026-hl-sa-q2-c', 'econ-2026-hl-sa-q3-a-agree', 'econ-2026-hl-sa-q3-a-disagree',
  'econ-2026-hl-sa-q3-b', 'econ-2026-hl-sa-q3-c', 'econ-2026-hl-sa-q4-a',
  'econ-2026-hl-sa-q4-b', 'econ-2026-hl-sa-q4-c', 'econ-2026-hl-sa-q5-a-irrational',
  'econ-2026-hl-sa-q5-a-rational', 'econ-2026-hl-sa-q5-b', 'econ-2026-hl-sa-q6-a',
  'econ-2026-hl-sa-q6-b', 'econ-2026-hl-sa-q7-a-subsidy', 'econ-2026-hl-sa-q7-a-tax',
  'econ-2026-hl-sa-q7-b-no', 'econ-2026-hl-sa-q7-b-yes', 'econ-2026-hl-sa-q8-a',
  'econ-2026-hl-sa-q8-b', 'econ-2026-hl-sa-q9-a', 'econ-2026-hl-sa-q9-b',
  // 2026 Ordinary: 74
  'econ-2026-ol-q11-a-i', 'econ-2026-ol-q11-a-ii', 'econ-2026-ol-q11-b-i',
  'econ-2026-ol-q11-b-ii', 'econ-2026-ol-q11-b-iii', 'econ-2026-ol-q11-c-i',
  'econ-2026-ol-q11-c-ii-agree', 'econ-2026-ol-q11-c-ii-disagree', 'econ-2026-ol-q12-a-i',
  'econ-2026-ol-q12-a-ii', 'econ-2026-ol-q12-b-i', 'econ-2026-ol-q12-b-ii',
  'econ-2026-ol-q12-c-i', 'econ-2026-ol-q12-c-ii', 'econ-2026-ol-q12-c-iii',
  'econ-2026-ol-q13-a-i', 'econ-2026-ol-q13-a-ii', 'econ-2026-ol-q13-a-ii-negative',
  'econ-2026-ol-q13-a-ii-positive', 'econ-2026-ol-q13-a-iii', 'econ-2026-ol-q13-b-i-economy',
  'econ-2026-ol-q13-b-i-households', 'econ-2026-ol-q13-b-ii', 'econ-2026-ol-q13-b-iii-agree',
  'econ-2026-ol-q13-b-iii-disagree', 'econ-2026-ol-q13-c-i', 'econ-2026-ol-q13-c-ii',
  'econ-2026-ol-q14-a-i', 'econ-2026-ol-q14-a-ii-no', 'econ-2026-ol-q14-a-ii-yes',
  'econ-2026-ol-q14-b-i-employee', 'econ-2026-ol-q14-b-i-employer', 'econ-2026-ol-q14-b-ii',
  'econ-2026-ol-q14-b-iii', 'econ-2026-ol-q14-c-i', 'econ-2026-ol-q14-c-ii',
  'econ-2026-ol-q14-c-iii', 'econ-2026-ol-q15-a-i', 'econ-2026-ol-q15-a-ii-agree',
  'econ-2026-ol-q15-a-ii-disagree', 'econ-2026-ol-q15-b-i', 'econ-2026-ol-q15-b-ii',
  'econ-2026-ol-q15-b-iii', 'econ-2026-ol-q15-c-i', 'econ-2026-ol-q15-c-ii',
  'econ-2026-ol-q16-a-i', 'econ-2026-ol-q16-a-ii', 'econ-2026-ol-q16-a-iii',
  'econ-2026-ol-q16-b-i', 'econ-2026-ol-q16-b-ii', 'econ-2026-ol-q16-b-iii',
  'econ-2026-ol-q16-c-i', 'econ-2026-ol-q16-c-ii', 'econ-2026-ol-q16-c-iii',
  'econ-2026-ol-sa-q1-i', 'econ-2026-ol-sa-q1-ii', 'econ-2026-ol-sa-q10-i',
  'econ-2026-ol-sa-q10-ii', 'econ-2026-ol-sa-q2-a-private', 'econ-2026-ol-sa-q2-a-social',
  'econ-2026-ol-sa-q2-b-government', 'econ-2026-ol-sa-q2-b-retailers',
  'econ-2026-ol-sa-q3-a', 'econ-2026-ol-sa-q3-b', 'econ-2026-ol-sa-q4-a',
  'econ-2026-ol-sa-q4-b-advantage', 'econ-2026-ol-sa-q4-b-disadvantage',
  'econ-2026-ol-sa-q5-advantage', 'econ-2026-ol-sa-q5-disadvantage', 'econ-2026-ol-sa-q6',
  'econ-2026-ol-sa-q7', 'econ-2026-ol-sa-q8-agree', 'econ-2026-ol-sa-q8-disagree',
  'econ-2026-ol-sa-q9',
]);
const economicsAliasIds = Object.keys(CARD_ID_ALIASES).filter(id => id.startsWith('econ-'));
/* Agricultural Science keeps its 869 pre-audit IDs frozen (438 Higher + 431
 * Ordinary, the identity hashes above). Source-reviewed tasks for 2010-2026
 * (agricultural-science-reviewed-tasks.json addedCardIds) are explicit
 * additions on top; cards corrected in place keep their IDs inside the frozen
 * set; per-item cards consolidated into one printed task are withdrawn onto a
 * progress alias (withdrawnCardIds), so the frozen form is the live
 * non-additions plus those alias keys. Never rebaseline the frozen count or hash. */
const agriAdditionIds = new Set<string>(agriculturalReview.addedCardIds);
const agriWithdrawn: Record<string, string> = (agriculturalReview as { withdrawnCardIds?: Record<string, string> }).withdrawnCardIds ?? {};
const agriAliasIds = Object.keys(CARD_ID_ALIASES).filter(id => id.startsWith('agsci-'));
/* Construction Studies keeps its 505 pre-audit IDs frozen (255 Higher + 250
 * Ordinary, the identity hashes above). Source-reviewed tasks (2010-2026
 * theory papers, scripts/markbank/authoring/construction_*.py) are explicit
 * additions on top; pre-audit per-item cards consolidated into one printed
 * choice ("choice is not a route", 2026-10-12) keep their identity through an
 * explicit progress alias, so the frozen form is the live non-additions plus
 * the Construction alias keys. Never rebaseline the frozen count or hash. */
const constructionAdditionIds = new Set([
  ...CONSTRUCTION_2015_HIGHER_REVIEWED_IDS, ...CONSTRUCTION_2015_ORDINARY_REVIEWED_IDS,
  ...CONSTRUCTION_2026_HIGHER_REVIEWED_IDS, ...CONSTRUCTION_2026_ORDINARY_REVIEWED_IDS,
  ...CONSTRUCTION_2025_HIGHER_ADDED_IDS, ...CONSTRUCTION_2025_ORDINARY_ADDED_IDS,
  ...CONSTRUCTION_2024_HIGHER_ADDED_IDS, ...CONSTRUCTION_2024_ORDINARY_ADDED_IDS,
  ...CONSTRUCTION_2023_HIGHER_ADDED_IDS, ...CONSTRUCTION_2023_ORDINARY_ADDED_IDS,
  ...CONSTRUCTION_REVIEWED_HIGHER_ADDED_IDS, ...CONSTRUCTION_REVIEWED_ORDINARY_ADDED_IDS,
]);
const constructionAliasIds = Object.keys(CARD_ID_ALIASES).filter(id => id.startsWith('cons-'));
/* English keeps its 650 pre-review IDs frozen (210 Higher + 440 Ordinary, the
 * identity hashes above). english_publish.py publishes every reviewed paper;
 * a 2021-2025 paper publishes only through english-legacy-bridge.json, which
 * lists the paper's legacy IDs (bridgedLegacyIds): each is kept by its reviewed
 * card under the same ID or withdrawn onto one through a progress alias
 * (bridgeAliases). The frozen form is the live bridged IDs plus those alias
 * keys; every other published card is an explicit addition. */
const englishPublishedIds = new Set([...publishedEnglishHigher.cards, ...publishedEnglishOrdinary.cards]
  .map(card => card.id));
const englishBridgedIds = new Set<string>([
  ...publishedEnglishHigher.bridgedLegacyIds, ...publishedEnglishOrdinary.bridgedLegacyIds]);
const englishAdditionIds = new Set([...englishPublishedIds].filter(id => !englishBridgedIds.has(id)));
const englishAliasIds = [...englishBridgedIds].filter(id => id in CARD_ID_ALIASES);
/* Biology keeps its 1,359 pre-review IDs frozen (673 Higher + 686 Ordinary,
 * the identity hashes above): every 2021-2025 card it shipped before the
 * paper-by-paper review. The review's additions are explicit: each id a
 * reviewed 2021-2025 sitting first ships (review.added in
 * biology-review-audit.json, plus bio-2025-hl-q9-b-ii, an authored card the
 * build had never shipped), the 2026 sittings, and every sitting before 2021,
 * carded for the first time. A shipped id a review withdraws survives as a
 * progress alias, so the frozen form is the live non-additions plus the bio-
 * alias keys. Never rebaseline the frozen count or hash. */
type BiologyReviewSitting = { review?: { added: string[] } };
const BIOLOGY_REVIEW_ADDED = new Set([
  ...Object.values((biologyReview as unknown as { sittings: Record<string, BiologyReviewSitting> })
    .sittings).flatMap(sitting => sitting.review?.added ?? []),
  'bio-2025-hl-q9-b-ii',
]);
const isBiologyAdded = (id: string) => {
  const year = Number(id.slice('bio-'.length, 'bio-'.length + 4));
  return year < 2021 || year > 2025 || BIOLOGY_REVIEW_ADDED.has(id);
};
const biologyAdditionIds = new Set([...BIO_HIGHER, ...BIO_ORDINARY]
  .map(card => card.id).filter(isBiologyAdded));
const biologyAliasIds = Object.keys(CARD_ID_ALIASES).filter(id => id.startsWith('bio-'));
const frozenIds = (name: string, cards: readonly { id: string }[]) => {
  const ids = cards.map(card => card.id);
  if (name.startsWith('business:')) return ids.filter(id => !businessAdditionIds.has(id));
  if (name.startsWith('economics:')) {
    const level = name.endsWith(':higher') ? '-hl-' : '-ol-';
    return [
      ...ids.filter(id => !economicsAdditionIds.has(id)),
      ...economicsAliasIds.filter(id => id.includes(level)),
    ];
  }
  if (name.startsWith('french:')) return ids.filter(id => !frenchAdditionIds.has(id));
  if (name.startsWith('biology:')) {
    const level = name.endsWith(':higher') ? '-hl-' : '-ol-';
    return [...ids.filter(id => !isBiologyAdded(id)), ...biologyAliasIds.filter(id => id.includes(level))];
  }
  if (name.startsWith('agricultural-science:')) {
    const level = name.endsWith(':higher') ? '-hl-' : '-ol-';
    return [...ids.filter(id => !agriAdditionIds.has(id)), ...agriAliasIds.filter(id => id.includes(level))];
  }
  if (name.startsWith('construction-studies:')) {
    const level = name.endsWith(':higher') ? '-hl-' : '-ol-';
    return [
      ...ids.filter(id => !constructionAdditionIds.has(id)),
      ...constructionAliasIds.filter(id => id.includes(level)),
    ];
  }
  if (name.startsWith('english:')) {
    const level = name.endsWith(':higher') ? '-hl-' : '-ol-';
    return [
      ...ids.filter(id => !englishAdditionIds.has(id)),
      ...englishAliasIds.filter(id => id.includes(level)),
    ];
  }
  const level = name.endsWith(':higher') ? '-hl-' : '-ol-';
  if (name.startsWith('art:')) {
    return [...ids.filter(id => !isArtAdded(id)), ...artAliasIds.filter(id => id.includes(level))];
  }
  if (name.startsWith('physical-education:')) {
    return [...ids.filter(id => peFrozen.has(id)), ...peAliasIds.filter(id => id.includes(level))];
  }
  return ids;
};
const liveFrozenCount = (name: string, cards: readonly { id: string }[]) =>
  name.startsWith('economics:') ? cards.filter(card => !economicsAdditionIds.has(card.id)).length
    : name.startsWith('agricultural-science:') ? cards.filter(card => !agriAdditionIds.has(card.id)).length
    : name.startsWith('construction-studies:') ? cards.filter(card => !constructionAdditionIds.has(card.id)).length
    : name.startsWith('english:') ? cards.filter(card => !englishAdditionIds.has(card.id)).length
    : name.startsWith('biology:') ? cards.filter(card => !isBiologyAdded(card.id)).length
    : cards.length;
const peAdditions = {
  higher: [PE_HIGHER, 257, 'b66f69f293e90b2913862dbb646bc161bbff8eda4ea41ba78d88fbb66acd23bf'],
  ordinary: [PE_ORDINARY, 294, '097f2e5140a024bf28633d1aa17898f041acbdb6ab658a5afd65eb8ba5681ac2'],
} as const;

describe('Mark Bank card preservation', () => {
  it.each(decks)('%s retains its complete stable card set', (name, cards, count, hash) => {
    const frozen = frozenIds(name, cards);
    expect(frozen.length, `${name}: card count changed`).toBe(count);
    expect(new Set(frozen).size, `${name}: duplicate frozen card IDs`).toBe(count);
    expect(new Set(cards.map((card) => card.id)).size, `${name}: duplicate card IDs`).toBe(cards.length);
    expect(idHash(frozen), `${name}: a card ID was removed or replaced`).toBe(hash);
  });

  it.each(Object.entries(peAdditions))('pins the reviewed Physical Education %s additions beside the frozen set', (_, [cards, count, hash]) => {
    // 2026-10-12: 652 -> 551 additions (443/430 -> 382/390 cards). Each printed
    // choice is one card; the 101 per-option and per-pair route cards were
    // branch-only and are withdrawn rather than aliased.
    const additions = cards.map(card => card.id).filter(id => !peFrozen.has(id));
    expect(additions).toHaveLength(count);
    expect(additions.filter(id => peAliasIds.includes(id))).toEqual([]);
    expect(idHash(additions)).toBe(hash);
  });

  it('collapses each Art printed choice to one card and resolves every withdrawn ID', () => {
    const higher = new Map(ART_HIGHER.map(card => [card.id, card]));
    const ordinary = new Map(ART_ORDINARY.map(card => [card.id, card]));
    expect(artAliasIds).toHaveLength(68);
    for (const oldId of artAliasIds) {
      const canonical = CARD_ID_ALIASES[oldId];
      const deck = oldId.includes('-hl-') ? higher : ordinary;
      expect(higher.has(oldId) || ordinary.has(oldId), `${oldId} should be withdrawn`).toBe(false);
      expect(deck.has(canonical), `${oldId} -> ${canonical} must be live at the same level`).toBe(true);
      expect(canonical in CARD_ID_ALIASES, `${oldId} must resolve in one step`).toBe(false);
      expect(canonical.slice(0, 12), `${oldId} must stay in its year and level`).toBe(oldId.slice(0, 12));
    }
    const aliased = (level: string) => artAliasIds.filter(id => id.includes(level)).length;
    expect([aliased('-hl-'), aliased('-ol-')]).toEqual([20, 48]);
    expect(ART_HIGHER).toHaveLength(222 - aliased('-hl-') + artAdded('higher'));
    expect(ART_ORDINARY).toHaveLength(240 - aliased('-ol-') + artAdded('ordinary'));
  });

  it('adds each further Art year on top of the frozen 2021–2025 identity', () => {
    // No added id was ever aliased or frozen; each is a new card for a printed task.
    const cards = [...ART_HIGHER, ...ART_ORDINARY];
    for (const [year, counts] of Object.entries(ART_ADDED)) {
      const added = cards.filter(card => card.year === Number(year));
      expect(added.filter(card => card.level === 'higher'), year).toHaveLength(counts.higher);
      expect(added.filter(card => card.level === 'ordinary'), year).toHaveLength(counts.ordinary);
      expect(added.every(card => card.id.startsWith(`art-${year}-`))).toBe(true);
    }
    expect(artAliasIds.filter(isArtAdded)).toEqual([]);
    expect(cards.filter(card => !isArtAdded(card.id)).every(card => card.year >= 2021 && card.year <= 2025))
      .toBe(true);
  });

  it('protects the complete current bank', () => {
    // 10,495 before this session, plus sixteen subjects carded in six waves:
    // Religious Education 288, LCVP 314, Technology 716, History 749,
    // French 260, Applied Maths 275, German 264, Spanish 347, Italian 350,
    // Russian 199, Japanese 600, Classical Studies 516, Latin 227,
    // Portuguese 173, Romanian 50 and Dutch 42.
    // 18,345 before Design & Communication Graphics, plus its 545 (307 Higher
    // and 238 Ordinary). Nothing removed.
    // Politics adds 1,086 tasks; all previous subjects retain their IDs.
    // Politics then folds its branch-only choice routes into their printed
    // tasks, 1,086 -> 622 (2026-10-12): 23,539 - 464.
    // Physical Education folds its 101 branch-only route cards into their
    // printed tasks (2026-10-12): 23,075 - 101; Accounting folds 2022 HL
    // Q6(c)'s six pair cards into one: - 5; Politics 2021 OL Q1(f) becomes one
    // card per syllabus topic: + 1.
    // Business and French keep their original card sets frozen (checked per
    // deck above); their reviewed additions are counted on top of the bank.
    // Business: 2010-2026 source-reviewed additions (2026-10-14), 1,382.
    // Economics keeps its 697 pre-review IDs frozen the same way; its frozen
    // form is its live cards less its reviewed additions plus its
    // consolidated halves, each now an alias key.
    // Art (2026-10-14): its 462 frozen 2021-2025 cards become one card per
    // printed task (68 per-option IDs withdrawn onto aliases) and 2010-2020
    // and 2026 are added on top: - 68 + 1,362.
    // Agricultural Science (2026-10-15): its 869 frozen cards gain 1,604
    // source-reviewed tasks and withdraw 9 per-item cards onto aliases: + 1,595.
    // English (2026-10-23): its 650 frozen cards gain 2,160 reviewed tasks and
    // withdraw 125 bridged legacy cards onto aliases: + 2,035.
    // Biology (merged 2026-10-24): its 1,359 frozen cards gain the paper-by-paper
    // review's additions (2010-2020 and 2026 carded for the first time, and the
    // tasks the reviewed 2021-2025 sittings had bundled or missed) and withdraw
    // two onto aliases: + biologyAdditionIds - 2.
    const businessAdded = (name: string, cards: readonly { id: string }[]) =>
      name.startsWith('business:') ? cards.filter(card => businessAdditionIds.has(card.id)).length : 0;
    // Construction Studies keeps its 505 pre-audit IDs frozen the same way:
    // live non-additions plus its consolidated per-item cards, each an alias key.
    const economicsFrozenDelta = (name: string, cards: readonly { id: string }[]) =>
      name.startsWith('economics:') || name.startsWith('agricultural-science:') || name.startsWith('construction-studies:')
        || name.startsWith('english:') || name.startsWith('biology:')
        ? frozenIds(name, cards).length - cards.length : 0;
    const artNet = artAdded('higher') + artAdded('ordinary') - artAliasIds.length;
    const agriNet = agriAdditionIds.size - agriAliasIds.length;
    expect(decks.reduce((total, [name, cards]) => (
      total + cards.length - businessAdded(name, cards) + economicsFrozenDelta(name, cards)
    ), 0)).toBe(22_970 + frenchAdditionIds.size + artNet);
    expect(decks.reduce((total, [, cards]) => total + cards.length, 0))
      .toBe(22_970 + frenchAdditionIds.size + businessAdditionIds.size
        + economicsAdditionIds.size - economicsAliasIds.length + artNet + agriNet
        + constructionAdditionIds.size - constructionAliasIds.length
        + englishAdditionIds.size - englishAliasIds.length
        + biologyAdditionIds.size - biologyAliasIds.length);
    // Maths adds 21 net cards; Engineering adds five and withdraws one invalid card.
    // Physical Education completion adds 652 cards to the previous 19,328.
    // Russian 199, Japanese 600, Classical Studies 516 and Latin 227.
    // Lithuanian 306, Latvian 20 and Czech 15 in a sixth wave:
    // 16,087 + 306 + 20 + 15.
    // Russian 199, Japanese 600, Classical Studies 516 and Polish 237.
    // Russian 199, Japanese 600, Classical Studies 516 and Arabic 250.
    // Polish 237, Arabic 250, Ancient Greek 383 and Modern Greek 79.
  });

  it('adds the source-reviewed Business cards on top of the frozen 606 without replacing any', () => {
    /* 2010-2026 Higher ABQs, full 2010-2026 Higher papers, full 2010-2026 Ordinary
     * papers, one card per printed choice marked alike (choice is not a route)
     * and the one differently marked 2013 route pool. Every
     * addition is a new, unique ID at its own level; none reuses an original
     * ID. */
    expect(businessAdditionIds.size).toBe(1382);
    const higher = BUSINESS_HIGHER.map(card => card.id);
    const ordinary = BUSINESS_ORDINARY.map(card => card.id);
    expect(new Set(higher).size).toBe(higher.length);
    expect(new Set(ordinary).size).toBe(ordinary.length);
    const higherAdditions = BUSINESS_HIGHER.filter(card => businessAdditionIds.has(card.id));
    const ordinaryAdditions = BUSINESS_ORDINARY.filter(card => businessAdditionIds.has(card.id));
    expect(higherAdditions).toHaveLength(605);
    expect(ordinaryAdditions).toHaveLength(777);
    expect(higherAdditions.length + ordinaryAdditions.length).toBe(businessAdditionIds.size);
    for (const id of businessAdditionIds) {
      expect(businessOriginalIds.has(id), id).toBe(false);
      expect(id.includes('-hl-') ? higher : ordinary, id).toContain(id);
    }
    expect(BUSINESS_HIGHER).toHaveLength(272 + higherAdditions.length);
    expect(BUSINESS_ORDINARY).toHaveLength(334 + ordinaryAdditions.length);
    for (const id of businessOriginalIds) {
      expect([...BUSINESS_HIGHER, ...BUSINESS_ORDINARY].some(card => card.id === id), id).toBe(true);
    }
  });

  it('adds the reviewed Economics routes on top of the frozen 697 and resolves every withdrawn ID', () => {
    const higher = new Map(ECON_HIGHER.map(card => [card.id, card]));
    const ordinary = new Map(ECON_ORDINARY.map(card => [card.id, card]));
    expect(economicsAdditionIds.size).toBe(192);
    expect(economicsAliasIds).toHaveLength(36);
    for (const id of economicsAdditionIds) {
      const deck = id.includes('-hl-') ? higher : ordinary;
      expect(deck.has(id), `${id}: addition missing from its level`).toBe(true);
      expect(id in CARD_ID_ALIASES, `${id}: addition reuses an alias key`).toBe(false);
    }
    for (const oldId of economicsAliasIds) {
      const canonical = CARD_ID_ALIASES[oldId];
      const deck = oldId.includes('-hl-') ? higher : ordinary;
      expect(higher.has(oldId) || ordinary.has(oldId), `${oldId} should be withdrawn`).toBe(false);
      expect(deck.has(canonical), `${oldId} -> ${canonical} must be live at the same level`).toBe(true);
      expect(canonical in CARD_ID_ALIASES, `${oldId} must resolve in one step`).toBe(false);
      expect(canonical.slice(0, 12), `${oldId} must stay in its year and level`).toBe(oldId.slice(0, 12));
    }
    const additions = (level: string) => [...economicsAdditionIds].filter(id => id.includes(level)).length;
    const aliased = (level: string) => economicsAliasIds.filter(id => id.includes(level)).length;
    expect([additions('-hl-'), aliased('-hl-'), additions('-ol-'), aliased('-ol-')]).toEqual([110, 24, 82, 12]);
    expect(ECON_HIGHER).toHaveLength(383 - aliased('-hl-') + additions('-hl-'));
    expect(ECON_ORDINARY).toHaveLength(314 - aliased('-ol-') + additions('-ol-'));
  });

  it('adds exactly the reviewed Agricultural Science tasks to the frozen pre-audit set', () => {
    // Frozen pre-audit set: 438 Higher + 431 Ordinary, counted and hashed above.
    // Every source-reviewed task is an explicit addition on top; each withdrawn
    // per-item card resolves through its progress alias.
    expect(agriAdditionIds.size).toBe(1604);
    const live = [...AGSCI_HIGHER, ...AGSCI_ORDINARY];
    const liveIds = new Set(live.map(card => card.id));
    for (const id of agriAdditionIds) expect(liveIds.has(id), `missing reviewed addition ${id}`).toBe(true);
    expect(Object.keys(agriWithdrawn).sort()).toEqual([...agriAliasIds].sort());
    for (const [id, canonical] of Object.entries(agriWithdrawn)) {
      expect(liveIds.has(id), `${id} must be withdrawn`).toBe(false);
      expect(CARD_ID_ALIASES[id], `${id} needs a progress alias`).toBe(canonical);
    }
    expect(live).toHaveLength(438 + 431 - agriAliasIds.length + agriAdditionIds.size);
  });

  it('keeps every Agricultural Science card corrected in place, each with its SEC evidence', () => {
    // Corrected IDs are NOT additions: they stay inside the frozen 869-card
    // identity hash above. Each is listed here with the reason it changed.
    const corrected: Record<string, string> = {
      'agsci-2025-ol-q8b': 'Symbols 2 and 3 marked 3+2 as a two-option group, not an all-or-nothing tick.',
      'agsci-2025-hl-q12a': 'Q12 is one any-four-of-five 2(4)+2(1) card listing all five prompts, 10 marks; Q12(b)–(e) are withdrawn as its aliases.',
      'agsci-2025-hl-q14bi': 'Restores the published result mark: 4x4 + 1 = 17, so Question 14 totals 50.',
      'agsci-2025-hl-q15b': 'Any three of four printed plants on one card, every photograph decoded (3x1).',
      'agsci-2025-ol-q1ai': 'Any three of four printed cattle breeds on one card, every photograph decoded, word list as printed (3x2).',
      'agsci-2025-ol-q9bi-ii': 'Keeps part (i) only (3 marks); part (ii) already ships as agsci-2025-ol-q9bii.',
      'agsci-2025-ol-q9biii-iv': 'Keeps part (iii) only (3 marks); part (iv) already ships as agsci-2025-ol-q9biv.',
      'agsci-2024-hl-q2ai': 'Any two of three printed breeds on one card, every photograph decoded (2(2)).',
      'agsci-2024-hl-q2aiii': 'Drops the question wording that had been listed as an accepted answer; any two of four printed characteristics, 2(2).',
      'agsci-2024-hl-q6a': 'Any two of four printed scheme features on one card: action row 2(3) and benefit row 2(2), ref Q6(a).',
      'agsci-2024-hl-q16bi': 'Restores the truncated answer ("... with Sample 2 or Sample 3") and the paper\'s results-table lead-in and crop.',
      'agsci-2024-hl-q16bii': 'Replaces a flattened results table in the stem with the paper\'s lead-in and the table crop.',
      'agsci-2024-hl-q17a': 'Restores the published 5 (factor) + 1 (description) split instead of all-or-nothing 6.',
      'agsci-2024-hl-q17cii': 'Replaces a flattened results table in the stem with the paper\'s own lead-in.',
      'agsci-2024-hl-q17ciii': 'Replaces a flattened results table in the stem with the paper\'s own lead-in.',
      'agsci-2024-hl-q18aiii': 'Any two of six printed dominant features at 6+2, not black coat and coat pattern only.',
      'agsci-2024-ol-q2biii': 'Replaces a stem of run-together diagram labels with the paper\'s lead-in and the picture crop.',
      'agsci-2024-ol-q14cii': 'Restores the published 2 + 2 for name or description: two names and two descriptions at 2 each.',
      'agsci-2024-ol-q14d': 'Restores the published 6(2): six hay/silage cells at 2 marks each, not three paired rows.',
      'agsci-2023-hl-q1aii': 'Restores the whole published answer ("... at least 2 kinds of resources (e.g. meat, eggs, milk)").',
      'agsci-2023-hl-q2a': 'Any two of three printed growth stages on one card, Flowering included (2(3)).',
      'agsci-2023-hl-q4a': 'Any three of four printed treatments on one card, sorting into pens included (3(2)).',
      'agsci-2023-hl-q5a': 'One row lists the whole sampling pool, any two at 3 (2(3)).',
      'agsci-2023-hl-q5c': 'Restores the whole published answer sentence.',
      'agsci-2023-hl-q8c': 'Replaces chart-label soup with the paper\'s wording and accepts both published conclusions.',
      'agsci-2023-hl-q9aii': 'One row lists the whole Farmdroid benefit pool, any two at 3 (2(3)).',
      'agsci-2023-hl-q9bi': 'One row lists the whole pregnancy-scanning pool, any two at 3 (2(3)).',
      'agsci-2023-hl-q11a': 'One row lists the whole calves-per-cow pool, any two at 3 (2(3)).',
      'agsci-2023-hl-q11b': 'One row lists the whole calving-rate pool, any two at 2 (2(2)).',
      'agsci-2023-hl-q13ai': 'Factors and descriptions earn 5+5+2+2 in the order correct, not 7 per pair.',
      'agsci-2023-hl-q13aii': 'The podzol drawing is banded D = 0,3,6 plus L = 3 x 2, not five ranked rows.',
      'agsci-2023-hl-q13bii': 'Restores each soil water state\'s whole published implication.',
      'agsci-2023-hl-q13c': 'Laboratory and field methods are mutually exclusive routes, every point listed (3(4)).',
      'agsci-2023-hl-q13dii': 'Lists all nine soil moisture functions at 4+2.',
      'agsci-2023-hl-q14biii': 'Lists all six clover advantages at 5+1.',
      'agsci-2023-hl-q14biv': 'Names the underlined term the paper prints ("annual plant").',
      'agsci-2023-hl-q14ci': 'Lists all six plant-count steps, any three at 4 (3(4)).',
      'agsci-2023-hl-q14cii': 'Lists all five plant-count advantages at 5+1.',
      'agsci-2023-hl-q15a': 'Hand, sediment and sieve methods are mutually exclusive routes, every point listed (3(4)).',
      'agsci-2023-hl-q15biii': 'Lists all five liming benefits at 5+2.',
      'agsci-2023-hl-q15cii': 'Replaces chart-label soup with the paper\'s lead-in and chart; restores both whole answers.',
      'agsci-2023-hl-q16aii': 'Replaces chart-label soup with the paper\'s lead-in and chart; accepts both published reasons.',
      'agsci-2023-hl-q18bii': 'Three factors and three descriptions at 3 each (F:3(3) + D:3(3)), not 6 per pair.',
      'agsci-2023-ol-q1b': 'Replaces drawing-label debris in the stem and the scheme asterisk in the answer (6.5, exact term).',
      'agsci-2023-ol-q2a': 'Any three of five printed breeds on one card at the published 3+2+1, every photograph decoded.',
      'agsci-2023-ol-q4': 'Restores the first-correct 6+2+2 instead of 6 pinned to controlled grazing.',
      'agsci-2023-ol-q6aiii': 'Replaces diagram-label soup with the paper\'s lead-in and the diagram.',
      'agsci-2023-ol-q8a': 'Four placements at the first-correct 6+2+1+1, not one all-or-nothing 10-mark row.',
      'agsci-2023-ol-q9ai': 'Adds the paper\'s lead-in and drops the scheme asterisk from the answer (Abomasum, exact term).',
      'agsci-2023-ol-q9b-iii': 'Restores the first-correct 3+1 instead of 3 pinned to the ruminant column.',
      'agsci-2023-ol-q10b-i-iii': 'Keeps part (i) only (3 marks); (ii) already ships as agsci-2023-ol-q10bii and (iii) is its own card.',
      'agsci-2023-ol-q10bii': 'Replaces a run-together results table in the stem with the paper\'s lead-in and the table crop.',
      'agsci-2023-ol-q13aii': 'Restores the first-correct 6+3+3 instead of 6 pinned to photograph A.',
      'agsci-2023-ol-q13bii': 'Replaces chart-label soup with the paper\'s lead-in and chart; accepts both published conclusions.',
      'agsci-2023-ol-q14a-i': 'Restores both whole published definitions.',
      'agsci-2023-ol-q14bi': 'Replaces the stem "W X" with the paper\'s lead-in.',
      'agsci-2023-ol-q14bii': 'Replaces the stem "W X" with the paper\'s lead-in.',
      'agsci-2023-ol-q14b-iii': 'Replaces the stem "W X" with the paper\'s lead-in.',
      'agsci-2023-ol-q15aii': 'Replaces the diagram key in the stem with the paper\'s lead-in and the soil diagrams.',
      'agsci-2023-ol-q15b': 'Restores the first-correct 6+4 instead of 6 pinned to label A.',
      'agsci-2023-ol-q16ai': 'Resazurin and bacterial-count methods as answer routes, every published point listed (3(4)).',
      'agsci-2023-ol-q18ci': 'Restores the whole first published point.',
      'agsci-2022-hl-q2b': 'Lists every characteristic in the scheme\'s two-page table, any two at 3 (2(3)).',
      'agsci-2022-hl-q10b': 'Kale, Miscanthus and OSR planting points as answer routes, not one mixed pool.',
      'agsci-2022-hl-q10c': 'Kale, Miscanthus and OSR advantages as answer routes, not one mixed pool.',
      'agsci-2022-hl-q15ai': 'Each synchronisation protocol (ewes, three for heifers or cows, sows) as an answer route, every step listed.',
      'agsci-2022-hl-q16ci': 'Restores the published 11 marks: named system 2, drawing 6/3/0, labels 3(1).',
      'agsci-2022-hl-q17ai': 'The earthworm drawing is banded D 6, 3, 0 plus labels 3(1), not one 6-mark row.',
      'agsci-2022-hl-q17bii': 'Restores the end of the hybrid vigour definition ("to those of both parents").',
      'agsci-2022-ol-q1a': 'Machine A, its function, machine B and its function at 2 each, as the scheme prints them.',
      'agsci-2022-ol-q2ai': 'Any three of four printed breeds on one card, every photograph decoded (3(2)).',
      'agsci-2022-ol-q2aii': 'Replaces the run-together word list in the stem with the paper\'s part (ii) wording.',
      'agsci-2022-ol-q3a': 'The indicator and pH-meter methods as answer routes, not one mixed step list.',
      'agsci-2022-ol-q3b': 'Every published implication listed; implication 3 and the lime answer 1, as printed.',
      'agsci-2022-ol-q4b': 'Statements (i)-(v) on the table card at 5(2); the five per-statement cards are withdrawn as its aliases.',
      'agsci-2022-ol-q5a': 'Restores the whole published production-diet answer.',
      'agsci-2022-ol-q7aiii': 'Each of the six nutrients as an answer route with its symptom and treatment.',
      'agsci-2022-ol-q7bii': 'Every published leaf adaptation listed at the first-correct 3+1; drops diagram labels from the stem.',
      'agsci-2022-ol-q9c': 'Restores the paper\'s tick-box wording and options.',
      'agsci-2022-ol-q10c': 'Every published sampling precaution listed at the first-correct 2+1.',
      'agsci-2022-ol-q11aiii': 'Restores the whole published answer and the paper\'s wording.',
      'agsci-2022-ol-q14civ': 'Nine ways and nine reasons as published menus, 2(2+2) 1(2+1).',
      'agsci-2022-ol-q16bii': 'Nine hay-making steps listed one each at 3(4)+3.',
      'agsci-2022-ol-q17ai': 'Ten advantages listed one each at 4+2, other valid answers open.',
      'agsci-2022-ol-q17aii': 'Five reasons listed one each, as printed, at 4+2.',
      'agsci-2022-ol-q17aiii': 'Six disadvantages listed one each at 4+2.',
      'agsci-2022-ol-q18ai': 'Six traits listed one each at 3(4).',
      'agsci-2022-ol-q18bi': 'Seven seedbed steps listed one each at 3(2).',
      'agsci-2021-hl-q1b': 'The first definition earns 2, the other definition and the example 1 each (2 + 1+1); drops the part (a) answers from the stem.',
      'agsci-2021-hl-q3ai': 'Replaces the sign text run together in the stem with the paper\'s lead-in.',
      'agsci-2021-hl-q3aii': 'Replaces the sign text run together in the stem with the paper\'s instruction.',
      'agsci-2021-hl-q3aiii': 'Restores the omitted bloodless-castration advantage; every published advantage listed.',
      'agsci-2021-hl-q3bii': 'Restores the omitted wet-land advantage; every published advantage listed.',
      'agsci-2021-hl-q3biii': 'Restores the omitted soil-structure way; every published way listed.',
      'agsci-2021-hl-q4c': 'Restores the omitted first way (plant more trees or hedges); every published way listed.',
      'agsci-2021-hl-q5a': 'Kale or stubble turnips, oilseed rape and Miscanthus as answer routes, not one mixed pool.',
      'agsci-2021-hl-q5b': 'Each crop\'s pests as an answer route, not one mixed pool.',
      'agsci-2021-hl-q5c': 'Each crop\'s two growth stages as an answer route.',
      'agsci-2021-hl-q6bii': 'Restores the tillage half of the second comparison.',
      'agsci-2021-hl-q9a': 'Restores the end of the genomic selection definition.',
      'agsci-2021-hl-q9c': 'Restores the breeding step after the list of traits.',
      'agsci-2021-hl-q10a': 'Restores the end of the artisan produce definition.',
      'agsci-2021-hl-q10c': 'The paper\'s wording with the pie chart cropped from the paper.',
      'agsci-2021-hl-q11bii': 'Bloat and acidosis as answer routes, each with its own symptom, treatment and prevention.',
      'agsci-2021-hl-q14bi': 'Drops the next part\'s table debris from the stem.',
      'agsci-2021-hl-q14bii': 'Pig, poultry and horse as answer routes at 2(2+1); restores "good terminal sires".',
      'agsci-2021-hl-q14cii': 'Removes a dash the scheme does not print.',
      'agsci-2021-hl-q14ciii': 'Removes a dash the scheme does not print.',
      'agsci-2021-hl-q15ai': 'Removes a dash the scheme does not print.',
      'agsci-2021-hl-q15aii': 'Removes a dash the scheme does not print.',
      'agsci-2021-hl-q15bi': 'Replaces axis and legend debris in the stem with the paper\'s lead-in and the bar chart.',
      'agsci-2021-hl-q15biii': 'Replaces axis and legend debris in the stem with the paper\'s lead-in and the bar chart.',
      'agsci-2021-hl-q15biv': 'All five published recommendations at 3(2), with the bar chart.',
      'agsci-2021-hl-q16aiii': 'Every TBC and SCC recommendation listed at 3(3), not a fixed third row.',
      'agsci-2021-hl-q16b': 'The resazurin test and the total bacterial count as answer routes, every published step listed.',
      'agsci-2021-hl-q17bi': 'Field 2 results in the stem and the reference soil index cropped from the paper.',
      'agsci-2021-hl-q17biv': 'Names 1 each and roles 3 each (3+3+1+1), not 4 per nutrient-and-role.',
      'agsci-2021-hl-q18a-crop-preservation': 'Grain, potato and grass preservation as answer routes, not one mixed pool.',
      'agsci-2021-ol-q1a': 'Replaces tick-box debris in the stem with the paper\'s instruction.',
      'agsci-2021-ol-q3a-i': 'Restores the omitted second explanation; every published explanation listed.',
      'agsci-2021-ol-q3a-iii': 'Restores the omitted fourth disadvantage; every published disadvantage listed at 3+1.',
      'agsci-2021-ol-q3b-iii': 'Restores the omitted "less labour required"; every published advantage listed at 3+1.',
      'agsci-2021-ol-q4b': 'Replaces diagram-label debris in the stem with the paper\'s lead-in.',
      'agsci-2021-ol-q4c': 'First-correct 3+1 across every published disadvantage, not 3 pinned to poor drainage.',
      'agsci-2021-ol-q5b': 'Restores the omitted timing step; every published step listed at 3+1.',
      'agsci-2021-ol-q8a-iii': 'Restores the omitted wellington boots; every published piece listed at 2(2).',
      'agsci-2021-ol-q8a-iv': 'Restores the whole second precaution ("avoid touching the infected area on the cattle").',
      'agsci-2021-ol-q8b-ii': 'Restores the omitted "keep all children and dogs away" precaution.',
      'agsci-2021-ol-q8b-iii': 'Restores the omitted electric-wires precaution; every published precaution listed at 3+2+1.',
      'agsci-2021-ol-q9b': 'Restores "soils or soil cultivation (ploughing)" and enteric fermentation; every source listed at 3+1.',
      'agsci-2021-ol-q10b': 'One answer in the scheme\'s words, not split at oestrogen.',
      'agsci-2021-ol-q10d': 'Drops diagram labels from the stem.',
      'agsci-2021-ol-q11b-i': 'Restores the whole second reason and the plan view.',
      'agsci-2021-ol-q11b-iii': 'Restores the omitted "increased milk yield from cows".',
      'agsci-2021-ol-q12a': 'Drops photograph letters and the word list run into the question; the list is quoted.',
      'agsci-2021-ol-q12b': 'Landrace, Large White, Rhode Island Red and Irish Sport Horse as answer routes.',
      'agsci-2021-ol-q13c-iv': 'Restores the omitted "do not share equipment" practice; every practice listed at 2+2+1.',
      'agsci-2021-ol-q14b-ii': 'Every published resazurin step listed at 3(3); other milk tests open.',
      'agsci-2021-ol-q14b-iii': 'Each error paired with its own remedy as an answer route.',
      'agsci-2021-ol-q14b-iv': 'Qualitative (resazurin) and quantitative (TBC) as answer routes with their justifications.',
      'agsci-2021-ol-q15c-iii': 'Restores the end of the packing point; every published way listed at 4+2.',
      'agsci-2021-ol-q16b-ii': 'Restores the omitted soil-types step; every published step listed at 4+2.',
      'agsci-2021-ol-q16c-ii': 'Restores the omitted third piece of advice.',
      'agsci-2021-ol-q16c-v': 'Each implication paired with its own reason as an answer route.',
      'agsci-2021-ol-q16d-i': 'Restores the omitted compaction-and-erosion principle; every principle listed at 4+4.',
      'agsci-2021-ol-q17a-iii': 'Restores the omitted "volume of water"; every factor listed at 4+3.',
      'agsci-2021-ol-q17a-iv': 'Restores the whole second effect of sowing depth.',
      'agsci-2021-ol-q17b-ii': 'Restores the omitted second piece of advice.',
      'agsci-2021-ol-q18a-i-seedbed': 'Restores the 2 marks for naming the crop (9, not 7) and the potato stones point.',
      'agsci-2021-ol-q18b-i': 'Restores the second published explanation of natural selection.',
      'agsci-2021-ol-q18c-iii': 'The paper\'s wording with the lamb growth graph; restores the omitted description.',
      'agsci-2021-ol-q18d-iii': 'Restores the omitted thread-and-ruler method.',
    };
    expect([...agriculturalReview.correctedCardIds].sort()).toEqual(Object.keys(corrected).sort());
    const live = new Map(decks.flatMap(([, cards]) => cards.map(card => [card.id, card] as const)));
    for (const id of Object.keys(corrected)) {
      expect(live.has(id), id).toBe(true);
      expect(agriAdditionIds.has(id), `${id} must stay a baseline identity`).toBe(false);
    }
    const records = (agriculturalReview as { corrections: Record<string, { reason: string; originalSha256: string }> }).corrections;
    expect(Object.keys(records).sort()).toEqual(Object.keys(corrected).filter(id => id !== 'agsci-2025-ol-q8b').sort());
    for (const record of Object.values(records)) {
      expect(record.reason).toMatch(/Visually verified paper PDF page \d+/);
      expect(record.originalSha256).toMatch(/^[0-9a-f]{64}$/);
    }
    expect(live.get('agsci-2025-hl-q14bi')?.totalMarks).toBe(17);
    expect(live.get('agsci-2025-hl-q12a')?.totalMarks).toBe(10);
    for (const key of ['b', 'c', 'd', 'e']) expect(live.has(`agsci-2025-hl-q12${key}`)).toBe(false);
    // 2024 Higher corrections keep each original's ID and total.
    for (const [id, marks] of [['agsci-2024-hl-q2ai', 4], ['agsci-2024-hl-q6a', 10], ['agsci-2024-hl-q6bii', 4], ['agsci-2024-hl-q15aiii', 4],
      ['agsci-2024-hl-q17a', 6], ['agsci-2024-hl-q18aiii', 8]] as const) expect(live.get(id)?.totalMarks, id).toBe(marks);
    // 2023 Higher corrections keep each original's ID and total.
    for (const [id, marks] of [['agsci-2023-hl-q2a', 6], ['agsci-2023-hl-q4a', 6], ['agsci-2023-hl-q13ai', 14], ['agsci-2023-hl-q13aii', 12],
      ['agsci-2023-hl-q13c', 12], ['agsci-2023-hl-q15a', 12], ['agsci-2023-hl-q18bii', 18]] as const) expect(live.get(id)?.totalMarks, id).toBe(marks);
    // 2023 Ordinary corrections keep each original's ID; the fused Q10(b)(i)-(iii) keeps part (i) at 3.
    for (const [id, marks] of [['agsci-2023-ol-q2a', 6], ['agsci-2023-ol-q4', 10], ['agsci-2023-ol-q8a', 10], ['agsci-2023-ol-q10b-i-iii', 3],
      ['agsci-2023-ol-q13aii', 12], ['agsci-2023-ol-q16ai', 12]] as const) expect(live.get(id)?.totalMarks, id).toBe(marks);
    // 2022 Higher Q16(c)(i) regains its published 11 marks; the other corrections keep their totals.
    for (const [id, marks] of [['agsci-2022-hl-q16ci', 11], ['agsci-2022-hl-q2b', 6], ['agsci-2022-hl-q15ai', 6], ['agsci-2022-hl-q17ai', 9]] as const) {
      expect(live.get(id)?.totalMarks, id).toBe(marks);
    }
    // 2022 Ordinary corrections keep each original's ID and total; Q4(b) absorbs its five statement cards.
    for (const [id, marks] of [['agsci-2022-ol-q4b', 10], ['agsci-2022-ol-q14civ', 11], ['agsci-2022-ol-q16bii', 15], ['agsci-2022-ol-q18ai', 12],
      ['agsci-2022-ol-q2ai', 6], ['agsci-2022-ol-q7aiii', 4]] as const) expect(live.get(id)?.totalMarks, id).toBe(marks);
    for (const key of ['i', 'ii', 'iii', 'iv', 'v']) expect(live.has(`agsci-2022-ol-q4b${key}`)).toBe(false);
    // 2021 Higher corrections keep each original's ID and total.
    for (const [id, marks] of [['agsci-2021-hl-q1b', 4], ['agsci-2021-hl-q11bii', 6], ['agsci-2021-hl-q14bii', 6], ['agsci-2021-hl-q16b', 12],
      ['agsci-2021-hl-q17biv', 8], ['agsci-2021-hl-q18a-crop-preservation', 4]] as const) expect(live.get(id)?.totalMarks, id).toBe(marks);
    // 2021 Ordinary corrections keep each original's ID; Q18(a)(i) Seedbed preparation regains the named-crop 2 marks.
    for (const [id, marks] of [['agsci-2021-ol-q18a-i-seedbed', 9], ['agsci-2021-ol-q12b', 2], ['agsci-2021-ol-q14b-iii', 3], ['agsci-2021-ol-q16c-v', 4],
      ['agsci-2021-ol-q4c', 4], ['agsci-2021-ol-q8b-iii', 6]] as const) expect(live.get(id)?.totalMarks, id).toBe(marks);
  });

  it('adds exactly the reviewed Construction tasks to the frozen pre-audit set', () => {
    // Frozen pre-audit Construction set: 255 Higher + 250 Ordinary, counted and
    // hashed above. Every source-reviewed task is an explicit addition on top.
    const live = [...CONS_HIGHER, ...CONS_ORDINARY];
    const liveIds = new Set(live.map(card => card.id));
    for (const id of constructionAdditionIds) expect(liveIds.has(id), `missing reviewed addition ${id}`).toBe(true);
    expect(live.filter(card => !constructionAdditionIds.has(card.id))).toHaveLength(255 + 250 - constructionAliasIds.length);
    expect(live).toHaveLength(255 + 250 - constructionAliasIds.length + constructionAdditionIds.size);
    for (const id of constructionAliasIds) expect(liveIds.has(id), `${id} should be withdrawn behind its alias`).toBe(false);
  });

  it('preserves every consolidated card identity through an explicit progress alias', () => {
    const liveIds = new Set(decks.flatMap(([, cards]) => cards.map(card => card.id)));
    /* 54 earlier aliases + 68 Art per-option cards (2026-10-12) + 36 Economics consolidations from the 2021-2025
     * physical review, each a frozen half of a jointly priced answer (or a
     * duplicate route) withdrawn onto the card that now carries its progress:
   *   econ-2021-hl-q12-a-ii-neg -> q12-a-ii-pos
   *   econ-2021-hl-q16-b-ii-economic -> q16-b-ii-social
   *   econ-2022-hl-sa-q6-a-i -> sa-q6-a-b
   *   econ-2022-hl-sa-q6-a-ii -> sa-q6-a-b
   *   econ-2022-hl-q11-c-iii-against -> q11-c-iii-for
   *   econ-2022-ol-q12-a-ii -> q12-a-i
   *   econ-2022-ol-sa-q3-ii -> sa-q3-i
   *   econ-2022-ol-sa-q8-ii -> sa-q8-i
   *   econ-2022-ol-q14-b-ii-water -> q14-b-i
   *   econ-2023-hl-sa-q2-c-dis -> sa-q2-c-adv
   *   econ-2023-hl-q11-a-iii-pos -> q11-a-iii-neg
   *   econ-2023-hl-q12-b-iii-dis -> q12-b-iii-adv
   *   econ-2023-hl-q16-c-i-against -> q16-c-i-for
   *   econ-2023-ol-sa-q10-social -> sa-q10-private
   *   econ-2023-ol-q14-a-ii-effect -> q14-a-ii-reason
   *   econ-2024-hl-sa-q6-b-up -> sa-q6-b-down
   *   econ-2024-hl-sa-q9-a-benefit -> sa-q9-a-cost
   *   econ-2024-hl-q13-b-iii-neg -> q13-b-iii-pos
   *   econ-2024-hl-q13-c-iii-neg -> q13-c-iii-pos
   *   econ-2024-hl-q14-c-i-debt -> q14-c-i-spending
   *   econ-2024-hl-q15-c-ii-social -> q15-c-ii-economic
   *   econ-2024-hl-q16-c-ii-benefit -> q16-c-ii-cost
   *   econ-2024-hl-q16-c-iii-disadvantage -> q16-c-iii-advantage
   *   econ-2025-hl-sa-q1-a-against -> sa-q1-a-for
   *   econ-2025-hl-sa-q4-a-bad -> sa-q4-a-good
   *   econ-2025-hl-sa-q4-b-cons -> sa-q4-b-gov
   *   econ-2025-hl-q11-b-iii-dis -> q11-b-iii-adv
   *   econ-2025-hl-q12-a-ii-gov -> q12-a-ii-tax
   *   econ-2025-hl-q12-c-i-employer -> q12-c-i-employee
   *   econ-2025-hl-q13-a-ii-challenge -> q13-a-ii-benefit
   *   econ-2025-ol-sa-q6-social -> sa-q6-private
   *   econ-2025-ol-sa-q8-ii -> seca-q8-i-ticks
   *   econ-2025-ol-q16-b-i-ind -> q16-b-i-ag
   *   econ-2024-ol-sa-q1-ii -> sa-q1-i
   *   econ-2024-ol-sa-q8-ii -> sa-q8-i
   *   econ-2024-ol-q16-b-ii-dis -> q16-b-ii-adv
     */
    // ...plus 9 Agricultural Science per-item cards consolidated into one
    // printed task (agsci- keys, the review ledger's withdrawnCardIds), and the
    // Construction Studies per-item cards consolidated into one printed choice
    // (cons- keys, counted from the alias file itself), and the 125 English
    // legacy cards withdrawn by the bridge onto a reviewed card (english- keys
    // listed in bridgedLegacyIds; the 10 earlier english- keys are in the 158).
    expect(agriAliasIds).toHaveLength(9);
    expect(constructionAliasIds).toHaveLength(58);
    expect(englishAliasIds).toHaveLength(125);
    // ...and the 2 Biology shipped ids a paper-by-paper review withdrew (bio- keys).
    expect(biologyAliasIds).toHaveLength(2);
    expect(Object.keys(CARD_ID_ALIASES)).toHaveLength(158 + agriAliasIds.length + constructionAliasIds.length
      + englishAliasIds.length + biologyAliasIds.length);
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
        && !name.startsWith('applied-maths:')
        && !name.startsWith('german:')
        && !name.startsWith('spanish:')
        && !name.startsWith('italian:')
        && !name.startsWith('russian:')
        && !name.startsWith('japanese:')
        && !name.startsWith('classical-studies:')
        && !name.startsWith('latin:')
        && !name.startsWith('polish:')
        && !name.startsWith('arabic:')
        && !name.startsWith('portuguese:')
        && !name.startsWith('romanian:')
        && !name.startsWith('dutch:')
        && !name.startsWith('lithuanian:')
        && !name.startsWith('latvian:')
        && !name.startsWith('czech:')
        && !name.startsWith('ancient-greek:')
        && !name.startsWith('modern-greek:')
        && !name.startsWith('bulgarian:')
        && !name.startsWith('croatian:')
        && !name.startsWith('danish:')
        && !name.startsWith('estonian:')
        && !name.startsWith('finnish:')
        && !name.startsWith('hungarian:')
        && !name.startsWith('mandarin-chinese:')
        && !name.startsWith('slovakian:')
        && !name.startsWith('slovenian:')
        && !name.startsWith('swedish:')
        && !name.startsWith('ukrainian:')
        && !name.startsWith('dcg:')
        && !name.startsWith('physical-education:')
        && !name.startsWith('politics-and-society:') && !name.startsWith('accounting:'))
      // Business counts its frozen set; Economics (and Agricultural Science,
      // Construction, English and Biology) its live frozen cards, its withdrawn halves
      // counted once, as the alias keys below; Art counts
      // its original cards (its added years are new cards, not part of this
      // earlier bank).
      .reduce((total, [name, cards]) => total + (name.startsWith('business:')
        ? frozenIds(name, cards).length
        : name.startsWith('art:') ? cards.filter(card => !isArtAdded(card.id)).length
          : liveFrozenCount(name, cards)), 0);
    expect(preNewSubjectCards + Object.keys(CARD_ID_ALIASES).length).toBe(9_768);
  });

  it('adds reviewed English papers without replacing any legacy card id or alias', () => {
    const published = new Set([...publishedEnglishHigher.cards, ...publishedEnglishOrdinary.cards]
      .map(card => card.id));
    expect(published.size).toBe(2_685);
    // No route card is published: a printed choice marked identically is one card.
    expect([...published].some(id => id.includes('-route-'))).toBe(false);
    // Legacy ids of bridged papers (2025 HL) are no longer served as legacy
    // cards: each is kept by its reviewed published card or is a progress alias.
    const bridged = [...publishedEnglishHigher.bridgedLegacyIds, ...publishedEnglishOrdinary.bridgedLegacyIds];
    const bridgeAliases: Record<string, string> = {
      ...publishedEnglishHigher.bridgeAliases, ...publishedEnglishOrdinary.bridgeAliases };
    expect(bridged).toHaveLength(650);
    for (const id of bridged) {
      const kept = published.has(id) && !(id in bridgeAliases);
      const aliased = CARD_ID_ALIASES[id] === bridgeAliases[id] && published.has(bridgeAliases[id]);
      expect(kept || aliased, `${id} must be kept or aliased`).toBe(true);
    }
    // The legacy 2021-2025 decks keep exactly their previous frozen identities:
    // the still-legacy cards plus the bridged ids reproduce the frozen hashes.
    const legacyIds = (cards: readonly { id: string }[], level: 'hl' | 'ol') => [
      ...cards.filter(card => !published.has(card.id)),
      ...bridged.filter(id => /^english-\d{4}-(hl|ol)-/.exec(id)?.[1] === level).map(id => ({ id })),
    ];
    expect(identityHash(legacyIds(ENGLISH_HIGHER, 'hl')))
      .toBe('231477c3f869811a39610398ed61ff14a4f3e5f087ebaa053a5d1b8daabc3df0');
    expect(identityHash(legacyIds(ENGLISH_ORDINARY, 'ol')))
      .toBe('9e667c2b7181e951fcb7b875ab7a0fb009f5db1389d75d89131dacebbc90994f');
    for (const [oldId, canonicalId] of Object.entries(CARD_ID_ALIASES)) {
      expect(published.has(oldId), `${oldId} is a withdrawn alias`).toBe(false);
      if (oldId.startsWith('english-')) expect(published.has(canonicalId)).toBe(bridgeAliases[oldId] === canonicalId);
    }
    const papers = [...publishedEnglishHigher.papers, ...publishedEnglishOrdinary.papers].map(paper => paper.paperId);
    expect([...published].every(id => papers.some(paper => id.startsWith(`${paper}-`)))).toBe(true);
    // Reviewed additions on top of the frozen 650: 548 Higher + 1,612 Ordinary,
    // none reusing a frozen ID or an alias key.
    const added = (level: string) => [...englishAdditionIds].filter(id => id.includes(level)).length;
    const aliased = (level: string) => englishAliasIds.filter(id => id.includes(level)).length;
    expect([added('-hl-'), aliased('-hl-'), added('-ol-'), aliased('-ol-')]).toEqual([548, 20, 1612, 105]);
    for (const id of englishAdditionIds) expect(id in CARD_ID_ALIASES, `${id}: addition reuses an alias key`).toBe(false);
    expect(ENGLISH_HIGHER).toHaveLength(210 - aliased('-hl-') + added('-hl-'));
    expect(ENGLISH_ORDINARY).toHaveLength(440 - aliased('-ol-') + added('-ol-'));
  });

  it('adds the reviewed Biology sittings on top of the frozen 2021-2025 set without replacing an id', () => {
    // Every card id names its own sitting, which is what isBiologyAdded reads.
    expect(BIO_HIGHER.every(card => card.id.startsWith(`bio-${card.year}-hl-`))).toBe(true);
    expect(BIO_ORDINARY.every(card => card.id.startsWith(`bio-${card.year}-ol-`))).toBe(true);
    // A shipped id a review withdraws survives as a progress alias; restored,
    // the 2021-2025 set is exactly the one pinned before the reviews (above).
    expect(biologyAliasIds.filter(id => id.includes('-hl-'))).toEqual(['bio-2024-hl-q8-b2']);
    expect(biologyAliasIds.filter(id => id.includes('-ol-'))).toEqual(['bio-2025-ol-q16-ciii-fig']);
    for (const id of biologyAdditionIds) expect(id in CARD_ID_ALIASES, `${id}: addition reuses an alias key`).toBe(false);
    // The live decks, pinned whole (their history is beside the frozen pins).
    expect(BIO_HIGHER).toHaveLength(2261);
    expect(identityHash(BIO_HIGHER)).toBe('8e30a3e6126a5253419bf9bc838f8bc8db205b85040333321fe95c3c536235f9');
    expect(BIO_ORDINARY).toHaveLength(2395);
    expect(identityHash(BIO_ORDINARY)).toBe('dfa89a0dd2e483f7eb7fe3cc3472edf1ebb1eaa123670d7ddf715c989a5d6d2e');
    expect(biologyAdditionIds.size).toBe(2261 + 2395 - (673 - 1) - (686 - 1));
    // The sittings before 2021 had no Biology cards: everything they carry is new.
    expect(BIO_HIGHER.filter(card => card.year <= 2020)).toHaveLength(1183);
    expect(BIO_ORDINARY.filter(card => card.year <= 2020)).toHaveLength(1303);
    expect(BIO_HIGHER.filter(card => card.year === 2026)).toHaveLength(188);
    expect(BIO_ORDINARY.filter(card => card.year === 2026)).toHaveLength(187);
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

  it('added the Art choose-two routes without replacing an id, and withdrew them onto Q4(a)', () => {
    // The nine heading-pair routes were added on top of the original Ordinary
    // identity; one card per printed task now withdraws them onto
    // art-2025-ol-q4-a, so they live on as alias keys of the frozen set.
    const frozen = frozenIds('art:ordinary', ART_ORDINARY);
    const routes = new Set(frozen.filter(id => id.startsWith('art-2025-ol-q4-a-')));
    expect(routes.size).toBe(9);
    for (const id of routes) expect(CARD_ID_ALIASES[id]).toBe('art-2025-ol-q4-a');
    expect(idHash(frozen.filter(id => !routes.has(id))))
      .toBe('e5403f6e685e0133ad94ef321f97a77f96127c2ee3570395e00662d7719ddbd5');
  });
});
