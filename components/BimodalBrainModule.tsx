
/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
*/

import React, { useState } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import {
  Brain, SlidersHorizontal, Lightbulb, PauseCircle, Zap, Clock
} from 'lucide-react';
import { ModuleProgress } from '../types';
import { purpleTheme } from '../moduleThemes';
import { Highlight, ReadingSection, MicroCommitment } from './ModuleShared';
import { ModuleLayout } from './ModuleLayout';

const theme = purpleTheme;

// --- INTERACTIVE COMPONENTS ---

const PinballSimulator = () => {
    const [mode, setMode] = useState<'focused' | 'diffuse'>('focused');
    return(
        <div className="my-10 p-8 md:p-12 bg-white rounded-[3rem] border border-stone-200 shadow-xl">
             <h4 className="font-serif text-2xl font-semibold text-stone-800 text-center italic">The Pinball Metaphor</h4>
             <p className="text-center text-sm text-stone-500 mb-8">Toggle between modes to see how your thoughts travel.</p>
             <div className="w-full h-64 bg-stone-900 rounded-2xl p-4 relative overflow-hidden">
                <AnimatePresence>
                    {mode === 'focused' && [...Array(25)].map((_, i) => <motion.div key={`f${i}`} initial={{opacity:0, scale:0}} animate={{opacity:1, scale:1}} exit={{opacity:0, scale:0}} className="absolute w-4 h-4 bg-purple-400 rounded-full" style={{top: `${10 + Math.random()*80}%`, left: `${10 + Math.random()*80}%`}} />)}
                    {mode === 'diffuse' && [...Array(8)].map((_, i) => <motion.div key={`d${i}`} initial={{opacity:0, scale:0}} animate={{opacity:1, scale:1}} exit={{opacity:0, scale:0}} className="absolute w-4 h-4 bg-purple-400 rounded-full" style={{top: `${10 + Math.random()*80}%`, left: `${10 + Math.random()*80}%`}} />)}
                </AnimatePresence>
             </div>
             <div className="flex justify-center gap-4 mt-6">
                <button onClick={() => setMode('focused')} className="px-4 py-2 bg-purple-100 text-purple-800 rounded-lg">Focused Mode</button>
                <button onClick={() => setMode('diffuse')} className="px-4 py-2 bg-stone-100 text-stone-800 rounded-lg">Diffuse Mode</button>
             </div>
        </div>
    );
};

// --- MODULE COMPONENT ---
const BimodalBrainModule: React.FC<{ onBack: () => void; progress: ModuleProgress; onProgressUpdate: (progress: ModuleProgress) => void }> = ({ onBack, progress, onProgressUpdate }) => {
  const sections = [
    { id: 'two-modes', title: 'The Two Modes of Thinking', eyebrow: '01 // The Discovery', icon: Brain },
    { id: 'focused-engine', title: 'The Focused Engine', eyebrow: '02 // Deep Work', icon: Zap },
    { id: 'diffuse-network', title: 'The Diffuse Network', eyebrow: '03 // Creative Insights', icon: Lightbulb },
    { id: 'toggling', title: 'Toggling the Switch', eyebrow: '04 // The Art of the Break', icon: PauseCircle },
    { id: 'procrastination-link', title: 'The Procrastination Link', eyebrow: '05 // Why We Delay', icon: Clock },
    { id: 'blueprint', title: 'The Bimodal Blueprint', eyebrow: '06 // Your Action Plan', icon: SlidersHorizontal },
  ];

  return (
    <ModuleLayout
      moduleNumber="09"
      moduleTitle="The Bimodal Brain"
      theme={theme}
      sections={sections}
      onBack={onBack}
      progress={progress}
      onProgressUpdate={onProgressUpdate}
    >
      {(activeSection) => (
        <>
          {activeSection === 0 && (
            <ReadingSection title="The Two Modes of Thinking." eyebrow="Step 1" icon={Brain} theme={theme}>
              <p>Your brain doesn't have just one mode of thinking; it has two, fundamentally different systems. The <Highlight description="A state of high-attention, analytical thought. It's what you use for solving familiar problems and executing procedures." theme={theme}>Focused Mode</Highlight> is your analytical workhorse. It's a state of intense concentration, perfect for solving a maths problem you already know how to do. The <Highlight description="A relaxed, low-attention state where your brain makes broad connections. It's the source of creative insights and 'Aha!' moments." theme={theme}>Diffuse Mode</Highlight> is your creative wanderer. It's a state of relaxed mind-wandering that allows your brain to make surprising new connections.</p>
            </ReadingSection>
          )}
          {activeSection === 1 && (
            <ReadingSection title="The Focused Engine." eyebrow="Step 2" icon={Zap} theme={theme}>
                <p>The Focused Mode is like a pinball machine with tightly packed bumpers. Your thoughts bounce around in a small, localized area, working through the details of a problem you understand. This is essential for procedural fluency in subjects like Maths and Chemistry. It's the mode you're in during a Pomodoro sprint. However, if you get stuck on a new or difficult problem, this mode can be a trap. Your thoughts just keep hitting the same bumpers, leading to frustration.</p>
                <PinballSimulator />
            </ReadingSection>
          )}
          {activeSection === 2 && (
             <ReadingSection title="The Diffuse Network." eyebrow="Step 3" icon={Lightbulb} theme={theme}>
                <p>The Diffuse Mode is when the bumpers are far apart. Your thoughts can travel long distances across your brain, connecting ideas from different subjects and experiences. This is where your 'Aha!' moments come from. You can't force this mode; you can only create the conditions for it to emerge. This happens when you relax your focus—by taking a walk, having a shower, or even just staring out the window.</p>
            </ReadingSection>
          )}
          {activeSection === 3 && (
             <ReadingSection title="Toggling the Switch." eyebrow="Step 4" icon={PauseCircle} theme={theme}>
                <p>The key to effective learning and problem-solving is learning to switch between these two modes. Work intensely in Focused Mode on a hard problem. When you get stuck, deliberately switch to Diffuse Mode by taking a break. Your brain will continue to work on the problem in the background (the <Highlight description="The subconscious processing of a problem that occurs when you are not actively thinking about it." theme={theme}>Incubation Effect</Highlight>). When you return to the problem, the solution will often seem obvious.</p>
                <MicroCommitment theme={theme}><p>The next time you're stuck on a homework problem, don't just push harder. Get up and walk around for 5 minutes. You're not giving up; you're using a different part of your brain.</p></MicroCommitment>
            </ReadingSection>
          )}
          {activeSection === 4 && (
            <ReadingSection title="The Procrastination Link." eyebrow="Step 5" icon={Clock} theme={theme}>
                <p>Procrastination is often caused by the discomfort of entering Focused Mode for a difficult task. The solution is to use a "Diffuse Mode warm-up." Instead of trying to force yourself into a 60-minute focused session, just commit to 5 minutes. This lowers the initial barrier and allows you to ease into the task. The pain of starting is always worse than the pain of continuing.</p>
            </ReadingSection>
          )}
          {activeSection === 5 && (
             <ReadingSection title="The Bimodal Blueprint." eyebrow="Step 6" icon={SlidersHorizontal} theme={theme}>
                <p>You now have the user manual for your brain's two gears. The strategic implication is clear: your study schedule must include both focused work *and* scheduled, unstructured breaks. This is not a luxury; it's a neurobiological necessity for deep learning and creativity.</p>
            </ReadingSection>
          )}
        </>
      )}
    </ModuleLayout>
  );
};
export default BimodalBrainModule;
