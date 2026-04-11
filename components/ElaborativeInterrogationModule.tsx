
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
    const retention = method === 'passive' ? 37 : method === 'ei' ? 72 : 0;

    return (
        <div className="my-10 rounded-2xl p-6 md:p-8" style={{ backgroundColor: '#F8F8F8', borderRadius: 18 }}>
            <h4 className="font-serif text-2xl font-semibold text-zinc-800 dark:text-white text-center">The "Hungry Man" Experiment</h4>
            <p className="text-center text-sm text-zinc-500 dark:text-zinc-400 mb-6">See the dramatic effect of asking "Why?" on your memory.</p>
            <div className="p-4 bg-zinc-100 dark:bg-zinc-800 rounded-xl text-center font-mono mb-6">"The hungry man got in the car."</div>
            <div className="grid grid-cols-2 gap-4">
                <button onClick={() => setMethod('passive')} className="p-4 rounded-xl text-sm font-bold" style={{ backgroundColor: method === 'passive' ? '#FCA5A5' : '#FFFFFF', border: `2.5px solid ${method === 'passive' ? '#DC2626' : '#1C1917'}`, borderRadius: 14, boxShadow: method === 'passive' ? 'none' : '3px 3px 0px 0px #1C1917', color: method === 'passive' ? '#7F1D1D' : '#1C1917' }}>Read Passively</button>
                <button onClick={() => setMethod('ei')} className="p-4 rounded-xl text-sm font-bold" style={{ backgroundColor: method === 'ei' ? '#6EE7B7' : '#FFFFFF', border: `2.5px solid ${method === 'ei' ? '#059669' : '#1C1917'}`, borderRadius: 14, boxShadow: method === 'ei' ? 'none' : '3px 3px 0px 0px #1C1917', color: method === 'ei' ? '#064E3B' : '#1C1917' }}>Ask "Why?"</button>
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
        <div className="my-10 rounded-2xl p-6 md:p-8 text-center" style={{ backgroundColor: '#F8F8F8', borderRadius: 18 }}>
            <h4 className="font-serif font-bold" style={{ fontSize: 24, color: '#1a1a1a' }}>Flashcard 2.0</h4>
            <p className="text-sm mt-1 mb-6" style={{ color: '#7a7068' }}>Stop making "what" cards. Start making "why" cards.</p>
            <div className="w-full cursor-pointer" style={{ perspective: 1000, minHeight: 220 }} onClick={() => setIsFlipped(!isFlipped)}>
                <motion.div className="relative w-full" style={{ transformStyle: 'preserve-3d', minHeight: 220 }} animate={{ rotateY: isFlipped ? 180 : 0 }} transition={{ duration: 0.5, ease: [0.16, 1, 0.3, 1] }}>
                    {/* Front */}
                    <div className="absolute inset-0 flex flex-col items-center justify-center bg-white dark:bg-zinc-900" style={{ backfaceVisibility: 'hidden', WebkitBackfaceVisibility: 'hidden', border: '2px solid #1a1a1a', borderRadius: 16, padding: '32px 28px' }}>
                        <p style={{ fontSize: 10, fontWeight: 700, letterSpacing: '0.12em', color: '#9e9186', marginBottom: 16, textTransform: 'uppercase' as const }}>Front</p>
                        <p className="font-serif font-semibold" style={{ fontSize: 20, color: '#1a1a1a', lineHeight: 1.5 }}>Why is the left ventricle wall thicker than the right?</p>
                        <p className="italic mt-4" style={{ fontSize: 12, color: '#9e9186' }}>Tap to reveal</p>
                    </div>
                    {/* Back */}
                    <div className="absolute inset-0 flex flex-col items-center justify-center" style={{ backfaceVisibility: 'hidden', WebkitBackfaceVisibility: 'hidden', transform: 'rotateY(180deg)', backgroundColor: '#e8f5f2', border: '2px solid #2A7D6F', borderRadius: 16, padding: '32px 28px' }}>
                        <p style={{ fontSize: 10, fontWeight: 700, letterSpacing: '0.12em', color: '#1a6358', marginBottom: 16, textTransform: 'uppercase' as const }}>Back</p>
                        <p className="font-serif" style={{ fontSize: 18, color: '#1a1a1a', lineHeight: 1.6 }}>Because it pumps blood to the whole body (high pressure), while the right only pumps to the lungs (low pressure).</p>
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
    <div className="my-10 rounded-2xl p-6 md:p-8" style={{ backgroundColor: '#F8F8F8', borderRadius: 18 }}>
      <h4 className="font-serif text-2xl font-semibold text-zinc-800 dark:text-white text-center">Why-Chain Builder</h4>
      <p className="text-center text-sm text-zinc-500 dark:text-zinc-400 mb-6">Pick a fact, then keep asking "Why?" to build deeper understanding.</p>

      {selectedFactIndex === null ? (
        <div className="space-y-3">
          <p className="text-sm font-medium text-zinc-600 dark:text-zinc-300 text-center mb-2">Choose a starting fact:</p>
          {WHY_CHAIN_FACTS.map((item, i) => (
            <button key={i} onClick={() => handleSelectFact(i)} className="w-full text-left p-4 rounded-xl text-sm text-zinc-800 font-medium" style={{ backgroundColor: '#FFFFFF', border: '2.5px solid #1C1917', borderRadius: 14, boxShadow: '3px 3px 0px 0px #1C1917' }}>
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
                  className="flex-1 bg-white dark:bg-zinc-800 rounded-xl px-5 py-3.5 text-sm font-medium text-zinc-800 dark:text-white placeholder-zinc-400 outline-none"
                  style={{ border: '1.5px solid #E7E5E4' }}
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
              <p className="font-serif text-lg font-semibold text-emerald-800 dark:text-emerald-300">Nice one — you've gone 4 levels deep.</p>
              <p className="text-sm text-emerald-700 dark:text-emerald-400">Each "Why?" created a new connection in your memory. That's why this technique beats just reading your notes over and over.</p>
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
    { id: 'why-engine', title: 'The "Why" Engine', eyebrow: '01 // How It Works', icon: HelpCircle },
    { id: 'rules-of-road', title: 'The Rules of the Road', eyebrow: '02 // When It Works Best', icon: BatteryWarning },
    { id: 'stem-toolkit', title: 'The STEM Toolkit', eyebrow: '03 // Science & Maths', icon: Cpu },
    { id: 'humanities-engine', title: 'The Humanities Engine', eyebrow: '04 // Essays & Arguments', icon: BookCopy },
    { id: 'language-edge', title: 'The Language Edge', eyebrow: '05 // Gaeilge & Beyond', icon: Link },
    { id: 'study-protocol', title: 'Your Study Plan', eyebrow: '06 // The Action Plan', icon: Wrench },
  ];

  return (
    <ModuleLayout moduleNumber="05" moduleTitle="Elaborative Interrogation" moduleSubtitle={`The "Why" Method`} moduleDescription="Stop just memorising facts and start actually understanding them by asking one simple question: &quot;Why?&quot;. This module shows you how to make what you study stick — and mean something — for the Leaving Cert." theme={theme} sections={sections} onBack={onBack} progress={progress} onProgressUpdate={onProgressUpdate} finishButtonText="Start Asking Why">
      {(activeSection) => (
        <>
          {activeSection === 0 && (
            <ReadingSection title="The 'Why' Engine." eyebrow="Step 1" icon={HelpCircle} theme={theme}>
              <p>Learning isn't about absorbing facts — it's about actively connecting them. <Highlight description="A study trick where you come up with an explanation for why something is true. Instead of just reading a fact, you ask 'Why?' and link it to stuff you already know." theme={theme}>Elaborative Interrogation (EI)</Highlight> is a simple but powerful technique that turns you from a passive reader into an active detective. The core of it is asking one simple question: "Why is this true?"</p>
              <p>When you ask "Why?", you force your brain to dig through what it already knows and find connections. This turns a random, easy-to-forget fact into part of a bigger picture that actually sticks.</p>
              <p>Here's a great example. One group of students read a simple sentence like "The hungry man got into the car." A second group was told to ask "Why?" after reading it. This second group came up with a reason ("...to go to a restaurant"), which gave their brains more to hold onto. On a surprise test later, the "Why?" group remembered almost double what the passive readers did (72% vs 37%).</p>
              <HungryManExperiment/>
            </ReadingSection>
          )}
           {activeSection === 1 && (
            <ReadingSection title="The Rules of the Road." eyebrow="Step 2" icon={BatteryWarning} theme={theme}>
              <p>The "Why?" method is powerful, but it works best under the right conditions. First, there's the <Highlight description="Asking 'Why?' works best when you already know a bit about the topic. If you know nothing, you'll just guess — and probably guess wrong. Use it to go deeper, not to learn something brand new." theme={theme}>Prior Knowledge Paradox</Highlight>. If you ask "Why?" about a topic you know nothing about, you'll just make up wrong answers. This technique is for going deeper on stuff you've already started learning, not for meeting a topic for the first time.</p>
              <p>Second, asking "Why?" is mentally tiring. It takes real <Highlight description="The slow, careful kind of thinking where you really have to concentrate. It's the opposite of autopilot — powerful, but it drains your energy fast." theme={theme}>focused thinking</Highlight>. If you try to do it when you're wrecked, your brain runs out of steam — a bit like <Highlight description="When your brain is running on empty. After a long day, you have less mental energy left for hard thinking, so save this technique for when you're fresh." theme={theme}>hitting a wall</Highlight> — and the whole thing becomes less effective. Save it for your best study hours, when you actually have energy.</p>
            </ReadingSection>
          )}
          {activeSection === 2 && (
            <ReadingSection title="The STEM Toolkit." eyebrow="Step 3" icon={Cpu} theme={theme}>
              <p>For STEM subjects, asking "Why?" is your secret weapon against just memorising without understanding. In Biology, it helps you connect what you understand to the specific keywords the marking scheme is looking for. Asking "Why is the cell membrane semi-permeable?" forces you to pull up the key ideas about phospholipids and proteins.</p>
              <p>In Maths, asking "Why?" is brilliant for <Highlight description="Actually understanding why a formula or rule works, not just knowing how to use it. When you get the 'why', you can figure things out even if you forget the exact steps." theme={theme}>understanding the reasoning</Highlight>. Asking "Why does the integral of a velocity-time graph give distance?" locks in the core idea. However, it's not great for <Highlight description="Being able to do maths steps quickly and accurately without stopping to think about each one. You build this through practice and repetition, not by questioning every step." theme={theme}>speed and accuracy in calculations</Highlight>. Don't stop to ask "why" during every line of a long calculation in an exam — build that speed through practice beforehand.</p>
              <WhyChainBuilder />
            </ReadingSection>
          )}
           {activeSection === 3 && (
            <ReadingSection title="The Humanities Engine." eyebrow="Step 4" icon={BookCopy} theme={theme}>
                <p>In essay subjects like History, asking "Why?" takes you from just describing what happened to explaining <em>why</em> it happened — and that's where the real marks are. Instead of just stating "Collins signed the Treaty," you ask "Why did he sign it?" The answer becomes the main argument in your essay, which instantly boosts your marks.</p>
                <p>For Geography, which is built on <Highlight description="Significant Relevant Points — basically the building blocks of a Geography answer. Each SRP is a developed fact that's worth marks. The more good ones you have, the better your grade." theme={theme}>SRPs</Highlight>, asking "Why?" naturally creates the "Statement + Development" structure your teacher is always on about. Statement: "Earthquakes are common in Japan." Ask "Why?" Development: "Because Japan is on the convergence of four tectonic plates..." You've just created a perfect, two-mark SRP without even thinking about it.</p>
            </ReadingSection>
          )}
           {activeSection === 4 && (
            <ReadingSection title="The Language Edge." eyebrow="Step 5" icon={Link} theme={theme}>
              <p>For the Irish Oral, learning scripts off by heart is a recipe for disaster. The examiner is trained to spot them and will deliberately throw you off-script. Asking "Why?" is the key to building a flexible web of ideas around a topic instead. By asking "Why?" over and over ("Why do you play football?" {'\u2192'} "Because I like the team spirit." {'\u2192'} "Why is team spirit important?"), you build loads of connections between your ideas.</p>
              <p>This means you can go with the flow during the conversation. If the examiner asks about friends, you can link it back to the friends you made playing football. If they ask about health, you can talk about how football keeps you fit. You're no longer stuck reciting a script — you're talking naturally because you've actually thought about the topic from different angles.</p>
            </ReadingSection>
          )}
           {activeSection === 5 && (
            <ReadingSection title="Your Study Plan." eyebrow="Step 6" icon={Wrench} theme={theme}>
              <p>You know why it works. Now here's a simple four-step plan to actually use it when you study.</p>
              <div className="my-10 rounded-2xl p-5 md:p-6 space-y-3" style={{ backgroundColor: '#F8F8F8', borderRadius: 18 }}>
                {/* Card 1 — Sky */}
                <div className="p-4 flex items-start gap-4" style={{ backgroundColor: '#93C5FD', border: '2.5px solid #2563EB', borderRadius: 16, boxShadow: '4px 4px 0px 0px #2563EB' }}>
                  <div className="w-11 h-11 rounded-xl flex items-center justify-center shrink-0 text-lg font-serif font-bold text-white" style={{ backgroundColor: '#2563EB' }}>1</div>
                  <div>
                    <p className="text-sm font-bold" style={{ color: '#1E3A8A' }}>Highlight the facts</p>
                    <p className="text-[13px] mt-0.5" style={{ color: '#1E3A8A', opacity: 0.8 }}>Look at your notes and highlight the main facts.</p>
                  </div>
                </div>
                {/* Card 2 — Sunshine */}
                <div className="p-4 flex items-start gap-4" style={{ backgroundColor: '#FCD34D', border: '2.5px solid #D97706', borderRadius: 16, boxShadow: '4px 4px 0px 0px #D97706' }}>
                  <div className="w-11 h-11 rounded-xl flex items-center justify-center shrink-0 text-lg font-serif font-bold text-white" style={{ backgroundColor: '#D97706' }}>2</div>
                  <div>
                    <p className="text-sm font-bold" style={{ color: '#78350F' }}>Ask "Why?"</p>
                    <p className="text-[13px] mt-0.5" style={{ color: '#78350F', opacity: 0.8 }}>For each fact, write "Why?" in the margin.</p>
                  </div>
                </div>
                {/* Card 3 — Peach */}
                <div className="p-4 flex items-start gap-4" style={{ backgroundColor: '#FDBA74', border: '2.5px solid #EA580C', borderRadius: 16, boxShadow: '4px 4px 0px 0px #EA580C' }}>
                  <div className="w-11 h-11 rounded-xl flex items-center justify-center shrink-0 text-lg font-serif font-bold text-white" style={{ backgroundColor: '#EA580C' }}>3</div>
                  <div>
                    <p className="text-sm font-bold" style={{ color: '#7C2D12' }}>Answer it yourself</p>
                    <p className="text-[13px] mt-0.5" style={{ color: '#7C2D12', opacity: 0.8 }}>Write an explanation in your own words.</p>
                  </div>
                </div>
                {/* Card 4 — Mint */}
                <div className="p-4 flex items-start gap-4" style={{ backgroundColor: '#6EE7B7', border: '2.5px solid #059669', borderRadius: 16, boxShadow: '4px 4px 0px 0px #059669' }}>
                  <div className="w-11 h-11 rounded-xl flex items-center justify-center shrink-0 text-lg font-serif font-bold text-white" style={{ backgroundColor: '#059669' }}>4</div>
                  <div>
                    <p className="text-sm font-bold" style={{ color: '#064E3B' }}>Check your answer</p>
                    <p className="text-[13px] mt-0.5" style={{ color: '#064E3B', opacity: 0.8 }}>Compare it against the textbook to make sure you didn't get it wrong.</p>
                  </div>
                </div>
              </div>
              <p>This turns passive note-reading into something that actually builds your memory. One of the best things to come out of this is the "Why" flashcard.</p>
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
