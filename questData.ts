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
  /** Phase 5 plumbing: curriculum level(s) the quest applies to. Defaults
   *  to 'senior' if absent (every existing quest was authored for senior). */
  curriculum?: 'junior' | 'senior' | 'both';
}

export const ONBOARDING_QUESTS: QuestDefinition[] = [
  { id: 'onboard-1', day: 1, title: 'Start your first module', description: 'Open any learning module and begin reading', metric: 'module-start', target: 1, rewardPoints: 25 },
  { id: 'onboard-2', day: 2, title: 'Complete a study session', description: 'Set a timer and study any subject', metric: 'study-session', target: 1, rewardPoints: 30 },
  { id: 'onboard-3', day: 3, title: 'Write your first debrief', description: 'Reflect on what you studied after a session', metric: 'debrief', target: 1, rewardPoints: 30 },
  { id: 'onboard-4', day: 4, title: 'Complete a timetable block', description: 'Follow your timetable and complete a study block', metric: 'timetable-block', target: 1, rewardPoints: 30 },
  { id: 'onboard-5', day: 5, title: 'Complete your first module', description: 'Finish all sections in any module', metric: 'module-complete', target: 1, rewardPoints: 45 },
  { id: 'onboard-6', day: 6, title: 'Hit a 3-day streak', description: 'Study for 3 days in a row', metric: 'streak-hit', target: 3, rewardPoints: 35 },
  { id: 'onboard-7', day: 7, title: 'Complete 2 study sessions', description: 'Build momentum with two sessions today', metric: 'study-session', target: 2, rewardPoints: 45 },
  // ── Junior Cycle onboarding (mirrors senior 1:1 — JC voice, peer tone) ────
  { id: 'onboard-jc-1', day: 1, title: 'Crack open your first module', description: 'Pick any module and read the first section', metric: 'module-start', target: 1, rewardPoints: 25, curriculum: 'junior' },
  { id: 'onboard-jc-2', day: 2, title: 'Get a real study session in', description: 'Set a timer, pick a subject, and just sit down with it', metric: 'study-session', target: 1, rewardPoints: 30, curriculum: 'junior' },
  { id: 'onboard-jc-3', day: 3, title: 'Write your first quick debrief', description: 'After a session, jot down what stuck and what didn\'t', metric: 'debrief', target: 1, rewardPoints: 30, curriculum: 'junior' },
  { id: 'onboard-jc-4', day: 4, title: 'Tick off a timetable block', description: 'Follow your study plan and finish one block', metric: 'timetable-block', target: 1, rewardPoints: 30, curriculum: 'junior' },
  { id: 'onboard-jc-5', day: 5, title: 'Finish your first whole module', description: 'Get through every section in one module', metric: 'module-complete', target: 1, rewardPoints: 45, curriculum: 'junior' },
  { id: 'onboard-jc-6', day: 6, title: 'String 3 days together', description: 'Study three days in a row — that\'s a streak', metric: 'streak-hit', target: 3, rewardPoints: 35, curriculum: 'junior' },
  { id: 'onboard-jc-7', day: 7, title: 'Double up today', description: 'Two study sessions today — build the rhythm', metric: 'study-session', target: 2, rewardPoints: 45, curriculum: 'junior' },
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
  /** Phase 5 plumbing: curriculum level(s) the template applies to. */
  curriculum?: 'junior' | 'senior' | 'both';
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
  // ── Junior Cycle personalised templates (mirrors senior 1:1 — JC voice) ───
  { id: 'p-jc-study-weak', titleTemplate: 'Hit {subject}', descTemplate: '{subject} has some shaky bits — give it a proper go', metric: 'subject-session', target: 1, rewardPoints: 30, condition: 'has-shaky-topics', curriculum: 'junior' },
  { id: 'p-jc-timetable-2', titleTemplate: 'Knock out 2 timetable blocks', descTemplate: 'Stick to the plan today — two blocks done', metric: 'timetable-block', target: 2, rewardPoints: 35, condition: 'has-subjects', curriculum: 'junior' },
  { id: 'p-jc-debrief', titleTemplate: 'Debrief after you study', descTemplate: 'A quick note on how the session went — that\'s the trick', metric: 'debrief', target: 1, rewardPoints: 25, condition: 'always', curriculum: 'junior' },
  { id: 'p-jc-finish-module', titleTemplate: 'Wrap up {module}', descTemplate: 'You\'re nearly there — finish the module you started', metric: 'specific-module', target: 1, rewardPoints: 45, condition: 'has-in-progress-module', curriculum: 'junior' },
  { id: 'p-jc-streak-extend', titleTemplate: 'Don\'t break the streak', descTemplate: 'One block today and you keep it going', metric: 'timetable-block', target: 1, rewardPoints: 25, condition: 'streak-active', curriculum: 'junior' },
  { id: 'p-jc-session-long', titleTemplate: 'Get 2 sessions in', descTemplate: 'Two sessions back-to-back — that\'s when it starts clicking', metric: 'study-session', target: 2, rewardPoints: 35, condition: 'has-subjects', curriculum: 'junior' },
  { id: 'p-jc-topic-review', titleTemplate: 'Update your wobbly topics', descTemplate: 'Mark how you\'re feeling on your shakiest topics', metric: 'topic-update', target: 3, rewardPoints: 30, condition: 'has-shaky-topics', curriculum: 'junior' },
  { id: 'p-jc-mock-log', titleTemplate: 'Log a test result', descTemplate: 'Plug in your latest class test or mock so you can see the trend', metric: 'mock-entry', target: 1, rewardPoints: 30, condition: 'has-subjects', curriculum: 'junior' },
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
