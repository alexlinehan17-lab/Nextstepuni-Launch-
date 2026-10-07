import { CARDS as ORDINARY } from '../components/MarkBank/cards/maths/ordinary';
import ordinary1 from '../scripts/markbank/mathematics/reviews/2025-ordinary-p1.json';
import ordinary2 from '../scripts/markbank/mathematics/reviews/2025-ordinary-p2.json';
import { describe, expect, it } from 'vitest';
import { logicalQuestionIdentity } from '../components/PaperTrail/topics';
import { CARDS as FOUNDATION } from '../components/MarkBank/cards/maths/foundation';
import foundation from '../scripts/markbank/mathematics/reviews/2025-foundation-single.json';
import foundation2026 from '../scripts/markbank/mathematics/reviews/2026-foundation-single.json';
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


describe('2025 Foundation Mathematics independent source review', () => {
  const cards = FOUNDATION.filter(card => card.year === 2025);

  it('has every one of the 42 separately marked tasks, with no orphan or duplicate', () => {
    expect(cards.map(card => card.id).sort()).toEqual(foundation.cards.map(card => card.id).sort());
    expect(cards).toHaveLength(42);
    expect(new Set(cards.map(card => card.id)).size).toBe(42);
    expect(cards.reduce((total, card) => total + card.totalMarks, 0)).toBe(375);
    for (const [question, marks] of Object.entries(foundation.printedQuestionMarks)) {
      expect(cards.filter(card => new RegExp(`Q${question}\\(`).test(card.questionRef))
        .reduce((total, card) => total + card.totalMarks, 0), `Q${question}`).toBe(marks);
    }
  });

  it('retains the level-specific scale values, original pages and both topic placements', () => {
    const specification = resolveCurriculumSpecification('mathematics', 2025)!;
    for (const task of foundation.cards) {
      const card = cards.find(candidate => candidate.id === task.id)!;
      expect(card.level, card.id).toBe('foundation');
      expect(card.paperFileid, card.id).toBe('LC003BLP000EV');
      expect(card.schemeCitation, card.id).toContain('Foundation Level');
      expect(card.sourceMaterial?.pages, card.id).toEqual(task.sourcePages);
      expect(card.sourceMaterial?.sourceFileid, card.id).toBe(foundation.paperFileid);
      expect('mathematicsScale' in card && card.mathematicsScale?.marks, card.id).toEqual(task.permittedMarks);
      expect(card.topicId, card.id).toBe(task.topicId);
      expect(findCanonicalTopic(specification, card.topicId), card.id).toBeDefined();
      const question = task.printedParts[0].match(/^Q(\d+)/)![1];
      expect(examTopicIdsForQuestion('mathematics', 'foundation', 2025, 'main', question, 'single', 'ev', foundation.paperFileid), card.id)
        .toEqual(expect.arrayContaining(task.examTopicIds));
    }
    const card = cards.find(card => card.id === 'maths-2025-fl-q7-c-d')!;
    expect('mathematicsScale' in card && card.mathematicsScale?.marks).toEqual([0, 4, 5, 7, 10]);
  });
});

describe('2026 Foundation Mathematics independent source review', () => {
  const cards = FOUNDATION.filter(card => card.year === 2026);

  it('retains all 42 published marking units and their 375 offered marks', () => {
    expect(cards.map(card => card.id).sort()).toEqual(foundation2026.cards.map(card => card.id).sort());
    expect(cards).toHaveLength(42);
    expect(cards.reduce((total, card) => total + card.totalMarks, 0)).toBe(375);
    for (const [question, marks] of Object.entries(foundation2026.printedQuestionMarks)) {
      expect(cards.filter(card => new RegExp(`Q${question}\\(`).test(card.questionRef))
        .reduce((total, card) => total + card.totalMarks, 0), `Q${question}`).toBe(marks);
    }
  });

  it('carries complete prompts, source pages, year-specific scales and both topic placements', () => {
    const specification = resolveCurriculumSpecification('mathematics', 2026)!;
    for (const task of foundation2026.cards) {
      const card = cards.find(candidate => candidate.id === task.id)!;
      expect(card.stem ?? '', card.id).toBe(task.stem);
      expect(card.questionText, card.id).toBe(task.questionText);
      expect(card.paperFileid, card.id).toBe('LC003BLP000EV');
      expect(card.sourceMaterial?.pages, card.id).toEqual(task.sourcePages);
      expect(card.sourceMaterial?.sourceFileid, card.id).toBe(foundation2026.paperFileid);
      expect('mathematicsScale' in card && card.mathematicsScale?.marks, card.id).toEqual(task.permittedMarks);
      expect(card.topicId, card.id).toBe(task.topicId);
      expect(findCanonicalTopic(specification, card.topicId), card.id).toBeDefined();
      const question = task.printedParts[0].match(/^Q(\d+)/)![1];
      expect(examTopicIdsForQuestion('mathematics', 'foundation', 2026, 'main', question, 'single', 'ev', foundation2026.paperFileid), card.id)
        .toEqual(expect.arrayContaining(task.examTopicIds));
    }
  });

  it('keeps cross-part allocations together and uses the changed 2026 credit bands', () => {
    const task = (id: string) => cards.find(card => card.id === `maths-2026-fl-${id}`)!;
    expect(task('q5-a-b').totalMarks).toBe(15);
    expect(task('q5-a-b').sourceMaterial?.pages).toEqual([12, 13]);
    expect(task('q5-a-b').questionText).toContain('(b)');
    const award = task('q7-c-d');
    expect('mathematicsScale' in award && award.mathematicsScale?.marks).toEqual([0, 4, 6, 8, 10]);
  });
});


describe.each([{ number: 1, count: 41, review: ordinary1 }, { number: 2, count: 42, review: ordinary2 }])(
  '2025 Ordinary Mathematics Paper $number independent source review', ({ number, count, review: census }) => {
    const cards = ORDINARY.filter(card => card.year === 2025 && card.questionRef.includes(`Paper ${number}`));
    it('retains every independently marked task and all 380 offered marks', () => {
      expect(cards.map(card => card.id).sort()).toEqual(census.cards.map(card => card.id).sort());
      expect(cards).toHaveLength(count);
      expect(cards.reduce((total, card) => total + card.totalMarks, 0)).toBe(380);
      for (const [question, marks] of Object.entries(census.printedQuestionMarks)) {
        expect(cards.filter(card => new RegExp(`Q${question}\\(`).test(card.questionRef))
          .reduce((total, card) => total + card.totalMarks, 0), `Q${question}`).toBe(marks);
      }
    });
    it('carries the entire reviewed prompt, source pages, paper-specific scale and both topic placements', () => {
      const specification = resolveCurriculumSpecification('mathematics', 2025)!;
      for (const task of census.cards) {
        const card = cards.find(candidate => candidate.id === task.id)!;
        expect(card.stem ?? '', card.id).toBe(task.stem);
        expect(card.questionText, card.id).toBe(task.questionText);
        expect(card.sourceMaterial?.pages, card.id).toEqual(task.sourcePages);
        expect(card.sourceMaterial?.sourceFileid, card.id).toBe(census.paperFileid);
        expect('mathematicsScale' in card && card.mathematicsScale?.marks, card.id).toEqual(task.permittedMarks);
        expect(card.topicId, card.id).toBe(task.topicId);
        expect(findCanonicalTopic(specification, card.topicId), card.id).toBeDefined();
        const question = task.printedParts[0].match(/^Q(\d+)/)![1];
        expect(examTopicIdsForQuestion('mathematics', 'ordinary', 2025, 'main', question, `p${number}`, 'ev', census.paperFileid), card.id)
          .toEqual(expect.arrayContaining(task.examTopicIds));
      }
    });
  },
);

it('restores omitted Ordinary subparts and symbols without changing their card identities', () => {
  const card = (id: string) => ORDINARY.find(candidate => candidate.id === `maths-2025-ol-${id}`)!;
  expect(card('p1-q3-c-i').questionText).toContain('(x + k)(x + t) = x² + bx + 12');
  expect(card('p1-q9-b-vi').questionText).toContain('T(n) = 0·5n² + bn');
  expect(card('p2-q4-a-ii').questionText).toContain('ax + by + c = 0');
  expect(card('p2-q5-b-ii').questionText).toContain('triangles ABD and ACD');
  expect(card('p2-q10-b-ii').questionText).toContain('(iii)');
});
