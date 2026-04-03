/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 *
 * Lightweight strategy registry extracted from studySessionData.ts.
 * Import this in eagerly-loaded hooks to avoid pulling in 24KB of STRATEGY_PROMPTS.
 */

export interface StrategyDefinition {
  moduleId: string;
  strategyName: string;
  description: string;
}

export const STRATEGY_REGISTRY: StrategyDefinition[] = [
  { moduleId: 'mastering-active-recall-protocol', strategyName: 'Active Recall', description: 'Test yourself from memory before reviewing notes' },
  { moduleId: 'mastering-spaced-repetition-protocol', strategyName: 'Spaced Repetition', description: 'Review material at increasing intervals to build long-term memory' },
  { moduleId: 'mastering-interleaving-protocol', strategyName: 'Interleaving', description: 'Mix different topics and problem types during practice' },
  { moduleId: 'elaborative-interrogation-protocol', strategyName: 'Elaboration', description: 'Ask "why" and "how" to deepen understanding' },
  { moduleId: 'agency-protocol', strategyName: 'Agency Mindset', description: 'Set clear intentions and take ownership of your learning' },
  { moduleId: 'growth-mindset-protocol', strategyName: 'Growth Mindset', description: 'Embrace challenge as a signal that learning is happening' },
  { moduleId: 'digital-distraction-protocol', strategyName: 'Deep Focus', description: 'Eliminate distractions and protect your attention' },
  { moduleId: 'learning-radar-protocol', strategyName: 'Metacognition', description: 'Monitor and adjust your learning strategies in real time' },
  { moduleId: 'exam-hall-strategies-protocol', strategyName: 'Exam Strategy', description: 'Practice under timed conditions to build exam readiness' },
];

export interface StudySessionRecord {
  id: string;
  date: string;
  subject: string;
  sessionType: 'new-learning' | 'practice' | 'revision';
  plannedMinutes: number;
  actualSeconds: number;
  startedAt: number;
  completedAt: number;
  pointsEarned: number;
  hadReflection: boolean;
  strategiesShown?: string[];
}
