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

  const now = new Date();
  const dayOfWeek = now.getDay();
  const daysUntilReset = dayOfWeek === 0 ? 1 : 8 - dayOfWeek;

  const stagger = (i: number) => ({ initial: { opacity: 0, y: 16 }, animate: { opacity: 1, y: 0 }, transition: { delay: i * 0.06, duration: 0.4, ease: [0.16, 1, 0.3, 1] as number[] } });

  return (
    <div className="min-h-screen bg-[#FDF8F0] dark:bg-zinc-950">

      {/* ── Hero: dark banner with rank + stats ── */}
      <div className="relative overflow-hidden" style={{ background: `linear-gradient(135deg, ${currentRank.colorHex} 0%, ${currentRank.colorHex}dd 100%)` }}>
        {/* Decorative circles */}
        <div className="absolute pointer-events-none" style={{ top: -60, right: -40, width: 200, height: 200, borderRadius: '50%', background: 'rgba(255,255,255,0.1)' }} />
        <div className="absolute pointer-events-none" style={{ bottom: -30, left: -30, width: 120, height: 120, borderRadius: '50%', background: 'rgba(255,255,255,0.07)' }} />

        {/* Header */}
        <div className="px-6 py-4 flex items-center gap-3">
          <button onClick={onBack} className="w-9 h-9 rounded-xl flex items-center justify-center transition-colors" style={{ backgroundColor: 'rgba(255,255,255,0.08)' }}>
            <ArrowLeft size={18} color="#fff" />
          </button>
          <h1 style={{ fontFamily: "'Source Serif 4', serif", fontSize: '18px', fontWeight: 600, color: '#fff' }}>Training Hub</h1>
        </div>

        {/* Rank + Progress */}
        <div className="px-6 max-w-3xl mx-auto pb-8 pt-4">
          <MotionDiv {...stagger(0)} className="flex items-center gap-5">
            {/* Rank badge */}
            <div
              className="w-16 h-16 rounded-2xl flex items-center justify-center shrink-0"
              style={{ backgroundColor: 'rgba(255,255,255,0.25)', border: '2px solid rgba(255,255,255,0.3)' }}
            >
              <RankIcon size={28} color="#fff" />
            </div>

            {/* Rank info + bar */}
            <div className="flex-1 min-w-0">
              <div className="flex items-baseline gap-2">
                <p style={{ fontFamily: "'Source Serif 4', serif", fontSize: '22px', fontWeight: 700, color: '#fff' }}>
                  {currentRank.title}
                </p>
                <span style={{ fontFamily: "'DM Sans', sans-serif", fontSize: '12px', color: 'rgba(255,255,255,0.4)' }}>
                  {nextRank ? `${totalPointsEarned} / ${nextRank.minPoints} XP` : 'Max rank'}
                </span>
              </div>
              {/* Progress bar */}
              <div className="mt-2 h-2 rounded-full overflow-hidden" style={{ backgroundColor: 'rgba(255,255,255,0.2)' }}>
                <motion.div
                  className="h-full rounded-full"
                  style={{ backgroundColor: '#fff' }}
                  initial={{ width: 0 }}
                  animate={{ width: `${Math.min(100, rankProgress)}%` }}
                  transition={{ duration: 1.2, ease: [0.16, 1, 0.3, 1] }}
                />
              </div>
            </div>
          </MotionDiv>

          {/* Stats row */}
          <MotionDiv {...stagger(1)} className="grid grid-cols-3 gap-3 mt-6">
            {[
              { value: streak.currentStreak, label: 'Day Streak' },
              { value: totalPointsEarned, label: 'Total XP' },
              { value: `${modulesCompleted}/${allCourses.length}`, label: 'Modules' },
            ].map((stat) => (
              <div key={stat.label} className="text-center py-3 rounded-xl" style={{ backgroundColor: 'rgba(255,255,255,0.2)' }}>
                <p style={{ fontFamily: "'Source Serif 4', serif", fontSize: '20px', fontWeight: 700, color: '#fff' }}>{stat.value}</p>
                <p style={{ fontFamily: "'DM Sans', sans-serif", fontSize: '10px', fontWeight: 600, letterSpacing: '0.1em', color: 'rgba(255,255,255,0.6)', textTransform: 'uppercase', marginTop: '2px' }}>{stat.label}</p>
              </div>
            ))}
          </MotionDiv>
        </div>
      </div>

      {/* ── Content area ── */}
      <div className="px-6 pb-28 max-w-3xl mx-auto">

        {/* Start Studying CTA */}
        {onGoToStudy && (
          <MotionDiv {...stagger(1.5)} className="flex justify-center mt-8">
            <PrimaryActionButton label="Start Studying" onClick={onGoToStudy} icon={Play} />
          </MotionDiv>
        )}

        {/* ── This Week ── */}
        <MotionDiv {...stagger(2)} className="mt-10">
          <div className="flex items-center justify-between mb-3">
            <p style={{ fontFamily: "'DM Sans', sans-serif", fontSize: '10px', fontWeight: 700, letterSpacing: '0.15em', color: '#9e9186', textTransform: 'uppercase' }}>This Week</p>
            <p style={{ fontFamily: "'DM Sans', sans-serif", fontSize: '11px', color: '#c4c0bc' }}>Resets in {daysUntilReset}d</p>
          </div>

          <div className="rounded-2xl bg-white dark:bg-zinc-900 p-5" style={{ border: '1px solid rgba(0,0,0,0.06)', boxShadow: '0 1px 4px rgba(0,0,0,0.04)' }}>
            {/* Weekly Goal bars */}
            <div className="space-y-4">
              {weeklyGoals.map((goal, gi) => {
                const current = weeklyGoalProgress[goal.metric] ?? 0;
                const pct = Math.min(100, Math.round((current / goal.target) * 100));
                const met = current >= goal.target;
                return (
                  <div key={goal.id}>
                    <div className="flex items-center justify-between mb-1.5">
                      <span style={{ fontFamily: "'DM Sans', sans-serif", fontSize: '13px', fontWeight: 500, color: met ? GOAL_COLORS[gi] : '#5a5550' }}>{goal.label}</span>
                      <span style={{ fontFamily: "'Source Serif 4', serif", fontSize: '13px', fontWeight: 700, color: met ? GOAL_COLORS[gi] : '#9e9186' }}>{current}/{goal.target}</span>
                    </div>
                    <div className="h-2 rounded-full overflow-hidden" style={{ backgroundColor: '#f0ede8' }}>
                      <motion.div
                        className="h-full rounded-full"
                        style={{ backgroundColor: GOAL_COLORS[gi] }}
                        initial={{ width: 0 }}
                        animate={{ width: `${pct}%` }}
                        transition={{ duration: 0.8, delay: gi * 0.1, ease: [0.16, 1, 0.3, 1] }}
                      />
                    </div>
                  </div>
                );
              })}
            </div>

            {/* Bonus indicator */}
            <div className="flex items-center justify-center gap-2 mt-5 pt-4" style={{ borderTop: '1px solid rgba(0,0,0,0.06)' }}>
              {weeklyGoals.map((goal, gi) => {
                const met = (weeklyGoalProgress[goal.metric] ?? 0) >= goal.target;
                return (
                  <div key={gi} className="flex items-center justify-center w-7 h-7 rounded-lg" style={{ backgroundColor: met ? GOAL_COLORS[gi] : '#e8e4de' }}>
                    {met ? (
                      <svg width="14" height="14" viewBox="0 0 14 14" fill="none"><path d="M3 7L6 10L11 4" stroke="#fff" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"/></svg>
                    ) : (
                      <span className="text-[10px] font-bold" style={{ color: '#a8a29e' }}>{gi + 1}</span>
                    )}
                  </div>
                );
              })}
              <span style={{ fontFamily: "'DM Sans', sans-serif", fontSize: '12px', fontWeight: 600, color: '#2A7D6F', marginLeft: '4px' }}>
                {weeklyGoals.filter(g => (weeklyGoalProgress[g.metric] ?? 0) >= g.target).length === 3 ? 'Bonus earned!' : '+50 JP bonus'}
              </span>
            </div>
          </div>

          {/* Weekly Challenge */}
          {weeklyChallenge?.isLoaded && !weeklyChallenge.isClaimed && (() => {
            const ch = weeklyChallenge;
            const CIcon = CHALLENGE_ICONS[ch.challenge.icon] || Trophy;
            const pct = Math.min(100, Math.round((ch.current / ch.challenge.target) * 100));
            return (
              <div className="flex items-center gap-3 rounded-2xl px-5 py-4 mt-3 bg-white dark:bg-zinc-900" style={{ border: '1px solid rgba(0,0,0,0.06)', boxShadow: '0 1px 4px rgba(0,0,0,0.04)' }}>
                <div className="w-10 h-10 rounded-xl flex items-center justify-center shrink-0" style={{ backgroundColor: 'rgba(42,125,111,0.12)' }}>
                  <CIcon size={20} style={{ color: '#2A7D6F' }} />
                </div>
                <div className="flex-1 min-w-0">
                  <p className="text-sm font-semibold truncate" style={{ color: '#1a1a1a' }}>{ch.challenge.title}</p>
                  <p className="text-xs" style={{ color: '#9e9186' }}>{ch.challenge.description || `${ch.current}/${ch.challenge.target}`}</p>
                </div>
                {ch.isCompleted && !ch.isClaimed ? (
                  <button onClick={async () => { await ch.claimReward(); pointsReload?.(); }} className="px-4 py-2 rounded-full text-xs font-bold text-white shrink-0" style={{ backgroundColor: '#2A7D6F' }}>
                    Claim
                  </button>
                ) : (
                  <div className="flex items-center gap-2 shrink-0">
                    <div className="w-10 h-2 rounded-full overflow-hidden" style={{ backgroundColor: '#e8e4de' }}>
                      <div className="h-full rounded-full" style={{ backgroundColor: '#2A7D6F', width: `${pct}%` }} />
                    </div>
                    <span style={{ fontSize: '11px', fontWeight: 700, color: '#2A7D6F' }}>{pct}%</span>
                  </div>
                )}
              </div>
            );
          })()}
        </MotionDiv>

        {/* ── Strategy Mastery ── */}
        {(() => {
          const masteredCount = strategyMastery ? STRATEGY_REGISTRY.filter(s => (strategyMastery[s.moduleId]?.tier ?? 'none') !== 'none').length : 0;
          const masteryPct = Math.round((masteredCount / STRATEGY_REGISTRY.length) * 100);
          return (
            <MotionDiv {...stagger(3)} className="mt-4">
              <div className="rounded-2xl bg-white dark:bg-zinc-900 overflow-hidden" style={{ border: '1px solid rgba(0,0,0,0.06)', boxShadow: '0 1px 4px rgba(0,0,0,0.04)' }}>
                <button onClick={() => setStrategyOpen(o => !o)} className="w-full flex items-center gap-3 px-5 py-4 cursor-pointer">
                  <div className="w-9 h-9 rounded-xl shrink-0 flex items-center justify-center" style={{ backgroundColor: 'rgba(107,92,231,0.1)' }}>
                    <Brain size={18} style={{ color: '#6C5CE7' }} />
                  </div>
                  <div className="flex-1 min-w-0 text-left">
                    <p className="text-sm font-semibold" style={{ color: '#1a1a1a' }}>Strategy Mastery</p>
                    <div className="flex items-center gap-2 mt-1.5">
                      <div className="flex-1 h-1.5 rounded-full overflow-hidden" style={{ backgroundColor: '#e8e4de', maxWidth: 120 }}>
                        <div className="h-full rounded-full" style={{ backgroundColor: '#6C5CE7', width: `${masteryPct}%` }} />
                      </div>
                      <span style={{ fontSize: '10px', fontWeight: 600, color: '#9e9186' }}>{masteredCount}/{STRATEGY_REGISTRY.length}</span>
                    </div>
                  </div>
                  <motion.div animate={{ rotate: strategyOpen ? 180 : 0 }} transition={{ duration: 0.3, ease: [0.16, 1, 0.3, 1] }}>
                    <ChevronDown size={16} color="#9e9186" />
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
                      <div className="px-5 pb-4 pt-1" style={{ borderTop: '1px solid rgba(0,0,0,0.06)' }}>
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
                                  <div key={strategy.moduleId} className={`py-3.5 ${si < arr.length - 1 ? '' : ''}`} style={si < arr.length - 1 ? { borderBottom: '1px solid rgba(0,0,0,0.04)' } : undefined}>
                                    <div className="flex items-center gap-3">
                                      <div className="w-8 h-8 rounded-xl shrink-0 flex items-center justify-center" style={{ backgroundColor: `${TIER_COLORS[tier]}14` }}>
                                        <Icon size={16} style={{ color: TIER_COLORS[tier] }} />
                                      </div>
                                      <span className="text-sm flex-1 font-medium" style={{ color: '#1a1a1a' }}>{strategy.strategyName}</span>
                                      <span style={{ fontSize: '10px', fontWeight: 600, textTransform: 'uppercase', color: TIER_COLORS[tier] }}>{TIER_LABELS[tier]}</span>
                                    </div>
                                    <div className="flex gap-1 mt-2.5 ml-11">
                                      {[0, 1, 2, 3].map(seg => (
                                        <div key={seg} className="flex-1 h-1.5 rounded-full" style={{ backgroundColor: seg <= tierIdx ? TIER_COLORS[tier] : '#e8e4de' }} />
                                      ))}
                                    </div>
                                  </div>
                                );
                              })}
                          </div>
                        ) : (
                          <p className="text-sm italic py-3" style={{ color: '#9e9186' }}>
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

        {/* ── Achievements ── */}
        {(() => {
          const achievePct = Math.round((unlockedAchievements.length / 58) * 100);
          return (
            <MotionDiv {...stagger(4)} className="mt-4">
              <div className="rounded-2xl bg-white dark:bg-zinc-900 overflow-hidden" style={{ border: '1px solid rgba(0,0,0,0.06)', boxShadow: '0 1px 4px rgba(0,0,0,0.04)' }}>
                <button onClick={() => setAchievementsOpen(o => !o)} className="w-full flex items-center gap-3 px-5 py-4 cursor-pointer">
                  <div className="w-9 h-9 rounded-xl shrink-0 flex items-center justify-center" style={{ backgroundColor: 'rgba(230,126,34,0.1)' }}>
                    <Award size={18} style={{ color: '#E67E22' }} />
                  </div>
                  <div className="flex-1 min-w-0 text-left">
                    <p className="text-sm font-semibold" style={{ color: '#1a1a1a' }}>Achievements</p>
                    <div className="flex items-center gap-2 mt-1.5">
                      <div className="flex-1 h-1.5 rounded-full overflow-hidden" style={{ backgroundColor: '#e8e4de', maxWidth: 120 }}>
                        <div className="h-full rounded-full" style={{ backgroundColor: '#E67E22', width: `${achievePct}%` }} />
                      </div>
                      <span style={{ fontSize: '10px', fontWeight: 600, color: '#9e9186' }}>{unlockedAchievements.length}/58</span>
                    </div>
                  </div>
                  <motion.div animate={{ rotate: achievementsOpen ? 180 : 0 }} transition={{ duration: 0.3, ease: [0.16, 1, 0.3, 1] }}>
                    <ChevronDown size={16} color="#9e9186" />
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
                      <div className="px-5 pb-5 pt-1" style={{ borderTop: '1px solid rgba(0,0,0,0.06)' }}>
                        <AchievementGallery unlockedAchievements={unlockedAchievements} achievementTimestamps={gamificationState.achievementTimestamps} />
                      </div>
                    </motion.div>
                  )}
                </AnimatePresence>
              </div>
            </MotionDiv>
          );
        })()}

        {/* ── Personal Bests ── */}
        {personalBests && Object.values(personalBests).some(v => v > 0) && (
          <MotionDiv {...stagger(5)} className="mt-10">
            <p style={{ fontFamily: "'DM Sans', sans-serif", fontSize: '10px', fontWeight: 700, letterSpacing: '0.15em', color: '#9e9186', textTransform: 'uppercase', marginBottom: '12px' }}>Personal Bests</p>
            <div className="grid grid-cols-2 gap-3">
              {[
                { key: 'bestDayPoints', label: 'Best Day Points', color: '#2A7D6F' },
                { key: 'bestDaySections', label: 'Best Day Sections', color: '#E67E22' },
                { key: 'bestWeekPoints', label: 'Best Week Points', color: '#6366f1' },
                { key: 'bestWeekSessions', label: 'Best Week Sessions', color: '#E84393' },
              ].filter(pb => (personalBests as any)[pb.key] > 0).map(pb => (
                <div key={pb.key} className="rounded-2xl bg-white dark:bg-zinc-900 px-4 py-4" style={{ border: '1px solid rgba(0,0,0,0.06)', boxShadow: '0 1px 4px rgba(0,0,0,0.04)' }}>
                  <div className="w-8 h-8 rounded-xl flex items-center justify-center mb-3" style={{ backgroundColor: `${pb.color}14` }}>
                    <Trophy size={16} style={{ color: pb.color }} />
                  </div>
                  <p style={{ fontFamily: "'Source Serif 4', serif", fontSize: '24px', fontWeight: 700, color: '#1a1a1a' }}>{(personalBests as any)[pb.key]}</p>
                  <p style={{ fontFamily: "'DM Sans', sans-serif", fontSize: '11px', color: '#9e9186', marginTop: '2px' }}>{pb.label}</p>
                </div>
              ))}
            </div>
          </MotionDiv>
        )}

        {/* ── North Star ── */}
        {northStar && (
          <MotionDiv {...stagger(6)} className="mt-10">
            <div className="relative overflow-hidden rounded-2xl" style={{ background: `linear-gradient(135deg, ${currentRank.colorHex}, ${currentRank.colorHex}dd)` }}>
              {/* Decorative circles */}
              <div className="absolute pointer-events-none" style={{ top: -30, right: -20, width: 100, height: 100, borderRadius: '50%', background: 'rgba(255,255,255,0.1)' }} />
              <div className="absolute pointer-events-none" style={{ bottom: -15, left: -15, width: 70, height: 70, borderRadius: '50%', background: 'rgba(255,255,255,0.07)' }} />

              <div className="relative z-10 p-6 text-center">
                <div className="w-10 h-10 rounded-full mx-auto mb-3 flex items-center justify-center" style={{ backgroundColor: 'rgba(255,255,255,0.18)' }}>
                  <Compass size={20} color="#fff" />
                </div>
                <p style={{ fontFamily: "'DM Sans', sans-serif", fontSize: '10px', fontWeight: 700, letterSpacing: '0.15em', color: 'rgba(255,255,255,0.5)', textTransform: 'uppercase', marginBottom: '8px' }}>Your North Star</p>
                <p style={{ fontFamily: "'Source Serif 4', serif", fontSize: '18px', fontStyle: 'italic', lineHeight: 1.5, color: '#fff' }}>
                  &ldquo;{northStar.statement}&rdquo;
                </p>
                <button onClick={onOpenJourney} className="mt-4 inline-flex items-center gap-1.5 group px-4 py-2 rounded-full text-xs font-semibold transition-colors" style={{ backgroundColor: 'rgba(255,255,255,0.2)', color: '#fff' }}>
                  My Journey <ArrowRight size={12} className="group-hover:translate-x-0.5 transition-transform" />
                </button>
              </div>
            </div>
          </MotionDiv>
        )}
      </div>
    </div>
  );
};

export default TrainingHub;
