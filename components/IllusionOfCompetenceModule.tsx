
/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
*/

import React, { useState } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { 
  ArrowLeft, CheckCircle2, ArrowRight, 
  Lock, Flag, Eye, AlertTriangle, Lightbulb, SlidersHorizontal, Brain, Wrench
} from 'lucide-react';

interface IllusionOfCompetenceModuleProps {
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

const ForgettingCurveSimulator = () => {
    const retentionData = [100, 40, 25, 15, 10, 5, 3];
    const [reviews, setReviews] = useState(0);
    const retention = reviews === 0 ? 3 : reviews === 1 ? 45 : reviews === 2 ? 75 : 95;

    return (
        <div className="my-10 p-8 md:p-12 bg-white rounded-[3rem] border border-stone-200 shadow-xl">
            <h4 className="font-serif text-2xl font-bold text-stone-800 text-center italic">The Forgetting Curve</h4>
            <p className="text-center text-sm text-stone-500 mb-8">Without review, you forget ~80% of what you learn in 24 hours.</p>
            <div className="w-full h-48 bg-stone-50 rounded-lg p-4">
                 <svg viewBox="0 0 100 100" className="w-full h-full" preserveAspectRatio="none">
                    <motion.path d={`M 0 5 C 20 10, 40 40, 100 ${100-retention}`} fill="none" stroke="#14b8a6" strokeWidth="3" transition={{type: 'spring', damping: 10}}/>
                    <path d={`M 0 5 C 20 10, 40 40, 100 97`} fill="none" stroke="#e5e7eb" strokeWidth="2" strokeDasharray="4"/>
                 </svg>
            </div>
            <p className="text-center font-bold mt-4">Retention after 1 Week: <span className="text-teal-600">{retention}%</span></p>
            <div className="flex justify-center gap-2 mt-4">
                <button onClick={() => setReviews(reviews + 1)} className="px-3 py-1 text-xs bg-stone-200 rounded-md">Add Review</button>
                <button onClick={() => setReviews(0)} className="px-3 py-1 text-xs bg-stone-200 rounded-md">Reset</button>
            </div>
        </div>
    );
};

const FeynmanExplainer = () => {
    const concept = "Osmosis is the net movement of water molecules through a selectively permeable membrane from a region of higher water concentration to a region of lower water concentration.";
    const [explanation, setExplanation] = useState('');
    const jargon = ['molecules', 'selectively', 'permeable', 'concentration'];
    const jargonCount = jargon.filter(word => explanation.toLowerCase().includes(word)).length;
    
    return(
        <div className="my-10 p-8 md:p-12 bg-white rounded-[3rem] border border-stone-200 shadow-xl">
             <h4 className="font-serif text-2xl font-bold text-stone-800 text-center italic">The Feynman Explainer</h4>
             <p className="text-center text-sm text-stone-500 mb-4">Task: Explain this definition of Osmosis in simple terms, as if to a 12-year-old.</p>
             <p className="p-4 bg-stone-100 border border-stone-200 rounded-xl text-xs text-center mb-4">{concept}</p>
             <textarea value={explanation} onChange={e => setExplanation(e.target.value)} className="w-full h-32 p-4 bg-stone-50 border-2 border-stone-200 rounded-xl focus:outline-none focus:border-teal-400" placeholder="Your simple explanation..."></textarea>
             {explanation.length > 0 && 
                <div className={`mt-4 text-center text-xs p-2 rounded-lg ${jargonCount > 0 ? 'bg-rose-100 text-rose-700' : 'bg-emerald-100 text-emerald-700'}`}>
                    {jargonCount > 0 ? `Warning: You're using ${jargonCount} jargon word(s). Simplify further!` : 'Great! This is a simple, clear explanation.'}
                </div>
             }
        </div>
    );
};


// --- MODULE COMPONENT ---
export const IllusionOfCompetenceModule: React.FC<{onBack: () => void}> = ({ onBack }) => {
  const [activeSection, setActiveSection] = useState(0);
  const [unlockedSection, setUnlockedSection] = useState(0);
  
  const sections = [
    { id: 'the-deception', title: 'The Great Deception', eyebrow: '01 // The Illusion', icon: Eye },
    { id: 'passive-traps', title: 'The Passive Traps', eyebrow: '02 // The False Comfort', icon: AlertTriangle },
    { id: 'desirable-difficulties', title: 'The Antidote', eyebrow: '03 // Desirable Difficulties', icon: Lightbulb },
    { id: 'strategic-toolkit', title: 'The Strategic Toolkit', eyebrow: '04 // The System', icon: SlidersHorizontal },
    { id: 'feynman-protocol', title: 'The Feynman Protocol', eyebrow: '05 // The Litmus Test', icon: Brain },
    { id: 'anti-fragile', title: 'Building Anti-Fragile Knowledge', eyebrow: '06 // The Action Plan', icon: Wrench },
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
            <p className="text-[9px] font-black text-teal-500 uppercase tracking-[0.4em] mb-0.5 underline">Module 01</p>
            <h1 className="font-serif font-bold text-lg tracking-tight text-stone-900">Overcoming Illusions of Competence</h1>
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
                <ReadingSection title="The Great Deception." eyebrow="Step 1" icon={Eye}>
                  <p>The most dangerous thing in your academic life isn't the stuff you know you don't know. It's the stuff you *think* you know, but actually don't. This is the <Highlight description="The cognitive bias where your subjective confidence in your mastery of a topic is significantly higher than your objective ability to retrieve and apply that knowledge.">Illusion of Competence</Highlight>. It's the primary driver of 'grade shock' after the Mocks.</p>
                  <p>It's caused by a simple brain shortcut: we mistake the ease of *recognising* information for the ability to *recall* it. Seeing a definition in your notes and thinking "Oh yeah, I know that" feels like learning. But it's a trap. It creates a false sense of security that is brutally exposed under exam conditions when the notes are gone and you have to retrieve the information from a blank page.</p>
                </ReadingSection>
              )}
              {activeSection === 1 && (
                <ReadingSection title="The Passive Traps." eyebrow="Step 2" icon={AlertTriangle}>
                  <p>This illusion is created by the most common study methods because they are low-stress and feel effective. The first is the <Highlight description="When you re-read, your brain recognizes the visual pattern of the highlighted text, not the information itself. The cue is the yellow ink, not your internal memory.">Highlighting Trap</Highlight>. The second is the <Highlight description="Following the logic of a solved problem feels like you could have solved it yourself. This is the 'passenger effect' - you practiced verification, not derivation.">'Solved Example' Fallacy</Highlight>. The third is the <Highlight description="When a teacher explains something clearly, you confuse their fluency with your own. You've toured their understanding, not built your own.">Lecture Delusion</Highlight>.</p>
                  <p>All these passive methods fail to account for the biological reality of your memory: the <Highlight description="The natural, exponential decay of memory. Without active reinforcement, you lose the majority of new information within 24 hours.">Forgetting Curve</Highlight>. Passive learning feels good, but the knowledge simply evaporates.</p>
                  <ForgettingCurveSimulator />
                </ReadingSection>
              )}
              {activeSection === 2 && (
                <ReadingSection title="The Antidote." eyebrow="Step 3" icon={Lightbulb}>
                  <p>To dismantle this illusion, we must shift from study methods that feel easy (passive) to ones that feel hard (active). The science of learning is built on the counter-intuitive concept of <Highlight description="Introduced by Robert & Elizabeth Bjork, this is the idea that learning conditions that feel harder and slow down initial performance often lead to far superior long-term retention.">Desirable Difficulties</Highlight>.</p>
                  <p>The single most powerful "desirable difficulty" is <Highlight description="The act of retrieving information from memory without cues. This 'testing effect' is a memory modifier; the struggle to recall is the learning process itself.">Active Recall</Highlight>. When you force your brain to retrieve information, you send a powerful signal to strengthen that neural pathway for future use. The struggle is not a sign you are failing; it is the physical sensation of your brain getting stronger.</p>
                </ReadingSection>
              )}
              {activeSection === 3 && (
                <ReadingSection title="The Strategic Toolkit." eyebrow="Step 4" icon={SlidersHorizontal}>
                  <p>Active Recall is the engine, but it needs a system to work effectively. The two key partners are <Highlight description="The strategy of spreading out your study sessions over time to interrupt the forgetting curve.">Spaced Repetition</Highlight> and <Highlight description="The strategy of mixing different topics within a study session to train the crucial 'problem spotting' skill.">Interleaving</Highlight>.</p>
                  <p>These strategies can be managed with a simple but powerful system: the <Highlight description="A way to plan study by logging what you've done and using a Red/Amber/Green system to rate your confidence, forcing you to always work on your weakest topics first.">Retrospective Revision Timetable</Highlight>. This system forces you to confront your incompetence daily and prioritizes output (mastery) over input (time spent studying).</p>
                </ReadingSection>
              )}
              {activeSection === 4 && (
                <ReadingSection title="The Feynman Protocol." eyebrow="Step 5" icon={Brain}>
                  <p>The ultimate litmus test for genuine understanding is the <Highlight description="Named after the Nobel prize-winning physicist Richard Feynman, this technique involves explaining a concept in simple terms, as if to a child, to identify the gaps in your own knowledge.">Feynman Technique</Highlight>. If you can't explain it simply, you don't really know it. The moment you stumble or have to use jargon is the "Illusion Gap"—the precise point where your knowledge is fragile.</p>
                  <p>For STEM subjects, a practical application of this is <Highlight description="Practicing exam questions under exam conditions—no notes, no textbook, no marking scheme. This forces you to confront what you can actually retrieve.">'Blind Practice'</Highlight> combined with a <Highlight description="A dedicated notebook where you log every mistake, diagnose why it happened (Slip, Gap, or Misconception), and prescribe a fix.">Mistake Log</Highlight>. This turns vague failure ("I'm bad at Maths") into specific, actionable data ("I keep forgetting the chain rule").</p>
                  <FeynmanExplainer />
                </ReadingSection>
              )}
               {activeSection === 5 && (
                <ReadingSection title="Anti-Fragile Knowledge." eyebrow="Step 6" icon={Wrench}>
                  <p>The goal is to move from <Highlight description="Knowledge that is context-dependent and breaks under pressure or when a question is phrased differently. It's a product of passive learning.">Fragile Knowledge</Highlight> to <Highlight description="Knowledge that actually gets stronger when challenged with new contexts and problems. It is the product of desirable difficulties.">Anti-Fragile Knowledge</Highlight>. This is the only path to genuine confidence.</p>
                  <p>By embracing these effortful strategies, you are not just learning more effectively; you are also managing your wellbeing. The anxiety of the Leaving Cert often stems from the subconscious knowledge that your understanding is fragile. Genuine competence, built through desirable difficulties, is the ultimate antidote to exam stress.</p>
                   <MicroCommitment>
                    <p>For your very next study session, commit to the "Book Closed" rule. Spend 20 minutes reading, then close the book and spend 10 minutes writing down everything you can remember. This one change will transform your learning.</p>
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
