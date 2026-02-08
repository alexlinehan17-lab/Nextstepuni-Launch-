/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
*/

import React, { useState } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { Cpu, ClipboardList, ListFilter, PlayCircle, BarChart2, HeartPulse, HardHat } from 'lucide-react';
import { ModuleProgress } from '../types';
import { amberTheme } from '../moduleThemes';
import { Highlight, ReadingSection, MicroCommitment } from './ModuleShared';
import { ModuleLayout } from './ModuleLayout';

const theme = amberTheme;

// --- INTERACTIVE COMPONENTS ---
const TriageSimulator = () => {
    const questions = [
        { id: 1, text: "A 'Describe' question on a topic you know well.", difficulty: 'green' },
        { id: 2, text: "An 'Evaluate' question that requires a long essay plan.", difficulty: 'amber' },
        { id: 3, text: "A multi-step maths problem on a topic you're weak on.", difficulty: 'red' },
    ];
    const [qIndex, setQIndex] = useState(0);
    const [choices, setChoices] = useState<(string|null)[]>(Array(questions.length).fill(null));

    const handleChoice = (choice: string) => {
        const newChoices = [...choices];
        newChoices[qIndex] = choice;
        setChoices(newChoices);
        setTimeout(() => setQIndex(q => Math.min(q + 1, questions.length)), 1000);
    };

    if (qIndex >= questions.length) {
        return (
            <div className="my-10 p-8 md:p-12 bg-white rounded-[3rem] border border-stone-200 shadow-xl text-center">
                <h4 className="font-serif text-2xl font-semibold text-stone-800 text-center italic">Triage Complete</h4>
                <button onClick={() => {setQIndex(0); setChoices(Array(questions.length).fill(null));}} className="mt-4 px-4 py-2 bg-amber-500 text-white font-bold text-sm rounded-lg">Run Drill Again</button>
            </div>
        );
    }

    return(
        <div className="my-10 p-8 md:p-12 bg-white rounded-[3rem] border border-stone-200 shadow-xl">
            <h4 className="font-serif text-2xl font-semibold text-stone-800 text-center italic">Triage Drill</h4>
            <p className="text-center text-sm text-stone-500 mb-8">Reading time has started. Quickly categorize this question.</p>
            <AnimatePresence mode="wait">
            <motion.div key={qIndex} initial={{opacity:0, x:20}} animate={{opacity:1, x:0}} exit={{opacity:0, x:-20}} className="p-6 bg-stone-100 border border-stone-200 rounded-2xl text-center font-bold text-stone-700 min-h-[100px] flex items-center justify-center">
                {questions[qIndex].text}
            </motion.div>
            </AnimatePresence>
            <div className="grid grid-cols-3 gap-3 mt-6">
                <button onClick={() => handleChoice('green')} className="p-4 bg-emerald-100 text-emerald-800 font-bold rounded-xl border-2 border-emerald-200 hover:border-emerald-400">Green</button>
                <button onClick={() => handleChoice('amber')} className="p-4 bg-amber-100 text-amber-800 font-bold rounded-xl border-2 border-amber-200 hover:border-amber-400">Amber</button>
                <button onClick={() => handleChoice('red')} className="p-4 bg-rose-100 text-rose-800 font-bold rounded-xl border-2 border-rose-200 hover:border-rose-400">Red</button>
            </div>
        </div>
    )
}

const MPMCalculator = () => {
    const [time, setTime] = useState(180);
    const [marks, setMarks] = useState(100);
    const [buffer, setBuffer] = useState(15);
    const mpm = (time - buffer) / marks;

    return (
        <div className="my-10 p-8 md:p-12 bg-white rounded-[3rem] border border-stone-200 shadow-xl">
             <h4 className="font-serif text-2xl font-semibold text-stone-800 text-center italic">Minutes-Per-Mark (MPM) Calculator</h4>
             <div className="grid grid-cols-3 gap-4 mt-6">
                <div><label className="text-xs font-bold">Total Time (mins)</label><input type="number" value={time} onChange={e=>setTime(parseInt(e.target.value))} className="w-full p-2 bg-stone-100 rounded-md" /></div>
                <div><label className="text-xs font-bold">Total Marks</label><input type="number" value={marks} onChange={e=>setMarks(parseInt(e.target.value))} className="w-full p-2 bg-stone-100 rounded-md" /></div>
                <div><label className="text-xs font-bold">Buffer (mins)</label><input type="number" value={buffer} onChange={e=>setBuffer(parseInt(e.target.value))} className="w-full p-2 bg-stone-100 rounded-md" /></div>
             </div>
             <div className="mt-6 p-4 bg-stone-900 rounded-xl text-center text-white">
                Your MPM is <span className="font-bold text-2xl text-amber-400">{mpm.toFixed(2)}</span>. A 20-mark question gets <span className="font-bold text-amber-400">{(mpm*20).toFixed(1)}</span> minutes.
             </div>
        </div>
    )
}

const BoxBreathingVisualizer = () => {
    const steps = ["Inhale...", "Hold...", "Exhale...", "Hold..."];
    return (
        <div className="my-10 p-8 md:p-12 bg-white rounded-[3rem] border border-stone-200 shadow-xl flex flex-col items-center">
             <h4 className="font-serif text-2xl font-semibold text-stone-800 text-center italic">4-4-4-4 Box Breathing</h4>
             <p className="text-center text-sm text-stone-500 mb-8">Feeling panicked? Run this protocol.</p>
             <div className="w-32 h-32 relative flex items-center justify-center">
                <motion.div
                    className="w-full h-full border-4 border-stone-200 rounded-lg"
                    animate={{ rotate: [0, 90, 180, 270, 360] }}
                    transition={{ duration: 16, repeat: Infinity, ease: 'linear' }}
                />
                 <motion.div
                    className="absolute w-4 h-4 bg-amber-500 rounded-full"
                    style={{ top: '-8px', left: '50%', x: '-50%'}}
                    animate={{
                        x: ['-50%', '-50%', 'calc(-50% + 64px)', 'calc(-50% + 64px)', 'calc(-50% - 64px)', 'calc(-50% - 64px)', '-50%', '-50%'],
                        y: [0, '128px', '128px', 0, 0, '128px', '128px', 0],
                    }}
                    transition={{ duration: 16, repeat: Infinity, ease: 'linear', times: [0, 0.25, 0.25, 0.5, 0.5, 0.75, 0.75, 1]}}
                />
                 <AnimatePresence mode="wait">
                    <motion.p
                        key={Math.floor(Date.now() / 4000) % 4}
                        className="absolute font-bold"
                        initial={{ opacity: 0 }}
                        animate={{ opacity: 1 }}
                        exit={{ opacity: 0 }}
                        transition={{ duration: 0.5 }}
                    >
                        {steps[Math.floor(Date.now() / 4000) % 4]}
                    </motion.p>
                 </AnimatePresence>
             </div>
        </div>
    );
}

// --- MODULE COMPONENT ---
const ExamHallStrategiesModule: React.FC<{ onBack: () => void; progress: ModuleProgress; onProgressUpdate: (progress: ModuleProgress) => void }> = ({ onBack, progress, onProgressUpdate }) => {
  const sections = [
    { id: 'execution-gap', title: 'The Execution Gap', eyebrow: '01 // The Problem', icon: Cpu },
    { id: 'cognitive-offloading', title: 'Cognitive Offloading', eyebrow: '02 // The Dump Sheet', icon: ClipboardList },
    { id: 'tactical-triage', title: 'Tactical Triage', eyebrow: '03 // Reading Time Strategy', icon: ListFilter },
    { id: 'order-of-attack', title: 'Order of Attack', eyebrow: '04 // The Momentum Principle', icon: PlayCircle },
    { id: 'exam-economics', title: 'Exam Economics', eyebrow: '05 // Strict Time Budgeting', icon: BarChart2 },
    { id: 'anxiety-regulation', title: 'Anxiety Regulation', eyebrow: '06 // Physiological Management', icon: HeartPulse },
    { id: 'post-exam-training', title: 'Post-Exam Training', eyebrow: '07 // The Drills', icon: HardHat },
  ];

  return (
    <ModuleLayout
      moduleNumber="03"
      moduleTitle="Exam Hall Strategies"
      theme={theme}
      sections={sections}
      onBack={onBack}
      progress={progress}
      onProgressUpdate={onProgressUpdate}
    >
      {(activeSection) => (
        <>
          {activeSection === 0 && (
            <ReadingSection title="The Execution Gap." eyebrow="Step 1" icon={Cpu} theme={theme}>
              <p>You can be the smartest person in the room, have every definition memorized, and still get a bad result. The gap between what you know (<Highlight description="What you have learned and stored in your long-term memory over months of study." theme={theme}>Competence</Highlight>) and what you can actually do on the day (<Highlight description="What you can retrieve and apply from your memory under the intense pressure of a timed exam." theme={theme}>Performance</Highlight>) is called the **Execution Gap**. This module is about closing that gap.</p>
              <p>The exam hall is not a library for quiet recall; it's a high-pressure, resource-management game. The pressure adds <Highlight description="The 'bad' mental workload that comes from things other than the question itself, like managing your panic, checking the clock, or trying to remember a formula." theme={theme}>Extraneous Cognitive Load</Highlight> to your brain, stealing the limited mental bandwidth you need for the actual questions. The strategies in this module are about minimizing that load so you can show what you really know.</p>
            </ReadingSection>
          )}
           {activeSection === 1 && (
            <ReadingSection title="Cognitive Offloading." eyebrow="Step 2" icon={ClipboardList} theme={theme}>
              <p>In the first few minutes of an exam, your stress hormones spike, which can block access to your memory. The <Highlight description="A pre-memorized sheet of high-yield, high-volatility information that you write down from memory at the very start of the exam before you even look at the questions." theme={theme}>"Dump Sheet"</Highlight> is a proactive strategy to combat this. It's about getting the most fragile, important information out of your head and onto paper before stress can erase it.</p>
              <p>This isn't cheating; it's <Highlight description="The act of moving information from your limited biological working memory to a physical resource (like paper), freeing up mental capacity to focus on problem-solving." theme={theme}>Cognitive Offloading</Highlight>. The sheet should contain "High-Yield, High-Volatility" information: things that are easy to forget under pressure but are likely to be useful (e.g., key quotes, formulas, dates, acronyms). You must rehearse writing it until it's a 3-minute automatic motor skill.</p>
            </ReadingSection>
          )}
           {activeSection === 2 && (
            <ReadingSection title="Tactical Triage." eyebrow="Step 3" icon={ListFilter} theme={theme}>
              <p>Reading time is not for passively reading. It's for <Highlight description="An active process during reading time where you scan the entire paper and sort questions into categories of difficulty, like a medic at a disaster scene." theme={theme}>Tactical Triage</Highlight>. Just like in an emergency room, your goal isn't to save every "patient" (question) perfectly; it's to get the most marks possible with your limited time.</p>
              <p>Use a **Traffic Light System**: **Green** questions are "low-hanging fruit" you're 100% confident you can answer quickly. **Amber** questions are ones you know how to do but will take time or complex calculation. **Red** questions are "time sinks"--topics you're weak on or don't immediately understand. Your first job is to find 2-3 "Green" questions to serve as your <Highlight description="The first easy questions you attempt, regardless of their position on the paper. They build confidence, calm your nerves, and create psychological momentum." theme={theme}>Anchor Questions</Highlight>.</p>
              <TriageSimulator />
            </ReadingSection>
          )}
          {activeSection === 3 && (
            <ReadingSection title="Order of Attack." eyebrow="Step 4" icon={PlayCircle} theme={theme}>
              <p>Starting at Question 1 is a rookie mistake. It gives control to the examiner, who may have put a difficult question first. You need to become a <Highlight description="A concept from cybersecurity where an attacker seeks the easiest path to breach a system. In an exam, you should act like one, seeking the easiest path to accumulate marks." theme={theme}>"Work-Averse Attacker"</Highlight>, extracting the maximum marks for the minimum effort. This means attacking the "Green" questions first, no matter where they are.</p>
              <p>This builds <Highlight description="The psychological phenomenon where early success creates a virtuous cycle of confidence and dopamine release, improving focus and making subsequent harder tasks feel more manageable." theme={theme}>Psychological Momentum</Highlight>. If you can't figure out a question in 30 seconds (the "30-Second Rule"), skip it immediately. The <Highlight description="The subconscious mind continues to work on a problem even after you've moved on. When you return to the question later, the solution often appears 'obvious.'" theme={theme}>Incubation Effect</Highlight> means your brain will keep working on it in the background.</p>
            </ReadingSection>
          )}
          {activeSection === 4 && (
            <ReadingSection title="Exam Economics." eyebrow="Step 5" icon={BarChart2} theme={theme}>
              <p>Time is the currency of the exam hall. Every minute is an investment that must provide a return (marks). The core metric is <Highlight description="Your fundamental time budget, calculated by dividing the total time (minus a buffer) by the total marks. E.g., (180-15 mins) / 100 marks = 1.65 minutes per mark." theme={theme}>Minutes Per Mark (MPM)</Highlight>. This tells you exactly how long you can spend on any given question.</p>
              <p>When your timer for a question goes off, you must execute a <Highlight description="The discipline of stopping work on a question immediately when its time budget expires, even if you are mid-sentence, to avoid the Sunk Cost Fallacy." theme={theme}>"Hard Stop."</Highlight> This is the hardest discipline to learn because of the <Highlight description="The cognitive bias to continue investing in a losing proposition (like a hard question) because of the resources (time) you have already spent. It's the number one cause of time mismanagement in exams." theme={theme}>Sunk Cost Fallacy</Highlight>. The first 5 minutes on a new question will always be more valuable than the last 5 minutes polishing an old one.</p>
              <MPMCalculator/>
            </ReadingSection>
          )}
          {activeSection === 5 && (
            <ReadingSection title="Anxiety Regulation." eyebrow="Step 6" icon={HeartPulse} theme={theme}>
              <p>When you hit a difficult question, your sympathetic nervous system can trigger a "Panic Spike," narrowing your focus and blocking access to your memory. You need a protocol to fight back. The fastest is <Highlight description="A breathing technique (4s inhale, 4s hold, 4s exhale, 4s hold) that forces your nervous system back into a calm 'rest and digest' state." theme={theme}>Box Breathing</Highlight>.</p>
              <p>Another tool is the <Highlight description="A grounding technique where you name 3 things you see, 3 sounds you hear, and 3 body parts you can feel. It forces your brain to process sensory data, disengaging the emotional amygdala hijack." theme={theme}>3-3-3 Rule</Highlight> for grounding. Finally, use <Highlight description="Changing your internal story from catastrophic ('I'm failing') to procedural ('This is a Red question. This is part of the plan. I will flag it and move on.')." theme={theme}>Cognitive Reframing</Highlight> to turn panic into a planned response.</p>
              <BoxBreathingVisualizer />
            </ReadingSection>
          )}
          {activeSection === 6 && (
            <ReadingSection title="The Training Protocol." eyebrow="Step 7" icon={HardHat} theme={theme}>
              <p>These strategies are skills. They must be trained. After every practice test, you must use an <Highlight description="A post-exam reflection tool that forces you to analyze your errors by process ('I misread the question,' 'I ran out of time') not just by content ('I didn't know the date')." theme={theme}>Exam Wrapper</Highlight> to analyze your performance. Did your triage work? Did you stick to your time budget?</p>
              <p>You must also run specific drills. **Triage Drills**: Give yourself 5 minutes with a past paper to *only* categorize questions as Green, Amber, or Red. **Dump Sprints**: Practice writing your dump sheet until it takes less than 3 minutes. **Hard Stop Drills**: Do questions with a strict timer and force yourself to stop when it rings. This builds the discipline you need to execute under pressure.</p>
              <MicroCommitment theme={theme}><p>For your next practice test, do a full "Exam Wrapper" analysis afterwards. Don't just check the answers; analyze *how* you took the test.</p></MicroCommitment>
            </ReadingSection>
          )}
        </>
      )}
    </ModuleLayout>
  );
};
export default ExamHallStrategiesModule;
