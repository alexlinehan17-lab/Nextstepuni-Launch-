
/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
*/

import React, { useState } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import {
  Cpu, BrainCircuit, RotateCcw, Zap, MessageSquareQuote, Activity
} from 'lucide-react';
import { ModuleProgress } from '../types';
import { amberTheme } from '../moduleThemes';
import { Highlight, ReadingSection, MicroCommitment } from './ModuleShared';
import { ModuleLayout } from './ModuleLayout';

const theme = amberTheme;

// --- INTERACTIVE COMPONENTS ---

const MindsetDiagnostic = () => {
  const [answers, setAnswers] = useState<( 'fixed' | 'growth' | null)[]>([null, null, null]);
  const score = answers.filter(a => a === 'growth').length;

  const handleAnswer = (index: number, type: 'fixed' | 'growth') => {
    const newAnswers = [...answers];
    newAnswers[index] = type;
    setAnswers(newAnswers);
  };

  const isComplete = answers.every(a => a !== null);

  return (
    <div className="my-10 p-8 md:p-12 bg-white dark:bg-zinc-800 rounded-xl border border-zinc-200 dark:border-zinc-700">
      <h4 className="font-serif text-2xl font-semibold text-zinc-800 dark:text-white text-center">Mindset Diagnostic</h4>
      <p className="text-center text-sm text-zinc-500 dark:text-zinc-400 mb-8">Which thought sounds more like you in a tough situation?</p>
      <div className="space-y-6">
        {/* Question 1 */}
        <div>
          <p className="text-sm font-bold text-center text-zinc-600 dark:text-zinc-300 mb-3">When I fail at something...</p>
          <div className="grid grid-cols-2 gap-3">
            <button onClick={() => handleAnswer(0, 'fixed')} className={`p-4 rounded-xl text-xs text-center border ${answers[0] === 'fixed' ? 'bg-rose-500 text-white border-rose-500' : 'bg-zinc-50 border-zinc-200 dark:border-zinc-700 hover:bg-zinc-100 dark:hover:bg-zinc-700'}`}>A) I feel like I'm a failure.</button>
            <button onClick={() => handleAnswer(0, 'growth')} className={`p-4 rounded-xl text-xs text-center border ${answers[0] === 'growth' ? 'bg-emerald-500 text-white border-emerald-500' : 'bg-zinc-50 border-zinc-200 dark:border-zinc-700 hover:bg-zinc-100 dark:hover:bg-zinc-700'}`}>B) I feel like I need to try a new strategy.</button>
          </div>
        </div>
        {/* Question 2 */}
         <div>
          <p className="text-sm font-bold text-center text-zinc-600 dark:text-zinc-300 mb-3">If a subject is hard for me...</p>
          <div className="grid grid-cols-2 gap-3">
            <button onClick={() => handleAnswer(1, 'fixed')} className={`p-4 rounded-xl text-xs text-center border ${answers[1] === 'fixed' ? 'bg-rose-500 text-white border-rose-500' : 'bg-zinc-50 border-zinc-200 dark:border-zinc-700 hover:bg-zinc-100 dark:hover:bg-zinc-700'}`}>A) It means I'm probably not smart enough for it.</button>
            <button onClick={() => handleAnswer(1, 'growth')} className={`p-4 rounded-xl text-xs text-center border ${answers[1] === 'growth' ? 'bg-emerald-500 text-white border-emerald-500' : 'bg-zinc-50 border-zinc-200 dark:border-zinc-700 hover:bg-zinc-100 dark:hover:bg-zinc-700'}`}>B) It means I have a great opportunity to learn.</button>
          </div>
        </div>
        {/* Question 3 */}
         <div>
          <p className="text-sm font-bold text-center text-zinc-600 dark:text-zinc-300 mb-3">I believe my intelligence is something...</p>
          <div className="grid grid-cols-2 gap-3">
            <button onClick={() => handleAnswer(2, 'fixed')} className={`p-4 rounded-xl text-xs text-center border ${answers[2] === 'fixed' ? 'bg-rose-500 text-white border-rose-500' : 'bg-zinc-50 border-zinc-200 dark:border-zinc-700 hover:bg-zinc-100 dark:hover:bg-zinc-700'}`}>A) That I can't change very much.</button>
            <button onClick={() => handleAnswer(2, 'growth')} className={`p-4 rounded-xl text-xs text-center border ${answers[2] === 'growth' ? 'bg-emerald-500 text-white border-emerald-500' : 'bg-zinc-50 border-zinc-200 dark:border-zinc-700 hover:bg-zinc-100 dark:hover:bg-zinc-700'}`}>B) That I can grow with effort.</button>
          </div>
        </div>
      </div>
      <AnimatePresence>
      {isComplete && (
        <motion.div initial={{opacity:0, y:10}} animate={{opacity:1, y:0}} className="mt-8 p-6 rounded-xl bg-zinc-900 text-white">
          <p className="text-center font-bold">
            {score === 3 && <span className="text-emerald-400">Result: You're operating with a strong Growth Mindset OS!</span>}
            {score === 2 && <span className="text-amber-400">Result: You're leaning towards Growth, with some Fixed-Mindset code still running.</span>}
            {score < 2 && <span className="text-rose-400">Result: Your system is currently running a Fixed-Mindset OS. Time for an upgrade!</span>}
          </p>
        </motion.div>
      )}
      </AnimatePresence>
    </div>
  );
};

const NeuroplasticityVisualizer = () => {
  const [connections, setConnections] = useState(0);

  return (
    <div className="my-10 p-8 md:p-12 bg-white dark:bg-zinc-800 rounded-xl border border-zinc-200 dark:border-zinc-700">
      <h4 className="font-serif text-2xl font-semibold text-zinc-800 dark:text-white text-center">The Brain Rewiring Simulator</h4>
      <p className="text-center text-sm text-zinc-500 dark:text-zinc-400 mb-8">Every time you practice, you strengthen the physical connections in your brain.</p>

      <div className="h-40 flex justify-center items-center">
        <svg width="250" height="100" viewBox="0 0 250 100">
          {/* Neurons */}
          <circle cx="50" cy="50" r="20" fill="#f59e0b" />
          <circle cx="200" cy="50" r="20" fill="#f59e0b" />
          <AnimatePresence>
            {connections > 0 && Array.from({length: connections}).map((_, i) => (
              <motion.path
                key={i}
                d={`M 70 50 Q 125 ${50 + (i - (connections-1)/2) * 15} 180 50`}
                fill="none"
                stroke="#f59e0b"
                initial={{ pathLength: 0, opacity: 0, strokeWidth: 1 }}
                animate={{ pathLength: 1, opacity: Math.max(0.1, i / connections), strokeWidth: 1 + i*0.5 }}
                transition={{ duration: 0.5 }}
              />
            ))}
          </AnimatePresence>
        </svg>
      </div>
      <div className="text-center">
        <button onClick={() => setConnections(c => Math.min(c + 1, 5))} className="px-6 py-3 bg-amber-500 text-white font-bold rounded-lg hover:bg-amber-600 transition-colors">
          Practice a Skill
        </button>
        <button onClick={() => setConnections(0)} className="ml-4 text-xs text-zinc-400">Reset</button>
      </div>
    </div>
  );
}

const ReframeChallenge = () => {
    const [reframe, setReframe] = useState('');
    const containsYet = reframe.toLowerCase().includes('yet');

    return(
        <div className="my-10 p-8 md:p-12 bg-white dark:bg-zinc-800 rounded-xl border border-zinc-200 dark:border-zinc-700">
            <h4 className="font-serif text-2xl font-semibold text-zinc-800 dark:text-white text-center">The "Yet" Reframe Challenge</h4>
            <p className="text-center text-sm text-zinc-500 dark:text-zinc-400 mb-8">Upgrade this fixed thought into a growth mindset statement using the power of "yet".</p>
            <div className="p-6 bg-rose-50 border border-rose-200 rounded-xl mb-4">
                <p className="text-rose-800 text-center font-mono"><strong>Fixed Thought:</strong> "I'm just not a maths person."</p>
            </div>
            <textarea
                value={reframe}
                onChange={(e) => setReframe(e.target.value)}
                placeholder="Your growth reframe..."
                className="w-full h-24 bg-zinc-50 dark:bg-zinc-800/50 border border-zinc-100 rounded-xl p-4 focus:border-amber-500 outline-none transition-colors"
            />
             <AnimatePresence>
                {containsYet && (
                <motion.div initial={{opacity:0, y:10}} animate={{opacity:1, y:0}} className="mt-4 p-4 rounded-xl bg-emerald-50 text-emerald-700 text-center text-sm font-bold">
                    Excellent! You've opened up the possibility of future growth.
                </motion.div>
                )}
            </AnimatePresence>
        </div>
    );
};


const feedbackPairs = [
  {
    verdict: "This essay is poorly written.",
    data: "Your argument structure needs clearer topic sentences and supporting evidence in each paragraph.",
    shift: "Shift: vague verdict \u2192 specific, actionable data",
  },
  {
    verdict: "You're just not a maths person.",
    data: "Your current approach to maths isn't working yet. Let's identify which specific steps are causing confusion.",
    shift: "Shift: identity label \u2192 strategy problem",
  },
  {
    verdict: "This is careless work.",
    data: "There are 4 calculation errors here. A final check-through step would catch these.",
    shift: "Shift: character judgment \u2192 countable, fixable issue",
  },
  {
    verdict: "You should know this by now.",
    data: "This concept hasn't stuck yet. Try explaining it to someone else to find where your understanding breaks down.",
    shift: "Shift: time-based shame \u2192 retrieval practice suggestion",
  },
  {
    verdict: "Disappointing result.",
    data: "You scored 52%. The areas to focus on are Q3 and Q5 \u2014 those are the highest-value gaps to close.",
    shift: "Shift: emotional verdict \u2192 strategic data",
  },
  {
    verdict: "You need to try harder.",
    data: "Your effort needs to be more targeted. Spend 20 minutes on active recall instead of 40 minutes re-reading.",
    shift: "Shift: vague effort demand \u2192 specific method change",
  },
];

const writeYourOwnTranslations = [
  "That feedback is pointing to a specific skill gap I can work on \u2014 it\u2019s data, not a label.",
  "This tells me my current strategy isn\u2019t working yet. Time to try a different approach.",
  "The feedback is about my method, not my ability. I can adjust and improve.",
];

const MotionDiv = motion.div as any;

const FeedbackTranslator = () => {
  const [flipped, setFlipped] = useState<boolean[]>(Array(6).fill(false));
  const [customFeedback, setCustomFeedback] = useState('');
  const [selectedTranslation, setSelectedTranslation] = useState<number | null>(null);

  const translatedCount = flipped.filter(Boolean).length;
  const allTranslated = translatedCount === 6;

  const handleFlip = (index: number) => {
    if (flipped[index]) return;
    const next = [...flipped];
    next[index] = true;
    setFlipped(next);
  };

  return (
    <div className="my-10 p-8 md:p-12 bg-white dark:bg-zinc-800 rounded-xl border border-zinc-200 dark:border-zinc-700">
      <h4 className="font-serif text-2xl font-semibold text-zinc-800 dark:text-white text-center">
        Feedback Translator
      </h4>
      <p className="text-center text-sm text-zinc-500 dark:text-zinc-400 mt-2 mb-2">
        Click each card to translate harsh "verdict language" into constructive "data language."
      </p>
      <p className="text-center text-xs font-semibold text-amber-600 dark:text-amber-400 mb-8">
        {translatedCount}/6 translated
      </p>

      <div className="space-y-4">
        {feedbackPairs.map((pair, i) => (
          <div key={i}>
            <AnimatePresence mode="wait">
              {!flipped[i] ? (
                <MotionDiv
                  key={`verdict-${i}`}
                  initial={{ opacity: 0, y: 8 }}
                  animate={{ opacity: 1, y: 0 }}
                  exit={{ opacity: 0, rotateY: 90 }}
                  transition={{ duration: 0.3 }}
                  onClick={() => handleFlip(i)}
                  className="cursor-pointer p-6 rounded-xl bg-rose-50 dark:bg-rose-950/40 border border-rose-200 dark:border-rose-800 hover:shadow-md transition-shadow"
                >
                  <span className="inline-block text-[10px] font-bold uppercase tracking-widest text-rose-500 dark:text-rose-400 mb-2">
                    Verdict
                  </span>
                  <p className="font-serif italic text-rose-800 dark:text-rose-200 text-base">
                    "{pair.verdict}"
                  </p>
                  <p className="text-[11px] text-rose-400 dark:text-rose-500 mt-2">Click to translate</p>
                </MotionDiv>
              ) : (
                <MotionDiv
                  key={`data-${i}`}
                  initial={{ opacity: 0, rotateY: -90 }}
                  animate={{ opacity: 1, rotateY: 0 }}
                  transition={{ duration: 0.35 }}
                  className="p-6 rounded-xl bg-emerald-50 dark:bg-emerald-950/40 border border-emerald-200 dark:border-emerald-800"
                >
                  <span className="inline-block text-[10px] font-bold uppercase tracking-widest text-emerald-500 dark:text-emerald-400 mb-2">
                    Data
                  </span>
                  <p className="text-emerald-900 dark:text-emerald-100 text-base font-medium">
                    "{pair.data}"
                  </p>
                  <p className="text-xs text-zinc-500 dark:text-zinc-400 mt-3 italic">
                    {pair.shift}
                  </p>
                </MotionDiv>
              )}
            </AnimatePresence>
          </div>
        ))}
      </div>

      <AnimatePresence>
        {allTranslated && (
          <MotionDiv
            initial={{ opacity: 0, y: 12 }}
            animate={{ opacity: 1, y: 0 }}
            className="mt-8 p-6 rounded-xl bg-zinc-900 text-white text-center"
          >
            <p className="font-bold text-emerald-400">
              You've learned to hear data, not verdicts.
            </p>
            <p className="text-sm text-zinc-400 mt-1">
              Every piece of feedback is a GPS coordinate, not a destination.
            </p>
          </MotionDiv>
        )}
      </AnimatePresence>

      {/* Write Your Own section */}
      <div className="mt-10 pt-8 border-t border-zinc-200 dark:border-zinc-700">
        <h5 className="font-serif text-lg font-semibold text-zinc-800 dark:text-white text-center mb-2">
          Write Your Own
        </h5>
        <p className="text-center text-sm text-zinc-500 dark:text-zinc-400 mb-4">
          Type a piece of feedback you've received, then pick the translation that fits best.
        </p>
        <input
          type="text"
          value={customFeedback}
          onChange={(e) => {
            setCustomFeedback(e.target.value);
            setSelectedTranslation(null);
          }}
          placeholder="e.g. You always make silly mistakes..."
          className="w-full bg-zinc-50 dark:bg-zinc-900 border border-zinc-200 dark:border-zinc-700 rounded-xl px-4 py-3 text-sm focus:border-amber-500 outline-none transition-colors"
        />
        <AnimatePresence>
          {customFeedback.trim().length > 0 && (
            <MotionDiv
              initial={{ opacity: 0, y: 8 }}
              animate={{ opacity: 1, y: 0 }}
              exit={{ opacity: 0, y: -8 }}
              className="mt-4 space-y-3"
            >
              <p className="text-xs font-semibold uppercase tracking-widest text-zinc-400 dark:text-zinc-500">
                Pick your growth translation:
              </p>
              {writeYourOwnTranslations.map((t, i) => (
                <button
                  key={i}
                  onClick={() => setSelectedTranslation(i)}
                  className={`w-full text-left p-4 rounded-xl border text-sm transition-colors ${
                    selectedTranslation === i
                      ? 'bg-emerald-50 dark:bg-emerald-950/40 border-emerald-300 dark:border-emerald-700 text-emerald-800 dark:text-emerald-200 font-medium'
                      : 'bg-zinc-50 dark:bg-zinc-900 border-zinc-200 dark:border-zinc-700 text-zinc-600 dark:text-zinc-300 hover:bg-zinc-100 dark:hover:bg-zinc-800'
                  }`}
                >
                  {t}
                </button>
              ))}
              <AnimatePresence>
                {selectedTranslation !== null && (
                  <MotionDiv
                    initial={{ opacity: 0, y: 6 }}
                    animate={{ opacity: 1, y: 0 }}
                    className="p-4 rounded-xl bg-emerald-50 dark:bg-emerald-950/40 border border-emerald-200 dark:border-emerald-800 text-center"
                  >
                    <p className="text-sm text-emerald-700 dark:text-emerald-300 font-medium">
                      You just turned a verdict into data. That's the growth mindset in action.
                    </p>
                  </MotionDiv>
                )}
              </AnimatePresence>
            </MotionDiv>
          )}
        </AnimatePresence>
      </div>
    </div>
  );
};


// --- MODULE COMPONENT ---
const GrowthMindsetModule: React.FC<{ onBack: () => void; progress: ModuleProgress; onProgressUpdate: (progress: ModuleProgress) => void }> = ({ onBack, progress, onProgressUpdate }) => {
  const sections = [
    { id: 'two-brains', title: 'The Two Brains: Fixed vs. Growth', eyebrow: '01 // The Operating System', icon: Cpu },
    { id: 'brain-muscle', title: 'Your Brain is Plastic', eyebrow: '02 // The Hardware Upgrade', icon: BrainCircuit },
    { id: 'power-of-yet', title: 'The Most Powerful Word', eyebrow: '03 // The Software Patch', icon: RotateCcw },
    { id: 'effort-is-key', title: 'Effort is the Real Talent', eyebrow: '04 // The Engine', icon: Zap },
    { id: 'feedback-fuel', title: 'Feedback is Fuel, Not a Verdict', eyebrow: '05 // The Navigation Data', icon: MessageSquareQuote },
    { id: 'install-os', title: 'Installing Your Growth OS', eyebrow: '06 // System Integration', icon: Activity },
  ];

  return (
    <ModuleLayout
      moduleNumber="13"
      moduleTitle="The Growth Protocol"
      moduleSubtitle="The Mind's Operating System"
      moduleDescription={`Upgrade your brain's core operating system from "fixed" to "growth." This module deconstructs the science of neuroplasticity and gives you the tools to see challenges as opportunities.`}
      theme={theme}
      sections={sections}
      onBack={onBack}
      progress={progress}
      onProgressUpdate={onProgressUpdate}
    >
      {(activeSection) => (
        <>
          {activeSection === 0 && (
            <ReadingSection title="The Two Brains: Fixed vs. Growth." eyebrow="Step 1" icon={Cpu} theme={theme}>
              <p>Imagine your brain is a computer. Some people believe it comes with "read-only" memory. You're born with a certain amount of intelligence, and that's that. This is the <Highlight description="The belief that your intelligence and abilities are static, unchangeable traits. People with this mindset avoid challenges to avoid 'proving' their limitations." theme={theme}>Fixed Mindset</Highlight>. It's an operating system that sees effort as pointless and failure as a permanent judgement.</p>
              <p>But the science shows your brain is more like a rewritable drive. Every time you learn something new, you're installing new software. This is the <Highlight description="The belief that intelligence can be developed through dedication and hard work. This view creates a love of learning and a resilience that is essential for great accomplishment." theme={theme}>Growth Mindset</Highlight>. It's an operating system that sees challenges as opportunities and failure as feedback. Which OS is your brain running right now?</p>
              <MindsetDiagnostic />
              <MicroCommitment theme={theme}>
                <p>Listen to how you talk about school today. Catch one "fixed" thought (e.g., "I'm bad at Irish") and just notice it. You don't have to change it yet, just acknowledge you're running that piece of code.</p>
              </MicroCommitment>
            </ReadingSection>
          )}
           {activeSection === 1 && (
            <ReadingSection title="Your Brain is Plastic." eyebrow="Step 2" icon={BrainCircuit} theme={theme}>
              <p>The single most important discovery in neuroscience is that your brain is not fixed. It physically changes based on what you do. This is called <Highlight description="The brain's ability to reorganize itself by forming new neural connections throughout life. It's the biological basis of learning and memory." theme={theme}>Neuroplasticity</Highlight>. Think of learning a new maths formula like walking through a forest. The first time, it's hard work, and there's no clear path.</p>
              <p>But if you walk that same path every day (i.e., you practice the formula), you wear down a clear trail. In your brain, this is real: the connections between your brain cells (neurons) get stronger, faster, and more efficient. You are literally building the road to knowledge in your head. Every bit of effort you put in is a construction project in your own brain.</p>
              <NeuroplasticityVisualizer />
               <MicroCommitment theme={theme}>
                <p>Pick the one school subject you find hardest. Spend just five minutes tonight reviewing a topic from it. You just sent a work crew to start clearing a new path in your brain's forest.</p>
              </MicroCommitment>
            </ReadingSection>
          )}
           {activeSection === 2 && (
            <ReadingSection title="The Most Powerful Word." eyebrow="Step 3" icon={RotateCcw} theme={theme}>
                <p>A fixed mindset speaks in absolutes: "I can't do this." "I'm not good at this." These are dead ends. They shut down effort and kill motivation. The growth mindset has a simple but incredibly powerful software patch for this bug: the word "yet."</p>
                <p>Adding "yet" to the end of a fixed statement instantly changes it from a verdict into a journey. "I can't do this" becomes "I can't do this... yet." "I'm not good at this" becomes "I'm not good at this... yet." It's a linguistic trick that tells your brain the story isn't over. It opens the door to new strategies and further effort, keeping your motivation circuit online.</p>
                <ReframeChallenge />
                <MicroCommitment theme={theme}>
                    <p>The next time you hear a friend (or yourself) say a "fixed" statement like "I don't get this," add a gentle "...yet?" at the end. You're installing the software patch for them.</p>
                </MicroCommitment>
            </ReadingSection>
          )}
           {activeSection === 3 && (
            <ReadingSection title="Effort is the Real Talent." eyebrow="Step 4" icon={Zap} theme={theme}>
                <p>Our culture loves the myth of "natural talent." We see someone brilliant at something and assume they were just born that way. This is one of the most damaging ideas in education. It teaches us that if something doesn't come easily, we must not be "talented" at it.</p>
                <p>The science of expertise shows this is a lie. Talent is a starting point, but effort is the engine of growth. It is the <Highlight description="Focused, strategic practice that pushes you slightly beyond your current comfort zone. This is the specific type of effort that triggers neuroplasticity and builds skill." theme={theme}>Deliberate Practice</Highlight> that forges the strong neural pathways we saw earlier. A growth mindset understands that effort isn't a sign of weakness; it's the process of getting smarter.</p>
                <MicroCommitment theme={theme}>
                    <p>Identify one area where you rely on "talent". Now, identify one tiny, effortful action you can take to actually improve it. (e.g., If you're 'naturally good' at English, spend 10 minutes learning one new sophisticated word).</p>
                </MicroCommitment>
            </ReadingSection>
          )}
           {activeSection === 4 && (
            <ReadingSection title="Feedback is Fuel, Not a Verdict." eyebrow="Step 5" icon={MessageSquareQuote} theme={theme}>
              <p>A fixed mindset hears criticism and thinks: "They're telling me I'm stupid." It treats feedback as a final verdict on your ability. This is why people with a fixed mindset get defensive or give up when they get a bad grade or tough correction from a teacher.</p>
              <p>A growth mindset hears the exact same criticism and thinks: "They're giving me data I can use to improve." It sees feedback as fuel for the engine. It's not about you, it's about your current strategy. A bad grade isn't a label, it's a diagnostic telling you where the path needs more work. Learning to separate your performance from your identity is a critical upgrade.</p>
              <FeedbackTranslator />
              <MicroCommitment theme={theme}>
                <p>Go back to a piece of work where you got a lower grade than you wanted. Find one comment from the teacher and write down what strategy it's telling you to try next time.</p>
              </MicroCommitment>
            </ReadingSection>
          )}
           {activeSection === 5 && (
            <ReadingSection title="Installing Your Growth OS." eyebrow="Step 6" icon={Activity} theme={theme}>
              <p>A growth mindset isn't a magical incantation. It's a new operating system that you have to consciously choose to run every day. It's built through small, consistent habits: the way you talk to yourself, the way you react to mistakes, and the way you approach a challenge.</p>
              <p>By internalising these ideas, you can start to build an identity based on growth. You stop being "the person who is bad at Maths" and become "the person who is working to get better at Maths." This shift is the foundation of resilience and the key to unlocking your academic potential. It's time to finalise the installation.</p>
               <MicroCommitment theme={theme}>
                <p>Write down your favourite "Growth Mindset Mantra" from this module. Stick it on your bedroom wall, your mirror, or the inside of your school journal. Make it visible.</p>
              </MicroCommitment>
            </ReadingSection>
          )}
        </>
      )}
    </ModuleLayout>
  );
};
export default GrowthMindsetModule;
