import { CARDS as ORDINARY } from '../components/MarkBank/cards/maths/ordinary';
import ordinary1 from '../scripts/markbank/mathematics/reviews/2025-ordinary-p1.json';
import ordinary2 from '../scripts/markbank/mathematics/reviews/2025-ordinary-p2.json';
import { describe, expect, it } from 'vitest';
import { logicalQuestionIdentity, topicsForPaper } from '../components/PaperTrail/topics';
import { CARDS as FOUNDATION } from '../components/MarkBank/cards/maths/foundation';
import foundation from '../scripts/markbank/mathematics/reviews/2025-foundation-single.json';
import foundation2026 from '../scripts/markbank/mathematics/reviews/2026-foundation-single.json';
import foundation2024 from '../scripts/markbank/mathematics/reviews/2024-foundation-single.json';
import foundation2023 from '../scripts/markbank/mathematics/reviews/2023-foundation-single.json';
import foundation2014p2 from '../scripts/markbank/mathematics/reviews/2014-foundation-p2-project.json';
import foundation2014p2Answers from '../scripts/paper-trail/answers/2014/LC003BLP230EV.pdf.json';
import foundation2014p1 from '../scripts/markbank/mathematics/reviews/2014-foundation-p1-project.json';
import foundation2015 from '../scripts/markbank/mathematics/reviews/2015-foundation-p1.json';
import foundation2016 from '../scripts/markbank/mathematics/reviews/2016-foundation-p1.json';
import foundation2017 from '../scripts/markbank/mathematics/reviews/2017-foundation-p1.json';
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
import higher2026p1 from '../scripts/markbank/mathematics/reviews/2026-higher-p1.json';

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

  it('resolves the exact standard or Project Maths question/scheme pair', async () => {
    const { resolveIndexedPaperFileid } = await import('../scripts/markbank/paperIndex.mjs');
    const standard = { paperFileid: 'LC003BLP100EV.pdf', schemeFileid: 'LC003BLP000EV.pdf' };
    const project = { paperFileid: 'LC003BLP130EV.pdf', schemeFileid: 'LC003BLP030EV.pdf' };
    expect(resolveIndexedPaperFileid('maths', 2013, 'foundation', standard)).toBe('LC003BLP100EV');
    expect(resolveIndexedPaperFileid('maths', 2013, 'foundation', project)).toBe('LC003BLP130EV');
    expect(() => resolveIndexedPaperFileid('maths', 2013, 'foundation', {
      ...project, schemeFileid: standard.schemeFileid,
    })).toThrow('No unique indexed question/scheme pair');
    expect(() => resolveIndexedPaperFileid('maths', 2013, 'foundation', {
      ...standard, paperFileid: standard.schemeFileid,
    })).toThrow('No unique indexed question/scheme pair');
    expect(() => resolveIndexedPaperFileid('maths', 2013, 'higher', project))
      .toThrow('No unique indexed question/scheme pair');
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
  { year: 2014, count: 48, offered: 325, review: foundation2014p2 },
  { year: 2014, count: 36, offered: 300, review: foundation2014p1 },
  { year: 2015, count: 35, offered: 300, review: foundation2015 },
  { year: 2016, count: 39, offered: 300, review: foundation2016 },
  { year: 2017, count: 34, offered: 300, review: foundation2017 },
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
  const cards = FOUNDATION.filter(card => card.year === year && card.sourceMaterial?.sourceFileid === census.paperFileid);

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

  it('retains both 2014 Paper 2 routes and their original candidate tariff', () => {
    const choices = foundation2014p2.finiteChoices[0];
    expect(choices.choose).toBe(1);
    expect(choices.options).toEqual(['8A', '8B']);
    const routes = choices.options.map(option => foundation2014p2.cards.filter(card =>
      card.printedParts[0].startsWith(`Q${option}(`)));
    expect(routes.map(route => route.length)).toEqual([3, 4]);
    expect(new Set(routes.flat().map(card => card.id)).size).toBe(7);
    for (const route of routes) {
      expect(route.reduce((total, card) => total + card.totalMarks, 0)).toBe(choices.routeMarks);
      for (const expected of route) {
        const card = FOUNDATION.find(card => card.id === expected.id)!;
        expect(card.questionText).toBe(expected.questionText);
        expect(card.totalMarks).toBe(expected.totalMarks);
      }
    }
    const mandatory = foundation2014p2.cards.filter(card => !/^Q8[AB]\(/.test(card.printedParts[0]));
    const mandatoryMarks = mandatory.reduce((sum, card) => sum + card.totalMarks, 0);
    expect(mandatoryMarks + choices.choose * choices.routeMarks).toBe(300);
    expect(mandatoryMarks + choices.options.length * choices.routeMarks).toBe(325);
    const atlas = topicsForPaper('mathematics', 2014, 'foundation', 'ev', foundation2014p2.paperFileid)!;
    expect(atlas.q.filter(question => /^8/.test(question.n)).map(question => question.n)).toEqual(['8']);
    const source = foundation2014p2Answers.q.find(question => question.n === '8')!;
    expect(source.pP).toBe(12);
    expect(source.region.map(region => region.p)).toEqual(expect.arrayContaining([41, 42]));
  });

  it('keeps Paper 2 credit bands and all continued data and diagrams', () => {
    const table = task(2014, 'p2-project-q2-b-i');
    expect('mathematicsScale' in table && table.mathematicsScale?.marks).toEqual([0, 2, 3, 4, 5]);
    const events = task(2014, 'p2-project-q2-b-ii-iii-iv');
    expect(events.totalMarks).toBe(5);
    expect(events.questionText).toContain('(iv)');
    expect(events.sourceMaterial?.pages).toEqual([4, 5]);
    const slope = task(2014, 'p2-project-q4-a');
    expect('mathematicsScale' in slope && slope.mathematicsScale?.marks).toEqual([0, 5, 7, 10]);
    expect(task(2014, 'p2-project-q5-c-ii').sourceMaterial?.pages).toEqual([8, 9]);
    expect(task(2014, 'p2-project-q9-b-iv').sourceMaterial?.pages).toEqual([14, 15]);
    const stairs = task(2014, 'p2-project-q10-a-v');
    expect(stairs.sourceMaterial?.pages).toEqual([16, 17]);
    expect(stairs.stem).toContain('1 m wide');
    expect(stairs.stem).toContain('10 steps');
  });

  it('preserves the 2014 graph instructions and the complete average-speed sources', () => {
    const speed = task(2014, 'p1-project-q10-d-i-ii');
    expect(speed.sourceMaterial?.pages).toEqual([14, 15, 16]);
    expect(speed.questionText).toContain('average speed');
    expect('mathematicsScale' in speed && speed.mathematicsScale?.schemePages).toEqual([20, 29]);
    for (const part of ['ii', 'iii', 'iv']) {
      expect(task(2014, `p1-project-q8-b-${part}`).questionText).toContain('Show your work on the diagram');
    }
    expect(task(2014, 'p1-project-q7-b').topicId).toBe('maths-4-3');
    expect(task(2014, 'p1-project-q6-a').topicId).toBe('maths-4-1');
    expect(task(2014, 'p1-project-q6-b').topicId).toBe('maths-4-1');
    expect(task(2014, 'p1-project-q2-a-i-ii').totalMarks).toBe(10);
  });

  it('places numerical substitution and expression tables under Expressions', () => {
    expect(task(2015, 'p1-q7-a-i').topicId).toBe('maths-4-1');
    expect(task(2017, 'p1-q8-a-iii').topicId).toBe('maths-4-1');
  });

  it('pairs 2015 model solutions with separate credit notes and retains all grouped prompts', () => {
    const journey = task(2015, 'p1-q3-b-i-ii-iii');
    expect(journey.totalMarks).toBe(10);
    expect(journey.questionText).toContain('(iii)');
    expect('mathematicsScale' in journey && journey.mathematicsScale?.schemePages).toEqual([9, 25]);
    const garden = task(2015, 'p1-q8-a-i');
    expect(garden.stem).toContain('0·5 m');
    expect('mathematicsScale' in garden && garden.mathematicsScale?.marks).toEqual([0, 7, 15]);
    expect(task(2015, 'p1-q10-b-i').sourceMaterial?.measurementRequired).toBe(true);
    expect(task(2015, 'p1-q10-b-iv').sourceMaterial?.pages).toEqual([16, 17]);
    const comparison = task(2015, 'p1-q9-b');
    expect('mathematicsScale' in comparison && comparison.mathematicsScale?.marks).toEqual([0, 10]);
    expect(task(2015, 'p1-q9-d').questionText).toContain('company name');
  });

  it('keeps the 2016 histogram group, measurement dependencies and unusual net scale', () => {
    const histogram = task(2016, 'p1-q4-b-ii-iii-iv');
    expect(histogram.totalMarks).toBe(10);
    expect(histogram.questionText).toContain('(iv)');
    expect(task(2016, 'p1-q7-b').sourceMaterial?.measurementRequired).toBe(true);
    expect(task(2016, 'p1-q7-c').sourceMaterial?.measurementRequired).toBe(true);
    const net = task(2016, 'p1-q10-a-i');
    expect('mathematicsScale' in net && net.mathematicsScale?.marks).toEqual([0, 2, 3, 4, 5]);
    const price = task(2016, 'p1-q9-b-iv');
    expect(price.sourceMaterial?.pages).toEqual([14, 15]);
    expect(price.stem).toContain('€60 per radiator');
    expect(task(2016, 'p1-q8-a-iii').questionText).toContain('12 − 2 × 3 + 1 = 4');
    expect(task(2016, 'p1-q10-b-i-ii').stem).toContain('radius 1·6 cm');
    expect(foundation2016.schemeVisualTranscriptions.find(page => page.page === 19)?.quotes).toContain('96·5 ÷ 0·5 = 193');
  });

  it('keeps the 2017 grouped scales and complete map and pattern dependencies', () => {
    const probability = task(2017, 'p1-q7-a-b-c');
    expect(probability.totalMarks).toBe(15);
    expect(probability.questionText).toContain('(c)');
    expect('mathematicsScale' in probability && probability.mathematicsScale?.marks).toEqual([0, 4, 7, 11, 15]);
    const yard = task(2017, 'p1-q9-a-i-ii-iii');
    expect(yard.totalMarks).toBe(20);
    expect('mathematicsScale' in yard && yard.mathematicsScale?.marks).toEqual([0, 5, 10, 15, 20]);
    const map = task(2017, 'p1-q8-b');
    expect(map.sourceMaterial?.measurementRequired).toBe(true);
    expect('mathematicsScale' in map && map.mathematicsScale?.schemePages).toEqual([15, 16]);
    expect(task(2017, 'p1-q10-d-e').sourceMaterial?.pages).toEqual([16, 17, 18]);
    expect(task(2017, 'p1-q10-d-e').questionText).toContain('54 chairs');
    expect(task(2017, 'p1-q6-b').totalMarks).toBe(5);
  });

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


describe.each([
  { level: 'higher' as const, number: 1, count: 42, review: higher2026p1 },
])('2026 $level Mathematics Paper $number independent source review', ({ level, number, count, review: census }) => {
  const deck = { higher: HIGHER, ordinary: ORDINARY }[level];
  const cards = deck.filter(card => card.year === 2026 && card.sourceMaterial?.sourceFileid === census.paperFileid);

  it('retains every published marking unit and all 380 offered marks', () => {
    expect(cards.map(card => card.id).sort()).toEqual(census.cards.map(card => card.id).sort());
    expect(cards).toHaveLength(count);
    expect(new Set(cards.map(card => card.id)).size).toBe(count);
    expect(cards.reduce((total, card) => total + card.totalMarks, 0)).toBe(380);
    for (const [question, marks] of Object.entries(census.printedQuestionMarks)) {
      expect(cards.filter(card => new RegExp(`Q${question}\\(`).test(card.questionRef))
        .reduce((total, card) => total + card.totalMarks, 0), `Q${question}`).toBe(marks);
    }
  });

  it('carries complete prompts, original pages, exact scales and both topic placements', () => {
    const specification = resolveCurriculumSpecification('mathematics', 2026)!;
    expect(specification.id).toBe(census.specificationId);
    for (const task of census.cards) {
      const card = cards.find(candidate => candidate.id === task.id)!;
      expect(card.level, card.id).toBe(level);
      expect(card.stem ?? '', card.id).toBe((task as { stem?: string }).stem ?? '');
      expect(card.questionText, card.id).toBe(task.questionText);
      expect(card.questionRef, card.id).toContain(`Paper ${number} ${task.printedParts.join(', ')}`);
      expect(card.paperFileid, card.id).toBe(census.paperFileid.replace(/\.pdf$/, ''));
      expect(card.sourceMaterial?.pages, card.id).toEqual(task.sourcePages);
      expect('mathematicsScale' in card && card.mathematicsScale?.marks, card.id).toEqual(task.permittedMarks);
      expect('mathematicsScale' in card && card.mathematicsScale?.schemePages, card.id).toEqual(task.schemePages);
      expect('mathematicsScale' in card && card.mathematicsScale?.schemeFileid, card.id).toBe(census.schemeFileid);
      expect(card.topicId, card.id).toBe(task.topicId);
      expect(findCanonicalTopic(specification, card.topicId), card.id).toBeDefined();
      const question = task.printedParts[0].match(/^Q(\d+)/)![1];
      expect(examTopicIdsForQuestion('mathematics', level, 2026, 'main', question, census.paperKey, 'ev', census.paperFileid), card.id)
        .toEqual(expect.arrayContaining(task.examTopicIds));
    }
  });
});

it('keeps the 2026 Higher Paper 1 shared scales and continued scheme pages together', () => {
  const card = (suffix: string) => HIGHER.find(candidate => candidate.id === `maths-2026-hl-p1-${suffix}`)!;
  for (const [suffix, marks, last] of [
    ['q5-b-i-ii', 10, '(ii)'], ['q8-e-i-ii', 5, '(ii)'], ['q9-a-b', 10, '(b)'],
    ['q10-a-i-ii', 10, '(ii)'], ['q10-b-i-ii', 5, '(ii)'], ['q10-f-i-ii', 15, '(ii)'],
  ] as const) {
    expect(card(suffix).totalMarks, suffix).toBe(marks);
    expect(card(suffix).questionText, suffix).toContain(last);
  }
  const cubic = card('q1-c');
  expect('mathematicsScale' in cubic && cubic.mathematicsScale?.schemePages).toEqual([8, 9]);
  const induction = card('q6-a');
  expect('mathematicsScale' in induction && induction.mathematicsScale?.marks).toEqual([0, 3, 8, 12, 15]);
  expect(card('q7-f').sourceMaterial?.pages).toEqual([18, 19]);
  expect(card('q8-e-i-ii').questionText).toContain('Tick one box only');
});
