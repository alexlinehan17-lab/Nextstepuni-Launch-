
/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
*/

import React, { useState, useEffect, useRef, useCallback, useMemo, Suspense, lazy } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { Sun, Moon, LogOut, ArrowLeft, Settings, Flame, ChevronRight, ChevronLeft, Trophy, Award, Brain, Target, BookOpen, Shield, FlaskConical, BarChart3, Star, Home, Compass, Rocket, User, X } from 'lucide-react';
import { Library } from './components/Library';
import { KnowledgeTree, CategoryType } from './components/KnowledgeTree';
import { LoadingSpinner } from './components/LoadingSpinner';
import { Auth, SessionUser, getAvatarUrl } from './components/Auth';
import { AdminDashboard } from './components/AdminDashboard';
import { GCDashboard } from './components/GCDashboard';
import SettingsModal from './components/SettingsModal';
import StudyPassportModal from './components/StudyPassportModal';
import { auth, db } from './firebase';
import { onAuthStateChanged, signOut, User as FirebaseUser } from 'firebase/auth';
import { doc, getDoc, setDoc } from 'firebase/firestore';
import { ModuleProgress, UserProgress, UserSettings, NorthStar } from './types';
import { moduleComponents, InnovationZone } from './moduleRegistry';
import { ALL_COURSES, categoryTitles, SUBJECT_TO_MODULE } from './courseData';
import { useSettings } from './hooks/useSettings';
import { useStreak, StreakData } from './hooks/useStreak';
import { useMood } from './hooks/useMood';
import { useTodaysFocus, FocusRecommendation } from './hooks/useTodaysFocus';
import { usePoints } from './hooks/usePoints';
import DashboardView from './components/DashboardView';
import LearningPathsView from './components/LearningPathsView';
import { type StudentSubjectProfile } from './components/subjectData';
import NorthStarEditModal from './components/NorthStarEditModal';
import ChangeSubjectsModal from './components/ChangeSubjectsModal';

const Onboarding = lazy(() => import('./components/Onboarding'));

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
}

const UserProfile: React.FC<UserProfileProps> = ({ user, onLogout, settings, updateSetting, onOpenSettings, avatarOverride, streak, recommendation, onSelectModule, onOpenPassport, onGoToDashboard, completedCount, totalCount, onOpenNorthStar, hasNorthStar }) => {
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
      <button onClick={() => setIsOpen(!isOpen)} className="flex items-center gap-2">
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
                <div className="w-8 h-8 rounded-lg bg-[#CC785C]/10 flex items-center justify-center">
                  <BarChart3 size={16} className="text-[#CC785C]" />
                </div>
                <span className="text-sm font-medium text-zinc-700 dark:text-zinc-300 flex-1 text-left">My Progress</span>
              </button>
              <button
                onClick={() => { setIsOpen(false); onOpenPassport(); }}
                className="w-full flex items-center gap-3 p-2 rounded-lg hover:bg-zinc-100 dark:hover:bg-white/5"
              >
                <div className="w-8 h-8 rounded-lg bg-[#CC785C]/10 dark:bg-[#CC785C]/10 flex items-center justify-center">
                  <Award size={16} className="text-[#CC785C]" />
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
                  <span className="text-sm font-medium text-zinc-700 dark:text-zinc-300">Theme</span>
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
  onGoToDashboard: () => void;
  onGoToLearningPaths: () => void;
  onGoToInnovationZone: () => void;
  onOpenProfile: () => void;
}

const MobileBottomNav: React.FC<MobileBottomNavProps> = ({ viewState, onGoHome, onGoToDashboard, onGoToLearningPaths, onGoToInnovationZone, onOpenProfile }) => {
  const tabs = [
    { id: 'tree', label: 'Home', icon: Home, action: onGoHome },
    { id: 'dashboard', label: 'Dashboard', icon: BarChart3, action: onGoToDashboard },
    { id: 'learning-paths', label: 'Paths', icon: Compass, action: onGoToLearningPaths },
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
              className={`flex flex-col items-center justify-center gap-1 flex-1 h-full transition-colors ${isActive ? 'text-[#CC785C]' : 'text-zinc-400 dark:text-zinc-500'}`}
            >
              <tab.icon size={20} strokeWidth={isActive ? 2 : 1.5} />
              <span className="text-[10px] font-medium">{tab.label}</span>
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
  completedCount: number;
  totalCount: number;
  onOpenNorthStar: () => void;
  hasNorthStar: boolean;
  todayMood: string | null;
  onSetMood: (mood: string) => void;
}

const MOBILE_MOOD_OPTIONS = [
  { key: 'calm', label: 'Calm', emoji: '😌' },
  { key: 'balanced', label: 'Balanced', emoji: '⚖️' },
  { key: 'energized', label: 'Energized', emoji: '⚡' },
  { key: 'stressed', label: 'Stressed', emoji: '😰' },
];

const MobileProfileSheet: React.FC<MobileProfileSheetProps> = ({ isOpen, onClose, user, onLogout, settings, updateSetting, onOpenSettings, avatarOverride, streak, recommendation, onSelectModule, onOpenPassport, onGoToDashboard, completedCount, totalCount, onOpenNorthStar, hasNorthStar, todayMood, onSetMood }) => {
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

              {/* Mood Check-in */}
              <div className="mb-3">
                <p className="text-[10px] font-semibold uppercase tracking-widest text-zinc-400 dark:text-zinc-500 px-1 mb-2">How are you feeling?</p>
                <div className="flex gap-2">
                  {MOBILE_MOOD_OPTIONS.map(m => (
                    <button
                      key={m.key}
                      onClick={() => onSetMood(m.key)}
                      className={`flex-1 flex flex-col items-center gap-1 py-2.5 rounded-xl text-xs font-medium transition-colors ${
                        todayMood === m.key
                          ? 'bg-[#CC785C]/10 text-[#CC785C] ring-1 ring-[#CC785C]/30'
                          : 'bg-zinc-50 dark:bg-zinc-800/50 text-zinc-500 dark:text-zinc-400'
                      }`}
                    >
                      <span className="text-base">{m.emoji}</span>
                      {m.label}
                    </button>
                  ))}
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
                  <div className="w-8 h-8 rounded-lg bg-[#CC785C]/10 flex items-center justify-center"><Award size={16} className="text-[#CC785C]" /></div>
                  <span className="text-sm font-medium text-zinc-700 dark:text-zinc-300 flex-1 text-left">Study Passport</span>
                  <span className="text-xs font-bold text-zinc-400 dark:text-zinc-500">{completedCount}/{totalCount}</span>
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
                  <span className="text-sm font-medium text-zinc-700 dark:text-zinc-300 flex-1 text-left">Theme</span>
                </button>
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

const RESEARCH_PAPERS = [
  { title: 'Implicit Theories of Intelligence Predict Achievement Across an Adolescent Transition', authors: 'Blackwell, Trzesniewski & Dweck', year: 2007, journal: 'Child Development', description: 'Students who believed their intelligence could grow got better maths grades over two years, while "fixed mindset" students flatlined. Teaching students the brain can grow with effort actually reversed declining grades.' },
  { title: 'Distributed Practice in Verbal Recall Tasks: A Review and Quantitative Synthesis', authors: 'Cepeda, Pashler, Vul, Wixted & Rohrer', year: 2006, journal: 'Psychological Bulletin', description: 'After analysing 317 experiments, researchers confirmed that spreading study sessions over time beats cramming into one sitting for long-term memory. The optimal gap is roughly 10-20% of the time until your exam.' },
  { title: 'Test-Enhanced Learning: Taking Memory Tests Improves Long-Term Retention', authors: 'Roediger & Karpicke', year: 2006, journal: 'Psychological Science', description: 'Students who tested themselves on material remembered far more long-term than students who simply re-read. The act of pulling information out of memory — even without feedback — made it stick dramatically better.' },
  { title: 'Reducing the Racial Achievement Gap: A Social-Psychological Intervention', authors: 'Cohen, Garcia, Apfel & Master', year: 2006, journal: 'Science', description: 'Students who spent just 15 minutes writing about their most important personal values saw the achievement gap narrow by 40%. This brief exercise protected against stereotype threat and freed up mental energy for learning.' },
  { title: 'Neuroplasticity: Changes in Grey Matter Induced by Training', authors: 'Draganski, Gaser, Busch, Schuierer, Bogdahn & May', year: 2004, journal: 'Nature', description: 'People who learned to juggle showed visible growth in brain areas over three months — their grey matter physically expanded. One of the first studies to prove that learning literally changes the structure of the brain.' },
  { title: 'The Role of Deliberate Practice in the Acquisition of Expert Performance', authors: 'Ericsson, Krampe & Tesch-Romer', year: 1993, journal: 'Psychological Review', description: 'Elite violinists had accumulated roughly twice as many hours of focused practice as less accomplished players by age 20. What people call "natural talent" is largely the result of structured, goal-directed practice.' },
  { title: 'Enhancing Interest and Performance With a Utility Value Intervention', authors: 'Hulleman & Harackiewicz', year: 2009, journal: 'Journal of Educational Psychology', description: 'When students wrote short essays connecting schoolwork to their own lives, struggling students improved by nearly two-thirds of a letter grade. Making study feel personally relevant boosted both interest and performance.' },
  { title: 'Stereotype Threat and the Intellectual Test Performance of African Americans', authors: 'Steele & Aronson', year: 1995, journal: 'Journal of Personality and Social Psychology', description: 'When a test was framed as measuring ability, disadvantaged students performed worse. When the same test was framed as a simple exercise, the gap vanished — proving that pressure from stereotypes directly drags down performance.' },
];

const App: React.FC = () => {
  const [viewState, setViewState] = useState<'tree' | 'category' | 'module' | 'innovation-zone' | 'dashboard' | 'learning-paths' | 'onboarding'>('tree');
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
  const { settings, updateSetting, isLoaded: settingsLoaded } = useSettings(user?.uid, user?.avatar);
  const { streak } = useStreak(user?.uid);
  const { todayMood, setMood, entries: moodEntries } = useMood(user?.uid);
  const { recommendation } = useTodaysFocus(userProgress, ALL_COURSES);
  const pointsData = usePoints(user?.uid);

  const isPopstateRef = useRef(false);
  const researchScrollRef = useRef<HTMLDivElement>(null);

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
            });
            if (progressDoc.exists()) {
              const progressData = progressDoc.data();
              setUserProgress(progressData as UserProgress);
              if (progressData.cosmeticUnlocks?.avatarSeeds) {
                setUnlockedAvatarSeeds(progressData.cosmeticUnlocks.avatarSeeds);
              }
              if (progressData.northStar) {
                setNorthStar(progressData.northStar as NorthStar);
              }
              if (progressData.subjectProfile) {
                setStudentProfile(progressData.subjectProfile as StudentSubjectProfile);
              } else {
                setNeedsOnboarding(true);
              }
            } else {
              setUserProgress({});
              setNeedsOnboarding(true);
            }
          } else {
             // This can happen if user creation was interrupted. Log them out.
            await signOut(auth);
            setUser(null);
            setUserProgress({});
          }
        } catch (error) {
           console.error("Error fetching user data:", error);
           await signOut(auth);
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

    setUserProgress(prev => ({ ...prev, [moduleId]: newProgress }));

    try {
      const progressDocRef = doc(db, "progress", user.uid);
      await setDoc(progressDocRef, { [moduleId]: newProgress }, { merge: true });
    } catch (error) {
      console.error("Failed to save progress:", error);
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
        setNorthStar(northStarData);
      }
      await setDoc(progressDocRef, saveData, { merge: true });
    } catch (error) {
      console.error('Failed to save subject profile:', error);
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
    }
  };

  const handleBackToTree = () => {
    window.history.back();
  };

  const handleBackToCategory = () => {
    window.history.back();
  };

  const renderContent = () => {
    if (isLoadingAuth) {
        return <LoadingSpinner />;
    }

    if (!user) {
      return (
        <div className="relative min-h-screen flex flex-col">
          {/* ── Navbar ── */}
          <nav className="fixed top-0 left-0 right-0 h-16 z-[100] bg-zinc-50/80 dark:bg-zinc-950/80 backdrop-blur-xl border-b border-zinc-200/50 dark:border-white/[0.06]">
            <div className="max-w-6xl mx-auto h-full px-6 flex items-center justify-between">
              {/* Left: Logo */}
              <img src="/nextstepuni-logo.png" alt="Nextstepuni" className="h-10 w-auto" />
              {/* Right: Log in */}
              <Auth
                onLoginSuccess={handleLoginSuccess}
                buttonLabel="Log in"
                buttonClassName="px-5 py-2.5 text-sm font-medium bg-zinc-900 dark:bg-white text-white dark:text-zinc-900 rounded-full hover:bg-zinc-700 dark:hover:bg-zinc-200 transition-colors"
                showChevron
                initialStep="login"
              />
            </div>
          </nav>

          {/* ── Gradient blobs ── */}
          <div className="fixed inset-0 overflow-hidden pointer-events-none" aria-hidden="true">
            <div className="absolute top-[15%] right-[10%] w-[500px] h-[500px] rounded-full bg-[#CC785C]/[0.07] blur-[100px] animate-blob-1" />
            <div className="absolute bottom-[20%] left-[5%] w-[450px] h-[450px] rounded-full bg-yellow-300/[0.09] blur-[100px] animate-blob-2" />
            <div className="absolute top-[40%] left-[30%] w-[400px] h-[400px] rounded-full bg-orange-200/[0.08] blur-[120px] animate-blob-3" />
          </div>

          {/* ── Hero ── */}
          <div className="min-h-screen flex flex-col items-center justify-center text-center px-6 pt-16 relative z-10">
            <h1 className="font-serif text-3xl sm:text-5xl md:text-7xl text-zinc-900 dark:text-white tracking-tight leading-[1.08] font-semibold max-w-3xl">
              {"Science-backed strategies to give you an".split(' ').map((word, i, arr) => (
                <span key={i} className="inline-block overflow-hidden align-bottom pb-[0.15em] mb-[-0.15em]">
                  <motion.span
                    className="inline-block"
                    initial={{ y: '100%' }}
                    animate={{ y: 0 }}
                    transition={{ duration: 0.7, delay: i * 0.05, ease: [0.16, 1, 0.3, 1] }}
                  >{word}{i < arr.length - 1 ? '\u00A0' : ''}</motion.span>
                </span>
              ))}
              {' '}
              <span className="inline-block overflow-hidden align-bottom pb-[0.15em] mb-[-0.15em]">
                <motion.span
                  className="inline-block px-1"
                  initial={{ y: '100%' }}
                  animate={{ y: 0 }}
                  transition={{ duration: 0.7, delay: 0.3, ease: [0.16, 1, 0.3, 1] }}
                  style={{ backgroundImage: 'linear-gradient(to top, rgba(250, 204, 21, 0.45) 35%, transparent 35%)', boxDecorationBreak: 'clone', WebkitBoxDecorationBreak: 'clone' } as React.CSSProperties}
                >unfair advantage</motion.span>
              </span>
              {' '}
              {"in your exams.".split(' ').map((word, i, arr) => (
                <span key={i} className="inline-block overflow-hidden align-bottom pb-[0.15em] mb-[-0.15em]">
                  <motion.span
                    className="inline-block"
                    initial={{ y: '100%' }}
                    animate={{ y: 0 }}
                    transition={{ duration: 0.7, delay: 0.4 + i * 0.05, ease: [0.16, 1, 0.3, 1] }}
                  >{word}{i < arr.length - 1 ? '\u00A0' : ''}</motion.span>
                </span>
              ))}
            </h1>

            <motion.p
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.8, delay: 0.6, ease: [0.16, 1, 0.3, 1] }}
              className="mt-8 text-lg text-zinc-500 dark:text-zinc-400 max-w-xl leading-relaxed"
            >
              Master proven learning techniques used by top students. Build better study habits, retain more, and perform when it counts.
            </motion.p>

            <motion.div
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.8, delay: 0.75, ease: [0.16, 1, 0.3, 1] }}
              className="mt-12"
            >
              <Auth
                onLoginSuccess={handleLoginSuccess}
                buttonLabel="Start Learning"
                buttonClassName="px-8 py-3.5 text-base font-medium bg-[#CC785C] text-white rounded-full hover:bg-[#B56A50] transition-colors shadow-lg shadow-[#CC785C]/20"
                initialStep="create"
              />
            </motion.div>
          </div>

          {/* ── How It Works ── */}
          <div className="relative z-10 px-6 pb-24">
            <div className="max-w-5xl mx-auto">
              <motion.div
                initial={{ opacity: 0, y: 30 }}
                whileInView={{ opacity: 1, y: 0 }}
                viewport={{ once: true, margin: '-80px' }}
                transition={{ duration: 0.7, ease: [0.16, 1, 0.3, 1] }}
                className="text-center mb-16"
              >
                <p className="text-[11px] font-semibold uppercase tracking-[0.2em] text-[#CC785C] mb-3">How It Works</p>
                <h2 className="font-serif text-2xl sm:text-3xl md:text-4xl font-semibold text-zinc-900 dark:text-white">A complete system, not a collection of tips.</h2>
              </motion.div>

              <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-6">
                {[
                  { icon: Brain, title: 'Rewire Your Mindset', description: 'Build the psychological foundations that separate top students from the rest.', delay: 0 },
                  { icon: BookOpen, title: 'Learn How to Learn', description: 'Master active recall, spaced repetition, and other techniques backed by cognitive science.', delay: 0.1 },
                  { icon: Target, title: 'Optimise Your Strategy', description: 'Use grade economics, subject synergies, and marking scheme mechanics to maximise your points.', delay: 0.2 },
                  { icon: Shield, title: 'Perform Under Pressure', description: 'Develop exam-day protocols that protect your working memory when it matters most.', delay: 0.3 },
                ].map((pillar, i) => (
                  <motion.div
                    key={i}
                    initial={{ opacity: 0, y: 24 }}
                    whileInView={{ opacity: 1, y: 0 }}
                    viewport={{ once: true, margin: '-60px' }}
                    transition={{ duration: 0.6, delay: pillar.delay, ease: [0.16, 1, 0.3, 1] }}
                    className="group p-6 rounded-2xl bg-white/60 dark:bg-zinc-900/40 border border-zinc-200/60 dark:border-zinc-800/60 backdrop-blur-sm hover:border-zinc-300 dark:hover:border-zinc-700 transition-colors"
                  >
                    <div className="w-10 h-10 rounded-xl bg-zinc-100 dark:bg-zinc-800 flex items-center justify-center mb-4 group-hover:bg-[#CC785C]/10 transition-colors">
                      <pillar.icon size={20} className="text-zinc-500 dark:text-zinc-400 group-hover:text-[#CC785C] transition-colors" />
                    </div>
                    <h3 className="font-semibold text-zinc-900 dark:text-white text-sm mb-2">{pillar.title}</h3>
                    <p className="text-xs text-zinc-500 dark:text-zinc-400 leading-relaxed">{pillar.description}</p>
                  </motion.div>
                ))}
              </div>

              {/* ── Stats row ── */}
              <div className="mt-16 grid grid-cols-1 sm:grid-cols-3 gap-4 sm:gap-6">
                {[
                  { value: '43', label: 'Interactive Modules', accent: 'from-[#CC785C]/20 to-[#CC785C]/5', border: 'border-[#CC785C]/20', textColor: 'text-[#CC785C]' },
                  { value: '7', label: 'Research-Backed Categories', accent: 'from-amber-400/20 to-amber-400/5', border: 'border-amber-400/20', textColor: 'text-amber-500 dark:text-amber-400' },
                  { value: '250+', label: 'Activities & Exercises', accent: 'from-emerald-400/20 to-emerald-400/5', border: 'border-emerald-400/20', textColor: 'text-emerald-600 dark:text-emerald-400' },
                ].map((stat, i) => (
                  <motion.div
                    key={i}
                    initial={{ opacity: 0, y: 20 }}
                    whileInView={{ opacity: 1, y: 0 }}
                    viewport={{ once: true, margin: '-60px' }}
                    transition={{ duration: 0.6, delay: i * 0.1, ease: [0.16, 1, 0.3, 1] }}
                    className={`relative overflow-hidden rounded-2xl border ${stat.border} bg-gradient-to-br ${stat.accent} backdrop-blur-sm p-8 text-center`}
                  >
                    <div className="absolute inset-0 bg-white/40 dark:bg-zinc-900/40" />
                    <div className="relative">
                      <p className={`text-4xl sm:text-5xl font-bold font-mono ${stat.textColor}`}>{stat.value}</p>
                      <p className="text-xs font-medium text-zinc-500 dark:text-zinc-400 mt-2 tracking-wide uppercase">{stat.label}</p>
                    </div>
                  </motion.div>
                ))}
              </div>
            </div>
          </div>

          {/* ── Recent Research ── */}
          <div className="relative z-10 px-6 pt-8 pb-20">
            <div className="max-w-5xl mx-auto">
              <motion.div
                initial={{ opacity: 0, y: 30 }}
                whileInView={{ opacity: 1, y: 0 }}
                viewport={{ once: true, margin: '-80px' }}
                transition={{ duration: 0.7, ease: [0.16, 1, 0.3, 1] }}
                className="flex items-end justify-between mb-10"
              >
                <div>
                  <p className="text-[11px] font-semibold uppercase tracking-[0.2em] text-[#CC785C] mb-3">The Evidence</p>
                  <h2 className="font-serif text-2xl sm:text-3xl md:text-4xl font-semibold text-zinc-900 dark:text-white">Built on real research.</h2>
                </div>
                <div className="hidden sm:flex items-center gap-2">
                  <button onClick={() => { if (researchScrollRef.current) researchScrollRef.current.scrollBy({ left: -researchScrollRef.current.offsetWidth * 0.75, behavior: 'smooth' }); }} className="w-10 h-10 rounded-full border border-zinc-200 dark:border-zinc-700 flex items-center justify-center text-zinc-500 dark:text-zinc-400 hover:bg-zinc-100 dark:hover:bg-zinc-800 transition-colors">
                    <ChevronLeft size={18} />
                  </button>
                  <button onClick={() => { if (researchScrollRef.current) researchScrollRef.current.scrollBy({ left: researchScrollRef.current.offsetWidth * 0.75, behavior: 'smooth' }); }} className="w-10 h-10 rounded-full border border-zinc-200 dark:border-zinc-700 flex items-center justify-center text-zinc-500 dark:text-zinc-400 hover:bg-zinc-100 dark:hover:bg-zinc-800 transition-colors">
                    <ChevronRight size={18} />
                  </button>
                </div>
              </motion.div>

              <div ref={researchScrollRef} className="flex gap-5 overflow-x-auto pb-4 snap-x snap-mandatory scrollbar-hide" style={{ scrollbarWidth: 'none', msOverflowStyle: 'none' }}>
                {RESEARCH_PAPERS.map((paper, i) => (
                  <motion.div
                    key={i}
                    initial={{ opacity: 0, y: 20 }}
                    whileInView={{ opacity: 1, y: 0 }}
                    viewport={{ once: true, margin: '-40px' }}
                    transition={{ duration: 0.5, delay: i * 0.05, ease: [0.16, 1, 0.3, 1] }}
                    className="snap-start shrink-0 w-[320px] sm:w-[360px] flex flex-col justify-between p-6 rounded-2xl bg-white/60 dark:bg-zinc-900/40 border border-zinc-200/60 dark:border-zinc-800/60 backdrop-blur-sm"
                  >
                    <div>
                      <p className="text-[10px] font-semibold uppercase tracking-wider text-zinc-400 dark:text-zinc-500 mb-3">{paper.journal} ({paper.year})</p>
                      <h3 className="font-serif text-base font-semibold text-zinc-900 dark:text-white leading-snug mb-3">{paper.title}</h3>
                      <p className="text-xs text-zinc-500 dark:text-zinc-400 leading-relaxed">{paper.description}</p>
                    </div>
                    <p className="text-[10px] text-zinc-400 dark:text-zinc-500 mt-5 pt-4 border-t border-zinc-100 dark:border-zinc-800">{paper.authors}</p>
                  </motion.div>
                ))}
              </div>

              <motion.div
                initial={{ opacity: 0 }}
                whileInView={{ opacity: 1 }}
                viewport={{ once: true }}
                transition={{ duration: 0.8, delay: 0.3 }}
                className="mt-10 flex items-center justify-center gap-3"
              >
                <FlaskConical size={14} className="text-[#CC785C]" />
                <p className="text-sm text-zinc-500 dark:text-zinc-400">Every module is grounded in peer-reviewed research from journals like <span className="font-medium text-zinc-700 dark:text-zinc-300">Nature</span>, <span className="font-medium text-zinc-700 dark:text-zinc-300">Science</span>, and <span className="font-medium text-zinc-700 dark:text-zinc-300">Psychological Review</span>.</p>
              </motion.div>
            </div>
          </div>

          {/* ── PwC Collaboration ── */}
          <div className="relative z-10 pb-10 pt-6 flex items-center justify-center gap-3">
            <div className="w-8 h-px bg-zinc-300 dark:bg-zinc-700" />
            <p className="text-xs text-zinc-400 dark:text-zinc-500 tracking-wide">A Nextstepuni / PwC Collaboration</p>
            <div className="w-8 h-px bg-zinc-300 dark:bg-zinc-700" />
          </div>

          {/* ── DEV: Skip Login ── */}
          <button
            onClick={() => handleLoginSuccess({ uid: 'dev-student', name: 'Dev User', avatar: 'Casper', isAdmin: false })}
            className="fixed bottom-4 left-4 z-50 px-3 py-1 bg-red-600/20 text-red-400 border border-red-600/30 rounded-full text-xs font-mono hover:bg-red-600/40"
          >
            DEV: Skip Login
          </button>
        </div>
      );
    }

    if (user.isAdmin) {
      return <AdminDashboard allCourses={ALL_COURSES} onLogout={handleLogout} />;
    }

    if (user.role === 'gc' && user.school) {
      return <GCDashboard school={user.school} onLogout={handleLogout} allCourses={ALL_COURSES} />;
    }

    if (viewState === 'dashboard') {
      return (
        <DashboardView
          userProgress={userProgress}
          allCourses={studentCourses}
          categoryTitles={categoryTitles}
          streak={streak}
          recommendation={recommendation}
          moodEntries={moodEntries}
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

    if (viewState === 'tree') {
      return <KnowledgeTree
        key="knowledge-tree"
        onSelectCategory={handleSelectCategory}
        onGoToInnovationZone={handleGoToInnovationZone}
        onGoToDashboard={handleGoToDashboard}
        onGoToLearningPaths={handleGoToLearningPaths}
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
        completedCount={completedCount}
        totalCount={studentCourses.length}
        todayMood={todayMood}
        onSetMood={setMood}
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
        />
      );
    }

    if (viewState === 'innovation-zone') {
        return (
          <Suspense fallback={<LoadingSpinner />}>
            <InnovationZone onBack={handleBackToTree} onSelectModule={handleSelectModule} user={user} autoOpenJourney={cameFromJourney} savedJourneyResult={journeyResult} onJourneyComplete={setJourneyResult} />
          </Suspense>
        );
    }

    if (viewState === 'module' && currentModuleId) {
      const ModuleComponent = moduleComponents[currentModuleId];
      if (ModuleComponent) {
        return (
          <Suspense fallback={<LoadingSpinner />}>
            {cameFromJourney && (
              <div className="fixed top-0 left-0 right-0 z-[80] bg-[#CC785C] dark:bg-[#CC785C]">
                <button
                  onClick={handleBackToCategory}
                  className="w-full flex items-center justify-center gap-2 py-2 text-white text-xs font-bold hover:bg-[#B56A50] dark:hover:bg-[#B56A50] transition-colors"
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
        );
      }
      return null;
    }

    return null;
  };

  return (
    <div className="min-h-screen bg-zinc-50 dark:bg-zinc-950 transition-colors duration-500">
      {user && viewState !== 'onboarding' && user.role !== 'gc' && !user.isAdmin && (
        <div className={`fixed top-6 right-6 z-[100] ${viewState === 'tree' ? 'hidden' : 'hidden md:block'}`}>
          <UserProfile user={user} onLogout={handleLogout} settings={settings} updateSetting={updateSetting} onOpenSettings={() => setSettingsOpen(true)} avatarOverride={settings.avatar} streak={streak} recommendation={recommendation} onSelectModule={handleSelectModule} onOpenPassport={() => setPassportOpen(true)} onGoToDashboard={handleGoToDashboard} completedCount={completedCount} totalCount={studentCourses.length} onOpenNorthStar={() => setNorthStarEditOpen(true)} hasNorthStar={northStar !== null} />
        </div>
      )}

      {renderContent()}

      {user && viewState !== 'onboarding' && viewState !== 'module' && !user.isAdmin && user.role !== 'gc' && (
        <MobileBottomNav
          viewState={viewState}
          onGoHome={handleGoHome}
          onGoToDashboard={handleGoToDashboard}
          onGoToLearningPaths={handleGoToLearningPaths}
          onGoToInnovationZone={handleGoToInnovationZone}
          onOpenProfile={() => setMobileProfileOpen(true)}
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
          completedCount={completedCount}
          totalCount={studentCourses.length}
          onOpenNorthStar={() => setNorthStarEditOpen(true)}
          hasNorthStar={northStar !== null}
          todayMood={todayMood}
          onSetMood={setMood}
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
    </div>
  );
};

export default App;
