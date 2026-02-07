
/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
*/

import React, { useState, useEffect } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { 
  ArrowLeft, CheckCircle2, Zap, ArrowRight, BookOpen, 
  Shield, Cpu, Waypoints,
  Activity, Lock, Flag
} from 'lucide-react';

type ModuleProgress = {
  unlockedSection: number;
};

interface HopeProtocolModuleProps {
  onBack: () => void;
  progress: ModuleProgress;
  onProgressUpdate: (progress: ModuleProgress) => void;
}

const Highlight = ({ children, description, color = "bg-emerald-100/40" }: { children?: React.ReactNode, description: string, color?: string }) => {
  const [isOpen, setIsOpen] = useState(false);

  return (
    <span className="relative inline-block mx-0.5">
      <button 
        onClick={(e) => {
          e.stopPropagation();
          setIsOpen(!isOpen);
        }}
        className={`relative inline-flex items-center px-2 py-0.5 font-bold ${color} rounded-md cursor-help hover:bg-emerald-200/60 transition-all duration-300 decoration-emerald-400/40 underline decoration-2 underline-offset-4 text-emerald-900`}
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

const ReadingSection = ({ title, eyebrow, icon: Icon, children }: { title: string, eyebrow: string, icon: any, children?: React.ReactNode }) => (
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

const MicroCommitment = ({ children }: { children?: React.ReactNode }) => (
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

const HopeDiagnostic = () => {
  const myths = [
    { myth: "Hope is just wishful thinking.", fact: "FALSE. Hope is an active cognitive skill combining motivation (willpower) and strategic planning (waypower)." },
    { myth: "You're either born hopeful or you're not.", fact: "FALSE. Hope is a teachable skill. The brain circuits for hope can be physically strengthened through practice (neuroplasticity)." },
    { myth: "Hope is the same as optimism.", fact: "FALSE. Optimism is a general belief that things will be okay. Hope is the specific belief that YOU can MAKE things okay through planning and effort." },
  ];
  return (
    <div className="my-10 p-8 md:p-12 bg-white rounded-[3rem] border border-stone-200 shadow-xl space-y-8">
      <h4 className="font-serif text-2xl font-bold text-stone-800 text-center italic">Hope Circuit Diagnostic</h4>
      <p className="text-center text-sm text-stone-500 -mt-4">Let's bust some common myths about where hope comes from.</p>
      <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
        {myths.map((item, i) => <MythBusterCard key={i} front={item.myth} back={item.fact} />)}
      </div>
    </div>
  );
}

interface MythBusterCardProps {
  front: string;
  back: string;
}

const MythBusterCard: React.FC<MythBusterCardProps> = ({ front, back }) => {
  const [isFlipped, setIsFlipped] = useState(false);
  return (
    <div className="w-full h-40 [perspective:1000px]" onClick={() => setIsFlipped(!isFlipped)}>
      <motion.div className="relative w-full h-full transition-transform duration-700" style={{ transformStyle: 'preserve-3d' }} animate={{ rotateX: isFlipped ? 180 : 0 }}>
        <div className="absolute w-full h-full [backface-visibility:hidden] rounded-3xl p-6 flex flex-col items-center justify-center text-center border-2 border-dashed border-stone-300 bg-stone-50 cursor-pointer group">
          <p className="text-sm font-bold leading-snug text-stone-700">{front}</p>
        </div>
        <div className="absolute w-full h-full [backface-visibility:hidden] rounded-3xl p-4 flex flex-col items-center justify-center text-center border-2 border-emerald-700 bg-emerald-600 text-white shadow-lg" style={{ transform: 'rotateX(180deg)' }}>
          <p className="text-xs font-bold leading-snug">{back}</p>
        </div>
      </motion.div>
    </div>
  );
};

const BrainMismatchDiagram = () => (
  <div className="my-10 p-8 md:p-12 bg-white rounded-[3rem] border border-stone-200 shadow-xl flex flex-col items-center">
    <h4 className="font-serif text-2xl font-bold text-stone-800 text-center italic mb-2">Adolescent Brain: System Mismatch</h4>
    <p className="text-center text-sm text-stone-500 mb-12 max-w-md">Your emotional 'accelerator' is at full volume, while your rational 'brakes' are still being fine-tuned.</p>
    
    <div className="w-full max-w-sm h-56 flex justify-around items-end gap-8 px-4">
      {/* Limbic System Bar */}
      <div className="w-full flex flex-col items-center h-full">
        <div className="flex-grow w-16 bg-stone-100 rounded-t-lg overflow-hidden relative">
          <motion.div 
            className="absolute bottom-0 w-full bg-rose-500"
            initial={{ height: "90%" }}
            animate={{ height: ["90%", "95%", "90%"] }}
            transition={{ duration: 1.5, repeat: Infinity, ease: "easeInOut" }}
            style={{ boxShadow: '0 0 20px rgba(239, 68, 68, 0.5)' }}
          />
        </div>
        <div className="text-center mt-4">
          <p className="font-bold text-rose-600">Limbic System</p>
          <p className="text-xs text-stone-500">The Accelerator (Max Volume)</p>
        </div>
      </div>

      {/* Prefrontal Cortex Bar */}
      <div className="w-full flex flex-col items-center h-full">
        <div className="flex-grow w-16 bg-stone-100 rounded-t-lg overflow-hidden relative">
          <motion.div 
            className="absolute bottom-0 w-full bg-emerald-500"
            initial={{ height: "0%" }}
            animate={{ height: "30%" }}
            transition={{ duration: 2, delay: 0.5, ease: "easeOut" }}
          />
           <motion.div 
            className="absolute bottom-0 w-full h-[30%] bg-white"
            initial={{ opacity: 0 }}
            animate={{ opacity: [0, 0.5, 0] }}
            transition={{ duration: 1, repeat: Infinity, ease: "easeInOut", delay: 1 }}
          />
        </div>
        <div className="text-center mt-4">
          <p className="font-bold text-emerald-600">Prefrontal Cortex</p>
          <p className="text-xs text-stone-500">The Brakes (Fine-Tuning)</p>
        </div>
      </div>
    </div>
  </div>
);

const DopamineDial = () => {
  const [motivation, setMotivation] = useState(10);
  const [choice, setChoice] = useState<'none' | 'cold' | 'hot'>('none');

  const handleChoice = (type: 'cold' | 'hot') => {
    setChoice(type);
    setMotivation(type === 'cold' ? 30 : 90);
  };
  
  const radius = 60;
  const circumference = Math.PI * radius; // Semicircle
  const offset = circumference - (motivation / 100) * circumference;

  return (
    <div className="my-10 p-8 md:p-12 bg-white rounded-[3rem] border border-stone-200 shadow-xl">
      <h4 className="font-serif text-2xl font-bold text-stone-800 text-center italic">Interactive: The Dopamine Dial</h4>
      <p className="text-center text-sm text-stone-500 mb-8">Scenario: You need to study for a history exam. Choose your thought process.</p>
      
      <div className="w-full flex justify-center items-end h-24">
        <svg width="160" height="80" viewBox="0 0 160 80" className="overflow-visible">
          <path d="M 20 80 A 60 60 0 0 1 140 80" fill="none" stroke="#e5e7eb" strokeWidth="15" strokeLinecap="round" />
          <motion.path 
            d="M 20 80 A 60 60 0 0 1 140 80" 
            fill="none" 
            stroke="url(#grad)" 
            strokeWidth="15" 
            strokeLinecap="round" 
            strokeDasharray={circumference}
            initial={{ strokeDashoffset: circumference }}
            animate={{ strokeDashoffset: offset }}
            transition={{ type: "spring", damping: 15, stiffness: 100 }}
          />
          <defs>
            <linearGradient id="grad" x1="0%" y1="0%" x2="100%" y2="0%">
              <stop offset="0%" style={{stopColor: "#34d399", stopOpacity:1}} />
              <stop offset="100%" style={{stopColor: "#10b981", stopOpacity:1}} />
            </linearGradient>
          </defs>
        </svg>
      </div>
      
      <div className="grid grid-cols-1 md:grid-cols-2 gap-4 mt-8">
        <button onClick={() => handleChoice('cold')} className="p-4 bg-blue-50 border-2 border-blue-200 rounded-xl text-left text-sm hover:bg-blue-100 transition-colors"><strong>"Cold" Cognition:</strong> "I need to study history."</button>
        <button onClick={() => handleChoice('hot')} className="p-4 bg-rose-50 border-2 border-rose-200 rounded-xl text-left text-sm hover:bg-rose-100 transition-colors"><strong>"Hot" Cognition (EFT):</strong> "Imagine acing that exam..."</button>
      </div>

      <AnimatePresence>
        {choice !== 'none' && (
          <motion.div initial={{opacity:0, y:10}} animate={{opacity:1, y:0}} className="mt-8 p-6 rounded-2xl bg-stone-900 text-white">
            {choice === 'cold' && <p><strong className="text-blue-400">Result:</strong> A small motivational increase. The task is abstract and lacks an immediate reward signal for your brain.</p>}
            {choice === 'hot' && <p><strong className="text-rose-400">Result:</strong> Major dopamine boost! Vividly simulating future success makes the reward feel real *now*, flooding your brain with the motivation to start.</p>}
          </motion.div>
        )}
      </AnimatePresence>
    </div>
  );
};

const HopeMap = () => {
  const [goal, setGoal] = useState('');
  const [pathways, setPathways] = useState(['']);
  const [obstacles, setObstacles] = useState(['']);

  const addPathway = () => setPathways([...pathways, '']);
  const addObstacle = () => setObstacles([...obstacles, '']);

  const updatePathway = (index: number, value: string) => {
    const newPathways = [...pathways];
    newPathways[index] = value;
    setPathways(newPathways);
  };
  const updateObstacle = (index: number, value: string) => {
    const newObstacles = [...obstacles];
    newObstacles[index] = value;
    setObstacles(newObstacles);
  };

  return (
    <div className="my-10 p-8 md:p-12 bg-white rounded-[3rem] border border-stone-200 shadow-xl space-y-8">
      <h4 className="font-serif text-2xl font-bold text-stone-800 text-center italic">My Hope Circuit Blueprint</h4>
      <div>
        <label className="block text-xs font-black text-stone-600 uppercase ml-4 mb-2">The Power Source (Your Goal)</label>
        <input value={goal} onChange={(e) => setGoal(e.target.value)} placeholder="e.g., Get a H2 in Leaving Cert Maths" className="w-full bg-stone-50 border-2 border-stone-100 rounded-xl p-4 focus:border-emerald-500 outline-none transition-colors" />
      </div>
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        <div>
          <label className="block text-xs font-black text-stone-600 uppercase ml-4 mb-2">The Wiring (Pathways)</label>
          <div className="space-y-2">
            {pathways.map((p, i) => (
              <input key={i} value={p} onChange={(e) => updatePathway(i, e.target.value)} placeholder={`Route ${i + 1}`} className="w-full bg-stone-50 border-2 border-stone-100 rounded-xl p-3 focus:border-emerald-500 outline-none transition-colors" />
            ))}
          </div>
          <button onClick={addPathway} className="mt-2 text-xs font-bold text-emerald-600 hover:text-emerald-800">+ Add another route</button>
        </div>
        <div>
          <label className="block text-xs font-black text-stone-600 uppercase ml-4 mb-2">Short Circuits (Obstacles)</label>
          <div className="space-y-2">
            {obstacles.map((o, i) => (
              <input key={i} value={o} onChange={(e) => updateObstacle(i, e.target.value)} placeholder={`Potential problem ${i + 1}`} className="w-full bg-stone-50 border-2 border-stone-100 rounded-xl p-3 focus:border-emerald-500 outline-none transition-colors" />
            ))}
          </div>
          <button onClick={addObstacle} className="mt-2 text-xs font-bold text-emerald-600 hover:text-emerald-800">+ Add another problem</button>
        </div>
      </div>
    </div>
  );
};

const CortisolSimulator = () => {
  const [responseType, setResponseType] = useState<'neutral' | 'low-hope' | 'high-hope'>('neutral');
  const pathData = {
    neutral: "M0,50 C40,50 60,10 100,10 L250,10 C300,10 320,80 400,90",
    'low-hope': "M0,50 C40,50 60,10 100,10 L250,10 C300,10 320,20 400,20",
    'high-hope': "M0,50 C40,50 60,10 100,10 L250,10 C300,10 320,70 400,80",
  }
  return (
     <div className="my-10 p-8 md:p-12 bg-white rounded-[3rem] border border-stone-200 shadow-xl">
        <h4 className="font-serif text-2xl font-bold text-stone-800 text-center italic">Cortisol Curve Simulator</h4>
        <p className="text-center text-sm text-stone-500 mb-2">Stressor Detected: Bad Mock Exam Result.</p>
        <p className="text-center text-sm text-stone-500 mb-8">How does your system respond?</p>
        <div className="bg-stone-50/50 p-6 rounded-2xl">
          <svg viewBox="0 0 400 100" className="w-full h-auto">
            <AnimatePresence>
            <motion.path
              key={responseType}
              d={pathData[responseType]}
              fill="none"
              stroke={responseType === 'low-hope' ? '#ef4444' : '#10b981'}
              strokeWidth="3"
              initial={{ pathLength: 0 }}
              animate={{ pathLength: 1 }}
              transition={{ duration: 1.5, ease: 'easeInOut' }}
              strokeLinecap="round"
            />
            </AnimatePresence>
             <text x="5" y="15" fontSize="8" fill="#9ca3af">High Cortisol</text>
             <text x="5" y="95" fontSize="8" fill="#9ca3af">Low Cortisol</text>
          </svg>
        </div>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4 mt-6">
          <button onClick={() => setResponseType('low-hope')} className="p-4 bg-rose-50 border-2 border-rose-200 rounded-xl text-left text-sm"><strong>Low-Hope Response:</strong> "This is pointless, I'm just bad at this subject." <span className="block text-xs text-rose-500 mt-1">Result: Flattened cortisol curve, prolonged stress.</span></button>
          <button onClick={() => setResponseType('high-hope')} className="p-4 bg-emerald-50 border-2 border-emerald-200 rounded-xl text-left text-sm"><strong>High-Hope Response:</strong> "Okay, that didn't work. What's a new plan I can try?" <span className="block text-xs text-emerald-500 mt-1">Result: Healthy cortisol recovery, stress buffered.</span></button>
        </div>
     </div>
  );
}

// --- MODULE COMPONENT ---
export const HopeProtocolModule: React.FC<HopeProtocolModuleProps> = ({ onBack, progress, onProgressUpdate }) => {
  const [activeSection, setActiveSection] = useState(progress.unlockedSection);
  const unlockedSection = progress.unlockedSection;
  
  const sections = [
    { id: 'schematic', title: 'The Schematic: De-Coding Hope', eyebrow: '01 // The Blueprint', icon: BookOpen },
    { id: 'circuit-board', title: "Your Brain's Circuit Board", eyebrow: '02 // The Hardware', icon: Cpu },
    { id: 'willpower', title: "Powering Up: The Science of 'Willpower'", eyebrow: '03 // The Voltage', icon: Zap },
    { id: 'waypower', title: "Designing the Wires: The Art of 'Waypower'", eyebrow: '04 // The Wiring', icon: Waypoints },
    { id: 'stress-shield', title: 'Stress Shield: Your Surge Protector', eyebrow: '05 // System Protection', icon: Shield },
    { id: 'upgrade', title: 'Upgrading the Hardware', eyebrow: '06 // System Upgrade', icon: Activity },
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
            <p className="text-[9px] font-black text-emerald-500 uppercase tracking-[0.4em] mb-0.5 underline">Module 02</p>
            <h1 className="font-serif font-bold text-lg tracking-tight text-stone-900">The Hope Protocol</h1>
          </div>
        </div>

        <div className="flex-grow space-y-4 overflow-y-auto no-scrollbar pr-2 relative">
          <div className="absolute left-[21px] top-6 bottom-6 w-0.5 bg-stone-100 -z-0" />
          <div className="absolute left-[21px] top-6 bottom-6 w-0.5">
              <motion.div
                  className="w-full bg-emerald-500 shadow-[0_0_10px_rgba(16,185,129,0.5)]"
                  style={{ height: `${progressPercentage}%` }}
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
           <ActivityRing progress={progressPercentage} /><p className="text-[11px] font-black text-stone-900 uppercase tracking-widest text-center">Progress</p>
        </div>
      </aside>

      <main className="flex-grow flex flex-col items-center py-10 md:py-24 px-6 md:px-16 overflow-y-auto h-screen relative">
        <div className="absolute inset-0 bg-[radial-gradient(#e5e7eb_1px,transparent_1px)] [background-size:32px_32px] opacity-40 pointer-events-none" />
        <div className="w-full max-w-4xl relative z-10">
          <AnimatePresence mode="wait">
            <motion.div key={activeSection} initial={{ opacity: 0, x: 20 }} animate={{ opacity: 1, x: 0 }} exit={{ opacity: 0, x: -20 }} transition={{ duration: 0.6, ease: [0.16, 1, 0.3, 1] }}>
              {activeSection === 0 && (
                <ReadingSection title="The Schematic: De-Coding Hope." eyebrow="Step 1" icon={BookOpen}>
                  <p>Forget everything you think you know about hope. It’s not a fluffy feeling or wishful thinking. According to decades of neuroscience, hope is a cognitive skill. It's a way of thinking, and like any skill, it can be learned, practiced, and mastered. Think of it as the technical schematic for your brain's motivation system.</p>
                  <p>The formula, developed by psychologist C.R. Snyder, is deceptively simple: Hope = Goals + <Highlight description="Also known as 'Willpower.' This is the raw motivational energy, the belief that you can and will start moving toward your goal. It's the 'I can do this' feeling, backed by your brain's reward system.">Agency</Highlight> + <Highlight description="Also known as 'Waypower.' This is the strategic thinking, the ability to generate multiple routes to your goal, anticipate problems, and adapt when you hit a roadblock. It's run by your brain's Prefrontal Cortex.">Pathways</Highlight>. A simple diagnostic can help you see where your own circuit is strong, and where it might need an upgrade.</p>
                  <HopeDiagnostic />
                  <MicroCommitment>
                    <p>Think of one vague goal you have (e.g., 'do better in French'). Open the notes app on your phone and re-write it as a clear, specific goal (e.g., 'Learn 10 new French vocabulary words by tomorrow evening').</p>
                  </MicroCommitment>
                </ReadingSection>
              )}
               {activeSection === 1 && (
                <ReadingSection title="Your Brain's Circuit Board." eyebrow="Step 2" icon={Cpu}>
                  <p>Your brain during your teenage years is a high-tech circuit board undergoing a massive upgrade. But there’s a catch: not all components get upgraded at the same speed. This is called the <Highlight description="The key neurological feature of adolescence. Your emotional, reward-seeking limbic system (the accelerator) matures early, while your rational, long-term planning Prefrontal Cortex (the brakes) is still under construction until your mid-20s.">Developmental Mismatch</Highlight>.</p>
                  <p>Your <Highlight description="The emotional, impulsive 'engine room' of your brain. It drives reward-seeking behaviour and emotional intensity. In teens, it's highly sensitive, giving you lots of raw motivational energy (Agency).">Limbic System</Highlight> (your 'accelerator') is fully matured, giving you huge amounts of energy and desire for goals (Agency). But your <Highlight description="The 'CEO' or 'planning department' of your brain, located behind your forehead. It's responsible for impulse control, long-term planning, and complex problem-solving (Pathways).">Prefrontal Cortex (PFC)</Highlight> (your 'brakes' and 'Sat-Nav') is still under construction. This means your desire to succeed often outstrips your brain's current capacity to plan the route, leading to frustration. This isn't a character flaw; it's a biological reality. Your job is to become a conscious engineer of this system.</p>
                  <BrainMismatchDiagram />
                   <MicroCommitment>
                    <p>Next time you feel a strong impulse to procrastinate, just notice it. Say to yourself, "That's my limbic system." Don't judge it, just label it. This simple act of noticing engages your PFC.</p>
                  </MicroCommitment>
                </ReadingSection>
              )}
               {activeSection === 2 && (
                <ReadingSection title="Powering Up: The Science of 'Willpower'." eyebrow="Step 3" icon={Zap}>
                    <p>Agency, or 'Willpower,' is the electrical current in your Hope Circuit. It’s the motivational force that gets you to start the engine. This isn't just 'trying hard'; it's a neurochemical process involving <Highlight description="The 'motivation molecule.' Dopamine is a neurotransmitter that drives you to seek rewards. A high-hope brain is better at generating its own dopamine hits by thinking about the future.">Dopamine</Highlight>.</p>
                    <p>The key is understanding the difference between "cold" and "hot" cognition. "Cold" cognition is abstract ("I need to study"). "Hot" cognition, or <Highlight description="Episodic Future Thinking (EFT) is the ability to vividly simulate personal future events. This 'hot' cognition is the engine that drives motivation, recruiting memory and emotional networks in the brain.">Episodic Future Thinking</Highlight>, is vivid and emotional ("I can see myself walking out of the exam hall feeling proud"). This "hot" thinking is what tells your PFC to activate the brain's reward system, giving you a motivational boost. You can literally learn to generate your own voltage.</p>
                    <DopamineDial />
                    <MicroCommitment>
                        <p>Before you start studying tonight, take 60 seconds. Close your eyes and vividly imagine the feeling of relief and pride after you finish. You're practicing Episodic Future Thinking and giving your brain a small, upfront hit of dopamine.</p>
                    </MicroCommitment>
                </ReadingSection>
              )}
              {activeSection === 3 && (
                <ReadingSection title="Designing the Wires: The Art of 'Waypower'." eyebrow="Step 4" icon={Waypoints}>
                  <p>If Agency is the raw power, Pathways thinking is the sophisticated wiring that directs it. It’s the most critical—and for teens, the most challenging—part of the Hope Circuit, because it depends entirely on your still-developing PFC.</p>
                  <p>Effective 'Waypower' involves three key skills: <strong>Planning</strong> (breaking a big goal into small steps), <strong>Flexibility</strong> (generating multiple routes), and <strong>Problem-Solving</strong> (anticipating obstacles). The 'Hope Map' is a tool used by psychologists to train this exact skill. It forces your PFC to design the circuit before you turn on the power, "inoculating" your brain against the stress of failure by pre-loading solutions.</p>
                  <HopeMap />
                  <MicroCommitment>
                    <p>Map out one tiny goal for tomorrow using the Goal-Pathway-Obstacle format. E.g., Goal: Get homework done by 8 pm. Pathway: Start at 6 pm in the kitchen. Obstacle: My brother will be noisy. Solution: Put on headphones.</p>
                  </MicroCommitment>
                </ReadingSection>
              )}
               {activeSection === 4 && (
                <ReadingSection title="Stress Shield: Your Surge Protector." eyebrow="Step 5" icon={Shield}>
                  <p>Hopelessness has a physical signature: a dysregulated stress response. When you face a threat (like a looming exam), your brain's alarm system—the <Highlight description="The Hypothalamic-Pituitary-Adrenal axis is your body's central stress response system. When it activates, it releases a cascade of hormones, culminating in cortisol.">HPA Axis</Highlight>—goes off, flooding your body with the stress hormone <Highlight description="Known as the 'stress hormone.' While essential in short bursts, chronically high levels of cortisol damage the brain, impair memory, and shut down access to your PFC (your planning centre).">Cortisol</Highlight>.</p>
                  <p>Hope acts as a neurobiological 'surge protector'. Having a clear goal and multiple pathways reduces the 'threat level' of a stressor. Your brain sees a difficult exam not as a life-threatening monster, but as a complex problem for which it has a plan. This calms the HPA axis, lowers cortisol, and keeps your PFC online when you need it most. See for yourself how a hopeful response can physically buffer the stress response in your body.</p>
                  <CortisolSimulator/>
                  <MicroCommitment>
                    <p>The next time you feel exam stress, consciously name the feeling ('I am feeling stressed about Maths'). Acknowledging the signal is the first step any engineer takes to regulate a system.</p>
                  </MicroCommitment>
                </ReadingSection>
              )}
               {activeSection === 5 && (
                <ReadingSection title="Upgrading the Hardware." eyebrow="Step 6" icon={Activity}>
                  <p>Your brain's wiring isn't fixed. The connections can be physically strengthened through practice, a process called <Highlight description="The brain's ability to reorganize itself by forming new neural connections throughout life. Every time you practice a skill—like planning a study session—you physically strengthen the white matter tracts involved.">Neuroplasticity</Highlight>. The 'highways' connecting your PFC to other brain regions, like the <Highlight description="The Superior Longitudinal Fasciculus is a massive 'superhighway' of white matter fibres connecting your frontal, parietal, and temporal lobes. It's the physical infrastructure for Pathways thinking.">Superior Longitudinal Fasciculus (SLF)</Highlight>, are like muscles: the more you use them for planning and goal-setting, the stronger and faster they get.</p>
                  <p>This means that every time you make a 'Hope Map' or break down a big task, you aren't just getting your work done—you are physically upgrading your brain's hardware for hope. One of the most powerful neuro-structural interventions is the 'Stop-Think' Protocol. It's a manual override for your brain's autopilot, forcing an engagement of the Hope Circuit.</p>
                   <MicroCommitment>
                    <p>Put a reminder on your phone for halfway through your study time tonight that just says 'STOP-THINK'. When it goes off, take 60 seconds to ask: "Is what I'm doing now the most effective way to reach my goal?"</p>
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