
/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
*/

import React, { useState, useEffect } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { 
  ArrowLeft, CheckCircle2, ArrowRight, Shield,
  Lock, Flag, HeartCrack, Recycle, Mic, Wrench, Quote
} from 'lucide-react';

type ModuleProgress = {
  unlockedSection: number;
};

// FIX: Added progress and onProgressUpdate props to align with App.tsx usage and enable state management.
interface TheGrammarOfGritModuleProps {
  onBack: () => void;
  progress: ModuleProgress;
  onProgressUpdate: (progress: ModuleProgress) => void;
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

// FIX: Completed the truncated file to provide the full module content.
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
  
  const ExplanatoryStyleQuiz = () => {
      const [answers, setAnswers] = useState<( 'pessimistic' | 'optimistic' | null)[]>([null, null, null]);
      const score = answers.filter(a => a === 'optimistic').length;
      
      const handleAnswer = (index: number, type: 'pessimistic' | 'optimistic') => {
        const newAnswers = [...answers];
        newAnswers[index] = type;
        setAnswers(newAnswers);
      };
      
      const isComplete = answers.every(a => a !== null);
  
      return (
        <div className="my-10 p-8 md:p-12 bg-white rounded-[3rem] border border-stone-200 shadow-xl">
          <h4 className="font-serif text-2xl font-bold text-stone-800 text-center italic">Self-Talk Diagnostic</h4>
          <p className="text-center text-sm text-stone-500 mb-8">You fail a test. Which voice is louder in your head?</p>
          <div className="space-y-6">
              <div>
                  <p className="text-center font-bold mb-2">"This means I'm stupid." vs "This means my strategy was wrong."</p>
                  <div className="grid grid-cols-2 gap-3"><button onClick={() => handleAnswer(0, 'pessimistic')} className={`p-4 rounded-xl border-2 ${answers[0] === 'pessimistic' ? 'bg-rose-500 text-white' : 'bg-stone-50'}`}>A</button><button onClick={() => handleAnswer(0, 'optimistic')} className={`p-4 rounded-xl border-2 ${answers[0] === 'optimistic' ? 'bg-emerald-500 text-white' : 'bg-stone-50'}`}>B</button></div>
              </div>
               <div>
                  <p className="text-center font-bold mb-2">"I'll never get this." vs "I'll try again tomorrow."</p>
                  <div className="grid grid-cols-2 gap-3"><button onClick={() => handleAnswer(1, 'pessimistic')} className={`p-4 rounded-xl border-2 ${answers[1] === 'pessimistic' ? 'bg-rose-500 text-white' : 'bg-stone-50'}`}>A</button><button onClick={() => handleAnswer(1, 'optimistic')} className={`p-4 rounded-xl border-2 ${answers[1] === 'optimistic' ? 'bg-emerald-500 text-white' : 'bg-stone-50'}`}>B</button></div>
              </div>
               <div>
                  <p className="text-center font-bold mb-2">"This ruins everything." vs "This is just one subject."</p>
                  <div className="grid grid-cols-2 gap-3"><button onClick={() => handleAnswer(2, 'pessimistic')} className={`p-4 rounded-xl border-2 ${answers[2] === 'pessimistic' ? 'bg-rose-500 text-white' : 'bg-stone-50'}`}>A</button><button onClick={() => handleAnswer(2, 'optimistic')} className={`p-4 rounded-xl border-2 ${answers[2] === 'optimistic' ? 'bg-emerald-500 text-white' : 'bg-stone-50'}`}>B</button></div>
              </div>
          </div>
           {isComplete && <p className="text-center mt-4 text-sm font-bold">{score > 1 ? <span className="text-emerald-600">Your explanatory style is optimistic and builds resilience.</span> : <span className="text-rose-600">Your explanatory style is pessimistic and may be eroding your resilience.</span>}</p>}
        </div>
      );
  };

export const TheGrammarOfGritModule: React.FC<TheGrammarOfGritModuleProps> = ({ onBack, progress, onProgressUpdate }) => {
  const [activeSection, setActiveSection] = useState(progress.unlockedSection);
  const unlockedSection = progress.unlockedSection;

  const sections = [
    { id: 'internal-narrator', title: 'Your Internal Narrator', eyebrow: '01 // The Source Code', icon: Mic },
    { id: 'three-ps', title: 'The 3 Ps of Failure', eyebrow: '02 // Personal, Pervasive, Permanent', icon: HeartCrack },
    { id: 'rewrite-protocol', title: 'The Re-Write Protocol', eyebrow: '03 // From Fragile to Agile', icon: Recycle },
    { id: 'self-compassion', title: 'The Role of Self-Compassion', eyebrow: '04 // The Antidote to Shame', icon: Shield },
    { id: 'blueprint', title: 'Your Resilience Blueprint', eyebrow: '05 // The Action Plan', icon: Wrench },
  ];

  useEffect(() => {
    setActiveSection(progress.unlockedSection);
  }, [progress.unlockedSection]);

  const handleCompleteSection = () => {
    if (activeSection === unlockedSection && unlockedSection < sections.length) {
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

  const progressPercentage = sections.length > 0 ? (unlockedSection / sections.length) * 100 : 0;

  return (
    <div className="min-h-screen bg-[#FBFBF9] text-stone-900 font-sans flex flex-col md:flex-row overflow-x-hidden">
      <aside className="w-full md:w-80 bg-white border-r border-stone-200 sticky top-0 md:h-screen z-40 p-8 flex flex-col">
        <div className="flex items-center gap-4 mb-12">
          <motion.button whileHover={{ scale: 1.05 }} whileTap={{ scale: 0.95 }} onClick={onBack} className="p-2 rounded-full transition-all border border-stone-200/50 shadow-sm bg-white">
            <ArrowLeft size={16} className="text-stone-700" />
          </motion.button>
          <div>
            <p className="text-[9px] font-black text-blue-500 uppercase tracking-[0.4em] mb-0.5 underline">Module 05</p>
            <h1 className="font-serif font-bold text-lg tracking-tight text-stone-900">The Grammar of Grit</h1>
          </div>
        </div>

        <div className="flex-grow space-y-4 overflow-y-auto no-scrollbar pr-2 relative">
          <div className="absolute left-[21px] top-6 bottom-6 w-0.5 bg-stone-100 -z-0" />
          <div className="absolute left-[21px] top-6 bottom-6 w-0.5">
              <motion.div
                  className="w-full bg-blue-500 shadow-[0_0_10px_rgba(59,130,246,0.5)]"
                  style={{ height: `${progressPercentage}%` }}
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
           <ActivityRing progress={progressPercentage} /><p className="text-[11px] font-black text-stone-900 uppercase tracking-widest text-center">Progress</p>
        </div>
      </aside>

      <main className="flex-grow flex flex-col items-center py-10 md:py-24 px-6 md:px-16 overflow-y-auto h-screen relative">
        <div className="absolute inset-0 bg-[radial-gradient(#e5e7eb_1px,transparent_1px)] [background-size:32px_32px] opacity-40 pointer-events-none" />
        <div className="w-full max-w-4xl relative z-10">
          <AnimatePresence mode="wait">
            <motion.div key={activeSection} initial={{ opacity: 0, x: 20 }} animate={{ opacity: 1, x: 0 }} exit={{ opacity: 0, x: -20 }} transition={{ duration: 0.6, ease: [0.16, 1, 0.3, 1] }}>
              {activeSection === 0 && (
                <ReadingSection title="Your Internal Narrator." eyebrow="Step 1" icon={Mic}>
                  <p>When you face a setback, who is the narrator in your head? The language they use is not just commentary; it's the source code for your resilience. The science of <Highlight description="Your habitual way of explaining events. It's a powerful predictor of your resilience, motivation, and even your physical health.">Explanatory Style</Highlight>, pioneered by Martin Seligman, shows that the 'grammar' of your self-talk determines whether you bounce back or break down.</p>
                  <ExplanatoryStyleQuiz />
                </ReadingSection>
              )}
              {activeSection === 1 && (
                <ReadingSection title="The 3 Ps of Failure." eyebrow="Step 2" icon={HeartCrack}>
                  <p>A pessimistic explanatory style, which erodes grit, interprets failure through three toxic lenses: **Personal** ("It's my fault; I'm stupid"), **Pervasive** ("I ruin everything I touch"), and **Permanent** ("It's always going to be this way"). This isn't just negative thinking; it's a specific grammatical structure that leads to learned helplessness.</p>
                  <p>An optimistic, resilient style does the opposite. It sees failure as **External/Specific** ("The strategy was wrong"), **Specific** ("I messed up this one thing"), and **Temporary** ("I'll do better next time"). This isn't about lying to yourself; it's about a disciplined, strategic choice to focus on what you can control.</p>
                </ReadingSection>
              )}
              {activeSection === 2 && (
                <ReadingSection title="The Re-Write Protocol." eyebrow="Step 3" icon={Recycle}>
                  <p>You can train your brain to adopt a more optimistic style. This is called <Highlight description="A core technique of Cognitive Behavioural Therapy (CBT) where you learn to identify, challenge, and change your negative automatic thoughts.">Cognitive Restructuring</Highlight>. When you catch yourself using one of the 3 Ps, you must consciously "re-write" the script. For example, "I'm useless at Maths" (Personal, Permanent) becomes "My study method for trigonometry isn't working yet" (Specific, Temporary).</p>
                  <MicroCommitment><p>Take one negative thought you had about school this week. Write it down. Now, try to rewrite it, changing one of the '3 Ps'. Turn a 'Personal' blame into a 'Specific' strategy problem.</p></MicroCommitment>
                </ReadingSection>
              )}
               {activeSection === 3 && (
                <ReadingSection title="The Role of Self-Compassion." eyebrow="Step 4" icon={Shield}>
                    <p>A harsh inner critic doesn't build resilience; it creates shame, which is a powerful de-motivator. <Highlight description="Treating yourself with the same kindness you would offer a friend who is struggling. It's a powerful antidote to the shame that can follow failure.">Self-compassion</Highlight> is the antidote. It allows you to acknowledge a failure without letting it define you. It's the difference between "I failed" and "I am a failure."</p>
                    <p>It has three parts: 1) **Self-Kindness**: Treat yourself like you'd treat a mate. 2) **Common Humanity**: Remember that everyone messes up. 3) **Mindfulness**: Acknowledge the feeling without letting it consume you.</p>
                </ReadingSection>
              )}
               {activeSection === 4 && (
                <ReadingSection title="Your Resilience Blueprint." eyebrow="Step 5" icon={Wrench}>
                  <p>You now have the tools to become the editor of your own internal monologue. By auditing your self-talk for the 3 Ps and consciously rewriting the script with self-compassion, you can build a resilient, growth-oriented mindset one sentence at a time.</p>
                  <MicroCommitment>
                    <p>The next time you make a small mistake, just notice your first thought. Don't judge it, just label it. Was it Personal? Pervasive? Permanent? This act of noticing is the first step to taking control.</p>
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
