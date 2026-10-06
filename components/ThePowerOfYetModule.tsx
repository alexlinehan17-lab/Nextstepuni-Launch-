import { BrandedBridge,InstructionList } from './learning/BrandedFeatures';
import { moduleFill } from './learning/brandTokens';


/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
*/

import { AnimatePresence,motion } from 'framer-motion';
import {
Book,
Brain,Link,
RotateCcw,
Wrench
} from 'lucide-react';
import React,{ useEffect,useRef,useState } from 'react';
import { POWER_OF_YET_REFERENCE_LIST } from '../data/references/powerOfYet';
import { useEssentialsMode } from '../hooks/useEssentialsMode';
import { yellowTheme } from '../moduleThemes';
import { type ModuleProgress } from '../types';
import { ModuleLayout } from './ModuleLayout';
import { Cite } from './ModuleReferences';
import { Highlight,MicroCommitment,ReadingSection } from './ModuleShared';

const theme = yellowTheme;

// --- INTERACTIVE COMPONENTS ---
const YetReframe = () => {
    const statements = [
      { fixed: "I can't do Honours Maths", yet: "I can't do Honours Maths... yet", shift: "Difficulty = challenge to overcome" },
      { fixed: "I can't write a strong Irish essay", yet: "I can't write a strong Irish essay... yet", shift: "Weakness = area of future growth" },
      { fixed: "I don't understand Chemistry", yet: "I don't understand Chemistry... yet", shift: "Confusion = starting point, not endpoint" },
      { fixed: "I haven't reached the grades I need", yet: "I haven't reached the grades I need... yet", shift: "Gap = distance to close, not a wall" },
    ];

    const [activeIndex, setActiveIndex] = useState<number | null>(null);
    const [reframed, setReframed] = useState<Set<number>>(new Set());
    const reframeTimerRef = useRef<ReturnType<typeof setTimeout> | null>(null);

    useEffect(() => {
      return () => {
        if (reframeTimerRef.current) clearTimeout(reframeTimerRef.current);
      };
    }, []);

    const handleClick = (index: number) => {
      if (reframed.has(index)) return;
      setActiveIndex(index);
      reframeTimerRef.current = setTimeout(() => {
        setReframed(prev => new Set(prev).add(index));
      }, 600);
    };

    const engagementPct = Math.round((reframed.size / statements.length) * 100);

    return <div className="wr-skin" data-wide="YetReframe"><div className="my-10 rounded-2xl p-6 md:p-8" style={{ backgroundColor: "var(--module-surface)", borderRadius: 18 }}>
        <h4 className="font-serif text-2xl font-semibold text-[var(--module-ink)] dark:text-[var(--module-ink)] text-center">The "Yet" Reframe</h4>
        <p className="text-center text-sm text-[var(--module-muted)] dark:text-[var(--module-muted)] mb-8">Click each fixed statement to add "yet" and watch the cognitive shift.</p>

        {/* Engagement meter */}
        <div className="mb-6">
          <div className="flex items-center justify-between mb-1.5">
            <span className="text-[10px] font-bold uppercase tracking-wider text-[var(--module-muted)] dark:text-[var(--module-muted)]">Brain Engagement</span>
            <span className="text-[10px] font-bold text-[var(--module-ink)] dark:text-[var(--module-ink)]">{engagementPct}%</span>
          </div>
          <div className="w-full h-2.5 bg-[var(--module-surface)] dark:bg-[var(--module-surface)] rounded-full overflow-hidden">
            <motion.div
              className="h-full rounded-full bg-[var(--module-orange)] from-[var(--module-orange)] via-[var(--module-orange)] to-[var(--module-orange)]"
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
                className="w-full text-left p-4 rounded-xl transition-all"
                style={isReframed ? { backgroundColor: "var(--module-success-soft)", border: "2.5px solid var(--module-line)", borderRadius: 14, boxShadow: 'none' } : { backgroundColor: "var(--module-surface)", border: "2.5px solid var(--module-line)", borderRadius: 14, boxShadow: 'none' }}
                layout data-wide-button="true" data-selected={!!(isReframed)} data-tone="mint" aria-pressed={!!(isReframed)}
              >
                <div className="flex items-start gap-3">
                  {/* Status indicator */}
                  <motion.div
                    animate={{
                      backgroundColor: moduleFill(isReframed ? "var(--module-success)" : "var(--module-surface)"),
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
                          <p className="font-semibold text-sm text-[var(--module-success-text)] dark:text-[var(--module-success-text)]">{s.yet}</p>
                          <p className="text-[11px] text-[var(--module-success-text)] dark:text-[var(--module-success-text)] mt-1">{s.shift}</p>
                        </motion.div>
                      ) : (
                        <motion.div key="fixed">
                          <p className={`font-semibold text-sm ${isAnimating ? "text-[var(--module-danger-text)] line-through" : "text-[var(--module-ink)] dark:text-[var(--module-muted)]"}`}>
                            {s.fixed}
                          </p>
                          {!isAnimating && (
                            <p className="text-[11px] text-[var(--module-muted)] dark:text-[var(--module-muted)] mt-1">Tap to reframe</p>
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
            className="mt-6 p-4 bg-[var(--module-surface)] dark:bg-[var(--module-surface)] rounded-xl border border-[var(--module-line)] dark:border-[var(--module-line)] text-center"
          >
            <p className="text-sm font-semibold text-[var(--module-ink)] dark:text-[var(--module-ink)]">Every "I can't" is just an "I can't yet" waiting to be unlocked.</p>
            <p className="text-xs text-[var(--module-ink)] dark:text-[var(--module-ink)] mt-1">That single word keeps your brain engaged with the error instead of shutting down.</p>
          </motion.div>
        )}

        {reframed.size > 0 && reframed.size < statements.length && (
          <p className="text-center text-xs text-[var(--module-muted)] dark:text-[var(--module-muted)] mt-4">{statements.length - reframed.size} more to go...</p>
        )}
      </div></div>;
};

const BRIDGE_SCENARIOS = [
  {
    yet: "I can't write good essays... yet",
    goal: "Write top-grade essays",
    strong: [
      "Write one paragraph and compare to the marking scheme",
      "Highlight 3 techniques in a sample top-grade essay",
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

const BridgeBuilder = () => <BrandedBridge scenarios={BRIDGE_SCENARIOS} />;

const YetAudit = () => {
    const [block, setBlock] = useState('');
    const [action, setAction] = useState('');

    return <div className="wr-skin" data-wide="YetAudit"><div className="my-10 rounded-2xl p-6 md:p-8" style={{ backgroundColor: "var(--module-surface)", borderRadius: 18 }}>
            <h4 className="font-serif text-2xl font-semibold text-[var(--module-ink)] dark:text-[var(--module-ink)] text-center">Your "Yet" Audit</h4>
            <p className="text-center text-sm text-[var(--module-muted)] dark:text-[var(--module-muted)] mb-8">Run your own block through the Identify-Append-Bridge protocol.</p>
            <div className="space-y-6 max-w-xl mx-auto">
                <div>
                    <p className="text-xs font-bold uppercase tracking-widest text-[var(--module-ink)] dark:text-[var(--module-ink)] mb-2">1. Identify the Block</p>
                    <input aria-label="Identify the block" value={block} onChange={e => setBlock(e.target.value)} placeholder="e.g., I can't write a good Irish essay" className="w-full bg-[var(--module-surface)] dark:bg-[var(--module-surface)] rounded-xl px-5 py-3.5 text-sm font-medium text-[var(--module-ink)] dark:text-[var(--module-ink)] placeholder-zinc-400 outline-none transition-all" style={{ border: "1.5px solid var(--module-line)" }}/>
                </div>
                <div>
                    <p className="text-xs font-bold uppercase tracking-widest text-[var(--module-ink)] dark:text-[var(--module-ink)] mb-2">2. Add "Yet"</p>
                    <div role="status" aria-live="polite" data-filled={!!block} className="p-3 rounded-lg text-sm min-h-[44px]" style={block ? { backgroundColor: "var(--module-success-soft)", border: "2px solid var(--module-line)", color: "var(--module-success-text)" } : { backgroundColor: "var(--module-surface)", border: "1.5px solid var(--module-line)", color: "var(--module-muted)" }}>
                        {block ? `${block}... yet.` : '...'}
                    </div>
                </div>
                <div>
                    <p className="text-xs font-bold uppercase tracking-widest text-[var(--module-ink)] dark:text-[var(--module-ink)] mb-2">3. Bridge to Action</p>
                    <input aria-label="Bridge to action" value={action} onChange={e => setAction(e.target.value)} placeholder="...so I will ask my teacher for one example tomorrow." className="w-full bg-[var(--module-surface)] dark:bg-[var(--module-surface)] rounded-xl px-5 py-3.5 text-sm font-medium text-[var(--module-ink)] dark:text-[var(--module-ink)] placeholder-zinc-400 outline-none transition-all" style={{ border: "1.5px solid var(--module-line)" }}/>
                </div>
            </div>
        </div></div>;
}

// --- MODULE COMPONENT ---
const ThePowerOfYetModule: React.FC<{ onBack: () => void; progress: ModuleProgress; onProgressUpdate: (progress: ModuleProgress) => void }> = ({ onBack, progress, onProgressUpdate }) => {
  const essentials = useEssentialsMode();
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
      references={POWER_OF_YET_REFERENCE_LIST}
      finishButtonText="Add Your 'Yet'"
    >
      {(activeSection) => (
        <>
          {activeSection === 0 && (
            <ReadingSection title="The Full Stop." eyebrow="Step 1" icon={Book} theme={theme}>
              {essentials ? (
                <>
                  <p>When you say "I can't do this," your brain treats it as a final verdict. It shuts down and stops trying. This is a <strong>fixed mindset</strong> -- the belief that you either have it or you do not.</p>
                  <p>You need to turn those full stops into commas. That is what this module teaches you to do.</p>
                </>
              ) : (
                <>
                  <p>When you say "I can't do Honours Maths" or "I'm not good at this," you're putting a full stop at the end of the sentence. Your brain takes that as a <Highlight description="Basically, you're telling yourself the story is over and you've hit your limit. It shuts the door on even trying." theme={theme}>final verdict</Highlight>. It's like saying: "That's it. I'm done. There's nothing more I can do."</p>
                  <p>This is what happens when you're stuck in a <Highlight description="The idea that you're either smart or you're not, and there's nothing you can do about it. When you think this way, every bad result feels like proof you're just not good enough." theme={theme}>Fixed Mindset</Highlight>. It's a dead end. It kills your motivation and tells your brain to give up on the problem. To keep going when things get tough, you need to learn to turn those full stops into commas.</p>
                </>
              )}
            </ReadingSection>
          )}
           {activeSection === 1 && (
            <ReadingSection title="The Software Patch." eyebrow="Step 2" icon={RotateCcw} theme={theme}>
              {essentials ? (
                <>
                  <p>The fix is one word: <strong>"yet."</strong> Stick it on the end of any "I can't" statement. "I can't do this" becomes "I can't do this... yet." It turns a verdict into a progress update.</p>
                  <p>Some schools have even replaced the grade "Fail" with "Not Yet" to send that exact message. You are not a failure. You are just not finished.</p>
                </>
              ) : (
                <>
                  <p>The fix is surprisingly simple: the word "yet." Just stick it on the end of any "I can't" statement and the whole meaning changes. "I can't do this" becomes "I can't do this... yet." "I don't understand this" becomes "I don't understand this... yet."</p>
                  <p>That one word turns a final verdict into a progress update. It reminds you that <Highlight description="Where you are right now isn't where you'll always be. You're just at one point on the journey, not the end of it." theme={theme}>where you are now isn't where you'll stay</Highlight>. Some schools have even swapped "Fail" grades for "Not Yet" on report cards to send that exact message — a failed test isn't a verdict, it's just a checkpoint you haven't passed yet. You're not a failure -- you're just not finished.</p>
                </>
              )}
              <MicroCommitment theme={theme}>
                <p>Listen to yourself and your friends today. Every time you hear an "I can't" statement, mentally add "yet" to the end of it. Just notice how it changes the feeling.</p>
              </MicroCommitment>
            </ReadingSection>
          )}
          {activeSection === 2 && (
            <ReadingSection title="The Brain on 'Yet'." eyebrow="Step 3" icon={Brain} theme={theme}>
              {essentials ? (
                <>
                  <p>When you make a mistake, your brain fires an error signal. If you believe you cannot improve, your brain tends to look away from the mistake. If you believe you can grow, your brain tends to lock on and learn from it.<Cite n={1} /></p>
                  <p>"Yet" helps keep your brain in that locked-on mode. It tells your brain to stay focused on the error instead of shutting down.</p>
                </>
              ) : (
                <>
                  <p>This isn't just a feel-good trick -- it actually changes what's happening inside your head. When you make a mistake, your brain fires off an <Highlight description="A burst of brain activity that happens when you notice you've made a mistake. The stronger this signal is, the more your brain is actually paying attention to the error and learning from it." theme={theme}>error-attention signal</Highlight>. It's basically your brain saying, "Hold on, let me look at what went wrong here."</p>
                  <p>In one study, people who believed they couldn't improve showed a weaker version of this signal — their brain spotted the mistake but quickly looked away, as if to protect the ego. People who believed they could grow showed a stronger signal: their brain locked onto the mistake and dug into it.<Cite n={1} /> The word "yet" helps keep your brain in that locked-on mode. It's like telling your brain, "This isn't over, stay focused," instead of letting it shut down and move on.</p>
                </>
              )}
              <YetReframe />
            </ReadingSection>
          )}
           {activeSection === 3 && (
            <ReadingSection title="The Action Bridge." eyebrow="Step 4" icon={Link} theme={theme}>
                {essentials ? (
                  <p>"Yet" alone is just a nice thought. You need a real plan. The full sentence is: "I can't do this yet, <strong>so I will...</strong>" Follow "yet" with a specific, concrete next step — vague plans like "try harder" tend to fizzle, while specific ones get done.<Cite n={2} /> That is the bridge from thinking to action.</p>
                ) : (
                  <>
                    <p>"Yet" is powerful, but on its own it's just a nice thought. To actually make a difference, you need to follow it up with a real plan. That's the crucial third step: the <Highlight description="The specific, concrete thing you're going to do next to move from 'can't do it' to 'can do it'. It stops 'yet' from being empty words and turns it into actual progress." theme={theme}>Bridge to Action</Highlight>.</p>
                    <p>The full sentence isn't just "I can't do this yet." It's "I can't do this yet, *so I will*..." That extra bit stops "yet" from being an excuse and turns it into a starting point. The key is that the next step is specific and concrete: research on "implementation intentions" finds that naming exactly what you'll do (and when) makes you far more likely to actually do it than a vague "I'll try harder."<Cite n={2} /> Here's the full method:</p>
                  </>
                )}
                <InstructionList kind="yet" />
                <BridgeBuilder />
                <MicroCommitment theme={theme}>
                  <p>Think of your toughest subject. Your Block might be "I can't understand Topic X." Your Bridge could be "I will watch one YouTube video explaining it tonight."</p>
                </MicroCommitment>
            </ReadingSection>
          )}
           {activeSection === 4 && (
            <ReadingSection title="Your 'Yet' Audit." eyebrow="Step 5" icon={Wrench} theme={theme}>
              {essentials ? (
                <p>Now use it for real. Pick one thing you are struggling with. Name the block, add "yet", then choose your next move. Use the tool below to try it right now.</p>
              ) : (
                <>
                  <p>You've got the full method now. It's a way to catch yourself in those "I can't" moments and turn them into something useful instead of spiralling. The last step is to actually use it on something real.</p>
                  <p>Use the tool below to pick one thing you're genuinely struggling with right now. Run it through the three steps: name the block, add "yet", then figure out your next move. This isn't just practice -- it's you, right now, changing how you deal with the hard stuff.</p>
                </>
              )}
              <YetAudit />
            </ReadingSection>
          )}
        </>
      )}
    </ModuleLayout>
  );
};
export default ThePowerOfYetModule;
