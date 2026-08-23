/**
 * Ways In — the source contract shared by Mark Bank, Paper Trail and the
 * support workspace.
 *
 * The contract deliberately carries the shape of an answer, never the answer
 * itself. A student can see how many pieces the task needs before attempting
 * it, but opening Ways In cannot leak a marking-scheme phrase.
 */

export type WaysInOrigin = 'mark-bank' | 'paper-trail';
export type WaysInMode = 'one-step' | 'show-me';
export type WaysInTextConfidence = 'verified' | 'pdf-text' | 'image-only';

export interface WaysInFigure {
  src: string;
  alt: string;
  attribution?: string;
}

export interface WaysInAnswerShape {
  /**
   * Number of distinct answer ideas or selectable parts PRINTED by the source.
   *
   * This must never be inferred from marking-scheme rows. It is optional
   * because many papers print a tariff without printing an answer count.
   */
  points?: number;
  /** Printed tariff for the whole question, when the source supplies one. */
  totalMarks?: number;
  /** A choice instruction such as “answer 4 of 6”, without answer content. */
  choice?: { answer: number; available: number };
  /** True when the official scheme permits alternative complete routes. */
  alternativeRoutes?: boolean;
}

export interface WaysInQuestionSource {
  id: string;
  origin: WaysInOrigin;
  subjectLabel: string;
  levelLabel?: string;
  year?: number;
  questionRef: string;
  /** Exact searchable wording from the source. Blank for an image-only paper. */
  questionText: string;
  /** Exact lead-in printed before the question, where the source separates it. */
  stem?: string;
  figure?: WaysInFigure;
  answerShape?: WaysInAnswerShape;
  textConfidence: WaysInTextConfidence;
  sourceLabel: string;
  sourceCopyright?: string;
}

export type QuestionHighlightKind = 'action' | 'constraint' | 'data' | 'content';

export interface QuestionHighlight {
  start: number;
  end: number;
  kind: QuestionHighlightKind;
  label: string;
}

export interface CommandDemand {
  surface: string;
  requiredAction: string;
  answerShape: string;
  commonTrap: string;
}

export interface WaysInStep {
  id: 'meet' | 'job' | 'boundaries' | 'shape' | 'attempt' | 'return';
  eyebrow: string;
  title: string;
  prompt: string;
}

export type WaysInPlanKind =
  | 'printed-parts'
  | 'calculation'
  | 'procedure'
  | 'explanation'
  | 'comparison'
  | 'direct';

export interface WaysInPlanPrompt {
  /** Stable within the generated frame; student work still stays session-only. */
  id: string;
  /** Neutral structural label, never an answer or marking-scheme phrase. */
  label: string;
  /** Exact paper wording that this planning row belongs to, when available. */
  sourceText?: string;
  placeholder: string;
}

export interface WaysInQuestionModel {
  exactText: string;
  lines: string[];
  /** Every distinct instruction safely detected, in printed order. */
  commands: CommandDemand[];
  /** First instruction, retained for the existing step-by-step workspace. */
  command: CommandDemand | null;
  givens: string[];
  constraints: string[];
  keywords: string[];
  /** A conservative planning frame derived from the printed question only. */
  planShape: {
    count: number;
    basis: 'printed' | 'flexible';
    /** Exact words from the question that justify a printed count. */
    evidence?: string;
    /** The visible paper structure that justifies the planning frame. */
    structure?: 'choice' | 'count-phrase' | 'parts' | 'blanks' | 'labels' | 'instructions';
  };
  /** Backwards-compatible alias for planShape.count. */
  expectedPoints: number;
  /** A question-shaped empty frame made only from visible paper wording. */
  planKind: WaysInPlanKind;
  planPrompts: WaysInPlanPrompt[];
  highlights: QuestionHighlight[];
  steps: WaysInStep[];
}
