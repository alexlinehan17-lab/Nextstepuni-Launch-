/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 */

import React, { useState, useEffect, useRef } from 'react';
import { motion, useAnimationControls } from 'framer-motion';
import { MotionButton, MotionSpan } from './Motion';
import { Flame, TrendingUp, Target, Zap, Award, Crown, Mountain, Footprints, Coins } from 'lucide-react';
import { type GamificationState, type StreakTier, getStreakTier } from '../gamificationConfig';
import { type StreakData } from '../hooks/useStreak';

const RANK_ICONS: Record<string, React.ElementType> = {
  Footprints,
  TrendingUp,
  Target,
  Zap,
  Award,
  Crown,
  Mountain,
};

const STREAK_TIER_STYLES: Record<StreakTier, string> = {
  none: 'text-zinc-400 dark:text-zinc-500',
  small: 'text-orange-400',
  medium: 'text-orange-500',
  large: 'text-orange-500',
  monthly: 'text-amber-400',
};

// ─── Animated Counter Hook ─────────────────────────────────────────────────

function useAnimatedCounter(target: number, duration = 800): { display: number; isAnimating: boolean } {
  const [display, setDisplay] = useState(target);
  const [isAnimating, setIsAnimating] = useState(false);
  const prevRef = useRef(target);
  const frameRef = useRef<number>(0);

  useEffect(() => {
    const prev = prevRef.current;
    prevRef.current = target;

    // Skip animation on first render or if value hasn't changed
    if (prev === target) return;

    const diff = target - prev;
    if (diff === 0) return;

    setIsAnimating(true);
    const startTime = performance.now();

    const animate = (now: number) => {
      const elapsed = now - startTime;
      const progress = Math.min(elapsed / duration, 1);
      // Ease out cubic
      const eased = 1 - Math.pow(1 - progress, 3);
      setDisplay(Math.round(prev + diff * eased));

      if (progress < 1) {
        frameRef.current = requestAnimationFrame(animate);
      } else {
        setDisplay(target);
        setIsAnimating(false);
      }
    };

    frameRef.current = requestAnimationFrame(animate);
    return () => cancelAnimationFrame(frameRef.current);
  }, [target, duration]);

  return { display, isAnimating };
}

// ─── Animated Points Display ────────────────────────────────────────────────

const AnimatedPoints: React.FC<{ value: number; size: 'sm' | 'xs' }> = ({ value, size }) => {
  const { display, isAnimating } = useAnimatedCounter(value);
  const coinControls = useAnimationControls();
  const prevValueRef = useRef(value);

  useEffect(() => {
    if (prevValueRef.current !== value && value > prevValueRef.current) {
      // Coin bounce when points increase
      coinControls.start({
        scale: [1, 1.4, 1],
        rotate: [0, -15, 15, 0],
        transition: { duration: 0.5, ease: 'easeOut' },
      });
    }
    prevValueRef.current = value;
  }, [value, coinControls]);

  const textClass = size === 'sm'
    ? 'text-xs font-bold'
    : 'text-[10px] font-bold';

  return (
    <div className="flex items-center gap-1">
      <motion.div animate={coinControls}>
        <Coins size={size === 'sm' ? 12 : 10} className="text-amber-500" />
      </motion.div>
      <MotionSpan
        className={`${textClass} tabular-nums ${isAnimating ? 'text-amber-500' : 'text-zinc-500 dark:text-zinc-400'}`}
        animate={isAnimating ? { scale: [1, 1.08, 1] } : {}}
        transition={{ duration: 0.3 }}
      >
        {display}
      </MotionSpan>
    </div>
  );
};

// ─── Component ──────────────────────────────────────────────────────────────

interface TrainingPulseProps {
  gamificationState: GamificationState;
  onOpenHub: () => void;
  streak: StreakData;
  pointsBalance: number;
}

const TrainingPulse: React.FC<TrainingPulseProps> = ({
  gamificationState,
  onOpenHub,
  streak,
  pointsBalance,
}) => {
  const { currentRank, rankProgress, nextRank } = gamificationState;
  const RankIcon = RANK_ICONS[currentRank.icon] || Footprints;
  const streakTier = getStreakTier(streak.currentStreak);

  return (
    <>
      {/* Desktop: Horizontal pill */}
      <MotionButton
        onClick={onOpenHub}
        whileHover={{ scale: 1.02 }}
        whileTap={{ scale: 0.98 }}
        className="hidden md:flex items-center gap-3 px-4 py-2 rounded-full bg-white dark:bg-zinc-900 border border-zinc-200 dark:border-zinc-800 shadow-sm hover:shadow-md transition-shadow cursor-pointer focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-[rgba(var(--accent),0.5)]"
      >
        {/* Rank badge */}
        <div className="flex items-center gap-1.5">
          <div
            className="w-7 h-7 rounded-full flex items-center justify-center"
            style={{ backgroundColor: `${currentRank.colorHex}18` }}
          >
            <RankIcon size={14} style={{ color: currentRank.colorHex }} />
          </div>
          <span className="text-xs font-bold text-zinc-700 dark:text-zinc-200">{currentRank.title}</span>
        </div>

        {/* XP progress bar */}
        {nextRank && (
          <div className="w-16 h-1.5 bg-zinc-100 dark:bg-zinc-800 rounded-full overflow-hidden">
            <motion.div
              className="h-full rounded-full"
              style={{ backgroundColor: currentRank.colorHex }}
              initial={{ width: 0 }}
              animate={{ width: `${rankProgress}%` }}
              transition={{ duration: 0.8, ease: 'easeOut' }}
            />
          </div>
        )}

        {/* Streak */}
        {streak.currentStreak > 0 && (
          <div className="flex items-center gap-1">
            <Flame
              size={14}
              className={`${STREAK_TIER_STYLES[streakTier]} ${streakTier === 'large' || streakTier === 'monthly' ? 'animate-pulse' : ''}`}
            />
            <span className="text-xs font-bold text-zinc-600 dark:text-zinc-300">{streak.currentStreak}</span>
          </div>
        )}

        {/* Animated points balance */}
        <AnimatedPoints value={pointsBalance} size="sm" />
      </MotionButton>

      {/* Mobile: Compact badge — shown inline in header area */}
      <MotionButton
        onClick={onOpenHub}
        whileTap={{ scale: 0.95 }}
        className="flex md:hidden items-center gap-2 px-3 py-1.5 rounded-full bg-white dark:bg-zinc-900 border border-zinc-200 dark:border-zinc-800 shadow-sm cursor-pointer focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-[rgba(var(--accent),0.5)]"
      >
        {/* Mini rank badge */}
        <div
          className="w-6 h-6 rounded-full flex items-center justify-center"
          style={{ backgroundColor: `${currentRank.colorHex}18` }}
        >
          <RankIcon size={12} style={{ color: currentRank.colorHex }} />
        </div>

        {/* Mini progress ring */}
        <svg className="w-5 h-5 -rotate-90" viewBox="0 0 24 24">
          <circle cx="12" cy="12" r="9" stroke={currentRank.colorHex} strokeWidth="2.5" fill="transparent" className="opacity-15" />
          <circle
            cx="12" cy="12" r="9"
            stroke={currentRank.colorHex}
            strokeWidth="2.5"
            fill="transparent"
            strokeDasharray={`${2 * Math.PI * 9}`}
            strokeDashoffset={`${2 * Math.PI * 9 * (1 - rankProgress / 100)}`}
            strokeLinecap="round"
          />
        </svg>

        {/* Streak count */}
        {streak.currentStreak > 0 && (
          <div className="flex items-center gap-0.5">
            <Flame size={12} className={STREAK_TIER_STYLES[streakTier]} />
            <span className="text-[10px] font-bold text-zinc-600 dark:text-zinc-300">{streak.currentStreak}</span>
          </div>
        )}
      </MotionButton>
    </>
  );
};

export default TrainingPulse;
