/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
*/

import React, { useId, useState } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { MotionDiv } from './Motion';
import {
  Key, PieChart, Briefcase, FileText, BrainCircuit, Wrench
} from 'lucide-react';
import { type ModuleProgress } from '../types';
import { grayTheme } from '../moduleThemes';
import { Highlight, ReadingSection, MicroCommitment, PersonalStory } from './ModuleShared';
import { ModuleLayout } from './ModuleLayout';
import { useEssentialsMode } from '../hooks/useEssentialsMode';
import { AnswerLine, ExerciseSheet } from './learning/Exercise';
import { Button } from './ui/Button';
import { AreaField } from './ui/Field';

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
        <ExerciseSheet title={'ABQ "Link" Methodology Drill'} name="ABQLinkDrill">
             {/* The step's words: on the sheet under a hairline, not in a grey box */}
             <AnimatePresence mode="wait">
                <motion.div key={step} initial={{opacity:0, y:10}} animate={{opacity:1, y:0}} exit={{opacity:0, y:-10}} className="ex-block min-h-[80px]">
                    <p className="ex-quote">{steps[step]}</p>
                </motion.div>
             </AnimatePresence>
             <div className="ex-actions"><Button onClick={() => setStep(s => (s + 1) % steps.length)}>Next Step</Button></div>
        </ExerciseSheet>
    );
};

// --- ABQ ANSWER SCAFFOLD ---
const ABQ_SCENARIOS = [
  {
    extract: 'TechStart Ltd grew from 5 to 50 employees in 18 months. The CEO now finds herself dealing with staff conflicts, missed deadlines, and communication breakdowns between departments.',
    prompt: 'Identify and explain ONE management challenge facing TechStart Ltd.',
    models: {
      state: 'TechStart Ltd is experiencing difficulties associated with the Growth phase of a business, specifically poor delegation and communication.',
      explain: 'As a business grows rapidly, the original management style becomes ineffective. Tasks that the owner once handled personally must now be delegated, and formal communication structures are needed.',
      link: 'This is evident in TechStart Ltd where "communication breakdowns between departments" and "missed deadlines" indicate the CEO has not yet adapted her management approach to the larger organisation.',
    },
    keywords: {
      state: ['growth', 'delegation', 'management', 'crisis', 'rapid', 'communication', 'phase'],
      link: ['"', 'communication', 'deadlines', 'breakdowns', 'TechStart'],
    },
  },
  {
    extract: 'FreshBake Bakery has been losing customers to a new competitor offering gluten-free and vegan options. Sales have dropped 15% in six months. The owner, Mary, has always focused on traditional recipes.',
    prompt: 'Advise Mary on a strategy to respond to the competitive threat.',
    models: {
      state: 'Mary should conduct market research and consider product diversification to respond to changing consumer demands.',
      explain: 'Market research involves gathering data on consumer preferences and competitor offerings. Product diversification means expanding the product range to include new options that meet emerging trends.',
      link: 'FreshBake is losing customers because the competitor offers "gluten-free and vegan options" that Mary\'s "traditional recipes" do not include. By adding these products, she can recapture lost market share.',
    },
    keywords: {
      state: ['market research', 'diversif', 'strategy', 'consumer', 'product', 'demand'],
      link: ['"', 'gluten', 'vegan', 'traditional', 'FreshBake', 'Mary'],
    },
  },
  {
    extract: 'GreenClean Ltd, an eco-friendly cleaning company, wants to expand from Dublin into Cork and Galway. They have \u20AC50,000 in savings and a strong social media presence with 20,000 followers.',
    prompt: 'Evaluate ONE source of finance suitable for GreenClean\u2019s expansion.',
    models: {
      state: 'GreenClean could use retained earnings (their \u20AC50,000 savings) as an internal source of finance for the expansion.',
      explain: 'Retained earnings are profits that have been kept in the business rather than distributed. This is an internal source with no interest charges or loss of ownership, but it depletes the company\u2019s cash reserves.',
      link: 'GreenClean has "\u20AC50,000 in savings" which could fund initial setup costs in Cork and Galway. However, this may leave limited working capital for day-to-day operations during the expansion.',
    },
    keywords: {
      state: ['retained', 'earnings', 'savings', 'internal', 'finance', 'source'],
      link: ['"', '50,000', 'savings', 'Cork', 'Galway', 'GreenClean', 'expansion'],
    },
  },
];

const STEP_LABELS = ['STATE', 'EXPLAIN', 'LINK'] as const;
const STEP_INSTRUCTIONS = [
  'State the theory or concept that applies to this case.',
  'Explain the theory in your own words \u2014 what does it mean?',
  'Link the theory back to the case study using a direct quote.',
];

const ABQAnswerScaffold = () => {
  const [scenarioIdx, setScenarioIdx] = useState(0);
  const [stepIdx, setStepIdx] = useState(0);
  const [inputs, setInputs] = useState(['', '', '']);
  const [revealed, setRevealed] = useState([false, false, false]);
  const [completed, setCompleted] = useState(false);
  const [allDone, setAllDone] = useState(false);
  const stepId = useId();

  const scenario = ABQ_SCENARIOS[scenarioIdx];

  const checkQuality = (text: string, step: number): 'good' | 'partial' => {
    const lower = text.toLowerCase();
    if (step === 1) {
      return lower.length > 40 ? 'good' : 'partial';
    }
    const kws = step === 0 ? scenario.keywords.state : scenario.keywords.link;
    const hits = kws.filter((kw) => lower.includes(kw.toLowerCase())).length;
    return hits >= 2 ? 'good' : 'partial';
  };

  const handleReveal = () => {
    const next = [...revealed];
    next[stepIdx] = true;
    setRevealed(next);
  };

  const handleNext = () => {
    if (stepIdx < 2) {
      setStepIdx(stepIdx + 1);
    } else {
      setCompleted(true);
    }
  };

  const handleNextScenario = () => {
    if (scenarioIdx < ABQ_SCENARIOS.length - 1) {
      setScenarioIdx(scenarioIdx + 1);
      setStepIdx(0);
      setInputs(['', '', '']);
      setRevealed([false, false, false]);
      setCompleted(false);
    } else {
      setAllDone(true);
    }
  };

  const handleInputChange = (value: string) => {
    const next = [...inputs];
    next[stepIdx] = value;
    setInputs(next);
  };

  const assembledAnswer = `${inputs[0]} ${inputs[1]} ${inputs[2]}`.trim();


  return (
    <ExerciseSheet
      title={<>
        ABQ Answer Builder
      </>}
      sub={<>
        Master the State &rarr; Explain &rarr; Link formula that the examiner rewards.
      </>}
      name="ABQAnswerScaffold"
    >
      <p className="ex-count ui-readout">
        Scenario {scenarioIdx + 1} / {ABQ_SCENARIOS.length}
      </p>

      {/* Case extract: words you read, on the sheet under their label and a hairline (no box) */}
      <div className="ex-block">
        <p className="ex-label">
          Case Extract
        </p>
        <p className="ex-block-text">
          {scenario.extract}
        </p>
      </div>

      {/* Theory prompt */}
      <p className="t-row text-ink-primary">
        {scenario.prompt}
      </p>

      {allDone ? (
        <MotionDiv
          initial={{ opacity: 0, y: 12 }}
          animate={{ opacity: 1, y: 0 }}
        >
          {/* Done: a line in ink with the tick, not a mint panel */}
          <AnswerLine>
            <b>
              All 3 scenarios complete.
            </b>{' '}
            The ABQ is worth <strong>80 marks</strong> &mdash; nearly a quarter of the paper. The
            State-Explain-Link structure is non-negotiable. Every answer without a direct quote from
            the case study is leaving marks on the table.
          </AnswerLine>
        </MotionDiv>
      ) : completed ? (
        <MotionDiv
          initial={{ opacity: 0, y: 12 }}
          animate={{ opacity: 1, y: 0 }}
          className="ex-stack"
        >
          {/* The student's assembled answer: their words under its label and a hairline (no mint box) */}
          <div className="ex-block">
            <p className="ex-label">
              Your Assembled SEL Answer
            </p>
            <p className="t-body text-ink-primary">
              {assembledAnswer}
            </p>
          </div>
          <div className="ex-actions">
            <Button onClick={handleNextScenario}>
              {scenarioIdx < ABQ_SCENARIOS.length - 1 ? 'Next Scenario \u2192' : 'Finish \u2713'}
            </Button>
          </div>
        </MotionDiv>
      ) : (
        <div className="ex-list">
          {STEP_LABELS.map((label, i) => {
            const isActive = i === stepIdx;
            const isDone = revealed[i];
            const isLocked = i > stepIdx;
            const quality = isDone ? checkQuality(inputs[i], i) : null;
            // The step's mark: green once the answer is checked and good, ink while it is the current
            // step, a hairline ring otherwise (was a green, amber or black border and shadow round the step)
            const badgeClass =
              quality === 'good'
                ? 'ex-badge ex-badge--done'
                : isActive
                ? 'ex-badge ex-badge--on'
                : 'ex-badge';

            return (
              <MotionDiv
                key={label}
                initial={{ opacity: 0, y: 10 }}
                animate={{ opacity: isLocked ? 0.4 : 1, y: 0 }}
                transition={{ delay: i * 0.08 }}
              >
                <div className="ex-stack">
                {/* Step header */}
                <div className="flex items-center gap-3">
                  <span className={badgeClass}>
                    {i + 1}
                  </span>
                  <span id={`${stepId}-label-${i}`} className="ex-label">
                    {label}
                  </span>
                </div>

                {isActive && (
                  <MotionDiv
                    initial={{ opacity: 0, height: 0 }}
                    animate={{ opacity: 1, height: 'auto' }}
                    className="overflow-hidden ex-stack"
                  >
                    <p id={`${stepId}-instr-${i}`} className="t-sub">
                      {STEP_INSTRUCTIONS[i]}
                    </p>
                    <AreaField
                      aria-labelledby={`${stepId}-label-${i} ${stepId}-instr-${i}`}
                      value={inputs[i]}
                      onChange={(e) => handleInputChange(e.target.value)}
                      rows={3}
                      placeholder={`Write your ${label} here...`}
                    />
                    {!isDone && (
                      <div>
                        <Button
                          onClick={handleReveal}
                          {...{ disabled: inputs[i].trim().length < 10 }}
                          className="disabled:opacity-40"
                        >
                          Check Against Model
                        </Button>
                      </div>
                    )}
                  </MotionDiv>
                )}

                {isDone && (
                  <MotionDiv
                    initial={{ opacity: 0, y: 6 }}
                    animate={{ opacity: 1, y: 0 }}
                    className="ex-stack"
                  >
                    {/* Show user input if not active step */}
                    {!isActive && (
                      <p className="t-sub">
                        {inputs[i]}
                      </p>
                    )}
                    {/* The model answer: its label and words under a hairline (no mint box) */}
                    <div className="ex-block">
                      <p className="ex-label">
                        Model Answer
                      </p>
                      <p className="ex-block-text">
                        {scenario.models[label.toLowerCase() as 'state' | 'explain' | 'link']}
                      </p>
                    </div>
                    {isActive && (
                      <div>
                        <Button onClick={handleNext}>
                          {stepIdx < 2 ? 'Continue to next step \u2192' : 'See assembled answer'}
                        </Button>
                      </div>
                    )}
                  </MotionDiv>
                )}
                </div>
              </MotionDiv>
            );
          })}
        </div>
      )}
    </ExerciseSheet>
  );
};

// --- MODULE COMPONENT ---
const MasteringBusinessModule: React.FC<{ onBack: () => void; progress: ModuleProgress; onProgressUpdate: (progress: ModuleProgress) => void }> = ({ onBack, progress, onProgressUpdate }) => {
  const essentials = useEssentialsMode();
  const sections = [
    { id: 'strategic-context', title: 'What You Need to Know for 2026', eyebrow: '01 // The Big Picture', icon: Key },
    { id: 'exam-architecture', title: 'How the Paper Works', eyebrow: '02 // The Layout', icon: PieChart },
    { id: 'abq-deep-dive', title: 'ABQ Deep Dive', eyebrow: '03 // The Game-Changer', icon: Briefcase },
    { id: 'science-of-scoring', title: 'How to Pick Up Every Mark', eyebrow: '04 // Getting Better Marks', icon: FileText },
    { id: 'high-yield-tactics', title: 'Quick Wins and Smart Moves', eyebrow: '05 // The Toolkit', icon: Wrench },
    { id: 'study-blueprint', title: 'Your Study Plan', eyebrow: '06 // The Action Plan', icon: BrainCircuit },
  ];

  return (
    <ModuleLayout
      moduleNumber="05"
      moduleTitle="Mastering Business"
      moduleSubtitle="Your Complete Guide to Getting Top Marks"
      moduleDescription={`Everything you need to crack the 2026 Business exam -- from the ABQ to the action words and the SEE/SEEE answer structure that examiners actually reward.`}
      theme={theme}
      sections={sections}
      onBack={onBack}
      progress={progress}
      onProgressUpdate={onProgressUpdate}
    >
      {(activeSection) => (
        <>
          {activeSection === 0 && (
            <ReadingSection title="What You Need to Know for 2026." eyebrow="Step 1" icon={Key} theme={theme}>
              {essentials ? (<>
              <p>Know <Highlight description="Understanding how the exam works, what the questions are really asking, and what the examiner wants to see in your answer." theme={theme}>how the exam works</Highlight>. For 2026, the compulsory ABQ covers Units 3, 4, and 5: management, HR, finance, and marketing. These topics will definitely come up. Be strong on them and you are halfway to top marks.</p>
              </>) : (<>
              <p>The Leaving Cert Business exam is not just about remembering facts -- it is about knowing <Highlight description="Understanding how the exam works, what the questions are really asking, and what the examiner wants to see in your answer." theme={theme}>how the exam actually works</Highlight>. For 2026, the big thing to know is that the compulsory Applied Business Question (ABQ) will be based on <strong>Units 3, 4, and 5</strong>.</p>
              <p>That means the focus is on the inside of a business: management, HR, finance, and marketing. You cannot dodge these topics -- they will definitely come up. If you are strong on these units, you are already halfway to top marks.</p>
              </>)}
            </ReadingSection>
          )}
           {activeSection === 1 && (
            <ReadingSection title="How the Paper Works." eyebrow="Step 2" icon={PieChart} theme={theme}>
              {essentials ? (<>
              <p>Three sections: Short Questions (20%, easy marks), ABQ (20%, case study), Long Questions (60%, four full answers). Smart tip: do the ABQ right after Short Questions while your brain is fresh. Do not save it until you are tired.</p>
              </>) : (<>
              <p>The Higher Level paper is 3 hours long and split into three sections. <strong>Section 1 (Short Questions)</strong> is your easiest marks -- worth 20% of the total and you can fly through them. <strong>Section 2 (ABQ)</strong> is the big one, also worth 20%, where you apply theory to a case study. <strong>Section 3 (Long Questions)</strong> is the main event, worth 60% of the marks -- you need to write four full answers.</p>
              <p>Here is a smart timing tip: do the ABQ right after the Short Questions. Your brain is still fresh at that point, and you will write better answers than if you leave it until you are tired from the long questions.</p>
              </>)}
            </ReadingSection>
          )}
           {activeSection === 2 && (
            <ReadingSection title="ABQ Deep Dive." eyebrow="Step 3" icon={Briefcase} theme={theme}>
                {essentials ? (<>
                <p>The ABQ gives you a business case study to solve. The number one rule: <Highlight description="The must-use 3-step formula for ABQ answers: say what the theory is, explain it in your own words, then quote directly from the case study to prove it." theme={theme}>State, Explain, Link</Highlight>. Name the theory. Explain it. Then quote directly from the case study. Every answer needs a direct quote. Forgetting to quote is the biggest reason students lose marks.</p>
                </>) : (<>
                <p>The 2026 ABQ will probably give you a business that is growing fast but running into problems -- things like staff issues, money troubles, or communication breakdowns. Your job is to read the case study and use your business theory to solve their problems.</p>
                <p>The number one rule is <Highlight description="The must-use 3-step formula for ABQ answers: say what the theory is, explain it in your own words, then quote directly from the case study to prove it." theme={theme}>State, Explain, Link</Highlight>. The biggest reason students lose marks is forgetting to quote directly from the case study. Every single answer needs a direct quote. Think of it as a simple 3-step recipe: name the theory, explain it, then prove it with words from the text.</p>
                </>)}
                <ABQLinkDrill />
                <ABQAnswerScaffold />
            </ReadingSection>
          )}
           {activeSection === 3 && (
            <ReadingSection title="How to Pick Up Every Mark." eyebrow="Step 4" icon={FileText} theme={theme}>
              {essentials ? (<>
              <p>Use the <Highlight description="A 3-step formula for each point: State it, Explain it, then give an Example. This is how you make sure the examiner can give you full marks." theme={theme}>SEE</Highlight> formula: State, Explain, Example. For a H1, use <Highlight description="The H1 version where you write two sentences of explanation instead of one, so the examiner has no excuse not to give you the marks." theme={theme}>SEEE</Highlight> with two explanation sentences. Watch the <Highlight description="The action word in the question (like State, Explain, or Evaluate) that tells you exactly how much detail the examiner expects. Get this wrong and you will either write too little or waste time." theme={theme}>action word</Highlight>: "State" means list it. "Explain" means define it. "Evaluate" means give your opinion with evidence. Always label evaluations clearly.</p>
              </>) : (<>
              <p>To get top marks, you need to write the way the examiner wants to see it. Each "point" in a long question is worth 5 marks. The way to guarantee those marks is a simple formula called <Highlight description="A 3-step formula for each point: State it, Explain it, then give an Example. This is how you make sure the examiner can give you full marks." theme={theme}>SEE</Highlight> -- State, Explain, Example. If you are aiming for a H1, use the upgraded version called <Highlight description="The H1 version where you write two sentences of explanation instead of one, so the examiner has no excuse not to give you the marks." theme={theme}>SEEE</Highlight>, where you give two explanation sentences instead of one.</p>
              <p>You also need to pay attention to the <Highlight description="The action word in the question (like State, Explain, or Evaluate) that tells you exactly how much detail the examiner expects. Get this wrong and you will either write too little or waste time." theme={theme}>action word</Highlight> in each question. "State" means just list the point. "Explain" means define it properly. "Evaluate" means give your opinion on whether it is good or bad -- and this is what separates H1 answers from the rest. When you see "Evaluate," always write a separate mini-paragraph starting with <strong>"Evaluation:"</strong> to make sure you grab those marks.</p>
              </>)}
            </ReadingSection>
          )}
          {activeSection === 4 && (
            <ReadingSection title="Quick Wins and Smart Moves." eyebrow="Step 5" icon={Wrench} theme={theme}>
              {essentials ? (<>
              <p>Section 1: use the <Highlight description="Answer every short question on the paper, even the ones you are unsure about. Only your best answers count, so extra attempts are free insurance." theme={theme}>answer-everything approach</Highlight>. Do all short questions. Only your best count. Section 3: avoid <Highlight description="Writing long paragraphs that sound nice but do not actually contain any real business terms or facts. The examiner cannot give marks for waffle." theme={theme}>waffle</Highlight> and <Highlight description="Saying the same thing twice in different words. The examiner will only give you marks for a point once, no matter how you phrase it." theme={theme}>repeating yourself</Highlight>. Make each point genuinely different: one about money, one about marketing, one about staff.</p>
              </>) : (<>
              <p>In Section 1 (Short Questions), use the <Highlight description="Answer every short question on the paper, even the ones you are unsure about. Only your best answers count, so extra attempts are free insurance." theme={theme}>answer-everything approach</Highlight>: do all the short questions, not just the required number. Only your best answers count, so extra attempts cost you almost no time and protect you if you slip up on one.</p>
              <p>In Section 3 (Long Questions), the biggest marks-killer is <Highlight description="Writing long paragraphs that sound nice but do not actually contain any real business terms or facts. The examiner cannot give marks for waffle." theme={theme}>waffle</Highlight> -- writing loads without actually saying anything specific. Stick to the SEEE structure so every sentence earns marks. Also watch out for <Highlight description="Saying the same thing twice in different words. The examiner will only give you marks for a point once, no matter how you phrase it." theme={theme}>repeating yourself</Highlight> when asked for multiple "impacts" or "benefits." Make sure each point is genuinely different -- for example, one about money, one about marketing, one about staff.</p>
              </>)}
              <PersonalStory name="Roisin" role="6th Year, Limerick">
                <p>I used to lose marks on the long questions because I would basically say the same thing three different ways. Once I started labelling my points (financial impact, marketing impact, staffing impact) I actually started getting full marks. It sounds simple but it made a huge difference.</p>
              </PersonalStory>
            </ReadingSection>
          )}
           {activeSection === 5 && (
            <ReadingSection title="Your Study Plan." eyebrow="Step 6" icon={BrainCircuit} theme={theme}>
              {essentials ? (<>
              <p>Use <Highlight description="Testing yourself from memory instead of just re-reading. It feels harder, but it is by far the best way to make things stick." theme={theme}>active recall</Highlight>: test yourself instead of re-reading. Use spider diagrams and flashcards. Break study into three phases below.</p>
              </>) : (<>
              <p>Just reading over your notes does not work -- you forget most of it within a day. The trick is <Highlight description="Testing yourself from memory instead of just re-reading. It feels harder, but it is by far the best way to make things stick." theme={theme}>active recall</Highlight> -- actually testing yourself. Use spider diagrams and flashcards to pull information out of your head, not just put it in.</p>
              <p>Break your study into three phases:</p>
              </>)}
              {/* The three phases: numbered lines on the page (were three coloured boxes) */}
              <ol className="ex-nums">
                <li>
                  <span className="ex-num">1</span>
                  <div className="ex-num-copy">
                    <p className="ex-num-title">Phase 1 (Sept-Dec)</p>
                    <p className="ex-num-sub">Focus hard on the ABQ units (3, 4, 5) since these are guaranteed to come up.</p>
                  </div>
                </li>
                <li>
                  <span className="ex-num">2</span>
                  <div className="ex-num-copy">
                    <p className="ex-num-title">Phase 2 (Jan-Mar)</p>
                    <p className="ex-num-sub">Cover the other units and start doing timed long questions.</p>
                  </div>
                </li>
                <li>
                  <span className="ex-num">3</span>
                  <div className="ex-num-copy">
                    <p className="ex-num-title">Phase 3 (Apr-May)</p>
                    <p className="ex-num-sub">Do <Highlight description="Mixing questions from different units in a single study session. This trains you to recognise what topic is being asked about, just like in the real exam." theme={theme}>mixed practice</Highlight> with past papers -- mix up the topics so you are ready for anything the exam throws at you.</p>
                  </div>
                </li>
              </ol>
               <MicroCommitment theme={theme}>
                <p>Go to your Business notes. Pick one topic. Create a one-page spider diagram summary of it from memory -- no peeking. Then open the book and check what you missed. That is active recall in action, and you have just done it.</p>
              </MicroCommitment>
            </ReadingSection>
          )}
        </>
      )}
    </ModuleLayout>
  );
};
export default MasteringBusinessModule;
