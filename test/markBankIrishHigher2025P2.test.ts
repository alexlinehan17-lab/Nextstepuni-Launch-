import { describe, expect, it } from 'vitest';
import { readFileSync } from 'node:fs';
import { execFileSync } from 'node:child_process';
import added from '../components/MarkBank/cards/irish/higher-2025-p2-authored.json';
import authored from '../components/MarkBank/cards/irish/authored.json';
import sourceReview from '../scripts/markbank/authored/irish-higher-2025-p2-source-review.json';
import inventory from '../scripts/markbank/authored/irish-archive-inventory.json';
import { CARDS as HIGHER } from '../components/MarkBank/cards/irish/higher';
import { irishMarks, irishScoreId } from '../components/MarkBank/SessionScreen';
import { examTopicIdsForQuestion, curriculumNodeIdsForExamTopic } from '../data/examTopics/registry';
import { tariffReconciles } from '../types/markBank';

type Card = { id: string; atlasQuestionId?: string; totalMarks: number; topicId: string; schemePages?: number[];
  reviewedPaperPages?: number[]; criteria: { id: string; maxMarks: number; permittedMarks: number[]; guidance: string[]; kind: string }[];
  markingGuideNote: string; questionText: string };
const cards = HIGHER.filter(c => c.year === 2025 && c.paperFileid === 'LC001ALP200IV');
const legacy = (authored.cards as unknown as (Card & { year: number; level: string; paper: number })[])
  .filter(c => c.year === 2025 && c.level === 'higher' && c.paper === 2);
const all = [...legacy, ...(added.cards as unknown as Card[])];
const get = (n: string) => all.find(c => c.atlasQuestionId === n)!;
const guide = (n: string) => get(n).criteria.map(c => c.guidance.join(' ')).join(' ');
const topicsFor = (n: string) => examTopicIdsForQuestion('irish', 'higher', 2025, 'main', n, 'p2', 'iv', 'LC001ALP200IV.pdf');

describe('2025 Higher Paper 2 source reconciliation (26 retained + 48 added)', () => {
  it('keeps every whole reading question and adds each published part and independent slot at its tariff', () => {
    expect(cards).toHaveLength(74);
    expect(new Set(cards.map(c => c.id)).size).toBe(74);
    for (const card of cards) expect(tariffReconciles(card), card.id).toBe(true);
    expect(legacy.map(c => c.id).sort()).toEqual([...added.review.legacyCardIds].sort());
    const wholes = legacy.filter(c => c.id.includes('-reading-'));
    expect(wholes.map(c => [c.atlasQuestionId, c.totalMarks])).toEqual(
      Array.from({ length: 12 }, (_, i) => [String(i + 1), i % 6 === 5 ? 15 : 7]));
    for (const c of wholes) {
      expect(c.criteria.map(r => [r.id, r.maxMarks]), c.id).toEqual(
        /q6$/.test(c.id) ? [['grammar', 3], ['point-1', 6], ['point-2', 6]] : [['a', 3], ['bi', 2], ['bii', 2]]);
    }
    // Repaired: Léamhthuiscint A Ceist 3 now carries its own (a) key, not Ceist 4–5.
    expect(guide('3')).toContain('Ba é an Fender Stratocaster sin príomhuirlis a cheirde ar feadh a shaoil = 3 mharc');
    expect(guide('3')).not.toContain('Luaigh dhá bhealach');
    const slots = added.cards.filter(c => /-\d$/.test(c.atlasQuestionId)).map(c => [c.atlasQuestionId, c.totalMarks]);
    expect(slots).toEqual([
      ['R-A-5-bi-1', 1], ['R-A-5-bi-2', 1], ['R-A-6-b-1', 6], ['R-A-6-b-2', 6],
      ['R-B-2-bi-1', 1], ['R-B-2-bi-2', 1], ['R-B-4-bi-1', 1], ['R-B-4-bi-2', 1], ['R-B-5-bi-1', 1], ['R-B-5-bi-2', 1],
      ['R-B-5-bii-1', 1], ['R-B-5-bii-2', 1], ['R-B-6-b-1', 6], ['R-B-6-b-2', 6],
    ]);
    expect(added.cards.filter(c => !/-\d$/.test(c.atlasQuestionId))).toHaveLength(34);
  });

  it('keeps order-dependent 2 + 1 items whole and allows only the printed mark values elsewhere', () => {
    for (const n of ['R-A-1-a', 'R-A-2-a', 'R-A-4-a', 'R-A-5-a', 'R-B-2-a', 'R-A-6-a', 'R-B-6-a']) {
      expect(get(n).criteria[0].permittedMarks, n).toEqual([0, 2, 3]);
    }
    expect(get('R-B-4-a').criteria[0].permittedMarks).toEqual([0, 1, 3]);
    expect(get('R-A-3-bii').criteria[0].permittedMarks).toEqual([0, 2]);
    expect(get('R-A-1-bi').criteria[0].permittedMarks).toEqual([0, 1, 2]);
    expect(get('R-A-6-a').topicId).toBe('irish-3-3');
    expect(guide('R-A-6-a')).toContain('cuirfear');
    expect(guide('R-B-6-a')).toContain('fógraíodh');
    expect(guide('R-A-6-b')).toContain('Pointe eolais 1 (P1)');
    expect(guide('R-B-5-bi-1')).toContain('Na cóitseálaithe is fearr = 1 mharc');
    for (const c of added.cards) {
      expect(c.sourceMaterial.pages, c.id).toEqual(c.atlasQuestionId.startsWith('R-A') ? [4, 5] : [6, 7]);
      expect(c.schemePages.every(p => p >= 19 && p <= 25), c.id).toBe(true);
    }
  });

  it('lifts the literature scheme onto the retained routes with one shared Gaeilge award', () => {
    const routes = legacy.filter(c => !c.id.includes('-reading-'));
    expect(routes.map(c => [c.atlasQuestionId, c.totalMarks, c.criteria.map(r => r.maxMarks)])).toEqual([
      ['P-2A-a', 30, [25, 5]], ['P-2A-b', 30, [25, 5]], ['P-2B-a', 30, [25, 5]], ['P-2B-b', 30, [25, 5]],
      ['F-3A-a', 30, [13, 5, 7, 5]], ['F-3A-b', 30, [13, 5, 7, 5]], ['F-3B-a', 30, [13, 5, 7, 5]], ['F-3B-b', 30, [13, 5, 7, 5]],
      ['X-4A', 40, [35, 5]], ['X-4B', 40, [35, 5]], ['X-4C', 40, [35, 5]], ['X-4D', 40, [35, 5]], ['X-4E', 40, [35, 5]], ['X-4F', 40, [17, 9, 9, 5]],
    ]);
    for (const c of routes) {
      const language = c.criteria.at(-1)!;
      expect(language).toMatchObject({ id: 'gaeilge', maxMarks: 5, kind: 'award' });
      expect(language.guidance.join(' '), c.id).toContain('Cumas lag/an-lag maidir leis na príomhghnéithe');
      expect(language.guidance.join(' '), c.id).not.toContain('sásúil');
      expect(c.markingGuideNote, c.id).toMatch(/indicative rather than exhaustive/);
    }
    expect(guide('P-2A-a')).toContain('Déan measúnú ar fhiúntas an phlé sa fhreagra as 18 marc');
    expect(guide('F-3A-a')).toContain('Gan ach íomhá amháin luaite agus pléite, marcáiltear an t-eolas as 10 marc');
    expect(get('F-3A-a').criteria[0].guidance[0]).toMatch(/^\(a\) An Spailpín Fánach \(i\)/);
    expect(guide('F-3A-b')).toContain('Pádraig Mac Suibhne');
    expect(guide('F-3B-a')).toContain('Príomhthéama = 2 mharc');
    expect(guide('X-4A')).toContain('as 25 marc');
    for (const c of routes) {
      for (const r of c.criteria.slice(0, -1)) expect(r.guidance.join(' '), c.id).not.toContain('Gaeilge (5 mharc)');
    }
    const route = cards.find(c => c.id === 'irish-2025-hl-p2-poetry-3a-a')!;
    if (route.rubric.system !== 'irish') throw new Error('Wrong rubric');
    expect(irishMarks(route, Object.fromEntries(route.rubric.criteria.map(c => [irishScoreId(c.id), c.maxMarks])))).toBe(30);
  });

  it('joins all 74 cards to Atlas with paper pages, scheme pages and same-level topics', () => {
    const map = JSON.parse(readFileSync('public/paper-answers/2025/LC001ALP200IV.pdf.json', 'utf8'));
    const q = (n: string) => map.q.find((q: { n: string }) => q.n === n);
    expect(map.schemeFileid).toBe('LC001ALP000IV.pdf');
    for (const c of all) {
      const n = c.atlasQuestionId!;
      expect(topicsFor(n).flatMap(curriculumNodeIdsForExamTopic), c.id).toContain(c.topicId);
      expect(q(n).paperRegion.map((r: { p: number }) => r.p), c.id).toEqual(c.reviewedPaperPages);
      expect((q(n).schemeRegion ?? q(n).region).map((r: { p: number }) => r.p), c.id).toEqual(c.schemePages);
    }
    expect(topicsFor('P-2A-b')).toEqual(['irish-higher-prescribed-prose-archive']);
    expect(topicsFor('F-3A-b')).toEqual(['irish-higher-prescribed-poetry-archive']);
    expect(topicsFor('X-4F')).toContain('irish-higher-danta-breise');
  });

  it('rejects unknown and stale raw selection directives', () => {
    const result = execFileSync('python3', ['-c', String.raw`
import sys,json
sys.path.insert(0,'scripts/markbank/authoring')
from irish_higher_2025_p2 import selection_decisions
review=json.load(sys.stdin)
class Page:
 def __init__(self,text): self.text=text
 def get_text(self): return self.text
pages=[Page('') for _ in range(16)]
for d in review['selectionDecisions']: pages[d['page']-1].text+=d['raw']+'\n'
assert len(selection_decisions(pages))==len(review['selectionDecisions'])
original=pages[11].text
for edited in [original+'\nFreagair do rogha dhá cheann as Ceist 4.\n',original.replace('(A, B, C, D, E nó F) thíos','(A, B, C, D nó E) thíos')]:
 pages[11].text=edited
 try: selection_decisions(pages)
 except AssertionError: pass
 else: raise AssertionError('Accepted an unknown/stale directive')
print('source guard passed')
`], { encoding: 'utf8', input: JSON.stringify(sourceReview) });
    expect(result).toContain('source guard passed');
  });

  it('records the visual sweep and reconciles the component without claiming archive completion', () => {
    expect(added.review.reviewedPaperPages).toEqual(Array.from({ length: 16 }, (_, i) => i + 1));
    expect(added.review.reviewedSchemePages).toEqual(Array.from({ length: 31 }, (_, i) => i + 18));
    expect(added.review.examStructure).toEqual({ readingA: 50, readingB: 50, prose: 30, poetry: 30, additionalLiterature: 40, total: 200 });
    const row = inventory.papers.find(p => p.key === '2025|higher|LC001ALP200IV.pdf')!;
    expect(row.markBankCardIds.slice().sort()).toEqual(cards.map(c => c.id).sort());
    expect(row).toMatchObject({ fullVisualReview: 'complete', bankAtlasTaskParity: 'complete', partAndSelectionReconciliation: 'complete' });
    expect(inventory.summary.papersPendingFullReview).toBe(64);
    expect(inventory.summary.orphanCardIds).toEqual([]);
  });
});
