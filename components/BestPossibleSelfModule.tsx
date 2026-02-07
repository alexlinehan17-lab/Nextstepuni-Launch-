
/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
*/

import React, { useState, useEffect } from 'react';
import { motion, AnimatePresence, Reorder } from 'framer-motion';
import { 
  ArrowLeft, CheckCircle2, ArrowRight,
  Lock, Flag, MapPin, BatteryWarning, Filter, Zap, ClipboardCheck, Lightbulb, Shield, Brain
} from 'lucide-react';

type ModuleProgress = {
  unlockedSection: number;
};

// FIX: Added progress and onProgressUpdate props to align with App.tsx usage and enable state management.
interface BestPossibleSelfModuleProps {
  onBack: () => void;
  progress: ModuleProgress;
  onProgressUpdate: (progress: ModuleProgress) => void;
}

const Highlight = ({ children, description, color = "bg-blue-100/40" }: { children: React.ReactNode, description: string, color?: string }) => {
  const [isOpen, setIsOpen] = useState(false);

  return (
    <span className="relative inline-block mx-0.5">
      <button 
        onClick={(e) => {
          e.stopPropagation();
          setIsOpen(!isOpen);
        }}
        className={`relative inline-flex items-center px-2 py-0.5 font-bold ${color} rounded-md cursor-help hover:bg-blue-200/60 transition-all duration-300 decoration-blue-400/40 underline decoration-2 underline-offset-4 text-blue-900`}
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
              <p className="font-sans font-bold text-blue-400 mb-2 uppercase tracking-[0.2em] text-[9px]">The Academic Insight</p>
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
        <div className="w-12 h-12 rounded-2xl bg-stone-900 flex items-center justify-center text-blue-400 shadow-xl border border-white/10">
          <Icon size={24} />
        </div>
      </div>
      <span className="inline-flex items-center gap-2 px-3 py-1 bg-blue-50 text-blue-600 text-[10px] font-black tracking-[0.4em] uppercase rounded-full mb-4">
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
  <div className="my-12 p-8 bg-blue-50/50 border-2 border-dashed border-blue-200 rounded-3xl">
    <div className="flex items-start gap-5">
      <div className="w-11 h-11 rounded-xl bg-blue-500 text-white flex items-center justify-center shrink-0 mt-1 shadow-lg shadow-blue-500/20">
        <Flag size={20} />
      </div>
      <div>
        <h4 className="font-bold text-blue-800 text-sm uppercase tracking-widest">Your Mission (Under 5 Mins)</h4>
        <div className="text-stone-600 mt-2 font-medium leading-relaxed">
          {children}
        </div>
      </div>
    </div>
  </div>
);

const ActivityRing = ({ progress, color = "#3b82f6" }: { progress: number, color?: string }) => {
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

const WOOPPlanner = () => {
    const [woop, setWoop] = useState({ wish: '', outcome: '', obstacle: '', plan: '' });
    const update = (field: keyof typeof woop, value: string) => setWoop(prev => ({...prev, [field]: value}));
    const isComplete = Object.values(woop).every(v => v.trim() !== '');

    return(
        <div className="my-10 p-8 md:p-12 bg-white rounded-[3rem] border border-stone-200 shadow-xl">
            <h4 className="font-serif text-2xl font-bold text-stone-800 text-center italic">Your WOOP Blueprint</h4>
            <div className="space-y-4 mt-8">
                <input value={woop.wish} onChange={e => update('wish', e.target.value)} placeholder="WISH: Your most important wish..." className="w-full p-4 bg-stone-50 rounded-lg border-2 border-stone-100 focus:border-blue-500 outline-none"/>
                <input value={woop.outcome} onChange={e => update('outcome', e.target.value)} placeholder="OUTCOME: The best result from that..." className="w-full p-4 bg-stone-50 rounded-lg border-2 border-stone-100 focus:border-blue-500 outline-none"/>
                <input value={woop.obstacle} onChange={e => update('obstacle', e.target.value)} placeholder="OBSTACLE: The main inner barrier..." className="w-full p-4 bg-stone-50 rounded-lg border-2 border-stone-100 focus:border-blue-500 outline-none"/>
                <input value={woop.plan} onChange={e => update('plan', e.target.value)} placeholder="PLAN: If [obstacle], then I will..." className="w-full p-4 bg-stone-50 rounded-lg border-2 border-stone-100 focus:border-blue-500 outline-none"/>
            </div>
            {isComplete && (
                <motion.div initial={{opacity:0}} animate={{opacity:1}} className="text-center mt-6">
                    <p className="text-sm font-bold text-emerald-600">Blueprint complete! You've turned a wish into an actionable plan.</p>
                </motion.div>
            )}
        </div>
    );
};

export const BestPossibleSelfModule: React.FC<BestPossibleSelfModuleProps> = ({ onBack, progress, onProgressUpdate }) => {
  const [activeSection, setActiveSection] = useState(progress.unlockedSection);
  const unlockedSection = progress.unlockedSection;

  const sections = [
    { id: 'daydream-problem', title: 'The Daydream Problem', eyebrow: '01 // The Trap', icon: BatteryWarning },
    { id: 'bps-protocol', title: 'The "Best Possible Self" Protocol', eyebrow: '02 // The Vision', icon: MapPin },
    { id: 'mental-contrasting', title: 'The Reality Check', eyebrow: '03 // Mental Contrasting', icon: Filter },
    { id: 'woop-method', title: 'The WOOP Method', eyebrow: '04 // The System', icon: Zap },
    { id: 'implementation', title: 'Implementation & Habit', eyebrow: '05 // The Action Plan', icon: ClipboardCheck },
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
        <div className="flex items-center gap-4 mb-12">
          <motion.button whileHover={{ scale: 1.05 }} whileTap={{ scale: 0.95 }} onClick={onBack} className="p-2 rounded-full transition-all border border-stone-200/50 shadow-sm bg-white">
            <ArrowLeft size={16} className="text-stone-700" />
          </motion.button>
          <div>
            <p className="text-[9px] font-black text-blue-500 uppercase tracking-[0.4em] mb-0.5 underline">Module 04</p>
            <h1 className="font-serif font-bold text-lg tracking-tight text-stone-900">Best Possible Self</h1>
          </div>
        </div>

        <div className="flex-grow space-y-4 overflow-y-auto no-scrollbar pr-2 relative">
          <div className="absolute left-[21px] top-6 bottom-6 w-0.5 bg-stone-100 -z-0" />
          <div className="absolute left-[21px] top-6 bottom-6 w-0.5">
              <motion.div
                  className="w-full bg-blue-500 shadow-[0_0_10px_rgba(59,130,246,0.5)]"
                  style={{ height: `${progressPercentage}%` }}
              />
          </div>
          {sections.map((section, idx) => {
            const isUnlocked = idx <= unlockedSection;
            const isActive = idx === activeSection;
            const isCompleted = idx < unlockedSection;
            return (
              <button key={section.id} disabled={!isUnlocked} onClick={() => handleJumpToSection(idx)} className={`relative z-10 w-full flex items-center gap-4 p-3 rounded-xl transition-all duration-500 text-left group ${isActive ? 'bg-blue-50 shadow-sm translate-x-2' : ''} ${!isUnlocked ? 'opacity-40 grayscale cursor-not-allowed' : 'hover:bg-stone-50'}`}>
                <div className={`w-11 h-11 rounded-xl flex items-center justify-center shrink-0 border-2 transition-all duration-500 ${isCompleted ? 'bg-blue-600 border-blue-600 text-white shadow-lg' : isActive ? 'bg-white border-blue-500 text-blue-600 shadow-xl rotate-12' : 'bg-white border-stone-200 text-stone-300'}`}>
                   {isCompleted ? <CheckCircle2 size={18} /> : isActive ? <section.icon size={18} /> : <Lock size={16} />}
                </div>
                <div className="flex-grow"><p className={`text-[8px] font-black uppercase tracking-widest ${isActive ? 'text-blue-500' : 'text-stone-400'}`}>{section.eyebrow.split('// ')[1]}</p><h4 className={`text-xs font-bold leading-tight ${isActive ? 'text-stone-900' : 'text-stone-500'}`}>{section.title}</h4></div>
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
                <ReadingSection title="The Daydream Problem." eyebrow="Step 1" icon={BatteryWarning}>
                  <p>We're often told to "think positive" and visualize our dreams. But research by Gabriele Oettingen reveals a paradox: pure <Highlight description="Indulging in idealized fantasies of the future. Counter-intuitively, this can relax you so much that it actually lowers your energy and motivation to take action.">positive fantasizing</Highlight> can be demotivating. It tricks your brain into feeling like you've already achieved the goal, reducing the energy you commit to the hard work needed to get there.</p>
                </ReadingSection>
              )}
              {activeSection === 1 && (
                <ReadingSection title="The 'Best Possible Self' Protocol." eyebrow="Step 2" icon={MapPin}>
                  <p>The solution isn't to stop dreaming, but to dream with purpose. The <Highlight description="A positive psychology intervention where you write in detail about an optimal future version of yourself. This has been shown to increase positive mood and build a sense of purpose.">'Best Possible Self' (BPS)</Highlight> exercise is a scientifically-validated tool for this. By writing a vivid, detailed description of your future life where you've achieved all your goals, you create a clear, emotionally-resonant target for your brain to aim for.</p>
                  <MicroCommitment><p>Take 5 minutes. In your phone's notes app, write one paragraph describing what your life would look like in 5 years if everything went as well as it possibly could. Be specific.</p></MicroCommitment>
                </ReadingSection>
              )}
               {activeSection === 2 && (
                <ReadingSection title="The Reality Check." eyebrow="Step 3" icon={Filter}>
                  <p>A vivid dream is not enough. The crucial next step is to ground that dream in reality. This is <Highlight description="The process of contrasting your desired future with the real-world obstacles that stand in your way. This contrast is what generates the energy for action.">Mental Contrasting</Highlight>. After vividly imagining your 'Best Possible Self', you must immediately and just as vividly imagine the primary obstacle *within you* that holds you back. It's not about external problems; it's about your own habits and beliefs.</p>
                </ReadingSection>
              )}
               {activeSection === 3 && (
                <ReadingSection title="The WOOP Method." eyebrow="Step 4" icon={Zap}>
                    <p>This process of combining a positive vision with a realistic obstacle is the core of the <Highlight description="A powerful, four-step goal-setting strategy: Wish, Outcome, Obstacle, Plan. It combines positive thinking with a realistic assessment of barriers.">WOOP Method</Highlight>. It's a simple but profound algorithm for turning wishes into action.</p>
                    <p>1. **Wish:** What is your most important goal? 2. **Outcome:** What is the best feeling or result if you achieve it? 3. **Obstacle:** What is the main thing *inside you* that stands in the way? 4. **Plan:** Create an "If [Obstacle], then I will [Action]" plan.</p>
                </ReadingSection>
              )}
               {activeSection === 4 && (
                <ReadingSection title="Implementation & Habit." eyebrow="Step 5" icon={ClipboardCheck}>
                  <p>You now have the full WOOP protocol. It's a portable, 5-minute tool you can use every day to align your daily actions with your long-term vision. By repeatedly running this mental simulation, you train your brain to automatically link your biggest dreams to your smallest daily habits. Use the blueprint below to run your first WOOP.</p>
                  <WOOPPlanner />
                </ReadingSection>
              )}
              <footer className="mt-24 flex items-center justify-between pt-12 border-t border-stone-200/60 px-4">
                <motion.button whileHover={{ scale: 1.05 }} whileTap={{ scale: 0.95 }} onClick={handlePrev} disabled={activeSection === 0} className={`flex items-center gap-4 bg-stone-100 text-stone-800 px-8 py-4 rounded-xl font-black text-[10px] uppercase tracking-widest transition-all shadow-sm ${activeSection === 0 ? 'opacity-0 pointer-events-none' : ''}`}>
                  <ArrowLeft size={16} /> Prev
                </motion.button>
                <motion.button whileHover={{ scale: 1.05 }} whileTap={{ scale: 0.95 }} onClick={handleCompleteSection} className="group relative flex items-center gap-4 bg-stone-900 text-white px-12 py-6 rounded-2xl font-black text-[12px] uppercase tracking-widest hover:bg-blue-600 transition-all shadow-[0_20px_50px_rgba(0,0,0,0.2)] overflow-hidden">
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
