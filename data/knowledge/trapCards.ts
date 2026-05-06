/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 *
 * Trap cards for the Spot the Trap module (Stage 2, E4).
 *
 * 15 paraphrased past-paper-style questions, each with:
 *   - the trap span (the word, phrase, or modifier most students miss)
 *   - the trap category (for pattern recognition)
 *   - why students miss it
 *   - the marking-scheme consequence (capped marks, lost band, slip, etc.)
 *
 * Per /CLAUDE.md content rule: question text paraphrased, never more
 * than 15 words verbatim from any SEC paper.
 *
 * Sources:
 * - English CERs 2008/2013 (modifier and Comparative trap patterns)
 * - 2015 Maths CER (plural values, in-terms-of)
 * - Chemistry / Biology marking schemes (definition keyphrases, state
 *   symbols)
 * - Geography 2012 CER (process vs landform, named example)
 * - 2016 French/Spanish/Italian CER (tense disguise)
 * - History 2017 CER (date precision in DBQ)
 */

import { type TrapCard } from '../../types/knowledge';

/** Helper — find the index range of a substring within a string for the
 *  `trapSpans` field. The lookup is exact (case-sensitive). */
function span(text: string, needle: string): { start: number; end: number } {
  const start = text.indexOf(needle);
  if (start === -1) {
    // Should never happen; keeps the data file safe even if a typo creeps in.
    return { start: 0, end: 0 };
  }
  return { start, end: start + needle.length };
}

// ─── English (4) ────────────────────────────────────────────────────
const eng1 = '"Discuss the effective use of disturbing imagery in the poem."';
const eng2 = '"How does the writer present the deeply embedded values of the family?"';
const eng3 = '"Refer to all three of the texts on your comparative course in your answer."';
const eng4 = '"Outline the writer\'s purpose, and explain how language is used to achieve it."';

// ─── Maths (3) ──────────────────────────────────────────────────────
const m1 = '"Find the values of x: x² − 7x + 12 = 0."';
const m2 = '"Express y in terms of x and z."';
const m3 = '"Solve for x when x is restricted to integer values: 2x² − 5x − 3 = 0."';

// ─── Chemistry (3) ──────────────────────────────────────────────────
const c1 = '"Define an isotope."';
const c2 = '"Write a balanced equation for the combustion of methane, including state symbols."';
const c3 = '"State the colour change at the end-point of the titration."';

// ─── Geography (2) ──────────────────────────────────────────────────
const g1 = '"Describe one named feature of coastal erosion."';
const g2 = '"Examine the impact of human activity on a named region you have studied."';

// ─── French (2) ─────────────────────────────────────────────────────
const f1 = '"Décris ta journée typique l\'année dernière."';
const f2 = '"Que ferais-tu si tu gagnais à la loterie?"';

// ─── History (1) ────────────────────────────────────────────────────
const h1 = '"With reference to the documents, account for events between 1916 and 1918."';

export const TRAP_CARDS: TrapCard[] = [
  {
    id: 'eng-modifier-effective',
    subject: 'English',
    category: 'modifier',
    paperLabel: 'English HL Paper 2 — poetry',
    questionText: eng1,
    trapSpans: [span(eng1, 'effective')],
    trapLabel: '"Effective" demands evaluation, not identification.',
    whyStudentsMiss: 'Most students treat the question as "Discuss the use of disturbing imagery" and just identify examples. The modifier "effective" requires you to evaluate how well the imagery works.',
    consequence: 'Without evaluation, the answer caps at the Purpose mark. The Purpose Ceiling rule then pulls Coherence and Language down to the same level — a beautifully written non-evaluation can score 30%.',
    marksAtRiskPct: 50,
    source: { section: 'B1', page: 8, cite: 'English CER — modifier awareness' },
  },
  {
    id: 'eng-modifier-deeply',
    subject: 'English',
    category: 'modifier',
    paperLabel: 'English HL Paper 2 — single text',
    questionText: eng2,
    trapSpans: [span(eng2, 'deeply embedded')],
    trapLabel: '"Deeply embedded" intensifier — surface analysis caps the band.',
    whyStudentsMiss: 'Students answer "what are the family\'s values?" The intensifier asks for structural patterns running through the text — recurring imagery, voice patterns, what the text presupposes — not a list.',
    consequence: 'Surface-level value-listing caps Purpose marks below the top band. The Coherence and Language ceilings then follow.',
    marksAtRiskPct: 30,
    source: { section: 'B1', page: 8, cite: 'English CER 2013 — over-rehearsed formulaic responses' },
  },
  {
    id: 'eng-plural-three-texts',
    subject: 'English',
    category: 'plural-singular',
    paperLabel: 'English HL Paper 2 — Comparative',
    questionText: eng3,
    trapSpans: [span(eng3, 'all three')],
    trapLabel: '"All three" — answering on two caps the mark.',
    whyStudentsMiss: 'The student who has studied two texts more deeply than the third answers strongly on two and gestures at the third — or skips it entirely. The English Chief Examiner is explicit: "you cannot answer on two films".',
    consequence: 'A two-text answer to a three-text question typically caps near 50%. Comparative is 70 marks — a 50% cap costs 17 marks.',
    marksAtRiskPct: 50,
    source: { section: 'A5', page: 7, cite: 'English Comparative Studies CER' },
  },
  {
    id: 'eng-command-switch-and',
    subject: 'English',
    category: 'command-switch',
    paperLabel: 'English HL Paper 1 — Comprehension',
    questionText: eng4,
    trapSpans: [span(eng4, 'and explain how language is used')],
    trapLabel: 'Two commands joined by "and" — both must be addressed.',
    whyStudentsMiss: 'Students read the first command ("Outline the writer\'s purpose") and answer it well. They miss that "explain how language is used" is a separate command with its own mark allocation.',
    consequence: 'Half the marks are tied to the second clause. Answering only the first caps you at 50% no matter how well written.',
    marksAtRiskPct: 50,
    source: { section: 'A1', page: 3, cite: 'Cross-LC paired-command convention' },
  },
  {
    id: 'maths-plural-values',
    subject: 'Maths',
    category: 'plural-singular',
    paperLabel: 'Maths HL Paper 1 — algebra',
    questionText: m1,
    trapSpans: [span(m1, 'values')],
    trapLabel: '"Values" — plural — means both roots.',
    whyStudentsMiss: 'Students factor the equation, find x = 3, and stop. They miss the second root x = 4. The plural cue is the only signal.',
    consequence: 'The marker awards work-of-merit (+1 in step 4) but withholds the plural-roots mark. Typically 50% of the part is at risk.',
    marksAtRiskPct: 50,
    source: { section: 'B2', page: 9, cite: '2015 Maths CER — answer in the required form' },
  },
  {
    id: 'maths-in-terms-of',
    subject: 'Maths',
    category: 'in-terms-of',
    paperLabel: 'Maths HL Paper 1 — algebra',
    questionText: m2,
    trapSpans: [span(m2, 'in terms of x and z')],
    trapLabel: '"In terms of" — answer must be algebraic.',
    whyStudentsMiss: 'Students substitute numerical values for x and z and give a number. The phrase requires the answer to remain a function of x and z — keep them as letters.',
    consequence: 'A numerical answer is wrong by form, not by computation. The marker treats this as a misread (−1) at minimum, more often a blunder (−3) for ignoring the directive.',
    marksAtRiskPct: 30,
    source: { section: 'B2', page: 9 },
  },
  {
    id: 'maths-restricted-domain',
    subject: 'Maths',
    category: 'plural-singular',
    paperLabel: 'Maths HL Paper 1 — quadratic',
    questionText: m3,
    trapSpans: [span(m3, 'restricted to integer values')],
    trapLabel: '"Restricted to integer values" — non-integer roots are rejected.',
    whyStudentsMiss: 'The student factors and finds x = 3 and x = −0.5. They write both. The restriction says only x = 3 is admissible.',
    consequence: 'Including the rejected root (−0.5) earns work-of-merit but loses the final-answer mark. Typically 20-30% of the part.',
    marksAtRiskPct: 25,
    source: { section: 'B2', page: 9 },
  },
  {
    id: 'chem-define-isotope',
    subject: 'Chemistry',
    category: 'definition-keyphrase',
    paperLabel: 'Chemistry HL — definition',
    questionText: c1,
    trapSpans: [span(c1, 'isotope')],
    trapLabel: 'Definition requires both key phrases.',
    whyStudentsMiss: 'Students write "an atom of an element with different mass" or similar. The marking scheme requires "same atomic number" AND "different mass numbers" — both phrases.',
    consequence: 'Missing either phrase loses one of the two marks. The full definition is non-negotiable per the marking scheme.',
    marksAtRiskPct: 50,
    source: { section: 'B4', page: 10, cite: 'Chemistry marking-scheme convention' },
  },
  {
    id: 'chem-state-symbols',
    subject: 'Chemistry',
    category: 'state-symbol',
    paperLabel: 'Chemistry HL — equations',
    questionText: c2,
    trapSpans: [span(c2, 'including state symbols')],
    trapLabel: 'State symbols (s), (l), (g), (aq) — required.',
    whyStudentsMiss: 'Students balance the equation correctly and forget the state symbols. The phrase "including state symbols" makes them mark-bearing in this question.',
    consequence: 'Per dossier § B4: missing state symbols in thermochemical equations costs marks. Typical penalty: 1 mark per state symbol missed, up to the full state-symbol allocation for the question.',
    marksAtRiskPct: 25,
    source: { section: 'B4', page: 11, cite: 'Chemistry marking-scheme convention' },
  },
  {
    id: 'chem-titration-colour',
    subject: 'Chemistry',
    category: 'definition-keyphrase',
    paperLabel: 'Chemistry HL — titration',
    questionText: c3,
    trapSpans: [span(c3, 'colour change')],
    trapLabel: '"Colour change" — both colours must be named, with direction.',
    whyStudentsMiss: 'Students write "the indicator changes colour" or "purple". The marking scheme requires the start colour AND the end colour with the direction: "purple to colourless".',
    consequence: 'Single-colour answers earn no mark. The full phrasing earns the mark; vague answers earn nothing.',
    marksAtRiskPct: 100,
    source: { section: 'B4', page: 11, cite: 'Chemistry titration marking convention' },
  },
  {
    id: 'geo-process-vs-landform',
    subject: 'Geography',
    category: 'process-vs-landform',
    paperLabel: 'Geography HL Paper 2 — physical',
    questionText: g1,
    trapSpans: [span(g1, 'feature'), span(g1, 'named')],
    trapLabel: '"Feature" — describe the landform; "named" — name it.',
    whyStudentsMiss: 'Students describe the processes (wave action, abrasion) instead of the feature itself. Per dossier § B6: process vs landform confusion is a perennial Geography error.',
    consequence: 'Process answers to feature questions cap at "Max X SRPs if merely description without reference to formation". A 30-mark question can cap at 4 marks under this rule.',
    marksAtRiskPct: 80,
    source: { section: 'B6', page: 12, cite: '2012 Geography CER — process vs landform' },
  },
  {
    id: 'geo-named-example',
    subject: 'Geography',
    category: 'named-example',
    paperLabel: 'Geography HL Paper 2 — option essay',
    questionText: g2,
    trapSpans: [span(g2, 'a named region')],
    trapLabel: '"Named region" — must specify which region.',
    whyStudentsMiss: 'Students write a generic answer about "developing economies" or "the Sahel" without committing to a specific named region. The named example is the anchor that lets every other SRP score.',
    consequence: 'Without a named example, SRPs about that region don\'t qualify as "Significant Relevant Points". An option essay (80 marks) can cap at half-marks.',
    marksAtRiskPct: 30,
    source: { section: 'B6', page: 12, cite: '2012 Geography CER — named examples' },
  },
  {
    id: 'fr-tense-past',
    subject: 'French',
    category: 'tense-disguise',
    paperLabel: 'French HL — written / oral',
    questionText: f1,
    trapSpans: [span(f1, 'l\'année dernière')],
    trapLabel: '"L\'année dernière" — past tense / imperfect required.',
    whyStudentsMiss: 'Students hear "ta journée typique" and launch into a present-tense paragraph about their typical day. The phrase "l\'année dernière" (last year) shifts everything to the past.',
    consequence: 'Per the 2016 French CER: tense confusion caps Structure marks (30% of oral / 30% of opinion piece). A wrong-tense answer is structurally invalid.',
    marksAtRiskPct: 30,
    source: { section: 'B8', page: 13, cite: '2016 French CER — tense control' },
  },
  {
    id: 'fr-tense-conditional',
    subject: 'French',
    category: 'tense-disguise',
    paperLabel: 'French HL — opinion piece',
    questionText: f2,
    trapSpans: [span(f2, 'ferais-tu'), span(f2, 'gagnais')],
    trapLabel: 'Conditional + imperfect — hypothetical mood.',
    whyStudentsMiss: 'The structure "Si... [imperfect], ... [conditional]" governs hypothetical statements. Students answer in the present ("Je fais...") and lose Structure marks.',
    consequence: 'Wrong-mood answers are penalised at the Structure band. Per 2016 French CER, this is the dominant reason students cap below H2 in Languages.',
    marksAtRiskPct: 25,
    source: { section: 'B8', page: 13, cite: '2016 French CER' },
  },
  {
    id: 'hist-date-precision',
    subject: 'History',
    category: 'date-precision',
    paperLabel: 'History HL — DBQ contextualisation',
    questionText: h1,
    trapSpans: [span(h1, 'between 1916 and 1918')],
    trapLabel: '"Between 1916 and 1918" — full range, with dates.',
    whyStudentsMiss: 'Students write a generic essay on "the period" without anchoring claims to specific dates within the 1916–1918 range. The 2017 History CER notes weak chronological control as a perennial issue.',
    consequence: 'The marker scans for date-precise references. A vague chronological narrative loses the Contextualisation marks (40 of the DBQ\'s 100). Up to 40% of the DBQ section.',
    marksAtRiskPct: 40,
    source: { section: 'B5', page: 11, cite: '2017 History CER — chronological control' },
  },
];

/** Plain-English label for each trap category, used in the pattern
 *  recognition card. */
export const TRAP_CATEGORY_LABELS: Record<TrapCard['category'], string> = {
  'modifier': 'Modifier traps',
  'plural-singular': 'Plural / count traps',
  'command-switch': 'Hidden second-command traps',
  'definition-keyphrase': 'Definition key-phrase traps',
  'state-symbol': 'State-symbol traps',
  'process-vs-landform': 'Process-vs-landform traps',
  'named-example': 'Named-example traps',
  'tense-disguise': 'Tense-disguise traps',
  'in-terms-of': 'Form-of-answer traps',
  'date-precision': 'Date-precision traps',
};

/** A behavioural fix per category, surfaced when a student\'s pattern
 *  card flags a recurring miss. */
export const TRAP_CATEGORY_FIXES: Record<TrapCard['category'], string> = {
  'modifier': 'Underline the modifier ("significant", "effective", "deeply") before writing. The modifier is where the Purpose marks live in English.',
  'plural-singular': 'Read the question twice, paying attention to "values" vs "value", "all three" vs "two", and any restriction. Plural cues mean multiple answers.',
  'command-switch': 'Highlight every command verb. If the question contains "and", "as well as", "before", or a semicolon, treat each clause as its own sub-task with its own marks.',
  'definition-keyphrase': 'Memorise the exact phrasing for every definition. Test yourself by writing the answer down and crossing it against a marking scheme — both phrases must appear.',
  'state-symbol': 'When the question says "including state symbols" or asks for thermochemical equations, label every reactant and product with (s), (l), (g), or (aq).',
  'process-vs-landform': 'Decide before you write: is the question asking for the *what* (the landform) or the *how* (the process)? Answer the one you\'re asked.',
  'named-example': 'Pick your named example BEFORE you start writing. Open every option essay paragraph with the name; the marker can then tag every SRP back to it.',
  'tense-disguise': 'Listen for time-words first ("hier", "demain", "l\'année dernière", "si... gagnais"). They override your default present-tense answer.',
  'in-terms-of': 'When the question says "in terms of", "to two decimal places", "as a percentage" — the form of the answer is mark-bearing. Don\'t simplify away the requirement.',
  'date-precision': 'Anchor every claim to a date inside the question\'s range. "Between 1916 and 1918" demands ≥3 specific date references in the answer.',
};
