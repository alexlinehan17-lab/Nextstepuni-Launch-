/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 */

import { SessionUser } from '../Auth';
import { UserProgress } from '../../types';
import { StudentSubjectProfile, TimetableCompletions, TimetableStreak } from '../subjectData';
import { NorthStar, PointsData } from '../../types';
import { GameState } from '../journeySimulatorData';

// ─── Firestore document shapes (read-only from GC perspective) ──────────────

/** Mood entries are stored as an array in moods/{uid}.entries */
export interface MoodEntry {
  date: string;    // "YYYY-MM-DD"
  mood: string;    // 'calm' | 'balanced' | 'energized' | 'stressed'
  timestamp: number;
}

export interface MoodDoc {
  entries?: MoodEntry[];
}

/** Journey result stored at progress/{uid}['journey-simulator'] */
export interface JourneyResult {
  endingId: string;          // maps to ARCHETYPES key
  finalStats: GameState;
  completedAt?: string;
  decisionsCount?: number;
}

// ─── Aggregated student data loaded once in GCDashboard shell ───────────────

export interface GCStudentFullData {
  user: SessionUser;
  progress: UserProgress;
  subjectProfile: StudentSubjectProfile | null;
  northStar: NorthStar | null;
  journeyResult: JourneyResult | null;
  mood: MoodDoc | null;
  streak: TimetableStreak | null;
  points: PointsData | null;
  timetableCompletions: TimetableCompletions | null;
}

// ─── Status types ───────────────────────────────────────────────────────────

export type StudentStatus = 'on-track' | 'needs-support' | 'new';

// ─── Mood Trend ─────────────────────────────────────────────────────────────

export type MoodTrend = 'improving' | 'declining' | 'stable' | 'insufficient-data';

// ─── Subject Gap Analysis ───────────────────────────────────────────────────

export interface SubjectGapData {
  subjectName: string;
  studentCount: number;
  avgGap: number;
  maxGap: number;
}

// ─── GC Notes ───────────────────────────────────────────────────────────────

export interface GCNote {
  notes: string;
  updatedAt: string;
}
