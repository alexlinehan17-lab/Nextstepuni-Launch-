
/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
*/

import React, { useState, useEffect } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { 
  ArrowLeft, CheckCircle2, ArrowRight, 
  Lock, Flag, Server, Filter, Archive, BrainCircuit, Moon, ClipboardCheck
} from 'lucide-react';

interface TheCognitiveArchitectureModuleProps {
  onBack: () => void;
}

const Highlight = ({ children, description, color = "bg-fuchsia-100/40", textColor = "text-fuchsia-900", decorColor = "decoration-fuchsia-400/40", hoverColor="hover:bg-fuchsia-200/60" }: { children?: React.ReactNode, description: string, color?: string, textColor?: string, decorColor?: string, hoverColor?: string }) => {
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
              <p className="font-sans font-bold text-fuchsia-400 mb-2 uppercase tracking-[0.2em] text-[9px]">The Academic Insight</p>
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
        <div className="w-12 h-12 rounded-2xl bg-stone-900 flex items-center justify-center text-fuchsia-400 shadow-xl border border-white/10">
          <Icon size={24} />
        </div>
      </div>
      <span className="inline-flex items-center gap-2 px-3 py-1 bg-fuchsia-50 text-fuchsia-600 text-[10px] font-black tracking-[0.4em] uppercase rounded-full mb-4">
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
  <div className="my-12 p-8 bg-fuchsia-50/50 border-2 border-dashed border-fuchsia-200 rounded-3xl">
    <div className="flex items-start gap-5">
      <div className="w-11 h-11 rounded-xl bg-fuchsia-500 text-white flex items-center justify-center shrink-0 mt-1 shadow-lg shadow-fuchsia-500/20">
        <Flag size={20} />
      </div>
      <div>
        <h4 className="font-bold text-fuchsia-800 text-sm uppercase tracking-widest">Your Mission (Under 5 Mins)</h4>
        <div className="text-stone-600 mt-2 font-medium leading-relaxed">
          {children}
        </div>
      </div>
    </div>
  </div>
);

const ActivityRing = ({ progress, color = "#d946ef" }: { progress: number, color?: string }) => {
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

const MemoryFlowVisualizer = () => {
  const [attention, setAttention] = useState(false);
  return (
    <div className="my-10 p-8 md:p-12 bg-white rounded-[3rem] border border-stone-200 shadow-xl">
      <h4 className="font-serif text-2xl font-bold text-stone-800 text-center italic">The Memory Pipeline</h4>
      <p className="text-center text-sm text-stone-500 mb-8">Information is either lost or transferred. Attention is the gatekeeper.</p>
      <div className="flex items-center justify-between text-center font-bold text-xs h-24">
        <span>Sensory</span>
        <svg className="w-full h-px mx-4"><line x1="0" y1="0" x2="100%" y2="0" stroke="black" strokeDasharray="4"/></svg>
        <span>Short-Term</span>
        <svg className="w-full h-px mx-4"><line x1="0" y1="0" x2="100%" y2="0" stroke="black" strokeDasharray="4"/></svg>
        <span>Long-Term</span>
      </div>
      <div className="flex justify-center mt-6">
        <button onClick={() => setAttention(!attention)} className="px-4 py-2 bg-fuchsia-500 text-white font-bold text-sm rounded-lg">{attention ? 'De-Focus' : 'Pay Attention'}</button>
      </div>
    </div>
  );
};

const WorkingMemorySimulator = () => {
  const [items, setItems] = useState<string[]>([]);
  const [inputValue, setInputValue] = useState('');
  const [showItems, setShowItems] = useState(false);
  const [result, setResult] = useState<number|null>(null);

  useEffect(() => {
    if (showItems) {
      const timer = setTimeout(() => setShowItems(false), 3000); // Items visible for 3s
      return () => clearTimeout(timer);
    }
  }, [showItems]);

  const startGame = () => {
    const newItems = Array.from({length: 7}, () => Math.floor(Math.random() * 90 + 10).toString());
    setItems(newItems);
    setShowItems(true);
    setResult(null);
    setInputValue('');
  };
  
  const checkAnswer = () => {
    const userItems = inputValue.split(' ').filter(Boolean);
    const score = items.filter(item => userItems.includes(item)).length;
    setResult(score);
  };
  
  if (result !== null) {
    return (
      <div className="my-10 p-8 md:p-12 bg-white rounded-[3rem] border border-stone-200 shadow-xl text-center">
        <h4 className="font-serif text-2xl font-bold text-stone-800 text-center italic">Results</h4>
        <p>You correctly recalled {result} out of {items.length} items.</p>
        <p className="text-xs text-stone-500">The original items were: {items.join(', ')}</p>
        <button onClick={startGame} className="mt-4 px-4 py-2 bg-fuchsia-500 text-white font-bold text-sm rounded-lg">Try Again</button>
      </div>
    );
  }

  return (
    <div className="my-10 p-8 md:p-12 bg-white rounded-[3rem] border border-stone-200 shadow-xl text-center">
      <h4 className="font-serif text-2xl font-bold text-stone-800 text-center italic">STM Bottleneck Test</h4>
      {!showItems && items.length === 0 && <button onClick={startGame} className="px-4 py-2 bg-fuchsia-500 text-white font-bold text-sm rounded-lg">Start</button>}
      
      {showItems && <p className="text-3xl font-mono tracking-widest">{items.join(' ')}</p>}
      
      {!showItems && items.length > 0 && 
        <div>
          <input value={inputValue} onChange={e => setInputValue(e.target.value)} placeholder="Type the numbers, separated by spaces" className="w-full p-2 border-2 rounded-md"/>
          <button onClick={checkAnswer} className="mt-4 px-4 py-2 bg-emerald-500 text-white font-bold text-sm rounded-lg">Check Answer</button>
        </div>
      }
    </div>
  );
};


// --- MODULE COMPONENT ---
export const TheCognitiveArchitectureModule: React.FC<TheCognitiveArchitectureModuleProps> = ({ onBack }) => {
  const [activeSection, setActiveSection] = useState(0);
  const [unlockedSection, setUnlockedSection] = useState(0);
  
  const sections = [
    { id: 'three-stores', title: 'The Three Memory Stores', eyebrow: '01 // The Blueprint', icon: Server },
    { id: 'bottleneck', title: 'The Working Memory Bottleneck', eyebrow: '02 // The Bottleneck', icon: Filter },
    { id: 'filing-cabinet', title: 'The LTM Filing Cabinet', eyebrow: '03 // The Library', icon: Archive },
    { id: 'save-button', title: 'Hitting the "Save" Button', eyebrow: '04 // The Biology of Saving', icon: BrainCircuit },
    { id: 'night-shift', title: 'The Night Shift', eyebrow: '05 // The Role of Sleep', icon: Moon },
    { id: 'checklist', title: 'The Operator\'s Checklist', eyebrow: '06 // The Action Plan', icon: ClipboardCheck },
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
            <p className="text-[9px] font-black text-fuchsia-500 uppercase tracking-[0.4em] mb-0.5 underline">Module 04</p>
            <h1 className="font-serif font-bold text-lg tracking-tight text-stone-900">Cognitive Architecture</h1>
          </div>
        </div>

        <div className="flex-grow space-y-4 overflow-y-auto no-scrollbar pr-2 relative">
          <div className="absolute left-[21px] top-6 bottom-6 w-0.5 bg-stone-100 -z-0" />
          <div className="absolute left-[21px] top-6 bottom-6 w-0.5">
              <motion.div
                  className="w-full bg-fuchsia-500 shadow-[0_0_10px_rgba(217,70,239,0.5)]"
                  initial={{ height: 0 }}
                  animate={{ height: sections.length > 1 ? `${(unlockedSection / (sections.length - 1)) * 100}%` : '0%' }}
              />
          </div>
          {sections.map((section, idx) => {
            const isUnlocked = idx <= unlockedSection;
            const isActive = idx === activeSection;
            const isCompleted = idx < unlockedSection;
            return (
              <button key={section.id} disabled={!isUnlocked} onClick={() => handleJumpToSection(idx)} className={`relative z-10 w-full flex items-center gap-4 p-3 rounded-xl transition-all duration-500 text-left group ${isActive ? 'bg-fuchsia-50 shadow-sm translate-x-2' : ''} ${!isUnlocked ? 'opacity-40 grayscale cursor-not-allowed' : 'hover:bg-stone-50'}`}>
                <div className={`w-11 h-11 rounded-xl flex items-center justify-center shrink-0 border-2 transition-all duration-500 ${isCompleted ? 'bg-fuchsia-600 border-fuchsia-600 text-white shadow-lg' : isActive ? 'bg-white border-fuchsia-500 text-fuchsia-600 shadow-xl rotate-12' : 'bg-white border-stone-200 text-stone-300'}`}>
                   {isCompleted ? <CheckCircle2 size={18} /> : isActive ? <section.icon size={18} /> : <Lock size={16} />}
                </div>
                <div className="flex-grow"><p className={`text-[8px] font-black uppercase tracking-widest ${isActive ? 'text-fuchsia-500' : 'text-stone-400'}`}>{section.eyebrow.split('// ')[1]}</p><h4 className={`text-xs font-bold leading-tight ${isActive ? 'text-stone-900' : 'text-stone-500'}`}>{section.title}</h4></div>
              </button>
            );
          })}
        </div>

        <div className="mt-8 border-t border-stone-100 pt-8 flex flex-col items-center">
           <ActivityRing progress={progress} color="#d946ef" /><p className="text-[11px] font-black text-stone-900 uppercase tracking-widest text-center">Progress</p>
        </div>
      </aside>

      <main className="flex-grow flex flex-col items-center py-10 md:py-24 px-6 md:px-16 overflow-y-auto h-screen relative">
        <div className="absolute inset-0 bg-[radial-gradient(#e5e7eb_1px,transparent_1px)] [background-size:32px_32px] opacity-40 pointer-events-none" />
        <div className="w-full max-w-4xl relative z-10">
          <AnimatePresence mode="wait">
            <motion.div key={activeSection} initial={{ opacity: 0, x: 20 }} animate={{ opacity: 1, x: 0 }} exit={{ opacity: 0, x: -20 }} transition={{ duration: 0.6, ease: [0.16, 1, 0.3, 1] }}>
              {activeSection === 0 && (
                <ReadingSection title="The Three Memory Stores." eyebrow="Step 1" icon={Server}>
                  <p>To win the Leaving Cert, you need to understand the machine you're working with: your own brain. The most useful model for this is the <Highlight description="A classic psychological model that proposes memory consists of three separate stores: Sensory Memory, Short-Term Memory (STM), and Long-Term Memory (LTM).">Multi-Store Model</Highlight>. It breaks your memory into three parts.</p>
                  <p>First, there's <Highlight description="An ultra-short-term buffer for information from your senses. It lasts for milliseconds and is mostly outside your conscious control.">Sensory Memory</Highlight>, the brief echo of what you see or hear. Anything you don't pay attention to here is gone forever. If you *do* pay attention, it moves to <Highlight description="A temporary storage space with very limited capacity and duration. Also known as Working Memory.">Short-Term Memory (STM)</Highlight>, your brain's mental workbench. From there, it has to be deliberately transferred to <Highlight description="The vast, durable library of your mind. This is where knowledge needs to end up to be useful in an exam.">Long-Term Memory (LTM)</Highlight>, the permanent hard drive. Your entire job as a student is to manage this transfer process effectively.</p>
                </ReadingSection>
              )}
              {activeSection === 1 && (
                <ReadingSection title="The Working Memory Bottleneck." eyebrow="Step 2" icon={Filter}>
                  <p>Your Short-Term Memory, or <Highlight description="The part of your mind that holds and actively manipulates a small amount of information for a short time. It's the 'RAM' of your brain.">Working Memory</Highlight>, is the biggest bottleneck in your learning. It's shockingly limited. Classic research suggested you can hold about 7 items, but for complex Leaving Cert topics, it's more like **4 'chunks' of information**.</p>
                  <p>Even worse, without active effort, this information decays in about **15-30 seconds**. This is why you can read a whole page of a textbook and have no memory of it. The information entered your working memory but evaporated before it could be processed. Cramming jams this bottleneck, creating a fragile memory that feels strong but is quickly erased.</p>
                  <WorkingMemorySimulator/>
                </ReadingSection>
              )}
              {activeSection === 2 && (
                <ReadingSection title="The LTM Filing Cabinet." eyebrow="Step 3" icon={Archive}>
                  <p>Your Long-Term Memory is not one big box; it's a sophisticated filing cabinet with different drawers for different types of knowledge. Knowing which drawer you're using helps you study smarter.</p>
                  <p>The first is <Highlight description="Memory for facts, concepts, and general knowledge. This is your 'textbook' memory for things like Biology definitions or History dates.">Semantic Memory</Highlight>—your library of facts. The second is <Highlight description="Memory for personal experiences and specific events. Remembering a specific Chemistry experiment is episodic.">Episodic Memory</Highlight>—your personal photo album of events. The third, and most critical for many subjects, is <Highlight description="Memory for skills and 'how-to' knowledge, like how to solve a Maths equation or conjugate a French verb. It's your 'muscle memory' for the mind.">Procedural Memory</Highlight>. Maths isn't about memorizing facts; it's about building automated procedures.</p>
                </ReadingSection>
              )}
              {activeSection === 3 && (
                <ReadingSection title="Hitting the 'Save' Button." eyebrow="Step 4" icon={BrainCircuit}>
                  <p>The transfer from your temporary workbench (STM) to your permanent hard drive (LTM) is called <Highlight description="The process of transforming temporary memories into durable, long-term ones. The 'depth' of this process determines the strength of the memory.">Encoding</Highlight>. Not all encoding is equal. <Highlight description="Processing information based on its surface features, like its sound or appearance (e.g., rote repetition). It creates weak memories.">Shallow Processing</Highlight>, like just re-reading a definition, creates weak, flimsy memories.</p>
                  <p><Highlight description="Processing information based on its meaning and connecting it to your existing knowledge. This creates strong, interconnected memories.">Deep Processing</Highlight> is about linking new information to what you already know. For example, learning that "mitochondria is the powerhouse of the cell" is shallow. Understanding *how* it produces ATP and why that's essential for your muscles to work is deep. The biological basis for this is <Highlight description="The long-lasting strengthening of the connections (synapses) between neurons. It's the physical basis of memory, often summarized as 'neurons that fire together, wire together.'">Long-Term Potentiation (LTP)</Highlight>—you're physically strengthening the wiring.</p>
                </ReadingSection>
              )}
              {activeSection === 4 && (
                <ReadingSection title="The Night Shift." eyebrow="Step 5" icon={Moon}>
                  <p>Here’s a non-negotiable rule of your brain's biology: the final "save" button is hit while you sleep. During the day, new information is temporarily stored in a part of your brain called the <Highlight description="A seahorse-shaped structure in the brain that acts as a temporary buffer or 'inbox' for new memories. It's like your brain's RAM.">Hippocampus</Highlight>. It's a volatile, temporary storage space.</p>
                  <p>During deep sleep, your brain runs a process called <Highlight description="The physiological process where memories are transferred from the temporary storage of the hippocampus to the permanent storage of the neocortex. This happens primarily during sleep.">System Consolidation</Highlight>. It replays the day's events and transfers important memories from the hippocampus to your main hard drive, the <Highlight description="The outer layer of the brain responsible for higher-order thinking. It's the 'hard drive' for your long-term memories.">Neocortex</Highlight>. Pulling an all-nighter is like trying to learn a new topic while constantly hitting 'cancel' on the save dialog. It's self-sabotage.</p>
                </ReadingSection>
              )}
              {activeSection === 5 && (
                <ReadingSection title="The Operator's Checklist." eyebrow="Step 6" icon={ClipboardCheck}>
                  <p>Understanding your cognitive architecture gives you an owner's manual for your own brain. It shows that high performance isn't about "natural talent"; it's about running the right processes. All the evidence-based strategies—Active Recall, Spacing, Interleaving—are simply ways to optimize this natural memory pipeline.</p>
                  <p>But even the best strategies will fail if the hardware is compromised. Your <Highlight description="Your biological state, including sleep, nutrition, hydration, and stress levels. Your cognitive function is highly dependent on your physiological baseline.">Physiological State</Highlight> is the foundation. High stress floods your brain with <Highlight description="The 'stress hormone.' Chronically high levels can impair the function of your hippocampus, making it harder to form and retrieve memories.">Cortisol</Highlight>, effectively blocking memory retrieval. Dehydration and poor nutrition starve your brain of the resources it needs. Getting your baseline right isn't a 'wellness' tip; it's a core academic strategy.</p>
                  <MicroCommitment>
                    <p>Tonight, set an alarm to put your phone away 60 minutes before you go to bed. This single act of 'sleep hygiene' has a bigger impact on your memory than an extra hour of cramming.</p>
                  </MicroCommitment>
                </ReadingSection>
              )}
              <footer className="mt-24 flex items-center justify-between pt-12 border-t border-stone-200/60 px-4">
                <motion.button whileHover={{ scale: 1.05 }} whileTap={{ scale: 0.95 }} onClick={handlePrev} disabled={activeSection === 0} className={`flex items-center gap-4 bg-stone-100 text-stone-800 px-8 py-4 rounded-xl font-black text-[10px] uppercase tracking-widest transition-all shadow-sm ${activeSection === 0 ? 'opacity-0 pointer-events-none' : ''}`}>
                  <ArrowLeft size={16} /> Prev
                </motion.button>
                <motion.button whileHover={{ scale: 1.05 }} whileTap={{ scale: 0.95 }} onClick={handleCompleteSection} className="group relative flex items-center gap-4 bg-stone-900 text-white px-12 py-6 rounded-2xl font-black text-[12px] uppercase tracking-widest hover:bg-fuchsia-600 transition-all shadow-[0_20px_50px_rgba(0,0,0,0.2)] overflow-hidden">
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
