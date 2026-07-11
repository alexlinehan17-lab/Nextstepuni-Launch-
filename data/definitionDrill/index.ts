/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 *
 * Definition Drill — drill the exact mark-earning WORDING of the definitions the
 * SEC scheme awards marks for. Pick a subject → drill each term: see the prompt,
 * recall the wording, reveal the scheme's own allocation, self-rate.
 *
 * SOURCE OF TRUTH — DERIVED, NOT HAND-AUTHORED. This is a read-only projection of
 * the Marking Lens corpus (data/markingLens), whose every entry is authored ONLY
 * from a filed SEC marking scheme (examiner-reports/) and machine-checked. A
 * definition is projected ONLY when the lens part is a definition prompt AND its
 * `decoded` field carries the scheme's actual mark-earning WORDING — not just a
 * mark split. This is the accreditation-critical filter: open-ended terms whose
 * scheme fixes only a mark structure (e.g. Business "Explain the term X — state
 * 2m + develop 3m") carry no wording to reveal, so they are NOT drillable here
 * and are dropped. The `answer` is the scheme's wording verbatim from the lens;
 * Definition Drill invents nothing.
 */

import { MARKING_LENS } from '../markingLens';
import type { LensPart, QuestionLens } from '../markingLens/types';

const SUBJECT_LABELS: Record<string, string> = {
  business: 'Business',
  physics: 'Physics',
  chemistry: 'Chemistry',
  'agricultural-science': 'Agricultural Science',
  biology: 'Biology',
  geography: 'Geography',
  economics: 'Economics',
  'home-economics-s-and-s': 'Home Economics',
  engineering: 'Engineering',
  'construction-studies': 'Construction Studies',
  'design-and-communication-graphics': 'Design & Communication Graphics',
};

export interface DrillDefinition {
  /** Stable id: subjectId|year|level|lang|fileid|n|partIndex. */
  id: string;
  /** The term being defined — a label derived from the prompt (not an SEC claim). */
  term: string;
  /** The scheme's prompt, verbatim from the lens part's task. */
  prompt: string;
  /** The mark-earning wording, verbatim from the lens part's decoded field. */
  answer: string;
  /** Marks this definition carries in the scheme. */
  marks: number;
  subjectId: string;
  subjectLabel: string;
  /** SEC attribution string. */
  source: string;
}

/** A part is a definition prompt when its task asks to define/explain/state a
 *  term, law or principle. */
const DEFINITION_PROMPT =
  /^(explain what is meant by|explain the term|explain the terms|define|what is meant by|distinguish between|state .*\b(law|principle)\b|state the equation that defines)/i;

/** A `decoded` field is a MARK-SPLIT DESCRIPTION (carries no revealable wording)
 *  when it just narrates how the marks divide — e.g. "The explanation earns 2
 *  marks", "Correct answer, 3 marks", "Part (i): 8 marks", "the full gradient
 *  statement 4". Open-ended "explain the term X" parts (Business, Economics,
 *  Biology, Ag Science) carry only this; there is no scheme wording to reveal, so
 *  they are NOT drillable and are dropped. This is the accreditation-critical
 *  filter — a definition with no wording would leave the reveal empty or force
 *  invention. The fixed-wording definitions (laws, principles, SI-unit and
 *  quantity definitions in Physics and Chemistry) carry the real phrasing and
 *  survive. Every pattern below was confirmed against the full projected set. */
const MARK_SPLIT_ONLY = [
  /\bearns?\s+\d+\s+marks?\b/i,               // "earns 2 marks", "earns 10 marks"
  /^correct answer\b/i,                        // "Correct answer, 3 marks."
  /\bpart\s*\(i+\)\s*:/i,                       // "Part (i): 8 marks."
  /\bexample\s+\d/i,                            // "example 3", "example 4 marks"
  /\bworth\s+\d/i,                              // "a further point worth 5"
  /\bthe\s+(full|first|second|further)\s+[a-z ]*\b(statement|term|point)\b/i, // "the full gradient statement", "the first term earns"
  // Open-ended "explain the term X" parts (Business/Economics) narrate the mark
  // split with no wording. These patterns catch that shape without catching the
  // Chemistry "Two elements (real wording), N marks" or Physics "One N-mark
  // element: real wording" forms, which carry the actual phrasing.
  /\bstate\s*\(\d.*develop\s*\(\d/i,           // "State (2m) + develop (3m)"
  /\bfor\s+(the|its)\s+(explanation|development)\b/i, // "4 marks for the explanation, 2 for its development"
  /\d-mark elements?\s+of\s+the\b/i,            // "Two 3-mark elements of the explanation"
  /^three elements\b/i,                        // "Three elements: 4m + 2m + 1m"
  /\bboth terms treated\b/i,                    // "Both terms treated: state (2m) + develop (3m) each"
];
const isMarkSplitOnly = (decoded: string): boolean =>
  MARK_SPLIT_ONLY.some(re => re.test(decoded.trim()));

/** Strip the definition-prompt lead-in to leave a short term label. */
const termFromPrompt = (task: string): string => {
  const t = task
    .replace(/^explain what is meant by\s+/i, '')
    .replace(/^explain the terms?\s+/i, '')
    .replace(/^what is meant by(?:\s+the term)?\s+/i, '')
    .replace(/^define(?:\s+the|\s+a|\s+an)?\s+/i, '')
    .replace(/^state\s+/i, '')
    .replace(/^distinguish between\s+/i, '')
    .replace(/\s+\(.*?\)\s*$/, '') // drop a trailing act/qualifier in parens
    .replace(/[.,;:]\s*$/, '')
    .trim();
  return t.length >= 2 ? t : task;
};

const idFor = (subjectId: string, e: QuestionLens, partIndex: number): string =>
  `${subjectId}|${e.year}|${e.level}|${e.lang}|${e.fileid}|${e.n}|${partIndex}`;

const isDrillable = (p: LensPart): boolean =>
  DEFINITION_PROMPT.test(p.task.trim()) &&
  !isMarkSplitOnly(p.decoded) &&
  // a real definition wording has some substance beyond a mark tag
  p.decoded.replace(/\(\d+\s*m\)/gi, '').trim().length >= 12;

// Project one definition per drillable part. The EV/IV language mirror collapses
// to a single card per (subject, year, level, question, part), EV preferred.
const byKey = new Map<string, DrillDefinition>();
for (const s of MARKING_LENS) {
  for (const e of s.entries) {
    e.parts.forEach((p, i) => {
      if (!isDrillable(p)) return;
      const dedupeKey = `${s.subjectId}|${e.year}|${e.level}|${e.n}|${i}`;
      const existing = byKey.get(dedupeKey);
      if (existing && e.lang !== 'ev') return;
      byKey.set(dedupeKey, {
        id: idFor(s.subjectId, e, i),
        term: termFromPrompt(p.task),
        prompt: p.task,
        answer: p.decoded,
        marks: p.marks,
        subjectId: s.subjectId,
        subjectLabel: SUBJECT_LABELS[s.subjectId] ?? s.subjectId,
        source: `${e.cite} — © State Examinations Commission`,
      });
    });
  }
}

/** All drillable definitions, ordered subject → term. */
export const DRILL_DEFINITIONS: DrillDefinition[] = [...byKey.values()].sort(
  (a, b) => a.subjectLabel.localeCompare(b.subjectLabel) || a.term.localeCompare(b.term),
);

export interface DrillSubject {
  id: string;
  label: string;
  count: number;
}

/** Subjects that have at least one drillable definition, with counts. */
export function drillSubjects(): DrillSubject[] {
  const m = new Map<string, DrillSubject>();
  for (const d of DRILL_DEFINITIONS) {
    const found = m.get(d.subjectId);
    if (found) found.count += 1;
    else m.set(d.subjectId, { id: d.subjectId, label: d.subjectLabel, count: 1 });
  }
  return [...m.values()].sort((a, b) => a.label.localeCompare(b.label));
}

/** The definitions for one subject. */
export function definitionsForSubject(subjectId: string): DrillDefinition[] {
  return DRILL_DEFINITIONS.filter(d => d.subjectId === subjectId);
}
