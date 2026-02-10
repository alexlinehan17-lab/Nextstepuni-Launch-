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

export function allocateSessions(
  priorities: SubjectPriority[],
  weeksUntilExam: number
): SessionAllocation[] {
  const intensity = computeIntensityFactor(weeksUntilExam);
  // Base: 14 sessions/week (2/day). Ramps to 21 (3/day) at max intensity
  const totalSessions = Math.round(14 + intensity * 7);

  const totalPriority = priorities.reduce((sum, p) => sum + p.priorityScore, 0);
  if (totalPriority === 0 || priorities.length === 0) {
    // Equal distribution if no priority differences
    const perSubject = Math.max(1, Math.floor(totalSessions / Math.max(1, priorities.length)));
    return priorities.map(p => ({
      subjectName: p.subjectName,
      sessions: perSubject,
      priorityLabel: 'Medium' as const,
      priorityScore: p.priorityScore,
    }));
  }

  // Proportional allocation with minimum 1 session per subject
  let allocations = priorities.map(p => ({
    subjectName: p.subjectName,
    rawShare: (p.priorityScore / totalPriority) * totalSessions,
    sessions: 0,
    priorityScore: p.priorityScore,
  }));

  // Assign minimum 1 to each, then distribute remainder proportionally
  let remaining = totalSessions - priorities.length; // reserve 1 each
  allocations = allocations.map(a => ({ ...a, sessions: 1 }));

  if (remaining > 0) {
    // Sort by rawShare descending for allocation
    const sorted = [...allocations].sort((a, b) => b.rawShare - a.rawShare);
    for (const alloc of sorted) {
      const extra = Math.round((alloc.rawShare - 1)); // how many extra beyond the 1
      const toAdd = Math.min(Math.max(0, extra), remaining);
      alloc.sessions += toAdd;
      remaining -= toAdd;
    }
    // Distribute any leftover one by one
    let idx = 0;
    while (remaining > 0) {
      sorted[idx % sorted.length].sessions += 1;
      remaining--;
      idx++;
    }
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
  restDays: string[] = []
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
        durationMinutes: 45,
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
  today: Date = new Date()
): { currentStreak: number; lastActiveDate: string } {
  const restSet = new Set(restDays);
  // Day names matching DAYS_OF_WEEK indexing (0=Mon..6=Sun)
  const dayNames = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'];

  const getDayName = (d: Date): string => {
    const jsDay = d.getDay(); // 0=Sun
    const idx = jsDay === 0 ? 6 : jsDay - 1; // convert to 0=Mon
    return dayNames[idx];
  };

  const todayKey = toDateKey(today);
  const todayDayName = getDayName(today);
  const todayIsRest = restSet.has(todayDayName);
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

    if (restSet.has(dayName)) continue; // skip rest days

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
