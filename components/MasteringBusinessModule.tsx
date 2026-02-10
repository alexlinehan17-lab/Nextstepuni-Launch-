/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
*/

import React, { useState } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import {
  Key, PieChart, Briefcase, FileText, BrainCircuit, Wrench
} from 'lucide-react';
import { ModuleProgress } from '../types';
import { grayTheme } from '../moduleThemes';
import { Highlight, ReadingSection, MicroCommitment } from './ModuleShared';
import { ModuleLayout } from './ModuleLayout';

const theme = grayTheme;

// --- INTERACTIVE COMPONENTS ---
const ABQLinkDrill = () => {
    const [step, setStep] = useState(0);
    const steps = [
        "STATE: Democratic Leadership",
        "EXPLAIN: This is a style where the manager involves employees in decision-making but retains the final say.",
        "LINK: In the text, 'Mary holds weekly meetings to get staff feedback on new menu ideas...'"
    ];
    return(
        <div className="my-10 p-8 md:p-12 bg-white dark:bg-zinc-800 rounded-xl border border-zinc-200 dark:border-zinc-700">
             <h4 className="font-serif text-2xl font-semibold text-zinc-800 dark:text-white text-center">ABQ "Link" Methodology Drill</h4>
             <AnimatePresence mode="wait">
                <motion.div key={step} initial={{opacity:0, y:10}} animate={{opacity:1, y:0}} exit={{opacity:0, y:-10}} className="mt-6 p-6 bg-zinc-100 dark:bg-zinc-800 rounded-xl min-h-[80px] flex items-center justify-center">
                    <p className="font-mono text-center text-sm">{steps[step]}</p>
                </motion.div>
             </AnimatePresence>
             <div className="flex justify-center mt-6"><button onClick={() => setStep(s => (s + 1) % steps.length)} className="px-4 py-2 bg-zinc-800 text-white text-xs font-bold rounded-lg">Next Step</button></div>
        </div>
    );
};

// --- MODULE COMPONENT ---
const MasteringBusinessModule: React.FC<{ onBack: () => void; progress: ModuleProgress; onProgressUpdate: (progress: ModuleProgress) => void }> = ({ onBack, progress, onProgressUpdate }) => {
  const sections = [
    { id: 'strategic-context', title: 'The Strategic Context for 2026', eyebrow: '01 // The Master Key', icon: Key },
    { id: 'exam-architecture', title: 'The Exam Architecture', eyebrow: '02 // The Blueprint', icon: PieChart },
    { id: 'abq-deep-dive', title: 'ABQ Deep Dive', eyebrow: '03 // The Pivot', icon: Briefcase },
    { id: 'science-of-scoring', title: 'The Science of Scoring', eyebrow: '04 // Grade Engineering', icon: FileText },
    { id: 'high-yield-tactics', title: 'High-Yield Tactics', eyebrow: '05 // The Toolkit', icon: Wrench },
    { id: 'study-blueprint', title: 'The Study Blueprint', eyebrow: '06 // The Action Plan', icon: BrainCircuit },
  ];

  return (
    <ModuleLayout
      moduleNumber="05"
      moduleTitle="Mastering Business"
      theme={theme}
      sections={sections}
      onBack={onBack}
      progress={progress}
      onProgressUpdate={onProgressUpdate}
    >
      {(activeSection) => (
        <>
          {activeSection === 0 && (
            <ReadingSection title="The Strategic Context for 2026." eyebrow="Step 1" icon={Key} theme={theme}>
              <p>The Leaving Cert Business exam isn't a test of memory; it's a test of <Highlight description="The ability to decode the specific rules and expectations of the exam, from timing to the precise meaning of 'outcome verbs'." theme={theme}>examination literacy</Highlight>. For 2026, the game is defined by one critical fact: the compulsory Applied Business Question (ABQ) will be based on **Units 3, 4, and 5**.</p>
              <p>This is your strategic roadmap. It shifts the focus from the wider economy to the "engine room" of a business: management, HR, finance, and marketing. A weakness in these units cannot be hidden, making the ABQ the primary filter for H1 candidates.</p>
            </ReadingSection>
          )}
           {activeSection === 1 && (
            <ReadingSection title="The Exam Architecture." eyebrow="Step 2" icon={PieChart} theme={theme}>
              <p>The 3-hour Higher Level paper is an endurance test split into three sections. **Section 1 (Shorts)** is your "return on investment" section, worth 20% of the marks for about 15% of the time. **Section 2 (ABQ)** is your high-risk, high-reward section, also worth 20%. **Section 3 (Longs)** is the marathon, worth 60% of the marks and requiring four full answers.</p>
              <p>Your timing strategy is critical. A common H1 approach is to tackle the ABQ immediately after the Shorts to leverage mental freshness before the fatigue of the long questions sets in.</p>
            </ReadingSection>
          )}
           {activeSection === 2 && (
            <ReadingSection title="ABQ Deep Dive." eyebrow="Step 3" icon={Briefcase} theme={theme}>
                <p>The 2026 ABQ will almost certainly feature a business in a "growth crisis"--a company that has launched successfully but is struggling with internal chaos. You will act as a consultant. Your job is to apply theory to solve their problems.</p>
                <p>The golden rule is the <Highlight description="The non-negotiable, 3-part structure for ABQ answers: State the theory, Explain it in your own words, and Link it with a direct quote from the text." theme={theme}>"Link" Methodology</Highlight>. Failure to quote directly from the case study is the single biggest cause of lost marks. It's a mechanical process: State, Explain, Link. Master this algorithm.</p>
                <ABQLinkDrill />
            </ReadingSection>
          )}
           {activeSection === 3 && (
            <ReadingSection title="The Science of Scoring." eyebrow="Step 4" icon={FileText} theme={theme}>
              <p>To get a H1, you must write for the examiner. The marking scheme is a rigid code. The standard unit of currency is the "point," worth 5 marks in a long question. To secure these marks, you must use a structured formula: <Highlight description="The standard formula for a 5-mark point: State the point, Explain it, and give an Example." theme={theme}>"SEE"</Highlight>. For a H1, you need the advanced <Highlight description="The H1 version of the formula, expanding the 'Explain' part into two distinct sentences to ensure full marks are captured." theme={theme}>"SEEE"</Highlight> version.</p>
              <p>You must also decode the <Highlight description="The specific verb used by the SEC in a question (e.g., State, Explain, Evaluate) which dictates the required depth and structure of your answer." theme={theme}>"Outcome Verb."</Highlight> "State" requires a list. "Explain" requires a definition. "Evaluate" requires a judgment, which is the key differentiator for top grades. Always add a separate mini-paragraph explicitly labelled **"Evaluation:"** to secure these marks.</p>
            </ReadingSection>
          )}
          {activeSection === 4 && (
            <ReadingSection title="High-Yield Tactics." eyebrow="Step 5" icon={Wrench} theme={theme}>
              <p>In Section 1 (Short Questions), use the <Highlight description="The strategy of answering all available short questions (e.g., 10 or 12) to create a safety net, as only your best 8 will be counted." theme={theme}>"Surplus" Strategy</Highlight>: answer all the questions. It takes little extra time and insures you against a calculation error.</p>
              <p>In Section 3 (Long Questions), avoid the <Highlight description="The phenomenon of writing lengthy paragraphs without any specific keywords or facts, which scores zero marks." theme={theme}>"Waffle" Phenomenon</Highlight> by using the SEEE structure. Every sentence must have a purpose. Also, avoid the <Highlight description="Making the same point twice using different words. Examiners will only award marks for it once." theme={theme}>"Repetition" Trap</Highlight> when asked for multiple "impacts" or "benefits"--make sure your points are distinct (e.g., one financial, one marketing).</p>
            </ReadingSection>
          )}
           {activeSection === 5 && (
            <ReadingSection title="The Study Blueprint." eyebrow="Step 6" icon={BrainCircuit} theme={theme}>
              <p>Success is a marathon, not a sprint. Passive reading yields only 10% retention. <Highlight description="Actively testing yourself by retrieving information from memory. This is the most effective study method, yielding up to 60% retention." theme={theme}>Active Recall</Highlight> is the engine of learning. Use spider diagrams and flashcards to test yourself, not just to make notes.</p>
              <p>Your study plan should be phased. **Phase 1 (Sept-Dec):** Deep dive on the ABQ units (3, 4, 5). **Phase 2 (Jan-Mar):** Cover the other units and begin timed long questions. **Phase 3 (Apr-May):** Use <Highlight description="Mixing questions from different units in a single study session to simulate the randomness of the exam and train your problem-spotting skills." theme={theme}>"Interleaved" Practice</Highlight> with past papers. This is not about just learning the material; it's about learning how to perform.</p>
               <MicroCommitment theme={theme}>
                <p>Go to your Business notes. Pick one topic. Create a one-page "spider diagram" summary of it *from memory*. Then, open the book and check what you missed. You've just started using active recall.</p>
              </MicroCommitment>
            </ReadingSection>
          )}
        </>
      )}
    </ModuleLayout>
  );
};
export default MasteringBusinessModule;
