
/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
*/

import React, { useState, useEffect } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { 
  ArrowLeft, CheckCircle2, ArrowRight, 
  Lock, Flag, Target, Brain, SlidersHorizontal, Shield, Moon, Utensils, Zap, Wind
} from 'lucide-react';

interface GameDayModuleProps {
  onBack: () => void;
}

const Highlight = ({ children, description, color = "bg-amber-100/40", textColor = "text-amber-900", decorColor = "decoration-amber-400/40", hoverColor="hover:bg-amber-200/60" }: { children?: React.ReactNode, description: string, color?: string, textColor?: string, decorColor?: string, hoverColor?: string }) => {
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
              <p className="font-sans font-bold text-amber-400 mb-2 uppercase tracking-[0.2em] text-[9px]">The Academic Insight</p>
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
        <div className="w-12 h-12 rounded-2xl bg-stone-900 flex items-center justify-center text-amber-400 shadow-xl border border-white/10">
          <Icon size={24} />
        </div>
      </div>
      <span className="inline-flex items-center gap-2 px-3 py-1 bg-amber-50 text-amber-600 text-[10px] font-black tracking-[0.4em] uppercase rounded-full mb-4">
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
  <div className="my-12 p-8 bg-amber-50/50 border-2 border-dashed border-amber-200 rounded-3xl">
    <div className="flex items-start gap-5">
      <div className="w-11 h-11 rounded-xl bg-amber-500 text-white flex items-center justify-center shrink-0 mt-1 shadow-lg shadow-amber-500/20">
        <Flag size={20} />
      </div>
      <div>
        <h4 className="font-bold text-amber-800 text-sm uppercase tracking-widest">Your Mission (Under 5 Mins)</h4>
        <div className="text-stone-600 mt-2 font-medium leading-relaxed">
          {children}
        </div>
      </div>
    </div>
  </div>
);

const ActivityRing = ({ progress, color = "#f59e0b" }: { progress: number, color?: string }) => {
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
const ChallengeThreatSimulator = () => {
    const [resources, setResources] = useState(50);
    const isChallenge = resources >= 50;

    return (
        <div className="my-10 p-8 md:p-12 bg-white rounded-[3rem] border border-stone-200 shadow-xl">
             <h4 className="font-serif text-2xl font-bold text-stone-800 text-center italic">Challenge vs. Threat State</h4>
             <div className="grid grid-cols-2 gap-8 items-center mt-8">
                <div className="text-center">
                    <p className="font-bold text-sm">Demands (The Exam)</p>
                    <div className="h-8 w-full bg-rose-200 rounded-full mt-2 border border-rose-300" />
                </div>
                <div className="text-center">
                    <p className="font-bold text-sm">Your Resources</p>
                    <div className="h-8 w-full bg-stone-100 rounded-full mt-2"><motion.div className="h-full bg-emerald-400 rounded-full" animate={{width: `${resources}%`}} /></div>
                </div>
             </div>
             <div className="flex justify-center gap-2 mt-4"><span className="font-bold">Resource Level:</span><input type="range" value={resources} onChange={e => setResources(parseInt(e.target.value))} /></div>
             <div className={`mt-6 p-4 rounded-xl text-center font-bold text-white ${isChallenge ? 'bg-emerald-500' : 'bg-rose-500'}`}>
                {isChallenge ? "CHALLENGE STATE: You feel 'pumped'. Blood vessels dilate, oxygen floods the brain. Go time." : "THREAT STATE: You feel 'scared'. Blood vessels constrict, PFC is impaired. 'Mind blanking' is likely."}
             </div>
        </div>
    );
};

const CircadianShifter = () => {
    const [wakeTime, setWakeTime] = useState(9);
    const shifts = Math.ceil(((wakeTime - 7) * 60) / 15);

    return(
        <div className="my-10 p-8 md:p-12 bg-white rounded-[3rem] border border-stone-200 shadow-xl">
             <h4 className="font-serif text-2xl font-bold text-stone-800 text-center italic">Circadian Rhythm Shifter</h4>
             <p className="text-center text-sm text-stone-500 mb-6">Input your current weekend wake-up time to get your 4-week 'Phase Advance' plan.</p>
             <div className="flex items-center justify-center gap-4">
                <label className="font-bold">Current Wake-up:</label>
                <input type="time" value={`${String(Math.floor(wakeTime)).padStart(2,'0')}:${String((wakeTime % 1)*60).padStart(2,'0')}`} onChange={e => setWakeTime(parseInt(e.target.value.split(':')[0]) + parseInt(e.target.value.split(':')[1])/60)} className="p-2 bg-stone-100 rounded-lg"/>
             </div>
             {wakeTime > 7 && <div className="mt-6 p-4 bg-amber-50 border border-amber-200 rounded-xl text-center">
                <p className="font-bold text-amber-800">Your Protocol:</p>
                <p className="text-sm">Shift your alarm back by 15 mins every <span className="font-bold">3-4 days</span> for the next <span className="font-bold">{shifts}</span> shifts to reach your 7:00 AM target.</p>
             </div>}
        </div>
    );
}

const TaperPlanner = () => {
    const [day, setDay] = useState(7);
    const taperData = {
        7: { volume: 80, intensity: 90, activity: 'Past Papers' },
        5: { volume: 60, intensity: 90, activity: 'Active Recall' },
        3: { volume: 40, intensity: 50, activity: 'Flashcards' },
        1: { volume: 10, intensity: 20, activity: 'Strategy Review' },
    };
    const currentData = taperData[day as keyof typeof taperData] || taperData[Object.keys(taperData).reverse().find(d => parseInt(d) >= day) as any];

    return (
        <div className="my-10 p-8 md:p-12 bg-white rounded-[3rem] border border-stone-200 shadow-xl">
             <h4 className="font-serif text-2xl font-bold text-stone-800 text-center italic">Academic Taper Planner</h4>
             <p className="text-center text-sm text-stone-500 mb-6">Move the slider to see how your training changes in the final week.</p>
             <label className="font-bold">Days Before Exam: {day}</label>
             <input type="range" min="1" max="7" value={day} onChange={e => setDay(parseInt(e.target.value))} className="w-full" />
             <div className="grid grid-cols-3 gap-4 mt-4 text-center">
                <div><p className="font-bold text-sm">Study Volume</p><div className="h-24 bg-stone-100 rounded-lg flex items-end mt-2"><motion.div className="w-full bg-blue-400 rounded-t-lg" animate={{height: `${currentData.volume}%`}} /></div></div>
                <div><p className="font-bold text-sm">Intensity</p><div className="h-24 bg-stone-100 rounded-lg flex items-end mt-2"><motion.div className="w-full bg-rose-400 rounded-t-lg" animate={{height: `${currentData.intensity}%`}} /></div></div>
                <div><p className="font-bold text-sm">Activity</p><div className="h-24 flex items-center justify-center mt-2 font-bold">{currentData.activity}</div></div>
             </div>
        </div>
    )
}

const CognitiveWarmup = () => {
    const [drill, setDrill] = useState<'none'|'verbal'|'math'>('none');
    const [time, setTime] = useState(60);
    const [words, setWords] = useState('');

    useEffect(() => {
        let timer: any;
        if(drill === 'verbal' && time > 0) {
            timer = setTimeout(() => setTime(t => t - 1), 1000);
        }
        return () => clearTimeout(timer);
    }, [drill, time]);
    
    const resetVerbal = () => {
        setDrill('verbal');
        setTime(60);
        setWords('');
    }

    if(drill === 'math') {
        return (
             <div className="my-10 p-8 md:p-12 bg-white rounded-[3rem] border border-stone-200 shadow-xl text-center">
                <h4 className="font-serif text-2xl font-bold text-stone-800 text-center italic">Calculation Sprint</h4>
                <p>1. 15 x 12 = ?</p>
                <p>2. What is 25% of 180?</p>
                <button onClick={() => setDrill('none')} className="text-xs mt-4">Back</button>
             </div>
        );
    }
    
    if(drill === 'verbal') {
        return (
            <div className="my-10 p-8 md:p-12 bg-white rounded-[3rem] border border-stone-200 shadow-xl text-center">
                <h4 className="font-serif text-2xl font-bold text-stone-800 text-center italic">Verbal Fluency Drill</h4>
                <p>For 60 seconds, list as many words as you can that start with the letter 'P'.</p>
                <p className="text-4xl font-bold my-4">{time}</p>
                <textarea value={words} onChange={e => setWords(e.target.value)} className="w-full h-24 bg-stone-100 rounded-lg p-2" disabled={time === 0} />
                <button onClick={resetVerbal} className="text-xs mt-4">Reset</button>
            </div>
        );
    }

    return (
        <div className="my-10 p-8 md:p-12 bg-white rounded-[3rem] border border-stone-200 shadow-xl text-center">
             <h4 className="font-serif text-2xl font-bold text-stone-800 text-center italic">Cognitive Warm-Up</h4>
             <p className="text-sm text-stone-500 mb-6">Choose your drill to prime your brain for action.</p>
             <div className="flex justify-center gap-4">
                <button onClick={() => resetVerbal()} className="p-4 bg-stone-100 rounded-lg">Verbal Fluency</button>
                <button onClick={() => setDrill('math')} className="p-4 bg-stone-100 rounded-lg">Math Sprint</button>
             </div>
        </div>
    );
};


// --- MODULE COMPONENT ---
export const GameDayModule: React.FC<GameDayModuleProps> = ({ onBack }) => {
  const [activeSection, setActiveSection] = useState(0);
  const [unlockedSection, setUnlockedSection] = useState(0);
  
  const sections = [
    { id: 'athlete-mindset', title: 'The Athlete Mindset', eyebrow: '01 // The Paradigm', icon: Target },
    { id: 'macrocycle', title: 'The Macrocycle', eyebrow: '02 // 1 Month Out', icon: SlidersHorizontal },
    { id: 'mesocycle', title: 'The Mesocycle', eyebrow: '03 // The Taper', icon: Brain },
    { id: 'mental-rehearsal', title: 'Mental Rehearsal', eyebrow: '04 // Visualization', icon: Shield },
    { id: 'microcycle', title: 'The Microcycle', eyebrow: '05 // The Day Before', icon: Moon },
    { id: 'game-day-morning', title: 'Game Day Morning', eyebrow: '06 // The Warm-Up', icon: Utensils },
    { id: 'in-the-arena', title: 'In The Arena', eyebrow: '07 // Execution', icon: Zap },
    { id: 'recovery', title: 'Halftime & Post-Game', eyebrow: '08 // Recovery', icon: Wind },
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
            <p className="text-[9px] font-black text-amber-500 uppercase tracking-[0.4em] mb-0.5 underline">Module 08</p>
            <h1 className="font-serif font-bold text-lg tracking-tight text-stone-900">Game Day Protocol</h1>
          </div>
        </div>

        <div className="flex-grow space-y-4 overflow-y-auto no-scrollbar pr-2 relative">
          <div className="absolute left-[21px] top-6 bottom-6 w-0.5 bg-stone-100 -z-0" />
          <div className="absolute left-[21px] top-6 bottom-6 w-0.5">
              <motion.div
                  className="w-full bg-amber-500 shadow-[0_0_10px_rgba(245,158,11,0.5)]"
                  initial={{ height: 0 }}
                  animate={{ height: sections.length > 1 ? `${(unlockedSection / (sections.length - 1)) * 100}%` : '0%' }}
              />
          </div>
          {sections.map((section, idx) => {
            const isUnlocked = idx <= unlockedSection;
            const isActive = idx === activeSection;
            const isCompleted = idx < unlockedSection;
            return (
              <button key={section.id} disabled={!isUnlocked} onClick={() => handleJumpToSection(idx)} className={`relative z-10 w-full flex items-center gap-4 p-3 rounded-xl transition-all duration-500 text-left group ${isActive ? 'bg-amber-50 shadow-sm translate-x-2' : ''} ${!isUnlocked ? 'opacity-40 grayscale cursor-not-allowed' : 'hover:bg-stone-50'}`}>
                <div className={`w-11 h-11 rounded-xl flex items-center justify-center shrink-0 border-2 transition-all duration-500 ${isCompleted ? 'bg-amber-600 border-amber-600 text-white shadow-lg' : isActive ? 'bg-white border-amber-500 text-amber-600 shadow-xl rotate-12' : 'bg-white border-stone-200 text-stone-300'}`}>
                   {isCompleted ? <CheckCircle2 size={18} /> : isActive ? <section.icon size={18} /> : <Lock size={16} />}
                </div>
                <div className="flex-grow"><p className={`text-[8px] font-black uppercase tracking-widest ${isActive ? 'text-amber-500' : 'text-stone-400'}`}>{section.eyebrow.split('// ')[1]}</p><h4 className={`text-xs font-bold leading-tight ${isActive ? 'text-stone-900' : 'text-stone-500'}`}>{section.title}</h4></div>
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
                <ReadingSection title="The Athlete Mindset." eyebrow="Step 1" icon={Target}>
                  <p>The Leaving Cert is not an academic test; it's an endurance event. Your brain consumes 20% of your body's oxygen and glucose. A 3-hour exam is a metabolic marathon. This module reframes you from a 'student' to an <Highlight description="A paradigm that treats academic performance as a physical discipline, prioritizing physiological optimization (sleep, nutrition, stress management) to maximize cognitive output.">Occupational Athlete</Highlight>. Your success is not just determined by what you know, but by the physiological state of the brain that's trying to access it.</p>
                  <p>The key to performance is engineering a <Highlight description="A physiological state where your brain perceives your resources (energy, preparation) as meeting or exceeding the demands of a task. It's characterized by adrenaline (for focus) and vasodilation (increased blood flow to the brain).">Challenge State</Highlight> ("pumped") and avoiding a <Highlight description="A physiological state where demands are perceived to exceed resources. It's characterized by cortisol (stress hormone) and vasoconstriction, which impairs function of the Prefrontal Cortex, leading to 'mind blanking'.">Threat State</Highlight> ("scared"). This isn't about positive thinking; it's about tangible physiological interventions.</p>
                  <ChallengeThreatSimulator />
                </ReadingSection>
              )}
               {activeSection === 1 && (
                <ReadingSection title="The Macrocycle: 1 Month Out." eyebrow="Step 2" icon={SlidersHorizontal}>
                  <p>In the final month, the focus shifts from accumulating new knowledge to consolidating what you have and standardizing your biology. This is the "Pre-Competition Phase." Your goal is to align your internal body clock with the external exam schedule through <Highlight description="The process of synchronizing your internal biological clock (circadian rhythm) to external cues, primarily the light-dark cycle.">Circadian Entrainment</Highlight>.</p>
                  <p>The average teenager is a "night owl," but exams start at 9:30 AM. You must systematically shift your sleep schedule. This is a gradual process. You also need to switch to a <Highlight description="A diet focused on foods that provide a slow, steady release of glucose (e.g., oats, whole grains) to avoid the 'spike and crash' cycle that impairs cognitive function.">Low-Glycemic Diet</Highlight> to ensure stable fuel for your brain.</p>
                  <CircadianShifter />
                </ReadingSection>
              )}
               {activeSection === 2 && (
                <ReadingSection title="The Mesocycle: The Taper." eyebrow="Step 3" icon={Brain}>
                  <p>The final week is the most mismanaged period of study. The instinct is to cram, but the athletic model dictates the opposite: <Highlight description="The systematic reduction of training volume in the days before a competition. A 40-60% reduction can lead to a ~3% performance improvement.">Tapering</Highlight>. Performance = Fitness - Fatigue. Cramming maximizes fatigue, leading to a suboptimal performance even if your "fitness" (knowledge) is high.</p>
                  <p>The academic taper involves systematically reducing study *volume* while maintaining *intensity*. You do fewer hours, but those hours are high-quality active recall. Crucially, you must stop learning new material 3 days out to avoid <Highlight description="When new information interferes with the recall of older information. This is why last-minute cramming can make you forget things you knew perfectly.">retroactive interference</Highlight>.</p>
                  <TaperPlanner />
                </ReadingSection>
              )}
              {activeSection === 3 && (
                <ReadingSection title="Mental Rehearsal." eyebrow="Step 4" icon={Shield}>
                  <p>Top athletes don't just train their bodies; they train their minds through visualization. But there's a trap. <Highlight description="Visualizing the final result (e.g., getting 625 points). Research shows this can deplete energy and increase anxiety.">Outcome Visualization</Highlight> can be counterproductive.</p>
                  <p>The key is <Highlight description="Visualizing the specific steps of the process (e.g., waking up calm, reading the question, taking a breath). This 'mental rehearsal' prepares the brain for the specific stressors it will face, creating a pre-rehearsed coping mechanism.">Process Visualization</Highlight>. By repeatedly running a "mental movie" of exam day, you prepare your brain for what's coming. When you face a difficult question, your brain recognizes the scenario ("I've been here before") and triggers your rehearsed coping strategy instead of a panic response.</p>
                </ReadingSection>
              )}
              {activeSection === 4 && (
                <ReadingSection title="The Microcycle: Day Before." eyebrow="Step 5" icon={Moon}>
                  <p>The 24 hours before your first exam are about stability and anxiety mitigation. All heavy cognitive lifting must cease by 6:00 PM. The evening is for shifting into a "rest and digest" state. Complete the <Highlight description="A control ritual where you pack your clear pencil case, calculator, ID, and water bottle the night before to reduce 'cognitive load' on the morning of the exam.">"Packing" Ritual</Highlight> early.</p>
                  <p>Your dinner should be a "Cognitive Carb-Load"—a balanced meal of complex carbs and lean protein (e.g., chicken and sweet potato) to ensure your brain's glycogen stores are full. Finally, perform a <Highlight description="Writing down any lingering facts or worries before sleep to 'offload' them from your working memory, allowing your brain to switch off.">"Brain Dump"</Highlight> to clear your mind.</p>
                </ReadingSection>
              )}
               {activeSection === 5 && (
                <ReadingSection title="Game Day: The Warm-Up." eyebrow="Step 6" icon={Utensils}>
                  <p>The morning of the exam is about managing the natural spike in cortisol and adrenaline and channeling it into focus. Do not hit snooze. Immediately hydrate with 500ml of water. Get 10 minutes of morning sunlight to anchor your circadian rhythm. Your breakfast must be Low-GI.</p>
                  <p>Just as an athlete warms up their muscles, you must warm up your brain. Passively reading notes is useless. You need a <Highlight description="Active priming exercises (e.g., verbal fluency drills, simple calculations) performed 20-30 minutes before an exam to lower the 'activation threshold' of the relevant neural circuits.">Cognitive Warm-Up</Highlight>. This gets the relevant brain areas perfused with blood and "online" before you open the paper.</p>
                  <CognitiveWarmup />
                </ReadingSection>
              )}
               {activeSection === 6 && (
                <ReadingSection title="In The Arena: Execution." eyebrow="Step 7" icon={Zap}>
                  <p>Create a psychological "bubble" on arrival. Headphones on, no panicked conversations. Upon entering the hall, perform the <Highlight description="Two sharp inhales through the nose, one long exhale through the mouth. The fastest tool to reduce autonomic arousal in real-time.">Physiological Sigh</Highlight> to calm your nervous system. For the first 5 minutes, do not write. Just read and breathe. This prevents the "panic misread."</p>
                </ReadingSection>
              )}
               {activeSection === 7 && (
                <ReadingSection title="Halftime & Post-Game." eyebrow="Step 8" icon={Wind}>
                  <p>On days with two exams, the "halftime" break is critical. Eat a light lunch of protein and complex carbs to avoid a "food coma." A 10-20 minute "Power Nap" or a guided <Highlight description="Non-Sleep Deep Rest. A guided meditation that can restore dopamine levels and reduce cortisol more effectively than a nap for some people.">NSDR</Highlight> script is the most effective way to reset.</p>
                  <p>After each exam, the rule is absolute: a strict <Highlight description="The rule to avoid all discussion of an exam after it is finished. This prevents 'anxiety contagion' and keeps your brain out of a 'Threat State' for the next paper.">"Post-Mortem" Ban</Highlight>. The paper is done. Bin the mental file. Focus on the next game.</p>
                  <MicroCommitment>
                    <p>Go to your calendar. Find the date one month before your first exam. Create an event: "Begin Macrocycle." You are no longer just a student. You are an athlete.</p>
                  </MicroCommitment>
                </ReadingSection>
              )}
              <footer className="mt-24 flex items-center justify-between pt-12 border-t border-stone-200/60 px-4">
                <motion.button whileHover={{ scale: 1.05 }} whileTap={{ scale: 0.95 }} onClick={handlePrev} disabled={activeSection === 0} className={`flex items-center gap-4 bg-stone-100 text-stone-800 px-8 py-4 rounded-xl font-black text-[10px] uppercase tracking-widest transition-all shadow-sm ${activeSection === 0 ? 'opacity-0 pointer-events-none' : ''}`}>
                  <ArrowLeft size={16} /> Prev
                </motion.button>
                <motion.button whileHover={{ scale: 1.05 }} whileTap={{ scale: 0.95 }} onClick={handleCompleteSection} className="group relative flex items-center gap-4 bg-stone-900 text-white px-12 py-6 rounded-2xl font-black text-[12px] uppercase tracking-widest hover:bg-amber-600 transition-all shadow-[0_20px_50px_rgba(0,0,0,0.2)] overflow-hidden">
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
