/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 */

import { type SessionUser, type CurriculumLevel } from '../../utils/authUtils';
import { type UserProgress } from '../../types';
import { type StudentSubjectProfile, type TimetableCompletions, type TimetableStreak, type YearGroup } from '../subjectData';
import { type NorthStar, type PointsData, type CollegeCompassState } from '../../types';
import { type GameState } from '../journeySimulatorData';
import { type DebriefEntry } from '../StudyDebrief';

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
  /** Course picks, unified across both Future Finder namespaces.
   *  `source` tells the render layer what it is looking at:
   *   - 'saved'  — the student's explicit bookmarks from the live tool
   *                (save-order, NOT a ranking — don't print 1/2/3 badges)
   *   - 'ranked' — the live tool's algorithmic top matches (a real ranking)
   *   - 'legacy' — the retired Future Finder's list (may be stale) */
  futureFinder: { topPicks: string[]; completedAt: string; source: 'saved' | 'ranked' | 'legacy' } | null;
  mockResults: MockResultEntry[] | null;
  recentDebriefs: DebriefEntry[] | null;
  /** College Compass checklist completions — the student's marks, read-only on the GC side. */
  collegeCompass: CollegeCompassState | null;
  /** First-class year-group + curriculum-level for fast filtering at the
   *  cohort level. Both derive from the user doc (yearGroup) with
   *  subjectProfile.yearGroup as a fallback. Surfaced in Phase 1 so Phase 6
   *  can add the dashboard filters without changing the loader. */
  yearGroup?: YearGroup;
  curriculumLevel?: CurriculumLevel;
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
