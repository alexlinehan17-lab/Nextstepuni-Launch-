/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 *
 * Launch-day view of the first-run funnel.
 *
 * The question this exists to answer, within an hour of a cohort arriving:
 * are students getting in? Two onboarding-fatal bugs shipped unnoticed before
 * this existed (2026-08-17), because nothing measured the path from account
 * created to tool opened.
 *
 * Reads the aggregate counts only — `getCountFromServer` never pulls the
 * documents, so this stays cheap however many events accumulate, and no event
 * body is ever loaded into the browser. See `utils/funnel.ts` for what is
 * stored (nothing personal) and why this is first-party rather than GA4.
 */
import React, { useCallback, useEffect, useState } from 'react';
import { collection, getCountFromServer, query, where } from 'firebase/firestore';
import { RefreshCw, TriangleAlert } from 'lucide-react';
import { db } from '../firebase';
import { FUNNEL_STEPS, type FunnelStep } from '../utils/funnel';

/** Local (Irish) calendar day — never toISOString, which rolls back a day at UTC+1. */
function localDay(offsetDays = 0): string {
  const date = new Date();
  date.setDate(date.getDate() - offsetDays);
  const month = String(date.getMonth() + 1).padStart(2, '0');
  const day = String(date.getDate()).padStart(2, '0');
  return `${date.getFullYear()}-${month}-${day}`;
}

const STEP_LABELS: Record<FunnelStep, string> = {
  register_succeeded: 'Account created',
  onboarding_started: 'Onboarding opened',
  onboarding_reached_subjects: 'Reached subjects',
  onboarding_reached_exam_date: 'Reached exam date',
  onboarding_completed: 'Onboarding completed',
  onboarding_skipped: 'Onboarding skipped',
  first_tool_opened: 'Opened a tool',
};

/** The ordered path a student walks. `onboarding_skipped` is a branch, not a stage. */
const FUNNEL_PATH: FunnelStep[] = [
  'register_succeeded',
  'onboarding_started',
  'onboarding_reached_subjects',
  'onboarding_reached_exam_date',
  'onboarding_completed',
  'first_tool_opened',
];

const RANGES = [
  { id: 'today', label: 'Today', days: 1 },
  { id: 'week', label: 'Last 7 days', days: 7 },
] as const;

type RangeId = (typeof RANGES)[number]['id'];

const AdminFunnelPanel: React.FC = () => {
  const [range, setRange] = useState<RangeId>('today');
  const [counts, setCounts] = useState<Record<string, number>>({});
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState('');

  const load = useCallback(async () => {
    setIsLoading(true);
    setError('');
    try {
      const days = RANGES.find(r => r.id === range)?.days ?? 1;
      const dayKeys = Array.from({ length: days }, (_, i) => localDay(i));
      const events = collection(db, 'funnelEvents');
      // One count per (step × day). `in` takes at most 30 values, and 7 days is
      // well inside that, so each step is a single aggregation query.
      const entries = await Promise.all(FUNNEL_STEPS.map(async step => {
        const snapshot = await getCountFromServer(query(
          events,
          where('day', 'in', dayKeys),
          where('step', '==', step),
        ));
        return [step, snapshot.data().count] as const;
      }));
      setCounts(Object.fromEntries(entries));
    } catch (loadError) {
      console.error('Error loading funnel counts:', loadError);
      setError('Funnel counts could not be loaded. Confirm the latest Firestore rules and indexes are deployed.');
    } finally {
      setIsLoading(false);
    }
  }, [range]);

  useEffect(() => { void load(); }, [load]);

  const top = counts[FUNNEL_PATH[0]] ?? 0;
  const completed = counts.onboarding_completed ?? 0;
  const started = counts.register_succeeded ?? 0;
  // The number that matters on launch day: of everyone who made an account,
  // how many actually got through setup?
  const throughRate = started > 0 ? Math.round((completed / started) * 100) : null;

  return (
    <section aria-label="First-run funnel">
      <div className="mb-5 flex flex-wrap items-center justify-between gap-3">
        <div>
          <h2 className="font-serif text-xl font-semibold text-[#1A1A1A]">Are students getting in?</h2>
          <p className="mt-1 text-sm text-[#7A7068]">
            Each student is counted once per visit, at the furthest step they reached.
          </p>
        </div>
        <div className="flex items-center gap-2">
          {RANGES.map(option => (
            <button
              key={option.id}
              type="button"
              onClick={() => setRange(option.id)}
              aria-pressed={range === option.id}
              className="rounded-full border-2 px-3 py-1.5 text-xs font-bold"
              style={{
                borderColor: range === option.id ? '#F26B1F' : '#1A1A1A',
                backgroundColor: range === option.id ? '#F26B1F' : '#FFFFFF',
                color: range === option.id ? '#FFFFFF' : '#1A1A1A',
              }}
            >
              {option.label}
            </button>
          ))}
          <button
            type="button"
            onClick={() => void load()}
            aria-label="Refresh funnel counts"
            className="flex h-8 w-8 items-center justify-center rounded-full border-2 border-[#1A1A1A] bg-white text-[#1A1A1A]"
          >
            <RefreshCw size={14} className={isLoading ? 'animate-spin' : undefined} />
          </button>
        </div>
      </div>

      {error && (
        <p role="alert" className="mb-4 flex items-start gap-2 rounded-xl border-2 border-[#B54D14] bg-[#FDEEDF] px-4 py-3 text-sm text-[#8C3A0E]">
          <TriangleAlert size={16} className="mt-0.5 shrink-0" />
          {error}
        </p>
      )}

      {throughRate !== null && (
        <div className="mb-6 rounded-2xl border-2 border-[#1A1A1A] bg-white p-5">
          <p className="text-[11px] font-bold uppercase tracking-[0.16em] text-[#9E9186]">
            Made an account → finished setup
          </p>
          <p className="mt-1 font-serif text-4xl font-bold" style={{ color: throughRate >= 70 ? '#3A8D5F' : '#F26B1F' }}>
            {throughRate}%
          </p>
          <p className="mt-1 text-sm text-[#7A7068]">
            {completed} of {started}. If this drops, the front door is broken — check the newest step with a fall-off below.
          </p>
        </div>
      )}

      <ol className="space-y-2">
        {FUNNEL_PATH.map((step, index) => {
          const value = counts[step] ?? 0;
          const previous = index === 0 ? value : (counts[FUNNEL_PATH[index - 1]] ?? 0);
          const lost = Math.max(0, previous - value);
          const width = top > 0 ? Math.round((value / top) * 100) : 0;
          return (
            <li key={step} className="rounded-xl border-2 border-[#1A1A1A] bg-white p-4">
              <div className="flex items-baseline justify-between gap-4">
                <span className="text-sm font-semibold text-[#1A1A1A]">{STEP_LABELS[step]}</span>
                <span className="font-serif text-xl font-bold tabular-nums text-[#1A1A1A]">{value}</span>
              </div>
              <div className="mt-2 h-2 w-full overflow-hidden rounded-full bg-[#E0DBD4]">
                <div className="h-full rounded-full" style={{ width: `${width}%`, background: '#F26B1F' }} />
              </div>
              {index > 0 && lost > 0 && (
                <p className="mt-2 text-xs text-[#7A7068]">
                  &minus;{lost} lost here{previous > 0 ? ` (${Math.round((lost / previous) * 100)}%)` : ''}
                </p>
              )}
            </li>
          );
        })}
      </ol>

      <p className="mt-5 text-xs leading-relaxed text-[#7A7068]">
        Skipped onboarding: <strong>{counts.onboarding_skipped ?? 0}</strong>. Students who abandon on the
        registration form itself are not counted — writing here requires a signed-in account, so that gap is
        deliberate (see <code>utils/funnel.ts</code>).
      </p>
    </section>
  );
};

export default AdminFunnelPanel;
