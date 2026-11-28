/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
*/

import { AnimatePresence,motion } from 'framer-motion';
import {
AlertTriangle,Lightbulb,ToggleRight,
Wrench,
ZapOff
} from 'lucide-react';
import React,{ useCallback,useEffect,useRef,useState } from 'react';
import { SCIENCE_OF_MISTAKES_REFERENCE_LIST } from '../data/references/scienceOfMistakes';
import { useEssentialsMode } from '../hooks/useEssentialsMode';
import { redTheme } from '../moduleThemes';
import { type ModuleProgress } from '../types';
import { ModuleLayout } from './ModuleLayout';
import { Cite } from './ModuleReferences';
import { Highlight,MicroCommitment,PersonalStory,ReadingSection } from './ModuleShared';
import { MotionDiv } from './Motion';
import { AnswerGroup,AnswerLine,ExerciseLabel,ExerciseSheet } from './learning/Exercise';
import { Button,TextButton } from './ui/Button';
import { ChoiceTile } from './ui/Choice';

const theme = redTheme;

// --- INTERACTIVE COMPONENTS ---
const BrainSignalVisualizer = () => {
    const [active, setActive] = useState(false);
    return(
        <ExerciseSheet title="The Brain's Two Signals" sub="When you make a mistake, your brain sends two distinct signals in less than half a second." name="BrainSignalVisualizer">
             {/* The two signals, drawn in ink on the sheet */}
             <div className="ex-figure">
             <div className="w-full max-w-lg mx-auto h-32 relative">
                <svg viewBox="0 0 300 100" className="w-full h-full absolute inset-0">
                    <path d="M0 50 L 300 50" stroke="var(--outline-soft)" strokeWidth="1" />
                    <AnimatePresence>
                    {active && <>
                        <motion.path initial={{pathLength:0}} animate={{pathLength:1}} transition={{duration:0.2, delay: 0.1}} d="M 50 50 C 60 50 65 20 75 20 S 90 50 100 50" stroke="var(--ink-primary)" strokeWidth="2" fill="none" />
                        <motion.path initial={{pathLength:0}} animate={{pathLength:1}} transition={{duration:0.5, delay: 0.3}} d="M 150 50 C 160 50 175 80 190 80 S 210 50 220 50" stroke="var(--ink-primary)" strokeWidth="2" fill="none" />
                    </>}
                    </AnimatePresence>
                </svg>
                {active && <>
                    <motion.div initial={{opacity:0}} animate={{opacity:1, transition:{delay:0.2}}} className="absolute top-0 left-[75px] -translate-x-1/2 text-center text-xs">
                        <p className="font-semibold text-ink-primary">ERN Signal</p>
                        <p className="text-ink-muted">The "Alarm"</p>
                    </motion.div>
                    <motion.div initial={{opacity:0}} animate={{opacity:1, transition:{delay:0.5}}} className="absolute bottom-0 left-[190px] -translate-x-1/2 text-center text-xs">
                        <p className="font-semibold text-ink-primary">Pe Signal</p>
                        <p className="text-ink-muted">The "Analysis"</p>
                    </motion.div>
                </>}
             </div>
             </div>
             <div className="ex-actions">
                <Button onClick={() => setActive(!active)}>{active ? "Reset" : "Make a Mistake"}</Button>
             </div>
        </ExerciseSheet>
    );
};

// --- AMYGDALA HIJACK SIMULATOR ---
const AmygdalaHijackSimulator = () => {
  const [stressLevel, setStressLevel] = useState(0);
  const [scenario, setScenario] = useState<string | null>(null);
  const [isAnimating, setIsAnimating] = useState(false);
  const [recoveryActive, setRecoveryActive] = useState<string | null>(null);
  const [hijackLabel, setHijackLabel] = useState(false);
  const [balanced, setBalanced] = useState(false);

  // Box breathing state
  const [breathPhase, setBreathPhase] = useState(0); // 0-3: inhale, hold, exhale, hold
  const [breathCount, setBreathCount] = useState(0);
  const breathLabels = ['Breathe In...', 'Hold...', 'Breathe Out...', 'Hold...'];

  // Grounding state
  const [groundingStep, setGroundingStep] = useState(0);
  const groundingSenses = [
    { count: 5, sense: 'things you can SEE' },
    { count: 4, sense: 'things you can HEAR' },
    { count: 3, sense: 'things you can TOUCH' },
    { count: 2, sense: 'things you can SMELL' },
    { count: 1, sense: 'thing you can TASTE' },
  ];
  const [groundingClicks, setGroundingClicks] = useState(0);

  // Reframe state
  const [reframeStep, setReframeStep] = useState(0);
  const reframes = [
    { threat: '"I\'m going to fail this exam."', reframe: '"This is a challenge, not a catastrophe."' },
    { threat: '"Everyone else knows this."', reframe: '"I\'ve prepared. I can work through this."' },
    { threat: '"One mistake means I\'ve blown it."', reframe: '"One question doesn\'t define the whole exam."' },
  ];

  const stressTargets: Record<string, number> = {
    low: 0.3,
    medium: 0.6,
    high: 1.0,
  };

  const stressIntervalRef = useRef<ReturnType<typeof setInterval> | null>(null);

  const animateStress = useCallback((target: number) => {
    // Clear any previous stress animation interval
    if (stressIntervalRef.current) {
      clearInterval(stressIntervalRef.current);
      stressIntervalRef.current = null;
    }

    setIsAnimating(true);
    setBalanced(false);
    setHijackLabel(false);
    setRecoveryActive(null);
    setBreathPhase(0);
    setBreathCount(0);
    setGroundingStep(0);
    setGroundingClicks(0);
    setReframeStep(0);

    let current = 0;
    const step = target / 20;
    stressIntervalRef.current = setInterval(() => {
      current += step;
      if (current >= target) {
        current = target;
        if (stressIntervalRef.current) {
          clearInterval(stressIntervalRef.current);
          stressIntervalRef.current = null;
        }
        setIsAnimating(false);
        if (target >= 0.7) {
          setHijackLabel(true);
        }
      }
      setStressLevel(current);
    }, 50);
  }, []);

  // Clean up stress animation interval on unmount
  useEffect(() => {
    return () => {
      if (stressIntervalRef.current) {
        clearInterval(stressIntervalRef.current);
      }
    };
  }, []);

  const handleScenario = (level: string) => {
    if (isAnimating) return;
    setScenario(level);
    animateStress(stressTargets[level]);
  };

  const reduceStress = useCallback((amount: number) => {
    setStressLevel(prev => {
      const next = Math.max(0, prev - amount);
      if (next <= 0.05) {
        setBalanced(true);
        setHijackLabel(false);
        setRecoveryActive(null);
      }
      return next;
    });
  }, []);

  // Keep a ref to the current stressLevel so the breathing interval
  // doesn't need stressLevel in its dependency array (which would
  // tear down and recreate the interval on every stress change).
  const stressLevelRef = useRef(stressLevel);
  useEffect(() => {
    stressLevelRef.current = stressLevel;
  }, [stressLevel]);

  // Box breathing effect
  useEffect(() => {
    if (recoveryActive !== 'breathing') return;
    const interval = setInterval(() => {
      setBreathPhase(prev => {
        const next = (prev + 1) % 4;
        if (next === 0) {
          setBreathCount(c => {
            const newCount = c + 1;
            if (newCount >= 3) {
              reduceStress(stressLevelRef.current);
              return 0;
            }
            reduceStress(stressLevelRef.current * 0.3);
            return newCount;
          });
        }
        return next;
      });
    }, 1200);
    return () => clearInterval(interval);
  }, [recoveryActive, reduceStress]);

  // Grounding clicks
  const handleGroundingClick = () => {
    const needed = groundingSenses[groundingStep].count;
    const nextClicks = groundingClicks + 1;
    if (nextClicks >= needed) {
      reduceStress(stressLevel * 0.2);
      if (groundingStep >= 4) {
        reduceStress(stressLevel);
      } else {
        setGroundingStep(prev => prev + 1);
        setGroundingClicks(0);
      }
    } else {
      setGroundingClicks(nextClicks);
    }
  };

  // Reframe clicks
  const handleReframe = () => {
    reduceStress(stressLevel * 0.35);
    if (reframeStep >= 2) {
      reduceStress(stressLevel);
    } else {
      setReframeStep(prev => prev + 1);
    }
  };

  const handleReset = () => {
    setStressLevel(0);
    setScenario(null);
    setIsAnimating(false);
    setRecoveryActive(null);
    setHijackLabel(false);
    setBalanced(false);
    setBreathPhase(0);
    setBreathCount(0);
    setGroundingStep(0);
    setGroundingClicks(0);
    setReframeStep(0);
  };

  // Derived visual values
  const _pfcOpacity = Math.max(0.15, 1 - stressLevel * 0.85);
  const _amygdalaGlow = stressLevel;
  const _connectionOpacity = Math.max(0.1, 1 - stressLevel * 0.9);
  const _connectionWidth = Math.max(1, 4 - stressLevel * 3);
  const cortisolHeight = stressLevel * 100;



  return <ExerciseSheet title="Amygdala Hijack Simulator" sub="See how stress hijacks your brain — then use recovery techniques to take control back." name="AmygdalaHijackSimulator">

      {/* Two-panel brain dashboard: the two parts of the brain laid on the sheet under a hairline (no boxes) */}
      <div className="grid grid-cols-1 sm:grid-cols-[1fr_auto_1fr] gap-4 sm:gap-0 items-stretch">
        {/* Prefrontal Cortex */}
        <div
          className="flex flex-col gap-1 pt-3 transition-all duration-500"
          style={{
            borderTop: '1px solid var(--hairline)',
            opacity: Math.max(0.4, 1 - stressLevel * 0.6),
          }}
        >

          <p className="t-row transition-colors duration-500" style={{ color: stressLevel > 0.6 ? 'var(--ink-muted)' : 'var(--ink-primary)' }}>
            Prefrontal Cortex
          </p>
          <p className="t-meta transition-colors duration-500" style={{ color: stressLevel > 0.6 ? 'var(--ink-muted)' : 'var(--ink-secondary)' }}>
            Rational Thinking
          </p>
          <div className="mt-3 h-2 w-full rounded overflow-hidden" style={{ backgroundColor: 'var(--hairline)' }}>
            <div
              className="h-full rounded transition-all duration-500"
              style={{
                width: `${Math.max(5, (1 - stressLevel) * 100)}%`,
                backgroundColor: stressLevel > 0.6 ? 'var(--ink-muted)' : 'var(--ink-primary)',
              }}
            />
          </div>
          <p className="ex-label mt-1 transition-colors duration-500" style={{ color: stressLevel > 0.6 ? 'var(--ink-muted)' : 'var(--ink-primary)' }}>
            {stressLevel < 0.3 ? 'Online' : stressLevel < 0.6 ? 'Weakening' : 'Offline'}
          </p>
        </div>

        {/* Connection indicator */}
        <div className="hidden sm:flex flex-col items-center justify-center px-4 gap-1.5">
          {[0, 1, 2, 3, 4].map(i => (
            <div
              key={i}
              className="w-2 h-2 rounded-full transition-all duration-500"
              style={{
                backgroundColor: 'var(--ink-primary)',
                opacity: stressLevel > (i * 0.2 + 0.1) ? 0.3 : 1,
              }}
            />
          ))}
          <p className="t-label text-ink-muted mt-1" style={{ writingMode: 'vertical-rl' as any }}>
            {stressLevel < 0.3 ? 'CONNECTED' : stressLevel < 0.7 ? 'WEAKENING' : 'SEVERED'}
          </p>
        </div>

        {/* Amygdala */}
        <div
          className="flex flex-col gap-1 pt-3 transition-all duration-500"
          style={{ borderTop: '1px solid var(--hairline)' }}
        >

          <p className="t-row transition-colors duration-500" style={{ color: stressLevel > 0.5 ? 'var(--ink-primary)' : 'var(--ink-muted)' }}>
            Amygdala
          </p>
          <p className="t-meta transition-colors duration-500" style={{ color: stressLevel > 0.5 ? 'var(--ink-secondary)' : 'var(--ink-muted)' }}>
            Threat Response
          </p>
          <div className="mt-3 h-2 w-full rounded overflow-hidden" style={{ backgroundColor: 'var(--hairline)' }}>
            <div
              className="h-full rounded transition-all duration-500"
              style={{
                width: `${Math.max(5, stressLevel * 100)}%`,
                backgroundColor: stressLevel > 0.7 ? 'var(--ink-primary)' : stressLevel > 0.4 ? 'var(--ink-secondary)' : 'var(--ink-muted)',
              }}
            />
          </div>
          <p className="ex-label mt-1 transition-colors duration-500" style={{ color: stressLevel > 0.5 ? 'var(--ink-primary)' : 'var(--ink-muted)' }}>
            {stressLevel < 0.3 ? 'Dormant' : stressLevel < 0.6 ? 'Alert' : 'Hijacking'}
          </p>
        </div>
      </div>

      {/* Cortisol bar + status */}
      <div className="flex flex-col gap-1.5">
        <div className="flex items-center justify-between gap-3">
          <span className="ex-label">Cortisol Level</span>
          <span className="ex-label" style={{ color: 'var(--ink-primary)' }}>
            {stressLevel < 0.15 ? 'Low' : stressLevel < 0.5 ? 'Moderate' : stressLevel < 0.8 ? 'High' : 'Extreme'}
          </span>
        </div>
        <div className="h-2 w-full rounded overflow-hidden" style={{ backgroundColor: 'var(--hairline)' }}>
          <div
            className="h-full rounded transition-all duration-300"
            style={{
              width: `${cortisolHeight}%`,
              backgroundColor: stressLevel > 0.7 ? 'var(--ink-primary)' : stressLevel > 0.4 ? 'var(--ink-secondary)' : 'var(--ink-muted)',
            }}
          />
        </div>
      </div>

      {/* Status label: small capitals in ink (no tinted pill) */}
      <AnimatePresence mode="wait">
        {hijackLabel && !balanced && (
          <MotionDiv
            key="hijack"
            initial={{ opacity: 0, scale: 0.9 }}
            animate={{ opacity: 1, scale: 1 }}
            exit={{ opacity: 0, scale: 0.9 }}
          >
            <p className="ex-label" style={{ color: 'var(--ink-primary)' }}>
              Amygdala Hijack
            </p>
          </MotionDiv>
        )}
        {balanced && (
          <MotionDiv
            key="balanced"
            initial={{ opacity: 0, scale: 0.9 }}
            animate={{ opacity: 1, scale: 1 }}
            exit={{ opacity: 0, scale: 0.9 }}
          >
            <p className="ex-label" style={{ color: 'var(--ink-primary)' }}>
              Balanced
            </p>
          </MotionDiv>
        )}
      </AnimatePresence>

      {/* Scenario answers: disabled while the stress rises, as before */}
      <AnswerGroup kind="one" legend="Choose a scenario:" chooseOnArrow={false}>
        <ChoiceTile
          chosen={scenario === 'low'}
          onClick={() => handleScenario('low')}
          disabled={isAnimating}
          label="Low Stakes — Homework Quiz"
        />
        <ChoiceTile
          chosen={scenario === 'medium'}
          onClick={() => handleScenario('medium')}
          disabled={isAnimating}
          label="Medium Stakes — Class Test"
        />
        <ChoiceTile
          chosen={scenario === 'high'}
          onClick={() => handleScenario('high')}
          disabled={isAnimating}
          label="High Stakes — Big Exam"
        />
      </AnswerGroup>

      {/* Recovery Techniques */}
      <AnimatePresence>
        {stressLevel > 0.15 && !isAnimating && !balanced && (
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            exit={{ opacity: 0, y: 20 }}
            className="ex-stack"
          >
            <AnswerGroup kind="one" legend="Choose a recovery technique:">
              <ChoiceTile
                chosen={recoveryActive === 'breathing'}
                onClick={() => { setRecoveryActive('breathing'); setBreathPhase(0); setBreathCount(0); }}
                label="Box Breathing"
              />
              <ChoiceTile
                chosen={recoveryActive === 'grounding'}
                onClick={() => { setRecoveryActive('grounding'); setGroundingStep(0); setGroundingClicks(0); }}
                label="5-4-3-2-1 Grounding"
              />
              <ChoiceTile
                chosen={recoveryActive === 'reframe'}
                onClick={() => { setRecoveryActive('reframe'); setReframeStep(0); }}
                label="Cognitive Reframe"
              />
            </AnswerGroup>

            {/* Box Breathing Panel */}
            <AnimatePresence mode="wait">
              {recoveryActive === 'breathing' && (
                <motion.div
                  key="breathing"
                  initial={{ opacity: 0, height: 0 }}
                  animate={{ opacity: 1, height: 'auto' }}
                  exit={{ opacity: 0, height: 0 }}
                  className="overflow-hidden"
                >
                  {/* On the sheet under a hairline (no box); the breathing square is the drawing */}
                  <div className="flex flex-col items-center gap-4 pt-4" style={{ borderTop: '1px solid var(--hairline)' }}>
                    <p className="t-body text-ink-primary">Follow the breathing square. 4 seconds each side.</p>
                    <div className="relative w-32 h-32">
                      {/* Square outline */}
                      <div className="absolute inset-0 rounded-lg" style={{ border: '2px solid var(--outline-soft)' }} />
                      {/* Animated highlight edge */}
                      <motion.div
                        className="absolute w-4 h-4 rounded-full"
                        animate={{
                          top: breathPhase === 0 ? ['100%', '0%'] : breathPhase === 1 ? '0%' : breathPhase === 2 ? ['0%', '100%'] : '100%',
                          left: breathPhase === 0 ? '0%' : breathPhase === 1 ? ['0%', '100%'] : breathPhase === 2 ? '100%' : ['100%', '0%'],
                        }}
                        transition={{ duration: 1.2, ease: 'linear' }}
                        style={{ marginTop: -8, marginLeft: -8, backgroundColor: 'var(--ink-primary)' }}
                      />
                    </div>
                    <motion.p
                      key={breathPhase}
                      initial={{ opacity: 0 }}
                      animate={{ opacity: 1 }}
                      className="ex-thought-words"
                    >
                      {breathLabels[breathPhase]}
                    </motion.p>
                    <p className="ex-count ui-readout">Cycle {breathCount + 1} of 3</p>
                  </div>
                </motion.div>
              )}

              {/* Grounding Panel */}
              {recoveryActive === 'grounding' && (
                <motion.div
                  key="grounding"
                  initial={{ opacity: 0, height: 0 }}
                  animate={{ opacity: 1, height: 'auto' }}
                  exit={{ opacity: 0, height: 0 }}
                  className="overflow-hidden"
                >
                  <div className="flex flex-col items-center gap-4 pt-4" style={{ borderTop: '1px solid var(--hairline)' }}>
                    <p className="t-body text-ink-primary">
                      Tap the button for {groundingSenses[groundingStep]?.count} {groundingSenses[groundingStep]?.sense}.
                    </p>
                    <div className="flex gap-2">
                      {Array.from({ length: groundingSenses[groundingStep]?.count || 0 }).map((_, i) => (
                        <div
                          key={i}
                          className="w-6 h-6 rounded-full transition-all duration-300"
                          style={{
                            border: `1.5px solid ${i < groundingClicks ? 'var(--ink-primary)' : 'var(--outline-soft)'}`,
                            backgroundColor: i < groundingClicks ? 'var(--ink-primary)' : 'transparent',
                          }}
                        />
                      ))}
                    </div>
                    <Button onClick={handleGroundingClick}>
                      I notice one ({groundingClicks}/{groundingSenses[groundingStep]?.count})
                    </Button>
                    <p className="ex-count ui-readout">
                      Step {groundingStep + 1} of 5
                    </p>
                  </div>
                </motion.div>
              )}

              {/* Reframe Panel */}
              {recoveryActive === 'reframe' && (
                <motion.div
                  key="reframe"
                  initial={{ opacity: 0, height: 0 }}
                  animate={{ opacity: 1, height: 'auto' }}
                  exit={{ opacity: 0, height: 0 }}
                  className="overflow-hidden"
                >
                  <div className="flex flex-col gap-4 pt-4" style={{ borderTop: '1px solid var(--hairline)' }}>
                    <p className="t-body text-ink-primary">Replace the threat with a realistic thought.</p>
                    {/* The two thoughts under their labels, with a step between them (no tinted boxes) */}
                    <div className="ex-stack">
                      <div className="ex-thought">
                        <ExerciseLabel>Threat Thought</ExerciseLabel>
                        <p className="ex-quote">{reframes[reframeStep].threat}</p>
                      </div>
                      <div className="ex-connector">
                        <i aria-hidden="true" />
                        <span className="t-row text-ink-muted">&darr;</span>
                        <i aria-hidden="true" />
                      </div>
                      <div className="ex-thought">
                        <ExerciseLabel>Reframed Thought</ExerciseLabel>
                        <p className="ex-quote">{reframes[reframeStep].reframe}</p>
                      </div>
                    </div>
                    <div className="ex-actions">
                      <Button onClick={handleReframe}>
                        I believe this reframe
                      </Button>
                    </div>
                    <p className="ex-count ui-readout text-center">
                      Reframe {reframeStep + 1} of 3
                    </p>
                  </div>
                </motion.div>
              )}
            </AnimatePresence>
          </motion.div>
        )}
      </AnimatePresence>

      {/* Balanced celebration */}
      <AnimatePresence>
        {balanced && (
          <MotionDiv
            initial={{ opacity: 0, y: 8 }}
            animate={{ opacity: 1, y: 0 }}
            exit={{ opacity: 0 }}
          >
            <AnswerLine>
              You restored the connection. Rational thinking is back online.
            </AnswerLine>
          </MotionDiv>
        )}
      </AnimatePresence>

      {/* Reset */}
      {scenario && !isAnimating && (
        <div className="ex-actions">
          <TextButton tone="quiet" onClick={handleReset}>
            Reset Simulator
          </TextButton>
        </div>
      )}
    </ExerciseSheet>;
};

// --- MODULE COMPONENT ---
const TheScienceOfMakingMistakesModule: React.FC<{ onBack: () => void; progress: ModuleProgress; onProgressUpdate: (progress: ModuleProgress) => void }> = ({ onBack, progress, onProgressUpdate }) => {
  const essentials = useEssentialsMode();
  const sections = [
    { id: 'brain-alarm', title: "The Brain's Alarm", eyebrow: '01 // The "Uh-Oh" Signal', icon: AlertTriangle },
    { id: 'second-signal', title: 'The Second Signal', eyebrow: '02 // The Analysis', icon: Lightbulb },
    { id: 'mindset-switch', title: 'The Mindset Switch', eyebrow: '03 // Leaning In', icon: ToggleRight },
    { id: 'high-stakes-hijack', title: 'The High-Stakes Hijack', eyebrow: '04 // The High-Stakes Brain', icon: ZapOff },
    { id: 'error-toolkit', title: 'Your Error Toolkit', eyebrow: '05 // Building Better Habits', icon: Wrench },
  ];

  return (
    <ModuleLayout
      moduleNumber="05"
      moduleTitle="The Science of Mistakes"
      moduleSubtitle="Why Mistakes Are Your Best Study Tool"
      moduleDescription="Your brain does something incredible when you mess up — if you let it. Here's how to stop fearing mistakes and start using them to get better, especially when the pressure is on."
      theme={theme}
      sections={sections}
      onBack={onBack}
      progress={progress}
      onProgressUpdate={onProgressUpdate}
      references={SCIENCE_OF_MISTAKES_REFERENCE_LIST}
      finishButtonText="Make Mistakes Count"
    >
      {(activeSection) => (
        <>
          {activeSection === 0 && (
            <ReadingSection title="The Brain's Alarm." eyebrow="Step 1" icon={AlertTriangle} theme={theme}>
              {essentials ? (
                <>
                  <p>When you make a mistake, your brain fires an instant alarm called the <Highlight description="An automatic brain signal that fires within about a tenth of a second of an error." theme={theme}>ERN</Highlight>.<Cite n={1} /> You do not even notice it happening. Think of it as your brain's smoke detector. This alarm spots the error but does not help you learn. What happens next is the part that matters.</p>
                  <PersonalStory name="Alex" role="Founder, NextStepUni">
                    <p>Failing the Junior Cert was the biggest mistake of my early life. At the time, it felt like a verdict — proof that school wasn't for me. It took me a long time to realise that the failure itself wasn't the problem. The problem was that I looked away from it instead of leaning in. When I finally did lean in, that failure became the single most useful piece of data I ever received.</p>
                  </PersonalStory>
                </>
              ) : (
                <>
                  <p>When you make a mistake — a typo, a wrong turn in a maths problem — your brain picks up on it instantly. Before you even realise what happened, an electrical signal called the <Highlight description="A tiny electrical blip your brain fires off within a fraction of a second of messing up. It happens before you even realise you made a mistake — it's your brain's automatic 'oh no' moment." theme={theme}>Error-Related Negativity (ERN)</Highlight> fires.<Cite n={1} /> It's a super-fast, automatic "uh-oh" moment.</p>
                  <p>Think of it as your brain's smoke detector. It's an unconscious alarm that goes off when what you did doesn't match what you meant to do. This signal matters, but it's not the part that actually helps you learn. It's what happens next that makes the real difference.</p>
                  <PersonalStory name="Alex" role="Founder, NextStepUni">
                    <p>Failing the Junior Cert was the biggest mistake of my early life. At the time, it felt like a verdict — proof that school wasn't for me. It took me a long time to realise that the failure itself wasn't the problem. The problem was that I looked away from it instead of leaning in. When I finally did lean in, that failure became the single most useful piece of data I ever received.</p>
                  </PersonalStory>
                </>
              )}
            </ReadingSection>
          )}
           {activeSection === 1 && (
            <ReadingSection title="The Second Signal." eyebrow="Step 2" icon={Lightbulb} theme={theme}>
              {essentials ? (
                <>
                  <p>Half a second later, a second signal called the <Highlight description="A brain signal showing you are consciously paying attention to the mistake." theme={theme}>Pe</Highlight> can fire. This one is not automatic. It means you are paying attention to the error. The bigger your Pe signal, the more likely you are to fix the mistake next time.<Cite n={2} /> The ERN is the alarm beeping. The Pe is you getting up to find the smoke.</p>
                </>
              ) : (
                <>
                  <p>About half a second after that first alarm, a second, bigger brainwave can kick in. This is the <Highlight description="A second, bigger brain signal that kicks in about half a second after a mistake. This one means you're actually paying attention to what went wrong. The stronger this signal is, the more likely you are to fix the mistake next time." theme={theme}>Error Positivity (Pe)</Highlight> signal. Unlike the first one, this doesn't happen on autopilot. This is the signal that you're consciously paying attention to the mistake, thinking about it, and actually engaging with it. It's the moment your brain decides to learn from what went wrong.</p>
                  <p>You can think of it like this: the ERN is the smoke alarm beeping. The Pe is you getting out of bed to find the source of the smoke. The size of your Pe wave is linked to how likely you are to correct the error and get it right next time.<Cite n={2} /> Basically, it's your brain's way of showing that you actually care about what went wrong.</p>
                </>
              )}
              <BrainSignalVisualizer />
            </ReadingSection>
          )}
          {activeSection === 2 && (
            <ReadingSection title="The Mindset Switch." eyebrow="Step 3" icon={ToggleRight} theme={theme}>
              {essentials ? (
                <p>Your mindset is linked to the size of that Pe signal. A <Highlight description="Believing you are either smart or not." theme={theme}>Fixed Mindset</Highlight> tends to produce a weaker signal. You look away from the mistake because it feels personal. A <Highlight description="Believing you can get smarter through effort." theme={theme}>Growth Mindset</Highlight> tends to produce a stronger signal.<Cite n={2} /> You lean into the mistake because it is useful information. You actually want to know what went wrong.</p>
              ) : (
                <>
                  <p>Here's the really interesting part. The size of your Pe wave — that second signal — is linked to your mindset. In one study, students with a <Highlight description="The belief that you're either smart or you're not, and nothing can change that. If you think this way, mistakes feel like proof you're not good enough." theme={theme}>Fixed Mindset</Highlight> showed a weaker Pe signal. They hear the alarm, but they quickly look away from the mistake because it feels personal. If "being smart" is your whole identity, then a mistake feels like proof that you're not.</p>
                  <p>Students with a <Highlight description="The belief that you can get smarter through effort and better strategies. If you think this way, mistakes don't feel like failures — they feel like useful information about what to work on next." theme={theme}>Growth Mindset</Highlight> showed a stronger Pe signal.<Cite n={2} /> They lean into the mistake and really focus on it. They get that the error isn't a judgement on how clever they are — it's a clue about what to work on next. They actually want the information that comes from getting it wrong.</p>
                </>
              )}
            </ReadingSection>
          )}
           {activeSection === 3 && (
            <ReadingSection title="The High-Stakes Hijack." eyebrow="Step 4" icon={ZapOff} theme={theme}>
                {essentials ? (
                  <>
                    <p>Stress can break this whole system. In a high-pressure exam, fear triggers an <Highlight description="When the panicky part of your brain shuts down the logical part." theme={theme}>amygdala hijack</Highlight>. Acute stress weakens the logical, problem-solving part of your brain, so it is much harder to analyse a mistake calmly in the moment.<Cite n={3} /> You stop learning from errors and just try to survive. This is why you "go blank" after one bad question. Try the simulator below to see it happen.</p>
                  </>
                ) : (
                  <>
                    <p>This whole system can be hijacked by stress. In a high-pressure situation like a big exam, the fear of messing up can trigger an <Highlight description="When the emotional, panicky part of your brain completely takes over and shuts down the calm, logical part. It's why one bad moment in an exam can make your whole brain feel like it's frozen." theme={theme}>amygdala hijack</Highlight>. This floods your brain with stress chemicals that basically put it into panic mode.</p>
                    <p>When that happens, the logical, problem-solving part of your brain — the prefrontal cortex — gets weaker under the flood of stress chemicals, making it much harder to think straight and work through an error calmly.<Cite n={3} /> Your brain shifts out of learning-mode and into survival-mode. This is exactly why you can "go blank" after one bad question in an exam and feel like you can't recover.</p>
                  </>
                )}
                <AmygdalaHijackSimulator />
            </ReadingSection>
          )}
           {activeSection === 4 && (
            <ReadingSection title="Your Error Toolkit." eyebrow="Step 5" icon={Wrench} theme={theme}>
              {essentials ? (
                <p>You can train your brain to handle mistakes. Stop treating errors as insults. They are information. Start a <Highlight description="A notebook where you write down each mistake and why it happened." theme={theme}>Mistake Log</Highlight>. Write down each mistake, figure out why it happened, and note one fix. This trains your brain to pay attention to errors instead of flinching away.</p>
              ) : (
                <>
                  <p>The good news is you can train your brain to handle mistakes better and stay solid under pressure. It's a skill, not something you're born with. The first step is to <strong>stop treating mistakes like they mean something about you</strong>. They're information, not insults. Every error is basically a signpost pointing to exactly where you need to focus next.</p>
                  <p>The most powerful tool for this is a <Highlight description="A simple notebook or page where you write down each mistake you make in practice, figure out why it happened (did you rush it, not understand it, or just forget something?), and write down one thing you'll do to fix it." theme={theme}>Mistake Log</Highlight>. Writing your mistakes down forces you to actually think about them properly instead of just cringing and moving on. It trains your brain to pay real attention to errors instead of flinching away from them. Don't just spot your mistakes — dig into them. They're the best study tool you have.</p>
                </>
              )}
               <MicroCommitment theme={theme}>
                <p>For your next piece of homework, actively look for one mistake you made. Don't just correct it. Write down in one sentence <em>why</em> you made it. You've just started your first mistake log.</p>
              </MicroCommitment>
            </ReadingSection>
          )}
        </>
      )}
    </ModuleLayout>
  );
};
export default TheScienceOfMakingMistakesModule;
