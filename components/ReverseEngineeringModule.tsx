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
    const [plan, setPlan] = useState<'forward' | 'reverse' | null>(null);
    return (
        <div className="my-10 p-8 md:p-12 bg-white rounded-[3rem] border border-stone-200 shadow-xl">
            <h4 className="font-serif text-2xl font-semibold text-stone-800 text-center italic">The Planning Paradox</h4>
            <p className="text-center text-sm text-stone-500 mb-6">How does your effort get distributed over 6 months?</p>
            <div className="flex justify-center gap-3 mb-6">
                <button onClick={() => setPlan('forward')} className={`px-4 py-2 text-sm font-bold rounded-lg border-2 ${plan === 'forward' ? 'bg-rose-500 text-white border-rose-500' : 'bg-rose-50 text-rose-800 border-rose-200'}`}>Forward Plan</button>
                <button onClick={() => setPlan('reverse')} className={`px-4 py-2 text-sm font-bold rounded-lg border-2 ${plan === 'reverse' ? 'bg-emerald-500 text-white border-emerald-500' : 'bg-emerald-50 text-emerald-800 border-emerald-200'}`}>Reverse Plan</button>
            </div>
            <div className="w-full h-10 bg-stone-100 rounded-lg">
                <motion.div
                    className={`h-full rounded-lg ${plan === 'forward' ? 'bg-rose-500' : 'bg-emerald-500'}`}
                    initial={{ width: '0%', clipPath: 'polygon(0 0, 0% 0, 0% 100%, 0% 100%)' }}
                    animate={plan === 'forward' ? { width: '100%', clipPath: ['polygon(0 0, 0% 0, 0% 100%, 0% 100%)', 'polygon(0 0, 10% 0, 95% 100%, 0% 100%)', 'polygon(0 0, 100% 0, 100% 100%, 0% 100%)']} : { width: '100%', clipPath: 'polygon(0 0, 100% 0, 100% 100%, 0% 100%)'}}
                    transition={{ duration: 2, ease: 'easeInOut', times: [0, 0.8, 1]}}
                />
            </div>
            <div className="grid grid-cols-3 text-xs text-stone-400 mt-2"><span>Start</span><span className="text-center">Mid-Point</span><span className="text-right">Exam</span></div>
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
        <div className="my-10 p-8 md:p-12 bg-white rounded-[3rem] border border-stone-200 shadow-xl">
             <h4 className="font-serif text-2xl font-semibold text-stone-800 text-center italic">Backward Design Protocol</h4>
             <p className="text-center text-sm text-stone-500 mb-8">Drag the steps into the correct order for a reverse-engineered plan.</p>
             <Reorder.Group axis="y" values={items} onReorder={setItems} className="space-y-3 max-w-sm mx-auto">
                {items.map((item, i) => (
                    <Reorder.Item key={item.id} value={item} className={`p-4 rounded-xl shadow-sm flex items-center gap-4 cursor-grabbing border ${item.stage === i + 1 ? 'bg-emerald-50 border-emerald-300' : 'bg-stone-50 border-stone-200'}`}>
                        <span className={`font-semibold text-2xl ${item.stage === i + 1 ? 'text-emerald-500' : 'text-stone-300'}`}>{i + 1}</span>
                        <span className="font-bold text-stone-700">{item.text}</span>
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
        <div className="my-10 p-8 md:p-12 bg-white rounded-[3rem] border border-stone-200 shadow-xl">
            <h4 className="font-serif text-2xl font-semibold text-stone-800 text-center italic">Implementation Checklist</h4>
             <p className="text-center text-sm text-stone-500 mb-8">Follow these steps to build your own reverse-engineered schedule.</p>
             <div className="space-y-3 mb-6">
                {items.map(item => (
                    <div key={item.id} onClick={() => toggleCheck(item.id)} className={`p-4 rounded-xl flex items-center gap-4 cursor-pointer border-2 transition-all ${item.checked ? 'bg-sky-50 border-sky-200' : 'bg-stone-50 border-stone-200'}`}>
                        <div className={`w-6 h-6 rounded-md flex items-center justify-center ${item.checked ? 'bg-sky-500 text-white' : 'bg-stone-200'}`}>
                            {item.checked && <CheckCircle2 size={14}/>}
                        </div>
                        <span className={`font-bold text-sm ${item.checked ? 'text-stone-500 line-through' : 'text-stone-700'}`}>{item.text}</span>
                    </div>
                ))}
             </div>
             <div className="w-full h-2 bg-stone-100 rounded-full"><motion.div className="h-full bg-sky-500 rounded-full" animate={{width: `${progress}%`}} /></div>
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
      moduleNumber="02"
      moduleTitle="Reverse Engineering"
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
