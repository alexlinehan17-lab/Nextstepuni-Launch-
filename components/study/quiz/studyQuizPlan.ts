/**
 * End-of-session questions use the saved canonical topic selection and the
 * student's Mark Bank deck. Never broaden a sparse topic to the whole subject.
 * Native Mark Bank renders and scores every selected question.
 */

import { SUBJECTS, deckSize, levelsFor, loadCards, type Level } from '../../MarkBank/deck';
import { cardsForCurriculumNode } from '../../MarkBank/curriculumMenu';
import { resolveSessionQueue } from '../../MarkBank/sessionPlanning';
import { readLocal } from '../../MarkBank/store';
import type { CardMemory } from '../../MarkBank/scheduler';
import { CURRICULUM_SPECIFICATIONS, findCanonicalTopic, resolveSubjectId, type CanonicalCurriculumSpecification } from '../../../curriculumRegistry';
import { canonicalNodeIds, sameStudySubject } from '../../../services/studyTopicHistory';
import { isPointCard, type SecCard } from '../../../types/markBank';
import { libraryTopicIds } from '../../MarkBank/libraryGroups';
import type { SessionCardResult } from '../../MarkBank/SessionScreen';
import type { StudyTopicSelection } from '../../../types/studyTopics';

/** Questions per quiz, and the fewest worth asking. */
export const QUIZ_SIZE = 4;
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

/** Short questions, including native rubric allocations and source readers. */
export function isQuizCard(card: SecCard): boolean {
  if (card.totalMarks <= 0 || card.totalMarks > QUIZ_MAX_MARKS || card.audioMaterial) return false;
  // Long listening exercises do not fit a quick check. All other question,
  // source and scoring formats are handled by the native Mark Bank screen.
  return !isPointCard(card) || (card.tariffModel.kind === 'fixed' && card.rows.length > 0
    && card.rows.length <= QUIZ_MAX_ROWS && card.rows.every(row => row.marks !== null || Boolean(row.group)));
}

function dedupe(cards: SecCard[]): SecCard[] {
  const seen = new Set<string>();
  return cards.filter(card => !seen.has(card.id) && seen.add(card.id));
}

/** The quiz-worthy cards on the given topics (every card when no topics are given). */
export function quizPool(cards: SecCard[], topicIds: readonly string[], spec?: CanonicalCurriculumSpecification): SecCard[] {
  const scoped = topicIds.length ? dedupe(topicIds.flatMap(id => cardsForCurriculumNode(id, cards, spec))) : cards;
  return scoped.filter(isQuizCard);
}

/** Give each selected topic a turn, then fill in scheduler order, without duplicates. */
export function planQuiz(
  pool: SecCard[],
  memories: Record<string, CardMemory | undefined>,
  now: number,
  examTs?: number,
  size = QUIZ_SIZE,
  topicPools: SecCard[][] = [],
): SecCard[] {
  if (!pool.length || size <= 0) return [];
  const picked: SecCard[] = [];
  const seen = new Set<string>();
  const add = (card?: SecCard) => {
    if (card && !seen.has(card.id) && picked.length < size) {
      seen.add(card.id);
      picked.push(card);
    }
  };
  for (const topicPool of topicPools) {
    if (topicPool.some(card => seen.has(card.id))) continue;
    add(resolveSessionQueue(topicPool, memories, now, examTs, 1)[0]);
  }
  resolveSessionQueue(pool, memories, now, examTs, size).forEach(add);
  return picked;
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

export interface QuizResult extends SessionCardResult {
  questionRef: string;
}

/** The displayed title comes from the same registry used to join the cards. */
export function quizCardTopic(card: SecCard, selection?: StudyTopicSelection): string {
  const spec = specificationFor(selection);
  const matched = selection?.topicIds.find(id => cardsForCurriculumNode(id, [card], spec).length);
  const selectedNodes = spec && matched ? new Set(canonicalNodeIds(spec, matched)) : undefined;
  const topic = libraryTopicIds(card, spec).filter(id => !selectedNodes || selectedNodes.has(id)).map(id => spec && findCanonicalTopic(spec, id)).find(Boolean);
  return topic?.title ?? (matched && spec?.groups.find(group => group.id === matched)?.title) ?? 'Session topic';
}

// ─── Loading ────────────────────────────────────────────────────────────────

export interface LoadedQuiz {
  deck: QuizDeck;
  cards: SecCard[];
  /** How many quiz-worthy cards the scope holds, so four never poses as the lot. */
  poolTotal: number;
  /** The studied topics by name, or null when unavailable. */
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
  const topicIds = input.topicSelection?.topicIds ?? [];
  const spec = specificationFor(input.topicSelection);
  if (!topicIds.length || !spec || spec.subjectId !== resolveSubjectId(input.subjectName)
    || spec.subjectId !== resolveSubjectId(input.topicSelection?.subjectId ?? '')) return null;
  const deck = resolveQuizDeck(input.subjectName, input.topicSelection?.subjectId, input.profileSubjects);
  if (!deck) return null;
  const cards = await loadCards(deck.subjectId, deck.level);
  const topicPools = topicIds.map(id => quizPool(cards, [id], spec));
  const pool = dedupe(topicPools.flat());
  const local = readLocal(input.uid, deck.deckId);
  const examTs = input.examDate ? new Date(input.examDate).getTime() : local.examTs;
  const picked = planQuiz(pool, local.cards, input.now, Number.isFinite(examTs) ? examTs : undefined, QUIZ_SIZE, topicPools);
  if (!picked.length) return null;
  return { deck, cards: picked, poolTotal: pool.length, topicLabel: quizTopicLabel(input.topicSelection) };
}
