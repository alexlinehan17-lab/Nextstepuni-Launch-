/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 *
 * Paper Trail — bridges a paper's identity (subjectId + paper label + level) to
 * the verified Necessary-Knowledge datasets: SUBJECT_TIMING (drives the
 * time-budget chips + exam-mode clock) and SUBJECT_MARKING_GRAMMARS (drives the
 * "How this subject is marked" card). Both datasets are keyed by their own ids;
 * this is the single place that maps the paper-trail subjectId across.
 *
 * Where no official timing exists the caller falls back to a generic,
 * proportional-to-marks pace (see textOverlay.totalMarks) — nothing is invented.
 */

import { SUBJECT_TIMING } from '../../data/knowledge/subjectTiming';
import { SUBJECT_MARKING_GRAMMARS } from '../../data/knowledge/subjectMarkingGrammar';
import type { SubjectTiming, SubjectMarkingGrammar } from '../../types/knowledge';

const timingById = new Map(SUBJECT_TIMING.map(t => [t.id, t]));
const grammarById = new Map(SUBJECT_MARKING_GRAMMARS.map(g => [g.id, g]));

// Corpus labels are worded ("Paper One" / "Paper Two"), not numeric — match
// both forms plus the roman "II".
const isPaper2 = (label: string) => /paper\s*(?:2|two|ii)\b/i.test(label);

/** Resolve the official timing for a paper, if the subject has one. English and
 *  Irish split by paper (their two papers are timed very differently), so the
 *  paper label disambiguates. Returns null → caller uses the generic fallback. */
export function timingFor(subjectId: string, paperLabel: string): SubjectTiming | null {
  switch (subjectId) {
    case 'english':
      return timingById.get(isPaper2(paperLabel) ? 'english-p2' : 'english-p1') ?? null;
    case 'irish':
      // Only Paper 2 (comprehension + literature) has a modelled breakdown;
      // Paper 1 (aural + written) is structured differently — stay generic.
      return isPaper2(paperLabel) ? (timingById.get('irish-p2') ?? null) : null;
    case 'mathematics':
      return timingById.get('maths') ?? null;
    case 'geography':
      return timingById.get('geography') ?? null;
    case 'business':
      return timingById.get('business') ?? null;
    case 'accounting':
      return timingById.get('accounting') ?? null;
    case 'biology':
      return timingById.get('biology') ?? null;
    case 'chemistry':
      return timingById.get('chemistry') ?? null;
    case 'physics':
      return timingById.get('physics') ?? null;
    case 'history':
      return timingById.get('history') ?? null;
    case 'french':
    case 'german':
    case 'spanish':
    case 'italian':
      return timingById.get('mfl') ?? null;
    default:
      return null;
  }
}

/** Resolve the marking-scheme grammar card for a subject, if one applies. */
export function grammarFor(subjectId: string): SubjectMarkingGrammar | null {
  switch (subjectId) {
    case 'english':
      return grammarById.get('english-pclm') ?? null;
    case 'geography':
    case 'history':
    case 'history-early-modern':
    case 'business':
      return grammarById.get('srp-system') ?? null;
    case 'mathematics':
      return grammarById.get('maths-attempt') ?? null;
    case 'accounting':
      return grammarById.get('accounting') ?? null;
    case 'biology':
    case 'chemistry':
    case 'physics':
      return grammarById.get('sciences') ?? null;
    default:
      return null;
  }
}
