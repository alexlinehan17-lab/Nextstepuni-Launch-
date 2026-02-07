
/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
*/

import React, { useState } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { 
  ArrowLeft, CheckCircle2, ArrowRight, 
  Lock, Flag, Cpu, ClipboardList, ListFilter, PlayCircle, BarChart2, HeartPulse, HardHat
} from 'lucide-react';

interface ExamHallStrategiesModuleProps {
  onBack: () => void;
}

const Highlight = ({ children, description, color = "bg-amber-100/40", textColor = "text-amber-900", decorColor = "decoration-amber-400/40", hoverColor="hover:bg-amber-200/60" }: { children?: React.ReactNode, description: string, color?: string, textColor?: string, decorColor?: string, hoverColor?: string }) => {
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
              <p className="font-sans font-bold text-amber-400 mb-2 uppercase tracking-[0.2em] text-[9px]">The Academic Insight</p>
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
        <div className="w-12 h-12 rounded-2xl bg-stone-900 flex items-center justify-center text-amber-400 shadow-xl border border-white/10">
          <Icon size={24} />
        </div>
      </div>
      <span className="inline-flex items-center gap-2 px-3 py-1 bg-amber-50 text-amber-600 text-[10px] font-black tracking-[0.4em] uppercase rounded-full mb-4">
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
  <div className="my-12 p-8 bg-amber-50/50 border-2 border-dashed border-amber-200 rounded-3xl">
    <div className="flex items-start gap-5">
      <div className="w-11 h-11 rounded-xl bg-amber-500 text-white flex items-center justify-center shrink-0 mt-1 shadow-lg shadow-amber-500/20">
        <Flag size={20} />
      </div>
      <div>
        <h4 className="font-bold text-amber-800 text-sm uppercase tracking-widest">Your Mission (Under 5 Mins)</h4>
        <div className="text-stone-600 mt-2 font-medium leading-relaxed">
          {children}
        </div>
      </div>
    </div>
  </div>
);

const ActivityRing = ({ progress, color = "#f59e0b" }: { progress: number, color?: string }) => {
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
const TriageSimulator = () => {
    const questions = [
        { id: 1, text: "A 'Describe' question on a topic you know well.", difficulty: 'green' },
        { id: 2, text: "An 'Evaluate' question that requires a long essay plan.", difficulty: 'amber' },
        { id: 3, text: "A multi-step maths problem on a topic you're weak on.", difficulty: 'red' },
    ];
    const [qIndex, setQIndex] = useState(0);
    const [choices, setChoices] = useState<(string|null)[]>(Array(questions.length).fill(null));

    const handleChoice = (choice: string) => {
        const newChoices = [...choices];
        newChoices[qIndex] = choice;
        setChoices(newChoices);
        setTimeout(() => setQIndex(q => Math.min(q + 1, questions.length)), 1000);
    };

    if (qIndex >= questions.length) {
        return (
            <div className="my-10 p-8 md:p-12 bg-white rounded-[3rem] border border-stone-200 shadow-xl text-center">
                <h4 className="font-serif text-2xl font-bold text-stone-800 text-center italic">Triage Complete</h4>
                <button onClick={() => {setQIndex(0); setChoices(Array(questions.length).fill(null));}} className="mt-4 px-4 py-2 bg-amber-500 text-white font-bold text-sm rounded-lg">Run Drill Again</button>
            </div>
        );
    }
    
    return(
        <div className="my-10 p-8 md:p-12 bg-white rounded-[3rem] border border-stone-200 shadow-xl">
            <h4 className="font-serif text-2xl font-bold text-stone-800 text-center italic">Triage Drill</h4>
            <p className="text-center text-sm text-stone-500 mb-8">Reading time has started. Quickly categorize this question.</p>
            <AnimatePresence mode="wait">
            <motion.div key={qIndex} initial={{opacity:0, x:20}} animate={{opacity:1, x:0}} exit={{opacity:0, x:-20}} className="p-6 bg-stone-100 border border-stone-200 rounded-2xl text-center font-bold text-stone-700 min-h-[100px] flex items-center justify-center">
                {questions[qIndex].text}
            </motion.div>
            </AnimatePresence>
            <div className="grid grid-cols-3 gap-3 mt-6">
                <button onClick={() => handleChoice('green')} className="p-4 bg-emerald-100 text-emerald-800 font-bold rounded-xl border-2 border-emerald-200 hover:border-emerald-400">Green</button>
                <button onClick={() => handleChoice('amber')} className="p-4 bg-amber-100 text-amber-800 font-bold rounded-xl border-2 border-amber-200 hover:border-amber-400">Amber</button>
                <button onClick={() => handleChoice('red')} className="p-4 bg-rose-100 text-rose-800 font-bold rounded-xl border-2 border-rose-200 hover:border-rose-400">Red</button>
            </div>
        </div>
    )
}

const MPMCalculator = () => {
    const [time, setTime] = useState(180);
    const [marks, setMarks] = useState(100);
    const [buffer, setBuffer] = useState(15);
    const mpm = (time - buffer) / marks;

    return (
        <div className="my-10 p-8 md:p-12 bg-white rounded-[3rem] border border-stone-200 shadow-xl">
             <h4 className="font-serif text-2xl font-bold text-stone-800 text-center italic">Minutes-Per-Mark (MPM) Calculator</h4>
             <div className="grid grid-cols-3 gap-4 mt-6">
                <div><label className="text-xs font-bold">Total Time (mins)</label><input type="number" value={time} onChange={e=>setTime(parseInt(e.target.value))} className="w-full p-2 bg-stone-100 rounded-md" /></div>
                <div><label className="text-xs font-bold">Total Marks</label><input type="number" value={marks} onChange={e=>setMarks(parseInt(e.target.value))} className="w-full p-2 bg-stone-100 rounded-md" /></div>
                <div><label className="text-xs font-bold">Buffer (mins)</label><input type="number" value={buffer} onChange={e=>setBuffer(parseInt(e.target.value))} className="w-full p-2 bg-stone-100 rounded-md" /></div>
             </div>
             <div className="mt-6 p-4 bg-stone-900 rounded-xl text-center text-white">
                Your MPM is <span className="font-bold text-2xl text-amber-400">{mpm.toFixed(2)}</span>. A 20-mark question gets <span className="font-bold text-amber-400">{(mpm*20).toFixed(1)}</span> minutes.
             </div>
        </div>
    )
}

const BoxBreathingVisualizer = () => {
    const steps = ["Inhale...", "Hold...", "Exhale...", "Hold..."];
    return (
        <div className="my-10 p-8 md:p-12 bg-white rounded-[3rem] border border-stone-200 shadow-xl flex flex-col items-center">
             <h4 className="font-serif text-2xl font-bold text-stone-800 text-center italic">4-4-4-4 Box Breathing</h4>
             <p className="text-center text-sm text-stone-500 mb-8">Feeling panicked? Run this protocol.</p>
             <div className="w-32 h-32 relative flex items-center justify-center">
                <motion.div 
                    className="w-full h-full border-4 border-stone-200 rounded-lg"
                    animate={{ rotate: [0, 90, 180, 270, 360] }}
                    transition={{ duration: 16, repeat: Infinity, ease: 'linear' }}
                />
                 <motion.div 
                    className="absolute w-4 h-4 bg-amber-500 rounded-full"
                    style={{ top: '-8px', left: '50%', x: '-50%'}}
                    animate={{ 
                        x: ['-50%', '-50%', 'calc(-50% + 64px)', 'calc(-50% + 64px)', 'calc(-50% - 64px)', 'calc(-50% - 64px)', '-50%', '-50%'],
                        y: [0, '128px', '128px', 0, 0, '128px', '128px', 0],
                    }}
                    transition={{ duration: 16, repeat: Infinity, ease: 'linear', times: [0, 0.25, 0.25, 0.5, 0.5, 0.75, 0.75, 1]}}
                />
                 <AnimatePresence mode="wait">
                    <motion.p 
                        key={Math.floor(Date.now() / 4000) % 4}
                        className="absolute font-bold"
                        initial={{ opacity: 0 }}
                        animate={{ opacity: 1 }}
                        exit={{ opacity: 0 }}
                        transition={{ duration: 0.5 }}
                    >
                        {steps[Math.floor(Date.now() / 4000) % 4]}
                    </motion.p>
                 </AnimatePresence>
             </div>
        </div>
    );
}

// --- MODULE COMPONENT ---
export const ExamHallStrategiesModule: React.FC<ExamHallStrategiesModuleProps> = ({ onBack }) => {
  const [activeSection, setActiveSection] = useState(0);
  const [unlockedSection, setUnlockedSection] = useState(0);
  
  const sections = [
    { id: 'execution-gap', title: 'The Execution Gap', eyebrow: '01 // The Problem', icon: Cpu },
    { id: 'cognitive-offloading', title: 'Cognitive Offloading', eyebrow: '02 // The Dump Sheet', icon: ClipboardList },
    { id: 'tactical-triage', title: 'Tactical Triage', eyebrow: '03 // Reading Time Strategy', icon: ListFilter },
    { id: 'order-of-attack', title: 'Order of Attack', eyebrow: '04 // The Momentum Principle', icon: PlayCircle },
    { id: 'exam-economics', title: 'Exam Economics', eyebrow: '05 // Strict Time Budgeting', icon: BarChart2 },
    { id: 'anxiety-regulation', title: 'Anxiety Regulation', eyebrow: '06 // Physiological Management', icon: HeartPulse },
    { id: 'post-exam-training', title: 'Post-Exam Training', eyebrow: '07 // The Drills', icon: HardHat },
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
            <p className="text-[9px] font-black text-amber-500 uppercase tracking-[0.4em] mb-0.5 underline">Module 03</p>
            <h1 className="font-serif font-bold text-lg tracking-tight text-stone-900">Exam Hall Strategies</h1>
          </div>
        </div>

        <div className="flex-grow space-y-4 overflow-y-auto no-scrollbar pr-2 relative">
          <div className="absolute left-[21px] top-6 bottom-6 w-0.5 bg-stone-100 -z-0" />
          <div className="absolute left-[21px] top-6 bottom-6 w-0.5">
              <motion.div
                  className="w-full bg-amber-500 shadow-[0_0_10px_rgba(245,158,11,0.5)]"
                  initial={{ height: 0 }}
                  animate={{ height: sections.length > 1 ? `${(unlockedSection / (sections.length - 1)) * 100}%` : '0%' }}
              />
          </div>
          {sections.map((section, idx) => {
            const isUnlocked = idx <= unlockedSection;
            const isActive = idx === activeSection;
            const isCompleted = idx < unlockedSection;
            return (
              <button key={section.id} disabled={!isUnlocked} onClick={() => handleJumpToSection(idx)} className={`relative z-10 w-full flex items-center gap-4 p-3 rounded-xl transition-all duration-500 text-left group ${isActive ? 'bg-amber-50 shadow-sm translate-x-2' : ''} ${!isUnlocked ? 'opacity-40 grayscale cursor-not-allowed' : 'hover:bg-stone-50'}`}>
                <div className={`w-11 h-11 rounded-xl flex items-center justify-center shrink-0 border-2 transition-all duration-500 ${isCompleted ? 'bg-amber-600 border-amber-600 text-white shadow-lg' : isActive ? 'bg-white border-amber-500 text-amber-600 shadow-xl rotate-12' : 'bg-white border-stone-200 text-stone-300'}`}>
                   {isCompleted ? <CheckCircle2 size={18} /> : isActive ? <section.icon size={18} /> : <Lock size={16} />}
                </div>
                <div className="flex-grow"><p className={`text-[8px] font-black uppercase tracking-widest ${isActive ? 'text-amber-500' : 'text-stone-400'}`}>{section.eyebrow.split('// ')[1]}</p><h4 className={`text-xs font-bold leading-tight ${isActive ? 'text-stone-900' : 'text-stone-500'}`}>{section.title}</h4></div>
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
                <ReadingSection title="The Execution Gap." eyebrow="Step 1" icon={Cpu}>
                  <p>You can be the smartest person in the room, have every definition memorized, and still get a bad result. The gap between what you know (<Highlight description="What you have learned and stored in your long-term memory over months of study.">Competence</Highlight>) and what you can actually do on the day (<Highlight description="What you can retrieve and apply from your memory under the intense pressure of a timed exam.">Performance</Highlight>) is called the **Execution Gap**. This module is about closing that gap.</p>
                  <p>The exam hall is not a library for quiet recall; it's a high-pressure, resource-management game. The pressure adds <Highlight description="The 'bad' mental workload that comes from things other than the question itself, like managing your panic, checking the clock, or trying to remember a formula.">Extraneous Cognitive Load</Highlight> to your brain, stealing the limited mental bandwidth you need for the actual questions. The strategies in this module are about minimizing that load so you can show what you really know.</p>
                </ReadingSection>
              )}
               {activeSection === 1 && (
                <ReadingSection title="Cognitive Offloading." eyebrow="Step 2" icon={ClipboardList}>
                  <p>In the first few minutes of an exam, your stress hormones spike, which can block access to your memory. The <Highlight description="A pre-memorized sheet of high-yield, high-volatility information that you write down from memory at the very start of the exam before you even look at the questions.">"Dump Sheet"</Highlight> is a proactive strategy to combat this. It's about getting the most fragile, important information out of your head and onto paper before stress can erase it.</p>
                  <p>This isn't cheating; it's <Highlight description="The act of moving information from your limited biological working memory to a physical resource (like paper), freeing up mental capacity to focus on problem-solving.">Cognitive Offloading</Highlight>. The sheet should contain "High-Yield, High-Volatility" information: things that are easy to forget under pressure but are likely to be useful (e.g., key quotes, formulas, dates, acronyms). You must rehearse writing it until it's a 3-minute automatic motor skill.</p>
                </ReadingSection>
              )}
               {activeSection === 2 && (
                <ReadingSection title="Tactical Triage." eyebrow="Step 3" icon={ListFilter}>
                  <p>Reading time is not for passively reading. It's for <Highlight description="An active process during reading time where you scan the entire paper and sort questions into categories of difficulty, like a medic at a disaster scene.">Tactical Triage</Highlight>. Just like in an emergency room, your goal isn't to save every "patient" (question) perfectly; it's to get the most marks possible with your limited time.</p>
                  <p>Use a **Traffic Light System**: **Green** questions are "low-hanging fruit" you're 100% confident you can answer quickly. **Amber** questions are ones you know how to do but will take time or complex calculation. **Red** questions are "time sinks"—topics you're weak on or don't immediately understand. Your first job is to find 2-3 "Green" questions to serve as your <Highlight description="The first easy questions you attempt, regardless of their position on the paper. They build confidence, calm your nerves, and create psychological momentum.">Anchor Questions</Highlight>.</p>
                  <TriageSimulator />
                </ReadingSection>
              )}
              {activeSection === 3 && (
                <ReadingSection title="Order of Attack." eyebrow="Step 4" icon={PlayCircle}>
                  <p>Starting at Question 1 is a rookie mistake. It gives control to the examiner, who may have put a difficult question first. You need to become a <Highlight description="A concept from cybersecurity where an attacker seeks the easiest path to breach a system. In an exam, you should act like one, seeking the easiest path to accumulate marks.">"Work-Averse Attacker"</Highlight>, extracting the maximum marks for the minimum effort. This means attacking the "Green" questions first, no matter where they are.</p>
                  <p>This builds <Highlight description="The psychological phenomenon where early success creates a virtuous cycle of confidence and dopamine release, improving focus and making subsequent harder tasks feel more manageable.">Psychological Momentum</Highlight>. If you can't figure out a question in 30 seconds (the "30-Second Rule"), skip it immediately. The <Highlight description="The subconscious mind continues to work on a problem even after you've moved on. When you return to the question later, the solution often appears 'obvious.'">Incubation Effect</Highlight> means your brain will keep working on it in the background.</p>
                </ReadingSection>
              )}
              {activeSection === 4 && (
                <ReadingSection title="Exam Economics." eyebrow="Step 5" icon={BarChart2}>
                  <p>Time is the currency of the exam hall. Every minute is an investment that must provide a return (marks). The core metric is <Highlight description="Your fundamental time budget, calculated by dividing the total time (minus a buffer) by the total marks. E.g., (180-15 mins) / 100 marks = 1.65 minutes per mark.">Minutes Per Mark (MPM)</Highlight>. This tells you exactly how long you can spend on any given question.</p>
                  <p>When your timer for a question goes off, you must execute a <Highlight description="The discipline of stopping work on a question immediately when its time budget expires, even if you are mid-sentence, to avoid the Sunk Cost Fallacy.">"Hard Stop."</Highlight> This is the hardest discipline to learn because of the <Highlight description="The cognitive bias to continue investing in a losing proposition (like a hard question) because of the resources (time) you have already spent. It's the number one cause of time mismanagement in exams.">Sunk Cost Fallacy</Highlight>. The first 5 minutes on a new question will always be more valuable than the last 5 minutes polishing an old one.</p>
                  <MPMCalculator/>
                </ReadingSection>
              )}
              {activeSection === 5 && (
                <ReadingSection title="Anxiety Regulation." eyebrow="Step 6" icon={HeartPulse}>
                  <p>When you hit a difficult question, your sympathetic nervous system can trigger a "Panic Spike," narrowing your focus and blocking access to your memory. You need a protocol to fight back. The fastest is <Highlight description="A breathing technique (4s inhale, 4s hold, 4s exhale, 4s hold) that forces your nervous system back into a calm 'rest and digest' state.">Box Breathing</Highlight>.</p>
                  <p>Another tool is the <Highlight description="A grounding technique where you name 3 things you see, 3 sounds you hear, and 3 body parts you can feel. It forces your brain to process sensory data, disengaging the emotional amygdala hijack.">3-3-3 Rule</Highlight> for grounding. Finally, use <Highlight description="Changing your internal story from catastrophic ('I'm failing') to procedural ('This is a Red question. This is part of the plan. I will flag it and move on.').">Cognitive Reframing</Highlight> to turn panic into a planned response.</p>
                  <BoxBreathingVisualizer />
                </ReadingSection>
              )}
              {activeSection === 6 && (
                <ReadingSection title="The Training Protocol." eyebrow="Step 7" icon={HardHat}>
                  <p>These strategies are skills. They must be trained. After every practice test, you must use an <Highlight description="A post-exam reflection tool that forces you to analyze your errors by process ('I misread the question,' 'I ran out of time') not just by content ('I didn't know the date').">Exam Wrapper</Highlight> to analyze your performance. Did your triage work? Did you stick to your time budget?</p>
                  <p>You must also run specific drills. **Triage Drills**: Give yourself 5 minutes with a past paper to *only* categorize questions as Green, Amber, or Red. **Dump Sprints**: Practice writing your dump sheet until it takes less than 3 minutes. **Hard Stop Drills**: Do questions with a strict timer and force yourself to stop when it rings. This builds the discipline you need to execute under pressure.</p>
                  <MicroCommitment><p>For your next practice test, do a full "Exam Wrapper" analysis afterwards. Don't just check the answers; analyze *how* you took the test.</p></MicroCommitment>
                </ReadingSection>
              )}
              <footer className="mt-24 flex items-center justify-between pt-12 border-t border-stone-200/60 px-4">
                <motion.button whileHover={{ scale: 1.05 }} whileTap={{ scale: 0.95 }} onClick={handlePrev} disabled={activeSection === 0} className={`flex items-center gap-4 bg-stone-100 text-stone-800 px-8 py-4 rounded-xl font-black text-[10px] uppercase tracking-widest transition-all shadow-sm ${activeSection === 0 ? 'opacity-0 pointer-events-none' : ''}`}>
                  <ArrowLeft size={16} /> Prev
                </motion.button>
                <motion.button whileHover={{ scale: 1.05 }} whileTap={{ scale: 0.95 }} onClick={handleCompleteSection} className="group relative flex items-center gap-4 bg-stone-900 text-white px-12 py-6 rounded-2xl font-black text-[12px] uppercase tracking-widest hover:bg-amber-600 transition-all shadow-[0_20px_50px_rgba(0,0,0,0.2)] overflow-hidden">
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
