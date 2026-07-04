/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 *
 * Paper Trail — practice streak + daily-goal strip (feature B3). A compact home
 * banner: the current practice streak and today's progress toward the daily
 * goal. Hidden until the student has practised at least once, so a brand-new
 * home stays clean (no demotivating "0-day streak").
 */

import React from 'react';
import { Flame, Check, ChevronRight } from 'lucide-react';
import { getStreak } from './streakStore';

const ACCENT = '#F26B1F';
const INK = '#1a1a1a';

interface Props {
  uid?: string;
  now: number;
  /** When set, the strip is a button that opens the progress dashboard. */
  onOpen?: () => void;
}

const StreakStrip: React.FC<Props> = ({ uid, now, onOpen }) => {
  const s = getStreak(uid, now);
  if (s.longest === 0 && s.todayCount === 0) return null;

  const pct = Math.min(100, Math.round((s.todayCount / s.goal) * 100));

  return (
    <div
      role={onOpen ? 'button' : undefined}
      tabIndex={onOpen ? 0 : undefined}
      onClick={onOpen}
      onKeyDown={onOpen ? e => { if (e.key === 'Enter' || e.key === ' ') { e.preventDefault(); onOpen(); } } : undefined}
      className={`w-full flex items-center gap-3 rounded-2xl border-2 border-[#1a1a1a] dark:border-zinc-700 bg-white dark:bg-zinc-900 px-4 py-3 mb-5${onOpen ? ' text-left cursor-pointer transition-transform active:translate-y-0.5 hover:-translate-y-0.5' : ''}`}
    >
      <span className="shrink-0 w-10 h-10 rounded-xl flex items-center justify-center" style={{ backgroundColor: '#FDEEDF' }}>
        <Flame size={19} style={{ color: ACCENT }} />
      </span>
      <span className="flex-1 min-w-0">
        <span className="block text-[15px] font-semibold" style={{ fontFamily: "'Source Serif 4', serif", color: INK }}>
          {s.current > 0 ? `${s.current}-day streak` : 'Keep your streak going'}
        </span>
        <span className="block text-[12px]" style={{ color: '#7a7068' }}>
          {s.current > 0
            ? s.activeToday
              ? `Longest: ${s.longest} day${s.longest === 1 ? '' : 's'}`
              : 'Practise today to keep it alive'
            : `Longest: ${s.longest} day${s.longest === 1 ? '' : 's'}`}
        </span>
      </span>
      {/* Daily goal */}
      <span className="shrink-0 text-right">
        <span className="flex items-center justify-end gap-1.5">
          {s.goalMet && <Check size={14} style={{ color: '#3A8D5F' }} />}
          <span className="text-[13px] font-bold tabular-nums" style={{ color: s.goalMet ? '#1F5F3E' : INK }}>
            {s.todayCount}/{s.goal}
          </span>
        </span>
        <span className="block mt-1 w-20 h-1.5 rounded-full overflow-hidden" style={{ backgroundColor: '#e0dbd4' }}>
          <span className="block h-full rounded-full transition-all" style={{ width: `${pct}%`, backgroundColor: s.goalMet ? '#3A8D5F' : ACCENT }} />
        </span>
        <span className="block text-[10px] mt-0.5" style={{ color: '#9e9186' }}>today’s goal</span>
      </span>
      {onOpen && <ChevronRight size={18} className="shrink-0" style={{ color: ACCENT }} />}
    </div>
  );
};

export default StreakStrip;
