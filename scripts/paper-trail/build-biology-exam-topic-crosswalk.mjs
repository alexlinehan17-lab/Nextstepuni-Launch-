#!/usr/bin/env node
/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 *
 * Reconcile factual Biology reference headings with the entitled SEC corpus.
 * The official outgoing and redeveloped curricula remain canonical.
 */

import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const HERE = path.dirname(fileURLToPath(import.meta.url));
const ROOT = path.resolve(HERE, '../..');
const SUBJECT_ID = 'biology';
const TAGS_PATH = path.join(HERE, 'topic-tags/tags/biology.json');
const REFERENCE_PATH = path.join(ROOT, 'data/examTopics/biology.json');
const CURRICULUM_CROSSWALK_PATH = path.join(
  ROOT, 'data/examTopics/biology-curriculum-crosswalk.json',
);
const REVIEWED_2026_PATH = path.join(
  ROOT, 'data/examTopics/biology-2026-exam-topic-map.json',
);
const OUTPUT_PATH = path.join(
  ROOT, 'data/examTopics/biology-local-crosswalk.json',
);
const RUNTIME_PATH = path.join(ROOT, 'data/examTopics/biology-runtime.json');
const BASELINE_PATH = path.join(
  ROOT, 'test/fixtures/biologyTopicQuestionBaseline.json',
);
const HOSTED_ROOT = path.join(ROOT, 'public/paper-anchors');

const reference = JSON.parse(fs.readFileSync(REFERENCE_PATH, 'utf8'));
const curriculumCrosswalk = JSON.parse(
  fs.readFileSync(CURRICULUM_CROSSWALK_PATH, 'utf8'),
);
const reviewed2026 = JSON.parse(fs.readFileSync(REVIEWED_2026_PATH, 'utf8'));
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
    'Biology curriculum crosswalk must cover every reference topic exactly once',
  );
}
for (const topic of allTopics) {
  const nodes = curriculumCrosswalk[topic.id];
  if (!Array.isArray(nodes) || !nodes.length || new Set(nodes).size !== nodes.length) {
    throw new Error(`${topic.id}: curriculum crosswalk must contain unique nodes`);
  }
  const wantedPrefix = topic.course === 'new' ? 'bio-' : 'biology-';
  for (const node of nodes) {
    if (!node.startsWith(wantedPrefix)) {
      throw new Error(`${topic.id}: invalid ${topic.course}-course node ${node}`);
    }
  }
}
for (const [key, topicIds] of Object.entries(reviewed2026.questions)) {
  if (!/^(higher|ordinary)\|(?:[1-9]|1[0-7])$/.test(key)) {
    throw new Error(`Invalid reviewed 2026 identity: ${key}`);
  }
  for (const id of topicIds) {
    if (!topicIndex.has(id)) throw new Error(`Unknown reviewed 2026 topic: ${id}`);
  }
}
if (Object.keys(reviewed2026.questions).length !== 34) {
  throw new Error('The reviewed 2026 Biology map must contain 34 questions');
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
    `Duplicate Biology variants: ${[...new Set(duplicatePaperIds)].join(', ')}`,
  );
}
if (localPapers.length !== 100) {
  throw new Error(`Expected 100 Biology variants, found ${localPapers.length}`);
}
const physicalCards = localPapers.reduce((sum, paper) => sum + paper.q.length, 0);
if (physicalCards !== 1068) {
  throw new Error(`Expected 1,068 Biology physical cards, found ${physicalCards}`);
}

const component = fileid => fileid.match(/P(000|038|040)/i)?.[1] ?? null;
const expectedNumbers = paper => {
  const part = component(paper.fileid);
  if (part === '000') {
    return Array.from({ length: 15 }, (_, index) => String(index + 1));
  }
  if (part === '038') {
    const count = paper.year <= 2020 ? 9 : 10;
    return Array.from({ length: count }, (_, index) => String(index + 1));
  }
  if (part === '040') {
    const first = paper.year <= 2020 ? 10 : 11;
    const last = paper.year <= 2020 ? 15 : 17;
    return Array.from(
      { length: last - first + 1 },
      (_, index) => String(first + index),
    );
  }
  throw new Error(`Unexpected Biology component: ${paper.fileid}`);
};

for (const paper of localPapers) {
  if (
    !['higher', 'ordinary'].includes(paper.level)
    || !['ev', 'iv'].includes(paper.lang)
    || paper.paperKey !== 'single'
  ) {
    throw new Error(`Unexpected Biology paper identity: ${paperIdentity(paper)}`);
  }
  const expected = expectedNumbers(paper);
  if (JSON.stringify(paper.q.map(question => question.n)) !== JSON.stringify(expected)) {
    throw new Error(
      `${paperIdentity(paper)}: expected ${expected.join(',')}, found `
      + paper.q.map(question => question.n).join(','),
    );
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
      !== JSON.stringify(expected)
  ) {
    throw new Error(`${hostedPath}: hosted identities do not match tags`);
  }
}

let preservedBaselineTasks = 0;
let correctedBaselineIds = 0;
for (const baselinePaper of preservationBaseline) {
  const live = localPapers.find(
    paper => paperIdentity(paper) === paperIdentity(baselinePaper),
  );
  if (!live) {
    throw new Error(`Preservation failure: missing ${paperIdentity(baselinePaper)}`);
  }
  const shifts = (
    baselinePaper.year === 2019 || baselinePaper.year === 2020
  ) && component(baselinePaper.fileid) === '040';
  for (const baselineNumber of baselinePaper.questions) {
    const correctedNumber = shifts
      ? String(Number(baselineNumber) - 1)
      : baselineNumber;
    if (!live.q.some(question => question.n === correctedNumber)) {
      throw new Error(
        `Preservation failure: missing ${paperIdentity(baselinePaper)} `
        + `Q${baselineNumber} -> Q${correctedNumber}`,
      );
    }
    preservedBaselineTasks += 1;
    correctedBaselineIds += Number(correctedNumber !== baselineNumber);
  }
}

const parseHeading = heading => {
  // Preserve source typography exactly. Some factual labels contain repeated
  // spaces (for example `Question  17`), and the compact runtime must be able
  // to reconstruct every heading byte-for-byte rather than normalising it.
  const normalized = heading.trim();
  const match = normalized.match(/^(\d{4}) - (.*?Question\s*)(\d+)(.*)$/);
  if (!match) throw new Error(`Unparseable Biology heading: ${heading}`);
  const [, yearText, prefix, number, tail] = match;
  const sitting = /Deferred Exam Paper/i.test(prefix)
    ? 'deferred'
    : /Sample Paper/i.test(prefix)
      ? 'sample'
      : 'main';
  const rangeEnd = Number(tail.match(/^-(\d+)(?:\b|\s|$)/)?.[1]);
  const first = Number(number);
  const questionNumbers = Number.isInteger(rangeEnd) && rangeEnd >= first
    ? Array.from(
      { length: rangeEnd - first + 1 },
      (_, index) => String(first + index),
    )
    : [String(first)];
  return {
    year: Number(yearText),
    sitting,
    prefix,
    questionNumber: String(first),
    tail,
    questionNumbers,
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
    throw new Error(`Ambiguous ${level} Biology ${year} Q${number}`);
  }
  return candidates[0] ?? null;
};

const associations = [];
const exactTopicsByCard = new Map();
for (const topic of allTopics) {
  for (const heading of topic.officialQuestionHeadings) {
    const parsed = parseHeading(heading);
    const targets = parsed.sitting === 'main'
      ? parsed.questionNumbers
        .map(number => ({
          number,
          paper: englishPaper(topic.level, parsed.year, number),
        }))
        .filter(target => target.paper)
      : [];
    const fullyMatched = (
      parsed.sitting === 'main'
      && targets.length === parsed.questionNumbers.length
    );

    if (fullyMatched) {
      for (const target of targets) {
        const key = [topic.level, parsed.year, target.number].join('|');
        const indexes = exactTopicsByCard.get(key) ?? [];
        const index = topicIndex.get(topic.id);
        if (index === undefined) throw new Error(`Unknown Biology topic ${topic.id}`);
        if (!indexes.includes(index)) indexes.push(index);
        exactTopicsByCard.set(key, indexes);
      }
      associations.push({
        topicId: topic.id,
        variant: topic.variant,
        level: topic.level,
        course: topic.course,
        heading,
        ...parsed,
        paperKey: 'single',
        resolution: 'matched',
        targets: targets.map(target => ({
          level: topic.level,
          lang: 'ev',
          year: parsed.year,
          paperKey: 'single',
          fileid: target.paper.fileid,
          questionNumber: target.number,
        })),
      });
      continue;
    }

    const reason = parsed.sitting === 'sample'
      ? 'The entitled corpus does not contain this official redeveloped-course sample paper. Its factual heading is retained; no StudyClix-hosted question image or PDF is copied.'
      : parsed.sitting === 'deferred'
        ? 'The entitled corpus does not contain this deferred Biology sitting. Its factual heading is retained; no StudyClix-hosted question image or PDF is copied.'
        : 'No matching entitled local SEC Biology card is present. Its factual heading is retained pending an independently verified official source.';
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

const oldTopicFallbackForNode = (level, nodeId) => {
  const candidates = allTopics
    .map((topic, index) => ({ topic, index }))
    .filter(({ topic }) => (
      topic.level === level
      && topic.course === 'old'
      && curriculumCrosswalk[topic.id].includes(nodeId)
    ))
    .sort((left, right) => (
      curriculumCrosswalk[left.topic.id].length
      - curriculumCrosswalk[right.topic.id].length
      || left.index - right.index
    ));
  if (!candidates.length) {
    throw new Error(`No ${level} old-course Biology topic covers ${nodeId}`);
  }
  return candidates[0].index;
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
      indexes = [...new Set(
        [question.primary, question.secondary]
          .filter(Boolean)
          .map(nodeId => oldTopicFallbackForNode(paper.level, nodeId)),
      )];
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
        reason: paper.year === 2026
          ? 'Official SEC 2026 task retained from direct paper review; it post-dates the factual reference snapshot.'
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
  allTopics.length !== 122
  || reported !== 4891
  || official !== 2419
  || mocks !== 2333
  || providerSamples !== 139
  || reported !== official + mocks + providerSamples
) {
  throw new Error(
    `Biology audit totals changed: ${allTopics.length}/${reported}/`
    + `${official}/${mocks}/${providerSamples}`,
  );
}
if (questionMappings.length !== 534) {
  throw new Error(
    `Expected 534 logical mappings, found ${questionMappings.length}`,
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
  item.questionNumber,
  tailIndex.get(item.tail),
]);
if (compactPartReferences.some(row => row.some(value => value === undefined))) {
  throw new Error('A compact Biology part reference has an unknown index');
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
          if (index === undefined) {
            throw new Error(`Unknown Biology group topic ${id}`);
          }
          return index;
        }),
      ]);
    }
  } else {
    groups.push([
      levelCode,
      courseCode,
      `biology-${variant}`,
      variantData.label,
      variantData.topics.map(topic => {
        const index = topicIndex.get(topic.id);
        if (index === undefined) {
          throw new Error(`Unknown Biology group topic ${topic.id}`);
        }
        return index;
      }),
    ]);
  }
}

// Topic ids and public paths repeat the same subject / level / course / group
// slugs. Keep only the terminal slug in the shipped runtime; registry.ts
// reconstructs the stable identities from the group membership. Validate that
// reconstruction here so compacting can never alter an audited public path.
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
  // [h/o, new/old, stable id, display label, topic indexes]
  groups,
  // [terminal slug, label, mocks, provider samples, curriculum nodes,
  //  reported total]. Stable ids, paths, level and course are losslessly
  //  reconstructed from the group membership.
  topics: compactTopics,
  headingPrefixes: prefixes,
  headingTails: tails,
  // [topic index, year-2000, prefix index, printed question, tail index]
  partReferences: compactPartReferences,
  // [h/o, year-2000, printed question, topic indexes], shared by EV/IV.
  questionMappings,
};

const matchedAssociations = associations.filter(
  item => item.resolution === 'matched',
);
const sourceBlockedAssociations = associations.filter(
  item => item.resolution === 'source-blocked',
);
const matchedLogicalCards = new Set(
  matchedAssociations.flatMap(item => item.questionNumbers.map(number => [
    item.level, item.year, number,
  ].join('|'))),
).size;
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
    corrected2019To2020SectionCCardIds: correctedBaselineIds,
  },
  associations,
  retainedLocalCards,
};

fs.writeFileSync(OUTPUT_PATH, `${JSON.stringify(localCrosswalk, null, 2)}\n`);
fs.writeFileSync(RUNTIME_PATH, JSON.stringify(runtime));

console.log(JSON.stringify(localCrosswalk.summary, null, 2));
console.log(`runtimeBytes ${fs.statSync(RUNTIME_PATH).size}`);
