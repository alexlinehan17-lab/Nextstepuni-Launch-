/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
*/

import React, { useState } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import {
  Cpu, Brain, Heart, Zap, Shield, Utensils, ClipboardCheck
} from 'lucide-react';
import { ModuleProgress } from '../types';
import { cyanTheme } from '../moduleThemes';
import { Highlight, ReadingSection, MicroCommitment } from './ModuleShared';
import { ModuleLayout } from './ModuleLayout';

const theme = cyanTheme;

// --- INTERACTIVE COMPONENTS ---
const PFCShutdownSimulator = () => {
    const [stress, setStress] = useState(false);
    return (
        <div className="my-10 p-8 md:p-12 bg-white dark:bg-zinc-800 rounded-2xl border border-zinc-200 dark:border-zinc-700 shadow-xl text-center">
             <h4 className="font-serif text-2xl font-semibold text-zinc-800 dark:text-white text-center italic">PFC Shutdown Simulator</h4>
             <p className="text-sm text-zinc-500 dark:text-zinc-400 mb-6">Click to see what happens when your Amygdala hijacks your brain.</p>
             <div className="flex justify-center items-center gap-4">
                <motion.div animate={{opacity: stress ? 1: 0.3}} className="text-center"><Zap size={48} className="text-rose-500 mx-auto"/><p className="font-bold">Amygdala</p></motion.div>
                <motion.div className="w-24 h-1 bg-zinc-300" animate={{backgroundColor: stress ? '#ef4444' : '#3b82f6'}} />
                <motion.div animate={{opacity: stress ? 0.3: 1}} className="text-center"><Brain size={48} className="text-blue-500 mx-auto"/><p className="font-bold">PFC</p></motion.div>
             </div>
             <button onClick={() => setStress(!stress)} className="mt-6 px-4 py-2 bg-rose-500 text-white font-bold text-sm rounded-lg">{stress ? 'De-escalate' : 'Trigger Stress'}</button>
        </div>
    );
}

const ArousalReappraisal = () => {
    return (
        <div className="my-10 p-8 md:p-12 bg-white dark:bg-zinc-800 rounded-2xl border border-zinc-200 dark:border-zinc-700 shadow-xl">
             <h4 className="font-serif text-2xl font-semibold text-zinc-800 dark:text-white text-center italic">Arousal Reappraisal</h4>
             <div className="relative h-48 w-full">
                <div className="absolute top-4 left-4 p-3 bg-rose-100 text-rose-800 rounded-lg font-bold">Anxiety</div>
                <div className="absolute top-4 right-4 p-3 bg-emerald-100 text-emerald-800 rounded-lg font-bold">Excitement</div>
                <div className="absolute bottom-4 left-1/2 -translate-x-1/2 p-3 bg-blue-100 text-blue-800 rounded-lg font-bold">Calm</div>
                <svg className="w-full h-full" viewBox="0 0 200 100">
                    <path d="M 20 10 H 180" stroke="#f59e0b" strokeWidth="2"/>
                    <path d="M 20 10 Q 100 120 180 10" stroke="#ef4444" strokeWidth="2" strokeDasharray="4"/>
                </svg>
             </div>
             <p className="text-center text-sm text-zinc-500 dark:text-zinc-400">It's easier to shift valence (Anxiety &#8594; Excitement) than to change arousal state (Anxiety &#8594; Calm).</p>
        </div>
    );
};

const BoxBreathing = () => (
     <div className="my-10 p-8 md:p-12 bg-white dark:bg-zinc-800 rounded-2xl border border-zinc-200 dark:border-zinc-700 shadow-xl text-center">
         <h4 className="font-serif text-2xl font-semibold text-zinc-800 dark:text-white text-center italic">Box Breathing</h4>
         <div className="w-24 h-24 mx-auto my-6 relative">
             <motion.div className="w-full h-full border-4 border-cyan-300 rounded-lg" animate={{rotate: 360}} transition={{duration: 16, repeat: Infinity, ease: 'linear'}}/>
             <motion.div className="absolute w-4 h-4 bg-cyan-500 rounded-full" style={{top: -8, left:'50%', x:'-50%'}} animate={{offsetDistance: "100%"}} transition={{duration: 16, repeat: Infinity, ease: 'linear'}}/>
         </div>
         <p className="text-sm font-bold">Inhale (4s) - Hold (4s) - Exhale (4s) - Hold (4s)</p>
    </div>
);

// --- MODULE COMPONENT ---
const EmotionalIntelligenceModule: React.FC<{ onBack: () => void; progress: ModuleProgress; onProgressUpdate: (progress: ModuleProgress) => void }> = ({ onBack, progress, onProgressUpdate }) => {
  const sections = [
    { id: 'neurobiology-stress', title: 'The Neurobiology of Stress', eyebrow: '01 // The Hardware', icon: Cpu },
    { id: 'emotional-intelligence', title: 'What is Emotional Intelligence?', eyebrow: '02 // The Software', icon: Brain },
    { id: 'self-awareness', title: 'Building Self-Awareness', eyebrow: '03 // Somatic Literacy', icon: Heart },
    { id: 'cognitive-regulation', title: 'Cognitive Regulation (Top-Down)', eyebrow: '04 // The Mind', icon: Zap },
    { id: 'physiological-regulation', title: 'Physiological Regulation (Bottom-Up)', eyebrow: '05 // The Body', icon: Shield },
    { id: 'bio-support', title: 'The Bio-Support System', eyebrow: '06 // Fuel & Maintenance', icon: Utensils },
    { id: 'integrated-timeline', title: 'The Integrated Timeline', eyebrow: '07 // The Plan', icon: ClipboardCheck },
  ];

  return (
    <ModuleLayout
      moduleNumber="13"
      moduleTitle="Emotional Intelligence"
      theme={theme}
      sections={sections}
      onBack={onBack}
      progress={progress}
      onProgressUpdate={onProgressUpdate}
    >
      {(activeSection) => (
        <>
          {activeSection === 0 && (
            <ReadingSection title="The Neurobiology of Stress." eyebrow="Step 1" icon={Cpu} theme={theme}>
              <p>Exam stress isn't a character flaw; it's a predictable neuroendocrine response. Your brain's alarm system, the <Highlight description="The Hypothalamic-Pituitary-Adrenal axis is the body's central stress response system. When a threat is perceived, it releases a cascade of hormones, culminating in cortisol." theme={theme}>HPA Axis</Highlight>, floods your system with cortisol. In the short term, this is good--it sharpens focus. But the Leaving Cert is a chronic stressor.</p>
              <p>Under chronic stress, high levels of cortisol effectively take your <Highlight description="The 'CEO' of your brain, responsible for planning, logic, and working memory. It is the last part of the brain to fully mature, making it vulnerable during adolescence." theme={theme}>Prefrontal Cortex (PFC)</Highlight> "offline." This is the biological reason for "going blank." Your brain has prioritized survival over cognition. Understanding this isn't an excuse; it's the first step to taking back control.</p>
              <PFCShutdownSimulator />
            </ReadingSection>
          )}
          {activeSection === 1 && (
            <ReadingSection title="What is Emotional Intelligence?" eyebrow="Step 2" icon={Brain} theme={theme}>
              <p><Highlight description="The capacity to be aware of, control, and express one's emotions, and to handle interpersonal relationships judiciously and empathetically." theme={theme}>Emotional Intelligence (EI)</Highlight> isn't about being "nice." In an academic context, it's a set of high-level cognitive skills for monitoring and regulating your internal state. High EI doesn't mean you don't feel stress; it means you can use that stress as fuel (<Highlight description="A positive, motivating form of stress that can improve performance." theme={theme}>eustress</Highlight>) instead of letting it become a debilitating force.</p>
              <p>For the Leaving Cert, we can break EI into three trainable skills: 1) **Emotional Awareness:** Noticing the physical signals of stress early. 2) **Emotional Understanding:** Correctly labeling the emotion. 3) **Emotional Regulation:** Using specific strategies to manage it.</p>
            </ReadingSection>
          )}
          {activeSection === 2 && (
            <ReadingSection title="Building Self-Awareness." eyebrow="Step 3" icon={Heart} theme={theme}>
              <p>You can't manage what you don't measure. The first step is to develop <Highlight description="The ability to read your body's internal physical signals, such as heart rate, breathing, and muscle tension." theme={theme}>Somatic Literacy</Highlight>. Your body often registers stress before your conscious mind does. These physical signals are called <Highlight description="Physical sensations (e.g., racing heart, tight stomach) that act as early warning signs for an emotional response." theme={theme}>Somatic Markers</Highlight>.</p>
              <p>A simple daily "Body Scan" can train your ability to notice these markers. By checking in with your body, you can catch the stress response early, before it cascades into a full-blown panic attack. It's about moving from "I'm freaking out" to "I am noticing the sensation of a rapid heartbeat."</p>
            </ReadingSection>
          )}
          {activeSection === 3 && (
            <ReadingSection title="Cognitive Regulation (Top-Down)." eyebrow="Step 4" icon={Zap} theme={theme}>
              <p>Once you've noticed the feeling, you need to manage it with your mind. This is <Highlight description="Using your thoughts and beliefs (cognition) to influence your emotional state." theme={theme}>Top-Down Regulation</Highlight>. A counter-intuitive but powerful strategy is <Highlight description="The act of reinterpreting the meaning of a high-arousal state. Physiologically, anxiety and excitement are almost identical; the only difference is the cognitive label you apply." theme={theme}>Arousal Reappraisal</Highlight>. It's neurologically easier to shift from "anxious" to "excited" than it is to "calm down."</p>
              <p>The second tool is <Highlight description="A core CBT technique where you challenge the validity of your negative automatic thoughts by examining the evidence for and against them." theme={theme}>Cognitive Restructuring</Highlight>. You treat your catastrophic thought ("I'm going to fail everything") like a prosecutor's claim in a courtroom and you become the defence lawyer, looking for counter-evidence.</p>
              <ArousalReappraisal/>
            </ReadingSection>
          )}
          {activeSection === 4 && (
            <ReadingSection title="Physiological Regulation (Bottom-Up)." eyebrow="Step 5" icon={Shield} theme={theme}>
              <p>Sometimes, your mind is too flooded to think straight. In these moments, you need to use your body to calm your mind. This is <Highlight description="Using physiological interventions (like breathing) to change your emotional state." theme={theme}>Bottom-Up Regulation</Highlight>. The fastest tool is breathing.</p>
              <p><Highlight description="A simple 4-4-4-4 breathing pattern that stimulates the Vagus nerve, a key part of your parasympathetic ('rest and digest') nervous system, acting as a physiological brake on the stress response." theme={theme}>Box Breathing</Highlight> is your emergency protocol for the exam hall. It's invisible and takes less than a minute to interrupt the panic loop and restore blood flow to your PFC.</p>
              <BoxBreathing />
            </ReadingSection>
          )}
          {activeSection === 5 && (
            <ReadingSection title="The Bio-Support System." eyebrow="Step 6" icon={Utensils} theme={theme}>
              <p>Emotional regulation is biologically expensive. A tired, dehydrated, or malnourished brain cannot regulate itself effectively, no matter how good your psychological tools are. Your baseline biology is non-negotiable.</p>
              <p>The "Anti-Cortisol" diet focuses on slow-release carbs (oats) and omega-3s (fish, walnuts) to stabilize your energy. Even mild dehydration (1-2%) significantly impairs concentration. And most importantly, sleep is when your brain consolidates learning and flushes out the metabolic waste that causes "brain fog." Strategic breaks, especially using <Highlight description="Non-Sleep Deep Rest: A guided meditation protocol that rapidly reduces cortisol and replenishes dopamine, making it an ideal 'reset button' during the study day." theme={theme}>NSDR</Highlight>, are also critical for recovery.</p>
            </ReadingSection>
          )}
          {activeSection === 6 && (
            <ReadingSection title="The Integrated Timeline." eyebrow="Step 7" icon={ClipboardCheck} theme={theme}>
              <p>You now have a complete toolkit of top-down and bottom-up strategies. The final step is to integrate them into a clear timeline.</p>
              <p><strong>Months Before:</strong> Build resilience. Practice daily Body Scans and learn Box Breathing when stress is low. **Morning Of:** Arousal regulation is key. Eat the "Exam Breakfast," stay away from panicked friends, and use the "Get Excited" reframe. **In The Hall:** If panic hits, use the "Paper Panic" drill: Stop, Breathe (3 cycles of Box Breathing), Micro-PMR (clench toes), and Re-engage with the easiest question. **Post-Exam:** A strict Post-Mortem Ban is essential to contain anxiety for the next paper.</p>
              <MicroCommitment theme={theme}><p>Choose one protocol from this module. Commit to practicing it for 5 minutes every day for one week. You are not just studying; you are training your nervous system.</p></MicroCommitment>
            </ReadingSection>
          )}
        </>
      )}
    </ModuleLayout>
  );
};
export default EmotionalIntelligenceModule;
