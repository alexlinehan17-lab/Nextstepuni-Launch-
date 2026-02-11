
/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
*/

import React, { useState, useEffect, Suspense } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { Sun, Moon, LogOut, ArrowLeft, Settings, Flame, ChevronRight, Trophy, Waves, Scale, Zap, CloudRain, Award } from 'lucide-react';
import { useTranslation } from 'react-i18next';
import './i18n';
import { Library } from './components/Library';
import { KnowledgeTree, CategoryType } from './components/KnowledgeTree';
import { LoadingSpinner } from './components/LoadingSpinner';
import { Auth, SessionUser, getAvatarUrl } from './components/Auth';
import { AdminDashboard } from './components/AdminDashboard';
import SettingsModal from './components/SettingsModal';
import StudyPassportModal from './components/StudyPassportModal';
import { auth, db } from './firebase';
import { onAuthStateChanged, signOut, User as FirebaseUser } from 'firebase/auth';
import { doc, getDoc, setDoc } from 'firebase/firestore';
import { ModuleProgress, UserProgress, UserSettings } from './types';
import { moduleComponents, InnovationZone } from './moduleRegistry';
import { ALL_COURSES, categoryTitles } from './courseData';
import { useSettings } from './hooks/useSettings';
import { useStreak, StreakData } from './hooks/useStreak';
import { useMood } from './hooks/useMood';
import { useTodaysFocus, FocusRecommendation } from './hooks/useTodaysFocus';

const MOOD_OPTIONS = [
  { key: 'calm', icon: Waves, label: 'Calm' },
  { key: 'balanced', icon: Scale, label: 'Balanced' },
  { key: 'energized', icon: Zap, label: 'Energized' },
  { key: 'stressed', icon: CloudRain, label: 'Stressed' },
] as const;

interface UserProfileProps {
  user: SessionUser;
  onLogout: () => void;
  settings: UserSettings;
  updateSetting: <K extends keyof UserSettings>(key: K, value: UserSettings[K]) => void;
  onOpenSettings: () => void;
  avatarOverride: string;
  streak: StreakData;
  todayMood: string | null;
  onSetMood: (mood: string) => void;
  recommendation: FocusRecommendation | null;
  onSelectModule: (moduleId: string) => void;
  onOpenPassport: () => void;
  completedCount: number;
  totalCount: number;
}

const UserProfile: React.FC<UserProfileProps> = ({ user, onLogout, settings, updateSetting, onOpenSettings, avatarOverride, streak, todayMood, onSetMood, recommendation, onSelectModule, onOpenPassport, completedCount, totalCount }) => {
  const { t } = useTranslation();
  const [isOpen, setIsOpen] = useState(false);
  const displayAvatar = avatarOverride || user.avatar;
  return (
    <div className="relative">
      <button onClick={() => setIsOpen(!isOpen)} className="flex items-center gap-2">
        <img src={getAvatarUrl(displayAvatar)} alt="User Avatar" className="w-10 h-10 rounded-full bg-zinc-200" />
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
                <p className="text-xs text-zinc-500">{user.isAdmin ? t('profile.admin') : t('profile.student')}</p>
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

            {/* Mood Check-in */}
            <div className="border-t border-zinc-200/50 dark:border-white/10 pt-3 mt-2 mb-2">
              <p className="text-[10px] font-semibold uppercase tracking-widest text-zinc-400 dark:text-zinc-500 px-2 mb-2">How are you feeling?</p>
              <div className="flex items-center justify-center gap-2 px-2">
                {MOOD_OPTIONS.map(({ key, icon: Icon, label }) => (
                  <button
                    key={key}
                    onClick={() => onSetMood(key)}
                    title={label}
                    className={`w-9 h-9 rounded-full flex items-center justify-center transition-all ${
                      todayMood === key
                        ? 'text-[#CC785C] bg-[#CC785C]/10 ring-2 ring-[#CC785C]'
                        : 'text-zinc-400 dark:text-zinc-500 hover:bg-zinc-100 dark:hover:bg-white/5'
                    }`}
                  >
                    <Icon size={16} />
                  </button>
                ))}
              </div>
            </div>

            {/* Study Passport */}
            <div className="border-t border-zinc-200/50 dark:border-white/10 pt-2 mt-2 mb-2">
              <button
                onClick={() => { setIsOpen(false); onOpenPassport(); }}
                className="w-full flex items-center gap-3 p-2 rounded-lg hover:bg-zinc-100 dark:hover:bg-white/5"
              >
                <div className="w-8 h-8 rounded-lg bg-purple-50 dark:bg-purple-500/10 flex items-center justify-center">
                  <Award size={16} className="text-purple-500" />
                </div>
                <span className="text-sm font-medium text-zinc-700 dark:text-zinc-300 flex-1 text-left">Study Passport</span>
                <span className="text-xs font-bold text-zinc-400 dark:text-zinc-500">{completedCount}/{totalCount}</span>
              </button>
            </div>

            {/* Existing: Theme, Settings, Log Out */}
            <div className="border-t border-zinc-200/50 dark:border-white/10 pt-2 mt-2">
              <button onClick={() => updateSetting('darkMode', !settings.darkMode)} className="w-full flex items-center justify-between p-2 rounded-lg hover:bg-zinc-100 dark:hover:bg-white/5">
                  <span className="text-sm font-medium text-zinc-700 dark:text-zinc-300">{t('profile.theme')}</span>
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
                <span className="text-sm font-medium text-zinc-700 dark:text-zinc-300">{t('profile.settings')}</span>
              </button>
              <button onClick={onLogout} className="w-full flex items-center gap-2 p-2 rounded-lg hover:bg-zinc-100 dark:hover:bg-white/5 mt-1">
                <LogOut size={16} className="text-rose-500" />
                <span className="text-sm font-medium text-rose-500">{t('profile.logout')}</span>
              </button>
            </div>
          </motion.div>
        )}
      </AnimatePresence>
    </div>
  )
}

const App: React.FC = () => {
  const { t } = useTranslation();
  const [viewState, setViewState] = useState<'tree' | 'category' | 'module' | 'innovation-zone'>('tree');
  const [currentCategory, setCurrentCategory] = useState<CategoryType | null>(null);
  const [currentModuleId, setCurrentModuleId] = useState<string | null>(null);
  const [cameFromJourney, setCameFromJourney] = useState(false);
  const [journeyResult, setJourneyResult] = useState<{ endingId: string; finalStats?: any } | null>(null);
  const [user, setUser] = useState<SessionUser | null>(null);
  const [userProgress, setUserProgress] = useState<UserProgress>({});
  const [isLoadingAuth, setIsLoadingAuth] = useState(true);
  const [settingsOpen, setSettingsOpen] = useState(false);
  const [passportOpen, setPassportOpen] = useState(false);
  const [unlockedAvatarSeeds, setUnlockedAvatarSeeds] = useState<string[]>([]);
  const { settings, updateSetting, isLoaded: settingsLoaded } = useSettings(user?.uid, user?.avatar);
  const { streak } = useStreak(user?.uid);
  const { todayMood, setMood } = useMood(user?.uid);
  const { recommendation } = useTodaysFocus(userProgress, ALL_COURSES);

  const completedCount = ALL_COURSES.filter(c => {
    const p = userProgress[c.id];
    return p && p.unlockedSection >= c.sectionsCount - 1;
  }).length;

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
            setUser({
              uid: firebaseUser.uid,
              name: userData.name,
              avatar: userData.avatar,
              isAdmin: false,
            });
            if (progressDoc.exists()) {
              const progressData = progressDoc.data();
              setUserProgress(progressData as UserProgress);
              if (progressData.cosmeticUnlocks?.avatarSeeds) {
                setUnlockedAvatarSeeds(progressData.cosmeticUnlocks.avatarSeeds);
              }
            } else {
              setUserProgress({});
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

    const updatedProgress = {
      ...userProgress,
      [moduleId]: newProgress
    };
    setUserProgress(updatedProgress); // Optimistic UI update

    try {
      const progressDocRef = doc(db, "progress", user.uid);
      await setDoc(progressDocRef, updatedProgress, { merge: true });
    } catch (error) {
      console.error("Failed to save progress:", error);
    }
  };

  const handleSelectCategory = (category: CategoryType) => {
    setCurrentCategory(category);
    setViewState('category');
  };

  const handleSelectModule = (moduleId: string) => {
    setCameFromJourney(viewState === 'innovation-zone');
    setCurrentModuleId(moduleId);
    setViewState('module');
  };

  const handleGoToInnovationZone = () => {
    setViewState('innovation-zone');
  };

  const handleBackToTree = () => {
    setCurrentCategory(null);
    setCameFromJourney(false);
    setViewState('tree');
  };

  const handleBackToCategory = () => {
    setCurrentModuleId(null);
    if (cameFromJourney) {
      setViewState('innovation-zone');
    } else if (currentCategory) {
      setViewState('category');
    } else {
      setViewState('tree');
    }
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
                buttonLabel={t('nav.login')}
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
          <div className="flex-1 flex flex-col items-center justify-center text-center px-6 pt-16 relative z-10">
            <h1 className="font-serif text-5xl md:text-7xl text-zinc-900 dark:text-white tracking-tight leading-[1.08] font-semibold max-w-3xl">
              {t('hero.title1').split(' ').map((word, i, arr) => (
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
                >{t('hero.highlight')}</motion.span>
              </span>
              {' '}
              {t('hero.title2').split(' ').map((word, i, arr) => (
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
              {t('hero.subtitle')}
            </motion.p>

            <motion.div
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.8, delay: 0.75, ease: [0.16, 1, 0.3, 1] }}
              className="mt-12"
            >
              <Auth
                onLoginSuccess={handleLoginSuccess}
                buttonLabel={t('nav.startLearning')}
                buttonClassName="px-8 py-3.5 text-base font-medium bg-[#CC785C] text-white rounded-full hover:bg-[#B56A50] transition-colors shadow-lg shadow-[#CC785C]/20"
                initialStep="create"
              />
            </motion.div>
          </div>

          {/* ── PwC Collaboration ── */}
          <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            transition={{ duration: 0.8, delay: 0.5 }}
            className="pb-10 pt-6 flex items-center justify-center gap-3"
          >
            <div className="w-8 h-px bg-zinc-300 dark:bg-zinc-700" />
            <p className="text-xs text-zinc-400 dark:text-zinc-500 tracking-wide">{t('hero.collab')}</p>
            <div className="w-8 h-px bg-zinc-300 dark:bg-zinc-700" />
          </motion.div>

          {/* ── DEV: Skip Login ── */}
          <button
            onClick={() => handleLoginSuccess({ uid: 'dev-student', name: 'Dev User', avatar: 'Casper', isAdmin: false })}
            className="fixed bottom-4 left-4 px-3 py-1 bg-red-600/20 text-red-400 border border-red-600/30 rounded-full text-xs font-mono hover:bg-red-600/40"
          >
            DEV: Skip Login
          </button>
        </div>
      );
    }

    if (user.isAdmin) {
      return <AdminDashboard allCourses={ALL_COURSES} />;
    }

    if (viewState === 'tree') {
      return <KnowledgeTree
        onSelectCategory={handleSelectCategory}
        onGoToInnovationZone={handleGoToInnovationZone}
        allCourses={ALL_COURSES}
        onSelectModule={handleSelectModule}
        categoryTitles={categoryTitles}
        userProgress={userProgress}
      />;
    }

    if (viewState === 'category' && currentCategory) {
      const categoryCourses = ALL_COURSES.filter(c => c.category === currentCategory);
      return (
        <Library
          title={categoryTitles[currentCategory]}
          courses={categoryCourses}
          onSelectCourse={handleSelectModule}
          onBack={handleBackToTree}
          userProgress={userProgress}
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
              <div className="fixed top-0 left-0 right-0 z-[80] bg-purple-600 dark:bg-purple-500">
                <button
                  onClick={handleBackToCategory}
                  className="w-full flex items-center justify-center gap-2 py-2 text-white text-xs font-bold hover:bg-purple-700 dark:hover:bg-purple-600 transition-colors"
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
      {user && (
        <div className="fixed top-6 right-6 z-[100]">
          <UserProfile user={user} onLogout={handleLogout} settings={settings} updateSetting={updateSetting} onOpenSettings={() => setSettingsOpen(true)} avatarOverride={settings.avatar} streak={streak} todayMood={todayMood} onSetMood={setMood} recommendation={recommendation} onSelectModule={handleSelectModule} onOpenPassport={() => setPassportOpen(true)} completedCount={completedCount} totalCount={ALL_COURSES.length} />
        </div>
      )}

      {renderContent()}

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
            allCourses={ALL_COURSES}
            categoryTitles={categoryTitles}
          />
        </>
      )}
    </div>
  );
};

export default App;
