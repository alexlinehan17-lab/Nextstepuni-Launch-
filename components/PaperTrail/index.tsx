/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 *
 * Paper Trail — every SEC exam paper and marking scheme, three taps away.
 *
 * IA rules (from the design review of examinations.ie's failure modes):
 *  - Paper and scheme are attributes of ONE exam entity — never separate
 *    branches. Each paper row carries both buttons; the viewer carries a
 *    persistent toggle that keeps your place in each document.
 *  - Year GRID, not dropdown cascades; unavailable years are greyed WITH the
 *    reason, never dead links; every empty state explains itself.
 *  - Human labels only; file sizes shown for students on metered data.
 *  - ≤3 taps cold (subject → year → paper), 1–2 warm (recents rail).
 *
 * Visual register: Innovation-Zone tool vocabulary — shared SubjectTilePicker
 * tiles, white cards, ink borders, archive-blue identity (#33658A).
 */

import React, { useCallback, useEffect, useMemo, useRef, useState } from 'react';
import { ArrowLeft, Clock3, FileStack, Layers, Repeat, Search } from 'lucide-react';
import SubjectTilePicker from '../shared/SubjectTilePicker';
import { baseName, displayName } from '../shared/subjectNames';
import Viewer from './Viewer';
import { grammarFor, timingFor } from './subjectMeta';
import { taggedSubjects, topicsForPaper, type TopicSibling } from './topics';
import { attemptNs } from './attemptStore';
import { examinerInsightsFor } from '../../data/paperTrail/examinerInsights';
import WeaknessMap from './WeaknessMap';
import ReviseByTopic from './ReviseByTopic';
import ReviewSession from './ReviewSession';
import StreakStrip from './StreakStrip';
import CountdownCard from './CountdownCard';
import ProgressDashboard from './ProgressDashboard';
import MockExamBuilder from './MockExamBuilder';
import FirstRunCoach from './FirstRunCoach';
import { deckStats } from './reviewStore';
import { loadSet } from './mockSetStore';
import { getStreak } from './streakStore';
import { allMarks } from './attemptStore';
import { paperAnswersPath, paperStoragePath, paperUrl, prettyBytes } from './storage';
import {
  FORMULAE_BOOKLET_LIVE,
  FORMULAE_BOOKLET_PATH,
  FORMULAE_INDEX_PATH,
  FORMULAE_SECTIONS,
  FORMULAE_SUBJECTS,
  type FormulaeHandle,
} from '../../data/paperTrailFormulae';
import { usePaperFinder } from '../../hooks/usePaperFinder';
import { getBootParam } from '../../utils/bootParams';
import {
  PAPER_TRAIL_GAPS,
  PAPER_TRAIL_INDEX,
  PAPER_TRAIL_SUBJECTS,
} from '../../paperTrailData';
import {
  recentKey,
  type PaperEntry,
  type PaperItem,
  type PaperLang,
  type PaperLevel,
  type PaperTrailSubject,
  type RecentPaper,
} from '../../types/paperTrail';

const BLUE = '#33658A';
const BLUE_TINT = '#E8EFF5';

const LEVEL_LABEL: Record<PaperLevel, string> = {
  higher: 'Higher',
  ordinary: 'Ordinary',
  foundation: 'Foundation',
  common: 'Common',
};

/** Student-vernacular names the generator's SEC/profile aliases don't cover. */
const SEARCH_ALIASES: Record<string, string[]> = {
  mathematics: ['maths', 'math'],
  'applied-mathematics': ['applied maths'],
  'physical-education': ['pe', 'lcpe'],
  'religious-education': ['re', 'religion'],
  'politics-and-society': ['politics'],
  'construction-studies': ['construction'],
  'agricultural-science': ['ag science', 'ag sci'],
  'agricultural-economics': ['ag econ'],
  'design-and-communication-graphics': ['dcg'],
  'home-economics': ['home ec'],
  'jc-mathematics': ['maths', 'math'],
  'jc-business-studies': ['business'],
};

/** Strip the trailing language marker; level/language are shown by filters. */
const paperLabel = (label: string) => label.replace(/\s*\([A-Z]{2}\)\s*$/, '').trim();

const subjectById = new Map(PAPER_TRAIL_SUBJECTS.map(s => [s.id, s]));

/** One tile in the home study launcher (Revise / Review / Mock set). Compact,
 *  vertical, launcher-style — three read as a single row rather than three
 *  stacked full-width cards. */
const StudyTile: React.FC<{
  icon: React.ReactNode;
  label: string;
  sub: string;
  badge?: number;
  dot?: boolean;
  onClick: () => void;
}> = ({ icon, label, sub, badge, dot, onClick }) => (
  <button
    onClick={onClick}
    className="relative flex flex-col items-center gap-2 rounded-2xl border-2 border-[#1A1A1A] dark:border-zinc-700 bg-white dark:bg-zinc-900 shadow-[3px_3px_0_0_#1A1A1A] dark:shadow-[3px_3px_0_0_#3f3f46] px-2 py-4 text-center transition-transform active:translate-y-0.5 hover:-translate-y-0.5"
  >
    <span className="w-11 h-11 rounded-xl flex items-center justify-center" style={{ backgroundColor: '#FDEEDF' }}>{icon}</span>
    <span className="text-[13px] font-semibold leading-tight" style={{ fontFamily: "'Source Serif 4', serif", color: '#1a1a1a' }}>{label}</span>
    <span className="text-[10.5px] leading-tight" style={{ color: '#9e9186' }}>{sub}</span>
    {badge != null && badge > 0 ? (
      <span className="absolute top-2 right-2 min-w-[18px] h-[18px] px-1 rounded-full text-[10.5px] font-bold flex items-center justify-center tabular-nums" style={{ backgroundColor: '#F26B1F', color: '#fff' }}>{badge}</span>
    ) : dot ? (
      <span className="absolute top-2.5 right-2.5 w-2 h-2 rounded-full" style={{ backgroundColor: '#F26B1F' }} />
    ) : null}
  </button>
);

// Deep-link params are snapshotted at boot by utils/bootParams (this lazy
// chunk loads long after NavigationContext rewrites the URL). Applied at most
// once per page load, inside an effect (StrictMode-safe: state survives the
// simulated remount, and the module flag stops a second application).
let bootApplied = false;

type View =
  | { v: 'home' }
  | { v: 'revise' }
  | { v: 'review' }
  | { v: 'progress' }
  | { v: 'mock' }
  | { v: 'subject'; subjectId: string }
  | {
      v: 'viewer';
      subjectId: string;
      year: number;
      level: PaperLevel;
      lang: PaperLang;
      item: PaperItem;
      side: 'paper' | 'scheme';
      paperPage?: number;
      schemePage?: number;
      /** Cross-year jump landing target — scroll here once anchors load. */
      focusQuestion?: string;
    };

interface PaperTrailProps {
  uid?: string;
  studentSubjects?: string[];
  /** Subject name → chosen level, from the subject profile. */
  studentLevels?: { name: string; level: string }[];
  studentCycle?: 'junior-cycle' | 'leaving-cert';
}

const PaperTrail: React.FC<PaperTrailProps> = ({
  uid,
  studentSubjects,
  studentLevels,
  studentCycle,
}) => {
  const { state, isLoaded, recordRecent, updatePage, setFilters } = usePaperFinder(uid);
  const junior = studentCycle === 'junior-cycle';

  const [view, setView] = useState<View>({ v: 'home' });
  const [level, setLevel] = useState<PaperLevel | null>(null);
  const [lang, setLang] = useState<PaperLang | null>(null);
  const [year, setYear] = useState<number | null>(null);
  const [scope, setScope] = useState<'mine' | 'all'>('mine');
  const [query, setQuery] = useState('');
  const [gapNote, setGapNote] = useState<string | null>(null);
  const searchBoxRef = useRef<HTMLDivElement | null>(null);

  // ── deep link (?tool=paper-trail&subject=…&year=…), applied once per load ──
  useEffect(() => {
    if (bootApplied) return;
    bootApplied = true;
    const subjectId = getBootParam('subject');
    if (!subjectId || !subjectById.has(subjectId)) return;
    const subj = subjectById.get(subjectId)!;
    if (junior !== (subj.cycle === 'jc')) return; // cycle guard
    const y = Number(getBootParam('year') ?? '');
    if (Number.isFinite(y) && y > 1990) setYear(y);
    setView({ v: 'subject', subjectId });
  }, []);

  // ── matching the student's profile to paper subjects ──
  const matchesStudent = useCallback(
    (s: PaperTrailSubject, names: Set<string>) =>
      names.has(baseName(s.name)) || (s.aliases ?? []).some(a => names.has(baseName(a))),
    [],
  );

  const groups = useMemo(() => {
    const mineNames = new Set((studentSubjects ?? []).map(baseName));
    const inCycle = PAPER_TRAIL_SUBJECTS.filter(s =>
      junior ? s.cycle === 'jc' : s.cycle !== 'jc',
    );
    const main = inCycle
      .filter(s => (junior ? true : s.cycle === 'lc'))
      .sort((a, b) => displayName(a.name).localeCompare(displayName(b.name)));
    const lca = (junior ? [] : inCycle.filter(s => s.cycle === 'lca')).sort((a, b) =>
      displayName(a.name).localeCompare(displayName(b.name)),
    );
    const mineIds = [
      ...main.filter(s => matchesStudent(s, mineNames)).map(s => s.id),
      ...lca.filter(s => matchesStudent(s, mineNames)).map(s => s.id),
    ];
    return { main, lca, mineIds };
  }, [junior, studentSubjects, matchesStudent]);

  /** Distinct-paper count (English-version only — IV duplicates would ~double it). */
  const paperCount = useCallback((id: string) => {
    const n = (PAPER_TRAIL_INDEX[id] ?? [])
      .filter(e => e.lang === 'ev')
      .reduce((acc, e) => acc + e.papers.filter(p => !p.modified).length, 0);
    return `${n} ${n === 1 ? 'paper' : 'papers'}`;
  }, []);

  /** The student's chosen level for a subject, where the profile knows it. */
  const profileLevelFor = useCallback(
    (subj: PaperTrailSubject): PaperLevel | null => {
      for (const sl of studentLevels ?? []) {
        const n = baseName(sl.name);
        if (n === baseName(subj.name) || (subj.aliases ?? []).some(a => baseName(a) === n)) {
          const lv = sl.level.toLowerCase();
          if (subj.levels.includes(lv as PaperLevel)) return lv as PaperLevel;
        }
      }
      return null;
    },
    [studentLevels],
  );

  // ── search accelerator ("english 2022 hl") ──
  const suggestions = useMemo(() => {
    const q = query.trim().toLowerCase();
    if (q.length < 2) return null;
    let yr: number | undefined;
    let lv: PaperLevel | undefined;
    const words: string[] = [];
    for (const tok of q.split(/\s+/)) {
      if (/^(19|20)\d\d$/.test(tok)) yr = Number(tok);
      else if (['hl', 'higher'].includes(tok)) lv = 'higher';
      else if (['ol', 'ordinary'].includes(tok)) lv = 'ordinary';
      else if (['fl', 'foundation'].includes(tok)) lv = 'foundation';
      else if (!/^p(aper)?\d?$/.test(tok) && !/^\d$/.test(tok)) words.push(tok);
    }
    const name = words.join(' ');
    const pool = junior
      ? PAPER_TRAIL_SUBJECTS.filter(s => s.cycle === 'jc')
      : PAPER_TRAIL_SUBJECTS.filter(s => s.cycle !== 'jc');
    return pool
      .filter(s => {
        if (name.length === 0) return true;
        const names = [s.name, ...(s.aliases ?? []), ...(SEARCH_ALIASES[s.id] ?? [])].map(n =>
          n.toLowerCase(),
        );
        return names.some(n => n.includes(name));
      })
      .slice(0, 6)
      .map(s => ({ subject: s, year: yr, level: lv }));
  }, [query, junior]);

  // Close the search dropdown on outside tap / Escape.
  useEffect(() => {
    if (!query) return;
    const onDown = (e: PointerEvent) => {
      if (searchBoxRef.current && !searchBoxRef.current.contains(e.target as Node)) setQuery('');
    };
    const onKey = (e: KeyboardEvent) => {
      if (e.key === 'Escape') setQuery('');
    };
    window.addEventListener('pointerdown', onDown);
    window.addEventListener('keydown', onKey);
    return () => {
      window.removeEventListener('pointerdown', onDown);
      window.removeEventListener('keydown', onKey);
    };
  }, [query]);

  // ── viewer launch helpers ──
  const openItem = useCallback(
    (subj: PaperTrailSubject, entry: PaperEntry, item: PaperItem, side: 'paper' | 'scheme') => {
      const key = recentKey(subj.id, entry.year, entry.level, entry.lang, item.doc.f);
      const existing = state.recents.find(r => r.key === key);
      setView({
        v: 'viewer',
        subjectId: subj.id,
        year: entry.year,
        level: entry.level,
        lang: entry.lang,
        item,
        side,
        paperPage: existing?.paperPage,
        schemePage: existing?.schemePage,
      });
      recordRecent({
        key,
        subjectId: subj.id,
        year: entry.year,
        level: entry.level,
        lang: entry.lang,
        label: item.label,
        kind: side,
        doc: item.doc,
        ...(item.scheme ? { scheme: item.scheme } : {}),
      });
    },
    [recordRecent, state.recents],
  );

  const openRecent = useCallback((r: RecentPaper) => {
    if (!subjectById.has(r.subjectId)) return;
    setView({
      v: 'viewer',
      subjectId: r.subjectId,
      year: r.year,
      level: r.level,
      lang: r.lang,
      item: { label: r.label, doc: r.doc, ...(r.scheme ? { scheme: r.scheme } : {}) },
      side: r.kind,
      paperPage: r.paperPage,
      schemePage: r.schemePage,
    });
  }, []);

  // Cross-year topic jump: resolve the sibling's paper from the index and open
  // it on the paper side, focused on the target question.
  const openCrossYear = useCallback((t: TopicSibling) => {
    if (!subjectById.has(t.subjectId)) return;
    const entry = (PAPER_TRAIL_INDEX[t.subjectId] ?? []).find(
      e => e.year === t.year && e.level === t.level && e.lang === t.lang,
    );
    const item = entry?.papers.find(p => p.doc.f === t.fileid);
    if (!item) return;
    setView({
      v: 'viewer',
      subjectId: t.subjectId,
      year: t.year,
      level: t.level,
      lang: t.lang,
      item,
      side: 'paper',
      focusQuestion: t.n,
    });
  }, []);

  if (!isLoaded) {
    return (
      <div className="w-full max-w-xl mx-auto py-16 text-center text-sm text-zinc-400">Loading…</div>
    );
  }

  // ═══════════════════════ VIEWER ═══════════════════════
  if (view.v === 'viewer') {
    const subj = subjectById.get(view.subjectId)!;
    const key = recentKey(view.subjectId, view.year, view.level, view.lang, view.item.doc.f);
    const url = (kind: 'paper' | 'scheme', f: string) =>
      paperUrl(paperStoragePath(subj.cycle, subj.id, view.year, kind, f));
    // The `answers` flag lives on the index, not on the recents snapshot — look
    // the live item up so the toggle appears even when re-opened from Recents.
    const liveItem = (PAPER_TRAIL_INDEX[subj.id] ?? [])
      .find(e => e.year === view.year && e.level === view.level && e.lang === view.lang)
      ?.papers.find(p => p.doc.f === view.item.doc.f);
    const hasAnswers = liveItem?.answers === 1 && !!view.item.scheme;
    // Formulae & Tables quick-jump — only for booklet subjects, and only once
    // the booklet is uploaded + the flag flipped (nothing dead ships).
    const formulae: FormulaeHandle | undefined =
      FORMULAE_BOOKLET_LIVE && FORMULAE_SUBJECTS[subj.id]
        ? {
            bookletUrl: paperUrl(FORMULAE_BOOKLET_PATH),
            indexUrl: paperUrl(FORMULAE_INDEX_PATH),
            sections: FORMULAE_SECTIONS.filter(s => s.subjects.includes(subj.id)),
          }
        : undefined;
    // Topic tags — present only when this exact paper is tagged (needs anchors,
    // so also gated on the answer map). The committed record carries a stable
    // paperKey, so pass it through by reference (keeps the viewer's memo stable).
    const topics =
      (hasAnswers
        ? topicsForPaper(subj.id, view.year, view.level, view.lang, view.item.doc.f)
        : null) ?? undefined;
    return (
      <Viewer
        title={`${displayName(subj.name)} · ${view.year}`}
        subtitle={`${paperLabel(view.item.label)} · ${LEVEL_LABEL[view.level]}${view.lang === 'iv' ? ' · Gaeilge' : ''}`}
        paper={{ url: url('paper', view.item.doc.f), label: paperLabel(view.item.label), bytes: view.item.doc.b }}
        scheme={
          view.item.scheme
            ? { url: url('scheme', view.item.scheme.f), label: 'Marking scheme', bytes: view.item.scheme.b }
            : undefined
        }
        answersUrl={
          hasAnswers ? paperUrl(paperAnswersPath(subj.cycle, subj.id, view.year, view.item.doc.f)) : undefined
        }
        timing={timingFor(subj.id, view.item.label)}
        grammar={grammarFor(subj.id)}
        formulae={formulae}
        topics={topics}
        onCrossYear={openCrossYear}
        focusQuestion={view.focusQuestion}
        storageNs={attemptNs(uid, subj.id, view.year, view.level, view.lang, view.item.doc.f)}
        examinerInsights={examinerInsightsFor(subj.id) ?? undefined}
        initialSide={view.side}
        initialPaperPage={view.paperPage ?? 1}
        initialSchemePage={view.schemePage ?? 1}
        onClose={() => setView({ v: 'subject', subjectId: view.subjectId })}
        onPosition={(side, page) => updatePage(key, page, side)}
      />
    );
  }

  // ═══════════════════════ REVISE BY TOPIC ═══════════════════════
  if (view.v === 'revise') {
    const inCycleTagged = taggedSubjects()
      .map(id => subjectById.get(id))
      .filter((s): s is PaperTrailSubject => !!s && (junior ? s.cycle === 'jc' : s.cycle !== 'jc'))
      .sort((a, b) => displayName(a.name).localeCompare(displayName(b.name)));
    const mineNames = new Set((studentSubjects ?? []).map(baseName));
    return (
      <ReviseByTopic
        subjects={inCycleTagged.map(s => ({ id: s.id, label: displayName(s.name) }))}
        mineIds={inCycleTagged.filter(s => matchesStudent(s, mineNames)).map(s => s.id)}
        uid={uid}
        subjectLabel={id => displayName(subjectById.get(id)?.name ?? id)}
        onOpenQuestion={openCrossYear}
        onBack={() => setView({ v: 'home' })}
      />
    );
  }

  // ═══════════════════════ MOCK-SET BUILDER ═══════════════════════
  if (view.v === 'mock') {
    const inCycleTagged = taggedSubjects()
      .map(id => subjectById.get(id))
      .filter((s): s is PaperTrailSubject => !!s && (junior ? s.cycle === 'jc' : s.cycle !== 'jc'))
      .sort((a, b) => displayName(a.name).localeCompare(displayName(b.name)));
    const mineNames = new Set((studentSubjects ?? []).map(baseName));
    return (
      <MockExamBuilder
        uid={uid}
        now={Date.now()}
        subjects={inCycleTagged.map(s => ({ id: s.id, label: displayName(s.name) }))}
        mineIds={inCycleTagged.filter(s => matchesStudent(s, mineNames)).map(s => s.id)}
        subjectLabel={id => displayName(subjectById.get(id)?.name ?? id)}
        onOpenQuestion={openCrossYear}
        onBack={() => setView({ v: 'home' })}
      />
    );
  }

  // ═══════════════════════ DAILY REVIEW (SRS) ═══════════════════════
  if (view.v === 'review') {
    return (
      <ReviewSession
        uid={uid}
        now={Date.now()}
        subjectLabel={id => displayName(subjectById.get(id)?.name ?? id)}
        onOpenQuestion={openCrossYear}
        onBack={() => setView({ v: 'home' })}
      />
    );
  }

  // ═══════════════════════ PROGRESS DASHBOARD ═══════════════════════
  if (view.v === 'progress') {
    return (
      <ProgressDashboard
        uid={uid}
        now={Date.now()}
        subjectLabel={id => displayName(subjectById.get(id)?.name ?? id)}
        onDrill={openCrossYear}
        onBack={() => setView({ v: 'home' })}
      />
    );
  }

  // ═══════════════════════ SUBJECT ═══════════════════════
  if (view.v === 'subject') {
    const subj = subjectById.get(view.subjectId)!;
    const entries = PAPER_TRAIL_INDEX[subj.id] ?? [];
    const activeLevel: PaperLevel =
      level && subj.levels.includes(level)
        ? level
        : (profileLevelFor(subj) ??
          (state.lastLevel && subj.levels.includes(state.lastLevel)
            ? state.lastLevel
            : subj.levels[0]));

    // Language: offer the toggle only where this LEVEL has both versions;
    // fall back to whichever language actually has entries (some Irish-medium
    // material is IV-first).
    const levelEntries = entries.filter(e => e.level === activeLevel);
    const langsAtLevel = [...new Set(levelEntries.map(e => e.lang))];
    const activeLang: PaperLang =
      lang && langsAtLevel.includes(lang)
        ? lang
        : state.lastLang && langsAtLevel.includes(state.lastLang)
          ? state.lastLang
          : (langsAtLevel[0] ?? 'ev');

    const slice = levelEntries.filter(e => e.lang === activeLang);
    const availableYears = [...new Set(slice.map(e => e.year))];
    const gapsForSubject = PAPER_TRAIL_GAPS.filter(g => g.subjectId === subj.id);
    // One chronological grid: real years + explained gaps, newest first.
    const yearCells: { year: number; gap?: string }[] = [
      ...availableYears.map(y => ({ year: y })),
      ...gapsForSubject
        .filter(g => !availableYears.includes(g.year))
        .map(g => ({ year: g.year, gap: g.reason })),
    ].sort((a, b) => b.year - a.year);

    const activeYear = year && availableYears.includes(year) ? year : availableYears[0];
    const entry = slice.find(e => e.year === activeYear);
    const requestedMissing = year != null && !availableYears.includes(year) && availableYears.length > 0;

    return (
      <div className="w-full max-w-xl mx-auto pb-12">
        <button
          onClick={() => {
            setView({ v: 'home' });
            setYear(null);
            setGapNote(null);
          }}
          className="flex items-center gap-1.5 text-[13px] font-medium text-zinc-500 hover:text-zinc-800 dark:hover:text-zinc-200 mb-4"
        >
          <ArrowLeft size={15} /> All subjects
        </button>

        <h2 className="text-2xl font-semibold mb-1" style={{ fontFamily: "'Source Serif 4', serif", color: '#1a1a1a' }}>
          {displayName(subj.name)}
          {subj.cycle === 'lca' && (
            <span className="ml-2 text-[12px] font-sans font-bold uppercase tracking-wide align-middle" style={{ color: '#9e9186' }}>
              LCA
            </span>
          )}
        </h2>
        <p className="text-[13px] mb-4" style={{ color: '#7a7068' }}>
          Real SEC papers with their marking schemes — pick a year.
        </p>

        {/* Level + language controls */}
        <div className="flex flex-wrap items-center gap-2.5 mb-4">
          {subj.levels.length > 1 && (
            <div className="flex items-center gap-1 p-1 rounded-xl bg-zinc-100 dark:bg-zinc-800/50" role="group" aria-label="Level">
              {subj.levels.map(lv => (
                <button
                  key={lv}
                  aria-pressed={activeLevel === lv}
                  onClick={() => {
                    setLevel(lv);
                    setFilters({ lastLevel: lv });
                    setYear(null);
                    setGapNote(null);
                  }}
                  className={`px-3.5 py-1.5 rounded-lg text-[13px] transition-all ${activeLevel === lv ? 'bg-white dark:bg-zinc-800 text-zinc-900 dark:text-white font-semibold shadow-sm' : 'text-zinc-500 dark:text-zinc-400'}`}
                >
                  {LEVEL_LABEL[lv]}
                </button>
              ))}
            </div>
          )}
          {langsAtLevel.length > 1 && (
            <div className="flex items-center gap-1 p-1 rounded-xl bg-zinc-100 dark:bg-zinc-800/50" role="group" aria-label="Language">
              {(['ev', 'iv'] as const)
                .filter(lg => langsAtLevel.includes(lg))
                .map(lg => (
                  <button
                    key={lg}
                    aria-pressed={activeLang === lg}
                    onClick={() => {
                      setLang(lg);
                      setFilters({ lastLang: lg });
                      setYear(null);
                      setGapNote(null);
                    }}
                    className={`px-3.5 py-1.5 rounded-lg text-[13px] transition-all ${activeLang === lg ? 'bg-white dark:bg-zinc-800 text-zinc-900 dark:text-white font-semibold shadow-sm' : 'text-zinc-500 dark:text-zinc-400'}`}
                  >
                    {lg === 'ev' ? 'English' : 'Gaeilge'}
                  </button>
                ))}
            </div>
          )}
        </div>

        {availableYears.length === 0 ? (
          <p className="text-[13.5px] rounded-2xl px-4 py-4" style={{ backgroundColor: BLUE_TINT, color: '#27506E' }}>
            Nothing is published at {LEVEL_LABEL[activeLevel]} level for this subject
            {subj.levels.length > 1 ? ' — try another level above.' : ' yet.'}
          </p>
        ) : (
          <>
            {/* Year grid */}
            <h3 className="text-[11px] font-bold uppercase tracking-[0.14em] mb-2.5" style={{ color: '#9e9186' }}>
              Choose a year
            </h3>
            <div className="flex flex-wrap gap-2 mb-2">
              {yearCells.map(c =>
                c.gap ? (
                  <button
                    key={`gap-${c.year}`}
                    onClick={() => setGapNote(`${c.year}: ${c.gap}`)}
                    aria-label={`${c.year} unavailable — ${c.gap}`}
                    className="px-3.5 py-2 rounded-xl border-2 border-dashed border-zinc-200 dark:border-zinc-800 text-[14px] font-bold text-zinc-300 dark:text-zinc-600"
                  >
                    {c.year}
                  </button>
                ) : (
                  <button
                    key={c.year}
                    onClick={() => {
                      setYear(c.year);
                      setGapNote(null);
                    }}
                    aria-pressed={activeYear === c.year}
                    className={`px-3.5 py-2 rounded-xl border-2 text-[14px] font-bold transition-all ${
                      activeYear === c.year
                        ? 'text-white'
                        : 'border-zinc-200 dark:border-zinc-700 bg-white dark:bg-zinc-900 text-zinc-700 dark:text-zinc-200 hover:border-zinc-400'
                    }`}
                    style={activeYear === c.year ? { backgroundColor: BLUE, borderColor: '#1A1A1A' } : undefined}
                  >
                    {c.year}
                  </button>
                ),
              )}
            </div>
            {gapNote && (
              <p className="text-[12px] mb-3 rounded-xl px-3.5 py-2.5" style={{ backgroundColor: BLUE_TINT, color: '#27506E' }}>
                {gapNote}
              </p>
            )}
            {requestedMissing && (
              <p className="text-[12px] mb-3" style={{ color: '#9e9186' }}>
                {year} isn’t available here — showing {activeYear} instead.
              </p>
            )}

            {/* Papers for the active year */}
            {entry && (
              <div className="space-y-3 mt-3">
                {entry.note && (
                  <p className="text-[12px] rounded-xl px-3.5 py-2.5" style={{ backgroundColor: BLUE_TINT, color: '#27506E' }}>
                    {entry.note}
                  </p>
                )}
                {(() => {
                  const mains = entry.papers.filter(p => !p.modified);
                  const list = mains.length > 0 ? mains : entry.papers;
                  return list.map(item => (
                    <div
                      key={item.doc.f}
                      className="rounded-2xl border-2 border-[#1A1A1A] dark:border-zinc-700 bg-white dark:bg-zinc-900 shadow-[4px_4px_0_0_#1A1A1A] dark:shadow-[4px_4px_0_0_#3f3f46] p-4"
                    >
                      <div className="flex items-center justify-between gap-3 mb-3">
                        <p className="text-[16px] font-semibold" style={{ fontFamily: "'Source Serif 4', serif", color: '#1a1a1a' }}>
                          {paperLabel(item.label)}
                          {item.modified && (
                            <span className="ml-2 text-[11px] font-sans font-medium" style={{ color: '#7a7068' }}>
                              accessible format
                            </span>
                          )}
                        </p>
                        <span className="text-[11px] shrink-0" style={{ color: '#9e9186' }}>
                          {activeYear} · {LEVEL_LABEL[activeLevel]}
                        </span>
                      </div>
                      <div className="flex items-center gap-2.5">
                        <button
                          onClick={() => openItem(subj, entry, item, 'paper')}
                          className="flex-1 py-2.5 rounded-full text-[13.5px] font-semibold text-white transition-transform active:translate-y-0.5"
                          style={{ backgroundColor: '#F26B1F', boxShadow: '0 3px 0 #B54D14' }}
                        >
                          Paper{item.doc.b > 0 && <span className="opacity-75 font-medium"> · {prettyBytes(item.doc.b)}</span>}
                        </button>
                        {item.scheme ? (
                          <button
                            onClick={() => openItem(subj, entry, item, 'scheme')}
                            className="flex-1 py-2.5 rounded-full text-[13.5px] font-semibold border-2 transition-transform active:translate-y-0.5"
                            style={{ borderColor: 'rgba(242,107,31,0.35)', color: '#F26B1F' }}
                          >
                            Marking scheme{item.scheme.b > 0 && <span className="opacity-70 font-medium"> · {prettyBytes(item.scheme.b)}</span>}
                          </button>
                        ) : (
                          <span className="flex-1 py-2.5 text-center text-[12px] rounded-full border-2 border-dashed border-zinc-200 dark:border-zinc-700" style={{ color: '#9e9186' }}>
                            Scheme not published
                          </span>
                        )}
                      </div>
                      {mains.length > 0 &&
                        !item.modified &&
                        entry.papers.some(p => p.modified && paperLabel(p.label).startsWith(paperLabel(item.label))) && (
                          <button
                            onClick={() => {
                              const mod = entry.papers.find(
                                p => p.modified && paperLabel(p.label).startsWith(paperLabel(item.label)),
                              )!;
                              openItem(subj, entry, mod, 'paper');
                            }}
                            className="mt-2.5 text-[11.5px] underline underline-offset-2"
                            style={{ color: '#7a7068' }}
                          >
                            Accessible format (vision-impaired candidates)
                          </button>
                        )}
                    </div>
                  ));
                })()}
                {entry.papers.length === 0 && (
                  <p className="text-[13px]" style={{ color: '#9e9186' }}>
                    Nothing published for this year and level.
                  </p>
                )}
              </div>
            )}
          </>
        )}
      </div>
    );
  }

  // ═══════════════════════ HOME ═══════════════════════
  const recents = state.recents.filter(r => {
    const s = subjectById.get(r.subjectId);
    return s && (junior ? s.cycle === 'jc' : s.cycle !== 'jc');
  });
  const showLcaSection =
    !junior &&
    groups.lca.length > 0 &&
    (scope === 'all' || groups.mineIds.length === 0 || groups.lca.some(s => groups.mineIds.includes(s.id)));
  const review = deckStats(uid, Date.now());
  const reviewTileSub = review.due > 0 ? `${review.due} due` : review.total > 0 ? 'all caught up' : 'spaced recall';
  const activeMock = loadSet(uid);
  // First-run coach shows only for a truly new student (nothing practised yet).
  const hasActivity =
    recents.length > 0 ||
    review.total > 0 ||
    !!activeMock ||
    getStreak(uid, Date.now()).longest > 0 ||
    allMarks(uid).length > 0;

  return (
    <div className="w-full max-w-xl mx-auto pb-12">
      <p className="text-[15px] leading-relaxed mb-5" style={{ color: '#5a5550', fontFamily: "'DM Sans', sans-serif" }}>
        Pick a subject — every paper opens with its marking scheme one tap away,
        {junior ? ' for every Junior Cycle exam you can sit.' : ' for every exam year back to 2010.'}
      </p>

      {/* Search accelerator */}
      <div className="relative mb-5" ref={searchBoxRef}>
        <Search size={16} className="absolute left-3.5 top-1/2 -translate-y-1/2 text-zinc-400" aria-hidden />
        <input
          value={query}
          onChange={e => setQuery(e.target.value)}
          placeholder={junior ? 'Try “science 2023”' : 'Try “english 2022 hl”'}
          aria-label="Search for a paper"
          className="w-full pl-10 pr-4 py-3 rounded-2xl border-2 border-zinc-200 dark:border-zinc-700 bg-white dark:bg-zinc-900 text-[14px] outline-none focus:border-[#1A1A1A] dark:focus:border-zinc-400 transition-colors"
        />
        {suggestions && (
          <div className="absolute z-20 left-0 right-0 mt-1.5 rounded-2xl border-2 border-[#1A1A1A] dark:border-zinc-700 bg-white dark:bg-zinc-900 shadow-[4px_4px_0_0_#1A1A1A] overflow-hidden">
            {suggestions.length === 0 ? (
              <p className="px-4 py-3 text-[13px] text-zinc-500">No matches — try the subject’s full name.</p>
            ) : (
              suggestions.map(sug => (
                <button
                  key={sug.subject.id}
                  onClick={() => {
                    setQuery('');
                    if (sug.level) setLevel(sug.level);
                    setYear(sug.year ?? null);
                    setGapNote(null);
                    setView({ v: 'subject', subjectId: sug.subject.id });
                  }}
                  className="w-full text-left px-4 py-3 text-[14px] font-medium text-zinc-800 dark:text-zinc-100 hover:bg-zinc-50 dark:hover:bg-zinc-800 border-b border-zinc-100 dark:border-zinc-800 last:border-0"
                >
                  {displayName(sug.subject.name)}
                  {sug.subject.cycle === 'lca' && <span className="ml-1.5 text-[11px] text-zinc-400">LCA</span>}
                  {(sug.year || sug.level) && (
                    <span className="ml-1.5 text-[12px] text-zinc-400">
                      {[sug.year, sug.level && LEVEL_LABEL[sug.level]].filter(Boolean).join(' · ')}
                    </span>
                  )}
                </button>
              ))
            )}
          </div>
        )}
      </div>

      {/* Exam countdown + daily focus (A3). */}
      <CountdownCard uid={uid} now={Date.now()} onOpen={() => setView({ v: 'progress' })} />

      {/* Practice streak + daily goal (B3) — hidden until first practice; opens
          the progress dashboard when tapped. */}
      <StreakStrip uid={uid} now={Date.now()} onOpen={() => setView({ v: 'progress' })} />

      {/* First-run coach — the study loop in three steps, for new students only. */}
      <FirstRunCoach uid={uid} hasActivity={hasActivity} />

      {/* Study launcher — Revise / Review / Mock, one compact row (A1/A2/B1). */}
      <div className="grid grid-cols-3 gap-2.5 mb-6">
        <StudyTile icon={<Layers size={20} style={{ color: '#F26B1F' }} />} label="Revise" sub="by topic" onClick={() => setView({ v: 'revise' })} />
        <StudyTile icon={<Repeat size={20} style={{ color: '#F26B1F' }} />} label="Review" sub={reviewTileSub} badge={review.due} onClick={() => setView({ v: 'review' })} />
        <StudyTile icon={<FileStack size={20} style={{ color: '#F26B1F' }} />} label="Mock set" sub={activeMock ? 'resume' : 'timed set'} dot={!!activeMock} onClick={() => setView({ v: 'mock' })} />
      </div>

      {/* Recents rail */}
      {recents.length > 0 && (
        <>
          <h3 className="text-[11px] font-bold uppercase tracking-[0.14em] mb-2.5" style={{ color: '#9e9186' }}>
            Pick up where you left off
          </h3>
          <div className="flex gap-2.5 overflow-x-auto pb-2 mb-5 -mx-1 px-1">
            {recents.map(r => {
              const s = subjectById.get(r.subjectId)!;
              const page = r.kind === 'scheme' ? r.schemePage : r.paperPage;
              return (
                <button
                  key={r.key}
                  onClick={() => openRecent(r)}
                  className="shrink-0 text-left rounded-2xl border-2 border-[#1A1A1A] dark:border-zinc-700 bg-white dark:bg-zinc-900 shadow-[3px_3px_0_0_#1A1A1A] dark:shadow-[3px_3px_0_0_#3f3f46] px-3.5 py-3 min-w-[150px] transition-transform hover:-translate-y-0.5"
                >
                  <p className="text-[13px] font-bold leading-tight" style={{ color: '#1a1a1a' }}>
                    {displayName(s.name)} {r.year}
                  </p>
                  <p className="text-[11px] mt-0.5 flex items-center gap-1" style={{ color: '#7a7068' }}>
                    <Clock3 size={11} aria-hidden />
                    {paperLabel(r.label)}
                    {r.kind === 'scheme' ? ' · scheme' : ''}
                    {page > 1 ? ` · p.${page}` : ''}
                  </p>
                </button>
              );
            })}
          </div>
        </>
      )}

      {/* Your practice — self-mark weakness map (Tier 3). Renders only if the
          student has self-marked at least one question. */}
      <WeaknessMap
        uid={uid}
        subjectName={id => displayName(subjectById.get(id)?.name ?? id)}
        onDrill={openCrossYear}
        onOpenDashboard={() => setView({ v: 'progress' })}
      />

      {/* Subject picker */}
      {groups.main.length === 0 ? (
        <p className="text-[13.5px] rounded-2xl px-4 py-4" style={{ backgroundColor: BLUE_TINT, color: '#27506E' }}>
          {junior
            ? 'Junior Cycle papers are being added — check back very soon.'
            : 'Papers are being added — check back very soon.'}
        </p>
      ) : (
        <SubjectTilePicker
          headingLabel="Pick a subject"
          subjects={groups.main.map(s => ({
            id: s.id,
            label: displayName(s.name),
            sublabel: paperCount(s.id),
          }))}
          mineIds={groups.mineIds.filter(id => groups.main.some(s => s.id === id))}
          scope={scope}
          onScopeChange={setScope}
          onPick={id => {
            setYear(null);
            setGapNote(null);
            setView({ v: 'subject', subjectId: id });
          }}
        />
      )}

      {/* LCA group — always reachable, never gated behind a toggle LCA students can't see */}
      {showLcaSection && (
        <div className="mt-7">
          <h3 className="text-[11px] font-bold uppercase tracking-[0.14em] mb-3" style={{ color: '#9e9186' }}>
            Leaving Cert Applied
          </h3>
          <SubjectTilePicker
            subjects={groups.lca.map(s => ({
              id: s.id,
              label: displayName(s.name),
              sublabel: paperCount(s.id),
            }))}
            scope="all"
            onScopeChange={() => {}}
            onPick={id => {
              setYear(null);
              setGapNote(null);
              setView({ v: 'subject', subjectId: id });
            }}
          />
        </div>
      )}

      <p className="text-[11px] leading-relaxed mt-7" style={{ color: '#9e9186' }}>
        Examination material © State Examinations Commission, reproduced with attribution. Papers
        open inside the app — nothing to download unless you want to.
      </p>
    </div>
  );
};

export default PaperTrail;
