import { describe, expect, it } from 'vitest';
import { logicalQuestionIdentity } from '../components/PaperTrail/topics';
import { CARDS as HIGHER } from '../components/MarkBank/cards/maths/higher';
import { resolveCurriculumSpecification, findCanonicalTopic } from '../curriculumRegistry';
import { examTopicIdsForQuestion } from '../data/examTopics/registry';
import review from '../scripts/markbank/mathematics/reviews/2025-higher-p1.json';
import paper2 from '../scripts/markbank/mathematics/reviews/2025-higher-p2.json';

describe('Mathematics booklet identities', () => {
  const question = {
    subjectId: 'mathematics', level: 'higher' as const, year: 2011,
    paperKey: 'p1', n: '1', fileid: 'LC003ALP100EV.pdf',
  };

  it('retains standard and Project Maths questions with the same printed number', () => {
    expect(logicalQuestionIdentity(question)).not.toBe(logicalQuestionIdentity({
      ...question, fileid: 'LC003ALP130EV.pdf',
    }));
  });

  it('still groups translated editions of the same booklet', () => {
    expect(logicalQuestionIdentity(question)).toBe(logicalQuestionIdentity({
      ...question, fileid: 'LC003ALP100IV.pdf',
    }));
  });
});

describe('2025 Higher Mathematics Paper 2 independent source review', () => {
  const cards = HIGHER.filter(card => card.year === 2025 && card.questionRef.includes('Paper 2'));

  it('has no open or orphaned scale units against the visually transcribed census', () => {
    expect(cards.map(card => card.id).sort()).toEqual(paper2.cards.map(card => card.id).sort());
    expect(cards).toHaveLength(43);
    expect(cards.reduce((sum, card) => sum + card.totalMarks, 0)).toBe(380);
    for (const [question, marks] of Object.entries(paper2.printedQuestionMarks)) {
      const group = cards.filter(card => new RegExp(`Q${question}\\(`).test(card.questionRef));
      expect(group.reduce((sum, card) => sum + card.totalMarks, 0), `Q${question}`).toBe(marks);
    }
  });

  it('carries diagrams, grouped parts, exact scales and reviewed topics for every task', () => {
    const specification = resolveCurriculumSpecification('mathematics', 2025)!;
    for (const expected of paper2.cards) {
      const card = cards.find(candidate => candidate.id === expected.id)!;
      expect(card.sourceMaterial?.pages, card.id).toEqual(expected.sourcePages);
      expect(card.sourceMaterial?.sourceFileid, card.id).toBe(paper2.paperFileid);
      expect('mathematicsScale' in card && card.mathematicsScale?.marks, card.id).toEqual(expected.permittedMarks);
      expect(card.topicId, card.id).toBe(expected.topicId);
      expect(findCanonicalTopic(specification, card.topicId), card.id).toBeDefined();
      const question = expected.printedParts[0].match(/^Q(\d+)/)![1];
      expect(examTopicIdsForQuestion('mathematics', 'higher', 2025, 'main', question, 'p2', 'ev', paper2.paperFileid), card.id)
        .toEqual(expect.arrayContaining(expected.examTopicIds));
    }
    const restoredTree = cards.find(card => card.id === 'maths-2025-hl-p2-q9-a-i')!;
    expect(restoredTree.questionRef).toContain('(i), (ii)');
    expect(restoredTree.totalMarks).toBe(15);
    expect(restoredTree.sourceMaterial?.pages).toEqual([24]);
  });
});

describe('2025 Higher Mathematics Paper 1 independent source review', () => {
  const cards = HIGHER.filter(card => card.year === 2025 && card.questionRef.includes('Paper 1'));

  it('retains all 42 published scale units and all 380 available marks', () => {
    expect(cards.map(card => card.id).sort()).toEqual(review.cards.map(card => card.id).sort());
    expect(cards).toHaveLength(42);
    expect(cards.reduce((sum, card) => sum + card.totalMarks, 0)).toBe(380);
    for (const question of Object.keys(review.printedQuestionMarks)) {
      const total = cards.filter(card => new RegExp(`Q${question}\\(`).test(card.questionRef))
        .reduce((sum, card) => sum + card.totalMarks, 0);
      expect(total, `Q${question}`).toBe(Number(question) <= 6 ? 30 : 50);
    }
  });

  it('keeps shared-scale parts together, including the scheme’s misleading Q10 header', () => {
    const byId = new Map(cards.map(card => [card.id, card]));
    expect(byId.get('maths-2025-hl-p1-q2-b-i')?.totalMarks).toBe(15);
    expect(byId.get('maths-2025-hl-p1-q2-b-i')?.questionRef).toContain('(i)–(iii)');
    expect(byId.get('maths-2025-hl-p1-q10-e-i')?.totalMarks).toBe(15);
    expect(byId.get('maths-2025-hl-p1-q10-e-i')?.questionRef).toContain('(i), (ii)');
  });

  it('files every reviewed task in the canonical curriculum and in Topic Atlas', () => {
    const specification = resolveCurriculumSpecification('mathematics', 2025)!;
    expect(specification.id).toBe(review.specificationId);
    for (const expected of review.cards) {
      const card = cards.find(candidate => candidate.id === expected.id)!;
      expect(card.topicId, card.id).toBe(expected.topicId);
      expect(findCanonicalTopic(specification, card.topicId), card.id).toBeDefined();
      const question = expected.printedParts[0].match(/^Q(\d+)/)![1];
      const atlas = examTopicIdsForQuestion('mathematics', 'higher', 2025, 'main', question, 'p1', 'ev', review.paperFileid);
      expect(atlas, card.id).toEqual(expect.arrayContaining(expected.examTopicIds));
    }
  });

  it('attaches the inspected original pages without losing the question or solution image', () => {
    for (const expected of review.cards) {
      const card = cards.find(candidate => candidate.id === expected.id)!;
      expect(card.sourceMaterial?.kind, card.id).toBe('source-question');
      expect(card.sourceMaterial?.pages, card.id).toEqual(expected.sourcePages);
      expect(card.sourceMaterial?.sourceFileid, card.id).toBe(review.paperFileid);
      expect('questionFigure' in card && card.questionFigure, card.id).toBeTruthy();
      expect('figure' in card && card.figure, card.id).toBeTruthy();
    }
  });
});
