
/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
*/

import React, { useState } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import {
  Battery, Brain, Moon, Coffee, HeartPulse, SlidersHorizontal
} from 'lucide-react';
import { ModuleProgress } from '../types';
import { orangeTheme } from '../moduleThemes';
import { Highlight, ReadingSection, MicroCommitment } from './ModuleShared';
import { ModuleLayout } from './ModuleLayout';

const theme = orangeTheme;

// --- INTERACTIVE COMPONENTS ---

const AllostaticLoadVisualizer = () => {
    return (
        <div className="my-10 p-8 md:p-12 bg-white dark:bg-zinc-800 rounded-2xl border border-zinc-200 dark:border-zinc-700 shadow-xl">
             <h4 className="font-serif text-2xl font-semibold text-zinc-800 dark:text-white text-center italic">The Leaving Cert Allostatic Load</h4>
             <p className="text-center text-sm text-zinc-500 dark:text-zinc-400 mb-8">Your brain's "wear and tear" isn't constant. It builds over time and spikes during exam clusters.</p>
             <div className="w-full h-40 bg-zinc-50 dark:bg-zinc-800/50 rounded-lg p-4">
                <svg viewBox="0 0 500 100" className="w-full h-full" preserveAspectRatio="none">
                    <path d="M 0 90 C 100 80, 200 60, 300 50 L 400 40 L 410 20 L 420 40 L 430 30 L 440 10 L 450 35 L 500 30" fill="none" stroke="#f97316" strokeWidth="3" />
                    <text x="50" y="95" fontSize="10" className="fill-zinc-400">5th Year</text>
                    <text x="350" y="95" fontSize="10" className="fill-zinc-400">6th Year</text>
                    <text x="450" y="95" fontSize="10" className="fill-rose-500 font-bold">Exams</text>
                </svg>
             </div>
        </div>
    );
};

const SleepCycleArchitect = () => {
    const [sleepHours, setSleepHours] = useState(8);
    const remLost = Math.max(0, (8 - sleepHours) * 25); // Rough calc
    return (
        <div className="my-10 p-8 md:p-12 bg-white dark:bg-zinc-800 rounded-2xl border border-zinc-200 dark:border-zinc-700 shadow-xl">
            <h4 className="font-serif text-2xl font-semibold text-zinc-800 dark:text-white text-center italic">The Sleep Cycle Architect</h4>
            <p className="text-center text-sm text-zinc-500 dark:text-zinc-400 mb-8">Use the slider to see what happens when you cut sleep short. Notice what gets cut first.</p>
            <div className="h-24 w-full bg-zinc-100 dark:bg-zinc-800 rounded-lg flex">
                <div className="h-full bg-slate-400" style={{width: `${(sleepHours/9)*100}%`}}>
                    {/* Cycles */}
                    <div className="h-full w-full flex">
                        {[...Array(5)].map((_, i) => (
                            <div key={i} className={`h-full border-r border-white/20 relative ${i*2 > sleepHours ? 'opacity-20' : ''}`} style={{width: '20%'}}>
                                <div className="absolute bottom-0 w-full h-1/2 bg-blue-400" />
                                <div className="absolute bottom-1/2 w-full h-1/4 bg-sky-300" />
                            </div>
                        ))}
                    </div>
                </div>
            </div>
            <input type="range" min="4" max="9" step="0.5" value={sleepHours} onChange={e => setSleepHours(parseFloat(e.target.value))} className="w-full mt-4" />
            <div className="text-center font-bold mt-2">{sleepHours.toFixed(1)} hours of sleep</div>
            <AnimatePresence>
            {remLost > 0 &&
                <motion.div initial={{opacity:0}} animate={{opacity:1}} className="mt-4 p-4 bg-rose-50 border border-rose-200 rounded-xl text-center text-sm">
                   You've lost approximately <span className="font-bold text-rose-600">{remLost}%</span> of your critical REM sleep, impairing problem-solving and emotional regulation.
                </motion.div>
            }
            </AnimatePresence>
        </div>
    );
};

// --- MODULE COMPONENT ---
const CognitiveEnduranceModule: React.FC<{ onBack: () => void; progress: ModuleProgress; onProgressUpdate: (progress: ModuleProgress) => void }> = ({ onBack, progress, onProgressUpdate }) => {
  const sections = [
    { id: 'marathon-mindset', title: 'The Marathon Mindset', eyebrow: '01 // The Construct', icon: Brain },
    { id: 'sleep-banking', title: 'The Sleep Banking Strategy', eyebrow: '02 // The Non-Negotiable', icon: Moon },
    { id: 'fueling-engine', title: 'Fueling the Engine', eyebrow: '03 // Nutrition & Hydration', icon: Coffee },
    { id: 'in-exam-tools', title: 'The In-Exam Toolkit', eyebrow: '04 // Psychological Protocols', icon: HeartPulse },
    { id: 'training-plan', title: 'The Training Plan', eyebrow: '05 // Progressive Overload', icon: SlidersHorizontal },
    { id: 'recovery-protocol', title: 'The Recovery Protocol', eyebrow: '06 // Active Recovery', icon: Battery },
  ];

  return (
    <ModuleLayout
      moduleNumber="10"
      moduleTitle="Cognitive Endurance"
      theme={theme}
      sections={sections}
      onBack={onBack}
      progress={progress}
      onProgressUpdate={onProgressUpdate}
    >
      {(activeSection) => (
        <>
          {activeSection === 0 && (
            <ReadingSection title="The Marathon Mindset." eyebrow="Step 1" icon={Brain} theme={theme}>
              <p>The Leaving Cert isn't a sprint; it's a marathon. Success isn't just about knowing the material. It's about being able to access that knowledge at 4 PM on a Friday after a brutal week of exams. This is <Highlight description="The ability to sustain high-level mental performance, maintain focus, and resist distraction over extended periods of effortful thinking." theme={theme}>Cognitive Endurance</Highlight>.</p>
              <p>It's a biological skill, not a measure of willpower. Your brain is an organ that consumes 20% of your body's energy. Under the chronic stress of the Leaving Cert, your brain accumulates "wear and tear"—a concept scientists call <Highlight description="The cumulative physiological 'wear and tear' on the body and brain that results from chronic stress. High allostatic load impairs PFC function and emotional regulation." theme={theme}>Allostatic Load</Highlight>. Building cognitive endurance is about training your brain to handle this load.</p>
              <AllostaticLoadVisualizer />
            </ReadingSection>
          )}
           {activeSection === 1 && (
            <ReadingSection title="The Sleep Banking Strategy." eyebrow="Step 2" icon={Moon} theme={theme}>
              <p>Sleep is the single most powerful tool for building endurance. It's not rest; it's when your brain consolidates memory and clears out metabolic waste like <Highlight description="A metabolic byproduct that accumulates in the brain during waking hours. It binds to receptors and inhibits neural activity, creating the feeling of 'sleep pressure' or 'brain fog'." theme={theme}>adenosine</Highlight>.</p>
              <p>As a teenager, your brain has a natural "phase delay," meaning you want to sleep late and wake up late. The exam schedule fights this. Crucially, the final hours of your sleep are dense with <Highlight description="Rapid Eye Movement sleep is critical for consolidating procedural (skill) memory and for emotional regulation. It is disproportionately lost when you wake up early." theme={theme}>REM Sleep</Highlight>, which is vital for problem-solving skills and emotional stability. Cutting sleep short is like skipping the most important part of your training.</p>
              <SleepCycleArchitect />
              <MicroCommitment theme={theme}><p>For the next 10 days, wake up at the same time every single day—even weekends. This 'Fixed Wake-Up' protocol is the fastest way to reset your body clock and align your peak alertness with exam time.</p></MicroCommitment>
            </ReadingSection>
          )}
          {activeSection === 2 && (
            <ReadingSection title="Fueling the Engine." eyebrow="Step 3" icon={Coffee} theme={theme}>
              <p>Your brain runs on glucose. An unstable fuel supply leads to unstable focus. High-sugar snacks cause a spike-and-crash cycle called <Highlight description="A state of low blood sugar that occurs 60-90 minutes after a high-sugar meal. It manifests as brain fog, irritability, and a loss of willpower, often coinciding with the middle of an exam." theme={theme}>Reactive Hypoglycemia</Highlight>, sabotaging your performance mid-exam.</p>
              <p>A cutting-edge hack from sports science is the <Highlight description="The finding that merely rinsing the mouth with a carbohydrate solution (without swallowing) can trick the brain into reducing the perception of fatigue and increasing neural drive." theme={theme}>Carbohydrate Mouth Rinse</Highlight>. Swishing a sports drink for 10 seconds activates reward centres in the brain, tricking it into thinking fuel is on the way. This can provide a vital mental boost in the final, gruelling hour of a long exam.</p>
            </ReadingSection>
          )}
           {activeSection === 3 && (
            <ReadingSection title="The In-Exam Toolkit." eyebrow="Step 4" icon={HeartPulse} theme={theme}>
                <p>Anxiety is the enemy of endurance. It hijacks your brain, diverting blood flow from your rational <Highlight description="The 'CEO' of your brain, responsible for executive functions like working memory and impulse control. Its function is severely impaired by stress and fatigue." theme={theme}>Prefrontal Cortex (PFC)</Highlight> to your emotional <Highlight description="The brain's primitive fear centre. When it becomes overactive, it can 'hijack' the PFC, leading to a 'blanking out' phenomenon." theme={theme}>amygdala</Highlight>. You need tools to manage this in real-time.</p>
                <p>The fastest way to calm your nervous system is the <Highlight description="A specific breathing pattern (two sharp inhales through the nose, one long exhale through the mouth) that reinflates collapsed air sacs in the lungs, rapidly offloading carbon dioxide and reducing autonomic arousal." theme={theme}>Physiological Sigh</Highlight>. It takes less than 10 seconds. When you feel panic rising after a tough question, this is your emergency brake.</p>
                <p>For your eyes, use the **20-20-20 Rule**: every 20 minutes, look at something 20 feet away for 20 seconds. This relaxes your eye muscles and fights the visual fatigue that causes headaches and slows reading speed.</p>
            </ReadingSection>
          )}
           {activeSection === 4 && (
            <ReadingSection title="The Training Plan." eyebrow="Step 5" icon={SlidersHorizontal} theme={theme}>
              <p>You can't train for a marathon by only running sprints. Likewise, you can't prepare for a 3-hour exam by only studying in 20-minute bursts. You need to train your focus using <Highlight description="The core principle of all training. To improve, you must gradually increase the duration, intensity, or difficulty of the task over time." theme={theme}>Progressive Overload</Highlight>.</p>
              <p>This means structuring your study in phases. Start with short, focused bursts (like the Pomodoro Technique) to build your base. Then, gradually increase the duration of your focus blocks, training your brain to push past the "boredom barrier." In the final weeks, you should be doing full "Simulation Blocks"—studying under exam conditions for 90-120 minutes straight. This is not about learning more content; it's about building mental muscle.</p>
            </ReadingSection>
          )}
           {activeSection === 5 && (
            <ReadingSection title="The Recovery Protocol." eyebrow="Step 6" icon={Battery} theme={theme}>
              <p>Recovery is not the absence of work; it's an active process. Lying on the couch scrolling through TikTok is not rest. It's <Highlight description="Low-quality rest that involves high-dopamine, high-input cognitive load (e.g., social media). It fragments attention and prevents true neural recovery." theme={theme}>Passive Recovery</Highlight>, and it can actually increase your cognitive fatigue.</p>
              <p><Highlight description="High-quality rest that involves low cognitive load and specific physiological benefits. Examples include light exercise, time in nature, and NSDR." theme={theme}>Active Recovery</Highlight> strategies are far superior. A 20-minute walk clears stress hormones. Even better is <Highlight description="Non-Sleep Deep Rest (NSDR) is a guided meditation technique that brings the brain into a state of deep relaxation while maintaining consciousness. It rapidly replenishes dopamine and reduces cortisol." theme={theme}>NSDR</Highlight>, a 10-20 minute guided relaxation that acts as a "system reset" for your brain. In the crucial break between two exams on the same day, a 20-minute NSDR session is the single most effective way to restore your cognitive endurance for the afternoon paper.</p>
              <MicroCommitment theme={theme}><p>Find a 10-minute NSDR or Yoga Nidra script on YouTube. Try it once this week instead of scrolling on your phone during a study break.</p></MicroCommitment>
            </ReadingSection>
          )}
        </>
      )}
    </ModuleLayout>
  );
};
export default CognitiveEnduranceModule;
