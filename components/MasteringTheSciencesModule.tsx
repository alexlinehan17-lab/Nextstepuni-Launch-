/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
*/

import React, { useState } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { 
  ArrowLeft, CheckCircle2, ArrowRight, 
  Lock, Flag, Key, Leaf, Beaker, Atom, Sprout, BrainCircuit, Wrench
} from 'lucide-react';

interface MasteringTheSciencesModuleProps {
  onBack: () => void;
}

const Highlight = ({ children, description, color = "bg-emerald-100/40", textColor = "text-emerald-900", decorColor = "decoration-emerald-400/40", hoverColor="hover:bg-emerald-200/60" }: { children?: React.ReactNode, description: string, color?: string, textColor?: string, decorColor?: string, hoverColor?: string }) => {
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
              <p className="font-sans font-bold text-emerald-400 mb-2 uppercase tracking-[0.2em] text-[9px]">The Academic Insight</p>
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
        <div className="w-12 h-12 rounded-2xl bg-stone-900 flex items-center justify-center text-emerald-400 shadow-xl border border-white/10">
          <Icon size={24} />
        </div>
      </div>
      <span className="inline-flex items-center gap-2 px-3 py-1 bg-emerald-50 text-emerald-600 text-[10px] font-black tracking-[0.4em] uppercase rounded-full mb-4">
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
  <div className="my-12 p-8 bg-emerald-50/50 border-2 border-dashed border-emerald-200 rounded-3xl">
    <div className="flex items-start gap-5">
      <div className="w-11 h-11 rounded-xl bg-emerald-500 text-white flex items-center justify-center shrink-0 mt-1 shadow-lg shadow-emerald-500/20">
        <Flag size={20} />
      </div>
      <div>
        <h4 className="font-bold text-emerald-800 text-sm uppercase tracking-widest">Your Mission (Under 5 Mins)</h4>
        <div className="text-stone-600 mt-2 font-medium leading-relaxed">
          {children}
        </div>
      </div>
    </div>
  </div>
);

const ActivityRing = ({ progress, color = "#10b981" }: { progress: number, color?: string }) => {
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
const CurlyArrowDrill = () => {
    const [start, setStart] = useState(false);
    const [end, setEnd] = useState(false);
    
    return(
        <div className="my-10 p-8 md:p-12 bg-white rounded-[3rem] border border-stone-200 shadow-xl text-center">
            <h4 className="font-serif text-2xl font-bold text-stone-800 text-center italic">"Curly Arrow" Drill</h4>
            <p className="text-sm text-stone-500 mb-6">Draw the arrow for this step: Cl⁻ attacking a carbocation.</p>
            <div className="flex justify-center items-center gap-4 text-3xl font-mono">
                <button onClick={() => setStart(true)} className="relative p-2">Cl<span className="absolute -top-1 -right-1 text-lg">-</span></button>
                <span>+</span>
                <button onClick={() => setEnd(true)} className="relative p-2">C<span className="absolute -top-1 -right-1 text-lg">+</span></button>
            </div>
            {start && end && <p className="text-emerald-600 font-bold mt-4">Correct! Arrow from electron source (Cl⁻) to electron sink (C⁺).</p>}
        </div>
    );
};

// --- MODULE COMPONENT ---
export const MasteringTheSciencesModule: React.FC<{onBack: () => void}> = ({ onBack }) => {
  const [activeSection, setActiveSection] = useState(0);
  const [unlockedSection, setUnlockedSection] = useState(0);
  
  const sections = [
    { id: 'hidden-curriculum', title: 'The Hidden Curriculum', eyebrow: '01 // The Master Key', icon: Key },
    { id: 'biology', title: 'Biology: Precision & Breadth', eyebrow: '02 // The Encyclopedia', icon: Leaf },
    { id: 'chemistry', title: 'Chemistry: Molecular Logic', eyebrow: '03 // The Architect', icon: Beaker },
    { id: 'physics', title: 'Physics: Abstract Logic', eyebrow: '04 // The Engineer', icon: Atom },
    { id: 'ag-science', title: 'Ag Science: The Scientific Method', eyebrow: '05 // The Investigator', icon: Sprout },
    { id: 'cognitive-strategies', title: 'Cognitive Grade Optimization', eyebrow: '06 // The Toolkit', icon: BrainCircuit },
    { id: 'action-plan', title: 'Your Action Plan', eyebrow: '07 // The Blueprint', icon: Flag },
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
            <p className="text-[9px] font-black text-emerald-500 uppercase tracking-[0.4em] mb-0.5 underline">Module 03</p>
            <h1 className="font-serif font-bold text-lg tracking-tight text-stone-900">Mastering the Sciences</h1>
          </div>
        </div>

        <div className="flex-grow space-y-4 overflow-y-auto no-scrollbar pr-2 relative">
          <div className="absolute left-[21px] top-6 bottom-6 w-0.5 bg-stone-100 -z-0" />
          <div className="absolute left-[21px] top-6 bottom-6 w-0.5">
              <motion.div
                  className="w-full bg-emerald-500 shadow-[0_0_10px_rgba(16,185,129,0.5)]"
                  initial={{ height: 0 }}
                  animate={{ height: sections.length > 1 ? `${(unlockedSection / (sections.length - 1)) * 100}%` : '0%' }}
              />
          </div>
          {sections.map((section, idx) => {
            const isUnlocked = idx <= unlockedSection;
            const isActive = idx === activeSection;
            const isCompleted = idx < unlockedSection;
            return (
              <button key={section.id} disabled={!isUnlocked} onClick={() => handleJumpToSection(idx)} className={`relative z-10 w-full flex items-center gap-4 p-3 rounded-xl transition-all duration-500 text-left group ${isActive ? 'bg-emerald-50 shadow-sm translate-x-2' : ''} ${!isUnlocked ? 'opacity-40 grayscale cursor-not-allowed' : 'hover:bg-stone-50'}`}>
                <div className={`w-11 h-11 rounded-xl flex items-center justify-center shrink-0 border-2 transition-all duration-500 ${isCompleted ? 'bg-emerald-600 border-emerald-600 text-white shadow-lg' : isActive ? 'bg-white border-emerald-500 text-emerald-600 shadow-xl rotate-12' : 'bg-white border-stone-200 text-stone-300'}`}>
                   {isCompleted ? <CheckCircle2 size={18} /> : isActive ? <section.icon size={18} /> : <Lock size={16} />}
                </div>
                <div className="flex-grow"><p className={`text-[8px] font-black uppercase tracking-widest ${isActive ? 'text-emerald-500' : 'text-stone-400'}`}>{section.eyebrow.split('// ')[1]}</p><h4 className={`text-xs font-bold leading-tight ${isActive ? 'text-stone-900' : 'text-stone-500'}`}>{section.title}</h4></div>
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
                <ReadingSection title="The Hidden Curriculum." eyebrow="Step 1" icon={Key}>
                  <p>Success in the Leaving Cert sciences is not just a test of knowledge; it's a test of strategic alignment. Each subject—Biology, Chemistry, Physics, and Ag Science—has its own "hidden curriculum," an unwritten set of rules dictated by the marking scheme. Mastering this hidden curriculum is the key to unlocking a H1.</p>
                  <p>This module provides the decryption key for each science, revealing the specific cognitive approach and "high-yield" content that delivers the most marks. You will learn to think like an examiner and engineer your answers for maximum credit.</p>
                </ReadingSection>
              )}
              {activeSection === 1 && (
                <ReadingSection title="Biology: Precision & Breadth." eyebrow="Step 2" icon={Leaf}>
                  <p>Biology rewards breadth of knowledge and, above all, <Highlight description="The marking scheme demands specific, non-negotiable keywords. Synonyms are often rejected. 'Specificity' or 'induced fit model' must be used for the active site.">terminological precision</Highlight>. An answer without the correct keyword is worthless. Definitions must be memorized verbatim. The exam structure is 5-3-4 (5/7 shorts, 3/4 experiments, 4/6 longs), and omitting any of the 22 mandatory experiments is a dangerous strategy. Beware the <Highlight description="In Section A, an incorrect third answer to a two-part question can cancel out a correct one. Adhere strictly to the quantity requested.">'Surplus Answer' Risk</Highlight> in short questions.</p>
                </ReadingSection>
              )}
              {activeSection === 2 && (
                <ReadingSection title="Chemistry: Molecular Logic." eyebrow="Step 3" icon={Beaker}>
                  <p>Chemistry demands dual competency: visualizing molecular interactions and executing complex calculations. Section A (experiments) is your <Highlight description="Section A, covering mandatory experiments like titrations, is highly predictable and can account for up to 38% of your grade if all three questions are answered.">Volumetric Anchor</Highlight>, offering predictable marks. Master the procedural precision of titrations and the visualization of organic apparatus.</p>
                  <p>Organic Chemistry (40%) requires you to master reaction maps and the <Highlight description="A formalism showing the movement of electron pairs. A curly arrow MUST originate from a bond or lone pair and point to an atom. Errors here are severely penalized.">'Curly Arrow' Formalism</Highlight> for mechanisms. A "Texas Carbon" (five-bonded carbon) is a zero-mark error. Stoichiometry is foundational; every calculation must begin by converting to Moles.</p>
                  <CurlyArrowDrill />
                </ReadingSection>
              )}
               {activeSection === 3 && (
                <ReadingSection title="Physics: Abstract Logic." eyebrow="Step 4" icon={Atom}>
                  <p>Physics rewards the application of abstract concepts to novel problems. Section A is your experimental portfolio and the source of "easy" marks if you master <Highlight description="Key protocols like ensuring the independent variable is on the X-axis and calculating slope from the line of best fit, not table points.">graphing protocols</Highlight>. All derivations must be learned by heart, including the geometric steps.</p>
                  <p>For novel questions, your secret weapon is <Highlight description="Using the units of physical quantities to deduce or check a formula (e.g., if Force is in N and Area is in m², Pressure must be N/m²).">Unit Algebra</Highlight>. Forgetting to convert from cm to m is the single most frequent cause of lost marks. Always double-check your calculator is in **Degree** mode for trigonometric functions.</p>
                </ReadingSection>
              )}
               {activeSection === 4 && (
                <ReadingSection title="Ag Science: The Scientific Method." eyebrow="Step 5" icon={Sprout}>
                  <p>The new Ag Science course is a radical shift from "farming facts" to "scientific principles." The <Highlight description="An Individual Investigative Study worth 25% of the total grade. It requires a formal scientific report with a testable hypothesis, experimental design, and statistical analysis.">Individual Investigative Study (IIS)</Highlight> is a capstone project that demands scientific rigor. A descriptive project without a clear hypothesis will be heavily penalized.</p>
                  <p>The written paper is now more <Highlight description="Linking topics across different strands (e.g., how fertilizer use in Crops affects water quality in the Environment strand).">synoptic</Highlight>, demanding critical thinking and data analysis, not just recall. Questions on experiments require the same rigor as Biology or Physics.</p>
                </ReadingSection>
              )}
              {activeSection === 5 && (
                <ReadingSection title="Cognitive Grade Optimization." eyebrow="Step 6" icon={BrainCircuit}>
                  <p>To master these diverse subjects, you must abandon passive re-reading. <Highlight description="Mixing different topics or subjects within a single study session. It feels harder but builds the crucial skill of identifying problem types.">Interleaving</Highlight> is superior to blocked practice for STEM subjects because it forces your brain to constantly "reload" context, strengthening retrieval pathways. A 90-minute session could involve a Physics problem, a Chemistry equation, and a Biology definition.</p>
                  <p>The most effective method for memorizing the hundreds of definitions in Biology and Ag Science is a combination of <Highlight description="Forcing your brain to retrieve information from memory (e.g., using the 'Blurting' method).">Active Recall</Highlight> and <Highlight description="Using tools like Anki or Quizlet to review information at increasing intervals, combating the 'forgetting curve'.">Spaced Repetition</Highlight>.</p>
                </ReadingSection>
              )}
              {activeSection === 6 && (
                <ReadingSection title="Your Action Plan." eyebrow="Step 7" icon={Flag}>
                  <p>You now have the strategic blueprint for each of the Leaving Cert sciences. You understand the "hidden curriculum" and the specific cognitive tools required for each. The path to a H1 is not about working harder, but about working smarter, with strategic engagement with the assessment architecture.</p>
                  <MicroCommitment>
                    <p>Pick ONE subject. Go to the SEC website and download the most recent Chief Examiner's Report. Read only the "Recommendations to Candidates" section. You've just gained access to the official cheat sheet.</p>
                  </MicroCommitment>
                </ReadingSection>
              )}
              <footer className="mt-24 flex items-center justify-between pt-12 border-t border-stone-200/60 px-4">
                <motion.button whileHover={{ scale: 1.05 }} whileTap={{ scale: 0.95 }} onClick={handlePrev} disabled={activeSection === 0} className={`flex items-center gap-4 bg-stone-100 text-stone-800 px-8 py-4 rounded-xl font-black text-[10px] uppercase tracking-widest transition-all shadow-sm ${activeSection === 0 ? 'opacity-0 pointer-events-none' : ''}`}>
                  <ArrowLeft size={16} /> Prev
                </motion.button>
                <motion.button whileHover={{ scale: 1.05 }} whileTap={{ scale: 0.95 }} onClick={handleCompleteSection} className="group relative flex items-center gap-4 bg-stone-900 text-white px-12 py-6 rounded-2xl font-black text-[12px] uppercase tracking-widest hover:bg-emerald-600 transition-all shadow-[0_20px_50px_rgba(0,0,0,0.2)] overflow-hidden">
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
