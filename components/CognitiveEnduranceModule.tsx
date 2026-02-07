
/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
*/

import React, { useState } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { 
  ArrowLeft, CheckCircle2, ArrowRight, 
  Lock, Flag, Battery, Brain, Moon, Coffee, HeartPulse, SlidersHorizontal
} from 'lucide-react';

interface CognitiveEnduranceModuleProps {
  onBack: () => void;
}

const Highlight = ({ children, description, color = "bg-orange-100/40", textColor = "text-orange-900", decorColor = "decoration-orange-400/40", hoverColor="hover:bg-orange-200/60" }: { children?: React.ReactNode, description: string, color?: string, textColor?: string, decorColor?: string, hoverColor?: string }) => {
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
              <p className="font-sans font-bold text-orange-400 mb-2 uppercase tracking-[0.2em] text-[9px]">The Academic Insight</p>
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
        <div className="w-12 h-12 rounded-2xl bg-stone-900 flex items-center justify-center text-orange-400 shadow-xl border border-white/10">
          <Icon size={24} />
        </div>
      </div>
      <span className="inline-flex items-center gap-2 px-3 py-1 bg-orange-50 text-orange-600 text-[10px] font-black tracking-[0.4em] uppercase rounded-full mb-4">
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
  <div className="my-12 p-8 bg-orange-50/50 border-2 border-dashed border-orange-200 rounded-3xl">
    <div className="flex items-start gap-5">
      <div className="w-11 h-11 rounded-xl bg-orange-500 text-white flex items-center justify-center shrink-0 mt-1 shadow-lg shadow-orange-500/20">
        <Flag size={20} />
      </div>
      <div>
        <h4 className="font-bold text-orange-800 text-sm uppercase tracking-widest">Your Mission (Under 5 Mins)</h4>
        <div className="text-stone-600 mt-2 font-medium leading-relaxed">
          {children}
        </div>
      </div>
    </div>
  </div>
);

const ActivityRing = ({ progress, color = "#f97316" }: { progress: number, color?: string }) => {
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

const AllostaticLoadVisualizer = () => {
    return (
        <div className="my-10 p-8 md:p-12 bg-white rounded-[3rem] border border-stone-200 shadow-xl">
             <h4 className="font-serif text-2xl font-bold text-stone-800 text-center italic">The Leaving Cert Allostatic Load</h4>
             <p className="text-center text-sm text-stone-500 mb-8">Your brain's "wear and tear" isn't constant. It builds over time and spikes during exam clusters.</p>
             <div className="w-full h-40 bg-stone-50 rounded-lg p-4">
                <svg viewBox="0 0 500 100" className="w-full h-full" preserveAspectRatio="none">
                    <path d="M 0 90 C 100 80, 200 60, 300 50 L 400 40 L 410 20 L 420 40 L 430 30 L 440 10 L 450 35 L 500 30" fill="none" stroke="#f97316" strokeWidth="3" />
                    <text x="50" y="95" fontSize="10" className="fill-stone-400">5th Year</text>
                    <text x="350" y="95" fontSize="10" className="fill-stone-400">6th Year</text>
                    <text x="450" y="95" fontSize="10" className="fill-rose-500 font-bold">Exams</text>
                </svg>
             </div>
        </div>
    );
};

const SleepCycleArchitect = () => {
    const [sleepHours, setSleepHours] = useState(8);
    const remLost = Math.max(0, (8 - sleepHours) * 25); // Rough calc
    return (
        <div className="my-10 p-8 md:p-12 bg-white rounded-[3rem] border border-stone-200 shadow-xl">
            <h4 className="font-serif text-2xl font-bold text-stone-800 text-center italic">The Sleep Cycle Architect</h4>
            <p className="text-center text-sm text-stone-500 mb-8">Use the slider to see what happens when you cut sleep short. Notice what gets cut first.</p>
            <div className="h-24 w-full bg-stone-100 rounded-lg flex">
                <div className="h-full bg-slate-400" style={{width: `${(sleepHours/9)*100}%`}}>
                    {/* Cycles */}
                    <div className="h-full w-full flex">
                        {[...Array(5)].map((_, i) => (
                            <div key={i} className={`h-full border-r border-white/20 relative ${i*2 > sleepHours ? 'opacity-20' : ''}`} style={{width: '20%'}}>
                                <div className="absolute bottom-0 w-full h-1/2 bg-blue-400" />
                                <div className="absolute bottom-1/2 w-full h-1/4 bg-sky-300" />
                            </div>
                        ))}
                    </div>
                </div>
            </div>
            <input type="range" min="4" max="9" step="0.5" value={sleepHours} onChange={e => setSleepHours(parseFloat(e.target.value))} className="w-full mt-4" />
            <div className="text-center font-bold mt-2">{sleepHours.toFixed(1)} hours of sleep</div>
            <AnimatePresence>
            {remLost > 0 && 
                <motion.div initial={{opacity:0}} animate={{opacity:1}} className="mt-4 p-4 bg-rose-50 border border-rose-200 rounded-xl text-center text-sm">
                   You've lost approximately <span className="font-bold text-rose-600">{remLost}%</span> of your critical REM sleep, impairing problem-solving and emotional regulation.
                </motion.div>
            }
            </AnimatePresence>
        </div>
    );
};

// --- MODULE COMPONENT ---
export const CognitiveEnduranceModule: React.FC<CognitiveEnduranceModuleProps> = ({ onBack }) => {
  const [activeSection, setActiveSection] = useState(0);
  const [unlockedSection, setUnlockedSection] = useState(0);
  
  const sections = [
    { id: 'marathon-mindset', title: 'The Marathon Mindset', eyebrow: '01 // The Construct', icon: Brain },
    { id: 'sleep-banking', title: 'The Sleep Banking Strategy', eyebrow: '02 // The Non-Negotiable', icon: Moon },
    { id: 'fueling-engine', title: 'Fueling the Engine', eyebrow: '03 // Nutrition & Hydration', icon: Coffee },
    { id: 'in-exam-tools', title: 'The In-Exam Toolkit', eyebrow: '04 // Psychological Protocols', icon: HeartPulse },
    { id: 'training-plan', title: 'The Training Plan', eyebrow: '05 // Progressive Overload', icon: SlidersHorizontal },
    { id: 'recovery-protocol', title: 'The Recovery Protocol', eyebrow: '06 // Active Recovery', icon: Battery },
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
            <p className="text-[9px] font-black text-orange-500 uppercase tracking-[0.4em] mb-0.5 underline">Module 10</p>
            <h1 className="font-serif font-bold text-lg tracking-tight text-stone-900">Cognitive Endurance</h1>
          </div>
        </div>

        <div className="flex-grow space-y-4 overflow-y-auto no-scrollbar pr-2 relative">
          <div className="absolute left-[21px] top-6 bottom-6 w-0.5 bg-stone-100 -z-0" />
          <div className="absolute left-[21px] top-6 bottom-6 w-0.5">
              <motion.div
                  className="w-full bg-orange-500 shadow-[0_0_10px_rgba(249,115,22,0.5)]"
                  initial={{ height: 0 }}
                  animate={{ height: sections.length > 1 ? `${(unlockedSection / (sections.length - 1)) * 100}%` : '0%' }}
              />
          </div>
          {sections.map((section, idx) => {
            const isUnlocked = idx <= unlockedSection;
            const isActive = idx === activeSection;
            const isCompleted = idx < unlockedSection;
            return (
              <button key={section.id} disabled={!isUnlocked} onClick={() => handleJumpToSection(idx)} className={`relative z-10 w-full flex items-center gap-4 p-3 rounded-xl transition-all duration-500 text-left group ${isActive ? 'bg-orange-50 shadow-sm translate-x-2' : ''} ${!isUnlocked ? 'opacity-40 grayscale cursor-not-allowed' : 'hover:bg-stone-50'}`}>
                <div className={`w-11 h-11 rounded-xl flex items-center justify-center shrink-0 border-2 transition-all duration-500 ${isCompleted ? 'bg-orange-600 border-orange-600 text-white shadow-lg' : isActive ? 'bg-white border-orange-500 text-orange-600 shadow-xl rotate-12' : 'bg-white border-stone-200 text-stone-300'}`}>
                   {isCompleted ? <CheckCircle2 size={18} /> : isActive ? <section.icon size={18} /> : <Lock size={16} />}
                </div>
                <div className="flex-grow"><p className={`text-[8px] font-black uppercase tracking-widest ${isActive ? 'text-orange-500' : 'text-stone-400'}`}>{section.eyebrow.split('// ')[1]}</p><h4 className={`text-xs font-bold leading-tight ${isActive ? 'text-stone-900' : 'text-stone-500'}`}>{section.title}</h4></div>
              </button>
            );
          })}
        </div>

        <div className="mt-8 border-t border-stone-100 pt-8 flex flex-col items-center">
           <ActivityRing progress={progress} color="#f97316" /><p className="text-[11px] font-black text-stone-900 uppercase tracking-widest text-center">Progress</p>
        </div>
      </aside>

      <main className="flex-grow flex flex-col items-center py-10 md:py-24 px-6 md:px-16 overflow-y-auto h-screen relative">
        <div className="absolute inset-0 bg-[radial-gradient(#e5e7eb_1px,transparent_1px)] [background-size:32px_32px] opacity-40 pointer-events-none" />
        <div className="w-full max-w-4xl relative z-10">
          <AnimatePresence mode="wait">
            <motion.div key={activeSection} initial={{ opacity: 0, x: 20 }} animate={{ opacity: 1, x: 0 }} exit={{ opacity: 0, x: -20 }} transition={{ duration: 0.6, ease: [0.16, 1, 0.3, 1] }}>
              {activeSection === 0 && (
                <ReadingSection title="The Marathon Mindset." eyebrow="Step 1" icon={Brain}>
                  <p>The Leaving Cert isn't a sprint; it's a marathon. Success isn't just about knowing the material. It's about being able to access that knowledge at 4 PM on a Friday after a brutal week of exams. This is <Highlight description="The ability to sustain high-level mental performance, maintain focus, and resist distraction over extended periods of effortful thinking.">Cognitive Endurance</Highlight>.</p>
                  <p>It's a biological skill, not a measure of willpower. Your brain is an organ that consumes 20% of your body's energy. Under the chronic stress of the Leaving Cert, your brain accumulates "wear and tear"—a concept scientists call <Highlight description="The cumulative physiological 'wear and tear' on the body and brain that results from chronic stress. High allostatic load impairs PFC function and emotional regulation.">Allostatic Load</Highlight>. Building cognitive endurance is about training your brain to handle this load.</p>
                  <AllostaticLoadVisualizer />
                </ReadingSection>
              )}
               {activeSection === 1 && (
                <ReadingSection title="The Sleep Banking Strategy." eyebrow="Step 2" icon={Moon}>
                  <p>Sleep is the single most powerful tool for building endurance. It’s not rest; it’s when your brain consolidates memory and clears out metabolic waste like <Highlight description="A metabolic byproduct that accumulates in the brain during waking hours. It binds to receptors and inhibits neural activity, creating the feeling of 'sleep pressure' or 'brain fog'.">adenosine</Highlight>.</p>
                  <p>As a teenager, your brain has a natural "phase delay," meaning you want to sleep late and wake up late. The exam schedule fights this. Crucially, the final hours of your sleep are dense with <Highlight description="Rapid Eye Movement sleep is critical for consolidating procedural (skill) memory and for emotional regulation. It is disproportionately lost when you wake up early.">REM Sleep</Highlight>, which is vital for problem-solving skills and emotional stability. Cutting sleep short is like skipping the most important part of your training.</p>
                  <SleepCycleArchitect />
                  <MicroCommitment><p>For the next 10 days, wake up at the same time every single day—even weekends. This 'Fixed Wake-Up' protocol is the fastest way to reset your body clock and align your peak alertness with exam time.</p></MicroCommitment>
                </ReadingSection>
              )}
              {activeSection === 2 && (
                <ReadingSection title="Fueling the Engine." eyebrow="Step 3" icon={Coffee}>
                  <p>Your brain runs on glucose. An unstable fuel supply leads to unstable focus. High-sugar snacks cause a spike-and-crash cycle called <Highlight description="A state of low blood sugar that occurs 60-90 minutes after a high-sugar meal. It manifests as brain fog, irritability, and a loss of willpower, often coinciding with the middle of an exam.">Reactive Hypoglycemia</Highlight>, sabotaging your performance mid-exam.</p>
                  <p>A cutting-edge hack from sports science is the <Highlight description="The finding that merely rinsing the mouth with a carbohydrate solution (without swallowing) can trick the brain into reducing the perception of fatigue and increasing neural drive.">Carbohydrate Mouth Rinse</Highlight>. Swishing a sports drink for 10 seconds activates reward centres in the brain, tricking it into thinking fuel is on the way. This can provide a vital mental boost in the final, gruelling hour of a long exam.</p>
                </ReadingSection>
              )}
               {activeSection === 3 && (
                <ReadingSection title="The In-Exam Toolkit." eyebrow="Step 4" icon={HeartPulse}>
                    <p>Anxiety is the enemy of endurance. It hijacks your brain, diverting blood flow from your rational <Highlight description="The 'CEO' of your brain, responsible for executive functions like working memory and impulse control. Its function is severely impaired by stress and fatigue.">Prefrontal Cortex (PFC)</Highlight> to your emotional <Highlight description="The brain's primitive fear centre. When it becomes overactive, it can 'hijack' the PFC, leading to a 'blanking out' phenomenon.">amygdala</Highlight>. You need tools to manage this in real-time.</p>
                    <p>The fastest way to calm your nervous system is the <Highlight description="A specific breathing pattern (two sharp inhales through the nose, one long exhale through the mouth) that reinflates collapsed air sacs in the lungs, rapidly offloading carbon dioxide and reducing autonomic arousal.">Physiological Sigh</Highlight>. It takes less than 10 seconds. When you feel panic rising after a tough question, this is your emergency brake.</p>
                    <p>For your eyes, use the **20-20-20 Rule**: every 20 minutes, look at something 20 feet away for 20 seconds. This relaxes your eye muscles and fights the visual fatigue that causes headaches and slows reading speed.</p>
                </ReadingSection>
              )}
               {activeSection === 4 && (
                <ReadingSection title="The Training Plan." eyebrow="Step 5" icon={SlidersHorizontal}>
                  <p>You can't train for a marathon by only running sprints. Likewise, you can't prepare for a 3-hour exam by only studying in 20-minute bursts. You need to train your focus using <Highlight description="The core principle of all training. To improve, you must gradually increase the duration, intensity, or difficulty of the task over time.">Progressive Overload</Highlight>.</p>
                  <p>This means structuring your study in phases. Start with short, focused bursts (like the Pomodoro Technique) to build your base. Then, gradually increase the duration of your focus blocks, training your brain to push past the "boredom barrier." In the final weeks, you should be doing full "Simulation Blocks"—studying under exam conditions for 90-120 minutes straight. This is not about learning more content; it's about building mental muscle.</p>
                </ReadingSection>
              )}
               {activeSection === 5 && (
                <ReadingSection title="The Recovery Protocol." eyebrow="Step 6" icon={Battery}>
                  <p>Recovery is not the absence of work; it's an active process. Lying on the couch scrolling through TikTok is not rest. It's <Highlight description="Low-quality rest that involves high-dopamine, high-input cognitive load (e.g., social media). It fragments attention and prevents true neural recovery.">Passive Recovery</Highlight>, and it can actually increase your cognitive fatigue.</p>
                  <p><Highlight description="High-quality rest that involves low cognitive load and specific physiological benefits. Examples include light exercise, time in nature, and NSDR.">Active Recovery</Highlight> strategies are far superior. A 20-minute walk clears stress hormones. Even better is <Highlight description="Non-Sleep Deep Rest (NSDR) is a guided meditation technique that brings the brain into a state of deep relaxation while maintaining consciousness. It rapidly replenishes dopamine and reduces cortisol.">NSDR</Highlight>, a 10-20 minute guided relaxation that acts as a "system reset" for your brain. In the crucial break between two exams on the same day, a 20-minute NSDR session is the single most effective way to restore your cognitive endurance for the afternoon paper.</p>
                  <MicroCommitment><p>Find a 10-minute NSDR or Yoga Nidra script on YouTube. Try it once this week instead of scrolling on your phone during a study break.</p></MicroCommitment>
                </ReadingSection>
              )}
              <footer className="mt-24 flex items-center justify-between pt-12 border-t border-stone-200/60 px-4">
                <motion.button whileHover={{ scale: 1.05 }} whileTap={{ scale: 0.95 }} onClick={handlePrev} disabled={activeSection === 0} className={`flex items-center gap-4 bg-stone-100 text-stone-800 px-8 py-4 rounded-xl font-black text-[10px] uppercase tracking-widest transition-all shadow-sm ${activeSection === 0 ? 'opacity-0 pointer-events-none' : ''}`}>
                  <ArrowLeft size={16} /> Prev
                </motion.button>
                <motion.button whileHover={{ scale: 1.05 }} whileTap={{ scale: 0.95 }} onClick={handleCompleteSection} className="group relative flex items-center gap-4 bg-stone-900 text-white px-12 py-6 rounded-2xl font-black text-[12px] uppercase tracking-widest hover:bg-orange-600 transition-all shadow-[0_20px_50px_rgba(0,0,0,0.2)] overflow-hidden">
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
