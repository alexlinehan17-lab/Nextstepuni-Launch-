/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 *
 * Religious Education StudyClix-reference parity, official-section coverage,
 * hosted-anchor and preservation gates.
 */

import fs from 'node:fs';
import path from 'node:path';
import { describe, expect, it } from 'vitest';
import { CURRICULUM } from '../curriculum';
import religiousEducationReference from '../data/examTopics/religious-education.json';
import religiousEducationCrosswalk from '../data/examTopics/religious-education-local-crosswalk.json';
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
import { isAnswerMap, VAULT_PREFER_ANCHORS } from '../components/PaperTrail/vaultResolve';
import preservationBaseline from './fixtures/religiousEducationTopicQuestionBaseline.json';

const ROOT = process.cwd();

const higherLabels = [
  'A. The Search for Meaning & Values',
  'B. Christianity',
  'C. World Religions',
  'D. Moral Decision-Making',
  'E. Religion & Gender',
  'F. Issues of Justice & Peace',
  'G. Worship, Prayer & Ritual',
  'H. The Bible',
  'I. Religion: The Irish Experience',
  'J. Religion & Science',
];

const ordinaryLabels = [
  'A. The Search for Meaning & Values',
  'B. Christianity',
  'C. World Religions',
  'D. Moral Decision-Making',
  'E. Religion & Gender',
  'F: Issues of Justice & Peace',
  'G: Worship, Prayer & Ritual',
  'H: The Bible',
  'I: Religion: The Irish Experience',
  'J: Religion & Science',
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
const crosswalk = religiousEducationCrosswalk;

describe('Religious Education exam-topic registry', () => {
  const taxonomy = examTopicTaxonomyFor('religious-education')!;

  it('pins the exact ten-topic reference menu at both levels', () => {
    expect(taxonomy).not.toBeNull();
    expect(taxonomy.groups.map(group => [group.label, group.level])).toEqual([
      ['Higher Level', 'higher'],
      ['Ordinary Level', 'ordinary'],
    ]);
    expect(taxonomy.topics.filter(topic => topic.level === 'higher').map(topic => topic.label))
      .toEqual(higherLabels);
    expect(taxonomy.topics.filter(topic => topic.level === 'ordinary').map(topic => topic.label))
      .toEqual(ordinaryLabels);
    expect(topicsForSubject('religious-education')).toHaveLength(20);
  });

  it('bridges every browse section to the complete official syllabus section', () => {
    const canonicalIds = new Set(
      CURRICULUM.flatMap(subject => subject.strands.flatMap(strand => strand.subtopics.map(topic => topic.id))),
    );
    for (const topic of taxonomy.topics) {
      const ids = curriculumNodeIdsForExamTopic(topic.id);
      expect(ids.length, `${topic.id} has no curriculum crosswalk`).toBeGreaterThan(0);
      expect(ids.filter(id => !canonicalIds.has(id)), `${topic.id} has orphaned ids`).toEqual([]);
    }
    expect(curriculumNodeIdsForExamTopic(
      'religious-education-higher-c-world-religions',
    )).toHaveLength(12);
  });

  it('reconciles all 366 factual official headings and records the source boundary', () => {
    expect(crosswalk.summary).toMatchObject({
      referenceHeadingAssociations: 366,
      matchedHeadingAssociations: 276,
      sourceBlockedHeadingAssociations: 90,
      matchedLocalCardLinks: 276,
      referenceMappedPrintedQuestions: 238,
    });
    expect(crosswalk.policy.granularity).toContain('complete printed Section A');
    expect(crosswalk.policy.excludedContent).toContain('No commercial mock question');

    const blocked = crosswalk.associations.filter(association => association.resolution === 'source-blocked');
    expect(new Set(blocked.map(association => association.year))).toEqual(
      new Set([2006, 2007, 2008, 2009, 2013]),
    );
    expect(blocked.every(association => (
      'reason' in association
      && association.reason.includes('official SEC paper and marking scheme')
      && association.reason.includes('no StudyClix-hosted')
    ))).toBe(true);
  });

  it('retains each reference heading as level-aware part metadata', () => {
    const references = examQuestionPartReferencesForSubject('religious-education');
    expect(references).toHaveLength(366);
    expect(references.filter(reference => reference.level === 'higher')).toHaveLength(187);
    expect(references.filter(reference => reference.level === 'ordinary')).toHaveLength(179);
    expect(new Set(references.map(reference => (
      `${reference.level}|${reference.topicId}|${reference.subdivision}`
    )))).toHaveLength(366);

    const higher2026SectionA = references.filter(reference => (
      reference.level === 'higher'
      && reference.year === 2026
      && reference.topicId === 'religious-education-higher-a-the-search-for-meaning-values'
    ));
    expect(higher2026SectionA).toHaveLength(2);
    expect(new Set(higher2026SectionA.map(reference => reference.n))).toEqual(new Set(['1']));
  });

  it('preserves every one of the 23 pre-migration variants and 69 cards', () => {
    expect(baseline).toHaveLength(23);
    expect(baseline.reduce((count, paper) => count + paper.questions.length, 0)).toBe(69);
    for (const expected of baseline) {
      const live = topicsForPaper(
        'religious-education',
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

  it('adds every locally verified paper section without sacrificing prior identity', () => {
    expect(crosswalk.summary).toMatchObject({
      localPaperVariants: 58,
      localQuestionMappings: 464,
      distinctLocalQuestions: 248,
      referenceMappedLocalQuestions: 444,
      retainedLocalQuestions: 20,
      preservedBaselinePaperVariants: 23,
      preservedBaselineCards: 69,
      addedLocalPaperVariants: 35,
      addedLocalCards: 395,
      hostedPaperAnchorMaps: 58,
    });

    const papers = PAPER_TOPIC_TAGS.filter(paper => paper.subjectId === 'religious-education');
    expect(papers).toHaveLength(58);
    expect(papers.reduce((count, paper) => count + paper.q.length, 0)).toBe(464);
    expect(papers.every(paper => paper.q.length === 8)).toBe(true);
  });

  it('classifies every local card into exactly one level-specific section', () => {
    const validTopicIds = new Set(taxonomy.topics.map(topic => topic.id));
    const papers = PAPER_TOPIC_TAGS.filter(paper => paper.subjectId === 'religious-education');
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

  it('never leaks a Higher classification into the Ordinary paper', () => {
    expect(examTopicIdsForQuestion(
      'religious-education', 'higher', 2025, 'main', '5', 'single', 'ev',
    )).toEqual(['religious-education-higher-f-issues-of-justice-peace']);
    expect(examTopicIdsForQuestion(
      'religious-education', 'ordinary', 2025, 'main', '5', 'single', 'ev',
    )).toEqual(['religious-education-ordinary-f-issues-of-justice-peace']);
  });

  it('keeps official local sections omitted from the reference pages', () => {
    expect(examTopicIdsForQuestion(
      'religious-education', 'ordinary', 2021, 'main', '1', 'single', 'ev',
    )).toEqual(['religious-education-ordinary-a-the-search-for-meaning-values']);
    expect(examTopicIdsForQuestion(
      'religious-education', 'higher', 2014, 'main', '8', 'single', 'iv',
    )).toEqual(['religious-education-higher-h-the-bible']);
    expect(examTopicIdsForQuestion(
      'religious-education', 'ordinary', 2015, 'main', '8', 'single', 'ev',
    )).toEqual(['religious-education-ordinary-j-religion-science']);
  });

  it('ships a matching paper-only anchor map for every local variant', () => {
    const prefer = VAULT_PREFER_ANCHORS.get('religious-education');
    expect(prefer).toBeDefined();
    const papers = PAPER_TOPIC_TAGS.filter(paper => paper.subjectId === 'religious-education');
    for (const paper of papers) {
      expect(prefer!(paper.fileid)).toBe(true);
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
    }
  });

  it('surfaces 248 distinct section cards through the 20-topic menu', () => {
    expect(subjectAtlasStats('religious-education')).toMatchObject({
      questions: 248,
      topics: 20,
      yearMin: 2010,
      yearMax: 2026,
    });
    expect(taxonomy.topics.reduce((count, topic) => count + topic.mockQuestionCount, 0))
      .toBe(304);
    expect(Object.values(religiousEducationReference.levels)
      .flatMap(level => level.topics)
      .reduce((count, topic) => count + topic.officialQuestionHeadings.length, 0))
      .toBe(366);
  });
});
