import React, { useState } from 'react';

const STAGES = [{ id: 'todo', label: 'To do' }, { id: 'doing', label: 'In progress' }, { id: 'done', label: 'Done' }] as const;
type Stage = typeof STAGES[number]['id'];
interface Task { id: number; text: string; column: Stage }

export default function KanbanBoard() {
  const [tasks, setTasks] = useState<Task[]>([
    { id: 1, text: 'Write Macbeth Quote Bank', column: 'todo' },
    { id: 2, text: 'Do 2023 Paper 1 Algebra Q', column: 'todo' },
    { id: 3, text: 'Practice Irish Oral Poem', column: 'doing' },
  ]);
  const [announcement, setAnnouncement] = useState('');
  const moveTask = (task: Task, column: Stage) => {
    if (column === task.column) return;
    setTasks(previous => previous.map(item => item.id === task.id ? { ...item, column } : item));
    setAnnouncement(`${task.text} moved to ${STAGES.find(stage => stage.id === column)?.label}.`);
  };
  return <section className="my-10 font-sans text-zinc-900 dark:text-zinc-100" aria-labelledby="kanban-heading">
    <div className="mb-5 border-b border-zinc-200 pb-5 dark:border-zinc-700">
      <p className="mb-2 text-xs font-bold uppercase tracking-widest text-[#B54D14] dark:text-orange-400">Try it · Make progress visible</p>
      <h4 id="kanban-heading" className="font-serif text-3xl font-semibold">Kanban Flow</h4>
      <p className="mt-2 text-base leading-relaxed text-zinc-600 dark:text-zinc-300">Move a task through the stages using its menu. Each task in Done is a win.</p>
    </div>
    <div className="grid grid-cols-1 gap-4 md:grid-cols-3">
      {STAGES.map((stage, index) => <section key={stage.id} data-stage={stage.id} aria-label={stage.label} className="min-w-0 rounded-xl border border-zinc-300 bg-white p-4 dark:border-zinc-700 dark:bg-zinc-900">
        <h5 className="flex items-center justify-between gap-3 text-base font-bold"><span><span className="mr-2 text-[#B54D14] dark:text-orange-400">0{index + 1}</span>{stage.label}</span><span aria-label={`${tasks.filter(task => task.column === stage.id).length} ${tasks.filter(task => task.column === stage.id).length === 1 ? 'task' : 'tasks'}`} className="tabular-nums">{tasks.filter(task => task.column === stage.id).length}</span></h5>
        <div className="mt-4 space-y-3">
          {tasks.filter(task => task.column === stage.id).map(task => <div key={task.id} className="border-t border-zinc-200 pt-3 dark:border-zinc-700">
            <p className="text-base font-semibold leading-snug">{task.text}</p>
            <label className="mt-3 block text-xs font-semibold text-zinc-600 dark:text-zinc-300" htmlFor={`kanban-task-${task.id}`}>Move task</label>
            <select id={`kanban-task-${task.id}`} aria-label={`Move ${task.text}`} value={task.column} onChange={event => moveTask(task, event.target.value as Stage)} className="mt-1 min-h-11 w-full rounded-lg border border-zinc-300 bg-white px-3 text-base text-zinc-900 focus-visible:outline focus-visible:outline-2 focus-visible:outline-[#B54D14] dark:border-zinc-600 dark:bg-zinc-900 dark:text-white">
              {STAGES.map(option => <option key={option.id} value={option.id}>{option.label}</option>)}
            </select>
          </div>)}
          {!tasks.some(task => task.column === stage.id) && <p className="py-2 text-sm text-zinc-500 dark:text-zinc-400">{stage.id === 'done' ? 'Your finished tasks land here.' : 'No tasks here yet.'}</p>}
        </div>
      </section>)}
    </div>
    <p role="status" className="mt-3 text-sm text-zinc-600 dark:text-zinc-300">{announcement || `${tasks.filter(task => task.column === 'done').length} of ${tasks.length} tasks done.`}</p>
  </section>;
}
