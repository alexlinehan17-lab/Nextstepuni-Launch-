

/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
*/

import React, { useState } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import {
  Book, RotateCcw, Brain, Link, Wrench
} from 'lucide-react';
import { ModuleProgress } from '../types';
import { yellowTheme } from '../moduleThemes';
import { Highlight, ReadingSection, MicroCommitment } from './ModuleShared';
import { ModuleLayout } from './ModuleLayout';

const theme = yellowTheme;

// --- INTERACTIVE COMPONENTS ---
const YetReframe = () => {
    const statements = [
      { fixed: "I can't do Honours Maths", yet: "I can't do Honours Maths... yet", shift: "Difficulty = challenge to overcome" },
      { fixed: "I'm terrible at Irish essays", yet: "I'm terrible at Irish essays... yet", shift: "Weakness = area of future growth" },
      { fixed: "I don't understand Chemistry", yet: "I don't understand Chemistry... yet", shift: "Confusion = starting point, not endpoint" },
      { fixed: "I'll never get the points I need", yet: "I'll never get the points I need... yet", shift: "Gap = distance to close, not a wall" },
    ];

    const [activeIndex, setActiveIndex] = useState<number | null>(null);
    const [reframed, setReframed] = useState<Set<number>>(new Set());

    const handleClick = (index: number) => {
      if (reframed.has(index)) return;
      setActiveIndex(index);
      setTimeout(() => {
        setReframed(prev => new Set(prev).add(index));
      }, 600);
    };

    const engagementPct = Math.round((reframed.size / statements.length) * 100);

    return (
      <div className="my-10 p-8 md:p-12 bg-white dark:bg-zinc-800 rounded-xl border border-zinc-200 dark:border-zinc-700">
        <h4 className="font-serif text-2xl font-semibold text-zinc-800 dark:text-white text-center">The "Yet" Reframe</h4>
        <p className="text-center text-sm text-zinc-500 dark:text-zinc-400 mb-8">Click each fixed statement to add "yet" and watch the cognitive shift.</p>

        {/* Engagement meter */}
        <div className="mb-6">
          <div className="flex items-center justify-between mb-1.5">
            <span className="text-[10px] font-bold uppercase tracking-wider text-zinc-400 dark:text-zinc-500">Brain Engagement</span>
            <span className="text-[10px] font-bold text-yellow-600 dark:text-yellow-400">{engagementPct}%</span>
          </div>
          <div className="w-full h-2.5 bg-zinc-100 dark:bg-zinc-900 rounded-full overflow-hidden">
            <motion.div
              className="h-full rounded-full bg-gradient-to-r from-rose-400 via-yellow-400 to-emerald-400"
              animate={{ width: `${engagementPct}%` }}
              transition={{ type: 'spring', stiffness: 80, damping: 15 }}
            />
          </div>
        </div>

        <div className="space-y-3">
          {statements.map((s, i) => {
            const isReframed = reframed.has(i);
            const isAnimating = activeIndex === i && !isReframed;

            return (
              <motion.button
                key={i}
                onClick={() => handleClick(i)}
                disabled={isReframed}
                className={`w-full text-left p-4 rounded-xl border transition-all ${
                  isReframed
                    ? 'bg-emerald-50 dark:bg-emerald-950/20 border-emerald-200 dark:border-emerald-800/40'
                    : 'bg-zinc-50 dark:bg-zinc-900/30 border-zinc-200 dark:border-zinc-700 hover:border-yellow-300 dark:hover:border-yellow-700 cursor-pointer'
                }`}
                layout
              >
                <div className="flex items-start gap-3">
                  {/* Status indicator */}
                  <motion.div
                    animate={{
                      backgroundColor: isReframed ? '#10b981' : '#e4e4e7',
                      scale: isAnimating ? [1, 1.3, 1] : 1,
                    }}
                    className="w-6 h-6 rounded-full flex items-center justify-center flex-shrink-0 mt-0.5"
                  >
                    {isReframed && (
                      <motion.svg
                        initial={{ pathLength: 0 }}
                        animate={{ pathLength: 1 }}
                        transition={{ duration: 0.3 }}
                        viewBox="0 0 16 16"
                        className="w-3.5 h-3.5"
                      >
                        <motion.path
                          d="M3 8 L6.5 11.5 L13 5"
                          fill="none"
                          stroke="white"
                          strokeWidth="2.5"
                          strokeLinecap="round"
                          strokeLinejoin="round"
                          initial={{ pathLength: 0 }}
                          animate={{ pathLength: 1 }}
                        />
                      </motion.svg>
                    )}
                  </motion.div>

                  <div className="flex-1 min-w-0">
                    <AnimatePresence mode="wait">
                      {isReframed ? (
                        <motion.div
                          key="reframed"
                          initial={{ opacity: 0, y: 4 }}
                          animate={{ opacity: 1, y: 0 }}
                        >
                          <p className="font-semibold text-sm text-emerald-700 dark:text-emerald-300">{s.yet}</p>
                          <p className="text-[11px] text-emerald-600/70 dark:text-emerald-400/60 mt-1">{s.shift}</p>
                        </motion.div>
                      ) : (
                        <motion.div key="fixed">
                          <p className={`font-semibold text-sm ${isAnimating ? 'text-rose-500 line-through' : 'text-zinc-700 dark:text-zinc-300'}`}>
                            {s.fixed}
                          </p>
                          {!isAnimating && (
                            <p className="text-[11px] text-zinc-400 dark:text-zinc-500 mt-1">Tap to reframe</p>
                          )}
                        </motion.div>
                      )}
                    </AnimatePresence>
                  </div>
                </div>
              </motion.button>
            );
          })}
        </div>

        {reframed.size === statements.length && (
          <motion.div
            initial={{ opacity: 0, y: 10 }}
            animate={{ opacity: 1, y: 0 }}
            className="mt-6 p-4 bg-yellow-50 dark:bg-yellow-950/20 rounded-xl border border-yellow-200 dark:border-yellow-800/40 text-center"
          >
            <p className="text-sm font-semibold text-yellow-700 dark:text-yellow-300">Every "I can't" is just an "I can't yet" waiting to be unlocked.</p>
            <p className="text-xs text-yellow-600/70 dark:text-yellow-400/60 mt-1">That single word keeps your brain engaged with the error instead of shutting down.</p>
          </motion.div>
        )}

        {reframed.size > 0 && reframed.size < statements.length && (
          <p className="text-center text-xs text-zinc-400 dark:text-zinc-500 mt-4">{statements.length - reframed.size} more to go...</p>
        )}
      </div>
    );
};

const BRIDGE_SCENARIOS = [
  {
    yet: "I can't write good essays... yet",
    goal: "Write H1-level essays",
    strong: [
      "Write one paragraph and compare to the marking scheme",
      "Highlight 3 techniques in a sample H1 essay",
      "Rewrite my weakest paragraph using feedback",
    ],
    weak: [
      "Read more",
      "Try harder next time",
      "Just write longer essays",
    ],
  },
  {
    yet: "I can't solve quadratic equations... yet",
    goal: "Confidently solve quadratics",
    strong: [
      "Do 3 practice problems from Chapter 5 tonight",
      "Watch a worked example and reattempt",
      "Ask my teacher to explain the factoring step",
    ],
    weak: [
      "Try harder",
      "Study more",
      "Hope for the best",
    ],
  },
  {
    yet: "I can't remember History dates... yet",
    goal: "Recall key dates confidently",
    strong: [
      "Make 10 flashcards for the key dates this week",
      "Create a timeline poster for my wall",
      "Test myself every morning for 5 minutes",
    ],
    weak: [
      "Read the chapter again",
      "Try to concentrate more",
      "Highlight everything",
    ],
  },
];

const WEAK_FEEDBACK = [
  "Too vague — what specifically will you do?",
  "That's wishful thinking — name a concrete step.",
  "Not a strategy — try something measurable.",
];

const BridgeBuilder = () => {
  const [scenarioIdx, setScenarioIdx] = useState(0);
  const [placedStrong, setPlacedStrong] = useState<string[]>([]);
  const [usedWeak, setUsedWeak] = useState<Set<string>>(new Set());
  const [feedback, setFeedback] = useState<string | null>(null);
  const [wobbling, setWobbling] = useState<string | null>(null);

  const scenario = BRIDGE_SCENARIOS[scenarioIdx];
  const bridgeComplete = placedStrong.length >= 3;

  const [shuffled, setShuffled] = useState(() => shuffle(scenario.strong, scenario.weak));

  function shuffle(strong: string[], weak: string[]) {
    const arr = [...strong, ...weak];
    for (let i = arr.length - 1; i > 0; i--) {
      const j = Math.floor(Math.random() * (i + 1));
      [arr[i], arr[j]] = [arr[j], arr[i]];
    }
    return arr;
  }

  const handleNewScenario = () => {
    const next = (scenarioIdx + 1) % BRIDGE_SCENARIOS.length;
    setScenarioIdx(next);
    setPlacedStrong([]);
    setUsedWeak(new Set());
    setFeedback(null);
    setWobbling(null);
    const s = BRIDGE_SCENARIOS[next];
    setShuffled(shuffle(s.strong, s.weak));
  };

  const handleAction = (action: string) => {
    if (bridgeComplete) return;
    if (placedStrong.includes(action) || usedWeak.has(action)) return;

    const isStrong = scenario.strong.includes(action);

    if (isStrong) {
      setPlacedStrong(prev => [...prev, action]);
      setFeedback(null);
      setWobbling(null);
    } else {
      const weakIdx = scenario.weak.indexOf(action);
      const msg = WEAK_FEEDBACK[weakIdx >= 0 && weakIdx < WEAK_FEEDBACK.length ? weakIdx : 0];
      setWobbling(action);
      setFeedback(msg);
      setTimeout(() => {
        setUsedWeak(prev => new Set(prev).add(action));
        setWobbling(null);
        setFeedback(null);
      }, 1500);
    }
  };

  const MotionDiv = motion.div as any;

  return (
    <div className="my-10 p-8 md:p-12 bg-white dark:bg-zinc-800 rounded-xl border border-zinc-200 dark:border-zinc-700">
      <h4 className="font-serif text-2xl font-semibold text-zinc-800 dark:text-white text-center">
        Bridge Builder
      </h4>
      <p className="text-center text-sm text-zinc-500 dark:text-zinc-400 mb-2">
        Build a bridge from "Yet" to your goal by choosing <strong>specific, concrete</strong> actions.
      </p>
      <p className="text-center text-xs font-semibold text-yellow-600 dark:text-yellow-400 mb-8">
        Bridge strength: {placedStrong.length}/3 planks
      </p>

      {/* Bridge Scene */}
      <div className="relative flex items-end justify-center gap-0 mb-8 select-none" style={{ minHeight: 180 }}>
        {/* Left cliff */}
        <div className="flex flex-col items-center z-10">
          <div className="bg-zinc-300 dark:bg-zinc-600 rounded-t-xl w-28 md:w-36 h-24 flex items-center justify-center px-2">
            <p className="text-[11px] md:text-xs font-semibold text-zinc-700 dark:text-zinc-200 text-center leading-tight">
              {scenario.yet}
            </p>
          </div>
          <div className="bg-zinc-400 dark:bg-zinc-700 w-28 md:w-36 h-4 rounded-b-sm" />
        </div>

        {/* Bridge gap */}
        <div className="relative flex-1 max-w-[240px] md:max-w-[300px]" style={{ minHeight: 120 }}>
          {/* Chasm background */}
          <div className="absolute bottom-0 left-0 right-0 h-12 bg-gradient-to-t from-zinc-200 dark:from-zinc-900 to-transparent rounded-b-lg" />

          {/* Planks */}
          <div className="absolute bottom-4 left-0 right-0 flex gap-1 justify-center items-end px-1">
            {[0, 1, 2].map(i => {
              const placed = i < placedStrong.length;
              return (
                <MotionDiv
                  key={i}
                  initial={placed ? { opacity: 0, y: -30, rotateZ: -5 } : { opacity: 0.3 }}
                  animate={
                    placed
                      ? { opacity: 1, y: 0, rotateZ: 0 }
                      : { opacity: 0.15 }
                  }
                  transition={{ type: 'spring', stiffness: 200, damping: 18, delay: placed ? 0.1 : 0 }}
                  className={`h-5 md:h-6 rounded-sm flex items-center justify-center ${
                    placed
                      ? 'bg-emerald-400 dark:bg-emerald-500 shadow-md'
                      : 'bg-zinc-200 dark:bg-zinc-700 border border-dashed border-zinc-300 dark:border-zinc-600'
                  }`}
                  style={{ flex: 1, minWidth: 0 }}
                >
                  {placed && (
                    <span className="text-[8px] md:text-[9px] font-bold text-white truncate px-1">
                      Plank {i + 1}
                    </span>
                  )}
                </MotionDiv>
              );
            })}
          </div>

          {/* Wobbling weak plank overlay */}
          <AnimatePresence>
            {wobbling && (
              <MotionDiv
                key="wobble"
                initial={{ opacity: 0, y: -20 }}
                animate={{
                  opacity: [0, 1, 1, 0],
                  y: [-20, 0, 0, 40],
                  rotateZ: [0, -3, 3, 8],
                }}
                exit={{ opacity: 0 }}
                transition={{ duration: 1.5, times: [0, 0.15, 0.7, 1] }}
                className="absolute bottom-4 left-1/2 -translate-x-1/2 h-5 md:h-6 w-1/3 rounded-sm bg-rose-400 dark:bg-rose-500 shadow-md flex items-center justify-center"
              >
                <span className="text-[8px] md:text-[9px] font-bold text-white">Crack!</span>
              </MotionDiv>
            )}
          </AnimatePresence>
        </div>

        {/* Right cliff */}
        <div className="flex flex-col items-center z-10">
          <div className="bg-emerald-200 dark:bg-emerald-900/60 rounded-t-xl w-28 md:w-36 h-24 flex items-center justify-center px-2 border border-emerald-300 dark:border-emerald-800/50">
            <p className="text-[11px] md:text-xs font-semibold text-emerald-700 dark:text-emerald-300 text-center leading-tight">
              {scenario.goal}
            </p>
          </div>
          <div className="bg-emerald-300 dark:bg-emerald-800 w-28 md:w-36 h-4 rounded-b-sm" />
        </div>
      </div>

      {/* Feedback banner */}
      <AnimatePresence>
        {feedback && (
          <MotionDiv
            key="feedback"
            initial={{ opacity: 0, y: -6 }}
            animate={{ opacity: 1, y: 0 }}
            exit={{ opacity: 0, y: -6 }}
            className="mb-4 p-3 rounded-lg bg-rose-50 dark:bg-rose-950/20 border border-rose-200 dark:border-rose-800/40 text-center"
          >
            <p className="text-xs font-semibold text-rose-600 dark:text-rose-400">{feedback}</p>
          </MotionDiv>
        )}
      </AnimatePresence>

      {/* Completion celebration */}
      <AnimatePresence>
        {bridgeComplete && (
          <MotionDiv
            key="celebrate"
            initial={{ opacity: 0, scale: 0.9 }}
            animate={{ opacity: 1, scale: 1 }}
            className="mb-4 p-4 rounded-xl bg-emerald-50 dark:bg-emerald-950/20 border border-emerald-200 dark:border-emerald-800/40 text-center"
          >
            <p className="text-base font-bold text-emerald-700 dark:text-emerald-300">
              Bridge Complete!
            </p>
            <p className="text-xs text-emerald-600/80 dark:text-emerald-400/70 mt-1">
              With specific actions, "yet" becomes a launchpad, not a wish.
            </p>
          </MotionDiv>
        )}
      </AnimatePresence>

      {/* Action blocks */}
      {!bridgeComplete && (
        <div>
          <p className="text-xs font-bold uppercase tracking-widest text-zinc-400 dark:text-zinc-500 mb-3 text-center">
            Choose an action to place on the bridge
          </p>
          <div className="grid grid-cols-1 sm:grid-cols-2 gap-2 max-w-xl mx-auto">
            {shuffled.map(action => {
              const isPlaced = placedStrong.includes(action);
              const isDiscarded = usedWeak.has(action);
              const isWobbling = wobbling === action;
              const disabled = isPlaced || isDiscarded || isWobbling;

              return (
                <MotionDiv
                  key={action}
                  whileHover={!disabled ? { scale: 1.02 } : {}}
                  whileTap={!disabled ? { scale: 0.98 } : {}}
                  onClick={() => !disabled && handleAction(action)}
                  className={`p-3 rounded-lg border text-left text-sm transition-colors ${
                    isPlaced
                      ? 'bg-emerald-50 dark:bg-emerald-950/20 border-emerald-200 dark:border-emerald-800/40 text-emerald-600 dark:text-emerald-400 opacity-60'
                      : isDiscarded
                        ? 'bg-zinc-100 dark:bg-zinc-900/40 border-zinc-200 dark:border-zinc-700 text-zinc-400 dark:text-zinc-600 line-through opacity-40'
                        : 'bg-zinc-50 dark:bg-zinc-900/30 border-zinc-200 dark:border-zinc-700 text-zinc-700 dark:text-zinc-300 hover:border-yellow-300 dark:hover:border-yellow-700 cursor-pointer'
                  }`}
                >
                  {action}
                </MotionDiv>
              );
            })}
          </div>
        </div>
      )}

      {/* New Scenario button */}
      <div className="mt-6 text-center">
        <button
          onClick={handleNewScenario}
          className="text-xs font-semibold text-yellow-600 dark:text-yellow-400 hover:text-yellow-700 dark:hover:text-yellow-300 transition-colors underline underline-offset-2"
        >
          New Scenario
        </button>
      </div>
    </div>
  );
};

const YetAudit = () => {
    const [block, setBlock] = useState('');
    const [action, setAction] = useState('');

    return (
        <div className="my-10 p-8 md:p-12 bg-white dark:bg-zinc-800 rounded-xl border border-zinc-200 dark:border-zinc-700">
            <h4 className="font-serif text-2xl font-semibold text-zinc-800 dark:text-white text-center">Your "Yet" Audit</h4>
            <p className="text-center text-sm text-zinc-500 dark:text-zinc-400 mb-8">Run your own block through the Identify-Append-Bridge protocol.</p>
            <div className="space-y-6 max-w-xl mx-auto">
                <div>
                    <p className="text-xs font-bold uppercase tracking-widest text-yellow-600 dark:text-yellow-400 mb-2">1. Identify the Block</p>
                    <input value={block} onChange={e => setBlock(e.target.value)} placeholder="e.g., I can't write a good Irish essay" className="w-full bg-zinc-50 dark:bg-zinc-900/50 rounded-lg p-3 text-sm text-zinc-800 dark:text-zinc-200 border border-zinc-200 dark:border-zinc-700 focus:outline-none focus:ring-2 focus:ring-yellow-400"/>
                </div>
                <div>
                    <p className="text-xs font-bold uppercase tracking-widest text-yellow-600 dark:text-yellow-400 mb-2">2. Add "Yet"</p>
                    <div className={`p-3 rounded-lg text-sm min-h-[44px] border ${block ? 'bg-emerald-50 dark:bg-emerald-950/20 border-emerald-200 dark:border-emerald-800/40 text-emerald-700 dark:text-emerald-300' : 'bg-zinc-50 dark:bg-zinc-900/50 border-zinc-200 dark:border-zinc-700 text-zinc-400 dark:text-zinc-500'}`}>
                        {block ? `${block}... yet.` : '...'}
                    </div>
                </div>
                <div>
                    <p className="text-xs font-bold uppercase tracking-widest text-yellow-600 dark:text-yellow-400 mb-2">3. Bridge to Action</p>
                    <input value={action} onChange={e => setAction(e.target.value)} placeholder="...so I will ask my teacher for one example tomorrow." className="w-full bg-zinc-50 dark:bg-zinc-900/50 rounded-lg p-3 text-sm text-zinc-800 dark:text-zinc-200 border border-zinc-200 dark:border-zinc-700 focus:outline-none focus:ring-2 focus:ring-yellow-400"/>
                </div>
            </div>
        </div>
    );
}


// --- MODULE COMPONENT ---
const ThePowerOfYetModule: React.FC<{ onBack: () => void; progress: ModuleProgress; onProgressUpdate: (progress: ModuleProgress) => void }> = ({ onBack, progress, onProgressUpdate }) => {
  const sections = [
    { id: 'full-stop', title: 'The Full Stop', eyebrow: '01 // The Verdict', icon: Book },
    { id: 'software-patch', title: 'The Software Patch', eyebrow: '02 // The "Yet" Upgrade', icon: RotateCcw },
    { id: 'brain-on-yet', title: 'The Brain on "Yet"', eyebrow: '03 // The Science', icon: Brain },
    { id: 'action-bridge', title: 'The Action Bridge', eyebrow: '04 // The Protocol', icon: Link },
    { id: 'yet-audit', title: 'Your "Yet" Audit', eyebrow: '05 // The Blueprint', icon: Wrench },
  ];

  return (
    <ModuleLayout
      moduleNumber="07"
      moduleTitle='The Power of "Yet"'
      moduleSubtitle="The Persistence Playbook"
      moduleDescription="One tiny word that changes everything about how you handle setbacks. This module gives you a dead-simple three-step method to stop beating yourself up when things go wrong and start actually moving forward."
      theme={theme}
      sections={sections}
      onBack={onBack}
      progress={progress}
      onProgressUpdate={onProgressUpdate}
    >
      {(activeSection) => (
        <>
          {activeSection === 0 && (
            <ReadingSection title="The Full Stop." eyebrow="Step 1" icon={Book} theme={theme}>
              <p>When you say "I can't do Honours Maths" or "I'm not good at this," you're putting a full stop at the end of the sentence. Your brain takes that as a <Highlight description="Basically, you're telling yourself the story is over and you've hit your limit. It shuts the door on even trying." theme={theme}>final verdict</Highlight>. It's like saying: "That's it. I'm done. There's nothing more I can do."</p>
              <p>This is what happens when you're stuck in a <Highlight description="The idea that you're either smart or you're not, and there's nothing you can do about it. When you think this way, every bad result feels like proof you're just not good enough." theme={theme}>Fixed Mindset</Highlight>. It's a dead end. It kills your motivation and tells your brain to give up on the problem. To keep going when things get tough, you need to learn to turn those full stops into commas.</p>
            </ReadingSection>
          )}
           {activeSection === 1 && (
            <ReadingSection title="The Software Patch." eyebrow="Step 2" icon={RotateCcw} theme={theme}>
              <p>The fix is surprisingly simple: the word "yet." Just stick it on the end of any "I can't" statement and the whole meaning changes. "I can't do this" becomes "I can't do this... yet." "I don't understand this" becomes "I don't understand this... yet."</p>
              <p>That one word turns a final verdict into a progress update. It reminds you that <Highlight description="Where you are right now isn't where you'll always be. You're just at one point on the journey, not the end of it." theme={theme}>where you are now isn't where you'll stay</Highlight>. A school in Chicago actually replaced "Fail" grades with "Not Yet" on report cards, and students started trying harder and finishing more work. You're not a failure -- you're just not finished.</p>
              <MicroCommitment theme={theme}>
                <p>Listen to yourself and your friends today. Every time you hear an "I can't" statement, mentally add "yet" to the end of it. Just notice how it changes the feeling.</p>
              </MicroCommitment>
            </ReadingSection>
          )}
          {activeSection === 2 && (
            <ReadingSection title="The Brain on 'Yet'." eyebrow="Step 3" icon={Brain} theme={theme}>
              <p>This isn't just a feel-good trick -- it actually changes what's happening inside your head. When you make a mistake, your brain fires off an <Highlight description="A burst of brain activity that happens when you notice you've made a mistake. The stronger this signal is, the more your brain is actually paying attention to the error and learning from it." theme={theme}>error-attention signal</Highlight>. It's basically your brain saying, "Hold on, let me look at what went wrong here."</p>
              <p>When people believe they can't improve, their brain spots the mistake but then quickly looks away -- like it's trying to protect their ego. But when people believe they can grow, their brain locks onto the mistake and really digs into it. The word "yet" keeps your brain in that locked-on mode. It's like telling your brain, "This isn't over, stay focused," instead of letting it shut down and move on.</p>
              <YetReframe />
            </ReadingSection>
          )}
           {activeSection === 3 && (
            <ReadingSection title="The Action Bridge." eyebrow="Step 4" icon={Link} theme={theme}>
                <p>"Yet" is powerful, but on its own it's just a nice thought. To actually make a difference, you need to follow it up with a real plan. That's the crucial third step: the <Highlight description="The specific, concrete thing you're going to do next to move from 'can't do it' to 'can do it'. It stops 'yet' from being empty words and turns it into actual progress." theme={theme}>Bridge to Action</Highlight>.</p>
                <p>The full sentence isn't just "I can't do this yet." It's "I can't do this yet, *so I will*..." That extra bit stops "yet" from being an excuse and turns it into a starting point. It connects the positive thinking to an actual next step. Here's the full method: <strong>1. Identify the Block, 2. Add "Yet", 3. Bridge to Action.</strong></p>
                <BridgeBuilder />
                <MicroCommitment theme={theme}>
                  <p>Think of your toughest subject. Your Block might be "I can't understand Topic X." Your Bridge could be "I will watch one YouTube video explaining it tonight."</p>
                </MicroCommitment>
            </ReadingSection>
          )}
           {activeSection === 4 && (
            <ReadingSection title="Your 'Yet' Audit." eyebrow="Step 5" icon={Wrench} theme={theme}>
              <p>You've got the full method now. It's a way to catch yourself in those "I can't" moments and turn them into something useful instead of spiralling. The last step is to actually use it on something real.</p>
              <p>Use the tool below to pick one thing you're genuinely struggling with right now. Run it through the three steps: name the block, add "yet", then figure out your next move. This isn't just practice -- it's you, right now, changing how you deal with the hard stuff.</p>
              <YetAudit />
            </ReadingSection>
          )}
        </>
      )}
    </ModuleLayout>
  );
};
export default ThePowerOfYetModule;
