/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 */
import React, { useState, useMemo, useRef, useEffect } from 'react';
import { TrendingUp, TrendingDown, ChevronRight, Flame, Flag, ArrowUp, ArrowDown, CircleHelp, MoreHorizontal } from 'lucide-react';
import { type CourseData } from '../Library';
import { type CategoryType } from '../KnowledgeTree';
import { type CurriculumLevel } from '../../utils/authUtils';
import { type YearGroup } from '../subjectData';
import { getSchoolName } from '../../schoolData';
import { doc, getDoc } from 'firebase/firestore';
import { db } from '../../firebase';
import { type SchoolEvent, GCCalendar, getLCExamDate } from './GCKeyEvents';
import { type GCStudentFullData, type StudentStatus } from './gcTypes';
import {
  getOverallProgress,
  getCategoryProgress,
  getStudentStatus,
  getStudentCurrentCAO,
  getStudentTargetCAO,
  getStudentSubjectsCovered,
  getStudentTopBandsCount,
  getStudentTargetTopBandsCount,
  getDaysUntilLC,
  isActiveThisWeek,
  getProgressDistribution,
  getSubjectGaps,
  generateStudentCSV,
  getRecentlyActiveStudents,
  getVisibleCourses,
  hasCAOGrades,
} from './gcUtils';
import { type EarlyWarningAlert } from './gcAlerts';
import { GCKeyEvents } from './GCKeyEvents';
import { SubjectHealthPanel } from './SubjectHealthPanel';
import GCExportModal from './GCExportModal';
import { type FlagData, type FlagPriority } from '../../hooks/useGCFlags';
import { logError } from '../../utils/logError';
import { getFunctions, httpsCallable } from 'firebase/functions';
import app from '../../firebase';
import { STAFF_BROADCASTS } from '../../data/staffEncouragement';
import SubjectAvatar from '../SubjectAvatar';
import { Button, TextButton } from '../ui/Button';
import { ChoiceTile, SelectionBar } from '../ui/Choice';
import { Menu, MenuAction, MenuPanel, MenuRadioRows, MenuRule } from '../ui/Menu';
import { Sheet } from '../ui/Sheet';
import { SearchField } from '../ui/Field';
import { List, Row } from '../ui/List';
import { useWide, STATUS_WORDS, StatusDot, StatusWords, SeverityDot, SEVERITY_WORDS, Fig, Pct, StudentArt, daysWords, daysSinceBlock } from './gcView';

// ─── Categories ─────────────────────────────────────────────────────────────

const CATEGORIES: { id: CategoryType; title: string; color: string; dotColor: string }[] = [
  { id: 'architecture-mindset', title: 'Architecture of Mindset', color: 'bg-blue-500', dotColor: 'bg-blue-500' },
  { id: 'science-growth', title: 'Science of Growth', color: 'bg-amber-500', dotColor: 'bg-amber-500' },
  { id: 'learning-cheat-codes', title: 'Learning Effectively', color: 'bg-teal-500', dotColor: 'bg-teal-500' },
  { id: 'subject-specific-science', title: 'Decoding Subjects', color: 'bg-slate-500', dotColor: 'bg-slate-500' },
  { id: 'exam-zone', title: 'Exam Strategy', color: 'bg-red-500', dotColor: 'bg-red-500' },
];

// ─── Sort / Filter ──────────────────────────────────────────────────────────

type SortKey = 'name' | 'progress' | 'cao-current' | 'cao-target' | 'gap' | 'streak';
type SortDir = 'asc' | 'desc';
type StatusFilter = 'all' | 'flagged' | 'needs-attention' | StudentStatus;
type CurriculumFilter = 'all' | 'junior' | 'senior';
type YearGroupFilter = 'all' | YearGroup;

// Canonical year-group order (Phase 6). Used to sort the dynamic
// year-group filter options so 1st-year shows before 6th-year regardless
// of the order they happen to appear in the cohort.
const YEAR_GROUP_ORDER: readonly YearGroup[] = ['1st', '2nd', '3rd', 'TY', '5th', '6th'];

function yearGroupSortOrder(a: YearGroup, b: YearGroup): number {
  return YEAR_GROUP_ORDER.indexOf(a) - YEAR_GROUP_ORDER.indexOf(b);
}

// Junior vs senior split (Phase 1 derivation). Phase 6 uses this client-side
// only — server-side curriculumLevel is already on the user doc.
function isJuniorYear(yg: YearGroup | undefined): boolean {
  return yg === '1st' || yg === '2nd' || yg === '3rd';
}

// ─── The nine status filters and the status guide (today's words, sentence case) ──

const STATUS_FILTERS: { key: StatusFilter; label: string }[] = [
  { key: 'all', label: 'All' },
  { key: 'needs-attention', label: 'Needs attention' },
  { key: 'thriving', label: 'Thriving' },
  { key: 'active', label: 'Active' },
  { key: 'new', label: 'New' },
  { key: 'drifting', label: 'Drifting' },
  { key: 'at-risk', label: 'At risk' },
  { key: 'inactive', label: 'Inactive' },
  { key: 'flagged', label: 'Flagged' },
];

/** Every status getStudentStatus can produce, in the guide's order, with today's explanation. */
export const STATUS_GUIDE: { status: StudentStatus; desc: string }[] = [
  { status: 'new', desc: 'Signed up within the last 7 days. Give them time to explore.' },
  { status: 'active', desc: 'Logged a study session in the past 7 days. On track.' },
  { status: 'thriving', desc: 'Active with a 5+ day streak, 3+ modules completed, or 3+ consecutive active weeks.' },
  { status: 'drifting', desc: '8\u201314 days since last session, or lost a strong streak recently. May need a nudge.' },
  { status: 'at-risk', desc: '15+ days inactive, lost a 7+ day streak, or 3+ weeks with zero sessions. Needs attention.' },
  { status: 'inactive', desc: 'Past the 7-day new window but has never logged a single study session.' },
];

/** Which students a status filter keeps: the table's filter, and the count the phone's filter sheet
 *  shows on its button before it is applied (one rule, so the two can never disagree). */
function statusMatch(s: { status: StudentStatus; student: GCStudentFullData }, filter: StatusFilter, flags?: GCFlagsAPI): boolean {
  if (filter === 'flagged') return !!flags?.isFlagged(s.student.user.uid);
  if (filter === 'needs-attention') return s.status === 'drifting' || s.status === 'at-risk' || !!flags?.isFlagged(s.student.user.uid);
  if (filter !== 'all') return s.status === filter;
  return true;
}


// ─── Component ──────────────────────────────────────────────────────────────

interface GCFlagsAPI {
  flags: Record<string, FlagData>;
  flagStudent: (uid: string, priority?: FlagPriority) => Promise<void>;
  unflagStudent: (uid: string) => Promise<void>;
  updateFlagPriority: (uid: string, priority: FlagPriority) => Promise<void>;
  isFlagged: (uid: string) => boolean;
  getFlagData: (uid: string) => FlagData | null;
  flaggedStudentUids: string[];
}

interface GCOverviewProps {
  studentData: GCStudentFullData[];
  allCourses: CourseData[];
  school: string;
  onSelectStudent: (uid: string) => void;
  onDeleteStudent?: (user: any) => void;
  onResetPassword?: (studentUid: string) => void;
  alerts?: EarlyWarningAlert[];
  onDismissAlert?: (alert: EarlyWarningAlert) => void;
  gcFlags?: GCFlagsAPI;
  /** On a phone the Overview and the Students list are two places of the bottom bar (area 8a). */
  place?: 'overview' | 'students';
  /** "See all N students" on a phone's Overview opens the Students place. */
  onOpenStudents?: () => void;
  /** When the snapshot was taken ("14:37"), said on a phone under the greeting. */
  dataAsOf?: string | null;
  /** A notice about the snapshot (the 1000-account cap), said under the greeting on a phone. */
  notice?: string | null;
}

export const GCOverview: React.FC<GCOverviewProps> = ({ studentData, allCourses, school, onSelectStudent, onDeleteStudent, onResetPassword, alerts = [], onDismissAlert, gcFlags, place = 'overview', onOpenStudents, dataAsOf, notice }) => {
  const [searchQuery, setSearchQuery] = useState('');
  const [showStatusGuide, setShowStatusGuide] = useState(false);
  const [showBroadcastModal, setShowBroadcastModal] = useState(false);
  // Broadcast audience scope (Phase 6 follow-up). Independent of the
  // dashboard's cohort filter so a GC can broadcast to "JC + TY" or
  // "5th + 6th" without disturbing what they're viewing on the dashboard.
  //   - broadcastCurriculum scopes which years can be picked
  //   - broadcastYearGroups is a Set; an EMPTY set means "all years in
  //     the active curriculum scope" (so the default broadcast hits
  //     everyone). Toggling a chip narrows the audience.
  const [broadcastCurriculum, setBroadcastCurriculum] = useState<CurriculumFilter>('all');
  const [broadcastYearGroups, setBroadcastYearGroups] = useState<Set<YearGroup>>(new Set());
  const [showExportModal, setShowExportModal] = useState(false);
  // Preset id, never prose — staff cannot type free text to students.
  const [broadcastMessageId, setBroadcastMessageId] = useState('');
  const [isBroadcasting, setIsBroadcasting] = useState(false);
  const [statusFilter, setStatusFilter] = useState<StatusFilter>('all');
  // Cohort filters (Phase 6 JC support). curriculumFilter is the primary
  // (broader) filter; yearGroupFilter is the secondary narrower filter.
  // Changing curriculumFilter resets yearGroupFilter to 'all' to avoid
  // stale combinations (e.g. junior + 6th).
  const [curriculumFilter, setCurriculumFilter] = useState<CurriculumFilter>('all');
  const [yearGroupFilter, setYearGroupFilter] = useState<YearGroupFilter>('all');
  const handleCurriculumChange = (next: CurriculumFilter) => {
    setCurriculumFilter(next);
    setYearGroupFilter('all');
  };
  const [sortKey, setSortKey] = useState<SortKey>('name');
  const [sortDir, setSortDir] = useState<SortDir>('asc');
  // Area 8a: the phone's sheets and lists (how things are shown; nothing here is read or written).
  const wide = useWide();
  const twoMonths = useWide(1200);
  const [allList, setAllList] = useState<null | 'warnings' | 'attention' | 'recent' | 'gaps'>(null);
  const [filterOpen, setFilterOpen] = useState(false);
  const [draftStatus, setDraftStatus] = useState<StatusFilter>('all');
  const [draftSortKey, setDraftSortKey] = useState<SortKey>('name');
  const [draftSortDir, setDraftSortDir] = useState<SortDir>('asc');
  const broadcastMessagesRef = useRef<HTMLDivElement>(null);

  // ─── Computed stats ─────────────────────────────────────────────────────

  // A student's curriculum, with a definite answer for everyone.
  //
  // The four places that derived this used to leave it `undefined` when the
  // user doc had neither field, and `undefined` matches NEITHER the 'junior'
  // nor the 'senior' filter — so those students disappeared from the table
  // under every setting except "All". That set is exactly the students who
  // haven't signed in since the curriculumLevel backfill shipped: the
  // disengaged ones a counsellor is looking for. Defaulting to 'senior'
  // matches what the backfill itself does, and can only ever ADD a row.
  const levelOf = (s: GCStudentFullData): CurriculumLevel =>
    s.curriculumLevel ?? (s.yearGroup ? (isJuniorYear(s.yearGroup) ? 'junior' : 'senior') : 'senior');

  const studentStats = useMemo(() => {
    return studentData.map(s => {
      // Score each student against the modules THEY can open — dividing by the
      // whole catalogue understated every student's progress (a completed
      // 7-subject senior read ~73%, a JC student ~20%).
      const visible = getVisibleCourses(s, allCourses);
      return {
        student: s,
        progress: getOverallProgress(s.progress, visible),
        status: getStudentStatus(s, visible),
        isJunior: levelOf(s) === 'junior',
        // Whether a CAO total means anything for this student at all. JC uses
        // bands and LCA uses credits — neither has an H/O grade, so their CAO
        // is not 0, it doesn't exist.
        hasGrades: hasCAOGrades(s),
        currentCAO: getStudentCurrentCAO(s),
        targetCAO: getStudentTargetCAO(s),
        // JC metrics — non-zero only when the student has currentBand/targetBand
        subjectsCovered: getStudentSubjectsCovered(s),
        topBandsCount: getStudentTopBandsCount(s),
        targetTopBandsCount: getStudentTargetTopBandsCount(s),
        streak: s.streak?.currentStreak ?? 0,
        activeThisWeek: isActiveThisWeek(s),
      };
    });
  }, [studentData, allCourses]);

  // ─── Cohort breakdown (Phase 6) ─────────────────────────────────────────

  // Counts for the summary header. Curriculum is the server-set value when
  // present; otherwise we derive client-side from yearGroup.
  const cohortCurriculumCounts = useMemo(() => {
    let junior = 0;
    let senior = 0;
    let unknown = 0;
    for (const s of studentData) {
      const lvl: CurriculumLevel | undefined =
        s.curriculumLevel ?? (s.yearGroup ? (isJuniorYear(s.yearGroup) ? 'junior' : 'senior') : undefined);
      if (lvl === 'junior') junior++;
      else if (lvl === 'senior') senior++;
      else unknown++;
    }
    return { junior, senior, unknown, total: studentData.length };
  }, [studentData]);

  // Dynamic year-group dropdown: only show year groups actually present in
  // the cohort, scoped by the active curriculum filter so junior+6th
  // can never be selectable.
  const availableYearGroups = useMemo(() => {
    const groups = new Set<YearGroup>();
    for (const s of studentData) {
      const lvl: CurriculumLevel | undefined =
        s.curriculumLevel ?? (s.yearGroup ? (isJuniorYear(s.yearGroup) ? 'junior' : 'senior') : undefined);
      if (curriculumFilter !== 'all' && lvl !== curriculumFilter) continue;
      if (s.yearGroup) groups.add(s.yearGroup);
    }
    return Array.from(groups).sort(yearGroupSortOrder);
  }, [studentData, curriculumFilter]);

  // ─── Cohort scope ───────────────────────────────────────────────────────
  //
  // ONE scoped array that every headline number derives from. Previously the
  // table rows were cohort-filtered but the status pills, stat cards, the
  // Attention list, the activity charts and the exports were not — so a GC who
  // filtered to "Junior Cycle · 2nd Year" read school-wide totals under a
  // cohort-scoped heading, and exported the entire school.
  const cohortScopedStats = useMemo(() => {
    return studentStats.filter(s => {
      if (curriculumFilter !== 'all' && levelOf(s.student) !== curriculumFilter) return false;
      if (yearGroupFilter !== 'all' && s.student.yearGroup !== yearGroupFilter) return false;
      return true;
    });
  }, [studentStats, curriculumFilter, yearGroupFilter]);

  const avgProgress = cohortScopedStats.length > 0
    ? cohortScopedStats.reduce((sum, s) => sum + s.progress, 0) / cohortScopedStats.length
    : 0;

  const driftingCount = cohortScopedStats.filter(s => s.status === 'drifting').length;
  const atRiskCount = cohortScopedStats.filter(s => s.status === 'at-risk').length;
  const flaggedCount = gcFlags?.flaggedStudentUids.length ?? 0;

  // Deduplicated attention set: drifting + at-risk + flagged
  const attentionStudents = useMemo(() => {
    const seen = new Set<string>();
    const list: { student: GCStudentFullData; status: StudentStatus; flag: FlagData | null; daysSince: number }[] = [];

    const addStudent = (s: typeof studentStats[0]) => {
      const uid = s.student.user.uid;
      if (seen.has(uid)) return;
      seen.add(uid);
      const flag = gcFlags?.getFlagData(uid) ?? null;
      // Compute days since last session
      let daysSince = Infinity;
      if (s.student.timetableCompletions) {
        const now = Date.now();
        for (const [date, blocks] of Object.entries(s.student.timetableCompletions)) {
          if (Array.isArray(blocks) && blocks.length > 0) {
            const d = new Date(date + 'T00:00:00').getTime();
            const diff = Math.floor((now - d) / 86400000);
            if (diff < daysSince) daysSince = diff;
          }
        }
      }
      list.push({ student: s.student, status: s.status, flag, daysSince });
    };

    // At Risk and Drifting
    cohortScopedStats.filter(s => s.status === 'at-risk' || s.status === 'drifting').forEach(addStudent);
    // Flagged (may overlap)
    if (gcFlags) {
      gcFlags.flaggedStudentUids.forEach(uid => {
        const s = cohortScopedStats.find(ss => ss.student.user.uid === uid);
        if (s) addStudent(s);
      });
    }

    // Sort: high-priority flagged → at-risk → drifting → normal-priority flagged
    list.sort((a, b) => {
      const aHighFlag = a.flag?.priority === 'high' ? 1 : 0;
      const bHighFlag = b.flag?.priority === 'high' ? 1 : 0;
      if (aHighFlag !== bHighFlag) return bHighFlag - aHighFlag;
      const statusOrder: Record<string, number> = { 'at-risk': 0, 'drifting': 1 };
      const aOrder = statusOrder[a.status] ?? 2;
      const bOrder = statusOrder[b.status] ?? 2;
      if (aOrder !== bOrder) return aOrder - bOrder;
      const aNormalFlag = a.flag && a.flag.priority === 'normal' ? 1 : 0;
      const bNormalFlag = b.flag && b.flag.priority === 'normal' ? 1 : 0;
      if (aNormalFlag !== bNormalFlag) return bNormalFlag - aNormalFlag;
      return 0;
    });

    return list;
  }, [cohortScopedStats, gcFlags]);

  const needsAttentionCount = attentionStudents.length;
  // Count only-flagged students (flagged but NOT at-risk/drifting)
  const flaggedOnlyCount = attentionStudents.filter(s => s.flag && s.status !== 'at-risk' && s.status !== 'drifting').length;

  const _avgCurrentCAO = cohortScopedStats.length > 0
    ? Math.round(cohortScopedStats.filter(s => s.hasGrades).reduce((sum, s) => sum + s.currentCAO, 0) / Math.max(1, cohortScopedStats.filter(s => s.hasGrades).length))
    : 0;

  const _activeThisWeekCount = cohortScopedStats.filter(s => s.activeThisWeek).length;

  // Status counts for filter pills
  const statusCounts = useMemo(() => {
    const counts: Record<string, number> = { all: cohortScopedStats.length };
    cohortScopedStats.forEach(s => { counts[s.status] = (counts[s.status] ?? 0) + 1; });
    counts['flagged'] = flaggedCount;
    counts['needs-attention'] = needsAttentionCount;
    return counts;
  }, [cohortScopedStats, flaggedCount, needsAttentionCount]);
  const daysUntilLC = getDaysUntilLC();

  // Cohort-scoped student list — drives Progress Breakdown + Subject-Level
  // Gaps + SubjectHealthPanel. Respects the active curriculum + year-group
  // filters so a GC filtering to "Junior Cycle / 3rd Year" sees panel
  // breakdowns scoped to that slice.
  const cohortScopedStudents = useMemo(() => {
    return studentData.filter(s => {
      if (curriculumFilter !== 'all' && levelOf(s) !== curriculumFilter) return false;
      if (yearGroupFilter !== 'all' && s.yearGroup !== yearGroupFilter) return false;
      return true;
    });
  }, [studentData, curriculumFilter, yearGroupFilter]);

  // Column headings for the three attainment columns, matched to whoever is
  // actually in the current cohort. In a mixed school they stay generic and
  // the tooltip explains the two scales.
  const attainmentHeadings = useMemo(() => {
    const hasJunior = cohortScopedStats.some(s => s.isJunior);
    const hasSenior = cohortScopedStats.some(s => !s.isJunior);
    if (hasJunior && !hasSenior) {
      return { current: 'At Merit+', target: 'Target Merit+', gap: 'To Gain', hint: 'Subjects at Merit or above, out of subjects taken' };
    }
    if (hasSenior && !hasJunior) {
      return { current: 'CAO Current', target: 'CAO Target', gap: 'Gap', hint: 'Best-six CAO points from current and target grades' };
    }
    return { current: 'Current', target: 'Target', gap: 'Gap', hint: 'CAO points for Senior Cycle students; subjects at Merit or above for Junior Cycle' };
  }, [cohortScopedStats]);

  const distribution = getProgressDistribution(cohortScopedStudents, allCourses);
  // NOT clamped to 1 — this is a population count shown as "N students", and
  // the clamp printed "1 students" for a cohort filter that matched nobody.
  // (distributionMax below stays clamped: it is used as a divisor.)
  const distributionTotal = distribution.reduce((a, b) => a + b, 0);
  const distributionMax = Math.max(1, ...distribution);

  // Human-readable label for the active cohort filter — used in panel
  // headings so the GC can see what scope they're looking at without
  // jumping back to the filter bar.
  const cohortScopeLabel = useMemo(() => {
    const parts: string[] = [];
    if (curriculumFilter === 'junior') parts.push('Junior Cycle');
    else if (curriculumFilter === 'senior') parts.push('Senior Cycle');
    if (yearGroupFilter !== 'all') parts.push(yearGroupFilter === 'TY' ? 'TY' : `${yearGroupFilter} Year`);
    return parts.join(' · ');
  }, [curriculumFilter, yearGroupFilter]);

  // ─── Category averages ─────────────────────────────────────────────────

  const _categoryAverages = useMemo(() => {
    return CATEGORIES.map(cat => {
      const avgProg = studentData.length > 0
        ? studentData.reduce((sum, s) => sum + getCategoryProgress(s.progress, allCourses, cat.id), 0) / studentData.length
        : 0;
      const zeroCount = studentData.filter(s => {
        const catCourses = allCourses.filter(c => c.category === cat.id);
        return catCourses.every(course => {
          const p = s.progress[course.id];
          return !p || p.unlockedSection === 0;
        });
      }).length;
      return { ...cat, avgProgress: avgProg, zeroStudents: zeroCount };
    });
  }, [studentData, allCourses]);

  // ─── New widgets data ──────────────────────────────────────────────────

  // Cohort-scoped, like every other panel — a GC filtered to 2nd Year should
  // not see 6th years in "Recently active".
  const recentlyActive = useMemo(() => getRecentlyActiveStudents(cohortScopedStudents), [cohortScopedStudents]);

  // ─── Activity range toggle ────────────────────────────────────────────

  const [activityRange, setActivityRange] = useState<'7d' | '30d'>('7d');

  // ─── Aggregated daily activity across ALL students (30 days) ──────────

  const aggregatedActivity = useMemo(() => {
    const counts: Record<string, number> = {};
    const now = new Date();
    for (let i = 29; i >= 0; i--) {
      const d = new Date(now);
      d.setDate(d.getDate() - i);
      const key = `${d.getFullYear()}-${String(d.getMonth() + 1).padStart(2, '0')}-${String(d.getDate()).padStart(2, '0')}`;
      counts[key] = 0;
    }
    cohortScopedStudents.forEach(s => {
      if (!s.timetableCompletions) return;
      Object.entries(s.timetableCompletions).forEach(([date, blocks]) => {
        if (date in counts && Array.isArray(blocks)) {
          counts[date] += blocks.length;
        }
      });
    });
    const all = Object.entries(counts)
      .sort(([a], [b]) => a.localeCompare(b))
      .map(([date, count]) => ({ date, count }));
    return activityRange === '7d' ? all.slice(-7) : all;
  }, [cohortScopedStudents, activityRange]);

  // ─── Weekly trends (week-over-week comparison) ────────────────────────

  const weeklyTrends = useMemo(() => {
    const now = new Date();
    const dayOfWeek = now.getDay();
    const mondayOffset = dayOfWeek === 0 ? 6 : dayOfWeek - 1;
    const thisMonday = new Date(now);
    thisMonday.setDate(now.getDate() - mondayOffset);
    thisMonday.setHours(0, 0, 0, 0);
    const lastMonday = new Date(thisMonday);
    lastMonday.setDate(thisMonday.getDate() - 7);

    const _fmt = (d: Date) => `${d.getFullYear()}-${String(d.getMonth() + 1).padStart(2, '0')}-${String(d.getDate()).padStart(2, '0')}`;

    let blocksThisWeek = 0;
    let blocksLastWeek = 0;
    const activeThisWeekSet = new Set<string>();
    const activeLastWeekSet = new Set<string>();

    cohortScopedStudents.forEach(s => {
      if (!s.timetableCompletions) return;
      Object.entries(s.timetableCompletions).forEach(([date, blocks]) => {
        if (!Array.isArray(blocks)) return;
        const d = new Date(date + 'T00:00:00');
        if (d >= thisMonday && d <= now) {
          blocksThisWeek += blocks.length;
          if (blocks.length > 0) activeThisWeekSet.add(s.user.uid);
        } else if (d >= lastMonday && d < thisMonday) {
          blocksLastWeek += blocks.length;
          if (blocks.length > 0) activeLastWeekSet.add(s.user.uid);
        }
      });
    });

    const blocksTrend = blocksLastWeek > 0
      ? Math.round(((blocksThisWeek - blocksLastWeek) / blocksLastWeek) * 100)
      : blocksThisWeek > 0 ? 100 : 0;

    return { blocksThisWeek, blocksLastWeek, blocksTrend };
    // Must match the array the body actually reads. Leaving this as
    // [studentData] froze "Blocks This Week" at the school-wide total under
    // every cohort filter — and made it order-dependent, since the next
    // setStudentData (a tray open, or Refresh) would recompute it against
    // whatever the filter happened to be at that moment.
  }, [cohortScopedStudents]);

  // ─── Filter + Sort ──────────────────────────────────────────────────────

  const filtered = useMemo(() => {
    // Starts from the cohort-scoped array so the table and the headline
    // numbers above it are guaranteed to describe the same population.
    let result = cohortScopedStats;
    if (searchQuery) {
      const q = searchQuery.toLowerCase();
      result = result.filter(s => s.student.user.name.toLowerCase().includes(q));
    }
    result = result.filter(s => statusMatch(s, statusFilter, gcFlags));
    // Copy before sorting — Array.prototype.sort mutates in place, and when no
    // filter is active `result` IS the memoised array, so this was quietly
    // reordering shared state that other panels read.
    result = [...result].sort((a, b) => {
      // Flagged students always pinned to top
      const aFlag = gcFlags?.getFlagData(a.student.user.uid);
      const bFlag = gcFlags?.getFlagData(b.student.user.uid);
      const aFlagged = !!aFlag;
      const bFlagged = !!bFlag;
      if (aFlagged !== bFlagged) return aFlagged ? -1 : 1;
      if (aFlagged && bFlagged) {
        // High priority first
        if (aFlag!.priority !== bFlag!.priority) return aFlag!.priority === 'high' ? -1 : 1;
        // Then most recently flagged first
        return bFlag!.flaggedAt - aFlag!.flaggedAt;
      }
      // Normal column sort for non-flagged
      let cmp = 0;
      switch (sortKey) {
        case 'name': cmp = a.student.user.name.localeCompare(b.student.user.name); break;
        case 'progress': cmp = a.progress - b.progress; break;
        // In a mixed cohort these columns hold CAO points for senior rows and
        // Merit+ counts for JC rows, so compare each row on its own metric
        // rather than reading a JC student's absent CAO as 0.
        case 'cao-current': cmp = (a.isJunior ? a.topBandsCount : a.currentCAO) - (b.isJunior ? b.topBandsCount : b.currentCAO); break;
        case 'cao-target': cmp = (a.isJunior ? a.targetTopBandsCount : a.targetCAO) - (b.isJunior ? b.targetTopBandsCount : b.targetCAO); break;
        case 'gap': cmp = (a.isJunior ? a.targetTopBandsCount - a.topBandsCount : a.targetCAO - a.currentCAO) - (b.isJunior ? b.targetTopBandsCount - b.topBandsCount : b.targetCAO - b.currentCAO); break;
        case 'streak': cmp = a.streak - b.streak; break;
      }
      return sortDir === 'desc' ? -cmp : cmp;
    });
    return result;
  }, [cohortScopedStats, searchQuery, statusFilter, sortKey, sortDir, gcFlags]);

  const handleSort = (key: SortKey) => {
    if (sortKey === key) {
      setSortDir(d => d === 'asc' ? 'desc' : 'asc');
    } else {
      setSortKey(key);
      setSortDir(key === 'name' ? 'asc' : 'desc');
    }
  };

  // ─── Subject Gaps ──────────────────────────────────────────────────────

  // Uses cohortScopedStudents so the gaps panel narrows when the GC picks
  // a curriculum + year. For senior-LC students the existing CAO-points
  // gap math applies; for JC students the same helper returns no gaps
  // (no currentGrade), so a JC-filtered view will show an empty gaps
  // panel rather than misleading senior numbers.
  const subjectGaps = useMemo(() => getSubjectGaps(cohortScopedStudents), [cohortScopedStudents]);
  const topGaps = subjectGaps.slice(0, 8);
  const maxAvgGap = topGaps.length > 0 ? Math.max(...topGaps.map(g => g.avgGap)) : 1;

  // ─── CSV Export ────────────────────────────────────────────────────────

  const handleExportCSV = () => {
    // Exports follow the on-screen filter — a GC who narrows to "Junior Cycle
    // · 2nd Year" and hits Export used to download the whole school.
    const csv = generateStudentCSV(cohortScopedStudents, allCourses);
    const blob = new Blob([csv], { type: 'text/csv;charset=utf-8;' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    const date = new Date().toISOString().slice(0, 10);
    a.href = url;
    a.download = `gc-students-${date}.csv`;
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    URL.revokeObjectURL(url);
  };

  // ─── Load school events for calendar ─────────────────────────────────────
  const [schoolEvents, setSchoolEvents] = useState<SchoolEvent[]>([]);
  useEffect(() => {
    let cancelled = false;
    getDoc(doc(db, 'gcEvents', school)).then(snap => {
      if (cancelled) return;
      if (snap.exists()) {
        setSchoolEvents((snap.data().events as SchoolEvent[]) || []);
      }
    }).catch((e) => logError('GCOverview.loadSchoolEvents', e));
    return () => { cancelled = true; };
  }, [school]);

  // ─── Render ─────────────────────────────────────────────────────────────

  const lcDateWords = getLCExamDate().toLocaleDateString('en-IE', { weekday: 'long', day: 'numeric', month: 'long', year: 'numeric' }).replace(/,/g, '');

  const hour = new Date().getHours();
  const greeting = hour < 12 ? 'Good morning.' : hour < 18 ? 'Good afternoon.' : 'Good evening.';

  const urgentCount = alerts.filter(a => a.severity === 'urgent').length;
  const watchCount = alerts.filter(a => a.severity === 'watch').length;
  const nudgeCount = alerts.filter(a => a.severity === 'nudge').length;
  const alertCounts = [
    urgentCount > 0 && `${urgentCount} urgent`,
    watchCount > 0 && `${watchCount} ${wide ? 'to watch' : 'watch'}`,
    nudgeCount > 0 && `${nudgeCount} nudge`,
  ].filter(Boolean).join(' · ');
  const attentionParts = [
    driftingCount > 0 && `${driftingCount} drifting`,
    atRiskCount > 0 && `${atRiskCount} at risk`,
    flaggedOnlyCount > 0 && `${flaggedOnlyCount} flagged`,
  ].filter(Boolean);
  const attentionMeta = wide ? `${needsAttentionCount} · ${attentionParts.join(', ')}` : attentionParts.join(' · ');
  const firstFew = wide ? 6 : 3;
  const trend = weeklyTrends.blocksTrend;
  const trendWords = trend < 0 ? `${Math.abs(trend)}% fewer than last week` : trend > 0 ? `${trend}% more than last week` : `${trend}% vs last week`;
  const TrendGlyph = trend >= 0 ? TrendingUp : TrendingDown;
  const countLine = `${filtered.length === cohortCurriculumCounts.total
    ? `${cohortCurriculumCounts.total} students`
    : `${filtered.length} of ${cohortCurriculumCounts.total}`}${cohortCurriculumCounts.junior > 0 && cohortCurriculumCounts.senior > 0 && curriculumFilter === 'all'
    ? ` · ${cohortCurriculumCounts.junior} Junior Cycle · ${cohortCurriculumCounts.senior} Senior Cycle`
    : ''}`;
  const yearOptions: readonly YearGroup[] =
    curriculumFilter === 'junior' ? ['1st', '2nd', '3rd'] as const
    : curriculumFilter === 'senior' ? ['TY', '5th', '6th'] as const
    : ['1st', '2nd', '3rd', 'TY', '5th', '6th'] as const;
  const yearWords = (yg: YearGroup) => (yg === 'TY' ? 'TY' : `${yg} Year`);

  const cohortMenus = (
    <>
      <Menu
        label="Students shown"
        value={curriculumFilter}
        onChange={handleCurriculumChange}
        options={[{ value: 'all', label: 'All students' }, { value: 'junior', label: 'Junior Cycle' }, { value: 'senior', label: 'Senior Cycle' }]}
      />
      <Menu
        label="Year"
        value={yearGroupFilter}
        onChange={value => setYearGroupFilter(value as YearGroupFilter)}
        options={[{ value: 'all', label: 'All years' }, ...yearOptions.map(yg => ({
          value: yg,
          label: `${yearWords(yg)}${availableYearGroups.includes(yg) ? '' : ' (none yet)'}`,
          short: yearWords(yg),
        }))]}
      />
    </>
  );
  const resetCohort = (curriculumFilter !== 'all' || yearGroupFilter !== 'all') ? (
    <TextButton tone="quiet" onClick={() => { setCurriculumFilter('all'); setYearGroupFilter('all'); }}>Reset</TextButton>
  ) : null;

  const blocksFigure = (
    <span className="gc8-trend"><TrendGlyph className={`ui-icon ${trend >= 0 ? 'gc8-up' : 'gc8-down'}`} width={16} height={16} strokeWidth={2} aria-hidden="true" />{trendWords}</span>
  );

  // One early warning, as a row that opens the student (phone) or a laptop row with Dismiss.
  const warningRow = (alert: EarlyWarningAlert, withDismiss: boolean) => (
    <Row
      key={alert.id}
      art={<StudentArt seed={alert.studentAvatar} />}
      title={alert.studentName}
      label={`View ${alert.studentName}: ${SEVERITY_WORDS[alert.severity]}, ${alert.title}`}
      meta={<span className="gc8-why"><SeverityDot severity={alert.severity} /><b>{SEVERITY_WORDS[alert.severity]}</b> · {alert.title}</span>}
      onPress={() => { setAllList(null); onSelectStudent(alert.studentUid); }}
      end={withDismiss && onDismissAlert ? <TextButton tone="quiet" onClick={() => onDismissAlert(alert)}>Dismiss</TextButton> : undefined}
    />
  );
  const warningLaptopRow = (alert: EarlyWarningAlert) => (
    <div key={alert.id} className="gc8-warn">
      <span className="gc8-sev"><SeverityDot severity={alert.severity} />{SEVERITY_WORDS[alert.severity]}</span>
      <StudentArt seed={alert.studentAvatar} size={32} />
      <button type="button" className="gc8-warn-open" onClick={() => onSelectStudent(alert.studentUid)} aria-label={`View ${alert.studentName}: ${alert.title}`}>
        <span className="gc8-person">{alert.studentName} <span>· {alert.title}</span></span>
        <span className="gc8-meta">{alert.description}</span>
      </button>
      {onDismissAlert ? <TextButton tone="quiet" title="Dismiss (will resurface if situation worsens)" onClick={() => onDismissAlert(alert)}>Dismiss</TextButton> : <span />}
      <ChevronRight className="ui-icon" width={20} height={20} strokeWidth={1.75} aria-hidden="true" />
    </div>
  );
  const attentionRow = ({ student, status, flag, daysSince }: typeof attentionStudents[number]) => (
    <Row
      key={student.user.uid}
      art={<StudentArt seed={student.user.avatar} size={wide ? 32 : 40} />}
      title={student.user.name}
      label={`View ${student.user.name}, status: ${STATUS_WORDS[status]}${flag ? ', flagged' : ''}`}
      meta={wide
        ? <StatusWords status={status} />
        : <StatusWords status={status}>{flag ? ' · flagged' : ''} · {daysWords(daysSince)}</StatusWords>}
      trailing={wide ? <>
        {flag ? <Flag className="ui-icon gc8-flag" width={16} height={16} strokeWidth={2} aria-label={`Flagged: ${flag.priority} priority`} /> : null}
        <span className="gc8-ago">{Number.isFinite(daysSince) && daysSince > 0
          ? <><b>{daysSince}</b>{daysSince === 1 ? ' day' : ' days'}</>
          : daysWords(daysSince)}</span>
      </> : undefined}
      onPress={() => { setAllList(null); onSelectStudent(student.user.uid); }}
    />
  );
  const recentRow = (s: typeof recentlyActive[number]) => (
    <Row
      key={s.uid}
      art={<StudentArt seed={s.avatar} />}
      title={s.name}
      meta={s.blocksCompletedToday > 0 ? `${s.blocksCompletedToday} ${s.blocksCompletedToday === 1 ? 'block' : 'blocks'} today` : 'None today'}
      value={s.timeAgo}
      onPress={() => { setAllList(null); onSelectStudent(s.uid); }}
    />
  );
  const gapRowPhone = (gap: typeof topGaps[number]) => (
    <div key={gap.subjectName} className="gc8-pgap">
      <SubjectAvatar subject={gap.subjectName} className="gc8-art gc8-art--32" />
      <div className="gc8-pgap-body">
        <div className="gc8-who">
          <span className="gc8-person">{gap.subjectName} <span className="gc8-meta">· {gap.studentCount} {gap.studentCount === 1 ? 'student' : 'students'}</span></span>
          <span className="gc8-gpts"><span className="gc8-strong">{gap.avgGap}</span><small className="gc8-unit">pts</small></span>
        </div>
        <span className="gc8-bar"><i style={{ width: `${(gap.avgGap / maxAvgGap) * 100}%` }} /></span>
      </div>
    </div>
  );

  const allListSheet = allList ? (() => {
    const lists = {
      warnings: { title: 'Early warning signals', rows: alerts.map(alert => warningRow(alert, true)), className: 'gc8-list gc8-warnlist' },
      attention: { title: 'Attention', rows: attentionStudents.map(attentionRow) },
      recent: { title: 'Recently active', rows: recentlyActive.map(recentRow) },
      gaps: { title: 'Subject-level gaps', rows: null },
    } as const;
    return lists[allList];
  })() : null;

  // ─── The students: search, the nine statuses, the sort ─────────────────
  const sortOptions: { value: SortKey; label: string }[] = [
    { value: 'name', label: 'Name' },
    { value: 'progress', label: 'Progress' },
    { value: 'cao-current', label: attainmentHeadings.current },
    { value: 'cao-target', label: attainmentHeadings.target },
    { value: 'gap', label: attainmentHeadings.gap },
    { value: 'streak', label: 'Streak' },
  ];
  const openFilterSheet = () => { setDraftStatus(statusFilter); setDraftSortKey(sortKey); setDraftSortDir(sortDir); setFilterOpen(true); };
  const draftCount = cohortScopedStats.filter(s => (!searchQuery || s.student.user.name.toLowerCase().includes(searchQuery.toLowerCase())) && statusMatch(s, draftStatus, gcFlags)).length;
  const statusFilterLabel = STATUS_FILTERS.find(f => f.key === statusFilter)?.label ?? 'All';
  const sortWords = `${sortOptions.find(o => o.value === sortKey)?.label ?? 'Name'}, ${sortKey === 'name'
    ? (sortDir === 'asc' ? 'A to Z' : 'Z to A')
    : (sortDir === 'desc' ? 'highest first' : 'lowest first')}`;

  const studentRowPhone = (row: typeof filtered[number]) => {
    const uid = row.student.user.uid;
    const flag = gcFlags?.getFlagData(uid);
    const days = daysSinceBlock(row.student);
    const detail = row.streak > 0 ? ` · ${row.streak}-day streak` : Number.isFinite(days) ? ` · ${daysWords(days)}` : '';
    return (
      <Row
        key={uid}
        art={<StudentArt seed={row.student.user.avatar} />}
        title={row.student.user.name}
        label={`View ${row.student.user.name}, status: ${STATUS_WORDS[row.status]}${flag ? ', flagged' : ''}`}
        meta={<StatusWords status={row.status}>{flag ? ' · flagged' : ''}{detail}</StatusWords>}
        trailing={<><Pct value={row.progress} className="ui-row-value" /><ChevronRight className="ui-icon ui-row-chev" width={20} height={20} strokeWidth={1.75} aria-hidden="true" /></>}
        onPress={() => onSelectStudent(uid)}
      />
    );
  };

  const rowMenu = (row: typeof filtered[number]) => {
    const uid = row.student.user.uid;
    const rowFlag = gcFlags?.getFlagData(uid) ?? null;
    if (!gcFlags && !onResetPassword && !onDeleteStudent) return <span />;
    return (
      <MenuPanel
        label={row.student.user.name}
        buttonLabel={`Actions for ${row.student.user.name}`}
        buttonClassName="gc8-acts"
        className="gc8-rowmenu"
        chevron={false}
        face={<MoreHorizontal className="ui-icon" width={20} height={20} strokeWidth={1.75} aria-hidden="true" />}
      >
        {gcFlags && (
          <MenuRadioRows<FlagPriority>
            label={rowFlag ? 'Edit student flag' : 'Flag student'}
            value={(rowFlag?.priority ?? '') as FlagPriority}
            onChange={priority => { void (rowFlag ? gcFlags.updateFlagPriority(uid, priority) : gcFlags.flagStudent(uid, priority)); }}
            options={[{ value: 'high', label: 'Flagged, high priority' }, { value: 'normal', label: 'Flagged, normal priority' }]}
          />
        )}
        {gcFlags && rowFlag && <MenuAction plain title="Remove flag" onPress={() => { void gcFlags.unflagStudent(uid); }} />}
        {gcFlags && (onResetPassword || onDeleteStudent) && <MenuRule />}
        {onResetPassword && <MenuAction plain title="Reset password" onPress={() => onResetPassword(uid)} />}
        {onDeleteStudent && <MenuAction plain tone="danger" title="Delete account" onPress={() => onDeleteStudent(row.student.user)} />}
      </MenuPanel>
    );
  };

  const sortHead = (key: SortKey, label: string, numeric = false, hint?: string) => (
    <button
      type="button"
      className={`gc8-th${numeric ? ' gc8-th--n' : ''}`}
      aria-sort={sortKey === key ? (sortDir === 'asc' ? 'ascending' : 'descending') : undefined}
      title={hint}
      onClick={() => handleSort(key)}
    >
      {label}
      {sortKey === key ? (sortDir === 'asc'
        ? <ArrowUp className="ui-icon" width={14} height={14} strokeWidth={2} aria-hidden="true" />
        : <ArrowDown className="ui-icon" width={14} height={14} strokeWidth={2} aria-hidden="true" />) : null}
    </button>
  );

  const emptyStudents = filtered.length === 0 ? (
    <div className="gc8-empty" role="status">
      <b>
        {studentData.length === 0
          ? 'No students have signed up yet.'
          : curriculumFilter === 'junior' && cohortCurriculumCounts.junior === 0
            ? 'No Junior Cycle students yet.'
            : curriculumFilter === 'senior' && cohortCurriculumCounts.senior === 0
              ? 'No Senior Cycle students yet.'
              : 'No students match your filters.'}
      </b>
      {studentData.length === 0
        ? 'Students will appear here once they register.'
        : curriculumFilter === 'junior' && cohortCurriculumCounts.junior === 0
          ? 'Junior Cycle support is new — when 1st/2nd/3rd-year students sign up they\'ll appear here.'
          : curriculumFilter === 'senior' && cohortCurriculumCounts.senior === 0
            ? 'When 5th/6th-year students sign up they\'ll appear here.'
            : 'Try adjusting your search or filter criteria.'}
    </div>
  ) : null;

  const searchField = (
    <SearchField
      label="Search students"
      placeholder="Search students"
      value={searchQuery}
      onChange={(e) => setSearchQuery(e.target.value)}
      className={wide ? 'gc8-find' : undefined}
    />
  );
  const statusGuideLink = (
    <TextButton tone="quiet" className="gc8-ib" onClick={() => setShowStatusGuide(true)}>
      <CircleHelp className="ui-icon" width={16} height={16} strokeWidth={2} aria-hidden="true" />Status guide
    </TextButton>
  );

  // ─── The sheets every place shares ──────────────────────────────────────
  const sheets = (
    <>
      {/* Broadcast: who it goes to, one preset message, one Send */}
      {(() => {
        // Year options scoped by the active broadcast curriculum, same
        // pattern as the dashboard cohort filter.
        const broadcastYearOptions: readonly YearGroup[] =
          broadcastCurriculum === 'junior' ? ['1st', '2nd', '3rd'] as const
          : broadcastCurriculum === 'senior' ? ['TY', '5th', '6th'] as const
          : ['1st', '2nd', '3rd', 'TY', '5th', '6th'] as const;

        // Compute recipients based on the modal's own audience scope.
        // Empty set = "all years in scope" (whole-curriculum broadcast).
        const broadcastRecipients = studentData.filter(s => {
          if (broadcastCurriculum !== 'all') {
            const lvl: CurriculumLevel | undefined =
              s.curriculumLevel ?? (s.yearGroup ? (isJuniorYear(s.yearGroup) ? 'junior' : 'senior') : undefined);
            if (lvl !== broadcastCurriculum) return false;
          }
          if (broadcastYearGroups.size > 0) {
            if (!s.yearGroup || !broadcastYearGroups.has(s.yearGroup)) return false;
          }
          return true;
        });

        const toggleYear = (yg: YearGroup) => {
          setBroadcastYearGroups(prev => {
            const next = new Set(prev);
            if (next.has(yg)) next.delete(yg); else next.add(yg);
            return next;
          });
        };
        const selectAllYears = () => setBroadcastYearGroups(new Set());

        // Build a human-readable audience label for the button + subtitle.
        const audienceLabel = (() => {
          const parts: string[] = [];
          if (broadcastCurriculum === 'junior') parts.push('Junior Cycle');
          else if (broadcastCurriculum === 'senior') parts.push('Senior Cycle');
          if (broadcastYearGroups.size > 0) {
            const sortedYears = broadcastYearOptions.filter(y => broadcastYearGroups.has(y));
            parts.push(sortedYears.map(y => y === 'TY' ? 'TY' : `${y} Year`).join(', '));
          }
          return parts.length === 0 ? 'all students' : parts.join(' · ');
        })();

        const send = async () => {
          if (!broadcastMessageId || broadcastRecipients.length === 0) return;
          setIsBroadcasting(true);
          // Server-composed, preset-only. See functions/src/staffMessagePolicy.
          try {
            const fn = httpsCallable<
              { studentUids: string[]; kind: string; messageId: string },
              { success: true; delivered: number }
            >(getFunctions(app), 'sendStaffNotification');
            await fn({
              studentUids: broadcastRecipients.map(s => s.user.uid),
              kind: 'broadcast',
              messageId: broadcastMessageId,
            });
          } catch (err) {
            logError('GCOverview.broadcast', err);
          }
          setIsBroadcasting(false);
          setShowBroadcastModal(false);
          setBroadcastMessageId('');
          // Reset audience to default for the next broadcast
          setBroadcastCurriculum('all');
          setBroadcastYearGroups(new Set());
        };

        return (
          <Sheet
            open={showBroadcastModal}
            title="Broadcast message"
            onClose={() => { if (!isBroadcasting) setShowBroadcastModal(false); }}
            footer={broadcastRecipients.length === 0
              ? <Button kind="main" size="lg" block unavailable="No students are in this audience.">No recipients</Button>
              : <Button
                  kind="main"
                  size="lg"
                  block
                  arrow="forward"
                  missing={!broadcastMessageId ? { sentence: `Choose a message for ${audienceLabel}.`, goTo: broadcastMessagesRef } : undefined}
                  onClick={() => { if (!isBroadcasting) void send(); }}
                >
                  {isBroadcasting ? 'Sending...' : `Send to ${broadcastRecipients.length}`}
                </Button>}
          >
            <div className="gc8-sheet-body">
              <p className="gc8-sub">
                Sending to <span className="gc8-strong">{broadcastRecipients.length}</span> {broadcastRecipients.length === 1 ? 'student' : 'students'}
                {broadcastCurriculum !== 'all' || broadcastYearGroups.size > 0 ? ` · ${audienceLabel}` : ''}
              </p>
              <div className="gc8-sheet-group">
                <p className="gc8-label">Audience</p>
                <SelectionBar
                  label="Audience"
                  size="md"
                  value={broadcastCurriculum}
                  onChange={lvl => { setBroadcastCurriculum(lvl); setBroadcastYearGroups(new Set()); }}
                  options={[{ value: 'all', label: 'Everyone' }, { value: 'junior', label: 'Junior Cycle' }, { value: 'senior', label: 'Senior Cycle' }]}
                />
                <div className="gc8-yearbtns">
                  <Button size="sm" aria-pressed={broadcastYearGroups.size === 0} onClick={selectAllYears}>All years</Button>
                  {broadcastYearOptions.map(yg => (
                    <Button key={yg} size="sm" aria-pressed={broadcastYearGroups.has(yg)} onClick={() => toggleYear(yg)}>
                      {yearWords(yg)} <span className="gc8-count">{studentData.filter(s => s.yearGroup === yg).length}</span>
                    </Button>
                  ))}
                </div>
              </div>
              <div className="gc8-sheet-group" ref={broadcastMessagesRef}>
                <p className="gc8-label">Choose a message for {audienceLabel}</p>
                <div className="gc8-msgs" role="radiogroup" aria-label="Message">
                  {STAFF_BROADCASTS.map(message => (
                    <ChoiceTile
                      key={message.id}
                      kind="one"
                      chosen={broadcastMessageId === message.id}
                      label={message.text}
                      onClick={() => setBroadcastMessageId(message.id)}
                    />
                  ))}
                </div>
              </div>
            </div>
          </Sheet>
        );
      })()}

      {/* Export: the four parts, CSV or PDF */}
      <GCExportModal
        isOpen={showExportModal}
        onClose={() => setShowExportModal(false)}
        studentData={cohortScopedStudents}
        allCourses={allCourses}
        school={school}
      />

      {/* The status guide: each status in its own words, marked in ink */}
      <Sheet open={showStatusGuide} title="Status guide" onClose={() => setShowStatusGuide(false)}>
        <div className="gc8-sheet-body">
          <h3 className="gc8-h">What do the statuses mean?</h3>
          <div className="gc8-guide">
            {STATUS_GUIDE.map(s => (
              <div key={s.status}>
                <StatusDot status={s.status} />
                <span className="gc8-guide-copy"><span className="gc8-person">{STATUS_WORDS[s.status]}</span><span className="gc8-sub">{s.desc}</span></span>
              </div>
            ))}
          </div>
        </div>
      </Sheet>

      {/* Filter students: the nine statuses and the sort, and how many you will see */}
      <Sheet
        open={filterOpen}
        title="Filter students"
        titleSize="small"
        onClose={() => setFilterOpen(false)}
        actions={<TextButton tone="quiet" onClick={() => { setDraftStatus('all'); setDraftSortKey('name'); setDraftSortDir('asc'); }}>Reset</TextButton>}
        footer={
          <Button kind="main" size="lg" block onClick={() => {
            setStatusFilter(draftStatus);
            setSortKey(draftSortKey);
            setSortDir(draftSortDir);
            setFilterOpen(false);
          }}>
            {`Show ${draftCount} ${draftCount === 1 ? 'student' : 'students'}`}
          </Button>
        }
      >
        <div className="gc8-sheet-body">
          <div className="gc8-sheet-group">
            <p className="gc8-label">Status</p>
            <div className="gc8-grid2" role="radiogroup" aria-label="Status">
              {STATUS_FILTERS.map(f => {
                const count = statusCounts[f.key] ?? 0;
                return (
                  <ChoiceTile
                    key={f.key}
                    kind="one"
                    chosen={draftStatus === f.key}
                    label={f.label}
                    meta={count === 0 ? 'None' : `${count} ${count === 1 ? 'student' : 'students'}`}
                    onClick={() => setDraftStatus(f.key)}
                  />
                );
              })}
            </div>
          </div>
          <div className="gc8-sheet-group">
            <p className="gc8-label">Sort by</p>
            <Menu block label="Sort by" value={draftSortKey} onChange={value => setDraftSortKey(value as SortKey)} options={sortOptions} />
            <SelectionBar
              label="Order"
              value={draftSortDir}
              onChange={value => setDraftSortDir(value as SortDir)}
              options={draftSortKey === 'name'
                ? [{ value: 'asc', label: 'A to Z' }, { value: 'desc', label: 'Z to A' }]
                : [{ value: 'desc', label: 'Highest first' }, { value: 'asc', label: 'Lowest first' }]}
            />
          </div>
        </div>
      </Sheet>

      {/* "All …": the whole of a list the page shows the first few of */}
      <Sheet open={!!allListSheet} title={allListSheet?.title ?? ''} onClose={() => setAllList(null)}>
        {allList === 'gaps'
          ? <div className="gc8-pgaps">{topGaps.map(gapRowPhone)}</div>
          : <List className={(allListSheet && 'className' in allListSheet ? allListSheet.className : undefined) ?? 'gc8-list'}>{allListSheet?.rows}</List>}
      </Sheet>
    </>
  );

  // ─── Students, a place of its own on a phone ────────────────────────────
  if (place === 'students' && !wide) {
    return (
      <>
        <section className="gc8-head" aria-labelledby="gc8-students-title">
          <div className="gc8-head-row">
            <h1 id="gc8-students-title" className="gc8-name">Students</h1>
            {statusGuideLink}
          </div>
          {cohortScopeLabel && <p className="gc8-sub">Showing: {cohortScopeLabel}</p>}
        </section>
        <section className="gc8-sec">
          {searchField}
          <Button block arrow="menu" className="gc8-filterbtn" aria-label={`Filter and sort students: ${statusFilterLabel}, ${sortWords}`} onClick={openFilterSheet}>
            {statusFilterLabel} · {sortWords}
          </Button>
          <ul className="ui-list gc8-list">{filtered.map(studentRowPhone)}</ul>
          {emptyStudents}
          <div className="gc8-best">
            <Button onClick={handleExportCSV}>Export list</Button>
          </div>
        </section>
        {sheets}
      </>
    );
  }

  // ─── The Overview: every part of today's page, in today's order ──────────
  const warningsSection = alerts.length > 0 ? (
    <section className="gc8-sec" aria-labelledby="gc8-warnings">
      <div className="gc8-sechead"><h2 id="gc8-warnings" className="gc8-h">Early warning signals</h2><span className="gc8-meta">{alertCounts}</span></div>
      {wide
        ? <div className="gc8-warns">{alerts.slice(0, firstFew).map(warningLaptopRow)}</div>
        : <List className="gc8-list">{alerts.slice(0, firstFew).map(alert => warningRow(alert, false))}</List>}
      {alerts.length > firstFew && (
        <TextButton className="gc8-more" arrow="forward" onClick={() => setAllList('warnings')}>{`All ${alerts.length} warnings`}</TextButton>
      )}
    </section>
  ) : null;

  const attentionSection = (
    <section className="gc8-sec" aria-labelledby="gc8-attention">
      <div className="gc8-sechead"><h2 id="gc8-attention" className="gc8-h">Attention</h2>{needsAttentionCount > 0 && <span className="gc8-meta">{attentionMeta}</span>}</div>
      {needsAttentionCount === 0 ? (
        <div className="gc8-empty"><b>All students are engaged</b>No students drifting, at risk, or flagged</div>
      ) : (
        <>
          <List className={`gc8-list${wide ? ' gc8-att' : ''}`}>{attentionStudents.slice(0, firstFew).map(attentionRow)}</List>
          {attentionStudents.length > firstFew && (
            <TextButton className="gc8-more" arrow="forward" onClick={() => setAllList('attention')}>{`All ${attentionStudents.length}`}</TextButton>
          )}
        </>
      )}
    </section>
  );

  const activitySection = (
    <section id="gc-analytics" className="gc8-sec">
      <DailyActivityChart aggregatedActivity={aggregatedActivity} activityRange={activityRange} onRangeChange={setActivityRange} wide={wide} />
    </section>
  );

  const recentSection = (
    <section className="gc8-sec" aria-labelledby="gc8-recent">
      <div className="gc8-sechead">
        <div className="gc8-sechead-col"><p className="gc8-label">Activity</p><h2 id="gc8-recent" className="gc8-h">Recently active</h2></div>
        {wide && recentlyActive.length > 0 && <span className="gc8-meta">{`The last ${recentlyActive.length} ${recentlyActive.length === 1 ? 'student' : 'students'} to study`}</span>}
      </div>
      {recentlyActive.length === 0 ? (
        <p className="gc8-empty">No recent activity.</p>
      ) : wide ? (
        <div className="gc8-recent">
          {recentlyActive.map(s => (
            <button key={s.uid} type="button" className="ui-part gc8-ra" onClick={() => onSelectStudent(s.uid)}>
              <StudentArt seed={s.avatar} size={32} />
              <span className="gc8-ra-copy">
                <span className="gc8-person" title={s.name}>{s.name}</span>
                <span className="gc8-meta">{s.blocksCompletedToday > 0 ? `${s.blocksCompletedToday} ${s.blocksCompletedToday === 1 ? 'block' : 'blocks'} today` : 'None today'}</span>
              </span>
              <span className="gc8-meta">{s.timeAgo}</span>
            </button>
          ))}
        </div>
      ) : (
        <>
          <List className="gc8-list">{recentlyActive.slice(0, firstFew).map(recentRow)}</List>
          {recentlyActive.length > firstFew && <TextButton className="gc8-more" arrow="forward" onClick={() => setAllList('recent')}>{`All ${recentlyActive.length}`}</TextButton>}
        </>
      )}
    </section>
  );

  // The one live orange figure is the countdown beside the Exam calendar (board); the one at the top of
  // a laptop's page is ink.
  const countdown = (big: boolean, live = true) => (
    <p className={`gc8-countdown${big ? ' gc8-countdown--big' : ''}`}>
      <span className={`gc8-num${live ? ' gc8-live' : ''}`}>{daysUntilLC}</span>
      <span className="gc8-meta">days to the{big ? ' ' : <br />}Leaving Cert{big ? <><br />{lcDateWords}</> : null}</span>
    </p>
  );
  const calendarSection = (
    <section className="gc8-sec" aria-labelledby="gc8-cal">
      <div className="gc8-sechead">
        <div className="gc8-sechead-col"><p className="gc8-label">Countdown</p><h2 id="gc8-cal" className="gc8-h">Exam calendar</h2></div>
        {wide ? <span className="gc8-meta">Choose a day to see what is on</span> : countdown(false)}
      </div>
      <GCCalendar events={schoolEvents} months={twoMonths ? 2 : 1} beside={wide} countdown={wide ? countdown(true) : undefined} />
    </section>
  );

  const distributionSection = (
    <section className="gc8-sec" aria-labelledby="gc8-dist">
      <div className="gc8-sechead">
        <div className="gc8-sechead-col"><p className="gc8-label">Distribution{cohortScopeLabel ? ` · ${cohortScopeLabel}` : ''}</p><h2 id="gc8-dist" className="gc8-h">Progress breakdown</h2></div>
        <span className="gc8-meta">{distributionTotal} students</span>
      </div>
      <div className="gc8-dist" role="img" aria-label={`Students by progress: ${['0–25%', '25–50%', '50–75%', '75–100%'].map((b, i) => `${b} ${distribution[i]}`).join(', ')}`}>
        {distribution.map((count, i) => (
          <div key={i}>
            <span className="gc8-readout">{count}</span>
            <i style={{ height: count > 0 ? `${Math.max((count / distributionMax) * 80, 6)}%` : 0 }} />
          </div>
        ))}
      </div>
      <div className="gc8-distx" aria-hidden="true">{['0–25%', '25–50%', '50–75%', '75–100%'].map(b => <span key={b}>{b}</span>)}</div>
    </section>
  );

  const gapsSection = topGaps.length > 0 ? (
    <section className="gc8-sec" aria-labelledby="gc8-gaps">
      <div className="gc8-sechead">
        <div className="gc8-sechead-col"><p className="gc8-label">Subject analysis{cohortScopeLabel ? ` · ${cohortScopeLabel}` : ''}</p><h2 id="gc8-gaps" className="gc8-h">Subject-level gaps</h2></div>
        <span className="gc8-meta">{wide ? 'Points to target · students' : 'Points to target'}</span>
      </div>
      {wide ? (
        <div className="gc8-gaps">
          {topGaps.map(gap => (
            <div key={gap.subjectName} className="gc8-gaprow">
              <SubjectAvatar subject={gap.subjectName} className="gc8-art gc8-art--28" />
              <span>{gap.subjectName}</span>
              <span className="gc8-bar"><i style={{ width: `${(gap.avgGap / maxAvgGap) * 100}%` }} /></span>
              <span className="gc8-gpts"><span className="gc8-strong">{gap.avgGap}</span><small className="gc8-unit">pts</small></span>
              <span className="gc8-meta gc8-n">{gap.studentCount}</span>
            </div>
          ))}
        </div>
      ) : (
        <>
          <div className="gc8-pgaps">{topGaps.slice(0, 4).map(gapRowPhone)}</div>
          {topGaps.length > 4 && <TextButton className="gc8-more" arrow="forward" onClick={() => setAllList('gaps')}>{`All ${topGaps.length} subjects`}</TextButton>}
        </>
      )}
    </section>
  ) : null;

  const studentsLaptop = (
    <section id="gc-students" className="gc8-sec" aria-labelledby="gc8-all">
      <div className="gc8-sechead">
        <h2 id="gc8-all" className="gc8-h">All students</h2>
        <div className="gc8-row-x">{searchField}{statusGuideLink}<Button onClick={handleExportCSV}>Export list</Button></div>
      </div>
      <div className="gc8-filts" role="group" aria-label="Status">
        {STATUS_FILTERS.map(f => (
          <Button key={f.key} size="sm" aria-pressed={statusFilter === f.key} onClick={() => setStatusFilter(f.key)}>
            {f.label} <span className="gc8-count">{statusCounts[f.key] ?? 0}</span>
          </Button>
        ))}
      </div>
      {/* The full table from 1200px; beside the sidebar on a narrower screen its nine columns do not fit,
          so the students are the phone's rows there (each opens the student, whose page has flag,
          reset and delete). */}
      {!twoMonths ? <ul className="ui-list gc8-list">{filtered.map(studentRowPhone)}</ul> : (
      <div className="gc8-tablewrap">
        <div className="gc8-table" role="table" aria-label="All students">
          <div className="gc8-tr gc8-tr--head" role="row">
            <span role="columnheader">{sortHead('name', 'Student')}</span>
            <span role="columnheader">{sortHead('progress', 'Progress')}</span>
            <span role="columnheader">{sortHead('cao-current', attainmentHeadings.current, true, attainmentHeadings.hint)}</span>
            <span role="columnheader">{sortHead('cao-target', attainmentHeadings.target, true, attainmentHeadings.hint)}</span>
            <span role="columnheader">{sortHead('gap', attainmentHeadings.gap, true, attainmentHeadings.hint)}</span>
            <span role="columnheader">{sortHead('streak', 'Streak', true)}</span>
            <span role="columnheader" className="gc8-label">Status</span>
            <span role="columnheader"><span className="sr-only">Flag</span></span>
            <span role="columnheader"><span className="sr-only">Actions</span></span>
          </div>
          {filtered.map(row => {
            const gap = row.targetCAO - row.currentCAO;
            const uid = row.student.user.uid;
            const rowFlag = gcFlags?.getFlagData(uid);
            const dash = <span className="gc8-dim">–</span>;
            return (
              <div key={uid} className="gc8-tr" role="row">
                <span role="cell">
                  <button type="button" className="ui-part gc8-stu" onClick={() => onSelectStudent(uid)}>
                    <StudentArt seed={row.student.user.avatar} size={32} /><span title={row.student.user.name}>{row.student.user.name}</span>
                  </button>
                </span>
                <span role="cell" className="gc8-prog"><Pct value={row.progress} /><span className="gc8-bar gc8-bar--thin"><i style={{ width: `${row.progress}%` }} /></span></span>
                {/* Per-row, not per-filter: a mixed school shows each
                    student in their own terms — CAO points for senior,
                    Merit+ counts for JC — instead of hiding the column or
                    printing a JC student's non-existent CAO as 0. */}
                {row.isJunior ? (
                  <>
                    <span role="cell" className="gc8-n">{row.subjectsCovered ? `${row.topBandsCount} / ${row.subjectsCovered}` : dash}</span>
                    <span role="cell" className="gc8-n">{row.subjectsCovered ? `${row.targetTopBandsCount} / ${row.subjectsCovered}` : dash}</span>
                    <span role="cell" className="gc8-n">{row.subjectsCovered ? `+${Math.max(0, row.targetTopBandsCount - row.topBandsCount)}` : dash}</span>
                  </>
                ) : (
                  <>
                    <span role="cell" className="gc8-n">{row.hasGrades ? row.currentCAO : dash}</span>
                    <span role="cell" className="gc8-n">{row.hasGrades ? row.targetCAO : dash}</span>
                    <span role="cell" className="gc8-n">{row.hasGrades ? `${gap > 0 ? '+' : ''}${gap}` : dash}</span>
                  </>
                )}
                <span role="cell" className="gc8-n">
                  {row.streak > 0
                    ? <span className="gc8-streak"><Flame className="ui-icon" width={16} height={16} strokeWidth={2} aria-hidden="true" />{row.streak}</span>
                    : <span className="gc8-dim">{row.streak}</span>}
                </span>
                <span role="cell"><StatusWords status={row.status} /></span>
                <span role="cell">{rowFlag ? <Flag className="ui-icon gc8-flag" width={16} height={16} strokeWidth={2} aria-label={`Flagged: ${rowFlag.priority} priority`} /> : null}</span>
                <span role="cell">{rowMenu(row)}</span>
              </div>
            );
          })}
        </div>
      </div>
      )}
      {emptyStudents}
    </section>
  );

  const studentsPhone = (
    <section className="gc8-sec" aria-labelledby="gc8-all">
      <div className="gc8-sechead"><h2 id="gc8-all" className="gc8-h">All students</h2></div>
      <List boxed>
        <Row
          title={`See all ${cohortScopedStats.length} ${cohortScopedStats.length === 1 ? 'student' : 'students'}`}
          meta="Search, filter by status, sort"
          onPress={onOpenStudents}
        />
      </List>
      <div className="gc8-best">
        <p className="gc8-label">Best on a laptop</p>
        <p className="gc8-sub">The full table with points, targets and gaps side by side, and exporting it.</p>
      </div>
    </section>
  );

  return (
    <>
      <section id="gc-overview" className="gc8-hero" aria-labelledby="gc8-greeting">
        <div className="gc8-head">
          <h1 id="gc8-greeting" className="gc8-title">{greeting}</h1>
          {wide
            ? <p className="gc8-sub">{getSchoolName(school)}.{needsAttentionCount > 0 ? ` ${needsAttentionCount} ${needsAttentionCount === 1 ? 'student' : 'students'} could do with a look today.` : ''}</p>
            : <p className="gc8-sub">{daysUntilLC} days to the Leaving Cert.{dataAsOf ? ` Data as of ${dataAsOf}.` : ''}</p>}
          {!wide && notice && <p className="gc8-sub gc8-strong">{notice}</p>}
        </div>
        {wide && (
          <div className="gc8-hero-end">
            {countdown(false, false)}
            <div className="gc8-row-x">
              <Button onClick={() => setShowExportModal(true)}>Export</Button>
              <Button onClick={() => setShowBroadcastModal(true)}>Broadcast</Button>
            </div>
          </div>
        )}
      </section>

      {wide ? (
        <div className="gc8-filter">
          <span className="gc8-label">Showing</span>
          {cohortMenus}
          {resetCohort}
          <span className="gc8-meta">{countLine}</span>
        </div>
      ) : (
        <section className="gc8-sec">
          <div className="gc8-row-x">{cohortMenus}{resetCohort}</div>
          <p className="gc8-meta">{countLine}</p>
          <div className="gc8-pair">
            <Button onClick={() => setShowBroadcastModal(true)}>Broadcast</Button>
            <Button onClick={() => setShowExportModal(true)}>Export</Button>
          </div>
        </section>
      )}

      {wide ? (
        <div className="gc8-figs">
          <div><p className="gc8-label">Total students</p><p className="gc8-num">{cohortScopedStudents.length}</p><p className="gc8-meta">In this view</p></div>
          <div><p className="gc8-label">Average progress</p><p className="gc8-num"><Fig value={avgProgress.toFixed(0)} unit="%" /></p><p className="gc8-meta">Through their modules</p></div>
          <div><p className="gc8-label">Blocks this week</p><p className="gc8-num">{weeklyTrends.blocksThisWeek}</p><p className="gc8-meta">{blocksFigure}</p></div>
        </div>
      ) : (
        <div className="gc8-figrows">
          <div><span className="gc8-sub">Students</span><span className="gc8-num">{cohortScopedStudents.length}</span></div>
          <div><span className="gc8-sub">Average progress</span><span className="gc8-num"><Fig value={avgProgress.toFixed(0)} unit="%" /></span></div>
          <div><span className="gc8-figrows-col"><span className="gc8-sub">Blocks this week</span><span className="gc8-meta">{blocksFigure}</span></span><span className="gc8-num">{weeklyTrends.blocksThisWeek}</span></div>
        </div>
      )}

      {wide ? <div className="gc8-two">{warningsSection ?? <span />}{attentionSection}</div> : <>{warningsSection}{attentionSection}</>}

      {wide
        ? <div className="gc8-two gc8-two--wide">{activitySection}<GCKeyEvents school={school} /></div>
        : <>{activitySection}<GCKeyEvents school={school} /></>}

      {recentSection}
      {calendarSection}

      {wide ? <div className="gc8-two gc8-two--even">{distributionSection}{gapsSection ?? <span />}</div> : <>{distributionSection}{gapsSection}</>}

      <SubjectHealthPanel studentData={cohortScopedStudents} wide={wide} />

      {wide ? studentsLaptop : studentsPhone}
      {sheets}
    </>
  );
};

// ─── Daily Activity Line Chart ──────────────────────────────────────────────
// One series drawn in ink with a flat fill, a scale, and a reading for the day you point at or tap
// (today's until you choose). The numbers are today's: the same 7 or 30 days, totals and average.

const CHART = { w: 560, h: 204, left: 44, right: 556, top: 16, base: 176, xlab: 200 };
const CHART_PHONE = { w: 342, h: 178, left: 36, right: 338, top: 14, base: 150, xlab: 172 };
const WEEKDAY = ['Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat'];
const MONTH_SHORT = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'];

function DailyActivityChart({
  aggregatedActivity,
  activityRange,
  onRangeChange,
  wide = true,
}: {
  aggregatedActivity: { date: string; count: number }[];
  activityRange: '7d' | '30d';
  onRangeChange: (range: '7d' | '30d') => void;
  wide?: boolean;
}) {
  const [chosenIdx, setChosenIdx] = useState<number | null>(null);
  const hitRef = useRef<HTMLDivElement>(null);

  const maxCount = Math.max(1, ...aggregatedActivity.map(d => d.count));
  const totalBlocks = aggregatedActivity.reduce((s, d) => s + d.count, 0);
  const activeDays = aggregatedActivity.filter(d => d.count > 0).length;
  const avgPerDay = activeDays > 0 ? (totalBlocks / aggregatedActivity.length).toFixed(1) : '0';
  const n = aggregatedActivity.length;
  const g = wide ? CHART : CHART_PHONE;

  // A scale with four lines: 0 and three steps of a round number.
  const step = Math.max(1, Math.ceil(maxCount / 3 / (maxCount > 30 ? 10 : maxCount > 6 ? 5 : 1)) * (maxCount > 30 ? 10 : maxCount > 6 ? 5 : 1));
  const top = step * 3;
  const yOf = (v: number) => g.base - (v / top) * (g.base - g.top);
  const xOf = (i: number) => (n > 1 ? g.left + (i / (n - 1)) * (g.right - 8 - g.left) : (g.left + g.right) / 2);

  // Monotone cubic interpolation (Fritsch-Carlson) — no overshoot, flat between equal values
  const buildMonotonePath = (pts: { x: number; y: number }[]): string => {
    if (pts.length < 2) return '';
    if (pts.length === 2) return `M${pts[0].x},${pts[0].y} L${pts[1].x},${pts[1].y}`;

    const len = pts.length;
    // Step 1: compute slopes between consecutive points
    const deltas: number[] = [];
    for (let i = 0; i < len - 1; i++) {
      const dx = pts[i + 1].x - pts[i].x;
      deltas.push(dx === 0 ? 0 : (pts[i + 1].y - pts[i].y) / dx);
    }

    // Step 2: compute tangents using Fritsch-Carlson
    const tangents: number[] = [deltas[0]];
    for (let i = 1; i < len - 1; i++) {
      if (deltas[i - 1] * deltas[i] <= 0) {
        // Sign change or zero — set tangent to 0 to prevent overshoot
        tangents.push(0);
      } else {
        tangents.push((deltas[i - 1] + deltas[i]) / 2);
      }
    }
    tangents.push(deltas[deltas.length - 1]);

    // Step 3: adjust tangents to ensure monotonicity
    for (let i = 0; i < len - 1; i++) {
      if (Math.abs(deltas[i]) < 1e-10) {
        // Flat segment — both tangents should be 0
        tangents[i] = 0;
        tangents[i + 1] = 0;
      } else {
        const alpha = tangents[i] / deltas[i];
        const beta = tangents[i + 1] / deltas[i];
        // Clamp to circle of radius 3 to prevent overshoot
        const mag = Math.sqrt(alpha * alpha + beta * beta);
        if (mag > 3) {
          tangents[i] = (3 * alpha / mag) * deltas[i];
          tangents[i + 1] = (3 * beta / mag) * deltas[i];
        }
      }
    }

    // Step 4: build cubic bezier path
    let d = `M${pts[0].x},${pts[0].y}`;
    for (let i = 0; i < len - 1; i++) {
      const dx = (pts[i + 1].x - pts[i].x) / 3;
      const cp1x = pts[i].x + dx;
      const cp1y = pts[i].y + tangents[i] * dx;
      const cp2x = pts[i + 1].x - dx;
      const cp2y = pts[i + 1].y - tangents[i + 1] * dx;
      d += ` C${cp1x},${cp1y} ${cp2x},${cp2y} ${pts[i + 1].x},${pts[i + 1].y}`;
    }
    return d;
  };

  const points = aggregatedActivity.map((d, i) => ({ x: xOf(i), y: yOf(d.count), date: d.date, count: d.count }));
  const linePath = buildMonotonePath(points);
  const areaPath = linePath && points.length ? `${linePath} L${points[points.length - 1].x},${g.base} L${points[0].x},${g.base} Z` : '';

  const dateOf = (key: string) => new Date(`${key}T00:00:00`);
  const dayWords = (key: string, i: number) => {
    if (i === n - 1) return 'Today';
    const d = dateOf(key);
    return `${WEEKDAY[d.getDay()]} ${d.getDate()}${n > 7 ? ` ${MONTH_SHORT[d.getMonth()]}` : ''}`;
  };
  const shown = chosenIdx !== null && chosenIdx < n ? chosenIdx : n - 1;
  const pick = points[shown];
  const pickFromPointer = (clientX: number) => {
    const box = hitRef.current?.getBoundingClientRect();
    if (!box || n <= 1) return;
    const x = ((clientX - box.left) / box.width) * g.w;
    const idx = Math.round(((x - g.left) / (g.right - 8 - g.left)) * (n - 1));
    setChosenIdx(Math.max(0, Math.min(n - 1, idx)));
  };
  // Which days carry a label under the axis: every day for a week, about six for a month.
  const labelEvery = n > 7 ? Math.ceil(n / 6) : 1;
  const readW = wide ? 100 : 86;
  const readX = pick ? Math.max(g.left, Math.min(pick.x - readW - 12, g.right - readW)) : 0;
  const readText = pick ? (shown === n - 1 ? 'Today' : (() => { const d = dateOf(pick.date); return `${WEEKDAY[d.getDay()]} ${d.getDate()} ${MONTH_SHORT[d.getMonth()]}`; })()) : '';

  return (
    <>
      <div className="gc8-sechead">
        <div className="gc8-sechead-col"><p className="gc8-label">Engagement</p><h2 className="gc8-h">Daily activity</h2></div>
        <Menu
          label="Activity range"
          value={activityRange}
          onChange={next => { setChosenIdx(null); onRangeChange(next); }}
          options={[{ value: '7d', label: wide ? 'Last 7 days' : '7 days' }, { value: '30d', label: wide ? 'Last 30 days' : '30 days' }]}
        />
      </div>
      <figure className="gc8-chart">
        <svg viewBox={`0 0 ${g.w} ${g.h}`} role="img" aria-label={`Study blocks a day, ${aggregatedActivity.map(d => d.count).join(', ')}`}>
          <g className="gc8-grid">{[0, 1, 2, 3].map(k => <line key={k} x1={g.left} x2={g.right} y1={yOf(step * k)} y2={yOf(step * k)} />)}</g>
          <g className="gc8-ylab">{[0, 1, 2, 3].map(k => <text key={k} x={g.left - 14} y={yOf(step * k) + 4}>{step * k}</text>)}</g>
          {areaPath && <path className="gc8-area" d={areaPath} />}
          {linePath && <path className="gc8-line" d={linePath} />}
          {pick && <line className="gc8-cross" x1={pick.x} x2={pick.x} y1={g.top} y2={g.base} />}
          {pick && (
            <g className="gc8-read">
              <rect x={readX} y={Math.max(g.top, Math.min(pick.y - 58, g.base - 44))} width={readW} height={wide ? 42 : 38} rx={8} />
              <text x={readX + 12} y={Math.max(g.top, Math.min(pick.y - 58, g.base - 44)) + 17} className="gc8-k">{readText}</text>
              <text x={readX + 12} y={Math.max(g.top, Math.min(pick.y - 58, g.base - 44)) + (wide ? 34 : 32)} className="gc8-v">{`${pick.count} ${pick.count === 1 ? 'block' : 'blocks'}`}</text>
            </g>
          )}
          {pick && <circle className="gc8-pt" cx={pick.x} cy={pick.y} r={4.5} />}
          <g className="gc8-xlab">
            {points.map((p, i) => ((n - 1 - i) % labelEvery === 0 ? (
              <text key={p.date} x={p.x} y={g.xlab} className={i === shown ? 'gc8-now' : undefined}>
                {wide || n > 7 ? dayWords(p.date, i) : WEEKDAY[dateOf(p.date).getDay()].charAt(0)}
              </text>
            ) : null))}
          </g>
        </svg>
        <div
          ref={hitRef}
          className="gc8-chart-hit"
          role="slider"
          tabIndex={0}
          aria-label="Day to read"
          aria-valuemin={1}
          aria-valuemax={n}
          aria-valuenow={shown + 1}
          aria-valuetext={`${readText}: ${pick?.count ?? 0} ${pick?.count === 1 ? 'block' : 'blocks'}`}
          onPointerDown={event => pickFromPointer(event.clientX)}
          onPointerMove={event => { if (event.pointerType === 'mouse' || event.buttons) pickFromPointer(event.clientX); }}
          onKeyDown={event => {
            if (event.key === 'ArrowLeft') setChosenIdx(Math.max(0, shown - 1));
            if (event.key === 'ArrowRight') setChosenIdx(Math.min(n - 1, shown + 1));
          }}
        />
      </figure>
      <p className="gc8-totals">
        <span><b>{totalBlocks}</b> {wide ? 'blocks in all' : 'blocks'}</span>
        <span><b>{activeDays}</b> active days</span>
        <span><b>{avgPerDay}</b> {wide ? 'a day on average' : 'a day'}</span>
        {wide && <span className="gc8-hint">Tap or point at any day to read it</span>}
      </p>
    </>
  );
}
