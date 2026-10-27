/**
 * Dev-only "Now" pane for the planner and the native-select sweep (review section 07).
 *
 * Mounts the REAL components on local sample data, no account and no network:
 *  - components/launchpad/PlannerWorkbench.tsx with the props SpacedRepetitionTimetable.tsx
 *    passes it (the week is the real planner algorithm, see kobra-review/sections/planner-demo.ts),
 *    including the real PlannerExplanation behind "See the allocation in detail".
 *  - Beneath it, three real components that still render a browser <select>:
 *    launchpad/SubjectPicker.tsx and launchpad/LaunchpadSelect.tsx as the Catch-Up Lane
 *    aside uses them (CatchUpLane/index.tsx:174-175), and activities/KanbanBoard.tsx inside the
 *    module reader's scope (ModuleLayout.tsx:259), as the Reframing Progress module shows it.
 */
import { Suspense, lazy, useMemo, useState, type CSSProperties } from 'react';
import KobraScope, { Button } from '../../components/approved-ui-runtime';
import PlannerWorkbench, { type PlannerEntry } from '../../components/launchpad/PlannerWorkbench';
import PlannerExplanation from '../../components/launchpad/PlannerExplanation';
import SubjectPicker from '../../components/launchpad/SubjectPicker';
import LaunchpadSelect from '../../components/launchpad/LaunchpadSelect';
import KanbanBoard from '../../components/activities/KanbanBoard';
import type { PlanCue, PlanCues } from '../../hooks/usePlanCues';
import '../../components/learning/learning.css';
import '../../components/learning/module-brand-review.css';
import {
  CATCH_UP_LEVELS, DEMO_DURATION, DEMO_REST_DAYS, DEMO_SUBJECT_NAMES, DEMO_UID, EXPLAIN_DETAIL, EXPLAIN_SENIOR, EXPLAIN_SPREAD,
  catchUpOptions, demoCompletions, demoPlan, type CatchUpLevel,
} from '../sections/planner-demo';

// ?still=1 is for headless screenshots only: virtual time does not advance the
// planner's arrival animations, so they are finished as they start.
if (new URLSearchParams(window.location.search).has('still')) {
  window.setInterval(() => document.getAnimations().forEach(animation => animation.finish()), 100);
}

const caption: CSSProperties = { margin: '0 0 10px', font: "500 12px/1.5 'DM Sans', sans-serif", color: 'var(--ink-secondary)' };
const code: CSSProperties = { font: '500 12px/1.5 ui-monospace, SFMono-Regular, Menlo, monospace', color: 'var(--ink-primary)' };

function Planner() {
  const [weekOffset, setWeekOffset] = useState(0);
  const [restDays, setRestDays] = useState(DEMO_REST_DAYS);
  const [duration, setDuration] = useState(DEMO_DURATION);
  const [completions, setCompletions] = useState(demoCompletions);
  const [deferred, setDeferred] = useState<string[]>([]);
  const [cues, setCues] = useState<PlanCues>({});
  const [showExplainer, setShowExplainer] = useState(false);
  const plan = useMemo(() => demoPlan(weekOffset, restDays, duration), [weekOffset, restDays, duration]);
  const toggle = (entry: PlannerEntry, done: boolean) => setCompletions(current => {
    const day = current[entry.dateKey] ?? [];
    return { ...current, [entry.dateKey]: done ? [...day, entry.id] : day.filter(id => id !== entry.id) };
  });
  return (
    <PlannerWorkbench uid={DEMO_UID} timetable={plan.timetable} subjects={DEMO_SUBJECT_NAMES} weekStart={plan.weekStart} weekOffset={weekOffset}
      onWeekChange={setWeekOffset} restDays={restDays} duration={duration} onSettings={() => {}}
      onPlanSettingsChange={(days, minutes) => { setRestDays(days); setDuration(minutes); }}
      isComplete={entry => completions[entry.dateKey]?.includes(entry.id) ?? false}
      isSkipped={entry => deferred.includes(entry.key)} isDeferred={entry => deferred.includes(entry.key)}
      onComplete={toggle} onSkip={(entry, skipped) => setDeferred(current => skipped ? [...current, entry.key] : current.filter(key => key !== entry.key))}
      onStudy={() => {}} schoolEvents={[]} hints={{}} cues={cues} onCueSave={(id: string, cue: PlanCue) => setCues(current => ({ ...current, [id]: cue }))}
      explanation={<><p>{plan.weeklyTarget.explanation}</p><p>{EXPLAIN_SPREAD}</p><p>{EXPLAIN_SENIOR}</p><Button variant="ghost" onClick={() => setShowExplainer(true)}>{EXPLAIN_DETAIL}</Button><PlannerExplanation open={showExplainer} onClose={() => setShowExplainer(false)} priorities={plan.priorities} allocations={plan.allocations} totalSessions={plan.totalSessions} totalMinutes={plan.totalMinutes} workloadExplanation={plan.weeklyTarget.explanation} /></>}
    />
  );
}

function NativeSelects() {
  const [level, setLevel] = useState<CatchUpLevel>('higher');
  const options = useMemo(() => catchUpOptions(level), [level]);
  const [subjectId, setSubjectId] = useState('biology');
  return (
    <section aria-labelledby="pl-now-selects" style={{ maxWidth: 1536, margin: '0 auto', padding: '40px clamp(20px, 3.5vw, 56px) 64px', borderTop: '1px solid var(--outline-strong)', fontFamily: "'DM Sans', sans-serif" }}>
      <h2 id="pl-now-selects" style={{ margin: '0 0 6px', font: '500 26px/1.2 var(--nsu-serif, Georgia, serif)', color: 'var(--ink-primary)' }}>Native selects around the app</h2>
      <p style={{ ...caption, marginBottom: 28 }}>The Launchpad subject picker and two components that render the browser’s own select, mounted on their own with sample options.</p>
      <div style={{ display: 'grid', gap: 36 }}>
        <div style={{ maxWidth: 340 }}>
          <p style={caption}><span style={code}>components/launchpad/SubjectPicker.tsx</span> and <span style={code}>components/launchpad/LaunchpadSelect.tsx</span>, as the Catch-Up Lane uses them</p>
          <SubjectPicker value={subjectId} options={options} onChange={setSubjectId} />
          <LaunchpadSelect className="w-full mt-3" aria-label="Catch-Up level" value={level} onChange={event => setLevel(event.target.value as CatchUpLevel)}>
            {CATCH_UP_LEVELS.map(item => <option key={item.value} value={item.value}>{item.label}</option>)}
          </LaunchpadSelect>
        </div>
        <div>
          <p style={{ ...caption, marginBottom: 0 }}><span style={code}>components/activities/KanbanBoard.tsx</span>, in the Reframing Progress module</p>
          <KobraScope className="nsu-module-reader theme-compat"><KanbanBoard /></KobraScope>
        </div>
      </div>
    </section>
  );
}

// ?kr-after=1 is a builder's check only: it mounts the Kobra rebuild on its own, at the
// After pane's padding, so it can be screenshotted without the rest of the review page.
const LazyAfter = lazy(() => import('../sections/PlannerAfter'));
const showAfter = new URLSearchParams(window.location.search).has('kr-after');

export default function PlannerBefore() {
  if (showAfter) {
    return (
      <KobraScope className="kr-page">
        <div style={{ maxWidth: 720, padding: window.innerWidth < 768 ? 20 : 28 }}><Suspense fallback={null}><LazyAfter /></Suspense></div>
      </KobraScope>
    );
  }
  return (
    <>
      <p style={{ ...caption, maxWidth: 1536, margin: '0 auto', padding: '14px clamp(20px, 3.5vw, 56px) 0' }}>Sample week for a demo Leaving Cert student. No account is connected.</p>
      <Planner />
      <NativeSelects />
    </>
  );
}
