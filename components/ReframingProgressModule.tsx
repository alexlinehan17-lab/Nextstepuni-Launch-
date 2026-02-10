
/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
*/

import React, { useState } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import {
  Target, BarChart, PieChart, Gamepad2, Columns, CalendarClock, Star
} from 'lucide-react';
import { ModuleProgress } from '../types';
import { tealTheme } from '../moduleThemes';
import { Highlight, ReadingSection, MicroCommitment } from './ModuleShared';
import { ModuleLayout } from './ModuleLayout';

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
            setTasks(tasks.map(t => t.id === item.id ? { ...t, column: targetColumn } : t));
        }
    };

    return (
        <div className="my-10 p-8 md:p-12 bg-white dark:bg-zinc-800 rounded-xl border border-zinc-200 dark:border-zinc-700">
             <h4 className="font-serif text-2xl font-semibold text-zinc-800 dark:text-white text-center">Kanban Flow</h4>
             <p className="text-center text-sm text-zinc-500 dark:text-zinc-400 mb-8">Drag tasks to the "Done" column to secure a "Win".</p>
             <div className="grid grid-cols-3 gap-4">
                {['todo', 'doing', 'done'].map(col => (
                    <div key={col} data-column={col} className="kanban-col p-4 bg-zinc-50 dark:bg-zinc-800/50 rounded-xl min-h-[200px]">
                        <h5 className="font-bold text-center text-sm uppercase tracking-widest text-zinc-500 dark:text-zinc-400">{col} {col === 'done' && `(${wins})`}</h5>
                        <div className="mt-4 space-y-2">
                            {tasks.filter(t => t.column === col).map(task => (
                                <motion.div
                                    key={task.id}
                                    drag
                                    onDragEnd={(e, info) => onDragEnd(info, task)}
                                    className="p-3 bg-white dark:bg-zinc-800 rounded-lg shadow-sm text-sm font-semibold cursor-grab active:cursor-grabbing"
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
        { name: "Ecology", status: 'red', last: null },
        { name: "Genetics", status: 'amber', last: null },
        { name: "Photosynthesis", status: 'green', last: null },
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
        <div className="my-10 p-8 md:p-12 bg-white dark:bg-zinc-800 rounded-xl border border-zinc-200 dark:border-zinc-700">
            <h4 className="font-serif text-2xl font-semibold text-zinc-800 dark:text-white text-center">Retrospective Log</h4>
            <p className="text-center text-sm text-zinc-500 dark:text-zinc-400 mb-8">Rate your confidence. Let the "Worst First" rule decide your next move.</p>
            {topics.map(t => (
                <div key={t.name} className="flex items-center justify-between p-2">
                    <span className="font-bold">{t.name}</span>
                    <div className="flex gap-1">
                        <button onClick={() => updateStatus(t.name, 'red')} className={`w-6 h-6 rounded-full border ${t.status === 'red' ? 'bg-rose-500 border-rose-600' : 'bg-rose-200'}`} />
                        <button onClick={() => updateStatus(t.name, 'amber')} className={`w-6 h-6 rounded-full border ${t.status === 'amber' ? 'bg-amber-500 border-amber-600' : 'bg-amber-200'}`} />
                        <button onClick={() => updateStatus(t.name, 'green')} className={`w-6 h-6 rounded-full border ${t.status === 'green' ? 'bg-emerald-500 border-emerald-600' : 'bg-emerald-200'}`} />
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
    <ModuleLayout moduleNumber="10" moduleTitle="Reframing Progress" theme={theme} sections={sections} onBack={onBack} progress={progress} onProgressUpdate={onProgressUpdate}>
      {(activeSection) => (
        <>
          {activeSection === 0 && (
            <ReadingSection title="The Time Trap." eyebrow="Step 1" icon={Target} theme={theme}>
              <p>The biggest lie in the Leaving Cert is that "hours logged" equals "wins secured." This is the "sweat equity" model of learning. It leads to burnout and the <Highlight description="A metacognitive failure where you misinterpret the ease of processing familiar information as a sign of durable learning." theme={theme}>Illusion of Competence</Highlight>. It's time for a paradigm shift.</p>
              <p>The antidote is to reframe progress from input (time) to output (results). This means abandoning <Highlight description="Low-effort, repetitive practice without feedback (e.g., re-reading). This feels productive but yields minimal long-term learning." theme={theme}>Naive Practice</Highlight> and embracing <Highlight description="High-intensity, targeted practice on specific weaknesses with immediate feedback. This is the engine of skill acquisition." theme={theme}>Deliberate Practice</Highlight>. Naive practice is reading an essay; deliberate practice is writing one paragraph and comparing it to a H1 standard.</p>
            </ReadingSection>
          )}
          {activeSection === 1 && (
            <ReadingSection title="The 80/20 Protocol." eyebrow="Step 2" icon={BarChart} theme={theme}>
                <p>The <Highlight description="The principle that roughly 80% of effects come from 20% of causes. In the Leaving Cert, this means ~80% of marks come from ~20% of the syllabus." theme={theme}>Pareto Principle</Highlight> is your strategic compass. It dictates a hierarchy of prioritization. Your job is to identify the "Vital Few" topics that offer the highest return on investment and master them first.</p>
                <p>In Biology, for example, Ecology and Genetics are guaranteed long questions. Mastering these secures a huge chunk of your grade before you even touch the sprawling Unit 3. This is not about ignoring the other 80%; it's about securing your foundational grade with high-probability "wins" first.</p>
            </ReadingSection>
          )}
          {activeSection === 2 && (
            <ReadingSection title="The 'Banked Grade' Heist." eyebrow="Step 3" icon={PieChart} theme={theme}>
                <p>The structure of the Leaving Cert allows for a strategic "heist." A significant portion of your final grade can be secured months before the written exams. These <Highlight description="Coursework, practical projects, and oral exams that are completed before June. They are immune to exam-day nerves and represent the ultimate 'early wins'." theme={theme}>'Banked Grades'</Highlight> are your safety net.</p>
                <p>For a student taking Irish (40% Oral), History (20% RSR), and Geography (20% Field Study), **80% of a subject equivalent** is secured before June. This realization must fundamentally alter your study prioritization in the spring of your 6th year.</p>
            </ReadingSection>
          )}
          {activeSection === 3 && (
            <ReadingSection title="The Quest System." eyebrow="Step 4" icon={Gamepad2} theme={theme}>
                <p>Traditional study is demotivating because the feedback loop is too long. <Highlight description="Applying game-like elements (points, levels, quests) to non-game activities to increase motivation and engagement." theme={theme}>Gamification</Highlight> hacks your brain's dopamine reward system to make progress feel immediate and tangible.</p>
                <p>The key is to reframe the vague goal of "doing well" into a series of concrete, manageable "quests" (e.g., "The Poetry Quest," "The Algebra Boss Battle"). This fosters a <Highlight description="The desire to learn and master a skill for its own sake. It is more resilient to failure than a Performance Orientation." theme={theme}>Mastery Orientation</Highlight>, where challenges are seen as opportunities to 'level up', rather than threats to your intelligence.</p>
            </ReadingSection>
          )}
          {activeSection === 4 && (
            <ReadingSection title="The Kanban Flow." eyebrow="Step 5" icon={Columns} theme={theme}>
                <p>Ditch your anxious timetable and adopt a project management tool. A <Highlight description="An agile project management tool that visualizes workflow into columns (e.g., To Do, Doing, Done)." theme={theme}>Kanban Board</Highlight> replaces a schedule of *when* to work with a system of *what* to achieve. It visualizes progress, not the passage of time.</p>
                <p>The act of physically moving a task from "Doing" to "Done" provides a micro-dose of dopamine, reinforcing the behaviour. Over time, the "Done" column becomes a tangible pile of "Wins," countering the feeling of having done nothing despite studying for hours.</p>
                <KanbanBoard />
            </ReadingSection>
          )}
          {activeSection === 5 && (
            <ReadingSection title="The Retrospective Log." eyebrow="Step 6" icon={CalendarClock} theme={theme}>
                <p>Standard timetables fail because they are prospective—they guess what you'll need to study. A <Highlight description="A data-driven revision system where you record what you've studied and your confidence level (Red/Amber/Green), then decide what to study next based on your weakest, oldest topic." theme={theme}>Retrospective Log</Highlight> is based on actual performance. It naturally enforces Spaced Repetition and Interleaving.</p>
                <p>The rule is simple: **"Worst First."** When you sit down to study, you don't follow a pre-written plan. You look at your log and ask two questions: "What am I Red/Amber in?" and "What has the oldest date?" This algorithmic approach removes decision fatigue and ensures you are always working on your biggest weaknesses.</p>
                <RetrospectiveLog/>
            </ReadingSection>
          )}
          {activeSection === 6 && (
            <ReadingSection title="The XP Engine." eyebrow="Step 7" icon={Star} theme={theme}>
                <p>For an extra motivational boost, you can externalize the reward structure by turning the Leaving Cert into a Role-Playing Game (RPG). Assign "Experience Points" (XP) to tasks based on their difficulty and impact.</p>
                <p>A low-yield task like reading a chapter might be 50 XP. A medium-yield task like making flashcards could be 100 XP. A high-yield "win" like completing a timed exam question could be 300 XP. Accumulate XP to reach "Levels," unlocking guilt-free rewards like a movie night. This makes the invisible progress of studying visible and rewarding.</p>
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
