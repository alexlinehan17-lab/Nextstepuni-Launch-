/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 *
 * Paper Trail — exam countdown + daily focus (feature A3). The student sets their
 * own exam (or first-paper) date; the card then shows a live day countdown and a
 * derived focus for today: cards due, the weakest topic to drill, and an honest
 * weekly pace to clear their weak topics before the date. Every number is
 * computed from the student's own data — no invented SEC timetable, no promises.
 */

import React, { useEffect, useState } from 'react';
import { CalendarDays, ChevronRight, Pencil } from 'lucide-react';
import { getExamDate, setExamDate, daysUntil } from './examDateStore';
import { dayKey } from './streakStore';
import { computeProgress } from './progressStats';
import { topicLabel } from './topics';

const INK = '#1a1a1a';
const ACCENT = '#F26B1F';
const BLUE_TINT = '#E8EFF5';

const MONTHS = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'];
const prettyDate = (iso: string) => {
  const [y, m, d] = iso.split('-').map(Number);
  return `${d} ${MONTHS[m - 1]} ${y}`;
};

const ISO = /^\d{4}-\d{2}-\d{2}$/;

interface Props {
  uid?: string;
  now: number;
  onOpen?: () => void;
  /** The exam start date the student gave at onboarding (subjectProfile
   *  .examStartDate, ISO). Used to pre-fill the countdown so a student never
   *  has to re-enter a date they already told us. A locally-set date always
   *  wins (they can still edit it here). */
  onboardingExamDate?: string;
}

const CountdownCard: React.FC<Props> = ({ uid, now, onOpen, onboardingExamDate }) => {
  const onboardingSeed = onboardingExamDate && ISO.test(onboardingExamDate) ? onboardingExamDate : null;
  const [date, setDate] = useState<string | null>(() => getExamDate(uid) ?? onboardingSeed);
  const [editing, setEditing] = useState(false);
  const [draft, setDraft] = useState(date ?? '');

  // Persist the onboarding date to the Paper Trail store the first time, so the
  // countdown is consistent across the tool and survives a reload — without
  // clobbering a date the student has since set/edited here.
  useEffect(() => {
    if (onboardingSeed && !getExamDate(uid)) setExamDate(uid, onboardingSeed);
  }, [uid, onboardingSeed]);

  const save = () => {
    if (!draft) return;
    setExamDate(uid, draft);
    setDate(draft);
    setEditing(false);
  };

  // ── Set / edit form ──
  if (editing || !date) {
    return (
      <div className="w-full rounded-2xl border-2 border-[#1a1a1a] dark:border-zinc-700 bg-white dark:bg-zinc-900 px-4 py-3.5 mb-5">
        <div className="flex items-center gap-2 mb-2">
          <CalendarDays size={17} style={{ color: ACCENT }} />
          <span className="text-[14px] font-semibold" style={{ fontFamily: "'Source Serif 4', serif", color: INK }}>
            {date ? 'Change your exam date' : 'Set your exam date'}
          </span>
        </div>
        {!date && (
          <p className="text-[12.5px] mb-2.5" style={{ color: '#7a7068' }}>
            Add the date of your first paper for a live countdown and a daily focus.
          </p>
        )}
        <div className="flex items-center gap-2">
          <input
            type="date"
            value={draft}
            min={dayKey(now)}
            onChange={e => setDraft(e.target.value)}
            aria-label="Exam date"
            className="flex-1 px-3 py-2 rounded-xl border-2 border-zinc-200 dark:border-zinc-700 bg-white dark:bg-zinc-900 text-[13.5px] outline-none focus:border-[#1a1a1a] dark:focus:border-zinc-400"
          />
          <button
            onClick={save}
            disabled={!draft}
            className="px-4 py-2 rounded-full text-[13px] font-semibold text-white disabled:opacity-40 transition-transform active:translate-y-0.5"
            style={{ backgroundColor: ACCENT, boxShadow: '0 3px 0 #B54D14' }}
          >
            Save
          </button>
          {date && (
            <button onClick={() => setEditing(false)} className="px-3 py-2 rounded-full text-[13px] font-medium" style={{ color: '#7a7068' }}>
              Cancel
            </button>
          )}
        </div>
      </div>
    );
  }

  // ── Countdown + focus ──
  const days = daysUntil(date, now);
  const p = computeProgress(uid, now);
  const weakest = p.weakestTopics.find(t => t.avg < 50) ?? p.weakestTopics[0];
  const weakCount = p.weakestTopics.filter(t => t.avg < 50).length;
  const weeks = Math.max(1, Math.ceil(days / 7));
  const perWeek = weakCount > 0 ? Math.ceil(weakCount / weeks) : 0;

  const passed = days < 0;
  const focusBits: string[] = [];
  if (!passed) {
    if (p.deck.due > 0) focusBits.push(`${p.deck.due} review card${p.deck.due === 1 ? '' : 's'} due`);
    if (weakest) focusBits.push(`drill ${topicLabel(weakest.subtopicId)}`);
  }

  return (
    <div
      role={onOpen ? 'button' : undefined}
      tabIndex={onOpen ? 0 : undefined}
      onClick={onOpen}
      onKeyDown={onOpen ? e => { if (e.key === 'Enter' || e.key === ' ') { e.preventDefault(); onOpen(); } } : undefined}
      className={`w-full rounded-2xl border-2 border-[#1a1a1a] dark:border-zinc-700 bg-white dark:bg-zinc-900 shadow-[4px_4px_0_0_#1a1a1a] dark:shadow-[4px_4px_0_0_#3f3f46] px-4 py-3.5 mb-5${onOpen ? ' cursor-pointer transition-transform active:translate-y-0.5 hover:-translate-y-0.5' : ''}`}
    >
      <div className="flex items-center gap-3">
        <span className="shrink-0 w-12 h-12 rounded-xl flex flex-col items-center justify-center" style={{ backgroundColor: passed ? BLUE_TINT : '#FDEEDF' }}>
          {passed ? (
            <CalendarDays size={20} style={{ color: '#33658A' }} />
          ) : (
            <>
              <span className="text-[18px] font-bold leading-none tabular-nums" style={{ fontFamily: "'Source Serif 4', serif", color: ACCENT }}>{days}</span>
              <span className="text-[8.5px] font-bold uppercase tracking-wide" style={{ color: '#8C3A0E' }}>days</span>
            </>
          )}
        </span>
        <span className="flex-1 min-w-0">
          <span className="block text-[15px] font-semibold" style={{ fontFamily: "'Source Serif 4', serif", color: INK }}>
            {passed ? 'Exam date passed' : days === 0 ? 'Your exam is today — good luck' : `${days} day${days === 1 ? '' : 's'} to your exam`}
          </span>
          <span className="block text-[12px]" style={{ color: '#7a7068' }}>
            {passed
              ? `Was ${prettyDate(date)} — set a new date`
              : focusBits.length
                ? `Today: ${focusBits.join(' · ')}`
                : `Exam on ${prettyDate(date)}`}
          </span>
          {!passed && perWeek > 0 && (
            <span className="block text-[11px] mt-0.5" style={{ color: '#9e9186' }}>
              ≈{perWeek} weak topic{perWeek === 1 ? '' : 's'}/week to clear {weakCount} before then
            </span>
          )}
        </span>
        <button
          onClick={e => { e.stopPropagation(); setDraft(date); setEditing(true); }}
          aria-label="Change exam date"
          className="shrink-0 w-8 h-8 rounded-lg flex items-center justify-center border-2"
          style={{ borderColor: '#d0cdc8', color: '#9e9186' }}
        >
          <Pencil size={14} />
        </button>
        {onOpen && <ChevronRight size={18} className="shrink-0" style={{ color: ACCENT }} />}
      </div>
    </div>
  );
};

export default CountdownCard;
