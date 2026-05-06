/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 *
 * Task-type taxonomy for the Exam Strategiser.
 * Each ExamQuestion declares a `taskType` that maps to one of these entries.
 * Grouping the question list by type surfaces the recurring structural
 * patterns examiners use (e.g. all "style elements" A(iii) tasks share the
 * same shape; all "regional economic activity" Geography tasks share the
 * same constraint pattern).
 */

import { type ExamSubject } from '../../types/examStrategiser';

export interface TaskTypeMeta {
  id: string;
  label: string;
  /** One-line description shown under the type heading. Tells the student
   *  what's recurring about this task type — the structural shape, the
   *  marking pattern, the constraint signature. */
  description: string;
  subject: ExamSubject;
}

export const TASK_TYPES: TaskTypeMeta[] = [
  // ── English ─────────────────────────────────────────────────────────
  {
    id: 'english-comprehension-insight',
    label: 'Comprehension — "what does the writer reveal"',
    description: 'A(i) tasks (15m). Three points required, each anchored in the text. Personal opinions without textual reference cap in the lower bands.',
    subject: 'english',
  },
  {
    id: 'english-personal-views',
    label: 'Personal views — "develop three points"',
    description: 'A(ii) tasks (15m). Your own developed views, drawing on the text and/or experience. "Develop" is the load-bearing word — paragraph not sentence.',
    subject: 'english',
  },
  {
    id: 'english-style-elements',
    label: 'Style elements — "identify four elements"',
    description: 'A(iii) tasks (20m). Four elements of the writer\'s style, each linked to a named effect (informative, engaging, intriguing, appealing).',
    subject: 'english',
  },
  {
    id: 'english-composition-genre-task',
    label: 'Composition — Question B genre task (50m)',
    description: 'Section I QB. Write in a prescribed genre (proposal, review reply, dialogue, diary). P/C/L/M discrete grid; P caps C and L. 2-3 explicit sub-tasks must be addressed.',
    subject: 'english',
  },
  {
    id: 'english-composition-speech',
    label: 'Composition — speech (100m)',
    description: 'Section II speech for or against a motion. P/C/L/M = 30/30/30/10. Pick ONE side. Speech-genre features (rhetorical questions, direct address, audience awareness).',
    subject: 'english',
  },
  {
    id: 'english-composition-discursive',
    label: 'Composition — discursive essay (100m)',
    description: 'Section II discursive essay weighing multiple views. NOT argumentative — must consider counter-arguments. Genre confusion is the most common 100m error.',
    subject: 'english',
  },
  {
    id: 'english-composition-short-story',
    label: 'Composition — short story (100m)',
    description: 'Section II narrative composition. Plot, character, setting, conflict, resolution. P caps C and L; getting the genre wrong (writing an essay instead) caps everything.',
    subject: 'english',
  },

  // ── Irish ───────────────────────────────────────────────────────────
  {
    id: 'irish-literature-essay',
    label: 'Litríocht — text-based essay',
    description: 'Paper 2 literature questions. Pléigh / Déan cur síos with quoted textual reference. Vague references ("sa scéal seo") lose marks; named characters and quoted moments earn SRPs.',
    subject: 'irish',
  },

  // ── Maths ───────────────────────────────────────────────────────────
  {
    id: 'maths-section-a-algebra',
    label: 'Section A — algebra',
    description: 'Short multi-part Section A questions on equations, inequalities, factor pairs, quadratic roots. Common trap: forgetting to flip inequality when dividing by a negative.',
    subject: 'maths',
  },
  {
    id: 'maths-section-a-calculus',
    label: 'Section A — calculus',
    description: 'Short multi-part Section A questions on differentiation, slopes of tangents, reading derivatives from graphs. Common trap: substituting into f(x) instead of f\'(x) for tangent slope.',
    subject: 'maths',
  },
  {
    id: 'maths-section-b-functions-graphing',
    label: 'Section B — functions & graphing',
    description: 'Long contextual Section B questions on reading graphs, modelling with functions, percentage error, exponential models, graph translations. Many sub-parts; "Show your work on the graph" is enforced.',
    subject: 'maths',
  },
  {
    id: 'maths-section-b-probability',
    label: 'Section B — probability',
    description: 'Long contextual Section B questions on probability trees, expected value, geometric probability. "Independent" means multiply along branches; "first loss is the third game" enforces order.',
    subject: 'maths',
  },
  {
    id: 'maths-section-b-statistics',
    label: 'Section B — statistics',
    description: 'Long contextual Section B questions on pie charts, correlation, margin of error (1/√n at OL), hypothesis testing by confidence interval. Three things required for the test: calculation, conclusion, reason.',
    subject: 'maths',
  },
  {
    id: 'maths-section-b-geometry',
    label: 'Section B — geometry & construction',
    description: 'Long contextual Section B questions on centroid construction, enlargements (k vs k²), sectors, arc length. Areas scale by k², not k — most common trap.',
    subject: 'maths',
  },
  {
    id: 'maths-section-b-trigonometry',
    label: 'Section B — trigonometry & counting',
    description: 'Long contextual Section B questions on cosine rule, ½ ab sin C, polygon decomposition, permutations. "Use the cosine rule" specifies method; ⁵P₂ ≠ ⁵C₂ when order matters.',
    subject: 'maths',
  },

  // ── Business ────────────────────────────────────────────────────────
  {
    id: 'business-section-1-short',
    label: 'Section 1 — short response',
    description: 'Compulsory 10-mark short-response questions. Mix of definitions, ratio calculations, true/false, matching. Brevity rewarded for "list/name/state" cues; full sentences for "outline/explain".',
    subject: 'business',
  },
  {
    id: 'business-abq',
    label: 'Applied Business Question (ABQ)',
    description: 'Compulsory 80-mark case-study question (20% of paper). The defining HL Business challenge — answers must combine business theory with direct quotes/phrases from the case. Theory without case-link scores 0; case-summary without theory scores 0.',
    subject: 'business',
  },
  {
    id: 'business-people-in-business',
    label: 'Section 3 — People in Business (Unit 1)',
    description: 'Section 3 Part 1 60-mark question (Q1 / Q4). Three sub-parts at 20 marks each. Tests contract law, industrial relations, employment legislation, conflict/co-operative relationships.',
    subject: 'business',
  },
  {
    id: 'business-domestic-environment',
    label: 'Section 3 — Domestic Environment (Unit 6)',
    description: 'Section 3 Part 1 60-mark question (Q2). Often least popular in cohort but well-marked when attempted. Tests business organisations, government taxes/policy, social/environmental responsibility.',
    subject: 'business',
  },
  {
    id: 'business-international-environment',
    label: 'Section 3 — International Environment (Unit 7)',
    description: 'Section 3 Part 1 60-mark question (Q3). Tests EU institutions, directives/regulations, global marketing, free-trade barriers, MNCs.',
    subject: 'business',
  },
  {
    id: 'business-managing',
    label: 'Section 3 — Managing (Units 4 / 5)',
    description: 'Section 3 Part 2 60-mark question (Q5 / Q6). Tests management activities, communication, change management, insurance, taxation, motivation theories, financial calculations.',
    subject: 'business',
  },
  {
    id: 'business-business-in-action',
    label: 'Section 3 — Business in Action (Units 2 / 3 / 5)',
    description: 'Section 3 Part 2 60-mark question (Q7 / Q8). Tests expansion methods, marketing mix, market research, finance sources, breakeven analysis. Often rewards numerical-plus-theory mixes.',
    subject: 'business',
  },

  // ── Geography ───────────────────────────────────────────────────────
  {
    id: 'geography-physical-process-explanation',
    label: 'Physical process — name + explain',
    description: 'Section 1 30-mark questions: name a feature, then explain via SRPs. Pattern: 14 SRPs + diagram-with-labels bonus + named-example bonus. "Max X SRPs if…" caps are punitive.',
    subject: 'geography',
  },
  {
    id: 'geography-regional-economic-activity',
    label: 'Regional economic activity — two factors',
    description: 'Section 2 30-mark questions: examine two factors (physical/human) influencing economic activity in a named region. Geographic constraints often kill answers (Ireland-tied, NOT in Europe).',
    subject: 'geography',
  },
];

export function getTaskType(id: string): TaskTypeMeta | undefined {
  return TASK_TYPES.find(t => t.id === id);
}

export function getTaskTypesForSubject(subject: ExamSubject): TaskTypeMeta[] {
  return TASK_TYPES.filter(t => t.subject === subject);
}
