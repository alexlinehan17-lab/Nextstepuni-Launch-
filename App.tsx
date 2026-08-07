
/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
*/

import React, { useState, useEffect, useRef, useCallback, useMemo } from 'react';
import { createPortal } from 'react-dom';
import { Home, Rocket, Dumbbell, Timer, Mountain, User } from 'lucide-react';
import { UserProfile, MobileProfileSheet } from './components/UserProfileMenu';
import { type CategoryType } from './components/KnowledgeTree';
import AppRouter from './components/AppRouter';
import OfflineBanner from './components/OfflineBanner';
import CommandPalette, { TOOL_TITLES } from './components/CommandPalette';
import ShortcutsOverlay from './components/ShortcutsOverlay';
import { recordVisit } from './components/lastVisited';
import SettingsModal from './components/SettingsModal';
import YearTransitionFlow from './components/YearTransitionFlow';
import { type YearGroup, type StudentSubject } from './components/subjectData';
import { type PastJCData } from './types';
import StudyPassportModal from './components/StudyPassportModal';
import { db } from './firebase';
import { doc, getDoc, setDoc, updateDoc, arrayUnion, writeBatch } from 'firebase/firestore';
import { type ModuleProgress, type NorthStar } from './types';
import { useToast } from './components/Toast';
import { ALL_COURSES, categoryTitles } from './courseData';
import { filterCoursesForStudent } from './utils/courseVisibility';
import { saveInBackground } from './utils/firestoreWrite';
import { useSettings } from './hooks/useSettings';
import { useTodaysFocus } from './hooks/useTodaysFocus';
import { useStrategyMastery } from './hooks/useStrategyMastery';
import { useWeeklyChallenge } from './hooks/useWeeklyChallenge';
import { useRecommendation } from './hooks/useRecommendation';
import { useQuests } from './hooks/useQuests';
import './utils/bootParams'; // eager URL snapshot for deep-link params (must run before NavigationContext rewrites the URL)
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
import { isSchoolStaff } from './utils/authUtils';
import { useNavigation } from './contexts/NavigationContext';
import { useProgress } from './contexts/ProgressContext';
import { saveModuleProgress } from './services/progressRepository';

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
    { id: 'innovation-zone', label: 'Launch', icon: Rocket, action: onGoToInnovationZone },
    { id: 'profile', label: 'Profile', icon: User, action: onOpenProfile },
  ];

  // Portaled to document.body so the nav stays viewport-anchored even when an
  // ancestor (e.g. PullToRefresh) applies a transform, which would otherwise
  // re-anchor position: fixed to the transformed wrapper.
  return createPortal(
    <nav
      className="fixed bottom-0 left-0 right-0 z-[90] md:hidden bg-[#FAFBF6]/95 dark:bg-zinc-900/95 backdrop-blur-xl border-t border-zinc-200/50 dark:border-white/[0.06]"
      style={{ paddingBottom: 'var(--sab, 0px)' }}
    >
      <div className="flex items-center justify-around h-16">
        {tabs.map((tab) => {
          const isActive = tab.id === viewState || (tab.id === 'tree' && viewState === 'category');
          return (
            <button
              key={tab.id}
              onClick={tab.action}
              className={`relative flex flex-col items-center justify-center gap-1 flex-1 h-full transition-colors focus-visible:outline-none focus-visible:bg-zinc-100 dark:focus-visible:bg-zinc-800 ${isActive ? 'text-[var(--accent-hex)]' : 'text-zinc-500 dark:text-zinc-500'}`}
            >
              <tab.icon size={22} strokeWidth={isActive ? 2 : 1.5} />
              <span className="text-[10px] font-medium">{tab.label}</span>
              {isActive && <div className="absolute bottom-1.5 w-1 h-1 rounded-full bg-[var(--accent-hex)]" />}
              {tab.id === 'profile' && unreadNotifications > 0 && (
                <div className="absolute top-2 right-1/2 translate-x-3 w-2 h-2 rounded-full bg-rose-500" />
              )}
            </button>
          );
        })}
      </div>
    </nav>,
    document.body
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
  const { viewState, currentCategory, currentModuleId, cameFromJourney: _cameFromJourney, activeTool } = nav.state;
  const [journeyResult, setJourneyResult] = useState<{ endingId: string; finalStats?: any } | null>(null);
  const { user, authResolved, needsOnboarding, handleLogout, markOnboardingComplete, markOnboardingNeeded, patchUser } = useAuth();

  // Progress state from context
  const progress = useProgress();
  const {
    userProgress, setUserProgress,
    studentProfile, setStudentProfile,
    northStar, setNorthStar,
    timetableCompletions,
    pointsData, streak,
    unlockedAvatarSeeds, setUnlockedAvatarSeeds,
    unlockedThemes, setUnlockedThemes,
    unlockedCardStyles, setUnlockedCardStyles,
    dismissedGuides, setDismissedGuides,
    progressLoaded,
    reloadProgress,
  } = progress;
  // Live mirror of studentProfile, for rollbacks that may run long after the
  // handler returned. A queued Firestore write can be rejected minutes later,
  // and a rollback closure captured at call time would otherwise clobber
  // whatever the student has done since.
  const studentProfileRef = useRef(studentProfile);
  useEffect(() => { studentProfileRef.current = studentProfile; }, [studentProfile]);

  const [settingsOpen, setSettingsOpen] = useState(false);
  const [passportOpen, setPassportOpen] = useState(false);
  const [northStarEditOpen, setNorthStarEditOpen] = useState(false);
  const [changeSubjectsOpen, setChangeSubjectsOpen] = useState(false);
  // Phase 8: forward year-progression state. yearTransitionOpen drives
  // the YearTransitionFlow modal (quiet bump / TY-or-5th picker /
  // graduate confirm). transitionToSeniorMode triggers the re-onboarding
  // flow after a successful JC→senior crossover — the Onboarding shell
  // reads it and starts at step 5 (Subjects) instead of step 1.
  const [yearTransitionOpen, setYearTransitionOpen] = useState(false);
  const [transitionToSeniorMode, setTransitionToSeniorMode] = useState(false);
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
  const [toastQueue, setToastQueue] = useState<AchievementDefinition[]>([]);
  const [currentToast, setCurrentToast] = useState<AchievementDefinition | null>(null);
  const [rankUpModal, setRankUpModal] = useState<AthleteRank | null>(null);
  const prevRankRef = useRef<string | null>(null);
  const [streakCelebration, setStreakCelebration] = useState<number | null>(null);
  const lastStreakRef = useRef(0);

  // Process toast queue
  useEffect(() => {
    if (currentToast) return;
    if (toastQueue.length === 0) return;
    const next = toastQueue[0];
    setToastQueue(q => q.slice(1));
    setCurrentToast(next);
  }, [toastQueue, currentToast]);

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
      const now = new Date().toISOString();
      const tiles: IslandState['placements'] = [];
      for (let i = 0; i < 3; i++) {
        const pos = findBestLandPlacement(occupied);
        occupied.add(`${pos.q},${pos.r}`);
        tiles.push({ itemId: 'terrain-grass', model: 'grass.glb', type: 'hex', q: pos.q, r: pos.r, purchasedAt: now });
      }
      // Atomic append (arrayUnion) so a concurrent purchase/claim can't clobber
      // these rank-up tiles via a whole-array overwrite. (audit item 18)
      saveInBackground(updateDoc(doc(db, 'progress', uid), {
        'islandState.placements': arrayUnion(...tiles),
        'islandState.lastPurchaseTimestamp': now,
      }), 'App.grantRankUpTiles', undefined, { silent: true });
    } catch (err) {
      console.error('Failed to grant rank-up tiles:', err);
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

  // Shared with the GC dashboard via utils/courseVisibility — the GC must
  // score a student against the modules that student can actually open, not
  // the full catalogue. Do not re-inline this.
  const studentCourses = useMemo(
    () => filterCoursesForStudent(ALL_COURSES, user?.curriculumLevel, studentProfile),
    [studentProfile, user?.curriculumLevel],
  );

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
    if (authResolved && progressLoaded && user && !user.isAdmin && !isSchoolStaff(user.role) && needsOnboarding && viewState === 'tree') {
      nav.navigateToOnboarding();
    }
  }, [authResolved, progressLoaded, user, needsOnboarding, viewState]);

  // Auth state is managed by AuthContext — see contexts/AuthContext.tsx
  // handleLoginSuccess and handleLogout come from useAuth()

  // Record the student's last-visited module/tool for the home page
  // "Pick up where you left off" card. Watching nav state catches every
  // entry path (tiles, command palette, deep links). Tools that know more
  // (e.g. Paper Trail's subject/year) overwrite with a richer record.
  useEffect(() => {
    if (!user || user.isAdmin || isSchoolStaff(user.role)) return;
    if (viewState === 'module' && currentModuleId) {
      const course = ALL_COURSES.find(c => c.id === currentModuleId);
      if (course) recordVisit(user.uid, { kind: 'module', id: course.id, label: course.title });
    } else if (viewState === 'innovation-zone' && activeTool && TOOL_TITLES[activeTool]) {
      recordVisit(user.uid, { kind: 'tool', id: activeTool, label: TOOL_TITLES[activeTool] });
    }
  }, [viewState, currentModuleId, activeTool, user]);

  const handleProgressUpdate = async (moduleId: string, newProgress: ModuleProgress) => {
    if (!user || user.isAdmin) return;

    const prevModuleProgress = userProgress[moduleId];
    const prevSection = prevModuleProgress?.unlockedSection ?? 0;
    const newSection = newProgress.unlockedSection;

    // Optimistic update — rolled back in catch if the write fails
    setUserProgress(prev => ({ ...prev, [moduleId]: newProgress }));

    try {
      // Compute points to award (pure computation, no Firestore reads)
      let pointsToAward = 0;
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
      }

      // Save progress + award points atomically via setDoc merge.
      // increment() is resolved server-side — no read needed, no cache staleness,
      // concurrent section completions can't clobber each other's points.
      // Fired, not awaited. Awaiting meant a student working through a module
      // on bad wifi got no points, no achievement toasts and no weekly-goal
      // credit — everything below sat behind a promise that never settles
      // offline. The write itself queues and flushes on reconnect, and
      // increment() is still resolved server-side at flush time, so concurrent
      // section completions remain safe.
      saveInBackground(
        saveModuleProgress(user.uid, moduleId, newProgress, pointsToAward),
        'App.saveModuleProgress',
        // Roll back optimistic update — restore the full previous object, not a minimal stub
        () => setUserProgress(prev => ({ ...prev, [moduleId]: prevModuleProgress ?? { unlockedSection: 0 } })),
      );

      pointsData.reload();

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
      showToast('Couldn\'t save your progress — please try again', 'error');
      // Roll back optimistic update — restore the full previous object, not a minimal stub
      setUserProgress(prev => ({ ...prev, [moduleId]: prevModuleProgress ?? { unlockedSection: 0 } }));
    }
  };

  const _handleSelectCategory = (category: CategoryType) => {
    nav.navigateToCategory(category);
  };

  const handleSelectModule = (moduleId: string) => {
    // JC click interception (Phase 4): if the user is JC and the target
    // module is tagged `jcStatus: 'coming-soon'`, route to the placeholder
    // screen instead of opening the senior LC module body.
    if (user?.curriculumLevel === 'junior') {
      const course = ALL_COURSES.find(c => c.id === moduleId);
      if (course?.jcStatus === 'coming-soon') {
        nav.navigateToJCComingSoon(moduleId);
        return;
      }
    }
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
    // These writes are fired, NOT awaited.
    //
    // Awaiting them stranded any student who finished onboarding without a
    // live connection: with persistentLocalCache a setDoc promise settles only
    // on server acknowledgement, so offline it never resolves and never
    // rejects. markOnboardingComplete() — the only thing that clears
    // AppRouter's needsOnboarding gate — sat after the await, so the student
    // tapped the final button and NOTHING happened: no navigation, no error,
    // no spinner, and the catch below could never fire. The offline banner
    // doesn't rescue it either, because it keys off navigator.onLine, which
    // stays true on captive-portal school wifi — exactly the case that hangs.
    //
    // The writes themselves are safe: Firestore applies them to the local
    // cache immediately and flushes them on reconnect. A rejection here is a
    // REAL failure (rules, quota, malformed data), and only then do we roll
    // back and return the student to onboarding — keeping the 2026-05-23
    // lesson that a student must never end up "onboarded" with no profile.
    const previousProfile = studentProfile;
    const previousNorthStar = northStar;
    const previousYearGroup = user.yearGroup;
    const previousCurriculumLevel = user.curriculumLevel;

    let rolledBack = false;
    const rollback = (err: unknown) => {
      if (rolledBack) return;
      rolledBack = true;
      // A queued write can be rejected minutes later, long after the student
      // has moved on. Only unwind if THIS profile is still the live one —
      // otherwise we'd clobber a newer, successful onboarding and yank them
      // out of whatever they were doing.
      if (studentProfileRef.current !== profile) {
        console.error('Onboarding save rejected after the profile moved on:', err);
        showToast('An earlier change could not be saved.', 'error');
        return;
      }
      console.error('Failed to save subject profile:', err);
      // Surface the actual Firebase error so silent bugs (rules rejection,
      // App Check, quota, malformed data) can't hide behind a generic
      // "check your connection" message.
      const rawMsg = err instanceof Error ? err.message : String(err);
      const trimmed = rawMsg.length > 120 ? rawMsg.slice(0, 120) + '…' : rawMsg;
      showToast(`Couldn't save: ${trimmed}`, 'error');
      setStudentProfile(previousProfile);
      setNorthStar(previousNorthStar);
      patchUser({ yearGroup: previousYearGroup, curriculumLevel: previousCurriculumLevel });
      // Re-raise the gate. markOnboardingComplete() has already run by the time
      // a rejection arrives, and it is one-way — without this the student stays
      // "onboarded" with no profile and AppRouter's gate is dead for the rest
      // of the session.
      markOnboardingNeeded();
      nav.navigateToOnboarding();
    };

    const progressDocRef = doc(db, 'progress', user.uid);
    const saveData: Record<string, any> = { subjectProfile: profile };
    if (northStarData) {
      saveData.northStar = northStarData;
      saveData.islandState = createStarterState(northStarData.category);
      setNorthStar(northStarData);
    }
    setDoc(progressDocRef, saveData, { merge: true }).catch(rollback);

    // Also save yearGroup + curriculumLevel to the users doc for GC dashboard
    // filtering and content gating (Phase 1 JC plumbing).
    if (profile.yearGroup) {
      const userDocRef = doc(db, 'users', user.uid);
      const userPatch: Record<string, any> = { yearGroup: profile.yearGroup };
      if (profile.curriculumLevel) userPatch.curriculumLevel = profile.curriculumLevel;
      setDoc(userDocRef, userPatch, { merge: true }).catch(rollback);
      // Mirror the write into the in-memory SessionUser so the rest of
      // the app (Settings → School Year, GC dashboard filters, etc.)
      // doesn't have to wait for the next sign-in to see the values.
      patchUser({
        yearGroup: profile.yearGroup,
        curriculumLevel: profile.curriculumLevel,
      });
    }
    // Save essentials mode preference to settings (use updateSetting to sync local state)
    if (essentialsMode !== undefined) {
      updateSetting('essentialsMode', essentialsMode);
    }
    // Trigger a Firestore re-fetch so local state matches the just-written
    // doc. Defensive against any setter drift between handleOnboardingComplete
    // and the next render — surfaced 2026-05-24 when JourneyView reported
    // northStar=null right after a successful onboarding. Safe offline: reads
    // resolve from the persistent cache, which already holds the write above.
    reloadProgress();
    // Phase 8: if this was a JC→senior re-onboarding, clear the
    // transition flag and show a celebratory toast. The flag-clear
    // hands control back to the regular fresh-mode flow for any
    // future re-runs (which wouldn't happen anyway).
    if (transitionToSeniorMode) {
      setTransitionToSeniorMode(false);
      showToast('Welcome to senior cycle!', 'success');
    }
    setStudentProfile(profile);
    markOnboardingComplete();
    nav.navigateToTree();
  };

  const handleNorthStarSave = async (ns: NorthStar) => {
    setNorthStar(ns);
    if (!user) return;
    try {
      const progressDocRef = doc(db, 'progress', user.uid);
      // setNorthStar already ran above — fire the write so an offline student
      // still keeps their North Star on screen.
      saveInBackground(setDoc(progressDocRef, { northStar: ns }, { merge: true }), 'App.saveNorthStar');
    } catch (err) {
      console.error('Failed to save North Star:', err);
      showToast('Couldn\'t save — check your connection', 'error');
    }
  };

  const handleOnboardingSkip = () => {
    markOnboardingComplete();
    nav.navigateToTree();
  };

  // ─── Phase 8: year-progression handlers ─────────────────────────────
  //
  // All three handlers write to users/{uid} (and progress/{uid} where
  // relevant), then trigger a ProgressContext reload so the next render
  // reflects the new authoritative Firestore state. The YearTransitionFlow
  // modal closes itself on completion.

  // Quiet bump: write the new yearGroup to users/{uid}, refresh local
  // SessionUser via AuthContext, brief celebratory toast. Curriculum
  // doesn't change for any of these transitions (1st→2nd, 2nd→3rd
  // stay junior; TY→5th, 5th→6th stay senior).
  const handleConfirmYearBump = async (next: YearGroup) => {
    if (!user) return;
    // Optimistic: patch the session first, then fire the write. Awaiting it
    // left the year-progression modal open forever offline — the promise never
    // settles, so neither patchUser nor the toast ever ran.
    const previousYearGroup = user.yearGroup;
    patchUser({ yearGroup: next });
    showToast(`Welcome to ${next === 'TY' ? 'TY' : next + ' Year'}!`, 'success');
    saveInBackground(
      setDoc(doc(db, 'users', user.uid), { yearGroup: next }, { merge: true }),
      'App.confirmYearBump',
      () => {
        patchUser({ yearGroup: previousYearGroup });
        showToast('Couldn\'t update your year — please try again.', 'error');
      },
    );
  };

  // JC → senior crossover: archive JC data, clear active JC fields,
  // update yearGroup + curriculumLevel, then enter the re-onboarding
  // wrapper so the user picks fresh senior subjects/grades/NS.
  const handleConfirmJCtoSenior = async (target: 'TY' | '5th') => {
    if (!user || !studentProfile) return;
    // Both writes are fired, not awaited. Awaiting them offline left the
    // student in the worst possible state: the modal stayed open, nothing
    // happened, and re-tapping re-ran the whole archive-and-clear. Because the
    // archive is built from CURRENT state, a half-applied retry could also
    // archive an already-cleared profile.
    //
    // Ordering matters here. The archive write must be issued BEFORE local
    // state is nulled, so `studentProfile` is still populated when we read it.
    // Both writes hit the local cache synchronously, so the archive is durable
    // (queued) before we clear anything — offline included.
    const now = new Date().toISOString();
    // 1. Build the PastJCData archive from the current active state.
    const archive: PastJCData = {
      transitionedAt: now,
      jcYearGroup: '3rd',
      jcSubjects: studentProfile.subjects.map((s: StudentSubject) => ({ ...s })),
      ...(northStar ? { jcNorthStar: northStar } : {}),
    };

    const previousProfile = studentProfile;
    const previousNorthStar = northStar;
    const previousYearGroup = user.yearGroup;
    const previousCurriculumLevel = user.curriculumLevel;
    let rolledBack = false;
    const rollback = (err: unknown) => {
      if (rolledBack) return;
      rolledBack = true;
      // Only unwind if the student is still mid-transition — a late rejection
      // must not drag them out of a re-onboarding they've since completed.
      if (studentProfileRef.current !== null) {
        console.error('JC->senior rejected after the profile moved on:', err);
        showToast('An earlier change could not be saved.', 'error');
        return;
      }
      console.error('Failed to transition to senior cycle:', err);
      showToast('Couldn\'t move you up a year — please try again.', 'error');
      setStudentProfile(previousProfile);
      setNorthStar(previousNorthStar);
      setTransitionToSeniorMode(false);
      patchUser({ yearGroup: previousYearGroup, curriculumLevel: previousCurriculumLevel });
      nav.navigateToTree();
    };

    // 2+3. ONE ATOMIC BATCH across both documents.
    //
    // These must not be two independent writes. The users doc carries the ONLY
    // copy of the JC archive; the progress doc write DESTROYS the live profile.
    // Issued separately, a rejected archive with a successful clear loses the
    // student's entire Junior Cycle subject list and North Star permanently —
    // and the rollback can't help, because it only restores React state while
    // reloadProgress() re-reads the cleared doc. A batch is all-or-nothing and
    // still queues offline as a single unit, so the offline fix is preserved.
    const batch = writeBatch(db);
    batch.set(doc(db, 'users', user.uid), {
      yearGroup: target,
      curriculumLevel: 'senior',
      pastJCData: archive,
    }, { merge: true });
    batch.set(doc(db, 'progress', user.uid), {
      subjectProfile: null,
      northStar: null,
    }, { merge: true });
    saveInBackground(batch.commit(), 'App.jcToSenior', rollback);
    patchUser({ yearGroup: target, curriculumLevel: 'senior' });
    // 4. Flip local state and open the transition re-onboarding shell.
    setStudentProfile(null);
    setNorthStar(null);
    setTransitionToSeniorMode(true);
    // Onboarding gate in AppRouter will catch needsOnboarding=true and
    // render Onboarding. The transitionToSeniorMode flag passes through
    // to switch the flow to Subjects → Grades → NS.
    // We need to mark onboarding as needed again so the gate fires.
    // markOnboardingNeeded is set via the progressDoc subjectProfile=null
    // write above; AuthContext's loadedData.needsOnboarding derives
    // from that, but it won't auto-refresh — trigger a reload. Safe offline:
    // reads resolve from the persistent cache, which holds the writes above.
    reloadProgress();
    nav.navigateToOnboarding();
  };

  // Graduation: write yearGroup='graduated'. No sign-out, no special
  // screen — the user retains full app access. Settings flips to the
  // soft post-LC label on next render.
  const handleConfirmGraduate = async () => {
    if (!user) return;
    const previousYearGroup = user.yearGroup;
    patchUser({ yearGroup: 'graduated' });
    showToast('Best of luck with what\'s next.', 'success');
    saveInBackground(
      setDoc(doc(db, 'users', user.uid), { yearGroup: 'graduated' }, { merge: true }),
      'App.confirmGraduate',
      () => {
        patchUser({ yearGroup: previousYearGroup });
        showToast('Couldn\'t update — please try again.', 'error');
      },
    );
  };

  const handleChangeSubjectsSave = async (profile: StudentSubjectProfile) => {
    setChangeSubjectsOpen(false);
    if (!user) { setStudentProfile(profile); return; }
    // Optimistic commit + rollback on a real rejection. Awaiting the write
    // before committing would hang forever offline — with persistentLocalCache
    // a setDoc promise settles only on server acknowledgement, so it neither
    // resolves nor rejects, and the student's subject change would silently do
    // nothing with no error shown. The write is still safe offline: Firestore
    // applies it locally at once and flushes it on reconnect.
    const previousProfile = studentProfile;
    setStudentProfile(profile);
    const progressDocRef = doc(db, 'progress', user.uid);
    setDoc(progressDocRef, { subjectProfile: profile }, { merge: true })
      .catch(err => {
        console.error('Failed to save updated subject profile:', err);
        showToast('Couldn\'t save your subjects — please try again', 'error');
        setStudentProfile(previousProfile);
      });
  };

  const _handleBackToTree = () => { nav.goBack(); };

  const _handleBackToCategory = () => { nav.goBack(); };

  const handleDismissGuide = useCallback(async (guideId: string) => {
    setDismissedGuides(prev => ({ ...prev, [guideId]: new Date().toISOString() }));
    if (user?.uid) {
      try {
        saveInBackground(setDoc(doc(db, 'progress', user.uid),
          { dismissedGuides: { [guideId]: new Date().toISOString() } },
          { merge: true }
        ), 'App.dismissGuide', undefined, { silent: true });
      } catch (err) {
        console.error('Failed to persist guide dismissal:', err);
        showToast('Couldn\'t save — check your connection', 'error');
      }
    }
  }, [user?.uid, showToast]);

  const routerProps = {
    studentProfile, userProgress, northStar, timetableCompletions,
    pointsData, streak, settings, updateSetting,
    gamification, currentToast,
    setCurrentToast,
    studentCourses, completedCount, smartRec, questState,
    claimQuestReward, reloadQuest,
    recommendation, strategyMastery, weeklyChallenge,
    dismissedGuides, handleDismissGuide,
    timetableBlockContext, setTimetableBlockContext, handleStudyFromTimetable,
    journeyResult, setJourneyResult,
    handleOnboardingComplete, handleOnboardingSkip,
    transitionToSeniorMode, transitionTargetYear: (transitionToSeniorMode ? (user?.yearGroup === 'TY' ? 'TY' : '5th') : undefined) as 'TY' | '5th' | undefined,
    handleProgressUpdate,
    setSettingsOpen, setPassportOpen, setChangeSubjectsOpen, setNorthStarEditOpen,
    setUnlockedAvatarSeeds,
    unlockedThemes, setUnlockedThemes,
    setUnlockedCardStyles,
  };

  return (
    <SettingsContext.Provider value={{ settings, updateSetting, unlockedThemes, unlockedCardStyles }}>
    <OfflineBanner />
    <div className="min-h-screen bg-zinc-50 dark:bg-zinc-950 transition-colors duration-500">
      {user && viewState !== 'onboarding' && !isSchoolStaff(user.role) && !user.isAdmin && (
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
                onDismiss={() => setCurrentToast(null)}
              />
            </div>
            <NotificationBell uid={user.uid} onUnreadCountChange={setUnreadNotificationCount} />
            <UserProfile user={user} onLogout={handleLogout} settings={settings} updateSetting={updateSetting} onOpenSettings={() => setSettingsOpen(true)} avatarOverride={settings.avatar} streak={streak} recommendation={recommendation} onSelectModule={handleSelectModule} onOpenPassport={() => setPassportOpen(true)} onGoToDashboard={handleGoToDashboard} completedCount={completedCount} totalCount={studentCourses.length} onOpenNorthStar={() => setNorthStarEditOpen(true)} hasNorthStar={northStar !== null} unlockedThemes={unlockedThemes} />
          </div>
        </div>
      )}

      {/* Mobile achievement toast — TrainingPulse removed on mobile per design feedback.
          AchievementToast still needs a mount point on mobile so it appears
          unobtrusively at top-left when a new achievement fires. */}
      {user && viewState !== 'onboarding' && viewState !== 'module' && !isSchoolStaff(user.role) && !user.isAdmin && (
        <div className="fixed top-4 left-4 z-[100] md:hidden pointer-events-none">
          <div className="pointer-events-auto">
            <AchievementToast
              achievement={currentToast}
              onDismiss={() => setCurrentToast(null)}
            />
          </div>
        </div>
      )}

      <AppRouter {...routerProps} />

      {/* Global QoL overlays — ⌘K jump-to + "?" shortcut card (students only) */}
      {user && !user.isAdmin && !isSchoolStaff(user.role) && viewState !== 'onboarding' && (
        <>
          <CommandPalette courses={studentCourses} />
          <ShortcutsOverlay suppressQuestionKey={viewState === 'tree'} />
        </>
      )}

      {user && viewState !== 'onboarding' && viewState !== 'module' && !user.isAdmin && !isSchoolStaff(user.role) && (
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

      {user && !user.isAdmin && !isSchoolStaff(user.role) && (
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
            userYearGroup={user?.yearGroup}
            onChangeSubjects={studentProfile ? () => { setSettingsOpen(false); setChangeSubjectsOpen(true); } : undefined}
            onResetNorthStar={() => { setSettingsOpen(false); setNorthStarEditOpen(true); }}
            onAdvanceYear={() => { setSettingsOpen(false); setYearTransitionOpen(true); }}
            onLogout={handleLogout}
          />
          <YearTransitionFlow
            isOpen={yearTransitionOpen}
            onClose={() => setYearTransitionOpen(false)}
            currentYearGroup={user?.yearGroup}
            onConfirmBump={handleConfirmYearBump}
            onConfirmJCtoSenior={handleConfirmJCtoSenior}
            onConfirmGraduate={handleConfirmGraduate}
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
            curriculumLevel={user?.curriculumLevel}
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
