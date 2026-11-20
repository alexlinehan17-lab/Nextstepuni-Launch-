import { examinationYearFromDate, resolveCurriculumSpecification, type CanonicalCurriculumSpecification } from '../../curriculumRegistry';
import { canonicalNodeIds } from '../../services/studyTopicHistory';
import type { SecCard } from '../../types/markBank';
import type { StrandRef, Level } from './deck';
import { libraryGroups, libraryTopicIds } from './libraryGroups';
import { askRecord, isModelSubject, modelHeadingGroups, modelHeadings } from '../PaperTrail/atlasModel';

/** A Topic Atlas heading of a subject in the single model (atlasModel.ts): the cards filed under it, else null. */
function cardsForModelHeading(id: string, cards: SecCard[]): SecCard[] | null {
  const subjectId = cards[0]?.subjectId;
  if (!subjectId || !modelHeadings(subjectId)?.some(t => t.id === id)) return null;
  return cards.filter(card => askRecord(card.id)?.topics.some(t => t.id === id));
}

/** The headings a card is listed under in this menu: its own topic record in the single model, otherwise its
 *  curriculum topics (libraryTopicIds). Curriculum ids stay behind the scenes for modules and progress. */
export function menuTopicIds(card: SecCard, menu: { model?: boolean; spec?: CanonicalCurriculumSpecification }): string[] {
  if (menu.model) return askRecord(card.id)?.topics.map(t => t.id) ?? [];
  return libraryTopicIds(card, menu.spec);
}

/** The cards under one topic of a Mark Bank menu: in the single model, the cards filed under that heading; otherwise
 *  the cards of that curriculum topic. Only the menu reads headings: a curriculum id elsewhere (a studied topic, a
 *  quiz scope) keeps its curriculum meaning, even where a subject's heading list reuses curriculum ids (Russian). */
export function cardsForMenuTopic(id: string, cards: SecCard[], menu: { model?: boolean; spec?: CanonicalCurriculumSpecification }): SecCard[] {
  if (menu.model) return cardsForModelHeading(id, cards) ?? [];
  return cardsForCurriculumNode(id, cards, menu.spec);
}

/** The cards of one curriculum topic (card.topicId and its library aliases), for modules, quizzes and progress. */
export function cardsForCurriculumNode(id: string, cards: SecCard[], spec?: CanonicalCurriculumSpecification): SecCard[] {
  const nodes = new Set(spec ? canonicalNodeIds(spec, id) : [id]);
  return cards.filter(card => nodes.has(card.topicId) || libraryTopicIds(card, spec).some(topicId => nodes.has(topicId)));
}

/** Current-cohort menus and explicitly retained original-paper topics coexist. */
export function markBankCurriculumMenu(subjectId: string, level: Level, examDate: string | null | undefined, cards: SecCard[]) {
  const resolved = resolveCurriculumSpecification(subjectId, examinationYearFromDate(examDate));
  const spec = resolved?.status === 'verified' && resolved.levels.includes(level) ? resolved : undefined;
  // The single model: the Mark Bank shows the Topic Atlas's headings, so a topic reads the same in both tools.
  if (isModelSubject(subjectId) && modelHeadingGroups(subjectId, level).length) {
    const modelStrands: StrandRef[] = modelHeadingGroups(subjectId, level).map(group => {
      const [label, ...rest] = group.label.split(': ');
      return { id: group.id, label: rest.length ? label : '', title: rest.length ? rest.join(': ') : group.label,
        topics: group.topics.map(topic => ({ id: topic.id, title: topic.title, code: topic.code })) };
    });
    return { spec, strands: modelStrands, current: Boolean(spec), model: true as const };
  }
  const strands: StrandRef[] = libraryGroups(subjectId, cards, examDate, level).map((group, index) => ({
    id: group.id, label: group.label ?? `Area ${index + 1}`, title: group.title,
    topics: group.topics.map((topic, topicIndex) => ({ id: topic.id, title: topic.title, code: topic.code ?? `${index + 1}.${topicIndex + 1}` })),
  }));
  return { spec, strands, current: Boolean(spec), model: false as const };
}
