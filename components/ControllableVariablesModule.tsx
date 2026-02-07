
/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
*/

import React, { useState } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { 
  ArrowLeft, CheckCircle2, ArrowRight, 
  Lock, Flag, Cpu, Moon, Droplet, BarChart, Zap, ClipboardCheck, Coffee
} from 'lucide-react';

interface ControllableVariablesModuleProps {
  onBack: () => void;
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

const ReadingSection = ({ title, eyebrow, icon: Icon, children }: { title: string, eyebrow: string, icon: any, children: React.ReactNode }) => (
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

const MicroCommitment = ({ children }: { children: React.ReactNode }) => (
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

const GlycemicIndexSimulator = () => {
    const [food, setFood] = useState<'none' | 'high' | 'low'>('none');
    
    const pathData = {
        none: "M0 80 L 500 80",
        high: "M0 80 C 100 10, 150 10, 200 60 C 250 110, 300 110, 500 90",
        low: "M0 80 C 100 70, 200 60, 500 50",
    }
    
    return(
        <div className="my-10 p-8 md:p-12 bg-white rounded-[3rem] border border-stone-200 shadow-xl">
            <h4 className="font-serif text-2xl font-bold text-stone-800 text-center italic">Glycemic Index Simulator</h4>
            <p className="text-center text-sm text-stone-500 mb-8">Choose a breakfast and see what it does to your blood sugar over 3 hours.</p>
            <div className="w-full h-32 bg-stone-50 rounded-lg p-4">
                <svg viewBox="0 0 500 100" className="w-full h-full" preserveAspectRatio="none">
                     <motion.path d={pathData[food]} fill="none" stroke="#f59e0b" strokeWidth="3" transition={{type: 'spring', damping: 15, stiffness: 100}}/>
                     <text x="5" y="15" fontSize="8" fill="#9ca3af">High Energy</text>
                     <text x="5" y="95" fontSize="8" fill="#9ca3af">Low Energy</text>
                </svg>
            </div>
             <div className="flex justify-center gap-4 mt-6">
                <button onClick={() => setFood('high')} className="px-4 py-2 bg-rose-100 text-rose-800 text-xs font-bold rounded-lg">Sugary Cereal (High-GI)</button>
                <button onClick={() => setFood('low')} className="px-4 py-2 bg-emerald-100 text-emerald-800 text-xs font-bold rounded-lg">Porridge (Low-GI)</button>
             </div>
        </div>
    );
};

const HighPerformanceChecklist = () => {
    const [checks, setChecks] = useState<{[key: string]: boolean}>({});
    const toggle = (key: string) => setChecks(prev => ({...prev, [key]: !prev[key]}));
    const items = [
        { key: 'wake', time: '08:30', task: 'Wake + Light Exposure', details: '10 mins outside. Anchors circadian clock.' },
        { key: 'fuel', time: '08:45', task: 'Hydration + Breakfast', details: '500ml water. Low-GI porridge.' },
        { key: 'deep1', time: '09:30', task: 'Study Block 1 (Deep Work)', details: '90 mins. High-cognitive load subjects.' },
        { key: 'break1', time: '11:00', task: 'Active Break', details: '15 mins walking. Avoid phone.' },
        { key: 'exercise', time: '16:00', task: 'EXERCISE (The Reset)', details: '45 mins. Spikes BDNF.' },
        { key: 'review', time: '18:30', task: 'Review Block (Active Recall)', details: '60 mins. "Test" yourself on morning work.' },
        { key: 'tech', time: '22:00', task: 'Tech Down-Regulation', details: 'No screens. Essential for melatonin onset.' },
        { key: 'sleep', time: '23:00', task: 'Sleep', details: '8.5 - 9 hours opportunity.' },
    ];

    return(
        <div className="my-10 p-8 md:p-12 bg-white rounded-[3rem] border border-stone-200 shadow-xl">
            <h4 className="font-serif text-2xl font-bold text-stone-800 text-center italic">High-Performance Checklist</h4>
            <p className="text-center text-sm text-stone-500 mb-8">This is the blueprint for a perfect study day, based on your biology.</p>
            <div className="space-y-3">
                {items.map(item => (
                    <div key={item.key} onClick={() => toggle(item.key)} className={`p-4 rounded-xl border-2 flex items-center gap-4 cursor-pointer ${checks[item.key] ? 'bg-emerald-50 border-emerald-200' : 'bg-stone-50 border-stone-200'}`}>
                        <span className="font-mono text-xs font-bold w-12">{item.time}</span>
                        <div className="flex-grow">
                            <p className="font-bold text-sm">{item.task}</p>
                            <p className="text-xs text-stone-500">{item.details}</p>
                        </div>
                        <div className={`w-6 h-6 rounded-full flex-shrink-0 flex items-center justify-center ${checks[item.key] ? 'bg-emerald-500' : 'bg-stone-300'}`}><CheckCircle2 size={12} className="text-white"/></div>
                    </div>
                ))}
            </div>
        </div>
    );
}


// --- MODULE COMPONENT ---
export const ControllableVariablesModule: React.FC<ControllableVariablesModuleProps> = ({ onBack }) => {
  const [activeSection, setActiveSection] = useState(0);
  const [unlockedSection, setUnlockedSection] = useState(0);
  
  const sections = [
    { id: 'engine', title: 'The Performance Engine', eyebrow: '01 // The Core Idea', icon: Cpu },
    { id: 'sleep', title: 'The Save Button: Sleep', eyebrow: '02 // The Foundation', icon: Moon },
    { id: 'nutrition', title: 'The Fuel Supply: Nutrition', eyebrow: '03 // The Energy', icon: Coffee },
    { id: 'exercise', title: 'The Upgrade: Exercise', eyebrow: '04 // The Catalyst', icon: Zap },
    { id: 'blueprint', title: 'The High-Performance Blueprint', eyebrow: '05 // The Plan', icon: ClipboardCheck },
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
            <p className="text-[9px] font-black text-slate-500 uppercase tracking-[0.4em] mb-0.5 underline">Module 09</p>
            <h1 className="font-serif font-bold text-lg tracking-tight text-stone-900">Controllable Variables</h1>
          </div>
        </div>

        <div className="flex-grow space-y-4 overflow-y-auto no-scrollbar pr-2 relative">
          <div className="absolute left-[21px] top-6 bottom-6 w-0.5 bg-stone-100 -z-0" />
          <div className="absolute left-[21px] top-6 bottom-6 w-0.5">
              <motion.div
                  className="w-full bg-slate-500 shadow-[0_0_10px_rgba(71,85,105,0.5)]"
                  initial={{ height: 0 }}
                  animate={{ height: sections.length > 1 ? `${(unlockedSection / (sections.length - 1)) * 100}%` : '0%' }}
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
           <ActivityRing progress={progress} color="#64748b" /><p className="text-[11px] font-black text-stone-900 uppercase tracking-widest text-center">Progress</p>
        </div>
      </aside>

      <main className="flex-grow flex flex-col items-center py-10 md:py-24 px-6 md:px-16 overflow-y-auto h-screen relative">
        <div className="absolute inset-0 bg-[radial-gradient(#e5e7eb_1px,transparent_1px)] [background-size:32px_32px] opacity-40 pointer-events-none" />
        <div className="w-full max-w-4xl relative z-10">
          <AnimatePresence mode="wait">
            <motion.div key={activeSection} initial={{ opacity: 0, x: 20 }} animate={{ opacity: 1, x: 0 }} exit={{ opacity: 0, x: -20 }} transition={{ duration: 0.6, ease: [0.16, 1, 0.3, 1] }}>
              {activeSection === 0 && (
                <ReadingSection title="The Performance Engine." eyebrow="Step 1" icon={Cpu}>
                  <p>Students often treat their brains like a disembodied intellect, ignoring the fact that learning, memory, and focus are biological processes. Your brain is not a computer; it's a high-performance engine. Its output is strictly constrained by its inputs and maintenance schedule. The emerging consensus from neuroscience is that your "capacity to learn" is not a fixed trait but a dynamic state that fluctuates based on three core physiological pillars: <Highlight description="The 'save button' for your memory, where learning is consolidated.">Sleep</Highlight>, <Highlight description="The fuel supply for your neurons, determining your ability to focus.">Nutrition</Highlight>, and <Highlight description="The upgrade mechanism that physically enhances your brain's ability to learn.">Exercise</Highlight>.</p>
                  <p>This module provides a scientifically grounded blueprint for the Leaving Cert student. It moves beyond generic advice to explain the mechanisms of memory and focus, providing actionable protocols. The strategic shift is from "time management" to <Highlight description="The superior strategy of focusing on the biological inputs (sleep, food, exercise) that determine the quality and quantity of your available mental energy.">energy management</Highlight>.</p>
                </ReadingSection>
              )}
              {activeSection === 1 && (
                <ReadingSection title="The Save Button: Sleep." eyebrow="Step 2" icon={Moon}>
                  <p>Learning is a two-stage process. The first stage, <Highlight description="The initial process of taking in new information when you are awake. These memory traces are fragile.">encoding</Highlight>, happens when you study. But this new information is fragile, temporarily stored in your brain's 'RAM'—the <Highlight description="A seahorse-shaped structure in the brain that acts as a temporary buffer for new memories.">hippocampus</Highlight>. Without the second stage, <Highlight description="The process by which fragile, short-term memories are stabilized and transferred to the neocortex for long-term storage. This happens primarily during sleep.">consolidation</Highlight>, that learning is erased. Sleep is the "save button." A student who studies for five hours but sleeps for five has learned less than a student who studies for three and sleeps for eight.</p>
                  <p>Your brain cycles through different types of sleep. <Highlight description="Deep, non-rapid eye movement sleep that is critical for consolidating declarative memories (facts, dates, definitions).">Slow-Wave Sleep (SWS)</Highlight>, dominant in the first half of the night, is for saving facts. <Highlight description="A stage of sleep characterized by vivid dreams and crucial for procedural memory (skills), creative problem-solving, and emotional regulation.">REM Sleep</Highlight>, dominant in the second half, is for making connections and solving problems. Cutting sleep short disproportionately sacrifices REM sleep, killing your creativity and problem-solving ability for the next day.</p>
                </ReadingSection>
              )}
              {activeSection === 2 && (
                <ReadingSection title="The Fuel Supply: Nutrition." eyebrow="Step 3" icon={Coffee}>
                  <p>Your brain is a metabolically expensive organ. It consumes 20% of your body's glucose. Nutrition is not a matter of aesthetics; it is a matter of substrate availability for your cognitive engine. The delivery mechanism of this glucose determines your performance.</p>
                  <p>High-<Highlight description="A measure of how quickly a food causes blood sugar levels to rise. High-GI foods (sugary snacks, white bread) cause a rapid spike and subsequent crash.">Glycemic Index (GI)</Highlight> foods create a roller-coaster of focus, leading to a "crash" mid-exam. Low-GI foods like oats provide a stable platform for concentration. Beyond energy, your brain needs specific micronutrients to build the chemicals that transmit signals. Deficiencies in <Highlight description="Found in oily fish, these fats are crucial for maintaining the fluidity of your brain cell membranes, allowing for efficient electrical signals.">Omega-3s</Highlight> and <Highlight description="Vitamins like B6, B9, and B12 are critical for synthesizing neurotransmitters like dopamine and serotonin.">B-Vitamins</Highlight> are directly correlated with "brain fog" and slower processing speeds. Finally, a loss of just 1% of body mass due to dehydration can cause measurable impairments in your working memory.</p>
                  <GlycemicIndexSimulator />
                </ReadingSection>
              )}
              {activeSection === 3 && (
                <ReadingSection title="The Upgrade: Exercise." eyebrow="Step 4" icon={Zap}>
                    <p>Exercise is not a distraction from study; it is a biological necessity for <Highlight description="The brain's ability to rewire itself and learn. Exercise is a powerful catalyst for this process.">neuroplasticity</Highlight>. The strongest link is <Highlight description="Brain-Derived Neurotrophic Factor (BDNF) is a protein that acts like 'Miracle-Gro' for your brain, supporting the growth of new neurons and synapses.">BDNF</Highlight>, a protein that acts as "molecular fertilizer" for your brain. Physical exertion effectively "switches on" the gene for BDNF production. A student with high BDNF levels will learn faster and retain more than a sedentary student.</p>
                    <p>Timing is critical. Exercise *before* study increases arousal and focus. Fascinatingly, research suggests exercise *after* a learning session may be even better for long-term retention—the <Highlight description="The finding that exercise performed a few hours after learning can retroactively 'tag' the preceding memories as important for consolidation.">Consolidation Hack</Highlight>. Finally, <Highlight description="Low-intensity exercise like walking, which helps clear metabolic waste and stress hormones like cortisol, making it superior to passive rest (scrolling on a phone).">Active Recovery</Highlight> is superior to passive rest for reducing cognitive fatigue.</p>
                </ReadingSection>
              )}
              {activeSection === 4 && (
                <ReadingSection title="The High-Performance Blueprint." eyebrow="Step 5" icon={ClipboardCheck}>
                  <p>By integrating the science of this "Cognitive Triad," we can construct an actionable blueprint for the Leaving Cert student. This approach shifts the focus from the flawed model of "time management" to the superior model of "energy management."</p>
                  <p>The following checklist is based on an optimized daily routine for a non-school day. It is designed to align with your natural adolescent circadian rhythms, maximize BDNF production, and ensure proper memory consolidation. This is not an aspirational goal; it is the evidence-based protocol for high performance.</p>
                  <HighPerformanceChecklist />
                  <MicroCommitment>
                    <p>Pick ONE item from this checklist that you are not currently doing. Just one. For the next seven days, commit to implementing that single change. Notice the effect it has on your energy and focus.</p>
                  </MicroCommitment>
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
