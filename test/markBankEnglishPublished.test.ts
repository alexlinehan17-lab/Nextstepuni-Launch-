/** @license SPDX-License-Identifier: Apache-2.0 */
/**
 * Reviewed English papers published to Mark Bank paper by paper.
 *
 * A paper ships only when its own independent review gate passes
 * (scripts/markbank/authoring/english_publish.py). These tests pin what that
 * means at runtime: exactly those papers and nothing else, every legacy id and
 * alias intact, each year's own printed grid and cap rule, finite routes with
 * their tariff and reader, and Topic Atlas parity for every published card.
 */
import { describe, expect, it } from 'vitest';
import { CARDS as HIGHER } from '../components/MarkBank/cards/english/higher';
import { CARDS as ORDINARY } from '../components/MarkBank/cards/english/ordinary';
import publishedHigherJson from '../components/MarkBank/cards/english/published-higher.json';
import publishedOrdinaryJson from '../components/MarkBank/cards/english/published-ordinary.json';
import authoredJson from '../components/MarkBank/cards/english/authored.json';
import visualJson from '../scripts/markbank/authored/english-visual-review.json';
import gridsJson from '../scripts/markbank/authored/english-marking-grids.json';
import censusJson from '../scripts/markbank/authored/english-census.json';
import englishQuestionRuntime from '../data/examTopics/english-question-runtime.json';
import { CARD_ID_ALIASES } from '../components/MarkBank/cardAliases';
import { effectivePclmScores, pclmMarks } from '../components/MarkBank/SessionScreen';
import {
  curriculumNodeIdsForExamTopic,
  examTopicIdsForQuestion,
} from '../data/examTopics/registry';
import { questionsForTopics } from '../components/PaperTrail/topics';
import { PAPER_TRAIL_INDEX } from '../paperTrailData';
import { HOSTED_ANSWER_OVERRIDES, preferredAnswersUrl } from '../components/PaperTrail/vaultResolve';
import { readFileSync } from 'node:fs';
import { resolve } from 'node:path';
import {
  tariffReconciles,
  type PclmAssessment,
  type PclmRubric,
  type SecRubricCard,
} from '../types/markBank';

type EnglishCard = SecRubricCard & { rubric: PclmRubric };
interface PublishedRecord {
  id: string; year: number; level: 'higher' | 'ordinary'; paper: 1 | 2; topicId: string;
  atlas: { fileid: string; n: string };
}
interface PublishedManifest {
  papers: Array<{ paperId: string; tasks: number; cards: number }>;
  cards: PublishedRecord[];
  legacyAdditionalSources: Record<string, unknown[]>;
}

const publishedHigher = publishedHigherJson as unknown as PublishedManifest;
const publishedOrdinary = publishedOrdinaryJson as unknown as PublishedManifest;
const RECORDS = [...publishedHigher.cards, ...publishedOrdinary.cards];
const PUBLISHED_IDS = new Set(RECORDS.map(card => card.id));
const ALL = [...HIGHER, ...ORDINARY] as EnglishCard[];
const byId = new Map(ALL.map(card => [card.id, card]));
const PUBLISHED = ALL.filter(card => PUBLISHED_IDS.has(card.id));
const card = (id: string) => {
  const found = byId.get(id);
  if (!found) throw new Error(`missing published card ${id}`);
  return found;
};
const routesOf = (parent: string) => PUBLISHED.filter(entry => entry.id.startsWith(`${parent}-route-`));
const bandsOf = (assessment: PclmAssessment) => (assessment.mode === 'composite'
  ? assessment.components.flatMap(component => component.bands)
  : assessment.bands).map(band => [band.grade, band.marks] as const);

const legacyPapers = new Set(censusJson.asks.map(ask => `english-${ask.year}-${ask.level}-p${ask.paper}`));

describe('English paper-by-paper publication', () => {
  it('publishes exactly the papers whose own independent review is complete', () => {
    const reviewed = visualJson.papers.filter(entry => entry.visualSweepComplete
      && 'independentPaperTally' in entry && entry.allTaskBoundariesSchemeChecked
      && entry.allFiniteRoutesReconciled && !legacyPapers.has(entry.paperId));
    const published = [...publishedHigher.papers, ...publishedOrdinary.papers];
    expect(published.map(paper => paper.paperId).sort()).toEqual(reviewed.map(entry => entry.paperId).sort());
    expect(published).toHaveLength(34);
    for (const paper of published) {
      const entry = reviewed.find(row => row.paperId === paper.paperId)!;
      const tally = (entry as unknown as { independentPaperTally: { baseTasks: number; finiteRoutes: number } })
        .independentPaperTally;
      expect([paper.tasks, paper.cards], paper.paperId).toEqual([tally.baseTasks, tally.finiteRoutes]);
      expect(RECORDS.filter(record => record.id.startsWith(`${paper.paperId}-`)), paper.paperId)
        .toHaveLength(paper.cards);
    }
    expect(PUBLISHED).toHaveLength(1_916);
  });

  it('never publishes an unreviewed or legacy-served paper', () => {
    const unreviewed = ['english-2016-hl-p2', 'english-2016-ol-p2', 'english-2017-hl-p1',
      'english-2019-ol-p2', 'english-2020-hl-p1'];
    for (const paper of unreviewed) {
      expect(ALL.some(entry => entry.id.startsWith(`${paper}-`)), paper).toBe(false);
    }
    // 2021-2025 stay served only by their legacy cards until a legacy bridge exists.
    expect(RECORDS.some(record => record.year >= 2021 && record.year <= 2025)).toBe(false);
  });

  it('keeps all 650 legacy cards, their ids and their aliases', () => {
    const legacyIds = authoredJson.cards.map(entry => entry.id);
    expect(legacyIds).toHaveLength(650);
    expect(legacyIds.every(id => byId.has(id))).toBe(true);
    expect(ALL.filter(entry => !PUBLISHED_IDS.has(entry.id))).toHaveLength(650);
    const withdrawn = Object.entries(authoredJson.withdrawnAliases);
    expect(withdrawn).toHaveLength(10);
    for (const [oldId, canonical] of withdrawn) {
      expect(byId.has(oldId), oldId).toBe(false);
      expect(byId.has(canonical), canonical).toBe(true);
      expect(CARD_ID_ALIASES[oldId], oldId).toBe(canonical);
    }
    for (const ask of censusJson.asks) {
      expect(byId.has(CARD_ID_ALIASES[ask.id] ?? ask.id), ask.id).toBe(true);
    }
    expect(RECORDS.some(record => legacyIds.includes(record.id) || record.id in CARD_ID_ALIASES)).toBe(false);
    expect(publishedHigher.legacyAdditionalSources).toEqual({});
    expect(publishedOrdinary.legacyAdditionalSources).toEqual({});
  });
});

describe('English published cards use their own year’s printed grid and cap', () => {
  it('reconciles every published grid and keeps each year’s labels', () => {
    expect(PUBLISHED.filter(entry => !tariffReconciles(entry)).map(entry => entry.id)).toEqual([]);
    const sittings = gridsJson.sittings as Record<string, { family: string }>;
    const families = gridsJson.families as Record<string, { labels: string[]; combinedLabels: string[] }>;
    for (const entry of PUBLISHED) {
      const family = families[sittings[`${entry.year}-${entry.level}`].family];
      const labels = new Set([...family.labels, ...family.combinedLabels]);
      for (const [grade] of bandsOf(entry.rubric.assessment)) expect(labels.has(grade), entry.id).toBe(true);
      if (entry.year >= 2018) {
        const prefix = entry.level === 'higher' ? 'H' : 'O';
        expect(bandsOf(entry.rubric.assessment).every(([grade]) => grade.startsWith(prefix)), entry.id).toBe(true);
      }
    }
  });

  it('transcribes the 2010-2016 Ordinary combined grid exactly, overlaps and F/NG 1 included', () => {
    const entry = card('english-2015-ol-p1-t1-a-iii-a');
    expect(entry.totalMarks).toBe(10);
    expect(entry.rubric.assessment.mode).toBe('combined');
    expect(bandsOf(entry.rubric.assessment)).toEqual([
      ['A', [8, 9, 10]], ['B', [7, 8]], ['C', [5, 6]], ['D', [4, 5]], ['E', [2, 3]], ['F/NG', [1]],
    ]);
    if (entry.rubric.assessment.mode !== 'combined') throw new Error('unreachable');
    expect(entry.rubric.assessment.printedGrid).toEqual({
      sitting: '2015-ordinary', schemePages: [47], overlapping: true, lowestMark: 1,
    });
  });

  it('uses the 2010-2016 Higher A+ to E- anchors', () => {
    const entry = card('english-2012-hl-p1-t1-a-i');
    expect(bandsOf(entry.rubric.assessment)).toEqual([
      ['A+', [13, 14, 15]], ['B', [11]], ['C', [9]], ['D', [6]], ['E-', [0, 1, 2, 3, 4, 5]],
    ]);
  });

  it('applies the 2010-2015 Ordinary Language-at-D rule, not the modern Purpose cap', () => {
    const entry = card('english-2014-ol-p1-composing-1');
    const assessment = entry.rubric.assessment;
    if (assessment.mode !== 'discrete') throw new Error('expected discrete');
    expect(assessment.capRule).toEqual({ kind: 'language-at-d-band', purposeBelow: 12, coherenceBelow: 12, languageMax: 16 });
    expect(assessment.primacyOfPurpose).toBeUndefined();
    // Both P and C below D: Language is limited to the top of its D band.
    expect(effectivePclmScores(entry, { purpose: 10, coherence: 11, language: 25, mechanics: 8 }))
      .toEqual({ purpose: 10, coherence: 11, language: 16, mechanics: 8 });
    // Coherence reaches D: no cap, and C may exceed P.
    expect(pclmMarks(entry, { purpose: 10, coherence: 20, language: 25, mechanics: 8 })).toBe(63);
  });

  it('prints no cap where the scheme prints none (2010-2015 HL, 2018 OL)', () => {
    const higher = card('english-2012-hl-p1-t1-b');
    if (higher.rubric.assessment.mode !== 'discrete') throw new Error('expected discrete');
    expect(higher.rubric.assessment.capRule).toEqual({ kind: 'none' });
    expect(higher.rubric.assessment.criteria.map(criterion => criterion.permittedMarks)).toEqual([
      [0, 1, 2, 3, 4, 5, 6, 9, 11, 13, 14, 15], [0, 1, 2, 3, 4, 5, 6, 9, 11, 13, 14, 15],
      [0, 1, 2, 3, 4, 5, 6, 9, 11, 13, 14, 15], [0, 1, 2, 3, 4, 5],
    ]);
    expect(pclmMarks(higher, { purpose: 6, coherence: 13, language: 11, mechanics: 4 })).toBe(34);
    const ordinary = card('english-2018-ol-p2-single-a-q3-i');
    if (ordinary.rubric.assessment.mode !== 'discrete') throw new Error('expected discrete');
    expect(ordinary.totalMarks).toBe(30);
    expect(ordinary.rubric.assessment.capRule).toEqual({ kind: 'none' });
    expect(ordinary.rubric.assessment.criteria.map(criterion => criterion.permittedMarks.at(-1)))
      .toEqual([9, 9, 9, 3]);
  });

  it('applies C/L <= P where the scheme prints it (2016, 2018 HL, 2026)', () => {
    for (const id of ['english-2016-ol-p1-composing-1', 'english-2018-hl-p1-composing-1', 'english-2026-hl-p1-t1-b']) {
      const entry = card(id);
      if (entry.rubric.assessment.mode !== 'discrete') throw new Error(id);
      expect(entry.rubric.assessment.capRule, id).toEqual({ kind: 'purpose-primacy' });
      const scores = { purpose: 9, coherence: 15, language: 14, mechanics: 5 };
      const effective = effectivePclmScores(entry, scores);
      expect([effective.coherence, effective.language], id).toEqual([9, 9]);
    }
  });

  it('uses the modern O1-O8 and H1-H8 prints for 2026', () => {
    expect(bandsOf(card('english-2026-ol-p2-unseen-q1').rubric.assessment)).toEqual([
      ['O1', [9, 10]], ['O2', [8]], ['O3', [7]], ['O4', [6]], ['O5', [5]], ['O6', [4]], ['O7', [3]], ['O8', [0, 1, 2]],
    ]);
    expect(bandsOf(card('english-2026-hl-p2-comparative-a-q1-a').rubric.assessment)).toEqual([
      ['H1', [27, 28, 29, 30]], ['H2', [24]], ['H3', [21]], ['H4', [18]], ['H5', [15]], ['H6', [12]],
      ['H7', [9]], ['H8', [0, 1, 2, 3, 4, 5, 6, 7, 8]],
    ]);
  });
});

describe('English published routes and readers', () => {
  it('expands finite printed choices into full-tariff routes with the parent reader', () => {
    const posters = routesOf('english-2016-hl-p1-t1-b');
    expect(posters).toHaveLength(12);
    expect(posters.every(entry => entry.totalMarks === 50 && entry.sourceMaterial?.pages.join() === '2')).toBe(true);
    const views = routesOf('english-2026-hl-p2-comparative-b-q1-a');
    expect(views.map(entry => entry.totalMarks)).toEqual([30, 30]);
    expect(views[0].questionText).toContain('predominantly by my emotional response');
    expect(routesOf('english-2015-hl-p2-single-c-ii').map(entry => entry.totalMarks)).toEqual([60, 60, 60]);
    expect(routesOf('english-2026-ol-p2-unseen-q2').every(entry => entry.sourceMaterial?.pages.join() === '14')).toBe(true);
    // A parent of finite routes is never also a card.
    expect(byId.has('english-2016-hl-p1-t1-b')).toBe(false);
  });

  it('carries the reviewed readers, companions and exclusions', () => {
    const yeats = routesOf('english-2010-ol-p2-prescribed-d-q2-iii');
    expect(yeats).toHaveLength(2);
    expect(yeats.every(entry => entry.sourceMaterial?.kind === 'supplementary-text'
      && (entry.sourceMaterial.texts?.length ?? 0) === 2)).toBe(true);
    const hopkins = card('english-2011-ol-p2-prescribed-d-q2-iii');
    expect(hopkins.additionalSourceMaterials?.map(source => [source.title, source.sourceYear, source.pages]))
      .toEqual([['Inversnaid', 2021, [20]]]);
    const plath = routesOf('english-2014-ol-p2-prescribed-c-q2-iii');
    expect(plath.length).toBeGreaterThan(0);
    expect(plath.every(entry => entry.additionalSourceMaterials?.[0]?.kind === 'linked-reading')).toBe(true);
    expect(card('english-2016-ol-p1-t1-a-iii-b').sourceMaterial).toBeUndefined();
    expect(card('english-2026-ol-p2-prescribed-c-q1-a').sourceMaterial).toMatchObject({ title: 'It’s Not', pages: [17] });
    expect(card('english-2010-ol-p2-comparative-a-q1-a').stem).toContain('Before beginning, name the texts');
  });
});

describe('English Topic Atlas parity for published papers', () => {
  it('files every published card under a topic carrying its canonical node', () => {
    const missing: string[] = [];
    for (const record of RECORDS) {
      const topics = examTopicIdsForQuestion('english', record.level, record.year, 'main', record.atlas.n,
        `p${record.paper}`, 'ev', record.atlas.fileid);
      if (!topics.some(topic => curriculumNodeIdsForExamTopic(topic).includes(record.topicId))) {
        missing.push(`${record.id} -> ${record.atlas.fileid} Q${record.atlas.n}`);
      }
    }
    expect(missing).toEqual([]);
  });

  it('only adds to the existing exact mappings', () => {
    const lost: string[] = [];
    for (const [level, , year, paperKey, fileid, n, indexes] of englishQuestionRuntime.questionMappings as Array<
      [string, string, number, string, string, string, number[]]>) {
      const now = examTopicIdsForQuestion('english', level === 'h' ? 'higher' : 'ordinary', year, 'main', n,
        paperKey, 'ev', fileid);
      for (const index of indexes) {
        const topic = englishQuestionRuntime.topicIds[index];
        if (!now.includes(topic)) lost.push(`${year} ${fileid} Q${n}: ${topic}`);
      }
    }
    expect(lost).toEqual([]);
  });

  it('serves every published paper\'s reviewed answer map and lists every block', () => {
    // Each published paper's reviewed sidecar is hosted byte-identically
    // (public/paper-answers, HOSTED_ANSWER_OVERRIDES) and flagged live in the
    // index, so its Atlas blocks resolve to the reviewed paper and scheme crops.
    const live = new Set(PAPER_TRAIL_INDEX.english.flatMap(entry => entry.papers
      .filter(item => item.answers === 1)
      .map(item => `${entry.year}|${entry.level}|${item.doc.f}`)));
    const papers = [...new Set(RECORDS.map(record => `${record.year}|${record.level}|${record.atlas.fileid}`))];
    expect(papers).toHaveLength(34);
    for (const paper of papers) {
      const [year, , fileid] = paper.split('|');
      expect(live.has(paper), `${paper} answers flag`).toBe(true);
      expect(HOSTED_ANSWER_OVERRIDES.has(`english|${year}|${fileid}`), `${paper} hosted`).toBe(true);
      expect(preferredAnswersUrl('english', Number(year), fileid, 'storage'))
        .toBe(`/paper-answers/${year}/${fileid}.json`);
      const hosted = readFileSync(resolve(__dirname, `../public/paper-answers/${year}/${fileid}.json`), 'utf8');
      const reviewed = readFileSync(resolve(__dirname, `../scripts/paper-trail/answers/${year}/${fileid}.json`), 'utf8');
      expect(hosted, paper).toBe(reviewed);
      const blocks = new Set((JSON.parse(hosted) as { q: Array<{ n: string }> }).q.map(question => question.n));
      for (const record of RECORDS.filter(entry => `${entry.year}|${entry.level}|${entry.atlas.fileid}` === paper)) {
        expect(blocks.has(record.atlas.n), `${record.id} block ${record.atlas.n}`).toBe(true);
      }
    }
    const browsable = new Set(questionsForTopics('english', null)
      .map(question => `${question.year}|${question.fileid}|${question.n}`));
    const absent = [...new Set(RECORDS.map(record => `${record.year}|${record.atlas.fileid}|${record.atlas.n}`))]
      .filter(key => !browsable.has(key));
    expect(absent).toEqual([]);
  });
});
