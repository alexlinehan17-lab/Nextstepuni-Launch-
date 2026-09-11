/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 *
 * How many options one best-of menu may show. Mirrors optionCapFor in
 * types/markBank.ts, which the build cannot import because it is TypeScript.
 * test/markBankDeck.test.ts asserts the two agree.
 */
export const MAX_OPTION_ROWS = 8;
// 2017 Construction Studies HL Q4(a) prints sixteen distinct acceptable
// functional requirements. The ceiling must cover the largest verified SEC
// menu; trimming it would make a correct answer impossible to self-mark.
export const MAX_LONG_OPTION_ROWS = 16;

/** Business Section 3 (Higher) and Section 2 (Ordinary); Sections B and C in
 *  the sciences. Keyed on the section, because a long question's individual
 *  parts are small while the menu the examiner prints for them is not. */
// German's reading comprehensions are long questions whose PARTS are small:
// the 2022 Higher TEXT I theme question prints twenty-six accepted points
// for ten marks and its 1(a) prints nine for six, so the section tokens the
// German deck cites — TEXT I, II and III — belong here too.
// Russian's reading and language-awareness questions are long questions whose
// PARTS are small: the 2025 Higher summary question prints seventeen accepted
// points for its eight content marks and the semantic-field task eighteen
// Russian words for ten. Its section tokens name the printed question rather
// than a letter (UNIT_NAME in ru_scheme.py), so they belong here too.
// The Baltic languages' reading tasks are long questions whose PARTS are
// small: 2024 Higher Lithuanian answers a five-mark "find one past-frequentative
// verb" with eleven verbs and 2022 Ordinary answers a five-mark "write one thing
// Jonas does in New York" with thirteen. One task is one printed text with up to
// eleven asks on it, which is what makes the examiner print a long menu, so the
// task tokens 'U1' to 'U3' (užduotis — the paper's own word for it) belong here.
const LONG_SECTIONS = new Set(['2', '3', 'B', 'C', 'T1', 'T2', 'T3',
  'C1', 'C2', 'CD', 'IR1', 'IR2', 'LA1', 'LA2', 'CA1',
  'U1', 'U2', 'U3']);

export const optionCapFor = (section) =>
  LONG_SECTIONS.has(section) ? MAX_LONG_OPTION_ROWS : MAX_OPTION_ROWS;
