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
