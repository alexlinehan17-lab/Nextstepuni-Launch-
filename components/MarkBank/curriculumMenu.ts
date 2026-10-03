import { examinationYearFromDate, resolveCurriculumSpecification, type CanonicalCurriculumSpecification } from '../../curriculumRegistry';
import { canonicalNodeIds } from '../../services/studyTopicHistory';
import type { SecCard } from '../../types/markBank';
import { strandsFor, type StrandRef, type Level } from './deck';

export function cardsForCurriculumNode(id: string, cards: SecCard[], spec?: CanonicalCurriculumSpecification): SecCard[] {
  const nodes = new Set(spec ? canonicalNodeIds(spec, id) : [id]);
  return cards.filter(card => nodes.has(card.topicId) || (spec?.legacyTopicAliases?.[card.topicId] && nodes.has(spec.legacyTopicAliases[card.topicId])));
}

/** Current-cohort menus and explicitly retained original-paper topics coexist. */
export function markBankCurriculumMenu(subjectId: string, level: Level, examDate: string | null | undefined, cards: SecCard[]) {
  const spec = resolveCurriculumSpecification(subjectId, examinationYearFromDate(examDate));
  const original = strandsFor(subjectId);
  if (!spec || spec.status !== 'verified' || !spec.levels.includes(level)) {
    return { spec: undefined, strands: original.map(strand => ({ ...strand, label: 'Original paper topics' })), current: false };
  }
  const current: StrandRef[] = spec.groups.map((group, index) => ({
    id: group.id, label: group.label ?? `Area ${index + 1}`, title: group.title,
    topics: group.topics.filter(topic => !topic.levels || topic.levels.includes(level)).map((topic, topicIndex) => ({ id: topic.id, title: topic.title, code: topic.code ?? `${index + 1}.${topicIndex + 1}` })),
  }));
  const currentIds = new Set(current.flatMap(strand => strand.topics.map(topic => topic.id)));
  const remaining = new Set(cards.filter(card => !currentIds.has(card.topicId) && !currentIds.has(spec.legacyTopicAliases?.[card.topicId] ?? '')).map(card => card.topicId));
  const retained = original.map(strand => ({ ...strand, id: `original:${strand.id}`, label: 'Original paper topics', topics: strand.topics.filter(topic => remaining.has(topic.id)) })).filter(strand => strand.topics.length > 0);
  return { spec, strands: [...current, ...retained], current: true };
}
