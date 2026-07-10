/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 *
 * Diagram Vault — the real diagrams, graphs, maps and charts that appear in SEC
 * exams, browsable by subject. Studyclix and the grind sites sell "how to draw
 * the diagram" as video; this shows students the actual exam figures, decoded.
 *
 * SOURCE OF TRUTH — DERIVED, NOT HAND-AUTHORED. Every entry is a read-only
 * projection of a figure exhibit already carried (and verified when curated) by:
 *   - catchUpLaneData.ts  → RECOVERY_CARDS[].figure          (has a topic)
 *   - commandWordData.ts  → COMMAND_WORD_QUESTIONS[].figure  (has a questionRef)
 * Each such figure was cropped from a real paper and stored with a verified
 * `alt` description and an SEC `source` attribution ("SEC Leaving Certificate
 * Biology 2022 Higher Level, Q15 — © State Examinations Commission"). This module
 * invents NO figure metadata of its own, so the vault can never drift from the
 * verified exhibits it mirrors: fix a figure at its source and the vault follows.
 *
 * The `alt` is the honest payload here — it is the decoded description of the
 * diagram, written the same way the module dossiers are (no claim beyond what the
 * figure shows). We surface the figure, its exam source, and that description.
 */

import { RECOVERY_CARDS } from '../../catchUpLaneData';
import { COMMAND_WORD_QUESTIONS } from '../../commandWordData';

export interface DiagramEntry {
  /** Stable id derived from the figure's file path. */
  id: string;
  subjectId: string;
  subjectLabel: string;
  /** Topic label when the source exhibit carried one (catch-up-lane figures). */
  topicLabel: string | null;
  /** 'higher' | 'ordinary' | 'common' | null. */
  level: string | null;
  /** Exam year parsed from the SEC source string, when present. */
  year: number | null;
  /** A short exam reference when the source exhibit carried one (command-word). */
  questionRef: string | null;
  /** Public path to the figure PNG. */
  src: string;
  /** Verified, decoded description of the figure. */
  alt: string;
  /** SEC attribution string. */
  source: string;
}

const LEVEL_RE = /(Higher|Ordinary|Foundation|Common)\s+Level/i;
const YEAR_RE = /\b(20\d{2}|19\d{2})\b/;

const idFromSrc = (src: string): string =>
  src.replace(/^.*\/exam-figures\//, '').replace(/\.png$/i, '').replace(/[/\s]+/g, '-');

const parseYear = (source: string): number | null => {
  const m = source.match(YEAR_RE);
  return m ? Number(m[0]) : null;
};

const parseLevel = (source: string, fallback: string | null): string | null => {
  const m = source.match(LEVEL_RE);
  if (m) return m[1].toLowerCase();
  return fallback;
};

// Build keyed by src so a figure shared across sources appears once. Catch-up-lane
// entries are added first because they carry a topic; a later command-word entry
// for the same figure only fills gaps (never overwrites a known topic).
const bySrc = new Map<string, DiagramEntry>();

for (const c of RECOVERY_CARDS) {
  if (!c.figure) continue;
  const src = c.figure.src;
  if (bySrc.has(src)) continue;
  bySrc.set(src, {
    id: idFromSrc(src),
    subjectId: c.subjectId,
    subjectLabel: c.subjectLabel,
    topicLabel: c.topicLabel ?? null,
    level: parseLevel(c.figure.source, c.level ?? null),
    year: parseYear(c.figure.source),
    questionRef: null,
    src,
    alt: c.figure.alt,
    source: c.figure.source,
  });
}

for (const q of COMMAND_WORD_QUESTIONS) {
  if (!q.figure) continue;
  const src = q.figure.src;
  const existing = bySrc.get(src);
  if (existing) {
    // Fill a missing questionRef only; never clobber the richer catch-up entry.
    if (!existing.questionRef && q.questionRef) existing.questionRef = q.questionRef;
    continue;
  }
  bySrc.set(src, {
    id: idFromSrc(src),
    subjectId: q.subjectId,
    subjectLabel: q.subjectLabel,
    topicLabel: null,
    level: parseLevel(q.figure.source, q.level ?? null),
    year: parseYear(q.figure.source),
    questionRef: q.questionRef ?? null,
    src,
    alt: q.figure.alt,
    source: q.figure.source,
  });
}

/** All diagram entries, deduped by figure, ordered subject → year desc. */
export const DIAGRAM_VAULT: DiagramEntry[] = [...bySrc.values()].sort((a, b) =>
  a.subjectLabel.localeCompare(b.subjectLabel) || (b.year ?? 0) - (a.year ?? 0) || a.id.localeCompare(b.id),
);

export interface DiagramSubject {
  id: string;
  label: string;
  count: number;
}

/** Subjects that have at least one diagram, with counts, alphabetical. */
export function diagramSubjects(): DiagramSubject[] {
  const m = new Map<string, DiagramSubject>();
  for (const e of DIAGRAM_VAULT) {
    const s = m.get(e.subjectId);
    if (s) s.count += 1;
    else m.set(e.subjectId, { id: e.subjectId, label: e.subjectLabel, count: 1 });
  }
  return [...m.values()].sort((a, b) => a.label.localeCompare(b.label));
}

/** The diagrams for one subject, newest first. */
export function diagramsForSubject(subjectId: string): DiagramEntry[] {
  return DIAGRAM_VAULT.filter(e => e.subjectId === subjectId);
}

/** Distinct topic labels present for a subject (for the in-subject filter chips). */
export function topicsForSubjectDiagrams(subjectId: string): string[] {
  const set = new Set<string>();
  for (const e of DIAGRAM_VAULT) {
    if (e.subjectId === subjectId && e.topicLabel) set.add(e.topicLabel);
  }
  return [...set].sort((a, b) => a.localeCompare(b));
}
