#!/usr/bin/env node
/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 *
 * Reconcile the metadata-only StudyClix Irish hierarchy with NextStepUni's
 * entitled SEC corpus. The reference contributes factual labels, hierarchy,
 * counts and official headings only; no provider question text, solutions,
 * notes, media or hosted PDFs are copied.
 *
 * The generator is additive. It begins with the frozen Irish topic-card
 * baseline, retains every established id/tag verbatim, then restores the
 * omitted listening, composition, literature and Foundation paper sections.
 */

import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const HERE = path.dirname(fileURLToPath(import.meta.url));
const ROOT = path.resolve(HERE, '../..');
const PAPERS_ROOT = path.join(ROOT, 'paper-trail-corpus/exampapers');
const ANSWERS_ROOT = path.join(HERE, 'answers');
const HOSTED_ROOT = path.join(ROOT, 'public/paper-anchors');
const TAGS_PATH = path.join(HERE, 'topic-tags/tags/irish.json');
const BASELINE_PATH = path.join(ROOT, 'test/fixtures/irishTopicQuestionBaseline.json');
const REFERENCE_PATH = path.join(ROOT, 'data/examTopics/irish.json');
const OUTPUT_PATH = path.join(ROOT, 'data/examTopics/irish-local-crosswalk.json');
const RUNTIME_PATH = path.join(ROOT, 'data/examTopics/irish-runtime.json');
const CURRICULUM_PATH = path.join(ROOT, 'data/examTopics/irish-curriculum-crosswalk.json');

const readJson = file => JSON.parse(fs.readFileSync(file, 'utf8'));
const reference = readJson(REFERENCE_PATH);
const preservationBaseline = readJson(BASELINE_PATH);
const referenceTopics = Object.entries(reference.variants).flatMap(([level, variant]) => (
  variant.topics.map(topic => ({ ...topic, level, referenceTopic: true }))
));
if (referenceTopics.length !== 62) {
  throw new Error('Expected 62 Irish reference topics, found ' + referenceTopics.length);
}

const EXTENSIONS = [
  {
    id: 'irish-higher-historic-additional-literature',
    label: 'Historic Additional Literature (NextStepUni archive)',
    level: 'higher',
    sourcePath: '/nextstepuni-preservation/irish/higher/historic-additional-literature',
    reportedQuestionCount: 0,
    officialQuestionHeadings: [],
    mockQuestionCount: 0,
    providerSampleQuestionCount: 0,
    extractedQuestionCount: 0,
    referenceTopic: false,
  },
  {
    id: 'irish-foundation-aural-cluastuiscint',
    label: 'Cluastuiscint (NextStepUni archive)',
    level: 'foundation',
    sourcePath: '/nextstepuni-preservation/irish/foundation/cluastuiscint',
    reportedQuestionCount: 0,
    officialQuestionHeadings: [],
    mockQuestionCount: 0,
    providerSampleQuestionCount: 0,
    extractedQuestionCount: 0,
    referenceTopic: false,
  },
];
const allTopics = [...referenceTopics, ...EXTENSIONS];
const topicById = new Map(allTopics.map(topic => [topic.id, topic]));
const topicIndex = new Map(allTopics.map((topic, index) => [topic.id, index]));
const topicByLabel = new Map(referenceTopics.map(topic => [topic.level + '|' + topic.label, topic.id]));
const topicId = (level, label) => {
  const id = topicByLabel.get(level + '|' + label);
  if (!id) throw new Error('Missing Irish reference topic: ' + level + ' · ' + label);
  return id;
};

const H = {
  conversation: topicId('higher', 'Aural - Comhrá (Conversation)'),
  announcement: topicId('higher', 'Aural - Fógra (Announcement)'),
  news: topicId('higher', 'Aural - Píosa Nuachta (News Pieces)'),
  extraPoetry: topicId('higher', 'Dánta Breise'),
  grammar: topicId('higher', 'Grammar'),
  oral: topicId('higher', 'Oral Exam'),
  reading: topicId('higher', 'Reading Comprehension'),
  poetry: topicId('higher', 'Studied Poetry (Filiocht Roghnach)'),
  prose: topicId('higher', 'Studied Prose (Pros Roghnach)'),
  debate: topicId('higher', 'Write a Debate..'),
  article: topicId('higher', 'Write a News/Magazine Article..'),
  story: topicId('higher', 'Write a Story..'),
  essay: topicId('higher', 'Write an Essay..'),
  historic: EXTENSIONS[0].id,
};
const O = {
  conversation: topicId('ordinary', 'AURAL - Comhrá (Conversation)'),
  news: topicId('ordinary', 'AURAL - Píosa Nuachta (News Pieces)'),
  announcement: topicId('ordinary', 'AURALS - Fógra (Announcement)'),
  grammar: topicId('ordinary', 'Grammar'),
  oral: topicId('ordinary', 'Oral exam'),
  reading: topicId('ordinary', 'Reading Comprehension'),
  blog: topicId('ordinary', 'Write a Blog/Creative Writing Task'),
  writtenConversation: topicId('ordinary', 'Write a Conversation..'),
  debate: topicId('ordinary', 'Write a Debate..'),
  letter: topicId('ordinary', 'Write a Letter/Email...'),
  story: topicId('ordinary', 'Write a Story..'),
  folktale: topicId('ordinary', 'Write About a Studied Folktale...'),
  poetry: topicId('ordinary', 'Write About a Studied Poem (Optional)...'),
  prose: topicId('ordinary', 'Write About a Studied Prose (Optional)...'),
};
const F = {
  form: topicId('foundation', 'Fill in a Form..'),
  match: topicId('foundation', 'Match the Pictures With the Text'),
  brochure: topicId('foundation', 'Reading - Brochure'),
  extract: topicId('foundation', 'Reading - Extract'),
  letterReading: topicId('foundation', 'Reading - Letter'),
  news: topicId('foundation', 'Reading - Newspaper Article'),
  poem: topicId('foundation', 'Reading - Poem'),
  letterWriting: topicId('foundation', 'Write a Letter...'),
  notice: topicId('foundation', 'Write a Notice...'),
  story: topicId('foundation', 'Write a Story...'),
  pictures: topicId('foundation', 'Write From Pictures...'),
  aural: EXTENSIONS[1].id,
};

const NEW_POETRY = {
  'Deireadh na Féide': 'irish-5-8',
  'Dínit an Bhróin': 'irish-5-7',
  'Glaoch Abhaile': 'irish-5-10',
  'Iníon': 'irish-5-9',
  'Úirchill an Chreagáin': 'irish-5-11',
};
const NEW_PROSE = {
  'An Glantóir': 'irish-4-11',
  'An tIriseoir': 'irish-4-14',
  Athair: 'irish-4-10',
  'Clann Lir': 'irish-4-9',
  Cuairteoir: 'irish-4-13',
  'Dordán': 'irish-6-14',
  'Eoinín na nÉan': 'irish-4-15',
};

const CURRICULUM_CROSSWALK = {};
const setCurriculum = (id, nodes) => { CURRICULUM_CROSSWALK[id] = nodes; };
setCurriculum(H.conversation, ['irish-1-1', 'irish-1-3']);
setCurriculum(H.announcement, ['irish-1-0', 'irish-1-3']);
setCurriculum(H.news, ['irish-1-2', 'irish-1-3']);
setCurriculum(H.extraPoetry, ['irish-6-5']);
setCurriculum(H.grammar, ['irish-3-3', 'irish-8-4']);
setCurriculum(H.oral, ['irish-0-0', 'irish-0-1', 'irish-0-2', 'irish-0-3', 'irish-0-4', 'irish-0-5', 'irish-0-6']);
setCurriculum(H.reading, ['irish-3-0', 'irish-3-1', 'irish-3-2']);
setCurriculum(H.poetry, ['irish-5-6', 'irish-7-0']);
setCurriculum(H.prose, ['irish-4-7', 'irish-7-0']);
setCurriculum(H.debate, ['irish-2-4', 'irish-2-5']);
setCurriculum(H.article, ['irish-2-1']);
setCurriculum(H.story, ['irish-2-3']);
setCurriculum(H.essay, ['irish-2-0']);
setCurriculum(H.historic, ['irish-6-0', 'irish-6-1', 'irish-6-2', 'irish-6-3', 'irish-6-4', 'irish-6-5', 'irish-6-6', 'irish-6-7', 'irish-6-8', 'irish-6-9', 'irish-6-10', 'irish-7-0']);
setCurriculum(O.conversation, ['irish-1-1', 'irish-1-3']);
setCurriculum(O.news, ['irish-1-2', 'irish-1-3']);
setCurriculum(O.announcement, ['irish-1-0', 'irish-1-3']);
setCurriculum(O.grammar, ['irish-8-4']);
setCurriculum(O.oral, ['irish-0-0', 'irish-0-1', 'irish-0-2', 'irish-0-3', 'irish-0-4', 'irish-0-5', 'irish-0-6']);
setCurriculum(O.reading, ['irish-3-0', 'irish-3-1', 'irish-3-2']);
setCurriculum(O.blog, ['irish-2-2', 'irish-2-6']);
setCurriculum(O.writtenConversation, ['irish-2-9']);
setCurriculum(O.debate, ['irish-2-4']);
setCurriculum(O.letter, ['irish-2-8']);
setCurriculum(O.story, ['irish-2-3']);
setCurriculum(O.folktale, ['irish-4-7', 'irish-7-1']);
setCurriculum(O.poetry, ['irish-5-6', 'irish-7-0']);
setCurriculum(O.prose, ['irish-4-7', 'irish-7-0']);
setCurriculum(F.form, ['irish-9-0']);
setCurriculum(F.match, ['irish-9-1']);
for (const id of [F.brochure, F.extract, F.letterReading, F.news, F.poem]) {
  setCurriculum(id, ['irish-9-2', 'irish-3-2']);
}
setCurriculum(F.letterWriting, ['irish-9-3', 'irish-2-8']);
setCurriculum(F.notice, ['irish-9-3', 'irish-8-2']);
setCurriculum(F.story, ['irish-9-3', 'irish-2-3']);
setCurriculum(F.pictures, ['irish-9-4', 'irish-8-2']);
setCurriculum(F.aural, ['irish-1-3']);

for (const topic of referenceTopics) {
  if (topic.id.includes('-poetry-') && !CURRICULUM_CROSSWALK[topic.id]) {
    const title = topic.label.replace(/^Poetry - /, '');
    setCurriculum(topic.id, [NEW_POETRY[title]]);
  }
  if (topic.id.includes('-prose-') && !CURRICULUM_CROSSWALK[topic.id]) {
    const title = topic.label.replace(/^Prose - /, '');
    setCurriculum(topic.id, [NEW_PROSE[title]]);
  }
}
for (const topic of allTopics) {
  if (!CURRICULUM_CROSSWALK[topic.id]?.filter(Boolean).length) {
    throw new Error('Irish topic has no curriculum bridge: ' + topic.id);
  }
}

const canonicalForTopicIds = ids => {
  const canonical = [...new Set(ids.flatMap(id => CURRICULUM_CROSSWALK[id] ?? []))];
  if (!canonical.length) throw new Error('No canonical Irish tags for ' + ids.join(', '));
  return {
    primary: canonical[0],
    ...(canonical[1] ? { secondary: canonical[1] } : {}),
  };
};
const fullPages = (start, end = start) => Array.from(
  { length: Math.max(1, end - start + 1) },
  (_, offset) => ({ p: start + offset, r: [0, 0, 1, 1] }),
);
const anchorAt = (pP, label) => ({
  label,
  pP,
  pY: [0, 1],
  paperRegion: fullPages(pP),
});
const cloneAnchor = (source, fallbackPage, label) => {
  if (!source || !Number.isFinite(source.pP)) return anchorAt(fallbackPage, label);
  return {
    label: label ?? source.label,
    pP: source.pP,
    pY: Array.isArray(source.pY) ? source.pY : [0, 1],
    ...(source.paperRegion ? { paperRegion: source.paperRegion } : {}),
    ...(source.endP !== undefined ? { endP: source.endP } : {}),
    ...(source.endY !== undefined ? { endY: source.endY } : {}),
  };
};

const baselineByFile = new Map(preservationBaseline.map(paper => [paper.year + '|' + paper.fileid, paper]));
const paperFiles = fs.readdirSync(PAPERS_ROOT, { withFileTypes: true })
  .filter(entry => entry.isDirectory() && /^20\d\d$/.test(entry.name))
  .flatMap(entry => fs.readdirSync(path.join(PAPERS_ROOT, entry.name))
    .filter(file => /^LC001[AGB]LP(?:100|200|A00|000)IV\.pdf$/i.test(file))
    .map(file => ({ year: Number(entry.name), file })))
  .sort((a, b) => a.year - b.year || a.file.localeCompare(b.file));
if (paperFiles.length !== 91) {
  throw new Error('Expected 91 Irish SEC paper components, found ' + paperFiles.length);
}

const parsePaper = ({ year, file }) => {
  const match = file.match(/^LC001([AGB])LP(100|200|A00|000)IV\.pdf$/i);
  if (!match) throw new Error('Unexpected Irish paper filename: ' + file);
  const level = match[1].toUpperCase() === 'A'
    ? 'higher'
    : match[1].toUpperCase() === 'G'
      ? 'ordinary'
      : 'foundation';
  const component = match[2].toUpperCase();
  const baseline = baselineByFile.get(year + '|' + file);
  const paperKey = baseline?.paperKey
    ?? (component === '200' ? 'p2' : component === 'A00' ? 'aural' : component === '100' ? 'p1' : 'single');
  const kind = level === 'foundation'
    ? (component === 'A00' ? 'foundation-aural' : 'foundation')
    : (component === '200' ? 'p2' : component === 'A00' ? 'aural' : 'p1');
  return { subjectId: 'irish', year, level, lang: 'iv', fileid: file, component, paperKey, kind, baseline };
};

const baselineBaseTopics = (paper, question) => {
  const n = Number(question.n);
  if (paper.level === 'higher' && paper.kind === 'p2') {
    if (n === 6) return [H.reading, H.grammar];
    if (n === 12) return [H.reading, H.grammar];
    return [H.reading];
  }
  if (paper.level === 'ordinary' && paper.kind === 'p2') return [O.reading];
  if (paper.level === 'foundation' && paper.kind === 'foundation-aural') return [F.aural];
  throw new Error('Unexpected Irish baseline card: ' + paper.year + ' ' + paper.fileid + ' Q' + question.n);
};
const baselineSlots = (paper, question) => {
  const n = Number(question.n);
  if (paper.level === 'higher' && paper.kind === 'p2') {
    if (n <= 5) return ['R-A'];
    if (n === 6) return ['R-A', 'G-A'];
    if (n <= 11) return ['R-B'];
    return ['R-B', 'G-B'];
  }
  if (paper.level === 'ordinary' && paper.kind === 'p2') return [n <= 5 ? 'R-A' : 'R-B'];
  return [];
};

const levelIds = level => level === 'higher' ? H : O;
const modernWritingSlots = paper => {
  if (paper.level === 'higher') {
    const slots = [
      ['W-A', [H.essay]],
      ['W-B', [H.story]],
      ['W-C', [paper.year <= 2012 ? H.article : H.debate]],
    ];
    if (paper.year <= 2012) slots.push(['W-D', [H.debate]]);
    const articleYears = new Set(reference.variants.higher.topics
      .find(topic => topic.id === H.article)
      .officialQuestionHeadings
      .filter(heading => !/Deferred|Sample/i.test(heading))
      .map(heading => Number(heading.slice(0, 4))));
    if (articleYears.has(paper.year)) slots[0][1].push(H.article);
    return slots;
  }
  return [
    ['W-A', [O.blog]],
    ['W-B', [O.story]],
    ['W-C', paper.year === 2016 ? [O.letter, O.writtenConversation] : [O.letter]],
    ['W-D', [O.writtenConversation]],
  ];
};
const fallbackLayout = paper => {
  if (paper.kind === 'aural') {
    return paper.level === 'higher'
      ? { aural: [3, 5, 8] }
      : { aural: [1, 3, 4] };
  }
  if (paper.kind === 'p1') {
    if (paper.year <= 2011) {
      return paper.level === 'higher'
        ? { writing: 3, reading: [4, 6] }
        : { writing: 2, reading: [3, 4] };
    }
    if (paper.year === 2012) {
      return paper.level === 'higher'
        ? { aural: [2, 3, 5], writing: 7 }
        : { aural: [3, 4, 5], writing: 7 };
    }
    return { aural: [3, 4, paper.level === 'higher' ? 6 : 5], writing: 7 };
  }
  if (paper.kind === 'p2') {
    if (paper.year <= 2011) {
      return paper.level === 'higher'
        ? { prose: 3, extra: 4, poetry: 8 }
        : { prose: 2, poetry: 3, proseOptional: 5, poetryOptional: 6 };
    }
    return paper.level === 'higher'
      ? { reading: [4, 6], prose: 8, poetry: 9, extra: 12 }
      : { reading: [4, 6], prose: 8, poetry: 10 };
  }
  if (paper.kind === 'foundation') {
    if (paper.year <= 2011) return { readingStart: 2, writingStart: 10 };
    return { listeningStart: paper.year >= 2023 ? 3 : 2, readingStart: paper.year >= 2023 ? 6 : 5, writingStart: 14 };
  }
  return { listeningStart: 2 };
};

const papers = paperFiles.map(parsePaper);
const paperByIdentity = new Map();
for (const paper of papers) {
  const sidecarPath = path.join(ANSWERS_ROOT, String(paper.year), paper.fileid + '.json');
  paper.sidecar = fs.existsSync(sidecarPath) ? readJson(sidecarPath) : null;
  const hostedPath = path.join(HOSTED_ROOT, String(paper.year), paper.fileid + '.json');
  paper.existingHosted = fs.existsSync(hostedPath) ? readJson(hostedPath) : null;
  paper.layout = fallbackLayout(paper);
  paper.q = [];
  paperByIdentity.set(paper.level + '|' + paper.year + '|' + paper.kind, paper);
}

const existingAnchorFor = (paper, n) => (
  paper.existingHosted?.q?.find(question => String(question.n) === String(n))
  ?? paper.sidecar?.q?.find(question => String(question.n) === String(n))
  ?? null
);
const addQuestion = (paper, config) => {
  if (paper.q.some(question => String(question.n) === String(config.n))) {
    throw new Error(paper.fileid + ': duplicate Irish card ' + config.n);
  }
  const baseTopicIds = [...new Set(config.baseTopicIds)];
  if (!baseTopicIds.length || baseTopicIds.some(id => topicById.get(id)?.level !== paper.level)) {
    throw new Error(paper.fileid + ' Q' + config.n + ': invalid base topic ids ' + baseTopicIds.join(', '));
  }
  paper.q.push({
    n: String(config.n),
    label: config.label,
    referenceSlots: config.referenceSlots ?? [],
    baseTopicIds,
    ...(config.baselineTag ?? canonicalForTopicIds(baseTopicIds)),
    anchor: cloneAnchor(config.anchor, config.fallbackPage ?? 1, config.label),
    baseline: Boolean(config.baselineTag),
  });
};
const ensureQuestion = (paper, config) => {
  const existing = paper.q.find(question => String(question.n) === String(config.n));
  if (existing) {
    existing.referenceSlots = [...new Set([...(existing.referenceSlots ?? []), ...(config.referenceSlots ?? [])])];
    existing.baseTopicIds = [...new Set([...(existing.baseTopicIds ?? []), ...config.baseTopicIds])];
    return existing;
  }
  addQuestion(paper, config);
  return paper.q.at(-1);
};
const sectionAnchor = (paper, n, fallbackPage, label) => (
  cloneAnchor(paper.sidecar?.q?.find(question => String(question.n) === String(n)), fallbackPage, label)
);

for (const paper of papers) {
  if (paper.baseline) {
    for (const question of paper.baseline.questions) {
      addQuestion(paper, {
        n: question.n,
        label: existingAnchorFor(paper, question.n)?.label ?? ('Question ' + question.n),
        referenceSlots: baselineSlots(paper, question),
        baseTopicIds: baselineBaseTopics(paper, question),
        baselineTag: {
          primary: question.primary,
          ...(question.secondary ? { secondary: question.secondary } : {}),
        },
        anchor: existingAnchorFor(paper, question.n),
        fallbackPage: 1,
      });
    }
  }

  if (paper.kind === 'aural') {
    const ids = levelIds(paper.level);
    const topics = [ids.announcement, ids.conversation, ids.news];
    const labels = ['Cluastuiscint · Cuid A', 'Cluastuiscint · Cuid B', 'Cluastuiscint · Cuid C'];
    for (let index = 0; index < 3; index += 1) {
      ensureQuestion(paper, {
        n: String(index + 1),
        label: labels[index],
        referenceSlots: ['A' + (index + 1)],
        baseTopicIds: [topics[index]],
        anchor: existingAnchorFor(paper, String(index + 1)),
        fallbackPage: paper.layout.aural[index],
      });
    }
    continue;
  }

  if (paper.kind === 'p1') {
    const ids = levelIds(paper.level);
    if (paper.year >= 2012) {
      const topics = [ids.announcement, ids.conversation, ids.news];
      const labels = ['Cluastuiscint · Cuid A', 'Cluastuiscint · Cuid B', 'Cluastuiscint · Cuid C'];
      for (let index = 0; index < 3; index += 1) {
        ensureQuestion(paper, {
          n: String(index + 1),
          label: labels[index],
          referenceSlots: ['A' + (index + 1)],
          baseTopicIds: [topics[index]],
          anchor: existingAnchorFor(paper, String(index + 1)),
          fallbackPage: paper.layout.aural[index],
        });
      }
    } else {
      addQuestion(paper, {
        n: 'R-A',
        label: 'Léamhthuiscint · Sliocht A',
        referenceSlots: ['R-A'],
        baseTopicIds: [ids.reading],
        fallbackPage: paper.layout.reading[0],
      });
      addQuestion(paper, {
        n: 'R-B',
        label: 'Léamhthuiscint · Sliocht B',
        referenceSlots: ['R-B'],
        baseTopicIds: [ids.reading],
        fallbackPage: paper.layout.reading[1],
      });
    }

    const writingSlots = modernWritingSlots(paper);
    const writingAnchor = sectionAnchor(paper, '4', paper.layout.writing, 'An Cheapadóireacht');
    const allWritingTopics = [...new Set(writingSlots.flatMap(([, topicIds]) => topicIds))];
    if (paper.year >= 2012) {
      ensureQuestion(paper, {
        n: '4',
        label: 'An Cheapadóireacht · all choices',
        baseTopicIds: allWritingTopics,
        anchor: writingAnchor,
        fallbackPage: paper.layout.writing,
      });
    }
    for (const [slot, topicIds] of writingSlots) {
      addQuestion(paper, {
        n: slot,
        label: 'An Cheapadóireacht · Rogha ' + slot.slice(-1),
        referenceSlots: [slot],
        baseTopicIds: topicIds,
        anchor: writingAnchor,
        fallbackPage: paper.layout.writing,
      });
    }
    continue;
  }

  if (paper.kind === 'p2') {
    const ids = levelIds(paper.level);
    const q1Anchor = sectionAnchor(paper, '1', paper.layout.reading?.[0] ?? paper.layout.prose, 'Léamhthuiscint');
    // Frozen P2 maps use 1–12 for reading subquestions, so their Q2/Q3/Q4
    // anchors are not the printed literature sections. Use the checked
    // section-page layout for additions to those papers; non-baseline maps
    // still retain their existing section anchors.
    const q2Anchor = paper.baseline
      ? anchorAt(paper.layout.prose, 'Prós')
      : sectionAnchor(paper, '2', paper.layout.prose, 'Prós');
    const q3Anchor = paper.baseline
      ? anchorAt(paper.layout.poetry, 'Filíocht')
      : sectionAnchor(paper, '3', paper.layout.poetry, 'Filíocht');
    const q4Anchor = paper.baseline
      ? anchorAt(paper.layout.extra ?? paper.layout.poetry, 'Litríocht Bhreise')
      : sectionAnchor(paper, '4', paper.layout.extra ?? paper.layout.poetry, 'Litríocht Bhreise');

    if (!paper.baseline && paper.sidecar) {
      const generic = paper.sidecar.q;
      for (const source of generic) {
        const n = String(source.n);
        let baseTopicIds;
        if (n === '1') baseTopicIds = [ids.reading];
        else if (n === '2') baseTopicIds = paper.level === 'higher' ? [H.prose] : [O.prose, O.folktale];
        else if (n === '3') baseTopicIds = paper.level === 'higher' ? [H.poetry] : [O.poetry];
        else baseTopicIds = [H.historic];
        ensureQuestion(paper, {
          n,
          label: source.label ?? ('Question ' + n),
          baseTopicIds,
          anchor: source,
          fallbackPage: source.pP ?? 1,
        });
      }
    }

    if (paper.year >= 2012 && !paper.baseline) {
      addQuestion(paper, {
        n: 'R-A',
        label: 'Léamhthuiscint · Sliocht A',
        referenceSlots: ['R-A'],
        baseTopicIds: [ids.reading],
        anchor: q1Anchor,
        fallbackPage: paper.layout.reading[0],
      });
      addQuestion(paper, {
        n: 'R-B',
        label: 'Léamhthuiscint · Sliocht B',
        referenceSlots: ['R-B'],
        baseTopicIds: [ids.reading],
        anchor: q1Anchor,
        fallbackPage: paper.layout.reading[1],
      });
      if (paper.level === 'higher') {
        addQuestion(paper, {
          n: 'G-A',
          label: 'Cruinneas Teanga · Sliocht A',
          referenceSlots: ['G-A'],
          baseTopicIds: [H.grammar],
          anchor: q1Anchor,
          fallbackPage: paper.layout.reading[0],
        });
        addQuestion(paper, {
          n: 'G-B',
          label: 'Cruinneas Teanga · Sliocht B',
          referenceSlots: ['G-B'],
          baseTopicIds: [H.grammar],
          anchor: q1Anchor,
          fallbackPage: paper.layout.reading[1],
        });
      }
    }

    addQuestion(paper, {
      n: 'P-A',
      label: 'Prós · Ábhar Ainmnithe',
      baseTopicIds: [ids.prose],
      anchor: q2Anchor,
      fallbackPage: paper.layout.prose,
    });
    addQuestion(paper, {
      n: 'P-B',
      label: 'Prós · Ábhar Roghnach',
      referenceSlots: ['P-B'],
      baseTopicIds: paper.level === 'higher' ? [H.prose] : [O.prose, O.folktale],
      anchor: q2Anchor,
      fallbackPage: paper.layout.proseOptional ?? paper.layout.prose,
    });
    addQuestion(paper, {
      n: 'F-A',
      label: 'Filíocht · Ábhar Ainmnithe',
      baseTopicIds: [ids.poetry],
      anchor: q3Anchor,
      fallbackPage: paper.layout.poetry,
    });
    addQuestion(paper, {
      n: 'F-B',
      label: 'Filíocht · Ábhar Roghnach',
      referenceSlots: ['F-B'],
      baseTopicIds: [ids.poetry],
      anchor: q3Anchor,
      fallbackPage: paper.layout.poetryOptional ?? paper.layout.poetry,
    });
    if (paper.level === 'higher') {
      addQuestion(paper, {
        n: 'X',
        label: 'Litríocht Bhreise · historic paper section',
        baseTopicIds: [H.historic],
        anchor: q4Anchor,
        fallbackPage: paper.layout.extra ?? paper.layout.poetry,
      });
    }
    continue;
  }

  if (paper.kind === 'foundation-aural') {
    if (!paper.baseline) throw new Error('Unexpected non-baseline Foundation aural: ' + paper.fileid);
    continue;
  }

  if (paper.kind === 'foundation') {
    const readingStart = paper.layout.readingStart;
    const writingStart = paper.layout.writingStart;
    if (paper.year >= 2012) {
      ensureQuestion(paper, {
        n: '1',
        label: 'Cluastuiscint',
        baseTopicIds: [F.aural],
        anchor: existingAnchorFor(paper, '1'),
        fallbackPage: paper.layout.listeningStart,
      });
    }
    if (paper.sidecar) {
      ensureQuestion(paper, {
        n: '2',
        label: paper.sidecar.q.find(question => String(question.n) === '2')?.label ?? 'Léamhthuiscint',
        baseTopicIds: [F.match, F.letterReading, F.brochure, F.news, F.extract, F.poem],
        anchor: existingAnchorFor(paper, '2'),
        fallbackPage: readingStart,
      });
      ensureQuestion(paper, {
        n: '3',
        label: paper.sidecar.q.find(question => String(question.n) === '3')?.label ?? 'Scríbhneoireacht',
        baseTopicIds: [F.form, F.letterWriting, F.notice, F.story, F.pictures],
        anchor: existingAnchorFor(paper, '3'),
        fallbackPage: writingStart,
      });
    }
    const readingSlots = [
      ['R-1', 'Léamhthuiscint · Meaitseáil pictiúir', [F.match], readingStart],
      ['R-2A', 'Léamhthuiscint · Litir', [F.letterReading], readingStart + 1],
      ['R-2B', 'Léamhthuiscint · Bróisiúr', [F.brochure], readingStart + 2],
      ['R-2C', 'Léamhthuiscint · Alt nuachta', [F.news], readingStart + 3],
      ['R-3A', 'Léamhthuiscint · Alt / Sliocht', [F.news, F.extract], readingStart + 4],
      ['R-3B', 'Léamhthuiscint · Sliocht', [F.extract], readingStart + 5],
      ['R-3C', 'Léamhthuiscint · Dán', [F.poem], readingStart + 6],
    ];
    for (const [n, label, baseTopicIds, page] of readingSlots) {
      addQuestion(paper, { n, label, referenceSlots: [n], baseTopicIds, fallbackPage: page });
    }
    const old = paper.year <= 2011;
    const writingSlots = old
      ? [
        ['W-4A', 'Scríobh · Fógra', [F.notice], writingStart],
        ['W-4B', 'Scríobh · Pictiúir', [F.pictures], writingStart + 1],
        ['W-5A', 'Scríobh · Litir', [F.letterWriting], writingStart + 2],
        ['W-5B', 'Scríobh · Foirm', [F.form], writingStart + 3],
        ['W-6A', 'Scríobh · Scéal', [F.story], writingStart + 4],
        ['W-6B', 'Scríobh · Scéal ó phictiúir', [F.story, F.pictures], writingStart + 5],
      ]
      : [
        ['W-4A', 'Scríobh · Fógra', [F.notice], writingStart],
        ['W-4B', 'Scríobh · Litir / Foirm', [F.letterWriting, F.form], writingStart + 1],
        ['W-5A', 'Scríobh · Scéal', [F.story], writingStart + 2],
        ['W-5B', 'Scríobh · Scéal ó phictiúir', [F.story, F.pictures], writingStart + 3],
      ];
    for (const [n, label, baseTopicIds, page] of writingSlots) {
      addQuestion(paper, { n, label, referenceSlots: [n], baseTopicIds, fallbackPage: page });
    }
  }
}

let preservedBaselineCards = 0;
for (const expected of preservationBaseline) {
  const paper = papers.find(candidate => candidate.year === expected.year && candidate.fileid === expected.fileid);
  if (!paper) throw new Error('Preservation failure: missing ' + expected.year + '|' + expected.fileid);
  if (paper.paperKey !== expected.paperKey) throw new Error('Preservation failure: changed paper key ' + expected.fileid);
  for (const expectedQuestion of expected.questions) {
    const actual = paper.q.find(question => question.n === expectedQuestion.n);
    if (!actual) throw new Error('Preservation failure: ' + expected.fileid + ' Q' + expectedQuestion.n);
    const compact = {
      n: actual.n,
      primary: actual.primary,
      ...(actual.secondary ? { secondary: actual.secondary } : {}),
    };
    if (JSON.stringify(compact) !== JSON.stringify(expectedQuestion)) {
      throw new Error('Preservation failure: changed ' + expected.fileid + ' Q' + expectedQuestion.n);
    }
    preservedBaselineCards += 1;
  }
}

const parseYear = heading => {
  const year = Number(heading.match(/^(\d{4})/)?.[1]);
  if (!year) throw new Error('Irish heading has no year: ' + heading);
  return year;
};
const readingPart = heading => {
  if (/Section 1 - Question B\b/i.test(heading)) return 'B';
  if (/Section 1(?: \(1\)| - Question 1)? - Part B\b/i.test(heading)) return 'B';
  if (/Question 2(?: - Part B)?$/i.test(heading)) return 'B';
  if (/Question 2 - Part b\b/i.test(heading)) return 'B';
  return 'A';
};
const writingLetter = heading => {
  const matches = [...heading.matchAll(/Question\s+(?:2)?([A-D])\b/gi)];
  if (matches.length) return matches.at(-1)[1].toUpperCase();
  const part = heading.match(/Part\s+([a-d])\b/i)?.[1];
  return part?.toUpperCase() ?? null;
};
const foundationSlot = (topic, heading) => {
  if (topic.id === F.match) return 'R-1';
  let match = heading.match(/Question\s+1\s+-\s+Part\s+([23])([abc])/i);
  if (match) return 'R-' + match[1] + match[2].toUpperCase();
  match = heading.match(/Question\s+2\s+-\s+Part\s+([45])([ab])/i);
  if (match) return 'W-' + match[1] + match[2].toUpperCase();
  match = heading.match(/Section\s+([23456])\s+-\s+Question\s+([abc])/i);
  if (match) return (Number(match[1]) <= 3 ? 'R-' : 'W-') + match[1] + match[2].toUpperCase();
  match = heading.match(/Question\s+([23456])\s+-\s+Part\s+([abc])/i);
  if (match) return (Number(match[1]) <= 3 ? 'R-' : 'W-') + match[1] + match[2].toUpperCase();
  const fallback = new Map([
    [F.brochure, 'R-2B'], [F.extract, 'R-3B'], [F.letterReading, 'R-2A'],
    [F.news, 'R-3A'], [F.poem, 'R-3C'], [F.form, 'W-5B'],
    [F.letterWriting, 'W-5A'], [F.notice, 'W-4A'], [F.story, 'W-5A'], [F.pictures, 'W-5B'],
  ]);
  return fallback.get(topic.id);
};
const referenceSlot = (topic, heading) => {
  if (topic.level === 'foundation') return foundationSlot(topic, heading);
  if (/aural-/i.test(topic.id) || /aurals-/i.test(topic.id)) {
    if (/Question A\b|Cuid A\b|Section A\b/i.test(heading)) return 'A1';
    if (/Question B\b|Cuid B\b|Section B\b/i.test(heading)) return 'A2';
    return 'A3';
  }
  if (topic.id === H.reading || topic.id === O.reading) return 'R-' + readingPart(heading);
  if (topic.id === H.grammar) return 'G-' + readingPart(heading);
  if (topic.id === H.prose || topic.id === O.prose || topic.id === O.folktale) return 'P-B';
  if (topic.id === H.poetry || topic.id === O.poetry) return 'F-B';
  if ([H.essay, H.story, H.article, H.debate, O.blog, O.story, O.letter, O.writtenConversation].includes(topic.id)) {
    const letter = writingLetter(heading);
    if (!letter) throw new Error('Cannot resolve Irish writing slot: ' + heading);
    return 'W-' + letter;
  }
  if (topic.id === H.oral || topic.id === O.oral) return 'ORAL';
  throw new Error('Unhandled Irish reference topic: ' + topic.id);
};
const topicKind = (topic, year) => {
  if (topic.level === 'foundation') return 'foundation';
  if (topic.id === H.oral || topic.id === O.oral) return 'oral';
  if (/aural-/i.test(topic.id) || /aurals-/i.test(topic.id)) return year <= 2011 ? 'aural' : 'p1';
  if ([H.essay, H.story, H.article, H.debate, O.blog, O.story, O.letter, O.writtenConversation].includes(topic.id)) return 'p1';
  if (topic.id === H.reading || topic.id === O.reading) return year === 2010 ? 'p1' : 'p2';
  return 'p2';
};
const blockedPaperKey = (topic, year) => {
  const kind = topicKind(topic, year);
  if (kind === 'oral') return 'oral';
  if (kind === 'aural') return 'aural';
  if (kind === 'p1') return 'p1';
  if (kind === 'p2') return 'p2';
  return year <= 2011 ? 'p1' : 'single';
};
const findPaper = (topic, year) => {
  const kind = topicKind(topic, year);
  const matches = papers.filter(paper => paper.year === year && paper.level === topic.level && paper.kind === kind);
  if (matches.length !== 1) {
    throw new Error(year + ' ' + topic.level + ' ' + kind + ': expected one Irish paper, found ' + matches.length);
  }
  return matches[0];
};
const resolveHeading = (topic, heading) => {
  const year = parseYear(heading);
  const sitting = /Deferred/i.test(heading) ? 'deferred' : /Sample/i.test(heading) ? 'sample' : 'main';
  const slot = referenceSlot(topic, heading);
  const blocked = (reason, reasonCode) => ({
    topicId: topic.id,
    heading,
    year,
    sitting,
    paperKey: blockedPaperKey(topic, year),
    referenceSlot: slot,
    resolution: 'source-blocked',
    reasonCode,
    reason,
  });
  if (year < 2010) {
    return blocked('The entitled local SEC corpus begins in 2010. The factual heading is retained, but no StudyClix-hosted question, solution, image or PDF is copied.', 'pre-corpus');
  }
  if (sitting === 'deferred') {
    return blocked('The factual deferred-paper heading is retained, but the corresponding entitled deferred booklet is not present in the local corpus.', 'deferred');
  }
  if (sitting === 'sample') {
    return blocked('The factual sample-paper heading is retained, but no entitled sample booklet is present in the local corpus.', 'sample');
  }
  if (topic.id === H.oral || topic.id === O.oral) {
    return blocked('The factual oral heading is retained, but Paper Trail does not hold an entitled oral picture-sequence booklet for this sitting.', 'oral-material');
  }
  const paper = findPaper(topic, year);
  let candidates = paper.q.filter(question => question.referenceSlots.includes(slot));
  if (!candidates.length && topic.level === 'foundation') {
    const alternatives = {
      'W-4B': ['W-5A', 'W-5B'],
      'W-5B': ['W-6B', 'W-6A'],
      'W-5A': ['W-6A', 'W-5A'],
    }[slot] ?? [];
    candidates = paper.q.filter(question => alternatives.includes(question.n));
  }
  if (!candidates.length) {
    throw new Error(topic.id + ': no local Irish card resolves ' + heading + ' (' + slot + ')');
  }
  return {
    topicId: topic.id,
    heading,
    year,
    sitting,
    paperKey: paper.paperKey,
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
if (associations.length !== 842) {
  throw new Error('Irish reference boundary mismatch: ' + associations.length + ' associations');
}
const matched = associations.filter(association => association.resolution === 'matched');
const sourceBlocked = associations.filter(association => association.resolution === 'source-blocked');
const referenceTopicsByLocalQuestion = new Map();
for (const association of matched) {
  for (const number of association.target.questionNumbers) {
    const key = [association.target.level, association.year, association.target.fileid, number].join('|');
    const ids = referenceTopicsByLocalQuestion.get(key) ?? [];
    if (!ids.includes(association.topicId)) ids.push(association.topicId);
    referenceTopicsByLocalQuestion.set(key, ids);
  }
}

const localQuestionMappings = papers.flatMap(paper => paper.q.map(question => {
  const key = [paper.level, paper.year, paper.fileid, question.n].join('|');
  const referenced = referenceTopicsByLocalQuestion.get(key) ?? [];
  const topicIds = [...new Set([...referenced, ...question.baseTopicIds])]
    .sort((a, b) => topicIndex.get(a) - topicIndex.get(b));
  if (!topicIds.length || topicIds.some(id => !topicById.has(id))) {
    throw new Error(paper.fileid + ' Q' + question.n + ': invalid Irish topic mapping');
  }
  if (topicIds.some(id => topicById.get(id).level !== paper.level)) {
    throw new Error(paper.fileid + ' Q' + question.n + ': cross-level Irish topic mapping');
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
      ? question.baseTopicIds.some(id => !referenced.includes(id))
        ? 'reference+retained-local'
        : 'reference'
      : 'retained-local',
  };
}));

const mappingIdentities = localQuestionMappings.map(mapping => [
  mapping.level, mapping.lang, mapping.year, mapping.fileid, mapping.n,
].join('|'));
if (new Set(mappingIdentities).size !== mappingIdentities.length) {
  throw new Error('Duplicate Irish local question mapping');
}

const tagPapers = papers
  .sort((a, b) => b.year - a.year || a.level.localeCompare(b.level) || a.fileid.localeCompare(b.fileid))
  .map(paper => ({
    subjectId: 'irish',
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
fs.writeFileSync(TAGS_PATH, JSON.stringify(tagPapers, null, 2) + '\n');

const hostedAnchorMaps = [];
for (const paper of papers) {
  const physicalOrder = [...paper.q].sort((a, b) => (
    a.anchor.pP - b.anchor.pP
    || a.anchor.pY[0] - b.anchor.pY[0]
    || paper.q.indexOf(a) - paper.q.indexOf(b)
  ));
  const printOrder = new Map(physicalOrder.map((question, index) => [question, index + 1]));
  const anchorCounts = new Map();
  for (const question of paper.q) {
    const key = question.anchor.pP + '|' + question.anchor.pY[0];
    anchorCounts.set(key, (anchorCounts.get(key) ?? 0) + 1);
  }
  const artifact = {
    v: 1,
    paperFileid: paper.fileid,
    schemeFileid: '',
    component: paper.component,
    band: [1, 1],
    copyright: '© State Examinations Commission',
    paperOnly: 1,
    q: paper.q.map(question => {
      const collision = anchorCounts.get(question.anchor.pP + '|' + question.anchor.pY[0]) > 1;
      return {
        n: question.n,
        label: question.label,
        printOrder: printOrder.get(question),
        pP: question.anchor.pP,
        pY: question.anchor.pY,
        ...(question.anchor.paperRegion
          ? { paperRegion: question.anchor.paperRegion }
          : collision
            ? { paperRegion: fullPages(question.anchor.pP) }
            : {}),
        ...(question.anchor.endP !== undefined ? { endP: question.anchor.endP } : {}),
        ...(question.anchor.endY !== undefined ? { endY: question.anchor.endY } : {}),
        region: [{ p: 1 }],
        mode: 'pagejump',
        conf: 0.5,
      };
    }),
  };
  const yearDir = path.join(HOSTED_ROOT, String(paper.year));
  fs.mkdirSync(yearDir, { recursive: true });
  const outputPath = path.join(yearDir, paper.fileid + '.json');
  fs.writeFileSync(outputPath, JSON.stringify(artifact) + '\n');
  hostedAnchorMaps.push(path.relative(ROOT, outputPath));
}

const blockedByReason = sourceBlocked.reduce((counts, association) => {
  counts[association.reasonCode] = (counts[association.reasonCode] ?? 0) + 1;
  return counts;
}, {});
const logicalQuestions = new Set(localQuestionMappings.map(mapping => [
  mapping.level, mapping.year, mapping.paperKey, mapping.n,
].join('|')));
const summary = {
  referenceTopics: referenceTopics.length,
  preservationExtensionTopics: EXTENSIONS.length,
  runtimeTopics: allTopics.length,
  referenceReportedAssociations: referenceTopics.reduce((sum, topic) => sum + topic.reportedQuestionCount, 0),
  referenceOfficialAssociations: associations.length,
  referenceMockAssociations: referenceTopics.reduce((sum, topic) => sum + topic.mockQuestionCount, 0),
  referenceProviderSampleAssociations: referenceTopics.reduce((sum, topic) => sum + topic.providerSampleQuestionCount, 0),
  matchedAssociations: matched.length,
  sourceBlockedAssociations: sourceBlocked.length,
  sourceBlockedByReason: blockedByReason,
  matchedLocalCardLinks: matched.reduce((sum, association) => sum + association.target.questionNumbers.length, 0),
  localPaperVariants: papers.length,
  localPhysicalMappings: localQuestionMappings.length,
  distinctStudentFacingQuestions: logicalQuestions.size,
  referenceMappedLocalQuestions: localQuestionMappings.filter(mapping => mapping.provenance.startsWith('reference')).length,
  retainedLocalQuestions: localQuestionMappings.filter(mapping => !mapping.provenance.startsWith('reference')).length,
  hostedPaperAnchorMaps: hostedAnchorMaps.length,
  preservedBaselineVariants: preservationBaseline.length,
  preservedBaselineCards,
  newlyAddedPaperVariants: papers.length - preservationBaseline.length,
  newlyAddedPhysicalMappings: localQuestionMappings.length - preservedBaselineCards,
  emptyOfficialReferenceTopics: referenceTopics
    .filter(topic => topic.officialQuestionHeadings.length === 0)
    .map(topic => topic.id),
};
const output = {
  schemaVersion: 1,
  subjectId: 'irish',
  capturedAt: reference.capturedAt,
  policy: {
    matchedSource: 'Entitled local State Examinations Commission corpus only.',
    excludedContent: 'No commercial mock question, solution, note, question text, StudyClix image or StudyClix-hosted PDF is copied.',
    restoredCards: 'Missing listening, composition, literature and Foundation choices use section/page boundaries checked in the official SEC booklets.',
    preservationExtensions: 'Two explicitly labelled local archive topics retain Higher additional literature and Foundation listening omitted by the reference menu.',
    referenceOmissions: 'Valid local tasks omitted or mis-grouped by the reference retain truthful Irish curriculum tags and retained-local provenance.',
  },
  summary,
  extensions: EXTENSIONS,
  associations,
  localQuestionMappings,
  hostedAnchorMaps,
};
fs.writeFileSync(OUTPUT_PATH, JSON.stringify(output, null, 2) + '\n');
fs.writeFileSync(CURRICULUM_PATH, JSON.stringify(CURRICULUM_CROSSWALK, null, 2) + '\n');

const levelCode = level => ({ higher: 'h', ordinary: 'o', foundation: 'f' })[level];
const paperKeyCode = paperKey => ({ single: 's', p1: '1', p2: '2', aural: 'a', oral: 'o' })[paperKey];
const sittingCode = sitting => ({ main: 'm', deferred: 'd', sample: 'x' })[sitting];
const runtimePartReferences = associations.flatMap(association => {
  const index = topicIndex.get(association.topicId);
  if (association.resolution === 'matched') {
    return association.target.questionNumbers.map(number => [
      index,
      association.year - 2000,
      levelCode(association.target.level),
      paperKeyCode(association.target.paperKey),
      sittingCode(association.sitting),
      number,
      association.heading,
    ]);
  }
  return [[
    index,
    association.year - 2000,
    levelCode(topicById.get(association.topicId).level),
    paperKeyCode(association.paperKey),
    sittingCode(association.sitting),
    association.referenceSlot,
    association.heading,
  ]];
});
const runtimeGroups = Object.entries(reference.variants).map(([level, variant]) => {
  const ids = variant.topics.map(topic => topic.id);
  for (const extension of EXTENSIONS.filter(topic => topic.level === level)) ids.push(extension.id);
  return [levelCode(level), 'irish-' + level, variant.label, ids.map(id => topicIndex.get(id))];
});
const runtime = {
  v: 1,
  subjectId: 'irish',
  capturedAt: reference.capturedAt,
  referenceProvider: reference.reference.provider,
  groups: runtimeGroups,
  topics: allTopics.map(topic => [
    topic.id,
    topic.label,
    topic.sourcePath,
    topic.mockQuestionCount,
    topic.providerSampleQuestionCount,
    CURRICULUM_CROSSWALK[topic.id],
    levelCode(topic.level),
    topic.reportedQuestionCount,
    topic.referenceTopic ? 1 : 0,
  ]),
  partReferences: runtimePartReferences,
  questionMappings: localQuestionMappings.map(mapping => [
    levelCode(mapping.level),
    'i',
    mapping.year - 2000,
    paperKeyCode(mapping.paperKey),
    mapping.n,
    mapping.topicIds.map(id => topicIndex.get(id)),
  ]),
};
fs.writeFileSync(RUNTIME_PATH, JSON.stringify(runtime) + '\n');

console.log(JSON.stringify({
  output: path.relative(ROOT, OUTPUT_PATH),
  runtime: path.relative(ROOT, RUNTIME_PATH),
  curriculum: path.relative(ROOT, CURRICULUM_PATH),
  tags: path.relative(ROOT, TAGS_PATH),
  ...summary,
}, null, 2));
