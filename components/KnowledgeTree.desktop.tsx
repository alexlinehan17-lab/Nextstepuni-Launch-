/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
*/

import React, { useState, useEffect, useCallback } from 'react';
import {
  User, Home, PanelLeft, ChartNoAxesCombined, Award, BookOpen, CalendarRange, Settings, LogOut, Sun, Moon, RefreshCw, Timer, Bell, MessageSquare, HelpCircle
} from 'lucide-react';
import FirstVisitCoachMarks, { coachMarksSeen } from './FirstVisitCoachMarks';
import StudentHomeContent from './StudentHomeContent';
import GetPointsButton from './GetPointsButton';
import type { StudySessionRecord } from '../studySessionData';
import { type CourseData } from './Library';
import { type UserSettings } from '../types';
import Avatar from './Avatar';
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
  onGoToDirection?: () => void;
  studySessions?: StudySessionRecord[];
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

export const KnowledgeTree: React.FC<KnowledgeTreeProps> = ({ onSelectCategory: _onSelectCategory, onGoToModules, onGoToInnovationZone, onGoToDashboard, onGoToLearningPaths, onGoToJourney, onGoToDirection, studySessions, onGoToStudy, onGoToInsights: _onGoToInsights, onGoToAccreditation, onGoToYearPlans, allCourses, onSelectModule, categoryTitles, userProgress, userName, userAvatarSeed, onLogout, onOpenSettings, onOpenPassport, onChangeSubjects, settings, updateSetting, unlockedThemes: _unlockedThemes = [], completedCount, totalCount, streak: _streak, pointsBalance, northStar: _northStar, studentProfile: _studentProfile, timetableCompletions: _timetableCompletions, smartRecommendation: _smartRecommendation, questState: _questState, onClaimQuestReward: _onClaimQuestReward, onRecommendationAction: _onRecommendationAction, onOpenTool, uid, onOpenSiteGuide = noop, onOpenFeedback = noop, onOpenMobileProfile = noop, hasUnreadNotifications = false }) => {
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
    { icon: BookOpen, label: 'References', onClick: onGoToAccreditation ?? (() => {}), active: false },
    { icon: Timer, label: 'Study Session', onClick: onGoToStudy ?? (() => {}), active: false },
    { icon: CalendarRange, label: 'Year Plans', onClick: onGoToYearPlans ?? (() => {}), active: false },
  ];

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
          <GetPointsButton uid={uid} expanded={sidebarOpen} />
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

      {/* The account drawer stays in its existing shell. */}
      <div className={`flex-1 bg-white dark:bg-[#181b18] transition-[margin] duration-300 ${sidebarOpen ? 'md:ml-56' : 'md:ml-[60px]'}`}>
        <StudentHomeContent uid={uid} userName={userName} userAvatarSeed={userAvatarSeed} onOpenMobileProfile={onOpenMobileProfile} hasUnreadNotifications={hasUnreadNotifications} allCourses={allCourses} categoryTitles={categoryTitles} userProgress={userProgress} studySessions={studySessions} pointsBalance={pointsBalance} onSelectModule={onSelectModule} onGoToStudy={onGoToStudy} onGoToModules={onGoToModules} onGoToDashboard={onGoToDashboard} onGoToLearningPaths={onGoToLearningPaths} onGoToDirection={onGoToDirection} onGoToJourney={onGoToJourney} onGoToInnovationZone={onGoToInnovationZone} onOpenTool={onOpenTool} />

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
