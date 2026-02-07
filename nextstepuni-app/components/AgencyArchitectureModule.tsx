/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
*/

import React, { useState, useEffect } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { 
  ArrowLeft, CheckCircle2, ArrowRight, 
  Lock, Flag, Scale, SlidersHorizontal, UserX, ServerCrash, Recycle, Code, RotateCcw
} from 'lucide-react';

type ModuleProgress = {
  unlockedSection: number;
};

interface AgencyArchitectureModuleProps {
  onBack: () => void;
  progress: ModuleProgress;
  onProgressUpdate: (progress: ModuleProgress) => void;
}

const Highlight = ({ children, description, color = "bg-amber-100/40", textColor = "text-amber-900", decorColor = "decoration-amber-400/40", hoverColor="hover:bg-amber-200/60" }: { children?: React.ReactNode, description: string, color?: string, textColor?: string, decorColor?: string, hoverColor?: string }) => {
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
              <p className="font-sans font-bold text-amber-400 mb-2 uppercase tracking-[0.2em] text-[9px]">The Academic Insight</p>
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
        <div className="w-12 h-12 rounded-2xl bg-stone-900 flex items-center justify-center text-amber-400 shadow-xl border border-white/10">
          <Icon size={24} />
        </div>
      </div>
      <span className="inline-flex items-center gap-2 px-3 py-1 bg-amber-50 text-amber-600 text-[10px] font-black tracking-[0.4em] uppercase rounded-full mb-4">
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
  <div className="my-12 p-8 bg-amber-50/50 border-2 border-dashed border-amber-200 rounded-3xl">
    <div className="flex items-start gap-5">
      <div className="w-11 h-11 rounded-xl bg-amber-500 text-white flex items-center justify-center shrink-0 mt-1 shadow-lg shadow-amber-500/20">
        <Flag size={20} />
      </div>
      <div>
        <h4 className="font-bold text-amber-800 text-sm uppercase tracking-widest">Your Mission (Under 5 Mins)</h4>
        <div className="text-stone-600 mt-2 font-medium leading-relaxed">
          {children}
        </div>
      </div>
    </div>
  </div>
);

const ActivityRing = ({ progress, color = "#f59e0b" }: { progress: number, color?: string }) => {
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

const AttributionSorter = () => {
    const reasons = [
        { text: "I didn't use the right study method.", type: 'internal', control: true },
        { text: "I'm just naturally bad at this subject.", type: 'internal', control: false },
        { text: "The test was unfairly hard.", type: 'external', control: false },
        { text: "I didn't put in enough focused effort.", type: 'internal', control: true },
    ];
    const [choice, setChoice] = useState<{ [key: string]: boolean }>({});

    return(
        <div className="my-10 p-8 md:p-12 bg-white rounded-[3rem] border border-stone-200 shadow-xl">
            <h4 className="font-serif text-2xl font-bold text-stone-800 text-center italic">Control Panel</h4>
            <p className="text-center text-sm text-stone-500 mb-8">Scenario: You fail a test. Which of these reasons are actually within your control?</p>
            <div className="space-y-3">
                {reasons.map(reason => (
                    <button key={reason.text} onClick={() => setChoice({...choice, [reason.text]: !choice[reason.text]})} className={`w-full p-4 rounded-xl border-2 text-left font-bold text-sm transition-all ${choice[reason.text] ? (reason.control ? 'bg-emerald-50 border-emerald-300' : 'bg-rose-50 border-rose-300') : 'bg-stone-50 border-stone-200 hover:bg-stone-100'}`}>
                        {reason.text}
                        {choice[reason.text] && <span className={`ml-2 font-black text-xs ${reason.control ? 'text-emerald-600' : 'text-rose-600'}`}>{reason.control ? '(CONTROLLABLE)' : '(UNCONTROLLABLE)'}</span>}
                    </button>
                ))}
            </div>
        </div>
    );
};

const AttributionReframeDrill = () => {
  const examples = [
    { id: 1, maladaptive: "I failed the test because I am stupid.", adaptive: "I failed the test because my study strategy for this topic was ineffective." },
    { id: 2, maladaptive: "I'm just naturally bad at Maths.", adaptive: "I haven't found an effective way to learn Maths *yet*." },
    { id: 3, maladaptive: "I'll never be good enough to get a H1.", adaptive: "Getting a H1 is a difficult goal, so I will need to break it down into smaller, manageable steps." },
  ];
  
  const [flipped, setFlipped] = useState<number[]>([]);

  const handleFlip = (id: number) => {
    setFlipped(
      flipped.includes(id)
        ? flipped.filter(fId => fId !== id)
        : [...flipped, id]
    );
  };

  return (
    <div className="my-10 p-8 md:p-12 bg-white rounded-[3rem] border border-stone-200 shadow-xl">
      <h4 className="font-serif text-2xl font-bold text-stone-800 text-center italic">Attribution Reframe Drill</h4>
      <p className="text-center text-sm text-stone-500 mb-8">Click on a self-defeating thought to transform it into an empowering one.</p>
      <div className="space-y-4">
        {examples.map((ex) => (
          <motion.div
            key={ex.id}
            onClick={() => handleFlip(ex.id)}
            className="p-6 rounded-2xl cursor-pointer border-2 border-dashed relative min-h-[100px] flex items-center justify-center"
            animate={{
              backgroundColor: flipped.includes(ex.id) ? 'rgba(236, 253, 245, 1)' : 'rgba(254, 242, 242, 1)',
              borderColor: flipped.includes(ex.id) ? 'rgb(110 231 183)' : 'rgb(254 202 202)'
            }}
          >
            <AnimatePresence mode="wait">
              <motion.p
                key={flipped.includes(ex.id) ? ex.adaptive : ex.maladaptive}
                initial={{ opacity: 0, y: 10 }}
                animate={{ opacity: 1, y: 0 }}
                exit={{ opacity: 0, y: -10 }}
                transition={{ duration: 0.3 }}
                className={`font-mono text-sm text-center ${flipped.includes(ex.id) ? 'text-emerald-800' : 'text-rose-800'}`}
              >
                "{flipped.includes(ex.id) ? ex.adaptive : ex.maladaptive}"
              </motion.p>
            </AnimatePresence>
             <div className="absolute bottom-2 right-3 text-stone-300 flex items-center gap-1 text-[9px] font-bold">
              <RotateCcw size={10} />
              REFRAME
            </div>
          </motion.div>
        ))}
      </div>
    </div>
  );
};


// --- MODULE COMPONENT ---
export const AgencyArchitectureModule: React.FC<AgencyArchitectureModuleProps> = ({ onBack, progress, onProgressUpdate }) => {
  const [activeSection, setActiveSection] = useState(progress.unlockedSection);
  const unlockedSection = progress.unlockedSection;
  
  const sections = [
    { id: 'attribution-theory', title: 'The Story of Failure', eyebrow: '01 // The Source Code', icon: Code },
    { id: 'three-dimensions', title: 'The Three Dimensions', eyebrow: '02 // The Control Panel', icon: SlidersHorizontal },
    { id: 'pessimistic-script', title: 'The Pessimist\'s Script', eyebrow: '03 // Learned Helplessness', icon: UserX },
    { id: 'agency-rewrite', title: 'The Agency Re-Write', eyebrow: '04 // Retraining', icon: Recycle },
    { id: 'blueprint', title: 'Your New OS', eyebrow: '05 // The Blueprint', icon: Flag },
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
            <p className="text-[9px] font-black text-amber-500 uppercase tracking-[0.4em] mb-0.5 underline">Module 07</p>
            <h1 className="font-serif font-bold text-lg tracking-tight text-stone-900">Controlling the Controllables</h1>
          </div>
        </div>

        <div className="flex-grow space-y-4 overflow-y-auto no-scrollbar pr-2 relative">
          <div className="absolute left-[21px] top-6 bottom-6 w-0.5 bg-stone-100 -z-0" />
          <div className="absolute left-[21px] top-6 bottom-6 w-0.5">
              <motion.div
                  className="w-full bg-amber-500 shadow-[0_0_10px_rgba(245,158,11,0.5)]"
                  style={{ height: `${progressPercentage}%` }}
              />
          </div>
          {sections.map((section, idx) => {
            const isUnlocked = idx <= unlockedSection;
            const isActive = idx === activeSection;
            const isCompleted = idx < unlockedSection;
            return (
              <button key={section.id} disabled={!isUnlocked} onClick={() => handleJumpToSection(idx)} className={`relative z-10 w-full flex items-center gap-4 p-3 rounded-xl transition-all duration-500 text-left group ${isActive ? 'bg-amber-50 shadow-sm translate-x-2' : ''} ${!isUnlocked ? 'opacity-40 grayscale cursor-not-allowed' : 'hover:bg-stone-50'}`}>
                <div className={`w-11 h-11 rounded-xl flex items-center justify-center shrink-0 border-2 transition-all duration-500 ${isCompleted ? 'bg-amber-600 border-amber-600 text-white shadow-lg' : isActive ? 'bg-white border-amber-500 text-amber-600 shadow-xl rotate-12' : 'bg-white border-stone-200 text-stone-300'}`}>
                   {isCompleted ? <CheckCircle2 size={18} /> : isActive ? <section.icon size={18} /> : <Lock size={16} />}
                </div>
                <div className="flex-grow"><p className={`text-[8px] font-black uppercase tracking-widest ${isActive ? 'text-amber-500' : 'text-stone-400'}`}>{section.eyebrow.split('// ')[1]}</p><h4 className={`text-xs font-bold leading-tight ${isActive ? 'text-stone-900' : 'text-stone-500'}`}>{section.title}</h4></div>
              </button>
            );
          })}
        </div>
        <div className="mt-8 border-t border-stone-100 pt-8 flex flex-col items-center">
           <ActivityRing progress={progressPercentage} color="#f59e0b" /><p className="text-[11px] font-black text-stone-900 uppercase tracking-widest text-center">Progress</p>
        </div>
      </aside>

      <main className="flex-grow flex flex-col items-center py-10 md:py-24 px-6 md:px-16 overflow-y-auto h-screen relative">
        <div className="absolute inset-0 bg-[radial-gradient(#e5e7eb_1px,transparent_1px)] [background-size:32px_32px] opacity-40 pointer-events-none" />
        <div className="w-full max-w-4xl relative z-10">
          <AnimatePresence mode="wait">
            <motion.div key={activeSection} initial={{ opacity: 0, x: 20 }} animate={{ opacity: 1, x: 0 }} exit={{ opacity: 0, x: -20 }} transition={{ duration: 0.6, ease: [0.16, 1, 0.3, 1] }}>
              {activeSection === 0 && (
                <ReadingSection title="The Story of Failure." eyebrow="Step 1" icon={Code}>
                  <p>When something bad happens, your brain instantly writes a story to explain why. This story is called an <Highlight description="A concept from social psychology referring to the causal explanations people generate for events. Your attributional style is a powerful predictor of your resilience and motivation.">attribution</Highlight>. It's the "source code" for your motivation. A resilient mindset isn't about being positive; it's about telling yourself the right kind of story after a failure.</p>
                  <p>The core principle is to focus on what you can control. The Stoic philosophers called this the <Highlight description="The ancient Stoic principle of dividing the world into things you can control (your thoughts, your actions) and things you cannot (external events, other people's opinions).">Dichotomy of Control</Highlight>. The research is clear: students who focus their energy on what they can control, and let go of what they can't, are more resilient and academically successful.</p>
                </ReadingSection>
              )}
              {activeSection === 1 && (
                <ReadingSection title="The Three Dimensions." eyebrow="Step 2" icon={SlidersHorizontal}>
                  <p>Every story you tell yourself about a failure can be broken down along three dimensions. <strong>1. Locus of Control:</strong> Is the cause <Highlight description="Attributing an outcome to something about yourself (e.g., your effort, your ability).">Internal</Highlight> (about you) or <Highlight description="Attributing an outcome to something outside of yourself (e.g., the teacher, the situation).">External</Highlight> (about the world)? <strong>2. Stability:</strong> Is the cause <Highlight description="A cause that is perceived as permanent and unchangeable (e.g., 'I'm just not a maths person').">Stable</Highlight> (permanent) or <Highlight description="A cause that is perceived as temporary and changeable (e.g., 'I didn't study enough for this specific test').">Unstable</Highlight> (temporary)? <strong>3. Controllability:</strong> Is the cause something you can change, or not?</p>
                  <AttributionSorter/>
                </ReadingSection>
              )}
              {activeSection === 2 && (
                <ReadingSection title="The Pessimist's Script." eyebrow="Step 3" icon={UserX}>
                  <p>The most dangerous story your brain can write is the "pessimistic explanatory style." It attributes failure to causes that are **Internal, Stable, and Uncontrollable**. For example: "I failed the test (bad event) because I am stupid (Internal, Stable, Uncontrollable)."</p>
                  <p>This is a psychological poison. It leads directly to a state of <Highlight description="A psychological state where a person feels powerless to change their situation, leading to passivity and giving up. It's the end-point of a pessimistic explanatory style.">Learned Helplessness</Highlight>. If you believe the cause of your failure is a permanent, unchangeable part of who you are, then there's no point in trying again. Your motivation collapses, not because you're lazy, but because your brain has logically concluded that effort is futile.</p>
                </ReadingSection>
              )}
               {activeSection === 3 && (
                <ReadingSection title="The Agency Re-Write." eyebrow="Step 4" icon={Recycle}>
                  <p>The good news is that you can consciously re-write this script. This is called <Highlight description="A cognitive-behavioral technique where individuals are explicitly taught to change their attributions for failure from internal, stable, and uncontrollable causes to external or internal, unstable, and controllable ones.">Attributional Retraining</Highlight>. It's a proven psychological intervention that builds resilience and improves academic performance.</p>
                  <p>The goal is to shift your explanations towards causes that are **Internal, Unstable, and Controllable**. "I failed the test because I am stupid" becomes "I failed the test because my *strategy* was ineffective." The cause is still internal (giving you agency), but it's unstable (you can change your strategy) and controllable. This isn't just wordplay; it's a fundamental shift in your brain's operating system that turns a dead end into a learning opportunity.</p>
                  <AttributionReframeDrill />
                </ReadingSection>
              )}
               {activeSection === 4 && (
                <ReadingSection title="Your New OS." eyebrow="Step 5" icon={Flag}>
                  <p>By practicing this "re-write," you are installing a new default operating system in your brain. You are training yourself to see setbacks not as verdicts, but as data points. This is the foundation of a Growth Mindset and the core of what it means to have agency over your own academic life.</p>
                  <MicroCommitment>
                    <p>The next time you face a small failure—any small failure—consciously run the 3D analysis. Ask yourself: "What story am I telling myself about why this happened?" Is it Internal/External? Stable/Unstable? Controllable/Uncontrollable? This act of noticing is the first step to rewriting the script.</p>
                  </MicroCommitment>
                </ReadingSection>
              )}
              <footer className="mt-24 flex items-center justify-between pt-12 border-t border-stone-200/60 px-4">
                <motion.button whileHover={{ scale: 1.05 }} whileTap={{ scale: 0.95 }} onClick={handlePrev} disabled={activeSection === 0} className={`flex items-center gap-4 bg-stone-100 text-stone-800 px-8 py-4 rounded-xl font-black text-[10px] uppercase tracking-widest transition-all shadow-sm ${activeSection === 0 ? 'opacity-0 pointer-events-none' : ''}`}>
                  <ArrowLeft size={16} /> Prev
                </motion.button>
                <motion.button whileHover={{ scale: 1.05 }} whileTap={{ scale: 0.95 }} onClick={handleCompleteSection} className="group relative flex items-center gap-4 bg-stone-900 text-white px-12 py-6 rounded-2xl font-black text-[12px] uppercase tracking-widest hover:bg-amber-600 transition-all shadow-[0_20px_50px_rgba(0,0,0,0.2)] overflow-hidden">
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
