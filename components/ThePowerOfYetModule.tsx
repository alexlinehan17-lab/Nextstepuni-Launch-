

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
const ErrorSignalVisualizer = () => {
    const [mindset, setMindset] = useState<'fixed' | 'growth' | null>(null);
    return(
        <div className="my-10 p-8 md:p-12 bg-white dark:bg-zinc-800 rounded-xl border border-zinc-200 dark:border-zinc-700">
             <h4 className="font-serif text-2xl font-semibold text-zinc-800 dark:text-white text-center">The Brain on "Yet"</h4>
             <p className="text-center text-sm text-zinc-500 dark:text-zinc-400 mb-8">Scenario: You make a mistake on a Maths problem. Which brain is yours?</p>
             <div className="grid grid-cols-2 gap-6">
                <div className="text-center">
                    <h5 className="font-bold mb-2">The "I Can't" Brain (Fixed)</h5>
                    <svg viewBox="0 0 100 50" className="w-full h-auto">
                       <path d="M 0 40 L 100 40" stroke="#e5e7eb" strokeWidth="1" />
                       <path d="M 40 40 C 45 40 48 30 52 30 S 57 40 60 40" stroke="#f43f5e" strokeWidth="1" fill="none" />
                       <text x="50" y="20" textAnchor="middle" fontSize="6" fill="#f43f5e">Small 'Pe' Wave</text>
                    </svg>
                    <p className="text-xs text-zinc-500 dark:text-zinc-400 mt-2">The brain "looks away" from the error to protect the ego. No learning occurs.</p>
                </div>
                 <div className="text-center">
                    <h5 className="font-bold mb-2">The "I Can't... Yet" Brain (Growth)</h5>
                    <svg viewBox="0 0 100 50" className="w-full h-auto">
                       <path d="M 0 40 L 100 40" stroke="#e5e7eb" strokeWidth="1" />
                       <path d="M 40 40 C 45 40 48 5 52 5 S 57 40 60 40" stroke="#10b981" strokeWidth="3" fill="none" />
                       <text x="50" y="20" textAnchor="middle" fontSize="6" fill="#10b981">Large 'Pe' Wave</text>
                    </svg>
                    <p className="text-xs text-zinc-500 dark:text-zinc-400 mt-2">The brain leans in, allocating massive attention to the error. Learning is triggered.</p>
                </div>
             </div>
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
              <ErrorSignalVisualizer />
            </ReadingSection>
          )}
           {activeSection === 3 && (
            <ReadingSection title="The Action Bridge." eyebrow="Step 4" icon={Link} theme={theme}>
                <p>"Yet" is powerful, but it's not magic. On its own, it's just wishful thinking. To be effective, "yet" must be tethered to a behavioral plan. This is the crucial third step of the protocol: the <Highlight description="A concrete, specific action that you will take to move from 'not yet' to 'can'. This tethers optimism to a behavioral plan." theme={theme}>Bridge to Action</Highlight>.</p>
                <p>The full, powerful sentence isn't just "I can't do this yet." It's "I can't do this yet, *so I will*..." This simple addition prevents "Yet" from being an excuse and turns it into a launchpad. It links the optimistic mindset to a concrete, strategic next step. This is the full protocol: **1. Identify the Block, 2. Add "Yet", 3. Bridge to Action.**</p>
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
