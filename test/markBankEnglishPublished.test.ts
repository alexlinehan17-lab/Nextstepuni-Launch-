/** @license SPDX-License-Identifier: Apache-2.0 */
/**
 * Reviewed English papers published to Mark Bank paper by paper.
 *
 * A paper ships only when its own independent review gate passes
 * (scripts/markbank/authoring/english_publish.py). These tests pin what that
 * means at runtime: exactly those papers and nothing else, every legacy id and
 * alias intact (a bridged legacy paper keeps each legacy id on its published
 * card or as a progress alias), each year's own printed grid and cap rule,
 * finite routes with their tariff and reader, and Topic Atlas parity for every
 * published card.
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
  atlasPlacements?: Array<{ fileid: string; n: string }>;
}
interface PublishedManifest {
  papers: Array<{ paperId: string; tasks: number; cards: number; printedDuplicates: number }>;
  cards: PublishedRecord[];
  legacyAdditionalSources: Record<string, unknown[]>;
  bridgedPapers: string[];
  bridgedLegacyIds: string[];
  bridgeAliases: Record<string, string>;
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
const placesOf = (record: PublishedRecord) => [record.atlas, ...(record.atlasPlacements ?? [])];
const bandsOf = (assessment: PclmAssessment) => (assessment.mode === 'composite'
  ? assessment.components.flatMap(component => component.bands)
  : assessment.bands).map(band => [band.grade, band.marks] as const);

const legacyPapers = new Set(censusJson.asks.map(ask => `english-${ask.year}-${ask.level}-p${ask.paper}`));
const BRIDGED_PAPERS = new Set([...publishedHigher.bridgedPapers, ...publishedOrdinary.bridgedPapers]);
const BRIDGED_IDS = new Set([...publishedHigher.bridgedLegacyIds, ...publishedOrdinary.bridgedLegacyIds]);
const BRIDGE_ALIASES = { ...publishedHigher.bridgeAliases, ...publishedOrdinary.bridgeAliases };
const paperOf = (record: PublishedRecord) =>
  `english-${record.year}-${record.level === 'higher' ? 'hl' : 'ol'}-p${record.paper}`;

describe('English paper-by-paper publication', () => {
  it('publishes exactly the papers whose own independent review is complete', () => {
    const reviewed = visualJson.papers.filter(entry => entry.visualSweepComplete
      && 'independentPaperTally' in entry && entry.allTaskBoundariesSchemeChecked
      && entry.allFiniteRoutesReconciled
      && (!legacyPapers.has(entry.paperId) || BRIDGED_PAPERS.has(entry.paperId)));
    const published = [...publishedHigher.papers, ...publishedOrdinary.papers];
    expect(published.map(paper => paper.paperId).sort()).toEqual(reviewed.map(entry => entry.paperId).sort());
    expect(published).toHaveLength(36);
    expect([...BRIDGED_PAPERS].sort()).toEqual(['english-2025-hl-p1', 'english-2025-hl-p2']);
    for (const paper of published) {
      const entry = reviewed.find(row => row.paperId === paper.paperId)!;
      const tally = (entry as unknown as { independentPaperTally: { baseTasks: number; finiteRoutes: number } })
        .independentPaperTally;
      // One card per task (a printed choice is one card); a task printed twice
      // on the paper is published once (english-printed-duplicates.json).
      expect([paper.tasks, paper.cards + paper.printedDuplicates], paper.paperId)
        .toEqual([tally.baseTasks, tally.finiteRoutes]);
      expect(RECORDS.filter(record => record.id.startsWith(`${paper.paperId}-`)), paper.paperId)
        .toHaveLength(paper.cards);
    }
    expect(PUBLISHED).toHaveLength(1_329);
  });

  it('never publishes an unreviewed or legacy-served paper', () => {
    const unreviewed = ['english-2016-hl-p2', 'english-2016-ol-p2', 'english-2017-hl-p1',
      'english-2019-ol-p2', 'english-2020-hl-p1'];
    for (const paper of unreviewed) {
      expect(ALL.some(entry => entry.id.startsWith(`${paper}-`)), paper).toBe(false);
    }
    // 2021-2025 stay served only by their legacy cards unless a legacy bridge exists.
    expect(RECORDS.filter(record => record.year >= 2021 && record.year <= 2025)
      .every(record => BRIDGED_PAPERS.has(paperOf(record)))).toBe(true);
  });

  it('keeps every one of the 650 legacy ids: live, or a progress alias to a live card', () => {
    const legacyIds = authoredJson.cards.map(entry => entry.id);
    expect(legacyIds).toHaveLength(650);
    const lost = legacyIds.filter(id => !byId.has(id) && !byId.has(CARD_ID_ALIASES[id] ?? ''));
    expect(lost).toEqual([]);
    // Unbridged legacy cards are served exactly as before.
    expect(ALL.filter(entry => !PUBLISHED_IDS.has(entry.id))).toHaveLength(650 - BRIDGED_IDS.size);
    expect(legacyIds.filter(id => !BRIDGED_IDS.has(id)).every(id => byId.has(id) && !PUBLISHED_IDS.has(id))).toBe(true);
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
    // Only a same-id bridge lets a published card carry a legacy id; no
    // published id is ever an alias.
    const reused = RECORDS.filter(record => legacyIds.includes(record.id)).map(record => record.id).sort();
    expect(reused).toEqual([...BRIDGED_IDS].filter(id => !(id in BRIDGE_ALIASES)).sort());
    expect(RECORDS.some(record => record.id in CARD_ID_ALIASES)).toBe(false);
    expect(publishedHigher.legacyAdditionalSources).toEqual({});
    expect(publishedOrdinary.legacyAdditionalSources).toEqual({});
  });

  it('bridges 2025 Higher Level: 38 ids kept by their reviewed card, 4 explicit progress aliases', () => {
    const bridged = [...BRIDGED_IDS].sort();
    expect(bridged).toEqual(authoredJson.cards.map(entry => entry.id)
      .filter(id => /^english-2025-hl-p[12]-/.test(id)).sort());
    expect(bridged).toHaveLength(42);
    expect(BRIDGE_ALIASES).toEqual({
      'english-2025-hl-p2-comparative-a-q1': 'english-2025-hl-p2-comparative-a-q1-a',
      'english-2025-hl-p2-comparative-b-q1': 'english-2025-hl-p2-comparative-b-q1-a',
      'english-2025-hl-p2-comparative-c-q1': 'english-2025-hl-p2-comparative-c-q1-a',
      'english-2025-hl-p2-unseen-q1': 'english-2025-hl-p2-unseen-q1-a',
    });
    for (const id of bridged) {
      const alias = BRIDGE_ALIASES[id];
      if (alias) {
        expect(byId.has(id), id).toBe(false);
        expect(CARD_ID_ALIASES[id], id).toBe(alias);
        expect(PUBLISHED_IDS.has(alias), alias).toBe(true);
      } else {
        // The id is now served by the independently reviewed card, not the legacy one.
        expect(card(id).qa.humanReviewedBy, id).toBe('independent-paper-review');
      }
    }
    // Every 2025 HL card is now a reviewed card; no legacy version is served twice.
    expect(ALL.filter(entry => entry.year === 2025 && entry.level === 'higher')
      .every(entry => PUBLISHED_IDS.has(entry.id))).toBe(true);
    expect(PUBLISHED.filter(entry => entry.year === 2025)).toHaveLength(46);
  });

  it('keeps the six 2025 Paper 1 indicative lists, lifted verbatim from the scheme', () => {
    const squash = (value: string) => value.replace(/[‐‑‒–—−]/g, '-').replace(/\s+/g, '');
    const scheme = readFileSync(resolve(__dirname, '../examiner-reports/english/schemes/2025-hl.md'), 'utf8');
    const carrying = PUBLISHED.filter(entry => entry.rubric.indicativeMaterial?.length);
    expect(carrying.map(entry => entry.id).sort()).toEqual([
      'english-2025-hl-p1-t1-a-i', 'english-2025-hl-p1-t1-a-iii', 'english-2025-hl-p1-t2-a-i',
      'english-2025-hl-p1-t2-a-iii', 'english-2025-hl-p1-t3-a-i', 'english-2025-hl-p1-t3-a-iii',
    ]);
    for (const entry of carrying) {
      expect(entry.rubric.indicativeMaterial, entry.id).toHaveLength(6);
      for (const item of entry.rubric.indicativeMaterial ?? []) {
        expect(squash(scheme).includes(squash(item)), `${entry.id}: ${item}`).toBe(true);
      }
      expect(entry.rubric.indicativeMaterialNote).toContain('none is a required answer');
    }
    expect(card('english-2025-hl-p1-t1-a-i').rubric.indicativeMaterial?.[0])
      .toBe('‘underdog effect’ heightens our empathy/has an emotional effect/a bias - we romanticise the underdog');
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

  it('applies C/L <= P where the scheme prints it (2016, 2018 HL, 2025 HL, 2026)', () => {
    for (const id of ['english-2016-ol-p1-composing-1', 'english-2018-hl-p1-composing-1', 'english-2025-hl-p2-prescribed-1',
      'english-2026-hl-p1-t1-b']) {
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

describe('English published printed choices and readers', () => {
  it('publishes a printed choice the scheme marks identically as ONE card with the printed instruction', () => {
    expect(PUBLISHED.some(entry => entry.id.includes('-route-'))).toBe(false);
    const posters = card('english-2016-hl-p1-t1-b');
    expect([posters.totalMarks, posters.sourceMaterial?.pages.join()]).toEqual([50, '2']);
    expect(posters.rubric.taskRequirements).toContain(
      'Make the choice the paper prints (First prize: 1 of 4; Second prize: 1 of 4, each a different one). '
      + 'Every choice is marked on the same grid.');
    const advice = card('english-2026-ol-p1-t3-a-i');
    expect([advice.totalMarks, advice.sourceMaterial?.pages.join(), advice.questionText.includes('For this practice response')])
      .toEqual([15, '6', false]);
    expect(advice.rubric.taskRequirements[1]).toBe(
      'Make the choice the paper prints (Most valuable: 2 of 10; Least valuable: 1 of 10, each a different one). '
      + 'Every choice is marked on the same grid.');
    expect(card('english-2026-hl-p2-comparative-b-q1-a').totalMarks).toBe(30);
    expect(card('english-2015-hl-p2-single-c-ii').totalMarks).toBe(60);
    expect(card('english-2026-ol-p2-unseen-q2').sourceMaterial?.pages.join()).toBe('14');
    expect(PUBLISHED.filter(entry => entry.id.startsWith('english-2026-ol-p1-'))).toHaveLength(20);
  });

  it('publishes a task printed more than once on a paper once, keeping every printed placement', () => {
    const either = RECORDS.find(record => record.id === 'english-2026-ol-p1-t1-a-iii-a')!;
    expect(placesOf(either).map(place => place.n)).toEqual(['8', '10', '12']);
    for (const id of ['english-2026-ol-p1-t2-a-iii-a', 'english-2026-ol-p1-t3-a-iii-a',
      'english-2026-ol-p2-comparative-a-q2-b', 'english-2026-ol-p2-comparative-b-q2-b',
      'english-2026-ol-p2-comparative-c-q2-b', 'english-2018-ol-p2-comparative-a-q2-b']) {
      expect(byId.has(id), id).toBe(false);
    }
    for (const id of ['english-2026-ol-p2-comparative-a-q1-b', 'english-2018-ol-p2-comparative-a-q1-b']) {
      expect(card(id).totalMarks, id).toBe(40);
    }
  });

  it('carries the reviewed readers, companions and exclusions', () => {
    const yeats = card('english-2010-ol-p2-prescribed-d-q2-iii');
    expect(yeats.sourceMaterial?.kind === 'supplementary-text'
      && (yeats.sourceMaterial.texts?.length ?? 0) === 2).toBe(true);
    const hopkins = card('english-2011-ol-p2-prescribed-d-q2-iii');
    expect(hopkins.additionalSourceMaterials?.map(source => [source.title, source.sourceYear, source.pages]))
      .toEqual([['Inversnaid', 2021, [20]]]);
    const plath = card('english-2014-ol-p2-prescribed-c-q2-iii');
    expect(plath.additionalSourceMaterials?.[0]?.kind).toBe('linked-reading');
    expect(card('english-2016-ol-p1-t1-a-iii-b').sourceMaterial).toBeUndefined();
    expect(card('english-2026-ol-p2-prescribed-c-q1-a').sourceMaterial).toMatchObject({ title: 'It’s Not', pages: [17] });
    expect(card('english-2010-ol-p2-comparative-a-q1-a').stem).toContain('Before beginning, name the texts');
  });
});

describe('English Topic Atlas parity for published papers', () => {
  it('files every published card under a topic carrying its canonical node', () => {
    const missing: string[] = [];
    for (const record of RECORDS) {
      for (const place of placesOf(record)) {
        const topics = examTopicIdsForQuestion('english', record.level, record.year, 'main', place.n,
          `p${record.paper}`, 'ev', place.fileid);
        if (!topics.some(topic => curriculumNodeIdsForExamTopic(topic).includes(record.topicId))) {
          missing.push(`${record.id} -> ${place.fileid} Q${place.n}`);
        }
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
    expect(papers).toHaveLength(36);
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
        for (const place of placesOf(record)) expect(blocks.has(place.n), `${record.id} block ${place.n}`).toBe(true);
      }
    }
    const browsable = new Set(questionsForTopics('english', null)
      .map(question => `${question.year}|${question.fileid}|${question.n}`));
    const absent = [...new Set(RECORDS.map(record => `${record.year}|${record.atlas.fileid}|${record.atlas.n}`))]
      .filter(key => !browsable.has(key));
    expect(absent).toEqual([]);
  });
});
