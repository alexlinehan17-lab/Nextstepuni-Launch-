/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 *
 * Japanese StudyClix-reference parity, source-boundary and preservation gates.
 */

import { readFileSync } from 'node:fs';
import { resolve } from 'node:path';
import { describe, expect, it } from 'vitest';
import { CURRICULUM } from '../curriculum';
import { PAPER_TOPIC_TAGS } from '../data/paperTrail/topicTags';
import japaneseCrosswalkJson from '../data/examTopics/japanese-local-crosswalk.json';
import japaneseBaselineJson from './fixtures/japaneseTopicQuestionBaseline.json';
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

const topicLabels = [
  'AURAL - Conversation',
  'Aural - Interview/Speech',
  'Aural - Radio/News',
  'Comprehension (General Reading)',
  'Comprehension (Website)',
  'Grammar',
  'Kanji',
  'ORAL Exam',
  'Personal Writing (All)',
  'Translation (Japanese to English)',
  'Writing – Holidays Abroad & Events',
  'Writing – Home & Ireland',
  'Writing – Me & My Family',
  'Writing – School, Studying Japanese & Future Plans',
];

type Baseline = Array<{
  level: 'higher' | 'ordinary';
  lang: 'ev' | 'iv';
  year: number;
  fileid: string;
  paperKey: string;
  questions: string[];
}>;

type MatchedAssociation = {
  topicId: string;
  heading: string;
  year: number;
  resolution: 'matched';
  target: {
    level: 'higher';
    lang: 'ev';
    paperKey: string;
    fileid: string;
    questionNumbers: string[];
  };
};

const crosswalk = japaneseCrosswalkJson;
const baseline = japaneseBaselineJson as Baseline;

describe('Japanese exam-topic registry', () => {
  const taxonomy = examTopicTaxonomyFor('japanese')!;

  it('pins the exact fourteen-topic Common Level reference menu', () => {
    expect(taxonomy).not.toBeNull();
    expect(taxonomy.groups.map(group => group.label)).toEqual(['Common Level']);
    expect(taxonomy.groups[0].level).toBe('common');
    expect(taxonomy.topics.map(topic => topic.label)).toEqual(topicLabels);
    expect(taxonomy.topics.every(topic => topic.level === 'common')).toBe(true);
    expect(topicsForSubject('japanese')).toHaveLength(14);
  });

  it('crosswalks every browse topic to official Japanese curriculum nodes', () => {
    const canonicalIds = new Set(
      CURRICULUM.flatMap(subject => subject.strands.flatMap(strand => strand.subtopics.map(topic => topic.id))),
    );
    for (const topic of taxonomy.topics) {
      const ids = curriculumNodeIdsForExamTopic(topic.id);
      expect(ids.length, `${topic.id} has no curriculum crosswalk`).toBeGreaterThan(0);
      expect(ids.filter(id => !canonicalIds.has(id)), `${topic.id} has orphaned curriculum ids`).toEqual([]);
    }
  });

  it('reconciles all 232 factual headings without copying commercial content', () => {
    expect(crosswalk.summary).toMatchObject({
      referenceHeadingAssociations: 232,
      matchedHeadingAssociations: 230,
      sourceBlockedHeadingAssociations: 2,
      matchedLocalCardLinks: 436,
      hostedPaperAnchorMaps: 93,
    });
    expect(crosswalk.policy.excludedContent).toContain('No commercial mock question');

    const sourceBlocked = crosswalk.associations.filter(association => association.resolution === 'source-blocked');
    expect(sourceBlocked.map(association => association.heading)).toEqual([
      '2021 - Oral Exam Materials - Section 1 - Question 1',
      '2021 - Oral Exam Materials - Section 1 - Question 2',
    ]);
    expect(sourceBlocked.every(association => (
      'reason' in association
      && association.reason.includes('SEC archive')
      && association.reason.includes('no StudyClix-hosted')
    ))).toBe(true);

    for (const association of crosswalk.associations.filter(
      (item): item is MatchedAssociation => item.resolution === 'matched',
    )) {
      const sidecar = JSON.parse(readFileSync(resolve(
        __dirname,
        `../scripts/paper-trail/answers/${association.year}/${association.target.fileid}.json`,
      ), 'utf8')) as { q: Array<{ n: string }> };
      const numbers = new Set(sidecar.q.map(question => question.n));
      expect(association.target.questionNumbers.length, association.heading).toBeGreaterThan(0);
      expect(association.target.questionNumbers.filter(number => !numbers.has(number)), association.heading).toEqual([]);
    }
  });

  it('retains every heading as part-aware audit metadata', () => {
    const references = examQuestionPartReferencesForSubject('japanese');
    expect(references).toHaveLength(438);
    expect(new Set(references.map(reference => `${reference.topicId}|${reference.subdivision}`))).toHaveLength(232);
    expect(references.filter(reference => reference.paperKey === 'oral')).toHaveLength(2);
    expect(references.filter(reference => reference.paperKey === 'aural')).toHaveLength(91);
    expect(references.filter(reference => reference.paperKey === 'single')).toHaveLength(345);
  });

  it('preserves every exact pre-migration paper and card identity', () => {
    expect(baseline).toHaveLength(93);
    for (const expected of baseline) {
      const live = topicsForPaper('japanese', expected.year, expected.level, expected.lang, expected.fileid);
      expect(live, `${expected.level}|${expected.lang}|${expected.year}|${expected.fileid}`).not.toBeNull();
      expect(live!.paperKey).toBe(expected.paperKey);
      expect(live!.q.map(question => question.n)).toEqual(expected.questions);
    }
  });

  it('classifies every one of the 1,329 retained local cards explicitly', () => {
    const papers = PAPER_TOPIC_TAGS.filter(paper => paper.subjectId === 'japanese');
    expect(papers).toHaveLength(93);
    expect(papers.reduce((count, paper) => count + paper.q.length, 0)).toBe(1_329);
    expect(crosswalk.summary).toMatchObject({
      localPaperVariants: 93,
      localQuestionMappings: 1_329,
      referenceMappedLocalQuestions: 388,
      retainedLocalQuestions: 941,
    });

    const validTopicIds = new Set(taxonomy.topics.map(topic => topic.id));
    for (const paper of papers) {
      for (const question of paper.q) {
        const topicIds = browseTopicIdsForQuestion(paper, question);
        expect(topicIds.length, `${paper.level}|${paper.lang}|${paper.year}|${paper.paperKey}|${question.n}`).toBeGreaterThan(0);
        expect(topicIds.filter(topicId => !validTopicIds.has(topicId))).toEqual([]);
      }
    }
  });

  it('keeps granular and coarse translation boundaries faithful', () => {
    expect(examTopicIdsForQuestion('japanese', 'higher', 2023, 'main', '12', 'single', 'ev')).toEqual([
      'japanese-common-comprehension-general-reading',
    ]);
    expect(examTopicIdsForQuestion('japanese', 'higher', 2023, 'main', '15', 'single', 'ev')).toEqual([
      'japanese-common-translation-japanese-to-english',
    ]);
    expect(examTopicIdsForQuestion('japanese', 'higher', 2014, 'main', '3', 'single', 'ev')).toEqual([
      'japanese-common-comprehension-general-reading',
      'japanese-common-translation-japanese-to-english',
    ]);
  });

  it('preserves deliberate overlap among the writing practice buckets', () => {
    expect(examTopicIdsForQuestion('japanese', 'higher', 2025, 'main', '29', 'single', 'ev')).toEqual([
      'japanese-common-personal-writing-all',
      'japanese-common-writing-me-my-family',
      'japanese-common-writing-school-studying-japanese-future-plans',
    ]);
    expect(examTopicIdsForQuestion('japanese', 'higher', 2024, 'main', '26', 'single', 'ev')).toEqual([
      'japanese-common-writing-home-ireland',
      'japanese-common-writing-me-my-family',
    ]);
    expect(examTopicIdsForQuestion('japanese', 'ordinary', 2025, 'main', '25', 'single', 'ev')).toEqual([
      'japanese-common-personal-writing-all',
    ]);
  });

  it('surfaces all 968 distinct local cards without inflating translations', () => {
    expect(subjectAtlasStats('japanese')).toMatchObject({
      questions: 968,
      topics: 14,
      yearMin: 2010,
      yearMax: 2026,
    });
    expect(topicsForSubject('japanese').find(topic => topic.label === 'ORAL Exam')).toMatchObject({
      count: 0,
      years: 0,
    });
  });

  it('stores only zero mock counts, never commercial mock content', () => {
    expect(taxonomy.topics.reduce((count, topic) => count + topic.mockQuestionCount, 0)).toBe(0);
    for (const topic of taxonomy.topics) {
      expect(Object.keys(topic).sort()).toEqual([
        'curriculumNodeIds',
        'id',
        'label',
        'level',
        'mockQuestionCount',
        'officialQuestionKeys',
        'sourcePath',
      ]);
    }
  });
});
