
/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
*/

import React, { useState } from 'react';
import { motion } from 'framer-motion';
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
    const ringCount = Math.min(wraps, 8);
    const axonR = Math.max(10, 88 - (ringCount * 9) - 8);
    const milestone = wraps === 1 ? 'First layer of myelin forming.' : wraps === 4 ? 'Halfway there — signal noticeably faster.' : wraps >= 8 ? 'Fully myelinated. Skill becoming automatic.' : null;

    return (
        <div className="my-10 rounded-2xl p-6 md:p-8" style={{ backgroundColor: '#F8F8F8', borderRadius: 18 }}>
            {/* Section chip + title */}
            <div className="text-center mb-8">
                <span className="inline-block px-3 py-1 rounded-full text-[11px] font-bold tracking-wider uppercase mb-3" style={{ backgroundColor: '#e8f5f2', color: '#1a6358', border: '1px solid rgba(42,125,111,0.2)', letterSpacing: '0.06em' }}>Neuroscience Simulation</span>
                <h4 className="font-serif font-bold" style={{ fontSize: 26, color: '#1a1a1a' }}>The Myelin Wrapper</h4>
                <p className="text-sm mt-1" style={{ color: '#7a7068' }}>Each time you practice a skill, you add a layer of myelin, making the signal faster.</p>
            </div>

            {/* Nerve cross-section card */}
            <div className="bg-white dark:bg-zinc-900" style={{ border: '2px solid #1a1a1a', borderRadius: 16, padding: 28, maxWidth: 320, margin: '0 auto' }}>
                <p className="text-center mb-4" style={{ fontSize: 10, fontWeight: 700, letterSpacing: '0.12em', color: '#9e9186', textTransform: 'uppercase' as const }}>Nerve Cross-Section</p>

                <svg viewBox="0 0 220 220" width="220" height="220" style={{ display: 'block', margin: '0 auto' }}>
                    {/* Outer boundary */}
                    <circle cx="110" cy="110" r="100" fill="#f4f0eb" stroke="#d0cdc8" strokeWidth="1.5"/>

                    {/* Myelin rings — outside in */}
                    {Array.from({ length: ringCount }).map((_, i) => {
                        const outerR = 88 - (i * 9);
                        const innerR = outerR - 7;
                        const opacity = 1 - (i * 0.08);
                        const isNewest = i === 0 && wraps > 0;
                        return (
                            <g key={`ring-${i}-${wraps}`}>
                                {isNewest ? (
                                    <motion.circle
                                        cx="110" cy="110" r={outerR}
                                        fill={i % 2 === 0 ? '#2A7D6F' : '#3d9e8f'}
                                        opacity={opacity}
                                        initial={{ scale: 0.7, opacity: 0 }}
                                        animate={{ scale: 1, opacity }}
                                        transition={{ duration: 0.35, ease: 'easeOut' }}
                                        style={{ transformOrigin: '110px 110px' }}
                                    />
                                ) : (
                                    <circle cx="110" cy="110" r={outerR} fill={i % 2 === 0 ? '#2A7D6F' : '#3d9e8f'} opacity={opacity} />
                                )}
                                <circle cx="110" cy="110" r={innerR} fill="#f4f0eb" />
                            </g>
                        );
                    })}

                    {/* Central axon */}
                    <circle cx="110" cy="110" r={axonR} fill="#e8f5f2" stroke="#2A7D6F" strokeWidth="2" />

                    {/* Speed pulse dot */}
                    {wraps > 0 && (
                        <circle cx="110" cy={110 - axonR} r="5" fill="#2A7D6F" opacity="0.9"/>
                    )}

                    {/* Zero state label */}
                    {wraps === 0 && (
                        <text x="110" y="115" textAnchor="middle" fontSize="11" fill="#9e9186" fontFamily="DM Sans, sans-serif">no myelin yet</text>
                    )}
                </svg>

                {/* Layer count */}
                <p className="text-center mt-3" style={{ fontSize: 12, color: '#9e9186' }}>{ringCount} / 8 myelin layers</p>

                {/* Signal speed stat */}
                <div className="text-center mt-4 pt-4" style={{ borderTop: '1px solid #e8e0d8' }}>
                    <p style={{ lineHeight: 1 }}>
                        <span className="font-serif font-bold" style={{ fontSize: 40, color: '#2A7D6F' }}>{speed}</span>
                        <span className="font-sans" style={{ fontSize: 16, color: '#9e9186', marginLeft: 4 }}>m/s</span>
                    </p>
                    <p className="mt-1" style={{ fontSize: 10, fontWeight: 700, letterSpacing: '0.1em', color: '#9e9186', textTransform: 'uppercase' as const }}>Signal Speed</p>
                </div>
            </div>

            {/* Milestone callout */}
            {milestone && (
                <motion.div
                    key={milestone}
                    initial={{ opacity: 0, y: 6 }}
                    animate={{ opacity: 1, y: 0 }}
                    className="mt-4 max-w-xs mx-auto"
                    style={{ borderLeft: '3px solid #2A7D6F', backgroundColor: '#f0faf8', borderRadius: '0 10px 10px 0', padding: '12px 16px' }}
                >
                    <p className="text-sm italic" style={{ color: '#1a6358' }}>{milestone}</p>
                </motion.div>
            )}

            {/* Buttons */}
            <div className="flex items-center justify-center gap-5 mt-6">
                <motion.button
                    onClick={() => setWraps(w => Math.min(w + 1, maxWraps))}
                    whileTap={{ scale: 0.97 }}
                    className="text-white font-semibold"
                    style={{ backgroundColor: '#2A7D6F', borderRadius: 100, padding: '14px 32px', fontSize: 15, border: 'none' }}
                    onMouseEnter={(e: React.MouseEvent<HTMLButtonElement>) => { e.currentTarget.style.backgroundColor = '#1a5a4e'; }}
                    onMouseLeave={(e: React.MouseEvent<HTMLButtonElement>) => { e.currentTarget.style.backgroundColor = '#2A7D6F'; }}
                >
                    Practice Skill
                </motion.button>
                <button
                    onClick={() => setWraps(0)}
                    className="font-medium"
                    style={{ fontSize: 13, color: '#9e9186', background: 'none', border: 'none' }}
                    onMouseEnter={(e: React.MouseEvent<HTMLButtonElement>) => { e.currentTarget.style.color = '#5a5550'; }}
                    onMouseLeave={(e: React.MouseEvent<HTMLButtonElement>) => { e.currentTarget.style.color = '#9e9186'; }}
                >
                    Reset
                </button>
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
        <div className="my-10 rounded-2xl p-6 md:p-8" style={{ backgroundColor: '#F8F8F8', borderRadius: 18 }}>
            <h4 className="font-serif text-2xl font-semibold text-zinc-800 dark:text-white text-center">Deep vs. Naive Practice</h4>
            <p className="text-center text-sm text-zinc-500 dark:text-zinc-400 mb-8">Which of these activities trigger myelin growth?</p>
            <div className="space-y-4">
                {activities.map(act => (
                    <div key={act.name} className="p-4 rounded-lg flex justify-between items-center" style={{ backgroundColor: '#FFFFFF', border: '2.5px solid #1C1917', borderRadius: 12, boxShadow: '3px 3px 0px 0px #1C1917' }}>
                        <span className="font-bold text-sm">{act.name}</span>
                        <div className="flex gap-2">
                           <button onClick={() => setChoice({...choice, [act.name]:'naive'})} className={`px-2 py-1 text-xs font-bold rounded ${choice[act.name] === 'naive' && act.type === 'naive' ? 'bg-emerald-200 text-emerald-800' : choice[act.name] === 'naive' && act.type === 'deep' ? 'bg-rose-200 text-rose-800' : 'bg-zinc-200'}`}>Naive</button>
                           <button onClick={() => setChoice({...choice, [act.name]:'deep'})} className={`px-2 py-1 text-xs font-bold rounded ${choice[act.name] === 'deep' && act.type === 'deep' ? 'bg-emerald-200 text-emerald-800' : choice[act.name] === 'deep' && act.type === 'naive' ? 'bg-rose-200 text-rose-800' : 'bg-zinc-200'}`}>Deep</button>
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
      moduleSubtitle="How Your Brain Gets Faster"
      moduleDescription={`That feeling of struggling with a hard question? It's not a sign you're bad at it — it's literally how your brain builds faster connections. This module shows you why the hard stuff is the stuff that works.`}
      theme={theme}
      sections={sections}
      onBack={onBack}
      progress={progress}
      onProgressUpdate={onProgressUpdate}
      finishButtonText="Build Your Wiring"
    >
      {(activeSection) => (
        <>
          {activeSection === 0 && (
            <ReadingSection title="The Silent Revolution." eyebrow="Step 1" icon={Cpu} theme={theme}>
              <p>In the last module, we learned that your brain physically changes when you learn. Now, we're looking at how you actually get good at something — how you go from slow and clunky to fast and automatic. It's not just about making connections between brain cells. It's about upgrading the wiring itself.</p>
              <p>Meet the unsung hero of your brain: the <Highlight description="These are basically the electricians of your brain. Their whole job is to wrap insulation around your brain's wiring so signals travel faster." theme={theme}>Oligodendrocyte</Highlight>. These cells work behind the scenes, wrapping your brain's circuits in a fatty insulation called <Highlight description="A fatty coating that wraps around your brain's wires, like the plastic insulation on a phone charger cable. It stops signals from leaking and makes everything way faster." theme={theme}>Myelin</Highlight>. This wrapping turns your brain's bumpy dirt roads into super-fast motorways. It's not just about knowing things — it's about being fast, precise, and doing things on autopilot.</p>
            </ReadingSection>
          )}
           {activeSection === 1 && (
            <ReadingSection title="The Signal of Struggle." eyebrow="Step 2" icon={Zap} theme={theme}>
                <p>So how does your brain know which wires to insulate? It listens for a signal. When you're really concentrating hard — like grinding through a tough maths question — your brain cells fire like crazy. That intense activity causes them to release chemicals along the wire, basically shouting: "This circuit is important! Upgrade it!"</p>
                <p>Those chemicals are a direct call to the electrician cells, telling them to get wrapping. And here's the key part: that feeling of <Highlight description="That frustrated, stuck feeling when you're working on something hard? That's actually your brain sending the signal to upgrade its wiring. No struggle, no upgrade." theme={theme}>struggle</Highlight> is not a sign you're failing. It's the physical sensation of your brain placing the order for a faster, better connection.</p>
            </ReadingSection>
          )}
          {activeSection === 2 && (
            <ReadingSection title="Deep Practice." eyebrow="Step 3" icon={SlidersHorizontal} theme={theme}>
              <p>The type of practice that sends this "upgrade" signal is called <Highlight description="A way of practising where you really focus, push yourself to the edge of what you can do, make mistakes, fix them, and repeat. It's the kind of practice that actually triggers your brain to upgrade its wiring." theme={theme}>Deep Practice</Highlight>. It's the opposite of passively re-reading your notes. Easy practice feels productive, but it barely registers with your brain — it doesn't trigger the upgrade. It just gives you a false sense of confidence.</p>
              <p>Deep practice is hard, uncomfortable, and full of mistakes. It means doing past papers without your notes, forcing yourself to recall things from scratch, and pushing yourself just outside your comfort zone. That discomfort is the signal. It's the heavy lifting that tells your brain to build more insulation — more myelin — around the circuits that matter.</p>
              <DeepPracticeSorter />
            </ReadingSection>
          )}
          {activeSection === 3 && (
            <ReadingSection title="The Mastery Metaphors." eyebrow="Step 4" icon={Microscope} theme={theme}>
              <p>To really picture what's going on, here are a couple of ways to think about it.</p>
              <p>Imagine upgrading your home internet from dial-up to fibre <strong>broadband</strong>. Before the upgrade, your brain can only handle one simple idea at a time — it buffers and lags. After deep practice wraps your circuits in myelin, you can handle multiple ideas at once without slowing down. Or think of it as paving a <strong>dirt road into a motorway</strong>. The first time you learn something, it's slow and bumpy. With deep practice, you pave that road, and information starts flowing at speed, almost on autopilot.</p>
              <MyelinWrapper/>
            </ReadingSection>
          )}
           {activeSection === 4 && (
            <ReadingSection title="The Rules of Myelination." eyebrow="Step 5" icon={Construction} theme={theme}>
                <p>There are a few simple rules here that you can't skip. First, <strong>struggle is not optional</strong>. Easy practice doesn't send the signal. You need to be in the "sweet spot" where you're making mistakes and fixing them. That loop of getting it wrong and then getting it right is what kicks off the building process.</p>
                <p>Second, <strong>it's permanent but slow</strong>. Once a skill gets wrapped in myelin, it sticks with you for good. This is why cramming the night before doesn't last, but weeks of proper practice does. You can't build a motorway overnight. Every session of deep practice adds another thin layer of insulation, like another ring on a tree.</p>
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
