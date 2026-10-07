import type { IrishCriterion, SecRubricCard } from '../../../../types/markBank';
import { resolveCurriculumSpecification } from '../../../../curriculumRegistry';
import authored from './foundation-authored.json';
import authored2024 from './foundation-2024-authored.json';
import authored2023 from './foundation-2023-authored.json';
import authored2022 from './foundation-2022-authored.json';
import authored2021 from './foundation-2021-authored.json';
import authored2020 from './foundation-2020-authored.json';
import authored2019 from './foundation-2019-authored.json';

export const CARDS: SecRubricCard[] = [authored2019, authored2020, authored2021, authored2022, authored2023, authored2024, authored].flatMap(({ cards, review }) => cards.map((card): SecRubricCard => ({
  id: card.id,
  subjectId: 'irish',
  level: 'foundation',
  topicId: card.topicId,
  additionalTopicIds: 'additionalTopicIds' in card ? card.additionalTopicIds : undefined,
  conceptId: card.conceptId,
  source: 'sec',
  kind: 'rubric',
  year: card.year,
  paperFileid: card.paperFileid,
  section: card.section as '1' | '2' | '3',
  questionRef: card.questionRef,
  questionText: card.questionText,
  totalMarks: card.totalMarks,
  sourceMaterial: { ...card.sourceMaterial, kind: 'source-text' },
  audioMaterial: 'audioMaterial' in card && card.audioMaterial
    ? { ...card.audioMaterial, kind: 'source-audio' } : undefined,
  schemeCitation: `SEC Gaeilge Bonnleibhéal ${card.year}, PDF p.${card.schemePage}` +
    (card.schemePages.length > 1 ? `–${card.schemePages.at(-1)}` : '') +
    ' — © State Examinations Commission.',
  schemeRegion: { schemeFileid: `${card.paperFileid}.pdf`, p: card.schemePage, r: [0, 0, 1, 1] },
  specVersion: resolveCurriculumSpecification('irish', card.year)!.id,
  qa: {
    gates: ['visual-paper-sweep', 'visual-scheme-sweep', 'published-mark-boundary', 'finite-route-expansion'],
    humanReviewedBy: 'source-review', humanReviewedAt: review.reviewDate,
  },
  rubric: {
    system: 'irish',
    taskRequirements: [...card.taskRequirements],
    criteria: structuredClone(card.criteria) as IrishCriterion[],
    markingGuideNote: card.markingGuideNote,
  },
})));
