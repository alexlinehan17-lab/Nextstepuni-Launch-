
/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
*/

import React, { useState } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { 
  ArrowLeft, CheckCircle2, ArrowRight, 
  Lock, Flag, HelpCircle, BatteryWarning, Link, BookCopy, Cpu, Wrench
} from 'lucide-react';

interface ElaborativeInterrogationModuleProps {
  onBack: () => void;
}

const Highlight = ({ children, description, color = "bg-pink-100/40", textColor = "text-pink-900", decorColor = "decoration-pink-400/40", hoverColor="hover:bg-pink-200/60" }: { children?: React.ReactNode, description: string, color?: string, textColor?: string, decorColor?: string, hoverColor?: string }) => {
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
              <p className="font-sans font-bold text-pink-400 mb-2 uppercase tracking-[0.2em] text-[9px]">The Academic Insight</p>
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
        <div className="w-12 h-12 rounded-2xl bg-stone-900 flex items-center justify-center text-pink-400 shadow-xl border border-white/10">
          <Icon size={24} />
        </div>
      </div>
      <span className="inline-flex items-center gap-2 px-3 py-1 bg-pink-50 text-pink-600 text-[10px] font-black tracking-[0.4em] uppercase rounded-full mb-4">
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
  <div className="my-12 p-8 bg-pink-50/50 border-2 border-dashed border-pink-200 rounded-3xl">
    <div className="flex items-start gap-5">
      <div className="w-11 h-11 rounded-xl bg-pink-500 text-white flex items-center justify-center shrink-0 mt-1 shadow-lg shadow-pink-500/20">
        <Flag size={20} />
      </div>
      <div>
        <h4 className="font-bold text-pink-800 text-sm uppercase tracking-widest">Your Mission (Under 5 Mins)</h4>
        <div className="text-stone-600 mt-2 font-medium leading-relaxed">
          {children}
        </div>
      </div>
    </div>
  </div>
);

const ActivityRing = ({ progress, color = "#ec4899" }: { progress: number, color?: string }) => {
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

const HungryManExperiment = () => {
    const [method, setMethod] = useState<'passive' | 'ei' | null>(null);
    let retention = method === 'passive' ? 37 : method === 'ei' ? 72 : 0;
    
    return (
        <div className="my-10 p-8 md:p-12 bg-white rounded-[3rem] border border-stone-200 shadow-xl">
            <h4 className="font-serif text-2xl font-bold text-stone-800 text-center italic">The "Hungry Man" Experiment</h4>
            <p className="text-center text-sm text-stone-500 mb-6">See the dramatic effect of asking "Why?" on your memory.</p>
            <div className="p-4 bg-stone-100 rounded-xl text-center font-mono mb-6">"The hungry man got in the car."</div>
            <div className="grid grid-cols-2 gap-4">
                <button onClick={() => setMethod('passive')} className="p-4 bg-stone-200 rounded-xl">Read Passively</button>
                <button onClick={() => setMethod('ei')} className="p-4 bg-pink-200 rounded-xl">Ask "Why?"</button>
            </div>
            {method && (
                 <div className="mt-6">
                    <p className="text-center text-sm font-bold mb-2">Memory Retention After 1 Week:</p>
                    <div className="w-full h-8 bg-stone-100 rounded-full"><motion.div className="h-full bg-pink-500 rounded-full" initial={{width:0}} animate={{width: `${retention}%`}} /></div>
                 </div>
            )}
        </div>
    );
};

const FlashcardFlipper = () => {
    const [isFlipped, setIsFlipped] = useState(false);
    return(
        <div className="my-10 p-8 md:p-12 bg-white rounded-[3rem] border border-stone-200 shadow-xl text-center">
            <h4 className="font-serif text-2xl font-bold text-stone-800 text-center italic">Flashcard 2.0</h4>
             <p className="text-center text-sm text-stone-500 mb-6">Stop making "what" cards. Start making "why" cards.</p>
            <div className="w-full h-48 [perspective:1000px]" onClick={() => setIsFlipped(!isFlipped)}>
                <motion.div className="relative w-full h-full" style={{transformStyle: 'preserve-3d'}} animate={{rotateY: isFlipped ? 180 : 0}}>
                    <div className="absolute w-full h-full [backface-visibility:hidden] rounded-2xl bg-stone-900 text-white flex flex-col items-center justify-center p-4">
                        <p className="text-xs text-stone-400 mb-2">FRONT</p>
                        <p className="font-bold">Why is the left ventricle wall thicker than the right?</p>
                    </div>
                    <div className="absolute w-full h-full [backface-visibility:hidden] rounded-2xl bg-emerald-500 text-white flex flex-col items-center justify-center p-4" style={{transform: 'rotateY(180deg)'}}>
                        <p className="text-xs text-emerald-200 mb-2">BACK</p>
                        <p className="font-bold text-sm">Because it pumps blood to the whole body (high pressure), while the right only pumps to the lungs (low pressure).</p>
                    </div>
                </motion.div>
            </div>
        </div>
    );
};

// --- MODULE COMPONENT ---
export const ElaborativeInterrogationModule: React.FC<ElaborativeInterrogationModuleProps> = ({ onBack }) => {
  const [activeSection, setActiveSection] = useState(0);
  const [unlockedSection, setUnlockedSection] = useState(0);
  
  const sections = [
    { id: 'why-engine', title: 'The "Why" Engine', eyebrow: '01 // The Mechanism', icon: HelpCircle },
    { id: 'rules-of-road', title: 'The Rules of the Road', eyebrow: '02 // The Constraints', icon: BatteryWarning },
    { id: 'stem-toolkit', title: 'The STEM Toolkit', eyebrow: '03 // Science & Maths', icon: Cpu },
    { id: 'humanities-engine', title: 'The Humanities Engine', eyebrow: '04 // Essays & Arguments', icon: BookCopy },
    { id: 'language-edge', title: 'The Language Edge', eyebrow: '05 // Gaeilge & Beyond', icon: Link },
    { id: 'study-protocol', title: 'The EI Study Protocol', eyebrow: '06 // The Action Plan', icon: Wrench },
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
            <p className="text-[9px] font-black text-pink-500 uppercase tracking-[0.4em] mb-0.5 underline">Module 05</p>
            <h1 className="font-serif font-bold text-lg tracking-tight text-stone-900">Elaborative Interrogation</h1>
          </div>
        </div>

        <div className="flex-grow space-y-4 overflow-y-auto no-scrollbar pr-2 relative">
          <div className="absolute left-[21px] top-6 bottom-6 w-0.5 bg-stone-100 -z-0" />
          <div className="absolute left-[21px] top-6 bottom-6 w-0.5">
              <motion.div
                  className="w-full bg-pink-500 shadow-[0_0_10px_rgba(236,72,153,0.5)]"
                  initial={{ height: 0 }}
                  animate={{ height: sections.length > 1 ? `${(unlockedSection / (sections.length - 1)) * 100}%` : '0%' }}
              />
          </div>
          {sections.map((section, idx) => {
            const isUnlocked = idx <= unlockedSection;
            const isActive = idx === activeSection;
            const isCompleted = idx < unlockedSection;
            return (
              <button key={section.id} disabled={!isUnlocked} onClick={() => handleJumpToSection(idx)} className={`relative z-10 w-full flex items-center gap-4 p-3 rounded-xl transition-all duration-500 text-left group ${isActive ? 'bg-pink-50 shadow-sm translate-x-2' : ''} ${!isUnlocked ? 'opacity-40 grayscale cursor-not-allowed' : 'hover:bg-stone-50'}`}>
                <div className={`w-11 h-11 rounded-xl flex items-center justify-center shrink-0 border-2 transition-all duration-500 ${isCompleted ? 'bg-pink-600 border-pink-600 text-white shadow-lg' : isActive ? 'bg-white border-pink-500 text-pink-600 shadow-xl rotate-12' : 'bg-white border-stone-200 text-stone-300'}`}>
                   {isCompleted ? <CheckCircle2 size={18} /> : isActive ? <section.icon size={18} /> : <Lock size={16} />}
                </div>
                <div className="flex-grow"><p className={`text-[8px] font-black uppercase tracking-widest ${isActive ? 'text-pink-500' : 'text-stone-400'}`}>{section.eyebrow.split('// ')[1]}</p><h4 className={`text-xs font-bold leading-tight ${isActive ? 'text-stone-900' : 'text-stone-500'}`}>{section.title}</h4></div>
              </button>
            );
          })}
        </div>

        <div className="mt-8 border-t border-stone-100 pt-8 flex flex-col items-center">
           <ActivityRing progress={progress} color="#ec4899" /><p className="text-[11px] font-black text-stone-900 uppercase tracking-widest text-center">Progress</p>
        </div>
      </aside>

      <main className="flex-grow flex flex-col items-center py-10 md:py-24 px-6 md:px-16 overflow-y-auto h-screen relative">
        <div className="absolute inset-0 bg-[radial-gradient(#e5e7eb_1px,transparent_1px)] [background-size:32px_32px] opacity-40 pointer-events-none" />
        <div className="w-full max-w-4xl relative z-10">
          <AnimatePresence mode="wait">
            <motion.div key={activeSection} initial={{ opacity: 0, x: 20 }} animate={{ opacity: 1, x: 0 }} exit={{ opacity: 0, x: -20 }} transition={{ duration: 0.6, ease: [0.16, 1, 0.3, 1] }}>
              {activeSection === 0 && (
                <ReadingSection title="The 'Why' Engine." eyebrow="Step 1" icon={HelpCircle}>
                  <p>Learning isn't about absorbing facts; it's about actively connecting them. <Highlight description="A powerful study technique that involves generating an explanation for why a fact or concept is true. It forces you to connect new information to your existing knowledge.">Elaborative Interrogation (EI)</Highlight> is a simple but profound technique that turns you from a passive reader into an active detective. The core of EI is asking one simple question: "Why is this true?"</p>
                  <p>When you ask "Why?", you force your brain to search its long-term memory for related information, creating a rich network of connections. This transforms an isolated, easy-to-forget fact into part of a memorable story.</p>
                  <p>This was powerfully demonstrated in the famous "hungry man" study. One group of students read a simple sentence like "The hungry man got into the car." A second group was told to ask "Why?". This second group inferred a reason ("...to go to a restaurant"), creating a richer memory. On a surprise test later, the "Why?" group's recall was almost double that of the passive readers (72% vs 37%).</p>
                  <HungryManExperiment/>
                </ReadingSection>
              )}
               {activeSection === 1 && (
                <ReadingSection title="The Rules of the Road." eyebrow="Step 2" icon={BatteryWarning}>
                  <p>EI is a high-performance tool, but it has two critical operating constraints. First is the <Highlight description="The counterintuitive finding that EI is most effective when you already have some background knowledge. It's for deepening understanding, not for learning something from scratch.">Prior Knowledge Paradox</Highlight>. If you ask "Why?" about a topic you know nothing about, you'll just invent wrong answers. EI is a consolidation tool, not a first-contact tool.</p>
                  <p>Second, EI is mentally exhausting. It requires slow, effortful <Highlight description="A term from psychologist Daniel Kahneman for slow, deliberate, and analytical thinking. It's powerful but consumes a lot of mental energy.">System 2 thinking</Highlight>. Doing it when you're tired can lead to a state of <Highlight description="The idea that self-control and cognitive resources are finite. When you're depleted, your ability to perform effortful mental tasks (like EI) diminishes significantly.">Ego Depletion</Highlight>, making the strategy less effective. Use it during your high-energy study periods.</p>
                </ReadingSection>
              )}
              {activeSection === 2 && (
                <ReadingSection title="The STEM Toolkit." eyebrow="Step 3" icon={Cpu}>
                  <p>For STEM subjects, EI is your secret weapon against rote learning. In Biology, it helps you bridge the gap between understanding a concept and knowing the specific keywords the marking scheme demands. Asking "Why is the cell membrane semi-permeable?" forces you to retrieve the key ideas of phospholipids and proteins.</p>
                  <p>In Maths, EI is brilliant for <Highlight description="Understanding the 'why' behind a mathematical rule or formula, rather than just memorizing the 'how'.">conceptual understanding</Highlight>. Asking "Why does the integral of a velocity-time graph give distance?" cements the core idea. However, it's inefficient for <Highlight description="The ability to perform mathematical procedures quickly and accurately. This is built through repetitive practice, not constant questioning.">procedural fluency</Highlight>. Don't stop to ask "why" during every line of a long calculation in an exam; build that fluency through practice beforehand.</p>
                </ReadingSection>
              )}
               {activeSection === 3 && (
                <ReadingSection title="The Humanities Engine." eyebrow="Step 4" icon={BookCopy}>
                    <p>In essay subjects like History, EI is an "analytical engine." It shifts you from just describing what happened (narrative) to explaining *why* it happened (analysis). Instead of just stating "Collins signed the Treaty," you ask "Why did he sign it?" The answer becomes your thesis statement, instantly boosting your marks for argument and evaluation.</p>
                    <p>For Geography, which is built on <Highlight description="Significant Relevant Points (SRPs) are the building blocks of a Geography answer. Each one is a developed piece of factual information worth marks.">SRPs</Highlight>, EI automates the "Statement + Development" structure. Statement: "Earthquakes are common in Japan." EI Prompt: "Why?" Development: "Because Japan is on the convergence of four tectonic plates..." You've just created a perfect, two-mark SRP.</p>
                </ReadingSection>
              )}
               {activeSection === 4 && (
                <ReadingSection title="The Language Edge." eyebrow="Step 5" icon={Link}>
                  <p>For the Irish Oral, rote-learning scripts is a recipe for disaster. The examiner is trained to spot them and will throw you off-script. EI is the key to building a flexible, robust "web of knowledge" around a topic. By recursively asking "Why?" ("Why do you play football?" -> "Because I like the team spirit." -> "Why is team spirit important?"), you build multiple connections.</p>
                  <p>This allows you to pivot naturally during the conversation. If the examiner asks about friends, you can link it back to the friends you made playing football. If they ask about health, you can talk about how football keeps you fit. You're no longer reciting a script; you're navigating a mental map you built yourself.</p>
                </ReadingSection>
              )}
               {activeSection === 5 && (
                <ReadingSection title="The EI Study Protocol." eyebrow="Step 6" icon={Wrench}>
                  <p>You have the science. Now, here is the simple, four-step protocol to integrate EI into your study routine.</p>
                  <p><strong>1. The Audit:</strong> Look at your notes and highlight the core facts. <strong>2. The Interrogation:</strong> For each fact, write "Why?" in the margin. <strong>3. The Elaboration:</strong> Answer the question in your own words. <strong>4. The Verification:</strong> Check your answer against the textbook to avoid learning errors. This cycle transforms passive note-taking into an active, memory-building process. One of the most powerful outputs of this is the "Why" flashcard.</p>
                  <FlashcardFlipper />
                  <MicroCommitment>
                    <p>Take one page of your notes from any subject. For the next 5 minutes, go through and simply write a "Why?" question next to every main fact or definition. That's the first step.</p>
                  </MicroCommitment>
                </ReadingSection>
              )}
              <footer className="mt-24 flex items-center justify-between pt-12 border-t border-stone-200/60 px-4">
                <motion.button whileHover={{ scale: 1.05 }} whileTap={{ scale: 0.95 }} onClick={handlePrev} disabled={activeSection === 0} className={`flex items-center gap-4 bg-stone-100 text-stone-800 px-8 py-4 rounded-xl font-black text-[10px] uppercase tracking-widest transition-all shadow-sm ${activeSection === 0 ? 'opacity-0 pointer-events-none' : ''}`}>
                  <ArrowLeft size={16} /> Prev
                </motion.button>
                <motion.button whileHover={{ scale: 1.05 }} whileTap={{ scale: 0.95 }} onClick={handleCompleteSection} className="group relative flex items-center gap-4 bg-stone-900 text-white px-12 py-6 rounded-2xl font-black text-[12px] uppercase tracking-widest hover:bg-pink-600 transition-all shadow-[0_20px_50px_rgba(0,0,0,0.2)] overflow-hidden">
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
