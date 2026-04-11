/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 */

import React from 'react';
import { MotionDiv } from './Motion';
import {
  ArrowLeft, TrendingUp, Clock, RefreshCw, Flame, BarChart3, Sparkles, Lightbulb,
  Zap, BookOpen, Calendar, Target,
} from 'lucide-react';
import { type StreakData } from '../hooks/useStreak';
import { type StrategyMasteryMap } from '../types';
import { useInsights, type Insight } from '../hooks/useInsights';

// FIX: Cast motion components to any to bypass broken type definitions

const ICON_MAP: Record<string, React.FC<{ size?: number; className?: string }>> = {
  TrendingUp,
  Clock,
  RefreshCw,
  Flame,
  BarChart3,
  Sparkles,
  Lightbulb,
  Zap,
  BookOpen,
  Calendar,
  Target,
};

interface InsightsViewProps {
  uid: string;
  streak: StreakData;
  strategyMastery: StrategyMasteryMap;
  onBack: () => void;
}

function InsightCard({ insight, index }: { insight: Insight; index: number }) {
  const IconComponent = ICON_MAP[insight.icon] ?? Lightbulb;

  return (
    <MotionDiv
      initial={{ opacity: 0, y: 16 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.35, delay: 0.08 * index }}
      className="bg-white dark:bg-zinc-900 border border-zinc-200 dark:border-zinc-800 rounded-xl p-4 flex items-start gap-4"
    >
      <div className={`w-10 h-10 rounded-lg flex items-center justify-center shrink-0 ${
        insight.iconColor.includes('emerald') ? 'bg-emerald-50 dark:bg-emerald-500/10' :
        insight.iconColor.includes('blue') ? 'bg-blue-50 dark:bg-blue-500/10' :
        insight.iconColor.includes('violet') ? 'bg-violet-50 dark:bg-violet-500/10' :
        insight.iconColor.includes('purple') ? 'bg-purple-50 dark:bg-purple-500/10' :
        insight.iconColor.includes('orange') ? 'bg-orange-50 dark:bg-orange-500/10' :
        insight.iconColor.includes('amber') ? 'bg-amber-50 dark:bg-amber-500/10' :
        insight.iconColor.includes('pink') ? 'bg-pink-50 dark:bg-pink-500/10' :
        insight.iconColor.includes('teal') ? 'bg-teal-50 dark:bg-teal-500/10' :
        insight.iconColor.includes('rose') ? 'bg-rose-50 dark:bg-rose-500/10' :
        insight.iconColor.includes('indigo') ? 'bg-indigo-50 dark:bg-indigo-500/10' :
        'bg-zinc-100 dark:bg-zinc-800'
      }`}>
        <IconComponent size={18} className={insight.iconColor} />
      </div>
      <div className="min-w-0">
        <p className="font-semibold text-zinc-800 dark:text-white text-sm leading-snug">{insight.title}</p>
        <p className="text-xs text-zinc-500 dark:text-zinc-400 mt-0.5 leading-relaxed">{insight.description}</p>
      </div>
    </MotionDiv>
  );
}

const InsightsView: React.FC<InsightsViewProps> = ({ uid, streak, strategyMastery, onBack }) => {
  const { insights, isLoaded } = useInsights(uid, streak, strategyMastery);

  return (
    <div className="min-h-screen bg-zinc-50 dark:bg-zinc-950 pt-16 md:pt-24 pb-40 md:pb-32 px-4 sm:px-6 transition-colors duration-500">
      <div className="max-w-3xl mx-auto">
        {/* Header */}
        <div className="flex items-center gap-4 mb-10">
          <button
            onClick={onBack}
            className="w-10 h-10 rounded-xl bg-white dark:bg-zinc-900 border border-zinc-200 dark:border-zinc-800 flex items-center justify-center hover:bg-zinc-50 dark:hover:bg-zinc-800 transition-colors"
          >
            <ArrowLeft size={18} className="text-zinc-600 dark:text-zinc-400" />
          </button>
          <div>
            <h1 className="font-serif text-3xl md:text-4xl font-bold text-zinc-900 dark:text-white">Your Insights</h1>
            <p className="text-sm text-zinc-500 dark:text-zinc-400 mt-1">Patterns from your study data</p>
          </div>
        </div>

        {/* Content */}
        {!isLoaded ? (
          <div className="flex items-center justify-center py-20">
            <div className="w-6 h-6 border-2 border-zinc-300 dark:border-zinc-600 border-t-transparent rounded-full animate-spin" />
          </div>
        ) : insights.length === 0 ? (
          <MotionDiv
            initial={{ opacity: 0, y: 12 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.4 }}
            className="text-center py-20"
          >
            <div className="w-14 h-14 mx-auto rounded-2xl bg-amber-50 dark:bg-amber-500/10 flex items-center justify-center mb-4">
              <Lightbulb size={24} className="text-amber-500" />
            </div>
            <p className="text-zinc-600 dark:text-zinc-400 text-sm font-medium">Keep studying — insights will appear as you build more data.</p>
          </MotionDiv>
        ) : (
          <div className="space-y-3">
            {insights.map((insight, i) => (
              <InsightCard key={insight.id} insight={insight} index={i} />
            ))}
          </div>
        )}
      </div>
    </div>
  );
};

export default InsightsView;
