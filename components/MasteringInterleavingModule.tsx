

/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
*/

import React, { useState, useEffect } from 'react';
import { motion, AnimatePresence, Reorder } from 'framer-motion';
import { 
  ArrowLeft, CheckCircle2, ArrowRight, 
  Lock, Flag, Layers, Shuffle, Brain, ListChecks, Wrench
} from 'lucide-react';

type ModuleProgress = {
  unlockedSection: number;
};

interface MasteringInterleavingModuleProps {
  onBack: () => void;
  progress: ModuleProgress;
  onProgressUpdate: (progress: ModuleProgress) => void;
}

const Highlight = ({ children, description, color = "bg-purple-100/40", textColor = "text-purple-900", decorColor = "decoration-purple-400/40", hoverColor="hover:bg-purple-200/60" }: { children?: React.ReactNode, description: string, color?: string, textColor?: string, decorColor?: string, hoverColor?: string }) => {
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
              <p className="font-sans font-bold text-purple-400 mb-2 uppercase tracking-[0.2em] text-[9px]">The Academic Insight</p>
              <p className="text-stone-200 font-medium">{description}</p>
            </motion.div>
          </>
        )}
      </AnimatePresence>
    </span>
  );
};

const ReadingSection = ({ title, eyebrow, icon: Icon, children }: { title: string, eyebrow: string, icon: any, children?: React.ReactNode }) => (
  <article className="animate-fade-in">
    <header className="mb-12 text-left relative">
      <div className="absolute -left-16 top-0 hidden xl:block">
        <div className="w-12 h-12 rounded-2xl bg-stone-900 flex items-center justify-center text-purple-400 shadow-xl border border-white/10">
          <Icon size={24} />
        </div>
      </div>
      <span className="inline-flex items-center gap-2 px-3 py-1 bg-purple-50 text-purple-600 text-[10px] font-black tracking-[0.4em] uppercase rounded-full mb-4">
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

const MicroCommitment = ({ children }: { children?: React.ReactNode }) => (
  <div className="my-12 p-8 bg-purple-50/50 border-2 border-dashed border-purple-200 rounded-3xl">
    <div className="flex items-start gap-5">
      <div className="w-11 h-11 rounded-xl bg-purple-500 text-white flex items-center justify-center shrink-0 mt-1 shadow-lg shadow-purple-500/20">
        <Flag size={20} />
      </div>
      <div>
        <h4 className="font-bold text-purple-800 text-sm uppercase tracking-widest">Your Mission (Under 5 Mins)</h4>
        <div className="text-stone-600 mt-2 font-medium leading-relaxed">
          {children}
        </div>
      </div>
    </div>
  </div>
);

const ActivityRing = ({ progress, color = "#a855f7" }: { progress: number, color?: string }) => {
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

const StudyPlannerInteractive = () => {
    const [planType, setPlanType] = useState<'blocked' | 'interleaved'>('blocked');
    const blockedSchedule = { Mon: ['Maths', 'Maths', 'Maths'], Tue: ['English', 'English', 'English'], Wed: ['Biology', 'Biology', 'Biology'] };
    const interleavedSchedule = { Mon: ['Maths', 'English', 'French'], Tue: ['English', 'Biology', 'History'], Wed: ['Biology', 'Maths', 'English'] };
    const schedule = planType === 'blocked' ? blockedSchedule : interleavedSchedule;

    return (
        <div className="my-10 p-8 md:p-12 bg-white rounded-[3rem] border border-stone-200 shadow-xl">
            <h4 className="font-serif text-2xl font-bold text-stone-800 text-center italic">Weekly Schedule Architect</h4>
            <div className="flex justify-center gap-2 p-1 bg-stone-100 rounded-full my-6 max-w-sm mx-auto">
                <button onClick={() => setPlanType('blocked')} className={`w-full px-4 py-2 text-xs font-bold rounded-full ${planType === 'blocked' ? 'bg-white shadow' : ''}`}>Blocked Schedule</button>
                <button onClick={() => setPlanType('interleaved')} className={`w-full px-4 py-2 text-xs font-bold rounded-full ${planType === 'interleaved' ? 'bg-white shadow' : ''}`}>Interleaved Schedule</button>
            </div>
            <div className="grid grid-cols-3 gap-2 text-center text-xs">
                {Object.entries(schedule).map(([day, subjects]) => (
                    <div key={day}>
                        <p className="font-bold mb-2">{day}</p>
                        <div className="space-y-1">
                            {subjects.map((sub, i) => (
                                <motion.div key={`${day}-${i}`} layoutId={`${day}-${i}-${sub}`} className="p-2 bg-stone-50 border border-stone-200 rounded-md">{sub}</motion.div>
                            ))}
                        </div>
                    </div>
                ))}
            </div>
        </div>
    );
};

const ProblemTypeSpotter = () => {
    const [choice, setChoice] = useState<{[key:string]: 'chain'|'product'|null}>({});
    const problems = [
        { id: 1, text: "y = sin(x²)", correct: "chain" },
        { id: 2, text: "y = x²sin(x)", correct: "product" },
    ];
    
    return (
        <div className="my-10 p-8 md:p-12 bg-white rounded-[3rem] border border-stone-200 shadow-xl">
             <h4 className="font-serif text-2xl font-bold text-stone-800 text-center italic">Problem Spotter</h4>
             <p className="text-center text-sm text-stone-500 mb-8">Calculus: Don't solve. Just identify the correct rule.</p>
             {problems.map(p => (
                <div key={p.id} className="mb-4">
                    <p className="text-center font-mono bg-stone-100 p-4 rounded-xl mb-2">{p.text}</p>
                    <div className="grid grid-cols-2 gap-2">
                        <button onClick={() => setChoice({...choice, [p.id]:'chain'})} className={`p-2 text-xs rounded-lg border-2 ${choice[p.id] && (choice[p.id] === 'chain' && p.correct === 'chain' ? 'bg-emerald-100 border-emerald-300' : choice[p.id] === 'chain' ? 'bg-rose-100 border-rose-300' : 'bg-stone-100 border-stone-200')}`}>Chain Rule</button>
                        <button onClick={() => setChoice({...choice, [p.id]:'product'})} className={`p-2 text-xs rounded-lg border-2 ${choice[p.id] && (choice[p.id] === 'product' && p.correct === 'product' ? 'bg-emerald-100 border-emerald-300' : choice[p.id] === 'product' ? 'bg-rose-100 border-rose-300' : 'bg-stone-100 border-stone-200')}`}>Product Rule</button>
                    </div>
                </div>
             ))}
        </div>
    );
};

const RetrospectiveRevisionLog = () => {
    const [topics, setTopics] = useState([
        { name: "Algebra", status: 'red', lastStudied: null },
        { name: "Statistics", status: 'amber', lastStudied: null },
        { name: "Geometry", status: 'green', lastStudied: null },
        { name: "Functions", status: 'red', lastStudied: null },
        { name: "Number", status: 'amber', lastStudied: null },
    ]);
    const [nextTopic, setNextTopic] = useState("Algebra");

    const updateStatus = (name: string, newStatus: 'red' | 'amber' | 'green') => {
        setTopics(topics.map(t => t.name === name ? {...t, status: newStatus} : t));
    };

    const findNextTopic = () => {
        const redTopics = topics.filter(t => t.status === 'red');
        if (redTopics.length > 0) {
            setNextTopic(redTopics[0].name);
            return;
        }
        const amberTopics = topics.filter(t => t.status === 'amber');
        if (amberTopics.length > 0) {
            setNextTopic(amberTopics[0].name);
            return;
        }
        setNextTopic(topics[0].name);
    }

    return (
         <div className="my-10 p-8 md:p-12 bg-white rounded-[3rem] border border-stone-200 shadow-xl">
             <h4 className="font-serif text-2xl font-bold text-stone-800 text-center italic">Retrospective Revision Log</h4>
             <p className="text-center text-sm text-stone-500 mb-8">Update your confidence after studying. The "Worst First" rule will guide you.</p>
             <div className="space-y-3">
                {topics.map(topic => (
                    <div key={topic.name} className="p-3 bg-stone-50 border border-stone-200 rounded-lg flex justify-between items-center">
                        <span className="font-bold text-sm">{topic.name}</span>
                        <div className="flex gap-1">
                            <button onClick={() => updateStatus(topic.name, 'red')} className={`w-6 h-6 rounded-full border-2 ${topic.status === 'red' ? 'bg-rose-500 border-rose-600' : 'bg-rose-200 border-rose-300'}`}></button>
                            <button onClick={() => updateStatus(topic.name, 'amber')} className={`w-6 h-6 rounded-full border-2 ${topic.status === 'amber' ? 'bg-amber-500 border-amber-600' : 'bg-amber-200 border-amber-300'}`}></button>
                            <button onClick={() => updateStatus(topic.name, 'green')} className={`w-6 h-6 rounded-full border-2 ${topic.status === 'green' ? 'bg-emerald-500 border-emerald-600' : 'bg-emerald-200 border-emerald-300'}`}></button>
                        </div>
                    </div>
                ))}
             </div>
             <div className="mt-6 text-center">
                 <button onClick={findNextTopic} className="px-4 py-2 bg-stone-800 text-white text-xs font-bold rounded-lg">Find Next Topic</button>
                 <p className="mt-4 text-sm">Next up: <span className="font-bold text-purple-600">{nextTopic}</span></p>
             </div>
        </div>
    );
}

// --- MODULE COMPONENT ---
export const MasteringInterleavingModule: React.FC<MasteringInterleavingModuleProps> = ({ onBack, progress, onProgressUpdate }) => {
  const [activeSection, setActiveSection] = useState(progress.unlockedSection);
  const unlockedSection = progress.unlockedSection;
  
  const sections = [
    { id: 'illusion-of-mastery', title: 'The Illusion of "Mastery"', eyebrow: '01 // The Blocked Trap', icon: Layers },
    { id: 'topic-salad', title: 'The "Topic Salad" Method', eyebrow: '02 // The Solution', icon: Shuffle },
    { id: 'desirable-difficulty', title: 'The Science of "Desirable Difficulty"', eyebrow: '03 // Why It Works', icon: Brain },
    { id: 'retrospective-timetable', title: 'The Retrospective Timetable', eyebrow: '04 // The System', icon: ListChecks },
    { id: 'subject-hacker', title: 'Your Interleaving Blueprint', eyebrow: '05 // The Action Plan', icon: Wrench },
  ];

  useEffect(() => {
    setActiveSection(progress.unlockedSection);
  }, [progress.unlockedSection]);
  
  const handleCompleteSection = () => {
    if (activeSection === unlockedSection && unlockedSection < sections.length - 1) {
      onProgressUpdate({ unlockedSection: unlockedSection + 1 });
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

  const progressPercentage = sections.length > 1 ? (unlockedSection / (sections.length - 1)) * 100 : 0;

  return (
    <div className="min-h-screen bg-[#FBFBF9] text-stone-900 font-sans flex flex-col md:flex-row overflow-x-hidden">
      <aside className="w-full md:w-80 bg-white border-r border-stone-200 sticky top-0 md:h-screen z-40 p-8 flex flex-col">
        <div className="flex items-center gap-4 mb-12">
          <motion.button whileHover={{ scale: 1.05 }} whileTap={{ scale: 0.95 }} onClick={onBack} className="p-2 rounded-full transition-all border border-stone-200/50 shadow-sm bg-white">
            <ArrowLeft size={16} className="text-stone-700" />
          </motion.button>
          <div>
            <p className="text-[9px] font-black text-purple-500 uppercase tracking-[0.4em] mb-0.5 underline">Module 03</p>
            <h1 className="font-serif font-bold text-lg tracking-tight text-stone-900">Mastering Interleaving</h1>
          </div>
        </div>

        <div className="flex-grow space-y-4 overflow-y-auto no-scrollbar pr-2 relative">
          <div className="absolute left-[21px] top-6 bottom-6 w-0.5 bg-stone-100 -z-0" />
          <div className="absolute left-[21px] top-6 bottom-6 w-0.5">
              <motion.div
                  className="w-full bg-purple-500 shadow-[0_0_10px_rgba(168,85,247,0.5)]"
                  style={{ height: `${progressPercentage}%` }}
              />
          </div>
          {sections.map((section, idx) => {
            const isUnlocked = idx <= unlockedSection;
            const isActive = idx === activeSection;
            const isCompleted = idx < unlockedSection;
            return (
              <button key={section.id} disabled={!isUnlocked} onClick={() => handleJumpToSection(idx)} className={`relative z-10 w-full flex items-center gap-4 p-3 rounded-xl transition-all duration-500 text-left group ${isActive ? 'bg-purple-50 shadow-sm translate-x-2' : ''} ${!isUnlocked ? 'opacity-40 grayscale cursor-not-allowed' : 'hover:bg-stone-50'}`}>
                <div className={`w-11 h-11 rounded-xl flex items-center justify-center shrink-0 border-2 transition-all duration-500 ${isCompleted ? 'bg-purple-600 border-purple-600 text-white shadow-lg' : isActive ? 'bg-white border-purple-500 text-purple-600 shadow-xl rotate-12' : 'bg-white border-stone-200 text-stone-300'}`}>
                   {isCompleted ? <CheckCircle2 size={18} /> : isActive ? <section.icon size={18} /> : <Lock size={16} />}
                </div>
                <div className="flex-grow"><p className={`text-[8px] font-black uppercase tracking-widest ${isActive ? 'text-purple-500' : 'text-stone-400'}`}>{section.eyebrow.split('// ')[1]}</p><h4 className={`text-xs font-bold leading-tight ${isActive ? 'text-stone-900' : 'text-stone-500'}`}>{section.title}</h4></div>
              </button>
            );
          })}
        </div>

        <div className="mt-8 border-t border-stone-100 pt-8 flex flex-col items-center">
           <ActivityRing progress={progressPercentage} color="#a855f7" /><p className="text-[11px] font-black text-stone-900 uppercase tracking-widest text-center">Progress</p>
        </div>
      </aside>

      <main className="flex-grow flex flex-col items-center py-10 md:py-24 px-6 md:px-16 overflow-y-auto h-screen relative">
        <div className="absolute inset-0 bg-[radial-gradient(#e5e7eb_1px,transparent_1px)] [background-size:32px_32px] opacity-40 pointer-events-none" />
        <div className="w-full max-w-4xl relative z-10">
          <AnimatePresence mode="wait">
            <motion.div key={activeSection} initial={{ opacity: 0, x: 20 }} animate={{ opacity: 1, x: 0 }} exit={{ opacity: 0, x: -20 }} transition={{ duration: 0.6, ease: [0.16, 1, 0.3, 1] }}>
              {activeSection === 0 && (
                <ReadingSection title="The Illusion of 'Mastery'." eyebrow="Step 1" icon={Layers}>
                  <p>Most students study using <Highlight description="The common study method of focusing on one topic until you feel you've mastered it before moving to the next (e.g., AAABBBCCC).">Blocked Practice</Highlight>. You spend Monday night on Maths, Tuesday on English, Wednesday on Biology. It feels productive. After three hours of Algebra, you feel like you've mastered it. But this is an <Highlight description="The misleading feeling of mastery you get from blocked practice, because the information is still fresh in your short-term memory.">Illusion of Competence</Highlight>.</p>
                  <p>The problem is, your brain isn't being trained for the real Leaving Cert. The exam is not blocked; it's a random mix of topics. When you do 20 algebra problems in a row, you don't have to figure out *what* to do, only *how* to do it. You fail to train the crucial <Highlight description="The crucial ability to tell the difference between similar types of problems or concepts to know which strategy to apply (e.g., telling integration from differentiation).">discriminative skills</Highlight> needed to succeed under pressure.</p>
                </ReadingSection>
              )}
               {activeSection === 1 && (
                <ReadingSection title="The 'Topic Salad' Method." eyebrow="Step 2" icon={Shuffle}>
                  <p>The solution is simple, but powerful: <Highlight description="The highly effective study strategy of mixing different topics or problem types within a single study session (e.g., ABCABCABC).">Interleaving</Highlight>. Instead of a "topic block," your study session should be a "topic salad." A fruit salad isn't a pile of apples next to a pile of bananas; it's a mix. Your study should be the same.</p>
                  <p>This happens at two levels. <Highlight description="Mixing subjects within your weekly timetable (e.g., Maths, English, and Biology on Monday).">Macro-interleaving</Highlight> is about your weekly schedule: instead of one subject for 3 hours, study three subjects for 1 hour each. <Highlight description="Mixing topics *within* a single subject session (e.g., doing a mix of Algebra, Stats, and Geometry questions).">Micro-interleaving</Highlight> is about mixing topics *within* a subject. This is harder, but as we'll see, the effort is where the learning happens.</p>
                  <StudyPlannerInteractive />
                </ReadingSection>
              )}
               {activeSection === 2 && (
                <ReadingSection title="The Science of 'Desirable Difficulty'." eyebrow="Step 3" icon={Brain}>
                  <p>Interleaving feels harder. When you switch from Maths to English, your brain has to work to "reload" a new context. This effort is called a <Highlight description="The idea from cognitive science that learning tasks that feel harder and more effortful actually lead to much stronger, long-term memory.">Desirable Difficulty</Highlight>. Blocked practice feels easy because it's like re-watching the same scene of a movie over and over. Interleaving forces your brain to constantly change the channel, which strengthens its ability to find the right channel under pressure.</p>
                  <p>This is the <Highlight description="The core theory behind interleaving. It says that mixing similar concepts forces the brain to notice the subtle differences ('discriminative features') between them, leading to deeper learning.">Discriminative-Contrast Hypothesis</Highlight>. By placing similar but different concepts next to each other (like differentiation and integration), interleaving forces your brain to spot the differences. You're not just learning a rule; you're learning *when* to use that rule.</p>
                  <ProblemTypeSpotter/>
                </ReadingSection>
              )}
              {activeSection === 3 && (
                <ReadingSection title="The Retrospective Timetable." eyebrow="Step 4" icon={ListChecks}>
                  <p>Interleaving can feel chaotic. The best way to manage it is to abandon your rigid, forward-planning timetable and adopt a <Highlight description="A powerful way to plan your study by tracking what you've already done and focusing on your weakest areas first, rather than planning weeks in advance.">Retrospective Revision Timetable</Highlight>. Instead of deciding what to study next week, you decide what to study *right now* based on what you're worst at.</p>
                  <p>The system is simple: 1. List every topic in a subject. 2. After you study a topic, you colour-code it: Green (I know this), Amber (It's okay), or Red (I'm lost). 3. The next time you study that subject, you follow the <Highlight description="The core principle of the Retrospective Timetable: always prioritize the topic you are least confident in (Red/Amber) to ensure you address your biggest weaknesses.">"Worst First" Rule</Highlight>: you must work on a Red topic. This naturally enforces interleaving and spacing, because you're constantly jumping between your weakest areas across the entire course.</p>
                  <RetrospectiveRevisionLog />
                </ReadingSection>
              )}
               {activeSection === 4 && (
                <ReadingSection title="Your Interleaving Blueprint." eyebrow="Step 5" icon={Wrench}>
                  <p>You have the science. Now you need the action plan. Interleaving isn't a vague concept; it's a set of specific, practical strategies you can apply to every subject you study for the Leaving Cert.</p>
                  <p>From the "Mixed Bag" approach in Maths to the "Poetry Roulette" in English, the goal is always the same: break up the blocks, embrace the struggle of switching, and train your brain for the reality of the exam. This is not about studying more; it's about studying smarter. It's time to build your own interleaved engine.</p>
                  <MicroCommitment>
                    <p>Tonight, take your hardest subject. Instead of studying one chapter for an hour, pick three different chapters and spend just 20 minutes on each. Feel the "desirable difficulty" of switching between them.</p>
                  </MicroCommitment>
                </ReadingSection>
              )}
              <footer className="mt-24 flex items-center justify-between pt-12 border-t border-stone-200/60 px-4">
                <motion.button whileHover={{ scale: 1.05 }} whileTap={{ scale: 0.95 }} onClick={handlePrev} disabled={activeSection === 0} className={`flex items-center gap-4 bg-stone-100 text-stone-800 px-8 py-4 rounded-xl font-black text-[10px] uppercase tracking-widest transition-all shadow-sm ${activeSection === 0 ? 'opacity-0 pointer-events-none' : ''}`}>
                  <ArrowLeft size={16} /> Prev
                </motion.button>
                <motion.button whileHover={{ scale: 1.05 }} whileTap={{ scale: 0.95 }} onClick={handleCompleteSection} className="group relative flex items-center gap-4 bg-stone-900 text-white px-12 py-6 rounded-2xl font-black text-[12px] uppercase tracking-widest hover:bg-purple-600 transition-all shadow-[0_20px_50px_rgba(0,0,0,0.2)] overflow-hidden">
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
