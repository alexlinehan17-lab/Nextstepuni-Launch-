import foundation2010project2 from '../scripts/markbank/mathematics/reviews/2010-foundation-p2-project.json';
import foundation2010p2 from '../scripts/markbank/mathematics/reviews/2010-foundation-p2.json';
import foundation2010p1 from '../scripts/markbank/mathematics/reviews/2010-foundation-p1.json';
import ordinary2010project2 from '../scripts/markbank/mathematics/reviews/2010-ordinary-p2-project.json';
import ordinary2010p2 from '../scripts/markbank/mathematics/reviews/2010-ordinary-p2.json';
import ordinary2010p1 from '../scripts/markbank/mathematics/reviews/2010-ordinary-p1.json';
import higher2010project2 from '../scripts/markbank/mathematics/reviews/2010-higher-p2-project.json';
import higher2010p2 from '../scripts/markbank/mathematics/reviews/2010-higher-p2.json';
import higher2010p1 from '../scripts/markbank/mathematics/reviews/2010-higher-p1.json';
import foundation2011project2 from '../scripts/markbank/mathematics/reviews/2011-foundation-p2-project.json';
import foundation2011project1 from '../scripts/markbank/mathematics/reviews/2011-foundation-p1-project.json';
import foundation2011p2 from '../scripts/markbank/mathematics/reviews/2011-foundation-p2.json';
import foundation2011p1 from '../scripts/markbank/mathematics/reviews/2011-foundation-p1.json';
import ordinary2011project2 from '../scripts/markbank/mathematics/reviews/2011-ordinary-p2-project.json';
import ordinary2011project1 from '../scripts/markbank/mathematics/reviews/2011-ordinary-p1-project.json';
import higher2011project2 from '../scripts/markbank/mathematics/reviews/2011-higher-p2-project.json';
import higher2011project1 from '../scripts/markbank/mathematics/reviews/2011-higher-p1-project.json';
import ordinary2011p2 from '../scripts/markbank/mathematics/reviews/2011-ordinary-p2.json';
import ordinary2011p1 from '../scripts/markbank/mathematics/reviews/2011-ordinary-p1.json';
import higher2011p2 from '../scripts/markbank/mathematics/reviews/2011-higher-p2.json';
import higher2011p1 from '../scripts/markbank/mathematics/reviews/2011-higher-p1.json';
import foundation2012project2 from '../scripts/markbank/mathematics/reviews/2012-foundation-p2-project.json';
import foundation2012project1 from '../scripts/markbank/mathematics/reviews/2012-foundation-p1-project.json';
import ordinary2012project2 from '../scripts/markbank/mathematics/reviews/2012-ordinary-p2-project.json';
import ordinary2012project1 from '../scripts/markbank/mathematics/reviews/2012-ordinary-p1-project.json';
import higher2012project2 from '../scripts/markbank/mathematics/reviews/2012-higher-p2-project.json';
import higher2012project1 from '../scripts/markbank/mathematics/reviews/2012-higher-p1-project.json';
import foundation2012p2 from '../scripts/markbank/mathematics/reviews/2012-foundation-p2.json';
import foundation2012p1 from '../scripts/markbank/mathematics/reviews/2012-foundation-p1.json';
import ordinary2012p2 from '../scripts/markbank/mathematics/reviews/2012-ordinary-p2.json';
import ordinary2012p1 from '../scripts/markbank/mathematics/reviews/2012-ordinary-p1.json';
import higher2012p2 from '../scripts/markbank/mathematics/reviews/2012-higher-p2.json';
import higher2012p1 from '../scripts/markbank/mathematics/reviews/2012-higher-p1.json';
import foundation2013phase2p2 from '../scripts/markbank/mathematics/reviews/2013-foundation-p2.json';
import foundation2013phase2p1 from '../scripts/markbank/mathematics/reviews/2013-foundation-p1.json';
import ordinary2013phase2p2 from '../scripts/markbank/mathematics/reviews/2013-ordinary-p2.json';
import ordinary2013phase2p1 from '../scripts/markbank/mathematics/reviews/2013-ordinary-p1.json';
import higher2013phase2p2 from '../scripts/markbank/mathematics/reviews/2013-higher-p2.json';
import higher2013phase2p1 from '../scripts/markbank/mathematics/reviews/2013-higher-p1.json';
import mathsSchemeCatalogue from '../scripts/markbank/authored/maths-scheme-row-figures-catalogue.json';
import foundation2013project2 from '../scripts/markbank/mathematics/reviews/2013-foundation-p2-project.json';
import foundation2013project1 from '../scripts/markbank/mathematics/reviews/2013-foundation-p1-project.json';
import ordinary2013project2 from '../scripts/markbank/mathematics/reviews/2013-ordinary-p2-project.json';
import ordinary2013project1 from '../scripts/markbank/mathematics/reviews/2013-ordinary-p1-project.json';
import higher2013project2 from '../scripts/markbank/mathematics/reviews/2013-higher-p2-project.json';
import higher2013project1 from '../scripts/markbank/mathematics/reviews/2013-higher-p1-project.json';
import ordinary2014p2 from '../scripts/markbank/mathematics/reviews/2014-ordinary-p2.json';
import ordinary2014p1 from '../scripts/markbank/mathematics/reviews/2014-ordinary-p1.json';
import higher2014p2 from '../scripts/markbank/mathematics/reviews/2014-higher-p2.json';
import higher2014p1 from '../scripts/markbank/mathematics/reviews/2014-higher-p1.json';
import ordinary2015p2 from '../scripts/markbank/mathematics/reviews/2015-ordinary-p2.json';
import ordinary2015p1 from '../scripts/markbank/mathematics/reviews/2015-ordinary-p1.json';
import higher2015p2 from '../scripts/markbank/mathematics/reviews/2015-higher-p2.json';
import higher2015p1 from '../scripts/markbank/mathematics/reviews/2015-higher-p1.json';
import questionCropOverrides from '../scripts/markbank/authoring/maths_qfig_overrides.json';
import { CARDS as ORDINARY } from '../components/MarkBank/cards/maths/ordinary';
import ordinary1 from '../scripts/markbank/mathematics/reviews/2025-ordinary-p1.json';
import ordinary2 from '../scripts/markbank/mathematics/reviews/2025-ordinary-p2.json';
import { describe, expect, it } from 'vitest';
import { CARD_ID_ALIASES } from '../components/MarkBank/cardAliases';
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
import higher2024p1 from '../scripts/markbank/mathematics/reviews/2024-higher-p1.json';
import higher2024p2 from '../scripts/markbank/mathematics/reviews/2024-higher-p2.json';
import higher2023p1 from '../scripts/markbank/mathematics/reviews/2023-higher-p1.json';
import higher2023p2 from '../scripts/markbank/mathematics/reviews/2023-higher-p2.json';
import ordinary2024p1 from '../scripts/markbank/mathematics/reviews/2024-ordinary-p1.json';
import ordinary2024p2 from '../scripts/markbank/mathematics/reviews/2024-ordinary-p2.json';
import ordinary2023p1 from '../scripts/markbank/mathematics/reviews/2023-ordinary-p1.json';
import ordinary2023p2 from '../scripts/markbank/mathematics/reviews/2023-ordinary-p2.json';
import higher2022p1 from '../scripts/markbank/mathematics/reviews/2022-higher-p1.json';
import higher2022p2 from '../scripts/markbank/mathematics/reviews/2022-higher-p2.json';
import ordinary2022p1 from '../scripts/markbank/mathematics/reviews/2022-ordinary-p1.json';
import ordinary2022p2 from '../scripts/markbank/mathematics/reviews/2022-ordinary-p2.json';
import higher2021p1 from '../scripts/markbank/mathematics/reviews/2021-higher-p1.json';
import higher2021p2 from '../scripts/markbank/mathematics/reviews/2021-higher-p2.json';
import ordinary2021p1 from '../scripts/markbank/mathematics/reviews/2021-ordinary-p1.json';
import ordinary2021p2 from '../scripts/markbank/mathematics/reviews/2021-ordinary-p2.json';
import higher2020p1 from '../scripts/markbank/mathematics/reviews/2020-higher-p1.json';
import ordinary2016p2 from '../scripts/markbank/mathematics/reviews/2016-ordinary-p2.json';
import ordinary2016p1 from '../scripts/markbank/mathematics/reviews/2016-ordinary-p1.json';
import higher2016p2 from '../scripts/markbank/mathematics/reviews/2016-higher-p2.json';
import higher2016p1 from '../scripts/markbank/mathematics/reviews/2016-higher-p1.json';
import ordinary2017p2 from '../scripts/markbank/mathematics/reviews/2017-ordinary-p2.json';
import ordinary2017p1 from '../scripts/markbank/mathematics/reviews/2017-ordinary-p1.json';
import higher2017p2 from '../scripts/markbank/mathematics/reviews/2017-higher-p2.json';
import higher2017p1 from '../scripts/markbank/mathematics/reviews/2017-higher-p1.json';
import ordinary2018p2 from '../scripts/markbank/mathematics/reviews/2018-ordinary-p2.json';
import ordinary2018p1 from '../scripts/markbank/mathematics/reviews/2018-ordinary-p1.json';
import higher2018p2 from '../scripts/markbank/mathematics/reviews/2018-higher-p2.json';
import higher2018p1 from '../scripts/markbank/mathematics/reviews/2018-higher-p1.json';
import schemeRowFigures from '../scripts/markbank/authored/maths-scheme-row-figures-catalogue.json';
import ordinary2019p2 from '../scripts/markbank/mathematics/reviews/2019-ordinary-p2.json';
import ordinary2019p1 from '../scripts/markbank/mathematics/reviews/2019-ordinary-p1.json';
import higher2019p2 from '../scripts/markbank/mathematics/reviews/2019-higher-p2.json';
import higher2019p1 from '../scripts/markbank/mathematics/reviews/2019-higher-p1.json';
import ordinary2020p2 from '../scripts/markbank/mathematics/reviews/2020-ordinary-p2.json';
import ordinary2020p1 from '../scripts/markbank/mathematics/reviews/2020-ordinary-p1.json';
import higher2020p2 from '../scripts/markbank/mathematics/reviews/2020-higher-p2.json';
import glyphMap from '../scripts/markbank/authoring/glyphmap.json';
import higher2026p1 from '../scripts/markbank/mathematics/reviews/2026-higher-p1.json';
import higher2026p2 from '../scripts/markbank/mathematics/reviews/2026-higher-p2.json';
import ordinary2026p1 from '../scripts/markbank/mathematics/reviews/2026-ordinary-p1.json';
import ordinary2026p2 from '../scripts/markbank/mathematics/reviews/2026-ordinary-p2.json';

describe('2012 Higher Project Maths Phase 3 Paper 1', () => {
  const cards = HIGHER.filter(c => c.id.startsWith('maths-2012-hl-p1-project-'));
  const card = (suffix: string) => {
    const c = cards.find(c => c.id === `maths-2012-hl-p1-project-q${suffix}`);
    if (!c || c.kind !== 'question') throw new Error(`Missing ${suffix}`);
    return c;
  };
  it('retains every reviewed task at its published boundary and reconciles all 300 marks', () => {
    expect(cards).toHaveLength(32);
    expect(cards.map(c => c.id).sort()).toEqual(higher2012project1.cards.map(c => c.id).sort());
    expect(cards.reduce((n,c) => n+c.totalMarks,0)).toBe(300);
    expect(higher2012project1.cards.reduce((n,c) => n+(c.components?.length ?? 1),0)).toBe(33);
    for (const [q,marks] of Object.entries(higher2012project1.printedQuestionMarks)) {
      const tasks = higher2012project1.cards.filter(c => c.printedParts[0].match(/^Q(\d+)/)![1] === q);
      expect(tasks.reduce((n,c) => n+c.totalMarks,0)).toBe(marks);
    }
    expect(card('7-e-f').totalMarks).toBe(5);
    expect(card('7-e-f').questionText).toContain('(f)');
    expect(card('9-c').totalMarks).toBe(5);
    expect(card('9-c').questionText).toContain('(ii)');
  });
  it('keeps all five altitude choices in one task at the original 5B tariff', () => {
    const c = card('9-b-i-altitude-1');
    const t = higher2012project1.cards.find(t => t.id === c.id)!;
    expect(t.selectionChoice?.pool).toEqual(['1','2','3','4','5']);
    expect(t.selectionChoice?.choose).toBe(1);
    expect(c.questionText).toContain('Taking any one value other than 0');
    expect(c.questionText).not.toContain('For this practice');
    expect(c.mathematicsScale?.marks).toEqual([0,3,5]);
    expect(c.totalMarks).toBe(5);
    expect(c.stem).toContain('0·883');
    expect(c.stem).toContain('0·1244');
  });
  it('keeps the two derivative components independent and applies only the twelve published stars', () => {
    expect(card('6-a').mathematicsScale?.components).toEqual([
      {id:'first-derivative',label:'First derivative',code:'10B',marks:[0,7,10],fullCreditMinusOne:false},
      {id:'second-derivative',label:'Second derivative',code:'10B',marks:[0,7,10],fullCreditMinusOne:false},
    ]);
    expect(card('6-a').totalMarks).toBe(20);
    expect(card('6-a').mathematicsScale?.fullCreditMinusOne).toBe(false);
    expect(card('3-a').mathematicsScale?.marks).toEqual([0,14,18,20]);
    expect(card('8-b').mathematicsScale?.marks).toEqual([0,6,12,18,20]);
    expect(cards.filter(c => c.kind === 'question' && c.mathematicsScale?.fullCreditMinusOne).map(c => c.id).sort())
      .toEqual(['7-a','7-b','7-c','7-d','8-b','8-c','8-d','8-f','9-a-i','9-d','9-e','9-f'].map(s => card(s).id).sort());
  });
  it('discloses inconsistent original scale headings without inventing extra score bands', () => {
    expect(card('7-d').totalMarks).toBe(10);
    expect(card('7-d').mathematicsScale?.marks).toEqual([0,7,10]);
    expect(card('7-d').figure?.sourceNote).toContain('printing error');
    expect(card('9-e').figure?.sourceNote).toContain('detailed notes explicitly specify 5C*');
    expect(card('9-f').totalMarks).toBe(5);
    expect(card('9-f').mathematicsScale?.marks).toEqual([0,3,4,5]);
    expect(card('9-f').figure?.sourceNote).toContain('Mid partial credit');
  });
  it('binds every card and Topic Atlas entry to the exact Phase 3 originals and full dependent context', () => {
    const spec = resolveCurriculumSpecification('mathematics',2012)!;
    for (const task of higher2012project1.cards) {
      const c = card(task.id.split('-q')[1]);
      expect(findCanonicalTopic(spec,c.topicId)).toBeDefined();
      expect(c.sourceMaterial?.sourceFileid).toBe('LC003ALP130EV.pdf');
      expect(c.sourceMaterial?.pages).toEqual(task.sourcePages);
      expect(c.mathematicsScale?.schemeFileid).toBe('LC003ALP030EV.pdf');
      expect(c.mathematicsScale?.schemePages).toEqual(task.schemePages);
      expect(c.questionFigure?.src).toContain('maths-2012-HL-ask-p1-project-');
      expect(c.figure?.solution).toBe(true);
      const q = task.printedParts[0].match(/^Q(\d+)/)![1];
      expect(examTopicIdsForQuestion('mathematics','higher',2012,'main',q,'p1','ev',higher2012project1.paperFileid))
        .toEqual(expect.arrayContaining(task.examTopicIds));
    }
    expect(card('3-a').stem).toContain('81/16');
    expect(card('8-f').sourceMaterial?.pages).toEqual([12,13,14,15]);
    expect(card('8-f').stem).toContain('154π/3');
    expect(card('9-a-ii').stem).toContain('to one decimal place');
    expect(card('4-a').topicId).toBe('maths-4-1');
    expect(card('8-f').topicId).toBe('maths-2-3');
  });
});

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
  { level: 'higher' as const, number: 2, count: 41, review: higher2026p2 },
  { level: 'ordinary' as const, number: 1, count: 42, review: ordinary2026p1 },
  { level: 'ordinary' as const, number: 2, count: 45, review: ordinary2026p2 },
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

it('keeps the 2026 Higher Paper 2 all-or-nothing scales, shared units and construction ruler', () => {
  const card = (suffix: string) => HIGHER.find(candidate => candidate.id === `maths-2026-hl-p2-${suffix}`)!;
  for (const suffix of ['q2-c', 'q10-c-ii']) {
    const task = card(suffix);
    expect('mathematicsScale' in task && task.mathematicsScale?.marks, suffix).toEqual([0, 5]);
  }
  for (const [suffix, marks, last] of [
    ['q2-b-i-ii', 15, '(ii)'], ['q5-b-i-ii', 10, '(ii)'], ['q5-b-iii-iv', 15, '(iv)'],
    ['q8-b-i-ii-iii', 5, '(iii)'], ['q10-b-i-ii', 5, '(ii)'],
  ] as const) {
    expect(card(suffix).totalMarks, suffix).toBe(marks);
    expect(card(suffix).questionText, suffix).toContain(last);
  }
  expect(card('q3-a').sourceMaterial?.measurementRequired).toBe(true);
  expect(card('q10-c-i').sourceMaterial?.pages).toEqual([29, 30]);
  expect(card('q10-c-i').stem).toContain('p is the probability');
});

it('keeps the 2026 Ordinary Paper 1 cross-letter inequality scale and Ordinary bands', () => {
  const card = (suffix: string) => ORDINARY.find(candidate => candidate.id === `maths-2026-ol-p1-${suffix}`)!;
  const inequalities = card('q10-b-c');
  expect(inequalities.totalMarks).toBe(10);
  expect(inequalities.questionRef).toContain('Q10(b)(i), Q10(b)(ii), Q10(c)(i), Q10(c)(ii)');
  expect('mathematicsScale' in inequalities && inequalities.mathematicsScale?.marks).toEqual([0, 3, 5, 8, 10]);
  const quadratic = card('q2-b');
  expect('mathematicsScale' in quadratic && quadratic.mathematicsScale?.marks).toEqual([0, 5, 11, 15]);
  const lunch = card('q1-a');
  expect('mathematicsScale' in lunch && lunch.mathematicsScale?.marks).toEqual([0, 4, 7, 10]);
  for (const [suffix, last] of [['q4-c-i-ii-iii', '(iii)'], ['q8-a-i-ii', '(ii)'], ['q10-a-iv-v', '(v)']] as const) {
    expect(card(suffix).questionText, suffix).toContain(last);
  }
  expect(card('q7-a-i-ii').stem).not.toContain('20:30');
});

it('keeps the 2026 Ordinary Paper 2 bands, measurement ruler and all-or-nothing unit', () => {
  const card = (suffix: string) => ORDINARY.find(candidate => candidate.id === `maths-2026-ol-p2-${suffix}`)!;
  const scale = (suffix: string) => { const c = card(suffix); return 'mathematicsScale' in c && c.mathematicsScale?.marks; };
  expect(scale('q3-a-i-ii')).toEqual([0, 4, 8, 12, 15]);
  expect(scale('q5-a-i')).toEqual([0, 5, 10, 15]);
  expect(scale('q6-a-i')).toEqual([0, 5, 10]);
  expect(scale('q6-b-i')).toEqual([0, 5]);
  for (const suffix of ['q6-a-i', 'q6-a-ii-iii']) expect(card(suffix).sourceMaterial?.measurementRequired, suffix).toBe(true);
  expect(card('q9-c-iii').stem).toContain('350 of the 540');
  expect(card('q10-b-iii').sourceMaterial?.pages).toEqual([27, 28]);
});

describe('2024 Higher Mathematics Paper 1 independent source review', () => {
  const cards = HIGHER.filter(card => card.year === 2024 && card.questionRef.includes('Paper 1'));
  const added = new Set(['maths-2024-hl-p1-q8-a-i-ii', 'maths-2024-hl-p1-q9-b-i']);

  it('retains all 41 published scale units and all 380 offered marks', () => {
    expect(cards.map(card => card.id).sort()).toEqual(higher2024p1.cards.map(card => card.id).sort());
    expect(cards).toHaveLength(41);
    expect(cards.reduce((total, card) => total + card.totalMarks, 0)).toBe(380);
    for (const [question, marks] of Object.entries(higher2024p1.printedQuestionMarks)) {
      expect(cards.filter(card => new RegExp(`Q${question}\\(`).test(card.questionRef))
        .reduce((total, card) => total + card.totalMarks, 0), `Q${question}`).toBe(marks);
    }
  });

  it('restores prompts, keeps existing crops, and files every task in both taxonomies', () => {
    const specification = resolveCurriculumSpecification('mathematics', 2024)!;
    for (const task of higher2024p1.cards) {
      const card = cards.find(candidate => candidate.id === task.id)!;
      expect(card.stem ?? '', card.id).toBe((task as { stem?: string }).stem ?? '');
      expect(card.questionText, card.id).toBe(task.questionText);
      expect(card.sourceMaterial?.pages, card.id).toEqual(task.sourcePages);
      expect(card.sourceMaterial?.sourceFileid, card.id).toBe(higher2024p1.paperFileid);
      expect('mathematicsScale' in card && card.mathematicsScale?.marks, card.id).toEqual(task.permittedMarks);
      expect(card.topicId, card.id).toBe(task.topicId);
      expect(findCanonicalTopic(specification, card.topicId), card.id).toBeDefined();
      if (task.id !== 'maths-2024-hl-p1-q8-a-i-ii') {
        expect('questionFigure' in card && card.questionFigure, card.id).toBeTruthy();
      }
      const question = task.printedParts[0].match(/^Q(\d+)/)![1];
      expect(examTopicIdsForQuestion('mathematics', 'higher', 2024, 'main', question, 'p1', 'ev', higher2024p1.paperFileid), card.id)
        .toEqual(expect.arrayContaining(task.examTopicIds));
    }
    expect(cards.filter(card => added.has(card.id))).toHaveLength(2);
    const roots = cards.find(card => card.id === 'maths-2024-hl-p1-q9-b-i')!;
    expect(roots.questionText).toContain('(ii)');
    expect(roots.rows.map(row => row.verbatim)).toContain('Ans: y = 6 [as y ≤ 8]');
    const table = cards.find(card => card.id === 'maths-2024-hl-p1-q8-a-i-ii')!;
    expect('mathematicsScale' in table && table.mathematicsScale?.marks).toEqual([0, 3, 5, 7, 10]);
  });
});

describe('2024 Higher Mathematics Paper 2 independent source review', () => {
  const cards = HIGHER.filter(card => card.year === 2024 && card.questionRef.includes('Paper 2'));

  it('retains all 40 published scale units and all 380 offered marks', () => {
    expect(cards.map(card => card.id).sort()).toEqual(higher2024p2.cards.map(card => card.id).sort());
    expect(cards).toHaveLength(40);
    expect(cards.reduce((total, card) => total + card.totalMarks, 0)).toBe(380);
    for (const [question, marks] of Object.entries(higher2024p2.printedQuestionMarks)) {
      expect(cards.filter(card => new RegExp(`Q${question}\\(`).test(card.questionRef))
        .reduce((total, card) => total + card.totalMarks, 0), `Q${question}`).toBe(marks);
    }
  });

  it('restores prompts and files every task in both taxonomies', () => {
    const specification = resolveCurriculumSpecification('mathematics', 2024)!;
    for (const task of higher2024p2.cards) {
      const card = cards.find(candidate => candidate.id === task.id)!;
      expect(card.stem ?? '', card.id).toBe((task as { stem?: string }).stem ?? '');
      expect(card.questionText, card.id).toBe(task.questionText);
      expect(card.sourceMaterial?.pages, card.id).toEqual(task.sourcePages);
      expect(card.sourceMaterial?.sourceFileid, card.id).toBe(higher2024p2.paperFileid);
      expect('mathematicsScale' in card && card.mathematicsScale?.marks, card.id).toEqual(task.permittedMarks);
      expect(card.topicId, card.id).toBe(task.topicId);
      expect(findCanonicalTopic(specification, card.topicId), card.id).toBeDefined();
      const question = task.printedParts[0].match(/^Q(\d+)/)![1];
      expect(examTopicIdsForQuestion('mathematics', 'higher', 2024, 'main', question, 'p2', 'ev', higher2024p2.paperFileid), card.id)
        .toEqual(expect.arrayContaining(task.examTopicIds));
    }
  });

  it('corrects the Q1(b)–(c) and Q7(a) boundaries and removes page furniture from marking points', () => {
    const card = (suffix: string) => cards.find(candidate => candidate.id === `maths-2024-hl-p2-${suffix}`)!;
    const swim = card('q1-b');
    expect(swim.questionRef).toBe('2024 HL Paper 2 Q1(b), (c)');
    expect(swim.questionText).toContain('(c)');
    expect('questionFigure' in swim && swim.questionFigure).toBeFalsy();
    expect(card('q7-a-i').questionRef).toBe('2024 HL Paper 2 Q7(a)(i)');
    expect(card('q7-a-i').rows.map(row => row.verbatim).join(' ')).not.toContain('A = 62');
    const percentile = card('q7-a-ii');
    expect('mathematicsScale' in percentile && percentile.mathematicsScale?.marks).toEqual([0, 4, 6, 10]);
    for (const suffix of ['q2-d', 'q10-c-i']) {
      expect(card(suffix).rows.map(row => row.verbatim).join(' '), suffix).not.toContain('Mathematics – Higher Level');
    }
    expect(card('q4-a').sourceMaterial?.measurementRequired).toBe(true);
  });
});

describe.each([
  { number: 1, count: 39, review: ordinary2024p1 },
  { number: 2, count: 43, review: ordinary2024p2 },
])('2024 Ordinary Mathematics Paper $number independent source review', ({ number, count, review: census }) => {
  const cards = ORDINARY.filter(card => card.year === 2024 && card.questionRef.includes(`Paper ${number}`));

  it('retains every published unit and all 380 offered marks', () => {
    expect(cards.map(card => card.id).sort()).toEqual(census.cards.map(card => card.id).sort());
    expect(cards).toHaveLength(count);
    expect(cards.reduce((total, card) => total + card.totalMarks, 0)).toBe(380);
    for (const [question, marks] of Object.entries(census.printedQuestionMarks)) {
      expect(cards.filter(card => new RegExp(`Q${question}\\(`).test(card.questionRef))
        .reduce((total, card) => total + card.totalMarks, 0), `Q${question}`).toBe(marks);
    }
  });

  it('restores prompts and files every task in both taxonomies', () => {
    const specification = resolveCurriculumSpecification('mathematics', 2024)!;
    for (const task of census.cards) {
      const card = cards.find(candidate => candidate.id === task.id)!;
      expect(card.stem ?? '', card.id).toBe((task as { stem?: string }).stem ?? '');
      expect(card.questionText, card.id).toBe(task.questionText);
      expect(card.sourceMaterial?.pages, card.id).toEqual(task.sourcePages);
      expect(card.sourceMaterial?.sourceFileid, card.id).toBe(census.paperFileid);
      expect('mathematicsScale' in card && card.mathematicsScale?.marks, card.id).toEqual(task.permittedMarks);
      expect(card.topicId, card.id).toBe(task.topicId);
      expect(findCanonicalTopic(specification, card.topicId), card.id).toBeDefined();
      const question = task.printedParts[0].match(/^Q(\d+)/)![1];
      expect(examTopicIdsForQuestion('mathematics', 'ordinary', 2024, 'main', question, `p${number}`, 'ev', census.paperFileid), card.id)
        .toEqual(expect.arrayContaining(task.examTopicIds));
    }
  });
});

it('ships the three 2024 Ordinary Paper 1 tasks the build used to refuse', () => {
  for (const suffix of ['q2-c', 'q3-a', 'q10-b-iv']) {
    const card = ORDINARY.find(candidate => candidate.id === `maths-2024-ol-p1-${suffix}`);
    expect(card, suffix).toBeDefined();
    expect(card!.rows.length, suffix).toBeGreaterThan(1);
  }
});

it('keeps 2024 Ordinary Paper 2 deductions out of the credit bands and re-cites Q2(c)-(d)', () => {
  const p2 = ORDINARY.filter(card => card.year === 2024 && card.questionRef.includes('Paper 2'));
  for (const card of p2) {
    for (const row of card.rows) {
      const options = row.group?.options ?? [row.verbatim];
      expect(options.join(' '), card.id).not.toMatch(/Full Credit \(-1\)|TTTTTT/);
    }
  }
  const cards = p2.find(card => card.id === 'maths-2024-ol-p2-q2-c')!;
  expect(cards.questionRef).toBe('2024 OL Paper 2 Q2(c), (d)');
  expect(cards.questionText).toContain('(d)');
  const sleep = p2.find(card => card.id === 'maths-2024-ol-p2-q5-a-ii')!;
  expect(sleep.rows.map(row => row.verbatim)).toContain('5% OR 97·5%');
});

describe('2023 Higher Mathematics Paper 1 independent source review', () => {
  const cards = HIGHER.filter(card => card.year === 2023 && card.questionRef.includes('Paper 1'));

  it('retains all 41 published scale units and all 380 offered marks', () => {
    expect(cards.map(card => card.id).sort()).toEqual(higher2023p1.cards.map(card => card.id).sort());
    expect(cards).toHaveLength(41);
    expect(cards.reduce((total, card) => total + card.totalMarks, 0)).toBe(380);
    for (const [question, marks] of Object.entries(higher2023p1.printedQuestionMarks)) {
      expect(cards.filter(card => new RegExp(`Q${question}\\(`).test(card.questionRef))
        .reduce((total, card) => total + card.totalMarks, 0), `Q${question}`).toBe(marks);
    }
  });

  it('restores prompts, ships the held-back tasks and files every task in both taxonomies', () => {
    const specification = resolveCurriculumSpecification('mathematics', 2023)!;
    for (const task of higher2023p1.cards) {
      const card = cards.find(candidate => candidate.id === task.id)!;
      expect(card.stem ?? '', card.id).toBe((task as { stem?: string }).stem ?? '');
      expect(card.questionText, card.id).toBe(task.questionText);
      expect(card.sourceMaterial?.pages, card.id).toEqual(task.sourcePages);
      expect(card.sourceMaterial?.sourceFileid, card.id).toBe(higher2023p1.paperFileid);
      expect('mathematicsScale' in card && card.mathematicsScale?.marks, card.id).toEqual(task.permittedMarks);
      expect(card.topicId, card.id).toBe(task.topicId);
      expect(findCanonicalTopic(specification, card.topicId), card.id).toBeDefined();
      const question = task.printedParts[0].match(/^Q(\d+)/)![1];
      expect(examTopicIdsForQuestion('mathematics', 'higher', 2023, 'main', question, 'p1', 'ev', higher2023p1.paperFileid), card.id)
        .toEqual(expect.arrayContaining(task.examTopicIds));
    }
    const rate = cards.find(card => card.id === 'maths-2023-hl-p1-q10-e-ii')!;
    expect(rate.rows.map(row => row.verbatim).join(' ')).not.toContain('Mathematics – Higher Level');
    const pattern = cards.find(card => card.id === 'maths-2023-hl-p1-q10-c')!;
    expect('mathematicsScale' in pattern && pattern.mathematicsScale?.marks).toEqual([0, 2, 3, 5]);
  });
});

describe('2023 Higher Mathematics Paper 2 independent source review', () => {
  const cards = HIGHER.filter(card => card.year === 2023 && card.questionRef.includes('Paper 2'));

  it('retains all 41 published scale units and all 380 offered marks', () => {
    expect(cards.map(card => card.id).sort()).toEqual(higher2023p2.cards.map(card => card.id).sort());
    expect(cards).toHaveLength(41);
    expect(cards.reduce((total, card) => total + card.totalMarks, 0)).toBe(380);
    for (const [question, marks] of Object.entries(higher2023p2.printedQuestionMarks)) {
      expect(cards.filter(card => new RegExp(`Q${question}\\(`).test(card.questionRef))
        .reduce((total, card) => total + card.totalMarks, 0), `Q${question}`).toBe(marks);
    }
  });

  it('restores prompts, corrects citations and files every task in both taxonomies', () => {
    const specification = resolveCurriculumSpecification('mathematics', 2023)!;
    for (const task of higher2023p2.cards) {
      const card = cards.find(candidate => candidate.id === task.id)!;
      expect(card.stem ?? '', card.id).toBe((task as { stem?: string }).stem ?? '');
      expect(card.questionText, card.id).toBe(task.questionText);
      expect(card.questionRef, card.id).toContain(task.printedParts[0].match(/^Q\d+\([a-z]\)/)![0]);
      expect(card.sourceMaterial?.pages, card.id).toEqual(task.sourcePages);
      expect('mathematicsScale' in card && card.mathematicsScale?.marks, card.id).toEqual(task.permittedMarks);
      expect(card.topicId, card.id).toBe(task.topicId);
      expect(findCanonicalTopic(specification, card.topicId), card.id).toBeDefined();
      const question = task.printedParts[0].match(/^Q(\d+)/)![1];
      expect(examTopicIdsForQuestion('mathematics', 'higher', 2023, 'main', question, 'p2', 'ev', higher2023p2.paperFileid), card.id)
        .toEqual(expect.arrayContaining(task.examTopicIds));
      expect(card.rows.map(row => row.verbatim).join(' '), card.id).not.toContain('Mathematics – Higher Level');
    }
  });
});

describe.each([
  { number: 1, count: 48, review: ordinary2023p1 },
  { number: 2, count: 46, review: ordinary2023p2 },
])('2023 Ordinary Mathematics Paper $number independent source review', ({ number, count, review: census }) => {
  const cards = ORDINARY.filter(card => card.year === 2023 && card.questionRef.includes(`Paper ${number}`));

  it('retains every published unit and all 380 offered marks', () => {
    expect(cards.map(card => card.id).sort()).toEqual(census.cards.map(card => card.id).sort());
    expect(cards).toHaveLength(count);
    expect(cards.reduce((total, card) => total + card.totalMarks, 0)).toBe(380);
    for (const [question, marks] of Object.entries(census.printedQuestionMarks)) {
      expect(cards.filter(card => new RegExp(`Q${question}\\(`).test(card.questionRef))
        .reduce((total, card) => total + card.totalMarks, 0), `Q${question}`).toBe(marks);
    }
  });

  it('restores prompts and files every task in both taxonomies without page furniture', () => {
    const specification = resolveCurriculumSpecification('mathematics', 2023)!;
    for (const task of census.cards) {
      const card = cards.find(candidate => candidate.id === task.id)!;
      expect(card.stem ?? '', card.id).toBe((task as { stem?: string }).stem ?? '');
      expect(card.questionText, card.id).toBe(task.questionText);
      expect(card.sourceMaterial?.pages, card.id).toEqual(task.sourcePages);
      expect('mathematicsScale' in card && card.mathematicsScale?.marks, card.id).toEqual(task.permittedMarks);
      expect(card.topicId, card.id).toBe(task.topicId);
      expect(findCanonicalTopic(specification, card.topicId), card.id).toBeDefined();
      const question = task.printedParts[0].match(/^Q(\d+)/)![1];
      expect(examTopicIdsForQuestion('mathematics', 'ordinary', 2023, 'main', question, `p${number}`, 'ev', census.paperFileid), card.id)
        .toEqual(expect.arrayContaining(task.examTopicIds));
      for (const row of card.rows) {
        expect((row.group?.options ?? [row.verbatim]).join(' '), card.id).not.toMatch(/Ordinary Level|Full Credit \(-1\)/);
      }
    }
  });
});

describe('2023 Ordinary Mathematics Paper 2 marking-point repairs', () => {
  const card = (suffix: string) => ORDINARY.find(candidate => candidate.id === `maths-2023-ol-p2-q${suffix}`)!;

  it('ships the restored cosine-rule card with its quoted scheme lines', () => {
    expect(card('7-c').rows.map(row => row.verbatim)).toContain('Model solution — ∠X = 42·4[°]');
    expect(card('7-c').mathematicsScale?.marks).toEqual([0, 3, 4, 5]);
  });

  it('keeps calculator-mode values, page headers and welded deductions out of every band', () => {
    for (const repaired of ORDINARY.filter(candidate => candidate.id.startsWith('maths-2023-ol-p2-'))) {
      for (const row of repaired.rows) {
        const text = (row.group?.options ?? [row.verbatim]).join(' ');
        expect(text, repaired.id).not.toMatch(/Rad:|Grad:|Mathematics – Ordinary Level/);
        // A credit band never carries a Zero Credit note; labelled quoted points may.
        expect((row.group?.options ?? []).join(' '), repaired.id).not.toMatch(/Zero Credit/);
      }
    }
    expect(card('9-b-iii').rows.map(row => row.verbatim)).toContain('Full Credit −1 (deduction) — Either conclusion or reason missing');
  });

  it('attaches the measuring tool only to the scaled construction', () => {
    const measured = ORDINARY.filter(candidate => candidate.id.startsWith('maths-2023-ol-p2-') && candidate.sourceMaterial?.measurementRequired);
    expect(measured.map(candidate => candidate.id)).toEqual(['maths-2023-ol-p2-q6-a']);
  });
});

// 2022 and 2021 Higher/Ordinary papers, reviewed from 2026-10-12. The 2022 papers were adjusted for
// COVID-19 (220 marks to count) but every question is offered and retained.
describe.each([
  { year: 2022, level: 'higher' as const, number: 1, count: 43, review: higher2022p1 },
  { year: 2022, level: 'higher' as const, number: 2, count: 43, review: higher2022p2 },
  { year: 2022, level: 'ordinary' as const, number: 1, count: 47, review: ordinary2022p1 },
  { year: 2022, level: 'ordinary' as const, number: 2, count: 50, review: ordinary2022p2 },
  { year: 2021, level: 'higher' as const, number: 1, count: 44, review: higher2021p1 },
  { year: 2021, level: 'higher' as const, number: 2, count: 42, review: higher2021p2 },
  { year: 2021, level: 'ordinary' as const, number: 1, count: 42, review: ordinary2021p1 },
  { year: 2021, level: 'ordinary' as const, number: 2, count: 48, review: ordinary2021p2 },
])('$year $level Mathematics Paper $number independent source review', ({ year, level, number, count, review: census }) => {
  const deck = level === 'higher' ? HIGHER : ORDINARY;
  const cards = deck.filter(card => card.year === year && card.questionRef.includes(`Paper ${number}`));

  it('retains every published scale unit and all 380 offered marks', () => {
    expect(cards.map(card => card.id).sort()).toEqual(census.cards.map(card => card.id).sort());
    expect(cards).toHaveLength(count);
    expect(cards.reduce((total, card) => total + card.totalMarks, 0)).toBe(380);
    for (const [question, marks] of Object.entries(census.printedQuestionMarks)) {
      expect(cards.filter(card => new RegExp(`Q${question}\\(`).test(card.questionRef))
        .reduce((total, card) => total + card.totalMarks, 0), `Q${question}`).toBe(marks);
    }
  });

  it('restores prompts and files every task in both taxonomies without page furniture', () => {
    const specification = resolveCurriculumSpecification('mathematics', year)!;
    for (const task of census.cards) {
      const card = cards.find(candidate => candidate.id === task.id)!;
      expect(card.stem ?? '', card.id).toBe((task as { stem?: string }).stem ?? '');
      expect(card.questionText, card.id).toBe(task.questionText);
      expect(card.questionRef, card.id).toContain(task.printedParts[0].match(/^Q\d+\([a-z]\)/)![0]);
      expect(card.sourceMaterial?.pages, card.id).toEqual(task.sourcePages);
      expect(card.sourceMaterial?.sourceFileid, card.id).toBe(census.paperFileid);
      expect('mathematicsScale' in card && card.mathematicsScale?.marks, card.id).toEqual(task.permittedMarks);
      expect(card.topicId, card.id).toBe(task.topicId);
      expect(findCanonicalTopic(specification, card.topicId), card.id).toBeDefined();
      const question = task.printedParts[0].match(/^Q(\d+)/)![1];
      expect(examTopicIdsForQuestion('mathematics', level, year, 'main', question, `p${number}`, 'ev', census.paperFileid), card.id)
        .toEqual(expect.arrayContaining(task.examTopicIds));
      for (const row of card.rows) {
        const text = (row.group?.options ?? [row.verbatim]).join(' ');
        expect(text, card.id).not.toMatch(/Higher Level|Ordinary Level|Marking Scheme|Rad:|Grad:/);
        expect((row.group?.options ?? []).join(' '), card.id).not.toMatch(/Full Credit ?[(]?[-−–]1|Zero Credit/);
      }
    }
  });
});

describe('2022 Higher Mathematics Paper 2 six-category scale and restored tasks', () => {
  const card = (suffix: string) => HIGHER.find(candidate => candidate.id === `maths-2022-hl-p2-q${suffix}`)!;

  it('awards Q10(e) on the published six-category 15E scale', () => {
    const marathon = card('10-e');
    expect('mathematicsScale' in marathon && marathon.mathematicsScale).toMatchObject({ code: '15E', marks: [0, 3, 6, 9, 12, 15] });
  });

  it('ships Q2(a) with each high-partial bullet quoted on its own line', () => {
    const verbatims = card('2-a').rows.map(row => row.verbatim);
    expect(verbatims).toContain('High Partial Credit — Fully correct substitution into formula');
    expect(verbatims).toContain('High Partial Credit — 8 + 4/5 (−1 − 8) and −4 + 4/5 (3 − (−4)), or equivalent');
  });
});

describe('2022 Ordinary Mathematics Paper 2 added construction', () => {
  it('attaches the page measuring tool only to the scaled enlargement', () => {
    const measured = ORDINARY.filter(card => card.id.startsWith('maths-2022-ol-p2-') && card.sourceMaterial?.measurementRequired);
    expect(measured.map(card => card.id)).toEqual(['maths-2022-ol-p2-q9-d']);
    const hitOrMiss = ORDINARY.find(card => card.id === 'maths-2022-ol-p2-q6-a-i')!;
    expect('mathematicsScale' in hitOrMiss && hitOrMiss.mathematicsScale?.marks).toEqual([0, 5]);
  });
});

describe('2021 Ordinary Mathematics Paper 1 glyph repair', () => {
  it('maps Cambria glyph 3053 (U+0BED), the z after y in the italic run, and ships Q2(b)', () => {
    expect((glyphMap as Record<string, string>)['\u0bed']).toBe('\u{1D467}');
    const card = ORDINARY.find(candidate => candidate.id === 'maths-2021-ol-p1-q2-b')!;
    expect(card.questionText).toBe('z₃ = z₁/z₂. Find z₃ in the form a + bi, where a, b ∈ ℤ.');
    expect(JSON.stringify(card)).not.toMatch(/[\u0B00-\u0DFF]/);
  });
});

describe('2021 Ordinary Mathematics Paper 2 repairs', () => {
  const card = (suffix: string) => ORDINARY.find(candidate => candidate.id === `maths-2021-ol-p2-q${suffix}`)!;

  it('ships Q5(b)(ii) with its prompt restored from the paper, and keeps U+F061 out of the glyph map', () => {
    expect(card('5-b-ii').questionText).toContain('Tick (✓)');
    expect((glyphMap as Record<string, string>)['\uf061']).toBeUndefined();
  });

  it('re-cites the Q6 cards to the single parts their scales cover', () => {
    expect(card('6-b-ii').questionRef).toBe('2021 OL Paper 2 Q6(b)(ii)');
    expect(card('6-a-i').questionRef).toBe('2021 OL Paper 2 Q6(a)(i)');
    expect(card('6-b-i').questionRef).toBe('2021 OL Paper 2 Q6(b)(i)');
  });

  it('withdraws the Q3(a) duplicate onto the card that now quotes both method ladders', () => {
    expect(ORDINARY.some(candidate => candidate.id === 'maths-2021-ol-p2-q3')).toBe(false);
    expect(CARD_ID_ALIASES['maths-2021-ol-p2-q3']).toBe('maths-2021-ol-p2-q3-a');
    const verbatims = card('3-a').rows.map(row => row.verbatim);
    expect(verbatims).toContain('Method 1, Low Partial Credit — Slope formula with some substitution');
    expect(verbatims).toContain('Method 2, High Partial Credit — m and c found');
  });
});

// 2020 and 2019 Higher/Ordinary papers: new papers reviewed from 2026-10-12. Every question was
// required (300 marks per paper), so every published scale unit is a task. The 2020 examinations
// were cancelled for Calculated Grades, but the SEC published both papers and their schemes.
describe.each([
  { year: 2020, level: 'higher' as const, number: 1, count: 36, review: higher2020p1 },
  { year: 2020, level: 'higher' as const, number: 2, count: 30, review: higher2020p2 },
  { year: 2020, level: 'ordinary' as const, number: 1, count: 40, review: ordinary2020p1 },
  { year: 2020, level: 'ordinary' as const, number: 2, count: 40, review: ordinary2020p2 },
  { year: 2019, level: 'higher' as const, number: 1, count: 35, review: higher2019p1 },
  { year: 2019, level: 'higher' as const, number: 2, count: 32, review: higher2019p2 },
  { year: 2019, level: 'ordinary' as const, number: 1, count: 36, review: ordinary2019p1 },
  { year: 2019, level: 'ordinary' as const, number: 2, count: 39, review: ordinary2019p2 },
  { year: 2018, level: 'higher' as const, number: 1, count: 33, review: higher2018p1 },
  { year: 2018, level: 'higher' as const, number: 2, count: 32, review: higher2018p2 },
  { year: 2018, level: 'ordinary' as const, number: 1, count: 37, review: ordinary2018p1 },
  { year: 2018, level: 'ordinary' as const, number: 2, count: 39, review: ordinary2018p2 },
  { year: 2017, level: 'higher' as const, number: 1, count: 33, review: higher2017p1 },
  { year: 2017, level: 'higher' as const, number: 2, count: 37, review: higher2017p2 },
  { year: 2017, level: 'ordinary' as const, number: 1, count: 35, review: ordinary2017p1 },
  { year: 2017, level: 'ordinary' as const, number: 2, count: 41, review: ordinary2017p2 },
  { year: 2014, level: 'ordinary' as const, number: 1, count: 39, review: ordinary2014p1 },
  { year: 2014, level: 'higher' as const, number: 1, count: 34, review: higher2014p1 },
  { year: 2015, level: 'ordinary' as const, number: 2, count: 37, review: ordinary2015p2 },
  { year: 2015, level: 'ordinary' as const, number: 1, count: 35, review: ordinary2015p1 },
  { year: 2015, level: 'higher' as const, number: 1, count: 32, review: higher2015p1 },
  { year: 2016, level: 'higher' as const, number: 1, count: 35, review: higher2016p1 },
  { year: 2016, level: 'higher' as const, number: 2, count: 34, review: higher2016p2 },
  { year: 2016, level: 'ordinary' as const, number: 1, count: 39, review: ordinary2016p1 },
  { year: 2016, level: 'ordinary' as const, number: 2, count: 39, review: ordinary2016p2 },
])('$year $level Mathematics Paper $number new-paper source review', ({ year, level, number, count, review: census }) => {
  const deck = level === 'higher' ? HIGHER : ORDINARY;
  const cards = deck.filter(card => card.year === year && card.questionRef.includes(`Paper ${number}`));

  it('ships every published scale unit and all 300 marks', () => {
    expect(cards.map(card => card.id).sort()).toEqual(census.cards.map(card => card.id).sort());
    expect(cards).toHaveLength(count);
    expect(cards.reduce((total, card) => total + card.totalMarks, 0)).toBe(300);
    for (const [question, marks] of Object.entries(census.printedQuestionMarks)) {
      expect(cards.filter(card => new RegExp(`Q${question}(?:\\(|$)`).test(card.questionRef))
        .reduce((total, card) => total + card.totalMarks, 0), `Q${question}`).toBe(marks);
    }
  });

  it('files every task in both taxonomies with repaired, labelled scheme lines', () => {
    const specification = resolveCurriculumSpecification('mathematics', year)!;
    for (const task of census.cards) {
      const card = cards.find(candidate => candidate.id === task.id)!;
      expect(card.stem ?? '', card.id).toBe((task as { stem?: string }).stem ?? '');
      expect(card.questionText, card.id).toBe(task.questionText);
      expect(card.sourceMaterial?.pages, card.id).toEqual(task.sourcePages);
      expect(card.sourceMaterial?.sourceFileid, card.id).toBe(census.paperFileid);
      expect('mathematicsScale' in card && card.mathematicsScale?.marks, card.id).toEqual(task.permittedMarks);
      expect(card.topicId, card.id).toBe(task.topicId);
      expect(findCanonicalTopic(specification, card.topicId), card.id).toBeDefined();
      const question = task.printedParts[0].match(/^Q(\d+)/)![1];
      expect(examTopicIdsForQuestion('mathematics', level, year, 'main', question, `p${number}`, 'ev', census.paperFileid), card.id)
        .toEqual(expect.arrayContaining(task.examTopicIds));
      // The 2019–2020 schemes encode their equation font in Syriac, NKo and Tamil code points.
      expect(JSON.stringify(card), card.id).not.toMatch(/[\u0700-\u08FF\u0A80-\u0DFF]/);
      for (const row of card.rows) {
        expect(row.verbatim, card.id).toMatch(/^[A-Z][A-Za-z0-9 ,()−-]+ — \S/);
        expect(row.verbatim, card.id).not.toMatch(/Higher Level|Ordinary Level|Marking Scheme/);
      }
    }
  });
});

describe('2015 Higher Mathematics Paper 1 printed boundaries', () => {
  const card = (suffix: string) => {
    const found = HIGHER.find(c => c.id === `maths-2015-hl-p1-q${suffix}`);
    if (!found || found.kind !== 'question') throw new Error(`Missing question card ${suffix}`);
    return found;
  };
  it('keeps combined scales together and honours the task-specific 10C exception', () => {
    for (const [suffix, parts] of [
      ['3-a-i', ['Q3(a)(i)', 'Q3(a)(ii)']],
      ['3-b-i', ['Q3(b)(i)', 'Q3(b)(ii)']],
      ['6-a-i', ['Q6(a)(i)', 'Q6(a)(ii)']],
    ] as const) {
      expect(higher2015p1.cards.find(c => c.id === card(suffix).id)?.printedParts).toEqual(parts);
    }
    expect(card('2').totalMarks).toBe(25);
    expect(card('7-b-i').mathematicsScale?.marks).toEqual([0, 3, 7, 10]);
  });
  it('preserves typeset answers for every task and the shared question context', () => {
    for (const task of higher2015p1.cards) {
      const runtime = HIGHER.find(c => c.id === task.id)!;
      if (runtime.kind !== 'question') throw new Error(`Expected question card ${task.id}`);
      expect(runtime.figure?.solution, task.id).toBe(true);
      expect(runtime.figure?.src, task.id).toContain('maths-2015-HL-scheme-');
      expect(runtime.questionFigure?.src, task.id).toContain('maths-2015-HL-ask-p1-');
    }
    for (const suffix of ['q8-c', 'q8-d']) {
      const overrides = questionCropOverrides as Record<string, { regions?: { page: number; top: number; bottom: number }[] }>;
      expect(overrides[`maths-2015-hl-p1-${suffix}`].regions)
        .toContainEqual({ page: 12, top: 591, bottom: 608 });
    }
    expect(card('7-d-ii').stem).toContain('inflection');
  });
});

describe('2019–2020 Mathematics scheme glyph repair', () => {
  it('maps the Cambria Math italic run the 2020 schemes encode in Syriac code points', () => {
    const map = glyphMap as Record<string, string>;
    expect(map['\u0754']).toBe('\u{1D465}');
    expect(map['\u074c']).toBe('\u{1D45D}');
    expect(map['\u07e0']).toBe('\u{1D703}');
  });
});

describe('2017 Higher scheme rows that cannot be lifted as text', () => {
  // Stacked fractions filtered as mark cells, glyphs with no repair, and model solutions
  // printed as images (a long division, graphs): these parts carry the SEC's own print of
  // their scheme row after the reveal.
  const cards = HIGHER.filter(card => card.year === 2017 && card.id.startsWith('maths-2017-hl-'));
  const withRow = cards.filter(card => 'figure' in card && card.figure?.candId.startsWith('maths-2017-HL-scheme-'));
  const crops = schemeRowFigures.filter(entry => entry.file.startsWith('maths-2017-HL-scheme-'));

  it('binds each printed scheme-row crop to exactly one card, held back until the reveal', () => {
    expect(crops.length).toBeGreaterThanOrEqual(11);
    expect(withRow).toHaveLength(crops.length);
    expect(new Set(withRow.map(card => 'figure' in card && card.figure?.candId)))
      .toEqual(new Set(crops.map(entry => entry.file.replace(/\.png$/, ''))));
    for (const card of withRow) {
      expect('figure' in card && card.figure?.solution, card.id).toBe(true);
      expect('figure' in card && card.figure?.src, card.id).toMatch(/^\/exam-figures\/maths\/markbank\/maths-2017-HL-scheme-p\d{3}-i\d\.png$/);
    }
  });

  it('covers the Paper 1 long division, the graphs, and the Q3(b) high partial credit that cannot be quoted', () => {
    const ids = withRow.map(card => card.id);
    expect(ids).toEqual(expect.arrayContaining(['maths-2017-hl-p1-q1-c-ii', 'maths-2017-hl-p1-q3-b', 'maths-2017-hl-p1-q5-a',
      'maths-2017-hl-p1-q6-a', 'maths-2017-hl-p1-q6-b', 'maths-2017-hl-p1-q9-a']));
  });

  it('covers the Paper 2 parts set in stacked fractions, the Q2(b) graph and the Q8(b)(i) tree diagram', () => {
    const ids = withRow.map(card => card.id);
    expect(ids.filter(id => id.startsWith('maths-2017-hl-p2-'))).toHaveLength(30);
    expect(ids).toEqual(expect.arrayContaining(['maths-2017-hl-p2-q1-a', 'maths-2017-hl-p2-q2-b', 'maths-2017-hl-p2-q4-a',
      'maths-2017-hl-p2-q8-b-i', 'maths-2017-hl-p2-q9-f']));
    expect(ids).not.toContain('maths-2017-hl-p2-q5-a');
  });
});

describe('2017 Ordinary scheme rows that cannot be lifted as text', () => {
  // Stacked fractions filtered as mark cells, and model solutions printed as images: these
  // parts carry the SEC's own print of their scheme row after the reveal.
  const cards = ORDINARY.filter(card => card.year === 2017 && card.id.startsWith('maths-2017-ol-'));
  const withRow = cards.filter(card => 'figure' in card && card.figure?.candId.startsWith('maths-2017-OL-scheme-'));
  const crops = schemeRowFigures.filter(entry => entry.file.startsWith('maths-2017-OL-scheme-'));

  it('binds each printed scheme-row crop to exactly one card, held back until the reveal', () => {
    expect(crops.length).toBeGreaterThanOrEqual(17);
    expect(withRow).toHaveLength(crops.length);
    expect(new Set(withRow.map(card => 'figure' in card && card.figure?.candId)))
      .toEqual(new Set(crops.map(entry => entry.file.replace(/\.png$/, ''))));
    for (const card of withRow) {
      expect('figure' in card && card.figure?.solution, card.id).toBe(true);
      expect('figure' in card && card.figure?.src, card.id).toMatch(/^\/exam-figures\/maths\/markbank\/maths-2017-OL-scheme-p\d{3}-i\d\.png$/);
    }
  });

  it('covers the Paper 1 parts set in stacked fractions, the tile pattern and the profit graph', () => {
    const ids = withRow.map(card => card.id);
    expect(ids.filter(id => id.startsWith('maths-2017-ol-p1-'))).toHaveLength(17);
    expect(ids).toEqual(expect.arrayContaining(['maths-2017-ol-p1-q3-a', 'maths-2017-ol-p1-q7-a', 'maths-2017-ol-p1-q8-c-ii',
      'maths-2017-ol-p1-q9-e-iii']));
  });

  it('covers the Paper 2 parts set in stacked fractions and the image-only construction and chart', () => {
    const ids = withRow.map(card => card.id);
    expect(ids.filter(id => id.startsWith('maths-2017-ol-p2-'))).toHaveLength(24);
    expect(ids).toEqual(expect.arrayContaining(['maths-2017-ol-p2-q4-a', 'maths-2017-ol-p2-q5-a-ii', 'maths-2017-ol-p2-q9-b-i',
      'maths-2017-ol-p2-q9-c-ii']));
    expect(ids).not.toContain('maths-2017-ol-p2-q6-b');
  });
});

describe('2018 Ordinary scheme rows that cannot be lifted as text', () => {
  // Model solutions printed as images (an Argand diagram, a tile diagram, a graph) and a
  // roots formula whose denominator the provenance reader filters as a mark cell: these
  // parts carry the SEC's own print of their scheme row after the reveal.
  const cards = ORDINARY.filter(card => card.year === 2018 && card.id.startsWith('maths-2018-ol-'));
  const withRow = cards.filter(card => 'figure' in card && card.figure?.candId.startsWith('maths-2018-OL-scheme-'));
  const crops = schemeRowFigures.filter(entry => entry.file.startsWith('maths-2018-OL-scheme-'));

  it('binds each printed scheme-row crop to exactly one card, held back until the reveal', () => {
    expect(crops.length).toBeGreaterThanOrEqual(4);
    expect(withRow).toHaveLength(crops.length);
    expect(new Set(withRow.map(card => 'figure' in card && card.figure?.candId)))
      .toEqual(new Set(crops.map(entry => entry.file.replace(/\.png$/, ''))));
    for (const card of withRow) {
      expect('figure' in card && card.figure?.solution, card.id).toBe(true);
      expect('figure' in card && card.figure?.src, card.id).toMatch(/^\/exam-figures\/maths\/markbank\/maths-2018-OL-scheme-p\d{3}-i\d\.png$/);
    }
  });

  it('covers the Paper 1 image-only model solutions and the Q3(a) roots formula', () => {
    const ids = withRow.map(card => card.id);
    expect(ids).toEqual(expect.arrayContaining(['maths-2018-ol-p1-q2-a', 'maths-2018-ol-p1-q3-a', 'maths-2018-ol-p1-q4-a',
      'maths-2018-ol-p1-q8-c']));
  });

  it('covers the Paper 2 table, construction, scatterplot and tick box, and the filtered fractions', () => {
    const ids = withRow.map(card => card.id);
    expect(ids).toEqual(expect.arrayContaining(['maths-2018-ol-p2-q1-a-i', 'maths-2018-ol-p2-q6-a-i', 'maths-2018-ol-p2-q7-f-i',
      'maths-2018-ol-p2-q7-f-ii', 'maths-2018-ol-p2-q8-e', 'maths-2018-ol-p2-q8-f', 'maths-2018-ol-p2-q9-a-i', 'maths-2018-ol-p2-q9-a-iii',
      'maths-2018-ol-p2-q9-b-i']));
  });
});

describe('2018 Higher scheme rows that cannot be lifted as text', () => {
  // A stacked-fraction numerator in the 2018 HL scheme extracts as a lone "1", which the
  // provenance reader filters as a mark cell, and some model solutions are printed as a
  // table or graph image. These parts carry the SEC's own print of their scheme row
  // (model solution and every credit band) after the reveal.
  const cards = HIGHER.filter(card => card.year === 2018 && card.id.startsWith('maths-2018-hl-'));
  const withRow = cards.filter(card => 'figure' in card && card.figure?.candId.startsWith('maths-2018-HL-scheme-'));
  const crops = schemeRowFigures.filter(entry => entry.file.startsWith('maths-2018-HL-scheme-'));

  it('binds each printed scheme-row crop to exactly one card, held back until the reveal', () => {
    expect(crops.length).toBeGreaterThanOrEqual(10);
    expect(withRow).toHaveLength(crops.length);
    expect(new Set(withRow.map(card => 'figure' in card && card.figure?.candId)))
      .toEqual(new Set(crops.map(entry => entry.file.replace(/\.png$/, ''))));
    for (const card of withRow) {
      expect('figure' in card && card.figure?.solution, card.id).toBe(true);
      expect('figure' in card && card.figure?.src, card.id).toMatch(/^\/exam-figures\/maths\/markbank\/maths-2018-HL-scheme-p\d{3}-i\d\.png$/);
    }
  });

  it('covers Paper 1 Q8, whose f(x), f′(x) and f′′(x) working cannot be quoted, and the image-only Q9(a) table', () => {
    const ids = withRow.map(card => card.id);
    expect(ids).toEqual(expect.arrayContaining(['maths-2018-hl-p1-q6-b-ii', 'maths-2018-hl-p1-q7-c', 'maths-2018-hl-p1-q7-d',
      'maths-2018-hl-p1-q7-e-ii', 'maths-2018-hl-p1-q8-a', 'maths-2018-hl-p1-q8-b', 'maths-2018-hl-p1-q8-c', 'maths-2018-hl-p1-q8-d',
      'maths-2018-hl-p1-q9-a', 'maths-2018-hl-p1-q9-c-i']));
  });

  it('covers Paper 2 parts whose working refers to a printed diagram, graph or tick table', () => {
    const ids = withRow.map(card => card.id);
    expect(ids).toEqual(expect.arrayContaining(['maths-2018-hl-p2-q4-b', 'maths-2018-hl-p2-q6-a', 'maths-2018-hl-p2-q7-d',
      'maths-2018-hl-p2-q8-b-i', 'maths-2018-hl-p2-q8-c', 'maths-2018-hl-p2-q9-b-iii']));
  });
});

describe('2019 Ordinary scheme rows that cannot be lifted as text', () => {
  // The 2019 OL scheme's text layer flattens sub/superscripts to ASCII and the provenance
  // reader filters a stacked fraction's denominator, so these parts carry the SEC's own
  // print of their scheme row (model solution and every credit band) after the reveal.
  const cards = ORDINARY.filter(card => card.year === 2019 && card.id.startsWith('maths-2019-ol-'));
  const withRow = cards.filter(card => 'figure' in card && card.figure?.candId.startsWith('maths-2019-OL-scheme-'));

  const crops = schemeRowFigures.filter(entry => entry.file.startsWith('maths-2019-OL-scheme-'));

  it('binds each of the 47 printed scheme-row crops to exactly one card, held back until the reveal', () => {
    expect(crops).toHaveLength(47);
    expect(withRow).toHaveLength(47);
    expect(new Set(withRow.map(card => 'figure' in card && card.figure?.candId)))
      .toEqual(new Set(crops.map(entry => entry.file.replace(/\.png$/, ''))));
    for (const card of withRow) {
      expect('figure' in card && card.figure?.solution, card.id).toBe(true);
      expect('figure' in card && card.figure?.src, card.id).toMatch(/^\/exam-figures\/maths\/markbank\/maths-2019-OL-scheme-p\d{3}-i\d\.png$/);
    }
  });

  it('covers the parts whose bands could not be quoted, including Q2(a)(iii) and Q9(d) on Paper 1', () => {
    const ids = withRow.map(card => card.id);
    expect(ids).toEqual(expect.arrayContaining(['maths-2019-ol-p1-q2-a-iii', 'maths-2019-ol-p1-q3-b', 'maths-2019-ol-p1-q7-d-ii',
      'maths-2019-ol-p1-q9-d', 'maths-2019-ol-p2-q8-b-i', 'maths-2019-ol-p2-q9-d-i']));
  });
});


describe('2015 Higher Paper 2 complete task review', () => {
  const cards = HIGHER.filter(card => card.id.startsWith('maths-2015-hl-p2-'));
  it('preserves all 35 tasks, all nine questions and every available mark', () => {
    expect(cards.map(c => c.id).sort()).toEqual(higher2015p2.cards.map(c => c.id).sort());
    expect(cards).toHaveLength(35);
    expect(cards.reduce((sum, c) => sum + c.totalMarks, 0)).toBe(300);
    for (const [q, total] of Object.entries(higher2015p2.printedQuestionMarks)) {
      expect(cards.filter(c => c.questionRef.includes(`Q${q}(`)).reduce((sum,c) => sum+c.totalMarks,0)).toBe(total);
    }
  });
  it('carries every complete prompt, published scale, both topic placements and verified images', () => {
    const spec = resolveCurriculumSpecification('mathematics', 2015)!;
    for (const task of higher2015p2.cards) {
      const card = cards.find(c => c.id === task.id)!;
      if (card.kind !== 'question') throw new Error('Expected question card');
      expect(card.stem ?? '', card.id).toBe(task.stem ?? '');
      expect(card.questionText, card.id).toBe(task.questionText);
      expect(card.sourceMaterial?.pages, card.id).toEqual(task.sourcePages);
      expect(card.mathematicsScale?.schemePages, card.id).toEqual(task.schemePages);
      expect(card.mathematicsScale?.marks, card.id).toEqual(task.permittedMarks);
      expect(card.mathematicsScale?.components, card.id).toEqual(task.components);
      expect(findCanonicalTopic(spec, card.topicId), card.id).toBeDefined();
      expect(card.questionFigure?.src,card.id).toContain('/maths/markbank/');
      expect(card.figure?.solution,card.id).toBe(true);
      const q = task.printedParts[0].match(/^Q(\d+)/)![1];
      expect(examTopicIdsForQuestion('mathematics','higher',2015,'main',q,'p2','ev',higher2015p2.paperFileid),card.id)
        .toEqual(expect.arrayContaining(task.examTopicIds));
    }
  });
  it('retains combined parts and the paper-specific 15C award', () => {
    for (const suffix of ['1-b-i','3-c-i','8-f-i']) expect(higher2015p2.cards.find(c => c.id.endsWith(`q${suffix}`))?.printedParts).toHaveLength(2);
    const task = cards.find(c => c.id.endsWith('q7-a'))!;
    expect('mathematicsScale' in task && task.mathematicsScale?.marks).toEqual([0,5,12,15]);
    expect(cards.find(c => c.id.endsWith('q6-a'))?.sourceMaterial?.measurementRequired).toBe(true);
  });
});


describe('2015 Ordinary Paper 1 printed boundaries and dependencies', () => {
  const card = (suffix: string) => {
    const c = ORDINARY.find(c => c.id === `maths-2015-ol-p1-q${suffix}`);
    if (!c || c.kind !== 'question') throw new Error(`Missing question ${suffix}`);
    return c;
  };
  it('keeps all subparts on each shared scale and the unusually weighted Section B', () => {
    const groups = {'2-b-i':2, '5-b-i':2, '6-a-i':2, '7-d-i':3, '8-c-i':2};
    for (const [suffix, count] of Object.entries(groups)) {
      expect(ordinary2015p1.cards.find(c => c.id === card(suffix).id)?.printedParts).toHaveLength(count);
    }
    expect(ordinary2015p1.printedQuestionMarks).toMatchObject({'7':70, '8':50, '9':30});
    expect(card('5-b-i').mathematicsScale?.marks).toEqual([0,2,5,9,10]);
    expect(card('6-a-i').mathematicsScale?.marks).toEqual([0,3,7,11,15]);
    expect(card('7-c').mathematicsScale?.marks).toEqual([0,2,3,4,5]);
  });
  it('carries required graph, pattern, earlier prompts and original typeset solutions', () => {
    for (const task of ordinary2015p1.cards) {
      const c = card(task.id.split('-q')[1]);
      expect(c.questionFigure?.src, c.id).toContain('maths-2015-OL-ask-p1-');
      expect(c.figure?.src, c.id).toContain('maths-2015-OL-scheme-');
      expect(c.figure?.solution, c.id).toBe(true);
      expect(c.mathematicsScale?.schemePages, c.id).toEqual(task.schemePages);
    }
    expect(card('4-c').stem).toContain('turning point');
    expect(card('6-b-ii').stem).toContain('reflection');
    expect(card('6-b-ii').stem).toContain('Find cos θ');
    expect(card('7-g').stem).toContain('Find the value of c');
    expect(card('8-c-i').stem).toContain('Draw the graph');
    expect(card('8-c-i').sourceMaterial?.pages).toEqual([12]);
    expect(card('8-d-ii').stem).toContain('Use calculus');
    expect(card('9-b').stem).toContain('€25 000');
    expect(card('5-a').figure?.sourceNote).toContain('(x − 1)(x − 3) = 0');
  });
});


describe('2015 Ordinary Paper 2 printed boundaries and visual dependencies', () => {
  const card = (suffix: string) => {
    const c = ORDINARY.find(c => c.id === `maths-2015-ol-p2-q${suffix}`);
    if (!c || c.kind !== 'question') throw new Error(`Missing question ${suffix}`);
    return c;
  };
  it('keeps shared scales intact and uses Paper 2 credit ladders', () => {
    const groups = {'1-b-i':2, '2-a-i':2, '4-b-i':2, '6-a-i':3, '6-b-i':2, '7-a-ii':2, '7-c-i':3};
    for (const [suffix, count] of Object.entries(groups)) {
      expect(ordinary2015p2.cards.find(c => c.id === card(suffix).id)?.printedParts).toHaveLength(count);
    }
    expect(ordinary2015p2.printedQuestionMarks).toMatchObject({'7':35,'8':45,'9':70});
    expect(card('1-a').mathematicsScale?.marks).toEqual([0,4,10]);
    expect(card('1-b-i').mathematicsScale?.marks).toEqual([0,4,9,10]);
    expect(card('3-a').mathematicsScale?.marks).toEqual([0,2,5,8,10]);
    expect(card('4-a').mathematicsScale?.marks).toEqual([0,5,10,15,20]);
    expect(card('9-b-i').mathematicsScale?.marks).toEqual([0,10,17,20]);
  });
  it('includes the original diagrams, full solutions and required preceding information', () => {
    for (const task of ordinary2015p2.cards) {
      const c = card(task.id.split('-q')[1]);
      expect(c.questionFigure?.src, c.id).toContain('maths-2015-OL-ask-p2-');
      expect(c.figure?.src, c.id).toContain('maths-2015-OL-scheme-');
      expect(c.figure?.solution, c.id).toBe(true);
      expect(c.mathematicsScale?.schemePages, c.id).toEqual(task.schemePages);
    }
    for (const suffix of ['7-a-i','7-a-ii','7-b','7-c-i']) {
      expect(card(suffix).sourceMaterial?.measurementRequired).toBe(true);
      expect(card(suffix).sourceMaterial?.pages).toContain(10);
    }
    for (const suffix of ['9-c-i','9-c-ii','9-c-iii','9-c-iv']) {
      expect(card(suffix).stem).toContain('Table 1');
      expect(card(suffix).stem).toContain('Table 2');
      expect(card(suffix).stem).toContain('500 boys and 500 girls');
    }
    expect(card('8-c-ii').stem).toContain('diameter of the tank is 12 m');
    expect(card('4-a').figure?.sourceNote).toContain('110°');
    expect(card('4-b-i').figure?.sourceNote).toContain('quarter');
    expect(card('8-b-iii').figure?.sourceNote).toContain('six whole tins');
  });
});


describe('2014 Higher Paper 1 source boundaries and standalone context', () => {
  const card = (suffix: string) => {
    const c = HIGHER.find(c => c.id === `maths-2014-hl-p1-q${suffix}`);
    if (!c || c.kind !== 'question') throw new Error(`Missing question ${suffix}`);
    return c;
  };
  it('uses the 2014 ladders and keeps the jointly marked graph and explanation together', () => {
    expect(card('1-a').mathematicsScale?.marks).toEqual([0,7,10,15]);
    expect(card('2-a').mathematicsScale?.marks).toEqual([0,2,3,4,5]);
    expect(card('2-b-i').mathematicsScale?.marks).toEqual([0,5,7,10]);
    expect(card('3-a').mathematicsScale?.marks).toEqual([0,3,7,8,10]);
    expect(card('4-a').mathematicsScale?.marks).toEqual([0,5,9,12,15]);
    expect(higher2014p1.cards.find(c => c.id === card('9-e-i').id)?.printedParts)
      .toEqual(['Q9(e)(i)', 'Q9(e)(ii)']);
    expect(card('9-e-i').totalMarks).toBe(5);
  });
  it('retains original typeset questions, complete solutions and shared instructions', () => {
    for (const task of higher2014p1.cards) {
      const c = card(task.id.split('-q')[1]);
      expect(c.questionFigure?.src, c.id).toContain('maths-2014-HL-ask-p1-');
      expect(c.figure?.src, c.id).toContain('maths-2014-HL-scheme-');
      expect(c.figure?.solution, c.id).toBe(true);
      expect(c.sourceMaterial?.sourceFileid).toBe('LC003ALP130EV.pdf');
    }
    for (const suffix of ['6-a-i','6-a-ii','6-b','6-c']) {
      expect(card(suffix).stem).toContain('ln aⁿ');
      expect(card(suffix).rows.map(r => r.verbatim).join(' ')).toContain('Low Partial Credit at most');
    }
    for (const suffix of ['7-a-i','7-a-ii']) {
      expect(card(suffix).rows.map(r => r.verbatim).join(' ')).toContain('wherever it occurs');
    }
    expect(card('2-b-ii').stem).toContain('1 − 2i');
    expect(card('8-c').stem).toContain('−0·013x² + 0·624x');
    expect(card('9-f-ii').stem).toContain('After five minutes');
  });
});


describe('2014 Higher Paper 2 alternatives and source fidelity', () => {
  const cards = HIGHER.filter(c => c.id.startsWith('maths-2014-hl-p2-'));
  const card = (suffix: string) => {
    const c = cards.find(c => c.id === `maths-2014-hl-p2-q${suffix}`);
    if (!c || c.kind !== 'question') throw new Error(`Missing question ${suffix}`);
    return c;
  };
  it('retains both 25-mark alternatives and all 325 offered marks in 41 unique cards', () => {
    expect(cards.map(c => c.id).sort()).toEqual(higher2014p2.cards.map(c => c.id).sort());
    expect(cards).toHaveLength(41);
    expect(new Set(cards.map(c => c.id)).size).toBe(41);
    expect(cards.reduce((n,c) => n+c.totalMarks,0)).toBe(325);
    for (const [q,total] of Object.entries(higher2014p2.printedQuestionMarks)) {
      expect(cards.filter(c => c.questionRef.includes(`Q${q}(`)).reduce((n,c) => n+c.totalMarks,0),q).toBe(total);
    }
    expect(cards.filter(c => c.questionRef.includes('Q6A(')).map(c => c.totalMarks)).toEqual([20,5]);
    expect(cards.filter(c => c.questionRef.includes('Q6B(')).map(c => c.totalMarks)).toEqual([10,10,5]);
    expect(card('6a-a').mathematicsScale?.components?.map(c => c.marks)).toEqual([[0,2,5],[0,2,5],[0,3,7,10]]);
  });
  it('preserves complete prompts, source pages, original figures and distinct Atlas alternatives', () => {
    const spec = resolveCurriculumSpecification('mathematics',2014)!;
    for (const task of higher2014p2.cards) {
      const c = card(task.id.split('-q')[1]);
      expect(c.stem ?? '').toBe(task.stem ?? '');
      expect(c.questionText).toBe(task.questionText);
      expect(c.sourceMaterial?.pages).toEqual(task.sourcePages);
      expect(c.mathematicsScale?.schemePages).toEqual(task.schemePages);
      expect(c.mathematicsScale?.marks).toEqual(task.permittedMarks);
      expect(c.mathematicsScale?.components).toEqual(task.components);
      expect(findCanonicalTopic(spec,c.topicId)).toBeDefined();
      expect(c.questionFigure?.src).toContain('maths-2014-HL-ask-p2-');
      expect(c.figure?.solution).toBe(true);
      const q = task.printedParts[0].match(/^Q(\d+[A-Z]?)/)![1];
      expect(examTopicIdsForQuestion('mathematics','higher',2014,'main',q,'p2','ev',higher2014p2.paperFileid))
        .toEqual(expect.arrayContaining(task.examTopicIds));
    }
  });
  it('keeps the three shared voltage scales and discloses conflicting Q9 allocations', () => {
    for (const part of ['a','b','c']) expect(higher2014p2.cards.find(c => c.id.endsWith(`q4-${part}-i`))?.printedParts).toHaveLength(2);
    expect(card('9-a-i').mathematicsScale?.marks).toEqual([0,5,10,15]);
    expect(card('9-a-iv').mathematicsScale?.marks).toEqual([0,2,3,5]);
    for (const suffix of ['9-a-i','9-a-iv']) expect(card(suffix).figure?.sourceNote).toContain('detailed marking notes');
    expect(card('7-d-i').figure?.sourceNote).toContain('male employment fell');
  });
  it('retains dependencies without supplying earlier answers in the question', () => {
    expect(card('4-c-i').stem).toContain('standard deviation');
    expect(card('7-c-iii').stem).toContain('979 590');
    expect(card('7-d-ii').stem).toContain('females were affected');
    expect(card('8-b-ii').stem).toContain('5% level');
    expect(card('9-a-iv').stem).toContain('C(−2, 2)');
    expect(card('9-a-iv').stem).toContain('x² + y² + 4x + 6y − 19 = 0');
    expect(card('9-b-iii').stem).toContain('area of the circle u');
  });
});


describe('2014 Ordinary Paper 1 detailed scales and context', () => {
  const card = (suffix: string) => {
    const c = ORDINARY.find(c => c.id === `maths-2014-ol-p1-q${suffix}`);
    if (!c || c.kind !== 'question') throw new Error(`Missing task ${suffix}`);
    return c;
  };
  it('uses the shared marking boundaries and the Ordinary 10D ladder', () => {
    for (const suffix of ['4-c-i', '5-a-i', '9-d-i']) {
      expect(ordinary2014p1.cards.find(c => c.id === card(suffix).id)?.printedParts).toHaveLength(2);
    }
    for (const suffix of ['1-c','3-b','5-b','8-d','9-d-i']) {
      expect(card(suffix).mathematicsScale?.marks).toEqual([0,3,5,8,10]);
    }
    expect(card('4-c-i').totalMarks).toBe(5);
    expect(card('4-c-i').figure?.sourceNote).toContain('detailed notes');
  });
  it('retains the original question and solution images and their source pages', () => {
    for (const task of ordinary2014p1.cards) {
      const c = card(task.id.split('-q')[1]);
      expect(c.questionFigure?.src).toContain('maths-2014-OL-ask-p1-');
      expect(c.questionFigure?.alt).toContain(task.questionText);
      expect(c.figure?.solution).toBe(true);
      expect(c.mathematicsScale?.schemePages).toEqual(task.schemePages);
    }
    expect(card('3-a-ii').stem).toContain('2(4 − 3x)');
    expect(card('5-c').stem).toContain('local maximum');
    expect(card('7-b-iii').stem).toContain('Bargain Deals');
    expect(card('8-e').stem).toContain('4h³ − 48h² + 144h');
    expect(card('9-c-ii').stem).toContain('2·5 seconds');
    expect(card('9-f').stem).toContain('h = 10t − t²');
  });
});


describe('2014 Ordinary Paper 2 alternatives, component scales and diagrams', () => {
  const cards = ORDINARY.filter(c => c.id.startsWith('maths-2014-ol-p2-'));
  const card = (suffix: string) => {
    const c = cards.find(c => c.id === `maths-2014-ol-p2-q${suffix}`);
    if (!c || c.kind !== 'question') throw new Error(`Missing task ${suffix}`);
    return c;
  };
  it('retains all 41 tasks and both Q6 choices, totalling 325 offered marks', () => {
    expect(cards.map(c => c.id).sort()).toEqual(ordinary2014p2.cards.map(c => c.id).sort());
    expect(cards).toHaveLength(41);
    expect(new Set(cards.map(c => c.id)).size).toBe(41);
    expect(cards.reduce((n,c) => n+c.totalMarks,0)).toBe(325);
    for (const [q,marks] of Object.entries(ordinary2014p2.printedQuestionMarks)) {
      expect(cards.filter(c => new RegExp(`Q${q}(?:\\(|$)`).test(c.questionRef))
        .reduce((n,c) => n+c.totalMarks,0),q).toBe(marks);
    }
    expect(cards.filter(c => c.questionRef.includes('Q6A(')).map(c => c.totalMarks)).toEqual([15,5,5]);
    expect(card('6b').totalMarks).toBe(25);
    expect(card('6b').mathematicsScale?.marks).toEqual([0,5,10,15,20,25]);
  });
  it('uses the paper-specific scales and independent tax/pie scoring components', () => {
    expect(card('1-a-i').mathematicsScale?.marks).toEqual([0,4,7,10]);
    expect(card('2-a').mathematicsScale?.marks).toEqual([0,5,10]);
    expect(card('6a-a-i').mathematicsScale?.marks).toEqual([0,7,15]);
    expect(card('7-b').mathematicsScale?.components?.map(c => c.marks)).toEqual([[0,3,4,5],[0,10,20]]);
    expect(card('7-c-i').mathematicsScale?.components?.map(c => c.marks)).toEqual([[0,3,4,5],[0,4,7,10]]);
    for (const suffix of ['1-a-i','3-a-i','4-b-i','7-a-i']) {
      expect(ordinary2014p2.cards.find(c => c.id === card(suffix).id)?.printedParts).toHaveLength(2);
    }
  });
  it('preserves standalone data, accessible prompts, source figures and exact Atlas alternatives', () => {
    const spec = resolveCurriculumSpecification('mathematics',2014)!;
    for (const task of ordinary2014p2.cards) {
      const c = card(task.id.split('-q')[1]);
      expect(c.stem ?? '').toBe(task.stem ?? '');
      expect(c.questionText).toBe(task.questionText);
      expect(c.sourceMaterial?.pages).toEqual(task.sourcePages);
      expect(c.mathematicsScale?.schemePages).toEqual(task.schemePages);
      expect(c.mathematicsScale?.marks).toEqual(task.permittedMarks);
      expect(findCanonicalTopic(spec,c.topicId)).toBeDefined();
      expect(c.questionFigure?.src).toContain('maths-2014-OL-ask-p2-');
      expect(c.questionFigure?.alt).toContain(task.questionText);
      expect(c.figure?.solution).toBe(true);
      const q = task.printedParts[0].match(/^Q(\d+[A-Z]?)/)![1];
      expect(examTopicIdsForQuestion('mathematics','ordinary',2014,'main',q,'p2','ev',ordinary2014p2.paperFileid))
        .toEqual(expect.arrayContaining(task.examTopicIds));
    }
    expect(card('3-b-ii').stem).toContain('(x + 2)²');
    expect(card('7-c-iv').stem).toContain('€241 million');
    expect(card('8-c-ii').stem).toContain('154 m');
    expect(card('9-b-ii').stem).toContain('11°');
  });
  it('flags original-page measurement and discloses the official pie-chart typo', () => {
    for (const suffix of ['6a-a-i','6a-a-ii']) expect(card(suffix).sourceMaterial?.measurementRequired).toBe(true);
    expect(card('7-b').figure?.sourceNote).toContain('37°');
    expect(card('7-a-i').figure?.sourceNote).toContain('1,710,000');
  });
});

describe('2013 Higher Project Maths Paper 1', () => {
  const cards = HIGHER.filter(c => c.id.startsWith('maths-2013-hl-p1-project-'));
  const card = (suffix: string) => {
    const c = cards.find(c => c.id === `maths-2013-hl-p1-project-q${suffix}`);
    if (!c || c.kind !== 'question') throw new Error(`Missing ${suffix}`);
    return c;
  };
  it('retains every independently reviewed task and the full 300 marks', () => {
    expect(cards.map(c => c.id).sort()).toEqual(higher2013project1.cards.map(c => c.id).sort());
    expect(cards).toHaveLength(34);
    expect(cards.reduce((n,c) => n+c.totalMarks,0)).toBe(300);
    for (const [q,marks] of Object.entries(higher2013project1.printedQuestionMarks)) {
      expect(cards.filter(c => c.questionRef.includes(`Q${q}(`)).reduce((n,c) => n+c.totalMarks,0)).toBe(marks);
    }
  });
  it('applies the minus-one option to the ten starred scales only', () => {
    const starred = ['3-b','4-a-i','4-a-ii','4-b','6-a','8-a','8-b','8-c','8-d','8-e'];
    expect(cards.filter(c => c.kind === 'question' && c.mathematicsScale?.fullCreditMinusOne).map(c => c.id).sort())
      .toEqual(starred.map(s => card(s).id).sort());
    expect(card('4-a-ii').mathematicsScale?.marks).toEqual([0,3,5,8,10]);
    expect(card('7-g').mathematicsScale?.marks).toEqual([0,2,3,4,5]);
  });
  it('binds the Project booklet, diagrams and Atlas placement without using the parallel legacy edition', () => {
    const spec = resolveCurriculumSpecification('mathematics',2013)!;
    for (const task of higher2013project1.cards) {
      const c = card(task.id.split('-q')[1]);
      expect(c.sourceMaterial?.sourceFileid).toBe('LC003ALP130EV.pdf');
      expect(c.mathematicsScale?.schemeFileid).toBe('LC003ALP030EV.pdf');
      expect(c.sourceMaterial?.pages).toEqual(task.sourcePages);
      expect(c.mathematicsScale?.schemePages).toEqual(task.schemePages);
      expect(c.mathematicsScale?.marks).toEqual(task.permittedMarks);
      expect(findCanonicalTopic(spec,c.topicId)).toBeDefined();
      expect(c.questionFigure?.src).toContain('maths-2013-HL-ask-p1-project-');
      expect(c.questionFigure?.alt).toContain(task.questionText);
      expect(c.figure?.src).toContain('maths-2013-HL-scheme-project-');
      expect(c.figure?.solution).toBe(true);
      const q = task.printedParts[0].match(/^Q(\d+)/)![1];
      expect(examTopicIdsForQuestion('mathematics','higher',2013,'main',q,'p1','ev',higher2013project1.paperFileid))
        .toEqual(expect.arrayContaining(task.examTopicIds));
    }
    expect(card('5-b').questionFigure?.alt).toContain('twelve original graphs');
    expect(card('6-d').questionFigure?.alt).toContain('Part (b)');
    expect(card('9-e').stem).toContain('uₙ = an² + bn');
  });
  it('clarifies genuine source mistakes while preserving the original models', () => {
    expect(card('4-a-ii').figure?.sourceNote).toContain('€392');
    expect(card('6-d').figure?.sourceNote).toContain('part (b)');
    expect(card('8-d').figure?.sourceNote).toContain('80 + 9(t − 10)');
    expect(card('9-e').figure?.sourceNote).toContain('4134');
    expect(card('1-b').figure?.sourceNote).toBeUndefined();
  });
});

describe('2013 Higher Project Maths Paper 2', () => {
  const cards = HIGHER.filter(c => c.id.startsWith('maths-2013-hl-p2-project-'));
  const card = (suffix: string) => {
    const c = cards.find(c => c.id === `maths-2013-hl-p2-project-q${suffix}`);
    if (!c || c.kind !== 'question') throw new Error(`Missing ${suffix}`);
    return c;
  };
  it('retains every independently reviewed task and the all 325 offered marks including both Q6 alternatives', () => {
    expect(cards.map(c => c.id).sort()).toEqual(higher2013project2.cards.map(c => c.id).sort());
    expect(cards).toHaveLength(44);
    expect(cards.reduce((n,c) => n+c.totalMarks,0)).toBe(325);
    for (const [q,marks] of Object.entries(higher2013project2.printedQuestionMarks)) {
      expect(cards.filter(c => c.questionRef.includes(`Q${q}(`)).reduce((n,c) => n+c.totalMarks,0)).toBe(marks);
    }
  });
  it('retains the joint boundaries and Paper 2 ladders', () => {
    expect(higher2013project2.cards.find(c => c.id === card('1-b').id)?.printedParts).toHaveLength(2);
    expect(higher2013project2.cards.find(c => c.id === card('6a-a').id)?.printedParts).toHaveLength(3);
    expect(card('6a-a').mathematicsScale?.marks).toEqual([0,3,7,9,10]);
    expect(card('6b-b').mathematicsScale?.marks).toEqual([0,5,10,15]);
    expect(card('7-f-ii').mathematicsScale?.marks).toEqual([0,5]);
    expect(card('9-c-i').mathematicsScale?.marks).toEqual([0,5,10]);
    const starred=['5-b-i','5-c','8-a-i','8-a-ii','8-b','9-c-ii','9-c-iii'];
    expect(cards.filter(c => c.kind === 'question' && c.mathematicsScale?.fullCreditMinusOne).map(c => c.id).sort())
      .toEqual(starred.map(s => card(s).id).sort());
  });
  it('keeps every diagram, exact edition, source page and Atlas placement', () => {
    const spec=resolveCurriculumSpecification('mathematics',2013)!;
    for (const task of higher2013project2.cards) {
      const c=card(task.id.split('-q')[1]);
      expect(c.sourceMaterial?.sourceFileid).toBe('LC003ALP230EV.pdf');
      expect(c.sourceMaterial?.pages).toEqual(task.sourcePages);
      expect(c.mathematicsScale?.schemeFileid).toBe('LC003ALP030EV.pdf');
      expect(c.mathematicsScale?.schemePages).toEqual(task.schemePages);
      expect(c.mathematicsScale?.marks).toEqual(task.permittedMarks);
      expect(findCanonicalTopic(spec,c.topicId)).toBeDefined();
      expect(c.questionFigure?.src).toContain('maths-2013-HL-ask-p2-project-');
      expect(c.questionFigure?.alt).toContain(task.questionText);
      expect(c.figure?.src).toContain('maths-2013-HL-scheme-project-');
      expect(c.figure?.solution).toBe(true);
      const q=task.printedParts[0].match(/^Q(\d+[A-Z]?)/)![1];
      expect(examTopicIdsForQuestion('mathematics','higher',2013,'main',q,'p2','ev',higher2013project2.paperFileid))
        .toEqual(expect.arrayContaining(task.examTopicIds));
    }
    expect(card('6a-c').sourceMaterial?.measurementRequired).toBe(true);
    expect(card('8-b').questionFigure?.alt).toContain('∠RHP = 36°');
    expect(card('9-c-iii').questionFigure?.alt).toContain('semicircles');
  });
  it('discloses the acknowledged faulty question and preserves its full-credit guidance', () => {
    for (const suffix of ['8-a-i','8-a-ii','8-b']) {
      expect(card(suffix).figure?.sourceNote).toContain('inconsistent data');
      expect(card(suffix).figure?.sourceNote).toContain('full marks');
      expect(card(suffix).mathematicsScale?.schemePages).toContain(75);
    }
    expect(card('7-e-i').figure?.sourceNote).toContain('[0·6684, 0·7316]');
    expect(card('9-c-i').figure?.sourceNote).toContain('4² + 2²');
    expect(card('9-c-i').figure?.sourceNote).toContain('10 marks');
  });
});


describe('2013 Ordinary Project Maths Paper 1', () => {
  const cards = ORDINARY.filter(c => c.id.startsWith('maths-2013-ol-p1-project-'));
  const card = (suffix: string) => {
    const c = cards.find(c => c.id === `maths-2013-ol-p1-project-q${suffix}`);
    if (!c || c.kind !== 'question') throw new Error(`Missing ${suffix}`);
    return c;
  };
  it('retains all 39 marking units with one choose-five card', () => {
    expect(cards.map(c => c.id).sort()).toEqual(ordinary2013project1.cards.map(c => c.id).sort());
    expect(cards).toHaveLength(39);
    expect(cards.filter(c => c.id.includes('-q3-b-ii-'))).toHaveLength(1);
    const c = card('3-b-ii-abcde');
    const task = ordinary2013project1.cards.find(t => t.id === c.id)!;
    expect(task.selectionChoice?.pool).toEqual(['A','B','C','D','E','F','G']);
    expect(task.selectionChoice?.choose).toBe(5);
    expect(c.questionText).toBe('Mark 5 of the numbers in the table on the number line below and label each number clearly.');
    expect(c.mathematicsScale?.marks).toEqual([0,2,4,5]);
    expect(c.totalMarks).toBe(5);
    expect(cards.reduce((n,c)=>n+c.totalMarks,0)).toBe(300);
  });
  it('preserves the exceptional holistic differentiation rule and the exact older scales', () => {
    expect(card('5').totalMarks).toBe(25);
    expect(card('5').mathematicsScale?.marks).toEqual([0,8,17,25]);
    expect(card('5').figure?.sourceNote).toContain('outside the syllabus');
    expect(ordinary2013project1.cards.find(c => c.id===card('5').id)?.printedParts).toEqual(['Q5(a)','Q5(b)','Q5(c)']);
    expect(card('2-a').mathematicsScale?.marks).toEqual([0,2,5,8,10]);
    expect(card('8-b').mathematicsScale?.marks).toEqual([0,5]);
    expect(cards.filter(c => c.kind==='question' && c.mathematicsScale?.fullCreditMinusOne).map(c=>c.id).sort())
      .toEqual(['1-d','3-a','4-a','4-c','7-b','7-e'].map(s=>card(s).id).sort());
  });
  it('keeps exact Project booklet sources, complete diagrams and canonical Atlas placements', () => {
    const spec=resolveCurriculumSpecification('mathematics',2013)!;
    for (const task of ordinary2013project1.cards) {
      const c=card(task.id.split('-q')[1]);
      expect(c.paperFileid).toBe('LC003GLP130EV');
      expect(c.sourceMaterial?.sourceFileid).toBe('LC003GLP130EV.pdf');
      expect(c.sourceMaterial?.pages).toEqual(task.sourcePages);
      expect(c.mathematicsScale?.schemeFileid).toBe('LC003GLP030EV.pdf');
      expect(c.mathematicsScale?.schemePages).toEqual(task.schemePages);
      expect(c.mathematicsScale?.marks).toEqual(task.permittedMarks);
      expect(findCanonicalTopic(spec,c.topicId)).toBeDefined();
      expect(c.questionFigure?.src).toContain('maths-2013-OL-ask-p1-project-');
      expect(c.figure?.src).toContain('maths-2013-OL-scheme-project-');
      expect(c.figure?.solution).toBe(true);
      const q=task.printedParts[0].match(/^Q(\d+)/)![1];
      expect(examTopicIdsForQuestion('mathematics','ordinary',2013,'main',q,'p1','ev',ordinary2013project1.paperFileid))
        .toEqual(expect.arrayContaining(task.examTopicIds));
    }
    expect(card('5').questionFigure?.alt).toContain('(c)');
    expect(card('3-b-ii-abcde').questionFigure?.alt).toContain('Mark five');
    expect(card('9-b').questionFigure?.alt).toContain('20 items');
  });
});


describe('2013 Ordinary Project Maths Paper 2', () => {
  const cards = ORDINARY.filter(c => c.id.startsWith('maths-2013-ol-p2-project-'));
  const card = (suffix: string) => {
    const c = cards.find(c => c.id === `maths-2013-ol-p2-project-q${suffix}`);
    if (!c || c.kind !== 'question') throw new Error(`Missing ${suffix}`);
    return c;
  };
  it('retains every marking unit, both geometry routes and the joint spinner scale', () => {
    expect(cards.map(c=>c.id).sort()).toEqual(ordinary2013project2.cards.map(c=>c.id).sort());
    expect(cards).toHaveLength(40);
    expect(cards.reduce((n,c)=>n+c.totalMarks,0)).toBe(325);
    expect(cards.filter(c=>!c.id.endsWith('-q6b')).reduce((n,c)=>n+c.totalMarks,0)).toBe(300);
    expect(ordinary2013project2.cards.find(c=>c.id===card('2-a-i').id)?.printedParts).toEqual(['Q2(a)(i)','Q2(a)(ii)']);
    expect(card('2-a-i').questionFigure?.alt).toContain('(ii) List all');
    expect(card('6b').totalMarks).toBe(25);
    expect(card('6b').mathematicsScale?.marks).toEqual([0,6,12,19,25]);
    expect(card('6a-b').sourceMaterial?.measurementRequired).toBe(true);
  });
  it('uses the exact Paper 2 ladders and only its ten starred deductions', () => {
    expect(card('1-a').mathematicsScale?.marks).toEqual([0,3,5]);
    expect(card('2-c').mathematicsScale?.marks).toEqual([0,3,4,5]);
    expect(card('1-b').mathematicsScale?.marks).toEqual([0,4,7,10]);
    expect(card('4-b').mathematicsScale?.marks).toEqual([0,2,5,8,10]);
    expect(card('7-a').mathematicsScale?.marks).toEqual([0,4,7,11,15]);
    expect(cards.filter(c=>c.kind==='question' && c.mathematicsScale?.fullCreditMinusOne).map(c=>c.id).sort())
      .toEqual(['5-a','5-b','5-c','7-d-i','8-a-ii','8-a-iv','8-b-i','8-b-iv','8-c-i','8-c-ii'].map(s=>card(s).id).sort());
    expect(card('7-h').totalMarks).toBe(10);
    expect(card('7-i').totalMarks).toBe(5);
    expect(card('7-i').figure?.src).toContain('p047-i1');
    expect(card('7-i').questionFigure?.alt).toContain('scatter plot');
    expect(card('7-f').questionFigure?.alt).toContain('75 174');
    expect(card('8-c-ii').questionFigure?.alt).toContain('midpoint');
  });
  it('keeps exact Project booklet sources, diagrams and canonical Atlas placements', () => {
    const spec=resolveCurriculumSpecification('mathematics',2013)!;
    for (const task of ordinary2013project2.cards) {
      const c=card(task.id.split('-q')[1]);
      expect(c.paperFileid).toBe('LC003GLP230EV');
      expect(c.sourceMaterial?.sourceFileid).toBe('LC003GLP230EV.pdf');
      expect(c.sourceMaterial?.pages).toEqual(task.sourcePages);
      expect(c.mathematicsScale?.schemeFileid).toBe('LC003GLP030EV.pdf');
      expect(c.mathematicsScale?.schemePages).toEqual(task.schemePages);
      expect(c.mathematicsScale?.marks).toEqual(task.permittedMarks);
      expect(findCanonicalTopic(spec,c.topicId)).toBeDefined();
      expect(c.questionFigure?.src).toContain('maths-2013-OL-ask-p2-project-');
      expect(c.figure?.src).toContain('maths-2013-OL-scheme-project-');
      expect(c.figure?.solution).toBe(true);
      const q=task.printedParts[0].match(/^Q(\d+[A-Z]?)/)![1];
      expect(examTopicIdsForQuestion('mathematics','ordinary',2013,'main',q,'p2','ev',ordinary2013project2.paperFileid))
        .toEqual(expect.arrayContaining(task.examTopicIds));
    }
  });
});

describe('2013 Foundation Project Maths Paper 1', () => {
  const cards = FOUNDATION.filter(c => c.id.startsWith('maths-2013-fl-p1-project-'));
  const card = (suffix: string) => {
    const c = cards.find(c => c.id === `maths-2013-fl-p1-project-q${suffix}`);
    if (!c || c.kind !== 'question') throw new Error(`Missing ${suffix}`);
    return c;
  };
  it('retains every shared scale with one freely chosen table row', () => {
    expect(cards.map(c=>c.id).sort()).toEqual(foundation2013project1.cards.map(c=>c.id).sort());
    expect(cards).toHaveLength(34);
    expect(card('1').totalMarks).toBe(25);
    expect(foundation2013project1.cards.find(c=>c.id===card('1').id)?.printedParts).toEqual(['Q1(a)','Q1(b)','Q1(c)']);
    expect(card('1').questionFigure?.alt).toContain('1/(0·5)²');
    const c = card('10-b-row-2');
    const t = foundation2013project1.cards.find(t=>t.id===c.id)!;
    expect(t.selectionChoice?.pool).toEqual(['2','3','4','5','6']);
    expect(t.printedParts).toEqual(['Q10(b)','Q10(c)']);
    expect(c.totalMarks).toBe(5);
    expect(c.questionText).toContain('using the numbers in one row of the table');
    expect(cards.filter(c=>c.id.includes('-row-'))).toHaveLength(1);
    expect(cards.reduce((n,c)=>n+c.totalMarks,0)).toBe(300);
  });
  it('uses Foundation ladders and exactly the six starred tasks', () => {
    expect(card('1').mathematicsScale?.marks).toEqual([0,6,12,19,25]);
    expect(card('2-a').mathematicsScale?.marks).toEqual([0,4,7,11,15]);
    expect(card('2-b').mathematicsScale?.marks).toEqual([0,3,7,10]);
    expect(card('3-a').mathematicsScale?.marks).toEqual([0,6,10,15]);
    expect(card('4-a').mathematicsScale?.marks).toEqual([0,7,13,20]);
    expect(card('4-b').mathematicsScale?.marks).toEqual([0,2,4,5]);
    expect(card('5-b').mathematicsScale?.marks).toEqual([0,2,5]);
    expect(card('9-a-i').mathematicsScale?.marks).toEqual([0,5,10]);
    expect(cards.filter(c=>c.kind==='question' && c.mathematicsScale?.fullCreditMinusOne).map(c=>c.id).sort())
      .toEqual(['1','3-a','3-b','5-a','5-b','5-c'].map(s=>card(s).id).sort());
    expect(card('8-b').section).toBe('A');
    expect(card('9-a-i').section).toBe('B');
    expect(card('9-a-iv').questionFigure?.alt).toContain('18:40–22:35');
    expect(card('10-h').questionFigure?.alt).toContain('0 ≤ x ≤ 75');
  });
  it('keeps exact Foundation Project sources, visual answers and canonical Atlas placements', () => {
    const spec=resolveCurriculumSpecification('mathematics',2013)!;
    for (const task of foundation2013project1.cards) {
      const c=card(task.id.split('-q')[1]);
      expect(c.paperFileid).toBe('LC003BLP130EV');
      expect(c.sourceMaterial?.sourceFileid).toBe('LC003BLP130EV.pdf');
      expect(c.sourceMaterial?.pages).toEqual(task.sourcePages);
      expect(c.mathematicsScale?.schemeFileid).toBe('LC003BLP030EV.pdf');
      expect(c.mathematicsScale?.schemePages).toEqual(task.schemePages);
      expect(c.mathematicsScale?.marks).toEqual(task.permittedMarks);
      expect(findCanonicalTopic(spec,c.topicId)).toBeDefined();
      expect(c.questionFigure?.src).toContain('maths-2013-FL-ask-p1-project-');
      expect(c.figure?.src).toContain('maths-2013-FL-scheme-project-');
      expect(c.figure?.solution).toBe(true);
      const q=task.printedParts[0].match(/^Q(\d+)/)![1];
      expect(examTopicIdsForQuestion('mathematics','foundation',2013,'main',q,'p1','ev',foundation2013project1.paperFileid))
        .toEqual(expect.arrayContaining(task.examTopicIds));
    }
  });
});


describe('2013 Foundation Project Maths Paper 2', () => {
  const cards = FOUNDATION.filter(c => c.id.startsWith('maths-2013-fl-p2-project-'));
  const card = (suffix: string) => {
    const c = cards.find(c => c.id === `maths-2013-fl-p2-project-q${suffix}`);
    if (!c || c.kind !== 'question') throw new Error(`Missing ${suffix}`);
    return c;
  };
  it('keeps one menu response and one freely chosen parallel pair', () => {
    expect(cards.map(c=>c.id).sort()).toEqual(foundation2013project2.cards.map(c=>c.id).sort());
    expect(cards).toHaveLength(47);
    expect(cards.filter(c=>c.id.includes('-meal-'))).toHaveLength(1);
    const meal = card('3-a-meal-01');
    expect(meal.totalMarks).toBe(15);
    expect(meal.questionText).toBe('Write one three-course lunch that Sarah could select.');
    expect(meal.mathematicsScale?.practiceInstruction).toContain('one starter, one main course and one dessert');
    const parallel = foundation2013project2.cards.filter(c=>c.id.includes('-q8b-c-'));
    expect(parallel).toHaveLength(1);
    expect(parallel[0].selectionChoice?.pool).toEqual(['AB and DC','AD and BC']);
    expect(foundation2013project2.cards).toHaveLength(47);
    expect(foundation2013project2.cards.reduce((n,c)=>n+c.totalMarks,0)).toBe(325);
    expect(foundation2013project2.cards.filter(c=>!c.printedParts[0].startsWith('Q8B')).reduce((n,c)=>n+c.totalMarks,0)).toBe(300);
    expect(foundation2013project2.cards.find(c=>c.id.endsWith('-q2-c'))?.printedParts).toEqual(['Q2(c)(i)','Q2(c)(ii)','Q2(c)(iii)']);
    expect(card('2-b').totalMarks).toBe(5);
    expect(card('3-c').totalMarks).toBe(5);
  });
  it('uses Paper 2 ladders and exactly seven starred units', () => {
    expect(card('1-a-i').mathematicsScale?.marks).toEqual([0,3,4,5]);
    expect(card('2-a-i').mathematicsScale?.marks).toEqual([0,4,8,10]);
    expect(card('2-b').mathematicsScale?.marks).toEqual([0,2,3,4,5]);
    expect(card('3-a-meal-01').mathematicsScale?.marks).toEqual([0,5,13,15]);
    expect(card('6-a').mathematicsScale?.marks).toEqual([0,4,8,12,15]);
    expect(card('8a-a').mathematicsScale?.marks).toEqual([0,4,8,9,10]);
    expect(card('10-a-i').mathematicsScale?.marks).toEqual([0,7,15]);
    expect(cards.filter(c=>c.kind==='question' && c.mathematicsScale?.fullCreditMinusOne).map(c=>c.id).sort())
      .toEqual(['7-b-i','7-b-ii','7-b-iii','8b-a','10-a-ii','10-b-ii','10-c'].map(s=>card(s).id).sort());
  });
  it('preserves complete original geometry and the sample-answer correction', () => {
    expect(card('4-e').figure?.sourceNote).toContain('repeats age 55');
    expect(card('3-a-meal-01').figure?.sourceNote).toContain('one starter, one main course and one dessert');
    expect(card('7-b-iii').questionFigure?.alt).toContain('|Z′Y′| = 8 cm');
    expect(card('8a-b').questionFigure?.alt).toContain('|PQ| = 7 cm');
    expect(card('8b-e').questionFigure?.alt).toContain('axial symmetry');
    expect(card('10-b-ii').questionFigure?.alt).toContain('70 m');
    expect(card('8b-e').section).toBe('A');
    expect(card('9-a').section).toBe('B');
  });
  it('binds every card to the exact Project sources and canonical Atlas topics', () => {
    const spec=resolveCurriculumSpecification('mathematics',2013)!;
    for (const task of foundation2013project2.cards) {
      const c=card(task.id.split('-q')[1]);
      expect(c.paperFileid).toBe('LC003BLP230EV');
      expect(c.sourceMaterial?.sourceFileid).toBe('LC003BLP230EV.pdf');
      expect(c.sourceMaterial?.pages).toEqual(task.sourcePages);
      expect(c.mathematicsScale?.schemeFileid).toBe('LC003BLP030EV.pdf');
      expect(c.mathematicsScale?.schemePages).toEqual(task.schemePages);
      expect(c.mathematicsScale?.marks).toEqual(task.permittedMarks);
      expect(findCanonicalTopic(spec,c.topicId)).toBeDefined();
      expect(c.questionFigure?.src).toContain('maths-2013-FL-ask-p2-project-');
      expect(c.figure?.src).toContain('maths-2013-FL-scheme-project-');
      expect(c.figure?.solution).toBe(true);
      const q=task.printedParts[0].match(/^Q(\d+[A-Z]?)/)![1];
      expect(examTopicIdsForQuestion('mathematics','foundation',2013,'main',q,'p2','ev',foundation2013project2.paperFileid))
        .toEqual(expect.arrayContaining(task.examTopicIds));
    }
  });
});


describe('2013 Higher Project Maths Phase 2 Paper 1', () => {
  const cards = HIGHER.filter(c => c.id.startsWith('maths-2013-hl-p1-q'));
  const card = (suffix: string) => {
    const c = cards.find(c => c.id === `maths-2013-hl-p1-q${suffix}`);
    if (!c || c.kind !== 'question') throw new Error(`Missing ${suffix}`);
    return c;
  };
  it('retains all eight required questions including the eleven old-syllabus calculus tasks', () => {
    expect(cards.map(c=>c.id).sort()).toEqual(higher2013phase2p1.cards.map(c=>c.id).sort());
    expect(cards).toHaveLength(34);
    expect(cards.reduce((n,c)=>n+c.totalMarks,0)).toBe(300);
    for (const [q,marks] of Object.entries(higher2013phase2p1.printedQuestionMarks)) {
      const tasks=cards.filter(c=>c.questionRef.includes(`Q${q}(`));
      expect(tasks.reduce((n,c)=>n+c.totalMarks,0)).toBe(marks);
      expect(tasks.every(c=>c.section===(Number(q)<=4?'A':Number(q)<=6?'B':'C'))).toBe(true);
    }
    expect(cards.filter(c=>c.section==='C')).toHaveLength(11);
  });
  it('uses the paper-specific ladders and only its four starred deductions', () => {
    expect(cards.filter(c=>c.kind==='question' && c.mathematicsScale?.fullCreditMinusOne).map(c=>c.id).sort())
      .toEqual(['3-b','4-a-i','4-a-ii','4-b'].map(s=>card(s).id).sort());
    expect(card('7-a').mathematicsScale?.marks).toEqual([0,5,10,15]);
    expect(card('7-c-ii').mathematicsScale?.marks).toEqual([0,4,7,11,15]);
    expect(card('7-b-ii').mathematicsScale?.marks).toEqual([0,2,3,4,5]);
  });
  it('binds every card to the Phase 2 sources and exact-booklet Atlas topics', () => {
    const spec=resolveCurriculumSpecification('mathematics',2013)!;
    for (const task of higher2013phase2p1.cards) {
      const c=card(task.id.split('-q')[1]);
      expect(c.sourceMaterial?.sourceFileid).toBe('LC003ALP100EV.pdf');
      expect(c.mathematicsScale?.schemeFileid).toBe('LC003ALP000EV.pdf');
      expect(c.sourceMaterial?.pages).toEqual(task.sourcePages);
      expect(c.mathematicsScale?.schemePages).toEqual(task.schemePages);
      expect(c.mathematicsScale?.marks).toEqual(task.permittedMarks);
      expect(findCanonicalTopic(spec,c.topicId)).toBeDefined();
      expect(c.questionFigure?.alt).toContain(task.questionText);
      expect(c.figure?.src).toMatch(/maths-2013-HL-scheme-p\d/);
      expect(c.figure?.solution).toBe(true);
      const q=task.printedParts[0].match(/^Q(\d+)/)![1];
      expect(examTopicIdsForQuestion('mathematics','higher',2013,'main',q,'p1','ev',higher2013phase2p1.paperFileid))
        .toEqual(expect.arrayContaining(task.examTopicIds));
    }
  });
  it('keeps dependent equations and diagrams while preserving the parallel Phase 3 catalogue', () => {
    expect(card('7-b-ii').questionFigure?.alt).toContain('dy/dx = −2e^t(t + e^t)');
    expect(card('7-c-ii').questionFigure?.alt).toContain('sin⁻¹x');
    expect(card('8-c-iii').questionFigure?.alt).toContain('y = 4x and y = x³');
    expect(card('4-a-ii').figure?.sourceNote).toContain('€392');
    expect(card('4-a-ii').figure?.sourceNote).toContain('€393');
    const names=mathsSchemeCatalogue.map(f=>f.file);
    expect(names.filter(f=>/^maths-2013-HL-scheme-p\d/.test(f))).toHaveLength(78);
    expect(names.filter(f=>f.startsWith('maths-2013-HL-scheme-project-p'))).toHaveLength(78);
    for (const c of [...cards,...HIGHER.filter(c=>c.id.startsWith('maths-2013-hl-p1-project-'))]) {
      if (c.kind !== 'question') throw new Error(`Expected question ${c.id}`);
      expect(names).toContain(c.figure?.src.split('/').at(-1));
    }
  });
});
describe('2013 Higher Project Maths Phase 2 Paper 2', () => {
  const cards = HIGHER.filter(c => c.id.startsWith('maths-2013-hl-p2-q'));
  const card = (suffix: string) => {
    const c = cards.find(c => c.id === `maths-2013-hl-p2-q${suffix}`);
    if (!c || c.kind !== 'question') throw new Error(`Missing ${suffix}`);
    return c;
  };
  it('retains every independently reviewed task and the all 325 offered marks including both Q6 alternatives', () => {
    expect(cards.map(c => c.id).sort()).toEqual(higher2013phase2p2.cards.map(c => c.id).sort());
    expect(cards).toHaveLength(44);
    expect(cards.reduce((n,c) => n+c.totalMarks,0)).toBe(325);
    for (const [q,marks] of Object.entries(higher2013phase2p2.printedQuestionMarks)) {
      expect(cards.filter(c => c.questionRef.includes(`Q${q}(`)).reduce((n,c) => n+c.totalMarks,0)).toBe(marks);
    }
  });
  it('retains the joint boundaries and Paper 2 ladders', () => {
    expect(higher2013phase2p2.cards.find(c => c.id === card('1-b').id)?.printedParts).toHaveLength(2);
    expect(higher2013phase2p2.cards.find(c => c.id === card('6a-a').id)?.printedParts).toHaveLength(3);
    expect(card('6a-a').mathematicsScale?.marks).toEqual([0,3,7,9,10]);
    expect(card('6b-b').mathematicsScale?.marks).toEqual([0,5,10,15]);
    expect(card('7-f-ii').mathematicsScale?.marks).toEqual([0,5]);
    expect(card('9-c-i').mathematicsScale?.marks).toEqual([0,5,10]);
    const starred=['5-b-i','5-c','8-a-i','8-a-ii','8-b','9-c-ii','9-c-iii'];
    expect(cards.filter(c => c.kind === 'question' && c.mathematicsScale?.fullCreditMinusOne).map(c => c.id).sort())
      .toEqual(starred.map(s => card(s).id).sort());
  });
  it('keeps every diagram, exact edition, source page and Atlas placement', () => {
    const spec=resolveCurriculumSpecification('mathematics',2013)!;
    for (const task of higher2013phase2p2.cards) {
      const c=card(task.id.split('-q')[1]);
      expect(c.sourceMaterial?.sourceFileid).toBe('LC003ALP200EV.pdf');
      expect(c.sourceMaterial?.pages).toEqual(task.sourcePages);
      expect(c.mathematicsScale?.schemeFileid).toBe('LC003ALP000EV.pdf');
      expect(c.mathematicsScale?.schemePages).toEqual(task.schemePages);
      expect(c.mathematicsScale?.marks).toEqual(task.permittedMarks);
      expect(findCanonicalTopic(spec,c.topicId)).toBeDefined();
      expect(c.questionFigure?.src).toContain('maths-2013-HL-ask-p2-project-');
      expect(c.questionFigure?.alt).toContain(task.questionText);
      expect(c.figure?.src).toContain('maths-2013-HL-scheme-p');
      expect(c.figure?.solution).toBe(true);
      const q=task.printedParts[0].match(/^Q(\d+[A-Z]?)/)![1];
      expect(examTopicIdsForQuestion('mathematics','higher',2013,'main',q,'p2','ev',higher2013phase2p2.paperFileid))
        .toEqual(expect.arrayContaining(task.examTopicIds));
    }
    expect(card('6a-c').sourceMaterial?.measurementRequired).toBe(true);
    expect(card('8-b').questionFigure?.alt).toContain('∠RHP = 36°');
    expect(card('9-c-iii').questionFigure?.alt).toContain('semicircles');
  });
  it('discloses the acknowledged faulty question and preserves its full-credit guidance', () => {
    for (const suffix of ['8-a-i','8-a-ii','8-b']) {
      expect(card(suffix).figure?.sourceNote).toContain('inconsistent data');
      expect(card(suffix).figure?.sourceNote).toContain('full marks');
      expect(card(suffix).mathematicsScale?.schemePages).toContain(75);
    }
    expect(card('7-e-i').figure?.sourceNote).toContain('[0·6684, 0·7316]');
    expect(card('9-c-i').figure?.sourceNote).toContain('4² + 2²');
    expect(card('9-c-i').figure?.sourceNote).toContain('10 marks');
  });
});

describe('2013 Ordinary Project Maths Phase 2 Paper 1', () => {
  const cards = ORDINARY.filter(c => c.id.startsWith('maths-2013-ol-p1-q'));
  const card = (suffix: string) => {
    const c = cards.find(c => c.id === `maths-2013-ol-p1-q${suffix}`);
    if (!c || c.kind !== 'question') throw new Error(`Missing ${suffix}`);
    return c;
  };
  it('retains all 41 marking units with one choose-five card', () => {
    expect(cards.map(c => c.id).sort()).toEqual(ordinary2013phase2p1.cards.map(c => c.id).sort());
    expect(cards).toHaveLength(41);
    expect(cards.filter(c => c.id.includes('-q3-b-ii-'))).toHaveLength(1);
    const c = card('3-b-ii-abcde');
    const task = ordinary2013phase2p1.cards.find(t => t.id === c.id)!;
    expect(task.selectionChoice?.pool).toEqual(['A','B','C','D','E','F','G']);
    expect(task.selectionChoice?.choose).toBe(5);
    expect(c.questionText).toBe('Mark 5 of the numbers in the table on the number line below and label each number clearly.');
    expect(c.mathematicsScale?.marks).toEqual([0,2,4,5]);
    expect(c.totalMarks).toBe(5);
    expect(cards.reduce((n,c)=>n+c.totalMarks,0)).toBe(300);
  });
  it('keeps every separately assessed calculus task and the eight starred scales', () => {
    expect(cards.filter(c=>c.id.startsWith('maths-2013-ol-p1-q7-'))).toHaveLength(7);
    expect(['a','b-i','b-ii','c-i','c-ii','c-iii','c-iv'].map(s=>card(`7-${s}`).totalMarks)).toEqual([10,5,10,5,10,5,5]);
    expect(card('7-b-ii').mathematicsScale?.marks).toEqual([0,2,5,8,10]);
    expect(card('8-a').mathematicsScale?.marks).toEqual([0,4,7,11,15]);
    expect(card('6-b').mathematicsScale?.marks).toEqual([0,5]);
    expect(cards.filter(c=>c.kind==='question' && c.mathematicsScale?.fullCreditMinusOne).map(c=>c.id).sort())
      .toEqual(['1-d','3-a','4-a','4-c','5-b','5-e','8-c-i','8-c-ii'].map(s=>card(s).id).sort());
    for (const c of cards) {
      const q=Number(c.id.match(/-q(\d+)/)![1]);
      expect(c.section).toBe(q<=4 ? 'A' : q<=6 ? 'B' : 'C');
    }
  });
  it('keeps exact Project booklet sources, complete diagrams and canonical Atlas placements', () => {
    const spec=resolveCurriculumSpecification('mathematics',2013)!;
    for (const task of ordinary2013phase2p1.cards) {
      const c=card(task.id.split('-q')[1]);
      expect(c.paperFileid).toBe('LC003GLP100EV');
      expect(c.sourceMaterial?.sourceFileid).toBe('LC003GLP100EV.pdf');
      expect(c.sourceMaterial?.pages).toEqual(task.sourcePages);
      expect(c.mathematicsScale?.schemeFileid).toBe('LC003GLP000EV.pdf');
      expect(c.mathematicsScale?.schemePages).toEqual(task.schemePages);
      expect(c.mathematicsScale?.marks).toEqual(task.permittedMarks);
      expect(findCanonicalTopic(spec,c.topicId)).toBeDefined();
      expect(c.questionFigure?.src).toContain('maths-2013-OL-ask-p1-');
      expect(c.figure?.src).toContain('maths-2013-OL-scheme-p');
      expect(c.figure?.solution).toBe(true);
      const q=task.printedParts[0].match(/^Q(\d+)/)![1];
      expect(examTopicIdsForQuestion('mathematics','ordinary',2013,'main',q,'p1','ev',ordinary2013phase2p1.paperFileid))
        .toEqual(expect.arrayContaining(task.examTopicIds));
    }
    expect(card('3-b-ii-abcde').questionText).toContain('Mark 5 of the numbers');
    expect(card('7-c-iii').questionFigure?.alt).toContain('slope of l₁');
    expect(card('8-b-ii').questionFigure?.alt).toContain('local maximum');
    expect(card('1-d').rows.map(r=>r.verbatim).join(' ')).toContain('−1 − 2i');
    expect(card('6-f').rows.map(r=>r.verbatim).join(' ')).toContain('other valid formula');
    expect(card('8-c-ii').totalMarks).toBe(5);
  });
});

describe('2013 Ordinary Project Maths Phase 2 Paper 2', () => {
  const cards = ORDINARY.filter(c => c.id.startsWith('maths-2013-ol-p2-q'));
  const card = (suffix: string) => {
    const c = cards.find(c => c.id === `maths-2013-ol-p2-q${suffix}`);
    if (!c || c.kind !== 'question') throw new Error(`Missing ${suffix}`);
    return c;
  };
  it('retains every marking unit, both geometry routes and the joint spinner scale', () => {
    expect(cards.map(c=>c.id).sort()).toEqual(ordinary2013phase2p2.cards.map(c=>c.id).sort());
    expect(cards).toHaveLength(40);
    expect(cards.reduce((n,c)=>n+c.totalMarks,0)).toBe(325);
    expect(cards.filter(c=>!c.id.endsWith('-q6b')).reduce((n,c)=>n+c.totalMarks,0)).toBe(300);
    expect(ordinary2013phase2p2.cards.find(c=>c.id===card('2-a-i').id)?.printedParts).toEqual(['Q2(a)(i)','Q2(a)(ii)']);
    expect(card('2-a-i').questionFigure?.alt).toContain('(ii) List all');
    expect(card('6b').totalMarks).toBe(25);
    expect(card('6b').mathematicsScale?.marks).toEqual([0,6,12,19,25]);
    expect(card('6a-b').sourceMaterial?.measurementRequired).toBe(true);
  });
  it('uses the exact Paper 2 ladders and only its ten starred deductions', () => {
    expect(card('1-a').mathematicsScale?.marks).toEqual([0,3,5]);
    expect(card('2-c').mathematicsScale?.marks).toEqual([0,3,4,5]);
    expect(card('1-b').mathematicsScale?.marks).toEqual([0,4,7,10]);
    expect(card('4-b').mathematicsScale?.marks).toEqual([0,2,5,8,10]);
    expect(card('7-a').mathematicsScale?.marks).toEqual([0,4,7,11,15]);
    expect(cards.filter(c=>c.kind==='question' && c.mathematicsScale?.fullCreditMinusOne).map(c=>c.id).sort())
      .toEqual(['5-a','5-b','5-c','7-d-i','8-a-ii','8-a-iv','8-b-i','8-b-iv','8-c-i','8-c-ii'].map(s=>card(s).id).sort());
    expect(card('7-h').totalMarks).toBe(10);
    expect(card('7-i').totalMarks).toBe(5);
    expect(card('7-i').figure?.src).toContain('p047-i1');
    expect(card('7-i').questionFigure?.alt).toContain('scatter plot');
    expect(card('7-f').questionFigure?.alt).toContain('75 174');
    expect(card('8-c-ii').questionFigure?.alt).toContain('midpoint');
  });
  it('keeps exact Phase 2 booklet sources, diagrams and canonical Atlas placements', () => {
    const spec=resolveCurriculumSpecification('mathematics',2013)!;
    for (const task of ordinary2013phase2p2.cards) {
      const c=card(task.id.split('-q')[1]);
      expect(c.paperFileid).toBe('LC003GLP200EV');
      expect(c.sourceMaterial?.sourceFileid).toBe('LC003GLP200EV.pdf');
      expect(c.sourceMaterial?.pages).toEqual(task.sourcePages);
      expect(c.mathematicsScale?.schemeFileid).toBe('LC003GLP000EV.pdf');
      expect(c.mathematicsScale?.schemePages).toEqual(task.schemePages);
      expect(c.mathematicsScale?.marks).toEqual(task.permittedMarks);
      expect(findCanonicalTopic(spec,c.topicId)).toBeDefined();
      expect(c.questionFigure?.src).toContain('maths-2013-OL-ask-p2-project-');
      expect(c.figure?.src).toMatch(/maths-2013-OL-scheme-(?:project-)?p/);
      expect(c.figure?.solution).toBe(true);
      const q=task.printedParts[0].match(/^Q(\d+[A-Z]?)/)![1];
      expect(examTopicIdsForQuestion('mathematics','ordinary',2013,'main',q,'p2','ev',ordinary2013phase2p2.paperFileid))
        .toEqual(expect.arrayContaining(task.examTopicIds));
    }
  });
  it('retains Phase 2-specific credit conditions and exact source images', () => {
    const rows=(suffix:string)=>card(suffix).rows.map(r=>r.verbatim).join(' ');
    expect(rows('3-a')).toContain('y = mx + c but slope not identified');
    expect(rows('3-b')).toContain('y − y₁ = m(x − x₁)');
    for (const part of ['4-a','4-b']) expect(rows(part)).toContain('r² incorrectly');
    expect(rows('4-c')).toContain('(x − 4)² = 16');
    for (const part of ['5-b','5-c']) expect(rows(part)).toContain('not expressed in terms of π');
    for (const part of ['3-a','3-b','4-a','4-b','4-c','5-b','5-c'])
      expect(card(part).figure?.src).toMatch(/maths-2013-OL-scheme-p/);
  });
});

describe('2013 Foundation Project Maths Phase 2 Paper 1', () => {
  const cards = FOUNDATION.filter(c => c.id.startsWith('maths-2013-fl-p1-q'));
  const card = (suffix: string) => {
    const c = cards.find(c => c.id === `maths-2013-fl-p1-q${suffix}`);
    if (!c || c.kind !== 'question') throw new Error(`Missing ${suffix}`);
    return c;
  };
  it('retains every shared scale with one freely chosen table row', () => {
    expect(cards.map(c=>c.id).sort()).toEqual(foundation2013phase2p1.cards.map(c=>c.id).sort());
    expect(cards).toHaveLength(29);
    expect(card('1').totalMarks).toBe(25);
    expect(foundation2013phase2p1.cards.find(c=>c.id===card('1').id)?.printedParts).toEqual(['Q1(a)','Q1(b)','Q1(c)']);
    expect(card('1').questionFigure?.alt).toContain('1/(0·5)²');
    const c = card('9-b-row-2');
    const t = foundation2013phase2p1.cards.find(t=>t.id===c.id)!;
    expect(t.selectionChoice?.pool).toEqual(['2','3','4','5','6']);
    expect(t.printedParts).toEqual(['Q9(b)','Q9(c)']);
    expect(c.totalMarks).toBe(5);
    expect(c.questionText).toContain('using the numbers in one row of the table');
    expect(cards.filter(c=>c.id.includes('-row-'))).toHaveLength(1);
    expect(cards.reduce((n,c)=>n+c.totalMarks,0)).toBe(300);
  });
  it('preserves separate graph components and the joint four read-offs', () => {
    expect(card('10-a').totalMarks).toBe(35);
    expect(card('10-a').mathematicsScale?.components).toEqual([
      {id:'points',label:'Points',code:'25D',marks:[0,6,12,19,25]},
      {id:'graph',label:'Graph',code:'10C',marks:[0,3,7,10],fullCreditMinusOne:true},
    ]);
    expect(card('10-a').mathematicsScale?.fullCreditMinusOne).toBe(false);
    expect(card('10-b').totalMarks).toBe(15);
    expect(foundation2013phase2p1.cards.find(c=>c.id===card('10-b').id)?.printedParts).toHaveLength(4);
    expect(card('6-a').rows.map(r=>r.verbatim).join(' ')).toContain('Correctly finds a² and b² and fails to add');
  });
  it('uses Foundation ladders and exactly the six starred tasks', () => {
    expect(card('1').mathematicsScale?.marks).toEqual([0,6,12,19,25]);
    expect(card('2-a').mathematicsScale?.marks).toEqual([0,4,7,11,15]);
    expect(card('2-b').mathematicsScale?.marks).toEqual([0,3,7,10]);
    expect(card('3-a').mathematicsScale?.marks).toEqual([0,6,10,15]);
    expect(card('4-a').mathematicsScale?.marks).toEqual([0,7,13,20]);
    expect(card('4-b').mathematicsScale?.marks).toEqual([0,2,4,5]);
    expect(card('5-b').mathematicsScale?.marks).toEqual([0,2,5]);
    expect(card('8-a-i').mathematicsScale?.marks).toEqual([0,5,10]);
    expect(cards.filter(c=>c.kind==='question' && c.mathematicsScale?.fullCreditMinusOne).map(c=>c.id).sort())
      .toEqual(['1','3-a','3-b','5-a','5-b','5-c'].map(s=>card(s).id).sort());
    expect(card('7-c').section).toBe('A');
    expect(card('8-a-i').section).toBe('B');
    expect(card('8-a-iv').questionFigure?.alt).toContain('18:40–22:35');
    expect(card('10-a').section).toBe('C');
    expect(card('10-a').questionFigure?.alt).toContain('2x² − 3x − 6');
  });
  it('keeps exact Foundation Phase 2 sources, visual answers and canonical Atlas placements', () => {
    const spec=resolveCurriculumSpecification('mathematics',2013)!;
    for (const task of foundation2013phase2p1.cards) {
      const c=card(task.id.split('-q')[1]);
      expect(c.paperFileid).toBe('LC003BLP100EV');
      expect(c.sourceMaterial?.sourceFileid).toBe('LC003BLP100EV.pdf');
      expect(c.sourceMaterial?.pages).toEqual(task.sourcePages);
      expect(c.mathematicsScale?.schemeFileid).toBe('LC003BLP000EV.pdf');
      expect(c.mathematicsScale?.schemePages).toEqual(task.schemePages);
      expect(c.mathematicsScale?.marks).toEqual('permittedMarks' in task ? task.permittedMarks : undefined);
      expect(c.mathematicsScale?.components).toEqual('components' in task ? task.components : undefined);
      expect(findCanonicalTopic(spec,c.topicId)).toBeDefined();
      expect(c.questionFigure?.src).toMatch(/maths-2013-FL-ask-p1-(?:project-)?/);
      expect(c.figure?.src).toMatch(/maths-2013-FL-scheme-(?:project-)?p/);
      expect(c.figure?.solution).toBe(true);
      const q=task.printedParts[0].match(/^Q(\d+)/)![1];
      expect(examTopicIdsForQuestion('mathematics','foundation',2013,'main',q,'p1','ev',foundation2013phase2p1.paperFileid))
        .toEqual(expect.arrayContaining(task.examTopicIds));
    }
  });
});
describe('2013 Foundation Project Maths Phase 2 Paper 2', () => {
  const cards = FOUNDATION.filter(c => c.id.startsWith('maths-2013-fl-p2-q'));
  const card = (suffix: string) => {
    const c = cards.find(c => c.id === `maths-2013-fl-p2-q${suffix}`);
    if (!c || c.kind !== 'question') throw new Error(`Missing ${suffix}`);
    return c;
  };
  it('keeps one menu response and one freely chosen parallel pair', () => {
    expect(cards.map(c=>c.id).sort()).toEqual(foundation2013phase2p2.cards.map(c=>c.id).sort());
    expect(cards).toHaveLength(47);
    expect(cards.filter(c=>c.id.includes('-meal-'))).toHaveLength(1);
    const meal = card('3-a-meal-01');
    expect(meal.totalMarks).toBe(15);
    expect(meal.questionText).toBe('Write one three-course lunch that Sarah could select.');
    expect(meal.mathematicsScale?.practiceInstruction).toContain('one starter, one main course and one dessert');
    const parallel = foundation2013phase2p2.cards.filter(c=>c.id.includes('-q8b-c-'));
    expect(parallel).toHaveLength(1);
    expect(parallel[0].selectionChoice?.pool).toEqual(['AB and DC','AD and BC']);
    expect(foundation2013phase2p2.cards).toHaveLength(47);
    expect(foundation2013phase2p2.cards.reduce((n,c)=>n+c.totalMarks,0)).toBe(325);
    expect(foundation2013phase2p2.cards.filter(c=>!c.printedParts[0].startsWith('Q8B')).reduce((n,c)=>n+c.totalMarks,0)).toBe(300);
    expect(foundation2013phase2p2.cards.find(c=>c.id.endsWith('-q2-c'))?.printedParts).toEqual(['Q2(c)(i)','Q2(c)(ii)','Q2(c)(iii)']);
    expect(card('2-b').totalMarks).toBe(5);
    expect(card('3-c').totalMarks).toBe(5);
  });
  it('uses Paper 2 ladders and exactly seven starred units', () => {
    expect(card('1-a-i').mathematicsScale?.marks).toEqual([0,3,4,5]);
    expect(card('2-a-i').mathematicsScale?.marks).toEqual([0,4,8,10]);
    expect(card('2-b').mathematicsScale?.marks).toEqual([0,2,3,4,5]);
    expect(card('3-a-meal-01').mathematicsScale?.marks).toEqual([0,5,13,15]);
    expect(card('6-a').mathematicsScale?.marks).toEqual([0,4,8,12,15]);
    expect(card('8a-a').mathematicsScale?.marks).toEqual([0,4,8,9,10]);
    expect(card('10-a-i').mathematicsScale?.marks).toEqual([0,7,15]);
    expect(cards.filter(c=>c.kind==='question' && c.mathematicsScale?.fullCreditMinusOne).map(c=>c.id).sort())
      .toEqual(['7-b-i','7-b-ii','7-b-iii','8b-a','10-a-ii','10-b-ii','10-c'].map(s=>card(s).id).sort());
  });
  it('preserves complete original geometry and the correct Phase 2 age list', () => {
    expect(card('4-e').figure?.sourceNote).toBeUndefined();
    expect(card('3-a-meal-01').figure?.sourceNote).toContain('one starter, one main course and one dessert');
    expect(card('7-b-iii').questionFigure?.alt).toContain('|Z′Y′| = 8 cm');
    expect(card('8a-b').questionFigure?.alt).toContain('|PQ| = 7 cm');
    expect(card('8b-e').questionFigure?.alt).toContain('axial symmetry');
    expect(card('10-b-ii').questionFigure?.alt).toContain('70 m');
    expect(card('8b-e').section).toBe('A');
    expect(card('9-a').section).toBe('B');
  });
  it('retains all four additional source criteria and the measurement tasks', () => {
    const rows=(suffix: string) => card(suffix).rows.map(r=>r.verbatim).join(' ');
    expect(rows('3-b')).toContain('4 × 3 × 5 without evaluating');
    expect(rows('5-b-i')).toContain('Correct midpoint of [AC] or [BC]');
    expect(rows('8b-b')).toContain('Some relevant with work ∠DAB');
    expect(rows('10-b-i')).toContain('α = tan⁻¹(70/50) or similar');
    expect(cards.filter(c=>c.kind==='question' && c.sourceMaterial?.measurementRequired).map(c=>c.id).sort())
      .toEqual(['7-a','8a-a','8a-b','8a-c','8b-e'].map(s=>card(s).id).sort());
  });
  it('binds every card to the exact Project sources and canonical Atlas topics', () => {
    const spec=resolveCurriculumSpecification('mathematics',2013)!;
    for (const task of foundation2013phase2p2.cards) {
      const c=card(task.id.split('-q')[1]);
      expect(c.paperFileid).toBe('LC003BLP200EV');
      expect(c.sourceMaterial?.sourceFileid).toBe('LC003BLP200EV.pdf');
      expect(c.sourceMaterial?.pages).toEqual(task.sourcePages);
      expect(c.mathematicsScale?.schemeFileid).toBe('LC003BLP000EV.pdf');
      expect(c.mathematicsScale?.schemePages).toEqual(task.schemePages);
      expect(c.mathematicsScale?.marks).toEqual(task.permittedMarks);
      expect(findCanonicalTopic(spec,c.topicId)).toBeDefined();
      expect(c.questionFigure?.src).toMatch(/maths-2013-FL-ask-p2-(?:project-)?/);
      expect(c.figure?.src).toMatch(/maths-2013-FL-scheme-(?:project-)?p/);
      expect(c.figure?.solution).toBe(true);
      const q=task.printedParts[0].match(/^Q(\d+[A-Z]?)/)![1];
      expect(examTopicIdsForQuestion('mathematics','foundation',2013,'main',q,'p2','ev',foundation2013phase2p2.paperFileid))
        .toEqual(expect.arrayContaining(task.examTopicIds));
    }
  });
});

describe('2012 Higher Paper 1 — step marks and deductions', () => {
  const cards = HIGHER.filter(c => c.id.startsWith('maths-2012-hl-p1-q'));
  const card = (suffix: string) => {
    const c = cards.find(c => c.id === `maths-2012-hl-p1-q${suffix}`);
    if (!c || c.kind !== 'question' || !c.mathematicsScale?.methods) throw new Error(`Missing legacy task ${suffix}`);
    return c;
  };
  it('retains all 45 independent tasks in eight complete 50-mark questions', () => {
    expect(cards).toHaveLength(45);
    expect(cards.map(c=>c.id).sort()).toEqual(higher2012p1.cards.map(c=>c.id).sort());
    expect([1,2,3,4,5,6,7,8].map(n=>cards.filter(c=>c.id.startsWith(`maths-2012-hl-p1-q${n}-`)).length))
      .toEqual([5,6,5,5,6,7,6,5]);
    for (let n=1; n<=8; n++) expect(cards.filter(c=>c.id.startsWith(`maths-2012-hl-p1-q${n}-`))
      .reduce((sum,c)=>sum+(c.kind==='question'?c.totalMarks:0),0)).toBe(50);
    expect(higher2012p1.cards.reduce((sum,c)=>sum+c.methods[0].components.length,0)).toBe(74);
  });
  it('keeps alternative assessment methods inside their task and uses the printed attempt floors', () => {
    expect(card('1-a').mathematicsScale?.methods).toHaveLength(2);
    expect(card('1-c-i').mathematicsScale?.methods).toHaveLength(3);
    expect(card('3-c-ii').mathematicsScale?.methods).toHaveLength(4);
    for (const c of cards) {
      if (c.kind!=='question') throw new Error(c.id);
      const scale=c.mathematicsScale!;
      expect(scale.code).toBeUndefined();
      expect(scale.fullCreditMinusOne).toBe(false);
      for (const method of scale.methods!) expect(method.components.reduce((sum,s)=>sum+s.maximum,0)).toBe(c.totalMarks);
    }
    expect(card('3-b-i').mathematicsScale?.methods?.[0].components.map(s=>[s.maximum,s.attempt])).toEqual([[10,3]]);
    expect(card('7-c-iii').mathematicsScale?.methods?.[0].components.map(s=>[s.maximum,s.attempt])).toEqual([[5,0]]);
  });
  it('carries task-specific caps, first principles and the integration-constant rule', () => {
    expect(card('1-b-i').mathematicsScale?.markingNote).toContain('2 marks once only');
    expect(card('3-b-ii').mathematicsScale?.markingNote).toContain('Both quadratic equations');
    expect(card('6-b-i').mathematicsScale?.markingNote).toContain('first principles');
    expect(card('8-a').mathematicsScale?.markingNote).toContain('3-mark deduction');
    expect(card('8-b-i').mathematicsScale?.markingNote).toContain('maximum deduction for limits is 3');
  });
  it('retains matrices, prior root context and the full tangent diagram', () => {
    expect(card('3-b-ii').stem).toContain('A = [[2y, y], [x², x]]');
    expect(card('3-b-ii').stem).not.toContain('must be shown');
    for (const suffix of ['7-c-ii','7-c-iii']) {
      expect(card(suffix).stem).toContain('root between 0 and 1');
      expect(card(suffix).questionFigure?.alt).toContain('root between 0 and 1');
    }
    expect(questionCropOverrides['maths-2012-hl-p1-q8-c-ii'].regions).toHaveLength(4);
    expect(card('8-c-ii').questionFigure?.alt).toContain('two tangents and the curve');
    expect(card('7-c-iii').figure?.sourceNote).toContain('named part');
  });
  it('places every task in Atlas using the exact original booklet and canonical Mark Bank topic', () => {
    const spec=resolveCurriculumSpecification('mathematics',2012)!;
    for (const task of higher2012p1.cards) {
      const c=card(task.id.split('-q')[1]);
      expect(findCanonicalTopic(spec,c.topicId)).toBeDefined();
      expect(c.paperFileid).toBe('LC003ALP100EV');
      expect(c.sourceMaterial?.sourceFileid).toBe('LC003ALP100EV.pdf');
      expect(c.sourceMaterial?.pages).toEqual(task.sourcePages);
      expect(c.mathematicsScale?.schemeFileid).toBe('LC003ALP000EV.pdf');
      expect(c.mathematicsScale?.schemePages).toEqual(task.schemePages);
      expect(c.mathematicsScale?.methods).toEqual(task.methods);
      expect(c.questionFigure?.src).toMatch(/maths-2012-HL-ask-p1-/);
      expect(c.figure?.src).toMatch(/maths-2012-HL-scheme-p/);
      expect(c.figure?.solution).toBe(true);
      const number=task.printedParts[0].match(/^Q(\d+)/)![1];
      expect(examTopicIdsForQuestion('mathematics','higher',2012,'main',number,'p1','ev',higher2012p1.paperFileid))
        .toEqual(expect.arrayContaining(task.examTopicIds));
    }
  });
});


describe('2012 Higher Phase 1 Paper 2', () => {
  const cards=HIGHER.filter(c=>c.id.startsWith('maths-2012-hl-p2-q'));
  const card=(suffix: string) => {
    const c=cards.find(c=>c.id===`maths-2012-hl-p2-q${suffix}`);
    if (!c || c.kind!=='question' || !c.mathematicsScale) throw new Error(suffix);
    return c;
  };
  it('keeps all 29 tasks and 34 scales, including both complete geometry routes', () => {
    expect(cards).toHaveLength(29);
    expect(cards.map(c=>c.id).sort()).toEqual(higher2012p2.cards.map(c=>c.id).sort());
    expect(higher2012p2.cards.reduce((n,c)=>n+(c.components?.length ?? 1),0)).toBe(34);
    expect(higher2012p2.cards.reduce((n,c)=>n+c.totalMarks,0)).toBe(325);
    for (const [q,marks] of Object.entries(higher2012p2.printedQuestionMarks)) {
      expect(higher2012p2.cards.filter(c=>c.printedParts[0].match(/^Q(\d+[A-Z]?)/)![1]===q)
        .reduce((n,c)=>n+c.totalMarks,0)).toBe(marks);
    }
    expect(card('6b').totalMarks).toBe(25);
    expect(['6a-a-i','6a-a-ii','6a-b'].reduce((n,s)=>n+card(s).totalMarks,0)).toBe(25);
  });
  it('keeps method descriptions, circle pairs and robot components together with exact stars', () => {
    expect(card('1-a').mathematicsScale?.components?.map(c=>[c.code,c.marks])).toEqual([
      ['5B',[0,3,5]],['5B',[0,3,5]],['5B',[0,3,5]]]);
    expect(card('2-a').mathematicsScale?.components?.map(c=>c.code)).toEqual(['5B','5B']);
    expect(card('8-a').totalMarks).toBe(55);
    expect(card('8-a').mathematicsScale?.components?.map(c=>[c.id,c.code,!!c.fullCreditMinusOne]))
      .toEqual([['length-pr','10B',false],['angle-beta','20C',true],['angle-alpha','25D',true]]);
    expect(cards.filter(c=>c.kind==='question' && c.mathematicsScale?.fullCreditMinusOne).map(c=>c.id).sort())
      .toEqual(['4-b-i','4-b-ii','7-d-i','7-d-ii','7-d-iii'].map(s=>card(s).id).sort());
  });
  it('uses the six-category proof scale and preserves construction tolerances', () => {
    expect(card('6b').mathematicsScale?.code).toBe('25E');
    expect(card('6b').mathematicsScale?.marks).toEqual([0,5,10,15,20,25]);
    expect(card('6b').rows.map(r=>r.verbatim).join(' ')).toContain('Upper Middle Partial Credit');
    expect(card('6b').mathematicsScale?.schemePages).toEqual([55,56,72]);
    for (const s of ['6a-a-i','6a-a-ii']) {
      expect(card(s).sourceMaterial?.measurementRequired).toBe(true);
      expect(card(s).rows.map(r=>r.verbatim).join(' ')).toContain('tolerance of 2°');
    }
  });
  it('retains all source corrections and dependencies beside the original typeset working', () => {
    expect(card('5-b').figure?.sourceNote).toContain('20.05');
    expect(card('6b').figure?.sourceNote).toContain('∠PCR');
    expect(card('7-e').figure?.sourceNote).toContain('0.3324');
    expect(card('7-e').figure?.sourceNote).toContain('0.0224');
    expect(card('7-e').stem).toContain('145 414');
    expect(card('8-b').stem).toContain('24 cm right and 7 cm above');
    expect(card('8-d').stem).toContain('|PQ| = 20 cm and |QR| = 12 cm');
    for (const s of ['7-d-i','7-d-ii','7-d-iii']) expect(card(s).questionFigure?.alt).toContain('two decimal places');
  });
  it('binds every card to the exact paper, scheme and canonical Atlas placement', () => {
    const spec=resolveCurriculumSpecification('mathematics',2012)!;
    for (const task of higher2012p2.cards) {
      const c=card(task.id.split('-q')[1]);
      expect(findCanonicalTopic(spec,c.topicId)).toBeDefined();
      expect(c.paperFileid).toBe('LC003ALP200EV');
      expect(c.sourceMaterial?.sourceFileid).toBe('LC003ALP200EV.pdf');
      expect(c.sourceMaterial?.pages).toEqual(task.sourcePages);
      expect(c.mathematicsScale?.schemeFileid).toBe('LC003ALP000EV.pdf');
      expect(c.mathematicsScale?.schemePages).toEqual(task.schemePages);
      expect(c.questionFigure?.src).toMatch(/maths-2012-HL-ask-p2-/);
      expect(c.figure?.solution).toBe(true);
      const q=task.printedParts[0].match(/^Q(\d+[A-Z]?)/)![1];
      expect(examTopicIdsForQuestion('mathematics','higher',2012,'main',q,'p2','ev',higher2012p2.paperFileid))
        .toEqual(expect.arrayContaining(task.examTopicIds));
    }
  });
});


describe('2012 Higher Phase 3 Paper 2', () => {
  const cards=HIGHER.filter(c=>c.id.startsWith('maths-2012-hl-p2-project-q'));
  const card=(suffix: string) => {
    const c=cards.find(c=>c.id===`maths-2012-hl-p2-project-q${suffix}`);
    if (!c || c.kind!=='question' || !c.mathematicsScale) throw new Error(suffix);
    return c;
  };
  it('keeps all 29 tasks and 34 scales, including both complete geometry routes', () => {
    expect(cards).toHaveLength(29);
    expect(cards.map(c=>c.id).sort()).toEqual(higher2012project2.cards.map(c=>c.id).sort());
    expect(higher2012project2.cards.reduce((n,c)=>n+(c.components?.length ?? 1),0)).toBe(34);
    expect(higher2012project2.cards.reduce((n,c)=>n+c.totalMarks,0)).toBe(325);
    for (const [q,marks] of Object.entries(higher2012project2.printedQuestionMarks)) {
      expect(higher2012project2.cards.filter(c=>c.printedParts[0].match(/^Q(\d+[A-Z]?)/)![1]===q)
        .reduce((n,c)=>n+c.totalMarks,0)).toBe(marks);
    }
    expect(card('6b').totalMarks).toBe(25);
    expect(['6a-a-i','6a-a-ii','6a-b'].reduce((n,s)=>n+card(s).totalMarks,0)).toBe(25);
  });
  it('keeps method descriptions, circle pairs and robot components together with exact stars', () => {
    expect(card('1-a').mathematicsScale?.components?.map(c=>[c.code,c.marks])).toEqual([
      ['5B',[0,3,5]],['5B',[0,3,5]],['5B',[0,3,5]]]);
    expect(card('2-a').mathematicsScale?.components?.map(c=>c.code)).toEqual(['5B','5B']);
    expect(card('8-a').totalMarks).toBe(55);
    expect(card('8-a').mathematicsScale?.components?.map(c=>[c.id,c.code,!!c.fullCreditMinusOne]))
      .toEqual([['length-pr','10B',false],['angle-beta','20C',true],['angle-alpha','25D',true]]);
    expect(cards.filter(c=>c.kind==='question' && c.mathematicsScale?.fullCreditMinusOne).map(c=>c.id).sort())
      .toEqual(['4-b-i','4-b-ii','7-d-i','7-d-ii','7-d-iii'].map(s=>card(s).id).sort());
  });
  it('uses the six-category proof scale and preserves construction tolerances', () => {
    expect(card('6b').mathematicsScale?.code).toBe('25E');
    expect(card('6b').mathematicsScale?.marks).toEqual([0,5,10,15,20,25]);
    expect(card('6b').rows.map(r=>r.verbatim).join(' ')).toContain('Upper Middle Partial Credit');
    expect(card('6b').mathematicsScale?.schemePages).toEqual([47,48,64]);
    for (const s of ['6a-a-i','6a-a-ii']) {
      expect(card(s).sourceMaterial?.measurementRequired).toBe(true);
      expect(card(s).rows.map(r=>r.verbatim).join(' ')).toContain('tolerance of 2°');
    }
  });
  it('retains all source corrections and dependencies beside the original typeset working', () => {
    expect(card('5-b').figure?.sourceNote).toContain('20.05');
    expect(card('6b').figure?.sourceNote).toContain('∠PCR');
    expect(card('7-e').figure?.sourceNote).toContain('0.3324');
    expect(card('7-e').figure?.sourceNote).toContain('0.0224');
    expect(card('7-e').stem).toContain('145 414');
    expect(card('8-b').stem).toContain('24 cm right and 7 cm above');
    expect(card('8-d').stem).toContain('|PQ| = 20 cm and |QR| = 12 cm');
    for (const s of ['7-d-i','7-d-ii','7-d-iii']) expect(card(s).questionFigure?.alt).toContain('two decimal places');
  });
  it('binds every card to the exact paper, scheme and canonical Atlas placement', () => {
    const spec=resolveCurriculumSpecification('mathematics',2012)!;
    for (const task of higher2012project2.cards) {
      const c=card(task.id.split('-q')[1]);
      expect(findCanonicalTopic(spec,c.topicId)).toBeDefined();
      expect(c.paperFileid).toBe('LC003ALP230EV');
      expect(c.sourceMaterial?.sourceFileid).toBe('LC003ALP230EV.pdf');
      expect(c.sourceMaterial?.pages).toEqual(task.sourcePages);
      expect(c.mathematicsScale?.schemeFileid).toBe('LC003ALP030EV.pdf');
      expect(c.mathematicsScale?.schemePages).toEqual(task.schemePages);
      expect(c.questionFigure?.src).toMatch(/maths-2012-HL-ask-p2-/);
      expect(c.figure?.solution).toBe(true);
      const q=task.printedParts[0].match(/^Q(\d+[A-Z]?)/)![1];
      expect(examTopicIdsForQuestion('mathematics','higher',2012,'main',q,'p2','ev',higher2012project2.paperFileid))
        .toEqual(expect.arrayContaining(task.examTopicIds));
    }
  });
});


describe('2012 Ordinary Paper 1 — source-specific step awards', () => {
  const cards=ORDINARY.filter(c=>c.id.startsWith('maths-2012-ol-p1-q'));
  const card=(suffix: string) => {
    const c=cards.find(c=>c.id===`maths-2012-ol-p1-q${suffix}`);
    if (!c || c.kind!=='question' || !c.mathematicsScale?.methods) throw new Error(suffix);
    return c;
  };
  it('retains all 48 tasks and every 50-mark question, including 52 marking components', () => {
    expect(cards).toHaveLength(48);
    expect(cards.map(c=>c.id).sort()).toEqual(ordinary2012p1.cards.map(c=>c.id).sort());
    expect([1,2,3,4,5,6,7,8].map(n=>cards.filter(c=>c.id.startsWith(`maths-2012-ol-p1-q${n}-`)).length))
      .toEqual([5,5,6,6,6,7,6,7]);
    for (let n=1;n<=8;n++) expect(cards.filter(c=>c.id.startsWith(`maths-2012-ol-p1-q${n}-`))
      .reduce((sum,c)=>sum+c.totalMarks,0)).toBe(50);
    expect(ordinary2012p1.cards.reduce((sum,c)=>sum+c.methods[0].components.length,0)).toBe(52);
  });
  it('uses exact explicit awards without inventing modern scale codes', () => {
    expect(card('2-c-ii').mathematicsScale?.methods?.[0].components[0].permittedMarks).toEqual([0,3,10]);
    expect(card('4-c').mathematicsScale?.methods?.[0].components.map(s=>s.permittedMarks)).toEqual([[0,3,7,10],[0,3,10]]);
    expect(card('1-b-ii').mathematicsScale?.methods?.[0].components.map(s=>[s.maximum,s.attempt])).toEqual([[5,2],[5,2]]);
    expect(card('3-b-i').mathematicsScale?.methods?.[0].components.map(s=>[s.maximum,s.attempt])).toEqual([[10,3],[5,2]]);
    for (const c of cards) if (c.kind==='question') {
      expect(c.mathematicsScale?.code).toBeUndefined();
      expect(c.mathematicsScale?.fullCreditMinusOne).toBe(false);
    }
  });
  it('preserves dependencies, actual source inconsistencies and intact graph instructions', () => {
    expect(card('1-b-ii').stem).toContain('35 087');
    expect(card('8-c-iii').stem).toContain('y-intercept');
    expect(card('4-c').figure?.sourceNote).toContain('(3 + 4i)');
    expect(card('5-c-i').figure?.sourceNote).toContain('Att 2');
    expect(card('5-c-i').figure?.sourceNote).toContain('not an official correction');
    expect(card('8-b-iii').figure?.sourceNote).toBeUndefined();
    expect(questionCropOverrides['maths-2012-ol-p1-q6-b-ii'].regions.at(-1)?.x1).toBe(580);
    expect(card('6-c-iii').questionText).toContain('−2 ≤ x ≤ 2');
  });
  it('links every exact task and original booklet to canonical Mark Bank and Atlas topics', () => {
    const spec=resolveCurriculumSpecification('mathematics',2012)!;
    for (const task of ordinary2012p1.cards) {
      const c=card(task.id.split('-q')[1]);
      expect(findCanonicalTopic(spec,c.topicId)).toBeDefined();
      expect(c.sourceMaterial?.sourceFileid).toBe('LC003GLP100EV.pdf');
      expect(c.sourceMaterial?.pages).toEqual(task.sourcePages);
      expect(c.mathematicsScale?.schemeFileid).toBe('LC003GLP000EV.pdf');
      expect(c.mathematicsScale?.schemePages).toEqual(task.schemePages);
      expect(c.mathematicsScale?.methods).toEqual(task.methods);
      expect(c.questionFigure?.src).toMatch(/maths-2012-OL-ask-p1-/);
      expect(c.questionFigure?.alt).toContain(task.questionText);
      expect(c.figure?.solution).toBe(true);
      const number=task.printedParts[0].match(/^Q(\d+)/)![1];
      expect(examTopicIdsForQuestion('mathematics','ordinary',2012,'main',number,'p1','ev',ordinary2012p1.paperFileid))
        .toEqual(expect.arrayContaining(task.examTopicIds));
    }
  });
});


describe('2012 Ordinary Phase 1 Paper 2', () => {
  const cards=ORDINARY.filter(c=>c.id.startsWith('maths-2012-ol-p2-q'));
  const card=(suffix: string) => {
    const c=cards.find(c=>c.id===`maths-2012-ol-p2-q${suffix}`);
    if (!c || c.kind!=='question' || !c.mathematicsScale) throw new Error(suffix);
    return c;
  };
  it('covers all 43 tasks, both geometry alternatives and all three sections', () => {
    expect(cards).toHaveLength(43);
    expect(cards.map(c=>c.id).sort()).toEqual(ordinary2012p2.cards.map(c=>c.id).sort());
    expect(cards.reduce((n,c)=>n+c.totalMarks,0)).toBe(325);
    for (const [q,marks] of Object.entries(ordinary2012p2.printedQuestionMarks)) {
      expect(ordinary2012p2.cards.filter(c=>c.printedParts[0].match(/^Q(\d+[A-Z]?)/)![1]===q)
        .reduce((n,c)=>n+c.totalMarks,0)).toBe(marks);
    }
    expect(card('5b').totalMarks).toBe(25);
    expect(['5a-a-i','5a-a-ii','5a-b'].reduce((n,s)=>n+card(s).totalMarks,0)).toBe(25);
    expect(cards.filter(c=>c.section==='A')).toHaveLength(19);
    expect(cards.filter(c=>c.section==='B')).toHaveLength(18);
    expect(cards.filter(c=>c.section==='C')).toHaveLength(6);
  });
  it('keeps exact Ordinary ladders, ten stars, binary credit and the joint method description', () => {
    expect(card('1-a').mathematicsScale?.marks).toEqual([0,4,7,10]);
    expect(card('3-a').mathematicsScale?.marks).toEqual([0,5,10,15]);
    expect(card('3-b').totalMarks).toBe(5);
    expect(card('3-b').mathematicsScale?.marks).toEqual([0,2,5]);
    expect(card('5b').mathematicsScale?.marks).toEqual([0,8,17,25]);
    expect(card('6-b-ii').mathematicsScale?.marks).toEqual([0,5]);
    expect(cards.filter(c=>c.kind==='question' && c.mathematicsScale?.fullCreditMinusOne).map(c=>c.id).sort())
      .toEqual(['2-b-iii','7-b','7-c','7-d','8-a-i','8-a-ii','8-b-i','8-b-ii','8-c-i','8-c-ii'].map(s=>card(s).id).sort());
  });
  it('retains chart, construction, multiple-choice and dependent measurement context', () => {
    for (const s of ['5a-a-ii','5a-b','6-c-i','8-b-i']) expect(card(s).sourceMaterial?.measurementRequired).toBe(true);
    expect(card('6-c-ii').sourceMaterial?.pages).toEqual([10,12]);
    expect(card('6-c-ii').rows.map(r=>r.verbatim).join(' ')).toContain('Selects B or C.');
    expect(card('6-d-iii').stem).toContain('12 diesel and 12 petrol');
    expect(card('7-e').sourceMaterial?.pages).toEqual([14,16]);
    expect(card('8-b-i').rows.map(r=>r.verbatim).join(' ')).toContain('all correct measurements are shown in (b) (ii)');
    expect(card('8-b-ii').stem).toContain('5 mm');
    expect(card('8-c-ii').stem).toContain('21π cm³');
  });
  it('binds every card to the exact originals and its canonical Atlas placement', () => {
    const spec=resolveCurriculumSpecification('mathematics',2012)!;
    for (const task of ordinary2012p2.cards) {
      const c=card(task.id.split('-q')[1]);
      expect(findCanonicalTopic(spec,c.topicId)).toBeDefined();
      expect(c.paperFileid).toBe('LC003GLP200EV');
      expect(c.sourceMaterial?.sourceFileid).toBe('LC003GLP200EV.pdf');
      expect(c.sourceMaterial?.pages).toEqual(task.sourcePages);
      expect(c.mathematicsScale?.schemeFileid).toBe('LC003GLP000EV.pdf');
      expect(c.mathematicsScale?.schemePages).toEqual(task.schemePages);
      expect(c.questionFigure?.src).toMatch(/maths-2012-OL-ask-p2-/);
      expect(c.figure?.solution).toBe(true);
      const q=task.printedParts[0].match(/^Q(\d+[A-Z]?)/)![1];
      expect(examTopicIdsForQuestion('mathematics','ordinary',2012,'main',q,'p2','ev',ordinary2012p2.paperFileid))
        .toEqual(expect.arrayContaining(task.examTopicIds));
    }
  });
});

describe('2012 Foundation Paper 1 — complete older deduction paper', () => {
  const cards=FOUNDATION.filter(c=>c.id.startsWith('maths-2012-fl-p1-q'));
  const card=(suffix: string) => {
    const c=cards.find(c=>c.id===`maths-2012-fl-p1-q${suffix}`);
    if (!c || c.kind!=='question' || !c.mathematicsScale?.methods) throw new Error(suffix);
    return c;
  };
  it('retains all 45 tasks, all seven questions and 47 marking steps', () => {
    expect(cards).toHaveLength(45);
    expect(cards.map(c=>c.id).sort()).toEqual(foundation2012p1.cards.map(c=>c.id).sort());
    expect([1,2,3,4,5,6,7].map(n=>cards.filter(c=>c.id.startsWith(`maths-2012-fl-p1-q${n}-`)).length))
      .toEqual([10,7,6,5,7,5,5]);
    for (let n=1;n<=7;n++) expect(cards.filter(c=>c.id.startsWith(`maths-2012-fl-p1-q${n}-`))
      .reduce((sum,c)=>sum+c.totalMarks,0)).toBe(n===1?100:50);
    expect(foundation2012p1.cards.reduce((sum,c)=>sum+c.methods[0].components.length,0)).toBe(47);
  });
  it('preserves the explicit award lists and independent variable/graph components', () => {
    for (const s of ['1-v','1-ix']) expect(card(s).mathematicsScale?.methods?.[0].components[0].permittedMarks).toEqual([0,4,10]);
    expect(card('4-b').mathematicsScale?.methods?.[0].components.map(s=>[s.maximum,s.attempt])).toEqual([[15,6],[5,2]]);
    expect(card('7-graph').mathematicsScale?.methods?.[0].components.map(s=>[s.maximum,s.attempt])).toEqual([[20,8],[10,4]]);
    expect(card('3-b').mathematicsScale?.methods?.[0].components.map(s=>[s.maximum,s.attempt])).toEqual([[20,8]]);
    for (const c of cards) if (c.kind==='question') {
      expect(c.mathematicsScale?.code).toBeUndefined();
      expect(c.mathematicsScale?.fullCreditMinusOne).toBe(false);
    }
  });
  it('keeps dependent context, shared notes and the genuine source reference correction', () => {
    expect(card('2-b-iii').stem).toContain('€11·80');
    expect(card('2-b-iii').figure?.sourceNote).toContain('weekly pay from part (ii)');
    expect(card('1-v').figure?.sourceNote).toBeUndefined();
    expect(card('5-c-iii').stem).toContain('x ∈ ℤ');
    expect(card('7-graph').mathematicsScale?.markingNote).toContain('all 30 marks');
    expect(card('5-a-i').figure?.src).toEqual(card('5-a-ii').figure?.src);
    for (const s of ['7-ii','7-iii','7-iv']) expect(card(s).figure?.src).toEqual(card('7-i').figure?.src);
    for (const id of ['maths-2012-fl-p1-q6-i','maths-2012-fl-p1-q6-ii','maths-2012-fl-p1-q6-iii','maths-2012-fl-p1-q6-iv','maths-2012-fl-p1-q6-v'] as const) {
      expect(questionCropOverrides[id].regions[0].bottom).toBe(330);
    }
  });
  it('binds every card to the exact original sources and a canonical Topic Atlas placement', () => {
    const spec=resolveCurriculumSpecification('mathematics',2012)!;
    for (const task of foundation2012p1.cards) {
      const c=card(task.id.split('-q')[1]);
      expect(findCanonicalTopic(spec,c.topicId)).toBeDefined();
      expect(c.sourceMaterial?.sourceFileid).toBe('LC003BLP100EV.pdf');
      expect(c.sourceMaterial?.pages).toEqual(task.sourcePages);
      expect(c.mathematicsScale?.schemeFileid).toBe('LC003BLP000EV.pdf');
      expect(c.mathematicsScale?.schemePages).toEqual(task.schemePages);
      expect(c.mathematicsScale?.methods).toEqual(task.methods);
      expect(c.questionFigure?.src).toMatch(/maths-2012-FL-ask-p1-/);
      expect(c.figure?.solution).toBe(true);
      const q=task.printedParts[0].match(/^Q(\d+)/)![1];
      expect(examTopicIdsForQuestion('mathematics','foundation',2012,'main',q,'p1','ev',foundation2012p1.paperFileid))
        .toEqual(expect.arrayContaining(task.examTopicIds));
    }
  });
});

describe('2012 Foundation Phase 1 Paper 2', () => {
  const cards=FOUNDATION.filter(c=>c.id.startsWith('maths-2012-fl-p2-q'));
  const card=(suffix: string) => {
    const c=cards.find(c=>c.id===`maths-2012-fl-p2-q${suffix}`);
    if (!c || c.kind!=='question' || !c.mathematicsScale) throw new Error(suffix);
    return c;
  };
  it('retains every task and both geometry alternatives with correct paper and practice totals', () => {
    expect(cards).toHaveLength(38);
    expect(cards.map(c=>c.id).sort()).toEqual(foundation2012p2.cards.map(c=>c.id).sort());
    expect(cards.reduce((n,c)=>n+c.totalMarks,0)).toBe(325);
    expect(foundation2012p2.cards.reduce((n,c)=>n+(c.components?.length ?? 1),0)).toBe(39);
    for (const [q,marks] of Object.entries(foundation2012p2.printedQuestionMarks)) {
      const tasks=foundation2012p2.cards.filter(c=>c.printedParts[0].match(/^Q(\d+[A-Z]?)/)![1]===q);
      expect(tasks.reduce((n,c)=>n+c.totalMarks,0)).toBe(marks);
    }
    expect(['A','B','C'].map(s=>cards.filter(c=>c.section===s).length)).toEqual([18,11,9]);
  });
  it('keeps any two of the four triangles in one five-mark card', () => {
    const c = card('4b-c-pair-01');
    const t = foundation2012p2.cards.find(t=>t.id===c.id)!;
    expect(t.selectionChoice?.pool).toEqual(['OAB','OBC','OCD','ODA']);
    expect(t.selectionChoice?.choose).toBe(2);
    expect(c.questionText).toBe('Name two isosceles triangles in the diagram.');
    expect(c.totalMarks).toBe(5);
    expect(c.mathematicsScale?.marks).toEqual([0,3,4,5]);
    expect(c.mathematicsScale?.practiceInstruction).toContain('first triangle and the second triangle');
    expect(cards.filter(c=>c.id.includes('-pair-'))).toHaveLength(1);
  });
  it('uses the exact Foundation ladders and applies the star to only the published components', () => {
    expect(card('1-a').mathematicsScale?.marks).toEqual([0,8,12,16,20]);
    expect(card('4a-a').mathematicsScale?.marks).toEqual([0,6,9,12,15]);
    expect(card('6-a-ii').mathematicsScale?.marks).toEqual([0,15,17,20]);
    expect(card('7-c-i').totalMarks).toBe(15);
    expect(card('7-c-ii').totalMarks).toBe(5);
    expect(card('8-b-i').mathematicsScale?.components).toEqual([
      {id:'substitution',label:'Substitution',code:'20C',marks:[0,15,17,20],fullCreditMinusOne:false},
      {id:'calculation',label:'Calculation',code:'10C',marks:[0,5,7,10],fullCreditMinusOne:true},
    ]);
    expect(card('8-b-i').totalMarks).toBe(30);
    expect(card('8-b-i').mathematicsScale?.fullCreditMinusOne).toBe(false);
    expect(card('8-b-ii').mathematicsScale?.fullCreditMinusOne).toBe(false);
    expect(cards.filter(c=>c.kind==='question' && c.mathematicsScale?.fullCreditMinusOne).map(c=>c.id).sort())
      .toEqual(['6-a-ii','6-a-iii','6-b-i','6-b-ii','7-a','7-b-i','7-b-ii','7-c-i','7-c-ii','8-a-i','8-a-ii'].map(s=>card(s).id).sort());
  });
  it('preserves every dependent diagram, original measurement prompt and open explanation', () => {
    for (const s of ['4a-a','4a-b']) expect(card(s).sourceMaterial?.measurementRequired).toBe(true);
    expect(card('4a-c').stem).toContain('measure ∠RSP');
    expect(card('5-e').stem).toContain('Principal in her old school');
    expect(card('5-e').sourceMaterial?.pages).toEqual([8,9]);
    expect(card('5-f').sourceMaterial?.pages).toEqual([8,9]);
    expect(card('6-a-iii').stem).toContain('scale factor 2');
    expect(card('7-c-ii').stem).toContain('diameter 12 cm');
    expect(card('8-b-ii').sourceMaterial?.pages).toEqual([14,15]);
    expect(card('8-b-ii').stem).toContain('intervals of 9 m');
    expect(card('6-b-ii').rows.map(r=>r.verbatim).join(' ')).toContain('sin⁻¹(14/75)');
  });
  it('links every card to the exact originals and canonical Topic Atlas placement', () => {
    const spec=resolveCurriculumSpecification('mathematics',2012)!;
    for (const task of foundation2012p2.cards) {
      const c=card(task.id.split('-q')[1]);
      expect(findCanonicalTopic(spec,c.topicId)).toBeDefined();
      expect(c.sourceMaterial?.sourceFileid).toBe('LC003BLP200EV.pdf');
      expect(c.sourceMaterial?.pages).toEqual(task.sourcePages);
      expect(c.mathematicsScale?.schemeFileid).toBe('LC003BLP000EV.pdf');
      expect(c.mathematicsScale?.schemePages).toEqual(task.schemePages);
      expect(c.questionFigure?.src).toMatch(/maths-2012-FL-ask-p2-/);
      expect(c.figure?.solution).toBe(true);
      const q=task.printedParts[0].match(/^Q(\d+[A-Z]?)/)![1];
      expect(examTopicIdsForQuestion('mathematics','foundation',2012,'main',q,'p2','ev',foundation2012p2.paperFileid))
        .toEqual(expect.arrayContaining(task.examTopicIds));
    }
  });
});


describe('2012 Ordinary Phase 3 Paper 1', () => {
  const cards=ORDINARY.filter(c=>c.id.startsWith('maths-2012-ol-p1-project-q'));
  const card=(suffix: string) => {
    const c=cards.find(c=>c.id===`maths-2012-ol-p1-project-q${suffix}`);
    if (!c || c.kind!=='question' || !c.mathematicsScale) throw new Error(suffix);
    return c;
  };
  it('keeps all 35 published mark units and all 300 marks without extra choice routes', () => {
    expect(cards).toHaveLength(35);
    expect(cards.map(c=>c.id).sort()).toEqual(ordinary2012project1.cards.map(c=>c.id).sort());
    expect(cards.reduce((n,c)=>n+c.totalMarks,0)).toBe(300);
    for (const [q,marks] of Object.entries(ordinary2012project1.printedQuestionMarks)) {
      expect(ordinary2012project1.cards.filter(c=>c.printedParts[0].match(/^Q(\d+)/)![1]===q)
        .reduce((n,c)=>n+c.totalMarks,0)).toBe(marks);
    }
  });
  it('keeps required parts on their single published scales, including the unusual 25C award', () => {
    const groups=[['3-b-c-d','10C',3],['4-a-b','25D',2],['8-c','5C',2],['8-f-g','5C',2],['9-b','10C',4]] as const;
    for (const [suffix,scale,parts] of groups) {
      expect(card(suffix).mathematicsScale?.code).toBe(scale);
      expect(card(suffix).mathematicsScale?.components).toBeUndefined();
      expect(ordinary2012project1.cards.find(c=>c.id===card(suffix).id)?.printedParts).toHaveLength(parts);
    }
    expect(card('4-a-b').mathematicsScale?.marks).toEqual([0,6,13,20,25]);
    expect(card('9-a-iii').mathematicsScale?.marks).toEqual([0,8,20,25]);
    expect(card('9-a-iii').totalMarks).toBe(25);
  });
  it('restricts minus-one to the five starred tasks and retains the units and definitions conventions', () => {
    expect(cards.filter(c=>c.kind==='question' && c.mathematicsScale?.fullCreditMinusOne).map(c=>c.id).sort())
      .toEqual(['7-a','7-d','7-f','7-g','9-a-i'].map(s=>card(s).id).sort());
    expect(card('7-a').rows.map(r=>r.verbatim).join(' ')).toMatch(/units/);
    for (const s of ['7-b-i','7-b-ii','7-b-iii']) {
      expect(card(s).stem).toContain('meaning of any letters');
      expect(card(s).mathematicsScale?.marks).toEqual([0,3,5]);
    }
    for (const s of ['7-b-ii','7-b-iii']) expect(card(s).figure?.sourceNote).toMatch(/once/);
  });
  it('retains the original nomograph for measurement and the complete dependent source context', () => {
    for (const s of ['7-f','7-g']) {
      expect(card(s).sourceMaterial?.measurementRequired).toBe(true);
      expect(card(s).sourceMaterial?.pages).toContain(12);
      expect(card(s).questionFigure?.alt).toContain('BSA');
    }
    expect(card('7-g').sourceMaterial?.pages).toEqual([10,12,13]);
    expect(card('6-c').sourceMaterial?.pages).toEqual([8,9]);
    expect(card('9-b').sourceMaterial?.pages).toEqual([18,19]);
    expect(card('3-b-c-d').stem).toContain('Argand diagram');
    expect(card('8-f-g').questionText).toContain('337');
    expect(card('8-f-g').questionText).toContain('first 40');
  });
  it('binds each card to its own exact source and canonical Topic Atlas placement', () => {
    const spec=resolveCurriculumSpecification('mathematics',2012)!;
    for (const task of ordinary2012project1.cards) {
      const c=card(task.id.split('-q')[1]);
      expect(findCanonicalTopic(spec,c.topicId)).toBeDefined();
      expect(c.paperFileid).toBe('LC003GLP130EV');
      expect(c.sourceMaterial?.sourceFileid).toBe('LC003GLP130EV.pdf');
      expect(c.sourceMaterial?.pages).toEqual(task.sourcePages);
      expect(c.mathematicsScale?.schemeFileid).toBe('LC003GLP030EV.pdf');
      expect(c.mathematicsScale?.schemePages).toEqual(task.schemePages);
      expect(c.questionFigure?.src).toContain('maths-2012-OL-ask-p1-project-');
      expect(c.figure?.solution).toBe(true);
      const q=task.printedParts[0].match(/^Q(\d+)/)![1];
      expect(examTopicIdsForQuestion('mathematics','ordinary',2012,'main',q,'p1','ev',ordinary2012project1.paperFileid))
        .toEqual(expect.arrayContaining(task.examTopicIds));
    }
  });
});


describe('2012 Ordinary Phase 3 Paper 2', () => {
  const cards=ORDINARY.filter(c=>c.id.startsWith('maths-2012-ol-p2-project-q'));
  const card=(suffix: string) => {
    const c=cards.find(c=>c.id===`maths-2012-ol-p2-project-q${suffix}`);
    if (!c || c.kind!=='question' || !c.mathematicsScale) throw new Error(suffix);
    return c;
  };
  it('retains all 43 marked tasks and both 25-mark geometry routes', () => {
    expect(cards).toHaveLength(43);
    expect(cards.map(c=>c.id).sort()).toEqual(ordinary2012project2.cards.map(c=>c.id).sort());
    expect(cards.reduce((n,c)=>n+c.totalMarks,0)).toBe(325);
    for (const [q,marks] of Object.entries(ordinary2012project2.printedQuestionMarks)) {
      expect(ordinary2012project2.cards.filter(c=>c.printedParts[0].match(/^Q(\d+[AB]?)/)![1]===q)
        .reduce((n,c)=>n+c.totalMarks,0)).toBe(marks);
    }
    expect(['6a-a-i','6a-a-ii','6a-b'].reduce((n,s)=>n+card(s).totalMarks,0)).toBe(25);
    expect(card('6b').mathematicsScale?.marks).toEqual([0,8,17,25]);
  });
  it('uses the detailed Q8 allocations and explains the inconsistent summary table', () => {
    for (const [s,code,marks] of [['8-a-i','5B',5],['8-a-ii','15D',15],['8-a-iii','15D',15],['8-a-iv','5B',5],['8-a-v','10D',10]] as const) {
      expect(card(s).mathematicsScale?.code).toBe(code);
      expect(card(s).totalMarks).toBe(marks);
      expect(card(s).figure?.sourceNote).toMatch(/summary table.*differs/);
    }
    expect(card('8-a-ii').mathematicsScale?.marks).toEqual([0,4,7,11,15]);
    expect(card('6a-a-i').figure?.sourceNote).toContain('perpendicular to the radius');
  });
  it('restricts minus-one to the ten starred tasks', () => {
    expect(cards.filter(c=>c.kind==='question' && c.mathematicsScale?.fullCreditMinusOne).map(c=>c.id).sort())
      .toEqual(['2-b-iii','5-a-i','5-a-ii','5-b-i','5-b-ii','8-a-ii','8-a-iii','8-a-iv','8-b-i','8-b-ii'].map(s=>card(s).id).sort());
  });
  it('preserves this edition’s trapezoidal rule and separately practicable construction context', () => {
    expect(card('8-b-ii').questionText).toContain('trapezoidal');
    expect(card('8-b-ii').questionText).not.toContain('Simpson');
    expect(card('8-b-ii').sourceMaterial?.pages).toEqual([19]);
    expect(card('8-b-ii').rows.map(r=>r.verbatim).join(' ')).toContain('OTHERS');
    for (const s of ['6a-a-ii','6a-b','7-c-i','8-b-i']) expect(card(s).sourceMaterial?.measurementRequired).toBe(true);
    expect(card('7-b-ii').stem).toContain('quarter');
    expect(card('7-c-ii').rows.map(r=>r.verbatim).join(' ')).toContain('B or C');
    expect(card('3-b').mathematicsScale?.code).toBe('5B');
    expect(card('3-b').mathematicsScale?.components).toBeUndefined();
  });
  it('binds every card to its exact source and canonical Topic Atlas placement', () => {
    const spec=resolveCurriculumSpecification('mathematics',2012)!;
    for (const task of ordinary2012project2.cards) {
      const c=card(task.id.split('-q')[1]);
      expect(findCanonicalTopic(spec,c.topicId)).toBeDefined();
      expect(c.paperFileid).toBe('LC003GLP230EV');
      expect(c.sourceMaterial?.sourceFileid).toBe('LC003GLP230EV.pdf');
      expect(c.sourceMaterial?.pages).toEqual(task.sourcePages);
      expect(c.mathematicsScale?.schemeFileid).toBe('LC003GLP030EV.pdf');
      expect(c.mathematicsScale?.schemePages).toEqual(task.schemePages);
      expect(c.questionFigure?.src).toBeTruthy();
      expect(c.figure?.solution).toBe(true);
      const q=task.printedParts[0].match(/^Q(\d+[AB]?)/)![1];
      expect(examTopicIdsForQuestion('mathematics','ordinary',2012,'main',q,'p2','ev',ordinary2012project2.paperFileid))
        .toEqual(expect.arrayContaining(task.examTopicIds));
    }
  });
});


describe('2012 Foundation Phase 3 Paper 1', () => {
  const cards=FOUNDATION.filter(c=>c.id.startsWith('maths-2012-fl-p1-project-q'));
  const card=(suffix: string) => {
    const c=cards.find(c=>c.id===`maths-2012-fl-p1-project-q${suffix}`);
    if (!c || c.kind!=='question' || !c.mathematicsScale) throw new Error(suffix);
    return c;
  };
  it('retains all 35 printed asks in their 27 published mark units and all 300 marks', () => {
    expect(cards).toHaveLength(27);
    expect(cards.map(c=>c.id).sort()).toEqual(foundation2012project1.cards.map(c=>c.id).sort());
    expect(cards.reduce((n,c)=>n+c.totalMarks,0)).toBe(300);
    expect(foundation2012project1.cards.reduce((n,c)=>n+c.printedParts.length,0)).toBe(35);
    for (const [q,marks] of Object.entries(foundation2012project1.printedQuestionMarks)) {
      expect(foundation2012project1.cards.filter(c=>c.printedParts[0].match(/^Q(\d+)/)![1]===q)
        .reduce((n,c)=>n+c.totalMarks,0)).toBe(marks);
    }
  });
  it('keeps each joint response on its Foundation scale with no extra minus-one award', () => {
    for (const [suffix,scale,parts] of [['1','25D',3],['2-a','5C',2],['6','25D',5],['7-a-i-ii','25D',2]] as const) {
      expect(card(suffix).mathematicsScale?.code).toBe(scale);
      expect(card(suffix).mathematicsScale?.components).toBeUndefined();
      expect(foundation2012project1.cards.find(c=>c.id===card(suffix).id)?.printedParts).toHaveLength(parts);
    }
    expect(card('1').mathematicsScale?.marks).toEqual([0,15,19,22,25]);
    expect(card('2-b').mathematicsScale?.marks).toEqual([0,12,18,20]);
    expect(card('4-b').mathematicsScale?.marks).toEqual([0,7,10,13,15]);
    expect(card('7-a-iii').mathematicsScale?.marks).toEqual([0,5,8,9,10]);
    expect(cards.some(c=>c.kind==='question' && c.mathematicsScale?.fullCreditMinusOne)).toBe(false);
    expect(card('8-e').totalMarks).toBe(10);
    expect(card('8-g').totalMarks).toBe(5);
  });
  it('retains graph tolerances, correct-point credit and candidate follow-through', () => {
    const notes=(s: string)=>card(s).rows.map(r=>r.verbatim).join(' ');
    expect(notes('6')).toMatch(/±\s*0·2/);
    expect(notes('7-b-iii')).toContain('±10 000');
    expect(notes('7-b-ii')).toMatch(/not joined, award full credit/);
    for (const s of ['8-c','8-d']) {
      expect(notes(s)).toContain('±1');
      expect(notes(s)).toContain('±7');
    }
    expect(notes('3-b')).toContain('3(a)');
    expect(notes('3-c')).toContain('3(b)');
    expect(notes('7-a-iii')).toContain('7(a)(ii)');
  });
  it('retains original number lines, graphs and time-card context for dependent tasks', () => {
    for (const s of ['2-b','6','7-b-ii','7-b-iii','7-b-iv','8-a','8-c','8-d']) {
      expect(card(s).sourceMaterial?.measurementRequired).toBe(true);
    }
    expect(card('6').sourceMaterial?.pages).toEqual([8,9]);
    expect(card('7-a-iii').sourceMaterial?.pages).toEqual([10,11]);
    expect(card('7-b-iv').sourceMaterial?.pages).toEqual([12,13]);
    expect(card('8-i').sourceMaterial?.pages).toEqual([14,16]);
    expect(card('8-i').stem).toContain('Deirdre');
    expect(card('8-g').questionText).toContain('fixed fee');
  });
  it('binds every card to this exact paper and canonical Topic Atlas placement', () => {
    const spec=resolveCurriculumSpecification('mathematics',2012)!;
    for (const task of foundation2012project1.cards) {
      const c=card(task.id.split('-q')[1]);
      expect(findCanonicalTopic(spec,c.topicId)).toBeDefined();
      expect(c.paperFileid).toBe('LC003BLP130EV');
      expect(c.sourceMaterial?.sourceFileid).toBe('LC003BLP130EV.pdf');
      expect(c.sourceMaterial?.pages).toEqual(task.sourcePages);
      expect(c.mathematicsScale?.schemeFileid).toBe('LC003BLP030EV.pdf');
      expect(c.mathematicsScale?.schemePages).toEqual(task.schemePages);
      expect(c.questionFigure?.src).toContain('maths-2012-FL-ask-p1-project-');
      expect(c.figure?.solution).toBe(true);
      const q=task.printedParts[0].match(/^Q(\d+)/)![1];
      expect(examTopicIdsForQuestion('mathematics','foundation',2012,'main',q,'p1','ev',foundation2012project1.paperFileid))
        .toEqual(expect.arrayContaining(task.examTopicIds));
    }
  });
});


describe('2012 Foundation Phase 3 Paper 2', () => {
  const cards=FOUNDATION.filter(c=>c.id.startsWith('maths-2012-fl-p2-project-q'));
  const card=(suffix: string) => {
    const c=cards.find(c=>c.id===`maths-2012-fl-p2-project-q${suffix}`);
    if (!c || c.kind!=='question' || !c.mathematicsScale) throw new Error(suffix);
    return c;
  };
  it('retains all 41 printed asks in 39 mark units and both complete geometry alternatives', () => {
    expect(cards).toHaveLength(39);
    expect(cards.map(c=>c.id).sort()).toEqual(foundation2012project2.cards.map(c=>c.id).sort());
    expect(cards.reduce((n,c)=>n+c.totalMarks,0)).toBe(325);
    expect(foundation2012project2.cards.reduce((n,c)=>n+c.printedParts.length,0)).toBe(41);
    for (const [q,marks] of Object.entries(foundation2012project2.printedQuestionMarks)) {
      expect(foundation2012project2.cards.filter(c=>c.printedParts[0].match(/^Q(\d+[AB]?)/)![1]===q)
        .reduce((n,c)=>n+c.totalMarks,0)).toBe(marks);
    }
    expect(card('5').totalMarks).toBe(25);
    expect(card('5').mathematicsScale?.components).toBeUndefined();
    expect(foundation2012project2.cards.find(c=>c.id===card('5').id)?.printedParts).toEqual(['Q5(a)','Q5(b)','Q5(c)']);
    expect(cards.filter(c=>c.id.includes('-q6a-'))).toHaveLength(3);
    expect(cards.filter(c=>c.id.includes('-q6b-'))).toHaveLength(5);
  });
  it('uses Paper 2 Foundation ladders and only the six explicitly starred awards', () => {
    expect(card('1-a').mathematicsScale?.marks).toEqual([0,8,12,16,20]);
    expect(card('5').mathematicsScale?.marks).toEqual([0,15,18,22,25]);
    expect(card('6a-a').mathematicsScale?.marks).toEqual([0,6,9,12,15]);
    expect(card('8-a-ii').mathematicsScale?.marks).toEqual([0,15,17,20]);
    expect(card('8-a-iv').mathematicsScale?.marks).toEqual([0,5,7,10]);
    expect(cards.filter(c=>c.kind==='question' && c.mathematicsScale?.fullCreditMinusOne)
      .map(c=>c.id.split('-q')[1]).sort()).toEqual(['8-a-ii','8-a-iii','8-a-iv','8-b-i','8-b-ii','8-c'].sort());
    expect(card('8-a-iv').figure?.sourceNote).toContain('detailed marking notes explicitly specify 10C*');
  });
  it('labels the erroneous point substitution and retains permissive marking notes', () => {
    expect(card('5').questionText).toContain('B(6, 8)');
    expect(card('5').figure?.sourceNote).toContain('substitutes x = 2');
    expect(card('5').figure?.sourceNote).toContain('2 × 8 = 5 × 6 − 14 = 16');
    expect(card('5').figure?.sourceNote).toContain('B is on l');
    expect(card('3-a').rows.map(r=>r.verbatim).join(' ')).toContain('Accept plot without key, leaves not ordered');
    expect(card('6b-d').rows.map(r=>r.verbatim).join(' ')).toContain('∠DCO and ∠DOC');
    expect(card('8-b-ii').rows.map(r=>r.verbatim).join(' ')).toContain('α = sin⁻¹(14/75) or similar');
  });
  it('gives each required T-shirt bullet its own 5C card and distinct matching question image', () => {
    const bullets=['1','2','3'].map(n=>card('7-b-ii-'+n));
    expect(new Set(bullets.map(c=>c.questionFigure?.src)).size).toBe(3);
    for (let i=0;i<3;i++) {
      expect(bullets[i].totalMarks).toBe(5);
      expect(bullets[i].mathematicsScale?.code).toBe('5C');
      expect(bullets[i].questionFigure?.src).toContain(`q7-b-ii-${i+1}.png`);
      expect(bullets[i].stem).toContain('All combinations');
    }
    expect(bullets[0].questionText).toContain('long-sleeved, round-neck, white');
    expect(bullets[1].questionText).toContain('short-sleeved grey');
    expect(bullets[2].questionText).toContain('long-sleeved T-shirt');
    expect(bullets[0].questionFigure?.alt).toContain('long-sleeved, round-neck, white');
    expect(bullets[1].questionFigure?.alt).toContain('short-sleeved grey');
    expect(bullets[2].questionFigure?.alt).toContain('long-sleeved T-shirt');
  });
  it('carries construction, sample and enlargement context into dependent parts', () => {
    for (const s of ['4-a','6a-a','6a-b','7-a-iii','8-a-i']) expect(card(s).sourceMaterial?.measurementRequired).toBe(true);
    expect(card('6a-c').stem).toContain('measure angle RSP');
    expect(card('6b-e').stem).toContain('|AB| = 12');
    expect(card('7-a-v').sourceMaterial?.pages).toEqual([10,11]);
    expect(card('7-a-vi').stem).toContain('her old school');
    expect(card('8-a-iv').sourceMaterial?.pages).toEqual([13,14]);
    expect(card('8-b-ii').sourceMaterial?.pages).toEqual([14,15]);
    expect(card('8-c').sourceMaterial?.pages).toEqual([13,15]);
    expect(card('8-c').stem).toContain('42 cm by 28 cm');
    expect(card('8-c').questionText).toContain('adding 5%');
  });
  it('binds every card to the exact original paper and canonical Topic Atlas placement', () => {
    const spec=resolveCurriculumSpecification('mathematics',2012)!;
    for (const task of foundation2012project2.cards) {
      const c=card(task.id.split('-q')[1]);
      expect(findCanonicalTopic(spec,c.topicId)).toBeDefined();
      expect(c.paperFileid).toBe('LC003BLP230EV');
      expect(c.sourceMaterial?.sourceFileid).toBe('LC003BLP230EV.pdf');
      expect(c.sourceMaterial?.pages).toEqual(task.sourcePages);
      expect(c.mathematicsScale?.schemeFileid).toBe('LC003BLP030EV.pdf');
      expect(c.mathematicsScale?.schemePages).toEqual(task.schemePages);
      expect(c.questionFigure?.src).toContain('maths-2012-FL-ask-p2-project-');
      expect(c.figure?.solution).toBe(true);
      const q=task.printedParts[0].match(/^Q(\d+[AB]?)/)![1];
      expect(examTopicIdsForQuestion('mathematics','foundation',2012,'main',q,'p2','ev',foundation2012project2.paperFileid))
        .toEqual(expect.arrayContaining(task.examTopicIds));
    }
  });
});


describe('2011 Higher Paper 1 — complete original deduction paper', () => {
  const cards = HIGHER.filter(c => c.id.startsWith('maths-2011-hl-p1-q'));
  const card = (suffix: string) => {
    const c = cards.find(c => c.id === `maths-2011-hl-p1-q${suffix}`);
    if (!c || c.kind !== 'question' || !c.mathematicsScale?.methods) throw new Error(suffix);
    return c;
  };
  it('retains all original tasks and every mark in each of the eight questions', () => {
    expect(cards).toHaveLength(41);
    expect(cards.map(c => c.id).sort()).toEqual(higher2011p1.cards.map(c => c.id).sort());
    expect([1,2,3,4,5,6,7,8].map(n => cards.filter(c => c.id.startsWith(`maths-2011-hl-p1-q${n}-`)).length))
      .toEqual([4,6,6,5,4,7,5,4]);
    for (let n=1;n<=8;n++) expect(cards.filter(c => c.id.startsWith(`maths-2011-hl-p1-q${n}-`))
      .reduce((sum,c) => sum+(c.kind==='question'?c.totalMarks:0),0)).toBe(50);
  });
  it('preserves separate component marks, attempt floors and complete alternative methods', () => {
    expect(card('7-b-i').mathematicsScale?.methods?.[0].components.map(c => [c.label,c.maximum,c.attempt]))
      .toEqual([['dx/dt',10,3],['dy/dt',10,3]]);
    expect(card('3-c-ii').mathematicsScale?.methods?.[0].components.map(c => [c.maximum,c.attempt])).toEqual([[5,2],[5,2]]);
    for (const suffix of ['1-b-i','1-c','2-a']) expect(card(suffix).mathematicsScale?.methods).toHaveLength(2);
    for (const c of cards) {
      if (c.kind!=='question') throw new Error(c.id);
      expect(c.mathematicsScale?.fullCreditMinusOne).toBe(false);
      expect(c.mathematicsScale?.code).toBeUndefined();
      for (const m of c.mathematicsScale!.methods!) expect(m.components.reduce((n,s)=>n+s.maximum,0)).toBe(c.totalMarks);
    }
  });
  it('keeps five marks for the tangent task despite the inconsistent later note', () => {
    expect(card('6-c-ii').totalMarks).toBe(5);
    expect(card('6-c-ii').mathematicsScale?.methods?.[0].components.map(c=>[c.maximum,c.attempt])).toEqual([[5,2]]);
    expect(card('6-c-ii').figure?.sourceNote).toContain('inconsistent');
    expect(card('6-c-ii').mathematicsScale?.markingNote).toContain('does not create another 5-mark award');
  });
  it('retains the source caps and the complete graph-identification task', () => {
    expect(card('3-c-ii').mathematicsScale?.markingNote).toContain('diagonal matrix');
    expect(card('5-c').mathematicsScale?.markingNote).toContain('must be proved');
    expect(card('6-b-iii').mathematicsScale?.markingNote).toContain('attempt marks at most');
    expect(card('8-c').mathematicsScale?.markingNote).toContain('second 5 marks receive 0');
    expect(card('7-c-ii').questionFigure?.alt).toContain('why each other diagram is incorrect');
    expect(questionCropOverrides['maths-2011-hl-p1-q7-c-ii'].regions.some(r => r.page===5 && r.bottom>=614)).toBe(true);
    expect(Object.values(higher2011p1.selectionDecisions).map(d=>d.classification).sort())
      .toEqual(['alternative-method','answer-identification','given-condition','whole-examination-selection']);
  });
  it('maps every card into Atlas and preserves its exact original question and scheme sources', () => {
    const spec=resolveCurriculumSpecification('mathematics',2011)!;
    for (const task of higher2011p1.cards) {
      const c=card(task.id.split('-q')[1]);
      expect(findCanonicalTopic(spec,c.topicId)).toBeDefined();
      expect(c.paperFileid).toBe('LC003ALP100EV');
      expect(c.sourceMaterial?.sourceFileid).toBe('LC003ALP100EV.pdf');
      expect(c.sourceMaterial?.pages).toEqual(task.sourcePages);
      expect(c.mathematicsScale?.schemeFileid).toBe('LC003ALP000EV.pdf');
      expect(c.mathematicsScale?.schemePages).toEqual(task.schemePages);
      expect(c.mathematicsScale?.methods).toEqual(task.methods);
      expect(c.questionFigure?.src).toMatch(/maths-2011-HL-ask-p1-/);
      expect(c.figure?.src).toMatch(/maths-2011-HL-scheme-p/);
      expect(c.figure?.solution).toBe(true);
      const q=task.printedParts[0].match(/^Q(\d+)/)![1];
      expect(examTopicIdsForQuestion('mathematics','higher',2011,'main',q,'p1','ev',higher2011p1.paperFileid))
        .toEqual(expect.arrayContaining(task.examTopicIds));
    }
  });
});


describe('2011 Higher Paper 2 — all eleven legacy questions', () => {
  const cards = HIGHER.filter(c => c.id.startsWith('maths-2011-hl-p2-q'));
  const card = (suffix: string) => {
    const c = cards.find(c => c.id === `maths-2011-hl-p2-q${suffix}`);
    if (!c || c.kind !== 'question' || !c.mathematicsScale?.methods) throw new Error(suffix);
    return c;
  };
  it('retains every offered task, including all four optional Section B questions', () => {
    expect(cards).toHaveLength(60);
    expect(cards.map(c=>c.id).sort()).toEqual(higher2011p2.cards.map(c=>c.id).sort());
    expect(Array.from({length:11},(_,i)=>cards.filter(c=>c.id.startsWith(`maths-2011-hl-p2-q${i+1}-`)).length))
      .toEqual([4,5,5,4,5,7,8,6,5,7,4]);
    for (let n=1;n<=11;n++) {
      const tasks=cards.filter(c=>c.id.startsWith(`maths-2011-hl-p2-q${n}-`));
      expect(tasks.reduce((sum,c)=>sum+c.totalMarks,0)).toBe(50);
      expect(tasks.every(c=>c.section===(n<=7?'A':'B'))).toBe(true);
    }
    expect(Object.values(higher2011p2.selectionDecisions).map(d=>d.classification).sort())
      .toEqual(['scenario-definition','scenario-definition','whole-examination-selection','whole-examination-selection','whole-examination-selection']);
    expect(higher2011p2.selectionReview.some(r=>r.classification==='open-example-choice')).toBe(true);
  });
  it('keeps alternative methods separate from separately scoreable required components', () => {
    expect(card('1-b').mathematicsScale?.methods).toHaveLength(3);
    for (const method of card('1-b').mathematicsScale!.methods!) {
      expect(method.components.map(c=>[c.maximum,c.attempt])).toEqual([[10,3],[5,2],[5,2],[5,2]]);
    }
    for (const suffix of ['2-c-i','10-b-i','10-b-ii']) {
      expect(card(suffix).mathematicsScale?.methods?.[0].components.map(c=>[c.maximum,c.attempt]))
        .toEqual([[5,2],[5,2]]);
    }
    expect(card('3-b-i').mathematicsScale?.methods?.[0].components.map(c=>[c.maximum,c.attempt])).toEqual([[20,7]]);
    expect(card('11-b-ii').mathematicsScale?.methods?.[0].components.map(c=>[c.maximum,c.attempt])).toEqual([[5,2],[10,3]]);
    for (const c of cards) {
      if (c.kind!=='question') throw new Error(c.id);
      expect(c.mathematicsScale?.code).toBeUndefined();
      expect(c.mathematicsScale?.fullCreditMinusOne).toBe(false);
      for (const method of c.mathematicsScale!.methods!) expect(method.components.reduce((n,s)=>n+s.maximum,0)).toBe(c.totalMarks);
    }
  });
  it('retains special marking restrictions and explains errors in the original scheme', () => {
    expect(card('3-a').mathematicsScale?.markingNote).toContain('does not necessarily apply');
    expect(card('5-c-ii').mathematicsScale?.markingNote).toContain('at most attempt marks');
    expect(card('8-b-ii').mathematicsScale?.markingNote).toContain('square units');
    expect(card('8-c-ii').mathematicsScale?.markingNote).toContain('At most attempt marks (2)');
    expect(card('8-a').mathematicsScale?.markingNote).toContain('1 mark');
    expect(card('2-b-ii').figure?.sourceNote).toContain('289 + 361 = 650');
    expect(card('8-a').figure?.sourceNote).toContain('dv = sin x dx');
    expect(card('9-c-i').figure?.sourceNote).toContain('population mean 67');
    expect(card('10-b-v').figure?.sourceNote).toContain('actually established in part (iv)');
    expect(card('11-b-ii').figure?.sourceNote).toContain('(3 cos θ + 4 sin θ)²');
  });
  it('carries diagrams, complete tables and prior choices into dependent tasks', () => {
    expect(card('10-a-ii').questionFigure?.alt).toContain('row c is b,c,a');
    for (const s of ['10-b-iii','10-b-iv','10-b-v']) expect(card(s).stem).toContain('Choose x of order 3 and y of order 2');
    expect(card('7-b-iv').questionFigure?.alt).toContain('both land at P');
    expect(card('11-b-iii').stem).toContain('The preceding part establishes');
    expect(questionCropOverrides['maths-2011-hl-p2-q5-c-i'].regions.some(r=>r.page===4 && r.bottom>=425)).toBe(true);
    expect(questionCropOverrides['maths-2011-hl-p2-q7-b-iii'].regions.some(r=>r.page===5 && r.top<=150 && r.bottom>=290)).toBe(true);
  });
  it('maps every card into Atlas against the exact original paper and scheme', () => {
    const spec=resolveCurriculumSpecification('mathematics',2011)!;
    for (const task of higher2011p2.cards) {
      const c=card(task.id.split('-q')[1]);
      expect(findCanonicalTopic(spec,c.topicId)).toBeDefined();
      expect(c.paperFileid).toBe('LC003ALP200EV');
      expect(c.sourceMaterial?.sourceFileid).toBe('LC003ALP200EV.pdf');
      expect(c.sourceMaterial?.pages).toEqual(task.sourcePages);
      expect(c.mathematicsScale?.schemeFileid).toBe('LC003ALP000EV.pdf');
      expect(c.mathematicsScale?.schemePages).toEqual(task.schemePages);
      expect(c.mathematicsScale?.methods).toEqual(task.methods);
      expect(c.questionFigure?.src).toMatch(/maths-2011-HL-ask-p2-/);
      expect(c.figure?.solution).toBe(true);
      const q=task.printedParts[0].match(/^Q(\d+)/)![1];
      expect(examTopicIdsForQuestion('mathematics','higher',2011,'main',q,'p2','ev',higher2011p2.paperFileid))
        .toEqual(expect.arrayContaining(task.examTopicIds));
    }
  });
});


describe('2011 Ordinary legacy Paper 1 — all eight questions', () => {
  const cards = ORDINARY.filter(c => c.id.startsWith('maths-2011-ol-p1-q'));
  const card = (suffix: string) => {
    const c = cards.find(c => c.id === `maths-2011-ol-p1-q${suffix}`);
    if (!c || c.kind !== 'question' || !c.mathematicsScale?.methods) throw new Error(suffix);
    return c;
  };
  it('retains all 49 tasks and all 400 offered marks', () => {
    expect(cards).toHaveLength(49);
    expect(cards.map(c=>c.id).sort()).toEqual(ordinary2011p1.cards.map(c=>c.id).sort());
    expect(Array.from({length:8},(_,i)=>cards.filter(c=>c.id.startsWith(`maths-2011-ol-p1-q${i+1}-`)).length))
      .toEqual([7,7,5,7,6,6,6,5]);
    for (let n=1;n<=8;n++) expect(cards.filter(c=>c.id.startsWith(`maths-2011-ol-p1-q${n}-`)).reduce((sum,c)=>sum+c.totalMarks,0)).toBe(50);
    expect(cards.every(c=>c.section==='A')).toBe(true);
    expect(Object.values(ordinary2011p1.selectionDecisions).map(d=>d.classification).sort())
      .toEqual(['derived-answer-verification','open-method-choice','whole-examination-selection']);
    expect(card('3-c-ii').totalMarks).toBe(5);
    expect(card('3-c-ii').mathematicsScale?.markingNote).toContain('Both original examples');
  });
  it('preserves the published component allocations and attempt floors', () => {
    expect(card('2-a').mathematicsScale?.methods?.[0].components.map(c=>[c.maximum,c.attempt])).toEqual([[10,3],[5,2]]);
    expect(card('3-b-i').mathematicsScale?.methods?.[0].components.map(c=>[c.maximum,c.attempt])).toEqual([[5,2],[5,2],[5,2]]);
    for (const suffix of ['3-c-i','4-c-ii','6-c-i']) expect(card(suffix).mathematicsScale?.methods?.[0].components.map(c=>[c.maximum,c.attempt])).toEqual([[5,2],[5,2]]);
    expect(card('6-a-i').mathematicsScale?.methods?.[0].components.map(c=>[c.maximum,c.attempt])).toEqual([[10,3]]);
    expect(card('8-i').mathematicsScale?.methods?.[0].components.map(c=>[c.maximum,c.attempt])).toEqual([[15,5]]);
    for (const c of cards) {
      if(c.kind!=='question') throw new Error(c.id);
      expect(c.mathematicsScale?.code).toBeUndefined();
      expect(c.mathematicsScale?.fullCreditMinusOne).toBe(false);
      for(const method of c.mathematicsScale!.methods!) expect(method.components.reduce((n,s)=>n+s.maximum,0)).toBe(c.totalMarks);
    }
  });
  it('retains follow-through restrictions and clarifies original source errors', () => {
    expect(card('1-b-ii').mathematicsScale?.markingNote).toContain('0.88/231');
    expect(card('2-b-iii').mathematicsScale?.markingNote).toContain('both earlier parts earned zero');
    expect(card('3-c-i').mathematicsScale?.methods?.[0].components).toHaveLength(2);
    expect(card('3-c-ii').mathematicsScale?.markingNote).toContain('linear');
    expect(card('5-c-ii').mathematicsScale?.markingNote).toContain('h = −1');
    expect(card('7-c-ii').totalMarks).toBe(5);
    expect(card('8-ii').mathematicsScale?.markingNote).toContain('at most attempt three');
    expect(card('6-b-ii').figure?.sourceNote).toContain('(1.5, 3) ∪ (3, ∞)');
    expect(card('7-b-ii').figure?.sourceNote).toContain('u = x² − 2x − 9');
    expect(card('8-iv').figure?.sourceNote).toContain('[−3, −2) ∪ [−1, 1]');
  });
  it('carries complete dependent stems, graphs and tables into practice', () => {
    expect(card('2-c-iii').stem).toContain('f(0) = 6 and f(3) = 0');
    expect(card('3-b-ii').stem).toContain('x/2 = (2 − y)/5');
    expect(card('6-c-ii').questionText).toContain('P(1, 3)');
    expect(questionCropOverrides['maths-2011-ol-p1-q6-c-ii'].regions.some(r=>r.top<=724 && r.bottom>=782)).toBe(true);
    expect(questionCropOverrides['maths-2011-ol-p1-q6-a-ii'].regions.some(r=>r.top<=414 && r.bottom>=554)).toBe(true);
    expect(questionCropOverrides['maths-2011-ol-p1-q8-iv'].regions.some(r=>r.top<=216 && r.bottom>=578)).toBe(true);
    expect(card('8-iv').stem).toContain('−5 ≤ x ≤ 1');
  });
  it('maps every card into Atlas with the exact unusually named original paper', () => {
    const spec=resolveCurriculumSpecification('mathematics',2011)!;
    for(const task of ordinary2011p1.cards) {
      const c=card(task.id.split('-q')[1]);
      expect(findCanonicalTopic(spec,c.topicId)).toBeDefined();
      expect(c.paperFileid).toBe('LC003GLP000EV');
      expect(c.sourceMaterial?.sourceFileid).toBe('LC003GLP000EV.pdf');
      expect(c.sourceMaterial?.pages).toEqual(task.sourcePages);
      expect(c.mathematicsScale?.schemeFileid).toBe('LC003GLP000EV.pdf');
      expect(c.mathematicsScale?.schemePages).toEqual(task.schemePages);
      expect(c.mathematicsScale?.methods).toEqual(task.methods);
      expect(c.questionFigure?.src).toMatch(/maths-2011-OL-ask-p1-/);
      expect(c.figure?.solution).toBe(true);
      const q=task.printedParts[0].match(/^Q(\d+)/)![1];
      expect(examTopicIdsForQuestion('mathematics','ordinary',2011,'main',q,'p1','ev',ordinary2011p1.paperFileid)).toEqual(expect.arrayContaining(task.examTopicIds));
    }
  });
});


describe('2011 Ordinary legacy Paper 2 — every selectable task', () => {
  const cards = ORDINARY.filter(c => c.id.startsWith('maths-2011-ol-p2-q'));
  const card = (suffix: string) => {
    const c = cards.find(c => c.id === `maths-2011-ol-p2-q${suffix}`);
    if (!c || c.kind !== 'question' || !c.mathematicsScale?.methods) throw new Error(suffix);
    return c;
  };
  const steps = (suffix: string) => card(suffix).mathematicsScale!.methods![0].components;
  it('retains all 74 tasks, eleven questions and all 550 offered marks', () => {
    expect(cards).toHaveLength(74);
    expect(cards.map(c=>c.id).sort()).toEqual(ordinary2011p2.cards.map(c=>c.id).sort());
    expect(Array.from({length:11},(_,i)=>cards.filter(c=>c.id.startsWith(`maths-2011-ol-p2-q${i+1}-`)).length))
      .toEqual([6,7,8,7,6,10,7,5,8,6,4]);
    for (let n=1;n<=11;n++) {
      const group=cards.filter(c=>c.id.startsWith(`maths-2011-ol-p2-q${n}-`));
      expect(group.reduce((sum,c)=>sum+c.totalMarks,0)).toBe(50);
      expect(group.every(c=>c.section===(n<=7?'A':'B'))).toBe(true);
    }
    expect(Object.values(ordinary2011p2.selectionDecisions).filter(d=>d.classification==='universal-theorem')).toHaveLength(1);
  });
  it('preserves restricted awards, hit-or-miss tasks and independent component allocations', () => {
    expect(steps('1-b-i').map(c=>c.permittedMarks)).toEqual([[0,3,10],[0,2,4,5]]);
    expect(steps('1-a-ii')[0].permittedMarks).toEqual([0,4,5]);
    expect(steps('2-b-ii')[0].permittedMarks).toEqual([0,4,5]);
    for(const suffix of ['2-c-ii','3-c-iii','11-b-iii']) expect(steps(suffix)[0].permittedMarks).toEqual([0,7,9,10]);
    for(const letter of ['b','c']) for(const roman of ['i','ii','iii','iv']) expect(steps(`6-${letter}-${roman}`).map(c=>[c.maximum,c.attempt])).toEqual([[5,0]]);
    expect(steps('11-a').map(c=>c.permittedMarks)).toEqual([[0,2,4,5],[0,2,4,5],[0,2,4,5]]);
    expect(steps('11-b-i').map(c=>[c.maximum,c.attempt])).toEqual([[5,2],[5,2],[5,2]]);
    expect(steps('11-b-ii').map(c=>[c.maximum,c.attempt])).toEqual([[5,2],[5,2]]);
    for(const c of cards) {
      if(c.kind!=='question') throw new Error(c.id);
      expect(c.mathematicsScale?.fullCreditMinusOne).toBe(false);
      for(const method of c.mathematicsScale!.methods!) expect(method.components.reduce((n,s)=>n+s.maximum,0)).toBe(c.totalMarks);
    }
  });
  it('retains proof caps, prerequisite work and source-error explanations', () => {
    expect(card('3-b-iii').mathematicsScale?.markingNote).toContain('2 + 2');
    expect(card('4-b').mathematicsScale?.markingNote).toContain('capped at seven');
    expect(card('8-b').mathematicsScale?.markingNote).toContain('fourteen');
    expect(card('7-c-iii').mathematicsScale?.markingNote).toContain('If no standard deviation was found');
    expect(card('10-c-ii').mathematicsScale?.markingNote).toContain('at most three');
    expect(card('11-b-iii').mathematicsScale?.markingNote).toContain('Testing only (16,12) is capped at seven');
    expect(card('2-b-ii').figure?.sourceNote).toContain('explicit restricted award list');
    expect(card('7-c-ii').figure?.sourceNote).toContain('22.138');
    expect(card('11-b-i').mathematicsScale?.markingNote).toContain('parking space');
  });
  it('keeps shared context, data, vector notation and complete diagrams in each task', () => {
    expect(card('1-b-i').stem).toContain('0.6, 1.8, 2.7, 2.2, 2.4 and 2.0');
    expect(card('7-c-iii').stem).toContain('unequal class widths');
    expect(card('11-b-iii').stem).toContain('€40 for a small van and €50');
    expect(questionCropOverrides['maths-2011-ol-p2-q4-c-iv'].regions.some(r=>r.top<=528 && r.bottom>=593)).toBe(true);
    expect(questionCropOverrides['maths-2011-ol-p2-q5-a'].regions[0].top).toBeLessThanOrEqual(35);
    for(const roman of ['i','ii','iii']) expect(card(`9-b-${roman}`).stem).toContain('P');
  });
  it('maps every card to canonical curriculum and Atlas with exact original sources', () => {
    const spec=resolveCurriculumSpecification('mathematics',2011)!;
    for(const task of ordinary2011p2.cards) {
      const c=card(task.id.split('-q')[1]);
      expect(findCanonicalTopic(spec,c.topicId)).toBeDefined();
      expect(c.paperFileid).toBe('LC003GLP200EV');
      expect(c.sourceMaterial?.sourceFileid).toBe('LC003GLP200EV.pdf');
      expect(c.sourceMaterial?.pages).toEqual(task.sourcePages);
      expect(c.mathematicsScale?.schemeFileid).toBe('LC003GLP000EV.pdf');
      expect(c.mathematicsScale?.schemePages).toEqual(task.schemePages);
      expect(c.mathematicsScale?.methods).toEqual(task.methods);
      expect(c.questionFigure?.src).toMatch(/maths-2011-OL-ask-p2-/);
      expect(c.figure?.solution).toBe(true);
      const q=task.printedParts[0].match(/^Q(\d+)/)![1];
      expect(examTopicIdsForQuestion('mathematics','ordinary',2011,'main',q,'p2','ev',ordinary2011p2.paperFileid)).toEqual(expect.arrayContaining(task.examTopicIds));
    }
  });
});


describe('2011 Higher Project Maths Phase 2 Paper 1', () => {
  const cards = HIGHER.filter(c => c.id.startsWith('maths-2011-hl-p1-project-q'));
  const card = (suffix: string) => {
    const c = cards.find(c => c.id === `maths-2011-hl-p1-project-q${suffix}`);
    if (!c || c.kind !== 'question') throw new Error(suffix);
    return c;
  };
  it('retains 36 published marking units, 350 offered marks with freely chosen observations', () => {
    expect(cards).toHaveLength(36);
    expect(cards.map(c=>c.id).sort()).toEqual(higher2011project1.cards.map(c=>c.id).sort());
    const groups = new Map<string,number>();
    for(const task of higher2011project1.cards) groups.set(task.id,task.totalMarks);
    expect(groups.size).toBe(36);
    expect([...groups.values()].reduce((a,b)=>a+b,0)).toBe(350);
    expect(cards.reduce((n,c)=>n+c.totalMarks,0)).toBe(350);
    expect(cards.filter(c=>c.section==='A')).toHaveLength(11);
    expect(cards.filter(c=>c.section==='B')).toHaveLength(9);
    expect(cards.filter(c=>c.section==='C')).toHaveLength(16);
    expect(higher2011project1.paperPagesInspected).toHaveLength(20);
    expect(higher2011project1.schemePagesInspected).toEqual(Array.from({length:42},(_,i)=>i+1));
  });
  it('retains the two separate scales and the dependency on an unused observation', () => {
    const a = card('4-a-times-0-1');
    const b = card('4-b-times-0-1-check-2');
    expect(cards.filter(c=>c.id.includes('-times-'))).toHaveLength(2);
    expect(a.questionText).toContain('Use any two');
    expect(a.mathematicsScale?.marks).toEqual([0,9,13,15]);
    expect(b.questionText).toBe('Use a different observation from the table to verify your values for A and b.');
    expect(b.mathematicsScale?.marks).toEqual([0,3,5]);
    expect(b.mathematicsScale?.practiceInstruction).toContain('a different observation');
    expect(b.figure?.sourceNote).toContain('any permitted choice');
    expect(higher2011project1.cards.find(t=>t.id===b.id)?.selectionChoice?.dependsOn).toBe('q4-a-observations');
  });
  it('keeps shared scales grouped and retains the six-award 20E ladder', () => {
    expect(card('3-a').mathematicsScale?.marks).toEqual([0,5,10,14,17,20]);
    for(const suffix of ['2-b','4-c-d','5-d','6-d-i-ii','6-d-iii-e']) {
      expect(card(suffix).totalMarks).toBe(5);
      expect(card(suffix).mathematicsScale?.code).toBe('5C');
    }
    expect(card('5-c').mathematicsScale?.code).toBe('20D');
    expect(card('6-d-iii-e').questionText).toContain('percentage tax');
    expect(higher2011project1.cards.find(c=>c.id.endsWith('q5-c'))?.printedParts).toEqual(['Q5(c)(i)','Q5(c)(ii)']);
    expect(card('4-c-d').figure?.sourceNote).toContain('(ln 2)/b');
  });
  it('retains all Section C deduction tasks and their restrictions', () => {
    const deduction=cards.filter(c=>c.kind==='question' && c.mathematicsScale?.methods);
    expect(deduction).toHaveLength(16);
    for(const c of deduction) {
      if(c.kind!=='question') throw new Error(c.id);
      for(const m of c.mathematicsScale!.methods!) expect(m.components.reduce((n,s)=>n+s.maximum,0)).toBe(c.totalMarks);
      expect(c.mathematicsScale?.fullCreditMinusOne).toBe(false);
    }
    expect(card('7-c-ii').totalMarks).toBe(5);
    expect(card('7-c-ii').mathematicsScale?.markingNote).toContain('does not create another 5-mark award');
    expect(card('8-c-i').mathematicsScale?.markingNote).toContain('caps the simplification at 2');
    expect(card('9-c').mathematicsScale?.markingNote).toContain('second 5 marks receive 0');
    expect(card('9-a').mathematicsScale?.markingNote).toContain('integration constant');
  });
  it('maps every task into canonical curriculum and Atlas using its exact parallel edition', () => {
    const spec=resolveCurriculumSpecification('mathematics',2011)!;
    for(const task of higher2011project1.cards) {
      const c=card(task.id.split('-q')[1]);
      expect(findCanonicalTopic(spec,c.topicId)).toBeDefined();
      expect(c.paperFileid).toBe('LC003ALP130EV');
      expect(c.sourceMaterial?.sourceFileid).toBe('LC003ALP130EV.pdf');
      expect(c.sourceMaterial?.pages).toEqual(task.sourcePages);
      expect(c.mathematicsScale?.schemeFileid).toBe('LC003ALP030EV.pdf');
      expect(c.mathematicsScale?.schemePages).toEqual(task.schemePages);
      expect(c.questionFigure?.src).toMatch(/maths-2011-HL-ask-p1-project-/);
      expect(c.figure?.solution).toBe(true);
      const q=task.printedParts[0].match(/^Q(\d+)/)![1];
      expect(examTopicIdsForQuestion('mathematics','higher',2011,'main',q,'p1','ev',higher2011project1.paperFileid)).toEqual(expect.arrayContaining(task.examTopicIds));
    }
  });
});


describe('2011 Higher Project Maths Phase 2 Paper 2', () => {
  const cards = HIGHER.filter(c => c.id.startsWith('maths-2011-hl-p2-project-q'));
  const card = (suffix: string) => {
    const c = cards.find(c => c.id === `maths-2011-hl-p2-project-q${suffix}`);
    if (!c || c.kind !== 'question') throw new Error(suffix);
    return c;
  };
  it('retains all 28 tasks, both proofs and 325 offered marks at the published boundaries', () => {
    expect(cards).toHaveLength(28);
    expect(cards.map(c=>c.id).sort()).toEqual(higher2011project2.cards.map(c=>c.id).sort());
    expect(cards.reduce((n,c)=>n+c.totalMarks,0)).toBe(325);
    expect(higher2011project2.cards.reduce((n,c)=>n+(c.components?.length ?? 1),0)).toBe(32);
    for(const [q, marks] of Object.entries(higher2011project2.printedQuestionMarks)) {
      expect(higher2011project2.cards.filter(c=>c.printedParts[0].match(/^Q(\d+[A-Z]?)/)![1]===q)
        .reduce((n,c)=>n+c.totalMarks,0)).toBe(marks);
    }
    expect(card('6a').totalMarks).toBe(25);
    expect(card('6b').totalMarks).toBe(25);
    expect(higher2011project2.paperPagesInspected).toHaveLength(20);
    expect(higher2011project2.schemePagesInspected).toEqual(Array.from({length:34},(_,i)=>i+43));
  });
  it('keeps the circle and theorem components on their one complete task', () => {
    expect(card('5').mathematicsScale?.components?.map(c=>[c.code,c.marks])).toEqual([
      ['15D',[0,8,10,13,15]],['5B',[0,3,5]],['5B',[0,3,5]]]);
    expect(card('6a').mathematicsScale?.components?.map(c=>[c.code,c.marks])).toEqual([
      ['5B',[0,3,5]],['10B',[0,6,10]],['10C',[0,6,8,10]]]);
    expect(card('5').mathematicsScale?.components?.map(c=>c.label)).toEqual([
      'Intersection of line and circle','Radius and centre','Equation']);
  });
  it('uses the detailed historical ladders and does not invent starred deductions', () => {
    expect(card('4-a').mathematicsScale?.marks).toEqual([0,9,15]);
    expect(card('6b').mathematicsScale?.marks).toEqual([0,15,22,25]);
    expect(card('8-b-i').mathematicsScale?.marks).toEqual([0,15,22,25]);
    expect(card('8-a-i').mathematicsScale?.marks).toEqual([0,15,20,23,25]);
    expect(card('7-c').mathematicsScale?.marks).toEqual([0,4,5,8,10]);
    for(const c of cards) {
      if(c.kind!=='question') throw new Error(c.id);
      expect(c.mathematicsScale?.fullCreditMinusOne).toBe(false);
      expect(c.mathematicsScale?.practiceInstruction).toBeUndefined();
    }
  });
  it('preserves diagram context, open methods, interval tolerances and follow-through', () => {
    expect(card('3-c').stem).toContain('insert scales');
    expect(card('7-a-i').rows.some(r=>r.kind==='point' && r.verbatim.includes('last two intervals'))).toBe(true);
    expect(card('7-b-iii').sourceMaterial?.pages).toEqual([12,13]);
    expect(card('8-a-iii').sourceMaterial?.pages).toEqual([15,16]);
    expect(card('8-a-i').rows.some(r=>r.kind==='point' && r.verbatim.includes('floor to apex'))).toBe(true);
    expect(card('8-a-ii').rows.some(r=>r.kind==='point' && r.verbatim.includes('Accept answers from (i)'))).toBe(true);
    expect(card('7-b-iii').figure?.sourceNote).toContain('310 to 210');
    expect(card('6b').figure?.sourceNote).toContain('Q₃ to Q₂');
  });
  it('explains the source errors and checks the original statistics data independently', () => {
    expect(card('1-a').figure?.sourceNote).toContain('(26 − 20)/5 = 1.2');
    expect(card('7-c').figure?.sourceNote).toContain('|OD|, not |OE|');
    const observations=[24,20,22,15,70,15,16,15,16,15,18,16,21,21,73,16,20,12,18,20,18,18,14,22,18];
    const corrected=observations.map(x=>x===70?20:x===73?17:x);
    const withoutOutliers=observations.filter(x=>x!==70 && x!==73);
    expect(corrected.reduce((a,b)=>a+b,0)/25).toBe(17.88);
    expect(withoutOutliers.reduce((a,b)=>a+b,0)/23).toBeCloseTo(17.83,2);
    for(const estimate of [17.88,17.83]) expect(observations.filter(x=>Math.abs(x-estimate)<=2)).toHaveLength(9);
    expect(observations.filter(x=>Math.abs(x-18)<=2)).toHaveLength(12);
    expect(card('8-b-ii').figure?.sourceNote).toContain('9/25 = 0.36');
    expect(card('8-b-ii').figure?.sourceNote).toContain('not to reject');
  });
  it('places every task in canonical Mark Bank and Atlas topics with exact-edition provenance', () => {
    const spec=resolveCurriculumSpecification('mathematics',2011)!;
    for(const task of higher2011project2.cards) {
      const c=card(task.id.split('-q')[1]);
      expect(findCanonicalTopic(spec,c.topicId)).toBeDefined();
      expect(c.topicId).toBe(task.topicId);
      expect(c.paperFileid).toBe('LC003ALP230EV');
      expect(c.sourceMaterial?.sourceFileid).toBe('LC003ALP230EV.pdf');
      expect(c.sourceMaterial?.pages).toEqual(task.sourcePages);
      expect(c.mathematicsScale?.schemeFileid).toBe('LC003ALP030EV.pdf');
      expect(c.mathematicsScale?.schemePages).toEqual(task.schemePages);
      expect(c.questionFigure?.src).toMatch(/maths-2011-HL-ask-p2-project-/);
      expect(c.figure?.solution).toBe(true);
      const q=task.printedParts[0].match(/^Q(\d+[A-Z]?)/)![1];
      expect(examTopicIdsForQuestion('mathematics','higher',2011,'main',q,'p2','ev',higher2011project2.paperFileid))
        .toEqual(expect.arrayContaining(task.examTopicIds));
    }
  });
});


describe('2011 Ordinary Project Maths Phase 2 Paper 1', () => {
  const cards = ORDINARY.filter(c => c.id.startsWith('maths-2011-ol-p1-project-q'));
  const card = (suffix: string) => {
    const c = cards.find(c => c.id === `maths-2011-ol-p1-project-q${suffix}`);
    if (!c || c.kind !== 'question') throw new Error(suffix);
    return c;
  };
  it('retains all 43 complete tasks and 350 offered marks at published boundaries', () => {
    expect(cards).toHaveLength(43);
    expect(cards.map(c=>c.id).sort()).toEqual(ordinary2011project1.cards.map(c=>c.id).sort());
    expect(cards.reduce((n,c)=>n+c.totalMarks,0)).toBe(350);
    for(const [q, marks] of Object.entries(ordinary2011project1.printedQuestionMarks)) {
      expect(ordinary2011project1.cards.filter(c=>c.printedParts[0].match(/^Q(\d+)/)![1]===q)
        .reduce((n,c)=>n+c.totalMarks,0)).toBe(marks);
    }
    expect(ordinary2011project1.paperPagesInspected).toHaveLength(20);
    expect(ordinary2011project1.schemePagesInspected).toEqual(Array.from({length:42},(_,i)=>i+1));
    expect(card('5-d-e-f').totalMarks).toBe(5);
    expect(ordinary2011project1.cards.find(c=>c.id.endsWith('q5-d-e-f'))?.printedParts)
      .toEqual(['Q5(d)','Q5(e)','Q5(f)']);
    expect(card('5-d-e-f').mathematicsScale?.marks).toEqual([0,3,4,5]);
  });
  it('uses Ordinary Level ladders and applies the starred deduction only where published', () => {
    expect(card('2-a').mathematicsScale?.marks).toEqual([0,8,13,15]);
    expect(card('4-a').mathematicsScale?.marks).toEqual([0,7,10,13,15]);
    expect(card('6-b').mathematicsScale?.marks).toEqual([0,5,8,10]);
    expect(card('6-c').mathematicsScale?.marks).toEqual([0,5]);
    expect(cards.filter(c=>c.kind==='question' && c.mathematicsScale?.fullCreditMinusOne)
      .map(c=>c.id.split('-q')[1]).sort()).toEqual(['1-c','6-c','6-d','6-g']);
    expect(card('5-a-iv').mathematicsScale?.markingNote).toContain('at least two points');
    expect(card('6-c').rows.some(r=>r.kind==='point' && r.verbatim.includes('69 km to 72 km'))).toBe(true);
    expect(card('6-d').rows.some(r=>r.kind==='point' && r.verbatim.includes('24 seconds to 28 seconds'))).toBe(true);
  });
  it('keeps two tangent steps inside one deduction task and retains all 17 older-style tasks', () => {
    expect(cards.filter(c=>c.kind==='question' && c.mathematicsScale?.methods)).toHaveLength(17);
    const steps=card('7-c-i').mathematicsScale?.methods?.[0].components;
    expect(steps?.map(c=>[c.maximum,c.attempt])).toEqual([[5,2],[5,2]]);
    expect(card('7-c-i').mathematicsScale?.markingNote).toContain('four total');
    expect(card('9-i').totalMarks).toBe(15);
    expect(card('9-ii').mathematicsScale?.markingNote).toContain('at most attempt three');
  });
  it('explains source errors and independently checks the corrected maths and graph domains', () => {
    expect(card('7-b-ii').figure?.sourceNote).toContain('dv/dx = 2x − 3');
    expect(card('7-b-ii').figure?.sourceNote).toContain('(1.5, 3) ∪ (3, ∞)');
    const derivative=(x:number)=>-(2*x-3)/(x*x-3*x)**2;
    for(const x of [1.6,2,2.9,3.1,10]) expect(derivative(x)).toBeLessThan(0);
    for(const x of [-2,0.5,1]) expect(derivative(x)).toBeGreaterThan(0);
    expect(card('8-b-ii').figure?.sourceNote).toContain('u = x² − 2x − 9');
    const x=-2;
    expect(4*(x*x-2*x-9)**3*(2*x-2)).toBe(24);
    expect(card('9-iv').figure?.sourceNote).toContain('[−3, −2) ∪ [−1, 1]');
    for(let i=-50;i<=10;i++) {
      const x=i/10;if(x===-2) continue;
      expect(1/(x+2)<=x+2).toBe((x>=-3 && x<-2)||(x>=-1 && x<=1));
    }
    expect(45+0.7*26-26**2/200).toBeCloseTo(59.82,2);
  });
  it('places every task in Mark Bank and Topic Atlas with original edition-specific sources', () => {
    const spec=resolveCurriculumSpecification('mathematics',2011)!;
    for(const task of ordinary2011project1.cards) {
      const c=card(task.id.split('-q')[1]);
      expect(findCanonicalTopic(spec,c.topicId)).toBeDefined();
      expect(c.topicId).toBe(task.topicId);
      expect(c.paperFileid).toBe('LC003GLP130EV');
      expect(c.sourceMaterial?.sourceFileid).toBe('LC003GLP130EV.pdf');
      expect(c.sourceMaterial?.pages).toEqual(task.sourcePages);
      const marking=c.mathematicsScale;
      expect(marking?.schemeFileid).toBe('LC003GLP030EV.pdf');
      expect(marking?.schemePages).toEqual(task.schemePages);
      expect(c.questionFigure?.src).toMatch(/maths-2011-OL-ask-p1-project-/);
      expect(c.figure?.solution).toBe(true);
      const q=task.printedParts[0].match(/^Q(\d+)/)![1];
      expect(examTopicIdsForQuestion('mathematics','ordinary',2011,'main',q,'p1','ev',ordinary2011project1.paperFileid))
        .toEqual(expect.arrayContaining(task.examTopicIds));
    }
  });
});


describe('2011 Ordinary Project Maths Phase 2 Paper 2', () => {
  const cards=ORDINARY.filter(c=>c.id.startsWith('maths-2011-ol-p2-project-q'));
  const card=(suffix:string)=> {
    const c=cards.find(c=>c.id===`maths-2011-ol-p2-project-q${suffix}`);
    if(!c || c.kind!=='question') throw new Error(suffix);
    return c;
  };
  it('retains every published task, both Question 6 routes and the holistic response boundaries', () => {
    expect(cards).toHaveLength(37);
    expect(cards.map(c=>c.id).sort()).toEqual(ordinary2011project2.cards.map(c=>c.id).sort());
    expect(cards.reduce((n,c)=>n+c.totalMarks,0)).toBe(325);
    for(const [q,marks] of Object.entries(ordinary2011project2.printedQuestionMarks)) {
      expect(ordinary2011project2.cards.filter(c=>c.printedParts[0].match(/^Q(\d+[A-Z]?)/)![1]===q)
        .reduce((n,c)=>n+c.totalMarks,0)).toBe(marks);
    }
    expect(ordinary2011project2.paperPagesInspected).toHaveLength(20);
    expect(ordinary2011project2.schemePagesInspected).toEqual(Array.from({length:34},(_,i)=>i+43));
    expect(cards.filter(c=>c.id.includes('-q6')).map(c=>c.totalMarks)).toEqual([15,10,25]);
    expect(card('2-c').questionText).toContain('outside');
    expect(card('2-c').totalMarks).toBe(5);
    expect(card('4-d').totalMarks).toBe(5);
    expect(cards.filter(c=>c.id.includes('-q7-b'))).toHaveLength(1);
    expect(card('7-b').questionText).toContain('Conor, Fiona and Ray');
    expect(card('7-b').totalMarks).toBe(5);
    expect(card('5-a-i').totalMarks).toBe(10);
    expect(card('5-a-ii').totalMarks).toBe(5);
  });
  it('uses the published Ordinary ladders, including the detailed-note star omitted by the summary', () => {
    expect(card('1-a').mathematicsScale?.marks).toEqual([0,7,10,13,15]);
    expect(card('4-a').mathematicsScale?.marks).toEqual([0,6,10]);
    expect(card('6b').mathematicsScale?.marks).toEqual([0,8,20,25]);
    expect(card('8-b').mathematicsScale?.marks).toEqual([0,10,18,20]);
    expect(cards.filter(c=>c.kind==='question' && c.mathematicsScale?.fullCreditMinusOne)
      .map(c=>c.id.split('-q')[1]).sort()).toEqual(['5-a-i','5-a-ii','7-a-iii','7-b','8-b','8-e','8-f']);
    expect(card('7-b').figure?.sourceNote).toContain('summary on page 62 omits the star');
    expect(card('2-d').mathematicsScale?.marks).toEqual([0,3,4,5]);
    expect(card('2-d').figure?.sourceNote).toContain('radius 3 and a circle of radius 5');
  });
  it('carries the original diagrams, dependent data and exceptional marking allowances', () => {
    expect(card('6a-a').sourceMaterial?.measurementRequired).toBe(true);
    expect(card('6a-a').sourceMaterial?.pages).toEqual([8]);
    for(const suffix of ['7-a-i','7-a-ii','7-a-iii','7-b','7-c','7-d']) {
      const override=questionCropOverrides[`maths-2011-ol-p2-project-q${suffix}` as keyof typeof questionCropOverrides];
      if(!('regions' in override)) throw new Error(`Missing original census table for ${suffix}`);
      const regions=override.regions;
      expect(regions.some(r=>r.page===10 && r.top<=159 && r.bottom>=356)).toBe(true);
    }
    for(const suffix of ['7-e-i','7-e-ii','7-e-iii','7-e-iv']) {
      expect(card(suffix).sourceMaterial?.pages).toContain(12);
      expect(card(suffix).stem).toContain('percentages of households');
    }
    expect(card('7-a-iii').rows.some(r=>r.kind==='point' && r.verbatim.includes('2·8 with no work'))).toBe(true);
    expect(card('7-c').rows.some(r=>r.kind==='point' && r.verbatim.includes('correct answer with no work'))).toBe(true);
    expect(card('8-f').rows.some(r=>r.kind==='point' && r.verbatim.includes('candidate’s answer from part (b)'))).toBe(true);
    expect(card('7-e-i').figure?.sourceNote).toContain('does not establish');
  });
  it('checks the census calculations, geometric correction and mass independently', () => {
    const frequencies=[326134,413786,264438,243303,136979,54618,15141,5050,1719,1128];
    const households=frequencies.reduce((a,b)=>a+b,0);
    const people=frequencies.reduce((a,b,i)=>a+b*(i+1),0);
    expect(households).toBe(1462296);
    expect(people).toBe(4105973);
    expect((people/households).toFixed(1)).toBe('2.8');
    expect((frequencies[6]+frequencies[7])/households).toBeCloseTo(0.0138,4);
    expect(1000*frequencies[3]/households).toBeCloseTo(166.38,2);
    expect(81000*0.2*4).toBe(64800);
    expect(3*0.17).toBeGreaterThan(0.29);
    const height=70*Math.sin(Math.PI/3);
    expect(height).toBeCloseTo(35*Math.sqrt(3),12);
    expect(height.toFixed(1)).toBe('60.6');
    expect(((140+70)/2*height*1.6*0.75/1000+6).toFixed(1)).toBe('13.6');
    expect(card('8-b').figure?.sourceNote).toContain('35√3');
    expect(card('8-b').figure?.sourceNote).toContain('not 70√3');
  });
  it('places every Mark Bank task in Topic Atlas with the matching paper edition', () => {
    const spec=resolveCurriculumSpecification('mathematics',2011)!;
    for(const task of ordinary2011project2.cards) {
      const c=card(task.id.split('-q')[1]);
      expect(findCanonicalTopic(spec,c.topicId)).toBeDefined();
      expect(c.topicId).toBe(task.topicId);
      expect(c.paperFileid).toBe('LC003GLP230EV');
      expect(c.sourceMaterial?.sourceFileid).toBe('LC003GLP230EV.pdf');
      expect(c.sourceMaterial?.pages).toEqual(task.sourcePages);
      expect(c.mathematicsScale?.schemeFileid).toBe('LC003GLP030EV.pdf');
      expect(c.mathematicsScale?.schemePages).toEqual(task.schemePages);
      expect(c.questionFigure?.src).toMatch(/maths-2011-OL-ask-p2-project-/);
      expect(c.figure?.solution).toBe(true);
      const q=task.printedParts[0].match(/^Q(\d+[A-Z]?)/)![1];
      expect(examTopicIdsForQuestion('mathematics','ordinary',2011,'main',q,'p2','ev',ordinary2011project2.paperFileid))
        .toEqual(expect.arrayContaining(task.examTopicIds));
    }
  });
});

describe('2011 Foundation legacy Paper 1 — complete original deduction paper', () => {
  const cards=FOUNDATION.filter(c=>c.id.startsWith('maths-2011-fl-p1-q'));
  const card=(suffix: string) => {
    const c=cards.find(c=>c.id===`maths-2011-fl-p1-q${suffix}`);
    if (!c || c.kind!=='question' || !c.mathematicsScale?.methods) throw new Error(suffix);
    return c;
  };
  it('retains all 46 tasks, seven questions, 400 offered marks and 48 marking components', () => {
    expect(cards).toHaveLength(46);
    expect(cards.map(c=>c.id).sort()).toEqual(foundation2011p1.cards.map(c=>c.id).sort());
    expect([1,2,3,4,5,6,7].map(n=>cards.filter(c=>c.id.startsWith(`maths-2011-fl-p1-q${n}-`)).length))
      .toEqual([10,8,6,5,7,5,5]);
    for (let n=1;n<=7;n++) expect(cards.filter(c=>c.id.startsWith(`maths-2011-fl-p1-q${n}-`))
      .reduce((sum,c)=>sum+c.totalMarks,0)).toBe(n===1?100:50);
    expect(foundation2011p1.cards.reduce((sum,c)=>sum+c.methods[0].components.length,0)).toBe(48);
    expect(foundation2011p1.paperPagesInspected).toEqual([1,2,3,4,5,6,7,8]);
    expect(foundation2011p1.schemePagesInspected).toEqual(Array.from({length:38},(_,i)=>i+1));
  });
  it('preserves the five restricted award lists and the source-conflict attempt decision', () => {
    for (const s of ['1-ix','1-x']) expect(card(s).mathematicsScale?.methods?.[0].components[0].permittedMarks).toEqual([0,4,10]);
    for (const s of ['2-c-iii','3-c-i','5-c-ii']) {
      const step=card(s).mathematicsScale?.methods?.[0].components[0];
      expect(step?.permittedMarks).toEqual([0,10]);
      expect(step?.attempt).toBe(0);
    }
    expect(card('5-c-i').mathematicsScale?.methods?.[0].components[0].attempt).toBe(2);
    expect(card('5-c-i').figure?.sourceNote).toContain('Attempts (4 marks)');
    expect(card('5-c-i').figure?.sourceNote).toContain('2-mark attempt');
    for (const c of cards) if (c.kind==='question') {
      expect(c.mathematicsScale?.code).toBeUndefined();
      expect(c.mathematicsScale?.fullCreditMinusOne).toBe(false);
    }
  });
  it('keeps the simultaneous-equation and graph steps within their published task tariffs', () => {
    expect(card('4-b').totalMarks).toBe(20);
    expect(card('4-b').mathematicsScale?.methods?.[0].components.map(s=>[s.maximum,s.attempt])).toEqual([[15,6],[5,2]]);
    expect(card('4-b').mathematicsScale?.markingNote).toContain('6 + 2 only');
    expect(card('7-graph').totalMarks).toBe(30);
    expect(card('7-graph').mathematicsScale?.methods?.[0].components.map(s=>[s.maximum,s.attempt])).toEqual([[20,8],[10,4]]);
    expect(card('7-graph').mathematicsScale?.markingNote).toContain('all 30 marks');
    expect(card('3-c-ii').mathematicsScale?.methods).toHaveLength(1);
    expect(card('3-c-ii').totalMarks).toBe(15);
    expect(card('3-c-ii').mathematicsScale?.markingNote).toContain('alternative methods');
  });
  it('retains complete required lists and marks each shared panel only for its named task', () => {
    for (const s of ['5-a-i','5-a-ii']) expect(card(s).mathematicsScale?.markingNote).toContain('All listed numbers are required');
    for (const s of ['5-b-i','5-b-ii']) expect(card(s).mathematicsScale?.markingNote).toContain('Both roots are required');
    expect(card('5-c-iii').mathematicsScale?.markingNote).toContain('All seven integers are required');
    expect(card('6-iii').mathematicsScale?.markingNote).toContain('Both days are required');
    expect(card('2-a-i').figure?.src).toBe(card('2-a-ii').figure?.src);
    expect(card('5-a-i').figure?.src).toBe(card('5-a-ii').figure?.src);
    expect(card('3-c-i').questionFigure?.src).toBe(card('3-c-ii').questionFigure?.src);
    for (const s of ['4-c-ii','4-c-iii']) expect(card(s).questionFigure?.src).toBe(card('4-c-i').questionFigure?.src);
    expect(card('5-b-i').mathematicsScale?.markingNote).toContain('does not add marks');
  });
  it('keeps the original graph and graph-reading tolerances with all four read-off tasks', () => {
    for (const s of ['7-i','7-ii','7-iii','7-iv']) {
      expect(card(s).figure?.src).toBe(card('7-i').figure?.src);
      expect(card(s).mathematicsScale?.schemePages).toEqual([34,35]);
      expect(card(s).mathematicsScale?.markingNote).toContain('±0·3 on x and ±0·5 on y');
      expect(card(s).mathematicsScale?.markingNote).toContain('named five-mark read-off');
    }
    expect(card('7-iii').mathematicsScale?.markingNote).toContain('algebra alone earns only the 2 attempt marks');
    for (const s of ['i','ii','iii','iv','v'] as const) {
      const id=`maths-2011-fl-p1-q6-${s}` as const;
      const regions=questionCropOverrides[id].regions;
      expect(regions[0].page).toBe(5);
      expect(regions[0].bottom-regions[0].top).toBeGreaterThan(220);
    }
  });
  it('binds every task to Paper 1 despite the source component 000 and places it in Topic Atlas', () => {
    const spec=resolveCurriculumSpecification('mathematics',2011)!;
    for (const task of foundation2011p1.cards) {
      const c=card(task.id.split('-q')[1]);
      expect(findCanonicalTopic(spec,c.topicId)).toBeDefined();
      expect(c.paperFileid).toBe('LC003BLP000EV');
      expect(c.questionRef).toMatch(/^2011 FL Paper 1 /);
      expect(c.sourceMaterial?.sourceFileid).toBe('LC003BLP000EV.pdf');
      expect(c.sourceMaterial?.pages).toEqual(task.sourcePages);
      expect(c.mathematicsScale?.schemeFileid).toBe('LC003BLP000EV.pdf');
      expect(c.mathematicsScale?.schemePages).toEqual(task.schemePages);
      expect(c.mathematicsScale?.methods).toEqual(task.methods);
      expect(c.questionFigure?.src).toMatch(/maths-2011-FL-ask-p1-/);
      expect(c.figure?.solution).toBe(true);
      const q=task.printedParts[0].match(/^Q(\d+)/)![1];
      expect(examTopicIdsForQuestion('mathematics','foundation',2011,'main',q,'p1','ev',foundation2011p1.paperFileid))
        .toEqual(expect.arrayContaining(task.examTopicIds));
    }
  });
});

describe('2011 Foundation legacy Paper 2 — all geometry, probability and statistics tasks', () => {
  const cards=FOUNDATION.filter(c=>c.id.startsWith('maths-2011-fl-p2-q'));
  const card=(suffix: string) => {
    const c=cards.find(c=>c.id===`maths-2011-fl-p2-q${suffix}`);
    if (!c || c.kind!=='question' || !c.mathematicsScale?.methods) throw new Error(suffix);
    return c;
  };
  it('retains all eight offered questions and their 49 tasks despite the six-question exam choice', () => {
    expect(cards).toHaveLength(49);
    expect(cards.map(c=>c.id).sort()).toEqual(foundation2011p2.cards.map(c=>c.id).sort());
    expect([1,2,3,4,5,6,7,8].map(n=>cards.filter(c=>c.id.startsWith(`maths-2011-fl-p2-q${n}-`)).length))
      .toEqual([3,4,8,7,5,9,7,6]);
    for (let n=1;n<=8;n++) expect(cards.filter(c=>c.id.startsWith(`maths-2011-fl-p2-q${n}-`))
      .reduce((sum,c)=>sum+c.totalMarks,0)).toBe(50);
    expect(foundation2011p2.cards.reduce((sum,c)=>sum+c.methods[0].components.length,0)).toBe(50);
    expect(foundation2011p2.paperPagesInspected).toEqual([1,2,3,4,5,6,7,8]);
    expect(foundation2011p2.schemePagesInspected).toEqual(Array.from({length:24},(_,i)=>i+37));
    expect(Object.values(foundation2011p2.selectionDecisions).map(d=>d.classification)).toEqual(['whole-examination-selection']);
  });
  it('keeps the two required angles together with independent five-mark awards', () => {
    expect(card('3-a').totalMarks).toBe(10);
    expect(card('3-a').mathematicsScale?.methods?.[0].components.map(c=>[c.maximum,c.attempt])).toEqual([[5,2],[5,2]]);
    expect(card('3-a').mathematicsScale?.markingNote).toContain('Both angles are required');
    expect(card('4-b-i').totalMarks).toBe(10);
    expect(card('4-b-i').mathematicsScale?.markingNote).toContain('Both points must be plotted');
    for (const c of cards) if (c.kind==='question') {
      expect(c.mathematicsScale?.code).toBeUndefined();
      expect(c.mathematicsScale?.fullCreditMinusOne).toBe(false);
    }
  });
  it('retains the unusual Simpson, mean and standard-deviation tariffs', () => {
    for (const [s,max,attempt] of [['1-b-i',35,14],['1-b-ii',5,2],['7-c-i',15,6],['7-c-ii',5,2]] as const) {
      expect(card(s).totalMarks).toBe(max);
      expect(card(s).mathematicsScale?.methods?.[0].components[0]).toMatchObject({maximum:max,attempt});
    }
    expect(card('1-b-i').figure?.src).toBe(card('1-b-ii').figure?.src);
    expect(card('7-c-i').figure?.src).toBe(card('7-c-ii').figure?.src);
    expect(card('2-b').mathematicsScale?.methods).toHaveLength(1);
    expect(card('2-b').mathematicsScale?.markingNote).toContain('alternatives for the same ten marks');
  });
  it('keeps shared probability penalties within each five-mark card and preserves all table data', () => {
    for (const part of ['b','c'] as const) for (const roman of ['i','ii','iii','iv'] as const) {
      const c=card(`6-${part}-${roman}`);
      expect(c.totalMarks).toBe(5);
      expect(c.mathematicsScale?.methods?.[0].components[0]).toMatchObject({maximum:5,attempt:2});
      expect(c.mathematicsScale?.markingNote).toContain('17-mark examples apply to all four answers together');
      expect(c.mathematicsScale?.markingNote).toContain('sample-space error once only');
      expect(c.figure?.src).toBe(card(`6-${part}-i`).figure?.src);
    }
    for (const roman of ['i','ii','iii','iv'] as const) {
      const regions=questionCropOverrides[`maths-2011-fl-p2-q6-c-${roman}`].regions;
      expect(regions[0]).toMatchObject({page:5,top:604,bottom:714});
      expect(card(`6-c-${roman}`).stem).toContain('boys aged 16, 17, 18: 11, 12, 4; girls aged 16, 17, 18: 15, 13, 5');
    }
  });
  it('retains the full frequency curve, published construction tolerances and source correction', () => {
    for (const roman of ['i','ii','iii','iv']) {
      expect(card(`7-b-${roman}`).figure?.src).toBe(card('7-b-i').figure?.src);
      expect(card(`7-b-${roman}`).mathematicsScale?.schemePages).toEqual([52,53]);
      expect(card(`7-b-${roman}`).mathematicsScale?.markingNote).toContain('13 emails for the median and 6 students above 18');
    }
    expect(card('8-a').mathematicsScale?.markingNote).toContain('±5° for angles and ±1 cm');
    for (const s of ['8-b-i','8-b-ii']) expect(card(s).mathematicsScale?.methods?.[0].components[0]).toMatchObject({maximum:10,attempt:4});
    expect(Math.acos(8/17)*180/Math.PI).toBeCloseTo(61.93,2);
    for (const s of ['5-a-i','5-a-ii']) {
      expect(card(s).figure?.sourceNote).toContain('61.93°');
      expect(card(s).figure?.sourceNote).toContain('fraction 8/17');
    }
    expect(card('5-b').mathematicsScale?.markingNote).toContain('Measuring the printed diagram earns attempt marks only');
  });
  it('binds every card to exact source pages, canonical curriculum and Topic Atlas', () => {
    const spec=resolveCurriculumSpecification('mathematics',2011)!;
    for (const task of foundation2011p2.cards) {
      const c=card(task.id.split('-q')[1]);
      expect(findCanonicalTopic(spec,c.topicId)).toBeDefined();
      expect(c.paperFileid).toBe('LC003BLP200EV');
      expect(c.questionRef).toMatch(/^2011 FL Paper 2 /);
      expect(c.sourceMaterial?.sourceFileid).toBe('LC003BLP200EV.pdf');
      expect(c.sourceMaterial?.pages).toEqual(task.sourcePages);
      expect(c.mathematicsScale?.schemeFileid).toBe('LC003BLP000EV.pdf');
      expect(c.mathematicsScale?.schemePages).toEqual(task.schemePages);
      expect(c.mathematicsScale?.methods).toEqual(task.methods);
      expect(c.questionFigure?.src).toMatch(/maths-2011-FL-ask-p2-/);
      expect(c.figure?.solution).toBe(true);
      const q=task.printedParts[0].match(/^Q(\d+)/)![1];
      expect(examTopicIdsForQuestion('mathematics','foundation',2011,'main',q,'p2','ev',foundation2011p2.paperFileid))
        .toEqual(expect.arrayContaining(task.examTopicIds));
    }
  });
});

describe('2011 Foundation Phase 2 Paper 1 — exact scales and shared task boundaries', () => {
  const cards=FOUNDATION.filter(c=>c.id.startsWith('maths-2011-fl-p1-project-q'));
  const card=(suffix: string) => {
    const c=cards.find(c=>c.id===`maths-2011-fl-p1-project-q${suffix}`);
    if (!c || c.kind!=='question' || !c.mathematicsScale) throw new Error(suffix);
    return c;
  };
  it('retains all eight required questions, 29 tasks, 30 marking components and 300 marks', () => {
    expect(cards).toHaveLength(29);
    expect(cards.map(c=>c.id).sort()).toEqual(foundation2011project1.cards.map(c=>c.id).sort());
    expect([1,2,3,4,5,6,7,8].map(n=>cards.filter(c=>c.id.startsWith(`maths-2011-fl-p1-project-q${n}-`)).length))
      .toEqual([4,2,2,2,2,7,5,5]);
    expect([1,2,3,4,5,6,7,8].map(n=>cards.filter(c=>c.id.startsWith(`maths-2011-fl-p1-project-q${n}-`)).reduce((s,c)=>s+c.totalMarks,0)))
      .toEqual([25,25,25,25,25,75,50,50]);
    expect(cards.reduce((n,c)=>n+(c.kind==='question' ? c.mathematicsScale?.methods?.[0].components.length ?? 1 : 0),0)).toBe(30);
    expect(foundation2011project1.paperPagesInspected).toEqual(Array.from({length:16},(_,i)=>i+1));
    expect(foundation2011project1.schemePagesInspected).toEqual(Array.from({length:28},(_,i)=>i+1));
  });
  it('uses this paper’s seven Foundation scales and only its three starred tasks', () => {
    for (const [suffix,marks] of [['1-b',[0,3,5]],['3-b',[0,3,4,5]],['6-a-i',[0,8,10]],['1-a',[0,6,9,10]],['2-a',[0,10,15]],['6-a-ii',[0,9,13,15]],['4-a',[0,12,17,20]]] as const)
      expect(card(suffix).mathematicsScale?.marks).toEqual(marks);
    expect(cards.filter(c=>c.kind==='question' && c.mathematicsScale?.fullCreditMinusOne).map(c=>c.id.split('-q')[1]).sort())
      .toEqual(['3-a','3-b','5-b']);
    for (const c of cards) if (c.kind==='question') expect(c.mathematicsScale?.generalNotesPages).toEqual([18,19,24]);
  });
  it('keeps both estimate/calculation prompts and both formula explanations at their shared tariffs', () => {
    expect(card('6-b-i-ii').totalMarks).toBe(15);
    expect(card('6-b-i-ii').mathematicsScale?.markingNote).toContain('either part correct earns high partial credit');
    expect(foundation2011project1.cards.find(c=>c.id===card('6-b-i-ii').id)?.printedParts).toEqual(['Q6(b)(i)','Q6(b)(ii)']);
    expect(card('7-e-f').totalMarks).toBe(5);
    expect(card('7-e-f').mathematicsScale?.markingNote).toContain('retain all three');
    expect(foundation2011project1.cards.find(c=>c.id===card('7-e-f').id)?.printedParts).toEqual(['Q7(e)','Q7(f)']);
    expect(Object.values(foundation2011project1.selectionDecisions).filter(d=>d.classification==='required-answer-identification')).toHaveLength(1);
    expect(card('1-a').mathematicsScale?.markingNote).toContain('All six classifications');
    expect(card('7-a').mathematicsScale?.markingNote).toContain('All six missing entries');
  });
  it('keeps the original graph task, both alternative methods and four independent read-offs', () => {
    expect(card('8-a').totalMarks).toBe(30);
    expect(card('8-a').mathematicsScale?.methods?.[0].components.map(c=>[c.maximum,c.attempt])).toEqual([[20,8],[10,4]]);
    expect(card('8-a').mathematicsScale?.schemePages).toEqual([25,26,27,28]);
    expect(card('8-a').mathematicsScale?.markingNote).toContain('without shown working earns all 30 marks');
    for (const suffix of ['8-b-i','8-b-ii','8-b-iii','8-b-iv']) {
      expect(card(suffix).figure?.src).toBe(card('8-b-i').figure?.src);
      expect(card(suffix).mathematicsScale?.methods?.[0].components[0]).toMatchObject({maximum:5,attempt:2});
      expect(card(suffix).mathematicsScale?.markingNote).toContain('±0.3 on x and ±0.5 on y');
      expect(card(suffix).mathematicsScale?.markingNote).toContain('exact turning point is x = 0.25');
    }
  });
  it('retains both quadratic roots and explains the original variable-label error', () => {
    expect(card('5-a').mathematicsScale?.markingNote).toContain('Both roots are required');
    expect(card('5-b').questionText).toContain('2y² − 7y − 5');
    expect(card('5-b').figure?.sourceNote).toContain('y');
    expect((7-Math.sqrt(89))/4).toBeCloseTo(-0.61,2);
    expect((7+Math.sqrt(89))/4).toBeCloseTo(4.11,2);
    expect(card('7-c').mathematicsScale?.schemePages).toEqual([15,16,23]);
    expect(card('7-d').mathematicsScale?.schemePages).toEqual([15,16,23]);
  });
  it('binds every task to exact Phase 2 source pages, canonical topics and Topic Atlas', () => {
    const spec=resolveCurriculumSpecification('mathematics',2011)!;
    for (const task of foundation2011project1.cards) {
      const c=card(task.id.split('-q')[1]);
      expect(findCanonicalTopic(spec,c.topicId)).toBeDefined();
      expect(c.topicId).toBe(task.topicId);
      expect(c.paperFileid).toBe('LC003BLP130EV');
      expect(c.sourceMaterial?.sourceFileid).toBe('LC003BLP130EV.pdf');
      expect(c.sourceMaterial?.pages).toEqual(task.sourcePages);
      expect(c.mathematicsScale?.schemeFileid).toBe('LC003BLP030EV.pdf');
      expect(c.mathematicsScale?.schemePages).toEqual(task.schemePages);
      expect(c.questionFigure?.src).toMatch(/maths-2011-FL-ask-p1-project-/);
      expect(c.figure?.solution).toBe(true);
      const q=task.printedParts[0].match(/^Q(\d+)/)![1];
      expect(examTopicIdsForQuestion('mathematics','foundation',2011,'main',q,'p1','ev',foundation2011project1.paperFileid))
        .toEqual(expect.arrayContaining(task.examTopicIds));
    }
  });
});

describe('2011 Foundation Phase 2 Paper 2 — both geometry alternatives and shared awards', () => {
  const cards=FOUNDATION.filter(c=>c.id.startsWith('maths-2011-fl-p2-project-q'));
  const card=(suffix: string) => {
    const c=cards.find(c=>c.id===`maths-2011-fl-p2-project-q${suffix}`);
    if (!c || c.kind!=='question' || !c.mathematicsScale) throw new Error(suffix);
    return c;
  };
  it('covers 37 printed asks in 31 mark units with both 25-mark geometry alternatives', () => {
    expect(cards).toHaveLength(31);
    expect(cards.map(c=>c.id).sort()).toEqual(foundation2011project2.cards.map(c=>c.id).sort());
    expect(cards.reduce((s,c)=>s+c.totalMarks,0)).toBe(325);
    expect(foundation2011project2.cards.reduce((s,c)=>s+c.printedParts.length,0)).toBe(37);
    for(const [q,marks] of Object.entries(foundation2011project2.printedQuestionMarks)) {
      expect(foundation2011project2.cards.filter(c=>c.printedParts[0].match(/^Q(\d+[AB]?)/)![1]===q).reduce((s,c)=>s+c.totalMarks,0)).toBe(marks);
    }
    expect(cards.filter(c=>c.id.includes('-q6a-'))).toHaveLength(2);
    expect(cards.filter(c=>c.id.includes('-q6b-'))).toHaveLength(3);
    expect(foundation2011project2.paperPagesInspected).toEqual(Array.from({length:16},(_,i)=>i+1));
    expect(foundation2011project2.schemePagesInspected).toEqual(Array.from({length:24},(_,i)=>i+29));
  });
  it('keeps five grouped task boundaries and the full required responses', () => {
    for(const [suffix,parts,marks] of [['2-b-c-d',3,5],['3-c-d',2,5],['4-b-c',2,10],['7-g-h',2,5],['8-b-i-ii',2,5]] as const) {
      expect(card(suffix).totalMarks).toBe(marks);
      expect(foundation2011project2.cards.find(c=>c.id===card(suffix).id)?.printedParts).toHaveLength(parts);
      expect(card(suffix).mathematicsScale?.components).toBeUndefined();
    }
    expect(card('2-b-c-d').mathematicsScale?.markingNote).toContain('All ten equal-number pairs');
    expect(card('4-b-c').mathematicsScale?.markingNote).toContain('Both slopes');
    expect(card('5-a').mathematicsScale?.markingNote).toContain('Both intercepts');
    expect(card('6b-b').mathematicsScale?.markingNote).toContain('Both s and t');
    expect(card('2-a').mathematicsScale?.markingNote).toContain('three distinct valid ordered pairs');
    expect(foundation2011project2.selectionReview.find(s=>s.classification==='open-example-construction')?.reason).toContain('not a printed pool');
  });
  it('preserves unusual 25B and 20B awards and only three published stars', () => {
    expect(card('8-a-ii').totalMarks).toBe(25);
    expect(card('8-a-ii').mathematicsScale?.marks).toEqual([0,20,25]);
    expect(card('7-a').mathematicsScale?.marks).toEqual([0,15,20]);
    expect(card('1-a').mathematicsScale?.marks).toEqual([0,12,17,20]);
    expect(card('3-a').mathematicsScale?.marks).toEqual([0,9,13,15]);
    expect(cards.filter(c=>c.kind==='question' && c.mathematicsScale?.fullCreditMinusOne).map(c=>c.id.split('-q')[1]).sort())
      .toEqual(['8-a-ii','8-a-iii','8-b-i-ii']);
    for(const c of cards) if(c.kind==='question') expect(c.mathematicsScale?.generalNotesPages).toEqual([44,45]);
  });
  it('retains statistical data, three-page dependencies and all accepted explanations', () => {
    for(const suffix of ['7-a','7-b','7-c','7-d','7-e','7-g-h','7-i']) expect(card(suffix).stem).toContain('12, 40, 64, 56, 24, 4');
    expect(card('7-g-h').sourceMaterial?.pages).toEqual([10,11,12]);
    expect(card('7-g-h').mathematicsScale?.schemePages).toEqual([39,40,49]);
    expect(card('7-g-h').mathematicsScale?.markingNote).toContain('candidate’s consistent sample estimate');
    expect(card('7-i').mathematicsScale?.markingNote).toContain('Both original explanations');
    expect(card('7-c').mathematicsScale?.markingNote).toContain('3.0 to 3.5 kg');
    expect(card('7-b').figure?.sourceNote).toContain('each vertical unit represents four babies');
  });
  it('explains source errors and retains construction and trigonometry details', () => {
    expect(card('3-b').figure?.sourceNote).toContain('6.769');
    expect(card('3-b').figure?.sourceNote).toContain('median, which is 7.2 mm');
    expect(Math.atan(4)*180/Math.PI).toBeCloseTo(75.96,2);
    expect(card('8-b-i-ii').figure?.sourceNote).toContain('premature-rounding');
    expect(card('8-b-i-ii').mathematicsScale?.markingNote).toContain('All three trigonometric methods');
    expect(card('6a-b').mathematicsScale?.markingNote).toContain('±5° / ±10°');
    for(const suffix of ['6a-b','8-a-i','8-c']) expect(card(suffix).sourceMaterial?.measurementRequired).toBe(true);
    expect(card('8-c').sourceMaterial?.pages).toEqual([14,15]);
    expect(card('8-a-iv').stem).toContain('2.8 cm');
  });
  it('binds each card to the exact Phase 2 paper and canonical Mark Bank and Atlas topics', () => {
    const spec=resolveCurriculumSpecification('mathematics',2011)!;
    for(const task of foundation2011project2.cards) {
      const c=card(task.id.split('-q')[1]);
      expect(findCanonicalTopic(spec,c.topicId)).toBeDefined();
      expect(c.topicId).toBe(task.topicId);
      expect(c.paperFileid).toBe('LC003BLP230EV');
      expect(c.sourceMaterial?.sourceFileid).toBe('LC003BLP230EV.pdf');
      expect(c.sourceMaterial?.pages).toEqual(task.sourcePages);
      expect(c.mathematicsScale?.schemeFileid).toBe('LC003BLP030EV.pdf');
      expect(c.mathematicsScale?.schemePages).toEqual(task.schemePages);
      expect(c.questionFigure?.src).toMatch(/maths-2011-FL-ask-p2-project-/);
      expect(c.figure?.solution).toBe(true);
      const q=task.printedParts[0].match(/^Q(\d+[AB]?)/)![1];
      expect(examTopicIdsForQuestion('mathematics','foundation',2011,'main',q,'p2','ev',foundation2011project2.paperFileid))
        .toEqual(expect.arrayContaining(task.examTopicIds));
    }
  });
});

describe('2010 Higher legacy Paper 1 — all four non-unit fifth roots', () => {
  const cards=HIGHER.filter(c=>c.id.startsWith('maths-2010-hl-p1-q'));
  const card=(suffix: string) => {
    const c=cards.find(c=>c.id===`maths-2010-hl-p1-q${suffix}`);
    if (!c || c.kind!=='question' || !c.mathematicsScale) throw new Error(suffix);
    return c;
  };
  it('covers all 40 published tasks and 400 offered marks without repeating the root choice', () => {
    expect(cards).toHaveLength(40);
    expect(cards.map(c=>c.id).sort()).toEqual(higher2010p1.cards.map(c=>c.id).sort());
    const logical=new Map<string,number>();
    for(const c of higher2010p1.cards) logical.set(c.id,c.totalMarks);
    expect(logical.size).toBe(40);
    expect([...logical.values()].reduce((a,b)=>a+b,0)).toBe(400);
    expect(cards.reduce((a,c)=>a+c.totalMarks,0)).toBe(400);
    expect(higher2010p1.paperPagesInspected).toEqual([1,2,3,4,5,6]);
    expect(higher2010p1.schemePagesInspected).toEqual(Array.from({length:40},(_,i)=>i+1));
    expect(Object.keys(higher2010p1.selectionDecisions)).toHaveLength(5);
  });
  it('accepts every eligible fifth root in one card with the unchanged ten-mark tariff', () => {
    const c = card('3-c-ii-root-1');
    const t = higher2010p1.cards.find(t=>t.id===c.id)!;
    expect(t.selectionChoice?.pool).toEqual(['1','2','3','4']);
    expect(t.selectionChoice?.choose).toBe(1);
    expect(c.questionText).toBe('Choose one of the roots w, where w ≠ 1. Prove that w² + w³ is real.');
    expect(c.totalMarks).toBe(10);
    expect(c.mathematicsScale?.methods?.[0].components.map(c=>c.maximum)).toEqual([5,5]);
    expect(cards.filter(c=>c.id.includes('-root-'))).toHaveLength(1);
    expect(c.figure?.sourceNote).toContain('any permitted choice');
    for(let n=1;n<=4;n++) {
      const theta=2*n*Math.PI/5;
      expect(Math.sin(2*theta)+Math.sin(3*theta)).toBeCloseTo(0,12);
      expect(Math.cos(2*theta)+Math.cos(3*theta)).toBeCloseTo(2*(-1)**n*Math.cos(n*Math.PI/5),12);
    }
  });
  it('retains the two-tangent and three-slope methods as separate scoring alternatives', () => {
    const methods=card('6-c-ii').mathematicsScale?.methods!;
    expect(methods.map(m=>m.components.map(c=>c.maximum))).toEqual([[5,5],[10]]);
    expect(methods[1].components[0].attempt).toBe(3);
    expect(card('6-c-ii').mathematicsScale?.markingNote).toContain('Both points and both tangents');
    for(const c of cards) if(c.kind==='question') {
      expect(c.mathematicsScale?.fullCreditMinusOne).toBe(false);
      for(const m of c.mathematicsScale!.methods!) expect(m.components.reduce((a,b)=>a+b.maximum,0)).toBe(c.totalMarks);
    }
  });
  it('keeps required paired answers and both binomial expansions together', () => {
    expect(card('3-b-i').questionText).toContain('both');
    expect(card('3-c-i').questionText).toContain('five roots');
    expect(card('5-c-i').questionText).toContain('both');
    expect(card('5-c-i').mathematicsScale?.methods?.[0].components.map(c=>c.maximum)).toEqual([5,5]);
    expect(card('5-c-ii').mathematicsScale?.methods?.[1].components[1].label).toContain('both roots');
    expect(card('1-c-i').figure?.src).toBe(card('1-c-ii').figure?.src);
  });
  it('discloses source mistakes and conflicting allocations while preserving the original evidence', () => {
    expect(card('2-c-ii').figure?.sourceNote).toContain('If a + b = 0');
    expect(card('4-c-ii').figure?.sourceNote).toContain('(k + 2)(2k + 3)');
    expect(card('6-a').figure?.sourceNote).toContain('not f(3/2)');
    expect(card('8-b').figure?.sourceNote).toContain('totalling only 15');
    expect(card('8-b').mathematicsScale?.methods?.[0].components.map(c=>[c.maximum,c.attempt])).toEqual([[10,3],[5,2],[5,2]]);
    expect(card('8-b').mathematicsScale?.schemePages).toContain(35);
    expect(card('8-c-iii').figure?.sourceNote).toContain('detailed row says Att 2');
    expect(card('8-c-iii').mathematicsScale?.methods?.[0].components[0].attempt).toBe(3);
    expect(card('8-c-iii').mathematicsScale?.schemePages).toContain(35);
  });
  it('joins every exact legacy paper task to canonical Mark Bank and Atlas topics', () => {
    const spec=resolveCurriculumSpecification('mathematics',2010)!;
    for(const task of higher2010p1.cards) {
      const c=card(task.id.split('-q')[1]);
      expect(findCanonicalTopic(spec,c.topicId)).toBeDefined();
      expect(c.topicId).toBe(task.topicId);
      expect(c.paperFileid).toBe('LC003ALP100EV');
      expect(c.sourceMaterial?.sourceFileid).toBe('LC003ALP100EV.pdf');
      expect(c.sourceMaterial?.pages).toEqual(task.sourcePages);
      expect(c.mathematicsScale?.schemeFileid).toBe('LC003ALP000EV.pdf');
      expect(c.mathematicsScale?.schemePages).toEqual(task.schemePages);
      expect(c.mathematicsScale?.generalNotesPages).toEqual([4]);
      expect(c.questionFigure?.src).toMatch(/maths-2010-HL-ask-p1-/);
      expect(c.figure?.solution).toBe(true);
      const q=task.printedParts[0].match(/^Q(\d+)/)![1];
      expect(examTopicIdsForQuestion('mathematics','higher',2010,'main',q,'p1','ev',higher2010p1.paperFileid)).toEqual(expect.arrayContaining(task.examTopicIds));
    }
  });
});

describe('2010 Higher legacy Paper 2 — complete core and optional tasks', () => {
  const cards=HIGHER.filter(c=>c.id.startsWith('maths-2010-hl-p2-q'));
  const card=(suffix: string) => {
    const c=cards.find(c=>c.id===`maths-2010-hl-p2-q${suffix}`);
    if (!c || c.kind!=='question' || !c.mathematicsScale) throw new Error(suffix);
    return c;
  };
  const steps=(suffix:string)=>card(suffix).mathematicsScale!.methods![0].components;
  it('retains all 57 marked tasks, including all four optional questions', () => {
    expect(cards).toHaveLength(57);
    expect(cards.map(c=>c.id).sort()).toEqual(higher2010p2.cards.map(c=>c.id).sort());
    expect([1,2,3,4,5,6,7,8,9,10,11].map(n=>cards.filter(c=>c.id.startsWith(`maths-2010-hl-p2-q${n}-`)).length))
      .toEqual([4,6,5,5,5,3,6,6,5,7,5]);
    for(let n=1;n<=11;n++) expect(cards.filter(c=>c.id.startsWith(`maths-2010-hl-p2-q${n}-`)).reduce((s,c)=>s+c.totalMarks,0)).toBe(50);
    expect(cards.reduce((s,c)=>s+c.totalMarks,0)).toBe(550);
    expect(higher2010p2.paperPagesInspected).toEqual([1,2,3,4,5,6,7,8]);
    expect(higher2010p2.schemePagesInspected).toEqual(Array.from({length:44},(_,i)=>39+i));
    expect(Object.keys(higher2010p2.selectionDecisions)).toHaveLength(8);
    expect(higher2010p2.selectionReview.find(s=>s.classification==='open-example-construction')?.reason).toContain('No finite pool');
  });
  it('uses exactly the fixed awards and hit-or-miss rules printed for each special case', () => {
    for(const s of ['1-b-i','2-b-i']) expect(steps(s)[0].permittedMarks).toEqual([0,2,5]);
    expect(steps('1-c')[1].permittedMarks).toEqual([0,5,15]);
    expect(steps('6-c')[0].permittedMarks).toEqual([0,6,17,20]);
    for(const s of ['2-c-iii','8-b-i','8-c-ii','8-c-iii']) {
      expect(steps(s)[0].attempt).toBe(0);
      expect(steps(s)[0].permittedMarks).toEqual([0,card(s).totalMarks]);
    }
    for(const m of card('5-c-ii').mathematicsScale!.methods!) {
      expect(m.components.map(c=>c.maximum)).toEqual([5,10]);
      expect(m.components[1].permittedMarks).toEqual([0,3,10]);
    }
  });
  it('keeps required lists and multi-step proofs together with the full original context', () => {
    expect(steps('6-b').map(c=>c.maximum)).toEqual([5,5,5,5]);
    expect(steps('9-c').map(c=>c.maximum)).toEqual([5,5,5,5]);
    expect(steps('10-b-i').map(c=>c.maximum)).toEqual([5,5]);
    expect(card('10-b-iii').questionText).toContain('all subgroups');
    expect(card('9-b-iii').questionText).toContain('four, five or six');
    for(const s of ['2-c-i','2-c-ii','2-c-iii','4-c-i','4-c-ii','4-c-iii','10-b-i','10-b-ii','10-b-iii','10-b-iv','10-b-v','11-c-i','11-c-ii']) {
      expect(card(s).questionFigure).toBeDefined();
      expect(card(s).sourceMaterial?.pages).toHaveLength(1);
    }
    for(const c of cards) if(c.kind==='question') {
      expect(c.mathematicsScale?.fullCreditMinusOne).toBe(false);
      for(const m of c.mathematicsScale!.methods!) expect(m.components.reduce((a,b)=>a+b.maximum,0)).toBe(c.totalMarks);
    }
  });
  it('retains the proof, derivation and prior-work caps beside the worked solutions', () => {
    expect(card('3-c-ii').mathematicsScale?.markingNote).toContain('at most the attempt mark 6');
    expect(card('7-c-ii').mathematicsScale?.markingNote).toContain('capped at 3');
    expect(card('8-b-ii').mathematicsScale?.markingNote).toContain('part (b)(i) earns 0');
    expect(card('8-c-i').mathematicsScale?.markingNote).toContain('without derivation');
    expect(card('10-b-v').mathematicsScale?.markingNote).toContain('explicit map');
  });
  it('explains source errors without rewriting the official evidence', () => {
    expect(card('1-c').figure?.sourceNote).toContain('√(16 + 4)');
    expect(card('4-a').figure?.sourceNote).toContain('at P');
    for(const s of ['7-c-i','7-c-ii']) expect(card(s).figure?.sourceNote).toContain('absolute value');
    expect(card('9-b-i').figure?.sourceNote).toContain('three decimal places');
    expect(card('9-c').figure?.sourceNote).toContain('[78.3, 81.7]');
    for(const s of ['10-a-i','10-a-ii']) expect(card(s).figure?.sourceNote).toContain('1 has no inverse');
    expect(card('11-b-i').figure?.sourceNote).toContain('Q11(b)(i)');
    expect(card('11-c-i').figure?.sourceNote).toContain('y′ = y/5');
    const margin=1.96*6/Math.sqrt(50);
    expect((80+margin).toFixed(1)).toBe('81.7');
    expect(Math.sqrt([-5,-10,-15,-20,-25].reduce((s,x)=>s+(x+15)**2,0)/5)).toBeCloseTo(5*Math.sqrt(2));
  });
  it('joins every exact legacy paper task to canonical Mark Bank and Atlas topics', () => {
    const spec=resolveCurriculumSpecification('mathematics',2010)!;
    for(const task of higher2010p2.cards) {
      const c=card(task.id.split('-q')[1]);
      expect(findCanonicalTopic(spec,c.topicId)).toBeDefined();
      expect(c.topicId).toBe(task.topicId);
      expect(c.paperFileid).toBe('LC003ALP200EV');
      expect(c.sourceMaterial?.sourceFileid).toBe('LC003ALP200EV.pdf');
      expect(c.sourceMaterial?.pages).toEqual(task.sourcePages);
      expect(c.mathematicsScale?.schemeFileid).toBe('LC003ALP000EV.pdf');
      expect(c.mathematicsScale?.schemePages).toEqual(task.schemePages);
      expect(c.mathematicsScale?.generalNotesPages).toEqual([41]);
      expect(c.questionFigure?.src).toMatch(/maths-2010-HL-ask-p2-/);
      expect(c.figure?.solution).toBe(true);
      const q=task.printedParts[0].match(/^Q(\d+)/)![1];
      expect(examTopicIdsForQuestion('mathematics','higher',2010,'main',q,'p2','ev',higher2010p2.paperFileid)).toEqual(expect.arrayContaining(task.examTopicIds));
    }
  });
});


describe('2010 Higher Project Maths Paper 2 — exact first-year scales', () => {
  const cards=HIGHER.filter(c=>c.id.startsWith('maths-2010-hl-p2-project-q'));
  const card=(suffix:string)=> {
    const c=cards.find(c=>c.id===`maths-2010-hl-p2-project-q${suffix}`);
    if(!c || c.kind!=='question') throw new Error(suffix);
    return c;
  };
  it('retains every task and both Question 9 routes at the published boundaries', () => {
    expect(cards).toHaveLength(35);
    expect(cards.map(c=>c.id).sort()).toEqual(higher2010project2.cards.map(c=>c.id).sort());
    expect(cards.reduce((s,c)=>s+c.totalMarks,0)).toBe(350);
    expect(higher2010project2.cards.reduce((s,c)=>s+(c.components?.length??1),0)).toBe(42);
    expect(['1','2','3','4','5','6','7','8','9a','9b'].map(q=>cards.filter(c=>c.id.startsWith(`maths-2010-hl-p2-project-q${q}-`)).length)).toEqual([4,2,2,2,3,4,7,5,3,3]);
    for(const [q,marks] of Object.entries(higher2010project2.printedQuestionMarks)) {
      expect(higher2010project2.cards.filter(c=>c.printedParts[0].match(/^Q(\d+[AB]?)/)![1]===q).reduce((s,c)=>s+c.totalMarks,0)).toBe(marks);
    }
    expect(higher2010project2.paperPagesInspected).toEqual(Array.from({length:20},(_,i)=>i+1));
    expect(higher2010project2.schemePagesInspected).toEqual([3,4,...Array.from({length:30},(_,i)=>i+41)]);
  });
  it('uses the 2010 bands, including different ten-, fifteen- and twenty-mark partial credit', () => {
    expect(card('1-a').mathematicsScale?.marks).toEqual([0,4,10]);
    expect(card('4-b').mathematicsScale?.marks).toEqual([0,3,8,10]);
    expect(card('2-a').mathematicsScale?.marks).toEqual([0,5,10,15]);
    expect(card('3-a').mathematicsScale?.marks).toEqual([0,7,13,20]);
    expect(card('9a-b').mathematicsScale?.marks).toEqual([0,6,9,13,15]);
    expect(card('9a-c').mathematicsScale?.components?.[0].marks).toEqual([0,5,10,15,20]);
    expect(card('9b-a').mathematicsScale?.components?.[2].marks).toEqual([0,3,5,8,10]);
  });
  it('keeps named scoring steps together and restricts the six starred awards exactly', () => {
    for(const [suffix,codes] of [['6-b',['5B','5C']],['7-b',['5A','5B']],['9a-c',['20D','5B']],['9b-a',['5B','5B','10D']],['9b-b-ii',['5B','10B','5B']]] as const) {
      expect(card(suffix).mathematicsScale?.components?.map(c=>c.code)).toEqual(codes);
    }
    expect(card('7-b').mathematicsScale?.components?.[0].marks).toEqual([0,5]);
    expect(cards.filter(c=>c.kind==='question' && c.mathematicsScale?.fullCreditMinusOne).map(c=>c.id.split('-q')[1])).toEqual(['8-a','8-c','9a-a','9a-b','9b-b-i']);
    expect(card('9b-b-ii').mathematicsScale?.fullCreditMinusOne).toBe(false);
    expect(card('9b-b-ii').mathematicsScale?.components?.map(c=>!!c.fullCreditMinusOne)).toEqual([false,false,true]);
    expect(card('9b-b-ii').mathematicsScale?.markingNote).toContain('Only the final 5B component');
  });
  it('keeps required paired responses, graph tolerances and all alternative methods', () => {
    expect(card('2-b').mathematicsScale?.markingNote).toContain('All three labels');
    expect(card('5-a').mathematicsScale?.markingNote).toContain('Both complete families');
    expect(card('5-b').mathematicsScale?.markingNote).toContain('All three matches');
    expect(card('6-c').mathematicsScale?.markingNote).toContain('Both vectors');
    expect(card('6-d').mathematicsScale?.markingNote).toContain('All three published consistency arguments');
    expect(card('7-b').mathematicsScale?.markingNote).toContain('135–139');
    expect(card('7-d').mathematicsScale?.markingNote).toContain('without working');
    expect(card('7-f').mathematicsScale?.markingNote).toContain('open choices');
    expect(card('9a-b').mathematicsScale?.markingNote).toContain('complement and direct-sum');
    expect(card('9b-a').mathematicsScale?.markingNote).toContain('restrictions on alternative proofs');
    expect(card('3-a').sourceMaterial?.measurementRequired).toBe(true);
  });
  it('retains the actual sample, original graphs, attribution and cross-page dependencies', () => {
    const sample=[39.5,40,39.7,40.2,39.8,39.7,40.2,39.9,40.1,39.6];
    const mean=sample.reduce((s,x)=>s+x,0)/10;
    expect(mean).toBeCloseTo(39.87,10);
    expect((mean-40)/(0.2/Math.sqrt(10))).toBeCloseTo(-2.0555,3);
    expect(card('9a-c').stem).toContain('39.5, 40.0, 39.7, 40.2, 39.8, 39.7, 40.2, 39.9, 40.1, 39.6');
    expect(card('9a-c').mathematicsScale?.markingNote).toContain('two-tailed');
    for(const suffix of ['7-d','7-e','7-f','7-g']) expect(card(suffix).sourceMaterial?.pages).toEqual([10,11]);
    expect(card('6-d').sourceMaterial?.pages).toEqual([8,9]);
    expect(card('9a-c').sourceMaterial?.pages).toEqual([14,15]);
    expect(card('8-e').sourceMaterial?.pages).toEqual([12,13]);
    for(const suffix of ['7-a','7-b','7-c','7-d','7-e','7-f','7-g']) {
      const crop=questionCropOverrides[`maths-2010-hl-p2-project-q${suffix}` as keyof typeof questionCropOverrides];
      if (!('regions' in crop)) throw new Error(`Missing graph regions: ${suffix}`);
      const regions=crop.regions;
      expect(regions.some(r=>r.page===10 && r.top<=157 && r.bottom>=552)).toBe(true);
      expect(card(suffix).stem).toContain('source attribution');
    }
    expect(8*Math.sqrt(17)).toBeCloseTo(32.9848,3);
  });
  it('joins every exact Project paper task to canonical Mark Bank and Topic Atlas topics', () => {
    const spec=resolveCurriculumSpecification('mathematics',2010)!;
    for(const task of higher2010project2.cards) {
      const c=card(task.id.split('-q')[1]);
      expect(findCanonicalTopic(spec,c.topicId)).toBeDefined();
      expect(c.topicId).toBe(task.topicId);
      expect(c.paperFileid).toBe('LC003ALP230EV');
      expect(c.sourceMaterial?.sourceFileid).toBe('LC003ALP230EV.pdf');
      expect(c.sourceMaterial?.pages).toEqual(task.sourcePages);
      expect(c.mathematicsScale?.schemeFileid).toBe('LC003ALP030EV.pdf');
      expect(c.mathematicsScale?.schemePages).toEqual(task.schemePages);
      expect(c.mathematicsScale?.generalNotesPages).toEqual([59]);
      expect(c.questionFigure?.src).toMatch(/maths-2010-HL-ask-p2-project-/);
      expect(c.figure?.solution).toBe(true);
      const q=task.printedParts[0].match(/^Q(\d+[AB]?)/)![1];
      expect(examTopicIdsForQuestion('mathematics','higher',2010,'main',q,'p2','ev',higher2010project2.paperFileid)).toEqual(expect.arrayContaining(task.examTopicIds));
    }
  });
});


describe('2010 Ordinary legacy Paper 1 — complete original deduction tasks', () => {
  const cards=ORDINARY.filter(c=>c.id.startsWith('maths-2010-ol-p1-q'));
  const card=(suffix:string)=> {
    const c=cards.find(c=>c.id===`maths-2010-ol-p1-q${suffix}`);
    if(!c || c.kind!=='question') throw new Error(suffix);
    return c;
  };
  it('retains all forty tasks and all eight offered questions despite the six-question exam limit', () => {
    expect(cards).toHaveLength(40);
    expect(cards.map(c=>c.id).sort()).toEqual(ordinary2010p1.cards.map(c=>c.id).sort());
    expect(cards.reduce((s,c)=>s+c.totalMarks,0)).toBe(400);
    expect(cards.reduce((s,c)=>s+(c.kind==='question'?c.mathematicsScale!.methods![0].components.length:0),0)).toBe(48);
    expect([1,2,3,4,5,6,7,8].map(q=>cards.filter(c=>c.id.startsWith(`maths-2010-ol-p1-q${q}-`)).length)).toEqual([5,4,4,4,7,5,6,5]);
    for(let q=1;q<=8;q++) expect(cards.filter(c=>c.id.startsWith(`maths-2010-ol-p1-q${q}-`)).reduce((s,c)=>s+c.totalMarks,0)).toBe(50);
    expect(ordinary2010p1.paperPagesInspected).toEqual([1,2,3,4,5,6,7,8]);
    expect(ordinary2010p1.schemePagesInspected).toEqual(Array.from({length:43},(_,i)=>i+1));
    expect(card('6-a').mathematicsScale?.markingNote).toContain('no printed answer-choice pool');
  });
  it('preserves exact component allocations and attempt floors without splitting complete responses', () => {
    for(const [suffix,allocations] of [['1-b-ii',[[5,2],[5,2]]],['2-b',[[10,3],[5,2],[5,2],[5,2]]],['3-a',[[10,3],[5,2]]],['3-b',[[10,3],[10,3]]],['4-c',[[5,2],[5,2],[5,2]]]] as const) {
      expect(card(suffix).mathematicsScale?.methods?.[0].components.map(c=>[c.maximum,c.attempt])).toEqual(allocations);
    }
    for(const c of cards) if(c.kind==='question') {
      expect(c.mathematicsScale?.fullCreditMinusOne).toBe(false);
      for(const m of c.mathematicsScale!.methods!) expect(m.components.reduce((s,c)=>s+c.maximum,0)).toBe(c.totalMarks);
    }
    expect(card('2-b').mathematicsScale?.markingNote).toContain('2 + 2');
    expect(card('6-c-ii').mathematicsScale?.markingNote).toContain('Both coordinate pairs');
    expect(card('7-c-i').mathematicsScale?.markingNote).toContain('t = 0 and t = 10');
  });
  it('restricts exceptional fixed awards and keeps the separate working-shown route', () => {
    expect(card('1-c-ii').mathematicsScale?.methods?.[0].components[0].permittedMarks).toEqual([0,2,5]);
    for(const suffix of ['5-a','6-b-i']) {
      const methods=card(suffix).mathematicsScale?.methods!;
      expect(methods.map(m=>m.id)).toEqual(['working-shown','answers-without-work']);
      expect(methods[1].components[0].permittedMarks).toEqual([0,3,4,7,10]);
    }
    expect(card('8-i').mathematicsScale?.methods?.[1].components[0].permittedMarks).toEqual([0,5,6,9,12,15]);
    expect(card('7-b-i').mathematicsScale?.markingNote).toContain('earns 0');
    expect(card('8-iv').mathematicsScale?.markingNote).toContain('Seven points');
    expect(card('6-b-ii').mathematicsScale?.markingNote).toContain('vertical asymptote');
  });
  it('explains actual printed inconsistencies and retains every relevant original scheme page', () => {
    expect(card('3-b').figure?.sourceNote).toBeUndefined();
    expect(card('3-c-ii').figure?.sourceNote).toContain('2');
    expect(card('3-c-ii').mathematicsScale?.methods?.[0].components[0].attempt).toBe(2);
    expect(card('7-b-i').figure?.sourceNote).toContain('Δx');
    expect(card('8-v').figure?.sourceNote).toContain('distinct');
    for(const suffix of ['7-c-i','7-c-ii','7-c-iii']) expect(card(suffix).mathematicsScale?.schemePages).toContain(35);
    for(const suffix of ['8-i','8-ii','8-iii','8-iv','8-v']) expect(card(suffix).mathematicsScale?.schemePages).toContain(37);
    expect(221/0.85*1.14).toBeCloseTo(296.40,10);
    expect([1,-1].map(x=>x-5/x)).toEqual([-4,4]);
    expect([-3,-2,0,2,3].map(x=>x**3-3*x+1)).toEqual([-17,-1,1,3,19]);
  });
  it('joins every exact original-paper task to canonical Mark Bank and Topic Atlas topics', () => {
    const spec=resolveCurriculumSpecification('mathematics',2010)!;
    for(const task of ordinary2010p1.cards) {
      const c=card(task.id.split('-q')[1]);
      expect(findCanonicalTopic(spec,c.topicId)).toBeDefined();
      expect(c.topicId).toBe(task.topicId);
      expect(c.paperFileid).toBe('LC003GLP100EV');
      expect(c.sourceMaterial?.sourceFileid).toBe('LC003GLP100EV.pdf');
      expect(c.sourceMaterial?.pages).toEqual(task.sourcePages);
      expect(c.mathematicsScale?.schemeFileid).toBe('LC003GLP000EV.pdf');
      expect(c.mathematicsScale?.schemePages).toEqual(task.schemePages);
      expect(c.mathematicsScale?.generalNotesPages).toEqual([4,5]);
      expect(c.questionFigure?.src).toMatch(/maths-2010-OL-ask-p1-/);
      expect(c.figure?.solution).toBe(true);
      const q=task.printedParts[0].match(/^Q(\d+)/)![1];
      expect(examTopicIdsForQuestion('mathematics','ordinary',2010,'main',q,'p1','ev',ordinary2010p1.paperFileid)).toEqual(expect.arrayContaining(task.examTopicIds));
    }
  });
});


describe('2010 Ordinary legacy Paper 2 — every core and optional task', () => {
  const cards=ORDINARY.filter(c=>c.id.startsWith('maths-2010-ol-p2-q'));
  const card=(suffix:string)=> {
    const c=cards.find(c=>c.id===`maths-2010-ol-p2-q${suffix}`);
    if(!c || c.kind!=='question') throw new Error(suffix);
    return c;
  };
  it('retains all 74 published tasks across all eleven offered questions', () => {
    expect(cards).toHaveLength(74);
    expect(cards.map(c=>c.id).sort()).toEqual(ordinary2010p2.cards.map(c=>c.id).sort());
    expect(cards.reduce((s,c)=>s+c.totalMarks,0)).toBe(550);
    expect(cards.reduce((s,c)=>s+(c.kind==='question'?c.mathematicsScale!.methods![0].components.length:0),0)).toBe(77);
    expect(Array.from({length:11},(_,i)=>cards.filter(c=>c.id.startsWith(`maths-2010-ol-p2-q${i+1}-`)).length)).toEqual([6,8,6,7,7,10,6,7,7,5,5]);
    for(let q=1;q<=11;q++) expect(cards.filter(c=>c.id.startsWith(`maths-2010-ol-p2-q${q}-`)).reduce((s,c)=>s+c.totalMarks,0)).toBe(50);
    expect(ordinary2010p2.paperPagesInspected).toEqual(Array.from({length:12},(_,i)=>i+1));
    expect(ordinary2010p2.schemePagesInspected).toEqual(Array.from({length:55},(_,i)=>i+42));
    expect(Object.keys(ordinary2010p2.selectionDecisions)).toHaveLength(3);
    expect(ordinary2010p2.selectionReview.find(s=>s.classification==='counting-scenario')?.reason).toContain('not printed answer-choice menus');
  });
  it('keeps separately scored work inside its original practicable task', () => {
    expect(card('1-b-i').mathematicsScale?.methods?.[0].components.map(c=>[c.maximum,c.attempt])).toEqual([[10,3],[5,2]]);
    expect(card('11-b-i').mathematicsScale?.methods?.[0].components.map(c=>[c.maximum,c.attempt])).toEqual([[10,3],[5,2],[5,2]]);
    expect(card('11-b-i').mathematicsScale?.methods?.[0].components[0].label).toBe('Better inequality');
    expect(card('11-b-ii').mathematicsScale?.markingNote).toContain('Testing only that vertex earns at most 2');
    for(const c of cards) if(c.kind==='question') {
      expect(c.mathematicsScale?.fullCreditMinusOne).toBe(false);
      for(const m of c.mathematicsScale!.methods!) expect(m.components.reduce((s,c)=>s+c.maximum,0)).toBe(c.totalMarks);
    }
  });
  it('honours hit-or-miss, strict awards and the separate vector assessment routes', () => {
    for(const suffix of ['2-c-ii','2-c-iii','8-c-i','8-c-ii','8-c-iii','8-c-iv']) expect(card(suffix).mathematicsScale?.methods?.[0].components[0].permittedMarks).toEqual([0,5]);
    expect(card('5-b-iv').mathematicsScale?.methods?.[0].components[0].permittedMarks).toEqual([0,10]);
    for(const [suffix,marks] of [['3-b-i',[0,5,15]],['3-c-ii',[0,3,10]],['5-c-i',[0,4,5]],['5-c-ii',[0,9,10]],['7-a-iii',[0,5,14,15]],['11-b-iii',[0,3,10]]] as const) expect(card(suffix).mathematicsScale?.methods?.[0].components[0].permittedMarks).toEqual(marks);
    for(const suffix of ['6-c-i','6-c-ii','6-c-iii']) expect(card(suffix).mathematicsScale?.methods?.[0].components[0].permittedMarks).toEqual([0,2,5]);
    expect(card('6-c-iv').mathematicsScale?.methods?.[0].components[0].permittedMarks).toEqual([0,2,4,5]);
    expect(card('9-b-ii').mathematicsScale?.methods?.map(m=>m.components[0].permittedMarks)).toEqual([[0,3,4,7,9,10],[0,10]]);
    expect(card('9-b-iii').mathematicsScale?.methods?.map(m=>m.components[0].permittedMarks)).toEqual([[0,2,4,5],[0,2,5]]);
  });
  it('preserves exact data, position-vector meaning and independently checked answers', () => {
    const amounts=[10,20,30,50],freq=[2,4,8,6];
    const mean=amounts.reduce((s,x,i)=>s+x*freq[i],0)/20;
    const sumSq=amounts.reduce((s,x,i)=>s+(x-mean)**2*freq[i],0);
    expect(mean).toBe(32);expect(sumSq).toBe(3520);
    expect(Math.sqrt(sumSq/20)).toBeCloseTo(13.2665,4);
    expect(Math.sqrt(sumSq/19)).toBeCloseTo(13.6111,4);
    expect(card('7-a-iii').figure?.sourceNote).toContain('13.139');
    expect(card('7-a-iii').stem).toContain('donation intervals');
    expect(card('7-a-iii').stem).toContain('excludes its upper endpoint');
    expect(card('9-c-ii').stem).toContain('position vector u = OU');
    expect(card('9-c-ii').mathematicsScale?.markingNote).toContain('RU = u − r');
    expect([(9+2*12)/3,(12+2*(-9))/3]).toEqual([11,-2]);
    expect(card('5-c-i').questionText).toContain('cable PR');
    expect(card('5-c-ii').figure?.sourceNote).toBeUndefined();
    expect(17.4/Math.cos(50*Math.PI/180)).toBeCloseTo(27.069,2);
    expect(Math.round(Math.hypot(32.4,17.4*Math.tan(50*Math.PI/180)))).toBe(38);
    expect(['i','ii','iii','iv'].map(x=>card(`8-c-${x}`).questionText)).toEqual(['Find ∠PSQ.','Find ∠SQP.','Find ∠QPR.','Find ∠RQS.']);
    expect(card('8-b').figure?.sourceNote).toContain('Converse, supplied by NextStepUni');
  });
  it('joins all exact paper tasks to both canonical Mark Bank and Topic Atlas topics', () => {
    const spec=resolveCurriculumSpecification('mathematics',2010)!;
    for(const task of ordinary2010p2.cards) {
      const c=card(task.id.split('-q')[1]);
      expect(findCanonicalTopic(spec,c.topicId)).toBeDefined();
      expect(c.topicId).toBe(task.topicId);
      expect(c.paperFileid).toBe('LC003GLP200EV');
      expect(c.sourceMaterial?.sourceFileid).toBe('LC003GLP200EV.pdf');
      expect(c.sourceMaterial?.pages).toEqual(task.sourcePages);
      expect(c.mathematicsScale?.schemeFileid).toBe('LC003GLP000EV.pdf');
      expect(c.mathematicsScale?.schemePages).toEqual(task.schemePages);
      expect(c.mathematicsScale?.generalNotesPages).toEqual([43,44]);
      expect(c.questionFigure?.src).toMatch(/maths-2010-OL-ask-p2-/);
      expect(c.figure?.solution).toBe(true);
      const q=task.printedParts[0].match(/^Q(\d+)/)![1];
      expect(examTopicIdsForQuestion('mathematics','ordinary',2010,'main',q,'p2','ev',ordinary2010p2.paperFileid)).toEqual(expect.arrayContaining(task.examTopicIds));
    }
    for(const suffix of ['4-c-i','4-c-ii','9-b-i','9-b-ii','9-b-iii']) expect(card(suffix).sourceMaterial?.measurementRequired).toBe(true);
  });
});

describe('2010 Ordinary Project Maths Paper 2 — both complete Question 9 routes', () => {
  const cards=ORDINARY.filter(c=>c.id.startsWith('maths-2010-ol-p2-project-q'));
  const card=(suffix:string)=> {
    const c=cards.find(c=>c.id===`maths-2010-ol-p2-project-q${suffix}`);
    if(!c || c.kind!=='question') throw new Error(suffix);
    return c;
  };
  it('retains every task at the published holistic or component boundary', () => {
    expect(cards).toHaveLength(44);
    expect(cards.map(c=>c.id).sort()).toEqual(ordinary2010project2.cards.map(c=>c.id).sort());
    expect(cards.reduce((s,c)=>s+c.totalMarks,0)).toBe(345);
    expect(cards.reduce((s,c)=>s+(c.kind==='question'?(c.mathematicsScale?.methods?.[0].components.length??c.mathematicsScale?.components?.length??1):0),0)).toBe(47);
    expect(['1','2','3','4','5','6','7','8','9a','9b'].map(q=>cards.filter(c=>c.id.startsWith(`maths-2010-ol-p2-project-q${q}-`)).length)).toEqual([6,2,3,4,4,3,6,5,6,5]);
    for(const [q,marks] of Object.entries(ordinary2010project2.printedQuestionMarks)) expect(ordinary2010project2.cards.filter(c=>c.printedParts[0].match(/^Q(\d+[AB]?)/)![1]===q).reduce((s,c)=>s+c.totalMarks,0)).toBe(marks);
    expect(ordinary2010project2.paperPagesInspected).toEqual(Array.from({length:20},(_,i)=>i+1));
    expect(ordinary2010project2.schemePagesInspected).toEqual([3,4,...Array.from({length:34},(_,i)=>i+45)]);
    for(const suffix of ['4-a','5-a','7-e','9a-e']) expect(card(suffix).totalMarks).toBe(5);
    expect(card('9b-c').totalMarks).toBe(10);
  });
  it('retains the mixed 2010 marking systems and fourteen specific starred allowances', () => {
    expect(card('1-b-i').mathematicsScale?.methods?.[0].components.map(c=>[c.maximum,c.attempt])).toEqual([[10,3],[5,2]]);
    expect(card('2-a').mathematicsScale?.components?.map(c=>c.marks)).toEqual([[0,7,9,12,15],[0,3,4,5]]);
    expect(card('9b-b').mathematicsScale?.components?.map(c=>c.marks)).toEqual([[0,5],[0,3,5]]);
    expect(card('4-b-i').mathematicsScale?.marks).toEqual([0,8,10]);
    expect(card('4-b-i').mathematicsScale?.markingNote).toContain('19 or 21');
    expect(cards.filter(c=>c.kind==='question' && c.mathematicsScale?.fullCreditMinusOne).map(c=>c.id.split('-q')[1])).toEqual(['4-b-i','4-b-ii','6-a','6-b','6-c','7-a','7-b','8-b','8-c','8-d','9a-a','9b-a-i','9b-a-ii','9b-a-iii']);
  });
  it('preserves corrected source guidance without changing original diagrams or credit notes', () => {
    expect(29**2+44**2).toBe(2777);
    expect(card('9b-a-ii').figure?.sourceNote).toContain('2777');
    expect(card('9b-a-ii').figure?.sourceNote).toContain('277');
    expect(card('7-e').figure?.sourceNote).toBeUndefined();
    expect(card('7-e').mathematicsScale?.markingNote).toContain('total');
    expect(card('9a-e').mathematicsScale?.markingNote).toContain('±0.3');
    expect(card('9a-e').mathematicsScale?.markingNote).toContain('15.5 or 16');
    expect(card('5-a').stem).toContain('seven songs');
    expect(card('5-c').questionText).toContain('reason');
  });
  it('joins every exact paper task to Mark Bank and Topic Atlas with its own guidance pages', () => {
    const spec=resolveCurriculumSpecification('mathematics',2010)!;
    for(const task of ordinary2010project2.cards) {
      const c=card(task.id.split('-q')[1]);
      expect(findCanonicalTopic(spec,c.topicId)).toBeDefined();
      expect(c.topicId).toBe(task.topicId);
      expect(c.paperFileid).toBe('LC003GLP230EV');
      expect(c.sourceMaterial?.sourceFileid).toBe('LC003GLP230EV.pdf');
      expect(c.sourceMaterial?.pages).toEqual(task.sourcePages);
      expect(c.mathematicsScale?.schemeFileid).toBe('LC003GLP030EV.pdf');
      expect(c.mathematicsScale?.schemePages).toEqual(task.schemePages);
      expect(c.mathematicsScale?.generalNotesPages).toEqual(c.id.includes('-q1-')?[61,62]:[67,68]);
      expect(c.questionFigure?.src).toMatch(/maths-2010-OL-ask-p2-project-/);
      expect(c.figure?.solution).toBe(true);
      const q=task.printedParts[0].match(/^Q(\d+[AB]?)/)![1];
      expect(examTopicIdsForQuestion('mathematics','ordinary',2010,'main',q,'p2','ev',ordinary2010project2.paperFileid)).toEqual(expect.arrayContaining(task.examTopicIds));
    }
    for(const suffix of ['6-a','6-b','8-e','9b-b']) expect(card(suffix).sourceMaterial?.measurementRequired).toBe(true);
  });
});


describe('2010 Foundation Paper 1 — complete original tasks and deductions', () => {
  const cards=FOUNDATION.filter(c=>c.id.startsWith('maths-2010-fl-p1-q'));
  const card=(suffix: string) => {
    const c=cards.find(c=>c.id===`maths-2010-fl-p1-q${suffix}`);
    if (!c || c.kind!=='question' || !c.mathematicsScale?.methods) throw new Error(suffix);
    return c;
  };
  it('retains all 45 tasks, 49 components and all seven offered questions', () => {
    expect(cards).toHaveLength(45);
    expect(cards.map(c=>c.id).sort()).toEqual(foundation2010p1.cards.map(c=>c.id).sort());
    expect([1,2,3,4,5,6,7].map(n=>cards.filter(c=>c.id.startsWith(`maths-2010-fl-p1-q${n}-`)).length))
      .toEqual([10,8,5,5,7,5,5]);
    for (let n=1;n<=7;n++) expect(cards.filter(c=>c.id.startsWith(`maths-2010-fl-p1-q${n}-`)).reduce((sum,c)=>sum+c.totalMarks,0)).toBe(n===1?100:50);
    expect(foundation2010p1.cards.reduce((sum,c)=>sum+c.methods[0].components.length,0)).toBe(49);
    expect(foundation2010p1.paperPagesInspected).toEqual([1,2,3,4,5,6,7,8]);
    expect(foundation2010p1.schemePagesInspected).toEqual(Array.from({length:39},(_,i)=>i+1));
    expect(foundation2010p1.generalNotesPages).toEqual([4]);
  });
  it('preserves the compound-interest, simultaneous-equation and graph allocations', () => {
    expect(card('3-b').mathematicsScale?.methods?.[0].components.map(s=>[s.maximum,s.attempt])).toEqual([[10,4],[5,2],[5,2]]);
    expect(card('3-b').mathematicsScale?.schemePages).toEqual([21,22,23]);
    expect(card('3-b').mathematicsScale?.markingNote).toContain('€3397·10 earns all 20');
    expect(card('4-b').mathematicsScale?.methods?.[0].components.map(s=>[s.maximum,s.attempt])).toEqual([[15,6],[5,2]]);
    expect(card('4-b').mathematicsScale?.markingNote).toContain('6 + 2 only');
    expect(card('7-graph').mathematicsScale?.methods?.[0].components.map(s=>[s.maximum,s.attempt])).toEqual([[20,8],[10,4]]);
    expect(card('7-graph').mathematicsScale?.schemePages).toEqual([36,37,38]);
    expect(card('7-graph').mathematicsScale?.markingNote).toContain('earns all 30 marks');
  });
  it('retains formulae, complete charts and self-contained context in split tasks', () => {
    for (const suffix of ['3-b','5-b-i','5-b-ii']) expect(card(suffix).sourceMaterial?.pages).toEqual(suffix==='3-b'?[3,6]:[4,6]);
    for (const suffix of ['i','ii','iii','iv','v'] as const) {
      const regions=questionCropOverrides[`maths-2010-fl-p1-q6-${suffix}`].regions;
      expect(regions[0]).toMatchObject({page:5,top:45,bottom:305});
      expect(regions).toHaveLength(2);
    }
    expect(card('2-b-iii').stem).toContain('weekly tax credit is €72');
    expect(card('2-c-iii').stem).toContain('92 km/h');
    expect(card('5-c-iii').stem).toContain('5 adults and 4 children');
    expect(card('4-c-iii').mathematicsScale?.markingNote).toContain('All seven integers');
  });
  it('keeps graph-reading tolerances and special awards beside the original solutions', () => {
    for (const suffix of ['7-i','7-ii','7-iii','7-iv']) {
      expect(card(suffix).figure?.src).toBe(card('7-i').figure?.src);
      expect(card(suffix).mathematicsScale?.schemePages).toEqual([38,39]);
      expect(card(suffix).mathematicsScale?.markingNote).toContain('±0·3 on x and ±0·5 on y');
    }
    expect(card('7-i').figure?.sourceNote).toContain('−11·5');
    expect(card('7-ii').mathematicsScale?.markingNote).toContain('only the two attempt marks');
    expect(card('1-v').mathematicsScale?.markingNote).toContain('9 marks');
    expect(card('6-i').mathematicsScale?.markingNote).toContain('12 marks');
    expect(card('6-ii').mathematicsScale?.markingNote).toContain('seven marks');
    expect(card('2-a-i').figure?.src).toBe(card('2-a-ii').figure?.src);
    expect(card('5-a-i').figure?.src).toBe(card('5-a-ii').figure?.src);
  });
  it('binds every card to the correct original paper, canonical topic and Topic Atlas', () => {
    const spec=resolveCurriculumSpecification('mathematics',2010)!;
    for(const task of foundation2010p1.cards) {
      const c=card(task.id.split('-q')[1]);
      expect(findCanonicalTopic(spec,c.topicId)).toBeDefined();
      expect(c.paperFileid).toBe('LC003BLP100EV');
      expect(c.questionRef).toMatch(/^2010 FL Paper 1 /);
      expect(c.sourceMaterial?.sourceFileid).toBe('LC003BLP100EV.pdf');
      expect(c.sourceMaterial?.pages).toEqual(task.sourcePages);
      expect(c.mathematicsScale?.schemeFileid).toBe('LC003BLP000EV.pdf');
      expect(c.mathematicsScale?.methods).toEqual(task.methods);
      expect(c.mathematicsScale?.fullCreditMinusOne).toBe(false);
      expect(c.questionFigure?.src).toMatch(/maths-2010-FL-ask-p1-/);
      expect(c.figure?.solution).toBe(true);
      const q=task.printedParts[0].match(/^Q(\d+)/)![1];
      expect(examTopicIdsForQuestion('mathematics','foundation',2010,'main',q,'p1','ev',foundation2010p1.paperFileid)).toEqual(expect.arrayContaining(task.examTopicIds));
    }
  });
});


describe('2010 Foundation Paper 2 — complete original tasks and deductions', () => {
  const cards=FOUNDATION.filter(c=>c.id.startsWith('maths-2010-fl-p2-q'));
  const card=(suffix: string) => {
    const c=cards.find(c=>c.id===`maths-2010-fl-p2-q${suffix}`);
    if (!c || c.kind!=='question' || !c.mathematicsScale?.methods) throw new Error(suffix);
    return c;
  };
  it('retains all 51 tasks, 52 scoring components and all eight offered questions', () => {
    expect(cards).toHaveLength(51);
    expect(cards.map(c=>c.id).sort()).toEqual(foundation2010p2.cards.map(c=>c.id).sort());
    expect([1,2,3,4,5,6,7,8].map(n=>cards.filter(c=>c.id.startsWith(`maths-2010-fl-p2-q${n}-`)).length))
      .toEqual([4,5,8,7,5,9,6,7]);
    for(let n=1;n<=8;n++) expect(cards.filter(c=>c.id.startsWith(`maths-2010-fl-p2-q${n}-`)).reduce((sum,c)=>sum+c.totalMarks,0)).toBe(50);
    expect(foundation2010p2.cards.reduce((sum,c)=>sum+c.methods[0].components.length,0)).toBe(52);
    expect(foundation2010p2.paperPagesInspected).toEqual([1,2,3,4,5,6,7,8]);
    expect(foundation2010p2.schemePagesInspected).toEqual(Array.from({length:25},(_,i)=>i+40));
    expect(foundation2010p2.generalNotesPages).toEqual([42]);
  });
  it('preserves required paired outputs and exact published attempt floors', () => {
    expect(card('3-a').mathematicsScale?.methods?.[0].components.map(c=>[c.maximum,c.attempt])).toEqual([[5,2],[5,2]]);
    expect(card('4-a').totalMarks).toBe(15);
    expect(card('4-a').mathematicsScale?.methods?.[0].components).toHaveLength(1);
    expect(card('1-b-i').mathematicsScale?.methods?.[0].components[0]).toMatchObject({maximum:30,attempt:12});
    expect(card('2-c-i').mathematicsScale?.methods?.[0].components[0]).toMatchObject({maximum:15,attempt:6});
    expect(card('8-a-ii').mathematicsScale?.markingNote).toContain('Both axes');
    expect(card('8-c-ii').mathematicsScale?.markingNote).toContain('perpendicular bisectors');
  });
  it('preserves group-level probability deductions without inventing extra card marks', () => {
    for(const part of ['b','c']) for(const suffix of ['i','ii','iii','iv']) {
      const c=card(`6-${part}-${suffix}`);
      expect(c.totalMarks).toBe(5);
      expect(c.mathematicsScale?.markingNote).toContain('only once');
      expect(c.mathematicsScale?.markingNote).toContain('17/20');
      expect(c.mathematicsScale?.markingNote).toContain('group award');
      expect(c.figure?.src).toBe(card(`6-${part}-i`).figure?.src);
    }
    for(const suffix of ['i','ii','iii','iv']) {
      const regions=questionCropOverrides[`maths-2010-fl-p2-q6-c-${suffix}`].regions;
      expect(regions[0]).toMatchObject({page:5,top:613,bottom:718});
    }
  });
  it('keeps full graphs, transfer diagrams and smooth-curve interpretation', () => {
    expect(questionCropOverrides['maths-2010-fl-p2-q2-c-ii'].regions).toHaveLength(2);
    expect(card('2-c-ii').stem).toContain('diameter 9 cm and height 12 cm');
    for(const suffix of ['i','ii','iii','iv']) {
      expect(card(`7-b-${suffix}`).figure?.src).toBe(card('7-b-i').figure?.src);
      expect(card(`7-b-${suffix}`).mathematicsScale?.schemePages).toEqual([58]);
      expect(questionCropOverrides[`maths-2010-fl-p2-q7-b-${suffix}`].regions[0]).toMatchObject({page:6,top:112,bottom:247});
    }
    expect(card('7-b-iv').mathematicsScale?.markingNote).toContain('50 − 44 = 6');
    expect(card('8-b-iii').questionText).toContain('18 cm²');
  });
  it('binds every card to its correct source, canonical topic and exact-edition Atlas', () => {
    const spec=resolveCurriculumSpecification('mathematics',2010)!;
    for(const task of foundation2010p2.cards) {
      const c=card(task.id.split('-q')[1]);
      expect(findCanonicalTopic(spec,c.topicId)).toBeDefined();
      expect(c.paperFileid).toBe('LC003BLP200EV');
      expect(c.questionRef).toMatch(/^2010 FL Paper 2 /);
      expect(c.sourceMaterial?.sourceFileid).toBe('LC003BLP200EV.pdf');
      expect(c.sourceMaterial?.pages).toEqual(task.sourcePages);
      expect(c.mathematicsScale?.schemeFileid).toBe('LC003BLP000EV.pdf');
      expect(c.mathematicsScale?.methods).toEqual(task.methods);
      expect(c.mathematicsScale?.generalNotesPages).toEqual([42]);
      expect(c.mathematicsScale?.fullCreditMinusOne).toBe(false);
      expect(c.questionFigure?.src).toMatch(/maths-2010-FL-ask-p2-/);
      expect(c.figure?.solution).toBe(true);
      const q=task.printedParts[0].match(/^Q(\d+)/)![1];
      expect(examTopicIdsForQuestion('mathematics','foundation',2010,'main',q,'p2','ev',foundation2010p2.paperFileid)).toEqual(expect.arrayContaining(task.examTopicIds));
    }
  });
});

describe('2010 Foundation Project Paper 2 — all compulsory tasks and mixed marking rules', () => {
  const cards=FOUNDATION.filter(c=>c.id.startsWith('maths-2010-fl-p2-project-q'));
  const card=(suffix:string)=> {
    const c=cards.find(c=>c.id===`maths-2010-fl-p2-project-q${suffix}`);
    if(!c || c.kind!=='question') throw new Error(suffix);
    return c;
  };
  it('retains all 34 tasks and 300 marks at their published boundaries', () => {
    expect(cards).toHaveLength(34);
    expect(cards.map(c=>c.id).sort()).toEqual(foundation2010project2.cards.map(c=>c.id).sort());
    expect(cards.reduce((s,c)=>s+c.totalMarks,0)).toBe(300);
    expect([1,2,3,4,5,6,7,8].map(q=>cards.filter(c=>c.id.startsWith(`maths-2010-fl-p2-project-q${q}-`)).length)).toEqual([4,5,3,3,4,3,7,5]);
    for(const [q,marks] of Object.entries(foundation2010project2.printedQuestionMarks)) expect(foundation2010project2.cards.filter(c=>c.printedParts[0].match(/^Q(\d+)/)![1]===q).reduce((s,c)=>s+c.totalMarks,0)).toBe(marks);
    expect(foundation2010project2.paperPagesInspected).toEqual(Array.from({length:16},(_,i)=>i+1));
    expect(foundation2010project2.schemePagesInspected).toEqual([3,4,...Array.from({length:27},(_,i)=>i+40)]);
    expect(card('5-a').mathematicsScale?.marks).toEqual([0,4,8,10]);
    expect(card('6-a').mathematicsScale?.marks).toEqual([0,4,8,10]);
    expect(card('6-c').totalMarks).toBe(5);
    expect(card('6-c').mathematicsScale?.markingNote).toContain('Both distance calculations');
    expect(cards.filter(c=>c.section==='0')).toHaveLength(9);
    expect(cards.filter(c=>c.section==='A')).toHaveLength(13);
    expect(cards.filter(c=>c.section==='B')).toHaveLength(12);
  });
  it('keeps the exact historical deduction rules, bands and four starred allowances', () => {
    expect(card('1-b-i').mathematicsScale?.methods?.[0].components[0]).toMatchObject({maximum:30,attempt:12});
    expect(card('2-c-i').mathematicsScale?.methods?.[0].components[0]).toMatchObject({maximum:15,attempt:6});
    expect(card('3-a-ii').mathematicsScale?.marks).toEqual([0,2,4,5]);
    expect(card('7-b-iv').mathematicsScale?.marks).toEqual([0,3,5]);
    expect(card('7-b-iii').mathematicsScale?.marks).toEqual([0,6,10]);
    expect(cards.filter(c=>c.kind==='question' && c.mathematicsScale?.fullCreditMinusOne).map(c=>c.id.split('-q')[1])).toEqual(['8-a','8-b','8-c','8-d']);
  });
  it('makes the conflicting Q8(d) summary explicit and follows its detailed 10B rule', () => {
    expect(card('8-d').mathematicsScale?.code).toBe('10B');
    expect(card('8-d').mathematicsScale?.marks).toEqual([0,6,10]);
    expect(card('8-d').mathematicsScale?.fullCreditMinusOne).toBe(true);
    expect(card('8-d').figure?.sourceNote).toContain('summary table');
    expect(card('8-d').figure?.sourceNote).toContain('0, 6, 9 or 10');
    expect(card('8-d').mathematicsScale?.markingNote).toContain('detailed rule');
  });
  it('retains all dependent diagrams, data and supported evaluation answers', () => {
    expect(card('2-c-ii').stem).toContain('diameter 9 cm and height 12 cm');
    for(const suffix of ['a','b','c']) expect(questionCropOverrides[`maths-2010-fl-p2-project-q6-${suffix}`].regions[0]).toMatchObject({page:11,top:73,bottom:384});
    expect(questionCropOverrides['maths-2010-fl-p2-project-q8-d'].regions.map(r=>r.page)).toEqual([14,14,15,15]);
    expect(card('8-d').stem).toContain('scale factor 3/5');
    expect(card('7-b-iv').mathematicsScale?.markingNote).toContain('either the mean or median');
    for(const suffix of ['5-c','8-e']) expect(card(suffix).sourceMaterial?.measurementRequired).toBe(true);
  });
  it('joins every card to the exact paper edition in Mark Bank and Topic Atlas', () => {
    const spec=resolveCurriculumSpecification('mathematics',2010)!;
    for(const task of foundation2010project2.cards) {
      const c=card(task.id.split('-q')[1]);
      expect(findCanonicalTopic(spec,c.topicId)).toBeDefined();
      expect(c.topicId).toBe(task.topicId);
      expect(c.paperFileid).toBe('LC003BLP230EV');
      expect(c.sourceMaterial?.sourceFileid).toBe('LC003BLP230EV.pdf');
      expect(c.sourceMaterial?.pages).toEqual(task.sourcePages);
      expect(c.mathematicsScale?.schemeFileid).toBe('LC003BLP030EV.pdf');
      expect(c.mathematicsScale?.schemePages).toEqual(task.schemePages);
      expect(c.mathematicsScale?.generalNotesPages).toEqual(c.id.includes('-q1-')||c.id.includes('-q2-')?[53]:[58,59]);
      expect(c.questionFigure?.src).toMatch(/maths-2010-FL-ask-p2-project-/);
      expect(c.figure?.solution).toBe(true);
      const q=task.printedParts[0].match(/^Q(\d+)/)![1];
      expect(examTopicIdsForQuestion('mathematics','foundation',2010,'main',q,'p2','ev',foundation2010project2.paperFileid)).toEqual(expect.arrayContaining(task.examTopicIds));
    }
  });
});
