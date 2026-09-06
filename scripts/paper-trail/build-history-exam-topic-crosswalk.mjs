#!/usr/bin/env node
/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 *
 * Reconcile the factual StudyClix History heading snapshot with the complete,
 * entitled SEC Later Modern paper corpus.  The official curriculum remains
 * canonical; this produces a compact level-aware practice taxonomy plus an
 * evidence-rich audit without copying commercial question content.
 */

import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const HERE = path.dirname(fileURLToPath(import.meta.url));
const ROOT = path.resolve(HERE, '../..');
const TAGS_PATH = path.join(HERE, 'topic-tags/tags/history.json');
const REFERENCE_PATH = path.join(ROOT, 'data/examTopics/history.json');
const OUTPUT_PATH = path.join(ROOT, 'data/examTopics/history-local-crosswalk.json');
const RUNTIME_PATH = path.join(ROOT, 'data/examTopics/history-runtime.json');
const BASELINE_PATH = path.join(ROOT, 'test/fixtures/historyTopicQuestionBaseline.json');
const HOSTED_ROOT = path.join(ROOT, 'public/paper-anchors');

const reference = JSON.parse(fs.readFileSync(REFERENCE_PATH, 'utf8'));
const localPapers = JSON.parse(fs.readFileSync(TAGS_PATH, 'utf8'));
const preservationBaseline = JSON.parse(fs.readFileSync(BASELINE_PATH, 'utf8'));
const LEVELS = ['higher', 'ordinary'];

const allTopics = LEVELS.flatMap(level => reference.levels[level].topics);
const topicIndex = new Map(allTopics.map((topic, index) => [topic.id, index]));
const topicSlot = topic => {
  const withinLevel = reference.levels.higher.topics.includes(topic)
    ? reference.levels.higher.topics.indexOf(topic)
    : reference.levels.ordinary.topics.indexOf(topic);
  if (withinLevel < 0) throw new Error(`Unknown History topic: ${topic.id}`);
  return {
    family: withinLevel < 6 ? 'I' : 'E',
    number: withinLevel < 6 ? withinLevel + 1 : withinLevel - 5,
  };
};
const topicForSlot = (level, family, number) => {
  const index = family === 'I' ? number - 1 : number + 5;
  const topic = reference.levels[level].topics[index];
  if (!topic) throw new Error(`Missing ${level} History ${family}${number}`);
  return topic;
};

const mainCurriculumId = (family, number) => (
  `history-${family === 'I' ? 2 : 3}-${(number - 1) * 4}`
);
const curriculumIdsForSlot = (family, number) => {
  const strand = family === 'I' ? 2 : 3;
  const start = (number - 1) * 4;
  return Array.from({ length: 4 }, (_, offset) => `history-${strand}-${start + offset}`);
};
const curriculumCrosswalk = Object.fromEntries(allTopics.map(topic => {
  const slot = topicSlot(topic);
  return [topic.id, curriculumIdsForSlot(slot.family, slot.number)];
}));
const mainNodeToSlot = new Map(
  ['I', 'E'].flatMap(family => Array.from({ length: 6 }, (_, index) => {
    const number = index + 1;
    return [mainCurriculumId(family, number), { family, number }];
  })),
);

const paperIdentity = paper => [
  paper.level,
  paper.lang,
  paper.year,
  paper.paperKey,
  paper.fileid,
].join('|');
const paperIds = localPapers.map(paperIdentity);
const duplicatePapers = paperIds.filter((identity, index) => paperIds.indexOf(identity) !== index);
if (duplicatePapers.length) {
  throw new Error(`Duplicate History topic-tag papers: ${[...new Set(duplicatePapers)].join(', ')}`);
}

const slotForLocalQuestion = question => {
  const explicit = question.n.match(/^([IE])([1-6])$/);
  if (explicit) return { family: explicit[1], number: Number(explicit[2]) };
  if (!/^(?:[1-4]|ALT)$/.test(question.n)) {
    throw new Error(`Unparseable History local card: ${question.n}`);
  }
  const canonicalIds = [question.primary, question.secondary].filter(Boolean);
  const slots = canonicalIds.map(id => mainNodeToSlot.get(id)).filter(Boolean);
  if (slots.length !== 1) {
    throw new Error(
      `History DQB Q${question.n} must carry exactly one main topic node: ${canonicalIds.join(', ')}`,
    );
  }
  return slots[0];
};

for (const paper of localPapers) {
  if (!LEVELS.includes(paper.level) || !['ev', 'iv'].includes(paper.lang)) {
    throw new Error(`Unexpected History paper identity: ${paperIdentity(paper)}`);
  }
  const numbers = paper.q.map(question => question.n);
  const expectsAlternative = paper.level === 'ordinary' && paper.year >= 2023 && paper.year <= 2026;
  const expectedCardCount = expectsAlternative ? 16 : 15;
  if (paper.q.length !== expectedCardCount || new Set(numbers).size !== expectedCardCount) {
    throw new Error(
      `${paperIdentity(paper)} must have ${expectedCardCount} unique cards; found ${paper.q.length}`,
    );
  }
  if (paper.q.filter(question => /^[1-4]$/.test(question.n)).length !== 4) {
    throw new Error(`${paperIdentity(paper)} does not preserve four DQB cards`);
  }
  if (paper.q.filter(question => /^[IE][1-6]$/.test(question.n)).length !== 11) {
    throw new Error(`${paperIdentity(paper)} does not expose eleven printed topic blocks`);
  }
  if (paper.q.filter(question => question.n === 'ALT').length !== (expectsAlternative ? 1 : 0)) {
    throw new Error(`${paperIdentity(paper)} has an invalid Alternative Part A card count`);
  }
  for (const question of paper.q) slotForLocalQuestion(question);
}

let preservedBaselineCards = 0;
for (const expected of preservationBaseline) {
  const live = localPapers.find(paper => paperIdentity(paper) === paperIdentity(expected));
  if (!live) throw new Error(`Preservation failure: missing paper ${paperIdentity(expected)}`);
  for (const number of expected.questions) {
    if (!live.q.some(question => question.n === number)) {
      throw new Error(`Preservation failure: missing ${paperIdentity(expected)} Q${number}`);
    }
    preservedBaselineCards += 1;
  }
}

const parseHeading = heading => {
  const year = Number(heading.match(/^(\d{4})/)?.[1]);
  const section = heading.match(/\bSection\s+([A-C1-4])\b/i)?.[1]?.toUpperCase();
  const question = heading.match(/\bQuestion\s+(.+)$/i)?.[1];
  if (!year || !section || !question) throw new Error(`Unparseable History heading: ${heading}`);
  return {
    year,
    section,
    question,
    sitting: /Deferred Exam Paper/i.test(heading) ? 'deferred' : 'main',
  };
};
const isDqbSection = section => section === '1' || section === 'A';
const expectedSectionFamily = section => {
  if (section === '2' || section === 'B') return 'I';
  if (section === '3' || section === 'C') return 'E';
  return null;
};
const preferredEnglishPaper = (level, year) => {
  const papers = localPapers.filter(paper => (
    paper.level === level
    && paper.lang === 'ev'
    && paper.year === year
    && paper.paperKey === 'single'
  ));
  if (papers.length > 1) throw new Error(`Ambiguous ${level} English History paper for ${year}`);
  return papers[0] ?? null;
};
const referenceNumber = parsed => `R${parsed.section}:${parsed.question}`;

const associations = LEVELS.flatMap(level => reference.levels[level].topics.flatMap(topic => {
  const slot = topicSlot(topic);
  return topic.officialQuestionHeadings.map(heading => {
    const parsed = parseHeading(heading);
    if (parsed.sitting === 'deferred') {
      return {
        topicId: topic.id,
        heading,
        level,
        year: parsed.year,
        sitting: parsed.sitting,
        resolution: 'source-blocked',
        referenceQuestionNumber: referenceNumber(parsed),
        reason: 'The entitled local SEC History corpus has no deferred-sitting booklet for this factual heading. It is retained pending acquisition and independent verification of the official paper and marking scheme; no StudyClix-hosted question image or PDF is copied.',
      };
    }

    const paper = preferredEnglishPaper(level, parsed.year);
    if (!paper) {
      return {
        topicId: topic.id,
        heading,
        level,
        year: parsed.year,
        sitting: parsed.sitting,
        resolution: 'source-blocked',
        referenceQuestionNumber: referenceNumber(parsed),
        reason: 'The entitled local SEC History corpus currently begins at 2010. This factual heading is retained pending acquisition and independent verification of the official paper and marking scheme; no StudyClix-hosted question image or PDF is copied.',
      };
    }

    const dqbQuestion = paper.q.find(question => question.n === '1');
    const dqbSlot = slotForLocalQuestion(dqbQuestion);
    const sameAsDqb = dqbSlot.family === slot.family && dqbSlot.number === slot.number;

    if (isDqbSection(parsed.section)) {
      if (!sameAsDqb) {
        throw new Error(`${heading}: reference DQB ${topic.id} conflicts with local SEC paper`);
      }
      const questionNumbers = ['1', '2', '3', '4'];
      return {
        topicId: topic.id,
        heading,
        level,
        year: parsed.year,
        sitting: parsed.sitting,
        resolution: 'matched',
        target: {
          level,
          lang: 'ev',
          paperKey: paper.paperKey,
          fileid: paper.fileid,
          questionNumbers,
        },
      };
    }

    if (parsed.question.toLowerCase() === 'alternative') {
      const isPotentialAlternative = (
        level === 'ordinary'
        && parsed.year >= 2023
        && parsed.year <= 2026
      );
      if (!isPotentialAlternative || !paper.q.some(question => question.n === 'ALT')) {
        throw new Error(`${heading}: invalid or unavailable Alternative Part A association`);
      }
      if (!sameAsDqb) {
        const known2024AlternativeAnomaly = (
          parsed.year === 2024
          && slot.family === 'I'
          && slot.number === 2
          && dqbSlot.family === 'E'
          && dqbSlot.number === 3
        );
        if (!known2024AlternativeAnomaly) {
          throw new Error(`${heading}: Alternative Part A topic conflicts with the local SEC paper`);
        }
        return {
          topicId: topic.id,
          heading,
          level,
          year: parsed.year,
          sitting: parsed.sitting,
          resolution: 'reference-anomaly',
          referenceQuestionNumber: referenceNumber(parsed),
          reason: 'StudyClix associates the 2024 Alternative Part A heading with Ireland Topic 2. The official SEC paper makes Europe Topic 3 the documents-based topic for 2024, and its alternative Part A passage concerns the Jarrow March within that topic. NextStepUni preserves the factual reference association in this audit while mapping the official card to Europe Topic 3.',
        };
      }
      return {
        topicId: topic.id,
        heading,
        level,
        year: parsed.year,
        sitting: parsed.sitting,
        resolution: 'matched',
        target: {
          level,
          lang: 'ev',
          paperKey: paper.paperKey,
          fileid: paper.fileid,
          questionNumbers: ['ALT'],
        },
      };
    }

    if (sameAsDqb) {
      const known2010OrdinaryAnomaly = (
        level === 'ordinary'
        && parsed.year === 2010
        && slot.family === 'I'
        && slot.number === 5
        && parsed.section === '3'
      );
      if (!known2010OrdinaryAnomaly) {
        throw new Error(`${heading}: DQB topic unexpectedly appears as a second topic block`);
      }
      return {
        topicId: topic.id,
        heading,
        level,
        year: parsed.year,
        sitting: parsed.sitting,
        resolution: 'reference-anomaly',
        referenceQuestionNumber: referenceNumber(parsed),
        reason: 'The 2010 Ordinary English SEC paper misprints its Ireland Topic 6 block as Topic 5. StudyClix associates that second heading with Topic 5 and labels it Section 3, but the official block title, content and front-page instructions identify Ireland Topic 6. NextStepUni retains the factual reference association in this audit while mapping the local card to the correct official curriculum topic.',
      };
    }

    const headingFamily = expectedSectionFamily(parsed.section);
    const known2010EuropeSectionTypo = (
      level === 'ordinary'
      && parsed.year === 2010
      && slot.family === 'E'
      && slot.number === 5
      && parsed.section === '4'
    );
    if (headingFamily !== slot.family && !known2010EuropeSectionTypo) {
      throw new Error(`${heading}: section family conflicts with ${topic.id}`);
    }

    const localNumber = `${slot.family}${slot.number}`;
    if (!paper.q.some(question => question.n === localNumber)) {
      throw new Error(`${heading}: local SEC paper is missing ${localNumber}`);
    }
    return {
      topicId: topic.id,
      heading,
      level,
      year: parsed.year,
      sitting: parsed.sitting,
      resolution: 'matched',
      ...(known2010EuropeSectionTypo
        ? { correction: 'The factual StudyClix heading says Section 4; the official SEC block is in Section 3.' }
        : {}),
      target: {
        level,
        lang: 'ev',
        paperKey: paper.paperKey,
        fileid: paper.fileid,
        questionNumbers: [localNumber],
      },
    };
  });
}));

const matched = associations.filter(association => association.resolution === 'matched');
const sourceBlocked = associations.filter(association => association.resolution === 'source-blocked');
const referenceAnomalies = associations.filter(association => association.resolution === 'reference-anomaly');
const referenceTopicsByLocalQuestion = new Map();
for (const association of matched) {
  for (const number of association.target.questionNumbers) {
    const key = [association.level, association.year, association.target.paperKey, number].join('|');
    const topics = referenceTopicsByLocalQuestion.get(key) ?? [];
    if (!topics.includes(association.topicId)) topics.push(association.topicId);
    referenceTopicsByLocalQuestion.set(key, topics);
  }
}

const localQuestionMappings = localPapers.flatMap(paper => paper.q.map(question => {
  const key = [paper.level, paper.year, paper.paperKey, question.n].join('|');
  const slot = slotForLocalQuestion(question);
  const fallbackTopicId = topicForSlot(paper.level, slot.family, slot.number).id;
  const referenceTopicIds = referenceTopicsByLocalQuestion.get(key);
  if (referenceTopicIds && !referenceTopicIds.includes(fallbackTopicId)) {
    throw new Error(`${key}: reference/local topic disagreement`);
  }
  return {
    level: paper.level,
    lang: paper.lang,
    year: paper.year,
    fileid: paper.fileid,
    paperKey: paper.paperKey,
    n: question.n,
    topicIds: referenceTopicIds ?? [fallbackTopicId],
    provenance: referenceTopicIds ? 'reference' : 'retained-local',
  };
}));

const distinctLocalQuestions = new Set(localQuestionMappings.map(mapping => (
  `${mapping.level}|${mapping.year}|${mapping.paperKey}|${mapping.n}`
))).size;
const referenceMappedPrintedQuestions = new Set(localQuestionMappings
  .filter(mapping => mapping.provenance === 'reference')
  .map(mapping => `${mapping.level}|${mapping.year}|${mapping.paperKey}|${mapping.n}`)).size;

for (const paper of localPapers) {
  const hostedPath = path.join(HOSTED_ROOT, String(paper.year), `${paper.fileid}.json`);
  if (!fs.existsSync(hostedPath)) throw new Error(`Missing History hosted anchors: ${hostedPath}`);
  const hosted = JSON.parse(fs.readFileSync(hostedPath, 'utf8'));
  const expectedNumbers = paper.q
    .filter(question => /^(?:[IE][1-6]|ALT)$/.test(question.n))
    .map(question => question.n);
  if (hosted.paperFileid !== paper.fileid || hosted.paperOnly !== 1) {
    throw new Error(`${hostedPath}: invalid paper-only identity`);
  }
  if (
    hosted.q.length !== expectedNumbers.length
    || expectedNumbers.some(number => !hosted.q.some(q => q.n === number))
  ) {
    throw new Error(`${hostedPath}: incomplete History topic anchors`);
  }
}

const output = {
  schemaVersion: 1,
  subjectId: reference.subjectId,
  capturedAt: reference.capturedAt,
  policy: {
    matchedSource: 'Entitled local SEC corpus only.',
    levelResolution: 'Higher and Ordinary reference headings are joined only to the same level; English and Irish official editions share the same printed topic classification.',
    granularity: 'The four shipped DQB subquestion cards remain intact. Each of the eleven independently selectable Ireland/Europe topic blocks is added as one stable section/topic card, together with the official Ordinary-level Alternative Part A task printed in 2023-2026.',
    correctionPolicy: 'Official SEC topic titles, content and instructions outrank a commercial browse heading. The verified 2010 Ordinary paper typo, its corresponding StudyClix association error, and the reference site\'s 2024 Alternative Part A misclassification are documented rather than propagated.',
    excludedContent: 'No commercial mock question, solution, note, question text, StudyClix image or StudyClix-hosted PDF is copied.',
  },
  summary: {
    referenceHeadingAssociations: associations.length,
    matchedHeadingAssociations: matched.length,
    sourceBlockedHeadingAssociations: sourceBlocked.length,
    referenceAnomalyAssociations: referenceAnomalies.length,
    matchedLocalCardLinks: matched.reduce(
      (count, association) => count + association.target.questionNumbers.length,
      0,
    ),
    referenceMappedPrintedQuestions,
    localPaperVariants: localPapers.length,
    localQuestionMappings: localQuestionMappings.length,
    distinctLocalQuestions,
    referenceMappedLocalQuestions: localQuestionMappings
      .filter(mapping => mapping.provenance === 'reference').length,
    retainedLocalQuestions: localQuestionMappings
      .filter(mapping => mapping.provenance === 'retained-local').length,
    preservedBaselinePaperVariants: preservationBaseline.length,
    preservedBaselineCards,
    addedLocalPaperVariants: localPapers.length - preservationBaseline.length,
    addedLocalCards: localQuestionMappings.length - preservedBaselineCards,
    hostedPaperAnchorMaps: localPapers.length,
  },
  curriculumCrosswalk,
  associations,
  localQuestionMappings,
};

fs.writeFileSync(OUTPUT_PATH, `${JSON.stringify(output, null, 2)}\n`);

const runtime = {
  v: 1,
  subjectId: reference.subjectId,
  capturedAt: reference.capturedAt,
  referenceProvider: reference.reference.provider,
  groups: LEVELS.map(level => [
    level === 'higher' ? 'h' : 'o',
    reference.levels[level].label,
    reference.levels[level].topics.map(topic => topicIndex.get(topic.id)),
  ]),
  // [id, label, source path, mock count, curriculum ids, h/o]
  topics: allTopics.map(topic => [
    topic.id,
    topic.label,
    topic.sourcePath,
    topic.mockQuestionCount,
    curriculumCrosswalk[topic.id],
    topic.id.includes('-higher-') ? 'h' : 'o',
  ]),
  // [topic index, year, main/deferred, local-or-reference number, heading]
  partReferences: associations.flatMap(association => {
    const numbers = association.resolution === 'matched'
      ? association.target.questionNumbers
      : [association.referenceQuestionNumber];
    return numbers.map(number => [
      topicIndex.get(association.topicId),
      association.year,
      association.sitting === 'deferred' ? 'd' : 'm',
      number,
      association.heading,
    ]);
  }),
  // h/o = level; e/i = English/Irish; all mappings are main/single.
  questionMappings: localQuestionMappings.map(mapping => [
    mapping.level === 'higher' ? 'h' : 'o',
    mapping.lang === 'ev' ? 'e' : 'i',
    mapping.year,
    mapping.n,
    topicIndex.get(mapping.topicIds[0]),
  ]),
};

for (const [runtimeTopicIndex] of runtime.partReferences) {
  if (!Number.isInteger(runtimeTopicIndex)) throw new Error('Unresolved History part-reference topic index');
}
for (const mapping of runtime.questionMappings) {
  if (!Number.isInteger(mapping[4])) throw new Error('Unresolved History local-mapping topic index');
}

fs.writeFileSync(RUNTIME_PATH, `${JSON.stringify(runtime)}\n`);
console.log(JSON.stringify(output.summary, null, 2));
