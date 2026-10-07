import { describe, expect, it } from 'vitest';
import { CARDS as higher } from '../components/MarkBank/cards/politics-and-society/higher';
import { CARDS as ordinary } from '../components/MarkBank/cards/politics-and-society/ordinary';
import census from '../scripts/markbank/authored/politics-census.json';
import audit from '../scripts/markbank/authored/politics-reconciliation.json';
import { tariffReconciles } from '../types/markBank';
import { resolveCurriculumSpecification } from '../curriculumRegistry';
import { examQuestionPartReferencesForSubject, POLITICS_EXAM_TASKS, politicsExamTopicIdsForTask, curriculumNodeIdsForExamTopic } from '../data/examTopics/registry';
import { SUBJECTS, loadCards } from '../components/MarkBank/deck';

const cards = [...higher, ...ordinary];
const byId = new Map(cards.map(card => [card.id, card]));

describe('Politics complete paper corpus', () => {
  it('ships every independently reviewed task across all 17 indexed papers with no extras', async () => {
    expect(census.papers).toHaveLength(17);
    expect(cards).toHaveLength(1086);
    expect(new Set(cards.map(card => card.id)).size).toBe(cards.length);
    for (const paper of census.papers) {
      const live = cards.filter(card => card.year === paper.year && card.level === paper.level);
      expect(live.length).toBe(paper.expectedCards);
      expect(live.map(card => [card.id, card.questionRef])).toEqual(paper.cards.map(card => [card.cardId, card.questionRef]));
    }
    expect(SUBJECTS.some(subject => subject.id === 'politics-and-society')).toBe(true);
    expect(await loadCards('politics-and-society', 'higher')).toEqual(higher);
  });

  it('keeps every published tariff, source page and exam-year topic valid', () => {
    for (const card of cards) {
      expect(tariffReconciles(card), card.id).toBe(true);
      const spec = resolveCurriculumSpecification(card.subjectId, card.year)!;
      expect(spec.id).toBe(card.specVersion);
      expect(spec.groups.flatMap(group => group.topics).some(topic => topic.id === card.topicId), card.id).toBe(true);
      const source = audit.sources.find(paper => paper.year === card.year && paper.level === card.level)!;
      expect(card.paperFileid).toBe(source.paperFileid);
      expect(card.sourceMaterial!.pages.length).toBeGreaterThan(0);
      expect(card.sourceMaterial!.pages.every(page => page >= 1 && page <= source.papers.pages)).toBe(true);
      if (card.rubric.system !== 'politics') throw new Error(card.id);
      expect(card.rubric.schemePages.every(page => page >= 1 && page <= source.schemes.pages)).toBe(true);
      expect(card.rubric.criteria.reduce((total, criterion) => total + criterion.maxMarks, 0)).toBe(card.totalMarks);
      expect(`${card.stem} ${card.questionText}`).not.toMatch(/[\ue000-\uf8ff]|�|https?:\/\/|www\./);
    }
  });

  it('expands internal combinations and route tariffs without revealing retrieval answers', () => {
    const acronyms = cards.filter(card => card.id.startsWith('politics-2021-ol-q1-l-'));
    expect(acronyms).toHaveLength(126); // C(9, 5)
    expect(acronyms.every(card => card.totalMarks === 10)).toBe(true);
    const causes = cards.filter(card => card.id.startsWith('politics-2023-ol-q2-d-'));
    expect(causes).toHaveLength(286); // C(13, 3)
    expect(causes.every(card => card.totalMarks === 15)).toBe(true);
    expect(causes.every(card => !card.questionText.includes('corruption'))).toBe(true);
    expect(cards.filter(card => card.id.startsWith('politics-2025-ol-q2-d-'))).toHaveLength(3);
    expect(byId.get('politics-2025-hl-q1-o-thinker')?.totalMarks).toBe(2);
    expect(byId.get('politics-2025-hl-q1-o-theory')?.totalMarks).toBe(3);
    expect(byId.get('politics-2024-hl-q2-a')?.totalMarks).toBe(10);
    expect(byId.get('politics-2021-hl-q1-b')?.topicId).toBe('politics-and-society-0-6');
    expect(byId.get('politics-2021-ol-q1-c-capitalism')?.topicId).toBe('politics-and-society-0-6');
    expect(byId.get('politics-2026-hl-q2-g')?.sourceMaterial?.pages).toEqual([8, 9, 12, 13]);
  });

  it('exposes every card in Atlas under its exact curriculum topic and preserves paper jumps', () => {
    expect(POLITICS_EXAM_TASKS.map(task => task.id).sort()).toEqual(cards.map(card => card.id).sort());
    const refs = examQuestionPartReferencesForSubject('politics-and-society');
    for (const task of POLITICS_EXAM_TASKS) {
      const content = politicsExamTopicIdsForTask(task)[0];
      expect(curriculumNodeIdsForExamTopic(content)).toContain(task.topicId);
      expect(refs.some(ref => ref.markBankCardId === task.id && ref.topicId === content &&
        ref.curriculumNodeId === task.topicId && ref.n === task.n && ref.fileid === task.fileid), task.id).toBe(true);
    }
  });
});
