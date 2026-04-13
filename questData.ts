/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 */

export type QuestMetric =
  | 'module-start' | 'module-complete' | 'specific-module'
  | 'study-session' | 'debrief' | 'timetable-block'
  | 'topic-update' | 'mock-entry' | 'streak-hit'
  | 'innovation-zone' | 'strategy-use' | 'subject-session';

export interface QuestDefinition {
  id: string;
  title: string;
  description: string;
  metric: QuestMetric;
  target: number;
  rewardPoints: number;
  day?: number;
  moduleId?: string;
  subjectName?: string;
}

export const ONBOARDING_QUESTS: QuestDefinition[] = [
  { id: 'onboard-1', day: 1, title: 'Start your first module', description: 'Open any learning module and begin reading', metric: 'module-start', target: 1, rewardPoints: 25 },
  { id: 'onboard-2', day: 2, title: 'Complete a study session', description: 'Set a timer and study any subject', metric: 'study-session', target: 1, rewardPoints: 30 },
  { id: 'onboard-3', day: 3, title: 'Write your first debrief', description: 'Reflect on what you studied after a session', metric: 'debrief', target: 1, rewardPoints: 30 },
  { id: 'onboard-4', day: 4, title: 'Complete a timetable block', description: 'Follow your timetable and complete a study block', metric: 'timetable-block', target: 1, rewardPoints: 30 },
  { id: 'onboard-5', day: 5, title: 'Complete your first module', description: 'Finish all sections in any module', metric: 'module-complete', target: 1, rewardPoints: 45 },
  { id: 'onboard-6', day: 6, title: 'Hit a 3-day streak', description: 'Study for 3 days in a row', metric: 'streak-hit', target: 3, rewardPoints: 35 },
  { id: 'onboard-7', day: 7, title: 'Complete 2 study sessions', description: 'Build momentum with two sessions today', metric: 'study-session', target: 2, rewardPoints: 45 },
];

// Personalized quest templates — the hook fills in subject/module dynamically
export interface PersonalizedQuestTemplate {
  id: string;
  titleTemplate: string;   // uses {subject}, {module}, {count}
  descTemplate: string;
  metric: QuestMetric;
  target: number;
  rewardPoints: number;
  // Conditions for when this quest should be selected
  condition: 'has-shaky-topics' | 'has-in-progress-module' | 'low-completion-rate' | 'streak-active' | 'has-subjects' | 'always';
}

export const PERSONALIZED_TEMPLATES: PersonalizedQuestTemplate[] = [
  { id: 'p-study-weak', titleTemplate: 'Study {subject}', descTemplate: '{subject} needs attention \u2014 it has shaky topics', metric: 'subject-session', target: 1, rewardPoints: 30, condition: 'has-shaky-topics' },
  { id: 'p-timetable-2', titleTemplate: 'Complete 2 timetable blocks', descTemplate: 'Follow your study plan today', metric: 'timetable-block', target: 2, rewardPoints: 35, condition: 'has-subjects' },
  { id: 'p-debrief', titleTemplate: 'Debrief after studying', descTemplate: 'Reflect on your session \u2014 it builds self-awareness', metric: 'debrief', target: 1, rewardPoints: 25, condition: 'always' },
  { id: 'p-finish-module', titleTemplate: 'Finish {module}', descTemplate: 'You\'re close \u2014 complete the module you started', metric: 'specific-module', target: 1, rewardPoints: 45, condition: 'has-in-progress-module' },
  { id: 'p-streak-extend', titleTemplate: 'Keep your streak alive', descTemplate: 'Complete at least one block today', metric: 'timetable-block', target: 1, rewardPoints: 25, condition: 'streak-active' },
  { id: 'p-session-long', titleTemplate: 'Study for 2 sessions', descTemplate: 'Two focused sessions build real momentum', metric: 'study-session', target: 2, rewardPoints: 35, condition: 'has-subjects' },
  { id: 'p-topic-review', titleTemplate: 'Review your weakest topics', descTemplate: 'Update your confidence in Syllabus X-Ray', metric: 'topic-update', target: 3, rewardPoints: 30, condition: 'has-shaky-topics' },
  { id: 'p-mock-log', titleTemplate: 'Log a mock result', descTemplate: 'Track your progress with a mock exam entry', metric: 'mock-entry', target: 1, rewardPoints: 30, condition: 'has-subjects' },
];

// Deterministic daily selection based on date + uid hash
export function hashSeed(s: string): number {
  let hash = 0;
  for (let i = 0; i < s.length; i++) {
    hash = ((hash << 5) - hash) + s.charCodeAt(i);
    hash |= 0;
  }
  return Math.abs(hash);
}
