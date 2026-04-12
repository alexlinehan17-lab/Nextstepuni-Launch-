
/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
*/

import React, { useState } from 'react';
import { motion } from 'framer-motion';
import {
  Layers, Shuffle, Brain, ListChecks, Wrench
} from 'lucide-react';
import { type ModuleProgress } from '../types';
import { purpleTheme } from '../moduleThemes';
import { Highlight, ReadingSection, MicroCommitment } from './ModuleShared';
import { ModuleLayout } from './ModuleLayout';
import { useEssentialsMode } from '../hooks/useEssentialsMode';

const theme = purpleTheme;

// --- INTERACTIVE COMPONENTS ---

const StudyPlannerInteractive = () => {
    const [planType, setPlanType] = useState<'blocked' | 'interleaved'>('blocked');
    const blockedSchedule = { Mon: ['Maths', 'Maths', 'Maths'], Tue: ['English', 'English', 'English'], Wed: ['Biology', 'Biology', 'Biology'] };
    const interleavedSchedule = { Mon: ['Maths', 'English', 'French'], Tue: ['English', 'Biology', 'History'], Wed: ['Biology', 'Maths', 'English'] };
    const schedule = planType === 'blocked' ? blockedSchedule : interleavedSchedule;

    return (
        <div className="my-10 rounded-2xl p-6 md:p-8" style={{ backgroundColor: '#F8F8F8', borderRadius: 18 }}>
            <h4 className="font-serif text-2xl font-semibold text-zinc-800 dark:text-white text-center">Weekly Schedule Architect</h4>
            <div className="flex justify-center gap-2 p-1 bg-zinc-100 dark:bg-zinc-800 rounded-full my-6 max-w-sm mx-auto">
                <button onClick={() => setPlanType('blocked')} className={`w-full px-4 py-2 text-xs font-bold rounded-full ${planType === 'blocked' ? 'bg-white dark:bg-zinc-700 shadow' : ''}`}>Blocked Schedule</button>
                <button onClick={() => setPlanType('interleaved')} className={`w-full px-4 py-2 text-xs font-bold rounded-full ${planType === 'interleaved' ? 'bg-white dark:bg-zinc-700 shadow' : ''}`}>Interleaved Schedule</button>
            </div>
            <div className="grid grid-cols-3 gap-2 text-center text-xs">
                {Object.entries(schedule).map(([day, subjects]) => (
                    <div key={day}>
                        <p className="font-bold mb-2">{day}</p>
                        <div className="space-y-1">
                            {subjects.map((sub, i) => (
                                <motion.div key={`${day}-${i}`} layoutId={`${day}-${i}-${sub}`} className="p-2 bg-zinc-50 dark:bg-zinc-700/50 border border-zinc-200 dark:border-zinc-700 rounded-md">{sub}</motion.div>
                            ))}
                        </div>
                    </div>
                ))}
            </div>
        </div>
    );
};

const ProblemTypeSpotter = () => {
    const [choice, setChoice] = useState<{[key:string]: 'chain'|'product'|null}>({});
    const [score, setScore] = useState(0);
    const problems = [
        { id: 1, text: "Differentiate: y = sin(x\u00B2)", correct: "chain", hint: "It's a function inside a function" },
        { id: 2, text: "Differentiate: y = x\u00B2sin(x)", correct: "product", hint: "Two separate functions multiplied together" },
        { id: 3, text: "Differentiate: y = sin(x\u00B2)", correct: "chain", hint: "It's a function inside a function" },
        { id: 4, text: "Differentiate: y = e\u02E3 \u00B7 ln(x)", correct: "product", hint: "Two separate functions multiplied together" },
        { id: 5, text: "Differentiate: y = (3x + 1)\u2075", correct: "chain", hint: "A function raised to a power" },
        { id: 6, text: "Differentiate: y = x\u00B2 \u00B7 cos(x)", correct: "product", hint: "Two functions multiplied together" },
    ];

    const handleChoice = (id: number, rule: 'chain' | 'product') => {
        if (choice[id]) return;
        const problem = problems.find(p => p.id === id);
        if (problem && rule === problem.correct) {
            setScore(s => s + 1);
        }
        setChoice({...choice, [id]: rule});
    };

    const allAnswered = problems.every(p => choice[p.id] !== undefined);

    const handleReset = () => {
        setChoice({});
        setScore(0);
    };

    return (
        <div className="my-10 rounded-2xl p-6 md:p-8" style={{ backgroundColor: '#F8F8F8', borderRadius: 18 }}>
             <h4 className="font-serif text-2xl font-semibold text-zinc-800 dark:text-white text-center">Problem Spotter</h4>
             <p className="text-center text-sm text-zinc-500 dark:text-zinc-400 mb-2">Calculus: Don't solve. Just identify the correct rule.</p>
             <p className="text-center text-xs font-semibold text-purple-600 dark:text-purple-400 mb-8">Score: {score}/{problems.length}</p>
             {problems.map(p => (
                <div key={p.id} className="mb-4">
                    <p className="text-center font-mono bg-zinc-100 dark:bg-zinc-800 p-4 rounded-xl mb-1">{p.text}</p>
                    <p className="text-center text-[10px] text-zinc-400 dark:text-zinc-500 mb-2 italic">Hint: {p.hint}</p>
                    <div className="grid grid-cols-2 gap-2">
                        <button onClick={() => handleChoice(p.id, 'chain')} className={`p-2 text-xs rounded-lg border ${choice[p.id] && (choice[p.id] === 'chain' && p.correct === 'chain' ? 'bg-emerald-100 border-emerald-300' : choice[p.id] === 'chain' ? 'bg-rose-100 border-rose-300' : 'bg-zinc-100 border-zinc-200 dark:border-zinc-700')}`}>Chain Rule</button>
                        <button onClick={() => handleChoice(p.id, 'product')} className={`p-2 text-xs rounded-lg border ${choice[p.id] && (choice[p.id] === 'product' && p.correct === 'product' ? 'bg-emerald-100 border-emerald-300' : choice[p.id] === 'product' ? 'bg-rose-100 border-rose-300' : 'bg-zinc-100 border-zinc-200 dark:border-zinc-700')}`}>Product Rule</button>
                    </div>
                </div>
             ))}
             {allAnswered && (
                <div className="text-center mt-6">
                    <p className="text-sm font-semibold text-zinc-700 dark:text-zinc-300 mb-3">You got {score} out of {problems.length} correct!</p>
                    <button onClick={handleReset} className="px-5 py-2 bg-purple-500 hover:bg-purple-600 text-white text-sm font-bold rounded-lg transition-colors">Try Again</button>
                </div>
             )}
        </div>
    );
};

const RetrospectiveRevisionLog = () => {
    const [topics, setTopics] = useState([
        { name: "Algebra", status: 'red' },
        { name: "Statistics", status: 'amber' },
        { name: "Geometry", status: 'green' },
        { name: "Functions", status: 'red' },
        { name: "Number", status: 'amber' },
    ]);
    const [nextTopic, setNextTopic] = useState("Algebra");

    const updateStatus = (name: string, newStatus: 'red' | 'amber' | 'green') => {
        setTopics(topics.map(t => t.name === name ? {...t, status: newStatus} : t));
    };

    const findNextTopic = () => {
        const redTopics = topics.filter(t => t.status === 'red');
        if (redTopics.length > 0) {
            setNextTopic(redTopics[0].name);
            return;
        }
        const amberTopics = topics.filter(t => t.status === 'amber');
        if (amberTopics.length > 0) {
            setNextTopic(amberTopics[0].name);
            return;
        }
        setNextTopic(topics[0].name);
    }

    return (
         <div className="my-10 rounded-2xl p-6 md:p-8" style={{ backgroundColor: '#F8F8F8', borderRadius: 18 }}>
             <h4 className="font-serif text-2xl font-semibold text-zinc-800 dark:text-white text-center">Retrospective Revision Log</h4>
             <p className="text-center text-sm text-zinc-500 dark:text-zinc-400 mb-8">Update your confidence after studying. The "Worst First" rule will guide you.</p>
             <div className="space-y-3">
                {topics.map(topic => (
                    <div key={topic.name} className="p-3 rounded-lg flex justify-between items-center" style={{ backgroundColor: '#FFFFFF', border: '2.5px solid #1C1917', borderRadius: 10, boxShadow: '3px 3px 0px 0px #1C1917' }}>
                        <span className="font-bold text-sm">{topic.name}</span>
                        <div className="flex gap-1">
                            <button aria-label="Mark as struggling (red)" onClick={() => updateStatus(topic.name, 'red')} className={`w-6 h-6 rounded-full border ${topic.status === 'red' ? 'bg-rose-500 border-rose-600' : 'bg-rose-200 border-rose-300'}`}></button>
                            <button aria-label="Mark as okay (amber)" onClick={() => updateStatus(topic.name, 'amber')} className={`w-6 h-6 rounded-full border ${topic.status === 'amber' ? 'bg-amber-500 border-amber-600' : 'bg-amber-200 border-amber-300'}`}></button>
                            <button aria-label="Mark as confident (green)" onClick={() => updateStatus(topic.name, 'green')} className={`w-6 h-6 rounded-full border ${topic.status === 'green' ? 'bg-emerald-500 border-emerald-600' : 'bg-emerald-200 border-emerald-300'}`}></button>
                        </div>
                    </div>
                ))}
             </div>
             <div className="mt-6 text-center">
                 <button onClick={findNextTopic} className="px-4 py-2 bg-zinc-800 dark:bg-zinc-200 text-white dark:text-zinc-900 text-xs font-bold rounded-lg">Find Next Topic</button>
                 <p className="mt-4 text-sm">Next up: <span className="font-bold text-purple-600">{nextTopic}</span></p>
             </div>
        </div>
    );
}

// --- MODULE COMPONENT ---
const MasteringInterleavingModule: React.FC<{ onBack: () => void; progress: ModuleProgress; onProgressUpdate: (progress: ModuleProgress) => void }> = ({ onBack, progress, onProgressUpdate }) => {
  const essentials = useEssentialsMode();
  const sections = [
    { id: 'illusion-of-mastery', title: 'Why "Finishing a Topic" Fools You', eyebrow: '01 // The Trap', icon: Layers },
    { id: 'topic-salad', title: 'The "Topic Salad" Method', eyebrow: '02 // The Fix', icon: Shuffle },
    { id: 'desirable-difficulty', title: 'Why Harder Feels Better (For Your Brain)', eyebrow: '03 // Why It Works', icon: Brain },
    { id: 'retrospective-timetable', title: 'The "Worst First" Timetable', eyebrow: '04 // The System', icon: ListChecks },
    { id: 'subject-hacker', title: 'Your Mix-It-Up Game Plan', eyebrow: '05 // Your Action Plan', icon: Wrench },
  ];

  return (
    <ModuleLayout moduleNumber="03" moduleTitle="Mix It Up" moduleSubtitle="The Topic Salad Method" moduleDescription={`Stop studying one subject for hours on end. Mixing your topics feels harder, but it's the fastest way to build the kind of knowledge that actually holds up in the Leaving Cert.`} theme={theme} sections={sections} onBack={onBack} progress={progress} onProgressUpdate={onProgressUpdate} finishButtonText="Shake Up Your Study">
      {(activeSection) => (
        <>
          {activeSection === 0 && (
            <ReadingSection title="Why 'Finishing a Topic' Fools You." eyebrow="Step 1" icon={Layers} theme={theme}>
              {essentials ? (
                <>
                  <p>Most students use <Highlight description="When you study one topic for ages before moving on, like doing Maths all Monday, English all Tuesday, Biology all Wednesday." theme={theme}>Blocked Practice</Highlight> -- one subject per night. It feels productive, but it creates a <Highlight description="That fake 'I totally know this' feeling you get right after studying something, just because it's still fresh in your head." theme={theme}>false sense of confidence</Highlight>.</p>
                  <p>The exam mixes topics together. If you only practise one type at a time, you never learn to <Highlight description="Being able to look at a question and figure out which approach to use -- like knowing whether you need the chain rule or the product rule." theme={theme}>tell similar problems apart</Highlight>. That's exactly what costs you marks.</p>
                </>
              ) : (
                <>
                  <p>Most students study using <Highlight description="When you study one topic for ages before moving on, like doing Maths all Monday, English all Tuesday, Biology all Wednesday." theme={theme}>Blocked Practice</Highlight>. You spend Monday night on Maths, Tuesday on English, Wednesday on Biology. It feels productive. After three hours of Algebra, you feel like you've nailed it. But that feeling is actually a <Highlight description="That fake 'I totally know this' feeling you get right after studying something, just because it's still fresh in your head." theme={theme}>false sense of confidence</Highlight>.</p>
                  <p>Here's the problem: your brain isn't being trained for the real Leaving Cert. The exam doesn't hand you 20 algebra questions in a row. It throws a mix at you. When you practise the same type of question over and over, you never have to figure out <em>what</em> to do, only <em>how</em> to do it. You never build the skill of <Highlight description="Being able to look at a question and figure out which approach to use -- like knowing whether you need the chain rule or the product rule." theme={theme}>telling similar problems apart</Highlight>, and that's exactly what the exam tests.</p>
                </>
              )}
            </ReadingSection>
          )}
           {activeSection === 1 && (
            <ReadingSection title="The 'Topic Salad' Method." eyebrow="Step 2" icon={Shuffle} theme={theme}>
              {essentials ? (
                <>
                  <p>The fix: <Highlight description="Instead of studying one topic for ages, you mix different topics or question types together in the same session." theme={theme}>mix your topics</Highlight>. Think "topic salad" instead of "topic block." Mix everything together.</p>
                  <p>Two levels: <Highlight description="Mixing different subjects across your week -- like doing Maths, English, and Biology all on Monday evening instead of just one." theme={theme}>mix across subjects</Highlight> in your weekly schedule. <Highlight description="Mixing different topics within one subject session -- like doing a bit of Algebra, then Stats, then Geometry, instead of just Algebra." theme={theme}>Mix within a subject</Highlight> during a single session. The harder it feels, the better it works.</p>
                </>
              ) : (
                <>
                  <p>The fix is simple but powerful: <Highlight description="Instead of studying one topic for ages, you mix different topics or question types together in the same session." theme={theme}>mixing your topics</Highlight>. Instead of a "topic block," think of your study session as a "topic salad." A fruit salad isn't a pile of apples next to a pile of bananas -- it's all mixed together. Your study should be the same.</p>
                  <p>This works at two levels. <Highlight description="Mixing different subjects across your week -- like doing Maths, English, and Biology all on Monday evening instead of just one." theme={theme}>Mixing across subjects</Highlight> is about your weekly schedule: instead of one subject for 3 hours, study three subjects for 1 hour each. <Highlight description="Mixing different topics within one subject session -- like doing a bit of Algebra, then Stats, then Geometry, instead of just Algebra." theme={theme}>Mixing within a subject</Highlight> is about shuffling topics <em>within</em> a single study session. This one is harder, but that extra effort is exactly where the real learning happens.</p>
                </>
              )}
              <StudyPlannerInteractive />
            </ReadingSection>
          )}
           {activeSection === 2 && (
            <ReadingSection title="Why Harder Feels Better (For Your Brain)." eyebrow="Step 3" icon={Brain} theme={theme}>
              {essentials ? (
                <>
                  <p>Switching topics feels harder. That's good. The extra effort is a <Highlight description="When studying feels tougher but that struggle is actually making your memory way stronger in the long run." theme={theme}>good kind of difficulty</Highlight> that builds stronger memory.</p>
                  <p>When you study similar concepts together, your brain must <Highlight description="When you study similar topics back-to-back, your brain has to figure out what makes each one different -- and that's what helps you pick the right approach in the exam." theme={theme}>spot the differences</Highlight>. You learn when to use each rule. That's exactly what the exam tests.</p>
                </>
              ) : (
                <>
                  <p>Mixing topics feels harder -- and that's the whole point. When you switch from Maths to English, your brain has to work to "reload" a completely different way of thinking. That extra effort is actually a <Highlight description="When studying feels tougher but that struggle is actually making your memory way stronger in the long run." theme={theme}>good kind of difficulty</Highlight>. Studying one thing on repeat feels smooth because it's like re-watching the same scene of a film over and over. Mixing it up forces your brain to keep switching gears, and that builds the mental muscle you need for the exam.</p>
                  <p>Here's the key idea: when you put similar but different concepts next to each other (like differentiation and integration), your brain is forced to <Highlight description="When you study similar topics back-to-back, your brain has to figure out what makes each one different -- and that's what helps you pick the right approach in the exam." theme={theme}>spot the differences between them</Highlight>. You're not just learning a rule -- you're learning <em>when</em> to use that rule. And that's exactly what the Leaving Cert asks you to do.</p>
                </>
              )}
              <ProblemTypeSpotter/>
            </ReadingSection>
          )}
          {activeSection === 3 && (
            <ReadingSection title="The 'Worst First' Timetable." eyebrow="Step 4" icon={ListChecks} theme={theme}>
              {essentials ? (
                <>
                  <p>Use a <Highlight description="Instead of planning your week ahead of time, you look back at what you've already studied and pick the topics you're weakest at next." theme={theme}>backwards-looking timetable</Highlight>. Decide what to study based on what you're weakest at right now.</p>
                  <p>List your topics. Colour-code them: Red, Amber, or Green. Follow the <Highlight description="A simple rule: always start with the topic you feel least confident about. If something's red, that's what you study next." theme={theme}>"Worst First" rule</Highlight> -- always start with a Red topic. This keeps you mixing naturally.</p>
                </>
              ) : (
                <>
                  <p>Mixing topics can feel a bit chaotic at first. The best way to stay on track is to ditch the rigid, plan-everything-in-advance timetable and use a <Highlight description="Instead of planning your week ahead of time, you look back at what you've already studied and pick the topics you're weakest at next." theme={theme}>backwards-looking revision timetable</Highlight>. Instead of deciding what to study next week, you decide what to study *right now* based on what you're struggling with most.</p>
                  <p>Here's how it works: 1. List every topic in a subject. 2. After you study a topic, colour-code it: Green (I know this), Amber (It's okay), or Red (I'm lost). 3. Next time you sit down to study that subject, follow the <Highlight description="A simple rule: always start with the topic you feel least confident about. If something's red, that's what you study next." theme={theme}>"Worst First" rule</Highlight> -- always start with a Red topic. This naturally keeps you mixing things up, because you're constantly jumping between your weakest areas across the whole course.</p>
                </>
              )}
              <RetrospectiveRevisionLog />
            </ReadingSection>
          )}
           {activeSection === 4 && (
            <ReadingSection title="Your Mix-It-Up Game Plan." eyebrow="Step 5" icon={Wrench} theme={theme}>
              {essentials ? (
                <p>Break up the blocks. Shuffle question types. Jump between topics. Train your brain for the mixed reality of the exam. Study smarter, not more.</p>
              ) : (
                <>
                  <p>You've got the idea. Now you need the action plan. Mixing your topics isn't some vague notion -- it's a set of real, practical strategies you can use for every single subject you study for the Leaving Cert.</p>
                  <p>Whether it's shuffling question types in Maths or jumping between poets in English, the goal is always the same: break up the blocks, lean into the struggle of switching, and train your brain for the reality of the exam. This is not about studying more -- it's about studying smarter.</p>
                </>
              )}
              <MicroCommitment theme={theme}>
                <p>Tonight, take your hardest subject. Instead of studying one chapter for an hour, pick three different chapters and spend just 20 minutes on each. Notice how the switching feels harder -- that's your brain building real, lasting connections.</p>
              </MicroCommitment>
            </ReadingSection>
          )}
        </>
      )}
    </ModuleLayout>
  );
};
export default MasteringInterleavingModule;
