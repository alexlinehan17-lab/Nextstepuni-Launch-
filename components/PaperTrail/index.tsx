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
import { ArrowLeft, Clock3, Layers, ListChecks, Search, Star } from 'lucide-react';
import SubjectTilePicker from '../shared/SubjectTilePicker';
import { baseName, displayName } from '../shared/subjectNames';
import Viewer from './Viewer';
import ImageViewer from './ImageViewer';
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
import { LoadingState } from '../ui/SystemState';
import Flashcards from './Flashcards';
import FirstRunCoach from './FirstRunCoach';
import MilestoneCelebration from './MilestoneCelebration';
import { deckStats } from './reviewStore';
import { allMarks } from './attemptStore';
import { composeCoach } from './coach';
import { composeDebrief, debriefSeen, markDebriefSeen } from './debrief';
import { pendingMilestones, acknowledgeMilestone, type Milestone } from './milestones';
import { paperAnswersPath, paperStoragePath, paperUrl, prettyBytes } from './storage';
import { isPinned, listPins, listRecentOpens, recordRecentOpen, togglePin, type PaperRef } from './recentsStore';
import { recordVisit } from '../lastVisited';
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
import { hasInitialVaultTopic } from './vaultDeepLink';
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

// The SEC archive contains a small number of distinct syllabuses whose
// cycle-filtered display names collapse to the same label (for example,
// "History" and "History (Early Modern)"). Keep the short label everywhere
// it is unambiguous, but preserve the qualifier when stripping it would create
// two indistinguishable subjects.
const subjectLabelCounts = PAPER_TRAIL_SUBJECTS.reduce((counts, subject) => {
  const key = `${subject.cycle}:${displayName(subject.name)}`;
  counts.set(key, (counts.get(key) ?? 0) + 1);
  return counts;
}, new Map<string, number>());

export const paperTrailSubjectLabel = (subject: PaperTrailSubject) =>
  (subjectLabelCounts.get(`${subject.cycle}:${displayName(subject.name)}`) ?? 0) > 1
    ? subject.name
    : displayName(subject.name);

const subjectLabelForId = (id: string) => {
  const subject = subjectById.get(id);
  return subject ? paperTrailSubjectLabel(subject) : displayName(id);
};


// Deep-link params are snapshotted at boot by utils/bootParams (this lazy
// chunk loads long after NavigationContext rewrites the URL). Applied at most
// once per page load, inside an effect (StrictMode-safe: state survives the
// simulated remount, and the module flag stops a second application).
let bootApplied = false;

/** A Topic Vault feed launch origin — closing the viewer returns here instead
 *  of the subject paper list, so a "Full paper" round-trip keeps the feed. */
type VaultOrigin = { subjectId: string; subtopicId: string };

type View =
  | { v: 'home' }
  | { v: 'revise'; restore?: VaultOrigin }
  | { v: 'review' }
  | { v: 'progress' }
  | { v: 'mock' }
  | { v: 'cards' }
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
      /** The screen to return to when the viewer is closed. Set for every
       *  cross-year jump (Revise feed, Mock builder, Progress, Weakness Map,
       *  Review) so Close lands back where the student launched from rather than
       *  dumping them on the subject year-grid. Absent for the normal
       *  open-from-year-grid flow (openItem), which falls back to the grid. */
      returnTo?: View;
    };

interface PaperTrailProps {
  uid?: string;
  studentSubjects?: string[];
  /** Subject name → chosen level, from the subject profile. */
  studentLevels?: { name: string; level: string }[];
  studentCycle?: 'junior-cycle' | 'leaving-cert';
  /** Leaving Cert Applied student — shows the LCA archive group (hidden for
   *  everyone else). */
  isLca?: boolean;
  /** Exam start date from onboarding (subjectProfile.examStartDate, ISO) —
   *  pre-fills the countdown so the student needn't re-enter it. */
  onboardingExamDate?: string;
  /** Cross-tool routing (error autopsy) — opens another Launchpad tool by id. */
  onOpenTool?: (toolId: string) => void;
}

const PaperTrail: React.FC<PaperTrailProps> = ({
  uid,
  studentSubjects,
  studentLevels,
  studentCycle,
  isLca = false,
  onboardingExamDate,
  onOpenTool,
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
  // Learning-milestone celebration — detected once at mount, shown one at a time.
  const [milestone, setMilestone] = useState<Milestone | null>(() => pendingMilestones(uid, Date.now())[0] ?? null);
  const dismissMilestone = useCallback(() => {
    setMilestone(prev => {
      if (prev) acknowledgeMilestone(uid, prev.id);
      return pendingMilestones(uid, Date.now())[0] ?? null;
    });
  }, [uid]);
  const searchBoxRef = useRef<HTMLDivElement | null>(null);

  // ── deep link (?tool=paper-trail&subject=…&year=…), applied once per load ──
  useEffect(() => {
    if (bootApplied) return;
    bootApplied = true;
    // A shared Topic Vault link (?subject=…&topic=…) opens the vault feed; the
    // feed itself consumes the target subject/topic. Wins over the paper-list
    // deep link when a valid topic is present.
    if (hasInitialVaultTopic()) { setView({ v: 'revise' }); return; }
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
      .sort((a, b) => paperTrailSubjectLabel(a).localeCompare(paperTrailSubjectLabel(b)));
    // The LCA archive group only surfaces for LCA students — everyone else
    // never sees Leaving Cert Applied subjects in their picker.
    const lca = (junior || !isLca ? [] : inCycle.filter(s => s.cycle === 'lca')).sort((a, b) =>
      paperTrailSubjectLabel(a).localeCompare(paperTrailSubjectLabel(b)),
    );
    const mineIds = [
      ...main.filter(s => matchesStudent(s, mineNames)).map(s => s.id),
      ...lca.filter(s => matchesStudent(s, mineNames)).map(s => s.id),
    ];
    return { main, lca, mineIds };
  }, [junior, isLca, studentSubjects, matchesStudent]);

  /**
   * Distinct-paper count. Count one language only — IV duplicates would ~double
   * it — preferring the English version. Irish-medium subjects (Irish) have NO
   * 'ev' entries at all, so fall back to whatever language they do carry ('iv')
   * rather than reporting 0 papers.
   */
  const paperCount = useCallback((id: string) => {
    const entries = PAPER_TRAIL_INDEX[id] ?? [];
    const countLang = entries.some(e => e.lang === 'ev')
      ? 'ev'
      : (entries[0]?.lang ?? 'ev');
    const n = entries
      .filter(e => e.lang === countLang)
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

  // Cross-year topic jump: resolve the sibling's paper from the index and open
  // it on the paper side, focused on the target question. Close must return the
  // student to wherever they launched from:
  //   - a Topic Vault (Revise feed) launch passes `from` → return to that feed,
  //     subject/topic restored;
  //   - Mock builder / Progress / Weakness Map / Review pass nothing → return to
  //     the screen that was on-screen when the jump was made (`prev`);
  //   - a jump made INSIDE the viewer inherits the previous viewer's returnTo,
  //     so the whole round-trip still ends where it began.
  const openCrossYear = useCallback((t: TopicSibling, from?: VaultOrigin) => {
    if (!subjectById.has(t.subjectId)) return;
    const entry = (PAPER_TRAIL_INDEX[t.subjectId] ?? []).find(
      e => e.year === t.year && e.level === t.level && e.lang === t.lang,
    );
    const item = entry?.papers.find(p => p.doc.f === t.fileid);
    if (!item) return;
    setView(prev => {
      const returnTo: View = from
        ? { v: 'revise', restore: from }
        : prev.v === 'viewer'
          ? prev.returnTo ?? { v: 'subject', subjectId: t.subjectId }
          : prev;
      return {
        v: 'viewer',
        subjectId: t.subjectId,
        year: t.year,
        level: t.level,
        lang: t.lang,
        item,
        side: 'paper',
        focusQuestion: t.n,
        returnTo,
      };
    });
  }, []);

  // ── local recents + pins (recentsStore) ──
  // Bumped whenever the localStorage-backed rails change, so home re-reads them.
  const [, bumpRails] = useState(0);

  // Record a recent (and the cross-tool last-visit for the home resume card)
  // whenever a paper is ACTUALLY opened in the viewer — this catches openItem,
  // the rails, cross-year jumps and deep links in one place. Idempotent, so a
  // StrictMode double-fire is harmless.
  useEffect(() => {
    if (view.v !== 'viewer') return;
    const subj = subjectById.get(view.subjectId);
    if (!subj) return;
    recordRecentOpen(
      uid,
      {
        key: recentKey(view.subjectId, view.year, view.level, view.lang, view.item.doc.f),
        subjectId: view.subjectId,
        year: view.year,
        level: view.level,
        lang: view.lang,
        fileid: view.item.doc.f,
        label: paperLabel(view.item.label),
        kind: view.side,
      },
      Date.now(),
    );
    recordVisit(uid, {
      kind: 'tool',
      id: 'paper-trail',
      label: 'Paper Trail',
      sub: `${paperTrailSubjectLabel(subj)} · ${view.year} · ${LEVEL_LABEL[view.level]}`,
    });
    bumpRails(n => n + 1);
  }, [view, uid]);

  const handleTogglePin = useCallback(
    (ref: Omit<PaperRef, 'at'>) => {
      togglePin(uid, ref, Date.now());
      bumpRails(n => n + 1);
    },
    [uid],
  );

  /** Open a stored (pinned/recent) paper — the live entry + item are resolved
   *  from the index so a stale stored record can never open a dead link. */
  const openStoredRef = useCallback(
    (r: PaperRef) => {
      const subj = subjectById.get(r.subjectId);
      const entry = (PAPER_TRAIL_INDEX[r.subjectId] ?? []).find(
        e => e.year === r.year && e.level === r.level && e.lang === r.lang,
      );
      const item = entry?.papers.find(p => p.doc.f === r.fileid);
      if (!subj || !entry || !item) return;
      openItem(subj, entry, item, r.kind);
    },
    [openItem],
  );

  if (!isLoaded) {
    return <LoadingState label="Opening the Paper Trail" />;
  }

  // ═══════════════════════ VIEWER ═══════════════════════
  if (view.v === 'viewer') {
    const subj = subjectById.get(view.subjectId)!;
    const key = recentKey(view.subjectId, view.year, view.level, view.lang, view.item.doc.f);
    const url = (kind: 'paper' | 'scheme', f: string) =>
      paperUrl(paperStoragePath(subj.cycle, subj.id, view.year, kind, f));
    // Image supplements (Geography aerial photo / map sheets and cousins) get
    // the lightbox — pdf.js has nothing to say about a JPEG.
    if (/\.jpg$/i.test(view.item.doc.f)) {
      return (
        <ImageViewer
          title={`${paperTrailSubjectLabel(subj)} · ${view.year}`}
          subtitle={`${paperLabel(view.item.label)} · ${LEVEL_LABEL[view.level]}${view.lang === 'iv' ? ' · Gaeilge' : ''}`}
          url={url('paper', view.item.doc.f)}
          onClose={() => setView(view.returnTo ?? { v: 'subject', subjectId: view.subjectId })}
        />
      );
    }
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
        title={`${paperTrailSubjectLabel(subj)} · ${view.year}`}
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
        onClose={() =>
          setView(view.returnTo ?? { v: 'subject', subjectId: view.subjectId })
        }
        onPosition={(side, page) => updatePage(key, page, side)}
      />
    );
  }

  // ═══════════════════════ REVISE BY TOPIC ═══════════════════════
  if (view.v === 'revise') {
    const inCycleTagged = taggedSubjects()
      .map(id => subjectById.get(id))
      .filter((s): s is PaperTrailSubject => !!s && (junior ? s.cycle === 'jc' : s.cycle !== 'jc'))
      .sort((a, b) => paperTrailSubjectLabel(a).localeCompare(paperTrailSubjectLabel(b)));
    const mineNames = new Set((studentSubjects ?? []).map(baseName));
    return (
      <ReviseByTopic
        subjects={inCycleTagged.map(s => ({ id: s.id, label: paperTrailSubjectLabel(s) }))}
        mineIds={inCycleTagged.filter(s => matchesStudent(s, mineNames)).map(s => s.id)}
        uid={uid}
        subjectLabel={subjectLabelForId}
        restore={view.restore}
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
      .sort((a, b) => paperTrailSubjectLabel(a).localeCompare(paperTrailSubjectLabel(b)));
    const mineNames = new Set((studentSubjects ?? []).map(baseName));
    return (
      <MockExamBuilder
        uid={uid}
        now={Date.now()}
        subjects={inCycleTagged.map(s => ({ id: s.id, label: paperTrailSubjectLabel(s) }))}
        mineIds={inCycleTagged.filter(s => matchesStudent(s, mineNames)).map(s => s.id)}
        subjectLabel={subjectLabelForId}
        onOpenQuestion={openCrossYear}
        onBack={() => setView({ v: 'home' })}
      />
    );
  }

  // ═══════════════════════ FLASHCARDS ═══════════════════════
  if (view.v === 'cards') {
    return <Flashcards uid={uid} now={Date.now()} onBack={() => setView({ v: 'home' })} />;
  }

  // ═══════════════════════ DAILY REVIEW (SRS) ═══════════════════════
  if (view.v === 'review') {
    return (
      <ReviewSession
        uid={uid}
        now={Date.now()}
        subjectLabel={subjectLabelForId}
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
        subjectLabel={subjectLabelForId}
        onDrill={openCrossYear}
        onBack={() => setView({ v: 'home' })}
        onStart={() => setView({ v: 'home' })}
        onRoute={route => {
          if (route === 'timed') setView({ v: 'mock' });
          else if (route === 'drill') setView({ v: 'revise' });
          else if (route === 'reflex') onOpenTool?.('command-word-reflex');
          else if (route === 'chair') onOpenTool?.('examiners-chair');
        }}
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
          {paperTrailSubjectLabel(subj)}
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
                          {/* Verified per-question answer map shipped for this paper —
                              tells students BEFORE opening that the Answers reveal is
                              available here (discoverability; coverage is per-paper). */}
                          {item.answers === 1 && item.scheme && (
                            <span
                              className="ml-2 inline-flex items-center gap-1 align-middle px-2 py-0.5 rounded-full text-[10.5px] font-sans font-bold"
                              style={{ backgroundColor: '#FDEEDF', color: '#8C3A0E' }}
                            >
                              <ListChecks size={11} aria-hidden /> Answers
                            </span>
                          )}
                        </p>
                        <span className="flex items-center gap-1 shrink-0">
                          <span className="text-[11px]" style={{ color: '#9e9186' }}>
                            {activeYear} · {LEVEL_LABEL[activeLevel]}
                          </span>
                          {(() => {
                            const pinRef: Omit<PaperRef, 'at'> = {
                              key: recentKey(subj.id, entry.year, entry.level, entry.lang, item.doc.f),
                              subjectId: subj.id,
                              year: entry.year,
                              level: entry.level,
                              lang: entry.lang,
                              fileid: item.doc.f,
                              label: paperLabel(item.label),
                              kind: 'paper',
                            };
                            const pinned = isPinned(uid, pinRef.key);
                            return (
                              <button
                                onClick={() => handleTogglePin(pinRef)}
                                aria-pressed={pinned}
                                aria-label={pinned ? `Unpin ${paperLabel(item.label)}` : `Pin ${paperLabel(item.label)} to your favourites`}
                                className="p-1 -mr-1 rounded-lg transition-transform active:translate-y-0.5"
                              >
                                <Star size={15} fill={pinned ? '#F26B1F' : 'none'} color={pinned ? '#F26B1F' : '#d0cdc8'} aria-hidden />
                              </button>
                            );
                          })()}
                        </span>
                      </div>
                      <div className="flex items-center gap-2.5">
                        <button
                          onClick={() => openItem(subj, entry, item, 'paper')}
                          className="flex-1 py-2.5 rounded-full text-[13.5px] font-semibold text-white transition-transform active:translate-y-0.5"
                          style={{ backgroundColor: '#F26B1F', boxShadow: '0 3px 0 #B54D14' }}
                        >
                          {/\.jpg$/i.test(item.doc.f) ? 'Image' : 'Paper'}
                          {item.doc.b > 0 && <span className="opacity-75 font-medium"> · {prettyBytes(item.doc.b)}</span>}
                        </button>
                        {item.scheme ? (
                          <button
                            onClick={() => openItem(subj, entry, item, 'scheme')}
                            className="flex-1 py-2.5 rounded-full text-[13.5px] font-semibold border-2 transition-transform active:translate-y-0.5"
                            style={{ borderColor: 'rgba(242,107,31,0.35)', color: '#F26B1F' }}
                          >
                            Marking scheme{item.scheme.b > 0 && <span className="opacity-70 font-medium"> · {prettyBytes(item.scheme.b)}</span>}
                          </button>
                        ) : /\.jpg$/i.test(item.doc.f) ? null : (
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
  const inCycle = (subjectId: string) => {
    const s = subjectById.get(subjectId);
    return !!s && (junior ? s.cycle === 'jc' : s.cycle !== 'jc');
  };
  // Pinned + recent rails from the per-account local store (recentsStore).
  const pins = listPins(uid).filter(p => inCycle(p.subjectId));
  const pinKeys = new Set(pins.map(p => p.key));
  const localRecents = listRecentOpens(uid).filter(r => inCycle(r.subjectId) && !pinKeys.has(r.key));
  // The local store is the rail's source of truth; accounts that predate it
  // fall back to the synced recents until the local store fills.
  const railRecents: PaperRef[] =
    localRecents.length > 0
      ? localRecents
      : recents
          .filter(r => !pinKeys.has(r.key))
          .slice(0, 6)
          .map(r => ({
            key: r.key,
            subjectId: r.subjectId,
            year: r.year,
            level: r.level,
            lang: r.lang,
            fileid: r.doc.f,
            label: paperLabel(r.label),
            kind: r.kind,
            at: 0,
          }));
  /** One card in the pinned/recent rails — body re-opens the exact paper, the
   *  star pins/unpins it. */
  const railCard = (r: PaperRef, pinned: boolean) => {
    const s = subjectById.get(r.subjectId)!;
    const saved = state.recents.find(x => x.key === r.key);
    const page = r.kind === 'scheme' ? saved?.schemePage : saved?.paperPage;
    return (
      <div
        key={r.key}
        className="relative shrink-0 min-w-[150px] rounded-2xl border-2 border-[#1A1A1A] dark:border-zinc-700 bg-white dark:bg-zinc-900 shadow-[3px_3px_0_0_#1A1A1A] dark:shadow-[3px_3px_0_0_#3f3f46] transition-transform hover:-translate-y-0.5"
      >
        <button onClick={() => openStoredRef(r)} className="block w-full text-left px-3.5 py-3 pr-8">
          <p className="text-[13px] font-bold leading-tight" style={{ color: '#1a1a1a' }}>
            {paperTrailSubjectLabel(s)} {r.year}
          </p>
          <p className="text-[11px] mt-0.5 flex items-center gap-1" style={{ color: '#7a7068' }}>
            <Clock3 size={11} aria-hidden />
            {r.label}
            {r.kind === 'scheme' ? ' · scheme' : ''}
            {page && page > 1 ? ` · p.${page}` : ''}
          </p>
          <p className="text-[10px] mt-0.5" style={{ color: '#9e9186' }}>{LEVEL_LABEL[r.level]}</p>
        </button>
        <button
          onClick={() => handleTogglePin(r)}
          aria-pressed={pinned}
          aria-label={pinned ? `Unpin ${paperTrailSubjectLabel(s)} ${r.year}` : `Pin ${paperTrailSubjectLabel(s)} ${r.year} to your favourites`}
          className="absolute top-2 right-2 p-1 rounded-lg transition-transform active:translate-y-0.5"
        >
          <Star size={13} fill={pinned ? '#F26B1F' : 'none'} color={pinned ? '#F26B1F' : '#d0cdc8'} aria-hidden />
        </button>
      </div>
    );
  };
  const showLcaSection =
    !junior &&
    groups.lca.length > 0 &&
    (scope === 'all' || groups.mineIds.length === 0 || groups.lca.some(s => groups.mineIds.includes(s.id)));
  const review = deckStats(uid, Date.now());
  // The Coach — tonight's session, composed across every tool's signals.
  const coachPlan = composeCoach(uid, Date.now());
  // The Sunday Debrief — weekly recap, shown Sun/Mon until dismissed (F11).
  const debriefDay = [0, 1].includes(new Date().getUTCDay());
  const debrief = debriefDay && !debriefSeen(uid, Date.now()) ? composeDebrief(uid, Date.now()) : null;
  // First-run coach: a live checklist that ticks as the student works the loop.
  const coachSteps = [
    { label: 'Open any paper beside its official marking scheme.', done: recents.length > 0 },
    { label: 'Mark yourself against it — tag where you lost the marks.', done: allMarks(uid).length > 0 },
    { label: 'Save a question to spaced review — we resurface it on schedule.', done: review.total > 0 },
  ];

  return (
    <div className="w-full max-w-xl mx-auto pb-12">
      {milestone && (
        <MilestoneCelebration milestone={milestone} dateIso={new Date(Date.now()).toISOString().slice(0, 10)} onClose={dismissMilestone} />
      )}
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
                  {paperTrailSubjectLabel(sug.subject)}
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
      <CountdownCard uid={uid} now={Date.now()} onboardingExamDate={onboardingExamDate} onOpen={() => setView({ v: 'progress' })} />

      {/* Practice streak + daily goal (B3) — hidden until first practice; opens
          the progress dashboard when tapped. */}
      <StreakStrip uid={uid} now={Date.now()} onOpen={() => setView({ v: 'progress' })} />

      {/* First-run coach — a live checklist of the loop; retires once it's running. */}
      <FirstRunCoach uid={uid} steps={coachSteps} />

      {/* The Sunday Debrief — the week in the student's own numbers (F11). */}
      {debrief && (
        <section className="rounded-2xl border-2 border-[#1a1a1a] dark:border-zinc-700 bg-white dark:bg-zinc-900 px-4 py-4 mb-6">
          <div className="flex items-start justify-between gap-2">
            <div>
              <p className="text-[10.5px] font-bold uppercase tracking-[0.12em] mb-1" style={{ color: '#9e9186' }}>The Sunday debrief</p>
              <h3 className="text-[16px] font-semibold mb-2" style={{ fontFamily: "'Source Serif 4', serif", color: '#1a1a1a' }}>
                {debrief.headline}
              </h3>
            </div>
            <button
              onClick={() => { markDebriefSeen(uid, Date.now()); setView({ v: 'home' }); }}
              aria-label="Dismiss debrief"
              className="p-1.5 rounded-lg text-[12px] font-semibold"
              style={{ color: '#9e9186' }}
            >
              ✕
            </button>
          </div>
          <ul className="space-y-1 mb-2">
            {debrief.lines.map((l, i) => (
              <li key={i} className="text-[13px] leading-relaxed" style={{ color: '#3a3530' }}>{l}</li>
            ))}
          </ul>
          {debrief.focus && (
            <p className="text-[12.5px] italic rounded-lg px-3 py-2" style={{ backgroundColor: '#FDEEDF', color: '#8C3A0E', borderLeft: '3px solid #F26B1F' }}>
              {debrief.focus}
            </p>
          )}
        </section>
      )}

      {/* The Coach — "your next 20 minutes", composed across every tool's signals. */}
      {coachPlan.length > 0 && (
        <section className="rounded-2xl border-2 border-[#1a1a1a] dark:border-zinc-700 bg-white dark:bg-zinc-900 px-4 py-3.5 mb-6">
          <div className="flex items-baseline justify-between mb-2.5">
            <h3 className="text-[15px] font-semibold" style={{ fontFamily: "'Source Serif 4', serif", color: '#1a1a1a' }}>
              Your next {coachPlan.reduce((a, i) => a + i.minutes, 0)} minutes
            </h3>
            <span className="text-[10.5px] font-bold uppercase tracking-[0.12em]" style={{ color: '#9e9186' }}>The Coach</span>
          </div>
          <div className="space-y-1.5">
            {coachPlan.map((item, i) => (
              <button
                key={item.id}
                onClick={() => {
                  if (item.route === 'chair') onOpenTool?.('examiners-chair');
                  else setView({ v: item.route });
                }}
                className="w-full flex items-center gap-3 rounded-xl border-2 border-[#d0cdc8] dark:border-zinc-700 px-3 py-2.5 text-left transition-transform active:translate-y-0.5 hover:border-[#F26B1F]"
              >
                <span
                  className="shrink-0 w-7 h-7 rounded-full flex items-center justify-center text-[13px] font-bold text-white"
                  style={{ backgroundColor: '#F26B1F', fontFamily: "'Source Serif 4', serif" }}
                >
                  {i + 1}
                </span>
                <span className="flex-1 min-w-0">
                  <span className="block text-[13.5px] font-semibold truncate" style={{ color: '#1a1a1a' }}>{item.title}</span>
                  <span className="block text-[11.5px] leading-snug" style={{ color: '#7a7068' }}>{item.sub}</span>
                </span>
                <span className="shrink-0 text-[11px] tabular-nums" style={{ color: '#9e9186' }}>~{item.minutes}m</span>
              </button>
            ))}
          </div>
        </section>
      )}

      {/* Study launcher — Topic Vault (A1). Review / Mock set / Cards are
          parked for now (2026-07-22); their views + stores remain intact. */}
      <button
        onClick={() => setView({ v: 'revise' })}
        className="w-full flex items-center gap-3 rounded-2xl border-2 border-[#1A1A1A] dark:border-zinc-700 bg-white dark:bg-zinc-900 shadow-[3px_3px_0_0_#1A1A1A] dark:shadow-[3px_3px_0_0_#3f3f46] px-4 py-3 mb-6 text-left transition-transform active:translate-y-0.5 hover:-translate-y-0.5"
      >
        <span className="shrink-0 w-9 h-9 rounded-xl flex items-center justify-center" style={{ backgroundColor: '#FDEEDF' }}>
          <Layers size={18} style={{ color: '#F26B1F' }} />
        </span>
        <span className="flex-1 min-w-0">
          <span className="block text-[14px] font-semibold" style={{ fontFamily: "'Source Serif 4', serif", color: '#1a1a1a' }}>Topic Vault</span>
          <span className="block text-[12px]" style={{ color: '#7a7068' }}>Every question by topic</span>
        </span>
      </button>

      {/* Pinned papers — favourites a grinding student keeps one tap away. */}
      {pins.length > 0 && (
        <>
          <h3 className="text-[11px] font-bold uppercase tracking-[0.14em] mb-2.5" style={{ color: '#9e9186' }}>
            Pinned
          </h3>
          <div className="flex gap-2.5 overflow-x-auto pb-2 mb-5 -mx-1 px-1">
            {pins.map(p => railCard(p, true))}
          </div>
        </>
      )}

      {/* Recents rail — the last papers this account actually opened. */}
      {railRecents.length > 0 && (
        <>
          <h3 className="text-[11px] font-bold uppercase tracking-[0.14em] mb-2.5" style={{ color: '#9e9186' }}>
            Pick up where you left off
          </h3>
          <div className="flex gap-2.5 overflow-x-auto pb-2 mb-5 -mx-1 px-1">
            {railRecents.map(r => railCard(r, false))}
          </div>
        </>
      )}

      {/* Your practice — self-mark weakness map (Tier 3). Renders only if the
          student has self-marked at least one question. */}
      <WeaknessMap
        uid={uid}
        subjectName={subjectLabelForId}
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
            label: paperTrailSubjectLabel(s),
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
              label: paperTrailSubjectLabel(s),
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
