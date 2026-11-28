/**
 * Comeback Engine v2
 *
 * A short recovery intervention, not a competing timetable. It diagnoses from
 * existing progress signals, builds a seven-day plan and routes every action
 * into the app's established execution tools.
 */
import React, { useEffect, useMemo, useState } from 'react';
import { doc, getDoc, setDoc } from 'firebase/firestore';
import { Check, CheckCircle2 } from 'lucide-react';
import { db } from '../firebase';
import { saveInBackground } from '../utils/firestoreWrite';
import { useAuth } from '../contexts/AuthContext';
import { useInnovationData } from '../contexts/InnovationDataContext';
import { useOptionalProgress } from '../contexts/ProgressContext';
import { DEMO_STUDENT_UID } from '../data/devStudent';
import type { StudentSubjectProfile } from './subjectData';
import { AnimatePresence, MotionDiv } from './Motion';
import { PinnedFooter } from './ui/Bars';
import { Button, IconButton, TextButton } from './ui/Button';
import { ChoiceTile, useRovingRadios } from './ui/Choice';
import { PaperSheet } from './ui/List';
import { Confirm } from './ui/Sheet';
import { useFrameTask } from './ui/Frame';
import SubjectAvatar from './SubjectAvatar';
import { useBackStep } from '../contexts/NavigationContext';
import { LoadingState } from './ui/SystemState';
import { useToast } from './Toast';
import './comeback/comeback-7.css';
import {
  buildRecoveryPlan,
  type RecoveryCapacity,
  type RecoveryPlan,
  type RecoveryReason,
} from './comeback/recoveryPlan';

interface ComebackEngineProps {
  uid: string;
  profile: StudentSubjectProfile;
  timetableCompletions?: Record<string, string[]>;
  onOpenTool?: (toolId: string) => void;
}

type Stage = 'capacity' | 'setup' | 'diagnosis' | 'plan';

const REASONS: { id: RecoveryReason; title: string; detail: string }[] = [
  { id: 'missed-time', title: 'I missed some time', detail: 'Absence, illness or life got in the way.' },
  { id: 'overloaded', title: 'My plan became too much', detail: 'The workload stopped feeling realistic.' },
  { id: 'unsure', title: 'I do not know where to start', detail: 'Too many subjects are competing for attention.' },
  { id: 'motivation', title: 'I lost momentum', detail: 'Starting again is the difficult part.' },
  { id: 'other', title: 'Something else', detail: 'Build a calm plan from the evidence we have.' },
];

const CAPACITIES: { value: RecoveryCapacity; title: string; detail: string }[] = [
  { value: 3, title: 'Gentle reset', detail: '3 focused blocks' },
  { value: 5, title: 'Steady week', detail: '5 focused blocks' },
  { value: 7, title: 'Strong return', detail: '7 focused blocks' },
];

const recoveryPlanSessionKey = (uid: string) => `nextstepuni:comeback-plan:${uid}`;

const readSessionPlan = (uid: string): RecoveryPlan | null => {
  if (typeof window === 'undefined') return null;
  try {
    const value = window.sessionStorage.getItem(recoveryPlanSessionKey(uid));
    if (!value) return null;
    const parsed = JSON.parse(value) as RecoveryPlan;
    return parsed?.version === 2 ? parsed : null;
  } catch {
    return null;
  }
};

const writeSessionPlan = (uid: string, next: RecoveryPlan | null) => {
  if (typeof window === 'undefined') return;
  if (next) window.sessionStorage.setItem(recoveryPlanSessionKey(uid), JSON.stringify(next));
  else window.sessionStorage.removeItem(recoveryPlanSessionKey(uid));
};

const ComebackEngineV2: React.FC<ComebackEngineProps> = ({
  uid,
  profile,
  timetableCompletions: suppliedCompletions,
  onOpenTool,
}) => {
  const sessionPlan = useMemo(() => readSessionPlan(uid), [uid]);
  const { user } = useAuth();
  const { showToast } = useToast();
  const { topicMastery, subjectPriorities } = useInnovationData();
  const progress = useOptionalProgress();
  const isDemo = uid === DEMO_STUDENT_UID;
  const [isLoading, setIsLoading] = useState(!sessionPlan);
  const [stage, setStage] = useState<Stage>(sessionPlan ? 'plan' : 'setup');
  const [reason, setReason] = useState<RecoveryReason>(sessionPlan?.reason ?? 'unsure');
  const [capacity, setCapacity] = useState<RecoveryCapacity>(sessionPlan?.capacity ?? 5);
  const [plan, setPlan] = useState<RecoveryPlan | null>(sessionPlan);
  const [legacyAnchor, setLegacyAnchor] = useState<string | undefined>();
  const [loadedCompletions, setLoadedCompletions] = useState<Record<string, string[]>>({});
  const [confirmRebuild, setConfirmRebuild] = useState(false);
  // The steps are a task on a phone: Continue is pinned and the tab bar steps aside; the bar's
  // one Back steps back a step (navigation.md: one leave control, no in-page back link).
  useFrameTask(stage !== 'plan' && !isLoading);
  useBackStep(stage === 'capacity' || stage === 'diagnosis', () => setStage(current => current === 'diagnosis' ? 'capacity' : 'setup'));

  const completions = suppliedCompletions ?? loadedCompletions;
  const curriculumLevel = user?.curriculumLevel ?? profile.curriculumLevel ?? 'senior';

  useEffect(() => {
    if (isDemo) {
      const data = progress?.rawProgressDoc;
      const saved = data?.comebackRecoveryPlan as RecoveryPlan | undefined;
      if (saved?.version === 2) {
        writeSessionPlan(uid, saved);
        setPlan(saved);
        setReason(saved.reason);
        setCapacity(saved.capacity);
        setStage('plan');
      } else if ((data?.comebackEngine as { anchor?: string } | undefined)?.anchor) {
        setLegacyAnchor((data?.comebackEngine as { anchor: string }).anchor);
      }
      if (!suppliedCompletions && data?.timetableCompletions) {
        setLoadedCompletions(data.timetableCompletions);
      }
      setIsLoading(false);
      return;
    }
    let cancelled = false;
    getDoc(doc(db, 'progress', uid)).then(snapshot => {
      if (cancelled) return;
      const data = snapshot.data();
      const saved = data?.comebackRecoveryPlan as RecoveryPlan | undefined;
      if (saved?.version === 2) {
        writeSessionPlan(uid, saved);
        setPlan(saved);
        setReason(saved.reason);
        setCapacity(saved.capacity);
        setStage('plan');
      } else if (data?.comebackEngine?.anchor) {
        // The old plan remains untouched. Its meaningful goal is carried into
        // the new plan when the student chooses to create one.
        setLegacyAnchor(data.comebackEngine.anchor);
      }
      if (!suppliedCompletions && data?.timetableCompletions) {
        setLoadedCompletions(data.timetableCompletions);
      }
      setIsLoading(false);
    }).catch(error => {
      console.error('Failed to load Comeback Engine:', error);
      if (!cancelled) setIsLoading(false);
    });
    return () => { cancelled = true; };
  }, [uid, suppliedCompletions, isDemo, progress?.rawProgressDoc]);

  const draftPlan = useMemo(() => buildRecoveryPlan({
    profile,
    priorities: subjectPriorities,
    masteryEntries: Object.values(topicMastery.canonicalMastery.topics),
    timetableCompletions: completions,
    reason,
    capacity,
    curriculumLevel,
    legacyAnchor,
  }), [profile, subjectPriorities, topicMastery.canonicalMastery.topics, completions, reason, capacity, curriculumLevel, legacyAnchor]);

  const savePlan = (next: RecoveryPlan) => {
    setPlan(next);
    writeSessionPlan(uid, next);
    if (isDemo) {
      progress?.updateDemoProgress(current => ({ ...current, comebackRecoveryPlan: next }));
      return;
    }
    saveInBackground(
      setDoc(doc(db, 'progress', uid), { comebackRecoveryPlan: next }, { merge: true }),
      'ComebackEngineV2.savePlan',
      () => {
      showToast('Your plan could not be saved. Check your connection.', 'error');
      },
    );
  };

  const createPlan = () => {
    void savePlan(draftPlan);
    setStage('plan');
  };

  const toggleAction = (actionId: string) => {
    if (!plan) return;
    const next = {
      ...plan,
      actions: plan.actions.map(action => action.id === actionId ? { ...action, done: !action.done } : action),
    };
    void savePlan(next);
  };

  const resetPlan = () => {
    setPlan(null);
    writeSessionPlan(uid, null);
    setStage('setup');
    if (isDemo) {
      progress?.updateDemoProgress(current => ({ ...current, comebackRecoveryPlan: null }));
      return;
    }
    setDoc(doc(db, 'progress', uid), { comebackRecoveryPlan: null }, { merge: true })
      .catch(error => {
        console.error('Failed to clear recovery plan:', error);
        showToast('The old plan could not be cleared. Check your connection.', 'error');
      });
  };

  const openPlanDestination = (destination: string) => {
    // Opening another tool unmounts this component. Keep an immediate local
    // return anchor as well as the persisted Firebase copy so browser Back
    // always restores the built plan, even on a slow or interrupted network.
    writeSessionPlan(uid, activePlan);
    onOpenTool?.(destination);
  };

  if (isLoading) return <LoadingState label="Reading your recent study pattern" />;

  const activePlan = plan ?? draftPlan;
  const completed = activePlan.actions.filter(action => action.done).length;
  const completionPercent = activePlan.actions.length ? Math.round(completed / activePlan.actions.length * 100) : 0;
  const firstDay = activePlan.actions[0]?.dayLabel;
  const lastDay = activePlan.actions[activePlan.actions.length - 1]?.dayLabel;
  const stepNumber = stage === 'setup' ? 1 : stage === 'capacity' ? 2 : 3;
  const foot = (children: React.ReactNode) => (
    <div className="cb7-foot-wrap frame-float frame-float-bottom">
      <PinnedFooter className="cb7-foot" note={`Step ${stepNumber} of 4`}>{children}</PinnedFooter>
    </div>
  );

  return (
    <div className="cb7" data-stage={stage}>
      <AnimatePresence mode="wait">
        {stage === 'setup' && (
          <MotionDiv key="setup" initial={{ opacity: 0 }} animate={{ opacity: 1 }} exit={{ opacity: 0 }} transition={{ duration: 0.2, ease: [0.22, 1, 0.36, 1] }} className="cb7-step cb7-step--aside">
            <section className="cb7-main">
              <div className="cb7-top">
                <Motif n="01" label="First, what changed?" />
                <h2 className="t-title cb7-title">No judgement. Just a better starting point.</h2>
              </div>
              <ChoiceRow label="First, what changed?" options={REASONS.map(option => ({ value: option.id, label: option.title, meta: option.detail }))} value={reason} onChange={value => setReason(value as RecoveryReason)} />
              {foot(<Button kind="main" size="lg" block arrow="forward" onClick={() => setStage('capacity')}>Continue</Button>)}
            </section>
            <aside className="cb7-aside"><h3 className="t-heading">One step at a time.</h3><p className="t-sub">First, what changed. Then choose a week that feels manageable. You can review the plan before saving it.</p></aside>
          </MotionDiv>
        )}
        {stage === 'capacity' && (
          <MotionDiv key="capacity" initial={{ opacity: 0 }} animate={{ opacity: 1 }} exit={{ opacity: 0 }} transition={{ duration: 0.2, ease: [0.22, 1, 0.36, 1] }} className="cb7-step">
            <section className="cb7-main">
              <div className="cb7-top">
                <Motif n="02" label="Choose an honest week" />
                <h2 className="t-title cb7-title">What can you genuinely manage?</h2>
                <p className="t-sub">This is a recovery week, not punishment. We cap the plan and respect your existing rest days.</p>
              </div>
              <ChoiceRow label="Choose an honest week" options={CAPACITIES.map(option => ({ value: String(option.value), label: option.title, meta: option.detail }))} value={String(capacity)} onChange={value => setCapacity(Number(value) as RecoveryCapacity)} />
              {legacyAnchor && <p className="t-sub cb7-anchor">Your previous goal is preserved: <span className="cb7-ink">{legacyAnchor}</span></p>}
              {foot(<Button kind="main" size="lg" block arrow="forward" onClick={() => setStage('diagnosis')}>Read my recovery signals</Button>)}
            </section>
          </MotionDiv>
        )}

        {stage === 'diagnosis' && (
          <MotionDiv key="diagnosis" initial={{ opacity: 0 }} animate={{ opacity: 1 }} exit={{ opacity: 0 }} transition={{ duration: 0.2, ease: [0.22, 1, 0.36, 1] }} className="cb7-step">
            <section className="cb7-main">
              <div className="cb7-top">
                <Motif n="03" label="Your diagnosis" />
                <h2 className="t-title cb7-title">Here is what the app can actually see.</h2>
                <p className="t-sub">No invented productivity score. These are the signals behind your plan, and you can rebuild it whenever your week changes.</p>
              </div>
              <ol className="cb7-signals">
                {draftPlan.signals.map((signal, index) => (
                  <li key={signal.id}>
                    <span className="ui-readout cb7-signal-n">{String(index + 1).padStart(2, '0')}</span>
                    <span className="cb7-signal-copy"><span className="t-row">{signal.label}</span><span className="t-sub">{signal.detail}</span></span>
                  </li>
                ))}
              </ol>
              <div className="cb7-focus">
                <p className="t-label">Recovery focus</p>
                <p className="t-heading">{draftPlan.priorities.join(' and ') || 'Your current subjects'}</p>
                <p className="t-sub">Only two priorities at most. Everything else stays in maintenance mode for seven days.</p>
              </div>
              {foot(<><Button kind="main" size="lg" block arrow="forward" onClick={createPlan}>Build my seven-day plan</Button><TextButton tone="quiet" className="cb7-adjust" onClick={() => setStage('setup')}>Adjust</TextButton></>)}
            </section>
          </MotionDiv>
        )}

        {stage === 'plan' && (
          <MotionDiv key="plan" initial={{ opacity: 0 }} animate={{ opacity: 1 }} transition={{ duration: 0.2, ease: [0.22, 1, 0.36, 1] }} className="cb7-step cb7-step--plan">
            <div className="cb7-top">
              <Motif n="04" label="Your seven days" />
              <h2 className="t-title cb7-title">A smaller plan. A little momentum.</h2>
            </div>
            <div className="cb7-plan">
              <PaperSheet className="cb7-target" label="Seven-day target">
                <p className="t-label">Seven-day target</p>
                <p className="cb7-count"><span className="cb7-num">{completed}</span><span className="cb7-of"> / {activePlan.actions.length}</span><span className="cb7-done"> blocks done</span></p>
                <span className="cb7-bar" role="progressbar" aria-label="Blocks done this week" aria-valuemin={0} aria-valuemax={100} aria-valuenow={completionPercent}><i style={{ width: `${completionPercent}%` }} /></span>
                <div className="cb7-facts">
                  <div><p className="t-label">Focus</p><p className="t-row">{activePlan.priorities.join(' and ')}</p></div>
                  <div><p className="t-label">Capacity</p><p className="t-row">{activePlan.capacity} blocks at most</p></div>
                </div>
                <p className="t-meta">Finishing every block is useful. Missing one does not erase the others. The plan can be rebuilt without penalty.</p>
              </PaperSheet>

              <section className="cb7-week" aria-label="This week">
                <div className="cb7-week-head"><h3 className="t-heading">This week</h3>{firstDay && <span className="ui-readout">{firstDay === lastDay ? firstDay : `${firstDay} to ${lastDay}`}</span>}</div>
                <ul className="cb7-blocks">
                  {activePlan.actions.map(action => (
                    <li key={action.id} className="cb7-block" data-done={action.done || undefined}>
                      <span className="t-label cb7-block-when">{action.dayLabel} · {sessionName(action.sessionType)} · {action.durationMinutes} min</span>
                      <span className="cb7-block-art" aria-hidden="true"><SubjectAvatar subject={action.subject} bare /></span>
                      <span className="cb7-block-copy">
                        <span className="t-row cb7-block-subject">{action.subject}</span>
                        {action.topic && <span className="t-sub">{action.topic}</span>}
                        <span className="t-meta">{action.reason}</span>
                        {!action.done && <TextButton arrow="opens" className="cb7-block-go" onClick={() => openPlanDestination(action.destination)}>{action.destination === 'mark-bank' ? 'Open Mark Bank' : 'Open your planner'}</TextButton>}
                      </span>
                      <IconButton className="cb7-tick" aria-pressed={action.done} label={action.done ? 'Mark incomplete' : 'Mark complete'} onClick={() => toggleAction(action.id)} icon={<Check className="ui-icon" width={20} height={20} strokeWidth={2} aria-hidden="true" focusable="false" />} />
                    </li>
                  ))}
                </ul>
                {completionPercent === 100 && (
                  <div className="cb7-complete">
                    <CheckCircle2 className="cb7-complete-mark" width={28} height={28} strokeWidth={1.75} aria-hidden="true" />
                    <h3 className="t-heading">The comeback week is complete.</h3>
                    <p className="t-sub">You rebuilt momentum without trying to repair everything at once. Return to your normal timetable, or rebuild this plan if another small recovery week would help.</p>
                  </div>
                )}
                <TextButton tone="quiet" className="cb7-rebuild" onClick={() => setConfirmRebuild(true)}>Rebuild plan</TextButton>
              </section>
            </div>
            <Confirm open={confirmRebuild} sentence="Rebuild plan?" keepLabel="Keep this plan" onKeep={() => setConfirmRebuild(false)} dangerLabel="Rebuild plan" onDanger={() => { setConfirmRebuild(false); resetPlan(); }} />
          </MotionDiv>
        )}
      </AnimatePresence>
    </div>
  );
};

/** The numbered motif kept from today's tool ("01 —— First, what changed?"), board c-tools2-comeback. */
const Motif: React.FC<{ n: string; label: string }> = ({ n, label }) => (
  <div className="cb7-motif"><b className="ui-readout">{n}</b><i aria-hidden="true" /><span className="t-label">{label}</span></div>
);

/** One answer from a short list, as the shared choice tiles: an ink outline and a drawn tick. */
function ChoiceRow<V extends string>({ label, options, value, onChange }: { label: string; options: { value: V; label: string; meta: string }[]; value: V; onChange: (value: V) => void }) {
  const current = options.findIndex(option => option.value === value);
  const roving = useRovingRadios(options.length, current, index => onChange(options[index].value));
  return (
    <div className="cb7-choices" role="radiogroup" aria-label={label}>
      {options.map((option, index) => (
        <ChoiceTile key={option.value} ref={element => { roving.refs.current[index] = element; }} chosen={option.value === value}
          label={option.label} meta={option.meta} tabIndex={roving.tabIndexOf(index)}
          onKeyDown={event => roving.onKeyDown(event, index)} onClick={() => onChange(option.value)} />
      ))}
    </div>
  );
}

const sessionName = (type: RecoveryPlan['actions'][number]['sessionType']) => {
  const words = type.replace('-', ' ');
  return words.charAt(0).toUpperCase() + words.slice(1);
};

export default ComebackEngineV2;
