/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
*/

import React, { useState } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { 
  ArrowLeft, CheckCircle2, ArrowRight, 
  Lock, Flag, Key, PieChart, Briefcase, FileText, BrainCircuit, Wrench
} from 'lucide-react';

interface MasteringBusinessModuleProps {
  onBack: () => void;
}

const Highlight = ({ children, description, color = "bg-gray-100/40", textColor = "text-gray-900", decorColor = "decoration-gray-400/40", hoverColor="hover:bg-gray-200/60" }: { children?: React.ReactNode, description: string, color?: string, textColor?: string, decorColor?: string, hoverColor?: string }) => {
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
              <p className="font-sans font-bold text-gray-400 mb-2 uppercase tracking-[0.2em] text-[9px]">The Academic Insight</p>
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
        <div className="w-12 h-12 rounded-2xl bg-stone-900 flex items-center justify-center text-gray-400 shadow-xl border border-white/10">
          <Icon size={24} />
        </div>
      </div>
      <span className="inline-flex items-center gap-2 px-3 py-1 bg-gray-50 text-gray-600 text-[10px] font-black tracking-[0.4em] uppercase rounded-full mb-4">
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
  <div className="my-12 p-8 bg-gray-50/50 border-2 border-dashed border-gray-200 rounded-3xl">
    <div className="flex items-start gap-5">
      <div className="w-11 h-11 rounded-xl bg-gray-500 text-white flex items-center justify-center shrink-0 mt-1 shadow-lg shadow-gray-500/20">
        <Flag size={20} />
      </div>
      <div>
        <h4 className="font-bold text-gray-800 text-sm uppercase tracking-widest">Your Mission (Under 5 Mins)</h4>
        <div className="text-stone-600 mt-2 font-medium leading-relaxed">
          {children}
        </div>
      </div>
    </div>
  </div>
);

const ActivityRing = ({ progress, color = "#4b5563" }: { progress: number, color?: string }) => {
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
const ABQLinkDrill = () => {
    const [step, setStep] = useState(0);
    const steps = [
        "STATE: Democratic Leadership",
        "EXPLAIN: This is a style where the manager involves employees in decision-making but retains the final say.",
        "LINK: In the text, 'Mary holds weekly meetings to get staff feedback on new menu ideas...'"
    ];
    return(
        <div className="my-10 p-8 md:p-12 bg-white rounded-[3rem] border border-stone-200 shadow-xl">
             <h4 className="font-serif text-2xl font-bold text-stone-800 text-center italic">ABQ "Link" Methodology Drill</h4>
             <AnimatePresence mode="wait">
                <motion.div key={step} initial={{opacity:0, y:10}} animate={{opacity:1, y:0}} exit={{opacity:0, y:-10}} className="mt-6 p-6 bg-stone-100 rounded-2xl min-h-[80px] flex items-center justify-center">
                    <p className="font-mono text-center text-sm">{steps[step]}</p>
                </motion.div>
             </AnimatePresence>
             <div className="flex justify-center mt-6"><button onClick={() => setStep(s => (s + 1) % steps.length)} className="px-4 py-2 bg-stone-800 text-white text-xs font-bold rounded-lg">Next Step</button></div>
        </div>
    );
};


// --- MODULE COMPONENT ---
export const MasteringBusinessModule: React.FC<{onBack: () => void}> = ({ onBack }) => {
  const [activeSection, setActiveSection] = useState(0);
  const [unlockedSection, setUnlockedSection] = useState(0);
  
  const sections = [
    { id: 'strategic-context', title: 'The Strategic Context for 2026', eyebrow: '01 // The Master Key', icon: Key },
    { id: 'exam-architecture', title: 'The Exam Architecture', eyebrow: '02 // The Blueprint', icon: PieChart },
    { id: 'abq-deep-dive', title: 'ABQ Deep Dive', eyebrow: '03 // The Pivot', icon: Briefcase },
    { id: 'science-of-scoring', title: 'The Science of Scoring', eyebrow: '04 // Grade Engineering', icon: FileText },
    { id: 'high-yield-tactics', title: 'High-Yield Tactics', eyebrow: '05 // The Toolkit', icon: Wrench },
    { id: 'study-blueprint', title: 'The Study Blueprint', eyebrow: '06 // The Action Plan', icon: BrainCircuit },
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
            <p className="text-[9px] font-black text-gray-500 uppercase tracking-[0.4em] mb-0.5 underline">Module 05</p>
            <h1 className="font-serif font-bold text-lg tracking-tight text-stone-900">Mastering Business</h1>
          </div>
        </div>

        <div className="flex-grow space-y-4 overflow-y-auto no-scrollbar pr-2 relative">
          <div className="absolute left-[21px] top-6 bottom-6 w-0.5 bg-stone-100 -z-0" />
          <div className="absolute left-[21px] top-6 bottom-6 w-0.5">
              <motion.div
                  className="w-full bg-gray-500 shadow-[0_0_10px_rgba(75,85,99,0.5)]"
                  initial={{ height: 0 }}
                  animate={{ height: sections.length > 1 ? `${(unlockedSection / (sections.length - 1)) * 100}%` : '0%' }}
              />
          </div>
          {sections.map((section, idx) => {
            const isUnlocked = idx <= unlockedSection;
            const isActive = idx === activeSection;
            const isCompleted = idx < unlockedSection;
            return (
              <button key={section.id} disabled={!isUnlocked} onClick={() => handleJumpToSection(idx)} className={`relative z-10 w-full flex items-center gap-4 p-3 rounded-xl transition-all duration-500 text-left group ${isActive ? 'bg-gray-50 shadow-sm translate-x-2' : ''} ${!isUnlocked ? 'opacity-40 grayscale cursor-not-allowed' : 'hover:bg-stone-50'}`}>
                <div className={`w-11 h-11 rounded-xl flex items-center justify-center shrink-0 border-2 transition-all duration-500 ${isCompleted ? 'bg-gray-600 border-gray-600 text-white shadow-lg' : isActive ? 'bg-white border-gray-500 text-gray-600 shadow-xl rotate-12' : 'bg-white border-stone-200 text-stone-300'}`}>
                   {isCompleted ? <CheckCircle2 size={18} /> : isActive ? <section.icon size={18} /> : <Lock size={16} />}
                </div>
                <div className="flex-grow"><p className={`text-[8px] font-black uppercase tracking-widest ${isActive ? 'text-gray-500' : 'text-stone-400'}`}>{section.eyebrow.split('// ')[1]}</p><h4 className={`text-xs font-bold leading-tight ${isActive ? 'text-stone-900' : 'text-stone-500'}`}>{section.title}</h4></div>
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
                <ReadingSection title="The Strategic Context for 2026." eyebrow="Step 1" icon={Key}>
                  <p>The Leaving Cert Business exam isn't a test of memory; it's a test of <Highlight description="The ability to decode the specific rules and expectations of the exam, from timing to the precise meaning of 'outcome verbs'.">examination literacy</Highlight>. For 2026, the game is defined by one critical fact: the compulsory Applied Business Question (ABQ) will be based on **Units 3, 4, and 5**.</p>
                  <p>This is your strategic roadmap. It shifts the focus from the wider economy to the "engine room" of a business: management, HR, finance, and marketing. A weakness in these units cannot be hidden, making the ABQ the primary filter for H1 candidates.</p>
                </ReadingSection>
              )}
               {activeSection === 1 && (
                <ReadingSection title="The Exam Architecture." eyebrow="Step 2" icon={PieChart}>
                  <p>The 3-hour Higher Level paper is an endurance test split into three sections. **Section 1 (Shorts)** is your "return on investment" section, worth 20% of the marks for about 15% of the time. **Section 2 (ABQ)** is your high-risk, high-reward section, also worth 20%. **Section 3 (Longs)** is the marathon, worth 60% of the marks and requiring four full answers.</p>
                  <p>Your timing strategy is critical. A common H1 approach is to tackle the ABQ immediately after the Shorts to leverage mental freshness before the fatigue of the long questions sets in.</p>
                </ReadingSection>
              )}
               {activeSection === 2 && (
                <ReadingSection title="ABQ Deep Dive." eyebrow="Step 3" icon={Briefcase}>
                    <p>The 2026 ABQ will almost certainly feature a business in a "growth crisis"—a company that has launched successfully but is struggling with internal chaos. You will act as a consultant. Your job is to apply theory to solve their problems.</p>
                    <p>The golden rule is the <Highlight description="The non-negotiable, 3-part structure for ABQ answers: State the theory, Explain it in your own words, and Link it with a direct quote from the text.">"Link" Methodology</Highlight>. Failure to quote directly from the case study is the single biggest cause of lost marks. It's a mechanical process: State, Explain, Link. Master this algorithm.</p>
                    <ABQLinkDrill />
                </ReadingSection>
              )}
               {activeSection === 3 && (
                <ReadingSection title="The Science of Scoring." eyebrow="Step 4" icon={FileText}>
                  <p>To get a H1, you must write for the examiner. The marking scheme is a rigid code. The standard unit of currency is the "point," worth 5 marks in a long question. To secure these marks, you must use a structured formula: <Highlight description="The standard formula for a 5-mark point: State the point, Explain it, and give an Example.">"SEE"</Highlight>. For a H1, you need the advanced <Highlight description="The H1 version of the formula, expanding the 'Explain' part into two distinct sentences to ensure full marks are captured.">"SEEE"</Highlight> version.</p>
                  <p>You must also decode the <Highlight description="The specific verb used by the SEC in a question (e.g., State, Explain, Evaluate) which dictates the required depth and structure of your answer.">"Outcome Verb."</Highlight> "State" requires a list. "Explain" requires a definition. "Evaluate" requires a judgment, which is the key differentiator for top grades. Always add a separate mini-paragraph explicitly labelled **"Evaluation:"** to secure these marks.</p>
                </ReadingSection>
              )}
              {activeSection === 4 && (
                <ReadingSection title="High-Yield Tactics." eyebrow="Step 5" icon={Wrench}>
                  <p>In Section 1 (Short Questions), use the <Highlight description="The strategy of answering all available short questions (e.g., 10 or 12) to create a safety net, as only your best 8 will be counted.">"Surplus" Strategy</Highlight>: answer all the questions. It takes little extra time and insures you against a calculation error.</p>
                  <p>In Section 3 (Long Questions), avoid the <Highlight description="The phenomenon of writing lengthy paragraphs without any specific keywords or facts, which scores zero marks.">"Waffle" Phenomenon</Highlight> by using the SEEE structure. Every sentence must have a purpose. Also, avoid the <Highlight description="Making the same point twice using different words. Examiners will only award marks for it once.">"Repetition" Trap</Highlight> when asked for multiple "impacts" or "benefits"—make sure your points are distinct (e.g., one financial, one marketing).</p>
                </ReadingSection>
              )}
               {activeSection === 5 && (
                <ReadingSection title="The Study Blueprint." eyebrow="Step 6" icon={BrainCircuit}>
                  <p>Success is a marathon, not a sprint. Passive reading yields only 10% retention. <Highlight description="Actively testing yourself by retrieving information from memory. This is the most effective study method, yielding up to 60% retention.">Active Recall</Highlight> is the engine of learning. Use spider diagrams and flashcards to test yourself, not just to make notes.</p>
                  <p>Your study plan should be phased. **Phase 1 (Sept-Dec):** Deep dive on the ABQ units (3, 4, 5). **Phase 2 (Jan-Mar):** Cover the other units and begin timed long questions. **Phase 3 (Apr-May):** Use <Highlight description="Mixing questions from different units in a single study session to simulate the randomness of the exam and train your problem-spotting skills.">"Interleaved" Practice</Highlight> with past papers. This is not about just learning the material; it's about learning how to perform.</p>
                   <MicroCommitment>
                    <p>Go to your Business notes. Pick one topic. Create a one-page "spider diagram" summary of it *from memory*. Then, open the book and check what you missed. You've just started using active recall.</p>
                  </MicroCommitment>
                </ReadingSection>
              )}
              <footer className="mt-24 flex items-center justify-between pt-12 border-t border-stone-200/60 px-4">
                <motion.button whileHover={{ scale: 1.05 }} whileTap={{ scale: 0.95 }} onClick={handlePrev} disabled={activeSection === 0} className={`flex items-center gap-4 bg-stone-100 text-stone-800 px-8 py-4 rounded-xl font-black text-[10px] uppercase tracking-widest transition-all shadow-sm ${activeSection === 0 ? 'opacity-0 pointer-events-none' : ''}`}>
                  <ArrowLeft size={16} /> Prev
                </motion.button>
                <motion.button whileHover={{ scale: 1.05 }} whileTap={{ scale: 0.95 }} onClick={handleCompleteSection} className="group relative flex items-center gap-4 bg-stone-900 text-white px-12 py-6 rounded-2xl font-black text-[12px] uppercase tracking-widest hover:bg-gray-600 transition-all shadow-[0_20px_50px_rgba(0,0,0,0.2)] overflow-hidden">
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
