/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
*/

import React, { useState } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { 
  ArrowLeft, CheckCircle2, ArrowRight, 
  Lock, Flag, Cpu, Brain, Heart, Zap, Shield, Moon, Utensils, ClipboardCheck
} from 'lucide-react';

interface EmotionalIntelligenceModuleProps {
  onBack: () => void;
}

const Highlight = ({ children, description, color = "bg-cyan-100/40", textColor = "text-cyan-900", decorColor = "decoration-cyan-400/40", hoverColor="hover:bg-cyan-200/60" }: { children?: React.ReactNode, description: string, color?: string, textColor?: string, decorColor?: string, hoverColor?: string }) => {
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
              <p className="font-sans font-bold text-cyan-400 mb-2 uppercase tracking-[0.2em] text-[9px]">The Academic Insight</p>
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
        <div className="w-12 h-12 rounded-2xl bg-stone-900 flex items-center justify-center text-cyan-400 shadow-xl border border-white/10">
          <Icon size={24} />
        </div>
      </div>
      <span className="inline-flex items-center gap-2 px-3 py-1 bg-cyan-50 text-cyan-600 text-[10px] font-black tracking-[0.4em] uppercase rounded-full mb-4">
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
  <div className="my-12 p-8 bg-cyan-50/50 border-2 border-dashed border-cyan-200 rounded-3xl">
    <div className="flex items-start gap-5">
      <div className="w-11 h-11 rounded-xl bg-cyan-500 text-white flex items-center justify-center shrink-0 mt-1 shadow-lg shadow-cyan-500/20">
        <Flag size={20} />
      </div>
      <div>
        <h4 className="font-bold text-cyan-800 text-sm uppercase tracking-widest">Your Mission (Under 5 Mins)</h4>
        <div className="text-stone-600 mt-2 font-medium leading-relaxed">
          {children}
        </div>
      </div>
    </div>
  </div>
);

const ActivityRing = ({ progress, color = "#06b6d4" }: { progress: number, color?: string }) => {
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
const PFCShutdownSimulator = () => {
    const [stress, setStress] = useState(false);
    return (
        <div className="my-10 p-8 md:p-12 bg-white rounded-[3rem] border border-stone-200 shadow-xl text-center">
             <h4 className="font-serif text-2xl font-bold text-stone-800 text-center italic">PFC Shutdown Simulator</h4>
             <p className="text-sm text-stone-500 mb-6">Click to see what happens when your Amygdala hijacks your brain.</p>
             <div className="flex justify-center items-center gap-4">
                <motion.div animate={{opacity: stress ? 1: 0.3}} className="text-center"><Zap size={48} className="text-rose-500 mx-auto"/><p className="font-bold">Amygdala</p></motion.div>
                <motion.div className="w-24 h-1 bg-stone-300" animate={{backgroundColor: stress ? '#ef4444' : '#3b82f6'}} />
                <motion.div animate={{opacity: stress ? 0.3: 1}} className="text-center"><Brain size={48} className="text-blue-500 mx-auto"/><p className="font-bold">PFC</p></motion.div>
             </div>
             <button onClick={() => setStress(!stress)} className="mt-6 px-4 py-2 bg-rose-500 text-white font-bold text-sm rounded-lg">{stress ? 'De-escalate' : 'Trigger Stress'}</button>
        </div>
    );
}

const ArousalReappraisal = () => {
    return (
        <div className="my-10 p-8 md:p-12 bg-white rounded-[3rem] border border-stone-200 shadow-xl">
             <h4 className="font-serif text-2xl font-bold text-stone-800 text-center italic">Arousal Reappraisal</h4>
             <div className="relative h-48 w-full">
                <div className="absolute top-4 left-4 p-3 bg-rose-100 text-rose-800 rounded-lg font-bold">Anxiety</div>
                <div className="absolute top-4 right-4 p-3 bg-emerald-100 text-emerald-800 rounded-lg font-bold">Excitement</div>
                <div className="absolute bottom-4 left-1/2 -translate-x-1/2 p-3 bg-blue-100 text-blue-800 rounded-lg font-bold">Calm</div>
                <svg className="w-full h-full" viewBox="0 0 200 100">
                    <path d="M 20 10 H 180" stroke="#f59e0b" strokeWidth="2"/>
                    <path d="M 20 10 Q 100 120 180 10" stroke="#ef4444" strokeWidth="2" strokeDasharray="4"/>
                </svg>
             </div>
             <p className="text-center text-sm text-stone-500">It's easier to shift valence (Anxiety &#8594; Excitement) than to change arousal state (Anxiety &#8594; Calm).</p>
        </div>
    );
};

const BoxBreathing = () => (
     <div className="my-10 p-8 md:p-12 bg-white rounded-[3rem] border border-stone-200 shadow-xl text-center">
         <h4 className="font-serif text-2xl font-bold text-stone-800 text-center italic">Box Breathing</h4>
         <div className="w-24 h-24 mx-auto my-6 relative">
             <motion.div className="w-full h-full border-4 border-cyan-300 rounded-lg" animate={{rotate: 360}} transition={{duration: 16, repeat: Infinity, ease: 'linear'}}/>
             <motion.div className="absolute w-4 h-4 bg-cyan-500 rounded-full" style={{top: -8, left:'50%', x:'-50%'}} animate={{offsetDistance: "100%"}} transition={{duration: 16, repeat: Infinity, ease: 'linear'}}/>
         </div>
         <p className="text-sm font-bold">Inhale (4s) - Hold (4s) - Exhale (4s) - Hold (4s)</p>
    </div>
);


// --- MODULE COMPONENT ---
export const EmotionalIntelligenceModule: React.FC<EmotionalIntelligenceModuleProps> = ({ onBack }) => {
  const [activeSection, setActiveSection] = useState(0);
  const [unlockedSection, setUnlockedSection] = useState(0);
  
  const sections = [
    { id: 'neurobiology-stress', title: 'The Neurobiology of Stress', eyebrow: '01 // The Hardware', icon: Cpu },
    { id: 'emotional-intelligence', title: 'What is Emotional Intelligence?', eyebrow: '02 // The Software', icon: Brain },
    { id: 'self-awareness', title: 'Building Self-Awareness', eyebrow: '03 // Somatic Literacy', icon: Heart },
    { id: 'cognitive-regulation', title: 'Cognitive Regulation (Top-Down)', eyebrow: '04 // The Mind', icon: Zap },
    { id: 'physiological-regulation', title: 'Physiological Regulation (Bottom-Up)', eyebrow: '05 // The Body', icon: Shield },
    { id: 'bio-support', title: 'The Bio-Support System', eyebrow: '06 // Fuel & Maintenance', icon: Utensils },
    { id: 'integrated-timeline', title: 'The Integrated Timeline', eyebrow: '07 // The Plan', icon: ClipboardCheck },
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
            <p className="text-[9px] font-black text-cyan-500 uppercase tracking-[0.4em] mb-0.5 underline">Module 13</p>
            <h1 className="font-serif font-bold text-lg tracking-tight text-stone-900">Emotional Intelligence</h1>
          </div>
        </div>

        <div className="flex-grow space-y-4 overflow-y-auto no-scrollbar pr-2 relative">
          <div className="absolute left-[21px] top-6 bottom-6 w-0.5 bg-stone-100 -z-0" />
          <div className="absolute left-[21px] top-6 bottom-6 w-0.5">
              <motion.div
                  className="w-full bg-cyan-500 shadow-[0_0_10px_rgba(6,182,212,0.5)]"
                  initial={{ height: 0 }}
                  animate={{ height: sections.length > 1 ? `${(unlockedSection / (sections.length - 1)) * 100}%` : '0%' }}
              />
          </div>
          {sections.map((section, idx) => {
            const isUnlocked = idx <= unlockedSection;
            const isActive = idx === activeSection;
            const isCompleted = idx < unlockedSection;
            return (
              <button key={section.id} disabled={!isUnlocked} onClick={() => handleJumpToSection(idx)} className={`relative z-10 w-full flex items-center gap-4 p-3 rounded-xl transition-all duration-500 text-left group ${isActive ? 'bg-cyan-50 shadow-sm translate-x-2' : ''} ${!isUnlocked ? 'opacity-40 grayscale cursor-not-allowed' : 'hover:bg-stone-50'}`}>
                <div className={`w-11 h-11 rounded-xl flex items-center justify-center shrink-0 border-2 transition-all duration-500 ${isCompleted ? 'bg-cyan-600 border-cyan-600 text-white shadow-lg' : isActive ? 'bg-white border-cyan-500 text-cyan-600 shadow-xl rotate-12' : 'bg-white border-stone-200 text-stone-300'}`}>
                   {isCompleted ? <CheckCircle2 size={18} /> : isActive ? <section.icon size={18} /> : <Lock size={16} />}
                </div>
                <div className="flex-grow"><p className={`text-[8px] font-black uppercase tracking-widest ${isActive ? 'text-cyan-500' : 'text-stone-400'}`}>{section.eyebrow.split('// ')[1]}</p><h4 className={`text-xs font-bold leading-tight ${isActive ? 'text-stone-900' : 'text-stone-500'}`}>{section.title}</h4></div>
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
                <ReadingSection title="The Neurobiology of Stress." eyebrow="Step 1" icon={Cpu}>
                  <p>Exam stress isn't a character flaw; it's a predictable neuroendocrine response. Your brain's alarm system, the <Highlight description="The Hypothalamic-Pituitary-Adrenal axis is the body's central stress response system. When a threat is perceived, it releases a cascade of hormones, culminating in cortisol.">HPA Axis</Highlight>, floods your system with cortisol. In the short term, this is good—it sharpens focus. But the Leaving Cert is a chronic stressor.</p>
                  <p>Under chronic stress, high levels of cortisol effectively take your <Highlight description="The 'CEO' of your brain, responsible for planning, logic, and working memory. It is the last part of the brain to fully mature, making it vulnerable during adolescence.">Prefrontal Cortex (PFC)</Highlight> "offline." This is the biological reason for "going blank." Your brain has prioritized survival over cognition. Understanding this isn't an excuse; it's the first step to taking back control.</p>
                  <PFCShutdownSimulator />
                </ReadingSection>
              )}
              {activeSection === 1 && (
                <ReadingSection title="What is Emotional Intelligence?" eyebrow="Step 2" icon={Brain}>
                  <p><Highlight description="The capacity to be aware of, control, and express one's emotions, and to handle interpersonal relationships judiciously and empathetically.">Emotional Intelligence (EI)</Highlight> isn't about being "nice." In an academic context, it's a set of high-level cognitive skills for monitoring and regulating your internal state. High EI doesn't mean you don't feel stress; it means you can use that stress as fuel (<Highlight description="A positive, motivating form of stress that can improve performance.">eustress</Highlight>) instead of letting it become a debilitating force.</p>
                  <p>For the Leaving Cert, we can break EI into three trainable skills: 1) **Emotional Awareness:** Noticing the physical signals of stress early. 2) **Emotional Understanding:** Correctly labeling the emotion. 3) **Emotional Regulation:** Using specific strategies to manage it.</p>
                </ReadingSection>
              )}
              {activeSection === 2 && (
                <ReadingSection title="Building Self-Awareness." eyebrow="Step 3" icon={Heart}>
                  <p>You can't manage what you don't measure. The first step is to develop <Highlight description="The ability to read your body's internal physical signals, such as heart rate, breathing, and muscle tension.">Somatic Literacy</Highlight>. Your body often registers stress before your conscious mind does. These physical signals are called <Highlight description="Physical sensations (e.g., racing heart, tight stomach) that act as early warning signs for an emotional response.">Somatic Markers</Highlight>.</p>
                  <p>A simple daily "Body Scan" can train your ability to notice these markers. By checking in with your body, you can catch the stress response early, before it cascades into a full-blown panic attack. It's about moving from "I'm freaking out" to "I am noticing the sensation of a rapid heartbeat."</p>
                </ReadingSection>
              )}
              {activeSection === 3 && (
                <ReadingSection title="Cognitive Regulation (Top-Down)." eyebrow="Step 4" icon={Zap}>
                    <p>Once you've noticed the feeling, you need to manage it with your mind. This is <Highlight description="Using your thoughts and beliefs (cognition) to influence your emotional state.">Top-Down Regulation</Highlight>. A counter-intuitive but powerful strategy is <Highlight description="The act of reinterpreting the meaning of a high-arousal state. Physiologically, anxiety and excitement are almost identical; the only difference is the cognitive label you apply.">Arousal Reappraisal</Highlight>. It's neurologically easier to shift from "anxious" to "excited" than it is to "calm down."</p>
                    <p>The second tool is <Highlight description="A core CBT technique where you challenge the validity of your negative automatic thoughts by examining the evidence for and against them.">Cognitive Restructuring</Highlight>. You treat your catastrophic thought ("I'm going to fail everything") like a prosecutor's claim in a courtroom and you become the defence lawyer, looking for counter-evidence.</p>
                    <ArousalReappraisal/>
                </ReadingSection>
              )}
               {activeSection === 4 && (
                <ReadingSection title="Physiological Regulation (Bottom-Up)." eyebrow="Step 5" icon={Shield}>
                  <p>Sometimes, your mind is too flooded to think straight. In these moments, you need to use your body to calm your mind. This is <Highlight description="Using physiological interventions (like breathing) to change your emotional state.">Bottom-Up Regulation</Highlight>. The fastest tool is breathing.</p>
                  <p><Highlight description="A simple 4-4-4-4 breathing pattern that stimulates the Vagus nerve, a key part of your parasympathetic ('rest and digest') nervous system, acting as a physiological brake on the stress response.">Box Breathing</Highlight> is your emergency protocol for the exam hall. It's invisible and takes less than a minute to interrupt the panic loop and restore blood flow to your PFC.</p>
                  <BoxBreathing />
                </ReadingSection>
              )}
              {activeSection === 5 && (
                <ReadingSection title="The Bio-Support System." eyebrow="Step 6" icon={Utensils}>
                  <p>Emotional regulation is biologically expensive. A tired, dehydrated, or malnourished brain cannot regulate itself effectively, no matter how good your psychological tools are. Your baseline biology is non-negotiable.</p>
                  <p>The "Anti-Cortisol" diet focuses on slow-release carbs (oats) and omega-3s (fish, walnuts) to stabilize your energy. Even mild dehydration (1-2%) significantly impairs concentration. And most importantly, sleep is when your brain consolidates learning and flushes out the metabolic waste that causes "brain fog." Strategic breaks, especially using <Highlight description="Non-Sleep Deep Rest: A guided meditation protocol that rapidly reduces cortisol and replenishes dopamine, making it an ideal 'reset button' during the study day.">NSDR</Highlight>, are also critical for recovery.</p>
                </ReadingSection>
              )}
              {activeSection === 6 && (
                <ReadingSection title="The Integrated Timeline." eyebrow="Step 7" icon={ClipboardCheck}>
                    <p>You now have a complete toolkit of top-down and bottom-up strategies. The final step is to integrate them into a clear timeline.</p>
                    <p><strong>Months Before:</strong> Build resilience. Practice daily Body Scans and learn Box Breathing when stress is low. **Morning Of:** Arousal regulation is key. Eat the "Exam Breakfast," stay away from panicked friends, and use the "Get Excited" reframe. **In The Hall:** If panic hits, use the "Paper Panic" drill: Stop, Breathe (3 cycles of Box Breathing), Micro-PMR (clench toes), and Re-engage with the easiest question. **Post-Exam:** A strict Post-Mortem Ban is essential to contain anxiety for the next paper.</p>
                    <MicroCommitment><p>Choose one protocol from this module. Commit to practicing it for 5 minutes every day for one week. You are not just studying; you are training your nervous system.</p></MicroCommitment>
                </ReadingSection>
              )}
              <footer className="mt-24 flex items-center justify-between pt-12 border-t border-stone-200/60 px-4">
                <motion.button whileHover={{ scale: 1.05 }} whileTap={{ scale: 0.95 }} onClick={handlePrev} disabled={activeSection === 0} className={`flex items-center gap-4 bg-stone-100 text-stone-800 px-8 py-4 rounded-xl font-black text-[10px] uppercase tracking-widest transition-all shadow-sm ${activeSection === 0 ? 'opacity-0 pointer-events-none' : ''}`}>
                  <ArrowLeft size={16} /> Prev
                </motion.button>
                <motion.button whileHover={{ scale: 1.05 }} whileTap={{ scale: 0.95 }} onClick={handleCompleteSection} className="group relative flex items-center gap-4 bg-stone-900 text-white px-12 py-6 rounded-2xl font-black text-[12px] uppercase tracking-widest hover:bg-cyan-600 transition-all shadow-[0_20px_50px_rgba(0,0,0,0.2)] overflow-hidden">
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
