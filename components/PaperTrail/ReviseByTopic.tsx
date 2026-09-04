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
import { ArrowLeft, ChevronDown as ChevronDownIcon, Download, Search, X, Link2, Check as CheckIcon } from 'lucide-react';
import { categoryOf, siblingsFor, strandsFor, subjectAtlasStats, taggedYearsForSubject, topicLabel, topicsForSubject, topicYearSets, type SubjectTopic, type TopicSibling } from './topics';
import { addCard, hasCard, removeCard } from './reviewStore';
import { masteryForSubject, type TopicMastery } from './topicMastery';
import { downloadPack } from './revisionPack';
import VaultQuestionCard from './VaultQuestionCard';
import { releaseVaultPdfs } from './vaultDocs';
import { buildVaultLink, consumeInitialVaultLocation } from './vaultDeepLink';

const INK = '#1a1a1a';
const LVL: Record<string, string> = { higher: 'HL', ordinary: 'OL', foundation: 'FL', common: 'CL' };
const CATEGORY_TINT: Record<string, { bg: string; ink: string }> = {
  stem: { bg: '#E8F1F5', ink: '#33658A' },
  language: { bg: '#EFEAF3', ink: '#5B4A7E' },
  business: { bg: '#F6EEDF', ink: '#8A6B2D' },
  'social-environmental': { bg: '#E8F2EC', ink: '#1F5F3E' },
  'practical-applied': { bg: '#ECEFF0', ink: '#46555E' },
  arts: { bg: '#F6EAED', ink: '#84495A' },
  other: { bg: '#F0EEEB', ink: '#6B635A' },
};
// Curriculum sections of the index, in reading order. The tint appears only
// as the small dot beside each section eyebrow — rows stay white and ruled.
const CATEGORY_ORDER = ['stem', 'language', 'business', 'social-environmental', 'practical-applied', 'arts', 'other'] as const;
// Segmented controls — copied from the iOS/Copilot register: a soft tray,
// the selected option raised on a white pill. Sleek, clickable, obvious.
const SEG_TRAY = 'inline-flex items-center gap-0.5 rounded-[10px] bg-[#F1EFEC] p-[3px] dark:bg-zinc-800';
const segBtn = (active: boolean) =>
  `rounded-[8px] px-3 py-[5px] text-[12.5px] font-semibold transition-colors ${
    active
      ? 'bg-white text-[#1a1a1a] shadow-[0_1px_2px_rgba(26,23,20,0.10)] dark:bg-zinc-600 dark:text-white'
      : 'text-[#8d857c] hover:text-[#57534e] dark:text-zinc-400 dark:hover:text-zinc-200'
  }`;

const CATEGORY_LABEL: Record<string, string> = {
  stem: 'Sciences & Maths',
  language: 'Languages',
  business: 'Business',
  'social-environmental': 'Social & Environmental',
  'practical-applied': 'Practical & Applied',
  arts: 'Arts',
  other: 'Other subjects',
};

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
    return (
      <div className="w-full max-w-2xl mx-auto pb-12">
        <button onClick={() => setSubtopicId(null)} className="flex items-center gap-1.5 text-[13px] font-medium mb-5" style={{ color: '#7a7068' }}>
          <ArrowLeft size={15} /> {subjectLabel(subjectId)}
        </button>
        <p className="mb-1 text-[10px] font-bold uppercase tracking-[0.15em]" style={{ color: (CATEGORY_TINT[categoryOf(subjectId) as string] ?? CATEGORY_TINT.other).ink }}>
          {subjectLabel(subjectId)} · {CATEGORY_LABEL[categoryOf(subjectId) as string] ?? 'Topic Atlas'}
        </p>
        <h2 ref={headingRef} tabIndex={-1} className="text-[26px] font-semibold mb-1 outline-none text-[#1a1a1a] dark:text-zinc-100" style={{ fontFamily: "'Source Serif 4', serif" }}>{topicLabel(subtopicId)}</h2>
        <p aria-live="polite" className="text-[13px] mb-5 tabular-nums" style={{ color: '#8d857c' }}>
          {shown.length === questions.length
            ? <>{questions.length} question{questions.length === 1 ? '' : 's'} · {years.size} year{years.size === 1 ? '' : 's'} · marking scheme beneath each</>
            : <>{shown.length} of {questions.length} questions{yearFilter !== 'all' ? ` · ${yearFilter}` : ''}{levelFilter !== 'all' ? ` · ${LVL[levelFilter] ?? levelFilter}` : ''}</>}
        </p>

        <div className="flex items-center gap-x-5 gap-y-3 flex-wrap pb-3 mb-6" style={{ borderBottom: '1px solid #e7e3de' }}>
          {levels.length > 1 && (
            <div className={SEG_TRAY} role="group" aria-label="Level">
              {(['all', ...levels] as const).map(l => (
                <button key={l} aria-pressed={levelFilter === l} onClick={() => setLevelFilter(l)}
                  className={segBtn(levelFilter === l)}>
                  {l === 'all' ? 'All levels' : LVL[l] ?? l}
                  <span className="ml-1 tabular-nums font-medium" style={{ color: '#b3aca3' }}>{levelCount(l)}</span>
                </button>
              ))}
            </div>
          )}
          {hasIrish && (
            <div className={SEG_TRAY} role="group" aria-label="Language">
              {(['ev', 'iv'] as const).map(l => (
                <button key={l} aria-pressed={langPref === l} onClick={() => pickLang(l)}
                  className={segBtn(langPref === l)}>
                  {l === 'ev' ? 'English' : 'Gaeilge'}
                </button>
              ))}
            </div>
          )}
          {yearList.length > 3 && (
            <div className="relative">
              <select
                value={yearFilter === 'all' ? 'all' : String(yearFilter)}
                onChange={e => setYearFilter(e.target.value === 'all' ? 'all' : Number(e.target.value))}
                aria-label="Year"
                className={`appearance-none cursor-pointer rounded-[10px] py-[8px] pl-3 pr-8 text-[12.5px] font-semibold outline-none transition-colors ${
                  yearFilter === 'all'
                    ? 'bg-[#F1EFEC] text-[#8d857c] hover:text-[#57534e] dark:bg-zinc-800 dark:text-zinc-400'
                    : 'bg-white text-[#1a1a1a] shadow-[0_1px_2px_rgba(26,23,20,0.10)] ring-1 ring-[#E5E1DA] dark:bg-zinc-600 dark:text-white dark:ring-zinc-600'
                }`}
              >
                <option value="all">All years</option>
                {yearList.map(y => <option key={y} value={y}>{y}</option>)}
              </select>
              <ChevronDownIcon size={14} aria-hidden="true" className="pointer-events-none absolute right-2.5 top-1/2 -translate-y-1/2" style={{ color: '#8d857c' }} />
            </div>
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
    return (
      <div className="w-full max-w-2xl mx-auto pb-12">
        <button onClick={() => setSubjectId(null)} className="flex items-center gap-1.5 text-[13px] font-medium mb-5" style={{ color: '#7a7068' }}>
          <ArrowLeft size={15} /> All subjects
        </button>
        {/* The volume's title page — the category duotone carries the
            subject's full sixteen-year signature above its contents. */}
        {(() => {
          const tint = CATEGORY_TINT[categoryOf(subjectId) as string] ?? CATEGORY_TINT.other;
          const peak = Math.max(1, ...stats.perYear.values());
          return (
            <div className="rounded-2xl overflow-hidden mb-5" style={{ border: '1.5px solid #383838' }}>
              <div className="px-6 pt-5 pb-5" style={{ backgroundColor: tint.bg }}>
                <p className="text-[10px] font-bold uppercase tracking-[0.15em]" style={{ color: tint.ink }}>
                  {CATEGORY_LABEL[categoryOf(subjectId) as string] ?? 'Charted subject'} · Topic Atlas
                </p>
                <h2 ref={headingRef} tabIndex={-1} className="mt-1.5 text-[27px] font-semibold outline-none" style={{ fontFamily: "'Source Serif 4', serif", color: INK }}>{subjectLabel(subjectId)}</h2>
                <div className="mt-4 flex items-end gap-[4px] h-[44px]" aria-hidden="true">
                  {stats.years.map(y => (
                    <span
                      key={y}
                      title={`${y}: ${stats.perYear.get(y) ?? 0} questions`}
                      className="flex-1 rounded-[2px]"
                      style={{
                        maxWidth: 20,
                        height: `${Math.max(10, Math.round(((stats.perYear.get(y) ?? 0) / peak) * 100))}%`,
                        backgroundColor: tint.ink,
                        opacity: 0.34,
                      }}
                    />
                  ))}
                </div>
                <p className="mt-3 text-[12.5px] font-semibold tabular-nums" style={{ color: tint.ink }}>
                  {stats.questions.toLocaleString()} questions · {baseTopics.length} topics · {stats.yearMin}–{stats.yearMax}
                </p>
              </div>
            </div>
          );
        })()}
        <p className="text-[13.5px] mb-4" style={{ color: '#5a5550' }}>
          Pick a topic — every question ever asked on it is inside.
        </p>
        <div className="flex items-center gap-x-5 gap-y-3 flex-wrap pb-3 mb-2" style={{ borderBottom: '1px solid #e7e3de' }}>
          <div className={SEG_TRAY} role="group" aria-label="Sort topics">
            {(['busiest', 'frequent'] as const).map(s => (
              <button key={s} aria-pressed={sort === s} onClick={() => setSort(s)}
                className={segBtn(sort === s)}>
                {s === 'busiest' ? 'Most asked' : 'Most recurrent'}
              </button>
            ))}
          </div>
          <span className="flex-1" />
          {sortedTopics.length > 8 && (
            <div className="relative">
              <Search size={14} className="absolute left-2.5 top-1/2 -translate-y-1/2 pointer-events-none" style={{ color: '#a8a29e' }} />
              <input
                type="text"
                value={topicQuery}
                onChange={e => setTopicQuery(e.target.value)}
                placeholder="Search topics"
                aria-label="Search topics"
                className="w-48 appearance-none rounded-[10px] bg-[#F1EFEC] py-[8px] pl-8 pr-8 text-[13px] outline-none transition-shadow placeholder:text-[#a8a29e] focus:ring-2 focus:ring-[rgba(242,107,31,0.28)] dark:bg-zinc-800 dark:text-zinc-100"
                style={{ color: INK }}
              />
              {topicQuery && (
                <button onClick={() => setTopicQuery('')} aria-label="Clear search"
                  className="absolute right-2.5 top-1/2 -translate-y-1/2" style={{ color: '#a8a29e' }}>
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
        ) : (() => {
          // Contents numbering runs continuously through the whole volume,
          // so the strand sections read like chapters of one book.
          const orderedByStrand = strands
            .map(strand => {
              const strandTopics = strand.subtopicIds
                .map(id => topicById.get(id))
                .filter((t): t is SubjectTopic => !!t);
              const ordered = [...strandTopics].sort((a, b) =>
                sort === 'busiest'
                  ? b.count - a.count || b.years - a.years || a.label.localeCompare(b.label)
                  : b.years - a.years || b.count - a.count || a.label.localeCompare(b.label));
              return { strand, ordered };
            })
            .filter(entry => entry.ordered.length > 0);
          const contentsNo = new Map<string, number>();
          let running = 0;
          for (const entry of orderedByStrand) for (const t of entry.ordered) contentsNo.set(t.subtopicId, ++running);
          return orderedByStrand.map(({ strand, ordered }) => (
            <section key={strand.id} className="mt-7">
              <div className="flex items-center gap-3 mb-1">
                <h3 className="shrink-0 text-[11px] font-bold uppercase tracking-[0.14em]" style={{ color: '#9e9186' }}>{strand.name}</h3>
                <span className="flex-1 h-px" style={{ backgroundColor: '#e7e3de' }} />
                <span className="shrink-0 text-[12px] tabular-nums" style={{ color: '#b3aca3' }}>
                  {ordered.reduce((a, t) => a + t.count, 0).toLocaleString()} q
                </span>
              </div>
              <div className="space-y-2">
                {ordered.map(t => {
                  const m = masteryMap.get(t.subtopicId);
                  const masteryColor = m ? (m.mastery >= 70 ? '#3A8D5F' : '#F26B1F') : null;
                  const asked = yearSets.get(t.subtopicId) ?? new Set<number>();
                  return (
                    <button
                      key={t.subtopicId}
                      onClick={() => setSubtopicId(t.subtopicId)}
                      className="group w-full flex items-center gap-3.5 rounded-xl border border-[#E5E1DA] bg-white px-4 py-3 text-left transition-all duration-150 hover:-translate-y-[1px] hover:border-[#383838] dark:border-zinc-700 dark:bg-zinc-900 dark:hover:border-zinc-400"
                    >
                      <span aria-hidden="true" className="w-6 shrink-0 text-right text-[13px] tabular-nums" style={{ fontFamily: "'Source Serif 4', serif", color: '#b3aca3' }}>
                        {String(contentsNo.get(t.subtopicId) ?? 0).padStart(2, '0')}
                      </span>
                      <span className="flex-1 min-w-0">
                        <span className="block text-[15.5px] leading-snug" style={{ fontFamily: "'Source Serif 4', serif", color: INK }}>{t.label}</span>
                        <span className="block sm:hidden text-[11.5px] mt-0.5 tabular-nums" style={{ color: '#9e9186' }}>{t.count} questions · {t.years} of {totalYears} years</span>
                      </span>
                      {masteryMap.size > 0 && (
                        <span className="shrink-0 w-10 text-right text-[11px] font-semibold tabular-nums" style={{ color: masteryColor ?? '#d8d3cc' }}>
                          {m ? `${m.mastery}%` : ''}
                        </span>
                      )}
                      <span className="shrink-0 w-10 text-right text-[13px] tabular-nums" style={{ color: '#8d857c' }}>{t.count}</span>
                      <span className="shrink-0 hidden sm:flex items-center gap-[2px]" aria-label={`Asked in ${t.years} of ${totalYears} years`}>
                        {stats.years.map(y => (
                          <span
                            key={y}
                            title={String(y)}
                            className="inline-block w-[4.5px] h-[13px] rounded-[2px] transition-colors"
                            style={{ backgroundColor: asked.has(y) ? 'rgba(242,107,31,0.55)' : '#ece8e3' }}
                          />
                        ))}
                      </span>
                    </button>
                  );
                })}
              </div>
            </section>
          ));
        })()}
      </div>
    );
  }

  // ── Level 0: the index — curriculum sections, one ruled row per subject.
  //    Structure and data carry the page; no decoration repeats per row. ──
  const shownSubjects = (scope === 'mine' ? subjects.filter(s => mineIds.includes(s.id)) : subjects);
  const totalQ = subjects.reduce((a, s) => a + subjectAtlasStats(s.id).questions, 0);
  const totalTopics = subjects.reduce((a, s) => a + topicsForSubject(s.id).length, 0);
  const span = subjects.reduce(
    (acc, s) => { const st = subjectAtlasStats(s.id); return { lo: Math.min(acc.lo, st.yearMin), hi: Math.max(acc.hi, st.yearMax) }; },
    { lo: Infinity, hi: 0 },
  );
  const grouped = CATEGORY_ORDER
    .map(cat => ({ cat, items: shownSubjects.filter(s => (categoryOf(s.id) as string) === cat) }))
    .filter(g => g.items.length > 0);
  return (
    <div className="w-full max-w-2xl mx-auto pb-12">
      <button onClick={onBack} className="flex items-center gap-1.5 text-[13px] font-medium mb-5" style={{ color: '#7a7068' }}>
        <ArrowLeft size={15} /> Paper Trail
      </button>
      <h2 ref={headingRef} tabIndex={-1} className="text-[28px] font-semibold mb-1 outline-none text-[#1a1a1a] dark:text-zinc-100" style={{ fontFamily: "'Source Serif 4', serif" }}>
        Topic Atlas
      </h2>
      <p className="text-[14px] leading-relaxed mb-5 max-w-[52ch]" style={{ color: '#5a5550' }}>
        Every question the SEC has asked, mapped by topic.
      </p>
      {subjects.length === 0 ? (
        <p className="text-[13.5px] py-4" style={{ color: '#5a5550' }}>
          The atlas is being charted subject by subject — check back soon.
        </p>
      ) : (
        <>
          {/* The record, stated once — cells divided by hairlines. */}
          <div className="grid grid-cols-3 sm:grid-cols-4 mb-6 py-3.5" style={{ borderTop: '1px solid #e7e3de', borderBottom: '1px solid #e7e3de' }}>
            {[
              { v: subjects.length.toLocaleString(), l: subjects.length === 1 ? 'Subject' : 'Subjects' },
              { v: totalTopics.toLocaleString(), l: 'Topics' },
              { v: totalQ.toLocaleString(), l: 'Questions' },
              { v: span.lo <= span.hi ? `${span.lo}–${span.hi}` : '—', l: 'Years', wide: true },
            ].map((cell, i) => (
              <div key={cell.l} className={`${i > 0 ? 'pl-4 sm:pl-5' : ''} ${cell.wide ? 'hidden sm:block' : ''}`} style={i > 0 ? { borderLeft: '1px solid #eeebe6' } : undefined}>
                <p className="text-[19px] font-semibold tabular-nums leading-tight" style={{ fontFamily: "'Source Serif 4', serif", color: INK }}>{cell.v}</p>
                <p className="text-[9.5px] font-bold uppercase tracking-[0.14em] mt-0.5" style={{ color: '#9e9186' }}>{cell.l}</p>
              </div>
            ))}
          </div>
          {mineIds.length > 0 && (
            <div className={`${SEG_TRAY} mb-2`} role="group" aria-label="Subject scope">
              {(['mine', 'all'] as const).map(sc => (
                <button key={sc} aria-pressed={scope === sc} onClick={() => setScope(sc)}
                  className={segBtn(scope === sc)}>
                  {sc === 'mine' ? 'My subjects' : 'All subjects'}
                </button>
              ))}
            </div>
          )}
          {grouped.map(group => {
            const tint = CATEGORY_TINT[group.cat] ?? CATEGORY_TINT.other;
            return (
            <section key={group.cat} className="mt-7">
              <div className="flex items-center gap-2.5 mb-3">
                <span aria-hidden="true" className="inline-block w-[7px] h-[7px] rounded-full shrink-0" style={{ backgroundColor: tint.ink }} />
                <h3 className="shrink-0 text-[11px] font-bold uppercase tracking-[0.14em]" style={{ color: '#9e9186' }}>{CATEGORY_LABEL[group.cat] ?? 'Other subjects'}</h3>
                <span className="flex-1 h-px" style={{ backgroundColor: '#e7e3de' }} />
                <span className="shrink-0 text-[12px] tabular-nums" style={{ color: '#b3aca3' }}>{group.items.length}</span>
              </div>
              {/* Each subject is a volume: a duotone cover carrying its own
                  sixteen-year signature, a white spine of type below. */}
              <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
                {group.items.map(s => {
                  const st = subjectAtlasStats(s.id);
                  const peak = Math.max(1, ...st.perYear.values());
                  return (
                    <button
                      key={s.id}
                      onClick={() => setSubjectId(s.id)}
                      aria-label={`${s.label} — ${st.questions.toLocaleString()} questions across ${topicsForSubject(s.id).length} topics, ${st.yearMin} to ${st.yearMax}`}
                      className="group text-left rounded-2xl overflow-hidden bg-white dark:bg-zinc-900 transition-transform duration-200 hover:-translate-y-0.5"
                      style={{ border: '1.5px solid #383838' }}
                    >
                      <span className="block px-5 pt-3.5 pb-3" style={{ backgroundColor: tint.bg }}>
                        <span className="flex items-baseline justify-between gap-3">
                          <span className="text-[9.5px] font-bold uppercase tracking-[0.15em]" style={{ color: tint.ink }}>
                            {st.questions.toLocaleString()} questions
                          </span>
                          <span className="text-[10.5px] font-semibold tabular-nums" style={{ color: tint.ink, opacity: 0.72 }}>{st.yearMin}–{st.yearMax}</span>
                        </span>
                        <span className="mt-2.5 flex items-end gap-[3px] h-[34px]" aria-hidden="true">
                          {st.years.map(y => (
                            <span
                              key={y}
                              title={`${y}: ${st.perYear.get(y) ?? 0} questions`}
                              className="flex-1 rounded-[2px] transition-opacity duration-200 group-hover:opacity-60"
                              style={{
                                height: `${Math.max(12, Math.round(((st.perYear.get(y) ?? 0) / peak) * 100))}%`,
                                backgroundColor: tint.ink,
                                opacity: 0.34,
                              }}
                            />
                          ))}
                        </span>
                      </span>
                      <span className="block px-5 pt-3.5 pb-4">
                        <span className="block text-[19px] leading-snug" style={{ fontFamily: "'Source Serif 4', serif", color: INK }}>{s.label}</span>
                        <span className="mt-1 block text-[12.5px] tabular-nums" style={{ color: '#8d857c' }}>
                          {topicsForSubject(s.id).length} topics mapped
                        </span>
                      </span>
                    </button>
                  );
                })}
              </div>
            </section>
            );
          })}
        </>
      )}
    </div>
  );
};

export default ReviseByTopic;
