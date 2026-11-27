/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
*/

import { motion } from 'framer-motion';
import { Brain,Coffee,Droplet,Leaf,Moon,Shield,SlidersHorizontal,Target,Utensils,Wind,X,Zap } from 'lucide-react';
import React,{ useEffect,useId,useState } from 'react';
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
import { AnswerGroup,AnswerLine,ExerciseRange,ExerciseSheet } from './learning/Exercise';
import { Button,TextButton } from './ui/Button';
import { ChoiceTile } from './ui/Choice';
import { AreaField,Field } from './ui/Field';

const theme = amberTheme;

// --- INTERACTIVE COMPONENTS ---
const ChallengeThreatSimulator = () => {
    const [resources, setResources] = useState(50);
    const isChallenge = resources >= 50;
    const levelId = useId();

    return (
        <ExerciseSheet title="Challenge vs. Threat State" name="ChallengeThreatSimulator">
             {/* The two bars: the exam's demands (fixed) against the student's own resources, on hairline tracks */}
             <div className="grid grid-cols-2 gap-8 items-end">
                <div>
                    <p className="ex-label">Demands (The Exam)</p>
                    <div className="h-2 w-full rounded-full mt-2" style={{ background: 'var(--ink-muted)' }} />
                </div>
                <div>
                    <p className="ex-label">Your Resources</p>
                    <div className="h-2 w-full rounded-full mt-2" style={{ background: 'var(--hairline)' }}><motion.div className="h-full rounded-full" style={{ background: 'var(--ink-primary)' }} animate={{width: `${resources}%`}} /></div>
                </div>
             </div>
             <div className="ex-slider">
                <p id={levelId} className="ex-slider-name">Resource Level:</p>
                <ExerciseRange value={resources} onChange={e => setResources(parseInt(e.target.value))} aria-labelledby={levelId} />
             </div>
             {/* The state it puts you in: a line in ink (the tick for the challenge state) */}
             <AnswerLine tone={isChallenge ? 'ok' : 'note'}>
                {isChallenge ? "CHALLENGE STATE: You feel 'pumped'. More blood and oxygen flow to your brain. Go time." : "THREAT STATE: You feel 'scared'. Your brain tightens up, thinking gets foggy. 'Mind blanking' is likely."}
             </AnswerLine>
        </ExerciseSheet>
    );
};

const CircadianShifter = () => {
    const [wakeTime, setWakeTime] = useState(9);
    const shifts = Math.ceil(((wakeTime - 7) * 60) / 15);

    return(
        <ExerciseSheet title="Sleep Schedule Shifter" sub="Enter your current weekend wake-up time to get a 4-week plan for shifting it earlier." name="CircadianShifter">
             <Field label="Current Wake-up Time" type="time" className="max-w-xs" value={`${String(Math.floor(wakeTime)).padStart(2,'0')}:${String((wakeTime % 1)*60).padStart(2,'0')}`} onChange={e => setWakeTime(parseInt(e.target.value.split(':')[0]) + parseInt(e.target.value.split(':')[1])/60)} />
             {/* The plan: words you read, under a hairline (no box) */}
             {wakeTime > 7 && (
                <div className="ex-block">
                    <p className="ex-block-title">Your Plan:</p>
                    <p className="ex-block-text">Shift your alarm back by 15 mins every <b className="text-ink-primary">3–4 days</b> for the next <b className="text-ink-primary">{shifts}</b> shifts to reach your 7:00 AM target.</p>
                </div>
             )}
        </ExerciseSheet>
    );
}

const TaperPlanner = () => {
    const [day, setDay] = useState(7);
    const dayId = useId();
    const taperData = {
        7: { volume: 80, intensity: 90, activity: 'Past Papers' },
        5: { volume: 60, intensity: 90, activity: 'Active Recall' },
        3: { volume: 40, intensity: 50, activity: 'Flashcards' },
        1: { volume: 10, intensity: 20, activity: 'Strategy Review' },
    };
    const taperKey = Object.keys(taperData).reverse().find(d => parseInt(d) >= day) || Object.keys(taperData)[0];
    const currentData = taperData[day as keyof typeof taperData] || taperData[taperKey as unknown as keyof typeof taperData];

    return (
        <ExerciseSheet title="Final Week Study Planner" sub="Move the slider to see how your study should change in the final week." name="TaperPlanner">
             <div className="ex-slider">
                <p id={dayId} className="ex-slider-name">Days Before Exam: {day}</p>
                <ExerciseRange min="1" max="7" value={day} onChange={e => setDay(parseInt(e.target.value))} aria-labelledby={dayId} />
             </div>
             {/* The two bars rise from a hairline in ink; the activity is named beside them */}
             <div className="grid grid-cols-3 gap-4 text-center">
                <div><p className="ex-label">Study Volume</p><div className="h-24 flex items-end mt-2" style={{ borderBottom: '1px solid var(--hairline)' }}><motion.div className="w-full rounded-t" style={{ background: 'var(--ink-primary)' }} animate={{height: `${currentData.volume}%`}} /></div></div>
                <div><p className="ex-label">Intensity</p><div className="h-24 flex items-end mt-2" style={{ borderBottom: '1px solid var(--hairline)' }}><motion.div className="w-full rounded-t" style={{ background: 'var(--ink-primary)' }} animate={{height: `${currentData.intensity}%`}} /></div></div>
                <div><p className="ex-label">Activity</p><div className="h-24 flex items-center justify-center mt-2 t-row text-ink-primary">{currentData.activity}</div></div>
             </div>
        </ExerciseSheet>
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

/** A food's glyph, bare, in ink-3 (no colour per kind: the kind is named in words beside it). */
const FoodIcon = ({ category, size = 'md' }: { category: string; size?: 'sm' | 'md' }) => {
  const cls = size === 'md' ? 'w-6 h-6' : 'w-4 h-4';
  if (category === 'Low-GI') return <Leaf className={`${cls} shrink-0 text-ink-muted`} />;
  if (category === 'Protein') return <Shield className={`${cls} shrink-0 text-ink-muted`} />;
  if (category.includes('High-GI')) return <Zap className={`${cls} shrink-0 text-ink-muted`} />;
  if (category === 'Caffeine') return <Coffee className={`${cls} shrink-0 text-ink-muted`} />;
  if (category === 'Hydration') return <Droplet className={`${cls} shrink-0 text-ink-muted`} />;
  return <X className={`${cls} shrink-0 text-ink-muted`} />;
};

const EnergyCurve = ({ level }: { level: 'high' | 'medium' | 'low' }) => {
  const curves = {
    high: {
      path: 'M 0 70 C 30 30, 60 25, 100 28 C 140 31, 200 30, 260 35 C 300 38, 340 40, 380 42',
      color: "var(--ink-primary)",
      label: 'Sustained energy. Your brain has steady glucose for 3+ hours. No crash.',
    },
    medium: {
      path: 'M 0 60 C 30 25, 60 30, 120 50 C 160 60, 180 35, 220 55 C 260 65, 300 45, 380 60',
      color: "var(--ink-primary)",
      label: 'Decent, but some crash risk. Consider swapping high-GI items for complex carbs.',
    },
    low: {
      path: 'M 0 70 C 20 10, 50 5, 80 15 C 110 70, 140 85, 200 88 C 240 90, 300 90, 380 92',
      color: "var(--ink-primary)",
      label: 'Sugar spike followed by a crash at ~10:30am. Your working memory will suffer mid-exam.',
    },
  };

  const c = curves[level];

  return (
    <MotionDiv
      initial={{ opacity: 0, y: 10 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.5 }}
      className="ex-block"
    >
      {/* The curve, on the sheet under a hairline and its label (no tinted box) */}
      <p className="ex-label">Energy Curve (Exam Morning)</p>
      <div className="flex items-end gap-2 t-meta">
        <span>High</span>
      </div>
      <svg viewBox="0 0 380 80" className="w-full h-20" preserveAspectRatio="none">
        <defs>
          <linearGradient id={`grad-${level}`} x1="0" y1="0" x2="0" y2="1">
            <stop offset="0%" stopColor={c.color} stopOpacity="0.12" />
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
      <div className="flex justify-between t-meta px-1">
        <span>7am</span>
        <span>9:30am</span>
        <span>11:30am</span>
        <span>1pm</span>
      </div>
      <div className="flex items-end gap-2 t-meta">
        <span>Low</span>
      </div>
      {/* What the curve means: a line in ink (the tick for sustained energy) */}
      <AnswerLine tone={level === 'high' ? 'ok' : 'note'} className="mt-2">{c.label}</AnswerLine>
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
    <ExerciseSheet title="Pre-Exam Meal Builder" sub="Build your exam morning breakfast. Your brain needs the right fuel." name="PreExamMealBuilder">
      {/* Food Grid: each food is an answer you choose (up to five); its kind is a second line, not a tinted pill;
          the order it went on the plate is a neutral ring under it */}
      <AnswerGroup kind="several" columns={2}>
        {FOODS.map((food) => {
          const isSelected = selected.includes(food.id);
          const isDisabled = !isSelected && selected.length >= 5;
          const faded = scored ? !isSelected : isDisabled;
          return (
            <ChoiceTile
              key={food.id}
              kind="several"
              tile
              chosen={isSelected}
              onClick={() => !isDisabled && toggleFood(food.id)}
              disabled={isDisabled}
              style={faded ? { opacity: 0.4 } : undefined}
              label={<span className="flex items-center gap-2"><FoodIcon category={food.category} /><span className="min-w-0">{food.name}</span></span>}
              meta={food.category}
              note={isSelected ? <span className="ex-badge">{selected.indexOf(food.id) + 1}</span> : undefined}
              noteTone="plain"
            />
          );
        })}
      </AnswerGroup>

      {/* Plate Area: the chosen foods ruled like rows (no pills) */}
      {selected.length > 0 && (
        <MotionDiv
          initial={{ opacity: 0, y: 10 }}
          animate={{ opacity: 1, y: 0 }}
          className="ex-stack"
        >
          <p className="ex-label">
            Your Plate ({selected.length}/5)
          </p>
          <div className="ex-list">
            {selectedFoods.map((food) => (
              <MotionDiv
                key={food.id}
                initial={{ scale: 0.8, opacity: 0 }}
                animate={{ scale: 1, opacity: 1 }}
                exit={{ scale: 0.8, opacity: 0 }}
              >
                <div className="flex items-center gap-2">
                  <FoodIcon category={food.category} size="sm" />
                  <span className="flex-1 min-w-0 t-body text-ink-primary">{food.name}</span>
                  {scored && (
                    <span className="ui-readout text-ink-primary">
                      {food.score >= 0 ? '+' : ''}{food.score}
                    </span>
                  )}
                  {!scored && (
                    <TextButton
                      tone="quiet"
                      onClick={(e) => {
                        e.stopPropagation();
                        toggleFood(food.id);
                      }}
                    >
                      ×
                    </TextButton>
                  )}
                </div>
              </MotionDiv>
            ))}
          </div>
        </MotionDiv>
      )}

      {/* Score Button / Results */}
      {!scored && selected.length >= 3 && (
        <MotionDiv initial={{ opacity: 0 }} animate={{ opacity: 1 }} className="ex-actions">
          <Button onClick={() => setScored(true)}>
            Score My Meal
          </Button>
        </MotionDiv>
      )}

      {!scored && selected.length < 3 && selected.length > 0 && (
        <p className="t-meta">
          Select at least 3 items to score your meal.
        </p>
      )}

      {scored && (
        <MotionDiv initial={{ opacity: 0, y: 10 }} animate={{ opacity: 1, y: 0 }} className="ex-stack">
          {/* Total: its label and the number in ink, under a hairline (no colour for good or bad) */}
          <div className="ex-result">
            <p className="ex-label">Total Score</p>
            <p className="t-number text-ink-primary">
              {totalScore >= 0 ? '+' : ''}{totalScore}
            </p>
          </div>

          <EnergyCurve level={energyLevel} />

          {/* Per-item breakdown: ruled rows, the score in the readout */}
          <div className="ex-list">
            {selectedFoods.map((food) => (
              <div key={food.id}>
                <div className="flex items-center justify-between gap-3">
                  <span className="flex items-center gap-1.5 t-body text-ink-primary">
                    <FoodIcon category={food.category} size="sm" /> {food.name}
                  </span>
                  <span className="ui-readout text-ink-primary">
                    {food.score >= 0 ? '+' : ''}{food.score}
                  </span>
                </div>
              </div>
            ))}
          </div>

          <div className="ex-actions">
            <Button onClick={reset}>
              Build Another Meal
            </Button>
          </div>
        </MotionDiv>
      )}
    </ExerciseSheet>
  );
};

const CognitiveWarmup = () => {
    const [drill, setDrill] = useState<'none'|'verbal'|'math'>('none');
    const [time, setTime] = useState(60);
    const [words, setWords] = useState('');
    const verbalId = useId();

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
             <ExerciseSheet title="Calculation Sprint" name="CognitiveWarmup">
                {/* The two sums, ruled like rows */}
                <div className="ex-list">
                    <p className="t-row text-ink-primary">1. 15 x 12 = ?</p>
                    <p className="t-row text-ink-primary">2. What is 25% of 180?</p>
                </div>
                <div className="ex-actions">
                    <TextButton tone="quiet" onClick={() => setDrill('none')}>Back</TextButton>
                </div>
             </ExerciseSheet>
        );
    }

    if(drill === 'verbal') {
        return (
            <ExerciseSheet title="Verbal Fluency Drill" sub="For 60 seconds, list as many words as you can that start with the letter 'P'." name="CognitiveWarmup" id={verbalId}>
                {/* The seconds left, as a number in ink */}
                <p className="t-number text-ink-primary">{time}</p>
                <AreaField value={words} onChange={e => setWords(e.target.value)} aria-labelledby={verbalId} disabled={time === 0} />
                <div className="ex-actions">
                    <TextButton tone="quiet" onClick={resetVerbal}>Reset</TextButton>
                </div>
            </ExerciseSheet>
        );
    }

    return (
        <ExerciseSheet title="Brain Warm-Up" sub="Pick a quick drill to get your brain warmed up and ready." name="CognitiveWarmup">
             <div className="ex-actions">
                <Button onClick={() => resetVerbal()}>Verbal Fluency</Button>
                <Button onClick={() => setDrill('math')}>Math Sprint</Button>
             </div>
        </ExerciseSheet>
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
