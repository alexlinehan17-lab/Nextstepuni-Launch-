/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
*/

import React, { useState } from 'react';
import { motion } from 'framer-motion';
import {
  BrainCircuit, Wrench, BookOpen, BarChart3, ClipboardCheck, ShieldCheck
} from 'lucide-react';
import { ModuleProgress } from '../types';
import { orangeTheme } from '../moduleThemes';
import { Highlight, ReadingSection, MicroCommitment } from './ModuleShared';
import { ModuleLayout } from './ModuleLayout';

const theme = orangeTheme;

// --- INTERACTIVE COMPONENTS ---
const JugglingStudyVisualizer = () => {
    const [scan, setScan] = useState(1);
    const data = [
        { scan: 1, value: 50, label: "Baseline" },
        { scan: 2, value: 80, label: "After 3 Months Practice" },
        { scan: 3, value: 60, label: "After 3 Months No Practice" },
    ];
    const currentData = data[scan-1];

    return (
        <div className="my-10 p-8 md:p-12 bg-white dark:bg-zinc-800 rounded-xl border border-zinc-200 dark:border-zinc-700">
             <h4 className="font-serif text-2xl font-semibold text-zinc-800 dark:text-white text-center">The Juggling Study (2004)</h4>
             <p className="text-center text-sm text-zinc-500 dark:text-zinc-400 mb-8">Proof that learning physically changes your brain's grey matter.</p>
             <div className="w-full max-w-xs mx-auto h-48 flex justify-center items-end">
                <motion.div
                    className="w-24 bg-orange-400 rounded-t-lg"
                    initial={{height: '50%'}}
                    animate={{height: `${currentData.value}%`}}
                    transition={{type: 'spring', damping: 15, stiffness: 100}}
                />
             </div>
             <p className="text-center font-bold mt-2">{currentData.label}</p>
             <div className="flex justify-center gap-2 mt-4">
                <button onClick={() => setScan(1)} className={`px-3 py-1 text-xs font-bold rounded-full ${scan===1 ? 'bg-orange-500 text-white' : 'bg-zinc-100'}`}>Scan 1</button>
                <button onClick={() => setScan(2)} className={`px-3 py-1 text-xs font-bold rounded-full ${scan===2 ? 'bg-orange-500 text-white' : 'bg-zinc-100'}`}>Scan 2</button>
                <button onClick={() => setScan(3)} className={`px-3 py-1 text-xs font-bold rounded-full ${scan===3 ? 'bg-orange-500 text-white' : 'bg-zinc-100'}`}>Scan 3</button>
             </div>
        </div>
    );
};

const StudyMethodGrader = () => {
    const [method, setMethod] = useState<'passive' | 'active' | null>(null);
    return(
        <div className="my-10 p-8 md:p-12 bg-white dark:bg-zinc-800 rounded-xl border border-zinc-200 dark:border-zinc-700">
            <h4 className="font-serif text-2xl font-semibold text-zinc-800 dark:text-white text-center">Study Method Grader</h4>
            <p className="text-center text-sm text-zinc-500 dark:text-zinc-400 mb-6">Which study method sends a stronger signal to build your brain?</p>
             <div className="grid grid-cols-2 gap-4">
                <button onClick={() => setMethod('passive')} className="p-4 bg-rose-50 border border-rose-200 rounded-xl text-center"><strong>Passive Re-reading:</strong> "I'll just read my notes again."</button>
                <button onClick={() => setMethod('active')} className="p-4 bg-emerald-50 border border-emerald-200 rounded-xl text-center"><strong>Active Recall:</strong> "I'll try to explain this from memory."</button>
             </div>
             {method &&
             <motion.div initial={{opacity:0}} animate={{opacity:1}} className="mt-6">
                <h5 className="font-bold text-center">Neuroplasticity Score:</h5>
                <div className="w-full h-8 bg-zinc-100 dark:bg-zinc-800 rounded-full mt-2 overflow-hidden">
                    <motion.div
                        className={`h-full rounded-full ${method === 'active' ? 'bg-emerald-500' : 'bg-rose-500'}`}
                        initial={{width: '0%'}}
                        animate={{width: method === 'active' ? '95%' : '20%'}}
                        transition={{duration: 1}}
                    />
                </div>
                <p className="text-xs text-center mt-2 text-zinc-500 dark:text-zinc-400">{method === 'active' ? 'High-fidelity signal sent. Brain rewiring initiated.' : 'Low-level signal. Minimal rewiring.'}</p>
             </motion.div>}
        </div>
    );
}

// --- MODULE COMPONENT ---
const NeuroplasticityProtocolModule: React.FC<{ onBack: () => void; progress: ModuleProgress; onProgressUpdate: (progress: ModuleProgress) => void }> = ({ onBack, progress, onProgressUpdate }) => {
  const sections = [
    { id: 'paradigm-shift', title: 'The Plastic Brain', eyebrow: '01 // The Paradigm Shift', icon: BrainCircuit },
    { id: 'brain-renovation', title: "The Brain's Renovation", eyebrow: '02 // Sculpt & Upgrade', icon: Wrench },
    { id: 'rulebook-of-learning', title: 'The Rulebook of Learning', eyebrow: '03 // Fire Together, Wire Together', icon: BookOpen },
    { id: 'physical-evidence', title: 'The Physical Evidence', eyebrow: '04 // The Juggling Study', icon: BarChart3 },
    { id: 'learning-blueprint', title: 'The Learning Blueprint', eyebrow: '05 // Neuro-Pedagogy', icon: ClipboardCheck },
    { id: 'system-maintenance', title: 'System Maintenance', eyebrow: '06 // Sleep & Stress', icon: ShieldCheck },
  ];

  return (
    <ModuleLayout
      moduleNumber="01"
      moduleTitle="Neuroplasticity Protocol"
      moduleSubtitle="Your Brain's User Manual"
      moduleDescription="Discover that your brain isn't fixed. Learn the science of how your brain physically changes when you study, and how to use this to your advantage."
      theme={theme}
      sections={sections}
      onBack={onBack}
      progress={progress}
      onProgressUpdate={onProgressUpdate}
    >
      {(activeSection) => (
        <>
          {activeSection === 0 && (
            <ReadingSection title="The Plastic Brain." eyebrow="Step 1" icon={BrainCircuit} theme={theme}>
              <p>For decades, scientists believed your brain was like concrete: it set early in life and couldn't be changed. You were born with a certain level of "smartness," and that was it. We now know this is completely wrong. Your brain is more like plasticine: it is constantly being reshaped by your experiences, thoughts, and actions.</p>
              <p>This ability to change is called <Highlight description="The brain's ability to modify its own structure and function in response to experience. It's the biological process that underpins all learning and skill acquisition." theme={theme}>Neuroplasticity</Highlight>. During your teenage years, your brain is more 'plastic' than at almost any other time in your life. It's a period of massive reorganization. Understanding how this process works isn't just interesting science; it's the user manual for your own brain.</p>
            </ReadingSection>
          )}
           {activeSection === 1 && (
            <ReadingSection title="The Brain's Renovation." eyebrow="Step 2" icon={Wrench} theme={theme}>
              <p>Your brain is undergoing two massive renovation projects at once. The first is <Highlight description="The process where the brain eliminates weak or unused synaptic connections. It's like a sculptor chipping away unnecessary stone to reveal the statue underneath. It makes the brain more efficient." theme={theme}>Synaptic Pruning</Highlight>. Your brain is like a gardener, trimming away the connections you don't use to free up resources for the ones you do. This is the "use it or lose it" principle in action. If you don't practice something, your brain physically dismantles the wiring for it.</p>
              <p>The second project is <Highlight description="The process of coating axons in a fatty sheath called myelin. This insulation makes nerve signals travel up to 100 times faster, allowing for quicker and more synchronized thinking." theme={theme}>Myelination</Highlight>. Think of this as upgrading a bumpy country road to a motorway. Your brain wraps insulation (myelin) around the neural pathways you use often, making them super-fast and efficient. Practice doesn't just make perfect; it makes *faster*.</p>
            </ReadingSection>
          )}
           {activeSection === 2 && (
            <ReadingSection title="The Rulebook of Learning." eyebrow="Step 3" icon={BookOpen} theme={theme}>
              <p>How does your brain know which connections to prune and which to myelinate? It follows a simple, powerful rule from 1949 known as <Highlight description="The foundational principle of neuroplasticity, often summarized as 'Cells that fire together, wire together.' It means that when two neurons are active at the same time, the connection between them gets stronger." theme={theme}>Hebbian Theory</Highlight>: "Cells that fire together, wire together." Every time you have a thought or practice a skill, you're sending an electrical signal through a chain of neurons. The more you fire that chain, the stronger the physical connections between those neurons become.</p>
              <p>We can think of this with two analogies. For strengthening connections, imagine a field of tall grass. The first time you walk across (study a topic once), you bend the grass, but it springs back. If you walk the same "Desire Path" repeatedly, you wear a permanent trail. For speed, think of an "Orchestra." To make music, different sections need their signals to arrive at the same time. Myelination is your brain's conductor, adjusting the speed of different pathways so your thoughts are perfectly timed and synchronized.</p>
            </ReadingSection>
          )}
          {activeSection === 3 && (
            <ReadingSection title="The Physical Evidence." eyebrow="Step 4" icon={BarChart3} theme={theme}>
              <p>This isn't just a theory; we can see it happen. In a landmark 2004 study, scientists took brain scans of people who had never juggled before. Then, they taught them to juggle and scanned their brains again after three months of practice. The result? A measurable, physical increase in the amount of grey matter in the parts of the brain responsible for tracking moving objects.</p>
              <p>But here's the crucial part: they then told the jugglers to stop practicing for three months. The final brain scan showed that those same areas of the brain had shrunk back down again. This is the "use it or lose it" principle in action. Your brain is an efficient machine; it will not waste energy maintaining a skill you aren't using. Your intelligence is not fixed; it is a dynamic landscape that you are actively shaping every day.</p>
              <JugglingStudyVisualizer />
            </ReadingSection>
          )}
          {activeSection === 4 && (
            <ReadingSection title="The Learning Blueprint." eyebrow="Step 5" icon={ClipboardCheck} theme={theme}>
                <p>This science gives us a blueprint for effective learning. It tells us *why* certain study techniques work and others don't. For example, <Highlight description="Reviewing material at increasing intervals (e.g., 1 day, 3 days, 1 week). This strategy works by reactivating neural pathways just as they begin to weaken, signaling to the brain that they are important and should be kept." theme={theme}>Spaced Repetition</Highlight> is powerful because it's the biological signal to "keep this connection" and "myelinate this pathway." Cramming, on the other hand, is like a single, intense stampede across the grass--it doesn't create a lasting path.</p>
                <p>Similarly, <Highlight description="Forcing your brain to retrieve information from scratch (e.g., using flashcards or practice tests) instead of passively re-reading it. This high-effort activity generates a much stronger 'fire together, wire together' signal." theme={theme}>Active Recall</Highlight> is far more effective than passive re-reading. Why? Because re-reading is a low-effort task that sends a weak signal. Active recall forces your brain to reconstruct the entire neural pathway from scratch, generating an intense "coincidence detection" signal that triggers powerful synaptic strengthening.</p>
                <StudyMethodGrader />
            </ReadingSection>
          )}
           {activeSection === 5 && (
            <ReadingSection title="System Maintenance." eyebrow="Step 6" icon={ShieldCheck} theme={theme}>
                <p>Finally, your brain's ability to change depends on how well you maintain it. Sleep isn't a luxury; it's the brain's cleaning and filing cycle. During deep sleep, your brain scales down the synaptic connections you made during the day, keeping the important ones and getting rid of the noise. Without enough sleep, your brain becomes saturated and "noisy," making it impossible to learn new things.</p>
                <p>Stress is the other enemy of plasticity. Chronic stress floods your brain with cortisol, a hormone that actively inhibits the growth of new connections and can even accelerate pruning in important areas like your memory centres. Managing stress isn't just for your mental health; it's a prerequisite for effective learning. By understanding these biological rules, you can stop working against your brain and start working with it.</p>
                <MicroCommitment theme={theme}>
                    <p>Tonight, put your phone away 30 minutes before you plan to sleep. This small act of "sleep hygiene" can have a huge impact on your brain's ability to consolidate what you learned today.</p>
                </MicroCommitment>
            </ReadingSection>
          )}
        </>
      )}
    </ModuleLayout>
  );
};
export default NeuroplasticityProtocolModule;
