/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 */

export interface LearningPath {
  id: string;
  title: string;
  subtitle: string;
  description: string;
  accentHex: string;
  moduleIds: string[];
}

export const LEARNING_PATHS: LearningPath[] = [
  {
    id: 'getting-started',
    title: 'Getting Started',
    subtitle: '8 foundational modules',
    description: 'Build the essential mindset, learning strategies, and habits every student needs before diving deeper.',
    accentHex: '#3b82f6',
    moduleIds: [
      'agency-protocol',
      'neuroplasticity-protocol',
      'growth-mindset-protocol',
      'illusion-of-competence-protocol',
      'mastering-active-recall-protocol',
      'mastering-spaced-repetition-protocol',
      'procrastination-protocol',
      'best-possible-self-protocol',
    ],
  },
  {
    id: 'exam-prep-sprint',
    title: 'Exam Prep Sprint',
    subtitle: '8 tactical modules',
    description: 'A fast-track path through the exam strategy, crisis management, and performance psychology you need for peak exam day.',
    accentHex: '#ef4444',
    moduleIds: [
      'leaving-cert-strategy-protocol',
      'points-optimization-protocol',
      'reverse-engineering-protocol',
      'exam-hall-strategies-protocol',
      'exam-crisis-management-protocol',
      'game-day-protocol',
      'cognitive-endurance-protocol',
      'reframing-catastrophic-thoughts-protocol',
    ],
  },
  {
    id: 'build-your-mindset',
    title: 'Build Your Mindset',
    subtitle: '13 modules',
    description: 'A comprehensive journey through the psychology of success — identity, resilience, motivation, and emotional intelligence.',
    accentHex: '#8b5cf6',
    moduleIds: [
      'agency-protocol',
      'self-efficacy-protocol',
      'best-possible-self-protocol',
      'implementation-protocol',
      'grammar-of-grit-protocol',
      'agency-architecture-protocol',
      'affirming-values-protocol',
      'strategic-advantage-protocol',
      'procrastination-protocol',
      'reframing-progress-protocol',
      'reframing-catastrophic-thoughts-protocol',
      'emotional-intelligence-protocol',
      'hope-protocol',
    ],
  },
  {
    id: 'master-your-learning',
    title: 'Master Your Learning',
    subtitle: '15 modules',
    description: 'Every science-backed study technique in one path — from cognitive architecture to advanced metacognition.',
    accentHex: '#14b8a6',
    moduleIds: [
      'cognitive-architecture-protocol',
      'illusion-of-competence-protocol',
      'mastering-active-recall-protocol',
      'mastering-spaced-repetition-protocol',
      'mastering-interleaving-protocol',
      'elaborative-interrogation-protocol',
      'bimodal-brain-protocol',
      'cognitive-load-protocol',
      'learning-radar-protocol',
      'note-taking-paradox-protocol',
      'mental-modelling-protocol',
      'autodidact-engine-protocol',
      'context-effect-protocol',
      'digital-distraction-protocol',
      'cognitive-endurance-protocol',
    ],
  },
];
