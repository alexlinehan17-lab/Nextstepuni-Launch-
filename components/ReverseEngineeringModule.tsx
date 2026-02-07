
/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
*/

import React, { useState } from 'react';
import { motion, AnimatePresence, Reorder } from 'framer-motion';
import { 
  ArrowLeft, CheckCircle2, ArrowRight, 
  Lock, Flag, History, DraftingCompass, ClipboardList, Layers, BrainCircuit, Shield
} from 'lucide-react';

interface ReverseEngineeringModuleProps {
  onBack: () => void;
}

const Highlight = ({ children, description, color = "bg-sky-100/40", textColor = "text-sky-900", decorColor = "decoration-sky-400/40", hoverColor="hover:bg-sky-200/60" }: { children?: React.ReactNode, description: string, color?: string, textColor?: string, decorColor?: string, hoverColor?: string }) => {
  const [isOpen, setIsOpen] = useState(false);

  return (
    <span className="relative inline-block mx-0.5">
      <button 
        onClick={(e) => {
          e.stopPropagation();
          setIsOpen(!isOpen);
        }}
        className={`relative inline-flex items-center px-2 py-0.5 font-bold ${color} ${textColor} rounded-md cursor-help ${hoverColor} transition-all duration-300 ${decorColor} underline decoration-2 underline-offset-4`}
      >
        <span className="not-italic">{children}</span>
      </button>
      <AnimatePresence>
        {isOpen && (
          <>
            <div className="fixed inset-0 z-[60]" onClick={() => setIsOpen(false)} />
            <motion.div 
              initial={{ opacity: 0, scale: 0.9, y: 10, x: "-50%" }}
              animate={{ opacity: 1, scale: 1, y: 0, x: "-50%" }}
              exit={{ opacity: 0, scale: 0.9, y: 10, x: "-50%" }}
              className="absolute z-[70] bottom-full left-1/2 mb-6 w-72 p-6 bg-stone-900/95 text-white text-xs rounded-2xl shadow-2xl pointer-events-auto leading-relaxed border border-white/10 backdrop-blur-xl whitespace-normal text-left"
              style={{ transformOrigin: 'bottom center' }}
            >
              <div className="absolute bottom-0 left-1/2 -translate-x-1/2 translate-y-full w-0 h-0 border-l-[10px] border-l-transparent border-r-[10px] border-r-transparent border-t-[10px] border-t-stone-900/95"></div>
              <p className="font-sans font-bold text-sky-400 mb-2 uppercase tracking-[0.2em] text-[9px]">The Academic Insight</p>
              <p className="text-stone-200 font-medium">{description}</p>
            </motion.div>
          </>
        )}
      </AnimatePresence>
    </span>
  );
};

const ReadingSection = ({ title, eyebrow, icon: Icon, children }: { title: string, eyebrow: string, icon: any, children: React.ReactNode }) => (
  <article className="animate-fade-in">
    <header className="mb-12 text-left relative">
      <div className="absolute -left-16 top-0 hidden xl:block">
        <div className="w-12 h-12 rounded-2xl bg-stone-900 flex items-center justify-center text-sky-400 shadow-xl border border-white/10">
          <Icon size={24} />
        </div>
      </div>
      <span className="inline-flex items-center gap-2 px-3 py-1 bg-sky-50 text-sky-600 text-[10px] font-black tracking-[0.4em] uppercase rounded-full mb-4">
        {eyebrow}
      </span>
      <h2 className="font-serif text-4xl md:text-6xl leading-tight tracking-tighter text-stone-900 font-bold italic">
        {title}
      </h2>
    </header>
    <div className="prose prose-stone prose-lg max-w-none space-y-8 text-stone-600 leading-relaxed font-sans text-justify overflow-visible">
      {children}
    </div>
  </article>
);

const MicroCommitment = ({ children }: { children: React.ReactNode }) => (
  <div className="my-12 p-8 bg-sky-50/50 border-2 border-dashed border-sky-200 rounded-3xl">
    <div className="flex items-start gap-5">
      <div className="w-11 h-11 rounded-xl bg-sky-500 text-white flex items-center justify-center shrink-0 mt-1 shadow-lg shadow-sky-500/20">
        <Flag size={20} />
      </div>
      <div>
        <h4 className="font-bold text-sky-800 text-sm uppercase tracking-widest">Your Mission (Under 5 Mins)</h4>
        <div className="text-stone-600 mt-2 font-medium leading-relaxed">
          {children}
        </div>
      </div>
    </div>
  </div>
);

const ActivityRing = ({ progress, color = "#0ea5e9" }: { progress: number, color?: string }) => {
  const radius = 35;
  const circumference = 2 * Math.PI * radius;
  const offset = circumference - (progress / 100) * circumference;

  return (
    <div className="relative flex items-center justify-center w-24 h-24 mx-auto mb-4">
      <svg className="w-full h-full -rotate-90 overflow-visible" viewBox="0 0 96 96">
        <circle cx="48" cy="48" r={radius} stroke={color} strokeWidth="10" fill="transparent" className="opacity-10"/>
        <motion.circle cx="48" cy="48" r={radius} stroke={color} strokeWidth="10" fill="transparent" strokeDasharray={circumference} initial={{ strokeDashoffset: circumference }} animate={{ strokeDashoffset: offset }} transition={{ duration: 1.5, ease: "easeOut" }} strokeLinecap="round" style={{ filter: `drop-shadow(0 0 8px ${color}55)` }}/>
      </svg>
    </div>
  );
};

// --- INTERACTIVE COMPONENTS ---
const PlanningParadoxVisualizer = () => {
    const [plan, setPlan] = useState<'forward' | 'reverse' | null>(null);
    return (
        <div className="my-10 p-8 md:p-12 bg-white rounded-[3rem] border border-stone-200 shadow-xl">
            <h4 className="font-serif text-2xl font-bold text-stone-800 text-center italic">The Planning Paradox</h4>
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
             <h4 className="font-serif text-2xl font-bold text-stone-800 text-center italic">Backward Design Protocol</h4>
             <p className="text-center text-sm text-stone-500 mb-8">Drag the steps into the correct order for a reverse-engineered plan.</p>
             <Reorder.Group axis="y" values={items} onReorder={setItems} className="space-y-3 max-w-sm mx-auto">
                {items.map((item, i) => (
                    <Reorder.Item key={item.id} value={item} className={`p-4 rounded-xl shadow-sm flex items-center gap-4 cursor-grabbing border ${item.stage === i + 1 ? 'bg-emerald-50 border-emerald-300' : 'bg-stone-50 border-stone-200'}`}>
                        <span className={`font-black text-2xl ${item.stage === i + 1 ? 'text-emerald-500' : 'text-stone-300'}`}>{i + 1}</span>
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
            <h4 className="font-serif text-2xl font-bold text-stone-800 text-center italic">Implementation Checklist</h4>
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
export const ReverseEngineeringModule: React.FC<ReverseEngineeringModuleProps> = ({ onBack }) => {
  const [activeSection, setActiveSection] = useState(0);
  const [unlockedSection, setUnlockedSection] = useState(0);
  
  const sections = [
    { id: 'paradox', title: 'The Chronological Paradox', eyebrow: '01 // The Problem', icon: History },
    { id: 'engine', title: 'The Theoretical Engine', eyebrow: '02 // Why It Works', icon: DraftingCompass },
    { id: 'deconstruction', title: 'The Deconstruction Phase', eyebrow: '03 // The Inventory', icon: ClipboardList },
    { id: 'phasing', title: 'The Strategic Phases', eyebrow: '04 // The Timeline', icon: Layers },
    { id: 'optimization', title: 'Cognitive Optimization', eyebrow: '05 // The Science', icon: BrainCircuit },
    { id: 'blueprint', title: 'The Resilient Blueprint', eyebrow: '06 // The Plan', icon: Shield },
  ];

  const handleCompleteSection = () => {
    if (activeSection === unlockedSection && activeSection < sections.length - 1) {
      setUnlockedSection(activeSection + 1);
    }
    if (activeSection < sections.length - 1) {
      setActiveSection(activeSection + 1);
    } else {
      onBack();
    }
    window.scrollTo({ top: 0, behavior: 'smooth' });
  };

  const handleJumpToSection = (index: number) => {
    if (index <= unlockedSection) {
      setActiveSection(index);
      window.scrollTo({ top: 0, behavior: 'smooth' });
    }
  };

  const handlePrev = () => {
    if (activeSection > 0) {
      setActiveSection(activeSection - 1);
      window.scrollTo({ top: 0, behavior: 'smooth' });
    }
  };

  const progress = ((unlockedSection + 1) / sections.length) * 100;

  return (
    <div className="min-h-screen bg-[#FBFBF9] text-stone-900 font-sans flex flex-col md:flex-row overflow-x-hidden">
      <aside className="w-full md:w-80 bg-white border-r border-stone-200 sticky top-0 md:h-screen z-40 p-8 flex flex-col">
        <div className="flex items-center gap-4 mb-12">
          <motion.button whileHover={{ scale: 1.05 }} whileTap={{ scale: 0.95 }} onClick={onBack} className="p-2 rounded-full transition-all border border-stone-200/50 shadow-sm bg-white">
            <ArrowLeft size={16} className="text-stone-700" />
          </motion.button>
          <div>
            <p className="text-[9px] font-black text-sky-500 uppercase tracking-[0.4em] mb-0.5 underline">Module 02</p>
            <h1 className="font-serif font-bold text-lg tracking-tight text-stone-900">Reverse Engineering</h1>
          </div>
        </div>

        <div className="flex-grow space-y-4 overflow-y-auto no-scrollbar pr-2 relative">
          <div className="absolute left-[21px] top-6 bottom-6 w-0.5 bg-stone-100 -z-0" />
          <div className="absolute left-[21px] top-6 bottom-6 w-0.5">
              <motion.div
                  className="w-full bg-sky-500 shadow-[0_0_10px_rgba(14,165,233,0.5)]"
                  initial={{ height: 0 }}
                  animate={{ height: sections.length > 1 ? `${(unlockedSection / (sections.length - 1)) * 100}%` : '0%' }}
              />
          </div>
          {sections.map((section, idx) => {
            const isUnlocked = idx <= unlockedSection;
            const isActive = idx === activeSection;
            const isCompleted = idx < unlockedSection;
            return (
              <button key={section.id} disabled={!isUnlocked} onClick={() => handleJumpToSection(idx)} className={`relative z-10 w-full flex items-center gap-4 p-3 rounded-xl transition-all duration-500 text-left group ${isActive ? 'bg-sky-50 shadow-sm translate-x-2' : ''} ${!isUnlocked ? 'opacity-40 grayscale cursor-not-allowed' : 'hover:bg-stone-50'}`}>
                <div className={`w-11 h-11 rounded-xl flex items-center justify-center shrink-0 border-2 transition-all duration-500 ${isCompleted ? 'bg-sky-600 border-sky-600 text-white shadow-lg' : isActive ? 'bg-white border-sky-500 text-sky-600 shadow-xl rotate-12' : 'bg-white border-stone-200 text-stone-300'}`}>
                   {isCompleted ? <CheckCircle2 size={18} /> : isActive ? <section.icon size={18} /> : <Lock size={16} />}
                </div>
                <div className="flex-grow"><p className={`text-[8px] font-black uppercase tracking-widest ${isActive ? 'text-sky-500' : 'text-stone-400'}`}>{section.eyebrow.split('// ')[1]}</p><h4 className={`text-xs font-bold leading-tight ${isActive ? 'text-stone-900' : 'text-stone-500'}`}>{section.title}</h4></div>
              </button>
            );
          })}
        </div>
        <div className="mt-8 border-t border-stone-100 pt-8 flex flex-col items-center">
           <ActivityRing progress={progress} color="#0ea5e9" /><p className="text-[11px] font-black text-stone-900 uppercase tracking-widest text-center">Progress</p>
        </div>
      </aside>

      <main className="flex-grow flex flex-col items-center py-10 md:py-24 px-6 md:px-16 overflow-y-auto h-screen relative">
        <div className="absolute inset-0 bg-[radial-gradient(#e5e7eb_1px,transparent_1px)] [background-size:32px_32px] opacity-40 pointer-events-none" />
        <div className="w-full max-w-4xl relative z-10">
          <AnimatePresence mode="wait">
            <motion.div key={activeSection} initial={{ opacity: 0, x: 20 }} animate={{ opacity: 1, x: 0 }} exit={{ opacity: 0, x: -20 }} transition={{ duration: 0.6, ease: [0.16, 1, 0.3, 1] }}>
              {activeSection === 0 && (
                <ReadingSection title="The Chronological Paradox." eyebrow="Step 1" icon={History}>
                  <p>The logical way to plan is to start at the beginning and work forward. It's also the reason most study plans fail. This forward-facing approach is a victim of the <Highlight description="The cognitive bias where we underestimate how long a task will take, assuming a 'best-case scenario' future with no interruptions.">Planning Fallacy</Highlight>. It ignores illness, fatigue, and life, leading to the infamous "student syndrome"—cramming everything into the final weeks.</p>
                  <p>The solution is to invert the planning vector. Instead of asking "What should I do today?", you ask "To be ready for the exam, where must I be the day before?". This is <Highlight description="A project management methodology that starts with the fixed end-date and works backward to the present, revealing dependencies and creating a more realistic timeline.">Reverse Engineering</Highlight>. You anchor your plan to the non-negotiable end date and build backward, forcing a confrontation with reality.</p>
                  <PlanningParadoxVisualizer />
                </ReadingSection>
              )}
               {activeSection === 1 && (
                <ReadingSection title="The Theoretical Engine." eyebrow="Step 2" icon={DraftingCompass}>
                  <p>Reverse engineering isn't just a hack; it's a powerful framework built on three proven theories. From education, it uses <Highlight description="A curriculum design framework that starts with the end goal (the assessment) and works backward to design the learning activities.">Backward Design</Highlight>, ensuring every study session is directly linked to exam performance. It eliminates "junk volume"—study that feels productive but scores no marks.</p>
                  <p>From project management, it uses the <Highlight description="A method for scheduling complex projects. It identifies the longest chain of dependent tasks (the 'critical path') that determines the project's total duration.">Critical Path Method (CPM)</Highlight> to map out dependencies. You can't learn Calculus before Algebra; Algebra is on the critical path. From psychology, it uses <Highlight description="The act of visualizing a future goal and working backward. This makes the required steps seem more necessary and increases motivation.">Future Retrospection</Highlight> to build motivation by creating a "memory of the future."</p>
                  <BackwardDesignSorter />
                </ReadingSection>
              )}
              {activeSection === 2 && (
                <ReadingSection title="The Deconstruction Phase." eyebrow="Step 3" icon={ClipboardList}>
                  <p>Before you can build a schedule, you must deconstruct the curriculum. The process begins by establishing the <Highlight description="The exam date itself. This is the immovable point from which all backward planning begins.">Fixed Anchor</Highlight>. You must also define your <Highlight description="The final 1-2 weeks before the exam, which are reserved for maintenance, sleep regulation, and confidence preservation—not new learning.">"Taper" Period</Highlight>.</p>
                  <p>Next, you conduct a <Highlight description="The process of breaking down the entire syllabus into 'atomic units' of study, each representing a 45-90 minute session.">Grand Inventory</Highlight> of the syllabus. A topic like "Cell Biology" is too big; it must be broken down into "Mitochondria," "Osmosis," etc. Finally, you apply the <Highlight description="The 80/20 rule. By analyzing past papers, you identify the 20% of topics that deliver 80% of the marks. These are your high-yield assets.">Pareto Principle</Highlight> to prioritize high-yield topics.</p>
                </ReadingSection>
              )}
               {activeSection === 3 && (
                <ReadingSection title="The Strategic Phases." eyebrow="Step 4" icon={Layers}>
                    <p>A reverse-engineered schedule is not a solid block of "study." It is segmented into distinct operational phases, each with a specific goal. Working backward from the exam, the timeline looks like this:</p>
                    <p><strong>Phase 4: Taper & Maintenance (Final 2 Weeks):</strong> No new material. Focus on light review, sleep, and stress management. <strong>Phase 3: Simulation & Conditioning (Months 1-2 Pre-Exam):</strong> Full-length mock exams to build stamina and refine technique. <strong>Phase 2: Consolidation & Interleaving (Months 3-4 Pre-Exam):</strong> Move from blocked to mixed practice, deepening connections. <strong>Phase 1: Foundation & Acquisition (Months 5-6 Pre-Exam):</strong> First-pass learning and creating revision assets (e.g., flashcards).</p>
                </ReadingSection>
              )}
               {activeSection === 4 && (
                <ReadingSection title="Cognitive Optimization." eyebrow="Step 5" icon={BrainCircuit}>
                  <p>A great schedule doesn't just plan *what* you study; it plans *how* you study. It integrates cognitive science directly into the timeline. It must schedule <Highlight description="Reviewing material at increasing intervals to counteract the Forgetting Curve.">Spaced Repetition</Highlight>, creating "return trips" to old material.</p>
                  <p>It must prioritize <Highlight description="Forcing your brain to retrieve information (e.g., practice testing) rather than passively re-reading it. This is the engine of long-term memory.">Active Recall</Highlight> ("Output") over passive review ("Input"). And it should favour <Highlight description="Mixing different topics or subjects within a study session. This feels harder but trains the crucial skill of 'problem spotting'.">Interleaving</Highlight> over blocked practice, especially in the later phases, to build flexible, exam-ready knowledge.</p>
                </ReadingSection>
              )}
               {activeSection === 5 && (
                <ReadingSection title="The Resilient Blueprint." eyebrow="Step 6" icon={Shield}>
                  <p>A perfect, rigid schedule is a fragile schedule. It will shatter the first time you get sick or have a family event. A resilient schedule is designed to fail gracefully. This requires building in <Highlight description="Intentionally blank weeks (10-20% of your total time) that can absorb disruptions without derailing the entire plan.">Buffer Weeks</Highlight>.</p>
                  <p>Before you begin, you must conduct a <Highlight description="Identifying all fixed life events (holidays, weddings, etc.) and 'blacking them out' of your available time from the start.">"Non-Negotiables" Audit</Highlight>. Finally, you must choose your tool. Whether it's a digital <Highlight description="A project management tool that visualizes tasks on a timeline, making dependencies clear.">Gantt Chart</Highlight>, a Notion template, or an analog wall with sticky notes, the tool must make the timeline, dependencies, and critical path visible. You are now ready to build your schedule.</p>
                  <ImplementationChecklist />
                </ReadingSection>
              )}
              <footer className="mt-24 flex items-center justify-between pt-12 border-t border-stone-200/60 px-4">
                <motion.button whileHover={{ scale: 1.05 }} whileTap={{ scale: 0.95 }} onClick={handlePrev} disabled={activeSection === 0} className={`flex items-center gap-4 bg-stone-100 text-stone-800 px-8 py-4 rounded-xl font-black text-[10px] uppercase tracking-widest transition-all shadow-sm ${activeSection === 0 ? 'opacity-0 pointer-events-none' : ''}`}>
                  <ArrowLeft size={16} /> Prev
                </motion.button>
                <motion.button whileHover={{ scale: 1.05 }} whileTap={{ scale: 0.95 }} onClick={handleCompleteSection} className="group relative flex items-center gap-4 bg-stone-900 text-white px-12 py-6 rounded-2xl font-black text-[12px] uppercase tracking-widest hover:bg-sky-600 transition-all shadow-[0_20px_50px_rgba(0,0,0,0.2)] overflow-hidden">
                  <span className="relative z-10">{activeSection === sections.length - 1 ? 'Finish Protocol' : 'Deploy Next Phase'}</span>
                  <ArrowRight size={18} className="relative z-10 group-hover:translate-x-2 transition-transform" />
                </motion.button>
              </footer>
            </motion.div>
          </AnimatePresence>
        </div>
      </main>
    </div>
  );
};
