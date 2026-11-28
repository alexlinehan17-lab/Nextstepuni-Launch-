import { BrandedHungryMan } from './learning/WideFeatures';

/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
*/

import { AnimatePresence,motion } from 'framer-motion';
import {
BatteryWarning,
BookCopy,Cpu,
HelpCircle,
Link,
Wrench
} from 'lucide-react';
import React,{ useId,useState } from 'react';
import { ELABORATIVE_INTERROGATION_REFERENCE_LIST } from '../data/references/elaborativeInterrogation';
import { useEssentialsMode } from '../hooks/useEssentialsMode';
import { pinkTheme } from '../moduleThemes';
import { type ModuleProgress } from '../types';
import { ModuleLayout } from './ModuleLayout';
import { Cite } from './ModuleReferences';
import { Highlight,MicroCommitment,ReadingSection } from './ModuleShared';
import { AnswerGroup,AnswerLine,ExerciseSheet,RevealCard } from './learning/Exercise';
import { Button,TextButton } from './ui/Button';
import { ChoiceTile } from './ui/Choice';
import { Field } from './ui/Field';

const theme = pinkTheme;

// --- INTERACTIVE COMPONENTS ---

const HungryManExperiment = BrandedHungryMan;

const FlashcardFlipper = () => {
    const [isFlipped, setIsFlipped] = useState(false);
    return(
        <ExerciseSheet title="Flashcard 2.0" sub={'Stop making "what" cards. Start making "why" cards.'} name="FlashcardFlipper">
            {/* The card you press to turn over (it turns back when pressed again, as today); its side's name as a small label */}
            <RevealCard
                revealed={isFlipped}
                onPress={() => setIsFlipped(!isFlipped)}
                keepBefore={false}
                before={<>
                    <span className="ex-label">Front</span>
                    <span className="ex-reveal-words">Why is the left ventricle wall thicker than the right?</span>
                </>}
                hint="Tap to reveal"
                after={<>
                    <span className="ex-label block mb-1.5">Back</span>
                    <span className="ex-reveal-words">Because it pumps blood to the whole body (high pressure), while the right only pumps to the lungs (low pressure).</span>
                </>}
            />
        </ExerciseSheet>
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

const DEPTH_LABELS = ['Starting Fact', 'Level 1', 'Level 2', 'Level 3'];

const WhyChainBuilder = () => {
  const [selectedFactIndex, setSelectedFactIndex] = useState<number | null>(null);
  const [chain, setChain] = useState<string[]>([]);
  const [currentInput, setCurrentInput] = useState('');
  const [askingWhy, setAskingWhy] = useState(false);
  const titleId = useId();

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
    <ExerciseSheet title="Why-Chain Builder" sub={'Pick a fact, then keep asking "Why?" to build deeper understanding.'} name="WhyChainBuilder" id={titleId}>
      {selectedFactIndex === null ? (
        <AnswerGroup kind="one" legend="Choose a starting fact:" chooseOnArrow={false}>
          {WHY_CHAIN_FACTS.map((item, i) => (
            <ChoiceTile key={i} chosen={selectedFactIndex === i} onClick={() => handleSelectFact(i)} label={item.fact} />
          ))}
        </AnswerGroup>
      ) : (
        <div className="flex flex-col">
          {/* Chain links: each one's words on the sheet under its level's label (no tinted box), an ink arrow between */}
          <AnimatePresence>
            {chain.map((text, i) => (
              <React.Fragment key={i}>
                {i > 0 && (
                  <motion.div
                    initial={{ opacity: 0 }}
                    animate={{ opacity: 1 }}
                    className="flex justify-center py-2 text-ink-muted text-xl select-none"
                  >
                    ↓
                  </motion.div>
                )}
                <motion.div
                  initial={{ opacity: 0, y: 20 }}
                  animate={{ opacity: 1, y: 0 }}
                  transition={{ duration: 0.4, ease: 'easeOut' }}
                  className="ex-thought"
                >
                  <span className="ex-label">{DEPTH_LABELS[i]}</span>
                  <p className="ex-quote">{text}</p>
                </motion.div>
              </React.Fragment>
            ))}
          </AnimatePresence>

          {/* Why button or input or completion */}
          {!isComplete && !askingWhy && (
            <div className="ex-actions py-4">
              <Button onClick={() => setAskingWhy(true)}>
                Why?
              </Button>
            </div>
          )}

          {!isComplete && askingWhy && fact && (
            <motion.div
              initial={{ opacity: 0, y: 10 }}
              animate={{ opacity: 1, y: 0 }}
              className="mt-4 space-y-3"
            >
              <div className="flex justify-center py-2 text-ink-muted text-xl select-none">↓</div>
              <div className="flex gap-2 items-center">
                <Field
                  type="text"
                  aria-labelledby={titleId}
                  value={currentInput}
                  onChange={(e) => setCurrentInput(e.target.value)}
                  onKeyDown={(e) => { if (e.key === 'Enter') handleSubmitAnswer(); }}
                  placeholder={fact.hints[currentLevel - 1] || 'Type your explanation…'}
                  className="flex-1 min-w-0"
                  autoFocus
                />
                <Button
                  onClick={handleSubmitAnswer}
                  {...{ disabled: !currentInput.trim() }}
                  className="disabled:opacity-40"
                >
                  Submit
                </Button>
              </div>
            </motion.div>
          )}

          {isComplete && (
            <motion.div
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: 0.3 }}
              className="mt-6 ex-stack"
            >
              {/* Done: a line in ink with the tick, not a mint panel */}
              <AnswerLine>
                <b>Nice one — you've gone 4 levels deep.</b>{' '}
                <span>Each "Why?" created a new connection in your memory. That's why this technique beats just reading your notes over and over.</span>
              </AnswerLine>
              <div className="ex-actions">
                <TextButton tone="quiet" onClick={handleStartOver}>
                  Start Over
                </TextButton>
              </div>
            </motion.div>
          )}
        </div>
      )}
    </ExerciseSheet>
  );
};

// --- MODULE COMPONENT ---
const ElaborativeInterrogationModule: React.FC<{ onBack: () => void; progress: ModuleProgress; onProgressUpdate: (progress: ModuleProgress) => void }> = ({ onBack, progress, onProgressUpdate }) => {
  const essentials = useEssentialsMode();
  const sections = [
    { id: 'why-engine', title: 'The "Why" Engine', eyebrow: '01 // How It Works', icon: HelpCircle },
    { id: 'rules-of-road', title: 'The Rules of the Road', eyebrow: '02 // When It Works Best', icon: BatteryWarning },
    { id: 'stem-toolkit', title: 'The STEM Toolkit', eyebrow: '03 // Science & Maths', icon: Cpu },
    { id: 'humanities-engine', title: 'The Humanities Engine', eyebrow: '04 // Essays & Arguments', icon: BookCopy },
    { id: 'language-edge', title: 'The Language Edge', eyebrow: '05 // Gaeilge & Beyond', icon: Link },
    { id: 'study-protocol', title: 'Your Study Plan', eyebrow: '06 // The Action Plan', icon: Wrench },
  ];

  return (
    <ModuleLayout moduleNumber="05" moduleTitle="Elaborative Interrogation" moduleSubtitle={`The "Why" Method`} moduleDescription="Stop just memorising facts and start actually understanding them by asking one simple question: &quot;Why?&quot;. This module shows you how to make what you study stick — and mean something — when it counts." theme={theme} sections={sections} onBack={onBack} progress={progress} onProgressUpdate={onProgressUpdate} finishButtonText="Start Asking Why" references={ELABORATIVE_INTERROGATION_REFERENCE_LIST}>
      {(activeSection) => (
        <>
          {activeSection === 0 && (
            <ReadingSection title="The 'Why' Engine." eyebrow="Step 1" icon={HelpCircle} theme={theme}>
              {essentials ? (
                <>
                  <p>After you read a fact, ask yourself "Why is this true?" This forces your brain to connect the new fact to things you already know. That connection is what makes it stick.</p>
                  <p>In classic experiments, students who asked "Why?" remembered far more than passive readers — one simple question can come close to doubling how much sticks.<Cite n={1} /><Cite n={2} /></p>
                </>
              ) : (
                <>
                  <p>Learning isn't about absorbing facts — it's about actively connecting them. <Highlight description="A study trick where you come up with an explanation for why something is true. Instead of just reading a fact, you ask 'Why?' and link it to stuff you already know." theme={theme}>Elaborative Interrogation (EI)</Highlight> is a simple but powerful technique that turns you from a passive reader into an active detective. The core of it is asking one simple question: "Why is this true?"</p>
                  <p>When you ask "Why?", you force your brain to dig through what it already knows and find connections. This turns a random, easy-to-forget fact into part of a bigger picture that actually sticks.</p>
                  <p>Here's a great example. One group of students read a simple sentence like "The hungry man got into the car." A second group was told to ask "Why?" after reading it. This second group came up with a reason ("...to go to a restaurant"), which gave their brains more to hold onto. On a surprise test later, the "Why?" group remembered close to double what the passive readers did.<Cite n={1} /><Cite n={2} /></p>
                </>
              )}
              <HungryManExperiment/>
            </ReadingSection>
          )}
           {activeSection === 1 && (
            <ReadingSection title="The Rules of the Road." eyebrow="Step 2" icon={BatteryWarning} theme={theme}>
              {essentials ? (
                <>
                  <p>Only use this technique on topics you already know a bit about. If you know nothing, you will just guess wrong.<Cite n={3} /> Use it to go deeper, not to start from scratch.</p>
                  <p>Asking "Why?" takes real mental energy. Save it for when you are fresh. Do not try it when you are exhausted.</p>
                </>
              ) : (
                <>
                  <p>The "Why?" method is powerful, but it works best under the right conditions. First, there's the <Highlight description="Asking 'Why?' works best when you already know a bit about the topic. If you know nothing, you'll just guess — and probably guess wrong. Use it to go deeper, not to learn something brand new." theme={theme}>Prior Knowledge Paradox</Highlight>. If you ask "Why?" about a topic you know nothing about, you'll just make up wrong answers. This technique is for going deeper on stuff you've already started learning, not for meeting a topic for the first time.<Cite n={3} /></p>
                  <p>Second, asking "Why?" is mentally tiring. It takes real <Highlight description="The slow, careful kind of thinking where you really have to concentrate. It's the opposite of autopilot — powerful, but it drains your energy fast." theme={theme}>focused thinking</Highlight>. If you try to do it when you're wrecked, your brain runs out of steam — a bit like <Highlight description="When your brain is running on empty. After a long day, you have less mental energy left for hard thinking, so save this technique for when you're fresh." theme={theme}>hitting a wall</Highlight> — and the whole thing becomes less effective. Save it for your best study hours, when you actually have energy.</p>
                </>
              )}
            </ReadingSection>
          )}
          {activeSection === 2 && (
            <ReadingSection title="The STEM Toolkit." eyebrow="Step 3" icon={Cpu} theme={theme}>
              {essentials ? (
                <>
                  <p>In Biology, ask "Why?" to connect understanding to marking scheme keywords. In Maths, ask "Why?" to understand formulas deeply. But do not ask "Why?" during calculations. Build speed through practice instead.</p>
                  <p>Try the Why-Chain below. Pick a fact and keep asking "Why?" to go deeper.</p>
                </>
              ) : (
                <>
                  <p>For STEM subjects, asking "Why?" is your secret weapon against just memorising without understanding. In Biology, it helps you connect what you understand to the specific keywords the marking scheme is looking for. Asking "Why is the cell membrane semi-permeable?" forces you to pull up the key ideas about phospholipids and proteins.</p>
                  <p>In Maths, asking "Why?" is brilliant for <Highlight description="Actually understanding why a formula or rule works, not just knowing how to use it. When you get the 'why', you can figure things out even if you forget the exact steps." theme={theme}>understanding the reasoning</Highlight>. Asking "Why does the integral of a velocity-time graph give distance?" locks in the core idea. However, it's not great for <Highlight description="Being able to do maths steps quickly and accurately without stopping to think about each one. You build this through practice and repetition, not by questioning every step." theme={theme}>speed and accuracy in calculations</Highlight>. Don't stop to ask "why" during every line of a long calculation in an exam — build that speed through practice beforehand.</p>
                </>
              )}
              <WhyChainBuilder />
            </ReadingSection>
          )}
           {activeSection === 3 && (
            <ReadingSection title="The Humanities Engine." eyebrow="Step 4" icon={BookCopy} theme={theme}>
              {essentials ? (
                <>
                  <p>In History, asking "Why?" turns description into argument. That is where the real marks are. In Geography, asking "Why?" naturally creates the statement-plus-development structure you need for SRPs.</p>
                  <p>Example: "Earthquakes are common in Japan." Ask "Why?" Answer: "Because Japan sits on four tectonic plates." You just built a perfect SRP.</p>
                </>
              ) : (
                <>
                  <p>In essay subjects like History, asking "Why?" takes you from just describing what happened to explaining <em>why</em> it happened — and that's where the real marks are. Instead of just stating "Collins signed the Treaty," you ask "Why did he sign it?" The answer becomes the main argument in your essay, which instantly boosts your marks.</p>
                  <p>For Geography, which is built on <Highlight description="Significant Relevant Points — basically the building blocks of a Geography answer. Each SRP is a developed fact that's worth marks. The more good ones you have, the better your grade." theme={theme}>SRPs</Highlight>, asking "Why?" naturally creates the "Statement + Development" structure your teacher is always on about. Statement: "Earthquakes are common in Japan." Ask "Why?" Development: "Because Japan is on the convergence of four tectonic plates..." You've just created a perfect, two-mark SRP without even thinking about it.</p>
                </>
              )}
            </ReadingSection>
          )}
           {activeSection === 4 && (
            <ReadingSection title="The Language Edge." eyebrow="Step 5" icon={Link} theme={theme}>
              {essentials ? (
                <>
                  <p>For the Irish Oral, do not learn scripts by heart. Examiners will throw you off. Instead, use "Why?" to build a web of connected ideas around each topic.</p>
                  <p>This lets you go with the flow. If the examiner changes direction, you can link back naturally because you have thought about the topic from many angles.</p>
                </>
              ) : (
                <>
                  <p>For the Irish Oral, learning scripts off by heart is a recipe for disaster. The examiner is trained to spot them and will deliberately throw you off-script. Asking "Why?" is the key to building a flexible web of ideas around a topic instead. By asking "Why?" over and over ("Why do you play football?" {'\u2192'} "Because I like the team spirit." {'\u2192'} "Why is team spirit important?"), you build loads of connections between your ideas.</p>
                  <p>This means you can go with the flow during the conversation. If the examiner asks about friends, you can link it back to the friends you made playing football. If they ask about health, you can talk about how football keeps you fit. You're no longer stuck reciting a script — you're talking naturally because you've actually thought about the topic from different angles.</p>
                </>
              )}
            </ReadingSection>
          )}
           {activeSection === 5 && (
            <ReadingSection title="Your Study Plan." eyebrow="Step 6" icon={Wrench} theme={theme}>
              {essentials ? (
                <p>Four steps: highlight the facts, write "Why?" next to each, answer in your own words, then check against the textbook. Make "Why?" flashcards instead of "What?" flashcards.</p>
              ) : (
                <p>You know why it works. Now here's a simple four-step plan to actually use it when you study.</p>
              )}
              <ol className="ex-nums">
                <li>
                  <span className="ex-num">1</span>
                  <div className="ex-num-copy">
                    <p className="ex-num-title">Highlight the facts</p>
                    <p className="ex-num-sub">Look at your notes and highlight the main facts.</p>
                  </div>
                </li>
                <li>
                  <span className="ex-num">2</span>
                  <div className="ex-num-copy">
                    <p className="ex-num-title">Ask "Why?"</p>
                    <p className="ex-num-sub">For each fact, write "Why?" in the margin.</p>
                  </div>
                </li>
                <li>
                  <span className="ex-num">3</span>
                  <div className="ex-num-copy">
                    <p className="ex-num-title">Answer it yourself</p>
                    <p className="ex-num-sub">Write an explanation in your own words.</p>
                  </div>
                </li>
                <li>
                  <span className="ex-num">4</span>
                  <div className="ex-num-copy">
                    <p className="ex-num-title">Check your answer</p>
                    <p className="ex-num-sub">Compare it against the textbook to make sure you didn't get it wrong.</p>
                  </div>
                </li>
              </ol>
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
