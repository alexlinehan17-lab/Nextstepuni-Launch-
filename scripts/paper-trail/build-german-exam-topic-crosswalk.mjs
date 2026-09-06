#!/usr/bin/env node
/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 *
 * Reconcile the metadata-only StudyClix German hierarchy with NextStepUni's
 * entitled SEC corpus. The reference contributes factual labels, counts and
 * headings only; no question text, solutions, notes, media or PDFs are copied.
 *
 * The generator is additive. It starts from the frozen German tag baseline,
 * incorporates every reviewed local answer sidecar, restores omitted official
 * writing choices from checked SEC page boundaries, and preserves every
 * pre-migration question identity and canonical tag verbatim.
 */

import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const HERE = path.dirname(fileURLToPath(import.meta.url));
const ROOT = path.resolve(HERE, '../..');
const ANSWERS_ROOT = path.join(HERE, 'answers');
const HOSTED_ROOT = path.join(ROOT, 'public/paper-anchors');
const TAGS_PATH = path.join(HERE, 'topic-tags/tags/german.json');
const BASELINE_PATH = path.join(ROOT, 'test/fixtures/germanTopicQuestionBaseline.json');
const REFERENCE_PATH = path.join(ROOT, 'data/examTopics/german.json');
const OUTPUT_PATH = path.join(ROOT, 'data/examTopics/german-local-crosswalk.json');
const RUNTIME_PATH = path.join(ROOT, 'data/examTopics/german-runtime.json');
const CURRICULUM_PATH = path.join(ROOT, 'data/examTopics/german-curriculum-crosswalk.json');

const readJson = file => JSON.parse(fs.readFileSync(file, 'utf8'));
const reference = readJson(REFERENCE_PATH);
const preservationBaseline = readJson(BASELINE_PATH);
const referenceTopics = Object.entries(reference.variants).flatMap(([level, variant]) => (
  variant.topics.map(topic => ({ ...topic, level }))
));
if (referenceTopics.length !== 25) {
  throw new Error(`Expected 25 German reference topics, found ${referenceTopics.length}`);
}

const topicById = new Map(referenceTopics.map(topic => [topic.id, topic]));
const topicIndex = new Map(referenceTopics.map((topic, index) => [topic.id, index]));
const topicByLabel = new Map(referenceTopics.map(topic => [`${topic.level}|${topic.label}`, topic.id]));
const topicId = (level, label) => {
  const id = topicByLabel.get(`${level}|${label}`);
  if (!id) throw new Error(`Missing German reference topic: ${level} · ${label}`);
  return id;
};

const H = {
  dialogue: topicId('higher', 'AURAL - Dialogue'),
  interview: topicId('higher', 'AURAL - Interview'),
  news: topicId('higher', 'AURAL - News Pieces'),
  phone: topicId('higher', 'AURAL - Phone Call'),
  theme: topicId('higher', 'Äußerung zum Thema (Write on a Theme)'),
  magazine: topicId('higher', 'Comprehension: Magazine or Newspaper'),
  novel: topicId('higher', 'Comprehension: Novel or Short Story'),
  grammar: topicId('higher', 'Grammatik (Grammar)'),
  picture: topicId('higher', 'Schriftliche Produktion (Picture)'),
  letter: topicId('higher', 'Schriftliche Produktion (Write a Letter)'),
};
const O = {
  dialogue: topicId('ordinary', 'AURAL - Dialogue'),
  interview: topicId('ordinary', 'AURAL - Interview'),
  news: topicId('ordinary', 'AURAL - News Pieces'),
  phone: topicId('ordinary', 'AURAL - Phone Call'),
  magazine: topicId('ordinary', 'Comprehension: Magazine or Newspaper'),
  novel: topicId('ordinary', 'Comprehension: Novel or Short Story'),
  dialogueWriting: topicId('ordinary', 'Finish the Dialogue'),
  grammar: topicId('ordinary', 'Grammar (Grammatik)'),
  blog: topicId('ordinary', 'Write a Blog...'),
  letter: topicId('ordinary', 'Write a Letter...'),
  story: topicId('ordinary', 'Write a Story...'),
  application: topicId('ordinary', 'Write an Application'),
  email: topicId('ordinary', 'Write an Email...'),
  theme: topicId('ordinary', 'Write on a Theme (Thema)'),
  opinion: topicId('ordinary', 'Write on a Topic/Give Your Opinion'),
};

const CURRICULUM_CROSSWALK = {
  [H.dialogue]: ['german-4-2', 'german-3-1'],
  [H.interview]: ['german-4-0', 'german-3-1'],
  [H.news]: ['german-4-3', 'german-3-1'],
  [H.phone]: ['german-4-1', 'german-3-1'],
  [H.theme]: ['german-7-0', 'german-3-3'],
  [H.magazine]: ['german-6-0', 'german-3-2'],
  [H.novel]: ['german-6-1', 'german-3-2'],
  [H.grammar]: ['german-3-4'],
  [H.picture]: ['german-7-1', 'german-3-3'],
  [H.letter]: ['german-7-2', 'german-3-3'],
  [O.dialogue]: ['german-4-2', 'german-3-1'],
  [O.interview]: ['german-4-0', 'german-3-1'],
  [O.news]: ['german-4-3', 'german-3-1'],
  [O.phone]: ['german-4-1', 'german-3-1'],
  [O.magazine]: ['german-6-0', 'german-3-2'],
  [O.novel]: ['german-6-1', 'german-3-2'],
  [O.dialogueWriting]: ['german-7-7', 'german-3-3'],
  [O.grammar]: ['german-3-4'],
  [O.blog]: ['german-7-3', 'german-3-3'],
  [O.letter]: ['german-7-2', 'german-3-3'],
  [O.story]: ['german-7-4', 'german-3-3'],
  [O.application]: ['german-7-5', 'german-3-3'],
  [O.email]: ['german-7-6', 'german-3-3'],
  [O.theme]: ['german-7-0', 'german-3-3'],
  [O.opinion]: ['german-7-8', 'german-3-3'],
};
for (const topic of referenceTopics) {
  if (!CURRICULUM_CROSSWALK[topic.id]?.length) {
    throw new Error(`German topic has no curriculum bridge: ${topic.id}`);
  }
}

const canonicalForTopicIds = ids => {
  const canonical = [...new Set(ids.flatMap(id => CURRICULUM_CROSSWALK[id] ?? []))];
  if (!canonical.length) throw new Error(`No canonical German tags for ${ids.join(', ')}`);
  return {
    primary: canonical[0],
    ...(canonical[1] ? { secondary: canonical[1] } : {}),
  };
};

const parseYear = heading => {
  const year = Number(heading.match(/^(\d{4})/)?.[1]);
  if (!year) throw new Error(`German heading has no year: ${heading}`);
  return year;
};
const paperKind = fileid => /PA00[IEB]V\.pdf$/i.test(fileid) ? 'aural' : 'written';
const paperIdentity = paper => [paper.level, paper.lang, paper.year, paper.fileid].join('|');
const templateIdentity = paper => [paper.level, paper.year, paper.kind].join('|');
const fullPages = (start, end = start) => Array.from(
  { length: end - start + 1 },
  (_, offset) => ({ p: start + offset, r: [0, 0, 1, 1] }),
);

const paperMap = new Map();
const baselineByIdentity = new Map();
for (const source of preservationBaseline) {
  const paper = {
    subjectId: 'german',
    level: source.level,
    lang: source.lang,
    year: source.year,
    fileid: source.fileid,
    paperKey: source.paperKey,
    kind: paperKind(source.fileid),
    q: source.questions.map(question => ({ ...question, baseline: true })),
  };
  const identity = paperIdentity(paper);
  if (paperMap.has(identity)) throw new Error(`Duplicate German baseline paper: ${identity}`);
  paperMap.set(identity, paper);
  baselineByIdentity.set(identity, source);
}

const parseSidecarIdentity = file => {
  const match = file.match(/^LC011([AG])L(P000|PA00)([EIB])V\.pdf\.json$/i);
  if (!match) throw new Error(`Unexpected German answer-map filename: ${file}`);
  const kind = match[2].toUpperCase() === 'PA00' ? 'aural' : 'written';
  return {
    level: match[1].toUpperCase() === 'A' ? 'higher' : 'ordinary',
    lang: match[3].toUpperCase() === 'I' ? 'iv' : 'ev',
    fileid: file.slice(0, -'.json'.length),
    paperKey: kind === 'aural' ? 'aural' : 'single',
    kind,
  };
};

const sidecarFiles = fs.readdirSync(ANSWERS_ROOT, { withFileTypes: true })
  .filter(entry => entry.isDirectory() && /^20\d\d$/.test(entry.name))
  .flatMap(entry => fs.readdirSync(path.join(ANSWERS_ROOT, entry.name))
    .filter(file => /^LC011.*\.pdf\.json$/i.test(file))
    .map(file => ({ year: Number(entry.name), file })))
  .sort((a, b) => a.year - b.year || a.file.localeCompare(b.file));

const rawSidecars = sidecarFiles.map(({ year, file }) => {
  const parsed = parseSidecarIdentity(file);
  return {
    year,
    file,
    ...parsed,
    data: readJson(path.join(ANSWERS_ROOT, String(year), file)),
  };
});
const representativeByTemplate = new Map();
for (const source of rawSidecars) {
  const key = templateIdentity(source);
  if (source.lang === 'ev' && !representativeByTemplate.has(key)) {
    representativeByTemplate.set(key, source);
  }
}

const sectionNumber = label => {
  const token = String(label ?? '').match(/Text\s*(III|II|I)\b/i)?.[1]?.toUpperCase();
  return ({ I: 1, II: 2, III: 3 })[token] ?? null;
};
const isGrammar = label => /Grammatik/i.test(String(label ?? ''));
const isTheme = label => /Äußerung|Aeusserung/i.test(String(label ?? ''));
const isProduction = label => /Schriftliche\s+Produktion|Ceapadóireacht/i.test(String(label ?? ''));
const readingFromSidecar = source => source.data.q.flatMap((question, sourceIndex) => {
  const section = sectionNumber(question.label);
  if (!section || isGrammar(question.label) || isTheme(question.label) || isProduction(question.label)) return [];
  const index = Number(String(question.label ?? '').match(/(?:^|·)\s*Q\.?\s*(\d+)\b/i)?.[1]) || null;
  return [{
    section,
    index,
    sourceIndex,
    label: index ? `Text ${['', 'I', 'II', 'III'][section]} · Q${index}` : `Text ${['', 'I', 'II', 'III'][section]} · Leseverständnis`,
    anchor: question,
  }];
});

const parseHostedReading = question => {
  const legacy = String(question.label ?? '').match(/^([BD])-(\d+)$/i);
  if (legacy) {
    return {
      section: legacy[1].toUpperCase() === 'B' ? 1 : 2,
      index: Number(legacy[2]),
      label: `Text ${legacy[1].toUpperCase() === 'B' ? 'I' : 'II'} · Q${legacy[2]}`,
      anchor: question,
    };
  }
  const semantic = String(question.label ?? '').match(/^Text\s+(I|II)\s+·\s+Q(\d+)$/i);
  if (!semantic) return null;
  return {
    section: semantic[1].toUpperCase() === 'I' ? 1 : 2,
    index: Number(semantic[2]),
    label: `Text ${semantic[1].toUpperCase()} · Q${semantic[2]}`,
    anchor: question,
  };
};
const existingHigherReading = (year, fileid) => {
  const file = path.join(HOSTED_ROOT, String(year), `${fileid}.json`);
  if (!fs.existsSync(file)) return [];
  const parsed = readJson(file).q?.map(parseHostedReading).filter(Boolean) ?? [];
  return parsed.length === 8 ? parsed : [];
};

const higherLayout = year => {
  if (year <= 2014) return { grammar: 5, theme: 9, production: 10 };
  if (year === 2015) return { grammar: 6, theme: 12, production: 13 };
  if (year === 2016) return { grammar: 6, theme: 11, production: 12 };
  if (year === 2017 || year === 2018) return { grammar: year === 2018 ? 7 : 6, theme: 12, production: 14 };
  if (year === 2019) return { grammar: 8, theme: 14, production: 16 };
  if (year === 2020) return { grammar: 8, theme: 16, production: 18 };
  if (year === 2021) return { grammar: 8, theme: 14, production: 16 };
  return { grammar: 9, theme: 16, production: 18 };
};
const ordinaryLayout = year => {
  if (year <= 2017) return { grammar: 5, theme: year <= 2011 ? 9 : 10, textThree: 12, production: 16 };
  if (year <= 2020) return { grammar: year === 2018 ? 6 : 7, theme: 12, textThree: 14, production: 18 };
  if (year === 2021) return { grammar: 8, theme: 13, textThree: 16, production: 20 };
  return { grammar: 9, theme: 14, textThree: 16, production: 20 };
};

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
const addQuestion = (paper, question) => {
  if (paper.q.some(existing => existing.n === question.n)) {
    throw new Error(`${paperIdentity(paper)}: duplicate card ${question.n}`);
  }
  paper.q.push(question);
};

const baselineTemplateFor = (paper, readingCount) => preservationBaseline.find(candidate => (
  candidate.year === paper.year
  && candidate.level === paper.level
  && candidate.paperKey === 'single'
  && candidate.questions.length === readingCount
));

for (const source of rawSidecars) {
  const candidate = {
    subjectId: 'german',
    year: source.year,
    level: source.level,
    lang: source.lang,
    fileid: source.fileid,
    paperKey: source.paperKey,
    kind: source.kind,
    q: [],
  };
  const identity = paperIdentity(candidate);
  const paper = paperMap.get(identity) ?? candidate;

  if (paper.kind === 'aural') {
    const ids = paper.level === 'higher' ? H : O;
    const auralTopics = { 1: ids.interview, 2: ids.phone, 3: ids.dialogue, 4: ids.news };
    for (const answerQuestion of source.data.q) {
      const baseTopicIds = [auralTopics[Number(answerQuestion.n)]];
      if (!baseTopicIds[0]) throw new Error(`${identity}: unexpected aural card ${answerQuestion.n}`);
      addQuestion(paper, {
        n: answerQuestion.n,
        label: answerQuestion.label ?? `Aural · Question ${answerQuestion.n}`,
        referenceSlot: `A${answerQuestion.n}`,
        baseTopicIds,
        ...canonicalForTopicIds(baseTopicIds),
        anchor: answerQuestion,
      });
    }
    paperMap.set(identity, paper);
    continue;
  }

  const representative = representativeByTemplate.get(templateIdentity(source));
  if (!representative) throw new Error(`${identity}: missing English/bilingual sidecar template`);
  let readings = readingFromSidecar(representative);
  if (paper.level === 'higher' && readings.length < 8) {
    const hosted = existingHigherReading(paper.year, paper.fileid);
    if (hosted.length === 8) readings = hosted;
  }
  if (!readings.length) throw new Error(`${identity}: no German reading cards resolved`);

  const ownBaseline = baselineByIdentity.get(identity);
  const sharedNumberTemplate = ownBaseline ?? baselineTemplateFor(paper, readings.length);
  const levelIds = paper.level === 'higher' ? H : O;
  for (const [index, reading] of readings.entries()) {
    const baseTopicIds = [reading.section === 1 ? levelIds.novel : levelIds.magazine];
    const baselineQuestion = ownBaseline ? paper.q[index] : null;
    const n = baselineQuestion?.n
      ?? sharedNumberTemplate?.questions[index]?.n
      ?? `${['', 'I', 'II', 'III'][reading.section]}${reading.index ?? ''}`;
    const question = baselineQuestion ?? {
      n,
      ...canonicalForTopicIds(baseTopicIds),
    };
    question.label = reading.label;
    question.referenceSlot = ['I', 'II', 'III'][reading.section - 1];
    question.baseTopicIds = baseTopicIds;
    question.anchor = reading.anchor;
    if (!baselineQuestion) addQuestion(paper, question);
  }

  const layout = paper.level === 'higher' ? higherLayout(paper.year) : ordinaryLayout(paper.year);
  const grammarSource = representative.data.q.find(question => isGrammar(question.label));
  const grammarTopic = paper.level === 'higher' ? H.grammar : O.grammar;
  addQuestion(paper, {
    n: 'G',
    label: 'Angewandte Grammatik',
    referenceSlot: 'G',
    baseTopicIds: [grammarTopic],
    ...canonicalForTopicIds([grammarTopic]),
    anchor: grammarSource ?? {
      n: 'G',
      label: 'Angewandte Grammatik',
      pP: layout.grammar,
      pY: [0, 1],
      paperRegion: fullPages(layout.grammar),
    },
  });

  const themeTopic = paper.level === 'higher' ? H.theme : O.theme;
  const themeEnd = paper.level === 'higher' ? layout.production - 1 : layout.textThree - 1;
  addQuestion(paper, customQuestion({
    n: 'T-A',
    label: 'Äußerung zum Thema · Option (a)',
    slot: 'T-A',
    baseTopicIds: [themeTopic],
    start: layout.theme,
    end: themeEnd,
  }));
  addQuestion(paper, customQuestion({
    n: 'T-B',
    label: 'Äußerung zum Thema · Option (b)',
    slot: 'T-B',
    baseTopicIds: [themeTopic],
    start: layout.theme,
    end: themeEnd,
  }));

  if (paper.level === 'higher') {
    addQuestion(paper, customQuestion({
      n: 'P-A',
      label: 'Schriftliche Produktion · Letter',
      slot: 'P-A',
      baseTopicIds: [H.letter],
      start: layout.production,
    }));
    addQuestion(paper, customQuestion({
      n: 'P-B',
      label: 'Schriftliche Produktion · Picture',
      slot: 'P-B',
      baseTopicIds: [H.picture],
      start: layout.production + 1,
    }));
  } else {
    addQuestion(paper, customQuestion({
      n: 'P-A',
      label: 'Schriftliche Produktion · Letter',
      slot: 'P-A',
      baseTopicIds: [O.letter],
      start: layout.production,
      end: layout.production + 1,
    }));
    addQuestion(paper, customQuestion({
      n: 'P-B',
      label: 'Schriftliche Produktion · Picture story',
      slot: 'P-B',
      baseTopicIds: [O.story],
      start: layout.production + 2,
      end: layout.production + 3,
    }));
  }

  const unresolvedBaseline = paper.q.filter(question => question.baseline && !question.baseTopicIds);
  for (const question of unresolvedBaseline) {
    if (paper.level !== 'ordinary') {
      throw new Error(`${identity} Q${question.n}: unresolved preserved card`);
    }
    question.label = `Text III · retained card ${question.n}`;
    question.referenceSlot = 'III';
    question.baseTopicIds = [O.magazine];
    question.anchor = {
      n: question.n,
      label: question.label,
      pP: layout.textThree,
      pY: [0, 1],
      paperRegion: fullPages(layout.textThree, Math.min(layout.textThree + 2, layout.production - 1)),
    };
  }

  paperMap.set(identity, paper);
}

const localPapers = [...paperMap.values()].sort((a, b) => (
  b.year - a.year
  || a.level.localeCompare(b.level)
  || a.lang.localeCompare(b.lang)
  || a.fileid.localeCompare(b.fileid)
));
if (localPapers.length !== 100) {
  throw new Error(`Expected 100 German local paper variants, found ${localPapers.length}`);
}

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

const auralSlotByTopic = new Map([
  [H.interview, 'A1'], [H.phone, 'A2'], [H.dialogue, 'A3'], [H.news, 'A4'],
  [O.interview, 'A1'], [O.phone, 'A2'], [O.dialogue, 'A3'], [O.news, 'A4'],
]);
const combinedOptions = heading => /\ba\s*(?:,|&|\/)\s*b\b|\ba\s*-\s*b\b/i.test(heading);
const optionLetter = heading => (
  heading.match(/Part\s+([abc])\b/i)?.[1]?.toUpperCase()
  ?? heading.match(/Question\s+([abc])(?:\b|[.,])/i)?.[1]?.toUpperCase()
  ?? null
);

const higherReferenceSlot = (topic, heading) => {
  const aural = auralSlotByTopic.get(topic.id);
  if (aural) return aural;
  if (topic.id === H.novel) return 'I';
  if (topic.id === H.magazine) return 'II';
  if (topic.id === H.grammar) return 'G';
  if (topic.id === H.letter) return 'P-A';
  if (topic.id === H.picture) return 'P-B';
  if (topic.id !== H.theme) throw new Error(`Unhandled Higher German topic: ${topic.id}`);
  if (/Section\s+5\b/i.test(heading)) return 'P-B';
  if (combinedOptions(heading)) return 'T';
  const option = optionLetter(heading);
  return option === 'A' ? 'T-A' : option === 'B' ? 'T-B' : 'T';
};

const ordinaryReadingSlot = (topic, heading) => {
  const year = parseYear(heading);
  if (topic.id === O.novel) {
    return year === 2016 && /Section\s+5\b/i.test(heading) ? 'III' : 'I';
  }
  if (topic.id !== O.magazine) throw new Error(`Not an Ordinary reading topic: ${topic.id}`);
  if (/Text\s*3\b/i.test(heading) || /Question\s+5\b/i.test(heading)) return 'III';
  if (year === 2010 && !/Text\s*2\b/i.test(heading)) return 'III';
  if (year === 2012 && /Section\s+3\b/i.test(heading)) return 'III';
  if (year === 2014 && /Section\s+3\b/i.test(heading)) return 'III';
  if (year === 2018 && /Section\s+3\b/i.test(heading)) return 'III';
  if ((year === 2020 || year === 2021) && /Section\s+3\b/i.test(heading)) return 'III';
  if (year === 2019 && /Section\s+4\b/i.test(heading)) return 'III';
  if (year === 2017 && /Section\s+5\b/i.test(heading)) return 'III';
  return 'II';
};

const ordinaryReferenceSlot = (topic, heading) => {
  const aural = auralSlotByTopic.get(topic.id);
  if (aural) return aural;
  if (topic.id === O.novel || topic.id === O.magazine) return ordinaryReadingSlot(topic, heading);
  if (topic.id === O.grammar) return 'G';
  if (topic.id === O.letter) return 'P-A';
  if (topic.id === O.story) return 'P-B';
  if (topic.id === O.blog) return 'T';
  if (/Question\s+6\b|Section\s+(?:Written|Writing)\b/i.test(heading)) return 'P-B';
  if (combinedOptions(heading)) return 'T';
  const year = parseYear(heading);
  const option = optionLetter(heading);
  if (year === 2023 && /Question\s+2\b/i.test(heading)) {
    if (option === 'B') return 'T-A';
    if (option === 'C') return 'T-B';
  }
  return option === 'A' ? 'T-A' : option === 'B' ? 'T-B' : 'T';
};
const referenceSlot = (topic, heading) => topic.level === 'higher'
  ? higherReferenceSlot(topic, heading)
  : ordinaryReferenceSlot(topic, heading);

const findPaper = (year, level, kind) => {
  const matches = localPapers.filter(paper => (
    paper.year === year && paper.level === level && paper.kind === kind && paper.lang === 'ev'
  ));
  if (matches.length !== 1) {
    throw new Error(`${year} ${level} ${kind}: expected one German reference paper, found ${matches.length}`);
  }
  return matches[0];
};
const candidatesForSlot = (paper, slot) => paper.q.filter(question => (
  slot === 'T' ? question.referenceSlot === 'T-A' || question.referenceSlot === 'T-B' : question.referenceSlot === slot
));

const resolveHeading = (topic, heading) => {
  const year = parseYear(heading);
  const sitting = /Deferred/i.test(heading) ? 'deferred' : 'main';
  const kind = topic.groupId === 'aural' ? 'aural' : 'written';
  const paperKey = kind === 'aural' ? 'aural' : 'single';
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
  const paper = findPaper(year, topic.level, kind);
  const candidates = candidatesForSlot(paper, slot);
  if (!candidates.length) throw new Error(`${topic.id}: no local German card resolves ${heading} (${slot})`);
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
if (associations.length !== 479) {
  throw new Error(`German reference boundary mismatch: ${associations.length} associations`);
}
const matched = associations.filter(association => association.resolution === 'matched');
const sourceBlocked = associations.filter(association => association.resolution === 'source-blocked');
if (matched.length !== 379 || sourceBlocked.length !== 100) {
  throw new Error(`German source boundary mismatch: matched=${matched.length}, blocked=${sourceBlocked.length}`);
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
  throw new Error(`Duplicate German local mappings: ${[...new Set(duplicateMappings)].join(', ')}`);
}

const tagPapers = localPapers.map(paper => ({
  subjectId: 'german',
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

const hostedQuestion = (question, index, paper, printOrderByQuestion, duplicateAnchors) => {
  const source = question.anchor;
  if (!source || !Number.isFinite(source.pP) || !Array.isArray(source.pY)) {
    throw new Error(`${paperIdentity(paper)} Q${question.n}: missing verified paper anchor`);
  }
  // A handful of legacy language sidecars have two semantic reading questions
  // collapsed onto the same paper start anchor. The generic next-anchor crop
  // quite correctly refuses that ambiguity. Keep the question usable without
  // pretending to know a finer boundary: show the complete verified start page
  // for both cards. This is a paper-only fallback, never an answer crop.
  const anchorKey = `${source.pP}|${source.pY[0]}`;
  const collisionFallback = duplicateAnchors.has(anchorKey)
    ? fullPages(source.pP)
    : undefined;
  return {
    n: question.n,
    label: question.label ?? `Question ${question.n}`,
    printOrder: printOrderByQuestion.get(question) ?? index + 1,
    pP: source.pP,
    pY: source.pY,
    ...(source.paperRegion
      ? { paperRegion: source.paperRegion }
      : collisionFallback
        ? { paperRegion: collisionFallback }
        : {}),
    ...(source.endP !== undefined ? { endP: source.endP } : {}),
    ...(source.endY !== undefined ? { endY: source.endY } : {}),
    region: [{ p: 1 }],
    mode: 'pagejump',
    conf: 0.5,
  };
};

const hostedAnchorMaps = [];
for (const paper of localPapers) {
  const physicalOrder = [...paper.q].sort((a, b) => (
    a.anchor.pP - b.anchor.pP
    || a.anchor.pY[0] - b.anchor.pY[0]
    || paper.q.indexOf(a) - paper.q.indexOf(b)
  ));
  const printOrderByQuestion = new Map(
    physicalOrder.map((question, index) => [question, index + 1]),
  );
  const anchorCounts = new Map();
  for (const question of paper.q) {
    const key = `${question.anchor.pP}|${question.anchor.pY[0]}`;
    anchorCounts.set(key, (anchorCounts.get(key) ?? 0) + 1);
  }
  const duplicateAnchors = new Set(
    [...anchorCounts].filter(([, count]) => count > 1).map(([key]) => key),
  );
  const artifact = {
    v: 1,
    paperFileid: paper.fileid,
    schemeFileid: '',
    component: paper.kind === 'aural' ? 'A00' : '000',
    band: [1, 1],
    copyright: '© State Examinations Commission',
    paperOnly: 1,
    q: paper.q.map((question, index) => hostedQuestion(
      question,
      index,
      paper,
      printOrderByQuestion,
      duplicateAnchors,
    )),
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
  const key = association.year < 2010 ? 'preCorpus' : 'deferred';
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
  emptyOfficialReferenceTopics: referenceTopics
    .filter(topic => topic.officialQuestionHeadings.length === 0)
    .map(topic => topic.id),
};

const output = {
  schemaVersion: 1,
  subjectId: 'german',
  capturedAt: reference.capturedAt,
  policy: {
    matchedSource: 'Entitled local State Examinations Commission corpus only.',
    excludedContent: 'No commercial mock question, solution, note, question text, StudyClix image or StudyClix-hosted PDF is copied.',
    restoredCards: 'Missing short-writing and written-production choices use page boundaries checked in the official SEC booklets.',
    referenceOmissions: 'Valid local tasks omitted by the reference retain the closest truthful German practice bucket, with retained-local provenance.',
  },
  summary,
  associations,
  localQuestionMappings,
  hostedAnchorMaps,
};
fs.writeFileSync(OUTPUT_PATH, `${JSON.stringify(output, null, 2)}\n`);
fs.writeFileSync(CURRICULUM_PATH, `${JSON.stringify(CURRICULUM_CROSSWALK, null, 2)}\n`);

const paperKeyCode = paperKey => paperKey === 'aural' ? 'a' : 's';
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

const runtimeGroups = Object.entries(reference.variants).flatMap(([level, variant]) => (
  variant.groups.map(group => {
    const ids = variant.topics
      .filter(topic => topic.groupId === group.id)
      .map(topic => topic.id);
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
  subjectId: 'german',
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
