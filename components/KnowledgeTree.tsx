/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
*/

import React, { useState, useEffect, useCallback } from 'react';
import FirstVisitCoachMarks, { coachMarksSeen } from './FirstVisitCoachMarks';
import StudentHomeContent from './StudentHomeContent';
import type { StudySessionRecord } from '../studySessionData';
import HomeNextStep from './HomeNextStep';
import { KnowledgeTree as DesktopKnowledgeTree } from './KnowledgeTree.desktop';
import { useMobileAppDesign } from '../hooks/useMobileAppDesign';
import { type GamificationState } from '../gamificationConfig';
import { type CourseData } from './Library';
import { type UserSettings } from '../types';
import { toDateKey } from './subjectData';
import { type StudyBlock } from './subjectData';

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
  onGoToModules: () => void;
  onGoToInnovationZone: () => void;
  onGoToDashboard: () => void;
  onGoToLearningPaths: () => void;
  onGoToJourney: () => void;
  onGoToDirection?: () => void;
  studySessions?: StudySessionRecord[];
  onGoToStudy?: () => void;
  onGoToInsights?: () => void;
  onGoToCutContent?: () => void;
  onGoToAccreditation?: () => void;
  onGoToYearPlans?: () => void;
  onGoToWipTools?: () => void;
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
  streak?: { currentStreak: number; longestStreak: number; lastActiveDate: string };
  pointsBalance?: number;
  northStar?: { category: string; statement: string } | null;
  studentProfile?: { subjects: { subjectName: string; currentGrade?: string; targetGrade?: string; level?: string }[]; examStartDate: string; restDays?: string[]; defaultBlockDuration?: number; createdAt?: string } | null;
  timetableCompletions?: Record<string, string[]>;
  smartRecommendation?: { id: string; title: string; description: string; category: string } | null;
  questState?: { quest: { title: string; description: string; rewardPoints: number; target: number }; current: number; isCompleted: boolean; isClaimed: boolean; dayNumber: number; isOnboarding: boolean } | null;
  onClaimQuestReward?: () => void;
  onRecommendationAction?: (action: string) => void;
  /** Deep-link a Launchpad tool by id (Site Guide "Take me there"). */
  onOpenTool?: (toolId: string) => void;
  /** Stable per-account key for one-time coach marks. */
  uid?: string;
  onOpenSiteGuide?: () => void;
  onOpenFeedback?: () => void;
  onOpenMobileProfile?: () => void;
  hasUnreadNotifications?: boolean;
  gamificationState?: GamificationState | null;
  onPlannedStudy?: (block: StudyBlock, index: number) => void;
}

const noop = () => {};

const MobileKnowledgeTree: React.FC<KnowledgeTreeProps> = ({ onSelectCategory: _onSelectCategory, onGoToModules, onGoToInnovationZone, onGoToDashboard, onGoToLearningPaths, onGoToJourney, onGoToDirection, studySessions, onGoToStudy, onGoToInsights: _onGoToInsights, onGoToAccreditation: _onGoToAccreditation, onGoToYearPlans: _onGoToYearPlans, allCourses, onSelectModule, categoryTitles, userProgress, userName, userAvatarSeed, onLogout: _onLogout, onOpenSettings: _onOpenSettings, onOpenPassport: _onOpenPassport, onChangeSubjects: _onChangeSubjects, settings: _settings, updateSetting: _updateSetting, unlockedThemes: _unlockedThemes = [], completedCount: _completedCount, totalCount: _totalCount, pointsBalance, studentProfile, timetableCompletions, onOpenTool, uid, onOpenSiteGuide = noop, onOpenFeedback: _onOpenFeedback = noop, onOpenMobileProfile = noop, hasUnreadNotifications = false, gamificationState, onPlannedStudy }) => {
  // Site Guide (the "?") + one-time first-visit coach marks.
  const [coachActive, setCoachActive] = useState(false);
  // "What's new" popover + its unseen-dot state.

  // Start the spotlight once the home screen has painted.
  // This also re-evaluates when auth supplies the stable account uid instead
  // of accidentally binding the one-time tour to the anonymous key.
  useEffect(() => {
    if (coachMarksSeen(uid)) {
      setCoachActive(false);
      return;
    }
    let secondFrame = 0;
    let timer: ReturnType<typeof setTimeout> | undefined;
    const firstFrame = requestAnimationFrame(() => {
      secondFrame = requestAnimationFrame(() => {
        timer = setTimeout(() => setCoachActive(true), 180);
      });
    });
    return () => {
      cancelAnimationFrame(firstFrame);
      if (secondFrame) cancelAnimationFrame(secondFrame);
      if (timer) clearTimeout(timer);
    };
  }, [uid]);

  const finishCoachMarks = useCallback(() => setCoachActive(false), []);
  const openGuideFromCoachMarks = useCallback(() => {
    setCoachActive(false);
    onOpenSiteGuide();
  }, [onOpenSiteGuide]);

  // Press "?" anywhere on the home page to open the guide.
  useEffect(() => {
    const onKey = (e: KeyboardEvent) => {
      const t = e.target as HTMLElement | null;
      if (t && (t.tagName === 'INPUT' || t.tagName === 'TEXTAREA' || t.isContentEditable)) return;
      if (e.key === '?') onOpenSiteGuide();
    };
    window.addEventListener('keydown', onKey);
    return () => window.removeEventListener('keydown', onKey);
  }, [onOpenSiteGuide]);

  
  // ── Dashboard computed values ──────────────────────────────────────────
  const [todayBlocks, setTodayBlocks] = useState<StudyBlock[]>([]);
  const [planReady, setPlanReady] = useState(false);
  const [planError, setPlanError] = useState(false);
  useEffect(() => {
    setPlanError(false);
    if (!studentProfile || studentProfile.subjects.length === 0) { setTodayBlocks([]); setPlanReady(true); return; }
    setPlanReady(false);
    let cancelled = false;
    import('./timetableAlgorithm').then(({ computeSubjectPriorities, allocateSessions, generateWeeklyTimetable, computeWeeksUntilExam }) => {
      try {
        const today = new Date();
        const jsDay = today.getDay();
        const todayDayIndex = jsDay === 0 ? 6 : jsDay - 1;
        const priorities = computeSubjectPriorities(studentProfile.subjects as any, undefined, studentProfile.examStartDate);
        const weeksUntilExam = computeWeeksUntilExam(studentProfile.examStartDate);
        const allocations = allocateSessions(priorities, weeksUntilExam);
        const restDays = studentProfile.restDays || [];
        const blockDuration = studentProfile.defaultBlockDuration ?? 45;
        const timetable = generateWeeklyTimetable(allocations, weeksUntilExam, 0, restDays, blockDuration);
        if (!cancelled) { setTodayBlocks(timetable[todayDayIndex]?.blocks ?? []); setPlanReady(true); }
      } catch (err) {
        console.error('Failed to generate timetable blocks:', err);
        if (!cancelled) { setTodayBlocks([]); setPlanReady(true); setPlanError(true); }
      }
    }).catch(() => {
      if (!cancelled) { setTodayBlocks([]); setPlanReady(true); setPlanError(true); }
    });
    return () => { cancelled = true; };
  }, [studentProfile]);

  const todayKey = toDateKey(new Date());
  const todayCompletions = timetableCompletions?.[todayKey] || [];

  return (
    <div className="mobile-home-shell product-shell dashboard-shell min-h-screen bg-[var(--surface-canvas)] text-[var(--ink-primary)] overflow-x-hidden relative selection:bg-[rgba(var(--accent),0.2)]">


      {/* The account drawer stays in its existing shell. */}
      <div className="flex-1 bg-[var(--surface-canvas)]">
        <StudentHomeContent uid={uid} userName={userName} userAvatarSeed={userAvatarSeed} onOpenMobileProfile={onOpenMobileProfile} hasUnreadNotifications={hasUnreadNotifications} allCourses={allCourses} categoryTitles={categoryTitles} userProgress={userProgress} studySessions={studySessions} pointsBalance={pointsBalance} onSelectModule={onSelectModule} onGoToStudy={onGoToStudy} onGoToModules={onGoToModules} onGoToDashboard={onGoToDashboard} onGoToLearningPaths={onGoToLearningPaths} onGoToDirection={onGoToDirection} onGoToJourney={onGoToJourney} onGoToInnovationZone={onGoToInnovationZone} onOpenTool={onOpenTool} />
        <div className="mx-auto max-w-4xl px-5 pb-24"><HomeNextStep ready={planReady} error={planError} onPlannedStudy={onPlannedStudy} blocks={todayBlocks} completions={todayCompletions} hasProfile={Boolean(studentProfile?.subjects.length)} gamification={gamificationState} onStudy={onGoToStudy} onPlan={onOpenTool ? () => onOpenTool('planner') : undefined} onProgress={onGoToDashboard} /></div>
      </div>

      {/* One-time first-visit coach marks — end by pointing at the "?". */}
      {coachActive && (
        <FirstVisitCoachMarks
          uid={uid}
          onFinish={finishCoachMarks}
          onOpenGuide={openGuideFromCoachMarks}
        />
      )}
    </div>
  );
};

/** Both layouts share the approved Home content and retain their account shell. */
export const KnowledgeTree: React.FC<KnowledgeTreeProps> = props => {
  const mobile = useMobileAppDesign();
  return mobile ? <MobileKnowledgeTree {...props} /> : <DesktopKnowledgeTree {...props} />;
};
