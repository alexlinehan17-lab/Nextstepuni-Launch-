/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 */

import React, { Suspense, lazy } from 'react';
import { ArrowLeft } from 'lucide-react';
import { useNavigation } from '../contexts/NavigationContext';
import { useAuth } from '../contexts/AuthContext';
import { useToast } from './Toast';
import { LoadingSpinner } from './LoadingSpinner';
import { KnowledgeTree, CategoryType } from './KnowledgeTree';
import { Library } from './Library';
import ModuleShowcase from './ModuleShowcase';

const LoginPage = lazy(() => import('./LoginPage'));
const AdminDashboard = lazy(() => import('./AdminDashboard').then(m => ({ default: m.AdminDashboard })));
const GCDashboard = lazy(() => import('./GCDashboard').then(m => ({ default: m.GCDashboard })));
const DashboardView = lazy(() => import('./DashboardView'));
const LearningPathsView = lazy(() => import('./LearningPathsView'));
import { moduleComponents, InnovationZone } from '../moduleRegistry';
import { ALL_COURSES, categoryTitles, SUBJECT_TO_MODULE } from '../courseData';
import { type ModuleProgress, type UserProgress, type UserSettings, type NorthStar } from '../types';
import { type StreakData } from '../hooks/useStreak';
import { type FocusRecommendation } from '../hooks/useTodaysFocus';
import { type StudentSubjectProfile } from './subjectData';
import { type QuestState } from '../hooks/useQuests';
import { type SmartRecommendation } from '../hooks/useRecommendation';
import { type StrategyMasteryMap } from '../types';
import { type WeeklyChallengeState } from '../hooks/useWeeklyChallenge';
import { type GamificationState, type AthleteRank, type AchievementDefinition } from '../gamificationConfig';
import { type CourseData } from './Library';
import { doc, getDoc, setDoc } from 'firebase/firestore';
import { db } from '../firebase';

const Onboarding = lazy(() => import('./Onboarding'));
const JourneyView = lazy(() => import('./journey/JourneyView'));
const TrainingHub = lazy(() => import('./TrainingHub'));
const StudySessionView = lazy(() => import('./study/StudySessionView'));
const InsightsView = lazy(() => import('./InsightsView'));

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
  pointsData: { balance: number; reload: () => void };
  streak: StreakData;

  // Settings
  settings: UserSettings;
  updateSetting: (key: string, value: any) => void;

  // Gamification
  gamification: {
    state: GamificationState;
    isLoaded: boolean;
    rollBonusFlash: () => boolean;
    checkAndUnlockAchievements: () => Promise<AchievementDefinition[]>;
    updateWeeklyGoalProgress: (metric: 'sections' | 'sessions' | 'reflections', incrementBy?: number) => Promise<void>;
    reload: () => void;
  };
  currentToast: AchievementDefinition | null;
  isBonusFlashToast: boolean;
  setCurrentToast: (toast: AchievementDefinition | null) => void;
  setIsBonusFlashToast: (v: boolean) => void;
  setRankUpModal: (rank: AthleteRank | null) => void;

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

  // Progress handler
  handleProgressUpdate: (moduleId: string, newProgress: ModuleProgress) => Promise<void>;

  // Modal setters
  setSettingsOpen: (open: boolean) => void;
  setPassportOpen: (open: boolean) => void;
  setChangeSubjectsOpen: (open: boolean) => void;
  setNorthStarEditOpen: (open: boolean) => void;

  // Cosmetic unlocks
  unlockedAvatarSeeds: string[];
  setUnlockedAvatarSeeds: (seeds: string[]) => void;
  unlockedThemes: string[];
  setUnlockedThemes: (themes: string[]) => void;
  unlockedCardStyles: string[];
  setUnlockedCardStyles: (styles: string[]) => void;
}

const AppRouter: React.FC<AppRouterProps> = (props) => {
  const { showToast } = useToast();
  const nav = useNavigation();
  const { viewState, currentCategory, currentModuleId, cameFromJourney } = nav.state;
  const { user, isLoadingAuth, handleLoginSuccess, handleLogout } = useAuth();

  const {
    studentProfile, userProgress, northStar, timetableCompletions,
    pointsData, streak, settings, updateSetting, gamification,
    currentToast, isBonusFlashToast, setCurrentToast, setIsBonusFlashToast, setRankUpModal,
    studentCourses, completedCount, smartRec, questState, claimQuestReward, reloadQuest,
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
  const handleGoToInnovationZone = () => { nav.navigateToInnovationZone(); };
  const handleGoToDashboard = () => { nav.navigateToDashboard(); };
  const handleGoToLearningPaths = () => { nav.navigateToLearningPaths(); };
  const handleGoToJourney = () => { nav.navigateToJourney(); };
  const handleGoToGamificationHub = () => { nav.navigateToGamificationHub(); };
  const handleGoToStudy = () => {
    setTimetableBlockContext(null);
    nav.navigateToStudySession();
  };
  const handleGoToInsights = () => { nav.navigateToInsights(); };

  if (isLoadingAuth) {
      return <LoadingSpinner />;
  }

  if (!user) {
    return <Suspense fallback={<LoadingSpinner />}><LoginPage handleLoginSuccess={handleLoginSuccess} /></Suspense>;
  }

  if (user.isAdmin) {
    return <Suspense fallback={<LoadingSpinner />}><AdminDashboard allCourses={ALL_COURSES} onLogout={handleLogout} /></Suspense>;
  }

  if (user.role === 'gc' && user.school) {
    return <Suspense fallback={<LoadingSpinner />}><GCDashboard school={user.school} onLogout={handleLogout} allCourses={ALL_COURSES} gcName={user.name} gcUid={user.uid} /></Suspense>;
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
              console.error('Failed to auto-complete timetable block:');
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
          uid={user?.uid}
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
          pointsBalance={pointsData.balance}
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
      onGoToTrainingHub={handleGoToGamificationHub}
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
      onDevRankUp={(rank) => setRankUpModal(rank)}
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

    // Showcase view for all main categories
    const showcaseCategories: string[] = ['architecture-mindset', 'science-growth', 'learning-cheat-codes', 'subject-specific-science', 'exam-zone'];
    if (showcaseCategories.includes(currentCategory)) {
      return (
        <div className="min-h-screen" style={{ backgroundColor: '#FDF8F0' }}>
          {/* Header */}
          <header className="fixed top-0 left-0 right-0 z-50 px-4 py-4 md:px-10 md:py-5" style={{ backgroundColor: '#FDF8F0', borderBottom: '1px solid rgba(0,0,0,0.06)' }}>
            <div className="flex items-center gap-4">
              <button onClick={handleBackToTree} className="p-2.5 rounded-xl transition-colors hover:bg-white/60" style={{ border: '1px solid rgba(0,0,0,0.06)' }}>
                <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="#1a1a1a" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><path d="M19 12H5M12 19l-7-7 7-7"/></svg>
              </button>
            </div>
          </header>
          {/* Showcase */}
          <div className="pt-24 md:pt-28 pb-12 flex items-center justify-center" style={{ minHeight: 'calc(100vh - 80px)' }}>
            <ModuleShowcase
              courses={categoryCourses}
              categoryTitle={categoryTitles[currentCategory]}
              categoryId={currentCategory}
              userProgress={userProgress}
              onSelectCourse={handleSelectModule}
            />
          </div>
        </div>
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

export default AppRouter;
