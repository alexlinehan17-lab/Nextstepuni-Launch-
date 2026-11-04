import { BrandedAgencyBalance } from './learning/WideFeatures';
/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
*/

import { motion } from 'framer-motion';
import {
Award,
BookOpen,
Feather,
FileText,
Scale
} from 'lucide-react';
import React,{ useState } from 'react';
import { STRATEGIC_ADVANTAGE_REFERENCE_LIST } from '../data/references/strategicAdvantage';
import { useEssentialsMode } from '../hooks/useEssentialsMode';
import { useNorthStar } from '../hooks/useNorthStar';
import { indigoTheme } from '../moduleThemes';
import { COMPACT_CALLOUT_PLACEMENTS } from '../northStarData';
import { type ModuleProgress } from '../types';
import { ModuleLayout } from './ModuleLayout';
import { Cite } from './ModuleReferences';
import { Highlight,MicroCommitment,PersonalStory,ReadingSection } from './ModuleShared';
import NorthStarCallout from './NorthStarCallout';

const theme = indigoTheme;

// --- INTERACTIVE COMPONENTS ---
const NarrativeSwitcher = () => {
    const [script, setScript] = useState<'idle' | 'contamination' | 'redemption'>('idle');
    const [animKey, setAnimKey] = useState(0);

    const contamination = [
      { text: '"I failed the mock."', tone: 'neutral' as const },
      { text: '"I\'m just not smart enough."', tone: 'bad' as const },
      { text: '"Everyone else got it. What\'s wrong with me?"', tone: 'bad' as const },
      { text: '"There\'s no point trying harder."', tone: 'bad' as const },
      { text: '"I give up."', tone: 'bad' as const },
    ];

    const redemption = [
      { text: '"I failed the mock."', tone: 'neutral' as const },
      { text: '"That stings. But now I know exactly where the gaps are."', tone: 'good' as const },
      { text: '"I\'m going to target those weak areas this week."', tone: 'good' as const },
      { text: '"I\'ll do 3 past papers focused on the topics I got wrong."', tone: 'good' as const },
      { text: '"This failure just became my study plan."', tone: 'good' as const },
    ];

    const handleSelect = (type: 'contamination' | 'redemption') => {
      setScript(type);
      setAnimKey(k => k + 1);
    };

    const toneStyles = {
      neutral: "bg-[var(--module-surface)] dark:bg-[var(--module-surface)] text-[var(--module-ink)] dark:text-[var(--module-muted)] border-[var(--module-line)] dark:border-[var(--module-line)]",
      bad: "bg-[var(--module-danger-soft)] dark:bg-[var(--module-danger-soft)] text-[var(--module-danger-text)] dark:text-[var(--module-danger-text)] border-[var(--module-line)] dark:border-[var(--module-line)]",
      good: "bg-[var(--module-success-soft)] dark:bg-[var(--module-success-soft)] text-[var(--module-success-text)] dark:text-[var(--module-success-text)] border-[var(--module-line)] dark:border-[var(--module-line)]",
    };

    const renderSequence = (steps: typeof contamination | typeof redemption, active: boolean) => (
      <div className="space-y-3">
        {steps.map((step, i) => (
          <motion.div
            key={`${animKey}-${i}`}
            initial={active ? { opacity: 0, y: 10 } : { opacity: 0.3 }}
            animate={active ? { opacity: 1, y: 0 } : { opacity: 0.3 }}
            transition={active ? { delay: i * 0.4, duration: 0.4 } : { duration: 0.3 }}
            className={`p-3 rounded-lg border text-sm font-medium ${active ? toneStyles[step.tone] : "bg-[var(--module-surface)] dark:bg-[var(--module-surface)] text-[var(--module-muted)] dark:text-[var(--module-ink)] border-[var(--module-line)] dark:border-[var(--module-line)]"}`}
          >
            {i > 0 && active && (
              <motion.span
                initial={{ opacity: 0 }}
                animate={{ opacity: 1 }}
                transition={{ delay: i * 0.4 + 0.1 }}
                className="mr-1.5"
              >
                →
              </motion.span>
            )}
            {step.text}
          </motion.div>
        ))}
      </div>
    );

    return <div className="wr-skin" data-wide="NarrativeSwitcher"><div className="my-10 rounded-2xl p-6 md:p-8" style={{ backgroundColor: "var(--module-surface)", borderRadius: 18 }}>
            <h4 className="font-serif text-2xl font-semibold text-[var(--module-ink)] dark:text-[var(--module-ink)] text-center">The Narrative Switcher</h4>
            <p className="text-center text-sm text-[var(--module-muted)] dark:text-[var(--module-muted)] mb-8">Pivotal Moment: You fail an important mock exam. Which story do you tell?</p>
            <div className="flex justify-center gap-4 mb-8">
                <button onClick={() => handleSelect('contamination')} className={`px-5 py-2.5 text-xs font-bold rounded-lg transition-all ${script === 'contamination' ? "bg-[var(--module-danger)] text-[var(--module-ink)] shadow-none shadow-none" : "bg-[var(--module-danger-soft)] text-[var(--module-danger-text)] hover:bg-[var(--module-danger-soft)]"}`} data-wide-button="true" data-selected={!!(script === 'contamination')} data-tone="coral" aria-pressed={!!(script === 'contamination')}>Contamination Script</button>
                <button onClick={() => handleSelect('redemption')} className={`px-5 py-2.5 text-xs font-bold rounded-lg transition-all ${script === 'redemption' ? "bg-[var(--module-success)] text-[var(--module-ink)] shadow-none shadow-none" : "bg-[var(--module-success-soft)] text-[var(--module-success-text)] hover:bg-[var(--module-success-soft)]"}`} data-wide-button="true" data-selected={!!(script === 'redemption')} data-tone="mint" aria-pressed={!!(script === 'redemption')}>Redemption Script</button>
            </div>
            {script !== 'idle' && (
              <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                <div>
                  <p className={`text-xs font-bold uppercase tracking-wider mb-3 ${script === 'contamination' ? "text-[var(--module-danger-text)]" : "text-[var(--module-muted)] dark:text-[var(--module-ink)]"}`}>Contamination Script</p>
                  {renderSequence(contamination, script === 'contamination')}
                </div>
                <div>
                  <p className={`text-xs font-bold uppercase tracking-wider mb-3 ${script === 'redemption' ? "text-[var(--module-success-text)]" : "text-[var(--module-muted)] dark:text-[var(--module-ink)]"}`}>Redemption Script</p>
                  {renderSequence(redemption, script === 'redemption')}
                </div>
              </div>
            )}
        </div></div>;
};


const AgencyCommunionBalancer = BrandedAgencyBalance;

const DesirableDifficultyComparison = () => {
    const [revealed, setRevealed] = useState(false);

    const W = 440, H = 260;
    const padL = 8, padR = 8, padT = 28, padB = 44;
    const chartW = W - padL - padR, chartH = H - padT - padB;
    const toX = (f: number) => padL + f * chartW;
    const toY = (f: number) => padT + (1 - f) * chartH;

    const xLabels = ['Study', 'Day 1', 'Day 3', 'Day 7', 'Day 14', 'Day 30'];

    // Easy Path data
    const easyComfort  = [0.90, 0.88, 0.85, 0.82, 0.78, 0.75];
    const easyDurability = [0.80, 0.55, 0.35, 0.25, 0.18, 0.12];

    // Hard Path data
    const hardComfort  = [0.25, 0.32, 0.40, 0.48, 0.55, 0.62];
    const hardDurability = [0.45, 0.52, 0.60, 0.68, 0.75, 0.82];

    const buildArea = (data: number[]) => {
        const pts = data.map((v, i) => ({ x: toX(i / (data.length - 1)), y: toY(v) }));
        let d = `M ${pts[0].x} ${toY(0)} L ${pts[0].x} ${pts[0].y}`;
        for (let i = 1; i < pts.length; i++) {
            const cx1 = pts[i - 1].x + (pts[i].x - pts[i - 1].x) * 0.4;
            const cx2 = pts[i - 1].x + (pts[i].x - pts[i - 1].x) * 0.6;
            d += ` C ${cx1} ${pts[i - 1].y}, ${cx2} ${pts[i].y}, ${pts[i].x} ${pts[i].y}`;
        }
        d += ` L ${pts[pts.length - 1].x} ${toY(0)} Z`;
        return d;
    };

    const buildLine = (data: number[]) => {
        const pts = data.map((v, i) => ({ x: toX(i / (data.length - 1)), y: toY(v) }));
        let d = `M ${pts[0].x} ${pts[0].y}`;
        for (let i = 1; i < pts.length; i++) {
            const cx1 = pts[i - 1].x + (pts[i].x - pts[i - 1].x) * 0.4;
            const cx2 = pts[i - 1].x + (pts[i].x - pts[i - 1].x) * 0.6;
            d += ` C ${cx1} ${pts[i - 1].y}, ${cx2} ${pts[i].y}, ${pts[i].x} ${pts[i].y}`;
        }
        return d;
    };

    const easyPhases = [
        { label: 'Feels productive', x1: 0, x2: 0.33, color: "var(--module-ink)" },
        { label: 'Confidence high', x1: 0.33, x2: 0.66, color: "var(--module-danger-text)" },
        { label: 'Exam shock', x1: 0.66, x2: 1, color: "var(--module-danger-text)" },
    ];
    const hardPhases = [
        { label: 'Feels frustrating', x1: 0, x2: 0.33, color: "var(--module-success-text)" },
        { label: 'Effort pays off', x1: 0.33, x2: 0.66, color: "var(--module-success-text)" },
        { label: 'Deeply encoded', x1: 0.66, x2: 1, color: "var(--module-success-text)" },
    ];

    const Chart = ({ comfort, durability, phases, areaColor, areaId, areaData, label }: {
        comfort: number[]; durability: number[]; phases: { label: string; x1: number; x2: number; color: string }[];
        areaColor: string; areaId: string; areaData: number[]; label: string;
    }) => (
        <svg viewBox={`0 0 ${W} ${H}`} className="w-full">
            <defs>
                <linearGradient id={areaId} x1="0" y1="0" x2="0" y2="1">
                    <stop offset="0%" stopColor={areaColor} stopOpacity="0.5" />
                    <stop offset="100%" stopColor={areaColor} stopOpacity="0.05" />
                </linearGradient>
            </defs>
            {/* Grid lines */}
            {[0.25, 0.5, 0.75, 1.0].map(v => (
                <line key={v} x1={padL} x2={W - padR} y1={toY(v)} y2={toY(v)} stroke="var(--module-muted)" strokeOpacity="0.15" strokeDasharray="3 3" />
            ))}
            {/* Baseline */}
            <line x1={padL} x2={W - padR} y1={toY(0)} y2={toY(0)} stroke="var(--module-muted)" strokeOpacity="0.3" />
            {/* Area fill */}
            <motion.path
                d={buildArea(areaData)}
                fill={`url(#${areaId})`}
                initial={{ opacity: 0 }}
                animate={{ opacity: 1 }}
                transition={{ duration: 0.8 }}
            />
            {/* Comfort line (solid) */}
            <motion.path
                d={buildLine(comfort)}
                fill="none" stroke={areaColor} strokeWidth="2.5" strokeLinecap="round"
                initial={{ pathLength: 0 }} animate={{ pathLength: 1 }}
                transition={{ duration: 1.2, ease: 'easeOut' }}
            />
            {/* Durability line (dashed) */}
            <motion.path
                d={buildLine(durability)}
                fill="none" stroke="var(--module-ink)" strokeWidth="1.5" strokeDasharray="5 3" strokeLinecap="round"
                initial={{ pathLength: 0 }} animate={{ pathLength: 1 }}
                transition={{ duration: 1.2, ease: 'easeOut', delay: 0.3 }}
            />
            {/* Comfort dots */}
            {comfort.map((v, i) => (
                <motion.circle key={i} cx={toX(i / (comfort.length - 1))} cy={toY(v)} r="3.5" fill={areaColor}
                    initial={{ scale: 0 }} animate={{ scale: 1 }} transition={{ delay: 0.2 * i + 0.3 }}
                />
            ))}
            {/* Y-axis labels */}
            <text x={padL + 2} y={toY(1.0) - 4} fontSize="9" fill="var(--module-surface)" fontWeight="600">High</text>
            <text x={padL + 2} y={toY(0) - 4} fontSize="9" fill="var(--module-surface)" fontWeight="600">Low</text>
            {/* X-axis labels */}
            {xLabels.map((m, i) => (
                <text key={m} x={toX(i / (xLabels.length - 1))} y={toY(0) + 14} fontSize="9" fill="var(--module-surface)" textAnchor="middle" fontWeight="600">{m}</text>
            ))}
            {/* Phase labels */}
            {phases.map((p, i) => (
                <text key={i} x={toX((p.x1 + p.x2) / 2)} y={toY(0) + 28} fontSize="8" fill={p.color} textAnchor="middle" fontWeight="700">{p.label}</text>
            ))}
            {/* Chart label */}
            <text x={W / 2} y={14} fontSize="11" fill="var(--module-muted)" textAnchor="middle" fontWeight="700">{label}</text>
            {/* Legend */}
            <line x1={W - padR - 100} x2={W - padR - 84} y1={14} y2={14} stroke={areaColor} strokeWidth="2" />
            <text x={W - padR - 80} y={17} fontSize="8" fill="var(--module-surface)">Comfort</text>
            <line x1={W - padR - 50} x2={W - padR - 34} y1={14} y2={14} stroke="var(--module-ink)" strokeWidth="1.5" strokeDasharray="4 2" />
            <text x={W - padR - 30} y={17} fontSize="8" fill="var(--module-surface)">Durability</text>
        </svg>
    );

    return (
        <div className="my-10 rounded-2xl p-6 md:p-8" style={{ backgroundColor: "var(--module-surface)", borderRadius: 18 }}>
            <h4 className="font-serif text-2xl font-semibold text-[var(--module-ink)] dark:text-[var(--module-ink)] text-center">The Difficulty Dividend</h4>
            <p className="text-center text-sm text-[var(--module-muted)] dark:text-[var(--module-muted)] mb-6">The study method that feels worst produces the best results.</p>

            {!revealed ? (
                <div className="text-center">
                    <p className="text-sm text-[var(--module-muted)] dark:text-[var(--module-muted)] mb-4">What happens to comfort and actual retention over 30 days for two very different study strategies?</p>
                    <button onClick={() => setRevealed(true)} className="px-5 py-2.5 text-sm font-bold rounded-lg bg-[var(--module-solid)] text-[var(--module-ink)] hover:bg-[var(--module-solid)] transition-colors" data-wide-button="true">
                        Reveal the Dividend
                    </button>
                </div>
            ) : (
                <motion.div initial={{ opacity: 0, y: 12 }} animate={{ opacity: 1, y: 0 }} transition={{ duration: 0.4 }}>
                    <div className="grid md:grid-cols-2 gap-4 mb-5">
                        <div className="rounded-lg border border-[var(--module-line)] dark:border-[var(--module-line)] bg-[var(--module-danger-soft)] dark:bg-[var(--module-danger-soft)] p-3">
                            <Chart comfort={easyComfort} durability={easyDurability} phases={easyPhases}
                                areaColor="var(--module-danger-text)" areaId="easy-grad" areaData={easyComfort} label="The Easy Path" />
                        </div>
                        <div className="rounded-lg border border-[var(--module-line)] dark:border-[var(--module-line)] bg-[var(--module-success-soft)] dark:bg-[var(--module-success-soft)] p-3">
                            <Chart comfort={hardComfort} durability={hardDurability} phases={hardPhases}
                                areaColor="var(--module-success-text)" areaId="hard-grad" areaData={hardDurability} label="The Hard Path" />
                        </div>
                    </div>
                    <div className="grid md:grid-cols-2 gap-4 text-sm">
                        <div className="flex items-start gap-2.5 p-3 rounded-lg bg-[var(--module-danger-soft)] dark:bg-[var(--module-danger-soft)] border border-[var(--module-line)] dark:border-[var(--module-line)]">
                            <span className="text-[var(--module-danger-text)] text-lg mt-0.5"></span>
                            <p className="text-[var(--module-ink)] dark:text-[var(--module-muted)]"><strong className="text-[var(--module-danger-text)] dark:text-[var(--module-danger-text)]">Re-reading and highlighting</strong> feel smooth and satisfying. But ease of processing during study doesn't predict long-term retention. This is the fluency illusion.</p>
                        </div>
                        <div className="flex items-start gap-2.5 p-3 rounded-lg bg-[var(--module-success-soft)] dark:bg-[var(--module-success-soft)] border border-[var(--module-line)] dark:border-[var(--module-line)]">
                            <span className="text-[var(--module-success-text)] text-lg mt-0.5"></span>
                            <p className="text-[var(--module-ink)] dark:text-[var(--module-muted)]"><strong className="text-[var(--module-success-text)] dark:text-[var(--module-success-text)]">Testing yourself, spacing, and interleaving</strong> feel slower and harder. But that desirable difficulty forces deeper encoding. The struggle IS the learning signal.</p>
                        </div>
                    </div>
                </motion.div>
            )}
        </div>
    );
};

// --- MODULE COMPONENT ---
const StrategicAdvantageModule: React.FC<{ onBack: () => void; progress: ModuleProgress; onProgressUpdate: (progress: ModuleProgress) => void }> = ({ onBack, progress, onProgressUpdate }) => {
  const essentials = useEssentialsMode();
  const { northStar } = useNorthStar();
  const sections = [
    { id: 'narrative-identity', title: 'The Story of You', eyebrow: '01 // Your Internal Script', icon: Feather },
    { id: 'agency-communion', title: 'The Two Pillars', eyebrow: '02 // Agency & Communion', icon: Scale },
    { id: 'pivotal-moments', title: 'The Power of Failure', eyebrow: '03 // Pivotal Moments', icon: BookOpen },
    { id: 'desirable-difficulties', title: 'The Advantage of Disadvantage', eyebrow: '04 // Desirable Difficulties', icon: Award },
    { id: 'redemption-script', title: 'Your Redemption Script', eyebrow: '05 // The Blueprint', icon: FileText },
  ];

  return (
    <ModuleLayout
      moduleNumber="08"
      moduleTitle="Your Strategic Advantage"
      moduleSubtitle="The Narrative Identity Playbook"
      moduleDescription="Learn how to take the tough parts of your story and turn them into your biggest strength — in school, in exams, and in life."
      theme={theme}
      sections={sections}
      references={STRATEGIC_ADVANTAGE_REFERENCE_LIST}
      onBack={onBack}
      progress={progress}
      onProgressUpdate={onProgressUpdate}
      finishButtonText="Own Your Story"
    >
      {(activeSection) => (
        <>
          {activeSection === 0 && (
            <ReadingSection title="The Story of You." eyebrow="Step 1" icon={Feather} theme={theme}>
              {essentials ? (<><p>You tell yourself a story about your life. That story shapes everything. A <Highlight description="When something good happens but then something bad follows, and the bad part takes over the whole story. It is the kind of thinking where one setback makes you feel like nothing will ever work out." theme={theme}>Contamination Script</Highlight> says setbacks define you. A <Highlight description="When something bad happens but you find a way to turn it into something good — a lesson, a motivation, a turning point. It is choosing to let the rough patch be the start of a comeback, not the end of the road." theme={theme}>Redemption Script</Highlight> turns hard times into fuel.<Cite n={1} /> You get to choose which one you run.</p></>) : (<><p>You are a storyteller. The most important story you will ever tell is the one you tell yourself about your own life. This is your <Highlight description="The ongoing story you tell yourself about who you are and where your life is going. We all have one — it shapes how you see your past, your present, and what you think is possible for your future." theme={theme}>Narrative Identity</Highlight>.<Cite n={1} /> It's how you make sense of your past, present, and future.</p>
              <p>Society often hands students from tough backgrounds a ready-made story: a tale of deficit and struggle. This is a <Highlight description="When something good happens but then something bad follows, and the bad part takes over the whole story. It is the kind of thinking where one setback makes you feel like nothing will ever work out." theme={theme}>Contamination Script</Highlight>. Resilience is the act of radical authorship: rejecting that story and writing your own, a <Highlight description="When something bad happens but you find a way to turn it into something good — a lesson, a motivation, a turning point. It is choosing to let the rough patch be the start of a comeback, not the end of the road." theme={theme}>Redemption Script</Highlight> where adversity becomes the source of your strength.</p>
              <PersonalStory name="Alex" role="Founder, NextStepUni">
                <p>I had a contamination script running for years. Lad from Togher, wrong crowds, failed the Junior Cert — it would have been easy to let that be the whole story. But in 4th year I rewrote it. I spent the year reading academic papers, built my own learning system, and went from rock bottom to nearly 600 points and a UCC Scholarship. The story didn't change because the facts changed. The facts were the same. I just chose to write a different next chapter.</p>
              </PersonalStory></>)}
              <NarrativeSwitcher />
            </ReadingSection>
          )}
           {activeSection === 1 && (
            <ReadingSection title="The Two Pillars." eyebrow="Step 2" icon={Scale} theme={theme}>
                {essentials ? (<><p>Great stories blend two themes. <Highlight description="The part of your story that is about you taking charge — your independence, your effort, and your ability to shape your own future through your own actions." theme={theme}>Agency</Highlight> is your own effort. <Highlight description="The part of your story that is about the people around you — your family, friends, and community, and how those relationships have shaped who you are." theme={theme}>Communion</Highlight> is the people who support you. Too much of one breaks the story. Balance them: "I worked hard to honour my family."<Cite n={1} /></p></>) : (<><p>Every great story is built on two core themes. The first is <Highlight description="The part of your story that is about you taking charge — your independence, your effort, and your ability to shape your own future through your own actions." theme={theme}>Agency</Highlight>—the story of the self-reliant hero who overcomes obstacles through their own power. The second is <Highlight description="The part of your story that is about the people around you — your family, friends, and community, and how those relationships have shaped who you are." theme={theme}>Communion</Highlight>—the story of connection, of being supported by family, friends, and community.</p>
                <p>A story of pure Agency leads to the "Isolated Hero" who burns out. A story of pure Communion leads to passivity. The most resilient narrative identities skillfully weave both: "I worked hard (Agency) to honour the sacrifices of my family (Communion)."<Cite n={1} /> Finding this balance is key to a sustainable story of success.</p></>)}
                <AgencyCommunionBalancer />
            </ReadingSection>
          )}
          {activeSection === 2 && (
            <ReadingSection title="The Power of Failure." eyebrow="Step 3" icon={BookOpen} theme={theme}>
              {northStar && (() => { const p = COMPACT_CALLOUT_PLACEMENTS.find(p => p.moduleId === 'strategic-advantage-protocol'); return p ? <NorthStarCallout northStar={northStar} variant="compact" message={p.message} /> : null; })()}
              {essentials ? (<><p>Your life is a collection of key scenes. Your failures are the most useful ones. Learn to <Highlight description="Looking at the same event from a different angle so it means something different to you. Instead of 'I failed,' you think 'I found out exactly what I need to work on.' Same facts, different story." theme={theme}>reframe</Highlight> them. "I failed" becomes "I found exactly what to work on." Same facts. Different story.</p></>) : (<><p>Your life story is not a continuous film; it's a collection of key scenes. These are your <Highlight description="The key moments in your life that stick with you — the highs, the lows, and the turning points. These are the scenes that define the story you tell about yourself." theme={theme}>Pivotal Moments</Highlight>.<Cite n={1} /> For resilient individuals, the most important pivotal moments are often failures. They are the moments where suffering is transformed into insight.</p>
              <p>The key is to learn the art of <Highlight description="Looking at the same event from a different angle so it means something different to you. Instead of 'I failed,' you think 'I found out exactly what I need to work on.' Same facts, different story." theme={theme}>Reframing</Highlight>. A technique like the "Failure Resume" helps you de-shame failure and see it not as a verdict on your worth, but as valuable data for future success. It's about learning to say, "I didn't suffer for nothing; I suffered to become stronger."</p></>)}
              <MicroCommitment theme={theme}>
                <p>Think of one failure from the last year. Now, name one thing you learned from it that you couldn't have learned otherwise. You've just taken the first step in writing a redemption script.</p>
              </MicroCommitment>
            </ReadingSection>
          )}
           {activeSection === 3 && (
            <ReadingSection title="The Advantage of Disadvantage." eyebrow="Step 4" icon={Award} theme={theme}>
              {essentials ? (<><p>What makes your journey harder might be making your learning deeper. <Highlight description="Study methods that feel harder and slower in the moment but actually help you remember things way better in the long run. The struggle is a feature, not a bug." theme={theme}>Desirable difficulties</Highlight> build stronger memory.<Cite n={2} /> Figuring things out alone beats being spoon-fed. Spreading study beats cramming.<Cite n={3} /> Your challenges are hidden training.</p></>) : (<><p>What if the things that make your academic journey harder are the very things that are making your learning deeper and more durable? This is the principle of <Highlight description="Study methods that feel harder and slower in the moment but actually help you remember things way better in the long run. The struggle is a feature, not a bug." theme={theme}>Desirable Difficulties</Highlight>.<Cite n={2} /> Learning that is "easy" (like re-reading notes) is shallow. Learning that is "hard" (like struggling to solve a problem without help) forces deeper processing and builds stronger neural pathways.</p>
              <p>If you have never had a private tutor, you have been forced to figure things out yourself — and that is actually one of the most powerful ways to learn. If you have less free time, you have probably had to spread your study out instead of cramming, which is exactly what the research says works best.<Cite n={3} /> Not having everything handed to you builds real problem-solving skills. These are not disadvantages — they are hidden training that students with every resource may never get.</p></>)}
              <DesirableDifficultyComparison />
            </ReadingSection>
          )}
          {activeSection === 4 && (
            <ReadingSection title="Your Redemption Script." eyebrow="Step 5" icon={FileText} theme={theme}>
              {essentials ? (<><p>You are the author of your story. Turn contamination into redemption. Balance self-reliance with connection. Reframe difficulty as advantage. Build your own "Failure Resume" below. Turn one past failure into an asset you can use.</p></>) : (<><p>You have the power to be the author of your own story. This module has given you the tools of narrative construction: the ability to turn contamination into redemption, to balance agency with communion, and to reframe difficulty as a desirable advantage. Now it's time to put it into practice.</p>
              <p>The final step is to build your own mini-"Failure Resume." By taking a past failure and actively converting it into an asset, you are practicing the core skill of resilient identity construction. You are forging your own redemption script, turning the lead of your past into the gold of your future.</p></>)}
              <div className="my-10 rounded-2xl p-6 md:p-8" style={{ backgroundColor: "var(--module-surface)", borderRadius: 18 }}>
                <h4 className="font-serif text-2xl font-semibold text-[var(--module-ink)] dark:text-[var(--module-ink)] text-center">My Redemption Story</h4>
                 <div className="mt-6 space-y-4">
                    <div>
                        <label className="block text-xs font-semibold text-[var(--module-ink)] dark:text-[var(--module-muted)] uppercase ml-4 mb-2">The Failure (Pivotal Moment):</label>
                        <select className="w-full bg-[var(--module-surface)] dark:bg-[var(--module-surface)] rounded-xl px-5 py-3.5 text-sm font-medium text-[var(--module-ink)] dark:text-[var(--module-ink)] outline-none" style={{ border: "1.5px solid var(--module-line)" }}><option>Failed a mock exam</option><option>Missed an assignment deadline</option><option>Didn't understand a topic in class</option></select>
                    </div>
                     <div>
                        <label className="block text-xs font-semibold text-[var(--module-ink)] dark:text-[var(--module-muted)] uppercase ml-4 mb-2">The Lesson (Your Asset):</label>
                        <textarea placeholder="What is the single most valuable lesson, skill, or piece of wisdom you gained from this experience?" className="w-full h-24 bg-[var(--module-surface)] dark:bg-[var(--module-surface)] rounded-xl px-5 py-3.5 text-sm font-medium text-[var(--module-ink)] dark:text-[var(--module-ink)] placeholder-zinc-400 outline-none" style={{ border: "1.5px solid var(--module-line)" }}></textarea>
                    </div>
                </div>
              </div>
            </ReadingSection>
          )}
        </>
      )}
    </ModuleLayout>
  );
};
export default StrategicAdvantageModule;
