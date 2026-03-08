/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 */

import {
  type StudentSubject, type StudyBlock, type DaySchedule, type WeeklyTimetable, type Grade,
  type TimetableCompletions,
  LC_SUBJECTS, DAYS_OF_WEEK, getPointsForGrade, getGradeIndex, HIGHER_GRADES, ORDINARY_GRADES,
  toDateKey,
} from './subjectData';

// ─── Priority Scoring ───────────────────────────────────────────────────────

export interface SubjectPriority {
  subjectName: string;
  currentGrade: Grade;
  targetGrade: Grade;
  isMaths: boolean;
  currentPoints: number;
  targetPoints: number;
  pointsGain: number;
  difficultyMultiplier: number;
  priorityScore: number;
}

export function computeSubjectPriorities(subjects: StudentSubject[]): SubjectPriority[] {
  return subjects.map(s => {
    const lcSubject = LC_SUBJECTS.find(lc => lc.name === s.subjectName);
    const isMaths = lcSubject?.isMaths || false;

    const currentPoints = getPointsForGrade(s.currentGrade, isMaths);
    const targetPoints = getPointsForGrade(s.targetGrade, isMaths);
    const pointsGain = Math.max(0, targetPoints - currentPoints);

    // Diminishing returns: weaker students (higher grade index) get higher multiplier
    const gradeIdx = getGradeIndex(s.currentGrade);
    const scale = s.currentGrade.startsWith('H') ? HIGHER_GRADES.length : ORDINARY_GRADES.length;
    const difficultyMultiplier = Math.max(0.3, gradeIdx / (scale - 1));

    const priorityScore = pointsGain * difficultyMultiplier;

    return {
      subjectName: s.subjectName,
      currentGrade: s.currentGrade,
      targetGrade: s.targetGrade,
      isMaths,
      currentPoints,
      targetPoints,
      pointsGain,
      difficultyMultiplier,
      priorityScore,
    };
  }).sort((a, b) => b.priorityScore - a.priorityScore);
}

// ─── Session Allocation ─────────────────────────────────────────────────────

export function computeWeeksUntilExam(examDateStr: string): number {
  const now = new Date();
  now.setHours(0, 0, 0, 0);
  const exam = new Date(examDateStr);
  exam.setHours(0, 0, 0, 0);
  const diffMs = exam.getTime() - now.getTime();
  return Math.max(0, Math.floor(diffMs / (7 * 24 * 60 * 60 * 1000)));
}

export function computeIntensityFactor(weeksUntilExam: number): number {
  // Ramps from 0 (far away) to 1 (exam imminent, <=4 weeks)
  return Math.min(1, Math.max(0, 1 - (weeksUntilExam - 4) / 20));
}

export interface SessionAllocation {
  subjectName: string;
  sessions: number;
  priorityLabel: 'High' | 'Medium' | 'Low';
  priorityScore: number;
}

// Maximum ratio between the most-studied and least-studied subject.
// e.g. 3 means the top subject gets at most 3× the sessions of the bottom.
const MAX_SESSION_RATIO = 3;

export function allocateSessions(
  priorities: SubjectPriority[],
  weeksUntilExam: number
): SessionAllocation[] {
  const intensity = computeIntensityFactor(weeksUntilExam);
  // Base: 14 sessions/week (2/day). Ramps to 21 (3/day) at max intensity
  const totalSessions = Math.round(14 + intensity * 7);
  const n = priorities.length;

  if (n === 0) return [];

  const totalPriority = priorities.reduce((sum, p) => sum + p.priorityScore, 0);
  if (totalPriority === 0) {
    // Equal distribution if no priority differences
    const perSubject = Math.max(1, Math.floor(totalSessions / n));
    return priorities.map(p => ({
      subjectName: p.subjectName,
      sessions: perSubject,
      priorityLabel: 'Medium' as const,
      priorityScore: p.priorityScore,
    }));
  }

  // Log-scale the priority scores to compress extreme differences.
  // A subject with 80× the raw score should NOT get 80× the sessions.
  // log(1 + score) maps 0→0 and compresses large values.
  const logScores = priorities.map(p => Math.log(1 + p.priorityScore));
  const totalLog = logScores.reduce((sum, s) => sum + s, 0);

  // Compute raw proportional shares from log-scaled scores
  let shares = logScores.map(s => (s / totalLog) * totalSessions);

  // Enforce max ratio: no subject gets more than MAX_SESSION_RATIO × the minimum.
  // We iteratively clamp until stable.
  for (let iter = 0; iter < 10; iter++) {
    const minShare = Math.min(...shares);
    const maxAllowed = minShare * MAX_SESSION_RATIO;
    let clamped = false;
    let excess = 0;
    let unclampedCount = 0;

    const clampedShares = shares.map(s => {
      if (s > maxAllowed) {
        excess += s - maxAllowed;
        clamped = true;
        return maxAllowed;
      }
      unclampedCount++;
      return s;
    });

    if (!clamped) {
      shares = clampedShares;
      break;
    }

    // Redistribute excess to unclamped subjects proportionally
    if (unclampedCount > 0) {
      const unclampedTotal = clampedShares.reduce((sum, s, i) =>
        sum + (s < maxAllowed ? s : 0), 0);
      shares = clampedShares.map(s => {
        if (s < maxAllowed && unclampedTotal > 0) {
          return s + (s / unclampedTotal) * excess;
        }
        return s;
      });
    } else {
      shares = clampedShares;
      break;
    }
  }

  // Round to integers with minimum 1 per subject
  let allocations = priorities.map((p, i) => ({
    subjectName: p.subjectName,
    sessions: Math.max(1, Math.round(shares[i])),
    priorityScore: p.priorityScore,
  }));

  // Adjust total to match target (rounding may overshoot/undershoot)
  let currentTotal = allocations.reduce((sum, a) => sum + a.sessions, 0);
  while (currentTotal > totalSessions) {
    // Remove from the subject with the most sessions (and lowest priority)
    const maxSessions = Math.max(...allocations.map(a => a.sessions));
    const idx = allocations.findIndex(a => a.sessions === maxSessions);
    if (allocations[idx].sessions > 1) {
      allocations[idx].sessions--;
      currentTotal--;
    } else break;
  }
  while (currentTotal < totalSessions) {
    // Add to the subject with the highest priority score that has fewest sessions
    const sorted = [...allocations]
      .map((a, i) => ({ ...a, idx: i }))
      .sort((a, b) => b.priorityScore - a.priorityScore);
    allocations[sorted[0].idx].sessions++;
    currentTotal++;
  }

  // Compute priority labels based on thirds
  const maxScore = Math.max(...priorities.map(p => p.priorityScore));
  return allocations.map(a => ({
    subjectName: a.subjectName,
    sessions: a.sessions,
    priorityLabel: a.priorityScore >= maxScore * 0.66 ? 'High'
      : a.priorityScore >= maxScore * 0.33 ? 'Medium'
      : 'Low',
    priorityScore: a.priorityScore,
  }));
}

// ─── Weekly Timetable Generation ────────────────────────────────────────────

export function generateWeeklyTimetable(
  allocations: SessionAllocation[],
  weeksUntilExam: number,
  weekOffset: number = 0,
  restDays: string[] = [],
  blockDuration: number = 45
): WeeklyTimetable {
  const effectiveWeeks = Math.max(0, weeksUntilExam - weekOffset);
  const intensity = computeIntensityFactor(effectiveWeeks);

  // Session type distribution based on proximity
  // Far from exams: mostly new-learning. Near exams: mostly practice
  const practiceRatio = 0.1 + intensity * 0.6; // 10% → 70%
  const revisionRatio = 0.1 + intensity * 0.1;  // 10% → 20%
  // Rest is new-learning

  // Determine available day indices (exclude rest days)
  const restDaySet = new Set(restDays);
  const availableDayIndices = DAYS_OF_WEEK
    .map((day, i) => ({ day, i }))
    .filter(d => !restDaySet.has(d.day))
    .map(d => d.i);
  const numAvailable = availableDayIndices.length || 1; // fallback to at least 1

  // Build blocks for each subject
  const allBlocks: StudyBlock[] = [];
  for (const alloc of allocations) {
    for (let i = 0; i < alloc.sessions; i++) {
      // Determine session type
      const rand = seededRandom(hashString(alloc.subjectName) + i + weekOffset * 1000);
      let sessionType: StudyBlock['sessionType'];
      if (rand < practiceRatio) {
        sessionType = 'practice';
      } else if (rand < practiceRatio + revisionRatio) {
        sessionType = 'revision';
      } else {
        sessionType = 'new-learning';
      }

      allBlocks.push({
        subjectName: alloc.subjectName,
        sessionType,
        durationMinutes: blockDuration,
      });
    }
  }

  // Distribute blocks across available days with maximum spacing
  const dayAssignments: StudyBlock[][] = Array.from({ length: 7 }, () => []);

  for (const alloc of allocations) {
    const subjectBlocks = allBlocks.filter(b => b.subjectName === alloc.subjectName);
    const count = subjectBlocks.length;
    if (count === 0) continue;

    // Evenly space across available days only
    for (let i = 0; i < count; i++) {
      const slotIndex = (Math.floor((i * numAvailable) / count) + hashString(alloc.subjectName) % Math.max(1, numAvailable)) % numAvailable;
      const dayIndex = availableDayIndices[slotIndex];
      dayAssignments[dayIndex].push(subjectBlocks[i]);
    }
  }

  // Interleave blocks within each day so same subject doesn't appear consecutively
  for (let d = 0; d < 7; d++) {
    dayAssignments[d] = interleaveBlocks(dayAssignments[d]);
  }

  return DAYS_OF_WEEK.map((day, i) => ({
    day,
    blocks: dayAssignments[i],
  }));
}

// ─── Utilities ──────────────────────────────────────────────────────────────

function hashString(str: string): number {
  let hash = 0;
  for (let i = 0; i < str.length; i++) {
    const char = str.charCodeAt(i);
    hash = ((hash << 5) - hash) + char;
    hash |= 0; // Convert to 32-bit integer
  }
  return Math.abs(hash);
}

function seededRandom(seed: number): number {
  // Simple seeded PRNG
  const x = Math.sin(seed * 9301 + 49297) * 49297;
  return x - Math.floor(x);
}

// ─── Streak Computation ─────────────────────────────────────────────────────

/**
 * Walks backwards from `today` counting consecutive study days with completions.
 * Rest days are skipped entirely (they don't break or extend streaks).
 * If today is a study day with no completions yet, the streak is preserved
 * (user still has time today).
 */
export function computeStreak(
  completions: TimetableCompletions,
  restDays: string[],
  today: Date = new Date(),
  restDayPasses: string[] = []
): { currentStreak: number; lastActiveDate: string } {
  const restSet = new Set(restDays);
  const restPassSet = new Set(restDayPasses);
  // Day names matching DAYS_OF_WEEK indexing (0=Mon..6=Sun)
  const dayNames = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'];

  const getDayName = (d: Date): string => {
    const jsDay = d.getDay(); // 0=Sun
    const idx = jsDay === 0 ? 6 : jsDay - 1; // convert to 0=Mon
    return dayNames[idx];
  };

  const todayKey = toDateKey(today);
  const todayDayName = getDayName(today);
  const todayIsRest = restSet.has(todayDayName) || restPassSet.has(todayKey);
  const todayHasCompletions = (completions[todayKey]?.length ?? 0) > 0;

  let streak = 0;
  let lastActiveDate = '';

  // If today is a study day and has completions, count it
  if (!todayIsRest && todayHasCompletions) {
    streak = 1;
    lastActiveDate = todayKey;
  }

  // Walk backwards from yesterday
  const cursor = new Date(today);
  cursor.setHours(0, 0, 0, 0);
  for (let i = 1; i <= 365; i++) {
    cursor.setDate(cursor.getDate() - 1);
    const key = toDateKey(cursor);
    const dayName = getDayName(cursor);

    if (restSet.has(dayName) || restPassSet.has(key)) continue; // skip rest days and rest day passes

    const dayCompletions = completions[key]?.length ?? 0;
    if (dayCompletions > 0) {
      streak++;
      if (!lastActiveDate) lastActiveDate = key;
    } else {
      break; // streak broken
    }
  }

  // If today is a study day with no completions, streak is preserved from yesterday
  // (already handled — we started counting from yesterday in the walk)
  // Update lastActiveDate if we found completions but today had none
  if (!todayIsRest && !todayHasCompletions && streak > 0 && !lastActiveDate) {
    // lastActiveDate would have been set in the loop
  }

  return { currentStreak: streak, lastActiveDate: lastActiveDate || todayKey };
}

function interleaveBlocks(blocks: StudyBlock[]): StudyBlock[] {
  if (blocks.length <= 1) return blocks;

  // Group by subject
  const groups: Record<string, StudyBlock[]> = {};
  for (const b of blocks) {
    if (!groups[b.subjectName]) groups[b.subjectName] = [];
    groups[b.subjectName].push(b);
  }

  const result: StudyBlock[] = [];
  const queues = Object.values(groups).sort((a, b) => b.length - a.length);

  while (queues.some(q => q.length > 0)) {
    for (const q of queues) {
      if (q.length > 0) {
        result.push(q.shift()!);
      }
    }
  }

  return result;
}
