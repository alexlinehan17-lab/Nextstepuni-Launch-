/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
*/

import React, { useState } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { 
  ArrowLeft, CheckCircle2, ArrowRight, 
  Lock, Flag, BookOpen, PenSquare, MessageSquare, BarChart, BrainCircuit, Mic, Settings
} from 'lucide-react';

interface MasteringEnglishModuleProps {
  onBack: () => void;
}

const Highlight = ({ children, description, color = "bg-blue-100/40", textColor = "text-blue-900", decorColor = "decoration-blue-400/40", hoverColor="hover:bg-blue-200/60" }: { children?: React.ReactNode, description: string, color?: string, textColor?: string, decorColor?: string, hoverColor?: string }) => {
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

// --- INTERACTIVE COMPONENTS ---
const PCLMGrader = () => {
    const [pclm, setPclm] = useState({ p: 50, c: 50, l: 50, m: 50 });
    
    // P caps C and L
    const cappedC = Math.min(pclm.c, pclm.p);
    const cappedL = Math.min(pclm.l, pclm.p);

    const total = (pclm.p * 0.3) + (cappedC * 0.3) + (cappedL * 0.3) + (pclm.m * 0.1);
    const grade = total >= 90 ? 'H1' : total >= 80 ? 'H2' : total >= 70 ? 'H3' : 'H4';

    return (
        <div className="my-10 p-8 md:p-12 bg-white rounded-[3rem] border border-stone-200 shadow-xl">
            <h4 className="font-serif text-2xl font-bold text-stone-800 text-center italic">PCLM Grader</h4>
            <div className="grid grid-cols-2 gap-6 items-center">
                <div className="space-y-2">
                    <input type="range" value={pclm.p} onChange={e => setPclm({...pclm, p: parseInt(e.target.value)})} className="w-full"/>
                    <input type="range" value={pclm.c} onChange={e => setPclm({...pclm, c: parseInt(e.target.value)})} className="w-full"/>
                    <input type="range" value={pclm.l} onChange={e => setPclm({...pclm, l: parseInt(e.target.value)})} className="w-full"/>
                    <input type="range" value={pclm.m} onChange={e => setPclm({...pclm, m: parseInt(e.target.value)})} className="w-full"/>
                </div>
                <div className="text-center">
                    <p className="text-6xl font-black text-blue-500">{grade}</p>
                </div>
            </div>
        </div>
    );
};


// --- MODULE COMPONENT ---
export const MasteringEnglishModule: React.FC<{onBack: () => void}> = ({ onBack }) => {
  const [activeSection, setActiveSection] = useState(0);
  const [unlockedSection, setUnlockedSection] = useState(0);
  
  const sections = [
    { id: 'pclm-blueprint', title: 'The PCLM Blueprint', eyebrow: '01 // The Marking Scheme', icon: Settings },
    { id: 'paper1-engine', title: 'Paper 1: The Engine of Grades', eyebrow: '02 // Language & Comprehension', icon: BookOpen },
    { id: 'composing', title: 'Paper 1: The 100-Mark Essay', eyebrow: '03 // Composing', icon: PenSquare },
    { id: 'single-text', title: 'Paper 2: The Single Text', eyebrow: '04 // Macbeth 2026', icon: MessageSquare },
    { id: 'comparative-study', title: 'Paper 2: The Comparative Study', eyebrow: '05 // The Modes', icon: BarChart },
    { id: 'poetry', title: 'Paper 2: Prescribed Poetry', eyebrow: '06 // The "Big 4" Rule', icon: Mic },
    { id: 'toolkit', title: 'The Strategic Toolkit', eyebrow: '07 // High-Yield Strategies', icon: BrainCircuit },
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
            <p className="text-[9px] font-black text-blue-500 uppercase tracking-[0.4em] mb-0.5 underline">Module 04</p>
            <h1 className="font-serif font-bold text-lg tracking-tight text-stone-900">Mastering English</h1>
          </div>
        </div>

        <div className="flex-grow space-y-4 overflow-y-auto no-scrollbar pr-2 relative">
          <div className="absolute left-[21px] top-6 bottom-6 w-0.5 bg-stone-100 -z-0" />
          <div className="absolute left-[21px] top-6 bottom-6 w-0.5">
              <motion.div
                  className="w-full bg-blue-500 shadow-[0_0_10px_rgba(59,130,246,0.5)]"
                  initial={{ height: 0 }}
                  animate={{ height: sections.length > 1 ? `${(unlockedSection / (sections.length - 1)) * 100}%` : '0%' }}
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
           <ActivityRing progress={progress} /><p className="text-[11px] font-black text-stone-900 uppercase tracking-widest text-center">Progress</p>
        </div>
      </aside>

      <main className="flex-grow flex flex-col items-center py-10 md:py-24 px-6 md:px-16 overflow-y-auto h-screen relative">
        <div className="absolute inset-0 bg-[radial-gradient(#e5e7eb_1px,transparent_1px)] [background-size:32px_32px] opacity-40 pointer-events-none" />
        <div className="w-full max-w-4xl relative z-10">
          <AnimatePresence mode="wait">
            <motion.div key={activeSection} initial={{ opacity: 0, x: 20 }} animate={{ opacity: 1, x: 0 }} exit={{ opacity: 0, x: -20 }} transition={{ duration: 0.6, ease: [0.16, 1, 0.3, 1] }}>
              {activeSection === 0 && (
                <ReadingSection title="The PCLM Blueprint." eyebrow="Step 1" icon={Settings}>
                  <p>The Leaving Cert English exam is not subjective. It is governed by a strict, unified marking scheme: <Highlight description="The four criteria for marking English: Purpose (30%), Coherence (30%), Language (30%), and Mechanics (10%).">PCLM</Highlight>. Understanding this blueprint is the single most significant differentiator between a H3 and a H1.</p>
                  <p><Highlight description="Did you answer the specific question asked? This is the most important criterion.">Purpose</Highlight> is king. A brilliant essay that is irrelevant is worthless. Crucially, your marks for Coherence and Language are *capped* by your Purpose mark. You must prioritize relevance above all else.</p>
                </ReadingSection>
              )}
              {activeSection === 1 && (
                <ReadingSection title="Paper 1: Engine of Grades." eyebrow="Step 2" icon={BookOpen}>
                  <p>Paper 1 is 50% of your total grade and the most reliable place to secure marks. Question A tests comprehension and analysis. The 20-mark "Style/Technique" question is where the H1 is won or lost. You must go beyond listing techniques and explain their *effect* on the reader.</p>
                  <p>Question B, the Functional Writing task, is a "hidden trap." You must adhere strictly to the conventions of the requested genre (e.g., letter, blog post). Writing a personal essay in the wrong format is a fatal error for your 'P' mark.</p>
                </ReadingSection>
              )}
               {activeSection === 2 && (
                <ReadingSection title="The 100-Mark Essay." eyebrow="Step 3" icon={PenSquare}>
                  <p>The Composing section is worth 25% of your total grade. The Personal Essay is the most popular but most poorly executed. It is not just a story; it must be a <Highlight description="An exploration of how an event felt, what was learned, and how the writer changed as a result.">reflective piece</Highlight>. "Show, don't tell" is the golden rule.</p>
                  <p>The Short Story is high-risk, high-reward. Focus on a single incident and a short timeframe. The Discursive Essay requires a balanced exploration of an issue, while the Persuasive Essay demands a firm stance and the use of rhetorical devices.</p>
                </ReadingSection>
              )}
              {activeSection === 3 && (
                <ReadingSection title="Paper 2: Single Text (Macbeth)." eyebrow="Step 4" icon={MessageSquare}>
                   <p>For 2026, the prescribed Shakespearean text is Macbeth. A H1 analysis requires you to discuss the interconnectedness of themes, character, and imagery. The core themes are: <Highlight description="It's not just about wanting power; it's about the moral cost of that want.">Ambition and its Corrupting Influence</Highlight>, Kingship vs. Tyranny, The Supernatural and Fate, and Appearance vs. Reality.</p>
                   <p>Character analysis should focus on trajectories. Macbeth devolves from "brave Macbeth" to a nihilistic "butcher." Lady Macbeth follows a reverse trajectory, from ruthless resolve to collapse under the weight of repressed guilt.</p>
                </ReadingSection>
              )}
               {activeSection === 4 && (
                <ReadingSection title="The Comparative Study." eyebrow="Step 5" icon={BarChart}>
                    <p>For Higher Level 2026, the three comparative modes are **Cultural Context**, **General Vision and Viewpoint (GVV)**, and **Literary Genre**. Crucially, "Theme or Issue" is NOT a mode for Higher Level. Preparing it is a catastrophic waste of time.</p>
                    <p>The key to a H1 is a link-heavy structure. Avoid discussing your texts sequentially. Instead, weave them together in each paragraph, comparing and contrasting them based on the mode. The <Highlight description="A study technique where you identify 4-5 key moments in each text that can be flexibly applied to any of the comparative modes.">"Key Moment" Matrix</Highlight> is the most effective way to prepare for this.</p>
                </ReadingSection>
              )}
               {activeSection === 5 && (
                <ReadingSection title="Prescribed Poetry." eyebrow="Step 6" icon={Mic}>
                  <p>The <Highlight description="The mathematical reality that to guarantee one of your studied poets appears on the paper (where 4 out of 8 are examined), you must study 5 poets thoroughly.">"Big 4+1" Rule</Highlight> is non-negotiable. To guarantee a poet you've studied appears, you must master five poets. H1 answers must balance a discussion of the poet's themes (substance) with an analysis of their style (how they say it).</p>
                </ReadingSection>
              )}
               {activeSection === 6 && (
                <ReadingSection title="The Strategic Toolkit." eyebrow="Step 7" icon={BrainCircuit}>
                  <p>High-yield strategies can transform your performance. Use the <Highlight description="A time-saving technique where you read the questions first, assign a color to each, and then highlight relevant quotes as you read the text.">'Index Margining'</Highlight> technique for Paper 1 Comprehension. Prioritize <Highlight description="Short phrases (3-5 words) that fit grammatically into your own sentences, which are far superior to long, clunky block quotes.">Embedded Quotes</Highlight> over long block quotes. And above all, adhere to a strict time management protocol for both papers.</p>
                   <MicroCommitment>
                    <p>For your next practice essay, perform a PCLM audit. Go through with four different highlighters and mark where you have demonstrated Purpose, Coherence, Language, and good Mechanics. This will reveal your weaknesses.</p>
                  </MicroCommitment>
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
