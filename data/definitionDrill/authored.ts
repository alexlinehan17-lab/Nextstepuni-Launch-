/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 *
 * Definition Drill — AUTHORED-BUT-STRICTLY-CITED extension.
 *
 * Most Definition Drill cards are a projection of the Marking Lens corpus
 * (see ./index.ts). A few high-value definitions live in filed SEC schemes that
 * are NOT yet in the Marking Lens corpus (e.g. Biology, whose lens entries are
 * marks-only for these terms). Each entry below was verified verbatim against
 * the named filed scheme in /examiner-reports/ — the `answer` is the scheme's
 * own mark-earning wording, nothing added. These carry an `authored|…` id so the
 * integrity gate can tell them from projected entries; they still pass the
 * SEC-attribution and real-wording gates.
 *
 * Verification trail (line ranges are into the filed .md at review time):
 *  - biology enzyme    — 2023 HL Q15(c)(i) "What is an enzyme?" → "Protein
 *    catalyst" (3). examiner-reports/biology/2023-marking-scheme.md.
 *  - biology osmosis   — 2025 HL Q9(a) "Explain the term osmosis." → "Movement
 *    of water (2); from a region of higher water concentration to a region of
 *    lower water concentration across a selectively permeable membrane (4)".
 *    examiner-reports/biology/2025-hl-marking-scheme.md.
 *  - chemistry acid    — 2025 HL Q7(a)(i) "Explain how an acid differs from a
 *    base according to the Brønsted-Lowry theory." → the acid element is
 *    "proton donor (2)". examiner-reports/chemistry/2025-marking-scheme.md.
 */

import type { DrillDefinition } from './index';

export const AUTHORED_DEFINITIONS: DrillDefinition[] = [
  {
    id: 'authored|biology|enzyme',
    term: 'an enzyme',
    prompt: 'What is an enzyme?',
    answer: 'Protein catalyst (3m).',
    marks: 3,
    subjectId: 'biology',
    subjectLabel: 'Biology',
    source: 'SEC Marking Scheme 2023, Biology Higher Level, Q15(c)(i) — © State Examinations Commission',
  },
  {
    id: 'authored|biology|osmosis',
    term: 'osmosis',
    prompt: 'Explain the term osmosis.',
    answer:
      'Movement of water (2m); from a region of higher water concentration to a region of lower water concentration, across a selectively permeable membrane (4m).',
    marks: 6,
    subjectId: 'biology',
    subjectLabel: 'Biology',
    source: 'SEC Marking Scheme 2025, Biology Higher Level, Q9(a) — © State Examinations Commission',
  },
  {
    id: 'authored|chemistry|acid-bronsted-lowry',
    term: 'an acid (Brønsted–Lowry)',
    prompt: 'Define an acid according to the Brønsted–Lowry theory.',
    // The 2025 scheme frames the question as "how an acid differs from a base";
    // the acid element it awards is "proton donor (2)".
    answer: 'Proton donor (2m).',
    marks: 2,
    subjectId: 'chemistry',
    subjectLabel: 'Chemistry',
    source: 'SEC Marking Scheme 2025, Chemistry Higher Level, Q7(a)(i) — © State Examinations Commission',
  },
];
