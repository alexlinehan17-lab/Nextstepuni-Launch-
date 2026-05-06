/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 *
 * Command word library for the Necessary Knowledge tab.
 * Source: /docs/leaving-cert-knowledge-dossier.md § A1 (pages 2-3).
 */

import { type CommandWordEntry, type ModifierEntry } from '../../types/knowledge';

const A1: { section: string; page: number } = { section: 'A1', page: 2 };

export const COMMAND_WORDS: CommandWordEntry[] = [
  {
    word: 'State',
    aliases: ['Name', 'Identify'],
    requiredAction: 'Give a one-word or one-phrase answer with no explanation.',
    typicalMarkRange: '1-2 marks. Section A short questions.',
    structuralTemplate: 'Answer = the named item. No paragraphs.',
    commonError: 'Writing a paragraph when one word is wanted — the most common Section A error.',
    source: { ...A1, cite: 'Cross-LC short-question convention' },
  },
  {
    word: 'Define',
    requiredAction: 'Give the precise syllabus definition. Examiners hunt for specific key phrases.',
    typicalMarkRange: '2-4 marks. Section A or first part of long questions.',
    structuralTemplate: '"[Term] is [exact phrase] [exact phrase]." Verify against the syllabus glossary.',
    commonError: 'Approximating the definition. In Chemistry, "isotope" must include "same atomic number but different mass numbers"; in Biology, definitions are key-phrase-matched against published lists.',
    source: { ...A1, cite: 'Chemistry / Biology marking schemes' },
  },
  {
    word: 'Outline',
    requiredAction: 'Set out main characteristics in brief, often bullet-style points.',
    typicalMarkRange: '10-20 marks. Mid-sized questions.',
    structuralTemplate: '2-4 numbered or bulleted points, 1-2 sentences each. No full-essay treatment.',
    commonError: 'Writing essay-length prose when bullets are wanted. Wastes time you needed for higher-mark questions later.',
    source: A1,
  },
  {
    word: 'Describe',
    requiredAction: 'Give an account in your own words. More depth than outline.',
    typicalMarkRange: '10-30 marks.',
    structuralTemplate: 'Sequential narrative covering features, stages, or characteristics.',
    commonError: 'Confusing "Describe" with "Explain". Describe = what; Explain = how/why. Mixing them up costs marks across all subjects.',
    source: A1,
  },
  {
    word: 'Explain',
    requiredAction: 'Show how or why. Causal or mechanistic reasoning required.',
    typicalMarkRange: '10-30 marks.',
    structuralTemplate: 'Cause → effect → effect. Explain the mechanism, not just label features.',
    commonError: 'Describing instead of explaining — the Chief Examiner has called this "the most-confused word in the LC". Students label features when they should be tracing how things happen.',
    source: { ...A1, cite: 'Cross-LC; widely cited in CERs' },
  },
  {
    word: 'Discuss',
    requiredAction: 'Examine an issue from more than one perspective. Implies a conclusion.',
    typicalMarkRange: '20-60 marks. Long-question and essay territory.',
    structuralTemplate: 'Perspective A → Perspective B → reasoned conclusion taking a position.',
    commonError: 'Treating "Discuss" identically to "Explain" — losing the second perspective and the conclusion. Single-perspective answers cap below the band.',
    source: A1,
  },
  {
    word: 'Evaluate',
    aliases: ['Assess'],
    requiredAction: 'Make a judgement using evidence. State your own opinion explicitly.',
    typicalMarkRange: '20-30 marks. Common in Business ABQ "Evaluate" sub-parts.',
    structuralTemplate: 'Evidence A + Evidence B → my judgement: ... because ...',
    commonError: 'Treating "Evaluate" as "Describe" — no judgement, no opinion. In Business ABQ this caps marks; the marking scheme requires the student\'s own opinion explicitly.',
    source: { ...A1, page: 3, cite: 'Business ABQ marking convention' },
  },
  {
    word: 'Justify',
    requiredAction: 'Give reasoned support for the position you have taken.',
    typicalMarkRange: '10-20 marks.',
    structuralTemplate: 'Position + reasons + evidence. Marks awarded for the reasons, not the position itself.',
    commonError: 'Stating a position without reasons. The marks live in the reasons.',
    source: { ...A1, page: 3 },
  },
  {
    word: 'Compare',
    requiredAction: 'Identify similarities (and usually differences). Must be integrated, not "all of A then all of B".',
    typicalMarkRange: '20-30 marks. The Comparative Studies section in English specifically.',
    structuralTemplate: 'Point about both texts → why this similarity / difference exists. Each paragraph integrates both texts.',
    commonError: 'Treating texts serially: all about Text A, then all about Text B. The English Chief Examiner explicitly states "best answers were written in an analytical fashion" — meaning integrated.',
    source: { ...A1, page: 3, cite: 'English Comparative Studies CER' },
  },
  {
    word: 'Contrast',
    requiredAction: 'Identify differences only.',
    typicalMarkRange: '10-20 marks.',
    structuralTemplate: 'Difference 1: A is X, B is Y. Difference 2: A is..., B is...',
    commonError: 'Including similarities — "Contrast" specifically excludes them. Read the cue, not your prepared "Compare" essay.',
    source: { ...A1, page: 3 },
  },
  {
    word: 'Analyse',
    requiredAction: 'Break into components and show relationships between them.',
    typicalMarkRange: '20-50 marks.',
    structuralTemplate: 'Component A + Component B + how they relate + why this matters. The English CER says: "first present your point, then discuss why this similarity or difference exists".',
    commonError: 'Listing components without showing the relationships between them. Dropped components score nothing without integration.',
    source: { ...A1, page: 3, cite: 'English CER' },
  },
  {
    word: 'Examine',
    requiredAction: 'Investigate closely. In Geography, drives the SRP requirement.',
    typicalMarkRange: '20-30 marks.',
    structuralTemplate: 'Detailed inspection of each aspect. Each SRP must develop the point — no waffle.',
    commonError: 'Skating across the surface without close investigation. SRPs that don\'t develop the question score nothing.',
    source: { ...A1, page: 3 },
  },
  {
    word: 'To what extent',
    aliases: ['How far'],
    requiredAction: 'Argue both for and against. The answer must take a position by the end.',
    typicalMarkRange: '20-30 marks.',
    structuralTemplate: 'Arguments for + arguments against + my position: ... because ...',
    commonError: 'Arguing only one side — the question structure expects both, then a judgement. One-sided answers are capped.',
    source: { ...A1, page: 3 },
  },
];

/** Modifiers — the words around a command word that shift its demand.
 *  In English, the Purpose marks live in these.
 *  Source: /docs/leaving-cert-knowledge-dossier.md § A1 p.3. */
export const COMMAND_MODIFIERS: ModifierEntry[] = [
  {
    word: 'significant',
    signal: 'Demands judgement of importance. "Significant insights" = pick insights that matter, not the first ones you can name.',
    source: { ...A1, page: 3 },
  },
  {
    word: 'effective',
    signal: 'Demands evaluation of how well something works. "Effective use of disturbing imagery" = analyse the success of the technique, not just identify it.',
    source: { ...A1, page: 3 },
  },
  {
    word: 'deeply',
    signal: 'Intensifier. "Deeply embedded values" = surface analysis is not enough; look at structural patterns.',
    source: { ...A1, page: 3 },
  },
  {
    word: 'disturbing',
    signal: 'Tonal modifier. The chosen evidence must support this specific tone — examiners notice when the evidence is generic.',
    source: { ...A1, page: 3 },
  },
];
