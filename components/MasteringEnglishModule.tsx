/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
*/

import React, { useState } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import {
  BookOpen, PenSquare, MessageSquare, BarChart, BrainCircuit, Mic, Settings
} from 'lucide-react';
import { ModuleProgress } from '../types';
import { blueTheme } from '../moduleThemes';
import { Highlight, ReadingSection, MicroCommitment } from './ModuleShared';
import { ModuleLayout } from './ModuleLayout';

const theme = blueTheme;

// --- INTERACTIVE COMPONENTS ---

const MotionDiv = motion.div as any;

const SHOW_DONT_TELL_PAIRS = [
  {
    telling: "She was scared.",
    showing: "Her fingers trembled against the cold door handle. She held her breath, straining to hear past the hammering in her chest.",
    tip: "Use physical sensations and specific actions instead of naming the emotion.",
  },
  {
    telling: "The house was old.",
    showing: "Paint curled from the window frames in brittle flakes. The porch sagged under a carpet of brown leaves that no one had swept in years.",
    tip: "Replace adjectives with concrete visual details that let the reader conclude 'old' themselves.",
  },
  {
    telling: "He was angry.",
    showing: "He slammed his fist on the desk. Papers scattered across the floor as his jaw tightened, the vein in his temple throbbing.",
    tip: "Show anger through actions, body language, and physical consequences.",
  },
  {
    telling: "It was a beautiful morning.",
    showing: "Sunlight caught the dew on each blade of grass, turning the garden into a field of tiny diamonds. A blackbird rehearsed its song from the chimney pot.",
    tip: "Engage multiple senses — sight, sound, touch — to paint the scene.",
  },
  {
    telling: "She was tired.",
    showing: "Her eyelids dragged shut between every sentence. She read the same paragraph for the fourth time, the words swimming into a grey blur.",
    tip: "Show fatigue through its effects on perception and behaviour.",
  },
];

const ShowDontTellConverter = () => {
  const [currentIndex, setCurrentIndex] = useState(0);
  const [userInputs, setUserInputs] = useState<string[]>(Array(5).fill(''));
  const [revealed, setRevealed] = useState<boolean[]>(Array(5).fill(false));
  const [completed, setCompleted] = useState(false);

  const completedCount = revealed.filter(Boolean).length;

  const handleInputChange = (value: string) => {
    const next = [...userInputs];
    next[currentIndex] = value;
    setUserInputs(next);
  };

  const handleReveal = () => {
    const next = [...revealed];
    next[currentIndex] = true;
    setRevealed(next);
  };

  const handleNext = () => {
    if (currentIndex < 4) {
      setCurrentIndex(currentIndex + 1);
    } else {
      setCompleted(true);
    }
  };

  const handleStartOver = () => {
    setCurrentIndex(0);
    setUserInputs(Array(5).fill(''));
    setRevealed(Array(5).fill(false));
    setCompleted(false);
  };

  const pair = SHOW_DONT_TELL_PAIRS[currentIndex];

  return (
    <div className="my-10 p-8 md:p-12 bg-white dark:bg-zinc-800 rounded-xl border border-zinc-200 dark:border-zinc-700">
      <h4 className="font-serif text-2xl font-semibold text-zinc-800 dark:text-white text-center">
        Show, Don't Tell Converter
      </h4>
      <p className="text-center text-sm text-zinc-500 dark:text-zinc-400 mt-1 mb-8">
        Rewrite each flat sentence using sensory detail, then compare with an expert version.
      </p>

      {/* Progress indicator */}
      <div className="flex items-center justify-center gap-2 mb-8">
        {SHOW_DONT_TELL_PAIRS.map((_, i) => (
          <div
            key={i}
            className={`w-3 h-3 rounded-full transition-colors duration-300 ${
              revealed[i]
                ? 'bg-emerald-500'
                : i === currentIndex
                ? 'bg-blue-500'
                : 'bg-zinc-200 dark:bg-zinc-600'
            }`}
          />
        ))}
        <span className="ml-3 text-sm font-medium text-zinc-500 dark:text-zinc-400">
          {completedCount}/5 converted
        </span>
      </div>

      <AnimatePresence mode="wait">
        {completed ? (
          <MotionDiv
            key="summary"
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            exit={{ opacity: 0, y: -20 }}
            transition={{ duration: 0.4 }}
          >
            <div className="text-center space-y-6 py-6">
              <div className="inline-flex items-center justify-center w-16 h-16 rounded-full bg-emerald-100 dark:bg-emerald-900/30 mx-auto">
                <PenSquare className="w-8 h-8 text-emerald-600 dark:text-emerald-400" />
              </div>
              <p className="text-lg text-zinc-700 dark:text-zinc-300 leading-relaxed max-w-xl mx-auto">
                <strong className="text-emerald-600 dark:text-emerald-400">Show Don't Tell</strong> is the single most powerful technique in Paper 1 creative writing. It transforms a H4 essay into H1 territory. The examiner doesn't want to be <em>told</em> how a character feels — they want to <em>feel it themselves</em>.
              </p>
              <button
                onClick={handleStartOver}
                className="mt-4 px-6 py-2.5 rounded-lg bg-blue-500 hover:bg-blue-600 text-white font-medium transition-colors duration-200"
              >
                Start Over
              </button>
            </div>
          </MotionDiv>
        ) : (
          <MotionDiv
            key={`card-${currentIndex}`}
            initial={{ opacity: 0, x: 40 }}
            animate={{ opacity: 1, x: 0 }}
            exit={{ opacity: 0, x: -40 }}
            transition={{ duration: 0.35 }}
          >
            {/* Telling card */}
            <div className="rounded-xl border border-rose-200 dark:border-rose-800/50 bg-rose-50 dark:bg-rose-900/20 p-6 mb-6">
              <span className="inline-block text-xs font-bold uppercase tracking-widest text-rose-500 dark:text-rose-400 mb-2">
                Telling
              </span>
              <p className="text-lg font-medium text-rose-900 dark:text-rose-100 italic">
                "{pair.telling}"
              </p>
            </div>

            {/* User input area */}
            {!revealed[currentIndex] && (
              <div className="space-y-4 mb-6">
                <label className="block text-sm font-medium text-zinc-600 dark:text-zinc-400">
                  Your "showing" version:
                </label>
                <textarea
                  value={userInputs[currentIndex]}
                  onChange={(e) => handleInputChange(e.target.value)}
                  placeholder="Rewrite the sentence using sensory details, actions, and specific imagery..."
                  rows={3}
                  className="w-full rounded-lg border border-zinc-300 dark:border-zinc-600 bg-white dark:bg-zinc-900 text-zinc-800 dark:text-zinc-200 px-4 py-3 text-sm focus:outline-none focus:ring-2 focus:ring-blue-500/50 focus:border-blue-500 placeholder:text-zinc-400 dark:placeholder:text-zinc-500 resize-none"
                />
                <button
                  onClick={handleReveal}
                  disabled={!userInputs[currentIndex].trim()}
                  className={`w-full py-3 rounded-lg font-medium transition-all duration-200 ${
                    userInputs[currentIndex].trim()
                      ? 'bg-blue-500 hover:bg-blue-600 text-white shadow-md shadow-blue-500/20'
                      : 'bg-zinc-200 dark:bg-zinc-700 text-zinc-400 dark:text-zinc-500 cursor-not-allowed'
                  }`}
                >
                  Compare with Expert
                </button>
              </div>
            )}

            {/* Comparison view */}
            {revealed[currentIndex] && (
              <MotionDiv
                initial={{ opacity: 0, y: 16 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ duration: 0.4 }}
                className="space-y-4 mb-6"
              >
                <div className="grid md:grid-cols-2 gap-4">
                  {/* User's version */}
                  <div className="rounded-xl border border-blue-200 dark:border-blue-800/50 bg-blue-50 dark:bg-blue-900/20 p-5">
                    <span className="inline-block text-xs font-bold uppercase tracking-widest text-blue-500 dark:text-blue-400 mb-2">
                      Your Version
                    </span>
                    <p className="text-sm text-blue-900 dark:text-blue-100 leading-relaxed">
                      "{userInputs[currentIndex]}"
                    </p>
                  </div>
                  {/* Expert version */}
                  <div className="rounded-xl border border-emerald-200 dark:border-emerald-800/50 bg-emerald-50 dark:bg-emerald-900/20 p-5">
                    <span className="inline-block text-xs font-bold uppercase tracking-widest text-emerald-500 dark:text-emerald-400 mb-2">
                      Showing
                    </span>
                    <p className="text-sm text-emerald-900 dark:text-emerald-100 leading-relaxed">
                      "{pair.showing}"
                    </p>
                  </div>
                </div>
                {/* Tip */}
                <p className="text-sm italic text-zinc-500 dark:text-zinc-400 text-center px-4">
                  Tip: {pair.tip}
                </p>
                {/* Next button */}
                <button
                  onClick={handleNext}
                  className="w-full py-3 rounded-lg font-medium bg-emerald-500 hover:bg-emerald-600 text-white transition-colors duration-200 shadow-md shadow-emerald-500/20"
                >
                  {currentIndex < 4 ? 'Next Sentence' : 'View Summary'}
                </button>
              </MotionDiv>
            )}
          </MotionDiv>
        )}
      </AnimatePresence>
    </div>
  );
};

const PCLMGrader = () => {
    const [pclm, setPclm] = useState({ p: 50, c: 50, l: 50, m: 50 });

    // P caps C and L
    const cappedC = Math.min(pclm.c, pclm.p);
    const cappedL = Math.min(pclm.l, pclm.p);

    const total = (pclm.p * 0.3) + (cappedC * 0.3) + (cappedL * 0.3) + (pclm.m * 0.1);
    const grade = total >= 90 ? 'H1' : total >= 80 ? 'H2' : total >= 70 ? 'H3' : 'H4';

    return (
        <div className="my-10 p-8 md:p-12 bg-white dark:bg-zinc-800 rounded-xl border border-zinc-200 dark:border-zinc-700">
            <h4 className="font-serif text-2xl font-semibold text-zinc-800 dark:text-white text-center">PCLM Grader</h4>
            <div className="grid grid-cols-2 gap-6 items-center">
                <div className="space-y-2">
                    <input type="range" value={pclm.p} onChange={e => setPclm({...pclm, p: parseInt(e.target.value)})} className="w-full"/>
                    <input type="range" value={pclm.c} onChange={e => setPclm({...pclm, c: parseInt(e.target.value)})} className="w-full"/>
                    <input type="range" value={pclm.l} onChange={e => setPclm({...pclm, l: parseInt(e.target.value)})} className="w-full"/>
                    <input type="range" value={pclm.m} onChange={e => setPclm({...pclm, m: parseInt(e.target.value)})} className="w-full"/>
                </div>
                <div className="text-center">
                    <p className="text-6xl font-semibold text-blue-500">{grade}</p>
                </div>
            </div>
        </div>
    );
};

// --- MODULE COMPONENT ---
const MasteringEnglishModule: React.FC<{ onBack: () => void; progress: ModuleProgress; onProgressUpdate: (progress: ModuleProgress) => void }> = ({ onBack, progress, onProgressUpdate }) => {
  const sections = [
    { id: 'pclm-blueprint', title: 'The PCLM Blueprint', eyebrow: '01 // The Marking Scheme', icon: Settings },
    { id: 'paper1-engine', title: 'Paper 1: The Engine of Grades', eyebrow: '02 // Language & Comprehension', icon: BookOpen },
    { id: 'composing', title: 'Paper 1: The 100-Mark Essay', eyebrow: '03 // Composing', icon: PenSquare },
    { id: 'single-text', title: 'Paper 2: The Single Text', eyebrow: '04 // Macbeth 2026', icon: MessageSquare },
    { id: 'comparative-study', title: 'Paper 2: The Comparative Study', eyebrow: '05 // The Modes', icon: BarChart },
    { id: 'poetry', title: 'Paper 2: Prescribed Poetry', eyebrow: '06 // The "Big 4" Rule', icon: Mic },
    { id: 'toolkit', title: 'The Strategic Toolkit', eyebrow: '07 // High-Yield Strategies', icon: BrainCircuit },
  ];

  return (
    <ModuleLayout
      moduleNumber="04"
      moduleTitle="Mastering English"
      moduleSubtitle="The PCLM Protocol"
      moduleDescription="A strategic deconstruction of the Leaving Cert English exam, focusing on mastering the PCLM marking scheme and optimizing for H1 performance."
      theme={theme}
      sections={sections}
      onBack={onBack}
      progress={progress}
      onProgressUpdate={onProgressUpdate}
    >
      {(activeSection) => (
        <>
          {activeSection === 0 && (
            <ReadingSection title="The PCLM Blueprint." eyebrow="Step 1" icon={Settings} theme={theme}>
              <p>The Leaving Cert English exam is not subjective. It is governed by a strict, unified marking scheme: <Highlight description="The four criteria for marking English: Purpose (30%), Coherence (30%), Language (30%), and Mechanics (10%)." theme={theme}>PCLM</Highlight>. Understanding this blueprint is the single most significant differentiator between a H3 and a H1.</p>
              <p><Highlight description="Did you answer the specific question asked? This is the most important criterion." theme={theme}>Purpose</Highlight> is king. A brilliant essay that is irrelevant is worthless. Crucially, your marks for Coherence and Language are *capped* by your Purpose mark. You must prioritize relevance above all else.</p>
            </ReadingSection>
          )}
          {activeSection === 1 && (
            <ReadingSection title="Paper 1: Engine of Grades." eyebrow="Step 2" icon={BookOpen} theme={theme}>
              <p>Paper 1 is 50% of your total grade and the most reliable place to secure marks. Question A tests comprehension and analysis. The 20-mark "Style/Technique" question is where the H1 is won or lost. You must go beyond listing techniques and explain their *effect* on the reader.</p>
              <p>Question B, the Functional Writing task, is a "hidden trap." You must adhere strictly to the conventions of the requested genre (e.g., letter, blog post). Writing a personal essay in the wrong format is a fatal error for your 'P' mark.</p>
            </ReadingSection>
          )}
           {activeSection === 2 && (
            <ReadingSection title="The 100-Mark Essay." eyebrow="Step 3" icon={PenSquare} theme={theme}>
              <p>The Composing section is worth 25% of your total grade. The Personal Essay is the most popular but most poorly executed. It is not just a story; it must be a <Highlight description="An exploration of how an event felt, what was learned, and how the writer changed as a result." theme={theme}>reflective piece</Highlight>. "Show, don't tell" is the golden rule.</p>
              <p>The Short Story is high-risk, high-reward. Focus on a single incident and a short timeframe. The Discursive Essay requires a balanced exploration of an issue, while the Persuasive Essay demands a firm stance and the use of rhetorical devices.</p>
              <ShowDontTellConverter />
            </ReadingSection>
          )}
          {activeSection === 3 && (
            <ReadingSection title="Paper 2: Single Text (Macbeth)." eyebrow="Step 4" icon={MessageSquare} theme={theme}>
               <p>For 2026, the prescribed Shakespearean text is Macbeth. A H1 analysis requires you to discuss the interconnectedness of themes, character, and imagery. The core themes are: <Highlight description="It's not just about wanting power; it's about the moral cost of that want." theme={theme}>Ambition and its Corrupting Influence</Highlight>, Kingship vs. Tyranny, The Supernatural and Fate, and Appearance vs. Reality.</p>
               <p>Character analysis should focus on trajectories. Macbeth devolves from "brave Macbeth" to a nihilistic "butcher." Lady Macbeth follows a reverse trajectory, from ruthless resolve to collapse under the weight of repressed guilt.</p>
            </ReadingSection>
          )}
           {activeSection === 4 && (
            <ReadingSection title="The Comparative Study." eyebrow="Step 5" icon={BarChart} theme={theme}>
                <p>For Higher Level 2026, the three comparative modes are <strong>Cultural Context</strong>, <strong>General Vision and Viewpoint (GVV)</strong>, and <strong>Literary Genre</strong>. Crucially, "Theme or Issue" is NOT a mode for Higher Level. Preparing it is a catastrophic waste of time.</p>
                <p>The key to a H1 is a link-heavy structure. Avoid discussing your texts sequentially. Instead, weave them together in each paragraph, comparing and contrasting them based on the mode. The <Highlight description="A study technique where you identify 4-5 key moments in each text that can be flexibly applied to any of the comparative modes." theme={theme}>"Key Moment" Matrix</Highlight> is the most effective way to prepare for this.</p>
            </ReadingSection>
          )}
           {activeSection === 5 && (
            <ReadingSection title="Prescribed Poetry." eyebrow="Step 6" icon={Mic} theme={theme}>
              <p>The <Highlight description="The mathematical reality that to guarantee one of your studied poets appears on the paper (where 4 out of 8 are examined), you must study 5 poets thoroughly." theme={theme}>"Big 4+1" Rule</Highlight> is non-negotiable. To guarantee a poet you've studied appears, you must master five poets. H1 answers must balance a discussion of the poet's themes (substance) with an analysis of their style (how they say it).</p>
            </ReadingSection>
          )}
           {activeSection === 6 && (
            <ReadingSection title="The Strategic Toolkit." eyebrow="Step 7" icon={BrainCircuit} theme={theme}>
              <p>High-yield strategies can transform your performance. Use the <Highlight description="A time-saving technique where you read the questions first, assign a color to each, and then highlight relevant quotes as you read the text." theme={theme}>'Index Margining'</Highlight> technique for Paper 1 Comprehension. Prioritize <Highlight description="Short phrases (3-5 words) that fit grammatically into your own sentences, which are far superior to long, clunky block quotes." theme={theme}>Embedded Quotes</Highlight> over long block quotes. And above all, adhere to a strict time management protocol for both papers.</p>
               <MicroCommitment theme={theme}>
                <p>For your next practice essay, perform a PCLM audit. Go through with four different highlighters and mark where you have demonstrated Purpose, Coherence, Language, and good Mechanics. This will reveal your weaknesses.</p>
              </MicroCommitment>
            </ReadingSection>
          )}
        </>
      )}
    </ModuleLayout>
  );
};
export default MasteringEnglishModule;
