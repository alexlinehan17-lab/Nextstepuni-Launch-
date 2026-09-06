#!/usr/bin/env node
/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 *
 * Reconcile factual Physics reference headings with the entitled SEC corpus.
 * The official outgoing syllabus and redeveloped specification remain the
 * canonical curriculum authorities.
 */

import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const HERE = path.dirname(fileURLToPath(import.meta.url));
const ROOT = path.resolve(HERE, '../..');
const SUBJECT_ID = 'physics';
const TAGS_PATH = path.join(HERE, 'topic-tags/tags/physics.json');
const REFERENCE_PATH = path.join(ROOT, 'data/examTopics/physics.json');
const CURRICULUM_CROSSWALK_PATH = path.join(
  ROOT, 'data/examTopics/physics-curriculum-crosswalk.json',
);
const REVIEWED_2026_PATH = path.join(
  ROOT, 'data/examTopics/physics-2026-exam-topic-map.json',
);
const REVIEWED_OMISSIONS_PATH = path.join(
  ROOT, 'data/examTopics/physics-reference-omissions-topic-map.json',
);
const OUTPUT_PATH = path.join(
  ROOT, 'data/examTopics/physics-local-crosswalk.json',
);
const RUNTIME_PATH = path.join(ROOT, 'data/examTopics/physics-runtime.json');
const BASELINE_PATH = path.join(
  ROOT, 'test/fixtures/physicsTopicQuestionBaseline.json',
);
const HOSTED_ROOT = path.join(ROOT, 'public/paper-anchors');

const readJson = file => JSON.parse(fs.readFileSync(file, 'utf8'));
const reference = readJson(REFERENCE_PATH);
const curriculumCrosswalk = readJson(CURRICULUM_CROSSWALK_PATH);
const reviewed2026 = readJson(REVIEWED_2026_PATH);
const reviewedOmissions = readJson(REVIEWED_OMISSIONS_PATH);
const localPapers = readJson(TAGS_PATH);
const preservationBaseline = readJson(BASELINE_PATH);

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
  const missing = referenceTopicIds.filter(id => !crosswalkTopicIds.includes(id));
  const extra = crosswalkTopicIds.filter(id => !referenceTopicIds.includes(id));
  throw new Error(
    `Physics curriculum crosswalk must cover every reference topic exactly once; `
    + `missing=${missing.join(',')} extra=${extra.join(',')}`,
  );
}
for (const topic of allTopics) {
  const nodes = curriculumCrosswalk[topic.id];
  if (!Array.isArray(nodes) || !nodes.length || new Set(nodes).size !== nodes.length) {
    throw new Error(`${topic.id}: curriculum crosswalk must contain unique nodes`);
  }
  const wantedPrefix = topic.course === 'new' ? 'phys-' : 'physics-';
  for (const node of nodes) {
    if (!node.startsWith(wantedPrefix)) {
      throw new Error(`${topic.id}: invalid ${topic.course}-course node ${node}`);
    }
  }
}

const validateReviewedMap = (questions, pattern, expected, label) => {
  if (Object.keys(questions).length !== expected) {
    throw new Error(`${label} must contain ${expected} questions`);
  }
  for (const [key, topicIds] of Object.entries(questions)) {
    if (!pattern.test(key)) throw new Error(`Invalid ${label} identity: ${key}`);
    if (!topicIds.length || new Set(topicIds).size !== topicIds.length) {
      throw new Error(`${key}: ${label} mapping must contain unique topics`);
    }
    const level = key.split('|')[0];
    for (const id of topicIds) {
      const index = topicIndex.get(id);
      if (index === undefined) throw new Error(`Unknown ${label} topic: ${id}`);
      if (allTopics[index].level !== level) {
        throw new Error(`${key}: cross-level ${label} topic ${id}`);
      }
    }
  }
};
validateReviewedMap(
  reviewed2026.questions,
  /^(higher|ordinary)\|(?:[1-9]|1[0-4])$/,
  28,
  'reviewed 2026 Physics map',
);
validateReviewedMap(
  reviewedOmissions.questions,
  /^(higher|ordinary)\|\d{4}\|(?:[1-9]|1[0-4])$/,
  13,
  'reviewed Physics reference-omission map',
);

const paperIdentity = paper => [
  paper.level, paper.lang, paper.year, paper.paperKey, paper.fileid,
].join('|');
const localPaperIds = localPapers.map(paperIdentity);
const duplicatePaperIds = localPaperIds.filter(
  (identity, index) => localPaperIds.indexOf(identity) !== index,
);
if (duplicatePaperIds.length) {
  throw new Error(
    `Duplicate Physics variants: ${[...new Set(duplicatePaperIds)].join(', ')}`,
  );
}
if (localPapers.length !== 68) {
  throw new Error(`Expected 68 Physics variants, found ${localPapers.length}`);
}
const physicalCards = localPapers.reduce((sum, paper) => sum + paper.q.length, 0);
if (physicalCards !== 864) {
  throw new Error(`Expected 864 Physics physical cards, found ${physicalCards}`);
}
for (const paper of localPapers) {
  const count = paper.year <= 2020 ? 12 : 14;
  const expectedNumbers = Array.from({ length: count }, (_, index) => String(index + 1));
  if (
    !['higher', 'ordinary'].includes(paper.level)
    || !['ev', 'iv'].includes(paper.lang)
    || paper.paperKey !== 'single'
    || JSON.stringify(paper.q.map(question => question.n))
      !== JSON.stringify(expectedNumbers)
  ) {
    throw new Error(`Unexpected Physics paper identity: ${paperIdentity(paper)}`);
  }
  const hostedPath = path.join(
    HOSTED_ROOT, String(paper.year), `${paper.fileid}.json`,
  );
  if (!fs.existsSync(hostedPath)) {
    throw new Error(`${paperIdentity(paper)}: missing hosted paper anchor map`);
  }
  const hosted = readJson(hostedPath);
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
  const liveNumbers = new Set(live.q.map(question => question.n));
  for (const number of baselinePaper.questions) {
    if (!liveNumbers.has(number)) {
      throw new Error(
        `Preservation failure: missing ${paperIdentity(baselinePaper)} Q${number}`,
      );
    }
    preservedBaselineTasks += 1;
  }
}

const parseHeading = heading => {
  // Keep the provider's factual typography exactly, including its occasional
  // double space and two duplicated lower-case short-question headings.
  const normalized = heading.trim();
  const match = normalized.match(
    /^(\d{4}) - (.*?Question\s+)([A-Za-z]|\d+)(.*)$/,
  );
  if (!match) throw new Error(`Unparseable Physics heading: ${heading}`);
  const [, yearText, prefix, token, tail] = match;
  const sitting = /Deferred Exam Paper/i.test(prefix)
    ? 'deferred'
    : /Sample Paper/i.test(prefix)
      ? 'sample'
      : 'main';
  const questionNumber = /^[A-Za-z]$/.test(token)
    ? /Section\s+11\b/i.test(prefix) ? '11' : null
    : token;
  if (!questionNumber) throw new Error(`Unknown Physics question token: ${heading}`);
  return {
    year: Number(yearText),
    sitting,
    prefix,
    questionToken: token,
    questionNumber,
    tail,
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
    throw new Error(`Ambiguous ${level} Physics ${year} Q${number}`);
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
      if (index === undefined) throw new Error(`Unknown Physics topic ${topic.id}`);
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
        ? 'The entitled corpus does not contain this deferred Physics sitting. Its factual heading is retained; no StudyClix-hosted question image or PDF is copied.'
        : 'No matching entitled local SEC Physics card is present. Its factual heading is retained pending an independently verified official source.';
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
      if (!ids) {
        throw new Error(
          `${logicalKey}: reference-omitted Physics task lacks direct SEC review`,
        );
      }
      indexes = ids.map(id => topicIndex.get(id));
      resolution = 'retained-local-reviewed';
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
        reason: paper.year === 2026
          ? 'Official SEC 2026 task retained from direct paper review; it post-dates the factual reference snapshot.'
          : 'Entitled SEC task omitted from the factual reference snapshot and retained from direct review of the official paper.',
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
  allTopics.length !== 113
  || reported !== 4701
  || official !== 2482
  || mocks !== 2051
  || providerSamples !== 168
  || reported !== official + mocks + providerSamples
) {
  throw new Error(
    `Physics audit totals changed: ${allTopics.length}/${reported}/`
    + `${official}/${mocks}/${providerSamples}`,
  );
}
if (questionMappings.length !== 432) {
  throw new Error(`Expected 432 logical mappings, found ${questionMappings.length}`);
}
if (retainedLocalCards.length !== 41) {
  throw new Error(
    `Expected 41 directly reviewed local mappings, found ${retainedLocalCards.length}`,
  );
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
  throw new Error('A compact Physics part reference has an unknown index');
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
          if (index === undefined) throw new Error(`Unknown Physics group topic ${id}`);
          return index;
        }),
      ]);
    }
  } else {
    groups.push([
      levelCode,
      courseCode,
      `physics-${variant}`,
      variantData.label,
      variantData.topics.map(topic => {
        const index = topicIndex.get(topic.id);
        if (index === undefined) throw new Error(`Unknown Physics topic ${topic.id}`);
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
  const group = variantData.groups.find(candidate => candidate.topicIds.includes(topic.id));
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
