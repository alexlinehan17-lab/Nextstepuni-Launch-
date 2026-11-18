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

/* A deferred sitting's booklet ("LC562ALP014EV-deferred.pdf") is its own
 * paper, numbered as June's. Its questions join on the booklet
 * (deferredQuestionMappings), never on June's year and number, so they
 * neither replace nor merge with June's question of the same number. */
const isDeferred = paper => /-deferred\.pdf$/i.test(paper.fileid);
const junePapers = localPapers.filter(paper => !isDeferred(paper));
const deferredPapers = localPapers.filter(isDeferred);

const paperIds = localPapers.map(paperIdentity);
const duplicatePaperIds = paperIds.filter((identity, index) => paperIds.indexOf(identity) !== index);
if (duplicatePaperIds.length) {
  throw new Error(`Duplicate DCG paper variants: ${[...new Set(duplicatePaperIds)].join(', ')}`);
}
if (junePapers.length !== 132) {
  throw new Error(`Expected 132 DCG variants, found ${junePapers.length}`);
}
/* The deferred sittings in the Atlas (each joins with its Mark Bank cards):
 * a Section A sheet and a Sections B and C booklet each, English, Higher.
 * Per sitting, the reference's deferred headings it matches, the logical
 * questions they name, and the questions it heads none of (C-5, retained
 * under Assemblies by design_and_communication_graphics.py). */
const DEFERRED_EXPECTED = new Map([
  [2022, { matched: 13, logical: 11, retained: 1 }],
  [2023, { matched: 11, logical: 11, retained: 1 }],
]);
const deferredYears = [...new Set(deferredPapers.map(paper => paper.year))].sort();
for (const year of deferredYears) {
  const booklets = deferredPapers.filter(paper => paper.year === year);
  if (!DEFERRED_EXPECTED.has(year) || booklets.length !== 2
      || booklets.some(paper => paper.level !== 'higher' || paper.lang !== 'ev')
      || new Set(booklets.map(paper => paper.paperKey)).size !== 2) {
    throw new Error(`${year}: expected the deferred Section A sheet and Sections B and C booklet, English, Higher`);
  }
}
const deferredExpected = deferredYears.reduce((sum, year) => {
  const expected = DEFERRED_EXPECTED.get(year);
  return {
    matched: sum.matched + expected.matched,
    logical: sum.logical + expected.logical,
    retained: sum.retained + expected.retained,
  };
}, { matched: 0, logical: 0, retained: 0 });

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

const EnglishPaper = (level, year, paperKey, sitting = 'main') => {
  const candidates = (sitting === 'deferred' ? deferredPapers : junePapers).filter(paper => (
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
  if (parsed.sitting === 'deferred'
      && !deferredPapers.some(paper => paper.year === parsed.year)) {
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
      const paper = explicitBlock ? null : EnglishPaper(level, parsed.year, slot.paperKey, parsed.sitting);
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

// A deferred question's key carries its sitting; June's is unchanged.
const logicalKeyFor = (level, year, sitting, paperKey, questionNumber) => [
  level,
  year,
  ...(sitting === 'deferred' ? ['deferred'] : []),
  paperKey,
  questionNumber,
].join('|');
const exactTopicsByCard = new Map();
for (const association of associations.filter(item => item.resolution === 'matched')) {
  const key = logicalKeyFor(
    association.level,
    association.year,
    association.sitting,
    association.paperKey,
    association.questionNumber,
  );
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
const deferredQuestionMappings = [];
const retainedLocalCards = [];
const retainedLogical = new Set();
for (const paper of localPapers) {
  const sitting = isDeferred(paper) ? 'deferred' : 'main';
  for (const question of paper.q) {
    const logicalKey = logicalKeyFor(paper.level, paper.year, sitting, paper.paperKey, question.n);
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
          ...(sitting === 'deferred' ? { sitting, fileid: paper.fileid } : {}),
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
    if (sitting === 'deferred') {
      deferredQuestionMappings.push([
        paper.level === 'higher' ? 'h' : 'o',
        paper.lang === 'ev' ? 'e' : 'i',
        paper.year,
        paper.paperKey === 'section-a' ? 'a' : 's',
        paper.fileid,
        question.n,
        indexes,
      ]);
      continue;
    }
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
  ...(item.sitting === 'deferred' ? ['deferred'] : []),
  item.paperKey,
  item.questionNumber,
].join('|'))).size;
const physicalMappings = localPapers.reduce((sum, paper) => sum + paper.q.length, 0);
const distinctStudentFacingQuestions = localPapers
  .filter(paper => paper.lang === 'ev')
  .reduce((sum, paper) => sum + paper.q.length, 0);

// June: 386 matched (41 blocked), 347 logical cards, 49 retained, 792
// mappings. Each deferred sitting in the Atlas moves its headings from blocked
// to matched and adds its own twelve questions (DEFERRED_EXPECTED).
const expectedMatched = 386 + deferredExpected.matched;
if (matchedAssociations.length !== expectedMatched
    || sourceBlockedAssociations.length !== 427 - expectedMatched) {
  throw new Error(`Unexpected DCG reconciliation split: ${matchedAssociations.length}/${sourceBlockedAssociations.length}`);
}
if (exactTopicsByCard.size !== 347 + deferredExpected.logical
    || retainedLocalCards.length !== 49 + deferredExpected.retained) {
  throw new Error(`Expected ${347 + deferredExpected.logical} matched + ${49 + deferredExpected.retained} retained logical cards, found ${exactTopicsByCard.size} + ${retainedLocalCards.length}`);
}
const deferredQuestions = 12 * deferredYears.length;
if (physicalMappings !== 792 + deferredQuestions
    || distinctStudentFacingQuestions !== 396 + deferredQuestions
    || questionMappings.length !== 792
    || deferredQuestionMappings.length !== deferredQuestions) {
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
  ...(deferredQuestionMappings.length ? { deferredQuestionMappings } : {}),
  summary,
};

fs.writeFileSync(OUTPUT_PATH, `${JSON.stringify(evidence, null, 2)}\n`);
fs.writeFileSync(RUNTIME_PATH, `${JSON.stringify(runtime)}\n`);
console.log(JSON.stringify(summary, null, 2));
