/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
*/

import React, { useState, useEffect } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { Target, Brain, SlidersHorizontal, Shield, Moon, Utensils, Zap, Wind, Leaf, Droplet, Coffee, X } from 'lucide-react';
import { ModuleProgress } from '../types';
import { amberTheme } from '../moduleThemes';
import { Highlight, ReadingSection, MicroCommitment, PersonalStory } from './ModuleShared';
import { ModuleLayout } from './ModuleLayout';
import { useNorthStar } from '../hooks/useNorthStar';
import NorthStarCallout from './NorthStarCallout';
import { COMPACT_CALLOUT_PLACEMENTS } from '../northStarData';

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
                {isChallenge ? "CHALLENGE STATE: You feel 'pumped'. More blood and oxygen flow to your brain. Go time." : "THREAT STATE: You feel 'scared'. Your brain tightens up, thinking gets foggy. 'Mind blanking' is likely."}
             </div>
        </div>
    );
};

const CircadianShifter = () => {
    const [wakeTime, setWakeTime] = useState(9);
    const shifts = Math.ceil(((wakeTime - 7) * 60) / 15);

    return(
        <div className="my-10 p-8 md:p-12 bg-white dark:bg-zinc-800 rounded-xl border border-zinc-200 dark:border-zinc-700">
             <h4 className="font-serif text-2xl font-semibold text-zinc-800 dark:text-white text-center">Sleep Schedule Shifter</h4>
             <p className="text-center text-sm text-zinc-500 dark:text-zinc-400 mb-6">Enter your current weekend wake-up time to get a 4-week plan for shifting it earlier.</p>
             <div className="flex items-center justify-center gap-4">
                <label className="font-bold">Current Wake-up:</label>
                <input type="time" value={`${String(Math.floor(wakeTime)).padStart(2,'0')}:${String((wakeTime % 1)*60).padStart(2,'0')}`} onChange={e => setWakeTime(parseInt(e.target.value.split(':')[0]) + parseInt(e.target.value.split(':')[1])/60)} className="p-2 bg-zinc-100 dark:bg-zinc-800 rounded-lg"/>
             </div>
             {wakeTime > 7 && <div className="mt-6 p-4 bg-amber-50 border border-amber-200 rounded-xl text-center">
                <p className="font-bold text-amber-800">Your Plan:</p>
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
             <h4 className="font-serif text-2xl font-semibold text-zinc-800 dark:text-white text-center">Final Week Study Planner</h4>
             <p className="text-center text-sm text-zinc-500 dark:text-zinc-400 mb-6">Move the slider to see how your study should change in the final week.</p>
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
  category: string;
  score: number;
}

const FOODS: FoodItem[] = [
  { id: 1, name: 'Porridge oats', category: 'Low-GI', score: 3 },
  { id: 2, name: 'Wholegrain toast', category: 'Low-GI', score: 2 },
  { id: 3, name: 'Banana', category: 'Low-GI', score: 2 },
  { id: 4, name: 'Natural yoghurt', category: 'Low-GI', score: 2 },
  { id: 5, name: 'Blueberries', category: 'Low-GI', score: 2 },
  { id: 6, name: 'Scrambled eggs', category: 'Protein', score: 3 },
  { id: 7, name: 'Peanut butter', category: 'Protein', score: 2 },
  { id: 8, name: 'Almonds', category: 'Protein', score: 2 },
  { id: 9, name: 'Sugar cereal (Coco Pops)', category: 'High-GI', score: -2 },
  { id: 10, name: 'White bread with jam', category: 'High-GI', score: -1 },
  { id: 11, name: 'Energy drink', category: 'High-GI + Caffeine', score: -3 },
  { id: 12, name: 'Chocolate bar', category: 'High-GI', score: -2 },
  { id: 13, name: 'Black coffee (moderate)', category: 'Caffeine', score: 1 },
  { id: 14, name: 'Glass of water', category: 'Hydration', score: 2 },
  { id: 15, name: 'Nothing (skip breakfast)', category: 'Empty', score: -4 },
];

const FoodIcon = ({ category, size = 'md' }: { category: string; size?: 'sm' | 'md' }) => {
  const cls = size === 'md' ? 'w-6 h-6' : 'w-4 h-4';
  if (category === 'Low-GI') return <Leaf className={`${cls} text-emerald-500`} />;
  if (category === 'Protein') return <Shield className={`${cls} text-blue-500`} />;
  if (category.includes('High-GI')) return <Zap className={`${cls} text-rose-500`} />;
  if (category === 'Caffeine') return <Coffee className={`${cls} text-amber-600`} />;
  if (category === 'Hydration') return <Droplet className={`${cls} text-sky-500`} />;
  return <X className={`${cls} text-zinc-400`} />;
};

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
      <svg viewBox="0 0 380 80" className="w-full h-20" preserveAspectRatio="none">
        <defs>
          <linearGradient id={`grad-${level}`} x1="0" y1="0" x2="0" y2="1">
            <stop offset="0%" stopColor={c.color} stopOpacity="0.3" />
            <stop offset="100%" stopColor={c.color} stopOpacity="0.02" />
          </linearGradient>
        </defs>
        <path d={`${c.path} L 380 80 L 0 80 Z`} fill={`url(#grad-${level})`} />
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
      </svg>
      <div className="flex justify-between text-xs text-zinc-400 dark:text-zinc-500 mt-1 px-1">
        <span>7am</span>
        <span>9:30am</span>
        <span>11:30am</span>
        <span>1pm</span>
      </div>
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
                <FoodIcon category={food.category} />
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
                <FoodIcon category={food.category} size="sm" />
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
                <span className="flex items-center gap-1.5 text-zinc-700 dark:text-zinc-300">
                  <FoodIcon category={food.category} size="sm" /> {food.name}
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
             <h4 className="font-serif text-2xl font-semibold text-zinc-800 dark:text-white text-center">Brain Warm-Up</h4>
             <p className="text-sm text-zinc-500 dark:text-zinc-400 mb-6">Pick a quick drill to get your brain warmed up and ready.</p>
             <div className="flex justify-center gap-4">
                <button onClick={() => resetVerbal()} className="p-4 bg-zinc-100 dark:bg-zinc-800 rounded-lg">Verbal Fluency</button>
                <button onClick={() => setDrill('math')} className="p-4 bg-zinc-100 dark:bg-zinc-800 rounded-lg">Math Sprint</button>
             </div>
        </div>
    );
};

// --- MODULE COMPONENT ---
const GameDayModule: React.FC<{ onBack: () => void; progress: ModuleProgress; onProgressUpdate: (progress: ModuleProgress) => void }> = ({ onBack, progress, onProgressUpdate }) => {
  const { northStar } = useNorthStar();
  const sections = [
    { id: 'athlete-mindset', title: 'The Athlete Mindset', eyebrow: '01 // The Game Plan', icon: Target },
    { id: 'macrocycle', title: '1 Month Out', eyebrow: '02 // Building Your Base', icon: SlidersHorizontal },
    { id: 'mesocycle', title: 'The Final Week', eyebrow: '03 // The Wind-Down', icon: Brain },
    { id: 'mental-rehearsal', title: 'Mental Rehearsal', eyebrow: '04 // Visualization', icon: Shield },
    { id: 'microcycle', title: 'The Day Before', eyebrow: '05 // Setting Up', icon: Moon },
    { id: 'game-day-morning', title: 'Game Day Morning', eyebrow: '06 // The Warm-Up', icon: Utensils },
    { id: 'in-the-arena', title: 'In The Arena', eyebrow: '07 // Go Time', icon: Zap },
    { id: 'recovery', title: 'Halftime & Post-Game', eyebrow: '08 // Recovery', icon: Wind },
  ];

  return (
    <ModuleLayout
      moduleNumber="06"
      moduleTitle="Game Day: Peak Performance"
      moduleSubtitle="Peak Performance on Demand"
      moduleDescription="Train for the Leaving Cert the way athletes train for competition. Sleep, food, mindset, and a solid game plan -- this is your playbook for performing at your best when it counts."
      theme={theme}
      sections={sections}
      onBack={onBack}
      progress={progress}
      onProgressUpdate={onProgressUpdate}
      finishButtonText="Game On"
    >
      {(activeSection) => (
        <>
          {activeSection === 0 && (
            <ReadingSection title="The Athlete Mindset." eyebrow="Step 1" icon={Target} theme={theme}>
              <p>The Leaving Cert is not just an academic test -- it's an endurance event. Your brain uses 20% of your body's energy. A 3-hour exam is basically a marathon for your head. This module is about treating yourself like an <Highlight description="The idea that you're not just studying with your mind -- your body matters too. Sleep, food, and stress management all directly affect how well your brain performs on the day." theme={theme}>Exam Athlete</Highlight>. How well you do isn't just about what you know -- it's about the state your brain is in when it's trying to remember it all.</p>
              <p>The goal is to get yourself into a <Highlight description="That 'I've got this' feeling. When you feel prepared and energised, your body sends more blood and oxygen to your brain. You think faster and stay focused." theme={theme}>Challenge State</Highlight> ("pumped") and avoid a <Highlight description="That 'I'm going to fail' feeling. When your brain thinks the exam is too much, stress hormones take over and your thinking brain basically shuts down. That's where 'mind blanking' comes from." theme={theme}>Threat State</Highlight> ("scared"). This isn't about positive thinking. It's about real, practical steps you can take to get your body and brain working together.</p>
              <PersonalStory name="Aisling" role="6th Year, Limerick">
                <p>Before my mocks, I used to just cram until 2am and hope for the best. I'd walk into the exam wrecked and my mind would go blank on stuff I definitely knew. When I started treating exam prep more like training -- sorting my sleep, eating properly, doing a warm-up routine -- it was like night and day. I wasn't any smarter, I was just less wrecked.</p>
              </PersonalStory>
              <ChallengeThreatSimulator />
            </ReadingSection>
          )}
           {activeSection === 1 && (
            <ReadingSection title="1 Month Out: Building Your Base." eyebrow="Step 2" icon={SlidersHorizontal} theme={theme}>
              <p>In the final month, the focus shifts from learning new stuff to locking in what you already know -- and getting your body into a good routine. Your main job right now is to get your <Highlight description="Getting your body clock in sync with exam times. If you've been going to bed at 1am and waking at 11am, you need to gradually shift that so you're sharp at 9:30am when the exam starts." theme={theme}>sleep schedule lined up with exam times</Highlight>.</p>
              <p>Most teenagers are night owls, but exams start at 9:30 AM. You need to gradually shift your wake-up time -- not all at once, but bit by bit. You should also start eating more <Highlight description="Foods like porridge, wholegrain bread, and bananas that give you slow, steady energy instead of a sugar spike followed by a crash. Think fuel that lasts the whole exam, not just the first 20 minutes." theme={theme}>slow-release energy foods</Highlight> so your brain has steady fuel instead of a sugar crash halfway through the paper.</p>
              <CircadianShifter />
            </ReadingSection>
          )}
           {activeSection === 2 && (
            <ReadingSection title="The Final Week: Winding Down." eyebrow="Step 3" icon={Brain} theme={theme}>
              <p>The last week before exams is where most students mess up. The instinct is to cram harder, but that's the opposite of what works. Athletes <Highlight description="Easing off in the days before a big event. Less volume, more rest. Cutting your study hours by 40-60% in the final days actually improves your performance because you go in fresh instead of burnt out." theme={theme}>ease off before a big event</Highlight> -- and you should too. Think of it this way: Performance = What You Know minus How Tired You Are. Cramming makes you exhausted, so even if you know loads, your brain can't access it properly.</p>
              <p>In the final week, you do fewer hours but make those hours count -- testing yourself, not just reading over notes. And here's the big one: stop learning new material 3 days out. Last-minute cramming can actually cause <Highlight description="When new information messes up your ability to remember older stuff. It's why cramming the night before can make you forget things you knew perfectly well last week." theme={theme}>new stuff to push out old stuff</Highlight> you already knew.</p>
              <TaperPlanner />
            </ReadingSection>
          )}
          {activeSection === 3 && (
            <ReadingSection title="Mental Rehearsal." eyebrow="Step 4" icon={Shield} theme={theme}>
              <p>Top athletes don't just train their bodies -- they train their minds through visualization. But there's a trap. <Highlight description="Picturing the end result (e.g. getting 625 points or opening your CAO offer). This can actually make you feel like you've already achieved it, which drains your motivation and can increase anxiety." theme={theme}>Just picturing the result</Highlight> (like imagining your CAO points) can actually backfire.</p>
              <p>What works is <Highlight description="Picturing the actual steps: waking up calm, walking into the hall, reading the first question, taking a breath before writing. When you've 'been there' in your head, your brain handles the real thing much better -- instead of panicking, it goes 'I know what to do here.'" theme={theme}>picturing the process</Highlight>. Run a "mental movie" of exam day in your head -- waking up, eating, walking in, reading the paper. When you hit a hard question on the day, your brain recognises the moment ("I've been here before") and stays calm instead of panicking.</p>
            </ReadingSection>
          )}
          {activeSection === 4 && (
            <ReadingSection title="The Day Before." eyebrow="Step 5" icon={Moon} theme={theme}>
              <p>The 24 hours before your first exam are about keeping things calm and steady. Stop any heavy studying by 6:00 PM. The evening is for winding down. Do your <Highlight description="Pack your clear pencil case, calculator, ID, exam number, and a bottle of water the night before. Getting this sorted early means one less thing to stress about in the morning." theme={theme}>"Packing" Ritual</Highlight> early so you're not scrambling in the morning.</p>
              <p>For dinner, go for something filling with slow-release energy -- pasta, rice, potatoes with some protein (whatever you have -- chicken, beans, eggs, anything decent). The goal is to fill up your energy stores so your brain has fuel in the morning. Before bed, do a <Highlight description="Grab a page and write down anything still bouncing around your head -- facts you're worried about, things on your mind, whatever. Getting it out of your head and onto paper helps your brain switch off so you can actually sleep." theme={theme}>"Brain Dump"</Highlight>: write down anything still buzzing around your head so your brain can switch off.</p>
            </ReadingSection>
          )}
           {activeSection === 5 && (
            <ReadingSection title="Game Day: The Warm-Up." eyebrow="Step 6" icon={Utensils} theme={theme}>
              {northStar && (() => { const p = COMPACT_CALLOUT_PLACEMENTS.find(p => p.moduleId === 'game-day-protocol'); return p ? <NorthStarCallout northStar={northStar} variant="compact" message={p.message} /> : null; })()}
              <p>The morning of the exam is about channeling your nerves into focus. Don't hit snooze. Drink a glass of water straight away. If you can, get a few minutes of daylight (even standing by a window helps) -- it wakes your brain up properly. Eat a breakfast that gives you slow, steady energy (more on that below).</p>
              <PreExamMealBuilder />
              <p>Just as an athlete warms up before a match, you need to warm up your brain. Passively reading over notes doesn't do much. What actually helps is a quick <Highlight description="Short brain exercises -- like listing words that start with a certain letter, or doing a few quick mental sums -- done 20-30 minutes before the exam. It gets the thinking parts of your brain warmed up and ready to go before you open the paper." theme={theme}>brain warm-up</Highlight>. It gets the right parts of your brain fired up and ready before you even open the paper.</p>
              <CognitiveWarmup />
            </ReadingSection>
          )}
           {activeSection === 6 && (
            <ReadingSection title="In The Arena: Execution." eyebrow="Step 7" icon={Zap} theme={theme}>
              <p>When you arrive, put yourself in a bubble. Headphones in if you have them, or just keep to yourself -- avoid panicked conversations with other students. When you sit down, do the <Highlight description="A quick breathing trick: two sharp sniffs in through your nose, then one long, slow breath out through your mouth. It's the fastest way to calm your nerves in the moment." theme={theme}>Physiological Sigh</Highlight> (two quick sniffs in through your nose, one long breath out). For the first 5 minutes, don't write anything. Just read the paper and breathe. This stops you from misreading questions in a panic.</p>
            </ReadingSection>
          )}
           {activeSection === 7 && (
            <ReadingSection title="Halftime & Post-Game." eyebrow="Step 8" icon={Wind} theme={theme}>
              <p>On days with two exams, the break between them is huge. Eat something that won't make you sleepy -- a sandwich, some fruit, whatever you can manage -- and avoid a massive heavy meal. If you can, a 10-20 minute nap or a quick <Highlight description="A guided relaxation technique you can find free on YouTube or Spotify. You lie down, close your eyes, and follow the instructions. It's not sleep, but it recharges your brain surprisingly well -- sometimes even better than a nap." theme={theme}>guided rest session (NSDR)</Highlight> is one of the best ways to recharge for the afternoon.</p>
              <p>After each exam, one rule: <Highlight description="Don't talk about the exam you just did. Seriously. When everyone starts comparing answers, it spreads panic -- and that panic follows you into your next paper. The exam is done. Let it go." theme={theme}>don't talk about it</Highlight>. No comparing answers, no "what did you get for question 5?" The paper is done. Bin the mental file. Focus on the next one.</p>
              <MicroCommitment theme={theme}>
                <p>Go to your calendar (phone, wall, whatever you have). Find the date one month before your first exam. Set a reminder: "Start my game day prep." From that point on, you're not just studying -- you're training.</p>
              </MicroCommitment>
            </ReadingSection>
          )}
        </>
      )}
    </ModuleLayout>
  );
};
export default GameDayModule;
