/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 *
 * Coursework Companion — how the SEC scheme actually marks the coursework,
 * project and practical components. Pick a subject → see each component: what
 * it is, the printed marking criteria with their marks, the grading table where
 * one is printed, and the filed SEC scheme every fact comes from.
 *
 * Data is the authored-but-strictly-cited corpus in data/courseworkCompanion —
 * every marks figure and criterion traces to a filed SEC marking scheme (the
 * integrity gate checks the filed document exists). Where a scheme prints no
 * component total or weighting, none is shown: the tool states only what the
 * scheme states.
 */

import React, { useMemo, useState } from 'react';
import { ArrowLeft, FolderCheck, ChevronDown } from 'lucide-react';
import SubjectTilePicker from '../shared/SubjectTilePicker';
import {
  courseworkSubjects,
  componentsForSubject,
  type CourseworkComponent,
} from '../../data/courseworkCompanion';

const INK = '#1a1a1a';
const ACCENT = '#F26B1F';
const ACCENT_TINT = '#FDEEDF';
const ACCENT_DARK_TEXT = '#8C3A0E';

interface Props {
  /** The student's subject NAMES (e.g. "Geography") — used to pre-scope "mine". */
  studentSubjects?: string[];
}

const ComponentCard: React.FC<{ component: CourseworkComponent }> = ({ component }) => {
  const [open, setOpen] = useState(false);
  return (
    <article className="rounded-2xl border-2 bg-white dark:bg-zinc-900 overflow-hidden" style={{ borderColor: '#d0cdc8' }}>
      <div className="p-4 sm:p-5">
        <div className="flex items-start justify-between gap-2 mb-1.5">
          <h3 className="text-[17px] font-semibold leading-snug" style={{ fontFamily: "'Source Serif 4', serif", color: INK }}>
            {component.name}
          </h3>
          {component.totalMarks !== null && (
            <span className="shrink-0 text-[12px] font-bold tabular-nums px-2.5 py-1 rounded-full" style={{ backgroundColor: ACCENT_TINT, color: ACCENT_DARK_TEXT }}>
              {component.totalMarks} marks
            </span>
          )}
        </div>
        <p className="text-[13px] leading-relaxed mb-2" style={{ color: '#5a5550' }}>{component.whatItIs}</p>

        <button
          onClick={() => setOpen(o => !o)}
          aria-expanded={open}
          className="inline-flex items-center gap-1 text-[12.5px] font-semibold"
          style={{ color: ACCENT }}
        >
          <ChevronDown size={14} className="transition-transform" style={{ transform: open ? 'rotate(180deg)' : 'none' }} />
          {open ? 'Hide the marking criteria' : `How it’s marked — ${component.criteria.length} criteria`}
        </button>

        {open && (
          <>
            <ul className="flex flex-col gap-2 mt-3">
              {component.criteria.map(cr => (
                <li key={cr.name} className="rounded-r-lg px-3.5 py-2.5" style={{ backgroundColor: ACCENT_TINT, borderLeft: `3px solid ${ACCENT}` }}>
                  <div className="flex items-start justify-between gap-2">
                    <span className="text-[13.5px] font-semibold" style={{ fontFamily: "'Source Serif 4', serif", color: INK }}>{cr.name}</span>
                    <span className="shrink-0 text-[12px] font-bold tabular-nums" style={{ fontFamily: "'Source Serif 4', serif", color: ACCENT }}>{cr.marks}m</span>
                  </div>
                  <p className="text-[12px] leading-relaxed mt-0.5" style={{ color: ACCENT_DARK_TEXT }}>{cr.whatItRewards}</p>
                </li>
              ))}
            </ul>

            {component.gradeBands && component.gradeBands.length > 0 && (
              <div className="mt-3">
                <p className="text-[10px] font-bold uppercase tracking-wide mb-1.5" style={{ color: '#9e9186' }}>Grading table (as printed)</p>
                <div className="flex flex-wrap gap-1.5">
                  {component.gradeBands.map(b => (
                    <span key={b.grade} className="text-[11px] font-semibold tabular-nums px-2 py-1 rounded-lg bg-white" style={{ border: '1.5px solid #d0cdc8', color: '#5a5550' }}>
                      Grade {b.grade}: {b.markBand}
                    </span>
                  ))}
                </div>
              </div>
            )}

            {component.structure && (
              <p className="text-[12px] italic leading-relaxed mt-3" style={{ color: '#7a7068' }}>{component.structure}</p>
            )}
          </>
        )}

        <p className="text-[10.5px] mt-3 pt-2" style={{ color: '#9e9186' }}>
          {component.source}
          {' · '}
          <a href={component.sourceUrl} target="_blank" rel="noreferrer" className="underline" style={{ color: '#9e9186' }}>
            SEC exam material archive
          </a>
        </p>
      </div>
    </article>
  );
};

const CourseworkCompanion: React.FC<Props> = ({ studentSubjects = [] }) => {
  const subjects = useMemo(() => courseworkSubjects(), []);
  const mineIds = useMemo(() => {
    const names = new Set(studentSubjects.map(s => s.trim().toLowerCase()));
    return subjects.filter(s => names.has(s.label.trim().toLowerCase())).map(s => s.id);
  }, [studentSubjects, subjects]);
  const [scope, setScope] = useState<'mine' | 'all'>('all');
  const [subjectId, setSubjectId] = useState<string | null>(null);

  const subjectLabel = (id: string) => subjects.find(s => s.id === id)?.label ?? id;
  const components = useMemo(() => (subjectId ? componentsForSubject(subjectId) : []), [subjectId]);

  // ── Level 1: one subject's coursework components ──
  if (subjectId) {
    return (
      <div className="w-full max-w-3xl mx-auto pb-12">
        <button onClick={() => setSubjectId(null)} className="flex items-center gap-1.5 text-[13px] font-medium mb-4" style={{ color: '#7a7068' }}>
          <ArrowLeft size={15} /> All subjects
        </button>
        <h2 className="text-2xl font-semibold mb-1" style={{ fontFamily: "'Source Serif 4', serif", color: INK }}>{subjectLabel(subjectId)}</h2>
        <p className="text-[13px] mb-4" style={{ color: '#7a7068' }}>
          {components.length} coursework component{components.length === 1 ? '' : 's'} — each marked exactly as the filed SEC scheme prints it.
        </p>
        <div className="flex flex-col gap-4">
          {components.map(c => <ComponentCard key={c.id} component={c} />)}
        </div>
      </div>
    );
  }

  // ── Level 0: subject picker ──
  return (
    <div className="w-full max-w-xl mx-auto pb-12">
      <h2 className="text-2xl font-semibold mb-1 flex items-center gap-2" style={{ fontFamily: "'Source Serif 4', serif", color: INK }}>
        <FolderCheck size={20} style={{ color: ACCENT }} /> Coursework Companion
      </h2>
      <p className="text-[13.5px] leading-relaxed mb-5" style={{ color: '#5a5550' }}>
        The coursework, project and practical components — what each one is and exactly how the SEC scheme marks it, criterion by criterion, straight from the filed marking scheme.
      </p>
      {subjects.length === 0 ? (
        <p className="text-[13.5px] rounded-2xl px-4 py-4" style={{ backgroundColor: '#E8EFF5', color: '#27506E' }}>
          Coursework components are being added subject by subject — check back soon.
        </p>
      ) : (
        <SubjectTilePicker
          headingLabel="Pick a subject"
          subjects={subjects.map(s => ({ id: s.id, label: s.label, sublabel: `${s.count} component${s.count === 1 ? '' : 's'}` }))}
          mineIds={mineIds}
          scope={scope}
          onScopeChange={setScope}
          onPick={setSubjectId}
        />
      )}
    </div>
  );
};

export default CourseworkCompanion;
