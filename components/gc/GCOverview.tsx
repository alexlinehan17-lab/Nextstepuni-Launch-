/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 */

import React, { useState, useMemo } from 'react';
import { motion } from 'framer-motion';
import { TrendingUp, TrendingDown, Minus, AlertTriangle, Search, ChevronDown, ChevronLeft, ChevronRight, Flame, UserX, Download, FileText, StickyNote } from 'lucide-react';
import { CourseData } from '../Library';
import { CategoryType } from '../KnowledgeTree';
import { getAvatarUrl } from '../Auth';
import { getSchoolName } from '../../schoolData';
import { GCStudentFullData, MoodTrend, StudentStatus } from './gcTypes';
import {
  getOverallProgress,
  getCategoryProgress,
  getStudentStatus,
  getStudentCurrentCAO,
  getStudentTargetCAO,
  getDaysUntilLC,
  isActiveThisWeek,
  getLatestMood,
  getProgressDistribution,
  getMoodTrend,
  getSubjectGaps,
  generateStudentCSV,
  getRecentlyActiveStudents,
  getClassMoodDistribution,
} from './gcUtils';

const MotionDiv = motion.div as any;

const CUSTOM_EASE = [0.16, 1, 0.3, 1] as const;

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
type StatusFilter = 'all' | 'on-track' | 'needs-support' | 'new';

const MOOD_EMOJI: Record<string, string> = {
  calm: '\u{1F60C}',
  balanced: '\u{1F642}',
  energized: '\u{26A1}',
  stressed: '\u{1F630}',
};

// ─── Earthy palette for progress bars ────────────────────────────────────────

const EARTHY_BARS = [
  { label: '0-25%', color: 'bg-[var(--accent-hex)]' },
  { label: '25-50%', color: 'bg-[#D4A574]' },
  { label: '50-75%', color: 'bg-[#8B9D77]' },
  { label: '75-100%', color: 'bg-[#5B7B6F]' },
];

// ─── Mood donut colors ───────────────────────────────────────────────────────

const MOOD_DONUT_COLORS: Record<string, string> = {
  calm: '#5B7B6F',
  balanced: '#8B9D77',
  energized: '#D4A574',
  stressed: 'var(--accent-hex)',
};

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

interface GCOverviewProps {
  studentData: GCStudentFullData[];
  allCourses: CourseData[];
  school: string;
  studentNotes: Record<string, { notes: string; updatedAt: string }>;
  onSelectStudent: (uid: string) => void;
}

export const GCOverview: React.FC<GCOverviewProps> = ({ studentData, allCourses, school, studentNotes, onSelectStudent }) => {
  const [searchQuery, setSearchQuery] = useState('');
  const [statusFilter, setStatusFilter] = useState<StatusFilter>('all');
  const [sortKey, setSortKey] = useState<SortKey>('name');
  const [sortDir, setSortDir] = useState<SortDir>('asc');

  // ─── Computed stats ─────────────────────────────────────────────────────

  const studentStats = useMemo(() => {
    return studentData.map(s => ({
      student: s,
      progress: getOverallProgress(s.progress, allCourses),
      status: getStudentStatus(s, allCourses),
      currentCAO: getStudentCurrentCAO(s),
      targetCAO: getStudentTargetCAO(s),
      streak: s.streak?.currentStreak ?? 0,
      latestMood: getLatestMood(s),
      moodTrend: getMoodTrend(s),
      activeThisWeek: isActiveThisWeek(s),
    }));
  }, [studentData, allCourses]);

  const avgProgress = studentStats.length > 0
    ? studentStats.reduce((sum, s) => sum + s.progress, 0) / studentStats.length
    : 0;

  const needsSupportCount = studentStats.filter(s => s.status === 'needs-support').length;

  const avgCurrentCAO = studentStats.length > 0
    ? Math.round(studentStats.filter(s => s.student.subjectProfile).reduce((sum, s) => sum + s.currentCAO, 0) / Math.max(1, studentStats.filter(s => s.student.subjectProfile).length))
    : 0;

  const activeThisWeekCount = studentStats.filter(s => s.activeThisWeek).length;
  const daysUntilLC = getDaysUntilLC();
  const distribution = getProgressDistribution(studentData, allCourses);
  const distributionTotal = Math.max(1, distribution.reduce((a, b) => a + b, 0));
  const distributionMax = Math.max(1, ...distribution);

  // ─── Category averages ─────────────────────────────────────────────────

  const categoryAverages = useMemo(() => {
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
  const moodDistribution = useMemo(() => getClassMoodDistribution(studentData), [studentData]);

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

    const fmt = (d: Date) => `${d.getFullYear()}-${String(d.getMonth() + 1).padStart(2, '0')}-${String(d.getDate()).padStart(2, '0')}`;

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
    if (statusFilter !== 'all') {
      result = result.filter(s => s.status === statusFilter);
    }
    result.sort((a, b) => {
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
  }, [studentStats, searchQuery, statusFilter, sortKey, sortDir]);

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

  const statusPill = (status: StudentStatus) => {
    switch (status) {
      case 'on-track':
        return (
          <span className="inline-flex items-center gap-1.5 px-2.5 py-1 rounded-lg text-xs font-medium bg-emerald-50 text-emerald-700 dark:bg-emerald-900/20 dark:text-emerald-400 border border-emerald-200 dark:border-emerald-800/40">
            <span className="w-1.5 h-1.5 rounded-full bg-emerald-500" />
            On Track
          </span>
        );
      case 'needs-support':
        return (
          <span className="inline-flex items-center gap-1.5 px-2.5 py-1 rounded-lg text-xs font-medium bg-rose-50 text-rose-700 dark:bg-rose-900/20 dark:text-rose-400 border border-rose-200 dark:border-rose-800/40">
            <span className="w-1.5 h-1.5 rounded-full bg-rose-500" />
            Needs Support
          </span>
        );
      case 'new':
        return (
          <span className="inline-flex items-center gap-1.5 px-2.5 py-1 rounded-lg text-xs font-medium bg-zinc-50 text-zinc-600 dark:bg-zinc-800/50 dark:text-zinc-400 border border-zinc-200 dark:border-zinc-700">
            <span className="w-1.5 h-1.5 rounded-full bg-zinc-400" />
            New
          </span>
        );
    }
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

  // ─── Mood trend icon helper ─────────────────────────────────────────────

  const trendIcon = (trend: MoodTrend) => {
    switch (trend) {
      case 'improving':
        return <TrendingUp size={12} className="text-emerald-500" />;
      case 'declining':
        return <TrendingDown size={12} className="text-rose-500" />;
      case 'stable':
        return <Minus size={12} className="text-zinc-400" />;
      default:
        return null;
    }
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

  // ─── Mood donut SVG ────────────────────────────────────────────────────

  const renderMoodDonut = () => {
    const { distribution: dist, total } = moodDistribution;
    const r = 60;
    const circ = 2 * Math.PI * r;
    let cumulativeOffset = 0;

    return (
      <div className="card-styled rounded-2xl bg-white dark:bg-zinc-900 border border-zinc-200/60 dark:border-zinc-800/60 shadow-[0_1px_3px_rgba(0,0,0,0.04)] hover:shadow-[0_4px_12px_rgba(0,0,0,0.06)] transition-shadow p-5 overflow-hidden">
        <p className="font-mono text-[9px] font-bold uppercase tracking-[0.25em] text-zinc-400 dark:text-zinc-500 mb-3">Class Mood</p>
        <p className="text-base font-semibold tracking-tight text-zinc-900 dark:text-white mb-4">7-Day Check-ins</p>

        <div className="flex justify-center">
          <div className="relative">
            <svg width={150} height={150} viewBox="0 0 150 150">
              {dist.map((entry) => {
                if (entry.count === 0) {
                  return null;
                }
                const segLength = (entry.count / Math.max(1, total)) * circ;
                const offset = circ - cumulativeOffset;
                cumulativeOffset += segLength;
                return (
                  <circle
                    key={entry.mood}
                    cx={75}
                    cy={75}
                    r={r}
                    fill="none"
                    stroke={MOOD_DONUT_COLORS[entry.mood] ?? '#999'}
                    strokeWidth={16}
                    strokeDasharray={`${segLength} ${circ - segLength}`}
                    strokeDashoffset={offset}
                    transform="rotate(-90 75 75)"
                  />
                );
              })}
              {total === 0 && (
                <circle cx={75} cy={75} r={r} fill="none" stroke="currentColor" className="text-zinc-200 dark:text-zinc-700" strokeWidth={16} />
              )}
            </svg>
            <div className="absolute inset-0 flex flex-col items-center justify-center">
              <span className="text-2xl font-bold text-zinc-900 dark:text-white">{total}</span>
              <span className="text-[10px] text-zinc-400">check-ins</span>
            </div>
          </div>
        </div>

        {/* Legend */}
        <div className="grid grid-cols-2 gap-x-4 gap-y-1.5 mt-4">
          {dist.map(entry => (
            <div key={entry.mood} className="flex items-center gap-2">
              <div className="w-2.5 h-2.5 rounded-full shrink-0" style={{ backgroundColor: MOOD_DONUT_COLORS[entry.mood] ?? '#999' }} />
              <span className="text-xs text-zinc-600 dark:text-zinc-400 capitalize">{entry.mood}</span>
              <span className="text-xs font-medium text-zinc-500 ml-auto">{entry.count}</span>
            </div>
          ))}
        </div>
      </div>
    );
  };

  // ─── Render ─────────────────────────────────────────────────────────────

  const hour = new Date().getHours();
  const greeting = hour < 12 ? 'Good morning.' : hour < 18 ? 'Good afternoon.' : 'Good evening.';

  return (
    <div className="p-6 lg:p-8 space-y-5">
      {/* ─── Greeting Row ─────────────────────────────────────────────── */}
      <div id="gc-overview" className="flex flex-col sm:flex-row sm:items-end sm:justify-between gap-4">
        <div>
          <p className="font-mono text-[10px] font-bold uppercase tracking-[0.25em] text-[var(--accent-hex)] mb-1">Guidance Dashboard</p>
          <h1 className="font-serif text-3xl font-semibold text-zinc-900 dark:text-white tracking-tight">{greeting}</h1>
          <p className="text-sm text-zinc-400 dark:text-zinc-500 mt-0.5">{getSchoolName(school)}</p>
        </div>
        <div className="flex items-center gap-2 px-3 py-1.5 rounded-xl bg-[rgba(var(--accent),0.1)] border border-[rgba(var(--accent),0.2)]">
          <span className="text-lg font-bold text-[var(--accent-hex)]">{daysUntilLC}</span>
          <span className="text-[10px] font-bold uppercase tracking-wider text-[rgba(var(--accent),0.7)]">days to LC</span>
        </div>
      </div>

      {/* ─── KPI Cards ────────────────────────────────────────────────── */}
      <div className="grid grid-cols-2 lg:grid-cols-4 gap-4">
        {[
          { label: 'Total Students', value: String(studentData.length), trend: null as number | null },
          { label: 'Avg Progress', value: `${avgProgress.toFixed(0)}%`, trend: null },
          { label: 'Blocks This Week', value: String(weeklyTrends.blocksThisWeek), trend: weeklyTrends.blocksTrend },
          { label: 'Needs Support', value: String(needsSupportCount), trend: null },
        ].map((kpi, i) => (
          <MotionDiv
            key={kpi.label}
            initial={{ opacity: 0, y: 12 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.5, delay: i * 0.04, ease: CUSTOM_EASE }}
            className="card-styled rounded-2xl bg-white dark:bg-zinc-900 border border-zinc-200/60 dark:border-zinc-800/60 shadow-[0_1px_3px_rgba(0,0,0,0.04)] hover:shadow-[0_4px_12px_rgba(0,0,0,0.06)] transition-shadow p-5"
          >
            <p className="font-mono text-[9px] font-bold uppercase tracking-[0.25em] text-zinc-400 dark:text-zinc-500 mb-2">{kpi.label}</p>
            <p className="font-sans text-4xl font-semibold tracking-tight text-zinc-900 dark:text-white">{kpi.value}</p>
            {kpi.trend !== null ? (
              <div className={`flex items-center gap-1 mt-2 text-xs font-medium ${kpi.trend >= 0 ? 'text-emerald-600' : 'text-rose-500'}`}>
                {kpi.trend >= 0 ? <TrendingUp size={12} /> : <TrendingDown size={12} />}
                <span>{kpi.trend > 0 ? '+' : ''}{kpi.trend}% vs last week</span>
              </div>
            ) : (
              <div className="mt-2 h-4" />
            )}
          </MotionDiv>
        ))}
      </div>

      {/* ─── Daily Activity Chart ────────────────────────────────────── */}
      {(() => {
        const maxCount = Math.max(1, ...aggregatedActivity.map(d => d.count));
        const totalBlocks = aggregatedActivity.reduce((s, d) => s + d.count, 0);
        const activeDays = aggregatedActivity.filter(d => d.count > 0).length;
        const avgPerDay = activeDays > 0 ? (totalBlocks / aggregatedActivity.length).toFixed(1) : '0';
        const todayKey = (() => {
          const n = new Date();
          return `${n.getFullYear()}-${String(n.getMonth() + 1).padStart(2, '0')}-${String(n.getDate()).padStart(2, '0')}`;
        })();
        const barCount = aggregatedActivity.length;
        const chartW = 600;
        const chartH = 80;
        const gap = 2;
        const barW = (chartW - gap * (barCount - 1)) / barCount;

        return (
          <MotionDiv
            initial={{ opacity: 0, y: 12 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.5, delay: 0.18, ease: CUSTOM_EASE }}
            className="card-styled rounded-2xl bg-white dark:bg-zinc-900 border border-zinc-200/60 dark:border-zinc-800/60 shadow-[0_1px_3px_rgba(0,0,0,0.04)] hover:shadow-[0_4px_12px_rgba(0,0,0,0.06)] transition-shadow p-5"
          >
            <div className="flex items-center justify-between mb-4">
              <div>
                <p className="font-mono text-[9px] font-bold uppercase tracking-[0.25em] text-zinc-400 dark:text-zinc-500">Engagement</p>
                <p className="text-lg font-semibold tracking-tight text-zinc-900 dark:text-white mt-0.5">Daily Activity</p>
              </div>
              <div className="flex rounded-lg bg-zinc-100 dark:bg-zinc-800 p-0.5">
                {(['7d', '30d'] as const).map(range => (
                  <button
                    key={range}
                    onClick={() => setActivityRange(range)}
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

            <svg viewBox={`0 0 ${chartW} ${chartH}`} className="w-full h-20" preserveAspectRatio="none">
              {/* Horizontal grid lines */}
              {[0.25, 0.5, 0.75].map(frac => (
                <line
                  key={frac}
                  x1={0}
                  y1={chartH - frac * (chartH - 4)}
                  x2={chartW}
                  y2={chartH - frac * (chartH - 4)}
                  stroke="currentColor"
                  className="text-zinc-100 dark:text-zinc-800"
                  strokeWidth={0.5}
                />
              ))}
              {aggregatedActivity.map((d, i) => {
                const x = i * (barW + gap);
                const h = d.count > 0 ? Math.max(4, (d.count / maxCount) * (chartH - 4)) : 2;
                const isToday = d.date === todayKey;
                const fill = isToday ? 'var(--accent-hex)' : d.count > 0 ? '#8B9D77' : undefined;
                return (
                  <rect
                    key={d.date}
                    x={x}
                    y={chartH - h}
                    width={barW}
                    height={h}
                    rx={2}
                    fill={fill}
                    className={d.count === 0 && !isToday ? 'fill-zinc-200 dark:fill-zinc-700' : ''}
                  >
                    <title>{d.date}: {d.count} blocks</title>
                  </rect>
                );
              })}
            </svg>

            <div className="flex justify-between mt-2">
              <span className="text-[10px] text-zinc-400">{aggregatedActivity[0]?.date}</span>
              <span className="text-[10px] text-zinc-400">{aggregatedActivity[aggregatedActivity.length - 1]?.date}</span>
            </div>

            <div className="flex gap-4 mt-3 text-xs text-zinc-500 dark:text-zinc-400">
              <span><span className="font-medium text-zinc-700 dark:text-zinc-300">{totalBlocks}</span> blocks total</span>
              <span><span className="font-medium text-zinc-700 dark:text-zinc-300">{activeDays}</span> active days</span>
              <span><span className="font-medium text-zinc-700 dark:text-zinc-300">{avgPerDay}</span> avg/day</span>
            </div>
          </MotionDiv>
        );
      })()}

      {/* ─── Two-Column Layout: Charts + Widgets ──────────────────────── */}
      <div id="gc-analytics" className="grid grid-cols-1 lg:grid-cols-3 gap-5 items-start">
        {/* Left column (2/3): Category Completion → Progress Distribution → Subject Gaps */}
        <div className="lg:col-span-2 space-y-5">
          {/* Category Completion */}
          <MotionDiv
            initial={{ opacity: 0, y: 12 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.5, delay: 0.2, ease: CUSTOM_EASE }}
            className="card-styled rounded-2xl bg-white dark:bg-zinc-900 border border-zinc-200/60 dark:border-zinc-800/60 shadow-[0_1px_3px_rgba(0,0,0,0.04)] hover:shadow-[0_4px_12px_rgba(0,0,0,0.06)] transition-shadow p-5"
          >
            <div>
              <p className="font-mono text-[9px] font-bold uppercase tracking-[0.25em] text-zinc-400 dark:text-zinc-500">Categories</p>
              <p className="text-lg font-semibold tracking-tight text-zinc-900 dark:text-white mt-0.5 mb-4">Category Completion</p>
            </div>
            <div className="space-y-2.5">
              {categoryAverages.map(cat => (
                <div key={cat.id} className="rounded-xl bg-zinc-50 dark:bg-zinc-800/30 border border-zinc-200/60 dark:border-zinc-700/40 p-3">
                  <div className="flex justify-between items-center mb-1.5">
                    <div className="flex items-center gap-2">
                      <div className={`w-2.5 h-2.5 rounded-full ${cat.dotColor}`} />
                      <p className="text-xs font-medium text-zinc-700 dark:text-zinc-300">{cat.title}</p>
                    </div>
                    <p className="text-xs font-bold text-zinc-600 dark:text-zinc-300">{cat.avgProgress.toFixed(0)}%</p>
                  </div>
                  <div className="w-full bg-zinc-200 dark:bg-zinc-700 rounded-full h-1.5">
                    <MotionDiv
                      className={`h-1.5 rounded-full ${cat.color}`}
                      initial={{ width: 0 }}
                      animate={{ width: `${cat.avgProgress}%` }}
                      transition={{ duration: 0.5, ease: 'easeOut' }}
                    />
                  </div>
                  {cat.zeroStudents > 0 && (
                    <div className="flex items-center gap-1 mt-1.5">
                      <AlertTriangle size={10} className="text-amber-500" />
                      <p className="text-[10px] text-zinc-400 dark:text-zinc-500">
                        {cat.zeroStudents} student{cat.zeroStudents !== 1 ? 's' : ''} with 0 modules started
                      </p>
                    </div>
                  )}
                </div>
              ))}
            </div>
          </MotionDiv>

          {/* Progress Distribution */}
          <MotionDiv
            initial={{ opacity: 0, y: 12 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.5, delay: 0.25, ease: CUSTOM_EASE }}
            className="card-styled rounded-2xl bg-white dark:bg-zinc-900 border border-zinc-200/60 dark:border-zinc-800/60 shadow-[0_1px_3px_rgba(0,0,0,0.04)] hover:shadow-[0_4px_12px_rgba(0,0,0,0.06)] transition-shadow p-5"
          >
            <div className="flex items-baseline justify-between mb-5">
              <div>
                <p className="font-mono text-[9px] font-bold uppercase tracking-[0.25em] text-zinc-400 dark:text-zinc-500">Distribution</p>
                <p className="text-lg font-semibold tracking-tight text-zinc-900 dark:text-white mt-0.5">Progress Breakdown</p>
              </div>
              <span className="text-xs font-medium text-zinc-400 dark:text-zinc-500">{distributionTotal} students</span>
            </div>
            <div className="flex gap-4">
              {distribution.map((count, i) => {
                const heightPct = (count / distributionMax) * 100;
                return (
                  <div key={i} className="flex-1 flex flex-col items-center gap-1.5">
                    <span className="text-xs font-bold text-zinc-600 dark:text-zinc-300">{count}</span>
                    <div className="w-full relative h-28">
                      {count > 0 ? (
                        <MotionDiv
                          className={`absolute bottom-0 left-1 right-1 ${EARTHY_BARS[i].color} rounded-lg`}
                          initial={{ height: 0 }}
                          animate={{ height: `${Math.max(heightPct, 8)}%` }}
                          transition={{ duration: 0.6, delay: 0.3 + i * 0.1, ease: CUSTOM_EASE }}
                        />
                      ) : (
                        <div className="absolute bottom-0 left-1 right-1 h-[2px] rounded-full bg-zinc-200 dark:bg-zinc-700" />
                      )}
                    </div>
                    <span className="text-[10px] font-medium text-zinc-400 dark:text-zinc-500">{EARTHY_BARS[i].label}</span>
                  </div>
                );
              })}
            </div>
          </MotionDiv>

          {/* Subject-Level Gaps */}
          {topGaps.length > 0 && (
            <MotionDiv
              initial={{ opacity: 0, y: 12 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.5, delay: 0.3, ease: CUSTOM_EASE }}
              className="card-styled rounded-2xl bg-white dark:bg-zinc-900 border border-zinc-200/60 dark:border-zinc-800/60 shadow-[0_1px_3px_rgba(0,0,0,0.04)] hover:shadow-[0_4px_12px_rgba(0,0,0,0.06)] transition-shadow p-5"
            >
              <div>
                <p className="font-mono text-[9px] font-bold uppercase tracking-[0.25em] text-zinc-400 dark:text-zinc-500">Subject Analysis</p>
                <p className="text-lg font-semibold tracking-tight text-zinc-900 dark:text-white mt-0.5 mb-4">Subject-Level Gaps</p>
              </div>
              <div className="space-y-2.5">
                {topGaps.map((gap, i) => {
                  const barPct = (gap.avgGap / maxAvgGap) * 100;
                  return (
                    <div key={gap.subjectName} className="flex items-center gap-3">
                      <span className="text-xs font-medium text-zinc-700 dark:text-zinc-300 w-32 truncate shrink-0">{gap.subjectName}</span>
                      <div className="flex-1 h-4 bg-zinc-100 dark:bg-zinc-800 rounded-full overflow-hidden">
                        <MotionDiv
                          className="h-full bg-[var(--accent-hex)] rounded-full"
                          initial={{ width: 0 }}
                          animate={{ width: `${barPct}%` }}
                          transition={{ duration: 0.5, delay: 0.35 + i * 0.05, ease: CUSTOM_EASE }}
                        />
                      </div>
                      <span className="text-xs font-bold text-zinc-600 dark:text-zinc-300 w-20 text-right shrink-0">
                        {gap.avgGap} pts <span className="font-normal text-zinc-400">({gap.studentCount})</span>
                      </span>
                    </div>
                  );
                })}
              </div>
            </MotionDiv>
          )}
        </div>

        {/* Right column (1/3): Recently Active → Mood Donut → Exam Calendar */}
        <div className="flex flex-col gap-5">
          {/* Recently Active Widget */}
          <div className="card-styled rounded-2xl bg-white dark:bg-zinc-900 border border-zinc-200/60 dark:border-zinc-800/60 shadow-[0_1px_3px_rgba(0,0,0,0.04)] hover:shadow-[0_4px_12px_rgba(0,0,0,0.06)] transition-shadow p-5">
            <p className="font-mono text-[9px] font-bold uppercase tracking-[0.25em] text-zinc-400 dark:text-zinc-500 mb-1">Activity</p>
            <p className="text-base font-semibold tracking-tight text-zinc-900 dark:text-white mb-4">Recently Active</p>
            {recentlyActive.length === 0 ? (
              <p className="text-sm text-zinc-400 italic">No recent activity.</p>
            ) : (
              <div className="space-y-2.5">
                {recentlyActive.map(s => (
                  <button
                    key={s.uid}
                    onClick={() => onSelectStudent(s.uid)}
                    className="w-full flex items-center gap-3 p-2 rounded-lg hover:bg-zinc-50 dark:hover:bg-zinc-800/40 transition-colors text-left"
                  >
                    <img src={getAvatarUrl(s.avatar)} alt="" className="w-8 h-8 rounded-full bg-zinc-200 shrink-0" />
                    <div className="min-w-0 flex-1">
                      <p className="text-sm font-medium text-zinc-800 dark:text-white truncate">{s.name}</p>
                      <p className="text-[10px] text-zinc-400 dark:text-zinc-500">
                        {s.blocksCompletedToday > 0 ? `${s.blocksCompletedToday} blocks today` : 'No blocks today'}
                      </p>
                    </div>
                    <span className="text-[10px] text-zinc-400 dark:text-zinc-500 shrink-0">{s.timeAgo}</span>
                  </button>
                ))}
              </div>
            )}
          </div>

          {/* Class Mood Donut */}
          {renderMoodDonut()}

          {/* Exam Countdown Calendar */}
          <div className="card-styled rounded-2xl bg-white dark:bg-zinc-900 border border-zinc-200/60 dark:border-zinc-800/60 shadow-[0_1px_3px_rgba(0,0,0,0.04)] hover:shadow-[0_4px_12px_rgba(0,0,0,0.06)] transition-shadow p-5">
            <div className="flex items-baseline justify-between mb-3">
              <div>
                <p className="font-mono text-[9px] font-bold uppercase tracking-[0.25em] text-zinc-400 dark:text-zinc-500">Countdown</p>
                <p className="text-base font-semibold tracking-tight text-zinc-900 dark:text-white mt-0.5">Exam Calendar</p>
              </div>
              <div className="text-right">
                <p className="text-3xl font-bold text-[var(--accent-hex)]">{daysUntilLC}</p>
                <p className="text-[10px] text-zinc-400">days</p>
              </div>
            </div>
            {/* Month navigation */}
            <div className="flex items-center justify-between mb-3">
              <button onClick={handleCalPrev} className="p-1 rounded-lg hover:bg-zinc-100 dark:hover:bg-zinc-800 transition-colors">
                <ChevronLeft size={16} className="text-zinc-400" />
              </button>
              <span className="text-xs font-medium text-zinc-600 dark:text-zinc-400">{MONTH_NAMES[calMonth]} {calYear}</span>
              <button onClick={handleCalNext} className="p-1 rounded-lg hover:bg-zinc-100 dark:hover:bg-zinc-800 transition-colors">
                <ChevronRight size={16} className="text-zinc-400" />
              </button>
            </div>
            {/* Day-of-week headers */}
            <div className="grid grid-cols-7 gap-1 mb-1">
              {['M', 'T', 'W', 'T', 'F', 'S', 'S'].map((d, i) => (
                <span key={i} className="text-center text-[9px] font-medium text-zinc-400 dark:text-zinc-500">{d}</span>
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
                let cellClass = 'text-zinc-600 dark:text-zinc-400';
                if (isToday) cellClass = 'bg-[var(--accent-hex)] text-white rounded-lg';
                else if (isLC) cellClass = 'bg-rose-500 text-white rounded-lg';

                return (
                  <div
                    key={i}
                    className={`aspect-square flex items-center justify-center text-[11px] font-medium ${cellClass}`}
                    title={isLC ? 'LC Exam Date' : isToday ? 'Today' : ''}
                  >
                    {cell.day}
                  </div>
                );
              })}
            </div>
            {/* Legend */}
            <div className="flex gap-4 mt-3 text-[10px] text-zinc-400">
              <div className="flex items-center gap-1.5">
                <div className="w-3 h-3 rounded bg-[var(--accent-hex)]" />
                <span>Today</span>
              </div>
              {lcDay !== null && (
                <div className="flex items-center gap-1.5">
                  <div className="w-3 h-3 rounded bg-rose-500" />
                  <span>LC Exam</span>
                </div>
              )}
            </div>
          </div>
        </div>
      </div>

      {/* ─── Student Table ────────────────────────────────────────────── */}
      <div id="gc-students" className="rounded-2xl bg-white dark:bg-zinc-900 border border-zinc-200/60 dark:border-zinc-800/60 shadow-[0_1px_3px_rgba(0,0,0,0.04)] hover:shadow-[0_4px_12px_rgba(0,0,0,0.06)] transition-shadow overflow-hidden">
        {/* Table Controls */}
        <div className="flex flex-col sm:flex-row gap-3 p-5 border-b border-zinc-100 dark:border-zinc-800">
          <div className="relative flex-1">
            <Search size={16} className="absolute left-3.5 top-1/2 -translate-y-1/2 text-zinc-400 dark:text-zinc-500" />
            <input
              type="text"
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
              placeholder="Search students..."
              className="w-full bg-zinc-50 dark:bg-zinc-800/50 border border-zinc-200 dark:border-zinc-700 rounded-xl py-2.5 pl-10 pr-4 text-zinc-900 dark:text-white text-sm placeholder:text-zinc-400 dark:placeholder:text-zinc-500 focus:outline-none focus:border-[rgba(var(--accent),0.6)] focus:ring-1 focus:ring-[rgba(var(--accent),0.3)] transition-colors"
            />
          </div>
          <div className="relative">
            <ChevronDown size={14} className="absolute right-3 top-1/2 -translate-y-1/2 text-zinc-400 pointer-events-none" />
            <select
              value={statusFilter}
              onChange={(e) => setStatusFilter(e.target.value as StatusFilter)}
              className="appearance-none bg-zinc-50 dark:bg-zinc-800/50 border border-zinc-200 dark:border-zinc-700 rounded-xl py-2.5 pl-4 pr-8 text-zinc-900 dark:text-white text-sm cursor-pointer focus:outline-none focus:border-[rgba(var(--accent),0.6)] focus:ring-1 focus:ring-[rgba(var(--accent),0.3)] transition-colors"
            >
              <option value="all">All Students</option>
              <option value="on-track">On Track</option>
              <option value="needs-support">Needs Support</option>
              <option value="new">New</option>
            </select>
          </div>
          <button
            onClick={handleExportCSV}
            className="flex items-center gap-2 px-4 py-2.5 rounded-xl bg-[rgba(var(--accent),0.1)] text-[var(--accent-hex)] hover:bg-[rgba(var(--accent),0.2)] text-sm font-medium transition-colors"
          >
            <Download size={16} />
            Export CSV
          </button>
        </div>

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
                <th className="px-5 py-3 text-[10px] font-bold uppercase tracking-wider text-zinc-500 dark:text-zinc-400 whitespace-nowrap">Mood</th>
                <th className="px-5 py-3 text-[10px] font-bold uppercase tracking-wider text-zinc-500 dark:text-zinc-400 whitespace-nowrap">Status</th>
              </tr>
            </thead>
            <tbody>
              {filtered.map((row, i) => {
                const gap = row.targetCAO - row.currentCAO;
                return (
                  <MotionDiv
                    key={row.student.user.uid}
                    as="tr"
                    initial={{ opacity: 0, y: 4 }}
                    animate={{ opacity: 1, y: 0 }}
                    transition={{ duration: 0.2, delay: i * 0.02 }}
                    onClick={() => onSelectStudent(row.student.user.uid)}
                    className="border-b border-zinc-100 dark:border-zinc-800/50 cursor-pointer hover:bg-zinc-50 dark:hover:bg-zinc-800/30 transition-colors"
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
                    <td className="px-5 py-4 align-middle">
                      <div className="flex items-center justify-center gap-1">
                        {row.latestMood ? MOOD_EMOJI[row.latestMood] || '\u2014' : '\u2014'}
                        {trendIcon(row.moodTrend)}
                      </div>
                    </td>
                    <td className="px-5 py-4 align-middle">{statusPill(row.status)}</td>
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

      {/* ─── Student Notes ─────────────────────────────────────────── */}
      <div id="gc-notes" className="rounded-2xl bg-white dark:bg-zinc-900 border border-zinc-200/60 dark:border-zinc-800/60 shadow-[0_1px_3px_rgba(0,0,0,0.04)] hover:shadow-[0_4px_12px_rgba(0,0,0,0.06)] transition-shadow overflow-hidden">
        <div className="p-5 border-b border-zinc-100 dark:border-zinc-800">
          <div className="flex items-center gap-2">
            <StickyNote size={16} className="text-[var(--accent-hex)]" />
            <p className="font-mono text-[9px] font-bold uppercase tracking-[0.25em] text-zinc-400 dark:text-zinc-500">Counsellor Notes</p>
          </div>
          <p className="text-lg font-semibold tracking-tight text-zinc-900 dark:text-white mt-1">Student Notes</p>
          <p className="text-xs text-zinc-400 dark:text-zinc-500 mt-0.5">Private notes on each student. Click a student to view or edit.</p>
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
                          <span className="text-[10px] text-zinc-400 dark:text-zinc-500 shrink-0">{timeLabel}</span>
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
    </div>
  );
};
