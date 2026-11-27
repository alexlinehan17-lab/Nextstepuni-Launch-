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

import SubjectPicker from '../launchpad/SubjectPicker';
import { useSubjectAccess } from '../launchpad/SubjectAccess';
import { usePulse } from '../../hooks/usePulse';
import React, { useEffect, useMemo, useRef, useState } from 'react';
import { ArrowLeft, ChevronRight, Ellipsis } from 'lucide-react';
import { categoryOf, logicalQuestionIdentity, siblingsFor, strandsFor, subjectAtlasStats, taggedYearsForSubject, topicLabel, topicsForSubject, topicYearSets, type SubjectTopic, type TopicSibling } from './topics';
import { addCard, hasCard, removeCard } from './reviewStore';
import { masteryForSubject, type TopicMastery } from './topicMastery';
import { downloadPack } from './revisionPack';
import VaultQuestionCard from './VaultQuestionCard';
import HorizontalTabs from '../ui/HorizontalTabs';
import { Button, TextButton } from '../ui/Button';
import { SelectionBar } from '../ui/Choice';
import { Menu, MenuAction, MenuPanel } from '../ui/Menu';
import { SearchField } from '../ui/Field';
import { showMessage } from '../ui/Message';
import { useBackStep } from '../../contexts/NavigationContext';
import { PaperSubjectArtwork } from './PaperSubjects';
import './atlas.css';
import { releaseVaultPdfs } from './vaultDocs';
import { buildVaultLink, consumeInitialVaultLocation, initialVaultFocus } from './vaultDeepLink';
import { examTopicTaxonomyFor } from '../../data/examTopics/registry';
import { isModelLoaded, isModelSubject, loadAtlasModel } from './atlasModel';

const PoliticsTopicFeed = React.lazy(() => import('./PoliticsTopicFeed'));

/** The levels a subject's topic headings can be filed under, in reading order. */
const LEVEL_KEYS = ['higher', 'ordinary', 'foundation', 'common'] as const;
const LEVEL_WORD: Record<string, string> = { higher: 'Higher', ordinary: 'Ordinary', foundation: 'Foundation', common: 'Common' };

/** A small mark per year, inked when the topic came up (the laptop's marks, now on the phone too, in ink). */
const YearMarks: React.FC<{ years: number[]; asked: Set<number>; label: string; large?: boolean }> = ({ years, asked, label, large = false }) => (
  <span className={`ta-marks${large ? ' ta-marks--lg' : ''}`} role="img" aria-label={label} style={{ '--ta-n': years.length } as React.CSSProperties}>
    {years.map(y => <i key={y} className={asked.has(y) ? 'on' : undefined} />)}
  </span>
);
/** The first, middle and last year under a large row of marks. */
const YearAxis: React.FC<{ years: number[] }> = ({ years }) => (
  <span className="ta-axis" aria-hidden="true">
    <span className="ui-readout">{years[0]}</span>
    {years.length > 2 && <span className="ui-readout">{years[Math.floor((years.length - 1) / 2)]}</span>}
    <span className="ui-readout">{years[years.length - 1]}</span>
  </span>
);

const INK = '#1a1a1a';
const LVL: Record<string, string> = { higher: 'HL', ordinary: 'OL', foundation: 'FL', common: 'CL' };
const CATEGORY_TINT: Record<string, { bg: string; ink: string }> = {
  stem: { bg: '#E8F1F5', ink: '#33658A' },
  language: { bg: '#EFEAF3', ink: '#5B4A7E' },
  business: { bg: '#F6EEDF', ink: '#8A6B2D' },
  'social-environmental': { bg: '#E8F2EC', ink: '#1F5F3E' },
  'practical-applied': { bg: '#ECEFF0', ink: '#46555E' },
  arts: { bg: '#F6EAED', ink: '#84495A' },
  other: { bg: 'var(--surface-soft)', ink: '#6B635A' },
};
// Curriculum sections of the index, in reading order. The tint appears only
// as the small dot beside each section eyebrow — rows stay white and ruled.
const CATEGORY_ORDER = ['stem', 'language', 'business', 'social-environmental', 'practical-applied', 'arts', 'other'] as const;

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
  restore?: { subjectId: string; subtopicId: string; level?: string };
  onOpenQuestion: (t: TopicSibling, origin: { subjectId: string; subtopicId: string; level?: string }) => void;
  onBack: () => void;
}

const ReviseByTopic: React.FC<Props> = ({ subjects, mineIds, uid, subjectLabel, restore, onOpenQuestion, onBack }) => {
  // A shared "?subject=…&topic=…" link opens the vault straight at that topic
  // (consumed once per load — see vaultDeepLink; safe, never touches history).
  const [boot] = useState(() => consumeInitialVaultLocation());
  const canSelectSubject = useSubjectAccess();
  const [scope, setScope] = useState<'mine' | 'all'>(mineIds.length ? 'mine' : 'all');
  const [subjectId, setSubjectState] = useState<string | null>(() => {
    let saved = '';
    try { saved = localStorage.getItem(`atlas.subject:${uid ?? 'guest'}`) ?? ''; } catch { /* private mode */ }
    const candidates = [restore?.subjectId, boot?.subjectId, saved, ...mineIds, ...subjects.map(s => s.id)];
    return candidates.find(id => id && subjects.some(s => s.id === id && canSelectSubject(s.label))) ?? null;
  });
  const setSubjectId = (id: string) => {
    const selected = subjects.find(s => s.id === id);
    if (selected && canSelectSubject(selected.label)) setSubjectState(id);
  };
  const [previewId, setPreviewId] = useState<string | null>(null);
  useEffect(() => { if (subjectId) {try {localStorage.setItem(`atlas.subject:${uid ?? 'guest'}`,subjectId);} catch { /* private mode */ }} setPreviewId(null); },[subjectId,uid]);
  const [subtopicId, setSubtopicId] = useState<string | null>(restore?.subjectId === subjectId ? restore.subtopicId : boot?.subjectId === subjectId ? boot.subtopicId ?? null : null);
  const [copied, pulseCopied, clearCopied] = usePulse(2000);
  const [sort, setSort] = useState<'reference' | 'busiest' | 'frequent'>('busiest');
  // A card's "Topic Atlas" link (atlasModel.atlasLinkForCard) also names its question: open the topic on that
  // question's year and level.
  const [focus] = useState(() => (boot ? initialVaultFocus() : null));
  const [levelFilter, setLevelFilter] = useState<'all' | string>(restore?.subjectId === subjectId ? restore.level ?? 'all' : focus?.level ?? 'all');
  const [yearFilter, setYearFilter] = useState<'all' | number>(focus?.year ?? 'all');
  const [topicQuery, setTopicQuery] = useState('');
  const [politicsView, setPoliticsView] = useState<'tasks' | 'papers'>('tasks');
  const [revVer, setRevVer] = useState(0); // bump to re-read review-deck membership
  // The level chosen on the topic map, where the subject files its topics by level.
  const [mapLevel, setMapLevel] = useState<string | null>(null);
  // Which questions showed as a printed picture and which as a row into the full paper.
  const [kinds, setKinds] = useState<Record<string, 'row' | 'printed'>>({});
  // A topic is a step of the map: the bar's one Back returns to the map first.
  useBackStep(Boolean(subjectId && subtopicId), () => setSubtopicId(null));
  // A subject picker in a tool lists the student's own subjects (Alex, 26 Nov 2026), and the one open.
  const pickerSubjects = mineIds.length ? subjects.filter(s => mineIds.includes(s.id) || s.id === subjectId) : subjects;
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
  const focusUsed = useRef(false);
  useEffect(() => {
    if (!focusUsed.current && focus && boot?.subjectId === subjectId && boot?.subtopicId === subtopicId) {
      focusUsed.current = true;
      setLevelFilter(focus.level ?? 'all');
      setYearFilter(focus.year ?? 'all');
      return;
    }
    setLevelFilter(restore?.subjectId === subjectId && restore?.subtopicId === subtopicId ? restore.level ?? 'all' : 'all');
    setYearFilter('all');
  }, [subtopicId, subjectId, restore?.subjectId, restore?.subtopicId, restore?.level]);
  // Reset the topic search when switching subjects.
  useEffect(() => { setTopicQuery(''); }, [subjectId]);
  // Audited exam taxonomies have a deliberate reference order. Canonical
  // syllabus taxonomies retain the Atlas's existing busiest-first default.
  useEffect(() => {
    setSort(subjectId && examTopicTaxonomyFor(subjectId) ? 'reference' : 'busiest');
  }, [subjectId]);
  // The "Copied" confirmation is per-topic.
  useEffect(() => { clearCopied(); }, [subtopicId, clearCopied]);

  const copyTopicLink = async () => {
    if (!subjectId || !subtopicId) return;
    const url = buildVaultLink(subjectId, subtopicId);
    try {
      await navigator.clipboard.writeText(url);
      pulseCopied();
      showMessage('Copied');
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

  // The single model: a subject's filing (which part sits under which heading) loads when the subject opens.
  const [modelReady, setModelReady] = useState(0);
  const modelPending = Boolean(subjectId && isModelSubject(subjectId) && !isModelLoaded(subjectId));
  useEffect(() => {
    if (!subjectId || !isModelSubject(subjectId) || isModelLoaded(subjectId)) return;
    let live = true;
    loadAtlasModel(subjectId).then(() => { if (live) setModelReady(v => v + 1); });
    return () => { live = false; };
  }, [subjectId]);

  // Per-topic mastery for the chosen subject (accuracy + FSRS retention).
  const masteryMap = useMemo(() => {
    void revVer; // recompute after adding cards changes retention signals
    void modelReady;
    const m = new Map<string, TopicMastery>();
    if (subjectId) for (const t of masteryForSubject(uid, subjectId)) m.set(t.subtopicId, t);
    return m;
  }, [subjectId, uid, revVer, modelReady]);

  const baseTopics: SubjectTopic[] = useMemo(() => { void modelReady; return subjectId ? topicsForSubject(subjectId) : []; }, [subjectId, modelReady]);
  const totalYears = useMemo(() => (subjectId ? taggedYearsForSubject(subjectId) : 0), [subjectId]);
  const sortedTopics: SubjectTopic[] = useMemo(() => {
    if (sort === 'busiest') return baseTopics; // already count-sorted
    if (sort === 'reference' && subjectId) {
      const taxonomy = examTopicTaxonomyFor(subjectId);
      const order = new Map(
        taxonomy?.groups.flatMap(group => group.topicIds).map((id, index) => [id, index]) ?? [],
      );
      return [...baseTopics].sort((a, b) =>
        (order.get(a.subtopicId) ?? Number.MAX_SAFE_INTEGER) -
        (order.get(b.subtopicId) ?? Number.MAX_SAFE_INTEGER));
    }
    return [...baseTopics].sort((a, b) => b.years - a.years || b.count - a.count || a.label.localeCompare(b.label));
  }, [baseTopics, sort, subjectId]);
  // Type-to-filter topics — subjects like Geography carry 40+ topics.
  const topics: SubjectTopic[] = useMemo(() => {
    const q = topicQuery.trim().toLowerCase();
    if (!q) return sortedTopics;
    return sortedTopics.filter(t => t.label.toLowerCase().includes(q));
  }, [sortedTopics, topicQuery]);
  const allEditions = useMemo(
    () => { void modelReady; return subjectId && subtopicId ? siblingsFor(subjectId, subtopicId) : []; },
    [subjectId, subtopicId, modelReady],
  );
  const hasIrish = useMemo(() => allEditions.some(q => q.lang === 'iv'), [allEditions]);
  // One edition per printed question: the preferred language where it exists,
  // the other edition otherwise (an Irish-only sitting still shows under
  // English, marked as Gaeilge on the card).
  const questions = useMemo(() => {
    const byQ = new Map<string, TopicSibling>();
    for (const q of allEditions) {
      const key = logicalQuestionIdentity(q);
      const cur = byQ.get(key);
      if (!cur || (cur.lang !== langPref && q.lang === langPref)) byQ.set(key, q);
    }
    return [...byQ.values()].sort((a, b) => b.year - a.year || a.level.localeCompare(b.level) || a.n.localeCompare(b.n, undefined, { numeric: true }));
  }, [allEditions, langPref]);

  if (modelPending) {
    return <div className="w-full max-w-2xl mx-auto pb-12"><p role="status" className="text-[13px] py-6" style={{ color: '#7a7068' }}>Loading this subject’s topics…</p></div>;
  }

  if (subjectId === 'politics-and-society' && subtopicId && politicsView === 'tasks') {
    return <div className="w-full max-w-2xl mx-auto pb-12">
      <p className="t-label">Politics and Society</p>
      <h2 ref={headingRef} tabIndex={-1} className="mb-3 t-title outline-none">{topicLabel(subtopicId)}</h2>
      <Button className="mb-5" onClick={() => setPoliticsView('papers')}>Browse full printed questions</Button>
      <React.Suspense fallback={<p role="status">Loading practice tasks…</p>}>
        <PoliticsTopicFeed key={subtopicId} topicId={subtopicId} />
      </React.Suspense>
    </div>;
  }

  // ── Level 2: the topic (c-tools2-atlas "One topic", r5-topic-atlas): the
  //    subject and level over the topic's name, its record said once with its
  //    year marks, then its questions grouped by year, newest first. A question
  //    that can show as a picture keeps the printed paper; one that cannot yet
  //    is a plain row into the full paper. ──
  if (subjectId && subtopicId) {
    const years = new Set(questions.map(q => q.year));
    const referenceEntries = examTopicTaxonomyFor(subjectId)?.topics
      .find(topic => topic.id === subtopicId)?.officialQuestionKeys.length ?? 0;
    const referenceOnly = questions.length === 0 && referenceEntries > 0;
    const levels = [...new Set(questions.map(q => q.level))];
    const yearList = [...years].sort((a, b) => b - a);
    const inYear = yearFilter === 'all' ? questions : questions.filter(q => q.year === yearFilter);
    const shown = levelFilter === 'all' ? inYear : inYear.filter(q => q.level === levelFilter);
    const levelCount = (l: string) => (l === 'all' ? inYear.length : inYear.filter(q => q.level === l).length);
    const stats = subjectAtlasStats(subjectId);
    const shownYears = [...new Set(shown.map(q => q.year))].sort((a, b) => b - a);
    // The level, where every question on the topic is set at one (a subject filed by level).
    const eyebrowLevel = levels.length === 1 && LEVEL_WORD[levels[0]] ? LEVEL_WORD[levels[0]] : null;
    return (
      <div className="ta-feed w-full pb-12">
        <header className="ta-top ta-topic-head">
          <div className="ta-topic-copy">
            <p className="t-label">{subjectLabel(subjectId)} · {eyebrowLevel ?? CATEGORY_LABEL[categoryOf(subjectId) as string] ?? 'Topic Atlas'}</p>
            <h2 ref={headingRef} tabIndex={-1} className="t-title outline-none">{topicLabel(subtopicId)}</h2>
            {referenceOnly ? (
              <p aria-live="polite" className="t-sub">
                {referenceEntries} reference entr{referenceEntries === 1 ? 'y' : 'ies'} · official source files pending
              </p>
            ) : shown.length === questions.length ? (
              <p className="t-sub ta-record" aria-label={`${questions.length} questions across ${years.size} years, marking scheme beneath each`}>
                <b>{questions.length} {questions.length === 1 ? 'question' : 'questions'}</b>, asked in <b>{years.size} of the last {totalYears} years</b>
                {levels.length > 1 ? <> · {levels.map(l => LVL[l] ?? l).join(' · ')}</> : null}
              </p>
            ) : (
              <p aria-live="polite" className="t-sub">
                {shown.length} of {questions.length} questions{yearFilter !== 'all' ? ` · ${yearFilter}` : ''}{levelFilter !== 'all' ? ` · ${LVL[levelFilter] ?? levelFilter}` : ''}
              </p>
            )}
          </div>
          {stats.years.length > 0 && <div className="ta-head-years">
            <YearMarks large years={stats.years} asked={years} label={`Asked in ${years.size} of the ${stats.years.length} years from ${stats.yearMin} to ${stats.yearMax}`} />
            <YearAxis years={stats.years} />
          </div>}
        </header>

        <div className="ta-filterrow">
          {levels.length > 1 && (
            <SelectionBar label="Level" size="md" className="ta-seg" value={levelFilter} onChange={l => setLevelFilter(l)}
              options={['all', ...levels].map(l => ({ value: l, label: `${l === 'all' ? 'All levels' : LVL[l] ?? l} ${levelCount(l)}` }))} />
          )}
          {hasIrish && (
            <SelectionBar label="Language" size="md" className="ta-seg" value={langPref} onChange={pickLang}
              options={[{ value: 'ev' as const, label: 'English' }, { value: 'iv' as const, label: 'Gaeilge' }]} />
          )}
          {yearList.length > 3 && (
            <Menu label="Year" value={yearFilter === 'all' ? 'all' : String(yearFilter)} onChange={v => setYearFilter(v === 'all' ? 'all' : Number(v))}
              options={[{ value: 'all', label: 'All years' }, ...yearList.map(y => ({ value: String(y), label: String(y) }))]} />
          )}
          <span className="ta-filter-gap" />
          <MenuPanel label="Export or share" buttonLabel="Export or share this topic" className="ta-more"
            face={<Ellipsis className="ui-icon" width={20} height={20} strokeWidth={1.75} aria-hidden="true" focusable="false" />}>
            {questions.length > 0 && (
              <MenuAction title="Export" meta="Download this topic's questions" onPress={() => downloadPack({
                subjectLabel: subjectLabel(subjectId),
                topicLabel: topicLabel(subtopicId),
                questions: shown.length ? shown : questions,
                dateIso: new Date(Date.now()).toISOString().slice(0, 10),
              })} />
            )}
            <MenuAction title={copied ? 'Copied' : 'Share'} meta="Copy a shareable link to this topic" onPress={() => { void copyTopicLink(); }} />
          </MenuPanel>
        </div>

        {subjectId === 'politics-and-society' && <Button className="ta-politics" onClick={() => setPoliticsView('tasks')}>Browse individual practice tasks</Button>}

        <div className="ta-years-list">
          {referenceOnly ? (
            <p className="t-meta ta-note">
              This reference topic is retained, but its official question material is not available in the local SEC corpus yet.
            </p>
          ) : shown.length === 0 ? (
            <p className="t-meta ta-note">
              No questions match that filter. <TextButton onClick={() => { setLevelFilter('all'); setYearFilter('all'); }}>Show all</TextButton>
            </p>
          ) : shownYears.map(y => {
            const inThisYear = shown.filter(q => q.year === y);
            const keys = inThisYear.map(q => `${q.year}-${q.level}-${q.lang}-${q.fileid}-${q.n}`);
            const allRows = keys.every(k => kinds[k] === 'row');
            return (
              <section key={y} className="ta-year" aria-label={String(y)}>
                <div className="ta-year-head">
                  <p className="t-number ta-year-num">{y}</p>
                  {allRows ? <span className="t-meta">Opens in the full paper</span> : null}
                </div>
                <div className="ta-year-body">
                  {inThisYear.map((q, i) => {
                    void revVer; // recompute membership when the deck changes
                    const saved = hasCard(uid, { subjectId: q.subjectId, year: q.year, level: q.level, lang: q.lang, fileid: q.fileid, n: q.n });
                    const key = keys[i];
                    return (
                      <VaultQuestionCard
                        key={key}
                        sibling={q}
                        saved={saved}
                        onToggleReview={() => toggleReview(q)}
                        onOpenInPaper={() => onOpenQuestion(q, { subjectId, subtopicId, ...(levelFilter !== 'all' ? { level: levelFilter } : {}) })}
                        topicId={subtopicId}
                        onOpenTopic={id => setSubtopicId(id)}
                        showLevel={levels.length > 1}
                        onKind={kind => setKinds(current => (current[key] === kind ? current : { ...current, [key]: kind }))}
                      />
                    );
                  })}
                </div>
              </section>
            );
          })}
        </div>
      </div>
    );
  }

  // ── Level 1: the topic map (c-tools2-atlas, r5-topic-atlas): the tool's own
  //    sentence as the headline; the subject (its character, no tile) and the
  //    level side by side, search and sort under them; each topic with its
  //    number, its count said once and a small mark per year, inked when it
  //    came up. On a laptop the chosen topic's panel stays on the right. ──
  if (subjectId) {
    const examTaxonomy = examTopicTaxonomyFor(subjectId);
    const stats = subjectAtlasStats(subjectId);
    const yearSets = topicYearSets(subjectId);
    const allStrands = strandsFor(subjectId, topics.map(t => t.subtopicId));
    // A level is chosen where the subject's topics are filed under level headings.
    const strandLevel = (name: string) => LEVEL_KEYS.find(level => name.startsWith(LEVEL_WORD[level] + ' Level')) ?? null;
    const levelOptions = LEVEL_KEYS.filter(level => allStrands.some(s => strandLevel(s.name) === level));
    const activeLevel: string | null = levelOptions.length > 1 ? (levelOptions.find(level => level === mapLevel) ?? levelOptions[0]) : null;
    const strands = activeLevel ? allStrands.filter(s => { const l = strandLevel(s.name); return !l || l === activeLevel; }) : allStrands;
    const topicById = new Map(topics.map(t => [t.subtopicId, t]));
    const sortOptions = ([...(examTaxonomy ? ['reference'] as const : []), 'busiest', 'frequent'] as const).map(s => ({
      value: s,
      label: s === 'reference' ? 'A to Z' : s === 'busiest' ? 'Most asked' : 'Most recurrent',
    }));
    const referenceOrder = new Map(examTaxonomy?.groups.flatMap(group => group.topicIds).map((id, index) => [id, index]) ?? []);
    const orderedByStrand = strands
      .map(strand => {
        const strandTopics = strand.subtopicIds
          .map(id => topicById.get(id))
          .filter((t): t is SubjectTopic => !!t);
        const ordered = [...strandTopics].sort((a, b) =>
          sort === 'reference'
            ? (referenceOrder.get(a.subtopicId) ?? Number.MAX_SAFE_INTEGER) - (referenceOrder.get(b.subtopicId) ?? Number.MAX_SAFE_INTEGER)
            : sort === 'busiest'
            ? b.count - a.count || b.years - a.years || a.label.localeCompare(b.label)
            : b.years - a.years || b.count - a.count || a.label.localeCompare(b.label));
        return { strand, ordered };
      })
      .filter(entry => entry.ordered.length > 0);
    // Contents numbering runs continuously through the whole volume.
    const contentsNo = new Map<string, number>();
    let running = 0;
    for (const entry of orderedByStrand) for (const t of entry.ordered) contentsNo.set(t.subtopicId, ++running);
    const visibleTopics = orderedByStrand.flatMap(entry => entry.ordered);
    const selected = visibleTopics.find(t => t.subtopicId === previewId) ?? visibleTopics[0];
    const selectedYears = selected ? yearSets.get(selected.subtopicId) ?? new Set<number>() : new Set<number>();
    return (
      <div className="lp-atlas ta-map pb-12">
        <header className="ta-top">
          <h2 ref={headingRef} tabIndex={-1} className="t-title outline-none">Every question, mapped by topic.</h2>
          <p className="t-sub">{stats.questions.toLocaleString()} {subjectLabel(subjectId)} questions from {stats.yearMin} to {stats.yearMax}. Each small mark is a year, inked when the topic came up.</p>
        </header>
        <div className="ta-cols">
        <section className="ta-list">
        <div className="ta-controls">
          <div className="ta-subject">
            <SubjectPicker value={subjectId} options={pickerSubjects.map(s => ({ value: s.id, label: s.label }))} onChange={setSubjectId}
              art={<PaperSubjectArtwork label={subjectLabel(subjectId)} className="ta-subject-art" />} />
          </div>
          <div className="ta-control-row">
            {activeLevel && (
              <SelectionBar label="Level" size="md" className="ta-seg ta-level" value={activeLevel} onChange={l => setMapLevel(l)}
                options={levelOptions.map(l => ({ value: l, label: LEVEL_WORD[l] }))} />
            )}
            <Menu label="Sort topics" className="ta-sort" value={sort} onChange={s => setSort(s)} options={sortOptions} />
          </div>
          {sortedTopics.length > 8 && (
            <SearchField label="Search topics" placeholder="Search topics" className="ta-search" value={topicQuery} onChange={e => setTopicQuery(e.target.value)} />
          )}
        </div>
        {topics.length === 0 ? (
          <p className="t-meta ta-note">
            No topics match “{topicQuery.trim()}”. <TextButton onClick={() => setTopicQuery('')}>Clear</TextButton>
          </p>
        ) : orderedByStrand.map(({ strand, ordered }) => (
          <section key={strand.id} className="ta-strand" aria-label={strand.name}>
            <div className="ta-listhead">
              <h3 className="t-label">{strand.name}</h3>
              <span className="ui-readout ta-muted">{ordered.reduce((a, t) => a + t.count, 0).toLocaleString()} questions<span className="ta-wide-only"> · a mark per year</span></span>
            </div>
            <ul className="ta-topics">
              {ordered.map(t => {
                const m = masteryMap.get(t.subtopicId);
                const asked = yearSets.get(t.subtopicId) ?? new Set<number>();
                const marks = <YearMarks years={stats.years} asked={asked} label={`Asked in ${t.years} of ${totalYears} years`} />;
                return (
                  <li key={t.subtopicId}>
                    <button type="button" className="ui-part ta-topic" data-on={selected?.subtopicId === t.subtopicId || undefined}
                      onClick={() => setSubtopicId(t.subtopicId)} onFocus={() => setPreviewId(t.subtopicId)} onMouseEnter={() => setPreviewId(t.subtopicId)}>
                      <span className="ui-readout ta-num" aria-hidden="true">{String(contentsNo.get(t.subtopicId) ?? 0).padStart(2, '0')}</span>
                      <span className="ta-topic-body">
                        <span className="ta-topic-title">{t.label}</span>
                        <span className="t-meta"><span className="ta-phone-only">{t.count} questions · </span>{t.years} of {totalYears} years{m ? ` · ${m.mastery}%` : ''}</span>
                        <span className="ta-phone-only ta-topic-marks">{marks}</span>
                      </span>
                      <span className="ta-wide-only ta-topic-marks">{marks}</span>
                      <span className="ta-wide-only ui-readout ta-count">{t.count}</span>
                      <ChevronRight className="ui-icon ta-phone-only ta-chev" width={20} height={20} strokeWidth={1.75} aria-hidden="true" focusable="false" />
                    </button>
                  </li>
                );
              })}
            </ul>
          </section>
        ))}
        <p className="t-meta ta-foot">Frequency describes past papers, not what will appear next.</p>
        </section>
        <aside className="ta-panel" aria-label="Selected topic">{selected ? <>
          <p className="t-label">Selected topic</p>
          <h2 className="t-title">{selected.label}</h2>
          <p className="t-sub ta-record"><b>{selected.count} questions</b>, asked in <b>{selected.years} of the last {totalYears} years</b></p>
          {stats.years.length > 0 && <div className="ta-head-years">
            <YearMarks large years={stats.years} asked={selectedYears} label={`Asked in ${selected.years} of the ${stats.years.length} years from ${stats.yearMin} to ${stats.yearMax}`} />
            <YearAxis years={stats.years} />
          </div>}
          <p className="t-meta">Browse the original questions and open each with its linked marking scheme.</p>
          <Button kind="main" size="lg" block arrow="forward" onClick={() => setSubtopicId(selected.subtopicId)}>Explore this topic</Button>
        </> : <p className="t-meta">Choose a topic from the map.</p>}</aside>
        </div>
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
          <div className="grid grid-cols-3 sm:grid-cols-4 mb-6 py-3.5" style={{ borderTop: '1px solid var(--hairline)', borderBottom: '1px solid var(--hairline)' }}>
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
            <HorizontalTabs
              variant="pill"
              size="sm"
              label="Subject scope"
              className="w-fit mb-2"
              value={scope}
              onChange={sc => setScope(sc)}
              options={[{ value: 'mine', label: 'My subjects' }, { value: 'all', label: 'All subjects' }]}
            />
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
                      disabled={!canSelectSubject(s.label)}
                      aria-label={`${s.label} — ${st.questions.toLocaleString()} questions across ${topicsForSubject(s.id).length} topics, ${st.yearMin} to ${st.yearMax}`}
                      className="group text-left rounded-2xl overflow-hidden bg-white dark:bg-surface-paper transition-transform duration-200 hover:-translate-y-0.5"
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
