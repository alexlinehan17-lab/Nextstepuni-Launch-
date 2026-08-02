/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 *
 * Diagram Vault — browse the real diagrams, graphs, maps and charts that appear
 * in SEC exams, by subject. A two-level navigator mirroring the Topic Vault:
 * pick a subject → see every verified exam figure for it, each with its decoded
 * description and its exam source. Data is the read-only projection in
 * data/diagramVault (derived from the verified figure exhibits), so every tile
 * shows a real, attributable figure — never a generated or unmoored image.
 */

import React, { useMemo, useState } from 'react';
import { ArrowLeft, Image as ImageIcon, ChevronDown } from 'lucide-react';
import SubjectTilePicker from '../shared/SubjectTilePicker';
import {
  diagramSubjects,
  diagramsForSubject,
  topicsForSubjectDiagrams,
  type DiagramEntry,
} from '../../data/diagramVault';
import { figureUrl } from '../../utils/figureUrl';

const INK = '#1a1a1a';
const ACCENT = '#F26B1F';
const LVL: Record<string, string> = { higher: 'HL', ordinary: 'OL', foundation: 'FL', common: 'CL' };

interface Props {
  /** The student's subject NAMES (e.g. "Biology") — used to pre-scope "mine". */
  studentSubjects?: string[];
}

/** A short, human title for a figure, derived from its slug id (subject / year /
 *  level tokens stripped). Falls back to the topic label. */
const titleFor = (e: DiagramEntry): string => {
  const slug = e.id
    .replace(/^[a-z-]*?-(?=\d{4}|hl|ol|fl|cl|am|jc)/i, '') // drop leading subject prefix
    .replace(/\b(19|20)\d{2}\b/g, '')
    .replace(/\b(hl|ol|fl|cl)\b/gi, '')
    .replace(/^(am|jc)-/i, '')
    .replace(/-/g, ' ')
    .replace(/\s+/g, ' ')
    .trim();
  const cleaned = slug.length >= 3 ? slug : '';
  if (cleaned) return cleaned.replace(/\b\w/g, c => c.toUpperCase());
  return e.topicLabel ?? e.questionRef ?? 'Exam figure';
};

const DiagramTile: React.FC<{ entry: DiagramEntry }> = ({ entry }) => {
  const [open, setOpen] = useState(false);
  const meta = [entry.level ? (LVL[entry.level] ?? entry.level) : null, entry.year ? String(entry.year) : null]
    .filter(Boolean)
    .join(' · ');
  return (
    // Cards stay white in dark mode (design system: all cards white) — the
    // inline ink text depends on it.
    <figure className="rounded-2xl border-2 border-[#d0cdc8] bg-white overflow-hidden flex flex-col">
      <div className="bg-[#f7f6f4] border-b border-[#e6e2dc] p-3 flex items-center justify-center">
        <img
          src={figureUrl(entry.src)}
          alt={entry.alt}
          loading="lazy"
          className="max-h-72 w-auto max-w-full object-contain"
        />
      </div>
      <figcaption className="p-3.5 flex flex-col gap-2 flex-1">
        <div className="flex items-start justify-between gap-2">
          <h3 className="text-[15px] font-semibold leading-snug" style={{ fontFamily: "'Source Serif 4', serif", color: INK }}>
            {titleFor(entry)}
          </h3>
          {meta && (
            <span className="shrink-0 text-[10.5px] font-bold tabular-nums px-1.5 py-0.5 rounded-full" style={{ backgroundColor: '#f0ede8', color: '#7a7068' }}>
              {meta}
            </span>
          )}
        </div>
        {(entry.topicLabel || entry.questionRef) && (
          <span className="text-[11px] font-semibold uppercase tracking-wide" style={{ color: '#8C3A0E' }}>
            {entry.topicLabel ?? entry.questionRef}
          </span>
        )}
        <button
          onClick={() => setOpen(o => !o)}
          aria-expanded={open}
          className="inline-flex items-center gap-1 text-[12.5px] font-semibold w-fit"
          style={{ color: ACCENT }}
        >
          <ChevronDown size={14} className="transition-transform" style={{ transform: open ? 'rotate(180deg)' : 'none' }} />
          {open ? 'Hide description' : 'What this diagram shows'}
        </button>
        {open && (
          <p className="text-[12.5px] leading-relaxed rounded-lg px-3 py-2" style={{ backgroundColor: '#FDEEDF', color: '#5a5550' }}>
            {entry.alt}
          </p>
        )}
        <p className="text-[10.5px] mt-auto pt-1" style={{ color: '#9e9186' }}>{entry.source}</p>
      </figcaption>
    </figure>
  );
};

const DiagramVault: React.FC<Props> = ({ studentSubjects = [] }) => {
  const subjects = useMemo(() => diagramSubjects(), []);
  // Match the student's subject NAMES to diagram subject ids, so the picker can
  // pre-filter to "my subjects" (falls back to all when nothing matches).
  const mineIds = useMemo(() => {
    const names = new Set(studentSubjects.map(s => s.trim().toLowerCase()));
    return subjects.filter(s => names.has(s.label.trim().toLowerCase())).map(s => s.id);
  }, [studentSubjects, subjects]);
  const [scope, setScope] = useState<'mine' | 'all'>('all');
  const [subjectId, setSubjectId] = useState<string | null>(null);
  const [topicFilter, setTopicFilter] = useState<'all' | string>('all');

  const subjectLabel = (id: string) => subjects.find(s => s.id === id)?.label ?? id;
  const entries = useMemo(() => (subjectId ? diagramsForSubject(subjectId) : []), [subjectId]);
  const topicChips = useMemo(() => (subjectId ? topicsForSubjectDiagrams(subjectId) : []), [subjectId]);
  const shown = useMemo(
    () => (topicFilter === 'all' ? entries : entries.filter(e => e.topicLabel === topicFilter)),
    [entries, topicFilter],
  );

  // ── Level 1: one subject's diagrams ──
  if (subjectId) {
    return (
      <div className="w-full max-w-3xl mx-auto pb-12">
        <button onClick={() => { setSubjectId(null); setTopicFilter('all'); }} className="flex items-center gap-1.5 text-[13px] font-medium mb-4" style={{ color: '#7a7068' }}>
          <ArrowLeft size={15} /> All subjects
        </button>
        <h2 className="text-2xl font-semibold mb-1 text-[#1a1a1a] dark:text-zinc-100" style={{ fontFamily: "'Source Serif 4', serif" }}>{subjectLabel(subjectId)}</h2>
        <p className="text-[13px] mb-4 text-[#7a7068] dark:text-zinc-400">
          {entries.length} exam figure{entries.length === 1 ? '' : 's'} — each cropped from a real paper, with its decoded description and exam source.
        </p>
        {topicChips.length > 1 && (
          <div className="flex items-center gap-1.5 overflow-x-auto pb-2 mb-4 -mx-1 px-1" role="group" aria-label="Filter by topic">
            {(['all', ...topicChips] as const).map(t => (
              <button
                key={t}
                aria-pressed={topicFilter === t}
                onClick={() => setTopicFilter(t)}
                className={`shrink-0 px-3 py-1 rounded-full text-[12px] font-semibold border-2 transition-colors ${topicFilter === t ? '' : 'bg-white'}`}
                style={topicFilter === t
                  ? { backgroundColor: ACCENT, borderColor: ACCENT, color: '#fff' }
                  : { borderColor: '#d0cdc8', color: '#7a7068' }}
              >
                {t === 'all' ? 'All topics' : t}
              </button>
            ))}
          </div>
        )}
        <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
          {shown.map(e => <DiagramTile key={e.id} entry={e} />)}
        </div>
      </div>
    );
  }

  // ── Level 0: subject picker (tool exit is handled by the zone's ToolHeader) ──
  return (
    <div className="w-full max-w-xl mx-auto pb-12">
      <h2 className="text-2xl font-semibold mb-1 flex items-center gap-2 text-[#1a1a1a] dark:text-zinc-100" style={{ fontFamily: "'Source Serif 4', serif" }}>
        <ImageIcon size={20} style={{ color: ACCENT }} /> Diagram Vault
      </h2>
      <p className="text-[13.5px] leading-relaxed mb-5 text-[#5a5550] dark:text-zinc-400">
        Every diagram, graph, map and chart that has come up in the exams — cropped straight from the paper and decoded. The one you have to draw or read for the marks, shown to you first.
      </p>
      {subjects.length === 0 ? (
        <p className="text-[13.5px] rounded-2xl px-4 py-4" style={{ backgroundColor: '#E8EFF5', color: '#27506E' }}>
          Exam diagrams are being added subject by subject — check back soon.
        </p>
      ) : (
        <SubjectTilePicker
          headingLabel="Pick a subject"
          subjects={subjects.map(s => ({ id: s.id, label: s.label, sublabel: `${s.count} figure${s.count === 1 ? '' : 's'}` }))}
          mineIds={mineIds}
          scope={scope}
          onScopeChange={setScope}
          onPick={setSubjectId}
        />
      )}
    </div>
  );
};

export default DiagramVault;
