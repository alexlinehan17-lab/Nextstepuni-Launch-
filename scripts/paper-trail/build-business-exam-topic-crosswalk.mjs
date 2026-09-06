#!/usr/bin/env node
/**
 * Reconcile the factual Business reference hierarchy with the complete,
 * entitled SEC corpus. The output keeps both overlapping course structures,
 * every part-aware factual heading, and a compact top-level question join.
 */

import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const HERE = path.dirname(fileURLToPath(import.meta.url));
const ROOT = path.resolve(HERE, '../..');
const SUBJECT_ID = 'business';
const TAGS_PATH = path.join(HERE, 'topic-tags/tags/business.json');
const REFERENCE_PATH = path.join(ROOT, 'data/examTopics/business.json');
const CURRICULUM_CROSSWALK_PATH = path.join(
  ROOT, 'data/examTopics/business-curriculum-crosswalk.json',
);
const REVIEWED_PATH = path.join(
  ROOT, 'data/examTopics/business-reviewed-question-topics.json',
);
const OUTPUT_PATH = path.join(ROOT, 'data/examTopics/business-local-crosswalk.json');
const RUNTIME_PATH = path.join(ROOT, 'data/examTopics/business-runtime.json');
const BASELINE_PATH = path.join(
  ROOT, 'test/fixtures/businessTopicQuestionBaseline.json',
);
const HOSTED_ROOT = path.join(ROOT, 'public/paper-anchors');

const readJson = file => JSON.parse(fs.readFileSync(file, 'utf8'));
const reference = readJson(REFERENCE_PATH);
const curriculumCrosswalk = readJson(CURRICULUM_CROSSWALK_PATH);
const reviewed = readJson(REVIEWED_PATH);
const localPapers = readJson(TAGS_PATH);
const preservationBaseline = readJson(BASELINE_PATH);

const VARIANTS = [
  'higher-new-course',
  'higher-old-course',
  'ordinary-new-course',
  'ordinary-old-course',
];
const allTopics = VARIANTS.flatMap(variant => (
  reference.variants[variant].topics.map(topic => ({
    ...topic,
    variant,
    level: variant.startsWith('higher') ? 'higher' : 'ordinary',
    course: variant.includes('new-course') ? 'new' : 'old',
  }))
));
const topicIndex = new Map(allTopics.map((topic, index) => [topic.id, index]));

const referenceTopicIds = allTopics.map(topic => topic.id).sort();
const curriculumTopicIds = Object.keys(curriculumCrosswalk).sort();
if (JSON.stringify(referenceTopicIds) !== JSON.stringify(curriculumTopicIds)) {
  throw new Error('Business curriculum crosswalk must cover all 105 reference topics exactly once');
}
for (const topic of allTopics) {
  const nodes = curriculumCrosswalk[topic.id];
  if (!Array.isArray(nodes) || !nodes.length || new Set(nodes).size !== nodes.length) {
    throw new Error(`${topic.id}: curriculum crosswalk must contain unique nodes`);
  }
  for (const node of nodes) {
    if (topic.course === 'new' && !/^business-2027-(?:u\d|[1-4]-\d)$/.test(node)) {
      throw new Error(`${topic.id}: invalid redeveloped node ${node}`);
    }
    if (topic.course === 'old' && !/^business-[0-6]-\d+$/.test(node)) {
      throw new Error(`${topic.id}: invalid outgoing node ${node}`);
    }
  }
}

const paperIdentity = paper => [
  paper.level, paper.lang, paper.year, paper.paperKey, paper.fileid,
].join('|');
const logicalIdentity = (level, year, paperKey, n) => (
  [level, year, paperKey, n].join('|')
);
const expectedNumbers = (level, year, paperKey) => {
  if (year <= 2019) {
    return level === 'higher'
      ? [
          ...Array.from({ length: 10 }, (_, index) => String(index + 1)),
          'ABQ',
          ...Array.from({ length: 7 }, (_, index) => `S3Q${index + 1}`),
        ]
      : [
          ...Array.from({ length: 15 }, (_, index) => String(index + 1)),
          ...Array.from({ length: 8 }, (_, index) => `S2Q${index + 1}`),
        ];
  }
  if (level === 'higher') {
    return paperKey === 'p1'
      ? Array.from({ length: year === 2020 ? 10 : 12 }, (_, index) => String(index + 1))
      : ['ABQ', ...Array.from({ length: year === 2020 ? 7 : 8 }, (_, index) => String(index + 1))];
  }
  return paperKey === 'p1'
    ? Array.from({ length: 15 }, (_, index) => String(index + 1))
    : Array.from({ length: year === 2020 ? 8 : 9 }, (_, index) => String(index + 1));
};

const paperIds = localPapers.map(paperIdentity);
if (paperIds.length !== new Set(paperIds).size || localPapers.length !== 96) {
  throw new Error('Business local corpus must contain 96 unique physical documents');
}
for (const paper of localPapers) {
  const expected = expectedNumbers(paper.level, paper.year, paper.paperKey);
  if (JSON.stringify(paper.q.map(question => question.n)) !== JSON.stringify(expected)) {
    throw new Error(`${paperIdentity(paper)}: incomplete or reordered top-level questions`);
  }
  const anchorPath = path.join(
    HOSTED_ROOT, String(paper.year), `${paper.fileid}.json`,
  );
  if (!fs.existsSync(anchorPath)) throw new Error(`${paperIdentity(paper)}: missing hosted anchors`);
  const anchors = readJson(anchorPath);
  if (
    anchors.paperOnly !== 1
    || JSON.stringify(anchors.q.map(question => question.n)) !== JSON.stringify(expected)
  ) {
    throw new Error(`${anchorPath}: hosted anchors do not match Business tags`);
  }
}

let preservedBaselineCards = 0;
for (const expected of preservationBaseline) {
  const live = localPapers.find(paper => paperIdentity(paper) === paperIdentity(expected));
  if (!live) throw new Error(`Preservation failure: missing ${paperIdentity(expected)}`);
  for (const number of expected.questions) {
    if (!live.q.some(question => question.n === number)) {
      throw new Error(`Preservation failure: missing ${paperIdentity(expected)} ${number}`);
    }
    preservedBaselineCards += 1;
  }
}

const parseHeading = (heading, level) => {
  const match = heading.match(
    /^(\d{4}) - (.*?Question\s+)(ABQ|A-C|[A-C]|\d+)(.*)$/i,
  );
  if (!match) throw new Error(`Unparseable Business heading: ${heading}`);
  const [, yearText, prefix, questionToken, tail] = match;
  const year = Number(yearText);
  const sitting = /Deferred Exam Paper/i.test(prefix)
    ? 'deferred'
    : /Sample Paper/i.test(prefix)
      ? 'sample'
      : 'main';
  const sections = [...prefix.matchAll(
    /Sections?\s+([123AB])(?:\s*&\s*([123]))?/gi,
  )].flatMap(section => section.slice(1).filter(Boolean).map(value => value.toUpperCase()));
  let paperKey = 'single';
  if (year >= 2020) {
    if (/^Paper\s*-\s*Sections?\s+2(?:\s*&\s*3)?/i.test(prefix)) {
      paperKey = 'p2';
    } else if (/^Paper\s*-\s*Section\s+1/i.test(prefix)) {
      paperKey = 'p1';
    } else {
      paperKey = sections[0] === '1' || sections[0] === 'A' ? 'p1' : 'p2';
    }
  }
  const token = questionToken.toUpperCase();
  let n;
  if (level === 'higher') {
    const semanticSection = sections.at(-1) ?? '';
    n = token === 'ABQ'
      || ['A', 'B', 'C', 'A-C'].includes(token)
      || ['2', 'B'].includes(semanticSection)
      ? 'ABQ'
      : year <= 2019 && semanticSection === '3'
        ? `S3Q${token}`
        : token;
  } else {
    n = year <= 2019 && ['2', 'B'].includes(sections[0])
      ? `S2Q${token}`
      : token;
  }
  return { year, sitting, prefix, questionToken, tail, paperKey, n };
};

const englishPaper = (level, year, paperKey, n) => {
  const candidates = localPapers.filter(paper => (
    paper.level === level
    && paper.lang === 'ev'
    && paper.year === year
    && paper.paperKey === paperKey
    && paper.q.some(question => question.n === n)
  ));
  if (candidates.length > 1) {
    throw new Error(`Ambiguous Business card ${logicalIdentity(level, year, paperKey, n)}`);
  }
  return candidates[0] ?? null;
};

const associations = [];
const exactTopicsByCard = new Map();
for (const topic of allTopics) {
  for (const heading of topic.officialQuestionHeadings) {
    const parsed = parseHeading(heading, topic.level);
    const explicitBlock = parsed.year < 2010
      ? 'The entitled local SEC Business corpus currently begins at 2010. The factual heading is retained pending an independently verified official paper; no StudyClix-hosted question image or PDF is copied.'
      : parsed.sitting === 'sample'
        ? 'Sample-paper content is not part of the entitled local SEC examination corpus. The factual heading is retained; no StudyClix-hosted question image or PDF is copied.'
        : parsed.sitting === 'deferred'
          ? 'The entitled local corpus does not contain this separate deferred sitting. The factual heading is retained; no StudyClix-hosted question image or PDF is copied.'
          : null;
    const paper = explicitBlock
      ? null
      : englishPaper(topic.level, parsed.year, parsed.paperKey, parsed.n);
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
          ?? 'No matching entitled local SEC document is present. The factual heading is retained pending independent verification; no StudyClix-hosted question image or PDF is copied.',
      });
      continue;
    }
    const key = logicalIdentity(topic.level, parsed.year, parsed.paperKey, parsed.n);
    const indexes = exactTopicsByCard.get(key) ?? [];
    const index = topicIndex.get(topic.id);
    if (index === undefined) throw new Error(`Unknown Business topic ${topic.id}`);
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
        paperKey: parsed.paperKey,
        fileid: paper.fileid,
        questionNumber: parsed.n,
      },
    });
  }
}

const topicForCode = (level, course, code) => {
  const variant = `${level}-${course}-course`;
  const topics = reference.variants[variant].topics;
  let topic;
  if (code === 'ABQ 3-4-5') {
    topic = topics.find(candidate => candidate.label === 'ABQ (Units 3, 4 & 5)');
  } else if (/^U\d$/i.test(code)) {
    topic = topics.find(candidate => candidate.label.startsWith(`${code}.`));
  } else {
    topic = topics.find(candidate => candidate.label.startsWith(`${code} `));
  }
  if (!topic) throw new Error(`${level}/${course}: unknown reviewed code ${code}`);
  return topic.id;
};

const logicalEnglishPapers = localPapers.filter(paper => paper.lang === 'ev');
const questionMappings = [];
const retainedLocalCards = [];
const usedReviewed = new Set();
for (const paper of logicalEnglishPapers) {
  for (const question of paper.q) {
    const key = logicalIdentity(paper.level, paper.year, paper.paperKey, question.n);
    let indexes = exactTopicsByCard.get(key);
    if (!indexes) {
      const review = reviewed.questions[key];
      if (!review) throw new Error(`${key}: reference omission lacks direct SEC review`);
      const ids = [
        ...review.old.map(code => topicForCode(paper.level, 'old', code)),
        ...review.new.map(code => topicForCode(paper.level, 'new', code)),
      ];
      indexes = [...new Set(ids)].map(id => topicIndex.get(id));
      if (!indexes.length || indexes.some(index => index === undefined)) {
        throw new Error(`${key}: invalid reviewed Business mapping`);
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
        reason: paper.year === 2026
          ? 'Official SEC 2026 task retained from direct paper review; it post-dates the factual reference snapshot.'
          : 'Entitled SEC task omitted from the factual reference snapshot and retained from direct review of the official paper.',
      });
    }
    questionMappings.push([
      paper.level === 'higher' ? 'h' : 'o',
      paper.year - 2000,
      paper.paperKey === 'single' ? 's' : paper.paperKey === 'p1' ? '1' : '2',
      question.n,
      indexes,
    ]);
  }
}
const reviewedKeys = Object.keys(reviewed.questions).sort();
if (JSON.stringify([...usedReviewed].sort()) !== JSON.stringify(reviewedKeys)) {
  throw new Error('Reviewed Business map must equal the exact local-reference omissions');
}

const reported = allTopics.reduce((sum, topic) => sum + topic.reportedQuestionCount, 0);
const official = allTopics.reduce((sum, topic) => sum + topic.officialQuestionHeadings.length, 0);
const mocks = allTopics.reduce((sum, topic) => sum + topic.mockQuestionCount, 0);
const providerSamples = allTopics.reduce((sum, topic) => sum + topic.providerSampleQuestionCount, 0);
if (
  allTopics.length !== 105
  || reported !== 5708
  || official !== 3075
  || mocks !== 2437
  || providerSamples !== 196
  || reported !== official + mocks + providerSamples
) {
  throw new Error('Business factual audit totals changed unexpectedly');
}
if (
  associations.filter(item => item.resolution === 'matched').length !== 2008
  || associations.filter(item => item.resolution === 'source-blocked').length !== 1067
  || exactTopicsByCard.size !== 663
  || retainedLocalCards.length !== 58
  || questionMappings.length !== 721
) {
  throw new Error('Business reconciliation coverage changed unexpectedly');
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
if (groups.some(group => group[4].some(index => index === undefined))) {
  throw new Error('Business group contains an unknown topic');
}

const compactTopics = allTopics.map(topic => {
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
  item.paperKey === 'single' ? 's' : item.paperKey === 'p1' ? '1' : '2',
  item.n,
]);
if (compactPartReferences.some(row => row.some(value => value === undefined))) {
  throw new Error('Business compact part reference contains an unknown value');
}

const matchedAssociations = associations.filter(item => item.resolution === 'matched');
const sourceBlockedAssociations = associations.filter(item => item.resolution === 'source-blocked');
const matchedQuestionTopicLinks = new Set(matchedAssociations.map(item => [
  item.topicId, item.level, item.year, item.paperKey, item.n,
].join('|'))).size;
const physicalCards = localPapers.reduce((sum, paper) => sum + paper.q.length, 0);
const summary = {
  referenceTopics: allTopics.length,
  referenceReportedAssociations: reported,
  referenceOfficialAssociations: official,
  referenceMockAssociations: mocks,
  referenceProviderSampleAssociations: providerSamples,
  matchedAssociations: matchedAssociations.length,
  sourceBlockedAssociations: sourceBlockedAssociations.length,
  matchedLogicalCards: exactTopicsByCard.size,
  matchedQuestionTopicLinks,
  retainedLocalLogicalCards: retainedLocalCards.length,
  localPaperDocuments: localPapers.length,
  localPhysicalCards: physicalCards,
  localLogicalQuestions: questionMappings.length,
  hostedAnchorMaps: localPapers.filter(paper => fs.existsSync(path.join(
    HOSTED_ROOT, String(paper.year), `${paper.fileid}.json`,
  ))).length,
  preservedBaselineVariants: preservationBaseline.length,
  preservedBaselineCards,
  emptyReferenceTopics: allTopics
    .filter(topic => topic.officialQuestionHeadings.length === 0)
    .map(topic => topic.id),
};
if (physicalCards !== 1442 || summary.hostedAnchorMaps !== 96 || preservedBaselineCards !== 523) {
  throw new Error('Business local corpus or preservation totals changed unexpectedly');
}

const evidence = {
  schemaVersion: 1,
  subjectId: SUBJECT_ID,
  capturedAt: reference.capturedAt,
  referenceProvider: reference.reference.provider,
  rightsBoundary: reference.reference.excludedContent,
  providerSamplePolicy: reference.reference.providerSamplePolicy,
  policy: {
    curriculumAuthority: 'NCCA/Curriculum Online',
    examAuthority: 'State Examinations Commission',
    commercialReferenceUse: 'Factual topic labels, hierarchy, headings, and counts only.',
  },
  summary,
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
};

fs.writeFileSync(OUTPUT_PATH, `${JSON.stringify(evidence, null, 2)}\n`);
fs.writeFileSync(RUNTIME_PATH, JSON.stringify(runtime));
console.log(JSON.stringify(summary, null, 2));
console.log(`runtimeBytes ${fs.statSync(RUNTIME_PATH).size}`);
