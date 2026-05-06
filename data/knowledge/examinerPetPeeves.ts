/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 *
 * Examiner pet-peeves drawn from Chief Examiner Reports.
 * Source: /docs/leaving-cert-knowledge-dossier.md § B1-B11 + § D.
 *
 * Per /CLAUDE.md content quality rules: no more than 15 words verbatim
 * per source. Each `peeve` here is paraphrased.
 */

import { type ExaminerPetPeeve } from '../../types/knowledge';

export const EXAMINER_PET_PEEVES: ExaminerPetPeeve[] = [
  {
    id: 'eng-formulaic',
    subject: 'English',
    peeve: 'Over-rehearsed, formulaic essays that ignore the specific question.',
    reportYear: 2013,
    example: 'A student lifts a memorised "Cultural Context" essay onto every Comparative question, regardless of the modifier in the actual prompt.',
    fix: 'Read the modifier first. Rewrite the question in your own words at the top of your answer to anchor what is actually being asked.',
    source: { section: 'B1', page: 8, cite: 'English Chief Examiner Report 2013' },
  },
  {
    id: 'eng-comparative-serial',
    subject: 'English',
    peeve: 'Comparative essays treated serially — "all of Text A, then all of Text B".',
    reportYear: 2013,
    example: 'A 7-page essay on the cultural context of Text 1, then 5 pages on Text 2, then 3 pages on Text 3. The texts never speak to each other.',
    fix: 'Frame each paragraph as an integrated comparative point: "Both X and Y deal with Z; in Text A this manifests as..., whereas in Text B...".',
    source: { section: 'B1', page: 8, cite: 'English CER — Comparative Studies' },
  },
  {
    id: 'lang-rote-oral',
    subject: 'Modern Languages',
    peeve: 'Rote-learned blocks of memorised material in the oral exam.',
    reportYear: 2016,
    example: 'Asked "What is your favourite hobby?" — student launches into a memorised paragraph about playing GAA that does not match the question\'s actual tense or detail.',
    fix: 'Listen for the tense and the specific question word before answering. Generate a new sentence from familiar vocabulary, not a recited block.',
    source: { section: 'B8', page: 13, cite: '2016 SEC CER — French / Spanish / Italian' },
  },
  {
    id: 'maths-no-working',
    subject: 'Maths',
    peeve: 'Working not shown — final answer alone, no procedural steps visible.',
    reportYear: 2015,
    example: 'A student writes "x = 4" with nothing else. The answer is wrong, but they had the correct formula on the page if they had only written it down.',
    fix: 'Always write the formula from the Tables and Formulae booklet first. That alone earns the attempt mark — typically 30-40% of the part\'s marks.',
    source: { section: 'B2', page: 9, cite: '2015 Maths Chief Examiner Report' },
  },
  {
    id: 'geo-overrun-shortq',
    subject: 'Geography',
    peeve: 'Spending 30 minutes on the short questions when 20 is enough — time taken from later essays.',
    reportYear: 2012,
    example: 'A student finishes Q1-Q12 (80 marks) at 10:45 when the budget was 10:30. They lose 15 minutes from their 80-mark option essay.',
    fix: 'Use a watch. Short questions get 20-25 minutes max. The option essay needs 35-40.',
    source: { section: 'B6', page: 12, cite: '2012 Geography CER' },
  },
  {
    id: 'biz-abq-no-quote',
    subject: 'Business',
    peeve: 'ABQ answers with theory and application but no direct quote from the case study.',
    reportYear: 2025,
    example: 'A student explains "demographic segmentation" and applies it to the case study generally, but never quotes a specific phrase from the text. The marker cannot award the link mark.',
    fix: 'Identify a direct quote from the case before writing each ABQ point. Theory → Explanation → "Quote in inverted commas".',
    source: { section: 'B7', page: 12, cite: '2025 Business HL Marking Scheme — ABQ link rule' },
  },
  {
    id: 'maths-force-given',
    subject: 'Maths',
    peeve: 'Forcing the answer when the question already gives it — manipulating working to fit.',
    reportYear: 2015,
    example: 'Question: "Show that x = 5". Student gets x = 4.7 in working but writes "= 5" because that is what was asked. The examiner sees the manipulation and awards no marks.',
    fix: 'State your conclusion based on your own work. If your value differs from the given one, write what you got — partial credit is preserved.',
    source: { section: 'B2', page: 9, cite: '2015 Maths Chief Examiner Report' },
  },
  {
    id: 'sci-missing-keyphrase',
    subject: 'Sciences',
    peeve: 'Definitions missing the specific syllabus key phrase the marking scheme is hunting.',
    reportYear: 2024,
    example: '"Isotope" answered as "an atom of an element with a different mass". The marking scheme requires "same atomic number but different mass numbers" — the answer is incomplete.',
    fix: 'Memorise the exact syllabus key phrases for every definition. Bullet form is fine. The marking scheme lists the acceptable phrasings.',
    source: { section: 'B4', page: 10, cite: 'Chemistry / Biology marking-scheme convention' },
  },
  {
    id: 'acc-calculator-trap',
    subject: 'Accounting',
    peeve: 'The "calculator trap" — adjustments calculated mentally with only the final figure on the page.',
    reportYear: 2024,
    example: 'A student calculates depreciation in their head and writes only "€5,000" on the P&L. The figure is wrong; without W1 working visible, no partial credit can be awarded.',
    fix: 'Every adjustment gets a labelled working: "W1: Depreciation = (Cost − Residual) ÷ Life = ...". Cross-reference the workings into the main account.',
    source: { section: 'B7', page: 13, cite: 'Accounting marking-scheme convention' },
  },
  {
    id: 'universal-generic',
    subject: 'All subjects',
    peeve: 'Generic, prepared answers that do not engage with the specific question asked.',
    reportYear: 2017,
    example: 'A student writes a beautifully memorised essay on the historical context of WWI; the question asked specifically about economic causes between 1914-1918. The modifier is ignored.',
    fix: 'Underline the question modifier (e.g. "economic", "between 1914 and 1918") before writing. Rewrite the question in your own words above your answer to confirm the demand.',
    source: { section: 'D', page: 17, cite: 'Cross-CER perennial complaint, every subject' },
  },
  {
    id: 'eng-genre-confusion',
    subject: 'English',
    peeve: 'Composition genre misjudged — discursive essay written as personal essay, or vice versa.',
    reportYear: 2013,
    example: 'A "Discursive essay on whether privacy is desirable" is written as a personal essay full of "I" and anecdote. The genre register is wrong from sentence one.',
    fix: 'Read the genre prescribed in the prompt before writing. Discursive = weigh multiple views. Personal = first-person reflection. Speech = oral register and direct address.',
    source: { section: 'B1', page: 8, cite: 'English Composition CER' },
  },
  {
    id: 'history-dbq-criticism',
    subject: 'History',
    peeve: 'Document-Based Question source criticism is weak — students fail to identify bias, propaganda, or limitations.',
    reportYear: 2017,
    example: 'A propaganda poster from WWII is described in surface detail. The student does not identify it as biased, does not name the audience, does not question reliability.',
    fix: 'Apply the "5 Ws" of source analysis habitually: Who, What, When, Where, Why. Use quotations from the document to demonstrate strengths and weaknesses.',
    source: { section: 'B5', page: 11, cite: '2017 History CER' },
  },
];
