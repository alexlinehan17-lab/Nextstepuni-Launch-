
/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
*/

import React, { useState } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import {
  Cpu, Moon, Coffee, Zap, ClipboardCheck, CheckCircle2
} from 'lucide-react';
import { ModuleProgress } from '../types';
import { slateTheme } from '../moduleThemes';
import { Highlight, ReadingSection, MicroCommitment } from './ModuleShared';
import { ModuleLayout } from './ModuleLayout';

const theme = slateTheme;

// --- INTERACTIVE COMPONENTS ---

const GlycemicIndexSimulator = () => {
    const [food, setFood] = useState<'none' | 'high' | 'low'>('none');

    const pathData = {
        none: "M0 80 L 500 80",
        high: "M0 80 C 100 10, 150 10, 200 60 C 250 110, 300 110, 500 90",
        low: "M0 80 C 100 70, 200 60, 500 50",
    }

    return(
        <div className="my-10 p-8 md:p-12 bg-white rounded-[3rem] border border-stone-200 shadow-xl">
            <h4 className="font-serif text-2xl font-semibold text-stone-800 text-center italic">Glycemic Index Simulator</h4>
            <p className="text-center text-sm text-stone-500 mb-8">Choose a breakfast and see what it does to your blood sugar over 3 hours.</p>
            <div className="w-full h-32 bg-stone-50 rounded-lg p-4">
                <svg viewBox="0 0 500 100" className="w-full h-full" preserveAspectRatio="none">
                     <motion.path d={pathData[food]} fill="none" stroke="#f59e0b" strokeWidth="3" transition={{type: 'spring', damping: 15, stiffness: 100}}/>
                     <text x="5" y="15" fontSize="8" fill="#9ca3af">High Energy</text>
                     <text x="5" y="95" fontSize="8" fill="#9ca3af">Low Energy</text>
                </svg>
            </div>
             <div className="flex justify-center gap-4 mt-6">
                <button onClick={() => setFood('high')} className="px-4 py-2 bg-rose-100 text-rose-800 text-xs font-bold rounded-lg">Sugary Cereal (High-GI)</button>
                <button onClick={() => setFood('low')} className="px-4 py-2 bg-emerald-100 text-emerald-800 text-xs font-bold rounded-lg">Porridge (Low-GI)</button>
             </div>
        </div>
    );
};

const HighPerformanceChecklist = () => {
    const [checks, setChecks] = useState<{[key: string]: boolean}>({});
    const toggle = (key: string) => setChecks(prev => ({...prev, [key]: !prev[key]}));
    const items = [
        { key: 'wake', time: '08:30', task: 'Wake + Light Exposure', details: '10 mins outside. Anchors circadian clock.' },
        { key: 'fuel', time: '08:45', task: 'Hydration + Breakfast', details: '500ml water. Low-GI porridge.' },
        { key: 'deep1', time: '09:30', task: 'Study Block 1 (Deep Work)', details: '90 mins. High-cognitive load subjects.' },
        { key: 'break1', time: '11:00', task: 'Active Break', details: '15 mins walking. Avoid phone.' },
        { key: 'exercise', time: '16:00', task: 'EXERCISE (The Reset)', details: '45 mins. Spikes BDNF.' },
        { key: 'review', time: '18:30', task: 'Review Block (Active Recall)', details: '60 mins. "Test" yourself on morning work.' },
        { key: 'tech', time: '22:00', task: 'Tech Down-Regulation', details: 'No screens. Essential for melatonin onset.' },
        { key: 'sleep', time: '23:00', task: 'Sleep', details: '8.5 - 9 hours opportunity.' },
    ];

    return(
        <div className="my-10 p-8 md:p-12 bg-white rounded-[3rem] border border-stone-200 shadow-xl">
            <h4 className="font-serif text-2xl font-semibold text-stone-800 text-center italic">High-Performance Checklist</h4>
            <p className="text-center text-sm text-stone-500 mb-8">This is the blueprint for a perfect study day, based on your biology.</p>
            <div className="space-y-3">
                {items.map(item => (
                    <div key={item.key} onClick={() => toggle(item.key)} className={`p-4 rounded-xl border-2 flex items-center gap-4 cursor-pointer ${checks[item.key] ? 'bg-emerald-50 border-emerald-200' : 'bg-stone-50 border-stone-200'}`}>
                        <span className="font-mono text-xs font-bold w-12">{item.time}</span>
                        <div className="flex-grow">
                            <p className="font-bold text-sm">{item.task}</p>
                            <p className="text-xs text-stone-500">{item.details}</p>
                        </div>
                        <div className={`w-6 h-6 rounded-full flex-shrink-0 flex items-center justify-center ${checks[item.key] ? 'bg-emerald-500' : 'bg-stone-300'}`}><CheckCircle2 size={12} className="text-white"/></div>
                    </div>
                ))}
            </div>
        </div>
    );
}


// --- MODULE COMPONENT ---
const ControllableVariablesModule: React.FC<{ onBack: () => void; progress: ModuleProgress; onProgressUpdate: (progress: ModuleProgress) => void }> = ({ onBack, progress, onProgressUpdate }) => {
  const sections = [
    { id: 'engine', title: 'The Performance Engine', eyebrow: '01 // The Core Idea', icon: Cpu },
    { id: 'sleep', title: 'The Save Button: Sleep', eyebrow: '02 // The Foundation', icon: Moon },
    { id: 'nutrition', title: 'The Fuel Supply: Nutrition', eyebrow: '03 // The Energy', icon: Coffee },
    { id: 'exercise', title: 'The Upgrade: Exercise', eyebrow: '04 // The Catalyst', icon: Zap },
    { id: 'blueprint', title: 'The High-Performance Blueprint', eyebrow: '05 // The Plan', icon: ClipboardCheck },
  ];

  return (
    <ModuleLayout
      moduleNumber="09"
      moduleTitle="Controllable Variables"
      theme={theme}
      sections={sections}
      onBack={onBack}
      progress={progress}
      onProgressUpdate={onProgressUpdate}
    >
      {(activeSection) => (
        <>
          {activeSection === 0 && (
            <ReadingSection title="The Performance Engine." eyebrow="Step 1" icon={Cpu} theme={theme}>
              <p>Students often treat their brains like a disembodied intellect, ignoring the fact that learning, memory, and focus are biological processes. Your brain is not a computer; it's a high-performance engine. Its output is strictly constrained by its inputs and maintenance schedule. The emerging consensus from neuroscience is that your "capacity to learn" is not a fixed trait but a dynamic state that fluctuates based on three core physiological pillars: <Highlight description="The 'save button' for your memory, where learning is consolidated." theme={theme}>Sleep</Highlight>, <Highlight description="The fuel supply for your neurons, determining your ability to focus." theme={theme}>Nutrition</Highlight>, and <Highlight description="The upgrade mechanism that physically enhances your brain's ability to learn." theme={theme}>Exercise</Highlight>.</p>
              <p>This module provides a scientifically grounded blueprint for the Leaving Cert student. It moves beyond generic advice to explain the mechanisms of memory and focus, providing actionable protocols. The strategic shift is from "time management" to <Highlight description="The superior strategy of focusing on the biological inputs (sleep, food, exercise) that determine the quality and quantity of your available mental energy." theme={theme}>energy management</Highlight>.</p>
            </ReadingSection>
          )}
          {activeSection === 1 && (
            <ReadingSection title="The Save Button: Sleep." eyebrow="Step 2" icon={Moon} theme={theme}>
              <p>Learning is a two-stage process. The first stage, <Highlight description="The initial process of taking in new information when you are awake. These memory traces are fragile." theme={theme}>encoding</Highlight>, happens when you study. But this new information is fragile, temporarily stored in your brain's 'RAM'--the <Highlight description="A seahorse-shaped structure in the brain that acts as a temporary buffer for new memories." theme={theme}>hippocampus</Highlight>. Without the second stage, <Highlight description="The process by which fragile, short-term memories are stabilized and transferred to the neocortex for long-term storage. This happens primarily during sleep." theme={theme}>consolidation</Highlight>, that learning is erased. Sleep is the "save button." A student who studies for five hours but sleeps for five has learned less than a student who studies for three and sleeps for eight.</p>
              <p>Your brain cycles through different types of sleep. <Highlight description="Deep, non-rapid eye movement sleep that is critical for consolidating declarative memories (facts, dates, definitions)." theme={theme}>Slow-Wave Sleep (SWS)</Highlight>, dominant in the first half of the night, is for saving facts. <Highlight description="A stage of sleep characterized by vivid dreams and crucial for procedural memory (skills), creative problem-solving, and emotional regulation." theme={theme}>REM Sleep</Highlight>, dominant in the second half, is for making connections and solving problems. Cutting sleep short disproportionately sacrifices REM sleep, killing your creativity and problem-solving ability for the next day.</p>
            </ReadingSection>
          )}
          {activeSection === 2 && (
            <ReadingSection title="The Fuel Supply: Nutrition." eyebrow="Step 3" icon={Coffee} theme={theme}>
              <p>Your brain is a metabolically expensive organ. It consumes 20% of your body's glucose. Nutrition is not a matter of aesthetics; it is a matter of substrate availability for your cognitive engine. The delivery mechanism of this glucose determines your performance.</p>
              <p>High-<Highlight description="A measure of how quickly a food causes blood sugar levels to rise. High-GI foods (sugary snacks, white bread) cause a rapid spike and subsequent crash." theme={theme}>Glycemic Index (GI)</Highlight> foods create a roller-coaster of focus, leading to a "crash" mid-exam. Low-GI foods like oats provide a stable platform for concentration. Beyond energy, your brain needs specific micronutrients to build the chemicals that transmit signals. Deficiencies in <Highlight description="Found in oily fish, these fats are crucial for maintaining the fluidity of your brain cell membranes, allowing for efficient electrical signals." theme={theme}>Omega-3s</Highlight> and <Highlight description="Vitamins like B6, B9, and B12 are critical for synthesizing neurotransmitters like dopamine and serotonin." theme={theme}>B-Vitamins</Highlight> are directly correlated with "brain fog" and slower processing speeds. Finally, a loss of just 1% of body mass due to dehydration can cause measurable impairments in your working memory.</p>
              <GlycemicIndexSimulator />
            </ReadingSection>
          )}
          {activeSection === 3 && (
            <ReadingSection title="The Upgrade: Exercise." eyebrow="Step 4" icon={Zap} theme={theme}>
                <p>Exercise is not a distraction from study; it is a biological necessity for <Highlight description="The brain's ability to rewire itself and learn. Exercise is a powerful catalyst for this process." theme={theme}>neuroplasticity</Highlight>. The strongest link is <Highlight description="Brain-Derived Neurotrophic Factor (BDNF) is a protein that acts like 'Miracle-Gro' for your brain, supporting the growth of new neurons and synapses." theme={theme}>BDNF</Highlight>, a protein that acts as "molecular fertilizer" for your brain. Physical exertion effectively "switches on" the gene for BDNF production. A student with high BDNF levels will learn faster and retain more than a sedentary student.</p>
                <p>Timing is critical. Exercise *before* study increases arousal and focus. Fascinatingly, research suggests exercise *after* a learning session may be even better for long-term retention--the <Highlight description="The finding that exercise performed a few hours after learning can retroactively 'tag' the preceding memories as important for consolidation." theme={theme}>Consolidation Hack</Highlight>. Finally, <Highlight description="Low-intensity exercise like walking, which helps clear metabolic waste and stress hormones like cortisol, making it superior to passive rest (scrolling on a phone)." theme={theme}>Active Recovery</Highlight> is superior to passive rest for reducing cognitive fatigue.</p>
            </ReadingSection>
          )}
          {activeSection === 4 && (
            <ReadingSection title="The High-Performance Blueprint." eyebrow="Step 5" icon={ClipboardCheck} theme={theme}>
              <p>By integrating the science of this "Cognitive Triad," we can construct an actionable blueprint for the Leaving Cert student. This approach shifts the focus from the flawed model of "time management" to the superior model of "energy management."</p>
              <p>The following checklist is based on an optimized daily routine for a non-school day. It is designed to align with your natural adolescent circadian rhythms, maximize BDNF production, and ensure proper memory consolidation. This is not an aspirational goal; it is the evidence-based protocol for high performance.</p>
              <HighPerformanceChecklist />
              <MicroCommitment theme={theme}>
                <p>Pick ONE item from this checklist that you are not currently doing. Just one. For the next seven days, commit to implementing that single change. Notice the effect it has on your energy and focus.</p>
              </MicroCommitment>
            </ReadingSection>
          )}
        </>
      )}
    </ModuleLayout>
  );
};
export default ControllableVariablesModule;
