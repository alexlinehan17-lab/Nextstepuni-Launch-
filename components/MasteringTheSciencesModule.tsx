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
    const [start, setStart] = useState(false);
    const [end, setEnd] = useState(false);

    return(
        <div className="my-10 p-8 md:p-12 bg-white dark:bg-zinc-800 rounded-xl border border-zinc-200 dark:border-zinc-700 text-center">
            <h4 className="font-serif text-2xl font-semibold text-zinc-800 dark:text-white text-center">"Curly Arrow" Drill</h4>
            <p className="text-sm text-zinc-500 dark:text-zinc-400 mb-6">Draw the arrow for this step: Cl\u207b attacking a carbocation.</p>
            <div className="flex justify-center items-center gap-4 text-3xl font-mono">
                <button onClick={() => setStart(true)} className="relative p-2">Cl<span className="absolute -top-1 -right-1 text-lg">-</span></button>
                <span>+</span>
                <button onClick={() => setEnd(true)} className="relative p-2">C<span className="absolute -top-1 -right-1 text-lg">+</span></button>
            </div>
            {start && end && <p className="text-emerald-600 font-bold mt-4">Correct! Arrow from electron source (Cl\u207b) to electron sink (C\u207a).</p>}
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
              <p>For novel questions, your secret weapon is <Highlight description="Using the units of physical quantities to deduce or check a formula (e.g., if Force is in N and Area is in m\u00b2, Pressure must be N/m\u00b2)." theme={theme}>Unit Algebra</Highlight>. Forgetting to convert from cm to m is the single most frequent cause of lost marks. Always double-check your calculator is in **Degree** mode for trigonometric functions.</p>
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
