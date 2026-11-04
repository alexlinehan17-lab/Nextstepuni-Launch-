/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 */

import React, { useEffect, useRef, useState } from 'react';
import { MotionButton, useReducedMotion } from './Motion';
import Avatar from './Avatar';
import type { GamificationState } from '../gamificationConfig';
import type { StreakData } from '../hooks/useStreak';
import './student-header.css';

function useAnimatedPoints(value: number, reducedMotion: boolean | null): number {
  const [display, setDisplay] = useState(value);
  const previous = useRef(value);

  useEffect(() => {
    if (reducedMotion || previous.current === value) {
      previous.current = value;
      setDisplay(value);
      return;
    }
    const from = previous.current;
    const start = performance.now();
    let frame: number;
    const animate = (now: number) => {
      const progress = Math.min((now - start) / 650, 1);
      const next = Math.round(from + (value - from) * (1 - Math.pow(1 - progress, 3)));
      previous.current = next;
      setDisplay(next);
      if (progress < 1) frame = requestAnimationFrame(animate);
    };
    frame = requestAnimationFrame(animate);
    return () => cancelAnimationFrame(frame);
  }, [value, reducedMotion]);

  return display;
}

interface TrainingPulseProps {
  gamificationState: GamificationState;
  onOpenProgress: () => void;
  streak: StreakData;
  pointsBalance: number;
  avatar: string;
}

const TrainingPulse: React.FC<TrainingPulseProps> = ({ gamificationState, onOpenProgress, streak, pointsBalance, avatar }) => {
  const { currentRank, rankProgress, nextRank } = gamificationState;
  const reducedMotion = useReducedMotion();
  const points = useAnimatedPoints(pointsBalance, reducedMotion);
  const progress = nextRank ? Math.max(0, Math.min(100, rankProgress)) : 100;
  const progressLabel = nextRank ? `${progress}% to ${nextRank.title}` : 'Highest rank reached';

  return (
    <MotionButton
      type="button"
      onClick={onOpenProgress}
      aria-label={`${currentRank.title}; ${progressLabel}; ${streak.currentStreak} day streak; ${pointsBalance} Journey Points. Open milestones.`}
      title="Open progress and milestones"
      whileHover={reducedMotion ? undefined : { y: -2 }}
      whileTap={reducedMotion ? undefined : { scale: 0.98 }}
      className="nsu-training-pulse"
    >
      <span className="nsu-rank-orbit" style={{ '--nsu-rank-progress': `${progress}%` } as React.CSSProperties} aria-hidden="true">
        <Avatar seed={avatar || 'star-crew:beanie'} className="nsu-rank-avatar" />
      </span>
      <span className="nsu-rank-copy">
        <strong>{currentRank.title}</strong>
        <small>{progressLabel}</small>
      </span>
      <span className="nsu-rank-stats" aria-hidden="true">
        <span><strong>{streak.currentStreak}</strong><small>day streak</small></span>
        <span><strong>{points.toLocaleString('en-IE')}</strong><small>Journey Points</small></span>
      </span>
    </MotionButton>
  );
};

export default TrainingPulse;
