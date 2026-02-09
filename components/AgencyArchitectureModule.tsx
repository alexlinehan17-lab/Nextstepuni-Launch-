/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
*/

import React, { useState } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import {
  Code, SlidersHorizontal, UserX, Recycle, Flag, RotateCcw
} from 'lucide-react';
import { ModuleProgress } from '../types';
import { amberTheme } from '../moduleThemes';
import { Highlight, ReadingSection, MicroCommitment } from './ModuleShared';
import { ModuleLayout } from './ModuleLayout';

const theme = amberTheme;

// --- INTERACTIVE COMPONENTS ---

const AttributionSorter = () => {
    const reasons = [
        { text: "I didn't use the right study method.", type: 'internal', control: true },
        { text: "I'm just naturally bad at this subject.", type: 'internal', control: false },
        { text: "The test was unfairly hard.", type: 'external', control: false },
        { text: "I didn't put in enough focused effort.", type: 'internal', control: true },
    ];
    const [choice, setChoice] = useState<{ [key: string]: boolean }>({});

    return(
        <div className="my-10 p-8 md:p-12 bg-white dark:bg-zinc-800 rounded-2xl border border-zinc-200 dark:border-zinc-700 shadow-xl">
            <h4 className="font-serif text-2xl font-semibold text-zinc-800 dark:text-white text-center italic">Control Panel</h4>
            <p className="text-center text-sm text-zinc-500 dark:text-zinc-400 mb-8">Scenario: You fail a test. Which of these reasons are actually within your control?</p>
            <div className="space-y-3">
                {reasons.map(reason => (
                    <button key={reason.text} onClick={() => setChoice({...choice, [reason.text]: !choice[reason.text]})} className={`w-full p-4 rounded-xl border-2 text-left font-bold text-sm transition-all ${choice[reason.text] ? (reason.control ? 'bg-emerald-50 border-emerald-300' : 'bg-rose-50 border-rose-300') : 'bg-zinc-50 border-zinc-200 dark:border-zinc-700 hover:bg-zinc-100 dark:hover:bg-zinc-700'}`}>
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
    <div className="my-10 p-8 md:p-12 bg-white dark:bg-zinc-800 rounded-2xl border border-zinc-200 dark:border-zinc-700 shadow-xl">
      <h4 className="font-serif text-2xl font-semibold text-zinc-800 dark:text-white text-center italic">Attribution Reframe Drill</h4>
      <p className="text-center text-sm text-zinc-500 dark:text-zinc-400 mb-8">Click on a self-defeating thought to transform it into an empowering one.</p>
      <div className="space-y-4">
        {examples.map((ex) => (
          <motion.div
            key={ex.id}
            onClick={() => handleFlip(ex.id)}
            className="p-6 rounded-2xl cursor-pointer border-2 border-dashed relative min-h-[100px] flex items-center justify-center"
            animate={{
              backgroundColor: flipped.includes(ex.id) ? 'rgba(236, 253, 245, 1)' : 'rgba(254, 242, 242, 1)',
              borderColor: flipped.includes(ex.id) ? 'rgb(110 231 183)' : 'rgb(254 202 202)'
            }}
          >
            <AnimatePresence mode="wait">
              <motion.p
                key={flipped.includes(ex.id) ? ex.adaptive : ex.maladaptive}
                initial={{ opacity: 0, y: 10 }}
                animate={{ opacity: 1, y: 0 }}
                exit={{ opacity: 0, y: -10 }}
                transition={{ duration: 0.3 }}
                className={`font-mono text-sm text-center ${flipped.includes(ex.id) ? 'text-emerald-800' : 'text-rose-800'}`}
              >
                "{flipped.includes(ex.id) ? ex.adaptive : ex.maladaptive}"
              </motion.p>
            </AnimatePresence>
             <div className="absolute bottom-2 right-3 text-zinc-300 flex items-center gap-1 text-[9px] font-bold">
              <RotateCcw size={10} />
              REFRAME
            </div>
          </motion.div>
        ))}
      </div>
    </div>
  );
};


// --- MODULE COMPONENT ---
const AgencyArchitectureModule: React.FC<{ onBack: () => void; progress: ModuleProgress; onProgressUpdate: (progress: ModuleProgress) => void }> = ({ onBack, progress, onProgressUpdate }) => {
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
      theme={theme}
      sections={sections}
      onBack={onBack}
      progress={progress}
      onProgressUpdate={onProgressUpdate}
    >
      {(activeSection) => (
        <>
          {activeSection === 0 && (
            <ReadingSection title="The Story of Failure." eyebrow="Step 1" icon={Code} theme={theme}>
              <p>When something bad happens, your brain instantly writes a story to explain why. This story is called an <Highlight description="A concept from social psychology referring to the causal explanations people generate for events. Your attributional style is a powerful predictor of your resilience and motivation." theme={theme}>attribution</Highlight>. It's the "source code" for your motivation. A resilient mindset isn't about being positive; it's about telling yourself the right kind of story after a failure.</p>
              <p>The core principle is to focus on what you can control. The Stoic philosophers called this the <Highlight description="The ancient Stoic principle of dividing the world into things you can control (your thoughts, your actions) and things you cannot (external events, other people's opinions)." theme={theme}>Dichotomy of Control</Highlight>. The research is clear: students who focus their energy on what they can control, and let go of what they can't, are more resilient and academically successful.</p>
            </ReadingSection>
          )}
          {activeSection === 1 && (
            <ReadingSection title="The Three Dimensions." eyebrow="Step 2" icon={SlidersHorizontal} theme={theme}>
              <p>Every story you tell yourself about a failure can be broken down along three dimensions. <strong>1. Locus of Control:</strong> Is the cause <Highlight description="Attributing an outcome to something about yourself (e.g., your effort, your ability)." theme={theme}>Internal</Highlight> (about you) or <Highlight description="Attributing an outcome to something outside of yourself (e.g., the teacher, the situation)." theme={theme}>External</Highlight> (about the world)? <strong>2. Stability:</strong> Is the cause <Highlight description="A cause that is perceived as permanent and unchangeable (e.g., 'I'm just not a maths person')." theme={theme}>Stable</Highlight> (permanent) or <Highlight description="A cause that is perceived as temporary and changeable (e.g., 'I didn't study enough for this specific test')." theme={theme}>Unstable</Highlight> (temporary)? <strong>3. Controllability:</strong> Is the cause something you can change, or not?</p>
              <AttributionSorter/>
            </ReadingSection>
          )}
          {activeSection === 2 && (
            <ReadingSection title="The Pessimist's Script." eyebrow="Step 3" icon={UserX} theme={theme}>
              <p>The most dangerous story your brain can write is the "pessimistic explanatory style." It attributes failure to causes that are **Internal, Stable, and Uncontrollable**. For example: "I failed the test (bad event) because I am stupid (Internal, Stable, Uncontrollable)."</p>
              <p>This is a psychological poison. It leads directly to a state of <Highlight description="A psychological state where a person feels powerless to change their situation, leading to passivity and giving up. It's the end-point of a pessimistic explanatory style." theme={theme}>Learned Helplessness</Highlight>. If you believe the cause of your failure is a permanent, unchangeable part of who you are, then there's no point in trying again. Your motivation collapses, not because you're lazy, but because your brain has logically concluded that effort is futile.</p>
            </ReadingSection>
          )}
           {activeSection === 3 && (
            <ReadingSection title="The Agency Re-Write." eyebrow="Step 4" icon={Recycle} theme={theme}>
              <p>The good news is that you can consciously re-write this script. This is called <Highlight description="A cognitive-behavioral technique where individuals are explicitly taught to change their attributions for failure from internal, stable, and uncontrollable causes to external or internal, unstable, and controllable ones." theme={theme}>Attributional Retraining</Highlight>. It's a proven psychological intervention that builds resilience and improves academic performance.</p>
              <p>The goal is to shift your explanations towards causes that are **Internal, Unstable, and Controllable**. "I failed the test because I am stupid" becomes "I failed the test because my *strategy* was ineffective." The cause is still internal (giving you agency), but it's unstable (you can change your strategy) and controllable. This isn't just wordplay; it's a fundamental shift in your brain's operating system that turns a dead end into a learning opportunity.</p>
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
