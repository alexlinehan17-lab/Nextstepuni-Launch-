#!/usr/bin/env node
/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 *
 * Reconcile the factual StudyClix Japanese heading snapshot with the exact
 * cards in NextStepUni's entitled SEC corpus. The reference site groups whole
 * sections while Paper Trail intentionally keeps smaller, stable cards, so a
 * single heading can resolve to several local card IDs.
 *
 * This script never reads or stores StudyClix question text, solutions or
 * commercial mock material. It consumes only the committed factual headings
 * in data/examTopics/japanese.json and emits local identities. It also derives
 * paper-only hosted anchor maps from the audited local sidecars so Topic Atlas
 * can render the official SEC question crops before the richer answer maps are
 * uploaded to Storage. Those hosted maps deliberately contain no scheme
 * filename or answer-region coordinates.
 */

import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const HERE = path.dirname(fileURLToPath(import.meta.url));
const ROOT = path.resolve(HERE, '../..');
const TAGS_DIR = path.join(HERE, 'topic-tags/tags');
const ANSWERS_DIR = path.join(HERE, 'answers');
const REFERENCE_PATH = path.join(ROOT, 'data/examTopics/japanese.json');
const OUTPUT_PATH = path.join(ROOT, 'data/examTopics/japanese-local-crosswalk.json');
const RUNTIME_PATH = path.join(ROOT, 'data/examTopics/japanese-runtime.json');
const BASELINE_PATH = path.join(ROOT, 'test/fixtures/japaneseTopicQuestionBaseline.json');
const HOSTED_ANCHORS_DIR = path.join(ROOT, 'public/paper-anchors');

const reference = JSON.parse(fs.readFileSync(REFERENCE_PATH, 'utf8'));
const preservationBaseline = JSON.parse(fs.readFileSync(BASELINE_PATH, 'utf8'));

const allTags = fs.readdirSync(TAGS_DIR)
  .filter(file => file.endsWith('.json'))
  .sort()
  .flatMap(file => JSON.parse(fs.readFileSync(path.join(TAGS_DIR, file), 'utf8')))
  .filter(paper => paper.subjectId === 'japanese');

const paperIdentity = paper => [
  paper.level,
  paper.lang,
  paper.year,
  paper.paperKey,
  paper.fileid,
].join('|');

const duplicatePapers = allTags
  .map(paperIdentity)
  .filter((identity, index, identities) => identities.indexOf(identity) !== index);
if (duplicatePapers.length) {
  throw new Error(`Duplicate Japanese topic-tag papers: ${[...new Set(duplicatePapers)].join(', ')}`);
}

const localPapers = allTags.map(paper => {
  const sidecarPath = path.join(ANSWERS_DIR, String(paper.year), `${paper.fileid}.json`);
  if (!fs.existsSync(sidecarPath)) throw new Error(`Missing Japanese sidecar: ${sidecarPath}`);
  const sidecar = JSON.parse(fs.readFileSync(sidecarPath, 'utf8'));
  const answerByNumber = new Map(sidecar.q.map(question => [question.n, question]));
  const questions = paper.q.map(question => {
    const answer = answerByNumber.get(question.n);
    if (!answer) throw new Error(`${paperIdentity(paper)} Q${question.n} has no answer-map card`);
    if (!answer.label) throw new Error(`${paperIdentity(paper)} Q${question.n} has no audited label`);
    return { ...question, label: answer.label };
  });
  return { ...paper, q: questions, answerMap: sidecar };
});

let preservedBaselineCards = 0;
for (const expected of preservationBaseline) {
  const live = localPapers.find(paper => paperIdentity(paper) === paperIdentity(expected));
  if (!live) throw new Error(`Preservation failure: missing Japanese paper ${paperIdentity(expected)}`);
  for (const number of expected.questions) {
    if (!live.q.some(question => question.n === number)) {
      throw new Error(`Preservation failure: missing ${paperIdentity(expected)} Q${number}`);
    }
    preservedBaselineCards += 1;
  }
}

const expectedCanonicalIds = {
  'japanese-common-aural-conversation': ['japanese-6-0'],
  'japanese-common-aural-interviewspeech': ['japanese-6-1'],
  'japanese-common-aural-radionews': ['japanese-6-2'],
  'japanese-common-comprehension-general-reading': [
    'japanese-5-0',
    'japanese-5-1',
    'japanese-5-2',
    'japanese-5-6',
  ],
  'japanese-common-comprehension-website': ['japanese-5-0'],
  'japanese-common-grammar': ['japanese-5-5'],
  'japanese-common-kanji': ['japanese-5-4'],
  'japanese-common-oral-exam': ['japanese-4-0'],
  'japanese-common-personal-writing-all': ['japanese-5-7'],
  'japanese-common-translation-japanese-to-english': ['japanese-5-3'],
  'japanese-common-writing-holidays-abroad-events': ['japanese-5-7'],
  'japanese-common-writing-home-ireland': ['japanese-5-7'],
  'japanese-common-writing-me-my-family': ['japanese-5-7'],
  'japanese-common-writing-school-studying-japanese-future-plans': ['japanese-5-7'],
};

const parseYear = heading => {
  const year = Number(heading.match(/^(\d{4})/)?.[1]);
  if (!year) throw new Error(`Japanese reference heading has no year: ${heading}`);
  return year;
};

const writtenSection = text => Number(text.match(/\bSection\s+([1-5])\b/i)?.[1]);

const localWrittenSection = label => Number(
  label.match(/\bQuestion\s*([1-5])\b/i)?.[1]
  ?? label.match(/\bQ\.?\s*([1-5])\b/i)?.[1],
);

const referenceWrittenParts = heading => {
  const explicitPart = heading.match(/\bPart\s+([A-D](?:\s*[-,]\s*[A-D])*)\b/i)?.[1];
  const questionPart = heading.match(/\bQuestion\s+([A-D](?:\s*[-,]\s*[A-D])*)\b/i)?.[1];
  const raw = explicitPart ?? questionPart;
  return raw ? [...raw.toUpperCase().matchAll(/[A-D]/g)].map(match => match[0]) : [];
};

const localWrittenPart = label => {
  const patterns = [
    /\b(?:Question|Q\.?)\s*[1-5]\s+Part\s+([A-D])\b/i,
    /\b(?:Question|Q\.?)\s*[1-5]\s+([A-D])\b/i,
    /\b(?:Question|Q\.?)\s*[1-5][^·]*·\s*([A-D])(?:\s*[.:·]|\b)/i,
  ];
  for (const pattern of patterns) {
    const part = label.match(pattern)?.[1];
    if (part) return part.toUpperCase();
  }
  return null;
};

const expandNumberList = raw => {
  if (!raw) return [];
  const out = [];
  for (const token of raw.split(',')) {
    const range = token.trim().match(/^(\d+)\s*-\s*(\d+)$/);
    if (range) {
      const lo = Number(range[1]);
      const hi = Number(range[2]);
      for (let number = lo; number <= hi; number++) out.push(number);
      continue;
    }
    const number = Number(token.trim());
    if (number) out.push(number);
  }
  return out;
};

const referenceWrittenItems = heading => {
  const lettered = heading.match(/\bPart\s+[A-D]\s*-\s*([\d,\s-]+)$/i)?.[1];
  const numbered = heading.match(/\bPart\s+([\d,\s-]+)$/i)?.[1];
  return expandNumberList(lettered ?? numbered);
};

const localWrittenItem = label => {
  const afterPart = label.match(/\b(?:Part\s+)?[A-D]\s*[.·:]\s*(?:Q\s*)?(\d+)\b/i)?.[1];
  const namedSkill = label.match(/\b(?:Kanji|Grammar)\s+(\d+)\b/i)?.[1];
  const afterSeparator = label.match(/·\s*Q\s*(\d+)\b/i)?.[1];
  const afterSection = label.match(/\b(?:Question|Q\.?)\s*[1-5]\s*·\s*(\d+)\b/i)?.[1];
  return Number(afterPart ?? namedSkill ?? afterSeparator ?? afterSection) || null;
};

const referenceAuralPart = heading => {
  const letter = heading.match(/\b(?:Section|Question)\s+([A-D])\b/i)?.[1];
  if (letter) return letter.toUpperCase();
  const numbered = Number(heading.match(/\bQuestion\s+([1-4])\b/i)?.[1]);
  return numbered ? String.fromCharCode(64 + numbered) : null;
};

const localAuralPart = label => label.match(/\b(?:PART|CUID)\s+([A-D])\b/i)?.[1]?.toUpperCase() ?? null;

const refineWhenPossible = (candidates, predicate) => {
  const refined = candidates.filter(predicate);
  return refined.length ? refined : candidates;
};

const findPreferredPaper = (year, paperKey) => {
  const papers = localPapers.filter(paper => (
    paper.year === year
    && paper.paperKey === paperKey
    && paper.level === 'higher'
    && paper.lang === 'ev'
  ));
  if (papers.length !== 1) {
    throw new Error(`${year} ${paperKey}: expected one Higher English/BV topic-tag paper, found ${papers.length}`);
  }
  return papers[0];
};

const resolveHeading = (topicId, heading) => {
  const year = parseYear(heading);
  if (topicId === 'japanese-common-oral-exam') {
    return {
      topicId,
      heading,
      year,
      resolution: 'source-blocked',
      reason: 'The SEC archive does not publish a separate 2021 Japanese oral-material paper or scheme. The factual heading is retained, but no StudyClix-hosted question image or PDF is copied.',
    };
  }

  const paperKey = topicId.includes('-aural-') ? 'aural' : 'single';
  const paper = findPreferredPaper(year, paperKey);
  const canonicalIds = new Set(expectedCanonicalIds[topicId]);
  let candidates = paper.q.filter(question => (
    canonicalIds.has(question.primary) || canonicalIds.has(question.secondary)
  ));

  if (paperKey === 'aural') {
    const part = referenceAuralPart(heading);
    if (!part) throw new Error(`Aural heading has no section/part: ${heading}`);
    candidates = candidates.filter(question => localAuralPart(question.label) === part);
  } else {
    const section = writtenSection(heading);
    if (!section) throw new Error(`Written heading has no section: ${heading}`);
    candidates = candidates.filter(question => localWrittenSection(question.label) === section);

    // A granular translation card used to inherit the surrounding reading
    // tag. Prefer cards without an explicit translation tag for the reference
    // site's General Reading heading, while retaining a lone coarse card when
    // older answer maps necessarily cover both reading and translation.
    if (topicId === 'japanese-common-comprehension-general-reading') {
      candidates = refineWhenPossible(candidates, question => (
        question.primary !== 'japanese-5-3' && question.secondary !== 'japanese-5-3'
      ));
    }

    const parts = referenceWrittenParts(heading);
    const partDisambiguatesSource = (
      topicId === 'japanese-common-comprehension-website'
      || (topicId === 'japanese-common-comprehension-general-reading' && section === 1)
      || topicId === 'japanese-common-grammar'
      || topicId === 'japanese-common-kanji'
    );
    if (parts.length && partDisambiguatesSource) {
      candidates = refineWhenPossible(candidates, question => parts.includes(localWrittenPart(question.label)));
    }

    const items = referenceWrittenItems(heading);
    const itemDisambiguatesSkill = (
      topicId === 'japanese-common-grammar'
      || topicId === 'japanese-common-kanji'
    );
    if (items.length && itemDisambiguatesSkill) {
      candidates = refineWhenPossible(candidates, question => items.includes(localWrittenItem(question.label)));
    }
  }

  if (!candidates.length) {
    throw new Error(`${topicId}: no local card resolves ${heading}`);
  }

  return {
    topicId,
    heading,
    year,
    resolution: 'matched',
    target: {
      level: paper.level,
      lang: paper.lang,
      paperKey: paper.paperKey,
      fileid: paper.fileid,
      questionNumbers: candidates.map(question => question.n),
    },
  };
};

const associations = reference.levels.common.topics.flatMap(topic => (
  topic.officialQuestionHeadings.map(heading => resolveHeading(topic.id, heading))
));

const matched = associations.filter(association => association.resolution === 'matched');
const sourceBlocked = associations.filter(association => association.resolution === 'source-blocked');
const localQuestionIdentity = (paper, number) => [
  paper.level,
  paper.lang,
  paper.year,
  paper.paperKey,
  number,
].join('|');

const referenceTopicsByLocalQuestion = new Map();
for (const association of matched) {
  for (const number of association.target.questionNumbers) {
    const key = [
      association.target.level,
      association.target.lang,
      association.year,
      association.target.paperKey,
      number,
    ].join('|');
    const ids = referenceTopicsByLocalQuestion.get(key) ?? [];
    if (!ids.includes(association.topicId)) ids.push(association.topicId);
    referenceTopicsByLocalQuestion.set(key, ids);
  }
}

const fallbackTopicIds = (paper, question) => {
  const canonical = new Set([question.primary, question.secondary].filter(Boolean));
  const topicIds = [];
  const add = topicId => {
    if (!topicIds.includes(topicId)) topicIds.push(topicId);
  };

  if (canonical.has('japanese-6-0')) add('japanese-common-aural-conversation');
  if (canonical.has('japanese-6-1')) add('japanese-common-aural-interviewspeech');
  if (canonical.has('japanese-6-2')) add('japanese-common-aural-radionews');

  if (canonical.has('japanese-5-0')) {
    if (localWrittenSection(question.label) === 1) {
      add('japanese-common-comprehension-website');
    } else {
      add('japanese-common-comprehension-general-reading');
    }
  }
  if ([...canonical].some(id => ['japanese-5-1', 'japanese-5-2', 'japanese-5-6'].includes(id))) {
    add('japanese-common-comprehension-general-reading');
  }
  if (canonical.has('japanese-5-3')) add('japanese-common-translation-japanese-to-english');
  if (canonical.has('japanese-5-4')) add('japanese-common-kanji');
  if (canonical.has('japanese-5-5')) add('japanese-common-grammar');
  if (canonical.has('japanese-5-7')) add('japanese-common-personal-writing-all');

  if (!topicIds.length) {
    throw new Error(`${paperIdentity(paper)} Q${question.n} has no Japanese exam-topic fallback`);
  }
  return topicIds;
};

const localQuestionMappings = localPapers.flatMap(paper => paper.q.map(question => {
  const referenceTopicIds = referenceTopicsByLocalQuestion.get(localQuestionIdentity(paper, question.n));
  return {
    level: paper.level,
    lang: paper.lang,
    year: paper.year,
    fileid: paper.fileid,
    paperKey: paper.paperKey,
    n: question.n,
    topicIds: referenceTopicIds ?? fallbackTopicIds(paper, question),
    provenance: referenceTopicIds ? 'reference' : 'retained-local',
  };
}));

const hostedAnchorForQuestion = (question, paperRegionFallback) => {
  const anchor = {
    n: question.n,
    pP: question.pP,
    pY: question.pY,
    region: [{ p: 1 }],
    mode: 'pagejump',
    conf: 0.5,
  };
  for (const key of ['label', 'printOrder', 'paperRegion', 'endP', 'endY']) {
    if (question[key] !== undefined) anchor[key] = question[key];
  }
  // Some pre-existing classic maps intentionally carry page-jump anchors:
  // several subquestions share one page/coordinate, or the best verified
  // anchor is the top of that page. The normal next-anchor crop derivation
  // must reject those ambiguous coordinates. Give the hosted PAPER-ONLY copy
  // an explicit full-page region instead: it truthfully contains the labelled
  // question and is safer than either a dead card or a guessed tight crop.
  if (!anchor.paperRegion && paperRegionFallback) {
    anchor.paperRegion = paperRegionFallback;
  }
  return anchor;
};

const hostedPaperAnchors = localPapers.map(paper => {
  const taggedNumbers = paper.q.map(question => question.n);
  const answerNumbers = paper.answerMap.q.map(question => question.n);
  if (JSON.stringify(answerNumbers) !== JSON.stringify(taggedNumbers)) {
    throw new Error(
      `${paperIdentity(paper)} answer-map identities differ from topic tags: `
      + `${answerNumbers.join(',')} vs ${taggedNumbers.join(',')}`,
    );
  }

  const coordinateCounts = new Map();
  for (const question of paper.answerMap.q) {
    const coordinate = `${question.pP}|${question.pY[0]}`;
    coordinateCounts.set(coordinate, (coordinateCounts.get(coordinate) ?? 0) + 1);
  }
  const fallbackRegions = new Map();
  for (const question of paper.answerMap.q) {
    if (question.pY[0] === 0 || coordinateCounts.get(`${question.pP}|${question.pY[0]}`) > 1) {
      fallbackRegions.set(question.n, [{ p: question.pP, r: [0, 0, 1, 1] }]);
    }
  }
  const coordinateOrder = [...paper.answerMap.q].sort((a, b) => (
    a.pP - b.pP || a.pY[0] - b.pY[0]
  ));
  for (let index = 0; index < coordinateOrder.length - 1; index++) {
    const question = coordinateOrder[index];
    const next = coordinateOrder[index + 1];
    if (!question.paperRegion && next.pP - question.pP > 3) {
      fallbackRegions.set(
        question.n,
        Array.from({ length: next.pP - question.pP }, (_, offset) => ({
          p: question.pP + offset,
          r: [0, offset === 0 ? Math.max(0, question.pY[0] - 0.008) : 0, 1, 1],
        })),
      );
    }
  }
  const artifact = {
    v: 1,
    paperFileid: paper.answerMap.paperFileid,
    schemeFileid: '',
    component: paper.answerMap.component,
    band: [1, 1],
    copyright: '© State Examinations Commission',
    paperOnly: 1,
    q: paper.answerMap.q.map(question => hostedAnchorForQuestion(
      question,
      fallbackRegions.get(question.n),
    )),
  };
  const yearDir = path.join(HOSTED_ANCHORS_DIR, String(paper.year));
  const outputPath = path.join(yearDir, `${paper.fileid}.json`);
  fs.mkdirSync(yearDir, { recursive: true });
  fs.writeFileSync(outputPath, `${JSON.stringify(artifact)}\n`);
  return path.relative(ROOT, outputPath);
});

const duplicateQuestionMappings = localQuestionMappings
  .map(mapping => [mapping.level, mapping.lang, mapping.year, mapping.paperKey, mapping.n].join('|'))
  .filter((identity, index, identities) => identities.indexOf(identity) !== index);
if (duplicateQuestionMappings.length) {
  throw new Error(`Duplicate Japanese local question identities: ${[...new Set(duplicateQuestionMappings)].join(', ')}`);
}

const output = {
  schemaVersion: 1,
  subjectId: 'japanese',
  capturedAt: reference.capturedAt,
  policy: {
    matchedSource: 'Entitled local SEC corpus only.',
    excludedContent: 'No commercial mock question, solution, note, question text, StudyClix image or StudyClix-hosted PDF is copied.',
  },
  summary: {
    referenceHeadingAssociations: associations.length,
    matchedHeadingAssociations: matched.length,
    sourceBlockedHeadingAssociations: sourceBlocked.length,
    matchedLocalCardLinks: matched.reduce((count, association) => count + association.target.questionNumbers.length, 0),
    localPaperVariants: localPapers.length,
    hostedPaperAnchorMaps: hostedPaperAnchors.length,
    localQuestionMappings: localQuestionMappings.length,
    referenceMappedLocalQuestions: localQuestionMappings.filter(mapping => mapping.provenance === 'reference').length,
    retainedLocalQuestions: localQuestionMappings.filter(mapping => mapping.provenance === 'retained-local').length,
    preservedBaselinePaperVariants: preservationBaseline.length,
    preservedBaselineCards,
  },
  associations,
  localQuestionMappings,
};

fs.writeFileSync(OUTPUT_PATH, `${JSON.stringify(output, null, 2)}\n`);

// Keep the evidence-rich crosswalk above out of the main application chunk.
// Topic ids are represented by their stable index in the fourteen-topic audit.
const runtimeTopicIndex = new Map(
  reference.levels.common.topics.map((topic, index) => [topic.id, index]),
);
const paperKeyCode = paperKey => {
  if (paperKey === 'single') return 's';
  if (paperKey === 'aural') return 'a';
  if (paperKey === 'oral') return 'r';
  throw new Error(`Unknown Japanese runtime paper key: ${paperKey}`);
};
const runtimePartReferences = associations.flatMap(association => {
  const topicIndex = runtimeTopicIndex.get(association.topicId);
  if (!Number.isInteger(topicIndex)) throw new Error(`Unknown Japanese topic: ${association.topicId}`);
  if (association.resolution === 'matched') {
    return association.target.questionNumbers.map(number => [
      topicIndex,
      association.year,
      association.target.level === 'higher' ? 'h' : 'o',
      paperKeyCode(association.target.paperKey),
      number,
      association.heading,
    ]);
  }
  const number = association.heading.match(/Question\s+(\d+)/i)?.[1];
  if (!number) throw new Error(`Unparseable Japanese source-blocked heading: ${association.heading}`);
  return [[topicIndex, association.year, 'c', 'r', number, association.heading]];
});
const runtime = {
  v: 1,
  partReferences: runtimePartReferences,
  questionMappings: localQuestionMappings.map(mapping => [
    mapping.level === 'higher' ? 'h' : 'o',
    mapping.lang === 'ev' ? 'e' : 'i',
    mapping.year,
    paperKeyCode(mapping.paperKey),
    mapping.n,
    mapping.topicIds.map(topicId => {
      const topicIndex = runtimeTopicIndex.get(topicId);
      if (!Number.isInteger(topicIndex)) throw new Error(`Unknown Japanese topic: ${topicId}`);
      return topicIndex;
    }),
  ]),
};
fs.writeFileSync(RUNTIME_PATH, `${JSON.stringify(runtime)}\n`);

console.log(
  `Japanese reference reconciliation: ${matched.length}/${associations.length} matched, `
  + `${sourceBlocked.length} source-blocked, ${output.summary.matchedLocalCardLinks} local card links`,
);
console.log(
  `Japanese preservation baseline: ${preservationBaseline.length} paper variants, `
  + `${preservedBaselineCards} cards`,
);
console.log(`Japanese hosted paper anchors: ${hostedPaperAnchors.length} maps`);
