/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 */

import React from 'react';
import { motion, useMotionValue, useTransform, animate, AnimatePresence } from 'framer-motion';
import { MotionDiv } from './Motion';
import {
  ArrowLeft, Flame, TrendingUp, Target, Zap, Award, Crown, Mountain,
  Footprints, Star, Brain, Repeat, Shuffle, HelpCircle,
  Compass, Sprout, Shield, Radar, ClipboardCheck, Trophy, ArrowRight, ChevronDown, Play,
} from 'lucide-react';
import { type GamificationState, generateWeeklyGoals, getWeekNumber, ATHLETE_RANKS } from '../gamificationConfig';
import PrimaryActionButton from './ui/PrimaryActionButton';
import { type StreakData } from '../hooks/useStreak';
import { type NorthStar, type UserProgress, type StrategyMasteryMap, type MasteryTier } from '../types';
import AchievementGallery from './AchievementGallery';
import { type CourseData } from './Library';
import { STRATEGY_REGISTRY } from '../utils/strategyRegistry';
import { type WeeklyChallengeState } from '../hooks/useWeeklyChallenge';

// ─── Reusable Progress Ring ─────────────────────────────────

const ProgressRing: React.FC<{
  progress: number; // 0-100
  size: number;
  strokeWidth: number;
  color: string;
  trackColor?: string;
  children?: React.ReactNode;
}> = ({ progress, size, strokeWidth, color, trackColor = '#E8E4DE', children }) => {
  const radius = (size - strokeWidth) / 2;
  const circumference = 2 * Math.PI * radius;
  const offset = circumference * (1 - Math.min(100, progress) / 100);

  return (
    <div className="relative" style={{ width: size, height: size }}>
      <svg width={size} height={size} className="-rotate-90">
        {/* Track */}
        <circle cx={size / 2} cy={size / 2} r={radius} fill="none" stroke={trackColor} strokeWidth={strokeWidth} />
        {/* Progress arc */}
        <motion.circle
          cx={size / 2} cy={size / 2} r={radius}
          fill="none" stroke={color} strokeWidth={strokeWidth}
          strokeLinecap="round"
          strokeDasharray={circumference}
          initial={{ strokeDashoffset: circumference }}
          animate={{ strokeDashoffset: offset }}
          transition={{ duration: 1.5, ease: [0.16, 1, 0.3, 1] }}
        />
      </svg>
      {/* Center content */}
      <div className="absolute inset-0 flex flex-col items-center justify-center">
        {children}
      </div>
    </div>
  );
};

// ─── Config ─────────────────────────────────────────────────

const RANK_ICONS: Record<string, React.ElementType> = {
  Footprints, Flame, TrendingUp, Target, Zap, Award, Crown, Mountain,
};

const TIER_ORDER: MasteryTier[] = ['habitual', 'applied', 'practiced', 'learned'];
const TIER_LABELS: Record<MasteryTier, string> = { none: '', learned: 'Learned', practiced: 'Practiced', applied: 'Applied', habitual: 'Habitual' };
const TIER_COLORS: Record<MasteryTier, string> = { none: '#A8A29E', learned: '#3B82F6', practiced: '#2A7D6F', applied: '#F59E0B', habitual: '#7C3AED' };
const TIER_INDEX: Record<MasteryTier, number> = { none: -1, learned: 0, practiced: 1, applied: 2, habitual: 3 };

const STRATEGY_ICONS: Record<string, React.ElementType> = {
  'mastering-active-recall-protocol': Brain, 'mastering-spaced-repetition-protocol': Repeat,
  'mastering-interleaving-protocol': Shuffle, 'elaborative-interrogation-protocol': HelpCircle,
  'agency-protocol': Compass, 'growth-mindset-protocol': Sprout, 'digital-distraction-protocol': Shield,
  'learning-radar-protocol': Radar, 'exam-hall-strategies-protocol': ClipboardCheck,
};

const CHALLENGE_ICONS: Record<string, React.ElementType> = {
  Brain, Repeat, Shuffle, HelpCircle, Compass, Sprout, Shield, Radar, ClipboardCheck, Zap, Trophy,
};

const GOAL_COLORS = ['#2A7D6F', '#E67E22', '#6366f1'];

// ─── Component ──────────────────────────────────────────────

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
  uid?: string;
}

const TrainingHub: React.FC<TrainingHubProps> = ({
  gamificationState, streak, pointsBalance, northStar, onBack, onOpenJourney,
  userProgress, allCourses, strategyMastery, weeklyChallenge, pointsReload, onGoToStudy, uid,
}) => {
  const { currentRank, nextRank, rankProgress, totalPointsEarned, unlockedAchievements, weeklyGoalProgress, weekStartDate, personalBests } = gamificationState;
  const weekNumber = getWeekNumber();
  const weeklyGoals = generateWeeklyGoals(currentRank.id, weekNumber);
  const RankIcon = RANK_ICONS[currentRank.icon] || Star;
  const modulesCompleted = allCourses.filter(c => { const p = userProgress[c.id]; return p && p.unlockedSection >= c.sectionsCount; }).length;

  const [strategyOpen, setStrategyOpen] = React.useState(false);
  const [achievementsOpen, setAchievementsOpen] = React.useState(false);

  // Days until weekly reset (Monday)
  const now = new Date();
  const dayOfWeek = now.getDay();
  const daysUntilReset = dayOfWeek === 0 ? 1 : 8 - dayOfWeek;

  const stagger = (i: number) => ({ initial: { opacity: 0, y: 16 }, animate: { opacity: 1, y: 0 }, transition: { delay: i * 0.06, duration: 0.4, ease: [0.16, 1, 0.3, 1] as number[] } });

  return (
    <div className="min-h-screen bg-[#FDF8F0] dark:bg-zinc-950">

      {/* ── 1. Coloured hero section: header + ring + stat pills ── */}
      <div className="relative" style={{ backgroundColor: currentRank.colorHex }}>
        {/* Header on colour */}
        <div className="px-6 py-4 flex items-center gap-3">
          <button onClick={onBack} className="w-9 h-9 rounded-xl flex items-center justify-center transition-colors" style={{ backgroundColor: 'rgba(255,255,255,0.15)' }}>
            <ArrowLeft size={18} style={{ color: '#fff' }} />
          </button>
          <h1 className="font-serif text-lg font-semibold text-white">Training Hub</h1>
        </div>

        <div className="px-6 max-w-2xl mx-auto py-12 md:py-16">

          {/* The Ring — white on rank colour */}
          <MotionDiv {...stagger(0)} className="flex flex-col items-center">
            <ProgressRing
              progress={rankProgress}
              size={typeof window !== 'undefined' && window.innerWidth < 768 ? 220 : 280}
              strokeWidth={16}
              color="#FFFFFF"
              trackColor="rgba(255,255,255,0.2)"
            >
              <RankIcon size={36} style={{ color: '#fff' }} />
              <span className="text-sm font-semibold mt-1 text-white">{currentRank.title}</span>
            </ProgressRing>
            <p className="text-sm mt-4 font-apercu tabular-nums" style={{ color: 'rgba(255,255,255,0.6)' }}>
              {nextRank
                ? `${totalPointsEarned} / ${nextRank.minPoints} XP`
                : 'Legend — Maximum rank'
              }
            </p>
          </MotionDiv>

          {/* Three stat pills — translucent white on colour */}
          <MotionDiv {...stagger(1)} className="grid grid-cols-3 gap-3 mt-8">
            <div className="rounded-2xl px-4 py-3 text-center" style={{ backgroundColor: 'rgba(255,255,255,0.15)' }}>
              <p className="text-xl font-apercu font-bold text-white">{streak.currentStreak}</p>
              <p className="text-[10px] uppercase tracking-widest font-semibold mt-0.5" style={{ color: 'rgba(255,255,255,0.7)' }}>Day Streak</p>
            </div>
            <div className="rounded-2xl px-4 py-3 text-center" style={{ backgroundColor: 'rgba(255,255,255,0.15)' }}>
              <p className="text-xl font-apercu font-bold text-white">{totalPointsEarned}</p>
              <p className="text-[10px] uppercase tracking-widest font-semibold mt-0.5" style={{ color: 'rgba(255,255,255,0.7)' }}>Total XP</p>
            </div>
            <div className="rounded-2xl px-4 py-3 text-center" style={{ backgroundColor: 'rgba(255,255,255,0.15)' }}>
              <p className="text-xl font-apercu font-bold text-white">{modulesCompleted}/{allCourses.length}</p>
              <p className="text-[10px] uppercase tracking-widest font-semibold mt-0.5" style={{ color: 'rgba(255,255,255,0.7)' }}>Modules</p>
            </div>
          </MotionDiv>
        </div>

        {/* SVG arc transition into cream */}
        <div className="absolute bottom-0 left-0 right-0" style={{ transform: 'translateY(1px)' }}>
          <svg viewBox="0 0 1440 60" preserveAspectRatio="none" className="w-full block" style={{ height: 60 }}>
            <path d="M0,0 C480,60 960,60 1440,0 L1440,60 L0,60 Z" className="fill-[#FDF8F0] dark:fill-zinc-950" />
          </svg>
        </div>
      </div>

      <div className="px-6 pb-24 max-w-2xl mx-auto bg-[#FDF8F0] dark:bg-zinc-950">

        {/* ── Start Studying CTA ── */}
        {onGoToStudy && (
          <MotionDiv {...stagger(1.5)} className="flex justify-center mt-8">
            <PrimaryActionButton label="Start Studying" onClick={onGoToStudy} icon={Play} />
          </MotionDiv>
        )}

        {/* ── 4. This Week ── */}
        <MotionDiv {...stagger(2)} className="mt-12 md:mt-16">
          <div className="flex items-center justify-between mb-6">
            <p className="text-xs uppercase tracking-[0.2em] font-semibold text-[#A8A29E] dark:text-zinc-500">This Week</p>
            <p className="text-xs text-[#C4C0BC] dark:text-zinc-600">Resets in {daysUntilReset}d</p>
          </div>

          {/* Weekly Goal Rings */}
          <div className="flex justify-center gap-8 mb-6">
            {weeklyGoals.map((goal, gi) => {
              const current = weeklyGoalProgress[goal.metric] ?? 0;
              const pct = Math.min(100, Math.round((current / goal.target) * 100));
              return (
                <div key={goal.id} className="flex flex-col items-center">
                  <ProgressRing progress={pct} size={56} strokeWidth={6} color={GOAL_COLORS[gi % GOAL_COLORS.length]} trackColor={`${GOAL_COLORS[gi % GOAL_COLORS.length]}30`}>
                    <span className="text-xs font-apercu font-bold tabular-nums text-[#1A1A1A] dark:text-white">{current}/{goal.target}</span>
                  </ProgressRing>
                  <span className="text-[10px] mt-2 text-[#A8A29E] dark:text-zinc-500">{goal.label}</span>
                </div>
              );
            })}
          </div>

          {/* Weekly Bonus dots */}
          <div className="flex items-center justify-center gap-2 mb-8">
            {weeklyGoals.map((goal, gi) => {
              const met = (weeklyGoalProgress[goal.metric] ?? 0) >= goal.target;
              return <div key={gi} className={`w-3 h-3 rounded-full ${met ? 'bg-[#2A7D6F]' : 'bg-[#E8E4DE] dark:bg-zinc-700'}`} />;
            })}
            <span className="text-xs font-semibold ml-2" style={{ color: '#2A7D6F' }}>
              {weeklyGoals.filter(g => (weeklyGoalProgress[g.metric] ?? 0) >= g.target).length === 3
                ? 'Bonus earned!'
                : '+50 pts next'}
            </span>
          </div>

          {/* Weekly Challenge */}
          {weeklyChallenge?.isLoaded && !weeklyChallenge.isClaimed && (() => {
            const ch = weeklyChallenge;
            const CIcon = CHALLENGE_ICONS[ch.challenge.icon] || Trophy;
            const pct = Math.min(100, Math.round((ch.current / ch.challenge.target) * 100));
            return (
              <div className="flex items-center gap-3 rounded-2xl px-5 py-4" style={{ backgroundColor: 'rgba(42,125,111,0.06)' }}>
                <div className="w-10 h-10 rounded-xl flex items-center justify-center shrink-0" style={{ backgroundColor: 'rgba(42,125,111,0.12)' }}>
                  <CIcon size={20} style={{ color: '#2A7D6F' }} />
                </div>
                <div className="flex-1 min-w-0">
                  <p className="text-sm font-semibold truncate text-[#1A1A1A] dark:text-white">{ch.challenge.title}</p>
                  <p className="text-xs text-[#A8A29E] dark:text-zinc-500">{ch.challenge.description || `${ch.current}/${ch.challenge.target}`}</p>
                </div>
                {ch.isCompleted && !ch.isClaimed ? (
                  <button onClick={async () => { await ch.claimReward(); pointsReload?.(); }} className="px-4 py-2 rounded-full text-xs font-bold text-white shrink-0" style={{ backgroundColor: '#2A7D6F' }}>
                    Claim
                  </button>
                ) : (
                  <ProgressRing progress={pct} size={40} strokeWidth={4} color="#2A7D6F">
                    <span className="text-[9px] font-apercu font-bold" style={{ color: '#2A7D6F' }}>{pct}%</span>
                  </ProgressRing>
                )}
              </div>
            );
          })()}
        </MotionDiv>

        {/* ── 5. Strategy Mastery (collapsible) ── */}
        <MotionDiv {...stagger(3)} className="mt-12 md:mt-16">
          <button onClick={() => setStrategyOpen(o => !o)} className="w-full flex items-center justify-between cursor-pointer">
            <p className="text-xs uppercase tracking-[0.2em] font-semibold text-[#A8A29E] dark:text-zinc-500">Strategy Mastery</p>
            <div className="flex items-center gap-2">
              <p className="text-xs text-[#C4C0BC] dark:text-zinc-600">
                {strategyMastery ? STRATEGY_REGISTRY.filter(s => (strategyMastery[s.moduleId]?.tier ?? 'none') !== 'none').length : 0}/{STRATEGY_REGISTRY.length}
              </p>
              <motion.div animate={{ rotate: strategyOpen ? 180 : 0 }} transition={{ duration: 0.3, ease: [0.16, 1, 0.3, 1] }}>
                <ChevronDown size={16} className="text-[#A8A29E] dark:text-zinc-500" />
              </motion.div>
            </div>
          </button>

          <AnimatePresence initial={false}>
            {strategyOpen && (
              <motion.div
                initial={{ height: 0, opacity: 0 }}
                animate={{ height: 'auto', opacity: 1 }}
                exit={{ height: 0, opacity: 0 }}
                transition={{ duration: 0.3, ease: [0.16, 1, 0.3, 1] }}
                style={{ overflow: 'hidden' }}
              >
                <div className="pt-6">
                  {strategyMastery && STRATEGY_REGISTRY.some(s => (strategyMastery[s.moduleId]?.tier ?? 'none') !== 'none') ? (
                    <div>
                      {STRATEGY_REGISTRY
                        .filter(s => (strategyMastery[s.moduleId]?.tier ?? 'none') !== 'none')
                        .sort((a, b) => TIER_INDEX[strategyMastery[b.moduleId]?.tier ?? 'none'] - TIER_INDEX[strategyMastery[a.moduleId]?.tier ?? 'none'])
                        .map((strategy, si, arr) => {
                          const tier = strategyMastery[strategy.moduleId]?.tier ?? 'none';
                          const tierIdx = TIER_INDEX[tier];
                          const Icon = STRATEGY_ICONS[strategy.moduleId] || Brain;
                          return (
                            <div key={strategy.moduleId} className={`py-3 ${si < arr.length - 1 ? 'border-b border-[#F0EFED] dark:border-zinc-800' : ''}`}>
                              <div className="flex items-center gap-2.5">
                                <div className="w-4 h-4 rounded-full shrink-0" style={{ backgroundColor: TIER_COLORS[tier] }} />
                                <Icon size={14} className="text-[#78716C] dark:text-zinc-400" />
                                <span className="text-sm flex-1 text-[#1A1A1A] dark:text-white">{strategy.strategyName}</span>
                                <span className="text-[10px] font-semibold uppercase" style={{ color: TIER_COLORS[tier] }}>{TIER_LABELS[tier]}</span>
                              </div>
                              {/* 4-segment tier bar */}
                              <div className="flex gap-0.5 mt-2 ml-[22px]">
                                {[0, 1, 2, 3].map(seg => (
                                  <div key={seg} className={`flex-1 h-1 rounded-full ${seg <= tierIdx ? '' : 'bg-[#E8E4DE] dark:bg-zinc-700'}`} style={seg <= tierIdx ? { backgroundColor: TIER_COLORS[tier] } : undefined} />
                                ))}
                              </div>
                            </div>
                          );
                        })}
                    </div>
                  ) : (
                    <p className="text-sm italic text-[#A8A29E] dark:text-zinc-500">
                      Complete modules, then use strategies in study sessions.
                    </p>
                  )}
                </div>
              </motion.div>
            )}
          </AnimatePresence>
        </MotionDiv>

        {/* ── 6. Achievements (collapsible) ── */}
        <MotionDiv {...stagger(4)} className="mt-12 md:mt-16">
          <button onClick={() => setAchievementsOpen(o => !o)} className="w-full flex items-center justify-between cursor-pointer">
            <p className="text-xs uppercase tracking-[0.2em] font-semibold text-[#A8A29E] dark:text-zinc-500">Achievements</p>
            <div className="flex items-center gap-2">
              <p className="text-xs text-[#C4C0BC] dark:text-zinc-600">{unlockedAchievements.length}/58</p>
              <motion.div animate={{ rotate: achievementsOpen ? 180 : 0 }} transition={{ duration: 0.3, ease: [0.16, 1, 0.3, 1] }}>
                <ChevronDown size={16} className="text-[#A8A29E] dark:text-zinc-500" />
              </motion.div>
            </div>
          </button>

          <AnimatePresence initial={false}>
            {achievementsOpen && (
              <motion.div
                initial={{ height: 0, opacity: 0 }}
                animate={{ height: 'auto', opacity: 1 }}
                exit={{ height: 0, opacity: 0 }}
                transition={{ duration: 0.3, ease: [0.16, 1, 0.3, 1] }}
                style={{ overflow: 'hidden' }}
              >
                <div className="pt-6">
                  <AchievementGallery unlockedAchievements={unlockedAchievements} achievementTimestamps={gamificationState.achievementTimestamps} />
                </div>
              </motion.div>
            )}
          </AnimatePresence>
        </MotionDiv>

        {/* ── 7. Personal Bests ── */}
        {personalBests && Object.values(personalBests).some(v => v > 0) && (
          <MotionDiv {...stagger(5)} className="mt-12 md:mt-16">
            <p className="text-xs uppercase tracking-[0.2em] font-semibold mb-6 text-[#A8A29E] dark:text-zinc-500">Personal Bests</p>
            <div className="flex gap-8 flex-wrap">
              {[
                { key: 'bestDayPoints', label: 'Day Pts', color: '#2A7D6F' },
                { key: 'bestDaySections', label: 'Day Sections', color: '#E67E22' },
                { key: 'bestWeekPoints', label: 'Week Pts', color: '#6C5CE7' },
                { key: 'bestWeekSessions', label: 'Week Sessions', color: '#E84393' },
              ].filter(pb => (personalBests as any)[pb.key] > 0).map(pb => (
                <div key={pb.key}>
                  <p className="text-2xl font-apercu font-bold" style={{ color: pb.color }}>{(personalBests as any)[pb.key]}</p>
                  <p className="text-[10px] uppercase tracking-widest mt-0.5 text-[#A8A29E] dark:text-zinc-500">{pb.label}</p>
                </div>
              ))}
            </div>
          </MotionDiv>
        )}
      </div>

      {/* ── 8. North Star footer ── */}
      {northStar && (
        <MotionDiv {...stagger(6)} className="mt-16 py-12 px-6 text-center" style={{ backgroundColor: `${currentRank.colorHex}14` }}>
          <div className="max-w-lg mx-auto">
            <p className="font-serif italic text-base leading-relaxed text-[#57534E] dark:text-zinc-400">
              &ldquo;{northStar.statement}&rdquo;
            </p>
            <button onClick={onOpenJourney} className="mt-3 text-xs font-semibold inline-flex items-center gap-1 group" style={{ color: currentRank.colorHex }}>
              My Journey <ArrowRight size={12} className="group-hover:translate-x-0.5 transition-transform" />
            </button>
          </div>
        </MotionDiv>
      )}
    </div>
  );
};

export default TrainingHub;
