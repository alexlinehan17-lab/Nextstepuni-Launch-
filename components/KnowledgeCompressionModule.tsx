
/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
*/

import React, { useState } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { 
  ArrowLeft, CheckCircle2, ArrowRight, 
  Lock, Flag, Target, Brain, SlidersHorizontal, Wrench, Compass, BarChart
} from 'lucide-react';

interface KnowledgeCompressionModuleProps {
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

// --- INTERACTIVE COMPONENT: SyllabusDeconstructor ---
const mathsSyllabus = {
  subject: "Mathematics (Higher Level)",
  strands: [
    {
      name: "Statistics & Probability",
      topics: [
        { name: "Inferential Statistics", frequency: 5, details: "Focus on hypothesis testing. Often a full long question." },
        { name: "Probability", frequency: 5, details: "High-value topic, frequently combined with other areas." },
        { name: "Descriptive Statistics", frequency: 3, details: "Core skills, but usually part of a larger question." },
      ]
    },
    {
      name: "Geometry & Trigonometry",
      topics: [
        { name: "Trigonometry", frequency: 5, details: "Guaranteed long question. Master 3D problems and proofs." },
        { name: "The Line & Circle", frequency: 4, details: "Essential coordinate geometry skills. Very frequent questions." },
        { name: "Enlargements/Constructions", frequency: 2, details: "Lower frequency, but can be easy marks if prepared." },
      ]
    },
    {
      name: "Functions & Calculus",
      topics: [
        { name: "Differentiation", frequency: 5, details: "The absolute core of Paper 1. Master rules and applications." },
        { name: "Integration", frequency: 5, details: "The other core of Paper 1. Focus on finding areas." },
        { name: "Functions", frequency: 3, details: "Often appears as a context for calculus questions." },
      ]
    },
    {
      name: "Algebra",
      topics: [
        { name: "Core Algebra", frequency: 5, details: "The language of the entire course. Essential for everything." },
        { name: "Sequences & Series", frequency: 4, details: "Predictable question style. Excellent for banking marks." },
      ]
    },
     {
      name: "Number",
      topics: [
        { name: "Complex Numbers", frequency: 4, details: "Very common long question. De Moivre's Theorem is key." },
        { name: "Financial Maths", frequency: 3, details: "Often a full question. Master the formula." },
      ]
    },
  ]
};

const SyllabusDeconstructor = () => {
    const [selectedTopic, setSelectedTopic] = useState<any>(null);

    const totalFrequency = mathsSyllabus.strands.reduce((sum, strand) => 
        sum + strand.topics.reduce((topicSum, topic) => topicSum + topic.frequency, 0), 0);
    
    const colors = ["#e0f2f1", "#b2dfdb", "#80cbc4", "#4db6ac", "#26a69a"];

    return (
        <div className="my-10 p-4 md:p-8 bg-white rounded-[2rem] border border-stone-200 shadow-xl">
            <h4 className="font-serif text-2xl font-bold text-stone-800 text-center italic">Syllabus Deconstructor</h4>
            <p className="text-center text-sm text-stone-500 mb-6">{mathsSyllabus.subject}</p>
            
            <div className="w-full h-[500px] bg-stone-50 rounded-lg p-2 flex flex-col gap-2">
                {mathsSyllabus.strands.map(strand => {
                    const strandTotalFreq = strand.topics.reduce((sum, topic) => sum + topic.frequency, 0);
                    const strandFlex = (strandTotalFreq / totalFrequency) * 100;
                    return (
                        <div key={strand.name} style={{flexGrow: strandFlex}} className="flex gap-2">
                            {strand.topics.map(topic => {
                                const topicFlex = (topic.frequency / strandTotalFreq) * 100;
                                return (
                                    <motion.div 
                                        key={topic.name} 
                                        style={{flexGrow: topicFlex, backgroundColor: colors[topic.frequency-1]}}
                                        className="rounded-md p-2 text-xs font-bold text-stone-800 cursor-pointer flex items-center justify-center text-center"
                                        whileHover={{scale: 1.05, zIndex: 10}}
                                        onClick={() => setSelectedTopic(topic)}
                                    >
                                        {topic.name}
                                    </motion.div>
                                );
                            })}
                        </div>
                    );
                })}
            </div>
            <AnimatePresence>
                {selectedTopic && (
                    <motion.div 
                        initial={{ opacity: 0, y: 10 }}
                        animate={{ opacity: 1, y: 0 }}
                        exit={{ opacity: 0, y: 10 }}
                        className="mt-4 p-4 bg-stone-900 text-white rounded-xl"
                    >
                        <h5 className="font-bold text-teal-300">{selectedTopic.name}</h5>
                        <p className="text-sm mt-1">{selectedTopic.details}</p>
                        <button onClick={() => setSelectedTopic(null)} className="text-xs text-stone-400 mt-2">Close</button>
                    </motion.div>
                )}
            </AnimatePresence>
        </div>
    );
};

// --- MODULE COMPONENT ---
export const KnowledgeCompressionModule: React.FC<KnowledgeCompressionModuleProps> = ({ onBack }) => {
  const [activeSection, setActiveSection] = useState(0);
  const [unlockedSection, setUnlockedSection] = useState(0);
  
  const sections = [
    { id: 'information-overload', title: 'Information Overload', eyebrow: '01 // The Problem', icon: Target },
    { id: 'pareto-principle', title: 'The 80/20 Rule', eyebrow: '02 // The Principle', icon: SlidersHorizontal },
    { id: 'syllabus-deconstructor', title: 'The Syllabus Deconstructor', eyebrow: '03 // The Tool', icon: Compass },
    { id: 'distillation-techniques', title: 'Distillation Techniques', eyebrow: '04 // The Methods', icon: Brain },
    { id: 'high-yield-assets', title: 'High-Yield Assets', eyebrow: '05 // The Output', icon: BarChart },
    { id: 'implementation', title: 'Your Triage Plan', eyebrow: '06 // The Action Plan', icon: Wrench },
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
            <p className="text-[9px] font-black text-teal-500 uppercase tracking-[0.4em] mb-0.5 underline">Module 06</p>
            <h1 className="font-serif font-bold text-lg tracking-tight text-stone-900">Knowledge Compression</h1>
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
           <ActivityRing progress={progress} color="#14b8a6" /><p className="text-[11px] font-black text-stone-900 uppercase tracking-widest text-center">Progress</p>
        </div>
      </aside>

      <main className="flex-grow flex flex-col items-center py-10 md:py-24 px-6 md:px-16 overflow-y-auto h-screen relative">
        <div className="absolute inset-0 bg-[radial-gradient(#e5e7eb_1px,transparent_1px)] [background-size:32px_32px] opacity-40 pointer-events-none" />
        <div className="w-full max-w-4xl relative z-10">
          <AnimatePresence mode="wait">
            <motion.div key={activeSection} initial={{ opacity: 0, x: 20 }} animate={{ opacity: 1, x: 0 }} exit={{ opacity: 0, x: -20 }} transition={{ duration: 0.6, ease: [0.16, 1, 0.3, 1] }}>
              {activeSection === 0 && (
                <ReadingSection title="The Information Overload." eyebrow="Step 1" icon={Target}>
                  <p>You have the best study techniques in the world. But now you face a new problem: there's too much stuff to study. A typical Leaving Cert subject has hundreds of potential topics. Trying to learn everything equally is a recipe for burnout and shallow knowledge. It's like trying to drink from a firehose.</p>
                  <p>The goal is not to cover everything; it's to cover the *right* things. To do this, you need to stop thinking like a student and start thinking like a strategic analyst. You need a system for <Highlight description="The process of sorting information based on its importance and urgency to prioritize your attention and effort.">Information Triage</Highlight>.</p>
                </ReadingSection>
              )}
              {activeSection === 1 && (
                <ReadingSection title="The 80/20 Rule." eyebrow="Step 2" icon={SlidersHorizontal}>
                  <p>The core principle of information triage is the <Highlight description="Also known as the Pareto Principle. It states that for many events, roughly 80% of the effects come from 20% of the causes. In studying, this means 80% of your marks will come from 20% of the syllabus.">80/20 Rule</Highlight>. Not all topics are created equal. A small number of "high-yield" topics consistently deliver the vast majority of the marks on the exam papers year after year.</p>
                  <p>Your job is to identify this "vital few" and ruthlessly prioritize them. This isn't about ignoring the rest of the syllabus. It's about allocating your most precious resource—your focused attention—where it will have the biggest impact. This is the difference between being busy and being effective.</p>
                </ReadingSection>
              )}
              {activeSection === 2 && (
                <ReadingSection title="The Syllabus Deconstructor." eyebrow="Step 3" icon={Compass}>
                  <p>To find the 20%, you need data. The <Highlight description="A visual tool that breaks down a syllabus into its core topics and uses historical exam data to assign a 'frequency score' to each, revealing the high-yield areas.">Syllabus Deconstructor</Highlight> is an interactive tool that does this for you. By analyzing years of past papers, we can map out the "hot zones" of the curriculum.</p>
                  <p>This tool transforms the syllabus from a long, intimidating list into a strategic map. It shows you where the 'big game' is, allowing you to plan your 'hunt' accordingly. We'll start with Maths, one of the most predictable exams on the schedule.</p>
                  <SyllabusDeconstructor />
                </ReadingSection>
              )}
              {activeSection === 3 && (
                <ReadingSection title="Distillation Techniques" eyebrow="Step 4" icon={Brain}>
                  <p>This section is under construction. Future content will explore techniques like concept mapping, the Feynman technique, and creating one-page summaries to distill complex information into memorable, high-yield assets.</p>
                </ReadingSection>
              )}
              {activeSection === 4 && (
                <ReadingSection title="High-Yield Assets" eyebrow="Step 5" icon={BarChart}>
                    <p>This section is under construction. Future content will guide you on how to turn your distilled knowledge into powerful revision tools like summary sheets, flashcards, and mind maps that are optimized for active recall.</p>
                </ReadingSection>
              )}
              {activeSection === 5 && (
                <ReadingSection title="Your Triage Plan" eyebrow="Step 6" icon={Wrench}>
                    <p>This section is under construction. Future content will provide a framework for creating a personalized study plan based on your own syllabus deconstruction, helping you allocate your time and energy for maximum point-scoring efficiency.</p>
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
