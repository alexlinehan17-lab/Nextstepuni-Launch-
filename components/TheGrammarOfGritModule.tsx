/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
*/

import React, { useState } from 'react';
import { motion } from 'framer-motion';
import {
  Shield, HeartCrack, Recycle, Mic, Wrench
} from 'lucide-react';
import { ModuleProgress } from '../types';
import { blueTheme } from '../moduleThemes';
import { Highlight, ReadingSection, MicroCommitment } from './ModuleShared';
import { ModuleLayout } from './ModuleLayout';

const theme = blueTheme;

// --- INTERACTIVE COMPONENTS ---

const MotionDiv = motion.div as any;

const ThoughtReframer = () => {
  const [thought, setThought] = useState('');
  const [personal, setPersonal] = useState(false);
  const [pervasive, setPervasive] = useState(false);
  const [permanent, setPermanent] = useState(false);

  const optimisticCount = [personal, pervasive, permanent].filter(Boolean).length;
  const resiliencePercent = Math.round((optimisticCount / 3) * 100);

  const getReframedThought = () => {
    if (!thought.trim()) return null;
    if (optimisticCount === 0) return thought;
    if (optimisticCount === 3) {
      return `My approach to "${thought.trim()}" isn't working yet — but it's one specific area I can improve with the right strategy.`;
    }
    const parts: string[] = [];
    if (personal) {
      parts.push('it\'s about the situation, not me');
    }
    if (pervasive) {
      parts.push('it\'s only this one area');
    }
    if (permanent) {
      parts.push('it\'s temporary');
    }
    return `"${thought.trim()}" — but ${parts.join(', and ')}.`;
  };

  const reframedThought = getReframedThought();

  const thoughtColorClass =
    optimisticCount === 0
      ? 'text-rose-600 dark:text-rose-400'
      : optimisticCount === 3
        ? 'text-emerald-600 dark:text-emerald-400'
        : 'text-amber-600 dark:text-amber-400';

  const barColorClass =
    optimisticCount === 0
      ? 'bg-rose-500'
      : optimisticCount === 3
        ? 'bg-emerald-500'
        : 'bg-amber-500';

  const toggleItems: {
    label: string;
    pessimistic: string;
    optimistic: string;
    value: boolean;
    onToggle: () => void;
  }[] = [
    {
      label: 'Personal → Specific',
      pessimistic: "It's about me",
      optimistic: "It's about this situation",
      value: personal,
      onToggle: () => setPersonal(!personal),
    },
    {
      label: 'Pervasive → Limited',
      pessimistic: 'It affects everything',
      optimistic: "It's just this one area",
      value: pervasive,
      onToggle: () => setPervasive(!pervasive),
    },
    {
      label: 'Permanent → Temporary',
      pessimistic: 'It will always be this way',
      optimistic: "It's temporary",
      value: permanent,
      onToggle: () => setPermanent(!permanent),
    },
  ];

  return (
    <div className="my-10 p-8 md:p-12 bg-white dark:bg-zinc-800 rounded-xl border border-zinc-200 dark:border-zinc-700">
      <h4 className="font-serif text-2xl font-semibold text-zinc-800 dark:text-white text-center">
        Thought Reframer
      </h4>
      <p className="text-center text-sm text-zinc-500 dark:text-zinc-400 mt-2 mb-8">
        Type a negative thought, then flip the 3 Ps to rewrite the script.
      </p>

      {/* Input */}
      <div className="mb-8">
        <input
          type="text"
          value={thought}
          onChange={(e) => setThought(e.target.value)}
          placeholder={"e.g. I'm terrible at maths"}
          className="w-full px-5 py-4 rounded-xl border border-zinc-300 dark:border-zinc-600 bg-zinc-50 dark:bg-zinc-900 text-zinc-800 dark:text-white placeholder-zinc-400 dark:placeholder-zinc-500 text-base focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-all"
        />
      </div>

      {/* Toggles */}
      <div className="space-y-6 mb-8">
        {toggleItems.map((item) => (
          <div key={item.label} className="flex flex-col items-center gap-2">
            <span className="text-xs font-bold uppercase tracking-wider text-blue-600 dark:text-blue-400">
              {item.label}
            </span>
            <div className="flex items-center gap-4">
              <span
                className={`text-xs font-medium text-right w-40 sm:w-48 shrink-0 transition-colors ${
                  !item.value
                    ? 'text-rose-600 dark:text-rose-400 font-bold'
                    : 'text-zinc-400 dark:text-zinc-500'
                }`}
              >
                {item.pessimistic}
              </span>
              <button
                onClick={item.onToggle}
                className={`relative w-14 h-7 rounded-full shrink-0 transition-colors duration-300 focus:outline-none focus:ring-2 focus:ring-blue-500 ${
                  item.value ? 'bg-emerald-500' : 'bg-rose-500'
                }`}
                aria-label={`Toggle ${item.label}`}
              >
                <MotionDiv
                  className="absolute top-0.5 w-6 h-6 rounded-full bg-white shadow-md"
                  animate={{ left: item.value ? '1.75rem' : '0.125rem' }}
                  transition={{ type: 'spring', stiffness: 500, damping: 30 }}
                />
              </button>
              <span
                className={`text-xs font-medium text-left w-40 sm:w-48 shrink-0 transition-colors ${
                  item.value
                    ? 'text-emerald-600 dark:text-emerald-400 font-bold'
                    : 'text-zinc-400 dark:text-zinc-500'
                }`}
              >
                {item.optimistic}
              </span>
            </div>
          </div>
        ))}
      </div>

      {/* Reframed thought display */}
      {thought.trim() && reframedThought && (
        <MotionDiv
          key={optimisticCount}
          initial={{ opacity: 0, y: 8 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.4 }}
          className="mb-8 p-5 rounded-xl bg-zinc-50 dark:bg-zinc-900 border border-zinc-200 dark:border-zinc-700"
        >
          <p className="text-xs font-bold uppercase tracking-wider text-zinc-400 dark:text-zinc-500 mb-2">
            {optimisticCount === 0
              ? 'Pessimistic Framing'
              : optimisticCount === 3
                ? 'Optimistic Reframe'
                : 'Partially Reframed'}
          </p>
          <p className={`text-base font-medium italic ${thoughtColorClass}`}>
            {reframedThought}
          </p>
          {optimisticCount === 3 && (
            <MotionDiv
              initial={{ scale: 0, opacity: 0 }}
              animate={{ scale: 1, opacity: 1 }}
              transition={{ delay: 0.2, type: 'spring', stiffness: 400, damping: 15 }}
              className="mt-3 text-center text-emerald-600 dark:text-emerald-400 text-sm font-bold"
            >
              All 3 Ps reframed — you have full control of the narrative.
            </MotionDiv>
          )}
        </MotionDiv>
      )}

      {/* Resilience Score bar */}
      <div>
        <div className="flex items-center justify-between mb-2">
          <span className="text-xs font-bold uppercase tracking-wider text-zinc-500 dark:text-zinc-400">
            Resilience Score
          </span>
          <span className={`text-sm font-bold ${thoughtColorClass}`}>
            {resiliencePercent}%
          </span>
        </div>
        <div className="w-full h-3 bg-zinc-200 dark:bg-zinc-700 rounded-full overflow-hidden">
          <MotionDiv
            className={`h-full rounded-full ${barColorClass}`}
            initial={{ width: '0%' }}
            animate={{
              width:
                resiliencePercent === 0
                  ? '0%'
                  : resiliencePercent === 33
                    ? '33%'
                    : resiliencePercent === 67
                      ? '67%'
                      : '100%',
            }}
            transition={{ duration: 0.5, ease: 'easeOut' }}
          />
        </div>
      </div>
    </div>
  );
};

const ExplanatoryStyleQuiz = () => {
    const [answers, setAnswers] = useState<( 'pessimistic' | 'optimistic' | null)[]>([null, null, null]);
    const score = answers.filter(a => a === 'optimistic').length;

    const handleAnswer = (index: number, type: 'pessimistic' | 'optimistic') => {
      const newAnswers = [...answers];
      newAnswers[index] = type;
      setAnswers(newAnswers);
    };

    const isComplete = answers.every(a => a !== null);

    return (
      <div className="my-10 p-8 md:p-12 bg-white dark:bg-zinc-800 rounded-xl border border-zinc-200 dark:border-zinc-700">
        <h4 className="font-serif text-2xl font-semibold text-zinc-800 dark:text-white text-center">Self-Talk Diagnostic</h4>
        <p className="text-center text-sm text-zinc-500 dark:text-zinc-400 mb-8">You fail a test. Which voice is louder in your head?</p>
        <div className="space-y-6">
            <div>
                <p className="text-center font-bold mb-2">"This means I'm stupid." vs "This means my strategy was wrong."</p>
                <div className="grid grid-cols-2 gap-3"><button onClick={() => handleAnswer(0, 'pessimistic')} className={`p-4 rounded-xl border ${answers[0] === 'pessimistic' ? 'bg-rose-500 text-white' : 'bg-zinc-50'}`}>A</button><button onClick={() => handleAnswer(0, 'optimistic')} className={`p-4 rounded-xl border ${answers[0] === 'optimistic' ? 'bg-emerald-500 text-white' : 'bg-zinc-50'}`}>B</button></div>
            </div>
             <div>
                <p className="text-center font-bold mb-2">"I'll never get this." vs "I'll try again tomorrow."</p>
                <div className="grid grid-cols-2 gap-3"><button onClick={() => handleAnswer(1, 'pessimistic')} className={`p-4 rounded-xl border ${answers[1] === 'pessimistic' ? 'bg-rose-500 text-white' : 'bg-zinc-50'}`}>A</button><button onClick={() => handleAnswer(1, 'optimistic')} className={`p-4 rounded-xl border ${answers[1] === 'optimistic' ? 'bg-emerald-500 text-white' : 'bg-zinc-50'}`}>B</button></div>
            </div>
             <div>
                <p className="text-center font-bold mb-2">"This ruins everything." vs "This is just one subject."</p>
                <div className="grid grid-cols-2 gap-3"><button onClick={() => handleAnswer(2, 'pessimistic')} className={`p-4 rounded-xl border ${answers[2] === 'pessimistic' ? 'bg-rose-500 text-white' : 'bg-zinc-50'}`}>A</button><button onClick={() => handleAnswer(2, 'optimistic')} className={`p-4 rounded-xl border ${answers[2] === 'optimistic' ? 'bg-emerald-500 text-white' : 'bg-zinc-50'}`}>B</button></div>
            </div>
        </div>
         {isComplete && <p className="text-center mt-4 text-sm font-bold">{score > 1 ? <span className="text-emerald-600">Your explanatory style is optimistic and builds resilience.</span> : <span className="text-rose-600">Your explanatory style is pessimistic and may be eroding your resilience.</span>}</p>}
      </div>
    );
};

// --- MODULE COMPONENT ---
const TheGrammarOfGritModule: React.FC<{ onBack: () => void; progress: ModuleProgress; onProgressUpdate: (progress: ModuleProgress) => void }> = ({ onBack, progress, onProgressUpdate }) => {
  const sections = [
    { id: 'internal-narrator', title: 'Your Internal Narrator', eyebrow: '01 // The Source Code', icon: Mic },
    { id: 'three-ps', title: 'The 3 Ps of Failure', eyebrow: '02 // Personal, Pervasive, Permanent', icon: HeartCrack },
    { id: 'rewrite-protocol', title: 'The Re-Write Protocol', eyebrow: '03 // From Fragile to Agile', icon: Recycle },
    { id: 'self-compassion', title: 'The Role of Self-Compassion', eyebrow: '04 // The Antidote to Shame', icon: Shield },
    { id: 'blueprint', title: 'Your Resilience Blueprint', eyebrow: '05 // The Action Plan', icon: Wrench },
  ];

  return (
    <ModuleLayout
      moduleNumber="05"
      moduleTitle="The Grammar of Grit"
      moduleSubtitle="The Language of Resilience Protocol"
      moduleDescription="Discover how the words you use to define yourself can either build resilience or create fragility in the face of failure."
      theme={theme}
      sections={sections}
      onBack={onBack}
      progress={progress}
      onProgressUpdate={onProgressUpdate}
    >
      {(activeSection) => (
        <>
          {activeSection === 0 && (
            <ReadingSection title="Your Internal Narrator." eyebrow="Step 1" icon={Mic} theme={theme}>
              <p>When you face a setback, who is the narrator in your head? The language they use is not just commentary; it's the source code for your resilience. The science of <Highlight description="Your habitual way of explaining events. It's a powerful predictor of your resilience, motivation, and even your physical health." theme={theme}>Explanatory Style</Highlight>, pioneered by Martin Seligman, shows that the 'grammar' of your self-talk determines whether you bounce back or break down.</p>
              <ExplanatoryStyleQuiz />
            </ReadingSection>
          )}
          {activeSection === 1 && (
            <ReadingSection title="The 3 Ps of Failure." eyebrow="Step 2" icon={HeartCrack} theme={theme}>
              <p>A pessimistic explanatory style, which erodes grit, interprets failure through three toxic lenses: <strong>Personal</strong> ("It's my fault; I'm stupid"), <strong>Pervasive</strong> ("I ruin everything I touch"), and <strong>Permanent</strong> ("It's always going to be this way"). This isn't just negative thinking; it's a specific grammatical structure that leads to learned helplessness.</p>
              <p>An optimistic, resilient style does the opposite. It sees failure as <strong>External/Specific</strong> ("The strategy was wrong"), <strong>Specific</strong> ("I messed up this one thing"), and <strong>Temporary</strong> ("I'll do better next time"). This isn't about lying to yourself; it's about a disciplined, strategic choice to focus on what you can control.</p>
            </ReadingSection>
          )}
          {activeSection === 2 && (
            <ReadingSection title="The Re-Write Protocol." eyebrow="Step 3" icon={Recycle} theme={theme}>
              <p>You can train your brain to adopt a more optimistic style. This is called <Highlight description="A core technique of Cognitive Behavioural Therapy (CBT) where you learn to identify, challenge, and change your negative automatic thoughts." theme={theme}>Cognitive Restructuring</Highlight>. When you catch yourself using one of the 3 Ps, you must consciously "re-write" the script. For example, "I'm useless at Maths" (Personal, Permanent) becomes "My study method for trigonometry isn't working yet" (Specific, Temporary).</p>
              <ThoughtReframer />
              <MicroCommitment theme={theme}><p>Take one negative thought you had about school this week. Write it down. Now, try to rewrite it, changing one of the '3 Ps'. Turn a 'Personal' blame into a 'Specific' strategy problem.</p></MicroCommitment>
            </ReadingSection>
          )}
           {activeSection === 3 && (
            <ReadingSection title="The Role of Self-Compassion." eyebrow="Step 4" icon={Shield} theme={theme}>
                <p>A harsh inner critic doesn't build resilience; it creates shame, which is a powerful de-motivator. <Highlight description="Treating yourself with the same kindness you would offer a friend who is struggling. It's a powerful antidote to the shame that can follow failure." theme={theme}>Self-compassion</Highlight> is the antidote. It allows you to acknowledge a failure without letting it define you. It's the difference between "I failed" and "I am a failure."</p>
                <p>It has three parts: 1) <strong>Self-Kindness</strong>: Treat yourself like you'd treat a mate. 2) <strong>Common Humanity</strong>: Remember that everyone messes up. 3) <strong>Mindfulness</strong>: Acknowledge the feeling without letting it consume you.</p>
            </ReadingSection>
          )}
           {activeSection === 4 && (
            <ReadingSection title="Your Resilience Blueprint." eyebrow="Step 5" icon={Wrench} theme={theme}>
              <p>You now have the tools to become the editor of your own internal monologue. By auditing your self-talk for the 3 Ps and consciously rewriting the script with self-compassion, you can build a resilient, growth-oriented mindset one sentence at a time.</p>
              <MicroCommitment theme={theme}>
                <p>The next time you make a small mistake, just notice your first thought. Don't judge it, just label it. Was it Personal? Pervasive? Permanent? This act of noticing is the first step to taking control.</p>
              </MicroCommitment>
            </ReadingSection>
          )}
        </>
      )}
    </ModuleLayout>
  );
};
export default TheGrammarOfGritModule;
