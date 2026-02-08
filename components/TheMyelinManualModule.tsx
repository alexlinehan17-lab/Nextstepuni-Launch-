
/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
*/

import React, { useState } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import {
  Cpu, Zap, SlidersHorizontal, Microscope, Construction
} from 'lucide-react';
import { ModuleProgress } from '../types';
import { amberTheme } from '../moduleThemes';
import { Highlight, ReadingSection, MicroCommitment } from './ModuleShared';
import { ModuleLayout } from './ModuleLayout';

const theme = amberTheme;

// --- INTERACTIVE COMPONENTS ---
const MyelinWrapper = () => {
    const [wraps, setWraps] = useState(0);
    const maxWraps = 10;
    const speed = 10 + (wraps * 9); // Speed from 10 to 100

    return (
        <div className="my-10 p-8 md:p-12 bg-white rounded-[3rem] border border-stone-200 shadow-xl">
            <h4 className="font-serif text-2xl font-semibold text-stone-800 text-center italic">The Myelin Wrapper</h4>
            <p className="text-center text-sm text-stone-500 mb-8">Each time you practice a skill, you add a layer of myelin, making the signal faster.</p>
            <div className="flex justify-center items-center h-24">
                <div className="relative w-64 h-2 bg-stone-200 rounded-full">
                     <div className="absolute inset-0 flex items-center">
                        <motion.div
                            className="w-full h-2 bg-blue-300 rounded-full"
                            style={{
                                height: 2 + wraps * 2,
                                y: '-50%',
                                top: '50%',
                            }}
                            transition={{type: 'spring', damping: 10, stiffness: 100}}
                        >
                            <div className="absolute -left-3 top-1/2 -translate-y-1/2 w-4 h-4 bg-amber-400 rounded-full" />
                        </motion.div>
                     </div>
                </div>
            </div>
             <div className="flex justify-center items-center gap-6 mt-8">
                <button onClick={() => setWraps(w => Math.min(w + 1, maxWraps))} className="px-5 py-3 bg-amber-500 text-white font-bold rounded-lg shadow-lg hover:bg-amber-600 transition-colors text-sm">Practice Skill</button>
                <div className="text-center">
                    <p className="font-mono text-2xl font-bold">{speed} <span className="text-sm">m/s</span></p>
                    <p className="text-xs font-bold uppercase tracking-widest text-stone-400">Signal Speed</p>
                </div>
                 <button onClick={() => setWraps(0)} className="text-xs text-stone-400">Reset</button>
             </div>
        </div>
    )
}

const DeepPracticeSorter = () => {
    const activities = [
        { name: "Highlighting notes", type: "naive" },
        { name: "Doing a past paper (timed)", type: "deep" },
        { name: "Watching a video", type: "naive" },
        { name: "Explaining a concept out loud", type: "deep" },
    ];
    const [choice, setChoice] = useState<{[key: string]: 'naive' | 'deep' | null}>({});

    return (
        <div className="my-10 p-8 md:p-12 bg-white rounded-[3rem] border border-stone-200 shadow-xl">
            <h4 className="font-serif text-2xl font-semibold text-stone-800 text-center italic">Deep vs. Naive Practice</h4>
            <p className="text-center text-sm text-stone-500 mb-8">Which of these activities trigger myelin growth?</p>
            <div className="space-y-4">
                {activities.map(act => (
                    <div key={act.name} className="p-4 bg-stone-50 border border-stone-200 rounded-lg flex justify-between items-center">
                        <span className="font-bold text-sm">{act.name}</span>
                        <div className="flex gap-2">
                           <button onClick={() => setChoice({...choice, [act.name]:'naive'})} className={`px-2 py-1 text-xs font-bold rounded ${choice[act.name] === 'naive' && act.type === 'naive' ? 'bg-emerald-200 text-emerald-800' : choice[act.name] === 'naive' && act.type === 'deep' ? 'bg-rose-200 text-rose-800' : 'bg-stone-200'}`}>Naive</button>
                           <button onClick={() => setChoice({...choice, [act.name]:'deep'})} className={`px-2 py-1 text-xs font-bold rounded ${choice[act.name] === 'deep' && act.type === 'deep' ? 'bg-emerald-200 text-emerald-800' : choice[act.name] === 'deep' && act.type === 'naive' ? 'bg-rose-200 text-rose-800' : 'bg-stone-200'}`}>Deep</button>
                        </div>
                    </div>
                ))}
            </div>
        </div>
    )
};


// --- MODULE COMPONENT ---
const TheMyelinManualModule: React.FC<{ onBack: () => void; progress: ModuleProgress; onProgressUpdate: (progress: ModuleProgress) => void }> = ({ onBack, progress, onProgressUpdate }) => {
  const sections = [
    { id: 'silent-revolution', title: 'The Silent Revolution', eyebrow: '01 // The Other Brain', icon: Cpu },
    { id: 'signal-of-struggle', title: 'The Signal of Struggle', eyebrow: '02 // The Chemical Trigger', icon: Zap },
    { id: 'deep-practice', title: 'Deep Practice', eyebrow: '03 // The Behavioural Trigger', icon: SlidersHorizontal },
    { id: 'myelin-metaphors', title: 'The Mastery Metaphors', eyebrow: '04 // The Mental Models', icon: Microscope },
    { id: 'rules-of-myelination', title: 'The Rules of Myelination', eyebrow: '05 // The Action Plan', icon: Construction },
  ];

  return (
    <ModuleLayout
      moduleNumber="02"
      moduleTitle="The Myelin Manual"
      theme={theme}
      sections={sections}
      onBack={onBack}
      progress={progress}
      onProgressUpdate={onProgressUpdate}
    >
      {(activeSection) => (
        <>
          {activeSection === 0 && (
            <ReadingSection title="The Silent Revolution." eyebrow="Step 1" icon={Cpu} theme={theme}>
              <p>In the last module, we learned that your brain physically changes when you learn. Now, we're zooming in on the secret to mastering a skill and making it automatic. It's not just about strengthening the connections *between* brain cells (synapses). It's about upgrading the connections *themselves*.</p>
              <p>Meet the unsung hero of your brain: the <Highlight description="A type of glial cell that produces myelin. Think of them as the expert electricians of your brain, responsible for insulating the wiring." theme={theme}>Oligodendrocyte</Highlight>. These cells are part of your 'other brain'—the glial cells—and their job is to wrap your neural circuits in a fatty insulation called <Highlight description="A lipid-rich substance that wraps around axons, acting like the plastic coating on an electrical wire. It prevents signal leakage and dramatically speeds up transmission." theme={theme}>Myelin</Highlight>. This process turns your brain's bumpy dirt roads into super-fast motorways. This isn't just about knowledge; it's about speed, precision, and automaticity.</p>
            </ReadingSection>
          )}
           {activeSection === 1 && (
            <ReadingSection title="The Signal of Struggle." eyebrow="Step 2" icon={Zap} theme={theme}>
                <p>How does this electrician know which wire to insulate? It listens for a specific signal. When you engage in intense, focused effort—like trying to solve a tough maths problem—your neurons fire at a very high frequency. This intense firing isn't a silent event. It causes the neuron to release chemical signals, like ATP and Glutamate, along its entire length.</p>
                <p>These chemicals are like a frantic call to the oligodendrocyte, screaming, "This circuit is important! It's being used intensely! We need an upgrade!" The feeling of <Highlight description="From a neurobiological perspective, 'struggle' is the behavioural state that generates the high-frequency neural firing necessary to trigger activity-dependent myelination." theme={theme}>struggle</Highlight> is not a sign you're failing; it's the physical sensation of your brain sending the order to build a better, faster circuit.</p>
            </ReadingSection>
          )}
          {activeSection === 2 && (
            <ReadingSection title="Deep Practice." eyebrow="Step 3" icon={SlidersHorizontal} theme={theme}>
              <p>The specific behavior that sends this "upgrade" signal is called <Highlight description="Popularized by Daniel Coyle, it's a method of practicing that involves intense focus, operating at the edge of your ability, embracing errors, and repeating the process. It is the direct trigger for myelination." theme={theme}>Deep Practice</Highlight>. It's the opposite of passively re-reading your notes. Naive practice is easy and feels productive, but it sends a weak, background signal that doesn't trigger myelination. It creates an "illusion of competence."</p>
              <p>Deep practice is hard, uncomfortable, and full of errors. It involves things like doing past papers without notes, forcing yourself to retrieve information from scratch, and pushing yourself just outside your comfort zone. That discomfort is the signal. It's the "heavy lifting" that tells your brain to build more muscle—or in this case, more myelin.</p>
              <DeepPracticeSorter />
            </ReadingSection>
          )}
          {activeSection === 3 && (
            <ReadingSection title="The Mastery Metaphors." eyebrow="Step 4" icon={Microscope} theme={theme}>
              <p>To really get a grip on this, we can use a few powerful analogies for what's happening inside your head when you engage in Deep Practice.</p>
              <p>Think of it as upgrading your home internet from dial-up to fibre optic **broadband**. Unmyelinated circuits are slow and have low bandwidth—they can only handle one simple idea at a time. A myelinated circuit can handle multiple complex ideas at once without "buffering." Or think of it as paving a **dirt road into a motorway**. The first time you learn something, it's slow and bumpy. With deep practice, you pave that road, allowing information to travel at high speed, automatically.</p>
              <MyelinWrapper/>
            </ReadingSection>
          )}
           {activeSection === 4 && (
            <ReadingSection title="The Rules of Myelination." eyebrow="Step 5" icon={Construction} theme={theme}>
                <p>Myelination follows a few simple, non-negotiable rules. First, **struggle is not optional**. Easy practice doesn't send the signal. You must operate in the "sweet spot" where you're making errors and correcting them. That error-correction loop is the sound of the construction crew getting to work.</p>
                <p>Second, **it's permanent but slow**. Unlike short-term memory, myelin is robust. Once a skill is wrapped, it stays with you. This is why cramming (synaptic) fails for long-term retention, but deep practice (myelin) works. But it takes time—weeks of consistent practice. You can't build a motorway overnight. Every session of deep practice adds another thin layer of tape, another ring to the tree.</p>
                <MicroCommitment theme={theme}>
                    <p>Identify your "sweet spot" for one subject. What is a task that is not too easy (you get it all right) and not too hard (you get it all wrong)? That's your target zone for the next study session.</p>
                </MicroCommitment>
            </ReadingSection>
          )}
        </>
      )}
    </ModuleLayout>
  );
};
export default TheMyelinManualModule;
