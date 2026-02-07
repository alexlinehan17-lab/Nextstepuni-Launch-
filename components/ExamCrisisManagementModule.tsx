/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
*/

import React, { useState, useEffect } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { 
  ArrowLeft, CheckCircle2, ArrowRight, 
  Lock, Flag, Cpu, Zap, Shield, Moon, Utensils, ClipboardList, Brain
} from 'lucide-react';

type ModuleProgress = {
  unlockedSection: number;
};

interface ExamCrisisManagementModuleProps {
  onBack: () => void;
  progress: ModuleProgress;
  onProgressUpdate: (progress: ModuleProgress) => void;
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
const CognitionShiftVisualizer = () => {
    const [isHot, setIsHot] = useState(false);
    return(
        <div className="my-10 p-8 md:p-12 bg-white rounded-[3rem] border border-stone-200 shadow-xl">
             <h4 className="font-serif text-2xl font-bold text-stone-800 text-center italic">Hot vs. Cold Cognition</h4>
             <p className="text-center text-sm text-stone-500 mb-8">Click the button to simulate what happens to your brain under exam stress.</p>
             <div className="flex justify-center items-center gap-4">
                <div className="text-center">
                    <motion.div animate={{opacity: isHot ? 0.3 : 1}}><Brain size={48} className="text-blue-500 mx-auto"/></motion.div>
                    <p className="font-bold text-sm mt-2">PFC (Cold)</p>
                </div>
                <div className="w-24 text-center">&harr;</div>
                <div className="text-center">
                     <motion.div animate={{opacity: isHot ? 1 : 0.3}}><Zap size={48} className="text-rose-500 mx-auto"/></motion.div>
                     <p className="font-bold text-sm mt-2">Amygdala (Hot)</p>
                </div>
             </div>
             <div className="text-center mt-6">
                <button onClick={() => setIsHot(!isHot)} className="px-4 py-2 bg-rose-500 text-white font-bold text-sm rounded-lg">{isHot ? 'De-escalate Threat' : 'Trigger Threat'}</button>
             </div>
        </div>
    );
};

const PhysiologicalSighGuide = () => (
    <div className="my-10 p-8 md:p-12 bg-white rounded-[3rem] border border-stone-200 shadow-xl text-center">
         <h4 className="font-serif text-2xl font-bold text-stone-800 text-center italic">The Physiological Sigh</h4>
         <p className="text-sm text-stone-500 mb-6">Your emergency brake for acute panic. Repeat 3 times.</p>
         <div className="flex justify-center items-center gap-8">
            <motion.div initial={{scale:0.5}} animate={{scale:[1, 1, 0.5, 0.5]}} transition={{duration:6, repeat: Infinity, times:[0, 0.4, 0.5, 1]}} className="w-20 h-20 rounded-full bg-sky-300 flex items-center justify-center font-bold">Inhale 1</motion.div>
            <motion.div initial={{scale:0.5}} animate={{scale:[0.5, 1, 0.5, 0.5]}} transition={{duration:6, repeat: Infinity, times:[0, 0.4, 0.5, 1]}} className="w-16 h-16 rounded-full bg-sky-300 flex items-center justify-center font-bold">Inhale 2</motion.div>
            <motion.div initial={{scale:1}} animate={{scale:[1, 1, 0.5, 1]}} transition={{duration:6, repeat: Infinity, times:[0, 0.5, 0.9, 1]}} className="w-24 h-24 rounded-full bg-sky-500 text-white flex items-center justify-center font-bold">Exhale</motion.div>
         </div>
    </div>
);


// --- MODULE COMPONENT ---
export const ExamCrisisManagementModule: React.FC<ExamCrisisManagementModuleProps> = ({ onBack, progress, onProgressUpdate }) => {
  const [activeSection, setActiveSection] = useState(progress.unlockedSection);
  const unlockedSection = progress.unlockedSection;
  
  const sections = [
    { id: 'anatomy-of-blank', title: 'The Anatomy of "Going Blank"', eyebrow: '01 // Hot vs. Cold Cognition', icon: Cpu },
    { id: 'blank-mind-protocol', title: 'The "Blank Mind" Protocol', eyebrow: '02 // Physiological Interventions', icon: Zap },
    { id: 'social-containment', title: 'Social Containment', eyebrow: '03 // The Post-Mortem Ban', icon: Shield },
    { id: 'cognitive-athlete-sleep', title: 'The Cognitive Athlete: Sleep', eyebrow: '04 // Sleep Architecture', icon: Moon },
    { id: 'cognitive-athlete-nutrition', title: 'The Cognitive Athlete: Nutrition', eyebrow: '05 // Bio-Optimization', icon: Utensils },
    { id: 'crisis-planning', title: 'Crisis Planning: The WRAP', eyebrow: '06 // The Pre-Planned Protocol', icon: ClipboardList },
    { id: 'implementation', title: 'The 7-Day Taper', eyebrow: '07 // The Implementation Guide', icon: Flag },
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
            <p className="text-[9px] font-black text-sky-500 uppercase tracking-[0.4em] mb-0.5 underline">Module 04</p>
            <h1 className="font-serif font-bold text-lg tracking-tight text-stone-900">Exam Crisis Management</h1>
          </div>
        </div>

        <div className="flex-grow space-y-4 overflow-y-auto no-scrollbar pr-2 relative">
          <div className="absolute left-[21px] top-6 bottom-6 w-0.5 bg-stone-100 -z-0" />
          <div className="absolute left-[21px] top-6 bottom-6 w-0.5">
              <motion.div
                  className="w-full bg-sky-500 shadow-[0_0_10px_rgba(14,165,233,0.5)]"
                  style={{ height: `${progressPercentage}%` }}
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
           <ActivityRing progress={progressPercentage} color="#0ea5e9" /><p className="text-[11px] font-black text-stone-900 uppercase tracking-widest text-center">Progress</p>
        </div>
      </aside>

      <main className="flex-grow flex flex-col items-center py-10 md:py-24 px-6 md:px-16 overflow-y-auto h-screen relative">
        <div className="absolute inset-0 bg-[radial-gradient(#e5e7eb_1px,transparent_1px)] [background-size:32px_32px] opacity-40 pointer-events-none" />
        <div className="w-full max-w-4xl relative z-10">
          <AnimatePresence mode="wait">
            <motion.div key={activeSection} initial={{ opacity: 0, x: 20 }} animate={{ opacity: 1, x: 0 }} exit={{ opacity: 0, x: -20 }} transition={{ duration: 0.6, ease: [0.16, 1, 0.3, 1] }}>
              {activeSection === 0 && (
                <ReadingSection title="Anatomy of 'Going Blank'." eyebrow="Step 1" icon={Cpu}>
                  <p>Going "blank" in an exam isn't you being stupid or unprepared. It's a physiological crisis. It's a neurochemical event where your brain's alarm system hijacks its command centre. To beat it, you need to understand the two states your brain operates in: <Highlight description="Your calm, logical state. Your Prefrontal Cortex (PFC) is in charge, allowing for clear thinking and easy memory retrieval.">Cold Cognition</Highlight> and <Highlight description="Your stressed, survival state. Your Amygdala (threat detector) takes over, shutting down the PFC and blocking access to memory.">Hot Cognition</Highlight>.</p>
                  <p>When you see a question you don't know, your brain can perceive it as a threat. This triggers an <Highlight description="The moment your emotional Amygdala hijacks your rational Prefrontal Cortex, flooding your system with stress hormones like cortisol and cutting the 'phone lines' to your memory.">Amygdala Hijack</Highlight>, switching you from "cold" to "hot" cognition. Your memory isn't gone; the connection is just temporarily offline. This isn't a knowledge problem; it's a hardware problem.</p>
                  <CognitionShiftVisualizer />
                </ReadingSection>
              )}
               {activeSection === 1 && (
                <ReadingSection title="The 'Blank Mind' Protocol." eyebrow="Step 2" icon={Zap}>
                    <p>Since the problem is physiological, the solution must be physiological. You can't "think" your way out of a panic because the thinking part of your brain is offline. You need to use your body to send a "safety" signal to your brain. This is called <Highlight description="Using bodily sensations and actions (like breathing) to influence your mental and emotional state, rather than trying to think your way calm.">bottom-up processing</Highlight>.</p>
                    <p>The fastest way to do this is the <Highlight description="An emergency breathing technique (two inhales, one long exhale) that re-inflates collapsed air sacs in your lungs, rapidly offloading CO2 and forcing your nervous system to calm down.">Physiological Sigh</Highlight>. It's your "hard reset" button. Once the initial chemical flood is stopped, you re-engage your PFC with a <Highlight description="The 5-4-3-2-1 technique of naming things you can see, feel, hear, smell, and taste. It forces your brain to process external sensory data, pulling it out of the internal panic loop.">Sensory Grounding</Highlight> exercise. Finally, you restart your cognitive engine with an <Highlight description="Deliberately finding the easiest possible question on the paper to answer. This micro-success triggers a small release of dopamine, which helps clear the cortisol 'fog' from your PFC.">'Easy Win'</Highlight>.</p>
                    <PhysiologicalSighGuide/>
                </ReadingSection>
              )}
              {activeSection === 2 && (
                <ReadingSection title="Social Containment." eyebrow="Step 3" icon={Shield}>
                  <p>The crisis doesn't end when you put your pen down. The minutes after an exam are a minefield of <Highlight description="The contagious spread of anxiety through a peer group, often triggered by post-exam 'post-mortems.'">Anxiety Contagion</Highlight>. Discussing answers with stressed-out friends is one of the worst things you can do. It elevates your cortisol levels, preventing the physiological recovery you need for the next exam.</p>
                  <p>This urge to compare answers is driven by a powerful psychological force called the <Highlight description="A psychological desire for a firm answer to a question and an aversion to ambiguity. The uncertainty of an exam result creates a cognitive 'open loop' that the brain desperately wants to close.">Need for Cognitive Closure (NFC)</Highlight>. You have to train the discipline to leave that loop open. This requires a strict <Highlight description="A personal rule to immediately exit the exam hall and avoid all discussion of the exam until the entire exam period is over.">"Post-Mortem Ban"</Highlight>. This isn't anti-social; it's a professional strategy to manage your mental stamina.</p>
                </ReadingSection>
              )}
               {activeSection === 3 && (
                <ReadingSection title="The Cognitive Athlete: Sleep." eyebrow="Step 4" icon={Moon}>
                  <p>You must treat the weeks before the Leaving Cert like a championship season. You are a <Highlight description="A model that treats academic performance like an athletic event, focusing on physiological optimization (sleep, nutrition) to maximize cognitive output.">Cognitive Athlete</Highlight>, and your brain is your primary muscle. Sleep is your most important training tool.</p>
                  <p>In the week before exams, you should engage in <Highlight description="The strategy of extending sleep duration in the days leading up to a period of sleep restriction to build a 'cognitive reserve' and mitigate the negative effects.">Sleep Banking</Highlight>—getting an extra hour of sleep per night. This builds a cognitive reserve that has been proven to protect against the effects of later sleep loss. During sleep, your brain also activates the <Highlight description="The brain's unique cleaning system, where cerebrospinal fluid flushes out metabolic waste products like adenosine that accumulate during waking hours and cause 'brain fog.'">Glymphatic System</Highlight>, clearing out the toxins that impair focus.</p>
                </ReadingSection>
              )}
              {activeSection === 4 && (
                <ReadingSection title="The Cognitive Athlete: Nutrition." eyebrow="Step 5" icon={Utensils}>
                  <p>Your brain runs on glucose, but it needs a steady supply, not a sugar rush. High <Highlight description="Foods that are rapidly digested, causing a quick spike and then a crash in blood sugar levels (e.g., sugary snacks, white bread).">Glycemic Index (GI)</Highlight> foods cause a "crash" that coincides with the middle of an exam. Your pre-exam meal should be low-GI complex carbs and protein 3 hours before.</p>
                  <p>To maximize your alertness on the day, you can use caffeine strategically. <Highlight description="The process of gradually reducing caffeine intake in the 7-10 days before an exam to re-sensitize your brain's adenosine receptors.">Caffeine Tapering</Highlight> means a normal cup of coffee on exam day will have a much more powerful effect. Pairing it with L-Theanine (found in tea) can create "calm focus" without the jitters.</p>
                </ReadingSection>
              )}
              {activeSection === 5 && (
                <ReadingSection title="Crisis Planning: The WRAP." eyebrow="Step 6" icon={ClipboardList}>
                  <p>Elite performers don't just react to crises; they plan for them. The <Highlight description="The Wellness Recovery Action Plan is a structured system for identifying your personal triggers and creating a pre-planned response to a crisis.">WRAP Framework</Highlight> is a tool for doing just that. It moves you from a state of panic to executing a pre-planned protocol.</p>
                  <p>Your Academic WRAP has four parts. **1. Daily Maintenance:** What do you need to do every day to stay well? **2. Triggers:** What external events throw you off? **3. Early Warning Signs:** What are your internal signals of rising stress? **4. Crisis Plan:** Your "Break Glass" protocol for a full-blown panic attack. By writing this down *before* the crisis, you outsource the decision-making to your calm, rational self.</p>
                </ReadingSection>
              )}
              {activeSection === 6 && (
                <ReadingSection title="The 7-Day Taper." eyebrow="Step 7" icon={Flag}>
                  <p>This is where it all comes together. The final week before the exams is your "Taper." Just like an athlete, you reduce the training load to allow your body and mind to recover and peak at the right moment. This is not the time for cramming.</p>
                  <p>Your 7-day taper should include: **Caffeine Resensitization** (T-7 days), **Circadian Entrainment** (T-5 days, waking up at exam time), and **Nutritional Priming** (T-3 days, shifting to low-GI foods and hyper-hydrating). The day before the exam, you stop all heavy study. You are no longer building knowledge; you are preparing the machine that will deploy it.</p>
                  <MicroCommitment>
                    <p>Take out your calendar. Find the date one week before your first exam. Create an event called "Begin 7-Day Taper." You've just taken the first step to becoming a Cognitive Athlete.</p>
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
