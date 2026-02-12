
/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
*/

import React, { useState } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import {
  Scaling, Brain, SlidersHorizontal, Thermometer, Puzzle, BarChartHorizontal, ZapOff
} from 'lucide-react';
import { ModuleProgress } from '../types';
import { tealTheme } from '../moduleThemes';
import { Highlight, ReadingSection, MicroCommitment } from './ModuleShared';
import { ModuleLayout } from './ModuleLayout';

const theme = tealTheme;

// --- INTERACTIVE COMPONENTS ---
const CognitiveLoadBalancer = () => {
    const [loads, setLoads] = useState({ intrinsic: 30, extraneous: 15, germane: 20 });
    const total = loads.intrinsic + loads.extraneous + loads.germane;
    const overload = total > 100;
    const germaneRoom = Math.max(0, 100 - loads.intrinsic - loads.extraneous);

    const getDiagnosis = () => {
      if (overload) return { text: 'Overloaded. Your Working Memory has no capacity left — nothing is being processed properly.', color: 'bg-rose-50 dark:bg-rose-950/20 border-rose-200 dark:border-rose-800/40 text-rose-700 dark:text-rose-300' };
      if (loads.extraneous > 30) return { text: 'Too much waste. Extraneous load is eating your capacity. Clear distractions before increasing study effort.', color: 'bg-amber-50 dark:bg-amber-950/20 border-amber-200 dark:border-amber-800/40 text-amber-700 dark:text-amber-300' };
      if (loads.germane < 15) return { text: 'Low learning. You have spare capacity but aren\'t using it for deep processing. Switch from passive to active study.', color: 'bg-zinc-50 dark:bg-zinc-900/30 border-zinc-200 dark:border-zinc-700 text-zinc-600 dark:text-zinc-300' };
      if (loads.germane >= 30 && !overload) return { text: 'Strong learning. Germane load is high and you\'re within capacity. This is effective study.', color: 'bg-emerald-50 dark:bg-emerald-950/20 border-emerald-200 dark:border-emerald-800/40 text-emerald-700 dark:text-emerald-300' };
      return { text: 'Moderate. You\'re within capacity but could push Germane load higher for deeper learning.', color: 'bg-teal-50 dark:bg-teal-950/20 border-teal-200 dark:border-teal-800/40 text-teal-700 dark:text-teal-300' };
    };

    const diagnosis = getDiagnosis();

    const loadTypes = [
      {
        key: 'intrinsic' as const,
        label: 'Intrinsic Load',
        plain: 'The difficulty of the topic itself',
        example: 'e.g., Probability is harder than basic addition',
        direction: 'Fixed — you can\'t change this, only manage around it',
        barColor: 'bg-blue-500',
        bgClass: 'bg-blue-50 dark:bg-blue-950/20',
        borderClass: 'border-blue-200 dark:border-blue-800/40',
        textClass: 'text-blue-700 dark:text-blue-300',
        accent: 'accent-blue-500',
        dotClass: 'bg-blue-500',
      },
      {
        key: 'extraneous' as const,
        label: 'Extraneous Load',
        plain: 'Waste from distractions & confusion',
        example: 'e.g., Phone buzzing, noisy room, unclear instructions',
        direction: 'Minimize this — it steals space from learning',
        barColor: 'bg-rose-500',
        bgClass: 'bg-rose-50 dark:bg-rose-950/20',
        borderClass: 'border-rose-200 dark:border-rose-800/40',
        textClass: 'text-rose-700 dark:text-rose-300',
        accent: 'accent-rose-500',
        dotClass: 'bg-rose-500',
      },
      {
        key: 'germane' as const,
        label: 'Germane Load',
        plain: 'The productive effort that builds memory',
        example: 'e.g., Active recall, self-explanation, practice questions',
        direction: 'Maximize this — it\'s the only load that causes learning',
        barColor: 'bg-teal-500',
        bgClass: 'bg-teal-50 dark:bg-teal-950/20',
        borderClass: 'border-teal-200 dark:border-teal-800/40',
        textClass: 'text-teal-700 dark:text-teal-300',
        accent: 'accent-teal-500',
        dotClass: 'bg-teal-500',
      },
    ];

    return (
      <div className="my-10 p-8 md:p-12 bg-white dark:bg-zinc-800 rounded-xl border border-zinc-200 dark:border-zinc-700">
        <h4 className="font-serif text-2xl font-semibold text-zinc-800 dark:text-white text-center">Cognitive Load Balancer</h4>
        <p className="text-center text-sm text-zinc-500 dark:text-zinc-400 mb-8">Your Working Memory is a small container. Three types of load compete for space inside it.</p>

        {/* Working Memory Tank */}
        <div className="mb-8">
          <div className="flex items-center justify-between mb-2">
            <span className="text-[10px] font-bold uppercase tracking-wider text-zinc-400 dark:text-zinc-500">Working Memory Capacity</span>
            <span className={`text-[10px] font-bold ${overload ? 'text-rose-500' : 'text-zinc-400 dark:text-zinc-500'}`}>{total}% / 100%</span>
          </div>
          <div className="relative w-full h-10 bg-zinc-100 dark:bg-zinc-900 rounded-xl overflow-hidden">
            <div className="absolute inset-0 flex">
              <motion.div
                className="h-full bg-blue-500/80"
                animate={{ width: `${Math.min(loads.intrinsic, 100)}%` }}
                transition={{ type: 'spring', stiffness: 120, damping: 20 }}
              />
              <motion.div
                className="h-full bg-rose-500/80"
                animate={{ width: `${Math.min(loads.extraneous, 100 - loads.intrinsic > 0 ? loads.extraneous : 0)}%` }}
                transition={{ type: 'spring', stiffness: 120, damping: 20 }}
              />
              <motion.div
                className="h-full bg-teal-500/80"
                animate={{ width: `${Math.min(loads.germane, germaneRoom > 0 ? loads.germane : 0)}%` }}
                transition={{ type: 'spring', stiffness: 120, damping: 20 }}
              />
            </div>
            {/* Capacity line */}
            <div className="absolute right-0 top-0 bottom-0 w-px bg-zinc-800 dark:bg-white opacity-30" />
            {overload && (
              <motion.div
                initial={{ opacity: 0 }}
                animate={{ opacity: [0.3, 0.6, 0.3] }}
                transition={{ duration: 1.2, repeat: Infinity }}
                className="absolute inset-0 bg-rose-500/20 rounded-xl"
              />
            )}
          </div>
          {/* Legend */}
          <div className="flex gap-4 mt-2 justify-center">
            {loadTypes.map(l => (
              <div key={l.key} className="flex items-center gap-1.5">
                <div className={`w-2.5 h-2.5 rounded-sm ${l.dotClass}`} />
                <span className="text-[9px] text-zinc-500 dark:text-zinc-400">{l.label}</span>
              </div>
            ))}
          </div>
        </div>

        {/* Load type cards */}
        <div className="space-y-3 mb-6">
          {loadTypes.map(l => (
            <div key={l.key} className={`p-4 rounded-xl border ${l.bgClass} ${l.borderClass}`}>
              <div className="flex items-start justify-between mb-1">
                <div>
                  <p className={`text-xs font-bold ${l.textClass}`}>{l.label}</p>
                  <p className="text-[11px] text-zinc-600 dark:text-zinc-300">{l.plain}</p>
                </div>
                <span className={`text-sm font-bold ${l.textClass} ml-3`}>{loads[l.key]}%</span>
              </div>
              <p className="text-[10px] text-zinc-400 dark:text-zinc-500 mb-2 italic">{l.example}</p>
              <input
                type="range" min="5" max="70"
                value={loads[l.key]}
                onChange={e => setLoads({ ...loads, [l.key]: parseInt(e.target.value) })}
                className={`w-full h-1.5 ${l.accent}`}
              />
              <p className={`text-[9px] font-bold mt-1 ${l.textClass} opacity-70`}>{l.direction}</p>
            </div>
          ))}
        </div>

        {/* Diagnosis */}
        <motion.div
          key={diagnosis.text}
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          className={`p-4 rounded-xl border ${diagnosis.color}`}
        >
          <p className="text-sm text-center">{diagnosis.text}</p>
        </motion.div>
      </div>
    );
}

const StairsEscalator = () => {
    const [choice, setChoice] = useState<'stairs' | 'escalator' | null>(null);
    return(
        <div className="my-10 p-8 md:p-12 bg-white dark:bg-zinc-800 rounded-xl border border-zinc-200 dark:border-zinc-700">
            <h4 className="font-serif text-2xl font-semibold text-zinc-800 dark:text-white text-center">Stairs vs. Escalator</h4>
            <p className="text-center text-sm text-zinc-500 dark:text-zinc-400 mb-6">Which path leads to real learning?</p>
            <div className="grid grid-cols-2 gap-4">
                <button onClick={() => setChoice('escalator')} className="p-4 bg-zinc-100 dark:bg-zinc-800 border border-zinc-200 dark:border-zinc-700 rounded-xl text-center"><strong>The Escalator:</strong> A perfectly clear lecture, re-reading your notes.</button>
                <button onClick={() => setChoice('stairs')} className="p-4 bg-zinc-100 dark:bg-zinc-800 border border-zinc-200 dark:border-zinc-700 rounded-xl text-center"><strong>The Stairs:</strong> Struggling with a past paper, trying to explain a topic.</button>
            </div>
            {choice &&
            <motion.div initial={{opacity:0}} animate={{opacity:1}} className="mt-6 p-4 rounded-xl text-sm text-white bg-zinc-900">
                {choice === 'escalator' && <p><strong>You chose the escalator.</strong> It feels smooth and effortless. You arrive at the top (the answer) quickly. But your muscles (your brain) did no work. The feeling of fluency is high, but long-term learning is low.</p>}
                {choice === 'stairs' && <p><strong>You chose the stairs.</strong> It's slow and feels hard. You might stumble (make mistakes). But this effort is what strengthens your cardiovascular system (your long-term memory). The feeling of learning is low, but the actual result is high.</p>}
            </motion.div>}
        </div>
    );
};

const ScenarioDiagnosis = () => {
  const scenarios = [
    {
      situation: 'Re-reading your History notes in a noisy kitchen while your family watches TV.',
      answer: 'extraneous',
      explanation: 'The task itself (re-reading) is too easy (Comfort Zone) AND the environment is full of distractions (high Extraneous Load). The primary fix is the environment — move somewhere quiet, then switch to active recall.',
    },
    {
      situation: 'Doing a past paper question from memory in a quiet room, on a topic you studied last week.',
      answer: 'optimal',
      explanation: 'This is Optimized Friction. The task is in your ZPD (hard but doable), the environment is clean (low Extraneous Load), and retrieval practice is a Desirable Difficulty. This is what effective study looks like.',
    },
    {
      situation: 'Watching a perfectly clear YouTube explainer on a topic you already understand well.',
      answer: 'zpd',
      explanation: 'The task is in the Comfort Zone — it feels productive because the explanation is fluent, but your brain is doing zero work. No struggle means no growth. You need to attempt harder problems on this topic.',
    },
    {
      situation: 'Attempting a university-level Maths proof with no guidance on a topic you haven\'t covered.',
      answer: 'zpd',
      explanation: 'This is the Frustration Zone. The task is so far beyond your current level that Working Memory overloads immediately. You need to step back to a worked example or ask for help to bring it into your ZPD.',
    },
    {
      situation: 'Highlighting your textbook in five different colours with a colour-coded system you invented.',
      answer: 'desirable',
      explanation: 'This feels effortful but it\'s fake friction. Highlighting is a passive task that doesn\'t force retrieval or generation. The effort is going into the system, not into learning. Replace it with a Brain Dump or practice questions.',
    },
    {
      situation: 'Trying to write an essay plan from memory, but your phone keeps buzzing with notifications.',
      answer: 'extraneous',
      explanation: 'The task is right (retrieval practice in the ZPD) but the environment is sabotaging it. Each notification hijacks your Working Memory, wiping out the very information you\'re trying to hold. Phone in another room.',
    },
  ];

  const pillars = [
    { key: 'zpd', label: 'Wrong Zone', desc: 'Too easy or too hard', color: 'bg-blue-500 text-white', borderActive: 'border-blue-500' },
    { key: 'extraneous', label: 'Too Much Noise', desc: 'Extraneous load is high', color: 'bg-rose-500 text-white', borderActive: 'border-rose-500' },
    { key: 'desirable', label: 'Fake Friction', desc: 'No desirable difficulties', color: 'bg-amber-500 text-white', borderActive: 'border-amber-500' },
    { key: 'optimal', label: 'Optimized', desc: 'All three pillars aligned', color: 'bg-emerald-500 text-white', borderActive: 'border-emerald-500' },
  ];

  const [current, setCurrent] = useState(0);
  const [answers, setAnswers] = useState<{ [key: number]: string }>({});
  const [revealed, setRevealed] = useState<Set<number>>(new Set());

  const handleAnswer = (pillarKey: string) => {
    if (revealed.has(current)) return;
    setAnswers(prev => ({ ...prev, [current]: pillarKey }));
    setRevealed(prev => new Set(prev).add(current));
  };

  const correct = Object.entries(answers).filter(([i, a]) => a === scenarios[parseInt(i)].answer).length;
  const allDone = revealed.size === scenarios.length;

  return (
    <div className="my-10 p-8 md:p-12 bg-white dark:bg-zinc-800 rounded-xl border border-zinc-200 dark:border-zinc-700">
      <h4 className="font-serif text-2xl font-semibold text-zinc-800 dark:text-white text-center">The Unified Model: Diagnose the Study Session</h4>
      <p className="text-center text-sm text-zinc-500 dark:text-zinc-400 mb-8">Read each scenario and identify the primary problem — or if the session is already optimized.</p>

      {/* Progress */}
      <div className="flex gap-1.5 mb-6">
        {scenarios.map((_, i) => (
          <button
            key={i}
            onClick={() => setCurrent(i)}
            className={`flex-1 h-2 rounded-full transition-all ${
              revealed.has(i)
                ? answers[i] === scenarios[i].answer ? 'bg-emerald-500' : 'bg-rose-400'
                : i === current ? 'bg-teal-400' : 'bg-zinc-200 dark:bg-zinc-700'
            }`}
          />
        ))}
      </div>

      {/* Scenario card */}
      <AnimatePresence mode="wait">
        <motion.div
          key={current}
          initial={{ opacity: 0, x: 15 }}
          animate={{ opacity: 1, x: 0 }}
          exit={{ opacity: 0, x: -15 }}
        >
          <div className="p-5 bg-zinc-50 dark:bg-zinc-900/30 rounded-xl border border-zinc-200 dark:border-zinc-700 mb-5">
            <p className="text-[10px] font-bold uppercase tracking-wider text-zinc-400 dark:text-zinc-500 mb-2">Scenario {current + 1} of {scenarios.length}</p>
            <p className="text-sm font-medium text-zinc-800 dark:text-zinc-200 leading-relaxed">{scenarios[current].situation}</p>
          </div>

          {/* Diagnosis buttons */}
          <div className="grid grid-cols-2 md:grid-cols-4 gap-2 mb-5">
            {pillars.map(p => {
              const isChosen = answers[current] === p.key;
              const isCorrect = scenarios[current].answer === p.key;
              const isRevealed = revealed.has(current);

              let btnClass = 'bg-zinc-50 dark:bg-zinc-900/30 text-zinc-600 dark:text-zinc-300 border-zinc-200 dark:border-zinc-700 hover:border-zinc-400';
              if (isRevealed && isChosen && isCorrect) btnClass = `${p.color} border-transparent`;
              else if (isRevealed && isChosen && !isCorrect) btnClass = 'bg-rose-100 dark:bg-rose-950/30 text-rose-600 dark:text-rose-400 border-rose-300 dark:border-rose-800';
              else if (isRevealed && isCorrect) btnClass = `${p.color} border-transparent opacity-70`;

              return (
                <button
                  key={p.key}
                  onClick={() => handleAnswer(p.key)}
                  disabled={isRevealed}
                  className={`p-3 rounded-xl border text-center transition-all ${btnClass}`}
                >
                  <p className="text-xs font-bold">{p.label}</p>
                  <p className="text-[9px] opacity-70 mt-0.5">{p.desc}</p>
                </button>
              );
            })}
          </div>

          {/* Feedback */}
          {revealed.has(current) && (
            <motion.div
              initial={{ opacity: 0, y: 8 }}
              animate={{ opacity: 1, y: 0 }}
              className={`p-4 rounded-xl border ${
                answers[current] === scenarios[current].answer
                  ? 'bg-emerald-50 dark:bg-emerald-950/20 border-emerald-200 dark:border-emerald-800/40'
                  : 'bg-rose-50 dark:bg-rose-950/20 border-rose-200 dark:border-rose-800/40'
              }`}
            >
              <p className={`text-xs font-bold mb-1 ${answers[current] === scenarios[current].answer ? 'text-emerald-600 dark:text-emerald-400' : 'text-rose-600 dark:text-rose-400'}`}>
                {answers[current] === scenarios[current].answer ? 'Correct' : 'Not quite'}
              </p>
              <p className="text-sm text-zinc-700 dark:text-zinc-300">{scenarios[current].explanation}</p>
            </motion.div>
          )}
        </motion.div>
      </AnimatePresence>

      {/* Navigation */}
      <div className="flex justify-between mt-6">
        <button
          onClick={() => setCurrent(c => Math.max(0, c - 1))}
          disabled={current === 0}
          className="px-4 py-2 text-xs font-bold text-zinc-500 dark:text-zinc-400 disabled:opacity-30"
        >
          Previous
        </button>
        {current < scenarios.length - 1 ? (
          <button
            onClick={() => setCurrent(c => c + 1)}
            className="px-4 py-2 text-xs font-bold text-teal-600 dark:text-teal-400"
          >
            Next
          </button>
        ) : allDone ? (
          <span className="px-4 py-2 text-xs font-bold text-emerald-600 dark:text-emerald-400">
            {correct}/{scenarios.length} correct
          </span>
        ) : null}
      </div>

      {/* Final insight */}
      {allDone && (
        <motion.div
          initial={{ opacity: 0, y: 10 }}
          animate={{ opacity: 1, y: 0 }}
          className="mt-4 p-4 bg-teal-50 dark:bg-teal-950/20 rounded-xl border border-teal-200 dark:border-teal-800/40 text-center"
        >
          <p className="text-sm font-semibold text-teal-700 dark:text-teal-300">
            The formula: Right Zone + Low Noise + Real Friction = Optimized Learning.
          </p>
          <p className="text-xs text-teal-600/70 dark:text-teal-400/60 mt-1">
            Before every study session, run this quick diagnostic on your setup.
          </p>
        </motion.div>
      )}
    </div>
  );
}


// --- MODULE COMPONENT ---
const EffectiveStruggleAndGrowthModule: React.FC<{ onBack: () => void; progress: ModuleProgress; onProgressUpdate: (progress: ModuleProgress) => void }> = ({ onBack, progress, onProgressUpdate }) => {
  const sections = [
    { id: 'fallacy-of-ease', title: 'The Fallacy of Ease', eyebrow: '01 // The Illusion', icon: Thermometer },
    { id: 'cognitive-load', title: 'Your Brain\'s Bottleneck', eyebrow: '02 // The Governor', icon: Brain },
    { id: 'zpd', title: 'The Sweet Spot', eyebrow: '03 // The Boundary', icon: Scaling },
    { id: 'desirable-difficulties', title: 'The Engine of Memory', eyebrow: '04 // The Engine', icon: Puzzle },
    { id: 'unified-model', title: 'The Unified Model', eyebrow: '05 // The Formula', icon: SlidersHorizontal },
    { id: 'recalibrate', title: 'Recalibrate Your Dashboard', eyebrow: '06 // The Feeling', icon: BarChartHorizontal },
  ];

  return (
    <ModuleLayout
      moduleNumber="04"
      moduleTitle="Effective Struggle"
      theme={theme}
      sections={sections}
      onBack={onBack}
      progress={progress}
      onProgressUpdate={onProgressUpdate}
    >
      {(activeSection) => (
        <>
          {activeSection === 0 && (
            <ReadingSection title="The Fallacy of Ease." eyebrow="Step 1" icon={Thermometer} theme={theme}>
              <p>Our intuition tells us that learning should feel easy. We think that if a teacher explains something perfectly and we understand it without any friction, that's a sign of great learning. This is the <Highlight description="The mistaken belief that learning which feels fluent and easy is effective. In reality, deep, long-term learning requires effortful processing and cognitive friction." theme={theme}>Intuitive Fallacy of Ease</Highlight>, and it's the single biggest trap students fall into.</p>
              <p>The science is clear: our subjective feeling of learning is often the exact opposite of what's actually happening in our brains. Easy learning feels good but is forgotten quickly. Hard, effortful learning feels bad but sticks. It's the difference between taking an escalator and taking the stairs. Only one of them makes you stronger.</p>
              <StairsEscalator />
            </ReadingSection>
          )}
           {activeSection === 1 && (
            <ReadingSection title="Your Brain's Bottleneck." eyebrow="Step 2" icon={Brain} theme={theme}>
              <p>To understand why difficulty is necessary, we have to look at your brain's architecture. Everything you learn has to pass through a tiny bottleneck called <Highlight description="The part of your mind that holds and manipulates information for a short period. It has a very limited capacity (around 3-5 items) and is the critical bottleneck for learning." theme={theme}>Working Memory</Highlight>. If you overload it, learning stops. This is called Cognitive Load Theory.</p>
              <p>There are three types of "load": <Highlight description="'Bad' difficulty caused by confusing instructions or a distracting environment. Your goal is to minimize this." theme={theme}>Extraneous Load</Highlight> (the bad stuff), <Highlight description="The inherent difficulty of the topic itself. This is fixed." theme={theme}>Intrinsic Load</Highlight> (the topic itself), and <Highlight description="'Good' difficulty caused by the effortful mental work of building understanding. Your goal is to maximize this." theme={theme}>Germane Load</Highlight> (the good stuff). The art of learning is to clear out all the 'bad' difficulty so you have enough mental space for the 'good' difficulty that actually builds memory.</p>
              <CognitiveLoadBalancer />
            </ReadingSection>
          )}
           {activeSection === 2 && (
            <ReadingSection title="The Sweet Spot." eyebrow="Step 3" icon={Scaling} theme={theme}>
              <p>The perfect level of difficulty is not too hard and not too easy. The psychologist Lev Vygotsky called this the <Highlight description="The 'sweet spot' of learning where a task is just beyond your current ability, but achievable with guidance or support. This is where the most efficient learning occurs." theme={theme}>Zone of Proximal Development (ZPD)</Highlight>. It's the Goldilocks zone of learning.</p>
              <p>Imagine three zones. The <strong>Comfort Zone</strong> is where you do things you've already mastered. Performance is high, but learning is zero. The <strong>Frustration Zone</strong> is where the task is so far beyond your current level that you can't even get started. This leads to cognitive overload and demotivation. The <strong>ZPD</strong> is the magic space in between, where you are stretched but not overwhelmed. This is the only place where growth happens.</p>
              <MicroCommitment theme={theme}>
                <p>Think about your hardest subject. What's one topic that feels just out of reach? Can you find a worked example or ask a friend for help to bring it into your ZPD?</p>
              </MicroCommitment>
            </ReadingSection>
          )}
          {activeSection === 3 && (
            <ReadingSection title="The Engine of Memory." eyebrow="Step 4" icon={Puzzle} theme={theme}>
              <p>So why is the "sweet spot" so effortful? Because of how memory works. Psychologist Robert Bjork discovered that memory has two strengths: <Highlight description="How easily you can recall a piece of information right now. It's high right after you study but fades quickly." theme={theme}>Retrieval Strength</Highlight> (how easy it is to access now) and <Highlight description="How deeply a memory is embedded in your brain. This only increases through effortful recall and is what we mean by 'learning'." theme={theme}>Storage Strength</Highlight> (how well you've actually learned it).</p>
              <p>Here's the paradox: your brain only increases Storage Strength when Retrieval Strength is *low*. In other words, you have to forget something a little bit before your brain will put in the effort to store it properly for the long term. This is why re-reading your notes feels easy (high retrieval strength) but does nothing for long-term memory. You need the "desirable difficulty" of struggling to remember.</p>
            </ReadingSection>
          )}
          {activeSection === 4 && (
            <ReadingSection title="The Unified Model." eyebrow="Step 5" icon={SlidersHorizontal} theme={theme}>
                <p>We can now put these three theories together to create a unified formula for optimal learning, or "Effective Struggle."</p>
                <ScenarioDiagnosis />
            </ReadingSection>
          )}
           {activeSection === 5 && (
            <ReadingSection title="Recalibrate Your Dashboard." eyebrow="Step 6" icon={BarChartHorizontal} theme={theme}>
              <p>Your brain is wired to conserve energy. It prefers the escalator to the stairs. This means your internal "dashboard"—your feeling about how well you're learning—is fundamentally unreliable. You have to consciously recalibrate it.</p>
              <p>From now on, when learning feels slow, frustrating, and difficult, that's not a sign you should stop. It's a sign that you're in the sweet spot. It's the sensation of your brain rewiring itself. You're not "confused"; you're building schema. You're not "slow"; you're building storage strength. If it feels like a struggle, it's working.</p>
              <MicroCommitment theme={theme}>
                <p>The next time you struggle with a problem, say this out loud: "This is not failure. This is the feeling of my brain getting stronger."</p>
              </MicroCommitment>
            </ReadingSection>
          )}
        </>
      )}
    </ModuleLayout>
  );
};
export default EffectiveStruggleAndGrowthModule;
