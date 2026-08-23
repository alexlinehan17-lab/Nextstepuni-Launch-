/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 *
 * Rich, deterministic data for the localhost-only Demo Account. The reserved
 * uid is never authenticated and none of this is written to Firestore. It is a
 * complete student story that lets product work exercise progress, study,
 * confidence, mastery, mock and programme visualisations together.
 */
import { ALL_COURSES } from '../courseData';
import { resolveCurriculumSpecification } from '../curriculumRegistry';
import { type DebriefEntry } from '../components/StudyDebrief';
import { type StudentSubjectProfile } from '../components/subjectData';
import { type CourseData } from '../components/Library';
import { extractModuleProgress, type ProgressDocument } from '../services/progressRepository';
import { canonicalMasteryKey } from '../services/topicMasteryMigration';
import {
  type NorthStar,
  type StudyConfidenceLabel,
  type StudyReflection,
  type TopicMasteryV2,
  type UnifiedConfidence,
  type UnifiedMockResult,
  type UserProgress,
} from '../types';
import { type SessionUser } from '../utils/authUtils';
import { filterCoursesForStudent } from '../utils/courseVisibility';
import { STRATEGY_REGISTRY, type StudySessionRecord } from '../utils/strategyRegistry';
import { getWeekStartDate, type GamificationFirestoreData } from '../gamificationConfig';

export const DEMO_STUDENT_UID = 'demo-student';

const DEMO_SESSION_STORAGE_KEY = 'nextstepuni:demo-session:v1';
const DEMO_PROGRESS_STORAGE_KEY = 'nextstepuni:demo-progress:v1';

/** @deprecated Use DEMO_STUDENT_UID. Kept for local tooling compatibility. */
export const DEV_STUDENT_UID = DEMO_STUDENT_UID;

const DEMO_COMPLETION_RATIO: Record<CourseData['category'], number> = {
  'architecture-mindset': 0.38,
  'science-growth': 0.46,
  'learning-cheat-codes': 0.57,
  'subject-specific-science': 0.43,
  'exam-zone': 0.34,
};

const CONFIDENCE_LABELS: Record<number, StudyConfidenceLabel> = {
  1: 'lost',
  2: 'shaky',
  3: 'okay',
  4: 'good',
  5: 'confident',
};

const clamp = (value: number, minimum: number, maximum: number) => (
  Math.min(maximum, Math.max(minimum, value))
);

const startOfLocalDay = (value: Date): Date => (
  new Date(value.getFullYear(), value.getMonth(), value.getDate())
);

const dateDaysAgo = (today: Date, daysAgo: number): Date => {
  const value = startOfLocalDay(today);
  value.setDate(value.getDate() - daysAgo);
  return value;
};

const atLocalTime = (date: Date, hour: number, minute = 0): Date => (
  new Date(date.getFullYear(), date.getMonth(), date.getDate(), hour, minute)
);

const toDateKey = (value: Date): string => {
  const year = value.getFullYear();
  const month = String(value.getMonth() + 1).padStart(2, '0');
  const day = String(value.getDate()).padStart(2, '0');
  return `${year}-${month}-${day}`;
};

const DEMO_UNLOCKED_ACHIEVEMENTS = [
  'first-step', 'getting-started', 'first-module', 'getting-serious', 'double-digits',
  'halfway-there', 'section-grinder', 'section-centurion',
  'session-one', 'five-sessions', 'ten-sessions', 'twenty-five-sessions', 'fifty-sessions',
  'streak-3', 'streak-7', 'streak-14', 'streak-21', 'streak-30', 'streak-shield-earned',
  'thinking-out-loud', 'five-reflections', 'ten-reflections', 'twenty-five-reflections',
  'north-star-set', 'north-star-first-week', 'north-star-dedicated',
  'ns-freedom-start', 'ns-freedom-10', 'ns-freedom-25',
  'first-hundred', 'five-hundred', 'one-thousand', 'three-thousand', 'five-thousand',
  'all-rounder', 'personal-best-day',
] as const;

const createDemoGamification = (today: Date): GamificationFirestoreData => {
  const achievementTimestamps = Object.fromEntries(
    DEMO_UNLOCKED_ACHIEVEMENTS.map((id, index) => {
      const daysAgo = Math.max(2, 330 - (index * 9));
      return [id, atLocalTime(dateDaysAgo(today, daysAgo), 18).getTime()];
    }),
  );

  return {
    unlockedAchievements: [...DEMO_UNLOCKED_ACHIEVEMENTS],
    achievementTimestamps,
    weeklyGoalProgress: { sections: 4, sessions: 6, reflections: 3 },
    weekStartDate: getWeekStartDate(today),
    lastSurpriseDate: toDateKey(dateDaysAgo(today, 12)),
    personalBests: {
      bestDayPoints: 112,
      bestDaySections: 8,
      bestDayReflections: 3,
      bestWeekPoints: 486,
      bestWeekSessions: 11,
    },
    streakShields: 2,
    streakShieldUsedDates: [],
    lastStreakBreakDate: toDateKey(dateDaysAgo(today, 43)),
    recoveryWindowEnd: '',
  };
};

const nextLeavingCertDate = (today: Date): string => {
  const examYear = today.getMonth() >= 5 ? today.getFullYear() + 1 : today.getFullYear();
  return `${examYear}-06-09`;
};

export const createDemoStudentSession = (): SessionUser => ({
  uid: DEMO_STUDENT_UID,
  name: 'Demo Student',
  avatar: 'Maya Angelou',
  role: 'student',
  isAdmin: false,
  yearGroup: '6th',
  curriculumLevel: 'senior',
});

export const createDemoStudentProfile = (today = new Date()): StudentSubjectProfile => {
  const joinedAt = atLocalTime(dateDaysAgo(today, 286), 16).toISOString();
  return {
    yearGroup: '6th',
    curriculumLevel: 'senior',
    examStartDate: nextLeavingCertDate(today),
    restDays: ['Sunday'],
    defaultBlockDuration: 45,
    createdAt: joinedAt,
    updatedAt: today.toISOString(),
    subjects: [
      { subjectName: 'Politics & Society', level: 'higher', currentGrade: 'H3', targetGrade: 'H1' },
      { subjectName: 'Geography', level: 'higher', currentGrade: 'H3', targetGrade: 'H2' },
      { subjectName: 'Mathematics', level: 'higher', currentGrade: 'H4', targetGrade: 'H2' },
      { subjectName: 'Applied Maths', level: 'higher', currentGrade: 'H4', targetGrade: 'H2' },
      { subjectName: 'English', level: 'higher', currentGrade: 'H3', targetGrade: 'H2' },
      { subjectName: 'Irish', level: 'higher', currentGrade: 'H4', targetGrade: 'H3' },
      { subjectName: 'Accounting', level: 'higher', currentGrade: 'H3', targetGrade: 'H1' },
    ],
  };
};

export const createDemoStudentNorthStar = (today = new Date()): NorthStar => {
  const createdAt = atLocalTime(dateDaysAgo(today, 286), 16).toISOString();
  const reviewedAt = atLocalTime(dateDaysAgo(today, 12), 18).toISOString();
  return {
    category: 'options-freedom',
    statement: 'Get enough points so I have choices',
    visionBoard: ['real-choices', 'see-world', 'freedom-no'],
    createdAt,
    updatedAt: reviewedAt,
    reviewedAt,
    authoredByStudent: true,
  };
};

export const createDemoModuleProgress = (profile: StudentSubjectProfile): UserProgress => {
  const progress: UserProgress = {};
  const visibleCourses = filterCoursesForStudent(ALL_COURSES, 'senior', profile);
  const categories = Object.keys(DEMO_COMPLETION_RATIO) as CourseData['category'][];

  for (const category of categories) {
    const courses = visibleCourses.filter(course => course.category === category);
    if (courses.length === 0) continue;
    const completedCount = Math.max(1, Math.min(
      courses.length - 1,
      Math.round(courses.length * DEMO_COMPLETION_RATIO[category]),
    ));

    courses.forEach((course, index) => {
      if (index < completedCount) {
        progress[course.id] = { unlockedSection: course.sectionsCount };
        return;
      }
      if (index === completedCount) {
        progress[course.id] = {
          unlockedSection: Math.max(1, Math.min(course.sectionsCount - 1, Math.ceil(course.sectionsCount * 0.58))),
        };
      }
    });
  }

  return progress;
};

const confidenceForSession = (daysAgo: number, sequence: number): number => {
  const baseline = daysAgo > 270
    ? 1
    : daysAgo > 205
      ? 2
      : daysAgo > 115
        ? 3
        : daysAgo > 38
          ? 3
          : 4;
  const variation = [0, 1, 0, -1, 0, 1][sequence % 6];
  return clamp(baseline + variation, 1, 5);
};

export const createDemoStudySessions = (
  today = new Date(),
  subjects = createDemoStudentProfile(today).subjects.map(subject => subject.subjectName),
): StudySessionRecord[] => {
  const sessions: StudySessionRecord[] = [];
  const strategyIds = STRATEGY_REGISTRY.map(strategy => strategy.moduleId);
  const sessionTypes: StudySessionRecord['sessionType'][] = ['practice', 'revision', 'new-learning'];
  const plannedDurations = [25, 35, 45, 50, 60];
  let sequence = 0;

  for (let daysAgo = 0; daysAgo <= 335; daysAgo += 1) {
    let sessionCount = 0;
    if (daysAgo === 0) sessionCount = 3;
    else if (daysAgo <= 6) sessionCount = daysAgo % 2 === 0 ? 2 : 1;
    else if (daysAgo <= 84 && daysAgo % 3 === 0) sessionCount = 1;
    else if (daysAgo > 84 && daysAgo % 10 === 0) sessionCount = 1;
    if (sessionCount === 0) continue;

    const day = dateDaysAgo(today, daysAgo);
    const date = toDateKey(day);
    for (let slot = 0; slot < sessionCount; slot += 1) {
      const subjectIndex = sequence % subjects.length;
      const plannedMinutes = plannedDurations[(daysAgo + slot + sequence) % plannedDurations.length];
      const actualMinutes = Math.max(18, plannedMinutes + ((((daysAgo + slot) % 5) - 2) * 3));
      const confidenceAfter = confidenceForSession(daysAgo, sequence);
      const completedAt = atLocalTime(day, slot === 0 ? 12 : 16 + slot * 2, slot === 0 ? 0 : 10);
      const primaryStrategy = strategyIds[(subjectIndex + sequence) % strategyIds.length];
      const secondaryStrategy = strategyIds[(subjectIndex + sequence + 3) % strategyIds.length];

      sessions.push({
        id: `demo-session-${date}-${slot}`,
        date,
        subject: subjects[subjectIndex],
        sessionType: sessionTypes[(daysAgo + slot) % sessionTypes.length],
        plannedMinutes,
        actualSeconds: actualMinutes * 60,
        startedAt: completedAt.getTime() - (actualMinutes * 60_000),
        completedAt: completedAt.getTime(),
        pointsEarned: 20 + ((sequence % 4) * 5),
        hadReflection: true,
        strategiesShown: sequence % 3 === 0
          ? [primaryStrategy, secondaryStrategy]
          : [primaryStrategy],
        confidenceAfter,
        confidenceLabel: CONFIDENCE_LABELS[confidenceAfter],
        reflectionMode: sequence % 4 === 0 ? 'full' : 'quick',
      });
      sequence += 1;
    }
  }

  return sessions.sort((a, b) => b.completedAt - a.completedAt);
};

const createDemoReflections = (sessions: StudySessionRecord[]): StudyReflection[] => (
  sessions
    .filter((_session, index) => index % 2 === 0)
    .map(session => ({
      dateKey: session.date,
      blockId: session.id,
      subjectName: session.subject,
      sessionType: session.sessionType,
      reflection: session.confidenceLabel ?? 'okay',
      pointsEarned: session.pointsEarned,
      timestamp: session.completedAt,
      confidenceAfter: session.confidenceAfter,
      confidenceLabel: session.confidenceLabel,
      reflectionMode: session.reflectionMode,
    }))
);

const createDemoDebriefs = (sessions: StudySessionRecord[]): DebriefEntry[] => {
  const legacyStrategies = ['past-papers', 'active-recall', 'summarising', 'teaching', 'flashcards'];
  return sessions
    .filter((session, index) => new Date(session.completedAt).getHours() === 12 && index % 4 === 0)
    .map((session, index) => ({
      id: `demo-debrief-${session.id}`,
      date: session.date,
      subject: session.subject,
      sessionType: session.sessionType,
      durationMinutes: Math.round(session.actualSeconds / 60),
      hardestTopic: index % 2 === 0 ? 'Applying ideas under time pressure' : 'Remembering precise key terms',
      topicsCovered: index % 2 === 0 ? ['Timed application', 'Error review'] : ['Core concepts'],
      strategy: legacyStrategies[index % legacyStrategies.length],
      confidenceBefore: clamp((session.confidenceAfter ?? 3) - 1, 1, 5),
      confidenceAfter: session.confidenceAfter ?? 3,
      whatWorked: index % 2 === 0
        ? 'Closed-book recall, then correcting in a different colour.'
        : 'Short timed questions followed by an examiner-style review.',
    }));
};

export const createDemoTopicMastery = (
  profile: StudentSubjectProfile,
  today = new Date(),
): TopicMasteryV2 => {
  const topics: TopicMasteryV2['topics'] = {};
  const examYear = Number(profile.examStartDate.slice(0, 4));
  const confidencePattern: UnifiedConfidence[] = [
    'solid', 'shaky', 'solid', 'not-started', 'shaky', 'solid', 'shaky', 'not-started',
  ];

  profile.subjects.forEach((subject, subjectIndex) => {
    const specification = resolveCurriculumSpecification(subject.subjectName, examYear);
    if (!specification) return;
    const coverageNodes = specification.coverageNodeLevel === 'topic'
      ? specification.groups.flatMap(group => group.topics.map(topic => ({ id: topic.id, name: topic.title })))
      : specification.groups.map(group => ({ id: group.id, name: group.title }));

    coverageNodes.slice(0, 8 + (subjectIndex % 4)).forEach((node, nodeIndex) => {
      const confidence = confidencePattern[(nodeIndex + subjectIndex) % confidencePattern.length];
      const updated = atLocalTime(dateDaysAgo(today, (nodeIndex * 3) + subjectIndex), 19);
      const source = nodeIndex % 3 === 0 ? 'debrief' as const : 'manual' as const;
      topics[canonicalMasteryKey(specification.id, node.id)] = {
        subjectId: specification.subjectId,
        subjectName: specification.subjectName,
        specificationId: specification.id,
        topicId: node.id,
        topicName: node.name,
        confidence,
        updatedAt: updated.getTime(),
        source,
        ...(source === 'debrief' ? { lastDebriefDate: toDateKey(updated) } : {}),
      };
    });
  });

  return { schemaVersion: 2, topics, unresolved: {} };
};

export const createDemoMockResults = (
  today = new Date(),
  subjects = createDemoStudentProfile(today).subjects.map(subject => subject.subjectName),
): UnifiedMockResult[] => {
  const dayOffsets = [310, 250, 190, 130, 80, 35, 6, 2, 0];
  const totals = [338, 356, 381, 405, 428, 449, 468, 492, 506];
  const labels = [
    'Baseline papers',
    'Autumn checkpoint',
    'Term assessment',
    'Winter papers',
    'January checkpoint',
    'Spring papers',
    'Timed paper set',
    'Weekly assessment',
    'Latest practice mock',
  ];

  return dayOffsets.map((daysAgo, resultIndex) => {
    const day = dateDaysAgo(today, daysAgo);
    const date = toDateKey(day);
    return {
      id: `demo-mock-${date}-${resultIndex}`,
      label: labels[resultIndex],
      date,
      entries: subjects.map((subjectName, subjectIndex) => {
        const gradeNumber = clamp(6 - Math.floor(resultIndex / 2) + ((subjectIndex % 3) - 1), 1, 7);
        return { subjectName, grade: `H${gradeNumber}`, level: 'higher' };
      }),
      totalPoints: totals[resultIndex],
      timestamp: atLocalTime(day, 15).getTime(),
      resultKind: 'full',
    };
  });
};

export const createDemoTimetableCompletions = (today = new Date()): Record<string, string[]> => {
  const completions: Record<string, string[]> = {};
  let studyDaysSeen = 0;
  for (let daysAgo = 0; daysAgo < 64; daysAgo += 1) {
    const day = dateDaysAgo(today, daysAgo);
    // A deliberate older gap makes the live streak 18 study days while the
    // saved personal best remains 42 days.
    if (day.getDay() === 0) continue;
    studyDaysSeen += 1;
    if (studyDaysSeen === 19) continue;
    const date = toDateKey(day);
    const blockCount = daysAgo % 4 === 0 ? 3 : daysAgo % 2 === 0 ? 2 : 1;
    completions[date] = Array.from(
      { length: blockCount },
      (_unused, index) => `demo-plan-${date}-${index}`,
    );
  }
  return completions;
};

export interface DemoStudentLoadedData {
  userProgress: UserProgress;
  northStar: NorthStar;
  studentProfile: StudentSubjectProfile;
  needsOnboarding: false;
  unlockedAvatarSeeds: string[];
  unlockedThemes: string[];
  unlockedCardStyles: string[];
  dismissedGuides: Record<string, string>;
  timetableCompletions: Record<string, string[]>;
  rawProgressDoc: ProgressDocument;
}

export const createDemoStudentLoadedData = (today = new Date()): DemoStudentLoadedData => {
  const studentProfile = createDemoStudentProfile(today);
  const northStar = createDemoStudentNorthStar(today);
  const userProgress = createDemoModuleProgress(studentProfile);
  const studySessions = createDemoStudySessions(
    today,
    studentProfile.subjects.map(subject => subject.subjectName),
  );
  const timetableCompletions = createDemoTimetableCompletions(today);
  const reflections = createDemoReflections(studySessions);
  const studyDebriefs = createDemoDebriefs(studySessions);
  const topicMasteryV2 = createDemoTopicMastery(studentProfile, today);
  const unifiedMockResults = createDemoMockResults(
    today,
    studentProfile.subjects.map(subject => subject.subjectName),
  );
  const latestDate = toDateKey(today);
  const gamification = createDemoGamification(today);

  return {
    userProgress,
    northStar,
    studentProfile,
    needsOnboarding: false,
    unlockedAvatarSeeds: ['Mary Baker', 'Harriet Tubman', 'Ma Rainey', 'Annie Jump'],
    unlockedThemes: [],
    unlockedCardStyles: ['glass', 'flat', 'gradient'],
    dismissedGuides: {},
    timetableCompletions,
    rawProgressDoc: {
      ...userProgress,
      subjectProfile: studentProfile,
      northStar,
      timetableCompletions,
      timetableStreak: { currentStreak: 18, longestStreak: 42, lastActiveDate: latestDate },
      pointsData: { totalEarned: 6_240, totalSpent: 1_175 },
      cosmeticUnlocks: {
        avatarSeeds: ['Mary Baker', 'Harriet Tubman', 'Ma Rainey', 'Annie Jump'],
        themeColors: [],
        cardStyles: ['glass', 'flat', 'gradient'],
      },
      studySessions,
      studyDebriefs,
      reflections,
      topicMasteryV2,
      unifiedMockResults,
      questRewards: {
        'demo-welcome-quest': atLocalTime(dateDaysAgo(today, 1), 18).toISOString(),
      },
      gamification,
      earnedRest: { restDayPasses: [] },
    },
  };
};

const canUseBrowserStorage = (): boolean => typeof window !== 'undefined';

const readStoredDemoProgress = (): ProgressDocument | null => {
  if (!canUseBrowserStorage()) return null;
  try {
    const stored = window.localStorage.getItem(DEMO_PROGRESS_STORAGE_KEY);
    if (!stored) return null;
    const parsed = JSON.parse(stored) as unknown;
    return parsed && typeof parsed === 'object' && !Array.isArray(parsed)
      ? parsed as ProgressDocument
      : null;
  } catch {
    return null;
  }
};

/** Rebuild the date-aware demo seed and layer locally saved interactions over it. */
export const loadDemoStudentLoadedData = (today = new Date()): DemoStudentLoadedData => {
  const seeded = createDemoStudentLoadedData(today);
  const stored = readStoredDemoProgress();
  if (!stored) return seeded;

  const rawProgressDoc: ProgressDocument = { ...seeded.rawProgressDoc, ...stored };
  const studentProfile = (rawProgressDoc.subjectProfile as StudentSubjectProfile | undefined)
    ?? seeded.studentProfile;
  const northStar = (rawProgressDoc.northStar as NorthStar | undefined) ?? seeded.northStar;
  const cosmeticUnlocks = rawProgressDoc.cosmeticUnlocks ?? {};

  return {
    ...seeded,
    userProgress: extractModuleProgress(rawProgressDoc),
    studentProfile,
    northStar,
    dismissedGuides: rawProgressDoc.dismissedGuides ?? seeded.dismissedGuides,
    timetableCompletions: rawProgressDoc.timetableCompletions ?? seeded.timetableCompletions,
    unlockedAvatarSeeds: cosmeticUnlocks.avatarSeeds ?? seeded.unlockedAvatarSeeds,
    unlockedThemes: cosmeticUnlocks.themeColors ?? seeded.unlockedThemes,
    unlockedCardStyles: cosmeticUnlocks.cardStyles ?? seeded.unlockedCardStyles,
    rawProgressDoc,
  };
};

export const persistDemoStudentProgress = (progress: ProgressDocument): void => {
  if (!canUseBrowserStorage()) return;
  try {
    window.localStorage.setItem(DEMO_PROGRESS_STORAGE_KEY, JSON.stringify(progress));
  } catch {
    // Privacy-restricted embeds can disable storage; in-memory demo state still works.
  }
};

export const markDemoSessionActive = (): void => {
  if (!canUseBrowserStorage()) return;
  try {
    window.sessionStorage.setItem(DEMO_SESSION_STORAGE_KEY, 'active');
  } catch {
    // In-memory login remains the fallback.
  }
};

export const clearDemoSession = (): void => {
  if (!canUseBrowserStorage()) return;
  try {
    window.sessionStorage.removeItem(DEMO_SESSION_STORAGE_KEY);
  } catch {
    // Nothing else to clear when storage is unavailable.
  }
};

export const hasActiveDemoSession = (): boolean => {
  if (!canUseBrowserStorage()) return false;
  try {
    return window.sessionStorage.getItem(DEMO_SESSION_STORAGE_KEY) === 'active';
  } catch {
    return false;
  }
};

/** @deprecated Local tooling aliases retained while callers migrate names. */
export const createDevStudentSession = createDemoStudentSession;
export const createDevStudentProfile = createDemoStudentProfile;
export const createDevStudentNorthStar = createDemoStudentNorthStar;
export const createDevStudentLoadedData = createDemoStudentLoadedData;
