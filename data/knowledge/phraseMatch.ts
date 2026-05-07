/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 *
 * Phrase Match — Marking Scheme Phrase Match library (Stage 3.3).
 *
 * 18 questions across Biology, Chemistry, Physics. Each question lists
 * the canonical key phrases the marking scheme is hunting, plus a small
 * set of acceptable paraphrases used by the matcher.
 *
 * Source: dossier § B4 (Sciences key phrases — chemistry "isotope" must
 * include "same atomic number but different mass numbers"; biology
 * "function of myelin sheath" = "to insulate" or "to speed up the
 * transmission"; "homologous series" = "same general formula", "similar
 * chemical properties", "gradation in physical properties").
 *
 * Per /CLAUDE.md content rule: question prompts paraphrased, never more
 * than 15 words verbatim from any SEC paper.
 */

import { type PhraseMatchQuestion } from '../../types/knowledge';

export const PHRASE_MATCH_QUESTIONS: PhraseMatchQuestion[] = [
  // ─── Biology (6) ──────────────────────────────────────────────────
  {
    id: 'bio-mitochondria',
    subject: 'biology',
    topicLabel: 'Mitochondria — function',
    questionPrompt: 'State the function of the mitochondrion in a eukaryotic cell.',
    keys: [
      {
        id: 'k1',
        canonical: 'site of aerobic respiration',
        acceptable: ['site of aerobic respiration', 'where aerobic respiration occurs', 'aerobic respiration takes place'],
        rationale: 'Names the process. The marking scheme requires this phrase or an equivalent.',
      },
      {
        id: 'k2',
        canonical: 'produces ATP',
        acceptable: ['produces atp', 'generates atp', 'makes atp', 'synthesises atp', 'releases energy as atp'],
        rationale: 'Names the energy currency.',
      },
      {
        id: 'k3',
        canonical: 'energy',
        acceptable: ['energy for the cell', 'energy production', 'cellular energy', 'powerhouse'],
        rationale: 'Names the role.',
      },
    ],
    modelAnswer: 'The mitochondrion is the site of aerobic respiration. It produces ATP and provides energy for the cell — the cellular powerhouse.',
    source: { section: 'B4', page: 10 },
  },
  {
    id: 'bio-enzyme',
    subject: 'biology',
    topicLabel: 'Enzyme — definition',
    questionPrompt: 'Define an enzyme.',
    keys: [
      {
        id: 'k1',
        canonical: 'biological catalyst',
        acceptable: ['biological catalyst', 'biocatalyst', 'a catalyst made by living cells'],
        rationale: 'The defining word. Without "biological catalyst" or equivalent, the answer is incomplete.',
      },
      {
        id: 'k2',
        canonical: 'speeds up reactions',
        acceptable: ['speeds up the reaction', 'accelerates the rate', 'increases the rate of reaction', 'speeds up chemical reactions'],
        rationale: 'Names the function.',
      },
      {
        id: 'k3',
        canonical: 'specific substrate',
        acceptable: ['specific to its substrate', 'substrate-specific', 'specific to a particular substrate', 'substrate specific'],
        rationale: 'Names the specificity property.',
      },
      {
        id: 'k4',
        canonical: 'active site',
        acceptable: ['active site', 'binding site'],
        rationale: 'Names the structural element.',
      },
    ],
    modelAnswer: 'An enzyme is a biological catalyst that speeds up reactions. Each enzyme is specific to its substrate, which binds to its active site.',
    source: { section: 'B4', page: 10 },
  },
  {
    id: 'bio-myelin',
    subject: 'biology',
    topicLabel: 'Myelin sheath — function',
    questionPrompt: 'State the function of the myelin sheath in a neuron.',
    keys: [
      {
        id: 'k1',
        canonical: 'insulates the axon',
        acceptable: ['insulates the axon', 'electrical insulator', 'to insulate', 'provides insulation'],
        rationale: 'Per dossier § B4 — the canonical phrase the marking scheme is matching.',
      },
      {
        id: 'k2',
        canonical: 'speeds up the transmission',
        acceptable: ['speeds up the transmission', 'increases the speed of', 'speeds up nerve impulses', 'faster conduction'],
        rationale: 'Per dossier § B4 — the second canonical phrase. Either this or the insulation phrase, but ideally both.',
      },
    ],
    modelAnswer: 'The myelin sheath insulates the axon and speeds up the transmission of nerve impulses (saltatory conduction).',
    source: { section: 'B4', page: 10, cite: 'Dossier § B4 — myelin sheath canonical phrasing' },
  },
  {
    id: 'bio-osmosis',
    subject: 'biology',
    topicLabel: 'Osmosis — definition',
    questionPrompt: 'Define osmosis.',
    keys: [
      {
        id: 'k1',
        canonical: 'movement of water',
        acceptable: ['movement of water', 'water moves', 'water passes', 'diffusion of water'],
        rationale: 'Identifies what is moving.',
      },
      {
        id: 'k2',
        canonical: 'low solute concentration to high',
        acceptable: ['low solute concentration to high', 'dilute to concentrated', 'lower water potential to higher', 'low to high concentration', 'high water potential to low'],
        rationale: 'The directional rule. Many students get this backwards.',
      },
      {
        id: 'k3',
        canonical: 'partially permeable membrane',
        acceptable: ['partially permeable membrane', 'semi-permeable membrane', 'selectively permeable'],
        rationale: 'Names the structure.',
      },
    ],
    modelAnswer: 'Osmosis is the movement of water from a region of low solute concentration to a region of high solute concentration across a partially permeable membrane.',
    source: { section: 'B4', page: 10 },
  },
  {
    id: 'bio-meiosis',
    subject: 'biology',
    topicLabel: 'Meiosis — definition',
    questionPrompt: 'Define meiosis.',
    keys: [
      {
        id: 'k1',
        canonical: 'two divisions',
        acceptable: ['two cell divisions', 'two divisions', 'two successive divisions'],
        rationale: 'Distinguishes meiosis from mitosis.',
      },
      {
        id: 'k2',
        canonical: 'four daughter cells',
        acceptable: ['four daughter cells', '4 daughter cells', 'produces four cells'],
        rationale: 'Names the output.',
      },
      {
        id: 'k3',
        canonical: 'haploid',
        acceptable: ['haploid', 'half the chromosome number'],
        rationale: 'Names the chromosome state.',
      },
      {
        id: 'k4',
        canonical: 'genetic variation',
        acceptable: ['genetic variation', 'genetically different', 'genetically distinct', 'crossing over'],
        rationale: 'Names the biological purpose.',
      },
    ],
    modelAnswer: 'Meiosis is a process of two divisions that produces four daughter cells, each haploid, with genetic variation introduced by crossing over.',
    source: { section: 'B4', page: 10 },
  },
  {
    id: 'bio-photosynthesis',
    subject: 'biology',
    topicLabel: 'Photosynthesis — overview',
    questionPrompt: 'Outline the process of photosynthesis.',
    keys: [
      {
        id: 'k1',
        canonical: 'in chlorophyll',
        acceptable: ['in chlorophyll', 'using chlorophyll', 'chlorophyll absorbs', 'in the chloroplasts'],
        rationale: 'Names the site.',
      },
      {
        id: 'k2',
        canonical: 'light energy',
        acceptable: ['light energy', 'sunlight', 'solar energy'],
        rationale: 'Names the energy source.',
      },
      {
        id: 'k3',
        canonical: 'carbon dioxide and water',
        acceptable: ['carbon dioxide and water', 'co2 and water', 'water and carbon dioxide'],
        rationale: 'Names the inputs.',
      },
      {
        id: 'k4',
        canonical: 'glucose and oxygen',
        acceptable: ['glucose and oxygen', 'oxygen and glucose', 'sugar and oxygen'],
        rationale: 'Names the products.',
      },
    ],
    modelAnswer: 'In chlorophyll, light energy is used to combine carbon dioxide and water, producing glucose and oxygen.',
    source: { section: 'B4', page: 10 },
  },

  // ─── Chemistry (6) ────────────────────────────────────────────────
  {
    id: 'chem-isotope',
    subject: 'chemistry',
    topicLabel: 'Isotope — definition',
    questionPrompt: 'Define an isotope.',
    keys: [
      {
        id: 'k1',
        canonical: 'atoms of the same element',
        acceptable: ['atoms of the same element', 'same element'],
        rationale: 'Names the comparison subject.',
      },
      {
        id: 'k2',
        canonical: 'same atomic number',
        acceptable: ['same atomic number', 'identical atomic number', 'same number of protons'],
        rationale: 'Per dossier § B4 — required phrase. Without this the answer is rejected.',
      },
      {
        id: 'k3',
        canonical: 'different mass numbers',
        acceptable: ['different mass numbers', 'different mass number', 'different number of neutrons', 'different mass'],
        rationale: 'Per dossier § B4 — required phrase.',
      },
    ],
    modelAnswer: 'Isotopes are atoms of the same element with the same atomic number but different mass numbers (because they have different numbers of neutrons).',
    source: { section: 'B4', page: 10, cite: 'Dossier § B4 — Chemistry "isotope" canonical phrasing' },
  },
  {
    id: 'chem-homologous',
    subject: 'chemistry',
    topicLabel: 'Homologous series — definition',
    questionPrompt: 'Define a homologous series.',
    keys: [
      {
        id: 'k1',
        canonical: 'same general formula',
        acceptable: ['same general formula', 'common general formula', 'fits a general formula'],
        rationale: 'Per dossier § B4 — required phrase #1.',
      },
      {
        id: 'k2',
        canonical: 'similar chemical properties',
        acceptable: ['similar chemical properties', 'same chemical properties', 'similar reactions'],
        rationale: 'Per dossier § B4 — required phrase #2.',
      },
      {
        id: 'k3',
        canonical: 'gradation in physical properties',
        acceptable: ['gradation in physical properties', 'gradual change in physical properties', 'physical properties change gradually', 'graded physical properties'],
        rationale: 'Per dossier § B4 — required phrase #3. Missing any one of the three phrases loses marks.',
      },
      {
        id: 'k4',
        canonical: 'differ by CH₂',
        acceptable: ['differ by ch2', 'differ by ch₂', 'each member differs by ch2', 'differ by a methylene group', 'differ by ch2 group', 'each successive member differs by'],
        rationale: 'Names the structural progression.',
      },
    ],
    modelAnswer: 'A homologous series is a family of compounds with the same general formula, similar chemical properties, and a gradation in physical properties; successive members differ by CH₂.',
    source: { section: 'B4', page: 10, cite: 'Dossier § B4 — Chemistry "homologous series" canonical phrasing' },
  },
  {
    id: 'chem-mole',
    subject: 'chemistry',
    topicLabel: 'Mole — definition',
    questionPrompt: 'Define a mole.',
    keys: [
      {
        id: 'k1',
        canonical: 'amount of substance',
        acceptable: ['amount of substance', 'unit of amount'],
        rationale: 'Names the kind of quantity.',
      },
      {
        id: 'k2',
        canonical: '6.02 × 10²³',
        acceptable: ['6.02 × 10²³', '6.022 × 10²³', '6.02 x 10^23', '6.02 x 10²³', '6.022 x 10^23', '6 x 10^23', 'avogadro\'s number'],
        rationale: 'The numerical value.',
      },
      {
        id: 'k3',
        canonical: 'particles',
        acceptable: ['particles', 'atoms', 'molecules', 'formula units', 'entities'],
        rationale: 'Names what is being counted.',
      },
    ],
    modelAnswer: 'A mole is the amount of substance that contains 6.02 × 10²³ particles (atoms, molecules, or formula units) — Avogadro\'s constant.',
    source: { section: 'B4', page: 10 },
  },
  {
    id: 'chem-acid',
    subject: 'chemistry',
    topicLabel: 'Acid — Brønsted–Lowry definition',
    questionPrompt: 'Define an acid (Brønsted–Lowry).',
    keys: [
      {
        id: 'k1',
        canonical: 'proton donor',
        acceptable: ['proton donor', 'donates a proton', 'donates protons', 'h+ donor', 'donates h+'],
        rationale: 'The defining property.',
      },
      {
        id: 'k2',
        canonical: 'in solution',
        acceptable: ['in aqueous solution', 'in solution', 'when dissolved in water'],
        rationale: 'Names the context.',
      },
    ],
    modelAnswer: 'A Brønsted–Lowry acid is a proton donor — a substance that donates a proton (H⁺) in aqueous solution.',
    source: { section: 'B4', page: 10 },
  },
  {
    id: 'chem-le-chatelier',
    subject: 'chemistry',
    topicLabel: 'Le Chatelier\'s principle',
    questionPrompt: 'State Le Chatelier\'s principle.',
    keys: [
      {
        id: 'k1',
        canonical: 'system at equilibrium',
        acceptable: ['system at equilibrium', 'equilibrium system', 'in dynamic equilibrium'],
        rationale: 'Names the precondition.',
      },
      {
        id: 'k2',
        canonical: 'is disturbed',
        acceptable: ['is disturbed', 'is subjected to a change', 'experiences a change', 'is stressed', 'is altered'],
        rationale: 'Names the trigger.',
      },
      {
        id: 'k3',
        canonical: 'shifts to oppose the change',
        acceptable: ['shifts to oppose the change', 'shifts to counteract', 'shifts in the direction that opposes', 'opposes the disturbance', 'minimise the disturbance', 'minimise the effect'],
        rationale: 'Names the response — the central rule.',
      },
    ],
    modelAnswer: 'If a system at equilibrium is disturbed, the equilibrium shifts to oppose the change.',
    source: { section: 'B4', page: 10 },
  },
  {
    id: 'chem-exothermic',
    subject: 'chemistry',
    topicLabel: 'Exothermic reaction',
    questionPrompt: 'Define an exothermic reaction.',
    keys: [
      {
        id: 'k1',
        canonical: 'releases energy',
        acceptable: ['releases energy', 'gives out energy', 'releases heat', 'evolves heat', 'releases heat energy'],
        rationale: 'Names the directionality.',
      },
      {
        id: 'k2',
        canonical: 'to the surroundings',
        acceptable: ['to the surroundings', 'into the surroundings', 'to its environment'],
        rationale: 'Names the recipient.',
      },
      {
        id: 'k3',
        canonical: 'negative ΔH',
        acceptable: ['negative δh', 'negative dh', 'negative enthalpy change', 'δh is negative', '-δh', 'δh < 0'],
        rationale: 'Names the thermodynamic signature.',
      },
    ],
    modelAnswer: 'An exothermic reaction releases energy to the surroundings; ΔH is negative.',
    source: { section: 'B4', page: 10 },
  },

  // ─── Physics (6) ──────────────────────────────────────────────────
  {
    id: 'phys-newton-1st',
    subject: 'physics',
    topicLabel: 'Newton\'s 1st Law',
    questionPrompt: 'State Newton\'s First Law of Motion.',
    keys: [
      {
        id: 'k1',
        canonical: 'object remains at rest',
        acceptable: ['remains at rest', 'stays at rest', 'remains stationary', 'an object at rest stays at rest'],
        rationale: 'Names the rest case.',
      },
      {
        id: 'k2',
        canonical: 'uniform motion in a straight line',
        acceptable: ['uniform motion in a straight line', 'constant velocity', 'moving at a constant speed in a straight line', 'continues in a straight line', 'continues in uniform motion'],
        rationale: 'Names the moving case.',
      },
      {
        id: 'k3',
        canonical: 'unless acted on by an external force',
        acceptable: ['unless acted on by an external force', 'until a force acts on it', 'unless an external force', 'unless a net force', 'unless acted upon by a force'],
        rationale: 'Names the exception clause.',
      },
    ],
    modelAnswer: 'An object remains at rest, or in uniform motion in a straight line, unless acted on by an external force.',
    source: { section: 'B4', page: 11 },
  },
  {
    id: 'phys-newton-unit',
    subject: 'physics',
    topicLabel: 'Definition of the Newton',
    questionPrompt: 'Define the Newton, the SI unit of force.',
    keys: [
      {
        id: 'k1',
        canonical: 'force required',
        acceptable: ['force required', 'force needed', 'the force that'],
        rationale: 'Names the kind of definition.',
      },
      {
        id: 'k2',
        canonical: '1 kg mass',
        acceptable: ['1 kg', 'one kilogram', '1 kilogram mass', 'mass of 1 kg', '1kg'],
        rationale: 'Names the mass.',
      },
      {
        id: 'k3',
        canonical: 'acceleration of 1 m/s²',
        acceptable: ['1 m/s²', '1 m/s2', 'acceleration of 1 m/s²', 'acceleration of one metre per second squared', 'an acceleration of 1 m s-2'],
        rationale: 'Names the acceleration.',
      },
    ],
    modelAnswer: 'The Newton is the force required to give a 1 kg mass an acceleration of 1 m/s².',
    source: { section: 'B4', page: 11 },
  },
  {
    id: 'phys-joule',
    subject: 'physics',
    topicLabel: 'Definition of the Joule',
    questionPrompt: 'Define the Joule, the SI unit of energy.',
    keys: [
      {
        id: 'k1',
        canonical: 'work done',
        acceptable: ['work done', 'energy transferred'],
        rationale: 'Names the kind of definition.',
      },
      {
        id: 'k2',
        canonical: 'force of 1 N',
        acceptable: ['force of 1 n', 'force of 1 newton', '1 N force', 'a 1 newton force'],
        rationale: 'Names the force.',
      },
      {
        id: 'k3',
        canonical: 'moves through 1 m',
        acceptable: ['1 m', 'one metre', 'a distance of 1 m', 'displacement of 1 m'],
        rationale: 'Names the distance.',
      },
      {
        id: 'k4',
        canonical: 'in the direction of the force',
        acceptable: ['in the direction of the force', 'parallel to the force', 'along the line of action'],
        rationale: 'Names the directional condition.',
      },
    ],
    modelAnswer: 'The Joule is the work done when a force of 1 N moves its point of application through 1 m in the direction of the force.',
    source: { section: 'B4', page: 11 },
  },
  {
    id: 'phys-momentum',
    subject: 'physics',
    topicLabel: 'Momentum',
    questionPrompt: 'Define momentum.',
    keys: [
      {
        id: 'k1',
        canonical: 'mass × velocity',
        acceptable: ['mass × velocity', 'mass times velocity', 'mass multiplied by velocity', 'm × v', 'mv', 'p = mv', 'product of mass and velocity'],
        rationale: 'The defining relationship.',
      },
      {
        id: 'k2',
        canonical: 'vector quantity',
        acceptable: ['vector quantity', 'vector', 'has direction'],
        rationale: 'Names the kind of quantity.',
      },
    ],
    modelAnswer: 'Momentum is the product of mass and velocity (p = mv); it is a vector quantity.',
    source: { section: 'B4', page: 11 },
  },
  {
    id: 'phys-refractive',
    subject: 'physics',
    topicLabel: 'Refractive index',
    questionPrompt: 'Define the refractive index of a medium.',
    keys: [
      {
        id: 'k1',
        canonical: 'ratio',
        acceptable: ['ratio of', 'is the ratio', 'ratio between'],
        rationale: 'Names the kind of definition.',
      },
      {
        id: 'k2',
        canonical: 'speed of light in a vacuum',
        acceptable: ['speed of light in a vacuum', 'speed of light in vacuum', 'c'],
        rationale: 'Names the numerator.',
      },
      {
        id: 'k3',
        canonical: 'speed of light in the medium',
        acceptable: ['speed of light in the medium', 'speed in the medium', 'speed of light through the substance'],
        rationale: 'Names the denominator.',
      },
    ],
    modelAnswer: 'The refractive index is the ratio of the speed of light in a vacuum to the speed of light in the medium.',
    source: { section: 'B4', page: 11 },
  },
  {
    id: 'phys-hookes',
    subject: 'physics',
    topicLabel: 'Hooke\'s Law',
    questionPrompt: 'State Hooke\'s Law.',
    keys: [
      {
        id: 'k1',
        canonical: 'extension',
        acceptable: ['extension', 'the stretch', 'amount stretched'],
        rationale: 'Names the dependent variable.',
      },
      {
        id: 'k2',
        canonical: 'directly proportional',
        acceptable: ['directly proportional', 'proportional to', 'in direct proportion'],
        rationale: 'Names the relationship.',
      },
      {
        id: 'k3',
        canonical: 'applied force',
        acceptable: ['applied force', 'force applied', 'force acting on it', 'load'],
        rationale: 'Names the independent variable.',
      },
      {
        id: 'k4',
        canonical: 'within elastic limit',
        acceptable: ['within elastic limit', 'within the elastic limit', 'provided the elastic limit is not exceeded', 'before the elastic limit'],
        rationale: 'The conditional clause — required for full marks.',
      },
    ],
    modelAnswer: 'The extension of a spring is directly proportional to the applied force, provided the elastic limit is not exceeded.',
    source: { section: 'B4', page: 11 },
  },
];
