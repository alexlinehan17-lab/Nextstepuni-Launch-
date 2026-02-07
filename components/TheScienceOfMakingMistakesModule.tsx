/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
*/

import React, { useState } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { 
  ArrowLeft, CheckCircle2, ArrowRight, 
  Lock, Flag, AlertTriangle, Lightbulb, ToggleRight, ZapOff, Wrench
} from 'lucide-react';

interface TheScienceOfMakingMistakesModuleProps {
  onBack: () => void;
}

const Highlight = ({ children, description, color = "bg-red-100/40", textColor = "text-red-900", decorColor = "decoration-red-400/40", hoverColor="hover:bg-red-200/60" }: { children?: React.ReactNode, description: string, color?: string, textColor?: string, decorColor?: string, hoverColor?: string }) => {
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
              <p className="font-sans font-bold text-red-400 mb-2 uppercase tracking-[0.2em] text-[9px]">The Academic Insight</p>
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
        <div className="w-12 h-12 rounded-2xl bg-stone-900 flex items-center justify-center text-red-400 shadow-xl border border-white/10">
          <Icon size={24} />
        </div>
      </div>
      <span className="inline-flex items-center gap-2 px-3 py-1 bg-red-50 text-red-600 text-[10px] font-black tracking-[0.4em] uppercase rounded-full mb-4">
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
  <div className="my-12 p-8 bg-red-50/50 border-2 border-dashed border-red-200 rounded-3xl">
    <div className="flex items-start gap-5">
      <div className="w-11 h-11 rounded-xl bg-red-500 text-white flex items-center justify-center shrink-0 mt-1 shadow-lg shadow-red-500/20">
        <Flag size={20} />
      </div>
      <div>
        <h4 className="font-bold text-red-800 text-sm uppercase tracking-widest">Your Mission (Under 5 Mins)</h4>
        <div className="text-stone-600 mt-2 font-medium leading-relaxed">
          {children}
        </div>
      </div>
    </div>
  </div>
);

const ActivityRing = ({ progress, color = "#dc2626" }: { progress: number, color?: string }) => {
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
const BrainSignalVisualizer = () => {
    const [active, setActive] = useState(false);
    return(
        <div className="my-10 p-8 md:p-12 bg-white rounded-[3rem] border border-stone-200 shadow-xl">
             <h4 className="font-serif text-2xl font-bold text-stone-800 text-center italic">The Brain's Two Signals</h4>
             <p className="text-center text-sm text-stone-500 mb-8">When you make a mistake, your brain sends two distinct signals in less than half a second.</p>
             <div className="w-full max-w-lg mx-auto h-32 relative">
                <svg viewBox="0 0 300 100" className="w-full h-full absolute inset-0">
                    <path d="M0 50 L 300 50" stroke="#e5e7eb" strokeWidth="1" />
                    <AnimatePresence>
                    {active && <>
                        <motion.path initial={{pathLength:0}} animate={{pathLength:1}} transition={{duration:0.2, delay: 0.1}} d="M 50 50 C 60 50 65 20 75 20 S 90 50 100 50" stroke="#f43f5e" strokeWidth="2" fill="none" />
                        <motion.path initial={{pathLength:0}} animate={{pathLength:1}} transition={{duration:0.5, delay: 0.3}} d="M 150 50 C 160 50 175 80 190 80 S 210 50 220 50" stroke="#10b981" strokeWidth="2" fill="none" />
                    </>}
                    </AnimatePresence>
                </svg>
                {active && <>
                    <motion.div initial={{opacity:0}} animate={{opacity:1, transition:{delay:0.2}}} className="absolute top-0 left-[75px] -translate-x-1/2 text-center text-xs">
                        <p className="font-bold text-rose-600">ERN Signal</p>
                        <p className="text-stone-500">The "Alarm"</p>
                    </motion.div>
                    <motion.div initial={{opacity:0}} animate={{opacity:1, transition:{delay:0.5}}} className="absolute bottom-0 left-[190px] -translate-x-1/2 text-center text-xs">
                        <p className="font-bold text-emerald-600">Pe Signal</p>
                        <p className="text-stone-500">The "Analysis"</p>
                    </motion.div>
                </>}
             </div>
             <div className="text-center mt-8">
                <button onClick={() => setActive(!active)} className="px-5 py-3 bg-stone-800 text-white font-bold rounded-lg text-sm">{active ? "Reset" : "Make a Mistake"}</button>
             </div>
        </div>
    );
};


// --- MODULE COMPONENT ---
export const TheScienceOfMakingMistakesModule: React.FC<TheScienceOfMakingMistakesModuleProps> = ({ onBack }) => {
  const [activeSection, setActiveSection] = useState(0);
  const [unlockedSection, setUnlockedSection] = useState(0);
  
  const sections = [
    { id: 'brain-alarm', title: "The Brain's Alarm", eyebrow: '01 // The "Uh-Oh" Signal', icon: AlertTriangle },
    { id: 'second-signal', title: 'The Second Signal', eyebrow: '02 // The Analysis', icon: Lightbulb },
    { id: 'mindset-switch', title: 'The Mindset Switch', eyebrow: '03 // Leaning In', icon: ToggleRight },
    { id: 'high-stakes-hijack', title: 'The High-Stakes Hijack', eyebrow: '04 // The Leaving Cert Brain', icon: ZapOff },
    { id: 'error-toolkit', title: 'Your Error Toolkit', eyebrow: '05 // Rewiring Your Brain', icon: Wrench },
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
            <p className="text-[9px] font-black text-red-500 uppercase tracking-[0.4em] mb-0.5 underline">Module 05</p>
            <h1 className="font-serif font-bold text-lg tracking-tight text-stone-900">The Science of Mistakes</h1>
          </div>
        </div>

        <div className="flex-grow space-y-4 overflow-y-auto no-scrollbar pr-2 relative">
          <div className="absolute left-[21px] top-6 bottom-6 w-0.5 bg-stone-100 -z-0" />
          <div className="absolute left-[21px] top-6 bottom-6 w-0.5">
              <motion.div
                  className="w-full bg-red-500 shadow-[0_0_10px_rgba(220,38,38,0.5)]"
                  initial={{ height: 0 }}
                  animate={{ height: sections.length > 1 ? `${(unlockedSection / (sections.length - 1)) * 100}%` : '0%' }}
              />
          </div>
          {sections.map((section, idx) => {
            const isUnlocked = idx <= unlockedSection;
            const isActive = idx === activeSection;
            const isCompleted = idx < unlockedSection;
            return (
              <button key={section.id} disabled={!isUnlocked} onClick={() => handleJumpToSection(idx)} className={`relative z-10 w-full flex items-center gap-4 p-3 rounded-xl transition-all duration-500 text-left group ${isActive ? 'bg-red-50 shadow-sm translate-x-2' : ''} ${!isUnlocked ? 'opacity-40 grayscale cursor-not-allowed' : 'hover:bg-stone-50'}`}>
                <div className={`w-11 h-11 rounded-xl flex items-center justify-center shrink-0 border-2 transition-all duration-500 ${isCompleted ? 'bg-red-600 border-red-600 text-white shadow-lg' : isActive ? 'bg-white border-red-500 text-red-600 shadow-xl rotate-12' : 'bg-white border-stone-200 text-stone-300'}`}>
                   {isCompleted ? <CheckCircle2 size={18} /> : isActive ? <section.icon size={18} /> : <Lock size={16} />}
                </div>
                <div className="flex-grow"><p className={`text-[8px] font-black uppercase tracking-widest ${isActive ? 'text-red-500' : 'text-stone-400'}`}>{section.eyebrow.split('// ')[1]}</p><h4 className={`text-xs font-bold leading-tight ${isActive ? 'text-stone-900' : 'text-stone-500'}`}>{section.title}</h4></div>
              </button>
            );
          })}
        </div>
        <div className="mt-8 border-t border-stone-100 pt-8 flex flex-col items-center">
           <ActivityRing progress={progress} color="#dc2626" /><p className="text-[11px] font-black text-stone-900 uppercase tracking-widest text-center">Progress</p>
        </div>
      </aside>
      <main className="flex-grow flex flex-col items-center py-10 md:py-24 px-6 md:px-16 overflow-y-auto h-screen relative">
        <div className="absolute inset-0 bg-[radial-gradient(#e5e7eb_1px,transparent_1px)] [background-size:32px_32px] opacity-40 pointer-events-none" />
        <div className="w-full max-w-4xl relative z-10">
          <AnimatePresence mode="wait">
            <motion.div key={activeSection} initial={{ opacity: 0, x: 20 }} animate={{ opacity: 1, x: 0 }} exit={{ opacity: 0, x: -20 }} transition={{ duration: 0.6, ease: [0.16, 1, 0.3, 1] }}>
              {activeSection === 0 && (
                <ReadingSection title="The Brain's Alarm." eyebrow="Step 1" icon={AlertTriangle}>
                  <p>When you make a mistake—a typo, a wrong turn in a maths problem—your brain registers it instantly. Before you are even consciously aware of it, an electrical signal called the <Highlight description="A neural signal of error detection that occurs within 50 milliseconds of a mistake. It is an unconscious 'uh-oh' signal originating from the anterior cingulate cortex.">Error-Related Negativity (ERN)</Highlight> fires. It's a super-fast, automatic "uh-oh" moment.</p>
                  <p>Think of it as your brain's smoke detector. It's a primitive, unconscious alarm that goes off when your actions don't match your intentions. This signal is crucial, but it's not the part that drives learning. It's what happens next that separates high-performers from the rest.</p>
                </ReadingSection>
              )}
               {activeSection === 1 && (
                <ReadingSection title="The Second Signal." eyebrow="Step 2" icon={Lightbulb}>
                  <p>About 200-500 milliseconds after the initial alarm, a second, larger brainwave can occur. This is the <Highlight description="A later neural signal (200-500ms post-error) that reflects conscious attention to and awareness of the mistake. The amplitude of the Pe wave is a strong predictor of post-error correction and learning.">Error Positivity (Pe)</Highlight> signal. This isn't automatic. This is the signal of your conscious brain paying attention to the mistake, analyzing it, and engaging with it. It's the moment your brain decides to learn from the error.</p>
                  <p>You can think of it like this: the ERN is the smoke alarm beeping. The Pe is you getting out of bed to find the source of the smoke. The size of your Pe wave literally predicts how likely you are to correct the error and get it right next time. It's the neurobiological signature of giving a damn about your mistakes.</p>
                  <BrainSignalVisualizer />
                </ReadingSection>
              )}
              {activeSection === 2 && (
                <ReadingSection title="The Mindset Switch." eyebrow="Step 3" icon={ToggleRight}>
                  <p>Here's where it gets fascinating. Neuroscientists have shown that the size of your Pe wave is directly controlled by your mindset. Students with a <Highlight description="The belief that intelligence is a fixed trait. People with this mindset tend to see errors as a threat to their ego.">Fixed Mindset</Highlight> show a much smaller Pe signal. They hear the alarm, but they quickly "look away" from the mistake because it feels like a threat to their self-concept. If "being smart" is your identity, then a mistake is evidence that you're not.</p>
                  <p>Students with a <Highlight description="The belief that intelligence can be grown through effort and strategy. They see errors as an opportunity to learn and improve.">Growth Mindset</Highlight> have a huge Pe signal. They lean into the mistake, allocating massive attentional resources to it. They understand that the error isn't a verdict on their ability; it's a crucial piece of data for improvement. They are hungry for the information contained within the failure.</p>
                </ReadingSection>
              )}
               {activeSection === 3 && (
                <ReadingSection title="The High-Stakes Hijack." eyebrow="Step 4" icon={ZapOff}>
                    <p>This whole system can be hijacked by stress. In a high-stakes situation like the Leaving Cert, the fear of failure can trigger an <Highlight description="An intense emotional response that is out of proportion to the real threat, caused by the amygdala overriding the rational prefrontal cortex.">amygdala hijack</Highlight>. This floods your brain with stress hormones like cortisol.</p>
                    <p>High cortisol levels do two terrible things. First, they impair the function of your prefrontal cortex, making it harder to think clearly. Second, they suppress the Pe signal. Your brain shifts from a "learning focus" to a "threat focus." It stops trying to analyse the mistake and starts trying to just survive the experience. This is why you can "go blank" after one mistake and find it impossible to recover.</p>
                </ReadingSection>
              )}
               {activeSection === 4 && (
                <ReadingSection title="Your Error Toolkit." eyebrow="Step 5" icon={Wrench}>
                  <p>The good news is you can train your brain to have a bigger Pe signal and be more resilient under pressure. It's a skill. The first step is to **de-shame mistakes**. See them as data, not as judgments on your character. Every error is a signpost pointing to exactly where you need to grow.</p>
                  <p>The most powerful tool for this is a <Highlight description="A dedicated notebook or document where you log every mistake you make in practice, diagnose its cause (e.g., slip, gap, misconception), and prescribe a specific action to fix it.">Mistake Log</Highlight>. This forces you to engage with your errors in a structured, analytical way. It's a manual override that forces your brain to generate a strong Pe signal. Don't just find your mistakes; interrogate them. They are your best teachers.</p>
                   <MicroCommitment>
                    <p>For your next piece of homework, actively look for one mistake you made. Don't just correct it. Write down in one sentence *why* you made it. You've just started your first mistake log.</p>
                  </MicroCommitment>
                </ReadingSection>
              )}
              <footer className="mt-24 flex items-center justify-between pt-12 border-t border-stone-200/60 px-4">
                <motion.button whileHover={{ scale: 1.05 }} whileTap={{ scale: 0.95 }} onClick={handlePrev} disabled={activeSection === 0} className={`flex items-center gap-4 bg-stone-100 text-stone-800 px-8 py-4 rounded-xl font-black text-[10px] uppercase tracking-widest transition-all shadow-sm ${activeSection === 0 ? 'opacity-0 pointer-events-none' : ''}`}>
                  <ArrowLeft size={16} /> Prev
                </motion.button>
                <motion.button whileHover={{ scale: 1.05 }} whileTap={{ scale: 0.95 }} onClick={handleCompleteSection} className="group relative flex items-center gap-4 bg-stone-900 text-white px-12 py-6 rounded-2xl font-black text-[12px] uppercase tracking-widest hover:bg-red-600 transition-all shadow-[0_20px_50px_rgba(0,0,0,0.2)] overflow-hidden">
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