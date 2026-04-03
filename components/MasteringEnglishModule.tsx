/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
*/

import React, { useState } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { MotionDiv } from './Motion';
import {
  BookOpen, PenSquare, MessageSquare, BarChart, BrainCircuit, Mic, Settings
} from 'lucide-react';
import { ModuleProgress } from '../types';
import { blueTheme } from '../moduleThemes';
import { Highlight, ReadingSection, MicroCommitment, PersonalStory } from './ModuleShared';
import { ModuleLayout } from './ModuleLayout';

const theme = blueTheme;

// --- INTERACTIVE COMPONENTS ---

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

// --- MODULE COMPONENT ---
const MasteringEnglishModule: React.FC<{ onBack: () => void; progress: ModuleProgress; onProgressUpdate: (progress: ModuleProgress) => void }> = ({ onBack, progress, onProgressUpdate }) => {
  const sections = [
    { id: 'pclm-blueprint', title: 'How You Actually Get Marked', eyebrow: '01 // The Marking Scheme', icon: Settings },
    { id: 'paper1-engine', title: 'Paper 1: Where the Marks Are', eyebrow: '02 // Language & Comprehension', icon: BookOpen },
    { id: 'composing', title: 'Paper 1: The 100-Mark Essay', eyebrow: '03 // Composing', icon: PenSquare },
    { id: 'single-text', title: 'Paper 2: The Single Text', eyebrow: '04 // Macbeth 2026', icon: MessageSquare },
    { id: 'comparative-study', title: 'Paper 2: The Comparative Study', eyebrow: '05 // The Modes', icon: BarChart },
    { id: 'poetry', title: 'Paper 2: Prescribed Poetry', eyebrow: '06 // The "Big 4" Rule', icon: Mic },
    { id: 'toolkit', title: 'Your English Toolkit', eyebrow: '07 // Smart Techniques', icon: BrainCircuit },
  ];

  return (
    <ModuleLayout
      moduleNumber="04"
      moduleTitle="Mastering English"
      moduleSubtitle="How the Marking Scheme Actually Works"
      moduleDescription="English isn't about luck or natural talent. Once you understand how PCLM marking works, you'll know exactly what the examiner wants -- and how to give it to them."
      theme={theme}
      sections={sections}
      onBack={onBack}
      progress={progress}
      onProgressUpdate={onProgressUpdate}
    >
      {(activeSection) => (
        <>
          {activeSection === 0 && (
            <ReadingSection title="How You Actually Get Marked." eyebrow="Step 1" icon={Settings} theme={theme}>
              <p>Here's something most students don't realise: English is not marked on vibes. Every single answer you write is graded using the same four-part system called <Highlight description="PCLM stands for Purpose, Coherence, Language, and Mechanics. These are the four things the examiner scores you on, every single time." theme={theme}>PCLM</Highlight>. Once you understand how it works, you'll know exactly what separates a H3 from a H1.</p>
              <p><Highlight description="Purpose means: did you actually answer what was asked? If you go off-topic, everything else suffers." theme={theme}>Purpose</Highlight> is the most important one. You could write the best essay of your life, but if it doesn't answer the question, it's worth very little. Even more importantly, your Coherence and Language marks are capped by your Purpose mark. So answering the actual question always comes first.</p>
              <PersonalStory name="Aisling" role="6th Year, Kilkenny">
                <p>I used to just pick whatever essay title sounded nice and write whatever came into my head. I got a H4 in my mock. Then I learned about PCLM and realised I was losing marks on Purpose every time. In the real exam, I spent five minutes planning how my essay actually answered the question before I started writing. I got a H2. Same writing ability -- I just stopped ignoring what the examiner was actually looking for.</p>
              </PersonalStory>
            </ReadingSection>
          )}
          {activeSection === 1 && (
            <ReadingSection title="Paper 1: Where the Marks Are." eyebrow="Step 2" icon={BookOpen} theme={theme}>
              <p>Paper 1 is half your total English grade, and it's the easiest place to pick up reliable marks. <Highlight description="Question A is the comprehension section. You read a text and answer questions about what it says and how it's written." theme={theme}>Question A</Highlight> tests whether you can read closely and explain what's going on. The 20-mark style question is the big one -- don't just name techniques like "metaphor" or "alliteration." You need to explain what effect they have on the reader and why the writer used them.</p>
              <p><Highlight description="Question B asks you to write in a specific format like a speech, a letter, or a blog post. You have to match the format exactly." theme={theme}>Question B</Highlight> is where a lot of students trip up. It asks you to write something in a specific format -- like a letter, a speech, or a blog post. If the question says "write a speech" and you write a personal essay instead, your Purpose mark drops through the floor no matter how good the writing is. Always check the format before you start.</p>
            </ReadingSection>
          )}
           {activeSection === 2 && (
            <ReadingSection title="The 100-Mark Essay." eyebrow="Step 3" icon={PenSquare} theme={theme}>
              <p>The Composing section is worth 25% of your total grade -- that's a massive chunk from one essay. The Personal Essay is the most popular choice, but most students do it wrong. It's not just telling a story. It needs to be a <Highlight description="A reflective piece means you don't just describe what happened -- you show how it felt, what you learned, and how it changed you." theme={theme}>reflective piece</Highlight> where you show how an experience affected you. "Show, don't tell" is the golden rule here.</p>
              <p>The Short Story can pay off big if you keep it tight -- one event, one short timeframe, no trying to cram in an entire life story. The Discursive Essay needs you to look at both sides of an issue fairly, while the Persuasive Essay is all about picking a side and arguing it hard with punchy language.</p>
              <ShowDontTellConverter />
            </ReadingSection>
          )}
          {activeSection === 3 && (
            <ReadingSection title="Paper 2: Single Text (Macbeth)." eyebrow="Step 4" icon={MessageSquare} theme={theme}>
               <p>For 2026, the Shakespeare play is Macbeth. To get top marks, you can't just talk about themes on their own -- you need to show how themes, characters, and imagery all connect to each other. The big themes are: <Highlight description="Ambition isn't just about wanting power. It's about what that wanting does to you as a person -- the guilt, the paranoia, the destruction." theme={theme}>Ambition and what it does to people</Highlight>, good leadership vs. tyranny, the supernatural and fate, and how things aren't always what they seem.</p>
               <p>When you're writing about characters, focus on how they change over the course of the play. Macbeth goes from being called "brave Macbeth" at the start to being called a "butcher" by the end. Lady Macbeth goes the opposite way -- she starts off ruthless and in control, but by the end she's sleepwalking and falling apart with guilt. Showing you understand these journeys is what gets you the big marks.</p>
            </ReadingSection>
          )}
           {activeSection === 4 && (
            <ReadingSection title="The Comparative Study." eyebrow="Step 5" icon={BarChart} theme={theme}>
                <p>For Higher Level 2026, the three comparative modes are <strong>Cultural Context</strong>, <strong>General Vision and Viewpoint (GVV)</strong>, and <strong>Literary Genre</strong>. Important: "Theme or Issue" is NOT a mode for Higher Level. Don't waste your time preparing for it.</p>
                <p>The secret to getting top marks here is linking your texts together constantly. Don't write about Text A, then Text B, then Text C separately. In every paragraph, compare and contrast them side by side. The best way to prepare is the <Highlight description="Pick 4-5 key moments from each text. These are scenes or turning points you can talk about no matter which mode comes up on the exam." theme={theme}>"Key Moment" method</Highlight> -- pick 4-5 key moments from each text that you can use flexibly no matter which mode comes up.</p>
            </ReadingSection>
          )}
           {activeSection === 5 && (
            <ReadingSection title="Prescribed Poetry." eyebrow="Step 6" icon={Mic} theme={theme}>
              <p>The <Highlight description="There are 8 poets on the course but only 4 come up on the exam. If you study 5, you're guaranteed at least one of yours will appear. Study fewer and you're gambling." theme={theme}>"Big 4+1" Rule</Highlight> is the most important thing to know about poetry. There are 8 poets on the course, but only 4 appear on the paper. If you study 5 poets well, you're guaranteed one of yours will come up. Study fewer and you're taking a serious risk.</p>
              <p>For top marks, don't just talk about what the poet is saying -- talk about how they say it. What words do they choose? What images do they use? How does the poem's rhythm or structure add to the feeling? Showing you can do both is what separates a H2 from a H1.</p>
            </ReadingSection>
          )}
           {activeSection === 6 && (
            <ReadingSection title="Your English Toolkit." eyebrow="Step 7" icon={BrainCircuit} theme={theme}>
              <p>A few smart techniques can make a real difference to your grade. For Paper 1 Comprehension, try <Highlight description="Read the questions before you read the text. Give each question a colour, then highlight useful quotes in matching colours as you read. It saves loads of time." theme={theme}>reading the questions first</Highlight> and colour-coding useful quotes as you read -- it saves loads of time. When quoting in essays, use <Highlight description="Short quotes of 3-5 words that you weave into your own sentences flow much better than dropping in a massive block quote." theme={theme}>short embedded quotes</Highlight> (3-5 words woven into your sentence) instead of big chunky block quotes. And watch your time carefully across both papers -- running out of time is one of the most common reasons students lose marks.</p>
               <MicroCommitment theme={theme}>
                <p>For your next practice essay, try a PCLM check. Grab four different coloured pens or highlighters and go through your essay marking where you've shown Purpose (did I answer the question?), Coherence (does it flow?), Language (is my writing interesting?), and Mechanics (spelling, grammar, paragraphs). It's a quick way to spot where you're losing marks.</p>
              </MicroCommitment>
            </ReadingSection>
          )}
        </>
      )}
    </ModuleLayout>
  );
};
export default MasteringEnglishModule;
