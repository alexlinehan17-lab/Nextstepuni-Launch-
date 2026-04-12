
/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
*/

import React, { useState } from 'react';
import { motion } from 'framer-motion';
import {
  Target, BarChart, PieChart, Gamepad2, Columns, CalendarClock, Star
} from 'lucide-react';
import { type ModuleProgress } from '../types';
import { tealTheme } from '../moduleThemes';
import { Highlight, ReadingSection, MicroCommitment } from './ModuleShared';
import { ModuleLayout } from './ModuleLayout';
import { useEssentialsMode } from '../hooks/useEssentialsMode';

const theme = tealTheme;

// --- INTERACTIVE COMPONENTS ---

const KanbanBoard = () => {
    const [tasks, setTasks] = useState([
        { id: 1, text: "Write Macbeth Quote Bank", column: 'todo' },
        { id: 2, text: "Do 2023 Paper 1 Algebra Q", column: 'todo' },
        { id: 3, text: "Practice Irish Oral Poem", column: 'doing' },
    ]);
    const [wins, setWins] = useState(0);

    const onDragEnd = (info: any, item: any) => {
        const point = info.point;
        const columns = document.querySelectorAll('.kanban-col');
        let targetColumn = null;
        columns.forEach((col: any) => {
            const rect = col.getBoundingClientRect();
            if (point.x > rect.left && point.x < rect.right && point.y > rect.top && point.y < rect.bottom) {
                targetColumn = col.dataset.column;
            }
        });

        if (targetColumn) {
            if (item.column !== 'done' && targetColumn === 'done') {
                setWins(w => w + 1);
            }
            setTasks(prev => prev.map(t => t.id === item.id ? { ...t, column: targetColumn } : t));
        }
    };

    return (
        <div className="my-10 rounded-2xl p-6 md:p-8" style={{ backgroundColor: '#F8F8F8', borderRadius: 18 }}>
             <h4 className="font-serif text-2xl font-semibold text-zinc-800 dark:text-white text-center">Kanban Flow</h4>
             <p className="text-center text-sm text-zinc-500 dark:text-zinc-400 mb-8">Drag tasks to the "Done" column to secure a "Win".</p>
             <div className="grid grid-cols-3 gap-4">
                {['todo', 'doing', 'done'].map(col => (
                    <div key={col} data-column={col} className="kanban-col p-4 rounded-xl min-h-[200px]" style={{ backgroundColor: '#FFFFFF', border: '1.5px solid #E7E5E4' }}>
                        <h5 className="font-bold text-center text-sm uppercase tracking-widest text-zinc-500 dark:text-zinc-400">{col} {col === 'done' && `(${wins})`}</h5>
                        <div className="mt-4 space-y-2">
                            {tasks.filter(t => t.column === col).map(task => (
                                <motion.div
                                    key={task.id}
                                    drag
                                    onDragEnd={(e, info) => onDragEnd(info, task)}
                                    className="p-3 rounded-lg text-sm font-semibold cursor-grab active:cursor-grabbing" style={{ backgroundColor: '#FFFFFF', border: '2.5px solid #1C1917', borderRadius: 10, boxShadow: '3px 3px 0px 0px #1C1917' }}
                                >{task.text}</motion.div>
                            ))}
                        </div>
                    </div>
                ))}
             </div>
        </div>
    );
};

const RetrospectiveLog = () => {
    const [topics, setTopics] = useState([
        { name: "Ecology", status: 'red' },
        { name: "Genetics", status: 'amber' },
        { name: "Photosynthesis", status: 'green' },
    ]);
    const [nextTopic, setNextTopic] = useState("Ecology (Red)");

    const updateStatus = (name: string, newStatus: 'red' | 'amber' | 'green') => {
        setTopics(topics.map(t => t.name === name ? { ...t, status: newStatus } : t));
    };

    const findNext = () => {
        const red = topics.find(t => t.status === 'red');
        if (red) { setNextTopic(`${red.name} (Red)`); return; }
        const amber = topics.find(t => t.status === 'amber');
        if (amber) { setNextTopic(`${amber.name} (Amber)`); return; }
        setNextTopic("Everything's Green! Review oldest topic.");
    };

    return (
        <div className="my-10 rounded-2xl p-6 md:p-8" style={{ backgroundColor: '#F8F8F8', borderRadius: 18 }}>
            <h4 className="font-serif text-2xl font-semibold text-zinc-800 dark:text-white text-center">Retrospective Log</h4>
            <p className="text-center text-sm text-zinc-500 dark:text-zinc-400 mb-8">Rate your confidence. Let the "Worst First" rule decide your next move.</p>
            {topics.map(t => (
                <div key={t.name} className="flex items-center justify-between p-2">
                    <span className="font-bold">{t.name}</span>
                    <div className="flex gap-1">
                        <button aria-label="Mark as struggling (red)" onClick={() => updateStatus(t.name, 'red')} className={`w-6 h-6 rounded-full border ${t.status === 'red' ? 'bg-rose-500 border-rose-600' : 'bg-rose-200'}`} />
                        <button aria-label="Mark as okay (amber)" onClick={() => updateStatus(t.name, 'amber')} className={`w-6 h-6 rounded-full border ${t.status === 'amber' ? 'bg-amber-500 border-amber-600' : 'bg-amber-200'}`} />
                        <button aria-label="Mark as confident (green)" onClick={() => updateStatus(t.name, 'green')} className={`w-6 h-6 rounded-full border ${t.status === 'green' ? 'bg-emerald-500 border-emerald-600' : 'bg-emerald-200'}`} />
                    </div>
                </div>
            ))}
             <div className="mt-6 text-center">
                 <button onClick={findNext} className="px-4 py-2 bg-zinc-800 text-white text-xs font-bold rounded-lg">Find Next Task</button>
                 <p className="mt-4 text-sm">Next up: <span className="font-bold text-teal-600">{nextTopic}</span></p>
             </div>
        </div>
    );
};


// --- MODULE COMPONENT ---
const ReframingProgressModule: React.FC<{ onBack: () => void; progress: ModuleProgress; onProgressUpdate: (progress: ModuleProgress) => void }> = ({ onBack, progress, onProgressUpdate }) => {
  const essentials = useEssentialsMode();
  const sections = [
    { id: 'time-trap', title: 'The Time Trap', eyebrow: '01 // Naive vs. Deliberate', icon: Target },
    { id: 'pareto-protocol', title: 'The 80/20 Protocol', eyebrow: '02 // The Vital Few', icon: BarChart },
    { id: 'banked-grade', title: 'The "Banked Grade" Heist', eyebrow: '03 // Securing Early Wins', icon: PieChart },
    { id: 'quest-system', title: 'The Quest System', eyebrow: '04 // Mastery vs. Performance', icon: Gamepad2 },
    { id: 'kanban-flow', title: 'The Kanban Flow', eyebrow: '05 // Visualizing Work', icon: Columns },
    { id: 'retrospective-log', title: 'The Retrospective Log', eyebrow: '06 // Data-Driven Study', icon: CalendarClock },
    { id: 'xp-engine', title: 'The XP Engine', eyebrow: '07 // Gamifying the Grind', icon: Star },
  ];

  return (
    <ModuleLayout moduleNumber="10" moduleTitle="Reframing Progress" moduleSubtitle="The Outcome-Based Approach" moduleDescription={`Stop counting hours and start counting wins. This module shows you how to track what actually matters so you can see real progress every single day.`} theme={theme} sections={sections} onBack={onBack} progress={progress} onProgressUpdate={onProgressUpdate} finishButtonText="Track Your Wins">
      {(activeSection) => (
        <>
          {activeSection === 0 && (
            <ReadingSection title="The Time Trap." eyebrow="Step 1" icon={Target} theme={theme}>
              {essentials ? (
                <>
                  <p>Stop counting hours. Start counting results. Sitting at a desk for five hours means nothing if you learned nothing. Ditch <Highlight description="Stuff like re-reading your notes or highlighting everything -- it feels productive but barely sticks. You're just going through the motions." theme={theme}>Naive Practice</Highlight> like re-reading notes. Switch to <Highlight description="Focused practice where you work on the specific things you're weak at and get feedback straight away. It's harder, but it's how you actually improve." theme={theme}>Deliberate Practice</Highlight>. That means working on your weak spots and getting feedback. Write a paragraph and compare it to a H1 answer. That is real progress.</p>
                </>
              ) : (
                <>
                  <p>The biggest lie in the Leaving Cert is that "hours logged" equals "wins secured." Sitting at a desk for five hours doesn't mean you learned anything. It leads to burnout and the <Highlight description="That feeling when you read your notes and think 'yeah, I know this' -- but then you can't actually answer the question in the exam. Recognising something is not the same as knowing it." theme={theme}>Illusion of Competence</Highlight>. It's time to flip this on its head.</p>
                  <p>Instead of measuring time spent, start measuring results. That means ditching <Highlight description="Stuff like re-reading your notes or highlighting everything -- it feels productive but barely sticks. You're just going through the motions." theme={theme}>Naive Practice</Highlight> and switching to <Highlight description="Focused practice where you work on the specific things you're weak at and get feedback straight away. It's harder, but it's how you actually improve." theme={theme}>Deliberate Practice</Highlight>. Naive practice is reading an essay; deliberate practice is writing one paragraph and comparing it to a H1 standard.</p>
                </>
              )}
            </ReadingSection>
          )}
          {activeSection === 1 && (
            <ReadingSection title="The 80/20 Protocol." eyebrow="Step 2" icon={BarChart} theme={theme}>
                {essentials ? (
                  <>
                    <p>Use the <Highlight description="Roughly 80% of your marks come from about 20% of the syllabus. So if you figure out which topics come up again and again, you can lock in most of your grade by nailing those first." theme={theme}>Pareto Principle</Highlight>. About 80% of your marks come from 20% of the syllabus. Find the topics that always come up. Nail those first. In Biology, Ecology and Genetics are guaranteed long questions. Master these and you lock in a huge chunk of your grade. Bank the easy wins before tackling the rest.</p>
                  </>
                ) : (
                  <>
                    <p>The <Highlight description="Roughly 80% of your marks come from about 20% of the syllabus. So if you figure out which topics come up again and again, you can lock in most of your grade by nailing those first." theme={theme}>Pareto Principle</Highlight> is your cheat code for prioritising. Your job is to figure out which topics give you the most marks for the least effort, and tackle those first.</p>
                    <p>In Biology, for example, Ecology and Genetics are guaranteed long questions. Mastering these secures a huge chunk of your grade before you even touch the sprawling Unit 3. This isn't about ignoring everything else -- it's about banking the easy wins first so you're already in a strong position.</p>
                  </>
                )}
            </ReadingSection>
          )}
          {activeSection === 2 && (
            <ReadingSection title="The 'Banked Grade' Heist." eyebrow="Step 3" icon={PieChart} theme={theme}>
                {essentials ? (
                  <>
                    <p>A chunk of your final grade can be locked in before the written exam. Your Irish oral, History RSR, and Geography field study are <Highlight description="Things like your Irish oral, your History RSR, or your Geography field study. They're done and dusted before June, so exam-day nerves can't touch them. Free marks, basically." theme={theme}>'Banked Grades'</Highlight>. They are done before June. Exam-day nerves cannot touch them. For Irish (40% Oral), History (20% RSR), and Geography (20% Field Study), that is 80% of a subject equivalent already safe. Focus on these early.</p>
                  </>
                ) : (
                  <>
                    <p>Here's something most people don't think about: a big chunk of your final grade can be locked in months before the written exams even happen. These <Highlight description="Things like your Irish oral, your History RSR, or your Geography field study. They're done and dusted before June, so exam-day nerves can't touch them. Free marks, basically." theme={theme}>'Banked Grades'</Highlight> are your safety net.</p>
                    <p>For a student taking Irish (40% Oral), History (20% RSR), and Geography (20% Field Study), <strong>80% of a subject equivalent</strong> is already in the bag before June. Once you realise that, it completely changes what you should be focusing on in the spring of 6th year.</p>
                  </>
                )}
            </ReadingSection>
          )}
          {activeSection === 3 && (
            <ReadingSection title="The Quest System." eyebrow="Step 4" icon={Gamepad2} theme={theme}>
                {essentials ? (
                  <>
                    <p>Turn your study into a game using <Highlight description="Turning your study into something more like a game -- with points, levels, and clear goals. It makes boring work feel more rewarding because you can actually see yourself making progress." theme={theme}>Gamification</Highlight>. Break "doing well" into bite-sized quests. Call them things like "The Poetry Quest" or "The Algebra Boss Battle." This builds <Highlight description="When you focus on actually getting better at something rather than just trying to look smart. If you hit a wall, you see it as a chance to level up, not proof that you're thick." theme={theme}>Mastery Orientation</Highlight>. Challenges become chances to level up. You stop fearing failure and start chasing progress.</p>
                  </>
                ) : (
                  <>
                    <p>Normal study is demotivating because you never feel like you're getting anywhere. <Highlight description="Turning your study into something more like a game -- with points, levels, and clear goals. It makes boring work feel more rewarding because you can actually see yourself making progress." theme={theme}>Gamification</Highlight> gives your brain quick wins so progress feels real and immediate.</p>
                    <p>The trick is to break the vague goal of "doing well" into specific, bite-sized "quests" (e.g., "The Poetry Quest," "The Algebra Boss Battle"). This builds a <Highlight description="When you focus on actually getting better at something rather than just trying to look smart. If you hit a wall, you see it as a chance to level up, not proof that you're thick." theme={theme}>Mastery Orientation</Highlight>, where challenges feel like chances to level up rather than threats to how smart you are.</p>
                  </>
                )}
            </ReadingSection>
          )}
          {activeSection === 4 && (
            <ReadingSection title="The Kanban Flow." eyebrow="Step 5" icon={Columns} theme={theme}>
                {essentials ? (
                  <>
                    <p>Ditch rigid timetables. Use a <Highlight description="A simple board with three columns: To Do, Doing, and Done. Instead of planning when to study, you plan what to get done -- and you can see your progress pile up in the Done column." theme={theme}>Kanban Board</Highlight>. It has three columns: To Do, Doing, Done. You track what you finish, not how long you sat there. Moving tasks to "Done" gives your brain a reward hit. Your Done column fills up with real wins.</p>
                  </>
                ) : (
                  <>
                    <p>Ditch the rigid timetable and try something that actually works. A <Highlight description="A simple board with three columns: To Do, Doing, and Done. Instead of planning when to study, you plan what to get done -- and you can see your progress pile up in the Done column." theme={theme}>Kanban Board</Highlight> swaps a schedule of <em>when</em> to work for a system of <em>what</em> to get done. You see progress, not just time passing.</p>
                    <p>There's something genuinely satisfying about moving a task from "Doing" to "Done." It gives your brain a little hit of reward, which makes you want to keep going. Over time, your "Done" column fills up with real wins -- so you never feel like you studied for hours with nothing to show for it.</p>
                  </>
                )}
                <KanbanBoard />
            </ReadingSection>
          )}
          {activeSection === 5 && (
            <ReadingSection title="The Retrospective Log." eyebrow="Step 6" icon={CalendarClock} theme={theme}>
                {essentials ? (
                  <>
                    <p>After each study session, rate your confidence in each topic. Use Red, Amber, or Green. This is your <Highlight description="A simple tracking system: after each study session, you rate how confident you feel in each topic (Red, Amber, or Green). Then next time you sit down, you pick the weakest, oldest topic first. No guessing." theme={theme}>Retrospective Log</Highlight>. Next time you sit down, follow one rule: <strong>"Worst First."</strong> Pick the weakest, oldest topic. No guessing. No following a rigid plan. You always tackle your biggest weak spot first.</p>
                  </>
                ) : (
                  <>
                    <p>Normal timetables fail because they're just guesses about what you'll need to study. A <Highlight description="A simple tracking system: after each study session, you rate how confident you feel in each topic (Red, Amber, or Green). Then next time you sit down, you pick the weakest, oldest topic first. No guessing." theme={theme}>Retrospective Log</Highlight> is based on what you've actually done and how you actually feel about each topic. It naturally keeps you revising the right stuff at the right time.</p>
                    <p>The rule is simple: <strong>"Worst First."</strong> When you sit down to study, you don't follow a pre-written plan. You look at your log and ask two questions: "What am I Red/Amber in?" and "What has the oldest date?" This takes the guesswork out of deciding what to study and makes sure you're always tackling your biggest weak spots.</p>
                  </>
                )}
                <RetrospectiveLog/>
            </ReadingSection>
          )}
          {activeSection === 6 && (
            <ReadingSection title="The XP Engine." eyebrow="Step 7" icon={Star} theme={theme}>
                {essentials ? (
                  <>
                    <p>Give yourself Experience Points (XP) for study tasks. Reading a chapter is 50 XP. Making flashcards is 100 XP. A timed exam question is 300 XP. Stack enough XP to "Level Up" and earn a guilt-free reward. This turns invisible progress into something you can see and feel good about.</p>
                  </>
                ) : (
                  <>
                    <p>Want an extra motivational boost? Turn your Leaving Cert into a Role-Playing Game. Give yourself "Experience Points" (XP) for tasks based on how useful they actually are.</p>
                    <p>Something easy like reading a chapter might be worth 50 XP. Making flashcards could be 100 XP. A proper timed exam question -- that's a 300 XP win. Stack up enough XP to hit a new "Level" and unlock a guilt-free reward like a movie night. It takes all that invisible progress you're making and turns it into something you can actually see and feel good about.</p>
                  </>
                )}
                 <MicroCommitment theme={theme}>
                    <p>Define your first "Level Up." What small, enjoyable reward can you give yourself for earning your first 1000 XP? Write it down. Now you have your first quest.</p>
                </MicroCommitment>
            </ReadingSection>
          )}
        </>
      )}
    </ModuleLayout>
  );
};
export default ReframingProgressModule;
