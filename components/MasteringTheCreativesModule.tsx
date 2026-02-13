/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
*/

import React, { useState, useEffect, useRef, useCallback } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { Key, PenTool, SlidersHorizontal, Film, Shield, Wrench } from 'lucide-react';
import { ModuleProgress } from '../types';
import { slateTheme } from '../moduleThemes';
import { Highlight, ReadingSection, MicroCommitment } from './ModuleShared';
import { ModuleLayout } from './ModuleLayout';

const theme = slateTheme;
const MotionDiv = motion.div as any;

// --- TECHNIQUE DATA ---

interface Technique {
  name: string;
  category: string;
  instruction: string;
  color: string;
  bg: string;
  border: string;
  ring: string;
  text: string;
  dot: string;
}

const techniques: Technique[] = [
  {
    name: 'Blind Contour Drawing',
    category: 'Art',
    instruction: "Without looking at your paper, draw the outline of your non-dominant hand. Don't lift your pen. Focus only on what your eyes see.",
    color: '#3b82f6',
    bg: 'bg-blue-50 dark:bg-blue-950/30',
    border: 'border-blue-200 dark:border-blue-800',
    ring: 'text-blue-500',
    text: 'text-blue-600 dark:text-blue-400',
    dot: 'bg-blue-500',
  },
  {
    name: 'Negative Space Sketch',
    category: 'Art',
    instruction: 'Look at an object near you. Instead of drawing the object, draw the space AROUND it. Fill in everything that isn\'t the object.',
    color: '#8b5cf6',
    bg: 'bg-violet-50 dark:bg-violet-950/30',
    border: 'border-violet-200 dark:border-violet-800',
    ring: 'text-violet-500',
    text: 'text-violet-600 dark:text-violet-400',
    dot: 'bg-violet-500',
  },
  {
    name: 'Melody Variation',
    category: 'Music',
    instruction: "Hum or sing 'Happy Birthday'. Now sing it again changing 3 notes. You've just composed an A1 variation \u2014 the core of melodic composition.",
    color: '#10b981',
    bg: 'bg-emerald-50 dark:bg-emerald-950/30',
    border: 'border-emerald-200 dark:border-emerald-800',
    ring: 'text-emerald-500',
    text: 'text-emerald-600 dark:text-emerald-400',
    dot: 'bg-emerald-500',
  },
  {
    name: 'Shot Composition',
    category: 'Film',
    instruction: "Frame an imaginary shot of the room you're in. Describe: camera angle (low/eye/high), shot type (close-up/mid/wide), and what emotion it creates.",
    color: '#f59e0b',
    bg: 'bg-amber-50 dark:bg-amber-950/30',
    border: 'border-amber-200 dark:border-amber-800',
    ring: 'text-amber-500',
    text: 'text-amber-600 dark:text-amber-400',
    dot: 'bg-amber-500',
  },
  {
    name: 'Texture Hunt',
    category: 'Art',
    instruction: 'Find 3 different textures within arm\'s reach. Describe each in one sentence using ONLY touch-words (rough, silky, gritty, cool, etc.).',
    color: '#f43f5e',
    bg: 'bg-rose-50 dark:bg-rose-950/30',
    border: 'border-rose-200 dark:border-rose-800',
    ring: 'text-rose-500',
    text: 'text-rose-600 dark:text-rose-400',
    dot: 'bg-rose-500',
  },
  {
    name: 'Rhythm Builder',
    category: 'Music',
    instruction: 'Tap a steady beat on your desk. Now add a syncopated off-beat with your other hand. Hold both for 30 seconds. This is rhythmic independence.',
    color: '#14b8a6',
    bg: 'bg-teal-50 dark:bg-teal-950/30',
    border: 'border-teal-200 dark:border-teal-800',
    ring: 'text-teal-500',
    text: 'text-teal-600 dark:text-teal-400',
    dot: 'bg-teal-500',
  },
  {
    name: 'Lighting Analysis',
    category: 'Film',
    instruction: 'Describe the lighting in the room right now. Is it high-key or low-key? Where are the shadows falling? What mood does it create?',
    color: '#f97316',
    bg: 'bg-orange-50 dark:bg-orange-950/30',
    border: 'border-orange-200 dark:border-orange-800',
    ring: 'text-orange-500',
    text: 'text-orange-600 dark:text-orange-400',
    dot: 'bg-orange-500',
  },
  {
    name: 'Observational Detail',
    category: 'Art',
    instruction: 'Pick one small object near you. Spend 2 minutes writing down every detail you can see \u2014 colour, shadow, reflection, texture, shape, imperfection.',
    color: '#06b6d4',
    bg: 'bg-cyan-50 dark:bg-cyan-950/30',
    border: 'border-cyan-200 dark:border-cyan-800',
    ring: 'text-cyan-500',
    text: 'text-cyan-600 dark:text-cyan-400',
    dot: 'bg-cyan-500',
  },
];

// --- DELIBERATE PRACTICE WHEEL ---

const DeliberatePracticeWheel: React.FC = () => {
  const [practiced, setPracticed] = useState<Set<number>>(new Set());
  const [phase, setPhase] = useState<'idle' | 'spinning' | 'active' | 'done'>('idle');
  const [highlightIndex, setHighlightIndex] = useState<number>(-1);
  const [selectedIndex, setSelectedIndex] = useState<number>(-1);
  const [timeLeft, setTimeLeft] = useState(120);
  const [timerFinished, setTimerFinished] = useState(false);
  const timerRef = useRef<ReturnType<typeof setInterval> | null>(null);
  const spinRef = useRef<ReturnType<typeof setTimeout> | null>(null);
  const allPracticed = practiced.size >= 8;

  // Cleanup on unmount
  useEffect(() => {
    return () => {
      if (timerRef.current) clearInterval(timerRef.current);
      if (spinRef.current) clearTimeout(spinRef.current);
    };
  }, []);

  // Timer countdown
  useEffect(() => {
    if (phase !== 'active') return;
    timerRef.current = setInterval(() => {
      setTimeLeft(prev => {
        if (prev <= 1) {
          if (timerRef.current) clearInterval(timerRef.current);
          setTimerFinished(true);
          setPhase('done');
          return 0;
        }
        return prev - 1;
      });
    }, 1000);
    return () => {
      if (timerRef.current) clearInterval(timerRef.current);
    };
  }, [phase]);

  const spin = useCallback(() => {
    if (phase === 'spinning') return;
    setTimerFinished(false);
    setPhase('spinning');

    // Pick a random target
    const target = Math.floor(Math.random() * 8);
    let current = 0;
    const totalSteps = 24 + target; // 3 full rotations + landing
    let step = 0;

    const tick = () => {
      setHighlightIndex(current % 8);
      step++;
      current++;
      if (step < totalSteps) {
        // Speed: start fast (~60ms), slow down toward end
        const delay = step < 16 ? 60 : step < 22 ? 120 : step < 26 ? 200 : 300;
        spinRef.current = setTimeout(tick, delay);
      } else {
        // Landed
        setSelectedIndex(target);
        setHighlightIndex(target);
        setTimeLeft(120);
        setPhase('active');
        setPracticed(prev => new Set(prev).add(target));
      }
    };
    tick();
  }, [phase]);

  const spinAgain = () => {
    setSelectedIndex(-1);
    setTimerFinished(false);
    setPhase('idle');
    setHighlightIndex(-1);
  };

  const formatTime = (s: number) => {
    const m = Math.floor(s / 60);
    const sec = s % 60;
    return `${m}:${sec.toString().padStart(2, '0')}`;
  };

  const timerProgress = (120 - timeLeft) / 120;
  const selected = selectedIndex >= 0 ? techniques[selectedIndex] : null;

  // SVG ring for timer
  const ringRadius = 54;
  const ringCircumference = 2 * Math.PI * ringRadius;

  return (
    <div className="my-10 p-8 md:p-12 bg-white dark:bg-zinc-800 rounded-xl border border-zinc-200 dark:border-zinc-700">
      <h4 className="font-serif text-2xl font-semibold text-zinc-800 dark:text-white text-center">
        Deliberate Practice Wheel
      </h4>
      <p className="text-center text-sm text-zinc-500 dark:text-zinc-400 mt-2 mb-8">
        Talent is a myth. Spin the wheel and practice a real technique for 2 minutes.
      </p>

      {/* Progress counter */}
      <div className="text-center mb-6">
        <span className="text-sm font-medium text-zinc-600 dark:text-zinc-300">
          {practiced.size}/8 techniques practiced
        </span>
        {allPracticed && (
          <MotionDiv
            initial={{ opacity: 0, y: 8 }}
            animate={{ opacity: 1, y: 0 }}
            className="mt-3 p-4 rounded-lg bg-emerald-50 dark:bg-emerald-950/30 border border-emerald-200 dark:border-emerald-800"
          >
            <p className="text-sm text-emerald-700 dark:text-emerald-300 font-medium">
              You've experienced deliberate practice across all creative disciplines. None of these required "talent" — just focused attention and willingness to try.
            </p>
          </MotionDiv>
        )}
      </div>

      {/* Wheel layout: 8 pills arranged around a central button */}
      <div className="relative w-72 h-72 mx-auto mb-8">
        {techniques.map((tech, i) => {
          const angle = (i / 8) * 2 * Math.PI - Math.PI / 2;
          const radius = 110;
          const cx = 144 + radius * Math.cos(angle) - 40;
          const cy = 144 + radius * Math.sin(angle) - 16;
          const isHighlighted = highlightIndex === i;
          const isPracticed = practiced.has(i);

          return (
            <MotionDiv
              key={i}
              className={`absolute flex items-center justify-center rounded-full px-3 py-1.5 text-xs font-semibold transition-all duration-150 border-2 select-none ${
                isHighlighted
                  ? 'scale-110 shadow-lg z-10'
                  : 'scale-100'
              }`}
              style={{
                left: cx,
                top: cy,
                width: 80,
                height: 32,
                backgroundColor: isHighlighted ? tech.color : isPracticed ? tech.color + '33' : 'transparent',
                borderColor: tech.color,
                color: isHighlighted ? '#fff' : isPracticed ? tech.color : tech.color,
              }}
              animate={{
                scale: isHighlighted ? 1.15 : 1,
                boxShadow: isHighlighted ? `0 0 20px ${tech.color}55` : '0 0 0px transparent',
              }}
              transition={{ duration: 0.15 }}
            >
              <span className="truncate text-center leading-tight" style={{ fontSize: '10px' }}>{tech.category}</span>
            </MotionDiv>
          );
        })}

        {/* Practiced dots ring (inner) */}
        {techniques.map((tech, i) => {
          const angle = (i / 8) * 2 * Math.PI - Math.PI / 2;
          const dotRadius = 72;
          const dx = 144 + dotRadius * Math.cos(angle) - 5;
          const dy = 144 + dotRadius * Math.sin(angle) - 5;
          return (
            <div
              key={`dot-${i}`}
              className={`absolute w-2.5 h-2.5 rounded-full transition-all duration-300 ${practiced.has(i) ? tech.dot : 'bg-zinc-200 dark:bg-zinc-600'}`}
              style={{ left: dx, top: dy }}
            />
          );
        })}

        {/* Central SPIN button */}
        <MotionDiv
          className="absolute inset-0 flex items-center justify-center"
        >
          {phase === 'idle' || phase === 'spinning' ? (
            <MotionDiv
              whileHover={phase !== 'spinning' ? { scale: 1.08 } : {}}
              whileTap={phase !== 'spinning' ? { scale: 0.95 } : {}}
            >
              <button
                onClick={spin}
                disabled={phase === 'spinning'}
                className={`w-24 h-24 rounded-full font-bold text-lg text-white shadow-xl transition-colors ${
                  phase === 'spinning'
                    ? 'bg-zinc-400 dark:bg-zinc-600 cursor-not-allowed'
                    : 'bg-zinc-800 dark:bg-white dark:text-zinc-800 hover:bg-zinc-700 dark:hover:bg-zinc-100 cursor-pointer'
                }`}
              >
                {phase === 'spinning' ? '...' : 'SPIN'}
              </button>
            </MotionDiv>
          ) : null}
        </MotionDiv>
      </div>

      {/* Selected technique exercise card */}
      <AnimatePresence mode="wait">
        {(phase === 'active' || phase === 'done') && selected && (
          <MotionDiv
            key={`exercise-${selectedIndex}`}
            initial={{ opacity: 0, y: 20, scale: 0.95 }}
            animate={{ opacity: 1, y: 0, scale: 1 }}
            exit={{ opacity: 0, y: -20, scale: 0.95 }}
            transition={{ duration: 0.4, ease: 'easeOut' }}
            className={`rounded-xl border p-6 md:p-8 ${selected.bg} ${selected.border}`}
          >
            {/* Header */}
            <div className="flex items-center gap-3 mb-4">
              <span
                className="px-3 py-1 rounded-full text-xs font-bold text-white"
                style={{ backgroundColor: selected.color }}
              >
                {selected.category}
              </span>
              <h5 className={`font-serif text-xl font-semibold ${selected.text}`}>
                {selected.name}
              </h5>
            </div>

            {/* Instruction */}
            <p className="text-zinc-700 dark:text-zinc-200 mb-6 leading-relaxed">
              {selected.instruction}
            </p>

            {/* Timer */}
            <div className="flex flex-col items-center">
              <div className="relative w-32 h-32 mb-4">
                <svg viewBox="0 0 120 120" className="w-full h-full -rotate-90">
                  {/* Background ring */}
                  <circle
                    cx="60"
                    cy="60"
                    r={ringRadius}
                    fill="none"
                    stroke="currentColor"
                    strokeWidth="6"
                    className="text-zinc-200 dark:text-zinc-600"
                  />
                  {/* Progress ring */}
                  <circle
                    cx="60"
                    cy="60"
                    r={ringRadius}
                    fill="none"
                    stroke={selected.color}
                    strokeWidth="6"
                    strokeLinecap="round"
                    strokeDasharray={ringCircumference}
                    strokeDashoffset={ringCircumference * (1 - timerProgress)}
                    style={{ transition: 'stroke-dashoffset 0.5s linear' }}
                  />
                </svg>
                {/* Timer text */}
                <div className="absolute inset-0 flex items-center justify-center">
                  <span className="text-2xl font-bold text-zinc-800 dark:text-white font-mono">
                    {formatTime(timeLeft)}
                  </span>
                </div>
              </div>

              {/* Timer status */}
              {timerFinished ? (
                <MotionDiv
                  initial={{ opacity: 0, y: 8 }}
                  animate={{ opacity: 1, y: 0 }}
                  className="text-center"
                >
                  <p className="text-lg font-semibold text-zinc-800 dark:text-white mb-2">
                    Time's up! How did that feel?
                  </p>
                  <p className="text-sm text-zinc-500 dark:text-zinc-400 mb-4">
                    That was deliberate practice. No talent required.
                  </p>
                </MotionDiv>
              ) : (
                <p className="text-sm text-zinc-500 dark:text-zinc-400 mb-4 animate-pulse">
                  Timer running — give it your full focus...
                </p>
              )}

              {/* Spin Again */}
              <button
                onClick={spinAgain}
                className="px-6 py-2.5 rounded-lg font-medium text-sm text-white transition-colors cursor-pointer"
                style={{ backgroundColor: selected.color }}
              >
                Spin Again
              </button>
            </div>
          </MotionDiv>
        )}
      </AnimatePresence>
    </div>
  );
};

// --- MODULE COMPONENT ---
const MasteringTheCreativesModule: React.FC<{ onBack: () => void; progress: ModuleProgress; onProgressUpdate: (progress: ModuleProgress) => void }> = ({ onBack, progress, onProgressUpdate }) => {
  const sections = [
    { id: 'shift-from-talent', title: 'The Talent Myth', eyebrow: '01 // The Paradigm Shift', icon: Key },
    { id: 'art-protocol', title: 'Art: The Visual Journal', eyebrow: '02 // The Art Protocol', icon: PenTool },
    { id: 'music-protocol', title: 'Music: The Algorithm of Melody', eyebrow: '03 // The Music Protocol', icon: SlidersHorizontal },
    { id: 'film-protocol', title: 'Film: The Grammar of Vision', eyebrow: '04 // The Film Protocol', icon: Film },
    { id: 'pressure-protocol', title: 'Mastering Exam Pressure', eyebrow: '05 // The Pressure Protocol', icon: Shield },
    { id: 'action-plan', title: 'Your Creative Blueprint', eyebrow: '06 // The Action Plan', icon: Wrench },
  ];

  return (
    <ModuleLayout
      moduleNumber="07"
      moduleTitle="Mastering the Creatives"
      moduleSubtitle="The Art, Music &amp; Film Guide"
      moduleDescription="A strategic deconstruction of the 'creative' subjects, revealing them as learnable skills governed by process, not just talent."
      theme={theme}
      sections={sections}
      onBack={onBack}
      progress={progress}
      onProgressUpdate={onProgressUpdate}
    >
      {(activeSection) => (
        <>
          {activeSection === 0 && (
            <ReadingSection title="The Talent Myth." eyebrow="Step 1" icon={Key} theme={theme}>
              <p>For years, you've probably heard the same old story: you're either "good at art" or you're not. You're born with "talent," or you're not. That's a myth. The Leaving Cert creative subjects--Art, Music, and Film--are not a lottery of natural ability. They're a game of skill.</p>
              <p>A deep dive into the marking schemes and examiner reports reveals the truth: top grades aren't awarded for some magical spark of genius. They're awarded for mastering a process. High performance is the result of <Highlight description="Focused, strategic practice that pushes you just beyond your current comfort zone. It's about working on your weaknesses, not just repeating what you're good at." theme={theme}>deliberate practice</Highlight>, understanding the technical rules of the game, and mastering <Highlight description="Working in cycles of creating, getting feedback, and refining. It's about treating your work as a draft that can always be improved, not a one-shot masterpiece." theme={theme}>iterative processes</Highlight>. This module is your playbook for learning these skills.</p>
              <DeliberatePracticeWheel />
            </ReadingSection>
          )}
           {activeSection === 1 && (
            <ReadingSection title="Art: The Visual Journal." eyebrow="Step 2" icon={PenTool} theme={theme}>
              <p>The new Art course has one core message: your process is as important as your final product. The <Highlight description="Formerly the sketchbook, this is now the 50% coursework component. It's the documented 'thinking process' behind your final piece." theme={theme}>Visual Journal</Highlight> is not a gallery of finished drawings; it's a messy laboratory of thought. A high-scoring journal shows your journey from an initial idea to a final piece.</p>
              <p>Kickstart your project with mind maps that go beyond words, using textures and sensory details. Master observational drawing not by "copying," but by tricking your brain with techniques like drawing upside down (<Highlight description="An observational drawing exercise where you draw from an upside-down reference photo, forcing your brain to see shapes and lines instead of recognizable objects." theme={theme}>Inversion</Highlight>) or drawing the space *around* an object (<Highlight description="An exercise where you focus on drawing the empty shapes between and around objects, which dramatically improves your sense of proportion." theme={theme}>Negative Space</Highlight>).</p>
               <MicroCommitment theme={theme}><p>Take any object on your desk. For just two minutes, try to draw it without looking at the paper, keeping your eyes locked on the object. This is 'Blind Contour' drawing. It feels weird, but it's a powerful way to train your eyes to truly see.</p></MicroCommitment>
            </ReadingSection>
          )}
          {activeSection === 2 && (
            <ReadingSection title="Music: The Algorithm of Melody." eyebrow="Step 3" icon={SlidersHorizontal} theme={theme}>
              <p>The 16-bar melody question is not a test of your inner Mozart; it's a structural engineering problem. You can get full marks by treating it like a puzzle with clear rules. Before you write a single note, run your "pre-flight check": What's the Key Signature? The Time Signature? What's the instrument's range?</p>
              <p>The most reliable structure is the A-A1-B-A2 formula. <strong>A</strong> is given. <strong>A1</strong> is a response that starts the same but ends differently, usually with a <Highlight description="The process of changing from one key to another. A mandatory part of the melody composition question." theme={theme}>modulation</Highlight> to a new key. <strong>B</strong> is the contrast--go higher, change the rhythm. <strong>A2</strong> is the return home, resolving firmly back in the original key. It's an algorithm, not a whim.</p>
            </ReadingSection>
          )}
           {activeSection === 3 && (
            <ReadingSection title="Film: The Grammar of Vision." eyebrow="Step 4" icon={Film} theme={theme}>
              <p>Film is not just a recorded story; it's a language constructed through technical choices. A H1 student doesn't just describe the plot; they analyze the *form*. How did the director use a <Highlight description="A camera shot where the camera looks up at the subject, making them seem powerful or threatening." theme={theme}>Low Angle Shot</Highlight> to make the villain seem powerful? How did they use <Highlight description="High-contrast lighting with deep shadows, often used in horror and noir to create mystery and danger." theme={theme}>Low-Key Lighting (Chiaroscuro)</Highlight> to create a sense of mystery?</p>
              <p>For the Comparative Study, you must analyze these technical choices as part of the General Vision & Viewpoint or Cultural Context. In *Blade Runner*, the constant rain and "Venetian blind" shadows aren't just for atmosphere; they're direct quotes from 1940s <Highlight description="A cinematic style known for its dark themes, cynical characters, and high-contrast, black-and-white visuals." theme={theme}>Film Noir</Highlight>, creating a feeling of paranoia and fractured identity.</p>
            </ReadingSection>
          )}
           {activeSection === 4 && (
            <ReadingSection title="Mastering Exam Pressure." eyebrow="Step 5" icon={Shield} theme={theme}>
              <p>Performance anxiety is the primary enemy in all creative subjects, from the Music practical to the Art deadline. It's a physiological response to perceived social judgment. Your brain releases adrenaline, causing trembling and shallow breathing. The key is to manage the biology, not just the thoughts.</p>
              <p>Use <Highlight description="A breathing technique (Inhale 4s, Hold 4s, Exhale 4s, Hold 4s) that activates the body's 'rest and digest' system to counteract the adrenaline rush." theme={theme}>Box Breathing</Highlight> to calm your nervous system. Reframe the exam from a test of "correctness" to a "communication of emotion." And most importantly, use <Highlight description="Practicing under exam-like conditions (e.g., performing for a mock examiner) to desensitize your brain to the context triggers of the real event." theme={theme}>Simulation Training</Highlight>. The more you expose your brain to the pressure in a safe environment, the less it will panic on the day.</p>
            </ReadingSection>
          )}
           {activeSection === 5 && (
            <ReadingSection title="Your Creative Blueprint." eyebrow="Step 6" icon={Wrench} theme={theme}>
              <p>You now have the master key. "Talent" is a myth. Success in creative subjects is a skill built through deliberate practice and strategic thinking. By mastering the process of the Visual Journal, the algorithm of melody, the grammar of film, and the psychology of performance, you can engineer your own success.</p>
              <MicroCommitment theme={theme}>
                <p>Pick ONE technique from this module. Just one. Whether it's a 'Blind Contour' drawing, analyzing one movie scene for lighting, or trying Box Breathing for one minute. Commit to trying it this week. You've just taken your first step to becoming a creative master.</p>
              </MicroCommitment>
            </ReadingSection>
          )}
        </>
      )}
    </ModuleLayout>
  );
};
export default MasteringTheCreativesModule;
