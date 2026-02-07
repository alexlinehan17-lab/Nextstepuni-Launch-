

/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
*/

import React, { useState, useEffect } from 'react';
import { motion, AnimatePresence, Reorder } from 'framer-motion';
import { 
  ArrowLeft, CheckCircle2, ArrowRight, 
  Lock, Flag, BrainCircuit, Shield, MessageSquare, BookOpen, Layers, Zap, Bus, Wrench
} from 'lucide-react';

type ModuleProgress = {
  unlockedSection: number;
};

interface CatastrophicThinkingModuleProps {
  onBack: () => void;
  progress: ModuleProgress;
  onProgressUpdate: (progress: ModuleProgress) => void;
}

const Highlight = ({ children, description, color = "bg-slate-100/40", textColor = "text-slate-900", decorColor = "decoration-slate-400/40", hoverColor="hover:bg-slate-200/60" }: { children?: React.ReactNode, description: string, color?: string, textColor?: string, decorColor?: string, hoverColor?: string }) => {
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
              <p className="font-sans font-bold text-slate-400 mb-2 uppercase tracking-[0.2em] text-[9px]">The Academic Insight</p>
              <p className="text-stone-200 font-medium">{description}</p>
            </motion.div>
          </>
        )}
      </AnimatePresence>
    </span>
  );
};

const ReadingSection = ({ title, eyebrow, icon: Icon, children }: { title: string, eyebrow: string, icon: any, children?: React.ReactNode }) => (
  <article className="animate-fade-in">
    <header className="mb-12 text-left relative">
      <div className="absolute -left-16 top-0 hidden xl:block">
        <div className="w-12 h-12 rounded-2xl bg-stone-900 flex items-center justify-center text-slate-400 shadow-xl border border-white/10">
          <Icon size={24} />
        </div>
      </div>
      <span className="inline-flex items-center gap-2 px-3 py-1 bg-slate-50 text-slate-600 text-[10px] font-black tracking-[0.4em] uppercase rounded-full mb-4">
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

const MicroCommitment = ({ children }: { children?: React.ReactNode }) => (
  <div className="my-12 p-8 bg-slate-50/50 border-2 border-dashed border-slate-200 rounded-3xl">
    <div className="flex items-start gap-5">
      <div className="w-11 h-11 rounded-xl bg-slate-500 text-white flex items-center justify-center shrink-0 mt-1 shadow-lg shadow-slate-500/20">
        <Flag size={20} />
      </div>
      <div>
        <h4 className="font-bold text-slate-800 text-sm uppercase tracking-widest">Your Mission (Under 5 Mins)</h4>
        <div className="text-stone-600 mt-2 font-medium leading-relaxed">
          {children}
        </div>
      </div>
    </div>
  </div>
);

const ActivityRing = ({ progress, color = "#64748b" }: { progress: number, color?: string }) => {
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

const ThoughtRecord = () => {
    const [step, setStep] = useState(0);
    const [record, setRecord] = useState({ situation: '', emotion: '', intensity: 90, nat: '', evidenceFor: '', evidenceAgainst: '', alternative: '', reRate: 50});
    const update = (field: string, value: any) => setRecord(prev => ({...prev, [field]: value}));
    
    const steps = ['Situation', 'Emotion', 'Negative Thought', 'Evidence For', 'Evidence Against', 'Alternative', 'Re-Rate'];

    return (
        <div className="my-10 p-8 md:p-12 bg-white rounded-[3rem] border border-stone-200 shadow-xl">
             <h4 className="font-serif text-2xl font-bold text-stone-800 text-center italic">The Thought Record</h4>
             <div className="flex justify-between my-4"><div className="w-full h-1 bg-stone-100 rounded-full"><motion.div className="h-1 bg-slate-500 rounded-full" animate={{width: `${(step / (steps.length - 1)) * 100}%`}}/></div></div>
             <AnimatePresence mode="wait">
             <motion.div key={step} initial={{opacity:0, x:20}} animate={{opacity:1, x:0}} exit={{opacity:0, x:-20}} >
                {step === 0 && <div><label className="font-bold">1. Situation:</label><input value={record.situation} onChange={e => update('situation', e.target.value)} placeholder="e.g., Sitting down to study History" className="w-full p-2 mt-2 bg-stone-50 rounded-lg"/></div>}
                {step === 1 && <div><label className="font-bold">2. Emotion:</label><input value={record.emotion} onChange={e => update('emotion', e.target.value)} placeholder="e.g., Panic" className="w-full p-2 mt-2 bg-stone-50 rounded-lg"/><label>Intensity: {record.intensity}%</label><input type="range" value={record.intensity} onChange={e => update('intensity', e.target.value)} className="w-full"/></div>}
                {step === 2 && <div><label className="font-bold">3. Negative Automatic Thought (NAT):</label><textarea value={record.nat} onChange={e => update('nat', e.target.value)} placeholder="e.g., I'll never remember all these dates." className="w-full p-2 mt-2 bg-stone-50 rounded-lg h-24"/></div>}
                {step === 3 && <div><label className="font-bold">4. Evidence For:</label><textarea value={record.evidenceFor} onChange={e => update('evidenceFor', e.target.value)} placeholder="e.g., I forgot the date of Clontarf yesterday." className="w-full p-2 mt-2 bg-stone-50 rounded-lg h-24"/></div>}
                {step === 4 && <div><label className="font-bold">5. Evidence Against:</label><textarea value={record.evidenceAgainst} onChange={e => update('evidenceAgainst', e.target.value)} placeholder="e.g., I passed my last test. I have 3 months to study." className="w-full p-2 mt-2 bg-stone-50 rounded-lg h-24"/></div>}
                {step === 5 && <div><label className="font-bold">6. Alternative Thought:</label><textarea value={record.alternative} onChange={e => update('alternative', e.target.value)} placeholder="e.g., History is hard, but if I use flashcards I can pass." className="w-full p-2 mt-2 bg-stone-50 rounded-lg h-24"/></div>}
                {step === 6 && <div><label className="font-bold">7. Re-Rate Emotion:</label><p>Initial Panic: {record.intensity}%</p><label>New Panic Level: {record.reRate}%</label><input type="range" value={record.reRate} onChange={e => update('reRate', e.target.value)} className="w-full"/></div>}
             </motion.div>
             </AnimatePresence>
             <div className="flex justify-between mt-4">
                <button onClick={() => setStep(s=>Math.max(0,s-1))} disabled={step===0} className="px-3 py-1 text-xs bg-stone-200 rounded-md disabled:opacity-50">Prev</button>
                <button onClick={() => setStep(s=>Math.min(steps.length-1,s+1))} disabled={step===steps.length-1} className="px-3 py-1 text-xs bg-stone-200 rounded-md disabled:opacity-50">Next</button>
             </div>
        </div>
    );
};

const GradedExposureHierarchy = () => {
    const [items, setItems] = useState([
        { id: 1, text: "Open Maths book (10 mins)", suds: 20 },
        { id: 2, text: "Read one past question", suds: 50 },
        { id: 3, text: "Attempt one question (timed)", suds: 80 },
    ]);
    return(
        <div className="my-10 p-8 md:p-12 bg-white rounded-[3rem] border border-stone-200 shadow-xl">
             <h4 className="font-serif text-2xl font-bold text-stone-800 text-center italic">Exposure Hierarchy Builder</h4>
             <Reorder.Group axis="y" values={items} onReorder={setItems} className="space-y-2 mt-6">
                {items.map(item => (
                    <Reorder.Item key={item.id} value={item} className="p-3 bg-stone-100 rounded-lg flex justify-between items-center cursor-grab active:cursor-grabbing">
                        <span>{item.text}</span>
                        <span className="font-bold text-sm text-rose-500">{item.suds} SUDS</span>
                    </Reorder.Item>
                ))}
             </Reorder.Group>
        </div>
    );
};

const PassengersOnBus = () => {
    const [busState, setBusState] = useState<'driving'|'stopped'>('driving');
    const [thought, setThought] = useState('');
    
    const thoughts = ["You're going to fail.", "You're not smart enough.", "Turn back now."];

    React.useEffect(() => {
        let interval: any;
        if(busState === 'driving') {
             interval = setInterval(() => {
                setThought(thoughts[Math.floor(Math.random() * thoughts.length)]);
                setTimeout(() => setThought(''), 1500);
            }, 3000);
        }
        return () => clearInterval(interval);
    }, [busState, thoughts]);

    return (
         <div className="my-10 p-8 md:p-12 bg-white rounded-[3rem] border border-stone-200 shadow-xl">
            <h4 className="font-serif text-2xl font-bold text-stone-800 text-center italic">Passengers on the Bus</h4>
             <div className="h-32 bg-stone-100 rounded-lg p-4 relative overflow-hidden">
                <motion.div className="absolute" animate={{x: busState === 'driving' ? '150%' : '50%'}} transition={{duration: busState === 'driving' ? 5 : 0.5}}><Bus size={48} className="text-slate-700"/></motion.div>
                {thought && <div className="absolute top-4 left-1/2 p-2 bg-white rounded-lg text-xs shadow-lg">{thought}</div>}
             </div>
             <div className="grid grid-cols-2 gap-4 mt-4">
                <button onClick={() => setBusState('stopped')} className="p-4 bg-rose-100 text-rose-800 rounded-xl">Argue with Passenger (Bus Stops)</button>
                <button onClick={() => setBusState('driving')} className="p-4 bg-emerald-100 text-emerald-800 rounded-xl">Acknowledge & Drive (Bus Moves)</button>
             </div>
        </div>
    );
}

// --- MODULE COMPONENT ---
export const CatastrophicThinkingModule: React.FC<CatastrophicThinkingModuleProps> = ({ onBack, progress, onProgressUpdate }) => {
  const [activeSection, setActiveSection] = useState(progress.unlockedSection);
  const unlockedSection = progress.unlockedSection;
  
  const sections = [
    { id: 'catastrophe-machine', title: 'The Catastrophe Machine', eyebrow: '01 // The Problem', icon: MessageSquare },
    { id: 'blank-mind', title: 'The Biology of "Blank Mind"', eyebrow: '02 // The Hardware', icon: BrainCircuit },
    { id: 'cbt-standard', title: 'The Gold Standard (CBT)', eyebrow: '03 // The Software', icon: BookOpen },
    { id: 'thought-record', title: 'The Thought Record', eyebrow: '04 // The Core Tool', icon: Wrench },
    { id: 'decatastrophize', title: 'Decatastrophizing', eyebrow: '05 // The "So What?" Drill', icon: Layers },
    { id: 'face-fear', title: 'Facing the Fear', eyebrow: '06 // Exposure', icon: Shield },
    { id: 'observer-self', title: 'The Observer Self (ACT)', eyebrow: '07 // The Alternative', icon: Zap },
    { id: 'action-plan', title: 'The Action Plan', eyebrow: '08 // The Blueprint', icon: Flag },
  ];
  
  useEffect(() => {
    setActiveSection(progress.unlockedSection);
  }, [progress.unlockedSection]);

  const handleCompleteSection = () => {
    if (activeSection === unlockedSection && unlockedSection < sections.length - 1) {
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

  const progressPercentage = sections.length > 1 ? (unlockedSection / (sections.length - 1)) * 100 : 0;

  return (
    <div className="min-h-screen bg-[#FBFBF9] text-stone-900 font-sans flex flex-col md:flex-row overflow-x-hidden">
      <aside className="w-full md:w-80 bg-white border-r border-stone-200 sticky top-0 md:h-screen z-40 p-8 flex flex-col">
        <div className="flex items-center gap-4 mb-12">
          <motion.button whileHover={{ scale: 1.05 }} whileTap={{ scale: 0.95 }} onClick={onBack} className="p-2 rounded-full transition-all border border-stone-200/50 shadow-sm bg-white">
            <ArrowLeft size={16} className="text-stone-700" />
          </motion.button>
          <div>
            <p className="text-[9px] font-black text-slate-500 uppercase tracking-[0.4em] mb-0.5 underline">Module 12</p>
            <h1 className="font-serif font-bold text-lg tracking-tight text-stone-900">Reframing Thoughts</h1>
          </div>
        </div>

        <div className="flex-grow space-y-4 overflow-y-auto no-scrollbar pr-2 relative">
          <div className="absolute left-[21px] top-6 bottom-6 w-0.5 bg-stone-100 -z-0" />
          <div className="absolute left-[21px] top-6 bottom-6 w-0.5">
              <motion.div
                  className="w-full bg-slate-500 shadow-[0_0_10px_rgba(75,85,99,0.5)]"
                  style={{ height: `${progressPercentage}%` }}
              />
          </div>
          {sections.map((section, idx) => {
            const isUnlocked = idx <= unlockedSection;
            const isActive = idx === activeSection;
            const isCompleted = idx < unlockedSection;
            return (
              <button key={section.id} disabled={!isUnlocked} onClick={() => handleJumpToSection(idx)} className={`relative z-10 w-full flex items-center gap-4 p-3 rounded-xl transition-all duration-500 text-left group ${isActive ? 'bg-slate-50 shadow-sm translate-x-2' : ''} ${!isUnlocked ? 'opacity-40 grayscale cursor-not-allowed' : 'hover:bg-stone-50'}`}>
                <div className={`w-11 h-11 rounded-xl flex items-center justify-center shrink-0 border-2 transition-all duration-500 ${isCompleted ? 'bg-slate-600 border-slate-600 text-white shadow-lg' : isActive ? 'bg-white border-slate-500 text-slate-600 shadow-xl rotate-12' : 'bg-white border-stone-200 text-stone-300'}`}>
                   {isCompleted ? <CheckCircle2 size={18} /> : isActive ? <section.icon size={18} /> : <Lock size={16} />}
                </div>
                <div className="flex-grow"><p className={`text-[8px] font-black uppercase tracking-widest ${isActive ? 'text-slate-500' : 'text-stone-400'}`}>{section.eyebrow.split('// ')[1]}</p><h4 className={`text-xs font-bold leading-tight ${isActive ? 'text-stone-900' : 'text-stone-500'}`}>{section.title}</h4></div>
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
                <ReadingSection title="The Catastrophe Machine." eyebrow="Step 1" icon={MessageSquare}>
                  <p><Highlight description="An exaggerated negative thought process about a potential threat. It's a cognitive distortion where you magnify the consequences and underestimate your ability to cope.">Catastrophizing</Highlight> is the engine of exam anxiety. It's a 3-part machine: 1) <Highlight description="Repetitive, intrusive thoughts about failure.">Rumination</Highlight> (the thought you can't switch off), 2) <Highlight description="Blowing the consequences out of proportion (e.g., 'If I get a H4, my life is over').">Magnification</Highlight> (making a mountain out of a molehill), and 3) <Highlight description="The belief that the negative outcome is inevitable and you are powerless to stop it.">Helplessness</Highlight> (the feeling you're powerless).</p>
                </ReadingSection>
              )}
               {activeSection === 1 && (
                <ReadingSection title="The Biology of 'Blank Mind'." eyebrow="Step 2" icon={BrainCircuit}>
                  <p>Going "blank" is not a metaphor; it's a neurobiological event. When your brain perceives a threat (the exam paper), your <Highlight description="The brain's threat detection centre.">amygdala</Highlight> activates the stress response, flooding your system with adrenaline and cortisol. High levels of cortisol physically inhibit your <Highlight description="The brain region essential for memory retrieval.">hippocampus</Highlight>, blocking access to stored information. Your logical <Highlight description="The 'CEO' of the brain, responsible for planning and logic.">Prefrontal Cortex</Highlight> is taken offline. You haven't forgotten the information; you've just temporarily lost the password.</p>
                </ReadingSection>
              )}
              {activeSection === 2 && (
                <ReadingSection title="The Gold Standard (CBT)." eyebrow="Step 3" icon={BookOpen}>
                  <p><Highlight description="Cognitive Behavioral Therapy (CBT) is a form of psychological treatment that has been demonstrated to be effective for a range of problems including anxiety and depression.">Cognitive Behavioral Therapy (CBT)</Highlight> is the gold standard for dismantling this machine. Its central idea is simple but revolutionary: events don't cause your feelings; your *interpretation* of events causes your feelings. The exam paper is neutral. The thought "I can't do this" is the interpretation that triggers panic. CBT teaches you to challenge that interpretation.</p>
                </ReadingSection>
              )}
               {activeSection === 3 && (
                <ReadingSection title="The Thought Record." eyebrow="Step 4" icon={Wrench}>
                  <p>The core tool of CBT is the <Highlight description="A structured exercise to identify, challenge, and reframe Negative Automatic Thoughts (NATs).">Thought Record</Highlight>. It forces you to move from vague, emotional thinking to specific, evidence-based reasoning. By systematically examining the evidence for and against your catastrophic thought, you can generate a more balanced, realistic alternative. Run this protocol every time you feel a spike of panic.</p>
                  <ThoughtRecord />
                </ReadingSection>
              )}
               {activeSection === 4 && (
                <ReadingSection title="Decatastrophizing." eyebrow="Step 5" icon={Layers}>
                    <p>This technique doesn't promise "it will all be fine." Instead, it confronts the worst-case scenario head-on to strip it of its terror. It's called the <Highlight description="A CBT technique where you follow a catastrophic thought to its conclusion by repeatedly asking 'And then what?' to reveal that the ultimate outcome is manageable.">Downward Arrow</Highlight> technique. By following the "what if" chain to its end, you realize the ultimate outcome is survivable, and you create a "Plan B."</p>
                </ReadingSection>
              )}
               {activeSection === 5 && (
                <ReadingSection title="Facing the Fear." eyebrow="Step 6" icon={Shield}>
                    <p>Anxiety creates a vicious cycle of avoidance. You fear a subject, so you avoid it, which makes you unprepared, which justifies the original fear. The only way to break this cycle is <Highlight description="A behavioral technique where you face a feared stimulus in small, incremental steps, allowing your brain to 'habituate' and learn that it is not a threat.">Graded Exposure</Highlight>. You build a "ladder" of feared tasks, from least scary to most scary, and slowly work your way up, retraining your brain's alarm system.</p>
                    <GradedExposureHierarchy/>
                </ReadingSection>
              )}
               {activeSection === 6 && (
                <ReadingSection title="The Observer Self (ACT)." eyebrow="Step 7" icon={Zap}>
                    <p>For some, challenging thoughts feels like an endless argument. <Highlight description="Acceptance and Commitment Therapy (ACT) is a 'third-wave' CBT approach that focuses on changing your relationship to your thoughts, rather than the content of the thoughts themselves.">Acceptance and Commitment Therapy (ACT)</Highlight> offers an alternative: don't argue with the thought, just notice it and act anyway. This is called <Highlight description="The process of 'unhooking' from your thoughts, seeing them as just words passing through your mind, rather than objective truths or commands.">Cognitive Defusion</Highlight>.</p>
                    <PassengersOnBus/>
                </ReadingSection>
              )}
               {activeSection === 7 && (
                <ReadingSection title="The Action Plan." eyebrow="Step 8" icon={Flag}>
                  <p>You now have a complete toolkit of evidence-based psychological strategies to manage exam anxiety. You have the "software" (CBT & ACT) to go with the "hardware" optimization (sleep, nutrition) from other modules. Now it's about practice.</p>
                  <MicroCommitment><p>Choose ONE tool from this module—the Thought Record, Downward Arrow, or an Exposure task. Commit to using it just once this week. You're not just studying; you're becoming your own therapist.</p></MicroCommitment>
                </ReadingSection>
              )}
              <footer className="mt-24 flex items-center justify-between pt-12 border-t border-stone-200/60 px-4">
                <motion.button whileHover={{ scale: 1.05 }} whileTap={{ scale: 0.95 }} onClick={handlePrev} disabled={activeSection === 0} className={`flex items-center gap-4 bg-stone-100 text-stone-800 px-8 py-4 rounded-xl font-black text-[10px] uppercase tracking-widest transition-all shadow-sm ${activeSection === 0 ? 'opacity-0 pointer-events-none' : ''}`}>
                  <ArrowLeft size={16} /> Prev
                </motion.button>
                <motion.button whileHover={{ scale: 1.05 }} whileTap={{ scale: 0.95 }} onClick={handleCompleteSection} className="group relative flex items-center gap-4 bg-stone-900 text-white px-12 py-6 rounded-2xl font-black text-[12px] uppercase tracking-widest hover:bg-slate-600 transition-all shadow-[0_20px_50px_rgba(0,0,0,0.2)] overflow-hidden">
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
