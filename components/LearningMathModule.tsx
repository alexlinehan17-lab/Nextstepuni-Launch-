
/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
*/

import React, { useState } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { 
  ArrowLeft, CheckCircle2, ArrowRight, 
  Lock, Flag, Target, Brain, SlidersHorizontal, AlertTriangle, PenTool, Key, BookOpen, Wrench
} from 'lucide-react';

interface LearningMathModuleProps {
  onBack: () => void;
}

const Highlight = ({ children, description, color = "bg-gray-100/40", textColor = "text-gray-900", decorColor = "decoration-gray-400/40", hoverColor="hover:bg-gray-200/60" }: { children?: React.ReactNode, description: string, color?: string, textColor?: string, decorColor?: string, hoverColor?: string }) => {
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
              <p className="font-sans font-bold text-gray-400 mb-2 uppercase tracking-[0.2em] text-[9px]">The Academic Insight</p>
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
        <div className="w-12 h-12 rounded-2xl bg-stone-900 flex items-center justify-center text-gray-400 shadow-xl border border-white/10">
          <Icon size={24} />
        </div>
      </div>
      <span className="inline-flex items-center gap-2 px-3 py-1 bg-gray-50 text-gray-600 text-[10px] font-black tracking-[0.4em] uppercase rounded-full mb-4">
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
  <div className="my-12 p-8 bg-gray-50/50 border-2 border-dashed border-gray-200 rounded-3xl">
    <div className="flex items-start gap-5">
      <div className="w-11 h-11 rounded-xl bg-gray-500 text-white flex items-center justify-center shrink-0 mt-1 shadow-lg shadow-gray-500/20">
        <Flag size={20} />
      </div>
      <div>
        <h4 className="font-bold text-gray-800 text-sm uppercase tracking-widest">Your Mission (Under 5 Mins)</h4>
        <div className="text-stone-600 mt-2 font-medium leading-relaxed">
          {children}
        </div>
      </div>
    </div>
  </div>
);

const ActivityRing = ({ progress, color = "#4b5563" }: { progress: number, color?: string }) => {
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
const PartialCreditCalculator = () => {
    const [steps, setSteps] = useState({ formula: false, sub: false, slip: false, blunder: false });

    let marks = 0;
    if(steps.blunder) marks = 3;
    else if(steps.formula && steps.sub && steps.slip) marks = 8;
    else if(steps.formula && steps.sub) marks = 10;
    else if(steps.formula) marks = 5;

    return (
        <div className="my-10 p-8 md:p-12 bg-white rounded-[3rem] border border-stone-200 shadow-xl">
             <h4 className="font-serif text-2xl font-bold text-stone-800 text-center italic">Partial Credit Calculator</h4>
             <p className="text-center text-sm text-stone-500 mb-8">Scenario: 10-mark Scale D Question. How many marks do you get?</p>
             <div className="grid grid-cols-2 gap-3">
                <button onClick={() => setSteps(s => ({...s, formula: !s.formula}))} className={`p-4 rounded-xl border-2 ${steps.formula ? 'bg-emerald-50' : ''}`}>Wrote correct formula</button>
                <button onClick={() => setSteps(s => ({...s, sub: !s.sub}))} className={`p-4 rounded-xl border-2 ${steps.sub ? 'bg-emerald-50' : ''}`}>Substituted a value</button>
                <button onClick={() => setSteps(s => ({...s, slip: !s.slip, blunder: false}))} className={`p-4 rounded-xl border-2 ${steps.slip ? 'bg-amber-50' : ''}`}>Made a minor calculation 'Slip'</button>
                <button onClick={() => setSteps(s => ({...s, blunder: !s.blunder, slip: false}))} className={`p-4 rounded-xl border-2 ${steps.blunder ? 'bg-rose-50' : ''}`}>Made a major concept 'Blunder'</button>
             </div>
             <div className="mt-8 p-4 bg-stone-900 rounded-xl text-center text-white">
                You get <span className="font-bold text-2xl text-gray-400">{marks}/10</span> marks.
            </div>
        </div>
    );
};

const ProblemSorter = () => {
    const problems = [
        {id: 1, text: "How many ways can 5 books be arranged?", type: 'p'},
        {id: 2, text: "How many teams of 5 can be picked from 10 players?", type: 'c'}
    ];
    const [choice, setChoice] = useState<{[key: number]: string | null}>({});

    const handleChoice = (id: number, c: string) => {
        setChoice(prev => ({...prev, [id]: c}));
    };

    return(
        <div className="my-10 p-8 md:p-12 bg-white rounded-[3rem] border border-stone-200 shadow-xl">
            <h4 className="font-serif text-2xl font-bold text-stone-800 text-center italic">Problem Sorter</h4>
            <p className="text-center text-sm text-stone-500 mb-8">Train your discriminative skills: Is it a Permutation (order matters) or a Combination (order doesn't)?</p>
            {problems.map(p => (
                <div key={p.id} className="mb-4">
                    <p className="p-4 bg-stone-100 rounded-lg text-center font-bold">{p.text}</p>
                    <div className="grid grid-cols-2 gap-2 mt-2">
                        <button onClick={() => handleChoice(p.id, 'p')} className={`p-2 rounded-lg border-2 ${choice[p.id] && (choice[p.id] === 'p' && p.type === 'p' ? 'bg-emerald-100 border-emerald-300' : choice[p.id] === 'p' ? 'bg-rose-100 border-rose-300' : 'bg-stone-100 border-stone-200')}`}>Permutation</button>
                        <button onClick={() => handleChoice(p.id, 'c')} className={`p-2 rounded-lg border-2 ${choice[p.id] && (choice[p.id] === 'c' && p.type === 'c' ? 'bg-emerald-100 border-emerald-300' : choice[p.id] === 'c' ? 'bg-rose-100 border-rose-300' : 'bg-stone-100 border-stone-200')}`}>Combination</button>
                    </div>
                </div>
            ))}
        </div>
    );
}

const ErrorLog = () => {
    const [error, setError] = useState('');
    const [type, setType] = useState<string | null>(null);

    return(
         <div className="my-10 p-8 md:p-12 bg-white rounded-[3rem] border border-stone-200 shadow-xl">
             <h4 className="font-serif text-2xl font-bold text-stone-800 text-center italic">My Error Log</h4>
             <p className="text-center text-sm text-stone-500 mb-8">Log a mistake from a practice question to turn it into a learning opportunity.</p>
             <div className="space-y-4">
                <textarea value={error} onChange={e => setError(e.target.value)} placeholder="Describe the mistake..." className="w-full h-24 p-4 bg-stone-50 border-2 rounded-xl focus:outline-none focus:border-gray-400"></textarea>
                <div className="grid grid-cols-3 gap-2">
                    <button onClick={() => setType('Concept')} className={`p-2 text-xs rounded-lg border-2 ${type === 'Concept' ? 'bg-gray-800 text-white' : 'bg-stone-100'}`}>Concept Error</button>
                    <button onClick={() => setType('Procedural')} className={`p-2 text-xs rounded-lg border-2 ${type === 'Procedural' ? 'bg-gray-800 text-white' : 'bg-stone-100'}`}>Procedural Error</button>
                    <button onClick={() => setType('Reading')} className={`p-2 text-xs rounded-lg border-2 ${type === 'Reading' ? 'bg-gray-800 text-white' : 'bg-stone-100'}`}>Reading Error</button>
                </div>
             </div>
             {error && type && <p className="text-center mt-4 text-sm font-bold text-emerald-600">Error logged. Now you won't make it again.</p>}
        </div>
    );
};


// --- MODULE COMPONENT ---
export const LearningMathModule: React.FC<{onBack: () => void}> = ({ onBack }) => {
  const [activeSection, setActiveSection] = useState(0);
  const [unlockedSection, setUnlockedSection] = useState(0);
  
  const sections = [
    { id: 'new-game', title: 'The New Game', eyebrow: '01 // Project Maths', icon: Target },
    { id: 'two-papers', title: 'The Two Papers', eyebrow: '02 // Technical vs. Contextual', icon: BookOpen },
    { id: 'deep-dive', title: 'The Five Strands', eyebrow: '03 // Curriculum Deep Dive', icon: SlidersHorizontal },
    { id: 'marking-scheme', title: 'Decoding the Scheme', eyebrow: '04 // Positive Marking', icon: Key },
    { id: 'attempt-mark', title: 'The "Attempt Mark" Goldmine', eyebrow: '05 // Partial Credit', icon: Wrench },
    { id: 'spotting-trends', title: 'Spotting the Trends', eyebrow: '06 // Gremlins & Hybrids', icon: Brain },
    { id: 'examiners-mind', title: 'The Examiner\'s Mind', eyebrow: '07 // Common Errors', icon: AlertTriangle },
    { id: 'cognitive-toolkit', title: 'The Cognitive Toolkit', eyebrow: '08 // Learning Science for Maths', icon: Brain },
    { id: 'h1-pathway', title: 'The H1 Pathway', eyebrow: '09 // Bankable Marks', icon: PenTool },
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
            <p className="text-[9px] font-black text-gray-500 uppercase tracking-[0.4em] mb-0.5 underline">Module 01</p>
            <h1 className="font-serif font-bold text-lg tracking-tight text-stone-900">The Maths Protocol</h1>
          </div>
        </div>

        <div className="flex-grow space-y-4 overflow-y-auto no-scrollbar pr-2 relative">
          <div className="absolute left-[21px] top-6 bottom-6 w-0.5 bg-stone-100 -z-0" />
          <div className="absolute left-[21px] top-6 bottom-6 w-0.5">
              <motion.div
                  className="w-full bg-gray-500 shadow-[0_0_10px_rgba(75,85,99,0.5)]"
                  initial={{ height: 0 }}
                  animate={{ height: sections.length > 1 ? `${(unlockedSection / (sections.length - 1)) * 100}%` : '0%' }}
              />
          </div>
          {sections.map((section, idx) => {
            const isUnlocked = idx <= unlockedSection;
            const isActive = idx === activeSection;
            const isCompleted = idx < unlockedSection;
            return (
              <button key={section.id} disabled={!isUnlocked} onClick={() => handleJumpToSection(idx)} className={`relative z-10 w-full flex items-center gap-4 p-3 rounded-xl transition-all duration-500 text-left group ${isActive ? 'bg-gray-50 shadow-sm translate-x-2' : ''} ${!isUnlocked ? 'opacity-40 grayscale cursor-not-allowed' : 'hover:bg-stone-50'}`}>
                <div className={`w-11 h-11 rounded-xl flex items-center justify-center shrink-0 border-2 transition-all duration-500 ${isCompleted ? 'bg-gray-600 border-gray-600 text-white shadow-lg' : isActive ? 'bg-white border-gray-500 text-gray-600 shadow-xl rotate-12' : 'bg-white border-stone-200 text-stone-300'}`}>
                   {isCompleted ? <CheckCircle2 size={18} /> : isActive ? <section.icon size={18} /> : <Lock size={16} />}
                </div>
                <div className="flex-grow"><p className={`text-[8px] font-black uppercase tracking-widest ${isActive ? 'text-gray-500' : 'text-stone-400'}`}>{section.eyebrow.split('// ')[1]}</p><h4 className={`text-xs font-bold leading-tight ${isActive ? 'text-stone-900' : 'text-stone-500'}`}>{section.title}</h4></div>
              </button>
            );
          })}
        </div>
        <div className="mt-8 border-t border-stone-100 pt-8 flex flex-col items-center">
           <ActivityRing progress={progress} color="#4b5563" /><p className="text-[11px] font-black text-stone-900 uppercase tracking-widest text-center">Progress</p>
        </div>
      </aside>

      <main className="flex-grow flex flex-col items-center py-10 md:py-24 px-6 md:px-16 overflow-y-auto h-screen relative">
        <div className="absolute inset-0 bg-[radial-gradient(#e5e7eb_1px,transparent_1px)] [background-size:32px_32px] opacity-40 pointer-events-none" />
        <div className="w-full max-w-4xl relative z-10">
          <AnimatePresence mode="wait">
            <motion.div key={activeSection} initial={{ opacity: 0, x: 20 }} animate={{ opacity: 1, x: 0 }} exit={{ opacity: 0, x: -20 }} transition={{ duration: 0.6, ease: [0.16, 1, 0.3, 1] }}>
              {activeSection === 0 && (
                <ReadingSection title="The New Game." eyebrow="Step 1" icon={Target}>
                  <p>Leaving Cert Maths is not the same game it used to be. The "Project Maths" initiative fundamentally changed the rules, shifting the focus from rote memorization of algorithms to genuine <Highlight description="The ability to understand the 'why' behind a mathematical rule, not just the 'how'.">conceptual understanding</Highlight> and problem-solving. It's a test of resilience, not just numeracy.</p>
                  <p>The introduction of the <Highlight description="The 25 extra CAO points awarded for a H6 or higher, making Maths the single most valuable subject in the points race.">Bonus Points</Highlight> has also changed the strategic landscape. A H6 in Maths is worth more than a H3 in any other subject. This "safety net" encourages students to aim high, but requires a deep, strategic approach to the exam.</p>
                </ReadingSection>
              )}
               {activeSection === 1 && (
                <ReadingSection title="The Two Papers." eyebrow="Step 2" icon={BookOpen}>
                  <p>The exam is split into two papers designed to test different cognitive skills. **Paper 1** is the **"Technical"** paper. It's heavily weighted towards Algebra, Calculus, and Number. It rewards <Highlight description="The ability to perform mathematical operations (like solving equations or differentiating) quickly and accurately.">procedural fluency</Highlight> and is less "wordy."</p>
                  <p>**Paper 2** is the **"Contextual"** paper. This is the test of interpretation and spatial reasoning, covering Statistics, Probability, Geometry, and Trigonometry. It's often described as "volatile" because a single novel diagram can throw off students who rely on memorized procedures rather than a deep understanding of the concepts.</p>
                </ReadingSection>
              )}
              {activeSection === 2 && (
                <ReadingSection title="The Five Strands." eyebrow="Step 3" icon={SlidersHorizontal}>
                  <p>The syllabus is divided into five interconnected strands. Questions are deliberately <Highlight description="Requiring students to combine knowledge from multiple strands (e.g., using Algebra to solve a Geometry problem).">synoptic</Highlight>, so you can't study topics in isolation.</p>
                  <p>The strands are: 1) **Statistics & Probability** (literacy-heavy), 2) **Geometry & Trigonometry** (visual and spatial), 3) **Number** (the foundation, including Complex Numbers), 4) **Algebra** (the "language" of the course), and 5) **Functions & Calculus** (the heavyweight of Paper 1).</p>
                </ReadingSection>
              )}
              {activeSection === 3 && (
                <ReadingSection title="Decoding the Marking Scheme." eyebrow="Step 4" icon={Key}>
                  <p>Understanding how marks are awarded is your single greatest strategic asset. The SEC uses a <Highlight description="An ethos where marks are awarded for what is correct, not deducted for what is wrong. The goal is to reward any valid progress.">"Positive Marking"</Highlight> system. This is codified in the Scale System (A, B, C, D).</p>
                  <p>**Scale A** (0, 10) is rare. **Scale B** (0, 5, 10) is "hit or miss." But **Scale C** (0, 3, 7, 10) and **Scale D** (0, 3, 5, 8, 10) are the most common. The crucial insight is the "Low Partial" mark—you can get 30% of the marks for simply writing down the correct formula and attempting to substitute a value. This is a strategic goldmine.</p>
                </ReadingSection>
              )}
              {activeSection === 4 && (
                <ReadingSection title="The 'Attempt Mark' Goldmine." eyebrow="Step 5" icon={Wrench}>
                  <p>The "Low Partial Credit" is your safety net. If you encounter a 10-mark question that seems impossible, simply writing down the relevant formula from the log tables and substituting one correct value often secures 3 marks. Leaving a question blank is a strategic failure of the highest order.</p>
                  <p>Accumulating these "scrap" marks across an entire paper can be the difference between a H4 and a H3. The goal is to *never get a zero*. Even on the hardest "gremlin" question, there are marks available for defining terms, writing a relevant formula, or drawing a diagram. You must train yourself to hunt for these partial marks.</p>
                  <PartialCreditCalculator />
                </ReadingSection>
              )}
              {activeSection === 5 && (
                <ReadingSection title="Spotting the Trends." eyebrow="Step 6" icon={Brain}>
                  <p>Analysis of past papers reveals clear trends. Paper 1 is seeing the rise of applied Calculus (rates of change) and Complex Numbers treated as geometry. Paper 2 is increasingly defined by its <Highlight description="Novel questions with unfamiliar diagrams or scenarios that test a student's ability to apply core principles to new situations.">"Gremlin" questions</Highlight> and <Highlight description="Questions that fuse topics from different strands, such as calculating the probability that a point lies within a certain geometric region.">Probability-Geometry hybrids</Highlight>. These questions are designed to defeat rote learning and reward flexible, conceptual understanding.</p>
                </ReadingSection>
              )}
              {activeSection === 6 && (
                <ReadingSection title="The Examiner's Mind." eyebrow="Step 7" icon={AlertTriangle}>
                  <p>The Chief Examiner's Reports highlight the most common student errors. The biggest is <Highlight description="The tendency for students to understand a concept but fail in the algebraic execution (e.g., mishandling signs, index errors).">"Algebraic Fragility."</Highlight> The second is the <Highlight description="The failure to check answers for reasonableness (e.g., calculating a probability greater than 1, or a negative distance).">"Check" Deficit</Highlight>. The third is the <Highlight description="The struggle to translate a 'real-world' story problem into a mathematical model, often due to over-reliance on blocked practice.">"Unfamiliar Context" Block</Highlight>.</p>
                  <p>A major pitfall is "forcing" an answer in "Show That" questions. It is strategically better to write, "I cannot derive the final step, but assuming x=5, I will proceed..." This allows you to gain partial credit on subsequent parts.</p>
                  <ProblemSorter />
                </ReadingSection>
              )}
              {activeSection === 7 && (
                <ReadingSection title="The Cognitive Toolkit." eyebrow="Step 8" icon={Brain}>
                  <p>To overcome these challenges, you must adopt strategies from cognitive science. <Highlight description="Studying one topic intensely (e.g., Algebra all week). It creates a false sense of mastery.">Blocking</Highlight> fails to train strategy selection. <Highlight description="Mixing up topics within a study session (e.g., one Algebra, one Geometry, one Probability). It feels harder but builds flexible, exam-ready knowledge.">Interleaving</Highlight> is crucial for Maths as it mimics the exam environment.</p>
                  <p>Passive reading of notes is ineffective. <Highlight description="Closing the book and attempting to write out a proof or definition from memory. This strengthens the neural pathways.">Active Recall</Highlight> is essential. Finally, you must maintain an <Highlight description="A log where you categorize your mistakes (Concept, Procedural, Reading) to prevent repetition and target revision.">Error Log</Highlight>. The most valuable part of a past paper is the "post-mortem."</p>
                  <ErrorLog />
                </ReadingSection>
              )}
              {activeSection === 8 && (
                <ReadingSection title="The H1 Pathway." eyebrow="Step 9" icon={PenTool}>
                  <p>For students aiming for the top grade, the strategy goes beyond competence. It requires speed and tactical awareness. H1 students distinguish themselves by their fluency, completing routine Section A questions faster to "bank" time for the harder Section B questions.</p>
                  <p>The final layer of strategy is to identify and master the few things in Maths that *can* be rote-learned. These are your <Highlight description="The small number of examinable proofs (e.g., Induction, irrationality of √2) and definitions (e.g., 'injective function'). These should be learned perfectly as they are 'free marks' when they appear.">"Bankable Marks."</Highlight> A small number of formal proofs and definitions are examinable. These should be learned perfectly and are 'free marks' if they appear on the day.</p>
                  <MicroCommitment><p>Go to your log tables. Pick one proof (e.g., Cos(A+B)). Spend 15 minutes learning it using active recall. You've just 'banked' a potential 10 marks.</p></MicroCommitment>
                </ReadingSection>
              )}
              <footer className="mt-24 flex items-center justify-between pt-12 border-t border-stone-200/60 px-4">
                <motion.button whileHover={{ scale: 1.05 }} whileTap={{ scale: 0.95 }} onClick={handlePrev} disabled={activeSection === 0} className={`flex items-center gap-4 bg-stone-100 text-stone-800 px-8 py-4 rounded-xl font-black text-[10px] uppercase tracking-widest transition-all shadow-sm ${activeSection === 0 ? 'opacity-0 pointer-events-none' : ''}`}>
                  <ArrowLeft size={16} /> Prev
                </motion.button>
                <motion.button whileHover={{ scale: 1.05 }} whileTap={{ scale: 0.95 }} onClick={handleCompleteSection} className="group relative flex items-center gap-4 bg-stone-900 text-white px-12 py-6 rounded-2xl font-black text-[12px] uppercase tracking-widest hover:bg-gray-600 transition-all shadow-[0_20px_50px_rgba(0,0,0,0.2)] overflow-hidden">
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
