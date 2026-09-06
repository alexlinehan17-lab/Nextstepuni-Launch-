#!/usr/bin/env node
/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 *
 * Reconcile the metadata-only StudyClix French hierarchy with NextStepUni's
 * entitled SEC corpus. The reference contributes factual labels, counts and
 * headings only; no question text, solutions, notes, media or PDFs are copied.
 *
 * The generator is additive. It starts from the frozen French tag baseline,
 * incorporates every usable reviewed local answer sidecar, restores omitted
 * official reading and written-production cards from checked SEC page
 * boundaries, and preserves every pre-migration question identity verbatim.
 */

import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const HERE = path.dirname(fileURLToPath(import.meta.url));
const ROOT = path.resolve(HERE, '../..');
const ANSWERS_ROOT = path.join(HERE, 'answers');
const HOSTED_ROOT = path.join(ROOT, 'public/paper-anchors');
const TAGS_PATH = path.join(HERE, 'topic-tags/tags/french.json');
const BASELINE_PATH = path.join(ROOT, 'test/fixtures/frenchTopicQuestionBaseline.json');
const REFERENCE_PATH = path.join(ROOT, 'data/examTopics/french.json');
const OUTPUT_PATH = path.join(ROOT, 'data/examTopics/french-local-crosswalk.json');
const RUNTIME_PATH = path.join(ROOT, 'data/examTopics/french-runtime.json');
const CURRICULUM_PATH = path.join(ROOT, 'data/examTopics/french-curriculum-crosswalk.json');

const readJson = file => JSON.parse(fs.readFileSync(file, 'utf8'));
const reference = readJson(REFERENCE_PATH);
const preservationBaseline = readJson(BASELINE_PATH);
const referenceTopics = Object.entries(reference.variants).flatMap(([level, variant]) => (
  variant.topics.map(topic => ({ ...topic, level }))
));
if (referenceTopics.length !== 33) {
  throw new Error(`Expected 33 French reference topics, found ${referenceTopics.length}`);
}

const topicById = new Map(referenceTopics.map(topic => [topic.id, topic]));
const topicIndex = new Map(referenceTopics.map((topic, index) => [topic.id, index]));
const topicByLabel = new Map(referenceTopics.map(topic => [`${topic.level}|${topic.label}`, topic.id]));
const topicId = (level, label) => {
  const id = topicByLabel.get(`${level}|${label}`);
  if (!id) throw new Error(`Missing French reference topic: ${level} · ${label}`);
  return id;
};

const H = {
  conversation: topicId('higher', 'AURAL - Conversation'),
  interview: topicId('higher', 'AURAL - Interview'),
  news: topicId('higher', 'AURAL - News Pieces'),
  literary: topicId('higher', 'Literary/Novel Comprehension'),
  newspaper: topicId('higher', 'Newspaper/Magazine Comprehension'),
  animals: topicId('higher', 'Opinion - Animals, Nature and the Environment'),
  education: topicId('higher', 'Opinion - Education'),
  health: topicId('higher', 'Opinion - Health'),
  travel: topicId('higher', 'Opinion - Ireland, Travel, Tourism and Culture'),
  politics: topicId('higher', 'Opinion - Politics, Social Issues and Equality'),
  sport: topicId('higher', 'Opinion - Sport'),
  technology: topicId('higher', 'Opinion - Technology and Media'),
  youth: topicId('higher', 'Opinion - Youth, Teenagers and Families'),
  oral: topicId('higher', 'ORAL Exam'),
  diary: topicId('higher', 'Write a Diary...'),
  letter: topicId('higher', 'Write a Letter...'),
  note: topicId('higher', 'Write a Note...'),
  email: topicId('higher', 'Write an Email...'),
  recit: topicId('higher', 'Written Production (récit)'),
};
const O = {
  conversation: topicId('ordinary', 'AURAL - Conversation'),
  interview: topicId('ordinary', 'AURAL - Interview'),
  news: topicId('ordinary', 'AURAL - News Pieces'),
  form: topicId('ordinary', 'Fill in a Form...'),
  gaps: topicId('ordinary', 'Fill in the Gaps...'),
  oral: topicId('ordinary', 'ORAL exam'),
  article: topicId('ordinary', 'Reading Comprehension - Article'),
  book: topicId('ordinary', 'Reading Comprehension - Book Extract'),
  readingInterview: topicId('ordinary', 'Reading Comprehension - Interview'),
  otherReading: topicId('ordinary', 'Reading Comprehension - Other Website & Magazine Extracts'),
  diary: topicId('ordinary', 'Write a Diary...'),
  letter: topicId('ordinary', 'Write a Letter...'),
  message: topicId('ordinary', 'Write a Message...'),
  postcard: topicId('ordinary', 'Write a Postcard...'),
};

const CURRICULUM_CROSSWALK = {
  [H.conversation]: ['french-3-0'],
  [H.interview]: ['french-3-1'],
  [H.news]: ['french-3-2'],
  [H.literary]: ['french-5-1', 'french-2-1'],
  [H.newspaper]: ['french-5-0', 'french-1-0'],
  [H.animals]: ['french-7-0'],
  [H.education]: ['french-7-1'],
  [H.health]: ['french-7-2'],
  [H.travel]: ['french-7-3'],
  [H.politics]: ['french-7-4'],
  [H.sport]: ['french-7-5'],
  [H.technology]: ['french-7-6'],
  [H.youth]: ['french-7-7'],
  [H.oral]: ['french-4-0', 'french-4-1'],
  [H.diary]: ['french-6-0'],
  [H.letter]: ['french-6-1'],
  [H.note]: ['french-6-2'],
  [H.email]: ['french-6-3'],
  [H.recit]: ['french-6-7'],
  [O.conversation]: ['french-3-0'],
  [O.interview]: ['french-3-1'],
  [O.news]: ['french-3-2'],
  [O.form]: ['french-6-5'],
  [O.gaps]: ['french-6-6'],
  [O.oral]: ['french-4-0', 'french-4-1'],
  [O.article]: ['french-5-0'],
  [O.book]: ['french-5-1'],
  [O.readingInterview]: ['french-5-2'],
  [O.otherReading]: ['french-5-3'],
  [O.diary]: ['french-6-0'],
  [O.letter]: ['french-6-1'],
  [O.message]: ['french-6-2'],
  [O.postcard]: ['french-6-4'],
};
for (const topic of referenceTopics) {
  if (!CURRICULUM_CROSSWALK[topic.id]?.length) {
    throw new Error(`French topic has no curriculum bridge: ${topic.id}`);
  }
}

const parseYear = heading => {
  const year = Number(heading.match(/^(\d{4})/)?.[1]);
  if (!year) throw new Error(`French heading has no year: ${heading}`);
  return year;
};
const topicKind = topic => /^AURAL/i.test(topic.label)
  ? 'aural'
  : /^ORAL/i.test(topic.label)
    ? 'oral'
    : /Comprehension/i.test(topic.label)
      ? 'reading'
      : 'writing';
const alphaNumber = token => {
  const normal = String(token).toUpperCase();
  if (/^\d+$/.test(normal)) return normal;
  const value = 'ABCDE'.indexOf(normal) + 1;
  return value > 0 ? String(value) : null;
};
const romanNumber = token => ({ I: 1, II: 2, III: 3, IV: 4 }[String(token).toUpperCase()] ?? null);

const auralNumber = heading => {
  const year = parseYear(heading);
  const letterQuestion = heading.match(/Question\s+([A-E])\b/i)?.[1];
  if (letterQuestion) return alphaNumber(letterQuestion);
  const letterSection = heading.match(/Section\s+([A-E])\b/i)?.[1];
  if (letterSection) return alphaNumber(letterSection);
  const section = heading.match(/Section\s+(\d+)/i)?.[1];
  const question = heading.match(/Question\s+(\d+)/i)?.[1];
  if (year >= 2015 && section) return section;
  if (question) return question;
  if (section) return section;
  throw new Error(`Cannot resolve French aural heading: ${heading}`);
};

const readingNumber = heading => {
  const token = heading.match(/Question\s+([A-D]|[1-4])\b/i)?.[1];
  const number = token && alphaNumber(token);
  if (!number) throw new Error(`Cannot resolve French reading heading: ${heading}`);
  return number;
};

const higherWritingSlot = heading => {
  const question = heading.match(/Question\s+([1-6])\b/i)?.[1];
  if (!question) throw new Error(`Cannot resolve French Higher writing heading: ${heading}`);
  const part = heading.match(/Part\s*\(?([abc])\)?/i)?.[1]?.toUpperCase() ?? '';
  return `B${question}${part}`;
};
const ordinaryWritingSlots = new Map([
  [O.gaps, 'B1A'],
  [O.form, 'B1B'],
  [O.message, 'B2A'],
  [O.postcard, 'B2B'],
  [O.diary, 'B3A'],
  [O.letter, 'B3B'],
]);

const referenceSlot = (topic, heading) => {
  const kind = topicKind(topic);
  if (kind === 'aural') return auralNumber(heading);
  if (kind === 'reading') return `A${readingNumber(heading)}`;
  if (kind === 'oral') {
    const question = heading.match(/Question\s+(\d+)/i)?.[1];
    return question ? `O${question}` : /Document/i.test(heading) ? 'OD' : 'O';
  }
  if (topic.level === 'ordinary') {
    const slot = ordinaryWritingSlots.get(topic.id);
    if (!slot) throw new Error(`Unknown Ordinary French writing topic: ${topic.id}`);
    return slot;
  }
  return higherWritingSlot(heading);
};

const referenceTopicsBySlot = new Map();
for (const topic of referenceTopics) {
  for (const heading of topic.officialQuestionHeadings) {
    const year = parseYear(heading);
    if (year < 2010 || /Deferred/i.test(heading) || topicKind(topic) === 'oral') continue;
    const kind = topicKind(topic) === 'aural' ? 'aural' : 'written';
    const key = [topic.level, year, kind, referenceSlot(topic, heading)].join('|');
    const ids = referenceTopicsBySlot.get(key) ?? [];
    if (!ids.includes(topic.id)) ids.push(topic.id);
    referenceTopicsBySlot.set(key, ids);
  }
}

// Five valid Higher tasks are omitted from the reference topic pages. Their
// nearest browse buckets were checked against the official SEC prompts.
const HIGHER_REFERENCE_OMISSIONS = new Map([
  ['2010|B1A', [H.recit]],
  ['2011|B1A', [H.youth]],
  ['2011|B1B', [H.politics]],
  ['2015|B1B', [H.recit]],
  ['2020|B2B', [H.travel]],
]);

const fallbackTopicIds = (level, year, kind, slot) => {
  const referenced = referenceTopicsBySlot.get([level, year, kind, slot].join('|')) ?? [];
  if (referenced.length) return referenced;
  if (kind === 'aural') {
    const ids = level === 'higher' ? H : O;
    if (slot === '2') return [ids.interview];
    if (slot === '5') return [ids.news];
    return [ids.conversation];
  }
  if (level === 'higher' && slot === 'A1') return [H.newspaper];
  if (level === 'higher' && slot === 'A2') return [H.literary];
  if (level === 'higher' && slot.startsWith('B')) {
    const omission = HIGHER_REFERENCE_OMISSIONS.get(`${year}|${slot}`);
    if (omission) return omission;
    throw new Error(`${year} Higher ${slot}: no reference or reviewed omission mapping`);
  }
  if (level === 'ordinary' && /^A[1-4]$/.test(slot)) return [O.otherReading];
  const ordinaryWriting = {
    B1A: O.gaps,
    B1B: O.form,
    B2A: O.message,
    B2B: O.postcard,
    B3A: O.diary,
    B3B: O.letter,
  }[slot];
  if (ordinaryWriting) return [ordinaryWriting];
  throw new Error(`${year} ${level} ${kind} ${slot}: no French fallback`);
};

const canonicalForTopicIds = ids => {
  const canonical = [...new Set(ids.flatMap(id => CURRICULUM_CROSSWALK[id] ?? []))];
  if (!canonical.length) throw new Error(`No canonical French tags for ${ids.join(', ')}`);
  return {
    primary: canonical[0],
    ...(canonical[1] ? { secondary: canonical[1] } : {}),
  };
};

const paperKind = fileid => /PA00[IEB]V\.pdf$/i.test(fileid) ? 'aural' : 'written';
const paperIdentity = paper => [paper.level, paper.lang, paper.year, paper.fileid].join('|');
const paperMap = new Map();
for (const source of preservationBaseline) {
  const paper = {
    subjectId: 'french',
    level: source.level,
    lang: source.lang,
    year: source.year,
    fileid: source.fileid,
    paperKey: source.paperKey,
    kind: paperKind(source.fileid),
    q: source.questions.map(question => ({ ...question, baseline: true })),
  };
  const identity = paperIdentity(paper);
  if (paperMap.has(identity)) throw new Error(`Duplicate French baseline paper: ${identity}`);
  paperMap.set(identity, paper);
}

const parseSidecarIdentity = file => {
  const match = file.match(/^LC010([AG])L(P000|PA00)([EIB])V\.pdf\.json$/i);
  if (!match) throw new Error(`Unexpected French answer-map filename: ${file}`);
  const kind = match[2].toUpperCase() === 'PA00' ? 'aural' : 'written';
  return {
    level: match[1].toUpperCase() === 'A' ? 'higher' : 'ordinary',
    lang: match[3].toUpperCase() === 'I' ? 'iv' : 'ev',
    fileid: file.slice(0, -'.json'.length),
    paperKey: kind === 'aural' ? 'aural' : 'single',
    kind,
  };
};
const isProductionUmbrella = label => (
  /(?:Production|Expression)\s+[ÉEé]crite|Ceapadóireacht/i.test(String(label ?? ''))
);
const topQuestionFromLabel = label => {
  const text = String(label ?? '');
  const token = text.match(/(?:Text(?:e)?|Comp(?:rehension)?|Reading)\s*(IV|III|II|I|[1-4])\b/i)?.[1]
    ?? text.match(/(?:^|·)\s*Q\.?\s*([1-4])\b/i)?.[1];
  if (!token) return null;
  return /^\d$/.test(token) ? Number(token) : romanNumber(token);
};
const readingTopQuestion = (paper, question, answerQuestion, answerMap) => {
  if (paper.level === 'higher') {
    if (question.primary === 'french-5-1') return 2;
    if (question.primary === 'french-5-0') return 1;
    if (/(?:Text(?:e)?\s*II\b|Text(?:e)?\s*2\b|Compréhension\s*2\b)/i.test(answerQuestion.label ?? '')) return 2;
    return 1;
  }
  const explicit = topQuestionFromLabel(answerQuestion.label);
  if (explicit) return explicit;
  const readingAnchors = answerMap.q.filter(item => !isProductionUmbrella(item.label));
  const pages = [...new Set(readingAnchors.map(item => item.pP))].sort((a, b) => a - b);
  const pageIndex = pages.indexOf(answerQuestion.pP);
  if (pageIndex >= 0 && pages.length <= 4) return pageIndex + 1;
  throw new Error(`${paperIdentity(paper)} Q${answerQuestion.n}: cannot resolve reading text`);
};

const sidecarFiles = fs.readdirSync(ANSWERS_ROOT, { withFileTypes: true })
  .filter(entry => entry.isDirectory() && /^20\d\d$/.test(entry.name))
  .flatMap(entry => fs.readdirSync(path.join(ANSWERS_ROOT, entry.name))
    .filter(file => /^LC010.*\.pdf\.json$/i.test(file))
    .map(file => ({ year: Number(entry.name), file })))
  .sort((a, b) => a.year - b.year || a.file.localeCompare(b.file));

for (const { year, file } of sidecarFiles) {
  const parsed = parseSidecarIdentity(file);
  const candidate = { subjectId: 'french', year, ...parsed, q: [] };
  const identity = paperIdentity(candidate);
  const paper = paperMap.get(identity) ?? candidate;
  const answerMap = readJson(path.join(ANSWERS_ROOT, String(year), file));
  for (const answerQuestion of answerMap.q) {
    let question = paper.q.find(item => item.n === answerQuestion.n);
    if (paper.kind === 'written' && isProductionUmbrella(answerQuestion.label) && !question) continue;
    if (!question) {
      question = { n: answerQuestion.n };
      paper.q.push(question);
    }
    const slot = paper.kind === 'aural'
      ? String(answerQuestion.n)
      : `A${readingTopQuestion(paper, question, answerQuestion, answerMap)}`;
    const baseTopicIds = fallbackTopicIds(paper.level, year, paper.kind, slot);
    question.label = answerQuestion.label ?? question.label ?? `Question ${answerQuestion.n}`;
    question.anchor = answerQuestion;
    question.referenceSlot = slot;
    question.baseTopicIds = baseTopicIds;
    if (!question.primary) Object.assign(question, canonicalForTopicIds(baseTopicIds));
  }
  const duplicateNumbers = paper.q
    .map(question => question.n)
    .filter((number, index, numbers) => numbers.indexOf(number) !== index);
  if (duplicateNumbers.length) throw new Error(`${identity}: duplicate cards ${duplicateNumbers.join(', ')}`);
  paperMap.set(identity, paper);
}

const fullPages = (start, end = start) => Array.from(
  { length: end - start + 1 },
  (_, offset) => ({ p: start + offset, r: [0, 0, 1, 1] }),
);
const customQuestion = ({ n, label, slot, baseTopicIds, start, end = start }) => ({
  n,
  label,
  referenceSlot: slot,
  baseTopicIds,
  ...canonicalForTopicIds(baseTopicIds),
  anchor: {
    n,
    label,
    pP: start,
    pY: [0, 1],
    paperRegion: fullPages(start, end),
  },
});
const addCustom = (paper, spec) => {
  if (paper.q.some(question => question.n === spec.n)) {
    throw new Error(`${paperIdentity(paper)}: custom card ${spec.n} already exists`);
  }
  paper.q.push(customQuestion(spec));
};

// The entitled bilingual 2019 Ordinary paper is indexed but its classic
// answer sidecar is absent. Its four reading and six writing choices are
// restored below from the checked official 16-page booklet.
{
  const paper = {
    subjectId: 'french',
    level: 'ordinary',
    lang: 'ev',
    year: 2019,
    fileid: 'LC010GLP000BV.pdf',
    paperKey: 'single',
    kind: 'written',
    q: [],
  };
  const identity = paperIdentity(paper);
  if (paperMap.has(identity)) throw new Error(`Unexpected existing French paper: ${identity}`);
  paperMap.set(identity, paper);
}

const ordinaryReadingPages = (year, number) => {
  if (year <= 2019) {
    const start = 1 + ((number - 1) * 2);
    return { start, end: start + 1 };
  }
  const current = { 1: [3, 5], 2: [6, 7], 3: [8, 9], 4: [10, 11] }[number];
  return { start: current[0], end: current[1] };
};

// 2015 and 2017 sidecars stop after the third Ordinary comprehension; 2019
// has no written sidecar. Fill only the missing top-level reading cards.
for (const paper of paperMap.values()) {
  if (paper.kind !== 'written' || paper.level !== 'ordinary') continue;
  for (let number = 1; number <= 4; number += 1) {
    const slot = `A${number}`;
    if (paper.q.some(question => question.referenceSlot === slot)) continue;
    const pages = ordinaryReadingPages(paper.year, number);
    const baseTopicIds = fallbackTopicIds(paper.level, paper.year, paper.kind, slot);
    addCustom(paper, {
      n: slot,
      label: `Section A · Question ${number}`,
      slot,
      baseTopicIds,
      ...pages,
    });
  }
}

const higherWritingSlots = year => year <= 2020
  ? ['B1A', 'B1B', 'B2A', 'B2B', 'B3A', 'B3B', 'B4A', 'B4B']
  : ['B1A', 'B1B', 'B1C', 'B2', 'B3', 'B4', 'B5', 'B6'];
const ordinaryWriting = ['B1A', 'B1B', 'B2A', 'B2B', 'B3A', 'B3B'];
const writingLabel = slot => {
  const match = slot.match(/^B(\d)([A-C]?)$/);
  return `Section B · Question ${match[1]}${match[2] ? `(${match[2].toLowerCase()})` : ''}`;
};
const writingPages = (paper, slot) => {
  const question = Number(slot[1]);
  if (paper.level === 'higher') {
    if (paper.year <= 2019) {
      const start = 5 + ((question - 1) * 2);
      return { start, end: start + 1 };
    }
    if (paper.year === 2020) {
      const start = 7 + ((question - 1) * 2);
      return { start, end: start + 1 };
    }
    if (question === 1) return { start: 7, end: 9 };
    if (question <= 4) return { start: 10, end: 10 };
    return { start: 11, end: 11 };
  }
  if (paper.year <= 2019) {
    if (slot === 'B1A') return { start: 9, end: 9 };
    if (slot === 'B1B') return { start: 10, end: 10 };
    if (question === 2) return { start: 11, end: 12 };
    return { start: 13, end: 14 };
  }
  if (slot === 'B1A') return { start: 11, end: 11 };
  if (slot === 'B1B') return { start: 12, end: 12 };
  if (question === 2) return { start: 13, end: 14 };
  return { start: 15, end: 16 };
};

for (const paper of paperMap.values()) {
  if (paper.kind !== 'written') continue;
  const slots = paper.level === 'higher' ? higherWritingSlots(paper.year) : ordinaryWriting;
  for (const slot of slots) {
    const baseTopicIds = fallbackTopicIds(paper.level, paper.year, paper.kind, slot);
    addCustom(paper, {
      n: slot,
      label: writingLabel(slot),
      slot,
      baseTopicIds,
      ...writingPages(paper, slot),
    });
  }
}

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

const findPaper = (year, level, kind) => {
  const matches = localPapers.filter(paper => (
    paper.year === year && paper.level === level && paper.kind === kind && paper.lang === 'ev'
  ));
  if (matches.length !== 1) {
    throw new Error(`${year} ${level} ${kind}: expected one French reference paper, found ${matches.length}`);
  }
  return matches[0];
};

const resolveHeading = (topic, heading) => {
  const year = parseYear(heading);
  const sitting = /Deferred/i.test(heading) ? 'deferred' : 'main';
  const kind = topicKind(topic);
  const paperKey = kind === 'aural' ? 'aural' : kind === 'oral' ? 'oral' : 'single';
  const slot = referenceSlot(topic, heading);
  const blocked = reason => ({
    topicId: topic.id,
    heading,
    year,
    sitting,
    paperKey,
    referenceSlot: slot,
    resolution: 'source-blocked',
    reason,
  });
  if (year < 2010) {
    return blocked('The entitled local SEC question corpus begins in 2010. The factual heading is retained, but no StudyClix-hosted question, solution, image or PDF is copied.');
  }
  if (sitting === 'deferred') {
    return blocked('The factual deferred-paper heading is retained, but the corresponding entitled deferred booklet is not present in the local corpus.');
  }
  if (kind === 'oral') {
    return blocked('The factual official oral heading is retained, but the published oral material is not present in the local Paper Trail corpus.');
  }
  const localKind = kind === 'aural' ? 'aural' : 'written';
  const paper = findPaper(year, topic.level, localKind);
  const candidates = paper.q.filter(question => question.referenceSlot === slot);
  if (!candidates.length) throw new Error(`${topic.id}: no local French card resolves ${heading}`);
  return {
    topicId: topic.id,
    heading,
    year,
    sitting,
    paperKey,
    referenceSlot: slot,
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
if (associations.length !== 739) {
  throw new Error(`French reference boundary mismatch: ${associations.length} associations`);
}
const matched = associations.filter(association => association.resolution === 'matched');
const sourceBlocked = associations.filter(association => association.resolution === 'source-blocked');

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

const localQuestionMappings = localPapers.flatMap(paper => paper.q.map(question => {
  const referenced = referenceTopicsByLocalQuestion.get(localQuestionIdentity(paper, question.n)) ?? [];
  const topicIds = [...new Set([...referenced, ...(question.baseTopicIds ?? [])])]
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
      ? question.baseTopicIds?.some(id => !referenced.includes(id))
        ? 'reference+retained-local'
        : 'reference'
      : 'retained-local',
  };
}));

const duplicateMappings = localQuestionMappings
  .map(mapping => [mapping.level, mapping.lang, mapping.year, mapping.fileid, mapping.n].join('|'))
  .filter((identity, index, identities) => identities.indexOf(identity) !== index);
if (duplicateMappings.length) {
  throw new Error(`Duplicate French local mappings: ${[...new Set(duplicateMappings)].join(', ')}`);
}

const tagPapers = localPapers.map(paper => ({
  subjectId: 'french',
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
  return {
    n: question.n,
    label: question.label ?? `Question ${question.n}`,
    printOrder: index + 1,
    pP: source.pP,
    pY: source.pY,
    paperRegion: source.paperRegion ?? fullPages(source.pP),
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
  mapping.level, mapping.year, mapping.paperKey, mapping.n,
].join('|')));
const blockedByReason = sourceBlocked.reduce((counts, association) => {
  const key = association.year < 2010
    ? 'preCorpus'
    : association.sitting === 'deferred'
      ? 'deferred'
      : 'oralMaterial';
  counts[key] = (counts[key] ?? 0) + 1;
  return counts;
}, {});
const summary = {
  referenceTopics: referenceTopics.length,
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
  subjectId: 'french',
  capturedAt: reference.capturedAt,
  policy: {
    matchedSource: 'Entitled local State Examinations Commission corpus only.',
    excludedContent: 'No commercial mock question, solution, note, question text, StudyClix image or StudyClix-hosted PDF is copied.',
    restoredCards: 'Missing reading and written-production cards use page boundaries checked in the official SEC booklets.',
    referenceOmissions: 'Valid local tasks omitted by the reference retain the closest truthful existing French practice bucket, with retained-local provenance.',
  },
  summary,
  associations,
  localQuestionMappings,
  hostedAnchorMaps,
};
fs.writeFileSync(OUTPUT_PATH, `${JSON.stringify(output, null, 2)}\n`);
fs.writeFileSync(CURRICULUM_PATH, `${JSON.stringify(CURRICULUM_CROSSWALK, null, 2)}\n`);

const paperKeyCode = paperKey => paperKey === 'aural' ? 'a' : paperKey === 'oral' ? 'o' : 's';
const sittingCode = sitting => sitting === 'deferred' ? 'd' : 'm';
const runtimePartReferences = associations.flatMap(association => {
  const index = topicIndex.get(association.topicId);
  if (association.resolution === 'matched') {
    return association.target.questionNumbers.map(number => [
      index,
      association.year - 2000,
      association.target.level === 'higher' ? 'h' : 'o',
      paperKeyCode(association.target.paperKey),
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
    paperKeyCode(association.paperKey),
    sittingCode(association.sitting),
    association.referenceSlot,
    association.heading,
  ]];
});

const runtimeGroups = Object.entries(reference.variants).map(([level, variant]) => [
  level === 'higher' ? 'h' : 'o',
  variant.label,
  variant.topics.map(topic => topicIndex.get(topic.id)),
]);
const runtime = {
  v: 1,
  subjectId: 'french',
  capturedAt: reference.capturedAt,
  referenceProvider: reference.reference.provider,
  groups: runtimeGroups,
  topics: referenceTopics.map(topic => [
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
    paperKeyCode(mapping.paperKey),
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
