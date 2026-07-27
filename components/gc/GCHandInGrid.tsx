/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 *
 * Guidance-Counsellor practice RAG grid (feature E8). Sparx-style at-a-glance
 * triage: one row per student, a red/amber/green status chip, and the signals a
 * counsellor scans first — active this week, overall progress, streak. Filter by
 * a cohort tag (DEIS / At-risk / Priority) to focus support. Read-only over the
 * data the dashboard already loads; tags are the counsellor's local annotations.
 */

import React, { useMemo, useState, useEffect } from 'react';
import { type CourseData } from '../Library';
import { type GCStudentFullData, type StudentStatus } from './gcTypes';
import { getOverallProgress, isActiveThisWeek, getStudentStatus, getVisibleCourses } from './gcUtils';
import { COHORT_TAGS, getTags, toggleTag, loadCohortTags, type CohortTag } from './cohortTags';

type Rag = 'red' | 'amber' | 'green';
const RAG_OF: Record<StudentStatus, Rag> = {
  'at-risk': 'red',
  inactive: 'red',
  drifting: 'amber',
  new: 'amber',
  thriving: 'green',
  active: 'green',
};
const RAG_STYLE: Record<Rag, { bg: string; fg: string; dot: string }> = {
  red: { bg: '#FBEAE8', fg: '#8E2A20', dot: '#C0392B' },
  amber: { bg: '#FBF1E3', fg: '#8A5A11', dot: '#C77D0A' },
  green: { bg: '#E8F2EC', fg: '#1F5F3E', dot: '#3A8D5F' },
};

interface Props {
  students: GCStudentFullData[];
  allCourses: CourseData[];
  school: string;
  onSelectStudent: (uid: string) => void;
}

const GCHandInGrid: React.FC<Props> = ({ students, allCourses, school, onSelectStudent }) => {
  const [filter, setFilter] = useState<CohortTag | null>(null);
  const [ver, setVer] = useState(0); // re-read tags after load / a toggle

  // Cohort tags now live in Firestore (security review M-8). Hydrate the cache
  // once for this school, then bump `ver` so the rows re-read getTags().
  useEffect(() => {
    let cancelled = false;
    loadCohortTags(school).then(() => { if (!cancelled) setVer(v => v + 1); });
    return () => { cancelled = true; };
  }, [school]);

  const rows = useMemo(() => {
    void ver;
    return students
      .map(s => {
        // Score against the modules this student can actually open — every
        // other GC surface does, and using the full catalogue here made the
        // Practice grid contradict the overview table for the same student.
        const visible = getVisibleCourses(s, allCourses);
        const status = getStudentStatus(s, visible);
        return {
          uid: s.user.uid,
          name: s.user.name || 'Student',
          status,
          rag: RAG_OF[status],
          active: isActiveThisWeek(s),
          progress: Math.round(getOverallProgress(s.progress, visible)),
          streak: s.streak?.currentStreak ?? 0,
          tags: getTags(school, s.user.uid),
        };
      })
      .sort((a, b) => {
        const order: Record<Rag, number> = { red: 0, amber: 1, green: 2 };
        return order[a.rag] - order[b.rag] || a.name.localeCompare(b.name);
      });
  }, [students, allCourses, school, ver]);

  const shown = filter ? rows.filter(r => r.tags.includes(filter)) : rows;
  const tagCount = (t: CohortTag) => rows.filter(r => r.tags.includes(t)).length;
  const ragCount = (rag: Rag) => shown.filter(r => r.rag === rag).length;

  return (
    <div className="p-6 max-w-5xl mx-auto w-full">
      <h1 className="text-xl font-semibold text-zinc-900 dark:text-zinc-100 mb-1">Practice status</h1>
      <p className="text-sm text-zinc-500 dark:text-zinc-400 mb-4">
        At-a-glance triage — who’s engaging and who needs a nudge. {ragCount('red')} need attention, {ragCount('amber')} drifting, {ragCount('green')} on track.
      </p>

      {/* Cohort filter */}
      <div className="flex flex-wrap items-center gap-2 mb-4">
        <button
          onClick={() => setFilter(null)}
          className={`px-3 py-1.5 rounded-full text-xs font-medium border transition-colors ${filter === null ? 'bg-zinc-900 text-white border-zinc-900 dark:bg-zinc-100 dark:text-zinc-900' : 'bg-white dark:bg-zinc-900 text-zinc-600 dark:text-zinc-300 border-zinc-200 dark:border-zinc-700'}`}
        >
          All {rows.length}
        </button>
        {COHORT_TAGS.map(t => (
          <button
            key={t}
            onClick={() => setFilter(filter === t ? null : t)}
            className={`px-3 py-1.5 rounded-full text-xs font-medium border transition-colors ${filter === t ? 'bg-zinc-900 text-white border-zinc-900 dark:bg-zinc-100 dark:text-zinc-900' : 'bg-white dark:bg-zinc-900 text-zinc-600 dark:text-zinc-300 border-zinc-200 dark:border-zinc-700'}`}
          >
            {t} {tagCount(t)}
          </button>
        ))}
      </div>

      <div className="overflow-x-auto rounded-xl border border-zinc-200 dark:border-zinc-800">
        <table className="w-full text-sm bg-white dark:bg-zinc-900 min-w-[640px]">
          <thead>
            <tr className="text-left text-[11px] uppercase tracking-wide text-zinc-400 border-b border-zinc-200 dark:border-zinc-800">
              <th className="px-4 py-2.5 font-semibold">Student</th>
              <th className="px-3 py-2.5 font-semibold">Status</th>
              <th className="px-3 py-2.5 font-semibold">This week</th>
              <th className="px-3 py-2.5 font-semibold text-right">Progress</th>
              <th className="px-3 py-2.5 font-semibold text-right">Streak</th>
              <th className="px-3 py-2.5 font-semibold">Cohort</th>
            </tr>
          </thead>
          <tbody>
            {shown.length === 0 ? (
              <tr><td colSpan={6} className="px-4 py-6 text-center text-zinc-400">No students{filter ? ` tagged ${filter}` : ''} yet.</td></tr>
            ) : shown.map(r => {
              const rs = RAG_STYLE[r.rag];
              return (
                <tr key={r.uid} className="border-b border-zinc-100 dark:border-zinc-800/60 last:border-0 hover:bg-zinc-50 dark:hover:bg-zinc-800/40">
                  <td className="px-4 py-2.5">
                    <button onClick={() => onSelectStudent(r.uid)} className="font-medium text-zinc-800 dark:text-zinc-100 hover:underline text-left">{r.name}</button>
                  </td>
                  <td className="px-3 py-2.5">
                    <span className="inline-flex items-center gap-1.5 px-2 py-0.5 rounded-full text-[11px] font-semibold" style={{ backgroundColor: rs.bg, color: rs.fg }}>
                      <span className="w-1.5 h-1.5 rounded-full" style={{ backgroundColor: rs.dot }} />
                      {r.status}
                    </span>
                  </td>
                  <td className="px-3 py-2.5">
                    <span className="text-[13px]" style={{ color: r.active ? '#3A8D5F' : '#b0a898' }}>{r.active ? 'active' : '—'}</span>
                  </td>
                  <td className="px-3 py-2.5 text-right tabular-nums text-zinc-700 dark:text-zinc-300">{r.progress}%</td>
                  <td className="px-3 py-2.5 text-right tabular-nums text-zinc-700 dark:text-zinc-300">{r.streak}</td>
                  <td className="px-3 py-2.5">
                    <div className="flex flex-wrap gap-1">
                      {COHORT_TAGS.map(t => {
                        const on = r.tags.includes(t);
                        return (
                          <button
                            key={t}
                            onClick={() => { toggleTag(school, r.uid, t); setVer(v => v + 1); }}
                            aria-pressed={on}
                            title={`${on ? 'Remove' : 'Add'} ${t}`}
                            className={`px-1.5 py-0.5 rounded text-[10px] font-semibold border transition-colors ${on ? 'bg-zinc-900 text-white border-zinc-900 dark:bg-zinc-100 dark:text-zinc-900' : 'bg-white dark:bg-zinc-900 text-zinc-400 border-zinc-200 dark:border-zinc-700 hover:text-zinc-600'}`}
                          >
                            {t === 'At-risk' ? 'AR' : t === 'Priority' ? 'Pri' : t}
                          </button>
                        );
                      })}
                    </div>
                  </td>
                </tr>
              );
            })}
          </tbody>
        </table>
      </div>
      <p className="text-[11px] text-zinc-400 mt-3">Cohort tags are your private annotations, stored on this device. Status is derived from each student’s recent activity and progress.</p>
    </div>
  );
};

export default GCHandInGrid;
