/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 */

import React, { Suspense, lazy, useEffect, useRef, useState } from 'react';
import { motion } from 'framer-motion';
import { ArrowLeft, Eye, EyeOff, Check } from 'lucide-react';
import { useNavigation } from '../contexts/NavigationContext';
import { useAuth } from '../contexts/AuthContext';
import { type SessionUser, isLcaYear, isSchoolStaff } from '../utils/authUtils';
import { endStaffProvisioning, isStaffProvisioning } from '../utils/staffProvisioning';
import { isRegistrationProvisioning, registrationHoldRemainingMs } from '../utils/registrationProvisioning';
import { LoadingSpinner } from './LoadingSpinner';
import { KnowledgeTree, type CategoryType } from './KnowledgeTree';
import { Library } from './Library';

// Lazy-loaded: ModuleShowcase statically pulls in subjectModuleData + the six
// subjectContent* files (~442KB). Loading it eagerly folded all of that into
// the entry chunk — audit 2026-06-01. Its only other consumer, SubjectModule,
// is already lazy (moduleRegistry.ts).
const ModuleShowcase = lazy(() => import('./ModuleShowcase'));
const LoginPage = lazy(() => import('./LoginPage'));
const ResetPasswordPage = lazy(() => import('./ResetPasswordPage'));
const AdminDashboard = lazy(() => import('./AdminDashboard').then(m => ({ default: m.AdminDashboard })));
const GCDashboard = lazy(() => import('./GCDashboard').then(m => ({ default: m.GCDashboard })));
const DashboardView = lazy(() => import('./DashboardView'));
const LearningPathsView = lazy(() => import('./LearningPathsView'));
const YearPlansView = lazy(() => import('./YearPlansView'));
const WipTools = lazy(() => import('./WipTools'));
const ModulesView = lazy(() => import('./ModulesView').then(m => ({ default: m.ModulesView })));
import { moduleComponents, InnovationZone } from '../moduleRegistry';
import { ALL_COURSES, categoryTitles } from '../courseData';
import { ModulePositionProvider, resolveModulePosition } from '../contexts/ModulePositionContext';
import { type ModuleProgress, type UserProgress, type UserSettings, type NorthStar, type StudyReflection, type TopicMasteryV2, type UnifiedMockResult } from '../types';
import { type StreakData } from '../hooks/useStreak';
import { type FocusRecommendation } from '../hooks/useTodaysFocus';
import { type StudentSubjectProfile } from './subjectData';
import { type QuestState } from '../hooks/useQuests';
import { type SmartRecommendation } from '../hooks/useRecommendation';
import { type StrategyMasteryMap } from '../types';
import { type WeeklyChallengeState } from '../hooks/useWeeklyChallenge';
import { type GamificationState, type AchievementDefinition } from '../gamificationConfig';
import { type CourseData } from './Library';
import { type DebriefEntry } from './StudyDebrief';
import { type StudySessionRecord } from '../utils/strategyRegistry';
import { doc, setDoc, arrayUnion } from 'firebase/firestore';
import { db } from '../firebase';
import { saveInBackground } from '../utils/firestoreWrite';
import { useProgress } from '../contexts/ProgressContext';
import { DEMO_STUDENT_UID } from '../data/devStudent';
import { isProgressReadyForUser } from '../utils/progressHydration';

const Onboarding = lazy(() => import('./Onboarding'));
const JCComingSoon = lazy(() => import('./JCComingSoon'));
const JourneyView = lazy(() => import('./journey/JourneyView'));
const MyDirection = lazy(() => import('./MyDirection'));
const StudySessionView = lazy(() => import('./study/StudySessionView'));
const InsightsView = lazy(() => import('./InsightsView'));
const CutContentPage = lazy(() => import('./CutContentPage'));
const AccreditationPage = lazy(() => import('./AccreditationPage'));

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

  componentDidCatch(_error: Error, _info: React.ErrorInfo) {
    console.error('Module failed to load');
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

/* ── Props Interface ── */

export interface AppRouterProps {
  // Progress data
  studentProfile: StudentSubjectProfile | null;
  userProgress: UserProgress;
  northStar: NorthStar | null;
  timetableCompletions: Record<string, string[]>;
  studySessions: StudySessionRecord[];
  studyDebriefs: DebriefEntry[];
  studyReflections: StudyReflection[];
  topicMasteryV2: TopicMasteryV2;
  unifiedMockResults: UnifiedMockResult[];
  // `balance` is spendable (earned − spent) and drives the header pill and the
  // shop; `totalEarned` is lifetime and drives the Progress page's "earned to
  // date" stat. Keeping both here stops that stat from being fed the balance,
  // which is what made it read "−23 earned to date" after shop purchases.
  pointsData: { balance: number; totalEarned: number; reload: () => void };
  streak: StreakData;

  // Settings
  settings: UserSettings;
  updateSetting: (key: string, value: any) => void;

  // Gamification
  gamification: {
    state: GamificationState;
    isLoaded: boolean;
    checkAndUnlockAchievements: () => Promise<AchievementDefinition[]>;
    updateWeeklyGoalProgress: (metric: 'sections' | 'sessions' | 'reflections', incrementBy?: number) => Promise<void>;
    reload: () => void;
  };
  currentToast: AchievementDefinition | null;
  setCurrentToast: (toast: AchievementDefinition | null) => void;

  // Computed data
  studentCourses: CourseData[];
  completedCount: number;
  smartRec: SmartRecommendation | null;
  questState: QuestState | null;
  claimQuestReward: () => void;
  reloadQuest: () => void;

  // Hooks
  recommendation: FocusRecommendation | null;
  strategyMastery: { masteryMap: StrategyMasteryMap; recompute: () => Promise<void> };
  weeklyChallenge: WeeklyChallengeState;

  // Guides
  dismissedGuides: Record<string, string>;
  handleDismissGuide: (guideId: string) => void;

  // Timetable
  timetableBlockContext: { subject: string; sessionType: 'new-learning' | 'practice' | 'revision'; durationMinutes: number; dateKey: string; blockId: string } | null;
  setTimetableBlockContext: (block: { subject: string; sessionType: 'new-learning' | 'practice' | 'revision'; durationMinutes: number; dateKey: string; blockId: string } | null) => void;
  handleStudyFromTimetable: (block: { subject: string; sessionType: 'new-learning' | 'practice' | 'revision'; durationMinutes: number; dateKey: string; blockId: string }) => void;

  // Journey
  journeyResult: { endingId: string; finalStats?: any } | null;
  setJourneyResult: (result: { endingId: string; finalStats?: any } | null) => void;

  // Onboarding handlers
  handleOnboardingComplete: (profile: StudentSubjectProfile, northStarData?: NorthStar) => Promise<void>;
  handleOnboardingSkip: () => void;
  /** Phase 8: when set, Onboarding renders in JC→senior re-onboarding mode
   *  (Subjects → Grades → North Star, starting from step 5). */
  transitionToSeniorMode?: boolean;
  /** Year already chosen in the YearTransitionFlow modal — passed so the
   *  year-picker step doesn't need to render in transition mode. */
  transitionTargetYear?: 'TY' | '5th';

  // Progress handler
  handleProgressUpdate: (moduleId: string, newProgress: ModuleProgress) => Promise<void>;

  // Modal setters
  setSettingsOpen: (open: boolean) => void;
  setPassportOpen: (open: boolean) => void;
  setChangeSubjectsOpen: (open: boolean) => void;
  setNorthStarEditOpen: (open: boolean) => void;

  // Cosmetic unlocks (only setters needed at this layer; values flow through SettingsContext)
  setUnlockedAvatarSeeds: (seeds: string[]) => void;
  unlockedThemes: string[];
  setUnlockedThemes: (themes: string[]) => void;
  setUnlockedCardStyles: (styles: string[]) => void;
}

/**
 * The registration hold, as state rather than a bare read.
 *
 * AppRouter holds no state of its own, so a marker read only during render
 * would never be re-read when it clears or expires -- both are plain
 * sessionStorage writes that schedule no React update. On the paths where no
 * auth-state change follows (a rejected rollback, an orphaned marker) that
 * would leave the student on a spinner with nothing to end it. Scheduling a
 * repaint for the hold's remaining lifetime makes the expiry a real deadline.
 */
function useRegistrationHold(): boolean {
  const [, bump] = useState(0);
  const held = isRegistrationProvisioning();
  useEffect(() => {
    if (!held) return;
    const remaining = registrationHoldRemainingMs();
    if (remaining <= 0) { bump(n => n + 1); return; }
    const timer = window.setTimeout(() => bump(n => n + 1), remaining + 50);
    return () => window.clearTimeout(timer);
  }, [held]);
  return held;
}

const AppRouter: React.FC<AppRouterProps> = (props) => {
  const nav = useNavigation();
  const registrationHeld = useRegistrationHold();
  const { updateDemoProgress, setTimetableCompletions, progressLoaded, progressDataUid } = useProgress();
  const { viewState, dashboardSection, currentCategory, currentModuleId, cameFromJourney } = nav.state;
  const { user, userResolved, needsOnboarding, handleLoginSuccess, handleLogout } = useAuth();

  const {
    studentProfile, userProgress, northStar, timetableCompletions,
    studySessions, studyDebriefs, studyReflections, topicMasteryV2, unifiedMockResults,
    pointsData, streak, settings, updateSetting, gamification,
    studentCourses, completedCount, smartRec, questState, claimQuestReward, reloadQuest,
    recommendation, strategyMastery, weeklyChallenge,
    dismissedGuides, handleDismissGuide,
    timetableBlockContext, setTimetableBlockContext, handleStudyFromTimetable,
    journeyResult, setJourneyResult,
    handleOnboardingComplete, handleOnboardingSkip,
    transitionToSeniorMode, transitionTargetYear,
    handleProgressUpdate,
    setSettingsOpen, setPassportOpen, setChangeSubjectsOpen, setNorthStarEditOpen,
    setUnlockedAvatarSeeds,
    unlockedThemes, setUnlockedThemes,
    setUnlockedCardStyles,
  } = props;

  // Navigation handlers from context
  const handleSelectCategory = (category: CategoryType) => {
    nav.navigateToCategory(category);
  };

  const handleSelectModule = (moduleId: string) => {
    nav.navigateToModule(moduleId, viewState, currentCategory);
  };

  const handleBackToTree = () => { nav.goBack(); };
  const handleBackToCategory = () => { nav.goBack(); };
  const handleGoToModules = () => { nav.navigateToModules(); };
  const handleGoToInnovationZone = () => { nav.navigateToInnovationZone(); };
  const handleGoToDashboard = () => { nav.navigateToDashboard(); };
  const handleGoToMilestones = () => { nav.navigateToDashboard('milestones'); };
  const handleGoToLearningPaths = () => { nav.navigateToLearningPaths(); };
  const handleGoToYearPlans = () => { nav.navigateToYearPlans(); };
  const handleGoToWipTools = () => { nav.navigateToWipTools(); };
  const handleGoToJourney = () => { nav.navigateToJourney(); };
  const handleGoToStudy = () => {
    setTimetableBlockContext(null);
    nav.navigateToStudySession();
  };
  const handleGoToInsights = () => { nav.navigateToInsights(); };
  const handleGoToCutContent = () => { nav.navigateToCutContent(); };
  const handleGoToAccreditation = () => { nav.navigateToAccreditation(); };

  // Firebase password-reset action URL — handled before any auth gating so the
  // user can land here whether or not they're signed in. Triggered by either
  // the path /reset-password or the query params mode=resetPassword + oobCode
  // (the latter is what Firebase appends to the configured Action URL).
  if (typeof window !== 'undefined') {
    const params = new URLSearchParams(window.location.search);
    const path = window.location.pathname;
    const hasResetParams = params.get('mode') === 'resetPassword' && !!params.get('oobCode');
    const isResetPath = path === '/reset-password' || path.startsWith('/reset-password/');
    if (hasResetParams || isResetPath) {
      return <Suspense fallback={<LoadingSpinner />}><ResetPasswordPage /></Suspense>;
    }
  }

  // Auth gate: show branded loading until userResolved, then decide login vs app.
  // userResolved is true once either:
  //   (a) user is non-null with Firestore docs loaded, or
  //   (b) user is definitively null after a 500ms grace period.
  // This prevents flashing LoginPage when onAuthStateChanged fires null first
  // during token refresh / IndexedDB rehydration.
  if (!userResolved) {
    return (
      <div className="flex items-center justify-center min-h-screen w-full bg-[#FAFBF6] dark:bg-zinc-950">
        <svg className="animate-spin" width="36" height="36" viewBox="0 0 36 36" fill="none">
          <circle cx="18" cy="18" r="15" stroke="#e0dbd4" strokeWidth="3" />
          <path d="M18 3a15 15 0 0 1 15 15" stroke="#F26B1F" strokeWidth="3" strokeLinecap="round" />
        </svg>
      </div>
    );
  }

  // Registration is still provisioning: the account exists and the student is
  // signed in, but the flow has not reached the users/{uid} write, so the
  // rollback can still delete the account under them.
  //
  // A full-screen overlay rather than an early return, because `user` is set by
  // this point and App.tsx renders the student chrome on `user &&` (App.tsx:963
  // onwards). Returning LoginPage here put a login form inside a signed-in
  // shell, which read as having been logged out — and returning a bare spinner
  // left the header and points pill visible behind it. Covering the viewport is
  // the only version that looks deliberate.
  //
  // LoginPage does not need to stay mounted for its error to survive: the
  // failure reason crosses the remount through sessionStorage, and the fresh
  // instance picks it up (see registrationProvisioning's error hand-off).
  if (user && registrationHeld) {
    return (
      <div className="fixed inset-0 z-[200] flex flex-col items-center justify-center gap-5 bg-[#FAFBF6] dark:bg-zinc-950">
        <svg className="animate-spin" width="36" height="36" viewBox="0 0 36 36" fill="none">
          <circle cx="18" cy="18" r="15" stroke="#e0dbd4" strokeWidth="3" />
          <path d="M18 3a15 15 0 0 1 15 15" stroke="#F26B1F" strokeWidth="3" strokeLinecap="round" />
        </svg>
        <p className="text-[15px]" style={{ fontFamily: "'Source Serif 4', serif", color: '#1a1a1a' }}>
          Setting up your account&hellip;
        </p>
      </div>
    );
  }

  if (!user) {
    return <Suspense fallback={<LoadingSpinner />}><LoginPage handleLoginSuccess={handleLoginSuccess} /></Suspense>;
  }

  // Auth and progress live in separate providers. A login can publish the user
  // one render before ProgressContext has mirrored that same user's document;
  // rendering the app in that gap flashes 0 JP and empty progress. Hold the
  // route until the progress snapshot explicitly belongs to this account.
  if (!isProgressReadyForUser(user.uid, progressLoaded, progressDataUid)) {
    return <LoadingSpinner />;
  }

  // Force password change if flagged by GC reset
  if (user.needsPasswordChange) {
    return <ChangePasswordModal user={user} onComplete={handleLogout} />;
  }

  if (user.isAdmin) {
    return <Suspense fallback={<LoadingSpinner />}><AdminDashboard allCourses={ALL_COURSES} onLogout={handleLogout} /></Suspense>;
  }

  // Guidance counsellors AND teaching staff both get the Staff Dashboard
  // (full parity — owner decision 2026-07-16).
  if (isSchoolStaff(user.role) && user.school) {
    // Provisioning resolved — release the hold set during the staff claim.
    endStaffProvisioning();
    return <Suspense fallback={<LoadingSpinner />}><GCDashboard school={user.school} onLogout={handleLogout} allCourses={ALL_COURSES} gcName={user.name} gcUid={user.uid} role={user.role} /></Suspense>;
  }

  // Onboarding gate: render Onboarding immediately when the auth+progress
  // load has resolved needsOnboarding=true. Previously the redirect went
  // through a useEffect in App.tsx that nav.navigateToOnboarding()'d after
  // viewState=tree had already rendered KnowledgeTree for one or two
  // frames — causing a brief home-screen flash for fresh signups before
  // they were bounced into onboarding. Synchronous gate here removes the
  // flash because Onboarding renders on the same render pass as the
  // user/needsOnboarding being set.
  if (needsOnboarding) {
    // A teacher redeeming a staff code is signed in BEFORE claimStaffAccess has
    // granted them role:'staff', and until it does they look exactly like a
    // student with no profile. Without this they were dropped into student
    // onboarding for the 5–15s the claim takes, and could complete it —
    // writing a subjectProfile onto a staff account. Hold the loading state
    // instead; the flow reloads into the Staff Dashboard when it resolves, and
    // the marker self-expires so a failed attempt cannot strand a real student.
    if (isStaffProvisioning()) return <LoadingSpinner />;
    // A student mid-registration never reaches here — the gate above keeps
    // LoginPage mounted for the whole window in which the rollback can still
    // call deleteUser() on their live account. Left as a note rather than a
    // second check, because duplicating the condition here would be dead code.
    return (
      <Suspense fallback={<LoadingSpinner />}>
        <Onboarding userId={user.uid} userName={user.name} onComplete={handleOnboardingComplete} onSkip={handleOnboardingSkip} mode={transitionToSeniorMode ? "transition-to-senior" : "fresh"} transitionTargetYear={transitionTargetYear} />
      </Suspense>
    );
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
          onGoToProgress={handleGoToMilestones}
          dismissedGuides={dismissedGuides}
          onDismissGuide={handleDismissGuide}
          weeklyChallenge={weeklyChallenge}
          timetableBlock={timetableBlockContext}
          onTimetableBlockComplete={async (dateKey, blockId, _actualMinutes) => {
            if (!user?.uid) return;
            if (user.uid === DEMO_STUDENT_UID) {
              setTimetableCompletions(previous => {
                const nextForDay = Array.from(new Set([...(previous[dateKey] ?? []), blockId]));
                const next = { ...previous, [dateKey]: nextForDay };
                updateDemoProgress(current => ({ ...current, timetableCompletions: next }));
                return next;
              });
              setTimetableBlockContext(null);
              return;
            }
            // arrayUnion is atomic — concurrent tabs can't clobber each other's
            // completions. Fired, not awaited: a student finishing a study
            // session offline would otherwise never see the block clear.
            const progressRef = doc(db, 'progress', user.uid);
            saveInBackground(
              setDoc(progressRef, {
                timetableCompletions: { [dateKey]: arrayUnion(blockId) },
              }, { merge: true }),
              'AppRouter.autoCompleteTimetableBlock',
            );
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

  if (viewState === 'dashboard') {
    return (
      <Suspense fallback={<LoadingSpinner />}>
        <DashboardView
          userProgress={userProgress}
          allCourses={studentCourses}
          categoryTitles={categoryTitles}
          streak={streak}
          recommendation={recommendation}
          onSelectModule={handleSelectModule}
          onBack={handleBackToTree}
          pointsEarned={pointsData.totalEarned}
          studentProfile={studentProfile}
          studySessions={studySessions}
          studyDebriefs={studyDebriefs}
          studyReflections={studyReflections}
          topicMastery={topicMasteryV2}
          mockResults={unifiedMockResults}
          timetableCompletions={timetableCompletions}
          questState={questState}
          onClaimQuestReward={claimQuestReward}
          onStartStudy={handleGoToStudy}
          gamificationState={gamification.isLoaded ? gamification.state : null}
          strategyMastery={strategyMastery.masteryMap}
          weeklyChallenge={weeklyChallenge}
          pointsReload={() => { pointsData.reload(); reloadQuest(); }}
          curriculumLevel={user?.curriculumLevel}
          activeTab={dashboardSection}
          onTabChange={nav.setDashboardSection}
          darkMode={settings.darkMode}
          onToggleTheme={() => updateSetting('darkMode', !settings.darkMode)}
        />
      </Suspense>
    );
  }

  if (viewState === 'learning-paths') {
    return (
      <Suspense fallback={<LoadingSpinner />}>
        <LearningPathsView
          allCourses={studentCourses}
          userProgress={userProgress}
          onSelectModule={handleSelectModule}
          onBack={handleBackToTree}
        />
      </Suspense>
    );
  }

  if (viewState === 'wip-tools') {
    return (
      <Suspense fallback={<LoadingSpinner />}>
        <WipTools onBack={handleBackToTree} onOpenTool={(toolId: string) => nav.navigateToInnovationZone(toolId)} />
      </Suspense>
    );
  }

  if (viewState === 'year-plans') {
    return (
      <Suspense fallback={<LoadingSpinner />}>
        <YearPlansView
          allCourses={studentCourses}
          userProgress={userProgress}
          onSelectModule={handleSelectModule}
          onBack={handleBackToTree}
          isLca={isLcaYear(user?.yearGroup)}
        />
      </Suspense>
    );
  }

  if (viewState === 'onboarding') {
    return (
      <Suspense fallback={<LoadingSpinner />}>
        <Onboarding userId={user.uid} userName={user.name} onComplete={handleOnboardingComplete} onSkip={handleOnboardingSkip} mode={transitionToSeniorMode ? "transition-to-senior" : "fresh"} transitionTargetYear={transitionTargetYear} />
      </Suspense>
    );
  }

  if (viewState === 'jc-coming-soon') {
    const fromCourse = currentModuleId
      ? studentCourses.find(c => c.id === currentModuleId)
      : undefined;
    return (
      <Suspense fallback={<LoadingSpinner />}>
        <JCComingSoon
          fromCourseTitle={fromCourse?.title}
          onBack={handleBackToTree}
        />
      </Suspense>
    );
  }

  if (viewState === 'cut-content') {
    return (
      <Suspense fallback={<LoadingSpinner />}>
        <CutContentPage onBack={handleBackToTree} />
      </Suspense>
    );
  }

  if (viewState === 'accreditation') {
    return (
      <Suspense fallback={<LoadingSpinner />}>
        <AccreditationPage onBack={handleBackToTree} onOpenModule={handleSelectModule} />
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
        />
      </Suspense>
    );
  }

  if (viewState === 'my-direction' && northStar && user) {
    return (
      <Suspense fallback={<LoadingSpinner />}>
        <MyDirection
          uid={user.uid}
          northStar={northStar}
          onBack={handleBackToTree}
          onEditNorthStar={() => setNorthStarEditOpen(true)}
          onOpenFutureFinder={() => nav.navigateToInnovationZone('future-finder-revamped')}
          onOpenPointsPassport={() => nav.navigateToInnovationZone('points-passport')}
        />
      </Suspense>
    );
  }

  if (viewState === 'tree') {
    return <KnowledgeTree
      key="knowledge-tree"
      onSelectCategory={handleSelectCategory}
      onGoToModules={handleGoToModules}
      onGoToInnovationZone={handleGoToInnovationZone}
      onGoToDashboard={handleGoToDashboard}
      onGoToLearningPaths={handleGoToLearningPaths}
      onGoToYearPlans={handleGoToYearPlans}
      onGoToWipTools={handleGoToWipTools}
      onGoToJourney={handleGoToJourney}
      onGoToStudy={handleGoToStudy}
      onGoToInsights={handleGoToInsights}
      onGoToCutContent={handleGoToCutContent}
      onGoToAccreditation={handleGoToAccreditation}
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
      onOpenTool={toolId => nav.navigateToInnovationZone(toolId)}
      uid={user?.uid}
    />;
  }

  if (viewState === 'modules') {
    return (
      <Suspense fallback={<LoadingSpinner />}>
        <ModulesView
          onBack={handleBackToTree}
          onSelectCategory={handleSelectCategory}
          onSelectModule={handleSelectModule}
          allCourses={studentCourses}
          categoryTitles={categoryTitles}
          userProgress={userProgress}
        />
      </Suspense>
    );
  }

  if (viewState === 'category' && currentCategory) {
    // Validate category exists — reject garbage URL values
    if (!categoryTitles[currentCategory]) {
      return <FallbackRedirect onRedirect={() => nav.navigateToTree()} />;
    }
    // `studentCourses` is the single visibility source used everywhere else in
    // the app. Keeping the selection screen on that same ordered list ensures
    // its displayed module numbers also work for filtered JC/subject views.
    const categoryCourses = studentCourses.filter(c => c.category === currentCategory);

    // Showcase view for all main categories
    const showcaseCategories: string[] = ['architecture-mindset', 'science-growth', 'learning-cheat-codes', 'subject-specific-science', 'exam-zone'];
    if (showcaseCategories.includes(currentCategory)) {
      return (
        // Page transition from ModulesView's hero — fade + lift + slight
        // scale so the carousel arrives feeling like the hero opened up,
        // not like a hard route change. ~450ms total.
        <motion.div
          initial={{ opacity: 0, y: 18, scale: 0.985 }}
          animate={{ opacity: 1, y: 0, scale: 1 }}
          transition={{ duration: 0.45, ease: [0.16, 1, 0.3, 1] }}
          className="min-h-screen bg-[#FAFBF6] dark:bg-zinc-950"
        >
          {/* Header */}
          <header className="fixed top-0 left-0 right-0 z-50 px-4 md:px-10 bg-[#FAFBF6] dark:bg-zinc-950 border-b border-zinc-200/50 dark:border-white/[0.06]" style={{ paddingTop: 'calc(16px + var(--sat, 0px))', paddingBottom: '24px' }}>
            <div className="flex items-center gap-4">
              <button onClick={handleBackToTree} aria-label="Back to modules" className="p-2.5 rounded-xl transition-colors hover:bg-white/60" style={{ border: '1px solid rgba(0,0,0,0.06)' }}>
                <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="#1a1a1a" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><path d="M19 12H5M12 19l-7-7 7-7"/></svg>
              </button>
            </div>
          </header>
          {/* Showcase */}
          <div className="pt-28 md:pt-32 pb-24 md:pb-12 flex items-center justify-center" style={{ minHeight: 'calc(100vh - 80px)' }}>
            <Suspense fallback={<LoadingSpinner />}>
              <ModuleShowcase
                courses={categoryCourses}
                categoryTitle={categoryTitles[currentCategory]}
                categoryId={currentCategory}
                userProgress={userProgress}
                onSelectCourse={handleSelectModule}
              />
            </Suspense>
          </div>
        </motion.div>
      );
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
          <InnovationZone onBack={handleBackToTree} user={user} initialSubjectProfile={studentProfile} savedJourneyResult={journeyResult} onJourneyComplete={setJourneyResult} settings={settings} updateSetting={updateSetting} onCosmeticUnlocksChange={(unlocks) => { setUnlockedAvatarSeeds(unlocks.avatarSeeds || []); setUnlockedThemes(unlocks.themeColors || []); setUnlockedCardStyles(unlocks.cardStyles || []); }} onStudyNow={handleStudyFromTimetable} dismissedGuides={dismissedGuides} onDismissGuide={handleDismissGuide} />
        </Suspense>
      );
  }

  if (viewState === 'module' && currentModuleId) {
    const ModuleComponent = moduleComponents[currentModuleId];
    const modulePosition = resolveModulePosition(studentCourses, currentModuleId);
    // A registered module can still be outside this student's curriculum or
    // selected-subject catalogue. Do not let a manually entered URL bypass the
    // same visibility rules used by the selection screen.
    if (ModuleComponent && !modulePosition) {
      return <FallbackRedirect onRedirect={() => nav.navigateToTree()} />;
    }
    if (ModuleComponent) {
      return (
        <ModuleErrorBoundary onBack={handleBackToCategory}>
          <Suspense fallback={<LoadingSpinner />}>
            {cameFromJourney && (
              // Keep this in normal document flow. A fixed banner competes
              // with each module's own sticky mobile header and can obscure
              // both its title and back control.
              <div
                className="relative z-10 bg-[var(--accent-hex)] dark:bg-[var(--accent-hex)]"
                style={{ paddingTop: 'var(--sat, 0px)' }}
              >
                <button
                  onClick={handleBackToCategory}
                  className="w-full flex items-center justify-center gap-2 py-2 text-white text-xs font-bold hover:bg-[var(--accent-dark-hex)] dark:hover:bg-[var(--accent-dark-hex)] transition-colors"
                >
                  <ArrowLeft size={14} />
                  Back to Journey Results
                </button>
              </div>
            )}
            <ModulePositionProvider value={modulePosition}>
              <div>
                <ModuleComponent
                  onBack={handleBackToCategory}
                  progress={userProgress[currentModuleId] || { unlockedSection: 0 }}
                  onProgressUpdate={(p) => handleProgressUpdate(currentModuleId, p)}
                />
              </div>
            </ModulePositionProvider>
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

  // Fallback: unknown view state — redirect to tree via effect (not during render)
  return <FallbackRedirect onRedirect={() => nav.navigateToTree()} />;
};

/** Password change screen — shown when a GC resets a student's password */
const ChangePasswordModal: React.FC<{ user: SessionUser; onComplete: () => Promise<void> }> = ({ user: _user, onComplete }) => {
  const [newPassword, setNewPassword] = useState('');
  const [showPassword, setShowPassword] = useState(false);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState('');

  const handleChangePassword = async () => {
    if (newPassword.length < 12) { setError('Password must be at least 12 characters.'); return; }
    if (newPassword.length > 128) { setError('Password must be no more than 128 characters.'); return; }
    setIsLoading(true); setError('');
    try {
      const { getFunctions, httpsCallable } = await import('firebase/functions');
      const { default: app } = await import('../firebase');
      const functions = getFunctions(app);
      const changeFn = httpsCallable(functions, 'changeOwnPassword');
      await changeFn({ newPassword });
      await onComplete();
    } catch (err) {
      console.error('Failed to change password:', err);
      setError('Failed to change password. Try again.');
    }
    setIsLoading(false);
  };

  const inputClass = "w-full py-3.5 px-4 rounded-xl text-sm font-sans text-zinc-800 dark:text-white placeholder-zinc-400 outline-none transition-all bg-white dark:bg-zinc-900 border-2 border-zinc-200 dark:border-zinc-700 focus:border-[#F26B1F]";

  return (
    <div className="min-h-screen flex items-center justify-center p-5 bg-[#FAFBF6] dark:bg-zinc-950">
      <div className="w-full max-w-md bg-white dark:bg-zinc-900 rounded-2xl p-8 md:p-10" style={{ border: '2px solid #1a1a1a' }}>
        <h2 className="text-2xl font-semibold tracking-tight mb-1" style={{ fontFamily: "'Source Serif 4', serif", color: '#1a1a1a' }}>Set a new password</h2>
        <p className="text-sm mb-8" style={{ color: '#7a7068' }}>Your password was reset by your guidance counsellor. Please choose a new password to continue.</p>
        <div className="space-y-4">
          <div>
            <label className="text-xs font-bold uppercase tracking-wider mb-1.5 block" style={{ color: '#9e9186' }}>New Password</label>
            <div className="relative">
              <input type={showPassword ? 'text' : 'password'} value={newPassword} onChange={e => { setNewPassword(e.target.value); setError(''); }} placeholder="Choose a new password" className={inputClass} autoFocus />
              <button type="button" onClick={() => setShowPassword(!showPassword)} aria-label={showPassword ? 'Hide password' : 'Show password'} aria-pressed={showPassword} className="absolute right-3 top-1/2 -translate-y-1/2 transition-colors" style={{ color: '#9e9186' }}>
                {showPassword ? <EyeOff size={16} /> : <Eye size={16} />}
              </button>
            </div>
            {newPassword.length > 0 && newPassword.length < 12 && (
              <p className="text-xs mt-1.5" style={{ color: '#9e9186' }}>{12 - newPassword.length} more character{12 - newPassword.length !== 1 ? 's' : ''} needed</p>
            )}
            {newPassword.length >= 12 && newPassword.length <= 128 && (
              <p className="text-xs mt-1.5 flex items-center gap-1" style={{ color: '#F26B1F' }}><Check size={12} /> Looks good</p>
            )}
          </div>
          {error && <p className="text-sm text-red-500 font-medium">{error}</p>}
          <button
            onClick={handleChangePassword}
            disabled={isLoading || newPassword.length < 12 || newPassword.length > 128}
            className="w-full py-3.5 rounded-full text-white text-[15px] font-semibold transition-all disabled:opacity-50 disabled:cursor-not-allowed"
            style={{ backgroundColor: '#F26B1F', borderBottom: '3px solid #B54D14', boxShadow: '0 4px 0 #B54D14' }}
          >
            {isLoading ? 'Saving...' : 'Set Password'}
          </button>
        </div>
      </div>
    </div>
  );
};

/** Triggers a redirect via useEffect instead of during render — avoids React anti-pattern */
const FallbackRedirect: React.FC<{ onRedirect: () => void }> = ({ onRedirect }) => {
  const called = useRef(false);
  useEffect(() => {
    if (!called.current) {
      called.current = true;
      onRedirect();
    }
  }, [onRedirect]);
  return <LoadingSpinner />;
};

export default AppRouter;
