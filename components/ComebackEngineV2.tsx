/**
 * Comeback Engine v2
 *
 * A short recovery intervention, not a competing timetable. It diagnoses from
 * existing progress signals, builds a seven-day plan and routes every action
 * into the app's established execution tools.
 */
import React, { useEffect, useMemo, useState } from 'react';
import { doc, getDoc, setDoc } from 'firebase/firestore';
import {
  ArrowRight, CalendarDays, Check, CheckCircle2, Clock3,
  ListChecks, RefreshCcw, Sparkles,
} from 'lucide-react';
import { db } from '../firebase';
import { useAuth } from '../contexts/AuthContext';
import { useInnovationData } from '../contexts/InnovationDataContext';
import type { StudentSubjectProfile } from './subjectData';
import { AnimatePresence, MotionDiv } from './Motion';
import PrimaryActionButton from './ui/PrimaryActionButton';
import { LoadingState } from './ui/SystemState';
import { useToast } from './Toast';
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

type Stage = 'setup' | 'diagnosis' | 'plan';

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

const signalTone = {
  attention: { ink: '#A43F08' },
  steady: { ink: '#5F574F' },
  positive: { ink: '#1F5F3E' },
};

const shell = 'rounded-[24px] border-2 border-[#1A1A1A] bg-white dark:bg-[#202020] dark:border-[#E7E2DC] shadow-[5px_5px_0_0_#1A1A1A] dark:shadow-[5px_5px_0_0_#E7E2DC]';

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
  const [isLoading, setIsLoading] = useState(!sessionPlan);
  const [stage, setStage] = useState<Stage>(sessionPlan ? 'plan' : 'setup');
  const [reason, setReason] = useState<RecoveryReason>(sessionPlan?.reason ?? 'unsure');
  const [capacity, setCapacity] = useState<RecoveryCapacity>(sessionPlan?.capacity ?? 5);
  const [plan, setPlan] = useState<RecoveryPlan | null>(sessionPlan);
  const [legacyAnchor, setLegacyAnchor] = useState<string | undefined>();
  const [loadedCompletions, setLoadedCompletions] = useState<Record<string, string[]>>({});

  const completions = suppliedCompletions ?? loadedCompletions;
  const curriculumLevel = user?.curriculumLevel ?? profile.curriculumLevel ?? 'senior';

  useEffect(() => {
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
  }, [uid, suppliedCompletions]);

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

  const savePlan = async (next: RecoveryPlan) => {
    setPlan(next);
    writeSessionPlan(uid, next);
    try {
      await setDoc(doc(db, 'progress', uid), { comebackRecoveryPlan: next }, { merge: true });
    } catch (error) {
      console.error('Failed to save recovery plan:', error);
      showToast('Your plan could not be saved. Check your connection.', 'error');
    }
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

  return (
    <div className="mx-auto w-full max-w-5xl px-4 pb-14 text-[#1A1A1A] dark:text-[#F6F2EC]">
      <div className="mb-8 grid gap-5 md:grid-cols-[1fr_auto] md:items-end">
        <div>
          <p className="mb-2 text-[11px] font-bold uppercase tracking-[0.22em] text-[#A39A91]">Comeback · seven-day recovery</p>
          <h1 className="font-serif text-4xl font-semibold tracking-[-0.025em] md:text-5xl">Comeback Engine</h1>
          <p className="mt-3 max-w-2xl text-[15px] leading-7 text-[#6F6861] dark:text-[#C9C2BA]">
            A smaller, evidence-led route back into study. It uses your real timetable rhythm, subject priorities and topic confidence—then sends you into the tools you already use.
          </p>
        </div>
        {stage === 'plan' && (
          <button type="button" onClick={resetPlan} className="inline-flex items-center gap-2 text-sm font-semibold text-[#6F6861] dark:text-[#D6CFC7]">
            <RefreshCcw size={16} /> Rebuild plan
          </button>
        )}
      </div>

      <AnimatePresence mode="wait">
        {stage === 'setup' && (
          <MotionDiv key="setup" initial={{ opacity: 0, y: 12 }} animate={{ opacity: 1, y: 0 }} exit={{ opacity: 0, y: -8 }} transition={{ duration: 0.28, ease: [0.22, 1, 0.36, 1] }} className="grid gap-6 lg:grid-cols-2">
            <section className={`${shell} p-6 md:p-8`}>
              <div className="mb-7 flex items-center gap-3">
                <span className="font-mono text-[11px] font-bold text-[#F26B1F]">01</span>
                <span className="h-px w-10 bg-[#F26B1F]" />
                <p className="text-[10px] font-bold uppercase tracking-[0.18em] text-[#A39A91]">First, what changed?</p>
              </div>
              <h2 className="mt-2 font-serif text-2xl font-semibold">No judgement. Just a better starting point.</h2>
              <div className="mt-5 space-y-2.5">
                {REASONS.map(option => {
                  const selected = reason === option.id;
                  return (
                    <button key={option.id} type="button" onClick={() => setReason(option.id)} className={`w-full rounded-xl border-2 p-4 text-left transition-transform duration-200 ${selected ? 'border-[#1A1A1A] bg-[#FFF4EC] -translate-y-0.5' : 'border-[#DED8D1] bg-transparent hover:border-[#8D837A]'}`}>
                      <span className="block text-sm font-bold">{option.title}</span>
                      <span className="mt-1 block text-xs leading-5 text-[#766E67] dark:text-[#BBB3AB]">{option.detail}</span>
                    </button>
                  );
                })}
              </div>
            </section>

            <section className={`${shell} p-6 md:p-8`}>
              <div className="mb-7 flex items-center gap-3">
                <span className="font-mono text-[11px] font-bold text-[#F26B1F]">02</span>
                <span className="h-px w-10 bg-[#F26B1F]" />
                <p className="text-[10px] font-bold uppercase tracking-[0.18em] text-[#A39A91]">Choose an honest week</p>
              </div>
              <h2 className="mt-2 font-serif text-2xl font-semibold">What can you genuinely manage?</h2>
              <p className="mt-2 text-sm leading-6 text-[#766E67] dark:text-[#BBB3AB]">This is a recovery week, not punishment. We cap the plan and respect your existing rest days.</p>
              <div className="mt-6 grid gap-3">
                {CAPACITIES.map(option => {
                  const selected = capacity === option.value;
                  return (
                    <button key={option.value} type="button" onClick={() => setCapacity(option.value)} className={`flex items-center justify-between rounded-xl border-2 px-4 py-4 text-left transition-transform duration-200 ${selected ? 'border-[#1A1A1A] bg-[#E8F2EC] -translate-y-0.5' : 'border-[#DED8D1] hover:border-[#8D837A]'}`}>
                      <span><strong className="block text-sm">{option.title}</strong><span className="mt-1 block text-xs text-[#766E67] dark:text-[#BBB3AB]">{option.detail}</span></span>
                      <span className={`flex h-7 w-7 items-center justify-center rounded-full border-2 ${selected ? 'border-[#1F5F3E] bg-[#1F5F3E] text-white' : 'border-[#CFC8C0]'}`}>{selected && <Check size={15} strokeWidth={3} />}</span>
                    </button>
                  );
                })}
              </div>
              {legacyAnchor && <p className="mt-5 rounded-xl bg-[#F3F0EC] px-4 py-3 text-xs leading-5 text-[#5F574F]">Your previous goal is preserved: <strong>{legacyAnchor}</strong></p>}
              <PrimaryActionButton label="Read my recovery signals" icon={ArrowRight} onClick={() => setStage('diagnosis')} className="mt-7 w-full" />
            </section>
          </MotionDiv>
        )}

        {stage === 'diagnosis' && (
          <MotionDiv key="diagnosis" initial={{ opacity: 0, y: 14 }} animate={{ opacity: 1, y: 0 }} exit={{ opacity: 0, y: -8 }} transition={{ duration: 0.3, ease: [0.22, 1, 0.36, 1] }} className={`${shell} overflow-hidden`}>
            <div className="border-b border-[#DED8D1] p-6 md:p-8">
              <p className="text-[10px] font-bold uppercase tracking-[0.18em] text-[#A39A91]">Your diagnosis</p>
              <h2 className="mt-2 font-serif text-3xl font-semibold">Here is what the app can actually see.</h2>
              <p className="mt-2 max-w-2xl text-sm leading-6 text-[#766E67] dark:text-[#BBB3AB]">No invented productivity score. These are the signals behind your plan, and you can rebuild it whenever your week changes.</p>
            </div>
            <div className="grid gap-px bg-[#DED8D1] md:grid-cols-3">
              {draftPlan.signals.map((signal, index) => {
                const tone = signalTone[signal.tone];
                return (
                  <div key={signal.id} className="min-h-40 bg-white p-6 dark:bg-[#202020]">
                    <div className="mb-5 flex items-center gap-3">
                      <span className="font-mono text-[11px] font-bold text-[#F26B1F]">{String(index + 1).padStart(2, '0')}</span>
                      <span className="h-px w-8 bg-[#F26B1F]" />
                    </div>
                    <h3 className="text-sm font-bold" style={{ color: tone.ink }}>{signal.label}</h3>
                    <p className="mt-2 text-sm leading-6 text-[#6F6861] dark:text-[#C9C2BA]">{signal.detail}</p>
                  </div>
                );
              })}
            </div>
            <div className="grid gap-5 p-6 md:grid-cols-[1fr_auto] md:items-center md:p-8">
              <div>
                <p className="text-[10px] font-bold uppercase tracking-[0.18em] text-[#A39A91]">Recovery focus</p>
                <p className="mt-2 font-serif text-xl font-semibold">{draftPlan.priorities.join(' and ') || 'Your current subjects'}</p>
                <p className="mt-1 text-sm text-[#766E67] dark:text-[#BBB3AB]">Only two priorities at most. Everything else stays in maintenance mode for seven days.</p>
              </div>
              <div className="flex flex-wrap gap-3">
                <button type="button" onClick={() => setStage('setup')} className="min-h-12 rounded-xl border-2 border-[#1A1A1A] px-5 text-sm font-bold dark:border-[#E7E2DC]">Adjust</button>
                <PrimaryActionButton label="Build my seven-day plan" icon={Sparkles} onClick={createPlan} />
              </div>
            </div>
          </MotionDiv>
        )}

        {stage === 'plan' && (
          <MotionDiv key="plan" initial={{ opacity: 0, y: 14 }} animate={{ opacity: 1, y: 0 }} transition={{ duration: 0.32, ease: [0.22, 1, 0.36, 1] }} className="grid gap-6 lg:grid-cols-[300px_1fr]">
            <aside className="h-fit overflow-hidden rounded-[24px] border-2 border-[#F26B1F] bg-white shadow-[5px_5px_0_0_#F26B1F] dark:bg-[#202020]">
              <div className="p-6">
                <div className="mb-6 flex items-center gap-3">
                  <span className="font-mono text-[11px] font-bold text-[#F26B1F]">07</span>
                  <span className="h-px w-10 bg-[#F26B1F]" />
                  <p className="text-[10px] font-bold uppercase tracking-[0.18em] text-[#A39A91]">Day plan</p>
                </div>
                <p className="text-[10px] font-bold uppercase tracking-[0.18em] text-[#A39A91]">Seven-day target</p>
                <p className="mt-1 font-serif text-4xl font-semibold">{completed}<span className="text-xl text-[#A39A91]">/{activePlan.actions.length}</span></p>
                <div className="mt-4 h-2 overflow-hidden rounded-full bg-[#E7E1DA]"><div className="h-full rounded-full bg-[#F26B1F] transition-[width] duration-500" style={{ width: `${completionPercent}%` }} /></div>
              </div>
              <div className="space-y-5 border-t border-[#E7E1DA] p-6">
                <div><p className="text-[10px] font-bold uppercase tracking-[0.16em] text-[#A39A91]">Focus</p><p className="mt-1 text-sm font-bold">{activePlan.priorities.join(' · ')}</p></div>
                <div><p className="text-[10px] font-bold uppercase tracking-[0.16em] text-[#A39A91]">Capacity</p><p className="mt-1 text-sm font-bold">{activePlan.capacity} blocks, maximum</p></div>
                <p className="border-l-2 border-[#F26B1F] pl-3 text-xs leading-5 text-[#6F6861] dark:text-[#C9C2BA]">Finishing every block is useful. Missing one does not erase the others—the plan can be rebuilt without penalty.</p>
              </div>
            </aside>

            <section className="space-y-3">
              {activePlan.actions.map((action, index) => (
                <MotionDiv key={action.id} initial={{ opacity: 0, x: 12 }} animate={{ opacity: 1, x: 0 }} transition={{ delay: index * 0.045, duration: 0.25 }} className={`${shell} p-5 md:p-6 ${action.done ? 'opacity-65' : ''}`}>
                  <div className="grid gap-4 md:grid-cols-[88px_1fr_auto] md:items-center">
                    <div>
                      <p className="font-mono text-[11px] font-bold uppercase tracking-[0.12em] text-[#A39A91]">{action.dayLabel}</p>
                      <p className="mt-1 flex items-center gap-1.5 text-xs text-[#766E67] dark:text-[#BBB3AB]"><Clock3 size={13} /> {action.durationMinutes} min</p>
                    </div>
                    <div>
                      <div className="flex flex-wrap items-center gap-2"><h3 className={`font-serif text-xl font-semibold ${action.done ? 'line-through' : ''}`}>{action.subject}</h3><span className="rounded-md bg-[#F3F0EC] px-2 py-1 text-[9px] font-bold uppercase tracking-[0.1em] text-[#5F574F]">{action.sessionType.replace('-', ' ')}</span></div>
                      {action.topic && <p className="mt-1 text-sm font-semibold text-[#A43F08]">{action.topic}</p>}
                      <p className="mt-1.5 text-xs leading-5 text-[#766E67] dark:text-[#BBB3AB]">{action.reason}</p>
                    </div>
                    <div className="flex items-center gap-2 md:justify-end">
                      <button type="button" onClick={() => toggleAction(action.id)} aria-label={action.done ? 'Mark incomplete' : 'Mark complete'} className={`flex h-11 w-11 items-center justify-center rounded-xl border-2 ${action.done ? 'border-[#1F5F3E] bg-[#1F5F3E] text-white' : 'border-[#CFC8C0]'}`}><Check size={18} strokeWidth={3} /></button>
                      {!action.done && <button type="button" onClick={() => openPlanDestination(action.destination)} className="inline-flex min-h-11 items-center gap-2 rounded-xl border-2 border-[#1A1A1A] px-4 text-xs font-bold dark:border-[#E7E2DC]">{action.destination === 'mark-bank' ? <ListChecks size={16} /> : <CalendarDays size={16} />}{action.destination === 'mark-bank' ? 'Open Mark Bank' : 'Open timetable'}</button>}
                    </div>
                  </div>
                </MotionDiv>
              ))}
              {completionPercent === 100 && (
                <div className={`${shell} bg-[#E8F2EC] p-6 text-center dark:bg-[#193226]`}>
                  <CheckCircle2 className="mx-auto text-[#1F5F3E] dark:text-[#76C499]" size={34} />
                  <h3 className="mt-3 font-serif text-2xl font-semibold">The comeback week is complete.</h3>
                  <p className="mx-auto mt-2 max-w-lg text-sm leading-6 text-[#456453] dark:text-[#B9D8C5]">You rebuilt momentum without trying to repair everything at once. Return to your normal timetable, or rebuild this plan if another small recovery week would help.</p>
                </div>
              )}
            </section>
          </MotionDiv>
        )}
      </AnimatePresence>
    </div>
  );
};

export default ComebackEngineV2;
