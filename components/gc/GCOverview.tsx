/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 */

import React, { useState, useMemo, useRef, useEffect } from 'react';
import { AnimatePresence } from 'framer-motion';
import { MotionDiv } from '../Motion';
import { TrendingUp, TrendingDown, AlertTriangle, Search, ChevronLeft, ChevronRight, Flame, UserX, Download, FileText, StickyNote, Trash2, X, AlertCircle, Eye, Megaphone, FileDown, UserPlus, CheckCircle, MinusCircle, Flag, Sparkles, KeyRound } from 'lucide-react';
import { type CourseData } from '../Library';
import { type CategoryType } from '../KnowledgeTree';
import { getAvatarUrl } from '../../utils/authUtils';
import { getSchoolName } from '../../schoolData';
import { doc, getDoc } from 'firebase/firestore';
import { db } from '../../firebase';
import { type SchoolEvent } from './GCKeyEvents';
import { type GCStudentFullData, type StudentStatus } from './gcTypes';
import {
  getOverallProgress,
  getCategoryProgress,
  getStudentStatus,
  getStudentCurrentCAO,
  getStudentTargetCAO,
  getDaysUntilLC,
  isActiveThisWeek,
  getProgressDistribution,
  getSubjectGaps,
  generateStudentCSV,
  getRecentlyActiveStudents,
} from './gcUtils';
import { type EarlyWarningAlert, type AlertSeverity } from './gcAlerts';
import { GCKeyEvents } from './GCKeyEvents';
import { SubjectHealthPanel } from './SubjectHealthPanel';
import { addNotificationToMultiple } from './gcNotifications';
import GCExportModal from './GCExportModal';
import { STATUS_CONFIG } from '../../utils/studentStatus';
import { type FlagData, type FlagPriority } from '../../hooks/useGCFlags';

const CUSTOM_EASE = [0.16, 1, 0.3, 1] as const;

// ─── Design tokens ──────────────────────────────────────────────────────────

const CARD_STYLE: React.CSSProperties = {
  backgroundColor: '#FAF7F4',
  border: '0.5px solid rgba(0,0,0,0.07)',
  borderRadius: 12,
  padding: 20,
};

const CARD_STYLE_DARK_CLASS = 'dark:!bg-[rgba(255,255,255,0.04)] dark:!border-[rgba(255,255,255,0.08)]';

const ACCENT = '#2A7D6F';
const _ACCENT_DARK = '#4DB8A4';
const SAGE = '#6B8F71';
const WARM_AMBER = '#C4873B';
const NEUTRAL_GREY = '#9A9590';
const TRACK_BG = '#EDEAE6';

// Dark mode badge/surface overrides (used via Tailwind dark: classes)
const _BADGE_SAGE_DARK = 'dark:!bg-[rgba(107,143,113,0.15)] dark:!text-[#8AB592]';
const _BADGE_AMBER_DARK = 'dark:!bg-[rgba(196,135,59,0.15)] dark:!text-[#D4A95C]';
const _BADGE_CLAY_DARK = 'dark:!bg-[rgba(42,125,111,0.15)] dark:!text-[#6BC4B0]';
const TEXT_ACCENT_DARK = 'dark:!text-[#4DB8A4]';
const TEXT_NEUTRAL_DARK = 'dark:!text-zinc-400';
const TRACK_BG_DARK = 'dark:!bg-zinc-800';

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

// ─── Calendar helpers ────────────────────────────────────────────────────────

function getCalendarDays(year: number, month: number): { day: number; isCurrentMonth: boolean }[] {
  const firstDay = new Date(year, month, 1).getDay();
  const daysInMonth = new Date(year, month + 1, 0).getDate();
  const offset = firstDay === 0 ? 6 : firstDay - 1; // Monday-start

  const days: { day: number; isCurrentMonth: boolean }[] = [];
  // Leading blanks
  for (let i = 0; i < offset; i++) {
    days.push({ day: 0, isCurrentMonth: false });
  }
  for (let d = 1; d <= daysInMonth; d++) {
    days.push({ day: d, isCurrentMonth: true });
  }
  return days;
}

function getLCExamDate(): Date {
  const now = new Date();
  const year = now.getFullYear();
  const june1 = new Date(year, 5, 1);
  let firstWed = new Date(june1);
  const dow = june1.getDay();
  const daysUntilWed = (3 - dow + 7) % 7;
  firstWed.setDate(june1.getDate() + daysUntilWed);
  if (firstWed.getTime() < now.getTime()) {
    const nextJune1 = new Date(year + 1, 5, 1);
    const nextDow = nextJune1.getDay();
    const nextDays = (3 - nextDow + 7) % 7;
    firstWed = new Date(nextJune1);
    firstWed.setDate(nextJune1.getDate() + nextDays);
  }
  return firstWed;
}

const MONTH_NAMES = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December'];

// ─── Component ──────────────────────────────────────────────────────────────

interface GCFlagsAPI {
  flags: Record<string, FlagData>;
  flagStudent: (uid: string, note?: string, priority?: FlagPriority) => Promise<void>;
  unflagStudent: (uid: string) => Promise<void>;
  updateFlagNote: (uid: string, note: string) => Promise<void>;
  updateFlagPriority: (uid: string, priority: FlagPriority) => Promise<void>;
  isFlagged: (uid: string) => boolean;
  getFlagData: (uid: string) => FlagData | null;
  flaggedStudentUids: string[];
}

interface GCOverviewProps {
  studentData: GCStudentFullData[];
  allCourses: CourseData[];
  school: string;
  studentNotes: Record<string, { notes: string; updatedAt: string }>;
  onSelectStudent: (uid: string) => void;
  onDeleteStudent?: (user: any) => void;
  onResetPassword?: (studentUid: string) => void;
  alerts?: EarlyWarningAlert[];
  onDismissAlert?: (alert: EarlyWarningAlert) => void;
  gcName?: string;
  gcFlags?: GCFlagsAPI;
}

export const GCOverview: React.FC<GCOverviewProps> = ({ studentData, allCourses, school, studentNotes, onSelectStudent, onDeleteStudent, onResetPassword, alerts = [], onDismissAlert, gcName, gcFlags }) => {
  const [searchQuery, setSearchQuery] = useState('');
  const [showStatusGuide, setShowStatusGuide] = useState(false);
  const [showBroadcastModal, setShowBroadcastModal] = useState(false);
  const [showExportModal, setShowExportModal] = useState(false);
  const [broadcastMessage, setBroadcastMessage] = useState('');
  const [isBroadcasting, setIsBroadcasting] = useState(false);
  const [statusFilter, setStatusFilter] = useState<StatusFilter>('all');
  const [sortKey, setSortKey] = useState<SortKey>('name');
  const [sortDir, setSortDir] = useState<SortDir>('asc');
  const [flagPopoverUid, setFlagPopoverUid] = useState<string | null>(null);
  const [flagNote, setFlagNote] = useState('');
  const [flagPriority, setFlagPriority] = useState<FlagPriority>('normal');
  const flagPopoverRef = useRef<HTMLDivElement>(null);

  // ─── Computed stats ─────────────────────────────────────────────────────

  const studentStats = useMemo(() => {
    return studentData.map(s => ({
      student: s,
      progress: getOverallProgress(s.progress, allCourses),
      status: getStudentStatus(s, allCourses),
      currentCAO: getStudentCurrentCAO(s),
      targetCAO: getStudentTargetCAO(s),
      streak: s.streak?.currentStreak ?? 0,
      activeThisWeek: isActiveThisWeek(s),
    }));
  }, [studentData, allCourses]);

  const avgProgress = studentStats.length > 0
    ? studentStats.reduce((sum, s) => sum + s.progress, 0) / studentStats.length
    : 0;

  const driftingCount = studentStats.filter(s => s.status === 'drifting').length;
  const atRiskCount = studentStats.filter(s => s.status === 'at-risk').length;
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
    studentStats.filter(s => s.status === 'at-risk' || s.status === 'drifting').forEach(addStudent);
    // Flagged (may overlap)
    if (gcFlags) {
      gcFlags.flaggedStudentUids.forEach(uid => {
        const s = studentStats.find(ss => ss.student.user.uid === uid);
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
  }, [studentStats, gcFlags]);

  const needsAttentionCount = attentionStudents.length;
  // Count only-flagged students (flagged but NOT at-risk/drifting)
  const flaggedOnlyCount = attentionStudents.filter(s => s.flag && s.status !== 'at-risk' && s.status !== 'drifting').length;

  const _avgCurrentCAO = studentStats.length > 0
    ? Math.round(studentStats.filter(s => s.student.subjectProfile).reduce((sum, s) => sum + s.currentCAO, 0) / Math.max(1, studentStats.filter(s => s.student.subjectProfile).length))
    : 0;

  const _activeThisWeekCount = studentStats.filter(s => s.activeThisWeek).length;

  // Status counts for filter pills
  const statusCounts = useMemo(() => {
    const counts: Record<string, number> = { all: studentStats.length };
    studentStats.forEach(s => { counts[s.status] = (counts[s.status] ?? 0) + 1; });
    counts['flagged'] = flaggedCount;
    counts['needs-attention'] = needsAttentionCount;
    return counts;
  }, [studentStats, flaggedCount, needsAttentionCount]);
  const daysUntilLC = getDaysUntilLC();
  const distribution = getProgressDistribution(studentData, allCourses);
  const distributionTotal = Math.max(1, distribution.reduce((a, b) => a + b, 0));
  const distributionMax = Math.max(1, ...distribution);

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

  const recentlyActive = useMemo(() => getRecentlyActiveStudents(studentData), [studentData]);

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
    studentData.forEach(s => {
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
  }, [studentData, activityRange]);

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

    studentData.forEach(s => {
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
  }, [studentData]);

  // ─── Filter + Sort ──────────────────────────────────────────────────────

  const filtered = useMemo(() => {
    let result = studentStats;
    if (searchQuery) {
      const q = searchQuery.toLowerCase();
      result = result.filter(s => s.student.user.name.toLowerCase().includes(q));
    }
    if (statusFilter === 'flagged') {
      result = result.filter(s => gcFlags?.isFlagged(s.student.user.uid));
    } else if (statusFilter === 'needs-attention') {
      result = result.filter(s => s.status === 'drifting' || s.status === 'at-risk' || gcFlags?.isFlagged(s.student.user.uid));
    } else if (statusFilter !== 'all') {
      result = result.filter(s => s.status === statusFilter);
    }
    result.sort((a, b) => {
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
        case 'cao-current': cmp = a.currentCAO - b.currentCAO; break;
        case 'cao-target': cmp = a.targetCAO - b.targetCAO; break;
        case 'gap': cmp = (a.targetCAO - a.currentCAO) - (b.targetCAO - b.currentCAO); break;
        case 'streak': cmp = a.streak - b.streak; break;
      }
      return sortDir === 'desc' ? -cmp : cmp;
    });
    return result;
  }, [studentStats, searchQuery, statusFilter, sortKey, sortDir, gcFlags]);

  const handleSort = (key: SortKey) => {
    if (sortKey === key) {
      setSortDir(d => d === 'asc' ? 'desc' : 'asc');
    } else {
      setSortKey(key);
      setSortDir(key === 'name' ? 'asc' : 'desc');
    }
  };

  const sortIndicator = (key: SortKey) => {
    if (sortKey !== key) return null;
    return sortDir === 'asc' ? ' \u2191' : ' \u2193';
  };

  // ─── Status pill helper ─────────────────────────────────────────────────

  const STATUS_ICONS: Record<StudentStatus, React.ElementType> = {
    'new': UserPlus, 'at-risk': AlertTriangle, 'drifting': TrendingDown,
    'thriving': TrendingUp, 'active': CheckCircle, 'inactive': MinusCircle,
  };

  const statusPill = (status: StudentStatus) => {
    const cfg = STATUS_CONFIG[status];
    const Icon = STATUS_ICONS[status];
    return (
      <span
        className={`inline-flex items-center gap-1.5 px-2.5 py-1 rounded-lg text-xs font-medium ${cfg.darkBgClass} ${cfg.darkTextClass}`}
        style={{ backgroundColor: cfg.bg, color: cfg.text }}
        aria-label={`Status: ${cfg.label}`}
      >
        <Icon size={12} aria-hidden="true" />
        {cfg.label}
      </span>
    );
  };

  // ─── CAO gap pill ─────────────────────────────────────────────────────

  const gapPill = (gap: number) => {
    const absGap = Math.abs(gap);
    let pillClass = 'bg-emerald-50 text-emerald-700 dark:bg-emerald-900/20 dark:text-emerald-400';
    if (absGap > 100) {
      pillClass = 'bg-rose-50 text-rose-700 dark:bg-rose-900/20 dark:text-rose-400';
    } else if (absGap > 50) {
      pillClass = 'bg-amber-50 text-amber-700 dark:bg-amber-900/20 dark:text-amber-400';
    }
    return (
      <span className={`inline-flex px-2 py-0.5 rounded-md text-xs font-semibold ${pillClass}`}>
        {gap > 0 ? '+' : ''}{gap}
      </span>
    );
  };

  // ─── Subject Gaps ──────────────────────────────────────────────────────

  const subjectGaps = useMemo(() => getSubjectGaps(studentData), [studentData]);
  const topGaps = subjectGaps.slice(0, 8);
  const maxAvgGap = topGaps.length > 0 ? Math.max(...topGaps.map(g => g.avgGap)) : 1;

  // ─── CSV Export ────────────────────────────────────────────────────────

  const handleExportCSV = () => {
    const csv = generateStudentCSV(studentData, allCourses);
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

  // ─── Calendar widget data ─────────────────────────────────────────────

  const now = new Date();
  const [calMonth, setCalMonth] = useState(now.getMonth());
  const [calYear, setCalYear] = useState(now.getFullYear());
  const calendarDays = getCalendarDays(calYear, calMonth);
  const todayDate = now.getDate();
  const isCurrentMonth = calYear === now.getFullYear() && calMonth === now.getMonth();
  const lcExamDate = getLCExamDate();
  const lcDay = lcExamDate.getMonth() === calMonth && lcExamDate.getFullYear() === calYear
    ? lcExamDate.getDate()
    : null;

  const handleCalPrev = () => {
    if (calMonth === 0) { setCalMonth(11); setCalYear(y => y - 1); }
    else setCalMonth(m => m - 1);
  };
  const handleCalNext = () => {
    if (calMonth === 11) { setCalMonth(0); setCalYear(y => y + 1); }
    else setCalMonth(m => m + 1);
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
    }).catch(() => {});
    return () => { cancelled = true; };
  }, [school]);

  // Map events to calendar days for the current month
  const eventsByDay = useMemo(() => {
    const map: Record<number, SchoolEvent[]> = {};
    for (const ev of schoolEvents) {
      const d = new Date(ev.date);
      if (d.getMonth() === calMonth && d.getFullYear() === calYear) {
        const day = d.getDate();
        if (!map[day]) map[day] = [];
        map[day].push(ev);
      }
    }
    return map;
  }, [schoolEvents, calMonth, calYear]);

  const EVENT_DOT_COLORS: Record<string, string> = {
    exams: '#EF4444',
    deadlines: '#F59E0B',
    school: '#3B82F6',
    other: '#8B5CF6',
  };

  // ─── Flag popover helpers ────────────────────────────────────────────────

  const openFlagPopover = (uid: string, e: React.MouseEvent) => {
    e.stopPropagation();
    const existing = gcFlags?.getFlagData(uid);
    setFlagNote(existing?.note ?? '');
    setFlagPriority(existing?.priority ?? 'normal');
    setFlagPopoverUid(uid);
  };

  // Close flag popover on outside click or Escape
  React.useEffect(() => {
    if (!flagPopoverUid) return;
    const handleClick = (e: MouseEvent) => {
      if (flagPopoverRef.current && !flagPopoverRef.current.contains(e.target as Node)) {
        setFlagPopoverUid(null);
      }
    };
    const handleKey = (e: KeyboardEvent) => {
      if (e.key === 'Escape') setFlagPopoverUid(null);
    };
    document.addEventListener('mousedown', handleClick);
    document.addEventListener('keydown', handleKey);
    return () => {
      document.removeEventListener('mousedown', handleClick);
      document.removeEventListener('keydown', handleKey);
    };
  }, [flagPopoverUid]);

  // ─── Render ─────────────────────────────────────────────────────────────

  const hour = new Date().getHours();
  const greeting = hour < 12 ? 'Good morning.' : hour < 18 ? 'Good afternoon.' : 'Good evening.';

  return (
    <div className="p-6 lg:p-8 space-y-5">
      {/* ═══════════════════════════════════════════════════════════════════
          ROW 0 — Header (full width)
          ═══════════════════════════════════════════════════════════════════ */}
      <div id="gc-overview" className="flex flex-col sm:flex-row sm:items-end sm:justify-between gap-4">
        <div>
          <p className={`text-[11px] font-medium uppercase tracking-widest ${TEXT_NEUTRAL_DARK}`} style={{ color: NEUTRAL_GREY }}>Guidance Dashboard</p>
          <h1 className="font-serif text-3xl font-semibold text-zinc-900 dark:text-white tracking-tight">{greeting}</h1>
          <p className={`text-sm mt-0.5 ${TEXT_NEUTRAL_DARK}`} style={{ color: NEUTRAL_GREY }}>{getSchoolName(school)}</p>
        </div>
        <div className="flex items-center gap-3">
          <div className="flex items-center gap-2 px-3 py-1.5 rounded-xl dark:!bg-[rgba(77,184,164,0.1)] dark:!border-[rgba(77,184,164,0.25)]" style={{ backgroundColor: 'rgba(42,125,111,0.08)', border: '1px solid rgba(42,125,111,0.2)' }}>
            <span className={`text-lg font-bold ${TEXT_ACCENT_DARK}`} style={{ color: ACCENT }}>{daysUntilLC}</span>
            <span className="text-[10px] font-bold uppercase tracking-wider dark:!text-[rgba(77,184,164,0.7)]" style={{ color: 'rgba(42,125,111,0.7)' }}>days to LC</span>
          </div>
          <button
            onClick={() => setShowExportModal(true)}
            className={`flex items-center gap-1.5 px-3.5 py-2 rounded-xl text-xs font-semibold transition-colors ${TEXT_ACCENT_DARK} dark:!border-[rgba(77,184,164,0.3)]`}
            style={{ color: ACCENT, border: '1px solid rgba(42,125,111,0.3)', backgroundColor: 'transparent' }}
          >
            <FileDown size={14} />
            Export
          </button>
          <button
            onClick={() => setShowBroadcastModal(true)}
            className={`flex items-center gap-1.5 px-3.5 py-2 rounded-xl text-xs font-semibold transition-colors ${TEXT_ACCENT_DARK} dark:!border-[rgba(77,184,164,0.3)]`}
            style={{ color: ACCENT, border: '1px solid rgba(42,125,111,0.3)', backgroundColor: 'transparent' }}
          >
            <Megaphone size={14} />
            Broadcast to Class
          </button>
        </div>
      </div>

      {/* Broadcast Modal */}
      <AnimatePresence>
        {showBroadcastModal && (
          <div className="fixed inset-0 z-[200] flex items-center justify-center bg-black/50 backdrop-blur-sm p-4" onClick={() => !isBroadcasting && setShowBroadcastModal(false)}>
            <MotionDiv
              initial={{ opacity: 0, scale: 0.95 }}
              animate={{ opacity: 1, scale: 1 }}
              exit={{ opacity: 0, scale: 0.95 }}
              className="bg-white dark:bg-zinc-900 rounded-2xl border border-zinc-200 dark:border-zinc-800 p-6 max-w-sm w-full shadow-2xl"
              onClick={(e: React.MouseEvent) => e.stopPropagation()}
            >
              <div className="flex items-center gap-3 mb-4">
                <div className="w-10 h-10 rounded-xl flex items-center justify-center dark:!bg-[rgba(77,184,164,0.1)]" style={{ backgroundColor: 'rgba(42,125,111,0.1)' }}>
                  <Megaphone size={20} style={{ color: ACCENT }} className={TEXT_ACCENT_DARK} />
                </div>
                <div>
                  <h3 className="text-sm font-semibold text-zinc-800 dark:text-white">Broadcast Message</h3>
                  <p className="text-xs text-zinc-500">Send to all {studentData.length} students</p>
                </div>
              </div>
              <textarea
                value={broadcastMessage}
                onChange={(e) => setBroadcastMessage(e.target.value)}
                placeholder="Write a message to all your students..."
                maxLength={300}
                className="w-full bg-zinc-50 dark:bg-zinc-800/50 border border-zinc-200 dark:border-zinc-700 rounded-xl p-3 text-sm text-zinc-800 dark:text-white placeholder:text-zinc-400 resize-none h-28 focus:outline-none focus:border-[rgba(42,125,111,0.5)] mb-1"
              />
              <p className="text-[10px] text-zinc-400 text-right mb-3">{broadcastMessage.length}/300</p>
              <div className="flex gap-2">
                <button onClick={() => setShowBroadcastModal(false)} className="flex-1 py-2 rounded-xl text-sm font-medium text-zinc-500 hover:bg-zinc-100 dark:hover:bg-zinc-800 transition-colors">
                  Cancel
                </button>
                <button
                  onClick={async () => {
                    if (!broadcastMessage.trim()) return;
                    setIsBroadcasting(true);
                    const uids = studentData.map(s => s.user.uid);
                    await addNotificationToMultiple(uids, {
                      type: 'gc-broadcast',
                      title: 'Message from your Guidance Counsellor',
                      body: broadcastMessage.trim(),
                      fromGCName: gcName,
                      severity: 'info',
                    });
                    setIsBroadcasting(false);
                    setShowBroadcastModal(false);
                    setBroadcastMessage('');
                  }}
                  disabled={!broadcastMessage.trim() || isBroadcasting}
                  className="flex-1 py-2 rounded-xl text-sm font-medium text-white disabled:opacity-50 disabled:cursor-not-allowed transition-colors dark:!bg-[#4DB8A4]"
                  style={{ backgroundColor: ACCENT }}
                >
                  {isBroadcasting ? 'Sending...' : 'Send to All'}
                </button>
              </div>
            </MotionDiv>
          </div>
        )}
      </AnimatePresence>

      {/* ─── Early Warning Alerts ──────────────────────────────────────── */}
      {alerts.length > 0 && (
        <MotionDiv
          initial={{ opacity: 0, y: 12 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.5, ease: CUSTOM_EASE }}
          className="rounded-2xl bg-white dark:bg-zinc-900 border border-zinc-200/60 dark:border-zinc-800/60 shadow-[0_1px_3px_rgba(0,0,0,0.04)] overflow-hidden"
        >
          {/* Alert header */}
          <div className="flex items-center justify-between px-5 py-3.5 border-b border-zinc-100 dark:border-zinc-800/60">
            <div className="flex items-center gap-2.5">
              <AlertCircle size={16} className="text-rose-500" />
              <span className="text-sm font-semibold text-zinc-800 dark:text-white">Early Warning Signals</span>
            </div>
            <div className="flex items-center gap-3 text-[10px] font-bold uppercase tracking-wider">
              {(() => {
                const urgent = alerts.filter(a => a.severity === 'urgent').length;
                const watch = alerts.filter(a => a.severity === 'watch').length;
                const nudge = alerts.filter(a => a.severity === 'nudge').length;
                return (
                  <>
                    {urgent > 0 && <span className="text-rose-500">{urgent} Urgent</span>}
                    {watch > 0 && <span className="text-amber-500">{watch} Watch</span>}
                    {nudge > 0 && <span className="text-blue-500">{nudge} Nudge</span>}
                  </>
                );
              })()}
            </div>
          </div>

          {/* Alert cards */}
          <div className="divide-y divide-zinc-100 dark:divide-zinc-800/40">
            {alerts.map((alert) => {
              const severityConfig: Record<AlertSeverity, { dot: string; bg: string }> = {
                urgent: { dot: 'bg-rose-500', bg: 'bg-rose-50/50 dark:bg-rose-500/5' },
                watch: { dot: 'bg-amber-500', bg: 'bg-amber-50/50 dark:bg-amber-500/5' },
                nudge: { dot: 'bg-blue-500', bg: 'bg-blue-50/50 dark:bg-blue-500/5' },
              };
              const cfg = severityConfig[alert.severity];

              return (
                <div
                  key={alert.id}
                  className={`flex items-center gap-4 px-5 py-3 ${cfg.bg} transition-colors`}
                >
                  {/* Severity dot + Avatar */}
                  <div className={`w-2 h-2 rounded-full shrink-0 ${cfg.dot}`} />
                  <img
                    src={getAvatarUrl(alert.studentAvatar)}
                    alt=""
                    className="w-8 h-8 rounded-lg bg-zinc-200 dark:bg-zinc-700 shrink-0"
                  />

                  {/* Info */}
                  <div className="flex-1 min-w-0">
                    <div className="flex items-center gap-2">
                      <span className="text-sm font-semibold text-zinc-800 dark:text-white truncate">{alert.studentName}</span>
                      <span className="text-zinc-300 dark:text-zinc-600">&middot;</span>
                      <span className="text-xs font-medium text-zinc-500 dark:text-zinc-400 truncate">{alert.title}</span>
                    </div>
                    <p className="text-[11px] text-zinc-400 dark:text-zinc-500 mt-0.5 truncate">{alert.description}</p>
                  </div>

                  {/* Actions */}
                  <div className="flex items-center gap-1.5 shrink-0">
                    <button
                      onClick={() => onSelectStudent(alert.studentUid)}
                      className="px-2.5 py-1.5 rounded-lg text-[10px] font-semibold text-zinc-600 dark:text-zinc-300 hover:bg-zinc-100 dark:hover:bg-zinc-800 transition-colors"
                    >
                      <Eye size={12} className="inline mr-1" />
                      View
                    </button>
                    {onDismissAlert && (
                      <button
                        onClick={() => onDismissAlert(alert)}
                        className="p-1.5 rounded-lg text-zinc-400 hover:text-zinc-600 dark:hover:text-zinc-300 hover:bg-zinc-100 dark:hover:bg-zinc-800 transition-colors"
                        title="Dismiss (will resurface if situation worsens)"
                      >
                        <X size={12} />
                      </button>
                    )}
                  </div>
                </div>
              );
            })}
          </div>
        </MotionDiv>
      )}

      {/* ═══════════════════════════════════════════════════════════════════
          ROW 1 — 4 Stat Cards (full width, 4 equal columns)
          ═══════════════════════════════════════════════════════════════════ */}
      <div className="grid grid-cols-3 gap-4">
        {[
          { label: 'Total Students', value: String(studentData.length), trend: null as number | null },
          { label: 'Avg Progress', value: `${avgProgress.toFixed(0)}%`, trend: null },
          { label: 'Blocks This Week', value: String(weeklyTrends.blocksThisWeek), trend: weeklyTrends.blocksTrend },
        ].map((kpi, i) => (
          <MotionDiv
            key={kpi.label}
            initial={{ opacity: 0, y: 12 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.5, delay: i * 0.04, ease: CUSTOM_EASE }}
            className={CARD_STYLE_DARK_CLASS}
            style={CARD_STYLE}
          >
            <p className={`text-[11px] font-medium uppercase tracking-widest mb-2 ${TEXT_NEUTRAL_DARK}`} style={{ color: NEUTRAL_GREY }}>{kpi.label}</p>
            <p className="text-3xl font-medium text-zinc-900 dark:text-white">{kpi.value}</p>
            {kpi.trend !== null ? (
              <div className={`flex items-center gap-1 mt-2 text-xs font-medium ${kpi.trend >= 0 ? 'dark:!text-[#8AB592]' : 'dark:!text-[#D4A95C]'}`} style={{ color: kpi.trend >= 0 ? SAGE : WARM_AMBER }}>
                {kpi.trend >= 0 ? <TrendingUp size={12} /> : <TrendingDown size={12} />}
                <span>{kpi.trend > 0 ? '+' : ''}{kpi.trend}% vs last week</span>
              </div>
            ) : (
              <div className="mt-2 h-4" />
            )}
          </MotionDiv>
        ))}
      </div>

      {/* ═══════════════════════════════════════════════════════════════════
          Unified Attention Section
          ═══════════════════════════════════════════════════════════════════ */}
      <MotionDiv
        initial={{ opacity: 0, y: 12 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.5, delay: 0.14, ease: CUSTOM_EASE }}
        className={CARD_STYLE_DARK_CLASS}
        style={CARD_STYLE}
      >
        <div className="flex items-start justify-between mb-1">
          <p className={`text-[11px] font-medium uppercase tracking-widest ${TEXT_NEUTRAL_DARK}`} style={{ color: NEUTRAL_GREY }}>Attention</p>
          {needsAttentionCount > 0 && (
            <p className={`text-3xl font-medium dark:!text-[#D4A95C]`} style={{ color: WARM_AMBER }}>{needsAttentionCount}</p>
          )}
        </div>

        {needsAttentionCount === 0 ? (
          <div className="text-center py-8">
            <Sparkles size={24} className="mx-auto mb-2" style={{ color: ACCENT }} />
            <p className="text-sm font-medium text-zinc-700 dark:text-zinc-300">All students are engaged</p>
            <p className={`text-xs mt-0.5 ${TEXT_NEUTRAL_DARK}`} style={{ color: NEUTRAL_GREY }}>No students drifting, at risk, or flagged</p>
          </div>
        ) : (
          <>
            <p className={`text-xs mb-5 ${TEXT_NEUTRAL_DARK}`} style={{ color: NEUTRAL_GREY }}>
              {[
                driftingCount > 0 && `${driftingCount} drifting`,
                atRiskCount > 0 && `${atRiskCount} at risk`,
                flaggedOnlyCount > 0 && `${flaggedOnlyCount} flagged`,
              ].filter(Boolean).join(' · ')}
            </p>
            <div className="space-y-1">
              {attentionStudents.map(({ student, status, flag, daysSince }) => {
                const stCfg = STATUS_CONFIG[status];
                const StatusIcon = STATUS_ICONS[status];
                return (
                  <button
                    key={student.user.uid}
                    onClick={() => onSelectStudent(student.user.uid)}
                    className="w-full flex items-center gap-3 px-3 py-2.5 rounded-lg hover:bg-zinc-50 dark:hover:bg-zinc-800/40 transition-colors text-left"
                    aria-label={`View ${student.user.name}, status: ${stCfg.label}${flag ? ', flagged' : ''}`}
                  >
                    <img src={getAvatarUrl(student.user.avatar)} alt="" className="w-8 h-8 rounded-full bg-zinc-200 dark:bg-zinc-700 shrink-0" />
                    <span className="text-sm font-medium text-zinc-800 dark:text-white truncate flex-1">{student.user.name}</span>
                    <span
                      className={`inline-flex items-center gap-1 px-2 py-0.5 rounded-md text-[10px] font-semibold shrink-0 ${stCfg.darkBgClass} ${stCfg.darkTextClass}`}
                      style={{ backgroundColor: stCfg.bg, color: stCfg.text }}
                      aria-label={`Status: ${stCfg.label}`}
                    >
                      <StatusIcon size={10} />
                      {stCfg.label}
                    </span>
                    {flag && (
                      <Flag
                        size={12}
                        fill={flag.priority === 'high' ? '#D97706' : ACCENT}
                        style={{ color: flag.priority === 'high' ? '#D97706' : ACCENT }}
                        className="shrink-0"
                        aria-label={`Flagged: ${flag.priority} priority`}
                      />
                    )}
                    <span className={`text-[10px] shrink-0 whitespace-nowrap ${TEXT_NEUTRAL_DARK}`} style={{ color: NEUTRAL_GREY }}>
                      {daysSince === Infinity ? 'No sessions' : daysSince === 0 ? 'Today' : daysSince === 1 ? '1 day ago' : `${daysSince}d ago`}
                    </span>
                  </button>
                );
              })}
            </div>
          </>
        )}
      </MotionDiv>

      {/* ═══════════════════════════════════════════════════════════════════
          ROW 2+ — 2-column 1fr 1fr grid
          ═══════════════════════════════════════════════════════════════════ */}
      <div id="gc-analytics" className="grid grid-cols-1 lg:grid-cols-2 gap-4">

        {/* ─── ROW 2 LEFT: Daily Activity ──────────────────────────────── */}
        <DailyActivityChart
          aggregatedActivity={aggregatedActivity}
          activityRange={activityRange}
          onRangeChange={setActivityRange}
        />

        {/* ─── ROW 2 RIGHT: Key Dates & Events ───────────────────────── */}
        <GCKeyEvents school={school} />

        {/* ─── Recently Active (full width) ──── */}
        <div className={CARD_STYLE_DARK_CLASS} style={{ ...CARD_STYLE, gridColumn: '1 / -1' }}>
          <p className={`text-[11px] font-medium uppercase tracking-widest ${TEXT_NEUTRAL_DARK}`} style={{ color: NEUTRAL_GREY }}>Activity</p>
          <p className="text-lg font-medium text-zinc-900 dark:text-white mt-0.5 mb-4">Recently Active</p>
          {recentlyActive.length === 0 ? (
            <p className="text-sm text-zinc-400 italic">No recent activity.</p>
          ) : (
            <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-2">
              {recentlyActive.map(s => (
                <button
                  key={s.uid}
                  onClick={() => onSelectStudent(s.uid)}
                  className="flex items-center gap-3 p-2 rounded-lg hover:bg-zinc-50 dark:hover:bg-zinc-800/40 transition-colors text-left"
                >
                  <img src={getAvatarUrl(s.avatar)} alt="" className="w-8 h-8 rounded-full bg-zinc-200 shrink-0" />
                  <div className="min-w-0 flex-1">
                    <p className="text-sm font-medium text-zinc-800 dark:text-white truncate">{s.name}</p>
                    <p className={`text-[10px] ${TEXT_NEUTRAL_DARK}`} style={{ color: NEUTRAL_GREY }}>
                      {s.blocksCompletedToday > 0 ? `${s.blocksCompletedToday} blocks today` : 'No blocks today'}
                    </p>
                  </div>
                  <span className={`text-[10px] shrink-0 ${TEXT_NEUTRAL_DARK}`} style={{ color: NEUTRAL_GREY }}>{s.timeAgo}</span>
                </button>
              ))}
            </div>
          )}
        </div>

        {/* ─── Exam Calendar (left) ────────────────────────────── */}
        <div className={CARD_STYLE_DARK_CLASS} style={CARD_STYLE}>
          <div className="flex items-start justify-between mb-5">
            <div>
              <p className={`text-[11px] font-medium uppercase tracking-widest ${TEXT_NEUTRAL_DARK}`} style={{ color: NEUTRAL_GREY }}>Countdown</p>
              <p className="text-lg font-medium text-zinc-900 dark:text-white mt-0.5">Exam Calendar</p>
            </div>
            <div className="text-right">
              <p className={`text-3xl font-bold ${TEXT_ACCENT_DARK}`} style={{ color: ACCENT }}>{daysUntilLC}</p>
              <p className={`text-[10px] ${TEXT_NEUTRAL_DARK}`} style={{ color: NEUTRAL_GREY }}>days</p>
            </div>
          </div>
          {/* Month navigation */}
          <div className="flex items-center justify-between mb-3">
            <button onClick={handleCalPrev} className="p-1 rounded-lg hover:bg-zinc-100 dark:hover:bg-zinc-800 transition-colors">
              <ChevronLeft size={16} style={{ color: NEUTRAL_GREY }} className={TEXT_NEUTRAL_DARK} />
            </button>
            <span className="text-xs font-medium text-zinc-600 dark:text-zinc-400">{MONTH_NAMES[calMonth]} {calYear}</span>
            <button onClick={handleCalNext} className="p-1 rounded-lg hover:bg-zinc-100 dark:hover:bg-zinc-800 transition-colors">
              <ChevronRight size={16} style={{ color: NEUTRAL_GREY }} className={TEXT_NEUTRAL_DARK} />
            </button>
          </div>
          {/* Day-of-week headers */}
          <div className="grid grid-cols-7 gap-1 mb-1">
            {['M', 'T', 'W', 'T', 'F', 'S', 'S'].map((d, i) => (
              <span key={i} className={`text-center text-[9px] font-medium ${TEXT_NEUTRAL_DARK}`} style={{ color: NEUTRAL_GREY }}>{d}</span>
            ))}
          </div>
          {/* Calendar grid */}
          <div className="grid grid-cols-7 gap-1">
            {calendarDays.map((cell, i) => {
              if (!cell.isCurrentMonth) {
                return <div key={i} className="aspect-square" />;
              }
              const isToday = isCurrentMonth && cell.day === todayDate;
              const isLC = lcDay !== null && cell.day === lcDay;
              const dayEvents = eventsByDay[cell.day] || [];

              return (
                <div
                  key={i}
                  className={`aspect-square flex flex-col items-center justify-center text-[11px] font-medium relative group ${
                    !isToday && !isLC ? 'text-zinc-600 dark:text-zinc-400' : 'text-white rounded-lg'
                  } ${dayEvents.length > 0 ? 'cursor-pointer' : ''}`}
                  style={isToday ? { backgroundColor: ACCENT } : isLC ? { backgroundColor: '#DC2626' } : undefined}
                >
                  {cell.day}
                  {dayEvents.length > 0 && (
                    <>
                      <div className="flex gap-0.5 absolute bottom-1">
                        {dayEvents.slice(0, 3).map((ev, j) => (
                          <div key={j} className="w-2.5 h-2.5 rounded-full" style={{ backgroundColor: EVENT_DOT_COLORS[ev.category] || '#8B5CF6' }} />
                        ))}
                      </div>
                      <div className="absolute bottom-full left-1/2 -translate-x-1/2 mb-1 hidden group-hover:block z-50">
                        <div className="bg-zinc-800 text-white text-[10px] font-medium rounded-lg px-2.5 py-1.5 whitespace-nowrap shadow-lg border border-zinc-700">
                          {dayEvents.map((ev, j) => (
                            <div key={j} className="flex items-center gap-1.5">
                              <div className="w-2.5 h-2.5 rounded-full shrink-0" style={{ backgroundColor: EVENT_DOT_COLORS[ev.category] || '#8B5CF6' }} />
                              {ev.title}
                            </div>
                          ))}
                        </div>
                      </div>
                    </>
                  )}
                </div>
              );
            })}
          </div>
          {/* Legend */}
          <div className={`flex flex-wrap gap-3 mt-3 text-[10px] ${TEXT_NEUTRAL_DARK}`} style={{ color: NEUTRAL_GREY }}>
            <div className="flex items-center gap-1.5">
              <div className="w-3 h-3 rounded" style={{ backgroundColor: ACCENT }} />
              <span>Today</span>
            </div>
            {lcDay !== null && (
              <div className="flex items-center gap-1.5">
                <div className="w-3 h-3 rounded bg-red-600" />
                <span>LC Exam</span>
              </div>
            )}
            {schoolEvents.length > 0 && (
              <>
                <div className="flex items-center gap-1.5"><div className="w-2.5 h-2.5 rounded-full" style={{ backgroundColor: '#EF4444' }} /><span>Exams</span></div>
                <div className="flex items-center gap-1.5"><div className="w-2.5 h-2.5 rounded-full" style={{ backgroundColor: '#F59E0B' }} /><span>Deadlines</span></div>
                <div className="flex items-center gap-1.5"><div className="w-2.5 h-2.5 rounded-full" style={{ backgroundColor: '#3B82F6' }} /><span>School</span></div>
                <div className="flex items-center gap-1.5"><div className="w-2.5 h-2.5 rounded-full" style={{ backgroundColor: '#8B5CF6' }} /><span>Other</span></div>
              </>
            )}
          </div>
        </div>

        {/* ─── Progress Breakdown (right, same row as calendar) ────── */}
        <MotionDiv
          initial={{ opacity: 0, y: 12 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.5, delay: 0.25, ease: CUSTOM_EASE }}
          className={CARD_STYLE_DARK_CLASS}
          style={{ ...CARD_STYLE, display: 'flex', flexDirection: 'column' }}
        >
          <div className="flex items-baseline justify-between mb-5">
            <div>
              <p className={`text-[11px] font-medium uppercase tracking-widest ${TEXT_NEUTRAL_DARK}`} style={{ color: NEUTRAL_GREY }}>Distribution</p>
              <p className="text-lg font-medium text-zinc-900 dark:text-white mt-0.5">Progress Breakdown</p>
            </div>
            <span className={`text-xs font-medium ${TEXT_NEUTRAL_DARK}`} style={{ color: NEUTRAL_GREY }}>{distributionTotal} students</span>
          </div>
          <div className="flex gap-4 flex-1 items-end">
            {distribution.map((count, i) => {
              const heightPct = (count / distributionMax) * 100;
              const bucketLabels = ['0-25%', '25-50%', '50-75%', '75-100%'];
              return (
                <div key={i} className="flex-1 flex flex-col items-center gap-1.5 h-full justify-end">
                  <span className="text-sm font-medium text-zinc-600 dark:text-zinc-300">{count}</span>
                  <div className="w-full relative flex-1 min-h-[200px]">
                    {count > 0 ? (
                      <MotionDiv
                        className="absolute bottom-0 left-1 right-1 rounded-lg"
                        style={{ backgroundColor: ACCENT }}
                        initial={{ height: 0 }}
                        animate={{ height: `${Math.max(heightPct, 8)}%` }}
                        transition={{ duration: 0.6, delay: 0.3 + i * 0.1, ease: CUSTOM_EASE }}
                      />
                    ) : (
                      <div className="absolute bottom-0 left-1 right-1 h-[2px] rounded-full bg-zinc-200 dark:bg-zinc-700" />
                    )}
                  </div>
                  <span className={`text-xs ${TEXT_NEUTRAL_DARK}`} style={{ color: NEUTRAL_GREY }}>{bucketLabels[i]}</span>
                </div>
              );
            })}
          </div>
        </MotionDiv>

        {/* ─── Subject-Level Gaps (full width span) ───────────── */}
        {topGaps.length > 0 && (
          <MotionDiv
            initial={{ opacity: 0, y: 12 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.5, delay: 0.3, ease: CUSTOM_EASE }}
            className={CARD_STYLE_DARK_CLASS}
            style={{ ...CARD_STYLE, gridColumn: '1 / -1' }}
          >
            <p className={`text-[11px] font-medium uppercase tracking-widest ${TEXT_NEUTRAL_DARK}`} style={{ color: NEUTRAL_GREY }}>Subject Analysis</p>
            <p className="text-lg font-medium text-zinc-900 dark:text-white mt-0.5 mb-4">Subject-Level Gaps</p>
            <div className="space-y-2.5">
              {topGaps.map((gap, i) => {
                const barPct = (gap.avgGap / maxAvgGap) * 100;
                return (
                  <div key={gap.subjectName} className="flex items-center gap-3">
                    <span className="text-xs font-medium text-zinc-700 dark:text-zinc-300 w-32 truncate shrink-0">{gap.subjectName}</span>
                    <div className={`flex-1 h-4 rounded-full overflow-hidden ${TRACK_BG_DARK}`} style={{ backgroundColor: TRACK_BG }}>
                      <MotionDiv
                        className="h-full rounded-full"
                        style={{ backgroundColor: ACCENT }}
                        initial={{ width: 0 }}
                        animate={{ width: `${barPct}%` }}
                        transition={{ duration: 0.5, delay: 0.35 + i * 0.05, ease: CUSTOM_EASE }}
                      />
                    </div>
                    <span className="text-xs font-bold text-zinc-600 dark:text-zinc-300 w-20 text-right shrink-0">
                      {gap.avgGap} pts <span className={`font-normal ${TEXT_NEUTRAL_DARK}`} style={{ color: NEUTRAL_GREY }}>({gap.studentCount})</span>
                    </span>
                  </div>
                );
              })}
            </div>
          </MotionDiv>
        )}
      </div>

      {/* ═══════════════════════════════════════════════════════════════════
          Subject Health (full width)
          ═══════════════════════════════════════════════════════════════════ */}
      <SubjectHealthPanel studentData={studentData} />

      {/* ═══════════════════════════════════════════════════════════════════
          Student Table — DO NOT CHANGE
          ═══════════════════════════════════════════════════════════════════ */}
      <div id="gc-students" className="rounded-2xl bg-white dark:bg-zinc-900 border border-zinc-200/60 dark:border-zinc-800/60 shadow-[0_1px_3px_rgba(0,0,0,0.04)] hover:shadow-[0_4px_12px_rgba(0,0,0,0.06)] transition-shadow overflow-hidden">
        {/* Table Controls */}
        <div className="p-5 border-b border-zinc-100 dark:border-zinc-800 space-y-3">
          <div className="flex flex-col sm:flex-row gap-3">
            <div className="relative flex-1">
              <Search size={16} className="absolute left-3.5 top-1/2 -translate-y-1/2 text-zinc-400 dark:text-zinc-500" />
              <input
                type="text"
                value={searchQuery}
                onChange={(e) => setSearchQuery(e.target.value)}
                placeholder="Search students..."
                className="w-full bg-zinc-50 dark:bg-zinc-800/50 border border-zinc-200 dark:border-zinc-700 rounded-xl py-2.5 pl-10 pr-4 text-zinc-900 dark:text-white text-sm placeholder:text-zinc-400 dark:placeholder:text-zinc-500 focus:outline-none focus:border-[rgba(42,125,111,0.5)] transition-colors"
              />
            </div>
            <button
              onClick={() => setShowStatusGuide(prev => !prev)}
              className="flex items-center gap-2 px-4 py-2.5 rounded-xl text-sm font-medium transition-colors text-zinc-400 dark:text-zinc-500 hover:text-zinc-600 dark:hover:text-zinc-300 border border-zinc-200 dark:border-zinc-700"
            >
              <AlertCircle size={16} />
              Status Guide
            </button>
            <button
              onClick={handleExportCSV}
              className={`flex items-center gap-2 px-4 py-2.5 rounded-xl text-sm font-medium transition-colors ${TEXT_ACCENT_DARK}`}
              style={{ backgroundColor: 'rgba(42,125,111,0.08)', color: ACCENT }}
            >
              <Download size={16} />
              Export CSV
            </button>
          </div>
          {/* Filter pills */}
          <div className="flex flex-wrap gap-1.5">
            {([
              { key: 'all' as StatusFilter, label: 'All' },
              { key: 'needs-attention' as StatusFilter, label: 'Needs Attention' },
              { key: 'thriving' as StatusFilter, label: 'Thriving' },
              { key: 'active' as StatusFilter, label: 'Active' },
              { key: 'new' as StatusFilter, label: 'New' },
              { key: 'drifting' as StatusFilter, label: 'Drifting' },
              { key: 'at-risk' as StatusFilter, label: 'At Risk' },
              { key: 'inactive' as StatusFilter, label: 'Inactive' },
              { key: 'flagged' as StatusFilter, label: 'Flagged' },
            ] as { key: StatusFilter; label: string }[]).map(f => {
              const count = statusCounts[f.key] ?? 0;
              const isActive = statusFilter === f.key;
              return (
                <button
                  key={f.key}
                  onClick={() => setStatusFilter(f.key)}
                  className={`px-3 py-1.5 rounded-lg text-xs font-medium transition-colors ${
                    isActive
                      ? 'text-white'
                      : 'text-zinc-600 dark:text-zinc-400 hover:bg-zinc-100 dark:hover:bg-zinc-800'
                  }`}
                  style={isActive ? { backgroundColor: ACCENT } : { backgroundColor: 'transparent' }}
                >
                  {f.label}{f.key !== 'all' ? ` (${count})` : ''}
                </button>
              );
            })}
          </div>
        </div>

        {/* Status Guide (collapsible) */}
        <AnimatePresence>
          {showStatusGuide && (
            <MotionDiv
              initial={{ opacity: 0, height: 0 }}
              animate={{ opacity: 1, height: 'auto' }}
              exit={{ opacity: 0, height: 0 }}
              className="overflow-hidden"
            >
              <div className="rounded-xl border border-zinc-200 dark:border-zinc-700 p-5 mb-4 bg-zinc-50 dark:bg-zinc-800/30">
                <p className="text-sm font-semibold text-zinc-800 dark:text-white mb-3">What do the statuses mean?</p>
                <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-3">
                  {[
                    { status: 'New', color: '#2A7D6F', desc: 'Signed up within the last 7 days. Give them time to explore.' },
                    { status: 'Active', color: '#3B82F6', desc: 'Logged a study session in the past 7 days. On track.' },
                    { status: 'Thriving', color: '#10B981', desc: 'Active with a 5+ day streak, 3+ modules completed, or 3+ consecutive active weeks.' },
                    { status: 'Drifting', color: '#F59E0B', desc: '8\u201314 days since last session, or lost a strong streak recently. May need a nudge.' },
                    { status: 'At Risk', color: '#EF4444', desc: '15+ days inactive, lost a 7+ day streak, or 3+ weeks with zero sessions. Needs attention.' },
                    { status: 'Inactive', color: '#71717A', desc: 'Past the 7-day new window but has never logged a single study session.' },
                  ].map(s => (
                    <div key={s.status} className="flex gap-3 items-start">
                      <div className="w-2.5 h-2.5 rounded-full mt-1 shrink-0" style={{ backgroundColor: s.color }} />
                      <div>
                        <p className="text-xs font-semibold text-zinc-700 dark:text-zinc-200">{s.status}</p>
                        <p className="text-[11px] text-zinc-500 dark:text-zinc-400 leading-relaxed">{s.desc}</p>
                      </div>
                    </div>
                  ))}
                </div>
              </div>
            </MotionDiv>
          )}
        </AnimatePresence>

        {/* Table */}
        <div className="overflow-x-auto">
          <table className="w-full text-sm">
            <thead>
              <tr className="border-b border-zinc-200 dark:border-zinc-800 text-left bg-zinc-50/50 dark:bg-zinc-800/20">
                {[
                  { key: 'name' as SortKey, label: 'Student' },
                  { key: 'progress' as SortKey, label: 'Progress' },
                  { key: 'cao-current' as SortKey, label: 'CAO Current' },
                  { key: 'cao-target' as SortKey, label: 'CAO Target' },
                  { key: 'gap' as SortKey, label: 'Gap' },
                  { key: 'streak' as SortKey, label: 'Streak' },
                ].map(col => (
                  <th
                    key={col.key}
                    onClick={() => handleSort(col.key)}
                    className="px-5 py-3 text-[10px] font-bold uppercase tracking-wider text-zinc-500 dark:text-zinc-400 cursor-pointer hover:text-zinc-700 dark:hover:text-zinc-200 select-none whitespace-nowrap"
                  >
                    {col.label}{sortIndicator(col.key)}
                  </th>
                ))}
                <th className="px-5 py-3 text-[10px] font-bold uppercase tracking-wider text-zinc-500 dark:text-zinc-400 whitespace-nowrap">Status</th>
                {gcFlags && <th className="px-2 py-3 w-10"></th>}
                {onDeleteStudent && <th className="px-3 py-3 w-10"></th>}
              </tr>
            </thead>
            <tbody>
              {filtered.map((row, i) => {
                const gap = row.targetCAO - row.currentCAO;
                const uid = row.student.user.uid;
                const rowFlag = gcFlags?.getFlagData(uid);
                const rowFlagged = !!rowFlag;
                return (
                  <MotionDiv
                    key={uid}
                    as="tr"
                    initial={{ opacity: 0, y: 4 }}
                    animate={{ opacity: 1, y: 0 }}
                    transition={{ duration: 0.2, delay: i * 0.02 }}
                    onClick={() => onSelectStudent(uid)}
                    className="border-b border-zinc-100 dark:border-zinc-800/50 cursor-pointer hover:bg-zinc-50 dark:hover:bg-zinc-800/30 transition-colors group"
                    style={{ display: 'table-row' }}
                  >
                    <td className="px-5 py-4 align-middle">
                      <div className="flex items-center gap-3">
                        <img src={getAvatarUrl(row.student.user.avatar)} alt="" className="w-8 h-8 rounded-full bg-zinc-200 ring-2 ring-zinc-100 dark:ring-zinc-800 hover:ring-[rgba(var(--accent),0.6)] hover:scale-110 transition-all cursor-pointer" />
                        <span className="font-medium text-zinc-800 dark:text-white whitespace-nowrap">{row.student.user.name}</span>
                      </div>
                    </td>
                    <td className="px-5 py-4 align-middle">
                      <div className="flex items-center gap-2">
                        <span className="font-medium text-zinc-700 dark:text-zinc-200">{row.progress.toFixed(0)}%</span>
                        <div className="w-16 h-1.5 bg-zinc-200 dark:bg-zinc-700 rounded-full overflow-hidden">
                          <div
                            className="h-full bg-[var(--accent-hex)] rounded-full transition-all"
                            style={{ width: `${row.progress}%` }}
                          />
                        </div>
                      </div>
                    </td>
                    <td className="px-5 py-4 align-middle text-zinc-600 dark:text-zinc-300">{row.student.subjectProfile ? row.currentCAO : '\u2014'}</td>
                    <td className="px-5 py-4 align-middle text-zinc-600 dark:text-zinc-300">{row.student.subjectProfile ? row.targetCAO : '\u2014'}</td>
                    <td className="px-5 py-4 align-middle">
                      {row.student.subjectProfile ? gapPill(gap) : '\u2014'}
                    </td>
                    <td className="px-5 py-4 align-middle">
                      <div className="flex items-center gap-1">
                        <Flame size={14} className={row.streak > 0 ? 'text-orange-500' : 'text-zinc-300 dark:text-zinc-600'} />
                        <span className="text-zinc-600 dark:text-zinc-300">{row.streak}</span>
                      </div>
                    </td>
                    <td className="px-5 py-4 align-middle">{statusPill(row.status)}</td>
                    {gcFlags && (
                      <td className="px-2 py-4 align-middle relative">
                        <button
                          onClick={(e) => openFlagPopover(uid, e)}
                          className={`w-7 h-7 rounded-lg flex items-center justify-center transition-all ${
                            rowFlagged
                              ? ''
                              : 'opacity-0 group-hover:opacity-100 text-zinc-300 dark:text-zinc-600 hover:text-zinc-500 dark:hover:text-zinc-400'
                          }`}
                          aria-label={rowFlagged ? `Edit flag for ${row.student.user.name}` : `Flag ${row.student.user.name}`}
                          title={rowFlagged ? 'Edit flag' : 'Flag student'}
                        >
                          <Flag
                            size={14}
                            fill={rowFlagged ? (rowFlag!.priority === 'high' ? '#D97706' : ACCENT) : 'none'}
                            style={rowFlagged ? { color: rowFlag!.priority === 'high' ? '#D97706' : ACCENT } : undefined}
                          />
                        </button>
                        {/* Flag popover */}
                        <AnimatePresence>
                          {flagPopoverUid === uid && (
                            <MotionDiv
                              ref={flagPopoverRef}
                              initial={{ opacity: 0, scale: 0.95, y: -4 }}
                              animate={{ opacity: 1, scale: 1, y: 0 }}
                              exit={{ opacity: 0, scale: 0.95, y: -4 }}
                              transition={{ duration: 0.15 }}
                              className="absolute right-0 top-full mt-1 z-50 w-72 bg-white dark:bg-zinc-900 rounded-xl border border-zinc-200 dark:border-zinc-700 shadow-xl p-4"
                              role="dialog"
                              aria-label={rowFlagged ? 'Edit student flag' : 'Flag student'}
                              onClick={(e: React.MouseEvent) => e.stopPropagation()}
                            >
                              <p className="text-xs font-semibold text-zinc-700 dark:text-zinc-300 mb-3">
                                {rowFlagged ? 'Edit Flag' : 'Flag Student'}
                              </p>
                              <textarea
                                value={flagNote}
                                onChange={(e) => setFlagNote(e.target.value)}
                                placeholder="Add a private note..."
                                className="w-full bg-zinc-50 dark:bg-zinc-800/50 border border-zinc-200 dark:border-zinc-700 rounded-lg p-2.5 text-sm text-zinc-800 dark:text-white placeholder:text-zinc-400 resize-none h-16 focus:outline-none focus:border-[rgba(42,125,111,0.5)] mb-3"
                              />
                              <div className="flex items-center gap-2 mb-3">
                                <span className="text-[10px] font-semibold uppercase tracking-wider text-zinc-500 dark:text-zinc-400">Priority:</span>
                                <button
                                  onClick={() => setFlagPriority('normal')}
                                  className={`px-2.5 py-1 rounded-md text-[10px] font-semibold transition-colors ${flagPriority === 'normal' ? 'text-white' : 'text-zinc-500 dark:text-zinc-400 bg-zinc-100 dark:bg-zinc-800'}`}
                                  style={flagPriority === 'normal' ? { backgroundColor: ACCENT } : undefined}
                                >
                                  Normal
                                </button>
                                <button
                                  onClick={() => setFlagPriority('high')}
                                  className={`px-2.5 py-1 rounded-md text-[10px] font-semibold transition-colors ${flagPriority === 'high' ? 'bg-amber-500 text-white' : 'text-zinc-500 dark:text-zinc-400 bg-zinc-100 dark:bg-zinc-800'}`}
                                >
                                  High
                                </button>
                              </div>
                              <div className="flex gap-2">
                                {rowFlagged && (
                                  <button
                                    onClick={async (e) => { e.stopPropagation(); await gcFlags.unflagStudent(uid); setFlagPopoverUid(null); }}
                                    className="px-3 py-1.5 rounded-lg text-xs font-medium text-red-500 hover:bg-red-50 dark:hover:bg-red-500/10 transition-colors"
                                  >
                                    Remove Flag
                                  </button>
                                )}
                                <button
                                  onClick={async (e) => {
                                    e.stopPropagation();
                                    if (rowFlagged) {
                                      await gcFlags.updateFlagNote(uid, flagNote);
                                      await gcFlags.updateFlagPriority(uid, flagPriority);
                                    } else {
                                      await gcFlags.flagStudent(uid, flagNote, flagPriority);
                                    }
                                    setFlagPopoverUid(null);
                                  }}
                                  className="ml-auto px-3 py-1.5 rounded-lg text-xs font-semibold text-white transition-colors"
                                  style={{ backgroundColor: ACCENT }}
                                >
                                  {rowFlagged ? 'Update' : 'Flag Student'}
                                </button>
                              </div>
                            </MotionDiv>
                          )}
                        </AnimatePresence>
                      </td>
                    )}
                    {(onDeleteStudent || onResetPassword) && (
                      <td className="px-3 py-4 align-middle">
                        <div className="flex items-center gap-1">
                          {onResetPassword && (
                            <button
                              onClick={(e) => { e.stopPropagation(); onResetPassword(row.student.user.uid); }}
                              className="w-7 h-7 rounded-lg flex items-center justify-center text-zinc-300 dark:text-zinc-600 hover:text-[#2A7D6F] dark:hover:text-[#2A7D6F] hover:bg-[#e8f5f2] dark:hover:bg-[#2A7D6F]/10 transition-colors"
                              title="Reset password"
                            >
                              <KeyRound size={14} />
                            </button>
                          )}
                          {onDeleteStudent && (
                            <button
                              onClick={(e) => { e.stopPropagation(); onDeleteStudent(row.student.user); }}
                              className="w-7 h-7 rounded-lg flex items-center justify-center text-zinc-300 dark:text-zinc-600 hover:text-red-500 dark:hover:text-red-400 hover:bg-red-50 dark:hover:bg-red-500/10 transition-colors"
                              title="Delete student"
                            >
                              <Trash2 size={14} />
                            </button>
                          )}
                        </div>
                      </td>
                    )}
                  </MotionDiv>
                );
              })}
            </tbody>
          </table>
        </div>

        {filtered.length === 0 && (
          <div className="text-center py-16">
            <UserX size={32} className="mx-auto text-zinc-300 dark:text-zinc-600 mb-3" />
            <p className="text-zinc-500 dark:text-zinc-400 text-sm font-medium">
              {studentData.length === 0 ? 'No students have signed up yet.' : 'No students match your filters.'}
            </p>
            <p className="text-zinc-400 dark:text-zinc-500 text-xs mt-1">
              {studentData.length === 0 ? 'Students will appear here once they register.' : 'Try adjusting your search or filter criteria.'}
            </p>
          </div>
        )}
      </div>

      {/* ═══════════════════════════════════════════════════════════════════
          Counsellor Notes (warm cream card)
          ═══════════════════════════════════════════════════════════════════ */}
      <div id="gc-notes" className={`rounded-xl overflow-hidden ${CARD_STYLE_DARK_CLASS}`} style={{ backgroundColor: '#FAF7F4', border: '0.5px solid rgba(0,0,0,0.07)' }}>
        <div className="p-5 border-b border-zinc-100 dark:border-zinc-800">
          <div className="flex items-center gap-2">
            <StickyNote size={16} style={{ color: ACCENT }} className={TEXT_ACCENT_DARK} />
            <p className={`text-[11px] font-medium uppercase tracking-widest ${TEXT_NEUTRAL_DARK}`} style={{ color: NEUTRAL_GREY }}>Counsellor Notes</p>
          </div>
          <p className="text-lg font-medium text-zinc-900 dark:text-white mt-1">Student Notes</p>
          <p className={`text-xs mt-0.5 ${TEXT_NEUTRAL_DARK}`} style={{ color: NEUTRAL_GREY }}>Private notes on each student. Click a student to view or edit.</p>
        </div>

        {(() => {
          const studentsWithNotes = studentData
            .filter(s => studentNotes[s.user.uid]?.notes)
            .sort((a, b) => {
              const aTime = studentNotes[a.user.uid]?.updatedAt ?? '';
              const bTime = studentNotes[b.user.uid]?.updatedAt ?? '';
              return bTime.localeCompare(aTime);
            });

          if (studentsWithNotes.length === 0) {
            return (
              <div className="text-center py-12">
                <FileText size={28} className="mx-auto text-zinc-300 dark:text-zinc-600 mb-3" />
                <p className="text-zinc-500 dark:text-zinc-400 text-sm font-medium">No notes yet.</p>
                <p className="text-zinc-400 dark:text-zinc-500 text-xs mt-1">
                  Open a student profile to add private notes.
                </p>
              </div>
            );
          }

          return (
            <div className="divide-y divide-zinc-100 dark:divide-zinc-800">
              {studentsWithNotes.map(s => {
                const note = studentNotes[s.user.uid];
                const preview = note.notes.length > 120 ? note.notes.slice(0, 120) + '...' : note.notes;
                const updatedDate = note.updatedAt ? new Date(note.updatedAt) : null;
                const timeLabel = updatedDate
                  ? `${updatedDate.toLocaleDateString('en-IE', { day: 'numeric', month: 'short' })} at ${updatedDate.toLocaleTimeString('en-IE', { hour: '2-digit', minute: '2-digit' })}`
                  : '';

                return (
                  <button
                    key={s.user.uid}
                    onClick={() => onSelectStudent(s.user.uid)}
                    className="w-full flex items-start gap-4 p-5 hover:bg-zinc-50 dark:hover:bg-zinc-800/30 transition-colors text-left"
                  >
                    <img src={getAvatarUrl(s.user.avatar)} alt="" className="w-9 h-9 rounded-full bg-zinc-200 shrink-0 mt-0.5" />
                    <div className="min-w-0 flex-1">
                      <div className="flex items-center justify-between gap-3">
                        <p className="text-sm font-medium text-zinc-800 dark:text-white truncate">{s.user.name}</p>
                        {timeLabel && (
                          <span className={`text-[10px] shrink-0 ${TEXT_NEUTRAL_DARK}`} style={{ color: NEUTRAL_GREY }}>{timeLabel}</span>
                        )}
                      </div>
                      <p className="text-xs text-zinc-500 dark:text-zinc-400 mt-1 leading-relaxed">{preview}</p>
                    </div>
                  </button>
                );
              })}
            </div>
          );
        })()}
      </div>

      {/* Export Modal */}
      <GCExportModal
        isOpen={showExportModal}
        onClose={() => setShowExportModal(false)}
        studentData={studentData}
        allCourses={allCourses}
        school={school}
      />
    </div>
  );
};

// ─── Daily Activity Line Chart ──────────────────────────────────────────────

function DailyActivityChart({
  aggregatedActivity,
  activityRange,
  onRangeChange,
}: {
  aggregatedActivity: { date: string; count: number }[];
  activityRange: '7d' | '30d';
  onRangeChange: (range: '7d' | '30d') => void;
}) {
  const [hoveredIdx, setHoveredIdx] = useState<number | null>(null);
  const chartRef = useRef<HTMLDivElement>(null);

  const maxCount = Math.max(1, ...aggregatedActivity.map(d => d.count));
  const totalBlocks = aggregatedActivity.reduce((s, d) => s + d.count, 0);
  const activeDays = aggregatedActivity.filter(d => d.count > 0).length;
  const avgPerDay = activeDays > 0 ? (totalBlocks / aggregatedActivity.length).toFixed(1) : '0';
  const n = aggregatedActivity.length;
  const chartH = 160;

  const fmtDate = (d: string) => {
    const parts = d.split('-');
    if (parts.length === 3) {
      const months = ['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec'];
      return `${months[parseInt(parts[1], 10) - 1]} ${parseInt(parts[2], 10)}`;
    }
    return d;
  };

  // Monotone cubic interpolation (Fritsch-Carlson) — no overshoot, flat between equal values
  const buildMonotonePath = (pts: { x: number; y: number }[]): string => {
    if (pts.length < 2) return '';
    if (pts.length === 2) return `M${pts[0].x},${pts[0].y} L${pts[1].x},${pts[1].y}`;

    const len = pts.length;
    // Step 1: compute slopes between consecutive points
    const deltas: number[] = [];
    const _slopes: number[] = [];
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

  const handleMouseMove = (e: React.MouseEvent<HTMLDivElement>) => {
    if (!chartRef.current || n <= 1) return;
    const rect = chartRef.current.getBoundingClientRect();
    const relX = (e.clientX - rect.left) / rect.width;
    const idx = Math.round(relX * (n - 1));
    setHoveredIdx(Math.max(0, Math.min(n - 1, idx)));
  };

  // Compute pixel positions based on actual container width
  const containerWidth = chartRef.current?.getBoundingClientRect().width ?? 500;
  const padLeft = 0;
  const padRight = 0;
  const usableW = containerWidth - padLeft - padRight;
  const padTop = 20;
  const padBottom = 10;
  const usableH = chartH - padTop - padBottom;

  const points = aggregatedActivity.map((d, i) => ({
    x: n > 1 ? padLeft + (i / (n - 1)) * usableW : containerWidth / 2,
    y: padTop + usableH - (d.count / maxCount) * usableH,
    date: d.date,
    count: d.count,
  }));

  const linePath = buildMonotonePath(points);
  const lastPt = points[points.length - 1];
  const firstPt = points[0];
  const areaPath = linePath ? `${linePath} L${lastPt?.x ?? containerWidth},${chartH} L${firstPt?.x ?? 0},${chartH} Z` : '';

  const hovered = hoveredIdx !== null ? points[hoveredIdx] : null;

  return (
    <MotionDiv
      initial={{ opacity: 0, y: 12 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.5, delay: 0.18, ease: [0.25, 0.46, 0.45, 0.94] }}
      className={CARD_STYLE_DARK_CLASS}
      style={CARD_STYLE}
    >
      <div className="flex items-center justify-between mb-6">
        <div>
          <p className={`text-[11px] font-medium uppercase tracking-widest ${TEXT_NEUTRAL_DARK}`} style={{ color: NEUTRAL_GREY }}>Engagement</p>
          <p className="text-lg font-medium text-zinc-900 dark:text-white mt-0.5">Daily Activity</p>
        </div>
        <div className="flex rounded-lg bg-zinc-100 dark:bg-zinc-800 p-0.5">
          {(['7d', '30d'] as const).map(range => (
            <button
              key={range}
              onClick={() => onRangeChange(range)}
              className={`px-3 py-1 text-xs font-medium rounded-md transition-colors ${
                activityRange === range
                  ? 'bg-white dark:bg-zinc-700 text-zinc-900 dark:text-white shadow-sm'
                  : 'text-zinc-500 dark:text-zinc-400 hover:text-zinc-700 dark:hover:text-zinc-300'
              }`}
            >
              {range}
            </button>
          ))}
        </div>
      </div>

      {/* Chart */}
      <div
        ref={chartRef}
        className="relative"
        style={{ height: chartH, cursor: 'crosshair' }}
        onMouseMove={handleMouseMove}
        onMouseLeave={() => setHoveredIdx(null)}
      >
        <svg
          width="100%"
          height={chartH}
          viewBox={`0 0 ${containerWidth} ${chartH}`}
          style={{ overflow: 'visible' }}
        >
          <defs>
            <linearGradient id="areaGradient" x1="0" y1="0" x2="0" y2="1">
              <stop offset="0%" stopColor={ACCENT} stopOpacity={0.15} />
              <stop offset="100%" stopColor={ACCENT} stopOpacity={0} />
            </linearGradient>
          </defs>

          {/* Area fill with gradient */}
          {areaPath && <path d={areaPath} fill="url(#areaGradient)" />}

          {/* Smooth line */}
          {linePath && (
            <path d={linePath} fill="none" stroke={ACCENT} strokeWidth={1.5} strokeLinecap="round" strokeLinejoin="round" opacity={0.7} />
          )}

          {/* Hover vertical line */}
          {hovered && (
            <line x1={hovered.x} y1={0} x2={hovered.x} y2={chartH} stroke={ACCENT} strokeWidth={1} opacity={0.15} />
          )}
        </svg>

        {/* Hover dot + tooltip as HTML */}
        {hovered && (
          <>
            <div
              className="absolute pointer-events-none transition-all duration-75 dark:!bg-zinc-900"
              style={{
                left: hovered.x - 4.5,
                top: hovered.y - 4.5,
                width: 9,
                height: 9,
                borderRadius: '50%',
                backgroundColor: '#FAF7F4',
                border: `2px solid ${ACCENT}`,
                boxShadow: '0 0 0 3px rgba(42,125,111,0.1)',
              }}
            />
            <div
              className="absolute pointer-events-none z-10 transition-all duration-75"
              style={{
                left: Math.max(0, Math.min(hovered.x - 50, containerWidth - 100)),
                top: hovered.y - 40,
              }}
            >
              <div
                className="text-[11px] font-medium text-center shadow-lg"
                style={{
                  backgroundColor: 'rgba(30,30,30,0.9)',
                  color: 'white',
                  borderRadius: 8,
                  padding: '5px 12px',
                  backdropFilter: 'blur(8px)',
                  whiteSpace: 'nowrap',
                }}
              >
                {fmtDate(hovered.date)} &middot; <span className="font-bold">{aggregatedActivity[hoveredIdx!]?.count ?? 0}</span> block{(aggregatedActivity[hoveredIdx!]?.count ?? 0) !== 1 ? 's' : ''}
              </div>
            </div>
          </>
        )}
      </div>

      <div className="flex justify-between mt-3">
        <span className={`text-[10px] ${TEXT_NEUTRAL_DARK}`} style={{ color: NEUTRAL_GREY }}>{fmtDate(aggregatedActivity[0]?.date || '')}</span>
        <span className={`text-[10px] ${TEXT_NEUTRAL_DARK}`} style={{ color: NEUTRAL_GREY }}>{fmtDate(aggregatedActivity[aggregatedActivity.length - 1]?.date || '')}</span>
      </div>

      <div className="flex gap-4 mt-3 text-xs text-zinc-500 dark:text-zinc-400">
        <span><span className="font-medium text-zinc-700 dark:text-zinc-300">{totalBlocks}</span> blocks total</span>
        <span><span className="font-medium text-zinc-700 dark:text-zinc-300">{activeDays}</span> active days</span>
        <span><span className="font-medium text-zinc-700 dark:text-zinc-300">{avgPerDay}</span> avg/day</span>
      </div>
    </MotionDiv>
  );
}
