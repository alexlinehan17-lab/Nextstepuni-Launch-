#!/usr/bin/env node
/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 *
 * Reconcile the factual Technology reference hierarchy with every entitled
 * SEC Section-A and Section-B/C booklet. Existing cards remain byte-for-byte
 * intact; missing editions and the previously hidden long-question booklet
 * are added from local official sources only.
 */

import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const HERE = path.dirname(fileURLToPath(import.meta.url));
const ROOT = path.resolve(HERE, '../..');
const SUBJECT_ID = 'technology';
const TAGS_PATH = path.join(HERE, 'topic-tags/tags/technology.json');
const REFERENCE_PATH = path.join(ROOT, 'data/examTopics/technology.json');
const CURRICULUM_CROSSWALK_PATH = path.join(
  ROOT,
  'data/examTopics/technology-curriculum-crosswalk.json',
);
const OUTPUT_PATH = path.join(ROOT, 'data/examTopics/technology-local-crosswalk.json');
const RUNTIME_PATH = path.join(ROOT, 'data/examTopics/technology-runtime.json');
const BASELINE_PATH = path.join(
  ROOT,
  'test/fixtures/technologyTopicQuestionBaseline.json',
);
const ANSWER_ROOT = path.join(HERE, 'answers');
const HOSTED_ROOT = path.join(ROOT, 'public/paper-anchors');
const LEVELS = ['higher', 'ordinary'];

const readJson = file => JSON.parse(fs.readFileSync(file, 'utf8'));
const reference = readJson(REFERENCE_PATH);
const sourcePapers = readJson(TAGS_PATH);
const preservationBaseline = readJson(BASELINE_PATH);

const range = (start, end) => Array.from(
  { length: end - start + 1 },
  (_, index) => `${start + index}`,
);
const groupNodes = (group, end) => range(0, end).map(n => `technology-${group}-${n}`);

const CANONICAL_BY_LABEL = {
  'A Process of Design': groupNodes(0, 10),
  'Communications & Graphics Media': groupNodes(3, 7),
  'Electricity & Electronics': ['technology-6-1', 'technology-6-2'],
  Energy: ['technology-6-0'],
  'Health & Safety': ['technology-2-0', 'technology-7-2', 'technology-11-6'],
  'Information and Communications Technology': ['technology-4-0', 'technology-4-1'],
  'Materials (Fabrics)': ['technology-2-0', ...groupNodes(11, 9)],
  'Materials (Metal)': ['technology-2-0', ...groupNodes(11, 9)],
  'Materials (Plastics)': ['technology-2-0', ...groupNodes(11, 9)],
  'Materials (Smart)': ['technology-2-0', ...groupNodes(11, 9)],
  'Materials (Wood)': ['technology-2-0', ...groupNodes(11, 9)],
  'Materials and Production (All Materials)': ['technology-2-0', 'technology-2-1'],
  'Materials & Production': ['technology-2-0', 'technology-2-1'],
  'Option: Applied Control Systems': groupNodes(8, 4),
  'Option 1: Applied Control Systems': groupNodes(8, 4),
  'Option: Electronics & Control': groupNodes(7, 8),
  'Option 2: Electronics & Control': groupNodes(7, 8),
  'Option: Information & Communications Technology': groupNodes(9, 3),
  'Option 3: Information & Communications Technology': groupNodes(9, 3),
  'Option: Manufacturing Systems': groupNodes(10, 4),
  'Option 4: Manufacturing Systems': groupNodes(10, 4),
  'Option: Materials Technology': groupNodes(11, 9),
  'Option 5: Materials Technology': groupNodes(11, 9),
  'Project & Quality Management': ['technology-1-0', 'technology-1-1'],
  'Sample Project Folder': [...groupNodes(0, 10), 'technology-1-0', 'technology-1-1'],
  'Structures & Mechanisms': ['technology-5-0', 'technology-5-1'],
  'Technology in Society': [
    'technology-0-1',
    'technology-0-2',
    'technology-0-3',
    'technology-0-9',
    'technology-2-1',
    'technology-6-0',
    'technology-11-7',
  ],
};

const allTopics = LEVELS.flatMap(level => (
  reference.variants[level].topics.map(topic => ({ ...topic, level, variant: level }))
));
const topicIndex = new Map(allTopics.map((topic, index) => [topic.id, index]));
if (reference.subjectId !== SUBJECT_ID || allTopics.length !== 37) {
  throw new Error(`Expected the 37-topic Technology reference, found ${allTopics.length}`);
}

const curriculumCrosswalk = Object.fromEntries(allTopics.map(topic => {
  const nodes = CANONICAL_BY_LABEL[topic.label];
  if (!nodes?.length || new Set(nodes).size !== nodes.length) {
    throw new Error(`${topic.id}: missing or duplicate canonical curriculum bridge`);
  }
  if (!nodes.every(node => /^technology-(?:[0-9]|1[01])-\d+$/.test(node))) {
    throw new Error(`${topic.id}: invalid canonical Technology node`);
  }
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
const sectionAQuestions = level => range(1, level === 'higher' ? 15 : 12);
const sectionBCQuestions = () => ['B2', 'B3', 'C1', 'C2', 'C3', 'C4', 'C5'];
const expectedQuestions = (level, fileid) => (
  fileid.includes('LP014') ? sectionAQuestions(level) : sectionBCQuestions()
);
const sectionBCComponent = year => year <= 2018 ? '015' : '039';
const fileidFor = (level, lang, year, section) => (
  `LC065${level === 'higher' ? 'A' : 'G'}LP${
    section === 'A' ? '014' : sectionBCComponent(year)
  }${lang.toUpperCase()}.pdf`
);

const expectedSpecs = [];
for (let year = 2026; year >= 2010; year -= 1) {
  for (const level of LEVELS) {
    if (year === 2020 && level === 'ordinary') continue;
    for (const lang of ['ev', 'iv']) {
      for (const section of ['A', 'BC']) {
        expectedSpecs.push({
          subjectId: SUBJECT_ID,
          level,
          lang,
          year,
          fileid: fileidFor(level, lang, year, section),
          paperKey: 'single',
          q: expectedQuestions(level, fileidFor(level, lang, year, section)).map(n => ({
            n,
            primary: 'technology-0-0',
          })),
        });
      }
    }
  }
}
if (expectedSpecs.length !== 132) {
  throw new Error(`Expected 132 Technology paper/booklet variants, found ${expectedSpecs.length}`);
}
const expectedIds = new Set(expectedSpecs.map(paperIdentity));
const unexpectedSource = sourcePapers.filter(paper => !expectedIds.has(paperIdentity(paper)));
if (unexpectedSource.length) {
  throw new Error(`Unexpected Technology source papers: ${unexpectedSource.map(paperIdentity).join(', ')}`);
}
const sourceById = new Map(sourcePapers.map(paper => [paperIdentity(paper), paper]));
const localPapers = expectedSpecs.map(spec => sourceById.get(paperIdentity(spec)) ?? spec);
const paperIds = localPapers.map(paperIdentity);
if (paperIds.length !== new Set(paperIds).size) {
  throw new Error('Technology local corpus contains duplicate paper/booklet identities');
}

for (const paper of localPapers) {
  const numbers = expectedQuestions(paper.level, paper.fileid);
  if (
    paper.subjectId !== SUBJECT_ID
    || !LEVELS.includes(paper.level)
    || !['ev', 'iv'].includes(paper.lang)
    || paper.paperKey !== 'single'
    || JSON.stringify(paper.q.map(question => question.n)) !== JSON.stringify(numbers)
  ) {
    throw new Error(`${paperIdentity(paper)}: incomplete or invalid Technology booklet`);
  }
}

let preservedBaselineCards = 0;
const baselineIds = new Set(preservationBaseline.map(paperIdentity));
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
if (preservationBaseline.length !== 56 || preservedBaselineCards !== 756) {
  throw new Error('The frozen Technology preservation baseline changed unexpectedly');
}

const clean = value => value.replace(/\s+/g, ' ').trim();
const parseHeading = heading => {
  const cleaned = clean(heading);
  const normalized = cleaned.replace(/`/g, '');
  const match = cleaned.match(/^(\d{4})(.*?Question\s+)(\d+(?:\s*,\s*\d+)?)(.*)$/i);
  if (!match) throw new Error(`Unparseable Technology heading: ${heading}`);
  const [, yearText, prefix, questionToken, tail] = match;
  let section = null;
  if (/Section\s*A\b/i.test(normalized) || /Paper\s+A\b/i.test(normalized)) section = 'A';
  else if (/Section\s*B\b/i.test(normalized)) section = 'B';
  else if (/Section\s*C\b/i.test(normalized)) section = 'C';
  else if (/Paper\s+B\b.*Section\s*[123]\b/i.test(normalized)) section = 'C';
  else if (/Paper\s+B\b.*Question\s+[23]\b/i.test(normalized)) section = 'B';
  if (!section) throw new Error(`Technology heading has no resolvable section: ${heading}`);
  const rawNumbers = normalized === '2016 - Paper A - Section A - Question 100'
    ? ['10']
    : questionToken.split(',').map(number => number.trim());
  const numbers = rawNumbers.map(number => section === 'A' ? number : `${section}${number}`);
  return {
    year: Number(yearText),
    prefix,
    questionToken,
    tail,
    section,
    numbers,
    n: numbers.join(','),
    sitting: Number(yearText) === 2020 ? 'deferred' : 'main',
  };
};

const englishPaper = (level, year, section) => {
  const fileid = fileidFor(level, 'ev', year, section === 'A' ? 'A' : 'BC');
  return localPapers.find(paper => (
    paper.level === level
    && paper.lang === 'ev'
    && paper.year === year
    && paper.fileid === fileid
  )) ?? null;
};

const associations = [];
const exactTopicsByCard = new Map();
for (const topic of allTopics) {
  for (const heading of topic.officialQuestionHeadings) {
    const parsed = parseHeading(heading);
    if (parsed.year < 2010) {
      associations.push({
        topicId: topic.id,
        variant: topic.variant,
        level: topic.level,
        heading,
        ...parsed,
        resolution: 'source-blocked',
        reason: 'The entitled local SEC Technology corpus begins at 2010. The factual heading remains recorded pending independent acquisition and verification; no StudyClix-hosted question image or PDF is copied.',
      });
      continue;
    }
    const paper = englishPaper(topic.level, parsed.year, parsed.section);
    if (!paper) throw new Error(`${heading}: matching entitled SEC booklet is absent`);
    for (const n of parsed.numbers) {
      if (!paper.q.some(question => question.n === n)) {
        throw new Error(`${heading}: ${paperIdentity(paper)} has no card ${n}`);
      }
      const key = logicalIdentity(topic.level, parsed.year, n);
      const indexes = exactTopicsByCard.get(key) ?? [];
      const index = topicIndex.get(topic.id);
      if (index === undefined) throw new Error(`Unknown Technology topic ${topic.id}`);
      if (!indexes.includes(index)) indexes.push(index);
      exactTopicsByCard.set(key, indexes);
    }
    associations.push({
      topicId: topic.id,
      variant: topic.variant,
      level: topic.level,
      heading,
      ...parsed,
      resolution: 'matched',
      target: {
        level: topic.level,
        lang: 'ev',
        year: parsed.year,
        paperKey: 'single',
        fileid: paper.fileid,
        questionNumbers: parsed.numbers,
      },
    });
  }
}

const topicIdForLabel = (level, label) => {
  const topic = reference.variants[level].topics.find(candidate => candidate.label === label);
  if (!topic) throw new Error(`${level}: unknown Technology topic ${label}`);
  return topic.id;
};
const optionLabels = {
  higher: {
    C1: 'Option: Applied Control Systems',
    C2: 'Option: Electronics & Control',
    C3: 'Option: Information & Communications Technology',
    C4: 'Option: Manufacturing Systems',
    C5: 'Option: Materials Technology',
  },
  ordinary: {
    C1: 'Option 1: Applied Control Systems',
    C2: 'Option 2: Electronics & Control',
    C3: 'Option 3: Information & Communications Technology',
    C4: 'Option 4: Manufacturing Systems',
    C5: 'Option 5: Materials Technology',
  },
};
const REVIEWED_LOCAL_OMISSIONS = {
  'higher|2026|8': {
    labels: ['Communications & Graphics Media'],
    evidence: 'Direct review of the entitled SEC 2026 Higher Section A booklet: Q8 is the graphical-techniques task.',
  },
  'higher|2026|15': {
    labels: ['Communications & Graphics Media'],
    evidence: 'Direct review of the entitled SEC 2026 Higher Section A booklet: Q15 asks for orthographic views of the printed product.',
  },
  'higher|2022|3': {
    labels: ['Technology in Society'],
    evidence: 'Direct review of the entitled SEC 2022 Higher Section A booklet: Q3 addresses environmental, economic, and social sustainable development through water-resource management.',
  },
  'higher|2022|4': {
    labels: ['Energy'],
    evidence: 'Direct review of the entitled SEC 2022 Higher Section A booklet: Q4 asks about hybrid propulsion and the advantages of hybrid buses over diesel-powered buses.',
  },
};
const fallbackLabelForCanonical = (level, canonicalId) => {
  const group = Number(canonicalId.split('-')[1]);
  if (group === 0) return 'A Process of Design';
  if (group === 1 || group === 10) return 'Project & Quality Management';
  if (group === 2 || group === 11) {
    return level === 'higher'
      ? 'Materials and Production (All Materials)'
      : 'Materials & Production';
  }
  if (group === 3) return 'Communications & Graphics Media';
  if (group === 4 || group === 9) return 'Information and Communications Technology';
  if (group === 5) return 'Structures & Mechanisms';
  if (group === 6 && canonicalId === 'technology-6-0') return 'Energy';
  if (group === 6 || group === 7) return 'Electricity & Electronics';
  if (group === 8) return 'A Process of Design';
  throw new Error(`${canonicalId}: no conservative Technology fallback bucket`);
};

const logicalEnglishPapers = localPapers.filter(paper => paper.lang === 'ev');
const questionMappings = [];
const retainedLocalCards = [];
for (const paper of logicalEnglishPapers) {
  for (const question of paper.q) {
    const key = logicalIdentity(paper.level, paper.year, question.n);
    const exact = exactTopicsByCard.get(key) ?? [];
    const indexes = [...exact];
    if (question.n.startsWith('C')) {
      const label = optionLabels[paper.level][question.n];
      const index = topicIndex.get(topicIdForLabel(paper.level, label));
      if (index === undefined) throw new Error(`${key}: missing option topic index`);
      if (!indexes.includes(index)) indexes.push(index);
    }
    const reviewed = REVIEWED_LOCAL_OMISSIONS[key];
    if (!indexes.length && reviewed) {
      for (const label of reviewed.labels) {
        const index = topicIndex.get(topicIdForLabel(paper.level, label));
        if (index !== undefined && !indexes.includes(index)) indexes.push(index);
      }
    }
    if (!indexes.length && paper.fileid.includes('LP014')) {
      const baselinePaper = sourceById.get(paperIdentity(paper));
      const baselineQuestion = baselinePaper?.q.find(candidate => candidate.n === question.n);
      const canonicalIds = baselineQuestion
        ? [baselineQuestion.primary, baselineQuestion.secondary].filter(Boolean)
        : [];
      for (const canonicalId of canonicalIds) {
        const label = fallbackLabelForCanonical(paper.level, canonicalId);
        const index = topicIndex.get(topicIdForLabel(paper.level, label));
        if (index !== undefined && !indexes.includes(index)) indexes.push(index);
      }
    }
    if (!indexes.length) {
      throw new Error(`${key}: local official Technology card lacks a reference or preservation mapping`);
    }
    const canonicalNodeIds = [...new Set(indexes.flatMap(index => (
      curriculumCrosswalk[allTopics[index].id]
    )))];
    if (!exact.length) {
      retainedLocalCards.push({
        level: paper.level,
        year: paper.year,
        paperKey: paper.paperKey,
        fileid: paper.fileid,
        questionNumber: question.n,
        canonicalNodeIds,
        topicIds: indexes.map(index => allTopics[index].id),
        resolution: reviewed
          ? 'retained-local-reviewed'
          : question.n.startsWith('C')
            ? 'retained-local-official-option'
            : 'retained-local-canonical-tag',
        reason: reviewed?.evidence
          ?? (question.n.startsWith('C')
            ? 'The entitled SEC Section C option is omitted from the factual reference topic pages and is retained under its printed option heading.'
            : 'The entitled SEC Section A card is omitted from the factual reference topic pages and is retained through its pre-existing verified canonical tag.'),
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

const mappingByCard = new Map(questionMappings.map(([levelCode, yearOffset, n, indexes]) => [
  `${levelCode}|${yearOffset}|${n}`,
  indexes,
]));
for (const paper of localPapers) {
  if (baselineIds.has(paperIdentity(paper))) continue;
  paper.q = paper.q.map(question => {
    const levelCode = paper.level === 'higher' ? 'h' : 'o';
    const indexes = mappingByCard.get(`${levelCode}|${paper.year - 2000}|${question.n}`);
    const levelIndexes = indexes?.filter(index => allTopics[index].level === paper.level) ?? [];
    const canonicalIds = [...new Set(levelIndexes.flatMap(index => (
      curriculumCrosswalk[allTopics[index].id]
    )))];
    if (!canonicalIds.length) throw new Error(`${paperIdentity(paper)} Q${question.n}: no canonical tag`);
    return {
      n: question.n,
      primary: canonicalIds[0],
      ...(canonicalIds[1] ? { secondary: canonicalIds[1] } : {}),
    };
  });
}

const reported = allTopics.reduce((sum, topic) => sum + topic.reportedQuestionCount, 0);
const official = allTopics.reduce((sum, topic) => sum + topic.officialQuestionHeadings.length, 0);
const mocks = allTopics.reduce((sum, topic) => sum + topic.mockQuestionCount, 0);
const providerSamples = allTopics.reduce((sum, topic) => sum + topic.providerSampleQuestionCount, 0);
const matchedAssociations = associations.filter(item => item.resolution === 'matched');
const sourceBlockedAssociations = associations.filter(item => item.resolution === 'source-blocked');
if (
  reported !== 2127
  || official !== 1190
  || mocks !== 937
  || providerSamples !== 0
  || reported !== official + mocks + providerSamples
  || matchedAssociations.length !== 1118
  || sourceBlockedAssociations.length !== 72
  || questionMappings.length !== 678
) {
  throw new Error('Technology reconciliation coverage changed unexpectedly');
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
    expectedQuestions(paper.level, paper.fileid),
  )) {
    throw new Error(`${paperIdentity(paper)} has a mismatched question map at ${mapPath}`);
  }
  if (map.paperOnly === 1) verifiedPaperOnlyMaps += 1;
  else verifiedSchemeMaps += 1;
}
if (verifiedSchemeMaps !== 61 || verifiedPaperOnlyMaps !== 71) {
  throw new Error('Technology paper/scheme map boundary changed unexpectedly');
}

const groups = LEVELS.map(level => [
  level === 'higher' ? 'h' : 'o',
  `technology-${level}`,
  reference.variants[level].label,
  reference.variants[level].topics.map(topic => topicIndex.get(topic.id)),
]);
const compactTopics = allTopics.map(topic => {
  const prefix = `technology-${topic.level}-`;
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
const files = [...new Set(matchedAssociations.map(item => item.target.fileid))];
const prefixIndex = new Map(prefixes.map((value, index) => [value, index]));
const tailIndex = new Map(tails.map((value, index) => [value, index]));
const fileIndex = new Map(files.map((value, index) => [value, index]));
const compactPartReferences = associations.map(item => [
  topicIndex.get(item.topicId),
  item.year - 2000,
  prefixIndex.get(item.prefix),
  item.questionToken,
  tailIndex.get(item.tail),
  item.n,
  item.resolution === 'matched' ? fileIndex.get(item.target.fileid) : -1,
  item.sitting === 'deferred' ? 'd' : 'm',
]);
if (compactPartReferences.some(row => row.some(value => value === undefined))) {
  throw new Error('Technology compact part reference contains an unknown value');
}

const matchedQuestionTopicLinks = new Set(matchedAssociations.flatMap(item => (
  item.numbers.map(n => [item.topicId, item.level, item.year, n].join('|'))
))).size;
const physicalMappings = localPapers.reduce((sum, paper) => sum + paper.q.length, 0);
const additions = localPapers.filter(paper => !baselineIds.has(paperIdentity(paper)));
const summary = {
  referenceTopics: allTopics.length,
  referenceGroups: 0,
  runtimeDisplayGroups: groups.length,
  referenceReportedAssociations: reported,
  referenceOfficialAssociations: official,
  referenceMockAssociations: mocks,
  referenceProviderSampleAssociations: providerSamples,
  matchedAssociations: matchedAssociations.length,
  sourceBlockedAssociations: sourceBlockedAssociations.length,
  sourceBlockedBreakdown: { beforeLocalCorpus: sourceBlockedAssociations.length },
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
    .filter(topic => topic.reportedQuestionCount === 0)
    .map(topic => topic.id),
};
if (
  physicalMappings !== 1356
  || summary.newlyAddedPaperVariants !== 76
  || summary.newlyAddedPhysicalMappings !== 600
  || summary.emptyReferenceTopics.length !== 6
) {
  throw new Error(`Technology local corpus totals changed unexpectedly: ${JSON.stringify({
    physicalMappings,
    newlyAddedPaperVariants: summary.newlyAddedPaperVariants,
    newlyAddedPhysicalMappings: summary.newlyAddedPhysicalMappings,
    emptyReferenceTopics: summary.emptyReferenceTopics,
  })}`);
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
    preservation: 'Every frozen Section A card remains present; complete Section B/C long-question cards are added from entitled SEC PDFs.',
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
  files,
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
