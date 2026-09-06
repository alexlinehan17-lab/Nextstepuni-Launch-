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
  type LucideIcon,
} from 'lucide-react';
import { type GamificationState, generateWeeklyGoals, getWeekNumber } from '../gamificationConfig';
import PrimaryActionButton from './ui/PrimaryActionButton';
import { type StreakData } from '../hooks/useStreak';
import { type NorthStar, type UserProgress, type StrategyMasteryMap, type MasteryTier } from '../types';
import AchievementGallery, { AchievementBadge } from './AchievementGallery';
import { getAchievementById } from '../achievementData';
import { type CourseData } from './Library';
import { STRATEGY_REGISTRY } from '../utils/strategyRegistry';
import { type WeeklyChallengeState } from '../hooks/useWeeklyChallenge';
import { ToolHeader } from './ToolHeader';
import { COLORS } from '../design/tokens';
import { getNorthStarDisplayText, hasStudentAuthoredNorthStar } from '../services/directionProfile';
import { getAchievementsForCurriculum } from '../achievementData';
import { type CurriculumLevel } from '../utils/authUtils';

// ─── Config ─────────────────────────────────────────────────

const RANK_ICONS: Record<string, LucideIcon> = {
  Footprints, Flame, TrendingUp, Target, Zap, Award, Crown, Mountain,
};

const _TIER_ORDER: MasteryTier[] = ['habitual', 'applied', 'practiced', 'learned'];
const TIER_LABELS: Record<MasteryTier, string> = { none: '', learned: 'Learned', practiced: 'Practiced', applied: 'Applied', habitual: 'Habitual' };
// `practiced` tier deliberately keeps the legacy teal #2A7D6F — this is the
// mastery-tier data-viz colour, not brand accent. Preserved per the colour
// pivot scope notes (data-viz preserve).
const TIER_COLORS: Record<MasteryTier, string> = { none: '#A8A29E', learned: '#3B82F6', practiced: '#2A7D6F', applied: '#F59E0B', habitual: '#7C3AED' };
const TIER_INDEX: Record<MasteryTier, number> = { none: -1, learned: 0, practiced: 1, applied: 2, habitual: 3 };

const STRATEGY_ICONS: Record<string, LucideIcon> = {
  'mastering-active-recall-protocol': Brain, 'mastering-spaced-repetition-protocol': Repeat,
  'mastering-interleaving-protocol': Shuffle, 'elaborative-interrogation-protocol': HelpCircle,
  'agency-protocol': Compass, 'growth-mindset-protocol': Sprout, 'digital-distraction-protocol': Shield,
  'learning-radar-protocol': Radar, 'exam-hall-strategies-protocol': ClipboardCheck,
};

const CHALLENGE_ICONS: Record<string, LucideIcon> = {
  Brain, Repeat, Shuffle, HelpCircle, Compass, Sprout, Shield, Radar, ClipboardCheck, Zap, Trophy,
};

const GOAL_COLORS = [COLORS.accent, '#E67E22', '#6366f1'];

// ─── Component ──────────────────────────────────────────────

interface TrainingHubProps {
  gamificationState: GamificationState;
  streak: StreakData;
  pointsBalance: number;
  northStar: NorthStar | null;
  onBack: () => void;
  onOpenJourney: () => void;
  onOpenDirection?: () => void;
  userProgress: UserProgress;
  allCourses: CourseData[];
  strategyMastery?: StrategyMasteryMap;
  dismissedGuides?: Record<string, string>;
  onDismissGuide?: (id: string) => void;
  weeklyChallenge?: WeeklyChallengeState;
  pointsReload?: () => void;
  onGoToStudy?: () => void;
  uid?: string;
  curriculumLevel?: CurriculumLevel;
}

const TrainingHub: React.FC<TrainingHubProps> = ({
  gamificationState, streak, pointsBalance: _pointsBalance, northStar, onBack, onOpenJourney, onOpenDirection,
  userProgress, allCourses, strategyMastery, weeklyChallenge, pointsReload, onGoToStudy, uid: _uid,
  curriculumLevel = 'senior',
}) => {
  const { currentRank, nextRank, rankProgress, totalPointsEarned, unlockedAchievements, weeklyGoalProgress, weekStartDate: _weekStartDate, personalBests } = gamificationState;
  const weekNumber = getWeekNumber();
  const weeklyGoals = generateWeeklyGoals(currentRank.id, weekNumber);
  const RankIcon = RANK_ICONS[currentRank.icon] || Star;
  const modulesCompleted = allCourses.filter(c => { const p = userProgress[c.id]; return p && p.unlockedSection >= c.sectionsCount; }).length;
  const availableAchievements = React.useMemo(
    () => getAchievementsForCurriculum(curriculumLevel),
    [curriculumLevel],
  );
  const unlockedAchievementSet = React.useMemo(
    () => new Set(unlockedAchievements),
    [unlockedAchievements],
  );
  const unlockedAchievementCount = availableAchievements.filter(achievement => unlockedAchievementSet.has(achievement.id)).length;
  const visibleAchievementTotal = availableAchievements.filter(
    achievement => !achievement.isHidden || unlockedAchievementSet.has(achievement.id),
  ).length;

  const [strategyOpen, setStrategyOpen] = React.useState(false);
  const [achievementsOpen, setAchievementsOpen] = React.useState(false);

  const now = new Date();
  const dayOfWeek = now.getDay();
  const daysUntilReset = dayOfWeek === 0 ? 1 : 8 - dayOfWeek;

  const stagger = (i: number) => ({ initial: { opacity: 0, y: 16 }, animate: { opacity: 1, y: 0 }, transition: { delay: i * 0.06, duration: 0.4, ease: [0.16, 1, 0.3, 1] as number[] } });

  return (
    <div className="min-h-screen theme-compat bg-white dark:bg-zinc-950">

      {/* Back affordance — small chip above the header */}
      <div className="px-6 pt-5">
        <button
          onClick={onBack}
          className="inline-flex items-center gap-2 px-3 py-2 rounded-xl text-[12px] font-semibold text-[#1A1A1A] dark:text-white border-[1.5px] border-[#383838] dark:border-zinc-600 bg-white dark:bg-zinc-900 shadow-[2px_2px_0_0_#383838] hover:-translate-y-0.5 active:translate-x-0.5 active:translate-y-0.5 active:shadow-none transition-all"
        >
          <ArrowLeft size={14} />
          Back
        </button>
      </div>

      {/* ── Editorial header ── */}
      <div className="px-6 max-w-3xl mx-auto pt-4">
        <ToolHeader
          themeColor={COLORS.accent}
          eyebrow="Track · Progress"
          title="Training Hub"
          subtitle="Build your streak. Earn your rank. Watch the work compound — week by week, point by point."
          iconBlob={
            <img
              src="/icons/training-hub.png"
              alt=""
              style={{ width: 108, height: 108, objectFit: 'contain' }}
            />
          }
        />
      </div>

      {/* ── Rank + stats ──
          Chunky-shadow card grammar matches the rest of the app
          (YearTransitionFlow, GC tiles, onboarding pickers). The ring
          wraps the rank icon as one combined identity — Mercury-dense
          replacement for the old linear progress bar. */}
      <div className="px-6 max-w-3xl mx-auto pt-6">
        <MotionDiv
          {...stagger(0)}
          className="rounded-2xl bg-white dark:bg-zinc-900 p-5 border-2 border-[#1A1A1A] dark:border-zinc-700 shadow-[4px_4px_0_0_#1A1A1A] dark:shadow-[4px_4px_0_0_#3f3f46]"
        >
          <div className="flex items-center gap-5">
            {/* Rank identity — ring wraps the icon, fill colour is the
                rank's own colour so the ring reads "you, at this stage". */}
            <div className="relative shrink-0" style={{ width: 76, height: 76 }}>
              <svg width="76" height="76" viewBox="0 0 76 76" className="-rotate-90 overflow-visible">
                <circle cx="38" cy="38" r="32" stroke="var(--accent-tint-hex)" strokeWidth="6" fill="transparent" />
                <motion.circle
                  cx="38" cy="38" r="32"
                  stroke={currentRank.colorHex}
                  strokeWidth="6"
                  fill="transparent"
                  strokeDasharray={2 * Math.PI * 32}
                  initial={{ strokeDashoffset: 2 * Math.PI * 32 }}
                  animate={{ strokeDashoffset: (2 * Math.PI * 32) - (Math.min(100, rankProgress) / 100) * (2 * Math.PI * 32) }}
                  transition={{ duration: 1.5, ease: 'easeOut' }}
                  strokeLinecap="round"
                  style={{ filter: `drop-shadow(0 0 6px ${currentRank.colorHex}33)` }}
                />
              </svg>
              <div className="absolute inset-0 flex items-center justify-center">
                <RankIcon size={28} color={currentRank.colorHex} />
              </div>
            </div>
            {/* Title + XP — restraint here so the ring carries the visual weight. */}
            <div className="flex-1 min-w-0">
              <p style={{ fontFamily: "'Source Serif 4', serif", fontSize: '22px', fontWeight: 600, color: 'var(--text-primary)' }}>
                {currentRank.title}
              </p>
              <p style={{ fontFamily: "'DM Sans', sans-serif", fontSize: '12px', color: 'var(--text-muted)', marginTop: 2 }}>
                {nextRank ? `${totalPointsEarned.toLocaleString()} / ${nextRank.minPoints.toLocaleString()} XP` : 'Max rank reached'}
              </p>
              {nextRank && (
                <p style={{ fontFamily: "'DM Sans', sans-serif", fontSize: '11px', fontWeight: 600, color: currentRank.colorHex, marginTop: 6 }}>
                  {(nextRank.minPoints - totalPointsEarned).toLocaleString()} XP to {nextRank.title}
                </p>
              )}
            </div>
          </div>
        </MotionDiv>

        {/* Stat record — one card, cells divided by hairlines rather than
            three competing boxes; serif tabular numerals carry the weight. */}
        <MotionDiv {...stagger(1)} className="mt-3 rounded-xl bg-white dark:bg-zinc-900 border-2 border-[#1A1A1A] dark:border-zinc-700 shadow-[4px_4px_0_0_#1A1A1A] dark:shadow-[4px_4px_0_0_#3f3f46]">
          <div className="grid grid-cols-3 py-4">
            {[
              { value: streak.currentStreak, label: 'Day Streak' },
              { value: totalPointsEarned.toLocaleString(), label: 'Total XP' },
              { value: `${modulesCompleted}/${allCourses.length}`, label: 'Modules' },
            ].map((stat, i) => (
              <div key={stat.label} className={`px-4 text-center ${i > 0 ? 'border-l border-[#E5E1DA] dark:border-zinc-700' : ''}`}>
                <p className="tabular-nums" style={{ fontFamily: "'Source Serif 4', serif", fontSize: '26px', fontWeight: 700, lineHeight: 1.1, color: 'var(--text-primary)' }}>{stat.value}</p>
                <p style={{ fontFamily: "'DM Sans', sans-serif", fontSize: '10px', fontWeight: 700, letterSpacing: '0.12em', color: 'var(--text-label)', textTransform: 'uppercase', marginTop: '3px' }}>{stat.label}</p>
              </div>
            ))}
          </div>
        </MotionDiv>

        {/* Latest badge — the most recent unlock surfaces here for a while
            instead of living only inside the gallery. */}
        {(() => {
          const ts = gamificationState.achievementTimestamps ?? {};
          // Unlocks that predate timestamps all tie at 0 — the array is
          // append-ordered, so the later index is the newer unlock.
          const latest = [...unlockedAchievements].sort((a, b) =>
            (ts[b] ?? 0) - (ts[a] ?? 0)
            || unlockedAchievements.indexOf(b) - unlockedAchievements.indexOf(a))[0];
          const latestDef = latest ? getAchievementById(latest) : undefined;
          if (!latest || !latestDef) return null;
          const when = ts[latest]
            ? new Date(ts[latest]).toLocaleDateString('en-IE', { day: 'numeric', month: 'short' })
            : null;
          return (
            <MotionDiv {...stagger(1.25)} className="mt-3 flex items-center gap-3 rounded-xl bg-white px-4 py-3 dark:bg-zinc-900" style={{ border: '1px solid rgba(0,0,0,0.06)', boxShadow: '0 1px 4px rgba(0,0,0,0.04)' }}>
              <AchievementBadge achievementId={latest} size={40} />
              <div className="min-w-0 flex-1">
                <p style={{ fontFamily: "'DM Sans', sans-serif", fontSize: '10px', fontWeight: 700, letterSpacing: '0.14em', color: '#9e9186', textTransform: 'uppercase' }}>Latest badge</p>
                <p className="truncate" style={{ fontFamily: "'Source Serif 4', serif", fontSize: '15px', fontWeight: 700, color: 'var(--text-primary)' }}>{latestDef.title}</p>
              </div>
              {when && <span className="shrink-0 text-[11px] font-semibold text-[#A8A29E] dark:text-zinc-500">Earned {when}</span>}
            </MotionDiv>
          );
        })()}
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
                    <div className="h-2 rounded-full overflow-hidden" style={{ backgroundColor: 'var(--accent-tint-hex)' }}>
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
              <span style={{ fontFamily: "'DM Sans', sans-serif", fontSize: '12px', fontWeight: 600, color: COLORS.accent, marginLeft: '4px' }}>
                {weeklyGoals.filter(g => (weeklyGoalProgress[g.metric] ?? 0) >= g.target).length === 3 ? 'Bonus earned!' : '+50 JP bonus'}
              </span>
            </div>
          </div>

          {/* Weekly Challenge */}
          {weeklyChallenge?.isLoaded && weeklyChallenge?.challenge && !weeklyChallenge.isClaimed && (() => {
            const ch = weeklyChallenge;
            const CIcon = CHALLENGE_ICONS[ch.challenge!.icon] || Trophy;
            const pct = Math.min(100, Math.round((ch.current / ch.challenge!.target) * 100));
            return (
              <div className="flex items-center gap-3 rounded-2xl px-5 py-4 mt-3 bg-white dark:bg-zinc-900" style={{ border: '1px solid rgba(0,0,0,0.06)', boxShadow: '0 1px 4px rgba(0,0,0,0.04)' }}>
                <div className="w-10 h-10 rounded-xl flex items-center justify-center shrink-0" style={{ backgroundColor: 'rgba(242,107,31,0.12)' }}>
                  <CIcon size={20} style={{ color: COLORS.accent }} />
                </div>
                <div className="flex-1 min-w-0">
                  <p className="text-sm font-semibold truncate" style={{ color: '#1a1a1a' }}>{ch.challenge!.title}</p>
                  <p className="text-xs" style={{ color: '#9e9186' }}>{ch.challenge!.description || `${ch.current}/${ch.challenge!.target}`}</p>
                </div>
                {ch.isCompleted && !ch.isClaimed ? (
                  <button onClick={async () => { await ch.claimReward(); pointsReload?.(); }} className="px-4 py-2 rounded-full text-xs font-bold text-white shrink-0" style={{ backgroundColor: COLORS.accent }}>
                    Claim
                  </button>
                ) : (
                  <div className="flex items-center gap-2 shrink-0">
                    <div className="w-10 h-2 rounded-full overflow-hidden" style={{ backgroundColor: 'var(--accent-tint-hex)' }}>
                      <div className="h-full rounded-full" style={{ backgroundColor: COLORS.accent, width: `${pct}%` }} />
                    </div>
                    <span style={{ fontSize: '11px', fontWeight: 700, color: COLORS.accent }}>{pct}%</span>
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
                      <div className="flex-1 h-1.5 rounded-full overflow-hidden" style={{ backgroundColor: 'var(--accent-tint-hex)', maxWidth: 120 }}>
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
          const achievePct = visibleAchievementTotal > 0
            ? Math.round((unlockedAchievementCount / visibleAchievementTotal) * 100)
            : 0;
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
                      <div className="flex-1 h-1.5 rounded-full overflow-hidden" style={{ backgroundColor: 'var(--accent-tint-hex)', maxWidth: 120 }}>
                        <div className="h-full rounded-full" style={{ backgroundColor: '#E67E22', width: `${achievePct}%` }} />
                      </div>
                      <span style={{ fontSize: '10px', fontWeight: 600, color: '#9e9186' }}>{unlockedAchievementCount}/{visibleAchievementTotal}</span>
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
                        <AchievementGallery
                          unlockedAchievements={unlockedAchievements}
                          achievementTimestamps={gamificationState.achievementTimestamps}
                          curriculumLevel={curriculumLevel}
                        />
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
                { key: 'bestDayPoints', label: 'Best Day Points', color: COLORS.accent },
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

        {/* ── North Star ──
            Pulled into the chunky-shadow + painted-blob language. The
            rank colour now lives in the blob and compass ink (instead of
            being the full gradient background), which keeps the emotional
            link between rank and "why you're studying" without turning
            the panel into a saturated island that's at odds with every
            other surface on the page. */}
        {northStar && (
          <MotionDiv {...stagger(6)} className="mt-10">
            <div className="rounded-2xl bg-white dark:bg-zinc-900 p-6 md:p-8 border-2 border-[#1A1A1A] dark:border-zinc-700 shadow-[4px_4px_0_0_#1A1A1A] dark:shadow-[4px_4px_0_0_#3f3f46]">
              <div className="flex flex-col items-center text-center">
                {/* A single hand-drawn object over a painted blob, matching the
                    product's illustrative icon family. The orange north needle
                    carries the brand accent; rank colour belongs in data, not
                    in the identity of this card. */}
                <div className="relative w-16 h-16 mb-4 shrink-0">
                  <svg viewBox="0 0 64 64" className="absolute inset-0 w-full h-full" aria-hidden="true">
                    <path
                      d="M 38 4 Q 12 6 6 28 Q 2 50 22 56 Q 50 62 60 36 Q 64 12 48 4 Q 42 2 38 4 Z"
                      fill="#D9D4F6"
                    />
                  </svg>
                  <img
                    src="/assets/training/north-star-compass.png"
                    alt=""
                    aria-hidden="true"
                    className="pointer-events-none absolute left-1/2 top-1/2 h-[120px] w-[120px] max-w-none -translate-x-1/2 -translate-y-1/2 object-contain"
                  />
                </div>

                <p style={{ fontFamily: "'DM Sans', sans-serif", fontSize: '10px', fontWeight: 700, letterSpacing: '0.18em', color: 'var(--text-label)', textTransform: 'uppercase', marginBottom: '10px' }}>
                  Your North Star
                </p>

                <p style={{ fontFamily: "'Source Serif 4', serif", fontSize: '20px', fontStyle: hasStudentAuthoredNorthStar(northStar) ? 'italic' : 'normal', lineHeight: 1.45, color: 'var(--text-primary)', maxWidth: 460 }}>
                  {hasStudentAuthoredNorthStar(northStar) ? `“${getNorthStarDisplayText(northStar)}”` : getNorthStarDisplayText(northStar)}
                </p>

                {/* Chunky-shadow accent button — same press feel as the
                    year-bump CTA. */}
                <button
                  onClick={onOpenDirection ?? onOpenJourney}
                  className="mt-6 inline-flex items-center gap-2 px-5 py-2.5 rounded-2xl border-2 border-[#1A1A1A] bg-[#F26B1F] text-[#FDF8F0] font-sans font-bold text-sm shadow-[4px_4px_0_0_#1A1A1A] hover:shadow-[6px_6px_0_0_#1A1A1A] hover:-translate-y-0.5 active:translate-x-1 active:translate-y-1 active:shadow-[0px_0px_0_0_#1A1A1A] transition-all duration-150"
                >
                  My Direction
                  <ArrowRight size={14} />
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
