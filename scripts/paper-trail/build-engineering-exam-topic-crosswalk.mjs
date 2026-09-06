#!/usr/bin/env node
/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 *
 * Reconcile the factual Engineering practice hierarchy with every entitled
 * SEC written paper. Existing cards are preserved; the four 2026 language /
 * level editions already present in the local SEC corpus are made selectable.
 */

import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const HERE = path.dirname(fileURLToPath(import.meta.url));
const ROOT = path.resolve(HERE, '../..');
const SUBJECT_ID = 'engineering';
const TAGS_PATH = path.join(HERE, 'topic-tags/tags/engineering.json');
const REFERENCE_PATH = path.join(ROOT, 'data/examTopics/engineering.json');
const CURRICULUM_CROSSWALK_PATH = path.join(
  ROOT,
  'data/examTopics/engineering-curriculum-crosswalk.json',
);
const OUTPUT_PATH = path.join(ROOT, 'data/examTopics/engineering-local-crosswalk.json');
const RUNTIME_PATH = path.join(ROOT, 'data/examTopics/engineering-runtime.json');
const BASELINE_PATH = path.join(ROOT, 'test/fixtures/engineeringTopicQuestionBaseline.json');
const ANSWER_ROOT = path.join(HERE, 'answers');
const HOSTED_ROOT = path.join(ROOT, 'public/paper-anchors');
const LEVELS = ['higher', 'ordinary'];
const VARIANTS = ['higher', 'ordinary', 'higher-new-course', 'ordinary-new-course'];

const readJson = file => JSON.parse(fs.readFileSync(file, 'utf8'));
const reference = readJson(REFERENCE_PATH);
const sourcePapers = readJson(TAGS_PATH);
const preservationBaseline = readJson(BASELINE_PATH);

const OLD_CURRICULUM_BY_LABEL = {
  Abbreviations: ['eng-3-14'],
  'Corrosion of Metals': ['eng-3-7'],
  'Energy, Electronics & Robotics': ['eng-2-16', 'eng-2-15'],
  'Equilibrium Diagrams': ['eng-1-3'],
  'Graphics and Design': ['eng-3-14'],
  'Health and Safety': ['eng-3-1'],
  'Heat Treatment': ['eng-2-6'],
  'Inventors and Engineers in Society': ['eng-3-14'],
  'Machining & Metrology': ['eng-2-11', 'eng-3-12'],
  'Materials: Properties and Uses': [
    'eng-1-2', 'eng-1-3', 'eng-1-4', 'eng-1-5', 'eng-1-9', 'eng-3-8',
  ],
  Mechanisms: ['eng-2-15'],
  Metallurgy: ['eng-1-2', 'eng-1-3', 'eng-1-4'],
  Pneumatics: ['eng-2-15', 'eng-2-16'],
  Polymers: ['eng-1-9'],
  'PRACTICAL EXAM': ['eng-2-10', 'eng-2-11', 'eng-2-13', 'eng-3-1'],
  PROJECT: ['eng-3-14', 'eng-2-13'],
  'Q2 - Special Topic': ['eng-3-14'],
  'Testing of Materials and Products': ['eng-3-8'],
  'The Structure of Materials': ['eng-1-3'],
  Welding: ['eng-2-10'],
  'CNC & Centre Lathe': ['eng-2-11', 'eng-2-13', 'eng-3-12'],
  'Design & Project Management': ['eng-3-14', 'eng-2-13'],
  'Finishing of Materials': ['eng-2-13', 'eng-3-7'],
  Furnaces: ['eng-1-2', 'eng-1-4'],
  ICT: ['eng-3-14', 'eng-2-16'],
  'Mechanical Joining & Assembly': ['eng-2-10'],
  'Non-Ferrous Metals & Alloys': ['eng-1-5', 'eng-1-3'],
  'Tools & Mechanisms': ['eng-2-11', 'eng-2-15'],
  'Welding & Soldering': ['eng-2-10'],
};

const NEW_CURRICULUM_BY_LABEL = {
  'CAD/CAM': 'engineering-2028-1-cadcam',
  'Engineering in Society': 'engineering-2028-1-engineering-in-society',
  'Manufacturing skills': 'engineering-2028-1-manufacturing-skills',
  'Materials Processing and Selection': 'engineering-2028-1-materials-processing-selection',
  'Measurement, Quality, and Automation': 'engineering-2028-1-measurement-quality-automation',
  'Project Planning and Evaluation': 'engineering-2028-1-project-planning-evaluation',
  'Advanced and Autonomous System': 'engineering-2028-2-advanced-autonomous-systems',
  'Communication, Programming, and Debugging': 'engineering-2028-2-communication-programming-debugging',
  'Control System Design': 'engineering-2028-2-control-system-design',
  'Control systems': 'engineering-2028-2-control-systems',
  'Sensors, Actuators, and Energy': 'engineering-2028-2-sensors-actuators-energy',
  'Design Process and Sustainability': 'engineering-2028-3-design-process-sustainability',
  'Engineering Specification and Prototyping': 'engineering-2028-3-specification-prototyping',
  'Functionality and Human-Centred Design': 'engineering-2028-3-human-centred-design',
  'Sketching, Visualisation and Communication': 'engineering-2028-3-sketching-visualisation-communication',
  'Electrical, Pneumatic and Hydraulic Systems': 'engineering-2028-4-electrical-pneumatic-hydraulic',
  'Energy and Power': 'engineering-2028-4-energy-power',
  Materials: 'engineering-2028-4-materials',
  'Mechanisms, Motion and Structures': 'engineering-2028-4-mechanisms-motion-structures',
};

// The Paper Trail source tags pre-date the compact canonical Mark Bank nodes.
// These are used only for the four newly exposed 2026 editions; exact practice
// navigation comes from the many-to-many mapping built below.
const SOURCE_TAGS_BY_LABEL = {
  Abbreviations: ['engineering-4-3'],
  'Corrosion of Metals': ['engineering-2-6'],
  'Energy, Electronics & Robotics': ['engineering-5-3', 'engineering-6-0'],
  'Equilibrium Diagrams': ['engineering-2-7'],
  'Graphics and Design': ['engineering-3-0', 'engineering-3-5'],
  'Health and Safety': ['engineering-0-0'],
  'Heat Treatment': ['engineering-2-5'],
  'Inventors and Engineers in Society': ['engineering-1-13'],
  'Machining & Metrology': ['engineering-1-4', 'engineering-1-0'],
  'Materials: Properties and Uses': ['engineering-2-1', 'engineering-2-2'],
  Mechanisms: ['engineering-7-0'],
  Metallurgy: ['engineering-2-2', 'engineering-2-4'],
  Pneumatics: ['engineering-8-0'],
  Polymers: ['engineering-2-1', 'engineering-12-8'],
  'Q2 - Special Topic': ['engineering-1-12'],
  'Testing of Materials and Products': ['engineering-2-0'],
  'The Structure of Materials': ['engineering-2-4'],
  Welding: ['engineering-1-8'],
  'CNC & Centre Lathe': ['engineering-4-5', 'engineering-1-4'],
  'Design & Project Management': ['engineering-3-5', 'engineering-3-6'],
  'Finishing of Materials': ['engineering-1-3'],
  Furnaces: ['engineering-2-2'],
  ICT: ['engineering-4-3'],
  'Mechanical Joining & Assembly': ['engineering-1-11', 'engineering-1-10'],
  'Non-Ferrous Metals & Alloys': ['engineering-2-2', 'engineering-2-7'],
  'Tools & Mechanisms': ['engineering-1-0', 'engineering-7-0'],
  'Welding & Soldering': ['engineering-1-8', 'engineering-1-7'],
};

const allTopics = VARIANTS.flatMap(variant => reference.variants[variant].topics.map(topic => ({
  ...topic,
  variant,
  level: variant.startsWith('higher') ? 'higher' : 'ordinary',
  course: variant.endsWith('new-course') ? 'new' : 'old',
})));
const topicIndex = new Map(allTopics.map((topic, index) => [topic.id, index]));
if (reference.subjectId !== SUBJECT_ID || allTopics.length !== 74) {
  throw new Error(`Expected the 74-topic Engineering reference, found ${allTopics.length}`);
}

const curriculumCrosswalk = Object.fromEntries(allTopics.map(topic => {
  const nodes = topic.course === 'new'
    ? [NEW_CURRICULUM_BY_LABEL[topic.label]].filter(Boolean)
    : OLD_CURRICULUM_BY_LABEL[topic.label];
  if (!nodes?.length || new Set(nodes).size !== nodes.length) {
    throw new Error(`${topic.id}: missing or duplicate curriculum crosswalk nodes`);
  }
  const valid = topic.course === 'new'
    ? nodes.every(node => /^engineering-2028-[1-4]-/.test(node))
    : nodes.every(node => /^eng-[123]-\d+$/.test(node));
  if (!valid) throw new Error(`${topic.id}: invalid canonical curriculum node`);
  return [topic.id, nodes];
}));

const paperIdentity = paper => [
  paper.level,
  paper.lang,
  paper.year,
  paper.paperKey,
  paper.fileid,
].join('|');
const logicalIdentity = (level, year, n) => [level, year, n].join('|');
const expectedNumbers = (level, year) => Array.from(
  { length: level === 'higher' ? (year <= 2020 ? 8 : 9) : 7 },
  (_, index) => String(index + 1),
);
const fileidFor = (level, lang) => (
  `LC027${level === 'higher' ? 'A' : 'G'}LP000${lang.toUpperCase()}.pdf`
);

const expectedSpecs = [];
for (let year = 2026; year >= 2010; year -= 1) {
  for (const level of LEVELS) {
    if (year === 2020 && level === 'ordinary') continue;
    for (const lang of ['ev', 'iv']) {
      expectedSpecs.push({
        subjectId: SUBJECT_ID,
        level,
        lang,
        year,
        fileid: fileidFor(level, lang),
        paperKey: 'single',
        q: expectedNumbers(level, year).map(n => ({ n, primary: 'engineering-2-1' })),
      });
    }
  }
}
if (expectedSpecs.length !== 66) {
  throw new Error(`Expected 66 Engineering written-paper variants, found ${expectedSpecs.length}`);
}
const expectedIds = new Set(expectedSpecs.map(paperIdentity));
const unexpectedSource = sourcePapers.filter(paper => !expectedIds.has(paperIdentity(paper)));
if (unexpectedSource.length) {
  throw new Error(`Unexpected Engineering source papers: ${unexpectedSource.map(paperIdentity).join(', ')}`);
}
const sourceById = new Map(sourcePapers.map(paper => [paperIdentity(paper), paper]));
const frozenPaperIds = new Set(preservationBaseline.map(paperIdentity));
const additions = expectedSpecs
  .filter(spec => !frozenPaperIds.has(paperIdentity(spec)))
  .map(spec => sourceById.get(paperIdentity(spec)) ?? spec);
const localPapers = [
  ...additions,
  ...sourcePapers.filter(paper => frozenPaperIds.has(paperIdentity(paper))),
];
const paperIds = localPapers.map(paperIdentity);
if (localPapers.length !== 66 || paperIds.length !== new Set(paperIds).size) {
  throw new Error('Engineering local corpus must contain 66 unique written-paper variants');
}
for (const paper of localPapers) {
  if (
    paper.subjectId !== SUBJECT_ID
    || !LEVELS.includes(paper.level)
    || !['ev', 'iv'].includes(paper.lang)
    || paper.paperKey !== 'single'
    || JSON.stringify(paper.q.map(question => question.n))
      !== JSON.stringify(expectedNumbers(paper.level, paper.year))
  ) {
    throw new Error(`${paperIdentity(paper)}: incomplete or invalid Engineering paper`);
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
if (preservationBaseline.length !== 62 || preservedBaselineCards !== 476) {
  throw new Error('The frozen Engineering preservation baseline changed unexpectedly');
}

const clean = value => value.replace(/\s+/g, ' ').trim();
const parseHeading = heading => {
  const normalized = clean(heading);
  const match = normalized.match(/^(\d{4})(.*?Question\s+)(\d+|A)(.*)$/i);
  if (!match) throw new Error(`Unparseable Engineering heading: ${heading}`);
  const [, yearText, prefix, questionToken, tail] = match;
  const questionNumber = questionToken.toUpperCase() === 'A' ? '1' : questionToken;
  if (questionToken.toUpperCase() === 'A' && !/^2016 - Section 1 - Question A - Part [bkd]$/i.test(normalized)) {
    throw new Error(`Unexpected Engineering Question A heading: ${heading}`);
  }
  return {
    year: Number(yearText),
    prefix,
    questionToken,
    tail,
    n: questionNumber,
    sitting: /Deferred Exam Paper/i.test(normalized)
      ? 'deferred'
      : /Sample Paper/i.test(normalized)
        ? 'sample'
        : 'main',
  };
};
const englishPaper = (level, year, n) => localPapers.find(paper => (
  paper.level === level
  && paper.lang === 'ev'
  && paper.year === year
  && paper.q.some(question => question.n === n)
)) ?? null;
const blockedReason = parsed => {
  if (parsed.year < 2010) {
    return 'The entitled local SEC Engineering corpus begins at 2010. The factual heading is retained pending independent acquisition and verification; no StudyClix-hosted question image or PDF is copied.';
  }
  if (parsed.sitting === 'sample') {
    return 'The factual heading belongs to an official new-course sample paper that is not a selectable document in the entitled local corpus. It remains source-blocked; no StudyClix-hosted question image or PDF is copied.';
  }
  if (parsed.sitting === 'deferred') {
    return 'The entitled local corpus does not contain this separate deferred sitting. The factual heading is retained; no StudyClix-hosted question image or PDF is copied.';
  }
  return null;
};

const associations = [];
const exactTopicsByCard = new Map();
for (const topic of allTopics) {
  for (const heading of topic.officialQuestionHeadings) {
    const parsed = parseHeading(heading);
    const explicitBlock = blockedReason(parsed);
    const paper = explicitBlock ? null : englishPaper(topic.level, parsed.year, parsed.n);
    if (!paper) {
      associations.push({
        topicId: topic.id,
        variant: topic.variant,
        level: topic.level,
        course: topic.course,
        heading,
        ...parsed,
        resolution: 'source-blocked',
        reason: explicitBlock
          ?? 'No matching entitled local SEC paper is present. The factual heading remains recorded pending independent verification; no StudyClix-hosted question image or PDF is copied.',
      });
      continue;
    }
    const key = logicalIdentity(topic.level, parsed.year, parsed.n);
    const indexes = exactTopicsByCard.get(key) ?? [];
    const index = topicIndex.get(topic.id);
    if (index === undefined) throw new Error(`Unknown Engineering topic ${topic.id}`);
    if (!indexes.includes(index)) indexes.push(index);
    exactTopicsByCard.set(key, indexes);
    associations.push({
      topicId: topic.id,
      variant: topic.variant,
      level: topic.level,
      course: topic.course,
      heading,
      ...parsed,
      resolution: 'matched',
      target: {
        level: topic.level,
        lang: 'ev',
        year: parsed.year,
        paperKey: 'single',
        fileid: paper.fileid,
        questionNumber: parsed.n,
      },
    });
  }
}

// Give the newly exposed 2026 physical editions honest broad source tags.
// Runtime practice tags below retain every exact many-to-many association.
for (const paper of additions) {
  for (const question of paper.q) {
    const key = logicalIdentity(paper.level, paper.year, question.n);
    const indexes = exactTopicsByCard.get(key);
    if (!indexes?.length) throw new Error(`${key}: newly added card has no audited topic`);
    const outgoingTopics = indexes
      .map(index => allTopics[index])
      .filter(topic => topic.course === 'old')
      .sort((a, b) => Number(a.label === 'Abbreviations') - Number(b.label === 'Abbreviations'));
    const sourceNodes = [...new Set(outgoingTopics.flatMap(topic => (
      SOURCE_TAGS_BY_LABEL[topic.label] ?? []
    )))];
    if (!sourceNodes.length) throw new Error(`${key}: no source tags from outgoing hierarchy`);
    question.primary = sourceNodes[0];
    if (sourceNodes[1]) question.secondary = sourceNodes[1];
  }
}

const logicalEnglishPapers = localPapers.filter(paper => paper.lang === 'ev');
const questionMappings = [];
for (const paper of logicalEnglishPapers) {
  for (const question of paper.q) {
    const key = logicalIdentity(paper.level, paper.year, question.n);
    const indexes = exactTopicsByCard.get(key);
    if (!indexes?.length) {
      throw new Error(`${key}: local Engineering card is absent from the audited hierarchy`);
    }
    questionMappings.push([
      paper.level === 'higher' ? 'h' : 'o',
      paper.year - 2000,
      question.n,
      indexes,
    ]);
  }
}

const reported = allTopics.reduce((sum, topic) => sum + topic.reportedQuestionCount, 0);
const official = allTopics.reduce((sum, topic) => sum + topic.officialQuestionHeadings.length, 0);
const mocks = allTopics.reduce((sum, topic) => sum + topic.mockQuestionCount, 0);
const providerSamples = allTopics.reduce((sum, topic) => sum + topic.providerSampleQuestionCount, 0);
const matchedAssociations = associations.filter(item => item.resolution === 'matched');
const sourceBlockedAssociations = associations.filter(item => item.resolution === 'source-blocked');
if (
  reported !== 4681
  || official !== 2921
  || mocks !== 1760
  || providerSamples !== 0
  || reported !== official + mocks + providerSamples
  || matchedAssociations.length !== 2287
  || sourceBlockedAssociations.length !== 634
  || exactTopicsByCard.size !== 254
  || questionMappings.length !== 254
) {
  throw new Error('Engineering reconciliation coverage changed unexpectedly');
}

let verifiedSchemeMaps = 0;
let verifiedPaperOnlyMaps = 0;
for (const paper of localPapers) {
  const classicPath = path.join(ANSWER_ROOT, String(paper.year), `${paper.fileid}.json`);
  const hostedPath = path.join(HOSTED_ROOT, String(paper.year), `${paper.fileid}.json`);
  const mapPath = fs.existsSync(classicPath) ? classicPath : fs.existsSync(hostedPath) ? hostedPath : null;
  if (!mapPath) throw new Error(`${paperIdentity(paper)} has no question anchor map`);
  const map = readJson(mapPath);
  if (JSON.stringify(map.q?.map(question => question.n)) !== JSON.stringify(
    expectedNumbers(paper.level, paper.year),
  )) {
    throw new Error(`${paperIdentity(paper)} has a mismatched question map at ${mapPath}`);
  }
  if (map.paperOnly === 1) verifiedPaperOnlyMaps += 1;
  else verifiedSchemeMaps += 1;
}
if (verifiedSchemeMaps !== 64 || verifiedPaperOnlyMaps !== 2) {
  throw new Error('Engineering paper/scheme map boundary changed unexpectedly');
}

const groups = VARIANTS.flatMap(variant => {
  const variantReference = reference.variants[variant];
  const levelCode = variant.startsWith('higher') ? 'h' : 'o';
  const courseCode = variant.endsWith('new-course') ? 'n' : 'o';
  if (!variantReference.groups.length) {
    return [[
      levelCode,
      courseCode,
      `engineering-${variant}`,
      variantReference.label,
      variantReference.topics.map(topic => topicIndex.get(topic.id)),
    ]];
  }
  return variantReference.groups.map(group => [
    levelCode,
    courseCode,
    group.id,
    `${variantReference.label} · ${group.label}`,
    group.topicIds.map(id => topicIndex.get(id)),
  ]);
});
if (groups.some(group => group[4].some(index => index === undefined))) {
  throw new Error('Engineering runtime group contains an unknown topic index');
}
// The terminal URL slug is the stable practice-topic identity. Using it
// directly avoids deriving the slug from group names whose word counts vary.
const compactTopics = allTopics.map(topic => [
  topic.sourcePath.split('/').at(-1),
  topic.label,
  topic.mockQuestionCount,
  topic.providerSampleQuestionCount,
  curriculumCrosswalk[topic.id],
  topic.reportedQuestionCount,
]);
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
  item.n,
]);
if (compactPartReferences.some(row => row.some(value => value === undefined))) {
  throw new Error('Engineering compact part reference contains an unknown value');
}

const matchedQuestionTopicLinks = new Set(matchedAssociations.map(item => (
  [item.topicId, item.level, item.year, item.n].join('|')
))).size;
const physicalMappings = localPapers.reduce((sum, paper) => sum + paper.q.length, 0);
const sourceBlockedBreakdown = {
  beforeLocalCorpus: sourceBlockedAssociations.filter(item => item.year < 2010).length,
  deferred: sourceBlockedAssociations.filter(item => item.sitting === 'deferred').length,
  sample: sourceBlockedAssociations.filter(item => item.sitting === 'sample').length,
};
const summary = {
  referenceTopics: allTopics.length,
  referenceGroups: 8,
  runtimeDisplayGroups: groups.length,
  referenceReportedAssociations: reported,
  referenceOfficialAssociations: official,
  referenceMockAssociations: mocks,
  referenceProviderSampleAssociations: providerSamples,
  matchedAssociations: matchedAssociations.length,
  sourceBlockedAssociations: sourceBlockedAssociations.length,
  sourceBlockedBreakdown,
  matchedLogicalCards: exactTopicsByCard.size,
  matchedQuestionTopicLinks,
  retainedLocalLogicalCards: 0,
  localPaperVariants: localPapers.length,
  localPhysicalMappings: physicalMappings,
  distinctStudentFacingQuestions: questionMappings.length,
  newlyAddedPaperVariants: additions.length,
  newlyAddedPhysicalMappings: additions.reduce((sum, paper) => sum + paper.q.length, 0),
  verifiedSchemeMaps,
  verifiedPaperOnlyMaps,
  preservedBaselineVariants: preservationBaseline.length,
  preservedBaselineCards,
  emptyReferenceTopics: allTopics
    .filter(topic => topic.reportedQuestionCount === 0)
    .map(topic => topic.id),
};
if (
  physicalMappings !== 508
  || matchedQuestionTopicLinks !== 1568
  || sourceBlockedBreakdown.beforeLocalCorpus !== 363
  || sourceBlockedBreakdown.deferred !== 173
  || sourceBlockedBreakdown.sample !== 98
  || summary.newlyAddedPaperVariants !== 4
  || summary.newlyAddedPhysicalMappings !== 32
  || summary.emptyReferenceTopics.length !== 4
  || groups.length !== 10
) {
  throw new Error(`Engineering local corpus totals changed unexpectedly: ${JSON.stringify(summary)}`);
}

const evidence = {
  schemaVersion: 1,
  subjectId: SUBJECT_ID,
  capturedAt: reference.capturedAt,
  reference: reference.reference,
  policy: {
    curriculumAuthority: 'NCCA/Curriculum Online',
    examAuthority: 'State Examinations Commission',
    commercialReferenceUse: 'Factual topic labels, hierarchy, headings, and counts only.',
    excludedCommercialContent: 'Question text, solutions, notes, videos, images, PDFs, and mock content.',
    preservation: 'Every frozen Engineering card remains present; the four 2026 official-language editions are added from entitled SEC PDFs.',
  },
  summary,
  curriculumCrosswalk,
  associations,
  retainedLocalCards: [],
};
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
  summary,
};

fs.writeFileSync(TAGS_PATH, `${JSON.stringify(localPapers, null, 1)}\n`);
fs.writeFileSync(CURRICULUM_CROSSWALK_PATH, `${JSON.stringify(curriculumCrosswalk, null, 2)}\n`);
fs.writeFileSync(OUTPUT_PATH, `${JSON.stringify(evidence, null, 2)}\n`);
fs.writeFileSync(RUNTIME_PATH, `${JSON.stringify(runtime)}\n`);
console.log(JSON.stringify(summary, null, 2));
console.log(`runtimeBytes ${fs.statSync(RUNTIME_PATH).size}`);
