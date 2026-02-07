/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
*/

import React, { useState } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { 
  ArrowLeft, CheckCircle2, ArrowRight, 
  Lock, Flag, Link2, Brain, Wand2, Gamepad2, Briefcase, DraftingCompass, Wind
} from 'lucide-react';

interface ConnectingEducationToGoalsModuleProps {
  onBack: () => void;
}

const Highlight = ({ children, description, color = "bg-fuchsia-100/40", textColor = "text-fuchsia-900", decorColor = "decoration-fuchsia-400/40", hoverColor="hover:bg-fuchsia-200/60" }: { children?: React.ReactNode, description: string, color?: string, textColor?: string, decorColor?: string, hoverColor?: string }) => {
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
              <p className="font-sans font-bold text-fuchsia-400 mb-2 uppercase tracking-[0.2em] text-[9px]">The Academic Insight</p>
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
        <div className="w-12 h-12 rounded-2xl bg-stone-900 flex items-center justify-center text-fuchsia-400 shadow-xl border border-white/10">
          <Icon size={24} />
        </div>
      </div>
      <span className="inline-flex items-center gap-2 px-3 py-1 bg-fuchsia-50 text-fuchsia-600 text-[10px] font-black tracking-[0.4em] uppercase rounded-full mb-4">
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
  <div className="my-12 p-8 bg-fuchsia-50/50 border-2 border-dashed border-fuchsia-200 rounded-3xl">
    <div className="flex items-start gap-5">
      <div className="w-11 h-11 rounded-xl bg-fuchsia-500 text-white flex items-center justify-center shrink-0 mt-1 shadow-lg shadow-fuchsia-500/20">
        <Flag size={20} />
      </div>
      <div>
        <h4 className="font-bold text-fuchsia-800 text-sm uppercase tracking-widest">Your Mission (Under 5 Mins)</h4>
        <div className="text-stone-600 mt-2 font-medium leading-relaxed">
          {children}
        </div>
      </div>
    </div>
  </div>
);

const ActivityRing = ({ progress, color = "#d946ef" }: { progress: number, color?: string }) => {
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

const WOOPPlanner = () => {
    const [data, setData] = useState({wish: '', outcome: '', obstacle: '', plan: ''});
    const update = (field: string, value: string) => setData(prev => ({...prev, [field]: value}));

    return (
        <div className="my-10 p-8 md:p-12 bg-white rounded-[3rem] border border-stone-200 shadow-xl">
            <h4 className="font-serif text-2xl font-bold text-stone-800 text-center italic">My WOOP Blueprint</h4>
            <div className="space-y-4 mt-6">
                <input value={data.wish} onChange={e => update('wish', e.target.value)} placeholder="WISH: What do you want to achieve?" className="w-full p-3 bg-stone-50 rounded-lg"/>
                <input value={data.outcome} onChange={e => update('outcome', e.target.value)} placeholder="OUTCOME: What's the best feeling if you do?" className="w-full p-3 bg-stone-50 rounded-lg"/>
                <input value={data.obstacle} onChange={e => update('obstacle', e.target.value)} placeholder="OBSTACLE: What *inside you* holds you back?" className="w-full p-3 bg-stone-50 rounded-lg"/>
                <input value={data.plan} onChange={e => update('plan', e.target.value)} placeholder="PLAN: If [obstacle], then I will..." className="w-full p-3 bg-stone-50 rounded-lg"/>
            </div>
        </div>
    );
};

// --- MODULE COMPONENT ---
export const ConnectingEducationToGoalsModule: React.FC<{onBack: () => void}> = ({ onBack }) => {
  const [activeSection, setActiveSection] = useState(0);
  const [unlockedSection, setUnlockedSection] = useState(0);
  
  const sections = [
    { id: 'time-horizon', title: 'The Time Horizon Problem', eyebrow: '01 // The Why', icon: Wind },
    { id: 'motivation-engine', title: 'The Engine of Motivation', eyebrow: '02 // The Fuel', icon: Brain },
    { id: 'impossibility-heuristic', title: 'The "Impossibility" Heuristic', eyebrow: '03 // The Reframe', icon: Wand2 },
    { id: 'structural-levers', title: 'Hacking the System', eyebrow: '04 // The Levers', icon: Briefcase },
    { id: 'playbook-motivation', title: 'Playbook: The "Why"', eyebrow: '05 // Motivation & Identity', icon: Gamepad2 },
    { id: 'playbook-action', title: 'Playbook: The "How" & "What"', eyebrow: '06 // The Action Plan', icon: Link2 },
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
            <p className="text-[9px] font-black text-fuchsia-500 uppercase tracking-[0.4em] mb-0.5 underline">Module 14</p>
            <h1 className="font-serif font-bold text-lg tracking-tight text-stone-900">Connecting to Goals</h1>
          </div>
        </div>

        <div className="flex-grow space-y-4 overflow-y-auto no-scrollbar pr-2 relative">
          <div className="absolute left-[21px] top-6 bottom-6 w-0.5 bg-stone-100 -z-0" />
          <div className="absolute left-[21px] top-6 bottom-6 w-0.5">
              <motion.div
                  className="w-full bg-fuchsia-500 shadow-[0_0_10px_rgba(217,70,239,0.5)]"
                  initial={{ height: 0 }}
                  animate={{ height: sections.length > 1 ? `${(unlockedSection / (sections.length - 1)) * 100}%` : '0%' }}
              />
          </div>
          {sections.map((section, idx) => {
            const isUnlocked = idx <= unlockedSection;
            const isActive = idx === activeSection;
            const isCompleted = idx < unlockedSection;
            return (
              <button key={section.id} disabled={!isUnlocked} onClick={() => handleJumpToSection(idx)} className={`relative z-10 w-full flex items-center gap-4 p-3 rounded-xl transition-all duration-500 text-left group ${isActive ? 'bg-fuchsia-50 shadow-sm translate-x-2' : ''} ${!isUnlocked ? 'opacity-40 grayscale cursor-not-allowed' : 'hover:bg-stone-50'}`}>
                <div className={`w-11 h-11 rounded-xl flex items-center justify-center shrink-0 border-2 transition-all duration-500 ${isCompleted ? 'bg-fuchsia-600 border-fuchsia-600 text-white shadow-lg' : isActive ? 'bg-white border-fuchsia-500 text-fuchsia-600 shadow-xl rotate-12' : 'bg-white border-stone-200 text-stone-300'}`}>
                   {isCompleted ? <CheckCircle2 size={18} /> : isActive ? <section.icon size={18} /> : <Lock size={16} />}
                </div>
                <div className="flex-grow"><p className={`text-[8px] font-black uppercase tracking-widest ${isActive ? 'text-fuchsia-500' : 'text-stone-400'}`}>{section.eyebrow.split('// ')[1]}</p><h4 className={`text-xs font-bold leading-tight ${isActive ? 'text-stone-900' : 'text-stone-500'}`}>{section.title}</h4></div>
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
                <ReadingSection title="The Time Horizon Problem." eyebrow="Step 1" icon={Wind}>
                  <p>Why is it so hard to study for a future that feels a million miles away? The science shows that psychological time isn't constant. Your <Highlight description="The extent to which you integrate the future into your present planning. It's a key cognitive resource for long-term goals.">Future Time Perspective (FTP)</Highlight> is a cognitive resource, and it's unequally distributed. Students from unstable environments often develop a rational, short-term "present-fatalistic" focus. This is a survival skill, but it's "maladaptive" for the long-game of education.</p>
                  <p>This isn't a character flaw. It's about bridging the gap. The goal is to make the future feel closer and more connected to today's actions. This is a psychological intervention that recruits neural circuitry to override the immediate pressures of disadvantage.</p>
                </ReadingSection>
              )}
               {activeSection === 1 && (
                <ReadingSection title="The Engine of Motivation." eyebrow="Step 2" icon={Brain}>
                  <p><Highlight description="A major theory of human motivation that focuses on the degree to which an individual’s behavior is self-motivated and self-determined.">Self-Determination Theory (SDT)</Highlight> explains the fuel for this journey. Motivation runs on a spectrum from "controlled" (doing it to avoid getting in trouble) to "autonomous" (doing it because you value it). The most potent form for academic success is <Highlight description="A type of autonomous motivation where you engage in a task because you personally value its outcome, even if the task itself isn't enjoyable.">Identified Regulation</Highlight>—you've accepted the goal as your own.</p>
                  <p>Crucially, research shows that for students from low-income backgrounds, the feeling of connection to the future ONLY works if it triggers these self-regulation strategies. "Dreaming big" is not enough. The dream must be converted into daily habits.</p>
                </ReadingSection>
              )}
              {activeSection === 2 && (
                <ReadingSection title="The 'Impossibility' Heuristic." eyebrow="Step 3" icon={Wand2}>
                  <p>When does a task feel "worth doing," and when does it feel "impossible"? <Highlight description="A theory stating that we are motivated to act in ways that are congruent with our identities.">Identity-Based Motivation (IBM)</Highlight> theory has the answer. It's about how you interpret difficulty. When a task feels "like me," difficulty is seen as **importance**. ("This is hard, so it must be worth it.") When a task feels alien, difficulty is seen as **impossibility**. ("This is hard, so it's not for people like me.")</p>
                  <p>This "impossibility heuristic" is a major barrier for students from disadvantaged backgrounds. The key is to reframe your identity—to see academic struggle not as a sign you don't belong, but as a challenge you are uniquely equipped to handle due to your resilience.</p>
                </ReadingSection>
              )}
              {activeSection === 3 && (
                <ReadingSection title="Hacking the System." eyebrow="Step 4" icon={Briefcase}>
                  <p>The Irish education system has real structural barriers, like the "grinds" industry. But it also has powerful structural levers designed to help you. These are not handouts; they are tools to level the playing field. Understanding them is a critical part of your strategy.</p>
                  <p>The main levers are the <Highlight description="Higher Education Access Route: A scheme that offers reduced points places to students from socio-economically disadvantaged backgrounds.">HEAR</Highlight> and <Highlight description="Disability Access Route to Education: A scheme that supports students whose education has been impacted by a disability.">DARE</Highlight> schemes, which offer reduced points for college entry, and the <Highlight description="Student Universal Support Ireland: The main financial grant for third-level education in Ireland.">SUSI</Highlight> grant, which provides financial support. Knowing the deadlines and eligibility criteria is not optional; it's part of the curriculum.</p>
                </ReadingSection>
              )}
               {activeSection === 4 && (
                <ReadingSection title="Playbook: The 'Why'." eyebrow="Step 5" icon={Gamepad2}>
                  <p>This is where theory becomes action. The first phase is to build your "why"—a Future Time Perspective strong enough to withstand the stress of the exam year. There are two core exercises.</p>
                  <p>The first is the <Highlight description="A powerful, four-step goal-setting strategy: Wish, Outcome, Obstacle, Plan. It combines positive thinking with a realistic assessment of barriers.">WOOP Method</Highlight>. It's a scientifically-validated way to connect a long-term goal to your immediate actions. The second is <Highlight description="A brief writing exercise about your core personal values (e.g., family, creativity). It has been proven to buffer the brain against stress and raise grades in low-SES students.">Self-Affirmation Journaling</Highlight>, which acts as a psychological shield against "Stereotype Threat" (the fear that 'people like me' don't succeed).</p>
                  <WOOPPlanner />
                </ReadingSection>
              )}
              {activeSection === 5 && (
                <ReadingSection title="Playbook: The 'How' & 'What'." eyebrow="Step 6" icon={Link2}>
                  <p>Once your "Why" is established, you need the "How" and the "What." The "How" is about using high-impact learning techniques that are free and outperform expensive grinds. This means prioritizing <Highlight description="The 'Testing Effect.' Forcing your brain to retrieve information is the single most effective way to build durable memory.">Retrieval Practice</Highlight> ("Brain Dumps") over passive re-reading, and using a <Highlight description="A simple schedule of reviewing material on Day 1, Day 2, Day 7, and Day 30 to move information into long-term memory.">Spaced Repetition</Highlight> schedule.</p>
                  <p>The "What" is about using every structural advantage available. You must conduct a **HEAR & DARE Audit** early in 6th year. You must become a **SUSI Maximizer**, checking your distance from college for the "Non-Adjacent" rate. And you must find **Free "Grinds"** through university access programs and high-quality YouTube channels. This is not just studying; it's system hacking.</p>
                  <MicroCommitment>
                    <p>Go to Google Maps right now. Check the distance from your house to your dream college course. Is it over 30km? You may have just found thousands of euro in extra SUSI funding.</p>
                  </MicroCommitment>
                </ReadingSection>
              )}
              <footer className="mt-24 flex items-center justify-between pt-12 border-t border-stone-200/60 px-4">
                <motion.button whileHover={{ scale: 1.05 }} whileTap={{ scale: 0.95 }} onClick={handlePrev} disabled={activeSection === 0} className={`flex items-center gap-4 bg-stone-100 text-stone-800 px-8 py-4 rounded-xl font-black text-[10px] uppercase tracking-widest transition-all shadow-sm ${activeSection === 0 ? 'opacity-0 pointer-events-none' : ''}`}>
                  <ArrowLeft size={16} /> Prev
                </motion.button>
                <motion.button whileHover={{ scale: 1.05 }} whileTap={{ scale: 0.95 }} onClick={handleCompleteSection} className="group relative flex items-center gap-4 bg-stone-900 text-white px-12 py-6 rounded-2xl font-black text-[12px] uppercase tracking-widest hover:bg-fuchsia-600 transition-all shadow-[0_20px_50px_rgba(0,0,0,0.2)] overflow-hidden">
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
