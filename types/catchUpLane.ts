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
}
