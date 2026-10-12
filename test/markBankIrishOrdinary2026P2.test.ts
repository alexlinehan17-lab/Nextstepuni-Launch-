import { describe, expect, it } from 'vitest';
import { readFileSync } from 'node:fs';
import { execFileSync } from 'node:child_process';
import authored from '../components/MarkBank/cards/irish/ordinary-2026-p2-authored.json';
import sourceReview from '../scripts/markbank/authored/irish-ordinary-2026-p2-source-review.json';
import inventory from '../scripts/markbank/authored/irish-archive-inventory.json';
import { CARDS as ORDINARY } from '../components/MarkBank/cards/irish/ordinary';
import { irishMarks, irishScoreId } from '../components/MarkBank/SessionScreen';
import { examTopicIdsForQuestion, curriculumNodeIdsForExamTopic } from '../data/examTopics/registry';
import { tariffReconciles } from '../types/markBank';

const cards = ORDINARY.filter(c => c.year === 2026 && c.paperFileid === 'LC001GLP200IV');
const get = (key: string) => authored.cards.find(c => c.atlasQuestionId === key)!;
const guide = (key: string) => get(key).criteria.map(c => c.guidance.join(' ')).join(' ');
const topicsFor = (key: string) => examTopicIdsForQuestion('irish', 'ordinary', 2026, 'main', key, 'p2', 'iv', 'LC001GLP200IV.pdf');

describe('2026 Ordinary Paper 2 source reconciliation', () => {
  it('keeps all ten reading questions whole and each printed part at 5 marks', () => {
    expect(cards).toHaveLength(72);
    expect(new Set(cards.map(c => c.id)).size).toBe(72);
    for (const card of cards) expect(tariffReconciles(card), card.id).toBe(true);
    const wholes = authored.cards.filter(c => /^R-[AB]-\d$/.test(c.atlasQuestionId));
    expect(wholes.map(c => c.totalMarks)).toEqual(Array(10).fill(10));
    expect(wholes.reduce((sum, c) => sum + c.totalMarks, 0)).toBe(100);
    const parts = authored.cards.filter(c => /^R-[AB]-\d-[ab]$/.test(c.atlasQuestionId));
    expect(parts).toHaveLength(20);
    expect(parts.every(c => c.totalMarks === 5)).toBe(true);
    // "3 mharc + 2 mharc" (first correct 3, second 2) and printed "= 3 mharc" partials stay 0/3/5.
    for (const key of ['R-A-2-a', 'R-A-2-b', 'R-B-1-a', 'R-B-4-b', 'R-B-5-a']) {
      expect(get(key).criteria[0].permittedMarks, key).toEqual([0, 3, 5]);
      expect(guide(key), key).toContain('3 mharc + 2 mharc = 5 mharc');
    }
    expect(get('R-A-1-a').criteria[0].permittedMarks).toEqual([0, 3, 5]);
    expect(guide('R-A-1-a')).toContain('Bhog siad ó Ghaeltacht Chonamara go Ráth Chairn = 5 mharc');
    for (const key of ['R-A-1-b', 'R-B-2-b']) expect(get(key).criteria[0].permittedMarks, key).toEqual([0, 5]);
    expect(guide('R-B-2-b')).toContain('Céline Dion');
    for (const c of [...wholes, ...parts]) {
      expect(c.markingGuideNote, c.id).toContain('Gaeilge lochtach: 0 - 5 a bhaint den iomlán a gnóthaíodh');
      expect(c.sourceMaterial.pages, c.id).toEqual(c.atlasQuestionId.startsWith('R-A') ? [4, 5] : [6, 7]);
      expect(c.schemePages.every(p => (c.atlasQuestionId.startsWith('R-A') ? [15, 16] : [17, 18]).includes(p)), c.id).toBe(true);
    }
    expect(get('R-A-3').criteria.map(c => c.id)).toEqual(['a', 'b']);
    expect(get('R-B-5-b').questionText).toBe('5(b) Cad a chreideann Andrea Corr faoin gceol? (Alt 5)');
  });

  it('expands every printed literature route with its own tariffs and one 0–4 Gaeilge deduction', () => {
    const routes = authored.cards.filter(c => /^(P-2[AB]-[abc](-caca-milis|-an-lasair-choille|-scannan|-drama)?|F-3[AB]-[abc])$/.test(c.atlasQuestionId));
    expect(routes.map(c => [c.atlasQuestionId, c.totalMarks, c.topicId])).toEqual([
      ['P-2A-a-caca-milis', 25, 'irish-4-6'], ['P-2A-a-an-lasair-choille', 25, 'irish-4-8'], ['P-2A-b', 25, 'irish-4-4'], ['P-2A-c', 25, 'irish-4-5'],
      ['P-2B-a-scannan', 25, 'irish-4-7'], ['P-2B-a-drama', 25, 'irish-4-7'], ['P-2B-b', 25, 'irish-4-7'], ['P-2B-c', 25, 'irish-4-7'],
      ['F-3A-a', 25, 'irish-5-2'], ['F-3A-b', 25, 'irish-5-3'], ['F-3A-c', 25, 'irish-5-1'],
      ['F-3B-a', 25, 'irish-5-6'], ['F-3B-b', 25, 'irish-5-6'], ['F-3B-c', 25, 'irish-5-6'],
    ]);
    for (const c of routes) expect(c.criteria.at(-1), c.id).toMatchObject({ id: 'gaeilge-deduction', kind: 'deduction', maxMarks: 4 });
    for (const key of ['F-3A-a', 'F-3A-b', 'F-3A-c']) expect(get(key).criteria.map(c => c.maxMarks), key).toEqual([8, 8, 9, 4]);
    for (const key of ['F-3B-a', 'F-3B-b', 'F-3B-c']) expect(get(key).criteria.map(c => c.maxMarks), key).toEqual([9, 7, 7, 2, 4]);
    for (const key of ['P-2B-a-scannan', 'P-2B-a-drama', 'P-2B-b', 'P-2B-c']) expect(get(key).criteria.map(c => c.maxMarks), key).toEqual([23, 2, 4]);
    expect(get('P-2B-a-scannan').criteria[1].guidance).toEqual(['Teideal an scannáin = 1 mharc Ainm an scríbhneora = 1 mharc (2 mharc)']);
    expect(get('P-2B-c').criteria[1].guidance[0]).toContain('Ainm an údair = 1 mharc');
    expect(guide('P-2A-b')).toContain('2 mharc ar lomphointe eolais agus 3 mharc ar fhorbairt');
    expect(guide('F-3A-c-iii')).toContain('Tá/Níl = 1 mharc');
    // No route or sub-question carries the language note inside an award.
    for (const c of authored.cards) {
      for (const criterion of c.criteria.filter(r => r.kind === 'award')) {
        expect(criterion.guidance.join(' '), `${c.id} ${criterion.id}`).not.toMatch(/\[\s*Gaeilge lochtach/);
      }
    }
    const route = cards.find(c => c.id === 'irish-2026-ol-p2-poetry-3a-a')!;
    if (route.rubric.system !== 'irish') throw new Error('Wrong rubric');
    const full = (deduct: number) => Object.fromEntries(route.rubric.criteria.map(c => [irishScoreId(c.id), c.kind === 'deduction' ? deduct : c.maxMarks]));
    expect(irishMarks(route, full(0))).toBe(25);
    expect(irishMarks(route, full(4))).toBe(21);
  });

  it('ships each printed prescribed sub-question, and 3A(b)(i)(a)–(d), at its published tariff', () => {
    const subs = authored.cards.filter(c => /^(P-2A-(a-caca-milis|a-an-lasair-choille|c)|F-3A-[abc])-[iv]+$/.test(c.atlasQuestionId));
    expect(subs).toHaveLength(24);
    expect(subs.filter(c => c.atlasQuestionId.startsWith('P-')).every(c => c.totalMarks === 5)).toBe(true);
    expect(subs.filter(c => c.atlasQuestionId.startsWith('F-')).map(c => c.totalMarks)).toEqual([8, 8, 9, 8, 8, 9, 8, 8, 9]);
    for (const key of ['P-2A-a-caca-milis-i', 'P-2A-a-an-lasair-choille-iii', 'P-2A-c-iv']) {
      expect(get(key).criteria[0].permittedMarks, key).toEqual([0, 3, 5]);
      expect(guide(key), key).toContain('3 mharc + 2 mharc');
    }
    expect(get('P-2A-a-caca-milis-v').criteria[0].permittedMarks).toEqual([0, 1, 2, 3, 4, 5]);
    const slots = authored.cards.filter(c => /^F-3A-b-i-[a-d]$/.test(c.atlasQuestionId));
    expect(slots.map(c => [c.atlasQuestionId, c.totalMarks, c.criteria[0].permittedMarks])).toEqual(
      ['a', 'b', 'c', 'd'].map(s => [`F-3A-b-i-${s}`, 2, [0, 2]]));
    expect(guide('F-3A-b-i-a')).toContain('Freagra: An tEarrach');
    expect(guide('F-3A-b-i-d')).toContain('ór-mhuir');
    expect(get('F-3A-b').criteria[0].permittedMarks).toEqual([0, 2, 4, 6, 8]);
    expect(get('F-3A-a').sourceMaterial.pages).toEqual([10]);
    expect(get('F-3A-c').schemePages).toEqual([30, 31]);
  });

  it('treats each choose-two within 2A, 2B, 3A and 3B as a choice, not a route', () => {
    // Each printed route keeps its own 25-mark card and carries the instruction; no two-route combination cards.
    expect(authored.cards.filter(c => 'memberCardIds' in c)).toEqual([]);
    const routes = authored.cards.filter(c => /^(P-2[AB]-[abc](-caca-milis|-an-lasair-choille|-scannan|-drama)?|F-3[AB]-[abc])$/.test(c.atlasQuestionId));
    expect(routes).toHaveLength(14);
    for (const route of routes) {
      expect(route.totalMarks, route.id).toBe(25);
      expect(route.taskRequirements[0], route.id).toBe('Freagair do rogha dhá cheann as (a), (b) nó (c).');
    }
    expect(get('F-3B-a').questionText).toContain('Níl cead an dán roghnach céanna a úsáid faoi dhó');
    expect(authored.review).not.toHaveProperty('pairedRouteCardIds');
    const route = cards.find(c => c.id === 'irish-2026-ol-p2-prose-2a-a-caca-milis')!;
    if (route.rubric.system !== 'irish') throw new Error('Wrong rubric');
    const scores = Object.fromEntries(route.rubric.criteria.map(c => [irishScoreId(c.id), c.kind === 'deduction' ? 0 : c.maxMarks]));
    expect(irishMarks(route, scores)).toBe(25);
  });

  it('joins all 72 cards to Atlas with paper pages, scheme pages and same-level topics', () => {
    const map = JSON.parse(readFileSync('public/paper-answers/2026/LC001GLP200IV.pdf.json', 'utf8'));
    const q = (n: string) => map.q.find((q: { n: string }) => q.n === n);
    expect(map.schemeFileid).toBe('LC001GLP100IV.pdf');
    for (const c of authored.cards) {
      expect(topicsFor(c.atlasQuestionId).flatMap(curriculumNodeIdsForExamTopic), c.id).toContain(c.topicId);
      expect(q(c.atlasQuestionId).paperRegion.map((r: { p: number }) => r.p), c.id).toEqual(c.reviewedPaperPages);
      expect(q(c.atlasQuestionId).region.map((r: { p: number }) => r.p), c.id).toEqual(c.schemePages);
      expect(q(c.atlasQuestionId).label, c.id).toBe(c.questionRef.replace('2026 OL Paper 2 ', ''));
    }
    for (const n of ['1', '2', '3']) expect(q(n), n).toBeDefined();
    expect(topicsFor('R-A-1-a')).toEqual(['irish-ordinary-reading-comprehension']);
    expect(topicsFor('P-2A-c')).toEqual(['irish-ordinary-prescribed-prose-archive']);
    expect(map.q.some((q: { n: string }) => q.n.includes('--'))).toBe(false);
    expect(topicsFor('F-3A-b-i-a')).toEqual(['irish-ordinary-prescribed-poetry-archive']);
    expect(topicsFor('P-2B-b')).toEqual(['irish-ordinary-write-about-a-studied-prose-optional']);
    expect(topicsFor('F-3B-c')).toEqual(['irish-ordinary-write-about-a-studied-poem-optional']);
  });

  it('rejects unknown and stale raw selection directives', () => {
    const result = execFileSync('python3', ['-c', String.raw`
import sys,json
sys.path.insert(0,'scripts/markbank/authoring')
from irish_ordinary_2026_p2 import selection_decisions
review=json.load(sys.stdin)
class Page:
 def __init__(self,text): self.text=text
 def get_text(self): return self.text
pages=[Page('') for _ in range(16)]
for d in review['selectionDecisions']: pages[d['page']-1].text+=d['raw']+'\n'
assert len(selection_decisions(pages))==len(review['selectionDecisions'])
original=pages[12].text
for edited in [original+'\nFreagair do rogha trí cinn as (a), (b) nó (c) thíos.\n',original.replace('dhá cheann as (a), (b) nó (c) thíos.','dhá cheann as (a) nó (b) thíos.')]:
 pages[12].text=edited
 try: selection_decisions(pages)
 except AssertionError: pass
 else: raise AssertionError('Accepted an unknown/stale directive')
print('source guard passed')
`], { encoding: 'utf8', input: JSON.stringify(sourceReview) });
    expect(result).toContain('source guard passed');
  });

  it('records the visual sweep and reconciles the component without claiming archive completion', () => {
    expect(authored.review.reviewedPaperPages).toEqual(Array.from({ length: 16 }, (_, i) => i + 1));
    expect(authored.review.reviewedSchemePages).toEqual(Array.from({ length: 21 }, (_, i) => i + 14));
    expect(authored.review.examStructure).toEqual({ readingA: 50, readingB: 50, prose: 50, poetry: 50, total: 200 });
    const row = inventory.papers.find(p => p.key === '2026|ordinary|LC001GLP200IV.pdf')!;
    expect(row.markBankCardIds.slice().sort()).toEqual(cards.map(c => c.id).sort());
    expect(row).toMatchObject({ fullVisualReview: 'complete', bankAtlasTaskParity: 'complete', partAndSelectionReconciliation: 'complete' });
    expect(inventory.summary.papersPendingFullReview).toBe(62);
    expect(inventory.summary.orphanCardIds).toEqual([]);
  });
});
