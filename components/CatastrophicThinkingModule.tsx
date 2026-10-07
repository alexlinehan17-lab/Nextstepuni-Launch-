import { moduleFill,moduleText } from './learning/brandTokens';
/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
*/

import { AnimatePresence,motion,Reorder } from 'framer-motion';
import {
BookOpen,
BrainCircuit,
Flag,
Layers,
MessageSquare,
Shield,
Wrench,
Zap
} from 'lucide-react';
import React,{ useState } from 'react';
import { CATASTROPHIC_THINKING_REFERENCE_LIST } from '../data/references/catastrophicThinking';
import { useEssentialsMode } from '../hooks/useEssentialsMode';
import { usePrivateDeviceDraft } from '../hooks/usePrivateDeviceDraft';
import { slateTheme } from '../moduleThemes';
import { type ModuleProgress } from '../types';
import { PrivateDraftControls } from './learning/PrivateDraftControls';
import { ModuleLayout } from './ModuleLayout';
import { Cite } from './ModuleReferences';
import { ConceptCardGrid,Highlight,MicroCommitment,ReadingSection,SupportSignpost } from './ModuleShared';
import { MotionDiv } from './Motion';

const theme = slateTheme;

// --- INTERACTIVE COMPONENTS ---

const ThoughtRecord = () => {
    const draft = usePrivateDeviceDraft('thought-record', { step: 0, record: { situation: '', emotion: '', intensity: 90, nat: '', evidenceFor: '', evidenceAgainst: '', alternative: '', reRate: 50 } });
    const { step, record } = draft.value;
    const setStep = (value: React.SetStateAction<number>) => draft.update(previous => ({ ...previous, step: typeof value === 'function' ? value(previous.step) : value }));
    const update = (field: string, value: string | number) => draft.update(previous => ({ ...previous, record: { ...previous.record, [field]: value } }));

    const steps = ['Situation', 'Emotion', 'Negative Thought', 'Evidence For', 'Evidence Against', 'Alternative', 'Re-Rate'];

    return (
        <div className="my-10 rounded-2xl p-8 md:p-12" style={{ backgroundColor: "var(--module-surface)", borderRadius: 18 }}>
             <h4 className="font-serif text-2xl font-semibold text-[var(--module-ink)] dark:text-[var(--module-ink)] text-center">The Thought Record</h4>
             <PrivateDraftControls title="My thought record" retain={draft.retain} setRetain={draft.setRetain} onClear={draft.clear} error={draft.error} text={Object.entries(record).map(([key, value]) => `${key}: ${value}`).join('\n')} />
             <div className="flex justify-between my-4"><div className="w-full h-1 bg-[var(--module-surface)] dark:bg-[var(--module-surface)] rounded-full"><motion.div className="h-1 bg-[var(--module-surface)] rounded-full" animate={{width: `${(step / (steps.length - 1)) * 100}%`}}/></div></div>
             <AnimatePresence mode="wait">
             <motion.div key={step} initial={{opacity:0, x:20}} animate={{opacity:1, x:0}} exit={{opacity:0, x:-20}} >
                {step === 0 && <div><label className="font-bold">1. Situation:</label><input value={record.situation} onChange={e => update('situation', e.target.value)} placeholder="e.g., Sitting down to study History" className="w-full bg-[var(--module-surface)] dark:bg-[var(--module-surface)] rounded-xl px-5 py-3.5 text-sm font-medium text-[var(--module-ink)] dark:text-[var(--module-ink)] placeholder-zinc-400 outline-none transition-all mt-2" style={{ border: "1.5px solid var(--module-line)" }}/></div>}
                {step === 1 && <div><label className="font-bold">2. Emotion:</label><input value={record.emotion} onChange={e => update('emotion', e.target.value)} placeholder="e.g., Panic" className="w-full bg-[var(--module-surface)] dark:bg-[var(--module-surface)] rounded-xl px-5 py-3.5 text-sm font-medium text-[var(--module-ink)] dark:text-[var(--module-ink)] placeholder-zinc-400 outline-none transition-all mt-2" style={{ border: "1.5px solid var(--module-line)" }}/><label>Intensity: {record.intensity}%</label><input type="range" value={record.intensity} onChange={e => update('intensity', e.target.value)} className="chunky-slider chunky-slider-coral"/></div>}
                {step === 2 && <div><label className="font-bold">3. Negative Automatic Thought (NAT):</label><textarea value={record.nat} onChange={e => update('nat', e.target.value)} placeholder="e.g., I'll never remember all these dates." className="w-full bg-[var(--module-surface)] dark:bg-[var(--module-surface)] rounded-xl px-5 py-3.5 text-sm font-medium text-[var(--module-ink)] dark:text-[var(--module-ink)] placeholder-zinc-400 outline-none transition-all mt-2 h-24" style={{ border: "1.5px solid var(--module-line)" }}/></div>}
                {step === 3 && <div><label className="font-bold">4. Evidence For:</label><textarea value={record.evidenceFor} onChange={e => update('evidenceFor', e.target.value)} placeholder="e.g., I got some dates wrong on last week's test." className="w-full bg-[var(--module-surface)] dark:bg-[var(--module-surface)] rounded-xl px-5 py-3.5 text-sm font-medium text-[var(--module-ink)] dark:text-[var(--module-ink)] placeholder-zinc-400 outline-none transition-all mt-2 h-24" style={{ border: "1.5px solid var(--module-line)" }}/></div>}
                {step === 4 && <div><label className="font-bold">5. Evidence Against:</label><textarea value={record.evidenceAgainst} onChange={e => update('evidenceAgainst', e.target.value)} placeholder="e.g., I passed my last test. I have 3 months to study." className="w-full bg-[var(--module-surface)] dark:bg-[var(--module-surface)] rounded-xl px-5 py-3.5 text-sm font-medium text-[var(--module-ink)] dark:text-[var(--module-ink)] placeholder-zinc-400 outline-none transition-all mt-2 h-24" style={{ border: "1.5px solid var(--module-line)" }}/></div>}
                {step === 5 && <div><label className="font-bold">6. Alternative Thought:</label><textarea value={record.alternative} onChange={e => update('alternative', e.target.value)} placeholder="e.g., History is hard, but if I use flashcards I can pass." className="w-full bg-[var(--module-surface)] dark:bg-[var(--module-surface)] rounded-xl px-5 py-3.5 text-sm font-medium text-[var(--module-ink)] dark:text-[var(--module-ink)] placeholder-zinc-400 outline-none transition-all mt-2 h-24" style={{ border: "1.5px solid var(--module-line)" }}/></div>}
                {step === 6 && <div className="space-y-4"><label className="font-bold">7. Re-Rate Emotion:</label>{record.alternative && <div className="p-3 bg-[var(--module-success-soft)] dark:bg-[var(--module-success)]/15 border border-success/30 dark:border-success/40 rounded-lg"><p className="text-[10px] font-bold uppercase tracking-wider text-[var(--module-success-text)] mb-1">Your Alternative Thought</p><p className="text-sm text-[var(--module-success-text)] dark:text-[var(--module-success-text)]">{record.alternative}</p></div>}<p className="text-sm">Initial Panic: <span className="font-bold text-[var(--module-danger-text)]">{record.intensity}%</span></p><label className="text-sm">New Panic Level: <span className="font-bold">{record.reRate}%</span></label><input type="range" value={record.reRate} onChange={e => update('reRate', e.target.value)} className="chunky-slider chunky-slider-coral"/>{Number(record.reRate) < Number(record.intensity) && <p className="text-xs text-[var(--module-success-text)] dark:text-[var(--module-success-text)] font-medium">You rated this feeling {Number(record.intensity) - Number(record.reRate)} points lower. Notice what helped; there is no required result.</p>}</div>}
             </motion.div>
             </AnimatePresence>
             <div className="flex justify-between mt-4">
                <button onClick={() => setStep(s=>Math.max(0,s-1))} disabled={step===0} className="px-3 py-1 text-xs bg-[var(--module-surface)] rounded-md disabled:opacity-50" data-wide-button="true">Prev</button>
                <button onClick={() => setStep(s=>Math.min(steps.length-1,s+1))} disabled={step===steps.length-1} className="px-3 py-1 text-xs bg-[var(--module-surface)] rounded-md disabled:opacity-50" data-wide-button="true">Next</button>
             </div>
        </div>
    );
};

const GradedExposureHierarchy = () => {
    const [items, setItems] = useState([
        { id: 1, text: "Open Maths book (10 mins)", suds: 20 },
        { id: 2, text: "Read one past question", suds: 50 },
        { id: 3, text: "Attempt one question (timed)", suds: 80 },
    ]);
    return(
        <div className="my-10 rounded-2xl p-8 md:p-12" style={{ backgroundColor: "var(--module-surface)", borderRadius: 18 }}>
             <h4 className="font-serif text-2xl font-semibold text-[var(--module-ink)] dark:text-[var(--module-ink)] text-center">Exposure Hierarchy Builder</h4>
             <Reorder.Group axis="y" values={items} onReorder={setItems} className="space-y-2 mt-6">
                {items.map(item => (
                    <Reorder.Item key={item.id} value={item} className="flex justify-between items-center cursor-grab active:cursor-grabbing" style={{ backgroundColor: "var(--module-surface)", border: "2.5px solid var(--module-line)", borderRadius: 16, padding: '14px 16px', boxShadow: 'none' }} whileDrag={{ scale: 1.03, y: -2, boxShadow: 'none' }}>
                        <span>{item.text}</span>
                        <span className="font-bold text-sm text-[var(--module-danger-text)]">{item.suds} SUDS</span>
                    </Reorder.Item>
                ))}
             </Reorder.Group>
        </div>
    );
};

interface Passenger {
  id: number;
  text: string;
  state: 'shouting' | 'acknowledged';
}

const PassengersOnBus = () => {
    const [passengers, setPassengers] = useState<Passenger[]>([
      { id: 1, text: "You're going to fail.", state: 'shouting' },
      { id: 2, text: "You're not smart enough.", state: 'shouting' },
      { id: 3, text: "Everyone else is doing better.", state: 'shouting' },
    ]);
    const [argued, setArgued] = useState(0);

    const shoutingCount = passengers.filter(p => p.state === 'shouting').length;
    const totalCount = passengers.length;
    const allAcknowledged = shoutingCount === 0 && totalCount > 0;

    const spawnThoughts = [
      "You'll embarrass yourself.",
      "It's too late to catch up.",
      "You should just give up.",
      "What if you blank out completely?",
    ];

    const handleArgue = (id: number) => {
      setArgued(a => a + 1);
      // Arguing makes the thought louder and spawns a new one
      const spawnText = spawnThoughts[argued % spawnThoughts.length];
      setPassengers(prev => [
        ...prev.map(p => p.id === id ? { ...p, text: p.text.toUpperCase() } : p),
        { id: Date.now(), text: spawnText, state: 'shouting' },
      ]);
    };

    const handleAcknowledge = (id: number) => {
      setPassengers(prev =>
        prev.map(p => p.id === id ? { ...p, state: 'acknowledged' } : p)
      );
    };

    const handleReset = () => {
      setPassengers([
        { id: 1, text: "You're going to fail.", state: 'shouting' },
        { id: 2, text: "You're not smart enough.", state: 'shouting' },
        { id: 3, text: "Everyone else is doing better.", state: 'shouting' },
      ]);
      setArgued(0);
    };

    // Speed indicator
    const speed = allAcknowledged ? 'Full Speed' : shoutingCount <= 1 ? 'Cruising' : shoutingCount <= 3 ? 'Slowing' : 'Stalled';
    const speedColor = allAcknowledged ? "text-[var(--module-success-text)]" : shoutingCount <= 1 ? "text-[var(--module-success-text)]" : shoutingCount <= 3 ? "text-[var(--module-ink)]" : "text-[var(--module-danger-text)]";
    const barWidth = allAcknowledged ? 100 : Math.max(5, Math.round(100 - (shoutingCount / Math.max(1, totalCount)) * 100));
    const barColor = allAcknowledged ? "bg-[var(--module-success)]" : shoutingCount <= 1 ? "bg-[var(--module-success)]" : shoutingCount <= 3 ? "bg-[var(--module-surface)]" : "bg-[var(--module-danger)]";

    return (
         <div className="my-10 rounded-2xl p-8 md:p-12" style={{ backgroundColor: "var(--module-surface)", borderRadius: 18 }}>
            <h4 className="font-serif text-2xl font-semibold text-[var(--module-ink)] dark:text-[var(--module-ink)] text-center">Passengers on the Bus</h4>
            <p className="text-center text-sm text-[var(--module-muted)] dark:text-[var(--module-muted)] mb-2">You're driving toward your goal. Negative thoughts are passengers shouting at you.</p>
            <p className="text-center text-xs text-[var(--module-muted)] dark:text-[var(--module-muted)] mb-6">You can't kick them off. But you can choose how to respond.</p>

            {/* Speed indicator */}
            <div className="mb-6 p-4 bg-[var(--module-surface)] dark:bg-[var(--module-surface)] rounded-xl">
              <div className="flex justify-between items-center mb-2">
                <p className="text-xs font-bold text-[var(--module-muted)] dark:text-[var(--module-muted)]">Progress Toward Your Goal</p>
                <p className={`text-xs font-bold ${speedColor}`}>{speed}</p>
              </div>
              <div className="w-full h-2.5 bg-[var(--module-surface)] dark:bg-[var(--module-surface)] rounded-full overflow-hidden">
                <motion.div
                  className={`h-full rounded-full ${barColor}`}
                  animate={{ width: `${barWidth}%` }}
                  transition={{ type: 'spring', damping: 15, stiffness: 80 }}
                />
              </div>
            </div>

            {/* Passenger cards */}
            <div className="space-y-3 mb-6">
              <AnimatePresence>
                {passengers.map(p => (
                  <motion.div
                    key={p.id}
                    initial={{ opacity: 0, y: -10, scale: 0.95 }}
                    animate={{ opacity: 1, y: 0, scale: 1 }}
                    exit={{ opacity: 0, scale: 0.9 }}
                    transition={{ duration: 0.3 }}
                    className={`p-4 rounded-xl border flex items-center justify-between gap-3 transition-colors ${
                      p.state === 'shouting'
                        ? "bg-[var(--module-danger-soft)] dark:bg-[var(--module-danger-soft)] border-[var(--module-line)] dark:border-[var(--module-line)]"
                        : "bg-[var(--module-surface)] dark:bg-[var(--module-surface)] border-[var(--module-line)] dark:border-[var(--module-line)]"
                    }`}
                  >
                    <div className="flex-1 min-w-0">
                      <p className={`text-sm font-medium ${
                        p.state === 'shouting'
                          ? "text-[var(--module-danger-text)] dark:text-[var(--module-danger-text)]"
                          : "text-[var(--module-muted)] dark:text-[var(--module-muted)] line-through"
                      }`}>
                        {p.state === 'shouting' && (
                          <motion.span
                            animate={{ opacity: [1, 0.5, 1] }}
                            transition={{ duration: 1.5, repeat: Infinity }}
                            className="inline-block w-2 h-2 rounded-full bg-[var(--module-danger)] mr-2 align-middle"
                          />
                        )}
                        "{p.text}"
                      </p>
                      {p.state === 'acknowledged' && (
                        <p className="text-[10px] text-[var(--module-muted)] dark:text-[var(--module-muted)] mt-1">Still here. No longer in control.</p>
                      )}
                    </div>
                    {p.state === 'shouting' && (
                      <div className="flex gap-2 shrink-0">
                        <button
                          onClick={() => handleArgue(p.id)}
                          className="px-3 py-1.5 text-[11px] font-bold bg-[var(--module-danger-soft)] dark:bg-[var(--module-danger-soft)] text-[var(--module-danger-text)] dark:text-[var(--module-danger-text)] rounded-lg hover:bg-[var(--module-danger-soft)] dark:hover:bg-[var(--module-danger-soft)] transition-colors" data-wide-button="true"
                        >
                          Argue
                        </button>
                        <button
                          onClick={() => handleAcknowledge(p.id)}
                          className="px-3 py-1.5 text-[11px] font-bold bg-[var(--module-success-soft)] dark:bg-[var(--module-success)]/15 text-[var(--module-success-text)] dark:text-[var(--module-success-text)] rounded-lg hover:bg-[var(--module-success)]/20 dark:hover:bg-[var(--module-success)]/25 transition-colors" data-wide-button="true"
                        >
                          Acknowledge
                        </button>
                      </div>
                    )}
                  </motion.div>
                ))}
              </AnimatePresence>
            </div>

            {/* Feedback */}
            {argued > 0 && shoutingCount > 3 && (
              <motion.p
                initial={{ opacity: 0 }}
                animate={{ opacity: 1 }}
                className="text-xs text-[var(--module-danger-text)] dark:text-[var(--module-danger-text)] font-medium text-center mb-4"
              >
                Notice: arguing created {passengers.length - 3} new thought{passengers.length - 3 > 1 ? 's' : ''}. Fighting thoughts makes them multiply.
              </motion.p>
            )}

            {allAcknowledged && (
              <motion.div
                initial={{ opacity: 0, y: 8 }}
                animate={{ opacity: 1, y: 0 }}
                className="p-4 bg-[var(--module-success-soft)] dark:bg-[var(--module-success)]/15 border border-success/30 dark:border-success/40 rounded-xl text-sm text-[var(--module-success-text)] dark:text-[var(--module-success-text)] font-medium text-center mb-4"
              >
                The passengers are still on the bus — but you're driving. That's defusion.
              </motion.div>
            )}

            <div className="flex justify-center">
              <button
                onClick={handleReset}
                className="px-4 py-2 text-xs font-bold bg-[var(--module-surface)] dark:bg-[var(--module-surface)] text-[var(--module-ink)] dark:text-[var(--module-muted)] rounded-lg hover:bg-[var(--module-surface)] dark:hover:bg-[var(--module-surface)] transition-colors" data-wide-button="true"
              >
                Reset
              </button>
            </div>
        </div>
    );
}

const CHAIN_LENGTH = 5;

const _chainColors = [
  { bg: "bg-[var(--module-danger-soft)] dark:bg-[var(--module-danger-soft)]", border: "border-[var(--module-line)] dark:border-[var(--module-line)]", text: "text-[var(--module-danger-text)] dark:text-[var(--module-danger-text)]", label: "text-[var(--module-danger-text)]", dot: "bg-[var(--module-danger)]", arrow: "text-[var(--module-danger-text)]" },
  { bg: "bg-[var(--module-surface)] dark:bg-[var(--module-surface)]", border: "border-[var(--module-line)] dark:border-[var(--module-line)]", text: "text-[var(--module-ink)] dark:text-[var(--module-ink)]", label: "text-[var(--module-ink)]", dot: "bg-[var(--module-orange)]", arrow: "text-[var(--module-ink)]" },
  { bg: "bg-[var(--module-surface)] dark:bg-[var(--module-surface)]", border: "border-[var(--module-line)] dark:border-[var(--module-line)]", text: "text-[var(--module-ink)] dark:text-[var(--module-ink)]", label: "text-[var(--module-ink)]", dot: "bg-[var(--module-surface)]", arrow: "text-[var(--module-ink)]" },
  { bg: "bg-[var(--module-surface)] dark:bg-[var(--module-surface)]", border: "border-[var(--module-line)] dark:border-[var(--module-line)]", text: "text-[var(--module-ink)] dark:text-[var(--module-muted)]", label: "text-[var(--module-muted)]", dot: "bg-[var(--module-surface)]", arrow: "text-[var(--module-muted)]" },
  { bg: "bg-[var(--module-success-soft)] dark:bg-[var(--module-success-soft)]", border: "border-[var(--module-line)] dark:border-[var(--module-line)]", text: "text-[var(--module-success-text)] dark:text-[var(--module-success-text)]", label: "text-[var(--module-success-text)]", dot: "bg-[var(--module-success)]", arrow: "text-[var(--module-success-text)]" },
];

const DownwardArrowDrill = () => {
  const [entries, setEntries] = useState<string[]>(['']);
  const [committed, setCommitted] = useState<boolean[]>([false]);
  const [showReflection, setShowReflection] = useState(false);

  const currentStep = committed.filter(Boolean).length;

  const handleChange = (index: number, value: string) => {
    setEntries(prev => {
      const next = [...prev];
      next[index] = value;
      return next;
    });
  };

  const handleNext = (index: number) => {
    if (!entries[index].trim()) return;
    setCommitted(prev => {
      const next = [...prev];
      next[index] = true;
      return next;
    });
    if (index + 1 < CHAIN_LENGTH) {
      setEntries(prev => [...prev, '']);
      setCommitted(prev => [...prev, false]);
    } else {
      setShowReflection(true);
    }
  };

  const handleReset = () => {
    setEntries(['']);
    setCommitted([false]);
    setShowReflection(false);
  };

  const handleKeyDown = (e: React.KeyboardEvent, index: number) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleNext(index);
    }
  };

  return (
    <div className="my-10 rounded-2xl p-6 md:p-8" style={{ backgroundColor: "var(--module-surface)", borderRadius: 18 }}>
      <h4 className="font-serif text-2xl font-bold text-center" style={{ color: "var(--module-ink)" }}>The Downward Arrow</h4>
      <p className="text-center text-sm mt-2 mb-8" style={{ color: "var(--module-muted)" }}>Follow the fear to its end. Ask "And then what?" until the catastrophe dissolves.</p>

      <div className="flex flex-col items-center max-w-lg mx-auto">
        {entries.map((entry, index) => {
          const isActive = !committed[index];
          const isLocked = index > currentStep;
          return (
            <React.Fragment key={index}>
              {/* Connector between cards */}
              {index > 0 && (
                <MotionDiv
                  initial={{ opacity: 0, y: -8 }}
                  animate={{ opacity: 1, y: 0 }}
                  transition={{ duration: 0.4, delay: 0.1 }}
                  className="flex flex-col items-center my-1"
                >
                  <div style={{ width: 2, height: 32, backgroundColor: moduleFill(committed[index] || isActive ? "var(--module-surface)" : "var(--module-surface)") }} />
                  <svg width="16" height="10" viewBox="0 0 16 10" fill="none">
                    <path d="M1 1L8 8L15 1" stroke={committed[index] || isActive ? "var(--module-danger-text)" : "var(--module-muted)"} strokeWidth="2.5" strokeLinecap="round" strokeLinejoin="round"/>
                  </svg>
                </MotionDiv>
              )}

              {/* Entry card */}
              <MotionDiv
                initial={{ opacity: 0, y: 16, scale: 0.95 }}
                animate={{ opacity: 1, y: 0, scale: 1 }}
                transition={{ duration: 0.4, delay: index * 0.1 }}
                className="w-full"
              >
                <div
                  style={{
                    backgroundColor: moduleFill(isActive ? "var(--module-surface)" : isLocked ? "var(--module-surface)" : "var(--module-surface)"),
                    border: isActive ? "2px solid var(--module-line)" : isLocked ? "2px solid var(--module-line)" : "2px solid var(--module-line)",
                    borderRadius: 14,
                    padding: '18px 22px',
                  }}
                >
                  <p className="text-[11px] font-bold uppercase tracking-wider mb-2" style={{ color: moduleText(isLocked ? "var(--module-muted)" : "var(--module-danger-text)") }}>
                    {index === 0 ? 'The exam thought that scares you most' : `Level ${index + 1}: And then what?`}
                  </p>

                  {committed[index] ? (
                    <p className="font-serif italic" style={{ fontSize: 16, color: "var(--module-ink)" }}>"{entry}"</p>
                  ) : (
                    <div className="flex flex-col gap-3">
                      <input
                        type="text"
                        value={entry}
                        onChange={e => handleChange(index, e.target.value)}
                        onKeyDown={e => handleKeyDown(e, index)}
                        placeholder={index === 0 ? "I'll fail my exam" : "If that happened, then..."}
                        className="w-full bg-[var(--module-surface)] dark:bg-[var(--module-surface)] rounded-xl px-4 py-3 text-sm text-[var(--module-ink)] dark:text-[var(--module-ink)] placeholder-zinc-400 outline-none"
                        style={{ border: "1.5px solid var(--module-line)" }}
                      />
                      <button
                        onClick={() => handleNext(index)}
                        disabled={!entry.trim()}
                        className="self-end px-5 py-2.5 text-xs font-bold text-[var(--module-ink)] transition-colors disabled:opacity-40 disabled:cursor-not-allowed"
                        style={{ backgroundColor: "var(--module-danger)", borderRadius: 10 }} data-wide-button="true"
                      >
                        {index + 1 < CHAIN_LENGTH ? 'And then what happens?' : 'See the full chain'}
                      </button>
                    </div>
                  )}
                </div>
              </MotionDiv>
            </React.Fragment>
          );
        })}
      </div>

      {/* Reflection — catastrophe dissolved */}
      <AnimatePresence>
        {showReflection && (
          <MotionDiv
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            exit={{ opacity: 0, y: 20 }}
            transition={{ duration: 0.5, delay: 0.2 }}
            className="mt-8 max-w-lg mx-auto"
          >
            <div style={{ backgroundColor: "var(--module-surface)", border: "2px solid var(--module-line)", borderRadius: 14, padding: '18px 22px' }}>
              <p className="text-[11px] font-bold uppercase tracking-wider mb-3" style={{ color: "var(--module-danger-text)" }}>Catastrophe Dissolved</p>

              <div className="space-y-2 mb-5">
                {entries.filter((_, i) => committed[i]).map((entry, index) => (
                  <div key={index} className="flex items-center gap-3">
                    <span className="w-6 h-6 rounded-full flex items-center justify-center shrink-0 text-[10px] font-bold text-[var(--module-ink)]" style={{ backgroundColor: "var(--module-danger)" }}>{index + 1}</span>
                    <p className="text-sm font-serif italic" style={{ color: "var(--module-danger-text)" }}>{entry}</p>
                  </div>
                ))}
              </div>

              <p className="text-sm mb-1" style={{ color: "var(--module-danger-text)" }}>Is your final answer really as catastrophic as the first one felt?</p>
              <p className="text-sm font-serif italic font-medium" style={{ color: "var(--module-danger-text)" }}>Most catastrophic chains end somewhere manageable. The fear lives in the ambiguity — not the reality.</p>
            </div>
          </MotionDiv>
        )}
      </AnimatePresence>

      {/* Reset */}
      {currentStep > 0 && (
        <div className="flex justify-center mt-6">
          <button onClick={handleReset} className="text-sm font-medium transition-colors hover:underline" style={{ color: "var(--module-muted)" }} data-wide-button="true">
            Start Over
          </button>
        </div>
      )}
    </div>
  );
};

// --- MODULE COMPONENT ---
const CatastrophicThinkingModule: React.FC<{ onBack: () => void; progress: ModuleProgress; onProgressUpdate: (progress: ModuleProgress) => void }> = ({ onBack, progress, onProgressUpdate }) => {
  const essentials = useEssentialsMode();

  const sections = essentials ? [
    { id: 'catastrophe-machine', title: 'The Catastrophe Machine', eyebrow: '01 // The Problem', icon: MessageSquare },
    { id: 'thought-record', title: 'The Thought Record (CBT)', eyebrow: '02 // The Core Tool', icon: Wrench },
    { id: 'decatastrophize', title: 'Decatastrophizing & Defusion', eyebrow: '03 // Breaking the Spiral', icon: Layers },
    { id: 'action-plan', title: 'The Action Plan', eyebrow: '04 // The Blueprint', icon: Flag },
  ] : [
    { id: 'catastrophe-machine', title: 'The Catastrophe Machine', eyebrow: '01 // The Problem', icon: MessageSquare },
    { id: 'blank-mind', title: 'Why You Go "Blank"', eyebrow: '02 // What Happens in Your Brain', icon: BrainCircuit },
    { id: 'cbt-standard', title: 'Challenging Your Thoughts (CBT)', eyebrow: '03 // The Main Approach', icon: BookOpen },
    { id: 'thought-record', title: 'The Thought Record', eyebrow: '04 // The Core Tool', icon: Wrench },
    { id: 'decatastrophize', title: 'Decatastrophizing', eyebrow: '05 // The "So What?" Drill', icon: Layers },
    { id: 'face-fear', title: 'Facing the Fear', eyebrow: '06 // Exposure', icon: Shield },
    { id: 'observer-self', title: 'Stepping Back from Your Thoughts', eyebrow: '07 // A Different Approach', icon: Zap },
    { id: 'action-plan', title: 'The Action Plan', eyebrow: '08 // The Blueprint', icon: Flag },
  ];

  return (
    <ModuleLayout
      moduleNumber="12"
      moduleTitle="Reframing Thoughts"
      moduleSubtitle="The CBT Toolkit"
      moduleDescription="Ever had your brain spiral into worst-case scenarios before an exam? This module gives you practical tools to catch those thoughts, challenge them, and take back control."
      theme={theme}
      sections={sections}
      fullSectionsCount={8}
      references={CATASTROPHIC_THINKING_REFERENCE_LIST}
      onBack={onBack}
      progress={progress}
      onProgressUpdate={onProgressUpdate}
      finishButtonText="Take Back Control"
    >
      {(activeSection) => (
        <>
          {activeSection === 0 && (
            <ReadingSection title="The Catastrophe Machine." eyebrow="Step 1" icon={MessageSquare} theme={theme}>
              <p>{essentials ? 'Exam anxiety runs on' : ''} <Highlight description="When your brain jumps straight to the worst possible outcome and convinces you it's definitely going to happen. Like thinking one bad mock result means your life is over." theme={theme}>Catastrophizing</Highlight>{essentials ? '. It has three parts. Name them and you can dismantle them.' : ' is the engine of exam anxiety. It\'s a 3-part machine — and once you can name the parts, you can start to dismantle them.'}</p>
              <ConceptCardGrid
                cards={[
                  { number: 1, term: "Rumination", description: "That one negative thought that plays on repeat in your head, like a song you can't get rid of. The thought you can't switch off." },
                  { number: 2, term: "Magnification", description: "Making things way bigger than they actually are. One bad test becomes proof you'll fail everything. Making a mountain out of a molehill." },
                  { number: 3, term: "Helplessness", description: "That sinking feeling where you're convinced the bad thing is going to happen and there's nothing you can do about it." },
                ]}
              />
            </ReadingSection>
          )}
          {!essentials && activeSection === 1 && (
            <ReadingSection title="Why You Go 'Blank'." eyebrow="Step 2" icon={BrainCircuit} theme={theme}>
              <p>Going "blank" in an exam isn't just in your head -- it's a real physical thing. When your brain decides the exam paper is a threat, your <Highlight description="The part of your brain that acts like a smoke alarm. It detects danger and hits the panic button, even when the 'danger' is just an exam paper." theme={theme}>amygdala</Highlight> triggers a stress response, flooding you with stress hormones. Those hormones basically block your <Highlight description="The part of your brain that stores and retrieves memories. When you're stressed, it gets shut down -- which is why you can't remember stuff you definitely studied." theme={theme}>hippocampus</Highlight>, which is the part that pulls up memories.<Cite n={1} /> Meanwhile, the <Highlight description="The part of your brain that handles logical thinking and planning. When you're panicking, it goes quiet -- which is why you can't think straight under pressure." theme={theme}>front of your brain</Highlight> -- the bit that does logical thinking -- goes quiet. You haven't forgotten the information; you've just temporarily lost the password.</p>
            </ReadingSection>
          )}
          {!essentials && activeSection === 2 && (
            <ReadingSection title="Challenging Your Thoughts (CBT)." eyebrow="Step 3" icon={BookOpen} theme={theme}>
              <p><Highlight description="CBT stands for Cognitive Behavioral Therapy. Basically, it's a way of noticing the thoughts that make you feel awful and learning to question whether they're actually true." theme={theme}>CBT</Highlight> is one of the most effective, best-evidenced ways to break the panic cycle.<Cite n={2} /> The big idea is actually pretty simple: it's not the exam that makes you panic -- it's what you <em>think</em> about the exam. The exam paper is just paper. The thought "I can't do this" is what triggers the panic. CBT teaches you to catch that thought and challenge it.</p>
            </ReadingSection>
          )}
          {(essentials ? activeSection === 1 : activeSection === 3) && (
            <ReadingSection title={essentials ? "The Thought Record (CBT)." : "The Thought Record."} eyebrow={essentials ? "Step 2" : "Step 4"} icon={Wrench} theme={theme}>
              {essentials ? (
                <p><Highlight description="Cognitive Behavioral Therapy — a way of noticing the thoughts that make you feel awful and learning to question whether they're actually true." theme={theme}>CBT</Highlight> says it's not the exam that causes panic. It's what you think about the exam. The <Highlight description="A step-by-step exercise where you write down the negative thought that's bothering you, look at the actual evidence for and against it, and come up with a more realistic way to see things." theme={theme}>Thought Record</Highlight> gets you out of your head.<Cite n={2} /> Write down the scary thought. List evidence for and against it. Create a balanced alternative.</p>
              ) : (
                <p>The main tool in CBT is the <Highlight description="A step-by-step exercise where you write down the negative thought that's bothering you, look at the actual evidence for and against it, and come up with a more realistic way to see things." theme={theme}>Thought Record</Highlight>.<Cite n={2} /> It gets you out of your head and onto paper. Instead of spiralling with vague panic, you look at the actual facts -- what really supports this scary thought, and what goes against it? Then you come up with a more balanced take. Try using it whenever you feel panic building.</p>
              )}
              <ThoughtRecord />
            </ReadingSection>
          )}
          {(essentials ? activeSection === 2 : activeSection === 4) && (
            <ReadingSection title={essentials ? "Decatastrophizing & Defusion." : "Decatastrophizing."} eyebrow={essentials ? "Step 3" : "Step 5"} icon={Layers} theme={theme}>
              {essentials ? (
                <>
                  <p>Face the worst-case head-on with the <Highlight description="You take your scariest thought and keep asking 'And then what?' until you reach the end. Most of the time, you'll realise the final outcome is actually something you could deal with." theme={theme}>Downward Arrow</Highlight>. Keep asking "And then what?" The end is usually survivable.</p>
                  <DownwardArrowDrill />
                  <p>Sometimes arguing with thoughts makes them louder. Try <Highlight description="Unhooking from your thoughts. Instead of treating every thought as the truth, you learn to see them as just words passing through your head -- like background noise you don't have to obey." theme={theme}>defusion</Highlight> instead (a core idea in Acceptance and Commitment Therapy).<Cite n={3} /> Notice the thought. Let it be there. Keep driving toward your goal.</p>
                  <PassengersOnBus/>
                </>
              ) : (
                <>
                  <p>This isn't about pretending "it will all be fine." Instead, you face the worst-case scenario head-on and take away its power. It's called the <Highlight description="You take your scariest thought and keep asking 'And then what?' until you reach the end. Most of the time, you'll realise the final outcome is actually something you could deal with." theme={theme}>Downward Arrow</Highlight> technique. By following the "what if" chain all the way to the end, you usually realise the worst case is actually survivable -- and you can make a backup plan for it.</p>
                  <DownwardArrowDrill />
                </>
              )}
            </ReadingSection>
          )}
          {!essentials && activeSection === 5 && (
            <ReadingSection title="Facing the Fear." eyebrow="Step 6" icon={Shield} theme={theme}>
              <p>Anxiety creates a vicious cycle. You're scared of a subject, so you avoid it, which means you're less prepared, which makes the fear even worse. A well-evidenced way to break this is <Highlight description="Instead of diving into the scariest thing all at once, you break it into small steps -- starting with what feels easiest and gradually working up. Your brain learns that it's not as bad as it thought." theme={theme}>Graded Exposure</Highlight>.<Cite n={2} /> You build a "ladder" of tasks, from least scary to most scary, and work your way up step by step. Each time, your brain learns that the thing it was dreading isn't actually that bad.</p>
              <GradedExposureHierarchy/>
            </ReadingSection>
          )}
          {!essentials && activeSection === 6 && (
            <ReadingSection title="Stepping Back from Your Thoughts." eyebrow="Step 7" icon={Zap} theme={theme}>
              <p>Sometimes trying to argue with negative thoughts just makes them louder. <Highlight description="ACT is a different approach. Instead of fighting your negative thoughts, you learn to notice them without letting them control you. You accept the thought is there, but you keep doing what matters to you anyway." theme={theme}>ACT (Acceptance and Commitment Therapy)</Highlight> offers an alternative: instead of arguing with the thought, just notice it's there and keep going anyway.<Cite n={3} /> This is called <Highlight description="Unhooking from your thoughts. Instead of treating every thought as the truth, you learn to see them as just words passing through your head -- like background noise you don't have to obey." theme={theme}>defusion</Highlight>.</p>
              <PassengersOnBus/>
            </ReadingSection>
          )}
          {(essentials ? activeSection === 3 : activeSection === 7) && (
            <ReadingSection title="The Action Plan." eyebrow={essentials ? "Step 4" : "Step 8"} icon={Flag} theme={theme}>
              <p>{essentials ? 'You now have tools to challenge thoughts (Thought Record) and step back from them (defusion). Pick one and use it once this week.' : 'You now have a proper toolkit for dealing with exam anxiety. You\'ve got ways to challenge your thoughts (CBT) and ways to step back from them (ACT), alongside the physical stuff (sleep, food, exercise) from other modules. Now it\'s about actually using them.'}</p>
              <SupportSignpost />
              <MicroCommitment theme={theme}><p>Pick ONE tool from this module -- the Thought Record, Downward Arrow, or an Exposure task. Use it just once this week. That's it. The more you practise, the more automatic it becomes.</p></MicroCommitment>
            </ReadingSection>
          )}
        </>
      )}
    </ModuleLayout>
  );
};
export default CatastrophicThinkingModule;
