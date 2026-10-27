/**
 * Sample data for the My Progress review (27 Oct 2026), shared by the "Now"
 * mount (kobra-review/before/ProgressBefore.tsx) and the Kobra rebuild
 * (ProgressAfter.tsx) so both panes show the same fortnight. Nothing here is
 * a real account: every value is labelled as sample where it is shown.
 * The quest, weekly challenge, ranks, goals and strategies are the app's own
 * definitions, picked from their data files rather than written here.
 */
import { ALL_COURSES } from '../../courseData';
import { toDateKey, type StudentSubjectProfile } from '../../components/subjectData';
import {
  getNextRank, getRankForPoints, getRankProgress, getWeekNumber, getWeekStartDate, type GamificationState,
} from '../../gamificationConfig';
import { getWeeklyChallenge } from '../../weeklyChallengeData';
import { ONBOARDING_QUESTS } from '../../questData';
import type { StudySessionRecord } from '../../utils/strategyRegistry';
import type { StrategyMasteryMap, StudyConfidenceLabel, TopicMasteryV2 } from '../../types';
import type { StreakData } from '../../hooks/useStreak';
import type { WeeklyChallengeState } from '../../hooks/useWeeklyChallenge';
import type { FocusRecommendation } from '../../hooks/useTodaysFocus';

export const SAMPLE_LABEL = 'Sample data, not a real account';

/** Minutes per day across the fortnight ending today, oldest first; 0 = a rest day. */
const FORTNIGHT = [55, 0, 70, 45, 90, 0, 40, 75, 48, 102, 0, 64, 125, 60];
const ROTA = ['Chemistry', 'English', 'Mathematics', 'Geography', 'French'];
const LABELS: StudyConfidenceLabel[] = ['okay', 'good', 'shaky', 'good', 'confident', 'okay', 'good'];
const SCORE: Record<StudyConfidenceLabel, number> = { lost: 1, shaky: 2, okay: 3, good: 4, confident: 5 };
const METHODS = ['mastering-active-recall-protocol', 'mastering-spaced-repetition-protocol', 'mastering-interleaving-protocol'];
const TYPES: StudySessionRecord['sessionType'][] = ['practice', 'revision', 'new-learning'];

export function sampleSessions(now = new Date()): StudySessionRecord[] {
  const records: StudySessionRecord[] = [];
  FORTNIGHT.forEach((minutes, index) => {
    if (!minutes) return;
    const date = new Date(now.getFullYear(), now.getMonth(), now.getDate() - (FORTNIGHT.length - 1 - index));
    const parts = minutes > 80 ? [Math.ceil(minutes / 2), Math.floor(minutes / 2)] : [minutes];
    parts.forEach((length, n) => {
      const startedAt = new Date(date.getFullYear(), date.getMonth(), date.getDate(), 16 + n * 2).getTime();
      const label = LABELS[(index + n) % LABELS.length];
      records.push({
        id: `sample-${index}-${n}`, date: toDateKey(date), subject: ROTA[(index + n) % ROTA.length],
        sessionType: TYPES[(index + n) % TYPES.length], plannedMinutes: length, actualSeconds: length * 60,
        startedAt, completedAt: startedAt + length * 60000, pointsEarned: 40, hadReflection: n === 0,
        confidenceLabel: label, confidenceAfter: SCORE[label],
        strategiesShown: [METHODS[(index + n) % METHODS.length]],
        strategiesUsed: [METHODS[(index + n) % METHODS.length]],
      });
    });
  });
  return records;
}

export const sampleStreak = (now = new Date()): StreakData => ({ currentStreak: 4, longestStreak: 9, lastActiveDate: toDateKey(now) });

/** Grades as onboarding collects them: current and target, never asked twice. */
export const sampleProfile = (): StudentSubjectProfile => ({
  subjects: [
    { subjectName: 'English', level: 'higher', currentGrade: 'H3', targetGrade: 'H2' },
    { subjectName: 'Irish', level: 'higher', currentGrade: 'H4', targetGrade: 'H3' },
    { subjectName: 'Mathematics', level: 'higher', currentGrade: 'H4', targetGrade: 'H3' },
    { subjectName: 'Chemistry', level: 'higher', currentGrade: 'H3', targetGrade: 'H2' },
    { subjectName: 'Geography', level: 'higher', currentGrade: 'H2', targetGrade: 'H1' },
    { subjectName: 'French', level: 'higher', currentGrade: 'H4', targetGrade: 'H3' },
  ],
  examStartDate: '2027-06-02', restDays: [], defaultBlockDuration: 45, yearGroup: '6th',
  createdAt: '2026-09-01T09:00:00.000Z', updatedAt: '2026-10-01T09:00:00.000Z',
});

const topic = (confidence: 'not-started' | 'shaky' | 'solid') => ({ confidence, updatedAt: Date.now(), source: 'manual' as const });
export const sampleTopicMastery = (): TopicMasteryV2 => ({
  schemaVersion: 2,
  topics: {},
  unresolved: {
    Chemistry: { 'Atomic structure': topic('solid'), 'Chemical bonding': topic('shaky'), 'Rates of reaction': topic('not-started') },
    Geography: { 'Plate tectonics': topic('solid'), 'Rivers': topic('solid'), 'Regional geography': topic('shaky') },
    Mathematics: { 'Algebra': topic('shaky'), 'Calculus': topic('not-started'), 'Probability': topic('solid') },
    English: { 'Comparative study': topic('shaky'), 'Poetry': topic('solid'), 'Composition': topic('not-started') },
  },
});

/** Every module before Controlling the Controllables complete, so Today has a module to continue. */
const HOME_MODULE = 'agency-architecture-protocol';
export function sampleUserProgress(): Record<string, { unlockedSection: number }> {
  const result: Record<string, { unlockedSection: number }> = {};
  for (const course of ALL_COURSES) {
    if (course.id === HOME_MODULE) { result[course.id] = { unlockedSection: 3 }; break; }
    result[course.id] = { unlockedSection: course.sectionsCount };
  }
  return result;
}
export function sampleRecommendation(): FocusRecommendation | null {
  const course = ALL_COURSES.find(item => item.id === HOME_MODULE);
  return course ? { moduleId: course.id, title: course.title, category: course.category, reason: 'in-progress' } : null;
}

/** Day 7 of onboarding, completed and not yet claimed: today it prints "Completed" in orange. */
export function sampleQuest() {
  const quest = ONBOARDING_QUESTS.find(item => item.id === 'onboard-7') ?? ONBOARDING_QUESTS[0];
  return {
    quest: { title: quest.title, description: quest.description, rewardPoints: quest.rewardPoints, target: quest.target },
    current: quest.target, isCompleted: true, isClaimed: false, dayNumber: quest.day ?? 7, isOnboarding: true,
  };
}

const POINTS = 1640;
export function sampleGamification(): GamificationState {
  const rank = getRankForPoints(POINTS);
  const next = getNextRank(rank);
  const day = 86_400_000;
  return {
    totalPointsEarned: POINTS, currentStreak: 4, longestStreak: 9, modulesCompleted: 6, sectionsCompleted: 31,
    categoriesCompleted: 1, totalReflections: 7, totalTimetableSessions: 5, northStarCategory: null,
    currentRank: rank, nextRank: next, rankProgress: getRankProgress(POINTS, rank, next),
    unlockedAchievements: ['first-step', 'getting-started', 'first-module', 'session-one'],
    achievementTimestamps: { 'first-step': Date.now() - 40 * day, 'getting-started': Date.now() - 30 * day, 'first-module': Date.now() - 12 * day, 'session-one': Date.now() - 9 * day },
    // The rank's first weekly goal is met; the other two are under way.
    weeklyGoalProgress: { sections: 6, sessions: 3, reflections: 1 },
    weekStartDate: getWeekStartDate(),
    personalBests: { bestDayPoints: 120, bestDaySections: 5, bestDayReflections: 2, bestWeekPoints: 410, bestWeekSessions: 9 },
    journeyMilestones: 2, streakShields: 1,
  };
}

export function sampleWeeklyChallenge(): WeeklyChallengeState {
  return {
    challenge: getWeeklyChallenge(getWeekNumber()), current: 2, isCompleted: false, isClaimed: false, isLoaded: true,
    claimReward: async () => {}, reload: () => {},
  };
}

export const sampleStrategyMastery = (): StrategyMasteryMap => ({
  'mastering-active-recall-protocol': { tier: 'applied', sessionCount: 6, subjectsSeen: ['Chemistry', 'Geography'] },
  'mastering-spaced-repetition-protocol': { tier: 'practiced', sessionCount: 3, subjectsSeen: ['English'] },
  'digital-distraction-protocol': { tier: 'learned', sessionCount: 1, subjectsSeen: [] },
});

export const SAMPLE_POINTS = { earned: 1240, available: 380 };
