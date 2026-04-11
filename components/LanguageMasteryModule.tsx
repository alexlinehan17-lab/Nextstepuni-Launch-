
/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
*/

import React, { useState } from 'react';
import { motion, Reorder } from 'framer-motion';
import {
  Target, Brain, Languages, Mic, Headphones, BookOpen, PenSquare, Wrench
} from 'lucide-react';
import { type ModuleProgress } from '../types';
import { skyTheme } from '../moduleThemes';
import { Highlight, ReadingSection, MicroCommitment, PersonalStory } from './ModuleShared';
import { ModuleLayout } from './ModuleLayout';

const theme = skyTheme;

// --- INTERACTIVE COMPONENTS ---
const DualTrackPlanner = () => {
    const [plan, setPlan] = useState<'rescue'|'mastery'>('rescue');

    const rescuePlan = { "Oral": 20, "Reading": 40, "Aural": 25, "Written": 15};
    const masteryPlan = { "Oral": 25, "Reading": 30, "Aural": 20, "Written": 25};
    const currentPlan = plan === 'rescue' ? rescuePlan : masteryPlan;

    return(
        <div className="my-10 rounded-2xl p-6 md:p-8" style={{ backgroundColor: '#F8F8F8', borderRadius: 18 }}>
             <h4 className="font-serif text-2xl font-semibold text-zinc-800 dark:text-white text-center">Your Study Plan Breakdown</h4>
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
        <div className="my-10 rounded-2xl p-6 md:p-8" style={{ backgroundColor: '#F8F8F8', borderRadius: 18 }}>
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
                                className="chunky-slider chunky-slider-teal" />
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
        <div className="my-10 rounded-2xl p-6 md:p-8" style={{ backgroundColor: '#F8F8F8', borderRadius: 18 }}>
            <h4 className="font-serif text-2xl font-semibold text-zinc-800 dark:text-white text-center">Paragraph Builder</h4>
            <p className="text-center text-sm text-zinc-500 dark:text-zinc-400 mb-6">Drag these into the right order to build a top-scoring essay paragraph.</p>
            <Reorder.Group axis="y" values={items} onReorder={setItems} className="space-y-2 max-w-sm mx-auto">
                {items.map(item => (
                    <Reorder.Item
                        key={item.id}
                        value={item}
                        className="p-4 text-center font-bold text-zinc-700 dark:text-zinc-200 cursor-grab active:cursor-grabbing"
                        style={{ backgroundColor: '#FFFFFF', border: '2.5px solid #1C1917', borderRadius: 16, boxShadow: '4px 4px 0px 0px #1C1917' }}
                        whileDrag={{ scale: 1.03, y: -2, boxShadow: '6px 6px 0px 0px #1C1917' }}
                    >
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
    { id: 'dual-track', title: 'Two Plans, One Goal', eyebrow: '01 // Your Game Plan', icon: Target },
    { id: 'oral-blueprint', title: 'The Oral Exam', eyebrow: '02 // Bank 25% Early', icon: Mic },
    { id: 'examiner-forensics', title: 'What Examiners Actually Want', eyebrow: '03 // Common Mistakes vs Top Marks', icon: Brain },
    { id: 'vocab-vault', title: 'Building Your Vocabulary', eyebrow: '04 // Making Words Stick', icon: Wrench },
    { id: 'auditory-processing', title: 'The Listening Exam', eyebrow: '05 // Training Your Ear', icon: Headphones },
    { id: 'reading-protocols', title: 'Reading Comprehension', eyebrow: '06 // Find the Answer Fast', icon: BookOpen },
    { id: 'written-algorithms', title: 'Writing Strong Essays', eyebrow: '07 // Building Great Paragraphs', icon: PenSquare },
    { id: 'mastery-plan', title: 'Your Action Plan', eyebrow: '08 // Make It Happen', icon: Languages },
  ];

  return (
    <ModuleLayout
      moduleNumber="02"
      moduleTitle="Mastering Languages"
      moduleSubtitle="Your Complete Guide to the Language Exams"
      moduleDescription="Whether you're aiming to pass or chasing a H1, this module breaks down exactly how the Leaving Cert language exams work and how to get the most out of every section."
      theme={theme}
      sections={sections}
      onBack={onBack}
      progress={progress}
      onProgressUpdate={onProgressUpdate}
      finishButtonText="Find Your Voice"
    >
      {(activeSection) => (
        <>
          {activeSection === 0 && (
            <ReadingSection title="Two Plans, One Goal." eyebrow="Step 1" icon={Target} theme={theme}>
              <p>Here's the thing most people miss: the Leaving Cert language exam isn't really one test -- it's two different challenges. If you're trying to get a solid pass, your goal is <Highlight description="Getting your meaning across clearly, even if your grammar isn't perfect. This is the 'Pass Plan'." theme={theme}>getting your message across</Highlight>. If you're going for a H1, you need to show the examiner you can <Highlight description="Using a range of tenses, expressions, and showing you really understand how the language works. This is the 'H1 Plan'." theme={theme}>really handle the language</Highlight>. Trying to do the same thing for both goals is a mistake -- your plan needs to match your target.</p>
              <p>Look at where the marks actually are. One of the biggest mistakes students make is spending all their time on essay writing when the Oral and Reading sections can give you way more marks for less effort -- especially if you're on the "Pass Plan".</p>
              <DualTrackPlanner />
            </ReadingSection>
          )}
           {activeSection === 1 && (
            <ReadingSection title="The Oral Exam." eyebrow="Step 2" icon={Mic} theme={theme}>
              <p>The Oral is the single best opportunity in the entire Leaving Cert. It happens before your written papers, so you can lock in up to 25% of your final grade early. The examiner marks you on four things: <Highlight description="How natural you sound -- your accent, rhythm, and how clearly you say words (worth 20%)." theme={theme}>Pronunciation</Highlight>, <Highlight description="The range of words and phrases you use, including natural expressions (worth 20%)." theme={theme}>Vocabulary</Highlight>, <Highlight description="Whether your grammar is correct and whether you use a range of tenses and sentence types (worth 30%)." theme={theme}>Structure</Highlight>, and <Highlight description="How well you keep the conversation going, respond naturally, and stay on topic (worth 30%)." theme={theme}>Communication</Highlight>.</p>
              <p>Notice how the marks are split: Structure and Communication together are worth 60%. That's where your focus should be. If you're aiming for a pass, nail your verbs in the present tense. If you're going for a H1, you need to switch between tenses smoothly and throw in some advanced grammar like the Subjunctive.</p>
              <OralBlueprintSliders />
            </ReadingSection>
          )}
           {activeSection === 2 && (
            <ReadingSection title="What Examiners Actually Want." eyebrow="Step 3" icon={Brain} theme={theme}>
              <p>The examiner reports tell us exactly what trips students up and what gets the top marks. The biggest <Highlight description="Mistakes that put a ceiling on your grade, no matter how good the rest of your work is." theme={theme}>grade-killer</Highlight> is learning an essay off by heart and writing it out even when it doesn't properly answer the question. Examiners spot this immediately and it tanks your Communication marks.</p>
              <p>On the flip side, there are specific things that scream "this student deserves a H1" to an examiner. These are <Highlight description="The specific skills that show the examiner you're operating at the top level." theme={theme}>H1 signals</Highlight>. In French and Spanish, the number one signal is using the <strong>Subjunctive</strong> correctly and naturally. In German, it's nailing the word order -- the <strong>"Verb Kicker"</strong> rule. These aren't just grammar rules to memorise; they show the examiner you genuinely understand the language.</p>
              <PersonalStory name="Saoirse" role="6th Year, Galway">
                <p>I was getting H4s in French all through 5th year. I was learning off essays and hoping for the best. Then I stopped doing that and focused on actually answering the question using three or four structures I knew really well. I started getting H2s in the mocks. The Subjunctive felt impossible at first, but once I had a few phrases down, it became automatic. I ended up getting a H1 in the Leaving Cert.</p>
              </PersonalStory>
            </ReadingSection>
          )}
          {activeSection === 3 && (
            <ReadingSection title="Building Your Vocabulary." eyebrow="Step 4" icon={Wrench} theme={theme}>
              <p>To hit a H1, you need somewhere between 2,000 and 3,000 words. That's a lot, and you absolutely cannot cram it. You need a system that actually works with how your brain remembers things. There are two solid approaches.</p>
              <p><Highlight description="Free apps like Anki that show you flashcards right before you'd forget them. Really effective, but you need to keep up with it daily." theme={theme}>Spaced repetition apps</Highlight> (like Anki -- it's free) are the digital option. They show you words right before you'd forget them, so you learn faster. The <Highlight description="A simple notebook method: write out word lists, leave them for two weeks, then come back and test yourself. Low effort, great for words you just need to recognise." theme={theme}>Goldlist Method</Highlight> is the low-tech option -- you write word lists in a notebook and come back to them after two weeks. No app needed, just a pen and paper. The best approach? Use both: apps for words you need to produce in essays, and the notebook method for words you just need to recognise in reading and listening.</p>
            </ReadingSection>
          )}
          {activeSection === 4 && (
            <ReadingSection title="The Listening Exam." eyebrow="Step 5" icon={Headphones} theme={theme}>
              <p>The listening exam is not about sitting back and hoping you catch something. You need to be actively working before you even hear the audio. The most important trick is <Highlight description="Use the reading time before each clip to read the questions and figure out what kind of answer you need -- is it a number? A place? A feeling? This tells your brain what to listen for." theme={theme}>reading ahead</Highlight>. During the reading time, look at the questions and figure out what kind of answer you need (a number? a place? a feeling?). This primes your brain to pick out the right information.</p>
              <p>To get better at understanding spoken language, you need to <Highlight description="Listen to real content in your target language to get used to the speed and rhythm. Free resources like 'News in Slow French' on YouTube are perfect for this." theme={theme}>listen to real content regularly</Highlight>. Free resources like "News in Slow French/German/Spanish" on YouTube are brilliant for this. Another great technique is <Highlight description="Listen to someone speaking in your target language and try to repeat what they say at the same time, almost like an echo. It trains your ear and your pronunciation together." theme={theme}>shadowing</Highlight> -- you listen to a native speaker and repeat what they say almost at the same time, like an echo. It's one of the best ways to improve both your listening and your pronunciation for the Oral.</p>
            </ReadingSection>
          )}
          {activeSection === 5 && (
            <ReadingSection title="Reading Comprehension." eyebrow="Step 6" icon={BookOpen} theme={theme}>
              <p>For Ordinary Level students, the reading comprehension is the single biggest section -- worth 40% of your marks. The biggest trap? Trying to translate every single word. You don't need to. The smart approach is <Highlight description="Underline the key words in the question, then scan the text looking for those words or their synonyms. The answers nearly always appear in the same order as the questions." theme={theme}>search and extract</Highlight> -- underline the key words in the question, then scan the text for those words. The answers almost always appear in the same order as the questions.</p>
              <p>If you're doing French, watch out for the <Highlight description="In French exams, 'Trouvez' means copy the answer exactly from the text. But 'Indiquez' or 'Dites' means you need to change the grammar -- like swapping 'je' for 'il'. Missing this costs a lot of students marks." theme={theme}>quote vs. rephrase trap</Highlight>. If the question says "Trouvez," you copy the answer word-for-word from the text. But if it says "Indiquez" or "Dites," you have to change the grammar (e.g., swap "je" for "il"). This catches out loads of students and it's often the difference between a H1 and a H2.</p>
            </ReadingSection>
          )}
           {activeSection === 6 && (
            <ReadingSection title="Writing Strong Essays." eyebrow="Step 7" icon={PenSquare} theme={theme}>
              <p>Here's a secret: top-scoring essays aren't written by geniuses. They're built from a set of reliable building blocks. Every paragraph should follow a simple <Highlight description="A 4-part recipe: 1. Start with your main point, 2. Explain or give a reason, 3. Give an example, 4. Link to the next point." theme={theme}>paragraph formula</Highlight>.</p>
              <p>If you're going for a H1, use linking words that go beyond the basics. Instead of "Et" or "Mais," try things like *N\u00e9anmoins* (however) or *De surcro\u00eet* (furthermore). These small upgrades show the examiner you're comfortable with the language at a high level.</p>
              <ParagraphSorter />
            </ReadingSection>
          )}
          {activeSection === 7 && (
            <ReadingSection title="Your Action Plan." eyebrow="Step 8" icon={Languages} theme={theme}>
                <p>You've now got a clear picture of how the Leaving Cert language exams actually work. You know which sections are worth the most marks, what examiners are looking for, and the specific techniques that separate top students from the rest. The exam isn't a mystery -- it's a system, and now you know how it works.</p>
                <MicroCommitment theme={theme}>
                  <p>Pick ONE thing from this module to try this week. Maybe it's the "search and extract" technique for reading, the paragraph formula for writing, or just starting a vocabulary notebook. One small step. That's all it takes to get started.</p>
                </MicroCommitment>
            </ReadingSection>
          )}
        </>
      )}
    </ModuleLayout>
  );
};
export default LanguageMasteryModule;
