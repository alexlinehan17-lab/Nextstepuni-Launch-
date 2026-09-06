#!/usr/bin/env node
/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 *
 * Reconcile factual DCG reference headings with the entitled SEC corpus. The
 * official curriculum remains canonical; this emits a level-aware practice
 * taxonomy and preserves every local Section-A and Section-B/C drawing card.
 */

import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const HERE = path.dirname(fileURLToPath(import.meta.url));
const ROOT = path.resolve(HERE, '../..');
const SUBJECT_ID = 'design-and-communication-graphics';
const TAGS_PATH = path.join(HERE, 'topic-tags/tags', `${SUBJECT_ID}.json`);
const REFERENCE_PATH = path.join(ROOT, 'data/examTopics', `${SUBJECT_ID}.json`);
const CURRICULUM_CROSSWALK_PATH = path.join(
  ROOT,
  'data/examTopics',
  `${SUBJECT_ID}-curriculum-crosswalk.json`,
);
const OUTPUT_PATH = path.join(ROOT, 'data/examTopics', `${SUBJECT_ID}-local-crosswalk.json`);
const RUNTIME_PATH = path.join(ROOT, 'data/examTopics', `${SUBJECT_ID}-runtime.json`);
const BASELINE_PATH = path.join(
  ROOT,
  'test/fixtures/designAndCommunicationGraphicsTopicQuestionBaseline.json',
);
const HOSTED_ROOT = path.join(ROOT, 'public/paper-anchors');

const reference = JSON.parse(fs.readFileSync(REFERENCE_PATH, 'utf8'));
const curriculumCrosswalk = JSON.parse(fs.readFileSync(CURRICULUM_CROSSWALK_PATH, 'utf8'));
const localPapers = JSON.parse(fs.readFileSync(TAGS_PATH, 'utf8'));
const preservationBaseline = JSON.parse(fs.readFileSync(BASELINE_PATH, 'utf8'));
const LEVELS = ['higher', 'ordinary'];
const EXPECTED_YEARS = {
  higher: Array.from({ length: 17 }, (_, index) => 2010 + index),
  ordinary: Array.from({ length: 17 }, (_, index) => 2010 + index).filter(year => year !== 2020),
};

const allTopics = LEVELS.flatMap(level => reference.levels[level].topics);
const topicIndex = new Map(allTopics.map((topic, index) => [topic.id, index]));
const topicLevel = new Map(LEVELS.flatMap(level => (
  reference.levels[level].topics.map(topic => [topic.id, level])
)));

const crosswalkKeys = Object.keys(curriculumCrosswalk).sort();
const topicIds = allTopics.map(topic => topic.id).sort();
if (JSON.stringify(crosswalkKeys) !== JSON.stringify(topicIds)) {
  throw new Error('DCG curriculum crosswalk must cover every reference topic exactly once');
}
for (const [topicId, nodeIds] of Object.entries(curriculumCrosswalk)) {
  if (!Array.isArray(nodeIds) || !nodeIds.length || new Set(nodeIds).size !== nodeIds.length) {
    throw new Error(`${topicId}: curriculum crosswalk must contain unique canonical nodes`);
  }
  for (const nodeId of nodeIds) {
    if (!/^design-and-communication-graphics-[0-2]-\d+$/.test(nodeId)) {
      throw new Error(`${topicId}: invalid canonical DCG node ${nodeId}`);
    }
  }
}

const paperIdentity = paper => [
  paper.level,
  paper.lang,
  paper.year,
  paper.paperKey,
  paper.fileid,
].join('|');

const paperIds = localPapers.map(paperIdentity);
const duplicatePaperIds = paperIds.filter((identity, index) => paperIds.indexOf(identity) !== index);
if (duplicatePaperIds.length) {
  throw new Error(`Duplicate DCG paper variants: ${[...new Set(duplicatePaperIds)].join(', ')}`);
}
if (localPapers.length !== 132) {
  throw new Error(`Expected 132 DCG variants, found ${localPapers.length}`);
}

for (const paper of localPapers) {
  if (!LEVELS.includes(paper.level) || !['ev', 'iv'].includes(paper.lang)) {
    throw new Error(`Unexpected DCG paper identity: ${paperIdentity(paper)}`);
  }
  const expected = paper.paperKey === 'section-a'
    ? ['1', '2', '3', '4']
    : paper.paperKey === 'single'
      ? ['1', '2', '3', '4', '5', '6', '7', '8']
      : null;
  if (!expected || JSON.stringify(paper.q.map(question => question.n)) !== JSON.stringify(expected)) {
    throw new Error(`${paperIdentity(paper)}: invalid question run`);
  }
}

let preservedBaselineCards = 0;
for (const expected of preservationBaseline) {
  const live = localPapers.find(paper => paperIdentity(paper) === paperIdentity(expected));
  if (!live) throw new Error(`Preservation failure: missing ${paperIdentity(expected)}`);
  for (const number of expected.questions) {
    if (!live.q.some(question => question.n === number)) {
      throw new Error(`Preservation failure: missing ${paperIdentity(expected)} Q${number}`);
    }
    preservedBaselineCards += 1;
  }
}

const clean = value => value.replace(/\s+/g, ' ').trim();
const parseHeading = heading => {
  const normalized = clean(heading);
  const year = Number(normalized.match(/^(\d{4})/)?.[1]);
  const sections = [...normalized.matchAll(/Section\s*([ABC])/gi)];
  const section = sections.at(-1)?.[1].toUpperCase();
  const question = normalized.match(/Question\s*(?:[ABC]\s*-?\s*)?(\d+)/i)
    ?? (section === 'B' ? normalized.match(/Part\s*(\d+)\b/i) : null);
  if (!year || !section || !question) throw new Error(`Unparseable DCG heading: ${heading}`);
  return {
    year,
    sitting: /Deferred Exam/i.test(normalized) ? 'deferred' : 'main',
    section,
    printedQuestionNumber: question[1],
  };
};

const localSlot = ({ section, printedQuestionNumber }) => {
  const printed = Number(printedQuestionNumber);
  if (section === 'A') return { paperKey: 'section-a', questionNumber: String(printed) };
  if (section === 'B') return { paperKey: 'single', questionNumber: String(printed) };
  if (section === 'C') return { paperKey: 'single', questionNumber: String(printed + 3) };
  throw new Error(`Unexpected DCG section ${section}`);
};

const EnglishPaper = (level, year, paperKey) => {
  const candidates = localPapers.filter(paper => (
    paper.level === level
    && paper.lang === 'ev'
    && paper.year === year
    && paper.paperKey === paperKey
  ));
  if (candidates.length > 1) {
    throw new Error(`Ambiguous ${level} English DCG ${paperKey} paper for ${year}`);
  }
  return candidates[0] ?? null;
};

const blockedReason = parsed => {
  if (parsed.year < 2010) {
    return 'The entitled local SEC DCG corpus currently begins at 2010. This factual heading is retained pending acquisition and independent verification of the official paper; no StudyClix-hosted question image or PDF is copied.';
  }
  if (parsed.sitting === 'deferred') {
    return 'The entitled Paper Trail corpus does not currently contain this deferred-sitting DCG booklet. The factual heading is retained pending acquisition and independent verification from an official source; no StudyClix-hosted question image or PDF is copied.';
  }
  return null;
};

const associations = [];
for (const level of LEVELS) {
  for (const topic of reference.levels[level].topics) {
    for (const heading of topic.officialQuestionHeadings) {
      const parsed = parseHeading(heading);
      const slot = localSlot(parsed);
      const explicitBlock = blockedReason(parsed);
      const paper = explicitBlock ? null : EnglishPaper(level, parsed.year, slot.paperKey);
      const localQuestion = paper?.q.find(question => question.n === slot.questionNumber);
      if (explicitBlock || !paper || !localQuestion) {
        associations.push({
          topicId: topic.id,
          level,
          heading,
          ...parsed,
          ...slot,
          resolution: 'source-blocked',
          reason: explicitBlock
            ?? 'No matching entitled local SEC paper card is present. The factual heading is retained pending independent verification; no StudyClix-hosted question image or PDF is copied.',
        });
        continue;
      }
      associations.push({
        topicId: topic.id,
        level,
        heading,
        ...parsed,
        ...slot,
        resolution: 'matched',
        target: {
          level,
          lang: 'ev',
          year: parsed.year,
          paperKey: slot.paperKey,
          fileid: paper.fileid,
          questionNumber: slot.questionNumber,
        },
      });
    }
  }
}

const referenceOfficialAssociations = allTopics.reduce(
  (sum, topic) => sum + topic.officialQuestionHeadings.length,
  0,
);
const referenceMockAssociations = allTopics.reduce(
  (sum, topic) => sum + topic.mockQuestionCount,
  0,
);
const referenceReportedAssociations = allTopics.reduce(
  (sum, topic) => sum + topic.reportedQuestionCount,
  0,
);
if (
  allTopics.length !== 29
  || referenceOfficialAssociations !== 427
  || referenceMockAssociations !== 360
  || referenceReportedAssociations !== 787
) {
  throw new Error('DCG factual audit totals changed unexpectedly');
}

const exactTopicsByCard = new Map();
for (const association of associations.filter(item => item.resolution === 'matched')) {
  const key = [
    association.level,
    association.year,
    association.paperKey,
    association.questionNumber,
  ].join('|');
  const indexes = exactTopicsByCard.get(key) ?? [];
  const index = topicIndex.get(association.topicId);
  if (index === undefined) throw new Error(`Unknown DCG topic ${association.topicId}`);
  if (!indexes.includes(index)) indexes.push(index);
  exactTopicsByCard.set(key, indexes);
}

const fallbackTopicForNode = (level, nodeId) => {
  const candidates = allTopics
    .map((topic, index) => ({ topic, index }))
    .filter(({ topic }) => topicLevel.get(topic.id) === level && curriculumCrosswalk[topic.id].includes(nodeId))
    .sort((left, right) => (
      curriculumCrosswalk[left.topic.id].length - curriculumCrosswalk[right.topic.id].length
      || left.index - right.index
    ));
  if (!candidates.length) throw new Error(`No ${level} DCG exam topic covers ${nodeId}`);
  return candidates[0].index;
};

const questionMappings = [];
const retainedLocalCards = [];
const retainedLogical = new Set();
for (const paper of localPapers) {
  for (const question of paper.q) {
    const logicalKey = [paper.level, paper.year, paper.paperKey, question.n].join('|');
    let indexes = exactTopicsByCard.get(logicalKey);
    if (!indexes) {
      indexes = [...new Set(
        [question.primary, question.secondary]
          .filter(Boolean)
          .map(nodeId => fallbackTopicForNode(paper.level, nodeId)),
      )];
      if (!retainedLogical.has(logicalKey)) {
        retainedLogical.add(logicalKey);
        retainedLocalCards.push({
          level: paper.level,
          year: paper.year,
          paperKey: paper.paperKey,
          questionNumber: question.n,
          canonicalNodeIds: [question.primary, question.secondary].filter(Boolean),
          topicIds: indexes.map(index => allTopics[index].id),
          resolution: 'retained-local',
          reason: 'Entitled SEC drawing task preserved locally although the factual reference snapshot has no association for this independently selectable question.',
        });
      }
    }
    if (!indexes.length) throw new Error(`${paperIdentity(paper)} Q${question.n}: empty topic mapping`);
    questionMappings.push([
      paper.level === 'higher' ? 'h' : 'o',
      paper.lang === 'ev' ? 'e' : 'i',
      paper.year,
      paper.paperKey === 'section-a' ? 'a' : 's',
      question.n,
      indexes,
    ]);
  }
}

const matchedAssociations = associations.filter(item => item.resolution === 'matched');
const sourceBlockedAssociations = associations.filter(item => item.resolution === 'source-blocked');
const matchedQuestionTopicLinks = new Set(matchedAssociations.map(item => [
  item.topicId,
  item.level,
  item.year,
  item.paperKey,
  item.questionNumber,
].join('|'))).size;
const physicalMappings = localPapers.reduce((sum, paper) => sum + paper.q.length, 0);
const distinctStudentFacingQuestions = localPapers
  .filter(paper => paper.lang === 'ev')
  .reduce((sum, paper) => sum + paper.q.length, 0);

if (matchedAssociations.length !== 386 || sourceBlockedAssociations.length !== 41) {
  throw new Error(`Unexpected DCG reconciliation split: ${matchedAssociations.length}/${sourceBlockedAssociations.length}`);
}
if (exactTopicsByCard.size !== 347 || retainedLocalCards.length !== 49) {
  throw new Error(`Expected 347 matched + 49 retained logical cards, found ${exactTopicsByCard.size} + ${retainedLocalCards.length}`);
}
if (physicalMappings !== 792 || distinctStudentFacingQuestions !== 396 || questionMappings.length !== 792) {
  throw new Error('DCG local corpus totals changed unexpectedly');
}

let hostedAnchorMaps = 0;
for (const paper of localPapers) {
  const mapPath = path.join(HOSTED_ROOT, String(paper.year), `${paper.fileid}.json`);
  if (!fs.existsSync(mapPath)) throw new Error(`${paperIdentity(paper)} has no hosted question map`);
  const map = JSON.parse(fs.readFileSync(mapPath, 'utf8'));
  const expectedNumbers = paper.q.map(question => question.n);
  if (map.paperFileid !== paper.fileid || JSON.stringify(map.q.map(question => question.n)) !== JSON.stringify(expectedNumbers)) {
    throw new Error(`${paperIdentity(paper)} has a mismatched hosted question map`);
  }
  hostedAnchorMaps += 1;
}

const groups = [];
let offset = 0;
for (const level of LEVELS) {
  const indexes = reference.levels[level].topics.map((_, index) => offset + index);
  groups.push([level === 'higher' ? 'h' : 'o', reference.levels[level].label, indexes]);
  offset += indexes.length;
}
const runtimeTopics = allTopics.map(topic => [
  topic.id,
  topic.label,
  topic.sourcePath,
  topic.mockQuestionCount,
  curriculumCrosswalk[topic.id],
  topicLevel.get(topic.id) === 'higher' ? 'h' : 'o',
]);
const partReferences = associations.map(association => [
  topicIndex.get(association.topicId),
  association.year,
  association.sitting === 'deferred' ? 'd' : 'm',
  association.paperKey === 'section-a' ? 'a' : 's',
  association.questionNumber,
  association.heading,
]);

const summary = {
  referenceTopics: allTopics.length,
  referenceReportedAssociations,
  referenceOfficialAssociations,
  referenceMockAssociations,
  matchedAssociations: matchedAssociations.length,
  sourceBlockedAssociations: sourceBlockedAssociations.length,
  matchedLogicalCards: exactTopicsByCard.size,
  matchedQuestionTopicLinks,
  retainedLocalLogicalCards: retainedLocalCards.length,
  localPaperVariants: localPapers.length,
  localPhysicalMappings: physicalMappings,
  distinctStudentFacingQuestions,
  hostedAnchorMaps,
  preservedBaselineVariants: preservationBaseline.length,
  preservedBaselineCards,
  emptyReferenceTopics: allTopics
    .filter(topic => topic.officialQuestionHeadings.length === 0)
    .map(topic => topic.id),
};

const evidence = {
  schemaVersion: 1,
  subjectId: reference.subjectId,
  capturedAt: reference.capturedAt,
  reference: reference.reference,
  policy: {
    curriculumAuthority: 'NCCA/Curriculum Online',
    examAuthority: 'State Examinations Commission',
    commercialReferenceUse: 'Factual topic labels, headings, classifications, and counts only.',
    excludedCommercialContent: 'Question text, solutions, notes, videos, images, PDFs, and mock content.',
  },
  summary,
  curriculumCrosswalk,
  associations,
  retainedLocalCards,
};
const runtime = {
  v: 1,
  subjectId: reference.subjectId,
  capturedAt: reference.capturedAt,
  referenceProvider: reference.reference.provider,
  groups,
  topics: runtimeTopics,
  partReferences,
  questionMappings,
  summary,
};

fs.writeFileSync(OUTPUT_PATH, `${JSON.stringify(evidence, null, 2)}\n`);
fs.writeFileSync(RUNTIME_PATH, `${JSON.stringify(runtime)}\n`);
console.log(JSON.stringify(summary, null, 2));
