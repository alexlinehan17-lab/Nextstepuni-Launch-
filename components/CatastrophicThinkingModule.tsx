/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
*/

import React, { useState } from 'react';
import { motion, AnimatePresence, Reorder } from 'framer-motion';
import {
  MessageSquare, BrainCircuit, BookOpen, Wrench, Layers, Shield, Zap, Flag, ArrowDown
} from 'lucide-react';
import { ModuleProgress } from '../types';
import { slateTheme } from '../moduleThemes';
import { Highlight, ReadingSection, MicroCommitment } from './ModuleShared';
import { ModuleLayout } from './ModuleLayout';

const theme = slateTheme;

// --- INTERACTIVE COMPONENTS ---

const ThoughtRecord = () => {
    const [step, setStep] = useState(0);
    const [record, setRecord] = useState({ situation: '', emotion: '', intensity: 90, nat: '', evidenceFor: '', evidenceAgainst: '', alternative: '', reRate: 50});
    const update = (field: string, value: any) => setRecord(prev => ({...prev, [field]: value}));

    const steps = ['Situation', 'Emotion', 'Negative Thought', 'Evidence For', 'Evidence Against', 'Alternative', 'Re-Rate'];

    return (
        <div className="my-10 p-8 md:p-12 bg-white dark:bg-zinc-800 rounded-xl border border-zinc-200 dark:border-zinc-700">
             <h4 className="font-serif text-2xl font-semibold text-zinc-800 dark:text-white text-center">The Thought Record</h4>
             <div className="flex justify-between my-4"><div className="w-full h-1 bg-zinc-100 dark:bg-zinc-800 rounded-full"><motion.div className="h-1 bg-slate-500 rounded-full" animate={{width: `${(step / (steps.length - 1)) * 100}%`}}/></div></div>
             <AnimatePresence mode="wait">
             <motion.div key={step} initial={{opacity:0, x:20}} animate={{opacity:1, x:0}} exit={{opacity:0, x:-20}} >
                {step === 0 && <div><label className="font-bold">1. Situation:</label><input value={record.situation} onChange={e => update('situation', e.target.value)} placeholder="e.g., Sitting down to study History" className="w-full p-2 mt-2 bg-zinc-50 dark:bg-zinc-800/50 rounded-lg"/></div>}
                {step === 1 && <div><label className="font-bold">2. Emotion:</label><input value={record.emotion} onChange={e => update('emotion', e.target.value)} placeholder="e.g., Panic" className="w-full p-2 mt-2 bg-zinc-50 dark:bg-zinc-800/50 rounded-lg"/><label>Intensity: {record.intensity}%</label><input type="range" value={record.intensity} onChange={e => update('intensity', e.target.value)} className="w-full"/></div>}
                {step === 2 && <div><label className="font-bold">3. Negative Automatic Thought (NAT):</label><textarea value={record.nat} onChange={e => update('nat', e.target.value)} placeholder="e.g., I'll never remember all these dates." className="w-full p-2 mt-2 bg-zinc-50 dark:bg-zinc-800/50 rounded-lg h-24"/></div>}
                {step === 3 && <div><label className="font-bold">4. Evidence For:</label><textarea value={record.evidenceFor} onChange={e => update('evidenceFor', e.target.value)} placeholder="e.g., I got some dates wrong on last week's test." className="w-full p-2 mt-2 bg-zinc-50 dark:bg-zinc-800/50 rounded-lg h-24"/></div>}
                {step === 4 && <div><label className="font-bold">5. Evidence Against:</label><textarea value={record.evidenceAgainst} onChange={e => update('evidenceAgainst', e.target.value)} placeholder="e.g., I passed my last test. I have 3 months to study." className="w-full p-2 mt-2 bg-zinc-50 dark:bg-zinc-800/50 rounded-lg h-24"/></div>}
                {step === 5 && <div><label className="font-bold">6. Alternative Thought:</label><textarea value={record.alternative} onChange={e => update('alternative', e.target.value)} placeholder="e.g., History is hard, but if I use flashcards I can pass." className="w-full p-2 mt-2 bg-zinc-50 dark:bg-zinc-800/50 rounded-lg h-24"/></div>}
                {step === 6 && <div className="space-y-4"><label className="font-bold">7. Re-Rate Emotion:</label>{record.alternative && <div className="p-3 bg-emerald-50 dark:bg-emerald-950/30 border border-emerald-200 dark:border-emerald-800/50 rounded-lg"><p className="text-[10px] font-bold uppercase tracking-wider text-emerald-500 mb-1">Your Alternative Thought</p><p className="text-sm text-emerald-700 dark:text-emerald-300">{record.alternative}</p></div>}<p className="text-sm">Initial Panic: <span className="font-bold text-rose-500">{record.intensity}%</span></p><label className="text-sm">New Panic Level: <span className="font-bold">{record.reRate}%</span></label><input type="range" value={record.reRate} onChange={e => update('reRate', e.target.value)} className="w-full"/>{Number(record.reRate) < Number(record.intensity) && <p className="text-xs text-emerald-600 dark:text-emerald-400 font-medium">Panic reduced by {Number(record.intensity) - Number(record.reRate)}%. The reframe is working.</p>}</div>}
             </motion.div>
             </AnimatePresence>
             <div className="flex justify-between mt-4">
                <button onClick={() => setStep(s=>Math.max(0,s-1))} disabled={step===0} className="px-3 py-1 text-xs bg-zinc-200 rounded-md disabled:opacity-50">Prev</button>
                <button onClick={() => setStep(s=>Math.min(steps.length-1,s+1))} disabled={step===steps.length-1} className="px-3 py-1 text-xs bg-zinc-200 rounded-md disabled:opacity-50">Next</button>
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
        <div className="my-10 p-8 md:p-12 bg-white dark:bg-zinc-800 rounded-xl border border-zinc-200 dark:border-zinc-700">
             <h4 className="font-serif text-2xl font-semibold text-zinc-800 dark:text-white text-center">Exposure Hierarchy Builder</h4>
             <Reorder.Group axis="y" values={items} onReorder={setItems} className="space-y-2 mt-6">
                {items.map(item => (
                    <Reorder.Item key={item.id} value={item} className="p-3 bg-zinc-100 dark:bg-zinc-800 rounded-lg flex justify-between items-center cursor-grab active:cursor-grabbing">
                        <span>{item.text}</span>
                        <span className="font-bold text-sm text-rose-500">{item.suds} SUDS</span>
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
    const speedColor = allAcknowledged ? 'text-emerald-500' : shoutingCount <= 1 ? 'text-emerald-400' : shoutingCount <= 3 ? 'text-amber-500' : 'text-rose-500';
    const barWidth = allAcknowledged ? 100 : Math.max(5, Math.round(100 - (shoutingCount / Math.max(1, totalCount)) * 100));
    const barColor = allAcknowledged ? 'bg-emerald-500' : shoutingCount <= 1 ? 'bg-emerald-400' : shoutingCount <= 3 ? 'bg-amber-500' : 'bg-rose-500';

    return (
         <div className="my-10 p-8 md:p-12 bg-white dark:bg-zinc-800 rounded-xl border border-zinc-200 dark:border-zinc-700">
            <h4 className="font-serif text-2xl font-semibold text-zinc-800 dark:text-white text-center">Passengers on the Bus</h4>
            <p className="text-center text-sm text-zinc-500 dark:text-zinc-400 mb-2">You're driving toward your goal. Negative thoughts are passengers shouting at you.</p>
            <p className="text-center text-xs text-zinc-400 dark:text-zinc-500 mb-6">You can't kick them off. But you can choose how to respond.</p>

            {/* Speed indicator */}
            <div className="mb-6 p-4 bg-zinc-50 dark:bg-zinc-900/50 rounded-xl">
              <div className="flex justify-between items-center mb-2">
                <p className="text-xs font-bold text-zinc-500 dark:text-zinc-400">Progress Toward Your Goal</p>
                <p className={`text-xs font-bold ${speedColor}`}>{speed}</p>
              </div>
              <div className="w-full h-2.5 bg-zinc-200 dark:bg-zinc-700 rounded-full overflow-hidden">
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
                        ? 'bg-rose-50 dark:bg-rose-950/20 border-rose-200 dark:border-rose-800/50'
                        : 'bg-zinc-50 dark:bg-zinc-900/30 border-zinc-200 dark:border-zinc-700'
                    }`}
                  >
                    <div className="flex-1 min-w-0">
                      <p className={`text-sm font-medium ${
                        p.state === 'shouting'
                          ? 'text-rose-700 dark:text-rose-300'
                          : 'text-zinc-400 dark:text-zinc-500 line-through'
                      }`}>
                        {p.state === 'shouting' && (
                          <motion.span
                            animate={{ opacity: [1, 0.5, 1] }}
                            transition={{ duration: 1.5, repeat: Infinity }}
                            className="inline-block w-2 h-2 rounded-full bg-rose-500 mr-2 align-middle"
                          />
                        )}
                        "{p.text}"
                      </p>
                      {p.state === 'acknowledged' && (
                        <p className="text-[10px] text-zinc-400 dark:text-zinc-500 mt-1">Still here. No longer in control.</p>
                      )}
                    </div>
                    {p.state === 'shouting' && (
                      <div className="flex gap-2 shrink-0">
                        <button
                          onClick={() => handleArgue(p.id)}
                          className="px-3 py-1.5 text-[11px] font-bold bg-rose-100 dark:bg-rose-900/40 text-rose-700 dark:text-rose-300 rounded-lg hover:bg-rose-200 dark:hover:bg-rose-900/60 transition-colors"
                        >
                          Argue
                        </button>
                        <button
                          onClick={() => handleAcknowledge(p.id)}
                          className="px-3 py-1.5 text-[11px] font-bold bg-emerald-100 dark:bg-emerald-900/40 text-emerald-700 dark:text-emerald-300 rounded-lg hover:bg-emerald-200 dark:hover:bg-emerald-900/60 transition-colors"
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
                className="text-xs text-rose-500 dark:text-rose-400 font-medium text-center mb-4"
              >
                Notice: arguing created {passengers.length - 3} new thought{passengers.length - 3 > 1 ? 's' : ''}. Fighting thoughts makes them multiply.
              </motion.p>
            )}

            {allAcknowledged && (
              <motion.div
                initial={{ opacity: 0, y: 8 }}
                animate={{ opacity: 1, y: 0 }}
                className="p-4 bg-emerald-50 dark:bg-emerald-950/30 border border-emerald-200 dark:border-emerald-800/50 rounded-xl text-sm text-emerald-700 dark:text-emerald-300 font-medium text-center mb-4"
              >
                The passengers are still on the bus — but you're driving. That's defusion.
              </motion.div>
            )}

            <div className="flex justify-center">
              <button
                onClick={handleReset}
                className="px-4 py-2 text-xs font-bold bg-zinc-100 dark:bg-zinc-700 text-zinc-600 dark:text-zinc-300 rounded-lg hover:bg-zinc-200 dark:hover:bg-zinc-600 transition-colors"
              >
                Reset
              </button>
            </div>
        </div>
    );
}

const MotionDiv = motion.div as any;

const CHAIN_LENGTH = 5;

const chainColors = [
  { bg: 'bg-rose-50 dark:bg-rose-950/30', border: 'border-rose-200 dark:border-rose-800/50', text: 'text-rose-700 dark:text-rose-300', label: 'text-rose-500', dot: 'bg-rose-500', arrow: 'text-rose-400' },
  { bg: 'bg-orange-50 dark:bg-orange-950/30', border: 'border-orange-200 dark:border-orange-800/50', text: 'text-orange-700 dark:text-orange-300', label: 'text-orange-500', dot: 'bg-orange-500', arrow: 'text-orange-400' },
  { bg: 'bg-amber-50 dark:bg-amber-950/30', border: 'border-amber-200 dark:border-amber-800/50', text: 'text-amber-700 dark:text-amber-300', label: 'text-amber-500', dot: 'bg-amber-500', arrow: 'text-amber-400' },
  { bg: 'bg-zinc-50 dark:bg-zinc-800/50', border: 'border-zinc-200 dark:border-zinc-700', text: 'text-zinc-700 dark:text-zinc-300', label: 'text-zinc-500', dot: 'bg-zinc-400', arrow: 'text-zinc-400' },
  { bg: 'bg-emerald-50 dark:bg-emerald-950/30', border: 'border-emerald-200 dark:border-emerald-800/50', text: 'text-emerald-700 dark:text-emerald-300', label: 'text-emerald-500', dot: 'bg-emerald-500', arrow: 'text-emerald-400' },
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
    <div className="my-10 p-8 md:p-12 bg-white dark:bg-zinc-800 rounded-xl border border-zinc-200 dark:border-zinc-700">
      <h4 className="font-serif text-2xl font-semibold text-zinc-800 dark:text-white text-center">The Downward Arrow</h4>
      <p className="text-center text-sm text-zinc-500 dark:text-zinc-400 mt-2 mb-8">Follow the fear to its end. Ask "And then what?" until the catastrophe dissolves.</p>

      <div className="flex flex-col items-center">
        {entries.map((entry, index) => (
          <React.Fragment key={index}>
            {/* Animated arrow between entries */}
            {index > 0 && (
              <MotionDiv
                initial={{ opacity: 0, y: -8 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ duration: 0.4, delay: 0.1 }}
                className="flex flex-col items-center my-2"
              >
                <div className={`w-0.5 h-6 ${chainColors[Math.min(index, CHAIN_LENGTH - 1)].dot}`} />
                <ArrowDown className={`w-5 h-5 ${chainColors[Math.min(index, CHAIN_LENGTH - 1)].arrow}`} />
              </MotionDiv>
            )}

            {/* Entry card */}
            <MotionDiv
              initial={{ opacity: 0, y: 16, scale: 0.95 }}
              animate={{ opacity: 1, y: 0, scale: 1 }}
              transition={{ duration: 0.4, delay: index * 0.1 }}
              className="w-full"
            >
              <div className={`p-4 rounded-xl border ${chainColors[Math.min(index, CHAIN_LENGTH - 1)].bg} ${chainColors[Math.min(index, CHAIN_LENGTH - 1)].border}`}>
                <p className={`text-[10px] font-bold uppercase tracking-wider mb-2 ${chainColors[Math.min(index, CHAIN_LENGTH - 1)].label}`}>
                  {index === 0 ? 'Your worst fear' : `Level ${index + 1}: And then what?`}
                </p>

                {committed[index] ? (
                  <p className={`text-sm font-medium ${chainColors[Math.min(index, CHAIN_LENGTH - 1)].text}`}>"{entry}"</p>
                ) : (
                  <div className="flex flex-col gap-3">
                    <input
                      type="text"
                      value={entry}
                      onChange={e => handleChange(index, e.target.value)}
                      onKeyDown={e => handleKeyDown(e, index)}
                      placeholder={index === 0 ? "I'll fail my exam" : "If that happened, then..."}
                      className="w-full p-3 text-sm bg-white dark:bg-zinc-900/50 border border-zinc-200 dark:border-zinc-700 rounded-lg text-zinc-800 dark:text-white placeholder-zinc-400 dark:placeholder-zinc-500 focus:outline-none focus:ring-2 focus:ring-slate-400 dark:focus:ring-slate-500"
                    />
                    <button
                      onClick={() => handleNext(index)}
                      disabled={!entry.trim()}
                      className="self-end px-4 py-2 text-xs font-bold bg-slate-600 hover:bg-slate-700 text-white rounded-lg transition-colors disabled:opacity-40 disabled:cursor-not-allowed"
                    >
                      {index + 1 < CHAIN_LENGTH ? 'And then what happens?' : 'See the full chain'}
                    </button>
                  </div>
                )}
              </div>
            </MotionDiv>
          </React.Fragment>
        ))}
      </div>

      {/* Reflection panel */}
      <AnimatePresence>
        {showReflection && (
          <MotionDiv
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            exit={{ opacity: 0, y: 20 }}
            transition={{ duration: 0.5, delay: 0.2 }}
            className="mt-8 p-6 bg-zinc-50 dark:bg-zinc-900/50 rounded-xl border border-zinc-200 dark:border-zinc-700"
          >
            <h5 className="font-serif text-lg font-semibold text-zinc-800 dark:text-white text-center mb-4">Look at your chain.</h5>

            <div className="space-y-2 mb-6">
              {entries.filter((_, i) => committed[i]).map((entry, index) => (
                <div key={index} className={`p-3 rounded-lg border ${chainColors[index].bg} ${chainColors[index].border} flex items-center gap-3`}>
                  <span className={`shrink-0 w-2 h-2 rounded-full ${chainColors[index].dot}`} />
                  <p className={`text-sm ${chainColors[index].text}`}>{entry}</p>
                </div>
              ))}
            </div>

            <p className="text-center text-sm text-zinc-600 dark:text-zinc-400 mb-2">Is your final answer really as catastrophic as the first one felt?</p>
            <p className="text-center text-sm font-medium text-emerald-600 dark:text-emerald-400">Most catastrophic chains end somewhere manageable. The fear lives in the ambiguity — not the reality.</p>
          </MotionDiv>
        )}
      </AnimatePresence>

      {/* Reset button */}
      {currentStep > 0 && (
        <div className="flex justify-center mt-6">
          <button
            onClick={handleReset}
            className="px-4 py-2 text-xs font-bold bg-zinc-100 dark:bg-zinc-700 text-zinc-600 dark:text-zinc-300 rounded-lg hover:bg-zinc-200 dark:hover:bg-zinc-600 transition-colors"
          >
            Start Over
          </button>
        </div>
      )}
    </div>
  );
};

// --- MODULE COMPONENT ---
const CatastrophicThinkingModule: React.FC<{ onBack: () => void; progress: ModuleProgress; onProgressUpdate: (progress: ModuleProgress) => void }> = ({ onBack, progress, onProgressUpdate }) => {
  const sections = [
    { id: 'catastrophe-machine', title: 'The Catastrophe Machine', eyebrow: '01 // The Problem', icon: MessageSquare },
    { id: 'blank-mind', title: 'The Biology of "Blank Mind"', eyebrow: '02 // The Hardware', icon: BrainCircuit },
    { id: 'cbt-standard', title: 'The Gold Standard (CBT)', eyebrow: '03 // The Software', icon: BookOpen },
    { id: 'thought-record', title: 'The Thought Record', eyebrow: '04 // The Core Tool', icon: Wrench },
    { id: 'decatastrophize', title: 'Decatastrophizing', eyebrow: '05 // The "So What?" Drill', icon: Layers },
    { id: 'face-fear', title: 'Facing the Fear', eyebrow: '06 // Exposure', icon: Shield },
    { id: 'observer-self', title: 'The Observer Self (ACT)', eyebrow: '07 // The Alternative', icon: Zap },
    { id: 'action-plan', title: 'The Action Plan', eyebrow: '08 // The Blueprint', icon: Flag },
  ];

  return (
    <ModuleLayout
      moduleNumber="12"
      moduleTitle="Reframing Thoughts"
      moduleSubtitle="The CBT Toolkit"
      moduleDescription="Deconstruct the neurobiology of exam panic and learn the gold-standard psychological tools (CBT &amp; ACT) to dismantle catastrophic thinking and regain control."
      theme={theme}
      sections={sections}
      onBack={onBack}
      progress={progress}
      onProgressUpdate={onProgressUpdate}
    >
      {(activeSection) => (
        <>
          {activeSection === 0 && (
            <ReadingSection title="The Catastrophe Machine." eyebrow="Step 1" icon={MessageSquare} theme={theme}>
              <p><Highlight description="An exaggerated negative thought process about a potential threat. It's a cognitive distortion where you magnify the consequences and underestimate your ability to cope." theme={theme}>Catastrophizing</Highlight> is the engine of exam anxiety. It's a 3-part machine: 1) <Highlight description="Repetitive, intrusive thoughts about failure." theme={theme}>Rumination</Highlight> (the thought you can't switch off), 2) <Highlight description="Blowing the consequences out of proportion (e.g., 'If I get a H4, my life is over')." theme={theme}>Magnification</Highlight> (making a mountain out of a molehill), and 3) <Highlight description="The belief that the negative outcome is inevitable and you are powerless to stop it." theme={theme}>Helplessness</Highlight> (the feeling you're powerless).</p>
            </ReadingSection>
          )}
          {activeSection === 1 && (
            <ReadingSection title="The Biology of 'Blank Mind'." eyebrow="Step 2" icon={BrainCircuit} theme={theme}>
              <p>Going "blank" is not a metaphor; it's a neurobiological event. When your brain perceives a threat (the exam paper), your <Highlight description="The brain's threat detection centre." theme={theme}>amygdala</Highlight> activates the stress response, flooding your system with adrenaline and cortisol. High levels of cortisol physically inhibit your <Highlight description="The brain region essential for memory retrieval." theme={theme}>hippocampus</Highlight>, blocking access to stored information. Your logical <Highlight description="The 'CEO' of the brain, responsible for planning and logic." theme={theme}>Prefrontal Cortex</Highlight> is taken offline. You haven't forgotten the information; you've just temporarily lost the password.</p>
            </ReadingSection>
          )}
          {activeSection === 2 && (
            <ReadingSection title="The Gold Standard (CBT)." eyebrow="Step 3" icon={BookOpen} theme={theme}>
              <p><Highlight description="Cognitive Behavioral Therapy (CBT) is a form of psychological treatment that has been demonstrated to be effective for a range of problems including anxiety and depression." theme={theme}>Cognitive Behavioral Therapy (CBT)</Highlight> is the gold standard for dismantling this machine. Its central idea is simple but revolutionary: events don't cause your feelings; your *interpretation* of events causes your feelings. The exam paper is neutral. The thought "I can't do this" is the interpretation that triggers panic. CBT teaches you to challenge that interpretation.</p>
            </ReadingSection>
          )}
          {activeSection === 3 && (
            <ReadingSection title="The Thought Record." eyebrow="Step 4" icon={Wrench} theme={theme}>
              <p>The core tool of CBT is the <Highlight description="A structured exercise to identify, challenge, and reframe Negative Automatic Thoughts (NATs)." theme={theme}>Thought Record</Highlight>. It forces you to move from vague, emotional thinking to specific, evidence-based reasoning. By systematically examining the evidence for and against your catastrophic thought, you can generate a more balanced, realistic alternative. Run this protocol every time you feel a spike of panic.</p>
              <ThoughtRecord />
            </ReadingSection>
          )}
          {activeSection === 4 && (
            <ReadingSection title="Decatastrophizing." eyebrow="Step 5" icon={Layers} theme={theme}>
              <p>This technique doesn't promise "it will all be fine." Instead, it confronts the worst-case scenario head-on to strip it of its terror. It's called the <Highlight description="A CBT technique where you follow a catastrophic thought to its conclusion by repeatedly asking 'And then what?' to reveal that the ultimate outcome is manageable." theme={theme}>Downward Arrow</Highlight> technique. By following the "what if" chain to its end, you realize the ultimate outcome is survivable, and you create a "Plan B."</p>
              <DownwardArrowDrill />
            </ReadingSection>
          )}
          {activeSection === 5 && (
            <ReadingSection title="Facing the Fear." eyebrow="Step 6" icon={Shield} theme={theme}>
              <p>Anxiety creates a vicious cycle of avoidance. You fear a subject, so you avoid it, which makes you unprepared, which justifies the original fear. The only way to break this cycle is <Highlight description="A behavioral technique where you face a feared stimulus in small, incremental steps, allowing your brain to 'habituate' and learn that it is not a threat." theme={theme}>Graded Exposure</Highlight>. You build a "ladder" of feared tasks, from least scary to most scary, and slowly work your way up, retraining your brain's alarm system.</p>
              <GradedExposureHierarchy/>
            </ReadingSection>
          )}
          {activeSection === 6 && (
            <ReadingSection title="The Observer Self (ACT)." eyebrow="Step 7" icon={Zap} theme={theme}>
              <p>For some, challenging thoughts feels like an endless argument. <Highlight description="Acceptance and Commitment Therapy (ACT) is a 'third-wave' CBT approach that focuses on changing your relationship to your thoughts, rather than the content of the thoughts themselves." theme={theme}>Acceptance and Commitment Therapy (ACT)</Highlight> offers an alternative: don't argue with the thought, just notice it and act anyway. This is called <Highlight description="The process of 'unhooking' from your thoughts, seeing them as just words passing through your mind, rather than objective truths or commands." theme={theme}>Cognitive Defusion</Highlight>.</p>
              <PassengersOnBus/>
            </ReadingSection>
          )}
          {activeSection === 7 && (
            <ReadingSection title="The Action Plan." eyebrow="Step 8" icon={Flag} theme={theme}>
              <p>You now have a complete toolkit of evidence-based psychological strategies to manage exam anxiety. You have the "software" (CBT & ACT) to go with the "hardware" optimization (sleep, nutrition) from other modules. Now it's about practice.</p>
              <MicroCommitment theme={theme}><p>Choose ONE tool from this module--the Thought Record, Downward Arrow, or an Exposure task. Commit to using it just once this week. You're not just studying; you're becoming your own therapist.</p></MicroCommitment>
            </ReadingSection>
          )}
        </>
      )}
    </ModuleLayout>
  );
};
export default CatastrophicThinkingModule;
