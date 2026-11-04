/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 */

import { describe, expect, it } from 'vitest';
import { CURRICULUM } from '../curriculum';
import reference from '../data/examTopics/english.json';
import crosswalk from '../data/examTopics/english-curriculum-crosswalk.json';
import reviewedArchive from '../data/examTopics/english-reviewed-archive-topics.json';
import baseQuestionRuntime from '../data/examTopics/english-question-runtime.json';
import reviewedQuestionRuntime from '../data/examTopics/english-reviewed-question-runtime.json';
import { PAPER_TOPIC_TAGS } from '../data/paperTrail/topicTags';
import {
  browseTopicIdsForQuestion,
  topicsForSubject,
} from '../components/PaperTrail/topics';
import {
  curriculumNodeIdsForExamTopic,
  examQuestionTopicMappingsForSubject,
  examTopicTaxonomyFor,
} from '../data/examTopics/registry';

const referenceTopics = Object.values(reference.variants).flatMap(variant => variant.topics);
// Additive archive topics and exact booklet links grow as english_publish.py
// publishes reviewed papers; derive the expected totals from its outputs.
const ARCHIVE = 11 + reviewedArchive.topics.length;
const mappingKey = (row: readonly unknown[]) => JSON.stringify(row.slice(0, 6));
const baseKeys = new Set((baseQuestionRuntime.questionMappings as unknown[][]).map(mappingKey));
const ADDED_LINKS = new Set((reviewedQuestionRuntime.questionMappings as unknown[][]).map(mappingKey)
  .filter(key => !baseKeys.has(key))).size;

describe('English exam-topic registry', () => {
  const taxonomy = examTopicTaxonomyFor('english')!;

  it('pins the complete 86-topic reference menu before explicit local archives', () => {
    expect(taxonomy).not.toBeNull();
    expect(taxonomy.groups.slice(0, 2)).toEqual([
      {
        id: 'english-higher',
        label: 'Higher Level',
        level: 'higher',
        topicIds: reference.variants.higher.topics.map(topic => topic.id),
      },
      {
        id: 'english-ordinary',
        label: 'Ordinary Level',
        level: 'ordinary',
        topicIds: reference.variants.ordinary.topics.map(topic => topic.id),
      },
    ]);
    expect(taxonomy.groups[2]).toMatchObject({
      id: 'english-higher-local-archive',
      label: 'Higher Level · Historical local archive',
      level: 'higher',
    });
    expect(taxonomy.topics.slice(0, 86).map(topic => [topic.id, topic.label, topic.sourcePath]))
      .toEqual(referenceTopics.map(topic => [topic.id, topic.label, topic.sourcePath]));
    // 11 original Higher archive topics, then the additive archive topics for
    // canonical nodes that published reviewed cards need and the reference menu
    // lacks (Higher ones appended to the Higher archive group, Ordinary ones in
    // an Ordinary archive group; english_publish.py keeps them append-only).
    // The 86 reference and 11 original archive topics keep their index.
    expect(reviewedArchive.topics.length).toBeGreaterThanOrEqual(67);
    expect(taxonomy.topics.slice(86)).toHaveLength(ARCHIVE);
    expect(taxonomy.topics.slice(86, 97).every(topic => topic.id.endsWith('-archive')
      && !topic.id.endsWith('-reviewed-archive'))).toBe(true);
    expect(taxonomy.topics.slice(97).every(topic => topic.id.endsWith('-reviewed-archive'))).toBe(true);
    expect(taxonomy.topics.slice(86).every(topic => (
      topic.sourcePath.startsWith('/nextstepuni-preservation/english/')
    ))).toBe(true);
    expect(taxonomy.groups[3]).toMatchObject({
      id: 'english-ordinary-local-archive',
      label: 'Ordinary Level · Historical local archive',
      level: 'ordinary',
    });
    expect(topicsForSubject('english')).toHaveLength(86 + ARCHIVE);
  });

  it('reconciles all 1,064 displayed associations without importing provider content', () => {
    expect(referenceTopics).toHaveLength(86);
    expect(reference.totals).toEqual({
      reported: 1064,
      state: 566,
      mock: 498,
      providerSample: 0,
      sourceLabelConflicts: 0,
    });
    for (const topic of referenceTopics) {
      expect(
        topic.officialQuestionHeadings.length
        + topic.mockQuestionCount
        + topic.providerSampleQuestionCount,
        topic.id,
      ).toBe(topic.reportedQuestionCount);
      expect(topic.officialQuestionHeadings.some(heading => /mock/i.test(heading)), topic.id)
        .toBe(false);
    }
  });

  it('bridges every reference and archive topic to canonical English nodes', () => {
    const canonicalIds = new Set(
      CURRICULUM.find(subject => subject.id === 'english')!
        .strands.flatMap(strand => strand.subtopics.map(topic => topic.id)),
    );
    expect(Object.keys(crosswalk)).toHaveLength(86 + ARCHIVE);
    for (const topic of taxonomy.topics) {
      const ids = curriculumNodeIdsForExamTopic(topic.id);
      expect(ids, topic.id).toEqual(crosswalk[topic.id as keyof typeof crosswalk]);
      expect(ids.length, topic.id).toBeGreaterThan(0);
      expect(ids.filter(id => !canonicalIds.has(id)), topic.id).toEqual([]);
    }
  });

  it('keeps every existing English SEC card browsable after the atomic switch', () => {
    const papers = PAPER_TOPIC_TAGS.filter(paper => paper.subjectId === 'english');
    expect(papers).toHaveLength(24);
    expect(papers.reduce((sum, paper) => sum + paper.q.length, 0)).toBe(125);
    // 771 original mappings, plus one exact booklet link for each published
    // reviewed paper's sidecar block that had no exact mapping (194 once the
    // 2010-2018, 2025 HL and 2026 papers were published).
    expect(ADDED_LINKS).toBeGreaterThanOrEqual(194);
    expect(examQuestionTopicMappingsForSubject('english')).toHaveLength(771 + ADDED_LINKS);
    const taxonomyIds = new Set(taxonomy.topics.map(topic => topic.id));
    for (const paper of papers) {
      for (const question of paper.q) {
        const ids = browseTopicIdsForQuestion(paper, question);
        expect(ids.length, `${paper.year} ${paper.level} ${paper.paperKey} Q${question.n}`)
          .toBeGreaterThan(0);
        expect(ids.filter(id => !taxonomyIds.has(id))).toEqual([]);
      }
    }
    expect(examQuestionTopicMappingsForSubject('english').some(mapping => (
      mapping.topicIds.some(id => id.endsWith('-archive'))
    ))).toBe(true);
  });
});
