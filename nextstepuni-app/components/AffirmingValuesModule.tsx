

/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
*/

import React, { useState, useEffect } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { 
  ArrowLeft, CheckCircle2, ArrowRight, 
  BrainCircuit, Shield,
  Lock, Flag, AlertTriangle, UserCheck
} from 'lucide-react';

type ModuleProgress = {
  unlockedSection: number;
};

interface AffirmingValuesModuleProps {
  onBack: () => void;
  progress: ModuleProgress;
  onProgressUpdate: (progress: ModuleProgress) => void;
}

const Highlight = ({ children, description, color = "bg-blue-100/40", textColor = "text-blue-900", decorColor = "decoration-blue-400/40", hoverColor="hover:bg-blue-200/60" }: { children?: React.ReactNode, description: string, color?: string, textColor?: string, decorColor?: string, hoverColor?: string }) => {
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
              <p className="font-sans font-bold text-blue-400 mb-2 uppercase tracking-[0.2em] text-[9px]">The Academic Insight</p>
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
        <div className="w-12 h-12 rounded-2xl bg-stone-900 flex items-center justify-center text-blue-400 shadow-xl border border-white/10">
          <Icon size={24} />
        </div>
      </div>
      <span className="inline-flex items-center gap-2 px-3 py-1 bg-blue-50 text-blue-600 text-[10px] font-black tracking-[0.4em] uppercase rounded-full mb-4">
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
  <div className="my-12 p-8 bg-blue-50/50 border-2 border-dashed border-blue-200 rounded-3xl">
    <div className="flex items-start gap-5">
      <div className="w-11 h-11 rounded-xl bg-blue-500 text-white flex items-center justify-center shrink-0 mt-1 shadow-lg shadow-blue-500/20">
        <Flag size={20} />
      </div>
      <div>
        <h4 className="font-bold text-blue-800 text-sm uppercase tracking-widest">Your Mission (Under 5 Mins)</h4>
        <div className="text-stone-600 mt-2 font-medium leading-relaxed">
          {children}
        </div>
      </div>
    </div>
  </div>
);

const ActivityRing = ({ progress, color = "#3b82f6" }: { progress: number, color?: string }) => {
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

const ValuesSelector = () => {
    const values = ["Family", "Friendship", "Creativity", "Kindness", "Humour", "Ambition", "Community", "Independence", "Learning"];
    const [selected, setSelected] = useState<string[]>([]);
    
    const handleSelect = (value: string) => {
        if (selected.includes(value)) {
            setSelected(selected.filter(v => v !== value));
        } else if (selected.length < 3) {
            setSelected([...selected, value]);
        }
    };

    return(
        <div className="my-10 p-8 md:p-12 bg-white rounded-[3rem] border border-stone-200 shadow-xl">
             <h4 className="font-serif text-2xl font-bold text-stone-800 text-center italic">Core Values Audit</h4>
             <p className="text-center text-sm text-stone-500 mb-8">Select your top 3 most important personal values.</p>
             <div className="flex flex-wrap justify-center gap-3">
                {values.map(value => (
                    <motion.button 
                        key={value}
                        onClick={() => handleSelect(value)}
                        className={`px-4 py-2 text-sm font-bold rounded-full border-2 transition-all ${selected.includes(value) ? 'bg-blue-500 text-white border-blue-500' : 'bg-stone-50 border-stone-200'}`}
                        whileHover={{y: -2}}
                    >
                        {value}
                    </motion.button>
                ))}
             </div>
             {selected.length === 3 && (
                <div className="mt-8">
                    <h5 className="font-bold text-center">Your 15-Minute Writing Prompt:</h5>
                    <p className="p-4 bg-stone-100 rounded-xl mt-2 text-center text-sm">Choose ONE of these values: <span className="font-bold">{selected.join(', ')}</span>. Write for 15 minutes about why this value is important to you and describe a time when you lived up to it.</p>
                </div>
             )}
        </div>
    );
};


// --- MODULE COMPONENT ---
export const AffirmingValuesModule: React.FC<AffirmingValuesModuleProps> = ({ onBack, progress, onProgressUpdate }) => {
  const [activeSection, setActiveSection] = useState(progress.unlockedSection);
  const unlockedSection = progress.unlockedSection;

  const sections = [
    { id: 'invisible-threat', title: 'The Invisible Threat', eyebrow: '01 // The Problem', icon: AlertTriangle },
    { id: 'psychological-shield', title: 'The Psychological Shield', eyebrow: '02 // The Solution', icon: Shield },
    { id: 'broaden-build', title: 'How It Works: "Broaden-and-Build"', eyebrow: '03 // The Mechanism', icon: BrainCircuit },
    { id: 'real-world-data', title: 'The Real World Data', eyebrow: '04 // The Evidence', icon: UserCheck }, // Changed Icon
    { id: 'your-protocol', title: 'Your Pre-Exam Protocol', eyebrow: '05 // The Action Plan', icon: UserCheck },
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
            <p className="text-[9px] font-black text-blue-500 uppercase tracking-[0.4em] mb-0.5 underline">Module 03</p>
            <h1 className="font-serif font-bold text-lg tracking-tight text-stone-900">Affirming Values</h1>
          </div>
        </div>

        <div className="flex-grow space-y-4 overflow-y-auto no-scrollbar pr-2 relative">
          <div className="absolute left-[21px] top-6 bottom-6 w-0.5 bg-stone-100 -z-0" />
          <div className="absolute left-[21px] top-6 bottom-6 w-0.5">
              <motion.div
                  className="w-full bg-blue-500 shadow-[0_0_10px_rgba(59,130,246,0.5)]"
                  style={{ height: `${progressPercentage}%` }}
              />
          </div>
          {sections.map((section, idx) => {
            const isUnlocked = idx <= unlockedSection;
            const isActive = idx === activeSection;
            const isCompleted = idx < unlockedSection;
            return (
              <button key={section.id} disabled={!isUnlocked} onClick={() => handleJumpToSection(idx)} className={`relative z-10 w-full flex items-center gap-4 p-3 rounded-xl transition-all duration-500 text-left group ${isActive ? 'bg-blue-50 shadow-sm translate-x-2' : ''} ${!isUnlocked ? 'opacity-40 grayscale cursor-not-allowed' : 'hover:bg-stone-50'}`}>
                <div className={`w-11 h-11 rounded-xl flex items-center justify-center shrink-0 border-2 transition-all duration-500 ${isCompleted ? 'bg-blue-600 border-blue-600 text-white shadow-lg' : isActive ? 'bg-white border-blue-500 text-blue-600 shadow-xl rotate-12' : 'bg-white border-stone-200 text-stone-300'}`}>
                   {isCompleted ? <CheckCircle2 size={18} /> : isActive ? <section.icon size={18} /> : <Lock size={16} />}
                </div>
                <div className="flex-grow"><p className={`text-[8px] font-black uppercase tracking-widest ${isActive ? 'text-blue-500' : 'text-stone-400'}`}>{section.eyebrow.split('// ')[1]}</p><h4 className={`text-xs font-bold leading-tight ${isActive ? 'text-stone-900' : 'text-stone-500'}`}>{section.title}</h4></div>
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
                <ReadingSection title="The Invisible Threat." eyebrow="Step 1" icon={AlertTriangle}>
                  <p>In a high-stakes situation like the Leaving Cert, your brain is on high alert for threats. For students from disadvantaged backgrounds, there's an extra, invisible threat in the room: the fear that a poor performance will confirm a negative stereotype about your group. This is called <Highlight description="A situational predicament in which individuals are at risk of confirming negative stereotypes about their social group. This adds extra cognitive load, which can impair performance.">Stereotype Threat</Highlight>.</p>
                  <p>It's a cognitive tax. Part of your precious working memory gets hijacked by this background anxiety, leaving less capacity for the actual exam questions. This isn't just "in your head"—it's a measurable physiological stress response that can sabotage your performance, even if you know the material perfectly.</p>
                </ReadingSection>
              )}
               {activeSection === 1 && (
                <ReadingSection title="The Psychological Shield." eyebrow="Step 2" icon={Shield}>
                  <p>For decades, psychologists have been searching for a "vaccine" against this threat. The most powerful and replicable intervention is astonishingly simple: a 15-minute writing exercise called <Highlight description="A brief psychological intervention where individuals write about their core personal values. This has been shown to buffer against stress and improve performance in high-pressure situations.">Self-Affirmation</Highlight>.</p>
                  <p>It sounds too good to be true, but the data is overwhelming. By taking a few moments before a stressful event to write about what's truly important to you (like family, creativity, or friendship), you create a psychological "shield." You remind your brain that your self-worth is not solely defined by the exam you're about to take. This frees up the cognitive resources that stereotype threat would otherwise steal.</p>
                </ReadingSection>
              )}
               {activeSection === 2 && (
                <ReadingSection title="How It Works: 'Broaden-and-Build'." eyebrow="Step 3" icon={BrainCircuit}>
                  <p>How can a simple writing exercise have such a powerful effect? It's not magic; it's neuroscience. According to Barbara Fredrickson's <Highlight description="A theory in positive psychology that suggests positive emotions (like the feeling of self-worth from an affirmation) broaden a person's mindset and help build their psychological, social, and intellectual resources.">Broaden-and-Build Theory</Highlight>, negative emotions (like fear) narrow your focus to a single threat. Positive emotions, on the other hand, do the opposite: they broaden your perspective.</p>
                  <p>When you affirm your core values, you activate brain regions associated with self-processing and reward (like the ventromedial prefrontal cortex). This creates a moment of positive emotion that "zooms out" your perspective. The exam is no longer a life-or-death verdict on your entire identity; it's just one part of a much larger, more meaningful life. This cognitive 'broadening' is what reduces the threat and frees up your working memory.</p>
                </ReadingSection>
              )}
              {activeSection === 3 && (
                <ReadingSection title="The Real World Data." eyebrow="Step 4" icon={UserCheck}>
                  <p>In a landmark study by Cohen et al. (2006), they gave a values affirmation exercise to a group of African American middle-school students. The results were staggering. This simple, 15-minute exercise, done just a few times a year, boosted the grades of the students by an average of 0.3 grade points.</p>
                  <p>Even more remarkably, two years later, the students who had done the exercise were still outperforming their peers. The intervention had set off a "virtuous cycle"—better grades led to more confidence, which led to even better grades. The effect was most powerful for the students who were most at risk of underperforming. This is one of the most effective psychological interventions ever discovered.</p>
                </ReadingSection>
              )}
               {activeSection === 4 && (
                <ReadingSection title="Your Pre-Exam Protocol." eyebrow="Step 5" icon={UserCheck}>
                  <p>You now have a scientifically-proven tool to protect your brain under pressure. The final step is to turn it into a concrete, pre-exam ritual. Before every major exam (especially the Mocks and the Leaving Cert itself), you will run the Self-Affirmation Protocol.</p>
                  <p>The steps are simple: **1. Identify your core values.** **2. Choose the one that feels most important to you right now.** **3. Write for 15 minutes.** This isn't an essay; it's a private reflection. Write about why the value is important and describe a specific time you lived up to it. This isn't a "nice to have"; it's a cognitive warm-up as important as checking your pens.</p>
                  <ValuesSelector />
                  <MicroCommitment>
                    <p>Take the values you selected above. Create a recurring event in your phone's calendar for the morning of every exam you have this year, with the title: "15 Min Values Affirmation." You've just weaponized positive psychology.</p>
                  </MicroCommitment>
                </ReadingSection>
              )}
              <footer className="mt-24 flex items-center justify-between pt-12 border-t border-stone-200/60 px-4">
                <motion.button whileHover={{ scale: 1.05 }} whileTap={{ scale: 0.95 }} onClick={handlePrev} disabled={activeSection === 0} className={`flex items-center gap-4 bg-stone-100 text-stone-800 px-8 py-4 rounded-xl font-black text-[10px] uppercase tracking-widest transition-all shadow-sm ${activeSection === 0 ? 'opacity-0 pointer-events-none' : ''}`}>
                  <ArrowLeft size={16} /> Prev
                </motion.button>
                <motion.button whileHover={{ scale: 1.05 }} whileTap={{ scale: 0.95 }} onClick={handleCompleteSection} className="group relative flex items-center gap-4 bg-stone-900 text-white px-12 py-6 rounded-2xl font-black text-[12px] uppercase tracking-widest hover:bg-blue-600 transition-all shadow-[0_20px_50px_rgba(0,0,0,0.2)] overflow-hidden">
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