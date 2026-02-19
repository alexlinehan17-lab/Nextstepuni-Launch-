/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 */

import React, { useState, useEffect, useCallback } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { ArrowLeft, Flame, Coins, ChevronDown, ChevronRight, BookOpen, AlertTriangle, TrendingUp, TrendingDown, Minus, FileText, X, Save } from 'lucide-react';
import { db } from '../../firebase';
import { doc, getDoc, setDoc } from 'firebase/firestore';
import { CourseData } from '../Library';
import { CategoryType } from '../KnowledgeTree';
import { getAvatarUrl } from '../Auth';
import { getSchoolName } from '../../schoolData';
import { getPointsForGrade, LC_SUBJECTS } from '../subjectData';
import { ARCHETYPES, STAT_LABELS, getStatGrade, StatKey } from '../journeySimulatorData';
import { NORTH_STAR_CATEGORIES, VISION_CARDS, CATEGORY_COLORS } from '../../northStarData';
import { GCStudentFullData } from './gcTypes';
import {
  getOverallProgress,
  getCategoryProgress,
  getStudentCurrentCAO,
  getStudentTargetCAO,
  getDaysUntilLC,
  getStudentStatus,
  getSupportReasons,
  getMoodTrend,
  getEngagementTimeline,
} from './gcUtils';
import { PentagonRadar } from './PentagonRadar';

const MotionDiv = motion.div as any;

const CUSTOM_EASE = [0.16, 1, 0.3, 1] as const;

// ─── Categories ─────────────────────────────────────────────────────────────

const CATEGORIES: { id: CategoryType; title: string; color: string; dotColor: string }[] = [
  { id: 'architecture-mindset', title: 'The Architecture of your Mindset', color: 'bg-blue-500', dotColor: 'bg-blue-500' },
  { id: 'science-growth', title: 'The Science of Growth', color: 'bg-amber-500', dotColor: 'bg-amber-500' },
  { id: 'learning-cheat-codes', title: 'The Science of Learning Effectively', color: 'bg-teal-500', dotColor: 'bg-teal-500' },
  { id: 'subject-specific-science', title: 'Decoding the Subjects', color: 'bg-slate-500', dotColor: 'bg-slate-500' },
  { id: 'exam-zone', title: 'Exam Strategy and Points Maximisation', color: 'bg-red-500', dotColor: 'bg-red-500' },
];

// ─── Mood heatmap helpers ───────────────────────────────────────────────────

const MOOD_COLORS: Record<string, string> = {
  calm: 'bg-emerald-400',
  balanced: 'bg-blue-400',
  energized: 'bg-amber-400',
  stressed: 'bg-rose-400',
};

const DAY_LABELS = ['M', 'T', 'W', 'T', 'F', 'S', 'S'];

function getLast28Days(): string[] {
  const days: string[] = [];
  const now = new Date();
  for (let i = 27; i >= 0; i--) {
    const d = new Date(now);
    d.setDate(d.getDate() - i);
    const y = d.getFullYear();
    const m = String(d.getMonth() + 1).padStart(2, '0');
    const day = String(d.getDate()).padStart(2, '0');
    days.push(`${y}-${m}-${day}`);
  }
  return days;
}

// ─── Section label helper ───────────────────────────────────────────────────

const SectionLabel: React.FC<{ label: string }> = ({ label }) => (
  <p className="font-mono text-[9px] font-bold uppercase tracking-[0.25em] text-zinc-400 dark:text-zinc-500 mb-3">{label}</p>
);

// ─── Component ──────────────────────────────────────────────────────────────

interface GCStudentDetailProps {
  student: GCStudentFullData;
  allCourses: CourseData[];
  onBack: () => void;
  school?: string;
  isTrayMode?: boolean;
  onNoteSaved?: (uid: string, notes: string, updatedAt: string) => void;
}

export const GCStudentDetail: React.FC<GCStudentDetailProps> = ({ student, allCourses, onBack, school, isTrayMode, onNoteSaved }) => {
  const [expandedCategories, setExpandedCategories] = useState<Set<string>>(new Set());

  const overallProgress = getOverallProgress(student.progress, allCourses);
  const currentCAO = getStudentCurrentCAO(student);
  const targetCAO = getStudentTargetCAO(student);
  const daysUntilLC = getDaysUntilLC();
  const status = getStudentStatus(student, allCourses);
  const supportReasons = getSupportReasons(student, allCourses);

  const toggleCategory = (id: string) => {
    setExpandedCategories(prev => {
      const next = new Set(prev);
      if (next.has(id)) next.delete(id); else next.add(id);
      return next;
    });
  };

  // ─── Mood trend ───────────────────────────────────────────────────────

  const moodTrend = getMoodTrend(student);

  // ─── Engagement timeline ──────────────────────────────────────────────

  const engagementTimeline = getEngagementTimeline(student.timetableCompletions);
  const maxBlocks = Math.max(1, ...engagementTimeline.map(d => d.count));
  const totalBlocks = engagementTimeline.reduce((sum, d) => sum + d.count, 0);
  const activeDays = engagementTimeline.filter(d => d.count > 0).length;

  // ─── GC Notes ───────────────────────────────────────────────────────

  const [noteText, setNoteText] = useState('');
  const [savedNotes, setSavedNotes] = useState('');
  const [noteLoading, setNoteLoading] = useState(false);
  const [noteSaving, setNoteSaving] = useState(false);
  const [noteError, setNoteError] = useState<string | null>(null);

  // Load existing notes on student change
  useEffect(() => {
    if (!school) return;
    let cancelled = false;
    setNoteText('');
    setSavedNotes('');
    setNoteLoading(true);

    const loadNotes = async () => {
      try {
        const noteDoc = await getDoc(doc(db, 'gcNotes', school, 'students', student.user.uid));
        if (!cancelled && noteDoc.exists()) {
          setSavedNotes(noteDoc.data().notes ?? '');
        }
      } catch { /* permission error */ }
      if (!cancelled) setNoteLoading(false);
    };
    loadNotes();

    return () => { cancelled = true; };
  }, [student.user.uid, school]);

  const handleSaveNote = useCallback(async () => {
    if (!school || !noteText.trim()) return;
    setNoteSaving(true);
    setNoteError(null);
    try {
      const now = new Date().toISOString();
      const ref = doc(db, 'gcNotes', school, 'students', student.user.uid);
      const updated = savedNotes ? `${savedNotes}\n\n${noteText.trim()}` : noteText.trim();
      await setDoc(ref, { notes: updated, updatedAt: now });
      setSavedNotes(updated);
      setNoteText('');
      onNoteSaved?.(student.user.uid, updated, now);
    } catch (err) {
      console.error('Failed to save note:', err);
      setNoteError('Failed to save. Please try again.');
    }
    setNoteSaving(false);
  }, [school, student.user.uid, noteText, savedNotes, onNoteSaved]);

  // ─── Tray Header (sticky, compact) ──────────────────────────────────

  const renderTrayHeader = () => (
    <div className="sticky top-0 z-10 bg-white dark:bg-zinc-900 border-b border-zinc-200 dark:border-zinc-800 px-6 py-4">
      <div className="flex items-center justify-between">
        <div className="flex items-center gap-3 min-w-0">
          <img
            src={getAvatarUrl(student.user.avatar)}
            alt=""
            className="w-10 h-10 rounded-full bg-zinc-200 dark:bg-zinc-700 ring-2 ring-[#CC785C]/20 shrink-0"
          />
          <div className="min-w-0">
            <p className="font-mono text-[9px] font-bold uppercase tracking-[0.2em] text-zinc-400 dark:text-zinc-500 mb-0.5">Student Profile</p>
            <h2 className="font-serif text-lg font-semibold tracking-tight text-zinc-900 dark:text-white truncate">{student.user.name}</h2>
          </div>
        </div>
        <button
          onClick={onBack}
          className="w-9 h-9 rounded-lg bg-zinc-100 dark:bg-zinc-800 flex items-center justify-center hover:bg-zinc-200 dark:hover:bg-zinc-700 transition-colors shrink-0"
        >
          <X size={18} className="text-zinc-500 dark:text-zinc-300" />
        </button>
      </div>
    </div>
  );

  // ─── Header banner (full mode) ────────────────────────────────────

  const renderHeader = () => (
    <div className="relative rounded-xl bg-white dark:bg-zinc-900 border border-zinc-200 dark:border-zinc-800 p-6 overflow-hidden">
      {/* Accent top bar + gradient glow */}
      <div className="absolute top-0 left-0 right-0 h-[3px] bg-[#CC785C]" />
      <div
        className="absolute inset-0 pointer-events-none"
        style={{ background: 'radial-gradient(ellipse at 50% 0%, rgba(204,120,92,0.06) 0%, transparent 70%)' }}
      />

      <div className="relative">
        {/* Top row: back button + name */}
        <div className="flex items-center gap-4 mb-5">
          <button
            onClick={onBack}
            className="w-10 h-10 rounded-xl bg-zinc-100 dark:bg-zinc-800 flex items-center justify-center hover:bg-zinc-200 dark:hover:bg-zinc-700 transition-colors"
          >
            <ArrowLeft size={18} className="text-zinc-600 dark:text-zinc-300" />
          </button>
          <img
            src={getAvatarUrl(student.user.avatar)}
            alt=""
            className="w-14 h-14 rounded-full bg-zinc-200 ring-2 ring-[#CC785C]/20"
          />
          <div>
            <p className="font-mono text-[9px] font-bold uppercase tracking-[0.25em] text-zinc-400 dark:text-zinc-500 mb-0.5">Student Profile</p>
            <h2 className="font-serif text-2xl font-semibold tracking-tight text-zinc-900 dark:text-white">{student.user.name}</h2>
            <p className="text-xs text-zinc-500 dark:text-zinc-400">{student.user.school ? getSchoolName(student.user.school) : ''}</p>
          </div>
        </div>

        {/* Stat chips grid */}
        <div className="grid grid-cols-2 sm:grid-cols-4 gap-3">
          {/* Progress ring chip */}
          <div className="bg-zinc-50 dark:bg-zinc-800/40 rounded-xl p-3 flex items-center gap-3">
            <svg width={44} height={44} viewBox="0 0 44 44">
              <circle cx={22} cy={22} r={18} fill="none" stroke="currentColor" className="text-zinc-200 dark:text-zinc-700" strokeWidth={3} />
              <circle
                cx={22} cy={22} r={18} fill="none"
                stroke="currentColor"
                className="text-[#CC785C]"
                strokeWidth={3}
                strokeLinecap="round"
                strokeDasharray={`${(overallProgress / 100) * 113.1} 113.1`}
                transform="rotate(-90 22 22)"
              />
            </svg>
            <div>
              <p className="text-xl font-bold text-zinc-900 dark:text-white">{overallProgress.toFixed(0)}%</p>
              <p className="text-[10px] font-medium text-zinc-500">Progress</p>
            </div>
          </div>
          {/* Current CAO */}
          <div className="bg-zinc-50 dark:bg-zinc-800/40 rounded-xl p-3 text-center flex flex-col items-center justify-center">
            <p className="text-xl font-bold text-zinc-900 dark:text-white">{student.subjectProfile ? currentCAO : '\u2014'}</p>
            <p className="text-[10px] font-medium text-zinc-500">Current CAO</p>
          </div>
          {/* Target CAO */}
          <div className="bg-zinc-50 dark:bg-zinc-800/40 rounded-xl p-3 text-center flex flex-col items-center justify-center">
            <p className="text-xl font-bold text-zinc-900 dark:text-white">{student.subjectProfile ? targetCAO : '\u2014'}</p>
            <p className="text-[10px] font-medium text-zinc-500">Target CAO</p>
          </div>
          {/* Days to exam */}
          <div className="bg-zinc-50 dark:bg-zinc-800/40 rounded-xl p-3 text-center flex flex-col items-center justify-center">
            <p className="text-xl font-bold text-zinc-900 dark:text-white">{daysUntilLC}</p>
            <p className="text-[10px] font-medium text-zinc-500">Days to Exam</p>
          </div>
        </div>

        {/* Needs Support explainer */}
        {status === 'needs-support' && supportReasons.length > 0 && (
          <div className="mt-4 rounded-xl bg-rose-50 dark:bg-rose-900/10 border border-rose-200 dark:border-rose-800/40 p-4">
            <div className="flex items-start gap-2.5">
              <AlertTriangle size={16} className="text-rose-500 mt-0.5 shrink-0" />
              <div>
                <p className="text-sm font-semibold text-rose-700 dark:text-rose-400 mb-1">Needs Support</p>
                <ul className="space-y-1">
                  {supportReasons.map((reason, i) => (
                    <li key={i} className="text-xs text-rose-600 dark:text-rose-300/80">{reason}</li>
                  ))}
                </ul>
              </div>
            </div>
          </div>
        )}
      </div>
    </div>
  );

  // ─── Subject Profile Card ───────────────────────────────────────────

  const renderSubjectProfile = () => {
    if (!student.subjectProfile) {
      return (
        <div className="rounded-xl bg-white dark:bg-zinc-900 border border-zinc-200 dark:border-zinc-800 p-6">
          <h3 className="font-serif text-lg font-semibold tracking-tight text-zinc-900 dark:text-white mb-2">Subject Profile</h3>
          <p className="text-sm text-zinc-400 italic">No subject profile set up yet.</p>
        </div>
      );
    }

    const maxPoints = 625;
    const currentPct = Math.min(100, (currentCAO / maxPoints) * 100);
    const targetPct = Math.min(100, (targetCAO / maxPoints) * 100);

    return (
      <div className="rounded-xl bg-white dark:bg-zinc-900 border border-zinc-200 dark:border-zinc-800 p-6">
        <h3 className="font-serif text-lg font-semibold tracking-tight text-zinc-900 dark:text-white mb-4">Subject Profile</h3>

        {/* CAO bar */}
        <div className="mb-5">
          <div className="flex justify-between text-xs text-zinc-500 dark:text-zinc-400 mb-1">
            <span>Current: {currentCAO} pts</span>
            <span>Target: {targetCAO} pts</span>
          </div>
          <div className="relative w-full h-5 bg-zinc-100 dark:bg-zinc-800 rounded-full overflow-hidden">
            <MotionDiv
              className="absolute inset-y-0 left-0 bg-[#CC785C] rounded-full"
              initial={{ width: 0 }}
              animate={{ width: `${currentPct}%` }}
              transition={{ duration: 0.6, ease: 'easeOut' }}
            />
            {targetPct > currentPct && (
              <div
                className="absolute inset-y-0 border-2 border-dashed border-[#CC785C]/50 rounded-full"
                style={{ left: `${currentPct}%`, width: `${targetPct - currentPct}%` }}
              />
            )}
          </div>
          <div className="flex justify-between text-[10px] text-zinc-400 mt-1">
            <span>0</span>
            <span>625</span>
          </div>
        </div>

        {/* Subject table */}
        <div className="overflow-x-auto">
          <table className="w-full text-sm">
            <thead>
              <tr className="border-b border-zinc-200 dark:border-zinc-800">
                <th className="text-left py-2.5 px-3 text-[10px] font-bold uppercase tracking-wider text-zinc-500 dark:text-zinc-400">Subject</th>
                <th className="text-center py-2.5 px-3 text-[10px] font-bold uppercase tracking-wider text-zinc-500 dark:text-zinc-400">Level</th>
                <th className="text-center py-2.5 px-3 text-[10px] font-bold uppercase tracking-wider text-zinc-500 dark:text-zinc-400">Current</th>
                <th className="text-center py-2.5 px-3 text-[10px] font-bold uppercase tracking-wider text-zinc-500 dark:text-zinc-400">Target</th>
                <th className="text-center py-2.5 px-3 text-[10px] font-bold uppercase tracking-wider text-zinc-500 dark:text-zinc-400">Pts Gain</th>
              </tr>
            </thead>
            <tbody>
              {student.subjectProfile.subjects.map((sub, idx) => {
                const isMaths = LC_SUBJECTS.find(lc => lc.name === sub.subjectName)?.isMaths ?? false;
                const currentPts = getPointsForGrade(sub.currentGrade, isMaths);
                const targetPts = getPointsForGrade(sub.targetGrade, isMaths);
                const gain = targetPts - currentPts;
                return (
                  <tr key={sub.subjectName} className={`border-b border-zinc-100 dark:border-zinc-800/50 ${idx % 2 === 1 ? 'bg-zinc-50/50 dark:bg-zinc-800/10' : ''}`}>
                    <td className="py-2.5 px-3 text-zinc-800 dark:text-white font-medium">{sub.subjectName}</td>
                    <td className="py-2.5 px-3 text-center">
                      <span className={`inline-flex px-2 py-0.5 rounded-md text-[10px] font-bold uppercase ${
                        sub.level === 'higher'
                          ? 'bg-blue-50 text-blue-700 dark:bg-blue-900/20 dark:text-blue-400'
                          : 'bg-zinc-100 text-zinc-600 dark:bg-zinc-800 dark:text-zinc-400'
                      }`}>
                        {sub.level === 'higher' ? 'HL' : 'OL'}
                      </span>
                    </td>
                    <td className="py-2.5 px-3 text-center text-zinc-600 dark:text-zinc-300">{sub.currentGrade}</td>
                    <td className="py-2.5 px-3 text-center text-zinc-600 dark:text-zinc-300">{sub.targetGrade}</td>
                    <td className="py-2.5 px-3 text-center">
                      <span className={`inline-flex px-2 py-0.5 rounded-md text-xs font-semibold ${
                        gain > 0
                          ? 'bg-emerald-50 text-emerald-700 dark:bg-emerald-900/20 dark:text-emerald-400'
                          : gain < 0
                          ? 'bg-rose-50 text-rose-700 dark:bg-rose-900/20 dark:text-rose-400'
                          : 'text-zinc-400'
                      }`}>
                        {gain > 0 ? `+${gain}` : gain === 0 ? '0' : gain}
                      </span>
                    </td>
                  </tr>
                );
              })}
            </tbody>
          </table>
        </div>
      </div>
    );
  };

  // ─── North Star Card ────────────────────────────────────────────────

  const renderNorthStar = () => {
    if (!student.northStar) {
      return (
        <div className="rounded-xl bg-white dark:bg-zinc-900 border border-zinc-200 dark:border-zinc-800 p-6">
          <h3 className="font-serif text-lg font-semibold tracking-tight text-zinc-900 dark:text-white mb-2">North Star</h3>
          <p className="text-sm text-zinc-400 italic">Not set yet.</p>
        </div>
      );
    }

    const ns = student.northStar;
    const catOption = NORTH_STAR_CATEGORIES.find(c => c.id === ns.category);
    const catColors = CATEGORY_COLORS[ns.category];
    const visionItems = ns.visionBoard
      .map(id => VISION_CARDS.find(v => v.id === id))
      .filter(Boolean);

    return (
      <div className="rounded-xl bg-white dark:bg-zinc-900 border border-zinc-200 dark:border-zinc-800 p-6">
        <h3 className="font-serif text-lg font-semibold tracking-tight text-zinc-900 dark:text-white mb-3">North Star</h3>
        {catOption && (
          <span className={`inline-flex items-center px-2.5 py-1 rounded-full text-xs font-medium border mb-3 ${catColors.bg} ${catColors.border} ${catColors.text}`}>
            {catOption.label}
          </span>
        )}
        {ns.statement && (
          <blockquote className="border-l-2 border-[#CC785C]/40 pl-4 my-3 text-sm text-zinc-600 dark:text-zinc-300 italic font-serif">
            &ldquo;{ns.statement}&rdquo;
          </blockquote>
        )}
        {visionItems.length > 0 && (
          <div className="flex flex-wrap gap-2 mt-3">
            {visionItems.map(v => (
              <span key={v!.id} className="px-2.5 py-1 rounded-lg bg-zinc-100 dark:bg-zinc-800 text-xs text-zinc-600 dark:text-zinc-400">
                {v!.label}
              </span>
            ))}
          </div>
        )}
      </div>
    );
  };

  // ─── Module Progress (collapsible with mini progress bars) ────────

  const renderModuleProgress = () => (
    <div className="rounded-xl bg-white dark:bg-zinc-900 border border-zinc-200 dark:border-zinc-800 p-6">
      <h3 className="font-serif text-lg font-semibold tracking-tight text-zinc-900 dark:text-white mb-4">Module Progress</h3>
      <div className="space-y-2">
        {CATEGORIES.map(cat => {
          const catCourses = allCourses.filter(c => c.category === cat.id);
          const completedCount = catCourses.filter(c => {
            const p = student.progress[c.id];
            return p && p.unlockedSection >= c.sectionsCount;
          }).length;
          const catProgress = getCategoryProgress(student.progress, allCourses, cat.id);
          const isExpanded = expandedCategories.has(cat.id);

          return (
            <div key={cat.id}>
              <button
                onClick={() => toggleCategory(cat.id)}
                className="w-full flex items-center justify-between py-2.5 px-2 rounded-lg hover:bg-zinc-50 dark:hover:bg-zinc-800/30 transition-colors group"
              >
                <div className="flex-1 min-w-0">
                  <div className="flex items-center gap-2 mb-1">
                    {isExpanded ? <ChevronDown size={14} className="text-zinc-400 shrink-0" /> : <ChevronRight size={14} className="text-zinc-400 shrink-0" />}
                    <div className={`w-2 h-2 rounded-full ${cat.dotColor} shrink-0`} />
                    <p className="text-xs font-medium text-zinc-700 dark:text-zinc-300 truncate">{cat.title}</p>
                    <span className="text-[10px] text-zinc-400 dark:text-zinc-500 shrink-0">{completedCount}/{catCourses.length} complete</span>
                  </div>
                  <div className="w-full bg-zinc-200 dark:bg-zinc-700 rounded-full h-1.5 ml-5">
                    <div className={`h-1.5 rounded-full ${cat.color} transition-all`} style={{ width: `${catProgress}%` }} />
                  </div>
                </div>
                <span className="text-xs font-bold text-zinc-500 dark:text-zinc-300 ml-3 shrink-0">{catProgress.toFixed(0)}%</span>
              </button>

              <AnimatePresence>
                {isExpanded && (
                  <MotionDiv
                    initial={{ height: 0, opacity: 0 }}
                    animate={{ height: 'auto', opacity: 1 }}
                    exit={{ height: 0, opacity: 0 }}
                    transition={{ duration: 0.25, ease: CUSTOM_EASE }}
                    className="overflow-hidden"
                  >
                    <div className="ml-5 mt-1 space-y-1.5 pb-2">
                      {catCourses.map(course => {
                        const p = student.progress[course.id];
                        const unlocked = p?.unlockedSection ?? 0;
                        const total = course.sectionsCount;
                        const pct = total > 0 ? Math.min(100, (unlocked / total) * 100) : 0;
                        const status = pct >= 100 ? 'Complete' : pct > 0 ? 'In Progress' : 'Not Started';
                        const statusColor = pct >= 100 ? 'text-emerald-600 dark:text-emerald-400' : pct > 0 ? 'text-blue-600 dark:text-blue-400' : 'text-zinc-400';

                        return (
                          <div key={course.id} className="flex items-center gap-3 py-2 px-3 rounded-lg bg-zinc-50 dark:bg-zinc-800/30">
                            <BookOpen size={12} className="text-zinc-400 shrink-0" />
                            <p className="text-xs text-zinc-700 dark:text-zinc-300 flex-1 truncate">{course.title}</p>
                            <div className="w-16 h-1.5 bg-zinc-200 dark:bg-zinc-700 rounded-full overflow-hidden shrink-0">
                              <div
                                className={`h-full rounded-full ${cat.color} transition-all`}
                                style={{ width: `${pct}%` }}
                              />
                            </div>
                            <span className={`text-[10px] font-medium ${statusColor} shrink-0 w-16 text-right`}>{status}</span>
                          </div>
                        );
                      })}
                    </div>
                  </MotionDiv>
                )}
              </AnimatePresence>
            </div>
          );
        })}
      </div>
    </div>
  );

  // ─── Journey Simulator Result ─────────────────────────────────────

  const renderJourneyResult = () => {
    if (!student.journeyResult) {
      return (
        <div className="rounded-xl bg-white dark:bg-zinc-900 border border-zinc-200 dark:border-zinc-800 p-6">
          <h3 className="font-serif text-lg font-semibold tracking-tight text-zinc-900 dark:text-white mb-2">Journey Simulator</h3>
          <p className="text-sm text-zinc-400 italic">Not yet attempted.</p>
        </div>
      );
    }

    const jr = student.journeyResult;
    const archetype = ARCHETYPES[jr.endingId];
    const stats = jr.finalStats;
    const statKeys: StatKey[] = ['energy', 'academicCap', 'socialSupport', 'systemSavvy', 'resilience'];

    return (
      <div className="rounded-xl bg-white dark:bg-zinc-900 border border-zinc-200 dark:border-zinc-800 p-6">
        <h3 className="font-serif text-lg font-semibold tracking-tight text-zinc-900 dark:text-white mb-4">Journey Simulator</h3>

        {/* Archetype badge */}
        {archetype && (
          <div className="mb-4">
            <span className={`inline-flex items-center px-2.5 py-1 rounded-lg text-xs font-semibold ${archetype.accentColor} ${archetype.accentBg}`}>
              {archetype.title}
            </span>
            <p className="text-xs text-zinc-500 dark:text-zinc-400 mt-1.5 leading-relaxed">{archetype.description}</p>
          </div>
        )}

        {/* Radar chart — centered */}
        <div className="flex justify-center my-2">
          <PentagonRadar
            values={statKeys.map(k => stats[k])}
            labels={statKeys.map(k => STAT_LABELS[k])}
            size={isTrayMode ? 220 : 300}
          />
        </div>

        {/* Stat rows */}
        <div className="space-y-2 mt-4">
          {statKeys.map(key => {
            const grade = getStatGrade(stats[key]);
            return (
              <div key={key} className="flex items-center gap-2.5">
                <span className={`w-7 h-7 rounded-lg flex items-center justify-center text-xs font-bold ${grade.bg} ${grade.color}`}>
                  {grade.letter}
                </span>
                <span className="text-sm text-zinc-700 dark:text-zinc-300">{STAT_LABELS[key]}</span>
                <span className="text-xs text-zinc-400 ml-auto">{stats[key]}</span>
              </div>
            );
          })}
        </div>
      </div>
    );
  };

  // ─── Engagement: Streak + Points (2-col sub-grid) ─────────────────

  const renderEngagementCards = () => {
    const streak = student.streak;
    const points = student.points;
    const totalEarned = points?.totalEarned ?? 0;

    return (
      <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
        {/* Streak */}
        <div className="rounded-xl bg-white dark:bg-zinc-900 border border-zinc-200 dark:border-zinc-800 p-5">
          <p className="font-mono text-[9px] font-bold uppercase tracking-[0.25em] text-zinc-400 dark:text-zinc-500 mb-3">Streak</p>
          <div className="flex items-center gap-3 mb-3">
            <div className={`w-12 h-12 rounded-xl flex items-center justify-center ${streak?.currentStreak ? 'bg-orange-50 dark:bg-orange-500/10' : 'bg-zinc-100 dark:bg-zinc-800'}`}>
              <Flame size={24} className={streak?.currentStreak ? 'text-orange-500' : 'text-zinc-300 dark:text-zinc-600'} />
            </div>
            <span className="text-3xl font-bold text-zinc-900 dark:text-white">{streak?.currentStreak ?? 0}</span>
            <span className="text-sm text-zinc-500">day{(streak?.currentStreak ?? 0) !== 1 ? 's' : ''}</span>
          </div>
          <div className="space-y-1 text-xs text-zinc-500 dark:text-zinc-400">
            <p>Longest streak: <span className="font-medium text-zinc-700 dark:text-zinc-300">{streak?.longestStreak ?? 0}</span></p>
            <p>Last active: <span className="font-medium text-zinc-700 dark:text-zinc-300">{streak?.lastActiveDate || 'Never'}</span></p>
          </div>
        </div>

        {/* Points Earned */}
        <div className="rounded-xl bg-white dark:bg-zinc-900 border border-zinc-200 dark:border-zinc-800 p-5">
          <p className="font-mono text-[9px] font-bold uppercase tracking-[0.25em] text-zinc-400 dark:text-zinc-500 mb-3">Points Earned</p>
          <div className="flex items-center gap-3">
            <div className="w-12 h-12 rounded-xl bg-amber-50 dark:bg-amber-500/10 flex items-center justify-center">
              <Coins size={24} className="text-amber-500" />
            </div>
            <span className="text-3xl font-bold text-zinc-900 dark:text-white">{totalEarned}</span>
            <span className="text-sm text-zinc-500">total</span>
          </div>
        </div>
      </div>
    );
  };

  // ─── Mood heatmap ────────────────────────────────────────────────

  const renderMoodHeatmap = () => {
    const last28 = getLast28Days();
    const moodEntries = student.mood?.entries ?? [];

    // Build a date-keyed lookup from the array
    const moodByDate: Record<string, string> = {};
    moodEntries.forEach(e => { moodByDate[e.date] = e.mood; });

    // Mood distribution
    const moodCounts: Record<string, number> = { calm: 0, balanced: 0, energized: 0, stressed: 0 };
    moodEntries.forEach(e => {
      if (e.mood in moodCounts) moodCounts[e.mood]++;
    });

    return (
      <div className="rounded-xl bg-white dark:bg-zinc-900 border border-zinc-200 dark:border-zinc-800 p-5">
        <div className="flex items-center justify-between mb-3">
          <p className="font-mono text-[9px] font-bold uppercase tracking-[0.25em] text-zinc-400 dark:text-zinc-500">Mood (28 Days)</p>
          {moodTrend !== 'insufficient-data' && (
            <span className={`inline-flex items-center gap-1.5 px-2.5 py-1 rounded-lg text-[10px] font-semibold ${
              moodTrend === 'improving'
                ? 'bg-emerald-50 text-emerald-700 dark:bg-emerald-900/20 dark:text-emerald-400'
                : moodTrend === 'declining'
                ? 'bg-rose-50 text-rose-700 dark:bg-rose-900/20 dark:text-rose-400'
                : 'bg-zinc-100 text-zinc-600 dark:bg-zinc-800 dark:text-zinc-400'
            }`}>
              {moodTrend === 'improving' && <TrendingUp size={12} />}
              {moodTrend === 'declining' && <TrendingDown size={12} />}
              {moodTrend === 'stable' && <Minus size={12} />}
              {moodTrend === 'improving' ? 'Improving vs prior week' : moodTrend === 'declining' ? 'Declining vs prior week' : 'Stable'}
            </span>
          )}
        </div>
        {/* Day-of-week labels */}
        <div className="grid grid-cols-7 gap-2 mb-1">
          {DAY_LABELS.map((d, i) => (
            <span key={i} className="text-center text-[9px] font-medium text-zinc-400 dark:text-zinc-500">{d}</span>
          ))}
        </div>
        <div className="grid grid-cols-7 gap-2 mb-4">
          {last28.map(day => {
            const mood = moodByDate[day];
            const color = mood ? (MOOD_COLORS[mood] ?? 'bg-zinc-200 dark:bg-zinc-700') : 'bg-zinc-200 dark:bg-zinc-700';
            return (
              <div
                key={day}
                className={`w-full aspect-square rounded-lg ${color} hover:scale-110 transition-transform cursor-default`}
                title={`${day}: ${mood ?? 'no entry'}`}
              />
            );
          })}
        </div>
        <div className="border-t border-zinc-200 dark:border-zinc-800 pt-3">
          <div className="flex flex-wrap gap-4 text-[10px] text-zinc-500 dark:text-zinc-400">
            {Object.entries(moodCounts).map(([mood, count]) => (
              <div key={mood} className="flex items-center gap-1.5">
                <div className={`w-3 h-3 rounded-full ${MOOD_COLORS[mood]}`} />
                <span className="capitalize">{mood}: {count}</span>
              </div>
            ))}
          </div>
        </div>
      </div>
    );
  };

  // ─── Engagement timeline (SVG bar chart) ────────────────────────────

  const renderEngagementTimeline = () => (
    <div className="rounded-xl bg-white dark:bg-zinc-900 border border-zinc-200 dark:border-zinc-800 p-5">
      <p className="font-mono text-[9px] font-bold uppercase tracking-[0.25em] text-zinc-400 dark:text-zinc-500 mb-3">Activity (30 Days)</p>
      <svg viewBox="0 0 300 60" className="w-full h-16" preserveAspectRatio="none">
        {engagementTimeline.map((d, i) => {
          const barW = 300 / 30 - 1.5;
          const x = i * (300 / 30) + 0.75;
          const h = d.count > 0 ? Math.max(4, (d.count / maxBlocks) * 52) : 2;
          return (
            <rect
              key={d.date}
              x={x}
              y={60 - h}
              width={barW}
              height={h}
              rx={1.5}
              className={d.count > 0 ? 'fill-[#CC785C]' : 'fill-zinc-200 dark:fill-zinc-700'}
            >
              <title>{d.date}: {d.count} blocks</title>
            </rect>
          );
        })}
      </svg>
      <div className="flex justify-between mt-2">
        <span className="text-[10px] text-zinc-400">{engagementTimeline[0]?.date}</span>
        <span className="text-[10px] text-zinc-400">{engagementTimeline[engagementTimeline.length - 1]?.date}</span>
      </div>
      <div className="flex gap-4 mt-2 text-xs text-zinc-500 dark:text-zinc-400">
        <span><span className="font-medium text-zinc-700 dark:text-zinc-300">{totalBlocks}</span> blocks completed</span>
        <span><span className="font-medium text-zinc-700 dark:text-zinc-300">{activeDays}</span> active days</span>
      </div>
    </div>
  );

  // ─── GC Notes ─────────────────────────────────────────────────────────

  const renderCounsellorNotes = () => {
    if (!school) return null;
    return (
      <div className="relative rounded-xl bg-white dark:bg-zinc-900 border border-zinc-200 dark:border-zinc-800 p-6 overflow-hidden">
        <div className="absolute top-0 left-0 right-0 h-[3px] bg-[#CC785C]" />
        <div className="flex items-center gap-2 mb-4">
          <FileText size={16} className="text-[#CC785C]" />
          <h3 className="text-lg font-semibold tracking-tight text-zinc-900 dark:text-white">Counsellor Notes</h3>
        </div>

        {noteLoading ? (
          <div className="h-32 bg-zinc-100 dark:bg-zinc-800 rounded-xl animate-pulse" />
        ) : (
          <>
            {/* Saved notes display */}
            {savedNotes && (
              <div className="mb-4 rounded-xl bg-zinc-50 dark:bg-zinc-800/40 border border-zinc-200/60 dark:border-zinc-700/40 p-4 max-h-60 overflow-y-auto">
                <p className="text-xs font-medium text-zinc-400 dark:text-zinc-500 uppercase tracking-wider mb-2">Saved Notes</p>
                <div className="text-sm text-zinc-700 dark:text-zinc-300 whitespace-pre-wrap leading-relaxed">{savedNotes}</div>
              </div>
            )}

            {/* New note input */}
            <textarea
              value={noteText}
              onChange={(e) => setNoteText(e.target.value)}
              placeholder="Add a note about this student..."
              className="w-full h-24 bg-white dark:bg-zinc-800/50 border border-zinc-200 dark:border-zinc-700 rounded-xl p-4 text-sm text-zinc-900 dark:text-white placeholder:text-zinc-400 dark:placeholder:text-zinc-500 focus:outline-none focus:border-[#CC785C]/60 focus:ring-1 focus:ring-[#CC785C]/30 transition-colors resize-y"
            />
            <div className="flex items-center justify-between mt-3">
              <div className="flex items-center gap-2 text-xs">
                {noteSaving && (
                  <span className="flex items-center gap-1.5 text-[#CC785C]">
                    <div className="w-3 h-3 border-2 border-[#CC785C] border-t-transparent rounded-full animate-spin" />
                    Saving...
                  </span>
                )}
                {noteError && (
                  <span className="text-rose-500">{noteError}</span>
                )}
              </div>
              <button
                onClick={handleSaveNote}
                disabled={noteSaving || !noteText.trim()}
                className="flex items-center gap-1.5 px-3 py-1.5 rounded-lg bg-[#CC785C]/10 text-[#CC785C] hover:bg-[#CC785C]/20 text-xs font-medium transition-colors disabled:opacity-50"
              >
                <Save size={13} />
                Save Note
              </button>
            </div>
          </>
        )}
      </div>
    );
  };

  // ─── Render ─────────────────────────────────────────────────────────

  if (isTrayMode) {
    return (
      <div>
        {renderTrayHeader()}
        <div className="p-6 space-y-6">
          {/* Stat chips — stays 4-col, fits 672px */}
          <div className="grid grid-cols-2 sm:grid-cols-4 gap-3">
            <div className="bg-zinc-50 dark:bg-zinc-800/40 rounded-xl p-3 flex items-center gap-3">
              <svg width={44} height={44} viewBox="0 0 44 44">
                <circle cx={22} cy={22} r={18} fill="none" stroke="currentColor" className="text-zinc-200 dark:text-zinc-700" strokeWidth={3} />
                <circle cx={22} cy={22} r={18} fill="none" stroke="currentColor" className="text-[#CC785C]" strokeWidth={3} strokeLinecap="round" strokeDasharray={`${(overallProgress / 100) * 113.1} 113.1`} transform="rotate(-90 22 22)" />
              </svg>
              <div>
                <p className="text-xl font-bold text-zinc-900 dark:text-white">{overallProgress.toFixed(0)}%</p>
                <p className="text-[10px] font-medium text-zinc-500">Progress</p>
              </div>
            </div>
            <div className="bg-zinc-50 dark:bg-zinc-800/40 rounded-xl p-3 text-center flex flex-col items-center justify-center">
              <p className="text-xl font-bold text-zinc-900 dark:text-white">{student.subjectProfile ? currentCAO : '\u2014'}</p>
              <p className="text-[10px] font-medium text-zinc-500">Current CAO</p>
            </div>
            <div className="bg-zinc-50 dark:bg-zinc-800/40 rounded-xl p-3 text-center flex flex-col items-center justify-center">
              <p className="text-xl font-bold text-zinc-900 dark:text-white">{student.subjectProfile ? targetCAO : '\u2014'}</p>
              <p className="text-[10px] font-medium text-zinc-500">Target CAO</p>
            </div>
            <div className="bg-zinc-50 dark:bg-zinc-800/40 rounded-xl p-3 text-center flex flex-col items-center justify-center">
              <p className="text-xl font-bold text-zinc-900 dark:text-white">{daysUntilLC}</p>
              <p className="text-[10px] font-medium text-zinc-500">Days to Exam</p>
            </div>
          </div>

          {/* Needs Support */}
          {status === 'needs-support' && supportReasons.length > 0 && (
            <div className="rounded-xl bg-rose-50 dark:bg-rose-900/10 border border-rose-200 dark:border-rose-800/40 p-4">
              <div className="flex items-start gap-2.5">
                <AlertTriangle size={16} className="text-rose-500 mt-0.5 shrink-0" />
                <div>
                  <p className="text-sm font-semibold text-rose-700 dark:text-rose-400 mb-1">Needs Support</p>
                  <ul className="space-y-1">
                    {supportReasons.map((reason, i) => (
                      <li key={i} className="text-xs text-rose-600 dark:text-rose-300/80">{reason}</li>
                    ))}
                  </ul>
                </div>
              </div>
            </div>
          )}

          {/* Single-column stacked layout for tray */}
          <div>
            <SectionLabel label="Academic Profile" />
            <div className="space-y-5">
              {renderSubjectProfile()}
              {renderNorthStar()}
            </div>
          </div>

          <div>
            <SectionLabel label="Learning Progress" />
            {renderModuleProgress()}
          </div>

          <div>
            <SectionLabel label="Engagement & Wellbeing" />
            <div className="space-y-5">
              {renderJourneyResult()}
              {renderMoodHeatmap()}
              {renderEngagementTimeline()}
              {renderEngagementCards()}
            </div>
          </div>

          {renderCounsellorNotes()}
        </div>
      </div>
    );
  }

  return (
    <MotionDiv
      initial={{ opacity: 0 }}
      animate={{ opacity: 1 }}
      transition={{ duration: 0.3 }}
      className="space-y-8"
    >
      {renderHeader()}

      {/* Academic Profile section */}
      <div>
        <SectionLabel label="Academic Profile" />
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          {renderSubjectProfile()}
          {renderNorthStar()}
        </div>
      </div>

      {/* Learning Progress section */}
      <div>
        <SectionLabel label="Learning Progress" />
        {renderModuleProgress()}
      </div>

      {/* Engagement & Wellbeing section */}
      <div>
        <SectionLabel label="Engagement & Wellbeing" />
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          {renderJourneyResult()}
          <div className="space-y-4">
            {renderMoodHeatmap()}
            {renderEngagementTimeline()}
            {renderEngagementCards()}
          </div>
        </div>
      </div>

      {/* Counsellor Notes section */}
      {renderCounsellorNotes()}
    </MotionDiv>
  );
};
