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
 * Visual register: white archive surfaces, full charcoal outlines, existing
 * orange controls and the shared Source Serif / DM Sans type system.
 */

import React, { useCallback, useEffect, useMemo, useRef, useState } from 'react';
import { ArrowLeft, ArrowRight, Bookmark, Search } from 'lucide-react';
import PaperSelection, { LEVEL_LABEL, paperLabel } from './PaperSelection';
import './archive.css';
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
import { paperAnswersPath, paperStoragePath, paperUrl } from './storage';
import { hostedAnchorsUrl, preferredAnswersUrl } from './vaultResolve';
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

/** Keep Topic Atlas/Mock Builder inside the student's actual programme. LC
 * and LCA reuse several display names, so a name-only profile match must never
 * pull both syllabuses into "My subjects". */
export const paperTrailSubjectVisibleForProfile = (
  subject: Pick<PaperTrailSubject, 'cycle'>,
  junior: boolean,
  isLca: boolean,
) => junior
  ? subject.cycle === 'jc'
  : subject.cycle === 'lc' || (isLca && subject.cycle === 'lca');

export const paperTrailSubjectMatchesProfileCycle = (
  subject: Pick<PaperTrailSubject, 'cycle'>,
  junior: boolean,
  isLca: boolean,
) => subject.cycle === (junior ? 'jc' : isLca ? 'lca' : 'lc');

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
  | { v: 'saved' }
  | { v: 'practice' }
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
  onBack?: () => void;
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
  /** Open straight into a sub-surface (the Topic Atlas tool card mounts the
   *  same component aimed at the topic browser). */
  initialView?: 'revise';
}

const PaperTrail: React.FC<PaperTrailProps> = ({
  uid,
  studentSubjects,
  studentLevels,
  studentCycle,
  isLca = false,
  onboardingExamDate,
  onOpenTool,
  onBack,
  initialView,
}) => {
  const { state, isLoaded, recordRecent, updatePage, setFilters, finishReading } = usePaperFinder(uid);
  const junior = studentCycle === 'junior-cycle';

  const [view, setView] = useState<View>(initialView === 'revise' ? { v: 'revise' } : { v: 'home' });
  const [level, setLevel] = useState<PaperLevel | null>(null);
  const [lang, setLang] = useState<PaperLang | null>(null);
  const [year, setYear] = useState<number | null>(null);
  const [scope, setScope] = useState<'mine' | 'all'>('mine');
  const [query, setQuery] = useState('');
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
      ...main.filter(s => !isLca && matchesStudent(s, mineNames)).map(s => s.id),
      ...lca.filter(s => matchesStudent(s, mineNames)).map(s => s.id),
    ];
    return { main, lca, mineIds };
  }, [junior, isLca, studentSubjects, matchesStudent]);

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
      : PAPER_TRAIL_SUBJECTS.filter(s => s.cycle === 'lc' || (isLca && s.cycle === 'lca'));
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
  }, [query, junior, isLca]);

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
      openItem(subj, entry, item, r.kind === 'scheme' && item.scheme ? 'scheme' : 'paper');
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
          onClose={() => {
            setLevel(view.level);
            setLang(view.lang);
            setYear(view.year);
            setView(view.returnTo ?? { v: 'subject', subjectId: view.subjectId });
          }}
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
          hasAnswers
            ? preferredAnswersUrl(
                subj.id,
                view.year,
                view.item.doc.f,
                paperUrl(paperAnswersPath(subj.cycle, subj.id, view.year, view.item.doc.f)),
              )
            : undefined
        }
        focusAnchorsUrl={
          view.focusQuestion ? hostedAnchorsUrl(view.year, view.item.doc.f) : undefined
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
        onClose={() => {
          finishReading();
          setLevel(view.level);
          setLang(view.lang);
          setYear(view.year);
          setView(view.returnTo ?? { v: 'subject', subjectId: view.subjectId });
        }}
        onPosition={(side, page) => updatePage(key, page, side)}
      />
    );
  }

  // ═══════════════════════ REVISE BY TOPIC ═══════════════════════
  if (view.v === 'revise') {
    const inCycleTagged = taggedSubjects()
      .map(id => subjectById.get(id))
      .filter((s): s is PaperTrailSubject => (
        !!s && paperTrailSubjectVisibleForProfile(s, junior, isLca)
      ))
      .sort((a, b) => paperTrailSubjectLabel(a).localeCompare(paperTrailSubjectLabel(b)));
    const mineNames = new Set((studentSubjects ?? []).map(baseName));
    return (
      <ReviseByTopic
        subjects={inCycleTagged.map(s => ({ id: s.id, label: paperTrailSubjectLabel(s) }))}
        mineIds={inCycleTagged.filter(s => (
          paperTrailSubjectMatchesProfileCycle(s, junior, isLca)
          && matchesStudent(s, mineNames)
        )).map(s => s.id)}
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
      .filter((s): s is PaperTrailSubject => (
        !!s && paperTrailSubjectVisibleForProfile(s, junior, isLca)
      ))
      .sort((a, b) => paperTrailSubjectLabel(a).localeCompare(paperTrailSubjectLabel(b)));
    const mineNames = new Set((studentSubjects ?? []).map(baseName));
    return (
      <MockExamBuilder
        uid={uid}
        now={Date.now()}
        subjects={inCycleTagged.map(s => ({ id: s.id, label: paperTrailSubjectLabel(s) }))}
        mineIds={inCycleTagged.filter(s => (
          paperTrailSubjectMatchesProfileCycle(s, junior, isLca)
          && matchesStudent(s, mineNames)
        )).map(s => s.id)}
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
    const availableYears = [...new Set(slice.map(e => e.year))].sort((a, b) => b - a);
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

    return <PaperSelection
      key={subj.id}
      uid={uid} subject={subj} label={paperTrailSubjectLabel(subj)}
      level={activeLevel} lang={activeLang} langs={langsAtLevel}
      year={activeYear} years={yearCells} entry={entry}
      notice={requestedMissing ? `${year} isn’t available here — showing ${activeYear} instead.` : undefined}
      onLevel={lv => { setLevel(lv); setFilters({ lastLevel: lv }); setYear(null); }}
      onLang={lg => { setLang(lg); setFilters({ lastLang: lg }); setYear(null); }}
      onYear={setYear}
      onOpen={(selectedEntry, item, side) => openItem(subj, selectedEntry, item, side)}
      onSave={handleTogglePin}
      onBack={() => { setView({ v: 'home' }); setYear(null); }}
      onTopics={() => setView({ v: 'revise' })}
    />;
  }

  // Saved records always resolve against the live index before being offered.
  const isAvailable = (r: PaperRef) => {
    const s = subjectById.get(r.subjectId);
    return s && paperTrailSubjectVisibleForProfile(s, junior, isLca)
      && (PAPER_TRAIL_INDEX[r.subjectId] ?? []).some(e => e.year === r.year
        && e.level === r.level && e.lang === r.lang && e.papers.some(p => p.doc.f === r.fileid));
  };
  const syncedRecents: PaperRef[] = state.recents.map(r => ({
    key: r.key, subjectId: r.subjectId, year: r.year, level: r.level, lang: r.lang,
    fileid: r.doc.f, label: paperLabel(r.label), kind: r.kind, at: r.at,
  }));
  const mergedRecents = new Map<string, PaperRef>();
  for (const r of [...listRecentOpens(uid), ...syncedRecents]) {
    if (!mergedRecents.has(r.key) || mergedRecents.get(r.key)!.at <= r.at) mergedRecents.set(r.key, r);
  }
  const recents = [...mergedRecents.values()].filter(isAvailable).sort((a, b) => b.at - a.at).slice(0, 8);
  const pins = listPins(uid).filter(isAvailable);
  const lastOpened = recents[0];
  const homeBack = <button className="pt-text-button" onClick={() => setView({ v: 'home' })}><ArrowLeft size={20} aria-hidden /> Paper Trail</button>;

  if (view.v === 'saved') {
    const row = (r: PaperRef) => {
      const saved = isPinned(uid, r.key);
      const position = state.recents.find(p => p.key === r.key);
      const page = r.kind === 'scheme' ? position?.schemePage : position?.paperPage;
      return <article key={r.key} className="pt-saved-row">
        <button onClick={() => openStoredRef(r)}>
          <span className="pt-saved-title">{subjectLabelForId(r.subjectId)} · {r.label}</span>
          <span>{r.year} · {LEVEL_LABEL[r.level]} level · {r.lang === 'ev' ? 'English' : 'Gaeilge'}{r.kind === 'scheme' ? ' · Marking scheme' : ''}{page && page > 1 ? ` · Page ${page}` : ''}</span>
        </button>
        <button className="pt-save" onClick={() => handleTogglePin(r)} aria-pressed={saved} aria-label={`${saved ? 'Remove saved' : 'Save'} ${subjectLabelForId(r.subjectId)} ${r.year} ${r.label}`}><Bookmark size={20} fill={saved ? 'currentColor' : 'none'} aria-hidden /></button>
      </article>;
    };
    return <section className="pt-archive pt-saved">
      <nav className="pt-toolbar" aria-label="Paper Trail">{homeBack}</nav>
      <h1 className="pt-title">Saved papers</h1>
      <p className="pt-page-intro">Your papers, ready when you are.</p>
      {pins.length ? pins.map(row) : <p className="pt-notice">Tap the bookmark beside a paper to save it here.</p>}
      <h2 className="pt-section-heading">Recently opened</h2>
      {recents.length ? recents.map(row) : <p className="pt-notice">Papers you open will appear here so you can pick up where you left off.</p>}
    </section>;
  }

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

  if (view.v === 'practice') return <section className="pt-archive pt-practice">
      <nav className="pt-toolbar" aria-label="Paper Trail">{homeBack}</nav>
      <h1 className="pt-title">Practice tools</h1>
      <p className="pt-page-intro">Build on every paper you practise.</p>
      <button className="pt-topic-link" onClick={() => setView({ v: 'progress' })}>Your progress <ArrowRight size={18} aria-hidden /></button>
      <button className="pt-topic-link" onClick={() => setView({ v: 'revise' })}>Topic Atlas <ArrowRight size={18} aria-hidden /></button>
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
              onClick={() => { markDebriefSeen(uid, Date.now()); setView({ v: 'practice' }); }}
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

      {/* Your practice — self-mark weakness map (Tier 3). Renders only if the
          student has self-marked at least one question. */}
      <WeaknessMap
        uid={uid}
        subjectName={subjectLabelForId}
        onDrill={openCrossYear}
        onOpenDashboard={() => setView({ v: 'progress' })}
      />

  </section>;

  const subjects = [...groups.main, ...groups.lca];
  const visibleSubjects = scope === 'mine' ? subjects.filter(s => groups.mineIds.includes(s.id)) : subjects;
  const pickSubject = (id: string, selectedYear?: number, selectedLevel?: PaperLevel) => {
    setQuery('');
    setYear(selectedYear ?? null);
    setLevel(selectedLevel ?? null);
    setLang(null);
    setView({ v: 'subject', subjectId: id });
  };

  return <section className="pt-archive pt-home" aria-label="Paper Trail archive">
    {milestone && <MilestoneCelebration milestone={milestone} dateIso={new Date().toISOString().slice(0, 10)} onClose={dismissMilestone} />}
    <nav className="pt-toolbar" aria-label="Paper Trail">
      <button className="pt-text-button" onClick={onBack}><ArrowLeft size={20} aria-hidden /> Tools</button>
      <button className="pt-text-button" onClick={() => setView({ v: 'saved' })}><Bookmark size={18} aria-hidden /> Saved</button>
    </nav>
    <header className="pt-hero">
      <div><p className="pt-eyebrow">Your exam archive</p><h1 className="pt-title">Paper Trail</h1><p className="pt-subtitle">Exam papers &amp; marking schemes</p></div>
      <img src="/assets/tools/paper-trail.png" alt="" width={96} height={96} />
    </header>
    <div className="pt-search-area" ref={searchBoxRef}>
      <label className="pt-search"><Search size={20} aria-hidden /><input type="search" value={query} onChange={e => setQuery(e.target.value)} placeholder="Find a subject or paper" aria-label="Find a subject or paper" aria-controls={suggestions ? 'pt-search-results' : undefined} /></label>
      {suggestions && <div id="pt-search-results" className="pt-search-results" aria-label="Search results">
        {suggestions.length === 0 ? <p>No matches — try the subject’s full name.</p> : suggestions.map(sug =>
          <button key={sug.subject.id} onClick={() => pickSubject(sug.subject.id, sug.year, sug.level)}>
            <span>{paperTrailSubjectLabel(sug.subject)}{sug.subject.cycle === 'lca' ? ' · LCA' : ''}</span>
            {(sug.year || sug.level) && <span>{[sug.year, sug.level && LEVEL_LABEL[sug.level]].filter(Boolean).join(' · ')}</span>}
            <ArrowRight size={18} aria-hidden />
          </button>)}
      </div>}
    </div>
    {lastOpened && <div className="pt-resume">
      <div><p className="pt-eyebrow">Last opened</p><p className="pt-resume-name">{subjectLabelForId(lastOpened.subjectId)} · {lastOpened.label}</p><p>{lastOpened.year} · {LEVEL_LABEL[lastOpened.level]} level{lastOpened.kind === 'scheme' ? ' · Scheme' : ''}</p></div>
      <button className="pt-continue" onClick={() => openStoredRef(lastOpened)}>Continue <ArrowRight size={18} aria-hidden /></button>
    </div>}
    <div className="pt-scope" role="group" aria-label="Subject selection">
      <button aria-pressed={scope === 'mine'} onClick={() => setScope('mine')}>My subjects</button>
      <button aria-pressed={scope === 'all'} onClick={() => setScope('all')}>All subjects</button>
    </div>
    {visibleSubjects.length > 0 ? <div className="pt-subject-grid" aria-label={scope === 'mine' ? 'My subjects' : 'All subjects'}>
      {visibleSubjects.map(subject => <button key={subject.id} className="pt-subject-card" onClick={() => pickSubject(subject.id)}>
        <span className="pt-subject-name">{paperTrailSubjectLabel(subject)}</span>
        <span className="pt-subject-detail"><span>{LEVEL_LABEL[profileLevelFor(subject) ?? (state.lastLevel && subject.levels.includes(state.lastLevel) ? state.lastLevel : subject.levels[0])]} level{subject.cycle === 'lca' ? ' · LCA' : ''}</span><ArrowRight size={20} aria-hidden /></span>
      </button>)}
    </div> : <div className="pt-empty-subjects">
      <h2 className="pt-section-heading">Find your first paper</h2>
      <p>{scope === 'mine' ? 'Your subjects will appear here once you add them to your profile. You can browse the full archive now.' : 'Papers are being added — check back soon.'}</p>
      {scope === 'mine' && <button className="pt-open-paper" onClick={() => setScope('all')}>Browse all subjects</button>}
    </div>}
    <div className="pt-home-links">
      <button onClick={() => setView({ v: 'revise' })}>Topic Atlas <ArrowRight size={18} aria-hidden /></button>
      <button onClick={() => setView({ v: 'practice' })}>Practice tools <ArrowRight size={18} aria-hidden /></button>
    </div>
    <p className="pt-context">{junior ? 'Junior Cycle' : isLca ? 'Leaving Cert Applied' : 'Leaving Certificate'} · Your subjects, your levels</p>
  </section>;
};

export default PaperTrail;
