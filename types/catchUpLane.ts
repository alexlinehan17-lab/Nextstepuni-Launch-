/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 *
 * Catch-Up Lane — absence-recovery micro-units.
 *
 * Tell the tool which subject you've fallen behind in; it hands you short,
 * self-contained "here's what you missed + one question to prove you got it"
 * units per topic, so a missed class stops silently becoming lost marks.
 *
 * Designed (2026-06-02) from evidence on where Irish DEIS Leaving Cert students
 * struggle: chronic absence is markedly higher in DEIS schools and depresses
 * attainment across all groups (one gap grinds can't buy back). Runs on the
 * EEF's two best bets — self-regulation (+7mo) and feedback (+6mo).
 *
 * Content is tagged to real curriculum.ts subject/subtopic IDs and authored
 * source-grounded, the same discipline as examRepsData.ts.
 */

export type RecoveryLevel = 'higher' | 'ordinary' | 'common';

/** The single retrieval question that proves the topic landed. Self-marked. */
export interface RecoveryCheck {
  /** One short question on the core of the topic. */
  prompt: string;
  /** What a strong answer says — revealed after the student has a go. */
  modelAnswer: string;
  /** The discrete things a full answer includes — the student ticks what they had. */
  needed: string[];
}

/** One absence-recovery micro-unit for a single curriculum subtopic. */
export interface RecoveryCard {
  /** Stable unique id, e.g. 'bio-cell-structure'. */
  id: string;
  /** curriculum.ts subject id, e.g. 'biology'. */
  subjectId: string;
  /** curriculum.ts subtopic id, e.g. 'biology-1-0'. */
  topicId: string;
  subjectLabel: string;
  topicLabel: string;
  /**
   * Optional short, specific row label shown in the topic list when a subtopic
   * has more than one card (e.g. two "Calculus" cards → "Differentiation" vs
   * "Slope from a graph"). Falls back to topicLabel when absent.
   */
  focus?: string;
  level: RecoveryLevel;
  /** "The 90-second version" — the core idea, plain language. */
  gist: string;
  /** "The one move that matters" — the single most exam-relevant point. */
  oneMove: { label: string; text: string };
  check: RecoveryCheck;
  /** Citation for the content (syllabus / examiner guidance). */
  source: string;
  /** Conservative heuristic: roughly how many marks this topic protects. */
  marksWeight: number;
  /**
   * Optional figure for visually-dependent topics (a graph, diagram, map, or
   * comprehension extract a description can't replace). Cropped from the real
   * SEC paper via tools/extract_exam_figure.py and stored under public/exam-figures/.
   * `source` MUST carry the SEC attribution (used under NextStepUni's SEC agreement).
   */
  figure?: { src: string; alt: string; source: string };
  /**
   * Optional comprehension passage, shown VERBATIM (under NextStepUni's SEC
   * agreement) in a scrollable reading panel — for prose-comprehension topics
   * where the student must read the actual text to answer. The right medium for
   * prose (selectable, reflows, accessible), as opposed to `figure` for diagrams/
   * graphs/maps. `source` MUST carry the SEC attribution.
   */
  passage?: { text: string; source: string };
}

/** A light, optional record of days the student flagged as missed. */
export interface AbsenceLog {
  /** ISO date yyyy-mm-dd. */
  dateKey: string;
  subjectIds: string[];
}

/** Persisted under progress/{uid}.catchUpLane (additive-merge namespace). */
export interface CatchUpLaneState {
  /** Subtopic ids the student marked recovered. */
  recoveredTopicIds: string[];
  /** Subtopic ids marked "still shaky" — resurface first. */
  shakyTopicIds: string[];
  /** Total micro-units completed. */
  attempts: number;
  /** Light absence log (used only for friendly framing, not topic mapping). */
  absences: AbsenceLog[];
  /** Arm 2: the student's saved re-entry plan (see ComebackPlan). */
  comeback?: ComebackPlan;
  updatedAt: string;
}

/**
 * Per-day progress on the First-Week-Back timeline (Arm 2's living layer).
 * Shame stays designed out: a softened day is acknowledged, never penalised.
 */
export interface FirstWeekDayProgress {
  /** ISO timestamp set when the student marks the day done. */
  doneAt?: string;
  /** True once the student has tapped "not today" — softens the copy, never scolds. */
  softened?: boolean;
  /** One quiet end-of-day reflection line (SRL self-reflection phase). */
  reflection?: string;
}

/**
 * Arm 2's living timeline: a graded 5-day re-entry walk seeded from the saved
 * plan. Turns a static record into plan → do the tiny thing → reflect → next.
 */
export interface FirstWeekProgress {
  /** ISO timestamp when the student first opened the timeline. */
  startedAt: string;
  /** Per-day progress, keyed by day number (1–5). */
  days: Record<number, FirstWeekDayProgress>;
}

/**
 * Arm 2 ("Your Comeback") — a saved, personal re-entry plan the student builds.
 * Grounded in EBSA / NEPS guidance + implementation-intentions evidence:
 * a personal why, the obstacle that triggers avoidance, one tiny graded step,
 * an if-then plan against that obstacle, a low-disclosure script, and their one
 * trusted adult + safe space. Shame is designed out (no "why were you out?",
 * no days-missed counters).
 */
export interface ComebackPlan {
  /** A personally meaningful reason it matters (powers the if-then). */
  why: string;
  /** Worry ids the student named as what's hard (obstacles). */
  obstacleIds: string[];
  /** The tiny, almost-guaranteed first step (graded exposure). */
  firstStep: string;
  /** Implementation intention against the named obstacle. */
  ifThen: { trigger: string; action: string };
  /** Chosen low-disclosure line for the "where were you?" moment. */
  script: string;
  /** Their one trusted adult (role label, e.g. "My year head"). */
  person: string;
  /** Where they'll go / their exit signal if it gets too much. */
  safeSpace: string;
  savedAt: string;
  /** The living 5-day re-entry timeline built on top of this plan (added lazily). */
  firstWeek?: FirstWeekProgress;
}
