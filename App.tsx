
/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
*/

import React, { useState, useEffect, useRef, useCallback, useMemo } from 'react';
import { Home, Rocket, Dumbbell, Timer, Mountain, User } from 'lucide-react';
import { UserProfile, MobileProfileSheet } from './components/UserProfileMenu';
import { type CategoryType } from './components/KnowledgeTree';
import AppRouter from './components/AppRouter';
import OfflineBanner from './components/OfflineBanner';
import SettingsModal from './components/SettingsModal';
import StudyPassportModal from './components/StudyPassportModal';
import { db } from './firebase';
import { doc, getDoc, setDoc, increment } from 'firebase/firestore';
import { type ModuleProgress, type NorthStar } from './types';
import { useToast } from './components/Toast';
import { ALL_COURSES, categoryTitles, SUBJECT_TO_MODULE } from './courseData';
import { useSettings } from './hooks/useSettings';
import { useTodaysFocus } from './hooks/useTodaysFocus';
import { useStrategyMastery } from './hooks/useStrategyMastery';
import { useWeeklyChallenge } from './hooks/useWeeklyChallenge';
import { useRecommendation } from './hooks/useRecommendation';
import { useQuests } from './hooks/useQuests';
import TrainingPulse from './components/TrainingPulse';
import AchievementToast from './components/AchievementToast';
import RankUpModal from './components/RankUpModal';
import StreakCelebration from './components/StreakCelebration';
import { useGamification } from './hooks/useGamification';
import { createStarterState } from './hooks/useIslandShop';
import { findBestLandPlacement } from './components/journey/hex/hexGeometry';
import { type IslandState } from './types';
import { type AthleteRank, type AchievementDefinition } from './gamificationConfig';
import { type StudentSubjectProfile } from './components/subjectData';
import NorthStarEditModal from './components/NorthStarEditModal';
import ChangeSubjectsModal from './components/ChangeSubjectsModal';
import NotificationBell from './components/NotificationBell';
import { POINTS, isModuleJustCompleted, isCategoryJustCompleted } from './journeyPointsConfig';
import { SettingsContext } from './contexts/SettingsContext';
import { useAuth } from './contexts/AuthContext';
import { useNavigation } from './contexts/NavigationContext';
import { useProgress } from './contexts/ProgressContext';

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

/* LoginPage extracted to components/LoginPage.tsx */

// ─── Remaining inline components ────────────────────────────

const _LoginPageRemoved = null; // placeholder to keep line references stable
if (_LoginPageRemoved) { /* never reached */ }

/* The following components (UserProfile, MobileProfileSheet, etc.) remain inline */

// ─── UserProfile component starts here ──────────────────────

// NOTE: The old LoginPage was here (530 lines). It's now at components/LoginPage.tsx

// (LoginPage code removed — now in components/LoginPage.tsx)
// The next component below is the inline UserProfile.

const App: React.FC = () => {
  const { showToast } = useToast();
  const nav = useNavigation();
  const { viewState, currentCategory, currentModuleId: _currentModuleId, cameFromJourney: _cameFromJourney } = nav.state;
  const [journeyResult, setJourneyResult] = useState<{ endingId: string; finalStats?: any } | null>(null);
  const { user, isLoadingAuth, authResolved, needsOnboarding: _authNeedsOnboarding, loadedData, handleLoginSuccess: _handleLoginSuccess, handleLogout } = useAuth();
  const [needsOnboarding, setNeedsOnboarding] = useState(false);

  // Progress state from context
  const progress = useProgress();
  const {
    userProgress, setUserProgress,
    studentProfile, setStudentProfile,
    northStar, setNorthStar,
    timetableCompletions, setTimetableCompletions: _setTimetableCompletions,
    pointsData, streak,
    unlockedAvatarSeeds, setUnlockedAvatarSeeds,
    unlockedThemes, setUnlockedThemes,
    unlockedCardStyles, setUnlockedCardStyles,
    dismissedGuides, setDismissedGuides,
    progressLoaded,
  } = progress;

  // Sync needsOnboarding from auth
  useEffect(() => {
    if (!isLoadingAuth) {
      setNeedsOnboarding(loadedData.needsOnboarding);
    }
  }, [isLoadingAuth, loadedData.needsOnboarding]);
  const [settingsOpen, setSettingsOpen] = useState(false);
  const [passportOpen, setPassportOpen] = useState(false);
  const [northStarEditOpen, setNorthStarEditOpen] = useState(false);
  const [changeSubjectsOpen, setChangeSubjectsOpen] = useState(false);
  const [mobileProfileOpen, setMobileProfileOpen] = useState(false);
  const [timetableBlockContext, setTimetableBlockContext] = useState<{ subject: string; sessionType: 'new-learning' | 'practice' | 'revision'; durationMinutes: number; dateKey: string; blockId: string } | null>(null);
  const [unreadNotificationCount, setUnreadNotificationCount] = useState(0);
  const { settings, updateSetting, isLoaded: _settingsLoaded } = useSettings(user?.uid, user?.avatar);
  const { recommendation } = useTodaysFocus(userProgress, ALL_COURSES);

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
  const [streakCelebration, setStreakCelebration] = useState<number | null>(null);
  const lastStreakRef = useRef(0);

  // Process toast queue
  useEffect(() => {
    if (currentToast || isBonusFlashToast) return;
    if (toastQueue.length === 0) return;
    const next = toastQueue[0];
    setToastQueue(q => q.slice(1));
    if (next === 'bonus-flash') {
      setIsBonusFlashToast(true);
    } else {
      setCurrentToast(next);
    }
  }, [toastQueue, currentToast, isBonusFlashToast]);

  // Grant 3 grass tiles on rank-up
  const grantRankUpTiles = async (uid: string) => {
    try {
      const snap = await getDoc(doc(db, 'progress', uid));
      const data = snap.data();
      const island: IslandState | undefined = data?.islandState;
      if (!island || !island.placements) return;
      const occupied = new Set<string>();
      for (const p of island.placements) {
        if (p.type === 'hex') occupied.add(`${p.q},${p.r}`);
      }
      const newPlacements = [...island.placements];
      const now = new Date().toISOString();
      for (let i = 0; i < 3; i++) {
        const pos = findBestLandPlacement(occupied);
        occupied.add(`${pos.q},${pos.r}`);
        newPlacements.push({ itemId: 'terrain-grass', model: 'grass.glb', type: 'hex', q: pos.q, r: pos.r, purchasedAt: now });
      }
      const newState: IslandState = { ...island, placements: newPlacements, lastPurchaseTimestamp: now };
      await setDoc(doc(db, 'progress', uid), { islandState: newState }, { merge: true });
    } catch {
      console.error('Failed to grant rank-up tiles:');
    }
  };

  // Detect rank changes — skip during initial load to avoid false positives
  // when gamification data arrives in stages after refresh.
  const mountTimeRef = useRef(Date.now());
  useEffect(() => {
    if (!gamification.isLoaded) return;
    const currentRankId = gamification.state.currentRank.id;
    const isInitialLoad = Date.now() - mountTimeRef.current < 3000;
    if (!isInitialLoad && prevRankRef.current !== null && prevRankRef.current !== currentRankId) {
      setRankUpModal(gamification.state.currentRank);
      if (user) grantRankUpTiles(user.uid);
    }
    prevRankRef.current = currentRankId;
  }, [gamification.state.currentRank.id, gamification.isLoaded]);

  // Detect streak milestones
  useEffect(() => {
    const milestones = [3, 7, 14, 21, 30, 50, 100];
    const current = streak.currentStreak;
    const last = lastStreakRef.current;
    if (current > last && milestones.includes(current)) {
      setStreakCelebration(current);
    }
    lastStreakRef.current = current;
  }, [streak.currentStreak]);

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

  // History state is now managed by NavigationContext (URL sync + pushState).

  // Redirect to onboarding for users without a subject profile.
  // Gated on authResolved AND progressLoaded to prevent redirect during initial load.
  useEffect(() => {
    if (authResolved && progressLoaded && user && !user.isAdmin && user.role !== 'gc' && needsOnboarding && viewState === 'tree') {
      nav.navigateToOnboarding();
    }
  }, [authResolved, progressLoaded, user, needsOnboarding, viewState]);

  // Auth state is managed by AuthContext — see contexts/AuthContext.tsx
  // handleLoginSuccess and handleLogout come from useAuth()

  const handleProgressUpdate = async (moduleId: string, newProgress: ModuleProgress) => {
    if (!user || user.isAdmin) return;

    const prevModuleProgress = userProgress[moduleId];
    const prevSection = prevModuleProgress?.unlockedSection ?? 0;
    const newSection = newProgress.unlockedSection;

    // Optimistic update — rolled back in catch if the write fails
    setUserProgress(prev => ({ ...prev, [moduleId]: newProgress }));

    try {
      const progressDocRef = doc(db, "progress", user.uid);

      // Compute points to award (pure computation, no Firestore reads)
      let pointsToAward = 0;
      let isBonus = false;
      if (newSection > prevSection) {
        const sectionsUnlocked = newSection - prevSection;
        pointsToAward = sectionsUnlocked * POINTS.SECTION_COMPLETE;

        const course = ALL_COURSES.find(c => c.id === moduleId);
        if (course) {
          if (isModuleJustCompleted(newSection, course.sectionsCount) && !isModuleJustCompleted(prevSection, course.sectionsCount)) {
            pointsToAward += POINTS.MODULE_COMPLETE_BONUS;
          }
          const updatedProgress = { ...userProgress, [moduleId]: newProgress };
          if (isCategoryJustCompleted(moduleId, updatedProgress, ALL_COURSES)) {
            const wasComplete = isCategoryJustCompleted(moduleId, userProgress, ALL_COURSES);
            if (!wasComplete) {
              pointsToAward += POINTS.CATEGORY_COMPLETE_BONUS;
            }
          }
        }

        if (pointsToAward > 0) {
          isBonus = gamification.rollBonusFlash();
          if (isBonus) pointsToAward *= 2;
        }
      }

      // Save progress + award points atomically via setDoc merge.
      // increment() is resolved server-side — no read needed, no cache staleness,
      // concurrent section completions can't clobber each other's points.
      const updates: Record<string, any> = { [moduleId]: newProgress };
      if (pointsToAward > 0) {
        updates.pointsData = { totalEarned: increment(pointsToAward) };
      }
      await setDoc(progressDocRef, updates, { merge: true });

      pointsData.reload();

      if (isBonus) {
        setToastQueue(q => [...q, 'bonus-flash']);
      }

      if (newSection > prevSection) {
        const sectionsUnlocked = newSection - prevSection;
        gamification.updateWeeklyGoalProgress('sections', sectionsUnlocked);
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
      // Roll back optimistic update — restore the full previous object, not a minimal stub
      setUserProgress(prev => ({ ...prev, [moduleId]: prevModuleProgress ?? { unlockedSection: 0 } }));
    }
  };

  const _handleSelectCategory = (category: CategoryType) => {
    nav.navigateToCategory(category);
  };

  const handleSelectModule = (moduleId: string) => {
    nav.navigateToModule(moduleId, viewState, currentCategory);
  };

  const handleGoToInnovationZone = () => { nav.navigateToInnovationZone(); };

  const handleGoToDashboard = () => { nav.navigateToDashboard(); };

  const _handleGoToLearningPaths = () => { nav.navigateToLearningPaths(); };

  const handleGoToJourney = () => { nav.navigateToJourney(); };

  const handleGoToGamificationHub = () => { nav.navigateToGamificationHub(); };

  const handleGoToStudy = () => {
    setTimetableBlockContext(null);
    nav.navigateToStudySession();
  };

  const handleStudyFromTimetable = useCallback((block: { subject: string; sessionType: 'new-learning' | 'practice' | 'revision'; durationMinutes: number; dateKey: string; blockId: string }) => {
    setTimetableBlockContext(block);
    nav.navigateToStudySession();
  }, [nav]);

  const handleGoToInsights = useCallback(() => { nav.navigateToInsights(); }, [nav]);

  const handleGoHome = () => { nav.navigateToTree(); };

  const handleOnboardingComplete = async (profile: StudentSubjectProfile, northStarData?: NorthStar, essentialsMode?: boolean) => {
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
        // yearGroup saved to Firestore — will be picked up on next auth refresh
      }
      // Save essentials mode preference to settings (use updateSetting to sync local state)
      if (essentialsMode !== undefined) {
        updateSetting('essentialsMode', essentialsMode);
      }
    } catch {
      console.error('Failed to save subject profile:');
      showToast('Couldn\'t save — check your connection', 'error');
    }
    setStudentProfile(profile);
    setNeedsOnboarding(false);
    nav.navigateToTree();
  };

  const handleNorthStarSave = async (ns: NorthStar) => {
    setNorthStar(ns);
    if (!user) return;
    try {
      const progressDocRef = doc(db, 'progress', user.uid);
      await setDoc(progressDocRef, { northStar: ns }, { merge: true });
    } catch {
      console.error('Failed to save North Star:');
      showToast('Couldn\'t save — check your connection', 'error');
    }
  };

  const handleOnboardingSkip = () => {
    setNeedsOnboarding(false);
    nav.navigateToTree();
  };

  const handleChangeSubjectsSave = async (profile: StudentSubjectProfile) => {
    setStudentProfile(profile);
    setChangeSubjectsOpen(false);
    if (!user) return;
    try {
      const progressDocRef = doc(db, 'progress', user.uid);
      await setDoc(progressDocRef, { subjectProfile: profile }, { merge: true });
    } catch {
      console.error('Failed to save updated subject profile:');
      showToast('Couldn\'t save — check your connection', 'error');
    }
  };

  const _handleBackToTree = () => { nav.goBack(); };

  const _handleBackToCategory = () => { nav.goBack(); };

  const handleDismissGuide = useCallback(async (guideId: string) => {
    setDismissedGuides(prev => ({ ...prev, [guideId]: new Date().toISOString() }));
    if (user?.uid) {
      try {
        await setDoc(doc(db, 'progress', user.uid),
          { dismissedGuides: { [guideId]: new Date().toISOString() } },
          { merge: true }
        );
      } catch {
        console.error('Failed to persist guide dismissal:');
        showToast('Couldn\'t save — check your connection', 'error');
      }
    }
  }, [user?.uid, showToast]);

  const routerProps = {
    studentProfile, userProgress, northStar, timetableCompletions,
    pointsData, streak, settings, updateSetting,
    gamification, currentToast, isBonusFlashToast,
    setCurrentToast, setIsBonusFlashToast, setRankUpModal,
    studentCourses, completedCount, smartRec, questState,
    claimQuestReward, reloadQuest,
    recommendation, strategyMastery, weeklyChallenge,
    dismissedGuides, handleDismissGuide,
    timetableBlockContext, setTimetableBlockContext, handleStudyFromTimetable,
    journeyResult, setJourneyResult,
    handleOnboardingComplete, handleOnboardingSkip,
    handleProgressUpdate,
    setSettingsOpen, setPassportOpen, setChangeSubjectsOpen, setNorthStarEditOpen,
    unlockedAvatarSeeds, setUnlockedAvatarSeeds,
    unlockedThemes, setUnlockedThemes,
    unlockedCardStyles, setUnlockedCardStyles,
  };

  return (
    <SettingsContext.Provider value={{ settings, updateSetting, unlockedThemes, unlockedCardStyles }}>
    <OfflineBanner />
    <div className="min-h-screen bg-zinc-50 dark:bg-zinc-950 transition-colors duration-500">
      {user && viewState !== 'onboarding' && user.role !== 'gc' && !user.isAdmin && (
        <div className={`fixed top-6 right-6 z-[100] ${viewState === 'my-journey' ? 'hidden' : 'hidden md:block'}`}>
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

      <AppRouter {...routerProps} />

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
        onGoToJourney={() => { setRankUpModal(null); handleGoToJourney(); }}
      />

      {/* Streak celebration */}
      <StreakCelebration
        streakCount={streakCelebration ?? 0}
        isOpen={streakCelebration !== null}
        onDismiss={() => setStreakCelebration(null)}
        weekDays={(() => {
          const today = new Date();
          const currentDayIdx = today.getDay() === 0 ? 6 : today.getDay() - 1;
          return [0,1,2,3,4,5,6].map(i => {
            const d = new Date(today);
            d.setDate(today.getDate() - (currentDayIdx - i));
            const key = d.toISOString().split('T')[0];
            return (timetableCompletions?.[key]?.length ?? 0) > 0;
          });
        })()}
      />
    </div>
    </SettingsContext.Provider>
  );
};

export default App;
