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
import { ArrowLeft, ChevronRight, Layers, Plus, Check, Download } from 'lucide-react';
import SubjectTilePicker from '../shared/SubjectTilePicker';
import { siblingsFor, taggedYearsForSubject, topicLabel, topicsForSubject, type SubjectTopic, type TopicSibling } from './topics';
import { addCard, hasCard, removeCard } from './reviewStore';
import { masteryForSubject, type TopicMastery } from './topicMastery';
import { downloadPack } from './revisionPack';

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
  const [sort, setSort] = useState<'busiest' | 'frequent'>('busiest');
  const [revVer, setRevVer] = useState(0); // bump to re-read review-deck membership

  const toggleReview = (q: TopicSibling) => {
    const id = { subjectId: q.subjectId, year: q.year, level: q.level, lang: q.lang, fileid: q.fileid, n: q.n };
    if (hasCard(uid, id)) removeCard(uid, id);
    else addCard(uid, id, subtopicId ?? undefined, Date.now());
    setRevVer(v => v + 1);
  };

  // Per-topic mastery for the chosen subject (accuracy + FSRS retention).
  const masteryMap = useMemo(() => {
    void revVer; // recompute after adding cards changes retention signals
    const m = new Map<string, TopicMastery>();
    if (subjectId) for (const t of masteryForSubject(uid, subjectId)) m.set(t.subtopicId, t);
    return m;
  }, [subjectId, uid, revVer]);

  const baseTopics: SubjectTopic[] = useMemo(() => (subjectId ? topicsForSubject(subjectId) : []), [subjectId]);
  const totalYears = useMemo(() => (subjectId ? taggedYearsForSubject(subjectId) : 0), [subjectId]);
  // "High-yield" = recurs in most tagged years (honest historical frequency,
  // never a prediction). Only meaningful once there are a few years to compare.
  const isHighYield = (t: SubjectTopic) => totalYears >= 3 && t.years / totalYears >= 0.6;
  const topics: SubjectTopic[] = useMemo(() => {
    if (sort === 'busiest') return baseTopics; // already count-sorted
    return [...baseTopics].sort((a, b) => b.years - a.years || b.count - a.count || a.label.localeCompare(b.label));
  }, [baseTopics, sort]);
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
        <p className="text-[13px] mb-3" style={{ color: '#7a7068' }}>
          {questions.length} question{questions.length === 1 ? '' : 's'} across {years.size} year{years.size === 1 ? '' : 's'} — tap to open with its marking scheme.
        </p>
        {questions.length > 0 && (
          <button
            onClick={() => downloadPack({
              subjectLabel: subjectLabel(subjectId),
              topicLabel: topicLabel(subtopicId),
              questions,
              dateIso: new Date(Date.now()).toISOString().slice(0, 10),
            })}
            className="inline-flex items-center gap-1.5 mb-4 rounded-full px-3.5 py-1.5 text-[12.5px] font-semibold border-2 transition-transform active:translate-y-0.5"
            style={{ borderColor: 'rgba(242,107,31,0.35)', color: ACCENT }}
          >
            <Download size={14} /> Export revision pack
          </button>
        )}
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
        <p className="text-[13px] mb-3" style={{ color: '#7a7068' }}>Pick a topic to drill every past question on it.</p>
        {/* Sort: busiest by question count, or by how many years it recurs. */}
        <div className="flex items-center gap-1 p-1 rounded-xl bg-zinc-100 dark:bg-zinc-800/50 w-fit mb-4" role="group" aria-label="Sort topics">
          {(['busiest', 'frequent'] as const).map(s => (
            <button
              key={s}
              aria-pressed={sort === s}
              onClick={() => setSort(s)}
              className={`px-3 py-1.5 rounded-lg text-[12.5px] transition-all ${sort === s ? 'bg-white dark:bg-zinc-800 font-semibold shadow-sm' : ''}`}
              style={{ color: sort === s ? INK : '#7a7068' }}
            >
              {s === 'busiest' ? 'Most questions' : 'Most examined'}
            </button>
          ))}
        </div>
        <div className="space-y-1.5">
          {topics.map(t => {
            const m = masteryMap.get(t.subtopicId);
            const masteryColor = m ? (m.mastery >= 70 ? '#3A8D5F' : '#F26B1F') : null;
            const highYield = isHighYield(t);
            return (
              <button
                key={t.subtopicId}
                onClick={() => setSubtopicId(t.subtopicId)}
                className="w-full flex items-center gap-3 rounded-xl border-2 border-[#d0cdc8] dark:border-zinc-700 bg-white dark:bg-zinc-900 px-3.5 py-3 text-left transition-transform active:translate-y-0.5 hover:border-[#F26B1F]"
              >
                <span className="flex-1 min-w-0">
                  <span className="flex items-center gap-2">
                    <span className="text-[14px] font-semibold" style={{ fontFamily: "'Source Serif 4', serif", color: INK }}>{t.label}</span>
                    {highYield && (
                      <span className="shrink-0 text-[9.5px] font-bold uppercase tracking-wide px-1.5 py-0.5 rounded-full" style={{ backgroundColor: '#FDEEDF', color: '#8C3A0E', border: '1px solid rgba(242,107,31,0.3)' }}>
                        High-yield
                      </span>
                    )}
                  </span>
                  <span className="block text-[11.5px] mt-0.5" style={{ color: '#7a7068' }}>
                    {t.count} question{t.count === 1 ? '' : 's'} · appeared in {t.years} of {totalYears} year{totalYears === 1 ? '' : 's'}
                  </span>
                </span>
                {m && masteryColor && (
                  <span className="shrink-0 w-16 text-right">
                    <span className="block text-[11px] font-bold tabular-nums" style={{ color: masteryColor }}>{m.mastery}%</span>
                    <span className="block mt-0.5 h-1.5 rounded-full overflow-hidden" style={{ backgroundColor: '#e0dbd4' }}>
                      <span className="block h-full rounded-full" style={{ width: `${m.mastery}%`, backgroundColor: masteryColor }} />
                    </span>
                    <span className="block text-[9px] mt-0.5" style={{ color: '#9e9186' }}>mastery</span>
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
