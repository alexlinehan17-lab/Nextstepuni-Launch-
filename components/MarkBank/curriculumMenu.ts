import { examinationYearFromDate, resolveCurriculumSpecification, type CanonicalCurriculumSpecification } from '../../curriculumRegistry';
import { canonicalNodeIds } from '../../services/studyTopicHistory';
import type { SecCard } from '../../types/markBank';
import type { StrandRef, Level } from './deck';
import { libraryGroups, libraryTopicIds } from './libraryGroups';

export function cardsForCurriculumNode(id: string, cards: SecCard[], spec?: CanonicalCurriculumSpecification): SecCard[] {
  const nodes = new Set(spec ? canonicalNodeIds(spec, id) : [id]);
  return cards.filter(card => nodes.has(card.topicId) || libraryTopicIds(card, spec).some(topicId => nodes.has(topicId)));
}

/** Current-cohort menus and explicitly retained original-paper topics coexist. */
export function markBankCurriculumMenu(subjectId: string, level: Level, examDate: string | null | undefined, cards: SecCard[]) {
  const resolved = resolveCurriculumSpecification(subjectId, examinationYearFromDate(examDate));
  const spec = resolved?.status === 'verified' && resolved.levels.includes(level) ? resolved : undefined;
  const strands: StrandRef[] = libraryGroups(subjectId, cards, examDate, level).map((group, index) => ({
    id: group.id, label: group.label ?? `Area ${index + 1}`, title: group.title,
    topics: group.topics.map((topic, topicIndex) => ({ id: topic.id, title: topic.title, code: topic.code ?? `${index + 1}.${topicIndex + 1}` })),
  }));
  return { spec, strands, current: Boolean(spec) };
}
