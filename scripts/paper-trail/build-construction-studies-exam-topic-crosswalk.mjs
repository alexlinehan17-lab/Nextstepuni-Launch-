#!/usr/bin/env node
/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 *
 * Reconcile the factual Construction Studies reference hierarchy with the
 * complete entitled SEC written-paper corpus. Both the outgoing Construction
 * Studies course and the incoming Construction Technology hierarchy remain
 * visible, while every pre-existing local question is preserved additively.
 */

import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const HERE = path.dirname(fileURLToPath(import.meta.url));
const ROOT = path.resolve(HERE, '../..');
const SUBJECT_ID = 'construction-studies';
const TAGS_PATH = path.join(HERE, 'topic-tags/tags/construction-studies.json');
const REFERENCE_PATH = path.join(ROOT, 'data/examTopics/construction-studies.json');
const REVIEWED_PATH = path.join(
  ROOT,
  'data/examTopics/construction-studies-reviewed-question-topics.json',
);
const CURRICULUM_CROSSWALK_PATH = path.join(
  ROOT,
  'data/examTopics/construction-studies-curriculum-crosswalk.json',
);
const OUTPUT_PATH = path.join(
  ROOT,
  'data/examTopics/construction-studies-local-crosswalk.json',
);
const RUNTIME_PATH = path.join(
  ROOT,
  'data/examTopics/construction-studies-runtime.json',
);
const BASELINE_PATH = path.join(
  ROOT,
  'test/fixtures/constructionStudiesTopicQuestionBaseline.json',
);
const HOSTED_ROOT = path.join(ROOT, 'public/paper-anchors');
const VARIANTS = ['higher', 'ordinary', 'higher-new-course', 'ordinary-new-course'];
const LEVELS = ['higher', 'ordinary'];

const readJson = file => JSON.parse(fs.readFileSync(file, 'utf8'));
const reference = readJson(REFERENCE_PATH);
const reviewed = readJson(REVIEWED_PATH);
const sourcePapers = readJson(TAGS_PATH);
const preservationBaseline = readJson(BASELINE_PATH);

const OLD_CURRICULUM_BY_LABEL = {
  'Condensation & Air Tightness': ['cons-6-5', 'cons-6-6'],
  'Conservation & Restoration': ['cons-1-1', 'cons-1-2'],
  Doors: ['cons-3-7', 'cons-4-5'],
  Drainage: ['cons-5-4', 'cons-5-5', 'cons-5-6'],
  'Fireplaces & Fire Prevention': ['cons-1-9', 'cons-5-7'],
  Floors: ['cons-4-2', 'cons-4-3'],
  Foundations: ['cons-2-1', 'cons-2-2', 'cons-2-3', 'cons-2-4', 'cons-2-5'],
  'Heat & U-Value Calculations': ['cons-6-1', 'cons-6-3'],
  'Heat Loss & Insulation': ['cons-6-2', 'cons-6-3'],
  'Hot Water & Space Heating': ['cons-5-2', 'cons-5-3'],
  'Passive Design': ['cons-6-2', 'cons-6-4', 'cons-6-5'],
  'Planning, Sustainability & Environment': ['cons-1-2', 'cons-1-3', 'cons-6-4'],
  'Project & Practical': [
    'cons-9-1', 'cons-9-2', 'cons-9-3', 'cons-9-4',
    'cons-10-1', 'cons-10-2', 'cons-10-3', 'cons-10-4',
    'cons-10-5', 'cons-10-6', 'cons-10-7',
  ],
  'Question 1: Drawing Questions': ['cons-1-5'],
  Roofs: ['cons-3-8', 'cons-3-9', 'cons-3-10'],
  'Services: Water, Gas, Electricity': ['cons-5-1', 'cons-5-2', 'cons-5-3', 'cons-5-8'],
  'Site Safety': ['cons-1-8', 'cons-1-9', 'cons-9-4'],
  Sound: ['cons-8-1', 'cons-8-2', 'cons-8-3', 'cons-8-4'],
  Stairs: ['cons-4-4', 'cons-10-1'],
  'Sustainability & the Environment': ['cons-1-2', 'cons-6-2', 'cons-6-4'],
  Walls: ['cons-3-2', 'cons-3-3', 'cons-3-4', 'cons-4-1'],
  'Windows & Light': [
    'cons-3-5', 'cons-3-6',
    'cons-7-1', 'cons-7-2', 'cons-7-3', 'cons-7-4',
  ],
  'Wood, Rot & Ventilation': ['cons-6-5', 'cons-10-3', 'cons-10-7'],

  'Air Tightness & Condensation': ['cons-6-5', 'cons-6-6'],
  Concrete: ['cons-2-6', 'cons-2-7'],
  'Fire Places & Fire Prevention': ['cons-1-9', 'cons-5-7'],
  'Foundations, Floors & Walls': [
    'cons-2-2', 'cons-2-4', 'cons-3-2', 'cons-3-3', 'cons-3-4',
    'cons-4-2', 'cons-4-3',
  ],
  'Heat & U Value Calculations': ['cons-6-1', 'cons-6-3'],
  'Question One Drawing Questions': ['cons-1-5'],
  'Services, Water, Gas, Electrical': ['cons-5-1', 'cons-5-2', 'cons-5-3', 'cons-5-8'],
  'Windows & Doors': ['cons-3-5', 'cons-3-6', 'cons-3-7', 'cons-4-5'],
};

const NEW_CURRICULUM_BY_LABEL = {
  'Design principles of a domestic dwelling for the built environment': 'construction-technology-1-design-principles',
  'Environmental and architectural heritage of dwellings': 'construction-technology-1-architectural-heritage',
  'Personal safety and Safety on a Construction Site': 'construction-technology-1-health-safety',
  'Universal Design applied to a domestic dwelling': 'construction-technology-1-universal-design',
  'Urban and rural design of a dwelling': 'construction-technology-1-urban-rural-design',
  'Communication skills': 'construction-technology-2-communication-skills',
  'Craft skills, processes and techniques': 'construction-technology-2-craft-skills',
  'Design skills': 'construction-technology-2-design-skills',
  'Graphical communication': 'construction-technology-2-graphical-communication',
  'Materials properties and use': 'construction-technology-2-material-properties',
  'Personal reflection': 'construction-technology-2-personal-reflection',
  'Project management': 'construction-technology-2-project-management',
  'Sustainable use of materials': 'construction-technology-2-sustainable-materials',
  'Building regulations and standards': 'construction-technology-3-regulations-standards',
  'Construction principles for a domestic dwelling': 'construction-technology-3-construction-principles',
  'Design for health, wellness and comfort': 'construction-technology-3-health-wellness-comfort',
  'Ecological building design': 'construction-technology-3-ecological-design',
  'Functions of the building fabric in a domestic dwelling': 'construction-technology-3-fabric-functions',
  'Passive design': 'construction-technology-3-passive-design',
  'Resilient design': 'construction-technology-3-resilient-design',
  Substructure: 'construction-technology-3-substructure-superstructure',
  Superstructure: 'construction-technology-3-substructure-superstructure',
  'Airtightness in a domestic dwelling': 'construction-technology-4-airtightness',
  'Drainage systems for a domestic dwelling': 'construction-technology-4-drainage',
  'Electricity in a domestic dwelling': 'construction-technology-4-electricity',
  'Energy sources and space heating systems in domestic houses': 'construction-technology-4-energy-heating',
  'Heat energy and scientific calculations in dwellings': 'construction-technology-4-heat-energy',
  'Indoor dwelling environment': 'construction-technology-4-indoor-environment',
  'Operational carbon of a domestic dwelling': 'construction-technology-4-operational-carbon',
  'Smart home technologies': 'construction-technology-4-smart-home',
  'Ventilation in a domestic dwelling': 'construction-technology-4-ventilation',
  'Water supply in a domestic dwelling': 'construction-technology-4-water-supply',
};

const variantForTopic = new Map();
const allTopics = VARIANTS.flatMap(variant => (
  reference.variants[variant].topics.map(topic => {
    variantForTopic.set(topic.id, variant);
    return {
      ...topic,
      variant,
      level: variant.startsWith('higher') ? 'higher' : 'ordinary',
      course: variant.endsWith('new-course') ? 'new' : 'old',
    };
  })
));
const topicIndex = new Map(allTopics.map((topic, index) => [topic.id, index]));
if (reference.subjectId !== SUBJECT_ID || allTopics.length !== 103) {
  throw new Error(`Expected the 103-topic Construction Studies reference, found ${allTopics.length}`);
}

const curriculumCrosswalk = Object.fromEntries(allTopics.map((topic) => {
  const nodes = topic.course === 'new'
    ? [NEW_CURRICULUM_BY_LABEL[topic.label]].filter(Boolean)
    : OLD_CURRICULUM_BY_LABEL[topic.label];
  if (!nodes?.length || new Set(nodes).size !== nodes.length) {
    throw new Error(`${topic.id}: missing or duplicate curriculum crosswalk nodes`);
  }
  const valid = topic.course === 'new'
    ? nodes.every(node => /^construction-technology-[1-4]-/.test(node))
    : nodes.every(node => /^cons-(?:10|[1-9])-\d+$/.test(node));
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
const expectedNumbers = level => Array.from(
  { length: level === 'higher' ? 10 : 9 },
  (_, index) => String(index + 1),
);

const ADDITION_TAGS = {
  higher: {
    '1': ['construction-studies-0-17', 'construction-studies-0-21'],
    '2': ['construction-studies-0-8'],
    '3': ['construction-studies-0-8'],
    '4': ['construction-studies-0-20'],
    '5': ['construction-studies-0-8'],
    '6': ['construction-studies-0-8'],
    '7': ['construction-studies-0-14'],
    '8': ['construction-studies-0-4'],
    '9': ['construction-studies-0-17'],
    '10': ['construction-studies-0-8', 'construction-studies-0-19'],
  },
  ordinary: {
    '1': ['construction-studies-0-9', 'construction-studies-0-21'],
    '2': ['construction-studies-0-8'],
    '3': ['construction-studies-0-4'],
    '4': ['construction-studies-0-8'],
    '5': ['construction-studies-0-13'],
    '6': ['construction-studies-0-16'],
    '7': ['construction-studies-0-8'],
    '8': ['construction-studies-0-19'],
    '9': ['construction-studies-0-19'],
  },
};
const additionQuestion = (level, n) => {
  const [primary, secondary] = ADDITION_TAGS[level][n] ?? [];
  if (!primary) throw new Error(`${level} Q${n}: no additive source tag`);
  return { n, primary, ...(secondary ? { secondary } : {}) };
};

const additions = [];
for (const [year, level, langs] of [
  [2026, 'higher', ['ev', 'iv']],
  [2026, 'ordinary', ['ev', 'iv']],
  [2014, 'higher', ['ev']],
]) {
  for (const lang of langs) {
    const fileid = `LC029${level === 'higher' ? 'A' : 'G'}LP000${lang.toUpperCase()}.pdf`;
    const identity = [level, lang, year, 'single', fileid].join('|');
    const existing = sourcePapers.find(paper => paperIdentity(paper) === identity);
    if (existing) {
      additions.push(existing);
      continue;
    }
    const answerPath = path.join(HERE, 'answers', String(year), `${fileid}.json`);
    if (!fs.existsSync(answerPath)) throw new Error(`Missing answer map: ${answerPath}`);
    const answerMap = readJson(answerPath);
    const numbers = expectedNumbers(level);
    if (JSON.stringify(answerMap.q?.map(question => question.n)) !== JSON.stringify(numbers)) {
      throw new Error(`${identity}: answer map does not contain the complete written paper`);
    }
    additions.push({
      subjectId: SUBJECT_ID,
      level,
      lang,
      year,
      fileid,
      paperKey: 'single',
      q: numbers.map(n => additionQuestion(level, n)),
    });
  }
}
const additionIds = new Set(additions.map(paperIdentity));
const localPapers = [
  ...additions,
  ...sourcePapers.filter(paper => !additionIds.has(paperIdentity(paper))),
];
const paperIds = localPapers.map(paperIdentity);
if (localPapers.length !== 68 || paperIds.length !== new Set(paperIds).size) {
  throw new Error('Construction Studies must contain 68 unique written-paper variants');
}
for (const paper of localPapers) {
  const numbers = expectedNumbers(paper.level);
  if (
    paper.subjectId !== SUBJECT_ID
    || !LEVELS.includes(paper.level)
    || !['ev', 'iv'].includes(paper.lang)
    || paper.paperKey !== 'single'
    || JSON.stringify(paper.q.map(question => question.n)) !== JSON.stringify(numbers)
  ) {
    throw new Error(`${paperIdentity(paper)}: incomplete or invalid written paper`);
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
if (preservationBaseline.length !== 63 || preservedBaselineCards !== 598) {
  throw new Error('The frozen Construction Studies preservation baseline changed unexpectedly');
}

const clean = value => value.replace(/\s+/g, ' ').trim();
const parseHeading = (heading) => {
  const normalized = clean(heading);
  const match = normalized.match(/^(\d{4})(.*?Question\s+)(\d+)(.*)$/i);
  if (!match) throw new Error(`Unparseable Construction Studies heading: ${heading}`);
  const [, yearText, prefix, questionToken, tail] = match;
  return {
    year: Number(yearText),
    prefix,
    questionToken,
    tail,
    n: questionToken,
    sitting: /Deferred Exam Paper/i.test(normalized)
      ? 'deferred'
      : /Sample Paper/i.test(normalized)
        ? 'sample'
        : 'main',
  };
};
const englishPaper = (level, year, n) => {
  const candidates = localPapers.filter(paper => (
    paper.level === level
    && paper.lang === 'ev'
    && paper.year === year
    && paper.q.some(question => question.n === n)
  ));
  if (candidates.length > 1) {
    throw new Error(`Ambiguous Construction Studies card ${logicalIdentity(level, year, n)}`);
  }
  return candidates[0] ?? null;
};
const blockedReason = (parsed) => {
  if (parsed.year < 2010) {
    return 'The entitled local SEC Construction Studies corpus begins at 2010. The factual heading is retained pending independent verification of an official paper; no StudyClix-hosted question image or PDF is copied.';
  }
  if (parsed.sitting === 'sample') {
    return 'The factual heading belongs to an official sample paper that is not a selectable document in the entitled local corpus. It remains source-blocked; no StudyClix-hosted question image or PDF is copied.';
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
          ?? 'No matching entitled local SEC paper is present. The factual heading is retained pending independent verification; no StudyClix-hosted question image or PDF is copied.',
      });
      continue;
    }
    const key = logicalIdentity(topic.level, parsed.year, parsed.n);
    const indexes = exactTopicsByCard.get(key) ?? [];
    const index = topicIndex.get(topic.id);
    if (index === undefined) throw new Error(`Unknown Construction Studies topic ${topic.id}`);
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

const oldTopicForLabel = (level, label) => {
  const topic = reference.variants[level].topics.find(candidate => candidate.label === label);
  if (!topic) throw new Error(`${level}: unknown reviewed outgoing topic ${label}`);
  return topic.id;
};
const logicalEnglishPapers = localPapers.filter(paper => paper.lang === 'ev');
const questionMappings = [];
const retainedLocalCards = [];
const usedReviewed = new Set();
for (const paper of logicalEnglishPapers) {
  for (const question of paper.q) {
    const key = logicalIdentity(paper.level, paper.year, question.n);
    let indexes = exactTopicsByCard.get(key);
    if (!indexes) {
      const review = reviewed.questions[key];
      if (!review) throw new Error(`${key}: reference omission lacks direct SEC review`);
      const ids = review.topics.map(label => oldTopicForLabel(paper.level, label));
      indexes = [...new Set(ids)].map(id => topicIndex.get(id));
      if (!indexes.length || indexes.some(index => index === undefined)) {
        throw new Error(`${key}: invalid reviewed Construction Studies mapping`);
      }
      usedReviewed.add(key);
      retainedLocalCards.push({
        level: paper.level,
        year: paper.year,
        paperKey: paper.paperKey,
        fileid: paper.fileid,
        questionNumber: question.n,
        canonicalNodeIds: [question.primary, question.secondary].filter(Boolean),
        topicIds: indexes.map(index => allTopics[index].id),
        resolution: 'retained-local-reviewed',
        reason: 'Entitled SEC task omitted from the factual reference snapshot and retained from direct review of the official paper.',
        evidence: review.evidence,
      });
    }
    questionMappings.push([
      paper.level === 'higher' ? 'h' : 'o',
      paper.year - 2000,
      question.n,
      indexes,
    ]);
  }
}
if (JSON.stringify([...usedReviewed].sort()) !== JSON.stringify(Object.keys(reviewed.questions).sort())) {
  throw new Error('Reviewed Construction Studies map must equal the exact local-reference omissions');
}

const reported = allTopics.reduce((sum, topic) => sum + topic.reportedQuestionCount, 0);
const official = allTopics.reduce((sum, topic) => sum + topic.officialQuestionHeadings.length, 0);
const mocks = allTopics.reduce((sum, topic) => sum + topic.mockQuestionCount, 0);
const providerSamples = allTopics.reduce((sum, topic) => sum + topic.providerSampleQuestionCount, 0);
const matchedAssociations = associations.filter(item => item.resolution === 'matched');
const sourceBlockedAssociations = associations.filter(item => item.resolution === 'source-blocked');
if (
  reported !== 2336
  || official !== 1396
  || mocks !== 940
  || providerSamples !== 0
  || reported !== official + mocks + providerSamples
  || matchedAssociations.length !== 1031
  || sourceBlockedAssociations.length !== 365
  || exactTopicsByCard.size !== 302
  || retainedLocalCards.length !== 21
  || questionMappings.length !== 323
) {
  throw new Error('Construction Studies reconciliation coverage changed unexpectedly');
}

let verifiedSchemeMaps = 0;
let verifiedPaperOnlyMaps = 0;
for (const paper of localPapers) {
  const classicPath = path.join(HERE, 'answers', String(paper.year), `${paper.fileid}.json`);
  const hostedPath = path.join(HOSTED_ROOT, String(paper.year), `${paper.fileid}.json`);
  const mapPath = fs.existsSync(classicPath) ? classicPath : fs.existsSync(hostedPath) ? hostedPath : null;
  if (!mapPath) throw new Error(`${paperIdentity(paper)} has no question anchor map`);
  const map = readJson(mapPath);
  if (JSON.stringify(map.q?.map(question => question.n)) !== JSON.stringify(expectedNumbers(paper.level))) {
    throw new Error(`${paperIdentity(paper)} has a mismatched question map at ${mapPath}`);
  }
  if (map.paperOnly === 1) verifiedPaperOnlyMaps += 1;
  else verifiedSchemeMaps += 1;
}
if (verifiedSchemeMaps !== 64 || verifiedPaperOnlyMaps !== 4) {
  throw new Error('Construction Studies paper/scheme map boundary changed unexpectedly');
}

const groups = [];
for (const variant of VARIANTS) {
  const variantData = reference.variants[variant];
  const levelCode = variant.startsWith('higher') ? 'h' : 'o';
  const courseCode = variant.endsWith('new-course') ? 'n' : 'o';
  if (variantData.groups.length) {
    for (const group of variantData.groups) {
      groups.push([
        levelCode,
        courseCode,
        group.id,
        `${variantData.label} · ${group.label}`,
        group.topicIds.map(id => topicIndex.get(id)),
      ]);
    }
  } else {
    groups.push([
      levelCode,
      courseCode,
      `${SUBJECT_ID}-${variant}`,
      variantData.label,
      variantData.topics.map(topic => topicIndex.get(topic.id)),
    ]);
  }
}
if (groups.length !== 10 || groups.some(group => group[4].some(index => index === undefined))) {
  throw new Error('Construction Studies runtime hierarchy must contain ten complete display groups');
}

const compactTopics = allTopics.map((topic) => {
  const prefix = `${SUBJECT_ID}-${topic.variant}-`;
  if (!topic.id.startsWith(prefix)) throw new Error(`${topic.id}: invalid compact prefix`);
  return [
    topic.id.slice(prefix.length),
    topic.label,
    topic.mockQuestionCount,
    topic.providerSampleQuestionCount,
    curriculumCrosswalk[topic.id],
    topic.reportedQuestionCount,
  ];
});
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
  throw new Error('Construction Studies compact part reference contains an unknown value');
}

const matchedQuestionTopicLinks = new Set(matchedAssociations.map(item => [
  item.topicId,
  item.level,
  item.year,
  item.n,
].join('|'))).size;
const physicalMappings = localPapers.reduce((sum, paper) => sum + paper.q.length, 0);
const sourceBlockedBreakdown = {
  beforeLocalCorpus: sourceBlockedAssociations.filter(item => item.year < 2010).length,
  deferredSittings: sourceBlockedAssociations.filter(item => item.sitting === 'deferred').length,
  officialSamplePapers: sourceBlockedAssociations.filter(item => item.sitting === 'sample').length,
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
  retainedLocalLogicalCards: retainedLocalCards.length,
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
    .filter(topic => topic.officialQuestionHeadings.length === 0)
    .map(topic => topic.id),
};
if (
  physicalMappings !== 646
  || summary.newlyAddedPaperVariants !== 5
  || summary.newlyAddedPhysicalMappings !== 48
  || sourceBlockedBreakdown.beforeLocalCorpus !== 225
  || sourceBlockedBreakdown.deferredSittings !== 49
  || sourceBlockedBreakdown.officialSamplePapers !== 91
) {
  throw new Error('Construction Studies corpus or source-boundary totals changed unexpectedly');
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
    preservation: 'Every frozen local card remains present; valid local questions omitted by the reference are mapped from direct review of entitled SEC papers.',
  },
  summary,
  curriculumCrosswalk,
  associations,
  retainedLocalCards,
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
