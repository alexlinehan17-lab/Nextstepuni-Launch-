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
import { Flame, MoreHorizontal } from 'lucide-react';
import { Button } from '../ui/Button';
import { MenuCheckRows, MenuLabel, MenuPanel } from '../ui/Menu';
import { useWide, StatusWords, StatusDot, STATUS_WORDS, Pct, StudentArt } from './gcView';

type Rag = 'red' | 'amber' | 'green';
const RAG_OF: Record<StudentStatus, Rag> = {
  'at-risk': 'red',
  inactive: 'red',
  drifting: 'amber',
  new: 'amber',
  thriving: 'green',
  active: 'green',
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
  const wide = useWide();

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
          avatar: s.user.avatar,
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

  const toggle = (uid: string, t: CohortTag) => { toggleTag(school, uid, t); setVer(v => v + 1); };
  const empty = <p className="gc8-empty">No students{filter ? ` tagged ${filter}` : ''} yet.</p>;
  const streak = (n: number) => (n > 0
    ? <span className="gc8-streak"><Flame className="ui-icon" width={16} height={16} strokeWidth={2} aria-hidden="true" />{n}</span>
    : <span className="gc8-dim">{n}</span>);

  return (
    <>
      <section className="gc8-head" aria-labelledby="gc8-practice">
        <h1 id="gc8-practice" className={wide ? 'gc8-title' : 'gc8-name'}>Practice status</h1>
        <p className="gc8-sub">
          At-a-glance triage: who’s engaging and who needs a nudge. {ragCount('red')} need attention, {ragCount('amber')} drifting, {ragCount('green')} on track.
        </p>
      </section>

      {/* Cohort filter */}
      <div className="gc8-filts" role="group" aria-label="Cohort tag">
        <Button size="sm" aria-pressed={filter === null} onClick={() => setFilter(null)}>All <span className="gc8-count">{rows.length}</span></Button>
        {COHORT_TAGS.map(t => (
          <Button key={t} size="sm" aria-pressed={filter === t} onClick={() => setFilter(filter === t ? null : t)}>
            {t} <span className="gc8-count">{tagCount(t)}</span>
          </Button>
        ))}
      </div>

      {wide ? (
        <section className="gc8-sec">
          <div className="gc8-ptablewrap">
            <div className="gc8-ptable" role="table" aria-label="Practice status">
              <div className="gc8-ptr gc8-ptr--head" role="row">
                <span role="columnheader" className="gc8-label">Student</span>
                <span role="columnheader" className="gc8-label">Status</span>
                <span role="columnheader" className="gc8-label">This week</span>
                <span role="columnheader" className="gc8-label gc8-n gc8-hpct">Progress</span>
                <span role="columnheader" className="gc8-label gc8-n">Streak</span>
                <span role="columnheader" className="gc8-label">Cohort</span>
              </div>
              {shown.map(r => (
                <div key={r.uid} className="gc8-ptr" role="row">
                  <span role="cell">
                    <button type="button" className="ui-part gc8-stu" onClick={() => onSelectStudent(r.uid)}>
                      <StudentArt seed={r.avatar} size={32} /><span>{r.name}</span>
                    </button>
                  </span>
                  <span role="cell"><StatusDot status={r.status} />{STATUS_WORDS[r.status]}</span>
                  <span role="cell">{r.active ? 'Active' : <span className="gc8-dim">–</span>}</span>
                  <span role="cell" className="gc8-n"><Pct value={r.progress} /></span>
                  <span role="cell" className="gc8-n">{streak(r.streak)}</span>
                  <span role="cell" className="gc8-tags">
                    {COHORT_TAGS.map(t => {
                      const on = r.tags.includes(t);
                      return (
                        <Button key={t} size="sm" className="gc8-tag" aria-pressed={on} title={`${on ? 'Remove' : 'Add'} ${t}`} onClick={() => toggle(r.uid, t)}>{t}</Button>
                      );
                    })}
                  </span>
                </div>
              ))}
            </div>
          </div>
          {shown.length === 0 && empty}
        </section>
      ) : (
        <section className="gc8-sec" aria-label="Practice status">
          <div>
            <div className="gc8-pr gc8-pr--head">
              <span className="gc8-label">Student</span>
              <span className="gc8-label gc8-n gc8-hpct">Progress</span>
              <span className="gc8-label gc8-n">Streak</span>
              <span />
            </div>
            {shown.map(r => (
              <div key={r.uid} className="gc8-pr">
                <button type="button" className="ui-part gc8-pwho" onClick={() => onSelectStudent(r.uid)}>
                  <StudentArt seed={r.avatar} />
                  <span className="gc8-pwho-copy">
                    <span className="gc8-person">{r.name}</span>
                    <span className="gc8-meta"><StatusWords status={r.status}>{r.tags.length ? ` · ${r.tags.join(', ')}` : ''}</StatusWords></span>
                  </span>
                </button>
                <Pct value={r.progress} />
                <span className="gc8-n">{streak(r.streak)}</span>
                <MenuPanel
                  label={`Cohort tags for ${r.name}`}
                  buttonLabel={`Cohort tags for ${r.name}`}
                  buttonClassName="gc8-acts"
                  className="gc8-rowmenu"
                  chevron={false}
                  face={<MoreHorizontal className="ui-icon" width={20} height={20} strokeWidth={1.75} aria-hidden="true" />}
                >
                  <MenuLabel>Cohort tags · private to you</MenuLabel>
                  <MenuCheckRows<CohortTag>
                    label={`Cohort tags for ${r.name}`}
                    options={COHORT_TAGS.map(t => ({ value: t, label: t }))}
                    values={r.tags as readonly CohortTag[]}
                    onToggle={t => toggle(r.uid, t)}
                  />
                </MenuPanel>
              </div>
            ))}
          </div>
          {shown.length === 0 && empty}
        </section>
      )}
      <p className="gc8-note">Cohort tags are your private annotations, stored on this device. Status is derived from each student’s recent activity and progress.</p>
    </>
  );
};

export default GCHandInGrid;
