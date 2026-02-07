/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
*/

import React, { useState } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { 
  ArrowLeft, CheckCircle2, ArrowRight, 
  Lock, Flag, BrainCircuit, Shield, Laptop, Home, Repeat, Users, Map
} from 'lucide-react';

interface DigitalDistractionModuleProps {
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
const AttentionDeficitCalculator = () => {
    const [checks, setChecks] = useState(3);
    const timeLost = checks * 23.25;
    const deepWorkTime = 60 - timeLost;
    return(
        <div className="my-10 p-8 md:p-12 bg-white rounded-[3rem] border border-stone-200 shadow-xl">
             <h4 className="font-serif text-2xl font-bold text-stone-800 text-center italic">Attention Deficit Calculator</h4>
             <p className="text-center text-sm text-stone-500 mb-6">Each phone check costs ~23 mins of focus. See the damage.</p>
             <div>
                <label className="font-bold text-sm">Phone checks per hour: {checks}</label>
                <input type="range" min="0" max="10" value={checks} onChange={e=>setChecks(parseInt(e.target.value))} className="w-full"/>
             </div>
             <div className="mt-6 p-4 bg-stone-900 rounded-xl text-center text-white">
                Deep Work Time Achieved: <span className={`font-bold text-2xl ${deepWorkTime > 0 ? 'text-emerald-400' : 'text-rose-400'}`}>{deepWorkTime.toFixed(1)} minutes</span>
             </div>
        </div>
    );
};

// --- MODULE COMPONENT ---
export const DigitalDistractionModule: React.FC<{onBack: () => void}> = ({ onBack }) => {
  const [activeSection, setActiveSection] = useState(0);
  const [unlockedSection, setUnlockedSection] = useState(0);
  
  const sections = [
    { id: 'adversary', title: 'The Adversary', eyebrow: '01 // Neuroscience of Distraction', icon: BrainCircuit },
    { id: 'hardware-barrier', title: 'Hardware Architecture', eyebrow: '02 // The Physical Barrier', icon: Shield },
    { id: 'software-fortification', title: 'Software Fortification', eyebrow: '03 // The Laptop Sanctuary', icon: Laptop },
    { id: 'environmental-engineering', title: 'Environmental Engineering', eyebrow: '04 // The Study Sanctuary', icon: Home },
    { id: 'behavioral-engineering', title: 'Behavioral Engineering', eyebrow: '05 // Atomic Habits', icon: Repeat },
    { id: 'social-dynamics', title: 'Social Dynamics', eyebrow: '06 // The FOMO Barrier', icon: Users },
    { id: 'roadmap', title: 'The Roadmap', eyebrow: '07 // Strategic Implementation', icon: Map },
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
            <p className="text-[9px] font-black text-slate-500 uppercase tracking-[0.4em] mb-0.5 underline">Module 07</p>
            <h1 className="font-serif font-bold text-lg tracking-tight text-stone-900">Digital Distractions</h1>
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
                <ReadingSection title="The Adversary." eyebrow="Step 1" icon={BrainCircuit}>
                  <p>Your inability to focus is not a character flaw. It's a predictable conflict between your brain's biology and a digital environment engineered to exploit it. The adolescent brain has an underdeveloped <Highlight description="The 'CEO' of your brain, responsible for impulse control and long-term planning.">Prefrontal Cortex (PFC)</Highlight> and a hyperactive <Highlight description="The brain's reward and emotion centre.">Limbic System</Highlight>. Social media is designed as a <Highlight description="Like a slot machine, it provides unpredictable rewards (likes, messages) that trigger a dopamine hit, creating a compulsive loop.">Variable Ratio Reinforcement Schedule</Highlight> that hijacks this system.</p>
                  <p>Every time you switch tasks (from study to Snapchat), you suffer from <Highlight description="The 'cognitive residue' left from the previous task. It takes an average of 23 minutes to regain deep focus after an interruption.">Attention Residue</Highlight>. This module is a blueprint for reclaiming your <Highlight description="Your ability to direct your own attention and consciousness, free from external manipulation.">Cognitive Sovereignty</Highlight>.</p>
                  <AttentionDeficitCalculator />
                </ReadingSection>
              )}
              {activeSection === 1 && (
                <ReadingSection title="Hardware Architecture." eyebrow="Step 2" icon={Shield}>
                  <p>Since your internal "software" (willpower) is compromised by adolescent biology, the most effective strategy is to alter the "hardware" of your environment. The most radical and effective barrier is the "Dumb Phone" revolution. By switching to a device without an algorithmic feed, you eliminate the possibility of distraction.</p>
                  <p>This involves a trade-off between <Highlight description="Making a behavior more difficult to perform. The 'friction' of using a T9 keypad for texting is a powerful deterrent.">Friction</Highlight> and function. There's a hierarchy of devices, from the "Purist" Nokia with zero features, to the "Hybrid" CAT S22 Flip which has WhatsApp but is physically unpleasant to scroll on. The goal is to make the cost of the distraction (frustration) outweigh the reward.</p>
                </ReadingSection>
              )}
              {activeSection === 2 && (
                <ReadingSection title="Software Fortification." eyebrow="Step 3" icon={Laptop}>
                  <p>Your laptop is a "Trojan Horse"—a study tool that is also the main portal for distraction. Browser extensions are easily disabled. You need system-level blocking architecture. Applications like <Highlight description="Software that can block websites, apps, or the entire internet on your computer. 'Locked Mode' makes it impossible to bypass the block.">Freedom or Cold Turkey</Highlight> are essential.</p>
                  <p>The best strategy is an "Allowlist" that creates a <Highlight description="Blocking the entire internet except for a few pre-approved educational sites like Studyclix or Examinations.ie.">"Walled Garden."</Highlight> To counter the "I need it for research" excuse, you can build an <Highlight description="Using tools like Kiwix to download entire websites (like Wikipedia) for offline use, satisfying the need for information without the temptation of the live internet.">"Offline Internet"</Highlight>. This separates "Hunting" for information from "Gathering" it.</p>
                </ReadingSection>
              )}
              {activeSection === 3 && (
                <ReadingSection title="Environmental Engineering." eyebrow="Step 4" icon={Home}>
                  <p>Your physical environment is a silent architect of your behavior. The principle of <Highlight description="The neurobiological fact that the mere presence of a tempting object (like a phone) in your visual field consumes cognitive resources as your brain actively works to inhibit the impulse to use it.">Visual Field Management</Highlight> is crucial. "Out of sight, out of mind" is not a cliché; it's a neurological reality. The mere presence of your phone, even face down, causes "Brain Drain."</p>
                  <p>The protocol is simple: the phone must be physically removed from the study room. It should be charged in a communal area like the kitchen. To counter the "I use it to check the time" excuse, place a simple analog clock on your desk.</p>
                </ReadingSection>
              )}
              {activeSection === 4 && (
                <ReadingSection title="Behavioral Engineering." eyebrow="Step 5" icon={Repeat}>
                  <p>You can automate the creation of these barriers using principles from behavioral psychology. The first tool is <Highlight description="A technique from James Clear's 'Atomic Habits' where you pair a new, desired behavior with an established one.">Habit Stacking</Highlight>. The formula is: "After [Current Habit], I will [New Habit]." For example: "After I walk in the door from school, I will immediately put my phone in the kitchen charger."</p>
                  <p>The second tool is <Highlight description="An 'If-Then' plan that pre-programs your response to an inevitable distraction, removing the need for in-the-moment willpower.">Implementation Intentions</Highlight>. The formula: "If [Trigger occurs], then I will [Action]." For example: "If I feel the urge to check Instagram, then I will stand up and do 5 star jumps." This removes the need to negotiate with your tired brain.</p>
                </ReadingSection>
              )}
              {activeSection === 5 && (
                <ReadingSection title="Social Dynamics." eyebrow="Step 6" icon={Users}>
                  <p>The biggest barrier to disconnecting is not the technology; it's the social anxiety it alleviates—the Fear Of Missing Out (FOMO). Disconnecting without explanation can lead to social friction. The <Highlight description="The strategy of explicitly communicating your new boundaries to your friends (e.g., 'I'm off my phone from 5-9 PM for the LC, I'll reply after').">"Social Contract"</Highlight> strategy manages expectations.</p>
                  <p>Instead of constant, low-quality connection, you should <Highlight description="The practice of condensing your social media use into specific, pre-scheduled 'Online Windows' (e.g., 8:30-9:30 PM).">"Batch" your socialization</Highlight>. This makes the interactions more focused and turns them into a reward for a day of deep work, rather than a constant background noise that fragments your attention.</p>
                </ReadingSection>
              )}
              {activeSection === 6 && (
                <ReadingSection title="The Roadmap." eyebrow="Step 7" icon={Map}>
                  <p>Implementing these barriers is a phased process over the Leaving Cert cycle. **Phase 1: The Audit (Sept - Dec).** Install RescueTime, identify your time sinks, and start with a Level 1 detox (phone out of the room at night). **Phase 2: The Hardening (Jan - Mar).** Introduce software blockers, an "Offline Internet," and "batch" your social communication. **Phase 3: The Sprint (Apr - June).** This is "Monk Mode." Switch to a "dumb phone," use "Locked Mode" on laptops, and consider deactivating social media accounts.</p>
                  <MicroCommitment>
                    <p>Tonight, take your phone charger out of your bedroom and move it to the kitchen. This is your first, most important step in building a wall of friction.</p>
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
