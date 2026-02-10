
/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
*/

import React, { useState } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import {
  SlidersHorizontal, Repeat, Brain, BookOpen, PenSquare, Wrench, Highlighter
} from 'lucide-react';
import { ModuleProgress } from '../types';
import { cyanTheme } from '../moduleThemes';
import { Highlight, ReadingSection, MicroCommitment } from './ModuleShared';
import { ModuleLayout } from './ModuleLayout';

const theme = cyanTheme;

// --- INTERACTIVE COMPONENTS ---

const FourHighlighterAudit = () => {
    const [activeHighlighter, setActiveHighlighter] = useState<string | null>(null);

    const highlights: { [key: string]: string[] } = {
        purpose: ['s1', 's3', 's4'],
        coherence: ['t1', 't2', 't3'],
        language: ['w1', 'w2', 'w3', 'w4', 'w5', 'w6', 'w7', 'w8'],
        mechanics: ['e1']
    };

    const isHighlighted = (id: string) => activeHighlighter && highlights[activeHighlighter]?.includes(id);

    const textWithSpans = `
        <span class="${isHighlighted('s1') ? 'bg-blue-200' : ''}">W.B. Yeats' poem 'The Second Coming' <span class="${isHighlighted('w1') ? 'bg-yellow-200' : ''}">powerfully captures</span> the anxiety of a world <span class="${isHighlighted('w2') ? 'bg-yellow-200' : ''}">descending into chaos</span>.</span>
        <span class="${isHighlighted('s2') ? '' : ''}"><span class="${isHighlighted('t1') ? 'bg-green-200' : ''}">Initially</span>, the poem presents the image of a falcon <span class="${isHighlighted('e1') ? 'bg-red-300' : ''}">loosing</span> control, a metaphor for society's breakdown.</span>
        <span class="${isHighlighted('s3') ? 'bg-blue-200' : ''}"><span class="${isHighlighted('t2') ? 'bg-green-200' : ''}">However</span>, Yeats then introduces the <span class="${isHighlighted('w4') ? 'bg-yellow-200' : ''}">terrifying 'rough beast,'</span> <span class="${isHighlighted('w5') ? 'bg-yellow-200' : ''}">slouching</span> towards Bethlehem. This <span class="${isHighlighted('w6') ? 'bg-yellow-200' : ''}">stark image</span> solidifies the poem's <span class="${isHighlighted('w7') ? 'bg-yellow-200' : ''}">apocalyptic vision</span>.</span>
        <span class="${isHighlighted('s4') ? 'bg-blue-200' : ''}"><span class="${isHighlighted('t3') ? 'bg-green-200' : ''}">Therefore</span>, the poem <span class="${isHighlighted('w8') ? 'bg-yellow-200' : ''}">encapsulates</span> a profound sense of cultural collapse.</span>
    `.replace(/<span class="(bg-blue-200|bg-green-200|bg-yellow-200|bg-red-300)">/g, '<span class="$1 px-1 rounded-sm">');

    return (
        <div className="my-10 p-8 md:p-12 bg-white dark:bg-zinc-800 rounded-xl border border-zinc-200 dark:border-zinc-700">
            <h4 className="font-serif text-2xl font-semibold text-zinc-800 dark:text-white text-center">The Four-Highlighter Audit</h4>
            <p className="text-center text-sm text-zinc-500 dark:text-zinc-400 mb-6">Click the highlighters to audit the paragraph below.</p>
            <div className="flex justify-center flex-wrap gap-3 mb-6">
                <button onClick={() => setActiveHighlighter(activeHighlighter === 'purpose' ? null : 'purpose')} className={`px-4 py-2 flex items-center gap-2 text-sm font-bold rounded-lg border ${activeHighlighter === 'purpose' ? 'bg-blue-500 text-white border-blue-500' : 'bg-blue-50 text-blue-800 border-blue-200'}`}> <Highlighter size={16}/> Purpose</button>
                <button onClick={() => setActiveHighlighter(activeHighlighter === 'coherence' ? null : 'coherence')} className={`px-4 py-2 flex items-center gap-2 text-sm font-bold rounded-lg border ${activeHighlighter === 'coherence' ? 'bg-green-500 text-white border-green-500' : 'bg-green-50 text-green-800 border-green-200'}`}> <Highlighter size={16}/> Coherence</button>
                <button onClick={() => setActiveHighlighter(activeHighlighter === 'language' ? null : 'language')} className={`px-4 py-2 flex items-center gap-2 text-sm font-bold rounded-lg border ${activeHighlighter === 'language' ? 'bg-yellow-400 text-yellow-900 border-yellow-500' : 'bg-yellow-50 text-yellow-800 border-yellow-200'}`}> <Highlighter size={16}/> Language</button>
                <button onClick={() => setActiveHighlighter(activeHighlighter === 'mechanics' ? null : 'mechanics')} className={`px-4 py-2 flex items-center gap-2 text-sm font-bold rounded-lg border ${activeHighlighter === 'mechanics' ? 'bg-red-500 text-white border-red-500' : 'bg-red-50 text-red-800 border-red-200'}`}> <Highlighter size={16}/> Mechanics</button>
            </div>
            <div className="bg-zinc-50 p-6 rounded-xl border border-zinc-200 dark:border-zinc-700 leading-relaxed" dangerouslySetInnerHTML={{ __html: textWithSpans }} />
        </div>
    );
};


// --- MODULE COMPONENT ---
const TheAutodidactsEngineModule: React.FC<{ onBack: () => void; progress: ModuleProgress; onProgressUpdate: (progress: ModuleProgress) => void }> = ({ onBack, progress, onProgressUpdate }) => {
  const sections = [
    { id: 'practice-hierarchy', title: 'The Practice Hierarchy', eyebrow: '01 // Not All Study Is Equal', icon: SlidersHorizontal },
    { id: 'feedback-engine', title: 'The Feedback Engine', eyebrow: '02 // The Rules of Autonomy', icon: Repeat },
    { id: 'maths-loop', title: 'The Maths Loop', eyebrow: '03 // Algorithmic Practice', icon: Brain },
    { id: 'language-loop', title: 'The Language Loop', eyebrow: '04 // Comparative Practice', icon: BookOpen },
    { id: 'writing-loop', title: 'The Writing Loop', eyebrow: '05 // Structural Practice', icon: PenSquare },
    { id: 'build-your-engine', title: 'Build Your Engine', eyebrow: '06 // The Action Plan', icon: Wrench },
  ];

  return (
    <ModuleLayout
      moduleNumber="06"
      moduleTitle="Using Feedback Loops"
      theme={theme}
      sections={sections}
      onBack={onBack}
      progress={progress}
      onProgressUpdate={onProgressUpdate}
    >
      {(activeSection) => (
        <>
          {activeSection === 0 && (
            <ReadingSection title="Not All Study Is Equal." eyebrow="Step 1" icon={SlidersHorizontal} theme={theme}>
              <p>Most study time is wasted. It's spent on what scientists call <Highlight description="Low-effort, repetitive practice without feedback. Examples include re-reading notes or highlighting a textbook. This kind of practice entrenches existing habits and does not lead to improvement." theme={theme}>Naive Practice</Highlight>--just going through the motions. This feels productive, but it doesn't build skill. To get better, you need to engage in <Highlight description="A highly structured activity designed specifically to improve performance. It requires a well-defined goal, full concentration, and, crucially, immediate and informative feedback." theme={theme}>Deliberate Practice</Highlight>.</p>
              <p>The secret ingredient of Deliberate Practice is a high-quality feedback loop. A great teacher provides this automatically. But when you're studying alone, you're in a "feedback vacuum." The goal of this module is to teach you how to become your own teacher by building your own feedback engine.</p>
            </ReadingSection>
          )}
           {activeSection === 1 && (
            <ReadingSection title="The Rules of Autonomy." eyebrow="Step 2" icon={Repeat} theme={theme}>
              <p>To build your own feedback loop, you need to obey two laws of your brain's hardware. First, the <Highlight description="The need to consciously focus on errors to strengthen the brain's learning signal (the Pe wave). This forces a Growth Mindset response through behaviour." theme={theme}>Law of Neural Amplification</Highlight>: You must force your brain to pay attention to errors. A Growth Mindset does this automatically by boosting your 'Pe' error signal. You must simulate this by using rigorous, unavoidable comparison against an expert model--what we'll call a "Teacher Proxy."</p>
              <p>Second, the <Highlight description="The principle that your working memory is severely limited. You cannot be a performer and a critic at the same time without overloading your brain." theme={theme}>Law of Cognitive Load</Highlight>: Your working memory is tiny. You cannot be a high-level performer and a high-level critic *at the same time*. This <Highlight description="The cognitive strain that occurs when your limited working memory is forced to handle two competing tasks at once, degrading performance on both." theme={theme}>Split-Attention Effect</Highlight> is why trying to check your work as you go is so hard. The solution is an <Highlight description="A feedback process where the performance phase is completely separate from the feedback phase. This protects working memory and allows for deeper analysis." theme={theme}>Asynchronous Loop</Highlight>: separate your "Performance Phase" (doing the work) from your "Feedback Phase" (checking the work).</p>
            </ReadingSection>
          )}
           {activeSection === 2 && (
            <ReadingSection title="The Maths Loop." eyebrow="Step 3" icon={Brain} theme={theme}>
              <p>In a subject like Maths, the "Teacher Proxy" is a full worked solution or marking scheme. The protocol is the <Highlight description="A technique where a student covers a worked solution, attempts only the first line, then uncovers the first line of the solution to compare. This creates a line-by-line feedback loop." theme={theme}>Split-Page Method</Highlight>. You cover the solution, attempt just one line of the problem, stop, then uncover the expert's first line. This creates a high-fidelity micro-feedback loop.</p>
              <p>If your step matches, you continue. If it's a mismatch, the learning begins. You must perform <Highlight description="The act of explaining a concept or the logic of a step to yourself. This forces deeper processing and is one of the most effective ways to build robust understanding." theme={theme}>Self-Explanation</Highlight>--writing down in your own words why the expert's step was better than yours. This forces you to confront the gap in your understanding and manually amplifies the learning signal in your brain.</p>
            </ReadingSection>
          )}
          {activeSection === 3 && (
            <ReadingSection title="The Language Loop." eyebrow="Step 4" icon={BookOpen} theme={theme}>
              <p>For language syntax and grammar, the "Teacher Proxy" is a native text. The protocol is <Highlight description="A powerful technique where you translate a text from your target language (L2) to your native language (L1), wait, and then translate it back to L2 without looking at the original to expose errors." theme={theme}>Back-Translation</Highlight>. You take a short native text (L2), translate it into your own language (L1), wait an hour, then translate your L1 version *back* into the L2 without looking at the original. Finally, you compare your new L2 version with the original, side-by-side.</p>
              <p>This process is brutally effective at exposing <Highlight description="The tendency to impose the grammatical structures and idioms of your native language (L1) onto the foreign language you are learning (L2)." theme={theme}>L1 Interference</Highlight>--the tendency to think in English while writing in Irish or French. Every difference between your version and the native text is a high-quality feedback point, revealing exactly where your internal model of the language is wrong.</p>
            </ReadingSection>
          )}
          {activeSection === 4 && (
            <ReadingSection title="The Writing Loop." eyebrow="Step 5" icon={PenSquare} theme={theme}>
                <p>For subjective skills like essay writing, the "Teacher Proxy" is a high-quality model essay and the official marking scheme (the PCLM criteria). The protocol is the <Highlight description="A self-correction protocol where you visually audit your own essay using four different colored highlighters, one for each of the PCLM criteria." theme={theme}>Four-Highlighter Method</Highlight>. After writing an essay, you make four passes, each with a different color, auditing your work against the examiner's criteria.</p>
                <p>
                    You use one color for <Highlight description="The relevance of your writing. Does every sentence directly address the question asked?" theme={{...theme, highlightBg: 'bg-blue-100/40', highlightText: 'text-blue-900', highlightDecor: 'decoration-blue-400/40', highlightHover: 'hover:bg-blue-200/60'}}>Purpose</Highlight> (sentences that directly answer the question), one for <Highlight description="The flow and structure of your argument. Do your ideas connect logically from one to the next?" theme={{...theme, highlightBg: 'bg-green-100/40', highlightText: 'text-green-900', highlightDecor: 'decoration-green-400/40', highlightHover: 'hover:bg-green-200/60'}}>Coherence</Highlight> (transition words and topic sentences), one for <Highlight description="The quality and precision of your word choice. Are you using strong verbs and specific terminology?" theme={{...theme, highlightBg: 'bg-yellow-100/40', highlightText: 'text-yellow-900', highlightDecor: 'decoration-yellow-400/40', highlightHover: 'hover:bg-yellow-200/60'}}>Language</Highlight> (strong verbs and terminology), and one for <Highlight description="The technical correctness of your writing, including spelling, punctuation, and grammar." theme={{...theme, highlightBg: 'bg-red-100/40', highlightText: 'text-red-900', highlightDecor: 'decoration-red-400/40', highlightHover: 'hover:bg-red-200/60'}}>Mechanics</Highlight> (spelling/grammar errors). This transforms a vague sense of "Is my essay good?" into a clear, visual dashboard of your strengths and weaknesses.
                </p>
                <FourHighlighterAudit />
            </ReadingSection>
          )}
          {activeSection === 5 && (
            <ReadingSection title="Build Your Engine." eyebrow="Step 6" icon={Wrench} theme={theme}>
              <p>You now have the blueprints for a high-performance feedback engine. You have the protocols to transform passive, naive practice into active, deliberate practice. You have the tools to become an autodidact--a self-teaching, self-regulating learner.</p>
              <p>The final step is to choose a single protocol and commit to trying it just once in the next week. This isn't about overhauling your entire study routine overnight. It's about taking one small, strategic step to upgrade your learning process. Select your mission below to build your engine.</p>
              <MicroCommitment theme={theme}>
                <p>Choose one subject you want to improve. This week, instead of just "studying," schedule 30 minutes to run one of these feedback loop protocols. You are moving from being a student to being a scientist of your own learning.</p>
              </MicroCommitment>
            </ReadingSection>
          )}
        </>
      )}
    </ModuleLayout>
  );
};
export default TheAutodidactsEngineModule;
