/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
*/

import React, { useState, useEffect, useCallback } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import {
  AlertTriangle, Lightbulb, ToggleRight, ZapOff, Wrench
} from 'lucide-react';
import { ModuleProgress } from '../types';
import { redTheme } from '../moduleThemes';
import { Highlight, ReadingSection, MicroCommitment } from './ModuleShared';
import { ModuleLayout } from './ModuleLayout';

const theme = redTheme;

// --- INTERACTIVE COMPONENTS ---
const BrainSignalVisualizer = () => {
    const [active, setActive] = useState(false);
    return(
        <div className="my-10 p-8 md:p-12 bg-white dark:bg-zinc-800 rounded-xl border border-zinc-200 dark:border-zinc-700">
             <h4 className="font-serif text-2xl font-semibold text-zinc-800 dark:text-white text-center">The Brain's Two Signals</h4>
             <p className="text-center text-sm text-zinc-500 dark:text-zinc-400 mb-8">When you make a mistake, your brain sends two distinct signals in less than half a second.</p>
             <div className="w-full max-w-lg mx-auto h-32 relative">
                <svg viewBox="0 0 300 100" className="w-full h-full absolute inset-0">
                    <path d="M0 50 L 300 50" stroke="#e5e7eb" strokeWidth="1" />
                    <AnimatePresence>
                    {active && <>
                        <motion.path initial={{pathLength:0}} animate={{pathLength:1}} transition={{duration:0.2, delay: 0.1}} d="M 50 50 C 60 50 65 20 75 20 S 90 50 100 50" stroke="#f43f5e" strokeWidth="2" fill="none" />
                        <motion.path initial={{pathLength:0}} animate={{pathLength:1}} transition={{duration:0.5, delay: 0.3}} d="M 150 50 C 160 50 175 80 190 80 S 210 50 220 50" stroke="#10b981" strokeWidth="2" fill="none" />
                    </>}
                    </AnimatePresence>
                </svg>
                {active && <>
                    <motion.div initial={{opacity:0}} animate={{opacity:1, transition:{delay:0.2}}} className="absolute top-0 left-[75px] -translate-x-1/2 text-center text-xs">
                        <p className="font-bold text-rose-600">ERN Signal</p>
                        <p className="text-zinc-500 dark:text-zinc-400">The "Alarm"</p>
                    </motion.div>
                    <motion.div initial={{opacity:0}} animate={{opacity:1, transition:{delay:0.5}}} className="absolute bottom-0 left-[190px] -translate-x-1/2 text-center text-xs">
                        <p className="font-bold text-emerald-600">Pe Signal</p>
                        <p className="text-zinc-500 dark:text-zinc-400">The "Analysis"</p>
                    </motion.div>
                </>}
             </div>
             <div className="text-center mt-8">
                <button onClick={() => setActive(!active)} className="px-5 py-3 bg-zinc-800 text-white font-bold rounded-lg text-sm">{active ? "Reset" : "Make a Mistake"}</button>
             </div>
        </div>
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

  const animateStress = useCallback((target: number) => {
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
    const interval = setInterval(() => {
      current += step;
      if (current >= target) {
        current = target;
        clearInterval(interval);
        setIsAnimating(false);
        if (target >= 0.7) {
          setHijackLabel(true);
        }
      }
      setStressLevel(current);
    }, 50);
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
              reduceStress(stressLevel);
              return 0;
            }
            reduceStress(stressLevel * 0.3);
            return newCount;
          });
        }
        return next;
      });
    }, 1200);
    return () => clearInterval(interval);
  }, [recoveryActive, stressLevel, reduceStress]);

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
  const pfcOpacity = Math.max(0.15, 1 - stressLevel * 0.85);
  const amygdalaGlow = stressLevel;
  const connectionOpacity = Math.max(0.1, 1 - stressLevel * 0.9);
  const connectionWidth = Math.max(1, 4 - stressLevel * 3);
  const cortisolHeight = stressLevel * 100;

  return (
    <div className="my-10 p-8 md:p-12 bg-white dark:bg-zinc-800 rounded-xl border border-zinc-200 dark:border-zinc-700">
      <h4 className="font-serif text-2xl font-semibold text-zinc-800 dark:text-white text-center">Amygdala Hijack Simulator</h4>
      <p className="text-center text-sm text-zinc-500 dark:text-zinc-400 mt-2 mb-8">See how stress hijacks your brain — then use recovery techniques to take control back.</p>

      <div className="flex flex-col lg:flex-row items-center justify-center gap-8 lg:gap-12">
        {/* Brain Diagram */}
        <div className="relative w-full max-w-sm">
          <svg viewBox="0 0 300 260" className="w-full">
            {/* Brain outline */}
            <ellipse cx="150" cy="130" rx="130" ry="110" fill="none" stroke="#a1a1aa" strokeWidth="1.5" strokeDasharray="4 3" opacity={0.4} />

            {/* Connection bridge */}
            <motion.line
              x1="150" y1="85" x2="150" y2="155"
              stroke="#a1a1aa"
              strokeWidth={connectionWidth}
              style={{ opacity: connectionOpacity }}
              strokeDasharray={stressLevel > 0.5 ? '6 4' : 'none'}
            />
            <motion.text
              x="170" y="125" fontSize="9" fill="#a1a1aa"
              style={{ opacity: connectionOpacity }}
            >
              connection
            </motion.text>

            {/* Prefrontal Cortex (top) */}
            <motion.rect
              x="75" y="30" width="150" height="60" rx="16"
              style={{
                fill: `rgba(59, 130, 246, ${pfcOpacity})`,
                transition: 'fill 0.3s ease',
              }}
            />
            <text x="150" y="56" textAnchor="middle" fontSize="13" fontWeight="bold"
              style={{ fill: stressLevel > 0.6 ? '#9ca3af' : '#1e3a5f', transition: 'fill 0.3s ease' }}>
              Prefrontal Cortex
            </text>
            <text x="150" y="74" textAnchor="middle" fontSize="10"
              style={{ fill: stressLevel > 0.6 ? '#9ca3af' : '#3b82f6', transition: 'fill 0.3s ease' }}>
              Rational Thinking
            </text>

            {/* Amygdala (center/deeper) */}
            <motion.ellipse
              cx="150" cy="185" rx="50" ry="35"
              style={{
                fill: `rgba(239, 68, 68, ${Math.max(0.15, amygdalaGlow)})`,
                transition: 'fill 0.3s ease',
              }}
            />
            {stressLevel > 0.5 && (
              <motion.ellipse
                cx="150" cy="185" rx="55" ry="40"
                initial={{ opacity: 0 }}
                animate={{ opacity: [0.2, 0.4, 0.2] }}
                transition={{ repeat: Infinity, duration: 1.5 }}
                fill="none"
                stroke="rgba(239, 68, 68, 0.4)"
                strokeWidth="2"
              />
            )}
            <text x="150" y="182" textAnchor="middle" fontSize="13" fontWeight="bold"
              style={{ fill: stressLevel > 0.5 ? '#fef2f2' : '#7f1d1d', transition: 'fill 0.3s ease' }}>
              Amygdala
            </text>
            <text x="150" y="198" textAnchor="middle" fontSize="10"
              style={{ fill: stressLevel > 0.5 ? '#fecaca' : '#ef4444', transition: 'fill 0.3s ease' }}>
              Threat Response
            </text>

            {/* Hijack label */}
            {hijackLabel && !balanced && (
              <motion.g initial={{ opacity: 0, y: 5 }} animate={{ opacity: 1, y: 0 }}>
                <rect x="85" y="230" width="130" height="26" rx="6" fill="#dc2626" />
                <text x="150" y="247" textAnchor="middle" fontSize="11" fontWeight="bold" fill="white">
                  AMYGDALA HIJACK
                </text>
              </motion.g>
            )}

            {/* Balanced label */}
            {balanced && (
              <motion.g initial={{ opacity: 0, y: 5 }} animate={{ opacity: 1, y: 0 }}>
                <rect x="100" y="230" width="100" height="26" rx="6" fill="#16a34a" />
                <text x="150" y="247" textAnchor="middle" fontSize="11" fontWeight="bold" fill="white">
                  BALANCED
                </text>
              </motion.g>
            )}
          </svg>
        </div>

        {/* Cortisol Meter */}
        <div className="flex flex-col items-center gap-2">
          <p className="text-xs font-bold uppercase tracking-wider text-zinc-500 dark:text-zinc-400">Cortisol</p>
          <div className="w-8 h-40 bg-zinc-100 dark:bg-zinc-700 rounded-full overflow-hidden relative border border-zinc-200 dark:border-zinc-600">
            <motion.div
              className="absolute bottom-0 left-0 right-0 rounded-full"
              style={{
                height: `${cortisolHeight}%`,
                backgroundColor: stressLevel > 0.7 ? '#dc2626' : stressLevel > 0.4 ? '#f59e0b' : '#22c55e',
                transition: 'height 0.3s ease, background-color 0.3s ease',
              }}
            />
          </div>
          <p className="text-xs text-zinc-500 dark:text-zinc-400 font-medium">
            {stressLevel < 0.15 ? 'Low' : stressLevel < 0.5 ? 'Moderate' : stressLevel < 0.8 ? 'High' : 'Extreme'}
          </p>
        </div>
      </div>

      {/* Scenario Buttons */}
      <div className="mt-10">
        <p className="text-center text-sm font-semibold text-zinc-600 dark:text-zinc-300 mb-4">Choose a scenario:</p>
        <div className="flex flex-wrap justify-center gap-3">
          <button
            onClick={() => handleScenario('low')}
            disabled={isAnimating}
            className={`px-5 py-2.5 rounded-lg text-sm font-bold transition-all duration-200 ${
              scenario === 'low'
                ? 'bg-green-500 text-white shadow-lg shadow-green-500/20'
                : 'bg-zinc-100 dark:bg-zinc-700 text-zinc-700 dark:text-zinc-200 hover:bg-green-100 dark:hover:bg-green-900/30'
            } disabled:opacity-50`}
          >
            Low Stakes — Homework Quiz
          </button>
          <button
            onClick={() => handleScenario('medium')}
            disabled={isAnimating}
            className={`px-5 py-2.5 rounded-lg text-sm font-bold transition-all duration-200 ${
              scenario === 'medium'
                ? 'bg-amber-500 text-white shadow-lg shadow-amber-500/20'
                : 'bg-zinc-100 dark:bg-zinc-700 text-zinc-700 dark:text-zinc-200 hover:bg-amber-100 dark:hover:bg-amber-900/30'
            } disabled:opacity-50`}
          >
            Medium Stakes — Class Test
          </button>
          <button
            onClick={() => handleScenario('high')}
            disabled={isAnimating}
            className={`px-5 py-2.5 rounded-lg text-sm font-bold transition-all duration-200 ${
              scenario === 'high'
                ? 'bg-red-500 text-white shadow-lg shadow-red-500/20'
                : 'bg-zinc-100 dark:bg-zinc-700 text-zinc-700 dark:text-zinc-200 hover:bg-red-100 dark:hover:bg-red-900/30'
            } disabled:opacity-50`}
          >
            High Stakes — Leaving Cert Exam
          </button>
        </div>
      </div>

      {/* Recovery Techniques */}
      <AnimatePresence>
        {stressLevel > 0.15 && !isAnimating && !balanced && (
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            exit={{ opacity: 0, y: 20 }}
            className="mt-10"
          >
            <p className="text-center text-sm font-semibold text-zinc-600 dark:text-zinc-300 mb-4">Choose a recovery technique:</p>
            <div className="flex flex-wrap justify-center gap-3 mb-6">
              <button
                onClick={() => { setRecoveryActive('breathing'); setBreathPhase(0); setBreathCount(0); }}
                className={`px-5 py-2.5 rounded-lg text-sm font-bold transition-all duration-200 ${
                  recoveryActive === 'breathing'
                    ? 'bg-sky-500 text-white shadow-lg shadow-sky-500/20'
                    : 'bg-zinc-100 dark:bg-zinc-700 text-zinc-700 dark:text-zinc-200 hover:bg-sky-100 dark:hover:bg-sky-900/30'
                }`}
              >
                Box Breathing
              </button>
              <button
                onClick={() => { setRecoveryActive('grounding'); setGroundingStep(0); setGroundingClicks(0); }}
                className={`px-5 py-2.5 rounded-lg text-sm font-bold transition-all duration-200 ${
                  recoveryActive === 'grounding'
                    ? 'bg-emerald-500 text-white shadow-lg shadow-emerald-500/20'
                    : 'bg-zinc-100 dark:bg-zinc-700 text-zinc-700 dark:text-zinc-200 hover:bg-emerald-100 dark:hover:bg-emerald-900/30'
                }`}
              >
                5-4-3-2-1 Grounding
              </button>
              <button
                onClick={() => { setRecoveryActive('reframe'); setReframeStep(0); }}
                className={`px-5 py-2.5 rounded-lg text-sm font-bold transition-all duration-200 ${
                  recoveryActive === 'reframe'
                    ? 'bg-violet-500 text-white shadow-lg shadow-violet-500/20'
                    : 'bg-zinc-100 dark:bg-zinc-700 text-zinc-700 dark:text-zinc-200 hover:bg-violet-100 dark:hover:bg-violet-900/30'
                }`}
              >
                Cognitive Reframe
              </button>
            </div>

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
                  <div className="flex flex-col items-center gap-4 p-6 bg-sky-50 dark:bg-sky-900/20 rounded-xl border border-sky-200 dark:border-sky-800">
                    <p className="text-sm font-medium text-sky-700 dark:text-sky-300">Follow the breathing square. 4 seconds each side.</p>
                    <div className="relative w-32 h-32">
                      {/* Square outline */}
                      <div className="absolute inset-0 border-2 border-sky-200 dark:border-sky-700 rounded-lg" />
                      {/* Animated highlight edge */}
                      <motion.div
                        className="absolute w-4 h-4 bg-sky-500 rounded-full shadow-lg shadow-sky-500/40"
                        animate={{
                          top: breathPhase === 0 ? ['100%', '0%'] : breathPhase === 1 ? '0%' : breathPhase === 2 ? ['0%', '100%'] : '100%',
                          left: breathPhase === 0 ? '0%' : breathPhase === 1 ? ['0%', '100%'] : breathPhase === 2 ? '100%' : ['100%', '0%'],
                        }}
                        transition={{ duration: 1.2, ease: 'linear' }}
                        style={{ marginTop: -8, marginLeft: -8 }}
                      />
                    </div>
                    <motion.p
                      key={breathPhase}
                      initial={{ opacity: 0 }}
                      animate={{ opacity: 1 }}
                      className="text-lg font-bold text-sky-600 dark:text-sky-400"
                    >
                      {breathLabels[breathPhase]}
                    </motion.p>
                    <p className="text-xs text-sky-500 dark:text-sky-400">Cycle {breathCount + 1} of 3</p>
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
                  <div className="flex flex-col items-center gap-4 p-6 bg-emerald-50 dark:bg-emerald-900/20 rounded-xl border border-emerald-200 dark:border-emerald-800">
                    <p className="text-sm font-medium text-emerald-700 dark:text-emerald-300">
                      Tap the button for {groundingSenses[groundingStep]?.count} {groundingSenses[groundingStep]?.sense}.
                    </p>
                    <div className="flex gap-2">
                      {Array.from({ length: groundingSenses[groundingStep]?.count || 0 }).map((_, i) => (
                        <div
                          key={i}
                          className="w-6 h-6 rounded-full border-2 transition-all duration-300"
                          style={{
                            borderColor: i < groundingClicks ? '#10b981' : '#d1d5db',
                            backgroundColor: i < groundingClicks ? '#10b981' : 'transparent',
                          }}
                        />
                      ))}
                    </div>
                    <button
                      onClick={handleGroundingClick}
                      className="px-6 py-3 bg-emerald-500 text-white font-bold rounded-lg text-sm hover:bg-emerald-600 transition-colors active:scale-95"
                    >
                      I notice one ({groundingClicks}/{groundingSenses[groundingStep]?.count})
                    </button>
                    <p className="text-xs text-emerald-500 dark:text-emerald-400">
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
                  <div className="flex flex-col items-center gap-4 p-6 bg-violet-50 dark:bg-violet-900/20 rounded-xl border border-violet-200 dark:border-violet-800">
                    <p className="text-sm font-medium text-violet-700 dark:text-violet-300">Replace the threat with a realistic thought.</p>
                    <div className="text-center space-y-3 max-w-sm">
                      <div className="p-3 bg-red-100 dark:bg-red-900/30 rounded-lg">
                        <p className="text-xs font-bold uppercase tracking-wider text-red-400 mb-1">Threat Thought</p>
                        <p className="text-sm font-medium text-red-700 dark:text-red-300">{reframes[reframeStep].threat}</p>
                      </div>
                      <div className="text-zinc-400 text-lg font-bold">&darr;</div>
                      <div className="p-3 bg-violet-100 dark:bg-violet-900/30 rounded-lg">
                        <p className="text-xs font-bold uppercase tracking-wider text-violet-400 mb-1">Reframed Thought</p>
                        <p className="text-sm font-medium text-violet-700 dark:text-violet-300">{reframes[reframeStep].reframe}</p>
                      </div>
                    </div>
                    <button
                      onClick={handleReframe}
                      className="px-6 py-3 bg-violet-500 text-white font-bold rounded-lg text-sm hover:bg-violet-600 transition-colors active:scale-95"
                    >
                      I believe this reframe
                    </button>
                    <p className="text-xs text-violet-500 dark:text-violet-400">
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
          <motion.div
            initial={{ opacity: 0, scale: 0.9 }}
            animate={{ opacity: 1, scale: 1 }}
            exit={{ opacity: 0, scale: 0.9 }}
            className="mt-8 text-center"
          >
            <p className="text-sm font-semibold text-emerald-600 dark:text-emerald-400">
              You restored the connection between your prefrontal cortex and amygdala. Rational thinking is back online.
            </p>
          </motion.div>
        )}
      </AnimatePresence>

      {/* Reset */}
      {scenario && !isAnimating && (
        <div className="mt-6 text-center">
          <button
            onClick={handleReset}
            className="px-4 py-2 text-xs font-medium text-zinc-500 dark:text-zinc-400 hover:text-zinc-800 dark:hover:text-white transition-colors underline"
          >
            Reset Simulator
          </button>
        </div>
      )}
    </div>
  );
};

// --- MODULE COMPONENT ---
const TheScienceOfMakingMistakesModule: React.FC<{ onBack: () => void; progress: ModuleProgress; onProgressUpdate: (progress: ModuleProgress) => void }> = ({ onBack, progress, onProgressUpdate }) => {
  const sections = [
    { id: 'brain-alarm', title: "The Brain's Alarm", eyebrow: '01 // The "Uh-Oh" Signal', icon: AlertTriangle },
    { id: 'second-signal', title: 'The Second Signal', eyebrow: '02 // The Analysis', icon: Lightbulb },
    { id: 'mindset-switch', title: 'The Mindset Switch', eyebrow: '03 // Leaning In', icon: ToggleRight },
    { id: 'high-stakes-hijack', title: 'The High-Stakes Hijack', eyebrow: '04 // The Leaving Cert Brain', icon: ZapOff },
    { id: 'error-toolkit', title: 'Your Error Toolkit', eyebrow: '05 // Rewiring Your Brain', icon: Wrench },
  ];

  return (
    <ModuleLayout
      moduleNumber="05"
      moduleTitle="The Science of Mistakes"
      moduleSubtitle="The Neural Architecture of Failure"
      moduleDescription="Learn why your brain's reaction to mistakes predicts success, and how to rewire it for resilience under pressure in high-stakes exams."
      theme={theme}
      sections={sections}
      onBack={onBack}
      progress={progress}
      onProgressUpdate={onProgressUpdate}
    >
      {(activeSection) => (
        <>
          {activeSection === 0 && (
            <ReadingSection title="The Brain's Alarm." eyebrow="Step 1" icon={AlertTriangle} theme={theme}>
              <p>When you make a mistake—a typo, a wrong turn in a maths problem—your brain registers it instantly. Before you are even consciously aware of it, an electrical signal called the <Highlight description="A neural signal of error detection that occurs within 50 milliseconds of a mistake. It is an unconscious 'uh-oh' signal originating from the anterior cingulate cortex." theme={theme}>Error-Related Negativity (ERN)</Highlight> fires. It's a super-fast, automatic "uh-oh" moment.</p>
              <p>Think of it as your brain's smoke detector. It's a primitive, unconscious alarm that goes off when your actions don't match your intentions. This signal is crucial, but it's not the part that drives learning. It's what happens next that separates high-performers from the rest.</p>
            </ReadingSection>
          )}
           {activeSection === 1 && (
            <ReadingSection title="The Second Signal." eyebrow="Step 2" icon={Lightbulb} theme={theme}>
              <p>About 200-500 milliseconds after the initial alarm, a second, larger brainwave can occur. This is the <Highlight description="A later neural signal (200-500ms post-error) that reflects conscious attention to and awareness of the mistake. The amplitude of the Pe wave is a strong predictor of post-error correction and learning." theme={theme}>Error Positivity (Pe)</Highlight> signal. This isn't automatic. This is the signal of your conscious brain paying attention to the mistake, analyzing it, and engaging with it. It's the moment your brain decides to learn from the error.</p>
              <p>You can think of it like this: the ERN is the smoke alarm beeping. The Pe is you getting out of bed to find the source of the smoke. The size of your Pe wave literally predicts how likely you are to correct the error and get it right next time. It's the neurobiological signature of giving a damn about your mistakes.</p>
              <BrainSignalVisualizer />
            </ReadingSection>
          )}
          {activeSection === 2 && (
            <ReadingSection title="The Mindset Switch." eyebrow="Step 3" icon={ToggleRight} theme={theme}>
              <p>Here's where it gets fascinating. Neuroscientists have shown that the size of your Pe wave is directly controlled by your mindset. Students with a <Highlight description="The belief that intelligence is a fixed trait. People with this mindset tend to see errors as a threat to their ego." theme={theme}>Fixed Mindset</Highlight> show a much smaller Pe signal. They hear the alarm, but they quickly "look away" from the mistake because it feels like a threat to their self-concept. If "being smart" is your identity, then a mistake is evidence that you're not.</p>
              <p>Students with a <Highlight description="The belief that intelligence can be grown through effort and strategy. They see errors as an opportunity to learn and improve." theme={theme}>Growth Mindset</Highlight> have a huge Pe signal. They lean into the mistake, allocating massive attentional resources to it. They understand that the error isn't a verdict on their ability; it's a crucial piece of data for improvement. They are hungry for the information contained within the failure.</p>
            </ReadingSection>
          )}
           {activeSection === 3 && (
            <ReadingSection title="The High-Stakes Hijack." eyebrow="Step 4" icon={ZapOff} theme={theme}>
                <p>This whole system can be hijacked by stress. In a high-stakes situation like the Leaving Cert, the fear of failure can trigger an <Highlight description="An intense emotional response that is out of proportion to the real threat, caused by the amygdala overriding the rational prefrontal cortex." theme={theme}>amygdala hijack</Highlight>. This floods your brain with stress hormones like cortisol.</p>
                <p>High cortisol levels do two terrible things. First, they impair the function of your prefrontal cortex, making it harder to think clearly. Second, they suppress the Pe signal. Your brain shifts from a "learning focus" to a "threat focus." It stops trying to analyse the mistake and starts trying to just survive the experience. This is why you can "go blank" after one mistake and find it impossible to recover.</p>
                <AmygdalaHijackSimulator />
            </ReadingSection>
          )}
           {activeSection === 4 && (
            <ReadingSection title="Your Error Toolkit." eyebrow="Step 5" icon={Wrench} theme={theme}>
              <p>The good news is you can train your brain to have a bigger Pe signal and be more resilient under pressure. It's a skill. The first step is to <strong>de-shame mistakes</strong>. See them as data, not as judgments on your character. Every error is a signpost pointing to exactly where you need to grow.</p>
              <p>The most powerful tool for this is a <Highlight description="A dedicated notebook or document where you log every mistake you make in practice, diagnose its cause (e.g., slip, gap, misconception), and prescribe a specific action to fix it." theme={theme}>Mistake Log</Highlight>. This forces you to engage with your errors in a structured, analytical way. It's a manual override that forces your brain to generate a strong Pe signal. Don't just find your mistakes; interrogate them. They are your best teachers.</p>
               <MicroCommitment theme={theme}>
                <p>For your next piece of homework, actively look for one mistake you made. Don't just correct it. Write down in one sentence *why* you made it. You've just started your first mistake log.</p>
              </MicroCommitment>
            </ReadingSection>
          )}
        </>
      )}
    </ModuleLayout>
  );
};
export default TheScienceOfMakingMistakesModule;
