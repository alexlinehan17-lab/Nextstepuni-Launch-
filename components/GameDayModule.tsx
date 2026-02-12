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

// --- PRE-EXAM MEAL BUILDER ---
interface FoodItem {
  id: number;
  name: string;
  emoji: string;
  category: string;
  score: number;
}

const FOODS: FoodItem[] = [
  { id: 1, name: 'Porridge oats', emoji: '🥣', category: 'Low-GI', score: 3 },
  { id: 2, name: 'Wholegrain toast', emoji: '🍞', category: 'Low-GI', score: 2 },
  { id: 3, name: 'Banana', emoji: '🍌', category: 'Low-GI', score: 2 },
  { id: 4, name: 'Natural yoghurt', emoji: '🥛', category: 'Low-GI', score: 2 },
  { id: 5, name: 'Blueberries', emoji: '🫐', category: 'Low-GI', score: 2 },
  { id: 6, name: 'Scrambled eggs', emoji: '🥚', category: 'Protein', score: 3 },
  { id: 7, name: 'Peanut butter', emoji: '🥜', category: 'Protein', score: 2 },
  { id: 8, name: 'Almonds', emoji: '🌰', category: 'Protein', score: 2 },
  { id: 9, name: 'Sugar cereal (Coco Pops)', emoji: '🥣', category: 'High-GI', score: -2 },
  { id: 10, name: 'White bread with jam', emoji: '🍯', category: 'High-GI', score: -1 },
  { id: 11, name: 'Energy drink', emoji: '⚡', category: 'High-GI + Caffeine', score: -3 },
  { id: 12, name: 'Chocolate bar', emoji: '🍫', category: 'High-GI', score: -2 },
  { id: 13, name: 'Black coffee (moderate)', emoji: '☕', category: 'Caffeine', score: 1 },
  { id: 14, name: 'Glass of water', emoji: '💧', category: 'Hydration', score: 2 },
  { id: 15, name: 'Nothing (skip breakfast)', emoji: '🚫', category: 'Empty', score: -4 },
];

const categoryBadgeClass = (category: string): string => {
  if (category.includes('High-GI')) return 'bg-rose-100 text-rose-700 dark:bg-rose-900/40 dark:text-rose-300';
  if (category === 'Low-GI') return 'bg-emerald-100 text-emerald-700 dark:bg-emerald-900/40 dark:text-emerald-300';
  if (category === 'Protein') return 'bg-blue-100 text-blue-700 dark:bg-blue-900/40 dark:text-blue-300';
  if (category === 'Caffeine') return 'bg-amber-100 text-amber-700 dark:bg-amber-900/40 dark:text-amber-300';
  if (category === 'Hydration') return 'bg-sky-100 text-sky-700 dark:bg-sky-900/40 dark:text-sky-300';
  return 'bg-zinc-100 text-zinc-600 dark:bg-zinc-700 dark:text-zinc-300';
};

const MotionDiv = motion.div as any;

const EnergyCurve = ({ level }: { level: 'high' | 'medium' | 'low' }) => {
  const curves = {
    high: {
      path: 'M 0 70 C 30 30, 60 25, 100 28 C 140 31, 200 30, 260 35 C 300 38, 340 40, 380 42',
      color: '#10b981',
      bg: 'bg-emerald-50 dark:bg-emerald-900/20 border-emerald-200 dark:border-emerald-800',
      label: 'Sustained energy. Your brain has steady glucose for 3+ hours. No crash.',
    },
    medium: {
      path: 'M 0 60 C 30 25, 60 30, 120 50 C 160 60, 180 35, 220 55 C 260 65, 300 45, 380 60',
      color: '#f59e0b',
      bg: 'bg-amber-50 dark:bg-amber-900/20 border-amber-200 dark:border-amber-800',
      label: 'Decent, but some crash risk. Consider swapping high-GI items for complex carbs.',
    },
    low: {
      path: 'M 0 70 C 20 10, 50 5, 80 15 C 110 70, 140 85, 200 88 C 240 90, 300 90, 380 92',
      color: '#ef4444',
      bg: 'bg-rose-50 dark:bg-rose-900/20 border-rose-200 dark:border-rose-800',
      label: 'Sugar spike followed by a crash at ~10:30am. Your working memory will suffer mid-exam.',
    },
  };

  const c = curves[level];

  return (
    <MotionDiv
      initial={{ opacity: 0, y: 10 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.5 }}
      className={`mt-6 p-5 rounded-xl border ${c.bg}`}
    >
      <p className="text-sm font-semibold text-zinc-700 dark:text-zinc-200 mb-3">Energy Curve (Exam Morning)</p>
      <div className="flex items-end gap-2 text-xs text-zinc-400 dark:text-zinc-500 mb-1">
        <span>High</span>
      </div>
      <svg viewBox="0 0 380 100" className="w-full h-24" preserveAspectRatio="none">
        <defs>
          <linearGradient id={`grad-${level}`} x1="0" y1="0" x2="0" y2="1">
            <stop offset="0%" stopColor={c.color} stopOpacity="0.3" />
            <stop offset="100%" stopColor={c.color} stopOpacity="0.02" />
          </linearGradient>
        </defs>
        <path d={`${c.path} L 380 100 L 0 100 Z`} fill={`url(#grad-${level})`} />
        <motion.path
          d={c.path}
          fill="none"
          stroke={c.color}
          strokeWidth="3"
          strokeLinecap="round"
          initial={{ pathLength: 0 }}
          animate={{ pathLength: 1 }}
          transition={{ duration: 1.2, ease: 'easeOut' }}
        />
        <text x="5" y="98" fontSize="10" fill="#a1a1aa">7am</text>
        <text x="115" y="98" fontSize="10" fill="#a1a1aa">9:30am</text>
        <text x="250" y="98" fontSize="10" fill="#a1a1aa">11:30am</text>
        <text x="340" y="98" fontSize="10" fill="#a1a1aa">1pm</text>
      </svg>
      <div className="flex items-end gap-2 text-xs text-zinc-400 dark:text-zinc-500 mt-1">
        <span>Low</span>
      </div>
      <p className="mt-3 text-sm font-medium text-zinc-700 dark:text-zinc-300">{c.label}</p>
    </MotionDiv>
  );
};

const PreExamMealBuilder = () => {
  const [selected, setSelected] = useState<number[]>([]);
  const [scored, setScored] = useState(false);

  const toggleFood = (id: number) => {
    if (scored) return;
    setSelected((prev) => {
      if (prev.includes(id)) return prev.filter((f) => f !== id);
      if (prev.length >= 5) return prev;
      return [...prev, id];
    });
  };

  const totalScore = selected.reduce((sum, id) => {
    const food = FOODS.find((f) => f.id === id);
    return sum + (food?.score ?? 0);
  }, 0);

  const energyLevel: 'high' | 'medium' | 'low' = totalScore >= 8 ? 'high' : totalScore >= 3 ? 'medium' : 'low';

  const reset = () => {
    setSelected([]);
    setScored(false);
  };

  const selectedFoods = selected.map((id) => FOODS.find((f) => f.id === id)!);

  return (
    <div className="my-10 p-8 md:p-12 bg-white dark:bg-zinc-800 rounded-xl border border-zinc-200 dark:border-zinc-700">
      <h4 className="font-serif text-2xl font-semibold text-zinc-800 dark:text-white text-center">
        Pre-Exam Meal Builder
      </h4>
      <p className="text-center text-sm text-zinc-500 dark:text-zinc-400 mt-2 mb-8">
        Build your exam morning breakfast. Your brain needs the right fuel.
      </p>

      {/* Food Grid */}
      <div className="grid grid-cols-2 md:grid-cols-3 gap-3">
        {FOODS.map((food) => {
          const isSelected = selected.includes(food.id);
          const isDisabled = !isSelected && selected.length >= 5;
          return (
            <MotionDiv
              key={food.id}
              whileTap={!scored && !isDisabled ? { scale: 0.96 } : {}}
              onClick={() => !isDisabled && toggleFood(food.id)}
              className={`relative p-3 rounded-xl border-2 transition-colors cursor-pointer select-none ${
                scored
                  ? isSelected
                    ? 'border-amber-400 bg-amber-50 dark:bg-amber-900/20'
                    : 'border-zinc-100 dark:border-zinc-700 opacity-40'
                  : isSelected
                  ? 'border-amber-400 bg-amber-50 dark:bg-amber-900/20'
                  : isDisabled
                  ? 'border-zinc-100 dark:border-zinc-700 opacity-40 cursor-not-allowed'
                  : 'border-zinc-200 dark:border-zinc-700 hover:border-amber-300 dark:hover:border-amber-600'
              }`}
            >
              <div className="flex items-center gap-2">
                <span className="text-2xl">{food.emoji}</span>
                <div className="min-w-0">
                  <p className="text-sm font-semibold text-zinc-800 dark:text-white leading-tight truncate">
                    {food.name}
                  </p>
                  <span
                    className={`inline-block mt-1 text-xs font-medium px-2 py-0.5 rounded-full ${categoryBadgeClass(food.category)}`}
                  >
                    {food.category}
                  </span>
                </div>
              </div>
              {isSelected && (
                <MotionDiv
                  initial={{ scale: 0 }}
                  animate={{ scale: 1 }}
                  className="absolute top-1 right-1 w-5 h-5 rounded-full bg-amber-400 flex items-center justify-center text-white text-xs font-bold"
                >
                  {selected.indexOf(food.id) + 1}
                </MotionDiv>
              )}
            </MotionDiv>
          );
        })}
      </div>

      {/* Plate Area */}
      {selected.length > 0 && (
        <MotionDiv
          initial={{ opacity: 0, y: 10 }}
          animate={{ opacity: 1, y: 0 }}
          className="mt-8 p-5 rounded-xl bg-zinc-50 dark:bg-zinc-900/50 border border-zinc-200 dark:border-zinc-700"
        >
          <p className="text-sm font-semibold text-zinc-600 dark:text-zinc-300 mb-3">
            Your Plate ({selected.length}/5)
          </p>
          <div className="flex flex-wrap gap-2">
            {selectedFoods.map((food) => (
              <MotionDiv
                key={food.id}
                initial={{ scale: 0.8, opacity: 0 }}
                animate={{ scale: 1, opacity: 1 }}
                exit={{ scale: 0.8, opacity: 0 }}
                className="flex items-center gap-1.5 bg-white dark:bg-zinc-800 px-3 py-1.5 rounded-full border border-zinc-200 dark:border-zinc-700 text-sm"
              >
                <span>{food.emoji}</span>
                <span className="font-medium text-zinc-700 dark:text-zinc-200">{food.name}</span>
                {scored && (
                  <span
                    className={`ml-1 font-bold ${food.score >= 0 ? 'text-emerald-600 dark:text-emerald-400' : 'text-rose-600 dark:text-rose-400'}`}
                  >
                    {food.score >= 0 ? '+' : ''}{food.score}
                  </span>
                )}
                {!scored && (
                  <button
                    onClick={(e) => {
                      e.stopPropagation();
                      toggleFood(food.id);
                    }}
                    className="ml-1 text-zinc-400 hover:text-rose-500 text-xs font-bold"
                  >
                    ×
                  </button>
                )}
              </MotionDiv>
            ))}
          </div>
        </MotionDiv>
      )}

      {/* Score Button / Results */}
      {!scored && selected.length >= 3 && (
        <MotionDiv initial={{ opacity: 0 }} animate={{ opacity: 1 }} className="mt-6 text-center">
          <button
            onClick={() => setScored(true)}
            className="px-6 py-3 bg-amber-500 hover:bg-amber-600 text-white font-bold rounded-xl transition-colors"
          >
            Score My Meal
          </button>
        </MotionDiv>
      )}

      {!scored && selected.length < 3 && selected.length > 0 && (
        <p className="mt-4 text-center text-sm text-zinc-400 dark:text-zinc-500">
          Select at least 3 items to score your meal.
        </p>
      )}

      {scored && (
        <MotionDiv initial={{ opacity: 0, y: 10 }} animate={{ opacity: 1, y: 0 }}>
          <div className="mt-6 text-center">
            <p className="text-sm font-semibold text-zinc-500 dark:text-zinc-400">Total Score</p>
            <p
              className={`text-4xl font-bold ${
                totalScore >= 8
                  ? 'text-emerald-600 dark:text-emerald-400'
                  : totalScore >= 3
                  ? 'text-amber-600 dark:text-amber-400'
                  : 'text-rose-600 dark:text-rose-400'
              }`}
            >
              {totalScore >= 0 ? '+' : ''}{totalScore}
            </p>
          </div>

          <EnergyCurve level={energyLevel} />

          {/* Per-item breakdown */}
          <div className="mt-5 space-y-2">
            {selectedFoods.map((food) => (
              <div key={food.id} className="flex items-center justify-between text-sm px-3 py-2 bg-zinc-50 dark:bg-zinc-900/50 rounded-lg">
                <span className="text-zinc-700 dark:text-zinc-300">
                  {food.emoji} {food.name}
                </span>
                <span
                  className={`font-bold ${food.score >= 0 ? 'text-emerald-600 dark:text-emerald-400' : 'text-rose-600 dark:text-rose-400'}`}
                >
                  {food.score >= 0 ? '+' : ''}{food.score}
                </span>
              </div>
            ))}
          </div>

          <div className="mt-6 text-center">
            <button
              onClick={reset}
              className="px-5 py-2.5 bg-zinc-200 dark:bg-zinc-700 hover:bg-zinc-300 dark:hover:bg-zinc-600 text-zinc-700 dark:text-zinc-200 font-semibold rounded-xl transition-colors"
            >
              Build Another Meal
            </button>
          </div>
        </MotionDiv>
      )}
    </div>
  );
};

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
      moduleSubtitle="Peak Performance on Demand"
      moduleDescription="Transform your exam preparation by adopting the mindset and physiological protocols of an elite athlete. This is your playbook for peak performance."
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
              <PreExamMealBuilder />
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
