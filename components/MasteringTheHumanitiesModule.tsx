/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
*/

import React, { useState } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import {
  Key, Landmark, Globe, Brain, Wrench
} from 'lucide-react';
import { ModuleProgress } from '../types';
import { pinkTheme } from '../moduleThemes';
import { Highlight, ReadingSection, MicroCommitment } from './ModuleShared';
import { ModuleLayout } from './ModuleLayout';

const theme = pinkTheme;

// --- INTERACTIVE COMPONENTS ---
const HistoryGrader = () => {
    const [cm, setCm] = useState(60);
    const [oe, setOe] = useState(15);
    const total = cm + oe;
    const grade = total >= 90 ? 'H1' : total >= 80 ? 'H2' : total >= 70 ? 'H3' : total >= 60 ? 'H4' : 'H5';

    return(
        <div className="my-10 p-8 md:p-12 bg-white dark:bg-zinc-800 rounded-xl border border-zinc-200 dark:border-zinc-700">
            <h4 className="font-serif text-2xl font-semibold text-zinc-800 dark:text-white text-center">CM/OE Grader</h4>
            <div className="grid grid-cols-2 gap-6 items-center">
                <div className="space-y-4">
                    <div><label className="text-xs font-bold">CM (Content): {cm}/60</label><input type="range" min="0" max="60" value={cm} onChange={e=>setCm(parseInt(e.target.value))} className="w-full"/></div>
                    <div><label className="text-xs font-bold">OE (Argument): {oe}/40</label><input type="range" min="0" max="40" value={oe} onChange={e=>setOe(parseInt(e.target.value))} className="w-full"/></div>
                </div>
                <div className="text-center">
                    <p className="text-sm">Final Grade:</p>
                    <p className="text-6xl font-semibold text-pink-500">{grade}</p>
                </div>
            </div>
        </div>
    );
};

// --- MODULE COMPONENT ---
const MasteringTheHumanitiesModule: React.FC<{ onBack: () => void; progress: ModuleProgress; onProgressUpdate: (progress: ModuleProgress) => void }> = ({ onBack, progress, onProgressUpdate }) => {
  const sections = [
    { id: 'hidden-curriculum', title: 'The Hidden Curriculum', eyebrow: '01 // The Master Key', icon: Key },
    { id: 'history-engine', title: 'The History Engine', eyebrow: '02 // CM + OE', icon: Landmark },
    { id: 'geography-algorithm', title: 'The Geography Algorithm', eyebrow: '03 // SRPs', icon: Globe },
    { id: 'universal-toolkit', title: 'The Universal Toolkit', eyebrow: '04 // The PEE Chain', icon: Brain },
    { id: 'blueprint', title: 'Your Blueprint', eyebrow: '05 // The Action Plan', icon: Wrench },
  ];

  return (
    <ModuleLayout
      moduleNumber="07"
      moduleTitle="Mastering the Humanities"
      moduleSubtitle="The Grade Optimisation Protocol"
      moduleDescription="Deconstruct the &quot;hidden curriculum&quot; of History, Geography, and Politics &amp; Society to transform your strategic application and maximize your grade."
      theme={theme}
      sections={sections}
      onBack={onBack}
      progress={progress}
      onProgressUpdate={onProgressUpdate}
    >
      {(activeSection) => (
        <>
          {activeSection === 0 && (
            <ReadingSection title="The Hidden Curriculum." eyebrow="Step 1" icon={Key} theme={theme}>
              <p>In the Leaving Cert Humanities, the gap between a H3 and a H1 is rarely a lack of knowledge. It's a lack of <Highlight description="The ability to align your knowledge with the specific, often unwritten, rules of the marking scheme for each subject." theme={theme}>strategic application</Highlight>. Each subject has a "hidden curriculum" and trades in a different "currency" of marks. To succeed, you must become fluent in each of these currencies.</p>
            </ReadingSection>
          )}
          {activeSection === 1 && (
            <ReadingSection title="The History Engine." eyebrow="Step 2" icon={Landmark} theme={theme}>
              <p>The History essay is not marked as one piece. It's a dual-process system. The <Highlight description="Cumulative Mark (60/100): Rewards the quantity and accuracy of historical facts. The strategy is volume - aim for 8-10 dense paragraphs." theme={theme}>Cumulative Mark (CM)</Highlight> is a measure of historical content. The <Highlight description="Overall Evaluation (40/100): A qualitative multiplier that assesses the quality of your argument, its relevance to the specific question, and your historical analysis." theme={theme}>Overall Evaluation (OE)</Highlight> assesses your skill as a historian.</p>
              <p>The classic H3 trap is maxing out the CM with a pre-learned essay but scoring low on OE because the essay doesn't answer the specific question asked. Your argument is the engine; facts are just the fuel.</p>
              <HistoryGrader/>
            </ReadingSection>
          )}
          {activeSection === 2 && (
            <ReadingSection title="The Geography Algorithm." eyebrow="Step 3" icon={Globe} theme={theme}>
              <p>Geography operates on a completely different logic. Its currency is the <Highlight description="A Significant Relevant Point is a single, developed piece of factual information, typically worth 2 marks. A 30-mark essay requires 15 of them." theme={theme}>Significant Relevant Point (SRP)</Highlight>. An essay is simply a container for accumulating these discrete units of information. The logic is algorithmic and quantitative.</p>
              <p>A weak answer gives a keyword; a strong answer gives a statement plus development. For example, "Limestone dissolves" (0 marks) vs. "Carbonation occurs when rainwater absorbs CO2, forming a weak carbonic acid" (2 marks). Your job is to become an SRP-generating machine.</p>
            </ReadingSection>
          )}
          {activeSection === 3 && (
            <ReadingSection title="The Universal Toolkit." eyebrow="Step 4" icon={Brain} theme={theme}>
              <p>While the currencies differ, the underlying structure of a good argument is universal. The <Highlight description="A robust heuristic for essay writing: plan 3-4 distinct arguments, structure each paragraph using PEE, and in discursive subjects, consider 3 perspectives (Thesis, Antithesis, Synthesis)." theme={theme}>"Rule of Three"</Highlight> is a powerful framework. Plan <strong>3 core arguments</strong> for every essay. Structure each paragraph using the <strong>PEE chain</strong>: <strong>P</strong>oint (your topic sentence), <strong>E</strong>vidence (your fact, quote, or SRP), and <strong>E</strong>xplanation (the "So what?" factor that links the evidence back to your point).</p>
            </ReadingSection>
          )}
          {activeSection === 4 && (
            <ReadingSection title="Your Blueprint." eyebrow="Step 5" icon={Wrench} theme={theme}>
              <p>You now have the decryption key for the Humanities exams. You understand the different "currencies" and the universal structures. Your task now is to become a "grade engineer"--to consciously align every answer you write with the specific demands of the marking scheme.</p>
              <MicroCommitment theme={theme}>
                <p>Go to the SEC website and download the marking scheme for your favourite Humanities subject. Spend 10 minutes reading it. This is no longer just an exam; it's a system you are learning to master.</p>
              </MicroCommitment>
            </ReadingSection>
          )}
        </>
      )}
    </ModuleLayout>
  );
};
export default MasteringTheHumanitiesModule;
