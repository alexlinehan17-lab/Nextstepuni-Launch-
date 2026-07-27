/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 *
 * GC assign panel (feature E9) — a counsellor sets a revision task for the whole
 * school with a title, a kind and an optional due date. Ship-gated: renders
 * nothing until ASSIGNMENTS_LIVE is on (see compliance/assignments-plan.md).
 */

import React, { useEffect, useState } from 'react';
import { Plus, Trash2 } from 'lucide-react';
import { saveInBackground } from '../../utils/firestoreWrite';
import {
  ASSIGNMENTS_LIVE,
  loadAssignments,
  saveAssignments,
  type Assignment,
  type AssignmentKind,
} from '../../data/assignments';

const KINDS: { k: AssignmentKind; label: string }[] = [
  { k: 'topic', label: 'Topic drill' },
  { k: 'mock', label: 'Mock set' },
  { k: 'pack', label: 'Revision pack' },
  { k: 'module', label: 'Module' },
  { k: 'general', label: 'General' },
];

const GCAssignPanel: React.FC<{ school: string; gcName?: string }> = ({ school, gcName }) => {
  const [items, setItems] = useState<Assignment[]>([]);
  const [title, setTitle] = useState('');
  const [kind, setKind] = useState<AssignmentKind>('topic');
  const [dueIso, setDueIso] = useState('');

  useEffect(() => {
    if (!ASSIGNMENTS_LIVE) return;
    loadAssignments(school).then(setItems);
  }, [school]);

  if (!ASSIGNMENTS_LIVE) return null;

  const persist = async (next: Assignment[]) => {
    // No busy flag around the write: awaiting it left the panel permanently
    // disabled on a throttled school network, because a write promise only
    // settles on server ack. The list updates instantly and the save queues.
    const previous = items;
    setItems(next);
    saveInBackground(
      saveAssignments(school, next),
      'GCAssignPanel.saveAssignments',
      () => setItems(previous),
    );
  };
  const add = () => {
    if (!title.trim()) return;
    const a: Assignment = {
      id: `${Date.now().toString(36)}-${Math.floor(Math.random() * 1e6).toString(36)}`,
      title: title.trim(),
      kind,
      dueIso: dueIso || undefined,
      createdTs: Date.now(),
      createdByName: gcName,
    };
    persist([a, ...items]);
    setTitle('');
    setDueIso('');
  };
  const remove = (id: string) => persist(items.filter(a => a.id !== id));

  return (
    <div className="p-6 max-w-3xl mx-auto w-full">
      <h2 className="text-lg font-semibold text-zinc-900 dark:text-zinc-100 mb-1">Set revision</h2>
      <p className="text-sm text-zinc-500 dark:text-zinc-400 mb-4">Assign a task to every student in your school. They’ll see it and tick it off.</p>

      <div className="rounded-xl border border-zinc-200 dark:border-zinc-800 bg-white dark:bg-zinc-900 p-4 mb-5">
        <input value={title} onChange={e => setTitle(e.target.value)} placeholder="e.g. Drill Calculus questions from 2019–2023"
          className="w-full mb-3 px-3 py-2 rounded-lg border border-zinc-200 dark:border-zinc-700 bg-white dark:bg-zinc-900 text-sm outline-none focus:border-zinc-400" />
        <div className="flex flex-wrap items-center gap-2">
          <select value={kind} onChange={e => setKind(e.target.value as AssignmentKind)} className="px-3 py-2 rounded-lg border border-zinc-200 dark:border-zinc-700 bg-white dark:bg-zinc-900 text-sm">
            {KINDS.map(x => <option key={x.k} value={x.k}>{x.label}</option>)}
          </select>
          <input type="date" value={dueIso} onChange={e => setDueIso(e.target.value)} className="px-3 py-2 rounded-lg border border-zinc-200 dark:border-zinc-700 bg-white dark:bg-zinc-900 text-sm" />
          <button onClick={add} disabled={!title.trim()} className="inline-flex items-center gap-1.5 px-4 py-2 rounded-lg bg-zinc-900 dark:bg-zinc-100 text-white dark:text-zinc-900 text-sm font-medium disabled:opacity-40">
            <Plus size={15} /> Assign
          </button>
        </div>
      </div>

      {items.length > 0 && (
        <div className="space-y-1.5">
          {items.map(a => (
            <div key={a.id} className="flex items-center gap-3 rounded-lg border border-zinc-200 dark:border-zinc-800 bg-white dark:bg-zinc-900 px-3.5 py-2.5">
              <span className="flex-1 min-w-0">
                <span className="block text-sm font-medium text-zinc-800 dark:text-zinc-100 truncate">{a.title}</span>
                <span className="block text-[11.5px] text-zinc-400">{KINDS.find(k => k.k === a.kind)?.label}{a.dueIso ? ` · due ${a.dueIso}` : ''}</span>
              </span>
              <button onClick={() => remove(a.id)} aria-label="Remove assignment" className="shrink-0 w-8 h-8 rounded-lg flex items-center justify-center border border-zinc-200 dark:border-zinc-700 text-zinc-400 hover:text-zinc-600">
                <Trash2 size={14} />
              </button>
            </div>
          ))}
        </div>
      )}
    </div>
  );
};

export default GCAssignPanel;
