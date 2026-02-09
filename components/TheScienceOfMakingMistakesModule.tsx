/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
*/

import React, { useState } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import {
  AlertTriangle, Lightbulb, ToggleRight, ZapOff, Wrench
} from 'lucide-react';
import { ModuleProgress } from '../types';
import { redTheme } from '../moduleThemes';
import { Highlight, ReadingSection, MicroCommitment } from './ModuleShared';
import { ModuleLayout } from './ModuleLayout';

const theme = redTheme;

// --- INTERACTIVE COMPONENTS ---
const BrainSignalVisualizer = () => {
    const [active, setActive] = useState(false);
    return(
        <div className="my-10 p-8 md:p-12 bg-white dark:bg-zinc-800 rounded-2xl border border-zinc-200 dark:border-zinc-700 shadow-xl">
             <h4 className="font-serif text-2xl font-semibold text-zinc-800 dark:text-white text-center italic">The Brain's Two Signals</h4>
             <p className="text-center text-sm text-zinc-500 dark:text-zinc-400 mb-8">When you make a mistake, your brain sends two distinct signals in less than half a second.</p>
             <div className="w-full max-w-lg mx-auto h-32 relative">
                <svg viewBox="0 0 300 100" className="w-full h-full absolute inset-0">
                    <path d="M0 50 L 300 50" stroke="#e5e7eb" strokeWidth="1" />
                    <AnimatePresence>
                    {active && <>
                        <motion.path initial={{pathLength:0}} animate={{pathLength:1}} transition={{duration:0.2, delay: 0.1}} d="M 50 50 C 60 50 65 20 75 20 S 90 50 100 50" stroke="#f43f5e" strokeWidth="2" fill="none" />
                        <motion.path initial={{pathLength:0}} animate={{pathLength:1}} transition={{duration:0.5, delay: 0.3}} d="M 150 50 C 160 50 175 80 190 80 S 210 50 220 50" stroke="#10b981" strokeWidth="2" fill="none" />
                    </>}
                    </AnimatePresence>
                </svg>
                {active && <>
                    <motion.div initial={{opacity:0}} animate={{opacity:1, transition:{delay:0.2}}} className="absolute top-0 left-[75px] -translate-x-1/2 text-center text-xs">
                        <p className="font-bold text-rose-600">ERN Signal</p>
                        <p className="text-zinc-500 dark:text-zinc-400">The "Alarm"</p>
                    </motion.div>
                    <motion.div initial={{opacity:0}} animate={{opacity:1, transition:{delay:0.5}}} className="absolute bottom-0 left-[190px] -translate-x-1/2 text-center text-xs">
                        <p className="font-bold text-emerald-600">Pe Signal</p>
                        <p className="text-zinc-500 dark:text-zinc-400">The "Analysis"</p>
                    </motion.div>
                </>}
             </div>
             <div className="text-center mt-8">
                <button onClick={() => setActive(!active)} className="px-5 py-3 bg-zinc-800 text-white font-bold rounded-lg text-sm">{active ? "Reset" : "Make a Mistake"}</button>
             </div>
        </div>
    );
};


// --- MODULE COMPONENT ---
const TheScienceOfMakingMistakesModule: React.FC<{ onBack: () => void; progress: ModuleProgress; onProgressUpdate: (progress: ModuleProgress) => void }> = ({ onBack, progress, onProgressUpdate }) => {
  const sections = [
    { id: 'brain-alarm', title: "The Brain's Alarm", eyebrow: '01 // The "Uh-Oh" Signal', icon: AlertTriangle },
    { id: 'second-signal', title: 'The Second Signal', eyebrow: '02 // The Analysis', icon: Lightbulb },
    { id: 'mindset-switch', title: 'The Mindset Switch', eyebrow: '03 // Leaning In', icon: ToggleRight },
    { id: 'high-stakes-hijack', title: 'The High-Stakes Hijack', eyebrow: '04 // The Leaving Cert Brain', icon: ZapOff },
    { id: 'error-toolkit', title: 'Your Error Toolkit', eyebrow: '05 // Rewiring Your Brain', icon: Wrench },
  ];

  return (
    <ModuleLayout
      moduleNumber="05"
      moduleTitle="The Science of Mistakes"
      theme={theme}
      sections={sections}
      onBack={onBack}
      progress={progress}
      onProgressUpdate={onProgressUpdate}
    >
      {(activeSection) => (
        <>
          {activeSection === 0 && (
            <ReadingSection title="The Brain's Alarm." eyebrow="Step 1" icon={AlertTriangle} theme={theme}>
              <p>When you make a mistake—a typo, a wrong turn in a maths problem—your brain registers it instantly. Before you are even consciously aware of it, an electrical signal called the <Highlight description="A neural signal of error detection that occurs within 50 milliseconds of a mistake. It is an unconscious 'uh-oh' signal originating from the anterior cingulate cortex." theme={theme}>Error-Related Negativity (ERN)</Highlight> fires. It's a super-fast, automatic "uh-oh" moment.</p>
              <p>Think of it as your brain's smoke detector. It's a primitive, unconscious alarm that goes off when your actions don't match your intentions. This signal is crucial, but it's not the part that drives learning. It's what happens next that separates high-performers from the rest.</p>
            </ReadingSection>
          )}
           {activeSection === 1 && (
            <ReadingSection title="The Second Signal." eyebrow="Step 2" icon={Lightbulb} theme={theme}>
              <p>About 200-500 milliseconds after the initial alarm, a second, larger brainwave can occur. This is the <Highlight description="A later neural signal (200-500ms post-error) that reflects conscious attention to and awareness of the mistake. The amplitude of the Pe wave is a strong predictor of post-error correction and learning." theme={theme}>Error Positivity (Pe)</Highlight> signal. This isn't automatic. This is the signal of your conscious brain paying attention to the mistake, analyzing it, and engaging with it. It's the moment your brain decides to learn from the error.</p>
              <p>You can think of it like this: the ERN is the smoke alarm beeping. The Pe is you getting out of bed to find the source of the smoke. The size of your Pe wave literally predicts how likely you are to correct the error and get it right next time. It's the neurobiological signature of giving a damn about your mistakes.</p>
              <BrainSignalVisualizer />
            </ReadingSection>
          )}
          {activeSection === 2 && (
            <ReadingSection title="The Mindset Switch." eyebrow="Step 3" icon={ToggleRight} theme={theme}>
              <p>Here's where it gets fascinating. Neuroscientists have shown that the size of your Pe wave is directly controlled by your mindset. Students with a <Highlight description="The belief that intelligence is a fixed trait. People with this mindset tend to see errors as a threat to their ego." theme={theme}>Fixed Mindset</Highlight> show a much smaller Pe signal. They hear the alarm, but they quickly "look away" from the mistake because it feels like a threat to their self-concept. If "being smart" is your identity, then a mistake is evidence that you're not.</p>
              <p>Students with a <Highlight description="The belief that intelligence can be grown through effort and strategy. They see errors as an opportunity to learn and improve." theme={theme}>Growth Mindset</Highlight> have a huge Pe signal. They lean into the mistake, allocating massive attentional resources to it. They understand that the error isn't a verdict on their ability; it's a crucial piece of data for improvement. They are hungry for the information contained within the failure.</p>
            </ReadingSection>
          )}
           {activeSection === 3 && (
            <ReadingSection title="The High-Stakes Hijack." eyebrow="Step 4" icon={ZapOff} theme={theme}>
                <p>This whole system can be hijacked by stress. In a high-stakes situation like the Leaving Cert, the fear of failure can trigger an <Highlight description="An intense emotional response that is out of proportion to the real threat, caused by the amygdala overriding the rational prefrontal cortex." theme={theme}>amygdala hijack</Highlight>. This floods your brain with stress hormones like cortisol.</p>
                <p>High cortisol levels do two terrible things. First, they impair the function of your prefrontal cortex, making it harder to think clearly. Second, they suppress the Pe signal. Your brain shifts from a "learning focus" to a "threat focus." It stops trying to analyse the mistake and starts trying to just survive the experience. This is why you can "go blank" after one mistake and find it impossible to recover.</p>
            </ReadingSection>
          )}
           {activeSection === 4 && (
            <ReadingSection title="Your Error Toolkit." eyebrow="Step 5" icon={Wrench} theme={theme}>
              <p>The good news is you can train your brain to have a bigger Pe signal and be more resilient under pressure. It's a skill. The first step is to **de-shame mistakes**. See them as data, not as judgments on your character. Every error is a signpost pointing to exactly where you need to grow.</p>
              <p>The most powerful tool for this is a <Highlight description="A dedicated notebook or document where you log every mistake you make in practice, diagnose its cause (e.g., slip, gap, misconception), and prescribe a specific action to fix it." theme={theme}>Mistake Log</Highlight>. This forces you to engage with your errors in a structured, analytical way. It's a manual override that forces your brain to generate a strong Pe signal. Don't just find your mistakes; interrogate them. They are your best teachers.</p>
               <MicroCommitment theme={theme}>
                <p>For your next piece of homework, actively look for one mistake you made. Don't just correct it. Write down in one sentence *why* you made it. You've just started your first mistake log.</p>
              </MicroCommitment>
            </ReadingSection>
          )}
        </>
      )}
    </ModuleLayout>
  );
};
export default TheScienceOfMakingMistakesModule;
