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

// Reviewed reference anomalies. The reference files these questions under a
// heading that the SEC paper's own printed dates or works contradict; each was
// decided 2026-10-12 from the paper (StudyClix is a cross-check, never the
// authority). The association is kept as an audited anomaly and the question
// is filed under the heading the paper supports, which is also the heading of
// its Mark Bank card.
const REVIEWED_REFERENCE_ANOMALIES = [
  {
    level: 'higher', year: 2021, n: '3',
    referenceTopicId: 'art-higher-pre-christian-ireland-c-4000bc-ad500',
    topicId: 'art-higher-insular-art-c-500-1100s',
    evidence: 'Q3 is "The Tara Brooch displays the artistry and technical brilliance of 8th century Irish metalwork": 8th-century Early Christian metalwork is Insular Art (c. 500-1100s), not Pre-Christian Ireland (c. 4000BC-AD500).',
  },
  {
    level: 'higher', year: 2021, n: '6',
    referenceTopicId: 'art-higher-irish-art-and-modernism',
    topicId: 'art-higher-post-1960s-art-in-ireland',
    evidence: "Q6 is 'Portrait of Henry Shefflin (b.1979), Hurler', illustrated on the accompanying sheet: a portrait of a sitter born in 1979 is Post-1960s Art in Ireland, not Irish Art and Modernism (c. 1880-1960s).",
  },
  {
    level: 'ordinary', year: 2021, n: '6',
    referenceTopicId: 'art-ordinary-irish-art-and-modernism',
    topicId: 'art-ordinary-post-1960s-art-in-ireland',
    evidence: "Q6 is 'The Hare Queen' by Fidelma Massey (b.1956), illustrated on the accompanying sheet: the work of an artist born in 1956 is Post 1960s Art in Ireland, not Irish Art and Modernism (c. 1880-1960s).",
  },
  {
    level: 'higher', year: 2022, n: '6',
    referenceTopicId: 'art-higher-irish-art-and-modernism',
    topicId: 'art-higher-post-1960s-art-in-ireland',
    evidence: "Q6 is \"Public sculpture should be created in response to the place in which it is situated\", with reference to 'Harmony' by Sandra Bell, illustrated on the accompanying sheet: a contemporary public sculpture is Post-1960s Art in Ireland, not Irish Art and Modernism (c. 1880-1960s).",
  },
  {
    level: 'ordinary', year: 2022, n: '6',
    referenceTopicId: 'art-ordinary-irish-art-and-modernism',
    topicId: 'art-ordinary-post-1960s-art-in-ireland',
    evidence: "Q6 is 'The Family', a sculpture by Maurice Harron (b.1946), illustrated on the accompanying sheet: the work of an artist born in 1946 is Post 1960s Art in Ireland, not Irish Art and Modernism (c. 1880-1960s).",
  },
  {
    level: 'higher', year: 2022, n: '13',
    referenceTopicId: 'art-higher-modernism-c-1900-1960s',
    topicId: 'art-higher-realism-impressionism-and-post-impressionism',
    evidence: 'Q13 is "Vincent van Gogh (1853-1890) attempted to convey intense emotion using strong colour and bold brushwork": a painter who died in 1890 is Post-Impressionism (c. 1850-1900s), not Modernism (c. 1900-1960s).',
  },
  {
    level: 'ordinary', year: 2022, n: '8',
    referenceTopicId: 'art-ordinary-europe-the-renaissance-c-1300-1600s',
    topicId: 'art-ordinary-europe-romanesque-and-gothic',
    evidence: "Q8 is the 'Last Judgement' by Gislebertus (12th century), illustrated on the accompanying sheet: a 12th-century tympanum is Romanesque and Gothic, not The Renaissance (c. 1300-1600s).",
  },
  {
    level: 'higher', year: 2020, n: '6',
    referenceTopicId: 'art-higher-irish-art-and-modernism',
    topicId: 'art-higher-post-1960s-art-in-ireland',
    evidence: "Q6 is 'Fionn Mac Cumhaill and his Hounds' by Lynn Kirkham, illustrated on the accompanying sheet: a contemporary public sculpture is Post-1960s Art in Ireland, not Irish Art and Modernism (c. 1880-1960s).",
  },
  {
    level: 'ordinary', year: 2020, n: '6',
    referenceTopicId: 'art-ordinary-irish-art-and-modernism',
    topicId: 'art-ordinary-post-1960s-art-in-ireland',
    evidence: "Q6 is the sculpture 'W. B. Yeats' by Rowan Gillespie (b.1953), illustrated on the accompanying sheet: the work of an artist born in 1953 is Post 1960s Art in Ireland, not Irish Art and Modernism (c. 1880-1960s).",
  },
  {
    level: 'ordinary', year: 2020, n: '11',
    referenceTopicId: 'art-ordinary-europe-the-renaissance-c-1300-1600s',
    topicId: 'art-ordinary-section-b-generic-questions',
    evidence: "Q11 is the 'Oath of the Horatii' by Jacques-Louis David (1748-1825), \"an example of Neoclassical painting\": Neoclassicism is neither The Renaissance (c. 1300-1600s) nor The Baroque (c. 1600-1700s) and has no heading of its own, so it files under Section B: Generic Questions.",
  },
  {
    level: 'ordinary', year: 2020, n: '11',
    referenceTopicId: 'art-ordinary-the-baroque-c-1600-1700s',
    topicId: 'art-ordinary-section-b-generic-questions',
    evidence: "Q11 is the 'Oath of the Horatii' by Jacques-Louis David (1748-1825), \"an example of Neoclassical painting\": Neoclassicism is neither The Renaissance (c. 1300-1600s) nor The Baroque (c. 1600-1700s) and has no heading of its own, so it files under Section B: Generic Questions.",
  },
  {
    level: 'ordinary', year: 2020, n: '12',
    referenceTopicId: 'art-ordinary-europe-modernism-c-1900-1960s',
    topicId: 'art-ordinary-europe-realism-impressionism-and-post-impressionism',
    evidence: "Q12 is \"'The Starry Night' by Vincent van Gogh (1853-1890) is an example of Post-Impressionist painting\": the paper itself names it Post-Impressionism (c. 1850-1900s), not Modernism (c. 1900-1960s).",
  },
  {
    level: 'higher', year: 2019, n: '11',
    referenceTopicId: 'art-higher-realism-impressionism-and-post-impressionism',
    topicId: 'art-higher-section-b-generic-questions',
    evidence: "Q11 is \"J.M.W. Turner (1775-1851) painted expressive and dramatic scenes\", with 'Rain, Steam and Speed - The Great Western Railway': Turner's Romanticism precedes Realism, Impressionism and Post-Impressionism (c. 1850-1900s) and has no heading of its own, as for Turner's option in 2022 HL Q14.",
  },
  {
    level: 'higher', year: 2019, n: '13',
    referenceTopicId: 'art-higher-realism-impressionism-and-post-impressionism',
    topicId: 'art-higher-modernism-c-1900-1960s',
    evidence: "Q13 is \"Henri Matisse (1869-1954) used stylised shapes, strong colours and patterns in his paintings\", with 'Odalisque Wearing Red Trousers': Matisse's work is Modernism (c. 1900-1960s), not Post-Impressionism.",
  },
  {
    level: 'ordinary', year: 2019, n: '5',
    referenceTopicId: 'art-ordinary-europe-realism-impressionism-and-post-impressionism',
    topicId: 'art-ordinary-irish-art-and-modernism',
    evidence: "Q5 is in Section 1 (Art in Ireland): 'A Convent Garden, Brittany' by William Leech (1881-1968), an Irish painter, is Irish Art and Modernism, not the European heading.",
  },
  {
    level: 'ordinary', year: 2019, n: '6',
    referenceTopicId: 'art-ordinary-irish-art-and-modernism',
    topicId: 'art-ordinary-post-1960s-art-in-ireland',
    evidence: "Q6 is the sculpture 'Misneach' by John Byrne (b.1959), illustrated on the accompanying sheet: the work of an artist born in 1959 is Post 1960s Art in Ireland, not Irish Art and Modernism (c. 1880-1960s).",
  },
  {
    level: 'ordinary', year: 2019, n: '11',
    referenceTopicId: 'art-ordinary-europe-the-renaissance-c-1300-1600s',
    topicId: 'art-ordinary-the-baroque-c-1600-1700s',
    evidence: "Q11 is 'The Supper at Emmaus' by Caravaggio (1571-1610), with \"(b) Briefly describe and discuss the Baroque style\": the paper itself places it in the Baroque (c. 1600-1700s), not The Renaissance.",
  },
  {
    level: 'higher', year: 2018, n: '10',
    referenceTopicId: 'art-higher-the-baroque-c-1600-1700s',
    topicId: 'art-higher-the-renaissance-c-1300-1600s',
    evidence: "Q10 is the altarpiece 'Assumption of the Virgin' by Titian (c.1488-1576), illustrated on the accompanying sheet: Titian is The Renaissance (c. 1300-1600s), not The Baroque (c. 1600-1700s).",
  },
  {
    level: 'ordinary', year: 2018, n: '6',
    referenceTopicId: 'art-ordinary-section-a-todays-world',
    topicId: 'art-ordinary-post-1960s-art-in-ireland',
    evidence: "Q6 is in Section 1 (Art in Ireland): the 'Dockers Monument' by Mike Duhan (b.1956), illustrated on the accompanying sheet, is Post 1960s Art in Ireland, not a Today's World question.",
  },
  {
    level: 'ordinary', year: 2018, n: '11',
    referenceTopicId: 'art-ordinary-europe-the-renaissance-c-1300-1600s',
    topicId: 'art-ordinary-the-baroque-c-1600-1700s',
    evidence: "Q11 is \"Choose one work by Caravaggio (1571-1610)\" with \"(b) Briefly describe and discuss Caravaggio's use of light\": Caravaggio is The Baroque (c. 1600-1700s), not The Renaissance.",
  },
  {
    level: 'ordinary', year: 2017, n: '6',
    referenceTopicId: 'art-ordinary-irish-art-and-modernism',
    topicId: 'art-ordinary-post-1960s-art-in-ireland',
    evidence: "Q6 is 'Coffin Ship' by John Behan (b. 1938), illustrated on the accompanying sheet: the National Famine Memorial sculpture (1997) is Post 1960s Art in Ireland, not Irish Art and Modernism (c. 1880-1960s).",
  },
  {
    level: 'ordinary', year: 2017, n: '11',
    referenceTopicId: 'art-ordinary-europe-the-renaissance-c-1300-1600s',
    topicId: 'art-ordinary-the-baroque-c-1600-1700s',
    evidence: "Q11 is 'The Ecstasy of Saint Teresa' by Gian Lorenzo Bernini (1598-1680), with \"(b) Briefly describe and discuss the Baroque style\": the paper itself places it in the Baroque (c. 1600-1700s), not The Renaissance.",
  },
  {
    level: 'higher', year: 2016, n: '6',
    referenceTopicId: 'art-higher-irish-art-and-modernism',
    topicId: 'art-higher-post-1960s-art-in-ireland',
    evidence: "Q6 is \"Alice Maher (b.1956) creates artworks in a wide variety of media\", with 'Berry Dress': the work of an artist born in 1956 is Post-1960s Art in Ireland, not Irish Art and Modernism (c. 1880-1960s).",
  },
  {
    level: 'ordinary', year: 2016, n: '6',
    referenceTopicId: 'art-ordinary-irish-art-and-modernism',
    topicId: 'art-ordinary-post-1960s-art-in-ireland',
    evidence: "Q6 is \"Robert Ballagh (b.1943) is one of Ireland's best known contemporary artists\": the paper itself calls him contemporary, so Post 1960s Art in Ireland, not Irish Art and Modernism (c. 1880-1960s).",
  },
  {
    level: 'ordinary', year: 2016, n: '11',
    referenceTopicId: 'art-ordinary-europe-the-renaissance-c-1300-1600s',
    topicId: 'art-ordinary-the-baroque-c-1600-1700s',
    evidence: "Q11 is 'Supper at Emmaus' by Caravaggio (1571 - 1610), illustrated on the accompanying sheet: Caravaggio is The Baroque (c. 1600-1700s), not The Renaissance, as the paper itself says in 2017 and 2019.",
  },
  {
    level: 'ordinary', year: 2016, n: '12',
    referenceTopicId: 'art-ordinary-irish-art-and-modernism',
    topicId: 'art-ordinary-europe-realism-impressionism-and-post-impressionism',
    evidence: "Q12 is in Section 2 (European Art): \"Choose one work that you have studied by Claude Monet (1840 - 1926)\" is Impressionism, not Irish Art and Modernism.",
  },
  {
    level: 'ordinary', year: 2016, n: '13',
    referenceTopicId: 'art-ordinary-europe-realism-impressionism-and-post-impressionism',
    topicId: 'art-ordinary-europe-modernism-c-1900-1960s',
    evidence: "Q13 is 'The Red Room (Harmony in Red)' by Henri Matisse (1869 - 1954), illustrated on the accompanying sheet: Matisse's work is Modernism (c. 1900-1960s), not Post-Impressionism.",
  },
  {
    level: 'higher', year: 2015, n: '3',
    referenceTopicId: 'art-higher-irish-art-and-modernism',
    topicId: 'art-higher-late-medieval-architecture-and-art-c1100-1550s',
    evidence: "Q3 is \"The simple design of stone churches in Early Christian Ireland developed into a more complex Irish Romanesque style\": Irish Romanesque church building (12th century) is Late Medieval Architecture and Art (c. 1100-1550s), not Irish Art and Modernism.",
  },
  {
    level: 'higher', year: 2015, n: '6',
    referenceTopicId: 'art-higher-irish-art-and-modernism',
    topicId: 'art-higher-post-1960s-art-in-ireland',
    evidence: "Q6 is \"Rowan Gillespie (b.1953) creates sculptures ...\", with 'Famine' illustrated on the accompanying sheet: the work of an artist born in 1953 is Post-1960s Art in Ireland, not Irish Art and Modernism (c. 1880-1960s).",
  },
  {
    level: 'higher', year: 2015, n: '7',
    referenceTopicId: 'art-higher-section-b-generic-questions',
    topicId: 'art-higher-irish-art-and-modernism',
    evidence: 'Q7 is in Section I (Art in Ireland), a choice of Irish artists from John Hogan (1800-1858) to Caroline McCarthy (b.1971): it is not a European (Section B) question, and like every other year\'s Q7 list it files under Irish Art and Modernism.',
  },
  {
    level: 'ordinary', year: 2015, n: '3',
    referenceTopicId: 'art-ordinary-pre-christian-ireland-c-4000bc-ad500',
    topicId: 'art-ordinary-insular-art-c-500-1100s',
    evidence: "Q3 is the 'Cross of the Scriptures' at Clonmacnoise, Co. Offaly, illustrated on the accompanying sheet: an Early Christian high cross is Insular Art (c. 500-1100s), not Pre-Christian Ireland.",
  },
  {
    level: 'ordinary', year: 2015, n: '11',
    referenceTopicId: 'art-ordinary-europe-realism-impressionism-and-post-impressionism',
    topicId: 'art-ordinary-the-baroque-c-1600-1700s',
    evidence: "Q11 is the 'Return of the Prodigal Son' by Rembrandt van Rijn (1606-1669), illustrated on the accompanying sheet: Rembrandt is The Baroque (c. 1600-1700s), not Realism, Impressionism and Post-Impressionism.",
  },
  {
    level: 'higher', year: 2014, n: '12',
    referenceTopicId: 'art-higher-modernism-c-1900-1960s',
    topicId: 'art-higher-realism-impressionism-and-post-impressionism',
    evidence: "Q12 is about \"the Realist painter Gustave Courbet (1819-1877)\" and 'Bonjour, Monsieur Courbet': the paper itself names him a Realist, so Realism, Impressionism and Post-Impressionism, not Modernism (c. 1900-1960s).",
  },
  {
    level: 'ordinary', year: 2014, n: '2',
    referenceTopicId: 'art-ordinary-pre-christian-ireland-c-4000bc-ad500',
    topicId: 'art-ordinary-insular-art-c-500-1100s',
    evidence: "Q2 is \"The 'Reask Pillar', Co. Kerry ... an example of an Early Christian stone slab / pillar\": the paper itself calls it Early Christian, so Insular Art (c. 500-1100s), not Pre-Christian Ireland.",
  },
  {
    level: 'ordinary', year: 2014, n: '3',
    referenceTopicId: 'art-ordinary-pre-christian-ireland-c-4000bc-ad500',
    topicId: 'art-ordinary-insular-art-c-500-1100s',
    evidence: "Q3 is \"The 'Tara Brooch' is an example of Irish metalwork from the Early Medieval period\": Early Medieval (8th-century) metalwork is Insular Art (c. 500-1100s), not Pre-Christian Ireland.",
  },
  {
    level: 'ordinary', year: 2014, n: '9',
    referenceTopicId: 'art-ordinary-europe-realism-impressionism-and-post-impressionism',
    topicId: 'art-ordinary-europe-the-renaissance-c-1300-1600s',
    evidence: "Q9 is 'Holy Trinity' by Masaccio (1401-c.1428), illustrated on the accompanying sheet: Masaccio is The Renaissance (c. 1300-1600s), not Realism, Impressionism and Post-Impressionism.",
  },
  {
    level: 'higher', year: 2013, n: '17',
    referenceTopicId: 'art-higher-art-as-social-commentary-or-commentator',
    topicId: 'art-higher-artists-theory-and-thinking',
    evidence: "Q17 is \"A curator's work involves planning all aspects of an exhibition\": (a) the main steps a curator took in planning and mounting a named exhibition and (b) curating an exhibition of Transition Year artwork. It comments on no social issue; it is a curating and exhibition question, filed with the gallery questions under Artists: Theory and Thinking (as 2024 HL Q5(a) \"the role of the curator\"), not Art as Social Commentary or Commentator.",
  },
  {
    level: 'ordinary', year: 2011, n: '14',
    referenceTopicId: 'art-ordinary-europe-realism-impressionism-and-post-impressionism',
    topicId: 'art-ordinary-europe-modernism-c-1900-1960s',
    evidence: "Q14 is \"Choose any work that you have studied by Henri Matisse (1869-1954)\": Matisse's work is Modernism (c. 1900-1960s), as for 2019 HL Q13, not Post-Impressionism.",
  },
];
const anomalyFor = (level, year, n, topicId) => REVIEWED_REFERENCE_ANOMALIES.find(item => (
  item.level === level && item.year === year && item.n === n && item.referenceTopicId === topicId
));
for (const item of REVIEWED_REFERENCE_ANOMALIES) {
  for (const id of [item.referenceTopicId, item.topicId]) {
    if (topicLevel.get(id) !== item.level) throw new Error(`Art anomaly ${item.year} Q${item.n}: ${id} is not ${item.level}`);
  }
}

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
      const anomaly = parsed.sitting === 'main'
        ? anomalyFor(level, parsed.year, parsed.questionNumber, topic.id)
        : undefined;
      if (anomaly) {
        anomaly.seen = (anomaly.seen ?? 0) + 1;
        associations.push({
          topicId: topic.id,
          level,
          heading,
          ...parsed,
          resolution: 'reference-anomaly',
          target: {
            level,
            lang: 'ev',
            year: parsed.year,
            paperKey: 'single',
            fileid: paper.fileid,
            questionNumber: parsed.questionNumber,
          },
          filedUnder: anomaly.topicId,
          reason: `StudyClix files this ${parsed.year} ${level} heading under ${topic.id}. Decided 2026-10-12 from the SEC paper: ${anomaly.evidence} NextStepUni files the question under ${anomaly.topicId}, the heading of its Mark Bank card; the reference association is retained here as an audited anomaly.`,
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
const unusedAnomalies = REVIEWED_REFERENCE_ANOMALIES.filter(item => item.seen !== 1);
if (unusedAnomalies.length) {
  throw new Error(`Art reviewed anomalies must each match one association: ${unusedAnomalies.map(item => `${item.year} ${item.level} Q${item.n}`).join(', ')}`);
}
const reviewedTopicsByCard = new Map();
for (const item of REVIEWED_REFERENCE_ANOMALIES) {
  const paper = EnglishWrittenPaper(item.level, item.year);
  const key = [item.level, item.year, paper.fileid, item.n].join('|');
  const indexes = reviewedTopicsByCard.get(key) ?? [];
  const index = topicIndex.get(item.topicId);
  if (!indexes.includes(index)) indexes.push(index);
  reviewedTopicsByCard.set(key, indexes);
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

// A choose-one list whose printed options are different syllabus periods or
// movements is carded one card per option (Mark Bank OPTION_TOPICS). The
// question-level reference heading is generic, so each option's own heading
// is added to the question's browse topics, with a reviewed part reference
// naming the printed option, so the card appears under its own heading.
const optionTopicsByCard = new Map();
const reviewedOptionTopics = [];
for (const card of authored.cards) {
  const [base, option] = card.questionRef.split(' · ');
  if (!option || /^task \d$/.test(option)) continue;
  const n = base.match(/\bQ(\d+)/)?.[1];
  const paper = EnglishWrittenPaper(card.level, card.year);
  if (!n || !paper) throw new Error(`Cannot place Art option card ${card.id}`);
  const index = fallbackTopicForNode(card.level, card.topicId);
  const key = [card.level, card.year, paper.fileid, n].join('|');
  const indexes = optionTopicsByCard.get(key) ?? [];
  if (!indexes.includes(index)) indexes.push(index);
  optionTopicsByCard.set(key, indexes);
  if (!reviewedOptionTopics.some(item => item.key === `${key}|${option}`)) {
    reviewedOptionTopics.push({
      key: `${key}|${option}`,
      level: card.level,
      year: card.year,
      fileid: paper.fileid,
      questionNumber: n,
      option,
      canonicalNodeId: card.topicId,
      topicId: allTopics[index].id,
      heading: `${card.year} - Question ${n} - ${option}`,
    });
  }
}

// Where the reference gives a question only a generic bucket ("Section A:
// Generic Questions", "Section B: Generic Questions"), its reviewed Mark Bank
// card names the specific heading; the question is added under that heading
// too, so the card and the Atlas agree.
const GENERIC_TOPIC_INDEXES = new Set([
  'art-higher-section-a-generic-questions',
  'art-higher-section-b-generic-questions',
  'art-ordinary-section-b-generic-questions',
].map(id => topicIndex.get(id)));
const cardTopicsByQuestion = new Map();
for (const card of authored.cards) {
  const n = card.questionRef.split(' · ')[0].match(/\bQ(\d+)/)?.[1];
  const paper = EnglishWrittenPaper(card.level, card.year);
  if (!n || !paper) continue;
  const key = [card.level, card.year, paper.fileid, n].join('|');
  const indexes = cardTopicsByQuestion.get(key) ?? [];
  const index = fallbackTopicForNode(card.level, card.topicId);
  if (!indexes.includes(index)) indexes.push(index);
  cardTopicsByQuestion.set(key, indexes);
}
const reviewedSpecificTopics = [];

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
    const reviewedIndexes = reviewedTopicsByCard.get(exactKey);
    const exactIndexes = exactTopicsByCard.get(exactKey);
    let indexes = reviewedIndexes || exactIndexes
      ? [...new Set([...(exactIndexes ?? []), ...(reviewedIndexes ?? [])])]
      : undefined;
    if (!indexes) {
      indexes = [...new Set(
        [question.primary, question.secondary]
          .filter(Boolean)
          .map(nodeId => fallbackTopicForNode(paper.level, nodeId)),
      )];
      // With no reference association, the local tags and the reviewed Mark
      // Bank card are the evidence: the card's heading is always included.
      const cardAdded = (WRITTEN_COMPONENTS.has(componentCode(paper.fileid))
        ? cardTopicsByQuestion.get(exactKey) ?? []
        : []).filter(index => !indexes.includes(index));
      indexes = [...indexes, ...cardAdded];
      if (paper.lang === 'ev' && cardAdded.length) {
        reviewedSpecificTopics.push({
          level: paper.level,
          year: paper.year,
          fileid: paper.fileid,
          questionNumber: question.n,
          topicIds: cardAdded.map(index => allTopics[index].id),
          basis: 'retained-local',
        });
      }
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
    const optionIndexes = WRITTEN_COMPONENTS.has(componentCode(paper.fileid))
      ? optionTopicsByCard.get(exactKey) ?? []
      : [];
    indexes = [...new Set([...indexes, ...optionIndexes])];
    const cardIndexes = WRITTEN_COMPONENTS.has(componentCode(paper.fileid))
      ? cardTopicsByQuestion.get(exactKey) ?? []
      : [];
    if (cardIndexes.length && indexes.every(index => GENERIC_TOPIC_INDEXES.has(index))) {
      const added = cardIndexes.filter(index => !indexes.includes(index));
      indexes = [...indexes, ...added];
      if (paper.lang === 'ev' && added.length) {
        reviewedSpecificTopics.push({
          level: paper.level,
          year: paper.year,
          fileid: paper.fileid,
          questionNumber: question.n,
          topicIds: added.map(index => allTopics[index].id),
        });
      }
    }
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
const referenceAnomalyAssociations = associations.filter(item => item.resolution === 'reference-anomaly');
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
const reviewedOnlyCards = [...reviewedTopicsByCard.keys()].filter(key => !exactTopicsByCard.has(key));
if (
  exactTopicsByCard.size + reviewedOnlyCards.length + retainedLocalCards.length
  !== distinctStudentFacingQuestions
) {
  throw new Error('Every logical Art card must be exactly matched, reviewed, or explicitly retained');
}
if (
  matchedAssociations.length !== 554
  || sourceBlockedAssociations.length !== 98
  || referenceAnomalyAssociations.length !== 38
  || exactTopicsByCard.size !== 506
  || reviewedTopicsByCard.size !== 37
  || reviewedOnlyCards.length !== 35
  || matchedQuestionTopicLinks !== 546
  || reviewedOptionTopics.length !== 158
  || reviewedSpecificTopics.length !== 52
  || retainedLocalCards.length !== 536
  || retainedWrittenLogicalCards !== 144
  || retainedPracticalLogicalCards !== 392
) {
  throw new Error(`Art reference/local reconciliation counts changed unexpectedly: ${JSON.stringify({
    matched: matchedAssociations.length,
    blocked: sourceBlockedAssociations.length,
    anomalies: referenceAnomalyAssociations.length,
    exactCards: exactTopicsByCard.size,
    reviewedCards: reviewedTopicsByCard.size,
    links: matchedQuestionTopicLinks,
    options: reviewedOptionTopics.length,
    specific: reviewedSpecificTopics.length,
    retained: retainedLocalCards.length,
    retainedWritten: retainedWrittenLogicalCards,
  })}`);
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
  association.target ? componentCode(association.target.fileid) : '',
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
  referenceAnomalyAssociations: referenceAnomalyAssociations.length,
  matchedLogicalCards: exactTopicsByCard.size,
  reviewedLogicalCards: reviewedOnlyCards.length,
  reviewedOptionTopics: reviewedOptionTopics.length,
  reviewedSpecificTopics: reviewedSpecificTopics.length,
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
    referenceAnomalies: 'Seven 2021-2022 questions the reference files under a heading their printed dates or works contradict are filed under the heading the SEC paper supports (resolution reference-anomaly, with the evidence).',
    specificTopics: 'A question the reference files only under a generic bucket is also filed under the specific heading of its reviewed Mark Bank card (reviewedSpecificTopics).',
    optionTopics: 'Each printed option of a 2021-2022 choose-one question whose options are different periods or movements is added under its own heading (reviewedOptionTopics), matching its Mark Bank card.',
  },
  summary,
  curriculumCrosswalk,
  associations,
  retainedLocalCards,
  reviewedOptionTopics: reviewedOptionTopics.map(({ key, ...item }) => item),
  reviewedSpecificTopics,
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
