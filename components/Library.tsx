

/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
*/

import React, { useState } from 'react';
import { AnimatePresence } from 'framer-motion';
import { MotionDiv } from './Motion';
import {
  ArrowLeft, CheckCircle2,
  ChevronRight, Lock, BookOpen,
  Zap, Brain, Target, Shield, Compass, Star,
  Sun, Moon, Home, BarChart3, Rocket, PanelLeft, Award, Settings, LogOut, Layers, RefreshCw, User, Mountain
} from 'lucide-react';
import { CategoryType } from './KnowledgeTree';
import { NorthStar, AccentThemeId, CardStyleId } from '../types';
import { type StudentSubjectProfile } from './subjectData';
import { useSettingsContext } from '../contexts/SettingsContext';
import { ACCENT_THEME_LIST, ACCENT_THEMES, CARD_STYLES } from '../themeData';
import { getAvatarUrl } from './Auth';
import ModuleShowcase from './ModuleShowcase';

// FIX: Cast motion components to any to bypass broken type definitions

export interface CourseData {
  id: string;
  category: CategoryType;
  title: string;
  subtitle: string;
  description: string;
  sectionsCount: number;
  tags: readonly string[];
  gradient: string;
  accentColor: string;
  auraColor?: string;
  pillBgColor: string;
}

type UserProgress = {
  [moduleId: string]: { unlockedSection: number };
};

interface LibraryProps {
  title: string;
  courses: CourseData[];
  onSelectCourse: (courseId: string) => void;
  onBack: () => void;
  userProgress: UserProgress;
  northStar?: NorthStar | null;
  studentProfile?: StudentSubjectProfile | null;
  // Sidebar props
  userName?: string;
  userAvatarSeed?: string;
  onLogout?: () => void;
  onOpenSettings?: () => void;
  onOpenPassport?: () => void;
  onGoToDashboard?: () => void;
  onGoToLearningPaths?: () => void;
  onGoToInnovationZone?: () => void;
  onGoToJourney?: () => void;
  onChangeSubjects?: () => void;
  completedCount?: number;
  totalCount?: number;
}

export interface BentoModuleTileProps {
  course: CourseData;
  index: number;
  isUnlocked: boolean;
  isCompleted: boolean;
  onClick: () => void;
  categoryTitle: string;
}

export const BentoModuleTile: React.FC<BentoModuleTileProps> = ({
  course,
  index,
  isUnlocked,
  isCompleted,
  onClick,
  categoryTitle
}) => {
  const icons = [BookOpen, Zap, Brain, Target, Shield, Compass, Star];
  const Icon = icons[index % icons.length];

  const getSpanClass = (idx: number) => {
    if (idx === 0) return "md:col-span-3 lg:col-span-4 lg:row-span-2 min-h-[400px]";
    if (idx === 1) return "md:col-span-3 lg:col-span-2 lg:row-span-1";
    if (idx === 2) return "md:col-span-3 lg:col-span-2 lg:row-span-1";
    if (idx % 5 === 0) return "md:col-span-6 lg:col-span-4";
    return "md:col-span-3 lg:col-span-2";
  };

  const pillBgColor = course.pillBgColor;

  return (
    <MotionDiv
      initial={{ opacity: 0, scale: 0.9, y: 20 }}
      whileInView={{ opacity: 1, scale: 1, y: 0 }}
      viewport={{ once: true }}
      transition={{ duration: 0.6, delay: index * 0.05, ease: [0.16, 1, 0.3, 1] }}
      whileHover={isUnlocked ? { scale: 1.01 } : {}}
      className={`group relative overflow-hidden rounded-2xl transition-all duration-300 ${getSpanClass(index)}
        ${isUnlocked ? 'cursor-pointer hover:shadow-md focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-[rgba(var(--accent),0.5)] focus-visible:ring-offset-2' : 'cursor-not-allowed'}
      `}
      onClick={isUnlocked ? onClick : undefined}
    >
      {/* Category Pill */}
      <div className={`absolute top-6 left-6 z-20 px-3 py-1.5 rounded-full ${pillBgColor} border border-black/10 dark:border-white/10`}>
        <p className={`text-[9px] font-semibold uppercase tracking-wider text-white`}>{categoryTitle}</p>
      </div>

      {/* Clean Surface */}
      <div className="h-full w-full card-styled bg-white dark:bg-zinc-900 border border-zinc-200 dark:border-zinc-800 p-8 pt-16 flex flex-col justify-between relative z-10 overflow-hidden">
        <div>
          <div className="flex items-center justify-between mb-8">
            <MotionDiv
              className={`w-14 h-14 rounded-2xl flex items-center justify-center transition-all duration-500 shadow-sm
                ${isCompleted ? 'bg-emerald-500 text-white' : isUnlocked ? 'bg-zinc-900 dark:bg-white text-white dark:text-zinc-900' : 'bg-zinc-200 dark:bg-zinc-800 text-zinc-400'}`}
              whileHover={isUnlocked ? { x: 5, y: -2 } : {}}
            >
              {isCompleted ? <CheckCircle2 size={28} /> : !isUnlocked ? <Lock size={24} /> : <Icon size={28} strokeWidth={1.5} />}
            </MotionDiv>

            <div className="flex flex-col items-end">
              <span className="font-mono text-[9px] font-semibold uppercase tracking-wider text-zinc-400 dark:text-zinc-500">Unit {index + 1}</span>
              {isCompleted && <span className="text-[8px] font-bold text-emerald-500 uppercase tracking-widest mt-1">Complete</span>}
            </div>
          </div>

          <h3 className="font-serif text-2xl md:text-3xl text-zinc-900 dark:text-white mb-4 leading-tight font-semibold tracking-tight">
            {course.title}
          </h3>

          <p className="text-zinc-500 dark:text-zinc-400 text-sm leading-relaxed font-medium line-clamp-3 mb-8">
            {course.description}
          </p>
        </div>

        <div className="flex items-center justify-between mt-auto pt-6 border-t border-zinc-200/30 dark:border-white/5">
          <div className="flex gap-2">
            {course.tags.slice(0, 2).map(tag => (
              <span key={tag} className="px-2.5 py-1 rounded-full bg-zinc-100 dark:bg-white/5 text-zinc-400 dark:text-zinc-500 text-[9px] font-bold uppercase tracking-wider">
                {tag}
              </span>
            ))}
          </div>
          {isUnlocked && (
            <MotionDiv
              className="text-zinc-900 dark:text-white"
              whileHover={{ x: 5 }}
            >
              <ChevronRight size={20} />
            </MotionDiv>
          )}
        </div>

        {!isUnlocked && (
          <div className="absolute inset-0 bg-zinc-50/80 dark:bg-zinc-950/80 flex items-center justify-center z-20">
            <div className="bg-white dark:bg-zinc-900 px-4 py-2 rounded-lg border border-zinc-200 dark:border-zinc-800 flex items-center gap-2">
               <Lock size={12} className="text-zinc-400" />
               <span className="text-[10px] font-semibold uppercase tracking-wider text-zinc-400">Locked</span>
            </div>
          </div>
        )}
      </div>
    </MotionDiv>
  );
};

export const Library: React.FC<LibraryProps> = ({ title, courses, onSelectCourse, onBack, userProgress, _northStar, _studentProfile, userName, userAvatarSeed, onLogout, onOpenSettings, onOpenPassport, onGoToDashboard, onGoToLearningPaths, onGoToInnovationZone, onGoToJourney, onChangeSubjects, completedCount = 0, totalCount = 0 }) => {
  const settingsCtx = useSettingsContext();
  const [sidebarOpen, setSidebarOpen] = useState(false);
  const [themePickerOpen, setThemePickerOpen] = useState(false);
  const [cardPickerOpen, setCardPickerOpen] = useState(false);
  const headerRef = React.useRef<HTMLElement>(null);
  const [headerHeight, setHeaderHeight] = useState(0);

  React.useLayoutEffect(() => {
    const measure = () => {
      if (headerRef.current) {
        setHeaderHeight(headerRef.current.getBoundingClientRect().height);
      }
    };
    measure();
    window.addEventListener('resize', measure);
    return () => window.removeEventListener('resize', measure);
  }, []);

  const hasSidebar = !!settingsCtx;

  const sidebarItems = [
    { icon: Home, label: 'Home', onClick: onBack, active: false },
    { icon: Mountain, label: 'My Journey', onClick: onGoToJourney, active: false },
    { icon: BarChart3, label: 'Dashboard', onClick: onGoToDashboard, active: false },
    { icon: Compass, label: 'Learning Paths', onClick: onGoToLearningPaths, active: false },
    { icon: Rocket, label: 'Innovation Zone', onClick: onGoToInnovationZone, active: false },
  ];

  const calculateCategoryProgress = () => {
    if (courses.length === 0) return 0;
    const totalCourses = courses.length;
    const completedCourses = courses.reduce((count, course) => {
      const progress = userProgress[course.id];
      const isComplete = progress && progress.unlockedSection >= course.sectionsCount;
      return count + (isComplete ? 1 : 0);
    }, 0);
    return Math.round((completedCourses / totalCourses) * 100);
  };

  const _overallProgress = calculateCategoryProgress();
  const _unlockedIndex = courses.length; // For now, all modules in a category are unlocked by default

  return (
    <div className="min-h-screen transition-colors duration-500 overflow-x-hidden relative" style={{ backgroundColor: '#FDF8F0' }}>

      {/* Sidebar — desktop only, starts below fixed header */}
      {hasSidebar && headerHeight > 0 && (
        <aside
          className={`hidden md:flex flex-col fixed left-0 bottom-0 z-[55] bg-white/80 dark:bg-zinc-900/80 backdrop-blur-sm border-r border-zinc-200 dark:border-zinc-800 overflow-y-auto transition-all duration-300 ease-[cubic-bezier(0.16,1,0.3,1)] ${sidebarOpen ? 'w-56' : 'w-[60px]'}`}
          style={{ top: `${headerHeight}px` }}
        >
          {/* Avatar row — click to toggle */}
          <button
            onClick={() => setSidebarOpen(!sidebarOpen)}
            className="flex items-center gap-3 px-3 py-3 w-full hover:bg-zinc-100 dark:hover:bg-zinc-800 transition-colors shrink-0"
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
          <nav className="flex-1 flex flex-col gap-1 px-2">
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
            {onOpenPassport && (
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
            )}

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

            {/* Theme toggle / picker */}
            {settingsCtx && (
              <div className="relative">
                <button
                  onClick={() => { setThemePickerOpen(!themePickerOpen); setCardPickerOpen(false); }}
                  className="w-full flex items-center gap-3 px-2.5 py-2 rounded-lg hover:bg-zinc-100 dark:hover:bg-zinc-800 transition-colors"
                >
                  <div className="shrink-0 flex items-center justify-center w-[18px]">
                    {settingsCtx.settings.darkMode ? (
                      <Moon size={18} strokeWidth={1.5} className="text-zinc-600 dark:text-zinc-400" />
                    ) : (
                      <Sun size={18} strokeWidth={1.5} className="text-amber-400" />
                    )}
                  </div>
                  <span className={`text-sm font-medium text-zinc-700 dark:text-zinc-300 whitespace-nowrap overflow-hidden transition-opacity duration-300 flex-1 text-left ${sidebarOpen ? 'opacity-100' : 'opacity-0'}`}>
                    Theme
                  </span>
                  <span className={`transition-opacity duration-300 ${sidebarOpen ? 'opacity-100' : 'opacity-0'}`}>
                    <div className="w-3.5 h-3.5 rounded-full border border-zinc-200 dark:border-zinc-700" style={{ backgroundColor: ACCENT_THEMES[settingsCtx.settings.accentTheme]?.hex || '#CC785C' }} />
                  </span>
                </button>
                <AnimatePresence>
                  {themePickerOpen && sidebarOpen && (
                    <MotionDiv
                      initial={{ opacity: 0, y: -4, scale: 0.95 }}
                      animate={{ opacity: 1, y: 0, scale: 1 }}
                      exit={{ opacity: 0, y: -4, scale: 0.95 }}
                      transition={{ duration: 0.15 }}
                      className="absolute left-0 bottom-full mb-2 w-56 bg-white dark:bg-zinc-900 border border-zinc-200 dark:border-zinc-800 rounded-xl shadow-lg dark:shadow-2xl p-3 z-50"
                    >
                      <button
                        onClick={() => { settingsCtx.updateSetting('darkMode', !settingsCtx.settings.darkMode); }}
                        className="w-full flex items-center justify-between p-2 rounded-lg hover:bg-zinc-100 dark:hover:bg-zinc-800 mb-2"
                      >
                        <span className="text-xs font-medium text-zinc-700 dark:text-zinc-300">{settingsCtx.settings.darkMode ? 'Light Mode' : 'Dark Mode'}</span>
                        {settingsCtx.settings.darkMode ? <Sun size={14} className="text-amber-400" /> : <Moon size={14} className="text-zinc-500" />}
                      </button>
                      <div className="border-t border-zinc-100 dark:border-zinc-800 pt-2">
                        <p className="text-[9px] font-bold uppercase tracking-widest text-zinc-400 dark:text-zinc-500 mb-2 px-1">Accent</p>
                        <div className="grid grid-cols-4 gap-1.5">
                          {ACCENT_THEME_LIST.filter(t => t.price === 0 || settingsCtx.unlockedThemes.includes(t.id)).map(theme => (
                            <button
                              key={theme.id}
                              onClick={() => { settingsCtx.updateSetting('accentTheme', theme.id as AccentThemeId); }}
                              title={theme.name}
                              className={`flex items-center justify-center p-1.5 rounded-lg transition-all ${
                                settingsCtx.settings.accentTheme === theme.id
                                  ? 'ring-2 ring-[var(--accent-hex)] bg-[rgba(var(--accent),0.1)]'
                                  : 'hover:bg-zinc-100 dark:hover:bg-zinc-800'
                              }`}
                            >
                              <div
                                className="w-5 h-5 rounded-full border border-white dark:border-zinc-700 shadow-sm"
                                style={{ backgroundColor: theme.hex }}
                              />
                            </button>
                          ))}
                        </div>
                      </div>
                    </MotionDiv>
                  )}
                </AnimatePresence>
              </div>
            )}

            {/* Card style picker */}
            {settingsCtx && (
              <div className="relative">
                <button
                  onClick={() => { setCardPickerOpen(!cardPickerOpen); setThemePickerOpen(false); }}
                  className="w-full flex items-center gap-3 px-2.5 py-2 rounded-lg hover:bg-zinc-100 dark:hover:bg-zinc-800 transition-colors"
                >
                  <div className="shrink-0 flex items-center justify-center w-[18px]">
                    <Layers size={18} strokeWidth={1.5} className="text-zinc-500" />
                  </div>
                  <span className={`text-sm font-medium text-zinc-700 dark:text-zinc-300 whitespace-nowrap overflow-hidden transition-opacity duration-300 flex-1 text-left ${sidebarOpen ? 'opacity-100' : 'opacity-0'}`}>
                    Cards
                  </span>
                </button>
                <AnimatePresence>
                  {cardPickerOpen && sidebarOpen && (
                    <MotionDiv
                      initial={{ opacity: 0, y: -4, scale: 0.95 }}
                      animate={{ opacity: 1, y: 0, scale: 1 }}
                      exit={{ opacity: 0, y: -4, scale: 0.95 }}
                      transition={{ duration: 0.15 }}
                      className="absolute left-0 bottom-full mb-2 w-56 bg-white dark:bg-zinc-900 border border-zinc-200 dark:border-zinc-800 rounded-xl shadow-lg dark:shadow-2xl p-3 z-50"
                    >
                      <p className="text-[9px] font-bold uppercase tracking-widest text-zinc-400 dark:text-zinc-500 mb-2 px-1">Card Style</p>
                      <div className="space-y-1">
                        {CARD_STYLES.filter(s => s.price === 0 || settingsCtx.unlockedCardStyles.includes(s.id)).map(style => (
                          <button
                            key={style.id}
                            onClick={() => { settingsCtx.updateSetting('cardStyle', style.id as CardStyleId); }}
                            className={`w-full flex items-center justify-between p-2 rounded-lg transition-all ${
                              settingsCtx.settings.cardStyle === style.id
                                ? 'ring-2 ring-[var(--accent-hex)] bg-[rgba(var(--accent),0.1)]'
                                : 'hover:bg-zinc-100 dark:hover:bg-zinc-800'
                            }`}
                          >
                            <div>
                              <p className="text-xs font-medium text-zinc-700 dark:text-zinc-300 text-left">{style.name}</p>
                              <p className="text-[10px] text-zinc-400 dark:text-zinc-500 text-left">{style.description}</p>
                            </div>
                          </button>
                        ))}
                      </div>
                    </MotionDiv>
                  )}
                </AnimatePresence>
              </div>
            )}

            {/* Settings */}
            {onOpenSettings && (
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
            )}

            {/* Log Out */}
            {onLogout && (
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
            )}
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
      )}

      {/* Main content area */}
      <div className={`flex flex-col items-center pt-24 md:pt-32 pb-12 transition-all duration-300 ease-[cubic-bezier(0.16,1,0.3,1)] ${hasSidebar ? (sidebarOpen ? 'md:ml-56' : 'md:ml-[60px]') : ''}`}>

      <header ref={headerRef} className="fixed top-0 left-0 right-0 z-[60] border-b px-4 py-4 md:px-10 md:py-6" style={{ backgroundColor: '#FDF8F0', borderColor: 'rgba(0,0,0,0.06)' }}>
        <div className="container mx-auto flex items-center justify-between">
          <div className="flex items-center gap-4 md:gap-8">
            <button onClick={onBack} className="p-2.5 rounded-xl bg-white dark:bg-zinc-900 border border-zinc-200 dark:border-zinc-800 transition-colors hover:bg-zinc-100 dark:hover:bg-zinc-800 focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-[rgba(var(--accent),0.5)]">
              <ArrowLeft size={18} className="text-zinc-900 dark:text-white" />
            </button>
            <div className="hidden md:block h-10 w-px bg-zinc-200 dark:bg-zinc-800" />
            <div>
              <p className="font-mono text-[9px] font-bold text-zinc-400 dark:text-zinc-500 uppercase tracking-[0.25em] mb-1">Module</p>
              <h1 className="font-serif font-semibold text-lg md:text-2xl tracking-tight text-zinc-900 dark:text-white truncate">{title}</h1>
            </div>
          </div>
        </div>
      </header>

      <main className="w-full px-4 md:px-6 pt-4 md:pt-10 relative z-10 flex items-center justify-center" style={{ minHeight: 'calc(100vh - 120px)' }}>
        <ModuleShowcase
          courses={courses}
          categoryTitle={title}
          categoryId={courses[0]?.category || 'learning-cheat-codes'}
          userProgress={userProgress}
          onSelectCourse={onSelectCourse}
        />
      </main>
      </div>
    </div>
  );
};
