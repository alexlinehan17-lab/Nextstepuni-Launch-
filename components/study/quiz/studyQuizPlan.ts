/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 *
 * Which Mark Bank questions an end-of-session quiz asks, and how it scores
 * them. Pure, so it can be tested without the page.
 *
 * Selection, in order:
 *   1. The session's subject names a Mark Bank deck at the student's level
 *      (the same rule Mark Bank itself uses to open on the right deck).
 *   2. The session's topics narrow the deck through the curriculum registry,
 *      so a whole area expands to its topics and an older cohort's ids still
 *      reach the cards. No topics, or too few cards on them: the whole subject.
 *   3. Only SHORT, self-contained questions qualify: a fixed tariff of ten
 *      marks or fewer, no source booklet, no audio, no alternative routes. A
 *      quick check should take five minutes, not become a second session.
 *   4. Mark Bank's own scheduler orders them — due cards and weak memories
 *      first, then new ones — so the quiz is also spaced repetition.
 *
 * Fewer than three qualifying cards means no quiz at all. Padding with
 * invented questions is never an option: everything shown is lifted from a
 * paper and its scheme.
 *
 * Scoring mirrors Mark Bank's `marksClaimed` / `suggestGrade` for the subset of
 * cards this module admits (fixed tariff, no routes, no bonus). A test pins
 * that parity, so a tick here is worth exactly what it is worth there.
 */

import { SUBJECTS, deckSize, levelsFor, loadCards, type Level } from '../../MarkBank/deck';
import { cardsForCurriculumNode } from '../../MarkBank/curriculumMenu';
import { resolveSessionQueue } from '../../MarkBank/sessionPlanning';
import { readLocal } from '../../MarkBank/store';
import type { CardMemory, MarkBankGrade } from '../../MarkBank/scheduler';
import { CURRICULUM_SPECIFICATIONS, findCanonicalTopic, resolveSubjectId, type CanonicalCurriculumSpecification } from '../../../curriculumRegistry';
import { sameStudySubject } from '../../../services/studyTopicHistory';
import { groupMarks, isPointCard, rowId, type MarkRow, type SecCard, type SecQuestionCard } from '../../../types/markBank';
import type { StudyTopicSelection } from '../../../types/studyTopics';

/** Questions per quiz, and the fewest worth asking. */
export const QUIZ_SIZE = 4;
export const QUIZ_MIN = 3;
/** A "short" question: this many marks or fewer, this many scheme rows or fewer. */
export const QUIZ_MAX_MARKS = 10;
export const QUIZ_MAX_ROWS = 6;

export interface QuizDeck {
  subjectId: string;
  level: Level;
  title: string;
  /** Mark Bank's review deck for this subject and level (`progress/{uid}/srs/{deckId}`). */
  deckId: string;
}

export interface ProfileSubjectLike {
  subjectName: string;
  level?: string;
}

/**
 * The deck a session's subject maps to, or null when Mark Bank has nothing
 * built for it. Mirrors Mark Bank's own profile default: a one-level subject
 * uses that level; otherwise Ordinary and Foundation students get Ordinary and
 * everyone else Higher.
 */
export function resolveQuizDeck(
  subjectName: string,
  canonicalSubjectId: string | undefined,
  profileSubjects?: readonly ProfileSubjectLike[],
): QuizDeck | null {
  const canonical = (canonicalSubjectId && resolveSubjectId(canonicalSubjectId)) || resolveSubjectId(subjectName);
  if (!canonical) return null;
  const subject = SUBJECTS.find(item => resolveSubjectId(item.id) === canonical);
  if (!subject) return null;
  const profile = profileSubjects?.find(item => sameStudySubject(item.subjectName, subjectName));
  const levels = levelsFor(subject.id);
  const level: Level = levels.length === 1
    ? levels[0]
    : /^(ordinary|foundation)/i.test(profile?.level ?? '') ? 'ordinary' : 'higher';
  if (deckSize(subject.id, level) <= 0) return null;
  return { subjectId: subject.id, level, title: subject.title, deckId: `${subject.id}-${level}` };
}

/** A question short and self-contained enough for a five-minute check. */
export function isQuizCard(card: SecCard): card is SecQuestionCard {
  if (!isPointCard(card) || card.kind !== 'question') return false;
  if (card.tariffModel.kind !== 'fixed') return false;
  if (card.totalMarks <= 0 || card.totalMarks > QUIZ_MAX_MARKS) return false;
  if (card.sourceMaterial || card.additionalSourceMaterials?.length || card.audioMaterial) return false;
  if (card.answerVariants?.length || card.taskGroups?.length || card.questionBonus) return false;
  if (!card.rows.length || card.rows.length > QUIZ_MAX_ROWS) return false;
  // Mutually exclusive routes and unpriced rows need Mark Bank's full screen.
  return card.rows.every(row => !row.route && (row.marks !== null || (row.kind === 'anyN' && !!row.group)));
}

function dedupe(cards: SecCard[]): SecCard[] {
  const seen = new Set<string>();
  return cards.filter(card => !seen.has(card.id) && seen.add(card.id));
}

/** The quiz-worthy cards on the given topics (every card when no topics are given). */
export function quizPool(cards: SecCard[], topicIds: readonly string[], spec?: CanonicalCurriculumSpecification): SecQuestionCard[] {
  const scoped = topicIds.length ? dedupe(topicIds.flatMap(id => cardsForCurriculumNode(id, cards, spec))) : cards;
  return scoped.filter(isQuizCard);
}

/** Order by Mark Bank's scheduler and take the quiz's worth; nothing if too few. */
export function planQuiz(
  pool: SecQuestionCard[],
  memories: Record<string, CardMemory | undefined>,
  now: number,
  examTs?: number,
  size = QUIZ_SIZE,
): SecQuestionCard[] {
  if (pool.length < QUIZ_MIN) return [];
  return resolveSessionQueue(pool, memories, now, examTs, size).filter(isQuizCard);
}

export function specificationFor(selection?: StudyTopicSelection): CanonicalCurriculumSpecification | undefined {
  return selection ? CURRICULUM_SPECIFICATIONS.find(spec => spec.id === selection.specificationId) : undefined;
}

/** "Thermochemistry", "Rivers and Coasts", or "Rivers and 2 more topics". */
export function quizTopicLabel(selection?: StudyTopicSelection): string | null {
  const spec = specificationFor(selection);
  if (!spec || !selection?.topicIds.length) return null;
  const names = selection.topicIds
    .map(id => spec.groups.find(group => group.id === id)?.title ?? findCanonicalTopic(spec, id)?.title)
    .filter((name): name is string => Boolean(name));
  if (!names.length) return null;
  if (names.length <= 2) return names.join(' and ');
  return `${names[0]} and ${names.length - 1} more topics`;
}

// ─── Scoring ────────────────────────────────────────────────────────────────

/** 'yes' for a ticked row, a number for a stepped criterion, 'no' otherwise. */
export type QuizClaim = 'no' | 'yes' | number;

export interface QuizAnswer {
  claims: Record<string, QuizClaim>;
  /** `anyN` groups: which options were ticked, by index. */
  picks: Record<string, number[]>;
}

export const EMPTY_ANSWER: QuizAnswer = { claims: {}, picks: {} };

export interface QuizResult {
  cardId: string;
  questionRef: string;
  marksClaimed: number;
  marksAvailable: number;
  grade: MarkBankGrade;
}

export const rowKey = rowId;

/** What a row is worth when fully claimed (`anyN` groups: their claimable max). */
export function rowValue(row: MarkRow): number {
  if (row.kind === 'anyN' && row.group) return groupMarks(row.group);
  return row.marks ?? 0;
}

/** Marks a student can claim on the card — the fixed tariff's rows, summed. */
export function cardMarks(card: SecQuestionCard): number {
  return card.rows.reduce((sum, row) => sum + rowValue(row), 0);
}

function groupClaimed(group: NonNullable<MarkRow['group']>, chosen: number): number {
  if (!group.perOptionSteps) return chosen * group.perOption;
  return group.perOptionSteps.slice(0, chosen).reduce((sum, marks) => sum + marks, 0);
}

export function marksEarned(card: SecQuestionCard, answer: QuizAnswer): number {
  return card.rows.reduce((sum, row, index) => {
    const key = rowKey(row, index);
    if (row.kind === 'anyN' && row.group) {
      const chosen = Math.min(answer.picks[key]?.length ?? 0, row.group.claimMax);
      return sum + groupClaimed(row.group, chosen);
    }
    const claim = answer.claims[key] ?? 'no';
    if (row.permittedMarks) {
      if (claim === 'yes') return sum + (row.marks ?? 0);
      return sum + (typeof claim === 'number' && row.permittedMarks.includes(claim) ? claim : 0);
    }
    const claimed = typeof claim === 'number' ? claim > 0 : claim !== 'no';
    return claimed ? sum + rowValue(row) : sum;
  }, 0);
}

/** The grade the ticks point at: all the marks, some, or none. */
export function quizGrade(card: SecQuestionCard, answer: QuizAnswer): MarkBankGrade {
  const got = marksEarned(card, answer);
  if (got <= 0) return 'missed';
  return got >= cardMarks(card) ? 'got' : 'shaky';
}

// ─── Loading ────────────────────────────────────────────────────────────────

export interface LoadedQuiz {
  deck: QuizDeck;
  cards: SecQuestionCard[];
  /** How many quiz-worthy cards the scope holds, so four never poses as the lot. */
  poolTotal: number;
  /** The studied topics by name, or null when the quiz had to widen to the subject. */
  topicLabel: string | null;
}

export async function loadQuiz(input: {
  uid: string;
  subjectName: string;
  topicSelection?: StudyTopicSelection;
  profileSubjects?: readonly ProfileSubjectLike[];
  examDate?: string | null;
  now: number;
}): Promise<LoadedQuiz | null> {
  const deck = resolveQuizDeck(input.subjectName, input.topicSelection?.subjectId, input.profileSubjects);
  if (!deck) return null;
  const cards = await loadCards(deck.subjectId, deck.level);
  const topicIds = input.topicSelection?.topicIds ?? [];
  let pool = quizPool(cards, topicIds, specificationFor(input.topicSelection));
  let onTopics = topicIds.length > 0;
  if (pool.length < QUIZ_MIN) { pool = quizPool(cards, []); onTopics = false; }
  const local = readLocal(input.uid, deck.deckId);
  const picked = planQuiz(pool, local.cards, input.now, local.examTs);
  if (!picked.length) return null;
  return { deck, cards: picked, poolTotal: pool.length, topicLabel: onTopics ? quizTopicLabel(input.topicSelection) : null };
}
