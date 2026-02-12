/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
*/

import React, { useState, useEffect } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { Target, Brain, SlidersHorizontal, Shield, Moon, Utensils, Zap, Wind } from 'lucide-react';
import { ModuleProgress } from '../types';
import { amberTheme } from '../moduleThemes';
import { Highlight, ReadingSection, MicroCommitment } from './ModuleShared';
import { ModuleLayout } from './ModuleLayout';

const theme = amberTheme;

// --- INTERACTIVE COMPONENTS ---
const ChallengeThreatSimulator = () => {
    const [resources, setResources] = useState(50);
    const isChallenge = resources >= 50;

    return (
        <div className="my-10 p-8 md:p-12 bg-white dark:bg-zinc-800 rounded-xl border border-zinc-200 dark:border-zinc-700">
             <h4 className="font-serif text-2xl font-semibold text-zinc-800 dark:text-white text-center">Challenge vs. Threat State</h4>
             <div className="grid grid-cols-2 gap-8 items-center mt-8">
                <div className="text-center">
                    <p className="font-bold text-sm">Demands (The Exam)</p>
                    <div className="h-8 w-full bg-rose-200 rounded-full mt-2 border border-rose-300" />
                </div>
                <div className="text-center">
                    <p className="font-bold text-sm">Your Resources</p>
                    <div className="h-8 w-full bg-zinc-100 dark:bg-zinc-800 rounded-full mt-2"><motion.div className="h-full bg-emerald-400 rounded-full" animate={{width: `${resources}%`}} /></div>
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
        <div className="my-10 p-8 md:p-12 bg-white dark:bg-zinc-800 rounded-xl border border-zinc-200 dark:border-zinc-700">
             <h4 className="font-serif text-2xl font-semibold text-zinc-800 dark:text-white text-center">Circadian Rhythm Shifter</h4>
             <p className="text-center text-sm text-zinc-500 dark:text-zinc-400 mb-6">Input your current weekend wake-up time to get your 4-week 'Phase Advance' plan.</p>
             <div className="flex items-center justify-center gap-4">
                <label className="font-bold">Current Wake-up:</label>
                <input type="time" value={`${String(Math.floor(wakeTime)).padStart(2,'0')}:${String((wakeTime % 1)*60).padStart(2,'0')}`} onChange={e => setWakeTime(parseInt(e.target.value.split(':')[0]) + parseInt(e.target.value.split(':')[1])/60)} className="p-2 bg-zinc-100 dark:bg-zinc-800 rounded-lg"/>
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
        <div className="my-10 p-8 md:p-12 bg-white dark:bg-zinc-800 rounded-xl border border-zinc-200 dark:border-zinc-700">
             <h4 className="font-serif text-2xl font-semibold text-zinc-800 dark:text-white text-center">Academic Taper Planner</h4>
             <p className="text-center text-sm text-zinc-500 dark:text-zinc-400 mb-6">Move the slider to see how your training changes in the final week.</p>
             <label className="font-bold">Days Before Exam: {day}</label>
             <input type="range" min="1" max="7" value={day} onChange={e => setDay(parseInt(e.target.value))} className="w-full" />
             <div className="grid grid-cols-3 gap-4 mt-4 text-center">
                <div><p className="font-bold text-sm">Study Volume</p><div className="h-24 bg-zinc-100 dark:bg-zinc-800 rounded-lg flex items-end mt-2"><motion.div className="w-full bg-blue-400 rounded-t-lg" animate={{height: `${currentData.volume}%`}} /></div></div>
                <div><p className="font-bold text-sm">Intensity</p><div className="h-24 bg-zinc-100 dark:bg-zinc-800 rounded-lg flex items-end mt-2"><motion.div className="w-full bg-rose-400 rounded-t-lg" animate={{height: `${currentData.intensity}%`}} /></div></div>
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
             <div className="my-10 p-8 md:p-12 bg-white dark:bg-zinc-800 rounded-xl border border-zinc-200 dark:border-zinc-700 text-center">
                <h4 className="font-serif text-2xl font-semibold text-zinc-800 dark:text-white text-center">Calculation Sprint</h4>
                <p>1. 15 x 12 = ?</p>
                <p>2. What is 25% of 180?</p>
                <button onClick={() => setDrill('none')} className="text-xs mt-4">Back</button>
             </div>
        );
    }

    if(drill === 'verbal') {
        return (
            <div className="my-10 p-8 md:p-12 bg-white dark:bg-zinc-800 rounded-xl border border-zinc-200 dark:border-zinc-700 text-center">
                <h4 className="font-serif text-2xl font-semibold text-zinc-800 dark:text-white text-center">Verbal Fluency Drill</h4>
                <p>For 60 seconds, list as many words as you can that start with the letter 'P'.</p>
                <p className="text-4xl font-bold my-4">{time}</p>
                <textarea value={words} onChange={e => setWords(e.target.value)} className="w-full h-24 bg-zinc-100 dark:bg-zinc-800 rounded-lg p-2" disabled={time === 0} />
                <button onClick={resetVerbal} className="text-xs mt-4">Reset</button>
            </div>
        );
    }

    return (
        <div className="my-10 p-8 md:p-12 bg-white dark:bg-zinc-800 rounded-xl border border-zinc-200 dark:border-zinc-700 text-center">
             <h4 className="font-serif text-2xl font-semibold text-zinc-800 dark:text-white text-center">Cognitive Warm-Up</h4>
             <p className="text-sm text-zinc-500 dark:text-zinc-400 mb-6">Choose your drill to prime your brain for action.</p>
             <div className="flex justify-center gap-4">
                <button onClick={() => resetVerbal()} className="p-4 bg-zinc-100 dark:bg-zinc-800 rounded-lg">Verbal Fluency</button>
                <button onClick={() => setDrill('math')} className="p-4 bg-zinc-100 dark:bg-zinc-800 rounded-lg">Math Sprint</button>
             </div>
        </div>
    );
};

// --- MODULE COMPONENT ---
const GameDayModule: React.FC<{ onBack: () => void; progress: ModuleProgress; onProgressUpdate: (progress: ModuleProgress) => void }> = ({ onBack, progress, onProgressUpdate }) => {
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

  return (
    <ModuleLayout
      moduleNumber="06"
      moduleTitle="Game Day Protocol"
      theme={theme}
      sections={sections}
      onBack={onBack}
      progress={progress}
      onProgressUpdate={onProgressUpdate}
    >
      {(activeSection) => (
        <>
          {activeSection === 0 && (
            <ReadingSection title="The Athlete Mindset." eyebrow="Step 1" icon={Target} theme={theme}>
              <p>The Leaving Cert is not an academic test; it's an endurance event. Your brain consumes 20% of your body's oxygen and glucose. A 3-hour exam is a metabolic marathon. This module reframes you from a 'student' to an <Highlight description="A paradigm that treats academic performance as a physical discipline, prioritizing physiological optimization (sleep, nutrition, stress management) to maximize cognitive output." theme={theme}>Occupational Athlete</Highlight>. Your success is not just determined by what you know, but by the physiological state of the brain that's trying to access it.</p>
              <p>The key to performance is engineering a <Highlight description="A physiological state where your brain perceives your resources (energy, preparation) as meeting or exceeding the demands of a task. It's characterized by adrenaline (for focus) and vasodilation (increased blood flow to the brain)." theme={theme}>Challenge State</Highlight> ("pumped") and avoiding a <Highlight description="A physiological state where demands are perceived to exceed resources. It's characterized by cortisol (stress hormone) and vasoconstriction, which impairs function of the Prefrontal Cortex, leading to 'mind blanking'." theme={theme}>Threat State</Highlight> ("scared"). This isn't about positive thinking; it's about tangible physiological interventions.</p>
              <ChallengeThreatSimulator />
            </ReadingSection>
          )}
           {activeSection === 1 && (
            <ReadingSection title="The Macrocycle: 1 Month Out." eyebrow="Step 2" icon={SlidersHorizontal} theme={theme}>
              <p>In the final month, the focus shifts from accumulating new knowledge to consolidating what you have and standardizing your biology. This is the "Pre-Competition Phase." Your goal is to align your internal body clock with the external exam schedule through <Highlight description="The process of synchronizing your internal biological clock (circadian rhythm) to external cues, primarily the light-dark cycle." theme={theme}>Circadian Entrainment</Highlight>.</p>
              <p>The average teenager is a "night owl," but exams start at 9:30 AM. You must systematically shift your sleep schedule. This is a gradual process. You also need to switch to a <Highlight description="A diet focused on foods that provide a slow, steady release of glucose (e.g., oats, whole grains) to avoid the 'spike and crash' cycle that impairs cognitive function." theme={theme}>Low-Glycemic Diet</Highlight> to ensure stable fuel for your brain.</p>
              <CircadianShifter />
            </ReadingSection>
          )}
           {activeSection === 2 && (
            <ReadingSection title="The Mesocycle: The Taper." eyebrow="Step 3" icon={Brain} theme={theme}>
              <p>The final week is the most mismanaged period of study. The instinct is to cram, but the athletic model dictates the opposite: <Highlight description="The systematic reduction of training volume in the days before a competition. A 40-60% reduction can lead to a ~3% performance improvement." theme={theme}>Tapering</Highlight>. Performance = Fitness - Fatigue. Cramming maximizes fatigue, leading to a suboptimal performance even if your "fitness" (knowledge) is high.</p>
              <p>The academic taper involves systematically reducing study *volume* while maintaining *intensity*. You do fewer hours, but those hours are high-quality active recall. Crucially, you must stop learning new material 3 days out to avoid <Highlight description="When new information interferes with the recall of older information. This is why last-minute cramming can make you forget things you knew perfectly." theme={theme}>retroactive interference</Highlight>.</p>
              <TaperPlanner />
            </ReadingSection>
          )}
          {activeSection === 3 && (
            <ReadingSection title="Mental Rehearsal." eyebrow="Step 4" icon={Shield} theme={theme}>
              <p>Top athletes don't just train their bodies; they train their minds through visualization. But there's a trap. <Highlight description="Visualizing the final result (e.g., getting 625 points). Research shows this can deplete energy and increase anxiety." theme={theme}>Outcome Visualization</Highlight> can be counterproductive.</p>
              <p>The key is <Highlight description="Visualizing the specific steps of the process (e.g., waking up calm, reading the question, taking a breath). This 'mental rehearsal' prepares the brain for the specific stressors it will face, creating a pre-rehearsed coping mechanism." theme={theme}>Process Visualization</Highlight>. By repeatedly running a "mental movie" of exam day, you prepare your brain for what's coming. When you face a difficult question, your brain recognizes the scenario ("I've been here before") and triggers your rehearsed coping strategy instead of a panic response.</p>
            </ReadingSection>
          )}
          {activeSection === 4 && (
            <ReadingSection title="The Microcycle: Day Before." eyebrow="Step 5" icon={Moon} theme={theme}>
              <p>The 24 hours before your first exam are about stability and anxiety mitigation. All heavy cognitive lifting must cease by 6:00 PM. The evening is for shifting into a "rest and digest" state. Complete the <Highlight description="A control ritual where you pack your clear pencil case, calculator, ID, and water bottle the night before to reduce 'cognitive load' on the morning of the exam." theme={theme}>"Packing" Ritual</Highlight> early.</p>
              <p>Your dinner should be a "Cognitive Carb-Load"--a balanced meal of complex carbs and lean protein (e.g., chicken and sweet potato) to ensure your brain's glycogen stores are full. Finally, perform a <Highlight description="Writing down any lingering facts or worries before sleep to 'offload' them from your working memory, allowing your brain to switch off." theme={theme}>"Brain Dump"</Highlight> to clear your mind.</p>
            </ReadingSection>
          )}
           {activeSection === 5 && (
            <ReadingSection title="Game Day: The Warm-Up." eyebrow="Step 6" icon={Utensils} theme={theme}>
              <p>The morning of the exam is about managing the natural spike in cortisol and adrenaline and channeling it into focus. Do not hit snooze. Immediately hydrate with 500ml of water. Get 10 minutes of morning sunlight to anchor your circadian rhythm. Your breakfast must be Low-GI.</p>
              <p>Just as an athlete warms up their muscles, you must warm up your brain. Passively reading notes is useless. You need a <Highlight description="Active priming exercises (e.g., verbal fluency drills, simple calculations) performed 20-30 minutes before an exam to lower the 'activation threshold' of the relevant neural circuits." theme={theme}>Cognitive Warm-Up</Highlight>. This gets the relevant brain areas perfused with blood and "online" before you open the paper.</p>
              <CognitiveWarmup />
            </ReadingSection>
          )}
           {activeSection === 6 && (
            <ReadingSection title="In The Arena: Execution." eyebrow="Step 7" icon={Zap} theme={theme}>
              <p>Create a psychological "bubble" on arrival. Headphones on, no panicked conversations. Upon entering the hall, perform the <Highlight description="Two sharp inhales through the nose, one long exhale through the mouth. The fastest tool to reduce autonomic arousal in real-time." theme={theme}>Physiological Sigh</Highlight> to calm your nervous system. For the first 5 minutes, do not write. Just read and breathe. This prevents the "panic misread."</p>
            </ReadingSection>
          )}
           {activeSection === 7 && (
            <ReadingSection title="Halftime & Post-Game." eyebrow="Step 8" icon={Wind} theme={theme}>
              <p>On days with two exams, the "halftime" break is critical. Eat a light lunch of protein and complex carbs to avoid a "food coma." A 10-20 minute "Power Nap" or a guided <Highlight description="Non-Sleep Deep Rest. A guided meditation that can restore dopamine levels and reduce cortisol more effectively than a nap for some people." theme={theme}>NSDR</Highlight> script is the most effective way to reset.</p>
              <p>After each exam, the rule is absolute: a strict <Highlight description="The rule to avoid all discussion of an exam after it is finished. This prevents 'anxiety contagion' and keeps your brain out of a 'Threat State' for the next paper." theme={theme}>"Post-Mortem" Ban</Highlight>. The paper is done. Bin the mental file. Focus on the next game.</p>
              <MicroCommitment theme={theme}>
                <p>Go to your calendar. Find the date one month before your first exam. Create an event: "Begin Macrocycle." You are no longer just a student. You are an athlete.</p>
              </MicroCommitment>
            </ReadingSection>
          )}
        </>
      )}
    </ModuleLayout>
  );
};
export default GameDayModule;
