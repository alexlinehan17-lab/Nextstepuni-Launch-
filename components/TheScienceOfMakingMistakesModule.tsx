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
import { Highlight, ReadingSection, MicroCommitment, PersonalStory } from './ModuleShared';
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

  const MotionDiv = motion.div as any;

  return (
    <div className="my-10 p-8 md:p-12 bg-white dark:bg-zinc-800 rounded-xl border border-zinc-200 dark:border-zinc-700">
      <h4 className="font-serif text-2xl font-semibold text-zinc-800 dark:text-white text-center">Amygdala Hijack Simulator</h4>
      <p className="text-center text-sm text-zinc-500 dark:text-zinc-400 mt-2 mb-8">See how stress hijacks your brain — then use recovery techniques to take control back.</p>

      {/* Two-panel brain dashboard */}
      <div className="grid grid-cols-1 sm:grid-cols-[1fr_auto_1fr] gap-4 sm:gap-0 items-stretch max-w-2xl mx-auto mb-6">
        {/* Prefrontal Cortex Card */}
        <div
          className="rounded-xl p-6 border text-center transition-all duration-500"
          style={{
            borderColor: stressLevel > 0.6 ? '#d4d4d8' : '#93c5fd',
            backgroundColor: stressLevel > 0.6 ? '#fafafa' : '#eff6ff',
            opacity: Math.max(0.4, 1 - stressLevel * 0.6),
          }}
        >
          <div
            className="w-12 h-12 rounded-full mx-auto mb-3 flex items-center justify-center text-lg transition-all duration-500"
            style={{
              backgroundColor: stressLevel > 0.6 ? '#e4e4e7' : '#dbeafe',
              color: stressLevel > 0.6 ? '#a1a1aa' : '#3b82f6',
            }}
          >
            &#x1f9e0;
          </div>
          <p className="text-sm font-bold transition-colors duration-500" style={{ color: stressLevel > 0.6 ? '#a1a1aa' : '#1e40af' }}>
            Prefrontal Cortex
          </p>
          <p className="text-xs mt-1 transition-colors duration-500" style={{ color: stressLevel > 0.6 ? '#d4d4d8' : '#60a5fa' }}>
            Rational Thinking
          </p>
          <div className="mt-4 h-2 w-full rounded-full overflow-hidden" style={{ backgroundColor: stressLevel > 0.6 ? '#e4e4e7' : '#bfdbfe' }}>
            <div
              className="h-full rounded-full transition-all duration-500"
              style={{
                width: `${Math.max(5, (1 - stressLevel) * 100)}%`,
                backgroundColor: stressLevel > 0.6 ? '#d4d4d8' : '#3b82f6',
              }}
            />
          </div>
          <p className="text-[10px] mt-2 font-semibold uppercase tracking-widest transition-colors duration-500" style={{ color: stressLevel > 0.6 ? '#a1a1aa' : '#3b82f6' }}>
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
                backgroundColor: stressLevel > (i * 0.2 + 0.1) ? '#e4e4e7' : '#a1a1aa',
                opacity: stressLevel > (i * 0.2 + 0.1) ? 0.3 : 1,
              }}
            />
          ))}
          <p className="text-[9px] text-zinc-400 dark:text-zinc-500 font-medium mt-1 writing-mode-vertical" style={{ writingMode: 'vertical-rl' as any }}>
            {stressLevel < 0.3 ? 'CONNECTED' : stressLevel < 0.7 ? 'WEAKENING' : 'SEVERED'}
          </p>
        </div>

        {/* Amygdala Card */}
        <div
          className="rounded-xl p-6 border text-center transition-all duration-500"
          style={{
            borderColor: stressLevel > 0.5 ? '#fca5a5' : '#e4e4e7',
            backgroundColor: stressLevel > 0.5 ? '#fef2f2' : '#fafafa',
            boxShadow: stressLevel > 0.7 ? '0 0 30px rgba(239, 68, 68, 0.15)' : 'none',
          }}
        >
          <div
            className="w-12 h-12 rounded-full mx-auto mb-3 flex items-center justify-center text-lg transition-all duration-500"
            style={{
              backgroundColor: stressLevel > 0.5 ? '#fee2e2' : '#f4f4f5',
              color: stressLevel > 0.5 ? '#ef4444' : '#a1a1aa',
            }}
          >
            &#x26a0;&#xfe0f;
          </div>
          <p className="text-sm font-bold transition-colors duration-500" style={{ color: stressLevel > 0.5 ? '#dc2626' : '#71717a' }}>
            Amygdala
          </p>
          <p className="text-xs mt-1 transition-colors duration-500" style={{ color: stressLevel > 0.5 ? '#f87171' : '#a1a1aa' }}>
            Threat Response
          </p>
          <div className="mt-4 h-2 w-full rounded-full overflow-hidden" style={{ backgroundColor: stressLevel > 0.5 ? '#fecaca' : '#e4e4e7' }}>
            <div
              className="h-full rounded-full transition-all duration-500"
              style={{
                width: `${Math.max(5, stressLevel * 100)}%`,
                backgroundColor: stressLevel > 0.7 ? '#dc2626' : stressLevel > 0.4 ? '#f59e0b' : '#a1a1aa',
              }}
            />
          </div>
          <p className="text-[10px] mt-2 font-semibold uppercase tracking-widest transition-colors duration-500" style={{ color: stressLevel > 0.5 ? '#dc2626' : '#a1a1aa' }}>
            {stressLevel < 0.3 ? 'Dormant' : stressLevel < 0.6 ? 'Alert' : 'Hijacking'}
          </p>
        </div>
      </div>

      {/* Cortisol bar + status */}
      <div className="max-w-2xl mx-auto mb-2">
        <div className="flex items-center justify-between mb-1.5">
          <span className="text-[10px] font-bold uppercase tracking-widest text-zinc-400 dark:text-zinc-500">Cortisol Level</span>
          <span className="text-[10px] font-bold uppercase tracking-widest" style={{
            color: stressLevel > 0.7 ? '#dc2626' : stressLevel > 0.4 ? '#f59e0b' : '#22c55e',
          }}>
            {stressLevel < 0.15 ? 'Low' : stressLevel < 0.5 ? 'Moderate' : stressLevel < 0.8 ? 'High' : 'Extreme'}
          </span>
        </div>
        <div className="h-3 w-full rounded-full overflow-hidden bg-zinc-100 dark:bg-zinc-700">
          <div
            className="h-full rounded-full transition-all duration-300"
            style={{
              width: `${cortisolHeight}%`,
              backgroundColor: stressLevel > 0.7 ? '#dc2626' : stressLevel > 0.4 ? '#f59e0b' : '#22c55e',
            }}
          />
        </div>
      </div>

      {/* Status label */}
      <AnimatePresence mode="wait">
        {hijackLabel && !balanced && (
          <MotionDiv
            key="hijack"
            initial={{ opacity: 0, scale: 0.9 }}
            animate={{ opacity: 1, scale: 1 }}
            exit={{ opacity: 0, scale: 0.9 }}
            className="text-center mt-4"
          >
            <span className="inline-block px-4 py-1.5 rounded-full bg-red-100 dark:bg-red-900/30 text-red-600 dark:text-red-400 text-xs font-bold uppercase tracking-widest">
              Amygdala Hijack
            </span>
          </MotionDiv>
        )}
        {balanced && (
          <MotionDiv
            key="balanced"
            initial={{ opacity: 0, scale: 0.9 }}
            animate={{ opacity: 1, scale: 1 }}
            exit={{ opacity: 0, scale: 0.9 }}
            className="text-center mt-4"
          >
            <span className="inline-block px-4 py-1.5 rounded-full bg-emerald-100 dark:bg-emerald-900/30 text-emerald-600 dark:text-emerald-400 text-xs font-bold uppercase tracking-widest">
              Balanced
            </span>
          </MotionDiv>
        )}
      </AnimatePresence>

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
          <MotionDiv
            initial={{ opacity: 0, y: 8 }}
            animate={{ opacity: 1, y: 0 }}
            exit={{ opacity: 0 }}
            className="mt-4 text-center"
          >
            <p className="text-sm font-semibold text-emerald-600 dark:text-emerald-400">
              You restored the connection. Rational thinking is back online.
            </p>
          </MotionDiv>
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
    >
      {(activeSection) => (
        <>
          {activeSection === 0 && (
            <ReadingSection title="The Brain's Alarm." eyebrow="Step 1" icon={AlertTriangle} theme={theme}>
              <p>When you make a mistake — a typo, a wrong turn in a maths problem — your brain picks up on it instantly. Before you even realise what happened, an electrical signal called the <Highlight description="A tiny electrical blip your brain fires off within 50 milliseconds of messing up. It happens before you even realise you made a mistake — it's your brain's automatic 'oh no' moment." theme={theme}>Error-Related Negativity (ERN)</Highlight> fires. It's a super-fast, automatic "uh-oh" moment.</p>
              <p>Think of it as your brain's smoke detector. It's an unconscious alarm that goes off when what you did doesn't match what you meant to do. This signal matters, but it's not the part that actually helps you learn. It's what happens next that makes the real difference.</p>
              <PersonalStory name="Alex" role="Founder, NextStepUni">
                <p>Failing the Junior Cert was the biggest mistake of my early life. At the time, it felt like a verdict — proof that school wasn't for me. It took me a long time to realise that the failure itself wasn't the problem. The problem was that I looked away from it instead of leaning in. When I finally did lean in, that failure became the single most useful piece of data I ever received.</p>
              </PersonalStory>
            </ReadingSection>
          )}
           {activeSection === 1 && (
            <ReadingSection title="The Second Signal." eyebrow="Step 2" icon={Lightbulb} theme={theme}>
              <p>About half a second after that first alarm, a second, bigger brainwave can kick in. This is the <Highlight description="A second, bigger brain signal that kicks in about half a second after a mistake. This one means you're actually paying attention to what went wrong. The stronger this signal is, the more likely you are to fix the mistake next time." theme={theme}>Error Positivity (Pe)</Highlight> signal. Unlike the first one, this doesn't happen on autopilot. This is the signal that you're consciously paying attention to the mistake, thinking about it, and actually engaging with it. It's the moment your brain decides to learn from what went wrong.</p>
              <p>You can think of it like this: the ERN is the smoke alarm beeping. The Pe is you getting out of bed to find the source of the smoke. The size of your Pe wave literally predicts how likely you are to correct the error and get it right next time. Basically, it's your brain's way of showing that you actually care about what went wrong.</p>
              <BrainSignalVisualizer />
            </ReadingSection>
          )}
          {activeSection === 2 && (
            <ReadingSection title="The Mindset Switch." eyebrow="Step 3" icon={ToggleRight} theme={theme}>
              <p>Here's the really interesting part. The size of your Pe wave — that second signal — depends heavily on your mindset. Students with a <Highlight description="The belief that you're either smart or you're not, and nothing can change that. If you think this way, mistakes feel like proof you're not good enough." theme={theme}>Fixed Mindset</Highlight> show a much weaker Pe signal. They hear the alarm, but they quickly look away from the mistake because it feels personal. If "being smart" is your whole identity, then a mistake feels like proof that you're not.</p>
              <p>Students with a <Highlight description="The belief that you can get smarter through effort and better strategies. If you think this way, mistakes don't feel like failures — they feel like useful information about what to work on next." theme={theme}>Growth Mindset</Highlight> have a much stronger Pe signal. They lean into the mistake and really focus on it. They get that the error isn't a judgement on how clever they are — it's a clue about what to work on next. They actually want the information that comes from getting it wrong.</p>
            </ReadingSection>
          )}
           {activeSection === 3 && (
            <ReadingSection title="The High-Stakes Hijack." eyebrow="Step 4" icon={ZapOff} theme={theme}>
                <p>This whole system can be hijacked by stress. In a high-pressure situation like the Leaving Cert, the fear of messing up can trigger an <Highlight description="When the emotional, panicky part of your brain completely takes over and shuts down the calm, logical part. It's why one bad moment in an exam can make your whole brain feel like it's frozen." theme={theme}>amygdala hijack</Highlight>. This floods your brain with stress chemicals that basically put it into panic mode.</p>
                <p>When that happens, two things go wrong at once. First, the logical, problem-solving part of your brain gets weaker, making it harder to think straight. Second, that important Pe signal gets squashed. Your brain stops trying to learn from the mistake and just tries to survive the moment. This is exactly why you can "go blank" after one bad question in an exam and feel like you can't recover.</p>
                <AmygdalaHijackSimulator />
            </ReadingSection>
          )}
           {activeSection === 4 && (
            <ReadingSection title="Your Error Toolkit." eyebrow="Step 5" icon={Wrench} theme={theme}>
              <p>The good news is you can train your brain to handle mistakes better and stay solid under pressure. It's a skill, not something you're born with. The first step is to <strong>stop treating mistakes like they mean something about you</strong>. They're information, not insults. Every error is basically a signpost pointing to exactly where you need to focus next.</p>
              <p>The most powerful tool for this is a <Highlight description="A simple notebook or page where you write down each mistake you make in practice, figure out why it happened (did you rush it, not understand it, or just forget something?), and write down one thing you'll do to fix it." theme={theme}>Mistake Log</Highlight>. Writing your mistakes down forces you to actually think about them properly instead of just cringing and moving on. It trains your brain to pay real attention to errors instead of flinching away from them. Don't just spot your mistakes — dig into them. They're the best study tool you have.</p>
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
