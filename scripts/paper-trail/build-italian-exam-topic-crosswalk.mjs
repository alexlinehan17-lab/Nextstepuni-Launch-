#!/usr/bin/env node
/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 *
 * Reconcile the metadata-only StudyClix Italian hierarchy with NextStepUni's
 * entitled SEC corpus. The reference snapshot contributes factual labels,
 * counts and headings only; no question text, solution, media or PDF is read
 * from or copied from StudyClix.
 *
 * The generator is deliberately additive. It rebuilds the Italian tag wave
 * from the frozen pre-migration baseline plus every audited local answer map,
 * then adds paper-only cards for omissions verified against the official SEC
 * papers. Existing question identities and canonical tags are never replaced.
 */

import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const HERE = path.dirname(fileURLToPath(import.meta.url));
const ROOT = path.resolve(HERE, '../..');
const ANSWERS_ROOT = path.join(HERE, 'answers');
const HOSTED_ROOT = path.join(ROOT, 'public/paper-anchors');
const TAGS_PATH = path.join(HERE, 'topic-tags/tags/italian.json');
const BASELINE_PATH = path.join(ROOT, 'test/fixtures/italianTopicQuestionBaseline.json');
const REFERENCE_PATH = path.join(ROOT, 'data/examTopics/italian.json');
const OUTPUT_PATH = path.join(ROOT, 'data/examTopics/italian-local-crosswalk.json');
const RUNTIME_PATH = path.join(ROOT, 'data/examTopics/italian-runtime.json');
const CURRICULUM_PATH = path.join(ROOT, 'data/examTopics/italian-curriculum-crosswalk.json');

const readJson = file => JSON.parse(fs.readFileSync(file, 'utf8'));
const reference = readJson(REFERENCE_PATH);
const preservationBaseline = readJson(BASELINE_PATH);

const referenceTopics = Object.entries(reference.variants).flatMap(([level, variant]) => (
  variant.topics.map(topic => ({ ...topic, level }))
));
const topicById = new Map(referenceTopics.map(topic => [topic.id, topic]));
const topicIndex = new Map(referenceTopics.map((topic, index) => [topic.id, index]));

if (referenceTopics.length !== 24) throw new Error(`Expected 24 Italian topics, found ${referenceTopics.length}`);

const IDS = {
  higher: {
    conversations: 'italian-higher-aural-conversations',
    news: 'italian-higher-aural-news-itemsstatements',
    essayTreno: 'italian-higher-essay-writing-il-treno-dei-bambini',
    essayMontagne: 'italian-higher-essay-writing-le-otto-montagne',
    oral: 'italian-higher-oral',
    readingTreno: 'italian-higher-reading-comprehension-il-treno-dei-bambini',
    journalistic: 'italian-higher-reading-comprehension-journalistic',
    readingMontagne: 'italian-higher-reading-comprehension-le-otto-montagne',
    literary: 'italian-higher-reading-comprehension-literary-unseen',
    formal: 'italian-higher-written-composition-formal',
    guided: 'italian-higher-written-composition-guided',
    opinion: 'italian-higher-written-composition-opinion-piece',
  },
  ordinary: {
    competitions: 'italian-ordinary-ads-competitions',
    general: 'italian-ordinary-ads-general-advertisements',
    jobs: 'italian-ordinary-ads-job-advertisements',
    rules: 'italian-ordinary-ads-rulessafety-instructions',
    special: 'italian-ordinary-ads-special-offersoccasions',
    conversations: 'italian-ordinary-aural-conversation',
    news: 'italian-ordinary-aural-news-itemsstatements',
    reading: 'italian-ordinary-reading-comprehension',
    correct: 'italian-ordinary-writing-correct-order',
    dialogue: 'italian-ordinary-writing-dialogue',
    form: 'italian-ordinary-writing-fill-in-a-form',
    letter: 'italian-ordinary-writing-informal-letter',
  },
};

const CURRICULUM_CROSSWALK = {
  [IDS.higher.conversations]: ['italian-3-0'],
  [IDS.higher.news]: ['italian-3-1'],
  [IDS.higher.essayTreno]: ['italian-2-1'],
  [IDS.higher.essayMontagne]: ['italian-2-1'],
  [IDS.higher.oral]: [
    'italian-4-0',
    'italian-0-0', 'italian-0-1', 'italian-0-2', 'italian-0-3',
    'italian-0-4', 'italian-0-5', 'italian-0-6', 'italian-0-7',
    'italian-0-8', 'italian-0-9', 'italian-0-10',
  ],
  [IDS.higher.readingTreno]: ['italian-5-2', 'italian-2-1'],
  [IDS.higher.journalistic]: ['italian-5-0'],
  [IDS.higher.readingMontagne]: ['italian-5-2', 'italian-2-1'],
  // Historical prescribed passages are retained in this broad literary
  // practice bucket because the current title-specific menu has no truthful
  // place for superseded novels. The bridge therefore spans both official
  // literary-reading nodes, while provenance remains explicit in the audit.
  [IDS.higher.literary]: ['italian-5-1', 'italian-5-2', 'italian-2-1'],
  [IDS.higher.formal]: ['italian-6-2'],
  [IDS.higher.guided]: ['italian-6-1'],
  [IDS.higher.opinion]: ['italian-6-0'],
  [IDS.ordinary.competitions]: ['italian-5-4'],
  [IDS.ordinary.general]: ['italian-5-4'],
  [IDS.ordinary.jobs]: ['italian-5-4'],
  [IDS.ordinary.rules]: ['italian-5-4'],
  [IDS.ordinary.special]: ['italian-5-4'],
  [IDS.ordinary.conversations]: ['italian-3-0'],
  [IDS.ordinary.news]: ['italian-3-1'],
  [IDS.ordinary.reading]: ['italian-5-3'],
  [IDS.ordinary.correct]: ['italian-6-5'],
  [IDS.ordinary.dialogue]: ['italian-6-3'],
  [IDS.ordinary.form]: ['italian-6-4'],
  [IDS.ordinary.letter]: ['italian-6-3'],
};

for (const topic of referenceTopics) {
  if (!CURRICULUM_CROSSWALK[topic.id]?.length) {
    throw new Error(`Italian topic has no curriculum bridge: ${topic.id}`);
  }
}

const paperIdentity = paper => [
  paper.level,
  paper.lang,
  paper.year,
  paper.paperKey,
  paper.fileid,
].join('|');

const paperMap = new Map();
for (const source of preservationBaseline) {
  const paper = {
    subjectId: 'italian',
    level: source.level,
    lang: source.lang,
    year: source.year,
    fileid: source.fileid,
    paperKey: source.paperKey,
    q: source.questions.map(question => ({ ...question, baseline: true })),
    answerMap: null,
  };
  const identity = paperIdentity(paper);
  if (paperMap.has(identity)) throw new Error(`Duplicate Italian baseline paper: ${identity}`);
  paperMap.set(identity, paper);
}

const parseSidecarIdentity = file => {
  const match = file.match(/^LC013([AG])L(P000|PA00)([EIB])V\.pdf\.json$/i);
  if (!match) throw new Error(`Unexpected Italian answer-map filename: ${file}`);
  return {
    level: match[1].toUpperCase() === 'A' ? 'higher' : 'ordinary',
    paperKey: match[2].toUpperCase() === 'PA00' ? 'aural' : 'single',
    lang: match[3].toUpperCase() === 'I' ? 'iv' : 'ev',
    fileid: file.slice(0, -'.json'.length),
  };
};

const roman = value => ({ I: 1, II: 2, III: 3, IV: 4, V: 5, VI: 6 }[value.toUpperCase()] ?? null);
const groupNumber = raw => /^\d+$/.test(raw) ? Number(raw) : roman(raw);

const ordinaryAGroup = (label, index) => {
  const patterns = [
    /(?:Section|Roinn)\s*A.*?(?:Question|Q|Ceist|Text|Téacs)\s*([12])/i,
    /Reading\s*A.*?Text\s*([12])/i,
    /^Text\s+(I|II)\b/i,
  ];
  for (const pattern of patterns) {
    const raw = label.match(pattern)?.[1];
    if (raw) return groupNumber(raw);
  }
  return index < 2 ? index + 1 : null;
};

const ordinaryBGroup = (label, index, paper, question) => {
  if (paper.year === 2018 && paper.lang === 'iv') return null;
  const patterns = [
    /(?:Section|Roinn)\s*B.*?(?:Question|Q|Ceist|Fógra|Text)\s*(VI|IV|III|II|V|I|\d+)\b/i,
    /^(?:Advert|Ad|Piece)\s*(VI|IV|III|II|V|I|\d+)\b/i,
  ];
  for (const pattern of patterns) {
    const raw = label.match(pattern)?.[1];
    if (raw) return groupNumber(raw);
  }
  if (!label && paper.year === 2010 && index >= 2 && index <= 7) return index - 1;
  if (question.primary === 'italian-5-4' && index >= 2) return index - 1;
  return null;
};

const semanticForSidecar = (paper, question, answerQuestion, index, answerQuestions) => {
  const label = String(answerQuestion.label ?? '');
  if (paper.paperKey === 'aural') return index === 0 ? 'aural-news' : 'aural-conversations';

  if (paper.level === 'higher') {
    if (/(?:Section|Roinn)\s*C|Scríobh na Teanga|Writing/i.test(label)) return 'higher-writing-all';
    if (answerQuestions.length >= 20) {
      if (index < 5) return 'higher-journalistic';
      if (index < 10) return 'higher-literary-unseen';
      return 'higher-prescribed-historic';
    }
    if (index === 0) return 'higher-journalistic';
    if (index === 1) return 'higher-literary-unseen';
    return 'higher-prescribed-historic';
  }

  if (paper.year === 2018 && paper.lang === 'iv') {
    return question.primary === 'italian-6-5' ? 'ordinary-writing-correct' : 'ordinary-reading';
  }
  if (/(?:Section|Roinn)\s*C|Scríobh na Teanga|Writing/i.test(label)) return 'ordinary-writing-all';
  const aGroup = ordinaryAGroup(label, index);
  if (aGroup && (
    /(?:Section|Roinn)\s*A|Reading\s*A|^Text\s+(?:I|II)\b/i.test(label)
    || index < 2
  )) return `ordinary-a-${aGroup}`;
  const bGroup = ordinaryBGroup(label, index, paper, question);
  if (bGroup) return `ordinary-b-${bGroup}`;
  if (question.primary === 'italian-6-5') return 'ordinary-writing-correct';
  if (question.primary === 'italian-6-4') return 'ordinary-writing-form';
  if (question.primary === 'italian-6-3') return 'ordinary-writing-all';
  if (question.primary === 'italian-5-4') return 'ordinary-b-general';
  return 'ordinary-reading';
};

const canonicalForSemantic = semantic => {
  if (semantic === 'aural-news') return { primary: 'italian-3-1' };
  if (semantic === 'aural-conversations') return { primary: 'italian-3-0' };
  if (semantic === 'higher-journalistic') return { primary: 'italian-5-0' };
  if (semantic === 'higher-literary-unseen') return { primary: 'italian-5-1' };
  if (semantic === 'higher-prescribed-historic') return { primary: 'italian-5-2' };
  if (semantic === 'higher-reading-montagne' || semantic === 'higher-reading-treno') {
    return { primary: 'italian-5-2', secondary: 'italian-2-1' };
  }
  if (semantic === 'higher-essay-montagne' || semantic === 'higher-essay-treno') {
    return { primary: 'italian-2-1' };
  }
  if (semantic === 'higher-writing-opinion') return { primary: 'italian-6-0' };
  if (semantic === 'higher-writing-guided') return { primary: 'italian-6-1' };
  if (semantic === 'higher-writing-formal') return { primary: 'italian-6-2' };
  if (semantic === 'higher-writing-all') return { primary: 'italian-6-0', secondary: 'italian-6-1' };
  if (semantic.startsWith('ordinary-a-') || semantic === 'ordinary-reading') {
    return { primary: 'italian-5-3' };
  }
  if (semantic.startsWith('ordinary-b-')) return { primary: 'italian-5-4' };
  if (semantic === 'ordinary-writing-letter' || semantic === 'ordinary-writing-dialogue') {
    return { primary: 'italian-6-3' };
  }
  if (semantic === 'ordinary-writing-form') return { primary: 'italian-6-4' };
  if (semantic === 'ordinary-writing-correct') return { primary: 'italian-6-5' };
  if (semantic === 'ordinary-writing-all') return { primary: 'italian-6-3', secondary: 'italian-6-4' };
  throw new Error(`No canonical Italian tag for semantic card ${semantic}`);
};

const sidecarFiles = fs.readdirSync(ANSWERS_ROOT, { withFileTypes: true })
  .filter(entry => entry.isDirectory() && /^20\d\d$/.test(entry.name))
  .flatMap(entry => fs.readdirSync(path.join(ANSWERS_ROOT, entry.name))
    .filter(file => /^LC013.*\.pdf\.json$/i.test(file))
    .map(file => ({ year: Number(entry.name), file })))
  .sort((a, b) => a.year - b.year || a.file.localeCompare(b.file));

for (const { year, file } of sidecarFiles) {
  const parsed = parseSidecarIdentity(file);
  const candidate = { subjectId: 'italian', year, ...parsed, q: [], answerMap: null };
  const identity = paperIdentity(candidate);
  const paper = paperMap.get(identity) ?? candidate;
  const answerMap = readJson(path.join(ANSWERS_ROOT, String(year), file));
  paper.answerMap = answerMap;

  for (const [index, answerQuestion] of answerMap.q.entries()) {
    let question = paper.q.find(item => item.n === answerQuestion.n);
    if (!question) {
      question = { n: answerQuestion.n };
      paper.q.push(question);
    }
    question.label = answerQuestion.label ?? undefined;
    question.anchor = answerQuestion;
    question.semantic = semanticForSidecar(paper, question, answerQuestion, index, answerMap.q);
    if (!question.primary) Object.assign(question, canonicalForSemantic(question.semantic));
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

const customQuestion = ({ n, label, semantic, start, end = start }) => ({
  n,
  label,
  semantic,
  ...canonicalForSemantic(semantic),
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

const italianPaper = (year, level, paperKey = 'single', lang = 'ev') => {
  const matches = [...paperMap.values()].filter(paper => (
    paper.year === year && paper.level === level && paper.paperKey === paperKey && paper.lang === lang
  ));
  if (matches.length !== 1) {
    throw new Error(`${year} ${level} ${lang} ${paperKey}: expected one Italian paper, found ${matches.length}`);
  }
  return matches[0];
};

// The 2018 English Ordinary answer map stopped after Section B Q4 even though
// the official booklet has Q5 (Internet Safety) on pages 14-15.
addCustom(italianPaper(2018, 'ordinary'), {
  n: 'B5',
  label: 'Section B · Question 5 · Internet Safety',
  semantic: 'ordinary-b-5',
  start: 14,
  end: 15,
});

// The classic 2019-2025 answer maps omit the complete writing section. These
// card boundaries were checked against each official SEC booklet.
for (let year = 2019; year <= 2025; year++) {
  const higherMatches = [...paperMap.values()].filter(paper => (
    paper.year === year && paper.level === 'higher' && paper.lang === 'ev' && paper.paperKey === 'single'
  ));
  for (const paper of higherMatches) {
    const compact = year <= 2020;
    addCustom(paper, {
      n: 'C1', label: 'Section C · Question 1 · Opinion Piece',
      semantic: 'higher-writing-opinion', start: 12, end: compact ? 12 : 13,
    });
    addCustom(paper, {
      n: 'C2', label: 'Section C · Question 2 · Guided Composition',
      semantic: 'higher-writing-guided', start: compact ? 13 : 14, end: compact ? 13 : 15,
    });
    addCustom(paper, {
      n: 'C3', label: 'Section C · Question 3 · Formal Writing',
      semantic: 'higher-writing-formal', start: compact ? 14 : 16, end: compact ? 15 : 17,
    });
  }

  const ordinaryMatches = [...paperMap.values()].filter(paper => (
    paper.year === year && paper.level === 'ordinary' && paper.lang === 'ev' && paper.paperKey === 'single'
  ));
  for (const paper of ordinaryMatches) {
    addCustom(paper, {
      n: 'C1A', label: 'Section C · Question 1(a) · Informal Letter',
      semantic: 'ordinary-writing-letter', start: 16,
    });
    addCustom(paper, {
      n: 'C1B', label: 'Section C · Question 1(b) · Dialogue',
      semantic: 'ordinary-writing-dialogue', start: 17,
    });
    addCustom(paper, {
      n: 'C2', label: 'Section C · Question 2 · Fill in a Form',
      semantic: 'ordinary-writing-form', start: 18,
    });
    addCustom(paper, {
      n: 'C3', label: 'Section C · Question 3 · Correct Order',
      semantic: 'ordinary-writing-correct', start: 19,
    });
  }
}

const add2026Paper = (level, fileid) => {
  const paper = {
    subjectId: 'italian', level, lang: 'ev', year: 2026, fileid, paperKey: 'single', q: [], answerMap: null,
  };
  const identity = paperIdentity(paper);
  if (paperMap.has(identity)) throw new Error(`2026 Italian paper already exists: ${identity}`);
  paperMap.set(identity, paper);
  return paper;
};

const higher2026 = add2026Paper('higher', 'LC013ALP000BV.pdf');
for (let number = 1; number <= 5; number++) {
  addCustom(higher2026, {
    n: String(number), label: `Section A · Journalistic · Question ${number}`,
    semantic: 'higher-journalistic', start: 3,
  });
  addCustom(higher2026, {
    n: String(number + 5), label: `Section B1 · Literary Unseen · Question ${number}`,
    semantic: 'higher-literary-unseen', start: 5,
  });
  addCustom(higher2026, {
    n: String(number + 10), label: `Section B2 · Le otto montagne · Question ${number}`,
    semantic: 'higher-reading-montagne', start: 7,
  });
  addCustom(higher2026, {
    n: String(number + 15), label: `Section B2 · Il treno dei bambini · Question ${number}`,
    semantic: 'higher-reading-treno', start: 9,
  });
}
addCustom(higher2026, {
  n: '21', label: 'Section B · Essay · Le otto montagne',
  semantic: 'higher-essay-montagne', start: 10,
});
addCustom(higher2026, {
  n: '22', label: 'Section B · Essay · Il treno dei bambini',
  semantic: 'higher-essay-treno', start: 10,
});
addCustom(higher2026, {
  n: '23', label: 'Section C · Question 1 · Opinion Piece',
  semantic: 'higher-writing-opinion', start: 12, end: 13,
});
addCustom(higher2026, {
  n: '24', label: 'Section C · Question 2 · Guided Composition',
  semantic: 'higher-writing-guided', start: 14, end: 15,
});
addCustom(higher2026, {
  n: '25', label: 'Section C · Question 3 · Formal Writing',
  semantic: 'higher-writing-formal', start: 16, end: 17,
});
higher2026.q.sort((a, b) => Number(a.n) - Number(b.n));

const ordinary2026 = add2026Paper('ordinary', 'LC013GLP000BV.pdf');
const ordinary2026Specs = [
  ['1', 'Section A · Question 1 · Reading Comprehension', 'ordinary-a-1', 2, 3],
  ['2', 'Section A · Question 2 · Reading Comprehension', 'ordinary-a-2', 4, 5],
  ['3', 'Section B · Question 1 · Job Advertisements', 'ordinary-b-1', 6, 7],
  ['4', 'Section B · Question 2 · Chocohotel', 'ordinary-b-2', 8, 9],
  ['5', 'Section B · Question 3 · Travel Offers', 'ordinary-b-3', 10, 11],
  ['6', 'Section B · Question 4 · Cinema Festival', 'ordinary-b-4', 12, 13],
  ['7', 'Section B · Question 5 · Interview Advice', 'ordinary-b-5', 14, 15],
  ['8', 'Section C · Question 1(a) · Informal Letter', 'ordinary-writing-letter', 16, 16],
  ['9', 'Section C · Question 1(b) · Dialogue', 'ordinary-writing-dialogue', 17, 17],
  ['10', 'Section C · Question 2 · Fill in a Form', 'ordinary-writing-form', 18, 18],
  ['11', 'Section C · Question 3 · Correct Order', 'ordinary-writing-correct', 19, 19],
];
for (const [n, label, semantic, start, end] of ordinary2026Specs) {
  addCustom(ordinary2026, { n, label, semantic, start, end });
}

const localPapers = [...paperMap.values()].sort((a, b) => (
  b.year - a.year
  || a.level.localeCompare(b.level)
  || a.lang.localeCompare(b.lang)
  || a.paperKey.localeCompare(b.paperKey)
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
  if (!year) throw new Error(`Italian heading has no year: ${heading}`);
  return year;
};
const sectionQuestion = (heading, section) => Number(
  heading.match(new RegExp(`Section\\s+${section}\\s+-\\s+Question\\s+(\\d+)`, 'i'))?.[1],
);

const ordinaryBTopics = new Map();
const addOrdinaryBTopic = (year, group, id) => {
  const key = `${year}|${group}`;
  const ids = ordinaryBTopics.get(key) ?? [];
  if (!ids.includes(id)) ids.push(id);
  ordinaryBTopics.set(key, ids);
};
for (const topic of reference.variants.ordinary.topics.filter(item => item.id.includes('-ads-'))) {
  for (const heading of topic.officialQuestionHeadings) {
    const year = parseYear(heading);
    const group = sectionQuestion(heading, 'B');
    if (year >= 2010 && group) addOrdinaryBTopic(year, group, topic.id);
  }
}
for (const [year, mapping] of Object.entries({
  2023: {
    1: IDS.ordinary.jobs,
    2: IDS.ordinary.general,
    3: IDS.ordinary.special,
    4: IDS.ordinary.rules,
    5: IDS.ordinary.general,
  },
  2026: {
    1: IDS.ordinary.jobs,
    2: IDS.ordinary.general,
    3: IDS.ordinary.special,
    4: IDS.ordinary.special,
    5: IDS.ordinary.rules,
  },
})) {
  for (const [group, id] of Object.entries(mapping)) addOrdinaryBTopic(Number(year), Number(group), id);
}

const semanticsForTopic = topicId => {
  if (topicId === IDS.higher.news || topicId === IDS.ordinary.news) return ['aural-news'];
  if (topicId === IDS.higher.conversations || topicId === IDS.ordinary.conversations) return ['aural-conversations'];
  if (topicId === IDS.higher.journalistic) return ['higher-journalistic'];
  if (topicId === IDS.higher.formal) return ['higher-writing-formal', 'higher-writing-all'];
  if (topicId === IDS.higher.guided) return ['higher-writing-guided', 'higher-writing-all'];
  if (topicId === IDS.higher.opinion) return ['higher-writing-opinion', 'higher-writing-all'];
  if (topicId === IDS.ordinary.reading) return ['ordinary-reading'];
  if (topicId === IDS.ordinary.correct) return ['ordinary-writing-correct', 'ordinary-writing-all'];
  if (topicId === IDS.ordinary.dialogue) return ['ordinary-writing-dialogue', 'ordinary-writing-all'];
  if (topicId === IDS.ordinary.letter) return ['ordinary-writing-letter', 'ordinary-writing-all'];
  return [];
};

const resolveHeading = (topic, heading) => {
  const year = parseYear(heading);
  const paperKey = /Aural Paper/i.test(heading) ? 'aural' : 'single';
  if (year < 2010) {
    return {
      topicId: topic.id,
      heading,
      year,
      paperKey,
      resolution: 'source-blocked',
      reason: 'The entitled local SEC question corpus begins in 2010. The factual 2009 heading is retained, but no StudyClix-hosted question, solution, image or PDF is copied.',
    };
  }
  const paper = italianPaper(year, topic.level, paperKey);
  let candidates = [];
  if (topic.id.includes('-ads-')) {
    const group = sectionQuestion(heading, 'B');
    candidates = paper.q.filter(question => question.semantic === `ordinary-b-${group}`);
  } else if (topic.id === IDS.ordinary.reading) {
    const group = sectionQuestion(heading, 'A');
    candidates = paper.q.filter(question => (
      question.semantic === `ordinary-a-${group}`
      || (question.semantic === 'ordinary-reading' && question.n === String(group))
    ));
  } else {
    const semantics = semanticsForTopic(topic.id);
    candidates = paper.q.filter(question => semantics.includes(question.semantic));
  }
  if (!candidates.length) {
    throw new Error(`${topic.id}: no local Italian card resolves ${heading}`);
  }
  return {
    topicId: topic.id,
    heading,
    year,
    paperKey,
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

const associations = referenceTopics.flatMap(topic => (
  topic.officialQuestionHeadings.map(heading => resolveHeading(topic, heading))
));
const matched = associations.filter(association => association.resolution === 'matched');
const sourceBlocked = associations.filter(association => association.resolution === 'source-blocked');
if (associations.length !== 340 || matched.length !== 317 || sourceBlocked.length !== 23) {
  throw new Error(`Italian reference boundary mismatch: ${matched.length}/${associations.length}, blocked=${sourceBlocked.length}`);
}

const localQuestionIdentity = (paper, number) => [
  paper.level, paper.lang, paper.year, paper.paperKey, number,
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
  const semantic = question.semantic;
  if (semantic === 'aural-news') {
    return [paper.level === 'higher' ? IDS.higher.news : IDS.ordinary.news];
  }
  if (semantic === 'aural-conversations') {
    return [paper.level === 'higher' ? IDS.higher.conversations : IDS.ordinary.conversations];
  }
  if (semantic === 'higher-journalistic') return [IDS.higher.journalistic];
  if (semantic === 'higher-literary-unseen' || semantic === 'higher-prescribed-historic') {
    return [IDS.higher.literary];
  }
  if (semantic === 'higher-reading-montagne') return [IDS.higher.readingMontagne];
  if (semantic === 'higher-reading-treno') return [IDS.higher.readingTreno];
  if (semantic === 'higher-essay-montagne') return [IDS.higher.essayMontagne];
  if (semantic === 'higher-essay-treno') return [IDS.higher.essayTreno];
  if (semantic === 'higher-writing-opinion') return [IDS.higher.opinion];
  if (semantic === 'higher-writing-guided') return [IDS.higher.guided];
  if (semantic === 'higher-writing-formal') return [IDS.higher.formal];
  if (semantic === 'higher-writing-all') return [IDS.higher.opinion, IDS.higher.guided, IDS.higher.formal];
  if (semantic === 'ordinary-reading' || semantic.startsWith('ordinary-a-')) return [IDS.ordinary.reading];
  if (semantic.startsWith('ordinary-b-')) {
    const group = Number(semantic.split('-').at(-1));
    return ordinaryBTopics.get(`${paper.year}|${group}`) ?? [IDS.ordinary.general];
  }
  if (semantic === 'ordinary-writing-letter') return [IDS.ordinary.letter];
  if (semantic === 'ordinary-writing-dialogue') return [IDS.ordinary.dialogue];
  if (semantic === 'ordinary-writing-form') return [IDS.ordinary.form];
  if (semantic === 'ordinary-writing-correct') return [IDS.ordinary.correct];
  if (semantic === 'ordinary-writing-all') {
    return [IDS.ordinary.letter, IDS.ordinary.dialogue, IDS.ordinary.form, IDS.ordinary.correct];
  }
  throw new Error(`${paperIdentity(paper)} Q${question.n}: no Italian exam-topic fallback for ${semantic}`);
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
    n: question.n,
    topicIds,
    provenance: referenced.length
      ? fallback.some(id => !referenced.includes(id)) ? 'reference+retained-local' : 'reference'
      : question.semantic === 'higher-prescribed-historic'
        ? 'retained-local-historic-literary'
        : 'retained-local',
  };
}));

const duplicateMappings = localQuestionMappings
  .map(mapping => [mapping.level, mapping.lang, mapping.year, mapping.paperKey, mapping.n].join('|'))
  .filter((identity, index, identities) => identities.indexOf(identity) !== index);
if (duplicateMappings.length) {
  throw new Error(`Duplicate Italian local question mappings: ${[...new Set(duplicateMappings)].join(', ')}`);
}

const tagPapers = localPapers.map(paper => ({
  subjectId: 'italian',
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
  let paperRegion = source.paperRegion;
  if (!paperRegion && (question.semantic === 'higher-writing-all' || question.semantic === 'ordinary-writing-all')) {
    paperRegion = fullPages(source.pP, source.pP + 3);
  }
  if (!paperRegion) paperRegion = fullPages(source.pP);
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
    component: paper.paperKey === 'aural' ? 'A00' : '000',
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
const summary = {
  referenceTopics: referenceTopics.length,
  referenceReportedAssociations: referenceTopics.reduce((sum, topic) => sum + topic.reportedQuestionCount, 0),
  referenceOfficialAssociations: associations.length,
  referenceMockAssociations: referenceTopics.reduce((sum, topic) => sum + topic.mockQuestionCount, 0),
  referenceProviderSampleAssociations: referenceTopics.reduce((sum, topic) => sum + topic.providerSampleQuestionCount, 0),
  matchedAssociations: matched.length,
  sourceBlockedAssociations: sourceBlocked.length,
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
  subjectId: 'italian',
  capturedAt: reference.capturedAt,
  policy: {
    matchedSource: 'Entitled local State Examinations Commission corpus only.',
    excludedContent: 'No commercial mock question, solution, note, question text, StudyClix image or StudyClix-hosted PDF is copied.',
    historicalLiterature: 'Superseded prescribed-text cards remain available in the broad Literary practice bucket and are never mislabeled as a current prescribed title.',
  },
  summary,
  associations,
  localQuestionMappings,
  hostedAnchorMaps,
};
fs.writeFileSync(OUTPUT_PATH, `${JSON.stringify(output, null, 2)}\n`);
fs.writeFileSync(CURRICULUM_PATH, `${JSON.stringify(CURRICULUM_CROSSWALK, null, 2)}\n`);

const paperKeyCode = paperKey => paperKey === 'aural' ? 'a' : 's';
const referenceNumber = heading => heading.match(/Question\s+(\d+)/i)?.[1] ?? '1';
const runtimePartReferences = associations.flatMap(association => {
  const index = topicIndex.get(association.topicId);
  if (association.resolution === 'matched') {
    return association.target.questionNumbers.map(number => [
      index,
      association.year - 2000,
      association.target.level === 'higher' ? 'h' : 'o',
      paperKeyCode(association.target.paperKey),
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
    referenceNumber(association.heading),
    association.heading,
  ]];
});

const runtime = {
  v: 1,
  subjectId: 'italian',
  capturedAt: reference.capturedAt,
  referenceProvider: reference.reference.provider,
  groups: Object.entries(reference.variants).map(([level, variant]) => [
    level === 'higher' ? 'h' : 'o',
    variant.label,
    variant.topics.map(topic => topicIndex.get(topic.id)),
  ]),
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
