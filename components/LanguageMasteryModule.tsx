
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
import { useEssentialsMode } from '../hooks/useEssentialsMode';
import { AnswerGroup, AnswerLine, ExerciseRange, ExerciseSheet } from './learning/Exercise';
import { ChoiceTile } from './ui/Choice';

const theme = skyTheme;

// --- INTERACTIVE COMPONENTS ---
const DualTrackPlanner = () => {
    const [plan, setPlan] = useState<'rescue'|'mastery'>('rescue');

    const rescuePlan = { "Oral": 20, "Reading": 40, "Aural": 25, "Written": 15};
    const masteryPlan = { "Oral": 25, "Reading": 30, "Aural": 20, "Written": 25};
    const currentPlan = plan === 'rescue' ? rescuePlan : masteryPlan;

    return(
        <ExerciseSheet title="Your Study Plan Breakdown" name="DualTrackPlanner">
             {/* The two plans: one is chosen (an ink outline, not a grey pill bar) */}
             <AnswerGroup kind="one" columns={2}>
                <ChoiceTile tile chosen={plan === 'rescue'} onClick={() => setPlan('rescue')} label="Rescue Plan (Pass)" />
                <ChoiceTile tile chosen={plan === 'mastery'} onClick={() => setPlan('mastery')} label="Mastery Plan (H1)" />
            </AnswerGroup>
            {/* The plan's split, drawn as bars on the sheet: an ink bar on a hairline track */}
            <div className="grid grid-cols-2 md:grid-cols-4 gap-4 text-center">
                {Object.entries(currentPlan).map(([component, value]) => (
                    <div key={component}>
                        <p className="ex-label">{component}</p>
                        <div className="w-full h-24 mt-2 flex items-end overflow-hidden" style={{ backgroundColor: 'var(--hairline)', borderRadius: 'var(--r-sm)' }}>
                            <motion.div className="w-full" style={{ backgroundColor: 'var(--ink-primary)' }} initial={{height:0}} animate={{height: `${value*2}%`}}/>
                        </div>
                        <p className="t-row text-ink-primary mt-1 tabular-nums">{value}%</p>
                    </div>
                ))}
            </div>
        </ExerciseSheet>
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
        <ExerciseSheet title="Oral Exam Blueprint" sub="Adjust each quadrant to see how the weighted marking scheme affects your grade." name="OralBlueprintSliders">
            <p className="t-meta">Structure + Communication = 60% of marks. Focus there.</p>

            {/* The four sliders: each one's name, its weight and what it earns, then the one shared slider */}
            <div className="ex-sliders">
                {sliders.map(s => {
                    const value = q[s.key];
                    const contribution = Math.round(value * (s.weight / 100));
                    return (
                        <div key={s.key} className="ex-slider">
                            <div className="flex items-baseline justify-between gap-3">
                                <div className="flex items-baseline gap-2">
                                    <span className="ex-slider-name">{s.label}</span>
                                    <span className="t-meta">{s.weight}%</span>
                                </div>
                                <div className="flex items-baseline gap-2">
                                    <span className="ui-readout text-ink-primary">{value}</span>
                                    <span className="t-meta">= {contribution} marks</span>
                                </div>
                            </div>
                            <ExerciseRange min="0" max="100" value={value}
                                onChange={e => setQ({ ...q, [s.key]: parseInt(e.target.value) })}
                                aria-label={s.label} />
                        </div>
                    );
                })}
            </div>

            {/* The grade it comes to: under a hairline, the figure and the grade in ink (no tinted panel or pill) */}
            <div className="ex-result">
                <p className="ex-label">Weighted Oral Grade</p>
                <div className="flex items-baseline gap-3">
                    <motion.span
                        key={totalScore}
                        className="ex-result-name tabular-nums"
                        initial={{ scale: 0.9 }}
                        animate={{ scale: 1 }}
                    >
                        {totalScore}%
                    </motion.span>
                    <span className="t-row text-ink-primary">
                        {grade.label}
                    </span>
                </div>
                <div className="w-full h-1 rounded-sm overflow-hidden mt-2" style={{ backgroundColor: 'var(--hairline)' }}>
                    <motion.div
                        className="h-full"
                        style={{ backgroundColor: 'var(--ink-primary)' }}
                        animate={{ width: `${totalScore}%` }}
                        transition={{ type: 'spring', stiffness: 80, damping: 18 }}
                    />
                </div>
                <div className="flex justify-between px-0.5">
                    {['H7','H6','H5','H4','H3','H2','H1'].map(g => (
                        <span key={g} className="t-label"
                            style={{ color: grade.label === g ? 'var(--ink-primary)' : 'var(--ink-muted)' }}>{g}</span>
                    ))}
                </div>
            </div>
        </ExerciseSheet>
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
        <ExerciseSheet title="Paragraph Builder" sub="Drag these into the right order to build a top-scoring essay paragraph." name="ParagraphSorter">
            {/* The four parts you drag: boxes with a line, no shadow */}
            <Reorder.Group axis="y" values={items} onReorder={setItems} className="ex-cards">
                {items.map(item => (
                    <Reorder.Item
                        key={item.id}
                        value={item}
                        className="flex items-center gap-3 min-h-[56px] cursor-grab active:cursor-grabbing t-body text-ink-primary"
                        style={{ backgroundColor: 'var(--surface-paper)', border: '1px solid var(--outline-soft)', borderRadius: 'var(--r-ctl)', padding: '13px 14px 13px 16px', boxShadow: 'none' }}
                        whileDrag={{ scale: 1.03, y: -2, boxShadow: 'none' }}
                    >
                        {item.text}
                    </Reorder.Item>
                ))}
            </Reorder.Group>
            {isCorrect && <AnswerLine>Correct! This is the blueprint for a high-scoring paragraph.</AnswerLine>}
        </ExerciseSheet>
    );
};

// --- MODULE COMPONENT ---
const LanguageMasteryModule: React.FC<{ onBack: () => void; progress: ModuleProgress; onProgressUpdate: (progress: ModuleProgress) => void }> = ({ onBack, progress, onProgressUpdate }) => {
  const essentials = useEssentialsMode();
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
              {essentials ? (<>
              <p>Your study plan depends on your target. For a pass, focus on <Highlight description="Getting your meaning across clearly, even if your grammar isn't perfect. This is the 'Pass Plan'." theme={theme}>getting your message across</Highlight>. For a H1, show you can <Highlight description="Using a range of tenses, expressions, and showing you really understand how the language works. This is the 'H1 Plan'." theme={theme}>really handle the language</Highlight>. Do not spend all your time on essay writing. The Oral and Reading sections give you more marks for less effort. Match your plan to your goal.</p>
              </>) : (<>
              <p>Here's the thing most people miss: the Leaving Cert language exam isn't really one test -- it's two different challenges. If you're trying to get a solid pass, your goal is <Highlight description="Getting your meaning across clearly, even if your grammar isn't perfect. This is the 'Pass Plan'." theme={theme}>getting your message across</Highlight>. If you're going for a H1, you need to show the examiner you can <Highlight description="Using a range of tenses, expressions, and showing you really understand how the language works. This is the 'H1 Plan'." theme={theme}>really handle the language</Highlight>. Trying to do the same thing for both goals is a mistake -- your plan needs to match your target.</p>
              <p>Look at where the marks actually are. One of the biggest mistakes students make is spending all their time on essay writing when the Oral and Reading sections can give you way more marks for less effort -- especially if you're on the "Pass Plan".</p>
              </>)}
              <DualTrackPlanner />
            </ReadingSection>
          )}
           {activeSection === 1 && (
            <ReadingSection title="The Oral Exam." eyebrow="Step 2" icon={Mic} theme={theme}>
              {essentials ? (<>
              <p>The Oral locks in up to 25% of your grade before written exams. You are marked on <Highlight description="How natural you sound -- your accent, rhythm, and how clearly you say words (worth 20%)." theme={theme}>Pronunciation</Highlight> (20%), <Highlight description="The range of words and phrases you use, including natural expressions (worth 20%)." theme={theme}>Vocabulary</Highlight> (20%), <Highlight description="Whether your grammar is correct and whether you use a range of tenses and sentence types (worth 30%)." theme={theme}>Structure</Highlight> (30%), and <Highlight description="How well you keep the conversation going, respond naturally, and stay on topic (worth 30%)." theme={theme}>Communication</Highlight> (30%). Structure and Communication are 60% combined. Focus there. For a pass, nail present tense verbs. For a H1, switch tenses smoothly.</p>
              </>) : (<>
              <p>The Oral is the single best opportunity in the entire Leaving Cert. It happens before your written papers, so you can lock in up to 25% of your final grade early. The examiner marks you on four things: <Highlight description="How natural you sound -- your accent, rhythm, and how clearly you say words (worth 20%)." theme={theme}>Pronunciation</Highlight>, <Highlight description="The range of words and phrases you use, including natural expressions (worth 20%)." theme={theme}>Vocabulary</Highlight>, <Highlight description="Whether your grammar is correct and whether you use a range of tenses and sentence types (worth 30%)." theme={theme}>Structure</Highlight>, and <Highlight description="How well you keep the conversation going, respond naturally, and stay on topic (worth 30%)." theme={theme}>Communication</Highlight>.</p>
              <p>Notice how the marks are split: Structure and Communication together are worth 60%. That's where your focus should be. If you're aiming for a pass, nail your verbs in the present tense. If you're going for a H1, you need to switch between tenses smoothly and throw in some advanced grammar like the Subjunctive.</p>
              </>)}
              <OralBlueprintSliders />
            </ReadingSection>
          )}
           {activeSection === 2 && (
            <ReadingSection title="What Examiners Actually Want." eyebrow="Step 3" icon={Brain} theme={theme}>
              {essentials ? (<>
              <p>The biggest <Highlight description="Mistakes that put a ceiling on your grade, no matter how good the rest of your work is." theme={theme}>grade-killer</Highlight>: learning an essay off by heart and writing it even when it does not answer the question. Examiners spot this instantly. For <Highlight description="The specific skills that show the examiner you're operating at the top level." theme={theme}>H1 signals</Highlight>: in French and Spanish, use the Subjunctive naturally. In German, nail word order. These show you truly understand the language.</p>
              </>) : (<>
              <p>The examiner reports tell us exactly what trips students up and what gets the top marks. The biggest <Highlight description="Mistakes that put a ceiling on your grade, no matter how good the rest of your work is." theme={theme}>grade-killer</Highlight> is learning an essay off by heart and writing it out even when it doesn't properly answer the question. Examiners spot this immediately and it tanks your Communication marks.</p>
              <p>On the flip side, there are specific things that scream "this student deserves a H1" to an examiner. These are <Highlight description="The specific skills that show the examiner you're operating at the top level." theme={theme}>H1 signals</Highlight>. In French and Spanish, the number one signal is using the <strong>Subjunctive</strong> correctly and naturally. In German, it's nailing the word order -- the <strong>"Verb Kicker"</strong> rule. These aren't just grammar rules to memorise; they show the examiner you genuinely understand the language.</p>
              </>)}
              <PersonalStory name="Saoirse" role="6th Year, Galway">
                <p>I was getting H4s in French all through 5th year. I was learning off essays and hoping for the best. Then I stopped doing that and focused on actually answering the question using three or four structures I knew really well. I started getting H2s in the mocks. The Subjunctive felt impossible at first, but once I had a few phrases down, it became automatic. I ended up getting a H1 in the Leaving Cert.</p>
              </PersonalStory>
            </ReadingSection>
          )}
          {activeSection === 3 && (
            <ReadingSection title="Building Your Vocabulary." eyebrow="Step 4" icon={Wrench} theme={theme}>
              {essentials ? (<>
              <p>You need 2,000-3,000 words for a H1. You cannot cram this. Use <Highlight description="Free apps like Anki that show you flashcards right before you'd forget them. Really effective, but you need to keep up with it daily." theme={theme}>Spaced repetition apps</Highlight> like Anki (free) for words you write in essays. Use the <Highlight description="A simple notebook method: write out word lists, leave them for two weeks, then come back and test yourself. Low effort, great for words you just need to recognise." theme={theme}>Goldlist Method</Highlight> (write word lists, return in two weeks) for words you just need to recognise. Use both together for best results.</p>
              </>) : (<>
              <p>To hit a H1, you need somewhere between 2,000 and 3,000 words. That's a lot, and you absolutely cannot cram it. You need a system that actually works with how your brain remembers things. There are two solid approaches.</p>
              <p><Highlight description="Free apps like Anki that show you flashcards right before you'd forget them. Really effective, but you need to keep up with it daily." theme={theme}>Spaced repetition apps</Highlight> (like Anki -- it's free) are the digital option. They show you words right before you'd forget them, so you learn faster. The <Highlight description="A simple notebook method: write out word lists, leave them for two weeks, then come back and test yourself. Low effort, great for words you just need to recognise." theme={theme}>Goldlist Method</Highlight> is the low-tech option -- you write word lists in a notebook and come back to them after two weeks. No app needed, just a pen and paper. The best approach? Use both: apps for words you need to produce in essays, and the notebook method for words you just need to recognise in reading and listening.</p>
              </>)}
            </ReadingSection>
          )}
          {activeSection === 4 && (
            <ReadingSection title="The Listening Exam." eyebrow="Step 5" icon={Headphones} theme={theme}>
              {essentials ? (<>
              <p>Before the audio plays, use <Highlight description="Use the reading time before each clip to read the questions and figure out what kind of answer you need -- is it a number? A place? A feeling? This tells your brain what to listen for." theme={theme}>reading ahead</Highlight>: read the questions and figure out what answer type you need. This primes your brain. To train your ear, <Highlight description="Listen to real content in your target language to get used to the speed and rhythm. Free resources like 'News in Slow French' on YouTube are perfect for this." theme={theme}>listen to real content regularly</Highlight> (try "News in Slow French" on YouTube). Try <Highlight description="Listen to someone speaking in your target language and try to repeat what they say at the same time, almost like an echo. It trains your ear and your pronunciation together." theme={theme}>shadowing</Highlight>: repeat what a speaker says in real time. This trains listening and pronunciation together.</p>
              </>) : (<>
              <p>The listening exam is not about sitting back and hoping you catch something. You need to be actively working before you even hear the audio. The most important trick is <Highlight description="Use the reading time before each clip to read the questions and figure out what kind of answer you need -- is it a number? A place? A feeling? This tells your brain what to listen for." theme={theme}>reading ahead</Highlight>. During the reading time, look at the questions and figure out what kind of answer you need (a number? a place? a feeling?). This primes your brain to pick out the right information.</p>
              <p>To get better at understanding spoken language, you need to <Highlight description="Listen to real content in your target language to get used to the speed and rhythm. Free resources like 'News in Slow French' on YouTube are perfect for this." theme={theme}>listen to real content regularly</Highlight>. Free resources like "News in Slow French/German/Spanish" on YouTube are brilliant for this. Another great technique is <Highlight description="Listen to someone speaking in your target language and try to repeat what they say at the same time, almost like an echo. It trains your ear and your pronunciation together." theme={theme}>shadowing</Highlight> -- you listen to a native speaker and repeat what they say almost at the same time, like an echo. It's one of the best ways to improve both your listening and your pronunciation for the Oral.</p>
              </>)}
            </ReadingSection>
          )}
          {activeSection === 5 && (
            <ReadingSection title="Reading Comprehension." eyebrow="Step 6" icon={BookOpen} theme={theme}>
              {essentials ? (<>
              <p>Do not translate every word. Use <Highlight description="Underline the key words in the question, then scan the text looking for those words or their synonyms. The answers nearly always appear in the same order as the questions." theme={theme}>search and extract</Highlight>: underline key words in the question, then scan the text for them. Answers appear in question order. For French, watch the <Highlight description="In French exams, 'Trouvez' means copy the answer exactly from the text. But 'Indiquez' or 'Dites' means you need to change the grammar -- like swapping 'je' for 'il'. Missing this costs a lot of students marks." theme={theme}>quote vs. rephrase trap</Highlight>: "Trouvez" means copy exactly. "Indiquez" means change the grammar.</p>
              </>) : (<>
              <p>For Ordinary Level students, the reading comprehension is the single biggest section -- worth 40% of your marks. The biggest trap? Trying to translate every single word. You don't need to. The smart approach is <Highlight description="Underline the key words in the question, then scan the text looking for those words or their synonyms. The answers nearly always appear in the same order as the questions." theme={theme}>search and extract</Highlight> -- underline the key words in the question, then scan the text for those words. The answers almost always appear in the same order as the questions.</p>
              <p>If you're doing French, watch out for the <Highlight description="In French exams, 'Trouvez' means copy the answer exactly from the text. But 'Indiquez' or 'Dites' means you need to change the grammar -- like swapping 'je' for 'il'. Missing this costs a lot of students marks." theme={theme}>quote vs. rephrase trap</Highlight>. If the question says "Trouvez," you copy the answer word-for-word from the text. But if it says "Indiquez" or "Dites," you have to change the grammar (e.g., swap "je" for "il"). This catches out loads of students and it's often the difference between a H1 and a H2.</p>
              </>)}
            </ReadingSection>
          )}
           {activeSection === 6 && (
            <ReadingSection title="Writing Strong Essays." eyebrow="Step 7" icon={PenSquare} theme={theme}>
              {essentials ? (<>
              <p>Every paragraph follows a <Highlight description="A 4-part recipe: 1. Start with your main point, 2. Explain or give a reason, 3. Give an example, 4. Link to the next point." theme={theme}>paragraph formula</Highlight>: main point, explanation, example, link to next point. For a H1, use advanced linking words instead of basic ones. Try the drag-and-drop exercise below to practise.</p>
              </>) : (<>
              <p>Here's a secret: top-scoring essays aren't written by geniuses. They're built from a set of reliable building blocks. Every paragraph should follow a simple <Highlight description="A 4-part recipe: 1. Start with your main point, 2. Explain or give a reason, 3. Give an example, 4. Link to the next point." theme={theme}>paragraph formula</Highlight>.</p>
              <p>If you're going for a H1, use linking words that go beyond the basics. Instead of "Et" or "Mais," try things like *N\u00e9anmoins* (however) or *De surcro\u00eet* (furthermore). These small upgrades show the examiner you're comfortable with the language at a high level.</p>
              </>)}
              <ParagraphSorter />
            </ReadingSection>
          )}
          {activeSection === 7 && (
            <ReadingSection title="Your Action Plan." eyebrow="Step 8" icon={Languages} theme={theme}>
                {essentials ? (<>
                <p>You now know the system. Pick one technique from this module to try this week. The exam is not a mystery. It rewards specific skills you can practise.</p>
                </>) : (<>
                <p>You've now got a clear picture of how the Leaving Cert language exams actually work. You know which sections are worth the most marks, what examiners are looking for, and the specific techniques that separate top students from the rest. The exam isn't a mystery -- it's a system, and now you know how it works.</p>
                </>)}
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
