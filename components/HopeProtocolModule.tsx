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
import { Highlight, ReadingSection, MicroCommitment } from './ModuleShared';
import { ModuleLayout } from './ModuleLayout';

const theme = emeraldTheme;

// --- INTERACTIVE COMPONENTS ---

const HopeDiagnostic = () => {
  const myths = [
    { myth: "Hope is just wishful thinking.", fact: "FALSE. Hope is an active cognitive skill combining motivation (willpower) and strategic planning (waypower)." },
    { myth: "You're either born hopeful or you're not.", fact: "FALSE. Hope is a teachable skill. The brain circuits for hope can be physically strengthened through practice (neuroplasticity)." },
    { myth: "Hope is the same as optimism.", fact: "FALSE. Optimism is a general belief that things will be okay. Hope is the specific belief that YOU can MAKE things okay through planning and effort." },
  ];
  return (
    <div className="my-10 p-8 md:p-12 bg-white dark:bg-zinc-800 rounded-2xl border border-zinc-200 dark:border-zinc-700 shadow-xl space-y-8">
      <h4 className="font-serif text-2xl font-semibold text-zinc-800 dark:text-white text-center italic">Hope Circuit Diagnostic</h4>
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
    <div className="w-full h-40 [perspective:1000px]" onClick={() => setIsFlipped(!isFlipped)}>
      <motion.div className="relative w-full h-full transition-transform duration-700" style={{ transformStyle: 'preserve-3d' }} animate={{ rotateX: isFlipped ? 180 : 0 }}>
        <div className="absolute w-full h-full [backface-visibility:hidden] rounded-3xl p-6 flex flex-col items-center justify-center text-center border-2 border-dashed border-zinc-300 bg-zinc-50 dark:bg-zinc-800/50 cursor-pointer group">
          <p className="text-sm font-bold leading-snug text-zinc-700 dark:text-zinc-200">{front}</p>
        </div>
        <div className="absolute w-full h-full [backface-visibility:hidden] rounded-3xl p-4 flex flex-col items-center justify-center text-center border-2 border-emerald-700 bg-emerald-600 text-white shadow-lg" style={{ transform: 'rotateX(180deg)' }}>
          <p className="text-xs font-bold leading-snug">{back}</p>
        </div>
      </motion.div>
    </div>
  );
};

const BrainMismatchDiagram = () => (
  <div className="my-10 p-8 md:p-12 bg-white dark:bg-zinc-800 rounded-2xl border border-zinc-200 dark:border-zinc-700 shadow-xl flex flex-col items-center">
    <h4 className="font-serif text-2xl font-semibold text-zinc-800 dark:text-white text-center italic mb-2">Adolescent Brain: System Mismatch</h4>
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
    <div className="my-10 p-8 md:p-12 bg-white dark:bg-zinc-800 rounded-2xl border border-zinc-200 dark:border-zinc-700 shadow-xl">
      <h4 className="font-serif text-2xl font-semibold text-zinc-800 dark:text-white text-center italic">Interactive: The Dopamine Dial</h4>
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
        <button onClick={() => handleChoice('cold')} className="p-4 bg-blue-50 border-2 border-blue-200 rounded-xl text-left text-sm hover:bg-blue-100 transition-colors"><strong>"Cold" Cognition:</strong> "I need to study history."</button>
        <button onClick={() => handleChoice('hot')} className="p-4 bg-rose-50 border-2 border-rose-200 rounded-xl text-left text-sm hover:bg-rose-100 transition-colors"><strong>"Hot" Cognition (EFT):</strong> "Imagine acing that exam..."</button>
      </div>

      <AnimatePresence>
        {choice !== 'none' && (
          <motion.div initial={{opacity:0, y:10}} animate={{opacity:1, y:0}} className="mt-8 p-6 rounded-2xl bg-zinc-900 text-white">
            {choice === 'cold' && <p><strong className="text-blue-400">Result:</strong> A small motivational increase. The task is abstract and lacks an immediate reward signal for your brain.</p>}
            {choice === 'hot' && <p><strong className="text-rose-400">Result:</strong> Major dopamine boost! Vividly simulating future success makes the reward feel real *now*, flooding your brain with the motivation to start.</p>}
          </motion.div>
        )}
      </AnimatePresence>
    </div>
  );
};

const HopeMap = () => {
  const [goal, setGoal] = useState('');
  const [pathways, setPathways] = useState(['']);
  const [obstacles, setObstacles] = useState(['']);

  const addPathway = () => setPathways([...pathways, '']);
  const addObstacle = () => setObstacles([...obstacles, '']);

  const updatePathway = (index: number, value: string) => {
    const newPathways = [...pathways];
    newPathways[index] = value;
    setPathways(newPathways);
  };
  const updateObstacle = (index: number, value: string) => {
    const newObstacles = [...obstacles];
    newObstacles[index] = value;
    setObstacles(newObstacles);
  };

  return (
    <div className="my-10 p-8 md:p-12 bg-white dark:bg-zinc-800 rounded-2xl border border-zinc-200 dark:border-zinc-700 shadow-xl space-y-8">
      <h4 className="font-serif text-2xl font-semibold text-zinc-800 dark:text-white text-center italic">My Hope Circuit Blueprint</h4>
      <div>
        <label className="block text-xs font-semibold text-zinc-600 dark:text-zinc-300 uppercase ml-4 mb-2">The Power Source (Your Goal)</label>
        <input value={goal} onChange={(e) => setGoal(e.target.value)} placeholder="e.g., Get a H2 in Leaving Cert Maths" className="w-full bg-zinc-50 dark:bg-zinc-800/50 border-2 border-zinc-100 rounded-xl p-4 focus:border-emerald-500 outline-none transition-colors" />
      </div>
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        <div>
          <label className="block text-xs font-semibold text-zinc-600 dark:text-zinc-300 uppercase ml-4 mb-2">The Wiring (Pathways)</label>
          <div className="space-y-2">
            {pathways.map((p, i) => (
              <input key={i} value={p} onChange={(e) => updatePathway(i, e.target.value)} placeholder={`Route ${i + 1}`} className="w-full bg-zinc-50 dark:bg-zinc-800/50 border-2 border-zinc-100 rounded-xl p-3 focus:border-emerald-500 outline-none transition-colors" />
            ))}
          </div>
          <button onClick={addPathway} className="mt-2 text-xs font-bold text-emerald-600 hover:text-emerald-800">+ Add another route</button>
        </div>
        <div>
          <label className="block text-xs font-semibold text-zinc-600 dark:text-zinc-300 uppercase ml-4 mb-2">Short Circuits (Obstacles)</label>
          <div className="space-y-2">
            {obstacles.map((o, i) => (
              <input key={i} value={o} onChange={(e) => updateObstacle(i, e.target.value)} placeholder={`Potential problem ${i + 1}`} className="w-full bg-zinc-50 dark:bg-zinc-800/50 border-2 border-zinc-100 rounded-xl p-3 focus:border-emerald-500 outline-none transition-colors" />
            ))}
          </div>
          <button onClick={addObstacle} className="mt-2 text-xs font-bold text-emerald-600 hover:text-emerald-800">+ Add another problem</button>
        </div>
      </div>
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
     <div className="my-10 p-8 md:p-12 bg-white dark:bg-zinc-800 rounded-2xl border border-zinc-200 dark:border-zinc-700 shadow-xl">
        <h4 className="font-serif text-2xl font-semibold text-zinc-800 dark:text-white text-center italic">Cortisol Curve Simulator</h4>
        <p className="text-center text-sm text-zinc-500 dark:text-zinc-400 mb-2">Stressor Detected: Bad Mock Exam Result.</p>
        <p className="text-center text-sm text-zinc-500 dark:text-zinc-400 mb-8">How does your system respond?</p>
        <div className="bg-zinc-50/50 p-6 rounded-2xl">
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
          <button onClick={() => setResponseType('low-hope')} className="p-4 bg-rose-50 border-2 border-rose-200 rounded-xl text-left text-sm"><strong>Low-Hope Response:</strong> "This is pointless, I'm just bad at this subject." <span className="block text-xs text-rose-500 mt-1">Result: Flattened cortisol curve, prolonged stress.</span></button>
          <button onClick={() => setResponseType('high-hope')} className="p-4 bg-emerald-50 border-2 border-emerald-200 rounded-xl text-left text-sm"><strong>High-Hope Response:</strong> "Okay, that didn't work. What's a new plan I can try?" <span className="block text-xs text-emerald-500 mt-1">Result: Healthy cortisol recovery, stress buffered.</span></button>
        </div>
     </div>
  );
}

// --- MODULE COMPONENT ---
const HopeProtocolModule: React.FC<{ onBack: () => void; progress: ModuleProgress; onProgressUpdate: (progress: ModuleProgress) => void }> = ({ onBack, progress, onProgressUpdate }) => {
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
      moduleTitle="The Hope Protocol"
      theme={theme}
      sections={sections}
      onBack={onBack}
      progress={progress}
      onProgressUpdate={onProgressUpdate}
    >
      {(activeSection) => (
        <>
          {activeSection === 0 && (
            <ReadingSection title="The Schematic: De-Coding Hope." eyebrow="Step 1" icon={BookOpen} theme={theme}>
              <p>Forget everything you think you know about hope. It's not a fluffy feeling or wishful thinking. According to decades of neuroscience, hope is a cognitive skill. It's a way of thinking, and like any skill, it can be learned, practiced, and mastered. Think of it as the technical schematic for your brain's motivation system.</p>
              <p>The formula, developed by psychologist C.R. Snyder, is deceptively simple: Hope = Goals + <Highlight description="Also known as 'Willpower.' This is the raw motivational energy, the belief that you can and will start moving toward your goal. It's the 'I can do this' feeling, backed by your brain's reward system." theme={theme}>Agency</Highlight> + <Highlight description="Also known as 'Waypower.' This is the strategic thinking, the ability to generate multiple routes to your goal, anticipate problems, and adapt when you hit a roadblock. It's run by your brain's Prefrontal Cortex." theme={theme}>Pathways</Highlight>. A simple diagnostic can help you see where your own circuit is strong, and where it might need an upgrade.</p>
              <HopeDiagnostic />
              <MicroCommitment theme={theme}>
                <p>Think of one vague goal you have (e.g., 'do better in French'). Open the notes app on your phone and re-write it as a clear, specific goal (e.g., 'Learn 10 new French vocabulary words by tomorrow evening').</p>
              </MicroCommitment>
            </ReadingSection>
          )}
           {activeSection === 1 && (
            <ReadingSection title="Your Brain's Circuit Board." eyebrow="Step 2" icon={Cpu} theme={theme}>
              <p>Your brain during your teenage years is a high-tech circuit board undergoing a massive upgrade. But there's a catch: not all components get upgraded at the same speed. This is called the <Highlight description="The key neurological feature of adolescence. Your emotional, reward-seeking limbic system (the accelerator) matures early, while your rational, long-term planning Prefrontal Cortex (the brakes) is still under construction until your mid-20s." theme={theme}>Developmental Mismatch</Highlight>.</p>
              <p>Your <Highlight description="The emotional, impulsive 'engine room' of your brain. It drives reward-seeking behaviour and emotional intensity. In teens, it's highly sensitive, giving you lots of raw motivational energy (Agency)." theme={theme}>Limbic System</Highlight> (your 'accelerator') is fully matured, giving you huge amounts of energy and desire for goals (Agency). But your <Highlight description="The 'CEO' or 'planning department' of your brain, located behind your forehead. It's responsible for impulse control, long-term planning, and complex problem-solving (Pathways)." theme={theme}>Prefrontal Cortex (PFC)</Highlight> (your 'brakes' and 'Sat-Nav') is still under construction. This means your desire to succeed often outstrips your brain's current capacity to plan the route, leading to frustration. This isn't a character flaw; it's a biological reality. Your job is to become a conscious engineer of this system.</p>
              <BrainMismatchDiagram />
               <MicroCommitment theme={theme}>
                <p>Next time you feel a strong impulse to procrastinate, just notice it. Say to yourself, "That's my limbic system." Don't judge it, just label it. This simple act of noticing engages your PFC.</p>
              </MicroCommitment>
            </ReadingSection>
          )}
           {activeSection === 2 && (
            <ReadingSection title="Powering Up: The Science of 'Willpower'." eyebrow="Step 3" icon={Zap} theme={theme}>
                <p>Agency, or 'Willpower,' is the electrical current in your Hope Circuit. It's the motivational force that gets you to start the engine. This isn't just 'trying hard'; it's a neurochemical process involving <Highlight description="The 'motivation molecule.' Dopamine is a neurotransmitter that drives you to seek rewards. A high-hope brain is better at generating its own dopamine hits by thinking about the future." theme={theme}>Dopamine</Highlight>.</p>
                <p>The key is understanding the difference between "cold" and "hot" cognition. "Cold" cognition is abstract ("I need to study"). "Hot" cognition, or <Highlight description="Episodic Future Thinking (EFT) is the ability to vividly simulate personal future events. This 'hot' cognition is the engine that drives motivation, recruiting memory and emotional networks in the brain." theme={theme}>Episodic Future Thinking</Highlight>, is vivid and emotional ("I can see myself walking out of the exam hall feeling proud"). This "hot" thinking is what tells your PFC to activate the brain's reward system, giving you a motivational boost. You can literally learn to generate your own voltage.</p>
                <DopamineDial />
                <MicroCommitment theme={theme}>
                    <p>Before you start studying tonight, take 60 seconds. Close your eyes and vividly imagine the feeling of relief and pride after you finish. You're practicing Episodic Future Thinking and giving your brain a small, upfront hit of dopamine.</p>
                </MicroCommitment>
            </ReadingSection>
          )}
          {activeSection === 3 && (
            <ReadingSection title="Designing the Wires: The Art of 'Waypower'." eyebrow="Step 4" icon={Waypoints} theme={theme}>
              <p>If Agency is the raw power, Pathways thinking is the sophisticated wiring that directs it. It's the most critical—and for teens, the most challenging—part of the Hope Circuit, because it depends entirely on your still-developing PFC.</p>
              <p>Effective 'Waypower' involves three key skills: <strong>Planning</strong> (breaking a big goal into small steps), <strong>Flexibility</strong> (generating multiple routes), and <strong>Problem-Solving</strong> (anticipating obstacles). The 'Hope Map' is a tool used by psychologists to train this exact skill. It forces your PFC to design the circuit before you turn on the power, "inoculating" your brain against the stress of failure by pre-loading solutions.</p>
              <HopeMap />
              <MicroCommitment theme={theme}>
                <p>Map out one tiny goal for tomorrow using the Goal-Pathway-Obstacle format. E.g., Goal: Get homework done by 8 pm. Pathway: Start at 6 pm in the kitchen. Obstacle: My brother will be noisy. Solution: Put on headphones.</p>
              </MicroCommitment>
            </ReadingSection>
          )}
           {activeSection === 4 && (
            <ReadingSection title="Stress Shield: Your Surge Protector." eyebrow="Step 5" icon={Shield} theme={theme}>
              <p>Hopelessness has a physical signature: a dysregulated stress response. When you face a threat (like a looming exam), your brain's alarm system—the <Highlight description="The Hypothalamic-Pituitary-Adrenal axis is your body's central stress response system. When it activates, it releases a cascade of hormones, culminating in cortisol." theme={theme}>HPA Axis</Highlight>—goes off, flooding your body with the stress hormone <Highlight description="Known as the 'stress hormone.' While essential in short bursts, chronically high levels of cortisol damage the brain, impair memory, and shut down access to your PFC (your planning centre)." theme={theme}>Cortisol</Highlight>.</p>
              <p>Hope acts as a neurobiological 'surge protector'. Having a clear goal and multiple pathways reduces the 'threat level' of a stressor. Your brain sees a difficult exam not as a life-threatening monster, but as a complex problem for which it has a plan. This calms the HPA axis, lowers cortisol, and keeps your PFC online when you need it most. See for yourself how a hopeful response can physically buffer the stress response in your body.</p>
              <CortisolSimulator/>
              <MicroCommitment theme={theme}>
                <p>The next time you feel exam stress, consciously name the feeling ('I am feeling stressed about Maths'). Acknowledging the signal is the first step any engineer takes to regulate a system.</p>
              </MicroCommitment>
            </ReadingSection>
          )}
           {activeSection === 5 && (
            <ReadingSection title="Upgrading the Hardware." eyebrow="Step 6" icon={Activity} theme={theme}>
              <p>Your brain's wiring isn't fixed. The connections can be physically strengthened through practice, a process called <Highlight description="The brain's ability to reorganize itself by forming new neural connections throughout life. Every time you practice a skill—like planning a study session—you physically strengthen the white matter tracts involved." theme={theme}>Neuroplasticity</Highlight>. The 'highways' connecting your PFC to other brain regions, like the <Highlight description="The Superior Longitudinal Fasciculus is a massive 'superhighway' of white matter fibres connecting your frontal, parietal, and temporal lobes. It's the physical infrastructure for Pathways thinking." theme={theme}>Superior Longitudinal Fasciculus (SLF)</Highlight>, are like muscles: the more you use them for planning and goal-setting, the stronger and faster they get.</p>
              <p>This means that every time you make a 'Hope Map' or break down a big task, you aren't just getting your work done—you are physically upgrading your brain's hardware for hope. One of the most powerful neuro-structural interventions is the 'Stop-Think' Protocol. It's a manual override for your brain's autopilot, forcing an engagement of the Hope Circuit.</p>
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
