/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
*/

import React, { useId, useState } from 'react';
import { AnimatePresence } from 'framer-motion';
import { MotionDiv } from './Motion';
import {
  Key, Landmark, Globe, Brain, Wrench
} from 'lucide-react';
import { type ModuleProgress } from '../types';
import { pinkTheme } from '../moduleThemes';
import { Highlight, ReadingSection, MicroCommitment, PersonalStory } from './ModuleShared';
import { ModuleLayout } from './ModuleLayout';
import { useEssentialsMode } from '../hooks/useEssentialsMode';
import { AnswerLine, ExerciseRange, ExerciseSheet } from './learning/Exercise';
import { Button } from './ui/Button';
import { Field } from './ui/Field';

const theme = pinkTheme;

// --- INTERACTIVE COMPONENTS ---

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
  const promptId = useId();

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
      <ExerciseSheet title="SRP Builder — Complete" name="SRPBuilder">
        <MotionDiv initial={{ opacity: 0, y: 16 }} animate={{ opacity: 1, y: 0 }} transition={{ duration: 0.4 }} className="ex-stack">
          {/* The count, in ink (was a green number), and the line that answers it with the tick (no mint box) */}
          <div className="ex-result">
            <p className="ex-result-name" style={{ fontSize: 48, lineHeight: '52px', letterSpacing: '-0.04em' }}>{srpCount} / 5</p>
            <p className="t-sub">SRPs Built</p>
          </div>
          <AnswerLine>Every 30-mark Geography answer needs <strong>~15 SRPs</strong>. If you can build them like this from keywords, you can engineer your grade.</AnswerLine>
        </MotionDiv>
      </ExerciseSheet>
    );
  }

  return (
    <ExerciseSheet title="SRP Builder — From Keyword to Full Marks" name="SRPBuilder">
      <p className="ex-count ui-readout">Topic {topicIdx + 1} of {SRP_TOPICS.length}</p>

      {/* The keyword: the word you build from, set large on the sheet (no pink pill) */}
      <p className="ex-thought-words">{topic.keyword}</p>

      {/* Steps: ruled rows on the sheet, each with its number ring (ink for the step you are on) */}
      <div className="ex-list">
        <AnimatePresence mode="wait">
          {topic.steps.map((step, i) => (
            i <= currentStep && (
              <MotionDiv key={`${topicIdx}-${i}`} initial={{ opacity: 0, y: 12 }} animate={{ opacity: 1, y: 0 }} transition={{ duration: 0.35, delay: 0.05 }}>
                <div className="ex-stack">
                {/* Step header */}
                <div className="flex items-center gap-3">
                  <span className={i === currentStep && !revealed[i] ? 'ex-badge ex-badge--on' : 'ex-badge'}>{i + 1}</span>
                  <span className="ex-label">{STEP_LABELS[i]}</span>
                </div>
                <p id={`${promptId}-${i}`} className="t-body text-ink-primary">{step.prompt}</p>

                {/* Input area */}
                {!revealed[i] ? (
                  <div className="flex gap-2 items-center">
                    <Field
                      type="text"
                      aria-labelledby={`${promptId}-${i}`}
                      value={inputs[i]}
                      onChange={e => {
                        const next = [...inputs];
                        next[i] = e.target.value;
                        setInputs(next);
                      }}
                      placeholder="Type your answer..."
                      className="flex-1 min-w-0"
                    />
                    <Button onClick={() => handleCheck(i)}>Check</Button>
                  </div>
                ) : (
                  <MotionDiv initial={{ opacity: 0, x: -8 }} animate={{ opacity: 1, x: 0 }} transition={{ duration: 0.3 }} className="flex flex-col gap-1">
                    {/* The check: a line in ink (the tick when the key terms are there), then the model answer (no mint or amber box) */}
                    <AnswerLine tone={checkKeyTerms(inputs[i], step.keyTerms) ? 'ok' : 'note'}>
                      {checkKeyTerms(inputs[i], step.keyTerms) ? 'Good — you hit the key terms' : 'Compare with the model answer'}
                    </AnswerLine>
                    <p className="ex-block-text">{step.expert}</p>
                  </MotionDiv>
                )}
                </div>
              </MotionDiv>
            )
          ))}
        </AnimatePresence>
      </div>

      {/* Assembled SRP: its label and words under a hairline (no green panel, side stripe or pill) */}
      {completed && (
        <MotionDiv initial={{ opacity: 0, y: 12 }} animate={{ opacity: 1, y: 0 }} transition={{ duration: 0.4, delay: 0.15 }} className="ex-stack">
          <div className="ex-block">
            <div className="flex items-center justify-between gap-3">
              <p className="ex-label">Assembled SRP</p>
              <span className="ui-readout text-ink-secondary">2 MARKS</span>
            </div>
            <p className="t-body text-ink-primary">{topic.fullSRP}</p>
          </div>
          <div className="ex-actions">
            <Button onClick={handleNext}>
              {topicIdx < SRP_TOPICS.length - 1 ? 'Next Topic \u2192' : 'See Results \u2192'}
            </Button>
          </div>
        </MotionDiv>
      )}
    </ExerciseSheet>
  );
};

const HistoryGrader = () => {
    const [cm, setCm] = useState(60);
    const [oe, setOe] = useState(15);
    const cmId = useId();
    const oeId = useId();
    const total = cm + oe;
    const grade = total >= 90 ? 'H1' : total >= 80 ? 'H2' : total >= 70 ? 'H3' : total >= 60 ? 'H4' : 'H5';

    return(
        <ExerciseSheet title="CM/OE Grader" name="HistoryGrader">
            <div className="grid grid-cols-2 gap-6 items-center">
                {/* The two sliders: the shared slider (a hairline track, an ink fill), each named by its visible label */}
                <div className="ex-sliders">
                    <div className="ex-slider"><p id={cmId} className="ex-slider-name">CM (Content): {cm}/60</p><ExerciseRange min="0" max="60" value={cm} onChange={e=>setCm(parseInt(e.target.value))} aria-labelledby={cmId}/></div>
                    <div className="ex-slider"><p id={oeId} className="ex-slider-name">OE (Argument): {oe}/40</p><ExerciseRange min="0" max="40" value={oe} onChange={e=>setOe(parseInt(e.target.value))} aria-labelledby={oeId}/></div>
                </div>
                {/* The grade it comes to: large, in ink (was pink) */}
                <div className="text-center">
                    <p className="t-sub">Final Grade:</p>
                    <p className="text-ink-primary" style={{ fontSize: 60, lineHeight: '64px', letterSpacing: '-0.04em' }}>{grade}</p>
                </div>
            </div>
        </ExerciseSheet>
    );
};

// --- MODULE COMPONENT ---
const MasteringTheHumanitiesModule: React.FC<{ onBack: () => void; progress: ModuleProgress; onProgressUpdate: (progress: ModuleProgress) => void }> = ({ onBack, progress, onProgressUpdate }) => {
  const essentials = useEssentialsMode();
  const sections = [
    { id: 'unwritten-rules', title: 'The Unwritten Rules', eyebrow: '01 // What They Don\'t Tell You', icon: Key },
    { id: 'history-engine', title: 'How History Is Really Marked', eyebrow: '02 // CM + OE', icon: Landmark },
    { id: 'geography-srps', title: 'How Geography Is Really Marked', eyebrow: '03 // SRPs', icon: Globe },
    { id: 'universal-toolkit', title: 'The Essay Toolkit', eyebrow: '04 // The PEE Chain', icon: Brain },
    { id: 'blueprint', title: 'Your Action Plan', eyebrow: '05 // What to Do Next', icon: Wrench },
  ];

  return (
    <ModuleLayout
      moduleNumber="08"
      moduleTitle="Mastering the Humanities"
      moduleSubtitle="Your Guide to Getting Better Marks"
      moduleDescription="History, Geography, and Politics & Society each have their own unwritten rules for how marks are given. Once you know them, everything changes."
      theme={theme}
      sections={sections}
      onBack={onBack}
      progress={progress}
      onProgressUpdate={onProgressUpdate}
      finishButtonText="Make Your Case"
    >
      {(activeSection) => (
        <>
          {activeSection === 0 && (
            <ReadingSection title="The Unwritten Rules." eyebrow="Step 1" icon={Key} theme={theme}>
              {essentials ? (
                <p>The gap between H3 and H1 isn't about knowing more. It's about <Highlight description="Knowing exactly what the examiner wants and giving it to them in the right format. Each subject rewards different things." theme={theme}>knowing what to do</Highlight> with what you know. Each subject rewards a different type of answer. Learn the rules, give the examiner what they want.</p>
              ) : (
                <>
                  <p>In the Leaving Cert Humanities, the gap between a H3 and a H1 is rarely about how much you know. It comes down to <Highlight description="Knowing exactly what the examiner wants and giving it to them in the right format. Each subject rewards different things." theme={theme}>knowing what to do</Highlight> with what you know. Each subject has its own unwritten rules and rewards a different type of answer. Once you figure out what each subject is actually looking for, you can start giving the examiner exactly what they want.</p>
                  <PersonalStory name="Sinéad" role="6th Year, Wexford">
                    <p>I was getting H3s in History even though I knew my stuff inside out. Turns out I was writing everything I knew about a topic instead of actually answering the question. Once I understood how the marking scheme worked, I jumped to a H1 in the mocks without learning a single new fact.</p>
                  </PersonalStory>
                </>
              )}
            </ReadingSection>
          )}
          {activeSection === 1 && (
            <ReadingSection title="How History Is Really Marked." eyebrow="Step 2" icon={Landmark} theme={theme}>
              {essentials ? (
                <>
                  <p>Your History essay gets two scores. <Highlight description="This is your facts score (out of 60). The more accurate historical detail you pack in, the higher it goes. Aim for 8-10 solid paragraphs." theme={theme}>CM (Cumulative Mark)</Highlight> counts your facts. <Highlight description="This is your argument score (out of 40). It measures how well you actually answer the question and how good your reasoning is." theme={theme}>OE (Overall Evaluation)</Highlight> scores your argument.</p>
                  <p>The H3 trap: dumping facts without answering the question. Your argument drives the grade. Facts are just fuel.</p>
                </>
              ) : (
                <>
                  <p>Here is the thing most students do not realise: your History essay is not marked as one piece. It actually gets two separate scores. The <Highlight description="This is your facts score (out of 60). The more accurate historical detail you pack in, the higher it goes. Aim for 8-10 solid paragraphs." theme={theme}>Cumulative Mark (CM)</Highlight> is basically how many facts you include. The <Highlight description="This is your argument score (out of 40). It measures how well you actually answer the question and how good your reasoning is." theme={theme}>Overall Evaluation (OE)</Highlight> is about how well you argue your point.</p>
                  <p>The classic H3 trap? You learn an essay off by heart, dump all your facts onto the page, and score well on CM -- but you barely answer the actual question, so your OE tanks. Your argument is what drives the grade; facts are just the fuel.</p>
                </>
              )}
              <HistoryGrader/>
            </ReadingSection>
          )}
          {activeSection === 2 && (
            <ReadingSection title="How Geography Is Really Marked." eyebrow="Step 3" icon={Globe} theme={theme}>
              {essentials ? (
                <>
                  <p>Geography marks come from <Highlight description="An SRP is one developed fact that earns you 2 marks. A 30-mark question needs about 15 of them. Think of each one as a mini building block." theme={theme}>SRPs (Significant Relevant Points)</Highlight>. Each developed fact is worth 2 marks. A 30-mark question needs about 15 of them.</p>
                  <p>"Limestone dissolves" gets nothing. "Carbonation occurs when rainwater absorbs CO2, forming carbonic acid" scores 2 marks. Develop every keyword.</p>
                </>
              ) : (
                <>
                  <p>Geography works completely differently to History. What matters here is the <Highlight description="An SRP is one developed fact that earns you 2 marks. A 30-mark question needs about 15 of them. Think of each one as a mini building block." theme={theme}>Significant Relevant Point (SRP)</Highlight>. A Geography essay is basically a collection of these small building blocks of information. The more solid SRPs you include, the higher your mark.</p>
                  <p>A weak answer just throws out a keyword; a strong answer develops it. For example, "Limestone dissolves" gets you nothing, but "Carbonation occurs when rainwater absorbs CO2, forming a weak carbonic acid" is worth 2 marks. The goal is to get really good at building these SRPs from any keyword.</p>
                </>
              )}
              <SRPBuilder />
            </ReadingSection>
          )}
          {activeSection === 3 && (
            <ReadingSection title="The Essay Toolkit." eyebrow="Step 4" icon={Brain} theme={theme}>
              <p>Even though each subject marks differently, the basic shape of a good answer is the same everywhere. The <Highlight description="A simple trick: plan 3 clear arguments for every essay, and structure each paragraph using PEE. It works in History, Geography, and Politics." theme={theme}>"Rule of Three"</Highlight> is a dead-simple approach that works across all your Humanities subjects. Plan <strong>3 clear arguments</strong> for every essay. Then structure each paragraph using the <strong>PEE chain</strong>: <strong>P</strong>oint (your opening sentence that states your argument), <strong>E</strong>vidence (the fact, quote, or SRP that backs it up), and <strong>E</strong>xplanation (the "so what?" -- why does this evidence matter and how does it support your point?).</p>
            </ReadingSection>
          )}
          {activeSection === 4 && (
            <ReadingSection title="Your Action Plan." eyebrow="Step 5" icon={Wrench} theme={theme}>
              <p>You now know how the Humanities exams actually work. You know that History has two scores, that Geography runs on SRPs, and that PEE works everywhere. The next step is simple: start checking your own answers against the marking scheme every time you practise. That is what separates someone who knows the material from someone who gets the marks for it.</p>
              <MicroCommitment theme={theme}>
                <p>Go to examinations.ie and download the marking scheme for your favourite Humanities subject. Spend 10 minutes reading through it. You will start to see exactly what the examiner is looking for -- and it is probably different from what you expected.</p>
              </MicroCommitment>
            </ReadingSection>
          )}
        </>
      )}
    </ModuleLayout>
  );
};
export default MasteringTheHumanitiesModule;
