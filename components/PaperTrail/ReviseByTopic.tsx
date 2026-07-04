/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 *
 * Paper Trail — "Revise by topic" hub (feature A1). The payoff of the 5,306
 * topic tags as a top-level surface: pick a subject → see its topics (busiest
 * first, with your own weakness overlaid from self-marks) → pick a topic → every
 * past question on it across years, one tap to open beside its scheme.
 *
 * Self-contained 3-level navigator; opening a question hands back to the parent
 * (which reuses the cross-year jump).
 */

import React, { useMemo, useState } from 'react';
import { ArrowLeft, ChevronRight, Layers, Plus, Check } from 'lucide-react';
import SubjectTilePicker from '../shared/SubjectTilePicker';
import { siblingsFor, topicLabel, topicsForPaper, topicsForSubject, type SubjectTopic, type TopicSibling } from './topics';
import { allMarks } from './attemptStore';
import { addCard, hasCard, removeCard } from './reviewStore';
import { type PaperLang, type PaperLevel } from '../../types/paperTrail';

const INK = '#1a1a1a';
const ACCENT = '#F26B1F';
const LVL: Record<string, string> = { higher: 'HL', ordinary: 'OL', foundation: 'FL', common: 'CL' };
const paperAbbr = (k: string) => (k === 'p1' ? 'P1' : k === 'p2' ? 'P2' : '');

interface Props {
  subjects: { id: string; label: string }[];
  mineIds: string[];
  uid?: string;
  subjectLabel: (id: string) => string;
  onOpenQuestion: (t: TopicSibling) => void;
  onBack: () => void;
}

const ReviseByTopic: React.FC<Props> = ({ subjects, mineIds, uid, subjectLabel, onOpenQuestion, onBack }) => {
  const [scope, setScope] = useState<'mine' | 'all'>(mineIds.length ? 'mine' : 'all');
  const [subjectId, setSubjectId] = useState<string | null>(null);
  const [subtopicId, setSubtopicId] = useState<string | null>(null);
  const [revVer, setRevVer] = useState(0); // bump to re-read review-deck membership

  const toggleReview = (q: TopicSibling) => {
    const id = { subjectId: q.subjectId, year: q.year, level: q.level, lang: q.lang, fileid: q.fileid, n: q.n };
    if (hasCard(uid, id)) removeCard(uid, id);
    else addCard(uid, id, subtopicId ?? undefined, Date.now());
    setRevVer(v => v + 1);
  };

  // Per-topic average self-mark % for the chosen subject (weakness overlay).
  const weakByTopic = useMemo(() => {
    const m = new Map<string, { sum: number; n: number }>();
    if (!subjectId) return m;
    for (const mk of allMarks(uid)) {
      if (mk.subjectId !== subjectId) continue;
      const tags = topicsForPaper(mk.subjectId, mk.year, mk.level as PaperLevel, mk.lang as PaperLang, mk.fileid);
      const t = tags?.q.find(q => q.n === mk.n);
      if (!t) continue;
      const pct = mk.max ? (mk.score / mk.max) * 100 : mk.score;
      const cur = m.get(t.primary) ?? { sum: 0, n: 0 };
      cur.sum += pct;
      cur.n += 1;
      m.set(t.primary, cur);
    }
    return m;
  }, [subjectId, uid]);

  const topics: SubjectTopic[] = useMemo(() => (subjectId ? topicsForSubject(subjectId) : []), [subjectId]);
  const questions = useMemo(
    () => (subjectId && subtopicId ? siblingsFor(subjectId, subtopicId) : []),
    [subjectId, subtopicId],
  );

  // ── Level 2: questions for a topic ──
  if (subjectId && subtopicId) {
    const years = new Set(questions.map(q => q.year));
    return (
      <div className="w-full max-w-xl mx-auto pb-12">
        <button onClick={() => setSubtopicId(null)} className="flex items-center gap-1.5 text-[13px] font-medium mb-4" style={{ color: '#7a7068' }}>
          <ArrowLeft size={15} /> {subjectLabel(subjectId)} topics
        </button>
        <h2 className="text-2xl font-semibold mb-1" style={{ fontFamily: "'Source Serif 4', serif", color: INK }}>{topicLabel(subtopicId)}</h2>
        <p className="text-[13px] mb-4" style={{ color: '#7a7068' }}>
          {questions.length} question{questions.length === 1 ? '' : 's'} across {years.size} year{years.size === 1 ? '' : 's'} — tap to open with its marking scheme.
        </p>
        <div className="space-y-1.5">
          {questions.map(q => {
            void revVer; // recompute membership when the deck changes
            const saved = hasCard(uid, { subjectId: q.subjectId, year: q.year, level: q.level, lang: q.lang, fileid: q.fileid, n: q.n });
            return (
              <div
                key={`${q.year}-${q.level}-${q.lang}-${q.fileid}-${q.n}`}
                className="flex items-center gap-2 rounded-xl border-2 border-[#1a1a1a] dark:border-zinc-700 bg-white dark:bg-zinc-900 pr-2 transition-transform hover:-translate-y-0.5"
              >
                <button
                  onClick={() => onOpenQuestion(q)}
                  className="flex-1 flex items-center gap-3 px-3.5 py-2.5 text-left transition-transform active:translate-y-0.5"
                >
                  <span className="shrink-0 w-11 text-[14px] font-bold tabular-nums" style={{ fontFamily: "'Source Serif 4', serif", color: INK }}>{q.year}</span>
                  <span className="flex-1 text-[12.5px]" style={{ color: '#5a5550' }}>
                    {LVL[q.level] ?? q.level}{paperAbbr(q.paperKey) ? ` · ${paperAbbr(q.paperKey)}` : ''}{q.lang === 'iv' ? ' · Gaeilge' : ''} · Question {q.n}
                  </span>
                  <ChevronRight size={16} className="shrink-0" style={{ color: ACCENT }} />
                </button>
                <button
                  onClick={() => toggleReview(q)}
                  aria-pressed={saved}
                  aria-label={saved ? 'Remove from daily review' : 'Add to daily review'}
                  title={saved ? 'In your daily review' : 'Add to daily review'}
                  className="shrink-0 w-8 h-8 rounded-lg flex items-center justify-center border-2 transition-colors"
                  style={saved
                    ? { backgroundColor: '#E8F2EC', borderColor: '#3A8D5F', color: '#1F5F3E' }
                    : { backgroundColor: '#fff', borderColor: '#d0cdc8', color: '#9e9186' }}
                >
                  {saved ? <Check size={15} /> : <Plus size={15} />}
                </button>
              </div>
            );
          })}
        </div>
      </div>
    );
  }

  // ── Level 1: topics for a subject ──
  if (subjectId) {
    return (
      <div className="w-full max-w-xl mx-auto pb-12">
        <button onClick={() => setSubjectId(null)} className="flex items-center gap-1.5 text-[13px] font-medium mb-4" style={{ color: '#7a7068' }}>
          <ArrowLeft size={15} /> All subjects
        </button>
        <h2 className="text-2xl font-semibold mb-1" style={{ fontFamily: "'Source Serif 4', serif", color: INK }}>{subjectLabel(subjectId)}</h2>
        <p className="text-[13px] mb-4" style={{ color: '#7a7068' }}>Pick a topic to drill every past question on it.</p>
        <div className="space-y-1.5">
          {topics.map(t => {
            const w = weakByTopic.get(t.subtopicId);
            const avg = w && w.n ? Math.round(w.sum / w.n) : null;
            return (
              <button
                key={t.subtopicId}
                onClick={() => setSubtopicId(t.subtopicId)}
                className="w-full flex items-center gap-3 rounded-xl border-2 border-[#d0cdc8] dark:border-zinc-700 bg-white dark:bg-zinc-900 px-3.5 py-3 text-left transition-transform active:translate-y-0.5 hover:border-[#F26B1F]"
              >
                <span className="flex-1 min-w-0">
                  <span className="block text-[14px] font-semibold" style={{ fontFamily: "'Source Serif 4', serif", color: INK }}>{t.label}</span>
                  <span className="block text-[11.5px]" style={{ color: '#7a7068' }}>
                    {t.count} question{t.count === 1 ? '' : 's'} · {t.years} year{t.years === 1 ? '' : 's'}
                  </span>
                </span>
                {avg !== null && (
                  <span className="shrink-0 text-[12px] font-bold tabular-nums px-2 py-0.5 rounded-full" style={{ backgroundColor: avg < 50 ? '#FDEEDF' : '#E8F2EC', color: avg < 50 ? '#8C3A0E' : '#1F5F3E' }}>
                    you: {avg}%
                  </span>
                )}
                <ChevronRight size={16} className="shrink-0" style={{ color: ACCENT }} />
              </button>
            );
          })}
        </div>
      </div>
    );
  }

  // ── Level 0: subject picker ──
  return (
    <div className="w-full max-w-xl mx-auto pb-12">
      <button onClick={onBack} className="flex items-center gap-1.5 text-[13px] font-medium mb-4" style={{ color: '#7a7068' }}>
        <ArrowLeft size={15} /> Paper Trail
      </button>
      <h2 className="text-2xl font-semibold mb-1 flex items-center gap-2" style={{ fontFamily: "'Source Serif 4', serif", color: INK }}>
        <Layers size={20} style={{ color: ACCENT }} /> Revise by topic
      </h2>
      <p className="text-[13.5px] leading-relaxed mb-5" style={{ color: '#5a5550' }}>
        Every past-paper question, sorted by topic. Weak on one thing? Drill every question on it across every year — with the marking scheme one tap away.
      </p>
      {subjects.length === 0 ? (
        <p className="text-[13.5px] rounded-2xl px-4 py-4" style={{ backgroundColor: '#E8EFF5', color: '#27506E' }}>
          Topic revision is being added subject by subject — check back soon.
        </p>
      ) : (
        <SubjectTilePicker
          headingLabel="Pick a subject"
          subjects={subjects.map(s => ({ id: s.id, label: s.label, sublabel: `${topicsForSubject(s.id).length} topics` }))}
          mineIds={mineIds}
          scope={scope}
          onScopeChange={setScope}
          onPick={setSubjectId}
        />
      )}
    </div>
  );
};

export default ReviseByTopic;
