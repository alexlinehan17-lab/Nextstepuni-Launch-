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
import { ArrowLeft, Download, Search, X, Link2, Check as CheckIcon } from 'lucide-react';
import { siblingsFor, strandsFor, subjectAtlasStats, taggedYearsForSubject, topicLabel, topicsForSubject, topicYearSets, type SubjectTopic, type TopicSibling } from './topics';
import { addCard, hasCard, removeCard } from './reviewStore';
import { masteryForSubject, type TopicMastery } from './topicMastery';
import { downloadPack } from './revisionPack';
import VaultQuestionCard from './VaultQuestionCard';
import { releaseVaultPdfs } from './vaultDocs';
import { buildVaultLink, consumeInitialVaultLocation } from './vaultDeepLink';

const INK = '#1a1a1a';
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
  // Language preference — English by default, remembered per device. The feed
  // shows one edition per question; the other stays a click away.
  const [langPref, setLangPref] = useState<'ev' | 'iv'>(() => {
    try { return localStorage.getItem('atlas.lang') === 'iv' ? 'iv' : 'ev'; } catch { return 'ev'; }
  });
  const pickLang = (l: 'ev' | 'iv') => {
    setLangPref(l);
    try { localStorage.setItem('atlas.lang', l); } catch { /* private mode */ }
  };

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
  const allEditions = useMemo(
    () => (subjectId && subtopicId ? siblingsFor(subjectId, subtopicId) : []),
    [subjectId, subtopicId],
  );
  const hasIrish = useMemo(() => allEditions.some(q => q.lang === 'iv'), [allEditions]);
  // One edition per printed question: the preferred language where it exists,
  // the other edition otherwise (an Irish-only sitting still shows under
  // English, marked as Gaeilge on the card).
  const questions = useMemo(() => {
    const byQ = new Map<string, TopicSibling>();
    for (const q of allEditions) {
      const key = `${q.year}|${q.level}|${q.paperKey}|${q.n}`;
      const cur = byQ.get(key);
      if (!cur || (cur.lang !== langPref && q.lang === langPref)) byQ.set(key, q);
    }
    return [...byQ.values()].sort((a, b) => b.year - a.year || a.level.localeCompare(b.level) || Number(a.n) - Number(b.n));
  }, [allEditions, langPref]);

  // ── Level 2: the feed — one edition per question, newest first, real
  //    paper crops with the scheme a tap below. Quiet text controls. ──
  if (subjectId && subtopicId) {
    const years = new Set(questions.map(q => q.year));
    const levels = [...new Set(questions.map(q => q.level))];
    const yearList = [...years].sort((a, b) => b - a);
    const inYear = yearFilter === 'all' ? questions : questions.filter(q => q.year === yearFilter);
    const shown = levelFilter === 'all' ? inYear : inYear.filter(q => q.level === levelFilter);
    const levelCount = (l: string) => (l === 'all' ? inYear.length : inYear.filter(q => q.level === l).length);
    const tab = (active: boolean) => ({
      color: active ? INK : '#8d857c',
      boxShadow: active ? `inset 0 -2px 0 0 ${INK}` : 'none',
    });
    return (
      <div className="w-full max-w-2xl mx-auto pb-12">
        <button onClick={() => setSubtopicId(null)} className="flex items-center gap-1.5 text-[13px] font-medium mb-5" style={{ color: '#7a7068' }}>
          <ArrowLeft size={15} /> {subjectLabel(subjectId)}
        </button>
        <h2 ref={headingRef} tabIndex={-1} className="text-[26px] font-semibold mb-1 outline-none text-[#1a1a1a] dark:text-zinc-100" style={{ fontFamily: "'Source Serif 4', serif" }}>{topicLabel(subtopicId)}</h2>
        <p aria-live="polite" className="text-[13px] mb-5 tabular-nums" style={{ color: '#8d857c' }}>
          {shown.length === questions.length
            ? <>{questions.length} question{questions.length === 1 ? '' : 's'} · {years.size} year{years.size === 1 ? '' : 's'} · marking scheme beneath each</>
            : <>{shown.length} of {questions.length} questions{yearFilter !== 'all' ? ` · ${yearFilter}` : ''}{levelFilter !== 'all' ? ` · ${LVL[levelFilter] ?? levelFilter}` : ''}</>}
        </p>

        <div className="flex items-center gap-x-5 gap-y-3 flex-wrap pb-3 mb-6" style={{ borderBottom: '1px solid #e7e3de' }}>
          {levels.length > 1 && (
            <div className="flex items-center gap-4" role="group" aria-label="Level">
              {(['all', ...levels] as const).map(l => (
                <button key={l} aria-pressed={levelFilter === l} onClick={() => setLevelFilter(l)}
                  className="pb-1 text-[13px] font-medium transition-colors" style={tab(levelFilter === l)}>
                  {l === 'all' ? 'All levels' : LVL[l] ?? l}
                  <span className="ml-1 tabular-nums" style={{ color: '#b3aca3' }}>{levelCount(l)}</span>
                </button>
              ))}
            </div>
          )}
          {hasIrish && (
            <div className="flex items-center gap-4" role="group" aria-label="Language">
              {(['ev', 'iv'] as const).map(l => (
                <button key={l} aria-pressed={langPref === l} onClick={() => pickLang(l)}
                  className="pb-1 text-[13px] font-medium transition-colors" style={tab(langPref === l)}>
                  {l === 'ev' ? 'English' : 'Gaeilge'}
                </button>
              ))}
            </div>
          )}
          {yearList.length > 3 && (
            <label className="flex items-center gap-1.5 text-[13px]" style={{ color: '#8d857c' }}>
              <select
                value={yearFilter === 'all' ? 'all' : String(yearFilter)}
                onChange={e => setYearFilter(e.target.value === 'all' ? 'all' : Number(e.target.value))}
                aria-label="Year"
                className="bg-transparent pb-1 text-[13px] font-medium outline-none cursor-pointer"
                style={{ color: yearFilter === 'all' ? '#8d857c' : INK, border: 'none', borderBottom: yearFilter === 'all' ? 'none' : `2px solid ${INK}` }}
              >
                <option value="all">All years</option>
                {yearList.map(y => <option key={y} value={y}>{y}</option>)}
              </select>
            </label>
          )}
          <span className="flex-1" />
          {questions.length > 0 && (
            <button
              onClick={() => downloadPack({
                subjectLabel: subjectLabel(subjectId),
                topicLabel: topicLabel(subtopicId),
                questions: shown.length ? shown : questions,
                dateIso: new Date(Date.now()).toISOString().slice(0, 10),
              })}
              className="flex items-center gap-1.5 text-[12.5px] font-medium transition-colors hover:text-[#1a1a1a]"
              style={{ color: '#8d857c' }}
            >
              <Download size={13} /> Export
            </button>
          )}
          <button
            onClick={copyTopicLink}
            aria-label="Copy a shareable link to this topic"
            className="flex items-center gap-1.5 text-[12.5px] font-medium transition-colors hover:text-[#1a1a1a]"
            style={copied ? { color: '#1F5F3E' } : { color: '#8d857c' }}
          >
            {copied ? <><CheckIcon size={13} /> Copied</> : <><Link2 size={13} /> Share</>}
          </button>
        </div>

        <div className="space-y-5">
          {shown.length === 0 ? (
            <p className="text-[13px] py-3" style={{ color: '#8d857c' }}>
              No questions match that filter. <button onClick={() => { setLevelFilter('all'); setYearFilter('all'); }} className="font-semibold underline" style={{ color: INK }}>Show all</button>
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

  // ── Level 1: the topic map — an editorial index: curriculum units as
  //    ruled sections, each topic a quiet row with its cross-year record. ──
  if (subjectId) {
    const stats = subjectAtlasStats(subjectId);
    const yearSets = topicYearSets(subjectId);
    const strands = strandsFor(subjectId, topics.map(t => t.subtopicId));
    const topicById = new Map(topics.map(t => [t.subtopicId, t]));
    const tab = (active: boolean) => ({
      color: active ? INK : '#8d857c',
      boxShadow: active ? `inset 0 -2px 0 0 ${INK}` : 'none',
    });
    return (
      <div className="w-full max-w-2xl mx-auto pb-12">
        <button onClick={() => setSubjectId(null)} className="flex items-center gap-1.5 text-[13px] font-medium mb-5" style={{ color: '#7a7068' }}>
          <ArrowLeft size={15} /> All subjects
        </button>
        <h2 ref={headingRef} tabIndex={-1} className="text-[26px] font-semibold mb-1 outline-none text-[#1a1a1a] dark:text-zinc-100" style={{ fontFamily: "'Source Serif 4', serif" }}>{subjectLabel(subjectId)}</h2>
        <p className="text-[13px] mb-5 tabular-nums" style={{ color: '#8d857c' }}>
          {stats.questions.toLocaleString()} questions · {baseTopics.length} topics · {stats.yearMin}–{stats.yearMax}
        </p>
        <div className="flex items-center gap-x-5 gap-y-3 flex-wrap pb-3 mb-2" style={{ borderBottom: '1px solid #e7e3de' }}>
          <div className="flex items-center gap-4" role="group" aria-label="Sort topics">
            {(['busiest', 'frequent'] as const).map(s => (
              <button key={s} aria-pressed={sort === s} onClick={() => setSort(s)}
                className="pb-1 text-[13px] font-medium transition-colors" style={tab(sort === s)}>
                {s === 'busiest' ? 'Most asked' : 'Most recurrent'}
              </button>
            ))}
          </div>
          <span className="flex-1" />
          {sortedTopics.length > 8 && (
            <div className="relative">
              <Search size={14} className="absolute left-0 top-1/2 -translate-y-1/2 pointer-events-none" style={{ color: '#b3aca3' }} />
              <input
                type="text"
                value={topicQuery}
                onChange={e => setTopicQuery(e.target.value)}
                placeholder="Search topics"
                aria-label="Search topics"
                className="w-44 bg-transparent pl-6 pr-6 pb-1 text-[13px] outline-none transition-colors"
                style={{ color: INK, borderBottom: `1px solid ${topicQuery ? INK : '#d8d3cc'}` }}
              />
              {topicQuery && (
                <button onClick={() => setTopicQuery('')} aria-label="Clear search"
                  className="absolute right-0 top-1/2 -translate-y-1/2" style={{ color: '#b3aca3' }}>
                  <X size={13} />
                </button>
              )}
            </div>
          )}
        </div>
        {topics.length === 0 ? (
          <p className="text-[13px] py-4" style={{ color: '#8d857c' }}>
            No topics match “{topicQuery.trim()}”. <button onClick={() => setTopicQuery('')} className="font-semibold underline" style={{ color: INK }}>Clear</button>
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
            <section key={strand.id} className="mt-7">
              <div className="flex items-center gap-3 mb-1">
                <h3 className="shrink-0 text-[11px] font-bold uppercase tracking-[0.14em]" style={{ color: '#9e9186' }}>{strand.name}</h3>
                <span className="flex-1 h-px" style={{ backgroundColor: '#e7e3de' }} />
              </div>
              <div>
                {ordered.map(t => {
                  const m = masteryMap.get(t.subtopicId);
                  const masteryColor = m ? (m.mastery >= 70 ? '#3A8D5F' : '#F26B1F') : null;
                  const asked = yearSets.get(t.subtopicId) ?? new Set<number>();
                  return (
                    <button
                      key={t.subtopicId}
                      onClick={() => setSubtopicId(t.subtopicId)}
                      className="group w-full flex items-center gap-4 px-1 py-3 text-left transition-colors hover:bg-[#f5f4f2] dark:hover:bg-zinc-800/40"
                      style={{ borderBottom: '1px solid #eeebe6' }}
                    >
                      <span className="flex-1 min-w-0">
                        <span className="block text-[15px] leading-snug" style={{ fontFamily: "'Source Serif 4', serif", color: INK }}>{t.label}</span>
                      </span>
                      {m && masteryColor && (
                        <span className="shrink-0 text-[11px] font-semibold tabular-nums" style={{ color: masteryColor }}>{m.mastery}%</span>
                      )}
                      <span className="shrink-0 w-10 text-right text-[13px] tabular-nums" style={{ color: '#8d857c' }}>{t.count}</span>
                      <span className="shrink-0 hidden sm:flex items-center gap-[2px]" aria-label={`Asked in ${t.years} of ${totalYears} years`}>
                        {stats.years.map(y => (
                          <span
                            key={y}
                            title={String(y)}
                            className="inline-block w-[4px] h-[12px] rounded-[1px] transition-colors"
                            style={{ backgroundColor: asked.has(y) ? '#4a453f' : '#e7e3de' }}
                          />
                        ))}
                      </span>
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

  // ── Level 0: the index — one ruled row per charted subject. ──
  const shownSubjects = (scope === 'mine' ? subjects.filter(s => mineIds.includes(s.id)) : subjects);
  const totalQ = subjects.reduce((a, s) => a + subjectAtlasStats(s.id).questions, 0);
  const scopeTab = (active: boolean) => ({
    color: active ? INK : '#8d857c',
    boxShadow: active ? `inset 0 -2px 0 0 ${INK}` : 'none',
  });
  return (
    <div className="w-full max-w-2xl mx-auto pb-12">
      <button onClick={onBack} className="flex items-center gap-1.5 text-[13px] font-medium mb-5" style={{ color: '#7a7068' }}>
        <ArrowLeft size={15} /> Paper Trail
      </button>
      <h2 ref={headingRef} tabIndex={-1} className="text-[28px] font-semibold mb-1 outline-none text-[#1a1a1a] dark:text-zinc-100" style={{ fontFamily: "'Source Serif 4', serif" }}>
        Topic Atlas
      </h2>
      <p className="text-[14px] leading-relaxed mb-1 max-w-[52ch]" style={{ color: '#5a5550' }}>
        Every question the SEC has asked, mapped by topic.
      </p>
      <p className="text-[12.5px] mb-6 tabular-nums" style={{ color: '#9e9186' }}>
        {subjects.length} subject{subjects.length === 1 ? '' : 's'} charted · {totalQ.toLocaleString()} questions
      </p>
      {subjects.length === 0 ? (
        <p className="text-[13.5px] py-4" style={{ color: '#5a5550' }}>
          The atlas is being charted subject by subject — check back soon.
        </p>
      ) : (
        <>
          {mineIds.length > 0 && (
            <div className="flex items-center gap-4 pb-3 mb-1" role="group" aria-label="Subject scope" style={{ borderBottom: '1px solid #e7e3de' }}>
              {(['mine', 'all'] as const).map(sc => (
                <button key={sc} aria-pressed={scope === sc} onClick={() => setScope(sc)}
                  className="pb-1 text-[13px] font-medium transition-colors" style={scopeTab(scope === sc)}>
                  {sc === 'mine' ? 'My subjects' : 'All subjects'}
                </button>
              ))}
            </div>
          )}
          <div>
            {shownSubjects.map(s => {
              const st = subjectAtlasStats(s.id);
              const peak = Math.max(1, ...st.perYear.values());
              return (
                <button
                  key={s.id}
                  onClick={() => setSubjectId(s.id)}
                  className="group w-full flex items-center gap-4 px-1 py-4 text-left transition-colors hover:bg-[#f5f4f2] dark:hover:bg-zinc-800/40"
                  style={{ borderBottom: '1px solid #eeebe6' }}
                >
                  <span className="flex-1 min-w-0">
                    <span className="block text-[17px]" style={{ fontFamily: "'Source Serif 4', serif", color: INK }}>{s.label}</span>
                    <span className="block text-[12px] mt-0.5 tabular-nums" style={{ color: '#8d857c' }}>
                      {st.questions.toLocaleString()} questions · {topicsForSubject(s.id).length} topics · {st.yearMin}–{st.yearMax}
                    </span>
                  </span>
                  <span className="shrink-0 hidden sm:flex items-end gap-[2px] h-[24px]" aria-hidden="true">
                    {st.years.map(y => (
                      <span
                        key={y}
                        title={`${y}: ${st.perYear.get(y) ?? 0} questions`}
                        className="inline-block w-[5px] rounded-[1px]"
                        style={{
                          height: `${Math.max(14, Math.round(((st.perYear.get(y) ?? 0) / peak) * 100))}%`,
                          backgroundColor: '#d8d3cc',
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
