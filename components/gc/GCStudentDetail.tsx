/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 */

import React, { useState, useEffect, useCallback } from 'react';
import { AnimatePresence } from 'framer-motion';
import { MotionDiv } from '../Motion';
import { ArrowLeft, Flame, Coins, ChevronDown, ChevronRight, BookOpen, AlertTriangle, FileText, X, Save, Compass, BarChart3, Brain, Lightbulb, Heart, UserPlus, TrendingDown, TrendingUp, CheckCircle, MinusCircle, Flag } from 'lucide-react';
import { db } from '../../firebase';
import { doc, getDoc, setDoc } from 'firebase/firestore';
import { addNotification } from './gcNotifications';
import { type CourseData } from '../Library';
import { type CategoryType } from '../KnowledgeTree';
import { getAvatarUrl } from '../../utils/authUtils';
import { getSchoolName } from '../../schoolData';
import { getPointsForGrade, LC_SUBJECTS } from '../subjectData';
import { ARCHETYPES, STAT_LABELS, getStatGrade, type StatKey } from '../journeySimulatorData';
import { NORTH_STAR_CATEGORIES, VISION_CARDS, CATEGORY_COLORS } from '../../northStarData';
import { type GCStudentFullData, type StudentStatus } from './gcTypes';
import { hydrateCourses } from '../futureFinderData';
import { type EarlyWarningAlert, type AlertSeverity } from './gcAlerts';
import {
  getOverallProgress,
  getCategoryProgress,
  getStudentCurrentCAO,
  getStudentTargetCAO,
  getDaysUntilLC,
  getStudentStatus,
  getEngagementTimeline,
} from './gcUtils';
import { getStatusReasons, STATUS_CONFIG } from '../../utils/studentStatus';
import { type FlagData, type FlagPriority } from '../../hooks/useGCFlags';
import { PentagonRadar } from './PentagonRadar';

const CUSTOM_EASE = [0.16, 1, 0.3, 1] as const;

// ─── Categories ─────────────────────────────────────────────────────────────

const CATEGORIES: { id: CategoryType; title: string; color: string; dotColor: string }[] = [
  { id: 'architecture-mindset', title: 'The Architecture of your Mindset', color: 'bg-blue-500', dotColor: 'bg-blue-500' },
  { id: 'science-growth', title: 'The Science of Growth', color: 'bg-amber-500', dotColor: 'bg-amber-500' },
  { id: 'learning-cheat-codes', title: 'The Science of Learning Effectively', color: 'bg-teal-500', dotColor: 'bg-teal-500' },
  { id: 'subject-specific-science', title: 'Decoding the Subjects', color: 'bg-slate-500', dotColor: 'bg-slate-500' },
  { id: 'exam-zone', title: 'Exam Strategy and Points Maximisation', color: 'bg-red-500', dotColor: 'bg-red-500' },
];

// ─── Section label helper ───────────────────────────────────────────────────

const SectionLabel: React.FC<{ label: string }> = ({ label }) => (
  <p className="font-mono text-[9px] font-bold uppercase tracking-[0.25em] text-zinc-400 dark:text-zinc-500 mb-3">{label}</p>
);

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

interface GCStudentDetailProps {
  student: GCStudentFullData;
  allCourses: CourseData[];
  onBack: () => void;
  school?: string;
  isTrayMode?: boolean;
  onNoteSaved?: (uid: string, notes: string, updatedAt: string) => void;
  alerts?: EarlyWarningAlert[];
  gcName?: string;
  gcFlags?: GCFlagsAPI;
}

const INNOVATION_TOOLS = [
  { id: 'journey', title: 'Academic Journey Simulator' },
  { id: 'cao-simulator', title: 'CAO Points Simulator' },
  { id: 'flashcards', title: 'Flashcard Studio' },
  { id: 'planner', title: 'Spaced Repetition Timetable' },
  { id: 'war-room', title: 'War Room' },
  { id: 'comeback', title: 'Comeback Engine' },
  { id: 'future-finder', title: 'Future Finder' },
  { id: 'learning-dna', title: 'Learning DNA' },
  { id: 'first-gen-intel', title: 'First Gen Intel' },
  { id: 'syllabus-xray', title: 'Syllabus X-Ray' },
];

export const GCStudentDetail: React.FC<GCStudentDetailProps> = ({ student, allCourses, onBack, school, isTrayMode, onNoteSaved, alerts = [], gcName, gcFlags }) => {
  const [expandedCategories, setExpandedCategories] = useState<Set<string>>(new Set());
  const [showRecommendModal, setShowRecommendModal] = useState(false);
  const [showKudosModal, setShowKudosModal] = useState(false);
  const [recommendToolId, setRecommendToolId] = useState<string | null>(null);
  const [recommendMessage, setRecommendMessage] = useState('');
  const [kudosMessage, setKudosMessage] = useState('');
  const [isSendingAction, setIsSendingAction] = useState(false);

  const overallProgress = getOverallProgress(student.progress, allCourses);
  const currentCAO = getStudentCurrentCAO(student);
  const targetCAO = getStudentTargetCAO(student);
  const daysUntilLC = getDaysUntilLC();
  const status = getStudentStatus(student, allCourses);
  const statusReasons = getStatusReasons(student, allCourses);
  const supportReasons = statusReasons;

  const STATUS_ICONS: Record<StudentStatus, React.ElementType> = {
    'new': UserPlus, 'at-risk': AlertTriangle, 'drifting': TrendingDown,
    'thriving': TrendingUp, 'active': CheckCircle, 'inactive': MinusCircle,
  };

  // ─── Status transition tracking (localStorage, GC-only) ──────────────
  const [previousStatus, setPreviousStatus] = useState<StudentStatus | null>(null);

  useEffect(() => {
    const key = `gc-status-${student.user.uid}`;
    try {
      const raw = localStorage.getItem(key);
      if (raw) {
        const data = JSON.parse(raw) as { status: StudentStatus; at: number };
        const daysSince = (Date.now() - data.at) / 86400000;
        if (data.status !== status && daysSince <= 7) {
          setPreviousStatus(data.status);
        } else {
          setPreviousStatus(null);
        }
      }
      // Save current status
      localStorage.setItem(key, JSON.stringify({ status, at: Date.now() }));
    } catch {
      setPreviousStatus(null);
    }
  }, [student.user.uid, status]);

  const toggleCategory = (id: string) => {
    setExpandedCategories(prev => {
      const next = new Set(prev);
      if (next.has(id)) next.delete(id); else next.add(id);
      return next;
    });
  };

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
    } catch {
      console.error('Failed to save note:');
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
            className="w-10 h-10 rounded-full bg-zinc-200 dark:bg-zinc-700 ring-2 ring-[rgba(var(--accent),0.2)] shrink-0"
          />
          <div className="min-w-0">
            <p className="font-mono text-[9px] font-bold uppercase tracking-[0.2em] text-zinc-400 dark:text-zinc-500 mb-0.5">Student Profile</p>
            <div className="flex items-center gap-2">
              <h2 className="font-serif text-lg font-semibold tracking-tight text-zinc-900 dark:text-white truncate">{student.user.name}</h2>
              {(() => {
                const cfg = STATUS_CONFIG[status];
                const SIcon = STATUS_ICONS[status];
                return (
                  <span className={`inline-flex items-center gap-1 px-2 py-0.5 rounded-md text-[10px] font-semibold shrink-0 ${cfg.darkBgClass} ${cfg.darkTextClass}`} style={{ backgroundColor: cfg.bg, color: cfg.text }} aria-label={`Status: ${cfg.label}`}>
                    <SIcon size={10} aria-hidden="true" />
                    {cfg.label}
                  </span>
                );
              })()}
              {previousStatus && (
                <span className="text-[10px] text-zinc-400 dark:text-zinc-500 shrink-0">
                  {STATUS_CONFIG[previousStatus].label} &rarr;
                </span>
              )}
            </div>
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
      <div className="absolute top-0 left-0 right-0 h-[3px] bg-[var(--accent-hex)]" />
      <div
        className="absolute inset-0 pointer-events-none"
        style={{ background: 'radial-gradient(ellipse at 50% 0%, rgba(var(--accent),0.06) 0%, transparent 70%)' }}
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
            className="w-14 h-14 rounded-full bg-zinc-200 ring-2 ring-[rgba(var(--accent),0.2)]"
          />
          <div>
            <p className="font-mono text-[9px] font-bold uppercase tracking-[0.25em] text-zinc-400 dark:text-zinc-500 mb-0.5">Student Profile</p>
            <div className="flex items-center gap-2.5">
              <h2 className="font-serif text-2xl font-semibold tracking-tight text-zinc-900 dark:text-white">{student.user.name}</h2>
              {(() => {
                const cfg = STATUS_CONFIG[status];
                const SIcon = STATUS_ICONS[status];
                return (
                  <span className={`inline-flex items-center gap-1.5 px-2.5 py-1 rounded-lg text-xs font-medium shrink-0 ${cfg.darkBgClass} ${cfg.darkTextClass}`} style={{ backgroundColor: cfg.bg, color: cfg.text }} aria-label={`Status: ${cfg.label}`}>
                    <SIcon size={12} aria-hidden="true" />
                    {cfg.label}
                  </span>
                );
              })()}
              {previousStatus && (
                <span className="text-xs text-zinc-400 dark:text-zinc-500 shrink-0">
                  {STATUS_CONFIG[previousStatus].label} &rarr;
                </span>
              )}
            </div>
            <p className="text-xs text-zinc-500 dark:text-zinc-400 mt-0.5">{student.user.school ? getSchoolName(student.user.school) : ''}</p>
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
                className="text-[var(--accent-hex)]"
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

        {/* Status explainer for at-risk / drifting */}
        {(status === 'at-risk' || status === 'drifting') && statusReasons.length > 0 && (() => {
          const cfg = STATUS_CONFIG[status];
          const SIcon = STATUS_ICONS[status];
          return (
            <div className={`mt-4 rounded-xl p-4 ${cfg.darkBgClass}`} style={{ backgroundColor: cfg.bg }}>
              <div className="flex items-start gap-2.5">
                <SIcon size={16} className="mt-0.5 shrink-0" style={{ color: cfg.text }} />
                <div>
                  <p className="text-sm font-semibold mb-1" style={{ color: cfg.text }}>{cfg.label}</p>
                  <ul className="space-y-1">
                    {statusReasons.map((reason, i) => (
                      <li key={i} className="text-xs" style={{ color: cfg.text, opacity: 0.8 }}>{reason}</li>
                    ))}
                  </ul>
                </div>
              </div>
            </div>
          );
        })()}

        {/* Early Warning Signals for this student */}
        {alerts.length > 0 && (
          <div className="mt-4 space-y-2">
            {alerts.map(alert => {
              const colors: Record<AlertSeverity, { bg: string; border: string; text: string; dot: string }> = {
                urgent: { bg: 'bg-rose-50 dark:bg-rose-900/10', border: 'border-rose-200 dark:border-rose-800/40', text: 'text-rose-700 dark:text-rose-400', dot: 'bg-rose-500' },
                watch: { bg: 'bg-amber-50 dark:bg-amber-900/10', border: 'border-amber-200 dark:border-amber-800/40', text: 'text-amber-700 dark:text-amber-400', dot: 'bg-amber-500' },
                nudge: { bg: 'bg-blue-50 dark:bg-blue-900/10', border: 'border-blue-200 dark:border-blue-800/40', text: 'text-blue-700 dark:text-blue-400', dot: 'bg-blue-500' },
              };
              const c = colors[alert.severity];
              return (
                <div key={alert.id} className={`rounded-xl ${c.bg} border ${c.border} px-4 py-3 flex items-center gap-3`}>
                  <div className={`w-2 h-2 rounded-full ${c.dot} shrink-0`} />
                  <div className="min-w-0">
                    <p className={`text-xs font-semibold ${c.text}`}>{alert.title}</p>
                    <p className="text-[11px] text-zinc-500 dark:text-zinc-400 mt-0.5">{alert.description}</p>
                  </div>
                </div>
              );
            })}
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
              className="absolute inset-y-0 left-0 bg-[var(--accent-hex)] rounded-full"
              initial={{ width: 0 }}
              animate={{ width: `${currentPct}%` }}
              transition={{ duration: 0.6, ease: 'easeOut' }}
            />
            {targetPct > currentPct && (
              <div
                className="absolute inset-y-0 border-2 border-dashed border-[rgba(var(--accent),0.5)] rounded-full"
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
          <blockquote className="border-l-2 border-[rgba(var(--accent),0.4)] pl-4 my-3 text-sm text-zinc-600 dark:text-zinc-300 italic font-serif">
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
              className={d.count > 0 ? 'fill-[var(--accent-hex)]' : 'fill-zinc-200 dark:fill-zinc-700'}
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

  // ─── Insights: Career Direction (FF picks) ─────────────────────────────

  const renderCareerDirection = () => {
    if (!student.futureFinder?.topPicks?.length) return null;
    const courses = hydrateCourses(student.futureFinder.topPicks).slice(0, 3);
    if (courses.length === 0) return null;

    return (
      <div className="rounded-xl bg-white dark:bg-zinc-900 border border-zinc-200 dark:border-zinc-800 p-5">
        <div className="flex items-center gap-2 mb-3">
          <Compass size={16} className="text-blue-500" />
          <h4 className="text-sm font-semibold text-zinc-900 dark:text-white">Career Direction</h4>
        </div>
        <div className="space-y-2">
          {courses.map((c, i) => (
            <div key={c.code} className="flex items-center gap-3 px-3 py-2.5 rounded-lg bg-zinc-50 dark:bg-zinc-800/30">
              <span className="text-xs font-bold text-zinc-400 w-5 text-center">{i + 1}</span>
              <div className="flex-1 min-w-0">
                <p className="text-xs font-semibold text-zinc-700 dark:text-zinc-300 truncate">{c.title}</p>
                <p className="text-[10px] text-zinc-400 dark:text-zinc-500">{c.institution} &middot; Level {c.level}</p>
              </div>
              <span className="text-xs font-bold text-zinc-600 dark:text-zinc-300 shrink-0">{c.typicalPoints} pts</span>
            </div>
          ))}
        </div>
      </div>
    );
  };

  // ─── Insights: Mock Trajectory ─────────────────────────────────────────

  const renderMockTrajectory = () => {
    if (!student.mockResults?.length) return null;
    const sorted = [...student.mockResults].sort((a, b) => (a.date ?? '').localeCompare(b.date ?? ''));

    return (
      <div className="rounded-xl bg-white dark:bg-zinc-900 border border-zinc-200 dark:border-zinc-800 p-5">
        <div className="flex items-center gap-2 mb-3">
          <BarChart3 size={16} className="text-amber-500" />
          <h4 className="text-sm font-semibold text-zinc-900 dark:text-white">Mock Trajectory</h4>
        </div>
        <div className="overflow-x-auto">
          <table className="w-full text-sm">
            <thead>
              <tr className="border-b border-zinc-200 dark:border-zinc-800">
                <th className="text-left py-2 px-2 text-[10px] font-bold uppercase tracking-wider text-zinc-500 dark:text-zinc-400">Subject</th>
                <th className="text-center py-2 px-2 text-[10px] font-bold uppercase tracking-wider text-zinc-500 dark:text-zinc-400">Grade</th>
                <th className="text-right py-2 px-2 text-[10px] font-bold uppercase tracking-wider text-zinc-500 dark:text-zinc-400">Date</th>
              </tr>
            </thead>
            <tbody>
              {sorted.map((m) => (
                <tr key={m.id} className="border-b border-zinc-100 dark:border-zinc-800/50">
                  <td className="py-2 px-2 text-xs text-zinc-700 dark:text-zinc-300">{m.subject}</td>
                  <td className="py-2 px-2 text-center text-xs font-semibold text-zinc-800 dark:text-zinc-200">{m.grade}</td>
                  <td className="py-2 px-2 text-right text-[10px] text-zinc-400 dark:text-zinc-500">{m.date}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
    );
  };

  // ─── Insights: Struggle Areas (debrief hardestTopic grouped by subject) ──

  const renderStruggleAreas = () => {
    if (!student.recentDebriefs?.length) return null;

    const grouped: Record<string, string[]> = {};
    for (const d of student.recentDebriefs) {
      if (!d.hardestTopic || d.hardestTopic === 'Not specified') continue;
      if (!grouped[d.subject]) grouped[d.subject] = [];
      if (!grouped[d.subject].includes(d.hardestTopic)) {
        grouped[d.subject].push(d.hardestTopic);
      }
    }

    const entries = Object.entries(grouped);
    if (entries.length === 0) return null;

    return (
      <div className="rounded-xl bg-white dark:bg-zinc-900 border border-zinc-200 dark:border-zinc-800 p-5">
        <div className="flex items-center gap-2 mb-3">
          <Brain size={16} className="text-rose-500" />
          <h4 className="text-sm font-semibold text-zinc-900 dark:text-white">Struggle Areas</h4>
        </div>
        <div className="space-y-3">
          {entries.map(([subject, topics]) => (
            <div key={subject}>
              <p className="text-xs font-semibold text-zinc-700 dark:text-zinc-300 mb-1">{subject}</p>
              <div className="flex flex-wrap gap-1.5">
                {topics.map(t => (
                  <span key={t} className="px-2 py-0.5 rounded-md bg-rose-50 dark:bg-rose-900/20 border border-rose-200 dark:border-rose-800/30 text-[10px] text-rose-700 dark:text-rose-400">
                    {t}
                  </span>
                ))}
              </div>
            </div>
          ))}
        </div>
      </div>
    );
  };

  // ─── GC Notes ─────────────────────────────────────────────────────────

  const renderCounsellorNotes = () => {
    if (!school) return null;
    return (
      <div className="relative rounded-xl bg-white dark:bg-zinc-900 border border-zinc-200 dark:border-zinc-800 p-6 overflow-hidden">
        <div className="absolute top-0 left-0 right-0 h-[3px] bg-[var(--accent-hex)]" />
        <div className="flex items-center gap-2 mb-4">
          <FileText size={16} className="text-[var(--accent-hex)]" />
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
              className="w-full h-24 bg-white dark:bg-zinc-800/50 border border-zinc-200 dark:border-zinc-700 rounded-xl p-4 text-sm text-zinc-900 dark:text-white placeholder:text-zinc-400 dark:placeholder:text-zinc-500 focus:outline-none focus:border-[rgba(var(--accent),0.6)] focus:ring-1 focus:ring-[rgba(var(--accent),0.3)] transition-colors resize-y"
            />
            <div className="flex items-center justify-between mt-3">
              <div className="flex items-center gap-2 text-xs">
                {noteSaving && (
                  <span className="flex items-center gap-1.5 text-[var(--accent-hex)]">
                    <div className="w-3 h-3 border-2 border-[var(--accent-hex)] border-t-transparent rounded-full animate-spin" />
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
                className="flex items-center gap-1.5 px-3 py-1.5 rounded-lg bg-[rgba(var(--accent),0.1)] text-[var(--accent-hex)] hover:bg-[rgba(var(--accent),0.2)] text-xs font-medium transition-colors disabled:opacity-50"
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

  // ─── Quick Actions (Recommend / Kudos) ───────────────────────────────

  const handleSendRecommendation = async () => {
    if (!recommendToolId) return;
    setIsSendingAction(true);
    const toolName = INNOVATION_TOOLS.find(t => t.id === recommendToolId)?.title || recommendToolId;
    await addNotification(student.user.uid, {
      type: 'gc-recommendation',
      title: `Tool Recommended: ${toolName}`,
      body: recommendMessage.trim() || `Your guidance counsellor recommends trying ${toolName}.`,
      fromGCName: gcName,
      actionToolId: recommendToolId,
      severity: 'info',
    });
    setIsSendingAction(false);
    setShowRecommendModal(false);
    setRecommendToolId(null);
    setRecommendMessage('');
  };

  const handleSendKudos = async () => {
    if (!kudosMessage.trim()) return;
    setIsSendingAction(true);
    await addNotification(student.user.uid, {
      type: 'gc-kudos',
      title: 'Words of encouragement',
      body: kudosMessage.trim(),
      fromGCName: gcName,
      severity: 'success',
    });
    setIsSendingAction(false);
    setShowKudosModal(false);
    setKudosMessage('');
  };

  const renderQuickActions = () => (
    <div className="flex items-center gap-2">
      <button
        onClick={() => setShowRecommendModal(true)}
        className="flex items-center gap-1.5 px-3 py-2 rounded-xl bg-indigo-50 dark:bg-indigo-900/20 text-indigo-600 dark:text-indigo-400 text-xs font-semibold hover:bg-indigo-100 dark:hover:bg-indigo-900/30 transition-colors border border-indigo-200/60 dark:border-indigo-800/40"
      >
        <Lightbulb size={14} />
        Recommend Tool
      </button>
      <button
        onClick={() => setShowKudosModal(true)}
        className="flex items-center gap-1.5 px-3 py-2 rounded-xl bg-emerald-50 dark:bg-emerald-900/20 text-emerald-600 dark:text-emerald-400 text-xs font-semibold hover:bg-emerald-100 dark:hover:bg-emerald-900/30 transition-colors border border-emerald-200/60 dark:border-emerald-800/40"
      >
        <Heart size={14} />
        Send Encouragement
      </button>
    </div>
  );

  const renderModals = () => (
    <>
      {/* Recommend Tool Modal */}
      <AnimatePresence>
        {showRecommendModal && (
          <div className="fixed inset-0 z-[200] flex items-center justify-center bg-black/50 backdrop-blur-sm p-4" onClick={() => !isSendingAction && setShowRecommendModal(false)}>
            <MotionDiv
              initial={{ opacity: 0, scale: 0.95 }}
              animate={{ opacity: 1, scale: 1 }}
              exit={{ opacity: 0, scale: 0.95 }}
              className="bg-white dark:bg-zinc-900 rounded-2xl border border-zinc-200 dark:border-zinc-800 p-6 max-w-sm w-full shadow-2xl"
              onClick={(e: React.MouseEvent) => e.stopPropagation()}
            >
              <div className="flex items-center gap-3 mb-4">
                <div className="w-10 h-10 rounded-xl bg-indigo-100 dark:bg-indigo-900/30 flex items-center justify-center">
                  <Lightbulb size={20} className="text-indigo-500" />
                </div>
                <div>
                  <h3 className="text-sm font-semibold text-zinc-800 dark:text-white">Recommend a Tool</h3>
                  <p className="text-xs text-zinc-500">for {student.user.name}</p>
                </div>
              </div>
              <div className="space-y-3 max-h-48 overflow-y-auto mb-3">
                {INNOVATION_TOOLS.map(tool => (
                  <button
                    key={tool.id}
                    onClick={() => setRecommendToolId(tool.id)}
                    className={`w-full text-left px-3 py-2 rounded-lg text-sm transition-colors ${recommendToolId === tool.id ? 'bg-indigo-100 dark:bg-indigo-900/30 text-indigo-700 dark:text-indigo-300 font-medium' : 'hover:bg-zinc-50 dark:hover:bg-zinc-800 text-zinc-700 dark:text-zinc-300'}`}
                  >
                    {tool.title}
                  </button>
                ))}
              </div>
              <textarea
                value={recommendMessage}
                onChange={(e) => setRecommendMessage(e.target.value)}
                placeholder="Add a short message (optional)"
                maxLength={200}
                className="w-full bg-zinc-50 dark:bg-zinc-800/50 border border-zinc-200 dark:border-zinc-700 rounded-xl p-3 text-sm text-zinc-800 dark:text-white placeholder:text-zinc-400 resize-none h-16 focus:outline-none focus:border-indigo-400 mb-3"
              />
              <div className="flex gap-2">
                <button onClick={() => setShowRecommendModal(false)} className="flex-1 py-2 rounded-xl text-sm font-medium text-zinc-500 hover:bg-zinc-100 dark:hover:bg-zinc-800 transition-colors">
                  Cancel
                </button>
                <button
                  onClick={handleSendRecommendation}
                  disabled={!recommendToolId || isSendingAction}
                  className="flex-1 py-2 rounded-xl text-sm font-medium bg-indigo-500 text-white hover:bg-indigo-600 disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
                >
                  {isSendingAction ? 'Sending...' : 'Send'}
                </button>
              </div>
            </MotionDiv>
          </div>
        )}
      </AnimatePresence>

      {/* Send Encouragement Modal */}
      <AnimatePresence>
        {showKudosModal && (
          <div className="fixed inset-0 z-[200] flex items-center justify-center bg-black/50 backdrop-blur-sm p-4" onClick={() => !isSendingAction && setShowKudosModal(false)}>
            <MotionDiv
              initial={{ opacity: 0, scale: 0.95 }}
              animate={{ opacity: 1, scale: 1 }}
              exit={{ opacity: 0, scale: 0.95 }}
              className="bg-white dark:bg-zinc-900 rounded-2xl border border-zinc-200 dark:border-zinc-800 p-6 max-w-sm w-full shadow-2xl"
              onClick={(e: React.MouseEvent) => e.stopPropagation()}
            >
              <div className="flex items-center gap-3 mb-4">
                <div className="w-10 h-10 rounded-xl bg-emerald-100 dark:bg-emerald-900/30 flex items-center justify-center">
                  <Heart size={20} className="text-emerald-500" />
                </div>
                <div>
                  <h3 className="text-sm font-semibold text-zinc-800 dark:text-white">Send Encouragement</h3>
                  <p className="text-xs text-zinc-500">to {student.user.name}</p>
                </div>
              </div>
              <textarea
                value={kudosMessage}
                onChange={(e) => setKudosMessage(e.target.value)}
                placeholder="Write a short encouraging message..."
                maxLength={200}
                className="w-full bg-zinc-50 dark:bg-zinc-800/50 border border-zinc-200 dark:border-zinc-700 rounded-xl p-3 text-sm text-zinc-800 dark:text-white placeholder:text-zinc-400 resize-none h-24 focus:outline-none focus:border-emerald-400 mb-1"
              />
              <p className="text-[10px] text-zinc-400 text-right mb-3">{kudosMessage.length}/200</p>
              <div className="flex gap-2">
                <button onClick={() => setShowKudosModal(false)} className="flex-1 py-2 rounded-xl text-sm font-medium text-zinc-500 hover:bg-zinc-100 dark:hover:bg-zinc-800 transition-colors">
                  Cancel
                </button>
                <button
                  onClick={handleSendKudos}
                  disabled={!kudosMessage.trim() || isSendingAction}
                  className="flex-1 py-2 rounded-xl text-sm font-medium bg-emerald-500 text-white hover:bg-emerald-600 disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
                >
                  {isSendingAction ? 'Sending...' : 'Send'}
                </button>
              </div>
            </MotionDiv>
          </div>
        )}
      </AnimatePresence>
    </>
  );

  const flagData = gcFlags?.getFlagData(student.user.uid);

  const renderFlagBanner = () => {
    if (!flagData) return null;
    const isHigh = flagData.priority === 'high';
    const bannerColor = isHigh ? '#D97706' : '#2A7D6F';
    const bannerBg = isHigh ? 'rgba(217,119,6,0.08)' : 'rgba(42,125,111,0.08)';
    return (
      <div className="flex items-center gap-3 px-6 py-2.5" style={{ backgroundColor: bannerBg }} role="status" aria-label={`Student is ${isHigh ? 'high priority' : ''} flagged`}>
        <Flag size={13} fill={bannerColor} style={{ color: bannerColor }} className="shrink-0" aria-hidden="true" />
        <span className="text-xs font-semibold" style={{ color: bannerColor }}>
          {isHigh ? 'High Priority' : 'Flagged'}
        </span>
        {flagData.note && (
          <>
            <span className="text-zinc-300 dark:text-zinc-600" aria-hidden="true">&middot;</span>
            <span className="text-xs text-zinc-500 dark:text-zinc-400 truncate flex-1">{flagData.note}</span>
          </>
        )}
        <button
          onClick={() => gcFlags?.unflagStudent(student.user.uid)}
          className="text-xs font-medium shrink-0 px-2 py-1 rounded-md hover:bg-zinc-200/50 dark:hover:bg-zinc-700/50 transition-colors"
          style={{ color: bannerColor }}
          aria-label={`Remove flag from ${student.user.name}`}
        >
          Unflag
        </button>
      </div>
    );
  };

  if (isTrayMode) {
    return (
      <div>
        {renderTrayHeader()}
        {renderFlagBanner()}
        {renderModals()}
        <div className="p-6 space-y-6">
          {/* Quick Actions */}
          {renderQuickActions()}

          {/* Stat chips — stays 4-col, fits 672px */}
          <div className="grid grid-cols-2 sm:grid-cols-4 gap-3">
            <div className="bg-zinc-50 dark:bg-zinc-800/40 rounded-xl p-3 flex items-center gap-3">
              <svg width={44} height={44} viewBox="0 0 44 44">
                <circle cx={22} cy={22} r={18} fill="none" stroke="currentColor" className="text-zinc-200 dark:text-zinc-700" strokeWidth={3} />
                <circle cx={22} cy={22} r={18} fill="none" stroke="currentColor" className="text-[var(--accent-hex)]" strokeWidth={3} strokeLinecap="round" strokeDasharray={`${(overallProgress / 100) * 113.1} 113.1`} transform="rotate(-90 22 22)" />
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

              {renderEngagementTimeline()}
              {renderEngagementCards()}
            </div>
          </div>

          {(student.futureFinder || student.mockResults || student.recentDebriefs) && (
            <div>
              <SectionLabel label="Insights" />
              <div className="space-y-5">
                {renderCareerDirection()}
                {renderMockTrajectory()}
                {renderStruggleAreas()}
              </div>
            </div>
          )}

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
      {renderFlagBanner()}
      {renderModals()}

      {/* Quick Actions */}
      {renderQuickActions()}

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
            {renderEngagementTimeline()}
            {renderEngagementCards()}
          </div>
        </div>
      </div>

      {/* Insights section */}
      {(student.futureFinder || student.mockResults || student.recentDebriefs) && (
        <div>
          <SectionLabel label="Insights" />
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
            {renderCareerDirection()}
            {renderMockTrajectory()}
            {renderStruggleAreas()}
          </div>
        </div>
      )}

      {/* Counsellor Notes section */}
      {renderCounsellorNotes()}
    </MotionDiv>
  );
};
