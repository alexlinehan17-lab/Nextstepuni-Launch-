/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
*/

import React, { useState } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import {
  HeartPulse, Calculator, Shield, Zap, Wrench, Brain, RotateCcw, HeartHandshake
} from 'lucide-react';
import { ModuleProgress } from '../types';
import { orangeTheme } from '../moduleThemes';
import { Highlight, ReadingSection, MicroCommitment } from './ModuleShared';
import { ModuleLayout } from './ModuleLayout';

const theme = orangeTheme;

// --- INTERACTIVE COMPONENTS ---

const ProcrastinationEquation = () => {
    const [vars, setVars] = useState({ E: 50, V: 50, I: 50, D: 50 });
    const utility = (vars.E * vars.V) / (1 + (vars.I * vars.D / 100)); // Scaled for display

    const Slider = ({ name, value, setter, label }: { name: keyof typeof vars, value: number, setter: (val: number) => void, label: string }) => (
        <div>
            <label className="text-xs font-bold">{label} ({value})</label>
            <input type="range" min="1" max="100" value={value} onChange={e => setter(parseInt(e.target.value))} className="w-full accent-orange-500" />
        </div>
    );

    return(
        <div className="my-10 p-8 md:p-12 bg-white dark:bg-zinc-800 rounded-2xl border border-zinc-200 dark:border-zinc-700 shadow-xl">
            <h4 className="font-serif text-2xl font-semibold text-zinc-800 dark:text-white text-center italic">The Procrastination Equation</h4>
            <p className="text-center text-sm text-zinc-500 dark:text-zinc-400 mb-8">Adjust the sliders to see what drives your motivation.</p>
            <div className="p-6 bg-zinc-900 rounded-2xl text-center mb-8">
                <p className="text-sm text-zinc-400">Your Motivation Score:</p>
                <p className="text-5xl font-semibold text-white tracking-tighter"><motion.span initial={{}} animate={{}}>{Math.round(utility)}</motion.span></p>
            </div>
            <div className="grid grid-cols-2 gap-6">
                <Slider name="E" value={vars.E} setter={v => setVars({...vars, E:v})} label="Expectancy (Belief)" />
                <Slider name="V" value={vars.V} setter={v => setVars({...vars, V:v})} label="Value (Enjoyment)" />
                <Slider name="I" value={vars.I} setter={v => setVars({...vars, I:v})} label="Impulsiveness" />
                <Slider name="D" value={vars.D} setter={v => setVars({...vars, D:v})} label="Delay (Deadline)" />
            </div>
        </div>
    );
};

const IfThenAutopilot = () => {
    const [plan, setPlan] = useState<{if: string, then: string} | null>(null);

    const createPlan = () => {
      setPlan({if: "I feel the urge to check my phone", then: "I will take three deep breaths and work for 2 more minutes"});
    };

    return(
         <div className="my-10 p-8 md:p-12 bg-white dark:bg-zinc-800 rounded-2xl border border-zinc-200 dark:border-zinc-700 shadow-xl">
            <h4 className="font-serif text-2xl font-semibold text-zinc-800 dark:text-white text-center italic">The "If-Then" Autopilot</h4>
            <p className="text-center text-sm text-zinc-500 dark:text-zinc-400 mb-8">Pre-load a decision to bypass willpower. Click to create a plan.</p>
            <div className="flex justify-center">
                <button onClick={createPlan} className="px-5 py-3 bg-orange-500 text-white font-bold rounded-lg text-sm">Create Plan</button>
            </div>
            {plan &&
            <motion.div initial={{opacity:0}} animate={{opacity:1}} className="mt-6 p-4 bg-zinc-900 rounded-xl text-white text-center font-mono text-sm">
                Plan created: IF <span className="text-rose-400">{plan.if}</span>, THEN <span className="text-emerald-400">{plan.then}</span>
            </motion.div>}
        </div>
    );
};

const GuiltSpiral = () => {
    const [guilt, setGuilt] = useState(10);
    const [avoidance, setAvoidance] = useState(10);

    const addCriticism = () => {
        setGuilt(g => Math.min(100, g + 30));
        setAvoidance(a => Math.min(100, a + 25));
    }

    const reset = () => {
        setGuilt(10);
        setAvoidance(10);
    }

    return(
        <div className="my-10 p-8 md:p-12 bg-white dark:bg-zinc-800 rounded-2xl border border-zinc-200 dark:border-zinc-700 shadow-xl">
             <h4 className="font-serif text-2xl font-semibold text-zinc-800 dark:text-white text-center italic">The Guilt Spiral</h4>
             <p className="text-center text-sm text-zinc-500 dark:text-zinc-400 mb-8">"Tough love" doesn't work. It just adds more negative emotion to the fire.</p>
             <div className="grid grid-cols-2 gap-6 mb-8">
                <div className="text-center">
                    <p className="font-bold text-sm text-rose-600 mb-2">Guilt Meter</p>
                    <div className="w-full h-6 bg-zinc-100 dark:bg-zinc-800 rounded-full"><motion.div className="h-full bg-rose-500 rounded-full" initial={{width: "10%"}} animate={{width: `${guilt}%`}} /></div>
                </div>
                <div className="text-center">
                    <p className="font-bold text-sm text-orange-600 mb-2">Urge to Avoid</p>
                    <div className="w-full h-6 bg-zinc-100 dark:bg-zinc-800 rounded-full"><motion.div className="h-full bg-orange-500 rounded-full" initial={{width: "10%"}} animate={{width: `${avoidance}%`}} /></div>
                </div>
            </div>
             <div className="flex justify-center gap-4">
                <button onClick={addCriticism} className="px-4 py-2 bg-rose-100 text-rose-800 text-xs font-bold rounded-lg">Add Self-Criticism</button>
                <button onClick={reset} className="px-4 py-2 bg-zinc-100 dark:bg-zinc-800 text-zinc-800 dark:text-white text-xs font-bold rounded-lg">Reset</button>
             </div>
        </div>
    );
};

const CircuitBreaker = () => {
    const [reframe, setReframe] = useState('');
    const containsForgive = reframe.toLowerCase().includes('forgive');
    const containsAction = reframe.toLowerCase().includes('i will');
    return(
         <div className="my-10 p-8 md:p-12 bg-white dark:bg-zinc-800 rounded-2xl border border-zinc-200 dark:border-zinc-700 shadow-xl">
            <h4 className="font-serif text-2xl font-semibold text-zinc-800 dark:text-white text-center italic">The Circuit Breaker</h4>
            <p className="text-center text-sm text-zinc-500 dark:text-zinc-400 mb-8">Rewrite this self-critical thought into a self-forgiving, action-oriented statement.</p>
            <p className="p-4 bg-rose-50 border border-rose-200 rounded-xl text-center font-mono text-rose-800 mb-4">"I'm so useless, I wasted the whole day."</p>
            <textarea value={reframe} onChange={e => setReframe(e.target.value)} placeholder="Your new script..." className="w-full h-24 p-4 bg-zinc-50 dark:bg-zinc-800/50 border-2 border-zinc-200 dark:border-zinc-700 rounded-xl focus:outline-none focus:border-orange-400" />
            {(containsForgive || containsAction) &&
                <div className="mt-4 grid grid-cols-2 gap-2 text-xs">
                    <p className={containsForgive ? 'text-emerald-600 font-bold' : 'text-zinc-400'}>Contains Self-Forgiveness</p>
                    <p className={containsAction ? 'text-emerald-600 font-bold' : 'text-zinc-400'}>Bridges to Action</p>
                </div>
            }
        </div>
    );
}

// --- MODULE COMPONENT ---
// NOTE: The original file was truncated at 272 lines (cut off mid-sidebar).
// All extractable content sections have been preserved below. The sidebar/footer
// code was in the truncated portion and is now handled by ModuleLayout.
// Content for sections 0-7 was not present in the original file's return block
// (the file cut off before the <main> content area), so section content is
// reconstructed based on the section definitions and interactive components available.
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

  return (
    <ModuleLayout
      moduleNumber="02"
      moduleTitle="Procrastination Protocol"
      theme={theme}
      sections={sections}
      onBack={onBack}
      progress={progress}
      onProgressUpdate={onProgressUpdate}
    >
      {(activeSection) => (
        <>
          {activeSection === 0 && (
            <ReadingSection title="The Real Reason You Delay." eyebrow="Step 1" icon={HeartPulse} theme={theme}>
              <p>Procrastination is not laziness. It is an <Highlight description="An emotion-regulation strategy where the brain prioritizes short-term mood repair over long-term goals. You're not avoiding the task; you're avoiding the negative emotion the task triggers." theme={theme}>emotional regulation problem</Highlight>. When you look at a maths textbook and feel a wave of dread, your brain's primary goal shifts from "learn calculus" to "make this feeling go away." The easiest way to do that? Avoid the task entirely.</p>
              <p>This is a critical reframe. You are not broken or lazy. Your brain is doing exactly what it's designed to do: protect you from perceived threats. The problem is that it has miscategorized a maths book as a threat. Understanding this is the first step to dismantling the cycle.</p>
            </ReadingSection>
          )}
          {activeSection === 1 && (
            <ReadingSection title="The Amygdala Hijack." eyebrow="Step 2" icon={Brain} theme={theme}>
              <p>The neural mechanism behind procrastination is a battle between two brain regions. Your <Highlight description="The brain's threat-detection centre. It triggers the fight-or-flight response when it perceives danger, including the 'danger' of a difficult or boring task." theme={theme}>amygdala</Highlight> (the alarm system) fires a distress signal when it detects a threatening task. Your <Highlight description="The 'CEO' of the brain, responsible for planning, impulse control, and long-term decision-making. In adolescence, it is still developing, making it easier for the amygdala to 'win'." theme={theme}>Prefrontal Cortex (PFC)</Highlight> (the CEO) should override this, but in the adolescent brain, it's still under construction.</p>
              <p>The result is an <Highlight description="When the emotional brain (amygdala) overwhelms the rational brain (PFC), hijacking your decision-making. This is why you 'know' you should study but still reach for your phone." theme={theme}>Amygdala Hijack</Highlight>. Your emotional brain overwhelms your rational brain. This is why "just try harder" is useless advice. You need strategies that work *with* your brain's architecture, not against it.</p>
            </ReadingSection>
          )}
          {activeSection === 2 && (
            <ReadingSection title="The Procrastination Equation." eyebrow="Step 3" icon={Calculator} theme={theme}>
              <p>Psychologist Piers Steel formalized procrastination into a single equation: <Highlight description="Motivation = (Expectancy x Value) / (Impulsiveness x Delay). This formula shows that your motivation to do a task is determined by four variables you can consciously manipulate." theme={theme}>Motivation = (Expectancy x Value) / (Impulsiveness x Delay)</Highlight>. This gives you four levers to pull.</p>
              <p>**Expectancy:** Your belief you can succeed. Low confidence = high procrastination. **Value:** How rewarding or meaningful the task feels. **Impulsiveness:** Your susceptibility to distractions. **Delay:** How far away the deadline is. A task that is boring, feels impossible, is easily interrupted, and has a distant deadline is a recipe for maximum procrastination.</p>
              <ProcrastinationEquation />
            </ReadingSection>
          )}
          {activeSection === 3 && (
            <ReadingSection title="The Ego's Defence System." eyebrow="Step 4" icon={Shield} theme={theme}>
              <p>Procrastination is also a <Highlight description="A psychological strategy to protect your self-image. By not trying, you can attribute failure to lack of effort rather than lack of ability, which is less threatening to your ego." theme={theme}>self-handicapping strategy</Highlight>. If you don't study and get a bad grade, you can tell yourself: "Well, I didn't really try." This protects your ego from the more terrifying conclusion: "I tried my best and I'm still not good enough."</p>
              <p>This is a Faustian bargain. You trade long-term success for short-term psychological safety. Recognizing this pattern is crucial. The antidote is a <Highlight description="The belief that your abilities can be developed through effort. It decouples your performance from your identity, making failure a data point, not a verdict." theme={theme}>Growth Mindset</Highlight>, which makes failure safe by redefining it as a learning event, not a measure of your worth.</p>
            </ReadingSection>
          )}
          {activeSection === 4 && (
            <ReadingSection title="The Guilt Cycle." eyebrow="Step 5" icon={RotateCcw} theme={theme}>
              <p>Most people respond to procrastination with self-criticism: "I'm so lazy. What's wrong with me?" This feels like accountability, but it's actually the worst thing you can do. Self-criticism generates <Highlight description="A negative emotional state that, ironically, fuels the very avoidance cycle it's trying to break. More guilt leads to more negative emotion, which leads to more avoidance." theme={theme}>guilt and shame</Highlight>, which are negative emotions. And what does your brain do with negative emotions? It tries to avoid them--by procrastinating more.</p>
              <p>This creates a vicious downward spiral: Procrastinate &#8594; Feel Guilty &#8594; More Negative Emotion &#8594; Procrastinate More &#8594; Feel More Guilty. "Tough love" doesn't break this cycle; it accelerates it.</p>
              <GuiltSpiral />
            </ReadingSection>
          )}
          {activeSection === 5 && (
            <ReadingSection title="The Forgiveness Protocol." eyebrow="Step 6" icon={HeartHandshake} theme={theme}>
              <p>The scientifically-proven circuit breaker for the guilt spiral is <Highlight description="Research by Dr. Michael Wohl showed that students who forgave themselves for procrastinating on a first exam were LESS likely to procrastinate on the next one. Self-compassion reduces the negative emotion that fuels avoidance." theme={theme}>Self-Forgiveness</Highlight>. A landmark study by Dr. Michael Wohl found that students who forgave themselves for procrastinating on their first exam were significantly less likely to procrastinate on their second.</p>
              <p>This isn't about letting yourself off the hook. It's about breaking the emotional chain reaction. The script is simple: "I procrastinated. That's a human thing to do. I forgive myself. Now, what is the smallest possible step I can take right now?"</p>
              <CircuitBreaker />
            </ReadingSection>
          )}
          {activeSection === 6 && (
            <ReadingSection title="The 'If-Then' Protocol." eyebrow="Step 7" icon={Zap} theme={theme}>
              <p>Willpower is a limited resource, especially for a developing brain. The most effective anti-procrastination strategy is one that bypasses willpower entirely: the <Highlight description="A pre-commitment strategy (also called Implementation Intentions) where you pre-load a decision: 'IF [trigger], THEN [action].' This automates the behavior, removing the need for an in-the-moment willpower battle." theme={theme}>"If-Then" Plan</Highlight>. By pre-loading a decision, you automate the response and remove the negotiation your brain is so good at losing.</p>
              <p>The formula: **IF** [Trigger/Situation], **THEN** I will [Specific Action]. For example: "IF it is 4:30 PM, THEN I will open my Maths textbook to page 1 and do the first question." The key is to make the action tiny and specific. You're not committing to "study Maths for 2 hours." You're committing to opening a book.</p>
              <IfThenAutopilot />
            </ReadingSection>
          )}
          {activeSection === 7 && (
            <ReadingSection title="Scaffolding Your Focus." eyebrow="Step 8" icon={Wrench} theme={theme}>
              <p>Now you have the psychological tools. The final step is to scaffold your environment to make starting easy and staying focused automatic. This means using techniques like the <Highlight description="A time-management method where you work in focused 25-minute intervals ('Pomodoros') separated by 5-minute breaks. It makes tasks feel finite and manageable." theme={theme}>Pomodoro Technique</Highlight> to make tasks feel finite, and environmental design to remove distractions.</p>
              <p>The ultimate goal is to build a system where starting is effortless and stopping requires effort. This is the opposite of your current default, where starting requires enormous effort and stopping (to check your phone) is effortless. Flip the script.</p>
              <MicroCommitment theme={theme}>
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
