/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
*/

import React, { useState } from 'react';
import { motion, Reorder } from 'framer-motion';
import { CheckCircle2, History, DraftingCompass, ClipboardList, Layers, BrainCircuit, Shield } from 'lucide-react';
import { type ModuleProgress } from '../types';
import { skyTheme } from '../moduleThemes';
import { Highlight, ReadingSection, PersonalStory, ToolJumpCard } from './ModuleShared';
import { ModuleLayout } from './ModuleLayout';
import { useEssentialsMode } from '../hooks/useEssentialsMode';

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
        <div className="my-10 rounded-2xl p-6 md:p-8" style={{ backgroundColor: '#F8F8F8', borderRadius: 18 }}>
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
        { id: 1, text: "Decide how you'll test yourself (Mocks)", stage: 2 },
        { id: 2, text: "Set your target grade (The Goal)", stage: 1 },
        { id: 3, text: "Plan your actual study sessions (The Study)", stage: 3 },
    ]);
    return(
        <div className="my-10 rounded-2xl p-6 md:p-8" style={{ backgroundColor: '#F8F8F8', borderRadius: 18 }}>
             <h4 className="font-serif text-2xl font-semibold text-zinc-800 dark:text-white text-center">Plan It Backwards</h4>
             <p className="text-center text-sm text-zinc-500 dark:text-zinc-400 mb-8">Drag the steps into the correct order for a backwards study plan.</p>
             <Reorder.Group axis="y" values={items} onReorder={setItems} className="space-y-3 max-w-sm mx-auto">
                {items.map((item, i) => (
                    <Reorder.Item
                        key={item.id}
                        value={item}
                        className="p-4 flex items-center gap-4 cursor-grab active:cursor-grabbing"
                        style={item.stage === i + 1
                            ? { backgroundColor: '#D1FAE5', border: '2.5px solid #059669', borderRadius: 16, boxShadow: '4px 4px 0px 0px #059669' }
                            : { backgroundColor: '#FFFFFF', border: '2.5px solid #1C1917', borderRadius: 16, boxShadow: '4px 4px 0px 0px #1C1917' }
                        }
                        whileDrag={{ scale: 1.03, y: -2, boxShadow: '6px 6px 0px 0px #1C1917' }}
                    >
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
        { id: 'd-day', text: 'Write down your exam date', checked: false },
        { id: 'taper', text: 'Block off the final week for light review only', checked: false },
        { id: 'inventory', text: 'Break the syllabus into small study chunks', checked: false },
        { id: 'buffer', text: 'Leave 20% of your time blank for unexpected stuff', checked: false },
        { id: 'critical-path', text: 'Put the hardest topics first', checked: false },
        { id: 'mocks', text: 'Schedule your mock exams', checked: false },
        { id: 'frog', text: 'Schedule your most dreaded subject early in the week', checked: false },
    ];
    const [items, setItems] = useState(initialItems);
    const toggleCheck = (id: string) => setItems(items.map(item => item.id === id ? {...item, checked: !item.checked} : item));
    const progress = (items.filter(i => i.checked).length / items.length) * 100;

    return (
        <div className="my-10 rounded-2xl p-6 md:p-8" style={{ backgroundColor: '#F8F8F8', borderRadius: 18 }}>
            <h4 className="font-serif text-2xl font-semibold text-zinc-800 dark:text-white text-center">Your Schedule Checklist</h4>
             <p className="text-center text-sm text-zinc-500 dark:text-zinc-400 mb-8">Follow these steps to build your own backwards study schedule.</p>
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
  const essentials = useEssentialsMode();
  const sections = [
    { id: 'paradox', title: 'Why Most Study Plans Fail', eyebrow: '01 // The Problem', icon: History },
    { id: 'engine', title: 'Why Planning Backwards Works', eyebrow: '02 // The Idea', icon: DraftingCompass },
    { id: 'deconstruction', title: 'Breaking Down the Syllabus', eyebrow: '03 // The Inventory', icon: ClipboardList },
    { id: 'phasing', title: 'Your Four Study Phases', eyebrow: '04 // The Timeline', icon: Layers },
    { id: 'optimization', title: 'Studying Smarter', eyebrow: '05 // The Science', icon: BrainCircuit },
    { id: 'blueprint', title: 'Making a Plan That Actually Lasts', eyebrow: '06 // Your Plan', icon: Shield },
  ];

  return (
    <ModuleLayout
      moduleNumber="03"
      moduleTitle="Reverse Engineering"
      moduleSubtitle="Plan Backwards, Get Ahead"
      moduleDescription="Most study plans fall apart within weeks. This module shows you how to start from your exam date and work backwards to build a schedule that actually holds up."
      theme={theme}
      sections={sections}
      onBack={onBack}
      progress={progress}
      onProgressUpdate={onProgressUpdate}
      finishButtonText="Set Your Countdown"
    >
      {(activeSection) => (
        <>
          {activeSection === 0 && (
            <ReadingSection title="Why Most Study Plans Fail." eyebrow="Step 1" icon={History} theme={theme}>
              {essentials ? (
                <>
                  <p>Planning forward feels obvious. It is also why most plans fail. You fall into the <Highlight description="We are naturally bad at guessing how long things take. We picture the best-case scenario and forget about sick days, tiredness, and life getting in the way." theme={theme}>Planning Fallacy</Highlight>. You underestimate how long things take. Everything piles up at the end. The fix: use <Highlight description="Instead of planning from today forward, you start at your exam date and work backwards to today. It forces you to face how much time you really have." theme={theme}>Reverse Engineering</Highlight>. Start from your exam date and work backwards. It forces you to face reality from day one.</p>
                </>
              ) : (
                <>
                  <p>Starting at the beginning and working forward seems like the obvious way to plan. It is also the main reason most study plans fall apart. The problem is the <Highlight description="We are naturally bad at guessing how long things take. We picture the best-case scenario and forget about sick days, tiredness, and life getting in the way." theme={theme}>Planning Fallacy</Highlight> -- we are terrible at guessing how long things will really take. We forget about sick days, tiredness, and just life getting in the way. So everything piles up at the end, and you are left cramming the week before.</p>
                  <p>The fix is surprisingly simple: plan backwards instead. Instead of asking "What should I do today?", ask "To be ready for the exam, where do I need to be the day before?". That is <Highlight description="Instead of planning from today forward, you start at your exam date and work backwards to today. It forces you to face how much time you really have." theme={theme}>Reverse Engineering</Highlight>. You start from your exam date -- which is not moving -- and work backwards. It forces you to face reality from day one.</p>
                </>
              )}
              <PlanningParadoxVisualizer />
            </ReadingSection>
          )}
           {activeSection === 1 && (
            <ReadingSection title="Why Planning Backwards Works." eyebrow="Step 2" icon={DraftingCompass} theme={theme}>
              {essentials ? (
                <>
                  <p>Three reasons this works. First: <Highlight description="Start with what you will be tested on, then plan your study around that. Every session has a clear purpose tied to the exam." theme={theme}>Backward Design</Highlight>. Start with what the exam tests. Plan every session around that. No "junk study." Second: you spot the <Highlight description="Some topics depend on others. For example, you cannot do Calculus without Algebra. The chain of topics you must cover first is the critical path." theme={theme}>Critical Path</Highlight>. Some topics depend on others. You cannot do Calculus before Algebra. Third: <Highlight description="When you imagine yourself at the finish line and trace the steps back, those steps feel more real and necessary. It is a motivation boost." theme={theme}>Future Thinking</Highlight>. Picturing exam day makes each step feel necessary and keeps you motivated.</p>
                </>
              ) : (
                <>
                  <p>Planning backwards is not just a clever trick -- there are solid reasons it works so well. First, it uses a simple idea called <Highlight description="Start with what you will be tested on, then plan your study around that. Every session has a clear purpose tied to the exam." theme={theme}>Backward Design</Highlight>: start with what the exam will actually test, and plan every study session around that. This cuts out "junk study" -- the kind that feels productive but does not actually earn you marks.</p>
                  <p>Second, it helps you spot the <Highlight description="Some topics depend on others. For example, you cannot do Calculus without Algebra. The chain of topics you must cover first is the critical path." theme={theme}>Critical Path</Highlight> -- the chain of topics where one depends on another. You cannot do Calculus before Algebra, so Algebra goes first. Third, by picturing yourself on exam day and working backwards, you create what is called <Highlight description="When you imagine yourself at the finish line and trace the steps back, those steps feel more real and necessary. It is a motivation boost." theme={theme}>Future Thinking</Highlight> -- it makes each step feel necessary and keeps you motivated because you can see exactly how it connects to the finish line.</p>
                </>
              )}
              <BackwardDesignSorter />
            </ReadingSection>
          )}
          {activeSection === 2 && (
            <ReadingSection title="Breaking Down the Syllabus." eyebrow="Step 3" icon={ClipboardList} theme={theme}>
              {essentials ? (
                <>
                  <p>Lock in your <Highlight description="Your exam date. It is not moving, so everything gets planned around it." theme={theme}>Exam Date</Highlight>. Block off a <Highlight description="The last week or two before the exam. You keep these for light review, sleep, and calming your nerves -- no cramming new stuff." theme={theme}>"Wind-Down" Period</Highlight> in the final two weeks. No new material then. Do a full <Highlight description="Go through every topic on the syllabus and break it into small chunks, each about one study session long (45-90 minutes)." theme={theme}>Syllabus Breakdown</Highlight>. Break every topic into chunks of one study session each. Use past papers to find the <Highlight description="Look at past papers and you will notice that roughly 20% of topics come up for about 80% of the marks. Focus your energy there first." theme={theme}>80/20 Rule</Highlight>. About 20% of topics earn 80% of the marks. Hit those first.</p>
                </>
              ) : (
                <>
                  <p>Before you build a schedule, you need to know exactly what you are dealing with. Start by locking in your <Highlight description="Your exam date. It is not moving, so everything gets planned around it." theme={theme}>Exam Date</Highlight> -- that is your finish line and it is not moving. Then block off a <Highlight description="The last week or two before the exam. You keep these for light review, sleep, and calming your nerves -- no cramming new stuff." theme={theme}>"Wind-Down" Period</Highlight> in the final week or two for light review, sleep, and calming your nerves -- not learning new material.</p>
                  <p>Next, do a full <Highlight description="Go through every topic on the syllabus and break it into small chunks, each about one study session long (45-90 minutes)." theme={theme}>Syllabus Breakdown</Highlight>. Go through every topic and break it into bite-sized chunks, each about one study session long. "Cell Biology" is too vague -- break it into "Mitochondria," "Osmosis," and so on. Then use past papers to figure out the <Highlight description="Look at past papers and you will notice that roughly 20% of topics come up for about 80% of the marks. Focus your energy there first." theme={theme}>80/20 Rule</Highlight>: roughly 20% of topics earn about 80% of the marks. Those are the ones you hit first.</p>
                  <PersonalStory name="Caoimhe" role="Leaving Cert student, Limerick">
                    <p>"I had this massive colour-coded timetable on my wall in January and felt so organised. By mid-February it was already in the bin. I was behind on everything and it just made me feel worse. When I tried planning backwards from the exam instead, I actually finished a topic ahead of schedule for the first time. It was such a relief to have a plan that worked with real life, not against it."</p>
                  </PersonalStory>
                </>
              )}
            </ReadingSection>
          )}
           {activeSection === 3 && (
            <ReadingSection title="Your Four Study Phases." eyebrow="Step 4" icon={Layers} theme={theme}>
                {essentials ? (
                  <p>Your schedule has four phases, working backwards. Phase 4 (final 2 weeks): light review and rest only. Phase 3 (1-2 months before): full mock papers under timed conditions. Phase 2 (3-4 months before): mix different topics together. Phase 1 (5-6 months before): learn the basics and make your revision materials. Each phase has a clear job.</p>
                ) : (
                  <p>A good backwards schedule is not just one big block of "study." It is split into four clear phases, each with its own job. Working backwards from the exam, here is what it looks like:</p>
                )}
                <div className="my-10 rounded-2xl p-5 md:p-6 space-y-3" style={{ backgroundColor: '#F8F8F8', borderRadius: 18 }}>
                  {/* Card 1 — Sky */}
                  <div className="p-4 flex items-start gap-4" style={{ backgroundColor: '#93C5FD', border: '2.5px solid #2563EB', borderRadius: 16, boxShadow: '4px 4px 0px 0px #2563EB' }}>
                    <div className="w-11 h-11 rounded-xl flex items-center justify-center shrink-0 text-lg font-serif font-bold text-white" style={{ backgroundColor: '#2563EB' }}>1</div>
                    <div>
                      <p className="text-sm font-bold" style={{ color: '#1E3A8A' }}>Phase 4: Wind Down (Final 2 Weeks)</p>
                      <p className="text-[13px] mt-0.5" style={{ color: '#1E3A8A', opacity: 0.8 }}>No new material. Light review, plenty of sleep, and keeping your nerves in check.</p>
                    </div>
                  </div>
                  {/* Card 2 — Sunshine */}
                  <div className="p-4 flex items-start gap-4" style={{ backgroundColor: '#FCD34D', border: '2.5px solid #D97706', borderRadius: 16, boxShadow: '4px 4px 0px 0px #D97706' }}>
                    <div className="w-11 h-11 rounded-xl flex items-center justify-center shrink-0 text-lg font-serif font-bold text-white" style={{ backgroundColor: '#D97706' }}>2</div>
                    <div>
                      <p className="text-sm font-bold" style={{ color: '#78350F' }}>Phase 3: Practice Exams (Months 1-2 Before the Exam)</p>
                      <p className="text-[13px] mt-0.5" style={{ color: '#78350F', opacity: 0.8 }}>Full mock papers under timed conditions to build stamina and sharpen your technique.</p>
                    </div>
                  </div>
                  {/* Card 3 — Peach */}
                  <div className="p-4 flex items-start gap-4" style={{ backgroundColor: '#FDBA74', border: '2.5px solid #EA580C', borderRadius: 16, boxShadow: '4px 4px 0px 0px #EA580C' }}>
                    <div className="w-11 h-11 rounded-xl flex items-center justify-center shrink-0 text-lg font-serif font-bold text-white" style={{ backgroundColor: '#EA580C' }}>3</div>
                    <div>
                      <p className="text-sm font-bold" style={{ color: '#7C2D12' }}>Phase 2: Mix and Deepen (Months 3-4 Before the Exam)</p>
                      <p className="text-[13px] mt-0.5" style={{ color: '#7C2D12', opacity: 0.8 }}>Start mixing topics together instead of studying one at a time -- this builds the flexible thinking the exam demands.</p>
                    </div>
                  </div>
                  {/* Card 4 — Mint */}
                  <div className="p-4 flex items-start gap-4" style={{ backgroundColor: '#6EE7B7', border: '2.5px solid #059669', borderRadius: 16, boxShadow: '4px 4px 0px 0px #059669' }}>
                    <div className="w-11 h-11 rounded-xl flex items-center justify-center shrink-0 text-lg font-serif font-bold text-white" style={{ backgroundColor: '#059669' }}>4</div>
                    <div>
                      <p className="text-sm font-bold" style={{ color: '#064E3B' }}>Phase 1: Learn the Basics (Months 5-6 Before the Exam)</p>
                      <p className="text-[13px] mt-0.5" style={{ color: '#064E3B', opacity: 0.8 }}>First-pass learning and making your revision materials (flashcards, summaries, whatever works for you).</p>
                    </div>
                  </div>
                </div>
            </ReadingSection>
          )}
           {activeSection === 4 && (
            <ReadingSection title="Studying Smarter." eyebrow="Step 5" icon={BrainCircuit} theme={theme}>
              {essentials ? (
                <>
                  <p>Plan how you study, not just what you study. Use <Highlight description="Instead of cramming everything once, you go back and review old topics at growing intervals. It is the best way to stop yourself forgetting things." theme={theme}>Spaced Repetition</Highlight>. Go back to old topics at regular intervals. Use <Highlight description="Testing yourself -- writing answers, doing practice questions -- rather than just re-reading your notes. It feels harder but it is far more effective." theme={theme}>Active Recall</Highlight>. Test yourself instead of re-reading. Try <Highlight description="Mixing different topics in one study session instead of doing hours on the same thing. It feels messier but it trains your brain to spot which method to use -- exactly what exams test." theme={theme}>Mixing Topics</Highlight> in later phases. Study different subjects in one session. It feels harder but trains flexible thinking.</p>
                </>
              ) : (
                <>
                  <p>A great schedule does not just plan what you study -- it also plans how you study. You need to build in <Highlight description="Instead of cramming everything once, you go back and review old topics at growing intervals. It is the best way to stop yourself forgetting things." theme={theme}>Spaced Repetition</Highlight>, which means going back to old topics at regular intervals so they do not fade from your memory.</p>
                  <p>You should also prioritise <Highlight description="Testing yourself -- writing answers, doing practice questions -- rather than just re-reading your notes. It feels harder but it is far more effective." theme={theme}>Active Recall</Highlight> (testing yourself, writing answers) over passive re-reading. And in the later phases, try <Highlight description="Mixing different topics in one study session instead of doing hours on the same thing. It feels messier but it trains your brain to spot which method to use -- exactly what exams test." theme={theme}>Mixing Topics</Highlight> -- studying different subjects in one session. It feels harder, but it trains your brain to spot which approach to use, which is exactly what exam questions test.</p>
                </>
              )}
            </ReadingSection>
          )}
           {activeSection === 5 && (
            <ReadingSection title="Making a Plan That Actually Lasts." eyebrow="Step 6" icon={Shield} theme={theme}>
              {essentials ? (
                <>
                  <p>A rigid schedule breaks the first time life gets in the way. Leave <Highlight description="Blank days or weeks (about 10-20% of your total time) that are there on purpose. When life throws you a curveball, these soak it up without wrecking everything." theme={theme}>Buffer Time</Highlight>. Keep 10-20% of your time blank on purpose. Do a <Highlight description="Write down everything that is definitely happening -- holidays, birthdays, matches, family events -- and block them out from the start so you are not kidding yourself about how much time you have." theme={theme}>Life Check</Highlight>. Block out holidays, birthdays, and matches from the start. Pick any tool you like. The tool does not matter. What matters is seeing your whole plan at a glance.</p>
                </>
              ) : (
                <>
                  <p>A perfect, rigid schedule will fall apart the first time you get sick or have a family event. A schedule that actually lasts is one that is built to bend without breaking. That means leaving <Highlight description="Blank days or weeks (about 10-20% of your total time) that are there on purpose. When life throws you a curveball, these soak it up without wrecking everything." theme={theme}>Buffer Time</Highlight> -- blank days that are there on purpose so that when something comes up, your whole plan does not collapse.</p>
                  <p>Before you start filling in dates, do a quick <Highlight description="Write down everything that is definitely happening -- holidays, birthdays, matches, family events -- and block them out from the start so you are not kidding yourself about how much time you have." theme={theme}>Life Check</Highlight>: write down everything you know is coming up (holidays, birthdays, matches) and block those out straight away. Finally, pick your tool. It could be a <Highlight description="A simple chart that shows your tasks on a timeline so you can see what needs to happen and when." theme={theme}>Timeline Chart</Highlight> in a free app, a Notion page, or just a wall of sticky notes. The tool does not matter -- what matters is that you can see your whole plan at a glance. You are now ready to build your schedule.</p>
                </>
              )}
              <ImplementationChecklist />
              <ToolJumpCard
                toolId="war-room"
                title="Map your syllabus in the War Room"
                description="The War Room is the strategic version of this — break each subject into topics, set confidence levels, and let it tell you where to spend the next hour."
                ctaLabel="Open the War Room"
              />
            </ReadingSection>
          )}
        </>
      )}
    </ModuleLayout>
  );
};
export default ReverseEngineeringModule;
