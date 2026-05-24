/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 */

// ── Types ──────────────────────────────────────────────────

export type ChallengeMetric = 'strategy-sessions' | 'strategy-subjects' | 'total-sessions' | 'reflection-sessions';

export interface WeeklyChallengeDefinition {
  id: string;
  title: string;
  description: string;
  metric: ChallengeMetric;
  target: number;
  rewardPoints: number;
  icon: string;
  strategyModuleId?: string;
  /** Phase 5 plumbing: which curriculum level(s) this challenge applies to.
   *  Defaults to 'senior' if absent. */
  curriculum?: 'junior' | 'senior' | 'both';
}

// ── Challenge Definitions ──────────────────────────────────

export const WEEKLY_CHALLENGES: WeeklyChallengeDefinition[] = [
  // 9 × strategy-sessions (one per strategy, target: 3, reward: 75pts)
  {
    id: 'wc-active-recall-sessions',
    title: 'Active Recall Week',
    description: 'Use Active Recall in 3 study sessions this week',
    metric: 'strategy-sessions',
    target: 3,
    rewardPoints: 100,
    icon: 'Brain',
    strategyModuleId: 'mastering-active-recall-protocol',
  },
  {
    id: 'wc-spaced-rep-sessions',
    title: 'Spaced Repetition Week',
    description: 'Use Spaced Repetition in 3 study sessions this week',
    metric: 'strategy-sessions',
    target: 3,
    rewardPoints: 100,
    icon: 'Repeat',
    strategyModuleId: 'mastering-spaced-repetition-protocol',
  },
  {
    id: 'wc-interleaving-sessions',
    title: 'Interleaving Week',
    description: 'Use Interleaving in 3 study sessions this week',
    metric: 'strategy-sessions',
    target: 3,
    rewardPoints: 100,
    icon: 'Shuffle',
    strategyModuleId: 'mastering-interleaving-protocol',
  },
  {
    id: 'wc-elaboration-sessions',
    title: 'Elaboration Week',
    description: 'Use Elaboration in 3 study sessions this week',
    metric: 'strategy-sessions',
    target: 3,
    rewardPoints: 100,
    icon: 'HelpCircle',
    strategyModuleId: 'elaborative-interrogation-protocol',
  },
  {
    id: 'wc-agency-sessions',
    title: 'Agency Mindset Week',
    description: 'Use Agency Mindset in 3 study sessions this week',
    metric: 'strategy-sessions',
    target: 3,
    rewardPoints: 100,
    icon: 'Compass',
    strategyModuleId: 'agency-protocol',
  },
  {
    id: 'wc-growth-mindset-sessions',
    title: 'Growth Mindset Week',
    description: 'Use Growth Mindset in 3 study sessions this week',
    metric: 'strategy-sessions',
    target: 3,
    rewardPoints: 100,
    icon: 'Sprout',
    strategyModuleId: 'growth-mindset-protocol',
  },
  {
    id: 'wc-deep-focus-sessions',
    title: 'Deep Focus Week',
    description: 'Use Deep Focus in 3 study sessions this week',
    metric: 'strategy-sessions',
    target: 3,
    rewardPoints: 100,
    icon: 'Shield',
    strategyModuleId: 'digital-distraction-protocol',
  },
  {
    id: 'wc-metacognition-sessions',
    title: 'Metacognition Week',
    description: 'Use Metacognition in 3 study sessions this week',
    metric: 'strategy-sessions',
    target: 3,
    rewardPoints: 100,
    icon: 'Radar',
    strategyModuleId: 'learning-radar-protocol',
  },
  {
    id: 'wc-exam-strategy-sessions',
    title: 'Exam Strategy Week',
    description: 'Use Exam Strategy in 3 study sessions this week',
    metric: 'strategy-sessions',
    target: 3,
    rewardPoints: 100,
    icon: 'ClipboardCheck',
    strategyModuleId: 'exam-hall-strategies-protocol',
  },

  // 5 × strategy-subjects (target: 2 unique subjects, reward: 100pts)
  {
    id: 'wc-active-recall-subjects',
    title: 'Active Recall Across Subjects',
    description: 'Apply Active Recall across 2 different subjects',
    metric: 'strategy-subjects',
    target: 2,
    rewardPoints: 150,
    icon: 'Brain',
    strategyModuleId: 'mastering-active-recall-protocol',
  },
  {
    id: 'wc-spaced-rep-subjects',
    title: 'Spaced Rep Across Subjects',
    description: 'Apply Spaced Repetition across 2 different subjects',
    metric: 'strategy-subjects',
    target: 2,
    rewardPoints: 150,
    icon: 'Repeat',
    strategyModuleId: 'mastering-spaced-repetition-protocol',
  },
  {
    id: 'wc-interleaving-subjects',
    title: 'Interleaving Across Subjects',
    description: 'Apply Interleaving across 2 different subjects',
    metric: 'strategy-subjects',
    target: 2,
    rewardPoints: 150,
    icon: 'Shuffle',
    strategyModuleId: 'mastering-interleaving-protocol',
  },
  {
    id: 'wc-deep-focus-subjects',
    title: 'Deep Focus Across Subjects',
    description: 'Apply Deep Focus across 2 different subjects',
    metric: 'strategy-subjects',
    target: 2,
    rewardPoints: 150,
    icon: 'Shield',
    strategyModuleId: 'digital-distraction-protocol',
  },
  {
    id: 'wc-exam-strategy-subjects',
    title: 'Exam Strategy Across Subjects',
    description: 'Apply Exam Strategy across 2 different subjects',
    metric: 'strategy-subjects',
    target: 2,
    rewardPoints: 150,
    icon: 'ClipboardCheck',
    strategyModuleId: 'exam-hall-strategies-protocol',
  },

  // 2 × total-sessions
  {
    id: 'wc-total-sessions-5',
    title: 'Consistent Week',
    description: 'Complete 5 study sessions this week',
    metric: 'total-sessions',
    target: 5,
    rewardPoints: 150,
    icon: 'Clock',
  },
  {
    id: 'wc-total-sessions-8',
    title: 'Power Week',
    description: 'Complete 8 study sessions this week',
    metric: 'total-sessions',
    target: 8,
    rewardPoints: 200,
    icon: 'Zap',
  },

  // 2 × reflection-sessions
  {
    id: 'wc-reflections-3',
    title: 'Reflective Learner',
    description: 'Write reflections in 3 study sessions this week',
    metric: 'reflection-sessions',
    target: 3,
    rewardPoints: 150,
    icon: 'PenLine',
  },
  {
    id: 'wc-reflections-5',
    title: 'Deep Thinker',
    description: 'Write reflections in 5 study sessions this week',
    metric: 'reflection-sessions',
    target: 5,
    rewardPoints: 200,
    icon: 'PenLine',
  },

  // 2 × stretch challenges
  {
    id: 'wc-deep-focus-stretch',
    title: 'Focus Master',
    description: 'Use Deep Focus in 4 study sessions this week',
    metric: 'strategy-sessions',
    target: 4,
    rewardPoints: 150,
    icon: 'Shield',
    strategyModuleId: 'digital-distraction-protocol',
  },
  {
    id: 'wc-deep-focus-subjects-stretch',
    title: 'Focus Across Subjects',
    description: 'Apply Deep Focus across 3 different subjects',
    metric: 'strategy-subjects',
    target: 3,
    rewardPoints: 175,
    icon: 'Shield',
    strategyModuleId: 'digital-distraction-protocol',
  },

  // ─── Junior Cycle challenges (mirrors senior 1:1 — JC voice) ──────────────
  // 9 × strategy-sessions
  { id: 'wc-jc-active-recall-sessions', title: 'Active Recall Week', description: 'Use Active Recall in 3 study sessions this week', metric: 'strategy-sessions', target: 3, rewardPoints: 100, icon: 'Brain', strategyModuleId: 'mastering-active-recall-protocol', curriculum: 'junior' },
  { id: 'wc-jc-spaced-rep-sessions', title: 'Spaced Repetition Week', description: 'Use Spaced Repetition in 3 study sessions this week', metric: 'strategy-sessions', target: 3, rewardPoints: 100, icon: 'Repeat', strategyModuleId: 'mastering-spaced-repetition-protocol', curriculum: 'junior' },
  { id: 'wc-jc-interleaving-sessions', title: 'Mix-It-Up Week', description: 'Use Interleaving in 3 study sessions this week', metric: 'strategy-sessions', target: 3, rewardPoints: 100, icon: 'Shuffle', strategyModuleId: 'mastering-interleaving-protocol', curriculum: 'junior' },
  { id: 'wc-jc-elaboration-sessions', title: 'Ask-Why Week', description: 'Use Elaboration in 3 study sessions this week', metric: 'strategy-sessions', target: 3, rewardPoints: 100, icon: 'HelpCircle', strategyModuleId: 'elaborative-interrogation-protocol', curriculum: 'junior' },
  { id: 'wc-jc-agency-sessions', title: 'Own It Week', description: 'Use Agency Mindset in 3 study sessions this week', metric: 'strategy-sessions', target: 3, rewardPoints: 100, icon: 'Compass', strategyModuleId: 'agency-protocol', curriculum: 'junior' },
  { id: 'wc-jc-growth-mindset-sessions', title: 'Get-Better Week', description: 'Use Growth Mindset in 3 study sessions this week', metric: 'strategy-sessions', target: 3, rewardPoints: 100, icon: 'Sprout', strategyModuleId: 'growth-mindset-protocol', curriculum: 'junior' },
  { id: 'wc-jc-deep-focus-sessions', title: 'Phone-Down Week', description: 'Use Deep Focus in 3 study sessions this week', metric: 'strategy-sessions', target: 3, rewardPoints: 100, icon: 'Shield', strategyModuleId: 'digital-distraction-protocol', curriculum: 'junior' },
  { id: 'wc-jc-metacognition-sessions', title: 'Notice-Yourself Week', description: 'Use Metacognition in 3 study sessions this week', metric: 'strategy-sessions', target: 3, rewardPoints: 100, icon: 'Radar', strategyModuleId: 'learning-radar-protocol', curriculum: 'junior' },
  { id: 'wc-jc-exam-strategy-sessions', title: 'Test Day Week', description: 'Use Exam Strategy in 3 study sessions this week', metric: 'strategy-sessions', target: 3, rewardPoints: 100, icon: 'ClipboardCheck', strategyModuleId: 'exam-hall-strategies-protocol', curriculum: 'junior' },

  // 5 × strategy-subjects
  { id: 'wc-jc-active-recall-subjects', title: 'Recall Across Subjects', description: 'Use Active Recall in 2 different subjects', metric: 'strategy-subjects', target: 2, rewardPoints: 150, icon: 'Brain', strategyModuleId: 'mastering-active-recall-protocol', curriculum: 'junior' },
  { id: 'wc-jc-spaced-rep-subjects', title: 'Spaced Rep Across Subjects', description: 'Use Spaced Repetition in 2 different subjects', metric: 'strategy-subjects', target: 2, rewardPoints: 150, icon: 'Repeat', strategyModuleId: 'mastering-spaced-repetition-protocol', curriculum: 'junior' },
  { id: 'wc-jc-interleaving-subjects', title: 'Mix It Across Subjects', description: 'Use Interleaving in 2 different subjects', metric: 'strategy-subjects', target: 2, rewardPoints: 150, icon: 'Shuffle', strategyModuleId: 'mastering-interleaving-protocol', curriculum: 'junior' },
  { id: 'wc-jc-deep-focus-subjects', title: 'Focus Across Subjects', description: 'Use Deep Focus in 2 different subjects', metric: 'strategy-subjects', target: 2, rewardPoints: 150, icon: 'Shield', strategyModuleId: 'digital-distraction-protocol', curriculum: 'junior' },
  { id: 'wc-jc-exam-strategy-subjects', title: 'Test Strategy Across Subjects', description: 'Use Exam Strategy in 2 different subjects', metric: 'strategy-subjects', target: 2, rewardPoints: 150, icon: 'ClipboardCheck', strategyModuleId: 'exam-hall-strategies-protocol', curriculum: 'junior' },

  // 2 × total-sessions
  { id: 'wc-jc-total-sessions-5', title: 'Steady Week', description: 'Get 5 study sessions in this week', metric: 'total-sessions', target: 5, rewardPoints: 150, icon: 'Clock', curriculum: 'junior' },
  { id: 'wc-jc-total-sessions-8', title: 'Big Week', description: 'Get 8 study sessions in this week', metric: 'total-sessions', target: 8, rewardPoints: 200, icon: 'Zap', curriculum: 'junior' },

  // 2 × reflection-sessions
  { id: 'wc-jc-reflections-3', title: 'Quick Thinker', description: 'Debrief 3 of your sessions this week', metric: 'reflection-sessions', target: 3, rewardPoints: 150, icon: 'PenLine', curriculum: 'junior' },
  { id: 'wc-jc-reflections-5', title: 'Real Reflector', description: 'Debrief 5 of your sessions this week', metric: 'reflection-sessions', target: 5, rewardPoints: 200, icon: 'PenLine', curriculum: 'junior' },

  // 2 × stretch
  { id: 'wc-jc-deep-focus-stretch', title: 'Focus Beast', description: 'Use Deep Focus in 4 study sessions this week', metric: 'strategy-sessions', target: 4, rewardPoints: 150, icon: 'Shield', strategyModuleId: 'digital-distraction-protocol', curriculum: 'junior' },
  { id: 'wc-jc-deep-focus-subjects-stretch', title: 'Focus, Three Subjects', description: 'Use Deep Focus in 3 different subjects', metric: 'strategy-subjects', target: 3, rewardPoints: 175, icon: 'Shield', strategyModuleId: 'digital-distraction-protocol', curriculum: 'junior' },
];

// ── Selector ──────────────────────────────────────────────

export function getWeeklyChallenge(
  weekNumber: number,
  curriculumLevel: 'junior' | 'senior' = 'senior',
): WeeklyChallengeDefinition | null {
  // Phase 5 plumbing: filter to the user's curriculum. Existing challenges
  // default to 'senior'. JC sees no challenges in Phase 5.
  const visible = WEEKLY_CHALLENGES.filter(c => {
    const tag = c.curriculum ?? 'senior';
    return tag === 'both' || tag === curriculumLevel;
  });
  if (visible.length === 0) return null;
  return visible[weekNumber % visible.length];
}
