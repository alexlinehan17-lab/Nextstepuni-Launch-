
/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
*/

import React, { useState } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { 
  ArrowLeft, CheckCircle2, ArrowRight, 
  Lock, Flag, MessageCircle, BarChart, Brain, User, Settings, AlertTriangle
} from 'lucide-react';

interface ThePraiseProtocolModuleProps {
  onBack: () => void;
}

const Highlight = ({ children, description, color = "bg-lime-100/40", textColor = "text-lime-900", decorColor = "decoration-lime-400/40", hoverColor="hover:bg-lime-200/60" }: { children?: React.ReactNode, description: string, color?: string, textColor?: string, decorColor?: string, hoverColor?: string }) => {
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
              <p className="font-sans font-bold text-lime-400 mb-2 uppercase tracking-[0.2em] text-[9px]">The Academic Insight</p>
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
        <div className="w-12 h-12 rounded-2xl bg-stone-900 flex items-center justify-center text-lime-400 shadow-xl border border-white/10">
          <Icon size={24} />
        </div>
      </div>
      <span className="inline-flex items-center gap-2 px-3 py-1 bg-lime-50 text-lime-600 text-[10px] font-black tracking-[0.4em] uppercase rounded-full mb-4">
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
  <div className="my-12 p-8 bg-lime-50/50 border-2 border-dashed border-lime-200 rounded-3xl">
    <div className="flex items-start gap-5">
      <div className="w-11 h-11 rounded-xl bg-lime-500 text-white flex items-center justify-center shrink-0 mt-1 shadow-lg shadow-lime-500/20">
        <Flag size={20} />
      </div>
      <div>
        <h4 className="font-bold text-lime-800 text-sm uppercase tracking-widest">Your Mission (Under 5 Mins)</h4>
        <div className="text-stone-600 mt-2 font-medium leading-relaxed">
          {children}
        </div>
      </div>
    </div>
  </div>
);

const ActivityRing = ({ progress, color = "#65a30d" }: { progress: number, color?: string }) => {
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

const DweckExperimentSimulator = () => {
    const [step, setStep] = useState(0); // 0: Start, 1: Praise Choice, 2: Task Choice, 3: Failure, 4: Result
    const [praiseType, setPraiseType] = useState<'person'|'process'|null>(null);
    const [taskChoice, setTaskChoice] = useState<'easy'|'hard'|null>(null);

    const reset = () => {
        setStep(0);
        setPraiseType(null);
        setTaskChoice(null);
    };

    const handlePraise = (type: 'person'|'process') => {
        setPraiseType(type);
        setStep(1);
    };

    const handleTask = (type: 'easy'|'hard') => {
        setTaskChoice(type);
        setStep(2);
        setTimeout(() => setStep(3), 2000); // Auto-advance to failure
        setTimeout(() => setStep(4), 4000); // Auto-advance to result
    };
    
    let resilience = 50, performance = 50;
    if(praiseType === 'person'){
        if(taskChoice === 'easy') { resilience = 20; performance = 40; }
        if(taskChoice === 'hard') { resilience = 30; performance = 30; }
    }
    if(praiseType === 'process'){
        if(taskChoice === 'easy') { resilience = 70; performance = 60; }
        if(taskChoice === 'hard') { resilience = 90; performance = 80; }
    }


    return(
        <div className="my-10 p-8 md:p-12 bg-white rounded-[3rem] border border-stone-200 shadow-xl">
             <h4 className="font-serif text-2xl font-bold text-stone-800 text-center italic">The Dweck Experiment Simulator</h4>
             <p className="text-center text-sm text-stone-500 mb-8">You just aced a test. Now, walk through the experiment and see the consequences.</p>

             <div className="grid grid-cols-2 gap-6 mb-8">
                <div className="text-center">
                    <p className="font-bold text-sm text-rose-600 mb-2">Resilience Meter</p>
                    <div className="w-full h-4 bg-stone-100 rounded-full"><motion.div className="h-full bg-rose-500 rounded-full" initial={{width: "50%"}} animate={{width: `${resilience}%`}} /></div>
                </div>
                <div className="text-center">
                    <p className="font-bold text-sm text-lime-600 mb-2">Performance Meter</p>
                    <div className="w-full h-4 bg-stone-100 rounded-full"><motion.div className="h-full bg-lime-500 rounded-full" initial={{width: "50%"}} animate={{width: `${performance}%`}} /></div>
                </div>
            </div>

            <AnimatePresence mode="wait">
                <motion.div key={step} initial={{opacity:0, x:20}} animate={{opacity:1, x:0}} exit={{opacity:0, x:-20}} className="text-center">
                    {step === 0 && <>
                        <p className="font-bold mb-4">Phase 1: Choose your praise</p>
                        <div className="grid grid-cols-2 gap-4">
                            <button onClick={() => handlePraise('person')} className="p-4 bg-rose-50 border-2 border-rose-200 rounded-xl">"You must be smart at this."</button>
                            <button onClick={() => handlePraise('process')} className="p-4 bg-emerald-50 border-2 border-emerald-200 rounded-xl">"You must have worked hard at this."</button>
                        </div>
                    </>}
                    {step === 1 && <>
                        <p className="font-bold mb-4">Phase 2: Choose your next task</p>
                         <div className="grid grid-cols-2 gap-4">
                            <button onClick={() => handleTask('easy')} className="p-4 bg-stone-100 border-2 border-stone-200 rounded-xl">An easy one (to look smart)</button>
                            <button onClick={() => handleTask('hard')} className="p-4 bg-stone-100 border-2 border-stone-200 rounded-xl">A hard one (to learn more)</button>
                        </div>
                    </>}
                    {step === 2 && <p className="font-bold text-blue-600">You chose the <span className="underline">{taskChoice}</span> task...</p>}
                    {step === 3 && <p className="font-bold text-rose-600">Phase 3: Induced Failure. You are given a much harder test and perform poorly...</p>}
                    {step === 4 && <>
                        <p className="font-bold text-lime-600 mb-4">Phase 4: Final Results</p>
                        {praiseType === 'person' && <p>Because your identity was tied to being "smart", failure was devastating. Your resilience and subsequent performance dropped.</p>}
                        {praiseType === 'process' && <p>Because your identity was tied to "working hard", the failure was seen as a challenge. Your resilience and subsequent performance increased.</p>}
                        <button onClick={reset} className="mt-4 px-4 py-2 bg-stone-800 text-white font-bold rounded-lg text-xs">Run Again</button>
                    </>}
                </motion.div>
            </AnimatePresence>
        </div>
    );
};

const ErrorSignalVisualizer = () => {
    const [active, setActive] = useState(false);
    return(
        <div className="my-10 p-8 md:p-12 bg-white rounded-[3rem] border border-stone-200 shadow-xl">
             <h4 className="font-serif text-2xl font-bold text-stone-800 text-center italic">The Brain's Error Signal</h4>
             <p className="text-center text-sm text-stone-500 mb-8">When you make a mistake, your brain sends two signals. The second signal (Pe) is where the magic happens.</p>
             <div className="grid grid-cols-2 gap-6">
                <div className="text-center">
                    <h5 className="font-bold mb-2">Fixed Mindset Brain</h5>
                    <svg viewBox="0 0 100 50" className="w-full h-auto">
                       <path d="M0 25 L 20 25 C 25 25 28 10 32 10 S 37 40 40 40 L 100 40" stroke="#f43f5e" strokeWidth="2" fill="none" />
                       <AnimatePresence>
                       {active && <motion.path initial={{pathLength:0}} animate={{pathLength:1}} exit={{pathLength:0}} d="M 40 40 C 45 40 48 30 52 30 S 57 40 60 40" stroke="#f43f5e" strokeWidth="1" fill="none" />}
                       </AnimatePresence>
                    </svg>
                    <p className="text-xs text-stone-500 mt-2">A small "Pe" signal. The brain notices the error but quickly "looks away" to protect the ego.</p>
                </div>
                 <div className="text-center">
                    <h5 className="font-bold mb-2">Growth Mindset Brain</h5>
                    <svg viewBox="0 0 100 50" className="w-full h-auto">
                        <path d="M0 25 L 20 25 C 25 25 28 10 32 10 S 37 40 40 40 L 100 40" stroke="#10b981" strokeWidth="2" fill="none" />
                       <AnimatePresence>
                       {active && <motion.path initial={{pathLength:0}} animate={{pathLength:1}} exit={{pathLength:0}} d="M 40 40 C 45 40 48 5 52 5 S 57 40 60 40" stroke="#10b981" strokeWidth="3" fill="none" />}
                       </AnimatePresence>
                    </svg>
                    <p className="text-xs text-stone-500 mt-2">A large "Pe" signal. The brain allocates massive attention to the error, analysing it to learn from it.</p>
                </div>
             </div>
             <div className="text-center mt-8">
                <button onClick={() => setActive(!active)} className="px-5 py-3 bg-stone-800 text-white font-bold rounded-lg text-sm">{active ? "Reset Signal" : "Make an Error"}</button>
             </div>
        </div>
    );
};


// --- MODULE COMPONENT ---
export const ThePraiseProtocolModule: React.FC<ThePraiseProtocolModuleProps> = ({ onBack }) => {
  const [activeSection, setActiveSection] = useState(0);
  const [unlockedSection, setUnlockedSection] = useState(0);
  
  const sections = [
    { id: 'praise-paradox', title: 'The Praise Paradox', eyebrow: '01 // The Framing Device', icon: MessageCircle },
    { id: 'dweck-experiment', title: 'The Dweck Experiment', eyebrow: '02 // The Evidence', icon: BarChart },
    { id: 'brain-on-praise', title: 'The Brain on Praise', eyebrow: '03 // The Neurobiology', icon: Brain },
    { id: 'real-world-data', title: 'The Real World Data', eyebrow: '04 // The Gender Gap', icon: User },
    { id: 'false-growth', title: 'The "Effort" Trap', eyebrow: '05 // False Growth Mindset', icon: AlertTriangle },
    { id: 'feedback-audit', title: 'The Feedback Audit', eyebrow: '06 // Your Action Plan', icon: Settings },
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
            <p className="text-[9px] font-black text-lime-500 uppercase tracking-[0.4em] mb-0.5 underline">Module 03</p>
            <h1 className="font-serif font-bold text-lg tracking-tight text-stone-900">The Praise Protocol</h1>
          </div>
        </div>

        <div className="flex-grow space-y-4 overflow-y-auto no-scrollbar pr-2 relative">
          <div className="absolute left-[21px] top-6 bottom-6 w-0.5 bg-stone-100 -z-0" />
          <div className="absolute left-[21px] top-6 bottom-6 w-0.5">
              <motion.div
                  className="w-full bg-lime-500 shadow-[0_0_10px_rgba(101,163,13,0.5)]"
                  initial={{ height: 0 }}
                  animate={{ height: sections.length > 1 ? `${(unlockedSection / (sections.length - 1)) * 100}%` : '0%' }}
              />
          </div>
          {sections.map((section, idx) => {
            const isUnlocked = idx <= unlockedSection;
            const isActive = idx === activeSection;
            const isCompleted = idx < unlockedSection;
            return (
              <button key={section.id} disabled={!isUnlocked} onClick={() => handleJumpToSection(idx)} className={`relative z-10 w-full flex items-center gap-4 p-3 rounded-xl transition-all duration-500 text-left group ${isActive ? 'bg-lime-50 shadow-sm translate-x-2' : ''} ${!isUnlocked ? 'opacity-40 grayscale cursor-not-allowed' : 'hover:bg-stone-50'}`}>
                <div className={`w-11 h-11 rounded-xl flex items-center justify-center shrink-0 border-2 transition-all duration-500 ${isCompleted ? 'bg-lime-600 border-lime-600 text-white shadow-lg' : isActive ? 'bg-white border-lime-500 text-lime-600 shadow-xl rotate-12' : 'bg-white border-stone-200 text-stone-300'}`}>
                   {isCompleted ? <CheckCircle2 size={18} /> : isActive ? <section.icon size={18} /> : <Lock size={16} />}
                </div>
                <div className="flex-grow"><p className={`text-[8px] font-black uppercase tracking-widest ${isActive ? 'text-lime-500' : 'text-stone-400'}`}>{section.eyebrow.split('// ')[1]}</p><h4 className={`text-xs font-bold leading-tight ${isActive ? 'text-stone-900' : 'text-stone-500'}`}>{section.title}</h4></div>
              </button>
            );
          })}
        </div>

        <div className="mt-8 border-t border-stone-100 pt-8 flex flex-col items-center">
           <ActivityRing progress={progress} color="#65a30d" /><p className="text-[11px] font-black text-stone-900 uppercase tracking-widest text-center">Progress</p>
        </div>
      </aside>

      <main className="flex-grow flex flex-col items-center py-10 md:py-24 px-6 md:px-16 overflow-y-auto h-screen relative">
        <div className="absolute inset-0 bg-[radial-gradient(#e5e7eb_1px,transparent_1px)] [background-size:32px_32px] opacity-40 pointer-events-none" />
        <div className="w-full max-w-4xl relative z-10">
          <AnimatePresence mode="wait">
            <motion.div key={activeSection} initial={{ opacity: 0, x: 20 }} animate={{ opacity: 1, x: 0 }} exit={{ opacity: 0, x: -20 }} transition={{ duration: 0.6, ease: [0.16, 1, 0.3, 1] }}>
              {activeSection === 0 && (
                <ReadingSection title="The Praise Paradox." eyebrow="Step 1" icon={MessageCircle}>
                  <p>We've been told our whole lives that praise builds confidence. But what if some types of praise are actually a psychological trap? This is the praise paradox. The words you hear—and the words you tell yourself—are not just encouragement; they are framing devices that program your brain's entire approach to success and failure.</p>
                  <p>The science, pioneered by Carol Dweck, splits praise into two categories. <Highlight description="Praise that focuses on innate, fixed traits like 'You're so smart' or 'You're a natural'. This praise is dangerous because it creates a Fixed Mindset.">Person Praise</Highlight> focuses on who you *are*. <Highlight description="Praise that focuses on controllable, unstable variables like effort, strategy, and process. E.g., 'You worked so hard on that.' This praise is powerful because it builds a Growth Mindset.">Process Praise</Highlight> focuses on what you *do*. One builds fragility, the other builds resilience. Understanding the difference is mission-critical.</p>
                </ReadingSection>
              )}
               {activeSection === 1 && (
                <ReadingSection title="The Dweck Experiment." eyebrow="Step 2" icon={BarChart}>
                    <p>In a groundbreaking 1998 study, Mueller and Dweck revealed the immediate, devastating impact of person praise. They gave students a test, told them all they did well, and then gave them one of two sentences of praise: "You must be smart" (Person) or "You must have worked hard" (Process).</p>
                    <p>The results were shocking. The "smart" kids immediately became risk-averse, choosing easier tasks to protect their new label. When faced with a harder problem and failing, they gave up, their performance collapsed, and nearly 40% of them lied about their scores. The "hard-working" kids did the opposite: they sought out challenges, enjoyed the struggle, improved their performance after failure, and were three times more honest. Let's run the simulation.</p>
                    <DweckExperimentSimulator />
                </ReadingSection>
              )}
               {activeSection === 2 && (
                <ReadingSection title="The Brain on Praise." eyebrow="Step 3" icon={Brain}>
                  <p>Why is the effect so dramatic? Because person and process praise engage different neural circuits. Praise is a social reward that triggers <Highlight description="The 'motivation molecule.' It's a neurotransmitter that drives your desire to pursue rewards.">dopamine</Highlight>. Process praise links that dopamine hit to the *action of effort*, effectively gamifying struggle and making you want to do it more. Person praise links dopamine to a *static identity*, making any failure a threat that causes a dopamine crash.</p>
                  <p>Even more powerfully, EEG studies show that when we make a mistake, our brains generate an error signal (the "Pe wave"). In a <Highlight description="The belief that intelligence is a fixed trait. People with this mindset see failure as a verdict on their innate ability.">Fixed Mindset</Highlight>, the Pe signal is tiny—the brain literally "looks away" from the mistake to protect its ego. In a <Highlight description="The belief that intelligence can be grown. People with this mindset see failure as an opportunity to learn and improve.">Growth Mindset</Highlight>, the Pe signal is huge—the brain allocates massive attentional resources to the error, desperate to learn from it.</p>
                  <ErrorSignalVisualizer />
                </ReadingSection>
              )}
              {activeSection === 3 && (
                <ReadingSection title="The Real World Data." eyebrow="Step 4" icon={User}>
                  <p>This isn't just a lab finding. A landmark longitudinal study tracked families from when their children were toddlers until they were in 4th class. It found that the *percentage* of process praise parents used (which was, on average, a tiny 18%) directly predicted whether their child would have a growth mindset five years later. More process praise led to a stronger growth mindset, which in turn led to higher achievement in Maths and English.</p>
                  <p>The study also uncovered a stark gender gap. From as young as 14 months, boys tended to receive significantly more process praise ("You built that tower so high!"), while girls were more likely to be praised for their traits ("You're such a good girl"). This early linguistic conditioning provides a powerful explanation for why high-achieving girls can be more vulnerable to developing a fixed mindset later on.</p>
                </ReadingSection>
              )}
              {activeSection === 4 && (
                <ReadingSection title="The 'Effort' Trap." eyebrow="Step 5" icon={AlertTriangle}>
                    <p>As these ideas became popular, a "False Growth Mindset" began to emerge. The most common error is equating a growth mindset with simply praising effort. Imagine a student fails a test after studying hard, and the teacher says, "Don't worry, you tried your best!" This is <Highlight description="Praise for effort that is disconnected from outcome. It's often used as a consolation prize and can signal that a person has reached the limit of their ability.">Consolation Praise</Highlight>, and it's toxic. It sends the message: "Your best isn't good enough, and there's nothing more you can do."</p>
                    <p>Effective process praise must be strategic. It links effort to *outcome* and *strategy*. A better response would be: "I can see you worked hard, but the study method you used didn't work. Let's look at your mistakes and find a new strategy." Effort is a vector, not a scalar; it must be pointed in the right direction.</p>
                </ReadingSection>
              )}
               {activeSection === 5 && (
                <ReadingSection title="The Feedback Audit." eyebrow="Step 6" icon={Settings}>
                  <p>To install a Growth Mindset OS, you need to become a detective of the feedback in your environment—from teachers, family, and especially your own self-talk. The "Feedback Audit" is a tool to measure your current reality. For one day, listen for praise and categorise it. Is it Person, Process, or just Outcome-based ("Good job")?</p>
                  <MicroCommitment>
                    <p>Tonight, when you're reviewing your day, think of one piece of feedback you received (from yourself or others). Was it Person or Process praise? Just noticing is the first step.</p>
                  </MicroCommitment>
                </ReadingSection>
              )}
              <footer className="mt-24 flex items-center justify-between pt-12 border-t border-stone-200/60 px-4">
                <motion.button whileHover={{ scale: 1.05 }} whileTap={{ scale: 0.95 }} onClick={handlePrev} disabled={activeSection === 0} className={`flex items-center gap-4 bg-stone-100 text-stone-800 px-8 py-4 rounded-xl font-black text-[10px] uppercase tracking-widest transition-all shadow-sm ${activeSection === 0 ? 'opacity-0 pointer-events-none' : ''}`}>
                  <ArrowLeft size={16} /> Prev
                </motion.button>
                <motion.button whileHover={{ scale: 1.05 }} whileTap={{ scale: 0.95 }} onClick={handleCompleteSection} className="group relative flex items-center gap-4 bg-stone-900 text-white px-12 py-6 rounded-2xl font-black text-[12px] uppercase tracking-widest hover:bg-lime-600 transition-all shadow-[0_20px_50px_rgba(0,0,0,0.2)] overflow-hidden">
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
