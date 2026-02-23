
/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
*/

import React, { useState } from 'react';
import { motion } from 'framer-motion';
import {
  Brain, Target, Shield, Eye, Settings
} from 'lucide-react';
import { ModuleProgress } from '../types';
import { roseTheme } from '../moduleThemes';
import { Highlight, ReadingSection, MicroCommitment, PersonalStory } from './ModuleShared';
import { ModuleLayout } from './ModuleLayout';
import { useNorthStar } from '../hooks/useNorthStar';
import NorthStarCallout from './NorthStarCallout';
import { COMPACT_CALLOUT_PLACEMENTS } from '../northStarData';

const theme = roseTheme;

const MotionPolygon = motion.polygon as any;

// --- INTERACTIVE COMPONENTS ---

const EFFICACY_DOMAINS = [
  'Maths & Problem Solving',
  'Essay Writing',
  'Memorisation & Recall',
  'Exam Performance Under Pressure',
  'Staying Focused for Long Sessions',
  'Understanding New Concepts',
];

const EfficacyRadar: React.FC = () => {
  const [values, setValues] = useState<number[]>([5, 5, 5, 5, 5, 5]);

  const size = 300;
  const cx = size / 2;
  const cy = size / 2;
  const maxR = 110;

  const angleStep = (2 * Math.PI) / 6;
  const startAngle = -Math.PI / 2; // top

  const pointOnHex = (index: number, radius: number) => {
    const angle = startAngle + index * angleStep;
    return {
      x: cx + radius * Math.cos(angle),
      y: cy + radius * Math.sin(angle),
    };
  };

  const hexagonPoints = (radius: number) =>
    Array.from({ length: 6 }, (_, i) => {
      const pt = pointOnHex(i, radius);
      return `${pt.x},${pt.y}`;
    }).join(' ');

  const dataPoints = values.map((v, i) => {
    const r = (v / 10) * maxR;
    const pt = pointOnHex(i, r);
    return `${pt.x},${pt.y}`;
  }).join(' ');

  const labelPositions = EFFICACY_DOMAINS.map((_, i) => {
    const pt = pointOnHex(i, maxR + 28);
    return pt;
  });

  const average = values.reduce((a, b) => a + b, 0) / values.length;

  const lowDomains = EFFICACY_DOMAINS.filter((_, i) => values[i] <= 3);
  const allHigh = values.every((v) => v >= 7);

  return (
    <div className="my-10 p-8 md:p-12 bg-white dark:bg-zinc-800 rounded-xl border border-zinc-200 dark:border-zinc-700">
      <h4 className="font-serif text-2xl font-semibold text-zinc-800 dark:text-white text-center">
        Self-Efficacy Radar
      </h4>
      <p className="text-center text-sm text-zinc-500 dark:text-zinc-400 mb-8">
        Rate your belief in your ability across these 6 domains (1 = no confidence, 10 = total confidence).
      </p>

      {/* Radar Chart */}
      <div className="flex justify-center mb-8">
        <svg
          viewBox={`0 0 ${size} ${size}`}
          className="w-full max-w-xs"
          style={{ overflow: 'visible' }}
        >
          {/* Grid hexagons */}
          {[0.33, 0.66, 1].map((scale) => (
            <polygon
              key={scale}
              points={hexagonPoints(maxR * scale)}
              fill="none"
              stroke="currentColor"
              className="text-zinc-200 dark:text-zinc-600"
              strokeWidth="1"
            />
          ))}

          {/* Axis lines */}
          {Array.from({ length: 6 }, (_, i) => {
            const pt = pointOnHex(i, maxR);
            return (
              <line
                key={i}
                x1={cx}
                y1={cy}
                x2={pt.x}
                y2={pt.y}
                stroke="currentColor"
                className="text-zinc-200 dark:text-zinc-600"
                strokeWidth="0.5"
              />
            );
          })}

          {/* Data polygon */}
          <MotionPolygon
            points={dataPoints}
            fill="rgba(225,29,72,0.15)"
            stroke="#e11d48"
            strokeWidth="2"
            initial={false}
            animate={{ points: dataPoints }}
            transition={{ type: 'spring', stiffness: 200, damping: 20 }}
          />

          {/* Data point dots */}
          {values.map((v, i) => {
            const r = (v / 10) * maxR;
            const pt = pointOnHex(i, r);
            return (
              <circle
                key={i}
                cx={pt.x}
                cy={pt.y}
                r="4"
                fill="#e11d48"
              />
            );
          })}

          {/* Labels */}
          {labelPositions.map((pt, i) => (
            <text
              key={i}
              x={pt.x}
              y={pt.y}
              textAnchor="middle"
              dominantBaseline="middle"
              className="fill-zinc-600 dark:fill-zinc-300"
              fontSize="9"
              fontWeight="500"
            >
              {EFFICACY_DOMAINS[i].length > 20
                ? EFFICACY_DOMAINS[i].split(' ').reduce<string[]>((lines, word) => {
                    const current = lines[lines.length - 1];
                    if (current && (current + ' ' + word).length <= 18) {
                      lines[lines.length - 1] = current + ' ' + word;
                    } else {
                      lines.push(word);
                    }
                    return lines;
                  }, []).map((line, li) => (
                    <tspan key={li} x={pt.x} dy={li === 0 ? '0' : '1.1em'}>
                      {line}
                    </tspan>
                  ))
                : EFFICACY_DOMAINS[i]}
            </text>
          ))}
        </svg>
      </div>

      {/* Sliders */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-x-8 gap-y-4 max-w-2xl mx-auto mb-8">
        {EFFICACY_DOMAINS.map((domain, i) => (
          <div key={domain}>
            <div className="flex justify-between items-baseline mb-1">
              <label className="text-sm font-medium text-zinc-700 dark:text-zinc-300">
                {domain}
              </label>
              <span className="text-sm font-bold text-rose-600 dark:text-rose-400 tabular-nums">
                {values[i]}
              </span>
            </div>
            <input
              type="range"
              min={1}
              max={10}
              value={values[i]}
              onChange={(e) => {
                const next = [...values];
                next[i] = Number(e.target.value);
                setValues(next);
              }}
              className="w-full h-2 rounded-lg appearance-none cursor-pointer bg-zinc-200 dark:bg-zinc-600 accent-rose-500"
            />
          </div>
        ))}
      </div>

      {/* Score & Insight */}
      <div className="text-center">
        <p className="text-lg font-semibold text-zinc-800 dark:text-white">
          Self-Efficacy Score:{' '}
          <span className="text-rose-600 dark:text-rose-400">{average.toFixed(1)}/10</span>
        </p>
        {lowDomains.length > 0 && (
          <motion.p
            key={lowDomains.join(',')}
            initial={{ opacity: 0, y: 4 }}
            animate={{ opacity: 1, y: 0 }}
            className="mt-3 text-sm text-amber-700 dark:text-amber-400"
          >
            Your belief in <span className="font-bold">{lowDomains[0]}</span> is low — this module will show you how to build it up.
          </motion.p>
        )}
        {allHigh && lowDomains.length === 0 && (
          <motion.p
            initial={{ opacity: 0, y: 4 }}
            animate={{ opacity: 1, y: 0 }}
            className="mt-3 text-sm text-emerald-700 dark:text-emerald-400 font-semibold"
          >
            Strong foundation — now let's make it bulletproof.
          </motion.p>
        )}
      </div>
    </div>
  );
};
const RoleModelSelector = () => {
    const [choice, setChoice] = useState<null | 'mastery' | 'coping'>(null);
    return (
        <div className="my-10 p-8 md:p-12 bg-white dark:bg-zinc-800 rounded-xl border border-zinc-200 dark:border-zinc-700">
             <h4 className="font-serif text-2xl font-semibold text-zinc-800 dark:text-white text-center">Which Story Builds More Belief?</h4>
             <p className="text-center text-sm text-zinc-500 dark:text-zinc-400 mb-6">You're struggling with a subject. Which of these role models is more helpful?</p>
             <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                <button onClick={() => setChoice('mastery')} className={`p-6 rounded-xl text-left border flex flex-col justify-between h-48 ${choice === 'mastery' ? 'bg-blue-500 text-white border-blue-500' : 'bg-zinc-50 hover:bg-zinc-100 dark:hover:bg-zinc-700 border-zinc-200 dark:border-zinc-700'}`}>
                    <div>
                        <p className="font-bold text-lg">The Genius (Mastery Model)</p>
                        <p className="text-xs mt-1">A past pupil who got 625 points, found school easy, and is now a doctor.</p>
                    </div>
                    <p className="text-xs font-mono self-end">"Just work hard."</p>
                </button>
                 <button onClick={() => setChoice('coping')} className={`p-6 rounded-xl text-left border flex flex-col justify-between h-48 ${choice === 'coping' ? 'bg-emerald-500 text-white border-emerald-500' : 'bg-zinc-50 hover:bg-zinc-100 dark:hover:bg-zinc-700 border-zinc-200 dark:border-zinc-700'}`}>
                    <div>
                        <p className="font-bold text-lg">The Grafter (Coping Model)</p>
                        <p className="text-xs mt-1">A past pupil who failed their mocks, changed their study habits, and got into their dream course.</p>
                    </div>
                     <p className="text-xs font-mono self-end">"Here's how I recovered."</p>
                </button>
             </div>
             {choice === 'coping' && <motion.p initial={{opacity:0}} animate={{opacity:1}} className="text-center mt-4 text-sm text-emerald-700 font-bold">Correct. Seeing someone struggle and bounce back is way more motivating than watching someone who made it look easy.</motion.p>}
        </div>
    );
};

const IcebergInteractive = () => {
    const [inputs, setInputs] = useState<string[]>([]);
    return (
        <div className="my-10 p-8 md:p-12 bg-white dark:bg-zinc-800 rounded-xl border border-zinc-200 dark:border-zinc-700">
            <h4 className="font-serif text-2xl font-semibold text-zinc-800 dark:text-white text-center">The Success Iceberg</h4>
            <p className="text-center text-sm text-zinc-500 dark:text-zinc-400 mb-8">Success is what people see. Process is what it takes. List the "invisible" parts of success.</p>
            <div className="max-w-md mx-auto">
                <div className="bg-blue-100 p-4 rounded-t-2xl text-center font-bold text-blue-800">Visible Success</div>
                <div className="bg-blue-50 p-6 rounded-b-2xl border-x-2 border-b-2 border-blue-200 min-h-[150px]">
                    <p className="text-sm font-bold text-zinc-600 dark:text-zinc-300 mb-2">Invisible Process:</p>
                    <ul className="list-disc list-inside text-sm text-zinc-500 dark:text-zinc-400 space-y-1">
                        {inputs.map((input, i) => <li key={i}>{input}</li>)}
                    </ul>
                     <input
                        placeholder="e.g., failed attempts, asking for help..."
                        className="w-full mt-4 p-2 text-sm bg-white dark:bg-zinc-800 border border-zinc-300 rounded-md"
                        onKeyDown={(e) => {
                            if (e.key === 'Enter' && e.currentTarget.value) {
                                setInputs([...inputs, e.currentTarget.value]);
                                e.currentTarget.value = '';
                            }
                        }}
                    />
                </div>
            </div>
        </div>
    );
}

// --- MODULE COMPONENT ---
const SelfEfficacyModule: React.FC<{ onBack: () => void; progress: ModuleProgress; onProgressUpdate: (progress: ModuleProgress) => void }> = ({ onBack, progress, onProgressUpdate }) => {
  const { northStar } = useNorthStar();
  const sections = [
    { id: 'belief-barrier', title: 'The Belief Barrier', eyebrow: '01 // Your Secret Engine', icon: Brain },
    { id: 'four-sources', title: 'How Belief is Built', eyebrow: '02 // The 4 Sources', icon: Target },
    { id: 'role-model-myth', title: 'The Role Model Myth', eyebrow: '03 // The Struggle Story', icon: Shield },
    { id: 'success-iceberg', title: 'The Success Iceberg', eyebrow: '04 // Detective of Process', icon: Eye },
    { id: 'habit-blueprint', title: 'The Habit Blueprint', eyebrow: '05 // Reverse-Engineer Success', icon: Settings },
  ];

  return (
    <ModuleLayout
      moduleNumber="09"
      moduleTitle="Self Efficacy"
      moduleSubtitle="The Architecture of Agency"
      moduleDescription={`"Try harder" is useless advice. This module shows you how to actually build real belief in yourself — the kind that sticks.`}
      theme={theme}
      sections={sections}
      onBack={onBack}
      progress={progress}
      onProgressUpdate={onProgressUpdate}
      finishButtonText="Build Your Belief"
    >
      {(activeSection) => (
        <>
          {activeSection === 0 && (
            <>
              <ReadingSection title="The Belief Barrier." eyebrow="Step 1" icon={Brain} theme={theme}>
                <p>Let's get one thing straight: the biggest barrier to your success isn't a lack of talent. It's a lack of belief. This core belief in your own ability is called <Highlight description="Your gut-level belief that you can actually do the thing you're trying to do. It's not about having the skill — it's about trusting yourself to use it when it counts." theme={theme}>Self-Efficacy</Highlight>. It's the engine that drives effort, persistence, and how you bounce back from setbacks.</p>
                <p>Think of it like this: a car might have a full tank of petrol (your knowledge and skills), but if the driver doesn't believe they can actually drive, the car is going nowhere. For students from tough backgrounds, society often spends years convincing you that you don't belong in the driver's seat. This module is about grabbing the keys.</p>
                <PersonalStory name="Alex" role="Founder, NextStepUni">
                  <p>Nobody in my life ever told me I was capable of getting high points. Not because they were cruel — they just didn't have that frame of reference. When you grow up in Togher, "belief in your academic ability" isn't something anyone talks about. I didn't lack talent. I lacked a single person who made me believe the driver's seat was mine to take.</p>
                </PersonalStory>
              </ReadingSection>
              <EfficacyRadar />
            </>
          )}
          {activeSection === 1 && (
            <ReadingSection title="How Belief is Built." eyebrow="Step 2" icon={Target} theme={theme}>
                <p>So where does this belief come from? It's not magic, and it's not something you're born with. It comes from four main places. Once you know what they are, you can actually start building it on purpose.</p>
                <p>The four sources are: 1) <Highlight description="The strongest way to build belief in yourself — by actually doing the thing and seeing it work. Even tiny wins count here." theme={theme}>Enactive Mastery</Highlight> (your own wins), 2) <Highlight description="When you see someone like you pull it off, your brain goes 'well, if they managed it, maybe I can too.' That feeling is gold." theme={theme}>Vicarious Experience</Highlight> (watching others win), 3) Social Persuasion (real encouragement), and 4) Physiological States (learning to read your body's signals). For students who haven't had a long history of easy wins, the second source—Vicarious Experience—is the most important lever we can pull.</p>
            </ReadingSection>
          )}
          {activeSection === 2 && (
            <ReadingSection title="The Role Model Myth." eyebrow="Step 3" icon={Shield} theme={theme}>
              <p>We're often told to look up to flawless heroes — the sporting legend, the genius scientist. These are <Highlight description="The kind of role model who makes everything look effortless. Inspiring on the surface, but they can actually make you feel like success is out of reach." theme={theme}>Mastery Models</Highlight>. But here's the thing: they can actually make you feel *worse* about yourself. Their success looks so effortless that the gap between where you are and where they are feels impossible to close.</p>
              <p>The better option is to find <Highlight description="Role models who are honest about their struggles and show you how they bounced back. Way more helpful for building your own belief than watching someone who never seemed to struggle." theme={theme}>Coping Models</Highlight>. These are people who are relatable, who fail, and who show you *how* they get back up. Hearing about how even the most successful people struggled and messed up is far more motivating than just hearing about their wins. It proves that struggle is part of the path, not a sign you're on the wrong one.</p>
              <RoleModelSelector/>
            </ReadingSection>
          )}
           {activeSection === 3 && (
            <ReadingSection title="The Success Iceberg." eyebrow="Step 4" icon={Eye} theme={theme}>
              {northStar && (() => { const p = COMPACT_CALLOUT_PLACEMENTS.find(p => p.moduleId === 'self-efficacy-protocol'); return p ? <NorthStarCallout northStar={northStar} variant="compact" message={p.message} /> : null; })()}
              <p>This brings us to the big idea of this whole module: stop just admiring other people's results and start figuring out how they actually got there. Success is like an iceberg. People only see the tip — the good grades, the confidence, the final result. They don't see the massive, messy reality underneath.</p>
              <p>The underwater part is the process: the failures, the wrong turns, the doubt, the boring routines, the asking for help. To build your own belief, you need to get good at spotting this invisible part. Start noticing the <Highlight description="The behind-the-scenes thinking that good students do without even realising it — things like noticing when something isn't working and switching approach. You can learn to do this too." theme={theme}>Metacognitive Regulation</Highlight> — the small, smart moves people make when they get stuck.</p>
              <IcebergInteractive />
            </ReadingSection>
          )}
          {activeSection === 4 && (
            <ReadingSection title="The Habit Blueprint." eyebrow="Step 5" icon={Settings} theme={theme}>
              <p>Once you start seeing the process behind other people's success, the final step is to bring it into your own life. Look at what works for them and turn it into habits you can repeat. The trick is to stop relying on willpower — it always runs out — and instead set up systems that run on autopilot.</p>
              <p>There are two key tools for this. First, <Highlight description="Making the thing you need to do so ridiculously small that you can't say no. When motivation is nowhere to be found, this is how you still get moving." theme={theme}>Micro-Habits</Highlight>, which break a big action down into something tiny (e.g. "write 2,000 words" becomes "write 3 sentences"). Second, <Highlight description="A dead-simple 'If X happens, Then I do Y' rule that takes the decision-making out of it. You decide once, and then it just happens on autopilot." theme={theme}>Implementation Intentions</Highlight>, which create an "If-Then" plan that puts your micro-habit on autopilot (e.g. "IF I open my laptop, THEN I will write 3 sentences"). This is how you build a system for success, one tiny, automatic step at a time.</p>
              <MicroCommitment theme={theme}>
                <p>Take one big study goal you have. Now, what's the smallest possible version of it you could do in two minutes? (e.g., "Revise all of Chapter 3" becomes "Read the first paragraph of Chapter 3"). That's your micro-habit.</p>
              </MicroCommitment>
            </ReadingSection>
          )}
        </>
      )}
    </ModuleLayout>
  );
};
export default SelfEfficacyModule;
