
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
    const [loads, setLoads] = useState({ intrinsic: 20, extraneous: 10, germane: 10 });
    const totalLoad = loads.intrinsic + loads.extraneous + loads.germane;
    const learning = totalLoad <= 100 && loads.germane > 10;
    const overload = totalLoad > 100;

    const Slider = ({ name, value, setter, color }: { name: string, value: number, setter: (val: number) => void, color: string }) => (
        <div className="flex items-center gap-2">
            <span className="text-xs font-bold w-28">{name}</span>
            <input type="range" min="10" max="80" value={value} onChange={e => setter(parseInt(e.target.value))} className={`w-full accent-${color}-500`} />
            <span className="text-xs font-bold w-8">{value}%</span>
        </div>
    );

    return (
         <div className="my-10 p-8 md:p-12 bg-white dark:bg-zinc-800 rounded-xl border border-zinc-200 dark:border-zinc-700">
            <h4 className="font-serif text-2xl font-semibold text-zinc-800 dark:text-white text-center">Cognitive Load Balancer</h4>
            <p className="text-center text-sm text-zinc-500 dark:text-zinc-400 mb-6">Your Working Memory is limited. Keep the total load below 100% and maximize Germane load to learn effectively.</p>
            <div className="w-full h-8 bg-zinc-100 dark:bg-zinc-800 rounded-full flex overflow-hidden mb-6">
                <motion.div className="h-full bg-blue-500" animate={{width: `${loads.intrinsic}%`}} />
                <motion.div className="h-full bg-rose-500" animate={{width: `${loads.extraneous}%`}} />
                <motion.div className="h-full bg-teal-500" animate={{width: `${loads.germane}%`}} />
            </div>
            <div className="space-y-2">
                <Slider name="Intrinsic Load" value={loads.intrinsic} setter={val => setLoads({...loads, intrinsic: val})} color="blue"/>
                <Slider name="Extraneous Load" value={loads.extraneous} setter={val => setLoads({...loads, extraneous: val})} color="rose"/>
                <Slider name="Germane Load" value={loads.germane} setter={val => setLoads({...loads, germane: val})} color="teal"/>
            </div>
            <div className={`mt-6 p-4 rounded-xl text-center text-white font-bold ${overload ? 'bg-rose-500' : learning ? 'bg-emerald-500' : 'bg-zinc-400'}`}>
                {overload ? 'COGNITIVE OVERLOAD! NO LEARNING.' : learning ? 'OPTIMAL LEARNING IN PROGRESS!' : 'LOW LEARNING. INCREASE GERMANE LOAD.'}
            </div>
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

const OptimizedFrictionEngine = () => {
  const [zpd, setZpd] = useState(0); // 0: Comfort, 1: ZPD, 2: Frustration
  const [extraneousLoad, setExtraneousLoad] = useState(50);
  const [desirableDifficulties, setDesirableDifficulties] = useState(50);

  const isOptimal = zpd === 1 && extraneousLoad < 20 && desirableDifficulties > 80;

  const zpdLabels = ["Comfort Zone", "Sweet Spot (ZPD)", "Frustration Zone"];
  const zpdColors = ["#3b82f6", "#10b981", "#ef4444"];

  let resultText = "Adjust the controls to find the optimal learning state...";
  if (zpd !== 1) resultText = "Set the task difficulty to the 'Sweet Spot'.";
  else if (extraneousLoad >= 20) resultText = "Minimize extraneous load by removing distractions.";
  else if (desirableDifficulties <= 80) resultText = "Maximize desirable difficulties to build memory.";
  if (isOptimal) resultText = "OPTIMAL LEARNING ENGAGED: You've achieved Optimized Friction!";

  return (
    <div className="my-12 p-8 md:p-12 bg-white dark:bg-zinc-800 rounded-xl border border-zinc-200 dark:border-zinc-700">
      <h4 className="font-serif text-2xl font-semibold text-zinc-800 dark:text-white text-center">The Optimized Friction Engine</h4>
      <p className="text-center text-sm text-zinc-500 dark:text-zinc-400 mb-8">Calibrate the three core variables to achieve true learning.</p>

      <div className="flex flex-col md:flex-row items-center gap-8">
        <div className="w-full md:w-1/3 flex justify-center items-center h-48">
          <motion.div
            className="relative w-40 h-40"
            animate={isOptimal ? { scale: 1.1, filter: 'drop-shadow(0 0 20px #10b981)' } : { scale: 1, filter: 'drop-shadow(0 0 5px #a8a29e)'}}
            transition={{ type: 'spring', damping: 10, stiffness: 100 }}
          >
            <motion.div className="absolute inset-0 rounded-full bg-teal-500 opacity-10" animate={{ scale: [1, 1.2, 1], opacity: isOptimal ? [0.1, 0.3, 0.1] : 0.1 }} transition={{ duration: 2, repeat: Infinity }} />
            <motion.div className="absolute inset-2 rounded-full bg-teal-500 opacity-20" animate={{ scale: [1, 1.1, 1], opacity: isOptimal ? [0.2, 0.4, 0.2] : 0.2 }} transition={{ duration: 1.5, repeat: Infinity, delay: 0.5 }}/>
            <div className="absolute inset-4 rounded-full bg-white dark:bg-zinc-800 border-4 border-teal-500 flex items-center justify-center">
              <Puzzle size={32} className="text-teal-600" />
            </div>
          </motion.div>
        </div>
        <div className="w-full md:w-2/3 space-y-6">
          {/* ZPD CONTROL */}
          <div>
            <div className="flex items-center gap-2 mb-2">
                <Scaling size={16} className="text-zinc-500 dark:text-zinc-400"/>
                <p className="text-sm font-bold">1. Zone of Proximal Development</p>
            </div>
            <div className="grid grid-cols-3 gap-1 bg-zinc-100 dark:bg-zinc-800 p-1 rounded-full">
              {zpdLabels.map((label, i) => (
                <button key={label} onClick={() => setZpd(i)} className={`py-2 text-xs font-bold rounded-full transition-colors ${zpd === i ? 'text-white shadow-md' : 'text-zinc-500 dark:text-zinc-400'}`} style={{backgroundColor: zpd === i ? zpdColors[i] : 'transparent'}}>{label.split(' (')[0]}</button>
              ))}
            </div>
          </div>
          {/* EXTRANEOUS LOAD CONTROL */}
           <div>
             <div className="flex items-center gap-2 mb-2">
                <ZapOff size={16} className="text-zinc-500 dark:text-zinc-400"/>
                <p className="text-sm font-bold">2. Extraneous Load (Minimize)</p>
            </div>
            <input type="range" min="0" max="100" value={extraneousLoad} onChange={e => setExtraneousLoad(parseInt(e.target.value))} className="w-full accent-rose-500" />
           </div>
          {/* DESIRABLE DIFFICULTIES CONTROL */}
           <div>
            <div className="flex items-center gap-2 mb-2">
                <Puzzle size={16} className="text-zinc-500 dark:text-zinc-400"/>
                <p className="text-sm font-bold">3. Desirable Difficulties (Maximize)</p>
            </div>
            <input type="range" min="0" max="100" value={desirableDifficulties} onChange={e => setDesirableDifficulties(parseInt(e.target.value))} className="w-full accent-emerald-500" />
           </div>
        </div>
      </div>
       <div className={`mt-8 p-4 rounded-xl text-center text-sm font-bold transition-all ${isOptimal ? 'bg-emerald-100 text-emerald-800' : 'bg-zinc-100 text-zinc-600 dark:text-zinc-300'}`}>
         {resultText}
      </div>
    </div>
  )
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
                <OptimizedFrictionEngine />
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
