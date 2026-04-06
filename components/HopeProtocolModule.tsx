/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
*/

import React, { useState } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import {
  Zap, BookOpen, Shield, Cpu, Waypoints, Activity
} from 'lucide-react';
import { ModuleProgress } from '../types';
import { emeraldTheme } from '../moduleThemes';
import { Highlight, ReadingSection, MicroCommitment, ConceptCardGrid } from './ModuleShared';
import { ModuleLayout } from './ModuleLayout';
import { useNorthStar } from '../hooks/useNorthStar';
import NorthStarCallout from './NorthStarCallout';
import { COMPACT_CALLOUT_PLACEMENTS } from '../northStarData';

const theme = emeraldTheme;

// --- INTERACTIVE COMPONENTS ---

const HopeDiagnostic = () => {
  const myths = [
    { myth: "Hope is just wishful thinking.", fact: "FALSE. Hope is an active skill — it combines the drive to start (willpower) with a plan to get there (waypower)." },
    { myth: "You're either born hopeful or you're not.", fact: "FALSE. Hope is something you can practise and get better at. Your brain physically rewires itself the more you use it." },
    { myth: "Hope is the same as optimism.", fact: "FALSE. Optimism says 'things will work out.' Hope says 'I can MAKE things work out — and here's my plan.'" },
  ];
  return (
    <div className="my-10 rounded-2xl p-6 md:p-8 space-y-8" style={{ backgroundColor: '#F8F8F8', borderRadius: 18 }}>
      <h4 className="font-serif text-2xl font-semibold text-zinc-800 dark:text-white text-center">Hope Circuit Diagnostic</h4>
      <p className="text-center text-sm text-zinc-500 dark:text-zinc-400 -mt-4">Let's bust some common myths about where hope comes from.</p>
      <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
        {myths.map((item, i) => <MythBusterCard key={i} front={item.myth} back={item.fact} />)}
      </div>
    </div>
  );
}

interface MythBusterCardProps {
  front: string;
  back: string;
}

const MythBusterCard: React.FC<MythBusterCardProps> = ({ front, back }) => {
  const [isFlipped, setIsFlipped] = useState(false);
  return (
    <div className="w-full h-44 [perspective:1000px] cursor-pointer" onClick={() => setIsFlipped(!isFlipped)}>
      <motion.div className="relative w-full h-full" style={{ transformStyle: 'preserve-3d' }} animate={{ rotateX: isFlipped ? 180 : 0 }} transition={{ duration: 0.5, ease: [0.16, 1, 0.3, 1] }}>
        <div className="absolute w-full h-full [backface-visibility:hidden] rounded-xl p-6 flex flex-col items-center justify-center text-center" style={{ backgroundColor: '#FFFFFF', border: '2.5px solid #1C1917', borderRadius: 12, boxShadow: '3px 3px 0px 0px #1C1917' }}>
          <p className="text-sm font-semibold leading-snug text-zinc-700 dark:text-zinc-200">{front}</p>
          <p className="absolute bottom-3 right-4 text-[9px] font-medium tracking-wider text-zinc-300 dark:text-zinc-600 uppercase">Tap to reveal</p>
        </div>
        <div className="absolute w-full h-full [backface-visibility:hidden] rounded-xl p-5 flex flex-col items-center justify-center text-center" style={{ transform: 'rotateX(180deg)', backgroundColor: '#6EE7B7', border: '2.5px solid #059669', borderRadius: 12, boxShadow: '3px 3px 0px 0px #059669', color: '#064E3B' }}>
          <p className="text-xs font-semibold leading-snug">{back}</p>
        </div>
      </motion.div>
    </div>
  );
};

const BrainMismatchDiagram = () => (
  <div className="my-10 rounded-2xl p-6 md:p-8 flex flex-col items-center" style={{ backgroundColor: '#F8F8F8', borderRadius: 18 }}>
    <h4 className="font-serif text-2xl font-semibold text-zinc-800 dark:text-white text-center mb-2">Adolescent Brain: System Mismatch</h4>
    <p className="text-center text-sm text-zinc-500 dark:text-zinc-400 mb-12 max-w-md">Your emotional 'accelerator' is at full volume, while your rational 'brakes' are still being fine-tuned.</p>

    <div className="w-full max-w-sm h-56 flex justify-around items-end gap-8 px-4">
      {/* Limbic System Bar */}
      <div className="w-full flex flex-col items-center h-full">
        <div className="flex-grow w-16 bg-zinc-100 dark:bg-zinc-800 rounded-t-lg overflow-hidden relative">
          <motion.div
            className="absolute bottom-0 w-full bg-rose-500"
            initial={{ height: "90%" }}
            animate={{ height: ["90%", "95%", "90%"] }}
            transition={{ duration: 1.5, repeat: Infinity, ease: "easeInOut" }}
            style={{ boxShadow: '0 0 20px rgba(239, 68, 68, 0.5)' }}
          />
        </div>
        <div className="text-center mt-4">
          <p className="font-bold text-rose-600">Limbic System</p>
          <p className="text-xs text-zinc-500 dark:text-zinc-400">The Accelerator (Max Volume)</p>
        </div>
      </div>

      {/* Prefrontal Cortex Bar */}
      <div className="w-full flex flex-col items-center h-full">
        <div className="flex-grow w-16 bg-zinc-100 dark:bg-zinc-800 rounded-t-lg overflow-hidden relative">
          <motion.div
            className="absolute bottom-0 w-full bg-emerald-500"
            initial={{ height: "0%" }}
            animate={{ height: "30%" }}
            transition={{ duration: 2, delay: 0.5, ease: "easeOut" }}
          />
           <motion.div
            className="absolute bottom-0 w-full h-[30%] bg-white dark:bg-zinc-800"
            initial={{ opacity: 0 }}
            animate={{ opacity: [0, 0.5, 0] }}
            transition={{ duration: 1, repeat: Infinity, ease: "easeInOut", delay: 1 }}
          />
        </div>
        <div className="text-center mt-4">
          <p className="font-bold text-emerald-600">Prefrontal Cortex</p>
          <p className="text-xs text-zinc-500 dark:text-zinc-400">The Brakes (Fine-Tuning)</p>
        </div>
      </div>
    </div>
  </div>
);

const DopamineDial = () => {
  const [motivation, setMotivation] = useState(10);
  const [choice, setChoice] = useState<'none' | 'cold' | 'hot'>('none');

  const handleChoice = (type: 'cold' | 'hot') => {
    setChoice(type);
    setMotivation(type === 'cold' ? 30 : 90);
  };

  const radius = 60;
  const circumference = Math.PI * radius; // Semicircle
  const offset = circumference - (motivation / 100) * circumference;

  return (
    <div className="my-10 rounded-2xl p-6 md:p-8" style={{ backgroundColor: '#F8F8F8', borderRadius: 18 }}>
      <h4 className="font-serif text-2xl font-semibold text-zinc-800 dark:text-white text-center">Interactive: The Dopamine Dial</h4>
      <p className="text-center text-sm text-zinc-500 dark:text-zinc-400 mb-8">Scenario: You need to study for a history exam. Choose your thought process.</p>

      <div className="w-full flex justify-center items-end h-24">
        <svg width="160" height="80" viewBox="0 0 160 80" className="overflow-visible">
          <path d="M 20 80 A 60 60 0 0 1 140 80" fill="none" stroke="#e5e7eb" strokeWidth="15" strokeLinecap="round" />
          <motion.path
            d="M 20 80 A 60 60 0 0 1 140 80"
            fill="none"
            stroke="url(#grad)"
            strokeWidth="15"
            strokeLinecap="round"
            strokeDasharray={circumference}
            initial={{ strokeDashoffset: circumference }}
            animate={{ strokeDashoffset: offset }}
            transition={{ type: "spring", damping: 15, stiffness: 100 }}
          />
          <defs>
            <linearGradient id="grad" x1="0%" y1="0%" x2="100%" y2="0%">
              <stop offset="0%" style={{stopColor: "#34d399", stopOpacity:1}} />
              <stop offset="100%" style={{stopColor: "#10b981", stopOpacity:1}} />
            </linearGradient>
          </defs>
        </svg>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-4 mt-8">
        <button onClick={() => handleChoice('cold')} className="p-4 rounded-xl text-left text-sm font-medium" style={{ backgroundColor: choice === 'cold' ? '#FCA5A5' : '#FFFFFF', border: `2.5px solid ${choice === 'cold' ? '#DC2626' : '#1C1917'}`, borderRadius: 14, boxShadow: choice === 'cold' ? 'none' : '3px 3px 0px 0px #1C1917', color: choice === 'cold' ? '#7F1D1D' : '#1C1917' }}><strong>"Cold" Cognition:</strong> "I need to study history."</button>
        <button onClick={() => handleChoice('hot')} className="p-4 rounded-xl text-left text-sm font-medium" style={{ backgroundColor: choice === 'hot' ? '#6EE7B7' : '#FFFFFF', border: `2.5px solid ${choice === 'hot' ? '#059669' : '#1C1917'}`, borderRadius: 14, boxShadow: choice === 'hot' ? 'none' : '3px 3px 0px 0px #1C1917', color: choice === 'hot' ? '#064E3B' : '#1C1917' }}><strong>"Hot" Cognition (EFT):</strong> "Imagine acing that exam..."</button>
      </div>

      <AnimatePresence>
        {choice !== 'none' && (
          <motion.div
            initial={{opacity:0, y:10}}
            animate={{opacity:1, y:0}}
            className="mt-8 p-6 rounded-xl"
            style={{
              backgroundColor: choice === 'cold' ? '#FCA5A5' : '#6EE7B7',
              border: `2.5px solid ${choice === 'cold' ? '#DC2626' : '#059669'}`,
              boxShadow: `3px 3px 0px 0px ${choice === 'cold' ? '#DC2626' : '#059669'}`,
            }}
          >
            {choice === 'cold' && <p style={{ color: '#7F1D1D' }}><strong>Result:</strong> A small motivational increase. The task is abstract and lacks an immediate reward signal for your brain.</p>}
            {choice === 'hot' && <p style={{ color: '#064E3B' }}><strong>Result:</strong> Major dopamine boost! Vividly simulating future success makes the reward feel real <em>now</em>, flooding your brain with the motivation to start.</p>}
          </motion.div>
        )}
      </AnimatePresence>
    </div>
  );
};

const HopeMap = () => {
  const [step, setStep] = useState(0);
  const [goal, setGoal] = useState('');
  const [pathway, setPathway] = useState('');
  const [obstacle, setObstacle] = useState('');
  const [solution, setSolution] = useState('');

  const steps = [
    { label: 'Goal', prompt: 'What is your goal?', hint: 'Be specific. Not "do well in Maths" but "Get a H2 in Leaving Cert Maths by June."' },
    { label: 'Pathway', prompt: 'What is your first route to get there?', hint: 'The first concrete step or strategy. e.g., "Complete 3 past papers per week starting in January."' },
    { label: 'Obstacle', prompt: 'What could block this pathway?', hint: 'Be honest. What is the most likely thing to derail you? e.g., "I lose motivation after a bad result."' },
    { label: 'Solution', prompt: 'How will you get around it?', hint: 'Pre-load the fix. e.g., "If I get a bad result, I will review my mistakes and adjust my plan, not quit."' },
  ];

  const values = [goal, pathway, obstacle, solution];
  const setters = [setGoal, setPathway, setObstacle, setSolution];
  const canAdvance = values[step]?.trim().length > 0;
  const isComplete = step === 4;

  return (
    <div className="my-10 rounded-2xl p-6 md:p-8" style={{ backgroundColor: '#F8F8F8', borderRadius: 18 }}>
      <h4 className="font-serif text-2xl font-semibold text-zinc-800 dark:text-white text-center">My Hope Circuit Blueprint</h4>
      <p className="text-center text-sm text-zinc-500 dark:text-zinc-400 mb-8">Build your circuit one component at a time.</p>

      {/* Progress dots */}
      <div className="flex justify-center gap-2 mb-8">
        {steps.map((s, i) => (
          <div key={i} className="flex items-center gap-2">
            <div
              className="w-8 h-8 flex items-center justify-center text-xs font-bold transition-all duration-300"
              style={{
                borderRadius: 10,
                backgroundColor: i < step || isComplete ? '#059669' : i === step && !isComplete ? '#6EE7B7' : '#E5E7EB',
                border: `2px solid ${i < step || isComplete ? '#047857' : i === step && !isComplete ? '#059669' : '#D1D5DB'}`,
                boxShadow: i < step || isComplete || (i === step && !isComplete) ? '2px 2px 0px 0px #047857' : '2px 2px 0px 0px #D1D5DB',
                color: i < step || isComplete ? '#fff' : i === step && !isComplete ? '#064E3B' : '#9CA3AF',
              }}
            >
              {i < step || isComplete ? '✓' : i + 1}
            </div>
            {i < steps.length - 1 && (
              <div className="w-8 h-0.5 transition-all duration-300" style={{ backgroundColor: i < step || isComplete ? '#059669' : '#E5E7EB' }} />
            )}
          </div>
        ))}
      </div>

      <AnimatePresence mode="wait">
        {!isComplete ? (
          <motion.div
            key={step}
            initial={{ opacity: 0, x: 20 }}
            animate={{ opacity: 1, x: 0 }}
            exit={{ opacity: 0, x: -20 }}
            transition={{ duration: 0.3 }}
            className="space-y-4"
          >
            <p className="text-xs font-semibold text-emerald-600 uppercase tracking-wider">{steps[step].label}</p>
            <p className="font-serif text-xl font-semibold text-zinc-800 dark:text-white">{steps[step].prompt}</p>
            <p className="text-sm text-zinc-500 dark:text-zinc-400">{steps[step].hint}</p>
            <input
              value={values[step]}
              onChange={(e) => setters[step](e.target.value)}
              placeholder="Type your answer here..."
              className="w-full bg-white dark:bg-zinc-800 rounded-xl px-5 py-3.5 text-sm font-medium text-zinc-800 dark:text-white placeholder-zinc-400 outline-none"
              style={{ border: '1.5px solid #E7E5E4' }}
              autoFocus
            />
            <div className="flex justify-between items-center pt-2">
              <button
                onClick={() => setStep(step - 1)}
                className={`text-sm font-medium text-zinc-400 hover:text-zinc-600 transition-colors ${step === 0 ? 'invisible' : ''}`}
              >
                Back
              </button>
              <button
                onClick={() => setStep(step + 1)}
                disabled={!canAdvance}
                className={`px-6 py-2.5 rounded-xl text-sm font-bold transition-all ${
                  canAdvance
                    ? 'bg-emerald-500 text-white hover:bg-emerald-600 shadow-lg shadow-emerald-500/20'
                    : 'bg-zinc-100 dark:bg-zinc-700 text-zinc-400 cursor-not-allowed'
                }`}
              >
                {step === 3 ? 'Complete Blueprint' : 'Next'}
              </button>
            </div>
          </motion.div>
        ) : (
          <motion.div
            key="complete"
            initial={{ opacity: 0, scale: 0.95 }}
            animate={{ opacity: 1, scale: 1 }}
            transition={{ duration: 0.4 }}
            className="space-y-4"
          >
            <div className="bg-white dark:bg-zinc-900 rounded-2xl" style={{ border: '2.5px solid #1C1917', boxShadow: '4px 4px 0px 0px #1C1917', padding: '24px 28px' }}>
              {/* Step 1: Power Source */}
              <div className="flex items-start gap-4">
                <div className="w-11 h-11 shrink-0 flex items-center justify-center" style={{ backgroundColor: '#FCD34D', border: '2px solid #D97706', borderRadius: 12, boxShadow: '2px 2px 0px 0px #D97706' }}>
                  <Zap size={18} style={{ color: '#78350F' }} />
                </div>
                <div className="pt-0.5">
                  <p className="text-[10px] uppercase tracking-wider font-semibold" style={{ color: '#78716C' }}>The Power Source</p>
                  <p className="font-serif font-semibold text-zinc-900 dark:text-white mt-0.5">{goal}</p>
                </div>
              </div>
              <div className="h-5 flex items-center" style={{ marginLeft: 21 }}><div className="w-0.5 h-full bg-zinc-200 dark:bg-zinc-700" /></div>

              {/* Step 2: Wiring */}
              <div className="flex items-start gap-4">
                <div className="w-11 h-11 shrink-0 flex items-center justify-center" style={{ backgroundColor: '#93C5FD', border: '2px solid #2563EB', borderRadius: 12, boxShadow: '2px 2px 0px 0px #2563EB' }}>
                  <Waypoints size={18} style={{ color: '#1E3A8A' }} />
                </div>
                <div className="pt-0.5">
                  <p className="text-[10px] uppercase tracking-wider font-semibold" style={{ color: '#78716C' }}>The Wiring</p>
                  <p className="font-serif font-semibold text-zinc-900 dark:text-white mt-0.5">{pathway}</p>
                </div>
              </div>
              <div className="h-5 flex items-center" style={{ marginLeft: 21 }}><div className="w-0.5 h-full bg-zinc-200 dark:bg-zinc-700" /></div>

              {/* Step 3: Short Circuit */}
              <div className="flex items-start gap-4">
                <div className="w-11 h-11 shrink-0 flex items-center justify-center" style={{ backgroundColor: '#FCA5A5', border: '2px solid #DC2626', borderRadius: 12, boxShadow: '2px 2px 0px 0px #DC2626' }}>
                  <Shield size={18} style={{ color: '#7F1D1D' }} />
                </div>
                <div className="pt-0.5">
                  <p className="text-[10px] uppercase tracking-wider font-semibold" style={{ color: '#78716C' }}>Short Circuit</p>
                  <p className="font-serif font-semibold text-zinc-900 dark:text-white mt-0.5">{obstacle}</p>
                </div>
              </div>
              <div className="h-5 flex items-center" style={{ marginLeft: 21 }}><div className="w-0.5 h-full bg-zinc-200 dark:bg-zinc-700" /></div>

              {/* Step 4: The Fix */}
              <div className="flex items-start gap-4">
                <div className="w-11 h-11 shrink-0 flex items-center justify-center" style={{ backgroundColor: '#6EE7B7', border: '2px solid #059669', borderRadius: 12, boxShadow: '2px 2px 0px 0px #059669' }}>
                  <Activity size={18} style={{ color: '#064E3B' }} />
                </div>
                <div className="pt-0.5">
                  <p className="text-[10px] uppercase tracking-wider font-semibold" style={{ color: '#78716C' }}>The Fix</p>
                  <p className="font-serif font-semibold text-zinc-900 dark:text-white mt-0.5">{solution}</p>
                </div>
              </div>
            </div>
            <button
              onClick={() => { setStep(0); setGoal(''); setPathway(''); setObstacle(''); setSolution(''); }}
              className="w-full text-center text-sm font-medium text-zinc-400 hover:text-zinc-600 hover:underline transition-colors pt-2"
            >
              Start a new blueprint
            </button>
          </motion.div>
        )}
      </AnimatePresence>
    </div>
  );
};

const CortisolSimulator = () => {
  const [responseType, setResponseType] = useState<'neutral' | 'low-hope' | 'high-hope'>('neutral');
  const pathData = {
    neutral: "M0,50 C40,50 60,10 100,10 L250,10 C300,10 320,80 400,90",
    'low-hope': "M0,50 C40,50 60,10 100,10 L250,10 C300,10 320,20 400,20",
    'high-hope': "M0,50 C40,50 60,10 100,10 L250,10 C300,10 320,70 400,80",
  }
  return (
     <div className="my-10 rounded-2xl p-6 md:p-8" style={{ backgroundColor: '#F8F8F8', borderRadius: 18 }}>
        <h4 className="font-serif text-2xl font-semibold text-zinc-800 dark:text-white text-center">Cortisol Curve Simulator</h4>
        <p className="text-center text-sm text-zinc-500 dark:text-zinc-400 mb-2">Stressor Detected: Bad Mock Exam Result.</p>
        <p className="text-center text-sm text-zinc-500 dark:text-zinc-400 mb-8">How does your system respond?</p>
        <div className="bg-zinc-50/50 p-6 rounded-xl">
          <svg viewBox="0 0 400 100" className="w-full h-auto">
            <AnimatePresence>
            <motion.path
              key={responseType}
              d={pathData[responseType]}
              fill="none"
              stroke={responseType === 'low-hope' ? '#ef4444' : '#10b981'}
              strokeWidth="3"
              initial={{ pathLength: 0 }}
              animate={{ pathLength: 1 }}
              transition={{ duration: 1.5, ease: 'easeInOut' }}
              strokeLinecap="round"
            />
            </AnimatePresence>
             <text x="5" y="15" fontSize="8" fill="#9ca3af">High Cortisol</text>
             <text x="5" y="95" fontSize="8" fill="#9ca3af">Low Cortisol</text>
          </svg>
        </div>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4 mt-6">
          <button onClick={() => setResponseType('low-hope')} className="p-4 bg-rose-50 border border-rose-200 rounded-xl text-left text-sm"><strong>Low-Hope Response:</strong> "This is pointless, I'm just bad at this subject." <span className="block text-xs text-rose-500 mt-1">Result: Flattened cortisol curve, prolonged stress.</span></button>
          <button onClick={() => setResponseType('high-hope')} className="p-4 bg-emerald-50 border border-emerald-200 rounded-xl text-left text-sm"><strong>High-Hope Response:</strong> "Okay, that didn't work. What's a new plan I can try?" <span className="block text-xs text-emerald-500 mt-1">Result: Healthy cortisol recovery, stress buffered.</span></button>
        </div>
     </div>
  );
}

// --- MODULE COMPONENT ---
const HopeProtocolModule: React.FC<{ onBack: () => void; progress: ModuleProgress; onProgressUpdate: (progress: ModuleProgress) => void }> = ({ onBack, progress, onProgressUpdate }) => {
  const { northStar } = useNorthStar();
  const sections = [
    { id: 'schematic', title: 'The Schematic: De-Coding Hope', eyebrow: '01 // The Blueprint', icon: BookOpen },
    { id: 'circuit-board', title: "Your Brain's Circuit Board", eyebrow: '02 // The Hardware', icon: Cpu },
    { id: 'willpower', title: "Powering Up: The Science of 'Willpower'", eyebrow: '03 // The Voltage', icon: Zap },
    { id: 'waypower', title: "Designing the Wires: The Art of 'Waypower'", eyebrow: '04 // The Wiring', icon: Waypoints },
    { id: 'stress-shield', title: 'Stress Shield: Your Surge Protector', eyebrow: '05 // System Protection', icon: Shield },
    { id: 'upgrade', title: 'Upgrading the Hardware', eyebrow: '06 // System Upgrade', icon: Activity },
  ];

  return (
    <ModuleLayout
      moduleNumber="02"
      moduleTitle="The Science of Hope"
      moduleSubtitle="Your Brain's Engineering Manual"
      moduleDescription="Hope isn't wishful thinking — it's a skill you can train. Learn how your brain creates motivation and how to get it working for you."
      theme={theme}
      sections={sections}
      onBack={onBack}
      progress={progress}
      onProgressUpdate={onProgressUpdate}
      finishButtonText="Ignite Your Hope"
    >
      {(activeSection) => (
        <>
          {activeSection === 0 && (
            <ReadingSection title="The Schematic: De-Coding Hope." eyebrow="Step 1" icon={BookOpen} theme={theme}>
              <p>Forget everything you think you know about hope. It's not a fluffy feeling or wishful thinking. Hope is actually a skill — a way of thinking that you can learn, practise, and get seriously good at. Think of it as the engineering manual for your brain's motivation system.</p>
              <p>The formula is simple: Hope = Goals + <Highlight description="Your willpower — the raw 'I can do this' energy that gets you off the couch and started. It's the spark that fires up your engine." theme={theme}>Agency</Highlight> + <Highlight description="Your waypower — the ability to come up with a plan, think of backup routes, and adapt when things go sideways. It's the sat-nav that keeps you on course." theme={theme}>Pathways</Highlight>. A quick diagnostic can help you see where your own circuit is strong and where it might need work.</p>
              <HopeDiagnostic />
              <MicroCommitment theme={theme}>
                <p>Think of one vague goal you have (e.g., 'do better in French'). Open the notes app on your phone and re-write it as a clear, specific goal (e.g., 'Learn 10 new French vocabulary words by tomorrow evening').</p>
              </MicroCommitment>
            </ReadingSection>
          )}
           {activeSection === 1 && (
            <ReadingSection title="Your Brain's Circuit Board." eyebrow="Step 2" icon={Cpu} theme={theme}>
              <p>Your brain right now is a high-tech circuit board undergoing a massive upgrade. But here's the catch: not all parts get upgraded at the same speed. This creates a <Highlight description="Your emotional brain (the accelerator) is already at full power, but your planning brain (the brakes) is still being built. That's why you can desperately want something but struggle to plan how to get it. It's not a flaw — it's just where your brain is at right now." theme={theme}>Developmental Mismatch</Highlight>.</p>
              <p>Your <Highlight description="The emotional engine room of your brain. It's what drives your desire for rewards, your excitement, and your impulses. In your teens, it's turned up to maximum — which gives you massive energy and motivation." theme={theme}>Limbic System</Highlight> (your 'accelerator') is already at full power, giving you huge amounts of energy and drive. But your <Highlight description="The planning department of your brain, right behind your forehead. It handles long-term thinking, impulse control, and problem-solving. It's still under construction until your mid-20s — which is why planning feels harder than wanting." theme={theme}>Prefrontal Cortex (PFC)</Highlight> (your 'brakes' and 'Sat-Nav') is still being built. This means your desire to succeed often outstrips your brain's ability to plan the route, leading to frustration. This isn't a character flaw — it's biology. Your job is to become a conscious engineer of this system.</p>
              <BrainMismatchDiagram />
               <MicroCommitment theme={theme}>
                <p>Next time you feel a strong impulse to procrastinate, just notice it. Say to yourself, "That's my limbic system." Don't judge it, just label it. This simple act of noticing engages your PFC.</p>
              </MicroCommitment>
            </ReadingSection>
          )}
           {activeSection === 2 && (
            <ReadingSection title="Powering Up: The Science of 'Willpower'." eyebrow="Step 3" icon={Zap} theme={theme}>
                <p>Agency — your willpower — is the electrical current in your Hope Circuit. It's the force that gets you to actually start. And it's not just about 'trying hard'; your brain has a specific chemical for this called <Highlight description="Your brain's motivation chemical. It's what makes you feel driven and excited about goals. The trick is: you can learn to trigger it on demand by vividly imagining your future success." theme={theme}>Dopamine</Highlight>.</p>
                <p>Here's the key: there's a huge difference between "cold" and "hot" thinking. "Cold" thinking is vague and abstract ("I should study"). "Hot" thinking — or <Highlight description="Imagining your future so vividly that it feels real. Picture yourself walking out of the exam hall, relieved and proud. That vivid image fires up your brain's reward system right now, giving you the motivation to start." theme={theme}>Episodic Future Thinking</Highlight> — is vivid and emotional ("I can see myself walking out of that exam hall, relieved and proud"). That vivid image fires up your brain's reward system and gives you a real motivational boost. You can literally learn to generate your own voltage.</p>
                <DopamineDial />
                <MicroCommitment theme={theme}>
                    <p>Before you start studying tonight, take 60 seconds. Close your eyes and vividly imagine the feeling of relief and pride after you finish. You're practicing Episodic Future Thinking and giving your brain a small, upfront hit of dopamine.</p>
                </MicroCommitment>
            </ReadingSection>
          )}
          {activeSection === 3 && (
            <ReadingSection title="Designing the Wires: The Art of 'Waypower'." eyebrow="Step 4" icon={Waypoints} theme={theme}>
              {northStar && (() => { const p = COMPACT_CALLOUT_PLACEMENTS.find(p => p.moduleId === 'hope-protocol'); return p ? <NorthStarCallout northStar={northStar} variant="compact" message={p.message} /> : null; })()}
              <p>If Agency is the raw power, Pathways thinking is the wiring that directs it. It's the most important — and for teens, the hardest — part of the Hope Circuit, because it relies on the part of your brain that's still being built.</p>
              <p>Good waypower comes down to three skills.</p>
              <ConceptCardGrid
                cards={[
                  { number: 1, term: "Planning", description: "Breaking a big goal into small steps." },
                  { number: 2, term: "Flexibility", description: "Having backup routes when the first path doesn't work out." },
                  { number: 3, term: "Problem-Solving", description: "Seeing obstacles before they hit you and pre-loading solutions." },
                ]}
              />
              <p>The Hope Map below trains exactly this. It forces you to design your circuit before you turn on the power — and pre-loads solutions so failure doesn't knock you off course.</p>
              <HopeMap />
              <MicroCommitment theme={theme}>
                <p>Map out one tiny goal for tomorrow using the Goal-Pathway-Obstacle format. E.g., Goal: Get homework done by 8 pm. Pathway: Start at 6 pm in the kitchen. Obstacle: My brother will be noisy. Solution: Put on headphones.</p>
              </MicroCommitment>
            </ReadingSection>
          )}
           {activeSection === 4 && (
            <ReadingSection title="Stress Shield: Your Surge Protector." eyebrow="Step 5" icon={Shield} theme={theme}>
              <p>Hopelessness isn't just a feeling — it has a physical effect on your body. When you face a threat (like a looming exam), your brain's alarm system — your <Highlight description="Your body's built-in stress alarm. When danger is detected, it fires off a chain reaction of hormones that flood you with stress chemicals. Useful if you're running from a bear. Less useful the night before your Maths paper." theme={theme}>Stress Response System</Highlight> — goes off, flooding you with the stress hormone <Highlight description="Your body's stress chemical. A short burst helps you focus, but when it stays high for too long, it messes with your memory, your sleep, and your ability to think clearly. Basically, it shuts down the exact brain functions you need for exams." theme={theme}>Cortisol</Highlight>.</p>
              <p>Here's the good news: hope acts as a built-in surge protector. When you have a clear goal and a plan, your brain sees a tough exam as a problem to solve — not a disaster. That lowers your stress levels and keeps your thinking brain online when you need it most. See for yourself how a hopeful response can physically change the stress in your body.</p>
              <CortisolSimulator/>
              <MicroCommitment theme={theme}>
                <p>The next time you feel exam stress, consciously name the feeling ('I am feeling stressed about Maths'). Acknowledging the signal is the first step any engineer takes to regulate a system.</p>
              </MicroCommitment>
            </ReadingSection>
          )}
           {activeSection === 5 && (
            <ReadingSection title="Upgrading the Hardware." eyebrow="Step 6" icon={Activity} theme={theme}>
              <p>Here's the most powerful idea in this entire unit: your brain's wiring isn't fixed. Every time you practise planning, goal-setting, or problem-solving, you physically strengthen the connections in your brain. This is called <Highlight description="Your brain's ability to rewire itself based on what you practise. Like a path through a field — the more you walk it, the clearer it gets. Every time you plan, set goals, or solve problems, you're literally building a stronger brain." theme={theme}>Neuroplasticity</Highlight>. The <Highlight description="The major highway inside your brain that connects your planning centre to the rest of your thinking systems. The more you use it, the faster and stronger it gets — like upgrading from a country road to a motorway." theme={theme}>Planning Highways</Highlight> in your brain work like muscles: the more you use them, the stronger they get.</p>
              <p>This means every time you make a Hope Map or break down a big task, you're not just getting work done — you're physically upgrading your brain. One of the best ways to train this is the 'Stop-Think' Protocol: a manual override for your brain's autopilot that forces you to engage the Hope Circuit.</p>
               <MicroCommitment theme={theme}>
                <p>Put a reminder on your phone for halfway through your study time tonight that just says 'STOP-THINK'. When it goes off, take 60 seconds to ask: "Is what I'm doing now the most effective way to reach my goal?"</p>
              </MicroCommitment>
            </ReadingSection>
          )}
        </>
      )}
    </ModuleLayout>
  );
};
export default HopeProtocolModule;
