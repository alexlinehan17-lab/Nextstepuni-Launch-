/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 *
 * Paper Trail — custom mock-set builder (feature B1). Assemble a practice set
 * from real past questions: pick a subject, go mixed or choose topics, pick a
 * length, and get a shuffled set that persists while you work through it (so it
 * survives opening each paper). Tick questions off, export the set as a sheet,
 * or clear it. Self-marking each question happens in the viewer as usual.
 */

import React, { useEffect, useMemo, useState } from 'react';
import { ArrowLeft, ChevronRight, Download, FileStack, RefreshCw, Check, Clock3 } from 'lucide-react';
import SubjectTilePicker from '../shared/SubjectTilePicker';
import { questionsForTopics, topicsForSubject, type SubjectTopic, type TopicSibling } from './topics';
import { buildSet, clearSet, loadSet, saveSet, toggleDone, type MockSet } from './mockSetStore';
import { downloadPack } from './revisionPack';

const INK = '#1a1a1a';
const ACCENT = '#F26B1F';
const SUCCESS = '#3A8D5F';
const LVL: Record<string, string> = { higher: 'HL', ordinary: 'OL', foundation: 'FL', common: 'CL' };
const paperAbbr = (k: string) => (k === 'p1' ? 'P1' : k === 'p2' ? 'P2' : '');
const LENGTHS = [5, 10, 15];
const fmtMin = (m: number) => (m >= 60 ? `${Math.floor(m / 60)}h ${m % 60}m` : `${m}m`);

interface Props {
  uid?: string;
  now: number;
  subjects: { id: string; label: string }[];
  mineIds: string[];
  subjectLabel: (id: string) => string;
  onOpenQuestion: (t: TopicSibling) => void;
  onBack: () => void;
}

const MockExamBuilder: React.FC<Props> = ({ uid, now, subjects, mineIds, subjectLabel, onOpenQuestion, onBack }) => {
  const [set, setSet] = useState<MockSet | null>(() => loadSet(uid));
  // Builder form state (only used when there's no active set).
  const [scope, setScope] = useState<'mine' | 'all'>(mineIds.length ? 'mine' : 'all');
  const [subjectId, setSubjectId] = useState<string | null>(null);
  const [mode, setMode] = useState<'mixed' | 'topics'>('mixed');
  const [chosen, setChosen] = useState<Set<string>>(new Set());
  const [count, setCount] = useState(10);
  const [tick, setTick] = useState(0);

  // Live-ish elapsed clock while a set is active.
  useEffect(() => {
    if (!set) return;
    const id = setInterval(() => setTick(t => t + 1), 1000);
    return () => clearInterval(id);
  }, [set]);

  const topics: SubjectTopic[] = useMemo(() => (subjectId ? topicsForSubject(subjectId) : []), [subjectId]);
  const pool = useMemo(
    () => (subjectId ? questionsForTopics(subjectId, mode === 'topics' ? [...chosen] : null) : []),
    [subjectId, mode, chosen],
  );

  const build = () => {
    if (!subjectId || pool.length === 0) return;
    const picked = buildSet(pool, count, now + pool.length);
    const label = `${subjectLabel(subjectId)} · ${mode === 'topics' && chosen.size ? `${chosen.size} topic${chosen.size === 1 ? '' : 's'}` : 'Mixed'}`;
    const s: MockSet = {
      subjectId,
      label,
      createdTs: now,
      targetMin: Math.round((picked.length * 8) / 5) * 5,
      items: picked.map(q => ({ q, done: false })),
    };
    saveSet(uid, s);
    setSet(s);
  };

  const toggleTopic = (id: string) =>
    setChosen(prev => {
      const next = new Set(prev);
      if (next.has(id)) next.delete(id);
      else next.add(id);
      return next;
    });

  const header = (label: string, onClick: () => void) => (
    <button onClick={onClick} className="flex items-center gap-1.5 text-[13px] font-medium mb-4" style={{ color: '#7a7068' }}>
      <ArrowLeft size={15} /> {label}
    </button>
  );

  // ═══════════ RUN: an active set ═══════════
  if (set) {
    void tick;
    const doneCount = set.items.filter(i => i.done).length;
    const elapsedMin = Math.max(0, Math.floor((now + tick * 1000 - set.createdTs) / 60000));
    const packOpts = {
      subjectLabel: subjectLabel(set.subjectId),
      topicLabel: set.label.replace(`${subjectLabel(set.subjectId)} · `, '') + ' — mock set',
      questions: set.items.map(i => i.q),
      dateIso: new Date(set.createdTs).toISOString().slice(0, 10),
    };
    const onToggle = (i: number) => setSet(toggleDone(uid, i));
    const finish = () => { clearSet(uid); setSet(null); setSubjectId(null); };

    return (
      <div className="w-full max-w-xl mx-auto pb-12">
        {header('Paper Trail', onBack)}
        <h2 className="text-2xl font-semibold mb-1" style={{ fontFamily: "'Source Serif 4', serif", color: INK }}>{set.label}</h2>
        <div className="flex items-center gap-3 text-[12.5px] mb-3" style={{ color: '#7a7068' }}>
          <span>{set.items.length} questions</span>
          <span className="flex items-center gap-1"><Clock3 size={13} /> {elapsedMin}m elapsed · target ~{fmtMin(set.targetMin)}</span>
        </div>
        <div className="h-1.5 rounded-full mb-4 overflow-hidden" style={{ backgroundColor: '#e0dbd4' }}>
          <div className="h-full rounded-full transition-all" style={{ width: `${(doneCount / set.items.length) * 100}%`, backgroundColor: doneCount === set.items.length ? SUCCESS : ACCENT }} />
        </div>

        <div className="space-y-1.5 mb-5">
          {set.items.map((it, i) => (
            <div key={`${it.q.year}-${it.q.level}-${it.q.lang}-${it.q.fileid}-${it.q.n}`} className="flex items-center gap-2 rounded-xl border-2 border-[#1a1a1a] dark:border-zinc-700 bg-white dark:bg-zinc-900 pr-2">
              <button
                onClick={() => onToggle(i)}
                aria-pressed={it.done}
                aria-label={it.done ? 'Mark not done' : 'Mark done'}
                className="shrink-0 ml-2 w-7 h-7 rounded-lg flex items-center justify-center border-2 transition-colors"
                style={it.done ? { backgroundColor: '#E8F2EC', borderColor: SUCCESS, color: '#1F5F3E' } : { backgroundColor: '#fff', borderColor: '#d0cdc8', color: '#d0cdc8' }}
              >
                {it.done && <Check size={15} />}
              </button>
              <button onClick={() => onOpenQuestion(it.q)} className="flex-1 flex items-center gap-2.5 py-2.5 pl-1 text-left transition-transform active:translate-y-0.5">
                <span className="shrink-0 w-6 text-[13px] font-bold tabular-nums" style={{ color: '#9e9186', fontFamily: "'Source Serif 4', serif" }}>{i + 1}</span>
                <span className="flex-1 text-[12.5px]" style={{ color: it.done ? '#9e9186' : '#5a5550', textDecoration: it.done ? 'line-through' : 'none' }}>
                  {it.q.year} · {LVL[it.q.level] ?? it.q.level}{paperAbbr(it.q.paperKey) ? ` · ${paperAbbr(it.q.paperKey)}` : ''}{it.q.lang === 'iv' ? ' · Gaeilge' : ''} · Question {it.q.n}
                </span>
                <ChevronRight size={16} className="shrink-0" style={{ color: ACCENT }} />
              </button>
            </div>
          ))}
        </div>

        <div className="flex flex-wrap items-center gap-2.5">
          <button onClick={() => downloadPack(packOpts)} className="inline-flex items-center gap-1.5 rounded-full px-4 py-2 text-[13px] font-semibold border-2 transition-transform active:translate-y-0.5" style={{ borderColor: 'rgba(242,107,31,0.35)', color: ACCENT }}>
            <Download size={14} /> Export set
          </button>
          <button onClick={finish} className="inline-flex items-center gap-1.5 rounded-full px-4 py-2 text-[13px] font-semibold border-2 transition-transform active:translate-y-0.5" style={{ borderColor: '#d0cdc8', color: '#7a7068' }}>
            <RefreshCw size={14} /> New set
          </button>
          {doneCount === set.items.length && (
            <span className="text-[12.5px] font-semibold" style={{ color: '#1F5F3E' }}>All done — nice.</span>
          )}
        </div>
      </div>
    );
  }

  // ═══════════ BUILD: pick subject ═══════════
  if (!subjectId) {
    return (
      <div className="w-full max-w-xl mx-auto pb-12">
        {header('Paper Trail', onBack)}
        <h2 className="text-2xl font-semibold mb-1 flex items-center gap-2" style={{ fontFamily: "'Source Serif 4', serif", color: INK }}>
          <FileStack size={20} style={{ color: ACCENT }} /> Build a mock set
        </h2>
        <p className="text-[13.5px] leading-relaxed mb-5" style={{ color: '#5a5550' }}>
          Assemble your own practice set from real past questions — mixed or on the topics you choose — then work through it against the marking schemes.
        </p>
        {subjects.length === 0 ? (
          <p className="text-[13.5px] rounded-2xl px-4 py-4" style={{ backgroundColor: '#E8EFF5', color: '#27506E' }}>
            Topic-tagged subjects are being added — check back soon.
          </p>
        ) : (
          <SubjectTilePicker
            headingLabel="Pick a subject"
            subjects={subjects.map(s => ({ id: s.id, label: s.label, sublabel: `${topicsForSubject(s.id).length} topics` }))}
            mineIds={mineIds}
            scope={scope}
            onScopeChange={setScope}
            onPick={id => { setSubjectId(id); setMode('mixed'); setChosen(new Set()); }}
          />
        )}
      </div>
    );
  }

  // ═══════════ BUILD: configure ═══════════
  const maxCount = pool.length;
  return (
    <div className="w-full max-w-xl mx-auto pb-12">
      {header('All subjects', () => setSubjectId(null))}
      <h2 className="text-2xl font-semibold mb-4" style={{ fontFamily: "'Source Serif 4', serif", color: INK }}>{subjectLabel(subjectId)} mock set</h2>

      {/* Scope */}
      <h3 className="text-[11px] font-bold uppercase tracking-[0.12em] mb-2" style={{ color: '#9e9186' }}>Coverage</h3>
      <div className="flex gap-2 mb-4">
        {(['mixed', 'topics'] as const).map(m => (
          <button
            key={m}
            onClick={() => setMode(m)}
            aria-pressed={mode === m}
            className="flex-1 py-2.5 rounded-xl border-2 text-[13px] font-semibold transition-colors"
            style={mode === m ? { backgroundColor: '#FDEEDF', borderColor: ACCENT, color: '#8C3A0E' } : { backgroundColor: '#fff', borderColor: '#d0cdc8', color: '#7a7068' }}
          >
            {m === 'mixed' ? 'Mixed — any topic' : 'Choose topics'}
          </button>
        ))}
      </div>

      {mode === 'topics' && (
        <div className="mb-4 max-h-64 overflow-y-auto rounded-xl border-2 border-[#d0cdc8] dark:border-zinc-700 divide-y divide-zinc-100 dark:divide-zinc-800">
          {topics.map(t => (
            <button key={t.subtopicId} onClick={() => toggleTopic(t.subtopicId)} className="w-full flex items-center gap-3 px-3.5 py-2.5 text-left">
              <span className="shrink-0 w-5 h-5 rounded flex items-center justify-center border-2" style={chosen.has(t.subtopicId) ? { backgroundColor: ACCENT, borderColor: ACCENT, color: '#fff' } : { borderColor: '#d0cdc8', color: 'transparent' }}>
                <Check size={13} />
              </span>
              <span className="flex-1 text-[13px] font-medium truncate" style={{ color: INK }}>{t.label}</span>
              <span className="shrink-0 text-[11.5px] tabular-nums" style={{ color: '#9e9186' }}>{t.count}</span>
            </button>
          ))}
        </div>
      )}

      {/* Length */}
      <h3 className="text-[11px] font-bold uppercase tracking-[0.12em] mb-2" style={{ color: '#9e9186' }}>Length</h3>
      <div className="flex gap-2 mb-2">
        {LENGTHS.map(n => (
          <button
            key={n}
            onClick={() => setCount(n)}
            aria-pressed={count === n}
            className="flex-1 py-2.5 rounded-xl border-2 text-[14px] font-bold transition-colors"
            style={count === n ? { backgroundColor: ACCENT, borderColor: ACCENT, color: '#fff' } : { backgroundColor: '#fff', borderColor: '#d0cdc8', color: '#7a7068' }}
          >
            {n}
          </button>
        ))}
      </div>
      <p className="text-[12px] mb-5" style={{ color: '#7a7068' }}>
        {maxCount === 0
          ? 'No questions match — pick at least one topic.'
          : `${Math.min(count, maxCount)} question${Math.min(count, maxCount) === 1 ? '' : 's'} from ${maxCount} available · target ~${fmtMin(Math.round((Math.min(count, maxCount) * 8) / 5) * 5)}`}
      </p>

      <button
        onClick={build}
        disabled={maxCount === 0}
        className="w-full py-3 rounded-full text-[14.5px] font-semibold text-white disabled:opacity-40 transition-transform active:translate-y-0.5"
        style={{ backgroundColor: ACCENT, boxShadow: '0 3px 0 #B54D14' }}
      >
        Build set
      </button>
    </div>
  );
};

export default MockExamBuilder;
