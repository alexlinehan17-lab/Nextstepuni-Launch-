

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

const YetAudit = () => {
    const [block, setBlock] = useState('');
    const [action, setAction] = useState('');

    return (
        <div className="my-10 p-8 md:p-12 bg-zinc-900 rounded-xl border border-white/10 text-white">
            <h4 className="font-serif text-3xl font-semibold text-center mb-8">Your "Yet" Audit</h4>
            <div className="space-y-6 max-w-xl mx-auto">
                <div>
                    <p className="text-xs font-bold uppercase tracking-widest text-yellow-400 mb-2">1. IDENTIFY THE BLOCK</p>
                    <input value={block} onChange={e => setBlock(e.target.value)} placeholder="e.g., I can't write a good Irish essay" className="w-full bg-white dark:bg-zinc-800/5 rounded-lg p-3 text-sm text-zinc-300 focus:outline-none focus:ring-2 focus:ring-yellow-400"/>
                </div>
                <div>
                    <p className="text-xs font-bold uppercase tracking-widest text-yellow-400 mb-2">2. ADD "YET"</p>
                    <div className="p-3 bg-white dark:bg-zinc-800/10 rounded-lg text-sm text-zinc-300 min-h-[44px]">
                        {block ? `I can't write a good Irish essay... yet.` : <span className="opacity-50">...</span>}
                    </div>
                </div>
                <div>
                    <p className="text-xs font-bold uppercase tracking-widest text-yellow-400 mb-2">3. BRIDGE TO ACTION</p>
                    <input value={action} onChange={e => setAction(e.target.value)} placeholder="...so I will ask my teacher for one example tomorrow." className="w-full bg-white dark:bg-zinc-800/5 rounded-lg p-3 text-sm text-zinc-300 focus:outline-none focus:ring-2 focus:ring-yellow-400"/>
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
              <p>When you say "I can't do Honours Maths" or "I'm not good at this," you're putting a full stop at the end of the sentence. Your brain interprets this as a <Highlight description="A final judgment on your ability, suggesting you have reached the limit of your capacity. It closes the door on future effort." theme={theme}>summative judgment</Highlight>. It's a verdict that says: "This story is over. You were found wanting."</p>
              <p>This is the language of a <Highlight description="The belief that intelligence and abilities are fixed, unchangeable traits. People with this mindset see failure as a diagnosis of their incompetence." theme={theme}>Fixed Mindset</Highlight>. It's a dead end. It shuts down effort, kills motivation, and tells your brain to disengage from the problem. To build resilience, you need to learn to turn these full stops into commas.</p>
            </ReadingSection>
          )}
           {activeSection === 1 && (
            <ReadingSection title="The Software Patch." eyebrow="Step 2" icon={RotateCcw} theme={theme}>
              <p>The solution is a simple but profound software patch for your brain: the word "yet." By adding this single word to the end of a fixed statement, you fundamentally change its meaning. "I can't do this" becomes "I can't do this... yet." "I don't understand this" becomes "I don't understand this... yet."</p>
              <p>This transforms the sentence from a final verdict into a progress report. It implies a <Highlight description="A sense that your current ability is just one point on a longer journey of learning, not a permanent state." theme={theme}>temporal trajectory</Highlight>. A famous study in a Chicago high school replaced "Fail" grades with "Not Yet." The result was a dramatic increase in persistence and task completion. You're not a failure; you're just unfinished.</p>
              <MicroCommitment theme={theme}>
                <p>Listen to yourself and your friends today. Every time you hear an "I can't" statement, mentally add "yet" to the end of it. Just notice how it changes the feeling.</p>
              </MicroCommitment>
            </ReadingSection>
          )}
          {activeSection === 2 && (
            <ReadingSection title="The Brain on 'Yet'." eyebrow="Step 3" icon={Brain} theme={theme}>
              <p>This isn't just a mental trick; it has a direct effect on your brain's hardware. When you make a mistake, your brain produces a signal called the <Highlight description="The 'Error Positivity' signal is a brainwave that shows you're paying conscious attention to a mistake. A bigger 'Pe' wave means you're more likely to learn from the error." theme={theme}>Pe (Error Positivity)</Highlight>. It's the physical sign that you're leaning in to analyse your failure.</p>
              <p>Research shows that people with a fixed mindset have a very small Pe signal. Their brain detects the error but quickly "looks away" to protect the ego. People with a growth mindset have a huge Pe signal--they allocate massive attention to the mistake. The word "yet" is a cognitive cue that tells your brain, "This task is not over," keeping your brain in that high-Pe state of engagement and analysis.</p>
              <YetReframe />
            </ReadingSection>
          )}
           {activeSection === 3 && (
            <ReadingSection title="The Action Bridge." eyebrow="Step 4" icon={Link} theme={theme}>
                <p>"Yet" is powerful, but it's not magic. On its own, it's just wishful thinking. To be effective, "yet" must be tethered to a behavioral plan. This is the crucial third step of the protocol: the <Highlight description="A concrete, specific action that you will take to move from 'not yet' to 'can'. This tethers optimism to a behavioral plan." theme={theme}>Bridge to Action</Highlight>.</p>
                <p>The full, powerful sentence isn't just "I can't do this yet." It's "I can't do this yet, *so I will*..." This simple addition prevents "Yet" from being an excuse and turns it into a launchpad. It links the optimistic mindset to a concrete, strategic next step. This is the full protocol: <strong>1. Identify the Block, 2. Add "Yet", 3. Bridge to Action.</strong></p>
                <MicroCommitment theme={theme}>
                  <p>Think of your toughest subject. Your Block might be "I can't understand Topic X." Your Bridge could be "I will watch one YouTube video explaining it tonight."</p>
                </MicroCommitment>
            </ReadingSection>
          )}
           {activeSection === 4 && (
            <ReadingSection title="Your 'Yet' Audit." eyebrow="Step 5" icon={Wrench} theme={theme}>
              <p>You now have the full protocol. It's a tool for rewriting your internal monologue in real-time, turning moments of despair into moments of strategic action. The final step is to apply it to your own life.</p>
              <p>Use the blueprint below to identify one specific academic block you're facing. Then, run it through the "Identify-Append-Bridge" protocol. This isn't just an exercise; it's you, right now, actively rewiring your brain for resilience. This is how you turn the science into a skill.</p>
              <YetAudit />
            </ReadingSection>
          )}
        </>
      )}
    </ModuleLayout>
  );
};
export default ThePowerOfYetModule;
