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
import React,{ useId,useState } from 'react';
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
import { AnswerLine,ExerciseLabel,ExerciseRange,ExerciseSheet } from './learning/Exercise';
import { Button,TextButton } from './ui/Button';
import { AreaField,Field } from './ui/Field';

const theme = slateTheme;

// --- INTERACTIVE COMPONENTS ---

const ThoughtRecord = () => {
    const draft = usePrivateDeviceDraft('thought-record', { step: 0, record: { situation: '', emotion: '', intensity: 90, nat: '', evidenceFor: '', evidenceAgainst: '', alternative: '', reRate: 50 } });
    const { step, record } = draft.value;
    const setStep = (value: React.SetStateAction<number>) => draft.update(previous => ({ ...previous, step: typeof value === 'function' ? value(previous.step) : value }));
    const update = (field: string, value: string | number) => draft.update(previous => ({ ...previous, record: { ...previous.record, [field]: value } }));

    const steps = ['Situation', 'Emotion', 'Negative Thought', 'Evidence For', 'Evidence Against', 'Alternative', 'Re-Rate'];
    const intensityId = useId();
    const reRateId = useId();

    return (
        <ExerciseSheet title="The Thought Record" name="ThoughtRecord">
             <PrivateDraftControls title="My thought record" retain={draft.retain} setRetain={draft.setRetain} onClear={draft.clear} error={draft.error} text={Object.entries(record).map(([key, value]) => `${key}: ${value}`).join('\n')} />
             {/* How far through the record: a hairline track, an ink fill */}
             <div className="w-full h-1 rounded-full" style={{ background: 'var(--hairline)' }}><motion.div className="h-1 rounded-full" style={{ background: 'var(--ink-primary)' }} animate={{width: `${(step / (steps.length - 1)) * 100}%`}}/></div>
             <AnimatePresence mode="wait">
             <motion.div key={step} initial={{opacity:0, x:20}} animate={{opacity:1, x:0}} exit={{opacity:0, x:-20}} >
                {step === 0 && <Field label="1. Situation:" value={record.situation} onChange={e => update('situation', e.target.value)} placeholder="e.g., Sitting down to study History" />}
                {step === 1 && <div className="ex-stack"><Field label="2. Emotion:" value={record.emotion} onChange={e => update('emotion', e.target.value)} placeholder="e.g., Panic" /><div className="ex-slider"><p id={intensityId} className="ex-slider-name">Intensity: {record.intensity}%</p><ExerciseRange value={record.intensity} onChange={e => update('intensity', e.target.value)} aria-labelledby={intensityId} /></div></div>}
                {step === 2 && <AreaField label="3. Negative Automatic Thought (NAT):" rows={3} value={record.nat} onChange={e => update('nat', e.target.value)} placeholder="e.g., I'll never remember all these dates." />}
                {step === 3 && <AreaField label="4. Evidence For:" rows={3} value={record.evidenceFor} onChange={e => update('evidenceFor', e.target.value)} placeholder="e.g., I got some dates wrong on last week's test." />}
                {step === 4 && <AreaField label="5. Evidence Against:" rows={3} value={record.evidenceAgainst} onChange={e => update('evidenceAgainst', e.target.value)} placeholder="e.g., I passed my last test. I have 3 months to study." />}
                {step === 5 && <AreaField label="6. Alternative Thought:" rows={3} value={record.alternative} onChange={e => update('alternative', e.target.value)} placeholder="e.g., History is hard, but if I use flashcards I can pass." />}
                {step === 6 && <div className="ex-stack"><p className="ex-slider-name">7. Re-Rate Emotion:</p>{record.alternative && <div className="ex-thought"><ExerciseLabel>Your Alternative Thought</ExerciseLabel><p className="ex-quote">{record.alternative}</p></div>}<p className="t-sub">Initial Panic: <b className="text-ink-primary">{record.intensity}%</b></p><div className="ex-slider"><p id={reRateId} className="ex-slider-name">New Panic Level: <b>{record.reRate}%</b></p><ExerciseRange value={record.reRate} onChange={e => update('reRate', e.target.value)} aria-labelledby={reRateId} /></div>{Number(record.reRate) < Number(record.intensity) && <AnswerLine tone="note">You rated this feeling {Number(record.intensity) - Number(record.reRate)} points lower. Notice what helped; there is no required result.</AnswerLine>}</div>}
             </motion.div>
             </AnimatePresence>
             <div className="flex justify-between items-center">
                <TextButton tone="quiet" onClick={() => setStep(s=>Math.max(0,s-1))} {...{ disabled: step===0 }}>Prev</TextButton>
                <Button size="sm" onClick={() => setStep(s=>Math.min(steps.length-1,s+1))} {...{ disabled: step===steps.length-1 }}>Next</Button>
             </div>
        </ExerciseSheet>
    );
};

const GradedExposureHierarchy = () => {
    const [items, setItems] = useState([
        { id: 1, text: "Open Maths book (10 mins)", suds: 20 },
        { id: 2, text: "Read one past question", suds: 50 },
        { id: 3, text: "Attempt one question (timed)", suds: 80 },
    ]);
    return(
        <ExerciseSheet title="Exposure Hierarchy Builder" name="GradedExposureHierarchy">
             {/* A sorter: each step is a box you drag (a line, no shadow) */}
             <Reorder.Group axis="y" values={items} onReorder={setItems} className="ex-cards">
                {items.map(item => (
                    <Reorder.Item key={item.id} value={item} className="flex justify-between items-center gap-3 min-h-[56px] cursor-grab active:cursor-grabbing t-body text-ink-primary" style={{ backgroundColor: "var(--surface-paper)", border: "1px solid var(--outline-soft)", borderRadius: 'var(--r-ctl)', padding: '13px 14px 13px 16px', boxShadow: 'none' }} whileDrag={{ scale: 1.03, y: -2, boxShadow: 'none' }}>
                        <span>{item.text}</span>
                        <span className="ui-readout shrink-0 text-ink-secondary">{item.suds} SUDS</span>
                    </Reorder.Item>
                ))}
             </Reorder.Group>
        </ExerciseSheet>
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
    const barWidth = allAcknowledged ? 100 : Math.max(5, Math.round(100 - (shoutingCount / Math.max(1, totalCount)) * 100));
    // The bar is ink; it turns the success green only when every passenger is acknowledged (done).
    const barFill = allAcknowledged ? 'var(--success-hex)' : 'var(--ink-primary)';

    return (
         <ExerciseSheet title="Passengers on the Bus" sub={<>You're driving toward your goal. Negative thoughts are passengers shouting at you.<span className="block mt-1">You can't kick them off. But you can choose how to respond.</span></>} name="PassengersOnBus">
            {/* Speed indicator: on the sheet, a hairline track and an ink fill */}
            <div className="flex flex-col gap-2">
              <div className="flex justify-between items-baseline gap-3">
                <ExerciseLabel>Progress Toward Your Goal</ExerciseLabel>
                <p className="t-sub text-ink-primary">{speed}</p>
              </div>
              <div className="w-full h-2 rounded-full overflow-hidden" style={{ background: 'var(--hairline)' }}>
                <motion.div
                  className="h-full rounded-full"
                  style={{ background: barFill }}
                  animate={{ width: `${barWidth}%` }}
                  transition={{ type: 'spring', damping: 15, stiffness: 80 }}
                />
              </div>
            </div>

            {/* Passengers: ruled like rows on the sheet, each with its two buttons */}
            <div className="ex-list">
              <AnimatePresence>
                {passengers.map(p => (
                  <motion.div
                    key={p.id}
                    initial={{ opacity: 0, y: -10, scale: 0.95 }}
                    animate={{ opacity: 1, y: 0, scale: 1 }}
                    exit={{ opacity: 0, scale: 0.9 }}
                    transition={{ duration: 0.3 }}
                  >
                   <div className="flex items-center justify-between gap-3">
                    <div className="flex-1 min-w-0">
                      <p className={`t-body ${
                        p.state === 'shouting'
                          ? "text-ink-primary"
                          : "text-ink-muted line-through"
                      }`}>
                        {p.state === 'shouting' && (
                          <span
                            className="inline-block w-2 h-2 rounded-full mr-2 align-middle"
                            style={{ background: 'var(--ink-primary)' }}
                            aria-hidden="true"
                          />
                        )}
                        "{p.text}"
                      </p>
                      {p.state === 'acknowledged' && (
                        <p className="t-meta mt-1">Still here. No longer in control.</p>
                      )}
                    </div>
                    {p.state === 'shouting' && (
                      <div className="flex gap-2 shrink-0">
                        <Button
                          size="sm"
                          onClick={() => handleArgue(p.id)}
                        >
                          Argue
                        </Button>
                        <Button
                          size="sm"
                          onClick={() => handleAcknowledge(p.id)}
                        >
                          Acknowledge
                        </Button>
                      </div>
                    )}
                   </div>
                  </motion.div>
                ))}
              </AnimatePresence>
            </div>

            {/* Feedback */}
            {argued > 0 && shoutingCount > 3 && (
              <motion.div
                initial={{ opacity: 0 }}
                animate={{ opacity: 1 }}
              >
                <AnswerLine tone="note">
                Notice: arguing created {passengers.length - 3} new thought{passengers.length - 3 > 1 ? 's' : ''}. Fighting thoughts makes them multiply.
                </AnswerLine>
              </motion.div>
            )}

            {allAcknowledged && (
              <motion.div
                initial={{ opacity: 0, y: 8 }}
                animate={{ opacity: 1, y: 0 }}
              >
                <AnswerLine>
                The passengers are still on the bus — but you're driving. That's defusion.
                </AnswerLine>
              </motion.div>
            )}

            <div className="ex-actions">
              <TextButton
                tone="quiet"
                onClick={handleReset}
              >
                Reset
              </TextButton>
            </div>
        </ExerciseSheet>
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
  const chainId = useId();

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
    <ExerciseSheet title="The Downward Arrow" sub={'Follow the fear to its end. Ask "And then what?" until the catastrophe dissolves.'} name="DownwardArrowDrill">
      <div className="flex flex-col">
        {entries.map((entry, index) => {
          const labelId = `${chainId}-level-${index}`;
          return (
            <React.Fragment key={index}>
              {/* Connector between steps: a hairline and an ink chevron */}
              {index > 0 && (
                <MotionDiv
                  initial={{ opacity: 0, y: -8 }}
                  animate={{ opacity: 1, y: 0 }}
                  transition={{ duration: 0.4, delay: 0.1 }}
                  className="ex-connector my-2"
                >
                  <i aria-hidden="true" />
                  <svg width="16" height="10" viewBox="0 0 16 10" fill="none" aria-hidden="true">
                    <path d="M1 1L8 8L15 1" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"/>
                  </svg>
                </MotionDiv>
              )}

              {/* Each step on the sheet under its label (no box of its own) */}
              <MotionDiv
                initial={{ opacity: 0, y: 16, scale: 0.95 }}
                animate={{ opacity: 1, y: 0, scale: 1 }}
                transition={{ duration: 0.4, delay: index * 0.1 }}
                className="w-full"
              >
                <div className="flex flex-col gap-2">
                  <p id={labelId} className="ex-label">
                    {index === 0 ? 'The exam thought that scares you most' : `Level ${index + 1}: And then what?`}
                  </p>

                  {committed[index] ? (
                    <p className="ex-quote">"{entry}"</p>
                  ) : (
                    <div className="flex flex-col gap-3">
                      <Field
                        type="text"
                        aria-labelledby={labelId}
                        value={entry}
                        onChange={e => handleChange(index, e.target.value)}
                        onKeyDown={e => handleKeyDown(e, index)}
                        placeholder={index === 0 ? "I'll fail my exam" : "If that happened, then..."}
                      />
                      <Button
                        className="self-end"
                        onClick={() => handleNext(index)}
                        {...{ disabled: !entry.trim() }}
                      >
                        {index + 1 < CHAIN_LENGTH ? 'And then what happens?' : 'See the full chain'}
                      </Button>
                    </div>
                  )}
                </div>
              </MotionDiv>
            </React.Fragment>
          );
        })}
      </div>

      {/* Reflection — catastrophe dissolved: under a hairline, its label, the chain as numbered lines */}
      <AnimatePresence>
        {showReflection && (
          <MotionDiv
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            exit={{ opacity: 0, y: 20 }}
            transition={{ duration: 0.5, delay: 0.2 }}
          >
            <div className="ex-block">
              <p className="ex-label">Catastrophe Dissolved</p>

              <ol className="flex flex-col gap-2 my-2">
                {entries.filter((_, i) => committed[i]).map((entry, index) => (
                  <li key={index} className="flex items-center gap-3">
                    <span className="ex-badge">{index + 1}</span>
                    <p className="t-body text-ink-primary">{entry}</p>
                  </li>
                ))}
              </ol>

              <p className="ex-block-text">Is your final answer really as catastrophic as the first one felt?</p>
              <p className="t-body text-ink-primary">Most catastrophic chains end somewhere manageable. The fear lives in the ambiguity — not the reality.</p>
            </div>
          </MotionDiv>
        )}
      </AnimatePresence>

      {/* Reset */}
      {currentStep > 0 && (
        <div className="ex-actions">
          <TextButton tone="quiet" onClick={handleReset}>
            Start Over
          </TextButton>
        </div>
      )}
    </ExerciseSheet>
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
