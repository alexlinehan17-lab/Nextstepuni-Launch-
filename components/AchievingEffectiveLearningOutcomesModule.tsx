

/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
*/

import React, { useState } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { 
  ArrowLeft, CheckCircle2, ArrowRight, 
  Lock, Flag, Eye, BarChart3, BrainCircuit, Timer, HeartPulse, ClipboardCheck
} from 'lucide-react';

interface AchievingEffectiveLearningOutcomesModuleProps {
  onBack: () => void;
}

const Highlight = ({ children, description, color = "bg-teal-100/40", textColor = "text-teal-900", decorColor = "decoration-teal-400/40", hoverColor="hover:bg-teal-200/60" }: { children?: React.ReactNode, description: string, color?: string, textColor?: string, decorColor?: string, hoverColor?: string }) => {
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
              <p className="font-sans font-bold text-teal-400 mb-2 uppercase tracking-[0.2em] text-[9px]">The Academic Insight</p>
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
        <div className="w-12 h-12 rounded-2xl bg-stone-900 flex items-center justify-center text-teal-400 shadow-xl border border-white/10">
          <Icon size={24} />
        </div>
      </div>
      <span className="inline-flex items-center gap-2 px-3 py-1 bg-teal-50 text-teal-600 text-[10px] font-black tracking-[0.4em] uppercase rounded-full mb-4">
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
  <div className="my-12 p-8 bg-teal-50/50 border-2 border-dashed border-teal-200 rounded-3xl">
    <div className="flex items-start gap-5">
      <div className="w-11 h-11 rounded-xl bg-teal-500 text-white flex items-center justify-center shrink-0 mt-1 shadow-lg shadow-teal-500/20">
        <Flag size={20} />
      </div>
      <div>
        <h4 className="font-bold text-teal-800 text-sm uppercase tracking-widest">Your Mission (Under 5 Mins)</h4>
        <div className="text-stone-600 mt-2 font-medium leading-relaxed">
          {children}
        </div>
      </div>
    </div>
  </div>
);

const ActivityRing = ({ progress, color = "#14b8a6" }: { progress: number, color?: string }) => {
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
const IllusionOfCompetenceChart = () => {
    const [view, setView] = useState<'prediction' | 'reality'>('prediction');
    const ssssData = { prediction: 90, reality: 40 };
    const stttData = { prediction: 40, reality: 61 };

    return (
        <div className="my-10 p-8 md:p-12 bg-white rounded-[3rem] border border-stone-200 shadow-xl">
            <h4 className="font-serif text-2xl font-bold text-stone-800 text-center italic">The Great Deception</h4>
            <p className="text-center text-sm text-stone-500 mb-8">Data from Roediger & Karpicke (2006) reveals the gap between what *feels* effective and what *is* effective.</p>
            <div className="grid grid-cols-2 gap-4 mb-8">
                <div className="text-center">
                    <h5 className="font-bold mb-2">Passive Rereading (SSSS)</h5>
                    <div className="h-48 w-full bg-stone-100 rounded-lg flex items-end">
                        <motion.div className="w-full bg-teal-400 rounded-t-lg" initial={{height:0}} animate={{height: `${view === 'prediction' ? ssssData.prediction : ssssData.reality}%`}} transition={{type: 'spring', stiffness: 100}}/>
                    </div>
                </div>
                <div className="text-center">
                     <h5 className="font-bold mb-2">Active Recall (STTT)</h5>
                     <div className="h-48 w-full bg-stone-100 rounded-lg flex items-end">
                        <motion.div className="w-full bg-indigo-400 rounded-t-lg" initial={{height:0}} animate={{height: `${view === 'prediction' ? stttData.prediction : stttData.reality}%`}} transition={{type: 'spring', stiffness: 100}}/>
                    </div>
                </div>
            </div>
            <div className="flex justify-center gap-2 p-1 bg-stone-100 rounded-full">
                <button onClick={() => setView('prediction')} className={`px-4 py-2 text-xs font-bold rounded-full ${view === 'prediction' ? 'bg-white shadow' : ''}`}>Student Prediction (JOL)</button>
                <button onClick={() => setView('reality')} className={`px-4 py-2 text-xs font-bold rounded-full ${view === 'reality' ? 'bg-white shadow' : ''}`}>Actual Test Results (1 Week Later)</button>
            </div>
        </div>
    );
};


// --- MODULE COMPONENT ---
export const AchievingEffectiveLearningOutcomesModule: React.FC<{onBack: () => void}> = ({ onBack }) => {
  const [activeSection, setActiveSection] = useState(0);
  const [unlockedSection, setUnlockedSection] = useState(0);
  
  const sections = [
    { id: 'illusion-of-competence', title: 'The Illusion of Competence', eyebrow: '01 // The Paradox', icon: Eye },
    { id: 'hard-data', title: 'The Hard Data', eyebrow: '02 // The Crossover Effect', icon: BarChart3 },
    { id: 'active-retrieval', title: 'Active Retrieval', eyebrow: '03 // The Gold Standard', icon: BrainCircuit },
    { id: 'distributed-practice', title: 'Distributed Practice', eyebrow: '04 // The Forgetting Curve', icon: Timer },
    { id: 'anxiety-paradox', title: 'The Anxiety Paradox', eyebrow: '05 // The Stress Test', icon: HeartPulse },
    { id: 'action-plan', title: 'Your Action Plan', eyebrow: '06 // The Audit', icon: ClipboardCheck },
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
            <p className="text-[9px] font-black text-teal-500 uppercase tracking-[0.4em] mb-0.5 underline">Module 01</p>
            <h1 className="font-serif font-bold text-lg tracking-tight text-stone-900">Effective Learning Outcomes</h1>
          </div>
        </div>

        <div className="flex-grow space-y-4 overflow-y-auto no-scrollbar pr-2 relative">
          <div className="absolute left-[21px] top-6 bottom-6 w-0.5 bg-stone-100 -z-0" />
          <div className="absolute left-[21px] top-6 bottom-6 w-0.5">
              <motion.div
                  className="w-full bg-teal-500 shadow-[0_0_10px_rgba(20,184,166,0.5)]"
                  initial={{ height: 0 }}
                  animate={{ height: sections.length > 1 ? `${(unlockedSection / (sections.length - 1)) * 100}%` : '0%' }}
              />
          </div>
          {sections.map((section, idx) => {
            const isUnlocked = idx <= unlockedSection;
            const isActive = idx === activeSection;
            const isCompleted = idx < unlockedSection;
            return (
              <button key={section.id} disabled={!isUnlocked} onClick={() => handleJumpToSection(idx)} className={`relative z-10 w-full flex items-center gap-4 p-3 rounded-xl transition-all duration-500 text-left group ${isActive ? 'bg-teal-50 shadow-sm translate-x-2' : ''} ${!isUnlocked ? 'opacity-40 grayscale cursor-not-allowed' : 'hover:bg-stone-50'}`}>
                <div className={`w-11 h-11 rounded-xl flex items-center justify-center shrink-0 border-2 transition-all duration-500 ${isCompleted ? 'bg-teal-600 border-teal-600 text-white shadow-lg' : isActive ? 'bg-white border-teal-500 text-teal-600 shadow-xl rotate-12' : 'bg-white border-stone-200 text-stone-300'}`}>
                   {isCompleted ? <CheckCircle2 size={18} /> : isActive ? <section.icon size={18} /> : <Lock size={16} />}
                </div>
                <div className="flex-grow"><p className={`text-[8px] font-black uppercase tracking-widest ${isActive ? 'text-teal-500' : 'text-stone-400'}`}>{section.eyebrow.split('// ')[1]}</p><h4 className={`text-xs font-bold leading-tight ${isActive ? 'text-stone-900' : 'text-stone-500'}`}>{section.title}</h4></div>
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
                <ReadingSection title="The Illusion of Competence." eyebrow="Step 1" icon={Eye}>
                  <p>There's a huge paradox in how we learn: the study methods that feel the most productive are often the least effective. We gravitate towards passive strategies like re-reading textbooks, highlighting notes, and watching lectures because they feel comfortable and easy. The material becomes familiar, and we mistake this feeling of familiarity for mastery.</p>
                  <p>This is the <Highlight description="A metacognitive failure where you misinterpret the ease of processing information (fluency) as a sign of durable learning. It's the primary reason students choose ineffective study strategies.">Illusion of Competence</Highlight>. It's caused by a cognitive shortcut called <Highlight description="A mental heuristic where the brain uses the ease ('fluency') of processing as a proxy for value. If something is easy to read or recall, we assume it's well-learned or true.">Fluency Bias</Highlight>. Your brain is an energy-conserving organ; it loves the path of least resistance. The problem is, when it comes to learning, that path leads off a cliff.</p>
                </ReadingSection>
              )}
              {activeSection === 1 && (
                <ReadingSection title="The Hard Data." eyebrow="Step 2" icon={BarChart3}>
                  <p>This isn't just a theory; it's a measurable disaster. A landmark study by Roediger & Karpicke (2006) proved it. They had students study a text using two methods: one group just re-read it (passive review), and the other group read it once and then tried to recall everything they could (active retrieval).</p>
                  <p>The results are devastating for our intuition. The students who simply re-read the text were far more confident in their learning. But on the actual test a week later, they performed terribly, forgetting over half of what they'd studied. The students who used active recall were less confident, but they retained significantly more information. The strategy that *felt* worse was dramatically more effective. You can see the shocking data for yourself.</p>
                  <IllusionOfCompetenceChart />
                </ReadingSection>
              )}
              {activeSection === 2 && (
                <ReadingSection title="Active Retrieval." eyebrow="Step 3" icon={BrainCircuit}>
                    <p>The most powerful way to build lasting memory is <Highlight description="The act of deliberately recalling information from memory, rather than passively reviewing it. This struggle to retrieve is the mechanism that strengthens long-term storage.">Active Retrieval</Highlight>, also known as practice testing. It's the "gold standard" for learning. Why? Because the act of struggling to pull information out of your brain sends a powerful signal to strengthen that neural pathway for future use.</p>
                    <p>This is the opposite of re-reading. Re-reading is like looking at a map of a city. Active retrieval is like being dropped in the city and forced to find your own way. It's harder, more frustrating, and you'll make more mistakes. But it's the only way you'll actually learn the layout. The struggle is not a sign that you're failing; it's the biological signal that you're learning.</p>
                </ReadingSection>
              )}
              {activeSection === 3 && (
                <ReadingSection title="Distributed Practice." eyebrow="Step 4" icon={Timer}>
                  <p>The second "golden rule" is <Highlight description="Also known as 'spacing.' It's the strategy of spreading out your study sessions over time, rather than cramming them all at once.">Distributed Practice</Highlight>. Cramming feels effective because it keeps information in your short-term working memory. It works for a test in 10 minutes, but it's a disaster for a test in a week.</p>
                  <p>Spacing leverages the <Highlight description="The natural, exponential decay of memory over time. To create durable learning, you must interrupt this curve by revisiting the information just as you're beginning to forget it.">Forgetting Curve</Highlight>. To build strong memories, you need to let yourself forget a little. This makes the next retrieval attempt harder, which, as we've learned, sends a stronger signal to your brain to "save this file permanently." The rule is simple: one hour a day for seven days is infinitely better than seven hours in one day.</p>
                </ReadingSection>
              )}
               {activeSection === 4 && (
                <ReadingSection title="The Anxiety Paradox." eyebrow="Step 5" icon={HeartPulse}>
                  <p>A common argument against more testing is that it causes anxiety. But the research shows the opposite. Frequent, low-stakes quizzing is one of the most powerful tools for *reducing* exam anxiety. Why? Because anxiety often comes from uncertainty. The Illusion of Competence leaves you feeling confident but actually being unprepared. The high-stakes exam is the first time you discover the truth, leading to panic.</p>
                  <p>Active retrieval is a process of <Highlight description="The act of accurately judging your own level of knowledge. Low-stakes testing calibrates your metacognition, eliminating the surprise and anxiety of a high-stakes exam.">Metacognitive Calibration</Highlight>. It strips away the illusion. By constantly testing yourself, you know *exactly* what you know and what you don't long before the real exam. There are no surprises, no panic. You've already faced the struggle in a low-stakes environment, desensitizing yourself to the pressure.</p>
                </ReadingSection>
              )}
               {activeSection === 5 && (
                <ReadingSection title="Your Action Plan." eyebrow="Step 6" icon={ClipboardCheck}>
                    <p>You now have the scientific evidence. The final step is to apply it. You must abandon the comfort of passive review and embrace the "desirable difficulty" of active retrieval. The key takeaways are simple but transformative.</p>
                    <p>**The "Book Closed" Rule:** Never judge how well you know something with the book open in front of you. That's just fluency talking. Close the book, then ask yourself what you know. **Embrace Disfluency:** Understand that the feeling of "struggle" is the feeling of learning happening. If studying feels easy, it's probably ineffective. **Stop Dropping Items:** Don't stop testing yourself on something just because you got it right once. Continued retrieval is what arrests the forgetting curve. </p>
                    <MicroCommitment>
                        <p>For your next study session, commit to this: for every 30 minutes, spend 10 minutes reading/reviewing, and 20 minutes testing yourself on what you just read. You will double your retention.</p>
                    </MicroCommitment>
                </ReadingSection>
              )}
              <footer className="mt-24 flex items-center justify-between pt-12 border-t border-stone-200/60 px-4">
                <motion.button whileHover={{ scale: 1.05 }} whileTap={{ scale: 0.95 }} onClick={handlePrev} disabled={activeSection === 0} className={`flex items-center gap-4 bg-stone-100 text-stone-800 px-8 py-4 rounded-xl font-black text-[10px] uppercase tracking-widest transition-all shadow-sm ${activeSection === 0 ? 'opacity-0 pointer-events-none' : ''}`}>
                  <ArrowLeft size={16} /> Prev
                </motion.button>
                <motion.button whileHover={{ scale: 1.05 }} whileTap={{ scale: 0.95 }} onClick={handleCompleteSection} className="group relative flex items-center gap-4 bg-stone-900 text-white px-12 py-6 rounded-2xl font-black text-[12px] uppercase tracking-widest hover:bg-teal-600 transition-all shadow-[0_20px_50px_rgba(0,0,0,0.2)] overflow-hidden">
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
