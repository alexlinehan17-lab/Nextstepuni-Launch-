/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 *
 * The Examiner's Chair (Launchpad) — content types.
 *
 * A marking session puts the student on the examiner's side of the desk: an
 * exam-style question, the REAL marking rules that govern it (cited to SEC
 * marking schemes / Chief Examiner's Reports held in /examiner-reports), and a
 * set of authored sample answers ("scripts") to mark against those rules.
 *
 * Content honesty rules (verify-don't-guess, see
 * compliance/evidence/examiners-chair.md):
 *  - Questions and scripts are AUTHORED for the exercise and labelled as such —
 *    never presented as real candidate work or real SEC questions.
 *  - Every marking grid / scale and every credit rule cites the SEC document it
 *    comes from (`cite` fields). No rule appears without a source.
 *  - Each script embodies a DOCUMENTED examiner-flagged behaviour where one is
 *    claimed (`embodies.cite`).
 *
 * Two marking modes mirror how the two launch subjects are really marked:
 *  - Business HL: grid marking — per-point criteria like Name(2)+Explain(2)+
 *    Link(1); the student decides which criteria each attempt earned.
 *  - Maths: scale marking — the SEC scale system (B/C/D scales, low/mid/high
 *    partial credit, Full Credit −1); the student places the whole script on
 *    the scale, exactly like the examiner's right-margin annotation.
 */

export type ChairSubjectId = 'business' | 'maths';

/** A source citation shown in-app and recorded in the dossier. */
export interface ChairCite {
  /** Short label, e.g. "SEC Business HL marking scheme 2025, p.6". */
  label: string;
}

/** A documented examiner-flagged behaviour a script is built to embody. */
export interface EmbodiedInsight {
  /** What the script deliberately does, in plain words. */
  behaviour: string;
  cite: ChairCite;
}

/** The transferable rule the student keeps after a session. */
export interface CodexRule {
  id: string;
  rule: string;
  detail: string;
  cite: ChairCite;
}

// ─────────────────────────── Business: grid marking ───────────────────────────

/** One markable criterion within a point, e.g. Name (2m). */
export interface GridCriterion {
  id: string;
  label: string;
  marks: number;
}

/** One attempted point inside a script, marked against the per-point criteria. */
export interface PointAttempt {
  id: string;
  /** The authored answer text for this attempt. */
  text: string;
  /** Examiner's key: marks awarded per criterion (0 or the criterion's full marks). */
  key: Record<string, number>;
  /** Examiner rationale for this attempt, shown on reveal. */
  keyNote: string;
}

export interface GridScript {
  id: string;
  /** Display label, e.g. "Script A". */
  label: string;
  /** One-line persona so the scripts feel distinct, e.g. "Knows the theory cold". */
  persona: string;
  attempts: PointAttempt[];
  embodies?: EmbodiedInsight;
}

export interface GridSession {
  mode: 'grid';
  id: string;
  subject: 'business';
  title: string;
  /** The question cue this session trains, e.g. "Outline", "List", "Evaluate". */
  cue: string;
  /** Authored question (may include a short authored case for ABQ-style sessions). */
  caseText?: string;
  question: string;
  /** Honesty label: what real SEC template this is modelled on. */
  questionNote: string;
  grid: {
    /** Criteria applied to EACH point attempt. */
    perPoint: GridCriterion[];
    /** The marking rule in the scheme's own shorthand, e.g. "2@5 (2+2+1)". */
    shorthand: string;
    /** The rule that makes this grid interesting, in plain words. */
    ruleNote: string;
    cite: ChairCite;
  };
  scripts: GridScript[];
  takeaway: CodexRule;
}

// ───────────────────────────── Maths: scale marking ─────────────────────────────

/** One selectable credit level on the session's scale. */
export interface ScaleLevel {
  id: string;
  /** Official descriptor, e.g. "Low partial credit". */
  label: string;
  /** The examiner's right-margin annotation for this level, e.g. "L", "H", "F*". */
  annotation: string;
  marks: number;
}

export interface ScaleScript {
  id: string;
  label: string;
  persona: string;
  /** The authored solution, line by line, as it would appear in a script. */
  work: string[];
  /** Examiner's key: the id of the correct ScaleLevel. */
  keyLevelId: string;
  keyNote: string;
  embodies?: EmbodiedInsight;
}

export interface ScaleSession {
  mode: 'scale';
  id: string;
  subject: 'maths';
  title: string;
  cue: string;
  question: string;
  questionNote: string;
  scale: {
    /** Official scale name, e.g. "10C". */
    name: string;
    levels: ScaleLevel[];
    /** The scheme-style marking notes governing this question. */
    notes: string[];
    cite: ChairCite;
  };
  scripts: ScaleScript[];
  takeaway: CodexRule;
}

export type MarkingSession = GridSession | ScaleSession;

export interface ChairSubject {
  id: ChairSubjectId;
  label: string;
  /** One-line description of what marking literacy looks like in this subject. */
  tagline: string;
  sessions: MarkingSession[];
  /** The sources every rule in this subject's sessions traces to. */
  sources: ChairCite[];
}
