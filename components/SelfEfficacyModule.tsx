
/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
*/

import React, { useState, useEffect } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { 
  ArrowLeft, CheckCircle2, ArrowRight, 
  Lock, Flag, Target, Brain, Shield, Eye, Settings
} from 'lucide-react';

const MotionButton = motion.button as any;
const MotionDiv = motion.div as any;
const MotionCircle = motion.circle as any;
const MotionP = motion.p as any;

type ModuleProgress = {
  unlockedSection: number;
};

interface SelfEfficacyModuleProps {
  onBack: () => void;
  progress: ModuleProgress;
  onProgressUpdate: (progress: ModuleProgress) => void;
}

const Highlight = ({ children, description, color = "bg-rose-100/40", textColor = "text-rose-900", decorColor = "decoration-rose-400/40", hoverColor="hover:bg-rose-200/60" }: { children?: React.ReactNode, description: string, color?: string, textColor?: string, decorColor?: string, hoverColor?: string }) => {
  const [isOpen, setIsOpen] = useState(false);

  return (
    <span className="relative inline-block mx-0.5">
      <MotionButton 
        onClick={(e: React.MouseEvent) => {
          e.stopPropagation();
          setIsOpen(!isOpen);
        }}
        className={`relative inline-flex items-center px-2 py-0.5 font-bold ${color} ${textColor} rounded-md cursor-help ${hoverColor} transition-all duration-300 ${decorColor} underline decoration-2 underline-offset-4`}
      >
        <span className="not-italic">{children}</span>
      </MotionButton>
      <AnimatePresence>
        {isOpen && (
          <>
            <div className="fixed inset-0 z-[60]" onClick={() => setIsOpen(false)} />
            <MotionDiv 
              initial={{ opacity: 0, scale: 0.9, y: 10, x: "-50%" }}
              animate={{ opacity: 1, scale: 1, y: 0, x: "-50%" }}
              exit={{ opacity: 0, scale: 0.9, y: 10, x: "-50%" }}
              className="absolute z-[70] bottom-full left-1/2 mb-6 w-72 p-6 bg-stone-900/95 text-white text-xs rounded-2xl shadow-2xl pointer-events-auto leading-relaxed border border-white/10 backdrop-blur-xl whitespace-normal text-left"
              style={{ transformOrigin: 'bottom center' }}
            >
              <div className="absolute bottom-0 left-1/2 -translate-x-1/2 translate-y-full w-0 h-0 border-l-[10px] border-l-transparent border-r-[10px] border-r-transparent border-t-[10px] border-t-stone-900/95"></div>
              <p className="font-sans font-bold text-rose-400 mb-2 uppercase tracking-[0.2em] text-[9px]">The Academic Insight</p>
              <p className="text-stone-200 font-medium">{description}</p>
            </MotionDiv>
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
        <div className="w-12 h-12 rounded-2xl bg-stone-900 flex items-center justify-center text-rose-400 shadow-xl border border-white/10">
          <Icon size={24} />
        </div>
      </div>
      <span className="inline-flex items-center gap-2 px-3 py-1 bg-rose-50 text-rose-600 text-[10px] font-black tracking-[0.4em] uppercase rounded-full mb-4">
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
  <div className="my-12 p-8 bg-rose-50/50 border-2 border-dashed border-rose-200 rounded-3xl">
    <div className="flex items-start gap-5">
      <div className="w-11 h-11 rounded-xl bg-rose-500 text-white flex items-center justify-center shrink-0 mt-1 shadow-lg shadow-rose-500/20">
        <Flag size={20} />
      </div>
      <div>
        <h4 className="font-bold text-rose-800 text-sm uppercase tracking-widest">Your Mission (Under 5 Mins)</h4>
        <div className="text-stone-600 mt-2 font-medium leading-relaxed">
          {children}
        </div>
      </div>
    </div>
  </div>
);

const ActivityRing = ({ progress, color = "#e11d48" }: { progress: number, color?: string }) => {
  const radius = 35;
  const circumference = 2 * Math.PI * radius;
  const offset = circumference - (progress / 100) * circumference;

  return (
    <div className="relative flex items-center justify-center w-24 h-24 mx-auto mb-4">
      <svg className="w-full h-full -rotate-90 overflow-visible" viewBox="0 0 96 96">
        <circle cx="48" cy="48" r={radius} stroke={color} strokeWidth="10" fill="transparent" className="opacity-10"/>
        <MotionCircle cx="48" cy="48" r={radius} stroke={color} strokeWidth="10" fill="transparent" strokeDasharray={circumference} initial={{ strokeDashoffset: circumference }} animate={{ strokeDashoffset: offset }} transition={{ duration: 1.5, ease: "easeOut" }} strokeLinecap="round" style={{ filter: `drop-shadow(0 0 8px ${color}55)` }}/>
      </svg>
    </div>
  );
};

// --- INTERACTIVE COMPONENTS ---
const RoleModelSelector = () => {
    const [choice, setChoice] = useState<null | 'mastery' | 'coping'>(null);
    return (
        <div className="my-10 p-8 md:p-12 bg-white rounded-[3rem] border border-stone-200 shadow-xl">
             <h4 className="font-serif text-2xl font-bold text-stone-800 text-center italic">Which Story Builds More Belief?</h4>
             <p className="text-center text-sm text-stone-500 mb-6">You're struggling with a subject. Which of these role models is more helpful?</p>
             <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                <button onClick={() => setChoice('mastery')} className={`p-6 rounded-2xl text-left border-2 flex flex-col justify-between h-48 ${choice === 'mastery' ? 'bg-blue-500 text-white border-blue-500' : 'bg-stone-50 hover:bg-stone-100 border-stone-200'}`}>
                    <div>
                        <p className="font-bold text-lg">The Genius (Mastery Model)</p>
                        <p className="text-xs mt-1">A past pupil who got 625 points, found school easy, and is now a doctor.</p>
                    </div>
                    <p className="text-xs font-mono self-end">"Just work hard."</p>
                </button>
                 <button onClick={() => setChoice('coping')} className={`p-6 rounded-2xl text-left border-2 flex flex-col justify-between h-48 ${choice === 'coping' ? 'bg-emerald-500 text-white border-emerald-500' : 'bg-stone-50 hover:bg-stone-100 border-stone-200'}`}>
                    <div>
                        <p className="font-bold text-lg">The Grafter (Coping Model)</p>
                        <p className="text-xs mt-1">A past pupil who failed their mocks, changed their study habits, and got into their dream course.</p>
                    </div>
                     <p className="text-xs font-mono self-end">"Here's how I recovered."</p>
                </button>
             </div>
             {choice === 'coping' && <MotionP initial={{opacity:0}} animate={{opacity:1}} className="text-center mt-4 text-sm text-emerald-700 font-bold">Correct. Seeing someone struggle and recover is scientifically proven to be more motivating than seeing flawless success.</MotionP>}
        </div>
    );
};

const IcebergInteractive = () => {
    const [inputs, setInputs] = useState<string[]>([]);
    return (
        <div className="my-10 p-8 md:p-12 bg-white rounded-[3rem] border border-stone-200 shadow-xl">
            <h4 className="font-serif text-2xl font-bold text-stone-800 text-center italic">The Success Iceberg</h4>
            <p className="text-center text-sm text-stone-500 mb-8">Success is what people see. Process is what it takes. List the "invisible" parts of success.</p>
            <div className="max-w-md mx-auto">
                <div className="bg-blue-100 p-4 rounded-t-2xl text-center font-bold text-blue-800">Visible Success</div>
                <div className="bg-blue-50 p-6 rounded-b-2xl border-x-2 border-b-2 border-blue-200 min-h-[150px]">
                    <p className="text-sm font-bold text-stone-600 mb-2">Invisible Process:</p>
                    <ul className="list-disc list-inside text-sm text-stone-500 space-y-1">
                        {inputs.map((input, i) => <li key={i}>{input}</li>)}
                    </ul>
                     <input 
                        placeholder="e.g., failed attempts, asking for help..." 
                        className="w-full mt-4 p-2 text-sm bg-white border border-stone-300 rounded-md"
                        onKeyDown={(e) => {
                            if (e.key === 'Enter' && e.currentTarget.value) {
                                setInputs([...inputs, e.currentTarget.value]);
                                e.currentTarget.value = '';
                            }
                        }}
                    />
                </div>
            </div>
        </div>
    );
}

// --- MODULE COMPONENT ---
export const SelfEfficacyModule: React.FC<SelfEfficacyModuleProps> = ({ onBack, progress, onProgressUpdate }) => {
  const [activeSection, setActiveSection] = useState(progress.unlockedSection);
  const unlockedSection = progress.unlockedSection;
  
  const sections = [
    { id: 'belief-barrier', title: 'The Belief Barrier', eyebrow: '01 // Your Secret Engine', icon: Brain },
    { id: 'four-sources', title: 'How Belief is Built', eyebrow: '02 // The 4 Sources', icon: Target },
    { id: 'role-model-myth', title: 'The Role Model Myth', eyebrow: '03 // The Struggle Story', icon: Shield },
    { id: 'success-iceberg', title: 'The Success Iceberg', eyebrow: '04 // Detective of Process', icon: Eye },
    { id: 'habit-blueprint', title: 'The Habit Blueprint', eyebrow: '05 // Reverse-Engineer Success', icon: Settings },
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
          <MotionButton whileHover={{ scale: 1.05 }} whileTap={{ scale: 0.95 }} onClick={onBack} className="p-2 rounded-full transition-all border border-stone-200/50 shadow-sm bg-white">
            <ArrowLeft size={16} className="text-stone-700" />
          </MotionButton>
          <div>
            <p className="text-[9px] font-black text-rose-500 uppercase tracking-[0.4em] mb-0.5 underline">Module 09</p>
            <h1 className="font-serif font-bold text-lg tracking-tight text-stone-900">Self Efficacy</h1>
          </div>
        </div>

        <div className="flex-grow space-y-4 overflow-y-auto no-scrollbar pr-2 relative">
          <div className="absolute left-[21px] top-6 bottom-6 w-0.5 bg-stone-100 -z-0" />
          <MotionDiv
              className="absolute left-[21px] top-6 w-0.5 bg-rose-500 shadow-[0_0_10px_rgba(225,29,72,0.5)]"
              style={{ height: `${progressPercentage}%` }}
          />
          {sections.map((section, idx) => {
            const isUnlocked = idx <= unlockedSection;
            const isActive = idx === activeSection;
            const isCompleted = idx < unlockedSection;
            return (
              <button key={section.id} disabled={!isUnlocked} onClick={() => handleJumpToSection(idx)} className={`relative z-10 w-full flex items-center gap-4 p-3 rounded-xl transition-all duration-500 text-left group ${isActive ? 'bg-rose-50 shadow-sm translate-x-2' : ''} ${!isUnlocked ? 'opacity-40 grayscale cursor-not-allowed' : 'hover:bg-stone-50'}`}>
                <MotionDiv className={`w-11 h-11 rounded-xl flex items-center justify-center shrink-0 border-2 transition-all duration-500 ${isCompleted ? 'bg-rose-600 border-rose-600 text-white shadow-lg' : isActive ? 'bg-white border-rose-500 text-rose-600 shadow-xl rotate-12' : 'bg-white border-stone-200 text-stone-300'}`}>
                   {isCompleted ? <CheckCircle2 size={18} /> : isActive ? <section.icon size={18} /> : <Lock size={16} />}
                </MotionDiv>
                <div className="flex-grow"><p className={`text-[8px] font-black uppercase tracking-widest ${isActive ? 'text-rose-500' : 'text-stone-400'}`}>{section.eyebrow.split('// ')[1]}</p><h4 className={`text-xs font-bold leading-tight ${isActive ? 'text-stone-900' : 'text-stone-500'}`}>{section.title}</h4></div>
              </button>
            );
          })}
        </div>

        <div className="mt-8 border-t border-stone-100 pt-8 flex flex-col items-center">
           <ActivityRing progress={progressPercentage} color="#e11d48" /><p className="text-[11px] font-black text-stone-900 uppercase tracking-widest text-center">Progress</p>
        </div>
      </aside>

      <main className="flex-grow flex flex-col items-center py-10 md:py-24 px-6 md:px-16 overflow-y-auto h-screen relative">
        <div className="absolute inset-0 bg-[radial-gradient(#e5e7eb_1px,transparent_1px)] [background-size:32px_32px] opacity-40 pointer-events-none" />
        <div className="w-full max-w-4xl relative z-10">
          <AnimatePresence mode="wait">
            <MotionDiv key={activeSection} initial={{ opacity: 0, x: 20 }} animate={{ opacity: 1, x: 0 }} exit={{ opacity: 0, x: -20 }} transition={{ duration: 0.6, ease: [0.16, 1, 0.3, 1] }}>
              {activeSection === 0 && (
                <ReadingSection title="The Belief Barrier." eyebrow="Step 1" icon={Brain}>
                  <p>Let's get one thing straight: the biggest barrier to your success isn't a lack of talent. It's a lack of belief. In psychology, this core belief in your own ability is called <Highlight description="The conviction that you have the power to organize and execute the actions needed to get things done. It's not about having the skill; it's about believing you can use it.">Self-Efficacy</Highlight>. It's the engine that drives effort, persistence, and resilience.</p>
                  <p>Think of it like this: a car might have a full tank of petrol (your knowledge and skills), but if the driver doesn't believe they can actually drive, the car is going nowhere. For students from tough backgrounds, society often spends years convincing you that you don't belong in the driver's seat. This module is about grabbing the keys.</p>
                </ReadingSection>
              )}
              {activeSection === 1 && (
                <ReadingSection title="How Belief is Built." eyebrow="Step 2" icon={Target}>
                    <p>So where does this belief come from? It's not magic. The science shows it comes from four main sources. Understanding them is like having the user manual for your own brain.</p>
                    <p>The four sources are: 1) <Highlight description="The most powerful source of self-efficacy, built from your own direct successes and personal victories, no matter how small.">Enactive Mastery</Highlight> (your own wins), 2) <Highlight description="Building your belief by watching someone *similar to you* succeed. It's the 'if they can do it, I can do it' effect.">Vicarious Experience</Highlight> (watching others win), 3) Social Persuasion (real encouragement), and 4) Physiological States (learning to read your body's signals). For students who haven't had a long history of easy wins, the second source—Vicarious Experience—is the most important lever we can pull.</p>
                </ReadingSection>
              )}
              {activeSection === 2 && (
                <ReadingSection title="The Role Model Myth." eyebrow="Step 3" icon={Shield}>
                  <p>We're often told to look up to flawless heroes—the sporting legend, the genius scientist. These are <Highlight description="Flawless, high-prestige role models who seem to succeed without effort. They can be inspiring, but often make success feel unattainable.">Mastery Models</Highlight>. But research shows they can actually *lower* your self-efficacy. Why? Because their success seems so effortless and distant that it creates a "capability gap" that feels impossible to cross.</p>
                  <p>The solution is to find <Highlight description="Relatable role models who openly struggle, make mistakes, and show how they recover. Watching them is far more effective for building self-belief.">Coping Models</Highlight>. These are people who are relatable, who fail, and who show you *how* they get back up. The famous "Even Einstein Struggled" study proved that learning about a genius's failures is far more motivating than just hearing about their successes. It proves that struggle is part of the path, not a sign you're on the wrong one.</p>
                  <RoleModelSelector/>
                </ReadingSection>
              )}
               {activeSection === 3 && (
                <ReadingSection title="The Success Iceberg." eyebrow="Step 4" icon={Eye}>
                  <p>This brings us to the core idea of this entire module: you need to stop being a passive fan of success and start being an active detective of process. Success is like an iceberg. People only see the tip—the good grades, the confidence, the final result. They don't see the massive, messy reality underwater.</p>
                  <p>The underwater part is the process: the failures, the wrong turns, the doubt, the boring routines, the asking for help. To build your own self-efficacy, you need to become an expert at seeing this invisible part. You need to train your brain to look for the <Highlight description="The 'thinking about your thinking' skills that successful people use to plan, monitor, and adjust their strategies. It's the invisible part of their process.">Metacognitive Regulation</Highlight>—the small, strategic moves people make when they get stuck.</p>
                  <IcebergInteractive />
                </ReadingSection>
              )}
              {activeSection === 4 && (
                <ReadingSection title="The Habit Blueprint." eyebrow="Step 5" icon={Settings}>
                  <p>Once you start seeing the process, the final step is to translate it into your own life. This is about "reverse-engineering" a role model's success into a set of repeatable habits. The secret is to bypass willpower, which always runs out, by creating automatic systems.</p>
                  <p>There are two key tools for this. First, <Highlight description="A tiny version of a new habit that is so small it's almost impossible not to do. It's the secret to getting started when motivation is low.">Micro-Habits</Highlight>, which break a big action down into something tiny (e.g. "write 2,000 words" becomes "write 3 sentences"). Second, <Highlight description="A simple but powerful 'If-Then' plan that links a specific situation to a specific action, putting your good habits on autopilot.">Implementation Intentions</Highlight>, which create an "If-Then" plan that puts your micro-habit on autopilot (e.g. "IF I open my laptop, THEN I will write 3 sentences"). This is how you build a system for success, one tiny, automatic step at a time.</p>
                  <MicroCommitment>
                    <p>Take one big study goal you have. Now, what's the smallest possible version of it you could do in two minutes? (e.g., "Revise all of Chapter 3" becomes "Read the first paragraph of Chapter 3"). That's your micro-habit.</p>
                  </MicroCommitment>
                </ReadingSection>
              )}
              <footer className="mt-24 flex items-center justify-between pt-12 border-t border-stone-200/60 px-4">
                <MotionButton whileHover={{ scale: 1.05 }} whileTap={{ scale: 0.95 }} onClick={handlePrev} disabled={activeSection === 0} className={`flex items-center gap-4 bg-stone-100 text-stone-800 px-8 py-4 rounded-xl font-black text-[10px] uppercase tracking-widest transition-all shadow-sm ${activeSection === 0 ? 'opacity-0 pointer-events-none' : ''}`}>
                  <ArrowLeft size={16} /> Prev
                </MotionButton>
                <MotionButton whileHover={{ scale: 1.05 }} whileTap={{ scale: 0.95 }} onClick={handleCompleteSection} className="group relative flex items-center gap-4 bg-stone-900 text-white px-12 py-6 rounded-2xl font-black text-[12px] uppercase tracking-widest hover:bg-rose-600 transition-all shadow-[0_20px_50px_rgba(0,0,0,0.2)] overflow-hidden">
                  <span className="relative z-10">{activeSection === sections.length - 1 ? 'Finish Protocol' : 'Deploy Next Phase'}</span>
                  <ArrowRight size={18} className="relative z-10 group-hover:translate-x-2 transition-transform" />
                </MotionButton>
              </footer>
            </MotionDiv>
          </AnimatePresence>
        </div>
      </main>
    </div>
  );
};
