#!/usr/bin/env node
/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 *
 * Build the additive Music exam-topic layer from the metadata-only reference
 * audit and NextStepUni's entitled SEC paper corpus.
 *
 * Music needs exact booklet identities: composing, listening, the Higher
 * listening elective and unprepared tests all retain the historical `single`
 * Paper Trail key and restart their printed question numbers. The generated
 * runtime join therefore carries the SEC component code and is decoded into
 * FILE_QUESTION_TOPICS. Existing Mark Bank cards are treated as immutable.
 */

import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const HERE = path.dirname(fileURLToPath(import.meta.url));
const ROOT = path.resolve(HERE, '../..');
const HOSTED_ROOT = path.join(ROOT, 'public/paper-anchors');
const ANSWERS_ROOT = path.join(ROOT, 'scripts/paper-trail/answers');
const EXAM_PAPERS_ROOT = path.join(ROOT, 'paper-trail-corpus/exampapers');
const MARKING_SCHEMES_ROOT = path.join(ROOT, 'paper-trail-corpus/markingschemes');
const REFERENCE_PATH = path.join(ROOT, 'data/examTopics/music.json');
const RECONCILIATION_PATH = path.join(ROOT, 'data/examTopics/music-audit-reconciliation.json');
const BASELINE_PATH = path.join(ROOT, 'test/fixtures/musicTopicQuestionBaseline.json');
const TAGS_PATH = path.join(HERE, 'topic-tags/tags/music.json');
const OUTPUT_PATH = path.join(ROOT, 'data/examTopics/music-local-crosswalk.json');
const RUNTIME_PATH = path.join(ROOT, 'data/examTopics/music-runtime.json');
const CURRICULUM_PATH = path.join(ROOT, 'data/examTopics/music-curriculum-crosswalk.json');

const readJson = file => JSON.parse(fs.readFileSync(file, 'utf8'));
const reference = readJson(REFERENCE_PATH);
const reconciliation = readJson(RECONCILIATION_PATH);
const baseline = readJson(BASELINE_PATH);

const referenceTopics = Object.entries(reference.variants).flatMap(([level, variant]) => (
  variant.topics.map(topic => ({ ...topic, level, archive: false }))
));
if (referenceTopics.length !== 34) {
  throw new Error(`Expected 34 Music reference topics, found ${referenceTopics.length}`);
}

const archiveTopics = [
  ['music-higher-listening-tchaikovsky-archive', 'Listening - Tchaikovsky (NextStepUni archive)', 'higher', 'music-2-15'],
  ['music-higher-listening-gerald-barry-archive', 'Listening - Gerald Barry (NextStepUni archive)', 'higher', 'music-2-16'],
  ['music-higher-listening-freddie-mercury-archive', 'Listening - Freddie Mercury (NextStepUni archive)', 'higher', 'music-2-14'],
  ['music-higher-listening-bach-archive', 'Listening - Bach (NextStepUni archive)', 'higher', 'music-2-17'],
  ['music-higher-listening-elective-archive', 'Listening Elective (NextStepUni archive)', 'higher', 'music-2-8'],
  ['music-ordinary-listening-tchaikovsky-archive', 'Listening - Tchaikovsky (NextStepUni archive)', 'ordinary', 'music-2-15'],
  ['music-ordinary-listening-gerald-barry-archive', 'Listening - Gerald Barry (NextStepUni archive)', 'ordinary', 'music-2-16'],
  ['music-ordinary-listening-freddie-mercury-archive', 'Listening - Freddie Mercury (NextStepUni archive)', 'ordinary', 'music-2-14'],
  ['music-ordinary-listening-bach-archive', 'Listening - Bach (NextStepUni archive)', 'ordinary', 'music-2-17'],
].map(([id, label, level, curriculumNodeId]) => ({
  id,
  label,
  level,
  sourcePath: `/nextstepuni-preservation/music/${id}`,
  reportedQuestionCount: 0,
  officialQuestionHeadings: [],
  mockQuestionCount: 0,
  providerSampleQuestionCount: 0,
  sourceLabelConflictCount: 0,
  archive: true,
  curriculumNodeId,
}));

const topics = [...referenceTopics, ...archiveTopics];
const topicById = new Map(topics.map(topic => [topic.id, topic]));
const topicIndex = new Map(topics.map((topic, index) => [topic.id, index]));

const H = {
  chords: 'music-higher-composing-melody-and-bass-from-chords',
  rhythm: 'music-higher-composing-to-a-given-dance-rhythm-or-meter',
  descant: 'music-higher-composing-adding-a-countermelodydescant-and-chords',
  bass: 'music-higher-composing-adding-bass-and-chords-to-a-tune',
  continuation: 'music-higher-composing-continuation-of-a-given-opening',
  text: 'music-higher-composing-setting-music-to-a-given-text',
  aural: 'music-higher-listening-aural-skills-unheard',
  berlioz: 'music-higher-listening-berlioz',
  deane: 'music-higher-listening-deane',
  irish: 'music-higher-listening-irish-music',
  irishEssay: 'music-higher-listening-irish-music-essay',
  mozart: 'music-higher-listening-mozart',
  beatles: 'music-higher-listening-the-beatles',
  practicals: 'music-higher-practicals',
  memoryMelody: 'music-higher-unprepared-aural-memory-melody',
  memoryRhythm: 'music-higher-unprepared-aural-memory-rhythm',
  improvisation: 'music-higher-unprepared-improvisation',
  sightReading: 'music-higher-unprepared-sight-reading-all',
  rhythmGuitar: 'music-higher-unprepared-sight-reading-rhythm-guitar',
  sightClapping: 'music-higher-unprepared-sight-reading-sight-clapping',
  ukulele: 'music-higher-unprepared-sight-reading-ukulele',
  tchaikovsky: 'music-higher-listening-tchaikovsky-archive',
  barry: 'music-higher-listening-gerald-barry-archive',
  mercury: 'music-higher-listening-freddie-mercury-archive',
  bach: 'music-higher-listening-bach-archive',
  elective: 'music-higher-listening-elective-archive',
};
const O = {
  bass: 'music-ordinary-adding-bass-and-chords-at-cadence-points',
  descant: 'music-ordinary-adding-descant-notes-and-chords',
  chords: 'music-ordinary-composing-bass-and-melody-from-chords',
  rhythm: 'music-ordinary-composing-to-a-given-rhythm-or-meter',
  continuation: 'music-ordinary-continuation-of-a-given-opening',
  aural: 'music-ordinary-listening-aural-skills-unheard',
  berlioz: 'music-ordinary-listening-berlioz',
  deane: 'music-ordinary-listening-deane',
  irish: 'music-ordinary-listening-irish-music',
  mozart: 'music-ordinary-listening-mozart',
  beatles: 'music-ordinary-listening-the-beatles',
  practicals: 'music-ordinary-practicals',
  text: 'music-ordinary-setting-music-to-a-given-text',
  tchaikovsky: 'music-ordinary-listening-tchaikovsky-archive',
  barry: 'music-ordinary-listening-gerald-barry-archive',
  mercury: 'music-ordinary-listening-freddie-mercury-archive',
  bach: 'music-ordinary-listening-bach-archive',
};

const CURRICULUM_CROSSWALK = {
  [H.chords]: ['music-1-14'],
  [H.rhythm]: ['music-1-12'],
  [H.descant]: ['music-1-15'],
  [H.bass]: ['music-1-13'],
  [H.continuation]: ['music-1-10'],
  [H.text]: ['music-1-11'],
  [H.aural]: ['music-2-4', 'music-2-3'],
  [H.berlioz]: ['music-2-10'],
  [H.deane]: ['music-2-11'],
  [H.irish]: ['music-2-2'],
  [H.irishEssay]: ['music-2-13', 'music-2-2'],
  [H.mozart]: ['music-2-9'],
  [H.beatles]: ['music-2-12'],
  [H.practicals]: ['music-0-4', 'music-0-5', 'music-0-6', 'music-0-12'],
  [H.memoryMelody]: ['music-0-5'],
  [H.memoryRhythm]: ['music-0-5'],
  [H.improvisation]: ['music-0-6'],
  [H.sightReading]: ['music-0-4'],
  [H.rhythmGuitar]: ['music-0-4'],
  [H.sightClapping]: ['music-0-4'],
  [H.ukulele]: ['music-0-4'],
  [H.tchaikovsky]: ['music-2-15'],
  [H.barry]: ['music-2-16'],
  [H.mercury]: ['music-2-14'],
  [H.bach]: ['music-2-17'],
  [H.elective]: ['music-2-8'],
  [O.bass]: ['music-1-13'],
  [O.descant]: ['music-1-15'],
  [O.chords]: ['music-1-14'],
  [O.rhythm]: ['music-1-12'],
  [O.continuation]: ['music-1-10'],
  [O.aural]: ['music-2-4', 'music-2-3'],
  [O.berlioz]: ['music-2-10'],
  [O.deane]: ['music-2-11'],
  [O.irish]: ['music-2-2'],
  [O.mozart]: ['music-2-9'],
  [O.beatles]: ['music-2-12'],
  [O.practicals]: ['music-0-4', 'music-0-5', 'music-0-6'],
  [O.text]: ['music-1-11'],
  [O.tchaikovsky]: ['music-2-15'],
  [O.barry]: ['music-2-16'],
  [O.mercury]: ['music-2-14'],
  [O.bach]: ['music-2-17'],
};
for (const topic of topics) {
  if (!CURRICULUM_CROSSWALK[topic.id]?.length) {
    throw new Error(`Music topic has no curriculum bridge: ${topic.id}`);
  }
}

const composingTopics = level => {
  const ids = level === 'higher' ? H : O;
  return [ids.continuation, ids.text, ids.rhythm, ids.chords, ids.bass, ids.descant];
};
const composingCanonical = [
  ['music-1-10'],
  ['music-1-11'],
  ['music-1-12'],
  ['music-1-14'],
  ['music-1-13'],
  ['music-1-15'],
];

const SET_WORKS = {
  2010: ['deane', 'berlioz', 'mozart', 'beatles'],
  2011: ['bach', 'barry', 'tchaikovsky', 'mercury'],
  2012: ['mozart', 'berlioz', 'deane', 'beatles'],
  2013: ['tchaikovsky', 'bach', 'barry', 'mercury'],
  2014: ['mozart', 'beatles', 'berlioz', 'deane'],
  2015: ['deane', 'berlioz', 'mozart', 'beatles'],
  2016: ['mozart', 'berlioz', 'beatles', 'deane'],
  2017: ['barry', 'mercury', 'bach', 'tchaikovsky'],
  2018: ['tchaikovsky', 'mercury', 'barry', 'bach'],
  2019: ['tchaikovsky', 'barry', 'bach', 'mercury'],
  2020: ['beatles', 'berlioz', 'mozart', 'deane'],
  2021: ['berlioz', 'deane', 'mozart', 'beatles'],
  2022: ['mozart', 'berlioz', 'deane', 'beatles'],
  2023: ['mercury', 'tchaikovsky', 'barry', 'bach'],
  2024: ['barry', 'bach', 'mercury', 'tchaikovsky'],
  2025: ['tchaikovsky', 'barry', 'mercury', 'bach'],
  2026: ['berlioz', 'mozart', 'deane', 'beatles'],
};
const SET_WORK_CANONICAL = {
  mozart: 'music-2-9',
  berlioz: 'music-2-10',
  deane: 'music-2-11',
  beatles: 'music-2-12',
  mercury: 'music-2-14',
  tchaikovsky: 'music-2-15',
  barry: 'music-2-16',
  bach: 'music-2-17',
};

const paperIdentity = paper => `${paper.year}|${paper.fileid}`;
const baselineByIdentity = new Map(baseline.map(paper => [paperIdentity(paper), paper]));
const papers = reconciliation.inventory.map(source => {
  const component = source.component;
  const stored = baselineByIdentity.get(paperIdentity(source));
  let q;
  if (stored) {
    q = stored.questions.map(question => ({ ...question }));
  } else if (component === '006') {
    q = composingCanonical.map(([primary], index) => ({ n: String(index + 1), primary }));
  } else if (component === '007') {
    q = [{ n: '1', primary: 'music-2-8' }];
  } else if (component === '008') {
    const works = SET_WORKS[source.year];
    if (!works) throw new Error(`Missing Music set-work sequence for ${source.year}`);
    q = [
      ...works.map((work, index) => ({ n: String(index + 1), primary: SET_WORK_CANONICAL[work] })),
      { n: '5', primary: 'music-2-2' },
      { n: '6', primary: 'music-2-4', secondary: 'music-2-3' },
    ];
  } else if (component === 'U00' && source.level === 'higher' && source.year === 2013) {
    q = Array.from({ length: 12 }, (_, index) => ({ n: String(index + 1), primary: 'music-0-5' }));
  } else {
    throw new Error(`No Music card template for ${paperIdentity(source)} (${component})`);
  }
  return {
    subjectId: 'music',
    level: source.level,
    lang: source.lang,
    year: source.year,
    fileid: source.fileid,
    paperKey: 'single',
    component,
    q,
  };
}).sort((a, b) => (
  b.year - a.year
  || a.level.localeCompare(b.level)
  || a.component.localeCompare(b.component)
  || a.lang.localeCompare(b.lang)
));

if (papers.length !== 178) throw new Error(`Expected 178 Music variants, found ${papers.length}`);

let preservedBaselineCards = 0;
for (const expected of baseline) {
  const paper = papers.find(candidate => paperIdentity(candidate) === paperIdentity(expected));
  if (!paper) throw new Error(`Preservation failure: missing ${paperIdentity(expected)}`);
  for (const expectedQuestion of expected.questions) {
    const actual = paper.q.find(question => question.n === expectedQuestion.n);
    if (JSON.stringify(actual) !== JSON.stringify(expectedQuestion)) {
      throw new Error(`Preservation failure: changed ${paperIdentity(expected)} Q${expectedQuestion.n}`);
    }
    preservedBaselineCards += 1;
  }
}
if (preservedBaselineCards !== 184) {
  throw new Error(`Expected to preserve 184 Music cards, preserved ${preservedBaselineCards}`);
}

const answerRegionOwners = new Map();
const existingAnswerSidecars = papers.flatMap(paper => {
  const sidecarPath = path.join(ANSWERS_ROOT, String(paper.year), `${paper.fileid}.json`);
  if (!fs.existsSync(sidecarPath)) return [];
  const sidecar = readJson(sidecarPath);
  if (sidecar.paperFileid !== paper.fileid) {
    throw new Error(`${path.relative(ROOT, sidecarPath)}: paper file ID does not match its Music booklet`);
  }
  if (!sidecar.schemeFileid) {
    throw new Error(`${path.relative(ROOT, sidecarPath)}: verified answer sidecar has no scheme file ID`);
  }
  const paperPath = path.join(EXAM_PAPERS_ROOT, String(paper.year), sidecar.paperFileid);
  const schemePath = path.join(MARKING_SCHEMES_ROOT, String(paper.year), sidecar.schemeFileid);
  if (!fs.existsSync(paperPath) || !fs.existsSync(schemePath)) {
    throw new Error(`${path.relative(ROOT, sidecarPath)}: referenced paper or marking scheme is unavailable`);
  }
  const expectedNumbers = new Set(paper.q.map(question => question.n));
  const seenNumbers = new Set();
  let previousQuestionEnd = null;
  for (const question of sidecar.q ?? []) {
    if (!expectedNumbers.has(question.n) || seenNumbers.has(question.n)) {
      throw new Error(`${path.relative(ROOT, sidecarPath)}: invalid or duplicate Music question ${question.n}`);
    }
    seenNumbers.add(question.n);
    if (question.mode !== 'crop' || question.conf < 0.9 || !question.region?.length) {
      throw new Error(`${path.relative(ROOT, sidecarPath)} Q${question.n}: answer crop is not verified`);
    }
    let totalArea = 0;
    let firstStart = null;
    let previousEnd = null;
    for (const segment of question.region) {
      const rect = segment.r;
      if (!Number.isInteger(segment.p) || segment.p < 1) {
        throw new Error(`${path.relative(ROOT, sidecarPath)} Q${question.n}: invalid scheme page`);
      }
      if (
        !Array.isArray(rect)
        || rect.length !== 4
        || rect.some(value => !Number.isFinite(value) || value < 0 || value > 1)
        || rect[2] <= rect[0]
        || rect[3] <= rect[1]
      ) {
        throw new Error(`${path.relative(ROOT, sidecarPath)} Q${question.n}: invalid scheme rectangle`);
      }
      if (
        previousEnd
        && (segment.p < previousEnd.page
          || (segment.p === previousEnd.page && rect[1] < previousEnd.y))
      ) {
        throw new Error(`${path.relative(ROOT, sidecarPath)} Q${question.n}: scheme regions run backwards`);
      }
      firstStart ??= { page: segment.p, y: rect[1] };
      previousEnd = { page: segment.p, y: rect[3] };
      totalArea += (rect[2] - rect[0]) * (rect[3] - rect[1]);
    }
    if (totalArea < 0.12) {
      throw new Error(`${path.relative(ROOT, sidecarPath)} Q${question.n}: implausibly small answer crop`);
    }
    if (previousQuestionEnd && firstStart) {
      const pageDelta = firstStart.page - previousQuestionEnd.page;
      const continuousOnSamePage = pageDelta === 0
        && firstStart.y >= previousQuestionEnd.y - 0.0121
        && firstStart.y <= previousQuestionEnd.y + 0.02;
      const continuousOnNextPage = pageDelta === 1
        && previousQuestionEnd.y >= 0.99
        && firstStart.y <= 0.01;
      if (!continuousOnSamePage && !continuousOnNextPage) {
        throw new Error(`${path.relative(ROOT, sidecarPath)} Q${question.n}: scheme questions are not contiguous`);
      }
    }
    previousQuestionEnd = previousEnd;
  }
  const regionFingerprint = JSON.stringify(
    (sidecar.q ?? []).map(question => ({ n: question.n, region: question.region })),
  );
  const regionIdentity = [
    paper.year,
    paper.level,
    paper.lang,
    sidecar.schemeFileid,
    regionFingerprint,
  ].join('|');
  const existingOwner = answerRegionOwners.get(regionIdentity);
  if (existingOwner && existingOwner.component !== paper.component) {
    throw new Error(
      `${path.relative(ROOT, sidecarPath)}: duplicates the complete ${existingOwner.component} `
      + `answer-region map from ${existingOwner.path}`,
    );
  }
  answerRegionOwners.set(regionIdentity, {
    component: paper.component,
    path: path.relative(ROOT, sidecarPath),
  });
  return [{
    path: path.relative(ROOT, sidecarPath),
    component: paper.component,
    crops: seenNumbers.size,
    complete: seenNumbers.size === expectedNumbers.size,
  }];
});
const existingAnswerSidecarCrops = existingAnswerSidecars
  .reduce((sum, sidecar) => sum + sidecar.crops, 0);
const completeExistingAnswerSidecarMaps = existingAnswerSidecars
  .filter(sidecar => sidecar.complete).length;
const partialExistingAnswerSidecarMaps = existingAnswerSidecars.length
  - completeExistingAnswerSidecarMaps;

const yearFromHeading = heading => Number(heading.match(/^(\d{4})/)?.[1]);
const sittingFromHeading = heading => (
  /deferred/i.test(heading) ? 'deferred' : /sample/i.test(heading) ? 'sample' : 'main'
);
const componentFromHeading = heading => (
  /unprepared/i.test(heading) ? 'U00' : /composing/i.test(heading) ? '006' : '008'
);
const questionFromHeading = (heading, component) => {
  if (component === 'U00') return null;
  if (component === '006') {
    return heading.match(/Question [AB]\s*-\s*Part ([1-6])/i)?.[1]
      ?? heading.match(/Question ([1-6])/i)?.[1]
      ?? null;
  }
  return heading.match(/Section ([1-6])\s*-\s*Question [A-Za-z]/i)?.[1]
    ?? heading.match(/Question ([1-6])/i)?.[1]
    ?? null;
};

const papersForReference = (year, level, component) => papers.filter(paper => (
  paper.year === year && paper.level === level && paper.component === component
));
const associations = [];
const referencedTopicsByLogicalCard = new Map();
for (const topic of referenceTopics) {
  for (const heading of topic.officialQuestionHeadings) {
    const year = yearFromHeading(heading);
    const sitting = sittingFromHeading(heading);
    const component = componentFromHeading(heading);
    const n = questionFromHeading(heading, component);
    const candidates = sitting === 'main' && n
      ? papersForReference(year, topic.level, component).filter(paper => paper.q.some(q => q.n === n))
      : [];
    let reason;
    if (sitting !== 'main') reason = `The ${sitting} heading is retained, but no matching entitled ${sitting} booklet is present in the local corpus.`;
    else if (year < 2010) reason = 'The factual heading predates the entitled 2010–2026 local corpus.';
    else if (component === 'U00') reason = 'The 2019 practical section identity is retained without joining it to the differently structured 2013–2016 unprepared-test booklets.';
    else if (!candidates.length) reason = 'No entitled local booklet/card with this exact level, year, component and question identity is present.';

    if (!reason) {
      const logicalKey = `${topic.level}|${year}|${component}|${n}`;
      const ids = referencedTopicsByLogicalCard.get(logicalKey) ?? [];
      if (!ids.includes(topic.id)) ids.push(topic.id);
      referencedTopicsByLogicalCard.set(logicalKey, ids);
    }
    associations.push({
      topicId: topic.id,
      heading,
      year,
      sitting,
      component,
      n: n ?? 'unresolved',
      resolution: reason ? 'source-blocked' : 'matched',
      ...(reason ? { reason } : {
        targets: candidates.map(paper => ({
          level: paper.level,
          lang: paper.lang,
          paperKey: paper.paperKey,
          fileid: paper.fileid,
          n,
        })),
      }),
    });
  }
}
if (associations.length !== 646) {
  throw new Error(`Expected 646 factual Music headings, found ${associations.length}`);
}

const baseTopicIdsForPaper = paper => {
  if (paper.component === '006') return composingTopics(paper.level);
  if (paper.component === '007') return [H.elective];
  if (paper.component === 'U00') return paper.q.map(() => (
    paper.level === 'higher' ? H.practicals : O.practicals
  ));
  const levelIds = paper.level === 'higher' ? H : O;
  return [
    ...SET_WORKS[paper.year].map(work => levelIds[work]),
    ...(paper.level === 'higher' ? [[levelIds.irish, levelIds.irishEssay]] : [[levelIds.irish]]),
    [levelIds.aural],
  ];
};

const localQuestionMappings = papers.flatMap(paper => {
  const base = baseTopicIdsForPaper(paper);
  return paper.q.map((question, index) => {
    const baseTopicIds = Array.isArray(base[index]) ? base[index] : [base[index]];
    const referenced = referencedTopicsByLogicalCard.get(
      `${paper.level}|${paper.year}|${paper.component}|${question.n}`,
    ) ?? [];
    const topicIds = [...new Set([...referenced, ...baseTopicIds])]
      .sort((a, b) => topicIndex.get(a) - topicIndex.get(b));
    if (!topicIds.length || topicIds.some(id => !topicById.has(id))) {
      throw new Error(`${paperIdentity(paper)} Q${question.n}: invalid Music topic mapping`);
    }
    if (topicIds.some(id => topicById.get(id).level !== paper.level)) {
      throw new Error(`${paperIdentity(paper)} Q${question.n}: cross-level Music mapping`);
    }
    return {
      level: paper.level,
      lang: paper.lang,
      year: paper.year,
      fileid: paper.fileid,
      paperKey: paper.paperKey,
      component: paper.component,
      n: question.n,
      topicIds,
      provenance: referenced.length ? 'reference+official-paper' : 'official-paper-retained',
    };
  });
});

const identities = localQuestionMappings.map(mapping => `${mapping.year}|${mapping.fileid}|${mapping.n}`);
if (new Set(identities).size !== identities.length) {
  throw new Error('Duplicate Music file/question mapping');
}
if (localQuestionMappings.length !== 978) {
  throw new Error(`Expected 978 Music physical mappings, found ${localQuestionMappings.length}`);
}

const tagPapers = papers.map(({ component: _component, ...paper }) => paper);
fs.writeFileSync(TAGS_PATH, `${JSON.stringify(tagPapers, null, 2)}\n`);

const fullPages = (start, end = start) => Array.from(
  { length: Math.max(1, end - start + 1) },
  (_, index) => ({ p: start + index, r: [0, 0, 1, 1] }),
);
const composingStarts = year => (
  year <= 2018 ? [3, 4, 5, 6, 8, 10]
    : year <= 2020 ? [3, 5, 7, 8, 10, 12]
      : [4, 6, 8, 12, 14, 16]
);
const listeningStarts = (year, level) => {
  if (year <= 2017) return [2, 4, 5, 6, 8, 10];
  if (year === 2018) return [2, 4, 5, 6, 8, 10];
  if (year === 2019) return level === 'higher'
    ? [2, 4, 5, 6, 8, 12]
    : [2, 4, 5, 6, 8, 10];
  if (year === 2020) return [2, 4, 5, 6, 8, 12];
  if (year === 2021) return level === 'higher'
    ? [3, 6, 8, 10, 12, 17]
    : [3, 8, 10, 12, 14, 16];
  if (year === 2022) return level === 'higher'
    ? [3, 6, 8, 10, 12, 17]
    : [3, 6, 8, 10, 12, 14];
  if (year >= 2023 && year <= 2025) return level === 'higher'
    ? [3, 6, 8, 10, 12, 18]
    : [3, 6, 8, 10, 12, 14];
  return level === 'higher' ? [3, 8, 10, 12, 14, 20] : [3, 6, 8, 10, 12, 14];
};
const labelsFor = paper => {
  if (paper.component === '006') return [
    'Continuation of a given opening',
    'Setting music to a given text',
    'Dance rhythm, metre or form',
    'Melody and bass from chords',
    'Bass notes and chord indications',
    'Countermelody or descant and chords',
  ];
  if (paper.component === '007') return ['Listening Elective'];
  if (paper.component === '008') {
    const display = {
      mozart: 'Mozart', berlioz: 'Berlioz', deane: 'Deane', beatles: 'The Beatles',
      mercury: 'Freddie Mercury', tchaikovsky: 'Tchaikovsky', barry: 'Gerald Barry', bach: 'Bach',
    };
    return [...SET_WORKS[paper.year].map(work => display[work]), 'Irish Music', 'Aural Skills'];
  }
  return paper.q.map(question => `Unprepared Test ${question.n}`);
};
const buildHostedQuestions = paper => {
  if (paper.component === 'U00') {
    const templatePath = path.join(HOSTED_ROOT, '2014',
      `LC067${paper.level === 'higher' ? 'A' : 'G'}LPU00${paper.lang.toUpperCase()}.pdf.json`);
    const fallbackPath = path.join(HOSTED_ROOT, '2014',
      `LC067${paper.level === 'higher' ? 'A' : 'G'}LPU00EV.pdf.json`);
    const template = readJson(fs.existsSync(templatePath) ? templatePath : fallbackPath);
    return template.q.map((question, index) => ({
      ...question,
      n: paper.q[index].n,
      label: `Unprepared Test ${paper.q[index].n}`,
    }));
  }
  const starts = paper.component === '006'
    ? composingStarts(paper.year)
    : paper.component === '007'
      ? [paper.year === 2026 ? 4 : 2]
      : listeningStarts(paper.year, paper.level);
  const labels = labelsFor(paper);
  return paper.q.map((question, index) => {
    const start = starts[index];
    const next = starts[index + 1];
    return {
      n: question.n,
      label: labels[index],
      printOrder: index + 1,
      pP: start,
      pY: [0, 1],
      paperRegion: fullPages(start, next ? next - 1 : start),
      region: [{ p: 1 }],
      mode: 'pagejump',
      conf: 0.5,
    };
  });
};

const hostedAnchorMaps = [];
let preservedHostedAnchorMaps = 0;
let generatedHostedAnchorMaps = 0;
const preMigrationHostedAnchorIdentities = new Set(
  reconciliation.inventory
    .filter(item => item.hasHostedPaperMap)
    .map(item => `${item.year}|${item.fileid}`),
);
for (const paper of papers) {
  const yearDir = path.join(HOSTED_ROOT, String(paper.year));
  const outputPath = path.join(yearDir, `${paper.fileid}.json`);
  if (preMigrationHostedAnchorIdentities.has(paperIdentity(paper)) && fs.existsSync(outputPath)) {
    const current = readJson(outputPath);
    const expectedNumbers = paper.q.map(question => question.n);
    const currentNumbers = current.q?.map(question => question.n) ?? [];
    if (JSON.stringify(currentNumbers) === JSON.stringify(expectedNumbers)) {
      hostedAnchorMaps.push(path.relative(ROOT, outputPath));
      preservedHostedAnchorMaps += 1;
      continue;
    }
  }
  const hostedQuestions = buildHostedQuestions(paper);
  const maxCropPages = Math.max(3, ...hostedQuestions.map(question => {
    const pages = question.paperRegion?.map(segment => segment.p) ?? [question.pP];
    return Math.max(...pages) - Math.min(...pages);
  }));
  const artifact = {
    v: 1,
    paperFileid: paper.fileid,
    schemeFileid: '',
    component: paper.component,
    band: [1, 1],
    copyright: '© State Examinations Commission',
    paperOnly: 1,
    ...(maxCropPages > 3 ? { maxCropPages } : {}),
    q: hostedQuestions,
  };
  fs.mkdirSync(yearDir, { recursive: true });
  fs.writeFileSync(outputPath, `${JSON.stringify(artifact)}\n`);
  hostedAnchorMaps.push(path.relative(ROOT, outputPath));
  generatedHostedAnchorMaps += 1;
}

const matched = associations.filter(association => association.resolution === 'matched');
const blocked = associations.filter(association => association.resolution === 'source-blocked');
const logicalQuestions = new Set(localQuestionMappings.map(mapping => (
  `${mapping.level}|${mapping.year}|${mapping.component}|${mapping.n}`
)));
const summary = {
  referenceTopics: referenceTopics.length,
  archiveTopics: archiveTopics.length,
  totalRuntimeTopics: topics.length,
  referenceReportedAssociations: referenceTopics.reduce((sum, topic) => sum + topic.reportedQuestionCount, 0),
  referenceOfficialAssociations: associations.length,
  referenceMockAssociations: referenceTopics.reduce((sum, topic) => sum + topic.mockQuestionCount, 0),
  referenceProviderSampleAssociations: referenceTopics.reduce((sum, topic) => sum + topic.providerSampleQuestionCount, 0),
  matchedAssociations: matched.length,
  sourceBlockedAssociations: blocked.length,
  localPaperVariants: papers.length,
  localPhysicalMappings: localQuestionMappings.length,
  distinctStudentFacingQuestions: logicalQuestions.size,
  referenceMappedLocalQuestions: localQuestionMappings.filter(mapping => mapping.provenance.startsWith('reference')).length,
  retainedLocalQuestions: localQuestionMappings.filter(mapping => !mapping.provenance.startsWith('reference')).length,
  hostedPaperAnchorMaps: hostedAnchorMaps.length,
  preservedHostedAnchorMaps,
  generatedHostedAnchorMaps,
  existingAnswerSidecarMaps: existingAnswerSidecars.length,
  existingAnswerSidecarCrops,
  completeExistingAnswerSidecarMaps,
  partialExistingAnswerSidecarMaps,
  preservedBaselineVariants: baseline.length,
  preservedBaselineCards,
  newlyAddedPaperVariants: papers.length - baseline.length,
  newlyAddedPhysicalMappings: localQuestionMappings.length - preservedBaselineCards,
  emptyOfficialReferenceTopics: referenceTopics
    .filter(topic => topic.officialQuestionHeadings.length === 0)
    .map(topic => topic.id),
};

const output = {
  schemaVersion: 1,
  subjectId: 'music',
  capturedAt: reference.capturedAt,
  status: 'runtime-mapped-source-completion-pending',
  policy: {
    matchedSource: 'Entitled local State Examinations Commission corpus only.',
    excludedContent: 'No commercial mock question, solution, note, question text, image, media or provider-hosted PDF is copied.',
    fileIdentity: 'Every mapping carries the exact SEC booklet component because Music components restart question numbering under one legacy paper key.',
    historicSetWorks: 'Four retired set-work shelves per level and the Higher listening elective are explicit NextStepUni archive topics; current reference labels are never stretched across a different work.',
    practicals: 'The frozen 2013–2016 unprepared-test cards remain under the broad Practicals shelf. The reference-only 2019 section headings remain source-blocked until the matching entitled booklet is available.',
    anchorConfidence: 'All 178 paper booklets and 978 paper mappings, plus all 775 stored scheme mappings, have been visually swept. Seventeen booklets remain honest paper-only cases pending entitled question-specific evidence.',
    existingAnswerSidecars: 'Existing high-confidence answer crops remain in scripts/paper-trail/answers and are counted as independent Storage-side evidence; they are never copied into paper-only hosted anchors.',
  },
  summary,
  associations,
  localQuestionMappings,
  hostedAnchorMaps,
};
fs.writeFileSync(OUTPUT_PATH, `${JSON.stringify(output, null, 2)}\n`);
fs.writeFileSync(CURRICULUM_PATH, `${JSON.stringify(CURRICULUM_CROSSWALK, null, 2)}\n`);

const componentCode = component => ({ '006': '6', '007': '7', '008': '8', U00: 'u' })[component];
const runtimeGroups = ['higher', 'ordinary'].map(level => [
  level === 'higher' ? 'h' : 'o',
  `music-${level}`,
  level === 'higher' ? 'Higher Level' : 'Ordinary Level',
  topics.map((topic, index) => ({ topic, index })).filter(({ topic }) => topic.level === level)
    .map(({ index }) => index),
]);
const runtime = {
  v: 1,
  subjectId: 'music',
  capturedAt: reference.capturedAt,
  referenceProvider: reference.reference.provider,
  groups: runtimeGroups,
  topics: topics.map(topic => [
    topic.id,
    topic.label,
    topic.sourcePath,
    topic.mockQuestionCount,
    topic.providerSampleQuestionCount,
    CURRICULUM_CROSSWALK[topic.id],
    topic.level === 'higher' ? 'h' : 'o',
    topic.reportedQuestionCount,
    topic.archive ? 1 : 0,
  ]),
  partReferences: associations.map(association => [
    topicIndex.get(association.topicId),
    association.year - 2000,
    topicById.get(association.topicId).level === 'higher' ? 'h' : 'o',
    association.sitting === 'deferred' ? 'd' : association.sitting === 'sample' ? 'x' : 'm',
    componentCode(association.component),
    association.n,
    association.heading,
    association.resolution === 'matched'
      ? association.targets.find(target => target.lang === 'ev')?.fileid ?? association.targets[0]?.fileid ?? ''
      : '',
  ]),
  questionMappings: localQuestionMappings.map(mapping => [
    mapping.level === 'higher' ? 'h' : 'o',
    mapping.lang === 'ev' ? 'e' : 'i',
    mapping.year - 2000,
    componentCode(mapping.component),
    mapping.n,
    mapping.topicIds.map(id => topicIndex.get(id)),
  ]),
};
fs.writeFileSync(RUNTIME_PATH, `${JSON.stringify(runtime)}\n`);

console.log(JSON.stringify({
  output: path.relative(ROOT, OUTPUT_PATH),
  runtime: path.relative(ROOT, RUNTIME_PATH),
  curriculum: path.relative(ROOT, CURRICULUM_PATH),
  tags: path.relative(ROOT, TAGS_PATH),
  summary,
}, null, 2));
