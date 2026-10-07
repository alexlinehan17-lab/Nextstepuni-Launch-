import { CARDS as ORDINARY } from '../components/MarkBank/cards/maths/ordinary';
import ordinary1 from '../scripts/markbank/mathematics/reviews/2025-ordinary-p1.json';
import ordinary2 from '../scripts/markbank/mathematics/reviews/2025-ordinary-p2.json';
import { describe, expect, it } from 'vitest';
import { logicalQuestionIdentity } from '../components/PaperTrail/topics';
import { CARDS as FOUNDATION } from '../components/MarkBank/cards/maths/foundation';
import foundation from '../scripts/markbank/mathematics/reviews/2025-foundation-single.json';
import foundation2026 from '../scripts/markbank/mathematics/reviews/2026-foundation-single.json';
import foundation2024 from '../scripts/markbank/mathematics/reviews/2024-foundation-single.json';
import foundation2023 from '../scripts/markbank/mathematics/reviews/2023-foundation-single.json';
import foundation2018 from '../scripts/markbank/mathematics/reviews/2018-foundation-p1.json';
import foundation2019 from '../scripts/markbank/mathematics/reviews/2019-foundation-single.json';
import foundation2020 from '../scripts/markbank/mathematics/reviews/2020-foundation-single.json';
import foundation2021 from '../scripts/markbank/mathematics/reviews/2021-foundation-single.json';
import foundation2022 from '../scripts/markbank/mathematics/reviews/2022-foundation-single.json';
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


describe.each([
  { year: 2018, count: 28, offered: 300, review: foundation2018 },
  { year: 2019, count: 34, offered: 300, review: foundation2019 },
  { year: 2020, count: 34, offered: 300, review: foundation2020 },
  { year: 2021, count: 48, offered: 390, review: foundation2021 },
  { year: 2022, count: 53, offered: 390, review: foundation2022 },
  { year: 2023, count: 35, offered: 375, review: foundation2023 },
  { year: 2024, count: 38, offered: 375, review: foundation2024 },
  { year: 2025, count: 42, offered: 375, review: foundation },
  { year: 2026, count: 42, offered: 375, review: foundation2026 },
])('$year Foundation Mathematics independent source review', ({ year, count, offered, review: census }) => {
  const cards = FOUNDATION.filter(card => card.year === year);

  it('retains every published marking unit and all offered marks', () => {
    expect(cards.map(card => card.id).sort()).toEqual(census.cards.map(card => card.id).sort());
    expect(cards).toHaveLength(count);
    expect(new Set(cards.map(card => card.id)).size).toBe(count);
    expect(cards.reduce((total, card) => total + card.totalMarks, 0)).toBe(offered);
    for (const [question, marks] of Object.entries(census.printedQuestionMarks)) {
      expect(cards.filter(card => new RegExp(`Q${question}\\(`).test(card.questionRef))
        .reduce((total, card) => total + card.totalMarks, 0), `Q${question}`).toBe(marks);
    }
  });

  it('carries complete prompts, original pages, exact credit bands and both topic placements', () => {
    const specification = resolveCurriculumSpecification('mathematics', year)!;
    for (const task of census.cards) {
      const card = cards.find(candidate => candidate.id === task.id)!;
      expect(card.level, card.id).toBe('foundation');
      expect(card.stem ?? '', card.id).toBe(task.stem);
      expect(card.questionText, card.id).toBe(task.questionText);
      expect(card.paperFileid, card.id).toBe(census.paperFileid.replace(/\.pdf$/, ''));
      expect(card.schemeCitation, card.id).toContain('Foundation Level');
      expect(card.sourceMaterial?.pages, card.id).toEqual(task.sourcePages);
      expect(card.sourceMaterial?.sourceFileid, card.id).toBe(census.paperFileid);
      expect('mathematicsScale' in card && card.mathematicsScale?.marks, card.id).toEqual(task.permittedMarks);
      expect(card.topicId, card.id).toBe(task.topicId);
      expect(findCanonicalTopic(specification, card.topicId), card.id).toBeDefined();
      const question = task.printedParts[0].match(/^Q(\d+)/)![1];
      expect(examTopicIdsForQuestion('mathematics', 'foundation', year, 'main', question, census.paperKey, 'ev', census.paperFileid), card.id)
        .toEqual(expect.arrayContaining(task.examTopicIds));
    }
  });
});

describe('Foundation Mathematics marking boundaries and source context', () => {
  const task = (year: number, suffix: string) => FOUNDATION.find(card => card.id === `maths-${year}-fl-${suffix}`)!;

  it('keeps the 2018 question and scheme file identities separate and groups all published components', () => {
    const price = task(2018, 'p1-q5-a-b-c');
    expect(price.totalMarks).toBe(20);
    expect(price.questionText).toContain('(c)');
    expect(price.paperFileid).toBe('LC003BLP100EV');
    expect('mathematicsScale' in price && price.mathematicsScale?.schemeFileid).toBe('LC003BLP000EV.pdf');
    expect('mathematicsScale' in price && price.mathematicsScale?.marks).toEqual([0, 5, 11, 16, 20]);
    expect(task(2018, 'p1-q9-a-ii-iii-iv').questionText).toContain('(iv)');
    expect(task(2018, 'p1-q9-b-i-ii-iii').questionText).toContain('(251·32 + 39·14)/10·3');
    expect(task(2018, 'p1-q10-b-ii-iii').sourceMaterial?.pages).toEqual([18, 19]);
    expect(task(2018, 'p1-q8-a').sourceMaterial?.measurementRequired).toBe(true);
  });

  it('retains the 2019 whole probability task, graph instructions and 45/55-mark long questions', () => {
    expect(foundation2019.printedQuestionMarks['9']).toBe(45);
    expect(foundation2019.printedQuestionMarks['10']).toBe(55);
    const probability = task(2019, 'q2-b-i-ii-iii-iv');
    expect(probability.totalMarks).toBe(15);
    expect(probability.questionText).toContain('(iv)');
    expect('mathematicsScale' in probability && probability.mathematicsScale?.marks).toEqual([0, 3, 6, 9, 15]);
    expect(task(2019, 'q5-a-b-c').questionText).toContain('(c)');
    expect(task(2019, 'q5-d').stem).toContain('show relevant work on the graph');
    expect(task(2019, 'q7-b-c').questionText).toContain('10 cm');
    expect(task(2019, 'q9-d').sourceMaterial?.pages).toEqual([14, 15]);
    expect(task(2019, 'q9-d').sourceMaterial?.measurementRequired).toBe(true);
  });

  it('retains the 2020 shared scales, year-specific marks and diagram dependencies', () => {
    for (const suffix of ['q4-a-i-ii', 'q5-b-i-ii-iii', 'q10-a-i-ii-iii']) {
      expect(task(2020, suffix).totalMarks).toBe(15);
      expect(task(2020, suffix).questionText).toContain('(ii)');
    }
    const probability = task(2020, 'q3-b-ii');
    expect(probability.sourceMaterial?.pages).toEqual([8, 9]);
    expect(probability.stem).toContain('A girl is chosen');
    expect(task(2020, 'q4-a-i-ii').sourceMaterial?.measurementRequired).toBe(true);
    expect(task(2020, 'q4-b').sourceMaterial?.measurementRequired).toBe(true);
    expect(task(2020, 'q10-c-i').sourceMaterial?.pages).toEqual([22, 23, 24]);
    const percent = task(2020, 'q7-a-i');
    expect('mathematicsScale' in percent && percent.mathematicsScale?.marks).toEqual([0, 3, 4, 5]);
    const sum = task(2020, 'q1-a-i');
    expect('mathematicsScale' in sum && sum.mathematicsScale?.marks).toEqual([0, 4, 8, 10]);
  });

  it('keeps the 2021 cross-letter journey scale and all shared prompts with their dependencies', () => {
    const journey = task(2021, 'q9-d-e');
    expect(journey.totalMarks).toBe(10);
    expect(journey.questionText).toContain('(d)');
    expect(journey.questionText).toContain('(e)');
    expect(journey.sourceMaterial?.pages).toEqual([20, 21]);
    expect(journey.stem).toContain('four hours');
    expect(task(2021, 'q6-b').questionText).toContain('0·5 cm × 0·5 cm');
    expect(task(2021, 'q2-a').sourceMaterial?.measurementRequired).toBe(true);
    expect(task(2021, 'q10-a-iii').stem).toContain('2 coats');
    expect(task(2021, 'q11-a-ii-iii').questionText).toContain('(iii)');
    expect(task(2021, 'q7-a-ii').stem).toContain('Agricultural Science or Biology');
  });

  it('retains all 2022 long-question marks and the paired scales without hiding component prompts', () => {
    for (const suffix of ['q6-a-ii-iii', 'q9-a-i-ii', 'q11-a-i-ii']) {
      const card = task(2022, suffix);
      expect(card.totalMarks).toBe(10);
      expect(card.questionText).toContain('(ii)');
    }
    expect(task(2022, 'q11-b-ii').sourceMaterial?.pages).toEqual([28, 29]);
    expect(task(2022, 'q11-b-iii').stem).toContain('€160');
    expect(task(2022, 'q10-b-i').sourceMaterial?.measurementRequired).toBe(true);
    expect(task(2022, 'q3-c').stem).toContain('2·5 cm³');
  });

  it('uses the different credit bands in 2025 and 2026', () => {
    const prior = task(2025, 'q7-c-d');
    const current = task(2026, 'q7-c-d');
    expect('mathematicsScale' in prior && prior.mathematicsScale?.marks).toEqual([0, 4, 5, 7, 10]);
    expect('mathematicsScale' in current && current.mathematicsScale?.marks).toEqual([0, 4, 6, 8, 10]);
  });

  it('keeps the 2026 walking graph and its cross-letter allocation together', () => {
    const walking = task(2026, 'q5-a-b');
    expect(walking.totalMarks).toBe(15);
    expect(walking.sourceMaterial?.pages).toEqual([12, 13]);
    expect(walking.questionText).toContain('(b)');
  });

  it('retains the complete 2024 enlargement, trigonometry and intersecting graph asks', () => {
    for (const suffix of ['q8-a', 'q11-d']) {
      const card = task(2024, suffix);
      expect(card.totalMarks).toBe(20);
      expect(card.questionText).toContain('(iii)');
      expect('mathematicsScale' in card && card.mathematicsScale?.marks).toEqual([0, 6, 8, 10, 20]);
    }
    const graphs = task(2024, 'q3-b-i-ii');
    expect(graphs.sourceMaterial?.pages).toEqual([8, 9]);
    expect(graphs.stem).toContain('value of the car');
    expect(graphs.stem).toContain('plot of land');
  });

  it('retains the 2023 travel task across three letters and supplies the construction ruler', () => {
    const travel = task(2023, 'q11-a-b-c');
    expect(travel.totalMarks).toBe(20);
    expect(travel.questionText).toContain('(a)');
    expect(travel.questionText).toContain('(b)');
    expect(travel.questionText).toContain('(c)');
    expect(travel.sourceMaterial?.pages).toEqual([27, 28]);
    expect(task(2023, 'q2-a-i').sourceMaterial?.measurementRequired).toBe(true);
    expect(task(2023, 'q9-d-ii-iii').sourceMaterial?.pages).toEqual([22, 23]);
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
