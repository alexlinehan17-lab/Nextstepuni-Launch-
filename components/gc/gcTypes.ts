/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 */

import { SessionUser } from '../Auth';
import { UserProgress } from '../../types';
import { StudentSubjectProfile, TimetableCompletions, TimetableStreak } from '../subjectData';
import { NorthStar, PointsData } from '../../types';
import { GameState } from '../journeySimulatorData';
import { DebriefEntry } from '../StudyDebrief';

// ─── Firestore document shapes (read-only from GC perspective) ──────────────

/** Journey result stored at progress/{uid}['journey-simulator'] */
export interface JourneyResult {
  endingId: string;          // maps to ARCHETYPES key
  finalStats: GameState;
  completedAt?: string;
  decisionsCount?: number;
}

// ─── Aggregated student data loaded once in GCDashboard shell ───────────────

/** Mock result from War Room */
export interface MockResultEntry {
  id: string;
  subject: string;
  grade: string;
  date: string;
  label?: string;
  timestamp: number;
}

export interface GCStudentFullData {
  user: SessionUser;
  progress: UserProgress;
  subjectProfile: StudentSubjectProfile | null;
  northStar: NorthStar | null;
  journeyResult: JourneyResult | null;
  streak: TimetableStreak | null;
  points: PointsData | null;
  timetableCompletions: TimetableCompletions | null;
  futureFinder: { topPicks: string[]; completedAt: string } | null;
  mockResults: MockResultEntry[] | null;
  recentDebriefs: DebriefEntry[] | null;
}

// ─── Status types ───────────────────────────────────────────────────────────

export type StudentStatus = 'new' | 'at-risk' | 'drifting' | 'thriving' | 'active' | 'inactive';

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
