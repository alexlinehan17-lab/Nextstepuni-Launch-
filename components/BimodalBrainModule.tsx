/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
*/

import React, { useState, useEffect } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { 
  ArrowLeft, CheckCircle2, ArrowRight, 
  Lock, Flag, Brain, SlidersHorizontal, Lightbulb, PauseCircle, Zap, Clock
} from 'lucide-react';

type ModuleProgress = {
  unlockedSection: number;
};

interface BimodalBrainModuleProps {
  onBack: () => void;
  progress: ModuleProgress;
  onProgressUpdate: (progress: ModuleProgress) => void;
}

const Highlight = ({ children, description, color = "bg-purple-100/40", textColor = "text-purple-900", decorColor = "decoration-purple-400/40", hoverColor="hover:bg-purple-200/60" }: { children?: React.ReactNode, description: string, color?: string, textColor?: string, decorColor?: string, hoverColor?: string }) => {
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
              <p className="font-sans font-bold text-purple-400 mb-2 uppercase tracking-[0.2em] text-[9px]">The Academic Insight</p>
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
        <div className="w-12 h-12 rounded-2xl bg-stone-900 flex items-center justify-center text-purple-400 shadow-xl border border-white/10">
          <Icon size={24} />
        </div>
      </div>
      <span className="inline-flex items-center gap-2 px-3 py-1 bg-purple-50 text-purple-600 text-[10px] font-black tracking-[0.4em] uppercase rounded-full mb-4">
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
  <div className="my-12 p-8 bg-purple-50/50 border-2 border-dashed border-purple-200 rounded-3xl">
    <div className="flex items-start gap-5">
      <div className="w-11 h-11 rounded-xl bg-purple-500 text-white flex items-center justify-center shrink-0 mt-1 shadow-lg shadow-purple-500/20">
        <Flag size={20} />
      </div>
      <div>
        <h4 className="font-bold text-purple-800 text-sm uppercase tracking-widest">Your Mission (Under 5 Mins)</h4>
        <div className="text-stone-600 mt-2 font-medium leading-relaxed">
          {children}
        </div>
      </div>
    </div>
  </div>
);

const ActivityRing = ({ progress, color = "#a855f7" }: { progress: number, color?: string }) => {
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

const PinballSimulator = () => {
    const [mode, setMode] = useState<'focused' | 'diffuse'>('focused');
    return(
        <div className="my-10 p-8 md:p-12 bg-white rounded-[3rem] border border-stone-200 shadow-xl">
             <h4 className="font-serif text-2xl font-bold text-stone-800 text-center italic">The Pinball Metaphor</h4>
             <p className="text-center text-sm text-stone-500 mb-8">Toggle between modes to see how your thoughts travel.</p>
             <div className="w-full h-64 bg-stone-900 rounded-2xl p-4 relative overflow-hidden">
                <AnimatePresence>
                    {mode === 'focused' && [...Array(25)].map((_, i) => <motion.div key={`f${i}`} initial={{opacity:0, scale:0}} animate={{opacity:1, scale:1}} exit={{opacity:0, scale:0}} className="absolute w-4 h-4 bg-purple-400 rounded-full" style={{top: `${10 + Math.random()*80}%`, left: `${10 + Math.random()*80}%`}} />)}
                    {mode === 'diffuse' && [...Array(8)].map((_, i) => <motion.div key={`d${i}`} initial={{opacity:0, scale:0}} animate={{opacity:1, scale:1}} exit={{opacity:0, scale:0}} className="absolute w-4 h-4 bg-purple-400 rounded-full" style={{top: `${10 + Math.random()*80}%`, left: `${10 + Math.random()*80}%`}} />)}
                </AnimatePresence>
             </div>
             <div className="flex justify-center gap-4 mt-6">
                <button onClick={() => setMode('focused')} className="px-4 py-2 bg-purple-100 text-purple-800 rounded-lg">Focused Mode</button>
                <button onClick={() => setMode('diffuse')} className="px-4 py-2 bg-stone-100 text-stone-800 rounded-lg">Diffuse Mode</button>
             </div>
        </div>
    );
};


// --- MODULE COMPONENT ---
export const BimodalBrainModule: React.FC<BimodalBrainModuleProps> = ({ onBack, progress, onProgressUpdate }) => {
  const [activeSection, setActiveSection] = useState(progress.unlockedSection);
  const unlockedSection = progress.unlockedSection;
  
  const sections = [
    { id: 'two-modes', title: 'The Two Modes of Thinking', eyebrow: '01 // The Discovery', icon: Brain },
    { id: 'focused-engine', title: 'The Focused Engine', eyebrow: '02 // Deep Work', icon: Zap },
    { id: 'diffuse-network', title: 'The Diffuse Network', eyebrow: '03 // Creative Insights', icon: Lightbulb },
    { id: 'toggling', title: 'Toggling the Switch', eyebrow: '04 // The Art of the Break', icon: PauseCircle },
    { id: 'procrastination-link', title: 'The Procrastination Link', eyebrow: '05 // Why We Delay', icon: Clock },
    { id: 'blueprint', title: 'The Bimodal Blueprint', eyebrow: '06 // Your Action Plan', icon: SlidersHorizontal },
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
            <p className="text-[9px] font-black text-purple-500 uppercase tracking-[0.4em] mb-0.5 underline">Module 09</p>
            <h1 className="font-serif font-bold text-lg tracking-tight text-stone-900">The Bimodal Brain</h1>
          </div>
        </div>

        <div className="flex-grow space-y-4 overflow-y-auto no-scrollbar pr-2 relative">
          <div className="absolute left-[21px] top-6 bottom-6 w-0.5 bg-stone-100 -z-0" />
          <div className="absolute left-[21px] top-6 bottom-6 w-0.5">
              <motion.div
                  className="w-full bg-purple-500 shadow-[0_0_10px_rgba(168,85,247,0.5)]"
                  style={{ height: `${progressPercentage}%` }}
              />
          </div>
          {sections.map((section, idx) => {
            const isUnlocked = idx <= unlockedSection;
            const isActive = idx === activeSection;
            const isCompleted = idx < unlockedSection;
            return (
              <button key={section.id} disabled={!isUnlocked} onClick={() => handleJumpToSection(idx)} className={`relative z-10 w-full flex items-center gap-4 p-3 rounded-xl transition-all duration-500 text-left group ${isActive ? 'bg-purple-50 shadow-sm translate-x-2' : ''} ${!isUnlocked ? 'opacity-40 grayscale cursor-not-allowed' : 'hover:bg-stone-50'}`}>
                <div className={`w-11 h-11 rounded-xl flex items-center justify-center shrink-0 border-2 transition-all duration-500 ${isCompleted ? 'bg-purple-600 border-purple-600 text-white shadow-lg' : isActive ? 'bg-white border-purple-500 text-purple-600 shadow-xl rotate-12' : 'bg-white border-stone-200 text-stone-300'}`}>
                   {isCompleted ? <CheckCircle2 size={18} /> : isActive ? <section.icon size={18} /> : <Lock size={16} />}
                </div>
                <div className="flex-grow"><p className={`text-[8px] font-black uppercase tracking-widest ${isActive ? 'text-purple-500' : 'text-stone-400'}`}>{section.eyebrow.split('// ')[1]}</p><h4 className={`text-xs font-bold leading-tight ${isActive ? 'text-stone-900' : 'text-stone-500'}`}>{section.title}</h4></div>
              </button>
            );
          })}
        </div>
        <div className="mt-8 border-t border-stone-100 pt-8 flex flex-col items-center">
           <ActivityRing progress={progressPercentage} color="#a855f7" /><p className="text-[11px] font-black text-stone-900 uppercase tracking-widest text-center">Progress</p>
        </div>
      </aside>

      <main className="flex-grow flex flex-col items-center py-10 md:py-24 px-6 md:px-16 overflow-y-auto h-screen relative">
        <div className="absolute inset-0 bg-[radial-gradient(#e5e7eb_1px,transparent_1px)] [background-size:32px_32px] opacity-40 pointer-events-none" />
        <div className="w-full max-w-4xl relative z-10">
          <AnimatePresence mode="wait">
            <motion.div key={activeSection} initial={{ opacity: 0, x: 20 }} animate={{ opacity: 1, x: 0 }} exit={{ opacity: 0, x: -20 }} transition={{ duration: 0.6, ease: [0.16, 1, 0.3, 1] }}>
              {activeSection === 0 && (
                <ReadingSection title="The Two Modes of Thinking." eyebrow="Step 1" icon={Brain}>
                  <p>Your brain doesn't have just one mode of thinking; it has two, fundamentally different systems. The <Highlight description="A state of high-attention, analytical thought. It's what you use for solving familiar problems and executing procedures.">Focused Mode</Highlight> is your analytical workhorse. It's a state of intense concentration, perfect for solving a maths problem you already know how to do. The <Highlight description="A relaxed, low-attention state where your brain makes broad connections. It's the source of creative insights and 'Aha!' moments.">Diffuse Mode</Highlight> is your creative wanderer. It's a state of relaxed mind-wandering that allows your brain to make surprising new connections.</p>
                </ReadingSection>
              )}
              {activeSection === 1 && (
                <ReadingSection title="The Focused Engine." eyebrow="Step 2" icon={Zap}>
                    <p>The Focused Mode is like a pinball machine with tightly packed bumpers. Your thoughts bounce around in a small, localized area, working through the details of a problem you understand. This is essential for procedural fluency in subjects like Maths and Chemistry. It's the mode you're in during a Pomodoro sprint. However, if you get stuck on a new or difficult problem, this mode can be a trap. Your thoughts just keep hitting the same bumpers, leading to frustration.</p>
                    <PinballSimulator />
                </ReadingSection>
              )}
              {activeSection === 2 && (
                 <ReadingSection title="The Diffuse Network." eyebrow="Step 3" icon={Lightbulb}>
                    <p>The Diffuse Mode is when the bumpers are far apart. Your thoughts can travel long distances across your brain, connecting ideas from different subjects and experiences. This is where your 'Aha!' moments come from. You can't force this mode; you can only create the conditions for it to emerge. This happens when you relax your focus—by taking a walk, having a shower, or even just staring out the window.</p>
                </ReadingSection>
              )}
              {activeSection === 3 && (
                 <ReadingSection title="Toggling the Switch." eyebrow="Step 4" icon={PauseCircle}>
                    <p>The key to effective learning and problem-solving is learning to switch between these two modes. Work intensely in Focused Mode on a hard problem. When you get stuck, deliberately switch to Diffuse Mode by taking a break. Your brain will continue to work on the problem in the background (the <Highlight description="The subconscious processing of a problem that occurs when you are not actively thinking about it.">Incubation Effect</Highlight>). When you return to the problem, the solution will often seem obvious.</p>
                    <MicroCommitment><p>The next time you're stuck on a homework problem, don't just push harder. Get up and walk around for 5 minutes. You're not giving up; you're using a different part of your brain.</p></MicroCommitment>
                </ReadingSection>
              )}
              {activeSection === 4 && (
                <ReadingSection title="The Procrastination Link." eyebrow="Step 5" icon={Clock}>
                    <p>Procrastination is often caused by the discomfort of entering Focused Mode for a difficult task. The solution is to use a "Diffuse Mode warm-up." Instead of trying to force yourself into a 60-minute focused session, just commit to 5 minutes. This lowers the initial barrier and allows you to ease into the task. The pain of starting is always worse than the pain of continuing.</p>
                </ReadingSection>
              )}
              {activeSection === 5 && (
                 <ReadingSection title="The Bimodal Blueprint." eyebrow="Step 6" icon={SlidersHorizontal}>
                    <p>You now have the user manual for your brain's two gears. The strategic implication is clear: your study schedule must include both focused work *and* scheduled, unstructured breaks. This is not a luxury; it's a neurobiological necessity for deep learning and creativity.</p>
                </ReadingSection>
              )}
              <footer className="mt-24 flex items-center justify-between pt-12 border-t border-stone-200/60 px-4">
                <motion.button whileHover={{ scale: 1.05 }} whileTap={{ scale: 0.95 }} onClick={handlePrev} disabled={activeSection === 0} className={`flex items-center gap-4 bg-stone-100 text-stone-800 px-8 py-4 rounded-xl font-black text-[10px] uppercase tracking-widest transition-all shadow-sm ${activeSection === 0 ? 'opacity-0 pointer-events-none' : ''}`}>
                  <ArrowLeft size={16} /> Prev
                </motion.button>
                <motion.button whileHover={{ scale: 1.05 }} whileTap={{ scale: 0.95 }} onClick={handleCompleteSection} className="group relative flex items-center gap-4 bg-stone-900 text-white px-12 py-6 rounded-2xl font-black text-[12px] uppercase tracking-widest hover:bg-purple-600 transition-all shadow-[0_20px_50px_rgba(0,0,0,0.2)] overflow-hidden">
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
