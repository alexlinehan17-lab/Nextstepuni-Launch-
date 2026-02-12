/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
*/

import React, { useState } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import {
  Key, Leaf, Beaker, Atom, Sprout, BrainCircuit, Flag
} from 'lucide-react';
import { ModuleProgress } from '../types';
import { emeraldTheme } from '../moduleThemes';
import { Highlight, ReadingSection, MicroCommitment } from './ModuleShared';
import { ModuleLayout } from './ModuleLayout';

const theme = emeraldTheme;

// --- INTERACTIVE COMPONENTS ---
const CurlyArrowDrill = () => {
    const [current, setCurrent] = useState(0);
    const [selected, setSelected] = useState<'a' | 'b' | null>(null);
    const [isCorrect, setIsCorrect] = useState(false);
    const [score, setScore] = useState(0);

    const scenarios = [
        { a: { formula: 'Cl\u207b', label: 'Chloride ion', isSource: true }, b: { formula: 'C\u207a', label: 'Carbocation', isSource: false },
          explanation: 'Cl\u207b has a lone pair (electron-rich) \u2192 donates to the electron-poor C\u207a.' },
        { a: { formula: 'H\u207a', label: 'Proton', isSource: false }, b: { formula: 'OH\u207b', label: 'Hydroxide ion', isSource: true },
          explanation: 'OH\u207b is electron-rich \u2192 arrow goes from OH\u207b lone pair to H\u207a.' },
        { a: { formula: 'BF\u2083', label: 'Boron trifluoride', isSource: false }, b: { formula: 'NH\u2083', label: 'Ammonia', isSource: true },
          explanation: 'NH\u2083 has a lone pair on nitrogen \u2192 donates to electron-deficient boron.' },
        { a: { formula: 'C=C', label: 'Alkene (\u03c0 bond)', isSource: true }, b: { formula: 'H\u207a', label: 'Proton', isSource: false },
          explanation: 'The \u03c0 bond is an electron source \u2192 arrow from C=C to H\u207a.' },
        { a: { formula: 'CH\u2083\u207a', label: 'Methyl cation', isSource: false }, b: { formula: 'H\u2082O', label: 'Water', isSource: true },
          explanation: 'H\u2082O has lone pairs \u2192 donates electrons to the electron-poor CH\u2083\u207a.' },
    ];

    const s = scenarios[current];
    const done = current >= scenarios.length;

    const handleSelect = (choice: 'a' | 'b') => {
        if (isCorrect) return;
        setSelected(choice);
        const right = (choice === 'a' && s.a.isSource) || (choice === 'b' && s.b.isSource);
        if (right) {
            setIsCorrect(true);
            setScore(prev => prev + 1);
        }
    };

    const handleNext = () => {
        setCurrent(prev => prev + 1);
        setSelected(null);
        setIsCorrect(false);
    };

    const btnClass = (side: 'a' | 'b') => {
        const isSource = side === 'a' ? s?.a.isSource : s?.b.isSource;
        const base = 'flex-1 max-w-[150px] p-4 rounded-xl border-2 text-center transition-all';
        if (isCorrect) {
            return isSource
                ? `${base} border-emerald-400 bg-emerald-50 dark:bg-emerald-950/20`
                : `${base} border-zinc-200 dark:border-zinc-700 opacity-40`;
        }
        if (selected === side && !isSource) {
            return `${base} border-rose-300 bg-rose-50/50 dark:bg-rose-950/10 dark:border-rose-800/40`;
        }
        return `${base} border-zinc-200 dark:border-zinc-700 hover:border-emerald-300 dark:hover:border-emerald-700 cursor-pointer`;
    };

    /* Curly arrow SVG: curves from source side to sink side */
    const arrowLR = 'M 6 18 Q 24 -2 42 18'; // left → right
    const arrowRL = 'M 42 18 Q 24 -2 6 18'; // right → left
    const headLR = '39,12 45,20 38,20';
    const headRL = '9,12 3,20 10,20';

    return (
        <div className="my-10 p-8 md:p-12 bg-white dark:bg-zinc-800 rounded-xl border border-zinc-200 dark:border-zinc-700">
            <h4 className="font-serif text-2xl font-semibold text-zinc-800 dark:text-white text-center">Curly Arrow Drill</h4>
            <p className="text-center text-sm text-zinc-500 dark:text-zinc-400 mb-2">Curly arrows always flow from electron SOURCE to electron SINK.</p>
            <p className="text-center text-xs text-zinc-400 dark:text-zinc-500 mb-6">Click the electron source in each pair.</p>

            {/* Progress */}
            <div className="mb-6">
                <div className="flex items-center justify-between mb-1.5">
                    <span className="text-[10px] font-bold uppercase tracking-wider text-zinc-400 dark:text-zinc-500">Progress</span>
                    <span className="text-[10px] font-bold text-emerald-600 dark:text-emerald-400">{Math.min(current + (isCorrect ? 1 : 0), scenarios.length)}/{scenarios.length}</span>
                </div>
                <div className="w-full h-2 bg-zinc-100 dark:bg-zinc-900 rounded-full overflow-hidden">
                    <motion.div
                        className="h-full rounded-full bg-emerald-400"
                        animate={{ width: `${(Math.min(current + (isCorrect ? 1 : 0), scenarios.length) / scenarios.length) * 100}%` }}
                        transition={{ type: 'spring', stiffness: 80, damping: 15 }}
                    />
                </div>
            </div>

            {!done ? (
                <AnimatePresence mode="wait">
                    <motion.div key={current} initial={{ opacity: 0, y: 10 }} animate={{ opacity: 1, y: 0 }} exit={{ opacity: 0, y: -10 }}>
                        <p className="text-center text-xs text-zinc-500 dark:text-zinc-400 mb-4">
                            Which is the electron <span className="font-bold text-emerald-600 dark:text-emerald-400">SOURCE</span>?
                        </p>

                        {/* Reaction pair */}
                        <div className="flex items-center justify-center gap-3 mb-4">
                            <button onClick={() => handleSelect('a')} disabled={isCorrect} className={btnClass('a')}>
                                <p className="text-2xl font-mono font-bold text-zinc-800 dark:text-white">{s.a.formula}</p>
                                <p className="text-[10px] text-zinc-500 dark:text-zinc-400 mt-1">{s.a.label}</p>
                            </button>

                            <div className="flex-shrink-0 w-12 h-6 flex items-center justify-center">
                                {isCorrect ? (
                                    <motion.svg initial={{ opacity: 0 }} animate={{ opacity: 1 }} width="48" height="24" viewBox="0 0 48 24">
                                        <motion.path
                                            d={s.a.isSource ? arrowLR : arrowRL}
                                            fill="none" stroke="#10b981" strokeWidth="2.5" strokeLinecap="round"
                                            initial={{ pathLength: 0 }} animate={{ pathLength: 1 }}
                                            transition={{ duration: 0.5 }}
                                        />
                                        <motion.polygon
                                            points={s.a.isSource ? headLR : headRL}
                                            fill="#10b981"
                                            initial={{ opacity: 0 }} animate={{ opacity: 1 }}
                                            transition={{ delay: 0.4 }}
                                        />
                                    </motion.svg>
                                ) : (
                                    <span className="text-lg font-bold text-zinc-300 dark:text-zinc-600">+</span>
                                )}
                            </div>

                            <button onClick={() => handleSelect('b')} disabled={isCorrect} className={btnClass('b')}>
                                <p className="text-2xl font-mono font-bold text-zinc-800 dark:text-white">{s.b.formula}</p>
                                <p className="text-[10px] text-zinc-500 dark:text-zinc-400 mt-1">{s.b.label}</p>
                            </button>
                        </div>

                        {/* Feedback */}
                        <AnimatePresence>
                            {selected && !isCorrect && (
                                <motion.p initial={{ opacity: 0 }} animate={{ opacity: 1 }}
                                    className="text-center text-xs text-rose-500 dark:text-rose-400 mb-3">
                                    That&apos;s the electron sink — it&apos;s electron-poor. Try the source.
                                </motion.p>
                            )}
                        </AnimatePresence>
                        {isCorrect && (
                            <motion.div initial={{ opacity: 0, y: 8 }} animate={{ opacity: 1, y: 0 }}
                                className="p-3 bg-emerald-50 dark:bg-emerald-950/20 border border-emerald-200 dark:border-emerald-800/40 rounded-xl text-center mb-4"
                            >
                                <p className="text-xs text-emerald-700 dark:text-emerald-300">{s.explanation}</p>
                            </motion.div>
                        )}
                        {isCorrect && (
                            <motion.div initial={{ opacity: 0 }} animate={{ opacity: 1 }} className="text-center">
                                <button onClick={handleNext}
                                    className="px-4 py-2 text-sm font-bold rounded-lg bg-emerald-500 hover:bg-emerald-600 text-white transition-colors">
                                    {current < scenarios.length - 1 ? 'Next Reaction' : 'See Results'}
                                </button>
                            </motion.div>
                        )}
                    </motion.div>
                </AnimatePresence>
            ) : (
                <motion.div initial={{ opacity: 0, y: 10 }} animate={{ opacity: 1, y: 0 }}
                    className="p-5 bg-emerald-50 dark:bg-emerald-950/20 rounded-xl border border-emerald-200 dark:border-emerald-800/40 text-center"
                >
                    <p className="text-3xl font-bold text-emerald-600 dark:text-emerald-400 mb-2">{score}/{scenarios.length}</p>
                    <p className="text-sm font-semibold text-emerald-700 dark:text-emerald-300">
                        {score === scenarios.length ? 'Perfect! You understand the source \u2192 sink principle.' : 'Remember: electrons always flow from rich to poor.'}
                    </p>
                    <p className="text-xs text-emerald-600/70 dark:text-emerald-400/60 mt-2">
                        The curly arrow always starts at the electron source (lone pair or bond) and points to the electron sink (electron-deficient atom).
                    </p>
                </motion.div>
            )}
        </div>
    );
};

// --- MODULE COMPONENT ---
const MasteringTheSciencesModule: React.FC<{ onBack: () => void; progress: ModuleProgress; onProgressUpdate: (progress: ModuleProgress) => void }> = ({ onBack, progress, onProgressUpdate }) => {
  const sections = [
    { id: 'hidden-curriculum', title: 'The Hidden Curriculum', eyebrow: '01 // The Master Key', icon: Key },
    { id: 'biology', title: 'Biology: Precision & Breadth', eyebrow: '02 // The Encyclopedia', icon: Leaf },
    { id: 'chemistry', title: 'Chemistry: Molecular Logic', eyebrow: '03 // The Architect', icon: Beaker },
    { id: 'physics', title: 'Physics: Abstract Logic', eyebrow: '04 // The Engineer', icon: Atom },
    { id: 'ag-science', title: 'Ag Science: The Scientific Method', eyebrow: '05 // The Investigator', icon: Sprout },
    { id: 'cognitive-strategies', title: 'Cognitive Grade Optimization', eyebrow: '06 // The Toolkit', icon: BrainCircuit },
    { id: 'action-plan', title: 'Your Action Plan', eyebrow: '07 // The Blueprint', icon: Flag },
  ];

  return (
    <ModuleLayout
      moduleNumber="03"
      moduleTitle="Mastering the Sciences"
      moduleSubtitle="The STEM Grade Optimization Protocol"
      moduleDescription={`A strategic deconstruction of the STEM exams, revealing the "hidden curriculum" of Biology, Chemistry, Physics, and Ag Science.`}
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
              <p>Success in the Leaving Cert sciences is not just a test of knowledge; it's a test of strategic alignment. Each subject--Biology, Chemistry, Physics, and Ag Science--has its own "hidden curriculum," an unwritten set of rules dictated by the marking scheme. Mastering this hidden curriculum is the key to unlocking a H1.</p>
              <p>This module provides the decryption key for each science, revealing the specific cognitive approach and "high-yield" content that delivers the most marks. You will learn to think like an examiner and engineer your answers for maximum credit.</p>
            </ReadingSection>
          )}
          {activeSection === 1 && (
            <ReadingSection title="Biology: Precision & Breadth." eyebrow="Step 2" icon={Leaf} theme={theme}>
              <p>Biology rewards breadth of knowledge and, above all, <Highlight description="The marking scheme demands specific, non-negotiable keywords. Synonyms are often rejected. 'Specificity' or 'induced fit model' must be used for the active site." theme={theme}>terminological precision</Highlight>. An answer without the correct keyword is worthless. Definitions must be memorized verbatim. The exam structure is 5-3-4 (5/7 shorts, 3/4 experiments, 4/6 longs), and omitting any of the 22 mandatory experiments is a dangerous strategy. Beware the <Highlight description="In Section A, an incorrect third answer to a two-part question can cancel out a correct one. Adhere strictly to the quantity requested." theme={theme}>'Surplus Answer' Risk</Highlight> in short questions.</p>
            </ReadingSection>
          )}
          {activeSection === 2 && (
            <ReadingSection title="Chemistry: Molecular Logic." eyebrow="Step 3" icon={Beaker} theme={theme}>
              <p>Chemistry demands dual competency: visualizing molecular interactions and executing complex calculations. Section A (experiments) is your <Highlight description="Section A, covering mandatory experiments like titrations, is highly predictable and can account for up to 38% of your grade if all three questions are answered." theme={theme}>Volumetric Anchor</Highlight>, offering predictable marks. Master the procedural precision of titrations and the visualization of organic apparatus.</p>
              <p>Organic Chemistry (40%) requires you to master reaction maps and the <Highlight description="A formalism showing the movement of electron pairs. A curly arrow MUST originate from a bond or lone pair and point to an atom. Errors here are severely penalized." theme={theme}>'Curly Arrow' Formalism</Highlight> for mechanisms. A "Texas Carbon" (five-bonded carbon) is a zero-mark error. Stoichiometry is foundational; every calculation must begin by converting to Moles.</p>
              <CurlyArrowDrill />
            </ReadingSection>
          )}
           {activeSection === 3 && (
            <ReadingSection title="Physics: Abstract Logic." eyebrow="Step 4" icon={Atom} theme={theme}>
              <p>Physics rewards the application of abstract concepts to novel problems. Section A is your experimental portfolio and the source of "easy" marks if you master <Highlight description="Key protocols like ensuring the independent variable is on the X-axis and calculating slope from the line of best fit, not table points." theme={theme}>graphing protocols</Highlight>. All derivations must be learned by heart, including the geometric steps.</p>
              <p>For novel questions, your secret weapon is <Highlight description="Using the units of physical quantities to deduce or check a formula (e.g., if Force is in N and Area is in m\u00b2, Pressure must be N/m\u00b2)." theme={theme}>Unit Algebra</Highlight>. Forgetting to convert from cm to m is the single most frequent cause of lost marks. Always double-check your calculator is in <strong>Degree</strong> mode for trigonometric functions.</p>
            </ReadingSection>
          )}
           {activeSection === 4 && (
            <ReadingSection title="Ag Science: The Scientific Method." eyebrow="Step 5" icon={Sprout} theme={theme}>
              <p>The new Ag Science course is a radical shift from "farming facts" to "scientific principles." The <Highlight description="An Individual Investigative Study worth 25% of the total grade. It requires a formal scientific report with a testable hypothesis, experimental design, and statistical analysis." theme={theme}>Individual Investigative Study (IIS)</Highlight> is a capstone project that demands scientific rigor. A descriptive project without a clear hypothesis will be heavily penalized.</p>
              <p>The written paper is now more <Highlight description="Linking topics across different strands (e.g., how fertilizer use in Crops affects water quality in the Environment strand)." theme={theme}>synoptic</Highlight>, demanding critical thinking and data analysis, not just recall. Questions on experiments require the same rigor as Biology or Physics.</p>
            </ReadingSection>
          )}
          {activeSection === 5 && (
            <ReadingSection title="Cognitive Grade Optimization." eyebrow="Step 6" icon={BrainCircuit} theme={theme}>
              <p>To master these diverse subjects, you must abandon passive re-reading. <Highlight description="Mixing different topics or subjects within a single study session. It feels harder but builds the crucial skill of identifying problem types." theme={theme}>Interleaving</Highlight> is superior to blocked practice for STEM subjects because it forces your brain to constantly "reload" context, strengthening retrieval pathways. A 90-minute session could involve a Physics problem, a Chemistry equation, and a Biology definition.</p>
              <p>The most effective method for memorizing the hundreds of definitions in Biology and Ag Science is a combination of <Highlight description="Forcing your brain to retrieve information from memory (e.g., using the 'Blurting' method)." theme={theme}>Active Recall</Highlight> and <Highlight description="Using tools like Anki or Quizlet to review information at increasing intervals, combating the 'forgetting curve'." theme={theme}>Spaced Repetition</Highlight>.</p>
            </ReadingSection>
          )}
          {activeSection === 6 && (
            <ReadingSection title="Your Action Plan." eyebrow="Step 7" icon={Flag} theme={theme}>
              <p>You now have the strategic blueprint for each of the Leaving Cert sciences. You understand the "hidden curriculum" and the specific cognitive tools required for each. The path to a H1 is not about working harder, but about working smarter, with strategic engagement with the assessment architecture.</p>
              <MicroCommitment theme={theme}>
                <p>Pick ONE subject. Go to the SEC website and download the most recent Chief Examiner's Report. Read only the "Recommendations to Candidates" section. You've just gained access to the official cheat sheet.</p>
              </MicroCommitment>
            </ReadingSection>
          )}
        </>
      )}
    </ModuleLayout>
  );
};
export default MasteringTheSciencesModule;
