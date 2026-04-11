/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
*/

import React, { useState, useMemo, useEffect } from 'react';
import { AnimatePresence } from 'framer-motion';
import { MotionCircle, MotionDiv } from './Motion';
import {
  Sprout, Rocket, Target,
  Fingerprint, ArrowRight, BarChart3, Compass, Lightbulb, KeyRound,
  User, Home, PanelLeft, Award, Settings, LogOut, Sun, Moon, RefreshCw, Mountain, Timer, Tag, X, Dumbbell
} from 'lucide-react';
import { getAvatarUrl } from '../components/Auth';
import { CourseData, BentoModuleTile } from './Library';
import { UserSettings } from '../types';
import { type AthleteRank, ATHLETE_RANKS } from '../gamificationConfig';
import { toDateKey } from './subjectData';
import { getSubjectHex } from '../utils/subjectColors';

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
  onGoToInnovationZone: () => void;
  onGoToDashboard: () => void;
  onGoToLearningPaths: () => void;
  onGoToJourney: () => void;
  onGoToStudy?: () => void;
  onGoToInsights?: () => void;
  onGoToTrainingHub?: () => void;
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
  studentProfile?: { subjects: { subjectName: string; currentGrade: string; targetGrade: string; level: string }[]; examStartDate: string; restDays?: string[]; defaultBlockDuration?: number; createdAt?: string } | null;
  timetableCompletions?: Record<string, string[]>;
  smartRecommendation?: { id: string; title: string; description: string; category: string } | null;
  questState?: { quest: { title: string; description: string; rewardPoints: number; target: number }; current: number; isCompleted: boolean; isClaimed: boolean; dayNumber: number; isOnboarding: boolean } | null;
  onClaimQuestReward?: () => void;
  onRecommendationAction?: (action: string) => void;
  onDevRankUp?: (rank: AthleteRank) => void;
}

const ActivityRing = ({
  progress,
  size = 52,
  strokeWidth = 4,
  color = "#3b82f6"
}: {
  progress: number,
  size?: number,
  strokeWidth?: number,
  color?: string
}) => {
  const radius = (size - strokeWidth) / 2;
  const circumference = 2 * Math.PI * radius;
  const offset = circumference - (progress / 100) * circumference;
  const isZero = progress === 0;
  const isComplete = progress >= 100;

  return (
    <div className="relative flex items-center justify-center shrink-0" style={{ width: size, height: size }}>
      <svg className="w-full h-full -rotate-90 overflow-visible" viewBox={`0 0 ${size} ${size}`}>
        {/* Track ring — accent-tinted instead of plain grey */}
        <circle
          cx={size / 2}
          cy={size / 2}
          r={radius}
          stroke={color}
          strokeWidth={strokeWidth}
          fill="transparent"
          opacity={0.1}
        />
        {/* Progress arc with glow */}
        {!isZero && (
          <MotionCircle
            cx={size / 2}
            cy={size / 2}
            r={radius}
            stroke={color}
            strokeWidth={strokeWidth + 0.5}
            fill="transparent"
            strokeDasharray={circumference}
            initial={{ strokeDashoffset: circumference }}
            whileInView={{ strokeDashoffset: offset }}
            viewport={{ once: true }}
            transition={{ duration: 1.5, delay: 0.5, ease: "easeOut" }}
            strokeLinecap="round"
            style={{ filter: `drop-shadow(0 0 4px ${color}40)` }}
          />
        )}
      </svg>
      <div className="absolute flex items-baseline justify-center leading-none">
        {isComplete ? (
          <svg width="16" height="16" viewBox="0 0 16 16" fill="none">
            <path d="M3.5 8.5L6.5 11.5L12.5 4.5" stroke={color} strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" />
          </svg>
        ) : isZero ? (
          <span className="text-[10px] font-semibold tracking-wide" style={{ color }}>Start</span>
        ) : (
          <span className="text-[13px] font-bold" style={{ color }}>{Math.round(progress)}</span>
        )}
      </div>
    </div>
  );
};

interface BentoTileProps {
  icon: any,
  title: string,
  subtitle: string,
  description?: string,
  onClick: () => void,
  accentHex: string,
  progress?: number,
  hideProgress?: boolean,
  className?: string,
  delay?: number
}

const BentoTile: React.FC<BentoTileProps> = ({
  icon: Icon,
  title,
  subtitle,
  description,
  onClick,
  accentHex,
  progress = 0,
  hideProgress = false,
  className = "",
  delay = 0
}) => {
  return (
    <MotionDiv
      initial={{ opacity: 0, y: 8 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.4, delay, ease: [0.16, 1, 0.3, 1] }}
      onClick={onClick}
      className={`card-styled group relative overflow-hidden rounded-2xl bg-white dark:bg-zinc-900 border border-zinc-200 dark:border-zinc-800 cursor-pointer transition-all duration-300 hover:border-zinc-300 dark:hover:border-zinc-700 hover:shadow-lg md:hover:-translate-y-1 focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-[rgba(var(--accent),0.5)] focus-visible:ring-offset-2 ${className}`}
    >
      {/* Accent top bar — always visible when started, reveals on hover otherwise */}
      <div
        className={`absolute top-0 left-0 right-0 h-[3px] transition-opacity duration-300 ${!hideProgress && progress > 0 ? 'opacity-100' : 'opacity-0 group-hover:opacity-100'}`}
        style={{ backgroundColor: accentHex }}
      />
      {/* Hover glow */}
      <div
        className="absolute inset-0 opacity-0 group-hover:opacity-100 transition-opacity duration-500 pointer-events-none"
        style={{ background: `radial-gradient(ellipse at 50% 0%, ${accentHex}08 0%, transparent 70%)` }}
      />
      <div className="relative p-8 h-full flex flex-col justify-between">
        <div>
          <div className="flex items-center justify-between mb-8">
            <div
              className="w-12 h-12 rounded-xl flex items-center justify-center transition-transform duration-300 group-hover:scale-110"
              style={{ color: accentHex, backgroundColor: accentHex + '12' }}
            >
              <Icon size={24} strokeWidth={1.5} />
            </div>

            <div className="opacity-0 group-hover:opacity-100 transition-all duration-300 group-hover:translate-x-0.5">
               <ArrowRight size={18} className="text-zinc-400 dark:text-zinc-500" />
            </div>
          </div>

          <p className="text-[11px] font-semibold uppercase tracking-[0.15em] text-zinc-400 dark:text-zinc-500 mb-2">
            {subtitle}</p>
          <h3 className="font-serif text-2xl md:text-3xl text-zinc-900 dark:text-white leading-tight font-semibold tracking-tight">
            {title}
          </h3>
          {description && (
            <p className="mt-3 text-[12px] leading-relaxed text-zinc-500 dark:text-zinc-400">{description}</p>
          )}
        </div>

        {!hideProgress && (
          <div className="mt-8 flex items-center justify-between gap-6 pt-6 border-t border-zinc-100 dark:border-zinc-800">
              <div className="flex flex-col">
                <span className="text-[10px] font-semibold uppercase tracking-widest text-zinc-400 dark:text-zinc-500">Progress</span>
              </div>
              <ActivityRing progress={progress} color={accentHex} />
          </div>
        )}
      </div>
    </MotionDiv>
  );
};

export const KnowledgeTree: React.FC<KnowledgeTreeProps> = ({ onSelectCategory, onGoToInnovationZone, onGoToDashboard, onGoToLearningPaths, onGoToJourney, onGoToStudy, _onGoToInsights, onGoToTrainingHub, allCourses, onSelectModule, categoryTitles, userProgress, userName, userAvatarSeed, onLogout, onOpenSettings, onOpenPassport, onChangeSubjects, settings, updateSetting, _unlockedThemes = [], completedCount, totalCount, streak, pointsBalance, northStar, studentProfile, timetableCompletions, smartRecommendation, questState, onClaimQuestReward, onRecommendationAction, onDevRankUp }) => {
  const [selectedTags, setSelectedTags] = useState<string[]>([]);
  const [tagFilterOpen, setTagFilterOpen] = useState(false);
  const [sidebarOpen, setSidebarOpen] = useState(false);

  const sidebarItems = [
    { icon: Home, label: 'Home', onClick: () => {}, active: true },
    { icon: Dumbbell, label: 'Training Hub', onClick: onGoToTrainingHub ?? (() => {}), active: false },
    { icon: Mountain, label: 'My Journey', onClick: onGoToJourney, active: false },
    { icon: Timer, label: 'Study Session', onClick: onGoToStudy ?? (() => {}), active: false },
    { icon: BarChart3, label: 'Dashboard', onClick: onGoToDashboard, active: false },
    { icon: Compass, label: 'Learning Paths', onClick: onGoToLearningPaths, active: false },
    { icon: Rocket, label: 'Innovation Zone', onClick: onGoToInnovationZone, active: false },
  ];
  
  const getCategoryProgress = (category: CategoryType) => {
    const categoryCourses = allCourses.filter(c => c.category === category);
    if (categoryCourses.length === 0) return 0;

    const totalCourses = categoryCourses.length;
    const completedCourses = categoryCourses.reduce((count, course) => {
      const progress = userProgress[course.id];
      const isComplete = progress && progress.unlockedSection >= course.sectionsCount;
      return count + (isComplete ? 1 : 0);
    }, 0);

    return (completedCourses / totalCourses) * 100;
  };

  const modules = [
    {
      id: 'architecture-mindset',
      title: "The Architecture of your Mindset",
      subtitle: "Module 01",
      description: "Build the psychological foundations for academic success. This module covers identity, beliefs, emotional regulation, and the resilience you need to thrive under pressure.",
      icon: Fingerprint,
      hex: "#3b82f6",
      className: "md:col-span-4"
    },
    {
      id: 'science-growth',
      title: "The Science of Growth",
      subtitle: "Module 02",
      description: "Understand how your brain physically changes through effort. The neuroscience of learning, neuroplasticity, and why struggle is the engine of growth.",
      icon: Sprout,
      hex: "#f59e0b",
      className: "md:col-span-2"
    },
    {
      id: 'learning-cheat-codes',
      title: "The Science of Learning Effectively",
      subtitle: "Module 03",
      description: "The practical techniques and study methods that separate high performers from everyone else. Active recall, spaced repetition, interleaving, and more.",
      icon: Lightbulb,
      hex: "#14b8a6",
      className: "md:col-span-2"
    },
     {
      id: 'subject-specific-science',
      title: "Decoding the Subjects",
      subtitle: "Module 04",
      description: "Subject-by-subject deconstruction of the Leaving Cert exams. The marking schemes, the hidden curriculum, and the strategies that unlock top grades in each subject.",
      icon: KeyRound,
      hex: "#6b7280",
      className: "md:col-span-2"
    },
    {
      id: 'exam-zone',
      title: "Exam Strategy and Points Maximisation",
      subtitle: "Module 05",
      description: "Cross-subject exam tactics, scheduling, crisis management, and the performance psychology you need to execute on the day.",
      icon: Target,
      hex: "#ef4444",
      className: "md:col-span-2"
    },
  ];

  const allTags = [...new Set(allCourses.flatMap(course => course.tags))].sort();

  const handleTagClick = (tag: string) => {
    const isSelected = selectedTags.includes(tag);
    if (isSelected) {
      const next = selectedTags.filter(t => t !== tag);
      setSelectedTags(next);
      if (next.length === 0) setTagFilterOpen(false);
    } else {
      if (selectedTags.length < 2) {
        setSelectedTags([...selectedTags, tag]);
      } else {
        setSelectedTags([selectedTags[1], tag]);
      }
      setTagFilterOpen(false);
    }
  };

  const filteredCourses = selectedTags.length > 0
    ? allCourses.filter(course => selectedTags.every(tag => course.tags.includes(tag as string)))
    : [];

  // ── Dashboard computed values ──────────────────────────────────────────
  const [todayBlocks, setTodayBlocks] = useState<any[]>([]);
  useEffect(() => {
    if (!studentProfile || studentProfile.subjects.length === 0) { setTodayBlocks([]); return; }
    import('./timetableAlgorithm').then(({ computeSubjectPriorities, allocateSessions, generateWeeklyTimetable, computeWeeksUntilExam }) => {
      try {
        const today = new Date();
        const jsDay = today.getDay();
        const todayDayIndex = jsDay === 0 ? 6 : jsDay - 1;
        const priorities = computeSubjectPriorities(studentProfile.subjects as any);
        const weeksUntilExam = computeWeeksUntilExam(studentProfile.examStartDate);
        const allocations = allocateSessions(priorities, weeksUntilExam);
        const restDays = studentProfile.restDays || [];
        const blockDuration = studentProfile.defaultBlockDuration ?? 45;
        const timetable = generateWeeklyTimetable(allocations, weeksUntilExam, 0, restDays, blockDuration);
        setTodayBlocks(timetable[todayDayIndex]?.blocks ?? []);
      } catch {
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
    <div className="min-h-screen bg-zinc-50 dark:bg-zinc-950 overflow-x-hidden relative transition-colors duration-500 selection:bg-[rgba(var(--accent),0.2)]">
      {/* Sidebar — desktop only */}
      <aside
        className={`hidden md:flex flex-col fixed top-0 left-0 h-full z-40 bg-white/80 dark:bg-zinc-900/80 backdrop-blur-sm border-r border-zinc-200 dark:border-zinc-800 overflow-hidden transition-all duration-300 ease-[cubic-bezier(0.16,1,0.3,1)] ${sidebarOpen ? 'w-56' : 'w-[60px]'}`}
      >
        {/* Avatar row — click to toggle */}
        <button
          onClick={() => setSidebarOpen(!sidebarOpen)}
          className="flex items-center gap-3 px-3 py-4 w-full hover:bg-zinc-100 dark:hover:bg-zinc-800 transition-colors"
        >
          <div className="w-9 h-9 rounded-lg overflow-hidden shrink-0 bg-zinc-200 dark:bg-zinc-700 flex items-center justify-center">
            {userAvatarSeed ? (
              <img src={getAvatarUrl(userAvatarSeed)} alt="Avatar" className="w-full h-full object-cover" />
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
              className={`flex items-center gap-3 px-2.5 py-2 rounded-lg transition-colors ${item.active ? 'bg-zinc-100 dark:bg-zinc-800' : 'hover:bg-zinc-100 dark:hover:bg-zinc-800'}`}
            >
              <div className="shrink-0 flex items-center justify-center w-[18px]">
                <item.icon size={18} strokeWidth={1.5} className="text-zinc-600 dark:text-zinc-400" />
              </div>
              <span className={`text-sm font-medium text-zinc-700 dark:text-zinc-300 whitespace-nowrap overflow-hidden transition-opacity duration-300 ${sidebarOpen ? 'opacity-100' : 'opacity-0'}`}>
                {item.label}
              </span>
            </button>
          ))}
        </nav>

        {/* User actions */}
        <div className="border-t border-zinc-200 dark:border-zinc-800 mx-2 pt-2 flex flex-col gap-1">
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
                <RefreshCw size={18} strokeWidth={1.5} className="text-teal-500" />
              </div>
              <span className={`text-sm font-medium text-zinc-700 dark:text-zinc-300 whitespace-nowrap overflow-hidden transition-opacity duration-300 flex-1 text-left ${sidebarOpen ? 'opacity-100' : 'opacity-0'}`}>
                Change Subjects
              </span>
            </button>
          )}

          {/* Dark / Light mode toggle */}
          <button
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
              {settings.darkMode ? 'Light Mode' : 'Dark Mode'}
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
          className="mb-6"
        >
          <p className="text-[12px] font-semibold uppercase tracking-[0.2em] mb-3" style={{ color: '#2A7D6F' }}>
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
        </MotionDiv>

        {/* Student Home Dashboard */}
        {studentProfile && settings.showDashboard !== false && (
          <MotionDiv
            initial={{ opacity: 0, y: 8 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.4, delay: 0.1, ease: [0.16, 1, 0.3, 1] }}
            className="mb-6"
          >
            {/* ── Warm colour banner — day's key stats ── */}
            <div
              className="rounded-2xl px-5 py-4 mb-4 flex items-center justify-between flex-wrap gap-3"
              style={{ backgroundColor: '#2A7D6F', boxShadow: '0 4px 16px rgba(42,125,111,0.15)' }}
            >
              <div className="flex items-center gap-4">
                <span className="text-sm font-medium text-white">
                  {todayBlocks.length > 0
                    ? `${todayBlocks.length} session${todayBlocks.length !== 1 ? 's' : ''} today`
                    : 'No sessions today'}
                </span>
                <span className="w-1 h-1 rounded-full" style={{ backgroundColor: 'rgba(255,255,255,0.3)' }} />
                <span className="text-sm text-white" style={{ opacity: 0.7 }}>{pointsBalance ?? 0} pts</span>
                {streak && streak.currentStreak > 0 && (
                  <>
                    <span className="w-1 h-1 rounded-full" style={{ backgroundColor: 'rgba(255,255,255,0.3)' }} />
                    <span className="text-sm font-medium text-white">{streak.currentStreak}-day streak</span>
                  </>
                )}
              </div>
              {onGoToStudy && todayBlocks.length > 0 && !todayBlocks.every((_b, i) => todayCompletions.includes(`block-${i}`)) && (
                <button
                  onClick={onGoToStudy}
                  className="flex items-center gap-1 text-xs font-bold px-4 py-2 rounded-lg transition-all hover:opacity-90"
                  style={{ backgroundColor: 'rgba(255,255,255,0.2)', color: '#fff' }}
                >
                  Study Now <ArrowRight size={12} />
                </button>
              )}
            </div>

            {/* ── White Mercury cards ── */}
            <div className="grid grid-cols-1 md:grid-cols-2 gap-3">
              {/* TODAY */}
              <div className="px-4 py-3 bg-[#FAF7F4] dark:bg-zinc-900 border border-[#EDEBE8] dark:border-zinc-800" style={{ borderRadius: 14, boxShadow: '0 1px 3px rgba(28,25,23,0.04)' }}>
                <p className="text-[10px] font-bold uppercase tracking-widest mb-2 text-[#A8A29E] dark:text-zinc-500">Today</p>
                {todayBlocks.length === 0 ? (
                  <p className="text-xs text-[#A8A29E] dark:text-zinc-500">No blocks scheduled</p>
                ) : todayBlocks.every((_b, i) => todayCompletions.includes(`block-${i}`)) ? (
                  <p className="text-xs font-bold" style={{ color: '#276749' }}>All done for today</p>
                ) : (
                  <div className="flex flex-col gap-1.5">
                    {todayBlocks.slice(0, 3).map((block, i) => (
                      <div key={i} className="flex items-center gap-2 text-xs">
                        <span className="w-3 h-3 rounded-full shrink-0" style={{ backgroundColor: getSubjectHex(block.subjectName) }} />
                        <span className="font-semibold truncate text-[#1A1A1A] dark:text-white">{block.subjectName}</span>
                        <span className="text-[10px] px-1.5 py-0.5 rounded bg-[#EDEBE8] dark:bg-zinc-700 text-[#78716C] dark:text-zinc-400">{sessionTypeLabel(block.sessionType)}</span>
                        <span className="text-[10px] text-[#A8A29E] dark:text-zinc-500">{block.durationMinutes}m</span>
                      </div>
                    ))}
                    {todayBlocks.length > 3 && (
                      <p className="text-[10px] text-[#A8A29E] dark:text-zinc-500">+{todayBlocks.length - 3} more</p>
                    )}
                  </div>
                )}
              </div>

              {/* PROGRESS */}
              <div className="px-4 py-3 bg-[#FAF7F4] dark:bg-zinc-900 border border-[#EDEBE8] dark:border-zinc-800" style={{ borderRadius: 14, boxShadow: '0 1px 3px rgba(28,25,23,0.04)' }}>
                <p className="text-[10px] font-bold uppercase tracking-widest mb-1 text-[#A8A29E] dark:text-zinc-500">Progress</p>
                <p className="text-2xl font-apercu font-black text-[#1A1A1A] dark:text-white">{pointsBalance ?? 0} pts</p>
                <div className="flex items-center gap-3 text-xs mt-1 mb-2">
                  {streak && streak.currentStreak > 0 ? (
                    <span className="font-bold" style={{ color: '#2A7D6F' }}>{streak.currentStreak}-day streak</span>
                  ) : (
                    <span className="text-[#A8A29E] dark:text-zinc-500">Start your streak today</span>
                  )}
                  <span className="text-[#EDEBE8] dark:text-zinc-700">·</span>
                  <span className="font-medium text-[#78716C] dark:text-zinc-400">{completedCount}/{totalCount} modules</span>
                </div>
                <div className="h-1.5 rounded-full overflow-hidden bg-[#EDEBE8] dark:bg-zinc-700">
                  <div className="h-full rounded-full" style={{ backgroundColor: '#2A7D6F', width: `${totalCount > 0 ? (completedCount / totalCount) * 100 : 0}%`, transition: 'width 0.5s ease' }} />
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

                return (
                  <div className="md:col-span-2">
                    <div className="flex items-center bg-[#FAF7F4] dark:bg-zinc-900 rounded-xl px-5 py-4 border border-[#EDEBE8] dark:border-zinc-800" style={{ borderRadius: 14, boxShadow: '0 1px 3px rgba(28,25,23,0.04)' }}>
                      {/* Left: streak count */}
                      <div className="flex flex-col items-center justify-center pr-5" style={{ minWidth: 88 }}>
                        <p className="font-apercu font-semibold tabular-nums" style={{ fontSize: 22, color: '#2A7D6F' }}>{streakCount}</p>
                        <p className="text-xs text-zinc-400 dark:text-zinc-500">current streak</p>
                      </div>

                      {/* Divider */}
                      <div className="w-px self-stretch bg-zinc-200 dark:bg-zinc-800" />

                      {/* Right: 7 mini bar charts */}
                      <div className="flex-1 flex justify-between pl-5" style={{ gap: 4 }}>
                        {DAY_LABELS.map((day, i) => {
                          const pts = weekPoints[i];
                          const isToday = i === currentDayIdx;
                          const isFuture = i > currentDayIdx;
                          const fillPct = pts === 0 ? 0 : pts === 1 ? 25 : pts === 2 ? 50 : pts === 3 ? 75 : 100;

                          return (
                            <div key={i} className="flex flex-col items-center flex-1">
                              {/* Bar container */}
                              <div
                                className={`w-full relative overflow-hidden rounded-md ${
                                  isToday
                                    ? 'border-[1.5px] border-[#2A7D6F]'
                                    : ''
                                }`}
                                style={{
                                  height: 32,
                                  backgroundColor: isFuture ? 'rgba(0,0,0,0.03)' : 'rgba(0,0,0,0.04)',
                                  ...(isToday ? { animation: 'streak-pulse 2.5s ease-in-out infinite' } : {}),
                                }}
                              >
                                {/* Fill bar */}
                                {fillPct > 0 && (
                                  <div
                                    className="absolute bottom-0 left-0 right-0 rounded-md"
                                    style={{
                                      height: `${fillPct}%`,
                                      backgroundColor: isToday ? 'rgba(42,125,111,0.7)' : '#2A7D6F',
                                    }}
                                  />
                                )}
                              </div>
                              {/* Day label */}
                              <span
                                className={`text-[11px] mt-1.5 ${
                                  isToday
                                    ? 'font-semibold'
                                    : isFuture
                                      ? 'text-zinc-300 dark:text-zinc-700'
                                      : 'text-zinc-500 dark:text-zinc-500'
                                }`}
                                style={isToday ? { color: '#2A7D6F' } : undefined}
                              >
                                {day}
                              </span>
                            </div>
                          );
                        })}
                      </div>
                    </div>
                  </div>
                );
              })()}

              {/* RECOMMENDED */}
              {smartRecommendation && (
                <button
                  onClick={() => onRecommendationAction?.(smartRecommendation.category)}
                  className="px-4 py-3 text-left hover:shadow-md transition-all bg-[#FAF7F4] dark:bg-zinc-900 border border-[#EDEBE8] dark:border-zinc-800"
                  style={{ borderRadius: 14, boxShadow: '0 1px 3px rgba(28,25,23,0.04)' }}
                >
                  <p className="text-[10px] font-bold uppercase tracking-widest mb-1 text-[#A8A29E] dark:text-zinc-500">Recommended</p>
                  <p className="text-xs font-semibold text-[#1A1A1A] dark:text-white">{smartRecommendation.title}</p>
                  <p className="text-[11px] mt-0.5 text-[#A8A29E] dark:text-zinc-500">{smartRecommendation.description}</p>
                </button>
              )}

              {/* QUEST */}
              {questState && (
                <div className="px-4 py-3 bg-[#FAF7F4] dark:bg-zinc-900 border border-[#EDEBE8] dark:border-zinc-800" style={{ borderRadius: 14, boxShadow: '0 1px 3px rgba(28,25,23,0.04)' }}>
                  <div className="flex items-center justify-between mb-1">
                    <p className="text-[10px] font-bold uppercase tracking-widest text-[#A8A29E] dark:text-zinc-500">
                      {questState.isOnboarding ? `Day ${questState.dayNumber} Quest` : 'Daily Quest'}
                    </p>
                    <span className="text-[10px] font-bold" style={{ color: '#2A7D6F' }}>{questState.quest.rewardPoints} pts</span>
                  </div>
                  <p className="text-xs font-semibold text-[#1A1A1A] dark:text-white">{questState.quest.title}</p>
                  <p className="text-[11px] mt-0.5 text-[#A8A29E] dark:text-zinc-500">{questState.quest.description}</p>
                  <div className="mt-2 flex items-center gap-2">
                    <div className="flex-1 h-1.5 rounded-full overflow-hidden bg-[#EDEBE8] dark:bg-zinc-700">
                      <div className="h-full rounded-full transition-all duration-500" style={{ width: `${Math.min(100, (questState.current / questState.quest.target) * 100)}%`, backgroundColor: '#2A7D6F' }} />
                    </div>
                    <span className="text-[10px] font-bold tabular-nums text-[#A8A29E] dark:text-zinc-500">{questState.current}/{questState.quest.target}</span>
                  </div>
                  {questState.isCompleted && !questState.isClaimed && onClaimQuestReward && (
                    <button onClick={onClaimQuestReward} className="mt-2 w-full py-1.5 rounded-lg text-xs font-bold text-white" style={{ backgroundColor: '#2A7D6F' }}>
                      Claim {questState.quest.rewardPoints} pts
                    </button>
                  )}
                  {questState.isClaimed && (
                    <p className="mt-2 text-[10px] font-bold" style={{ color: '#2A7D6F' }}>Claimed</p>
                  )}
                </div>
              )}
            </div>
          </MotionDiv>
        )}

        {/* Inline tag filter */}
        <div className="mb-6">
          {selectedTags.length === 0 ? (
            <button
              onClick={() => setTagFilterOpen(!tagFilterOpen)}
              className="flex items-center gap-2 px-3.5 py-2 rounded-xl border border-zinc-200 dark:border-zinc-800 bg-white dark:bg-zinc-900 hover:border-zinc-300 dark:hover:border-zinc-700 transition-colors"
            >
              <Tag size={14} className="text-zinc-400" />
              <span className="text-xs font-medium text-zinc-500 dark:text-zinc-400">Filter by topic</span>
            </button>
          ) : (
            <div className="flex items-center gap-2 flex-wrap">
              <Tag size={14} className="text-zinc-400 shrink-0" />
              {selectedTags.map(tag => (
                <button
                  key={tag}
                  onClick={() => handleTagClick(tag)}
                  className="flex items-center gap-1.5 px-3 py-1.5 rounded-full text-xs font-medium bg-[var(--accent-hex)] text-white"
                >
                  {tag}
                  <X size={12} />
                </button>
              ))}
              <button
                onClick={() => { setSelectedTags([]); setTagFilterOpen(false); }}
                className="text-[10px] font-medium text-zinc-400 hover:text-zinc-600 dark:hover:text-zinc-300 ml-1"
              >
                Clear
              </button>
            </div>
          )}
          <AnimatePresence>
            {tagFilterOpen && selectedTags.length === 0 && (
              <MotionDiv
                initial={{ opacity: 0, height: 0 }}
                animate={{ opacity: 1, height: 'auto' }}
                exit={{ opacity: 0, height: 0 }}
                transition={{ duration: 0.2, ease: [0.16, 1, 0.3, 1] }}
                className="overflow-hidden"
              >
                <div className="flex flex-wrap gap-2 mt-3">
                  {allTags.map(tag => (
                    <button
                      key={tag}
                      onClick={() => handleTagClick(tag)}
                      className="px-3 py-1.5 text-xs font-medium rounded-full border border-zinc-200 dark:border-zinc-800 bg-white dark:bg-zinc-900 text-zinc-600 dark:text-zinc-400 hover:border-[var(--accent-hex)] hover:text-[var(--accent-hex)] transition-colors"
                    >
                      {tag}
                    </button>
                  ))}
                </div>
              </MotionDiv>
            )}
          </AnimatePresence>
        </div>

        {/* Filtered results or category grid */}
        <AnimatePresence mode="wait">
        {selectedTags.length > 0 ? (
          <MotionDiv
            key="filtered"
            initial={{ opacity: 0, y: 8 }}
            animate={{ opacity: 1, y: 0 }}
            exit={{ opacity: 0, y: -8 }}
            transition={{ duration: 0.25 }}
          >
            {filteredCourses.length > 0 ? (
              <div className="grid grid-cols-1 md:grid-cols-3 lg:grid-cols-6 gap-6">
                {filteredCourses.map((course, index) => {
                  const progress = userProgress[course.id];
                  const isCompleted = progress && progress.unlockedSection >= course.sectionsCount;
                  return (
                    <BentoModuleTile
                      key={course.id}
                      course={course}
                      index={index}
                      isUnlocked={true}
                      isCompleted={isCompleted}
                      onClick={() => onSelectModule(course.id)}
                      categoryTitle={categoryTitles[course.category]}
                    />
                  );
                })}
              </div>
            ) : (
              <div className="text-center py-16">
                <p className="text-sm text-zinc-400 dark:text-zinc-500">No modules match the selected tags.</p>
              </div>
            )}
          </MotionDiv>
        ) : (
          <MotionDiv
            key="grid"
            initial={{ opacity: 0, y: 8 }}
            animate={{ opacity: 1, y: 0 }}
            exit={{ opacity: 0, y: -8 }}
            transition={{ duration: 0.25 }}
          >
        <div className="grid grid-cols-1 md:grid-cols-6 gap-6">
          {modules.map((mod, i) => (
            <BentoTile
              key={mod.id}
              title={mod.title}
              subtitle={mod.subtitle}
              description={mod.description}
              icon={mod.icon}
              accentHex={mod.hex}
              onClick={() => onSelectCategory(mod.id as CategoryType)}
              progress={getCategoryProgress(mod.id as CategoryType)}
              className={mod.className}
              delay={i * 0.1}
            />
          ))}
           <BentoTile
              title="The Innovation Zone"
              subtitle="Explore"
              description="Your personal AI-powered study companion. Use the Journey Simulator to stress-test your study habits, get personalised feedback, and discover which units will have the biggest impact on your performance."
              icon={Rocket}
              accentHex="#8b5cf6"
              onClick={onGoToInnovationZone}
              className="md:col-span-6"
              delay={modules.length * 0.1}
              hideProgress
            />
           <BentoTile
              title="My Progress"
              subtitle="Dashboard"
              description="Track your modules completed, study streak, and category progress all in one place."
              icon={BarChart3}
              accentHex="var(--accent-hex)"
              onClick={onGoToDashboard}
              className="md:col-span-3"
              delay={(modules.length + 1) * 0.1}
              hideProgress
            />
           <BentoTile
              title="Learning Paths"
              subtitle="Guided"
              description="Follow curated sequences of modules designed to take you from foundation to mastery."
              icon={Compass}
              accentHex="#10b981"
              onClick={onGoToLearningPaths}
              className="md:col-span-3"
              delay={(modules.length + 2) * 0.1}
              hideProgress
            />
        </div>
          </MotionDiv>
        )}
        </AnimatePresence>

      {/* DEV: Rank Up Tester */}
      {onDevRankUp && (
        <div className="flex flex-wrap justify-center gap-2 mt-8 mb-4">
          {ATHLETE_RANKS.map(rank => (
            <button
              key={rank.id}
              onClick={() => onDevRankUp(rank)}
              className="px-3 py-1 rounded-full text-[9px] font-mono border transition-colors hover:opacity-80"
              style={{ color: rank.colorHex, borderColor: rank.colorHex, backgroundColor: `${rank.colorHex}10` }}
            >
              {rank.title}
            </button>
          ))}
        </div>
      )}

      </div>
      </div>
    </div>
  );
};
