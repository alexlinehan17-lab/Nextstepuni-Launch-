/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 *
 * History StudyClix-reference parity, official-topic coverage, hosted-anchor
 * and preservation gates.
 */

import fs from 'node:fs';
import path from 'node:path';
import { describe, expect, it } from 'vitest';
import { CURRICULUM } from '../curriculum';
import historyReference from '../data/examTopics/history.json';
import historyCrosswalk from '../data/examTopics/history-local-crosswalk.json';
import { PAPER_TOPIC_TAGS } from '../data/paperTrail/topicTags';
import {
  browseTopicIdsForQuestion,
  subjectAtlasStats,
  topicsForPaper,
  topicsForSubject,
} from '../components/PaperTrail/topics';
import {
  curriculumNodeIdsForExamTopic,
  examQuestionPartReferencesForSubject,
  examTopicIdsForQuestion,
  examTopicTaxonomyFor,
} from '../data/examTopics/registry';
import { isAnswerMap } from '../components/PaperTrail/vaultResolve';
import preservationBaseline from './fixtures/historyTopicQuestionBaseline.json';

const ROOT = process.cwd();

const higherLabels = [
  '1.IRL Ireland and the Union',
  '2.IRL Movements for Political/Social Reform',
  '3.IRL Sovereignty and the Impact of Partition',
  '4.IRL The Irish Diaspora',
  '5.IRL Politics and Society in Northern Ireland',
  '6.IRL Republic - Government, Society, Economy',
  'EUR1. Nationalism and State Formation',
  'EUR2. Nation States and International Tensions',
  'EUR3. Dictatorship and Democracy',
  'EUR4. Division and Realignment',
  'EUR5. Retreat From Empire and the Aftermath',
  'EUR6. The United States and the World',
];

const ordinaryLabels = [
  '1. IRL Ireland and the Union',
  '2. IRL Movements for Political/Social Reform',
  '3. IRL Sovereignty and the Impact of Partition',
  '4.IRL The Irish Diaspora',
  '5.IRL Politics and Society in Northern Ireland',
  '6.IRL Republic - Government, Society, Economy',
  'EUR1. Nationalism and State Formation',
  'EUR2. Nation States and International Tensions',
  'EUR3. Dictatorship and Democracy',
  'EUR4. Division and Realignment',
  'EUR5. Retreat from Empire and the Aftermath',
  'EUR6. The United States and the World',
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
const crosswalk = historyCrosswalk;

describe('History exam-topic registry', () => {
  const taxonomy = examTopicTaxonomyFor('history')!;

  it('pins the exact twelve-topic Later Modern reference menu at both levels', () => {
    expect(taxonomy).not.toBeNull();
    expect(taxonomy.groups.map(group => [group.label, group.level])).toEqual([
      ['Higher Level', 'higher'],
      ['Ordinary Level', 'ordinary'],
    ]);
    expect(taxonomy.topics.filter(topic => topic.level === 'higher').map(topic => topic.label))
      .toEqual(higherLabels);
    expect(taxonomy.topics.filter(topic => topic.level === 'ordinary').map(topic => topic.label))
      .toEqual(ordinaryLabels);
    expect(topicsForSubject('history')).toHaveLength(24);
  });

  it('bridges each browse topic to its full official topic and three case studies', () => {
    const canonicalIds = new Set(
      CURRICULUM.flatMap(subject => subject.strands.flatMap(strand => strand.subtopics.map(topic => topic.id))),
    );
    const linkedIds = taxonomy.topics.flatMap(topic => {
      const ids = curriculumNodeIdsForExamTopic(topic.id);
      expect(ids, `${topic.id} must span one topic and three case studies`).toHaveLength(4);
      expect(ids.filter(id => !canonicalIds.has(id)), `${topic.id} has orphaned ids`).toEqual([]);
      return ids;
    });
    expect(linkedIds).toHaveLength(96);
    expect(new Set(linkedIds)).toHaveLength(48);
  });

  it('reconciles all 466 factual headings and records every official-source boundary', () => {
    expect(crosswalk.summary).toMatchObject({
      referenceHeadingAssociations: 466,
      matchedHeadingAssociations: 405,
      sourceBlockedHeadingAssociations: 59,
      referenceAnomalyAssociations: 2,
      matchedLocalCardLinks: 501,
      referenceMappedPrintedQuestions: 501,
    });
    expect(crosswalk.policy.excludedContent).toContain('No commercial mock question');

    const blocked = crosswalk.associations.filter(association => association.resolution === 'source-blocked');
    expect(new Set(blocked.map(association => association.year))).toEqual(
      new Set([2008, 2009, 2022, 2023]),
    );
    expect(blocked.every(association => (
      'reason' in association
      && association.reason.includes('official paper and marking scheme')
      && association.reason.includes('no StudyClix-hosted')
    ))).toBe(true);

    const anomalies = crosswalk.associations.filter(association => association.resolution === 'reference-anomaly');
    expect(anomalies.map(association => association.heading)).toEqual([
      '2024 - Section 3 - Question Alternative',
      '2010 - Section 3 - Question 5',
    ]);
    expect(crosswalk.associations.filter(association => 'correction' in association))
      .toHaveLength(1);
  });

  it('retains all headings as level-aware part metadata', () => {
    const references = examQuestionPartReferencesForSubject('history');
    expect(references).toHaveLength(562);
    expect(references.filter(reference => reference.level === 'higher')).toHaveLength(298);
    expect(references.filter(reference => reference.level === 'ordinary')).toHaveLength(264);
    expect(new Set(references.map(reference => (
      `${reference.level}|${reference.topicId}|${reference.subdivision}`
    )))).toHaveLength(466);
    expect(references.every(reference => reference.paperKey === 'single')).toBe(true);
  });

  it('preserves all 18 pre-migration variants and all 72 original cards', () => {
    expect(baseline).toHaveLength(18);
    expect(baseline.reduce((count, paper) => count + paper.questions.length, 0)).toBe(72);
    for (const expected of baseline) {
      const live = topicsForPaper(
        'history',
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

  it('adds every independently selectable official task without replacing a prior identity', () => {
    expect(crosswalk.summary).toMatchObject({
      localPaperVariants: 68,
      localQuestionMappings: 1028,
      distinctLocalQuestions: 514,
      referenceMappedLocalQuestions: 1002,
      retainedLocalQuestions: 26,
      preservedBaselinePaperVariants: 18,
      preservedBaselineCards: 72,
      addedLocalPaperVariants: 50,
      addedLocalCards: 956,
      hostedPaperAnchorMaps: 68,
    });

    const papers = PAPER_TOPIC_TAGS.filter(paper => paper.subjectId === 'history');
    expect(papers).toHaveLength(68);
    expect(papers.reduce((count, paper) => count + paper.q.length, 0)).toBe(1028);
    for (const paper of papers) {
      expect(paper.q.filter(question => /^[1-4]$/.test(question.n))).toHaveLength(4);
      expect(paper.q.filter(question => /^[IE][1-6]$/.test(question.n))).toHaveLength(11);
      const expectsAlternative = paper.level === 'ordinary' && paper.year >= 2023;
      expect(paper.q.filter(question => question.n === 'ALT')).toHaveLength(expectsAlternative ? 1 : 0);
      expect(paper.q).toHaveLength(expectsAlternative ? 16 : 15);
    }
  });

  it('classifies every local card into exactly one level-specific browse topic', () => {
    const validTopicIds = new Set(taxonomy.topics.map(topic => topic.id));
    const papers = PAPER_TOPIC_TAGS.filter(paper => paper.subjectId === 'history');
    for (const paper of papers) {
      for (const question of paper.q) {
        const topicIds = browseTopicIdsForQuestion(paper, question);
        expect(topicIds, `${paper.level}|${paper.lang}|${paper.year}|${question.n}`)
          .toHaveLength(1);
        expect(validTopicIds.has(topicIds[0])).toBe(true);
        expect(topicIds[0]).toContain(`-${paper.level}-`);
      }
    }
  });

  it('does not leak a Higher classification into the Ordinary paper', () => {
    expect(examTopicIdsForQuestion(
      'history', 'higher', 2025, 'main', 'I1', 'single', 'ev',
    )).toEqual(['history-higher-1irl-ireland-and-the-union']);
    expect(examTopicIdsForQuestion(
      'history', 'ordinary', 2025, 'main', 'I1', 'single', 'ev',
    )).toEqual(['history-ordinary-1-irl-ireland-and-the-union']);
  });

  it('keeps official local tasks omitted or misclassified by the reference menu', () => {
    expect(examTopicIdsForQuestion(
      'history', 'ordinary', 2024, 'main', 'ALT', 'single', 'ev',
    )).toEqual(['history-ordinary-eur3-dictatorship-and-democracy']);
    expect(examTopicIdsForQuestion(
      'history', 'ordinary', 2026, 'main', 'ALT', 'single', 'ev',
    )).toEqual(['history-ordinary-2-irl-movements-for-politicalsocial-reform']);
    expect(examTopicIdsForQuestion(
      'history', 'ordinary', 2023, 'main', 'ALT', 'single', 'iv',
    )).toEqual(['history-ordinary-5irl-politics-and-society-in-northern-ireland']);
    expect(examTopicIdsForQuestion(
      'history', 'ordinary', 2025, 'main', 'ALT', 'single', 'ev',
    )).toEqual(['history-ordinary-eur3-dictatorship-and-democracy']);
    expect(examTopicIdsForQuestion(
      'history', 'ordinary', 2010, 'main', 'I6', 'single', 'ev',
    )).toEqual(['history-ordinary-6irl-republic-government-society-economy']);
  });

  it('ships a complete paper-only anchor map for every new topic-block card', () => {
    const papers = PAPER_TOPIC_TAGS.filter(paper => paper.subjectId === 'history');
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
      const expectedNumbers = paper.q
        .filter(question => /^(?:[IE][1-6]|ALT)$/.test(question.n))
        .map(question => question.n);
      expect(anchorMap.q.map((question: { n: string }) => question.n)).toEqual(expectedNumbers);
      expect(anchorMap.q.every((question: { mode: string }) => question.mode === 'pagejump'))
        .toBe(true);
    }
  });

  it('surfaces all 514 distinct tasks through the 24-topic menu', () => {
    expect(subjectAtlasStats('history')).toMatchObject({
      questions: 514,
      topics: 24,
      yearMin: 2010,
      yearMax: 2026,
    });
    expect(taxonomy.topics.reduce((count, topic) => count + topic.mockQuestionCount, 0))
      .toBe(455);
    expect(Object.values(historyReference.levels)
      .flatMap(level => level.topics)
      .reduce((count, topic) => count + topic.officialQuestionHeadings.length, 0))
      .toBe(466);
  });
});
