/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
*/

import React, { useState } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import {
  Sprout, Rocket, Target, FlaskConical,
  Fingerprint, ArrowRight, Sparkles, BarChart3, Compass, Lightbulb, KeyRound,
  User, Home, PanelLeft, Award, Settings, LogOut, Sun, Moon, RefreshCw, Mountain, Timer, Tag, X
} from 'lucide-react';
import { getAvatarUrl } from '../components/Auth';
import { CourseData, BentoModuleTile } from './Library';
import { UserSettings } from '../types';
import { MoodFaceIcon, MOOD_KEYS, MOOD_LABELS } from './MoodFaceIcon';

// FIX: Cast motion components to any to bypass broken type definitions
const MotionDiv = motion.div as any;
const MotionCircle = motion.circle as any;

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
  todayMood: string | null;
  onSetMood: (mood: string) => void;
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

export const KnowledgeTree: React.FC<KnowledgeTreeProps> = ({ onSelectCategory, onGoToInnovationZone, onGoToDashboard, onGoToLearningPaths, onGoToJourney, onGoToStudy, onGoToInsights, allCourses, onSelectModule, categoryTitles, userProgress, userName, userAvatarSeed, onLogout, onOpenSettings, onOpenPassport, onChangeSubjects, settings, updateSetting, unlockedThemes = [], completedCount, totalCount, todayMood, onSetMood }) => {
  const [selectedTags, setSelectedTags] = useState<string[]>([]);
  const [tagFilterOpen, setTagFilterOpen] = useState(false);
  const [sidebarOpen, setSidebarOpen] = useState(false);
  const [moodExpanded, setMoodExpanded] = useState(false);

  const sidebarItems = [
    { icon: Home, label: 'Home', onClick: () => {}, active: true },
    { icon: Mountain, label: 'My Journey', onClick: onGoToJourney, active: false },
    { icon: Timer, label: 'Study Session', onClick: onGoToStudy ?? (() => {}), active: false },
    { icon: BarChart3, label: 'Dashboard', onClick: onGoToDashboard, active: false },
    { icon: Lightbulb, label: 'Insights', onClick: onGoToInsights ?? (() => {}), active: false },
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

        {/* Mood check-in */}
        <div className="px-2 mt-1 mb-1">
          <button
            onClick={() => setMoodExpanded(!moodExpanded)}
            className={`relative flex items-center gap-3 px-2.5 py-2 rounded-lg transition-colors w-full ${moodExpanded ? 'bg-zinc-100 dark:bg-zinc-800' : 'hover:bg-zinc-100 dark:hover:bg-zinc-800'}`}
          >
            <div className="shrink-0 flex items-center justify-center w-[18px] relative">
              <MoodFaceIcon mood={todayMood || 'balanced'} size={18} className="text-zinc-600 dark:text-zinc-400" />
              {todayMood && (
                <div className="absolute -top-0.5 -right-0.5 w-2 h-2 rounded-full bg-[var(--accent-hex)]" />
              )}
            </div>
            <span className={`text-sm font-medium text-zinc-700 dark:text-zinc-300 whitespace-nowrap overflow-hidden transition-opacity duration-300 ${sidebarOpen ? 'opacity-100' : 'opacity-0'}`}>
              Mood
            </span>
          </button>

          <AnimatePresence>
            {moodExpanded && (
              <motion.div
                initial={{ height: 0, opacity: 0 }}
                animate={{ height: 'auto', opacity: 1 }}
                exit={{ height: 0, opacity: 0 }}
                transition={{ duration: 0.2, ease: [0.16, 1, 0.3, 1] }}
                className="overflow-hidden"
              >
                <div className={`py-2 ${sidebarOpen ? 'grid grid-cols-4 gap-1 px-1' : 'flex flex-col items-center gap-2'}`}>
                  {MOOD_KEYS.map((key) => (
                    <button
                      key={key}
                      onClick={() => {
                        onSetMood(key);
                        setTimeout(() => setMoodExpanded(false), 400);
                      }}
                      title={MOOD_LABELS[key]}
                      className={`flex flex-col items-center gap-1.5 rounded-lg py-1.5 transition-all ${
                        todayMood === key
                          ? 'text-[var(--accent-hex)]'
                          : 'text-zinc-400 dark:text-zinc-500 hover:bg-zinc-100 dark:hover:bg-zinc-800'
                      }`}
                    >
                      <div className={`w-8 h-8 rounded-full flex items-center justify-center transition-all ${
                        todayMood === key
                          ? 'bg-[rgba(var(--accent),0.1)] ring-2 ring-[var(--accent-hex)]'
                          : ''
                      }`}>
                        <MoodFaceIcon mood={key} size={18} />
                      </div>
                      {sidebarOpen && (
                        <span className="text-[9px] font-medium leading-none">
                          {MOOD_LABELS[key]}
                        </span>
                      )}
                    </button>
                  ))}
                </div>
              </motion.div>
            )}
          </AnimatePresence>
        </div>

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
        <MotionDiv
          initial={{ opacity: 0, y: 12 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.5, ease: [0.16, 1, 0.3, 1] }}
          className="mb-6"
        >
          <p className="text-[11px] font-semibold uppercase tracking-[0.2em] text-[var(--accent-hex)] mb-3">
            Learning Lab
          </p>
          <h1 className="font-serif text-4xl md:text-5xl text-zinc-900 dark:text-white tracking-tight leading-tight font-semibold">
            {(() => { const h = new Date().getHours(); const firstName = userName?.split(' ')[0] || ''; const name = firstName ? ', ' + firstName : ''; return h < 12 ? `Good morning${name}.` : h < 18 ? `Good afternoon${name}.` : `Good evening${name}.`; })()}
          </h1>
          <p className="mt-2 text-zinc-400 dark:text-zinc-500 text-sm">
            {(() => {
              const completed = allCourses.filter(c => { const p = userProgress[c.id]; return p && p.unlockedSection >= c.sectionsCount; }).length;
              const inProgress = allCourses.filter(c => { const p = userProgress[c.id]; return p && p.unlockedSection > 0 && p.unlockedSection < c.sectionsCount; }).length;
              if (completed === allCourses.length) return 'You\'ve completed the full curriculum. Remarkable.';
              if (completed > 0) return `You've completed ${completed} of ${allCourses.length} modules.`;
              if (inProgress > 0) return `You have ${inProgress} module${inProgress !== 1 ? 's' : ''} in progress.`;
              return 'Pick a module to start your journey.';
            })()}
          </p>
        </MotionDiv>

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
              description="Track your modules completed, study streak, mood, and category progress all in one place."
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

      </div>
      </div>
    </div>
  );
};
