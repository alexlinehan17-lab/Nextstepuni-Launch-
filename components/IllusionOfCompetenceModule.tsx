/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
*/

import React, { useState } from 'react';
import { motion } from 'framer-motion';
import {
  Eye, AlertTriangle, Lightbulb, SlidersHorizontal, Brain, Wrench
} from 'lucide-react';
import { ModuleProgress } from '../types';
import { tealTheme } from '../moduleThemes';
import { Highlight, ReadingSection, MicroCommitment } from './ModuleShared';
import { ModuleLayout } from './ModuleLayout';

const theme = tealTheme;

// --- INTERACTIVE COMPONENTS ---

const ForgettingCurveSimulator = () => {
    const [reviews, setReviews] = useState(0);
    const retention = reviews === 0 ? 3 : reviews === 1 ? 45 : reviews === 2 ? 75 : 95;

    return (
        <div className="my-10 p-8 md:p-12 bg-white rounded-[3rem] border border-stone-200 shadow-xl">
            <h4 className="font-serif text-2xl font-semibold text-stone-800 text-center italic">The Forgetting Curve</h4>
            <p className="text-center text-sm text-stone-500 mb-8">Without review, you forget ~80% of what you learn in 24 hours.</p>
            <div className="w-full h-48 bg-stone-50 rounded-lg p-4">
                 <svg viewBox="0 0 100 100" className="w-full h-full" preserveAspectRatio="none">
                    <motion.path d={`M 0 5 C 20 10, 40 40, 100 ${100-retention}`} fill="none" stroke="#14b8a6" strokeWidth="3" transition={{type: 'spring', damping: 10}}/>
                    <path d={`M 0 5 C 20 10, 40 40, 100 97`} fill="none" stroke="#e5e7eb" strokeWidth="2" strokeDasharray="4"/>
                 </svg>
            </div>
            <p className="text-center font-bold mt-4">Retention after 1 Week: <span className="text-teal-600">{retention}%</span></p>
            <div className="flex justify-center gap-2 mt-4">
                <button onClick={() => setReviews(reviews + 1)} className="px-3 py-1 text-xs bg-stone-200 rounded-md">Add Review</button>
                <button onClick={() => setReviews(0)} className="px-3 py-1 text-xs bg-stone-200 rounded-md">Reset</button>
            </div>
        </div>
    );
};

const FeynmanExplainer = () => {
    const concept = "Osmosis is the net movement of water molecules through a selectively permeable membrane from a region of higher water concentration to a region of lower water concentration.";
    const [explanation, setExplanation] = useState('');
    const jargon = ['molecules', 'selectively', 'permeable', 'concentration'];
    const jargonCount = jargon.filter(word => explanation.toLowerCase().includes(word)).length;

    return(
        <div className="my-10 p-8 md:p-12 bg-white rounded-[3rem] border border-stone-200 shadow-xl">
             <h4 className="font-serif text-2xl font-semibold text-stone-800 text-center italic">The Feynman Explainer</h4>
             <p className="text-center text-sm text-stone-500 mb-4">Task: Explain this definition of Osmosis in simple terms, as if to a 12-year-old.</p>
             <p className="p-4 bg-stone-100 border border-stone-200 rounded-xl text-xs text-center mb-4">{concept}</p>
             <textarea value={explanation} onChange={e => setExplanation(e.target.value)} className="w-full h-32 p-4 bg-stone-50 border-2 border-stone-200 rounded-xl focus:outline-none focus:border-teal-400" placeholder="Your simple explanation..."></textarea>
             {explanation.length > 0 &&
                <div className={`mt-4 text-center text-xs p-2 rounded-lg ${jargonCount > 0 ? 'bg-rose-100 text-rose-700' : 'bg-emerald-100 text-emerald-700'}`}>
                    {jargonCount > 0 ? `Warning: You're using ${jargonCount} jargon word(s). Simplify further!` : 'Great! This is a simple, clear explanation.'}
                </div>
             }
        </div>
    );
};


// --- MODULE COMPONENT ---
const IllusionOfCompetenceModule: React.FC<{ onBack: () => void; progress: ModuleProgress; onProgressUpdate: (progress: ModuleProgress) => void }> = ({ onBack, progress, onProgressUpdate }) => {
  const sections = [
    { id: 'the-deception', title: 'The Great Deception', eyebrow: '01 // The Illusion', icon: Eye },
    { id: 'passive-traps', title: 'The Passive Traps', eyebrow: '02 // The False Comfort', icon: AlertTriangle },
    { id: 'desirable-difficulties', title: 'The Antidote', eyebrow: '03 // Desirable Difficulties', icon: Lightbulb },
    { id: 'strategic-toolkit', title: 'The Strategic Toolkit', eyebrow: '04 // The System', icon: SlidersHorizontal },
    { id: 'feynman-protocol', title: 'The Feynman Protocol', eyebrow: '05 // The Litmus Test', icon: Brain },
    { id: 'anti-fragile', title: 'Building Anti-Fragile Knowledge', eyebrow: '06 // The Action Plan', icon: Wrench },
  ];

  return (
    <ModuleLayout
      moduleNumber="01"
      moduleTitle="Overcoming Illusions of Competence"
      theme={theme}
      sections={sections}
      onBack={onBack}
      progress={progress}
      onProgressUpdate={onProgressUpdate}
    >
      {(activeSection) => (
        <>
          {activeSection === 0 && (
            <ReadingSection title="The Great Deception." eyebrow="Step 1" icon={Eye} theme={theme}>
              <p>The most dangerous thing in your academic life isn't the stuff you know you don't know. It's the stuff you *think* you know, but actually don't. This is the <Highlight description="The cognitive bias where your subjective confidence in your mastery of a topic is significantly higher than your objective ability to retrieve and apply that knowledge." theme={theme}>Illusion of Competence</Highlight>. It's the primary driver of 'grade shock' after the Mocks.</p>
              <p>It's caused by a simple brain shortcut: we mistake the ease of *recognising* information for the ability to *recall* it. Seeing a definition in your notes and thinking "Oh yeah, I know that" feels like learning. But it's a trap. It creates a false sense of security that is brutally exposed under exam conditions when the notes are gone and you have to retrieve the information from a blank page.</p>
            </ReadingSection>
          )}
          {activeSection === 1 && (
            <ReadingSection title="The Passive Traps." eyebrow="Step 2" icon={AlertTriangle} theme={theme}>
              <p>This illusion is created by the most common study methods because they are low-stress and feel effective. The first is the <Highlight description="When you re-read, your brain recognizes the visual pattern of the highlighted text, not the information itself. The cue is the yellow ink, not your internal memory." theme={theme}>Highlighting Trap</Highlight>. The second is the <Highlight description="Following the logic of a solved problem feels like you could have solved it yourself. This is the 'passenger effect' - you practiced verification, not derivation." theme={theme}>'Solved Example' Fallacy</Highlight>. The third is the <Highlight description="When a teacher explains something clearly, you confuse their fluency with your own. You've toured their understanding, not built your own." theme={theme}>Lecture Delusion</Highlight>.</p>
              <p>All these passive methods fail to account for the biological reality of your memory: the <Highlight description="The natural, exponential decay of memory. Without active reinforcement, you lose the majority of new information within 24 hours." theme={theme}>Forgetting Curve</Highlight>. Passive learning feels good, but the knowledge simply evaporates.</p>
              <ForgettingCurveSimulator />
            </ReadingSection>
          )}
          {activeSection === 2 && (
            <ReadingSection title="The Antidote." eyebrow="Step 3" icon={Lightbulb} theme={theme}>
              <p>To dismantle this illusion, we must shift from study methods that feel easy (passive) to ones that feel hard (active). The science of learning is built on the counter-intuitive concept of <Highlight description="Introduced by Robert & Elizabeth Bjork, this is the idea that learning conditions that feel harder and slow down initial performance often lead to far superior long-term retention." theme={theme}>Desirable Difficulties</Highlight>.</p>
              <p>The single most powerful "desirable difficulty" is <Highlight description="The act of retrieving information from memory without cues. This 'testing effect' is a memory modifier; the struggle to recall is the learning process itself." theme={theme}>Active Recall</Highlight>. When you force your brain to retrieve information, you send a powerful signal to strengthen that neural pathway for future use. The struggle is not a sign you are failing; it is the physical sensation of your brain getting stronger.</p>
            </ReadingSection>
          )}
          {activeSection === 3 && (
            <ReadingSection title="The Strategic Toolkit." eyebrow="Step 4" icon={SlidersHorizontal} theme={theme}>
              <p>Active Recall is the engine, but it needs a system to work effectively. The two key partners are <Highlight description="The strategy of spreading out your study sessions over time to interrupt the forgetting curve." theme={theme}>Spaced Repetition</Highlight> and <Highlight description="The strategy of mixing different topics within a study session to train the crucial 'problem spotting' skill." theme={theme}>Interleaving</Highlight>.</p>
              <p>These strategies can be managed with a simple but powerful system: the <Highlight description="A way to plan study by logging what you've done and using a Red/Amber/Green system to rate your confidence, forcing you to always work on your weakest topics first." theme={theme}>Retrospective Revision Timetable</Highlight>. This system forces you to confront your incompetence daily and prioritizes output (mastery) over input (time spent studying).</p>
            </ReadingSection>
          )}
          {activeSection === 4 && (
            <ReadingSection title="The Feynman Protocol." eyebrow="Step 5" icon={Brain} theme={theme}>
              <p>The ultimate litmus test for genuine understanding is the <Highlight description="Named after the Nobel prize-winning physicist Richard Feynman, this technique involves explaining a concept in simple terms, as if to a child, to identify the gaps in your own knowledge." theme={theme}>Feynman Technique</Highlight>. If you can't explain it simply, you don't really know it. The moment you stumble or have to use jargon is the "Illusion Gap"--the precise point where your knowledge is fragile.</p>
              <p>For STEM subjects, a practical application of this is <Highlight description="Practicing exam questions under exam conditions--no notes, no textbook, no marking scheme. This forces you to confront what you can actually retrieve." theme={theme}>'Blind Practice'</Highlight> combined with a <Highlight description="A dedicated notebook where you log every mistake, diagnose why it happened (Slip, Gap, or Misconception), and prescribe a fix." theme={theme}>Mistake Log</Highlight>. This turns vague failure ("I'm bad at Maths") into specific, actionable data ("I keep forgetting the chain rule").</p>
              <FeynmanExplainer />
            </ReadingSection>
          )}
           {activeSection === 5 && (
            <ReadingSection title="Anti-Fragile Knowledge." eyebrow="Step 6" icon={Wrench} theme={theme}>
              <p>The goal is to move from <Highlight description="Knowledge that is context-dependent and breaks under pressure or when a question is phrased differently. It's a product of passive learning." theme={theme}>Fragile Knowledge</Highlight> to <Highlight description="Knowledge that actually gets stronger when challenged with new contexts and problems. It is the product of desirable difficulties." theme={theme}>Anti-Fragile Knowledge</Highlight>. This is the only path to genuine confidence.</p>
              <p>By embracing these effortful strategies, you are not just learning more effectively; you are also managing your wellbeing. The anxiety of the Leaving Cert often stems from the subconscious knowledge that your understanding is fragile. Genuine competence, built through desirable difficulties, is the ultimate antidote to exam stress.</p>
               <MicroCommitment theme={theme}>
                <p>For your very next study session, commit to the "Book Closed" rule. Spend 20 minutes reading, then close the book and spend 10 minutes writing down everything you can remember. This one change will transform your learning.</p>
              </MicroCommitment>
            </ReadingSection>
          )}
        </>
      )}
    </ModuleLayout>
  );
};
export default IllusionOfCompetenceModule;
