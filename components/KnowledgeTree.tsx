/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
*/

import React, { useState, useEffect, useCallback } from 'react';
import { MotionDiv } from './Motion';
import {
  User, Home, PanelLeft, ChartNoAxesCombined, Award, BookOpen, CalendarRange, Settings, LogOut, Sun, Moon, RefreshCw, Timer, Bell, MessageSquare, HelpCircle, Compass, Route, Mountain
} from 'lucide-react';
import FirstVisitCoachMarks, { coachMarksSeen } from './FirstVisitCoachMarks';
import ResumeCard from './ResumeCard';
import HomeNextStep from './HomeNextStep';
import { KnowledgeTree as DesktopKnowledgeTree } from './KnowledgeTree.desktop';
import { useMobileAppDesign } from '../hooks/useMobileAppDesign';
import { type GamificationState } from '../gamificationConfig';
import { type CourseData } from './Library';
import { type UserSettings } from '../types';
import { toDateKey } from './subjectData';
import { type StudyBlock } from './subjectData';
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
  gamificationState?: GamificationState | null;
  onPlannedStudy?: (block: StudyBlock, index: number) => void;
}

const noop = () => {};

const MobileKnowledgeTree: React.FC<KnowledgeTreeProps> = ({ onSelectCategory: _onSelectCategory, onGoToModules, onGoToInnovationZone, onGoToDashboard, onGoToLearningPaths, onGoToJourney, onGoToStudy, onGoToInsights: _onGoToInsights, onGoToAccreditation, onGoToYearPlans, allCourses, onSelectModule, categoryTitles: _categoryTitles, userProgress, userName, userAvatarSeed, onLogout, onOpenSettings, onOpenPassport, onChangeSubjects, settings, updateSetting, unlockedThemes: _unlockedThemes = [], completedCount, totalCount, studentProfile, timetableCompletions, onOpenTool, uid, onOpenSiteGuide = noop, onOpenFeedback = noop, onOpenMobileProfile = noop, hasUnreadNotifications = false, gamificationState, onPlannedStudy }) => {
  const [sidebarOpen, setSidebarOpen] = useState(false);
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
    { icon: Compass, label: 'Launchpad', onClick: onGoToInnovationZone, active: false },
    { icon: Route, label: 'Learning paths', onClick: onGoToLearningPaths, active: false },
    { icon: Mountain, label: 'My Journey', onClick: onGoToJourney, active: false },
    { icon: BookOpen, label: 'References', onClick: onGoToAccreditation ?? (() => {}), active: false },
    { icon: Timer, label: 'Study Session', onClick: onGoToStudy ?? (() => {}), active: false },
    { icon: CalendarRange, label: 'Year Plans', onClick: onGoToYearPlans ?? (() => {}), active: false },
  ];
  
  // ── Dashboard computed values ──────────────────────────────────────────
  const [todayBlocks, setTodayBlocks] = useState<StudyBlock[]>([]);
  const [planReady, setPlanReady] = useState(false);
  const [planError, setPlanError] = useState(false);
  useEffect(() => {
    setPlanError(false);
    if (!studentProfile || studentProfile.subjects.length === 0) { setTodayBlocks([]); setPlanReady(true); return; }
    setPlanReady(false);
    let cancelled = false;
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
        if (!cancelled) { setTodayBlocks(timetable[todayDayIndex]?.blocks ?? []); setPlanReady(true); }
      } catch (err) {
        console.error('Failed to generate timetable blocks:', err);
        if (!cancelled) { setTodayBlocks([]); setPlanReady(true); setPlanError(true); }
      }
    }).catch(() => {
      if (!cancelled) { setTodayBlocks([]); setPlanReady(true); setPlanError(true); }
    });
    return () => { cancelled = true; };
  }, [studentProfile]);

  const todayKey = toDateKey(new Date());
  const todayCompletions = timetableCompletions?.[todayKey] || [];

  return (
    <div className="mobile-home-shell product-shell dashboard-shell min-h-screen bg-[var(--surface-canvas)] text-[var(--ink-primary)] overflow-x-hidden relative selection:bg-[rgba(var(--accent),0.2)]">
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
              data-coach={item.label === 'Launchpad' ? 'launchpad' : undefined}
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
      <div className="home-next-step w-full max-w-7xl px-5 sm:px-6">
        {/* ── Greeting — simple typography on cream ── */}
        <MotionDiv
          initial={{ opacity: 0, y: 12 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.5, ease: [0.16, 1, 0.3, 1] }}
          className="mb-6 flex items-start justify-between gap-4"
        >
          <div className="min-w-0">
            <p className="text-[12px] font-semibold uppercase tracking-[0.2em] mb-3" style={{ color: COLORS.accent }}>
              Your learning, your way
            </p>
            <p className="text-[15px] leading-relaxed text-[var(--ink-secondary)]">{(() => { const h = new Date().getHours(); const firstName = userName?.split(' ')[0] || ''; const name = firstName ? `, ${firstName}` : ''; return h < 12 ? `Good morning${name}.` : h < 18 ? `Good afternoon${name}.` : `Good evening${name}.`; })()}</p>
            <h1 className="mt-1 font-serif text-[36px] font-semibold tracking-tight leading-tight text-[var(--ink-primary)]">Your next step.</h1>

          </div>
          <button
            type="button"
            onClick={onOpenMobileProfile}
            aria-label="Open profile and settings"
            data-coach="help"
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
          onBrowseModules={onGoToModules}
        />

        <HomeNextStep ready={planReady} error={planError} onPlannedStudy={onPlannedStudy} blocks={todayBlocks} completions={todayCompletions} hasProfile={Boolean(studentProfile?.subjects.length)} gamification={gamificationState} onStudy={onGoToStudy} onPlan={onOpenTool ? () => onOpenTool('planner') : undefined} onProgress={onGoToDashboard} />
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

/** Desktop remains on the pre-rollout screen. */
export const KnowledgeTree: React.FC<KnowledgeTreeProps> = props => {
  const mobile = useMobileAppDesign();
  return mobile ? <MobileKnowledgeTree {...props} /> : <DesktopKnowledgeTree {...props} />;
};
