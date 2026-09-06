/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 *
 * Physics & Chemistry StudyClix-reference parity, level-resolution and
 * preservation gates.
 */

import { describe, expect, it } from 'vitest';
import { CURRICULUM } from '../curriculum';
import physicsAndChemistryReference from '../data/examTopics/physics-and-chemistry.json';
import physicsAndChemistryCrosswalk from '../data/examTopics/physics-and-chemistry-local-crosswalk.json';
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
import preservationBaseline from './fixtures/physicsAndChemistryTopicQuestionBaseline.json';

const topicLabels = [
  'C | Acids and Bases',
  'C | Atomic Theory',
  'C | Bonding and Molecular Theory',
  'C | Chemical Equations',
  'C | Chlorides',
  'C | Electrochemistry and the Activity Series',
  'C | Hydrides',
  'C | Organic Chemistry',
  'C | Oxidation and Reduction',
  'C | Oxides',
  'C | The Elements',
  'C | Thermochemistry',
  'P | Acceleration',
  'P | Capacitor and Capacitance',
  'P | Conductors, Insulators and Electric Fields',
  'P | Current Electricity',
  'P | Electromagnetic Induction, AC, DC, Transformers',
  'P | Force, Mass, Momentum',
  'P | Gravitation',
  'P | Heat',
  'P | Light (Waves and Particles)',
  'P | Pressure, Moments, Gravity',
  'P | Radioactivity',
  'P | Reflection and Mirrors',
  'P | Refraction and Lenses',
  'P | Speed, Displacement, Velocity',
  'P | Vectors and Scalars',
  'P | Work, Energy, Power',
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
const crosswalk = physicsAndChemistryCrosswalk;

describe('Physics & Chemistry exam-topic registry', () => {
  const taxonomy = examTopicTaxonomyFor('physics-and-chemistry')!;

  it('pins the exact 28-topic shared reference menu', () => {
    expect(taxonomy).not.toBeNull();
    expect(taxonomy.groups.map(group => group.label)).toEqual(['Common Level']);
    expect(taxonomy.groups[0].level).toBe('common');
    expect(taxonomy.topics.map(topic => topic.label)).toEqual(topicLabels);
    expect(taxonomy.topics.every(topic => topic.level === 'common')).toBe(true);
    expect(topicsForSubject('physics-and-chemistry')).toHaveLength(28);
  });

  it('crosswalks every browse topic to real official curriculum nodes', () => {
    const canonicalIds = new Set(
      CURRICULUM.flatMap(subject => subject.strands.flatMap(strand => strand.subtopics.map(topic => topic.id))),
    );
    for (const topic of taxonomy.topics) {
      const ids = curriculumNodeIdsForExamTopic(topic.id);
      expect(ids.length, `${topic.id} has no curriculum crosswalk`).toBeGreaterThan(0);
      expect(ids.filter(id => !canonicalIds.has(id)), `${topic.id} has orphaned curriculum ids`).toEqual([]);
    }
  });

  it('reconciles all 706 factual headings and records the official-source boundary', () => {
    expect(crosswalk.summary).toMatchObject({
      referenceHeadingAssociations: 706,
      matchedHeadingAssociations: 626,
      sourceBlockedHeadingAssociations: 80,
      matchedLocalCardLinks: 626,
      referenceMappedPrintedQuestions: 159,
    });
    expect(crosswalk.policy.levelResolution).toContain('Higher Level');
    expect(crosswalk.policy.excludedContent).toContain('No commercial mock question');

    const blocked = crosswalk.associations.filter(association => association.resolution === 'source-blocked');
    expect(new Set(blocked.map(association => association.year))).toEqual(new Set([2008, 2009]));
    expect(blocked.every(association => (
      'reason' in association
      && association.reason.includes('official SEC paper and marking scheme')
      && association.reason.includes('no StudyClix-hosted')
    ))).toBe(true);

    const localPapers = PAPER_TOPIC_TAGS.filter(paper => paper.subjectId === 'physics-and-chemistry');
    for (const association of crosswalk.associations.filter(item => item.resolution === 'matched')) {
      expect(association.target.level).toBe('higher');
      expect(association.target.lang).toBe('ev');
      const paper = localPapers.find(candidate => (
        candidate.year === association.year
        && candidate.level === association.target.level
        && candidate.lang === association.target.lang
        && candidate.paperKey === association.target.paperKey
        && candidate.fileid === association.target.fileid
      ));
      expect(paper, association.heading).toBeDefined();
      const numbers = new Set(paper!.q.map(question => question.n));
      expect(association.target.questionNumbers.filter(number => !numbers.has(number)), association.heading).toEqual([]);
    }
  });

  it('retains every heading as part-aware audit metadata', () => {
    const references = examQuestionPartReferencesForSubject('physics-and-chemistry');
    expect(references).toHaveLength(706);
    expect(new Set(references.map(reference => `${reference.topicId}|${reference.subdivision}`))).toHaveLength(706);
    expect(references.every(reference => reference.level === 'higher')).toBe(true);
    expect(references.every(reference => reference.paperKey === 'single')).toBe(true);
  });

  it('preserves every one of the 53 pre-migration paper variants and 635 cards', () => {
    expect(baseline).toHaveLength(53);
    expect(baseline.reduce((count, paper) => count + paper.questions.length, 0)).toBe(635);
    for (const expected of baseline) {
      const live = topicsForPaper(
        'physics-and-chemistry',
        expected.year,
        expected.level,
        expected.lang,
        expected.fileid,
      );
      expect(live, `${expected.level}|${expected.lang}|${expected.year}|${expected.fileid}`).not.toBeNull();
      expect(live!.paperKey).toBe(expected.paperKey);
      expect(live!.q.map(question => question.n)).toEqual(expect.arrayContaining(expected.questions));
    }
  });

  it('adds 2026 and the omitted 2015 English card without sacrificing any prior identity', () => {
    expect(crosswalk.summary).toMatchObject({
      localPaperVariants: 57,
      localQuestionMappings: 684,
      distinctLocalQuestions: 384,
      referenceMappedLocalQuestions: 266,
      retainedLocalQuestions: 370,
      official2026LocalQuestions: 48,
      preservedBaselinePaperVariants: 53,
      preservedBaselineCards: 635,
      addedLocalPaperVariants: 4,
      addedLocalCards: 49,
    });

    const papers = PAPER_TOPIC_TAGS.filter(paper => paper.subjectId === 'physics-and-chemistry');
    expect(papers).toHaveLength(57);
    expect(papers.reduce((count, paper) => count + paper.q.length, 0)).toBe(684);
    expect(papers.find(paper => (
      paper.year === 2015 && paper.level === 'higher' && paper.lang === 'ev'
    ))?.q.map(question => question.n)).toContain('12');
    expect(papers.filter(paper => paper.year === 2026)).toHaveLength(4);
    expect(papers.filter(paper => paper.year === 2026).every(paper => paper.q.length === 12)).toBe(true);
  });

  it('classifies every retained and added local card explicitly', () => {
    const validTopicIds = new Set(taxonomy.topics.map(topic => topic.id));
    const papers = PAPER_TOPIC_TAGS.filter(paper => paper.subjectId === 'physics-and-chemistry');
    for (const paper of papers) {
      for (const question of paper.q) {
        const topicIds = browseTopicIdsForQuestion(paper, question);
        expect(topicIds.length, `${paper.level}|${paper.lang}|${paper.year}|${question.n}`).toBeGreaterThan(0);
        expect(topicIds.filter(topicId => !validTopicIds.has(topicId))).toEqual([]);
      }
    }
  });

  it('does not misapply Higher Level reference headings to Ordinary Level cards', () => {
    expect(examTopicIdsForQuestion(
      'physics-and-chemistry', 'higher', 2025, 'main', '2', 'single', 'ev',
    )).toContain('physics-and-chemistry-common-p-force-mass-momentum');
    expect(examTopicIdsForQuestion(
      'physics-and-chemistry', 'ordinary', 2025, 'main', '2', 'single', 'ev',
    )).toEqual([
      'physics-and-chemistry-common-p-speed-displacement-velocity',
      'physics-and-chemistry-common-p-work-energy-power',
    ]);
  });

  it('uses the inspected official SEC papers for the 2026 reference omissions', () => {
    expect(examTopicIdsForQuestion(
      'physics-and-chemistry', 'higher', 2026, 'main', '7', 'single', 'ev',
    )).toHaveLength(12);
    expect(examTopicIdsForQuestion(
      'physics-and-chemistry', 'ordinary', 2026, 'main', '8', 'single', 'iv',
    )).toEqual([
      'physics-and-chemistry-common-c-atomic-theory',
      'physics-and-chemistry-common-c-bonding-and-molecular-theory',
      'physics-and-chemistry-common-c-chlorides',
      'physics-and-chemistry-common-c-the-elements',
    ]);
  });

  it('surfaces all 384 distinct printed questions through the 28-topic menu', () => {
    expect(subjectAtlasStats('physics-and-chemistry')).toMatchObject({
      questions: 384,
      topics: 28,
      yearMin: 2010,
      yearMax: 2026,
    });
  });

  it('keeps empty reference buckets structural while allowing entitled local additions', () => {
    const emptyReferenceTopics = physicsAndChemistryReference.levels.common.topics
      .filter(topic => topic.officialQuestionHeadings.length === 0)
      .map(topic => topic.label);
    expect(emptyReferenceTopics).toEqual([
      'C | Chlorides',
      'C | Hydrides',
      'C | Organic Chemistry',
      'P | Gravitation',
      'P | Heat',
      'P | Reflection and Mirrors',
    ]);
    expect(taxonomy.topics.reduce((count, topic) => count + topic.mockQuestionCount, 0)).toBe(0);
  });
});
