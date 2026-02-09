/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
*/

import React, { useState } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { Key, FlaskConical, BookOpen, Languages, Feather, Award, CheckCircle2 } from 'lucide-react';
import { ModuleProgress } from '../types';
import { redTheme } from '../moduleThemes';
import { Highlight, ReadingSection, MicroCommitment } from './ModuleShared';
import { ModuleLayout } from './ModuleLayout';

const theme = redTheme;

// --- INTERACTIVE COMPONENTS ---
const PartialCreditCalculator = () => {
    const [steps, setSteps] = useState({ formula: false, substitution: false, slip: false, blunder: false });

    let marks = 0;
    let grade = "Zero Credit";
    if (steps.formula && !steps.blunder) { marks = 3; grade = "Low Partial"; }
    if (steps.formula && steps.substitution && !steps.blunder) { marks = 5; grade = "Mid Partial"; }
    if (steps.formula && steps.substitution && !steps.blunder && !steps.slip) { marks = 10; grade = "Full Credit"; }
    if (steps.formula && steps.substitution && !steps.blunder && steps.slip) { marks = 8; grade = "High Partial"; }
    if(steps.blunder) {marks = 3; grade="Low Partial (Blunder)"}

    return(
        <div className="my-10 p-8 md:p-12 bg-white dark:bg-zinc-800 rounded-2xl border border-zinc-200 dark:border-zinc-700 shadow-xl">
            <h4 className="font-serif text-2xl font-semibold text-zinc-800 dark:text-white text-center italic">Partial Credit Calculator</h4>
            <p className="text-center text-sm text-zinc-500 dark:text-zinc-400 mb-8">Scenario: A 10-mark D-Scale question. Check the steps you complete.</p>
            <div className="grid grid-cols-2 gap-4">
                <button onClick={() => setSteps({...steps, formula: !steps.formula})} className={`p-4 rounded-xl border-2 ${steps.formula ? 'bg-emerald-100' : ''}`}>Wrote correct formula</button>
                <button onClick={() => setSteps({...steps, substitution: !steps.substitution})} className={`p-4 rounded-xl border-2 ${steps.substitution ? 'bg-emerald-100' : ''}`}>Attempted substitution</button>
                <button onClick={() => setSteps({...steps, slip: !steps.slip, blunder: false})} className={`p-4 rounded-xl border-2 ${steps.slip ? 'bg-amber-100' : ''}`}>Made a minor 'Slip'</button>
                <button onClick={() => setSteps({...steps, blunder: !steps.blunder, slip: false})} className={`p-4 rounded-xl border-2 ${steps.blunder ? 'bg-rose-100' : ''}`}>Made a major 'Blunder'</button>
            </div>
            <div className="mt-8 p-4 bg-zinc-900 rounded-xl text-center text-white">
                You get <span className="font-bold text-2xl text-red-400">{marks}/10</span> ({grade})
            </div>
        </div>
    );
}

const OralPivotSimulator = () => {
    const [response, setResponse] = useState<null|'short'|'pivot'>(null);
    return(
         <div className="my-10 p-8 md:p-12 bg-white dark:bg-zinc-800 rounded-2xl border border-zinc-200 dark:border-zinc-700 shadow-xl">
            <h4 className="font-serif text-2xl font-semibold text-zinc-800 dark:text-white text-center italic">Oral Exam Pivot Simulator</h4>
            <p className="text-center font-bold text-zinc-700 dark:text-zinc-200 mb-2">Examiner: "How was your weekend?"</p>
            <div className="grid grid-cols-2 gap-4">
                <button onClick={() => setResponse('short')} className="p-4 bg-zinc-100 dark:bg-zinc-800 rounded-xl"><strong>A:</strong> "It was grand, I went to the cinema."</button>
                <button onClick={() => setResponse('pivot')} className="p-4 bg-zinc-100 dark:bg-zinc-800 rounded-xl"><strong>B:</strong> "It was stressful, I was studying. To relax, I play Gaelic Football."</button>
            </div>
            {response && <motion.p initial={{opacity:0}} animate={{opacity:1}} className={`mt-4 p-4 rounded-xl text-sm font-bold text-center ${response==='pivot' ? 'bg-emerald-100 text-emerald-800' : 'bg-rose-100 text-rose-800'}`}>
                {response === 'short' ? "FAIL: You've given control back to the examiner. Next question is random." : "SUCCESS! You've pivoted to a prepared topic. The examiner will now ask about sport."}
            </motion.p>}
        </div>
    );
}

// --- MODULE COMPONENT ---
const SubjectSpecificAdviceModule: React.FC<{ onBack: () => void; progress: ModuleProgress; onProgressUpdate: (progress: ModuleProgress) => void }> = ({ onBack, progress, onProgressUpdate }) => {
  const sections = [
    { id: 'strategic-compliance', title: 'Strategic Compliance', eyebrow: '01 // The Master Key', icon: Key },
    { id: 'stem-protocols', title: 'The STEM Protocols', eyebrow: '02 // Maths & Science', icon: FlaskConical },
    { id: 'humanities-protocols', title: 'The Humanities Engine', eyebrow: '03 // History & Geography', icon: BookOpen },
    { id: 'languages-protocols', title: 'Linguistic Engineering', eyebrow: '04 // Irish & Languages', icon: Languages },
    { id: 'english-protocol', title: 'The PCLM Protocol', eyebrow: '05 // English P1 & P2', icon: Feather },
    { id: 'grade-engineering', title: 'The Grade Engineering Mindset', eyebrow: '06 // The Final Mindset', icon: Award },
  ];

  return (
    <ModuleLayout
      moduleNumber="05"
      moduleTitle="Subject Specific Advice"
      theme={theme}
      sections={sections}
      onBack={onBack}
      progress={progress}
      onProgressUpdate={onProgressUpdate}
    >
      {(activeSection) => (
        <>
          {activeSection === 0 && (
            <ReadingSection title="Strategic Compliance." eyebrow="Step 1" icon={Key} theme={theme}>
              <p>The Leaving Cert is not a test of intelligence. It is a standardized, bureaucratic process governed by rigid algorithms. High performance isn't just about knowing your subject; it's about <Highlight description="The ability to align your answer with the specific, often non-intuitive, criteria of the marking scheme." theme={theme}>Strategic Compliance</Highlight>. The gap between a H3 and a H1 is often not a gap in understanding, but in formatting.</p>
              <p>This module is the decryption key. By deconstructing the assessment architecture of each subject, we can identify the specific "method marks" and structural requirements that allow you to engineer your grades. The Leaving Cert is a coded system; the marking schemes are the key.</p>
            </ReadingSection>
          )}
           {activeSection === 1 && (
            <ReadingSection title="The STEM Protocols." eyebrow="Step 2" icon={FlaskConical} theme={theme}>
              <p>In STEM subjects, the final answer is only a small part of the story. The vast majority of marks are for the process. For Maths, this means exploiting the <Highlight description="A system that rewards any valid attempt or correct step, even if the final answer is wrong." theme={theme}>"attempt mark" philosophy</Highlight>. You can get 70-90% of the marks for a question with a completely incorrect final answer. Never leave a blank space.</p>
              <p>For Biology, it's about <Highlight description="The use of precise, non-negotiable keywords that trigger marks. Synonyms are often rejected." theme={theme}>Terminological Exactitude</Highlight>. 'Osmosis' gets marks; 'water moving' does not. Also, beware the <Highlight description="The policy in Biology where an incorrect item in a list can cancel out a correct one. Provide only the number of points requested." theme={theme}>'Surplus' Danger</Highlight>. In Physics and Chemistry, the <Highlight description="The predictable 3-3-3-3 structure for calculation questions: Formula, Substitution, Manipulation, Calculation." theme={theme}>'3-3-3-3 System'</Highlight> means you bank marks for setup before you ever touch your calculator.</p>
              <PartialCreditCalculator />
            </ReadingSection>
          )}
           {activeSection === 2 && (
            <ReadingSection title="The Humanities Engine." eyebrow="Step 3" icon={BookOpen} theme={theme}>
              <p>In Humanities, the game shifts from "right answer" to "coherent argument." For Geography, this is a mechanical process of accumulating <Highlight description="A Significant Relevant Point is a single piece of factual information, worth 2 marks. A 30-mark essay requires 15 SRPs." theme={theme}>SRPs</Highlight>. An essay is just a container for these points.</p>
              <p>History uses a dual-layered matrix: the <Highlight description="Cumulative Mark (max 60): Measures the density of historical facts (dates, names, stats)." theme={theme}>CM</Highlight> for facts and the <Highlight description="Overall Evaluation (max 40): Measures the quality of your argument, historical language, and coherence." theme={theme}>OE</Highlight> for argument. A common trap is to get high CM but low OE by telling a story instead of making an argument. Use the <Highlight description="A sentence at the end of each paragraph that explicitly links the facts back to the question, signaling 'Argumentation' to the examiner." theme={theme}>'Link-Back' Tactic</Highlight> to boost your OE.</p>
            </ReadingSection>
          )}
          {activeSection === 3 && (
            <ReadingSection title="Linguistic Engineering." eyebrow="Step 4" icon={Languages} theme={theme}>
              <p>In languages, the goal is "Communicative Competence," not poetic genius. It's about manipulating the language you know to fit the question. The Oral exam is your chance to take control. Examiners are trained to follow your lead. Use the <Highlight description="Answering a question and adding a 'hook' to steer the conversation towards a topic you have prepared (e.g., 'To relax, I play Gaelic Football...')." theme={theme}>'Pivot' Technique</Highlight> to move from a random question to a prepared script.</p>
              <p>For written exams, use <Highlight description="Grammatically complex, thematically neutral sentences that can be inserted into any essay to demonstrate linguistic flair and boost the 'Language' mark." theme={theme}>'Skeleton Key' Phrases</Highlight>. For French, this means using the Subjunctive. For Spanish, it's idiomatic expressions. For German, it's mastering word order like inversion. These are high-yield investments for your language grade.</p>
              <OralPivotSimulator/>
            </ReadingSection>
          )}
          {activeSection === 4 && (
            <ReadingSection title="The PCLM Protocol." eyebrow="Step 5" icon={Feather} theme={theme}>
              <p>English is not subjective. It is marked using a rigid, standardized rubric: the <Highlight description="The four criteria for marking English: Purpose (30%), Coherence (30%), Language (30%), and Mechanics (10%)." theme={theme}>PCLM</Highlight> criteria. Your grade is a direct result of how you score on these four metrics.</p>
              <p><Highlight description="Did you answer the specific question asked? This is the most important criterion." theme={theme}>Purpose</Highlight> and <Highlight description="Is your argument logical and well-structured?" theme={theme}>Coherence</Highlight> are worth 60% of the marks. For the Comparative, avoid the "linear" trap (Text A, then B, then C) and use the <Highlight description="The technique of structuring comparative paragraphs by theme, weaving links and contrasts between all three texts throughout." theme={theme}>'Weave' Method</Highlight> to maximize your Coherence score. For Paper 1, your <Highlight description="Language (30%): Demonstrates originality of expression, lexical range, and syntactic control." theme={theme}>Language</Highlight> mark is about flair and vocabulary. For Paper 2, it's about using literary terminology correctly.</p>
              <MicroCommitment theme={theme}>
                <p>Take out your last English essay. Go through it with a red pen and score yourself on each of the four PCLM criteria out of 10. Identify which area is your weakest, and focus your next essay practice on improving that specific metric.</p>
              </MicroCommitment>
            </ReadingSection>
          )}
          {activeSection === 5 && (
            <ReadingSection title="The Grade Engineering Mindset." eyebrow="Step 6" icon={Award} theme={theme}>
              <p>The final mindset shift is this: you are not a student sitting an exam. You are an <Highlight description="Treating your grade as an output that can be reverse-engineered by understanding and exploiting the inputs (marking scheme rules)." theme={theme}>engineer of your grade</Highlight>. Every subject has a code. The marking scheme is the decryption key. Your job is not to "know everything" but to strategically allocate your effort to the areas with the highest mark-to-effort ratio.</p>
              <p>This means making hard choices. Some topics are worth more marks per hour of study than others. Some question types are more predictable. Some subjects have more "free marks" in their structure. The student who understands this system will always outperform the student who simply studies harder without direction.</p>
              <MicroCommitment theme={theme}>
                <p>Pick your three highest-priority subjects. For each one, download the most recent marking scheme from examinations.ie and spend 15 minutes reading it. Not to study the content, but to study the system. Note down any patterns, keywords, or structural requirements you find.</p>
              </MicroCommitment>
            </ReadingSection>
          )}
        </>
      )}
    </ModuleLayout>
  );
};
export default SubjectSpecificAdviceModule;
