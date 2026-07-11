/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 *
 * Answer Architect — the mark-earning SKELETON of a top answer, by subject. A
 * two-level navigator mirroring Diagram Vault: pick a subject → see every real
 * exam question's answer built as an ordered sequence of mark-earning beats, with
 * the shape of the answer up top and its SEC source underneath.
 *
 * Where Marking Lens shows "where the marks went" beside one paper's crop, this
 * re-lenses the same verified spine into "the beats a full-marks answer hits, in
 * order." Data is the read-only projection in data/answerArchitect (derived from
 * the filed-scheme Marking Lens corpus), so every beat is real and attributable —
 * never a model answer or an invented mark.
 */

import React, { useMemo, useState } from 'react';
import { ArrowLeft, ListChecks, ChevronDown, AlertTriangle } from 'lucide-react';
import SubjectTilePicker from '../shared/SubjectTilePicker';
import {
  architectSubjects,
  skeletonsForSubject,
  levelLabel,
  type AnswerSkeleton,
} from '../../data/answerArchitect';

const INK = '#1a1a1a';
const ACCENT = '#F26B1F';
const ACCENT_TINT = '#FDEEDF';
const ACCENT_DARK_TEXT = '#8C3A0E';

interface Props {
  /** The student's subject NAMES (e.g. "Biology") — used to pre-scope "mine". */
  studentSubjects?: string[];
}

/** One numbered beat row — the ConceptCardGrid vocabulary (accent number badge,
 *  serif term, body description) with the beat's marks as a weight badge. */
const BeatRow: React.FC<{ beat: AnswerSkeleton['beats'][number] }> = ({ beat }) => (
  <li className="flex gap-3 rounded-2xl border-2 p-4" style={{ borderColor: INK, backgroundColor: '#fff' }}>
    <span
      className="shrink-0 grid place-items-center rounded-full text-white font-bold"
      style={{ width: 32, height: 32, backgroundColor: ACCENT, fontFamily: "'Source Serif 4', serif", fontSize: 14 }}
      aria-hidden="true"
    >
      {beat.order}
    </span>
    <div className="flex-1 min-w-0">
      <div className="flex items-start justify-between gap-2">
        <h4 className="text-[15px] font-semibold leading-snug" style={{ fontFamily: "'Source Serif 4', serif", color: INK }}>
          {beat.part && <span style={{ color: ACCENT_DARK_TEXT }}>{beat.part} </span>}
          {beat.requirement}
        </h4>
        <span
          className="shrink-0 text-[11px] font-bold tabular-nums px-2 py-0.5 rounded-full"
          style={{ backgroundColor: '#f0ede8', color: '#7a7068' }}
        >
          {beat.marks}m
        </span>
      </div>
      <p className="text-[12.5px] leading-relaxed mt-1" style={{ color: '#5a5550' }}>{beat.earns}</p>
    </div>
  </li>
);

const SkeletonCard: React.FC<{ skeleton: AnswerSkeleton }> = ({ skeleton }) => {
  const [open, setOpen] = useState(false);
  const meta = `${levelLabel(skeleton.level)} · ${skeleton.year}`;
  return (
    // Cards stay white in dark mode (design system: all cards white) — the
    // inline ink text depends on it.
    <article className="rounded-2xl border-2 bg-white overflow-hidden" style={{ borderColor: '#d0cdc8' }}>
      <div className="p-4 sm:p-5">
        <div className="flex items-start justify-between gap-2 mb-2">
          <div>
            <h3 className="text-[17px] font-semibold leading-snug" style={{ fontFamily: "'Source Serif 4', serif", color: INK }}>
              {skeleton.questionRef}
            </h3>
            <span className="text-[11px] font-bold uppercase tracking-wide" style={{ color: '#9e9186' }}>{meta}</span>
          </div>
          <span
            className="shrink-0 text-[12px] font-bold tabular-nums px-2.5 py-1 rounded-full"
            style={{ backgroundColor: ACCENT_TINT, color: ACCENT_DARK_TEXT }}
          >
            {skeleton.totalMarks} marks
          </span>
        </div>

        {/* The shape of the answer — accent callout. */}
        <p
          className="text-[13.5px] italic leading-relaxed rounded-r-lg px-4 py-2.5 mb-1"
          style={{ backgroundColor: ACCENT_TINT, borderLeft: `3px solid ${ACCENT}`, color: ACCENT_DARK_TEXT }}
        >
          {skeleton.structure}
        </p>

        <button
          onClick={() => setOpen(o => !o)}
          aria-expanded={open}
          className="inline-flex items-center gap-1 text-[12.5px] font-semibold mt-2"
          style={{ color: ACCENT }}
        >
          <ChevronDown size={14} className="transition-transform" style={{ transform: open ? 'rotate(180deg)' : 'none' }} />
          {open ? 'Hide the skeleton' : `Build the answer — ${skeleton.beats.length} beats`}
        </button>

        {open && (
          <>
            <ol className="flex flex-col gap-2.5 mt-3">
              {skeleton.beats.map(b => <BeatRow key={b.order} beat={b} />)}
            </ol>

            {skeleton.pitfall && (
              <div
                className="flex gap-2.5 rounded-r-lg px-4 py-3 mt-3"
                style={{ backgroundColor: ACCENT_TINT, borderLeft: `3px solid ${ACCENT}` }}
              >
                <AlertTriangle size={16} className="shrink-0 mt-0.5" style={{ color: ACCENT }} aria-hidden="true" />
                <div>
                  <p className="text-[12.5px] italic leading-relaxed" style={{ color: ACCENT_DARK_TEXT }}>
                    {skeleton.pitfall.text}
                  </p>
                  <p className="text-[10.5px] mt-1" style={{ color: '#9e9186' }}>{skeleton.pitfall.cite}</p>
                </div>
              </div>
            )}
          </>
        )}

        <p className="text-[10.5px] mt-3 pt-2" style={{ color: '#9e9186' }}>{skeleton.source}</p>
      </div>
    </article>
  );
};

const AnswerArchitect: React.FC<Props> = ({ studentSubjects = [] }) => {
  const subjects = useMemo(() => architectSubjects(), []);
  const mineIds = useMemo(() => {
    const names = new Set(studentSubjects.map(s => s.trim().toLowerCase()));
    return subjects.filter(s => names.has(s.label.trim().toLowerCase())).map(s => s.id);
  }, [studentSubjects, subjects]);
  const [scope, setScope] = useState<'mine' | 'all'>('all');
  const [subjectId, setSubjectId] = useState<string | null>(null);

  const subjectLabel = (id: string) => subjects.find(s => s.id === id)?.label ?? id;
  const skeletons = useMemo(() => (subjectId ? skeletonsForSubject(subjectId) : []), [subjectId]);

  // ── Level 1: one subject's answer skeletons ──
  if (subjectId) {
    return (
      <div className="w-full max-w-3xl mx-auto pb-12">
        <button onClick={() => setSubjectId(null)} className="flex items-center gap-1.5 text-[13px] font-medium mb-4" style={{ color: '#7a7068' }}>
          <ArrowLeft size={15} /> All subjects
        </button>
        <h2 className="text-2xl font-semibold mb-1 text-[#1a1a1a] dark:text-zinc-100" style={{ fontFamily: "'Source Serif 4', serif" }}>{subjectLabel(subjectId)}</h2>
        <p className="text-[13px] mb-4 text-[#7a7068] dark:text-zinc-400">
          {skeletons.length} answer skeleton{skeletons.length === 1 ? '' : 's'} — each a real exam question, built as the ordered beats the SEC scheme awards marks for.
        </p>
        <div className="flex flex-col gap-4">
          {skeletons.map(s => <SkeletonCard key={s.id} skeleton={s} />)}
        </div>
      </div>
    );
  }

  // ── Level 0: subject picker (tool exit handled by the zone's ToolHeader) ──
  return (
    <div className="w-full max-w-xl mx-auto pb-12">
      <h2 className="text-2xl font-semibold mb-1 flex items-center gap-2 text-[#1a1a1a] dark:text-zinc-100" style={{ fontFamily: "'Source Serif 4', serif" }}>
        <ListChecks size={20} style={{ color: ACCENT }} /> Answer Architect
      </h2>
      <p className="text-[13.5px] leading-relaxed mb-5 text-[#5a5550] dark:text-zinc-400">
        The mark-earning skeleton of a top answer. For real exam questions, see the shape of a full-marks answer and every beat it is built from — in order, with the marks the SEC scheme awards each one.
      </p>
      {subjects.length === 0 ? (
        <p className="text-[13.5px] rounded-2xl px-4 py-4" style={{ backgroundColor: '#E8EFF5', color: '#27506E' }}>
          Answer skeletons are being added subject by subject — check back soon.
        </p>
      ) : (
        <SubjectTilePicker
          headingLabel="Pick a subject"
          subjects={subjects.map(s => ({ id: s.id, label: s.label, sublabel: `${s.count} skeleton${s.count === 1 ? '' : 's'}` }))}
          mineIds={mineIds}
          scope={scope}
          onScopeChange={setScope}
          onPick={setSubjectId}
        />
      )}
    </div>
  );
};

export default AnswerArchitect;
