/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 */

import React, { useEffect, useRef } from 'react';
import { AnimatePresence } from 'framer-motion';
import { MotionDiv } from './Motion';
import { Trophy, Star, Flame, BookOpen, Clock, Target, Award, Crown, Mountain, Zap, Eye, Brain, Lightbulb, Shield, Sparkles } from 'lucide-react';
import { type AchievementDefinition } from '../gamificationConfig';

const ICON_MAP: Record<string, React.ElementType> = {
  Trophy, Star, Flame, BookOpen, Clock, Target, Award, Crown, Mountain, Zap,
  Eye, Brain, Lightbulb, Shield, Sparkles,
  Footprints: Target, PlayCircle: Zap, BookCheck: BookOpen,
  Hash: Trophy, Milestone: Mountain, FolderCheck: BookOpen,
  CircleDot: Target, Timer: Clock, CalendarCheck: Clock,
  Calendar: Clock, PenLine: Brain, MessageSquare: Brain,
  NotebookPen: Brain, Compass: Target, ShieldCheck: Shield,
  ArrowUp: Zap, BarChart3: Target, Gem: Star, Sunrise: Star,
  Layers: BookOpen,
};

interface AchievementToastProps {
  achievement: AchievementDefinition | null;
  onDismiss: () => void;
}

const AchievementToast: React.FC<AchievementToastProps> = ({ achievement, onDismiss }) => {
  // Use ref for onDismiss to avoid resetting the timer on every render
  const onDismissRef = useRef(onDismiss);
  onDismissRef.current = onDismiss;

  const isVisible = achievement !== null;

  // Auto-dismiss after 3 seconds — only re-triggers when visibility actually changes
  useEffect(() => {
    if (!isVisible) return;
    const timer = setTimeout(() => onDismissRef.current(), 3000);
    return () => clearTimeout(timer);
  }, [isVisible, achievement?.id]);

  return (
    <AnimatePresence>
      {achievement && (
        <MotionDiv
          initial={{ opacity: 0, y: -6, scale: 0.95 }}
          animate={{ opacity: 1, y: 0, scale: 1 }}
          exit={{ opacity: 0, y: -6, scale: 0.95 }}
          transition={{ duration: 0.3, ease: [0.16, 1, 0.3, 1] }}
          onClick={onDismiss}
          className="mt-2 cursor-pointer w-full"
        >
          <div className="flex items-center justify-center gap-2 px-3.5 py-2 rounded-full bg-purple-50 dark:bg-purple-900/20 border border-purple-200 dark:border-purple-700/40 shadow-sm">
            {(() => {
              const Icon = ICON_MAP[achievement.icon] || Trophy;
              return <Icon size={14} className="text-purple-500 dark:text-purple-400 shrink-0" />;
            })()}
            <span className="text-xs font-bold text-purple-700 dark:text-purple-300 truncate max-w-[140px]">{achievement.title}</span>
            {achievement.bonusPoints > 0 && (
              <span className="text-[10px] font-bold text-amber-500 whitespace-nowrap">+{achievement.bonusPoints}</span>
            )}
          </div>
        </MotionDiv>
      )}
    </AnimatePresence>
  );
};

export default AchievementToast;
