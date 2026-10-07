import { BrandedPracticeSorter } from './learning/BrandedFeatures';
import { moduleFill,moduleText } from './learning/brandTokens';

/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
*/

import { motion } from 'framer-motion';
import {
Construction,
Cpu,
Microscope,
SlidersHorizontal,
Zap
} from 'lucide-react';
import React,{ useState } from 'react';
import { MYELIN_MANUAL_REFERENCE_LIST } from '../data/references/myelinManual';
import { COLORS } from '../design/tokens';
import { useEssentialsMode } from '../hooks/useEssentialsMode';
import { amberTheme } from '../moduleThemes';
import { type ModuleProgress } from '../types';
import { ModuleLayout } from './ModuleLayout';
import { Cite } from './ModuleReferences';
import { Highlight,MicroCommitment,ReadingSection } from './ModuleShared';

const theme = amberTheme;

// --- INTERACTIVE COMPONENTS ---
const MyelinWrapper = () => {
    const [wraps, setWraps] = useState(0);
    const maxWraps = 10;
    const speed = 10 + (wraps * 9); // Speed from 10 to 100
    const ringCount = Math.min(wraps, 8);
    const axonR = Math.max(10, 88 - (ringCount * 9) - 8);
    const milestone = wraps === 1 ? 'First layer of myelin forming.' : wraps === 4 ? 'Halfway there — signal noticeably faster.' : wraps >= 8 ? 'Fully myelinated. Skill becoming automatic.' : null;

    return (
        <div className="my-10 rounded-2xl p-6 md:p-8" style={{ backgroundColor: "var(--module-surface)", borderRadius: 18 }}>
            {/* Section chip + title */}
            <div className="text-center mb-8">
                <span className="inline-block px-3 py-1 rounded-full text-[11px] font-bold tracking-wider uppercase mb-3" style={{ backgroundColor: moduleFill(COLORS.accentTint), color: moduleText(COLORS.accentDarkText), border: '1px solid rgba(242,107,31,0.2)', letterSpacing: '0.06em' }}>Neuroscience Simulation</span>
                <h4 className="font-serif font-bold" style={{ fontSize: 26, color: "var(--module-ink)" }}>The Myelin Wrapper</h4>
                <p className="text-sm mt-1" style={{ color: "var(--module-muted)" }}>Each time you practice a skill, you add a layer of myelin, making the signal faster.</p>
            </div>

            {/* Nerve cross-section card */}
            <div className="bg-[var(--module-surface)] dark:bg-[var(--module-surface)]" style={{ border: "2px solid var(--module-line)", borderRadius: 16, padding: 28, maxWidth: 320, margin: '0 auto' }}>
                <p className="text-center mb-4" style={{ fontSize: 10, fontWeight: 700, letterSpacing: '0.12em', color: "var(--module-muted)", textTransform: 'uppercase' as const }}>Nerve Cross-Section</p>

                <svg viewBox="0 0 220 220" width="220" height="220" style={{ display: 'block', margin: '0 auto' }}>
                    {/* Outer boundary */}
                    <circle cx="110" cy="110" r="100" fill="var(--module-surface)" stroke="var(--module-muted)" strokeWidth="1.5"/>

                    {/* Myelin rings — outside in */}
                    {Array.from({ length: ringCount }).map((_, i) => {
                        const outerR = 88 - (i * 9);
                        const innerR = outerR - 7;
                        const opacity = 1 - (i * 0.08);
                        const isNewest = i === 0 && wraps > 0;
                        return (
                            <g key={`ring-${i}-${wraps}`}>
                                {isNewest ? (
                                    <motion.circle
                                        cx="110" cy="110" r={outerR}
                                        fill={i % 2 === 0 ? COLORS.accent : COLORS.accentDark}
                                        opacity={opacity}
                                        initial={{ scale: 0.7, opacity: 0 }}
                                        animate={{ scale: 1, opacity }}
                                        transition={{ duration: 0.35, ease: 'easeOut' }}
                                        style={{ transformOrigin: '110px 110px' }}
                                    />
                                ) : (
                                    <circle cx="110" cy="110" r={outerR} fill={i % 2 === 0 ? COLORS.accent : COLORS.accentDark} opacity={opacity} />
                                )}
                                <circle cx="110" cy="110" r={innerR} fill="var(--module-surface)" />
                            </g>
                        );
                    })}

                    {/* Central axon */}
                    <circle cx="110" cy="110" r={axonR} fill={COLORS.accentTint} stroke={COLORS.accent} strokeWidth="2" />

                    {/* Speed pulse dot */}
                    {wraps > 0 && (
                        <circle cx="110" cy={110 - axonR} r="5" fill={COLORS.accent} opacity="0.9"/>
                    )}

                    {/* Zero state label */}
                    {wraps === 0 && (
                        <text x="110" y="115" textAnchor="middle" fontSize="11" fill="var(--module-muted)" fontFamily="DM Sans, sans-serif">no myelin yet</text>
                    )}
                </svg>

                {/* Layer count */}
                <p className="text-center mt-3" style={{ fontSize: 12, color: "var(--module-muted)" }}>{ringCount} / 8 myelin layers</p>

                {/* Signal speed stat */}
                <div className="text-center mt-4 pt-4" style={{ borderTop: "1px solid var(--module-line)" }}>
                    <p style={{ lineHeight: 1 }}>
                        <span className="font-serif font-bold" style={{ fontSize: 40, color: 'var(--module-accent-text)' }}>{speed}</span>
                        <span className="font-sans" style={{ fontSize: 16, color: "var(--module-muted)", marginLeft: 4 }}>m/s</span>
                    </p>
                    <p className="mt-1" style={{ fontSize: 10, fontWeight: 700, letterSpacing: '0.1em', color: "var(--module-muted)", textTransform: 'uppercase' as const }}>Signal Speed</p>
                </div>
            </div>

            {/* Milestone callout */}
            {milestone && (
                <motion.div
                    key={milestone}
                    initial={{ opacity: 0, y: 6 }}
                    animate={{ opacity: 1, y: 0 }}
                    className="mt-4 max-w-xs mx-auto"
                    style={{ borderLeft: `3px solid ${COLORS.accent}`, backgroundColor: moduleFill(COLORS.accentTint), borderRadius: '0 10px 10px 0', padding: '12px 16px' }}
                >
                    <p className="text-sm italic" style={{ color: moduleText(COLORS.accentDarkText) }}>{milestone}</p>
                </motion.div>
            )}

            {/* Buttons */}
            <div className="flex items-center justify-center gap-5 mt-6">
                <motion.button
                    onClick={() => setWraps(w => Math.min(w + 1, maxWraps))}
                    whileTap={{ scale: 0.97 }}
                    className="text-[var(--module-ink)] font-semibold"
                    style={{ backgroundColor: moduleFill(COLORS.accent), borderRadius: 100, padding: '14px 32px', fontSize: 15, border: 'none' }}
                    onMouseEnter={(e: React.MouseEvent<HTMLButtonElement>) => { e.currentTarget.style.backgroundColor = COLORS.accentDark; }}
                    onMouseLeave={(e: React.MouseEvent<HTMLButtonElement>) => { e.currentTarget.style.backgroundColor = COLORS.accent; }} data-wide-button="true"
                >
                    Practice Skill
                </motion.button>
                <button
                    onClick={() => setWraps(0)}
                    className="font-medium"
                    style={{ fontSize: 13, color: "var(--module-muted)", background: 'none', border: 'none' }}
                    onMouseEnter={(e: React.MouseEvent<HTMLButtonElement>) => { e.currentTarget.style.color = "var(--module-ink)"; }}
                    onMouseLeave={(e: React.MouseEvent<HTMLButtonElement>) => { e.currentTarget.style.color = "var(--module-muted)"; }} data-wide-button="true"
                >
                    Reset
                </button>
            </div>
        </div>
    )
}

const DeepPracticeSorter = BrandedPracticeSorter;


// --- MODULE COMPONENT ---
const TheMyelinManualModule: React.FC<{ onBack: () => void; progress: ModuleProgress; onProgressUpdate: (progress: ModuleProgress) => void }> = ({ onBack, progress, onProgressUpdate }) => {
  const essentials = useEssentialsMode();
  const sections = [
    { id: 'silent-revolution', title: 'The Silent Revolution', eyebrow: '01 // The Other Brain', icon: Cpu },
    { id: 'signal-of-struggle', title: 'The Signal of Struggle', eyebrow: '02 // The Chemical Trigger', icon: Zap },
    { id: 'deep-practice', title: 'Deep Practice', eyebrow: '03 // The Behavioural Trigger', icon: SlidersHorizontal },
    { id: 'myelin-metaphors', title: 'The Mastery Metaphors', eyebrow: '04 // The Mental Models', icon: Microscope },
    { id: 'rules-of-myelination', title: 'The Rules of Myelination', eyebrow: '05 // The Action Plan', icon: Construction },
  ];

  return (
    <ModuleLayout
      moduleNumber="02"
      moduleTitle="The Myelin Manual"
      moduleSubtitle="How Your Brain Gets Faster"
      moduleDescription={`That feeling of struggling with a hard question? It's not a sign you're bad at it — it's literally how your brain builds faster connections. This module shows you why the hard stuff is the stuff that works.`}
      theme={theme}
      sections={sections}
      onBack={onBack}
      progress={progress}
      onProgressUpdate={onProgressUpdate}
      finishButtonText="Build Your Wiring"
      references={MYELIN_MANUAL_REFERENCE_LIST}
    >
      {(activeSection) => (
        <>
          {activeSection === 0 && (
            <ReadingSection title="The Silent Revolution." eyebrow="Step 1" icon={Cpu} theme={theme}>
              {essentials ? (
                <>
                  <p>Getting good at something means upgrading your brain's wiring. Cells called oligodendrocytes wrap your brain's circuits in insulation called <strong>myelin</strong>. This makes signals travel much faster.<Cite n={1} /></p>
                  <p>Myelin turns slow, clunky skills into fast, automatic ones. It is why practice eventually makes things feel effortless.</p>
                </>
              ) : (
                <>
                  <p>In the last module, we learned that your brain physically changes when you learn. Now, we're looking at how you actually get good at something — how you go from slow and clunky to fast and automatic. It's not just about making connections between brain cells. It's about upgrading the wiring itself.</p>
                  <p>Meet the unsung hero of your brain: the <Highlight description="These are basically the electricians of your brain. Their whole job is to wrap insulation around your brain's wiring so signals travel faster." theme={theme}>Oligodendrocyte</Highlight>. These cells work behind the scenes, wrapping your brain's circuits in a fatty insulation called <Highlight description="A fatty coating that wraps around your brain's wires, like the plastic insulation on a phone charger cable. It stops signals from leaking and makes everything way faster." theme={theme}>Myelin</Highlight>.<Cite n={1} /> This wrapping turns your brain's bumpy dirt roads into super-fast motorways. It's not just about knowing things — it's about being fast, precise, and doing things on autopilot.</p>
                </>
              )}
            </ReadingSection>
          )}
           {activeSection === 1 && (
            <ReadingSection title="The Signal of Struggle." eyebrow="Step 2" icon={Zap} theme={theme}>
              {essentials ? (
                <>
                  <p>Your brain insulates the wires it uses most. When brain cells fire a lot during focused practice, that activity helps trigger the cells that wrap them in myelin.<Cite n={1} /><Cite n={2} /></p>
                  <p>That feeling of effortful struggle is not failure — it's a sign you're practising at the right level. Coasting through easy material drives far less of this change.</p>
                </>
              ) : (
                <>
                  <p>So how does your brain know which wires to insulate? It largely comes down to activity. When you're really concentrating hard — like grinding through a tough maths question — the brain cells in that circuit fire intensely, and that activity helps recruit the cells that build myelin around them.<Cite n={1} /><Cite n={2} /> Researchers call this "activity-dependent" (or adaptive) myelination.</p>
                  <p>And here's the key part: that feeling of <Highlight description="That frustrated, stuck feeling when you're working on something hard? It's a sign you're practising at the edge of your ability — exactly the effortful practice that drives skill change." theme={theme}>struggle</Highlight> is not a sign you're failing. It's a sign you're working at the edge of your ability — the kind of focused, effortful practice that drives these changes. Coasting through easy material does much less.</p>
                </>
              )}
            </ReadingSection>
          )}
          {activeSection === 2 && (
            <ReadingSection title="Deep Practice." eyebrow="Step 3" icon={SlidersHorizontal} theme={theme}>
              {essentials ? (
                <>
                  <p><strong>Deep practice</strong> is the effortful, focused kind that drives skill.<Cite n={3} /> It means doing past papers without notes, recalling from scratch, and pushing just outside your comfort zone.<Cite n={4} /> Easy practice barely registers with your brain.</p>
                  <p>The discomfort you feel during hard practice is the signal. That is your brain building faster wiring.</p>
                </>
              ) : (
                <>
                  <p>The type of practice that drives this change is what's often called <Highlight description="A way of practising where you really focus, push yourself to the edge of what you can do, make mistakes, fix them, and repeat. It's the effortful kind of practice that actually builds skill." theme={theme}>Deep Practice</Highlight> — a close cousin of "deliberate practice".<Cite n={3} /> It's the opposite of passively re-reading your notes. Easy practice feels productive, but it barely registers with your brain — it doesn't trigger the upgrade. It just gives you a false sense of confidence.</p>
                  <p>Deep practice is hard, uncomfortable, and full of mistakes. It means doing past papers without your notes, forcing yourself to recall things from scratch, and pushing yourself just outside your comfort zone.<Cite n={4} /> That discomfort is a sign you're working at the right level — the effortful practice that drives your brain to strengthen and insulate the circuits that matter.</p>
                </>
              )}
              <DeepPracticeSorter />
            </ReadingSection>
          )}
          {activeSection === 3 && (
            <ReadingSection title="The Mastery Metaphors." eyebrow="Step 4" icon={Microscope} theme={theme}>
              {essentials ? (
                <p>Think of it like upgrading from dial-up to broadband. Before practice, your brain handles one idea at a time and lags. After deep practice builds myelin, information flows at speed. Each practice session paves the road a little more.</p>
              ) : (
                <>
                  <p>To really picture what's going on, here are a couple of ways to think about it.</p>
                  <p>Imagine upgrading your home internet from dial-up to fibre <strong>broadband</strong>. Before the upgrade, your brain can only handle one simple idea at a time — it buffers and lags. After deep practice wraps your circuits in myelin, you can handle multiple ideas at once without slowing down. Or think of it as paving a <strong>dirt road into a motorway</strong>. The first time you learn something, it's slow and bumpy. With deep practice, you pave that road, and information starts flowing at speed, almost on autopilot.<Cite n={5} /></p>
                </>
              )}
              <MyelinWrapper/>
            </ReadingSection>
          )}
           {activeSection === 4 && (
            <ReadingSection title="The Rules of Myelination." eyebrow="Step 5" icon={Construction} theme={theme}>
              {essentials ? (
                <>
                  <p><strong>Struggle is not optional.</strong> Easy practice doesn't drive the change. You need the sweet spot where you make mistakes and fix them.<Cite n={4} /></p>
                  <p><strong>It is durable but slow.</strong> Skills built through proper practice last far longer than crammed knowledge — but, like any brain change, they need topping up; stop practising entirely and they fade. Every session adds another layer.</p>
                </>
              ) : (
                <>
                  <p>There are a few simple rules here that you can't skip. First, <strong>struggle is not optional</strong>. Easy practice doesn't drive the change. You need to be in the "sweet spot" where you're making mistakes and fixing them.<Cite n={4} /> That loop of getting it wrong and then getting it right is what builds skill.</p>
                  <p>Second, <strong>it's durable but slow</strong>. A skill built through proper practice lasts far longer than anything you cram the night before. You can't build a motorway overnight — every session of deep practice adds another thin layer. But, like the juggling study in the last module showed, brain changes aren't frozen forever: stop practising completely and they gradually fade, so keep topping skills up.</p>
                </>
              )}
                <MicroCommitment theme={theme}>
                    <p>Identify your "sweet spot" for one subject. What is a task that is not too easy (you get it all right) and not too hard (you get it all wrong)? That's your target zone for the next study session.</p>
                </MicroCommitment>
            </ReadingSection>
          )}
        </>
      )}
    </ModuleLayout>
  );
};
export default TheMyelinManualModule;
