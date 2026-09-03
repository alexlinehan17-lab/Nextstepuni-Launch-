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

import { usePulse } from '../../hooks/usePulse';
import React, { useEffect, useMemo, useRef, useState } from 'react';
import { ArrowLeft, ChevronRight, Compass, Download, Search, X, Link2, Check as CheckIcon } from 'lucide-react';
import { siblingsFor, strandsFor, subjectAtlasStats, taggedYearsForSubject, topicLabel, topicsForSubject, topicYearSets, type SubjectTopic, type TopicSibling } from './topics';
import { addCard, hasCard, removeCard } from './reviewStore';
import { masteryForSubject, type TopicMastery } from './topicMastery';
import { downloadPack } from './revisionPack';
import VaultQuestionCard from './VaultQuestionCard';
import { releaseVaultPdfs } from './vaultDocs';
import { buildVaultLink, consumeInitialVaultLocation } from './vaultDeepLink';

const INK = '#1a1a1a';
const ACCENT = '#F26B1F';
const LVL: Record<string, string> = { higher: 'HL', ordinary: 'OL', foundation: 'FL', common: 'CL' };

interface Props {
  subjects: { id: string; label: string }[];
  mineIds: string[];
  uid?: string;
  subjectLabel: (id: string) => string;
  /** Re-open the feed at this subject/topic — set when returning from a
   *  "Full paper" round-trip (the parent carries it on the viewer view). */
  restore?: { subjectId: string; subtopicId: string };
  onOpenQuestion: (t: TopicSibling, origin: { subjectId: string; subtopicId: string }) => void;
  onBack: () => void;
}

const ReviseByTopic: React.FC<Props> = ({ subjects, mineIds, uid, subjectLabel, restore, onOpenQuestion, onBack }) => {
  // A shared "?subject=…&topic=…" link opens the vault straight at that topic
  // (consumed once per load — see vaultDeepLink; safe, never touches history).
  const [boot] = useState(() => consumeInitialVaultLocation());
  const [scope, setScope] = useState<'mine' | 'all'>(mineIds.length ? 'mine' : 'all');
  const [subjectId, setSubjectId] = useState<string | null>(restore?.subjectId ?? boot?.subjectId ?? null);
  const [subtopicId, setSubtopicId] = useState<string | null>(restore?.subtopicId ?? boot?.subtopicId ?? null);
  const [copied, pulseCopied, clearCopied] = usePulse(2000);
  const [sort, setSort] = useState<'busiest' | 'frequent'>('busiest');
  const [levelFilter, setLevelFilter] = useState<'all' | string>('all');
  const [yearFilter, setYearFilter] = useState<'all' | number>('all');
  const [topicQuery, setTopicQuery] = useState('');
  const [revVer, setRevVer] = useState(0); // bump to re-read review-deck membership

  // The vault feed keeps a small pool of open PDFs — release them on exit.
  useEffect(() => () => releaseVaultPdfs(), []);
  // Drilling in/out replaces the whole view, so the focused element vanishes
  // and focus falls back to <body>. Land keyboard/screen-reader users on the
  // new level's heading instead (skipping the initial mount — no focus theft).
  const level = subjectId ? (subtopicId ? 2 : 1) : 0;
  const headingRef = useRef<HTMLHeadingElement | null>(null);
  const prevLevel = useRef(level);
  useEffect(() => {
    if (prevLevel.current !== level) headingRef.current?.focus();
    prevLevel.current = level;
  }, [level]);
  // A new topic starts with fresh level + year filters.
  useEffect(() => { setLevelFilter('all'); setYearFilter('all'); }, [subtopicId]);
  // Reset the topic search when switching subjects.
  useEffect(() => { setTopicQuery(''); }, [subjectId]);
  // The "Copied" confirmation is per-topic.
  useEffect(() => { clearCopied(); }, [subtopicId, clearCopied]);

  const copyTopicLink = async () => {
    if (!subjectId || !subtopicId) return;
    const url = buildVaultLink(subjectId, subtopicId);
    try {
      await navigator.clipboard.writeText(url);
      pulseCopied();
    } catch {
      // Clipboard blocked (insecure context / permissions) — surface the URL so
      // the student can still copy it by hand rather than failing silently.
      window.prompt('Copy this link to share the topic:', url);
    }
  };

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
  const sortedTopics: SubjectTopic[] = useMemo(() => {
    if (sort === 'busiest') return baseTopics; // already count-sorted
    return [...baseTopics].sort((a, b) => b.years - a.years || b.count - a.count || a.label.localeCompare(b.label));
  }, [baseTopics, sort]);
  // Type-to-filter topics — subjects like Geography carry 40+ topics.
  const topics: SubjectTopic[] = useMemo(() => {
    const q = topicQuery.trim().toLowerCase();
    if (!q) return sortedTopics;
    return sortedTopics.filter(t => t.label.toLowerCase().includes(q));
  }, [sortedTopics, topicQuery]);
  const questions = useMemo(
    () => (subjectId && subtopicId ? siblingsFor(subjectId, subtopicId) : []),
    [subjectId, subtopicId],
  );

  // ── Level 2: the vault feed — every question on the topic, newest first,
  //    rendered as real paper crops with the scheme behind a toggle. ──
  if (subjectId && subtopicId) {
    const years = new Set(questions.map(q => q.year));
    const levels = [...new Set(questions.map(q => q.level))];
    const yearList = [...years].sort((a, b) => b - a); // newest first
    const inYear = yearFilter === 'all' ? questions : questions.filter(q => q.year === yearFilter);
    const shown = levelFilter === 'all' ? inYear : inYear.filter(q => q.level === levelFilter);
    const levelCount = (l: string) => (l === 'all' ? inYear.length : inYear.filter(q => q.level === l).length);
    return (
      <div className="w-full max-w-2xl mx-auto pb-12">
        <button onClick={() => setSubtopicId(null)} className="flex items-center gap-1.5 text-[13px] font-medium mb-4" style={{ color: '#7a7068' }}>
          <ArrowLeft size={15} /> {subjectLabel(subjectId)} topics
        </button>
        <h2 ref={headingRef} tabIndex={-1} className="text-2xl font-semibold mb-1 outline-none text-[#1a1a1a] dark:text-zinc-100" style={{ fontFamily: "'Source Serif 4', serif" }}>{topicLabel(subtopicId)}</h2>
        <p aria-live="polite" className="text-[13px] mb-3" style={{ color: '#7a7068' }}>
          {levelFilter === 'all' && yearFilter === 'all'
            ? <>{questions.length} question{questions.length === 1 ? '' : 's'} across {years.size} year{years.size === 1 ? '' : 's'}, newest first — each shown as printed on the paper, marking scheme one tap below.</>
            : <>Showing {shown.length} of {questions.length} question{questions.length === 1 ? '' : 's'}{yearFilter !== 'all' ? ` from ${yearFilter}` : ''}{levelFilter !== 'all' ? ` · ${LVL[levelFilter] ?? levelFilter}` : ''}.</>}
        </p>
        <div className="flex items-center gap-2 flex-wrap mb-4">
          {levels.length > 1 && (
            <div className="flex items-center gap-1 p-1 rounded-xl bg-zinc-100 dark:bg-zinc-800/50 w-fit" role="group" aria-label="Filter by level">
              {(['all', ...levels] as const).map(l => (
                <button
                  key={l}
                  aria-pressed={levelFilter === l}
                  onClick={() => setLevelFilter(l)}
                  className={`px-3 py-1.5 rounded-lg text-[12px] transition-all ${levelFilter === l ? 'bg-white dark:bg-zinc-800 font-semibold shadow-sm' : ''}`}
                  style={{ color: levelFilter === l ? INK : '#7a7068' }}
                >
                  {l === 'all' ? 'All levels' : LVL[l] ?? l}
                  <span className="ml-1 tabular-nums" style={{ color: '#9e9186' }}>{levelCount(l)}</span>
                </button>
              ))}
            </div>
          )}
          {questions.length > 0 && (
            <button
              onClick={() => downloadPack({
                subjectLabel: subjectLabel(subjectId),
                topicLabel: topicLabel(subtopicId),
                questions,
                dateIso: new Date(Date.now()).toISOString().slice(0, 10),
              })}
              className="inline-flex items-center gap-1.5 rounded-full px-3.5 py-1.5 text-[12.5px] font-semibold border-2 transition-transform active:translate-y-0.5"
              style={{ borderColor: 'rgba(242,107,31,0.35)', color: ACCENT }}
            >
              <Download size={14} /> Export revision pack
            </button>
          )}
          <button
            onClick={copyTopicLink}
            aria-label="Copy a shareable link to this topic"
            className="inline-flex items-center gap-1.5 rounded-full px-3.5 py-1.5 text-[12.5px] font-semibold border-2 transition-transform active:translate-y-0.5"
            style={copied
              ? { borderColor: '#3A8D5F', color: '#1F5F3E', backgroundColor: '#E8F2EC' }
              : { borderColor: '#d0cdc8', color: '#7a7068' }}
          >
            {copied ? <><CheckIcon size={14} /> Link copied</> : <><Link2 size={14} /> Copy link</>}
          </button>
        </div>
        {/* Year filter — jump straight to a sitting (Studyclix-style). */}
        {yearList.length > 3 && (
          <div className="flex items-center gap-1.5 overflow-x-auto pb-2 mb-3 -mx-1 px-1" role="group" aria-label="Filter by year">
            <button
              aria-pressed={yearFilter === 'all'}
              onClick={() => setYearFilter('all')}
              className={`shrink-0 px-3 py-1 rounded-full text-[12px] font-semibold border-2 transition-colors ${yearFilter === 'all' ? '' : 'bg-white'}`}
              style={yearFilter === 'all'
                ? { backgroundColor: ACCENT, borderColor: ACCENT, color: '#fff' }
                : { borderColor: '#d0cdc8', color: '#7a7068' }}
            >
              All years
            </button>
            {yearList.map(y => (
              <button
                key={y}
                aria-pressed={yearFilter === y}
                onClick={() => setYearFilter(y)}
                className={`shrink-0 px-3 py-1 rounded-full text-[12px] font-semibold tabular-nums border-2 transition-colors ${yearFilter === y ? '' : 'bg-white'}`}
                style={yearFilter === y
                  ? { backgroundColor: ACCENT, borderColor: ACCENT, color: '#fff' }
                  : { borderColor: '#d0cdc8', color: '#7a7068' }}
              >
                {y}
              </button>
            ))}
          </div>
        )}
        <div className="space-y-4">
          {shown.length === 0 ? (
            <p className="text-[13px] rounded-xl px-4 py-3" style={{ backgroundColor: '#FDEEDF', color: '#8C3A0E' }}>
              No questions for that filter. <button onClick={() => { setLevelFilter('all'); setYearFilter('all'); }} className="font-semibold underline">Show all</button>
            </p>
          ) : shown.map(q => {
            void revVer; // recompute membership when the deck changes
            const saved = hasCard(uid, { subjectId: q.subjectId, year: q.year, level: q.level, lang: q.lang, fileid: q.fileid, n: q.n });
            return (
              <VaultQuestionCard
                key={`${q.year}-${q.level}-${q.lang}-${q.fileid}-${q.n}`}
                sibling={q}
                saved={saved}
                onToggleReview={() => toggleReview(q)}
                onOpenInPaper={() => onOpenQuestion(q, { subjectId, subtopicId })}
              />
            );
          })}
        </div>
      </div>
    );
  }

  // ── Level 1: the topic map — curriculum units, each topic with its
  //    cross-year record as a strip of year dots. ──
  if (subjectId) {
    const stats = subjectAtlasStats(subjectId);
    const yearSets = topicYearSets(subjectId);
    const strands = strandsFor(subjectId, topics.map(t => t.subtopicId));
    const topicById = new Map(topics.map(t => [t.subtopicId, t]));
    return (
      <div className="w-full max-w-2xl mx-auto pb-12">
        <button onClick={() => setSubjectId(null)} className="flex items-center gap-1.5 text-[13px] font-medium mb-4" style={{ color: '#7a7068' }}>
          <ArrowLeft size={15} /> All subjects
        </button>
        <h2 ref={headingRef} tabIndex={-1} className="text-2xl font-semibold mb-1 outline-none text-[#1a1a1a] dark:text-zinc-100" style={{ fontFamily: "'Source Serif 4', serif" }}>{subjectLabel(subjectId)}</h2>
        <p className="text-[13px] mb-4" style={{ color: '#7a7068' }}>
          <span className="tabular-nums">{stats.questions.toLocaleString()}</span> past questions · <span className="tabular-nums">{baseTopics.length}</span> topics · <span className="tabular-nums">{stats.yearMin}–{stats.yearMax}</span>. Pick a topic to see every one.
        </p>
        <div className="flex items-center gap-2 flex-wrap mb-3">
          <div className="flex items-center gap-1 p-1 rounded-xl bg-zinc-100 dark:bg-zinc-800/50 w-fit" role="group" aria-label="Sort topics">
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
        </div>
        {sortedTopics.length > 8 && (
          <div className="relative mb-4">
            <Search size={15} className="absolute left-3 top-1/2 -translate-y-1/2 pointer-events-none" style={{ color: '#9e9186' }} />
            <input
              type="text"
              value={topicQuery}
              onChange={e => setTopicQuery(e.target.value)}
              placeholder={`Search ${sortedTopics.length} topics…`}
              aria-label="Search topics"
              className="w-full rounded-xl border-2 border-[#d0cdc8] bg-white pl-9 pr-9 py-2.5 text-[13.5px] outline-none focus:border-[#F26B1F] transition-colors"
              style={{ color: INK }}
            />
            {topicQuery && (
              <button
                onClick={() => setTopicQuery('')}
                aria-label="Clear search"
                className="absolute right-2.5 top-1/2 -translate-y-1/2 w-6 h-6 rounded-lg flex items-center justify-center hover:bg-zinc-100 dark:hover:bg-zinc-800"
                style={{ color: '#9e9186' }}
              >
                <X size={14} />
              </button>
            )}
          </div>
        )}
        {topics.length === 0 ? (
          <p className="text-[13px] rounded-xl px-4 py-3" style={{ backgroundColor: '#FDEEDF', color: '#8C3A0E' }}>
            No topics match “{topicQuery.trim()}”. <button onClick={() => setTopicQuery('')} className="font-semibold underline">Clear</button>
          </p>
        ) : strands.map(strand => {
          const strandTopics = strand.subtopicIds
            .map(id => topicById.get(id))
            .filter((t): t is SubjectTopic => !!t);
          if (!strandTopics.length) return null;
          const ordered = [...strandTopics].sort((a, b) =>
            sort === 'busiest'
              ? b.count - a.count || b.years - a.years || a.label.localeCompare(b.label)
              : b.years - a.years || b.count - a.count || a.label.localeCompare(b.label));
          return (
            <section key={strand.id} className="mb-6">
              <h3 className="text-[11px] font-bold uppercase tracking-[0.12em] mb-2" style={{ color: '#9e9186' }}>
                {strand.name}
              </h3>
              <div className="space-y-2">
                {ordered.map(t => {
                  const m = masteryMap.get(t.subtopicId);
                  const masteryColor = m ? (m.mastery >= 70 ? '#3A8D5F' : '#F26B1F') : null;
                  const highYield = isHighYield(t);
                  const asked = yearSets.get(t.subtopicId) ?? new Set<number>();
                  return (
                    <button
                      key={t.subtopicId}
                      onClick={() => setSubtopicId(t.subtopicId)}
                      className="w-full flex items-center gap-3 rounded-xl border-[1.5px] border-[#1a1a1a] bg-white px-4 py-3 text-left transition-all active:translate-y-0.5 hover:-translate-y-0.5 hover:shadow-[3px_3px_0_0_#1A1A1A]"
                    >
                      <span className="flex-1 min-w-0">
                        <span className="flex items-center gap-2">
                          <span className="text-[14.5px] font-semibold" style={{ fontFamily: "'Source Serif 4', serif", color: INK }}>{t.label}</span>
                          {highYield && (
                            <span className="shrink-0 text-[9.5px] font-bold uppercase tracking-wide px-1.5 py-0.5 rounded-full" style={{ backgroundColor: '#FDEEDF', color: '#8C3A0E', border: '1px solid rgba(242,107,31,0.3)' }}>
                              High-yield
                            </span>
                          )}
                        </span>
                        <span className="block text-[11.5px] mt-0.5 mb-1.5" style={{ color: '#7a7068' }}>
                          <span className="tabular-nums">{t.count}</span> question{t.count === 1 ? '' : 's'} · <span className="tabular-nums">{t.years}</span> of <span className="tabular-nums">{totalYears}</span> years
                        </span>
                        <span className="flex items-center gap-[3px]" aria-hidden="true">
                          {stats.years.map(y => (
                            <span
                              key={y}
                              title={String(y)}
                              className="inline-block w-[7px] h-[7px] rounded-full"
                              style={asked.has(y)
                                ? { backgroundColor: '#F26B1F' }
                                : { backgroundColor: 'transparent', boxShadow: 'inset 0 0 0 1.5px #e0dbd4' }}
                            />
                          ))}
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
            </section>
          );
        })}
      </div>
    );
  }

  // ── Level 0: the atlas shelf — one card per charted subject, each carrying
  //    its own per-year question fingerprint. ──
  const shownSubjects = (scope === 'mine' ? subjects.filter(s => mineIds.includes(s.id)) : subjects);
  const maxPerYear = (per: Map<number, number>) => Math.max(1, ...per.values());
  return (
    <div className="w-full max-w-2xl mx-auto pb-12">
      <button onClick={onBack} className="flex items-center gap-1.5 text-[13px] font-medium mb-4" style={{ color: '#7a7068' }}>
        <ArrowLeft size={15} /> Paper Trail
      </button>
      <h2 ref={headingRef} tabIndex={-1} className="text-2xl font-semibold mb-1 flex items-center gap-2 outline-none text-[#1a1a1a] dark:text-zinc-100" style={{ fontFamily: "'Source Serif 4', serif" }}>
        <Compass size={22} style={{ color: ACCENT }} /> Topic Atlas
      </h2>
      <p className="text-[13.5px] leading-relaxed mb-5 max-w-[52ch]" style={{ color: '#5a5550' }}>
        Every past-paper question, mapped by topic. Pick a subject, pick a topic, and every question the SEC has asked on it is one tap away — with its marking scheme beside it.
      </p>
      {subjects.length === 0 ? (
        <p className="text-[13.5px] rounded-2xl px-4 py-4" style={{ backgroundColor: '#E8EFF5', color: '#27506E' }}>
          The atlas is being charted subject by subject — check back soon.
        </p>
      ) : (
        <>
          {mineIds.length > 0 && (
            <div className="flex items-center gap-1 p-1 rounded-xl bg-zinc-100 dark:bg-zinc-800/50 w-fit mb-4" role="group" aria-label="Subject scope">
              {(['mine', 'all'] as const).map(sc => (
                <button
                  key={sc}
                  aria-pressed={scope === sc}
                  onClick={() => setScope(sc)}
                  className={`px-3 py-1.5 rounded-lg text-[12.5px] transition-all ${scope === sc ? 'bg-white dark:bg-zinc-800 font-semibold shadow-sm' : ''}`}
                  style={{ color: scope === sc ? INK : '#7a7068' }}
                >
                  {sc === 'mine' ? 'My subjects' : 'All subjects'}
                </button>
              ))}
            </div>
          )}
          <div className="grid grid-cols-1 sm:grid-cols-2 gap-3">
            {shownSubjects.map(s => {
              const st = subjectAtlasStats(s.id);
              const peak = maxPerYear(st.perYear);
              return (
                <button
                  key={s.id}
                  onClick={() => setSubjectId(s.id)}
                  className="rounded-2xl border-2 border-[#1A1A1A] bg-white shadow-[3px_3px_0_0_#1A1A1A] px-4 pt-4 pb-3 text-left transition-transform active:translate-y-0.5 hover:-translate-y-0.5"
                >
                  <span className="block text-[16.5px] font-semibold mb-0.5" style={{ fontFamily: "'Source Serif 4', serif", color: INK }}>{s.label}</span>
                  <span className="block text-[11.5px] mb-2.5" style={{ color: '#7a7068' }}>
                    <span className="tabular-nums">{st.questions.toLocaleString()}</span> questions · <span className="tabular-nums">{topicsForSubject(s.id).length}</span> topics · <span className="tabular-nums">{st.yearMin}–{st.yearMax}</span>
                  </span>
                  <span className="flex items-end gap-[2px] h-[22px]" aria-hidden="true">
                    {st.years.map(y => (
                      <span
                        key={y}
                        title={`${y}: ${st.perYear.get(y) ?? 0} questions`}
                        className="flex-1 rounded-[1px] min-w-[3px]"
                        style={{
                          height: `${Math.max(12, Math.round(((st.perYear.get(y) ?? 0) / peak) * 100))}%`,
                          backgroundColor: 'rgba(242,107,31,0.45)',
                        }}
                      />
                    ))}
                  </span>
                </button>
              );
            })}
          </div>
        </>
      )}
    </div>
  );
};

export default ReviseByTopic;
