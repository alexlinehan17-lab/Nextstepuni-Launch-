/** A small practice sample, never a whole-subject grade or mastery estimate. */
import { findCanonicalTopic, resolveSubjectId, type CanonicalCurriculumSpecification } from '../../curriculumRegistry';
import { isPointCard, type SecCard } from '../../types/markBank';
import type { SessionCardResult } from './SessionScreen';
import type { Level } from './deck';
import { libraryTopicIds } from './libraryGroups';
import { resolveSessionQueue } from './sessionPlanning';
import type { CardMemory } from './scheduler';
import { isQuizCard, preferShortQuestions, QUIZ_MAX_MARKS, QUIZ_MAX_ROWS } from '../study/quiz/studyQuizPlan';

// A workload limit, not a scientifically optimal number of questions.
export const STARTING_POINT_TOPICS = 3;

export interface StartingPointTopic {
  id: string;
  title: string;
  group: string;
  cards: SecCard[];
}
export interface StartingPointQuestion {
  topicId: string;
  title: string;
  card: SecCard;
}

/** Only one unambiguous current-cohort topic may receive a question's marks.
 * Archived, unmapped and mixed-topic tasks stay available in the normal bank.
 */
export function startingPointTopics(spec: CanonicalCurriculumSpecification | undefined, level: Level, cards: SecCard[]): StartingPointTopic[] {
  if (!spec || spec.status !== 'verified' || !spec.levels.includes(level)) return [];
  const byTopic = new Map<string, SecCard[]>();
  const seen = new Set<string>();
  for (const card of cards) {
    if (seen.has(card.id) || resolveSubjectId(card.subjectId) !== spec.subjectId || card.level !== level
      || !isQuizCard(card) || !card.schemeCitation.trim() || !card.qa.humanReviewedBy.trim() || !card.qa.humanReviewedAt.trim()) continue;
    seen.add(card.id);
    const mapped = libraryTopicIds(card, spec).map(id => findCanonicalTopic(spec, id)?.id);
    if (mapped.some(id => !id)) continue;
    const ids = [...new Set(mapped)];
    if (ids.length !== 1 || !ids[0]) continue;
    byTopic.set(ids[0], [...(byTopic.get(ids[0]) ?? []), card]);
  }
  return spec.groups.flatMap(group => group.topics
    .filter(topic => !topic.levels || topic.levels.includes(level))
    .map(topic => ({ id: topic.id, title: topic.title, group: group.title, cards: preferShortQuestions(byTopic.get(topic.id) ?? []) })));
}

export function planStartingPoint(topics: StartingPointTopic[], selected: readonly string[], memories: Record<string, CardMemory | undefined>, now: number, examTs?: number): StartingPointQuestion[] {
  const picked: StartingPointQuestion[] = [];
  const seen = new Set<string>();
  for (const id of [...new Set(selected)].slice(0, STARTING_POINT_TOPICS)) {
    const topic = topics.find(item => item.id === id);
    if (!topic) continue;
    const card = resolveSessionQueue(topic.cards.filter(item => !seen.has(item.id)), memories, now, examTs, 1)[0];
    if (!card) continue;
    // One extended task is a complete sitting. Other selected topics remain unknown.
    const extended = card.totalMarks > QUIZ_MAX_MARKS || (isPointCard(card) && card.rows.length > QUIZ_MAX_ROWS);
    if (extended && picked.length) continue;
    picked.push({ topicId: id, title: topic.title, card });
    seen.add(card.id);
    if (extended) break;
  }
  return picked;
}

export function startingPointResults(questions: StartingPointQuestion[], results: SessionCardResult[]) {
  return questions.map(question => {
    const result = results.find(item => item.cardId === question.card.id
      && Number.isFinite(item.marksClaimed) && Number.isFinite(item.marksAvailable)
      && item.marksAvailable === question.card.totalMarks && item.marksAvailable > 0
      && item.marksClaimed >= 0 && item.marksClaimed <= item.marksAvailable);
    return { ...question, result, status: !result ? 'unknown' as const
      : result.marksClaimed < result.marksAvailable ? 'practice' as const : 'recheck' as const };
  });
}
