
/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
*/

import React, { useState } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import {
  Target, Brain, SlidersHorizontal, AlertTriangle, PenTool, Key, BookOpen, Wrench
} from 'lucide-react';
import { ModuleProgress } from '../types';
import { grayTheme } from '../moduleThemes';
import { Highlight, ReadingSection, MicroCommitment } from './ModuleShared';
import { ModuleLayout } from './ModuleLayout';

const theme = grayTheme;

// --- INTERACTIVE COMPONENTS ---
const PartialCreditCalculator = () => {
    const [steps, setSteps] = useState({ formula: false, sub: false, slip: false, blunder: false });

    let marks = 0;
    if(steps.blunder) marks = 3;
    else if(steps.formula && steps.sub && steps.slip) marks = 8;
    else if(steps.formula && steps.sub) marks = 10;
    else if(steps.formula) marks = 5;

    return (
        <div className="my-10 p-8 md:p-12 bg-white rounded-[3rem] border border-stone-200 shadow-xl">
             <h4 className="font-serif text-2xl font-semibold text-stone-800 text-center italic">Partial Credit Calculator</h4>
             <p className="text-center text-sm text-stone-500 mb-8">Scenario: 10-mark Scale D Question. How many marks do you get?</p>
             <div className="grid grid-cols-2 gap-3">
                <button onClick={() => setSteps(s => ({...s, formula: !s.formula}))} className={`p-4 rounded-xl border-2 ${steps.formula ? 'bg-emerald-50' : ''}`}>Wrote correct formula</button>
                <button onClick={() => setSteps(s => ({...s, sub: !s.sub}))} className={`p-4 rounded-xl border-2 ${steps.sub ? 'bg-emerald-50' : ''}`}>Substituted a value</button>
                <button onClick={() => setSteps(s => ({...s, slip: !s.slip, blunder: false}))} className={`p-4 rounded-xl border-2 ${steps.slip ? 'bg-amber-50' : ''}`}>Made a minor calculation 'Slip'</button>
                <button onClick={() => setSteps(s => ({...s, blunder: !s.blunder, slip: false}))} className={`p-4 rounded-xl border-2 ${steps.blunder ? 'bg-rose-50' : ''}`}>Made a major concept 'Blunder'</button>
             </div>
             <div className="mt-8 p-4 bg-stone-900 rounded-xl text-center text-white">
                You get <span className="font-bold text-2xl text-gray-400">{marks}/10</span> marks.
            </div>
        </div>
    );
};

const ProblemSorter = () => {
    const problems = [
        {id: 1, text: "How many ways can 5 books be arranged?", type: 'p'},
        {id: 2, text: "How many teams of 5 can be picked from 10 players?", type: 'c'}
    ];
    const [choice, setChoice] = useState<{[key: number]: string | null}>({});

    const handleChoice = (id: number, c: string) => {
        setChoice(prev => ({...prev, [id]: c}));
    };

    return(
        <div className="my-10 p-8 md:p-12 bg-white rounded-[3rem] border border-stone-200 shadow-xl">
            <h4 className="font-serif text-2xl font-semibold text-stone-800 text-center italic">Problem Sorter</h4>
            <p className="text-center text-sm text-stone-500 mb-8">Train your discriminative skills: Is it a Permutation (order matters) or a Combination (order doesn't)?</p>
            {problems.map(p => (
                <div key={p.id} className="mb-4">
                    <p className="p-4 bg-stone-100 rounded-lg text-center font-bold">{p.text}</p>
                    <div className="grid grid-cols-2 gap-2 mt-2">
                        <button onClick={() => handleChoice(p.id, 'p')} className={`p-2 rounded-lg border-2 ${choice[p.id] && (choice[p.id] === 'p' && p.type === 'p' ? 'bg-emerald-100 border-emerald-300' : choice[p.id] === 'p' ? 'bg-rose-100 border-rose-300' : 'bg-stone-100 border-stone-200')}`}>Permutation</button>
                        <button onClick={() => handleChoice(p.id, 'c')} className={`p-2 rounded-lg border-2 ${choice[p.id] && (choice[p.id] === 'c' && p.type === 'c' ? 'bg-emerald-100 border-emerald-300' : choice[p.id] === 'c' ? 'bg-rose-100 border-rose-300' : 'bg-stone-100 border-stone-200')}`}>Combination</button>
                    </div>
                </div>
            ))}
        </div>
    );
}

const ErrorLog = () => {
    const [error, setError] = useState('');
    const [type, setType] = useState<string | null>(null);

    return(
         <div className="my-10 p-8 md:p-12 bg-white rounded-[3rem] border border-stone-200 shadow-xl">
             <h4 className="font-serif text-2xl font-semibold text-stone-800 text-center italic">My Error Log</h4>
             <p className="text-center text-sm text-stone-500 mb-8">Log a mistake from a practice question to turn it into a learning opportunity.</p>
             <div className="space-y-4">
                <textarea value={error} onChange={e => setError(e.target.value)} placeholder="Describe the mistake..." className="w-full h-24 p-4 bg-stone-50 border-2 rounded-xl focus:outline-none focus:border-gray-400"></textarea>
                <div className="grid grid-cols-3 gap-2">
                    <button onClick={() => setType('Concept')} className={`p-2 text-xs rounded-lg border-2 ${type === 'Concept' ? 'bg-gray-800 text-white' : 'bg-stone-100'}`}>Concept Error</button>
                    <button onClick={() => setType('Procedural')} className={`p-2 text-xs rounded-lg border-2 ${type === 'Procedural' ? 'bg-gray-800 text-white' : 'bg-stone-100'}`}>Procedural Error</button>
                    <button onClick={() => setType('Reading')} className={`p-2 text-xs rounded-lg border-2 ${type === 'Reading' ? 'bg-gray-800 text-white' : 'bg-stone-100'}`}>Reading Error</button>
                </div>
             </div>
             {error && type && <p className="text-center mt-4 text-sm font-bold text-emerald-600">Error logged. Now you won't make it again.</p>}
        </div>
    );
};

// --- MODULE COMPONENT ---
const LearningMathModule: React.FC<{ onBack: () => void; progress: ModuleProgress; onProgressUpdate: (progress: ModuleProgress) => void }> = ({ onBack, progress, onProgressUpdate }) => {
  const sections = [
    { id: 'new-game', title: 'The New Game', eyebrow: '01 // Project Maths', icon: Target },
    { id: 'two-papers', title: 'The Two Papers', eyebrow: '02 // Technical vs. Contextual', icon: BookOpen },
    { id: 'deep-dive', title: 'The Five Strands', eyebrow: '03 // Curriculum Deep Dive', icon: SlidersHorizontal },
    { id: 'marking-scheme', title: 'Decoding the Scheme', eyebrow: '04 // Positive Marking', icon: Key },
    { id: 'attempt-mark', title: 'The "Attempt Mark" Goldmine', eyebrow: '05 // Partial Credit', icon: Wrench },
    { id: 'spotting-trends', title: 'Spotting the Trends', eyebrow: '06 // Gremlins & Hybrids', icon: Brain },
    { id: 'examiners-mind', title: 'The Examiner\'s Mind', eyebrow: '07 // Common Errors', icon: AlertTriangle },
    { id: 'cognitive-toolkit', title: 'The Cognitive Toolkit', eyebrow: '08 // Learning Science for Maths', icon: Brain },
    { id: 'h1-pathway', title: 'The H1 Pathway', eyebrow: '09 // Bankable Marks', icon: PenTool },
  ];

  return (
    <ModuleLayout
      moduleNumber="01"
      moduleTitle="The Maths Protocol"
      theme={theme}
      sections={sections}
      onBack={onBack}
      progress={progress}
      onProgressUpdate={onProgressUpdate}
    >
      {(activeSection) => (
        <>
          {activeSection === 0 && (
            <ReadingSection title="The New Game." eyebrow="Step 1" icon={Target} theme={theme}>
              <p>Leaving Cert Maths is not the same game it used to be. The "Project Maths" initiative fundamentally changed the rules, shifting the focus from rote memorization of algorithms to genuine <Highlight description="The ability to understand the 'why' behind a mathematical rule, not just the 'how'." theme={theme}>conceptual understanding</Highlight> and problem-solving. It's a test of resilience, not just numeracy.</p>
              <p>The introduction of the <Highlight description="The 25 extra CAO points awarded for a H6 or higher, making Maths the single most valuable subject in the points race." theme={theme}>Bonus Points</Highlight> has also changed the strategic landscape. A H6 in Maths is worth more than a H3 in any other subject. This "safety net" encourages students to aim high, but requires a deep, strategic approach to the exam.</p>
            </ReadingSection>
          )}
           {activeSection === 1 && (
            <ReadingSection title="The Two Papers." eyebrow="Step 2" icon={BookOpen} theme={theme}>
              <p>The exam is split into two papers designed to test different cognitive skills. **Paper 1** is the **"Technical"** paper. It's heavily weighted towards Algebra, Calculus, and Number. It rewards <Highlight description="The ability to perform mathematical operations (like solving equations or differentiating) quickly and accurately." theme={theme}>procedural fluency</Highlight> and is less "wordy."</p>
              <p>**Paper 2** is the **"Contextual"** paper. This is the test of interpretation and spatial reasoning, covering Statistics, Probability, Geometry, and Trigonometry. It's often described as "volatile" because a single novel diagram can throw off students who rely on memorized procedures rather than a deep understanding of the concepts.</p>
            </ReadingSection>
          )}
          {activeSection === 2 && (
            <ReadingSection title="The Five Strands." eyebrow="Step 3" icon={SlidersHorizontal} theme={theme}>
              <p>The syllabus is divided into five interconnected strands. Questions are deliberately <Highlight description="Requiring students to combine knowledge from multiple strands (e.g., using Algebra to solve a Geometry problem)." theme={theme}>synoptic</Highlight>, so you can't study topics in isolation.</p>
              <p>The strands are: 1) **Statistics & Probability** (literacy-heavy), 2) **Geometry & Trigonometry** (visual and spatial), 3) **Number** (the foundation, including Complex Numbers), 4) **Algebra** (the "language" of the course), and 5) **Functions & Calculus** (the heavyweight of Paper 1).</p>
            </ReadingSection>
          )}
          {activeSection === 3 && (
            <ReadingSection title="Decoding the Marking Scheme." eyebrow="Step 4" icon={Key} theme={theme}>
              <p>Understanding how marks are awarded is your single greatest strategic asset. The SEC uses a <Highlight description="An ethos where marks are awarded for what is correct, not deducted for what is wrong. The goal is to reward any valid progress." theme={theme}>"Positive Marking"</Highlight> system. This is codified in the Scale System (A, B, C, D).</p>
              <p>**Scale A** (0, 10) is rare. **Scale B** (0, 5, 10) is "hit or miss." But **Scale C** (0, 3, 7, 10) and **Scale D** (0, 3, 5, 8, 10) are the most common. The crucial insight is the "Low Partial" mark—you can get 30% of the marks for simply writing down the correct formula and attempting to substitute a value. This is a strategic goldmine.</p>
            </ReadingSection>
          )}
          {activeSection === 4 && (
            <ReadingSection title="The 'Attempt Mark' Goldmine." eyebrow="Step 5" icon={Wrench} theme={theme}>
              <p>The "Low Partial Credit" is your safety net. If you encounter a 10-mark question that seems impossible, simply writing down the relevant formula from the log tables and substituting one correct value often secures 3 marks. Leaving a question blank is a strategic failure of the highest order.</p>
              <p>Accumulating these "scrap" marks across an entire paper can be the difference between a H4 and a H3. The goal is to *never get a zero*. Even on the hardest "gremlin" question, there are marks available for defining terms, writing a relevant formula, or drawing a diagram. You must train yourself to hunt for these partial marks.</p>
              <PartialCreditCalculator />
            </ReadingSection>
          )}
          {activeSection === 5 && (
            <ReadingSection title="Spotting the Trends." eyebrow="Step 6" icon={Brain} theme={theme}>
              <p>Analysis of past papers reveals clear trends. Paper 1 is seeing the rise of applied Calculus (rates of change) and Complex Numbers treated as geometry. Paper 2 is increasingly defined by its <Highlight description="Novel questions with unfamiliar diagrams or scenarios that test a student's ability to apply core principles to new situations." theme={theme}>"Gremlin" questions</Highlight> and <Highlight description="Questions that fuse topics from different strands, such as calculating the probability that a point lies within a certain geometric region." theme={theme}>Probability-Geometry hybrids</Highlight>. These questions are designed to defeat rote learning and reward flexible, conceptual understanding.</p>
            </ReadingSection>
          )}
          {activeSection === 6 && (
            <ReadingSection title="The Examiner's Mind." eyebrow="Step 7" icon={AlertTriangle} theme={theme}>
              <p>The Chief Examiner's Reports highlight the most common student errors. The biggest is <Highlight description="The tendency for students to understand a concept but fail in the algebraic execution (e.g., mishandling signs, index errors)." theme={theme}>"Algebraic Fragility."</Highlight> The second is the <Highlight description="The failure to check answers for reasonableness (e.g., calculating a probability greater than 1, or a negative distance)." theme={theme}>"Check" Deficit</Highlight>. The third is the <Highlight description="The struggle to translate a 'real-world' story problem into a mathematical model, often due to over-reliance on blocked practice." theme={theme}>"Unfamiliar Context" Block</Highlight>.</p>
              <p>A major pitfall is "forcing" an answer in "Show That" questions. It is strategically better to write, "I cannot derive the final step, but assuming x=5, I will proceed..." This allows you to gain partial credit on subsequent parts.</p>
              <ProblemSorter />
            </ReadingSection>
          )}
          {activeSection === 7 && (
            <ReadingSection title="The Cognitive Toolkit." eyebrow="Step 8" icon={Brain} theme={theme}>
              <p>To overcome these challenges, you must adopt strategies from cognitive science. <Highlight description="Studying one topic intensely (e.g., Algebra all week). It creates a false sense of mastery." theme={theme}>Blocking</Highlight> fails to train strategy selection. <Highlight description="Mixing up topics within a study session (e.g., one Algebra, one Geometry, one Probability). It feels harder but builds flexible, exam-ready knowledge." theme={theme}>Interleaving</Highlight> is crucial for Maths as it mimics the exam environment.</p>
              <p>Passive reading of notes is ineffective. <Highlight description="Closing the book and attempting to write out a proof or definition from memory. This strengthens the neural pathways." theme={theme}>Active Recall</Highlight> is essential. Finally, you must maintain an <Highlight description="A log where you categorize your mistakes (Concept, Procedural, Reading) to prevent repetition and target revision." theme={theme}>Error Log</Highlight>. The most valuable part of a past paper is the "post-mortem."</p>
              <ErrorLog />
            </ReadingSection>
          )}
          {activeSection === 8 && (
            <ReadingSection title="The H1 Pathway." eyebrow="Step 9" icon={PenTool} theme={theme}>
              <p>For students aiming for the top grade, the strategy goes beyond competence. It requires speed and tactical awareness. H1 students distinguish themselves by their fluency, completing routine Section A questions faster to "bank" time for the harder Section B questions.</p>
              <p>The final layer of strategy is to identify and master the few things in Maths that *can* be rote-learned. These are your <Highlight description="The small number of examinable proofs (e.g., Induction, irrationality of root 2) and definitions (e.g., 'injective function'). These should be learned perfectly as they are 'free marks' when they appear." theme={theme}>"Bankable Marks."</Highlight> A small number of formal proofs and definitions are examinable. These should be learned perfectly and are 'free marks' if they appear on the day.</p>
              <MicroCommitment theme={theme}><p>Go to your log tables. Pick one proof (e.g., Cos(A+B)). Spend 15 minutes learning it using active recall. You've just 'banked' a potential 10 marks.</p></MicroCommitment>
            </ReadingSection>
          )}
        </>
      )}
    </ModuleLayout>
  );
};
export default LearningMathModule;
