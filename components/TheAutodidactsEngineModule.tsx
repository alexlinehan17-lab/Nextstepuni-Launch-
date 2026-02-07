

/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
*/

import React, { useState } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { 
  ArrowLeft, CheckCircle2, ArrowRight, 
  Lock, Flag, SlidersHorizontal, Repeat, Brain, BookOpen, PenSquare, Wrench, Highlighter
} from 'lucide-react';

interface TheAutodidactsEngineModuleProps {
  onBack: () => void;
}

const Highlight = ({ children, description, color = "bg-cyan-100/40", textColor = "text-cyan-900", decorColor = "decoration-cyan-400/40", hoverColor="hover:bg-cyan-200/60" }: { children?: React.ReactNode, description: string, color?: string, textColor?: string, decorColor?: string, hoverColor?: string }) => {
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
              <p className="font-sans font-bold text-cyan-400 mb-2 uppercase tracking-[0.2em] text-[9px]">The Academic Insight</p>
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
        <div className="w-12 h-12 rounded-2xl bg-stone-900 flex items-center justify-center text-cyan-400 shadow-xl border border-white/10">
          <Icon size={24} />
        </div>
      </div>
      <span className="inline-flex items-center gap-2 px-3 py-1 bg-cyan-50 text-cyan-600 text-[10px] font-black tracking-[0.4em] uppercase rounded-full mb-4">
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
  <div className="my-12 p-8 bg-cyan-50/50 border-2 border-dashed border-cyan-200 rounded-3xl">
    <div className="flex items-start gap-5">
      <div className="w-11 h-11 rounded-xl bg-cyan-500 text-white flex items-center justify-center shrink-0 mt-1 shadow-lg shadow-cyan-500/20">
        <Flag size={20} />
      </div>
      <div>
        <h4 className="font-bold text-cyan-800 text-sm uppercase tracking-widest">Your Mission (Under 5 Mins)</h4>
        <div className="text-stone-600 mt-2 font-medium leading-relaxed">
          {children}
        </div>
      </div>
    </div>
  </div>
);

const ActivityRing = ({ progress, color = "#06b6d4" }: { progress: number, color?: string }) => {
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

const FourHighlighterAudit = () => {
    const [activeHighlighter, setActiveHighlighter] = useState<string | null>(null);

    const highlights: { [key: string]: string[] } = {
        purpose: ['s1', 's3', 's4'],
        coherence: ['t1', 't2', 't3'],
        language: ['w1', 'w2', 'w3', 'w4', 'w5', 'w6', 'w7', 'w8'],
        mechanics: ['e1']
    };

    const isHighlighted = (id: string) => activeHighlighter && highlights[activeHighlighter]?.includes(id);

    const textSpans = [
        { id: 's1', text: "W.B. Yeats' poem 'The Second Coming' powerfully captures the anxiety of a world descending into chaos. " },
        { id: 's2', text: "Initially, the poem presents the image of a falcon " },
        { id: 'e1', text: "loosing" },
        { id: 's2_cont', text: " control, a metaphor for society's breakdown. " },
        { id: 's3', text: "However, Yeats then introduces the terrifying 'rough beast,' slouching towards Bethlehem. This stark image solidifies the poem's apocalyptic vision. " },
        { id: 's4', text: "Therefore, the poem encapsulates a profound sense of cultural collapse." },
    ];
    
    const wordSpans = [
        { id: 'w1', text: 'powerfully captures' },
        { id: 'w2', text: 'descending into chaos' },
        { id: 'w3', text: 'losing control' },
        { id: 'w4', text: "terrifying 'rough beast,'" },
        { id: 'w5', text: 'slouching' },
        { id: 'w6', text: 'stark image' },
        { id: 'w7', text: 'apocalyptic vision' },
        { id: 'w8', text: 'encapsulates' },
    ];
    
    const transitionSpans = [
        { id: 't1', text: 'Initially' },
        { id: 't2', text: 'However' },
        { id: 't3', text: 'Therefore' },
    ]

    const textWithSpans = `
        <span class="${isHighlighted('s1') ? 'bg-blue-200' : ''}">W.B. Yeats' poem 'The Second Coming' <span class="${isHighlighted('w1') ? 'bg-yellow-200' : ''}">powerfully captures</span> the anxiety of a world <span class="${isHighlighted('w2') ? 'bg-yellow-200' : ''}">descending into chaos</span>.</span>
        <span class="${isHighlighted('s2') ? '' : ''}"><span class="${isHighlighted('t1') ? 'bg-green-200' : ''}">Initially</span>, the poem presents the image of a falcon <span class="${isHighlighted('e1') ? 'bg-red-300' : ''}">loosing</span> control, a metaphor for society's breakdown.</span>
        <span class="${isHighlighted('s3') ? 'bg-blue-200' : ''}"><span class="${isHighlighted('t2') ? 'bg-green-200' : ''}">However</span>, Yeats then introduces the <span class="${isHighlighted('w4') ? 'bg-yellow-200' : ''}">terrifying 'rough beast,'</span> <span class="${isHighlighted('w5') ? 'bg-yellow-200' : ''}">slouching</span> towards Bethlehem. This <span class="${isHighlighted('w6') ? 'bg-yellow-200' : ''}">stark image</span> solidifies the poem's <span class="${isHighlighted('w7') ? 'bg-yellow-200' : ''}">apocalyptic vision</span>.</span>
        <span class="${isHighlighted('s4') ? 'bg-blue-200' : ''}"><span class="${isHighlighted('t3') ? 'bg-green-200' : ''}">Therefore</span>, the poem <span class="${isHighlighted('w8') ? 'bg-yellow-200' : ''}">encapsulates</span> a profound sense of cultural collapse.</span>
    `.replace(/<span class="(bg-blue-200|bg-green-200|bg-yellow-200|bg-red-300)">/g, '<span class="$1 px-1 rounded-sm">');

    return (
        <div className="my-10 p-8 md:p-12 bg-white rounded-[3rem] border border-stone-200 shadow-xl">
            <h4 className="font-serif text-2xl font-bold text-stone-800 text-center italic">The Four-Highlighter Audit</h4>
            <p className="text-center text-sm text-stone-500 mb-6">Click the highlighters to audit the paragraph below.</p>
            <div className="flex justify-center flex-wrap gap-3 mb-6">
                <button onClick={() => setActiveHighlighter(activeHighlighter === 'purpose' ? null : 'purpose')} className={`px-4 py-2 flex items-center gap-2 text-sm font-bold rounded-lg border-2 ${activeHighlighter === 'purpose' ? 'bg-blue-500 text-white border-blue-500' : 'bg-blue-50 text-blue-800 border-blue-200'}`}> <Highlighter size={16}/> Purpose</button>
                <button onClick={() => setActiveHighlighter(activeHighlighter === 'coherence' ? null : 'coherence')} className={`px-4 py-2 flex items-center gap-2 text-sm font-bold rounded-lg border-2 ${activeHighlighter === 'coherence' ? 'bg-green-500 text-white border-green-500' : 'bg-green-50 text-green-800 border-green-200'}`}> <Highlighter size={16}/> Coherence</button>
                <button onClick={() => setActiveHighlighter(activeHighlighter === 'language' ? null : 'language')} className={`px-4 py-2 flex items-center gap-2 text-sm font-bold rounded-lg border-2 ${activeHighlighter === 'language' ? 'bg-yellow-400 text-yellow-900 border-yellow-500' : 'bg-yellow-50 text-yellow-800 border-yellow-200'}`}> <Highlighter size={16}/> Language</button>
                <button onClick={() => setActiveHighlighter(activeHighlighter === 'mechanics' ? null : 'mechanics')} className={`px-4 py-2 flex items-center gap-2 text-sm font-bold rounded-lg border-2 ${activeHighlighter === 'mechanics' ? 'bg-red-500 text-white border-red-500' : 'bg-red-50 text-red-800 border-red-200'}`}> <Highlighter size={16}/> Mechanics</button>
            </div>
            <div className="bg-stone-50 p-6 rounded-2xl border border-stone-200 leading-relaxed" dangerouslySetInnerHTML={{ __html: textWithSpans }} />
        </div>
    );
};


// --- MODULE COMPONENT ---
export const TheAutodidactsEngineModule: React.FC<{onBack: () => void}> = ({ onBack }) => {
  const [activeSection, setActiveSection] = useState(0);
  const [unlockedSection, setUnlockedSection] = useState(0);
  
  const sections = [
    { id: 'practice-hierarchy', title: 'The Practice Hierarchy', eyebrow: '01 // Not All Study Is Equal', icon: SlidersHorizontal },
    { id: 'feedback-engine', title: 'The Feedback Engine', eyebrow: '02 // The Rules of Autonomy', icon: Repeat },
    { id: 'maths-loop', title: 'The Maths Loop', eyebrow: '03 // Algorithmic Practice', icon: Brain },
    { id: 'language-loop', title: 'The Language Loop', eyebrow: '04 // Comparative Practice', icon: BookOpen },
    { id: 'writing-loop', title: 'The Writing Loop', eyebrow: '05 // Structural Practice', icon: PenSquare },
    { id: 'build-your-engine', title: 'Build Your Engine', eyebrow: '06 // The Action Plan', icon: Wrench },
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
            <p className="text-[9px] font-black text-cyan-500 uppercase tracking-[0.4em] mb-0.5 underline">Module 06</p>
            <h1 className="font-serif font-bold text-lg tracking-tight text-stone-900">Using Feedback Loops</h1>
          </div>
        </div>

        <div className="flex-grow space-y-4 overflow-y-auto no-scrollbar pr-2 relative">
          <div className="absolute left-[21px] top-6 bottom-6 w-0.5 bg-stone-100 -z-0" />
          <div className="absolute left-[21px] top-6 bottom-6 w-0.5">
              <motion.div
                  className="w-full bg-cyan-500 shadow-[0_0_10px_rgba(6,182,212,0.5)]"
                  initial={{ height: 0 }}
                  animate={{ height: sections.length > 1 ? `${(unlockedSection / (sections.length - 1)) * 100}%` : '0%' }}
              />
          </div>
          {sections.map((section, idx) => {
            const isUnlocked = idx <= unlockedSection;
            const isActive = idx === activeSection;
            const isCompleted = idx < unlockedSection;
            return (
              <button key={section.id} disabled={!isUnlocked} onClick={() => handleJumpToSection(idx)} className={`relative z-10 w-full flex items-center gap-4 p-3 rounded-xl transition-all duration-500 text-left group ${isActive ? 'bg-cyan-50 shadow-sm translate-x-2' : ''} ${!isUnlocked ? 'opacity-40 grayscale cursor-not-allowed' : 'hover:bg-stone-50'}`}>
                <div className={`w-11 h-11 rounded-xl flex items-center justify-center shrink-0 border-2 transition-all duration-500 ${isCompleted ? 'bg-cyan-600 border-cyan-600 text-white shadow-lg' : isActive ? 'bg-white border-cyan-500 text-cyan-600 shadow-xl rotate-12' : 'bg-white border-stone-200 text-stone-300'}`}>
                   {isCompleted ? <CheckCircle2 size={18} /> : isActive ? <section.icon size={18} /> : <Lock size={16} />}
                </div>
                <div className="flex-grow"><p className={`text-[8px] font-black uppercase tracking-widest ${isActive ? 'text-cyan-500' : 'text-stone-400'}`}>{section.eyebrow.split('// ')[1]}</p><h4 className={`text-xs font-bold leading-tight ${isActive ? 'text-stone-900' : 'text-stone-500'}`}>{section.title}</h4></div>
              </button>
            );
          })}
        </div>

        <div className="mt-8 border-t border-stone-100 pt-8 flex flex-col items-center">
           <ActivityRing progress={progress} color="#06b6d4" /><p className="text-[11px] font-black text-stone-900 uppercase tracking-widest text-center">Progress</p>
        </div>
      </aside>

      <main className="flex-grow flex flex-col items-center py-10 md:py-24 px-6 md:px-16 overflow-y-auto h-screen relative">
        <div className="absolute inset-0 bg-[radial-gradient(#e5e7eb_1px,transparent_1px)] [background-size:32px_32px] opacity-40 pointer-events-none" />
        <div className="w-full max-w-4xl relative z-10">
          <AnimatePresence mode="wait">
            <motion.div key={activeSection} initial={{ opacity: 0, x: 20 }} animate={{ opacity: 1, x: 0 }} exit={{ opacity: 0, x: -20 }} transition={{ duration: 0.6, ease: [0.16, 1, 0.3, 1] }}>
              {activeSection === 0 && (
                <ReadingSection title="Not All Study Is Equal." eyebrow="Step 1" icon={SlidersHorizontal}>
                  <p>Most study time is wasted. It's spent on what scientists call <Highlight description="Low-effort, repetitive practice without feedback. Examples include re-reading notes or highlighting a textbook. This kind of practice entrenches existing habits and does not lead to improvement.">Naive Practice</Highlight>—just going through the motions. This feels productive, but it doesn't build skill. To get better, you need to engage in <Highlight description="A highly structured activity designed specifically to improve performance. It requires a well-defined goal, full concentration, and, crucially, immediate and informative feedback.">Deliberate Practice</Highlight>.</p>
                  <p>The secret ingredient of Deliberate Practice is a high-quality feedback loop. A great teacher provides this automatically. But when you're studying alone, you're in a "feedback vacuum." The goal of this module is to teach you how to become your own teacher by building your own feedback engine.</p>
                </ReadingSection>
              )}
               {activeSection === 1 && (
                <ReadingSection title="The Rules of Autonomy." eyebrow="Step 2" icon={Repeat}>
                  <p>To build your own feedback loop, you need to obey two laws of your brain's hardware. First, the <Highlight description="The need to consciously focus on errors to strengthen the brain's learning signal (the Pe wave). This forces a Growth Mindset response through behaviour.">Law of Neural Amplification</Highlight>: You must force your brain to pay attention to errors. A Growth Mindset does this automatically by boosting your 'Pe' error signal. You must simulate this by using rigorous, unavoidable comparison against an expert model—what we'll call a "Teacher Proxy."</p>
                  <p>Second, the <Highlight description="The principle that your working memory is severely limited. You cannot be a performer and a critic at the same time without overloading your brain.">Law of Cognitive Load</Highlight>: Your working memory is tiny. You cannot be a high-level performer and a high-level critic *at the same time*. This <Highlight description="The cognitive strain that occurs when your limited working memory is forced to handle two competing tasks at once, degrading performance on both.">Split-Attention Effect</Highlight> is why trying to check your work as you go is so hard. The solution is an <Highlight description="A feedback process where the performance phase is completely separate from the feedback phase. This protects working memory and allows for deeper analysis.">Asynchronous Loop</Highlight>: separate your "Performance Phase" (doing the work) from your "Feedback Phase" (checking the work).</p>
                </ReadingSection>
              )}
               {activeSection === 2 && (
                <ReadingSection title="The Maths Loop." eyebrow="Step 3" icon={Brain}>
                  <p>In a subject like Maths, the "Teacher Proxy" is a full worked solution or marking scheme. The protocol is the <Highlight description="A technique where a student covers a worked solution, attempts only the first line, then uncovers the first line of the solution to compare. This creates a line-by-line feedback loop.">Split-Page Method</Highlight>. You cover the solution, attempt just one line of the problem, stop, then uncover the expert's first line. This creates a high-fidelity micro-feedback loop.</p>
                  <p>If your step matches, you continue. If it's a mismatch, the learning begins. You must perform <Highlight description="The act of explaining a concept or the logic of a step to yourself. This forces deeper processing and is one of the most effective ways to build robust understanding.">Self-Explanation</Highlight>—writing down in your own words why the expert's step was better than yours. This forces you to confront the gap in your understanding and manually amplifies the learning signal in your brain.</p>
                </ReadingSection>
              )}
              {activeSection === 3 && (
                <ReadingSection title="The Language Loop." eyebrow="Step 4" icon={BookOpen}>
                  <p>For language syntax and grammar, the "Teacher Proxy" is a native text. The protocol is <Highlight description="A powerful technique where you translate a text from your target language (L2) to your native language (L1), wait, and then translate it back to L2 without looking at the original to expose errors.">Back-Translation</Highlight>. You take a short native text (L2), translate it into your own language (L1), wait an hour, then translate your L1 version *back* into the L2 without looking at the original. Finally, you compare your new L2 version with the original, side-by-side.</p>
                  <p>This process is brutally effective at exposing <Highlight description="The tendency to impose the grammatical structures and idioms of your native language (L1) onto the foreign language you are learning (L2).">L1 Interference</Highlight>—the tendency to think in English while writing in Irish or French. Every difference between your version and the native text is a high-quality feedback point, revealing exactly where your internal model of the language is wrong.</p>
                </ReadingSection>
              )}
              {activeSection === 4 && (
                <ReadingSection title="The Writing Loop." eyebrow="Step 5" icon={PenSquare}>
                    <p>For subjective skills like essay writing, the "Teacher Proxy" is a high-quality model essay and the official marking scheme (the PCLM criteria). The protocol is the <Highlight description="A self-correction protocol where you visually audit your own essay using four different colored highlighters, one for each of the PCLM criteria.">Four-Highlighter Method</Highlight>. After writing an essay, you make four passes, each with a different color, auditing your work against the examiner's criteria.</p>
                    <p>
                        You use one color for <Highlight description="The relevance of your writing. Does every sentence directly address the question asked?" color="bg-blue-100/40" textColor="text-blue-900" decorColor="decoration-blue-400/40" hoverColor="hover:bg-blue-200/60">Purpose</Highlight> (sentences that directly answer the question), one for <Highlight description="The flow and structure of your argument. Do your ideas connect logically from one to the next?" color="bg-green-100/40" textColor="text-green-900" decorColor="decoration-green-400/40" hoverColor="hover:bg-green-200/60">Coherence</Highlight> (transition words and topic sentences), one for <Highlight description="The quality and precision of your word choice. Are you using strong verbs and specific terminology?" color="bg-yellow-100/40" textColor="text-yellow-900" decorColor="decoration-yellow-400/40" hoverColor="hover:bg-yellow-200/60">Language</Highlight> (strong verbs and terminology), and one for <Highlight description="The technical correctness of your writing, including spelling, punctuation, and grammar." color="bg-red-100/40" textColor="text-red-900" decorColor="decoration-red-400/40" hoverColor="hover:bg-red-200/60">Mechanics</Highlight> (spelling/grammar errors). This transforms a vague sense of "Is my essay good?" into a clear, visual dashboard of your strengths and weaknesses.
                    </p>
                    <FourHighlighterAudit />
                </ReadingSection>
              )}
              {activeSection === 5 && (
                <ReadingSection title="Build Your Engine." eyebrow="Step 6" icon={Wrench}>
                  <p>You now have the blueprints for a high-performance feedback engine. You have the protocols to transform passive, naive practice into active, deliberate practice. You have the tools to become an autodidact—a self-teaching, self-regulating learner.</p>
                  <p>The final step is to choose a single protocol and commit to trying it just once in the next week. This isn't about overhauling your entire study routine overnight. It's about taking one small, strategic step to upgrade your learning process. Select your mission below to build your engine.</p>
                  <MicroCommitment>
                    <p>Choose one subject you want to improve. This week, instead of just "studying," schedule 30 minutes to run one of these feedback loop protocols. You are moving from being a student to being a scientist of your own learning.</p>
                  </MicroCommitment>
                </ReadingSection>
              )}
              <footer className="mt-24 flex items-center justify-between pt-12 border-t border-stone-200/60 px-4">
                <motion.button whileHover={{ scale: 1.05 }} whileTap={{ scale: 0.95 }} onClick={handlePrev} disabled={activeSection === 0} className={`flex items-center gap-4 bg-stone-100 text-stone-800 px-8 py-4 rounded-xl font-black text-[10px] uppercase tracking-widest transition-all shadow-sm ${activeSection === 0 ? 'opacity-0 pointer-events-none' : ''}`}>
                  <ArrowLeft size={16} /> Prev
                </motion.button>
                <motion.button whileHover={{ scale: 1.05 }} whileTap={{ scale: 0.95 }} onClick={handleCompleteSection} className="group relative flex items-center gap-4 bg-stone-900 text-white px-12 py-6 rounded-2xl font-black text-[12px] uppercase tracking-widest hover:bg-cyan-600 transition-all shadow-[0_20px_50px_rgba(0,0,0,0.2)] overflow-hidden">
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
