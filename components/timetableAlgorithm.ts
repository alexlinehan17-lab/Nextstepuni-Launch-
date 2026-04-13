/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 */

import {
  type StudentSubject, type StudyBlock, type WeeklyTimetable, type Grade,
  type TimetableCompletions,
  LC_SUBJECTS, DAYS_OF_WEEK, getPointsForGrade, getGradeIndex, HIGHER_GRADES, ORDINARY_GRADES,
  toDateKey,
} from './subjectData';
import { getSyllabusForSubject, computeEfficiency } from './syllabusData';
import { type TopicMasteryMap } from '../types';

// ─── SM-2 Spaced Repetition Algorithm ──────────────────────────────────────
//
// Based on the SuperMemo SM-2 algorithm by Piotr Wozniak.
// Adapted for subject-level scheduling rather than individual flashcards.
// Each subject tracks its own ease factor and optimal review interval.

export interface SubjectSM2State {
  subjectName: string;
  easeFactor: number;     // starts 2.5, min 1.3 — how "easy" the subject is for this student
  interval: number;       // days until next review (1, 3, 7, 14, 28, etc.)
  repetitions: number;    // consecutive successful reviews (quality >= 3)
  nextReviewDate: string; // ISO date "YYYY-MM-DD"
  lastQuality: number;    // 0-5, last session quality
}

/** Initialise SM-2 state for subjects that have no history yet. */
export function initSM2States(subjectNames: string[], today: Date = new Date()): SubjectSM2State[] {
  const todayKey = toDateKey(today);
  return subjectNames.map(name => ({
    subjectName: name,
    easeFactor: 2.5,
    interval: 1,
    repetitions: 0,
    nextReviewDate: todayKey,
    lastQuality: 0,
  }));
}

/**
 * Core SM-2 update. Called after a study session is completed.
 *
 * Quality scale (0-5):
 *   5 — Perfect, no hesitation
 *   4 — Correct with minor hesitation
 *   3 — Correct but with difficulty
 *   2 — Incorrect but close / recognised answer
 *   1 — Incorrect, vague memory
 *   0 — Complete blackout
 *
 * If quality < 3: reset repetitions (start interval over — the student needs
 * to re-learn this material). If quality >= 3: advance the interval.
 */
export function updateSM2(state: SubjectSM2State, quality: number, today: Date = new Date()): SubjectSM2State {
  const q = Math.max(0, Math.min(5, Math.round(quality)));

  // Update ease factor using SM-2 formula
  // EF' = EF + (0.1 - (5 - q) * (0.08 + (5 - q) * 0.02))
  let newEF = state.easeFactor + (0.1 - (5 - q) * (0.08 + (5 - q) * 0.02));
  newEF = Math.max(1.3, newEF); // floor at 1.3

  let newInterval: number;
  let newReps: number;

  if (q < 3) {
    // Failed — reset to beginning
    newReps = 0;
    newInterval = 1;
  } else {
    newReps = state.repetitions + 1;
    if (newReps === 1) {
      newInterval = 1;   // first successful review: see again tomorrow
    } else if (newReps === 2) {
      newInterval = 3;   // second: 3 days
    } else {
      // subsequent: multiply previous interval by ease factor
      newInterval = Math.round(state.interval * newEF);
    }
  }

  // Cap interval at 60 days for exam prep context — students shouldn't go
  // more than ~2 months without touching a subject
  newInterval = Math.min(60, newInterval);

  const nextDate = new Date(today);
  nextDate.setDate(nextDate.getDate() + newInterval);

  return {
    subjectName: state.subjectName,
    easeFactor: newEF,
    interval: newInterval,
    repetitions: newReps,
    nextReviewDate: toDateKey(nextDate),
    lastQuality: q,
  };
}

/**
 * Derive a quality score (0-5) from study debrief data.
 * Maps confidence gain and completion status to the SM-2 quality scale.
 */
export function qualityFromDebrief(
  confidenceBefore: number, // 1-5
  confidenceAfter: number,  // 1-5
  completed: boolean
): number {
  if (!completed) return 1; // incomplete session

  const gain = confidenceAfter - confidenceBefore;
  const level = confidenceAfter;

  // High confidence after + positive gain → high quality
  if (level >= 5 && gain >= 1) return 5;
  if (level >= 4 && gain >= 0) return 4;
  if (level >= 3) return 3;
  if (level >= 2) return 2;
  return 1;
}

/**
 * Simpler quality derivation when no debrief data exists.
 * Just based on whether the student completed the session.
 */
export function qualityFromCompletion(completed: boolean): number {
  return completed ? 4 : 1;
}

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
  efficiencyMultiplier: number;
  priorityScore: number;
}

export function computeSubjectPriorities(
  subjects: StudentSubject[],
  topicMastery?: TopicMasteryMap
): SubjectPriority[] {
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

    // Syllabus efficiency: subjects with higher-efficiency topics get a small boost
    // This encourages studying subjects where effort yields more exam marks
    let efficiencyMultiplier = 1.0;
    const syllabus = getSyllabusForSubject(s.subjectName);
    if (syllabus && syllabus.topics.length > 0) {
      const avgEfficiency = syllabus.topics.reduce(
        (sum, t) => sum + computeEfficiency(t, syllabus.totalMarks), 0
      ) / syllabus.topics.length;
      // Normalize: avg efficiency ~1-5 range, map to 0.85–1.15 multiplier
      efficiencyMultiplier = Math.max(0.85, Math.min(1.15, 0.9 + avgEfficiency * 0.05));
    }

    // Topic mastery boost: subjects with more shaky topics get higher priority
    let topicBoost = 1.0;
    if (topicMastery && topicMastery[s.subjectName]) {
      const topics = topicMastery[s.subjectName];
      const topicEntries = Object.values(topics);
      if (topicEntries.length > 0) {
        const shakyCount = topicEntries.filter(t => t.confidence === 'shaky').length;
        const notStartedCount = topicEntries.filter(t => t.confidence === 'not-started').length;
        const shakyRatio = (shakyCount + notStartedCount * 0.5) / topicEntries.length;
        // Boost up to 1.3x for subjects where most topics are shaky/not-started
        topicBoost = 1.0 + shakyRatio * 0.3;
      }
    }

    const priorityScore = pointsGain * difficultyMultiplier * efficiencyMultiplier * topicBoost;

    return {
      subjectName: s.subjectName,
      currentGrade: s.currentGrade,
      targetGrade: s.targetGrade,
      isMaths,
      currentPoints,
      targetPoints,
      pointsGain,
      difficultyMultiplier,
      efficiencyMultiplier,
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

// ─── Sustainability Limits ──────────────────────────────────────────────────
//
// Study hours per week must be sustainable. Research shows diminishing returns
// beyond ~3 hours/day for focused study. These limits scale with exam proximity.

/** Maximum study blocks per weekday (school day — student has 6+ hours of classes). */
function weekdayBlockCap(weeksUntilExam: number): number {
  if (weeksUntilExam <= 2) return 4;  // exam crunch: ~3 hours
  if (weeksUntilExam <= 6) return 3;  // pre-exam: ~2.25 hours
  return 3;                            // normal: ~2.25 hours
}

/** Maximum study blocks per weekend day (no school — more time available). */
function weekendBlockCap(weeksUntilExam: number): number {
  if (weeksUntilExam <= 2) return 6;  // exam crunch: ~4.5 hours
  if (weeksUntilExam <= 6) return 5;  // pre-exam: ~3.75 hours
  return 4;                            // normal: ~3 hours
}

/** Maximum total weekly study hours based on distance from exams. */
function maxWeeklyHours(weeksUntilExam: number): number {
  if (weeksUntilExam <= 2) return 22;  // absolute max during crunch
  if (weeksUntilExam <= 6) return 18;
  if (weeksUntilExam <= 12) return 15;
  if (weeksUntilExam <= 20) return 12;
  return 10;                            // far from exams: sustainable base
}

// Weekend day indices: Saturday = 5, Sunday = 6 in DAYS_OF_WEEK
const WEEKEND_INDICES = new Set([5, 6]);

// Maximum ratio between the most-studied and least-studied subject.
const MAX_SESSION_RATIO = 3;

export function allocateSessions(
  priorities: SubjectPriority[],
  weeksUntilExam: number,
  sm2States?: SubjectSM2State[]
): SessionAllocation[] {
  const intensity = computeIntensityFactor(weeksUntilExam);
  // Base: 14 sessions/week (2/day). Ramps to 21 (3/day) at max intensity
  const totalSessions = Math.round(14 + intensity * 7);
  const n = priorities.length;

  if (n === 0) return [];

  const totalPriority = priorities.reduce((sum, p) => sum + p.priorityScore, 0);
  if (totalPriority === 0) {
    const perSubject = Math.max(1, Math.floor(totalSessions / n));
    return priorities.map(p => ({
      subjectName: p.subjectName,
      sessions: perSubject,
      priorityLabel: 'Medium' as const,
      priorityScore: p.priorityScore,
    }));
  }

  // If we have SM-2 states, boost subjects with low ease factors (harder)
  // and reduce sessions for subjects with long intervals (well-learned).
  const sm2Map = new Map<string, SubjectSM2State>();
  if (sm2States) {
    for (const s of sm2States) sm2Map.set(s.subjectName, s);
  }

  // Compute effective scores: priority × SM-2 urgency multiplier
  const effectiveScores = priorities.map(p => {
    let score = p.priorityScore;
    const sm2 = sm2Map.get(p.subjectName);
    if (sm2) {
      // Lower ease factor = harder = needs more sessions (boost up to 1.5×)
      const easePenalty = Math.max(0.8, Math.min(1.5, 3.0 - sm2.easeFactor));
      // Shorter interval = due sooner = needs more sessions this week
      const intervalUrgency = sm2.interval <= 1 ? 1.4
        : sm2.interval <= 3 ? 1.2
        : sm2.interval <= 7 ? 1.0
        : sm2.interval <= 14 ? 0.85
        : 0.7; // well-learned, long interval — fewer sessions needed
      score *= easePenalty * intervalUrgency;
    }
    return { subjectName: p.subjectName, score, priorityScore: p.priorityScore };
  });

  // Log-scale to compress extreme differences.
  // Subjects at target (score=0) get a small maintenance allocation (0.5 sessions base).
  const logScores = effectiveScores.map(e =>
    e.score > 0 ? Math.log(1 + e.score) : 0
  );
  const totalLog = logScores.reduce((sum, s) => sum + s, 0);

  // Separate zero-priority subjects (at target) from active ones.
  // Zero-priority subjects get 1 maintenance session; the rest of the budget
  // is distributed among active subjects.
  const zeroCount = effectiveScores.filter(e => e.score === 0).length;
  const activeSessionBudget = Math.max(1, totalSessions - zeroCount);

  let shares: number[];
  if (totalLog === 0) {
    // All subjects are at target — equal distribution
    shares = logScores.map(() => totalSessions / n);
  } else {
    shares = logScores.map(s =>
      s > 0 ? (s / totalLog) * activeSessionBudget : 1
    );
  }

  // Enforce max ratio (only among subjects with non-zero shares > 1)
  const nonZeroShares = shares.filter(s => s > 1);
  if (nonZeroShares.length > 0) {
    for (let iter = 0; iter < 10; iter++) {
      const minNonZero = Math.min(...shares.filter(s => s > 1));
      const maxAllowed = minNonZero * MAX_SESSION_RATIO;
      let clamped = false;
      let excess = 0;
      let unclampedCount = 0;

      const clampedShares = shares.map(s => {
        if (s <= 1) return s; // don't clamp maintenance sessions
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

      if (unclampedCount > 0) {
        const unclampedTotal = clampedShares.reduce((sum, s) =>
          sum + (s > 1 && s < maxAllowed ? s : 0), 0);
        shares = clampedShares.map(s => {
          if (s > 1 && s < maxAllowed && unclampedTotal > 0) {
            return s + (s / unclampedTotal) * excess;
          }
          return s;
        });
      } else {
        shares = clampedShares;
        break;
      }
    }
  }

  // Round to integers with minimum 1 per subject
  const allocations = priorities.map((p, i) => ({
    subjectName: p.subjectName,
    sessions: Math.max(1, Math.round(shares[i])),
    priorityScore: p.priorityScore,
  }));

  // Adjust total to match target
  let currentTotal = allocations.reduce((sum, a) => sum + a.sessions, 0);
  while (currentTotal > totalSessions) {
    const maxSess = Math.max(...allocations.map(a => a.sessions));
    const idx = allocations.findIndex(a => a.sessions === maxSess);
    if (allocations[idx].sessions > 1) {
      allocations[idx].sessions--;
      currentTotal--;
    } else break;
  }
  while (currentTotal < totalSessions) {
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
//
// Now uses SM-2 principles for spacing, weekend-aware loading, and daily caps.

export function generateWeeklyTimetable(
  allocations: SessionAllocation[],
  weeksUntilExam: number,
  weekOffset: number = 0,
  restDays: string[] = [],
  blockDuration: number = 45,
  sm2States?: SubjectSM2State[],
  topicMastery?: TopicMasteryMap
): WeeklyTimetable {
  const effectiveWeeks = Math.max(0, weeksUntilExam - weekOffset);
  const intensity = computeIntensityFactor(effectiveWeeks);

  // Session type distribution based on SM-2 state + exam proximity
  const sm2Map = new Map<string, SubjectSM2State>();
  if (sm2States) {
    for (const s of sm2States) sm2Map.set(s.subjectName, s);
  }

  // Determine available days and their capacities
  const restDaySet = new Set(restDays);
  const dayCaps: number[] = DAYS_OF_WEEK.map((day, i) => {
    if (restDaySet.has(day)) return 0;
    return WEEKEND_INDICES.has(i)
      ? weekendBlockCap(effectiveWeeks)
      : weekdayBlockCap(effectiveWeeks);
  });

  // Enforce weekly hours sustainability cap
  const maxMinutes = maxWeeklyHours(effectiveWeeks) * 60;
  const maxTotalBlocks = Math.floor(maxMinutes / blockDuration);
  const totalCapacity = dayCaps.reduce((s, c) => s + c, 0);
  const effectiveCapacity = Math.min(totalCapacity, maxTotalBlocks);

  // Build blocks for each subject, capped to effective capacity
  const allBlocks: { block: StudyBlock; priority: number; subjectName: string }[] = [];
  const totalRequested = allocations.reduce((s, a) => s + a.sessions, 0);
  const scaleFactor = totalRequested > effectiveCapacity
    ? effectiveCapacity / totalRequested
    : 1;

  for (const alloc of allocations) {
    const scaledSessions = Math.max(1, Math.round(alloc.sessions * scaleFactor));
    const sm2 = sm2Map.get(alloc.subjectName);

    for (let i = 0; i < scaledSessions; i++) {
      // Determine session type using SM-2 state, not random
      let sessionType: StudyBlock['sessionType'];
      if (sm2) {
        // SM-2 driven: subjects with many reps → more practice/revision
        // New subjects (few reps) → more new-learning
        if (sm2.repetitions === 0) {
          sessionType = 'new-learning';
        } else if (sm2.repetitions <= 2 || sm2.easeFactor < 2.0) {
          // Still learning or struggling — mix of revision and practice
          sessionType = (i % 2 === 0) ? 'revision' : 'practice';
        } else {
          // Well-practiced — mostly practice with some revision
          sessionType = (i % 3 === 0) ? 'revision' : 'practice';
        }
      } else {
        // Fallback: use exam proximity
        const practiceRatio = 0.1 + intensity * 0.6;
        const revisionRatio = 0.1 + intensity * 0.1;
        const rand = seededRandom(hashString(alloc.subjectName) + i + weekOffset * 1000);
        if (rand < practiceRatio) {
          sessionType = 'practice';
        } else if (rand < practiceRatio + revisionRatio) {
          sessionType = 'revision';
        } else {
          sessionType = 'new-learning';
        }
      }

      // Suggest shaky topics for this block
      let suggestedTopics: string[] | undefined;
      if (topicMastery && topicMastery[alloc.subjectName]) {
        const topics = topicMastery[alloc.subjectName];
        suggestedTopics = Object.entries(topics)
          .filter(([, entry]) => entry.confidence === 'shaky')
          .sort((a, b) => a[1].updatedAt - b[1].updatedAt) // oldest first
          .slice(0, 3)
          .map(([name]) => name);
      }

      allBlocks.push({
        block: { subjectName: alloc.subjectName, sessionType, durationMinutes: blockDuration, suggestedTopics },
        priority: alloc.priorityScore,
        subjectName: alloc.subjectName,
      });
    }
  }

  // ─── SM-2 Aware Day Assignment ──────────────────────────────────────────
  //
  // Goals:
  // 1. Maximise spacing between same-subject sessions (SM-2 principle)
  // 2. Weekend days get more blocks (student has no school)
  // 3. No day exceeds its cap
  // 4. Higher-priority subjects placed first (best slots)

  const dayAssignments: StudyBlock[][] = Array.from({ length: 7 }, () => []);
  const dayLoads: number[] = Array(7).fill(0);

  // Sort subjects by priority (highest first) for placement precedence
  const subjectGroups = new Map<string, typeof allBlocks>();
  for (const entry of allBlocks) {
    if (!subjectGroups.has(entry.subjectName)) subjectGroups.set(entry.subjectName, []);
    subjectGroups.get(entry.subjectName)!.push(entry);
  }

  const sortedSubjects = [...subjectGroups.entries()]
    .sort((a, b) => b[1][0].priority - a[1][0].priority);

  // Available day indices (not rest days)
  const availableDayIndices = DAYS_OF_WEEK
    .map((day, i) => ({ day, i }))
    .filter(d => !restDaySet.has(d.day))
    .map(d => d.i);

  if (availableDayIndices.length === 0) {
    return DAYS_OF_WEEK.map(day => ({ day, blocks: [] }));
  }

  for (const [subjectName, entries] of sortedSubjects) {
    const count = entries.length;
    if (count === 0) continue;

    // Compute optimal spacing: spread sessions as far apart as possible
    // SM-2 interval tells us the ideal gap between reviews
    const sm2 = sm2Map.get(subjectName);
    const idealGap = sm2
      ? Math.max(1, Math.min(sm2.interval, Math.floor(availableDayIndices.length / count)))
      : Math.max(1, Math.floor(availableDayIndices.length / count));

    // Place sessions with maximum spacing, respecting daily caps
    // Start position varies per subject to avoid all subjects clustering on the same days
    const startOffset = hashString(subjectName) % availableDayIndices.length;

    const placedDays: number[] = [];
    for (let i = 0; i < count; i++) {
      // Ideal slot: spaced by idealGap from the start offset
      const idealSlotIdx = (startOffset + i * idealGap) % availableDayIndices.length;

      // Find the best available day near the ideal slot
      let bestDay = -1;
      let bestScore = -Infinity;

      for (let search = 0; search < availableDayIndices.length; search++) {
        const slotIdx = (idealSlotIdx + search) % availableDayIndices.length;
        const dayIdx = availableDayIndices[slotIdx];

        // Skip if day is at capacity
        if (dayLoads[dayIdx] >= dayCaps[dayIdx]) continue;

        // Score this slot: prefer days that are far from other sessions of same subject
        let minDistToSame = availableDayIndices.length; // max possible
        for (const pd of placedDays) {
          const dist = Math.min(
            Math.abs(dayIdx - pd),
            7 - Math.abs(dayIdx - pd) // wrap-around distance
          );
          minDistToSame = Math.min(minDistToSame, dist);
        }

        // Prefer: (1) maximum distance from same subject, (2) closer to ideal slot,
        // (3) lighter load days, (4) weekend days (more free time)
        const distFromIdeal = Math.min(search, availableDayIndices.length - search);
        const loadPenalty = dayLoads[dayIdx] * 0.5;
        // Weekend bonus: prefer placing blocks on Sat/Sun since student has no school.
        // Scale by how full the day is relative to cap — fuller weekends get less bonus.
        const isWeekend = WEEKEND_INDICES.has(dayIdx);
        const remainingCapRatio = dayCaps[dayIdx] > 0 ? 1 - (dayLoads[dayIdx] / dayCaps[dayIdx]) : 0;
        const weekendBonus = isWeekend ? 3 * remainingCapRatio : 0;
        const score = minDistToSame * 10 - distFromIdeal - loadPenalty + weekendBonus;

        if (score > bestScore) {
          bestScore = score;
          bestDay = dayIdx;
        }
      }

      // Fallback: if no day has capacity, find the least loaded day
      if (bestDay === -1) {
        bestDay = availableDayIndices.reduce((best, di) =>
          dayLoads[di] < dayLoads[best] ? di : best, availableDayIndices[0]);
      }

      dayAssignments[bestDay].push(entries[i].block);
      dayLoads[bestDay]++;
      placedDays.push(bestDay);
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
): { currentStreak: number; longestStreak: number; lastActiveDate: string } {
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

  return { currentStreak: streak, longestStreak: streak, lastActiveDate: lastActiveDate || todayKey };
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
