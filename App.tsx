
/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
*/

import React, { useState, useEffect, Suspense } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { Sun, Moon, LogOut, ArrowLeft } from 'lucide-react';
import { Library } from './components/Library';
import { KnowledgeTree, CategoryType } from './components/KnowledgeTree';
import { LoadingSpinner } from './components/LoadingSpinner';
import { Auth, SessionUser, getAvatarUrl } from './components/Auth';
import { AdminDashboard } from './components/AdminDashboard';
import { auth, db } from './firebase';
import { onAuthStateChanged, signOut, User as FirebaseUser } from 'firebase/auth';
import { doc, getDoc, setDoc } from 'firebase/firestore';
import { ModuleProgress, UserProgress } from './types';
import { moduleComponents, InnovationZone } from './moduleRegistry';
import { ALL_COURSES, categoryTitles } from './courseData';

const UserProfile = ({ user, onLogout, darkMode, setDarkMode }: { user: SessionUser, onLogout: () => void, darkMode: boolean, setDarkMode: (v: boolean) => void }) => {
  const [isOpen, setIsOpen] = useState(false);
  return (
    <div className="relative">
      <button onClick={() => setIsOpen(!isOpen)} className="flex items-center gap-2">
        <img src={getAvatarUrl(user.avatar)} alt="User Avatar" className="w-10 h-10 rounded-full bg-zinc-200" />
      </button>
      <AnimatePresence>
        {isOpen && (
          <motion.div
            initial={{ opacity: 0, y: -10, scale: 0.95 }}
            animate={{ opacity: 1, y: 0, scale: 1 }}
            exit={{ opacity: 0, y: -10, scale: 0.95 }}
            className="absolute top-full right-0 mt-2 w-64 bg-white dark:bg-zinc-900 border border-zinc-200 dark:border-zinc-800 rounded-xl shadow-lg p-4"
          >
            <div className="flex items-center gap-3 border-b border-zinc-200/50 dark:border-white/10 pb-3 mb-3">
              <img src={getAvatarUrl(user.avatar)} alt="User Avatar" className="w-12 h-12 rounded-full bg-zinc-200" />
              <div>
                <p className="font-bold text-zinc-800 dark:text-white">{user.name}</p>
                <p className="text-xs text-zinc-500">{user.isAdmin ? 'Admin' : 'Student'}</p>
              </div>
            </div>

            <button onClick={() => setDarkMode(!darkMode)} className="w-full flex items-center justify-between p-2 rounded-lg hover:bg-zinc-100 dark:hover:bg-white/5">
                <span className="text-sm font-medium text-zinc-700 dark:text-zinc-300">Theme</span>
                 <AnimatePresence mode="wait">
                    {darkMode ? (
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
            <button onClick={onLogout} className="w-full flex items-center gap-2 p-2 rounded-lg hover:bg-zinc-100 dark:hover:bg-white/5 mt-1">
              <LogOut size={16} className="text-rose-500" />
              <span className="text-sm font-medium text-rose-500">Log Out</span>
            </button>
          </motion.div>
        )}
      </AnimatePresence>
    </div>
  )
}

const App: React.FC = () => {
  const [viewState, setViewState] = useState<'tree' | 'category' | 'module' | 'innovation-zone'>('tree');
  const [currentCategory, setCurrentCategory] = useState<CategoryType | null>(null);
  const [currentModuleId, setCurrentModuleId] = useState<string | null>(null);
  const [cameFromJourney, setCameFromJourney] = useState(false);
  const [journeyResult, setJourneyResult] = useState<{ endingId: string; finalStats?: any } | null>(null);
  const [darkMode, setDarkMode] = useState(false);
  const [user, setUser] = useState<SessionUser | null>(null);
  const [userProgress, setUserProgress] = useState<UserProgress>({});
  const [isLoadingAuth, setIsLoadingAuth] = useState(true);

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
              setUserProgress(progressDoc.data() as UserProgress);
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

  // Sync dark mode state with document class
  useEffect(() => {
    if (darkMode) {
      document.documentElement.classList.add('dark');
    } else {
      document.documentElement.classList.remove('dark');
    }
  }, [darkMode]);

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
          <div className="flex-1 flex flex-col items-center justify-center text-center px-6 pt-16 relative z-10">
            <h1 className="font-serif text-5xl md:text-7xl text-zinc-900 dark:text-white tracking-tight leading-[1.08] font-semibold max-w-3xl">
              {[
                { text: 'Science-backed', delay: 0 },
                { text: 'strategies', delay: 0.05 },
                { text: 'to', delay: 0.1 },
                { text: 'give', delay: 0.15 },
                { text: 'you', delay: 0.2 },
                { text: 'an', delay: 0.25 },
              ].map((w, i) => (
                <span key={i} className="inline-block overflow-hidden align-bottom pb-[0.15em] mb-[-0.15em]">
                  <motion.span
                    className="inline-block"
                    initial={{ y: '100%' }}
                    animate={{ y: 0 }}
                    transition={{ duration: 0.7, delay: w.delay, ease: [0.16, 1, 0.3, 1] }}
                  >{w.text}</motion.span>
                </span>
              )).reduce<React.ReactNode[]>((acc, el, i) => i === 0 ? [el] : [...acc, ' ', el], [])}
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
              {[
                { text: 'in', delay: 0.4 },
                { text: 'your', delay: 0.45 },
                { text: 'exams.', delay: 0.5 },
              ].map((w, i) => (
                <span key={i} className="inline-block overflow-hidden align-bottom pb-[0.15em] mb-[-0.15em]">
                  <motion.span
                    className="inline-block"
                    initial={{ y: '100%' }}
                    animate={{ y: 0 }}
                    transition={{ duration: 0.7, delay: w.delay, ease: [0.16, 1, 0.3, 1] }}
                  >{w.text}</motion.span>
                </span>
              )).reduce<React.ReactNode[]>((acc, el, i) => i === 0 ? [el] : [...acc, ' ', el], [])}
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

          {/* ── PwC Collaboration ── */}
          <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            transition={{ duration: 0.8, delay: 0.5 }}
            className="pb-10 pt-6 flex items-center justify-center gap-3"
          >
            <div className="w-8 h-px bg-zinc-300 dark:bg-zinc-700" />
            <p className="text-xs text-zinc-400 dark:text-zinc-500 tracking-wide">A Nextstepuni / PwC Collaboration</p>
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
          <UserProfile user={user} onLogout={handleLogout} darkMode={darkMode} setDarkMode={setDarkMode} />
        </div>
      )}

      {renderContent()}
    </div>
  );
};

export default App;
