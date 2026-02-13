
/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
*/

import React, { useState } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import {
  HelpCircle, BatteryWarning, Link, BookCopy, Cpu, Wrench
} from 'lucide-react';
import { ModuleProgress } from '../types';
import { pinkTheme } from '../moduleThemes';
import { Highlight, ReadingSection, MicroCommitment } from './ModuleShared';
import { ModuleLayout } from './ModuleLayout';

const theme = pinkTheme;

// --- INTERACTIVE COMPONENTS ---

const HungryManExperiment = () => {
    const [method, setMethod] = useState<'passive' | 'ei' | null>(null);
    let retention = method === 'passive' ? 37 : method === 'ei' ? 72 : 0;

    return (
        <div className="my-10 p-8 md:p-12 bg-white dark:bg-zinc-800 rounded-xl border border-zinc-200 dark:border-zinc-700">
            <h4 className="font-serif text-2xl font-semibold text-zinc-800 dark:text-white text-center">The "Hungry Man" Experiment</h4>
            <p className="text-center text-sm text-zinc-500 dark:text-zinc-400 mb-6">See the dramatic effect of asking "Why?" on your memory.</p>
            <div className="p-4 bg-zinc-100 dark:bg-zinc-800 rounded-xl text-center font-mono mb-6">"The hungry man got in the car."</div>
            <div className="grid grid-cols-2 gap-4">
                <button onClick={() => setMethod('passive')} className="p-4 bg-zinc-200 rounded-xl">Read Passively</button>
                <button onClick={() => setMethod('ei')} className="p-4 bg-pink-200 rounded-xl">Ask "Why?"</button>
            </div>
            {method && (
                 <div className="mt-6">
                    <p className="text-center text-sm font-bold mb-2">Memory Retention After 1 Week:</p>
                    <div className="w-full h-8 bg-zinc-100 dark:bg-zinc-800 rounded-full"><motion.div className="h-full bg-pink-500 rounded-full" initial={{width:0}} animate={{width: `${retention}%`}} /></div>
                 </div>
            )}
        </div>
    );
};

const FlashcardFlipper = () => {
    const [isFlipped, setIsFlipped] = useState(false);
    return(
        <div className="my-10 p-8 md:p-12 bg-white dark:bg-zinc-800 rounded-xl border border-zinc-200 dark:border-zinc-700 text-center">
            <h4 className="font-serif text-2xl font-semibold text-zinc-800 dark:text-white text-center">Flashcard 2.0</h4>
             <p className="text-center text-sm text-zinc-500 dark:text-zinc-400 mb-6">Stop making "what" cards. Start making "why" cards.</p>
            <div className="w-full h-48 [perspective:1000px]" onClick={() => setIsFlipped(!isFlipped)}>
                <motion.div className="relative w-full h-full" style={{transformStyle: 'preserve-3d'}} animate={{rotateY: isFlipped ? 180 : 0}}>
                    <div className="absolute w-full h-full [backface-visibility:hidden] rounded-xl bg-zinc-900 text-white flex flex-col items-center justify-center p-4">
                        <p className="text-xs text-zinc-400 mb-2">FRONT</p>
                        <p className="font-bold">Why is the left ventricle wall thicker than the right?</p>
                    </div>
                    <div className="absolute w-full h-full [backface-visibility:hidden] rounded-xl bg-emerald-500 text-white flex flex-col items-center justify-center p-4" style={{transform: 'rotateY(180deg)'}}>
                        <p className="text-xs text-emerald-200 mb-2">BACK</p>
                        <p className="font-bold text-sm">Because it pumps blood to the whole body (high pressure), while the right only pumps to the lungs (low pressure).</p>
                    </div>
                </motion.div>
            </div>
        </div>
    );
};

const WHY_CHAIN_FACTS = [
  {
    fact: 'The left ventricle wall is thicker than the right ventricle wall.',
    hints: [
      'e.g. Because it needs to pump blood further…',
      'e.g. Because the systemic circuit is longer…',
      'e.g. Because blood must reach every cell…',
    ],
  },
  {
    fact: 'Plants appear green in colour.',
    hints: [
      'e.g. Because they reflect green wavelengths of light…',
      'e.g. Because chlorophyll absorbs red and blue light…',
      'e.g. Because those wavelengths drive photosynthesis most efficiently…',
    ],
  },
  {
    fact: 'Metals are good conductors of electricity.',
    hints: [
      'e.g. Because they have free-moving electrons…',
      'e.g. Because metallic bonding leaves delocalised electrons…',
      'e.g. Because delocalised electrons can carry charge through the lattice…',
    ],
  },
];

const CHAIN_COLORS = [
  { border: 'border-l-zinc-400', bg: 'bg-zinc-50 dark:bg-zinc-700', label: 'text-zinc-500 dark:text-zinc-400' },
  { border: 'border-l-blue-500', bg: 'bg-blue-50 dark:bg-blue-900/30', label: 'text-blue-600 dark:text-blue-400' },
  { border: 'border-l-violet-500', bg: 'bg-violet-50 dark:bg-violet-900/30', label: 'text-violet-600 dark:text-violet-400' },
  { border: 'border-l-emerald-500', bg: 'bg-emerald-50 dark:bg-emerald-900/30', label: 'text-emerald-600 dark:text-emerald-400' },
];

const DEPTH_LABELS = ['Starting Fact', 'Level 1', 'Level 2', 'Level 3'];

const WhyChainBuilder = () => {
  const [selectedFactIndex, setSelectedFactIndex] = useState<number | null>(null);
  const [chain, setChain] = useState<string[]>([]);
  const [currentInput, setCurrentInput] = useState('');
  const [askingWhy, setAskingWhy] = useState(false);

  const handleSelectFact = (index: number) => {
    setSelectedFactIndex(index);
    setChain([WHY_CHAIN_FACTS[index].fact]);
    setCurrentInput('');
    setAskingWhy(false);
  };

  const handleSubmitAnswer = () => {
    if (!currentInput.trim()) return;
    setChain((prev) => [...prev, currentInput.trim()]);
    setCurrentInput('');
    setAskingWhy(false);
  };

  const handleStartOver = () => {
    setSelectedFactIndex(null);
    setChain([]);
    setCurrentInput('');
    setAskingWhy(false);
  };

  const isComplete = chain.length === 4;
  const currentLevel = chain.length;
  const fact = selectedFactIndex !== null ? WHY_CHAIN_FACTS[selectedFactIndex] : null;

  return (
    <div className="my-10 p-8 md:p-12 bg-white dark:bg-zinc-800 rounded-xl border border-zinc-200 dark:border-zinc-700">
      <h4 className="font-serif text-2xl font-semibold text-zinc-800 dark:text-white text-center">Why-Chain Builder</h4>
      <p className="text-center text-sm text-zinc-500 dark:text-zinc-400 mb-6">Pick a fact, then keep asking "Why?" to build deeper understanding.</p>

      {selectedFactIndex === null ? (
        <div className="space-y-3">
          <p className="text-sm font-medium text-zinc-600 dark:text-zinc-300 text-center mb-2">Choose a starting fact:</p>
          {WHY_CHAIN_FACTS.map((item, i) => (
            <button key={i} onClick={() => handleSelectFact(i)} className="w-full text-left p-4 rounded-lg border border-zinc-200 dark:border-zinc-600 hover:border-pink-400 dark:hover:border-pink-400 transition-colors bg-zinc-50 dark:bg-zinc-700 text-zinc-800 dark:text-zinc-100 text-sm">
              {item.fact}
            </button>
          ))}
        </div>
      ) : (
        <div className="space-y-0">
          {/* Chain links */}
          <AnimatePresence>
            {chain.map((text, i) => (
              <React.Fragment key={i}>
                {i > 0 && (
                  <motion.div
                    initial={{ opacity: 0 }}
                    animate={{ opacity: 1 }}
                    className="flex justify-center py-2 text-zinc-400 dark:text-zinc-500 text-xl select-none"
                  >
                    ↓
                  </motion.div>
                )}
                <motion.div
                  initial={{ opacity: 0, y: 20 }}
                  animate={{ opacity: 1, y: 0 }}
                  transition={{ duration: 0.4, ease: 'easeOut' }}
                  className={`p-4 rounded-lg border-l-4 ${CHAIN_COLORS[i].border} ${CHAIN_COLORS[i].bg}`}
                >
                  <span className={`text-xs font-semibold uppercase tracking-wide ${CHAIN_COLORS[i].label}`}>{DEPTH_LABELS[i]}</span>
                  <p className="text-sm text-zinc-800 dark:text-zinc-100 mt-1">{text}</p>
                </motion.div>
              </React.Fragment>
            ))}
          </AnimatePresence>

          {/* Why button or input or completion */}
          {!isComplete && !askingWhy && (
            <div className="flex justify-center py-4">
              <motion.button
                onClick={() => setAskingWhy(true)}
                className="px-6 py-2.5 rounded-full bg-pink-500 text-white font-semibold text-sm shadow-lg hover:bg-pink-600 transition-colors"
                animate={{ scale: [1, 1.05, 1] }}
                transition={{ duration: 1.5, repeat: Infinity, ease: 'easeInOut' }}
              >
                Why?
              </motion.button>
            </div>
          )}

          {!isComplete && askingWhy && fact && (
            <motion.div
              initial={{ opacity: 0, y: 10 }}
              animate={{ opacity: 1, y: 0 }}
              className="mt-4 space-y-3"
            >
              <div className="flex justify-center py-2 text-zinc-400 dark:text-zinc-500 text-xl select-none">↓</div>
              <div className="flex gap-2">
                <input
                  type="text"
                  value={currentInput}
                  onChange={(e) => setCurrentInput(e.target.value)}
                  onKeyDown={(e) => { if (e.key === 'Enter') handleSubmitAnswer(); }}
                  placeholder={fact.hints[currentLevel - 1] || 'Type your explanation…'}
                  className="flex-1 px-4 py-2.5 rounded-lg border border-zinc-300 dark:border-zinc-600 bg-white dark:bg-zinc-700 text-sm text-zinc-800 dark:text-zinc-100 placeholder-zinc-400 dark:placeholder-zinc-500 focus:outline-none focus:ring-2 focus:ring-pink-400"
                  autoFocus
                />
                <button
                  onClick={handleSubmitAnswer}
                  disabled={!currentInput.trim()}
                  className="px-5 py-2.5 rounded-lg bg-pink-500 text-white text-sm font-semibold disabled:opacity-40 hover:bg-pink-600 transition-colors"
                >
                  Submit
                </button>
              </div>
            </motion.div>
          )}

          {isComplete && (
            <motion.div
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: 0.3 }}
              className="mt-6 p-6 rounded-xl bg-emerald-50 dark:bg-emerald-900/20 border border-emerald-200 dark:border-emerald-700 text-center space-y-3"
            >
              <p className="font-serif text-lg font-semibold text-emerald-800 dark:text-emerald-300">You've built a 4-level deep understanding.</p>
              <p className="text-sm text-emerald-700 dark:text-emerald-400">Each "Why?" created a new connection in your long-term memory. This is why elaboration beats rote learning.</p>
              <button
                onClick={handleStartOver}
                className="mt-3 px-5 py-2 rounded-full bg-zinc-800 dark:bg-zinc-200 text-white dark:text-zinc-800 text-sm font-semibold hover:opacity-80 transition-opacity"
              >
                Start Over
              </button>
            </motion.div>
          )}
        </div>
      )}
    </div>
  );
};

// --- MODULE COMPONENT ---
const ElaborativeInterrogationModule: React.FC<{ onBack: () => void; progress: ModuleProgress; onProgressUpdate: (progress: ModuleProgress) => void }> = ({ onBack, progress, onProgressUpdate }) => {
  const sections = [
    { id: 'why-engine', title: 'The "Why" Engine', eyebrow: '01 // The Mechanism', icon: HelpCircle },
    { id: 'rules-of-road', title: 'The Rules of the Road', eyebrow: '02 // The Constraints', icon: BatteryWarning },
    { id: 'stem-toolkit', title: 'The STEM Toolkit', eyebrow: '03 // Science & Maths', icon: Cpu },
    { id: 'humanities-engine', title: 'The Humanities Engine', eyebrow: '04 // Essays & Arguments', icon: BookCopy },
    { id: 'language-edge', title: 'The Language Edge', eyebrow: '05 // Gaeilge & Beyond', icon: Link },
    { id: 'study-protocol', title: 'The EI Study Protocol', eyebrow: '06 // The Action Plan', icon: Wrench },
  ];

  return (
    <ModuleLayout moduleNumber="05" moduleTitle="Elaborative Interrogation" moduleSubtitle={`The "Why" Method`} moduleDescription="Move beyond rote learning by mastering the art of asking &quot;Why?&quot;. This module teaches you how to transform shallow facts into deep, interconnected knowledge for the new Leaving Cert." theme={theme} sections={sections} onBack={onBack} progress={progress} onProgressUpdate={onProgressUpdate}>
      {(activeSection) => (
        <>
          {activeSection === 0 && (
            <ReadingSection title="The 'Why' Engine." eyebrow="Step 1" icon={HelpCircle} theme={theme}>
              <p>Learning isn't about absorbing facts; it's about actively connecting them. <Highlight description="A powerful study technique that involves generating an explanation for why a fact or concept is true. It forces you to connect new information to your existing knowledge." theme={theme}>Elaborative Interrogation (EI)</Highlight> is a simple but profound technique that turns you from a passive reader into an active detective. The core of EI is asking one simple question: "Why is this true?"</p>
              <p>When you ask "Why?", you force your brain to search its long-term memory for related information, creating a rich network of connections. This transforms an isolated, easy-to-forget fact into part of a memorable story.</p>
              <p>This was powerfully demonstrated in the famous "hungry man" study. One group of students read a simple sentence like "The hungry man got into the car." A second group was told to ask "Why?". This second group inferred a reason ("...to go to a restaurant"), creating a richer memory. On a surprise test later, the "Why?" group's recall was almost double that of the passive readers (72% vs 37%).</p>
              <HungryManExperiment/>
            </ReadingSection>
          )}
           {activeSection === 1 && (
            <ReadingSection title="The Rules of the Road." eyebrow="Step 2" icon={BatteryWarning} theme={theme}>
              <p>EI is a high-performance tool, but it has two critical operating constraints. First is the <Highlight description="The counterintuitive finding that EI is most effective when you already have some background knowledge. It's for deepening understanding, not for learning something from scratch." theme={theme}>Prior Knowledge Paradox</Highlight>. If you ask "Why?" about a topic you know nothing about, you'll just invent wrong answers. EI is a consolidation tool, not a first-contact tool.</p>
              <p>Second, EI is mentally exhausting. It requires slow, effortful <Highlight description="A term from psychologist Daniel Kahneman for slow, deliberate, and analytical thinking. It's powerful but consumes a lot of mental energy." theme={theme}>System 2 thinking</Highlight>. Doing it when you're tired can lead to a state of <Highlight description="The idea that self-control and cognitive resources are finite. When you're depleted, your ability to perform effortful mental tasks (like EI) diminishes significantly." theme={theme}>Ego Depletion</Highlight>, making the strategy less effective. Use it during your high-energy study periods.</p>
            </ReadingSection>
          )}
          {activeSection === 2 && (
            <ReadingSection title="The STEM Toolkit." eyebrow="Step 3" icon={Cpu} theme={theme}>
              <p>For STEM subjects, EI is your secret weapon against rote learning. In Biology, it helps you bridge the gap between understanding a concept and knowing the specific keywords the marking scheme demands. Asking "Why is the cell membrane semi-permeable?" forces you to retrieve the key ideas of phospholipids and proteins.</p>
              <p>In Maths, EI is brilliant for <Highlight description="Understanding the 'why' behind a mathematical rule or formula, rather than just memorizing the 'how'." theme={theme}>conceptual understanding</Highlight>. Asking "Why does the integral of a velocity-time graph give distance?" cements the core idea. However, it's inefficient for <Highlight description="The ability to perform mathematical procedures quickly and accurately. This is built through repetitive practice, not constant questioning." theme={theme}>procedural fluency</Highlight>. Don't stop to ask "why" during every line of a long calculation in an exam; build that fluency through practice beforehand.</p>
              <WhyChainBuilder />
            </ReadingSection>
          )}
           {activeSection === 3 && (
            <ReadingSection title="The Humanities Engine." eyebrow="Step 4" icon={BookCopy} theme={theme}>
                <p>In essay subjects like History, EI is an "analytical engine." It shifts you from just describing what happened (narrative) to explaining *why* it happened (analysis). Instead of just stating "Collins signed the Treaty," you ask "Why did he sign it?" The answer becomes your thesis statement, instantly boosting your marks for argument and evaluation.</p>
                <p>For Geography, which is built on <Highlight description="Significant Relevant Points (SRPs) are the building blocks of a Geography answer. Each one is a developed piece of factual information worth marks." theme={theme}>SRPs</Highlight>, EI automates the "Statement + Development" structure. Statement: "Earthquakes are common in Japan." EI Prompt: "Why?" Development: "Because Japan is on the convergence of four tectonic plates..." You've just created a perfect, two-mark SRP.</p>
            </ReadingSection>
          )}
           {activeSection === 4 && (
            <ReadingSection title="The Language Edge." eyebrow="Step 5" icon={Link} theme={theme}>
              <p>For the Irish Oral, rote-learning scripts is a recipe for disaster. The examiner is trained to spot them and will throw you off-script. EI is the key to building a flexible, robust "web of knowledge" around a topic. By recursively asking "Why?" ("Why do you play football?" {'\u2192'} "Because I like the team spirit." {'\u2192'} "Why is team spirit important?"), you build multiple connections.</p>
              <p>This allows you to pivot naturally during the conversation. If the examiner asks about friends, you can link it back to the friends you made playing football. If they ask about health, you can talk about how football keeps you fit. You're no longer reciting a script; you're navigating a mental map you built yourself.</p>
            </ReadingSection>
          )}
           {activeSection === 5 && (
            <ReadingSection title="The EI Study Protocol." eyebrow="Step 6" icon={Wrench} theme={theme}>
              <p>You have the science. Now, here is the simple, four-step protocol to integrate EI into your study routine.</p>
              <p><strong>1. The Audit:</strong> Look at your notes and highlight the core facts. <strong>2. The Interrogation:</strong> For each fact, write "Why?" in the margin. <strong>3. The Elaboration:</strong> Answer the question in your own words. <strong>4. The Verification:</strong> Check your answer against the textbook to avoid learning errors. This cycle transforms passive note-taking into an active, memory-building process. One of the most powerful outputs of this is the "Why" flashcard.</p>
              <FlashcardFlipper />
              <MicroCommitment theme={theme}>
                <p>Take one page of your notes from any subject. For the next 5 minutes, go through and simply write a "Why?" question next to every main fact or definition. That's the first step.</p>
              </MicroCommitment>
            </ReadingSection>
          )}
        </>
      )}
    </ModuleLayout>
  );
};
export default ElaborativeInterrogationModule;
