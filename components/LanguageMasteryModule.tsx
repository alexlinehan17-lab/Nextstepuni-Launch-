
/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
*/

import React, { useState } from 'react';
import { motion, AnimatePresence, Reorder } from 'framer-motion';
import {
  Target, Brain, Languages, Mic, Headphones, BookOpen, PenSquare, Wrench
} from 'lucide-react';
import { ModuleProgress } from '../types';
import { skyTheme } from '../moduleThemes';
import { Highlight, ReadingSection, MicroCommitment } from './ModuleShared';
import { ModuleLayout } from './ModuleLayout';

const theme = skyTheme;

// --- INTERACTIVE COMPONENTS ---
const DualTrackPlanner = () => {
    const [plan, setPlan] = useState<'rescue'|'mastery'>('rescue');

    const rescuePlan = { "Oral": 20, "Reading": 40, "Aural": 25, "Written": 15};
    const masteryPlan = { "Oral": 25, "Reading": 30, "Aural": 20, "Written": 25};
    const currentPlan = plan === 'rescue' ? rescuePlan : masteryPlan;

    return(
        <div className="my-10 p-8 md:p-12 bg-white dark:bg-zinc-800 rounded-xl border border-zinc-200 dark:border-zinc-700">
             <h4 className="font-serif text-2xl font-semibold text-zinc-800 dark:text-white text-center">Dual-Track Strategy Planner</h4>
             <div className="flex justify-center gap-2 p-1 bg-zinc-100 dark:bg-zinc-800 rounded-full my-6 max-w-sm mx-auto">
                <button onClick={() => setPlan('rescue')} className={`w-full px-4 py-2 text-xs font-bold rounded-full ${plan === 'rescue' ? 'bg-white shadow' : ''}`}>Rescue Plan (Pass)</button>
                <button onClick={() => setPlan('mastery')} className={`w-full px-4 py-2 text-xs font-bold rounded-full ${plan === 'mastery' ? 'bg-white shadow' : ''}`}>Mastery Plan (H1)</button>
            </div>
            <div className="grid grid-cols-2 md:grid-cols-4 gap-4 text-center">
                {Object.entries(currentPlan).map(([component, value]) => (
                    <div key={component}>
                        <p className="font-bold text-sm">{component}</p>
                        <div className="w-full h-24 bg-zinc-100 dark:bg-zinc-800 rounded-lg mt-2 flex items-end">
                            <motion.div className="w-full bg-sky-400 rounded-t-lg" initial={{height:0}} animate={{height: `${value*2}%`}}/>
                        </div>
                        <p className="text-xl font-bold mt-1">{value}%</p>
                    </div>
                ))}
            </div>
        </div>
    );
};

const OralBlueprintSliders = () => {
    const [q, setQ] = useState({ pron: 50, vocab: 50, struct: 50, comm: 50 });

    const sliders = [
        { key: 'pron' as const, label: 'Pronunciation', weight: 20 },
        { key: 'vocab' as const, label: 'Vocabulary', weight: 20 },
        { key: 'struct' as const, label: 'Structure', weight: 30 },
        { key: 'comm' as const, label: 'Communication', weight: 30 },
    ];

    const totalScore = Math.round(sliders.reduce((s, sl) => s + q[sl.key] * (sl.weight / 100), 0));

    const getGrade = (score: number) => {
        if (score >= 90) return { label: 'H1', color: '#10b981' };
        if (score >= 80) return { label: 'H2', color: '#06b6d4' };
        if (score >= 70) return { label: 'H3', color: '#0ea5e9' };
        if (score >= 60) return { label: 'H4', color: '#3b82f6' };
        if (score >= 50) return { label: 'H5', color: '#f59e0b' };
        if (score >= 40) return { label: 'H6', color: '#f97316' };
        return { label: 'H7', color: '#ef4444' };
    };
    const grade = getGrade(totalScore);

    return (
        <div className="my-10 p-8 md:p-12 bg-white dark:bg-zinc-800 rounded-xl border border-zinc-200 dark:border-zinc-700">
            <h4 className="font-serif text-2xl font-semibold text-zinc-800 dark:text-white text-center">Oral Exam Blueprint</h4>
            <p className="text-center text-sm text-zinc-500 dark:text-zinc-400 mb-2">Adjust each quadrant to see how the weighted marking scheme affects your grade.</p>
            <p className="text-center text-xs text-zinc-400 dark:text-zinc-500 mb-8">Structure + Communication = 60% of marks. Focus there.</p>

            {/* Slider cards */}
            <div className="space-y-5 mb-8">
                {sliders.map(s => {
                    const value = q[s.key];
                    const contribution = Math.round(value * (s.weight / 100));
                    return (
                        <div key={s.key}>
                            <div className="flex items-center justify-between mb-2">
                                <div className="flex items-center gap-2">
                                    <span className="text-sm font-semibold text-zinc-700 dark:text-zinc-200">{s.label}</span>
                                    <span className="text-[9px] font-bold px-1.5 py-0.5 rounded-full bg-sky-100 dark:bg-sky-950/30 text-sky-600 dark:text-sky-400">{s.weight}%</span>
                                </div>
                                <div className="flex items-center gap-2">
                                    <span className="text-sm font-bold text-zinc-700 dark:text-zinc-200">{value}</span>
                                    <span className="text-[10px] text-zinc-400 dark:text-zinc-500">= {contribution} marks</span>
                                </div>
                            </div>
                            <div className="w-full h-1.5 bg-zinc-100 dark:bg-zinc-900 rounded-full overflow-hidden mb-2">
                                <motion.div
                                    className="h-full rounded-full bg-sky-400"
                                    animate={{ width: `${value}%` }}
                                    transition={{ type: 'spring', stiffness: 120, damping: 20 }}
                                />
                            </div>
                            <input type="range" min="0" max="100" value={value}
                                onChange={e => setQ({ ...q, [s.key]: parseInt(e.target.value) })}
                                className="w-full accent-sky-500" />
                        </div>
                    );
                })}
            </div>

            {/* Score panel */}
            <div className="p-5 rounded-xl border" style={{ backgroundColor: grade.color + '08', borderColor: grade.color + '30' }}>
                <p className="text-[10px] font-bold uppercase tracking-wider text-center text-zinc-400 dark:text-zinc-500 mb-2">Weighted Oral Grade</p>
                <div className="flex items-center justify-center gap-3 mb-4">
                    <motion.span
                        key={totalScore}
                        className="text-4xl font-bold"
                        style={{ color: grade.color }}
                        initial={{ scale: 0.9 }}
                        animate={{ scale: 1 }}
                    >
                        {totalScore}%
                    </motion.span>
                    <span className="text-lg font-bold px-3 py-1 rounded-full"
                        style={{ backgroundColor: grade.color + '18', color: grade.color }}>
                        {grade.label}
                    </span>
                </div>
                <div className="w-full h-2.5 bg-white/50 dark:bg-zinc-800/50 rounded-full overflow-hidden">
                    <motion.div
                        className="h-full rounded-full"
                        style={{ backgroundColor: grade.color }}
                        animate={{ width: `${totalScore}%` }}
                        transition={{ type: 'spring', stiffness: 80, damping: 18 }}
                    />
                </div>
                <div className="flex justify-between mt-1.5 px-0.5">
                    {['H7','H6','H5','H4','H3','H2','H1'].map(g => (
                        <span key={g} className={`text-[7px] ${grade.label === g ? 'font-bold' : ''}`}
                            style={{ color: grade.label === g ? grade.color : '#a1a1aa' }}>{g}</span>
                    ))}
                </div>
            </div>
        </div>
    );
};

const ParagraphSorter = () => {
    const [items, setItems] = useState([
        { id: 1, text: "Expansion/Reason" },
        { id: 2, text: "Topic Sentence" },
        { id: 3, text: "Connector/Bridge" },
        { id: 4, text: "Example" },
    ]);
    const correctOrder = [2, 1, 4, 3];
    const isCorrect = items.every((item, i) => item.id === correctOrder[i]);

    return (
        <div className="my-10 p-8 md:p-12 bg-white dark:bg-zinc-800 rounded-xl border border-zinc-200 dark:border-zinc-700">
            <h4 className="font-serif text-2xl font-semibold text-zinc-800 dark:text-white text-center">Paragraph Algorithm</h4>
            <p className="text-center text-sm text-zinc-500 dark:text-zinc-400 mb-6">Drag these components into the correct order to build a perfect essay paragraph.</p>
            <Reorder.Group axis="y" values={items} onReorder={setItems} className="space-y-2 max-w-sm mx-auto">
                {items.map(item => (
                    <Reorder.Item key={item.id} value={item} className="p-4 bg-zinc-100 dark:bg-zinc-800 rounded-lg text-center font-bold text-zinc-700 dark:text-zinc-200 cursor-grab active:cursor-grabbing">
                        {item.text}
                    </Reorder.Item>
                ))}
            </Reorder.Group>
            {isCorrect && <p className="text-center font-bold text-emerald-600 mt-4">Correct! This is the blueprint for a high-scoring paragraph.</p>}
        </div>
    );
};

// --- MODULE COMPONENT ---
const LanguageMasteryModule: React.FC<{ onBack: () => void; progress: ModuleProgress; onProgressUpdate: (progress: ModuleProgress) => void }> = ({ onBack, progress, onProgressUpdate }) => {
  const sections = [
    { id: 'dual-track', title: 'The Dual-Track Imperative', eyebrow: '01 // The Strategy', icon: Target },
    { id: 'oral-blueprint', title: 'The Oral Blueprint', eyebrow: '02 // The 25% Bank', icon: Mic },
    { id: 'examiner-forensics', title: 'Examiner Forensics', eyebrow: '03 // Killer Errors vs H1 Differentiators', icon: Brain },
    { id: 'vocab-vault', title: 'The Vocabulary Vault', eyebrow: '04 // SRS vs Goldlist', icon: Wrench },
    { id: 'auditory-processing', title: 'Auditory Processing', eyebrow: '05 // The Aural Exam', icon: Headphones },
    { id: 'reading-protocols', title: 'Reading Comprehension Protocols', eyebrow: '06 // Search & Extract', icon: BookOpen },
    { id: 'written-algorithms', title: 'Written Production Algorithms', eyebrow: '07 // The Paragraph Engine', icon: PenSquare },
    { id: 'mastery-plan', title: 'Your Mastery Plan', eyebrow: '08 // The Action Plan', icon: Languages },
  ];

  return (
    <ModuleLayout
      moduleNumber="02"
      moduleTitle="Mastering Languages"
      moduleSubtitle="The Language Mastery Protocol"
      moduleDescription="A strategic deconstruction of the MFL exams, providing a bifurcated strategy for both foundational proficiency and top-tier performance."
      theme={theme}
      sections={sections}
      onBack={onBack}
      progress={progress}
      onProgressUpdate={onProgressUpdate}
    >
      {(activeSection) => (
        <>
          {activeSection === 0 && (
            <ReadingSection title="The Dual-Track Imperative." eyebrow="Step 1" icon={Target} theme={theme}>
              <p>The Leaving Cert MFL exam isn't one test; it's two. For students at risk of failing, the goal is <Highlight description="The ability to transact meaning despite grammatical errors. This is the 'Rescue Plan'." theme={theme}>Communicative Proficiency</Highlight>. For students aiming for a H1, the goal is <Highlight description="Demonstrating syntactical complexity, idiomatic richness, and meta-cognitive control. This is the 'Mastery Plan'." theme={theme}>Language Awareness</Highlight>. A one-size-fits-all approach is a recipe for failure. Your strategy must match your target.</p>
              <p>The allocation of marks is a strategic map. A fatal error is focusing on written production when the Oral and Reading components offer a much higher return on investment, especially for students on the "Rescue Plan".</p>
              <DualTrackPlanner />
            </ReadingSection>
          )}
           {activeSection === 1 && (
            <ReadingSection title="The Oral Blueprint." eyebrow="Step 2" icon={Mic} theme={theme}>
              <p>The Oral is the highest ROI activity in the entire Leaving Cert. It happens before the written papers, allowing you to "bank" up to 25% of your final grade. The marking scheme is a universal algorithm, divided into four quadrants: <Highlight description="Intonation, rhythm, and accuracy of sounds (20%)." theme={theme}>Pronunciation</Highlight>, <Highlight description="Lexical richness and idiomatic language (20%)." theme={theme}>Vocabulary</Highlight>, <Highlight description="Grammatical accuracy and complexity (30%)." theme={theme}>Structure</Highlight>, and <Highlight description="Fluency, spontaneity, and sustaining interaction (30%)." theme={theme}>Communication</Highlight>.</p>
              <p>Understanding how these are weighted is key. Structure and Communication make up 60% of the marks. For the "Rescue Plan," the goal is verb control in the present tense. For the "Mastery Plan," it's about toggling tenses and deploying advanced structures like the Subjunctive.</p>
              <OralBlueprintSliders />
            </ReadingSection>
          )}
           {activeSection === 2 && (
            <ReadingSection title="Examiner Forensics." eyebrow="Step 3" icon={Brain} theme={theme}>
              <p>Chief Examiner Reports are the exam's "black box recorder," telling us exactly why students fail and succeed. The biggest <Highlight description="Errors that cap a student's grade, regardless of other strengths." theme={theme}>"Killer Error"</Highlight> is the "Rote Learning Penalty"—reciting a pre-learned essay that doesn't answer the question. This gets punished heavily in the Communication quadrant.</p>
              <p>Conversely, there are clear <Highlight description="Skills that reliably signal a top-tier student to an examiner." theme={theme}>"H1 Differentiators."</Highlight> In French and Spanish, the number one differentiator is the spontaneous, correct use of the <strong>Subjunctive Mood</strong>. In German, it's mastery of word order—the <strong>"Verb Kicker"</strong> rule. These aren't just grammar points; they are signals of high-level Language Awareness.</p>
            </ReadingSection>
          )}
          {activeSection === 3 && (
            <ReadingSection title="The Vocabulary Vault." eyebrow="Step 4" icon={Wrench} theme={theme}>
              <p>The Leaving Cert requires a massive vocabulary (2,000-3,000 words for a H1). This cannot be crammed. You need a system based on cognitive science. There are two main approaches.</p>
              <p><Highlight description="Software (like Anki) that uses algorithms to schedule flashcard reviews at the precise moment you're about to forget them. Highly efficient but can be high-maintenance." theme={theme}>Spaced Repetition Systems (SRS)</Highlight> are the digital, high-efficiency option. The <Highlight description="A low-tech, low-stress method involving writing lists of words in a notebook and reviewing them after a two-week 'incubation' period. Excellent for passive vocabulary." theme={theme}>Goldlist Method</Highlight> is the analog, low-stress alternative, relying on the physical act of writing to aid retention. The best strategy is often a hybrid: SRS for active vocabulary (production) and Goldlist for passive vocabulary (recognition).</p>
            </ReadingSection>
          )}
          {activeSection === 4 && (
            <ReadingSection title="Auditory Processing." eyebrow="Step 5" icon={Headphones} theme={theme}>
              <p>The Aural (Listening) exam is not a passive activity. It requires active processing strategies. The most important is <Highlight description="Using the pre-listening reading time to analyze the questions and predict the *type* of answer required (e.g., a number, a place, an emotion)." theme={theme}>Prediction & Priming</Highlight>. This tunes your brain to listen for specific information.</p>
              <p>To improve your ear, you need <Highlight description="Listening to native materials to internalize the rhythm and intonation of the language." theme={theme}>Contextual Immersion</Highlight>. Resources like "News in Slow French/German/Spanish" are perfect. A powerful technique is <Highlight description="Listening to a native speaker and repeating what they say almost simultaneously. This builds a direct link between your auditory and motor cortex, dramatically improving pronunciation." theme={theme}>Shadowing</Highlight>, which is the ultimate hack for your Pronunciation marks in the Oral.</p>
            </ReadingSection>
          )}
          {activeSection === 5 && (
            <ReadingSection title="Reading Protocols." eyebrow="Step 6" icon={BookOpen} theme={theme}>
              <p>The Reading Comprehension is the single largest component for Ordinary Level students (40%). The biggest trap is trying to translate every word. The expert strategy is <Highlight description="The technique of underlining keywords in the question and scanning the text for them, knowing that answers almost always appear in chronological order." theme={theme}>"Search and Extract."</Highlight></p>
              <p>Beware the <Highlight description="A critical distinction in French exams. 'Trouvez' means quote exactly; 'Indiquez' means manipulate the language (e.g., change 'je' to 'il'). Failure to distinguish these is a major source of lost marks." theme={theme}>"Manipulation Rule"</Highlight> in French. If the question says "Trouvez," you quote. If it says "Indiquez" or "Dites," you must change the grammar. This is a classic differentiator between H1 and H2 students.</p>
            </ReadingSection>
          )}
           {activeSection === 6 && (
            <ReadingSection title="Written Algorithms." eyebrow="Step 7" icon={PenSquare} theme={theme}>
              <p>High-scoring essays are not works of creative genius; they are assembled using pre-fabricated, high-quality components. Every paragraph should follow a strict <Highlight description="A 4-part structure for building coherent paragraphs: 1. Topic Sentence, 2. Expansion/Reason, 3. Example, 4. Connector/Bridge to the next point." theme={theme}>Paragraph Algorithm</Highlight>.</p>
              <p>For the "Mastery Plan," the goal is to use sophisticated logical connectors (e.g., *N\u00e9anmoins*, *De surcro\u00eet*) and avoid starting sentences with basic words like "Et" or "Mais." This signals high-level Language Awareness to the examiner.</p>
              <ParagraphSorter />
            </ReadingSection>
          )}
          {activeSection === 7 && (
            <ReadingSection title="Your Mastery Plan." eyebrow="Step 8" icon={Languages} theme={theme}>
                <p>You now have the complete strategic blueprint for the Leaving Cert MFL exams. You understand the dual-track system, the importance of each component, and the specific cognitive and tactical tools required for success. The exam is not a mystery; it is a system that can be engineered.</p>
                <MicroCommitment theme={theme}>
                  <p>Pick ONE strategy from this module. Whether it's the "Search and Extract" technique, the Paragraph Algorithm, or starting a Goldlist notebook. Commit to trying it just once this week. You've just taken your first step from being a language student to a language engineer.</p>
                </MicroCommitment>
            </ReadingSection>
          )}
        </>
      )}
    </ModuleLayout>
  );
};
export default LanguageMasteryModule;
