/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
*/

import React, { useState } from 'react';
import { motion, AnimatePresence, Reorder } from 'framer-motion';
import { CheckCircle2, History, DraftingCompass, ClipboardList, Layers, BrainCircuit, Shield } from 'lucide-react';
import { ModuleProgress } from '../types';
import { skyTheme } from '../moduleThemes';
import { Highlight, ReadingSection, MicroCommitment } from './ModuleShared';
import { ModuleLayout } from './ModuleLayout';

const theme = skyTheme;

// --- INTERACTIVE COMPONENTS ---
const PlanningParadoxVisualizer = () => {
    const [revealed, setRevealed] = useState(false);

    const W = 440, H = 260;
    const padL = 8, padR = 8, padT = 28, padB = 44;
    const chartW = W - padL - padR, chartH = H - padT - padB;
    const toX = (f: number) => padL + f * chartW;
    const toY = (f: number) => padT + (1 - f) * chartH;

    const months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun'];
    // Forward plan: minimal effort early, exponential panic at end
    const fwdEffort = [0.08, 0.10, 0.15, 0.30, 0.72, 1.0];
    // Reverse plan: steady, strategic, tapers down for rest before exams
    const revEffort = [0.70, 0.65, 0.60, 0.55, 0.45, 0.30];
    // Stress lines
    const fwdStress = [0.12, 0.15, 0.25, 0.55, 0.85, 1.0];
    const revStress = [0.30, 0.25, 0.22, 0.20, 0.18, 0.10];

    const buildArea = (data: number[]) => {
        const pts = data.map((v, i) => ({ x: toX(i / (data.length - 1)), y: toY(v) }));
        let d = `M ${pts[0].x} ${toY(0)} L ${pts[0].x} ${pts[0].y}`;
        for (let i = 1; i < pts.length; i++) {
            const cx1 = pts[i - 1].x + (pts[i].x - pts[i - 1].x) * 0.4;
            const cx2 = pts[i - 1].x + (pts[i].x - pts[i - 1].x) * 0.6;
            d += ` C ${cx1} ${pts[i - 1].y}, ${cx2} ${pts[i].y}, ${pts[i].x} ${pts[i].y}`;
        }
        d += ` L ${pts[pts.length - 1].x} ${toY(0)} Z`;
        return d;
    };

    const buildLine = (data: number[]) => {
        const pts = data.map((v, i) => ({ x: toX(i / (data.length - 1)), y: toY(v) }));
        let d = `M ${pts[0].x} ${pts[0].y}`;
        for (let i = 1; i < pts.length; i++) {
            const cx1 = pts[i - 1].x + (pts[i].x - pts[i - 1].x) * 0.4;
            const cx2 = pts[i - 1].x + (pts[i].x - pts[i - 1].x) * 0.6;
            d += ` C ${cx1} ${pts[i - 1].y}, ${cx2} ${pts[i].y}, ${pts[i].x} ${pts[i].y}`;
        }
        return d;
    };

    const fwdPhases = [
        { label: 'Procrastinate', x1: 0, x2: 0.33, color: '#fca5a5' },
        { label: 'Catch up', x1: 0.33, x2: 0.66, color: '#f87171' },
        { label: 'Cram & panic', x1: 0.66, x2: 1, color: '#ef4444' },
    ];
    const revPhases = [
        { label: 'Set targets & past papers', x1: 0, x2: 0.33, color: '#6ee7b7' },
        { label: 'Fill gaps & refine', x1: 0.33, x2: 0.66, color: '#34d399' },
        { label: 'Taper & rest', x1: 0.66, x2: 1, color: '#10b981' },
    ];

    const Chart = ({ effort, stress, phases, areaColor, areaId, stressColor, label }: {
        effort: number[]; stress: number[]; phases: { label: string; x1: number; x2: number; color: string }[];
        areaColor: string; areaId: string; stressColor: string; label: string;
    }) => (
        <svg viewBox={`0 0 ${W} ${H}`} className="w-full">
            <defs>
                <linearGradient id={areaId} x1="0" y1="0" x2="0" y2="1">
                    <stop offset="0%" stopColor={areaColor} stopOpacity="0.5" />
                    <stop offset="100%" stopColor={areaColor} stopOpacity="0.05" />
                </linearGradient>
            </defs>
            {/* Grid lines */}
            {[0.25, 0.5, 0.75, 1.0].map(v => (
                <line key={v} x1={padL} x2={W - padR} y1={toY(v)} y2={toY(v)} stroke="#a1a1aa" strokeOpacity="0.15" strokeDasharray="3 3" />
            ))}
            {/* Baseline */}
            <line x1={padL} x2={W - padR} y1={toY(0)} y2={toY(0)} stroke="#a1a1aa" strokeOpacity="0.3" />
            {/* Effort area */}
            <motion.path
                d={buildArea(effort)}
                fill={`url(#${areaId})`}
                initial={{ opacity: 0 }}
                animate={{ opacity: 1 }}
                transition={{ duration: 0.8 }}
            />
            {/* Effort line */}
            <motion.path
                d={buildLine(effort)}
                fill="none" stroke={areaColor} strokeWidth="2.5" strokeLinecap="round"
                initial={{ pathLength: 0 }} animate={{ pathLength: 1 }}
                transition={{ duration: 1.2, ease: 'easeOut' }}
            />
            {/* Stress line (dashed) */}
            <motion.path
                d={buildLine(stress)}
                fill="none" stroke={stressColor} strokeWidth="1.5" strokeDasharray="5 3" strokeLinecap="round"
                initial={{ pathLength: 0 }} animate={{ pathLength: 1 }}
                transition={{ duration: 1.2, ease: 'easeOut', delay: 0.3 }}
            />
            {/* Effort dots */}
            {effort.map((v, i) => (
                <motion.circle key={i} cx={toX(i / (effort.length - 1))} cy={toY(v)} r="3.5" fill={areaColor}
                    initial={{ scale: 0 }} animate={{ scale: 1 }} transition={{ delay: 0.2 * i + 0.3 }}
                />
            ))}
            {/* Y-axis labels */}
            <text x={padL + 2} y={toY(1.0) - 4} fontSize="9" fill="#a1a1aa" fontWeight="600">High</text>
            <text x={padL + 2} y={toY(0) - 4} fontSize="9" fill="#a1a1aa" fontWeight="600">Low</text>
            {/* Month labels */}
            {months.map((m, i) => (
                <text key={m} x={toX(i / (months.length - 1))} y={toY(0) + 14} fontSize="9" fill="#a1a1aa" textAnchor="middle" fontWeight="600">{m}</text>
            ))}
            {/* Phase labels */}
            {phases.map((p, i) => (
                <text key={i} x={toX((p.x1 + p.x2) / 2)} y={toY(0) + 28} fontSize="8" fill={p.color} textAnchor="middle" fontWeight="700">{p.label}</text>
            ))}
            {/* Chart label */}
            <text x={W / 2} y={14} fontSize="11" fill="#71717a" textAnchor="middle" fontWeight="700">{label}</text>
            {/* Legend */}
            <line x1={W - padR - 88} x2={W - padR - 72} y1={14} y2={14} stroke={areaColor} strokeWidth="2" />
            <text x={W - padR - 68} y={17} fontSize="8" fill="#a1a1aa">Effort</text>
            <line x1={W - padR - 44} x2={W - padR - 28} y1={14} y2={14} stroke={stressColor} strokeWidth="1.5" strokeDasharray="4 2" />
            <text x={W - padR - 24} y={17} fontSize="8" fill="#a1a1aa">Stress</text>
        </svg>
    );

    return (
        <div className="my-10 p-6 md:p-10 bg-white dark:bg-zinc-800 rounded-xl border border-zinc-200 dark:border-zinc-700">
            <h4 className="font-serif text-2xl font-semibold text-zinc-800 dark:text-white text-center">The Planning Paradox</h4>
            <p className="text-center text-sm text-zinc-500 dark:text-zinc-400 mb-6">Two students. Same 6 months. Opposite strategies.</p>

            {!revealed ? (
                <div className="text-center">
                    <p className="text-sm text-zinc-500 dark:text-zinc-400 mb-4">Most students start at the beginning and plan forward. What does that effort curve actually look like?</p>
                    <button onClick={() => setRevealed(true)} className="px-5 py-2.5 text-sm font-bold rounded-lg bg-sky-500 text-white hover:bg-sky-600 transition-colors">
                        Reveal the Paradox
                    </button>
                </div>
            ) : (
                <motion.div initial={{ opacity: 0, y: 12 }} animate={{ opacity: 1, y: 0 }} transition={{ duration: 0.4 }}>
                    <div className="grid md:grid-cols-2 gap-4 mb-5">
                        <div className="rounded-lg border border-rose-200 dark:border-rose-900 bg-rose-50/50 dark:bg-rose-950/20 p-3">
                            <Chart effort={fwdEffort} stress={fwdStress} phases={fwdPhases}
                                areaColor="#ef4444" areaId="fwd-grad" stressColor="#f59e0b" label="Forward Planner" />
                        </div>
                        <div className="rounded-lg border border-emerald-200 dark:border-emerald-900 bg-emerald-50/50 dark:bg-emerald-950/20 p-3">
                            <Chart effort={revEffort} stress={revStress} phases={revPhases}
                                areaColor="#10b981" areaId="rev-grad" stressColor="#f59e0b" label="Reverse Planner" />
                        </div>
                    </div>
                    <div className="grid md:grid-cols-2 gap-4 text-sm">
                        <div className="flex items-start gap-2.5 p-3 rounded-lg bg-rose-50 dark:bg-rose-950/30 border border-rose-200 dark:border-rose-900">
                            <span className="text-rose-500 text-lg mt-0.5">&#x2716;</span>
                            <p className="text-zinc-600 dark:text-zinc-300"><strong className="text-rose-600 dark:text-rose-400">Low effort early</strong> feels comfortable but creates a debt. Stress explodes in the final weeks when it's too late to fill gaps.</p>
                        </div>
                        <div className="flex items-start gap-2.5 p-3 rounded-lg bg-emerald-50 dark:bg-emerald-950/30 border border-emerald-200 dark:border-emerald-900">
                            <span className="text-emerald-500 text-lg mt-0.5">&#x2714;</span>
                            <p className="text-zinc-600 dark:text-zinc-300"><strong className="text-emerald-600 dark:text-emerald-400">Front-loaded effort</strong> feels harder at first, but stress decreases over time. You arrive at the exam rested and confident.</p>
                        </div>
                    </div>
                </motion.div>
            )}
        </div>
    );
};

const BackwardDesignSorter = () => {
    const [items, setItems] = useState([
        { id: 1, text: "Determine Acceptable Evidence (Mocks)", stage: 2 },
        { id: 2, text: "Identify Desired Results (The Goal)", stage: 1 },
        { id: 3, text: "Plan Learning Experiences (The Study)", stage: 3 },
    ]);
    return(
        <div className="my-10 p-8 md:p-12 bg-white dark:bg-zinc-800 rounded-xl border border-zinc-200 dark:border-zinc-700">
             <h4 className="font-serif text-2xl font-semibold text-zinc-800 dark:text-white text-center">Backward Design Protocol</h4>
             <p className="text-center text-sm text-zinc-500 dark:text-zinc-400 mb-8">Drag the steps into the correct order for a reverse-engineered plan.</p>
             <Reorder.Group axis="y" values={items} onReorder={setItems} className="space-y-3 max-w-sm mx-auto">
                {items.map((item, i) => (
                    <Reorder.Item key={item.id} value={item} className={`p-4 rounded-xl shadow-sm flex items-center gap-4 cursor-grabbing border ${item.stage === i + 1 ? 'bg-emerald-50 border-emerald-300' : 'bg-zinc-50 border-zinc-200 dark:border-zinc-700'}`}>
                        <span className={`font-semibold text-2xl ${item.stage === i + 1 ? 'text-emerald-500' : 'text-zinc-300'}`}>{i + 1}</span>
                        <span className="font-bold text-zinc-700 dark:text-zinc-200">{item.text}</span>
                    </Reorder.Item>
                ))}
             </Reorder.Group>
        </div>
    );
};

const ImplementationChecklist = () => {
    const initialItems = [
        { id: 'd-day', text: 'Identify D-Day (Exam Date)', checked: false },
        { id: 'taper', text: 'Define the Taper Period (Final Week)', checked: false },
        { id: 'inventory', text: 'Syllabus Inventory & Breakdown', checked: false },
        { id: 'buffer', text: 'Apply the Buffer (Subtract 20% of time)', checked: false },
        { id: 'critical-path', text: 'Map the Critical Path (Hardest topics first)', checked: false },
        { id: 'mocks', text: 'Schedule Mock Exams', checked: false },
        { id: 'frog', text: 'Schedule "The Frog" (Most hated subject)', checked: false },
    ];
    const [items, setItems] = useState(initialItems);
    const toggleCheck = (id: string) => setItems(items.map(item => item.id === id ? {...item, checked: !item.checked} : item));
    const progress = (items.filter(i => i.checked).length / items.length) * 100;

    return (
        <div className="my-10 p-8 md:p-12 bg-white dark:bg-zinc-800 rounded-xl border border-zinc-200 dark:border-zinc-700">
            <h4 className="font-serif text-2xl font-semibold text-zinc-800 dark:text-white text-center">Implementation Checklist</h4>
             <p className="text-center text-sm text-zinc-500 dark:text-zinc-400 mb-8">Follow these steps to build your own reverse-engineered schedule.</p>
             <div className="space-y-3 mb-6">
                {items.map(item => (
                    <div key={item.id} onClick={() => toggleCheck(item.id)} className={`p-4 rounded-xl flex items-center gap-4 cursor-pointer border transition-all ${item.checked ? 'bg-sky-50 border-sky-200' : 'bg-zinc-50 border-zinc-200 dark:border-zinc-700'}`}>
                        <div className={`w-6 h-6 rounded-md flex items-center justify-center ${item.checked ? 'bg-sky-500 text-white' : 'bg-zinc-200'}`}>
                            {item.checked && <CheckCircle2 size={14}/>}
                        </div>
                        <span className={`font-bold text-sm ${item.checked ? 'text-zinc-500 dark:text-zinc-400 line-through' : 'text-zinc-700 dark:text-zinc-200'}`}>{item.text}</span>
                    </div>
                ))}
             </div>
             <div className="w-full h-2 bg-zinc-100 dark:bg-zinc-800 rounded-full"><motion.div className="h-full bg-sky-500 rounded-full" animate={{width: `${progress}%`}} /></div>
        </div>
    );
}

// --- MODULE COMPONENT ---
const ReverseEngineeringModule: React.FC<{ onBack: () => void; progress: ModuleProgress; onProgressUpdate: (progress: ModuleProgress) => void }> = ({ onBack, progress, onProgressUpdate }) => {
  const sections = [
    { id: 'paradox', title: 'The Chronological Paradox', eyebrow: '01 // The Problem', icon: History },
    { id: 'engine', title: 'The Theoretical Engine', eyebrow: '02 // Why It Works', icon: DraftingCompass },
    { id: 'deconstruction', title: 'The Deconstruction Phase', eyebrow: '03 // The Inventory', icon: ClipboardList },
    { id: 'phasing', title: 'The Strategic Phases', eyebrow: '04 // The Timeline', icon: Layers },
    { id: 'optimization', title: 'Cognitive Optimization', eyebrow: '05 // The Science', icon: BrainCircuit },
    { id: 'blueprint', title: 'The Resilient Blueprint', eyebrow: '06 // The Plan', icon: Shield },
  ];

  return (
    <ModuleLayout
      moduleNumber="03"
      moduleTitle="Reverse Engineering"
      moduleSubtitle="The Temporal Architecture Protocol"
      moduleDescription="Ditch the failed 'start-to-finish' study plan. Learn to plan backwards from your exam date to create a realistic, resilient, and effective study schedule."
      theme={theme}
      sections={sections}
      onBack={onBack}
      progress={progress}
      onProgressUpdate={onProgressUpdate}
    >
      {(activeSection) => (
        <>
          {activeSection === 0 && (
            <ReadingSection title="The Chronological Paradox." eyebrow="Step 1" icon={History} theme={theme}>
              <p>The logical way to plan is to start at the beginning and work forward. It's also the reason most study plans fail. This forward-facing approach is a victim of the <Highlight description="The cognitive bias where we underestimate how long a task will take, assuming a 'best-case scenario' future with no interruptions." theme={theme}>Planning Fallacy</Highlight>. It ignores illness, fatigue, and life, leading to the infamous "student syndrome"--cramming everything into the final weeks.</p>
              <p>The solution is to invert the planning vector. Instead of asking "What should I do today?", you ask "To be ready for the exam, where must I be the day before?". This is <Highlight description="A project management methodology that starts with the fixed end-date and works backward to the present, revealing dependencies and creating a more realistic timeline." theme={theme}>Reverse Engineering</Highlight>. You anchor your plan to the non-negotiable end date and build backward, forcing a confrontation with reality.</p>
              <PlanningParadoxVisualizer />
            </ReadingSection>
          )}
           {activeSection === 1 && (
            <ReadingSection title="The Theoretical Engine." eyebrow="Step 2" icon={DraftingCompass} theme={theme}>
              <p>Reverse engineering isn't just a hack; it's a powerful framework built on three proven theories. From education, it uses <Highlight description="A curriculum design framework that starts with the end goal (the assessment) and works backward to design the learning activities." theme={theme}>Backward Design</Highlight>, ensuring every study session is directly linked to exam performance. It eliminates "junk volume"--study that feels productive but scores no marks.</p>
              <p>From project management, it uses the <Highlight description="A method for scheduling complex projects. It identifies the longest chain of dependent tasks (the 'critical path') that determines the project's total duration." theme={theme}>Critical Path Method (CPM)</Highlight> to map out dependencies. You can't learn Calculus before Algebra; Algebra is on the critical path. From psychology, it uses <Highlight description="The act of visualizing a future goal and working backward. This makes the required steps seem more necessary and increases motivation." theme={theme}>Future Retrospection</Highlight> to build motivation by creating a "memory of the future."</p>
              <BackwardDesignSorter />
            </ReadingSection>
          )}
          {activeSection === 2 && (
            <ReadingSection title="The Deconstruction Phase." eyebrow="Step 3" icon={ClipboardList} theme={theme}>
              <p>Before you can build a schedule, you must deconstruct the curriculum. The process begins by establishing the <Highlight description="The exam date itself. This is the immovable point from which all backward planning begins." theme={theme}>Fixed Anchor</Highlight>. You must also define your <Highlight description="The final 1-2 weeks before the exam, which are reserved for maintenance, sleep regulation, and confidence preservation--not new learning." theme={theme}>"Taper" Period</Highlight>.</p>
              <p>Next, you conduct a <Highlight description="The process of breaking down the entire syllabus into 'atomic units' of study, each representing a 45-90 minute session." theme={theme}>Grand Inventory</Highlight> of the syllabus. A topic like "Cell Biology" is too big; it must be broken down into "Mitochondria," "Osmosis," etc. Finally, you apply the <Highlight description="The 80/20 rule. By analyzing past papers, you identify the 20% of topics that deliver 80% of the marks. These are your high-yield assets." theme={theme}>Pareto Principle</Highlight> to prioritize high-yield topics.</p>
            </ReadingSection>
          )}
           {activeSection === 3 && (
            <ReadingSection title="The Strategic Phases." eyebrow="Step 4" icon={Layers} theme={theme}>
                <p>A reverse-engineered schedule is not a solid block of "study." It is segmented into distinct operational phases, each with a specific goal. Working backward from the exam, the timeline looks like this:</p>
                <p><strong>Phase 4: Taper & Maintenance (Final 2 Weeks):</strong> No new material. Focus on light review, sleep, and stress management. <strong>Phase 3: Simulation & Conditioning (Months 1-2 Pre-Exam):</strong> Full-length mock exams to build stamina and refine technique. <strong>Phase 2: Consolidation & Interleaving (Months 3-4 Pre-Exam):</strong> Move from blocked to mixed practice, deepening connections. <strong>Phase 1: Foundation & Acquisition (Months 5-6 Pre-Exam):</strong> First-pass learning and creating revision assets (e.g., flashcards).</p>
            </ReadingSection>
          )}
           {activeSection === 4 && (
            <ReadingSection title="Cognitive Optimization." eyebrow="Step 5" icon={BrainCircuit} theme={theme}>
              <p>A great schedule doesn't just plan *what* you study; it plans *how* you study. It integrates cognitive science directly into the timeline. It must schedule <Highlight description="Reviewing material at increasing intervals to counteract the Forgetting Curve." theme={theme}>Spaced Repetition</Highlight>, creating "return trips" to old material.</p>
              <p>It must prioritize <Highlight description="Forcing your brain to retrieve information (e.g., practice testing) rather than passively re-reading it. This is the engine of long-term memory." theme={theme}>Active Recall</Highlight> ("Output") over passive review ("Input"). And it should favour <Highlight description="Mixing different topics or subjects within a study session. This feels harder but trains the crucial skill of 'problem spotting'." theme={theme}>Interleaving</Highlight> over blocked practice, especially in the later phases, to build flexible, exam-ready knowledge.</p>
            </ReadingSection>
          )}
           {activeSection === 5 && (
            <ReadingSection title="The Resilient Blueprint." eyebrow="Step 6" icon={Shield} theme={theme}>
              <p>A perfect, rigid schedule is a fragile schedule. It will shatter the first time you get sick or have a family event. A resilient schedule is designed to fail gracefully. This requires building in <Highlight description="Intentionally blank weeks (10-20% of your total time) that can absorb disruptions without derailing the entire plan." theme={theme}>Buffer Weeks</Highlight>.</p>
              <p>Before you begin, you must conduct a <Highlight description="Identifying all fixed life events (holidays, weddings, etc.) and 'blacking them out' of your available time from the start." theme={theme}>"Non-Negotiables" Audit</Highlight>. Finally, you must choose your tool. Whether it's a digital <Highlight description="A project management tool that visualizes tasks on a timeline, making dependencies clear." theme={theme}>Gantt Chart</Highlight>, a Notion template, or an analog wall with sticky notes, the tool must make the timeline, dependencies, and critical path visible. You are now ready to build your schedule.</p>
              <ImplementationChecklist />
            </ReadingSection>
          )}
        </>
      )}
    </ModuleLayout>
  );
};
export default ReverseEngineeringModule;
