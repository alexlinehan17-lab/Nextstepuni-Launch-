/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
*/

import React, { useState, useEffect } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { 
  ArrowLeft, CheckCircle2, ArrowRight, 
  Lock, Flag, Key, FlaskConical, BookOpen, Languages, Feather, Award
} from 'lucide-react';

type ModuleProgress = {
  unlockedSection: number;
};

interface SubjectSpecificAdviceModuleProps {
  onBack: () => void;
  progress: ModuleProgress;
  onProgressUpdate: (progress: ModuleProgress) => void;
}

const Highlight = ({ children, description, color = "bg-red-100/40", textColor = "text-red-900", decorColor = "decoration-red-400/40", hoverColor="hover:bg-red-200/60" }: { children?: React.ReactNode, description: string, color?: string, textColor?: string, decorColor?: string, hoverColor?: string }) => {
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
              <p className="font-sans font-bold text-red-400 mb-2 uppercase tracking-[0.2em] text-[9px]">The Academic Insight</p>
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
        <div className="w-12 h-12 rounded-2xl bg-stone-900 flex items-center justify-center text-red-400 shadow-xl border border-white/10">
          <Icon size={24} />
        </div>
      </div>
      <span className="inline-flex items-center gap-2 px-3 py-1 bg-red-50 text-red-600 text-[10px] font-black tracking-[0.4em] uppercase rounded-full mb-4">
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
  <div className="my-12 p-8 bg-red-50/50 border-2 border-dashed border-red-200 rounded-3xl">
    <div className="flex items-start gap-5">
      <div className="w-11 h-11 rounded-xl bg-red-500 text-white flex items-center justify-center shrink-0 mt-1 shadow-lg shadow-red-500/20">
        <Flag size={20} />
      </div>
      <div>
        <h4 className="font-bold text-red-800 text-sm uppercase tracking-widest">Your Mission (Under 5 Mins)</h4>
        <div className="text-stone-600 mt-2 font-medium leading-relaxed">
          {children}
        </div>
      </div>
    </div>
  </div>
);

const ActivityRing = ({ progress, color = "#ef4444" }: { progress: number, color?: string }) => {
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
const PartialCreditCalculator = () => {
    const [steps, setSteps] = useState({ formula: false, substitution: false, slip: false, blunder: false });

    let marks = 0;
    let grade = "Zero Credit";
    if (steps.formula && !steps.blunder) { marks = 3; grade = "Low Partial"; }
    if (steps.formula && steps.substitution && !steps.blunder) { marks = 5; grade = "Mid Partial"; }
    if (steps.formula && steps.substitution && !steps.blunder && !steps.slip) { marks = 10; grade = "Full Credit"; }
    if (steps.formula && steps.substitution && !steps.blunder && steps.slip) { marks = 8; grade = "High Partial"; }
    if(steps.blunder) {marks = 3; grade="Low Partial (Blunder)"}

    return(
        <div className="my-10 p-8 md:p-12 bg-white rounded-[3rem] border border-stone-200 shadow-xl">
            <h4 className="font-serif text-2xl font-bold text-stone-800 text-center italic">Partial Credit Calculator</h4>
            <p className="text-center text-sm text-stone-500 mb-8">Scenario: A 10-mark D-Scale question. Check the steps you complete.</p>
            <div className="grid grid-cols-2 gap-4">
                <button onClick={() => setSteps({...steps, formula: !steps.formula})} className={`p-4 rounded-xl border-2 ${steps.formula ? 'bg-emerald-100' : ''}`}>Wrote correct formula</button>
                <button onClick={() => setSteps({...steps, substitution: !steps.substitution})} className={`p-4 rounded-xl border-2 ${steps.substitution ? 'bg-emerald-100' : ''}`}>Attempted substitution</button>
                <button onClick={() => setSteps({...steps, slip: !steps.slip, blunder: false})} className={`p-4 rounded-xl border-2 ${steps.slip ? 'bg-amber-100' : ''}`}>Made a minor 'Slip'</button>
                <button onClick={() => setSteps({...steps, blunder: !steps.blunder, slip: false})} className={`p-4 rounded-xl border-2 ${steps.blunder ? 'bg-rose-100' : ''}`}>Made a major 'Blunder'</button>
            </div>
            <div className="mt-8 p-4 bg-stone-900 rounded-xl text-center text-white">
                You get <span className="font-bold text-2xl text-red-400">{marks}/10</span> ({grade})
            </div>
        </div>
    );
}

const OralPivotSimulator = () => {
    const [response, setResponse] = useState<null|'short'|'pivot'>(null);
    return(
         <div className="my-10 p-8 md:p-12 bg-white rounded-[3rem] border border-stone-200 shadow-xl">
            <h4 className="font-serif text-2xl font-bold text-stone-800 text-center italic">Oral Exam Pivot Simulator</h4>
            <p className="text-center font-bold text-stone-700 mb-2">Examiner: "How was your weekend?"</p>
            <div className="grid grid-cols-2 gap-4">
                <button onClick={() => setResponse('short')} className="p-4 bg-stone-100 rounded-xl"><strong>A:</strong> "It was grand, I went to the cinema."</button>
                <button onClick={() => setResponse('pivot')} className="p-4 bg-stone-100 rounded-xl"><strong>B:</strong> "It was stressful, I was studying. To relax, I play Gaelic Football."</button>
            </div>
            {response && <motion.p initial={{opacity:0}} animate={{opacity:1}} className={`mt-4 p-4 rounded-xl text-sm font-bold text-center ${response==='pivot' ? 'bg-emerald-100 text-emerald-800' : 'bg-rose-100 text-rose-800'}`}>
                {response === 'short' ? "FAIL: You've given control back to the examiner. Next question is random." : "SUCCESS! You've pivoted to a prepared topic. The examiner will now ask about sport."}
            </motion.p>}
        </div>
    );
}

// --- MODULE COMPONENT ---
export const SubjectSpecificAdviceModule: React.FC<SubjectSpecificAdviceModuleProps> = ({ onBack, progress, onProgressUpdate }) => {
  const [activeSection, setActiveSection] = useState(progress.unlockedSection);
  const unlockedSection = progress.unlockedSection;
  
  const sections = [
    { id: 'strategic-compliance', title: 'Strategic Compliance', eyebrow: '01 // The Master Key', icon: Key },
    { id: 'stem-protocols', title: 'The STEM Protocols', eyebrow: '02 // Maths & Science', icon: FlaskConical },
    { id: 'humanities-protocols', title: 'The Humanities Engine', eyebrow: '03 // History & Geography', icon: BookOpen },
    { id: 'languages-protocols', title: 'Linguistic Engineering', eyebrow: '04 // Irish & Languages', icon: Languages },
    { id: 'english-protocol', title: 'The PCLM Protocol', eyebrow: '05 // English P1 & P2', icon: Feather },
    { id: 'grade-engineering', title: 'The Grade Engineering Mindset', eyebrow: '06 // The Final Mindset', icon: Award },
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
            <p className="text-[9px] font-black text-red-500 uppercase tracking-[0.4em] mb-0.5 underline">Module 05</p>
            <h1 className="font-serif font-bold text-lg tracking-tight text-stone-900">Subject Specific Advice</h1>
          </div>
        </div>

        <div className="flex-grow space-y-4 overflow-y-auto no-scrollbar pr-2 relative">
          <div className="absolute left-[21px] top-6 bottom-6 w-0.5 bg-stone-100 -z-0" />
          <div className="absolute left-[21px] top-6 bottom-6 w-0.5">
              <motion.div
                  className="w-full bg-red-500 shadow-[0_0_10px_rgba(239,68,68,0.5)]"
                  style={{ height: `${progressPercentage}%` }}
              />
          </div>
          {sections.map((section, idx) => {
            const isUnlocked = idx <= unlockedSection;
            const isActive = idx === activeSection;
            const isCompleted = idx < unlockedSection;
            return (
              <button key={section.id} disabled={!isUnlocked} onClick={() => handleJumpToSection(idx)} className={`relative z-10 w-full flex items-center gap-4 p-3 rounded-xl transition-all duration-500 text-left group ${isActive ? 'bg-red-50 shadow-sm translate-x-2' : ''} ${!isUnlocked ? 'opacity-40 grayscale cursor-not-allowed' : 'hover:bg-stone-50'}`}>
                <div className={`w-11 h-11 rounded-xl flex items-center justify-center shrink-0 border-2 transition-all duration-500 ${isCompleted ? 'bg-red-600 border-red-600 text-white shadow-lg' : isActive ? 'bg-white border-red-500 text-red-600 shadow-xl rotate-12' : 'bg-white border-stone-200 text-stone-300'}`}>
                   {isCompleted ? <CheckCircle2 size={18} /> : isActive ? <section.icon size={18} /> : <Lock size={16} />}
                </div>
                <div className="flex-grow"><p className={`text-[8px] font-black uppercase tracking-widest ${isActive ? 'text-red-500' : 'text-stone-400'}`}>{section.eyebrow.split('// ')[1]}</p><h4 className={`text-xs font-bold leading-tight ${isActive ? 'text-stone-900' : 'text-stone-500'}`}>{section.title}</h4></div>
              </button>
            );
          })}
        </div>
        <div className="mt-8 border-t border-stone-100 pt-8 flex flex-col items-center">
           <ActivityRing progress={progressPercentage} color="#ef4444" /><p className="text-[11px] font-black text-stone-900 uppercase tracking-widest text-center">Progress</p>
        </div>
      </aside>

      <main className="flex-grow flex flex-col items-center py-10 md:py-24 px-6 md:px-16 overflow-y-auto h-screen relative">
        <div className="absolute inset-0 bg-[radial-gradient(#e5e7eb_1px,transparent_1px)] [background-size:32px_32px] opacity-40 pointer-events-none" />
        <div className="w-full max-w-4xl relative z-10">
          <AnimatePresence mode="wait">
            <motion.div key={activeSection} initial={{ opacity: 0, x: 20 }} animate={{ opacity: 1, x: 0 }} exit={{ opacity: 0, x: -20 }} transition={{ duration: 0.6, ease: [0.16, 1, 0.3, 1] }}>
              {activeSection === 0 && (
                <ReadingSection title="Strategic Compliance." eyebrow="Step 1" icon={Key}>
                  <p>The Leaving Cert is not a test of intelligence. It is a standardized, bureaucratic process governed by rigid algorithms. High performance isn't just about knowing your subject; it's about <Highlight description="The ability to align your answer with the specific, often non-intuitive, criteria of the marking scheme.">Strategic Compliance</Highlight>. The gap between a H3 and a H1 is often not a gap in understanding, but in formatting.</p>
                  <p>This module is the decryption key. By deconstructing the assessment architecture of each subject, we can identify the specific "method marks" and structural requirements that allow you to engineer your grades. The Leaving Cert is a coded system; the marking schemes are the key.</p>
                </ReadingSection>
              )}
               {activeSection === 1 && (
                <ReadingSection title="The STEM Protocols." eyebrow="Step 2" icon={FlaskConical}>
                  <p>In STEM subjects, the final answer is only a small part of the story. The vast majority of marks are for the process. For Maths, this means exploiting the <Highlight description="A system that rewards any valid attempt or correct step, even if the final answer is wrong.">"attempt mark" philosophy</Highlight>. You can get 70-90% of the marks for a question with a completely incorrect final answer. Never leave a blank space.</p>
                  <p>For Biology, it's about <Highlight description="The use of precise, non-negotiable keywords that trigger marks. Synonyms are often rejected.">Terminological Exactitude</Highlight>. 'Osmosis' gets marks; 'water moving' does not. Also, beware the <Highlight description="The policy in Biology where an incorrect item in a list can cancel out a correct one. Provide only the number of points requested.">'Surplus' Danger</Highlight>. In Physics and Chemistry, the <Highlight description="The predictable 3-3-3-3 structure for calculation questions: Formula, Substitution, Manipulation, Calculation.">'3-3-3-3 System'</Highlight> means you bank marks for setup before you ever touch your calculator.</p>
                  <PartialCreditCalculator />
                </ReadingSection>
              )}
               {activeSection === 2 && (
                <ReadingSection title="The Humanities Engine." eyebrow="Step 3" icon={BookOpen}>
                  <p>In Humanities, the game shifts from "right answer" to "coherent argument." For Geography, this is a mechanical process of accumulating <Highlight description="A Significant Relevant Point is a single piece of factual information, worth 2 marks. A 30-mark essay requires 15 SRPs.">SRPs</Highlight>. An essay is just a container for these points.</p>
                  <p>History uses a dual-layered matrix: the <Highlight description="Cumulative Mark (max 60): Measures the density of historical facts (dates, names, stats).">CM</Highlight> for facts and the <Highlight description="Overall Evaluation (max 40): Measures the quality of your argument, historical language, and coherence.">OE</Highlight> for argument. A common trap is to get high CM but low OE by telling a story instead of making an argument. Use the <Highlight description="A sentence at the end of each paragraph that explicitly links the facts back to the question, signaling 'Argumentation' to the examiner.">'Link-Back' Tactic</Highlight> to boost your OE.</p>
                </ReadingSection>
              )}
              {activeSection === 3 && (
                <ReadingSection title="Linguistic Engineering." eyebrow="Step 4" icon={Languages}>
                  <p>In languages, the goal is "Communicative Competence," not poetic genius. It's about manipulating the language you know to fit the question. The Oral exam is your chance to take control. Examiners are trained to follow your lead. Use the <Highlight description="Answering a question and adding a 'hook' to steer the conversation towards a topic you have prepared (e.g., 'To relax, I play Gaelic Football...').">'Pivot' Technique</Highlight> to move from a random question to a prepared script.</p>
                  <p>For written exams, use <Highlight description="Grammatically complex, thematically neutral sentences that can be inserted into any essay to demonstrate linguistic flair and boost the 'Language' mark.">'Skeleton Key' Phrases</Highlight>. For French, this means using the Subjunctive. For Spanish, it's idiomatic expressions. For German, it's mastering word order like inversion. These are high-yield investments for your language grade.</p>
                  <OralPivotSimulator/>
                </ReadingSection>
              )}
              {activeSection === 4 && (
                <ReadingSection title="The PCLM Protocol." eyebrow="Step 5" icon={Feather}>
                  <p>English is not subjective. It is marked using a rigid, standardized rubric: the <Highlight description="The four criteria for marking English: Purpose (30%), Coherence (30%), Language (30%), and Mechanics (10%).">PCLM</Highlight> criteria. Your grade is a direct result of how you score on these four metrics.</p>
                  <p><Highlight description="Did you answer the specific question asked? This is the most important criterion." color="bg-blue-100/40" textColor="text-blue-900" decorColor="decoration-blue-400/40" hoverColor="hover:bg-blue-200/60">Purpose</Highlight> and <Highlight description="Is your argument logical and well-structured?" color="bg-green-100/40" textColor="text-green-900" decorColor="decoration-green-400/40" hoverColor="hover:bg-green-200/60">Coherence</Highlight> are worth 60% of the marks. For the Comparative, avoid the "linear" trap (Text A, then B, then C) and use the <Highlight description="The technique of structuring comparative paragraphs by theme, weaving links and contrasts between all three texts throughout.">'Weave' Method</Highlight> to maximize your Coherence score. For