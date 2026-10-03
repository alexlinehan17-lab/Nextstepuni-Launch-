import { findCanonicalTopic, resolveCurriculumSpecification, specificationsForSubject, type CanonicalCurriculumGroup } from '../../curriculumRegistry';
import type { SecCard } from '../../types/markBank';

/** A range only joins consecutive years; gaps must remain visible. */
export function libraryYearsLabel(years: number[]): string {
  const sorted = [...new Set(years)].sort((a, b) => a - b);
  const runs: string[] = [];
  for (let index = 0; index < sorted.length; index++) {
    const first = sorted[index];
    let last = first;
    while (sorted[index + 1] === last + 1) last = sorted[++index];
    runs.push(first === last ? String(first) : `${first}–${last}`);
  }
  return runs.join(', ');
}

/** Source-reviewed cards may contain tasks from several canonical topics. */
export function libraryTopicIds(card: SecCard): string[] {
  const specification = resolveCurriculumSpecification(card.subjectId, card.year);
  return [(specification && findCanonicalTopic(specification, card.topicId)?.id) ?? card.topicId];
}

/** Compatibility for callers that need one representative topic. */
export const libraryTopicId = (card: SecCard): string => libraryTopicIds(card)[0];

/** Keep the current curriculum first, and retain every archived question's canonical topic. */
export function libraryGroups(subjectId: string, cards: SecCard[]): CanonicalCurriculumGroup[] {
  const current = resolveCurriculumSpecification(subjectId);
  const groups = (current?.groups ?? []).map(group => ({ ...group, topics: [...group.topics] }));
  const seen = new Set(groups.flatMap(group => group.topics.map(topic => topic.id)));
  const required = new Set(cards.flatMap(libraryTopicIds));
  for (const specification of specificationsForSubject(subjectId)) {
    for (const group of specification.groups) {
      const missing = group.topics.filter(topic => required.has(topic.id) && !seen.has(topic.id));
      if (!missing.length) continue;
      const existing = groups.find(item => item.id === group.id);
      if (existing) existing.topics.push(...missing);
      else groups.push({ ...group, topics: missing });
      missing.forEach(topic => seen.add(topic.id));
    }
  }
  return groups;
}

export const libraryCardsForTopic = (topicId: string, cards: SecCard[]) =>
  cards.filter(card => libraryTopicIds(card).includes(topicId));
