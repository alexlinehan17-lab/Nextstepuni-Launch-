#!/usr/bin/env node
/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 *
 * Reconcile the metadata-only StudyClix Spanish hierarchy with NextStepUni's
 * entitled SEC corpus. The reference contributes factual labels, counts and
 * headings only; no question text, solutions, notes, media or PDFs are copied.
 *
 * The generator is additive. It starts from the frozen Spanish tag baseline,
 * incorporates every reviewed local answer sidecar, restores the omitted
 * Ordinary written-production choices from verified SEC page boundaries and
 * keeps superseded prescribed texts in one clearly labelled local extension.
 */

import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const HERE = path.dirname(fileURLToPath(import.meta.url));
const ROOT = path.resolve(HERE, '../..');
const ANSWERS_ROOT = path.join(HERE, 'answers');
const HOSTED_ROOT = path.join(ROOT, 'public/paper-anchors');
const TAGS_PATH = path.join(HERE, 'topic-tags/tags/spanish.json');
const BASELINE_PATH = path.join(ROOT, 'test/fixtures/spanishTopicQuestionBaseline.json');
const REFERENCE_PATH = path.join(ROOT, 'data/examTopics/spanish.json');
const OUTPUT_PATH = path.join(ROOT, 'data/examTopics/spanish-local-crosswalk.json');
const RUNTIME_PATH = path.join(ROOT, 'data/examTopics/spanish-runtime.json');
const CURRICULUM_PATH = path.join(ROOT, 'data/examTopics/spanish-curriculum-crosswalk.json');

const readJson = file => JSON.parse(fs.readFileSync(file, 'utf8'));
const reference = readJson(REFERENCE_PATH);
const preservationBaseline = readJson(BASELINE_PATH);

const referenceTopics = Object.entries(reference.variants).flatMap(([level, variant]) => (
  variant.topics.map(topic => ({ ...topic, level }))
));
if (referenceTopics.length !== 33) {
  throw new Error(`Expected 33 Spanish reference topics, found ${referenceTopics.length}`);
}

const HISTORIC_LITERATURE_ID = 'spanish-higher-prescribed-literature-historic-texts';
const historicLiteratureTopic = {
  id: HISTORIC_LITERATURE_ID,
  label: 'Prescribed Literature (Historic Texts)',
  groupId: 'written',
  sourcePath: '/nextstepuni/spanish/higher/written/prescribed-literature-historic-texts',
  reportedQuestionCount: 0,
  officialQuestionHeadings: [],
  mockQuestionCount: 0,
  providerSampleQuestionCount: 0,
  extractedQuestionCount: 0,
  level: 'higher',
  localExtension: true,
};
const runtimeTopics = [...referenceTopics, historicLiteratureTopic];
const topicById = new Map(runtimeTopics.map(topic => [topic.id, topic]));
const topicIndex = new Map(runtimeTopics.map((topic, index) => [topic.id, index]));

const IDS = {
  higher: {
    announcement: 'spanish-higher-aural-anuncio-announcement',
    description: 'spanish-higher-aural-descriptivo-description',
    dialogueAural: 'spanish-higher-aural-dialogo-dialogue',
    weather: 'spanish-higher-aural-el-tiempo-weather',
    news: 'spanish-higher-aural-una-noticia-news',
    oral: 'spanish-higher-oral-exam',
    role1: 'spanish-higher-role-play-1-alojamiento',
    role2: 'spanish-higher-role-play-2-el-portatil-roto',
    role3: 'spanish-higher-role-play-3-una-autocaravanacamper',
    role4: 'spanish-higher-role-play-4-el-medio-ambiente',
    role5: 'spanish-higher-role-play-5-averia-de-coche',
    journalistic: 'spanish-higher-journalistic-text',
    opinion: 'spanish-higher-opinion-text',
    prescribedCurrent: 'spanish-higher-prescribed-literature-ana-alcolea-el-medallon-perdido',
    short: 'spanish-higher-short-comprehensions',
    dialogueWritten: 'spanish-higher-write-a-dialogue',
    diaryNote: 'spanish-higher-write-a-diary-entrynote',
    letter: 'spanish-higher-write-a-letteremail',
    prescribedHistoric: HISTORIC_LITERATURE_ID,
  },
  ordinary: {
    announcement: 'spanish-ordinary-aural-anuncio-announcement',
    description: 'spanish-ordinary-aural-descriptivo-description',
    dialogueAural: 'spanish-ordinary-aural-dialogo-dialogue',
    weather: 'spanish-ordinary-aural-el-tiempo-weather',
    news: 'spanish-ordinary-aural-una-noticia-news',
    oral: 'spanish-ordinary-oral-exam',
    role1: 'spanish-ordinary-role-play-1-alojamiento',
    role2: 'spanish-ordinary-role-play-2-el-portatil-roto',
    role3: 'spanish-ordinary-role-play-3-una-autocaravanacamper',
    role4: 'spanish-ordinary-role-play-4-el-medio-ambiente',
    role5: 'spanish-ordinary-role-play-5-averia-de-coche',
    comprehension: 'spanish-ordinary-comprehension',
    diary: 'spanish-ordinary-write-a-diary-entry',
    letter: 'spanish-ordinary-write-a-letteremail',
    note: 'spanish-ordinary-write-a-note',
  },
};

const CURRICULUM_CROSSWALK = {
  [IDS.higher.announcement]: ['spanish-3-0'],
  [IDS.higher.description]: ['spanish-3-1'],
  [IDS.higher.dialogueAural]: ['spanish-3-2'],
  [IDS.higher.weather]: ['spanish-3-3', 'spanish-0-2'],
  [IDS.higher.news]: ['spanish-3-4'],
  [IDS.higher.oral]: [
    'spanish-4-0', 'spanish-0-0', 'spanish-0-1', 'spanish-0-7',
    'spanish-0-8', 'spanish-0-9',
  ],
  [IDS.higher.role1]: ['spanish-4-1', 'spanish-0-4', 'spanish-0-6'],
  [IDS.higher.role2]: ['spanish-4-2', 'spanish-0-5', 'spanish-0-6'],
  [IDS.higher.role3]: ['spanish-4-3', 'spanish-0-3', 'spanish-0-6'],
  [IDS.higher.role4]: ['spanish-4-4', 'spanish-0-6', 'spanish-2-4'],
  [IDS.higher.role5]: ['spanish-4-5', 'spanish-0-3', 'spanish-0-5', 'spanish-0-6'],
  [IDS.higher.journalistic]: ['spanish-5-0', 'spanish-1-0', 'spanish-2-0'],
  [IDS.higher.opinion]: ['spanish-5-0', 'spanish-1-1', 'spanish-1-2', 'spanish-6-0'],
  [IDS.higher.prescribedCurrent]: ['spanish-2-1', 'spanish-7-0'],
  [IDS.higher.short]: ['spanish-5-1', 'spanish-1-0'],
  [IDS.higher.dialogueWritten]: ['spanish-6-1', 'spanish-0-8'],
  [IDS.higher.diaryNote]: ['spanish-6-3', 'spanish-1-3'],
  [IDS.higher.letter]: ['spanish-6-2', 'spanish-1-3'],
  [IDS.higher.prescribedHistoric]: [
    'spanish-2-1', 'spanish-7-1', 'spanish-7-2', 'spanish-7-3',
  ],
  [IDS.ordinary.announcement]: ['spanish-3-0'],
  [IDS.ordinary.description]: ['spanish-3-1'],
  [IDS.ordinary.dialogueAural]: ['spanish-3-2'],
  [IDS.ordinary.weather]: ['spanish-3-3', 'spanish-0-2'],
  [IDS.ordinary.news]: ['spanish-3-4'],
  [IDS.ordinary.oral]: [
    'spanish-4-0', 'spanish-0-0', 'spanish-0-1', 'spanish-0-7',
    'spanish-0-8', 'spanish-0-9',
  ],
  [IDS.ordinary.role1]: ['spanish-4-1', 'spanish-0-4', 'spanish-0-6'],
  [IDS.ordinary.role2]: ['spanish-4-2', 'spanish-0-5', 'spanish-0-6'],
  [IDS.ordinary.role3]: ['spanish-4-3', 'spanish-0-3', 'spanish-0-6'],
  [IDS.ordinary.role4]: ['spanish-4-4', 'spanish-0-6', 'spanish-2-4'],
  [IDS.ordinary.role5]: ['spanish-4-5', 'spanish-0-3', 'spanish-0-5', 'spanish-0-6'],
  [IDS.ordinary.comprehension]: ['spanish-5-2', 'spanish-1-0'],
  [IDS.ordinary.diary]: ['spanish-6-3', 'spanish-1-3'],
  [IDS.ordinary.letter]: ['spanish-6-2', 'spanish-1-3'],
  [IDS.ordinary.note]: ['spanish-6-4', 'spanish-0-10'],
};

for (const topic of runtimeTopics) {
  if (!CURRICULUM_CROSSWALK[topic.id]?.length) {
    throw new Error(`Spanish topic has no curriculum bridge: ${topic.id}`);
  }
}

const paperKind = fileid => /PA00[EI]V\.pdf$/i.test(fileid) ? 'aural' : 'written';
const paperIdentity = paper => [paper.level, paper.lang, paper.year, paper.fileid].join('|');
const paperMap = new Map();
for (const source of preservationBaseline) {
  const paper = {
    subjectId: 'spanish',
    level: source.level,
    lang: source.lang,
    year: source.year,
    fileid: source.fileid,
    paperKey: source.paperKey,
    kind: paperKind(source.fileid),
    q: source.questions.map(question => ({ ...question, baseline: true })),
    answerMap: null,
  };
  const identity = paperIdentity(paper);
  if (paperMap.has(identity)) throw new Error(`Duplicate Spanish baseline paper: ${identity}`);
  paperMap.set(identity, paper);
}

const parseSidecarIdentity = file => {
  const match = file.match(/^LC012([AG])L(P000|PA00)([EI])V\.pdf\.json$/i);
  if (!match) throw new Error(`Unexpected Spanish answer-map filename: ${file}`);
  return {
    level: match[1].toUpperCase() === 'A' ? 'higher' : 'ordinary',
    lang: match[3].toUpperCase() === 'I' ? 'iv' : 'ev',
    fileid: file.slice(0, -'.json'.length),
    kind: match[2].toUpperCase() === 'PA00' ? 'aural' : 'written',
  };
};

const auralSemanticFromCanonical = primary => ({
  'spanish-3-0': 'aural-announcement',
  'spanish-3-1': 'aural-description',
  'spanish-3-2': 'aural-dialogue',
  'spanish-3-3': 'aural-weather',
  'spanish-3-4': 'aural-news',
}[primary] ?? null);

const writtenSemanticFromCanonical = question => {
  if (question.primary === 'spanish-2-1') {
    return question.secondary === 'spanish-7-0'
      ? 'higher-prescribed-current'
      : 'higher-prescribed-historic';
  }
  if (question.primary === 'spanish-5-1') return 'higher-short';
  if (question.primary === 'spanish-5-0' && question.secondary === 'spanish-1-1') {
    return 'higher-opinion';
  }
  if (question.primary === 'spanish-5-0') return 'higher-journalistic';
  if (/^spanish-6-/.test(question.primary ?? '')) return 'higher-writing-all';
  return null;
};

const auralSemanticFromNumber = number => {
  if (number === '1') return 'aural-announcement';
  if (number === '2' || number === '3') return 'aural-dialogue';
  if (number === '4' || number === '5') return 'aural-description';
  if (number === '6') return 'aural-weather';
  if (number === '7') return 'aural-news';
  throw new Error(`Unknown Spanish aural question number: ${number}`);
};

const semanticForSidecar = (paper, question, answerQuestion) => {
  if (paper.kind === 'aural') {
    return auralSemanticFromCanonical(question.primary) ?? auralSemanticFromNumber(answerQuestion.n);
  }
  if (paper.level === 'ordinary') return 'ordinary-comprehension';

  const label = String(answerQuestion.label ?? '');
  // The 2011 and 2013 Higher Irish answer maps pre-date display labels. Their
  // SEC booklets were re-opened during this reconciliation: zero-based paper
  // page 1 is the prescribed-literature choice and page 3 is the alternative
  // journalistic-text choice. Keep those reviewed cards rather than excluding
  // the two sidecar-only variants.
  if (!label && paper.lang === 'iv' && [2011, 2013].includes(paper.year)) {
    if (answerQuestion.pP === 1) return 'higher-prescribed-historic';
    if (answerQuestion.pP === 3) return 'higher-journalistic';
  }
  if (/(?:Section|Sec|Roinn)\s*C|Written production|Scríbhneoireacht/i.test(label)) {
    return 'higher-writing-all';
  }
  if (/(?:Section|Sec|Roinn)\s*B/i.test(label)) return 'higher-opinion';
  if (/Short Comprehension|téacsanna gearra|(?:Q|Question|Ceist)\s*2\b/i.test(label)) {
    return 'higher-short';
  }
  if (/Journalistic|Iriseoireachta|Q1\s*\(b\)|Ceist\s*1\s*\(b\)/i.test(label)) {
    return 'higher-journalistic';
  }
  if (/Prescribed Literature|Literary text|Litríocht|Q1\s*\(a\)|Ceist\s*1\s*\(a\)/i.test(label)) {
    return paper.year === 2026 ? 'higher-prescribed-current' : 'higher-prescribed-historic';
  }
  // Some reviewed sidecars intentionally contain no display labels. Their
  // frozen canonical tags still identify the card, so use that preserved
  // metadata only after the more specific bilingual label evidence above.
  const canonicalSemantic = writtenSemanticFromCanonical(question);
  if (canonicalSemantic) return canonicalSemantic;
  throw new Error(`${paperIdentity(paper)} Q${answerQuestion.n}: unknown Spanish card label ${label}`);
};

const literatureCanonical = year => {
  if (year <= 2013) return 'spanish-7-2';
  if (year <= 2020) return 'spanish-7-3';
  if (year <= 2025) return 'spanish-7-1';
  return 'spanish-7-0';
};

const canonicalForSemantic = (semantic, year) => {
  if (semantic === 'aural-announcement') return { primary: 'spanish-3-0' };
  if (semantic === 'aural-description') return { primary: 'spanish-3-1' };
  if (semantic === 'aural-dialogue') return { primary: 'spanish-3-2' };
  if (semantic === 'aural-weather') return { primary: 'spanish-3-3' };
  if (semantic === 'aural-news') return { primary: 'spanish-3-4' };
  if (semantic === 'higher-prescribed-current' || semantic === 'higher-prescribed-historic') {
    return { primary: 'spanish-2-1', secondary: literatureCanonical(year) };
  }
  if (semantic === 'higher-journalistic') return { primary: 'spanish-5-0' };
  if (semantic === 'higher-short') return { primary: 'spanish-5-1' };
  if (semantic === 'higher-opinion') return { primary: 'spanish-5-0', secondary: 'spanish-1-1' };
  if (semantic === 'higher-writing-all') return { primary: 'spanish-6-1', secondary: 'spanish-6-2' };
  if (semantic === 'ordinary-comprehension') return { primary: 'spanish-5-2' };
  if (semantic === 'ordinary-writing-letter') return { primary: 'spanish-6-2' };
  if (semantic === 'ordinary-writing-note') return { primary: 'spanish-6-4' };
  if (semantic === 'ordinary-writing-diary') return { primary: 'spanish-6-3' };
  throw new Error(`No canonical Spanish tag for semantic card ${semantic}`);
};

const sidecarFiles = fs.readdirSync(ANSWERS_ROOT, { withFileTypes: true })
  .filter(entry => entry.isDirectory() && /^20\d\d$/.test(entry.name))
  .flatMap(entry => fs.readdirSync(path.join(ANSWERS_ROOT, entry.name))
    .filter(file => /^LC012.*\.pdf\.json$/i.test(file))
    .map(file => ({ year: Number(entry.name), file })))
  .sort((a, b) => a.year - b.year || a.file.localeCompare(b.file));

for (const { year, file } of sidecarFiles) {
  const parsed = parseSidecarIdentity(file);
  const candidate = {
    subjectId: 'spanish', year, ...parsed, paperKey: 'single', q: [], answerMap: null,
  };
  const identity = paperIdentity(candidate);
  const paper = paperMap.get(identity) ?? candidate;
  const answerMap = readJson(path.join(ANSWERS_ROOT, String(year), file));
  paper.answerMap = answerMap;

  for (const answerQuestion of answerMap.q) {
    let question = paper.q.find(item => item.n === answerQuestion.n);
    if (!question) {
      question = { n: answerQuestion.n };
      paper.q.push(question);
    }
    question.label = answerQuestion.label ?? question.label;
    question.anchor = answerQuestion;
    question.semantic = semanticForSidecar(paper, question, answerQuestion);
    if (!question.primary) Object.assign(question, canonicalForSemantic(question.semantic, year));
  }

  const duplicateNumbers = paper.q
    .map(question => question.n)
    .filter((number, index, numbers) => numbers.indexOf(number) !== index);
  if (duplicateNumbers.length) throw new Error(`${identity}: duplicate cards ${duplicateNumbers.join(', ')}`);
  paperMap.set(identity, paper);
}

// The November 2020 Ordinary Irish aural paper has a reviewed, committed
// paper-only map but no classic scheme sidecar. Keep its frozen cards and use
// that existing map as their verified paper anchor source.
for (const paper of paperMap.values()) {
  if (paper.answerMap || paper.kind !== 'aural') continue;
  const hostedPath = path.join(HOSTED_ROOT, String(paper.year), `${paper.fileid}.json`);
  if (!fs.existsSync(hostedPath)) {
    throw new Error(`${paperIdentity(paper)}: frozen paper has no local anchor source`);
  }
  const hosted = readJson(hostedPath);
  for (const question of paper.q) {
    const anchor = hosted.q.find(item => item.n === question.n);
    if (!anchor) throw new Error(`${paperIdentity(paper)} Q${question.n}: hosted anchor missing`);
    question.anchor = anchor;
    question.label = anchor.label ?? `Question ${question.n}`;
    question.semantic = auralSemanticFromCanonical(question.primary) ?? auralSemanticFromNumber(question.n);
  }
}

const fullPages = (start, end = start) => Array.from(
  { length: end - start + 1 },
  (_, offset) => ({ p: start + offset, r: [0, 0, 1, 1] }),
);

const customQuestion = ({ n, label, semantic, page, pageEnd = page, year }) => ({
  n,
  label,
  semantic,
  ...canonicalForSemantic(semantic, year),
  anchor: { n, label, pP: page, pY: [0, 1], paperRegion: fullPages(page, pageEnd) },
});

const addCustom = (paper, spec) => {
  if (paper.q.some(question => question.n === spec.n)) {
    throw new Error(`${paperIdentity(paper)}: custom card ${spec.n} already exists`);
  }
  paper.q.push(customQuestion({ ...spec, year: paper.year }));
};

const findPaper = (year, level, lang, kind) => {
  const matches = [...paperMap.values()].filter(paper => (
    paper.year === year && paper.level === level && paper.lang === lang && paper.kind === kind
  ));
  if (matches.length !== 1) {
    throw new Error(`${year} ${level} ${lang} ${kind}: expected one Spanish paper, found ${matches.length}`);
  }
  return matches[0];
};

// Restore the sole missing indexed variant (2020 Ordinary Irish written).
// The English and Irish official booklets have matching 12-page layouts; the
// five reading boundaries are copied from the reviewed English paper map.
{
  const source = findPaper(2020, 'ordinary', 'ev', 'written');
  const paper = {
    subjectId: 'spanish',
    level: 'ordinary',
    lang: 'iv',
    year: 2020,
    fileid: 'LC012GLP000IV.pdf',
    paperKey: 'single',
    kind: 'written',
    q: source.q.map(question => ({
      n: question.n,
      label: `Roinn A · Ceist ${question.n}`,
      semantic: 'ordinary-comprehension',
      ...canonicalForSemantic('ordinary-comprehension', 2020),
      anchor: {
        n: question.n,
        label: `Roinn A · Ceist ${question.n}`,
        pP: question.anchor.pP,
        pY: question.anchor.pY,
        paperRegion: fullPages(question.anchor.pP),
      },
    })),
    answerMap: null,
  };
  const identity = paperIdentity(paper);
  if (paperMap.has(identity)) throw new Error(`Unexpected existing Spanish paper: ${identity}`);
  paperMap.set(identity, paper);
}

const ordinaryWritingPages = year => {
  if (year <= 2018) return { letter: 6, choice: 7 };
  if (year === 2019) return { letter: 7, choice: 8 };
  if (year === 2020) return { letter: 8, choice: 9 };
  if (year === 2021) return { letter: 10, choice: 12 };
  return { letter: 12, choice: 14 };
};

// The classic Ordinary maps stop at the end of Section A. Both official-
// language editions were checked: these pages contain Q1 Letter/Email and the
// Q2(a) Note / Q2(b) Diary choice in every 2010-2026 booklet.
for (let year = 2010; year <= 2026; year++) {
  const pages = ordinaryWritingPages(year);
  for (const lang of ['ev', 'iv']) {
    const paper = findPaper(year, 'ordinary', lang, 'written');
    addCustom(paper, {
      n: 'B1', label: 'Section B · Question 1 · Letter / Email',
      semantic: 'ordinary-writing-letter', page: pages.letter,
    });
    addCustom(paper, {
      n: 'B2A', label: 'Section B · Question 2(a) · Note',
      semantic: 'ordinary-writing-note', page: pages.choice,
    });
    addCustom(paper, {
      n: 'B2B', label: 'Section B · Question 2(b) · Diary Entry',
      semantic: 'ordinary-writing-diary', page: pages.choice,
    });
  }
}

// A few legacy language-edition sidecars omit a whole component even though
// the indexed SEC booklet contains it. Both editions share their page layout,
// so restore one umbrella card from the reviewed sibling edition's boundaries.
// This covers 2011/2013 Irish A2+B, 2016 English B and 2022 English A2.
const restoreMissingHigherSection = ({ semantic, n, label, nextSemantic }) => {
  for (const paper of paperMap.values()) {
    if (paper.kind !== 'written' || paper.level !== 'higher') continue;
    if (paper.q.some(question => question.semantic === semantic)) continue;
    const sibling = [...paperMap.values()].find(candidate => (
      candidate.year === paper.year
      && candidate.level === paper.level
      && candidate.kind === paper.kind
      && candidate.lang !== paper.lang
    ));
    const siblingCards = sibling?.q.filter(question => question.semantic === semantic) ?? [];
    if (!siblingCards.length) {
      throw new Error(`${paperIdentity(paper)}: neither language edition maps ${semantic}`);
    }
    const pages = siblingCards.map(question => question.anchor?.pP).filter(Number.isFinite);
    if (!pages.length) throw new Error(`${paperIdentity(paper)}: ${semantic} sibling has no page`);
    const page = Math.min(...pages);
    let pageEnd = Math.max(...pages);
    if (siblingCards.length === 1 && nextSemantic) {
      const nextPages = sibling.q
        .filter(question => question.semantic === nextSemantic)
        .map(question => question.anchor?.pP)
        .filter(Number.isFinite);
      if (nextPages.length) pageEnd = Math.max(page, Math.min(...nextPages) - 1);
    }
    addCustom(paper, { n, label, semantic, page, pageEnd });
  }
};

restoreMissingHigherSection({
  semantic: 'higher-short',
  n: 'A2',
  label: 'Section A · Question 2 · Short Comprehensions',
  nextSemantic: 'higher-opinion',
});
restoreMissingHigherSection({
  semantic: 'higher-opinion',
  n: 'B',
  label: 'Section B · Opinion Text · Questions 1–5',
  nextSemantic: 'higher-writing-all',
});

const localPapers = [...paperMap.values()].sort((a, b) => (
  b.year - a.year
  || a.level.localeCompare(b.level)
  || a.lang.localeCompare(b.lang)
  || a.fileid.localeCompare(b.fileid)
));

let preservedBaselineCards = 0;
for (const expected of preservationBaseline) {
  const paper = paperMap.get(paperIdentity(expected));
  if (!paper) throw new Error(`Preservation failure: missing ${paperIdentity(expected)}`);
  for (const expectedQuestion of expected.questions) {
    const actual = paper.q.find(question => question.n === expectedQuestion.n);
    if (!actual) throw new Error(`Preservation failure: ${paperIdentity(expected)} Q${expectedQuestion.n}`);
    const compact = {
      n: actual.n,
      primary: actual.primary,
      ...(actual.secondary ? { secondary: actual.secondary } : {}),
    };
    if (JSON.stringify(compact) !== JSON.stringify(expectedQuestion)) {
      throw new Error(`Preservation failure: changed ${paperIdentity(expected)} Q${expectedQuestion.n}`);
    }
    preservedBaselineCards += 1;
  }
}

const parseYear = heading => {
  const year = Number(heading.match(/^(\d{4})/)?.[1]);
  if (!year) throw new Error(`Spanish heading has no year: ${heading}`);
  return year;
};
const referenceNumber = heading => heading.match(/Question\s+(\d+)/i)?.[1] ?? '1';
const topicSemantic = topicId => {
  const pairs = new Map([
    [IDS.higher.announcement, 'aural-announcement'],
    [IDS.higher.description, 'aural-description'],
    [IDS.higher.dialogueAural, 'aural-dialogue'],
    [IDS.higher.weather, 'aural-weather'],
    [IDS.higher.news, 'aural-news'],
    [IDS.higher.journalistic, 'higher-journalistic'],
    [IDS.higher.opinion, 'higher-opinion'],
    [IDS.higher.prescribedCurrent, 'higher-prescribed-current'],
    [IDS.higher.short, 'higher-short'],
    [IDS.higher.dialogueWritten, 'higher-writing-all'],
    [IDS.higher.diaryNote, 'higher-writing-all'],
    [IDS.higher.letter, 'higher-writing-all'],
    [IDS.ordinary.announcement, 'aural-announcement'],
    [IDS.ordinary.description, 'aural-description'],
    [IDS.ordinary.dialogueAural, 'aural-dialogue'],
    [IDS.ordinary.weather, 'aural-weather'],
    [IDS.ordinary.news, 'aural-news'],
    [IDS.ordinary.comprehension, 'ordinary-comprehension'],
    [IDS.ordinary.diary, 'ordinary-writing-diary'],
    [IDS.ordinary.letter, 'ordinary-writing-letter'],
    [IDS.ordinary.note, 'ordinary-writing-note'],
  ]);
  return pairs.get(topicId) ?? null;
};

const resolveHeading = (topic, heading) => {
  const year = parseYear(heading);
  const sitting = /Deferred/i.test(heading) ? 'deferred' : 'main';
  const kind = topic.groupId === 'aural' ? 'aural' : topic.groupId === 'written' ? 'written' : 'oral';
  const blocked = (reason) => ({
    topicId: topic.id, heading, year, sitting, paperKey: kind, resolution: 'source-blocked', reason,
  });
  if (year < 2010) {
    return blocked('The entitled local SEC question corpus begins in 2010. The factual heading is retained, but no StudyClix-hosted question, solution, image or PDF is copied.');
  }
  if (sitting === 'deferred') {
    return blocked('The factual deferred-paper heading is retained, but the corresponding entitled deferred booklet is not present in the local corpus.');
  }
  if (kind === 'oral') {
    return blocked('The factual official role-play heading is retained, but the published oral booklet is not present in the local Paper Trail corpus.');
  }
  const paper = findPaper(year, topic.level, 'ev', kind);
  const semantic = topicSemantic(topic.id);
  let candidates = paper.q.filter(question => question.semantic === semantic);
  if (kind === 'aural') {
    const printed = referenceNumber(heading);
    const exact = candidates.filter(question => question.n === printed);
    if (exact.length) candidates = exact;
  }
  if (!candidates.length) {
    throw new Error(`${topic.id}: no local Spanish card resolves ${heading}`);
  }
  return {
    topicId: topic.id,
    heading,
    year,
    sitting,
    paperKey: kind,
    resolution: 'matched',
    target: {
      level: paper.level,
      lang: paper.lang,
      paperKey: paper.paperKey,
      kind: paper.kind,
      fileid: paper.fileid,
      questionNumbers: candidates.map(question => question.n),
    },
  };
};

const associations = referenceTopics.flatMap(topic => (
  topic.officialQuestionHeadings.map(heading => resolveHeading(topic, heading))
));
const matched = associations.filter(association => association.resolution === 'matched');
const sourceBlocked = associations.filter(association => association.resolution === 'source-blocked');
if (associations.length !== 471) {
  throw new Error(`Spanish reference boundary mismatch: ${associations.length} associations`);
}

const localQuestionIdentity = (paper, number) => [
  paper.level, paper.lang, paper.year, paper.fileid, number,
].join('|');
const referenceTopicsByLocalQuestion = new Map();
for (const association of matched) {
  for (const number of association.target.questionNumbers) {
    const key = [
      association.target.level,
      association.target.lang,
      association.year,
      association.target.fileid,
      number,
    ].join('|');
    const ids = referenceTopicsByLocalQuestion.get(key) ?? [];
    if (!ids.includes(association.topicId)) ids.push(association.topicId);
    referenceTopicsByLocalQuestion.set(key, ids);
  }
}

const fallbackTopicIds = (paper, question) => {
  const levelIds = paper.level === 'higher' ? IDS.higher : IDS.ordinary;
  if (question.semantic === 'aural-announcement') return [levelIds.announcement];
  if (question.semantic === 'aural-description') return [levelIds.description];
  if (question.semantic === 'aural-dialogue') return [levelIds.dialogueAural];
  if (question.semantic === 'aural-weather') return [levelIds.weather];
  if (question.semantic === 'aural-news') return [levelIds.news];
  if (question.semantic === 'higher-prescribed-current') return [IDS.higher.prescribedCurrent];
  if (question.semantic === 'higher-prescribed-historic') return [IDS.higher.prescribedHistoric];
  if (question.semantic === 'higher-journalistic') return [IDS.higher.journalistic];
  if (question.semantic === 'higher-opinion') return [IDS.higher.opinion];
  if (question.semantic === 'higher-short') return [IDS.higher.short];
  if (question.semantic === 'higher-writing-all') {
    return [IDS.higher.dialogueWritten, IDS.higher.diaryNote, IDS.higher.letter];
  }
  if (question.semantic === 'ordinary-comprehension') return [IDS.ordinary.comprehension];
  if (question.semantic === 'ordinary-writing-letter') return [IDS.ordinary.letter];
  if (question.semantic === 'ordinary-writing-note') return [IDS.ordinary.note];
  if (question.semantic === 'ordinary-writing-diary') return [IDS.ordinary.diary];
  throw new Error(`${paperIdentity(paper)} Q${question.n}: no Spanish fallback for ${question.semantic}`);
};

const localQuestionMappings = localPapers.flatMap(paper => paper.q.map(question => {
  const referenced = referenceTopicsByLocalQuestion.get(localQuestionIdentity(paper, question.n)) ?? [];
  const fallback = fallbackTopicIds(paper, question);
  const topicIds = [...new Set([...referenced, ...fallback])]
    .sort((a, b) => topicIndex.get(a) - topicIndex.get(b));
  if (!topicIds.length || topicIds.some(id => !topicById.has(id))) {
    throw new Error(`${paperIdentity(paper)} Q${question.n}: invalid topic mapping ${topicIds.join(', ')}`);
  }
  if (topicIds.some(id => topicById.get(id).level !== paper.level)) {
    throw new Error(`${paperIdentity(paper)} Q${question.n}: cross-level topic mapping`);
  }
  return {
    level: paper.level,
    lang: paper.lang,
    year: paper.year,
    fileid: paper.fileid,
    paperKey: paper.paperKey,
    kind: paper.kind,
    n: question.n,
    topicIds,
    provenance: referenced.length
      ? fallback.some(id => !referenced.includes(id)) ? 'reference+retained-local' : 'reference'
      : question.semantic === 'higher-prescribed-historic'
        ? 'retained-local-historic-literature'
        : 'retained-local',
  };
}));

const duplicateMappings = localQuestionMappings
  .map(mapping => [mapping.level, mapping.lang, mapping.year, mapping.fileid, mapping.n].join('|'))
  .filter((identity, index, identities) => identities.indexOf(identity) !== index);
if (duplicateMappings.length) {
  throw new Error(`Duplicate Spanish local mappings: ${[...new Set(duplicateMappings)].join(', ')}`);
}

const tagPapers = localPapers.map(paper => ({
  subjectId: 'spanish',
  level: paper.level,
  lang: paper.lang,
  year: paper.year,
  fileid: paper.fileid,
  paperKey: paper.paperKey,
  q: paper.q.map(question => ({
    n: question.n,
    primary: question.primary,
    ...(question.secondary ? { secondary: question.secondary } : {}),
  })),
}));
fs.writeFileSync(TAGS_PATH, `${JSON.stringify(tagPapers, null, 2)}\n`);

const hostedQuestion = (question, index, paper) => {
  const source = question.anchor;
  if (!source || !Number.isFinite(source.pP) || !Array.isArray(source.pY)) {
    throw new Error(`${paperIdentity(paper)} Q${question.n}: missing verified paper anchor`);
  }
  const paperRegion = source.paperRegion ?? fullPages(source.pP);
  return {
    n: question.n,
    label: question.label ?? `Question ${question.n}`,
    printOrder: index + 1,
    pP: source.pP,
    pY: source.pY,
    paperRegion,
    region: [{ p: 1 }],
    mode: 'pagejump',
    conf: 0.5,
  };
};

const hostedAnchorMaps = [];
for (const paper of localPapers) {
  const artifact = {
    v: 1,
    paperFileid: paper.fileid,
    schemeFileid: '',
    component: paper.kind === 'aural' ? 'A00' : '000',
    band: [1, 1],
    copyright: '© State Examinations Commission',
    paperOnly: 1,
    q: paper.q.map((question, index) => hostedQuestion(question, index, paper)),
  };
  const yearDir = path.join(HOSTED_ROOT, String(paper.year));
  fs.mkdirSync(yearDir, { recursive: true });
  const outputPath = path.join(yearDir, `${paper.fileid}.json`);
  fs.writeFileSync(outputPath, `${JSON.stringify(artifact)}\n`);
  hostedAnchorMaps.push(path.relative(ROOT, outputPath));
}

const logicalQuestions = new Set(localQuestionMappings.map(mapping => [
  mapping.level, mapping.year, mapping.kind, mapping.n,
].join('|')));
const blockedByReason = sourceBlocked.reduce((counts, association) => {
  const key = association.year < 2010
    ? 'preCorpus'
    : association.sitting === 'deferred'
      ? 'deferred'
      : 'oralBooklet';
  counts[key] = (counts[key] ?? 0) + 1;
  return counts;
}, {});
const summary = {
  referenceTopics: referenceTopics.length,
  runtimeTopics: runtimeTopics.length,
  localExtensionTopics: 1,
  referenceReportedAssociations: referenceTopics.reduce((sum, topic) => sum + topic.reportedQuestionCount, 0),
  referenceOfficialAssociations: associations.length,
  referenceMockAssociations: referenceTopics.reduce((sum, topic) => sum + topic.mockQuestionCount, 0),
  referenceProviderSampleAssociations: referenceTopics.reduce((sum, topic) => sum + topic.providerSampleQuestionCount, 0),
  matchedAssociations: matched.length,
  sourceBlockedAssociations: sourceBlocked.length,
  sourceBlockedByReason: blockedByReason,
  matchedLocalCardLinks: matched.reduce((sum, association) => sum + association.target.questionNumbers.length, 0),
  localPaperVariants: localPapers.length,
  localPhysicalMappings: localQuestionMappings.length,
  distinctStudentFacingQuestions: logicalQuestions.size,
  referenceMappedLocalQuestions: localQuestionMappings.filter(mapping => mapping.provenance.startsWith('reference')).length,
  retainedLocalQuestions: localQuestionMappings.filter(mapping => !mapping.provenance.startsWith('reference')).length,
  hostedPaperAnchorMaps: hostedAnchorMaps.length,
  preservedBaselineVariants: preservationBaseline.length,
  preservedBaselineCards,
  newlyAddedPaperVariants: localPapers.length - preservationBaseline.length,
  newlyAddedPhysicalMappings: localQuestionMappings.length - preservedBaselineCards,
  emptyReferenceTopics: referenceTopics.filter(topic => topic.reportedQuestionCount === 0).map(topic => topic.id),
};

const output = {
  schemaVersion: 1,
  subjectId: 'spanish',
  capturedAt: reference.capturedAt,
  policy: {
    matchedSource: 'Entitled local State Examinations Commission corpus only.',
    excludedContent: 'No commercial mock question, solution, note, question text, StudyClix image or StudyClix-hosted PDF is copied.',
    historicalLiterature: 'Superseded prescribed-text cards remain available in one explicit local Historic Texts bucket and are never mislabeled as the current Ana Alcolea text.',
    ordinaryWriting: 'The restored 2010-2026 Letter, Note and Diary cards use page boundaries checked in both official-language SEC booklets.',
  },
  summary,
  associations,
  localQuestionMappings,
  hostedAnchorMaps,
};
fs.writeFileSync(OUTPUT_PATH, `${JSON.stringify(output, null, 2)}\n`);
fs.writeFileSync(CURRICULUM_PATH, `${JSON.stringify(CURRICULUM_CROSSWALK, null, 2)}\n`);

const kindCode = kind => kind === 'aural' ? 'a' : kind === 'oral' ? 'o' : 'w';
const sittingCode = sitting => sitting === 'deferred' ? 'd' : 'm';
const runtimePartReferences = associations.flatMap(association => {
  const index = topicIndex.get(association.topicId);
  if (association.resolution === 'matched') {
    return association.target.questionNumbers.map(number => [
      index,
      association.year - 2000,
      association.target.level === 'higher' ? 'h' : 'o',
      kindCode(association.target.kind),
      sittingCode(association.sitting),
      number,
      association.heading,
    ]);
  }
  const topic = topicById.get(association.topicId);
  return [[
    index,
    association.year - 2000,
    topic.level === 'higher' ? 'h' : 'o',
    kindCode(association.paperKey),
    sittingCode(association.sitting),
    referenceNumber(association.heading),
    association.heading,
  ]];
});

const runtimeGroups = Object.entries(reference.variants).flatMap(([level, variant]) => (
  variant.groups.map(group => {
    const ids = variant.topics
      .filter(topic => topic.groupId === group.id)
      .map(topic => topic.id);
    if (level === 'higher' && group.id === 'written') ids.push(HISTORIC_LITERATURE_ID);
    return [
      level === 'higher' ? 'h' : 'o',
      group.id,
      group.label,
      ids.map(id => topicIndex.get(id)),
    ];
  })
));

const runtime = {
  v: 1,
  subjectId: 'spanish',
  capturedAt: reference.capturedAt,
  referenceProvider: reference.reference.provider,
  groups: runtimeGroups,
  topics: runtimeTopics.map(topic => [
    topic.id,
    topic.label,
    topic.sourcePath,
    topic.mockQuestionCount,
    topic.providerSampleQuestionCount,
    CURRICULUM_CROSSWALK[topic.id],
    topic.level === 'higher' ? 'h' : 'o',
    topic.reportedQuestionCount,
  ]),
  partReferences: runtimePartReferences,
  questionMappings: localQuestionMappings.map(mapping => [
    mapping.level === 'higher' ? 'h' : 'o',
    mapping.lang === 'ev' ? 'e' : 'i',
    mapping.year - 2000,
    kindCode(mapping.kind),
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
  ...summary,
}, null, 2));
