
/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
*/

import React, { useState, useEffect } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { 
  ArrowLeft, CheckCircle2, ArrowRight, 
  Lock, Flag, HeartPulse, Calculator, Shield, Zap, Wrench, Brain, RotateCcw, HeartHandshake
} from 'lucide-react';

type ModuleProgress = {
  unlockedSection: number;
};

interface ProcrastinationModuleProps {
  onBack: () => void;
  progress: ModuleProgress;
  onProgressUpdate: (progress: ModuleProgress) => void;
}

const Highlight = ({ children, description, color = "bg-orange-100/40", textColor = "text-orange-900", decorColor = "decoration-orange-400/40", hoverColor="hover:bg-orange-200/60" }: { children?: React.ReactNode, description: string, color?: string, textColor?: string, decorColor?: string, hoverColor?: string }) => {
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
              <p className="font-sans font-bold text-orange-400 mb-2 uppercase tracking-[0.2em] text-[9px]">The Academic Insight</p>
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
        <div className="w-12 h-12 rounded-2xl bg-stone-900 flex items-center justify-center text-orange-400 shadow-xl border border-white/10">
          <Icon size={24} />
        </div>
      </div>
      <span className="inline-flex items-center gap-2 px-3 py-1 bg-orange-50 text-orange-600 text-[10px] font-black tracking-[0.4em] uppercase rounded-full mb-4">
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
  <div className="my-12 p-8 bg-orange-50/50 border-2 border-dashed border-orange-200 rounded-3xl">
    <div className="flex items-start gap-5">
      <div className="w-11 h-11 rounded-xl bg-orange-500 text-white flex items-center justify-center shrink-0 mt-1 shadow-lg shadow-orange-500/20">
        <Flag size={20} />
      </div>
      <div>
        <h4 className="font-bold text-orange-800 text-sm uppercase tracking-widest">Your Mission (Under 5 Mins)</h4>
        <div className="text-stone-600 mt-2 font-medium leading-relaxed">
          {children}
        </div>
      </div>
    </div>
  </div>
);

const ActivityRing = ({ progress, color = "#f97316" }: { progress: number, color?: string }) => {
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

const ProcrastinationEquation = () => {
    const [vars, setVars] = useState({ E: 50, V: 50, I: 50, D: 50 });
    const utility = (vars.E * vars.V) / (1 + (vars.I * vars.D / 100)); // Scaled for display

    const Slider = ({ name, value, setter, label }: { name: keyof typeof vars, value: number, setter: (val: number) => void, label: string }) => (
        <div>
            <label className="text-xs font-bold">{label} ({value})</label>
            <input type="range" min="1" max="100" value={value} onChange={e => setter(parseInt(e.target.value))} className="w-full accent-orange-500" />
        </div>
    );
    
    return(
        <div className="my-10 p-8 md:p-12 bg-white rounded-[3rem] border border-stone-200 shadow-xl">
            <h4 className="font-serif text-2xl font-bold text-stone-800 text-center italic">The Procrastination Equation</h4>
            <p className="text-center text-sm text-stone-500 mb-8">Adjust the sliders to see what drives your motivation.</p>
            <div className="p-6 bg-stone-900 rounded-2xl text-center mb-8">
                <p className="text-sm text-stone-400">Your Motivation Score:</p>
                <p className="text-5xl font-black text-white tracking-tighter"><motion.span initial={{}} animate={{}}>{Math.round(utility)}</motion.span></p>
            </div>
            <div className="grid grid-cols-2 gap-6">
                <Slider name="E" value={vars.E} setter={v => setVars({...vars, E:v})} label="Expectancy (Belief)" />
                <Slider name="V" value={vars.V} setter={v => setVars({...vars, V:v})} label="Value (Enjoyment)" />
                <Slider name="I" value={vars.I} setter={v => setVars({...vars, I:v})} label="Impulsiveness" />
                <Slider name="D" value={vars.D} setter={v => setVars({...vars, D:v})} label="Delay (Deadline)" />
            </div>
        </div>
    );
};

const IfThenAutopilot = () => {
    const [plan, setPlan] = useState<{if: string, then: string} | null>(null);

    const createPlan = () => {
      setPlan({if: "I feel the urge to check my phone", then: "I will take three deep breaths and work for 2 more minutes"});
    };

    return(
         <div className="my-10 p-8 md:p-12 bg-white rounded-[3rem] border border-stone-200 shadow-xl">
            <h4 className="font-serif text-2xl font-bold text-stone-800 text-center italic">The "If-Then" Autopilot</h4>
            <p className="text-center text-sm text-stone-500 mb-8">Pre-load a decision to bypass willpower. Click to create a plan.</p>
            <div className="flex justify-center">
                <button onClick={createPlan} className="px-5 py-3 bg-orange-500 text-white font-bold rounded-lg text-sm">Create Plan</button>
            </div>
            {plan && 
            <motion.div initial={{opacity:0}} animate={{opacity:1}} className="mt-6 p-4 bg-stone-900 rounded-xl text-white text-center font-mono text-sm">
                Plan created: IF <span className="text-rose-400">{plan.if}</span>, THEN <span className="text-emerald-400">{plan.then}</span>
            </motion.div>}
        </div>
    );
};

const GuiltSpiral = () => {
    const [guilt, setGuilt] = useState(10);
    const [avoidance, setAvoidance] = useState(10);

    const addCriticism = () => {
        setGuilt(g => Math.min(100, g + 30));
        setAvoidance(a => Math.min(100, a + 25));
    }

    const reset = () => {
        setGuilt(10);
        setAvoidance(10);
    }
    
    return(
        <div className="my-10 p-8 md:p-12 bg-white rounded-[3rem] border border-stone-200 shadow-xl">
             <h4 className="font-serif text-2xl font-bold text-stone-800 text-center italic">The Guilt Spiral</h4>
             <p className="text-center text-sm text-stone-500 mb-8">"Tough love" doesn't work. It just adds more negative emotion to the fire.</p>
             <div className="grid grid-cols-2 gap-6 mb-8">
                <div className="text-center">
                    <p className="font-bold text-sm text-rose-600 mb-2">Guilt Meter</p>
                    <div className="w-full h-6 bg-stone-100 rounded-full"><motion.div className="h-full bg-rose-500 rounded-full" initial={{width: "10%"}} animate={{width: `${guilt}%`}} /></div>
                </div>
                <div className="text-center">
                    <p className="font-bold text-sm text-orange-600 mb-2">Urge to Avoid</p>
                    <div className="w-full h-6 bg-stone-100 rounded-full"><motion.div className="h-full bg-orange-500 rounded-full" initial={{width: "10%"}} animate={{width: `${avoidance}%`}} /></div>
                </div>
            </div>
             <div className="flex justify-center gap-4">
                <button onClick={addCriticism} className="px-4 py-2 bg-rose-100 text-rose-800 text-xs font-bold rounded-lg">Add Self-Criticism</button>
                <button onClick={reset} className="px-4 py-2 bg-stone-100 text-stone-800 text-xs font-bold rounded-lg">Reset</button>
             </div>
        </div>
    );
};

const CircuitBreaker = () => {
    const [reframe, setReframe] = useState('');
    const containsForgive = reframe.toLowerCase().includes('forgive');
    const containsAction = reframe.toLowerCase().includes('i will');
    return(
         <div className="my-10 p-8 md:p-12 bg-white rounded-[3rem] border border-stone-200 shadow-xl">
            <h4 className="font-serif text-2xl font-bold text-stone-800 text-center italic">The Circuit Breaker</h4>
            <p className="text-center text-sm text-stone-500 mb-8">Rewrite this self-critical thought into a self-forgiving, action-oriented statement.</p>
            <p className="p-4 bg-rose-50 border border-rose-200 rounded-xl text-center font-mono text-rose-800 mb-4">"I'm so useless, I wasted the whole day."</p>
            <textarea value={reframe} onChange={e => setReframe(e.target.value)} placeholder="Your new script..." className="w-full h-24 p-4 bg-stone-50 border-2 border-stone-200 rounded-xl focus:outline-none focus:border-orange-400" />
            {(containsForgive || containsAction) &&
                <div className="mt-4 grid grid-cols-2 gap-2 text-xs">
                    <p className={containsForgive ? 'text-emerald-600 font-bold' : 'text-stone-400'}>✓ Contains Self-Forgiveness</p>
                    <p className={containsAction ? 'text-emerald-600 font-bold' : 'text-stone-400'}>✓ Bridges to Action</p>
                </div>
            }
        </div>
    );
}


// --- MODULE COMPONENT ---
export const ProcrastinationModule: React.FC<ProcrastinationModuleProps> = ({ onBack, progress, onProgressUpdate }) => {
  const [activeSection, setActiveSection] = useState(progress.unlockedSection);
  const unlockedSection = progress.unlockedSection;
  
  const sections = [
    { id: 'real-reason', title: 'The Real Reason You Delay', eyebrow: '01 // Not Laziness', icon: HeartPulse },
    { id: 'amygdala-hijack', title: 'The Amygdala Hijack', eyebrow: '02 // Brain Battle', icon: Brain },
    { id: 'procrastination-equation', title: 'The Procrastination Equation', eyebrow: '03 // The Formula', icon: Calculator },
    { id: 'ego-defence', title: 'The Ego\'s Defence System', eyebrow: '04 // The Traps', icon: Shield },
    { id: 'guilt-cycle', title: 'The Guilt Cycle', eyebrow: '05 // The Downward Spiral', icon: RotateCcw },
    { id: 'forgiveness-protocol', title: 'The Forgiveness Protocol', eyebrow: '06 // The Circuit Breaker', icon: HeartHandshake },
    { id: 'if-then-protocol', title: 'The "If-Then" Protocol', eyebrow: '07 // The Antidote', icon: Zap },
    { id: 'scaffolding-focus', title: 'Scaffolding Your Focus', eyebrow: '08 // The Toolkit', icon: Wrench },
  ];

  useEffect(() => {
    setActiveSection(progress.unlockedSection);
  }, [progress.unlockedSection]);

  const handleCompleteSection = () => {
    if (activeSection === unlockedSection && unlockedSection < sections.length) {
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

  const progressPercentage = sections.length > 0 ? (unlockedSection / sections.length) * 100 : 0;

  return (
    <div className="min-h-screen bg-[#FBFBF9] text-stone-900 font-sans flex flex-col md:flex-row overflow-x-hidden">
      <aside className="w-full md:w-80 bg-white border-r border-stone-200 sticky top-0 md:h-screen z-40 p-8 flex flex-col">
