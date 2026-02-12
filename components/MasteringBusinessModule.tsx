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
  const MotionDiv = motion.div as any;

  return (
    <div className="my-10 p-8 md:p-12 bg-white dark:bg-zinc-800 rounded-xl border border-zinc-200 dark:border-zinc-700">
      <h4 className="font-serif text-2xl font-semibold text-zinc-800 dark:text-white text-center">
        ABQ Answer Builder
      </h4>
      <p className="text-center text-sm text-zinc-500 dark:text-zinc-400 mt-2">
        Master the State &rarr; Explain &rarr; Link formula that the examiner rewards.
      </p>
      <p className="text-center text-xs text-zinc-400 dark:text-zinc-500 mt-1 font-medium">
        Scenario {scenarioIdx + 1} / {ABQ_SCENARIOS.length}
      </p>

      {/* Case extract */}
      <div className="mt-8 p-5 bg-zinc-50 dark:bg-zinc-900 rounded-lg border-l-4 border-zinc-400 dark:border-zinc-500">
        <p className="text-xs font-bold uppercase tracking-wider text-zinc-400 dark:text-zinc-500 mb-2">
          Case Extract
        </p>
        <p className="text-sm text-zinc-700 dark:text-zinc-300 italic leading-relaxed">
          {scenario.extract}
        </p>
      </div>

      {/* Theory prompt */}
      <p className="mt-5 text-sm font-bold text-zinc-800 dark:text-white">
        {scenario.prompt}
      </p>

      {allDone ? (
        <MotionDiv
          initial={{ opacity: 0, y: 12 }}
          animate={{ opacity: 1, y: 0 }}
          className="mt-8 p-6 bg-emerald-50 dark:bg-emerald-900/30 rounded-xl border border-emerald-200 dark:border-emerald-700"
        >
          <p className="text-sm font-semibold text-emerald-800 dark:text-emerald-300 text-center">
            All 3 scenarios complete.
          </p>
          <p className="text-sm text-zinc-700 dark:text-zinc-300 mt-3 leading-relaxed text-center">
            The ABQ is worth <strong>80 marks</strong> &mdash; nearly a quarter of the paper. The
            State-Explain-Link structure is non-negotiable. Every answer without a direct quote from
            the case study is leaving marks on the table.
          </p>
        </MotionDiv>
      ) : completed ? (
        <MotionDiv
          initial={{ opacity: 0, y: 12 }}
          animate={{ opacity: 1, y: 0 }}
          className="mt-8"
        >
          <p className="text-xs font-bold uppercase tracking-wider text-zinc-400 dark:text-zinc-500 mb-3">
            Your Assembled SEL Answer
          </p>
          <div className="p-5 bg-emerald-50 dark:bg-emerald-900/20 rounded-xl border border-emerald-200 dark:border-emerald-700">
            <p className="text-sm text-zinc-800 dark:text-zinc-200 leading-relaxed">
              {assembledAnswer}
            </p>
          </div>
          <div className="flex justify-center mt-6">
            <button
              onClick={handleNextScenario}
              className="px-5 py-2.5 bg-zinc-800 dark:bg-zinc-200 text-white dark:text-zinc-900 text-xs font-bold rounded-lg hover:opacity-90 transition-opacity"
            >
              {scenarioIdx < ABQ_SCENARIOS.length - 1 ? 'Next Scenario \u2192' : 'Finish \u2713'}
            </button>
          </div>
        </MotionDiv>
      ) : (
        <div className="mt-6 space-y-4">
          {STEP_LABELS.map((label, i) => {
            const isActive = i === stepIdx;
            const isDone = revealed[i];
            const isLocked = i > stepIdx;
            const quality = isDone ? checkQuality(inputs[i], i) : null;
            const borderColor =
              quality === 'good'
                ? 'border-emerald-400 dark:border-emerald-500'
                : quality === 'partial'
                ? 'border-amber-400 dark:border-amber-500'
                : 'border-zinc-200 dark:border-zinc-700';

            return (
              <MotionDiv
                key={label}
                initial={{ opacity: 0, y: 10 }}
                animate={{ opacity: isLocked ? 0.4 : 1, y: 0 }}
                transition={{ delay: i * 0.08 }}
                className={`p-5 rounded-xl border-2 ${borderColor} bg-white dark:bg-zinc-800 transition-colors`}
              >
                {/* Step header */}
                <div className="flex items-center gap-3 mb-3">
                  <span className="flex items-center justify-center w-7 h-7 rounded-full bg-zinc-800 dark:bg-zinc-200 text-white dark:text-zinc-900 text-xs font-bold">
                    {i + 1}
                  </span>
                  <span className="text-xs font-bold uppercase tracking-wider text-zinc-500 dark:text-zinc-400">
                    {label}
                  </span>
                </div>

                {isActive && (
                  <MotionDiv
                    initial={{ opacity: 0, height: 0 }}
                    animate={{ opacity: 1, height: 'auto' }}
                    className="overflow-hidden"
                  >
                    <p className="text-xs text-zinc-500 dark:text-zinc-400 mb-3">
                      {STEP_INSTRUCTIONS[i]}
                    </p>
                    <textarea
                      value={inputs[i]}
                      onChange={(e) => handleInputChange(e.target.value)}
                      rows={3}
                      placeholder={`Write your ${label} here...`}
                      className="w-full p-3 text-sm bg-zinc-50 dark:bg-zinc-900 border border-zinc-200 dark:border-zinc-700 rounded-lg text-zinc-800 dark:text-zinc-200 placeholder-zinc-400 dark:placeholder-zinc-500 focus:outline-none focus:ring-2 focus:ring-zinc-400 dark:focus:ring-zinc-500 resize-none"
                    />
                    {!isDone && (
                      <button
                        onClick={handleReveal}
                        disabled={inputs[i].trim().length < 10}
                        className="mt-3 px-4 py-2 bg-zinc-800 dark:bg-zinc-200 text-white dark:text-zinc-900 text-xs font-bold rounded-lg disabled:opacity-40 hover:opacity-90 transition-opacity"
                      >
                        Check Against Model
                      </button>
                    )}
                  </MotionDiv>
                )}

                {isDone && (
                  <MotionDiv
                    initial={{ opacity: 0, y: 6 }}
                    animate={{ opacity: 1, y: 0 }}
                  >
                    {/* Show user input if not active step */}
                    {!isActive && (
                      <p className="text-sm text-zinc-600 dark:text-zinc-400 mb-3 italic">
                        {inputs[i]}
                      </p>
                    )}
                    <div className="p-4 bg-emerald-50 dark:bg-emerald-900/20 rounded-lg border border-emerald-200 dark:border-emerald-700">
                      <p className="text-xs font-bold uppercase tracking-wider text-emerald-600 dark:text-emerald-400 mb-1">
                        Model Answer
                      </p>
                      <p className="text-sm text-zinc-700 dark:text-zinc-300 leading-relaxed">
                        {scenario.models[label.toLowerCase() as 'state' | 'explain' | 'link']}
                      </p>
                    </div>
                    {isActive && (
                      <button
                        onClick={handleNext}
                        className="mt-3 px-4 py-2 bg-zinc-800 dark:bg-zinc-200 text-white dark:text-zinc-900 text-xs font-bold rounded-lg hover:opacity-90 transition-opacity"
                      >
                        {stepIdx < 2 ? 'Continue to next step \u2192' : 'See assembled answer'}
                      </button>
                    )}
                  </MotionDiv>
                )}
              </MotionDiv>
            );
          })}
        </div>
      )}
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
      moduleSubtitle="The Grade Optimization Protocol"
      moduleDescription={`Deconstruct the Business exam for 2026, focusing on the ABQ, "outcome verbs", and the "SEE/SEEE" structure to engineer a H1.`}
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
              <p>The Leaving Cert Business exam isn't a test of memory; it's a test of <Highlight description="The ability to decode the specific rules and expectations of the exam, from timing to the precise meaning of 'outcome verbs'." theme={theme}>examination literacy</Highlight>. For 2026, the game is defined by one critical fact: the compulsory Applied Business Question (ABQ) will be based on <strong>Units 3, 4, and 5</strong>.</p>
              <p>This is your strategic roadmap. It shifts the focus from the wider economy to the "engine room" of a business: management, HR, finance, and marketing. A weakness in these units cannot be hidden, making the ABQ the primary filter for H1 candidates.</p>
            </ReadingSection>
          )}
           {activeSection === 1 && (
            <ReadingSection title="The Exam Architecture." eyebrow="Step 2" icon={PieChart} theme={theme}>
              <p>The 3-hour Higher Level paper is an endurance test split into three sections. <strong>Section 1 (Shorts)</strong> is your "return on investment" section, worth 20% of the marks for about 15% of the time. <strong>Section 2 (ABQ)</strong> is your high-risk, high-reward section, also worth 20%. <strong>Section 3 (Longs)</strong> is the marathon, worth 60% of the marks and requiring four full answers.</p>
              <p>Your timing strategy is critical. A common H1 approach is to tackle the ABQ immediately after the Shorts to leverage mental freshness before the fatigue of the long questions sets in.</p>
            </ReadingSection>
          )}
           {activeSection === 2 && (
            <ReadingSection title="ABQ Deep Dive." eyebrow="Step 3" icon={Briefcase} theme={theme}>
                <p>The 2026 ABQ will almost certainly feature a business in a "growth crisis"--a company that has launched successfully but is struggling with internal chaos. You will act as a consultant. Your job is to apply theory to solve their problems.</p>
                <p>The golden rule is the <Highlight description="The non-negotiable, 3-part structure for ABQ answers: State the theory, Explain it in your own words, and Link it with a direct quote from the text." theme={theme}>"Link" Methodology</Highlight>. Failure to quote directly from the case study is the single biggest cause of lost marks. It's a mechanical process: State, Explain, Link. Master this algorithm.</p>
                <ABQLinkDrill />
                <ABQAnswerScaffold />
            </ReadingSection>
          )}
           {activeSection === 3 && (
            <ReadingSection title="The Science of Scoring." eyebrow="Step 4" icon={FileText} theme={theme}>
              <p>To get a H1, you must write for the examiner. The marking scheme is a rigid code. The standard unit of currency is the "point," worth 5 marks in a long question. To secure these marks, you must use a structured formula: <Highlight description="The standard formula for a 5-mark point: State the point, Explain it, and give an Example." theme={theme}>"SEE"</Highlight>. For a H1, you need the advanced <Highlight description="The H1 version of the formula, expanding the 'Explain' part into two distinct sentences to ensure full marks are captured." theme={theme}>"SEEE"</Highlight> version.</p>
              <p>You must also decode the <Highlight description="The specific verb used by the SEC in a question (e.g., State, Explain, Evaluate) which dictates the required depth and structure of your answer." theme={theme}>"Outcome Verb."</Highlight> "State" requires a list. "Explain" requires a definition. "Evaluate" requires a judgment, which is the key differentiator for top grades. Always add a separate mini-paragraph explicitly labelled <strong>"Evaluation:"</strong> to secure these marks.</p>
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
              <p>Your study plan should be phased. <strong>Phase 1 (Sept-Dec):</strong> Deep dive on the ABQ units (3, 4, 5). <strong>Phase 2 (Jan-Mar):</strong> Cover the other units and begin timed long questions. <strong>Phase 3 (Apr-May):</strong> Use <Highlight description="Mixing questions from different units in a single study session to simulate the randomness of the exam and train your problem-spotting skills." theme={theme}>"Interleaved" Practice</Highlight> with past papers. This is not about just learning the material; it's about learning how to perform.</p>
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
