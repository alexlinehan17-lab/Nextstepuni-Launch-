/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 *
 * Per-subject marking-scheme architecture for the Necessary Knowledge
 * "Marking Scheme Grammar Explainer" module.
 * Source: /docs/leaving-cert-knowledge-dossier.md § A2.
 */

import { type SubjectMarkingGrammar } from '../../types/knowledge';

export const SUBJECT_MARKING_GRAMMARS: SubjectMarkingGrammar[] = [
  {
    id: 'english-pclm',
    subjectLabel: 'English — PCLM + Purpose Ceiling',
    architecture:
      "Long answers — composition, comprehension Question B, Comparative essays — are marked across four bands totalling 100%. The Purpose Ceiling is the rule that catches more bright students than any other.",
    rules: [
      { title: 'P — Clarity of Purpose (30%)', body: 'Engagement with the actual task asked. The modifier in the question lives here.' },
      { title: 'C — Coherence of Delivery (30%)', body: 'Logical structure and sustained argument across the answer.' },
      { title: 'L — Efficiency of Language (30%)', body: 'Genre-appropriate, controlled language. A speech reads like a speech; a discursive essay weighs multiple views.' },
      { title: 'M — Mechanics (10%)', body: 'Spelling, grammar, punctuation. Strict — apostrophes, comma splices, run-ons all count.' },
      { title: 'The Purpose Ceiling — the killer rule', body: 'Marks for C or L cannot exceed the marks for P. From every English marking scheme verbatim. An off-question essay caps at the P mark, no matter how well written. Brilliant prose on the wrong question can score around 30%.' },
    ],
    workedExample: {
      setup: 'Beautifully written, wrong question. P = 8 / 30. C = 28 / 30 if marked alone. L = 28 / 30 alone. M = 8 / 10.',
      outcome: 'C and L cap at 8 (the P mark). Total = 8 + 8 + 8 + 8 = 32%.',
    },
    source: { section: 'A2', page: 4, cite: 'Every English marking scheme verbatim' },
  },
  {
    id: 'srp-system',
    subjectLabel: 'Geography / History / Business — SRP system',
    architecture:
      "Long answers in these subjects are marked in SRPs — Significant Relevant Points — typically worth 2 marks each. The marking grammar is mostly arithmetic: count the SRPs, hit the cap.",
    rules: [
      { title: 'SRP = 2 marks', body: 'A single piece of factual information that develops the question. Fluff and generalisation score 0.' },
      { title: '30-mark essay = 15 SRPs', body: 'Most teachers tell students to aim for 17 to be safe. The buffer absorbs SRPs the marker rejects as not "developing" the question.' },
      { title: 'Annotated diagrams earn SRPs', body: 'Label = 1 SRP. Annotation (a sentence explaining the process at that location) = additional SRP. Diagrams without annotation are worth less.' },
      { title: 'Context matters — same sentence, different score', body: 'The marking scheme says "each SRP should emerge from the information put forward by the candidate, leading to an overall coherent response". Identical sentences across two scripts may score differently if one builds toward the question and the other doesn\'t.' },
      { title: '"Max X SRPs if…" caps', body: 'The most punitive rule. Examples: "Max 7 SRPs if only one factor examined" → caps you at 14 / 30. "Max 2 SRPs if merely description without reference to formation" → caps at 4 / 30. Read the marking-scheme caps before writing.' },
    ],
    workedExample: {
      setup: 'Geography 30-mark essay. 14 SRPs at 2 marks each + a labelled-and-annotated diagram (1 + 1 SRP).',
      outcome: '14 × 2 + 2 = 30. Maximum reached.',
    },
    source: { section: 'A2', page: 4 },
  },
  {
    id: 'maths-attempt',
    subjectLabel: 'Maths — Attempt mark, Blunder, Slip, Misreading',
    architecture:
      "Each part has a published partial-credit scale. Penalties are explicit. The most important sentence in the entire scheme: 'if you write nothing the examiner cannot award any marks.'",
    rules: [
      { title: 'Attempt mark — 30-40% of the part\'s marks', body: 'For any correct, relevant first step. Including just writing the correct formula from the Tables and Formulae booklet.' },
      { title: 'Blunder (B) — minus 3 marks', body: 'Mathematical error or omission in working. The big penalty.' },
      { title: 'Slip (S) — minus 1 mark', body: 'Numerical slip — calculator error, transcription mistake.' },
      { title: 'Misreading (M) — minus 1 mark', body: 'If the misreading didn\'t oversimplify the question. If it did, you only get the attempt mark.' },
      { title: 'Standard scales', body: '5B (0,2,5) for short parts. 5C (0,2,3,5) for two-band partial credit. 10C (0,4,7,10) for three-band. 10D (0,3,5,8,10) for four-band — the most common 10-mark question.' },
      { title: 'Worthless work scores 0', body: 'Writing the question back, copying numbers without a relevant step, padding without progress — no marks.' },
    ],
    workedExample: {
      setup: '10-mark question on a 10D scale. Student writes the correct formula (4 marks). Substitutes correctly (5 marks). Makes a slip in the arithmetic — final answer wrong (-1 slip).',
      outcome: 'Final score: 7 / 10. The slip costs 1 mark, not the whole question. Showing working preserved 70% of the available marks despite the wrong answer.',
    },
    source: { section: 'A2', page: 3, cite: '2015 Maths CER + every Maths marking scheme' },
  },
  {
    id: 'accounting',
    subjectLabel: 'Accounting — Headings, Units, Cross-references',
    architecture:
      "Final accounts are marked on completeness of headings, units, and visible cross-referenced workings. The fastest-paced LC paper at 27 seconds per mark — there is no room for invisible work.",
    rules: [
      { title: 'Headings are mark-bearing', body: '"Profit & Loss Account", "For the year ended 31/12/20XX", "Authorised Capital". Typical penalty: minus 1 mark per omitted heading.' },
      { title: 'Units required', body: '€ sign and % sign must appear where applicable. Not optional — they\'re mark-bearing.' },
      { title: 'Workings cross-referenced (W1, W2…)', body: 'Adjustments calculated "in your head" with only the final figure visible — the calculator trap. If the figure is wrong, all partial marks are forfeited.' },
      { title: 'Time pressure: 0.45 mins per mark', body: '27 seconds per mark — the fastest-paced LC paper. Plan the time per question before you start writing.' },
    ],
    workedExample: {
      setup: 'Adjustment for depreciation. Student writes only "€5,000" on the P&L. The correct figure is €4,800.',
      outcome: 'Without W1 working visible, no partial credit. The student loses 4 marks — the entire adjustment. With "W1: Depreciation = (Cost − Residual) ÷ Life = ...", they would have earned 3 of those 4 even with the wrong final figure.',
    },
    source: { section: 'A2', page: 5 },
  },
  {
    id: 'sciences',
    subjectLabel: 'Sciences (Biology / Chemistry / Physics) — Key-phrase matching',
    architecture:
      "Definitions, explanations, and worked answers are matched against key-phrase lists in the marking scheme. Bullet-point format is preferred — examiners can find key points faster.",
    rules: [
      { title: 'Key phrases are non-negotiable', body: 'Chemistry "isotope" must include "same atomic number but different mass numbers". Biology "function of myelin sheath" = "to insulate" or "to speed up the transmission". Missing a phrase = lost mark.' },
      { title: 'Bullet points preferred over prose', body: 'Examiners can find key points faster, and the question demands "5 key points" type answers. Prose buries the marks.' },
      { title: 'Diagrams = 9 marks (Biology)', body: '6 for the diagram + 3 for labelling. Title required.' },
      { title: 'Units in scientific calculations', body: 'Missing units commonly costs the final mark. Wrong unit (cm³ instead of m³ in pV = nRT) is one of the most common Physics / Chemistry errors. Temperature in Kelvin in gas-law calculations.' },
      { title: 'State symbols (s, l, g, aq)', body: 'Required in thermochemical equations like Heat of Formation. Missing them costs marks.' },
    ],
    workedExample: {
      setup: 'Chemistry: "Define isotope." Student writes: "an atom of an element with a different mass."',
      outcome: 'Missing "same atomic number". The marking scheme key-phrase list rejects this answer — partial credit only. The full key phrase is "same atomic number but different mass numbers".',
    },
    source: { section: 'A2', page: 5 },
  },
];
