
/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
*/

import React, { useState, useEffect, useRef, useCallback, useMemo, Suspense, lazy } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { Sun, Moon, LogOut, ArrowLeft, ArrowRight, Settings, Flame, ChevronRight, Trophy, Award, Target, BarChart3, Star, Home, Compass, Rocket, User, X, Mountain, Dumbbell, Timer, Lightbulb, Eye, EyeOff, School, GraduationCap } from 'lucide-react';
import { Library } from './components/Library';
import { KnowledgeTree, CategoryType } from './components/KnowledgeTree';
import { LoadingSpinner } from './components/LoadingSpinner';
import { Auth, SessionUser, getAvatarUrl, AVATAR_SEEDS } from './components/Auth';
import { AdminDashboard } from './components/AdminDashboard';
import { GCDashboard } from './components/GCDashboard';
import SettingsModal from './components/SettingsModal';
import StudyPassportModal from './components/StudyPassportModal';
import { auth, db } from './firebase';
import { onAuthStateChanged, signOut, signInWithEmailAndPassword, createUserWithEmailAndPassword, sendPasswordResetEmail, User as FirebaseUser } from 'firebase/auth';
import { doc, getDoc, setDoc, updateDoc, increment } from 'firebase/firestore';
import { ModuleProgress, UserProgress, UserSettings, NorthStar } from './types';
import { moduleComponents, InnovationZone } from './moduleRegistry';
import { useToast } from './components/Toast';
import { ALL_COURSES, categoryTitles, SUBJECT_TO_MODULE } from './courseData';
import { useSettings } from './hooks/useSettings';
import { useStreak, StreakData } from './hooks/useStreak';
import { useTodaysFocus, FocusRecommendation } from './hooks/useTodaysFocus';
import { usePoints } from './hooks/usePoints';
import { useStrategyMastery } from './hooks/useStrategyMastery';
import { useWeeklyChallenge } from './hooks/useWeeklyChallenge';
import { useRecommendation } from './hooks/useRecommendation';
import { useQuests } from './hooks/useQuests';
import DashboardView from './components/DashboardView';
import LearningPathsView from './components/LearningPathsView';
import TrainingPulse from './components/TrainingPulse';
import AchievementToast from './components/AchievementToast';
import RankUpModal from './components/RankUpModal';
import { useGamification } from './hooks/useGamification';
import { createStarterState } from './hooks/useIslandShop';
import { type AthleteRank, type AchievementDefinition, getRankForPoints } from './gamificationConfig';
import { type StudentSubjectProfile } from './components/subjectData';
import NorthStarEditModal from './components/NorthStarEditModal';
import ChangeSubjectsModal from './components/ChangeSubjectsModal';
import NotificationBell from './components/NotificationBell';
import { generateAutoNotifications } from './components/gc/gcNotifications';
import { ACCENT_THEME_LIST, ACCENT_THEMES } from './themeData';
import { POINTS, isModuleJustCompleted, isCategoryJustCompleted } from './journeyPointsConfig';
import { type AccentThemeId } from './types';
import { SettingsContext } from './contexts/SettingsContext';
import { SCHOOLS } from './schoolData';

const Onboarding = lazy(() => import('./components/Onboarding'));
const JourneyView = lazy(() => import('./components/journey/JourneyView'));
const TrainingHub = lazy(() => import('./components/TrainingHub'));
const StudySessionView = lazy(() => import('./components/study/StudySessionView'));
const InsightsView = lazy(() => import('./components/InsightsView'));

interface UserProfileProps {
  user: SessionUser;
  onLogout: () => void;
  settings: UserSettings;
  updateSetting: <K extends keyof UserSettings>(key: K, value: UserSettings[K]) => void;
  onOpenSettings: () => void;
  avatarOverride: string;
  streak: StreakData;
  recommendation: FocusRecommendation | null;
  onSelectModule: (moduleId: string) => void;
  onOpenPassport: () => void;
  onGoToDashboard: () => void;
  completedCount: number;
  totalCount: number;
  onOpenNorthStar: () => void;
  hasNorthStar: boolean;
  unlockedThemes: string[];
}

const UserProfile: React.FC<UserProfileProps> = ({ user, onLogout, settings, updateSetting, onOpenSettings, avatarOverride, streak, recommendation, onSelectModule, onOpenPassport, onGoToDashboard, completedCount, totalCount, onOpenNorthStar, hasNorthStar, unlockedThemes }) => {
  const [isOpen, setIsOpen] = useState(false);
  const dropdownRef = useRef<HTMLDivElement>(null);
  const displayAvatar = avatarOverride || user.avatar;

  useEffect(() => {
    if (!isOpen) return;
    const handleClickOutside = (e: MouseEvent) => {
      if (dropdownRef.current && !dropdownRef.current.contains(e.target as Node)) {
        setIsOpen(false);
      }
    };
    document.addEventListener('mousedown', handleClickOutside);
    return () => document.removeEventListener('mousedown', handleClickOutside);
  }, [isOpen]);

  return (
    <div className="relative" ref={dropdownRef}>
      <button onClick={() => setIsOpen(!isOpen)} className="flex items-center gap-2 focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-[rgba(var(--accent),0.5)] rounded-full">
        <img src={getAvatarUrl(displayAvatar)} alt="User Avatar" className="w-12 h-12 rounded-full bg-zinc-200" />
      </button>
      <AnimatePresence>
        {isOpen && (
          <motion.div
            initial={{ opacity: 0, y: -10, scale: 0.95 }}
            animate={{ opacity: 1, y: 0, scale: 1 }}
            exit={{ opacity: 0, y: -10, scale: 0.95 }}
            className="absolute top-full right-0 mt-2 w-72 bg-white dark:bg-zinc-900 border border-zinc-200 dark:border-zinc-800 rounded-xl shadow-lg p-4 max-h-[80vh] overflow-y-auto"
          >
            {/* User info */}
            <div className="flex items-center gap-3 border-b border-zinc-200/50 dark:border-white/10 pb-3 mb-3">
              <img src={getAvatarUrl(displayAvatar)} alt="User Avatar" className="w-12 h-12 rounded-full bg-zinc-200" />
              <div>
                <p className="font-bold text-zinc-800 dark:text-white">{user.name}</p>
                <p className="text-xs text-zinc-500">{user.isAdmin ? 'Admin' : 'Student'}</p>
              </div>
            </div>

            {/* Study Streak */}
            <div className="flex items-center gap-3 p-2 mb-1">
              <div className="w-8 h-8 rounded-lg bg-orange-50 dark:bg-orange-500/10 flex items-center justify-center">
                <Flame size={16} className="text-orange-500" />
              </div>
              <div className="flex-1">
                <p className="text-sm font-semibold text-zinc-800 dark:text-white">
                  {streak.currentStreak} day streak
                </p>
                {streak.longestStreak > 1 && (
                  <p className="text-[10px] text-zinc-400 dark:text-zinc-500">
                    Longest: {streak.longestStreak} days
                  </p>
                )}
              </div>
            </div>

            {/* Today's Focus */}
            <div className="border-t border-zinc-200/50 dark:border-white/10 pt-3 mt-2 mb-2">
              <p className="text-[10px] font-semibold uppercase tracking-widest text-zinc-400 dark:text-zinc-500 px-2 mb-2">Today's Focus</p>
              {recommendation && recommendation.reason !== 'all-complete' ? (
                <button
                  onClick={() => { setIsOpen(false); onSelectModule(recommendation.moduleId); }}
                  className="w-full flex items-center justify-between p-2 rounded-lg hover:bg-zinc-100 dark:hover:bg-white/5 group"
                >
                  <p className="text-sm font-medium text-zinc-700 dark:text-zinc-300 text-left line-clamp-1 pr-2">{recommendation.title}</p>
                  <ChevronRight size={14} className="text-zinc-400 dark:text-zinc-500 shrink-0 group-hover:translate-x-0.5 transition-transform" />
                </button>
              ) : (
                <div className="flex items-center gap-2 p-2">
                  <Trophy size={14} className="text-amber-500" />
                  <p className="text-sm font-medium text-amber-600 dark:text-amber-400">All modules complete!</p>
                </div>
              )}
            </div>

            {/* My Progress + Study Passport */}
            <div className="border-t border-zinc-200/50 dark:border-white/10 pt-2 mt-2 mb-2">
              <button
                onClick={() => { setIsOpen(false); onGoToDashboard(); }}
                className="w-full flex items-center gap-3 p-2 rounded-lg hover:bg-zinc-100 dark:hover:bg-white/5"
              >
                <div className="w-8 h-8 rounded-lg bg-[rgba(var(--accent),0.1)] flex items-center justify-center">
                  <BarChart3 size={16} className="text-[var(--accent-hex)]" />
                </div>
                <span className="text-sm font-medium text-zinc-700 dark:text-zinc-300 flex-1 text-left">My Progress</span>
              </button>
              <button
                onClick={() => { setIsOpen(false); onOpenPassport(); }}
                className="w-full flex items-center gap-3 p-2 rounded-lg hover:bg-zinc-100 dark:hover:bg-white/5"
              >
                <div className="w-8 h-8 rounded-lg bg-[rgba(var(--accent),0.1)] dark:bg-[rgba(var(--accent),0.1)] flex items-center justify-center">
                  <Award size={16} className="text-[var(--accent-hex)]" />
                </div>
                <span className="text-sm font-medium text-zinc-700 dark:text-zinc-300 flex-1 text-left">Study Passport</span>
                <span className="text-xs font-bold text-zinc-400 dark:text-zinc-500">{completedCount}/{totalCount}</span>
              </button>
            </div>

            {/* North Star + Theme, Settings, Log Out */}
            <div className="border-t border-zinc-200/50 dark:border-white/10 pt-2 mt-2">
              {hasNorthStar && (
                <button
                  onClick={() => { setIsOpen(false); onOpenNorthStar(); }}
                  className="w-full flex items-center gap-3 p-2 rounded-lg hover:bg-zinc-100 dark:hover:bg-white/5"
                >
                  <div className="w-8 h-8 rounded-lg bg-amber-50 dark:bg-amber-500/10 flex items-center justify-center">
                    <Star size={16} className="text-amber-500" />
                  </div>
                  <span className="text-sm font-medium text-zinc-700 dark:text-zinc-300 flex-1 text-left">My North Star</span>
                </button>
              )}
              <button onClick={() => updateSetting('darkMode', !settings.darkMode)} className="w-full flex items-center justify-between p-2 rounded-lg hover:bg-zinc-100 dark:hover:bg-white/5">
                  <span className="text-sm font-medium text-zinc-700 dark:text-zinc-300">{settings.darkMode ? 'Light Mode' : 'Dark Mode'}</span>
                   <AnimatePresence mode="wait">
                      {settings.darkMode ? (
                        <motion.div key="sun" initial={{ rotate: -90, opacity: 0 }} animate={{ rotate: 0, opacity: 1 }} exit={{ rotate: 90, opacity: 0 }} transition={{ duration: 0.2 }}>
                          <Sun size={16} className="text-amber-400" />
                        </motion.div>
                      ) : (
                        <motion.div key="moon" initial={{ rotate: -90, opacity: 0 }} animate={{ rotate: 0, opacity: 1 }} exit={{ rotate: 90, opacity: 0 }} transition={{ duration: 0.2 }}>
                          <Moon size={16} className="text-zinc-600" />
                        </motion.div>
                      )}
                  </AnimatePresence>
              </button>
              {/* Accent Theme Picker */}
              {ACCENT_THEME_LIST.filter(t => t.price === 0 || unlockedThemes.includes(t.id)).length > 1 && (
                <div className="mt-1 px-2">
                  <p className="text-[9px] font-bold uppercase tracking-widest text-zinc-400 dark:text-zinc-500 mb-1.5">Accent</p>
                  <div className="flex flex-wrap gap-1.5">
                    {ACCENT_THEME_LIST.filter(t => t.price === 0 || unlockedThemes.includes(t.id)).map(theme => (
                      <button
                        key={theme.id}
                        onClick={() => updateSetting('accentTheme', theme.id as AccentThemeId)}
                        title={theme.name}
                        className={`p-1 rounded-lg transition-all ${
                          settings.accentTheme === theme.id
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
              )}
              <button onClick={() => { setIsOpen(false); onOpenSettings(); }} className="w-full flex items-center gap-2 p-2 rounded-lg hover:bg-zinc-100 dark:hover:bg-white/5 mt-1">
                <Settings size={16} className="text-zinc-500" />
                <span className="text-sm font-medium text-zinc-700 dark:text-zinc-300">Settings</span>
              </button>
              <button onClick={onLogout} className="w-full flex items-center gap-2 p-2 rounded-lg hover:bg-zinc-100 dark:hover:bg-white/5 mt-1">
                <LogOut size={16} className="text-rose-500" />
                <span className="text-sm font-medium text-rose-500">Log Out</span>
              </button>
            </div>
          </motion.div>
        )}
      </AnimatePresence>
    </div>
  )
}

/* ── Mobile Bottom Navigation Bar ── */
interface MobileBottomNavProps {
  viewState: string;
  onGoHome: () => void;
  onGoToTrainingHub: () => void;
  onGoToStudy: () => void;
  onGoToJourney: () => void;
  onGoToInnovationZone: () => void;
  onOpenProfile: () => void;
  unreadNotifications?: number;
}

const MobileBottomNav: React.FC<MobileBottomNavProps> = ({ viewState, onGoHome, onGoToTrainingHub, onGoToStudy, onGoToJourney, onGoToInnovationZone, onOpenProfile, unreadNotifications = 0 }) => {
  const tabs = [
    { id: 'tree', label: 'Home', icon: Home, action: onGoHome },
    { id: 'gamification-hub', label: 'Training', icon: Dumbbell, action: onGoToTrainingHub },
    { id: 'study-session', label: 'Study', icon: Timer, action: onGoToStudy },
    { id: 'my-journey', label: 'Journey', icon: Mountain, action: onGoToJourney },
    { id: 'innovation-zone', label: 'Innovate', icon: Rocket, action: onGoToInnovationZone },
    { id: 'profile', label: 'Profile', icon: User, action: onOpenProfile },
  ];

  return (
    <nav
      className="fixed bottom-0 left-0 right-0 z-[90] md:hidden bg-white/80 dark:bg-zinc-900/80 backdrop-blur-xl border-t border-zinc-200/50 dark:border-white/[0.06]"
      style={{ paddingBottom: 'var(--sab, 0px)' }}
    >
      <div className="flex items-center justify-around h-16">
        {tabs.map((tab) => {
          const isActive = tab.id === viewState || (tab.id === 'tree' && viewState === 'category');
          return (
            <button
              key={tab.id}
              onClick={tab.action}
              className={`relative flex flex-col items-center justify-center gap-1 flex-1 h-full transition-colors focus-visible:outline-none focus-visible:bg-zinc-100 dark:focus-visible:bg-zinc-800 ${isActive ? 'text-[var(--accent-hex)]' : 'text-zinc-400 dark:text-zinc-500'}`}
            >
              <tab.icon size={20} strokeWidth={isActive ? 2 : 1.5} />
              <span className="text-[10px] font-medium">{tab.label}</span>
              {isActive && <div className="absolute bottom-1.5 w-1 h-1 rounded-full bg-[var(--accent-hex)]" />}
              {tab.id === 'profile' && unreadNotifications > 0 && (
                <div className="absolute top-2 right-1/2 translate-x-3 w-2 h-2 rounded-full bg-rose-500" />
              )}
            </button>
          );
        })}
      </div>
    </nav>
  );
};

/* ── Mobile Profile Sheet ── */
interface MobileProfileSheetProps {
  isOpen: boolean;
  onClose: () => void;
  user: SessionUser;
  onLogout: () => void;
  settings: UserSettings;
  updateSetting: <K extends keyof UserSettings>(key: K, value: UserSettings[K]) => void;
  onOpenSettings: () => void;
  avatarOverride: string;
  streak: StreakData;
  recommendation: FocusRecommendation | null;
  onSelectModule: (moduleId: string) => void;
  onOpenPassport: () => void;
  onGoToDashboard: () => void;
  onGoToInsights: () => void;
  completedCount: number;
  totalCount: number;
  onOpenNorthStar: () => void;
  hasNorthStar: boolean;
  unlockedThemes: string[];
}

const MobileProfileSheet: React.FC<MobileProfileSheetProps> = ({ isOpen, onClose, user, onLogout, settings, updateSetting, onOpenSettings, avatarOverride, streak, recommendation, onSelectModule, onOpenPassport, onGoToDashboard, onGoToInsights, completedCount, totalCount, onOpenNorthStar, hasNorthStar, unlockedThemes }) => {
  const displayAvatar = avatarOverride || user.avatar;
  return (
    <AnimatePresence>
      {isOpen && (
        <>
          {/* Backdrop */}
          <motion.div
            key="profile-backdrop"
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            exit={{ opacity: 0 }}
            onClick={onClose}
            className="fixed inset-0 z-[95] bg-black/40 md:hidden"
          />
          {/* Sheet */}
          <motion.div
            key="profile-sheet"
            initial={{ y: '100%' }}
            animate={{ y: 0 }}
            exit={{ y: '100%' }}
            transition={{ type: 'spring', damping: 28, stiffness: 300 }}
            className="fixed bottom-0 left-0 right-0 z-[96] md:hidden bg-white dark:bg-zinc-900 rounded-t-2xl border-t border-zinc-200 dark:border-zinc-800 max-h-[85vh] overflow-y-auto"
            style={{ paddingBottom: 'var(--sab, 0px)' }}
          >
            {/* Drag handle */}
            <div className="flex justify-center pt-3 pb-2">
              <div className="w-10 h-1 rounded-full bg-zinc-300 dark:bg-zinc-700" />
            </div>

            <div className="px-5 pb-6">
              {/* User info */}
              <div className="flex items-center justify-between mb-4">
                <div className="flex items-center gap-3">
                  <img src={getAvatarUrl(displayAvatar)} alt="Avatar" className="w-12 h-12 rounded-full bg-zinc-200" />
                  <div>
                    <p className="font-bold text-zinc-800 dark:text-white">{user.name}</p>
                    <p className="text-xs text-zinc-500">Student</p>
                  </div>
                </div>
                <button onClick={onClose} className="p-2 rounded-lg hover:bg-zinc-100 dark:hover:bg-zinc-800">
                  <X size={18} className="text-zinc-400" />
                </button>
              </div>

              {/* Streak */}
              <div className="flex items-center gap-3 p-3 rounded-xl bg-zinc-50 dark:bg-zinc-800/50 mb-3">
                <div className="w-8 h-8 rounded-lg bg-orange-50 dark:bg-orange-500/10 flex items-center justify-center">
                  <Flame size={16} className="text-orange-500" />
                </div>
                <div className="flex-1">
                  <p className="text-sm font-semibold text-zinc-800 dark:text-white">{streak.currentStreak} day streak</p>
                  {streak.longestStreak > 1 && (
                    <p className="text-[10px] text-zinc-400 dark:text-zinc-500">Longest: {streak.longestStreak} days</p>
                  )}
                </div>
              </div>

              {/* Today's Focus */}
              <div className="mb-3">
                <p className="text-[10px] font-semibold uppercase tracking-widest text-zinc-400 dark:text-zinc-500 px-1 mb-2">Today's Focus</p>
                {recommendation && recommendation.reason !== 'all-complete' ? (
                  <button
                    onClick={() => { onClose(); onSelectModule(recommendation.moduleId); }}
                    className="w-full flex items-center justify-between p-3 rounded-xl bg-zinc-50 dark:bg-zinc-800/50 group"
                  >
                    <p className="text-sm font-medium text-zinc-700 dark:text-zinc-300 text-left line-clamp-1 pr-2">{recommendation.title}</p>
                    <ChevronRight size={14} className="text-zinc-400 dark:text-zinc-500 shrink-0" />
                  </button>
                ) : (
                  <div className="flex items-center gap-2 p-3 rounded-xl bg-zinc-50 dark:bg-zinc-800/50">
                    <Trophy size={14} className="text-amber-500" />
                    <p className="text-sm font-medium text-amber-600 dark:text-amber-400">All modules complete!</p>
                  </div>
                )}
              </div>

              {/* Actions */}
              <div className="space-y-1">
                <button onClick={() => { onClose(); onOpenPassport(); }} className="w-full flex items-center gap-3 p-3 rounded-xl hover:bg-zinc-50 dark:hover:bg-zinc-800/50">
                  <div className="w-8 h-8 rounded-lg bg-[rgba(var(--accent),0.1)] flex items-center justify-center"><Award size={16} className="text-[var(--accent-hex)]" /></div>
                  <span className="text-sm font-medium text-zinc-700 dark:text-zinc-300 flex-1 text-left">Study Passport</span>
                  <span className="text-xs font-bold text-zinc-400 dark:text-zinc-500">{completedCount}/{totalCount}</span>
                </button>
                <button onClick={() => { onClose(); onGoToInsights(); }} className="w-full flex items-center gap-3 p-3 rounded-xl hover:bg-zinc-50 dark:hover:bg-zinc-800/50">
                  <div className="w-8 h-8 rounded-lg bg-amber-50 dark:bg-amber-500/10 flex items-center justify-center"><Lightbulb size={16} className="text-amber-500" /></div>
                  <span className="text-sm font-medium text-zinc-700 dark:text-zinc-300 flex-1 text-left">Insights</span>
                </button>
                {hasNorthStar && (
                  <button onClick={() => { onClose(); onOpenNorthStar(); }} className="w-full flex items-center gap-3 p-3 rounded-xl hover:bg-zinc-50 dark:hover:bg-zinc-800/50">
                    <div className="w-8 h-8 rounded-lg bg-amber-50 dark:bg-amber-500/10 flex items-center justify-center"><Star size={16} className="text-amber-500" /></div>
                    <span className="text-sm font-medium text-zinc-700 dark:text-zinc-300 flex-1 text-left">My North Star</span>
                  </button>
                )}
                <button onClick={() => updateSetting('darkMode', !settings.darkMode)} className="w-full flex items-center gap-3 p-3 rounded-xl hover:bg-zinc-50 dark:hover:bg-zinc-800/50">
                  <div className="w-8 h-8 rounded-lg bg-zinc-100 dark:bg-zinc-800 flex items-center justify-center">
                    {settings.darkMode ? <Sun size={16} className="text-amber-400" /> : <Moon size={16} className="text-zinc-600" />}
                  </div>
                  <span className="text-sm font-medium text-zinc-700 dark:text-zinc-300 flex-1 text-left">{settings.darkMode ? 'Light Mode' : 'Dark Mode'}</span>
                </button>
                {ACCENT_THEME_LIST.filter(t => t.price === 0 || unlockedThemes.includes(t.id)).length > 1 && (
                  <div className="px-3 py-2">
                    <p className="text-[9px] font-bold uppercase tracking-widest text-zinc-400 dark:text-zinc-500 mb-1.5">Accent</p>
                    <div className="flex flex-wrap gap-1.5">
                      {ACCENT_THEME_LIST.filter(t => t.price === 0 || unlockedThemes.includes(t.id)).map(theme => (
                        <button
                          key={theme.id}
                          onClick={() => updateSetting('accentTheme', theme.id as AccentThemeId)}
                          title={theme.name}
                          className={`p-1.5 rounded-lg transition-all ${
                            settings.accentTheme === theme.id
                              ? 'ring-2 ring-[var(--accent-hex)] bg-[rgba(var(--accent),0.1)]'
                              : 'hover:bg-zinc-100 dark:hover:bg-zinc-800'
                          }`}
                        >
                          <div
                            className="w-6 h-6 rounded-full border border-white dark:border-zinc-700 shadow-sm"
                            style={{ backgroundColor: theme.hex }}
                          />
                        </button>
                      ))}
                    </div>
                  </div>
                )}
                <button onClick={() => { onClose(); onOpenSettings(); }} className="w-full flex items-center gap-3 p-3 rounded-xl hover:bg-zinc-50 dark:hover:bg-zinc-800/50">
                  <div className="w-8 h-8 rounded-lg bg-zinc-100 dark:bg-zinc-800 flex items-center justify-center"><Settings size={16} className="text-zinc-500" /></div>
                  <span className="text-sm font-medium text-zinc-700 dark:text-zinc-300 flex-1 text-left">Settings</span>
                </button>
                <button onClick={() => { onClose(); onLogout(); }} className="w-full flex items-center gap-3 p-3 rounded-xl hover:bg-zinc-50 dark:hover:bg-zinc-800/50">
                  <div className="w-8 h-8 rounded-lg bg-rose-50 dark:bg-rose-500/10 flex items-center justify-center"><LogOut size={16} className="text-rose-500" /></div>
                  <span className="text-sm font-medium text-rose-500 flex-1 text-left">Log Out</span>
                </button>
              </div>
            </div>
          </motion.div>
        </>
      )}
    </AnimatePresence>
  );
};

/* ── Module Error Boundary ── */
interface ModuleErrorBoundaryProps {
  onBack: () => void;
  children: React.ReactNode;
}

interface ModuleErrorBoundaryState {
  hasError: boolean;
  error: Error | null;
}

class ModuleErrorBoundary extends React.Component<ModuleErrorBoundaryProps, ModuleErrorBoundaryState> {
  constructor(props: ModuleErrorBoundaryProps) {
    super(props);
    this.state = { hasError: false, error: null };
  }

  static getDerivedStateFromError(error: Error): ModuleErrorBoundaryState {
    return { hasError: true, error };
  }

  componentDidCatch(error: Error, info: React.ErrorInfo) {
    console.error('Module failed to load:', error, info);
  }

  render() {
    if (this.state.hasError) {
      return (
        <div className="min-h-screen bg-zinc-50 dark:bg-zinc-950 flex items-center justify-center p-6">
          <div className="max-w-md w-full bg-white dark:bg-zinc-900 border border-zinc-200 dark:border-zinc-800 rounded-2xl p-8 text-center">
            <div className="w-14 h-14 mx-auto mb-4 rounded-full bg-rose-100 dark:bg-rose-500/10 flex items-center justify-center">
              <span className="text-2xl">!</span>
            </div>
            <h2 className="text-lg font-bold text-zinc-800 dark:text-white mb-2">Something went wrong</h2>
            <p className="text-sm text-zinc-500 dark:text-zinc-400 mb-6">
              {this.state.error?.message || 'This module failed to load. Please try again.'}
            </p>
            <button
              onClick={() => {
                this.setState({ hasError: false, error: null });
                this.props.onBack();
              }}
              className="px-6 py-2.5 rounded-full bg-[var(--accent-hex)] text-white text-sm font-medium hover:opacity-90 transition-opacity"
            >
              Go Back
            </button>
          </div>
        </div>
      );
    }

    return this.props.children;
  }
}

// ── Split-Panel Login Page ──
const MotionDiv = motion.div as any;
const MotionButton = motion.button as any;

const LoginPage: React.FC<{ handleLoginSuccess: (u: SessionUser) => void }> = ({ handleLoginSuccess }) => {
  const [authMode, setAuthMode] = useState<'login' | 'register'>('login');
  const [loginType, setLoginType] = useState<'student' | 'gc' | null>(null);
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [confirmPassword, setConfirmPassword] = useState('');
  const [name, setName] = useState('');
  const [school, setSchool] = useState('');
  const [gcSchool, setGcSchool] = useState('');
  const [avatar, setAvatar] = useState('');
  const [showPassword, setShowPassword] = useState(false);
  const [showConfirmPw, setShowConfirmPw] = useState(false);
  const [error, setError] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [resetSent, setResetSent] = useState(false);

  const handleLogin = async () => {
    setIsLoading(true);
    setError('');
    try {
      const emailToUse = email.includes('@') ? email : `${email}@nextstep.app`;
      const cred = await signInWithEmailAndPassword(auth, emailToUse, password);
      const userDoc = await getDoc(doc(db, 'users', cred.user.uid));
      if (userDoc.exists()) {
        const data = userDoc.data();
        handleLoginSuccess({
          uid: cred.user.uid,
          name: data.name || 'Student',
          avatar: data.avatar || 'James',
          isAdmin: data.isAdmin || false,
          role: data.role || 'student',
          school: data.school || '',
          yearGroup: data.yearGroup,
        });
      }
    } catch (e: any) {
      setError(e.code === 'auth/invalid-credential' ? 'Invalid email or password' : 'Something went wrong. Try again.');
    }
    setIsLoading(false);
  };

  const handleGCLogin = async () => {
    if (!gcSchool || !password.trim()) {
      setError('Please select your school and enter your password.');
      return;
    }
    setIsLoading(true);
    setError('');
    try {
      const gcEmail = `gc-${gcSchool}@nextstep.app`;
      await signInWithEmailAndPassword(auth, gcEmail, password);
    } catch (e: any) {
      setError('Invalid credentials.');
    }
    setIsLoading(false);
  };

  const handleRegister = async () => {
    if (password !== confirmPassword) { setError('Passwords don\'t match'); return; }
    if (!name.trim()) { setError('Please enter your name'); return; }
    if (!school) { setError('Please select your school'); return; }
    if (!avatar) { setError('Please choose an avatar'); return; }
    setIsLoading(true);
    setError('');
    try {
      const emailToUse = `${name.toLowerCase().replace(/\s+/g, '')}${Date.now().toString(36)}@nextstep.app`;
      const cred = await createUserWithEmailAndPassword(auth, emailToUse, password);
      await setDoc(doc(db, 'users', cred.user.uid), {
        name: name.trim(),
        avatar,
        school,
        role: 'student',
        createdAt: new Date().toISOString(),
      });
      handleLoginSuccess({
        uid: cred.user.uid,
        name: name.trim(),
        avatar,
        school,
        role: 'student',
      });
    } catch (e: any) {
      setError('Registration failed. Try again.');
    }
    setIsLoading(false);
  };

  const handleForgotPassword = async () => {
    if (!email) { setError('Enter your email first'); return; }
    try {
      await sendPasswordResetEmail(auth, email);
      setResetSent(true);
    } catch { setError('Could not send reset email'); }
  };

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (authMode === 'register') {
      handleRegister();
    } else if (loginType === 'gc') {
      handleGCLogin();
    } else {
      handleLogin();
    }
  };

  const resetForm = () => {
    setEmail('');
    setPassword('');
    setConfirmPassword('');
    setName('');
    setSchool('');
    setGcSchool('');
    setAvatar('');
    setError('');
    setResetSent(false);
    setShowPassword(false);
    setShowConfirmPw(false);
  };

  const inputClass = "w-full py-3 px-4 rounded-xl text-sm text-zinc-800 placeholder-zinc-400 outline-none transition-all";
  const inputBorder: React.CSSProperties = { backgroundColor: '#FAF7F4', border: '1px solid #e4e4e7' };

  // ── Left Panel: Animated Gradient with Framer Motion blobs ──
  const gradientPanel = (
    <div className="hidden md:block w-1/2 relative overflow-hidden" style={{ borderRadius: '16px 0 0 16px', backgroundColor: '#0C1A2A' }}>
      {/* Animated color blobs — each has an outer motion wrapper (no filter) and inner colored div (with blur) */}
      <motion.div
        className="absolute"
        style={{ top: '-20%', left: '-10%', width: 450, height: 450 }}
        animate={{ x: [0, 80, -40, 0], y: [0, -60, 70, 0], scale: [1, 1.15, 0.9, 1] }}
        transition={{ duration: 20, repeat: Infinity, repeatType: 'loop' as const, ease: 'easeInOut' }}
      >
        <div style={{ width: '100%', height: '100%', borderRadius: '50%', background: 'rgba(40, 70, 160, 0.7)', filter: 'blur(80px)' }} />
      </motion.div>
      <motion.div
        className="absolute"
        style={{ top: '25%', right: '-15%', width: 400, height: 400 }}
        animate={{ x: [0, -70, 50, 0], y: [0, 80, -40, 0], scale: [1, 0.85, 1.15, 1] }}
        transition={{ duration: 25, repeat: Infinity, repeatType: 'loop' as const, ease: 'easeInOut' }}
      >
        <div style={{ width: '100%', height: '100%', borderRadius: '50%', background: 'rgba(120, 40, 180, 0.55)', filter: 'blur(80px)' }} />
      </motion.div>
      <motion.div
        className="absolute"
        style={{ bottom: '-15%', left: '15%', width: 350, height: 350 }}
        animate={{ x: [0, 60, -80, 0], y: [0, -70, 40, 0], scale: [1, 1.1, 0.88, 1] }}
        transition={{ duration: 22, repeat: Infinity, repeatType: 'loop' as const, ease: 'easeInOut' }}
      >
        <div style={{ width: '100%', height: '100%', borderRadius: '50%', background: 'rgba(200, 50, 100, 0.5)', filter: 'blur(80px)' }} />
      </motion.div>
      <motion.div
        className="absolute"
        style={{ bottom: '-10%', right: '0%', width: 350, height: 350 }}
        animate={{ x: [0, -50, 60, 0], y: [0, 50, -30, 0], scale: [1, 1.12, 0.92, 1] }}
        transition={{ duration: 18, repeat: Infinity, repeatType: 'loop' as const, ease: 'easeInOut' }}
      >
        <div style={{ width: '100%', height: '100%', borderRadius: '50%', background: 'rgba(42, 125, 111, 0.65)', filter: 'blur(80px)' }} />
      </motion.div>

    </div>
  );

  // ── GC Login View ──
  if (loginType === 'gc') {
    return (
      <div className="min-h-screen flex items-center justify-center p-4 md:p-8" style={{ backgroundColor: '#FAFAF7' }}>
        <MotionDiv
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.5, ease: 'easeOut' }}
          className="w-full max-w-5xl bg-white rounded-2xl overflow-hidden flex"
          style={{ minHeight: 540, boxShadow: '0 4px 40px rgba(0,0,0,0.06)' }}
        >
          {/* Left: Animated Gradient */}
          {gradientPanel}

          {/* Right: GC Form */}
          <div className="w-full md:w-1/2 flex flex-col justify-center px-8 md:px-14 py-16">
            <div className="w-full max-w-[380px] mx-auto">
              {/* Logo */}
              <MotionDiv initial={{ opacity: 0 }} animate={{ opacity: 1 }} transition={{ duration: 0.5 }}>
                <p className="text-zinc-400 text-[10px] font-semibold tracking-[0.2em] mb-8">NEXTSTEPUNI</p>
              </MotionDiv>

              <AnimatePresence mode="wait">
                <MotionDiv
                  key="gc-form"
                  initial={{ opacity: 0, x: 20 }}
                  animate={{ opacity: 1, x: 0 }}
                  exit={{ opacity: 0, x: -20 }}
                  transition={{ duration: 0.3 }}
                >
                  {/* Back button */}
                  <button
                    type="button"
                    onClick={() => { setLoginType(null); resetForm(); }}
                    className="flex items-center gap-1.5 text-sm text-zinc-400 hover:text-zinc-600 mb-6 transition-colors"
                  >
                    <ArrowLeft size={14} /> Back
                  </button>

                  {/* Heading */}
                  <h2 className="text-3xl font-semibold text-zinc-900 tracking-tight mb-1">Guidance Counsellor</h2>
                  <p className="text-sm text-zinc-400 mb-8">Select your school and enter your password.</p>

                  <form onSubmit={handleSubmit} className="space-y-4">
                    {/* School dropdown */}
                    <div>
                      <label className="text-sm text-zinc-600 font-medium mb-1.5 block">School</label>
                      <select
                        value={gcSchool}
                        onChange={e => { setGcSchool(e.target.value); setError(''); }}
                        className={`${inputClass} appearance-none cursor-pointer ${!gcSchool ? 'text-zinc-400' : ''}`}
                        style={inputBorder}
                        autoFocus
                      >
                        <option value="" disabled>Select your school</option>
                        {SCHOOLS.map(s => (
                          <option key={s.id} value={s.id}>{s.name}</option>
                        ))}
                      </select>
                    </div>

                    {/* Password */}
                    <div>
                      <label className="text-sm text-zinc-600 font-medium mb-1.5 block">Password</label>
                      <div className="relative">
                        <input
                          type={showPassword ? 'text' : 'password'}
                          value={password}
                          onChange={e => { setPassword(e.target.value); setError(''); }}
                          placeholder="Enter your password"
                          className={inputClass}
                          style={inputBorder}
                        />
                        <button type="button" onClick={() => setShowPassword(!showPassword)} className="absolute right-3 top-1/2 -translate-y-1/2 text-zinc-400 hover:text-zinc-600 transition-colors">
                          {showPassword ? <EyeOff size={16} /> : <Eye size={16} />}
                        </button>
                      </div>
                    </div>

                    {/* Error */}
                    <AnimatePresence>{error && <MotionDiv initial={{ opacity: 0 }} animate={{ opacity: 1 }} exit={{ opacity: 0 }} className="text-sm text-red-500 font-medium">{error}</MotionDiv>}</AnimatePresence>

                    {/* Submit */}
                    <MotionButton
                      type="submit"
                      disabled={isLoading}
                      whileHover={{ scale: 1.01 }}
                      whileTap={{ scale: 0.99 }}
                      className="w-full py-3 rounded-xl text-white text-sm font-semibold transition-all disabled:opacity-60 disabled:cursor-not-allowed"
                      style={{ backgroundColor: '#2A7D6F' }}
                    >
                      {isLoading ? 'Signing in...' : 'Sign In'}
                    </MotionButton>
                  </form>

                  {/* DEV: Skip Login */}
                  <button
                    onClick={() => handleLoginSuccess({ uid: 'dev-student', name: 'Dev User', avatar: 'Casper', isAdmin: false })}
                    className="mt-10 mx-auto block px-3 py-1 bg-red-600/10 text-red-400 border border-red-600/20 rounded-full text-[9px] font-mono hover:bg-red-600/20 transition-colors"
                  >
                    DEV: Skip Login
                  </button>
                </MotionDiv>
              </AnimatePresence>
            </div>
          </div>
        </MotionDiv>
      </div>
    );
  }

  // ── Main Login / Register View ──
  return (
    <div className="min-h-screen flex items-center justify-center p-4 md:p-8" style={{ backgroundColor: '#FAFAF7' }}>
      <MotionDiv
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.5, ease: 'easeOut' }}
        className="w-full max-w-5xl bg-white rounded-2xl overflow-hidden flex"
        style={{ minHeight: 540, boxShadow: '0 2px 8px rgba(0,0,0,0.06), 0 12px 40px rgba(0,0,0,0.04)', border: '1.5px solid rgba(0,0,0,0.25)' }}
      >
        {/* Left: Animated Gradient */}
        {gradientPanel}

        {/* Right: Form */}
        <div className="w-full md:w-1/2 flex flex-col justify-center px-8 md:px-14 py-16">
          <div className="w-full max-w-[380px] mx-auto">
            {/* Logo */}
            <MotionDiv initial={{ opacity: 0 }} animate={{ opacity: 1 }} transition={{ duration: 0.5 }}>
              <p className="text-zinc-400 text-[10px] font-semibold tracking-[0.2em] mb-8">NEXTSTEPUNI</p>
            </MotionDiv>

            <AnimatePresence mode="wait">
              {authMode === 'login' ? (
                <MotionDiv
                  key="login-form"
                  initial={{ opacity: 0, x: 20 }}
                  animate={{ opacity: 1, x: 0 }}
                  exit={{ opacity: 0, x: -20 }}
                  transition={{ duration: 0.3 }}
                >
                  {/* Heading */}
                  <h2 className="text-3xl font-semibold text-zinc-900 tracking-tight mb-8">Welcome back</h2>

                  <form onSubmit={handleSubmit} className="space-y-4">
                    {/* Email / Username */}
                    <div>
                      <label className="text-sm text-zinc-600 font-medium mb-1.5 block">Email / Username</label>
                      <input
                        type="text"
                        value={email}
                        onChange={e => { setEmail(e.target.value); setError(''); setResetSent(false); }}
                        placeholder="your@email.com or username"
                        className={inputClass}
                        style={inputBorder}
                        autoFocus
                      />
                    </div>

                    {/* Password */}
                    <div>
                      <div className="flex items-center justify-between mb-1.5">
                        <label className="text-sm text-zinc-600 font-medium">Password</label>
                        <button type="button" onClick={handleForgotPassword} className="text-xs font-medium transition-colors hover:opacity-70" style={{ color: '#2A7D6F' }}>
                          {resetSent ? 'Reset email sent!' : 'Forgot password?'}
                        </button>
                      </div>
                      <div className="relative">
                        <input
                          type={showPassword ? 'text' : 'password'}
                          value={password}
                          onChange={e => { setPassword(e.target.value); setError(''); }}
                          placeholder="Enter your password"
                          className={inputClass}
                          style={inputBorder}
                        />
                        <button type="button" onClick={() => setShowPassword(!showPassword)} className="absolute right-3 top-1/2 -translate-y-1/2 text-zinc-400 hover:text-zinc-600 transition-colors">
                          {showPassword ? <EyeOff size={16} /> : <Eye size={16} />}
                        </button>
                      </div>
                    </div>

                    {/* Error */}
                    <AnimatePresence>{error && <MotionDiv initial={{ opacity: 0 }} animate={{ opacity: 1 }} exit={{ opacity: 0 }} className="text-sm text-red-500 font-medium">{error}</MotionDiv>}</AnimatePresence>
                    {/* Reset sent */}
                    {resetSent && <p className="text-sm text-green-500 font-medium">Check your email for a reset link.</p>}

                    {/* Submit */}
                    <MotionButton
                      type="submit"
                      disabled={isLoading}
                      whileHover={{ scale: 1.01 }}
                      whileTap={{ scale: 0.99 }}
                      className="w-full py-3 rounded-xl text-white text-sm font-semibold transition-all disabled:opacity-60 disabled:cursor-not-allowed"
                      style={{ backgroundColor: '#2A7D6F' }}
                    >
                      {isLoading ? 'Signing in...' : 'Sign In'}
                    </MotionButton>
                  </form>

                  {/* Toggle to register */}
                  <p className="text-sm text-zinc-400 text-center mt-6">
                    Don&apos;t have an account?{' '}
                    <button type="button" onClick={() => { setAuthMode('register'); resetForm(); }} className="text-sm font-semibold transition-colors hover:opacity-80" style={{ color: '#2A7D6F' }}>Register</button>
                  </p>

                  {/* OR divider */}
                  <div className="flex items-center gap-4 mt-6">
                    <div className="flex-1 h-px bg-zinc-200" />
                    <span className="text-xs text-zinc-400">OR</span>
                    <div className="flex-1 h-px bg-zinc-200" />
                  </div>

                  {/* GC Login button */}
                  <MotionButton
                    type="button"
                    onClick={() => { setLoginType('gc'); resetForm(); }}
                    whileHover={{ scale: 1.01, backgroundColor: '#fafaf7' }}
                    whileTap={{ scale: 0.99 }}
                    className="w-full py-3 rounded-xl text-sm font-medium text-zinc-600 transition-all flex items-center justify-center gap-2 mt-4"
                    style={{ border: '1px solid #e4e4e7', backgroundColor: '#ffffff' }}
                  >
                    <GraduationCap size={16} />
                    Sign in as Guidance Counsellor
                  </MotionButton>
                </MotionDiv>
              ) : (
                <MotionDiv
                  key="register-form"
                  initial={{ opacity: 0, x: 20 }}
                  animate={{ opacity: 1, x: 0 }}
                  exit={{ opacity: 0, x: -20 }}
                  transition={{ duration: 0.3 }}
                >
                  {/* Heading */}
                  <h2 className="text-3xl font-semibold text-zinc-900 tracking-tight mb-8">Create your account</h2>

                  <form onSubmit={handleSubmit} className="space-y-4">
                    {/* Name */}
                    <div>
                      <label className="text-sm text-zinc-600 font-medium mb-1.5 block">Name</label>
                      <input
                        type="text"
                        value={name}
                        onChange={e => { setName(e.target.value); setError(''); }}
                        placeholder="Choose a username"
                        className={inputClass}
                        style={inputBorder}
                        autoFocus
                      />
                    </div>

                    {/* School dropdown */}
                    <div>
                      <label className="text-sm text-zinc-600 font-medium mb-1.5 block">School</label>
                      <div className="relative">
                        <select
                          value={school}
                          onChange={e => { setSchool(e.target.value); setError(''); }}
                          className={`${inputClass} appearance-none cursor-pointer ${!school ? 'text-zinc-400' : ''}`}
                          style={inputBorder}
                        >
                          <option value="" disabled>Select your school</option>
                          {SCHOOLS.map(s => (
                            <option key={s.id} value={s.id}>{s.name}</option>
                          ))}
                        </select>
                        <School size={16} className="absolute right-3 top-1/2 -translate-y-1/2 text-zinc-400 pointer-events-none" />
                      </div>
                    </div>

                    {/* Avatar picker */}
                    <div>
                      <label className="text-sm text-zinc-600 font-medium mb-1.5 block">Choose your avatar</label>
                      <div className="grid grid-cols-4 gap-2">
                        {AVATAR_SEEDS.map(seed => (
                          <button
                            key={seed}
                            type="button"
                            onClick={() => setAvatar(seed)}
                            className={`rounded-xl aspect-square p-1 transition-all ${avatar === seed ? 'ring-2 ring-offset-1' : 'ring-1 ring-zinc-200 hover:ring-zinc-400'}`}
                            style={avatar === seed ? { backgroundColor: '#FAF7F4', ringColor: '#2A7D6F' } : { backgroundColor: '#ffffff' }}
                          >
                            <img src={getAvatarUrl(seed)} alt={seed} className="w-full h-full rounded-lg" />
                          </button>
                        ))}
                      </div>
                    </div>

                    {/* Password */}
                    <div>
                      <label className="text-sm text-zinc-600 font-medium mb-1.5 block">Password</label>
                      <div className="relative">
                        <input
                          type={showPassword ? 'text' : 'password'}
                          value={password}
                          onChange={e => { setPassword(e.target.value); setError(''); }}
                          placeholder="Create a password"
                          className={inputClass}
                          style={inputBorder}
                        />
                        <button type="button" onClick={() => setShowPassword(!showPassword)} className="absolute right-3 top-1/2 -translate-y-1/2 text-zinc-400 hover:text-zinc-600 transition-colors">
                          {showPassword ? <EyeOff size={16} /> : <Eye size={16} />}
                        </button>
                      </div>
                    </div>

                    {/* Confirm Password */}
                    <div>
                      <label className="text-sm text-zinc-600 font-medium mb-1.5 block">Confirm Password</label>
                      <div className="relative">
                        <input
                          type={showConfirmPw ? 'text' : 'password'}
                          value={confirmPassword}
                          onChange={e => { setConfirmPassword(e.target.value); setError(''); }}
                          placeholder="Confirm your password"
                          className={inputClass}
                          style={inputBorder}
                        />
                        <button type="button" onClick={() => setShowConfirmPw(!showConfirmPw)} className="absolute right-3 top-1/2 -translate-y-1/2 text-zinc-400 hover:text-zinc-600 transition-colors">
                          {showConfirmPw ? <EyeOff size={16} /> : <Eye size={16} />}
                        </button>
                      </div>
                    </div>

                    {/* Error */}
                    <AnimatePresence>{error && <MotionDiv initial={{ opacity: 0 }} animate={{ opacity: 1 }} exit={{ opacity: 0 }} className="text-sm text-red-500 font-medium">{error}</MotionDiv>}</AnimatePresence>

                    {/* Submit */}
                    <MotionButton
                      type="submit"
                      disabled={isLoading}
                      whileHover={{ scale: 1.01 }}
                      whileTap={{ scale: 0.99 }}
                      className="w-full py-3 rounded-xl text-white text-sm font-semibold transition-all disabled:opacity-60 disabled:cursor-not-allowed"
                      style={{ backgroundColor: '#2A7D6F' }}
                    >
                      {isLoading ? 'Creating account...' : 'Create Account'}
                    </MotionButton>
                  </form>

                  {/* Toggle to login */}
                  <p className="text-sm text-zinc-400 text-center mt-6">
                    Already have an account?{' '}
                    <button type="button" onClick={() => { setAuthMode('login'); resetForm(); }} className="text-sm font-semibold transition-colors hover:opacity-80" style={{ color: '#2A7D6F' }}>Sign in</button>
                  </p>
                </MotionDiv>
              )}
            </AnimatePresence>

            {/* DEV: Skip Login */}
            <button
              onClick={() => handleLoginSuccess({ uid: 'dev-student', name: 'Dev User', avatar: 'Casper', isAdmin: false })}
              className="mt-10 mx-auto block px-3 py-1 bg-red-600/10 text-red-400 border border-red-600/20 rounded-full text-[9px] font-mono hover:bg-red-600/20 transition-colors"
            >
              DEV: Skip Login
            </button>
          </div>
        </div>
      </MotionDiv>
    </div>
  );
};

const App: React.FC = () => {
  const { showToast } = useToast();
  const [viewState, setViewState] = useState<'tree' | 'category' | 'module' | 'innovation-zone' | 'dashboard' | 'learning-paths' | 'onboarding' | 'my-journey' | 'gamification-hub' | 'study-session' | 'insights'>('tree');
  const [currentCategory, setCurrentCategory] = useState<CategoryType | null>(null);
  const [currentModuleId, setCurrentModuleId] = useState<string | null>(null);
  const [cameFromJourney, setCameFromJourney] = useState(false);
  const [journeyResult, setJourneyResult] = useState<{ endingId: string; finalStats?: any } | null>(null);
  const [user, setUser] = useState<SessionUser | null>(null);
  const [userProgress, setUserProgress] = useState<UserProgress>({});
  const [isLoadingAuth, setIsLoadingAuth] = useState(true);
  const [needsOnboarding, setNeedsOnboarding] = useState(false);
  const [settingsOpen, setSettingsOpen] = useState(false);
  const [passportOpen, setPassportOpen] = useState(false);
  const [northStar, setNorthStar] = useState<NorthStar | null>(null);
  const [northStarEditOpen, setNorthStarEditOpen] = useState(false);
  const [changeSubjectsOpen, setChangeSubjectsOpen] = useState(false);
  const [mobileProfileOpen, setMobileProfileOpen] = useState(false);
  const [studentProfile, setStudentProfile] = useState<StudentSubjectProfile | null>(null);
  const [unlockedAvatarSeeds, setUnlockedAvatarSeeds] = useState<string[]>([]);
  const [unlockedThemes, setUnlockedThemes] = useState<string[]>([]);
  const [unlockedCardStyles, setUnlockedCardStyles] = useState<string[]>([]);
  const [dismissedGuides, setDismissedGuides] = useState<Record<string, string>>({});
  const [timetableBlockContext, setTimetableBlockContext] = useState<{ subject: string; sessionType: 'new-learning' | 'practice' | 'revision'; durationMinutes: number; dateKey: string; blockId: string } | null>(null);
  const [timetableCompletions, setTimetableCompletions] = useState<Record<string, string[]>>({});
  const [unreadNotificationCount, setUnreadNotificationCount] = useState(0);
  const { settings, updateSetting, isLoaded: settingsLoaded } = useSettings(user?.uid, user?.avatar);
  const { streak } = useStreak(user?.uid);
  const { recommendation } = useTodaysFocus(userProgress, ALL_COURSES);
  const pointsData = usePoints(user?.uid);

  // Gamification
  const gamification = useGamification({
    uid: user?.uid,
    userProgress,
    pointsData,
    streak,
    northStar,
  });
  const [toastQueue, setToastQueue] = useState<(AchievementDefinition | 'bonus-flash')[]>([]);
  const [currentToast, setCurrentToast] = useState<AchievementDefinition | null>(null);
  const [isBonusFlashToast, setIsBonusFlashToast] = useState(false);
  const [rankUpModal, setRankUpModal] = useState<AthleteRank | null>(null);
  const prevRankRef = useRef<string | null>(null);

  // Process toast queue
  useEffect(() => {
    if (currentToast || isBonusFlashToast) return; // Already showing
    if (toastQueue.length === 0) return;
    const next = toastQueue[0];
    setToastQueue(q => q.slice(1));
    if (next === 'bonus-flash') {
      setIsBonusFlashToast(true);
    } else {
      setCurrentToast(next);
    }
  }, [toastQueue, currentToast, isBonusFlashToast]);

  // Detect rank changes
  useEffect(() => {
    if (!gamification.isLoaded) return;
    const currentRankId = gamification.state.currentRank.id;
    if (prevRankRef.current !== null && prevRankRef.current !== currentRankId) {
      setRankUpModal(gamification.state.currentRank);
    }
    prevRankRef.current = currentRankId;
  }, [gamification.state.currentRank.id, gamification.isLoaded]);

  const isPopstateRef = useRef(false);

  const studentCourses = useMemo(() => {
    if (!studentProfile) return ALL_COURSES;
    const relevantModuleIds = new Set(
      studentProfile.subjects.map(s => SUBJECT_TO_MODULE[s.subjectName]).filter(Boolean)
    );
    return ALL_COURSES.filter(c => {
      if (c.category === 'subject-specific-science') {
        return relevantModuleIds.has(c.id);
      }
      return true;
    });
  }, [studentProfile]);

  const strategyMastery = useStrategyMastery(user?.uid, userProgress, studentCourses);
  const weeklyChallenge = useWeeklyChallenge(user?.uid);
  const { recommendation: smartRec } = useRecommendation(user?.uid, userProgress, studentCourses, streak, studentProfile, timetableCompletions);
  const { questState, claimReward: claimQuestReward, reload: reloadQuest } = useQuests(user?.uid, userProgress, studentCourses, streak, studentProfile, timetableCompletions);

  const completedCount = studentCourses.filter(c => {
    const p = userProgress[c.id];
    return p && p.unlockedSection >= c.sectionsCount;
  }).length;

  // Browser back/forward button support
  useEffect(() => {
    const handlePopState = (e: PopStateEvent) => {
      isPopstateRef.current = true;
      const state = e.state;
      if (!state || state.view === 'tree') {
        setCurrentCategory(null);
        setCurrentModuleId(null);
        setCameFromJourney(false);
        setViewState('tree');
      } else if (state.view === 'category') {
        setCurrentModuleId(null);
        setCurrentCategory(state.category);
        setCameFromJourney(false);
        setViewState('category');
      } else if (state.view === 'innovation-zone') {
        setCurrentModuleId(null);
        setCameFromJourney(false);
        setViewState('innovation-zone');
      } else if (state.view === 'dashboard') {
        setCurrentModuleId(null);
        setCameFromJourney(false);
        setViewState('dashboard');
      } else if (state.view === 'learning-paths') {
        setCurrentModuleId(null);
        setCameFromJourney(false);
        setViewState('learning-paths');
      } else if (state.view === 'my-journey') {
        setCurrentModuleId(null);
        setCameFromJourney(false);
        setViewState('my-journey');
      } else if (state.view === 'gamification-hub') {
        setCurrentModuleId(null);
        setCameFromJourney(false);
        setViewState('gamification-hub');
      } else if (state.view === 'study-session') {
        setCurrentModuleId(null);
        setCameFromJourney(false);
        setViewState('study-session');
      } else if (state.view === 'insights') {
        setCurrentModuleId(null);
        setCameFromJourney(false);
        setViewState('insights');
      } else if (state.view === 'module') {
        setCurrentModuleId(state.moduleId);
        setCurrentCategory(state.category || null);
        setCameFromJourney(state.fromJourney || false);
        setViewState('module');
      }
      window.scrollTo(0, 0);
      isPopstateRef.current = false;
    };
    window.addEventListener('popstate', handlePopState);
    return () => window.removeEventListener('popstate', handlePopState);
  }, []);

  // Set initial history state when logged-in user lands on tree
  useEffect(() => {
    if (user && !user.isAdmin && user.role !== 'gc' && viewState === 'tree' && !window.history.state?.view) {
      window.history.replaceState({ view: 'tree' }, '');
    }
  }, [user, viewState]);

  // Redirect to onboarding for users without a subject profile
  useEffect(() => {
    if (user && !user.isAdmin && user.role !== 'gc' && needsOnboarding && !isLoadingAuth && viewState === 'tree') {
      setViewState('onboarding');
    }
  }, [user, needsOnboarding, isLoadingAuth, viewState]);

  // Set up the real-time auth listener
  useEffect(() => {
    const unsubscribe = onAuthStateChanged(auth, async (firebaseUser: FirebaseUser | null) => {
      if (firebaseUser) {
        // Admin user — no Firestore profile needed
        if (firebaseUser.email === 'admin@nextstep.app') {
          setUser({
            uid: firebaseUser.uid,
            name: 'Admin',
            avatar: 'Charlie',
            isAdmin: true,
          });
          setUserProgress({});
          setIsLoadingAuth(false);
          return;
        }

        // Regular student — fetch their profile and progress from Firestore
        const userDocRef = doc(db, "users", firebaseUser.uid);
        const progressDocRef = doc(db, "progress", firebaseUser.uid);

        try {
          const [userDoc, progressDoc] = await Promise.all([getDoc(userDocRef), getDoc(progressDocRef)]);

          if (userDoc.exists()) {
            const userData = userDoc.data();
            const isGC = userData.role === 'gc';
            setUser({
              uid: firebaseUser.uid,
              name: userData.name,
              avatar: userData.avatar || 'Charlie',
              isAdmin: false,
              role: userData.role,
              school: userData.school,
              yearGroup: userData.yearGroup,
            });
            if (progressDoc.exists()) {
              const progressData = progressDoc.data();
              setUserProgress(progressData as UserProgress);
              if (progressData.cosmeticUnlocks?.avatarSeeds) {
                setUnlockedAvatarSeeds(progressData.cosmeticUnlocks.avatarSeeds);
              }
              if (progressData.cosmeticUnlocks?.themeColors) {
                setUnlockedThemes(progressData.cosmeticUnlocks.themeColors);
              }
              if (progressData.cosmeticUnlocks?.cardStyles) {
                setUnlockedCardStyles(progressData.cosmeticUnlocks.cardStyles);
              }
              if (progressData.northStar) {
                setNorthStar(progressData.northStar as NorthStar);
              }
              if (progressData.dismissedGuides) {
                setDismissedGuides(progressData.dismissedGuides);
              }
              if (progressData.subjectProfile) {
                setStudentProfile(progressData.subjectProfile as StudentSubjectProfile);
              } else {
                setNeedsOnboarding(true);
              }
              if (progressData.timetableCompletions) {
                setTimetableCompletions(progressData.timetableCompletions as Record<string, string[]>);
              }
              // Fire-and-forget auto-notifications
              if (userData.role !== 'gc') {
                generateAutoNotifications(firebaseUser.uid, progressData).catch(() => {});
              }
            } else {
              setUserProgress({});
              setNeedsOnboarding(true);
            }
          } else {
            // User creation was interrupted — Firebase auth exists but no Firestore profile.
            // Attempt to recover by creating a minimal profile from the auth data.
            try {
              const recoveredName = firebaseUser.email?.split('@')[0] || 'Student';
              await setDoc(doc(db, 'users', firebaseUser.uid), {
                name: recoveredName,
                avatar: 'Charlie',
                school: '',
              });
              setUser({
                uid: firebaseUser.uid,
                name: recoveredName,
                avatar: 'Charlie',
                isAdmin: false,
              });
              setUserProgress({});
              setNeedsOnboarding(true);
            } catch (recoveryError) {
              console.error('Failed to recover orphaned account:', recoveryError);
              await signOut(auth);
              setUser(null);
              setUserProgress({});
            }
          }
        } catch (error) {
           console.error("Error fetching user data:", error);
           // Don't silently sign out — let the user in with minimal data
           const fallbackName = firebaseUser.displayName || firebaseUser.email?.split('@')[0] || 'Student';
           setUser({
             uid: firebaseUser.uid,
             name: fallbackName,
             avatar: 'Charlie',
             isAdmin: false,
           });
           setUserProgress({});
           setNeedsOnboarding(true);
           setIsLoadingAuth(false);
           showToast("Your profile couldn't be loaded fully. Some data may be missing.", 'warning', 5000);
        }

      } else {
        // User is signed out
        setUser(null);
        setUserProgress({});
      }
      setIsLoadingAuth(false);
    });

    return () => unsubscribe(); // Cleanup subscription on unmount
  }, []);

  const handleLoginSuccess = (loggedInUser: SessionUser) => {
    setUser(loggedInUser);
  };

  const handleLogout = async () => {
    await signOut(auth);
  };

  const handleProgressUpdate = async (moduleId: string, newProgress: ModuleProgress) => {
    if (!user || user.isAdmin) return;

    const prevSection = userProgress[moduleId]?.unlockedSection ?? 0;
    const newSection = newProgress.unlockedSection;

    setUserProgress(prev => ({ ...prev, [moduleId]: newProgress }));

    try {
      const progressDocRef = doc(db, "progress", user.uid);
      await setDoc(progressDocRef, { [moduleId]: newProgress }, { merge: true });

      // Award points for newly unlocked sections
      if (newSection > prevSection) {
        const sectionsUnlocked = newSection - prevSection;
        let pointsToAward = sectionsUnlocked * POINTS.SECTION_COMPLETE;

        const course = ALL_COURSES.find(c => c.id === moduleId);
        if (course) {
          // Module complete bonus
          if (isModuleJustCompleted(newSection, course.sectionsCount) && !isModuleJustCompleted(prevSection, course.sectionsCount)) {
            pointsToAward += POINTS.MODULE_COMPLETE_BONUS;
          }

          // Category complete bonus
          const updatedProgress = { ...userProgress, [moduleId]: newProgress };
          if (isCategoryJustCompleted(moduleId, updatedProgress, ALL_COURSES)) {
            // Check it wasn't already complete before
            const wasComplete = isCategoryJustCompleted(moduleId, userProgress, ALL_COURSES);
            if (!wasComplete) {
              pointsToAward += POINTS.CATEGORY_COMPLETE_BONUS;
            }
          }
        }

        if (pointsToAward > 0) {
          // Roll for bonus flash (15% chance of 2x)
          const isBonus = gamification.rollBonusFlash();
          const finalPoints = isBonus ? pointsToAward * 2 : pointsToAward;

          await updateDoc(progressDocRef, {
            'pointsData.totalEarned': increment(finalPoints),
          });
          pointsData.reload();

          if (isBonus) {
            setToastQueue(q => [...q, 'bonus-flash']);
          }

          // Update weekly goal progress for sections
          gamification.updateWeeklyGoalProgress('sections', sectionsUnlocked);
        }
      }

      // Check for newly unlocked achievements (after points have been written)
      const newAchievements = await gamification.checkAndUnlockAchievements();
      if (newAchievements.length > 0) {
        setToastQueue(q => [...q, ...newAchievements]);
      }
      gamification.reload();
    } catch (error) {
      console.error("Failed to save progress:", error);
      showToast('Couldn\'t save your progress — check your connection', 'error');
    }
  };

  const handleSelectCategory = (category: CategoryType) => {
    setCurrentCategory(category);
    setViewState('category');
    window.scrollTo(0, 0);
    if (!isPopstateRef.current) {
      window.history.pushState({ view: 'category', category }, '');
    }
  };

  const handleSelectModule = (moduleId: string) => {
    const fromJourney = viewState === 'innovation-zone';
    setCameFromJourney(fromJourney);
    setCurrentModuleId(moduleId);
    setViewState('module');
    window.scrollTo(0, 0);
    if (!isPopstateRef.current) {
      window.history.pushState({ view: 'module', moduleId, category: currentCategory, fromJourney }, '');
    }
  };

  const handleGoToInnovationZone = () => {
    setViewState('innovation-zone');
    window.scrollTo(0, 0);
    if (!isPopstateRef.current) {
      window.history.pushState({ view: 'innovation-zone' }, '');
    }
  };

  const handleGoToDashboard = () => {
    setViewState('dashboard');
    window.scrollTo(0, 0);
    if (!isPopstateRef.current) {
      window.history.pushState({ view: 'dashboard' }, '');
    }
  };

  const handleGoToLearningPaths = () => {
    setViewState('learning-paths');
    window.scrollTo(0, 0);
    if (!isPopstateRef.current) {
      window.history.pushState({ view: 'learning-paths' }, '');
    }
  };

  const handleGoToJourney = () => {
    setViewState('my-journey');
    window.scrollTo(0, 0);
    if (!isPopstateRef.current) {
      window.history.pushState({ view: 'my-journey' }, '');
    }
  };

  const handleGoToGamificationHub = () => {
    setViewState('gamification-hub');
    window.scrollTo(0, 0);
    if (!isPopstateRef.current) {
      window.history.pushState({ view: 'gamification-hub' }, '');
    }
  };

  const handleGoToStudy = () => {
    setTimetableBlockContext(null);
    setViewState('study-session');
    window.scrollTo(0, 0);
    if (!isPopstateRef.current) {
      window.history.pushState({ view: 'study-session' }, '');
    }
  };

  const handleStudyFromTimetable = useCallback((block: { subject: string; sessionType: 'new-learning' | 'practice' | 'revision'; durationMinutes: number; dateKey: string; blockId: string }) => {
    setTimetableBlockContext(block);
    setViewState('study-session');
    window.scrollTo(0, 0);
    if (!isPopstateRef.current) {
      window.history.pushState({ view: 'study-session' }, '');
    }
  }, []);

  const handleGoToInsights = useCallback(() => {
    setViewState('insights');
    window.scrollTo(0, 0);
    if (!isPopstateRef.current) {
      window.history.pushState({ view: 'insights' }, '');
    }
  }, []);

  const handleGoHome = () => {
    setCurrentCategory(null);
    setCurrentModuleId(null);
    setCameFromJourney(false);
    setViewState('tree');
    window.scrollTo(0, 0);
    if (!isPopstateRef.current) {
      window.history.pushState({ view: 'tree' }, '');
    }
  };

  const handleOnboardingComplete = async (profile: StudentSubjectProfile, northStarData?: NorthStar) => {
    if (!user) return;
    try {
      const progressDocRef = doc(db, 'progress', user.uid);
      const saveData: Record<string, any> = { subjectProfile: profile };
      if (northStarData) {
        saveData.northStar = northStarData;
        saveData.islandState = createStarterState(northStarData.category);
        setNorthStar(northStarData);
      }
      await setDoc(progressDocRef, saveData, { merge: true });
      // Also save yearGroup to the users doc for GC dashboard filtering
      if (profile.yearGroup) {
        const userDocRef = doc(db, 'users', user.uid);
        await setDoc(userDocRef, { yearGroup: profile.yearGroup }, { merge: true });
        setUser(prev => prev ? { ...prev, yearGroup: profile.yearGroup } : prev);
      }
    } catch (error) {
      console.error('Failed to save subject profile:', error);
      showToast('Couldn\'t save — check your connection', 'error');
    }
    setStudentProfile(profile);
    setNeedsOnboarding(false);
    setViewState('tree');
    window.history.replaceState({ view: 'tree' }, '');
  };

  const handleNorthStarSave = async (ns: NorthStar) => {
    setNorthStar(ns);
    if (!user) return;
    try {
      const progressDocRef = doc(db, 'progress', user.uid);
      await setDoc(progressDocRef, { northStar: ns }, { merge: true });
    } catch (error) {
      console.error('Failed to save North Star:', error);
      showToast('Couldn\'t save — check your connection', 'error');
    }
  };

  const handleOnboardingSkip = () => {
    setNeedsOnboarding(false);
    setViewState('tree');
    window.history.replaceState({ view: 'tree' }, '');
  };

  const handleChangeSubjectsSave = async (profile: StudentSubjectProfile) => {
    setStudentProfile(profile);
    setChangeSubjectsOpen(false);
    if (!user) return;
    try {
      const progressDocRef = doc(db, 'progress', user.uid);
      await setDoc(progressDocRef, { subjectProfile: profile }, { merge: true });
    } catch (error) {
      console.error('Failed to save updated subject profile:', error);
      showToast('Couldn\'t save — check your connection', 'error');
    }
  };

  const handleBackToTree = () => {
    window.history.back();
  };

  const handleBackToCategory = () => {
    window.history.back();
  };

  const handleDismissGuide = useCallback(async (guideId: string) => {
    setDismissedGuides(prev => ({ ...prev, [guideId]: new Date().toISOString() }));
    if (user?.uid) {
      try {
        await setDoc(doc(db, 'progress', user.uid),
          { dismissedGuides: { [guideId]: new Date().toISOString() } },
          { merge: true }
        );
      } catch (err) {
        console.error('Failed to persist guide dismissal:', err);
        showToast('Couldn\'t save — check your connection', 'error');
      }
    }
  }, [user?.uid, showToast]);

  const renderContent = () => {
    if (isLoadingAuth) {
        return <LoadingSpinner />;
    }

    if (!user) {
      return <LoginPage handleLoginSuccess={handleLoginSuccess} />;
    }

    if (user.isAdmin) {
      return <AdminDashboard allCourses={ALL_COURSES} onLogout={handleLogout} />;
    }

    if (user.role === 'gc' && user.school) {
      return <GCDashboard school={user.school} onLogout={handleLogout} allCourses={ALL_COURSES} gcName={user.name} />;
    }

    if (viewState === 'study-session') {
      return (
        <Suspense fallback={<LoadingSpinner />}>
          <StudySessionView
            user={user}
            studentProfile={studentProfile}
            userProgress={userProgress}
            allCourses={studentCourses}
            pointsReload={() => { pointsData.reload(); reloadQuest(); }}
            streak={streak}
            onBack={handleBackToTree}
            onStrategyMasteryRecompute={strategyMastery.recompute}
            strategyMastery={strategyMastery.masteryMap}
            onGoToTrainingHub={handleGoToGamificationHub}
            dismissedGuides={dismissedGuides}
            onDismissGuide={handleDismissGuide}
            weeklyChallenge={weeklyChallenge}
            timetableBlock={timetableBlockContext}
            onTimetableBlockComplete={async (dateKey, blockId, _actualMinutes) => {
              if (!user?.uid) return;
              try {
                const progressRef = doc(db, 'progress', user.uid);
                const progressSnap = await getDoc(progressRef);
                const data = progressSnap.data() || {};
                const completions = (data.timetableCompletions || {}) as Record<string, string[]>;
                const dayArr = [...(completions[dateKey] ?? [])];
                if (!dayArr.includes(blockId)) dayArr.push(blockId);
                const updated = { ...completions, [dateKey]: dayArr };
                await setDoc(progressRef, { timetableCompletions: updated }, { merge: true });
              } catch (e) {
                console.error('Failed to auto-complete timetable block:', e);
                showToast('Couldn\'t save — check your connection', 'error');
              }
              setTimetableBlockContext(null);
            }}
          />
        </Suspense>
      );
    }

    if (viewState === 'insights') {
      return (
        <Suspense fallback={<LoadingSpinner />}>
          <InsightsView
            uid={user.uid}
            streak={streak}
            strategyMastery={strategyMastery.masteryMap}
            onBack={handleBackToTree}
          />
        </Suspense>
      );
    }

    if (viewState === 'gamification-hub') {
      return (
        <Suspense fallback={<LoadingSpinner />}>
          <TrainingHub
            gamificationState={gamification.state}
            streak={streak}
            pointsBalance={pointsData.balance}
            northStar={northStar}
            onBack={handleBackToTree}
            onOpenJourney={handleGoToJourney}
            userProgress={userProgress}
            allCourses={studentCourses}
            strategyMastery={strategyMastery.masteryMap}
            dismissedGuides={dismissedGuides}
            onDismissGuide={handleDismissGuide}
            weeklyChallenge={weeklyChallenge}
            pointsReload={() => { pointsData.reload(); reloadQuest(); }}
            onGoToStudy={handleGoToStudy}
          />
        </Suspense>
      );
    }

    if (viewState === 'dashboard') {
      return (
        <DashboardView
          userProgress={userProgress}
          allCourses={studentCourses}
          categoryTitles={categoryTitles}
          streak={streak}
          recommendation={recommendation}
          onSelectModule={handleSelectModule}
          onBack={handleBackToTree}
          pointsBalance={pointsData.balance}
        />
      );
    }

    if (viewState === 'learning-paths') {
      return (
        <LearningPathsView
          allCourses={studentCourses}
          userProgress={userProgress}
          onSelectModule={handleSelectModule}
          onBack={handleBackToTree}
        />
      );
    }

    if (viewState === 'onboarding') {
      return (
        <Suspense fallback={<LoadingSpinner />}>
          <Onboarding userName={user.name} onComplete={handleOnboardingComplete} onSkip={handleOnboardingSkip} />
        </Suspense>
      );
    }

    if (viewState === 'my-journey') {
      return (
        <Suspense fallback={<LoadingSpinner />}>
          <JourneyView
            onBack={handleBackToTree}
            user={user}
            northStar={northStar}
            onOpenNorthStar={() => setNorthStarEditOpen(true)}
            pointsBalance={pointsData.balance}
            onPointsReload={pointsData.reload}
            userProgress={userProgress}
            allCourses={studentCourses}
            subjects={studentProfile?.subjects?.map((s: any) => s.subjectName) ?? []}
            flaresEnabled={settings?.flaresToggle !== false}
          />
        </Suspense>
      );
    }

    if (viewState === 'tree') {
      return <KnowledgeTree
        key="knowledge-tree"
        onSelectCategory={handleSelectCategory}
        onGoToInnovationZone={handleGoToInnovationZone}
        onGoToDashboard={handleGoToDashboard}
        onGoToLearningPaths={handleGoToLearningPaths}
        onGoToJourney={handleGoToJourney}
        onGoToStudy={handleGoToStudy}
        onGoToInsights={handleGoToInsights}
        allCourses={studentCourses}
        onSelectModule={handleSelectModule}
        categoryTitles={categoryTitles}
        userProgress={userProgress}
        userName={user?.name}
        userAvatarSeed={(settings.avatar || user?.avatar) ?? undefined}
        onLogout={handleLogout}
        onOpenSettings={() => setSettingsOpen(true)}
        onOpenPassport={() => setPassportOpen(true)}
        onChangeSubjects={studentProfile ? () => setChangeSubjectsOpen(true) : undefined}
        settings={settings}
        updateSetting={updateSetting}
        unlockedThemes={unlockedThemes}
        completedCount={completedCount}
        totalCount={studentCourses.length}
        streak={streak}
        pointsBalance={pointsData.balance}
        northStar={northStar}
        studentProfile={studentProfile}
        timetableCompletions={timetableCompletions}
        smartRecommendation={smartRec}
        questState={questState}
        onClaimQuestReward={() => { claimQuestReward(); pointsData.reload?.(); }}
        onRecommendationAction={() => {
          handleGoToStudy();
        }}
      />;
    }

    if (viewState === 'category' && currentCategory) {
      let categoryCourses = ALL_COURSES.filter(c => c.category === currentCategory);

      // For subject-specific-science, only show modules relevant to the student's chosen subjects
      if (currentCategory === 'subject-specific-science' && studentProfile) {
        const relevantModuleIds = new Set(
          studentProfile.subjects.map(s => SUBJECT_TO_MODULE[s.subjectName]).filter(Boolean)
        );
        categoryCourses = categoryCourses.filter(c => relevantModuleIds.has(c.id));
      }

      return (
        <Library
          title={categoryTitles[currentCategory]}
          courses={categoryCourses}
          onSelectCourse={handleSelectModule}
          onBack={handleBackToTree}
          userProgress={userProgress}
          northStar={northStar}
          studentProfile={studentProfile}
          userName={user?.name}
          userAvatarSeed={(settings.avatar || user?.avatar) ?? undefined}
          onLogout={handleLogout}
          onOpenSettings={() => setSettingsOpen(true)}
          onOpenPassport={() => setPassportOpen(true)}
          onGoToDashboard={handleGoToDashboard}
          onGoToLearningPaths={handleGoToLearningPaths}
          onGoToInnovationZone={handleGoToInnovationZone}
          onGoToJourney={handleGoToJourney}
          onChangeSubjects={studentProfile ? () => setChangeSubjectsOpen(true) : undefined}
          completedCount={completedCount}
          totalCount={studentCourses.length}
        />
      );
    }

    if (viewState === 'innovation-zone') {
        return (
          <Suspense fallback={<LoadingSpinner />}>
            <InnovationZone onBack={handleBackToTree} onSelectModule={handleSelectModule} user={user} autoOpenJourney={cameFromJourney} savedJourneyResult={journeyResult} onJourneyComplete={setJourneyResult} settings={settings} updateSetting={updateSetting} onCosmeticUnlocksChange={(unlocks) => { setUnlockedAvatarSeeds(unlocks.avatarSeeds || []); setUnlockedThemes(unlocks.themeColors || []); setUnlockedCardStyles(unlocks.cardStyles || []); }} onStudyNow={handleStudyFromTimetable} />
          </Suspense>
        );
    }

    if (viewState === 'module' && currentModuleId) {
      const ModuleComponent = moduleComponents[currentModuleId];
      if (ModuleComponent) {
        return (
          <ModuleErrorBoundary onBack={handleBackToCategory}>
            <Suspense fallback={<LoadingSpinner />}>
              {cameFromJourney && (
                <div className="fixed top-0 left-0 right-0 z-[80] bg-[var(--accent-hex)] dark:bg-[var(--accent-hex)]">
                  <button
                    onClick={handleBackToCategory}
                    className="w-full flex items-center justify-center gap-2 py-2 text-white text-xs font-bold hover:bg-[var(--accent-dark-hex)] dark:hover:bg-[var(--accent-dark-hex)] transition-colors"
                  >
                    <ArrowLeft size={14} />
                    Back to Journey Results
                  </button>
                </div>
              )}
              <ModuleComponent
                onBack={handleBackToCategory}
                progress={userProgress[currentModuleId] || { unlockedSection: 0 }}
                onProgressUpdate={(p) => handleProgressUpdate(currentModuleId, p)}
              />
            </Suspense>
          </ModuleErrorBoundary>
        );
      }
      // Module ID not found in registry — show fallback and navigate back
      return (
        <div className="min-h-screen bg-zinc-50 dark:bg-zinc-950 flex items-center justify-center p-6">
          <div className="max-w-md w-full bg-white dark:bg-zinc-900 border border-zinc-200 dark:border-zinc-800 rounded-2xl p-8 text-center">
            <h2 className="text-lg font-bold text-zinc-800 dark:text-white mb-2">Module not found</h2>
            <p className="text-sm text-zinc-500 dark:text-zinc-400 mb-6">
              The module &ldquo;{currentModuleId}&rdquo; could not be found.
            </p>
            <button
              onClick={handleBackToCategory}
              className="px-6 py-2.5 rounded-full bg-[var(--accent-hex)] text-white text-sm font-medium hover:opacity-90 transition-opacity"
            >
              Go Back
            </button>
          </div>
        </div>
      );
    }

    // Fallback: unknown view state — navigate back to tree
    handleBackToTree();
    return <LoadingSpinner />;
  };

  return (
    <SettingsContext.Provider value={{ settings, updateSetting, unlockedThemes, unlockedCardStyles }}>
    <div className="min-h-screen bg-zinc-50 dark:bg-zinc-950 transition-colors duration-500">
      {user && viewState !== 'onboarding' && user.role !== 'gc' && !user.isAdmin && (
        <div className={`fixed top-6 right-6 z-[100] ${viewState === 'tree' || viewState === 'category' ? 'hidden' : viewState === 'my-journey' ? 'hidden' : 'hidden md:block'}`}>
          <div className="flex items-center gap-2">
            <div>
              {gamification.isLoaded && (
                <TrainingPulse
                  gamificationState={gamification.state}
                  onOpenHub={handleGoToGamificationHub}
                  streak={streak}
                  pointsBalance={pointsData.balance}
                />
              )}
              <AchievementToast
                achievement={currentToast}
                isBonusFlash={isBonusFlashToast}
                onDismiss={() => { setCurrentToast(null); setIsBonusFlashToast(false); }}
              />
            </div>
            <NotificationBell uid={user.uid} onUnreadCountChange={setUnreadNotificationCount} />
            <UserProfile user={user} onLogout={handleLogout} settings={settings} updateSetting={updateSetting} onOpenSettings={() => setSettingsOpen(true)} avatarOverride={settings.avatar} streak={streak} recommendation={recommendation} onSelectModule={handleSelectModule} onOpenPassport={() => setPassportOpen(true)} onGoToDashboard={handleGoToDashboard} completedCount={completedCount} totalCount={studentCourses.length} onOpenNorthStar={() => setNorthStarEditOpen(true)} hasNorthStar={northStar !== null} unlockedThemes={unlockedThemes} />
          </div>
        </div>
      )}

      {/* Mobile: TrainingPulse in top-left when not on tree/category/onboarding */}
      {user && viewState !== 'onboarding' && viewState !== 'tree' && viewState !== 'category' && viewState !== 'module' && viewState !== 'study-session' && viewState !== 'my-journey' && user.role !== 'gc' && !user.isAdmin && gamification.isLoaded && (
        <div className="fixed top-4 left-4 z-[100] md:hidden">
          <TrainingPulse
            gamificationState={gamification.state}
            onOpenHub={handleGoToGamificationHub}
            streak={streak}
            pointsBalance={pointsData.balance}
          />
          <AchievementToast
            achievement={currentToast}
            isBonusFlash={isBonusFlashToast}
            onDismiss={() => { setCurrentToast(null); setIsBonusFlashToast(false); }}
          />
        </div>
      )}

      {renderContent()}

      {user && viewState !== 'onboarding' && viewState !== 'module' && !user.isAdmin && user.role !== 'gc' && (
        <MobileBottomNav
          viewState={viewState}
          onGoHome={handleGoHome}
          onGoToTrainingHub={handleGoToGamificationHub}
          onGoToStudy={handleGoToStudy}
          onGoToJourney={handleGoToJourney}
          onGoToInnovationZone={handleGoToInnovationZone}
          onOpenProfile={() => setMobileProfileOpen(true)}
          unreadNotifications={unreadNotificationCount}
        />
      )}

      {user && !user.isAdmin && user.role !== 'gc' && (
        <MobileProfileSheet
          isOpen={mobileProfileOpen}
          onClose={() => setMobileProfileOpen(false)}
          user={user}
          onLogout={handleLogout}
          settings={settings}
          updateSetting={updateSetting}
          onOpenSettings={() => setSettingsOpen(true)}
          avatarOverride={settings.avatar}
          streak={streak}
          recommendation={recommendation}
          onSelectModule={handleSelectModule}
          onOpenPassport={() => setPassportOpen(true)}
          onGoToDashboard={handleGoToDashboard}
          onGoToInsights={handleGoToInsights}
          completedCount={completedCount}
          totalCount={studentCourses.length}
          onOpenNorthStar={() => setNorthStarEditOpen(true)}
          hasNorthStar={northStar !== null}
          unlockedThemes={unlockedThemes}
        />
      )}

      {user && (
        <>
          <SettingsModal
            isOpen={settingsOpen}
            onClose={() => setSettingsOpen(false)}
            settings={settings}
            updateSetting={updateSetting}
            unlockedAvatarSeeds={unlockedAvatarSeeds}
            unlockedThemes={unlockedThemes}
            unlockedCardStyles={unlockedCardStyles}
            userName={user?.name}
            userSchool={user?.school}
            onChangeSubjects={studentProfile ? () => { setSettingsOpen(false); setChangeSubjectsOpen(true); } : undefined}
            onResetNorthStar={() => { setSettingsOpen(false); setNorthStarEditOpen(true); }}
            onLogout={handleLogout}
          />
          <StudyPassportModal
            isOpen={passportOpen}
            onClose={() => setPassportOpen(false)}
            userProgress={userProgress}
            allCourses={studentCourses}
            categoryTitles={categoryTitles}
          />
          <NorthStarEditModal
            isOpen={northStarEditOpen}
            onClose={() => setNorthStarEditOpen(false)}
            onSave={handleNorthStarSave}
            currentNorthStar={northStar}
          />
          {studentProfile && (
            <ChangeSubjectsModal
              isOpen={changeSubjectsOpen}
              onClose={() => setChangeSubjectsOpen(false)}
              onSave={handleChangeSubjectsSave}
              currentProfile={studentProfile}
            />
          )}
        </>
      )}

      {/* Gamification overlays */}
      <RankUpModal
        isOpen={rankUpModal !== null}
        newRank={rankUpModal}
        onClose={() => setRankUpModal(null)}
      />
    </div>
    </SettingsContext.Provider>
  );
};

export default App;
