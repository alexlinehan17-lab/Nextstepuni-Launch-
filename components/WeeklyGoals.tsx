/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 */

import React from 'react';
import { motion } from 'framer-motion';
import { MotionDiv } from './Motion';
import { BookOpen, Clock, PenLine, ChevronRight, Layers, Timer, MessageSquare, CalendarCheck, NotebookPen, CheckCircle2 } from 'lucide-react';
import { type WeeklyGoal, WEEKLY_GOAL_BONUS } from '../gamificationConfig';

const GOAL_ICONS: Record<string, React.ElementType> = {
  BookOpen, Clock, PenLine, Layers, Timer, MessageSquare, CalendarCheck, NotebookPen, ChevronRight,
};

interface WeeklyGoalsProps {
  goals: WeeklyGoal[];
  progress: Record<string, number>;
  weekStartDate: string;
}

const WeeklyGoals: React.FC<WeeklyGoalsProps> = ({ goals, progress, weekStartDate }) => {
  const completedGoals = goals.filter(g => (progress[g.metric] ?? 0) >= g.target).length;
  const bonusEarned = WEEKLY_GOAL_BONUS[completedGoals] ?? 0;
  const nextBonus = completedGoals < 3 ? WEEKLY_GOAL_BONUS[completedGoals + 1] ?? 0 : 0;

  // Calculate days until Monday reset
  const now = new Date();
  const day = now.getDay();
  const daysUntilMonday = day === 0 ? 1 : 8 - day;

  return (
    <div className="space-y-4">
      {/* Header */}
      <div className="flex items-center justify-between">
        <h3 className="text-sm font-semibold uppercase tracking-widest text-zinc-400 dark:text-zinc-500">
          This Week
        </h3>
        <span className="text-[10px] font-medium text-zinc-400 dark:text-zinc-500">
          Resets in {daysUntilMonday} day{daysUntilMonday !== 1 ? 's' : ''}
        </span>
      </div>

      {/* Goals */}
      <div className="space-y-3">
        {goals.map((goal, i) => {
          const current = progress[goal.metric] ?? 0;
          const pct = Math.min(100, Math.round((current / goal.target) * 100));
          const isComplete = current >= goal.target;
          const Icon = GOAL_ICONS[goal.icon] || BookOpen;

          return (
            <MotionDiv
              key={goal.id}
              initial={{ opacity: 0, y: 8 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.3, delay: i * 0.05 }}
              className={`p-3.5 rounded-xl border transition-colors ${
                isComplete
                  ? 'bg-emerald-50 dark:bg-emerald-900/10 border-emerald-200 dark:border-emerald-800/30'
                  : 'bg-white dark:bg-zinc-900 border-zinc-200 dark:border-zinc-800'
              }`}
            >
              <div className="flex items-center gap-3">
                <div className={`w-8 h-8 rounded-lg flex items-center justify-center shrink-0 ${
                  isComplete
                    ? 'bg-emerald-100 dark:bg-emerald-900/30'
                    : 'bg-zinc-100 dark:bg-zinc-800'
                }`}>
                  {isComplete
                    ? <CheckCircle2 size={16} className="text-emerald-500" />
                    : <Icon size={16} className="text-zinc-400 dark:text-zinc-500" />
                  }
                </div>
                <div className="flex-1 min-w-0">
                  <div className="flex items-center justify-between mb-1">
                    <p className={`text-sm font-medium ${
                      isComplete
                        ? 'text-emerald-700 dark:text-emerald-300'
                        : 'text-zinc-700 dark:text-zinc-300'
                    }`}>
                      {goal.label}
                    </p>
                    <span className={`text-xs font-bold ${
                      isComplete
                        ? 'text-emerald-500'
                        : 'text-zinc-400 dark:text-zinc-500'
                    }`}>
                      {Math.min(current, goal.target)}/{goal.target}
                    </span>
                  </div>
                  <div className="w-full h-1.5 bg-zinc-100 dark:bg-zinc-800 rounded-full overflow-hidden">
                    <motion.div
                      className={`h-full rounded-full ${
                        isComplete ? 'bg-emerald-500' : 'bg-[var(--accent-hex)]'
                      }`}
                      initial={{ width: 0 }}
                      animate={{ width: `${pct}%` }}
                      transition={{ duration: 0.8, ease: 'easeOut' }}
                    />
                  </div>
                </div>
              </div>
            </MotionDiv>
          );
        })}
      </div>

      {/* Bonus escalation */}
      <div className="flex items-center justify-between p-3 rounded-xl bg-zinc-50 dark:bg-zinc-800/50 border border-zinc-200/50 dark:border-zinc-800">
        <div className="flex items-center gap-2">
          <span className="text-[10px] font-semibold uppercase tracking-wider text-zinc-400 dark:text-zinc-500">
            Weekly Bonus
          </span>
          <div className="flex gap-1">
            {[1, 2, 3].map(n => (
              <div
                key={n}
                className={`w-2 h-2 rounded-full ${
                  completedGoals >= n
                    ? 'bg-[var(--accent-hex)]'
                    : 'bg-zinc-200 dark:bg-zinc-700'
                }`}
              />
            ))}
          </div>
        </div>
        <span className="text-xs font-bold text-[var(--accent-hex)]">
          {bonusEarned > 0 ? `+${bonusEarned} pts earned` : nextBonus > 0 ? `+${nextBonus} pts next` : ''}
        </span>
      </div>
    </div>
  );
};

export default WeeklyGoals;
