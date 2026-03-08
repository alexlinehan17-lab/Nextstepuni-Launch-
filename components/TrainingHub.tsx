/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 */

import React from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import {
  ArrowLeft, Flame, TrendingUp, Target, Zap, Award, Crown, Mountain,
  Footprints, Coins, Star, ChevronRight, BarChart3,
  BookOpen, Clock, PenLine, Layers, Brain, Repeat, Shuffle, HelpCircle,
  Compass, Sprout, Shield, Radar, ClipboardCheck, Sparkles, Trophy, CheckCircle2,
} from 'lucide-react';
import { type GamificationState, type StreakTier, getStreakTier, getWeekNumber, generateWeeklyGoals } from '../gamificationConfig';
import { type StreakData } from '../hooks/useStreak';
import { type NorthStar, type UserProgress, type StrategyMasteryMap, type MasteryTier } from '../types';
import { ActivityRing } from './ModuleShared';
import WeeklyGoals from './WeeklyGoals';
import AchievementGallery from './AchievementGallery';
import { type CourseData } from './Library';
import { STRATEGY_REGISTRY } from '../studySessionData';
import { type WeeklyChallengeState } from '../hooks/useWeeklyChallenge';

const MotionDiv = motion.div as any;
const MotionButton = motion.button as any;

const RANK_ICONS: Record<string, React.ElementType> = {
  Footprints, TrendingUp, Target, Zap, Award, Crown, Mountain,
};

const TIER_ORDER: MasteryTier[] = ['learned', 'practiced', 'applied', 'habitual'];

const TIER_CONFIG: Record<MasteryTier, { label: string; color: string; bg: string; border: string }> = {
  none: { label: 'Not Started', color: 'text-zinc-400 dark:text-zinc-500', bg: 'bg-zinc-100 dark:bg-zinc-800', border: 'border-zinc-200 dark:border-zinc-700' },
  learned: { label: 'Learned', color: 'text-blue-600 dark:text-blue-400', bg: 'bg-blue-50 dark:bg-blue-900/20', border: 'border-blue-200 dark:border-blue-800/40' },
  practiced: { label: 'Practiced', color: 'text-teal-600 dark:text-teal-400', bg: 'bg-teal-50 dark:bg-teal-900/20', border: 'border-teal-200 dark:border-teal-800/40' },
  applied: { label: 'Applied', color: 'text-amber-600 dark:text-amber-400', bg: 'bg-amber-50 dark:bg-amber-900/20', border: 'border-amber-200 dark:border-amber-800/40' },
  habitual: { label: 'Habitual', color: 'text-purple-600 dark:text-purple-400', bg: 'bg-purple-50 dark:bg-purple-900/20', border: 'border-purple-200 dark:border-purple-800/40' },
};

const STRATEGY_ICONS: Record<string, React.ElementType> = {
  'mastering-active-recall-protocol': Brain,
  'mastering-spaced-repetition-protocol': Repeat,
  'mastering-interleaving-protocol': Shuffle,
  'elaborative-interrogation-protocol': HelpCircle,
  'agency-protocol': Compass,
  'growth-mindset-protocol': Sprout,
  'digital-distraction-protocol': Shield,
  'learning-radar-protocol': Radar,
  'exam-hall-strategies-protocol': ClipboardCheck,
};

const CHALLENGE_ICONS: Record<string, React.ElementType> = {
  Brain, Repeat, Shuffle, HelpCircle, Compass, Sprout, Shield, Radar,
  ClipboardCheck, Clock, Zap, PenLine, Trophy,
};

interface TrainingHubProps {
  gamificationState: GamificationState;
  streak: StreakData;
  pointsBalance: number;
  northStar: NorthStar | null;
  onBack: () => void;
  onOpenJourney: () => void;
  userProgress: UserProgress;
  allCourses: CourseData[];
  strategyMastery?: StrategyMasteryMap;
  dismissedGuides?: Record<string, string>;
  onDismissGuide?: (id: string) => void;
  weeklyChallenge?: WeeklyChallengeState;
  pointsReload?: () => void;
  onGoToStudy?: () => void;
}

const TrainingHub: React.FC<TrainingHubProps> = ({
  gamificationState,
  streak,
  pointsBalance,
  northStar,
  onBack,
  onOpenJourney,
  userProgress,
  allCourses,
  strategyMastery,
  dismissedGuides,
  onDismissGuide,
  weeklyChallenge,
  pointsReload,
  onGoToStudy,
}) => {
  const {
    currentRank,
    nextRank,
    rankProgress,
    totalPointsEarned,
    personalBests,
    unlockedAchievements,
    weeklyGoalProgress,
    weekStartDate,
    modulesCompleted,
    sectionsCompleted,
    totalReflections,
    totalTimetableSessions,
    categoriesCompleted,
  } = gamificationState;

  const RankIcon = RANK_ICONS[currentRank.icon] || Footprints;
  const streakTier = getStreakTier(streak.currentStreak);
  const weekNumber = getWeekNumber();
  const weeklyGoals = generateWeeklyGoals(currentRank.id, weekNumber);

  // Count completed modules for stats
  const totalModules = allCourses.length;

  return (
    <div className="min-h-screen bg-zinc-50 dark:bg-zinc-950 pt-16 md:pt-24 pb-40 md:pb-32 px-4 sm:px-6 transition-colors duration-500">
      <div className="max-w-3xl mx-auto">
        {/* Header */}
        <div className="flex items-center gap-4 mb-10">
          <button
            onClick={onBack}
            className="w-10 h-10 rounded-xl bg-white dark:bg-zinc-900 border border-zinc-200 dark:border-zinc-800 flex items-center justify-center text-zinc-500 hover:text-zinc-900 dark:hover:text-white transition-colors focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-[rgba(var(--accent),0.5)]"
          >
            <ArrowLeft size={18} />
          </button>
          <h1 className="font-serif text-3xl md:text-4xl font-semibold text-zinc-900 dark:text-white tracking-tight">
            Training Hub
          </h1>
        </div>

        {/* First-visit intro card */}
        <AnimatePresence>
          {!dismissedGuides?.['training-hub-intro'] && (
            <MotionDiv
              key="training-hub-intro"
              initial={{ opacity: 0, y: -8 }}
              animate={{ opacity: 1, y: 0 }}
              exit={{ opacity: 0, y: -8, transition: { duration: 0.2 } }}
              className="bg-[rgba(var(--accent),0.04)] border border-[rgba(var(--accent),0.15)] rounded-2xl p-5 mb-6"
            >
              <div className="flex items-start gap-3">
                <Sparkles size={18} className="text-[rgba(var(--accent),1)] shrink-0 mt-0.5" />
                <div className="space-y-2">
                  <p className="font-semibold text-sm text-zinc-800 dark:text-white">Welcome to Training Hub</p>
                  <p className="text-sm text-zinc-600 dark:text-zinc-400 leading-relaxed">
                    Training Hub tracks your rank, weekly goals, and strategy mastery. Mastery has 4 tiers — Learned, Practiced, Applied, and Habitual — earned by engaging with strategy prompts during study sessions.
                  </p>
                  <button
                    onClick={() => onDismissGuide?.('training-hub-intro')}
                    className="mt-1 text-sm font-medium text-[rgba(var(--accent),1)] hover:underline"
                  >
                    Got it
                  </button>
                </div>
              </div>
            </MotionDiv>
          )}
        </AnimatePresence>

        {/* ── 1. Rank Card ── */}
        <MotionDiv
          initial={{ opacity: 0, y: 12 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.4, delay: 0.05 }}
          className="card-styled bg-white dark:bg-zinc-900 border border-zinc-200 dark:border-zinc-800 rounded-2xl p-6 mb-6"
        >
          <div className="flex items-center gap-5">
            {/* Activity ring with rank icon */}
            <div className="relative shrink-0">
              <ActivityRing
                progress={rankProgress}
                color={currentRank.colorHex}
                size={88}
                strokeWidth={6}
              />
              <div className="absolute inset-0 flex items-center justify-center mb-4">
                <RankIcon size={28} style={{ color: currentRank.colorHex }} />
              </div>
            </div>
            <div className="flex-1">
              <p className="text-[10px] font-semibold uppercase tracking-widest text-zinc-400 dark:text-zinc-500 mb-1">
                Current Rank
              </p>
              <h2
                className="text-2xl font-bold mb-1"
                style={{ color: currentRank.colorHex }}
              >
                {currentRank.title}
              </h2>
              {nextRank ? (
                <p className="text-xs text-zinc-500 dark:text-zinc-400">
                  {totalPointsEarned}/{nextRank.minPoints} pts to {nextRank.title}
                </p>
              ) : (
                <p className="text-xs text-zinc-500 dark:text-zinc-400">
                  Maximum rank achieved
                </p>
              )}
              {/* Progress bar */}
              {nextRank && (
                <div className="w-full h-2 bg-zinc-100 dark:bg-zinc-800 rounded-full overflow-hidden mt-2">
                  <motion.div
                    className="h-full rounded-full"
                    style={{ backgroundColor: currentRank.colorHex }}
                    initial={{ width: 0 }}
                    animate={{ width: `${rankProgress}%` }}
                    transition={{ duration: 1, ease: 'easeOut' }}
                  />
                </div>
              )}
            </div>
          </div>

          {/* Quick stats row */}
          <div className="grid grid-cols-3 gap-3 mt-5 pt-5 border-t border-zinc-200/50 dark:border-white/[0.06]">
            <div className="text-center">
              <p className="text-lg font-bold text-zinc-800 dark:text-white">{streak.currentStreak}</p>
              <p className="text-[10px] text-zinc-400 dark:text-zinc-500 font-medium">Day Streak</p>
            </div>
            <div className="text-center">
              <p className="text-lg font-bold text-zinc-800 dark:text-white">{totalPointsEarned}</p>
              <p className="text-[10px] text-zinc-400 dark:text-zinc-500 font-medium">Total XP</p>
            </div>
            <div className="text-center">
              <p className="text-lg font-bold text-zinc-800 dark:text-white">{pointsBalance}</p>
              <p className="text-[10px] text-zinc-400 dark:text-zinc-500 font-medium">Balance</p>
            </div>
          </div>
        </MotionDiv>

        {/* ── 2. Weekly Goals ── */}
        <MotionDiv
          initial={{ opacity: 0, y: 12 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.4, delay: 0.1 }}
          className="card-styled bg-white dark:bg-zinc-900 border border-zinc-200 dark:border-zinc-800 rounded-2xl p-6 mb-6"
        >
          <WeeklyGoals
            goals={weeklyGoals}
            progress={weeklyGoalProgress}
            weekStartDate={weekStartDate}
          />
        </MotionDiv>

        {/* ── 2b. Weekly Challenge ── */}
        {weeklyChallenge?.isLoaded && (
          <MotionDiv
            initial={{ opacity: 0, y: 12 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.4, delay: 0.12 }}
            className="mb-6"
          >
            {(() => {
              const ch = weeklyChallenge;
              const ChallengeIcon = CHALLENGE_ICONS[ch.challenge.icon] || Trophy;
              const progressPct = Math.min(100, Math.round((ch.current / ch.challenge.target) * 100));
              const cardBg = ch.isClaimed
                ? 'bg-emerald-50 dark:bg-emerald-900/20 border-emerald-200 dark:border-emerald-800/40'
                : ch.isCompleted
                ? 'bg-amber-50 dark:bg-amber-900/20 border-amber-200 dark:border-amber-800/40'
                : 'bg-white dark:bg-zinc-900 border-zinc-200 dark:border-zinc-800';

              return (
                <div className={`card-styled border rounded-2xl p-6 ${cardBg}`}>
                  {/* Header */}
                  <div className="flex items-center justify-between mb-4">
                    <div className="flex items-center gap-2">
                      <Trophy size={16} className="text-amber-500" />
                      <h3 className="text-sm font-semibold uppercase tracking-widest text-zinc-400 dark:text-zinc-500">
                        Weekly Challenge
                      </h3>
                    </div>
                    <span className="text-xs font-bold text-amber-600 dark:text-amber-400 bg-amber-100 dark:bg-amber-900/30 px-2 py-0.5 rounded-full">
                      +{ch.challenge.rewardPoints} pts
                    </span>
                  </div>

                  {/* Challenge info */}
                  <div className="flex items-start gap-3 mb-4">
                    <div className="w-10 h-10 rounded-xl bg-zinc-100 dark:bg-zinc-800 flex items-center justify-center shrink-0">
                      <ChallengeIcon size={20} className="text-zinc-600 dark:text-zinc-400" />
                    </div>
                    <div>
                      <p className="text-base font-semibold text-zinc-800 dark:text-white">{ch.challenge.title}</p>
                      <p className="text-sm text-zinc-500 dark:text-zinc-400 mt-0.5">{ch.challenge.description}</p>
                    </div>
                  </div>

                  {/* Progress bar */}
                  <div className="mb-3">
                    <div className="flex items-center justify-between mb-1.5">
                      <span className="text-xs font-medium text-zinc-500 dark:text-zinc-400">Progress</span>
                      <span className="text-xs font-bold text-zinc-700 dark:text-zinc-300">
                        {ch.current}/{ch.challenge.target}
                      </span>
                    </div>
                    <div className="w-full h-2 bg-zinc-200 dark:bg-zinc-700 rounded-full overflow-hidden">
                      <motion.div
                        className={`h-full rounded-full ${ch.isClaimed ? 'bg-emerald-500' : ch.isCompleted ? 'bg-amber-500' : 'bg-[var(--accent-hex)]'}`}
                        initial={{ width: 0 }}
                        animate={{ width: `${progressPct}%` }}
                        transition={{ duration: 0.8, ease: 'easeOut' }}
                      />
                    </div>
                  </div>

                  {/* Go to study session */}
                  {!ch.isCompleted && !ch.isClaimed && onGoToStudy && (
                    <MotionButton
                      onClick={onGoToStudy}
                      whileHover={{ scale: 1.01 }}
                      whileTap={{ scale: 0.98 }}
                      className="w-full py-2.5 rounded-xl text-sm font-semibold bg-[var(--accent-hex)] text-white hover:opacity-90 transition-opacity mb-2"
                    >
                      Start Study Session
                    </MotionButton>
                  )}

                  {/* Action / status */}
                  {ch.isCompleted && !ch.isClaimed && (
                    <MotionButton
                      onClick={async () => {
                        await ch.claimReward();
                        pointsReload?.();
                      }}
                      whileHover={{ scale: 1.01 }}
                      whileTap={{ scale: 0.98 }}
                      className="w-full py-2.5 rounded-xl text-sm font-bold bg-amber-500 text-white hover:bg-amber-600 transition-colors"
                    >
                      Claim Reward
                    </MotionButton>
                  )}
                  {ch.isClaimed && (
                    <div className="flex items-center justify-center gap-2 py-2">
                      <CheckCircle2 size={16} className="text-emerald-500" />
                      <span className="text-sm font-semibold text-emerald-600 dark:text-emerald-400">Completed</span>
                    </div>
                  )}
                </div>
              );
            })()}
          </MotionDiv>
        )}

        {/* ── 3. Personal Bests ── */}
        <MotionDiv
          initial={{ opacity: 0, y: 12 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.4, delay: 0.17 }}
          className="mb-6"
        >
          <h3 className="text-sm font-semibold uppercase tracking-widest text-zinc-400 dark:text-zinc-500 mb-3">
            Personal Bests
          </h3>
          <div className="flex gap-3 overflow-x-auto pb-1 -mx-1 px-1 scrollbar-none">
            {[
              { label: 'Best Day Points', value: personalBests.bestDayPoints, icon: Zap, color: '#f59e0b' },
              { label: 'Best Week Sessions', value: personalBests.bestWeekSessions, icon: Clock, color: '#3b82f6' },
              { label: 'Longest Streak', value: streak.longestStreak, icon: Flame, color: '#f97316' },
              { label: 'Best Day Sections', value: personalBests.bestDaySections, icon: BookOpen, color: '#14b8a6' },
            ].map((pb, i) => (
              <div
                key={i}
                className="flex-shrink-0 w-36 p-4 rounded-xl bg-white dark:bg-zinc-900 border border-zinc-200 dark:border-zinc-800"
              >
                <pb.icon size={16} style={{ color: pb.color }} className="mb-2" />
                <p className="text-xl font-bold text-zinc-800 dark:text-white">{pb.value}</p>
                <p className="text-[10px] text-zinc-400 dark:text-zinc-500 font-medium">{pb.label}</p>
              </div>
            ))}
          </div>
        </MotionDiv>

        {/* ── 4. Training Stats ── */}
        <MotionDiv
          initial={{ opacity: 0, y: 12 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.4, delay: 0.22 }}
          className="card-styled bg-white dark:bg-zinc-900 border border-zinc-200 dark:border-zinc-800 rounded-2xl p-6 mb-6"
        >
          <h3 className="text-sm font-semibold uppercase tracking-widest text-zinc-400 dark:text-zinc-500 mb-4">
            Training Stats
          </h3>
          <div className="grid grid-cols-2 sm:grid-cols-4 gap-4">
            {[
              { label: 'Sessions', value: totalTimetableSessions, icon: Clock },
              { label: 'Reflections', value: totalReflections, icon: PenLine },
              { label: 'Modules', value: `${modulesCompleted}/${totalModules}`, icon: BookOpen },
              { label: 'Categories', value: categoriesCompleted, icon: Layers },
            ].map((stat, i) => (
              <div key={i} className="text-center p-3 rounded-xl bg-zinc-50 dark:bg-zinc-800/30">
                <stat.icon size={16} className="text-zinc-400 dark:text-zinc-500 mx-auto mb-1.5" />
                <p className="text-lg font-bold text-zinc-800 dark:text-white">{stat.value}</p>
                <p className="text-[10px] text-zinc-400 dark:text-zinc-500 font-medium">{stat.label}</p>
              </div>
            ))}
          </div>
        </MotionDiv>

        {/* ── 5. Strategy Mastery ── */}
        {strategyMastery && (
          <MotionDiv
            initial={{ opacity: 0, y: 12 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.4, delay: 0.24 }}
            className="card-styled bg-white dark:bg-zinc-900 border border-zinc-200 dark:border-zinc-800 rounded-2xl p-6 mb-6"
          >
            <h3 className="text-sm font-semibold uppercase tracking-widest text-zinc-400 dark:text-zinc-500 mb-4">
              Strategy Mastery
            </h3>
            <div className="grid grid-cols-1 sm:grid-cols-2 gap-3">
              {STRATEGY_REGISTRY.map(strategy => {
                const record = strategyMastery[strategy.moduleId];
                const tier = record?.tier ?? 'none';
                const tierConfig = TIER_CONFIG[tier];
                const tierIndex = TIER_ORDER.indexOf(tier);
                const StrategyIcon = STRATEGY_ICONS[strategy.moduleId] || Brain;

                return (
                  <div
                    key={strategy.moduleId}
                    className={`p-4 rounded-xl border ${tierConfig.border} ${tierConfig.bg} transition-colors`}
                  >
                    <div className="flex items-center gap-3 mb-3">
                      <div className="w-8 h-8 rounded-lg bg-white dark:bg-zinc-800 flex items-center justify-center shrink-0">
                        <StrategyIcon size={16} className={tierConfig.color} />
                      </div>
                      <div className="flex-1 min-w-0">
                        <p className="text-sm font-semibold text-zinc-800 dark:text-white truncate">
                          {strategy.strategyName}
                        </p>
                        <span className={`text-[10px] font-bold uppercase tracking-wider ${tierConfig.color}`}>
                          {tierConfig.label}
                        </span>
                      </div>
                    </div>
                    {/* 4-step progress bar */}
                    <div className="grid grid-cols-4 gap-1">
                      {TIER_ORDER.map((t, i) => {
                        const filled = i <= tierIndex;
                        const segmentColor = filled
                          ? t === 'learned' ? 'bg-blue-500'
                          : t === 'practiced' ? 'bg-teal-500'
                          : t === 'applied' ? 'bg-amber-500'
                          : 'bg-purple-500'
                          : 'bg-zinc-200 dark:bg-zinc-700';
                        return (
                          <div
                            key={t}
                            className={`h-1.5 rounded-full ${segmentColor} transition-colors`}
                          />
                        );
                      })}
                    </div>
                  </div>
                );
              })}
            </div>
          </MotionDiv>
        )}

        {/* ── 6. Achievements Gallery ── */}
        <MotionDiv
          initial={{ opacity: 0, y: 12 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.4, delay: 0.27 }}
          className="card-styled bg-white dark:bg-zinc-900 border border-zinc-200 dark:border-zinc-800 rounded-2xl p-6 mb-6"
        >
          <AchievementGallery
            unlockedAchievements={unlockedAchievements}
            achievementTimestamps={gamificationState.achievementTimestamps}
          />
        </MotionDiv>

        {/* ── 7. North Star Progress ── */}
        {northStar && (
          <MotionDiv
            initial={{ opacity: 0, y: 12 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.4, delay: 0.32 }}
            className="card-styled bg-white dark:bg-zinc-900 border border-zinc-200 dark:border-zinc-800 rounded-2xl p-6 mb-6"
          >
            <div className="flex items-center gap-2 mb-4">
              <Star size={16} className="text-amber-500" />
              <h3 className="text-sm font-semibold uppercase tracking-widest text-zinc-400 dark:text-zinc-500">
                North Star
              </h3>
            </div>
            <p className="text-base font-semibold text-zinc-800 dark:text-white mb-2 italic">
              "{northStar.statement}"
            </p>
            <p className="text-xs text-zinc-400 dark:text-zinc-500 mb-4">
              Category: {northStar.category.replace('-', ' ')}
            </p>
            <MotionButton
              onClick={onOpenJourney}
              whileHover={{ scale: 1.01 }}
              whileTap={{ scale: 0.99 }}
              className="w-full flex items-center justify-between p-3.5 rounded-xl bg-[rgba(var(--accent),0.05)] dark:bg-[rgba(var(--accent),0.1)] hover:bg-[rgba(var(--accent),0.1)] dark:hover:bg-[rgba(var(--accent),0.15)] transition-colors group"
            >
              <div className="flex items-center gap-2">
                <Mountain size={16} className="text-[var(--accent-hex)]" />
                <span className="text-sm font-medium text-zinc-700 dark:text-zinc-300">Unlock Your Vision</span>
              </div>
              <ChevronRight size={14} className="text-[var(--accent-hex)] group-hover:translate-x-0.5 transition-transform" />
            </MotionButton>
          </MotionDiv>
        )}
      </div>
    </div>
  );
};

export default TrainingHub;
