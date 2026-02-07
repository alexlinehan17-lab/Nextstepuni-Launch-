

/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
*/

import React, { useState } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { 
  ArrowLeft, CheckCircle2, ArrowRight, 
  Lock, Flag, Book, RotateCcw, Brain, Link, Wrench
} from 'lucide-react';

interface ThePowerOfYetModuleProps {
  onBack: () => void;
}

const Highlight = ({ children, description, color = "bg-yellow-100/40", textColor = "text-yellow-900", decorColor = "decoration-yellow-400/40", hoverColor="hover:bg-yellow-200/60" }: { children?: React.ReactNode, description: string, color?: string, textColor?: string, decorColor?: string, hoverColor?: string }) => {
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
              <p className="font-sans font-bold text-yellow-400 mb-2 uppercase tracking-[0.2em] text-[9px]">The Academic Insight</p>
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
        <div className="w-12 h-12 rounded-2xl bg-stone-900 flex items-center justify-center text-yellow-400 shadow-xl border border-white/10">
          <Icon size={24} />
        </div>
      </div>
      <span className="inline-flex items-center gap-2 px-3 py-1 bg-yellow-50 text-yellow-600 text-[10px] font-black tracking-[0.4em] uppercase rounded-full mb-4">
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
  <div className="my-12 p-8 bg-yellow-50/50 border-2 border-dashed border-yellow-200 rounded-3xl">
    <div className="flex items-start gap-5">
      <div className="w-11 h-11 rounded-xl bg-yellow-500 text-white flex items-center justify-center shrink-0 mt-1 shadow-lg shadow-yellow-500/20">
        <Flag size={20} />
      </div>
      <div>
        <h4 className="font-bold text-yellow-800 text-sm uppercase tracking-widest">Your Mission (Under 5 Mins)</h4>
        <div className="text-stone-600 mt-2 font-medium leading-relaxed">
          {children}
        </div>
      </div>
    </div>
  </div>
);

const ActivityRing = ({ progress, color = "#ca8a04" }: { progress: number, color?: string }) => {
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
const ErrorSignalVisualizer = () => {
    const [mindset, setMindset] = useState<'fixed' | 'growth' | null>(null);
    return(
        <div className="my-10 p-8 md:p-12 bg-white rounded-[3rem] border border-stone-200 shadow-xl">
             <h4 className="font-serif text-2xl font-bold text-stone-800 text-center italic">The Brain on "Yet"</h4>
             <p className="text-center text-sm text-stone-500 mb-8">Scenario: You make a mistake on a Maths problem. Which brain is yours?</p>
             <div className="grid grid-cols-2 gap-6">
                <div className="text-center">
                    <h5 className="font-bold mb-2">The "I Can't" Brain (Fixed)</h5>
                    <svg viewBox="0 0 100 50" className="w-full h-auto">
                       <path d="M 0 40 L 100 40" stroke="#e5e7eb" strokeWidth="1" />
                       <path d="M 40 40 C 45 40 48 30 52 30 S 57 40 60 40" stroke="#f43f5e" strokeWidth="1" fill="none" />
                       <text x="50" y="20" textAnchor="middle" fontSize="6" fill="#f43f5e">Small 'Pe' Wave</text>
                    </svg>
                    <p className="text-xs text-stone-500 mt-2">The brain "looks away" from the error to protect the ego. No learning occurs.</p>
                </div>
                 <div className="text-center">
                    <h5 className="font-bold mb-2">The "I Can't... Yet" Brain (Growth)</h5>
                    <svg viewBox="0 0 100 50" className="w-full h-auto">
                       <path d="M 0 40 L 100 40" stroke="#e5e7eb" strokeWidth="1" />
                       <path d="M 40 40 C 45 40 48 5 52 5 S 57 40 60 40" stroke="#10b981" strokeWidth="3" fill="none" />
                       <text x="50" y="20" textAnchor="middle" fontSize="6" fill="#10b981">Large 'Pe' Wave</text>
                    </svg>
                    <p className="text-xs text-stone-500 mt-2">The brain leans in, allocating massive attention to the error. Learning is triggered.</p>
                </div>
             </div>
        </div>
    );
};

const YetAudit = () => {
    const [block, setBlock] = useState('');
    const [action, setAction] = useState('');
    
    return (
        <div className="my-10 p-8 md:p-12 bg-stone-900 rounded-[3rem] border border-white/10 shadow-2xl text-white">
            <h4 className="font-serif text-3xl font-bold text-center italic mb-8">Your "Yet" Audit</h4>
            <div className="space-y-6 max-w-xl mx-auto">
                <div>
                    <p className="text-xs font-bold uppercase tracking-widest text-yellow-400 mb-2">1. IDENTIFY THE BLOCK</p>
                    <input value={block} onChange={e => setBlock(e.target.value)} placeholder="e.g., I can't write a good Irish essay" className="w-full bg-white/5 rounded-lg p-3 text-sm text-stone-300 focus:outline-none focus:ring-2 focus:ring-yellow-400"/>
                </div>
                <div>
                    <p className="text-xs font-bold uppercase tracking-widest text-yellow-400 mb-2">2. ADD "YET"</p>
                    <div className="p-3 bg-white/10 rounded-lg text-sm text-stone-300 min-h-[44px]">
                        {block ? `I can't write a good Irish essay... yet.` : <span className="opacity-50">...</span>}
                    </div>
                </div>
                <div>
                    <p className="text-xs font-bold uppercase tracking-widest text-yellow-400 mb-2">3. BRIDGE TO ACTION</p>
                    <input value={action} onChange={e => setAction(e.target.value)} placeholder="...so I will ask my teacher for one example tomorrow." className="w-full bg-white/5 rounded-lg p-3 text-sm text-stone-300 focus:outline-none focus:ring-2 focus:ring-yellow-400"/>
                </div>
            </div>
        </div>
    );
}


// --- MODULE COMPONENT ---
export const ThePowerOfYetModule: React.FC<ThePowerOfYetModuleProps> = ({ onBack }) => {
  const [activeSection, setActiveSection] = useState(0);
  const [unlockedSection, setUnlockedSection] = useState(0);
  
  const sections = [
    { id: 'full-stop', title: 'The Full Stop', eyebrow: '01 // The Verdict', icon: Book },
    { id: 'software-patch', title: 'The Software Patch', eyebrow: '02 // The "Yet" Upgrade', icon: RotateCcw },
    { id: 'brain-on-yet', title: 'The Brain on "Yet"', eyebrow: '03 // The Science', icon: Brain },
    { id: 'action-bridge', title: 'The Action Bridge', eyebrow: '04 // The Protocol', icon: Link },
    { id: 'yet-audit', title: 'Your "Yet" Audit', eyebrow: '05 // The Blueprint', icon: Wrench },
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
            <p className="text-[9px] font-black text-yellow-500 uppercase tracking-[0.4em] mb-0.5 underline">Module 07</p>
            <h1 className="font-serif font-bold text-lg tracking-tight text-stone-900">The Power of "Yet"</h1>
          </div>
        </div>

        <div className="flex-grow space-y-4 overflow-y-auto no-scrollbar pr-2 relative">
          <div className="absolute left-[21px] top-6 bottom-6 w-0.5 bg-stone-100 -z-0" />
          <div className="absolute left-[21px] top-6 bottom-6 w-0.5">
              <motion.div
                  className="w-full bg-yellow-500 shadow-[0_0_10px_rgba(202,138,4,0.5)]"
                  initial={{ height: 0 }}
                  animate={{ height: sections.length > 1 ? `${(unlockedSection / (sections.length - 1)) * 100}%` : '0%' }}
              />
          </div>
          {sections.map((section, idx) => {
            const isUnlocked = idx <= unlockedSection;
            const isActive = idx === activeSection;
            const isCompleted = idx < unlockedSection;
            return (
              <button key={section.id} disabled={!isUnlocked} onClick={() => handleJumpToSection(idx)} className={`relative z-10 w-full flex items-center gap-4 p-3 rounded-xl transition-all duration-500 text-left group ${isActive ? 'bg-yellow-50 shadow-sm translate-x-2' : ''} ${!isUnlocked ? 'opacity-40 grayscale cursor-not-allowed' : 'hover:bg-stone-50'}`}>
                <div className={`w-11 h-11 rounded-xl flex items-center justify-center shrink-0 border-2 transition-all duration-500 ${isCompleted ? 'bg-yellow-600 border-yellow-600 text-white shadow-lg' : isActive ? 'bg-white border-yellow-500 text-yellow-600 shadow-xl rotate-12' : 'bg-white border-stone-200 text-stone-300'}`}>
                   {isCompleted ? <CheckCircle2 size={18} /> : isActive ? <section.icon size={18} /> : <Lock size={16} />}
                </div>
                <div className="flex-grow"><p className={`text-[8px] font-black uppercase tracking-widest ${isActive ? 'text-yellow-500' : 'text-stone-400'}`}>{section.eyebrow.split('// ')[1]}</p><h4 className={`text-xs font-bold leading-tight ${isActive ? 'text-stone-900' : 'text-stone-500'}`}>{section.title}</h4></div>
              </button>
            );
          })}
        </div>

        <div className="mt-8 border-t border-stone-100 pt-8 flex flex-col items-center">
           <ActivityRing progress={progress} color="#ca8a04" /><p className="text-[11px] font-black text-stone-900 uppercase tracking-widest text-center">Progress</p>
        </div>
      </aside>

      <main className="flex-grow flex flex-col items-center py-10 md:py-24 px-6 md:px-16 overflow-y-auto h-screen relative">
        <div className="absolute inset-0 bg-[radial-gradient(#e5e7eb_1px,transparent_1px)] [background-size:32px_32px] opacity-40 pointer-events-none" />
        <div className="w-full max-w-4xl relative z-10">
          <AnimatePresence mode="wait">
            <motion.div key={activeSection} initial={{ opacity: 0, x: 20 }} animate={{ opacity: 1, x: 0 }} exit={{ opacity: 0, x: -20 }} transition={{ duration: 0.6, ease: [0.16, 1, 0.3, 1] }}>
              {activeSection === 0 && (
                <ReadingSection title="The Full Stop." eyebrow="Step 1" icon={Book}>
                  <p>When you say "I can't do Honours Maths" or "I'm not good at this," you're putting a full stop at the end of the sentence. Your brain interprets this as a <Highlight description="A final judgment on your ability, suggesting you have reached the limit of your capacity. It closes the door on future effort.">summative judgment</Highlight>. It's a verdict that says: "This story is over. You were found wanting."</p>
                  <p>This is the language of a <Highlight description="The belief that intelligence and abilities are fixed, unchangeable traits. People with this mindset see failure as a diagnosis of their incompetence.">Fixed Mindset</Highlight>. It's a dead end. It shuts down effort, kills motivation, and tells your brain to disengage from the problem. To build resilience, you need to learn to turn these full stops into commas.</p>
                </ReadingSection>
              )}
               {activeSection === 1 && (
                <ReadingSection title="The Software Patch." eyebrow="Step 2" icon={RotateCcw}>
                  <p>The solution is a simple but profound software patch for your brain: the word "yet." By adding this single word to the end of a fixed statement, you fundamentally change its meaning. "I can't do this" becomes "I can't do this... yet." "I don't understand this" becomes "I don't understand this... yet."</p>
                  <p>This transforms the sentence from a final verdict into a progress report. It implies a <Highlight description="A sense that your current ability is just one point on a longer journey of learning, not a permanent state.">temporal trajectory</Highlight>. A famous study in a Chicago high school replaced "Fail" grades with "Not Yet." The result was a dramatic increase in persistence and task completion. You're not a failure; you're just unfinished.</p>
                  <MicroCommitment>
                    <p>Listen to yourself and your friends today. Every time you hear an "I can't" statement, mentally add "yet" to the end of it. Just notice how it changes the feeling.</p>
                  </MicroCommitment>
                </ReadingSection>
              )}
              {activeSection === 2 && (
                <ReadingSection title="The Brain on 'Yet'." eyebrow="Step 3" icon={Brain}>
                  <p>This isn't just a mental trick; it has a direct effect on your brain's hardware. When you make a mistake, your brain produces a signal called the <Highlight description="The 'Error Positivity' signal is a brainwave that shows you're paying conscious attention to a mistake. A bigger 'Pe' wave means you're more likely to learn from the error.">Pe (Error Positivity)</Highlight>. It's the physical sign that you're leaning in to analyse your failure.</p>
                  <p>Research shows that people with a fixed mindset have a very small Pe signal. Their brain detects the error but quickly "looks away" to protect the ego. People with a growth mindset have a huge Pe signal—they allocate massive attention to the mistake. The word "yet" is a cognitive cue that tells your brain, "This task is not over," keeping your brain in that high-Pe state of engagement and analysis.</p>
                  <ErrorSignalVisualizer />
                </ReadingSection>
              )}
               {activeSection === 3 && (
                <ReadingSection title="The Action Bridge." eyebrow="Step 4" icon={Link}>
                    <p>"Yet" is powerful, but it's not magic. On its own, it's just wishful thinking. To be effective, "yet" must be tethered to a behavioral plan. This is the crucial third step of the protocol: the <Highlight description="A concrete, specific action that you will take to move from 'not yet' to 'can'. This tethers optimism to a behavioral plan.">Bridge to Action</Highlight>.</p>
                    <p>The full, powerful sentence isn't just "I can't do this yet." It's "I can't do this yet, *so I will*..." This simple addition prevents "Yet" from being an excuse and turns it into a launchpad. It links the optimistic mindset to a concrete, strategic next step. This is the full protocol: **1. Identify the Block, 2. Add "Yet", 3. Bridge to Action.**</p>
                    <MicroCommitment>
                      <p>Think of your toughest subject. Your Block might be "I can't understand Topic X." Your Bridge could be "I will watch one YouTube video explaining it tonight."</p>
                    </MicroCommitment>
                </ReadingSection>
              )}
               {activeSection === 4 && (
                <ReadingSection title="Your 'Yet' Audit." eyebrow="Step 5" icon={Wrench}>
                  <p>You now have the full protocol. It's a tool for rewriting your internal monologue in real-time, turning moments of despair into moments of strategic action. The final step is to apply it to your own life.</p>
                  <p>Use the blueprint below to identify one specific academic block you're facing. Then, run it through the "Identify-Append-Bridge" protocol. This isn't just an exercise; it's you, right now, actively rewiring your brain for resilience. This is how you turn the science into a skill.</p>
                  <YetAudit />
                </ReadingSection>
              )}
              <footer className="mt-24 flex items-center justify-between pt-12 border-t border-stone-200/60 px-4">
                <motion.button whileHover={{ scale: 1.05 }} whileTap={{ scale: 0.95 }} onClick={handlePrev} disabled={activeSection === 0} className={`flex items-center gap-4 bg-stone-100 text-stone-800 px-8 py-4 rounded-xl font-black text-[10px] uppercase tracking-widest transition-all shadow-sm ${activeSection === 0 ? 'opacity-0 pointer-events-none' : ''}`}>
                  <ArrowLeft size={16} /> Prev
                </motion.button>
                <motion.button whileHover={{ scale: 1.05 }} whileTap={{ scale: 0.95 }} onClick={handleCompleteSection} className="group relative flex items-center gap-4 bg-stone-900 text-white px-12 py-6 rounded-2xl font-black text-[12px] uppercase tracking-widest hover:bg-yellow-600 transition-all shadow-[0_20px_50px_rgba(0,0,0,0.2)] overflow-hidden">
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
