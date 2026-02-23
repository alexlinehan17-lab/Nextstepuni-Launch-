/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
*/

import React, { useState, useEffect } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import {
  Code, SlidersHorizontal, UserX, Recycle, Flag
} from 'lucide-react';
import { ModuleProgress } from '../types';
import { amberTheme } from '../moduleThemes';
import { Highlight, ReadingSection, MicroCommitment, PersonalStory } from './ModuleShared';
import { ModuleLayout } from './ModuleLayout';
import { useModuleResponses } from '../hooks/useModuleResponses';

const theme = amberTheme;

// --- INTERACTIVE COMPONENTS ---

const MotionDiv = motion.div as any;

const AttributionMapper = ({ savedValues, onSave }: { savedValues?: { locus: number; stability: number; controllability: number }; onSave?: (values: { locus: number; stability: number; controllability: number }) => void }) => {
  const [locus, setLocus] = useState(savedValues?.locus ?? 50);
  const [stability, setStability] = useState(savedValues?.stability ?? 50);
  const [controllability, setControllability] = useState(savedValues?.controllability ?? 50);

  useEffect(() => {
    if (savedValues) {
      setLocus(savedValues.locus);
      setStability(savedValues.stability);
      setControllability(savedValues.controllability);
    }
  }, [savedValues]);

  // Internal (high locus) + Unstable (low stability) + Controllable (low controllability) = growth
  // Optimism score: locus contributes positively when high, stability when low, controllability when low
  const optimismScore = (locus / 100) + (1 - stability / 100) + (1 - controllability / 100); // 0–3

  const getLabel = (): { text: string; color: string } => {
    if (optimismScore >= 2.2) return { text: 'Growth Attribution', color: 'emerald' };
    if (optimismScore <= 1.0) return { text: 'Helplessness Risk', color: 'rose' };
    return { text: 'Mixed', color: 'amber' };
  };

  const getExplanation = (): string => {
    const isInternal = locus >= 55;
    const isStable = stability >= 55;
    const isControllable = controllability <= 45;

    if (isInternal && !isStable && isControllable) {
      return "This is the ideal growth attribution. You take ownership, see it as temporary, and believe you can change it. This pattern fuels motivation and resilience.";
    }
    if (!isInternal && isStable && !isControllable) {
      return "You see this as someone else's fault, permanent, and out of your control. This is the classic pattern behind learned helplessness — it kills motivation because effort feels pointless.";
    }
    if (isInternal && isStable && !isControllable) {
      return "You see this as permanent and out of your control — this is the pattern that leads to learned helplessness. Try reframing: what specific strategy could you change?";
    }
    if (!isInternal && !isStable && isControllable) {
      return "You see this as external and temporary, but believe you can act on it. That's a resilient stance, though taking more ownership could help you grow even faster.";
    }
    if (isInternal && isStable && isControllable) {
      return "You take ownership and feel you can act, but seeing it as permanent may weigh you down. Try reframing: is this really forever, or just this situation?";
    }
    if (!isInternal && isStable && isControllable) {
      return "You see the cause as external and permanent but feel you can still act. Consider whether more ownership of the cause would give you a clearer path forward.";
    }
    if (!isInternal && !isStable && !isControllable) {
      return "You see this as external, temporary, and beyond your control. That can feel comforting, but look for the part you can influence — even small actions build agency.";
    }
    if (isInternal && !isStable && !isControllable) {
      return "You own the cause and see it as temporary, but feel powerless to change it. The missing piece is controllability — what one small lever could you pull?";
    }
    // Neutral / middle ground
    return "Your attribution sits in the middle ground. Try pushing the sliders to the extremes to see how different stories about failure lead to very different emotional outcomes.";
  };

  const label = getLabel();

  const labelBgClass = label.color === 'emerald'
    ? 'bg-emerald-100 dark:bg-emerald-900/40 text-emerald-700 dark:text-emerald-300'
    : label.color === 'rose'
    ? 'bg-rose-100 dark:bg-rose-900/40 text-rose-700 dark:text-rose-300'
    : 'bg-amber-100 dark:bg-amber-900/40 text-amber-700 dark:text-amber-300';

  const borderClass = label.color === 'emerald'
    ? 'border-emerald-200 dark:border-emerald-700'
    : label.color === 'rose'
    ? 'border-rose-200 dark:border-rose-700'
    : 'border-amber-200 dark:border-amber-700';

  const handleSliderChange = (dimension: 'locus' | 'stability' | 'controllability', value: number) => {
    const setters = { locus: setLocus, stability: setStability, controllability: setControllability };
    setters[dimension](value);
    const next = { locus, stability, controllability, [dimension]: value };
    onSave?.(next);
  };

  const sliders: { label: string; leftLabel: string; rightLabel: string; leftExample: string; rightExample: string; value: number; dimension: 'locus' | 'stability' | 'controllability' }[] = [
    {
      label: 'Locus',
      leftLabel: 'External',
      rightLabel: 'Internal',
      leftExample: '"The teacher marked unfairly"',
      rightExample: '"I didn\'t prepare well"',
      value: locus,
      dimension: 'locus',
    },
    {
      label: 'Stability',
      leftLabel: 'Unstable',
      rightLabel: 'Stable',
      leftExample: '"I had an off day"',
      rightExample: '"I\'m always like this"',
      value: stability,
      dimension: 'stability',
    },
    {
      label: 'Controllability',
      leftLabel: 'Controllable',
      rightLabel: 'Uncontrollable',
      leftExample: '"I can change my approach"',
      rightExample: '"There\'s nothing I can do"',
      value: controllability,
      dimension: 'controllability',
    },
  ];

  return (
    <div className="my-10 p-8 md:p-12 bg-white dark:bg-zinc-800 rounded-xl border border-zinc-200 dark:border-zinc-700">
      <h4 className="font-serif text-2xl font-semibold text-zinc-800 dark:text-white text-center">Attribution Mapper</h4>
      <p className="text-center text-sm text-zinc-500 dark:text-zinc-400 mt-2 mb-10">
        Think of a recent setback or bad result. Map how you interpreted it:
      </p>

      <div className="space-y-8">
        {sliders.map((s) => (
          <div key={s.label}>
            <p className="text-sm font-bold text-zinc-700 dark:text-zinc-200 mb-1 text-center">{s.label}</p>
            <div className="flex items-center gap-3">
              <div className="flex flex-col items-end w-28 shrink-0">
                <span className="text-xs font-semibold text-zinc-600 dark:text-zinc-300">{s.leftLabel}</span>
                <span className="text-[10px] text-zinc-400 dark:text-zinc-500 italic text-right">{s.leftExample}</span>
              </div>
              <input
                type="range"
                min={0}
                max={100}
                value={s.value}
                onChange={(e) => handleSliderChange(s.dimension, Number(e.target.value))}
                className="w-full"
              />
              <div className="flex flex-col items-start w-28 shrink-0">
                <span className="text-xs font-semibold text-zinc-600 dark:text-zinc-300">{s.rightLabel}</span>
                <span className="text-[10px] text-zinc-400 dark:text-zinc-500 italic text-left">{s.rightExample}</span>
              </div>
            </div>
          </div>
        ))}
      </div>

      <MotionDiv
        key={label.text}
        initial={{ opacity: 0, y: 8 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.35 }}
        className={`mt-10 p-6 rounded-xl border ${borderClass} text-center`}
      >
        <span className={`inline-block px-3 py-1 rounded-full text-xs font-bold uppercase tracking-wider ${labelBgClass}`}>
          {label.text}
        </span>
        <p className="mt-3 text-sm text-zinc-600 dark:text-zinc-300 leading-relaxed">
          {getExplanation()}
        </p>
      </MotionDiv>
    </div>
  );
};

const AttributionSorter = ({ savedChoices, onSave }: { savedChoices?: { [key: string]: boolean }; onSave?: (choices: { [key: string]: boolean }) => void }) => {
    const reasons = [
        { text: "I didn't use the right study method.", type: 'internal', control: true },
        { text: "I'm just naturally bad at this subject.", type: 'internal', control: false },
        { text: "The test was unfairly hard.", type: 'external', control: false },
        { text: "I didn't put in enough focused effort.", type: 'internal', control: true },
    ];
    const [choice, setChoice] = useState<{ [key: string]: boolean }>(savedChoices || {});

    useEffect(() => {
      if (savedChoices) setChoice(savedChoices);
    }, [savedChoices]);

    return(
        <div className="my-10 p-8 md:p-12 bg-white dark:bg-zinc-800 rounded-xl border border-zinc-200 dark:border-zinc-700">
            <h4 className="font-serif text-2xl font-semibold text-zinc-800 dark:text-white text-center">Control Panel</h4>
            <p className="text-center text-sm text-zinc-500 dark:text-zinc-400 mb-8">Scenario: You fail a test. Which of these reasons are actually within your control?</p>
            <div className="space-y-3">
                {reasons.map(reason => (
                    <button key={reason.text} onClick={() => { const next = {...choice, [reason.text]: !choice[reason.text]}; setChoice(next); onSave?.(next); }} className={`w-full p-4 rounded-xl border text-left font-bold text-sm transition-all ${choice[reason.text] ? (reason.control ? 'bg-emerald-50 border-emerald-300' : 'bg-rose-50 border-rose-300') : 'bg-zinc-50 border-zinc-200 dark:border-zinc-700 hover:bg-zinc-100 dark:hover:bg-zinc-700'}`}>
                        {reason.text}
                        {choice[reason.text] && <span className={`ml-2 font-semibold text-xs ${reason.control ? 'text-emerald-600' : 'text-rose-600'}`}>{reason.control ? '(CONTROLLABLE)' : '(UNCONTROLLABLE)'}</span>}
                    </button>
                ))}
            </div>
        </div>
    );
};

const AttributionReframeDrill = () => {
  const examples = [
    { id: 1, maladaptive: "I failed the test because I am stupid.", adaptive: "I failed the test because my study strategy for this topic was ineffective." },
    { id: 2, maladaptive: "I'm just naturally bad at Maths.", adaptive: "I haven't found an effective way to learn Maths *yet*." },
    { id: 3, maladaptive: "I'll never be good enough to get a H1.", adaptive: "Getting a H1 is a difficult goal, so I will need to break it down into smaller, manageable steps." },
  ];

  const [flipped, setFlipped] = useState<number[]>([]);

  const handleFlip = (id: number) => {
    setFlipped(
      flipped.includes(id)
        ? flipped.filter(fId => fId !== id)
        : [...flipped, id]
    );
  };

  return (
    <div className="my-10 p-8 md:p-10 bg-white dark:bg-zinc-900 rounded-xl border border-zinc-200 dark:border-zinc-800">
      <h4 className="font-serif text-2xl font-semibold text-zinc-900 dark:text-white text-center">Attribution Reframe Drill</h4>
      <p className="text-center text-sm text-zinc-500 dark:text-zinc-400 mb-8">Click on a self-defeating thought to transform it into an empowering one.</p>
      <div className="space-y-3">
        {examples.map((ex) => (
          <motion.div
            key={ex.id}
            onClick={() => handleFlip(ex.id)}
            className="p-6 rounded-xl cursor-pointer border relative min-h-[100px] flex items-center justify-center transition-colors"
            animate={{
              backgroundColor: flipped.includes(ex.id) ? 'rgba(236, 253, 245, 1)' : 'rgba(250, 250, 247, 1)',
              borderColor: flipped.includes(ex.id) ? 'rgb(167 243 208)' : 'rgb(229 228 223)'
            }}
          >
            <AnimatePresence mode="wait">
              <motion.p
                key={flipped.includes(ex.id) ? ex.adaptive : ex.maladaptive}
                initial={{ opacity: 0, y: 10 }}
                animate={{ opacity: 1, y: 0 }}
                exit={{ opacity: 0, y: -10 }}
                transition={{ duration: 0.3 }}
                className={`text-sm text-center font-medium ${flipped.includes(ex.id) ? 'text-emerald-800' : 'text-zinc-600 dark:text-zinc-400'}`}
              >
                "{flipped.includes(ex.id) ? ex.adaptive : ex.maladaptive}"
              </motion.p>
            </AnimatePresence>
            <p className="absolute bottom-2.5 right-4 text-[9px] font-medium tracking-wider text-zinc-300 dark:text-zinc-600 uppercase">
              {flipped.includes(ex.id) ? 'Reframed' : 'Tap to reframe'}
            </p>
          </motion.div>
        ))}
      </div>
    </div>
  );
};


// --- MODULE COMPONENT ---
const AgencyArchitectureModule: React.FC<{ onBack: () => void; progress: ModuleProgress; onProgressUpdate: (progress: ModuleProgress) => void }> = ({ onBack, progress, onProgressUpdate }) => {
  const { responses, saveResponse, isLoaded } = useModuleResponses('controlling-the-controllables');

  const sections = [
    { id: 'attribution-theory', title: 'The Story of Failure', eyebrow: '01 // The Source Code', icon: Code },
    { id: 'three-dimensions', title: 'The Three Dimensions', eyebrow: '02 // The Control Panel', icon: SlidersHorizontal },
    { id: 'pessimistic-script', title: 'The Pessimist\'s Script', eyebrow: '03 // Learned Helplessness', icon: UserX },
    { id: 'agency-rewrite', title: 'The Agency Re-Write', eyebrow: '04 // Retraining', icon: Recycle },
    { id: 'blueprint', title: 'Your New OS', eyebrow: '05 // The Blueprint', icon: Flag },
  ];

  return (
    <ModuleLayout
      moduleNumber="07"
      moduleTitle="Controlling the Controllables"
      moduleSubtitle="The Attribution Retraining Guide"
      moduleDescription="Learn to distinguish between what you can and cannot control, and rewire your brain to see failure as feedback, not a final verdict."
      theme={theme}
      sections={sections}
      onBack={onBack}
      progress={progress}
      onProgressUpdate={onProgressUpdate}
      finishButtonText="Take the Controls"
    >
      {(activeSection) => (
        <>
          {activeSection === 0 && (
            <ReadingSection title="The Story of Failure." eyebrow="Step 1" icon={Code} theme={theme}>
              <p>When something bad happens, your brain instantly writes a story to explain why. This story is called an <Highlight description="The story your brain tells you about why something happened. The kind of story you default to has a huge effect on how motivated and resilient you feel." theme={theme}>attribution</Highlight>. It's the "source code" for your motivation. A resilient mindset isn't about being positive; it's about telling yourself the right kind of story after a failure.</p>
              <p>The core principle is to focus on what you can control. This idea is called the <Highlight description="A simple but powerful idea: split everything in your life into two buckets — stuff you can actually control (your effort, your attitude) and stuff you can't (other people, external events). Then pour your energy into the first bucket." theme={theme}>Dichotomy of Control</Highlight>. The research is clear: students who focus their energy on what they can control, and let go of what they can't, are more resilient and academically successful.</p>
              <PersonalStory name="Alex" role="Founder, NextStepUni">
                <p>After I failed my Junior Cert, I had a long list of things I couldn't control. Where I grew up, the crowds I'd been in, the things that had happened. In 4th year I made a decision to stop looking at that list. I focused on the one thing I could control: how I studied. I read the academic papers, I built a system, and I worked it every day. That was the only variable I changed — and it changed everything.</p>
              </PersonalStory>
            </ReadingSection>
          )}
          {activeSection === 1 && (
            <ReadingSection title="The Three Dimensions." eyebrow="Step 2" icon={SlidersHorizontal} theme={theme}>
              <p>Every story you tell yourself about a failure can be broken down along three dimensions. <strong>1. Locus of Control:</strong> Is the cause <Highlight description="You're saying the cause is something about you — like how much effort you put in or how you prepared." theme={theme}>Internal</Highlight> (about you) or <Highlight description="You're saying the cause is something outside of you — like the teacher, the exam, or bad luck." theme={theme}>External</Highlight> (about the world)? <strong>2. Stability:</strong> Is the cause <Highlight description="You're saying this is permanent — it's always been this way and always will be. Like thinking 'I'm just not a maths person.'" theme={theme}>Stable</Highlight> (permanent) or <Highlight description="You're saying this is temporary — it happened this time but it's not a forever thing. Like thinking 'I didn't study enough for this specific test.'" theme={theme}>Unstable</Highlight> (temporary)? <strong>3. Controllability:</strong> Is the cause something you can change, or not?</p>
              <AttributionMapper savedValues={responses['attribution-mapper']} onSave={(v) => saveResponse('attribution-mapper', v)} />
              <AttributionSorter savedChoices={responses['attribution-sorter']} onSave={(c) => saveResponse('attribution-sorter', c)} />
            </ReadingSection>
          )}
          {activeSection === 2 && (
            <ReadingSection title="The Pessimist's Script." eyebrow="Step 3" icon={UserX} theme={theme}>
              <p>The most dangerous story your brain can write is the "pessimistic explanatory style." It attributes failure to causes that are <strong>Internal, Stable, and Uncontrollable</strong>. For example: "I failed the test (bad event) because I am stupid (Internal, Stable, Uncontrollable)."</p>
              <p>This kind of thinking is toxic. It leads straight to <Highlight description="When you've told yourself 'there's no point' so many times that you actually start to believe it. You stop trying — not because you're lazy, but because your brain has convinced itself that nothing you do will make a difference." theme={theme}>Learned Helplessness</Highlight>. If you believe the cause of your failure is a permanent, unchangeable part of who you are, then there's no point in trying again. Your motivation collapses, not because you're lazy, but because your brain has logically concluded that effort is futile.</p>
            </ReadingSection>
          )}
           {activeSection === 3 && (
            <ReadingSection title="The Agency Re-Write." eyebrow="Step 4" icon={Recycle} theme={theme}>
              <p>The good news is that you can consciously re-write this script. This is called <Highlight description="Basically, training yourself to change the story you tell about why things went wrong. Instead of jumping to 'I'm useless,' you learn to say 'my approach didn't work — what can I try differently?'" theme={theme}>Attributional Retraining</Highlight>. It genuinely works — students who practise this become more resilient and do better in their exams.</p>
              <p>The goal is to shift your explanations towards causes that are <strong>Internal, Unstable, and Controllable</strong>. "I failed the test because I am stupid" becomes "I failed the test because my *strategy* was ineffective." The cause is still internal (giving you agency), but it's unstable (you can change your strategy) and controllable. This isn't just wordplay; it's a fundamental shift in your brain's operating system that turns a dead end into a learning opportunity.</p>
              <AttributionReframeDrill />
            </ReadingSection>
          )}
           {activeSection === 4 && (
            <ReadingSection title="Your New OS." eyebrow="Step 5" icon={Flag} theme={theme}>
              <p>By practicing this "re-write," you are installing a new default operating system in your brain. You are training yourself to see setbacks not as verdicts, but as data points. This is the foundation of a Growth Mindset and the core of what it means to have agency over your own academic life.</p>
              <MicroCommitment theme={theme}>
                <p>The next time you face a small failure—any small failure—consciously run the 3D analysis. Ask yourself: "What story am I telling myself about why this happened?" Is it Internal/External? Stable/Unstable? Controllable/Uncontrollable? This act of noticing is the first step to rewriting the script.</p>
              </MicroCommitment>
            </ReadingSection>
          )}
        </>
      )}
    </ModuleLayout>
  );
};
export default AgencyArchitectureModule;
