/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 *
 * Economics reference-taxonomy parity, complete SEC task coverage, hosted
 * anchor, canonical curriculum, and card-preservation gates.
 */

import fs from 'node:fs';
import path from 'node:path';
import { describe, expect, it } from 'vitest';
import { CURRICULUM } from '../curriculum';
import economicsReference from '../data/examTopics/economics.json';
import economicsCrosswalk from '../data/examTopics/economics-local-crosswalk.json';
import curriculumCrosswalk from '../data/examTopics/economics-curriculum-crosswalk.json';
import { PAPER_TOPIC_TAGS } from '../data/paperTrail/topicTags';
import {
  browseTopicIdsForQuestion,
  subjectAtlasStats,
  topicsForPaper,
  topicsForSubject,
} from '../components/PaperTrail/topics';
import { paperRegionFor } from '../components/PaperTrail/paperRegion';
import { isAnswerMap } from '../components/PaperTrail/vaultResolve';
import {
  curriculumNodeIdsForExamTopic,
  examQuestionPartReferencesForSubject,
  examTopicIdsForQuestion,
  examTopicTaxonomyFor,
} from '../data/examTopics/registry';
import preservationBaseline from './fixtures/economicsTopicQuestionBaseline.json';

const ROOT = process.cwd();

const higherLabels = [
  '1.1 Economic Concepts',
  '1.2 Sustainability',
  '2.1 The Market Economy',
  '2.2 Elasticity',
  '2.3 Costs of Production, Revenue & Profit',
  '2.4 Government Intervention',
  '3.1 Market Structures',
  '3.2 The Labour Market',
  '3.3 Market Failure',
  '4.1 National Income',
  '4.2 Fiscal Policy and the Budget Framework',
  '4.3 Employment',
  '4.4 Monetary Policy and Price Level',
  '4.5 The Financial Sector',
  '5.1 Economic Growth and Development',
  '5.2 Globalisation',
  '5.3 International Trade and Competitiveness',
  '6.1 Topical Questions and Statistics',
  'Research Project',
];

const ordinaryLabels = [
  '1.1 Economics as a Way of Thinking',
  '1.2 The Economic Concepts of Scarcity and Choice',
  '1.3 Sustainability',
  '2.1 The Market Economy',
  '2.2 Elasticity',
  '2.3 Costs of Production, Revenue & Profit',
  '2.4 Government Intervention',
  '3.1 Market Structures',
  '3.2 The Labour Market',
  '3.3 Market Failure',
  '4.1 National Income',
  '4.2 Fiscal Policy & the Budget Framework',
  '4.3 Employment',
  '4.4 Monetary Policy & the Price Level',
  '4.5 The Financial Sector',
  '5.1 Economic Growth & Development',
  '5.2 Globalisation',
  '5.3 International Trade & Competitiveness',
  'Acronyms',
  'Formulas',
  'Research Project',
];

type Baseline = Array<{
  level: 'higher' | 'ordinary';
  lang: 'ev' | 'iv';
  year: number;
  fileid: string;
  paperKey: string;
  questions: string[];
}>;

const baseline = preservationBaseline as Baseline;
const evidence = economicsCrosswalk;

describe('Economics exam-topic registry', () => {
  const taxonomy = examTopicTaxonomyFor('economics')!;

  it('pins the exact flat reference hierarchy independently at each level', () => {
    expect(taxonomy).not.toBeNull();
    expect(taxonomy.groups.map(group => [group.label, group.level])).toEqual([
      ['Higher Level', 'higher'],
      ['Ordinary Level', 'ordinary'],
    ]);
    expect(taxonomy.topics.filter(topic => topic.level === 'higher').map(topic => topic.label))
      .toEqual(higherLabels);
    expect(taxonomy.topics.filter(topic => topic.level === 'ordinary').map(topic => topic.label))
      .toEqual(ordinaryLabels);
    expect(topicsForSubject('economics')).toHaveLength(40);
  });

  it('bridges every practice bucket only to canonical NCCA Economics nodes', () => {
    const subject = CURRICULUM.find(item => item.id === 'economics')!;
    const canonicalIds = new Set(
      subject.strands.flatMap(strand => strand.subtopics.map(topic => topic.id)),
    );
    expect(canonicalIds.size).toBe(21);
    expect(Object.keys(curriculumCrosswalk)).toHaveLength(40);
    for (const topic of taxonomy.topics) {
      const ids = curriculumNodeIdsForExamTopic(topic.id);
      expect(ids).toEqual(curriculumCrosswalk[topic.id as keyof typeof curriculumCrosswalk]);
      expect(ids.length, topic.id).toBeGreaterThan(0);
      expect(ids.filter(id => !canonicalIds.has(id)), `${topic.id} has orphaned ids`).toEqual([]);
    }
  });

  it('reconciles every factual association and records each source boundary', () => {
    expect(evidence.summary).toMatchObject({
      referenceTopics: 40,
      referenceReportedAssociations: 1851,
      referenceOfficialAssociations: 1120,
      referenceMockAssociations: 731,
      // 903 headings resolve to a local paper question; 93 of them are
      // contradicted by the SEC-paper topic review (economics-sec-topic-
      // reviews.json, each with its reason) and are recorded as reference
      // anomalies rather than matches. Card tags are unchanged. The 2019
      // Higher review (2026-11-04) added five: Section A Q3 (development and
      // growth, not monetary policy), Q9 (not Government Intervention),
      // Section B Q4(c) twice (skills shortages are the labour market) and
      // Q6 (inflation and competitiveness, not globalisation). The 2019
      // Ordinary review added seven: Section A Q1 (acronyms, a study-aid
      // heading with no syllabus node), Q3 (the factors of production, not the
      // labour market), Q8 (scarcity, not Government Intervention), Section B
      // Q4 (international trade, not globalisation), Q5(b)-(c) twice (interest
      // rates and post-office closures, neither globalisation nor a formula)
      // and Q6 (taxation and the Budget, not Government Intervention). The 2020
      // Higher review added eight: Section A Q3 and Section B Q3 under
      // Government Intervention (unemployment policy; employment, MNCs and the
      // pay gap), Section B Q5(a)-(b) under employment (enterprise and the
      // marginal revenue product of labour), Section B Q8 under economic
      // concepts (national income terms), and four topical-questions headings
      // (Section A Q5, Q7 and Q8 and Section B Q1(c)), a heading no syllabus
      // node falls back to. The 2018 Higher review added seven: Section A Q4
      // under economic concepts (diminishing returns are costs), Q7 under
      // globalisation (income inequality), Section B Q6(a)-(b) under the
      // financial sector (migration and the single market), Q7(a) under
      // topical questions, Q8(b) under government intervention and under
      // growth and development (FDI is globalisation), and Q8(c) under
      // government intervention (the environment is sustainability). The 2018
      // Ordinary review added sixteen, among them Section A Q1 and Q6 under
      // acronyms and Section B Q6(a) under formulas (study-aid headings), and
      // Section B Q4(b)-(c), Q5(a) and (c) and Q7(b) under national income
      // (savings, the budget and visible trade are filed under their own
      // topics); each is recorded with the review's reason. The 2017 Higher
      // review added three: Section A Q1 and Q9 under government intervention
      // (public pay and third-level fees are fiscal policy) and Section B Q8(c)
      // under topical questions. The 2017 Ordinary review added thirteen:
      // Section A Q1 and Q5 and Section B Q8(a) under acronyms and Section B
      // Q2(c) and Q5(a) under formulas (study-aid headings); Section A Q3 and
      // Q6 and Section B Q3(b)-(c), Q5(b) and Q7(c) under government
      // intervention (cross-border shopping, third-level spending, public pay
      // and emigration, the circular flow and Brexit are filed under their own
      // topics); Section A Q3 under growth and development; and Section A Q4
      // and Section B Q6(a)-(b) under globalisation (visible trade is
      // international trade, the current budget fiscal policy). The 2016
      // Higher review added five: Section A Q5(a) and (b) under government
      // intervention (youth unemployment is employment), Q5(b) under national
      // income, Q4 under market structures (economies of scale are costs) and
      // Q9 under fiscal policy (the minimum wage is the labour market). The
      // 2016 Ordinary review added nine: Section B Q6 and Q7 under acronyms
      // and Section A Q4 and Q9 and Section B Q7 under formulas (study-aid
      // headings); Section A Q1 under the labour market (land is a factor of
      // production), Q2 under globalisation (protection is international
      // trade), Q8 under government intervention (the black economy is
      // national income) and Section B Q3 under growth and development (the
      // minimum wage and conferences are filed under their own topics). The
      // 2015 Higher review added one: Section A Q9 under government
      // intervention (an ageing population's pension and retirement policy is
      // fiscal policy and the labour market). The 2015 Ordinary review added
      // eleven: Section A Q6, Section B Q4(b) and Section B Q6 under acronyms
      // and Section B Q8 under formulas (study-aid headings); Section A Q1
      // under the labour market (land is a factor of production); Section A
      // Q4 and Section B Q5 under globalisation (visible trade and the
      // exchange rate are international trade); Section A Q3 under government
      // intervention (corporation tax is fiscal policy); Section A Q8 under
      // government intervention and under growth and development (emigration
      // is employment and unemployment); and Section B Q6 under national
      // income (the current budget is fiscal policy). The 2014 Higher review
      // added none. The 2014 Ordinary review added fifteen: Section A Q5 and
      // Q9 under formulas and Section B Q6, Q7 and Q8(b)-(c) under acronyms
      // (study-aid headings); Section A Q1 under the market economy (the
      // definition of economics is scarcity and choice); Section A Q4 and Q7
      // under government intervention (public sector pay and a tax relief are
      // fiscal policy); Section B Q3 under government intervention (economic
      // systems are the market economy, as earlier reviews file them);
      // Section B Q7 under government intervention (tariffs and quotas are
      // international trade, the EU globalisation); Section B Q8(b)-(c) under
      // government intervention and globalisation (unemployment is employment,
      // the government's aims fiscal policy); Section B Q5 under the labour
      // market (costs, the entrepreneur and location are filed under their own
      // topics); Section B Q8(a) under growth and development (emigration is
      // employment and unemployment); and Section A Q2 under globalisation
      // (visible and invisible trade are international trade). The 2013
      // Higher review added six: Section A Q9 and Section B Q8(b) and Q8(c)
      // under topical questions and statistics (a study-aid heading);
      // Section A Q8 under costs of production (the APC is national income);
      // and Section B Q8(a) and Q8(b) under government intervention (youth
      // unemployment is employment and unemployment, the national debt
      // fiscal policy). The 2013 Ordinary review added eleven: Section A Q6
      // under formulas and Section B Q4, Q7 and Q8 under acronyms (study-aid
      // headings); Section A Q1 and Q6 under the labour market (the factors
      // of production are scarcity and choice, the sofas' costs costs of
      // production); Section A Q9 and Section B Q5(a)-(b) under growth and
      // development (infrastructure is fiscal policy, the circular flow and
      // consumer spending national income); Section B Q3 and Q5(a)-(b) under
      // government intervention (labour and the public sector are filed under
      // their own topics); and Section B Q5(c) under globalisation (the black
      // economy is national income). The 2012 Higher review added six:
      // Section A Q3 under employment (the black economy is national
      // income); Section A Q7 under national income (savings are the
      // financial sector); Section A Q9 under government intervention (the
      // household charge is fiscal policy); Section B Q3(b) under economic
      // growth and development (entrepreneurship is scarcity and choice) and
      // Q3(c) under costs of production (the survival of small firms is
      // market structures); and Section B Q8(b) under national income (the
      // Live Register is employment and unemployment). The 2012 Ordinary
      // review added nine: Section A Q5 and Section B Q4 and Q8 under
      // acronyms and Section B Q5 under formulas (study-aid headings);
      // Section A Q4, Section B Q5 and Q7(c) under government intervention
      // (austerity is fiscal policy, national income and the multiplier are
      // national income, multinationals are globalisation); Section B Q5
      // under employment (its national income terms are filed under their
      // own topic); and Section A Q8 under economic growth and development
      // (emigration is employment and unemployment). The 2011 Higher review
      // added two: Section A Q2 under government intervention (a mixed
      // economy is the market economy, as earlier reviews file economic
      // systems) and Section A Q7 under international trade (multinationals
      // re-locating are globalisation). The 2011 Ordinary review added
      // eleven: Section A Q1 and Section B Q5 and Q8 under acronyms and
      // Section A Q9 and Section B Q6 under formulas (study-aid headings);
      // Section A Q6 under the market economy (an economic good is scarcity
      // and choice); Section A Q8 and Section B Q5 and Q8 under government
      // intervention (the government's aims, the budget and the retirement
      // age are fiscal policy); and Section A Q5 and Section B Q4 under
      // globalisation (barriers to trade and tourism are international
      // trade).
      matchedAssociations: 677,
      referenceAnomalyAssociations: 226,
      sourceBlockedAssociations: 217,
      matchedLogicalCards: 517,
      matchedQuestionTopicLinks: 603,
      retainedLocalLogicalCards: 32,
    });
    expect(evidence.policy.excludedCommercialContent).toContain('Question text');

    const blocked = evidence.associations.filter(association => association.resolution === 'source-blocked');
    expect(new Set(blocked.map(association => association.year))).toEqual(
      new Set([2006, 2007, 2008, 2009, 2020, 2022]),
    );
    expect(new Set(blocked.map(association => association.sitting))).toEqual(
      new Set(['main', 'sample', 'deferred']),
    );
    expect(blocked.every(association => (
      'reason' in association && association.reason.includes('no StudyClix-hosted')
    ))).toBe(true);
    expect(evidence.summary.emptyReferenceTopics).toEqual([
      'economics-higher-research-project',
      'economics-ordinary-44-monetary-policy-the-price-level',
      'economics-ordinary-research-project',
    ]);
  });

  it('retains all 1,120 headings as level- and sitting-aware part metadata', () => {
    const references = examQuestionPartReferencesForSubject('economics');
    expect(references).toHaveLength(1120);
    expect(references.filter(reference => reference.level === 'higher')).toHaveLength(602);
    expect(references.filter(reference => reference.level === 'ordinary')).toHaveLength(518);
    expect(new Set(references.map(reference => (
      `${reference.level}|${reference.topicId}|${reference.subdivision}`
    )))).toHaveLength(1120);
    expect(references.every(reference => reference.paperKey === 'single')).toBe(true);
  });

  it('preserves all 26 pre-migration variants and all 304 original cards', () => {
    expect(baseline).toHaveLength(26);
    expect(baseline.reduce((count, paper) => count + paper.questions.length, 0)).toBe(304);
    for (const expected of baseline) {
      const live = topicsForPaper(
        'economics',
        expected.year,
        expected.level,
        expected.lang,
        expected.fileid,
      );
      expect(live, `${expected.level}|${expected.lang}|${expected.year}|${expected.fileid}`)
        .not.toBeNull();
      expect(live!.paperKey).toBe(expected.paperKey);
      expect(live!.q.map(question => question.n)).toEqual(expect.arrayContaining(expected.questions));
    }
  });

  it('exposes all old Section-B tasks and every new-format question', () => {
    expect(evidence.summary).toMatchObject({
      localPaperVariants: 66,
      localPhysicalMappings: 1098,
      distinctStudentFacingQuestions: 549,
      hostedAnchorMaps: 54,
      preservedBaselineVariants: 26,
      preservedBaselineCards: 304,
    });
    const papers = PAPER_TOPIC_TAGS.filter(paper => paper.subjectId === 'economics');
    expect(papers).toHaveLength(66);
    expect(papers.reduce((count, paper) => count + paper.q.length, 0)).toBe(1098);
    for (const paper of papers) {
      const expected = paper.year <= 2020
        ? [...Array.from({ length: 9 }, (_, i) => String(i + 1)), ...Array.from({ length: 8 }, (_, i) => `B${i + 1}`)]
        : Array.from({ length: 16 }, (_, i) => String(i + 1));
      expect(paper.q.map(question => question.n), `${paper.level}|${paper.lang}|${paper.year}`)
        .toEqual(expected);
    }
  });

  it('classifies every physical card into one or more same-level practice buckets', () => {
    const valid = new Map(taxonomy.topics.map(topic => [topic.id, topic.level]));
    const papers = PAPER_TOPIC_TAGS.filter(paper => paper.subjectId === 'economics');
    for (const paper of papers) {
      for (const question of paper.q) {
        const topicIds = browseTopicIdsForQuestion(paper, question);
        expect(topicIds.length, `${paper.level}|${paper.lang}|${paper.year}|${question.n}`)
          .toBeGreaterThan(0);
        expect(topicIds.every(topicId => valid.get(topicId) === paper.level)).toBe(true);
      }
    }
  });

  it('keeps exact multi-topic joins and reviewed reference omissions', () => {
    expect(examTopicIdsForQuestion(
      'economics', 'higher', 2026, 'main', '1', 'single', 'ev',
    )).toEqual([
      'economics-higher-11-economic-concepts',
      'economics-higher-53-international-trade-and-competitiveness',
    ]);
    expect(examTopicIdsForQuestion(
      'economics', 'ordinary', 2025, 'main', '1', 'single', 'iv',
    )).toEqual(['economics-ordinary-11-economics-as-a-way-of-thinking']);
    expect(examTopicIdsForQuestion(
      'economics', 'higher', 2010, 'main', '1', 'single', 'ev',
    )).toEqual(['economics-higher-21-the-market-economy']);
    expect(examTopicIdsForQuestion(
      'economics', 'ordinary', 2010, 'main', 'B6', 'single', 'ev',
    )).toEqual([
      'economics-ordinary-45-the-financial-sector',
      'economics-ordinary-44-monetary-policy-the-price-level',
    ]);
    expect(examTopicIdsForQuestion(
      'economics', 'ordinary', 2019, 'main', 'B8', 'single', 'iv',
    )).toEqual([
      'economics-ordinary-51-economic-growth-development',
      'economics-ordinary-43-employment',
    ]);
  });

  it('ships complete hosted anchors wherever the classic map cannot address a card', () => {
    const papers = PAPER_TOPIC_TAGS.filter(paper => (
      paper.subjectId === 'economics' && (paper.year <= 2020 || (paper.year === 2025 && paper.level === 'higher'))
    ));
    expect(papers).toHaveLength(44);
    for (const paper of papers) {
      const anchorPath = path.join(
        ROOT,
        'public',
        'paper-anchors',
        String(paper.year),
        `${paper.fileid}.json`,
      );
      expect(fs.existsSync(anchorPath), anchorPath).toBe(true);
      const anchorMap = JSON.parse(fs.readFileSync(anchorPath, 'utf8'));
      expect(isAnswerMap(anchorMap), anchorPath).toBe(true);
      expect(anchorMap.paperOnly).toBe(1);
      expect(anchorMap.q.map((question: { n: string }) => question.n))
        .toEqual(paper.q.map(question => question.n));
      expect(anchorMap.q.every((question: { mode: string }) => question.mode === 'pagejump'))
        .toBe(true);
      for (const question of anchorMap.q) {
        expect(
          paperRegionFor(anchorMap.q, question.n, anchorMap.maxCropPages ?? 3),
          `${anchorPath} Q${question.n}`,
        ).not.toBeNull();
      }
    }
  });

  it('surfaces all 549 entitled tasks through the 40-topic menu', () => {
    expect(subjectAtlasStats('economics')).toMatchObject({
      questions: 549,
      topics: 40,
      yearMin: 2010,
      yearMax: 2026,
    });
    expect(taxonomy.topics.reduce((count, topic) => count + topic.mockQuestionCount, 0))
      .toBe(731);
    expect(Object.values(economicsReference.levels)
      .flatMap(level => level.topics)
      .reduce((count, topic) => count + topic.officialQuestionHeadings.length, 0))
      .toBe(1120);
  });
});
