/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 */

import React from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { MotionDiv } from './Motion';
import {
  ArrowLeft, Flame, TrendingUp, Target, Zap, Award, Crown, Mountain,
  Footprints, Star, Brain, Repeat, Shuffle, HelpCircle,
  Compass, Sprout, Shield, Radar, ClipboardCheck, Trophy, ArrowRight, ChevronDown, Play,
} from 'lucide-react';
import { type GamificationState, generateWeeklyGoals, getWeekNumber } from '../gamificationConfig';
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

const _TIER_ORDER: MasteryTier[] = ['habitual', 'applied', 'practiced', 'learned'];
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
  gamificationState, streak, _pointsBalance, northStar, onBack, onOpenJourney,
  userProgress, allCourses, strategyMastery, weeklyChallenge, pointsReload, onGoToStudy, _uid,
}) => {
  const { currentRank, nextRank, rankProgress, totalPointsEarned, unlockedAchievements, weeklyGoalProgress, _weekStartDate, personalBests } = gamificationState;
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
      <div className="relative overflow-hidden" style={{ backgroundColor: currentRank.colorHex }}>
        {/* Decorative blobs — spread apart, no overlapping */}
        <div className="absolute pointer-events-none" style={{ top: -70, right: -50, width: 220, height: 220, borderRadius: '50%', background: 'rgba(255,255,255,0.07)' }} />
        <div className="absolute pointer-events-none" style={{ bottom: 60, left: -50, width: 160, height: 160, borderRadius: '50%', background: 'rgba(0,0,0,0.05)' }} />
        <div className="absolute pointer-events-none" style={{ top: '45%', left: '55%', width: 90, height: 90, borderRadius: '50%', background: 'rgba(255,255,255,0.05)' }} />
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
          <div className="flex items-center justify-between mb-4">
            <p className="text-xs uppercase tracking-[0.2em] font-semibold text-[#A8A29E] dark:text-zinc-500">This Week</p>
            <p className="text-xs text-[#C4C0BC] dark:text-zinc-600">Resets in {daysUntilReset}d</p>
          </div>

          <div className="rounded-2xl bg-[#FEFDFB] dark:bg-zinc-900 border border-[#EDEBE8] dark:border-zinc-800 px-5 py-6" style={{ boxShadow: '0 1px 4px rgba(28,25,23,0.04)' }}>
            {/* Weekly Goal Rings */}
            <div className="flex justify-center gap-8 mb-5">
              {weeklyGoals.map((goal, gi) => {
                const current = weeklyGoalProgress[goal.metric] ?? 0;
                const pct = Math.min(100, Math.round((current / goal.target) * 100));
                return (
                  <div key={goal.id} className="flex flex-col items-center">
                    <ProgressRing progress={pct} size={56} strokeWidth={6} color={GOAL_COLORS[gi % GOAL_COLORS.length]} trackColor={`${GOAL_COLORS[gi % GOAL_COLORS.length]}30`}>
                      <span className="text-xs font-apercu font-bold tabular-nums text-[#1A1A1A] dark:text-white">{current}/{goal.target}</span>
                    </ProgressRing>
                    <span className="text-[10px] mt-2 text-[#78716C] dark:text-zinc-400">{goal.label}</span>
                  </div>
                );
              })}
            </div>

            {/* Weekly Bonus — stamp row */}
            <div className="flex items-center justify-center gap-3 pt-4 mt-4" style={{ borderTop: '1px solid #EDEBE8' }}>
              {weeklyGoals.map((goal, gi) => {
                const met = (weeklyGoalProgress[goal.metric] ?? 0) >= goal.target;
                return (
                  <div key={gi} className="flex items-center justify-center w-7 h-7 rounded-lg" style={{ backgroundColor: met ? '#2A7D6F' : '#E8E4DE' }}>
                    {met ? (
                      <svg width="14" height="14" viewBox="0 0 14 14" fill="none"><path d="M3 7L6 10L11 4" stroke="#fff" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"/></svg>
                    ) : (
                      <span className="text-[10px] font-bold text-[#A8A29E]">{gi + 1}</span>
                    )}
                  </div>
                );
              })}
              <div className="rounded-lg px-3 py-1.5" style={{ backgroundColor: 'rgba(42,125,111,0.1)' }}>
                <span className="text-xs font-bold" style={{ color: '#2A7D6F' }}>
                  {weeklyGoals.filter(g => (weeklyGoalProgress[g.metric] ?? 0) >= g.target).length === 3
                    ? 'Bonus earned! +50 pts'
                    : '+50 pts bonus'}
                </span>
              </div>
            </div>
          </div>

          {/* Weekly Challenge */}
          {weeklyChallenge?.isLoaded && !weeklyChallenge.isClaimed && (() => {
            const ch = weeklyChallenge;
            const CIcon = CHALLENGE_ICONS[ch.challenge.icon] || Trophy;
            const pct = Math.min(100, Math.round((ch.current / ch.challenge.target) * 100));
            return (
              <div className="flex items-center gap-3 rounded-2xl px-5 py-4 mt-3 bg-[#FEFDFB] dark:bg-zinc-900 border border-[#EDEBE8] dark:border-zinc-800" style={{ boxShadow: '0 1px 4px rgba(28,25,23,0.04)' }}>
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

        {/* ── 5. Strategy Mastery (collapsible in card) ── */}
        {(() => {
          const masteredCount = strategyMastery ? STRATEGY_REGISTRY.filter(s => (strategyMastery[s.moduleId]?.tier ?? 'none') !== 'none').length : 0;
          const masteryPct = Math.round((masteredCount / STRATEGY_REGISTRY.length) * 100);
          return (
            <MotionDiv {...stagger(3)} className="mt-8">
              <div className="rounded-2xl bg-[#FEFDFB] dark:bg-zinc-900 border border-[#EDEBE8] dark:border-zinc-800 overflow-hidden" style={{ boxShadow: '0 1px 4px rgba(28,25,23,0.04)' }}>
                <button onClick={() => setStrategyOpen(o => !o)} className="w-full flex items-center gap-3 px-5 py-4 cursor-pointer">
                  <div className="w-9 h-9 rounded-xl shrink-0 flex items-center justify-center" style={{ backgroundColor: 'rgba(107,92,231,0.1)' }}>
                    <Brain size={18} style={{ color: '#6C5CE7' }} />
                  </div>
                  <div className="flex-1 min-w-0 text-left">
                    <p className="text-sm font-semibold text-[#1A1A1A] dark:text-white">Strategy Mastery</p>
                    <div className="flex items-center gap-2 mt-1.5">
                      <div className="flex-1 h-1.5 rounded-full bg-[#E8E4DE] dark:bg-zinc-700 overflow-hidden" style={{ maxWidth: 120 }}>
                        <div className="h-full rounded-full" style={{ backgroundColor: '#6C5CE7', width: `${masteryPct}%` }} />
                      </div>
                      <span className="text-[10px] font-semibold text-[#A8A29E] dark:text-zinc-500">{masteredCount}/{STRATEGY_REGISTRY.length}</span>
                    </div>
                  </div>
                  <motion.div animate={{ rotate: strategyOpen ? 180 : 0 }} transition={{ duration: 0.3, ease: [0.16, 1, 0.3, 1] }}>
                    <ChevronDown size={16} className="text-[#A8A29E] dark:text-zinc-500" />
                  </motion.div>
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
                      <div className="px-5 pb-4 pt-1" style={{ borderTop: '1px solid #EDEBE8' }}>
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
                                  <div key={strategy.moduleId} className={`py-3.5 ${si < arr.length - 1 ? 'border-b border-[#F0EFED] dark:border-zinc-800' : ''}`}>
                                    <div className="flex items-center gap-3">
                                      <div className="w-8 h-8 rounded-xl shrink-0 flex items-center justify-center" style={{ backgroundColor: `${TIER_COLORS[tier]}14` }}>
                                        <Icon size={16} style={{ color: TIER_COLORS[tier] }} />
                                      </div>
                                      <span className="text-sm flex-1 font-medium text-[#1A1A1A] dark:text-white">{strategy.strategyName}</span>
                                      <span className="text-[10px] font-semibold uppercase" style={{ color: TIER_COLORS[tier] }}>{TIER_LABELS[tier]}</span>
                                    </div>
                                    <div className="flex gap-1 mt-2.5 ml-11">
                                      {[0, 1, 2, 3].map(seg => (
                                        <div key={seg} className={`flex-1 h-1.5 rounded-full ${seg <= tierIdx ? '' : 'bg-[#E8E4DE] dark:bg-zinc-700'}`} style={seg <= tierIdx ? { backgroundColor: TIER_COLORS[tier] } : undefined} />
                                      ))}
                                    </div>
                                  </div>
                                );
                              })}
                          </div>
                        ) : (
                          <p className="text-sm italic py-3 text-[#A8A29E] dark:text-zinc-500">
                            Complete modules, then use strategies in study sessions.
                          </p>
                        )}
                      </div>
                    </motion.div>
                  )}
                </AnimatePresence>
              </div>
            </MotionDiv>
          );
        })()}

        {/* ── 6. Achievements (collapsible in card) ── */}
        {(() => {
          const achievePct = Math.round((unlockedAchievements.length / 58) * 100);
          return (
            <MotionDiv {...stagger(4)} className="mt-4">
              <div className="rounded-2xl bg-[#FEFDFB] dark:bg-zinc-900 border border-[#EDEBE8] dark:border-zinc-800 overflow-hidden" style={{ boxShadow: '0 1px 4px rgba(28,25,23,0.04)' }}>
                <button onClick={() => setAchievementsOpen(o => !o)} className="w-full flex items-center gap-3 px-5 py-4 cursor-pointer">
                  <div className="w-9 h-9 rounded-xl shrink-0 flex items-center justify-center" style={{ backgroundColor: 'rgba(230,126,34,0.1)' }}>
                    <Award size={18} style={{ color: '#E67E22' }} />
                  </div>
                  <div className="flex-1 min-w-0 text-left">
                    <p className="text-sm font-semibold text-[#1A1A1A] dark:text-white">Achievements</p>
                    <div className="flex items-center gap-2 mt-1.5">
                      <div className="flex-1 h-1.5 rounded-full bg-[#E8E4DE] dark:bg-zinc-700 overflow-hidden" style={{ maxWidth: 120 }}>
                        <div className="h-full rounded-full" style={{ backgroundColor: '#E67E22', width: `${achievePct}%` }} />
                      </div>
                      <span className="text-[10px] font-semibold text-[#A8A29E] dark:text-zinc-500">{unlockedAchievements.length}/58</span>
                    </div>
                  </div>
                  <motion.div animate={{ rotate: achievementsOpen ? 180 : 0 }} transition={{ duration: 0.3, ease: [0.16, 1, 0.3, 1] }}>
                    <ChevronDown size={16} className="text-[#A8A29E] dark:text-zinc-500" />
                  </motion.div>
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
                      <div className="px-5 pb-5 pt-1" style={{ borderTop: '1px solid #EDEBE8' }}>
                        <AchievementGallery unlockedAchievements={unlockedAchievements} achievementTimestamps={gamificationState.achievementTimestamps} />
                      </div>
                    </motion.div>
                  )}
                </AnimatePresence>
              </div>
            </MotionDiv>
          );
        })()}

        {/* ── 7. Personal Bests ── */}
        {personalBests && Object.values(personalBests).some(v => v > 0) && (
          <MotionDiv {...stagger(5)} className="mt-12 md:mt-16">
            <p className="text-xs uppercase tracking-[0.2em] font-semibold mb-4 text-[#A8A29E] dark:text-zinc-500">Personal Bests</p>
            <div className="grid grid-cols-2 gap-3">
              {[
                { key: 'bestDayPoints', label: 'Best Day Points', color: '#2A7D6F' },
                { key: 'bestDaySections', label: 'Best Day Sections', color: '#E67E22' },
                { key: 'bestWeekPoints', label: 'Best Week Points', color: '#6C5CE7' },
                { key: 'bestWeekSessions', label: 'Best Week Sessions', color: '#E84393' },
              ].filter(pb => (personalBests as any)[pb.key] > 0).map(pb => (
                <div
                  key={pb.key}
                  className="rounded-2xl bg-[#FEFDFB] dark:bg-zinc-900 border border-[#EDEBE8] dark:border-zinc-800 px-4 py-4"
                  style={{ boxShadow: '0 1px 4px rgba(28,25,23,0.04)' }}
                >
                  <div className="w-8 h-8 rounded-xl flex items-center justify-center mb-3" style={{ backgroundColor: `${pb.color}14` }}>
                    <Trophy size={16} style={{ color: pb.color }} />
                  </div>
                  <p className="text-2xl font-apercu font-bold text-[#1A1A1A] dark:text-white">{(personalBests as any)[pb.key]}</p>
                  <p className="text-[11px] mt-1 text-[#A8A29E] dark:text-zinc-500">{pb.label}</p>
                </div>
              ))}
            </div>
          </MotionDiv>
        )}
      </div>

      {/* ── 8. North Star footer — rank colour environment ── */}
      {northStar && (
        <MotionDiv {...stagger(6)} className="relative overflow-hidden">
          {/* Wave transition from cream into colour */}
          <div style={{ backgroundColor: currentRank.colorHex }}>
            <svg viewBox="0 0 1440 60" preserveAspectRatio="none" className="w-full block" style={{ height: 60, transform: 'translateY(-1px)' }}>
              <path d="M0,60 C480,0 960,0 1440,60 L1440,0 L0,0 Z" className="fill-[#FDF8F0] dark:fill-zinc-950" />
            </svg>
          </div>

          <div className="relative" style={{ backgroundColor: currentRank.colorHex }}>
            {/* Decorative blobs — partially off-edge, clipped by outer wrapper */}
            <div className="absolute pointer-events-none" style={{ top: -40, right: -30, width: 140, height: 140, borderRadius: '50%', background: 'rgba(255,255,255,0.08)' }} />
            <div className="absolute pointer-events-none" style={{ bottom: -20, left: -20, width: 100, height: 100, borderRadius: '50%', background: 'rgba(0,0,0,0.05)' }} />

            <div className="relative z-10 pt-4 pb-16 px-6 text-center">
              <div className="max-w-md mx-auto">
                <div className="w-10 h-10 rounded-full mx-auto mb-4 flex items-center justify-center" style={{ backgroundColor: 'rgba(255,255,255,0.18)' }}>
                  <Compass size={20} style={{ color: '#fff' }} />
                </div>
                <p className="text-[11px] uppercase tracking-[0.14em] font-semibold mb-3" style={{ color: 'rgba(255,255,255,0.5)' }}>Your North Star</p>
                <p className="font-serif italic text-lg leading-relaxed text-white">
                  &ldquo;{northStar.statement}&rdquo;
                </p>
                <button onClick={onOpenJourney} className="mt-5 text-xs font-semibold inline-flex items-center gap-1.5 group px-4 py-2 rounded-full transition-colors" style={{ backgroundColor: 'rgba(255,255,255,0.18)', color: '#fff' }}>
                  My Journey <ArrowRight size={12} className="group-hover:translate-x-0.5 transition-transform" />
                </button>
              </div>
            </div>
          </div>
        </MotionDiv>
      )}
    </div>
  );
};

export default TrainingHub;
