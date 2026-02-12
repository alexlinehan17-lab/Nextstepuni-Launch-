
/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
*/

import React, { useState } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import {
  Cpu, Moon, Coffee, Zap, Repeat, ClipboardCheck, CheckCircle2
} from 'lucide-react';
import { ModuleProgress } from '../types';
import { slateTheme } from '../moduleThemes';
import { Highlight, ReadingSection, MicroCommitment } from './ModuleShared';
import { ModuleLayout } from './ModuleLayout';

const theme = slateTheme;

// --- INTERACTIVE COMPONENTS ---

const GlycemicIndexSimulator = () => {
    const [selected, setSelected] = useState<Set<'high' | 'low'>>(new Set());

    const toggle = (type: 'high' | 'low') => {
      setSelected(prev => {
        const next = new Set(prev);
        if (next.has(type)) next.delete(type); else next.add(type);
        return next;
      });
    };

    // Chart dimensions (inside padding)
    const W = 360, H = 160;
    const padL = 40, padR = 16, padT = 16, padB = 28;
    const chartW = W - padL - padR;
    const chartH = H - padT - padB;

    // Map data points to SVG coords
    const toX = (hour: number) => padL + (hour / 3) * chartW;
    const toY = (level: number) => padT + chartH - (level / 100) * chartH; // 0-100 scale

    // Blood sugar curves (hour, level) — baseline is ~50
    const highGI = [
      [0, 50], [0.3, 65], [0.5, 88], [0.75, 92], [1, 78], [1.3, 55], [1.6, 35], [2, 30], [2.5, 38], [3, 45],
    ] as [number, number][];

    const lowGI = [
      [0, 50], [0.5, 58], [1, 65], [1.5, 68], [2, 66], [2.5, 62], [3, 58],
    ] as [number, number][];

    // Build smooth path from points
    const buildPath = (points: [number, number][]) => {
      if (points.length < 2) return '';
      const coords = points.map(([h, l]) => [toX(h), toY(l)]);
      let d = `M ${coords[0][0]} ${coords[0][1]}`;
      for (let i = 1; i < coords.length; i++) {
        const prev = coords[i - 1];
        const curr = coords[i];
        const cpx = (prev[0] + curr[0]) / 2;
        d += ` C ${cpx} ${prev[1]}, ${cpx} ${curr[1]}, ${curr[0]} ${curr[1]}`;
      }
      return d;
    };

    const highPath = buildPath(highGI);
    const lowPath = buildPath(lowGI);

    // Focus zone band (optimal blood sugar ~55-75)
    const focusTop = toY(75);
    const focusBottom = toY(55);

    const hours = [0, 1, 2, 3];
    const levels = [
      { val: 25, label: 'Low' },
      { val: 50, label: 'Normal' },
      { val: 75, label: 'High' },
    ];

    return (
      <div className="my-10 p-8 md:p-12 bg-white dark:bg-zinc-800 rounded-xl border border-zinc-200 dark:border-zinc-700">
        <h4 className="font-serif text-2xl font-semibold text-zinc-800 dark:text-white text-center">Glycemic Index Simulator</h4>
        <p className="text-center text-sm text-zinc-500 dark:text-zinc-400 mb-6">Toggle each breakfast to compare what happens to your blood sugar over 3 hours.</p>

        {/* Buttons */}
        <div className="flex justify-center gap-3 mb-6">
          <button
            onClick={() => toggle('high')}
            className={`px-4 py-2 text-xs font-bold rounded-lg border transition-all ${
              selected.has('high')
                ? 'bg-rose-500 text-white border-rose-500'
                : 'bg-rose-50 text-rose-700 border-rose-200 hover:border-rose-400'
            }`}
          >
            Sugary Cereal (High-GI)
          </button>
          <button
            onClick={() => toggle('low')}
            className={`px-4 py-2 text-xs font-bold rounded-lg border transition-all ${
              selected.has('low')
                ? 'bg-emerald-500 text-white border-emerald-500'
                : 'bg-emerald-50 text-emerald-700 border-emerald-200 hover:border-emerald-400'
            }`}
          >
            Porridge (Low-GI)
          </button>
        </div>

        {/* Chart */}
        <div className="bg-zinc-50 dark:bg-zinc-900/30 rounded-xl border border-zinc-200 dark:border-zinc-700 p-2">
          <svg viewBox={`0 0 ${W} ${H}`} className="w-full h-auto">
            {/* Focus zone band */}
            <rect
              x={padL} y={focusTop}
              width={chartW} height={focusBottom - focusTop}
              fill="currentColor"
              className="text-emerald-100 dark:text-emerald-900/20"
            />
            <text
              x={padL + 4} y={focusTop + 11}
              className="text-[7px] font-bold"
              fill="#10b981"
              opacity={0.6}
            >
              FOCUS ZONE
            </text>

            {/* Gridlines */}
            {levels.map(l => (
              <line key={l.val} x1={padL} y1={toY(l.val)} x2={W - padR} y2={toY(l.val)} stroke="currentColor" className="text-zinc-200 dark:text-zinc-700" strokeWidth="0.5" />
            ))}
            {hours.map(h => (
              <line key={h} x1={toX(h)} y1={padT} x2={toX(h)} y2={H - padB} stroke="currentColor" className="text-zinc-200 dark:text-zinc-700" strokeWidth="0.5" />
            ))}

            {/* Y-axis labels */}
            {levels.map(l => (
              <text key={l.val} x={padL - 4} y={toY(l.val) + 3} textAnchor="end" className="text-[7px]" fill="#a1a1aa">{l.label}</text>
            ))}

            {/* X-axis labels */}
            {hours.map(h => (
              <text key={h} x={toX(h)} y={H - padB + 14} textAnchor="middle" className="text-[7px]" fill="#a1a1aa">{h}h</text>
            ))}

            {/* High-GI path */}
            {selected.has('high') && (
              <>
                <motion.path
                  d={highPath}
                  fill="none"
                  stroke="#f43f5e"
                  strokeWidth="2.5"
                  strokeLinecap="round"
                  strokeLinejoin="round"
                  initial={{ pathLength: 0 }}
                  animate={{ pathLength: 1 }}
                  transition={{ duration: 1.2, ease: 'easeOut' }}
                />
                {/* Crash annotation */}
                <motion.g
                  initial={{ opacity: 0 }}
                  animate={{ opacity: 1 }}
                  transition={{ delay: 0.8 }}
                >
                  <line x1={toX(1.6)} y1={toY(35)} x2={toX(1.6)} y2={toY(35) - 18} stroke="#f43f5e" strokeWidth="0.8" strokeDasharray="2 2" />
                  <text x={toX(1.6)} y={toY(35) - 22} textAnchor="middle" className="text-[6px] font-bold" fill="#f43f5e">CRASH</text>
                </motion.g>
              </>
            )}

            {/* Low-GI path */}
            {selected.has('low') && (
              <motion.path
                d={lowPath}
                fill="none"
                stroke="#10b981"
                strokeWidth="2.5"
                strokeLinecap="round"
                strokeLinejoin="round"
                initial={{ pathLength: 0 }}
                animate={{ pathLength: 1 }}
                transition={{ duration: 1.2, ease: 'easeOut' }}
              />
            )}
          </svg>
        </div>

        {/* Legend / insight */}
        {selected.size > 0 && (
          <motion.div
            initial={{ opacity: 0, y: 6 }}
            animate={{ opacity: 1, y: 0 }}
            className="mt-4 flex justify-center gap-5"
          >
            {selected.has('high') && (
              <div className="flex items-center gap-2">
                <div className="w-5 h-1 rounded-full bg-rose-500" />
                <span className="text-[10px] text-zinc-500 dark:text-zinc-400">Spike then crash — focus lost by hour 2</span>
              </div>
            )}
            {selected.has('low') && (
              <div className="flex items-center gap-2">
                <div className="w-5 h-1 rounded-full bg-emerald-500" />
                <span className="text-[10px] text-zinc-500 dark:text-zinc-400">Steady release — stays in focus zone for 3 hours</span>
              </div>
            )}
          </motion.div>
        )}

        {selected.size === 0 && (
          <p className="text-center text-xs text-zinc-400 dark:text-zinc-500 mt-4">Select a breakfast to see its blood sugar curve.</p>
        )}
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
        <div className="my-10 p-8 md:p-12 bg-white dark:bg-zinc-800 rounded-xl border border-zinc-200 dark:border-zinc-700">
            <h4 className="font-serif text-2xl font-semibold text-zinc-800 dark:text-white text-center">High-Performance Checklist</h4>
            <p className="text-center text-sm text-zinc-500 dark:text-zinc-400 mb-8">This is the blueprint for a perfect study day, based on your biology.</p>
            <div className="space-y-3">
                {items.map(item => (
                    <div key={item.key} onClick={() => toggle(item.key)} className={`p-4 rounded-xl border flex items-center gap-4 cursor-pointer ${checks[item.key] ? 'bg-emerald-50 border-emerald-200' : 'bg-zinc-50 border-zinc-200 dark:border-zinc-700'}`}>
                        <span className="font-mono text-xs font-bold w-12">{item.time}</span>
                        <div className="flex-grow">
                            <p className="font-bold text-sm">{item.task}</p>
                            <p className="text-xs text-zinc-500 dark:text-zinc-400">{item.details}</p>
                        </div>
                        <div className={`w-6 h-6 rounded-full flex-shrink-0 flex items-center justify-center ${checks[item.key] ? 'bg-emerald-500' : 'bg-zinc-300'}`}><CheckCircle2 size={12} className="text-white"/></div>
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
    { id: 'vicious-cycle', title: 'The Vicious Cycle', eyebrow: '05 // The Feedback Loop', icon: Repeat },
    { id: 'blueprint', title: 'The High-Performance Blueprint', eyebrow: '06 // Your Protocol', icon: ClipboardCheck },
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
              <p>At the centre of this engine is your <Highlight description="The 'CEO' of your brain, located behind your forehead. It's responsible for working memory, inhibitory control, and complex decision-making. It's the last part of the brain to fully mature." theme={theme}>Prefrontal Cortex (PFC)</Highlight>--the academic command centre that allows you to hold a complex Maths problem in your head or structure an English essay. During your teenage years, this area is undergoing a massive renovation, making it incredibly powerful but also uniquely vulnerable. When deprived of sleep or stable energy, your brain performs a ruthless triage, functionally decoupling the rational PFC from the emotional amygdala--a process called <Highlight description="The breakdown of communication between the rational prefrontal cortex and the emotional amygdala caused by sleep or energy deprivation. This leaves you neurologically predisposed to anxiety and poor decision-making." theme={theme}>Neural Decoupling</Highlight>. You're not just tired; your hardware is compromised.</p>
              <p>This module provides a scientifically grounded blueprint for the Leaving Cert student. It moves beyond generic advice to explain the mechanisms of memory and focus, providing actionable protocols. The strategic shift is from "time management" to <Highlight description="The superior strategy of focusing on the biological inputs (sleep, food, exercise) that determine the quality and quantity of your available mental energy." theme={theme}>energy management</Highlight>.</p>
            </ReadingSection>
          )}
          {activeSection === 1 && (
            <ReadingSection title="The Save Button: Sleep." eyebrow="Step 2" icon={Moon} theme={theme}>
              <p>Learning is a two-stage process. The first stage, <Highlight description="The initial process of taking in new information when you are awake. These memory traces are fragile." theme={theme}>encoding</Highlight>, happens when you study. But this new information is fragile, temporarily stored in your brain's 'RAM'--the <Highlight description="A seahorse-shaped structure in the brain that acts as a temporary buffer for new memories." theme={theme}>hippocampus</Highlight>. Without the second stage, <Highlight description="The process by which fragile, short-term memories are stabilized and transferred to the neocortex for long-term storage. This happens primarily during sleep." theme={theme}>consolidation</Highlight>, that learning is erased. Sleep is the "save button." A student who studies for five hours but sleeps for five has learned less than a student who studies for three and sleeps for eight.</p>
              <p>Your brain cycles through different types of sleep. <Highlight description="Deep, non-rapid eye movement sleep that is critical for consolidating declarative memories (facts, dates, definitions)." theme={theme}>Slow-Wave Sleep (SWS)</Highlight>, dominant in the first half of the night, is for saving facts. <Highlight description="A stage of sleep characterized by vivid dreams and crucial for procedural memory (skills), creative problem-solving, and emotional regulation." theme={theme}>REM Sleep</Highlight>, dominant in the second half, is for making connections and solving problems. Cutting sleep short disproportionately sacrifices REM sleep, killing your creativity and problem-solving ability for the next day.</p>
              <p>The data on sleep deprivation is sobering. After just one week of 5-hour nights, students' working memory accuracy drops by a catastrophic <Highlight description="A landmark sleep study finding: restricting sleep to 5 hours per night for one week causes a 17% drop in working memory accuracy--enough to turn an A into a C." theme={theme}>17%</Highlight>--enough to turn an A into a C. Even more striking is the <Highlight description="The scientifically established fact that after 17-19 hours of continuous wakefulness, your cognitive impairment is equivalent to having a Blood Alcohol Concentration (BAC) of 0.05%." theme={theme}>Intoxication Equivalence</Highlight>: after 17-19 hours awake, your cognitive impairment equals a Blood Alcohol Concentration of 0.05%. If you wake up at 6 AM, by 11 PM you are functionally as impaired as someone who is legally drunk. And "weekend catch-up" is a myth--two nights of recovery sleep are not enough to restore your executive functions.</p>
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
            <ReadingSection title="The Vicious Cycle." eyebrow="Step 5" icon={Repeat} theme={theme}>
              <p>Sleep and nutrition are not separate issues. They are locked in a vicious feedback loop. Sleep loss disrupts the hormones that regulate hunger--specifically <Highlight description="Sleep deprivation suppresses leptin (the 'I'm full' hormone) and elevates ghrelin (the 'I'm hungry' hormone), making you biologically crave high-calorie, high-carbohydrate foods." theme={theme}>leptin and ghrelin</Highlight>--making you biologically crave high-calorie, high-carbohydrate foods. You wake up tired, so you're primed to choose the sugary cereal over the eggs.</p>
              <p>That high-sugar food then disrupts your sleep. The blood glucose fluctuations can interfere with <Highlight description="Deep, non-rapid eye movement sleep that is critical for consolidating declarative memories (facts, dates, definitions). Disrupted by blood sugar instability." theme={theme}>Slow-Wave Sleep (SWS)</Highlight>, the deep sleep stage crucial for memory consolidation. So, poor sleep leads to poor diet, which leads to even poorer sleep. Over a semester, this cycle cumulatively erodes your brain's executive function. Recognising this loop is the first step to breaking it--and that starts with stabilising either end: better sleep hygiene or a low-GI breakfast.</p>
            </ReadingSection>
          )}
          {activeSection === 5 && (
            <ReadingSection title="The High-Performance Blueprint." eyebrow="Step 6" icon={ClipboardCheck} theme={theme}>
              <p>By integrating the science of this "Cognitive Triad," we can construct an actionable blueprint for the Leaving Cert student. This approach shifts the focus from the flawed model of "time management" to the superior model of "energy management."</p>
              <p>The following checklist is based on an optimized daily routine for a non-school day. It is designed to align with your natural adolescent circadian rhythms, maximize BDNF production, and ensure proper memory consolidation. This is not an aspirational goal; it is the evidence-based protocol for high performance.</p>
              <HighPerformanceChecklist />
              <MicroCommitment theme={theme}>
                <p><strong>The Breakfast Experiment:</strong> Try two mornings with different breakfasts. <strong>Day 1:</strong> Eat a high-sugar breakfast (sugary cereal, fruit juice, white toast). At 10:30 AM, rate your energy and focus from 1-10. <strong>Day 2:</strong> Eat a low-sugar, high-protein breakfast (porridge, eggs, yogurt). At 10:30 AM, rate your energy and focus from 1-10. Compare the results--feel the data for yourself.</p>
              </MicroCommitment>
            </ReadingSection>
          )}
        </>
      )}
    </ModuleLayout>
  );
};
export default ControllableVariablesModule;
