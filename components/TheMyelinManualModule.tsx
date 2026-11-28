import { BrandedPracticeSorter } from './learning/BrandedFeatures';

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
import { AnswerLine,ExerciseLabel,ExerciseSheet } from './learning/Exercise';
import { Button,TextButton } from './ui/Button';

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
        <ExerciseSheet label="Neuroscience Simulation" title="The Myelin Wrapper" sub="Each time you practice a skill, you add a layer of myelin, making the signal faster." name="MyelinWrapper">
            {/* The nerve cross-section, on the sheet under its label (no box of its own) */}
            <div className="ex-figure">
                <ExerciseLabel>Nerve Cross-Section</ExerciseLabel>

                <svg viewBox="0 0 220 220" width="220" height="220" className="ex-figure-art">
                    {/* Outer boundary */}
                    <circle cx="110" cy="110" r="100" fill="var(--surface-paper)" stroke="var(--ink-muted)" strokeWidth="1.5"/>

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
                                <circle cx="110" cy="110" r={innerR} fill="var(--surface-paper)" />
                            </g>
                        );
                    })}

                    {/* Central axon */}
                    <circle cx="110" cy="110" r={axonR} fill="var(--surface-paper)" stroke={COLORS.accent} strokeWidth="2" />

                    {/* Speed pulse dot */}
                    {wraps > 0 && (
                        <circle cx="110" cy={110 - axonR} r="5" fill={COLORS.accent} opacity="0.9"/>
                    )}

                    {/* Zero state label */}
                    {wraps === 0 && (
                        <text x="110" y="115" textAnchor="middle" fontSize="11" fill="var(--ink-muted)" style={{ fontFamily: 'var(--font-ui)' }}>no myelin yet</text>
                    )}
                </svg>

                {/* Layer count */}
                <p className="ex-figure-count">{ringCount} / 8 myelin layers</p>

                {/* Signal speed: the number in ink and its label, not a box */}
                <div className="flex flex-col items-center gap-1 text-center">
                    <p className="m-0" style={{ lineHeight: 1 }}>
                        <span className="text-ink-primary" style={{ fontSize: 40, letterSpacing: '-0.04em' }}>{speed}</span>
                        <span className="text-ink-muted" style={{ fontSize: 16, marginLeft: 4 }}>m/s</span>
                    </p>
                    <ExerciseLabel>Signal Speed</ExerciseLabel>
                </div>
            </div>

            {/* Milestone: a line in ink (the tick once fully myelinated) */}
            {milestone && (
                <motion.div
                    key={milestone}
                    initial={{ opacity: 0, y: 6 }}
                    animate={{ opacity: 1, y: 0 }}
                >
                    <AnswerLine tone={wraps >= 8 ? 'ok' : 'note'}>{milestone}</AnswerLine>
                </motion.div>
            )}

            {/* Buttons */}
            <div className="ex-actions">
                <Button onClick={() => setWraps(w => Math.min(w + 1, maxWraps))}>
                    Practice Skill
                </Button>
                <TextButton tone="quiet" onClick={() => setWraps(0)}>
                    Reset
                </TextButton>
            </div>
        </ExerciseSheet>
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
