#!/usr/bin/env node
/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 *
 * Reconcile factual Chemistry reference headings with the entitled SEC corpus.
 * The official outgoing and redeveloped curricula remain canonical.
 */

import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const HERE = path.dirname(fileURLToPath(import.meta.url));
const ROOT = path.resolve(HERE, '../..');
const SUBJECT_ID = 'chemistry';
const TAGS_PATH = path.join(HERE, 'topic-tags/tags/chemistry.json');
const REFERENCE_PATH = path.join(ROOT, 'data/examTopics/chemistry.json');
const CURRICULUM_CROSSWALK_PATH = path.join(
  ROOT, 'data/examTopics/chemistry-curriculum-crosswalk.json',
);
const REVIEWED_2026_PATH = path.join(
  ROOT, 'data/examTopics/chemistry-2026-exam-topic-map.json',
);
const REVIEWED_OMISSIONS_PATH = path.join(
  ROOT, 'data/examTopics/chemistry-reference-omissions-topic-map.json',
);
const OUTPUT_PATH = path.join(
  ROOT, 'data/examTopics/chemistry-local-crosswalk.json',
);
const RUNTIME_PATH = path.join(ROOT, 'data/examTopics/chemistry-runtime.json');
const BASELINE_PATH = path.join(
  ROOT, 'test/fixtures/chemistryTopicQuestionBaseline.json',
);
const HOSTED_ROOT = path.join(ROOT, 'public/paper-anchors');

const reference = JSON.parse(fs.readFileSync(REFERENCE_PATH, 'utf8'));
const curriculumCrosswalk = JSON.parse(
  fs.readFileSync(CURRICULUM_CROSSWALK_PATH, 'utf8'),
);
const reviewed2026 = JSON.parse(fs.readFileSync(REVIEWED_2026_PATH, 'utf8'));
const reviewedOmissions = JSON.parse(
  fs.readFileSync(REVIEWED_OMISSIONS_PATH, 'utf8'),
);
const localPapers = JSON.parse(fs.readFileSync(TAGS_PATH, 'utf8'));
const preservationBaseline = JSON.parse(fs.readFileSync(BASELINE_PATH, 'utf8'));

const VARIANTS = [
  'higher-new-course',
  'higher-old-course',
  'ordinary-new-course',
  'ordinary-old-course',
];
const allTopics = VARIANTS.flatMap(
  variant => reference.variants[variant].topics.map(topic => ({
    ...topic,
    variant,
    level: variant.startsWith('higher') ? 'higher' : 'ordinary',
    course: variant.includes('new-course') ? 'new' : 'old',
  })),
);
const topicIndex = new Map(allTopics.map((topic, index) => [topic.id, index]));

const referenceTopicIds = allTopics.map(topic => topic.id).sort();
const crosswalkTopicIds = Object.keys(curriculumCrosswalk).sort();
if (JSON.stringify(referenceTopicIds) !== JSON.stringify(crosswalkTopicIds)) {
  throw new Error(
    'Chemistry curriculum crosswalk must cover every reference topic exactly once',
  );
}
for (const topic of allTopics) {
  const nodes = curriculumCrosswalk[topic.id];
  if (!Array.isArray(nodes) || !nodes.length || new Set(nodes).size !== nodes.length) {
    throw new Error(`${topic.id}: curriculum crosswalk must contain unique nodes`);
  }
  const wantedPrefix = topic.course === 'new' ? 'chem-' : 'chemistry-';
  for (const node of nodes) {
    if (!node.startsWith(wantedPrefix)) {
      throw new Error(`${topic.id}: invalid ${topic.course}-course node ${node}`);
    }
  }
}
for (const [key, topicIds] of Object.entries(reviewed2026.questions)) {
  if (!/^(higher|ordinary)\|(?:[1-9]|1[01])$/.test(key)) {
    throw new Error(`Invalid reviewed 2026 identity: ${key}`);
  }
  for (const id of topicIds) {
    if (!topicIndex.has(id)) throw new Error(`Unknown reviewed 2026 topic: ${id}`);
  }
}
if (Object.keys(reviewed2026.questions).length !== 22) {
  throw new Error('The reviewed 2026 Chemistry map must contain 22 questions');
}
if (Object.keys(reviewedOmissions.questions).length !== 10) {
  throw new Error('The Chemistry reference-omission map must contain 10 questions');
}
for (const [key, topicIds] of Object.entries(reviewedOmissions.questions)) {
  if (!/^(higher|ordinary)\|\d{4}\|(?:[1-9]|1[01])$/.test(key)) {
    throw new Error(`Invalid reviewed omission identity: ${key}`);
  }
  for (const id of topicIds) {
    if (!topicIndex.has(id)) throw new Error(`Unknown reviewed omission topic: ${id}`);
  }
}

const paperIdentity = paper => [
  paper.level, paper.lang, paper.year, paper.paperKey, paper.fileid,
].join('|');
const localPaperIds = localPapers.map(paperIdentity);
const duplicatePaperIds = localPaperIds.filter(
  (identity, index) => localPaperIds.indexOf(identity) !== index,
);
if (duplicatePaperIds.length) {
  throw new Error(
    `Duplicate Chemistry variants: ${[...new Set(duplicatePaperIds)].join(', ')}`,
  );
}
if (localPapers.length !== 68) {
  throw new Error(`Expected 68 Chemistry variants, found ${localPapers.length}`);
}
const physicalCards = localPapers.reduce((sum, paper) => sum + paper.q.length, 0);
if (physicalCards !== 748) {
  throw new Error(`Expected 748 Chemistry physical cards, found ${physicalCards}`);
}

const expectedNumbers = Array.from({ length: 11 }, (_, index) => String(index + 1));
for (const paper of localPapers) {
  if (
    !['higher', 'ordinary'].includes(paper.level)
    || !['ev', 'iv'].includes(paper.lang)
    || paper.paperKey !== 'single'
    || JSON.stringify(paper.q.map(question => question.n))
      !== JSON.stringify(expectedNumbers)
  ) {
    throw new Error(`Unexpected Chemistry paper identity: ${paperIdentity(paper)}`);
  }
  const hostedPath = path.join(
    HOSTED_ROOT, String(paper.year), `${paper.fileid}.json`,
  );
  if (!fs.existsSync(hostedPath)) {
    throw new Error(`${paperIdentity(paper)}: missing hosted paper anchor map`);
  }
  const hosted = JSON.parse(fs.readFileSync(hostedPath, 'utf8'));
  if (
    hosted.paperOnly !== 1
    || JSON.stringify(hosted.q.map(question => question.n))
      !== JSON.stringify(expectedNumbers)
  ) {
    throw new Error(`${hostedPath}: hosted identities do not match tags`);
  }
}

let preservedBaselineTasks = 0;
for (const baselinePaper of preservationBaseline) {
  const live = localPapers.find(
    paper => paperIdentity(paper) === paperIdentity(baselinePaper),
  );
  if (!live) {
    throw new Error(`Preservation failure: missing ${paperIdentity(baselinePaper)}`);
  }
  const liveNumbers = live.q.map(question => question.n);
  if (JSON.stringify(liveNumbers) !== JSON.stringify(baselinePaper.questions)) {
    throw new Error(`Preservation failure: changed ${paperIdentity(baselinePaper)}`);
  }
  preservedBaselineTasks += baselinePaper.questions.length;
}

const parseHeading = heading => {
  // Keep the provider's factual typography exactly, including its occasional
  // double spaces and lower-case short-question tokens.
  const normalized = heading.trim();
  const match = normalized.match(
    /^(\d{4}) - (.*?Question\s+)([A-Za-z]|\d+)(.*)$/,
  );
  if (!match) throw new Error(`Unparseable Chemistry heading: ${heading}`);
  const [, yearText, prefix, token, tail] = match;
  const sitting = /Deferred Exam Paper/i.test(prefix)
    ? 'deferred'
    : /Sample Paper/i.test(prefix)
      ? 'sample'
      : 'main';
  let questionNumber = token;
  if (/^[A-Za-z]$/.test(token)) {
    // StudyClix has thirteen legacy headings written as "Question b" etc.
    // They are parts of the paper's mixed short-answer Q4, except two 2017
    // headings whose preceding "Section 11" identifies Q11(c)(a/b).
    questionNumber = /Section\s+11\b/i.test(prefix) ? '11' : '4';
  }
  return {
    year: Number(yearText),
    sitting,
    prefix,
    questionToken: token,
    questionNumber,
    tail,
    questionNumbers: [questionNumber],
  };
};

const englishPaper = (level, year, number) => {
  const candidates = localPapers.filter(paper => (
    paper.level === level
    && paper.lang === 'ev'
    && paper.year === year
    && paper.q.some(question => question.n === number)
  ));
  if (candidates.length > 1) {
    throw new Error(`Ambiguous ${level} Chemistry ${year} Q${number}`);
  }
  return candidates[0] ?? null;
};

const associations = [];
const exactTopicsByCard = new Map();
for (const topic of allTopics) {
  for (const heading of topic.officialQuestionHeadings) {
    const parsed = parseHeading(heading);
    const target = parsed.sitting === 'main'
      ? englishPaper(topic.level, parsed.year, parsed.questionNumber)
      : null;
    if (target) {
      const key = [topic.level, parsed.year, parsed.questionNumber].join('|');
      const indexes = exactTopicsByCard.get(key) ?? [];
      const index = topicIndex.get(topic.id);
      if (index === undefined) throw new Error(`Unknown Chemistry topic ${topic.id}`);
      if (!indexes.includes(index)) indexes.push(index);
      exactTopicsByCard.set(key, indexes);
      associations.push({
        topicId: topic.id,
        variant: topic.variant,
        level: topic.level,
        course: topic.course,
        heading,
        ...parsed,
        paperKey: 'single',
        resolution: 'matched',
        targets: [{
          level: topic.level,
          lang: 'ev',
          year: parsed.year,
          paperKey: 'single',
          fileid: target.fileid,
          questionNumber: parsed.questionNumber,
        }],
      });
      continue;
    }

    const reason = parsed.sitting === 'sample'
      ? 'Provider or official sample-paper content is not part of the entitled local SEC examination corpus. Its factual heading is retained; no question image or PDF is copied.'
      : parsed.sitting === 'deferred'
        ? 'The entitled corpus does not contain this deferred Chemistry sitting. Its factual heading is retained; no StudyClix-hosted question image or PDF is copied.'
        : 'No matching entitled local SEC Chemistry card is present. Its factual heading is retained pending an independently verified official source.';
    associations.push({
      topicId: topic.id,
      variant: topic.variant,
      level: topic.level,
      course: topic.course,
      heading,
      ...parsed,
      paperKey: 'single',
      resolution: 'source-blocked',
      reason,
    });
  }
}

const isFormatTopic = id => (
  id.includes('-experiment-')
  || id.endsWith('-q4')
);

const oldFallbackTopics = (level, number, nodeIds) => {
  const indexes = [];
  const add = index => {
    if (index !== undefined && !indexes.includes(index)) indexes.push(index);
  };
  for (const [index, topic] of allTopics.entries()) {
    if (topic.level !== level || topic.course !== 'old' || isFormatTopic(topic.id)) {
      continue;
    }
    if (nodeIds.some(nodeId => curriculumCrosswalk[topic.id].includes(nodeId))) {
      add(index);
    }
  }
  const formatId = level === 'higher'
    ? number === '1'
      ? 'chemistry-higher-old-course-experiment-q1-titration'
      : number === '2'
        ? 'chemistry-higher-old-course-experiment-q2-organic'
        : number === '3'
          ? 'chemistry-higher-old-course-experiment-q3-other'
          : number === '4'
            ? 'chemistry-higher-old-course-q4'
            : null
    : ['1', '2', '3'].includes(number)
      ? 'chemistry-ordinary-old-course-experiment-questions'
      : null;
  if (formatId) add(topicIndex.get(formatId));
  return indexes;
};

// Content-equivalence bridge used only when a valid local question post-dates
// the captured reference headings. It does not claim old and new specifications
// are identical; it makes suitable outgoing-syllabus practice discoverable
// under the closest redeveloped unit.
const OLD_TO_NEW_NODES = {
  'chemistry-0-0': ['chem-1-3'],
  'chemistry-0-1': ['chem-1-2'],
  'chemistry-0-2': ['chem-1-2'],
  'chemistry-0-3': ['chem-1-2', 'chem-1-3'],
  'chemistry-0-4': ['chem-3-5'],
  'chemistry-1-0': ['chem-2-1'],
  'chemistry-1-1': ['chem-2-1'],
  'chemistry-1-2': ['chem-2-1'],
  'chemistry-1-3': ['chem-2-1'],
  'chemistry-1-4': ['chem-2-2'],
  'chemistry-1-5': ['chem-3-5'],
  'chemistry-2-0': ['chem-1-1', 'chem-2-3'],
  'chemistry-2-1': ['chem-2-3'],
  'chemistry-2-2': ['chem-1-4'],
  'chemistry-2-3': ['chem-1-4'],
  'chemistry-2-4': ['chem-1-4'],
  'chemistry-3-0': ['chem-1-4', 'chem-4-1'],
  'chemistry-3-1': ['chem-3-4'],
  'chemistry-3-2': ['chem-4-1'],
  'chemistry-3-3': ['chem-3-4'],
  'chemistry-4-0': ['chem-2-4', 'chem-4-3'],
  'chemistry-4-1': ['chem-2-4', 'chem-4-2'],
  'chemistry-4-2': ['chem-2-4', 'chem-4-2'],
  'chemistry-4-3': ['chem-3-1'],
  'chemistry-4-4': ['chem-2-4', 'chem-4-3'],
  'chemistry-4-5': ['chem-3-1', 'chem-4-3'],
  'chemistry-5-0': ['chem-3-2'],
  'chemistry-5-1': ['chem-3-2'],
  'chemistry-6-0': ['chem-2-4', 'chem-4-2'],
  'chemistry-6-1': ['chem-2-4', 'chem-4-2'],
  'chemistry-6-2': ['chem-4-2'],
  'chemistry-6-3': ['chem-4-2'],
  'chemistry-6-4': ['chem-4-3'],
  'chemistry-7-0': ['chem-3-3'],
  'chemistry-7-1': ['chem-3-3'],
  'chemistry-7-2': ['chem-3-3'],
  'chemistry-8-0': ['chem-3-4', 'chem-4-3'],
  'chemistry-8-1': ['chem-4-3'],
  'chemistry-8-2': ['chem-4-3'],
  'chemistry-8-3': ['chem-4-3'],
  'chemistry-9-0': ['chem-4-3'],
  'chemistry-9-1': ['chem-4-3'],
  'chemistry-10-0': ['chem-4-3'],
  'chemistry-10-1': ['chem-4-3'],
  'chemistry-10-2': ['chem-4-3'],
  'chemistry-10-3': ['chem-4-3'],
  'chemistry-10-4': ['chem-4-3'],
  'chemistry-11-0': ['chem-1-1', 'chem-2-1', 'chem-2-2'],
  'chemistry-11-1': ['chem-4-2'],
  'chemistry-11-2': ['chem-1-1', 'chem-1-3', 'chem-3-5'],
  'chemistry-12-0': ['chem-3-5'],
  'chemistry-12-1': ['chem-3-5'],
  'chemistry-12-2': ['chem-3-5'],
  'chemistry-12-3': ['chem-3-5'],
  'chemistry-12-4': ['chem-3-5'],
};

const newFallbackTopics = (level, nodeIds) => {
  const newNodeIds = [...new Set(nodeIds.flatMap(nodeId => {
    const mapped = OLD_TO_NEW_NODES[nodeId];
    if (!mapped) throw new Error(`No redeveloped Chemistry bridge for ${nodeId}`);
    return mapped;
  }))];
  return allTopics
    .map((topic, index) => ({ topic, index }))
    .filter(({ topic }) => (
      topic.level === level
      && topic.course === 'new'
      && newNodeIds.some(nodeId => curriculumCrosswalk[topic.id].includes(nodeId))
    ))
    .map(({ index }) => index);
};

const logicalEnglishPapers = localPapers.filter(paper => paper.lang === 'ev');
const questionMappings = [];
const retainedLocalCards = [];
for (const paper of logicalEnglishPapers) {
  for (const question of paper.q) {
    const logicalKey = [paper.level, paper.year, question.n].join('|');
    let indexes = exactTopicsByCard.get(logicalKey);
    let resolution = 'matched';
    if (!indexes && paper.year === 2026) {
      const ids = reviewed2026.questions[`${paper.level}|${question.n}`];
      if (!ids) throw new Error(`Missing reviewed 2026 mapping for ${logicalKey}`);
      indexes = ids.map(id => topicIndex.get(id));
      resolution = 'retained-local-reviewed';
    }
    if (!indexes) {
      const ids = reviewedOmissions.questions[logicalKey];
      if (ids) {
        indexes = ids.map(id => topicIndex.get(id));
        resolution = 'retained-local-reviewed';
      }
    }
    if (!indexes) {
      const nodeIds = [question.primary, question.secondary].filter(Boolean);
      indexes = [...new Set([
        ...newFallbackTopics(paper.level, nodeIds),
        ...oldFallbackTopics(paper.level, question.n, nodeIds),
      ])];
      resolution = 'retained-local-canonical-fallback';
    }
    if (!indexes.length || indexes.some(index => index === undefined)) {
      throw new Error(`${logicalKey}: empty or invalid topic mapping`);
    }
    questionMappings.push([
      paper.level === 'higher' ? 'h' : 'o',
      paper.year - 2000,
      question.n,
      indexes,
    ]);
    if (resolution !== 'matched') {
      retainedLocalCards.push({
        level: paper.level,
        year: paper.year,
        paperKey: paper.paperKey,
        fileid: paper.fileid,
        questionNumber: question.n,
        canonicalNodeIds: [question.primary, question.secondary].filter(Boolean),
        topicIds: indexes.map(index => allTopics[index].id),
        resolution,
        reason: resolution === 'retained-local-reviewed'
          ? paper.year === 2026
            ? 'Official SEC 2026 task retained from direct paper review; it post-dates the factual reference snapshot.'
            : 'Entitled SEC task omitted from the factual reference snapshot and retained from direct review of the official paper.'
          : 'Entitled SEC task preserved although the factual reference snapshot has no association for this independently selectable question.',
      });
    }
  }
}

const reported = allTopics.reduce(
  (sum, topic) => sum + topic.reportedQuestionCount, 0,
);
const official = allTopics.reduce(
  (sum, topic) => sum + topic.officialQuestionHeadings.length, 0,
);
const mocks = allTopics.reduce(
  (sum, topic) => sum + topic.mockQuestionCount, 0,
);
const providerSamples = allTopics.reduce(
  (sum, topic) => sum + topic.providerSampleQuestionCount, 0,
);
if (
  allTopics.length !== 76
  || reported !== 4026
  || official !== 2265
  || mocks !== 1612
  || providerSamples !== 149
  || reported !== official + mocks + providerSamples
) {
  throw new Error(
    `Chemistry audit totals changed: ${allTopics.length}/${reported}/`
    + `${official}/${mocks}/${providerSamples}`,
  );
}
if (questionMappings.length !== 374) {
  throw new Error(
    `Expected 374 logical mappings, found ${questionMappings.length}`,
  );
}
if (retainedLocalCards.some(card => (
  card.resolution === 'retained-local-canonical-fallback'
))) {
  throw new Error('Every reference-omitted Chemistry task must be directly reviewed');
}

const prefixes = [...new Set(associations.map(item => item.prefix))];
const tails = [...new Set(associations.map(item => item.tail))];
const prefixIndex = new Map(prefixes.map((value, index) => [value, index]));
const tailIndex = new Map(tails.map((value, index) => [value, index]));
const compactPartReferences = associations.map(item => [
  topicIndex.get(item.topicId),
  item.year - 2000,
  prefixIndex.get(item.prefix),
  item.questionToken,
  tailIndex.get(item.tail),
]);
if (compactPartReferences.some(row => row.some(value => value === undefined))) {
  throw new Error('A compact Chemistry part reference has an unknown index');
}

const groups = [];
for (const variant of VARIANTS) {
  const variantData = reference.variants[variant];
  const levelCode = variant.startsWith('higher') ? 'h' : 'o';
  const courseCode = variant.includes('new-course') ? 'n' : 'o';
  if (variantData.groups.length) {
    for (const group of variantData.groups) {
      groups.push([
        levelCode,
        courseCode,
        group.id,
        `${variantData.label} · ${group.label}`,
        group.topicIds.map(id => {
          const index = topicIndex.get(id);
          if (index === undefined) throw new Error(`Unknown Chemistry group topic ${id}`);
          return index;
        }),
      ]);
    }
  } else {
    groups.push([
      levelCode,
      courseCode,
      `chemistry-${variant}`,
      variantData.label,
      variantData.topics.map(topic => {
        const index = topicIndex.get(topic.id);
        if (index === undefined) throw new Error(`Unknown Chemistry topic ${topic.id}`);
        return index;
      }),
    ]);
  }
}

const compactTopics = allTopics.map(topic => {
  const idPrefix = `${SUBJECT_ID}-${topic.variant}-`;
  if (!topic.id.startsWith(idPrefix)) {
    throw new Error(`${topic.id}: expected prefix ${idPrefix}`);
  }
  const slug = topic.id.slice(idPrefix.length);
  const variantData = reference.variants[topic.variant];
  const group = variantData.groups.find(candidate => (
    candidate.topicIds.includes(topic.id)
  ));
  const groupPrefix = `${SUBJECT_ID}-${topic.variant}-`;
  const groupSlug = group ? group.id.slice(groupPrefix.length) : '';
  const reconstructedPath = [
    '',
    'leaving-certificate',
    SUBJECT_ID,
    topic.variant,
    groupSlug,
    slug,
  ].filter((segment, index) => index === 0 || segment).join('/');
  if (reconstructedPath !== topic.sourcePath) {
    throw new Error(
      `${topic.id}: compact path mismatch ${reconstructedPath} != ${topic.sourcePath}`,
    );
  }
  return [
    slug,
    topic.label,
    topic.mockQuestionCount,
    topic.providerSampleQuestionCount,
    curriculumCrosswalk[topic.id],
    topic.reportedQuestionCount,
  ];
});

const runtime = {
  v: 1,
  subjectId: SUBJECT_ID,
  capturedAt: reference.capturedAt,
  referenceProvider: reference.reference.provider,
  groups,
  topics: compactTopics,
  headingPrefixes: prefixes,
  headingTails: tails,
  partReferences: compactPartReferences,
  questionMappings,
};

const matchedAssociations = associations.filter(
  item => item.resolution === 'matched',
);
const sourceBlockedAssociations = associations.filter(
  item => item.resolution === 'source-blocked',
);
const matchedLogicalCards = new Set(matchedAssociations.map(item => [
  item.level, item.year, item.questionNumber,
].join('|'))).size;
const localCrosswalk = {
  schemaVersion: 1,
  subjectId: SUBJECT_ID,
  capturedAt: reference.capturedAt,
  referenceProvider: reference.reference.provider,
  rightsBoundary: reference.reference.excludedContent,
  providerSamplePolicy: reference.reference.providerSamplePolicy,
  summary: {
    referenceTopics: allTopics.length,
    referenceReportedAssociations: reported,
    referenceOfficialAssociations: official,
    referenceMockAssociations: mocks,
    referenceProviderSampleAssociations: providerSamples,
    matchedAssociations: matchedAssociations.length,
    sourceBlockedAssociations: sourceBlockedAssociations.length,
    matchedLogicalCards,
    retainedLocalLogicalCards: retainedLocalCards.length,
    localPaperVariants: localPapers.length,
    localPhysicalCards: physicalCards,
    localLogicalQuestions: questionMappings.length,
    preservedBaselineVariants: preservationBaseline.length,
    preservedBaselineTasks,
  },
  associations,
  retainedLocalCards,
};

fs.writeFileSync(OUTPUT_PATH, `${JSON.stringify(localCrosswalk, null, 2)}\n`);
fs.writeFileSync(RUNTIME_PATH, JSON.stringify(runtime));

console.log(JSON.stringify(localCrosswalk.summary, null, 2));
console.log(`runtimeBytes ${fs.statSync(RUNTIME_PATH).size}`);
