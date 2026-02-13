
/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
*/

import React, { useState } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import {
  Layers, Shuffle, Brain, ListChecks, Wrench
} from 'lucide-react';
import { ModuleProgress } from '../types';
import { purpleTheme } from '../moduleThemes';
import { Highlight, ReadingSection, MicroCommitment } from './ModuleShared';
import { ModuleLayout } from './ModuleLayout';

const theme = purpleTheme;

// --- INTERACTIVE COMPONENTS ---

const StudyPlannerInteractive = () => {
    const [planType, setPlanType] = useState<'blocked' | 'interleaved'>('blocked');
    const blockedSchedule = { Mon: ['Maths', 'Maths', 'Maths'], Tue: ['English', 'English', 'English'], Wed: ['Biology', 'Biology', 'Biology'] };
    const interleavedSchedule = { Mon: ['Maths', 'English', 'French'], Tue: ['English', 'Biology', 'History'], Wed: ['Biology', 'Maths', 'English'] };
    const schedule = planType === 'blocked' ? blockedSchedule : interleavedSchedule;

    return (
        <div className="my-10 p-8 md:p-12 bg-white dark:bg-zinc-800 rounded-xl border border-zinc-200 dark:border-zinc-700">
            <h4 className="font-serif text-2xl font-semibold text-zinc-800 dark:text-white text-center">Weekly Schedule Architect</h4>
            <div className="flex justify-center gap-2 p-1 bg-zinc-100 dark:bg-zinc-800 rounded-full my-6 max-w-sm mx-auto">
                <button onClick={() => setPlanType('blocked')} className={`w-full px-4 py-2 text-xs font-bold rounded-full ${planType === 'blocked' ? 'bg-white shadow' : ''}`}>Blocked Schedule</button>
                <button onClick={() => setPlanType('interleaved')} className={`w-full px-4 py-2 text-xs font-bold rounded-full ${planType === 'interleaved' ? 'bg-white shadow' : ''}`}>Interleaved Schedule</button>
            </div>
            <div className="grid grid-cols-3 gap-2 text-center text-xs">
                {Object.entries(schedule).map(([day, subjects]) => (
                    <div key={day}>
                        <p className="font-bold mb-2">{day}</p>
                        <div className="space-y-1">
                            {subjects.map((sub, i) => (
                                <motion.div key={`${day}-${i}`} layoutId={`${day}-${i}-${sub}`} className="p-2 bg-zinc-50 dark:bg-zinc-800/50 border border-zinc-200 dark:border-zinc-700 rounded-md">{sub}</motion.div>
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
    const problems = [
        { id: 1, text: "y = sin(x\u00B2)", correct: "chain" },
        { id: 2, text: "y = x\u00B2sin(x)", correct: "product" },
    ];

    return (
        <div className="my-10 p-8 md:p-12 bg-white dark:bg-zinc-800 rounded-xl border border-zinc-200 dark:border-zinc-700">
             <h4 className="font-serif text-2xl font-semibold text-zinc-800 dark:text-white text-center">Problem Spotter</h4>
             <p className="text-center text-sm text-zinc-500 dark:text-zinc-400 mb-8">Calculus: Don't solve. Just identify the correct rule.</p>
             {problems.map(p => (
                <div key={p.id} className="mb-4">
                    <p className="text-center font-mono bg-zinc-100 dark:bg-zinc-800 p-4 rounded-xl mb-2">{p.text}</p>
                    <div className="grid grid-cols-2 gap-2">
                        <button onClick={() => setChoice({...choice, [p.id]:'chain'})} className={`p-2 text-xs rounded-lg border ${choice[p.id] && (choice[p.id] === 'chain' && p.correct === 'chain' ? 'bg-emerald-100 border-emerald-300' : choice[p.id] === 'chain' ? 'bg-rose-100 border-rose-300' : 'bg-zinc-100 border-zinc-200 dark:border-zinc-700')}`}>Chain Rule</button>
                        <button onClick={() => setChoice({...choice, [p.id]:'product'})} className={`p-2 text-xs rounded-lg border ${choice[p.id] && (choice[p.id] === 'product' && p.correct === 'product' ? 'bg-emerald-100 border-emerald-300' : choice[p.id] === 'product' ? 'bg-rose-100 border-rose-300' : 'bg-zinc-100 border-zinc-200 dark:border-zinc-700')}`}>Product Rule</button>
                    </div>
                </div>
             ))}
        </div>
    );
};

const RetrospectiveRevisionLog = () => {
    const [topics, setTopics] = useState([
        { name: "Algebra", status: 'red', lastStudied: null },
        { name: "Statistics", status: 'amber', lastStudied: null },
        { name: "Geometry", status: 'green', lastStudied: null },
        { name: "Functions", status: 'red', lastStudied: null },
        { name: "Number", status: 'amber', lastStudied: null },
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
         <div className="my-10 p-8 md:p-12 bg-white dark:bg-zinc-800 rounded-xl border border-zinc-200 dark:border-zinc-700">
             <h4 className="font-serif text-2xl font-semibold text-zinc-800 dark:text-white text-center">Retrospective Revision Log</h4>
             <p className="text-center text-sm text-zinc-500 dark:text-zinc-400 mb-8">Update your confidence after studying. The "Worst First" rule will guide you.</p>
             <div className="space-y-3">
                {topics.map(topic => (
                    <div key={topic.name} className="p-3 bg-zinc-50 dark:bg-zinc-800/50 border border-zinc-200 dark:border-zinc-700 rounded-lg flex justify-between items-center">
                        <span className="font-bold text-sm">{topic.name}</span>
                        <div className="flex gap-1">
                            <button onClick={() => updateStatus(topic.name, 'red')} className={`w-6 h-6 rounded-full border ${topic.status === 'red' ? 'bg-rose-500 border-rose-600' : 'bg-rose-200 border-rose-300'}`}></button>
                            <button onClick={() => updateStatus(topic.name, 'amber')} className={`w-6 h-6 rounded-full border ${topic.status === 'amber' ? 'bg-amber-500 border-amber-600' : 'bg-amber-200 border-amber-300'}`}></button>
                            <button onClick={() => updateStatus(topic.name, 'green')} className={`w-6 h-6 rounded-full border ${topic.status === 'green' ? 'bg-emerald-500 border-emerald-600' : 'bg-emerald-200 border-emerald-300'}`}></button>
                        </div>
                    </div>
                ))}
             </div>
             <div className="mt-6 text-center">
                 <button onClick={findNextTopic} className="px-4 py-2 bg-zinc-800 text-white text-xs font-bold rounded-lg">Find Next Topic</button>
                 <p className="mt-4 text-sm">Next up: <span className="font-bold text-purple-600">{nextTopic}</span></p>
             </div>
        </div>
    );
}

// --- MODULE COMPONENT ---
const MasteringInterleavingModule: React.FC<{ onBack: () => void; progress: ModuleProgress; onProgressUpdate: (progress: ModuleProgress) => void }> = ({ onBack, progress, onProgressUpdate }) => {
  const sections = [
    { id: 'illusion-of-mastery', title: 'The Illusion of "Mastery"', eyebrow: '01 // The Blocked Trap', icon: Layers },
    { id: 'topic-salad', title: 'The "Topic Salad" Method', eyebrow: '02 // The Solution', icon: Shuffle },
    { id: 'desirable-difficulty', title: 'The Science of "Desirable Difficulty"', eyebrow: '03 // Why It Works', icon: Brain },
    { id: 'retrospective-timetable', title: 'The Retrospective Timetable', eyebrow: '04 // The System', icon: ListChecks },
    { id: 'subject-hacker', title: 'Your Interleaving Blueprint', eyebrow: '05 // The Action Plan', icon: Wrench },
  ];

  return (
    <ModuleLayout moduleNumber="03" moduleTitle="Mastering Interleaving" moduleSubtitle="The Topic Salad Method" moduleDescription={`Ditch "blocked" study and learn the science of mixing topics to build deep, flexible knowledge that stands up under exam pressure.`} theme={theme} sections={sections} onBack={onBack} progress={progress} onProgressUpdate={onProgressUpdate}>
      {(activeSection) => (
        <>
          {activeSection === 0 && (
            <ReadingSection title="The Illusion of 'Mastery'." eyebrow="Step 1" icon={Layers} theme={theme}>
              <p>Most students study using <Highlight description="The common study method of focusing on one topic until you feel you've mastered it before moving to the next (e.g., AAABBBCCC)." theme={theme}>Blocked Practice</Highlight>. You spend Monday night on Maths, Tuesday on English, Wednesday on Biology. It feels productive. After three hours of Algebra, you feel like you've mastered it. But this is an <Highlight description="The misleading feeling of mastery you get from blocked practice, because the information is still fresh in your short-term memory." theme={theme}>Illusion of Competence</Highlight>.</p>
              <p>The problem is, your brain isn't being trained for the real Leaving Cert. The exam is not blocked; it's a random mix of topics. When you do 20 algebra problems in a row, you don't have to figure out *what* to do, only *how* to do it. You fail to train the crucial <Highlight description="The crucial ability to tell the difference between similar types of problems or concepts to know which strategy to apply (e.g., telling integration from differentiation)." theme={theme}>discriminative skills</Highlight> needed to succeed under pressure.</p>
            </ReadingSection>
          )}
           {activeSection === 1 && (
            <ReadingSection title="The 'Topic Salad' Method." eyebrow="Step 2" icon={Shuffle} theme={theme}>
              <p>The solution is simple, but powerful: <Highlight description="The highly effective study strategy of mixing different topics or problem types within a single study session (e.g., ABCABCABC)." theme={theme}>Interleaving</Highlight>. Instead of a "topic block," your study session should be a "topic salad." A fruit salad isn't a pile of apples next to a pile of bananas; it's a mix. Your study should be the same.</p>
              <p>This happens at two levels. <Highlight description="Mixing subjects within your weekly timetable (e.g., Maths, English, and Biology on Monday)." theme={theme}>Macro-interleaving</Highlight> is about your weekly schedule: instead of one subject for 3 hours, study three subjects for 1 hour each. <Highlight description="Mixing topics *within* a single subject session (e.g., doing a mix of Algebra, Stats, and Geometry questions)." theme={theme}>Micro-interleaving</Highlight> is about mixing topics *within* a subject. This is harder, but as we'll see, the effort is where the learning happens.</p>
              <StudyPlannerInteractive />
            </ReadingSection>
          )}
           {activeSection === 2 && (
            <ReadingSection title="The Science of 'Desirable Difficulty'." eyebrow="Step 3" icon={Brain} theme={theme}>
              <p>Interleaving feels harder. When you switch from Maths to English, your brain has to work to "reload" a new context. This effort is called a <Highlight description="The idea from cognitive science that learning tasks that feel harder and more effortful actually lead to much stronger, long-term memory." theme={theme}>Desirable Difficulty</Highlight>. Blocked practice feels easy because it's like re-watching the same scene of a movie over and over. Interleaving forces your brain to constantly change the channel, which strengthens its ability to find the right channel under pressure.</p>
              <p>This is the <Highlight description="The core theory behind interleaving. It says that mixing similar concepts forces the brain to notice the subtle differences ('discriminative features') between them, leading to deeper learning." theme={theme}>Discriminative-Contrast Hypothesis</Highlight>. By placing similar but different concepts next to each other (like differentiation and integration), interleaving forces your brain to spot the differences. You're not just learning a rule; you're learning *when* to use that rule.</p>
              <ProblemTypeSpotter/>
            </ReadingSection>
          )}
          {activeSection === 3 && (
            <ReadingSection title="The Retrospective Timetable." eyebrow="Step 4" icon={ListChecks} theme={theme}>
              <p>Interleaving can feel chaotic. The best way to manage it is to abandon your rigid, forward-planning timetable and adopt a <Highlight description="A powerful way to plan your study by tracking what you've already done and focusing on your weakest areas first, rather than planning weeks in advance." theme={theme}>Retrospective Revision Timetable</Highlight>. Instead of deciding what to study next week, you decide what to study *right now* based on what you're worst at.</p>
              <p>The system is simple: 1. List every topic in a subject. 2. After you study a topic, you colour-code it: Green (I know this), Amber (It's okay), or Red (I'm lost). 3. The next time you study that subject, you follow the <Highlight description="The core principle of the Retrospective Timetable: always prioritize the topic you are least confident in (Red/Amber) to ensure you address your biggest weaknesses." theme={theme}>"Worst First" Rule</Highlight>: you must work on a Red topic. This naturally enforces interleaving and spacing, because you're constantly jumping between your weakest areas across the entire course.</p>
              <RetrospectiveRevisionLog />
            </ReadingSection>
          )}
           {activeSection === 4 && (
            <ReadingSection title="Your Interleaving Blueprint." eyebrow="Step 5" icon={Wrench} theme={theme}>
              <p>You have the science. Now you need the action plan. Interleaving isn't a vague concept; it's a set of specific, practical strategies you can apply to every subject you study for the Leaving Cert.</p>
              <p>From the "Mixed Bag" approach in Maths to the "Poetry Roulette" in English, the goal is always the same: break up the blocks, embrace the struggle of switching, and train your brain for the reality of the exam. This is not about studying more; it's about studying smarter. It's time to build your own interleaved engine.</p>
              <MicroCommitment theme={theme}>
                <p>Tonight, take your hardest subject. Instead of studying one chapter for an hour, pick three different chapters and spend just 20 minutes on each. Feel the "desirable difficulty" of switching between them.</p>
              </MicroCommitment>
            </ReadingSection>
          )}
        </>
      )}
    </ModuleLayout>
  );
};
export default MasteringInterleavingModule;
