#!/usr/bin/env node
/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 *
 * Reconcile the factual Art reference headings with the complete entitled SEC
 * corpus. Art needs a file-aware join: through 2017, independently selectable
 * practical booklets and the written paper all restart their numbering at Q1.
 * The official curriculum remains canonical and no commercial question text,
 * image, solution, note, video, or PDF is stored here.
 */

import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const HERE = path.dirname(fileURLToPath(import.meta.url));
const ROOT = path.resolve(HERE, '../..');
const SUBJECT_ID = 'art';
const TAGS_PATH = path.join(HERE, 'topic-tags/tags/art.json');
const REFERENCE_PATH = path.join(ROOT, 'data/examTopics/art.json');
const CURRICULUM_CROSSWALK_PATH = path.join(
  ROOT,
  'data/examTopics/art-curriculum-crosswalk.json',
);
const OUTPUT_PATH = path.join(ROOT, 'data/examTopics/art-local-crosswalk.json');
const RUNTIME_PATH = path.join(ROOT, 'data/examTopics/art-runtime.json');
const BASELINE_PATH = path.join(ROOT, 'test/fixtures/artTopicQuestionBaseline.json');
const AUTHORED_PATH = path.join(ROOT, 'components/MarkBank/cards/art/authored.json');
const HOSTED_ROOT = path.join(ROOT, 'public/paper-anchors');
const LEVELS = ['higher', 'ordinary'];
const NEW_YEARS = [2026, 2025, 2024, 2023];
const WRITTEN_COMPONENTS = new Set(['000', '013']);

const readJson = file => JSON.parse(fs.readFileSync(file, 'utf8'));
const reference = readJson(REFERENCE_PATH);
const curriculumCrosswalk = readJson(CURRICULUM_CROSSWALK_PATH);
const sourcePapers = readJson(TAGS_PATH);
const preservationBaseline = readJson(BASELINE_PATH);
const authored = readJson(AUTHORED_PATH);

const allTopics = LEVELS.flatMap(level => reference.variants[level].topics);
const topicIndex = new Map(allTopics.map((topic, index) => [topic.id, index]));
const topicLevel = new Map(LEVELS.flatMap(level => (
  reference.variants[level].topics.map(topic => [topic.id, level])
)));

if (reference.subjectId !== SUBJECT_ID || allTopics.length !== 32) {
  throw new Error(`Expected the 32-topic Art reference, found ${allTopics.length}`);
}
const crosswalkKeys = Object.keys(curriculumCrosswalk).sort();
const topicIds = allTopics.map(topic => topic.id).sort();
if (JSON.stringify(crosswalkKeys) !== JSON.stringify(topicIds)) {
  throw new Error('Art curriculum crosswalk must cover every reference topic exactly once');
}
for (const [topicId, nodeIds] of Object.entries(curriculumCrosswalk)) {
  if (!Array.isArray(nodeIds) || !nodeIds.length || new Set(nodeIds).size !== nodeIds.length) {
    throw new Error(`${topicId}: curriculum crosswalk must contain unique canonical nodes`);
  }
  for (const nodeId of nodeIds) {
    if (!/^art-[0-6]-\d+$/.test(nodeId)) {
      throw new Error(`${topicId}: invalid canonical Art node ${nodeId}`);
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
const componentCode = fileid => {
  const code = fileid.match(/LP(\d{3})/)?.[1];
  if (!code) throw new Error(`Unrecognised Art paper file id: ${fileid}`);
  return code;
};
const englishTwin = fileid => fileid.replace(/IV\.pdf$/i, 'EV.pdf');
const logicalFileid = fileid => fileid.replace(/(?:EV|IV)\.pdf$/i, 'BV.pdf');
const logicalCardKey = (paper, n) => [
  paper.level,
  paper.year,
  logicalFileid(paper.fileid),
  n,
].join('|');

// The 2023–2026 written papers and marking schemes are already in Paper Trail.
// Add their verified 19-question answer-map identities to the topic-tag source.
// Canonical tags are filled after the reference association pass below.
const additions = [];
for (const year of NEW_YEARS) {
  for (const level of LEVELS) {
    for (const lang of ['ev', 'iv']) {
      const fileid = `LC014${level === 'higher' ? 'A' : 'G'}LP000${lang.toUpperCase()}.pdf`;
      const identity = [level, lang, year, 'single', fileid].join('|');
      if (sourcePapers.some(paper => paperIdentity(paper) === identity)) continue;
      const answerPath = path.join(HERE, 'answers', String(year), `${fileid}.json`);
      if (!fs.existsSync(answerPath)) throw new Error(`Missing Art answer map: ${answerPath}`);
      const answerMap = readJson(answerPath);
      const expectedNumbers = Array.from({ length: 19 }, (_, index) => String(index + 1));
      if (JSON.stringify(answerMap.q?.map(question => question.n)) !== JSON.stringify(expectedNumbers)) {
        throw new Error(`${identity}: answer map must contain Q1–Q19 exactly`);
      }
      additions.push({
        subjectId: SUBJECT_ID,
        level,
        lang,
        year,
        fileid,
        paperKey: 'single',
        q: expectedNumbers.map(n => ({ n, primary: 'art-6-4' })),
      });
    }
  }
}
const localPapers = [...additions, ...sourcePapers];

const paperIds = localPapers.map(paperIdentity);
const duplicatePaperIds = paperIds.filter((identity, index) => paperIds.indexOf(identity) !== index);
if (duplicatePaperIds.length) {
  throw new Error(`Duplicate Art paper variants: ${[...new Set(duplicatePaperIds)].join(', ')}`);
}
if (localPapers.length !== 152) {
  throw new Error(`Expected 152 Art paper variants after supplementation, found ${localPapers.length}`);
}
for (const paper of localPapers) {
  if (
    paper.subjectId !== SUBJECT_ID
    || !LEVELS.includes(paper.level)
    || !['ev', 'iv'].includes(paper.lang)
    || paper.paperKey !== 'single'
    || !['000', '009', '010', '011', '013'].includes(componentCode(paper.fileid))
  ) {
    throw new Error(`Unexpected Art paper identity: ${paperIdentity(paper)}`);
  }
}

let preservedBaselineCards = 0;
const baselinePaperIds = new Set(preservationBaseline.map(paperIdentity));
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
if (preservationBaseline.length !== 136 || preservedBaselineCards !== 1850) {
  throw new Error('The frozen Art preservation baseline changed unexpectedly');
}
const supplementedPapers = localPapers.filter(paper => !baselinePaperIds.has(paperIdentity(paper)));
if (supplementedPapers.length !== 16) {
  throw new Error(`Expected 16 post-baseline Art written-paper variants, found ${supplementedPapers.length}`);
}

const clean = value => value.replace(/\s+/g, ' ').trim();
const parseHeading = heading => {
  const normalized = clean(heading);
  const year = Number(normalized.match(/^(\d{4})/)?.[1]);
  const sectionMatches = [...normalized.matchAll(/Section\s+(A|B|C|I{1,3}|[123])\b/gi)];
  const section = sectionMatches.at(-1)?.[1].toUpperCase();
  const number = normalized.match(/Question\s+(\d+)\b/i)?.[1];
  if (!year || !section || !number) throw new Error(`Unparseable Art heading: ${heading}`);
  return {
    year,
    sitting: /Deferred Exam Paper/i.test(normalized)
      ? 'deferred'
      : /Sample Paper/i.test(normalized)
        ? 'sample'
        : 'main',
    section,
    questionNumber: number,
  };
};

const EnglishWrittenPaper = (level, year) => {
  const candidates = localPapers.filter(paper => (
    paper.level === level
    && paper.lang === 'ev'
    && paper.year === year
    && WRITTEN_COMPONENTS.has(componentCode(paper.fileid))
  ));
  if (candidates.length > 1) {
    throw new Error(`Ambiguous ${level} English Art written paper for ${year}`);
  }
  return candidates[0] ?? null;
};

const blockedReason = parsed => {
  if (parsed.year < 2010) {
    return 'The entitled local SEC Art corpus currently begins at 2010. This factual heading is retained pending acquisition and independent verification of the official paper and marking scheme; no StudyClix-hosted question image or PDF is copied.';
  }
  if (parsed.sitting === 'sample') {
    return 'The entitled Paper Trail corpus does not currently carry this sample booklet as a selectable paper. The factual heading is retained pending independent verification from an official source; no StudyClix-hosted question image or PDF is copied.';
  }
  if (parsed.sitting === 'deferred') {
    return 'The entitled Paper Trail corpus does not currently carry this deferred-sitting booklet. The factual heading is retained pending independent verification from an official source; no StudyClix-hosted question image or PDF is copied.';
  }
  return null;
};

const associations = [];
for (const level of LEVELS) {
  for (const topic of reference.variants[level].topics) {
    for (const heading of topic.officialQuestionHeadings) {
      const parsed = parseHeading(heading);
      const explicitBlock = blockedReason(parsed);
      const paper = explicitBlock ? null : EnglishWrittenPaper(level, parsed.year);
      const localQuestion = paper?.q.find(question => question.n === parsed.questionNumber);
      if (explicitBlock || !paper || !localQuestion) {
        associations.push({
          topicId: topic.id,
          level,
          heading,
          ...parsed,
          resolution: 'source-blocked',
          reason: explicitBlock
            ?? 'No matching entitled local SEC Art written-paper card is present. The factual heading is retained pending independent verification; no StudyClix-hosted question image or PDF is copied.',
        });
        continue;
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
          paperKey: 'single',
          fileid: paper.fileid,
          questionNumber: parsed.questionNumber,
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
const referenceProviderSampleAssociations = allTopics.reduce(
  (sum, topic) => sum + topic.providerSampleQuestionCount,
  0,
);
const referenceReportedAssociations = allTopics.reduce(
  (sum, topic) => sum + topic.reportedQuestionCount,
  0,
);
if (
  referenceOfficialAssociations !== 690
  || referenceMockAssociations !== 609
  || referenceProviderSampleAssociations !== 0
  || referenceReportedAssociations !== 1299
) {
  throw new Error('Art factual audit totals changed unexpectedly');
}
if (associations.length !== referenceOfficialAssociations) {
  throw new Error(`Expected ${referenceOfficialAssociations} reconciliations, found ${associations.length}`);
}

const exactTopicsByCard = new Map();
for (const association of associations.filter(item => item.resolution === 'matched')) {
  const key = [
    association.level,
    association.year,
    association.target.fileid,
    association.target.questionNumber,
  ].join('|');
  const indexes = exactTopicsByCard.get(key) ?? [];
  const index = topicIndex.get(association.topicId);
  if (index === undefined) throw new Error(`Unknown Art topic ${association.topicId}`);
  if (!indexes.includes(index)) indexes.push(index);
  exactTopicsByCard.set(key, indexes);
}

// Current Mark Bank cards contain directly reviewed canonical classifications
// for every 2023–2025 written question. They improve Syllabus X-Ray links while
// leaving the level-aware reference topic identity untouched.
const authoredCanonicalByCard = new Map();
for (const card of authored.cards) {
  if (card.year < 2023 || card.year > 2025) continue;
  const n = card.questionRef.match(/\bQ(\d+)\b/i)?.[1];
  if (!n) throw new Error(`Cannot read Art authored question identity: ${card.questionRef}`);
  const key = [card.level, card.year, n].join('|');
  const nodes = authoredCanonicalByCard.get(key) ?? [];
  if (!nodes.includes(card.topicId)) nodes.push(card.topicId);
  authoredCanonicalByCard.set(key, nodes);
}
if (authoredCanonicalByCard.size !== 114) {
  throw new Error(`Expected 114 reviewed 2023–2025 Art question identities, found ${authoredCanonicalByCard.size}`);
}

const higherFallbackTopicByNode = {
  'art-0-0': 'art-higher-artists-theory-and-thinking',
  'art-0-1': 'art-higher-artists-processes-and-media',
  'art-0-2': 'art-higher-artists-processes-and-media',
  'art-0-3': 'art-higher-artists-theory-and-thinking',
  'art-0-4': 'art-higher-artists-processes-and-media',
  'art-1-0': 'art-higher-artists-processes-and-media',
  'art-1-1': 'art-higher-artists-theory-and-thinking',
  'art-1-2': 'art-higher-artists-processes-and-media',
  'art-1-3': 'art-higher-artists-processes-and-media',
  'art-2-0': 'art-higher-artists-theory-and-thinking',
  'art-2-1': 'art-higher-artists-theory-and-thinking',
  'art-2-2': 'art-higher-art-as-social-commentary-or-commentator',
  'art-2-3': 'art-higher-artists-theory-and-thinking',
  'art-2-4': 'art-higher-artists-processes-and-media',
  'art-3-0': 'art-higher-artists-theory-and-thinking',
  'art-3-1': 'art-higher-section-a-generic-questions',
  'art-3-2': 'art-higher-artists-theory-and-thinking',
  'art-3-3': 'art-higher-artists-processes-and-media',
  'art-3-4': 'art-higher-artists-processes-and-media',
  'art-3-5': 'art-higher-artists-processes-and-media',
};
const fallbackTopicForNode = (level, nodeId) => {
  const direct = allTopics
    .map((topic, index) => ({ topic, index }))
    .filter(({ topic }) => topicLevel.get(topic.id) === level && curriculumCrosswalk[topic.id].includes(nodeId));
  if (direct.length === 1) return direct[0].index;
  if (level === 'ordinary' && /^art-[0-3]-\d+$/.test(nodeId)) {
    return topicIndex.get('art-ordinary-section-a-todays-world');
  }
  if (level === 'higher' && higherFallbackTopicByNode[nodeId]) {
    return topicIndex.get(higherFallbackTopicByNode[nodeId]);
  }
  if (direct.length > 1) {
    return direct.sort((left, right) => (
      curriculumCrosswalk[left.topic.id].length - curriculumCrosswalk[right.topic.id].length
      || left.index - right.index
    ))[0].index;
  }
  throw new Error(`No ${level} Art exam topic covers canonical node ${nodeId}`);
};

const canonicalNodesForNewPaper = (paper, n, exactIndexes) => {
  const reviewed = authoredCanonicalByCard.get([paper.level, paper.year, n].join('|'));
  if (reviewed?.length) return reviewed;
  const topicIdsForCard = exactIndexes.map(index => allTopics[index].id);
  if (
    paper.level === 'ordinary'
    && topicIdsForCard.length === 1
    && topicIdsForCard[0] === 'art-ordinary-section-a-todays-world'
  ) {
    return ['art-6-4'];
  }
  return [...new Set(topicIdsForCard.flatMap(topicId => curriculumCrosswalk[topicId]))].slice(0, 2);
};

for (const paper of supplementedPapers) {
  for (const question of paper.q) {
    const exactIndexes = exactTopicsByCard.get([
      paper.level,
      paper.year,
      englishTwin(paper.fileid),
      question.n,
    ].join('|')) ?? [];
    const reviewed = authoredCanonicalByCard.get([paper.level, paper.year, question.n].join('|'));
    let canonicalNodes;
    if (reviewed?.length) {
      canonicalNodes = reviewed;
    } else {
      if (!exactIndexes.length) {
        throw new Error(`${paperIdentity(paper)} Q${question.n}: missing exact or reviewed mapping`);
      }
      canonicalNodes = canonicalNodesForNewPaper(paper, question.n, exactIndexes);
    }
    if (!canonicalNodes.length || canonicalNodes.length > 2) {
      throw new Error(`${paperIdentity(paper)} Q${question.n}: invalid canonical mapping`);
    }
    question.primary = canonicalNodes[0];
    if (canonicalNodes[1]) question.secondary = canonicalNodes[1];
    else delete question.secondary;
  }
}

const questionMappings = [];
const retainedLocalCards = [];
const retainedLogical = new Set();
for (const paper of localPapers) {
  for (const question of paper.q) {
    const exactKey = [
      paper.level,
      paper.year,
      englishTwin(paper.fileid),
      question.n,
    ].join('|');
    let indexes = exactTopicsByCard.get(exactKey);
    if (!indexes) {
      indexes = [...new Set(
        [question.primary, question.secondary]
          .filter(Boolean)
          .map(nodeId => fallbackTopicForNode(paper.level, nodeId)),
      )];
      const logicalKey = logicalCardKey(paper, question.n);
      if (!retainedLogical.has(logicalKey)) {
        retainedLogical.add(logicalKey);
        retainedLocalCards.push({
          level: paper.level,
          year: paper.year,
          fileid: logicalFileid(paper.fileid),
          component: componentCode(paper.fileid),
          questionNumber: question.n,
          canonicalNodeIds: [question.primary, question.secondary].filter(Boolean),
          topicIds: indexes.map(index => allTopics[index].id),
          resolution: 'retained-local',
          reason: paper.year === 2023 && paper.level === 'ordinary'
            ? 'Official SEC 2023 Ordinary Visual Studies question retained from direct paper review; the factual reference snapshot omits that complete paper.'
            : WRITTEN_COMPONENTS.has(componentCode(paper.fileid))
              ? 'Entitled SEC written-paper card preserved locally although the factual reference snapshot has no association for this top-level question.'
              : 'Entitled SEC practical-component choice preserved through its verified canonical tag; the reference hierarchy covers Visual Studies questions only.',
        });
      }
    }
    if (!indexes.length) throw new Error(`${paperIdentity(paper)} Q${question.n}: empty topic mapping`);
    questionMappings.push([
      paper.level === 'higher' ? 'h' : 'o',
      paper.lang === 'ev' ? 'e' : 'i',
      paper.year - 2000,
      componentCode(paper.fileid),
      question.n,
      indexes,
    ]);
  }
}

let verifiedSchemeMaps = 0;
let verifiedPaperOnlyMaps = 0;
for (const paper of localPapers) {
  const classicPath = path.join(HERE, 'answers', String(paper.year), `${paper.fileid}.json`);
  const hostedPath = path.join(HOSTED_ROOT, String(paper.year), `${paper.fileid}.json`);
  const mapPath = fs.existsSync(classicPath) ? classicPath : fs.existsSync(hostedPath) ? hostedPath : null;
  if (!mapPath) throw new Error(`${paperIdentity(paper)} has no question anchor map`);
  const map = readJson(mapPath);
  const expected = paper.q.map(question => question.n);
  const actual = map.q?.map(question => question.n);
  if (JSON.stringify(actual) !== JSON.stringify(expected)) {
    throw new Error(`${paperIdentity(paper)} has a mismatched question map at ${mapPath}`);
  }
  if (map.paperOnly === 1) verifiedPaperOnlyMaps += 1;
  else verifiedSchemeMaps += 1;
}

const matchedAssociations = associations.filter(item => item.resolution === 'matched');
const sourceBlockedAssociations = associations.filter(item => item.resolution === 'source-blocked');
const matchedQuestionTopicLinks = new Set(matchedAssociations.map(item => [
  item.topicId,
  item.level,
  item.year,
  item.target.fileid,
  item.target.questionNumber,
].join('|'))).size;
const physicalMappings = localPapers.reduce((sum, paper) => sum + paper.q.length, 0);
const distinctStudentFacingQuestions = new Set(localPapers.flatMap(paper => (
  paper.q.map(question => logicalCardKey(paper, question.n))
))).size;
const retainedWrittenLogicalCards = retainedLocalCards.filter(card => (
  WRITTEN_COMPONENTS.has(card.component)
)).length;
const retainedPracticalLogicalCards = retainedLocalCards.length - retainedWrittenLogicalCards;

if (physicalMappings !== 2154 || questionMappings.length !== 2154) {
  throw new Error(`Expected 2,154 physical Art mappings, found ${questionMappings.length}`);
}
if (distinctStudentFacingQuestions !== 1077) {
  throw new Error(`Expected 1,077 Art logical questions, found ${distinctStudentFacingQuestions}`);
}
if (exactTopicsByCard.size + retainedLocalCards.length !== distinctStudentFacingQuestions) {
  throw new Error('Every logical Art card must be exactly matched or explicitly retained');
}
if (
  matchedAssociations.length !== 592
  || sourceBlockedAssociations.length !== 98
  || exactTopicsByCard.size !== 541
  || matchedQuestionTopicLinks !== 584
  || retainedLocalCards.length !== 536
  || retainedWrittenLogicalCards !== 144
  || retainedPracticalLogicalCards !== 392
) {
  throw new Error('Art reference/local reconciliation counts changed unexpectedly');
}
if (verifiedSchemeMaps !== 65 || verifiedPaperOnlyMaps !== 87) {
  throw new Error('Art paper/scheme map boundary changed unexpectedly');
}

const groups = [];
for (const level of LEVELS) {
  if (level === 'ordinary') {
    const id = 'art-ordinary-section-a-todays-world';
    groups.push(['o', id, "Section A: Today's World", [topicIndex.get(id)]]);
  }
  for (const group of reference.variants[level].groups) {
    groups.push([
      level === 'higher' ? 'h' : 'o',
      group.id,
      group.label,
      group.topicIds.map(topicId => topicIndex.get(topicId)),
    ]);
  }
}
if (groups.length !== 6 || groups.some(group => group[3].some(index => index === undefined))) {
  throw new Error('Art runtime hierarchy must contain the three sections at both levels');
}
const runtimeTopics = allTopics.map(topic => [
  topic.id,
  topic.label,
  topic.sourcePath,
  topic.mockQuestionCount,
  topic.providerSampleQuestionCount,
  curriculumCrosswalk[topic.id],
  topicLevel.get(topic.id) === 'higher' ? 'h' : 'o',
  topic.reportedQuestionCount,
]);
const sittingCode = { main: 'm', deferred: 'd', sample: 's' };
const partReferences = associations.map(association => [
  topicIndex.get(association.topicId),
  association.year - 2000,
  sittingCode[association.sitting],
  association.resolution === 'matched' ? componentCode(association.target.fileid) : '',
  association.questionNumber,
  association.heading,
]);

const summary = {
  referenceTopics: allTopics.length,
  referenceGroups: 5,
  runtimeDisplayGroups: groups.length,
  referenceReportedAssociations,
  referenceOfficialAssociations,
  referenceMockAssociations,
  referenceProviderSampleAssociations,
  matchedAssociations: matchedAssociations.length,
  sourceBlockedAssociations: sourceBlockedAssociations.length,
  matchedLogicalCards: exactTopicsByCard.size,
  matchedQuestionTopicLinks,
  retainedLocalLogicalCards: retainedLocalCards.length,
  retainedWrittenLogicalCards,
  retainedPracticalLogicalCards,
  localPaperVariants: localPapers.length,
  localPhysicalMappings: physicalMappings,
  distinctStudentFacingQuestions,
  newlyAddedPaperVariants: supplementedPapers.length,
  newlyAddedPhysicalMappings: supplementedPapers.reduce((sum, paper) => sum + paper.q.length, 0),
  verifiedSchemeMaps,
  verifiedPaperOnlyMaps,
  preservedBaselineVariants: preservationBaseline.length,
  preservedBaselineCards,
  emptyReferenceTopics: allTopics
    .filter(topic => topic.officialQuestionHeadings.length === 0)
    .map(topic => topic.id),
};

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
    fileAwareIdentity: 'Art component code is part of every local join because practical and written booklets reuse printed question numbers.',
  },
  reviewedLocalEvidence: {
    ordinary2023: 'Official SEC LC014GLP000EV paper inspected directly; Q1–Q7 are Section A and Q8–Q19 align one-to-one with the printed Section B/C period headings.',
    canonical2023To2025: 'Existing authored Mark Bank cards provide the directly reviewed canonical syllabus node for each written question.',
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
  topics: runtimeTopics,
  partReferences,
  questionMappings,
  summary,
};

// Keep the established one-space generated formatting so the source diff is
// limited to the sixteen genuinely new paper variants.
fs.writeFileSync(TAGS_PATH, `${JSON.stringify(localPapers, null, 1)}\n`);
fs.writeFileSync(OUTPUT_PATH, `${JSON.stringify(evidence, null, 2)}\n`);
fs.writeFileSync(RUNTIME_PATH, `${JSON.stringify(runtime)}\n`);
console.log(JSON.stringify(summary, null, 2));
