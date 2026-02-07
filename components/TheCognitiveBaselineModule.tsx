
/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
*/

import React, { useState } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { 
  ArrowLeft, CheckCircle2, ArrowRight, 
  Lock, Flag, Cpu, Moon, Coffee, Droplet, ListChecks, FlaskConical
} from 'lucide-react';

interface TheCognitiveBaselineModuleProps {
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

const ActivityRing = ({ progress, color = "#475569" }: { progress: number, color?: string }) => {
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
const CognitiveBaselineChecklist = () => {
    const [checks, setChecks] = useState<{ [key: string]: boolean }>({});
    const toggleCheck = (key: string) => setChecks(prev => ({ ...prev, [key]: !prev[key] }));

    const items = [
        { key: 'sleep', label: '9h 15m Time in Bed', details: 'The minimum to get ~8.5h of actual sleep.' },
        { key: 'consistency', label: '<60 min sleep variation', details: 'Avoid "Social Jetlag" between weekdays and weekends.' },
        { key: 'hydration', label: '~8-11 Cups of Water', details: 'Approx. 2-2.5 litres daily. Sip consistently, as thirst is a delayed signal.' },
        { key: 'breakfast', label: 'Low-GI Breakfast', details: 'Avoid sugary cereals/toast. Choose oats, eggs, or protein.' },
        { key: 'detox', label: '1 hour digital detox pre-bed', details: 'Blue light delays sleep and reduces sleep quality.' },
    ];
    
    return(
        <div className="my-10 p-8 md:p-12 bg-white rounded-[3rem] border border-stone-200 shadow-xl">
             <h4 className="font-serif text-2xl font-bold text-stone-800 text-center italic">My Cognitive Baseline Checklist</h4>
             <p className="text-center text-sm text-stone-500 mb-8">This isn't a "nice to have" list. This is the biological minimum for high performance.</p>
             <div className="space-y-4">
                {items.map(item => (
                    <div key={item.key} onClick={() => toggleCheck(item.key)} className={`p-4 rounded-2xl border-2 flex items-center gap-4 cursor-pointer transition-all ${checks[item.key] ? 'bg-emerald-50 border-emerald-300' : 'bg-stone-50 border-stone-200'}`}>
                        <div className={`w-8 h-8 rounded-full flex items-center justify-center text-white ${checks[item.key] ? 'bg-emerald-500' : 'bg-stone-300'}`}>
                            {checks[item.key] && <CheckCircle2 size={16} />}
                        </div>
                        <div>
                            <p className="font-bold">{item.label}</p>
                            <p className="text-xs text-stone-500">{item.details}</p>
                        </div>
                    </div>
                ))}
             </div>
        </div>
    );
};

// --- MODULE COMPONENT ---
export const TheCognitiveBaselineModule: React.FC<{onBack: () => void}> = ({ onBack }) => {
  const [activeSection, setActiveSection] = useState(0);
  const [unlockedSection, setUnlockedSection] = useState(0);
  
  const sections = [
    { id: 'command-centre', title: 'The Command Centre', eyebrow: '01 // The Fragile PFC', icon: Cpu },
    { id: 'sleep-debt-crisis', title: 'The Sleep Debt Crisis', eyebrow: '02 // Intoxication Equivalence', icon: Moon },
    { id: 'sugar-crash', title: 'The Sugar Crash', eyebrow: '03 // Reactive Hypoglycemia', icon: Coffee },
    { id: 'vicious-cycle', title: 'The Vicious Cycle', eyebrow: '04 // Sleep & Sugar', icon: Droplet },
    { id: 'cognitive-baseline', title: 'The Cognitive Baseline', eyebrow: '05 // The Checklist', icon: ListChecks },
    { id: 'self-experiment', title: 'The Self-Experiment', eyebrow: '06 // Feel The Data', icon: FlaskConical },
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
            <p className="text-[9px] font-black text-slate-500 uppercase tracking-[0.4em] mb-0.5 underline">Module 08</p>
            <h1 className="font-serif font-bold text-lg tracking-tight text-stone-900">The Cognitive Baseline</h1>
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
           <ActivityRing progress={progress} color="#475569" /><p className="text-[11px] font-black text-stone-900 uppercase tracking-widest text-center">Progress</p>
        </div>
      </aside>

      <main className="flex-grow flex flex-col items-center py-10 md:py-24 px-6 md:px-16 overflow-y-auto h-screen relative">
        <div className="absolute inset-0 bg-[radial-gradient(#e5e7eb_1px,transparent_1px)] [background-size:32px_32px] opacity-40 pointer-events-none" />
        <div className="w-full max-w-4xl relative z-10">
          <AnimatePresence mode="wait">
            <motion.div key={activeSection} initial={{ opacity: 0, x: 20 }} animate={{ opacity: 1, x: 0 }} exit={{ opacity: 0, x: -20 }} transition={{ duration: 0.6, ease: [0.16, 1, 0.3, 1] }}>
              {activeSection === 0 && (
                <ReadingSection title="The Command Centre." eyebrow="Step 1" icon={Cpu}>
                  <p>Your brain's <Highlight description="The 'CEO' of your brain, located behind your forehead. It's responsible for working memory, inhibitory control, and complex decision-making. It's the last part of the brain to fully mature.">Prefrontal Cortex (PFC)</Highlight> is your academic command centre. It's what allows you to hold a complex Maths problem in your head or structure an English essay. During your teenage years, this area is undergoing a massive renovation, making it incredibly powerful but also uniquely vulnerable.</p>
                  <p>When deprived of sleep or stable energy, your brain doesn't just get 'tired'. It performs a ruthless triage, functionally decoupling your 'rational' PFC from your 'emotional' <Highlight description="The brain's primitive fear and emotion centre. Without the PFC's inhibitory control, the amygdala can become hyperactive, leading to emotional volatility and anxiety.">amygdala</Highlight>. You're not just sleepy; you're neurologically predisposed to anxiety and poor decision-making. Your hardware is compromised.</p>
                </ReadingSection>
              )}
               {activeSection === 1 && (
                <ReadingSection title="The Sleep Debt Crisis." eyebrow="Step 2" icon={Moon}>
                  <p>The biggest myth in student culture is that you can "get used to" less sleep. The data is clear: you can't. While you might stop *feeling* sleepy, your cognitive performance continues to plummet. A landmark study found that after a week of just 5 hours' sleep, students' working memory accuracy dropped by a catastrophic 17%—enough to turn an A into a C.</p>
                  <p>Worse, "weekend catch-up" is a myth. Two nights of recovery sleep are not enough to restore your executive functions. This creates a compounding "sleep debt." The most shocking finding is the <Highlight description="The scientifically established fact that after 17-19 hours of wakefulness, your cognitive impairment is equivalent to having a Blood Alcohol Concentration (BAC) of 0.05%.">Intoxication Equivalence</Highlight>: if you wake up at 6 AM, by 11 PM you are functionally as impaired as someone who is legally drunk.</p>
                </ReadingSection>
              )}
              {activeSection === 2 && (
                <ReadingSection title="The Sugar Crash." eyebrow="Step 3" icon={Coffee}>
                  <p>If sleep is your brain's maintenance crew, glucose is its fuel. Your adolescent brain consumes glucose at a much higher rate than an adult's, making it extremely sensitive to fuel shortages. A high-sugar breakfast (sugary cereal, white toast) causes a rapid spike in blood glucose, followed by an aggressive insulin response that leads to a "crash" 90-120 minutes later.</p>
                  <p>This crash, known as <Highlight description="A state of low blood sugar that occurs after a high-glycemic meal. In adolescents, it coincides with late morning classes and causes significant drops in attention and processing speed.">Reactive Hypoglycemia</Highlight>, is a cognitive disaster. It hits right in the middle of your 3rd or 4th class, resulting in slower processing speeds and higher error rates. You are literally "running on fumes" during critical learning hours.</p>
                </ReadingSection>
              )}
               {activeSection === 3 && (
                <ReadingSection title="The Vicious Cycle." eyebrow="Step 4" icon={Droplet}>
                    <p>Sleep and nutrition are not separate issues. They are locked in a vicious feedback loop. Sleep loss disrupts the hormones that regulate hunger, making you biologically crave high-calorie, high-carbohydrate foods. You wake up tired, so you're primed to choose the sugary cereal over the eggs.</p>
                    <p>That high-sugar food then disrupts your sleep. The blood glucose fluctuations can interfere with Slow Wave Sleep (SWS), the deep sleep stage crucial for memory consolidation. So, poor sleep leads to poor diet, which leads to even poorer sleep. Over a semester, this cycle cumulatively erodes your brain's executive function.</p>
                </ReadingSection>
              )}
              {activeSection === 4 && (
                <ReadingSection title="The Cognitive Baseline." eyebrow="Step 5" icon={ListChecks}>
                    <p>High academic performance is not just about effort; it's about ensuring your biological hardware is running correctly. The "Minimum Effective Doses" for sleep, hydration, and nutrition are not suggestions; they are biological requirements. Below is the evidence-based checklist for your cognitive baseline. Your mission is to treat this not as an ideal, but as the absolute, non-negotiable foundation for your work.</p>
                    <CognitiveBaselineChecklist />
                </ReadingSection>
              )}
              {activeSection === 5 && (
                <ReadingSection title="The Self-Experiment." eyebrow="Step 6" icon={FlaskConical}>
                  <p>To truly understand the impact of nutrition, you need to feel the data yourself. The "Sugar Crash" self-experiment is a simple way to demonstrate the cognitive cost of a high-sugar breakfast compared to a low-sugar, high-protein alternative.</p>
                  <p>The protocol is simple. For two consecutive days, you will eat a different breakfast and record how you feel during your 10:30 AM class. This allows you to experience the reality of reactive hypoglycemia and makes the abstract data of the research tangible. This isn't just an experiment; it's you taking control of your own biology.</p>
                  <MicroCommitment>
                    <p><strong>Day 1:</strong> Eat a high-sugar breakfast (sugary cereal, fruit juice, white toast). At 10:30 AM, rate your energy and focus from 1-10.</p>
                    <p><strong>Day 2:</strong> Eat a low-sugar, high-protein breakfast (eggs, oatmeal, yogurt). At 10:30 AM, rate your energy and focus from 1-10. Compare the results.</p>
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
