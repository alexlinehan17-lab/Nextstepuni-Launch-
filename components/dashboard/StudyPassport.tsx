/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 *
 * The Study Passport — the account's all-time record as a dark enamel
 * card, copied from Flighty's passport register: huge serif numerals,
 * small-caps labels, one warm accent. Deliberately the only dark card
 * in the dashboard; it is an artifact, not a surface.
 */

import React, { useMemo } from 'react';
import { type StreakData } from '../../hooks/useStreak';
import { type StudySessionRecord } from '../../utils/strategyRegistry';

const IVORY = '#F5F1EA';
const IVORY_DIM = 'rgba(245, 241, 234, 0.55)';
const EDGE = 'rgba(245, 241, 234, 0.12)';

interface Props {
  streak: StreakData;
  sessions: StudySessionRecord[];
  totalXP: number;
  badgesEarned: number;
  badgesVisible: number;
}

const StudyPassport: React.FC<Props> = ({ streak, sessions, totalXP, badgesEarned, badgesVisible }) => {
  const record = useMemo(() => {
    let seconds = 0;
    let firstYear: number | null = null;
    for (const s of sessions) {
      seconds += s.actualSeconds || 0;
      const y = new Date(s.startedAt || s.completedAt || Date.now()).getFullYear();
      if (Number.isFinite(y) && (firstYear === null || y < firstYear)) firstYear = y;
    }
    const hours = seconds / 3600;
    return {
      hours: hours >= 10 ? String(Math.round(hours)) : (Math.round(hours * 10) / 10).toString(),
      sessions: sessions.length,
      firstYear,
    };
  }, [sessions]);

  const cells: Array<{ v: string; l: string; warm?: boolean }> = [
    { v: String(streak.currentStreak), l: 'Day streak', warm: true },
    { v: String(streak.longestStreak), l: 'Longest streak' },
    { v: record.sessions.toLocaleString(), l: 'Sessions' },
    { v: `${record.hours}h`, l: 'Focused time' },
    { v: totalXP.toLocaleString(), l: 'Total XP' },
    { v: `${badgesEarned}/${badgesVisible}`, l: 'Badges' },
  ];

  return (
    <article
      className="lg:col-span-12 rounded-[18px] px-6 py-5 sm:px-8 sm:py-6"
      style={{ backgroundColor: '#1A1A1A', border: `1.5px solid ${EDGE}` }}
      aria-label="Study Passport — all-time record"
    >
      <div className="flex items-baseline justify-between gap-4">
        <p className="text-[10px] font-bold uppercase tracking-[0.22em]" style={{ color: IVORY_DIM }}>
          NextStep · Study Passport
        </p>
        <p className="text-[10px] font-semibold uppercase tracking-[0.16em] tabular-nums" style={{ color: IVORY_DIM }}>
          {record.firstYear ? `Est. ${record.firstYear}` : 'All-time'}
        </p>
      </div>
      <div className="mt-5 grid grid-cols-2 gap-y-6 sm:grid-cols-3 lg:grid-cols-6">
        {cells.map((cell, i) => (
          <div
            key={cell.l}
            className={`px-1 ${i > 0 ? 'sm:border-l sm:pl-5' : ''}`}
            style={i > 0 ? { borderColor: EDGE } : undefined}
          >
            <p
              className="font-serif text-[30px] font-semibold leading-none tabular-nums"
              style={{ color: cell.warm ? 'rgba(242, 138, 66, 0.95)' : IVORY }}
            >
              {cell.v}
            </p>
            <p className="mt-2 text-[9px] font-bold uppercase tracking-[0.16em]" style={{ color: IVORY_DIM }}>
              {cell.l}
            </p>
          </div>
        ))}
      </div>
      <p className="mt-5 border-t pt-3 text-[10px]" style={{ borderColor: EDGE, color: IVORY_DIM }}>
        The permanent record — every focused minute counts toward it.
      </p>
    </article>
  );
};

export default StudyPassport;
