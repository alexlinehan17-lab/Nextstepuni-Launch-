/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 *
 * Year Plans — a curated module curriculum for each school year, 1st through
 * 6th. Same data shape philosophy as learningPaths.ts: ordered moduleIds into
 * courseData. Assignment rules (agreed 2026-07-21):
 *   · Junior Cycle (1st–3rd): 14 unique general modules per year, no repeats
 *     across the three years, drawn from the 42 JC-eligible general modules
 *     (subject-strategy modules excluded — students pick those per subject).
 *   · 4th Year (TY): a 12-module senior-cycle bridge (reflection + foundations).
 *   · 5th–6th: 12 modules each, unique across senior years. Senior years may
 *     revisit 'both'-cycle modules a student met in JC — seniors get the full
 *     (non-essentials) rendering, so the revisit is a deepening, not a rerun.
 * Ordering within a year is the intended teaching order.
 */

export type YearPlanCycle = 'junior' | 'ty' | 'senior';

export interface YearPlan {
  id: string;
  /** School year 1–6. */
  year: number;
  /** Display title, e.g. "1st Year". */
  title: string;
  /** Italic serif subtitle. */
  subtitle: string;
  /** Muted description under the subtitle. */
  description: string;
  cycle: YearPlanCycle;
  /** Ordered course ids from courseData.ts — the intended teaching order. */
  moduleIds: string[];
}

export const YEAR_PLANS: YearPlan[] = [
  {
    id: 'year-1',
    year: 1,
    title: '1st Year',
    subtitle: 'Landing well',
    description:
      'Settling into secondary school: how memory actually works, why effort grows ability, and the first habits that make homework lighter.',
    cycle: 'junior',
    moduleIds: [
      'cognitive-architecture-protocol',
      'neuroplasticity-protocol',
      'growth-mindset-protocol',
      'praise-protocol',
      'power-of-yet-protocol',
      'science-of-making-mistakes-protocol',
      'grammar-of-grit-protocol',
      'agency-architecture-protocol',
      'bimodal-brain-protocol',
      'hope-protocol',
      'best-possible-self-protocol',
      'teaching-effect-protocol',
      'procrastination-protocol',
      'self-efficacy-protocol',
    ],
  },
  {
    id: 'year-2',
    year: 2,
    title: '2nd Year',
    subtitle: 'Building the toolkit',
    description:
      'The core study techniques — testing yourself, spacing it out, mixing it up — plus the focus habits that beat the phone.',
    cycle: 'junior',
    moduleIds: [
      'mastering-active-recall-protocol',
      'mastering-spaced-repetition-protocol',
      'mastering-interleaving-protocol',
      'elaborative-interrogation-protocol',
      'note-taking-paradox-protocol',
      'context-effect-protocol',
      'cognitive-load-protocol',
      'digital-distraction-protocol',
      'implementation-protocol',
      'learning-radar-protocol',
      'effective-struggle-protocol',
      'controllable-variables-protocol',
      'mastering-foreign-languages-protocol',
      'mastering-the-creatives-protocol',
    ],
  },
  {
    id: 'year-3',
    year: 3,
    title: '3rd Year',
    subtitle: 'The first big exams',
    description:
      'Junior Cycle exam year: turning technique into exam performance, managing nerves, and finishing strong without burning out.',
    cycle: 'junior',
    moduleIds: [
      'illusion-of-competence-protocol',
      'myelin-manual-protocol',
      'autodidact-engine-protocol',
      'cognitive-endurance-protocol',
      'mental-modelling-protocol',
      'reverse-engineering-protocol',
      'exam-hall-strategies-protocol',
      'exam-crisis-management-protocol',
      'affirming-values-protocol',
      'game-day-protocol',
      'reframing-catastrophic-thoughts-protocol',
      'emotional-intelligence-protocol',
      'strategic-advantage-protocol',
      'mastering-business-protocol',
    ],
  },
  {
    id: 'year-4',
    year: 4,
    title: '4th Year',
    subtitle: 'The bridge year',
    description:
      'Transition Year with a purpose: who you are, where you want to go, and the senior-cycle foundations to carry you there.',
    cycle: 'ty',
    moduleIds: [
      'agency-protocol',
      'linking-study-future-goals-protocol',
      'best-possible-self-protocol',
      'hope-protocol',
      'self-efficacy-protocol',
      'affirming-values-protocol',
      'reframing-progress-protocol',
      'procrastination-protocol',
      'agency-architecture-protocol',
      'growth-mindset-protocol',
      'science-of-making-mistakes-protocol',
      'teaching-effect-protocol',
    ],
  },
  {
    id: 'year-5',
    year: 5,
    title: '5th Year',
    subtitle: 'The serious build',
    description:
      'Senior cycle proper: deep learning science at full strength, deliberate practice, and the planning that keeps two years on track.',
    cycle: 'senior',
    moduleIds: [
      'mastering-active-recall-protocol',
      'mastering-spaced-repetition-protocol',
      'mastering-interleaving-protocol',
      'elaborative-interrogation-protocol',
      'cognitive-load-protocol',
      'effective-struggle-protocol',
      'myelin-manual-protocol',
      'mental-modelling-protocol',
      'note-taking-paradox-protocol',
      'learning-radar-protocol',
      'autodidact-engine-protocol',
      'reverse-engineering-protocol',
    ],
  },
  {
    id: 'year-6',
    year: 6,
    title: '6th Year',
    subtitle: 'Delivering on the day',
    description:
      'Leaving Cert year: marking-scheme fluency, answer engineering, points strategy, and staying steady through the exam season itself.',
    cycle: 'senior',
    moduleIds: [
      'marking-scheme-decoder-protocol',
      'answer-engineering-protocol',
      'leaving-cert-strategy-protocol',
      'points-optimization-protocol',
      'exam-hall-strategies-protocol',
      'exam-crisis-management-protocol',
      'game-day-protocol',
      'cognitive-endurance-protocol',
      'reframing-catastrophic-thoughts-protocol',
      'emotional-intelligence-protocol',
      'illusion-of-competence-protocol',
      'strategic-advantage-protocol',
    ],
  },
];
