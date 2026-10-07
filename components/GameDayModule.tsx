/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
*/

import { motion } from 'framer-motion';
import { Brain,Coffee,Droplet,Leaf,Moon,Shield,SlidersHorizontal,Target,Utensils,Wind,X,Zap } from 'lucide-react';
import React,{ useEffect,useState } from 'react';
import { GAME_DAY_REFERENCE_LIST } from '../data/references/gameDay';
import { useEssentialsMode } from '../hooks/useEssentialsMode';
import { useNorthStar } from '../hooks/useNorthStar';
import { amberTheme } from '../moduleThemes';
import { COMPACT_CALLOUT_PLACEMENTS } from '../northStarData';
import { type ModuleProgress } from '../types';
import { ModuleLayout } from './ModuleLayout';
import { Cite } from './ModuleReferences';
import { Highlight,MicroCommitment,PersonalStory,ReadingSection,ToolJumpCard } from './ModuleShared';
import { MotionDiv } from './Motion';
import NorthStarCallout from './NorthStarCallout';

const theme = amberTheme;

// --- INTERACTIVE COMPONENTS ---
const ChallengeThreatSimulator = () => {
    const [resources, setResources] = useState(50);
    const isChallenge = resources >= 50;

    return (
        <div className="my-10 rounded-2xl p-8 md:p-12" style={{ backgroundColor: "var(--module-surface)", borderRadius: 18 }}>
             <h4 className="font-serif text-2xl font-semibold text-[var(--module-ink)] dark:text-[var(--module-ink)] text-center">Challenge vs. Threat State</h4>
             <div className="grid grid-cols-2 gap-8 items-center mt-8">
                <div className="text-center">
                    <p className="font-bold text-sm">Demands (The Exam)</p>
                    <div className="h-8 w-full bg-[var(--module-danger-soft)] rounded-full mt-2 border border-[var(--module-line)]" />
                </div>
                <div className="text-center">
                    <p className="font-bold text-sm">Your Resources</p>
                    <div className="h-8 w-full bg-[var(--module-surface)] dark:bg-[var(--module-surface)] rounded-full mt-2"><motion.div className="h-full bg-[var(--module-success)] rounded-full" animate={{width: `${resources}%`}} /></div>
                </div>
             </div>
             <div className="flex justify-center gap-2 mt-4"><span className="font-bold">Resource Level:</span><input type="range" value={resources} onChange={e => setResources(parseInt(e.target.value))} className="chunky-slider chunky-slider-sky" /></div>
             <div className="mt-6 p-4 rounded-xl text-center font-bold" style={isChallenge ? { backgroundColor: "var(--module-success-soft)", border: "2.5px solid var(--module-line)", boxShadow: 'none', color: "var(--module-success-text)", borderRadius: 14 } : { backgroundColor: "var(--module-surface)", border: "2.5px solid var(--module-line)", boxShadow: 'none', color: "var(--module-danger-text)", borderRadius: 14 }}>
                {isChallenge ? "CHALLENGE STATE: You feel 'pumped'. More blood and oxygen flow to your brain. Go time." : "THREAT STATE: You feel 'scared'. Your brain tightens up, thinking gets foggy. 'Mind blanking' is likely."}
             </div>
        </div>
    );
};

const CircadianShifter = () => {
    const [wakeTime, setWakeTime] = useState(9);
    const shifts = Math.ceil(((wakeTime - 7) * 60) / 15);

    return(
        <div className="my-10 rounded-2xl p-6 md:p-8" style={{ backgroundColor: "var(--module-surface)", borderRadius: 18 }}>
             <h4 className="font-serif font-bold text-center" style={{ fontSize: 22, color: "var(--module-ink)" }}>Sleep Schedule Shifter</h4>
             <p className="text-center text-sm mt-1 mb-6" style={{ color: "var(--module-muted)" }}>Enter your current weekend wake-up time to get a 4-week plan for shifting it earlier.</p>
             <div className="flex flex-col items-center gap-2">
                <label style={{ fontSize: 10, fontWeight: 700, letterSpacing: '0.12em', color: "var(--module-muted)", textTransform: 'uppercase' as const }}>Current Wake-up Time</label>
                <input type="time" value={`${String(Math.floor(wakeTime)).padStart(2,'0')}:${String((wakeTime % 1)*60).padStart(2,'0')}`} onChange={e => setWakeTime(parseInt(e.target.value.split(':')[0]) + parseInt(e.target.value.split(':')[1])/60)} className="outline-none" style={{ border: "1.5px solid var(--module-line)", borderRadius: 10, padding: '12px 16px', fontSize: 16, color: "var(--module-ink)" }} onFocus={(e) => { e.currentTarget.style.borderColor = "var(--module-danger-text)"; }} onBlur={(e) => { e.currentTarget.style.borderColor = "var(--module-muted)"; }} />
             </div>
             {wakeTime > 7 && (
                <div className="mt-6 text-center" style={{ backgroundColor: "var(--module-surface)", border: "2px solid var(--module-line)", borderRadius: 14, padding: '20px 24px' }}>
                    <p className="font-serif font-semibold" style={{ fontSize: 18, color: "var(--module-danger-text)" }}>Your Plan:</p>
                    <p className="mt-2" style={{ fontSize: 15, color: "var(--module-ink)" }}>Shift your alarm back by 15 mins every <span className="font-bold" style={{ color: "var(--module-danger-text)" }}>3–4 days</span> for the next <span className="font-bold" style={{ color: "var(--module-danger-text)" }}>{shifts}</span> shifts to reach your 7:00 AM target.</p>
                </div>
             )}
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
    const taperKey = Object.keys(taperData).reverse().find(d => parseInt(d) >= day) || Object.keys(taperData)[0];
    const currentData = taperData[day as keyof typeof taperData] || taperData[taperKey as unknown as keyof typeof taperData];

    return (
        <div className="my-10 rounded-2xl p-8 md:p-12" style={{ backgroundColor: "var(--module-surface)", borderRadius: 18 }}>
             <h4 className="font-serif text-2xl font-semibold text-[var(--module-ink)] dark:text-[var(--module-ink)] text-center">Final Week Study Planner</h4>
             <p className="text-center text-sm text-[var(--module-muted)] dark:text-[var(--module-muted)] mb-6">Move the slider to see how your study should change in the final week.</p>
             <label className="font-bold">Days Before Exam: {day}</label>
             <input type="range" min="1" max="7" value={day} onChange={e => setDay(parseInt(e.target.value))} className="chunky-slider chunky-slider-sunshine" />
             <div className="grid grid-cols-3 gap-4 mt-4 text-center">
                <div><p className="font-bold text-sm">Study Volume</p><div className="h-24 bg-[var(--module-surface)] dark:bg-[var(--module-surface)] rounded-lg flex items-end mt-2"><motion.div className="w-full bg-[var(--module-solid)] rounded-t-lg" animate={{height: `${currentData.volume}%`}} /></div></div>
                <div><p className="font-bold text-sm">Intensity</p><div className="h-24 bg-[var(--module-surface)] dark:bg-[var(--module-surface)] rounded-lg flex items-end mt-2"><motion.div className="w-full bg-[var(--module-danger)] rounded-t-lg" animate={{height: `${currentData.intensity}%`}} /></div></div>
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
  { id: 13, name: 'Black coffee (moderate)', category: 'Caffeine', score: 0 },
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
  if (category.includes('High-GI')) return "bg-[var(--module-danger-soft)] text-[var(--module-danger-text)] dark:bg-[var(--module-danger-soft)] dark:text-[var(--module-danger-text)]";
  if (category === 'Low-GI') return "bg-[var(--module-success-soft)] text-[var(--module-success-text)] dark:bg-[var(--module-success-soft)] dark:text-[var(--module-success-text)]";
  if (category === 'Protein') return "bg-[var(--module-surface)] text-[var(--module-ink)] dark:bg-[var(--module-surface)] dark:text-[var(--module-ink)]";
  if (category === 'Caffeine') return "bg-[var(--module-surface)] text-[var(--module-ink)] dark:bg-[var(--module-surface)] dark:text-[var(--module-ink)]";
  if (category === 'Hydration') return "bg-[var(--module-surface)] text-[var(--module-ink)] dark:bg-[var(--module-surface)] dark:text-[var(--module-ink)]";
  return "bg-[var(--module-surface)] text-[var(--module-ink)] dark:bg-[var(--module-surface)] dark:text-[var(--module-muted)]";
};

const EnergyCurve = ({ level }: { level: 'high' | 'medium' | 'low' }) => {
  const curves = {
    high: {
      path: 'M 0 70 C 30 30, 60 25, 100 28 C 140 31, 200 30, 260 35 C 300 38, 340 40, 380 42',
      color: "var(--module-success-text)",
      bg: "bg-[var(--module-success-soft)] dark:bg-[var(--module-success-soft)] border-[var(--module-line)] dark:border-[var(--module-line)]",
      label: 'Sustained energy. Your brain has steady glucose for 3+ hours. No crash.',
    },
    medium: {
      path: 'M 0 60 C 30 25, 60 30, 120 50 C 160 60, 180 35, 220 55 C 260 65, 300 45, 380 60',
      color: "var(--module-ink)",
      bg: "bg-[var(--module-surface)] dark:bg-[var(--module-surface)] border-[var(--module-line)] dark:border-[var(--module-line)]",
      label: 'Decent, but some crash risk. Consider swapping high-GI items for complex carbs.',
    },
    low: {
      path: 'M 0 70 C 20 10, 50 5, 80 15 C 110 70, 140 85, 200 88 C 240 90, 300 90, 380 92',
      color: "var(--module-danger-text)",
      bg: "bg-[var(--module-danger-soft)] dark:bg-[var(--module-danger-soft)] border-[var(--module-line)] dark:border-[var(--module-line)]",
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
      <p className="text-sm font-semibold text-[var(--module-ink)] dark:text-[var(--module-muted)] mb-3">Energy Curve (Exam Morning)</p>
      <div className="flex items-end gap-2 text-xs text-[var(--module-muted)] dark:text-[var(--module-muted)] mb-1">
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
      <div className="flex justify-between text-xs text-[var(--module-muted)] dark:text-[var(--module-muted)] mt-1 px-1">
        <span>7am</span>
        <span>9:30am</span>
        <span>11:30am</span>
        <span>1pm</span>
      </div>
      <div className="flex items-end gap-2 text-xs text-[var(--module-muted)] dark:text-[var(--module-muted)] mt-1">
        <span>Low</span>
      </div>
      <p className="mt-3 text-sm font-medium text-[var(--module-ink)] dark:text-[var(--module-muted)]">{c.label}</p>
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
    <div className="my-10 rounded-2xl p-8 md:p-12" style={{ backgroundColor: "var(--module-surface)", borderRadius: 18 }}>
      <h4 className="font-serif text-2xl font-semibold text-[var(--module-ink)] dark:text-[var(--module-ink)] text-center">
        Pre-Exam Meal Builder
      </h4>
      <p className="text-center text-sm text-[var(--module-muted)] dark:text-[var(--module-muted)] mt-2 mb-8">
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
              className="relative p-3 transition-all cursor-pointer select-none"
              style={
                scored
                  ? isSelected
                    ? { backgroundColor: "var(--module-surface)", border: "2.5px solid var(--module-line)", borderRadius: 14, boxShadow: 'none' }
                    : { backgroundColor: "var(--module-surface)", border: "2.5px solid var(--module-line)", borderRadius: 14, opacity: 0.4 }
                  : isSelected
                  ? { backgroundColor: "var(--module-surface)", border: "2.5px solid var(--module-line)", borderRadius: 14, boxShadow: 'none' }
                  : isDisabled
                  ? { backgroundColor: "var(--module-surface)", border: "2.5px solid var(--module-line)", borderRadius: 14, opacity: 0.4, cursor: 'not-allowed' }
                  : { backgroundColor: "var(--module-surface)", border: "2.5px solid var(--module-line)", borderRadius: 14, boxShadow: 'none' }
              }
            >
              <div className="flex items-center gap-2">
                <FoodIcon category={food.category} />
                <div className="min-w-0">
                  <p className="text-sm font-semibold text-[var(--module-ink)] dark:text-[var(--module-ink)] leading-tight truncate">
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
                  className="absolute top-1 right-1 w-5 h-5 rounded-full bg-[var(--module-surface)] flex items-center justify-center text-[var(--module-ink)] text-xs font-bold"
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
          className="mt-8 p-5 rounded-xl bg-[var(--module-surface)] dark:bg-[var(--module-surface)] border border-[var(--module-line)] dark:border-[var(--module-line)]"
        >
          <p className="text-sm font-semibold text-[var(--module-ink)] dark:text-[var(--module-muted)] mb-3">
            Your Plate ({selected.length}/5)
          </p>
          <div className="flex flex-wrap gap-2">
            {selectedFoods.map((food) => (
              <MotionDiv
                key={food.id}
                initial={{ scale: 0.8, opacity: 0 }}
                animate={{ scale: 1, opacity: 1 }}
                exit={{ scale: 0.8, opacity: 0 }}
                className="flex items-center gap-1.5 bg-[var(--module-surface)] dark:bg-[var(--module-surface)] px-3 py-1.5 rounded-full border border-[var(--module-line)] dark:border-[var(--module-line)] text-sm"
              >
                <FoodIcon category={food.category} size="sm" />
                <span className="font-medium text-[var(--module-ink)] dark:text-[var(--module-muted)]">{food.name}</span>
                {scored && (
                  <span
                    className={`ml-1 font-bold ${food.score >= 0 ? "text-[var(--module-success-text)] dark:text-[var(--module-success-text)]" : "text-[var(--module-danger-text)] dark:text-[var(--module-danger-text)]"}`}
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
                    className="ml-1 text-[var(--module-muted)] hover:text-[var(--module-danger-text)] text-xs font-bold" data-wide-button="true"
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
            className="px-6 py-3 bg-[var(--module-surface)] hover:bg-[var(--module-surface)] text-[var(--module-ink)] font-bold rounded-xl transition-colors" data-wide-button="true"
          >
            Score My Meal
          </button>
        </MotionDiv>
      )}

      {!scored && selected.length < 3 && selected.length > 0 && (
        <p className="mt-4 text-center text-sm text-[var(--module-muted)] dark:text-[var(--module-muted)]">
          Select at least 3 items to score your meal.
        </p>
      )}

      {scored && (
        <MotionDiv initial={{ opacity: 0, y: 10 }} animate={{ opacity: 1, y: 0 }}>
          <div className="mt-6 text-center">
            <p className="text-sm font-semibold text-[var(--module-muted)] dark:text-[var(--module-muted)]">Total Score</p>
            <p
              className={`text-4xl font-bold ${
                totalScore >= 8
                  ? "text-[var(--module-success-text)] dark:text-[var(--module-success-text)]"
                  : totalScore >= 3
                  ? "text-[var(--module-ink)] dark:text-[var(--module-ink)]"
                  : "text-[var(--module-danger-text)] dark:text-[var(--module-danger-text)]"
              }`}
            >
              {totalScore >= 0 ? '+' : ''}{totalScore}
            </p>
          </div>

          <EnergyCurve level={energyLevel} />

          {/* Per-item breakdown */}
          <div className="mt-5 space-y-2">
            {selectedFoods.map((food) => (
              <div key={food.id} className="flex items-center justify-between text-sm px-3 py-2 bg-[var(--module-surface)] dark:bg-[var(--module-surface)] rounded-lg">
                <span className="flex items-center gap-1.5 text-[var(--module-ink)] dark:text-[var(--module-muted)]">
                  <FoodIcon category={food.category} size="sm" /> {food.name}
                </span>
                <span
                  className={`font-bold ${food.score >= 0 ? "text-[var(--module-success-text)] dark:text-[var(--module-success-text)]" : "text-[var(--module-danger-text)] dark:text-[var(--module-danger-text)]"}`}
                >
                  {food.score >= 0 ? '+' : ''}{food.score}
                </span>
              </div>
            ))}
          </div>

          <div className="mt-6 text-center">
            <button
              onClick={reset}
              className="px-5 py-2.5 bg-[var(--module-surface)] dark:bg-[var(--module-surface)] hover:bg-[var(--module-surface)] dark:hover:bg-[var(--module-surface)] text-[var(--module-ink)] dark:text-[var(--module-muted)] font-semibold rounded-xl transition-colors" data-wide-button="true"
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
             <div className="my-10 rounded-2xl p-8 md:p-12 text-center" style={{ backgroundColor: "var(--module-surface)", borderRadius: 18 }}>
                <h4 className="font-serif text-2xl font-semibold text-[var(--module-ink)] dark:text-[var(--module-ink)] text-center">Calculation Sprint</h4>
                <p>1. 15 x 12 = ?</p>
                <p>2. What is 25% of 180?</p>
                <button onClick={() => setDrill('none')} className="text-xs mt-4" data-wide-button="true">Back</button>
             </div>
        );
    }

    if(drill === 'verbal') {
        return (
            <div className="my-10 rounded-2xl p-8 md:p-12 text-center" style={{ backgroundColor: "var(--module-surface)", borderRadius: 18 }}>
                <h4 className="font-serif text-2xl font-semibold text-[var(--module-ink)] dark:text-[var(--module-ink)] text-center">Verbal Fluency Drill</h4>
                <p>For 60 seconds, list as many words as you can that start with the letter 'P'.</p>
                <p className="text-4xl font-bold my-4">{time}</p>
                <textarea value={words} onChange={e => setWords(e.target.value)} className="w-full h-24 bg-[var(--module-surface)] dark:bg-[var(--module-surface)] rounded-lg p-2" disabled={time === 0} />
                <button onClick={resetVerbal} className="text-xs mt-4" data-wide-button="true">Reset</button>
            </div>
        );
    }

    return (
        <div className="my-10 rounded-2xl p-8 md:p-12 text-center" style={{ backgroundColor: "var(--module-surface)", borderRadius: 18 }}>
             <h4 className="font-serif text-2xl font-semibold text-[var(--module-ink)] dark:text-[var(--module-ink)] text-center">Brain Warm-Up</h4>
             <p className="text-sm text-[var(--module-muted)] dark:text-[var(--module-muted)] mb-6">Pick a quick drill to get your brain warmed up and ready.</p>
             <div className="flex justify-center gap-4">
                <button onClick={() => resetVerbal()} className="p-4 font-bold text-sm transition-all" style={{ backgroundColor: "var(--module-surface)", border: "2.5px solid var(--module-line)", borderRadius: 14, boxShadow: 'none', color: "var(--module-ink)" }} data-wide-button="true">Verbal Fluency</button>
                <button onClick={() => setDrill('math')} className="p-4 font-bold text-sm transition-all" style={{ backgroundColor: "var(--module-surface)", border: "2.5px solid var(--module-line)", borderRadius: 14, boxShadow: 'none', color: "var(--module-ink)" }} data-wide-button="true">Math Sprint</button>
             </div>
        </div>
    );
};

// --- MODULE COMPONENT ---
const GameDayModule: React.FC<{ onBack: () => void; progress: ModuleProgress; onProgressUpdate: (progress: ModuleProgress) => void }> = ({ onBack, progress, onProgressUpdate }) => {
  const essentials = useEssentialsMode();
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
      moduleDescription="Train for your big exams the way athletes train for competition. Sleep, food, mindset, and a solid game plan -- this is your playbook for performing at your best when it counts."
      theme={theme}
      sections={sections}
      onBack={onBack}
      progress={progress}
      onProgressUpdate={onProgressUpdate}
      references={GAME_DAY_REFERENCE_LIST}
      finishButtonText="Game On"
    >
      {(activeSection) => (
        <>
          {activeSection === 0 && (
            <ReadingSection title="The Athlete Mindset." eyebrow="Step 1" icon={Target} theme={theme}>
              {essentials ? (
                <>
                  <p>Your brain uses 20% of your body's energy.<Cite n={1} /> A 3-hour exam is a marathon for your head. How you perform depends on sleep, food, and stress management, not just what you know.</p>
                  <p>Your goal: get into a Challenge State ("I have got this") and avoid a Threat State ("I am going to fail").<Cite n={2} /> The simulator below shows the difference.</p>
                </>
              ) : (
                <>
                  <p>Big exams aren't just academic tests -- they're endurance events. Your brain uses 20% of your body's energy.<Cite n={1} /> A 2-3 hour paper is basically a marathon for your head. This module is about treating yourself like an <Highlight description="The idea that you're not just studying with your mind -- your body matters too. Sleep, food, and stress management all directly affect how well your brain performs on the day." theme={theme}>Exam Athlete</Highlight>. How well you do isn't just about what you know -- it's about the state your brain is in when it's trying to remember it all.</p>
                  <p>The goal is to get yourself into a <Highlight description="That 'I've got this' feeling. When you feel prepared and energised, your body sends more blood and oxygen to your brain. You think faster and stay focused." theme={theme}>Challenge State</Highlight> ("pumped") and avoid a <Highlight description="That 'I'm going to fail' feeling. When your brain thinks the exam is too much, stress hormones take over and your thinking brain basically shuts down. That's where 'mind blanking' comes from." theme={theme}>Threat State</Highlight> ("scared").<Cite n={2} /> This isn't about positive thinking. It's about real, practical steps you can take to get your body and brain working together.</p>
                  <PersonalStory name="Aisling" role="6th Year, Limerick" junior={{ name: 'Aisling', role: '3rd Year, Limerick', children: (
                    <p>Before a big test, I used to just cram until midnight and hope for the best. I'd walk in wrecked and my mind would go blank on stuff I definitely knew. When I started treating it more like training -- sorting my sleep, eating properly, doing a warm-up routine -- it was like night and day. I wasn't any smarter, I was just less wrecked.</p>
                  ) }}>
                    <p>Before my mocks, I used to just cram until 2am and hope for the best. I'd walk into the exam wrecked and my mind would go blank on stuff I definitely knew. When I started treating exam prep more like training -- sorting my sleep, eating properly, doing a warm-up routine -- it was like night and day. I wasn't any smarter, I was just less wrecked.</p>
                  </PersonalStory>
                </>
              )}
              <ChallengeThreatSimulator />
            </ReadingSection>
          )}
           {activeSection === 1 && (
            <ReadingSection title="1 Month Out: Building Your Base." eyebrow="Step 2" icon={SlidersHorizontal} theme={theme}>
              {essentials ? (
                <p>One month out: shift your sleep schedule to match exam times. Move your alarm back 15 minutes every 3-4 days. Start eating slow-release foods like porridge and wholegrain bread.<Cite n={3} /> Use the planner below.</p>
              ) : (
                <>
                  <p>In the final month, the focus shifts from learning new stuff to locking in what you already know -- and getting your body into a good routine. Your main job right now is to get your <Highlight description="Getting your body clock in sync with exam times. If you've been going to bed at 1am and waking at 11am, you need to gradually shift that so you're sharp at 9:30am when the exam starts." theme={theme}>sleep schedule lined up with exam times</Highlight>.</p>
                  <p>Most teenagers are night owls, but exams start at 9:30 AM. You need to gradually shift your wake-up time -- not all at once, but bit by bit. You should also start eating more <Highlight description="Foods like porridge, wholegrain bread, and bananas that give you slow, steady energy instead of a sugar spike followed by a crash. Think fuel that lasts the whole exam, not just the first 20 minutes." theme={theme}>slow-release energy foods</Highlight> so your brain has steadier fuel through the morning.<Cite n={3} /></p>
                </>
              )}
              <CircadianShifter />
            </ReadingSection>
          )}
           {activeSection === 2 && (
            <ReadingSection title="The Final Week: Winding Down." eyebrow="Step 3" icon={Brain} theme={theme}>
              {essentials ? (
                <p>Do not cram the final week. Cut study volume by 40-60%. Test yourself instead of re-reading.<Cite n={4} /> Stop learning new material 3 days out. New stuff can push out old stuff you already knew.<Cite n={5} /> Use the planner below.</p>
              ) : (
                <>
                  <p>The last week before exams is where most students mess up. The instinct is to cram harder, but that's the opposite of what works. Athletes <Highlight description="Easing off in the days before a big event. Less volume, more rest. Cutting your study hours by 40-60% in the final days helps you go in fresh instead of burnt out." theme={theme}>ease off before a big event</Highlight> -- and you should too. Think of it this way: Performance = What You Know minus How Tired You Are. Cramming makes you exhausted, so even if you know loads, your brain can't access it properly.</p>
                  <p>In the final week, you do fewer hours but make those hours count -- testing yourself, not just reading over notes.<Cite n={4} /> And here's the big one: stop learning new material 3 days out. Last-minute cramming can actually cause <Highlight description="When new information messes up your ability to remember older stuff. It's why cramming the night before can make you forget things you knew perfectly well last week." theme={theme}>new stuff to push out old stuff</Highlight> you already knew.<Cite n={5} /></p>
                </>
              )}
              <TaperPlanner />
            </ReadingSection>
          )}
          {activeSection === 3 && (
            <ReadingSection title="Mental Rehearsal." eyebrow="Step 4" icon={Shield} theme={theme}>
              {essentials ? (
                <p>Do not just picture the result. Picture the process. Run a mental movie: waking up, eating, walking in, reading the paper, hitting a hard question. When you have "been there" in your head, your brain stays calm on the day.<Cite n={6} /></p>
              ) : (
                <>
                  <p>Top athletes don't just train their bodies -- they train their minds through visualization. But there's a trap. <Highlight description="Picturing the end result (e.g. opening your results envelope and seeing top grades). This can actually make you feel like you've already achieved it, which drains your motivation and can increase anxiety." theme={theme}>Just picturing the result</Highlight> (like imagining your final grades) can actually backfire.</p>
                  <p>What works is <Highlight description="Picturing the actual steps: waking up calm, walking into the hall, reading the first question, taking a breath before writing. When you've 'been there' in your head, your brain handles the real thing much better -- instead of panicking, it goes 'I know what to do here.'" theme={theme}>picturing the process</Highlight>.<Cite n={6} /> Run a "mental movie" of exam day in your head -- waking up, eating, walking in, reading the paper. When you hit a hard question on the day, your brain recognises the moment ("I've been here before") and stays calm instead of panicking.</p>
                </>
              )}
            </ReadingSection>
          )}
          {activeSection === 4 && (
            <ReadingSection title="The Day Before." eyebrow="Step 5" icon={Moon} theme={theme}>
              {essentials ? (
                <p>Stop heavy studying by 6pm. Pack your exam bag the night before. Eat a filling dinner with slow-release energy. Before bed, do a brain dump: write down everything on your mind so your brain can switch off.<Cite n={7} /></p>
              ) : (
                <>
                  <p>The 24 hours before your first exam are about keeping things calm and steady. Stop any heavy studying by 6:00 PM. The evening is for winding down. Do your <Highlight description="Pack your clear pencil case, calculator, ID, exam number, and a bottle of water the night before. Getting this sorted early means one less thing to stress about in the morning." theme={theme}>"Packing" Ritual</Highlight> early so you're not scrambling in the morning.</p>
                  <p>For dinner, go for something filling with slow-release energy -- pasta, rice, potatoes with some protein (whatever you have -- chicken, beans, eggs, anything decent). The goal is to fill up your energy stores so your brain has fuel in the morning. Before bed, do a <Highlight description="Grab a page and write down anything still bouncing around your head -- facts you're worried about, things on your mind, whatever. Getting it out of your head and onto paper helps your brain switch off so you can actually sleep." theme={theme}>"Brain Dump"</Highlight>: write down anything still buzzing around your head so your brain can switch off.<Cite n={7} /></p>
                </>
              )}
            </ReadingSection>
          )}
           {activeSection === 5 && (
            <ReadingSection title="Game Day: The Warm-Up." eyebrow="Step 6" icon={Utensils} theme={theme}>
              {northStar && (() => { const p = COMPACT_CALLOUT_PLACEMENTS.find(p => p.moduleId === 'game-day-protocol'); return p ? <NorthStarCallout northStar={northStar} variant="compact" message={p.message} /> : null; })()}
              {essentials ? (
                <p>Do not hit snooze. Drink water. Get daylight. Eat a slow-energy breakfast. Then do a quick brain warm-up: a verbal fluency drill or mental sums. This fires up your thinking brain before the exam.</p>
              ) : (
                <p>The morning of the exam is about channeling your nerves into focus. Don't hit snooze. Drink a glass of water straight away. If you can, get a few minutes of daylight (even standing by a window helps) -- it wakes your brain up properly. Eat a breakfast that gives you slow, steady energy (more on that below).</p>
              )}
              <PreExamMealBuilder />
              {!essentials && (
                <p>Just as an athlete warms up before a match, you need to warm up your brain. Passively reading over notes doesn't do much. What actually helps is a quick <Highlight description="Short brain exercises -- like listing words that start with a certain letter, or doing a few quick mental sums -- done 20-30 minutes before the exam. It gets the thinking parts of your brain warmed up and ready to go before you open the paper." theme={theme}>brain warm-up</Highlight>. It gets the right parts of your brain fired up and ready before you even open the paper.</p>
              )}
              <CognitiveWarmup />
            </ReadingSection>
          )}
           {activeSection === 6 && (
            <ReadingSection title="In The Arena: Execution." eyebrow="Step 7" icon={Zap} theme={theme}>
              {essentials ? (
                <p>Headphones in. Avoid panicked conversations. Sit down and do a Physiological Sigh: two nose sniffs, one long mouth exhale.<Cite n={8} /> Read the paper for 5 minutes before writing anything. This stops you misreading questions in a panic.</p>
              ) : (
                <p>When you arrive, put yourself in a bubble. Headphones in if you have them, or just keep to yourself -- avoid panicked conversations with other students. When you sit down, do the <Highlight description="A quick breathing trick: two sharp sniffs in through your nose, then one long, slow breath out through your mouth. It's the fastest way to calm your nerves in the moment." theme={theme}>Physiological Sigh</Highlight> (two quick sniffs in through your nose, one long breath out).<Cite n={8} /> For the first 5 minutes, don't write anything. Just read the paper and breathe. This stops you from misreading questions in a panic.</p>
              )}
            </ReadingSection>
          )}
           {activeSection === 7 && (
            <ReadingSection title="Halftime & Post-Game." eyebrow="Step 8" icon={Wind} theme={theme}>
              {essentials ? (
                <p>Between exams: eat something light, try a 10-20 minute rest or nap. After each exam: do not compare answers with anyone.<Cite n={9} /> The paper is done. Bin the mental file. Focus on the next one.</p>
              ) : (
                <>
                  <p>On days with two exams, the break between them is huge. Eat something that won't make you sleepy -- a sandwich, some fruit, whatever you can manage -- and avoid a massive heavy meal. If you can, a 10-20 minute nap or a quick <Highlight description="A guided relaxation technique you can find free on YouTube or Spotify. You lie down, close your eyes, and follow the instructions. It's not sleep, but it recharges your brain surprisingly well -- sometimes even better than a nap." theme={theme}>guided rest session (NSDR)</Highlight> is one of the best ways to recharge for the afternoon.</p>
                  <p>After each exam, one rule: <Highlight description="Don't talk about the exam you just did. Seriously. When everyone starts comparing answers, it spreads panic -- and that panic follows you into your next paper. The exam is done. Let it go." theme={theme}>don't talk about it</Highlight>.<Cite n={9} /> No comparing answers, no "what did you get for question 5?" The paper is done. Bin the mental file. Focus on the next one.</p>
                </>
              )}
              <MicroCommitment theme={theme}>
                <p>Go to your calendar (phone, wall, whatever you have). Find the date one month before your first exam. Set a reminder: "Start my game day prep." From that point on, you're not just studying -- you're training.</p>
              </MicroCommitment>
              <ToolJumpCard
                toolId="war-room"
                title="Lock in your final-stretch plan"
                description="The War Room maps your remaining time across subjects and tells you what to focus on right up to game day. The strategic side of what you just read."
                ctaLabel="Open the War Room"
              />
            </ReadingSection>
          )}
        </>
      )}
    </ModuleLayout>
  );
};
export default GameDayModule;
