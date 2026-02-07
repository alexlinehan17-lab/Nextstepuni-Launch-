/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
*/

import React, { useState } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { 
  ArrowLeft, CheckCircle2, ArrowRight, 
  Lock, Flag, Key, Landmark, Globe, FileBadge2, Brain, Wrench
} from 'lucide-react';

interface MasteringTheHumanitiesModuleProps {
  onBack: () => void;
}

const Highlight = ({ children, description, color = "bg-pink-100/40", textColor = "text-pink-900", decorColor = "decoration-pink-400/40", hoverColor="hover:bg-pink-200/60" }: { children?: React.ReactNode, description: string, color?: string, textColor?: string, decorColor?: string, hoverColor?: string }) => {
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
              <p className="font-sans font-bold text-pink-400 mb-2 uppercase tracking-[0.2em] text-[9px]">The Academic Insight</p>
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
        <div className="w-12 h-12 rounded-2xl bg-stone-900 flex items-center justify-center text-pink-400 shadow-xl border border-white/10">
          <Icon size={24} />
        </div>
      </div>
      <span className="inline-flex items-center gap-2 px-3 py-1 bg-pink-50 text-pink-600 text-[10px] font-black tracking-[0.4em] uppercase rounded-full mb-4">
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
  <div className="my-12 p-8 bg-pink-50/50 border-2 border-dashed border-pink-200 rounded-3xl">
    <div className="flex items-start gap-5">
      <div className="w-11 h-11 rounded-xl bg-pink-500 text-white flex items-center justify-center shrink-0 mt-1 shadow-lg shadow-pink-500/20">
        <Flag size={20} />
      </div>
      <div>
        <h4 className="font-bold text-pink-800 text-sm uppercase tracking-widest">Your Mission (Under 5 Mins)</h4>
        <div className="text-stone-600 mt-2 font-medium leading-relaxed">
          {children}
        </div>
      </div>
    </div>
  </div>
);

const ActivityRing = ({ progress, color = "#ec4899" }: { progress: number, color?: string }) => {
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
const HistoryGrader = () => {
    const [cm, setCm] = useState(60);
    const [oe, setOe] = useState(15);
    const total = cm + oe;
    const grade = total >= 90 ? 'H1' : total >= 80 ? 'H2' : total >= 70 ? 'H3' : total >= 60 ? 'H4' : 'H5';
    
    return(
        <div className="my-10 p-8 md:p-12 bg-white rounded-[3rem] border border-stone-200 shadow-xl">
            <h4 className="font-serif text-2xl font-bold text-stone-800 text-center italic">CM/OE Grader</h4>
            <div className="grid grid-cols-2 gap-6 items-center">
                <div className="space-y-4">
                    <div><label className="text-xs font-bold">CM (Content): {cm}/60</label><input type="range" min="0" max="60" value={cm} onChange={e=>setCm(parseInt(e.target.value))} className="w-full"/></div>
                    <div><label className="text-xs font-bold">OE (Argument): {oe}/40</label><input type="range" min="0" max="40" value={oe} onChange={e=>setOe(parseInt(e.target.value))} className="w-full"/></div>
                </div>
                <div className="text-center">
                    <p className="text-sm">Final Grade:</p>
                    <p className="text-6xl font-black text-pink-500">{grade}</p>
                </div>
            </div>
        </div>
    );
};

const CourseworkCalculator = () => {
    const [project, setProject] = useState(90);
    const required = Math.max(0, (450 - project*0.2) / 0.8); // 450 is 90% of 500 for H1
    return(
        <div className="my-10 p-8 md:p-12 bg-white rounded-[3rem] border border-stone-200 shadow-xl">
             <h4 className="font-serif text-2xl font-bold text-stone-800 text-center italic">The Coursework Advantage</h4>
             <p className="text-center text-sm text-stone-500 mb-6">See how your 20% project changes the exam requirement for a H1.</p>
             <div>
                <label className="font-bold text-sm">Your Project Grade: {project}%</label>
                <input type="range" min="40" max="100" value={project} onChange={e=>setProject(parseInt(e.target.value))} className="w-full"/>
             </div>
             <div className="mt-6 p-4 bg-stone-900 rounded-xl text-center text-white">
                Required Exam Mark for H1: <span className="font-bold text-2xl text-pink-400">{required.toFixed(1)}%</span>
             </div>
        </div>
    );
}

// --- MODULE COMPONENT ---
export const MasteringTheHumanitiesModule: React.FC<{onBack: () => void}> = ({ onBack }) => {
  const [activeSection, setActiveSection] = useState(0);
  const [unlockedSection, setUnlockedSection] = useState(0);
  
  const sections = [
    { id: 'hidden-curriculum', title: 'The Hidden Curriculum', eyebrow: '01 // The Master Key', icon: Key },
    { id: 'history-engine', title: 'The History Engine', eyebrow: '02 // CM + OE', icon: Landmark },
    { id: 'geography-algorithm', title: 'The Geography Algorithm', eyebrow: '03 // SRPs', icon: Globe },
    { id: 'coursework-advantage', title: 'The Coursework Advantage', eyebrow: '04 // Banking Marks', icon: FileBadge2 },
    { id: 'universal-toolkit', title: 'The Universal Toolkit', eyebrow: '05 // The PEE Chain', icon: Brain },
    { id: 'blueprint', title: 'Your Blueprint', eyebrow: '06 // The Action Plan', icon: Wrench },
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
            <p className="text-[9px] font-black text-pink-500 uppercase tracking-[0.4em] mb-0.5 underline">Module 04</p>
            <h1 className="font-serif font-bold text-lg tracking-tight text-stone-900">Mastering the Humanities</h1>
          </div>
        </div>

        <div className="flex-grow space-y-4 overflow-y-auto no-scrollbar pr-2 relative">
          <div className="absolute left-[21px] top-6 bottom-6 w-0.5 bg-stone-100 -z-0" />
          <div className="absolute left-[21px] top-6 bottom-6 w-0.5">
              <motion.div
                  className="w-full bg-pink-500 shadow-[0_0_10px_rgba(236,72,153,0.5)]"
                  initial={{ height: 0 }}
                  animate={{ height: sections.length > 1 ? `${(unlockedSection / (sections.length - 1)) * 100}%` : '0%' }}
              />
          </div>
          {sections.map((section, idx) => {
            const isUnlocked = idx <= unlockedSection;
            const isActive = idx === activeSection;
            const isCompleted = idx < unlockedSection;
            return (
              <button key={section.id} disabled={!isUnlocked} onClick={() => handleJumpToSection(idx)} className={`relative z-10 w-full flex items-center gap-4 p-3 rounded-xl transition-all duration-500 text-left group ${isActive ? 'bg-pink-50 shadow-sm translate-x-2' : ''} ${!isUnlocked ? 'opacity-40 grayscale cursor-not-allowed' : 'hover:bg-stone-50'}`}>
                <div className={`w-11 h-11 rounded-xl flex items-center justify-center shrink-0 border-2 transition-all duration-500 ${isCompleted ? 'bg-pink-600 border-pink-600 text-white shadow-lg' : isActive ? 'bg-white border-pink-500 text-pink-600 shadow-xl rotate-12' : 'bg-white border-stone-200 text-stone-300'}`}>
                   {isCompleted ? <CheckCircle2 size={18} /> : isActive ? <section.icon size={18} /> : <Lock size={16} />}
                </div>
                <div className="flex-grow"><p className={`text-[8px] font-black uppercase tracking-widest ${isActive ? 'text-pink-500' : 'text-stone-400'}`}>{section.eyebrow.split('// ')[1]}</p><h4 className={`text-xs font-bold leading-tight ${isActive ? 'text-stone-900' : 'text-stone-500'}`}>{section.title}</h4></div>
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
                  <p>In the Leaving Cert Humanities, the gap between a H3 and a H1 is rarely a lack of knowledge. It's a lack of <Highlight description="The ability to align your knowledge with the specific, often unwritten, rules of the marking scheme for each subject.">strategic application</Highlight>. Each subject has a "hidden curriculum" and trades in a different "currency" of marks. To succeed, you must become fluent in each of these currencies.</p>
                </ReadingSection>
              )}
              {activeSection === 1 && (
                <ReadingSection title="The History Engine." eyebrow="Step 2" icon={Landmark}>
                  <p>The History essay is not marked as one piece. It's a dual-process system. The <Highlight description="Cumulative Mark (60/100): Rewards the quantity and accuracy of historical facts. The strategy is volume - aim for 8-10 dense paragraphs.">Cumulative Mark (CM)</Highlight> is a measure of historical content. The <Highlight description="Overall Evaluation (40/100): A qualitative multiplier that assesses the quality of your argument, its relevance to the specific question, and your historical analysis.">Overall Evaluation (OE)</Highlight> assesses your skill as a historian.</p>
                  <p>The classic H3 trap is maxing out the CM with a pre-learned essay but scoring low on OE because the essay doesn't answer the specific question asked. Your argument is the engine; facts are just the fuel.</p>
                  <HistoryGrader/>
                </ReadingSection>
              )}
              {activeSection === 2 && (
                <ReadingSection title="The Geography Algorithm." eyebrow="Step 3" icon={Globe}>
                  <p>Geography operates on a completely different logic. Its currency is the <Highlight description="A Significant Relevant Point is a single, developed piece of factual information, typically worth 2 marks. A 30-mark essay requires 15 of them.">Significant Relevant Point (SRP)</Highlight>. An essay is simply a container for accumulating these discrete units of information. The logic is algorithmic and quantitative.</p>
                  <p>A weak answer gives a keyword; a strong answer gives a statement plus development. For example, "Limestone dissolves" (0 marks) vs. "Carbonation occurs when rainwater absorbs CO2, forming a weak carbonic acid" (2 marks). Your job is to become an SRP-generating machine.</p>
                </ReadingSection>
              )}
              {activeSection === 3 && (
                <ReadingSection title="The Coursework Advantage." eyebrow="Step 4" icon={FileBadge2}>
                  <p>The single most effective statistical intervention you can make is to maximize your coursework grade. For subjects like History (RSR), Geography (Fieldwork), and Politics & Society (Citizenship Project), 20% of your final grade is "banked" before you even enter the exam hall. This is a massive strategic advantage.</p>
                  <p>A student who gets 90/100 (18%) on their project only needs 72% on the written paper to get a H1. A student with a 50/100 project (10%) needs 80%—a much harder task under pressure. This is a controllable variable you must optimize.</p>
                  <CourseworkCalculator/>
                </ReadingSection>
              )}
              {activeSection === 4 && (
                <ReadingSection title="The Universal Toolkit." eyebrow="Step 5" icon={Brain}>
                  <p>While the currencies differ, the underlying structure of a good argument is universal. The <Highlight description="A robust heuristic for essay writing: plan 3-4 distinct arguments, structure each paragraph using PEE, and in discursive subjects, consider 3 perspectives (Thesis, Antithesis, Synthesis).">"Rule of Three"</Highlight> is a powerful framework. Plan **3 core arguments** for every essay. Structure each paragraph using the **PEE chain**: **P**oint (your topic sentence), **E**vidence (your fact, quote, or SRP), and **E**xplanation (the "So what?" factor that links the evidence back to your point).</p>
                </ReadingSection>
              )}
              {activeSection === 5 && (
                <ReadingSection title="Your Blueprint." eyebrow="Step 6" icon={Wrench}>
                  <p>You now have the decryption key for the Humanities exams. You understand the different "currencies" and the universal structures. Your task now is to become a "grade engineer"—to consciously align every answer you write with the specific demands of the marking scheme.</p>
                  <MicroCommitment>
                    <p>Go to the SEC website and download the marking scheme for your favourite Humanities subject. Spend 10 minutes reading it. This is no longer just an exam; it's a system you are learning to master.</p>
                  </MicroCommitment>
                </ReadingSection>
              )}
              <footer className="mt-24 flex items-center justify-between pt-12 border-t border-stone-200/60 px-4">
                <motion.button whileHover={{ scale: 1.05 }} whileTap={{ scale: 0.95 }} onClick={handlePrev} disabled={activeSection === 0} className={`flex items-center gap-4 bg-stone-100 text-stone-800 px-8 py-4 rounded-xl font-black text-[10px] uppercase tracking-widest transition-all shadow-sm ${activeSection === 0 ? 'opacity-0 pointer-events-none' : ''}`}>
                  <ArrowLeft size={16} /> Prev
                </motion.button>
                <motion.button whileHover={{ scale: 1.05 }} whileTap={{ scale: 0.95 }} onClick={handleCompleteSection} className="group relative flex items-center gap-4 bg-stone-900 text-white px-12 py-6 rounded-2xl font-black text-[12px] uppercase tracking-widest hover:bg-pink-600 transition-all shadow-[0_20px_50px_rgba(0,0,0,0.2)] overflow-hidden">
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
