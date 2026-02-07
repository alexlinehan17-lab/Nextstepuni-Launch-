
/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
*/

import React, { useState } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { 
  ArrowLeft, CheckCircle2, ArrowRight, 
  Lock, Flag, Cpu, Zap, Microscope, Construction, SlidersHorizontal
} from 'lucide-react';

interface TheMyelinManualModuleProps {
  onBack: () => void;
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
const MyelinWrapper = () => {
    const [wraps, setWraps] = useState(0);
    const maxWraps = 10;
    const speed = 10 + (wraps * 9); // Speed from 10 to 100

    return (
        <div className="my-10 p-8 md:p-12 bg-white rounded-[3rem] border border-stone-200 shadow-xl">
            <h4 className="font-serif text-2xl font-bold text-stone-800 text-center italic">The Myelin Wrapper</h4>
            <p className="text-center text-sm text-stone-500 mb-8">Each time you practice a skill, you add a layer of myelin, making the signal faster.</p>
            <div className="flex justify-center items-center h-24">
                <div className="relative w-64 h-2 bg-stone-200 rounded-full">
                     <div className="absolute inset-0 flex items-center">
                        <motion.div 
                            className="w-full h-2 bg-blue-300 rounded-full"
                            style={{
                                height: 2 + wraps * 2,
                                y: '-50%',
                                top: '50%',
                            }}
                            transition={{type: 'spring', damping: 10, stiffness: 100}}
                        >
                            <div className="absolute -left-3 top-1/2 -translate-y-1/2 w-4 h-4 bg-amber-400 rounded-full" />
                        </motion.div>
                     </div>
                </div>
            </div>
             <div className="flex justify-center items-center gap-6 mt-8">
                <button onClick={() => setWraps(w => Math.min(w + 1, maxWraps))} className="px-5 py-3 bg-amber-500 text-white font-bold rounded-lg shadow-lg hover:bg-amber-600 transition-colors text-sm">Practice Skill</button>
                <div className="text-center">
                    <p className="font-mono text-2xl font-bold">{speed} <span className="text-sm">m/s</span></p>
                    <p className="text-xs font-bold uppercase tracking-widest text-stone-400">Signal Speed</p>
                </div>
                 <button onClick={() => setWraps(0)} className="text-xs text-stone-400">Reset</button>
             </div>
        </div>
    )
}

const DeepPracticeSorter = () => {
    const activities = [
        { name: "Highlighting notes", type: "naive" },
        { name: "Doing a past paper (timed)", type: "deep" },
        { name: "Watching a video", type: "naive" },
        { name: "Explaining a concept out loud", type: "deep" },
    ];
    const [choice, setChoice] = useState<{[key: string]: 'naive' | 'deep' | null}>({});
    
    return (
        <div className="my-10 p-8 md:p-12 bg-white rounded-[3rem] border border-stone-200 shadow-xl">
            <h4 className="font-serif text-2xl font-bold text-stone-800 text-center italic">Deep vs. Naive Practice</h4>
            <p className="text-center text-sm text-stone-500 mb-8">Which of these activities trigger myelin growth?</p>
            <div className="space-y-4">
                {activities.map(act => (
                    <div key={act.name} className="p-4 bg-stone-50 border border-stone-200 rounded-lg flex justify-between items-center">
                        <span className="font-bold text-sm">{act.name}</span>
                        <div className="flex gap-2">
                           <button onClick={() => setChoice({...choice, [act.name]:'naive'})} className={`px-2 py-1 text-xs font-bold rounded ${choice[act.name] === 'naive' && act.type === 'naive' ? 'bg-emerald-200 text-emerald-800' : choice[act.name] === 'naive' && act.type === 'deep' ? 'bg-rose-200 text-rose-800' : 'bg-stone-200'}`}>Naive</button>
                           <button onClick={() => setChoice({...choice, [act.name]:'deep'})} className={`px-2 py-1 text-xs font-bold rounded ${choice[act.name] === 'deep' && act.type === 'deep' ? 'bg-emerald-200 text-emerald-800' : choice[act.name] === 'deep' && act.type === 'naive' ? 'bg-rose-200 text-rose-800' : 'bg-stone-200'}`}>Deep</button>
                        </div>
                    </div>
                ))}
            </div>
        </div>
    )
};


// --- MODULE COMPONENT ---
export const TheMyelinManualModule: React.FC<TheMyelinManualModuleProps> = ({ onBack }) => {
  const [activeSection, setActiveSection] = useState(0);
  const [unlockedSection, setUnlockedSection] = useState(0);
  
  const sections = [
    { id: 'silent-revolution', title: 'The Silent Revolution', eyebrow: '01 // The Other Brain', icon: Cpu },
    { id: 'signal-of-struggle', title: 'The Signal of Struggle', eyebrow: '02 // The Chemical Trigger', icon: Zap },
    { id: 'deep-practice', title: 'Deep Practice', eyebrow: '03 // The Behavioural Trigger', icon: SlidersHorizontal },
    { id: 'myelin-metaphors', title: 'The Mastery Metaphors', eyebrow: '04 // The Mental Models', icon: Microscope },
    { id: 'rules-of-myelination', title: 'The Rules of Myelination', eyebrow: '05 // The Action Plan', icon: Construction },
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
            <p className="text-[9px] font-black text-amber-500 uppercase tracking-[0.4em] mb-0.5 underline">Module 02</p>
            <h1 className="font-serif font-bold text-lg tracking-tight text-stone-900">The Myelin Manual</h1>
          </div>
        </div>

        <div className="flex-grow space-y-4 overflow-y-auto no-scrollbar pr-2 relative">
          <div className="absolute left-[21px] top-6 bottom-6 w-0.5 bg-stone-100 -z-0" />
          <div className="absolute left-[21px] top-6 bottom-6 w-0.5">
              <motion.div
                  className="w-full bg-amber-500 shadow-[0_0_10px_rgba(245,158,11,0.5)]"
                  initial={{ height: 0 }}
                  animate={{ height: sections.length > 1 ? `${(unlockedSection / (sections.length - 1)) * 100}%` : '0%' }}
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
           <ActivityRing progress={progress} color="#f59e0b" /><p className="text-[11px] font-black text-stone-900 uppercase tracking-widest text-center">Progress</p>
        </div>
      </aside>

      <main className="flex-grow flex flex-col items-center py-10 md:py-24 px-6 md:px-16 overflow-y-auto h-screen relative">
        <div className="absolute inset-0 bg-[radial-gradient(#e5e7eb_1px,transparent_1px)] [background-size:32px_32px] opacity-40 pointer-events-none" />
        <div className="w-full max-w-4xl relative z-10">
          <AnimatePresence mode="wait">
            <motion.div key={activeSection} initial={{ opacity: 0, x: 20 }} animate={{ opacity: 1, x: 0 }} exit={{ opacity: 0, x: -20 }} transition={{ duration: 0.6, ease: [0.16, 1, 0.3, 1] }}>
              {activeSection === 0 && (
                <ReadingSection title="The Silent Revolution." eyebrow="Step 1" icon={Cpu}>
                  <p>In the last module, we learned that your brain physically changes when you learn. Now, we're zooming in on the secret to mastering a skill and making it automatic. It's not just about strengthening the connections *between* brain cells (synapses). It's about upgrading the connections *themselves*.</p>
                  <p>Meet the unsung hero of your brain: the <Highlight description="A type of glial cell that produces myelin. Think of them as the expert electricians of your brain, responsible for insulating the wiring.">Oligodendrocyte</Highlight>. These cells are part of your 'other brain'—the glial cells—and their job is to wrap your neural circuits in a fatty insulation called <Highlight description="A lipid-rich substance that wraps around axons, acting like the plastic coating on an electrical wire. It prevents signal leakage and dramatically speeds up transmission.">Myelin</Highlight>. This process turns your brain's bumpy dirt roads into super-fast motorways. This isn't just about knowledge; it's about speed, precision, and automaticity.</p>
                </ReadingSection>
              )}
               {activeSection === 1 && (
                <ReadingSection title="The Signal of Struggle." eyebrow="Step 2" icon={Zap}>
                    <p>How does this electrician know which wire to insulate? It listens for a specific signal. When you engage in intense, focused effort—like trying to solve a tough maths problem—your neurons fire at a very high frequency. This intense firing isn't a silent event. It causes the neuron to release chemical signals, like ATP and Glutamate, along its entire length.</p>
                    <p>These chemicals are like a frantic call to the oligodendrocyte, screaming, "This circuit is important! It's being used intensely! We need an upgrade!" The feeling of <Highlight description="From a neurobiological perspective, 'struggle' is the behavioural state that generates the high-frequency neural firing necessary to trigger activity-dependent myelination.">struggle</Highlight> is not a sign you're failing; it's the physical sensation of your brain sending the order to build a better, faster circuit.</p>
                </ReadingSection>
              )}
              {activeSection === 2 && (
                <ReadingSection title="Deep Practice." eyebrow="Step 3" icon={SlidersHorizontal}>
                  <p>The specific behavior that sends this "upgrade" signal is called <Highlight description="Popularized by Daniel Coyle, it's a method of practicing that involves intense focus, operating at the edge of your ability, embracing errors, and repeating the process. It is the direct trigger for myelination.">Deep Practice</Highlight>. It's the opposite of passively re-reading your notes. Naive practice is easy and feels productive, but it sends a weak, background signal that doesn't trigger myelination. It creates an "illusion of competence."</p>
                  <p>Deep practice is hard, uncomfortable, and full of errors. It involves things like doing past papers without notes, forcing yourself to retrieve information from scratch, and pushing yourself just outside your comfort zone. That discomfort is the signal. It's the "heavy lifting" that tells your brain to build more muscle—or in this case, more myelin.</p>
                  <DeepPracticeSorter />
                </ReadingSection>
              )}
              {activeSection === 3 && (
                <ReadingSection title="The Mastery Metaphors." eyebrow="Step 4" icon={Microscope}>
                  <p>To really get a grip on this, we can use a few powerful analogies for what's happening inside your head when you engage in Deep Practice.</p>
                  <p>Think of it as upgrading your home internet from dial-up to fibre optic **broadband**. Unmyelinated circuits are slow and have low bandwidth—they can only handle one simple idea at a time. A myelinated circuit can handle multiple complex ideas at once without "buffering." Or think of it as paving a **dirt road into a motorway**. The first time you learn something, it's slow and bumpy. With deep practice, you pave that road, allowing information to travel at high speed, automatically.</p>
                  <MyelinWrapper/>
                </ReadingSection>
              )}
               {activeSection === 4 && (
                <ReadingSection title="The Rules of Myelination." eyebrow="Step 5" icon={Construction}>
                    <p>Myelination follows a few simple, non-negotiable rules. First, **struggle is not optional**. Easy practice doesn't send the signal. You must operate in the "sweet spot" where you're making errors and correcting them. That error-correction loop is the sound of the construction crew getting to work.</p>
                    <p>Second, **it's permanent but slow**. Unlike short-term memory, myelin is robust. Once a skill is wrapped, it stays with you. This is why cramming (synaptic) fails for long-term retention, but deep practice (myelin) works. But it takes time—weeks of consistent practice. You can't build a motorway overnight. Every session of deep practice adds another thin layer of tape, another ring to the tree.</p>
                    <MicroCommitment>
                        <p>Identify your "sweet spot" for one subject. What is a task that is not too easy (you get it all right) and not too hard (you get it all wrong)? That's your target zone for the next study session.</p>
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
