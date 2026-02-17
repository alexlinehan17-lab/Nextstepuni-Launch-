/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
*/

import React, { useState, useEffect } from 'react';
import { motion } from 'framer-motion';
import {
  BrainCircuit, Shield, AlertTriangle, UserCheck
} from 'lucide-react';
import { ModuleProgress } from '../types';
import { blueTheme } from '../moduleThemes';
import { Highlight, ReadingSection, MicroCommitment, PersonalStory } from './ModuleShared';
import { ModuleLayout } from './ModuleLayout';
import { useModuleResponses } from '../hooks/useModuleResponses';

const theme = blueTheme;

// --- INTERACTIVE COMPONENTS ---

const MotionDiv = motion.div as any;
const MotionButton = motion.button as any;

type MemoryBlock = {
  label: string;
  threatened: boolean;
};

const INITIAL_BLOCKS: MemoryBlock[] = [
  { label: 'Recall', threatened: false },
  { label: 'Reasoning', threatened: false },
  { label: 'Analysis', threatened: false },
  { label: 'Focus', threatened: false },
  { label: 'Planning', threatened: false },
  { label: 'Comprehension', threatened: false },
  { label: 'Logic', threatened: false },
  { label: 'Creativity', threatened: false },
  { label: 'Attention', threatened: false },
  { label: 'Connections', threatened: false },
  { label: 'Evaluation', threatened: false },
  { label: 'Synthesis', threatened: false },
];

const THREAT_LABELS = [
  'Self-doubt',
  'Worry',
  'Am I good enough?',
  'They expect me to fail',
  'I don\'t belong',
];

const THREAT_INDICES = [2, 5, 8, 10, 11];

const WorkingMemoryGrid = () => {
  const [phase, setPhase] = useState<'full' | 'threatened' | 'restored'>('full');
  const [blocks, setBlocks] = useState<MemoryBlock[]>(INITIAL_BLOCKS);
  const [animating, setAnimating] = useState(false);

  const activeCount = blocks.filter(b => !b.threatened).length;
  const percentage = Math.round((activeCount / blocks.length) * 100);

  const handleSimulateThreat = () => {
    if (animating) return;
    setAnimating(true);
    const newBlocks = [...INITIAL_BLOCKS];
    let step = 0;

    const interval = setInterval(() => {
      if (step < THREAT_INDICES.length) {
        const idx = THREAT_INDICES[step];
        newBlocks[idx] = { label: THREAT_LABELS[step], threatened: true };
        setBlocks([...newBlocks]);
        step++;
      } else {
        clearInterval(interval);
        setPhase('threatened');
        setAnimating(false);
      }
    }, 500);
  };

  const handleActivateShield = () => {
    if (animating) return;
    setAnimating(true);
    const currentBlocks = [...blocks];
    const threatenedIndices = THREAT_INDICES.slice().reverse();
    let step = 0;

    const interval = setInterval(() => {
      if (step < threatenedIndices.length) {
        const idx = threatenedIndices[step];
        currentBlocks[idx] = { ...INITIAL_BLOCKS[idx], threatened: false };
        setBlocks([...currentBlocks]);
        step++;
      } else {
        clearInterval(interval);
        setPhase('restored');
        setAnimating(false);
      }
    }, 400);
  };

  const handleReset = () => {
    setBlocks([...INITIAL_BLOCKS]);
    setPhase('full');
  };

  return (
    <div className="my-10 p-8 md:p-12 bg-white dark:bg-zinc-800 rounded-xl border border-zinc-200 dark:border-zinc-700">
      <h4 className="font-serif text-2xl font-semibold text-zinc-800 dark:text-white text-center">
        Working Memory Under Threat
      </h4>
      <p className="text-center text-sm text-zinc-500 dark:text-zinc-400 mb-8">
        See how invisible pressure steals your brainpower — and how a simple exercise gives it back.
      </p>

      {/* Percentage indicator */}
      <div className="flex justify-center mb-6">
        <div className="inline-flex items-center gap-2 px-4 py-2 bg-zinc-100 dark:bg-zinc-700 rounded-full">
          <span className="text-sm font-mono font-bold text-zinc-600 dark:text-zinc-300">
            Working Memory:
          </span>
          <MotionDiv
            key={percentage}
            initial={{ scale: 1.3, opacity: 0 }}
            animate={{ scale: 1, opacity: 1 }}
            transition={{ type: 'spring', stiffness: 300, damping: 20 }}
            className={`text-lg font-mono font-bold ${
              percentage === 100
                ? 'text-blue-600 dark:text-blue-400'
                : percentage < 70
                ? 'text-red-500 dark:text-red-400'
                : 'text-amber-500 dark:text-amber-400'
            }`}
          >
            {percentage}%
          </MotionDiv>
        </div>
      </div>

      {/* Grid */}
      <div className="grid grid-cols-3 sm:grid-cols-4 gap-3 max-w-md mx-auto mb-8">
        {blocks.map((block, i) => (
          <MotionDiv
            key={i}
            layout
            animate={{
              backgroundColor: block.threatened ? undefined : undefined,
              scale: block.threatened ? [1, 0.9, 1] : 1,
            }}
            transition={{ type: 'spring', stiffness: 400, damping: 25 }}
            className={`relative flex items-center justify-center rounded-lg h-16 sm:h-18 text-center px-1 ${
              block.threatened
                ? 'bg-red-100 dark:bg-red-900/40 border-2 border-red-300 dark:border-red-700'
                : 'bg-blue-100 dark:bg-blue-900/40 border-2 border-blue-300 dark:border-blue-700'
            }`}
          >
            <MotionDiv
              key={block.label}
              initial={{ opacity: 0, y: 4 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.3 }}
              className={`text-xs font-bold leading-tight ${
                block.threatened
                  ? 'text-red-700 dark:text-red-300'
                  : 'text-blue-700 dark:text-blue-300'
              }`}
            >
              {block.label}
            </MotionDiv>
          </MotionDiv>
        ))}
      </div>

      {/* Buttons */}
      <div className="flex flex-col sm:flex-row items-center justify-center gap-3">
        {phase === 'full' && (
          <MotionButton
            onClick={handleSimulateThreat}
            disabled={animating}
            whileHover={{ scale: 1.04 }}
            whileTap={{ scale: 0.97 }}
            className="px-6 py-3 bg-red-500 hover:bg-red-600 text-white font-bold text-sm rounded-full shadow-lg transition-colors disabled:opacity-50"
          >
            Simulate Exam Pressure
          </MotionButton>
        )}
        {phase === 'threatened' && (
          <MotionButton
            onClick={handleActivateShield}
            disabled={animating}
            initial={{ opacity: 0, y: 8 }}
            animate={{ opacity: 1, y: 0 }}
            whileHover={{ scale: 1.04 }}
            whileTap={{ scale: 0.97 }}
            className="px-6 py-3 bg-blue-500 hover:bg-blue-600 text-white font-bold text-sm rounded-full shadow-lg transition-colors disabled:opacity-50"
          >
            Activate Shield (Values Affirmation)
          </MotionButton>
        )}
        {phase === 'restored' && (
          <MotionDiv
            initial={{ opacity: 0, y: 8 }}
            animate={{ opacity: 1, y: 0 }}
            className="flex flex-col items-center gap-3"
          >
            <p className="text-sm font-bold text-blue-600 dark:text-blue-400 text-center">
              Full capacity restored. Affirming your values frees your working memory.
            </p>
            <MotionButton
              onClick={handleReset}
              whileHover={{ scale: 1.04 }}
              whileTap={{ scale: 0.97 }}
              className="px-5 py-2 bg-zinc-200 dark:bg-zinc-700 hover:bg-zinc-300 dark:hover:bg-zinc-600 text-zinc-700 dark:text-zinc-200 font-bold text-sm rounded-full transition-colors"
            >
              Reset Demo
            </MotionButton>
          </MotionDiv>
        )}
      </div>
    </div>
  );
};

const ValuesSelector = ({ savedValues, onSave }: { savedValues?: string[]; onSave?: (values: string[]) => void }) => {
    const values = ["Family", "Friendship", "Creativity", "Kindness", "Humour", "Ambition", "Community", "Independence", "Learning"];
    const [selected, setSelected] = useState<string[]>(savedValues || []);

    useEffect(() => {
      if (savedValues) setSelected(savedValues);
    }, [savedValues]);

    const handleSelect = (value: string) => {
        let next: string[];
        if (selected.includes(value)) {
            next = selected.filter(v => v !== value);
        } else if (selected.length < 3) {
            next = [...selected, value];
        } else {
            return;
        }
        setSelected(next);
        onSave?.(next);
    };

    return(
        <div className="my-10 p-8 md:p-12 bg-white dark:bg-zinc-800 rounded-xl border border-zinc-200 dark:border-zinc-700">
             <h4 className="font-serif text-2xl font-semibold text-zinc-800 dark:text-white text-center">Core Values Audit</h4>
             <p className="text-center text-sm text-zinc-500 dark:text-zinc-400 mb-8">Select your top 3 most important personal values.</p>
             <div className="flex flex-wrap justify-center gap-3">
                {values.map(value => (
                    <motion.button
                        key={value}
                        onClick={() => handleSelect(value)}
                        className={`px-4 py-2 text-sm font-bold rounded-full border transition-all ${selected.includes(value) ? 'bg-blue-500 text-white border-blue-500' : 'bg-zinc-50 border-zinc-200 dark:border-zinc-700'}`}
                        whileHover={{y: -2}}
                    >
                        {value}
                    </motion.button>
                ))}
             </div>
             {selected.length === 3 && (
                <div className="mt-8">
                    <h5 className="font-bold text-center">Your 15-Minute Writing Prompt:</h5>
                    <p className="p-4 bg-zinc-100 dark:bg-zinc-800 rounded-xl mt-2 text-center text-sm">Choose ONE of these values: <span className="font-bold">{selected.join(', ')}</span>. Write for 15 minutes about why this value is important to you and describe a time when you lived up to it.</p>
                </div>
             )}
        </div>
    );
};

// --- MODULE COMPONENT ---
const AffirmingValuesModule: React.FC<{ onBack: () => void; progress: ModuleProgress; onProgressUpdate: (progress: ModuleProgress) => void }> = ({ onBack, progress, onProgressUpdate }) => {
  const { responses, saveResponse, isLoaded } = useModuleResponses('affirming-values');

  const sections = [
    { id: 'invisible-threat', title: 'The Invisible Threat', eyebrow: '01 // The Problem', icon: AlertTriangle },
    { id: 'psychological-shield', title: 'The Psychological Shield', eyebrow: '02 // The Solution', icon: Shield },
    { id: 'broaden-build', title: 'How It Works: The Zoom-Out Effect', eyebrow: '03 // The Mechanism', icon: BrainCircuit },
    { id: 'real-world-data', title: 'The Real World Data', eyebrow: '04 // The Evidence', icon: UserCheck },
    { id: 'your-protocol', title: 'Your Pre-Exam Protocol', eyebrow: '05 // The Action Plan', icon: UserCheck },
  ];

  return (
    <ModuleLayout
      moduleNumber="03"
      moduleTitle="Affirming Values"
      moduleSubtitle="The Psychological Shield"
      moduleDescription="Discover the invisible pressure that steals your brainpower in exams — and a simple 15-minute exercise that shields you from it."
      theme={theme}
      sections={sections}
      onBack={onBack}
      progress={progress}
      onProgressUpdate={onProgressUpdate}
    >
      {(activeSection) => (
        <>
          {activeSection === 0 && (
            <>
            <ReadingSection title="The Invisible Threat." eyebrow="Step 1" icon={AlertTriangle} theme={theme}>
              <p>In a high-stakes situation like the Leaving Cert, your brain is on high alert. For students from disadvantaged backgrounds, there's an extra, invisible threat in the room: the fear that a bad result will confirm what people already think about "people like you." This is called <Highlight description="That nagging background voice during an exam that says 'people like me don't get these results.' It's not just nerves — it actually takes up space in your brain, leaving less room for the actual questions." theme={theme}>Stereotype Threat</Highlight>.</p>
              <p>It's like a hidden tax on your brainpower. Part of your working memory gets hijacked by this background anxiety, leaving less room for the actual exam questions. This isn't just "in your head" — it's a real stress response that can cost you marks, even when you know the material perfectly.</p>
              <PersonalStory name="Alex" role="Founder, NextStepUni">
                <p>I know what this feels like. Walking into an exam hall, part of my brain was always running a background programme: "People from Togher don't get these kinds of results." I didn't have a name for it then, but it was stereotype threat. I was fighting the exam and fighting that voice at the same time — and I didn't realise it was costing me marks until I learned the science behind it.</p>
              </PersonalStory>
            </ReadingSection>
            <WorkingMemoryGrid />
            </>
          )}
           {activeSection === 1 && (
            <ReadingSection title="The Psychological Shield." eyebrow="Step 2" icon={Shield} theme={theme}>
              <p>Researchers spent years looking for a way to fight this invisible threat. The best solution they found is almost ridiculously simple: a 15-minute writing exercise called <Highlight description="Before a stressful event, you spend 15 minutes writing about what matters most to you — your family, your friends, your creativity. It reminds your brain that you're more than just an exam result, and that frees up the brainpower the threat was stealing." theme={theme}>Self-Affirmation</Highlight>.</p>
              <p>It sounds too good to be true, but it works. By writing about what's truly important to you before a stressful event — family, creativity, friendship — you create a mental shield. You remind your brain that your self-worth isn't defined by this one exam. That simple reminder frees up the brainpower that the threat would otherwise steal.</p>
            </ReadingSection>
          )}
           {activeSection === 2 && (
            <ReadingSection title="How It Works: The Zoom-Out Effect." eyebrow="Step 3" icon={BrainCircuit} theme={theme}>
              <p>How can a simple writing exercise have such a powerful effect? It comes down to how your brain handles emotions. When you're scared, your focus narrows — all you can see is the threat. But positive emotions do the opposite: they <Highlight description="When you feel good about who you are, your brain literally opens up. You see more options, think more clearly, and stop fixating on the one thing that's scaring you. It's like going from tunnel vision to a wide-angle lens." theme={theme}>Broaden Your Perspective</Highlight>.</p>
              <p>When you write about your values, your brain gets a hit of positive emotion — a reminder that you're more than this one exam. That "zooms out" your perspective. Suddenly the Leaving Cert isn't a life-or-death verdict on your entire identity; it's just one part of a much bigger, more meaningful life. That shift is what reduces the threat and frees up your working memory.</p>
            </ReadingSection>
          )}
          {activeSection === 3 && (
            <ReadingSection title="The Real World Data." eyebrow="Step 4" icon={UserCheck} theme={theme}>
              <p>This isn't just theory — it's been tested in real classrooms. Researchers gave a group of students from disadvantaged backgrounds this exact exercise: 15 minutes of writing about their values, just a few times a year. The result? Their grades jumped significantly — and the effect lasted.</p>
              <p>Two years later, those students were still outperforming their peers. The exercise had kicked off a positive cycle — better grades led to more confidence, which led to even better grades. And the effect was strongest for the students who were most at risk of underperforming. A 15-minute exercise, a few times a year, changed their trajectory.</p>
            </ReadingSection>
          )}
           {activeSection === 4 && (
            <ReadingSection title="Your Pre-Exam Protocol." eyebrow="Step 5" icon={UserCheck} theme={theme}>
              <p>You now have a genuine tool to protect your brain under pressure. The last step is to make it a habit — a pre-exam ritual you do every time, just like checking you have the right pens.</p>
              <p>The steps are simple: <strong>1. Pick your core values below.</strong> <strong>2. Choose the one that matters most right now.</strong> <strong>3. Write for 15 minutes.</strong> This isn't an essay — it's a private reflection. Write about why the value is important to you and describe a specific time you lived up to it. Do this before every major exam, especially the Mocks and the Leaving Cert.</p>
              <ValuesSelector savedValues={responses['selected-values']} onSave={(v) => saveResponse('selected-values', v)} />
              <MicroCommitment theme={theme}>
                <p>Take the values you selected above. Create a recurring event in your phone's calendar for the morning of every exam you have this year, with the title: "15 Min Values Writing." You now have a pre-exam shield that actually works.</p>
              </MicroCommitment>
            </ReadingSection>
          )}
        </>
      )}
    </ModuleLayout>
  );
};
export default AffirmingValuesModule;
