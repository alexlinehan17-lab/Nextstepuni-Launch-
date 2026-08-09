/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 */

import {
  type StudentSubject, type StudyBlock, type WeeklyTimetable, type Grade,
  type TimetableCompletions, type JCBand,
  LC_SUBJECTS, DAYS_OF_WEEK, getPointsForGrade, getGradeIndex,
  JC_BANDS,
  toDateKey,
} from './subjectData';
import type { CurriculumLevel } from '../utils/authUtils';
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
  /** Gain to the student's actual best-six CAO total if this target is reached. */
  bestSixPointsGain?: number;
  /** Number of grade boundaries between current and target (senior cycle only). */
  targetGradeSteps?: number;
  difficultyMultiplier: number;
  efficiencyMultiplier: number;
  priorityScore: number;
}

/**
 * JC-friendly priority weighting.
 *
 * Senior priority is driven by CAO-points gain; JC has no points concept.
 * Instead we weight by *band deficit*: how many descriptor bands the
 * student is below their target. Subjects more than two bands below
 * target get the highest priority, mirroring "where the most room to grow
 * is" without invoking points. Topic mastery still feeds the boost.
 *
 * Returns the same SubjectPriority shape so the downstream session
 * allocator + timetable generator work unchanged. Points-related fields
 * (currentPoints/targetPoints/pointsGain) are populated with band index
 * deltas so existing UI that references pointsGain still renders a number
 * (semantically: "bands of room to grow"). UI that displays the field as
 * a CAO-points label must be gated on curriculumLevel.
 */
export function computeSubjectPrioritiesJC(
  subjects: StudentSubject[],
  topicMastery?: TopicMasteryMap
): SubjectPriority[] {
  return subjects.map(s => {
    const currentBand: JCBand = s.currentBand ?? 'Not Graded';
    const targetBand: JCBand = s.targetBand ?? 'Distinction';
    const currentIdx = JC_BANDS.indexOf(currentBand);
    const targetIdx = JC_BANDS.indexOf(targetBand);
    // bandDeficit > 0 when below target. JC_BANDS is ordered best→worst, so
    // higher currentIdx (further from 0/Distinction) at a fixed targetIdx
    // means a larger deficit.
    const bandDeficit = Math.max(0, currentIdx - targetIdx);

    // Two-bands-below-target is the inflection point per spec — boost it.
    // 0 deficit → minimal priority, 1 → low, 2 → medium, 3+ → high.
    const deficitWeight = bandDeficit === 0 ? 0
      : bandDeficit === 1 ? 0.4
      : bandDeficit === 2 ? 0.8
      : 1.0;

    // Topic mastery boost — same shaky-ratio logic as senior.
    let topicBoost = 1.0;
    if (topicMastery && topicMastery[s.subjectName]) {
      const topics = topicMastery[s.subjectName];
      const topicEntries = Object.values(topics);
      if (topicEntries.length > 0) {
        const shakyCount = topicEntries.filter(t => t.confidence === 'shaky').length;
        const notStartedCount = topicEntries.filter(t => t.confidence === 'not-started').length;
        const shakyRatio = (shakyCount + notStartedCount * 0.5) / topicEntries.length;
        topicBoost = 1.0 + shakyRatio * 0.5; // slightly stronger boost than senior (no points signal to anchor)
      }
    }

    // Base score so even at-target subjects still get >0 — keeps maintenance
    // sessions flowing rather than zeroing out cleanly-mastered subjects.
    const baseScore = 0.2;
    const priorityScore = (baseScore + deficitWeight) * topicBoost;

    return {
      subjectName: s.subjectName,
      // The Grade-typed fields are LC-only; populate with placeholders the
      // JC UI never reads. Downstream allocator only touches priorityScore +
      // subjectName.
      currentGrade: 'H8' as Grade,
      targetGrade: 'H8' as Grade,
      isMaths: false,
      currentPoints: currentIdx,
      targetPoints: targetIdx,
      pointsGain: bandDeficit, // reinterpreted: "bands of room to grow"
      difficultyMultiplier: deficitWeight,
      efficiencyMultiplier: topicBoost,
      priorityScore,
    };
  }).sort((a, b) => b.priorityScore - a.priorityScore);
}

/**
 * Curriculum-aware dispatcher. Existing callers that pass only subjects
 * + mastery default to senior behaviour (zero regression).
 */
export function computeSubjectPrioritiesForCurriculum(
  subjects: StudentSubject[],
  topicMastery: TopicMasteryMap | undefined,
  curriculumLevel: CurriculumLevel,
  examDate?: string | null,
): SubjectPriority[] {
  return curriculumLevel === 'junior'
    ? computeSubjectPrioritiesJC(subjects, topicMastery)
    : computeSubjectPriorities(subjects, topicMastery, examDate);
}

export function computeSubjectPriorities(
  subjects: StudentSubject[],
  topicMastery?: TopicMasteryMap,
  examDate?: string | null,
): SubjectPriority[] {
  const subjectPoints = subjects.map(s => {
    const isMaths = LC_SUBJECTS.find(lc => lc.name === s.subjectName)?.isMaths || false;
    return {
      subject: s,
      isMaths,
      currentPoints: getPointsForGrade(s.currentGrade, isMaths),
      targetPoints: getPointsForGrade(s.targetGrade, isMaths),
    };
  });
  const bestSixTotal = (points: number[]) => points
    .sort((a, b) => b - a)
    .slice(0, 6)
    .reduce((sum, pointsValue) => sum + pointsValue, 0);
  const baselineBestSix = bestSixTotal(subjectPoints.map(row => row.currentPoints));

  return subjects.map(s => {
    const subjectIndex = subjects.indexOf(s);
    const { isMaths, currentPoints, targetPoints } = subjectPoints[subjectIndex];
    const pointsGain = Math.max(0, targetPoints - currentPoints);
    const projectedPoints = subjectPoints.map((row, index) => (
      index === subjectIndex ? Math.max(row.currentPoints, row.targetPoints) : row.currentPoints
    ));
    const bestSixPointsGain = Math.max(0, bestSixTotal(projectedPoints) - baselineBestSix);

    // A nearby target is more actionable than an equally valuable seven-grade
    // leap. This tempers aspiration without declaring weak subjects hopeless.
    const targetGradeSteps = Math.max(0, getGradeIndex(s.currentGrade) - getGradeIndex(s.targetGrade));
    const difficultyMultiplier = targetGradeSteps > 0 ? 1 / Math.sqrt(targetGradeSteps) : 1;

    // Syllabus efficiency: subjects with higher-efficiency topics get a small boost
    // This encourages studying subjects where effort yields more exam marks
    let efficiencyMultiplier = 1.0;
    const syllabus = getSyllabusForSubject(s.subjectName, examDate);
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

    const priorityScore = bestSixPointsGain * difficultyMultiplier * efficiencyMultiplier * topicBoost;

    return {
      subjectName: s.subjectName,
      currentGrade: s.currentGrade,
      targetGrade: s.targetGrade,
      isMaths,
      currentPoints,
      targetPoints,
      pointsGain,
      bestSixPointsGain,
      targetGradeSteps,
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

export interface WeeklyStudyTarget {
  targetMinutes: number;
  targetHours: number;
  phase: 'foundation' | 'building' | 'revision' | 'exam-prep';
  explanation: string;
}

/**
 * A deliberately conservative workload curve for focused work outside class.
 * There is no scientifically valid universal number of study hours, so this is
 * a product recommendation bounded by the realities of a secondary-school week:
 * start at roughly six focused hours, add volume gradually, and never prescribe
 * the 20–40 hour "grind" weeks common in study-content marketing.
 */
export function computeWeeklyStudyTarget(weeksUntilExam: number): WeeklyStudyTarget {
  if (weeksUntilExam <= 4) {
    return {
      targetMinutes: 720,
      targetHours: 12,
      phase: 'exam-prep',
      explanation: 'Exam preparation: more frequent retrieval and timed practice, still capped to protect sleep and recovery.',
    };
  }
  if (weeksUntilExam <= 8) {
    return {
      targetMinutes: 600,
      targetHours: 10,
      phase: 'revision',
      explanation: 'Revision phase: practice increases while sessions remain spread across the week.',
    };
  }
  if (weeksUntilExam <= 16) {
    return {
      targetMinutes: 495,
      targetHours: 8.25,
      phase: 'building',
      explanation: 'Building phase: a steady workload with room for school, sleep and recovery.',
    };
  }
  if (weeksUntilExam <= 24) {
    return {
      targetMinutes: 405,
      targetHours: 6.75,
      phase: 'building',
      explanation: 'Building phase: consistency matters more than cramming this far from the exam.',
    };
  }
  return {
    targetMinutes: 360,
    targetHours: 6,
    phase: 'foundation',
    explanation: 'Foundation phase: build a repeatable weekly habit before increasing the load.',
  };
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

// Weekend day indices: Saturday = 5, Sunday = 6 in DAYS_OF_WEEK
const WEEKEND_INDICES = new Set([5, 6]);

// Maximum ratio between the most-studied and least-studied subject.
const MAX_SESSION_RATIO = 3;

export function allocateSessions(
  priorities: SubjectPriority[],
  weeksUntilExam: number,
  sm2States?: SubjectSM2State[],
  blockDuration: number = 45,
): SessionAllocation[] {
  const target = computeWeeklyStudyTarget(weeksUntilExam);
  const safeBlockDuration = Math.max(25, Math.min(90, blockDuration));
  const totalSessions = Math.max(
    priorities.length,
    Math.round(target.targetMinutes / safeBlockDuration),
  );
  const n = priorities.length;

  if (n === 0) return [];

  const totalPriority = priorities.reduce((sum, p) => sum + p.priorityScore, 0);
  if (totalPriority === 0) {
    const base = Math.floor(totalSessions / n);
    const remainder = totalSessions % n;
    return priorities.map((p, index) => ({
      subjectName: p.subjectName,
      sessions: base + (index < remainder ? 1 : 0),
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
    // Rounding can over-allocate. Remove surplus from the lowest-priority
    // subject above its maintenance floor; never arbitrarily penalise the
    // first/highest-priority subject with the largest rounded share.
    const removable = allocations
      .map((allocation, index) => ({ ...allocation, index }))
      .filter(allocation => allocation.sessions > 1)
      .sort((a, b) => a.priorityScore - b.priorityScore || b.sessions - a.sessions);
    const candidate = removable[0];
    if (candidate) {
      allocations[candidate.index].sessions--;
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

  // Enforce the recommended weekly envelope. `allocateSessions` normally
  // already matches it; this second boundary protects callers with custom
  // allocations and weeks with very few available days.
  const maxMinutes = computeWeeklyStudyTarget(effectiveWeeks).targetMinutes;
  const maxTotalBlocks = Math.max(1, Math.floor(maxMinutes / blockDuration));
  const totalCapacity = dayCaps.reduce((s, c) => s + c, 0);
  const effectiveCapacity = Math.min(totalCapacity, maxTotalBlocks);

  // Build blocks for each subject, capped to effective capacity
  const allBlocks: { block: StudyBlock; priority: number; subjectName: string }[] = [];
  const totalRequested = allocations.reduce((s, a) => s + a.sessions, 0);

  // Fit subject counts to the actual week exactly. Simple per-subject rounding
  // could turn a 10-block capacity into 12 blocks (each subject was forced to
  // at least one), after which the placement fallback overflowed individual
  // days. Largest-remainder allocation keeps the weekly total honest.
  const fittedCounts = new Map<string, number>();
  if (totalRequested <= effectiveCapacity) {
    allocations.forEach(a => fittedCounts.set(a.subjectName, a.sessions));
  } else {
    const ranked = [...allocations].sort((a, b) => b.priorityScore - a.priorityScore);
    const canMaintainAll = effectiveCapacity >= allocations.length;
    let remaining = effectiveCapacity;
    if (canMaintainAll) {
      allocations.forEach(a => fittedCounts.set(a.subjectName, 1));
      remaining -= allocations.length;
    }
    const weightedTotal = ranked.reduce((sum, a) => sum + Math.max(0.01, a.sessions - (canMaintainAll ? 1 : 0)), 0);
    const fractions = ranked.map(a => {
      const raw = remaining * Math.max(0.01, a.sessions - (canMaintainAll ? 1 : 0)) / weightedTotal;
      const whole = Math.floor(raw);
      fittedCounts.set(a.subjectName, (fittedCounts.get(a.subjectName) ?? 0) + whole);
      return { subjectName: a.subjectName, fraction: raw - whole };
    });
    let assigned = [...fittedCounts.values()].reduce((sum, n) => sum + n, 0);
    fractions.sort((a, b) => b.fraction - a.fraction);
    for (let i = 0; assigned < effectiveCapacity; i++, assigned++) {
      const subjectName = fractions[i % fractions.length].subjectName;
      fittedCounts.set(subjectName, (fittedCounts.get(subjectName) ?? 0) + 1);
    }
  }

  for (const alloc of allocations) {
    const scaledSessions = fittedCounts.get(alloc.subjectName) ?? 0;
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

  // First decide how full each day should be. Load balance is the primary
  // constraint; spacing is optimised *inside* that balanced shape. Weekends get
  // only a slight preference, never enough to create a four-block Saturday
  // beside a one-block Thursday.
  const targetDayLoads: number[] = Array(7).fill(0);
  for (let placed = 0; placed < allBlocks.length; placed++) {
    const candidates = availableDayIndices.filter(i => targetDayLoads[i] < dayCaps[i]);
    if (candidates.length === 0) break;
    const chosen = candidates.reduce((best, i) => {
      const weekendWeight = WEEKEND_INDICES.has(i) ? 1.12 : 1;
      const score = targetDayLoads[i] / weekendWeight;
      const bestWeight = WEEKEND_INDICES.has(best) ? 1.12 : 1;
      const bestScore = targetDayLoads[best] / bestWeight;
      if (score !== bestScore) return score < bestScore ? i : best;
      // Rotate ties by week so the same weekday is not always the heavy one.
      return ((i - weekOffset + 7) % 7) < ((best - weekOffset + 7) % 7) ? i : best;
    }, candidates[0]);
    targetDayLoads[chosen]++;
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

        // Skip once this day's balanced target has been filled.
        if (dayLoads[dayIdx] >= targetDayLoads[dayIdx]) continue;

        // Score this slot: prefer days that are far from other sessions of same subject
        let minDistToSame = availableDayIndices.length; // max possible
        for (const pd of placedDays) {
          const dist = Math.min(
            Math.abs(dayIdx - pd),
            7 - Math.abs(dayIdx - pd) // wrap-around distance
          );
          minDistToSame = Math.min(minDistToSame, dist);
        }

        // Prefer: (1) avoid repeating a subject on one day, (2) maximum distance
        // from its other sessions, (3) lighter load, (4) the ideal spaced slot.
        const distFromIdeal = Math.min(search, availableDayIndices.length - search);
        const loadPenalty = dayLoads[dayIdx] * 2;
        const sameDayPenalty = placedDays.includes(dayIdx) ? 100 : 0;
        const score = minDistToSame * 10 - distFromIdeal - loadPenalty - sameDayPenalty;

        if (score > bestScore) {
          bestScore = score;
          bestDay = dayIdx;
        }
      }

      // Defensive fallback: choose a day below its hard cap. Under normal
      // operation targetDayLoads guarantees this branch is never needed.
      if (bestDay === -1) {
        const belowCap = availableDayIndices.filter(di => dayLoads[di] < dayCaps[di]);
        if (belowCap.length === 0) break;
        bestDay = belowCap.reduce((best, di) =>
          dayLoads[di] < dayLoads[best] ? di : best, belowCap[0]);
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
