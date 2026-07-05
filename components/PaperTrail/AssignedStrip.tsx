/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 *
 * Assigned-to-you strip (feature E9, student side). Shows the revision tasks the
 * student's GC has set, newest first, with a one-tap "Mark done". Ship-gated:
 * renders nothing until ASSIGNMENTS_LIVE is on and a school is provided (see
 * compliance/assignments-plan.md — threading the student's school here is the
 * final activation step).
 */

import React, { useEffect, useState } from 'react';
import { ClipboardList, Check } from 'lucide-react';
import {
  ASSIGNMENTS_LIVE,
  assignmentStatus,
  loadAssignments,
  markAssignmentComplete,
  type Assignment,
} from '../../data/assignments';

const STATUS_STYLE = {
  done: { bg: '#E8F2EC', fg: '#1F5F3E', label: 'Done' },
  overdue: { bg: '#FBEAE8', fg: '#8E2A20', label: 'Overdue' },
  open: { bg: '#FDEEDF', fg: '#8C3A0E', label: 'To do' },
} as const;

interface Props {
  uid?: string;
  school?: string;
  /** From the student's own progress doc: assignmentId → completed epoch ms. */
  completions?: Record<string, number>;
}

const AssignedStrip: React.FC<Props> = ({ uid, school, completions = {} }) => {
  const [items, setItems] = useState<Assignment[]>([]);
  const [done, setDone] = useState<Record<string, number>>(completions);

  useEffect(() => {
    if (!ASSIGNMENTS_LIVE || !school) return;
    loadAssignments(school).then(setItems);
  }, [school]);

  if (!ASSIGNMENTS_LIVE || !school || items.length === 0) return null;

  const todayIso = new Date(Date.now()).toISOString().slice(0, 10);
  const complete = (id: string) => {
    const ts = Date.now();
    setDone(d => ({ ...d, [id]: ts }));
    if (uid) markAssignmentComplete(uid, id, ts);
  };

  return (
    <div className="w-full rounded-2xl border-2 border-[#1a1a1a] dark:border-zinc-700 bg-white dark:bg-zinc-900 px-4 py-3.5 mb-5">
      <p className="text-[10.5px] font-bold uppercase tracking-[0.12em] mb-2 flex items-center gap-1.5" style={{ color: '#9e9186' }}>
        <ClipboardList size={13} /> Set by your school
      </p>
      <div className="space-y-1.5">
        {items.map(a => {
          const st = assignmentStatus(a, done[a.id], todayIso);
          const s = STATUS_STYLE[st];
          return (
            <div key={a.id} className="flex items-center gap-3 rounded-xl border-2 border-[#d0cdc8] dark:border-zinc-700 px-3 py-2">
              <span className="flex-1 min-w-0">
                <span className="block text-[13.5px] font-semibold truncate" style={{ color: '#1a1a1a' }}>{a.title}</span>
                {a.dueIso && <span className="block text-[11px]" style={{ color: '#7a7068' }}>due {a.dueIso}</span>}
              </span>
              {st === 'done' ? (
                <span className="shrink-0 text-[11px] font-bold px-2 py-0.5 rounded-full inline-flex items-center gap-1" style={{ backgroundColor: s.bg, color: s.fg }}>
                  <Check size={12} /> {s.label}
                </span>
              ) : (
                <button onClick={() => complete(a.id)} className="shrink-0 text-[11.5px] font-semibold px-2.5 py-1 rounded-full border-2" style={{ borderColor: s.fg, color: s.fg }}>
                  Mark done
                </button>
              )}
            </div>
          );
        })}
      </div>
    </div>
  );
};

export default AssignedStrip;
