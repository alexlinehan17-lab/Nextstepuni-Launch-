#!/usr/bin/env node
/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 *
 * Reconcile the factual StudyClix Economics heading snapshot with the complete
 * entitled SEC corpus. The NCCA curriculum remains canonical; this emits a
 * level-aware practice taxonomy and a compact question join without copying
 * commercial question content.
 */

import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const HERE = path.dirname(fileURLToPath(import.meta.url));
const ROOT = path.resolve(HERE, '../..');
const TAGS_PATH = path.join(HERE, 'topic-tags/tags/economics.json');
const REFERENCE_PATH = path.join(ROOT, 'data/examTopics/economics.json');
const CROSSWALK_PATH = path.join(ROOT, 'data/examTopics/economics-curriculum-crosswalk.json');
const OUTPUT_PATH = path.join(ROOT, 'data/examTopics/economics-local-crosswalk.json');
const RUNTIME_PATH = path.join(ROOT, 'data/examTopics/economics-runtime.json');
const BASELINE_PATH = path.join(ROOT, 'test/fixtures/economicsTopicQuestionBaseline.json');
const HOSTED_ROOT = path.join(ROOT, 'public/paper-anchors');

const reference = JSON.parse(fs.readFileSync(REFERENCE_PATH, 'utf8'));
const curriculumCrosswalk = JSON.parse(fs.readFileSync(CROSSWALK_PATH, 'utf8'));
const localPapers = JSON.parse(fs.readFileSync(TAGS_PATH, 'utf8'));
const preservationBaseline = JSON.parse(fs.readFileSync(BASELINE_PATH, 'utf8'));
const LEVELS = ['higher', 'ordinary'];

const allTopics = LEVELS.flatMap(level => reference.levels[level].topics);
const topicIndex = new Map(allTopics.map((topic, index) => [topic.id, index]));
const topicLevel = new Map(LEVELS.flatMap(level => (
  reference.levels[level].topics.map(topic => [topic.id, level])
)));

const crosswalkKeys = Object.keys(curriculumCrosswalk).sort();
const topicIds = allTopics.map(topic => topic.id).sort();
if (JSON.stringify(crosswalkKeys) !== JSON.stringify(topicIds)) {
  throw new Error('Economics curriculum crosswalk must cover every reference topic exactly once');
}
for (const [topicId, nodeIds] of Object.entries(curriculumCrosswalk)) {
  if (!Array.isArray(nodeIds) || !nodeIds.length || new Set(nodeIds).size !== nodeIds.length) {
    throw new Error(`${topicId}: curriculum crosswalk must contain unique canonical nodes`);
  }
  for (const nodeId of nodeIds) {
    if (!/^economics-[0-4]-\d+$/.test(nodeId)) {
      throw new Error(`${topicId}: invalid canonical Economics node ${nodeId}`);
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
  throw new Error(`Duplicate Economics paper variants: ${[...new Set(duplicatePaperIds)].join(', ')}`);
}
if (localPapers.length !== 66) {
  throw new Error(`Expected 66 Economics variants, found ${localPapers.length}`);
}

for (const paper of localPapers) {
  if (!LEVELS.includes(paper.level) || !['ev', 'iv'].includes(paper.lang) || paper.paperKey !== 'single') {
    throw new Error(`Unexpected Economics paper identity: ${paperIdentity(paper)}`);
  }
  const expected = paper.year <= 2020
    ? [...Array.from({ length: 9 }, (_, i) => String(i + 1)), ...Array.from({ length: 8 }, (_, i) => `B${i + 1}`)]
    : Array.from({ length: 16 }, (_, i) => String(i + 1));
  const actual = paper.q.map(question => question.n);
  if (JSON.stringify(actual) !== JSON.stringify(expected)) {
    throw new Error(`${paperIdentity(paper)}: expected ${expected.join(',')}, found ${actual.join(',')}`);
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
  const match = normalized.match(
    /^(\d{4})\s*-\s*(?:(Paper|Sample Paper|Deferred Exam Paper)\s*-\s*)?Section\s*([AB12])\s*-\s*Question\s*(\d{1,2})\b/i,
  );
  if (!match) throw new Error(`Unparseable Economics heading: ${heading}`);
  const edition = (match[2] ?? 'main').toLowerCase();
  return {
    year: Number(match[1]),
    edition,
    section: ({ 1: 'A', 2: 'B' }[match[3].toUpperCase()] ?? match[3].toUpperCase()),
    question: Number(match[4]),
    sitting: edition.includes('deferred') ? 'deferred' : edition.includes('sample') ? 'sample' : 'main',
  };
};

const localNumber = parsed => (
  parsed.year <= 2020
    ? parsed.section === 'A' ? String(parsed.question) : `B${parsed.question}`
    : String(parsed.question)
);
const referenceNumber = parsed => `${parsed.section}${parsed.question}`;
const englishPaper = (level, year) => {
  const candidates = localPapers.filter(paper => (
    paper.level === level && paper.lang === 'ev' && paper.year === year
  ));
  if (candidates.length > 1) throw new Error(`Ambiguous ${level} English Economics paper for ${year}`);
  return candidates[0] ?? null;
};

const blockedReason = parsed => {
  if (parsed.year < 2010) {
    return 'The entitled local SEC Economics corpus currently begins at 2010. This factual heading is retained pending acquisition and independent verification of the official paper and marking scheme; no StudyClix-hosted question image or PDF is copied.';
  }
  if (parsed.sitting === 'sample') {
    return 'The entitled Paper Trail corpus does not currently contain this new-specification sample paper. The factual heading is retained pending acquisition and independent verification from an official source; no StudyClix-hosted question image or PDF is copied.';
  }
  if (parsed.sitting === 'deferred') {
    return 'The entitled Paper Trail corpus does not currently contain this deferred-sitting booklet. The factual heading is retained pending acquisition and independent verification from an official source; no StudyClix-hosted question image or PDF is copied.';
  }
  return null;
};

const associations = [];
for (const level of LEVELS) {
  for (const topic of reference.levels[level].topics) {
    for (const heading of topic.officialQuestionHeadings) {
      const parsed = parseHeading(heading);
      const explicitBlock = blockedReason(parsed);
      const paper = explicitBlock ? null : englishPaper(level, parsed.year);
      if (explicitBlock || !paper) {
        associations.push({
          topicId: topic.id,
          level,
          heading,
          ...parsed,
          resolution: 'source-blocked',
          referenceQuestionNumber: referenceNumber(parsed),
          reason: explicitBlock ?? 'No matching entitled local SEC paper variant is present. The factual heading is retained pending acquisition and independent verification; no StudyClix-hosted question image or PDF is copied.',
        });
        continue;
      }

      const number = localNumber(parsed);
      const localQuestion = paper.q.find(question => question.n === number);
      if (!localQuestion) {
        throw new Error(`${heading}: no local ${level} ${parsed.year} Q${number}`);
      }
      associations.push({
        topicId: topic.id,
        level,
        heading,
        ...parsed,
        resolution: 'matched',
        target: {
          level,
          lang: 'ev',
          year: parsed.year,
          paperKey: paper.paperKey,
          fileid: paper.fileid,
          questionNumber: number,
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
if (referenceOfficialAssociations !== 1120 || referenceMockAssociations !== 731 || referenceReportedAssociations !== 1851) {
  throw new Error('Economics factual audit totals changed unexpectedly');
}
if (associations.length !== referenceOfficialAssociations) {
  throw new Error(`Expected ${referenceOfficialAssociations} reconciliations, found ${associations.length}`);
}

const exactTopicsByCard = new Map();
for (const association of associations.filter(item => item.resolution === 'matched')) {
  const key = [association.level, association.year, association.target.questionNumber].join('|');
  const topics = exactTopicsByCard.get(key) ?? [];
  const index = topicIndex.get(association.topicId);
  if (index === undefined) throw new Error(`Unknown topic ${association.topicId}`);
  if (!topics.includes(index)) topics.push(index);
  exactTopicsByCard.set(key, topics);
}

const fallbackTopicForNode = (level, nodeId) => {
  const candidates = allTopics
    .map((topic, index) => ({ topic, index }))
    .filter(({ topic }) => topicLevel.get(topic.id) === level && curriculumCrosswalk[topic.id].includes(nodeId))
    .sort((left, right) => (
      curriculumCrosswalk[left.topic.id].length - curriculumCrosswalk[right.topic.id].length
      || left.index - right.index
    ));
  if (!candidates.length) throw new Error(`No ${level} exam topic covers canonical node ${nodeId}`);
  return candidates[0].index;
};

const questionMappings = [];
const retainedLocalCards = [];
const retainedLogical = new Set();
for (const paper of localPapers) {
  for (const question of paper.q) {
    const logicalKey = [paper.level, paper.year, question.n].join('|');
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
          questionNumber: question.n,
          canonicalNodeIds: [question.primary, question.secondary].filter(Boolean),
          topicIds: indexes.map(index => allTopics[index].id),
          resolution: 'retained-local',
          reason: 'Entitled SEC card preserved locally although the factual reference snapshot has no association for this top-level question.',
        });
      }
    }
    if (!indexes.length) throw new Error(`${paperIdentity(paper)} Q${question.n}: empty topic mapping`);
    questionMappings.push([
      paper.level === 'higher' ? 'h' : 'o',
      paper.lang === 'ev' ? 'e' : 'i',
      paper.year,
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
  item.target.questionNumber,
].join('|'))).size;
const distinctStudentFacingQuestions = localPapers
  .filter(paper => paper.lang === 'ev')
  .reduce((sum, paper) => sum + paper.q.length, 0);
const physicalMappings = localPapers.reduce((sum, paper) => sum + paper.q.length, 0);

if (matchedAssociations.length !== 903 || sourceBlockedAssociations.length !== 217) {
  throw new Error(`Unexpected Economics reconciliation split: ${matchedAssociations.length}/${sourceBlockedAssociations.length}`);
}
if (exactTopicsByCard.size !== 517 || retainedLocalCards.length !== 32) {
  throw new Error(`Expected 517 matched + 32 retained logical cards, found ${exactTopicsByCard.size} + ${retainedLocalCards.length}`);
}
if (physicalMappings !== 1098 || distinctStudentFacingQuestions !== 549 || questionMappings.length !== 1098) {
  throw new Error('Economics local corpus totals changed unexpectedly');
}

const hostedAnchorMaps = localPapers.filter(paper => (
  fs.existsSync(path.join(HOSTED_ROOT, String(paper.year), `${paper.fileid}.json`))
));
for (const paper of localPapers) {
  if (paper.year > 2020 && paper.year !== 2025) continue;
  const hasClassic = fs.existsSync(path.join(HERE, 'answers', String(paper.year), `${paper.fileid}.json`));
  const hasHosted = fs.existsSync(path.join(HOSTED_ROOT, String(paper.year), `${paper.fileid}.json`));
  if (!hasClassic && !hasHosted) throw new Error(`${paperIdentity(paper)} has no question anchor map`);
  if (paper.year <= 2020 && !hasHosted) throw new Error(`${paperIdentity(paper)} lacks Section-B hosted anchors`);
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
const sittingCode = { main: 'm', deferred: 'd', sample: 's' };
const partReferences = associations.map(association => [
  topicIndex.get(association.topicId),
  association.year,
  sittingCode[association.sitting],
  association.resolution === 'matched'
    ? association.target.questionNumber
    : referenceNumber(association),
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
  hostedAnchorMaps: hostedAnchorMaps.length,
  preservedBaselineVariants: preservationBaseline.length,
  preservedBaselineCards,
  emptyReferenceTopics: allTopics.filter(topic => topic.officialQuestionHeadings.length === 0).map(topic => topic.id),
};

const evidence = {
  schemaVersion: 1,
  subjectId: reference.subjectId,
  capturedAt: reference.capturedAt,
  reference: reference.reference,
  policy: {
    curriculumAuthority: 'NCCA/Curriculum Online',
    examAuthority: 'State Examinations Commission',
    commercialReferenceUse: 'Factual topic labels, headings, and counts only.',
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
