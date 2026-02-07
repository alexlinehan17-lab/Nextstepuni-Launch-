
/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
*/

import React, { useState } from 'react';
import { motion, AnimatePresence, Reorder } from 'framer-motion';
import { 
  ArrowLeft, CheckCircle2, ArrowRight, 
  Lock, Flag, Target, Brain, Languages, Mic, Headphones, BookOpen, PenSquare, Wrench
} from 'lucide-react';

interface LanguageMasteryModuleProps {
  onBack: () => void;
}

const Highlight = ({ children, description, color = "bg-sky-100/40", textColor = "text-sky-900", decorColor = "decoration-sky-400/40", hoverColor="hover:bg-sky-200/60" }: { children?: React.ReactNode, description: string, color?: string, textColor?: string, decorColor?: string, hoverColor?: string }) => {
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
              <p className="font-sans font-bold text-sky-400 mb-2 uppercase tracking-[0.2em] text-[9px]">The Academic Insight</p>
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
        <div className="w-12 h-12 rounded-2xl bg-stone-900 flex items-center justify-center text-sky-400 shadow-xl border border-white/10">
          <Icon size={24} />
        </div>
      </div>
      <span className="inline-flex items-center gap-2 px-3 py-1 bg-sky-50 text-sky-600 text-[10px] font-black tracking-[0.4em] uppercase rounded-full mb-4">
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
  <div className="my-12 p-8 bg-sky-50/50 border-2 border-dashed border-sky-200 rounded-3xl">
    <div className="flex items-start gap-5">
      <div className="w-11 h-11 rounded-xl bg-sky-500 text-white flex items-center justify-center shrink-0 mt-1 shadow-lg shadow-sky-500/20">
        <Flag size={20} />
      </div>
      <div>
        <h4 className="font-bold text-sky-800 text-sm uppercase tracking-widest">Your Mission (Under 5 Mins)</h4>
        <div className="text-stone-600 mt-2 font-medium leading-relaxed">
          {children}
        </div>
      </div>
    </div>
  </div>
);

const ActivityRing = ({ progress, color = "#0ea5e9" }: { progress: number, color?: string }) => {
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
const DualTrackPlanner = () => {
    const [plan, setPlan] = useState<'rescue'|'mastery'>('rescue');

    const rescuePlan = { "Oral": 20, "Reading": 40, "Aural": 25, "Written": 15};
    const masteryPlan = { "Oral": 25, "Reading": 30, "Aural": 20, "Written": 25};
    const currentPlan = plan === 'rescue' ? rescuePlan : masteryPlan;
    
    return(
        <div className="my-10 p-8 md:p-12 bg-white rounded-[3rem] border border-stone-200 shadow-xl">
             <h4 className="font-serif text-2xl font-bold text-stone-800 text-center italic">Dual-Track Strategy Planner</h4>
             <div className="flex justify-center gap-2 p-1 bg-stone-100 rounded-full my-6 max-w-sm mx-auto">
                <button onClick={() => setPlan('rescue')} className={`w-full px-4 py-2 text-xs font-bold rounded-full ${plan === 'rescue' ? 'bg-white shadow' : ''}`}>Rescue Plan (Pass)</button>
                <button onClick={() => setPlan('mastery')} className={`w-full px-4 py-2 text-xs font-bold rounded-full ${plan === 'mastery' ? 'bg-white shadow' : ''}`}>Mastery Plan (H1)</button>
            </div>
            <div className="grid grid-cols-2 md:grid-cols-4 gap-4 text-center">
                {Object.entries(currentPlan).map(([component, value]) => (
                    <div key={component}>
                        <p className="font-bold text-sm">{component}</p>
                        <div className="w-full h-24 bg-stone-100 rounded-lg mt-2 flex items-end">
                            <motion.div className="w-full bg-sky-400 rounded-t-lg" initial={{height:0}} animate={{height: `${value*2}%`}}/>
                        </div>
                        <p className="text-xl font-bold mt-1">{value}%</p>
                    </div>
                ))}
            </div>
        </div>
    );
};

const OralBlueprintSliders = () => {
    const [quadrants, setQuadrants] = useState({ pron: 50, vocab: 50, struct: 50, comm: 50 });
    const weights = { pron: 0.2, vocab: 0.2, struct: 0.3, comm: 0.3 };
    const totalScore = (quadrants.pron * weights.pron) + (quadrants.vocab * weights.vocab) + (quadrants.struct * weights.struct) + (quadrants.comm * weights.comm);

    const Slider = ({label, value, setter}: {label:string, value:number, setter:(v:number)=>void}) => (
        <div>
            <label className="text-xs font-bold">{label} ({value}%)</label>
            <input type="range" min="0" max="100" value={value} onChange={e => setter(parseInt(e.target.value))} className="w-full accent-sky-500"/>
        </div>
    );

    return (
        <div className="my-10 p-8 md:p-12 bg-white rounded-[3rem] border border-stone-200 shadow-xl">
            <h4 className="font-serif text-2xl font-bold text-stone-800 text-center italic">Oral Exam Blueprint</h4>
            <div className="grid grid-cols-2 gap-6 items-center">
                <div className="space-y-4">
                    <Slider label="Pronunciation (20%)" value={quadrants.pron} setter={v => setQuadrants({...quadrants, pron: v})}/>
                    <Slider label="Vocabulary (20%)" value={quadrants.vocab} setter={v => setQuadrants({...quadrants, vocab: v})}/>
                    <Slider label="Structure (30%)" value={quadrants.struct} setter={v => setQuadrants({...quadrants, struct: v})}/>
                    <Slider label="Communication (30%)" value={quadrants.comm} setter={v => setQuadrants({...quadrants, comm: v})}/>
                </div>
                <div className="text-center">
                     <p className="text-sm text-stone-500">Your Oral Grade:</p>
                     <p className="text-6xl font-black text-sky-500 tracking-tighter">{Math.round(totalScore)}%</p>
                </div>
            </div>
        </div>
    );
};

const ParagraphSorter = () => {
    const [items, setItems] = useState([
        { id: 1, text: "Expansion/Reason" },
        { id: 2, text: "Topic Sentence" },
        { id: 3, text: "Connector/Bridge" },
        { id: 4, text: "Example" },
    ]);
    const correctOrder = [2, 1, 4, 3];
    const isCorrect = items.every((item, i) => item.id === correctOrder[i]);

    return (
        <div className="my-10 p-8 md:p-12 bg-white rounded-[3rem] border border-stone-200 shadow-xl">
            <h4 className="font-serif text-2xl font-bold text-stone-800 text-center italic">Paragraph Algorithm</h4>
            <p className="text-center text-sm text-stone-500 mb-6">Drag these components into the correct order to build a perfect essay paragraph.</p>
            <Reorder.Group axis="y" values={items} onReorder={setItems} className="space-y-2 max-w-sm mx-auto">
                {items.map(item => (
                    <Reorder.Item key={item.id} value={item} className="p-4 bg-stone-100 rounded-lg text-center font-bold text-stone-700 cursor-grab active:cursor-grabbing">
                        {item.text}
                    </Reorder.Item>
                ))}
            </Reorder.Group>
            {isCorrect && <p className="text-center font-bold text-emerald-600 mt-4">Correct! This is the blueprint for a high-scoring paragraph.</p>}
        </div>
    );
};


// --- MODULE COMPONENT ---
export const LanguageMasteryModule: React.FC<LanguageMasteryModuleProps> = ({ onBack }) => {
  const [activeSection, setActiveSection] = useState(0);
  const [unlockedSection, setUnlockedSection] = useState(0);
  
  const sections = [
    { id: 'dual-track', title: 'The Dual-Track Imperative', eyebrow: '01 // The Strategy', icon: Target },
    { id: 'oral-blueprint', title: 'The Oral Blueprint', eyebrow: '02 // The 25% Bank', icon: Mic },
    { id: 'examiner-forensics', title: 'Examiner Forensics', eyebrow: '03 // Killer Errors vs H1 Differentiators', icon: Brain },
    { id: 'vocab-vault', title: 'The Vocabulary Vault', eyebrow: '04 // SRS vs Goldlist', icon: Wrench },
    { id: 'auditory-processing', title: 'Auditory Processing', eyebrow: '05 // The Aural Exam', icon: Headphones },
    { id: 'reading-protocols', title: 'Reading Comprehension Protocols', eyebrow: '06 // Search & Extract', icon: BookOpen },
    { id: 'written-algorithms', title: 'Written Production Algorithms', eyebrow: '07 // The Paragraph Engine', icon: PenSquare },
    { id: 'mastery-plan', title: 'Your Mastery Plan', eyebrow: '08 // The Action Plan', icon: Languages },
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
            <p className="text-[9px] font-black text-sky-500 uppercase tracking-[0.4em] mb-0.5 underline">Module 02</p>
            <h1 className="font-serif font-bold text-lg tracking-tight text-stone-900">Mastering Languages</h1>
          </div>
        </div>

        <div className="flex-grow space-y-4 overflow-y-auto no-scrollbar pr-2 relative">
          <div className="absolute left-[21px] top-6 bottom-6 w-0.5 bg-stone-100 -z-0" />
          <div className="absolute left-[21px] top-6 bottom-6 w-0.5">
              <motion.div
                  className="w-full bg-sky-500 shadow-[0_0_10px_rgba(14,165,233,0.5)]"
                  initial={{ height: 0 }}
                  animate={{ height: sections.length > 1 ? `${(unlockedSection / (sections.length - 1)) * 100}%` : '0%' }}
              />
          </div>
          {sections.map((section, idx) => {
            const isUnlocked = idx <= unlockedSection;
            const isActive = idx === activeSection;
            const isCompleted = idx < unlockedSection;
            return (
              <button key={section.id} disabled={!isUnlocked} onClick={() => handleJumpToSection(idx)} className={`relative z-10 w-full flex items-center gap-4 p-3 rounded-xl transition-all duration-500 text-left group ${isActive ? 'bg-sky-50 shadow-sm translate-x-2' : ''} ${!isUnlocked ? 'opacity-40 grayscale cursor-not-allowed' : 'hover:bg-stone-50'}`}>
                <div className={`w-11 h-11 rounded-xl flex items-center justify-center shrink-0 border-2 transition-all duration-500 ${isCompleted ? 'bg-sky-600 border-sky-600 text-white shadow-lg' : isActive ? 'bg-white border-sky-500 text-sky-600 shadow-xl rotate-12' : 'bg-white border-stone-200 text-stone-300'}`}>
                   {isCompleted ? <CheckCircle2 size={18} /> : isActive ? <section.icon size={18} /> : <Lock size={16} />}
                </div>
                <div className="flex-grow"><p className={`text-[8px] font-black uppercase tracking-widest ${isActive ? 'text-sky-500' : 'text-stone-400'}`}>{section.eyebrow.split('// ')[1]}</p><h4 className={`text-xs font-bold leading-tight ${isActive ? 'text-stone-900' : 'text-stone-500'}`}>{section.title}</h4></div>
              </button>
            );
          })}
        </div>
        <div className="mt-8 border-t border-stone-100 pt-8 flex flex-col items-center">
           <ActivityRing progress={progress} color="#0ea5e9" /><p className="text-[11px] font-black text-stone-900 uppercase tracking-widest text-center">Progress</p>
        </div>
      </aside>

      <main className="flex-grow flex flex-col items-center py-10 md:py-24 px-6 md:px-16 overflow-y-auto h-screen relative">
        <div className="absolute inset-0 bg-[radial-gradient(#e5e7eb_1px,transparent_1px)] [background-size:32px_32px] opacity-40 pointer-events-none" />
        <div className="w-full max-w-4xl relative z-10">
          <AnimatePresence mode="wait">
            <motion.div key={activeSection} initial={{ opacity: 0, x: 20 }} animate={{ opacity: 1, x: 0 }} exit={{ opacity: 0, x: -20 }} transition={{ duration: 0.6, ease: [0.16, 1, 0.3, 1] }}>
              {activeSection === 0 && (
                <ReadingSection title="The Dual-Track Imperative." eyebrow="Step 1" icon={Target}>
                  <p>The Leaving Cert MFL exam isn't one test; it's two. For students at risk of failing, the goal is <Highlight description="The ability to transact meaning despite grammatical errors. This is the 'Rescue Plan'.">Communicative Proficiency</Highlight>. For students aiming for a H1, the goal is <Highlight description="Demonstrating syntactical complexity, idiomatic richness, and meta-cognitive control. This is the 'Mastery Plan'.">Language Awareness</Highlight>. A one-size-fits-all approach is a recipe for failure. Your strategy must match your target.</p>
                  <p>The allocation of marks is a strategic map. A fatal error is focusing on written production when the Oral and Reading components offer a much higher return on investment, especially for students on the "Rescue Plan".</p>
                  <DualTrackPlanner />
                </ReadingSection>
              )}
               {activeSection === 1 && (
                <ReadingSection title="The Oral Blueprint." eyebrow="Step 2" icon={Mic}>
                  <p>The Oral is the highest ROI activity in the entire Leaving Cert. It happens before the written papers, allowing you to "bank" up to 25% of your final grade. The marking scheme is a universal algorithm, divided into four quadrants: <Highlight description="Intonation, rhythm, and accuracy of sounds (20%).">Pronunciation</Highlight>, <Highlight description="Lexical richness and idiomatic language (20%).">Vocabulary</Highlight>, <Highlight description="Grammatical accuracy and complexity (30%).">Structure</Highlight>, and <Highlight description="Fluency, spontaneity, and sustaining interaction (30%).">Communication</Highlight>.</p>
                  <p>Understanding how these are weighted is key. Structure and Communication make up 60% of the marks. For the "Rescue Plan," the goal is verb control in the present tense. For the "Mastery Plan," it's about toggling tenses and deploying advanced structures like the Subjunctive.</p>
                  <OralBlueprintSliders />
                </ReadingSection>
              )}
               {activeSection === 2 && (
                <ReadingSection title="Examiner Forensics." eyebrow="Step 3" icon={Brain}>
                  <p>Chief Examiner Reports are the exam's "black box recorder," telling us exactly why students fail and succeed. The biggest <Highlight description="Errors that cap a student's grade, regardless of other strengths.">"Killer Error"</Highlight> is the "Rote Learning Penalty"—reciting a pre-learned essay that doesn't answer the question. This gets punished heavily in the Communication quadrant.</p>
                  <p>Conversely, there are clear <Highlight description="Skills that reliably signal a top-tier student to an examiner.">"H1 Differentiators."</Highlight> In French and Spanish, the number one differentiator is the spontaneous, correct use of the **Subjunctive Mood**. In German, it's mastery of word order—the **"Verb Kicker"** rule. These aren't just grammar points; they are signals of high-level Language Awareness.</p>
                </ReadingSection>
              )}
              {activeSection === 3 && (
                <ReadingSection title="The Vocabulary Vault." eyebrow="Step 4" icon={Wrench}>
                  <p>The Leaving Cert requires a massive vocabulary (2,000-3,000 words for a H1). This cannot be crammed. You need a system based on cognitive science. There are two main approaches.</p>
                  <p><Highlight description="Software (like Anki) that uses algorithms to schedule flashcard reviews at the precise moment you're about to forget them. Highly efficient but can be high-maintenance.">Spaced Repetition Systems (SRS)</Highlight> are the digital, high-efficiency option. The <Highlight description="A low-tech, low-stress method involving writing lists of words in a notebook and reviewing them after a two-week 'incubation' period. Excellent for passive vocabulary.">Goldlist Method</Highlight> is the analog, low-stress alternative, relying on the physical act of writing to aid retention. The best strategy is often a hybrid: SRS for active vocabulary (production) and Goldlist for passive vocabulary (recognition).</p>
                </ReadingSection>
              )}
              {activeSection === 4 && (
                <ReadingSection title="Auditory Processing." eyebrow="Step 5" icon={Headphones}>
                  <p>The Aural (Listening) exam is not a passive activity. It requires active processing strategies. The most important is <Highlight description="Using the pre-listening reading time to analyze the questions and predict the *type* of answer required (e.g., a number, a place, an emotion).">Prediction & Priming</Highlight>. This tunes your brain to listen for specific information.</p>
                  <p>To improve your ear, you need <Highlight description="Listening to native materials to internalize the rhythm and intonation of the language.">Contextual Immersion</Highlight>. Resources like "News in Slow French/German/Spanish" are perfect. A powerful technique is <Highlight description="Listening to a native speaker and repeating what they say almost simultaneously. This builds a direct link between your auditory and motor cortex, dramatically improving pronunciation.">Shadowing</Highlight>, which is the ultimate hack for your Pronunciation marks in the Oral.</p>
                </ReadingSection>
              )}
              {activeSection === 5 && (
                <ReadingSection title="Reading Protocols." eyebrow="Step 6" icon={BookOpen}>
                  <p>The Reading Comprehension is the single largest component for Ordinary Level students (40%). The biggest trap is trying to translate every word. The expert strategy is <Highlight description="The technique of underlining keywords in the question and scanning the text for them, knowing that answers almost always appear in chronological order.">"Search and Extract."</Highlight></p>
                  <p>Beware the <Highlight description="A critical distinction in French exams. 'Trouvez' means quote exactly; 'Indiquez' means manipulate the language (e.g., change 'je' to 'il'). Failure to distinguish these is a major source of lost marks.">"Manipulation Rule"</Highlight> in French. If the question says "Trouvez," you quote. If it says "Indiquez" or "Dites," you must change the grammar. This is a classic differentiator between H1 and H2 students.</p>
                </ReadingSection>
              )}
               {activeSection === 6 && (
                <ReadingSection title="Written Algorithms." eyebrow="Step 7" icon={PenSquare}>
                  <p>High-scoring essays are not works of creative genius; they are assembled using pre-fabricated, high-quality components. Every paragraph should follow a strict <Highlight description="A 4-part structure for building coherent paragraphs: 1. Topic Sentence, 2. Expansion/Reason, 3. Example, 4. Connector/Bridge to the next point.">Paragraph Algorithm</Highlight>.</p>
                  <p>For the "Mastery Plan," the goal is to use sophisticated logical connectors (e.g., *Néanmoins*, *De surcroît*) and avoid starting sentences with basic words like "Et" or "Mais." This signals high-level Language Awareness to the examiner.</p>
                  <ParagraphSorter />
                </ReadingSection>
              )}
              {activeSection === 7 && (
                <ReadingSection title="Your Mastery Plan." eyebrow="Step 8" icon={Languages}>
                    <p>You now have the complete strategic blueprint for the Leaving Cert MFL exams. You understand the dual-track system, the importance of each component, and the specific cognitive and tactical tools required for success. The exam is not a mystery; it is a system that can be engineered.</p>
                    <MicroCommitment>
                      <p>Pick ONE strategy from this module. Whether it's the "Search and Extract" technique, the Paragraph Algorithm, or starting a Goldlist notebook. Commit to trying it just once this week. You've just taken your first step from being a language student to a language engineer.</p>
                    </MicroCommitment>
                </ReadingSection>
              )}
              <footer className="mt-24 flex items-center justify-between pt-12 border-t border-stone-200/60 px-4">
                <motion.button whileHover={{ scale: 1.05 }} whileTap={{ scale: 0.95 }} onClick={handlePrev} disabled={activeSection === 0} className={`flex items-center gap-4 bg-stone-100 text-stone-800 px-8 py-4 rounded-xl font-black text-[10px] uppercase tracking-widest transition-all shadow-sm ${activeSection === 0 ? 'opacity-0 pointer-events-none' : ''}`}>
                  <ArrowLeft size={16} /> Prev
                </motion.button>
                <motion.button whileHover={{ scale: 1.05 }} whileTap={{ scale: 0.95 }} onClick={handleCompleteSection} className="group relative flex items-center gap-4 bg-stone-900 text-white px-12 py-6 rounded-2xl font-black text-[12px] uppercase tracking-widest hover:bg-sky-600 transition-all shadow-[0_20px_50px_rgba(0,0,0,0.2)] overflow-hidden">
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
