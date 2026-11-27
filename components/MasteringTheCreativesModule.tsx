/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
*/

import React, { useState, useEffect, useRef, useCallback } from 'react';
import { AnimatePresence } from 'framer-motion';
import { MotionDiv } from './Motion';
import { Key, PenTool, SlidersHorizontal, Film, Shield, Wrench } from 'lucide-react';
import { type ModuleProgress } from '../types';
import { slateTheme } from '../moduleThemes';
import { Highlight, ReadingSection, MicroCommitment, PersonalStory } from './ModuleShared';
import { ModuleLayout } from './ModuleLayout';
import { useEssentialsMode } from '../hooks/useEssentialsMode';
import { AnswerLine, ExercisePart, ExerciseSheet } from './learning/Exercise';
import { Button } from './ui/Button';

const theme = slateTheme;

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
    <ExerciseSheet
      title={<>
        Deliberate Practice Wheel
      </>}
      sub={<>
        You don’t need to be naturally gifted — the marking scheme rewards process. Spin the wheel and practice a real technique for 2 minutes.
      </>}
      name="DeliberatePracticeWheel"
    >
      {/* Progress counter: a count in the readout; once all are practised, a line in ink with the tick */}
      <div className="ex-stack">
        <p className="ex-count ui-readout">
          {practiced.size}/8 techniques practiced
        </p>
        {allPracticed && (
          <MotionDiv
            initial={{ opacity: 0, y: 8 }}
            animate={{ opacity: 1, y: 0 }}
          >
            <AnswerLine>
              You've experienced deliberate practice across all creative disciplines. None of these required "talent" — just focused attention and willingness to try.
            </AnswerLine>
          </MotionDiv>
        )}
      </div>

      {/* Wheel layout: 8 labels arranged around a central button (the wheel's own drawing, in ink: the
          landing spot has an ink outline, practised ones are ink and the rest ink-3; practised dots are green) */}
      <div className="relative w-72 h-72 mx-auto">
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
              className={`absolute flex items-center justify-center px-3 py-1.5 t-label transition-colors duration-150 select-none ${
                isHighlighted
                  ? 'z-10'
                  : ''
              }`}
              style={{
                left: cx,
                top: cy,
                width: 80,
                height: 32,
                borderRadius: 'var(--r-ctl)',
                border: `1.5px solid ${isHighlighted ? 'var(--ink-primary)' : 'transparent'}`,
                backgroundColor: 'var(--surface-paper)',
                color: isHighlighted || isPracticed ? 'var(--ink-primary)' : 'var(--ink-muted)',
              }}
              animate={{
                scale: isHighlighted ? 1.15 : 1,
              }}
              transition={{ duration: 0.15 }}
            >
              <span className="truncate text-center">{tech.category}</span>
            </MotionDiv>
          );
        })}

        {/* Practiced dots ring (inner) */}
        {techniques.map((_, i) => {
          const angle = (i / 8) * 2 * Math.PI - Math.PI / 2;
          const dotRadius = 72;
          const dx = 144 + dotRadius * Math.cos(angle) - 5;
          const dy = 144 + dotRadius * Math.sin(angle) - 5;
          return (
            <div
              key={`dot-${i}`}
              className="absolute w-2.5 h-2.5 rounded-full transition-all duration-300"
              style={{
                left: dx,
                top: dy,
                ...(practiced.has(i)
                  ? { backgroundColor: 'var(--success-hex)' }
                  : { border: '1.5px solid var(--outline-soft)' }),
              }}
            />
          );
        })}

        {/* Central SPIN button */}
        <MotionDiv
          className="absolute inset-0 flex items-center justify-center"
        >
          {phase === 'idle' || phase === 'spinning' ? (
            <Button
              onClick={spin}
              {...{ disabled: phase === 'spinning' }}
              className="disabled:opacity-40"
            >
              {phase === 'spinning' ? '...' : 'SPIN'}
            </Button>
          ) : null}
        </MotionDiv>
      </div>

      {/* Selected technique: the exercise the wheel landed on, under a hairline with its own label and
          title (no tinted card, no coloured pill) */}
      <AnimatePresence mode="wait">
        {(phase === 'active' || phase === 'done') && selected && (
          <MotionDiv
            key={`exercise-${selectedIndex}`}
            initial={{ opacity: 0, y: 20, scale: 0.95 }}
            animate={{ opacity: 1, y: 0, scale: 1 }}
            exit={{ opacity: 0, y: -20, scale: 0.95 }}
            transition={{ duration: 0.4, ease: 'easeOut' }}
          >
            <ExercisePart label={selected.category} title={selected.name} sub={selected.instruction} level={5}>
              {/* Timer: the ring in ink on a hairline track */}
              <div className="ex-figure">
                <div className="relative w-32 h-32">
                  <svg viewBox="0 0 120 120" className="w-full h-full -rotate-90">
                    {/* Background ring */}
                    <circle
                      cx="60"
                      cy="60"
                      r={ringRadius}
                      fill="none"
                      stroke="var(--hairline)"
                      strokeWidth="6"
                    />
                    {/* Progress ring */}
                    <circle
                      cx="60"
                      cy="60"
                      r={ringRadius}
                      fill="none"
                      stroke="var(--ink-primary)"
                      strokeWidth="6"
                      strokeLinecap="round"
                      strokeDasharray={ringCircumference}
                      strokeDashoffset={ringCircumference * (1 - timerProgress)}
                      style={{ transition: 'stroke-dashoffset 0.5s linear' }}
                    />
                  </svg>
                  {/* Timer text */}
                  <div className="absolute inset-0 flex items-center justify-center">
                    <span className="ui-readout text-ink-primary" style={{ fontSize: 24, lineHeight: '28px' }}>
                      {formatTime(timeLeft)}
                    </span>
                  </div>
                </div>
              </div>

              {/* Timer status */}
              {timerFinished ? (
                <MotionDiv
                  initial={{ opacity: 0, y: 8 }}
                  animate={{ opacity: 1, y: 0 }}
                >
                  <AnswerLine>
                    <b>
                      Time's up! How did that feel?
                    </b>{' '}
                    That was deliberate practice. No talent required.
                  </AnswerLine>
                </MotionDiv>
              ) : (
                <p className="t-sub animate-pulse">
                  Timer running — give it your full focus...
                </p>
              )}

              {/* Spin Again */}
              <div className="ex-actions">
                <Button onClick={spinAgain}>
                  Spin Again
                </Button>
              </div>
            </ExercisePart>
          </MotionDiv>
        )}
      </AnimatePresence>
    </ExerciseSheet>
  );
};

// --- MODULE COMPONENT ---
const MasteringTheCreativesModule: React.FC<{ onBack: () => void; progress: ModuleProgress; onProgressUpdate: (progress: ModuleProgress) => void }> = ({ onBack, progress, onProgressUpdate }) => {
  const essentials = useEssentialsMode();
  const sections = [
    { id: 'shift-from-talent', title: 'The Talent Myth', eyebrow: '01 // Mindset Reset', icon: Key },
    { id: 'art-protocol', title: 'Art: The Visual Journal', eyebrow: '02 // Art', icon: PenTool },
    { id: 'music-protocol', title: 'Music: Writing a Melody', eyebrow: '03 // Music', icon: SlidersHorizontal },
    { id: 'film-protocol', title: 'Film: Reading the Screen', eyebrow: '04 // Film', icon: Film },
    { id: 'pressure-protocol', title: 'Handling Exam Nerves', eyebrow: '05 // Exam Day', icon: Shield },
    { id: 'action-plan', title: 'Your Creative Game Plan', eyebrow: '06 // Next Steps', icon: Wrench },
  ];

  return (
    <ModuleLayout
      moduleNumber="07"
      moduleTitle="Mastering the Creatives"
      moduleSubtitle="Your Art, Music & Film Playbook"
      moduleDescription="Think you need 'natural talent' for the creatives? Think again. This module breaks it all down into skills you can learn step by step."
      theme={theme}
      sections={sections}
      onBack={onBack}
      progress={progress}
      onProgressUpdate={onProgressUpdate}
      finishButtonText="Create with Confidence"
    >
      {(activeSection) => (
        <>
          {activeSection === 0 && (
            <ReadingSection title="The Talent Myth." eyebrow="Step 1" icon={Key} theme={theme}>
              {essentials ? (
                <>
                  <p>Art, Music, and Film are skills, not talents. The marking scheme rewards process, not genius. Focus on <Highlight description="Practising with focus on the bits you find hard, not just repeating what you're already good at. It's how you actually improve." theme={theme}>deliberate practice</Highlight> and <Highlight description="Creating something, getting feedback, improving it, and repeating. Think of every piece of work as a draft you can make better." theme={theme}>working in drafts</Highlight>. Create, improve, refine, repeat.</p>
                </>
              ) : (
                <>
                  <p>You've probably heard it a hundred times: "She's just naturally gifted at art" or "He was born musical." Here's the truth -- that's nonsense. Art, Music, and Film in the Leaving Cert are not about being born with some special gift. They're skills, and you can get good at them the same way you'd get good at anything else: by learning the rules and practising smart.</p>
                  <p>If you look at the marking schemes, the examiners aren't giving H1s for mysterious "genius." They reward students who show a clear process. That means <Highlight description="Practising with focus on the bits you find hard, not just repeating what you're already good at. It's how you actually improve." theme={theme}>deliberate practice</Highlight> -- pushing yourself on the stuff you're weakest at -- and <Highlight description="Creating something, getting feedback, improving it, and repeating. Think of every piece of work as a draft you can make better." theme={theme}>working in drafts</Highlight>, where you create, improve, and refine. This module is your step-by-step guide to doing exactly that.</p>
                  <PersonalStory name="Clodagh" role="6th Year, Ballyfermot">
                    <p>I genuinely thought I was terrible at Art. Like, I couldn't even draw a straight line. But when I stopped trying to make everything look perfect and started focusing on the process -- experimenting, messing up, trying again -- my teacher said my Visual Journal was one of the strongest in the class. I got a H2 and I still can't draw a straight line. Turns out that's not what they're looking for.</p>
                  </PersonalStory>
                </>
              )}
              <DeliberatePracticeWheel />
            </ReadingSection>
          )}
           {activeSection === 1 && (
            <ReadingSection title="Art: The Visual Journal." eyebrow="Step 2" icon={PenTool} theme={theme}>
              {essentials ? (
                <>
                  <p>Your <Highlight description="This used to be called your sketchbook. It's now worth 50% of your mark. It shows the examiner how you developed your ideas from start to finish." theme={theme}>Visual Journal</Highlight> is worth 50% of your mark. It should show your thinking journey, not perfect drawings. Include experiments, dead ends, and breakthroughs.</p>
                  <p>Try <Highlight description="When you draw from a photo turned upside down, your brain stops seeing 'a face' or 'a hand' and starts seeing actual shapes and lines. It massively improves your drawing." theme={theme}>Inversion</Highlight> (drawing from upside-down photos) or <Highlight description="Instead of drawing the thing, you draw the gaps around it. It sounds weird but it really helps you get proportions right." theme={theme}>Negative Space</Highlight> sketching. Both train your eyes to really see.</p>
                </>
              ) : (
                <>
                  <p>Here's the big thing about the new Art course: your process matters just as much as your final piece. The <Highlight description="This used to be called your sketchbook. It's now worth 50% of your mark. It shows the examiner how you developed your ideas from start to finish." theme={theme}>Visual Journal</Highlight> isn't supposed to be a collection of perfect drawings. It's supposed to be messy -- full of experiments, ideas, dead ends, and breakthroughs. A high-scoring journal shows your thinking journey, not just pretty pictures.</p>
                  <p>Start your project with mind maps that use images and textures, not just words. For observational drawing, don't just try to "copy" what you see -- trick your brain into really looking. Try drawing from an upside-down photo (<Highlight description="When you draw from a photo turned upside down, your brain stops seeing 'a face' or 'a hand' and starts seeing actual shapes and lines. It massively improves your drawing." theme={theme}>Inversion</Highlight>) or sketching the empty space around an object instead of the object itself (<Highlight description="Instead of drawing the thing, you draw the gaps around it. It sounds weird but it really helps you get proportions right." theme={theme}>Negative Space</Highlight>). You don't need fancy supplies -- a pencil, a biro, even a phone camera for reference photos all work perfectly.</p>
                </>
              )}
              <MicroCommitment theme={theme}><p>Take any object on your desk. For just two minutes, try to draw it without looking at the paper, keeping your eyes locked on the object. This is 'Blind Contour' drawing. It feels weird, but it's a powerful way to train your eyes to truly see.</p></MicroCommitment>
            </ReadingSection>
          )}
          {activeSection === 2 && (
            <ReadingSection title="Music: Writing a Melody." eyebrow="Step 3" icon={SlidersHorizontal} theme={theme}>
              {essentials ? (
                <>
                  <p>The 16-bar melody is a puzzle with clear rules. Check key, time signature, and instrument range before writing anything.</p>
                  <p>Use the A-A1-B-A2 structure. A is given. A1 varies the ending, moving to a <Highlight description="This just means changing key -- like shifting the 'home base' of your melody. It's a required part of the composition question." theme={theme}>new key</Highlight>. B creates contrast. A2 returns home. It's a formula, not a guessing game.</p>
                </>
              ) : (
                <>
                  <p>The 16-bar melody question isn't about being the next Mozart -- it's more like a puzzle with clear rules. You can score full marks by following a formula. Before you write a single note, check the basics: What key is it in? What time signature? What instrument are you writing for, and what notes can it play?</p>
                  <p>The most reliable structure is A-A1-B-A2. <strong>A</strong> is the opening phrase (it's given to you). <strong>A1</strong> starts the same but ends differently, usually moving into a <Highlight description="This just means changing key -- like shifting the 'home base' of your melody. It's a required part of the composition question." theme={theme}>new key</Highlight>. <strong>B</strong> is where you mix things up -- go higher, change the rhythm, create contrast. <strong>A2</strong> brings it all home, landing back in the original key. Think of it like a story: setup, variation, surprise, resolution. It's a formula, not a guessing game.</p>
                </>
              )}
            </ReadingSection>
          )}
           {activeSection === 3 && (
            <ReadingSection title="Film: Reading the Screen." eyebrow="Step 4" icon={Film} theme={theme}>
              {essentials ? (
                <>
                  <p>Every shot is a deliberate choice. Explain how the director tells the story visually. Why use a <Highlight description="The camera looks up at a character, which makes them look powerful, intimidating, or important." theme={theme}>Low Angle Shot</Highlight>? Why use <Highlight description="Dark, moody lighting with strong shadows. Think horror films or detective movies -- it creates tension and mystery." theme={theme}>Low-Key Lighting</Highlight>?</p>
                  <p>In the Comparative Study, connect visual choices to themes. Recognise styles like <Highlight description="A style of film from the 1940s known for dark, shadowy visuals and cynical characters. Directors still borrow from it today." theme={theme}>Film Noir</Highlight>. Spotting these connections is what earns top marks.</p>
                </>
              ) : (
                <>
                  <p>Film isn't just a story on a screen -- every shot is a deliberate choice by the director. To get a H1, you can't just talk about the plot. You need to explain <em>how</em> the director tells the story visually. Why did they use a <Highlight description="The camera looks up at a character, which makes them look powerful, intimidating, or important." theme={theme}>Low Angle Shot</Highlight> to make the villain look scary? Why is the lighting dark and full of shadows (<Highlight description="Dark, moody lighting with strong shadows. Think horror films or detective movies -- it creates tension and mystery." theme={theme}>Low-Key Lighting</Highlight>) in that particular scene?</p>
                  <p>In the Comparative Study, you need to connect these visual choices to themes like General Vision & Viewpoint or Cultural Context. For example, in <em>Blade Runner</em>, the constant rain and shadow patterns aren't random -- they're borrowed from the style of old 1940s detective films called <Highlight description="A style of film from the 1940s known for dark, shadowy visuals and cynical characters. Directors still borrow from it today." theme={theme}>Film Noir</Highlight>, and they create a mood of paranoia and confusion. Spotting these connections is what separates a solid answer from a great one.</p>
                </>
              )}
            </ReadingSection>
          )}
           {activeSection === 4 && (
            <ReadingSection title="Handling Exam Nerves." eyebrow="Step 5" icon={Shield} theme={theme}>
              {essentials ? (
                <p>Use <Highlight description="Breathe in for 4 seconds, hold for 4, breathe out for 4, hold for 4. It sounds simple but it genuinely calms your body down when you're stressed." theme={theme}>Box Breathing</Highlight> before exams. Think "I'm showing what I've learned." Do <Highlight description="Practise under exam-like conditions -- play your piece for your family, do a timed drawing, present to a friend. The more you rehearse the pressure, the less scary the real thing feels." theme={theme}>mock run-throughs</Highlight> at home. The more you practise the pressure, the less scary it becomes.</p>
              ) : (
                <>
                  <p>Nerves are the biggest enemy in creative subjects -- whether it's your Music practical, an Art deadline, or a Film exam. When you're anxious, your body goes into fight-or-flight mode: your hands shake, your breathing gets shallow, and your brain feels foggy. The good news? You can learn to manage this, and it gets easier with practice.</p>
                  <p>Try <Highlight description="Breathe in for 4 seconds, hold for 4, breathe out for 4, hold for 4. It sounds simple but it genuinely calms your body down when you're stressed." theme={theme}>Box Breathing</Highlight> to settle your nerves before a performance or exam. Instead of thinking "I have to get this right," try thinking "I'm showing them what I've learned." And the best trick of all? <Highlight description="Practise under exam-like conditions -- play your piece for your family, do a timed drawing, present to a friend. The more you rehearse the pressure, the less scary the real thing feels." theme={theme}>Mock run-throughs</Highlight>. Play your piece for your family. Do a timed sketch. Present your Film essay to a friend. The more you rehearse the pressure, the less your body panics on the day.</p>
                </>
              )}
            </ReadingSection>
          )}
           {activeSection === 5 && (
            <ReadingSection title="Your Creative Game Plan." eyebrow="Step 6" icon={Wrench} theme={theme}>
              {essentials ? (
                <p>You don’t need to be naturally gifted — the marking scheme rewards process. You now know the Visual Journal, melody structure, film analysis, and exam nerves management. Pick one thing and do it this week.</p>
              ) : (
                <p>Here's the bottom line: "talent" is a myth. Doing well in Art, Music, and Film comes down to learning the process, practising with purpose, and not being afraid to make mistakes along the way. You now know how the Visual Journal works, how to structure a melody, how to read a film like an examiner, and how to handle your nerves. That's a serious toolkit.</p>
              )}
              <MicroCommitment theme={theme}>
                <p>Pick ONE thing from this module. Just one. Maybe it's a Blind Contour drawing, or analysing the lighting in one scene of a film you like, or trying Box Breathing for one minute before bed. Commit to doing it this week. That's it -- one small step, and you're already on your way.</p>
              </MicroCommitment>
            </ReadingSection>
          )}
        </>
      )}
    </ModuleLayout>
  );
};
export default MasteringTheCreativesModule;
