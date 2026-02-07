
/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
*/

import React, { useState } from 'react';
import { motion, AnimatePresence, Reorder } from 'framer-motion';
import { 
  ArrowLeft, CheckCircle2, ArrowRight, 
  Lock, Flag, Target, Trophy, Gamepad2, Columns, CalendarClock, PlusCircle, BarChart, Check, PieChart, Star
} from 'lucide-react';

interface ReframingProgressModuleProps {
  onBack: () => void;
}

const Highlight = ({ children, description, color = "bg-teal-100/40", textColor = "text-teal-900", decorColor = "decoration-teal-400/40", hoverColor="hover:bg-teal-200/60" }: { children?: React.ReactNode, description: string, color?: string, textColor?: string, decorColor?: string, hoverColor?: string }) => {
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
              <p className="font-sans font-bold text-teal-400 mb-2 uppercase tracking-[0.2em] text-[9px]">The Academic Insight</p>
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
        <div className="w-12 h-12 rounded-2xl bg-stone-900 flex items-center justify-center text-teal-400 shadow-xl border border-white/10">
          <Icon size={24} />
        </div>
      </div>
      <span className="inline-flex items-center gap-2 px-3 py-1 bg-teal-50 text-teal-600 text-[10px] font-black tracking-[0.4em] uppercase rounded-full mb-4">
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
  <div className="my-12 p-8 bg-teal-50/50 border-2 border-dashed border-teal-200 rounded-3xl">
    <div className="flex items-start gap-5">
      <div className="w-11 h-11 rounded-xl bg-teal-500 text-white flex items-center justify-center shrink-0 mt-1 shadow-lg shadow-teal-500/20">
        <Flag size={20} />
      </div>
      <div>
        <h4 className="font-bold text-teal-800 text-sm uppercase tracking-widest">Your Mission (Under 5 Mins)</h4>
        <div className="text-stone-600 mt-2 font-medium leading-relaxed">
          {children}
        </div>
      </div>
    </div>
  </div>
);

const ActivityRing = ({ progress, color = "#14b8a6" }: { progress: number, color?: string }) => {
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

const KanbanBoard = () => {
    const [tasks, setTasks] = useState([
        { id: 1, text: "Write Macbeth Quote Bank", column: 'todo' },
        { id: 2, text: "Do 2023 Paper 1 Algebra Q", column: 'todo' },
        { id: 3, text: "Practice Irish Oral Poem", column: 'doing' },
    ]);
    const [wins, setWins] = useState(0);

    const onDragEnd = (info: any, item: any) => {
        const point = info.point;
        const columns = document.querySelectorAll('.kanban-col');
        let targetColumn = null;
        columns.forEach((col: any) => {
            const rect = col.getBoundingClientRect();
            if (point.x > rect.left && point.x < rect.right && point.y > rect.top && point.y < rect.bottom) {
                targetColumn = col.dataset.column;
            }
        });

        if (targetColumn) {
            if (item.column !== 'done' && targetColumn === 'done') {
                setWins(w => w + 1);
            }
            setTasks(tasks.map(t => t.id === item.id ? { ...t, column: targetColumn } : t));
        }
    };

    return (
        <div className="my-10 p-8 md:p-12 bg-white rounded-[3rem] border border-stone-200 shadow-xl">
             <h4 className="font-serif text-2xl font-bold text-stone-800 text-center italic">Kanban Flow</h4>
             <p className="text-center text-sm text-stone-500 mb-8">Drag tasks to the "Done" column to secure a "Win".</p>
             <div className="grid grid-cols-3 gap-4">
                {['todo', 'doing', 'done'].map(col => (
                    <div key={col} data-column={col} className="kanban-col p-4 bg-stone-50 rounded-2xl min-h-[200px]">
                        <h5 className="font-bold text-center text-sm uppercase tracking-widest text-stone-500">{col} {col === 'done' && `(${wins})`}</h5>
                        <div className="mt-4 space-y-2">
                            {tasks.filter(t => t.column === col).map(task => (
                                <motion.div 
                                    key={task.id} 
                                    drag
                                    onDragEnd={(e, info) => onDragEnd(info, task)}
                                    className="p-3 bg-white rounded-lg shadow-sm text-sm font-semibold cursor-grab active:cursor-grabbing"
                                >{task.text}</motion.div>
                            ))}
                        </div>
                    </div>
                ))}
             </div>
        </div>
    );
};

const RetrospectiveLog = () => {
    const [topics, setTopics] = useState([
        { name: "Ecology", status: 'red', last: null },
        { name: "Genetics", status: 'amber', last: null },
        { name: "Photosynthesis", status: 'green', last: null },
    ]);
    const [nextTopic, setNextTopic] = useState("Ecology (Red)");

    const updateStatus = (name: string, newStatus: 'red' | 'amber' | 'green') => {
        setTopics(topics.map(t => t.name === name ? { ...t, status: newStatus } : t));
    };

    const findNext = () => {
        const red = topics.find(t => t.status === 'red');
        if (red) { setNextTopic(`${red.name} (Red)`); return; }
        const amber = topics.find(t => t.status === 'amber');
        if (amber) { setNextTopic(`${amber.name} (Amber)`); return; }
        setNextTopic("Everything's Green! Review oldest topic.");
    };

    return (
        <div className="my-10 p-8 md:p-12 bg-white rounded-[3rem] border border-stone-200 shadow-xl">
            <h4 className="font-serif text-2xl font-bold text-stone-800 text-center italic">Retrospective Log</h4>
            <p className="text-center text-sm text-stone-500 mb-8">Rate your confidence. Let the "Worst First" rule decide your next move.</p>
            {topics.map(t => (
                <div key={t.name} className="flex items-center justify-between p-2">
                    <span className="font-bold">{t.name}</span>
                    <div className="flex gap-1">
                        <button onClick={() => updateStatus(t.name, 'red')} className={`w-6 h-6 rounded-full border-2 ${t.status === 'red' ? 'bg-rose-500 border-rose-600' : 'bg-rose-200'}`} />
                        <button onClick={() => updateStatus(t.name, 'amber')} className={`w-6 h-6 rounded-full border-2 ${t.status === 'amber' ? 'bg-amber-500 border-amber-600' : 'bg-amber-200'}`} />
                        <button onClick={() => updateStatus(t.name, 'green')} className={`w-6 h-6 rounded-full border-2 ${t.status === 'green' ? 'bg-emerald-500 border-emerald-600' : 'bg-emerald-200'}`} />
                    </div>
                </div>
            ))}
             <div className="mt-6 text-center">
                 <button onClick={findNext} className="px-4 py-2 bg-stone-800 text-white text-xs font-bold rounded-lg">Find Next Task</button>
                 <p className="mt-4 text-sm">Next up: <span className="font-bold text-teal-600">{nextTopic}</span></p>
             </div>
        </div>
    );
};


// --- MODULE COMPONENT ---
export const ReframingProgressModule: React.FC<ReframingProgressModuleProps> = ({ onBack }) => {
  const [activeSection, setActiveSection] = useState(0);
  const [unlockedSection, setUnlockedSection] = useState(0);
  
  const sections = [
    { id: 'time-trap', title: 'The Time Trap', eyebrow: '01 // Naive vs. Deliberate', icon: Target },
    { id: 'pareto-protocol', title: 'The 80/20 Protocol', eyebrow: '02 // The Vital Few', icon: BarChart },
    { id: 'banked-grade', title: 'The "Banked Grade" Heist', eyebrow: '03 // Securing Early Wins', icon: PieChart },
    { id: 'quest-system', title: 'The Quest System', eyebrow: '04 // Mastery vs. Performance', icon: Gamepad2 },
    { id: 'kanban-flow', title: 'The Kanban Flow', eyebrow: '05 // Visualizing Work', icon: Columns },
    { id: 'retrospective-log', title: 'The Retrospective Log', eyebrow: '06 // Data-Driven Study', icon: CalendarClock },
    { id: 'xp-engine', title: 'The XP Engine', eyebrow: '07 // Gamifying the Grind', icon: Star },
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
            <p className="text-[9px] font-black text-teal-500 uppercase tracking-[0.4em] mb-0.5 underline">Module 10</p>
            <h1 className="font-serif font-bold text-lg tracking-tight text-stone-900">Reframing Progress</h1>
          </div>
        </div>

        <div className="flex-grow space-y-4 overflow-y-auto no-scrollbar pr-2 relative">
          <div className="absolute left-[21px] top-6 bottom-6 w-0.5 bg-stone-100 -z-0" />
          <div className="absolute left-[21px] top-6 bottom-6 w-0.5">
              <motion.div
                  className="w-full bg-teal-500 shadow-[0_0_10px_rgba(20,184,166,0.5)]"
                  initial={{ height: 0 }}
                  animate={{ height: sections.length > 1 ? `${(unlockedSection / (sections.length - 1)) * 100}%` : '0%' }}
              />
          </div>
          {sections.map((section, idx) => {
            const isUnlocked = idx <= unlockedSection;
            const isActive = idx === activeSection;
            const isCompleted = idx < unlockedSection;
            return (
              <button key={section.id} disabled={!isUnlocked} onClick={() => handleJumpToSection(idx)} className={`relative z-10 w-full flex items-center gap-4 p-3 rounded-xl transition-all duration-500 text-left group ${isActive ? 'bg-teal-50 shadow-sm translate-x-2' : ''} ${!isUnlocked ? 'opacity-40 grayscale cursor-not-allowed' : 'hover:bg-stone-50'}`}>
                <div className={`w-11 h-11 rounded-xl flex items-center justify-center shrink-0 border-2 transition-all duration-500 ${isCompleted ? 'bg-teal-600 border-teal-600 text-white shadow-lg' : isActive ? 'bg-white border-teal-500 text-teal-600 shadow-xl rotate-12' : 'bg-white border-stone-200 text-stone-300'}`}>
                   {isCompleted ? <CheckCircle2 size={18} /> : isActive ? <section.icon size={18} /> : <Lock size={16} />}
                </div>
                <div className="flex-grow"><p className={`text-[8px] font-black uppercase tracking-widest ${isActive ? 'text-teal-500' : 'text-stone-400'}`}>{section.eyebrow.split('// ')[1]}</p><h4 className={`text-xs font-bold leading-tight ${isActive ? 'text-stone-900' : 'text-stone-500'}`}>{section.title}</h4></div>
              </button>
            );
          })}
        </div>
        <div className="mt-8 border-t border-stone-100 pt-8 flex flex-col items-center">
           <ActivityRing progress={progress} /><p className="text-[11px] font-black text-stone-900 uppercase tracking-widest text-center">Progress</p>
        </div>
      </aside>

      <main className="flex-grow flex flex-col items-center py-10 md:py-24 px-6 md:px-16 overflow-y-auto h-screen relative">
        <div className="absolute inset-0 bg-[radial-gradient(#e5e7eb_1px,transparent_1px)] [background-size:32px_32px] opacity-40 pointer-events-none" />
        <div className="w-full max-w-4xl relative z-10">
          <AnimatePresence mode="wait">
            <motion.div key={activeSection} initial={{ opacity: 0, x: 20 }} animate={{ opacity: 1, x: 0 }} exit={{ opacity: 0, x: -20 }} transition={{ duration: 0.6, ease: [0.16, 1, 0.3, 1] }}>
              {activeSection === 0 && (
                <ReadingSection title="The Time Trap." eyebrow="Step 1" icon={Target}>
                  <p>The biggest lie in the Leaving Cert is that "hours logged" equals "wins secured." This is the "sweat equity" model of learning. It leads to burnout and the <Highlight description="A metacognitive failure where you misinterpret the ease of processing familiar information as a sign of durable learning.">Illusion of Competence</Highlight>. It's time for a paradigm shift.</p>
                  <p>The antidote is to reframe progress from input (time) to output (results). This means abandoning <Highlight description="Low-effort, repetitive practice without feedback (e.g., re-reading). This feels productive but yields minimal long-term learning.">Naive Practice</Highlight> and embracing <Highlight description="High-intensity, targeted practice on specific weaknesses with immediate feedback. This is the engine of skill acquisition.">Deliberate Practice</Highlight>. Naive practice is reading an essay; deliberate practice is writing one paragraph and comparing it to a H1 standard.</p>
                </ReadingSection>
              )}
              {activeSection === 1 && (
                <ReadingSection title="The 80/20 Protocol." eyebrow="Step 2" icon={BarChart}>
                    <p>The <Highlight description="The principle that roughly 80% of effects come from 20% of causes. In the Leaving Cert, this means ~80% of marks come from ~20% of the syllabus.">Pareto Principle</Highlight> is your strategic compass. It dictates a hierarchy of prioritization. Your job is to identify the "Vital Few" topics that offer the highest return on investment and master them first.</p>
                    <p>In Biology, for example, Ecology and Genetics are guaranteed long questions. Mastering these secures a huge chunk of your grade before you even touch the sprawling Unit 3. This is not about ignoring the other 80%; it's about securing your foundational grade with high-probability "wins" first.</p>
                </ReadingSection>
              )}
              {activeSection === 2 && (
                <ReadingSection title="The 'Banked Grade' Heist." eyebrow="Step 3" icon={PieChart}>
                    <p>The structure of the Leaving Cert allows for a strategic "heist." A significant portion of your final grade can be secured months before the written exams. These <Highlight description="Coursework, practical projects, and oral exams that are completed before June. They are immune to exam-day nerves and represent the ultimate 'early wins'.">'Banked Grades'</Highlight> are your safety net.</p>
                    <p>For a student taking Irish (40% Oral), History (20% RSR), and Geography (20% Field Study), **80% of a subject equivalent** is secured before June. This realization must fundamentally alter your study prioritization in the spring of your 6th year.</p>
                </ReadingSection>
              )}
              {activeSection === 3 && (
                <ReadingSection title="The Quest System." eyebrow="Step 4" icon={Gamepad2}>
                    <p>Traditional study is demotivating because the feedback loop is too long. <Highlight description="Applying game-like elements (points, levels, quests) to non-game activities to increase motivation and engagement.">Gamification</Highlight> hacks your brain's dopamine reward system to make progress feel immediate and tangible.</p>
                    <p>The key is to reframe the vague goal of "doing well" into a series of concrete, manageable "quests" (e.g., "The Poetry Quest," "The Algebra Boss Battle"). This fosters a <Highlight description="The desire to learn and master a skill for its own sake. It is more resilient to failure than a Performance Orientation.">Mastery Orientation</Highlight>, where challenges are seen as opportunities to 'level up', rather than threats to your intelligence.</p>
                </ReadingSection>
              )}
              {activeSection === 4 && (
                <ReadingSection title="The Kanban Flow." eyebrow="Step 5" icon={Columns}>
                    <p>Ditch your anxious timetable and adopt a project management tool. A <Highlight description="An agile project management tool that visualizes workflow into columns (e.g., To Do, Doing, Done).">Kanban Board</Highlight> replaces a schedule of *when* to work with a system of *what* to achieve. It visualizes progress, not the passage of time.</p>
                    <p>The act of physically moving a task from "Doing" to "Done" provides a micro-dose of dopamine, reinforcing the behaviour. Over time, the "Done" column becomes a tangible pile of "Wins," countering the feeling of having done nothing despite studying for hours.</p>
                    <KanbanBoard />
                </ReadingSection>
              )}
              {activeSection === 5 && (
                <ReadingSection title="The Retrospective Log." eyebrow="Step 6" icon={CalendarClock}>
                    <p>Standard timetables fail because they are prospective—they guess what you'll need to study. A <Highlight description="A data-driven revision system where you record what you've studied and your confidence level (Red/Amber/Green), then decide what to study next based on your weakest, oldest topic.">Retrospective Log</Highlight> is based on actual performance. It naturally enforces Spaced Repetition and Interleaving.</p>
                    <p>The rule is simple: **"Worst First."** When you sit down to study, you don't follow a pre-written plan. You look at your log and ask two questions: "What am I Red/Amber in?" and "What has the oldest date?" This algorithmic approach removes decision fatigue and ensures you are always working on your biggest weaknesses.</p>
                    <RetrospectiveLog/>
                </ReadingSection>
              )}
              {activeSection === 6 && (
                <ReadingSection title="The XP Engine." eyebrow="Step 7" icon={Star}>
                    <p>For an extra motivational boost, you can externalize the reward structure by turning the Leaving Cert into a Role-Playing Game (RPG). Assign "Experience Points" (XP) to tasks based on their difficulty and impact.</p>
                    <p>A low-yield task like reading a chapter might be 50 XP. A medium-yield task like making flashcards could be 100 XP. A high-yield "win" like completing a timed exam question could be 300 XP. Accumulate XP to reach "Levels," unlocking guilt-free rewards like a movie night. This makes the invisible progress of studying visible and rewarding.</p>
                     <MicroCommitment>
                        <p>Define your first "Level Up." What small, enjoyable reward can you give yourself for earning your first 1000 XP? Write it down. Now you have your first quest.</p>
                    </MicroCommitment>
                </ReadingSection>
              )}
              <footer className="mt-24 flex items-center justify-between pt-12 border-t border-stone-200/60 px-4">
                <motion.button whileHover={{ scale: 1.05 }} whileTap={{ scale: 0.95 }} onClick={handlePrev} disabled={activeSection === 0} className={`flex items-center gap-4 bg-stone-100 text-stone-800 px-8 py-4 rounded-xl font-black text-[10px] uppercase tracking-widest transition-all shadow-sm ${activeSection === 0 ? 'opacity-0 pointer-events-none' : ''}`}>
                  <ArrowLeft size={16} /> Prev
                </motion.button>
                <motion.button whileHover={{ scale: 1.05 }} whileTap={{ scale: 0.95 }} onClick={handleCompleteSection} className="group relative flex items-center gap-4 bg-stone-900 text-white px-12 py-6 rounded-2xl font-black text-[12px] uppercase tracking-widest hover:bg-teal-600 transition-all shadow-[0_20px_50px_rgba(0,0,0,0.2)] overflow-hidden">
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
