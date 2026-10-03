import { examinationYearFromDate, findCanonicalTopic, resolveCurriculumSpecification, specificationsForSubject, type CanonicalCurriculumGroup, type CanonicalCurriculumSpecification } from '../../curriculumRegistry';
import type { Level } from './deck';
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
export function libraryTopicIds(card: SecCard, current?: CanonicalCurriculumSpecification): string[] {
  const specification = resolveCurriculumSpecification(card.subjectId, card.year);
  const original = (specification && findCanonicalTopic(specification, card.topicId)?.id) ?? card.topicId;
  const cohort = current && (findCanonicalTopic(current, card.topicId) ?? findCanonicalTopic(current, original));
  return [...new Set([original, ...(cohort ? [cohort.id] : [])])];
}

/** Compatibility for callers that need one representative topic. */
export const libraryTopicId = (card: SecCard): string => libraryTopicIds(card)[0];

/** Keep the current curriculum first, and retain every archived question's canonical topic. */
export function libraryGroups(subjectId: string, cards: SecCard[], examDate?: string | null, level?: Level): CanonicalCurriculumGroup[] {
  const resolved = resolveCurriculumSpecification(subjectId, examinationYearFromDate(examDate));
  const current = resolved?.status === 'verified' && (!level || resolved.levels.includes(level)) ? resolved : undefined;
  const groups = (current?.groups ?? []).map(group => ({ ...group, topics: group.topics.filter(topic => !level || !topic.levels || topic.levels.includes(level)) }));
  const seen = new Set(groups.flatMap(group => group.topics.map(topic => topic.id)));
  const required = new Set(cards.flatMap(card => libraryTopicIds(card, current)));
  for (const specification of specificationsForSubject(subjectId)) {
    for (const group of specification.groups) {
      const missing = group.topics.filter(topic => required.has(topic.id) && !seen.has(topic.id));
      if (!missing.length) continue;
      groups.push({ ...group, id: `original:${specification.id}:${group.id}`, label: 'Original paper topics', topics: missing });
      missing.forEach(topic => seen.add(topic.id));
    }
  }
  return groups;
}

export const libraryCardsForTopic = (topicId: string, cards: SecCard[], current?: CanonicalCurriculumSpecification) =>
  cards.filter(card => libraryTopicIds(card, current).includes(topicId));
