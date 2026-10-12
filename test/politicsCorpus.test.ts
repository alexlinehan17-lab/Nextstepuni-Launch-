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
const criteria = (id: string) => {
  const card = byId.get(id)!;
  if (card.rubric.system !== 'politics') throw new Error(id);
  return card.rubric.criteria.map(criterion => [criterion.label, criterion.maxMarks]);
};

describe('Politics complete paper corpus', () => {
  it('ships every independently reviewed task across all 17 indexed papers with no extras', async () => {
    expect(census.papers).toHaveLength(17);
    expect(cards).toHaveLength(622);
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

  it('keeps each choose-N task as one card with the printed question and N slots', () => {
    // 2021 OL Q1(l): any five of nine printed acronyms, 5 x 2 marks.
    const acronyms = byId.get('politics-2021-ol-q1-l')!;
    expect(cards.filter(card => card.id.startsWith('politics-2021-ol-q1-l'))).toHaveLength(1);
    expect(acronyms.questionRef).toBe('2021 OL Q1(l)');
    expect(acronyms.totalMarks).toBe(10);
    expect(acronyms.questionText.startsWith('Write out in full five of the following acronyms:')).toBe(true);
    if (acronyms.rubric.system !== 'politics') throw new Error(acronyms.id);
    for (const acronym of ['UNCRC', 'EU', 'IHREC', 'IMF', 'UN', 'UDHR', 'WHO', 'ECHR', 'WTO']) {
      // The whole printed list, and the scheme's expansion labelled by each printed acronym.
      expect(acronyms.questionText.split('\n')).toContain(`• ${acronym}`);
      expect(acronyms.rubric.schemeGuidance!.join('\n')).toMatch(new RegExp(`^${acronym}: \\S`, 'm'));
    }
    expect(acronyms.rubric.taskRequirements).toEqual(['Write out in full five of the following acronyms:']);
    expect(acronyms.rubric.criteria.map(criterion => [criterion.label, criterion.maxMarks])).toEqual(
      ['First', 'Second', 'Third', 'Fourth', 'Fifth'].map(label => [`${label} acronym you wrote out`, 2]));
    // 2023 OL Q2(d): the scheme names three causes or any other named in Document B, 3 x 5.
    const causes = byId.get('politics-2023-ol-q2-d')!;
    expect(cards.filter(card => card.id.startsWith('politics-2023-ol-q2-d'))).toHaveLength(1);
    expect(causes.questionText).toBe('According to Document B, name three main causes of poverty in developing countries.');
    expect(causes.totalMarks).toBe(15);
    if (causes.rubric.system !== 'politics') throw new Error(causes.id);
    expect(causes.rubric.criteria.map(criterion => [criterion.label, criterion.maxMarks])).toEqual(
      [['First cause you named', 5], ['Second cause you named', 5], ['Third cause you named', 5]]);
    expect(causes.rubric.schemeGuidance!.join('\n')).toContain('Or any other point named in the piece');
    // 2019 OL Q2(d): any two of the three reasons in Document B, 5 + 5.
    const reasons = byId.get('politics-2019-ol-q2-d')!;
    expect(reasons.questionText).toBe('Document B gives the reasons why the family have had to move twice in three months. Give two of these reasons.');
    expect(criteria('politics-2019-ol-q2-d')).toEqual([['First reason you gave', 5], ['Second reason you gave', 5]]);
    // Choose-one tasks keep the printed wording too: no option is written into the question.
    expect(byId.get('politics-2021-ol-q1-f')!.questionText).toBe(
      'Explain the role and function of one of the following:\n• Civil service\n• Non-governmental organisations\n• Statutory bodies');
    expect(criteria('politics-2021-ol-q1-f')).toEqual([['Role', 5], ['Function', 5]]);
    expect(byId.get('politics-2022-ol-q1-b')!.questionText).toBe(
      'Is it important to vote in an election? Give a reason for your answer.\nYes ☐ No ☐');
    expect(criteria('politics-2025-ol-q2-d')).toEqual([['Country', 2], ['Cause of hunger', 8]]);
    expect(byId.get('politics-2025-hl-q1-o-thinker')?.totalMarks).toBe(2);
    expect(byId.get('politics-2025-hl-q1-o-theory')?.totalMarks).toBe(3);
    expect(byId.get('politics-2024-hl-q2-a')?.totalMarks).toBe(10);
    expect(byId.get('politics-2021-hl-q1-b')?.topicId).toBe('politics-and-society-0-6');
    expect(byId.get('politics-2021-ol-q1-c')?.topicId).toBe('politics-and-society-0-6');
    expect(byId.get('politics-2026-hl-q2-g')?.sourceMaterial?.pages).toEqual([8, 9, 12, 13]);
  });

  it('never publishes a choice as route siblings', () => {
    // Choice is not a route. Sessions do not collapse siblings, so one card per
    // option or per combination put the same printed question in front of a
    // student up to 286 times, each rewritten to name its options.
    const choices = audit.tasks.filter(task => 'choice' in task && task.choice);
    expect(choices).toHaveLength(34);
    expect(audit.tasks.some(task => 'route' in task)).toBe(false);
    const families = new Map<string, string[]>();
    for (const task of choices) {
      const card = byId.get(task.id)!;
      const choice = task.choice!;
      const family = `${card.year}|${card.level}|${choice.key}`;
      families.set(family, [...(families.get(family) ?? []), task.id]);
      expect(choice.choose, task.id).toBeLessThan(choice.poolSize);
      expect(choice.pool, task.id).toHaveLength(choice.poolSize);
      if (card.rubric.system !== 'politics') throw new Error(card.id);
      if (choice.choose > 1) {
        // One slot per chosen item at the scheme's per-slot tariff, and the printed instruction.
        expect(card.rubric.criteria, task.id).toHaveLength(choice.choose);
        expect(new Set(card.rubric.criteria.map(criterion => criterion.maxMarks)).size, task.id).toBe(1);
        expect(card.rubric.taskRequirements, task.id).toContain(choice.instruction);
      }
      // No card names a chosen option in place of the printed question.
      expect(card.questionText, task.id).not.toMatch(/Selected (?:response|answer)|\{selection\}|counting from the top/);
    }
    for (const [family, ids] of families) expect(ids, family).toHaveLength(1);
  });

  it('has no two cards of one printed question marked by identical criteria', () => {
    // The general guard, independent of the reviewed pools: two cards from the
    // same printed question marked by identical criteria are route siblings
    // (Yes/No, either/or, any-N combinations). Legitimate splits are
    // separately priced, so their criteria differ.
    const signatures = new Map<string, string>();
    for (const card of cards) {
      if (card.rubric.system !== 'politics') throw new Error(card.id);
      const question = `${card.year}|${card.level}|${card.questionRef.split(' — ')[0]}`;
      const signature = `${question}|${JSON.stringify(card.rubric.criteria.map(criterion => [criterion.label, criterion.maxMarks]))}`;
      expect(signatures.get(signature), `${card.id} repeats ${signatures.get(signature)}`).toBeUndefined();
      signatures.set(signature, card.id);
    }
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
