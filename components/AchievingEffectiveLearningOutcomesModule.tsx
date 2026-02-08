
/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
*/

import React, { useState } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import {
  Eye, BarChart3, BrainCircuit, Timer, HeartPulse, ClipboardCheck
} from 'lucide-react';
import { ModuleProgress } from '../types';
import { tealTheme } from '../moduleThemes';
import { Highlight, ReadingSection, MicroCommitment } from './ModuleShared';
import { ModuleLayout } from './ModuleLayout';

const theme = tealTheme;

// --- INTERACTIVE COMPONENTS ---
const IllusionOfCompetenceChart = () => {
    const [view, setView] = useState<'prediction' | 'reality'>('prediction');
    const ssssData = { prediction: 90, reality: 40 };
    const stttData = { prediction: 40, reality: 61 };

    return (
        <div className="my-10 p-8 md:p-12 bg-white rounded-[3rem] border border-stone-200 shadow-xl">
            <h4 className="font-serif text-2xl font-semibold text-stone-800 text-center italic">The Great Deception</h4>
            <p className="text-center text-sm text-stone-500 mb-8">Data from Roediger & Karpicke (2006) reveals the gap between what *feels* effective and what *is* effective.</p>
            <div className="grid grid-cols-2 gap-4 mb-8">
                <div className="text-center">
                    <h5 className="font-bold mb-2">Passive Rereading (SSSS)</h5>
                    <div className="h-48 w-full bg-stone-100 rounded-lg flex items-end">
                        <motion.div className="w-full bg-teal-400 rounded-t-lg" initial={{height:0}} animate={{height: `${view === 'prediction' ? ssssData.prediction : ssssData.reality}%`}} transition={{type: 'spring', stiffness: 100}}/>
                    </div>
                </div>
                <div className="text-center">
                     <h5 className="font-bold mb-2">Active Recall (STTT)</h5>
                     <div className="h-48 w-full bg-stone-100 rounded-lg flex items-end">
                        <motion.div className="w-full bg-indigo-400 rounded-t-lg" initial={{height:0}} animate={{height: `${view === 'prediction' ? stttData.prediction : stttData.reality}%`}} transition={{type: 'spring', stiffness: 100}}/>
                    </div>
                </div>
            </div>
            <div className="flex justify-center gap-2 p-1 bg-stone-100 rounded-full">
                <button onClick={() => setView('prediction')} className={`px-4 py-2 text-xs font-bold rounded-full ${view === 'prediction' ? 'bg-white shadow' : ''}`}>Student Prediction (JOL)</button>
                <button onClick={() => setView('reality')} className={`px-4 py-2 text-xs font-bold rounded-full ${view === 'reality' ? 'bg-white shadow' : ''}`}>Actual Test Results (1 Week Later)</button>
            </div>
        </div>
    );
};


// --- MODULE COMPONENT ---
const AchievingEffectiveLearningOutcomesModule: React.FC<{ onBack: () => void; progress: ModuleProgress; onProgressUpdate: (progress: ModuleProgress) => void }> = ({ onBack, progress, onProgressUpdate }) => {
  const sections = [
    { id: 'illusion-of-competence', title: 'The Illusion of Competence', eyebrow: '01 // The Paradox', icon: Eye },
    { id: 'hard-data', title: 'The Hard Data', eyebrow: '02 // The Crossover Effect', icon: BarChart3 },
    { id: 'active-retrieval', title: 'Active Retrieval', eyebrow: '03 // The Gold Standard', icon: BrainCircuit },
    { id: 'distributed-practice', title: 'Distributed Practice', eyebrow: '04 // The Forgetting Curve', icon: Timer },
    { id: 'anxiety-paradox', title: 'The Anxiety Paradox', eyebrow: '05 // The Stress Test', icon: HeartPulse },
    { id: 'action-plan', title: 'Your Action Plan', eyebrow: '06 // The Audit', icon: ClipboardCheck },
  ];

  return (
    <ModuleLayout moduleNumber="01" moduleTitle="Effective Learning Outcomes" theme={theme} sections={sections} onBack={onBack} progress={progress} onProgressUpdate={onProgressUpdate}>
      {(activeSection) => (
        <>
          {activeSection === 0 && (
            <ReadingSection title="The Illusion of Competence." eyebrow="Step 1" icon={Eye} theme={theme}>
              <p>There's a huge paradox in how we learn: the study methods that feel the most productive are often the least effective. We gravitate towards passive strategies like re-reading textbooks, highlighting notes, and watching lectures because they feel comfortable and easy. The material becomes familiar, and we mistake this feeling of familiarity for mastery.</p>
              <p>This is the <Highlight description="A metacognitive failure where you misinterpret the ease of processing information (fluency) as a sign of durable learning. It's the primary reason students choose ineffective study strategies." theme={theme}>Illusion of Competence</Highlight>. It's caused by a cognitive shortcut called <Highlight description="A mental heuristic where the brain uses the ease ('fluency') of processing as a proxy for value. If something is easy to read or recall, we assume it's well-learned or true." theme={theme}>Fluency Bias</Highlight>. Your brain is an energy-conserving organ; it loves the path of least resistance. The problem is, when it comes to learning, that path leads off a cliff.</p>
            </ReadingSection>
          )}
          {activeSection === 1 && (
            <ReadingSection title="The Hard Data." eyebrow="Step 2" icon={BarChart3} theme={theme}>
              <p>This isn't just a theory; it's a measurable disaster. A landmark study by Roediger & Karpicke (2006) proved it. They had students study a text using two methods: one group just re-read it (passive review), and the other group read it once and then tried to recall everything they could (active retrieval).</p>
              <p>The results are devastating for our intuition. The students who simply re-read the text were far more confident in their learning. But on the actual test a week later, they performed terribly, forgetting over half of what they'd studied. The students who used active recall were less confident, but they retained significantly more information. The strategy that *felt* worse was dramatically more effective. You can see the shocking data for yourself.</p>
              <IllusionOfCompetenceChart />
            </ReadingSection>
          )}
          {activeSection === 2 && (
            <ReadingSection title="Active Retrieval." eyebrow="Step 3" icon={BrainCircuit} theme={theme}>
                <p>The most powerful way to build lasting memory is <Highlight description="The act of deliberately recalling information from memory, rather than passively reviewing it. This struggle to retrieve is the mechanism that strengthens long-term storage." theme={theme}>Active Retrieval</Highlight>, also known as practice testing. It's the "gold standard" for learning. Why? Because the act of struggling to pull information out of your brain sends a powerful signal to strengthen that neural pathway for future use.</p>
                <p>This is the opposite of re-reading. Re-reading is like looking at a map of a city. Active retrieval is like being dropped in the city and forced to find your own way. It's harder, more frustrating, and you'll make more mistakes. But it's the only way you'll actually learn the layout. The struggle is not a sign that you're failing; it's the biological signal that you're learning.</p>
            </ReadingSection>
          )}
          {activeSection === 3 && (
            <ReadingSection title="Distributed Practice." eyebrow="Step 4" icon={Timer} theme={theme}>
              <p>The second "golden rule" is <Highlight description="Also known as 'spacing.' It's the strategy of spreading out your study sessions over time, rather than cramming them all at once." theme={theme}>Distributed Practice</Highlight>. Cramming feels effective because it keeps information in your short-term working memory. It works for a test in 10 minutes, but it's a disaster for a test in a week.</p>
              <p>Spacing leverages the <Highlight description="The natural, exponential decay of memory over time. To create durable learning, you must interrupt this curve by revisiting the information just as you're beginning to forget it." theme={theme}>Forgetting Curve</Highlight>. To build strong memories, you need to let yourself forget a little. This makes the next retrieval attempt harder, which, as we've learned, sends a stronger signal to your brain to "save this file permanently." The rule is simple: one hour a day for seven days is infinitely better than seven hours in one day.</p>
            </ReadingSection>
          )}
           {activeSection === 4 && (
            <ReadingSection title="The Anxiety Paradox." eyebrow="Step 5" icon={HeartPulse} theme={theme}>
              <p>A common argument against more testing is that it causes anxiety. But the research shows the opposite. Frequent, low-stakes quizzing is one of the most powerful tools for *reducing* exam anxiety. Why? Because anxiety often comes from uncertainty. The Illusion of Competence leaves you feeling confident but actually being unprepared. The high-stakes exam is the first time you discover the truth, leading to panic.</p>
              <p>Active retrieval is a process of <Highlight description="The act of accurately judging your own level of knowledge. Low-stakes testing calibrates your metacognition, eliminating the surprise and anxiety of a high-stakes exam." theme={theme}>Metacognitive Calibration</Highlight>. It strips away the illusion. By constantly testing yourself, you know *exactly* what you know and what you don't long before the real exam. There are no surprises, no panic. You've already faced the struggle in a low-stakes environment, desensitizing yourself to the pressure.</p>
            </ReadingSection>
          )}
           {activeSection === 5 && (
            <ReadingSection title="Your Action Plan." eyebrow="Step 6" icon={ClipboardCheck} theme={theme}>
                <p>You now have the scientific evidence. The final step is to apply it. You must abandon the comfort of passive review and embrace the "desirable difficulty" of active retrieval. The key takeaways are simple but transformative.</p>
                <p>**The "Book Closed" Rule:** Never judge how well you know something with the book open in front of you. That's just fluency talking. Close the book, then ask yourself what you know. **Embrace Disfluency:** Understand that the feeling of "struggle" is the feeling of learning happening. If studying feels easy, it's probably ineffective. **Stop Dropping Items:** Don't stop testing yourself on something just because you got it right once. Continued retrieval is what arrests the forgetting curve. </p>
                <MicroCommitment theme={theme}>
                    <p>For your next study session, commit to this: for every 30 minutes, spend 10 minutes reading/reviewing, and 20 minutes testing yourself on what you just read. You will double your retention.</p>
                </MicroCommitment>
            </ReadingSection>
          )}
        </>
      )}
    </ModuleLayout>
  );
};
export default AchievingEffectiveLearningOutcomesModule;
