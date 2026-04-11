/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
*/

import React, { useState } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { MotionDiv } from './Motion';
import {
  Key, PieChart, Briefcase, FileText, BrainCircuit, Wrench
} from 'lucide-react';
import { type ModuleProgress } from '../types';
import { grayTheme } from '../moduleThemes';
import { Highlight, ReadingSection, MicroCommitment, PersonalStory } from './ModuleShared';
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
        <div className="my-10 rounded-2xl p-6 md:p-8" style={{ backgroundColor: '#F8F8F8', borderRadius: 18 }}>
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


  return (
    <div className="my-10 rounded-2xl p-6 md:p-8" style={{ backgroundColor: '#F8F8F8', borderRadius: 18 }}>
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
      <div className="mt-8 p-5 bg-zinc-50 dark:bg-zinc-900 rounded-lg" style={{ borderLeft: '4px solid #A1A1AA' }}>
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
            const shadowColor =
              quality === 'good'
                ? '#059669'
                : quality === 'partial'
                ? '#D97706'
                : '#1C1917';
            const borderColorHex =
              quality === 'good'
                ? '#059669'
                : quality === 'partial'
                ? '#D97706'
                : '#1C1917';

            return (
              <MotionDiv
                key={label}
                initial={{ opacity: 0, y: 10 }}
                animate={{ opacity: isLocked ? 0.4 : 1, y: 0 }}
                transition={{ delay: i * 0.08 }}
                className="p-5 rounded-xl transition-colors"
                style={{ backgroundColor: '#FFFFFF', border: `2px solid ${borderColorHex}`, borderRadius: 14, boxShadow: `3px 3px 0px 0px ${shadowColor}` }}
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
                      className="w-full bg-white dark:bg-zinc-800 rounded-xl px-5 py-3.5 text-sm font-medium text-zinc-800 dark:text-white placeholder-zinc-400 outline-none resize-none" style={{ border: '1.5px solid #E7E5E4' }}
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
              <p>The Leaving Cert Business exam is not just about remembering facts -- it is about knowing <Highlight description="Understanding how the exam works, what the questions are really asking, and what the examiner wants to see in your answer." theme={theme}>how the exam actually works</Highlight>. For 2026, the big thing to know is that the compulsory Applied Business Question (ABQ) will be based on <strong>Units 3, 4, and 5</strong>.</p>
              <p>That means the focus is on the inside of a business: management, HR, finance, and marketing. You cannot dodge these topics -- they will definitely come up. If you are strong on these units, you are already halfway to top marks.</p>
            </ReadingSection>
          )}
           {activeSection === 1 && (
            <ReadingSection title="How the Paper Works." eyebrow="Step 2" icon={PieChart} theme={theme}>
              <p>The Higher Level paper is 3 hours long and split into three sections. <strong>Section 1 (Short Questions)</strong> is your easiest marks -- worth 20% of the total and you can fly through them. <strong>Section 2 (ABQ)</strong> is the big one, also worth 20%, where you apply theory to a case study. <strong>Section 3 (Long Questions)</strong> is the main event, worth 60% of the marks -- you need to write four full answers.</p>
              <p>Here is a smart timing tip: do the ABQ right after the Short Questions. Your brain is still fresh at that point, and you will write better answers than if you leave it until you are tired from the long questions.</p>
            </ReadingSection>
          )}
           {activeSection === 2 && (
            <ReadingSection title="ABQ Deep Dive." eyebrow="Step 3" icon={Briefcase} theme={theme}>
                <p>The 2026 ABQ will probably give you a business that is growing fast but running into problems -- things like staff issues, money troubles, or communication breakdowns. Your job is to read the case study and use your business theory to solve their problems.</p>
                <p>The number one rule is <Highlight description="The must-use 3-step formula for ABQ answers: say what the theory is, explain it in your own words, then quote directly from the case study to prove it." theme={theme}>State, Explain, Link</Highlight>. The biggest reason students lose marks is forgetting to quote directly from the case study. Every single answer needs a direct quote. Think of it as a simple 3-step recipe: name the theory, explain it, then prove it with words from the text.</p>
                <ABQLinkDrill />
                <ABQAnswerScaffold />
            </ReadingSection>
          )}
           {activeSection === 3 && (
            <ReadingSection title="How to Pick Up Every Mark." eyebrow="Step 4" icon={FileText} theme={theme}>
              <p>To get top marks, you need to write the way the examiner wants to see it. Each "point" in a long question is worth 5 marks. The way to guarantee those marks is a simple formula called <Highlight description="A 3-step formula for each point: State it, Explain it, then give an Example. This is how you make sure the examiner can give you full marks." theme={theme}>SEE</Highlight> -- State, Explain, Example. If you are aiming for a H1, use the upgraded version called <Highlight description="The H1 version where you write two sentences of explanation instead of one, so the examiner has no excuse not to give you the marks." theme={theme}>SEEE</Highlight>, where you give two explanation sentences instead of one.</p>
              <p>You also need to pay attention to the <Highlight description="The action word in the question (like State, Explain, or Evaluate) that tells you exactly how much detail the examiner expects. Get this wrong and you will either write too little or waste time." theme={theme}>action word</Highlight> in each question. "State" means just list the point. "Explain" means define it properly. "Evaluate" means give your opinion on whether it is good or bad -- and this is what separates H1 answers from the rest. When you see "Evaluate," always write a separate mini-paragraph starting with <strong>"Evaluation:"</strong> to make sure you grab those marks.</p>
            </ReadingSection>
          )}
          {activeSection === 4 && (
            <ReadingSection title="Quick Wins and Smart Moves." eyebrow="Step 5" icon={Wrench} theme={theme}>
              <p>In Section 1 (Short Questions), use the <Highlight description="Answer every short question on the paper, even the ones you are unsure about. Only your best answers count, so extra attempts are free insurance." theme={theme}>answer-everything approach</Highlight>: do all the short questions, not just the required number. Only your best answers count, so extra attempts cost you almost no time and protect you if you slip up on one.</p>
              <p>In Section 3 (Long Questions), the biggest marks-killer is <Highlight description="Writing long paragraphs that sound nice but do not actually contain any real business terms or facts. The examiner cannot give marks for waffle." theme={theme}>waffle</Highlight> -- writing loads without actually saying anything specific. Stick to the SEEE structure so every sentence earns marks. Also watch out for <Highlight description="Saying the same thing twice in different words. The examiner will only give you marks for a point once, no matter how you phrase it." theme={theme}>repeating yourself</Highlight> when asked for multiple "impacts" or "benefits." Make sure each point is genuinely different -- for example, one about money, one about marketing, one about staff.</p>
              <PersonalStory name="Roisin" role="6th Year, Limerick">
                <p>I used to lose marks on the long questions because I would basically say the same thing three different ways. Once I started labelling my points (financial impact, marketing impact, staffing impact) I actually started getting full marks. It sounds simple but it made a huge difference.</p>
              </PersonalStory>
            </ReadingSection>
          )}
           {activeSection === 5 && (
            <ReadingSection title="Your Study Plan." eyebrow="Step 6" icon={BrainCircuit} theme={theme}>
              <p>Just reading over your notes does not work -- you forget most of it within a day. The trick is <Highlight description="Testing yourself from memory instead of just re-reading. It feels harder, but it is by far the best way to make things stick." theme={theme}>active recall</Highlight> -- actually testing yourself. Use spider diagrams and flashcards to pull information out of your head, not just put it in.</p>
              <p>Break your study into three phases:</p>
              <div className="my-10 rounded-2xl p-5 md:p-6 space-y-3" style={{ backgroundColor: '#F8F8F8', borderRadius: 18 }}>
                <div className="p-4 flex items-start gap-4" style={{ backgroundColor: '#93C5FD', border: '2.5px solid #2563EB', borderRadius: 16, boxShadow: '4px 4px 0px 0px #2563EB' }}>
                  <div className="w-11 h-11 rounded-xl flex items-center justify-center shrink-0 text-lg font-serif font-bold text-white" style={{ backgroundColor: '#2563EB' }}>1</div>
                  <div>
                    <p className="text-sm font-bold" style={{ color: '#1E3A8A' }}>Phase 1 (Sept-Dec)</p>
                    <p className="text-[13px] mt-0.5" style={{ color: '#1E3A8A', opacity: 0.8 }}>Focus hard on the ABQ units (3, 4, 5) since these are guaranteed to come up.</p>
                  </div>
                </div>
                <div className="p-4 flex items-start gap-4" style={{ backgroundColor: '#FCD34D', border: '2.5px solid #D97706', borderRadius: 16, boxShadow: '4px 4px 0px 0px #D97706' }}>
                  <div className="w-11 h-11 rounded-xl flex items-center justify-center shrink-0 text-lg font-serif font-bold text-white" style={{ backgroundColor: '#D97706' }}>2</div>
                  <div>
                    <p className="text-sm font-bold" style={{ color: '#78350F' }}>Phase 2 (Jan-Mar)</p>
                    <p className="text-[13px] mt-0.5" style={{ color: '#78350F', opacity: 0.8 }}>Cover the other units and start doing timed long questions.</p>
                  </div>
                </div>
                <div className="p-4 flex items-start gap-4" style={{ backgroundColor: '#FDBA74', border: '2.5px solid #EA580C', borderRadius: 16, boxShadow: '4px 4px 0px 0px #EA580C' }}>
                  <div className="w-11 h-11 rounded-xl flex items-center justify-center shrink-0 text-lg font-serif font-bold text-white" style={{ backgroundColor: '#EA580C' }}>3</div>
                  <div>
                    <p className="text-sm font-bold" style={{ color: '#7C2D12' }}>Phase 3 (Apr-May)</p>
                    <p className="text-[13px] mt-0.5" style={{ color: '#7C2D12', opacity: 0.8 }}>Do <Highlight description="Mixing questions from different units in a single study session. This trains you to recognise what topic is being asked about, just like in the real exam." theme={theme}>mixed practice</Highlight> with past papers -- mix up the topics so you are ready for anything the exam throws at you.</p>
                  </div>
                </div>
              </div>
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
