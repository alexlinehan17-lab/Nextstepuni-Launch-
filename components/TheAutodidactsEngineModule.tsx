
/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
*/

import React, { useState } from 'react';
import { AnimatePresence } from 'framer-motion';
import { MotionDiv } from './Motion';
import {
  SlidersHorizontal, Repeat, Brain, BookOpen, PenSquare, Wrench, Highlighter
} from 'lucide-react';
import { type ModuleProgress } from '../types';
import { cyanTheme } from '../moduleThemes';
import { Highlight, ReadingSection, MicroCommitment } from './ModuleShared';
import { ModuleLayout } from './ModuleLayout';

const theme = cyanTheme;

// --- INTERACTIVE COMPONENTS ---

interface SplitPageProblem {
  title: string;
  equation: string;
  steps: {
    prompt: string;
    expert: string;
    keywords: string[];
  }[];
}

const PROBLEMS: SplitPageProblem[] = [
  {
    title: 'Quadratic Equation',
    equation: 'Solve: 2x\u00B2 + 5x \u2212 3 = 0',
    steps: [
      { prompt: 'Identify a, b, and c', expert: 'a = 2, b = 5, c = \u22123', keywords: ['2', '5', '-3'] },
      { prompt: 'Write the quadratic formula', expert: 'x = (\u2212b \u00B1 \u221A(b\u00B2\u22124ac)) / 2a', keywords: ['b', '4ac', '2a', '\u00B1'] },
      { prompt: 'Substitute values', expert: 'x = (\u22125 \u00B1 \u221A(25 + 24)) / 4', keywords: ['-5', '25', '24', '4'] },
      { prompt: 'Simplify under the root', expert: 'x = (\u22125 \u00B1 \u221A49) / 4 = (\u22125 \u00B1 7) / 4', keywords: ['49', '7', '-5'] },
      { prompt: 'Find both solutions', expert: 'x = 2/4 = 0.5  or  x = \u221212/4 = \u22123', keywords: ['0.5', '-3'] },
    ],
  },
  {
    title: 'Simultaneous Equations',
    equation: 'Solve: 3x + 2y = 12  and  x \u2212 y = 1',
    steps: [
      { prompt: 'Rearrange the second equation for x', expert: 'x = 1 + y', keywords: ['1', 'y', 'x'] },
      { prompt: 'Substitute into the first equation', expert: '3(1 + y) + 2y = 12 \u2192 3 + 3y + 2y = 12', keywords: ['1', 'y', '12', '3y', '2y'] },
      { prompt: 'Solve for y', expert: '5y = 9 \u2192 y = 9/5 = 1.8', keywords: ['5y', '9', '1.8'] },
      { prompt: 'Back-substitute to find x', expert: 'x = 1 + 1.8 = 2.8', keywords: ['2.8', '1.8'] },
      { prompt: 'State the full solution', expert: 'x = 2.8, y = 1.8', keywords: ['2.8', '1.8'] },
    ],
  },
];

const SplitPageSimulator = () => {
  const [problemIndex, setProblemIndex] = useState(0);
  const [userInputs, setUserInputs] = useState<string[]>(['', '', '', '', '']);
  const [revealed, setRevealed] = useState<boolean[]>([false, false, false, false, false]);
  const [currentStep, setCurrentStep] = useState(0);
  const [finished, setFinished] = useState(false);

  const problem = PROBLEMS[problemIndex];

  const resetState = () => {
    setUserInputs(['', '', '', '', '']);
    setRevealed([false, false, false, false, false]);
    setCurrentStep(0);
    setFinished(false);
  };

  const handleInputChange = (index: number, value: string) => {
    const next = [...userInputs];
    next[index] = value;
    setUserInputs(next);
  };

  const handleReveal = (index: number) => {
    const next = [...revealed];
    next[index] = true;
    setRevealed(next);
    if (index < 4) {
      setCurrentStep(index + 1);
    } else {
      setFinished(true);
    }
  };

  const checkMatch = (index: number): boolean => {
    const input = userInputs[index].toLowerCase();
    const step = problem.steps[index];
    const matched = step.keywords.filter((kw) => input.includes(kw.toLowerCase()));
    return matched.length >= Math.ceil(step.keywords.length / 2);
  };

  const matchCount = problem.steps.reduce((acc, _, i) => acc + (revealed[i] && checkMatch(i) ? 1 : 0), 0);

  const switchProblem = () => {
    setProblemIndex((prev) => (prev + 1) % PROBLEMS.length);
    resetState();
  };

  return (
    <div className="my-10 rounded-2xl p-6 md:p-8" style={{ backgroundColor: '#F8F8F8', borderRadius: 18 }}>
      <h4 className="font-serif text-2xl font-semibold text-zinc-800 dark:text-white text-center">
        Split-Page Simulator
      </h4>
      <p className="text-center text-sm text-zinc-500 dark:text-zinc-400 mb-6">
        Attempt each step, then reveal the expert solution to see where your understanding breaks down.
      </p>

      {/* Problem Statement */}
      <div className="mb-8 p-5 bg-cyan-50 dark:bg-cyan-950/40 border border-cyan-200 dark:border-cyan-800 rounded-xl text-center">
        <span className="text-xs font-bold uppercase tracking-widest text-cyan-600 dark:text-cyan-400">
          {problem.title}
        </span>
        <p className="mt-2 font-mono text-lg font-semibold text-zinc-800 dark:text-white">
          {problem.equation}
        </p>
      </div>

      {/* Steps */}
      <div className="space-y-4">
        {problem.steps.map((step, i) => {
          const unlocked = i <= currentStep;
          const isRevealed = revealed[i];
          const match = isRevealed ? checkMatch(i) : null;

          return (
            <MotionDiv
              key={`${problemIndex}-${i}`}
              initial={{ opacity: 0, y: 12 }}
              animate={{ opacity: unlocked ? 1 : 0.4, y: 0 }}
              transition={{ duration: 0.3, delay: i * 0.05 }}
              className="rounded-xl p-5 transition-colors"
              style={{
                backgroundColor: isRevealed ? (match ? '#6EE7B7' : '#FCD34D') : '#FFFFFF',
                border: isRevealed ? `2.5px solid ${match ? '#059669' : '#D97706'}` : '1.5px solid #E7E5E4',
                boxShadow: !isRevealed ? 'none' : `3px 3px 0px 0px ${match ? '#059669' : '#D97706'}`,
              }}
            >
              {/* Step Header */}
              <div className="flex items-center gap-3 mb-3">
                <span
                  className={`flex-shrink-0 w-7 h-7 flex items-center justify-center rounded-full text-xs font-bold ${
                    isRevealed
                      ? match
                        ? 'bg-emerald-500 text-white'
                        : 'bg-amber-500 text-white'
                      : 'bg-zinc-200 dark:bg-zinc-700 text-zinc-600 dark:text-zinc-300'
                  }`}
                >
                  {i + 1}
                </span>
                <span className="text-sm font-semibold text-zinc-700 dark:text-zinc-200">
                  {step.prompt}
                </span>
              </div>

              {unlocked ? (
                <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                  {/* User Attempt */}
                  <div>
                    <label className="block text-xs font-bold uppercase tracking-wider text-zinc-500 dark:text-zinc-400 mb-1.5">
                      Your Attempt
                    </label>
                    <input
                      type="text"
                      value={userInputs[i]}
                      onChange={(e) => handleInputChange(i, e.target.value)}
                      disabled={isRevealed}
                      placeholder="Type your answer..."
                      className="w-full bg-white dark:bg-zinc-800 rounded-xl px-5 py-3.5 text-sm font-medium text-zinc-800 dark:text-white placeholder-zinc-400 outline-none disabled:opacity-60"
                      style={{ border: '1.5px solid #E7E5E4' }}
                    />
                  </div>

                  {/* Expert Solution / Reveal Button */}
                  <div>
                    <label className="block text-xs font-bold uppercase tracking-wider text-zinc-500 dark:text-zinc-400 mb-1.5">
                      Expert Solution
                    </label>
                    <AnimatePresence mode="wait">
                      {isRevealed ? (
                        <MotionDiv
                          key="expert"
                          initial={{ opacity: 0, x: 20 }}
                          animate={{ opacity: 1, x: 0 }}
                          transition={{ duration: 0.35 }}
                          className={`px-4 py-2.5 text-sm rounded-lg font-mono ${
                            match
                              ? 'bg-emerald-100 dark:bg-emerald-900/40 text-emerald-800 dark:text-emerald-200'
                              : 'bg-amber-100 dark:bg-amber-900/40 text-amber-800 dark:text-amber-200'
                          }`}
                        >
                          <span>{step.expert}</span>
                          {!match && (
                            <span className="block mt-1 text-xs italic text-amber-600 dark:text-amber-400">
                              Compare your approach
                            </span>
                          )}
                        </MotionDiv>
                      ) : (
                        <button
                          onClick={() => handleReveal(i)}
                          disabled={!userInputs[i].trim()}
                          className="w-full px-4 py-2.5 text-sm font-semibold rounded-lg bg-cyan-600 hover:bg-cyan-700 text-white disabled:opacity-40 disabled:cursor-not-allowed transition-colors"
                        >
                          Reveal Expert Solution
                        </button>
                      )}
                    </AnimatePresence>
                  </div>
                </div>
              ) : (
                <div className="h-10 rounded-lg bg-zinc-100 dark:bg-zinc-700/40 flex items-center justify-center">
                  <span className="text-xs text-zinc-400 dark:text-zinc-500">Complete the previous step to unlock</span>
                </div>
              )}
            </MotionDiv>
          );
        })}
      </div>

      {/* Summary */}
      <AnimatePresence>
        {finished && (
          <MotionDiv
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.5 }}
            className="mt-8 p-6 rounded-xl bg-cyan-50 dark:bg-cyan-950/30 border border-cyan-200 dark:border-cyan-800 text-center"
          >
            <p className="text-lg font-semibold text-zinc-800 dark:text-white mb-2">
              You matched {matchCount}/5 steps.
            </p>
            <p className="text-sm text-zinc-600 dark:text-zinc-300 max-w-lg mx-auto">
              The Split-Page Method forces you to try before you peek &mdash; that's the whole trick. Every mismatch shows you exactly what to work on next, not that you've failed.
            </p>
            <button
              onClick={switchProblem}
              className="mt-5 px-6 py-2.5 text-sm font-semibold rounded-lg bg-cyan-600 hover:bg-cyan-700 text-white transition-colors"
            >
              Try Another Problem
            </button>
          </MotionDiv>
        )}
      </AnimatePresence>
    </div>
  );
};

const FourHighlighterAudit = () => {
    const [activeHighlighter, setActiveHighlighter] = useState<string | null>(null);

    const highlights: { [key: string]: string[] } = {
        purpose: ['s1', 's3', 's4'],
        coherence: ['t1', 't2', 't3'],
        language: ['w1', 'w2', 'w3', 'w4', 'w5', 'w6', 'w7', 'w8'],
        mechanics: ['e1']
    };

    const isHighlighted = (id: string) => activeHighlighter && highlights[activeHighlighter]?.includes(id);

    const hl = (id: string, base: string) =>
      `${isHighlighted(id) ? base + ' px-1 rounded-sm' : ''}`;

    return (
        <div className="my-10 rounded-2xl p-6 md:p-8" style={{ backgroundColor: '#F8F8F8', borderRadius: 18 }}>
            <h4 className="font-serif text-2xl font-semibold text-zinc-800 dark:text-white text-center">The Four-Highlighter Audit</h4>
            <p className="text-center text-sm text-zinc-500 dark:text-zinc-400 mb-6">Click the highlighters to audit the paragraph below.</p>
            <div className="flex justify-center flex-wrap gap-3 mb-6">
                <button onClick={() => setActiveHighlighter(activeHighlighter === 'purpose' ? null : 'purpose')} className={`px-4 py-2 flex items-center gap-2 text-sm font-bold rounded-lg border ${activeHighlighter === 'purpose' ? 'bg-blue-500 text-white border-blue-500' : 'bg-blue-50 text-blue-800 border-blue-200'}`}> <Highlighter size={16}/> Purpose</button>
                <button onClick={() => setActiveHighlighter(activeHighlighter === 'coherence' ? null : 'coherence')} className={`px-4 py-2 flex items-center gap-2 text-sm font-bold rounded-lg border ${activeHighlighter === 'coherence' ? 'bg-green-500 text-white border-green-500' : 'bg-green-50 text-green-800 border-green-200'}`}> <Highlighter size={16}/> Coherence</button>
                <button onClick={() => setActiveHighlighter(activeHighlighter === 'language' ? null : 'language')} className={`px-4 py-2 flex items-center gap-2 text-sm font-bold rounded-lg border ${activeHighlighter === 'language' ? 'bg-yellow-400 text-yellow-900 border-yellow-500' : 'bg-yellow-50 text-yellow-800 border-yellow-200'}`}> <Highlighter size={16}/> Language</button>
                <button onClick={() => setActiveHighlighter(activeHighlighter === 'mechanics' ? null : 'mechanics')} className={`px-4 py-2 flex items-center gap-2 text-sm font-bold rounded-lg border ${activeHighlighter === 'mechanics' ? 'bg-red-500 text-white border-red-500' : 'bg-red-50 text-red-800 border-red-200'}`}> <Highlighter size={16}/> Mechanics</button>
            </div>
            <div className="p-6 rounded-xl leading-relaxed" style={{ backgroundColor: '#FFFFFF', border: '1.5px solid #E7E5E4' }}>
              <span className={hl('s1', 'bg-blue-200')}>W.B. Yeats' poem 'The Second Coming' <span className={hl('w1', 'bg-yellow-200')}>powerfully captures</span> the anxiety of a world <span className={hl('w2', 'bg-yellow-200')}>descending into chaos</span>.</span>
              {' '}
              <span><span className={hl('t1', 'bg-green-200')}>Initially</span>, the poem presents the image of a falcon <span className={hl('e1', 'bg-red-300')}>loosing</span> control, a metaphor for society's breakdown.</span>
              {' '}
              <span className={hl('s3', 'bg-blue-200')}><span className={hl('t2', 'bg-green-200')}>However</span>, Yeats then introduces the <span className={hl('w4', 'bg-yellow-200')}>terrifying 'rough beast,'</span> <span className={hl('w5', 'bg-yellow-200')}>slouching</span> towards Bethlehem. This <span className={hl('w6', 'bg-yellow-200')}>stark image</span> solidifies the poem's <span className={hl('w7', 'bg-yellow-200')}>apocalyptic vision</span>.</span>
              {' '}
              <span className={hl('s4', 'bg-blue-200')}><span className={hl('t3', 'bg-green-200')}>Therefore</span>, the poem <span className={hl('w8', 'bg-yellow-200')}>encapsulates</span> a profound sense of cultural collapse.</span>
            </div>
        </div>
    );
};

// --- MODULE COMPONENT ---
const TheAutodidactsEngineModule: React.FC<{ onBack: () => void; progress: ModuleProgress; onProgressUpdate: (progress: ModuleProgress) => void }> = ({ onBack, progress, onProgressUpdate }) => {
  const sections = [
    { id: 'practice-hierarchy', title: 'Not All Study Is Equal', eyebrow: '01 // The Big Idea', icon: SlidersHorizontal },
    { id: 'feedback-engine', title: 'How Feedback Loops Work', eyebrow: '02 // Two Key Rules', icon: Repeat },
    { id: 'maths-loop', title: 'The Maths Loop', eyebrow: '03 // Step-by-Step Practice', icon: Brain },
    { id: 'language-loop', title: 'The Language Loop', eyebrow: '04 // Translate and Compare', icon: BookOpen },
    { id: 'writing-loop', title: 'The Writing Loop', eyebrow: '05 // Audit Your Writing', icon: PenSquare },
    { id: 'build-your-engine', title: 'Build Your Engine', eyebrow: '06 // The Action Plan', icon: Wrench },
  ];

  return (
    <ModuleLayout
      moduleNumber="06"
      moduleTitle="Using Feedback Loops"
      moduleSubtitle="How to Be Your Own Teacher"
      moduleDescription="When you're studying alone, you don't have a teacher to tell you what you're getting wrong. This module shows you how to build that feedback into your study sessions yourself."
      theme={theme}
      sections={sections}
      onBack={onBack}
      progress={progress}
      onProgressUpdate={onProgressUpdate}
      finishButtonText="Be Your Own Teacher"
    >
      {(activeSection) => (
        <>
          {activeSection === 0 && (
            <ReadingSection title="Not All Study Is Equal." eyebrow="Step 1" icon={SlidersHorizontal} theme={theme}>
              <p>Most study time is wasted. It's spent on what we call <Highlight description="Going through the motions without really thinking -- like re-reading your notes or highlighting a textbook. It feels productive, but you're not actually getting better at anything." theme={theme}>Passive Practice</Highlight>--just going through the motions. This feels productive, but it doesn't build skill. To actually get better, you need <Highlight description="Practising with a clear goal, full focus, and -- this is the key part -- a way to check whether you're getting it right. It's harder, but it's what actually makes you improve." theme={theme}>Focused Practice</Highlight>.</p>
              <p>The key ingredient of focused practice is a good feedback loop -- a way to check your work against the right answer. A great teacher does this for you automatically. But when you're studying alone, you don't have that. The goal of this module is to show you how to become your own teacher by building that feedback into your study sessions.</p>
            </ReadingSection>
          )}
           {activeSection === 1 && (
            <ReadingSection title="Two Rules for Self-Study." eyebrow="Step 2" icon={Repeat} theme={theme}>
              <p>To build your own feedback loop, you need to follow two rules about how your brain works. First, <Highlight description="Your brain learns best when you actually notice your mistakes. If you just skip past errors, you don't learn from them. You need to compare your work against the correct answer so mistakes are impossible to ignore." theme={theme}>Pay Attention to Your Mistakes</Highlight>: Your brain learns the most when it spots an error. If you just gloss over mistakes, nothing sticks. That's why you need to compare your work against a correct version -- a marking scheme, a worked solution, a model answer -- so mistakes become impossible to ignore.</p>
              <p>Second, <Highlight description="Your brain can only hold a few things at once. If you try to do the work AND check the work at the same time, you'll do both badly. Do them separately instead." theme={theme}>Don't Do Everything at Once</Highlight>: Your brain can only juggle so much at one time. You can't do the work and check the work at the same time -- you'll do both badly. This <Highlight description="When your brain tries to handle two demanding tasks at the same time, both suffer. It's like trying to have two conversations at once -- neither one goes well." theme={theme}>mental overload</Highlight> is why checking your work as you go feels so hard. The fix is simple: use a <Highlight description="A two-step process: first you do the work, then you check the work. Keeping these separate means you can give each one your full attention." theme={theme}>two-step process</Highlight> -- first do the work, then check the work. Keep them separate.</p>
            </ReadingSection>
          )}
           {activeSection === 2 && (
            <ReadingSection title="The Maths Loop." eyebrow="Step 3" icon={Brain} theme={theme}>
              <p>In Maths, your "stand-in teacher" is a full worked solution or marking scheme. The technique is the <Highlight description="You cover the worked solution, try just the first step yourself, then uncover the first step of the solution to compare. You go one step at a time so you get instant feedback on every single line." theme={theme}>Split-Page Method</Highlight>. You cover the solution, try just one step of the problem, stop, then uncover the correct first step. This gives you instant feedback on every single line of working.</p>
              <p>If your step matches, keep going. If it doesn't -- that's where the real learning happens. Write down in your own words why the correct step was different from yours. This is called <Highlight description="Explaining something to yourself in your own words. It sounds simple, but it forces you to actually understand the 'why' behind each step instead of just copying it." theme={theme}>self-explanation</Highlight> -- and it forces you to actually understand the 'why' behind each step, instead of just copying and moving on.</p>
              <SplitPageSimulator />
            </ReadingSection>
          )}
          {activeSection === 3 && (
            <ReadingSection title="The Language Loop." eyebrow="Step 4" icon={BookOpen} theme={theme}>
              <p>For languages, your "stand-in teacher" is a correct text in the language you're learning. The technique is <Highlight description="You translate a passage from Irish (or French, etc.) into English, wait a while, then translate your English version back without looking at the original. Then you compare the two versions side by side to spot your mistakes." theme={theme}>Back-Translation</Highlight>. You take a short passage in Irish (or French, etc.), translate it into English, wait an hour, then translate your English version <em>back</em> into the original language without looking at it. Finally, you compare your version with the original, side by side.</p>
              <p>This is brilliant at exposing <Highlight description="When you accidentally use English grammar or phrasing while writing in another language. For example, structuring an Irish sentence the way you'd say it in English." theme={theme}>English-brain habits</Highlight> -- where you accidentally use English grammar and phrasing while writing in Irish or French. Every difference between your version and the original shows you exactly where your understanding of the language needs work.</p>
            </ReadingSection>
          )}
          {activeSection === 4 && (
            <ReadingSection title="The Writing Loop." eyebrow="Step 5" icon={PenSquare} theme={theme}>
                <p>For essay writing, your "stand-in teacher" is a model essay and the official marking scheme (the PCLM criteria). The technique is the <Highlight description="You go through your own essay four times, each time with a different coloured highlighter, checking one specific thing each time (Purpose, Coherence, Language, Mechanics)." theme={theme}>Four-Highlighter Method</Highlight>. After writing an essay, you go through it four times, each time with a different colour, checking your work against what the examiner is looking for.</p>
                <p>
                    You use one colour for <Highlight description="Is every sentence actually answering the question? Highlight the bits that directly address what was asked." theme={{...theme, highlightBg: 'bg-blue-100/40', highlightText: 'text-blue-900', highlightDecor: 'decoration-blue-400/40', highlightHover: 'hover:bg-blue-200/60'}}>Purpose</Highlight> (sentences that directly answer the question), one for <Highlight description="Does your essay flow? Do your ideas connect logically from one paragraph to the next?" theme={{...theme, highlightBg: 'bg-green-100/40', highlightText: 'text-green-900', highlightDecor: 'decoration-green-400/40', highlightHover: 'hover:bg-green-200/60'}}>Coherence</Highlight> (linking words and topic sentences), one for <Highlight description="Are you using good word choices? Strong verbs, specific words instead of vague ones?" theme={{...theme, highlightBg: 'bg-yellow-100/40', highlightText: 'text-yellow-900', highlightDecor: 'decoration-yellow-400/40', highlightHover: 'hover:bg-yellow-200/60'}}>Language</Highlight> (strong verbs and word choice), and one for <Highlight description="The basic stuff -- spelling, punctuation, and grammar. Mistakes here are the easiest marks to lose." theme={{...theme, highlightBg: 'bg-red-100/40', highlightText: 'text-red-900', highlightDecor: 'decoration-red-400/40', highlightHover: 'hover:bg-red-200/60'}}>Mechanics</Highlight> (spelling/grammar errors). Instead of vaguely wondering "Is my essay any good?", you get a clear picture of exactly what's working and what needs fixing.
                </p>
                <FourHighlighterAudit />
            </ReadingSection>
          )}
          {activeSection === 5 && (
            <ReadingSection title="Build Your Engine." eyebrow="Step 6" icon={Wrench} theme={theme}>
              <p>You now have everything you need to study smarter on your own. You've got techniques to turn passive, go-through-the-motions study into focused practice that actually builds skill. You've got the tools to be your own teacher.</p>
              <p>The last step is simple: pick one of these techniques and try it just once this week. You don't need to overhaul your entire study routine overnight. Just take one small step to upgrade how you learn. Pick your mission below.</p>
              <MicroCommitment theme={theme}>
                <p>Choose one subject you want to improve. This week, instead of just "studying," set aside 30 minutes to try one of the feedback loop techniques from this module. That's how you go from just putting in time to actually getting better.</p>
              </MicroCommitment>
            </ReadingSection>
          )}
        </>
      )}
    </ModuleLayout>
  );
};
export default TheAutodidactsEngineModule;
