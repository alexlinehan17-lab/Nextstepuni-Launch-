#!/usr/bin/env node
/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 *
 * Reconcile the factual StudyClix Religious Education heading snapshot with
 * NextStepUni's stable, entitled SEC section cards. The official syllabus
 * remains canonical; the generated runtime supplies the flatter level-aware
 * practice menu and never imports commercial question content.
 */

import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const HERE = path.dirname(fileURLToPath(import.meta.url));
const ROOT = path.resolve(HERE, '../..');
const TAGS_PATH = path.join(HERE, 'topic-tags/tags/religious-education.json');
const REFERENCE_PATH = path.join(ROOT, 'data/examTopics/religious-education.json');
const OUTPUT_PATH = path.join(ROOT, 'data/examTopics/religious-education-local-crosswalk.json');
const RUNTIME_PATH = path.join(ROOT, 'data/examTopics/religious-education-runtime.json');
const BASELINE_PATH = path.join(ROOT, 'test/fixtures/religiousEducationTopicQuestionBaseline.json');

const reference = JSON.parse(fs.readFileSync(REFERENCE_PATH, 'utf8'));
const localPapers = JSON.parse(fs.readFileSync(TAGS_PATH, 'utf8'));
const preservationBaseline = JSON.parse(fs.readFileSync(BASELINE_PATH, 'utf8'));

const LEVELS = ['higher', 'ordinary'];
const sectionOfTopic = topicId => (
  topicId.match(/-(?:higher|ordinary)-([a-j])-/i)?.[1]?.toUpperCase()
);
const sectionOfQuestion = question => {
  const match = question.primary.match(/^religious-education-(\d+)-/);
  if (!match) throw new Error(`Unparseable Religious Education canonical id: ${question.primary}`);
  return String.fromCharCode(65 + Number(match[1]));
};
const topicFor = (level, section) => {
  const topic = reference.levels[level].topics[section.charCodeAt(0) - 65];
  if (!topic || sectionOfTopic(topic.id) !== section) {
    throw new Error(`Missing ${level} Section ${section} reference topic`);
  }
  return topic;
};

const CURRICULUM_COUNTS = [9, 11, 12, 8, 7, 8, 10, 9, 9, 9];
const curriculumIdsForSection = section => {
  const groupIndex = section.charCodeAt(0) - 65;
  return Array.from(
    { length: CURRICULUM_COUNTS[groupIndex] },
    (_, topicIndex) => `religious-education-${groupIndex}-${topicIndex}`,
  );
};
const curriculumCrosswalk = Object.fromEntries(
  LEVELS.flatMap(level => 'ABCDEFGHIJ'.split('').map(section => [
    topicFor(level, section).id,
    curriculumIdsForSection(section),
  ])),
);

const paperIdentity = paper => [
  paper.level,
  paper.lang,
  paper.year,
  paper.paperKey,
  paper.fileid,
].join('|');

const paperIds = localPapers.map(paperIdentity);
const duplicatePapers = paperIds.filter((identity, index) => paperIds.indexOf(identity) !== index);
if (duplicatePapers.length) {
  throw new Error(`Duplicate Religious Education topic-tag papers: ${[...new Set(duplicatePapers)].join(', ')}`);
}
for (const paper of localPapers) {
  const numbers = paper.q.map(question => question.n);
  if (new Set(numbers).size !== numbers.length) {
    throw new Error(`${paperIdentity(paper)} has duplicate card numbers`);
  }
  if (paper.q.length !== 8) {
    throw new Error(`${paperIdentity(paper)} has ${paper.q.length} cards; expected eight printed sections`);
  }
}

let preservedBaselineCards = 0;
for (const expected of preservationBaseline) {
  const live = localPapers.find(paper => paperIdentity(paper) === paperIdentity(expected));
  if (!live) throw new Error(`Preservation failure: missing paper ${paperIdentity(expected)}`);
  for (const number of expected.questions) {
    if (!live.q.some(question => question.n === number)) {
      throw new Error(`Preservation failure: missing ${paperIdentity(expected)} Q${number}`);
    }
    preservedBaselineCards += 1;
  }
}

const parseYear = heading => {
  const year = Number(heading.match(/^(\d{4})/)?.[1]);
  if (!year) throw new Error(`Unparseable Religious Education heading: ${heading}`);
  return year;
};
const preferredEnglishPaper = (level, year) => {
  const papers = localPapers.filter(paper => (
    paper.level === level
    && paper.lang === 'ev'
    && paper.year === year
    && paper.paperKey === 'single'
  ));
  if (papers.length > 1) throw new Error(`Ambiguous ${level} English paper for ${year}`);
  return papers[0] ?? null;
};
const referenceQuestionNumber = (heading, section) => (
  heading.match(/\bQuestion\s+([A-J0-9]+)/i)?.[1] ?? section
);

const associations = LEVELS.flatMap(level => reference.levels[level].topics.flatMap(referenceTopic => {
  const section = sectionOfTopic(referenceTopic.id);
  return referenceTopic.officialQuestionHeadings.map(heading => {
    const year = parseYear(heading);
    const paper = preferredEnglishPaper(level, year);
    const question = paper?.q.find(candidate => sectionOfQuestion(candidate) === section);
    if (!paper || !question) {
      return {
        topicId: referenceTopic.id,
        heading,
        level,
        year,
        resolution: 'source-blocked',
        referenceQuestionNumber: referenceQuestionNumber(heading, section),
        reason: 'The entitled local SEC Religious Education corpus has no matching paper for this year and level. The factual heading is retained pending acquisition and independent verification of the official SEC paper and marking scheme; no StudyClix-hosted question image or PDF is copied.',
      };
    }
    return {
      topicId: referenceTopic.id,
      heading,
      level,
      year,
      resolution: 'matched',
      target: {
        level,
        lang: 'ev',
        paperKey: paper.paperKey,
        fileid: paper.fileid,
        questionNumbers: [question.n],
      },
    };
  });
}));

const matched = associations.filter(association => association.resolution === 'matched');
const sourceBlocked = associations.filter(association => association.resolution === 'source-blocked');
const matchedTopicYears = new Set(matched.map(association => (
  `${association.level}|${association.year}|${association.topicId}`
)));

const topicOrder = new Map(
  LEVELS.flatMap(level => reference.levels[level].topics)
    .map((topic, index) => [topic.id, index]),
);
const localQuestionMappings = localPapers.flatMap(paper => paper.q.map(question => {
  const section = sectionOfQuestion(question);
  const topicId = topicFor(paper.level, section).id;
  return {
    level: paper.level,
    lang: paper.lang,
    year: paper.year,
    fileid: paper.fileid,
    paperKey: paper.paperKey,
    n: question.n,
    topicIds: [topicId],
    provenance: matchedTopicYears.has(`${paper.level}|${paper.year}|${topicId}`)
      ? 'reference'
      : 'retained-local',
  };
}));

const distinctLocalQuestions = new Set(localQuestionMappings.map(mapping => (
  `${mapping.level}|${mapping.year}|${mapping.paperKey}|${mapping.n}`
))).size;
const referenceMappedPrintedQuestions = new Set(localQuestionMappings
  .filter(mapping => mapping.provenance === 'reference')
  .map(mapping => `${mapping.level}|${mapping.year}|${mapping.paperKey}|${mapping.n}`)).size;

const output = {
  schemaVersion: 1,
  subjectId: reference.subjectId,
  capturedAt: reference.capturedAt,
  policy: {
    matchedSource: 'Entitled local SEC corpus only.',
    levelResolution: 'Higher and Ordinary reference headings are joined only to the same level in the local SEC corpus; English/Irish editions share the same printed section classification.',
    granularity: 'StudyClix may split the compulsory Section A into several headings. NextStepUni retains every factual heading as part-aware metadata while its current official-paper sidecar presents the complete printed Section A as one card.',
    excludedContent: 'No commercial mock question, solution, note, question text, StudyClix image or StudyClix-hosted PDF is copied.',
  },
  summary: {
    referenceHeadingAssociations: associations.length,
    matchedHeadingAssociations: matched.length,
    sourceBlockedHeadingAssociations: sourceBlocked.length,
    matchedLocalCardLinks: matched.reduce(
      (count, association) => count + association.target.questionNumbers.length,
      0,
    ),
    referenceMappedPrintedQuestions,
    localPaperVariants: localPapers.length,
    localQuestionMappings: localQuestionMappings.length,
    distinctLocalQuestions,
    referenceMappedLocalQuestions: localQuestionMappings
      .filter(mapping => mapping.provenance === 'reference').length,
    retainedLocalQuestions: localQuestionMappings
      .filter(mapping => mapping.provenance === 'retained-local').length,
    preservedBaselinePaperVariants: preservationBaseline.length,
    preservedBaselineCards,
    addedLocalPaperVariants: localPapers.length - preservationBaseline.length,
    addedLocalCards: localQuestionMappings.length - preservedBaselineCards,
    hostedPaperAnchorMaps: localPapers.length,
  },
  curriculumCrosswalk,
  associations,
  localQuestionMappings,
};

fs.writeFileSync(OUTPUT_PATH, `${JSON.stringify(output, null, 2)}\n`);

const runtimeTopics = LEVELS.flatMap(level => reference.levels[level].topics);
const runtimeTopicIndex = new Map(runtimeTopics.map((topic, index) => [topic.id, index]));
const runtime = {
  v: 1,
  subjectId: reference.subjectId,
  capturedAt: reference.capturedAt,
  referenceProvider: reference.reference.provider,
  groups: LEVELS.map(level => [
    level === 'higher' ? 'h' : 'o',
    reference.levels[level].label,
    reference.levels[level].topics.map(topic => runtimeTopicIndex.get(topic.id)),
  ]),
  // [id, label, source path, mock count, curriculum ids, h/o]
  topics: runtimeTopics.map(topic => {
    const level = topic.id.includes('-higher-') ? 'h' : 'o';
    return [
      topic.id,
      topic.label,
      topic.sourcePath,
      topic.mockQuestionCount,
      curriculumCrosswalk[topic.id],
      level,
    ];
  }),
  // The topic index carries the level. All references are main/single.
  partReferences: associations.map(association => [
    runtimeTopicIndex.get(association.topicId),
    association.year,
    association.resolution === 'matched'
      ? association.target.questionNumbers[0]
      : association.referenceQuestionNumber,
    association.heading,
  ]),
  // h/o = Higher/Ordinary; e/i = English/Irish. All are main/single.
  questionMappings: localQuestionMappings.map(mapping => [
    mapping.level === 'higher' ? 'h' : 'o',
    mapping.lang === 'ev' ? 'e' : 'i',
    mapping.year,
    mapping.n,
    runtimeTopicIndex.get(mapping.topicIds[0]),
  ]),
};

for (const [topicIndex] of runtime.partReferences) {
  if (!Number.isInteger(topicIndex)) throw new Error('Unresolved part-reference topic index');
}
for (const mapping of runtime.questionMappings) {
  if (!Number.isInteger(mapping[4])) throw new Error('Unresolved local-mapping topic index');
}

fs.writeFileSync(RUNTIME_PATH, `${JSON.stringify(runtime)}\n`);
console.log(JSON.stringify(output.summary, null, 2));
