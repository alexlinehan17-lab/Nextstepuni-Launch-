/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
*/

import React, { useState, useMemo, useEffect, useCallback, useRef } from 'react';
import { AnimatePresence, MotionDiv, useReducedMotion } from './Motion';
import {
  ArrowRight, Check,
  User, Home, PanelLeft, ChartNoAxesCombined, Award, BookOpen, CalendarRange, Settings, LogOut, Sun, Moon, RefreshCw, Timer, Bell, MessageSquare, HelpCircle
} from 'lucide-react';
import FirstVisitCoachMarks, { coachMarksSeen } from './FirstVisitCoachMarks';
import ResumeCard from './ResumeCard';
import { type CourseData } from './Library';
import { type UserSettings } from '../types';
import { toDateKey } from './subjectData';
import { SectionCard } from './SectionCard';
import { ModulesIcon, InnovationZoneIcon, MyProgressIcon, LearningPathsIcon, MyJourneyIcon } from './sectionIcons';
import Avatar from './Avatar';
import { COLORS } from '../design/tokens';
import { toggleNotificationPanel } from '../utils/notificationPanel';

export type CategoryType =
  | 'architecture-mindset'
  | 'science-growth'
  | 'learning-cheat-codes'
  | 'exam-zone'
  | 'subject-specific-science';

type UserProgress = {
  [moduleId: string]: { unlockedSection: number };
};

interface KnowledgeTreeProps {
  onSelectCategory: (category: CategoryType) => void;
  onGoToModules: () => void;
  onGoToInnovationZone: () => void;
  onGoToDashboard: () => void;
  onGoToLearningPaths: () => void;
  onGoToJourney: () => void;
  onGoToStudy?: () => void;
  onGoToInsights?: () => void;
  onGoToCutContent?: () => void;
  onGoToAccreditation?: () => void;
  onGoToYearPlans?: () => void;
  onGoToWipTools?: () => void;
  onSelectModule: (moduleId: string) => void;
  allCourses: CourseData[];
  categoryTitles: Record<CategoryType, string>;
  userProgress: UserProgress;
  userName?: string;
  userAvatarSeed?: string;
  onLogout: () => void;
  onOpenSettings: () => void;
  onOpenPassport: () => void;
  onChangeSubjects?: () => void;
  settings: UserSettings;
  updateSetting: <K extends keyof UserSettings>(key: K, value: UserSettings[K]) => void;
  unlockedThemes?: string[];
  completedCount: number;
  totalCount: number;
  streak?: { currentStreak: number; longestStreak: number; lastActiveDate: string };
  pointsBalance?: number;
  northStar?: { category: string; statement: string } | null;
  studentProfile?: { subjects: { subjectName: string; currentGrade?: string; targetGrade?: string; level?: string }[]; examStartDate: string; restDays?: string[]; defaultBlockDuration?: number; createdAt?: string } | null;
  timetableCompletions?: Record<string, string[]>;
  smartRecommendation?: { id: string; title: string; description: string; category: string } | null;
  questState?: { quest: { title: string; description: string; rewardPoints: number; target: number }; current: number; isCompleted: boolean; isClaimed: boolean; dayNumber: number; isOnboarding: boolean } | null;
  onClaimQuestReward?: () => void;
  onRecommendationAction?: (action: string) => void;
  /** Deep-link a Launchpad tool by id (Site Guide "Take me there"). */
  onOpenTool?: (toolId: string) => void;
  /** Stable per-account key for one-time coach marks. */
  uid?: string;
  onOpenSiteGuide?: () => void;
  onOpenFeedback?: () => void;
  onOpenMobileProfile?: () => void;
  hasUnreadNotifications?: boolean;
}

const noop = () => {};

export const KnowledgeTree: React.FC<KnowledgeTreeProps> = ({ onSelectCategory: _onSelectCategory, onGoToModules, onGoToInnovationZone, onGoToDashboard, onGoToLearningPaths, onGoToJourney, onGoToStudy, onGoToInsights: _onGoToInsights, onGoToAccreditation, onGoToYearPlans, allCourses, onSelectModule, categoryTitles: _categoryTitles, userProgress, userName, userAvatarSeed, onLogout, onOpenSettings, onOpenPassport, onChangeSubjects, settings, updateSetting, unlockedThemes: _unlockedThemes = [], completedCount, totalCount, streak, pointsBalance, northStar, studentProfile, timetableCompletions, smartRecommendation, questState, onClaimQuestReward, onRecommendationAction, onOpenTool, uid, onOpenSiteGuide = noop, onOpenFeedback = noop, onOpenMobileProfile = noop, hasUnreadNotifications = false }) => {
  const [sidebarOpen, setSidebarOpen] = useState(false);
  const reduceMotion = useReducedMotion();
  // The former inline home panel has moved into the full student dashboard.
  // Keep the legacy preference dormant so an old `showDashboard: true` value
  // cannot render duplicate analytics above the home modules.
  const dashboardVisible = false;
  const dashboardRef = useRef<HTMLDivElement | null>(null);
  const dashboardRevealRequested = useRef(false);
  // Site Guide (the "?") + one-time first-visit coach marks.
  const [coachActive, setCoachActive] = useState(false);
  // "What's new" popover + its unseen-dot state.

  // Start the spotlight once the home screen has painted.
  // This also re-evaluates when auth supplies the stable account uid instead
  // of accidentally binding the one-time tour to the anonymous key.
  useEffect(() => {
    if (coachMarksSeen(uid)) {
      setCoachActive(false);
      return;
    }
    let secondFrame = 0;
    let timer: ReturnType<typeof setTimeout> | undefined;
    const firstFrame = requestAnimationFrame(() => {
      secondFrame = requestAnimationFrame(() => {
        timer = setTimeout(() => setCoachActive(true), 180);
      });
    });
    return () => {
      cancelAnimationFrame(firstFrame);
      if (secondFrame) cancelAnimationFrame(secondFrame);
      if (timer) clearTimeout(timer);
    };
  }, [uid]);

  // Keep the newly revealed panel in view. Without this, browser scroll
  // anchoring can hold the module grid in place while the dashboard opens
  // above it, making a successful toggle look as though nothing happened.
  useEffect(() => {
    if (!dashboardVisible || !dashboardRevealRequested.current) return;
    dashboardRevealRequested.current = false;

    let secondFrame = 0;
    const firstFrame = requestAnimationFrame(() => {
      secondFrame = requestAnimationFrame(() => {
        dashboardRef.current?.scrollIntoView({
          behavior: reduceMotion ? 'auto' : 'smooth',
          block: 'start',
        });
      });
    });

    return () => {
      cancelAnimationFrame(firstFrame);
      if (secondFrame) cancelAnimationFrame(secondFrame);
    };
  }, [dashboardVisible, reduceMotion]);

  const finishCoachMarks = useCallback(() => setCoachActive(false), []);
  const openGuideFromCoachMarks = useCallback(() => {
    setCoachActive(false);
    onOpenSiteGuide();
  }, [onOpenSiteGuide]);

  // Press "?" anywhere on the home page to open the guide.
  useEffect(() => {
    const onKey = (e: KeyboardEvent) => {
      const t = e.target as HTMLElement | null;
      if (t && (t.tagName === 'INPUT' || t.tagName === 'TEXTAREA' || t.isContentEditable)) return;
      if (e.key === '?') onOpenSiteGuide();
    };
    window.addEventListener('keydown', onKey);
    return () => window.removeEventListener('keydown', onKey);
  }, [onOpenSiteGuide]);

  const sidebarItems = [
    { icon: Home, label: 'Home', onClick: () => {}, active: true },
    { icon: ChartNoAxesCombined, label: 'My Progress', onClick: onGoToDashboard, active: false },
    { icon: BookOpen, label: 'References', onClick: onGoToAccreditation ?? (() => {}), active: false },
    { icon: Timer, label: 'Study Session', onClick: onGoToStudy ?? (() => {}), active: false },
    { icon: CalendarRange, label: 'Year Plans', onClick: onGoToYearPlans ?? (() => {}), active: false },
  ];
  
  // Aggregate + per-category progress for the Modules hero
  const MODULE_SEGMENTS: Array<{ id: CategoryType; n: string; label: string; accent: string }> = [
    { id: 'architecture-mindset',     n: '01', label: 'Mind',   accent: '#3b82f6' },
    { id: 'science-growth',           n: '02', label: 'Growth', accent: '#f59e0b' },
    { id: 'learning-cheat-codes',     n: '03', label: 'Learn',  accent: '#14b8a6' },
    { id: 'subject-specific-science', n: '04', label: 'Decode', accent: '#ec4899' },
    { id: 'exam-zone',                n: '05', label: 'Exam',   accent: '#ef4444' },
  ];

  const moduleStats = useMemo(() => {
    const perCategory: Record<string, { completed: number; total: number; percent: number }> = {};
    let totalCompleted = 0;
    let total = 0;
    for (const seg of MODULE_SEGMENTS) {
      const courses = allCourses.filter(c => c.category === seg.id);
      const cTotal = courses.length;
      const cCompleted = courses.reduce((acc, c) => {
        const p = userProgress[c.id];
        return acc + (p && p.unlockedSection >= c.sectionsCount ? 1 : 0);
      }, 0);
      perCategory[seg.id] = {
        completed: cCompleted,
        total: cTotal,
        percent: cTotal > 0 ? (cCompleted / cTotal) * 100 : 0,
      };
      totalCompleted += cCompleted;
      total += cTotal;
    }
    return {
      perCategory,
      totalCompleted,
      total,
      overallPercent: total > 0 ? (totalCompleted / total) * 100 : 0,
    };
  }, [allCourses, userProgress]);

  const { totalCompleted: totalModulesCompleted, total: totalModules, overallPercent } = moduleStats;

  // ── Dashboard computed values ──────────────────────────────────────────
  const [todayBlocks, setTodayBlocks] = useState<any[]>([]);
  useEffect(() => {
    if (!studentProfile || studentProfile.subjects.length === 0) { setTodayBlocks([]); return; }
    import('./timetableAlgorithm').then(({ computeSubjectPriorities, allocateSessions, generateWeeklyTimetable, computeWeeksUntilExam }) => {
      try {
        const today = new Date();
        const jsDay = today.getDay();
        const todayDayIndex = jsDay === 0 ? 6 : jsDay - 1;
        const priorities = computeSubjectPriorities(studentProfile.subjects as any, undefined, studentProfile.examStartDate);
        const weeksUntilExam = computeWeeksUntilExam(studentProfile.examStartDate);
        const allocations = allocateSessions(priorities, weeksUntilExam);
        const restDays = studentProfile.restDays || [];
        const blockDuration = studentProfile.defaultBlockDuration ?? 45;
        const timetable = generateWeeklyTimetable(allocations, weeksUntilExam, 0, restDays, blockDuration);
        setTodayBlocks(timetable[todayDayIndex]?.blocks ?? []);
      } catch (err) {
        console.error('Failed to generate timetable blocks:', err);
        setTodayBlocks([]);
      }
    });
  }, [studentProfile]);

  const _daysUntilExam = useMemo(() => {
    if (!studentProfile?.examStartDate) return null;
    const exam = new Date(studentProfile.examStartDate);
    const now = new Date();
    return Math.max(0, Math.ceil((exam.getTime() - now.getTime()) / 86400000));
  }, [studentProfile]);

  const _examProgress = useMemo(() => {
    if (!studentProfile?.examStartDate || !studentProfile?.createdAt) return null;
    const created = new Date(studentProfile.createdAt).getTime();
    const exam = new Date(studentProfile.examStartDate).getTime();
    const now = Date.now();
    const total = exam - created;
    if (total <= 0) return 100;
    return Math.min(100, Math.max(0, ((now - created) / total) * 100));
  }, [studentProfile]);

  const todayKey = toDateKey(new Date());
  const todayCompletions = timetableCompletions?.[todayKey] || [];

  const sessionTypeLabel = (t: string) => {
    if (t === 'new-learning') return 'New';
    if (t === 'practice') return 'Practice';
    if (t === 'revision') return 'Revision';
    return t;
  };

  return (
    <div className="product-shell dashboard-shell min-h-screen bg-[var(--surface-canvas)] text-[var(--ink-primary)] overflow-x-hidden relative selection:bg-[rgba(var(--accent),0.2)]">
      {/* Sidebar — desktop only */}
      <aside
        className={`hidden md:flex flex-col fixed top-0 left-0 h-full z-40 bg-white dark:bg-zinc-900 border-r-[1.5px] border-[#383838] dark:border-zinc-700 overflow-hidden transition-all duration-300 ease-[cubic-bezier(0.16,1,0.3,1)] ${sidebarOpen ? 'w-56' : 'w-[60px]'}`}
      >
        {/* Avatar row — click to toggle */}
        <button
          onClick={() => setSidebarOpen(!sidebarOpen)}
          className="flex items-center gap-3 px-3 py-4 w-full border-b border-[#DED9D3] hover:bg-[#F3EEE7] dark:border-zinc-700 dark:hover:bg-zinc-800 transition-colors"
        >
          <div className="w-9 h-9 rounded-xl border-[1.5px] border-[#383838] overflow-hidden shrink-0 bg-white dark:bg-zinc-700 flex items-center justify-center">
            {userAvatarSeed ? (
              <Avatar seed={userAvatarSeed} alt="Avatar" className="w-full h-full object-cover" />
            ) : (
              <User size={18} strokeWidth={1.5} className="text-zinc-400 dark:text-zinc-500" />
            )}
          </div>
          <span className={`text-sm font-medium text-zinc-700 dark:text-zinc-300 whitespace-nowrap overflow-hidden transition-opacity duration-300 ${sidebarOpen ? 'opacity-100' : 'opacity-0'}`}>
            {userName || 'Student'}
          </span>
        </button>

        {/* Nav items */}
        <nav className="flex-1 flex flex-col gap-1 px-2 mt-2">
          {sidebarItems.map((item) => (
            <button
              key={item.label}
              onClick={item.onClick}
              className={`relative flex items-center gap-3 px-2.5 py-2.5 rounded-xl transition-colors ${item.active ? 'bg-[#FDEBDD] text-[#9A3B0E] dark:bg-zinc-800' : 'hover:bg-[#F3EEE7] dark:hover:bg-zinc-800'}`}
            >
              <div className="shrink-0 flex items-center justify-center w-[18px]">
                <item.icon size={18} strokeWidth={item.active ? 2 : 1.6} className={item.active ? 'text-[#F26B1F]' : 'text-zinc-600 dark:text-zinc-400'} />
              </div>
              <span className={`text-sm font-medium text-zinc-700 dark:text-zinc-300 whitespace-nowrap overflow-hidden transition-opacity duration-300 ${sidebarOpen ? 'opacity-100' : 'opacity-0'}`}>
                {item.label}
              </span>
            </button>
          ))}
        </nav>

        {/* User actions */}
        <div className="border-t border-zinc-200 dark:border-zinc-800 mx-2 pt-2 flex flex-col gap-1">
          {/* Notifications */}
          <button
            data-notification-toggle
            onClick={toggleNotificationPanel}
            className="flex items-center gap-3 px-2.5 py-2 rounded-lg hover:bg-zinc-100 dark:hover:bg-zinc-800 transition-colors"
          >
            <div className="shrink-0 flex items-center justify-center w-[18px] relative">
              <Bell size={18} strokeWidth={1.5} className="text-amber-500" />
            </div>
            <span className={`text-sm font-medium text-zinc-700 dark:text-zinc-300 whitespace-nowrap overflow-hidden transition-opacity duration-300 flex-1 text-left ${sidebarOpen ? 'opacity-100' : 'opacity-0'}`}>
              Notifications
            </span>
          </button>

          {/* Study Passport */}
          <button
            onClick={onOpenPassport}
            className="flex items-center gap-3 px-2.5 py-2 rounded-lg hover:bg-zinc-100 dark:hover:bg-zinc-800 transition-colors"
          >
            <div className="shrink-0 flex items-center justify-center w-[18px]">
              <Award size={18} strokeWidth={1.5} className="text-purple-500" />
            </div>
            <span className={`text-sm font-medium text-zinc-700 dark:text-zinc-300 whitespace-nowrap overflow-hidden transition-opacity duration-300 flex-1 text-left ${sidebarOpen ? 'opacity-100' : 'opacity-0'}`}>
              Study Passport
            </span>
            <span className={`text-xs font-bold text-zinc-400 dark:text-zinc-500 whitespace-nowrap transition-opacity duration-300 ${sidebarOpen ? 'opacity-100' : 'opacity-0'}`}>
              {completedCount}/{totalCount}
            </span>
          </button>

          {/* Change Subjects */}
          {onChangeSubjects && (
            <button
              onClick={onChangeSubjects}
              className="flex items-center gap-3 px-2.5 py-2 rounded-lg hover:bg-zinc-100 dark:hover:bg-zinc-800 transition-colors"
            >
              <div className="shrink-0 flex items-center justify-center w-[18px]">
                <RefreshCw size={18} strokeWidth={1.5} className="text-[#F26B1F]" />
              </div>
              <span className={`text-sm font-medium text-zinc-700 dark:text-zinc-300 whitespace-nowrap overflow-hidden transition-opacity duration-300 flex-1 text-left ${sidebarOpen ? 'opacity-100' : 'opacity-0'}`}>
                Change Subjects
              </span>
            </button>
          )}

          {/* Dark / Light mode toggle */}
          <button
            type="button"
            role="switch"
            aria-checked={settings.darkMode}
            aria-label={settings.darkMode ? 'Use light mode (Beta)' : 'Use dark mode (Beta)'}
            onClick={() => updateSetting('darkMode', !settings.darkMode)}
            className="w-full flex items-center gap-3 px-2.5 py-2 rounded-lg hover:bg-zinc-100 dark:hover:bg-zinc-800 transition-colors"
          >
            <div className="shrink-0 flex items-center justify-center w-[18px]">
              {settings.darkMode ? (
                <Sun size={18} strokeWidth={1.5} className="text-amber-400" />
              ) : (
                <Moon size={18} strokeWidth={1.5} className="text-zinc-600 dark:text-zinc-400" />
              )}
            </div>
            <span className={`text-sm font-medium text-zinc-700 dark:text-zinc-300 whitespace-nowrap overflow-hidden transition-opacity duration-300 ${sidebarOpen ? 'opacity-100' : 'opacity-0'}`}>
              {settings.darkMode ? 'Light Mode (Beta)' : 'Dark Mode (Beta)'}
            </span>
          </button>

          {/* How the app works — the Site Guide */}
          <button
            data-coach="help"
            onClick={onOpenSiteGuide}
            className="flex items-center gap-3 px-2.5 py-2 rounded-lg hover:bg-zinc-100 dark:hover:bg-zinc-800 transition-colors"
          >
            <div className="shrink-0 flex items-center justify-center w-[18px]">
              <HelpCircle size={18} strokeWidth={1.5} className="text-[#F26B1F]" />
            </div>
            <span className={`text-sm font-medium text-zinc-700 dark:text-zinc-300 whitespace-nowrap overflow-hidden transition-opacity duration-300 ${sidebarOpen ? 'opacity-100' : 'opacity-0'}`}>
              How the app works
            </span>
          </button>

          {/* Anonymous product feedback */}
          <button
            onClick={onOpenFeedback}
            className="flex items-center gap-3 px-2.5 py-2 rounded-lg hover:bg-zinc-100 dark:hover:bg-zinc-800 transition-colors"
          >
            <div className="shrink-0 flex items-center justify-center w-[18px]">
              <MessageSquare size={18} strokeWidth={1.5} className="text-zinc-500" />
            </div>
            <span className={`text-sm font-medium text-zinc-700 dark:text-zinc-300 whitespace-nowrap overflow-hidden transition-opacity duration-300 ${sidebarOpen ? 'opacity-100' : 'opacity-0'}`}>
              Help us improve
            </span>
          </button>

          {/* Settings */}
          <button
            onClick={onOpenSettings}
            className="flex items-center gap-3 px-2.5 py-2 rounded-lg hover:bg-zinc-100 dark:hover:bg-zinc-800 transition-colors"
          >
            <div className="shrink-0 flex items-center justify-center w-[18px]">
              <Settings size={18} strokeWidth={1.5} className="text-zinc-500" />
            </div>
            <span className={`text-sm font-medium text-zinc-700 dark:text-zinc-300 whitespace-nowrap overflow-hidden transition-opacity duration-300 ${sidebarOpen ? 'opacity-100' : 'opacity-0'}`}>
              Settings
            </span>
          </button>

          {/* Log Out */}
          <button
            onClick={onLogout}
            className="flex items-center gap-3 px-2.5 py-2 rounded-lg hover:bg-zinc-100 dark:hover:bg-zinc-800 transition-colors"
          >
            <div className="shrink-0 flex items-center justify-center w-[18px]">
              <LogOut size={18} strokeWidth={1.5} className="text-rose-500" />
            </div>
            <span className={`text-sm font-medium text-rose-500 whitespace-nowrap overflow-hidden transition-opacity duration-300 ${sidebarOpen ? 'opacity-100' : 'opacity-0'}`}>
              Log Out
            </span>
          </button>
        </div>

        {/* Collapse toggle */}
        <button
          onClick={() => setSidebarOpen(!sidebarOpen)}
          className="flex items-center gap-3 px-2.5 py-3 mx-2 mb-3 rounded-lg hover:bg-zinc-100 dark:hover:bg-zinc-800 transition-colors"
        >
          <div className={`shrink-0 flex items-center justify-center w-[18px] transition-transform duration-300 ${sidebarOpen ? '' : 'rotate-180'}`}>
            <PanelLeft size={18} strokeWidth={1.5} className="text-zinc-400 dark:text-zinc-500" />
          </div>
          <span className={`text-sm font-medium text-zinc-400 dark:text-zinc-500 whitespace-nowrap overflow-hidden transition-opacity duration-300 ${sidebarOpen ? 'opacity-100' : 'opacity-0'}`}>
            Collapse
          </span>
        </button>
      </aside>

      {/* Main content */}
      <div className={`flex-1 flex flex-col items-center pt-8 md:pt-16 pb-40 md:pb-32 transition-all duration-300 ease-[cubic-bezier(0.16,1,0.3,1)] ${sidebarOpen ? 'md:ml-56' : 'md:ml-[60px]'}`}>
      <div className="w-full max-w-7xl px-6">
        {/* ── Greeting — simple typography on cream ── */}
        <MotionDiv
          initial={{ opacity: 0, y: 12 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.5, ease: [0.16, 1, 0.3, 1] }}
          className="mb-6 flex items-start justify-between gap-4"
        >
          <div className="min-w-0">
            <p className="text-[12px] font-semibold uppercase tracking-[0.2em] mb-3" style={{ color: COLORS.accent }}>
              Learning Lab
            </p>
            <h1 className="font-serif tracking-tight leading-tight font-bold text-[#1A1A1A] dark:text-white" style={{ fontSize: 'clamp(28px, 5vw, 36px)' }}>
              {(() => { const h = new Date().getHours(); const firstName = userName?.split(' ')[0] || ''; const name = firstName ? `, ${firstName}` : ''; return h < 12 ? `Good morning${name}.` : h < 18 ? `Good afternoon${name}.` : `Good evening${name}.`; })()}
            </h1>
            <p className="mt-2 text-[#78716C] dark:text-zinc-400" style={{ fontSize: 15 }}>
              {(() => {
                const h = new Date().getHours();
                const completed = allCourses.filter(c => { const p = userProgress[c.id]; return p && p.unlockedSection >= c.sectionsCount; }).length;
                const inProgress = allCourses.filter(c => { const p = userProgress[c.id]; return p && p.unlockedSection > 0 && p.unlockedSection < c.sectionsCount; }).length;
                const allBlocksDone = todayBlocks.length > 0 && todayBlocks.every((_b: any, i: number) => todayCompletions.includes(`block-${i}`));
                if (completed === allCourses.length) return 'You\'ve completed the full curriculum. Remarkable.';
                if (h >= 18 && allBlocksDone) return 'All done for today. Quick review before tomorrow?';
                if (h >= 18) return 'Wind down with a final session or review your progress.';
                if (h < 12 && studentProfile) return 'Here\'s your plan for today.';
                if (completed > 0) return `You've completed ${completed} of ${allCourses.length} modules.`;
                if (inProgress > 0) return `You have ${inProgress} module${inProgress !== 1 ? 's' : ''} in progress.`;
                return 'Pick a module to start your journey.';
              })()}
            </p>
          </div>
          <button
            type="button"
            onClick={onOpenMobileProfile}
            aria-label="Open profile and settings"
            className="relative mt-0.5 flex h-11 w-11 shrink-0 items-center justify-center overflow-hidden rounded-full border-[1.5px] border-[#383838] bg-white shadow-[2px_2px_0_0_#383838] active:translate-x-0.5 active:translate-y-0.5 active:shadow-none md:hidden dark:border-zinc-600 dark:bg-zinc-800"
          >
            {userAvatarSeed ? (
              <Avatar seed={userAvatarSeed} alt="" className="h-full w-full object-cover" />
            ) : (
              <User size={18} strokeWidth={1.6} className="text-zinc-500" />
            )}
            {hasUnreadNotifications && <span className="absolute right-0.5 top-0.5 h-2.5 w-2.5 rounded-full border-2 border-white bg-rose-500 dark:border-zinc-800" />}
          </button>
        </MotionDiv>

        {/* Pick up where you left off — deep-link back to the last module/tool */}
        <ResumeCard
          uid={uid}
          allCourses={allCourses}
          userProgress={userProgress}
          onSelectModule={onSelectModule}
          onOpenTool={onOpenTool}
        />

        {/* Student Home Dashboard */}
        <AnimatePresence initial={false}>
          {dashboardVisible && (
            <MotionDiv
              ref={dashboardRef}
              key="home-dashboard"
              initial={reduceMotion ? { opacity: 0 } : { height: 0, opacity: 0, y: -12, scale: 0.992 }}
              animate={reduceMotion ? { opacity: 1 } : { height: 'auto', opacity: 1, y: 0, scale: 1 }}
              exit={reduceMotion ? { opacity: 0 } : { height: 0, opacity: 0, y: -10, scale: 0.992 }}
              transition={reduceMotion ? { duration: 0.12 } : {
                height: { duration: 0.46, ease: [0.16, 1, 0.3, 1] },
                opacity: { duration: 0.24, ease: 'easeOut' },
                y: { duration: 0.4, ease: [0.16, 1, 0.3, 1] },
                scale: { duration: 0.4, ease: [0.16, 1, 0.3, 1] },
              }}
              className="overflow-hidden"
              style={{ scrollMarginTop: 24, transformOrigin: 'top center', willChange: 'height, opacity, transform' }}
            >
              <section aria-label="Home dashboard" className="pb-6">
            {/* Daily plan first; supporting information follows. */}
            <div className="grid grid-cols-1 md:grid-cols-2 gap-3">
              {/* TODAY */}
              <div data-coach="study" className="md:col-span-2 px-5 py-5 md:px-7 md:py-6 bg-white dark:bg-zinc-900 border-[1.5px] border-[#383838] dark:border-zinc-700" style={{ borderRadius: 16 }}>
                <div className="flex items-start justify-between gap-4 mb-5">
                  <div>
                    <p className="text-[10px] font-bold uppercase tracking-[0.18em] mb-1.5 text-[#A0968D] dark:text-zinc-500">Today’s plan</p>
                    <h2 className="font-serif text-2xl md:text-3xl font-bold text-[#1A1A1A] dark:text-white">
                      {todayBlocks.length > 0
                        ? `${todayBlocks.length} focused session${todayBlocks.length !== 1 ? 's' : ''}`
                        : 'Nothing scheduled'}
                    </h2>
                    <p className="mt-1 text-xs text-[#78716C] dark:text-zinc-400">{pointsBalance ?? 0} JP available</p>
                  </div>
                  {onGoToStudy && todayBlocks.length > 0 && !todayBlocks.every((_b, i) => todayCompletions.includes(`block-${i}`)) && (
                    <button
                      onClick={onGoToStudy}
                      className="shrink-0 flex items-center gap-1.5 text-xs font-bold px-4 py-2.5 rounded-lg text-white border-2 border-[#1A1A1A] bg-[#F26B1F] shadow-[3px_3px_0_0_#1A1A1A] transition-transform active:translate-x-[3px] active:translate-y-[3px] active:shadow-none"
                    >
                      Study Now <ArrowRight size={12} />
                    </button>
                  )}
                </div>
                {todayBlocks.length === 0 ? (
                  /* Rest state — Gentler Streak's lesson: an empty day is a
                     feature, not a hole. Same ring language as completion. */
                  <div className="flex items-center gap-4 rounded-xl px-4 py-5">
                    <span aria-hidden="true" className="flex h-11 w-11 shrink-0 items-center justify-center rounded-full border-[2.5px] border-[#3A8D5F]">
                      <Check size={18} strokeWidth={2.6} className="text-[#3A8D5F]" />
                    </span>
                    <div>
                      <p className="font-serif text-[17px] font-bold text-[#1A1A1A] dark:text-white">Nothing scheduled — rest counts.</p>
                      <p className="mt-0.5 text-xs leading-relaxed text-[#78716C] dark:text-zinc-400">A clear day is part of the plan. Come back fresh, or open one topic that has been on your mind.</p>
                    </div>
                  </div>
                ) : todayBlocks.every((_b, i) => todayCompletions.includes(`block-${i}`)) ? (
                  <div className="flex items-center gap-4 rounded-xl px-4 py-5">
                    <span aria-hidden="true" className="flex h-11 w-11 shrink-0 items-center justify-center rounded-full bg-[#3A8D5F]">
                      <Check size={18} strokeWidth={2.6} className="text-white" />
                    </span>
                    <div>
                      <p className="font-serif text-[17px] font-bold text-[#1A1A1A] dark:text-white">All done. Rest counts.</p>
                      <p className="mt-0.5 text-xs leading-relaxed text-[#78716C] dark:text-zinc-400">Every block finished — proper recovery is how the work sticks.</p>
                    </div>
                  </div>
                ) : (
                  /* Stepped rail — the day reads as a sequence: done, current, upcoming.
                     One warm glyph per screen; the rail itself stays hairline-quiet. */
                  <div className="relative">
                    <span aria-hidden="true" className="absolute w-px bg-[#E5E1DA] dark:bg-zinc-700" style={{ left: 10.5, top: 18, bottom: 18 }} />
                    {todayBlocks.slice(0, 4).map((block, i) => {
                      const complete = todayCompletions.includes(`block-${i}`);
                      const nextIndex = todayBlocks.findIndex((_candidate, index) => !todayCompletions.includes(`block-${index}`));
                      const isNext = i === nextIndex;
                      return (
                        <div key={i} className="relative flex items-center gap-3.5 py-2">
                          <span
                            aria-hidden="true"
                            className={`relative z-[1] flex h-[22px] w-[22px] shrink-0 items-center justify-center rounded-full ${
                              complete
                                ? 'bg-[#3A8D5F]'
                                : isNext
                                  ? 'border-[1.5px] border-[#F26B1F] bg-white dark:bg-zinc-900'
                                  : 'border-[1.5px] border-[#D6D3D0] bg-white dark:border-zinc-600 dark:bg-zinc-900'
                            }`}
                          >
                            {complete && <Check size={12} strokeWidth={2.6} className="text-white" />}
                            {isNext && <span className="h-[9px] w-[9px] rounded-full bg-[#F26B1F]" />}
                          </span>
                          <div className="min-w-0 flex-1">
                            <span className={`block truncate text-sm ${
                              complete
                                ? 'font-semibold text-[#A8A29E] dark:text-zinc-500'
                                : isNext
                                  ? 'font-bold text-[#1A1A1A] dark:text-white'
                                  : 'font-semibold text-[#57534E] dark:text-zinc-300'
                            }`}>{block.subjectName}</span>
                            <p className={`mt-0.5 text-[11px] ${complete ? 'text-[#C2BCB4] dark:text-zinc-600' : 'text-[#78716C] dark:text-zinc-400'}`}>
                              {sessionTypeLabel(block.sessionType)} · {block.durationMinutes} min
                            </p>
                          </div>
                          {isNext && onGoToStudy && (
                            <button onClick={onGoToStudy} className="shrink-0 text-xs font-bold text-[#F26B1F] hover:underline">
                              Begin →
                            </button>
                          )}
                        </div>
                      );
                    })}
                  </div>
                )}
              </div>

              {/* PROGRESS — deliberately secondary */}
              <div className="px-5 py-4 bg-white dark:bg-zinc-900 border-[1.5px] border-[#383838] dark:border-zinc-700" style={{ borderRadius: 14 }}>
                <div className="flex items-center justify-between gap-4">
                  <div>
                    <p className="text-[10px] font-bold uppercase tracking-widest mb-2 text-[#A8A29E] dark:text-zinc-500">Programme progress</p>
                    <div className="flex items-baseline gap-1">
                      <span className="font-apercu font-black tabular-nums leading-none text-[#1A1A1A] dark:text-white text-3xl">
                    {Math.round(overallPercent)}
                      </span>
                      <span className="font-apercu font-bold text-lg text-[#A8A29E] dark:text-zinc-500">%</span>
                    </div>
                  </div>
                  <span className="text-xs font-semibold text-[#78716C] dark:text-zinc-400">{completedCount}/{totalCount} modules</span>
                </div>
                <div className="h-1.5 rounded-full overflow-hidden bg-[#EDEBE8] dark:bg-zinc-700 mt-2.5">
                  <div className="h-full rounded-full transition-all duration-700" style={{ backgroundColor: COLORS.accent, width: `${overallPercent}%` }} />
                </div>
                {northStar && (
                  <p className="mt-2 text-[11px] italic leading-relaxed truncate text-[#A8A29E] dark:text-zinc-500">&ldquo;{northStar.statement}&rdquo;</p>
                )}
              </div>

              {/* Weekly activity bar chart */}
              {(() => {
                const today = new Date();
                const currentDayIdx = today.getDay() === 0 ? 6 : today.getDay() - 1;
                const DAY_LABELS = ['M','T','W','T','F','S','S'];

                // Compute daily points for current week
                const weekPoints: number[] = DAY_LABELS.map((_, i) => {
                  const dayDate = new Date(today);
                  dayDate.setDate(today.getDate() - (currentDayIdx - i));
                  const dateKey = toDateKey(dayDate);
                  const blocks = timetableCompletions?.[dateKey]?.length ?? 0;
                  return Math.min(blocks, 4);
                });

                // Compute streak: consecutive days going backwards with points >= 1
                let streakCount = 0;
                const startIdx = weekPoints[currentDayIdx] >= 1 ? currentDayIdx : currentDayIdx - 1;
                for (let d = startIdx; d >= 0; d--) {
                  if (weekPoints[d] >= 1) streakCount++;
                  else break;
                }
                // Also count beyond this week via the streak prop
                if (streak && startIdx >= 0 && weekPoints[0] >= 1) {
                  streakCount = Math.max(streakCount, streak.currentStreak);
                }

                // The streak number is the identity; the month grid is the evidence —
                // the same apricot-cell vocabulary as the Atlas year strips.
                const monthLabel = today.toLocaleString('en-IE', { month: 'long' });
                const daysInMonth = new Date(today.getFullYear(), today.getMonth() + 1, 0).getDate();
                const firstDow = (() => { const d = new Date(today.getFullYear(), today.getMonth(), 1).getDay(); return d === 0 ? 6 : d - 1; })();
                const dayCells = Array.from({ length: daysInMonth }, (_, i) => {
                  const date = new Date(today.getFullYear(), today.getMonth(), i + 1);
                  const done = timetableCompletions?.[toDateKey(date)]?.length ?? 0;
                  return { day: i + 1, done, isToday: i + 1 === today.getDate(), isFuture: i + 1 > today.getDate() };
                });

                return (
                  <div className="h-full">
                    <div className="h-full flex items-center gap-5 bg-white dark:bg-zinc-900 px-5 py-4 border-[1.5px] border-[#383838] dark:border-zinc-700" style={{ borderRadius: 14 }}>
                      <div className="flex flex-col justify-center shrink-0" style={{ minWidth: 72 }}>
                        <p className="font-apercu font-black tabular-nums leading-none text-[#1A1A1A] dark:text-white" style={{ fontSize: 44 }}>{streakCount}</p>
                        <p className="mt-1.5 text-[10px] font-bold uppercase tracking-[0.16em] text-[#A0968D] dark:text-zinc-500">Day streak</p>
                      </div>
                      <div className="w-px self-stretch bg-[#EDEBE8] dark:bg-zinc-800" />
                      <div className="min-w-0">
                        <p className="mb-1.5 text-[10px] font-bold uppercase tracking-[0.14em] text-[#A8A29E] dark:text-zinc-500">{monthLabel}</p>
                        <div className="grid grid-cols-7 gap-1" role="img" aria-label={`Days studied in ${monthLabel}: ${dayCells.filter(c => c.done > 0).length}`}>
                          {Array.from({ length: firstDow }).map((_, i) => <span key={`pad-${i}`} className="h-3.5 w-3.5" />)}
                          {dayCells.map(c => (
                            <span
                              key={c.day}
                              className={`h-3.5 w-3.5 rounded-[4px] ${
                                c.done === 0
                                  ? c.isFuture
                                    ? 'bg-[#F8F6F3] dark:bg-zinc-800/50'
                                    : 'bg-[#F1EEE9] dark:bg-zinc-800'
                                  : ''
                              } ${c.isToday ? 'ring-[1.5px] ring-inset ring-[#1A1A1A] dark:ring-white' : ''}`}
                              style={c.done > 0 ? { backgroundColor: c.done >= 3 ? 'rgba(242,107,31,0.72)' : 'rgba(242,107,31,0.45)' } : undefined}
                            />
                          ))}
                        </div>
                      </div>
                    </div>
                  </div>
                );
              })()}

              {/* RECOMMENDED */}
              {smartRecommendation && (
                <button
                  onClick={() => onRecommendationAction?.(smartRecommendation.category)}
                  className="px-5 py-4 text-left transition-transform hover:-translate-y-0.5 bg-white dark:bg-zinc-900 border-[1.5px] border-[#383838] dark:border-zinc-700"
                  style={{ borderRadius: 14 }}
                >
                  <p className="text-[10px] font-bold uppercase tracking-widest mb-1 text-[#A8A29E] dark:text-zinc-500">Recommended</p>
                  <p className="text-xs font-semibold text-[#1A1A1A] dark:text-white truncate">{smartRecommendation.title}</p>
                  <p className="text-[11px] mt-0.5 text-[#A8A29E] dark:text-zinc-500">{smartRecommendation.description}</p>
                </button>
              )}

              {/* QUEST */}
              {questState && (
                <div className="overflow-hidden bg-white dark:bg-zinc-900 border-[1.5px] border-[#383838] dark:border-zinc-700" style={{ borderRadius: 14 }}>
                  {/* Band header — the quest wears its identity like the Atlas covers. */}
                  <div className="flex items-center justify-between px-5 py-2" style={{ backgroundColor: 'rgba(242,107,31,0.13)' }}>
                    <p className="text-[10px] font-bold uppercase tracking-[0.16em]" style={{ color: '#B5500F' }}>
                      {questState.isOnboarding ? `Day ${questState.dayNumber} Quest` : 'Daily Quest'}
                    </p>
                    <span className="text-[10px] font-bold tabular-nums" style={{ color: '#B5500F' }}>{questState.quest.rewardPoints} JP</span>
                  </div>
                  <div className="px-5 pb-4 pt-3">
                  <p className="text-xs font-semibold text-[#1A1A1A] dark:text-white">{questState.quest.title}</p>
                  <p className="text-[11px] mt-0.5 text-[#A8A29E] dark:text-zinc-500">{questState.quest.description}</p>
                  <div className="mt-2.5 flex items-center gap-2">
                    <div className="flex-1 h-2.5 rounded-full overflow-hidden bg-[#EDEBE8] dark:bg-zinc-700">
                      <div className="h-full rounded-full transition-all duration-500" style={{ width: `${Math.min(100, (questState.current / questState.quest.target) * 100)}%`, backgroundColor: questState.isCompleted ? '#3A8D5F' : 'rgba(242,107,31,0.62)' }} />
                    </div>
                    <span className="text-[10px] font-bold tabular-nums text-[#A8A29E] dark:text-zinc-500">{questState.isCompleted ? 'Completed' : `${Math.min(questState.current, questState.quest.target)}/${questState.quest.target}`}</span>
                  </div>
                  {questState.isCompleted && !questState.isClaimed && onClaimQuestReward && (
                    <button onClick={onClaimQuestReward} className="mt-3 w-full py-2.5 rounded-lg text-xs font-bold text-white border-2 border-[#1A1A1A] bg-[#F26B1F] shadow-[3px_3px_0_0_#1A1A1A] active:translate-x-[3px] active:translate-y-[3px] active:shadow-none">
                      Claim {questState.quest.rewardPoints} JP
                    </button>
                  )}
                  {questState.isClaimed && (
                    <p className="mt-2 text-[10px] font-bold" style={{ color: '#3A8D5F' }}>Claimed</p>
                  )}
                  </div>
                </div>
              )}
            </div>
              </section>
            </MotionDiv>
          )}
        </AnimatePresence>

        {/* ── Section cards — top-level dashboard nav ── */}
        <MotionDiv
          initial={{ opacity: 0, y: 8 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.4, delay: 0.15, ease: [0.16, 1, 0.3, 1] }}
          className="grid grid-cols-1 md:grid-cols-2 gap-3 md:gap-4"
        >
          <div data-coach="modules">
            <SectionCard
              eyebrow="The Programme"
              title="Modules"
              subtitle={`Five worlds. ${totalModules} modules. ${totalModulesCompleted} complete.`}
              icon={<ModulesIcon />}
              onClick={onGoToModules}
            />
          </div>
          <div data-coach="launchpad">
            <SectionCard
              eyebrow="Explore"
              title="Launchpad"
              subtitle="Tools to plan, understand, and track."
              icon={<InnovationZoneIcon />}
              onClick={onGoToInnovationZone}
            />
          </div>
          <SectionCard
            eyebrow="Dashboard"
            title="My Progress"
            subtitle="Study rhythm, confidence, practice and programme progress."
            icon={<MyProgressIcon />}
            onClick={onGoToDashboard}
          />
          <SectionCard
            eyebrow="Guided"
            title="Learning Paths"
            subtitle="Curated routes from foundation to mastery."
            icon={<LearningPathsIcon />}
            onClick={onGoToLearningPaths}
          />
          <SectionCard
            eyebrow="Build Your World"
            title="My Journey"
            subtitle="Turn your progress into an island of your own."
            icon={<MyJourneyIcon />}
            onClick={onGoToJourney}
            className="md:col-span-2"
          />
        </MotionDiv>

      </div>
      </div>

      {/* One-time first-visit coach marks — end by pointing at the "?". */}
      {coachActive && (
        <FirstVisitCoachMarks
          uid={uid}
          onFinish={finishCoachMarks}
          onOpenGuide={openGuideFromCoachMarks}
        />
      )}
    </div>
  );
};
