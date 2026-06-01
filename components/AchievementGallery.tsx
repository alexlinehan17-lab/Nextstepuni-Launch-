/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 */

import React, { useState } from 'react';
import { MotionDiv } from './Motion';
import {
  Trophy, Star, Flame, BookOpen, Clock, Target, Award, Crown, Mountain, Zap,
  Eye, Brain, Lightbulb, Shield, Sparkles, HelpCircle,
  type LucideIcon,
} from 'lucide-react';
import { type AchievementCategory } from '../gamificationConfig';
import { ACHIEVEMENTS } from '../achievementData';

const ICON_MAP: Record<string, LucideIcon> = {
  Trophy, Star, Flame, BookOpen, Clock, Target, Award, Crown, Mountain, Zap,
  Eye, Brain, Lightbulb, Shield, Sparkles, HelpCircle,
  Footprints: Target, PlayCircle: Zap, BookCheck: BookOpen,
  Hash: Trophy, Milestone: Mountain, FolderCheck: BookOpen,
  CircleDot: Target, Timer: Clock, CalendarCheck: Clock,
  Calendar: Clock, PenLine: Brain, MessageSquare: Brain,
  NotebookPen: Brain, Compass: Target, ShieldCheck: Shield,
  ArrowUp: Zap, BarChart3: Target, Gem: Star, Sunrise: Star,
  Layers: BookOpen,
};

// Painted-blob + ink-illustration recipe per achievement category. Mirrors
// the WorldIconBlob aesthetic on the Library page so the Training Hub stops
// reading as a different design language. Soft pastel blob + saturated
// matching ink keeps each row visually distinct without a rainbow effect.
const BLOB_PATH = 'M 38 4 Q 12 6 6 28 Q 2 50 22 56 Q 50 62 60 36 Q 64 12 48 4 Q 42 2 38 4 Z';

const CATEGORY_PALETTE: Record<AchievementCategory, { blob: string; ink: string }> = {
  modules:      { blob: '#B8C9E5', ink: '#4361EE' },
  timetable:    { blob: '#FDD9A3', ink: '#F59E0B' },
  streaks:      { blob: '#F6C8B0', ink: '#F26B1F' },
  reflection:   { blob: '#C8E0D2', ink: '#3A8D5F' },
  'north-star': { blob: '#D4CCF0', ink: '#6C5CE7' },
  mastery:      { blob: '#E8D5A8', ink: '#B8941A' },
  journey:      { blob: '#A8D0C5', ink: '#2A7D6F' },
};

const BlobIcon: React.FC<{ category: AchievementCategory; Icon: LucideIcon; locked?: boolean }> = ({ category, Icon, locked }) => {
  const palette = CATEGORY_PALETTE[category];
  return (
    <div className="relative w-12 h-12 mb-2.5 shrink-0">
      <svg viewBox="0 0 64 64" className="absolute inset-0 w-full h-full" aria-hidden="true">
        <path d={BLOB_PATH} fill={locked ? '#E5E1DA' : palette.blob} opacity={locked ? 0.6 : 0.9} />
      </svg>
      <div className="absolute inset-0 flex items-center justify-center">
        <Icon size={22} style={{ color: locked ? '#A8A29E' : palette.ink }} />
      </div>
    </div>
  );
};

const CATEGORY_TABS: { id: AchievementCategory | 'all'; label: string }[] = [
  { id: 'all', label: 'All' },
  { id: 'modules', label: 'Modules' },
  { id: 'timetable', label: 'Timetable' },
  { id: 'streaks', label: 'Streaks' },
  { id: 'reflection', label: 'Reflections' },
  { id: 'north-star', label: 'North Star' },
  { id: 'mastery', label: 'Mastery' },
  { id: 'journey', label: 'Journey' },
];

interface AchievementGalleryProps {
  unlockedAchievements: string[];
  achievementTimestamps: Record<string, number>;
}

const AchievementGallery: React.FC<AchievementGalleryProps> = ({
  unlockedAchievements,
  achievementTimestamps,
}) => {
  const [activeTab, setActiveTab] = useState<AchievementCategory | 'all'>('all');
  const unlockedSet = new Set(unlockedAchievements);

  const filtered = activeTab === 'all'
    ? ACHIEVEMENTS
    : ACHIEVEMENTS.filter(a => a.category === activeTab);

  const unlocked = filtered.filter(a => unlockedSet.has(a.id));
  const locked = filtered.filter(a => !unlockedSet.has(a.id));

  return (
    <div className="space-y-4">
      {/* Header */}
      <div className="flex items-center justify-between">
        <h3 className="text-sm font-semibold uppercase tracking-widest text-zinc-400 dark:text-zinc-500">
          Achievements
        </h3>
        <span className="text-xs font-bold text-zinc-400 dark:text-zinc-500">
          {unlockedAchievements.length}/{ACHIEVEMENTS.filter(a => !a.isHidden || unlockedSet.has(a.id)).length}
        </span>
      </div>

      {/* Filter tabs */}
      <div className="flex gap-1.5 overflow-x-auto pb-1 -mx-1 px-1 scrollbar-none">
        {CATEGORY_TABS.map(tab => (
          <button
            key={tab.id}
            onClick={() => setActiveTab(tab.id)}
            className={`px-3 py-1.5 rounded-full text-[11px] font-semibold whitespace-nowrap transition-colors ${
              activeTab === tab.id
                ? 'bg-[var(--accent-hex)] text-white'
                : 'bg-zinc-100 dark:bg-zinc-800 text-zinc-500 dark:text-zinc-400 hover:bg-zinc-200 dark:hover:bg-zinc-700'
            }`}
          >
            {tab.label}
          </button>
        ))}
      </div>

      {/* Achievement grid */}
      <div className="grid grid-cols-2 sm:grid-cols-3 gap-3">
        {/* Unlocked achievements */}
        {unlocked.map((achievement, i) => {
          const Icon = ICON_MAP[achievement.icon] || Trophy;
          const timestamp = achievementTimestamps[achievement.id];
          const dateStr = timestamp ? new Date(timestamp).toLocaleDateString('en-IE', { day: 'numeric', month: 'short' }) : '';

          return (
            <MotionDiv
              key={achievement.id}
              initial={{ opacity: 0, scale: 0.95 }}
              animate={{ opacity: 1, scale: 1 }}
              transition={{ duration: 0.3, delay: i * 0.03 }}
              className="p-3.5 rounded-xl bg-white dark:bg-zinc-900 border border-zinc-200 dark:border-zinc-800 shadow-sm"
            >
              <BlobIcon category={achievement.category} Icon={Icon} />
              <p className="text-xs font-bold text-zinc-800 dark:text-white leading-tight mb-0.5">
                {achievement.title}
              </p>
              <p className="text-[10px] text-zinc-400 dark:text-zinc-500 leading-tight">
                {achievement.description}
              </p>
              {dateStr && (
                <p className="text-[9px] font-semibold text-zinc-300 dark:text-zinc-600 mt-1.5">
                  {dateStr}
                </p>
              )}
            </MotionDiv>
          );
        })}

        {/* Locked achievements */}
        {locked.map((achievement, i) => {
          const isHidden = achievement.isHidden;

          return (
            <MotionDiv
              key={achievement.id}
              initial={{ opacity: 0, scale: 0.95 }}
              animate={{ opacity: 1, scale: 1 }}
              transition={{ duration: 0.3, delay: (unlocked.length + i) * 0.03 }}
              className="p-3.5 rounded-xl bg-zinc-50 dark:bg-zinc-900/50 border border-zinc-200/50 dark:border-zinc-800/50 opacity-60"
            >
              <BlobIcon
                category={achievement.category}
                Icon={isHidden ? HelpCircle : (ICON_MAP[achievement.icon] || Trophy)}
                locked
              />
              <p className="text-xs font-bold text-zinc-400 dark:text-zinc-600 leading-tight mb-0.5">
                {isHidden ? '???' : achievement.title}
              </p>
              <p className="text-[10px] text-zinc-300 dark:text-zinc-700 leading-tight">
                {isHidden ? 'Hidden achievement' : achievement.description}
              </p>
            </MotionDiv>
          );
        })}
      </div>
    </div>
  );
};

export default AchievementGallery;
