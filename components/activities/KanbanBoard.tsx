import { useState } from 'react';

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
  return <section className="my-10 font-sans text-[var(--module-ink)] dark:text-[var(--module-muted)]" aria-labelledby="kanban-heading">
    <div className="mb-5 border-b border-[var(--module-line)] pb-5 dark:border-[var(--module-line)]">
      <p className="mb-2 text-xs font-bold uppercase tracking-widest text-[var(--module-danger-text)] dark:text-[var(--module-ink)]">Try it · Make progress visible</p>
      <h4 id="kanban-heading" className="font-serif text-3xl font-semibold">Kanban Flow</h4>
      <p className="mt-2 text-base leading-relaxed text-[var(--module-ink)] dark:text-[var(--module-muted)]">Move a task through the stages using its menu. Each task in Done is a win.</p>
    </div>
    <div className="grid grid-cols-1 gap-4 md:grid-cols-3">
      {STAGES.map((stage, index) => <section key={stage.id} data-stage={stage.id} aria-label={stage.label} className="min-w-0 rounded-xl border border-[var(--module-line)] bg-[var(--module-surface)] p-4 dark:border-[var(--module-line)] dark:bg-[var(--module-surface)]">
        <h5 className="flex items-center justify-between gap-3 text-base font-bold"><span><span className="mr-2 text-[var(--module-danger-text)] dark:text-[var(--module-ink)]">0{index + 1}</span>{stage.label}</span><span aria-label={`${tasks.filter(task => task.column === stage.id).length} ${tasks.filter(task => task.column === stage.id).length === 1 ? 'task' : 'tasks'}`} className="tabular-nums">{tasks.filter(task => task.column === stage.id).length}</span></h5>
        <div className="mt-4 space-y-3">
          {tasks.filter(task => task.column === stage.id).map(task => <div key={task.id} className="border-t border-[var(--module-line)] pt-3 dark:border-[var(--module-line)]">
            <p className="text-base font-semibold leading-snug">{task.text}</p>
            <label className="mt-3 block text-xs font-semibold text-[var(--module-ink)] dark:text-[var(--module-muted)]" htmlFor={`kanban-task-${task.id}`}>Move task</label>
            <select id={`kanban-task-${task.id}`} aria-label={`Move ${task.text}`} value={task.column} onChange={event => moveTask(task, event.target.value as Stage)} className="mt-1 min-h-11 w-full rounded-lg border border-[var(--module-line)] bg-[var(--module-surface)] px-3 text-base text-[var(--module-ink)] focus-visible:outline focus-visible:outline-2 focus-visible:outline-[#B54D14] dark:border-[var(--module-line)] dark:bg-[var(--module-surface)] dark:text-[var(--module-ink)]">
              {STAGES.map(option => <option key={option.id} value={option.id}>{option.label}</option>)}
            </select>
          </div>)}
          {!tasks.some(task => task.column === stage.id) && <p className="py-2 text-sm text-[var(--module-muted)] dark:text-[var(--module-muted)]">{stage.id === 'done' ? 'Your finished tasks land here.' : 'No tasks here yet.'}</p>}
        </div>
      </section>)}
    </div>
    <p role="status" className="mt-3 text-sm text-[var(--module-ink)] dark:text-[var(--module-muted)]">{announcement || `${tasks.filter(task => task.column === 'done').length} of ${tasks.length} tasks done.`}</p>
  </section>;
}
