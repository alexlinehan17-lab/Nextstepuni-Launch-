import { BrandedGuiltComparison } from './learning/BrandedCharts';
import { BrandedAutopilot,BrandedCircuitBreaker,BrandedEquation,InstructionList } from './learning/BrandedFeatures';
/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
*/

import { motion } from 'framer-motion';
import {
Brain,
Calculator,
HeartHandshake,
HeartPulse,
RotateCcw,
Shield,
Wrench,
Zap
} from 'lucide-react';
import React,{ useState } from 'react';
import { PROCRASTINATION_REFERENCE_LIST } from '../data/references/procrastination';
import { useEssentialsMode } from '../hooks/useEssentialsMode';
import { useNorthStar } from '../hooks/useNorthStar';
import { orangeTheme } from '../moduleThemes';
import { COMPACT_CALLOUT_PLACEMENTS } from '../northStarData';
import { type ModuleProgress } from '../types';
import { ModuleLayout } from './ModuleLayout';
import { Cite } from './ModuleReferences';
import { Highlight,MicroCommitment,ReadingSection } from './ModuleShared';
import NorthStarCallout from './NorthStarCallout';

const theme = orangeTheme;

// --- INTERACTIVE COMPONENTS ---

const ProcrastinationEquation = BrandedEquation;

const IfThenAutopilot = BrandedAutopilot;

const GuiltSpiral = () => {
    const [guilt, setGuilt] = useState(10);
    const [avoidance, setAvoidance] = useState(10);

    const addCriticism = () => {
        setGuilt(g => Math.min(100, g + 30));
        setAvoidance(a => Math.min(100, a + 25));
    }

    const practiceForgiveness = () => {
        setGuilt(g => Math.max(0, g - 18));
        setAvoidance(a => Math.max(0, a - 15));
    }

    const reset = () => {
        setGuilt(10);
        setAvoidance(10);
    }

    return(
        <div className="my-10 rounded-2xl p-6 md:p-8" style={{ backgroundColor: "var(--module-surface)", borderRadius: 18 }}>
             <h4 className="font-serif text-2xl font-semibold text-[var(--module-ink)] dark:text-[var(--module-ink)] text-center">The Guilt Spiral</h4>
             <p className="text-center text-sm text-[var(--module-muted)] dark:text-[var(--module-muted)] mb-8">"Tough love" doesn't work. It just adds more negative emotion to the fire. Try both buttons to see the difference.</p>
             <div className="grid grid-cols-2 gap-6 mb-8">
                <div className="text-center">
                    <p className="font-bold text-sm text-[var(--module-danger-text)] mb-2">Guilt Meter</p>
                    <div className="w-full h-6 bg-[var(--module-surface)] dark:bg-[var(--module-surface)] rounded-full"><motion.div className="h-full bg-[var(--module-danger)] rounded-full" initial={{width: "10%"}} animate={{width: `${guilt}%`}} /></div>
                </div>
                <div className="text-center">
                    <p className="font-bold text-sm text-[var(--module-ink)] mb-2">Urge to Avoid</p>
                    <div className="w-full h-6 bg-[var(--module-surface)] dark:bg-[var(--module-surface)] rounded-full"><motion.div className="h-full bg-[var(--module-orange)] rounded-full" initial={{width: "10%"}} animate={{width: `${avoidance}%`}} /></div>
                </div>
            </div>
             <div className="flex justify-center gap-3 flex-wrap">
                <button onClick={addCriticism} className="px-4 py-2 bg-[var(--module-danger-soft)] dark:bg-[var(--module-danger-soft)] text-[var(--module-danger-text)] dark:text-[var(--module-danger-text)] text-xs font-bold rounded-lg border border-[var(--module-line)] dark:border-[var(--module-line)]" data-wide-button="true">Add Self-Criticism</button>
                <button onClick={practiceForgiveness} className="px-4 py-2 bg-[var(--module-success-soft)] dark:bg-[var(--module-success-soft)] text-[var(--module-success-text)] dark:text-[var(--module-success-text)] text-xs font-bold rounded-lg border border-[var(--module-line)] dark:border-[var(--module-line)]" data-wide-button="true">Practice Self-Forgiveness</button>
                <button onClick={reset} className="px-4 py-2 bg-[var(--module-surface)] dark:bg-[var(--module-surface)] text-[var(--module-ink)] dark:text-[var(--module-muted)] text-xs font-bold rounded-lg border border-[var(--module-line)] dark:border-[var(--module-line)]" data-wide-button="true">Reset</button>
             </div>
        </div>
    );
};

const GuiltSpiralComparison = BrandedGuiltComparison;

const CircuitBreaker = BrandedCircuitBreaker

// --- MODULE COMPONENT ---
const ProcrastinationModule: React.FC<{ onBack: () => void; progress: ModuleProgress; onProgressUpdate: (progress: ModuleProgress) => void }> = ({ onBack, progress, onProgressUpdate }) => {
  const sections = [
    { id: 'real-reason', title: 'The Real Reason You Delay', eyebrow: '01 // Not Laziness', icon: HeartPulse },
    { id: 'amygdala-hijack', title: 'The Amygdala Hijack', eyebrow: '02 // Brain Battle', icon: Brain },
    { id: 'procrastination-equation', title: 'The Procrastination Equation', eyebrow: '03 // The Formula', icon: Calculator },
    { id: 'ego-defence', title: 'The Ego\'s Defence System', eyebrow: '04 // The Traps', icon: Shield },
    { id: 'guilt-cycle', title: 'The Guilt Cycle', eyebrow: '05 // The Downward Spiral', icon: RotateCcw },
    { id: 'forgiveness-protocol', title: 'The Forgiveness Protocol', eyebrow: '06 // The Circuit Breaker', icon: HeartHandshake },
    { id: 'if-then-protocol', title: 'The "If-Then" Protocol', eyebrow: '07 // The Antidote', icon: Zap },
    { id: 'scaffolding-focus', title: 'Scaffolding Your Focus', eyebrow: '08 // The Toolkit', icon: Wrench },
  ];

  const essentials = useEssentialsMode();
  const { northStar } = useNorthStar();

  return (
    <ModuleLayout
      moduleNumber="11"
      moduleTitle="Understanding Procrastination"
      moduleSubtitle="The Architecture of Delay"
      moduleDescription={`Procrastination isn't laziness — your brain is just wired to avoid things that feel bad. Once you understand what's actually going on, you can start beating it.`}
      theme={theme}
      sections={sections}
      references={PROCRASTINATION_REFERENCE_LIST}
      onBack={onBack}
      progress={progress}
      onProgressUpdate={onProgressUpdate}
      finishButtonText="Get Moving"
    >
      {(activeSection) => (
        <>
          {activeSection === 0 && (
            <ReadingSection title="The Real Reason You Delay." eyebrow="Step 1" icon={HeartPulse} theme={theme}>
              {essentials ? (
                <>
                  <p>Procrastination is not laziness. It is an <Highlight description="Your brain would rather feel okay right now than do something hard for later. You're not dodging the task itself — you're dodging the bad feeling the task gives you." theme={theme}>emotional regulation problem</Highlight>.<Cite n={1} /> You avoid tasks because they feel bad. Your brain is protecting you from a perceived threat. A maths book is not a real threat. But your brain treats it like one. You are not broken. Once you understand this, you can start fixing it.</p>
                </>
              ) : (
                <>
                  <p>Procrastination is not laziness. It is an <Highlight description="Your brain would rather feel okay right now than do something hard for later. You're not dodging the task itself — you're dodging the bad feeling the task gives you." theme={theme}>emotional regulation problem</Highlight>.<Cite n={1} /> When you look at a maths textbook and feel a wave of dread, your brain's primary goal shifts from "learn calculus" to "make this feeling go away." The easiest way to do that? Avoid the task entirely.</p>
                  <p>This is a critical reframe. You are not broken or lazy. Your brain is doing exactly what it's designed to do: protect you from perceived threats. The problem is that it has miscategorized a maths book as a threat. Understanding this is the first step to dismantling the cycle.</p>
                </>
              )}
            </ReadingSection>
          )}
          {activeSection === 1 && (
            <ReadingSection title="The Amygdala Hijack." eyebrow="Step 2" icon={Brain} theme={theme}>
              {essentials ? (
                <>
                  <p>Two parts of your brain are fighting. Your <Highlight description="The part of your brain that acts like a smoke alarm. It goes off when it senses danger — and unfortunately, it treats a hard maths problem the same as an actual threat." theme={theme}>amygdala</Highlight> is your alarm system. It panics at hard tasks. Your <Highlight description="The boss of your brain — it handles planning, self-control, and thinking about the future. The catch? At your age, it's still being built, so your alarm system can easily overrule it." theme={theme}>Prefrontal Cortex (PFC)</Highlight> handles planning and self-control. At your age, the PFC is still being built.<Cite n={2} /> So your alarm system often wins. This is an <Highlight description="When your emotional brain completely takes over your logical brain. It's why you can know you should be studying but still end up scrolling your phone without even deciding to." theme={theme}>Amygdala Hijack</Highlight>. "Just try harder" will not fix this. You need smarter tricks.</p>
                </>
              ) : (
                <>
                  <p>Procrastination is basically a tug-of-war inside your head between two parts of your brain. Your <Highlight description="The part of your brain that acts like a smoke alarm. It goes off when it senses danger — and unfortunately, it treats a hard maths problem the same as an actual threat." theme={theme}>amygdala</Highlight> (the alarm system) freaks out when it spots something that feels threatening. Your <Highlight description="The boss of your brain — it handles planning, self-control, and thinking about the future. The catch? At your age, it's still being built, so your alarm system can easily overrule it." theme={theme}>Prefrontal Cortex (PFC)</Highlight> (the boss) is supposed to step in and calm things down, but at your age, it's still being built — so it often loses the fight.<Cite n={2} /></p>
                  <p>The result is an <Highlight description="When your emotional brain completely takes over your logical brain. It's why you can know you should be studying but still end up scrolling your phone without even deciding to." theme={theme}>Amygdala Hijack</Highlight>. Your emotional brain steamrolls your logical brain. That's why "just try harder" is useless advice. You need tricks that work <em>with</em> how your brain actually works, not against it.</p>
                </>
              )}
            </ReadingSection>
          )}
          {activeSection === 2 && (
            <ReadingSection title="The Procrastination Equation." eyebrow="Step 3" icon={Calculator} theme={theme}>
              {essentials ? (
                <p>Procrastination follows a formula: <Highlight description="Your motivation comes down to four things you can actually control: how confident you feel, how much the task matters to you, how easily you get distracted, and how far away the deadline is." theme={theme}>Motivation = (Expectancy x Value) / (Impulsiveness x Delay)</Highlight>.<Cite n={3} /> You have four levers. Boost your confidence (E) and make tasks meaningful (V). Reduce distractions (I) and shorten deadlines (D). Use the interactive tool below to see how each lever affects your motivation.</p>
              ) : (
                <p>There's actually a formula that explains procrastination: <Highlight description="Your motivation comes down to four things you can actually control: how confident you feel, how much the task matters to you, how easily you get distracted, and how far away the deadline is." theme={theme}>Motivation = (Expectancy x Value) / (Impulsiveness x Delay)</Highlight>.<Cite n={3} /> This gives you four levers to pull.</p>
              )}
              <InstructionList kind="equation" />
              <ProcrastinationEquation />
            </ReadingSection>
          )}
          {activeSection === 3 && (
            <ReadingSection title="The Ego's Defence System." eyebrow="Step 4" icon={Shield} theme={theme}>
              {essentials ? (
                <>
                  <p>Procrastination is a <Highlight description="A sneaky way your brain protects your self-image. If you don't try, you can always blame the result on not trying — which feels way less scary than trying your best and still falling short." theme={theme}>self-handicapping strategy</Highlight>.<Cite n={4} /> If you don't try, you can blame the bad result on not trying. That feels safer than trying and failing. The fix is a <Highlight description="Believing that you can get better at things through effort. When you think this way, a bad result just means 'I need more practice' instead of 'I'm not smart enough.'" theme={theme}>Growth Mindset</Highlight>. A bad result just means "I need more practice." It makes failure safe. You stop avoiding tasks.</p>
                </>
              ) : (
                <>
                  <p>Procrastination is also a <Highlight description="A sneaky way your brain protects your self-image. If you don't try, you can always blame the result on not trying — which feels way less scary than trying your best and still falling short." theme={theme}>self-handicapping strategy</Highlight>.<Cite n={4} /> If you don't study and get a bad grade, you can tell yourself: "Well, I didn't really try." This protects your ego from the more terrifying conclusion: "I tried my best and I'm still not good enough."</p>
                  <p>It's a bad deal. You trade long-term success for short-term comfort. But once you spot the pattern, you can break it. The fix is a <Highlight description="Believing that you can get better at things through effort. When you think this way, a bad result just means 'I need more practice' instead of 'I'm not smart enough.'" theme={theme}>Growth Mindset</Highlight> — which makes it safe to fail, because a bad result just means "I need to try differently" instead of "I'm not good enough."</p>
                </>
              )}
            </ReadingSection>
          )}
          {activeSection === 4 && (
            <ReadingSection title="The Guilt Cycle." eyebrow="Step 5" icon={RotateCcw} theme={theme}>
              {northStar && (() => { const p = COMPACT_CALLOUT_PLACEMENTS.find(p => p.moduleId === 'procrastination-protocol'); return p ? <NorthStarCallout northStar={northStar} variant="compact" message={p.message} /> : null; })()}
              {essentials ? (
                <>
                  <p>Self-criticism after procrastinating feels responsible. It is the worst response. It creates <Highlight description="That horrible sinking feeling after you've wasted time. The cruel twist is that feeling guilty makes you want to avoid even more, which creates even more guilt. It feeds itself." theme={theme}>guilt and shame</Highlight>. Guilt is a negative emotion. Your brain avoids negative emotions by procrastinating more. This creates a spiral: procrastinate, feel guilty, procrastinate more. Tough love makes it worse.</p>
                </>
              ) : (
                <>
                  <p>Most people respond to procrastination with self-criticism: "I'm so lazy. What's wrong with me?" This feels like accountability, but it's actually the worst thing you can do. Self-criticism generates <Highlight description="That horrible sinking feeling after you've wasted time. The cruel twist is that feeling guilty makes you want to avoid even more, which creates even more guilt. It feeds itself." theme={theme}>guilt and shame</Highlight>, which are negative emotions. And what does your brain do with negative emotions? It tries to avoid them—by procrastinating more.</p>
                  <p>This creates a vicious downward spiral: Procrastinate &#8594; Feel Guilty &#8594; More Negative Emotion &#8594; Procrastinate More &#8594; Feel More Guilty. "Tough love" doesn't break this cycle; it accelerates it.</p>
                </>
              )}
              <GuiltSpiralComparison />
              <GuiltSpiral />
            </ReadingSection>
          )}
          {activeSection === 5 && (
            <ReadingSection title="The Forgiveness Protocol." eyebrow="Step 6" icon={HeartHandshake} theme={theme}>
              {essentials ? (
                <>
                  <p><Highlight description="Letting go of the guilt instead of beating yourself up. It sounds soft, but students who forgive themselves for procrastinating actually procrastinate less the next time. The guilt is what keeps you stuck." theme={theme}>Self-Forgiveness</Highlight> breaks the guilt spiral. Students who forgave themselves procrastinated less next time.<Cite n={5} /> This is not letting yourself off the hook. It breaks the emotional chain. Use this script: "I procrastinated. That is human. I forgive myself. What is the smallest step I can take right now?"</p>
                </>
              ) : (
                <>
                  <p>The thing that actually breaks the guilt spiral is <Highlight description="Letting go of the guilt instead of beating yourself up. It sounds soft, but students who forgive themselves for procrastinating actually procrastinate less the next time. The guilt is what keeps you stuck." theme={theme}>Self-Forgiveness</Highlight>. It sounds too simple, but it works: students who forgave themselves for procrastinating before one exam were way less likely to procrastinate before the next one.<Cite n={5} /></p>
                  <p>This isn't about letting yourself off the hook. It's about breaking the emotional chain reaction. The script is simple: "I procrastinated. That's a human thing to do. I forgive myself. Now, what is the smallest possible step I can take right now?"</p>
                </>
              )}
              <CircuitBreaker />
            </ReadingSection>
          )}
          {activeSection === 6 && (
            <ReadingSection title="The 'If-Then' Protocol." eyebrow="Step 7" icon={Zap} theme={theme}>
              <p>Willpower runs out, especially when you're tired or stressed. So the best trick is to stop relying on willpower altogether and use an <Highlight description="You decide in advance what you'll do when a specific situation comes up. Because you've already made the decision, you don't have to fight yourself in the moment — it just happens." theme={theme}>"If-Then" Plan</Highlight> (an implementation intention).<Cite n={6} /> You make the decision ahead of time, so when the moment comes, there's nothing to argue about — you just do the thing.</p>
              <p>The formula: <strong>IF</strong> [Trigger/Situation], <strong>THEN</strong> I will [Specific Action]. For example: "IF it is 4:30 PM, THEN I will open my Maths textbook to page 1 and do the first question." The key is to make the action tiny and specific. You're not committing to "study Maths for 2 hours." You're committing to opening a book.</p>
              <IfThenAutopilot />
            </ReadingSection>
          )}
          {activeSection === 7 && (
            <ReadingSection title="Scaffolding Your Focus." eyebrow="Step 8" icon={Wrench} theme={theme}>
              <p>Now you have the mental tools. The last step is to set up your environment so that starting is easy and staying focused happens naturally. Use things like the <Highlight description="Work for 25 minutes, then take a 5-minute break. That's it. Knowing you only have to focus for 25 minutes makes it way easier to actually start." theme={theme}>Pomodoro Technique</Highlight> to make tasks feel manageable, and set up your space so distractions aren't within arm's reach.</p>
              <p>The ultimate goal is to build a system where starting is effortless and stopping requires effort. This is the opposite of your current default, where starting requires enormous effort and stopping (to check your phone) is effortless. Flip the script.</p>
              <MicroCommitment artwork="thinker" theme={theme}>
                <p>Right now, identify the ONE task you've been avoiding the most. Write down one "If-Then" plan for it. Make the action so small it feels almost silly. That's the point.</p>
              </MicroCommitment>
            </ReadingSection>
          )}
        </>
      )}
    </ModuleLayout>
  );
};
export default ProcrastinationModule;
