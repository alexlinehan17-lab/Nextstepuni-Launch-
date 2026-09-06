#!/usr/bin/env node
/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 *
 * Reconcile the factual StudyClix Physics & Chemistry heading snapshot with
 * NextStepUni's stable, entitled SEC paper cards. StudyClix currently exposes
 * one shared menu but its question cards are from the Higher Level paper. The
 * reference associations are therefore joined only to the matching Higher
 * paper and are propagated across its English/Irish editions. Ordinary Level,
 * reference omissions and the newer 2026 papers retain explicit local
 * classifications through the canonical curriculum bridge.
 *
 * This script never reads or stores StudyClix question text, solutions,
 * commercial mock material, images or PDFs. It consumes only the committed
 * factual headings in data/examTopics/physics-and-chemistry.json.
 */

import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const HERE = path.dirname(fileURLToPath(import.meta.url));
const ROOT = path.resolve(HERE, '../..');
const TAGS_PATH = path.join(HERE, 'topic-tags/tags/physics-and-chemistry.json');
const REFERENCE_PATH = path.join(ROOT, 'data/examTopics/physics-and-chemistry.json');
const OUTPUT_PATH = path.join(ROOT, 'data/examTopics/physics-and-chemistry-local-crosswalk.json');
const RUNTIME_PATH = path.join(ROOT, 'data/examTopics/physics-and-chemistry-runtime.json');
const BASELINE_PATH = path.join(ROOT, 'test/fixtures/physicsAndChemistryTopicQuestionBaseline.json');

const reference = JSON.parse(fs.readFileSync(REFERENCE_PATH, 'utf8'));
const localPapers = JSON.parse(fs.readFileSync(TAGS_PATH, 'utf8'));
const preservationBaseline = JSON.parse(fs.readFileSync(BASELINE_PATH, 'utf8'));

const topic = suffix => `physics-and-chemistry-common-${suffix}`;

/**
 * Student-facing exam buckets remain separate from official syllabus nodes.
 * This many-to-many bridge is used by Syllabus X-Ray and is emitted with the
 * generated artifact so runtime code and tests consume one audited mapping.
 */
const CURRICULUM_CROSSWALK = {
  [topic('c-acids-and-bases')]: ['physics-and-chemistry-8-2'],
  [topic('c-atomic-theory')]: ['physics-and-chemistry-8-0'],
  [topic('c-bonding-and-molecular-theory')]: ['physics-and-chemistry-8-1'],
  [topic('c-chemical-equations')]: [
    'physics-and-chemistry-8-2',
    'physics-and-chemistry-8-3',
    'physics-and-chemistry-8-4',
    'physics-and-chemistry-8-5',
  ],
  [topic('c-chlorides')]: ['physics-and-chemistry-8-1', 'physics-and-chemistry-8-5'],
  [topic('c-electrochemistry-and-the-activity-series')]: [
    'physics-and-chemistry-8-3',
    'physics-and-chemistry-8-5',
  ],
  [topic('c-hydrides')]: ['physics-and-chemistry-8-1', 'physics-and-chemistry-8-5'],
  [topic('c-organic-chemistry')]: ['physics-and-chemistry-8-4'],
  [topic('c-oxidation-and-reduction')]: ['physics-and-chemistry-8-3'],
  [topic('c-oxides')]: [
    'physics-and-chemistry-8-1',
    'physics-and-chemistry-8-3',
    'physics-and-chemistry-8-5',
  ],
  [topic('c-the-elements')]: [
    'physics-and-chemistry-8-0',
    'physics-and-chemistry-8-1',
    'physics-and-chemistry-8-5',
  ],
  [topic('c-thermochemistry')]: ['physics-and-chemistry-8-5'],
  [topic('p-acceleration')]: ['physics-and-chemistry-0-0', 'physics-and-chemistry-0-2'],
  [topic('p-capacitor-and-capacitance')]: ['physics-and-chemistry-6-7'],
  [topic('p-conductors-insulators-and-electric-fields')]: [
    'physics-and-chemistry-6-0',
    'physics-and-chemistry-6-1',
    'physics-and-chemistry-6-2',
    'physics-and-chemistry-6-3',
    'physics-and-chemistry-6-4',
    'physics-and-chemistry-6-5',
    'physics-and-chemistry-6-6',
    'physics-and-chemistry-6-10',
  ],
  [topic('p-current-electricity')]: [
    'physics-and-chemistry-6-8',
    'physics-and-chemistry-6-9',
    'physics-and-chemistry-6-11',
    'physics-and-chemistry-6-12',
    'physics-and-chemistry-6-13',
    'physics-and-chemistry-6-14',
    'physics-and-chemistry-6-15',
  ],
  [topic('p-electromagnetic-induction-ac-dc-transformers')]: [
    'physics-and-chemistry-6-16',
    'physics-and-chemistry-6-17',
    'physics-and-chemistry-6-18',
  ],
  [topic('p-force-mass-momentum')]: [
    'physics-and-chemistry-0-2',
    'physics-and-chemistry-0-3',
  ],
  [topic('p-gravitation')]: ['physics-and-chemistry-0-4'],
  [topic('p-heat')]: [
    'physics-and-chemistry-1-0',
    'physics-and-chemistry-1-1',
    'physics-and-chemistry-1-2',
    'physics-and-chemistry-1-3',
    'physics-and-chemistry-2-0',
    'physics-and-chemistry-2-1',
    'physics-and-chemistry-2-2',
    'physics-and-chemistry-2-3',
    'physics-and-chemistry-2-4',
    'physics-and-chemistry-2-5',
  ],
  [topic('p-light-waves-and-particles')]: [
    'physics-and-chemistry-3-0',
    'physics-and-chemistry-3-1',
    'physics-and-chemistry-5-5',
    'physics-and-chemistry-5-6',
    'physics-and-chemistry-5-7',
    'physics-and-chemistry-5-8',
    'physics-and-chemistry-5-9',
    'physics-and-chemistry-5-10',
    'physics-and-chemistry-7-1',
    'physics-and-chemistry-7-2',
    'physics-and-chemistry-7-3',
  ],
  [topic('p-pressure-moments-gravity')]: [
    'physics-and-chemistry-0-4',
    'physics-and-chemistry-0-5',
    'physics-and-chemistry-0-6',
    'physics-and-chemistry-0-7',
  ],
  [topic('p-radioactivity')]: [
    'physics-and-chemistry-7-4',
    'physics-and-chemistry-7-5',
    'physics-and-chemistry-7-6',
    'physics-and-chemistry-7-7',
    'physics-and-chemistry-7-8',
  ],
  [topic('p-reflection-and-mirrors')]: ['physics-and-chemistry-5-0', 'physics-and-chemistry-5-1'],
  [topic('p-refraction-and-lenses')]: [
    'physics-and-chemistry-5-2',
    'physics-and-chemistry-5-3',
    'physics-and-chemistry-5-4',
  ],
  [topic('p-speed-displacement-velocity')]: ['physics-and-chemistry-0-0'],
  [topic('p-vectors-and-scalars')]: ['physics-and-chemistry-0-1'],
  [topic('p-work-energy-power')]: [
    'physics-and-chemistry-0-8',
    'physics-and-chemistry-0-9',
    'physics-and-chemistry-0-10',
  ],
};

// Coarse legacy tags do not always distinguish neighbouring browse buckets.
// These conservative fallbacks retain the verified meaning without claiming a
// part-level precision that the local tag did not record.
const FALLBACK_BY_CANONICAL_ID = {
  'physics-and-chemistry-0-0': [topic('p-speed-displacement-velocity')],
  'physics-and-chemistry-0-1': [topic('p-vectors-and-scalars')],
  'physics-and-chemistry-0-2': [topic('p-force-mass-momentum'), topic('p-acceleration')],
  'physics-and-chemistry-0-3': [topic('p-force-mass-momentum')],
  'physics-and-chemistry-0-4': [topic('p-pressure-moments-gravity'), topic('p-gravitation')],
  'physics-and-chemistry-0-5': [topic('p-pressure-moments-gravity')],
  'physics-and-chemistry-0-6': [topic('p-pressure-moments-gravity')],
  'physics-and-chemistry-0-7': [topic('p-pressure-moments-gravity')],
  'physics-and-chemistry-0-8': [topic('p-work-energy-power')],
  'physics-and-chemistry-0-9': [topic('p-work-energy-power')],
  'physics-and-chemistry-0-10': [topic('p-work-energy-power')],
  'physics-and-chemistry-0-11': [topic('p-force-mass-momentum')],
  'physics-and-chemistry-0-12': [topic('p-force-mass-momentum')],
  'physics-and-chemistry-1-0': [topic('p-heat')],
  'physics-and-chemistry-1-1': [topic('p-heat')],
  'physics-and-chemistry-1-2': [topic('p-heat')],
  'physics-and-chemistry-1-3': [topic('p-heat')],
  'physics-and-chemistry-2-0': [topic('p-heat')],
  'physics-and-chemistry-2-1': [topic('p-heat')],
  'physics-and-chemistry-2-2': [topic('p-heat')],
  'physics-and-chemistry-2-3': [topic('p-heat')],
  'physics-and-chemistry-2-4': [topic('p-heat')],
  'physics-and-chemistry-2-5': [topic('p-heat')],
  'physics-and-chemistry-3-0': [topic('p-light-waves-and-particles')],
  'physics-and-chemistry-3-1': [topic('p-light-waves-and-particles')],
  'physics-and-chemistry-4-0': [topic('p-light-waves-and-particles')],
  'physics-and-chemistry-4-1': [topic('p-light-waves-and-particles')],
  'physics-and-chemistry-4-2': [topic('p-light-waves-and-particles')],
  'physics-and-chemistry-4-3': [topic('p-light-waves-and-particles')],
  'physics-and-chemistry-4-4': [topic('p-light-waves-and-particles')],
  'physics-and-chemistry-5-0': [topic('p-reflection-and-mirrors')],
  'physics-and-chemistry-5-1': [topic('p-reflection-and-mirrors')],
  'physics-and-chemistry-5-2': [topic('p-refraction-and-lenses')],
  'physics-and-chemistry-5-3': [topic('p-refraction-and-lenses')],
  'physics-and-chemistry-5-4': [topic('p-refraction-and-lenses')],
  'physics-and-chemistry-5-5': [topic('p-light-waves-and-particles')],
  'physics-and-chemistry-5-6': [topic('p-light-waves-and-particles')],
  'physics-and-chemistry-5-7': [topic('p-light-waves-and-particles')],
  'physics-and-chemistry-5-8': [topic('p-light-waves-and-particles')],
  'physics-and-chemistry-5-9': [topic('p-light-waves-and-particles')],
  'physics-and-chemistry-5-10': [topic('p-light-waves-and-particles')],
  'physics-and-chemistry-6-0': [topic('p-conductors-insulators-and-electric-fields')],
  'physics-and-chemistry-6-1': [topic('p-conductors-insulators-and-electric-fields')],
  'physics-and-chemistry-6-2': [topic('p-conductors-insulators-and-electric-fields')],
  'physics-and-chemistry-6-3': [topic('p-conductors-insulators-and-electric-fields')],
  'physics-and-chemistry-6-4': [topic('p-conductors-insulators-and-electric-fields')],
  'physics-and-chemistry-6-5': [topic('p-conductors-insulators-and-electric-fields')],
  'physics-and-chemistry-6-6': [topic('p-conductors-insulators-and-electric-fields')],
  'physics-and-chemistry-6-7': [topic('p-capacitor-and-capacitance')],
  'physics-and-chemistry-6-8': [topic('p-current-electricity')],
  'physics-and-chemistry-6-9': [topic('p-current-electricity')],
  'physics-and-chemistry-6-10': [topic('p-conductors-insulators-and-electric-fields')],
  'physics-and-chemistry-6-11': [topic('p-current-electricity')],
  'physics-and-chemistry-6-12': [topic('p-current-electricity')],
  'physics-and-chemistry-6-13': [topic('p-current-electricity')],
  'physics-and-chemistry-6-14': [topic('p-current-electricity')],
  'physics-and-chemistry-6-15': [topic('p-current-electricity')],
  'physics-and-chemistry-6-16': [topic('p-electromagnetic-induction-ac-dc-transformers')],
  'physics-and-chemistry-6-17': [topic('p-electromagnetic-induction-ac-dc-transformers')],
  'physics-and-chemistry-6-18': [topic('p-electromagnetic-induction-ac-dc-transformers')],
  'physics-and-chemistry-7-0': [topic('p-conductors-insulators-and-electric-fields')],
  'physics-and-chemistry-7-1': [topic('p-light-waves-and-particles')],
  'physics-and-chemistry-7-2': [topic('p-light-waves-and-particles')],
  'physics-and-chemistry-7-3': [topic('p-light-waves-and-particles')],
  'physics-and-chemistry-7-4': [topic('p-radioactivity')],
  'physics-and-chemistry-7-5': [topic('p-radioactivity')],
  'physics-and-chemistry-7-6': [topic('p-radioactivity')],
  'physics-and-chemistry-7-7': [topic('p-radioactivity')],
  'physics-and-chemistry-7-8': [topic('p-radioactivity')],
  'physics-and-chemistry-7-9': [topic('p-radioactivity')],
  'physics-and-chemistry-8-0': [topic('c-atomic-theory'), topic('c-the-elements')],
  'physics-and-chemistry-8-1': [topic('c-bonding-and-molecular-theory')],
  'physics-and-chemistry-8-2': [topic('c-acids-and-bases')],
  'physics-and-chemistry-8-3': [
    topic('c-oxidation-and-reduction'),
    topic('c-electrochemistry-and-the-activity-series'),
  ],
  'physics-and-chemistry-8-4': [topic('c-organic-chemistry')],
  'physics-and-chemistry-8-5': [
    topic('c-chemical-equations'),
    topic('c-the-elements'),
    topic('c-thermochemistry'),
  ],
};

/** Part-aware classifications taken directly from the local 2026 SEC papers. */
const OFFICIAL_2026_TOPIC_IDS = {
  higher: {
    '1': [
      topic('p-vectors-and-scalars'), topic('p-speed-displacement-velocity'),
      topic('p-force-mass-momentum'), topic('p-work-energy-power'),
      topic('p-reflection-and-mirrors'), topic('p-refraction-and-lenses'),
      topic('p-light-waves-and-particles'), topic('p-heat'),
      topic('p-current-electricity'), topic('p-electromagnetic-induction-ac-dc-transformers'),
      topic('p-radioactivity'),
    ],
    '2': [
      topic('p-gravitation'), topic('p-pressure-moments-gravity'),
      topic('p-acceleration'), topic('p-work-energy-power'),
    ],
    '3': [topic('p-refraction-and-lenses')],
    '4': [topic('p-heat')],
    '5': [topic('p-current-electricity'), topic('p-heat')],
    '6': [
      topic('p-conductors-insulators-and-electric-fields'), topic('p-radioactivity'),
      topic('p-capacitor-and-capacitance'), topic('p-light-waves-and-particles'),
    ],
    '7': [
      topic('c-acids-and-bases'), topic('c-atomic-theory'),
      topic('c-bonding-and-molecular-theory'), topic('c-chemical-equations'),
      topic('c-chlorides'), topic('c-electrochemistry-and-the-activity-series'),
      topic('c-hydrides'), topic('c-organic-chemistry'),
      topic('c-oxidation-and-reduction'), topic('c-oxides'),
      topic('c-the-elements'), topic('c-thermochemistry'),
    ],
    '8': [topic('c-atomic-theory'), topic('c-the-elements')],
    '9': [topic('c-acids-and-bases'), topic('c-chemical-equations')],
    '10': [
      topic('c-electrochemistry-and-the-activity-series'),
      topic('c-oxidation-and-reduction'), topic('c-chemical-equations'),
    ],
    '11': [topic('c-organic-chemistry'), topic('c-chemical-equations')],
    '12': [
      topic('c-atomic-theory'), topic('c-chemical-equations'),
      topic('c-acids-and-bases'), topic('c-thermochemistry'),
    ],
  },
  ordinary: {
    '1': [
      topic('p-work-energy-power'), topic('p-pressure-moments-gravity'),
      topic('p-vectors-and-scalars'), topic('p-acceleration'), topic('p-heat'),
      topic('p-light-waves-and-particles'), topic('p-reflection-and-mirrors'),
      topic('p-conductors-insulators-and-electric-fields'), topic('p-current-electricity'),
      topic('p-radioactivity'),
    ],
    '2': [topic('p-speed-displacement-velocity'), topic('p-acceleration')],
    '3': [topic('p-refraction-and-lenses')],
    '4': [topic('p-heat')],
    '5': [
      topic('p-current-electricity'), topic('p-conductors-insulators-and-electric-fields'),
      topic('p-capacitor-and-capacitance'),
    ],
    '6': [
      topic('p-force-mass-momentum'), topic('p-electromagnetic-induction-ac-dc-transformers'),
      topic('p-heat'), topic('p-radioactivity'),
    ],
    '7': [
      topic('c-acids-and-bases'), topic('c-atomic-theory'),
      topic('c-bonding-and-molecular-theory'), topic('c-chemical-equations'),
      topic('c-electrochemistry-and-the-activity-series'), topic('c-organic-chemistry'),
      topic('c-oxidation-and-reduction'), topic('c-the-elements'),
    ],
    '8': [
      topic('c-atomic-theory'), topic('c-bonding-and-molecular-theory'),
      topic('c-chlorides'), topic('c-the-elements'),
    ],
    '9': [
      topic('c-oxidation-and-reduction'), topic('c-acids-and-bases'),
      topic('c-chemical-equations'), topic('c-oxides'),
    ],
    '10': [topic('c-acids-and-bases'), topic('c-chemical-equations')],
    '11': [
      topic('c-organic-chemistry'), topic('c-thermochemistry'),
      topic('c-chemical-equations'), topic('c-oxides'),
    ],
    '12': [
      topic('c-oxides'), topic('c-the-elements'),
      topic('c-chemical-equations'), topic('c-bonding-and-molecular-theory'),
    ],
  },
};

const paperIdentity = paper => [
  paper.level,
  paper.lang,
  paper.year,
  paper.paperKey,
  paper.fileid,
].join('|');

const paperIdentities = localPapers.map(paperIdentity);
const duplicatePapers = paperIdentities.filter((identity, index) => paperIdentities.indexOf(identity) !== index);
if (duplicatePapers.length) {
  throw new Error(`Duplicate Physics & Chemistry topic-tag papers: ${[...new Set(duplicatePapers)].join(', ')}`);
}
for (const paper of localPapers) {
  const numbers = paper.q.map(question => question.n);
  const duplicateNumbers = numbers.filter((number, index) => numbers.indexOf(number) !== index);
  if (duplicateNumbers.length) {
    throw new Error(`${paperIdentity(paper)} has duplicate cards: ${[...new Set(duplicateNumbers)].join(', ')}`);
  }
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
  const question = heading.match(/\bQuestion\s+(\d+)/i);
  if (!year || !question) throw new Error(`Unparseable Physics & Chemistry heading: ${heading}`);
  return { year, n: question[1] };
};

const preferredHigherEnglishPaper = year => {
  const papers = localPapers.filter(paper => (
    paper.year === year
    && paper.level === 'higher'
    && paper.lang === 'ev'
    && paper.paperKey === 'single'
  ));
  if (papers.length !== 1) return null;
  return papers[0];
};

const resolveHeading = (topicId, heading) => {
  const { year, n } = parseHeading(heading);
  const paper = preferredHigherEnglishPaper(year);
  if (!paper) {
    return {
      topicId,
      heading,
      year,
      resolution: 'source-blocked',
      reason: 'The entitled local SEC Physics & Chemistry corpus currently begins at 2010. This factual heading is retained pending acquisition and independent verification of the official SEC paper and marking scheme; no StudyClix-hosted question image or PDF is copied.',
    };
  }
  if (!paper.q.some(question => question.n === n)) {
    throw new Error(`${paperIdentity(paper)} has no card for ${heading}`);
  }
  return {
    topicId,
    heading,
    year,
    resolution: 'matched',
    target: {
      level: 'higher',
      lang: 'ev',
      paperKey: paper.paperKey,
      fileid: paper.fileid,
      questionNumbers: [n],
    },
  };
};

const associations = reference.levels.common.topics.flatMap(referenceTopic => (
  referenceTopic.officialQuestionHeadings.map(heading => resolveHeading(referenceTopic.id, heading))
));
const matched = associations.filter(association => association.resolution === 'matched');
const sourceBlocked = associations.filter(association => association.resolution === 'source-blocked');

// StudyClix's cards are Higher Level, but English and Irish are translations
// of the same printed assessment. Join by printed identity so both editions
// receive the same factual reference classification.
const referenceTopicsByHigherQuestion = new Map();
for (const association of matched) {
  const n = association.target.questionNumbers[0];
  const key = `${association.year}|${association.target.paperKey}|${n}`;
  const ids = referenceTopicsByHigherQuestion.get(key) ?? [];
  if (!ids.includes(association.topicId)) ids.push(association.topicId);
  referenceTopicsByHigherQuestion.set(key, ids);
}

const topicOrder = new Map(reference.levels.common.topics.map((item, index) => [item.id, index]));
const orderedUniqueTopics = ids => [...new Set(ids)].sort((a, b) => topicOrder.get(a) - topicOrder.get(b));

const fallbackTopicIds = (paper, question) => {
  const ids = [question.primary, question.secondary]
    .filter(Boolean)
    .flatMap(canonicalId => FALLBACK_BY_CANONICAL_ID[canonicalId] ?? []);
  const topicIds = orderedUniqueTopics(ids);
  if (!topicIds.length) {
    throw new Error(`${paperIdentity(paper)} Q${question.n} has no exam-topic fallback`);
  }
  return topicIds;
};

const localQuestionMappings = localPapers.flatMap(paper => paper.q.map(question => {
  const referenceTopicIds = paper.level === 'higher' && paper.year <= 2025
    ? referenceTopicsByHigherQuestion.get(`${paper.year}|${paper.paperKey}|${question.n}`)
    : null;
  const official2026TopicIds = paper.year === 2026
    ? OFFICIAL_2026_TOPIC_IDS[paper.level]?.[question.n]
    : null;
  const topicIds = referenceTopicIds
    ?? (official2026TopicIds ? orderedUniqueTopics(official2026TopicIds) : fallbackTopicIds(paper, question));
  return {
    level: paper.level,
    lang: paper.lang,
    year: paper.year,
    fileid: paper.fileid,
    paperKey: paper.paperKey,
    n: question.n,
    topicIds,
    provenance: referenceTopicIds
      ? 'reference'
      : official2026TopicIds
        ? 'official-local-2026'
        : 'retained-local',
  };
}));

const distinctLocalQuestions = new Set(localQuestionMappings.map(mapping => (
  `${mapping.level}|${mapping.year}|${mapping.paperKey}|${mapping.n}`
))).size;
const referenceMappedPrintedQuestions = new Set(localQuestionMappings
  .filter(mapping => mapping.provenance === 'reference')
  .map(mapping => `${mapping.level}|${mapping.year}|${mapping.paperKey}|${mapping.n}`)).size;

const output = {
  schemaVersion: 1,
  subjectId: reference.subjectId,
  capturedAt: reference.capturedAt,
  policy: {
    matchedSource: 'Entitled local SEC corpus only.',
    levelResolution: 'StudyClix Phys-Chem question cards were verified as Higher Level. Exact reference associations are joined only to Higher Level printed questions and shared across their English and Irish editions.',
    excludedContent: 'No commercial mock question, solution, note, question text, StudyClix image or StudyClix-hosted PDF is copied.',
  },
  summary: {
    referenceHeadingAssociations: associations.length,
    matchedHeadingAssociations: matched.length,
    sourceBlockedHeadingAssociations: sourceBlocked.length,
    matchedLocalCardLinks: matched.reduce((count, association) => count + association.target.questionNumbers.length, 0),
    referenceMappedPrintedQuestions,
    localPaperVariants: localPapers.length,
    localQuestionMappings: localQuestionMappings.length,
    distinctLocalQuestions,
    referenceMappedLocalQuestions: localQuestionMappings.filter(mapping => mapping.provenance === 'reference').length,
    retainedLocalQuestions: localQuestionMappings.filter(mapping => mapping.provenance === 'retained-local').length,
    official2026LocalQuestions: localQuestionMappings.filter(mapping => mapping.provenance === 'official-local-2026').length,
    preservedBaselinePaperVariants: preservationBaseline.length,
    preservedBaselineCards,
    addedLocalPaperVariants: localPapers.length - preservationBaseline.length,
    addedLocalCards: localQuestionMappings.length - preservedBaselineCards,
  },
  curriculumCrosswalk: CURRICULUM_CROSSWALK,
  associations,
  localQuestionMappings,
};

fs.writeFileSync(OUTPUT_PATH, `${JSON.stringify(output, null, 2)}\n`);

// The complete audit artifact above deliberately repeats human-readable
// evidence. Keep that evidence out of the production bundle by emitting a
// tuple-based runtime projection containing only what Topic Atlas and the
// cross-surface joins need.
const runtimeTopicIndex = new Map(
  reference.levels.common.topics.map((item, index) => [item.id, index]),
);
const runtime = {
  v: 1,
  subjectId: reference.subjectId,
  capturedAt: reference.capturedAt,
  referenceProvider: reference.reference.provider,
  groupLabel: reference.levels.common.label,
  topics: reference.levels.common.topics.map(item => [
    item.id,
    item.label,
    item.sourcePath,
    item.mockQuestionCount,
    CURRICULUM_CROSSWALK[item.id],
  ]),
  // All reference cards were verified as Higher, main-sitting, single-paper
  // identities, so those repeated fields are encoded by the schema itself.
  partReferences: associations.map(association => [
    runtimeTopicIndex.get(association.topicId),
    association.year,
    association.resolution === 'matched'
      ? association.target.questionNumbers[0]
      : parseHeading(association.heading).n,
    association.heading,
  ]),
  // h/o = Higher/Ordinary; e/i = English/Irish. All are main/single.
  questionMappings: localQuestionMappings.map(mapping => [
    mapping.level === 'higher' ? 'h' : 'o',
    mapping.lang === 'ev' ? 'e' : 'i',
    mapping.year,
    mapping.n,
    mapping.topicIds.map(topicId => runtimeTopicIndex.get(topicId)),
  ]),
};
fs.writeFileSync(RUNTIME_PATH, `${JSON.stringify(runtime)}\n`);
console.log(JSON.stringify(output.summary, null, 2));
