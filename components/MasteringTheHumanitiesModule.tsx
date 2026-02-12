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

const MotionDiv = motion.div as any;

interface SRPTopic {
  keyword: string;
  steps: { prompt: string; expert: string; keyTerms: string[] }[];
  fullSRP: string;
}

const SRP_TOPICS: SRPTopic[] = [
  {
    keyword: 'Carbonation',
    steps: [
      { prompt: 'What is carbonation?', expert: 'Carbonation is a chemical weathering process', keyTerms: ['chemical', 'weathering'] },
      { prompt: 'How does it work?', expert: 'where rainwater absorbs CO\u2082 to form a weak carbonic acid that dissolves limestone', keyTerms: ['carbonic acid', 'limestone', 'CO\u2082'] },
      { prompt: 'Give a specific example', expert: 'e.g. the formation of limestone pavements in the Burren, Co. Clare', keyTerms: ['Burren', 'Clare'] },
    ],
    fullSRP: 'Carbonation is a chemical weathering process where rainwater absorbs CO\u2082 to form a weak carbonic acid that dissolves limestone, e.g. the Burren, Co. Clare.',
  },
  {
    keyword: 'Urbanisation',
    steps: [
      { prompt: 'What is urbanisation?', expert: 'Urbanisation is the movement of people from rural to urban areas', keyTerms: ['movement', 'rural', 'urban'] },
      { prompt: 'What causes it?', expert: 'driven by pull factors such as employment, education, and better services in cities', keyTerms: ['pull factors', 'employment'] },
      { prompt: 'Give a specific example', expert: 'e.g. Dublin\u2019s population grew from 1.0M to 1.4M between 1991 and 2022', keyTerms: ['Dublin', '1.0M', '1.4M'] },
    ],
    fullSRP: 'Urbanisation is the movement of people from rural to urban areas, driven by pull factors such as employment and services, e.g. Dublin grew from 1.0M to 1.4M.',
  },
  {
    keyword: 'Abrasion',
    steps: [
      { prompt: 'What is abrasion?', expert: 'Abrasion is a process of erosion', keyTerms: ['erosion', 'process'] },
      { prompt: 'How does it work?', expert: 'where rock fragments carried by rivers, waves, or glaciers scrape and wear away the bedrock surface', keyTerms: ['rock fragments', 'scrape', 'bedrock'] },
      { prompt: 'Give a specific example', expert: 'e.g. the smoothing of river beds in the River Shannon', keyTerms: ['River Shannon', 'smoothing'] },
    ],
    fullSRP: 'Abrasion is a process of erosion where rock fragments carried by rivers, waves, or glaciers scrape and wear away the bedrock surface, e.g. the River Shannon.',
  },
  {
    keyword: 'Continental Drift',
    steps: [
      { prompt: 'What is continental drift?', expert: 'Continental drift is the theory that the continents were once joined in a supercontinent called Pangaea', keyTerms: ['theory', 'Pangaea', 'supercontinent'] },
      { prompt: 'What evidence supports it?', expert: 'supported by evidence such as matching fossils, rock types, and coastline shapes across continents', keyTerms: ['fossils', 'coastline', 'rock types'] },
      { prompt: 'Give a specific example', expert: 'e.g. Mesosaurus fossils found in both South America and Africa', keyTerms: ['Mesosaurus', 'South America', 'Africa'] },
    ],
    fullSRP: 'Continental drift is the theory that continents were once joined as Pangaea, supported by matching fossils and coastline shapes, e.g. Mesosaurus fossils in South America and Africa.',
  },
  {
    keyword: 'Freeze-Thaw Weathering',
    steps: [
      { prompt: 'What is freeze-thaw?', expert: 'Freeze-thaw is a physical weathering process', keyTerms: ['physical', 'weathering'] },
      { prompt: 'How does it work?', expert: 'where water enters cracks in rock, freezes and expands by 9%, widening the crack over repeated cycles', keyTerms: ['cracks', 'freezes', 'expands', '9%'] },
      { prompt: 'Give a specific example', expert: 'e.g. scree slopes on mountain sides in the Macgillycuddy\u2019s Reeks', keyTerms: ['scree', 'Macgillycuddy'] },
    ],
    fullSRP: 'Freeze-thaw is a physical weathering process where water enters cracks, freezes and expands by 9%, widening them over repeated cycles, e.g. scree slopes in the Macgillycuddy\u2019s Reeks.',
  },
];

const STEP_LABELS = ['Define', 'Process', 'Example'];

const SRPBuilder = () => {
  const [topicIdx, setTopicIdx] = useState(0);
  const [currentStep, setCurrentStep] = useState(0);
  const [inputs, setInputs] = useState<string[]>(['', '', '']);
  const [revealed, setRevealed] = useState<boolean[]>([false, false, false]);
  const [completed, setCompleted] = useState(false);
  const [srpCount, setSrpCount] = useState(0);
  const [allDone, setAllDone] = useState(false);

  const topic = SRP_TOPICS[topicIdx];

  const checkKeyTerms = (input: string, keyTerms: string[]) => {
    const lower = input.toLowerCase();
    let hits = 0;
    for (const term of keyTerms) {
      if (lower.includes(term.toLowerCase())) hits++;
    }
    return hits >= 2 || (keyTerms.length < 2 && hits >= 1);
  };

  const handleCheck = (stepIndex: number) => {
    const next = [...revealed];
    next[stepIndex] = true;
    setRevealed(next);
    if (stepIndex < 2) {
      setCurrentStep(stepIndex + 1);
    } else {
      setCompleted(true);
      setSrpCount(prev => prev + 1);
    }
  };

  const handleNext = () => {
    if (topicIdx < SRP_TOPICS.length - 1) {
      setTopicIdx(prev => prev + 1);
      setCurrentStep(0);
      setInputs(['', '', '']);
      setRevealed([false, false, false]);
      setCompleted(false);
    } else {
      setAllDone(true);
    }
  };

  if (allDone) {
    return (
      <div className="my-10 p-8 md:p-12 bg-white dark:bg-zinc-800 rounded-xl border border-zinc-200 dark:border-zinc-700">
        <h4 className="font-serif text-2xl font-semibold text-zinc-800 dark:text-white text-center">SRP Builder — Complete</h4>
        <MotionDiv initial={{ opacity: 0, y: 16 }} animate={{ opacity: 1, y: 0 }} transition={{ duration: 0.4 }} className="mt-8 text-center space-y-4">
          <p className="text-5xl font-bold text-emerald-500">{srpCount} / 5</p>
          <p className="text-sm font-medium text-zinc-500 dark:text-zinc-400">SRPs Built</p>
          <div className="mt-6 p-6 bg-emerald-50 dark:bg-emerald-900/20 rounded-lg border border-emerald-200 dark:border-emerald-800">
            <p className="text-sm text-zinc-700 dark:text-zinc-300 leading-relaxed">Every 30-mark Geography answer needs <strong>~15 SRPs</strong>. If you can build them like this from keywords, you can engineer your grade.</p>
          </div>
        </MotionDiv>
      </div>
    );
  }

  return (
    <div className="my-10 p-8 md:p-12 bg-white dark:bg-zinc-800 rounded-xl border border-zinc-200 dark:border-zinc-700">
      <h4 className="font-serif text-2xl font-semibold text-zinc-800 dark:text-white text-center">SRP Builder — From Keyword to Full Marks</h4>
      <p className="text-center text-xs text-zinc-400 dark:text-zinc-500 mt-1">Topic {topicIdx + 1} of {SRP_TOPICS.length}</p>

      {/* Keyword pill */}
      <div className="flex justify-center mt-6">
        <span className="inline-block px-5 py-2 rounded-full bg-pink-100 dark:bg-pink-900/30 text-pink-700 dark:text-pink-300 font-bold text-lg tracking-wide">{topic.keyword}</span>
      </div>

      {/* Steps */}
      <div className="mt-8 space-y-6">
        <AnimatePresence mode="wait">
          {topic.steps.map((step, i) => (
            i <= currentStep && (
              <MotionDiv key={`${topicIdx}-${i}`} initial={{ opacity: 0, y: 12 }} animate={{ opacity: 1, y: 0 }} transition={{ duration: 0.35, delay: 0.05 }} className="space-y-3">
                {/* Step header */}
                <div className="flex items-center gap-3">
                  <span className="flex-shrink-0 w-7 h-7 rounded-full bg-pink-500 text-white text-xs font-bold flex items-center justify-center">{i + 1}</span>
                  <span className="text-xs font-semibold uppercase tracking-wider text-zinc-400 dark:text-zinc-500">{STEP_LABELS[i]}</span>
                </div>
                <p className="text-sm font-medium text-zinc-700 dark:text-zinc-300">{step.prompt}</p>

                {/* Input area */}
                {!revealed[i] ? (
                  <div className="flex gap-2">
                    <input
                      type="text"
                      value={inputs[i]}
                      onChange={e => {
                        const next = [...inputs];
                        next[i] = e.target.value;
                        setInputs(next);
                      }}
                      placeholder="Type your answer..."
                      className="flex-1 px-4 py-2 rounded-lg border border-zinc-300 dark:border-zinc-600 bg-zinc-50 dark:bg-zinc-900 text-sm text-zinc-800 dark:text-zinc-200 focus:outline-none focus:ring-2 focus:ring-pink-400"
                    />
                    <button onClick={() => handleCheck(i)} className="px-4 py-2 rounded-lg bg-pink-500 hover:bg-pink-600 text-white text-sm font-semibold transition-colors">Check</button>
                  </div>
                ) : (
                  <MotionDiv initial={{ opacity: 0, x: -8 }} animate={{ opacity: 1, x: 0 }} transition={{ duration: 0.3 }} className={`p-3 rounded-lg text-sm ${checkKeyTerms(inputs[i], step.keyTerms) ? 'bg-emerald-50 dark:bg-emerald-900/20 border border-emerald-200 dark:border-emerald-800' : 'bg-amber-50 dark:bg-amber-900/20 border border-amber-200 dark:border-amber-800'}`}>
                    <p className={`text-xs font-bold mb-1 ${checkKeyTerms(inputs[i], step.keyTerms) ? 'text-emerald-600 dark:text-emerald-400' : 'text-amber-600 dark:text-amber-400'}`}>
                      {checkKeyTerms(inputs[i], step.keyTerms) ? 'Good — you hit the key terms' : 'Compare with the model answer'}
                    </p>
                    <p className="text-zinc-700 dark:text-zinc-300">{step.expert}</p>
                  </MotionDiv>
                )}
              </MotionDiv>
            )
          ))}
        </AnimatePresence>
      </div>

      {/* Assembled SRP */}
      {completed && (
        <MotionDiv initial={{ opacity: 0, y: 12 }} animate={{ opacity: 1, y: 0 }} transition={{ duration: 0.4, delay: 0.15 }} className="mt-8 p-5 bg-emerald-50 dark:bg-emerald-900/20 rounded-xl border-l-4 border-emerald-500">
          <div className="flex items-center justify-between mb-2">
            <p className="text-xs font-bold uppercase tracking-wider text-emerald-600 dark:text-emerald-400">Assembled SRP</p>
            <span className="px-2 py-0.5 rounded text-xs font-bold bg-emerald-500 text-white">2 MARKS</span>
          </div>
          <p className="text-sm text-zinc-800 dark:text-zinc-200 leading-relaxed">{topic.fullSRP}</p>
          <div className="mt-4 flex justify-end">
            <button onClick={handleNext} className="px-5 py-2 rounded-lg bg-pink-500 hover:bg-pink-600 text-white text-sm font-semibold transition-colors">
              {topicIdx < SRP_TOPICS.length - 1 ? 'Next Topic \u2192' : 'See Results \u2192'}
            </button>
          </div>
        </MotionDiv>
      )}
    </div>
  );
};

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
              <SRPBuilder />
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
