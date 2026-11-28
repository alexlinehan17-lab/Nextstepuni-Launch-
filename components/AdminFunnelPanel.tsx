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
import { RefreshCw } from 'lucide-react';
import { db } from '../firebase';
import { FUNNEL_STEPS, type FunnelStep } from '../utils/funnel';
import { TopBar } from './ui/Bars';
import { IconButton } from './ui/Button';
import { SelectionBar } from './ui/Choice';
import { PaperSheet } from './ui/List';
import { Fig } from './gc/gcView';

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

/**
 * The first-run counts over the last `days` local calendar days: one aggregation per (step × days).
 * `in` takes at most 30 values, and 7 days is well inside that, so each step is a single count query.
 * The First run page and the Overview's second row both read through this, so they cannot disagree.
 */
export async function loadFunnelCounts(days: number): Promise<Record<string, number>> {
  const dayKeys = Array.from({ length: days }, (_, i) => localDay(i));
  const events = collection(db, 'funnelEvents');
  const entries = await Promise.all(FUNNEL_STEPS.map(async step => {
    const snapshot = await getCountFromServer(query(
      events,
      where('day', 'in', dayKeys),
      where('step', '==', step),
    ));
    return [step, snapshot.data().count] as const;
  }));
  return Object.fromEntries(entries);
}

/** The arithmetic read from those counts, shared by the page and the Overview's row. */
export function funnelSummary(counts: Record<string, number>) {
  const started = counts.register_succeeded ?? 0;
  const completed = counts.onboarding_completed ?? 0;
  return {
    started,
    completed,
    // The number that matters on launch day: of everyone who made an account,
    // how many actually got through setup?
    throughRate: started > 0 ? Math.round((completed / started) * 100) : null,
    // Made an account but never reached the subjects step.
    stoppedBeforeSubjects: Math.max(0, started - (counts.onboarding_reached_subjects ?? 0)),
  };
}

interface AdminFunnelPanelProps {
  /** On a phone the page is reached from Overview's second row: Back to it, and the page's Refresh
   *  in the bar (the agreed board). Without it the panel is the page's body (a laptop). */
  onBack?: () => void;
}

const AdminFunnelPanel: React.FC<AdminFunnelPanelProps> = ({ onBack }) => {
  const [range, setRange] = useState<RangeId>('today');
  const [counts, setCounts] = useState<Record<string, number>>({});
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState('');

  const load = useCallback(async () => {
    setIsLoading(true);
    setError('');
    try {
      const days = RANGES.find(r => r.id === range)?.days ?? 1;
      setCounts(await loadFunnelCounts(days));
    } catch (loadError) {
      console.error('Error loading funnel counts:', loadError);
      setError('Funnel counts could not be loaded. Confirm the latest Firestore rules and indexes are deployed.');
    } finally {
      setIsLoading(false);
    }
  }, [range]);

  useEffect(() => { void load(); }, [load]);

  const top = counts[FUNNEL_PATH[0]] ?? 0;
  const { started, completed, throughRate } = funnelSummary(counts);

  const refresh = (
    <IconButton
      label="Refresh funnel counts"
      className="adm-refresh"
      onClick={() => void load()}
      icon={<RefreshCw className={`ui-icon${isLoading ? ' adm-spin' : ''}`} width={20} height={20} strokeWidth={1.75} aria-hidden="true" />}
    />
  );

  const body = (
    <section aria-label="First-run funnel" className="adm-funnel">
      <header className="gc8-head adm-head">
        <p className="gc8-label">First run</p>
        <div className="adm-titlerow">
          <h1 className="gc8-title">Are students getting in?</h1>
          {onBack ? null : refresh}
        </div>
        <p className="gc8-sub">
          Each student is counted once per visit, at the furthest step they reached.
        </p>
        <SelectionBar
          label="Period"
          size="md"
          className="adm-seg2"
          options={RANGES.map(option => ({ value: option.id, label: option.label }))}
          value={range}
          onChange={value => setRange(value as RangeId)}
        />
      </header>

      {error && <p role="alert" className="adm-alert">{error}</p>}

      {throughRate !== null && (
        <PaperSheet className="adm-through" label="Made an account, then finished setup">
          <p className="gc8-label">Made an account → finished setup</p>
          {/* The headline figure in ink (the agreed board: not green or orange). */}
          <p className="gc8-num adm-throughnum"><Fig value={throughRate} unit="%" /></p>
          <p className="gc8-sub">
            {completed} of {started}. If this drops, the front door is broken: check the newest step with a fall-off below.
          </p>
        </PaperSheet>
      )}

      <ol className="adm-steps">
        {FUNNEL_PATH.map((step, index) => {
          const value = counts[step] ?? 0;
          const previous = index === 0 ? value : (counts[FUNNEL_PATH[index - 1]] ?? 0);
          const lost = Math.max(0, previous - value);
          const width = top > 0 ? Math.round((value / top) * 100) : 0;
          return (
            <li key={step}>
              <div className="adm-stephead">
                <span>{STEP_LABELS[step]}</span>
                <span className="adm-count">{value}</span>
              </div>
              <span className="gc8-bar adm-livebar" aria-hidden="true"><i style={{ width: `${width}%` }} /></span>
              {index > 0 && lost > 0 && (
                <p className="adm-lost">
                  &minus;{lost} lost here{previous > 0 ? ` (${Math.round((lost / previous) * 100)}%)` : ''}
                </p>
              )}
            </li>
          );
        })}
      </ol>

      <p className="gc8-meta adm-foot">
        Skipped onboarding: <b>{counts.onboarding_skipped ?? 0}</b>. Students who abandon on the
        registration form itself are not counted. Writing here requires a signed-in account, so that gap is
        deliberate.
      </p>
    </section>
  );

  if (!onBack) return body;
  return (
    <>
      <TopBar className="gc8-placebar adm-pagebar" leave={{ kind: 'back', onPress: onBack, label: 'Back to Overview' }} action={refresh} />
      <main className="gc8-main adm-main">{body}</main>
    </>
  );
};

export default AdminFunnelPanel;
