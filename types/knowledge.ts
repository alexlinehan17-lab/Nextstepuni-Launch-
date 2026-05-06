/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 *
 * Necessary Knowledge tab — types shared across the tab's components and
 * its data files. All content here traces to /docs/leaving-cert-knowledge-
 * dossier.md, which itself is sourced from SEC marking schemes, Chief
 * Examiner Reports, and NCCA documents. Every entry below carries a
 * `source` reference back into the dossier.
 */

/** A pointer back into the dossier, so any claim is auditable. */
export interface DossierRef {
  /** Section identifier from the dossier — e.g. "A1", "B1", "D". */
  section: string;
  /** Approximate page in the markdown / source PDF. */
  page?: number;
  /** Optional line — the original source the dossier itself cites
   *  (e.g. "2013 Chief Examiner Report — English"). */
  cite?: string;
}

// ─── Command Word Decoder (E1) ──────────────────────────────────────────

export interface CommandWordEntry {
  word: string;
  /** What this command word actually demands. One sentence. */
  requiredAction: string;
  /** Typical mark range where this command appears. */
  typicalMarkRange: string;
  /** Structural template for the answer. */
  structuralTemplate: string;
  /** Specific common error from CERs / marking schemes for this word. */
  commonError: string;
  /** Optional aliases — words treated as equivalent (e.g. "Assess" → "Evaluate"). */
  aliases?: string[];
  source: DossierRef;
}

/** Modifiers are words that change the demand around a command word —
 *  "significant", "effective", "deeply embedded". The Purpose marks in
 *  English live in these. Dossier A1 p.3. */
export interface ModifierEntry {
  word: string;
  /** What this modifier signals about the demand. */
  signal: string;
  source: DossierRef;
}

// ─── Examiner Pet-Peeve Trainer (E12) ──────────────────────────────────

export interface ExaminerPetPeeve {
  id: string;
  subject: string;
  /** Paraphrased summary of the peeve. Never more than 15 words verbatim
   *  per source, per /CLAUDE.md content quality rules. */
  peeve: string;
  /** Year of the underlying Chief Examiner Report or marking scheme. */
  reportYear: number;
  /** A worked example of what triggers it. */
  example: string;
  /** The fix — one specific, actionable behaviour. */
  fix: string;
  source: DossierRef;
}

// ─── Marking Scheme Grammar Explainer (E2-cousin) ──────────────────────

export interface MarkingGrammarRule {
  title: string;
  body: string;
}

export interface SubjectMarkingGrammar {
  id: string;
  subjectLabel: string;
  /** Short narrative — the architecture of how this subject is marked. */
  architecture: string;
  rules: MarkingGrammarRule[];
  /** Optional worked example showing the marking applied. */
  workedExample?: { setup: string; outcome: string };
  source: DossierRef;
}

// ─── Time-Allocation Calculator (E3) ───────────────────────────────────

export interface SubjectTimingBreakdown {
  section: string;
  marks: number;
  minutes: number;
}

export interface SubjectTiming {
  id: string;
  subjectLabel: string;
  totalMarks: number;
  totalMinutes: number;
  /** Mock breakdown of how to spend the time across sections. */
  breakdown: SubjectTimingBreakdown[];
  source: DossierRef;
}

// ─── Quick-Check (used at end of every module) ─────────────────────────

export interface QuickCheckQuestion {
  id: string;
  prompt: string;
  options: string[];
  correctAnswer: string;
  /** Brief explanation shown after answering. */
  explanation: string;
}
