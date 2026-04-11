/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
*/

import React, { useState, useEffect, useRef } from 'react';
import { motion } from 'framer-motion';
import { MotionDiv } from './Motion';
import {
  BrainCircuit, Shield, AlertTriangle, UserCheck
} from 'lucide-react';
import { type ModuleProgress } from '../types';
import { blueTheme } from '../moduleThemes';
import { Highlight, ReadingSection, MicroCommitment, PersonalStory } from './ModuleShared';
import { ModuleLayout } from './ModuleLayout';
import { useModuleResponses } from '../hooks/useModuleResponses';

const theme = blueTheme;

// --- INTERACTIVE COMPONENTS ---

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
  const intervalRef = useRef<ReturnType<typeof setInterval> | null>(null);

  // Clean up any running interval on unmount
  useEffect(() => {
    return () => {
      if (intervalRef.current) clearInterval(intervalRef.current);
    };
  }, []);

  const activeCount = blocks.filter(b => !b.threatened).length;
  const percentage = Math.round((activeCount / blocks.length) * 100);

  const handleSimulateThreat = () => {
    if (animating) return;
    setAnimating(true);
    const newBlocks = [...INITIAL_BLOCKS];
    let step = 0;

    intervalRef.current = setInterval(() => {
      if (step < THREAT_INDICES.length) {
        const idx = THREAT_INDICES[step];
        newBlocks[idx] = { label: THREAT_LABELS[step], threatened: true };
        setBlocks([...newBlocks]);
        step++;
      } else {
        clearInterval(intervalRef.current!);
        intervalRef.current = null;
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

    intervalRef.current = setInterval(() => {
      if (step < threatenedIndices.length) {
        const idx = threatenedIndices[step];
        currentBlocks[idx] = { ...INITIAL_BLOCKS[idx], threatened: false };
        setBlocks([...currentBlocks]);
        step++;
      } else {
        clearInterval(intervalRef.current!);
        intervalRef.current = null;
        setPhase('restored');
        setAnimating(false);
      }
    }, 400);
  };

  const handleReset = () => {
    setBlocks([...INITIAL_BLOCKS]);
    setPhase('full');
  };

  const threatenedCount = blocks.filter(b => b.threatened).length;
  const productiveBlocks = blocks.filter(b => !b.threatened);
  const intrusiveBlocks = blocks.filter(b => b.threatened);
  const showBar = phase === 'threatened' && !animating;
  const pctColor = percentage === 100 ? '#2A7D6F' : percentage < 70 ? '#DC2626' : '#D97706';

  return (
    <div className="my-10 rounded-2xl p-6 md:p-8" style={{ backgroundColor: '#F8F8F8', borderRadius: 18 }}>
      <h4 className="font-serif text-2xl font-semibold text-zinc-800 dark:text-white text-center">
        Working Memory Under Threat
      </h4>
      <p className="text-center text-sm text-zinc-500 dark:text-zinc-400 mb-8">
        See how invisible pressure steals your brainpower — and how a simple exercise gives it back.
      </p>

      {/* Capacity meter */}
      <div className="max-w-md mx-auto mb-6">
        <div className="flex items-baseline justify-between mb-2">
          <span className="text-xs font-medium tracking-wider uppercase text-zinc-500">Brain Capacity</span>
          <MotionDiv
            key={percentage}
            initial={{ scale: 1.3, opacity: 0 }}
            animate={{ scale: 1, opacity: 1 }}
            transition={{ type: 'spring', stiffness: 300, damping: 20 }}
            className="font-serif font-bold text-xl"
            style={{ color: pctColor }}
          >
            {percentage}%
          </MotionDiv>
        </div>
        <div className="bg-white dark:bg-zinc-800" style={{ border: '2.5px solid #1C1917', borderRadius: 12, boxShadow: '3px 3px 0px 0px #1C1917', height: 20, overflow: 'hidden' }}>
          <MotionDiv
            className="h-full"
            style={{ backgroundColor: pctColor }}
            animate={{ width: `${percentage}%` }}
            transition={{ duration: 0.5, ease: [0.16, 1, 0.3, 1] }}
          />
        </div>
      </div>

      {/* Grid view (visible when not in completed threatened state) */}
      {!showBar && (
        <div className="grid grid-cols-3 sm:grid-cols-4 gap-3 max-w-md mx-auto mb-8">
          {blocks.map((block, i) => (
            <MotionDiv
              key={i}
              animate={{ scale: block.threatened ? [1, 0.9, 1] : 1 }}
              transition={{ type: 'spring', stiffness: 400, damping: 25 }}
              className="relative flex items-center justify-center h-16 text-center px-1"
              style={{
                backgroundColor: block.threatened ? '#FCA5A5' : '#93C5FD',
                border: '2.5px solid #1C1917',
                borderRadius: 12,
                boxShadow: '3px 3px 0px 0px #1C1917',
              }}
            >
              <MotionDiv
                key={block.label}
                initial={{ opacity: 0, y: 4 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ duration: 0.3 }}
                className="text-xs font-bold leading-tight"
                style={{ color: block.threatened ? '#991B1B' : '#1E3A8A' }}
              >
                {block.label}
              </MotionDiv>
            </MotionDiv>
          ))}
        </div>
      )}

      {/* Stacked bar view (visible when threat animation finished) */}
      {showBar && (
        <MotionDiv
          initial={{ opacity: 0, y: 8 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.5 }}
          className="max-w-md mx-auto mb-8"
        >
          <div className="flex" style={{ border: '2.5px solid #1C1917', borderRadius: 16, boxShadow: '4px 4px 0px 0px #1C1917', overflow: 'hidden', height: 80 }}>
            {/* Productive segment */}
            <div className="flex flex-col items-center justify-center" style={{ flex: activeCount, backgroundColor: '#2563EB', borderRight: threatenedCount > 0 ? '2.5px solid #1C1917' : 'none' }}>
              <span className="text-[11px] font-medium uppercase tracking-wider" style={{ color: 'rgba(255,255,255,0.6)' }}>Productive</span>
              <span className="font-serif font-bold text-2xl text-white">{percentage}%</span>
            </div>
            {/* Intrusive segment */}
            {threatenedCount > 0 && (
              <div className="flex flex-col items-center justify-center" style={{ flex: threatenedCount, backgroundColor: '#DC2626' }}>
                <span className="text-[11px] font-medium uppercase tracking-wider" style={{ color: 'rgba(255,255,255,0.6)' }}>Intrusive</span>
                <span className="font-serif font-bold text-2xl text-white">{100 - percentage}%</span>
              </div>
            )}
          </div>

          {/* Tag chips below the bar */}
          <div className="flex gap-3 mt-3">
            <div className="flex flex-wrap gap-1.5" style={{ flex: activeCount }}>
              {productiveBlocks.map((b, i) => (
                <span key={i} className="text-[11px] font-medium px-2.5 py-1" style={{ backgroundColor: '#EFF6FF', border: '1.5px solid #2563EB', borderRadius: 8, color: '#1E3A8A' }}>{b.label}</span>
              ))}
            </div>
            <div className="flex flex-wrap gap-1.5" style={{ flex: threatenedCount }}>
              {intrusiveBlocks.map((b, i) => (
                <span key={i} className="text-[11px] font-medium px-2.5 py-1" style={{ backgroundColor: '#FEF2F2', border: '1.5px solid #DC2626', borderRadius: 8, color: '#7F1D1D' }}>{b.label}</span>
              ))}
            </div>
          </div>
        </MotionDiv>
      )}

      {/* Buttons */}
      <div className="flex flex-col sm:flex-row items-center justify-center gap-3">
        {phase === 'full' && (
          <motion.button
            onClick={handleSimulateThreat}
            disabled={animating}
            className="px-6 py-3 text-white font-bold text-sm disabled:opacity-50"
            style={{ backgroundColor: '#DC2626', border: '2.5px solid #1C1917', borderRadius: 14, boxShadow: '4px 4px 0px 0px #1C1917' }}
            whileHover={{ x: -2, y: -2, boxShadow: '6px 6px 0px 0px #1C1917' }}
            whileTap={{ x: 2, y: 2, boxShadow: '1px 1px 0px 0px #1C1917' }}
            transition={{ type: 'spring', stiffness: 400, damping: 25 }}
          >
            Simulate Exam Pressure
          </motion.button>
        )}
        {phase === 'threatened' && (
          <motion.button
            onClick={handleActivateShield}
            disabled={animating}
            initial={{ opacity: 0, y: 8 }}
            animate={{ opacity: 1, y: 0 }}
            className="px-6 py-3 text-white font-bold text-sm disabled:opacity-50"
            style={{ backgroundColor: '#2A7D6F', border: '2.5px solid #1F5F54', borderRadius: 14, boxShadow: '4px 4px 0px 0px #1F5F54' }}
            whileHover={{ x: -2, y: -2, boxShadow: '6px 6px 0px 0px #1F5F54' }}
            whileTap={{ x: 2, y: 2, boxShadow: '1px 1px 0px 0px #1F5F54' }}
            transition={{ type: 'spring', stiffness: 400, damping: 25 }}
          >
            Activate Shield (Values Affirmation)
          </motion.button>
        )}
        {phase === 'restored' && (
          <MotionDiv
            initial={{ opacity: 0, y: 8 }}
            animate={{ opacity: 1, y: 0 }}
            className="flex flex-col items-center gap-3"
          >
            <div className="p-4 rounded-xl text-center" style={{ backgroundColor: '#6EE7B7', border: '2.5px solid #059669', boxShadow: '3px 3px 0px 0px #059669' }}>
              <p className="text-sm font-bold" style={{ color: '#064E3B' }}>
                Full capacity restored. Affirming your values frees your working memory.
              </p>
            </div>
            <motion.button
              onClick={handleReset}
              className="px-5 py-2 font-bold text-sm"
              style={{ backgroundColor: '#FFFFFF', border: '2.5px solid #1C1917', borderRadius: 14, boxShadow: '3px 3px 0px 0px #1C1917', color: '#1C1917' }}
              whileHover={{ x: -1, y: -1, boxShadow: '4px 4px 0px 0px #1C1917' }}
              whileTap={{ x: 1, y: 1, boxShadow: '1px 1px 0px 0px #1C1917' }}
              transition={{ type: 'spring', stiffness: 400, damping: 25 }}
            >
              Reset Demo
            </motion.button>
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
        <div className="my-10 rounded-2xl p-6 md:p-8" style={{ backgroundColor: '#F8F8F8', borderRadius: 18 }}>
             <h4 className="font-serif text-2xl font-semibold text-zinc-800 dark:text-white text-center">Core Values Audit</h4>
             <p className="text-center text-sm text-zinc-500 dark:text-zinc-400 mb-8">Select your top 3 most important personal values.</p>
             <div className="flex flex-wrap justify-center gap-3">
                {values.map(value => (
                    <motion.button
                        key={value}
                        onClick={() => handleSelect(value)}
                        className={`px-4 py-2 text-sm font-bold rounded-full transition-all ${selected.includes(value) ? 'bg-blue-500 text-white' : ''}`}
                        style={selected.includes(value) ? { border: '2.5px solid #1D4ED8', boxShadow: '3px 3px 0px 0px #1D4ED8' } : { backgroundColor: '#FFFFFF', border: '2.5px solid #1C1917', boxShadow: '3px 3px 0px 0px #1C1917' }}
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
  const { responses, saveResponse, isLoaded: _isLoaded } = useModuleResponses('affirming-values');

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
      finishButtonText="Raise Your Shield"
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
