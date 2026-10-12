import { describe, expect, it } from 'vitest';
import { readFileSync } from 'node:fs';
import { execFileSync } from 'node:child_process';
import added from '../components/MarkBank/cards/irish/ordinary-2025-p2-authored.json';
import authored from '../components/MarkBank/cards/irish/authored.json';
import sourceReview from '../scripts/markbank/authored/irish-ordinary-2025-p2-source-review.json';
import inventory from '../scripts/markbank/authored/irish-archive-inventory.json';
import { CARDS as ORDINARY } from '../components/MarkBank/cards/irish/ordinary';
import { irishMarks, irishScoreId } from '../components/MarkBank/SessionScreen';
import { examTopicIdsForQuestion, curriculumNodeIdsForExamTopic } from '../data/examTopics/registry';
import { tariffReconciles } from '../types/markBank';

type Card = { id: string; atlasQuestionId?: string; totalMarks: number; topicId: string; schemePages?: number[];
  reviewedPaperPages?: number[]; taskRequirements: string[]; schemeFileid?: string;
  criteria: { id: string; maxMarks: number; permittedMarks: number[]; guidance: string[]; kind: string }[];
  markingGuideNote: string; questionText: string };
const cards = ORDINARY.filter(c => c.year === 2025 && c.paperFileid === 'LC001GLP200IV');
const legacy = (authored.cards as unknown as (Card & { year: number; level: string; paper: number })[])
  .filter(c => c.year === 2025 && c.level === 'ordinary' && c.paper === 2);
const all = [...legacy, ...(added.cards as unknown as Card[])];
const get = (n: string) => all.find(c => c.atlasQuestionId === n)!;
const guide = (n: string) => get(n).criteria.map(c => c.guidance.join(' ')).join(' ');
const topicsFor = (n: string) => examTopicIdsForQuestion('irish', 'ordinary', 2025, 'main', n, 'p2', 'iv', 'LC001GLP200IV.pdf');
const routes = () => legacy.filter(c => !c.id.includes('-reading-'));

describe('2025 Ordinary Paper 2 source reconciliation (22 retained + 32 added)', () => {
  it('keeps every whole reading question and adds each published part at its own tariff', () => {
    expect(cards).toHaveLength(54);
    expect(new Set(cards.map(c => c.id)).size).toBe(54);
    for (const card of cards) expect(tariffReconciles(card), card.id).toBe(true);
    expect(legacy.map(c => c.id).sort()).toEqual([...added.review.legacyCardIds].sort());
    const wholes = legacy.filter(c => c.id.includes('-reading-'));
    expect(wholes.map(c => [c.atlasQuestionId, c.totalMarks])).toEqual(Array.from({ length: 10 }, (_, i) => [String(i + 1), 10]));
    for (const c of wholes) expect(c.criteria.map(r => [r.id, r.maxMarks]), c.id).toEqual([['a', 5], ['b', 5]]);
    const parts = added.cards.filter(c => c.atlasQuestionId.startsWith('R-'));
    expect(parts).toHaveLength(20);
    for (const c of parts) {
      expect(c.totalMarks, c.id).toBe(5);
      expect(c.sourceMaterial.pages, c.id).toEqual(c.atlasQuestionId.startsWith('R-A') ? [4, 5] : [6, 7]);
      expect(c.schemePages.every(p => p >= 15 && p <= 18), c.id).toBe(true);
    }
  });

  it('keeps 3 + 2 items whole and allows only the printed mark values', () => {
    // “3 mharc + 2 mharc”: first correct point 3, second 2.
    for (const n of ['R-A-2-a', 'R-A-2-b', 'R-A-3-b', 'R-B-1-b', 'R-B-2-b', 'R-B-3-a', 'R-B-3-b', 'R-B-4-a', 'R-B-4-b', 'R-B-5-a', 'R-B-5-b']) {
      expect(get(n).criteria[0].permittedMarks, n).toEqual([0, 3, 5]);
      expect(guide(n), n).toContain('3 mharc + 2 mharc = 5 mharc');
    }
    // A single answer with a printed partial (“= 3 mharc”).
    for (const n of ['R-A-1-b', 'R-A-4-b', 'R-A-5-b']) expect(get(n).criteria[0].permittedMarks, n).toEqual([0, 3, 5]);
    for (const n of ['R-A-1-a', 'R-A-3-a', 'R-A-4-a', 'R-A-5-a', 'R-B-1-a', 'R-B-2-a']) expect(get(n).criteria[0].permittedMarks, n).toEqual([0, 5]);
    expect(guide('R-A-3-a')).toContain('Is é an chéad Éireannach riamh é a bhuaigh bonn trí huaire as a chéile = 5 mharc');
    expect(guide('R-B-5-a')).toContain('Fanacht siar caoga méadar ó na fianna');
    expect(get('R-A-1-b').questionText).toContain('ar lasadh istigh ann?');
    expect(guide('R-A-1-a')).toContain('Gearrfar pionós i ngeall ar iomarcaíocht');
    expect(get('1').markingGuideNote).toContain('[Gaeilge lochtach: 0 - 5 a bhaint den iomlán a gnóthaíodh]');
  });

  it('lifts the literature scheme onto the twelve retained options with one 0–4 Gaeilge deduction each', () => {
    expect(routes().map(c => [c.atlasQuestionId, c.totalMarks, c.criteria.map(r => [r.id, r.maxMarks])])).toEqual([
      ['P-2A-a', 25, [['eolas', 25], ['gaeilge-deduction', 4]]], ['P-2A-b', 25, [['eolas', 25], ['gaeilge-deduction', 4]]],
      ['P-2A-c', 25, [['eolas', 25], ['gaeilge-deduction', 4]]],
      ['P-2B-a', 25, [['eolas', 23], ['teideal', 2], ['gaeilge-deduction', 4]]],
      ['P-2B-b', 25, [['priomhphearsa', 1], ['eolas', 22], ['teideal', 2], ['gaeilge-deduction', 4]]],
      ['P-2B-c', 25, [['priomhthema', 1], ['eolas', 22], ['teideal', 2], ['gaeilge-deduction', 4]]],
      ...['a', 'b', 'c'].map(l => [`F-3A-${l}`, 25, [['eolas-i', 8], ['eolas-ii', 8], ['eolas-iii', 9], ['gaeilge-deduction', 4]]]),
      ...['a', 'b', 'c'].map(l => [`F-3B-${l}`, 25, [['eolas-i', 9], ['eolas-ii', 7], ['eolas-iii', 7], ['teideal', 2], ['gaeilge-deduction', 4]]]),
    ]);
    for (const c of routes()) {
      const language = c.criteria.at(-1)!;
      expect(language).toMatchObject({ kind: 'deduction', maxMarks: 4 });
      expect(language.guidance[0], c.id).toContain('[Gaeilge lochtach: 0-4 a bhaint den iomlán a gnóthaíodh]');
      for (const r of c.criteria.slice(0, -1)) expect(r.guidance.join(' '), c.id).not.toContain('Gaeilge lochtach');
      expect(c.schemeFileid, c.id).toBe('LC001GLP000IV');
    }
    expect(guide('P-2A-a')).toContain('5 phointe eolais agus 5 mharc ar gach pointe eolais');
    expect(guide('P-2A-b')).toContain('Pósadh Niamh Chinn Óir agus Oisín');
    expect(guide('P-2A-c')).toContain('Ascaill na Fuinseoige');
    // The scheme text layer splits “ceann”; the card carries the printed word.
    expect(guide('P-2B-a')).toContain('5 mharc an ceann ar an gcéad trí phointe eolais');
    expect(guide('P-2B-a')).not.toContain('cea nn');
    expect(get('P-2B-b').criteria.find(r => r.id === 'teideal')!.permittedMarks).toEqual([0, 2]);
    expect(get('P-2B-a').criteria.find(r => r.id === 'teideal')!.permittedMarks).toEqual([0, 1, 2]);
    expect(get('P-2B-c').criteria.find(r => r.id === 'priomhthema')!.permittedMarks).toEqual([0, 1]);
    expect(get('F-3A-a').criteria[0].permittedMarks).toEqual([0, 2, 4, 6, 8]);
    expect(guide('F-3A-b')).toContain('Tá cliabh/ciseán ar a dhroim aige');
    expect(guide('F-3A-c')).toContain('Is maith/Ní maith = 1 mharc');
    expect(guide('F-3B-c')).toContain('Dhá phríomhsmaoineamh = 5 mharc + 4 mharc');
    const route = cards.find(c => c.id === 'irish-2025-ol-p2-poetry-3a-b')!;
    if (route.rubric.system !== 'irish') throw new Error('Wrong rubric');
    const full = Object.fromEntries(route.rubric.criteria.map(c => [irishScoreId(c.id), c.kind === 'award' ? c.maxMarks : 0]));
    expect(irishMarks(route, full)).toBe(25);
    expect(irishMarks(route, { ...full, [irishScoreId('gaeilge-deduction')]: 4 })).toBe(21);
  });

  it('adds every prescribed-poetry sub-question and the three printed 3A(a)(i) questions', () => {
    const subs = added.cards.filter(c => c.atlasQuestionId.startsWith('F-'));
    expect(subs.map(c => [c.atlasQuestionId, c.totalMarks, c.topicId])).toEqual([
      ['F-3A-a-i', 8, 'irish-5-4'], ['F-3A-a-i-a', 2, 'irish-5-4'], ['F-3A-a-i-b', 2, 'irish-5-4'], ['F-3A-a-i-c', 4, 'irish-5-4'],
      ['F-3A-a-ii', 8, 'irish-5-4'], ['F-3A-a-iii', 9, 'irish-5-4'],
      ['F-3A-b-i', 8, 'irish-5-3'], ['F-3A-b-ii', 8, 'irish-5-3'], ['F-3A-b-iii', 9, 'irish-5-3'],
      ['F-3A-c-i', 8, 'irish-5-5'], ['F-3A-c-ii', 8, 'irish-5-5'], ['F-3A-c-iii', 9, 'irish-5-5'],
    ]);
    expect(get('F-3A-a-i-a').criteria[0].permittedMarks).toEqual([0, 2]);
    expect(get('F-3A-a-i-c').criteria[0].permittedMarks).toEqual([0, 2, 4]);
    expect(guide('F-3A-a-i-a')).toContain('bláth na n-airní');
    expect(guide('F-3A-a-i-b')).not.toContain('bláth na n-airní');
    for (const c of subs) expect(c.criteria.every(r => r.kind === 'award'), c.id).toBe(true);
  });

  it('carries the printed choose-two instruction on every option and never combines two options', () => {
    for (const c of [...routes(), ...added.cards.filter(c => c.atlasQuestionId.startsWith('F-'))]) {
      expect(c.taskRequirements[0], c.atlasQuestionId).toMatch(/^Freagair do rogha dhá cheann as \(a\), \(b\) nó \(c\)( thíos)?\.$/);
    }
    expect(get('F-3B-a').taskRequirements).toContain('Níl cead an dán roghnach céanna a úsáid faoi dhó sna freagraí ar (a), (b) nó (c) thíos.');
    expect(get('P-2B-b').taskRequirements).toContain('Níl cead aon ábhar a bhaineann le Prós Ainmnithe a úsáid sna freagraí ar an bPrós Roghnach.');
    expect(all.filter(c => /--|\+/.test(c.atlasQuestionId ?? ''))).toEqual([]);
    expect(added.review.choicePolicy).toContain('Choice is not a route');
  });

  it('joins all 54 cards to Atlas with paper pages, scheme pages and same-level topics', () => {
    const map = JSON.parse(readFileSync('public/paper-answers/2025/LC001GLP200IV.pdf.json', 'utf8'));
    const q = (n: string) => map.q.find((q: { n: string }) => q.n === n);
    expect(map.schemeFileid).toBe('LC001GLP000IV.pdf');
    for (const c of all) {
      const n = c.atlasQuestionId!;
      expect(topicsFor(n).flatMap(curriculumNodeIdsForExamTopic), c.id).toContain(c.topicId);
      expect(q(n).paperRegion.map((r: { p: number }) => r.p), c.id).toEqual(c.reviewedPaperPages);
      expect((q(n).schemeRegion ?? q(n).region).map((r: { p: number }) => r.p), c.id).toEqual(c.schemePages);
    }
    expect(topicsFor('R-A-1-a')).toEqual(['irish-ordinary-reading-comprehension']);
    expect(topicsFor('P-2A-b')).toEqual(['irish-ordinary-prescribed-prose-archive']);
    expect(topicsFor('F-3A-a-i-c')).toEqual(['irish-ordinary-prescribed-poetry-archive']);
    expect(topicsFor('P-2B-b')).toEqual(['irish-ordinary-write-about-a-studied-prose-optional']);
    expect(topicsFor('F-3B-c')).toEqual(['irish-ordinary-write-about-a-studied-poem-optional']);
  });

  it('rejects unknown and stale raw selection directives', () => {
    const result = execFileSync('python3', ['-c', String.raw`
import sys,json
sys.path.insert(0,'scripts/markbank/authoring')
from irish_ordinary_2025_p2 import selection_decisions
review=json.load(sys.stdin)
class Page:
 def __init__(self,text): self.text=text
 def get_text(self): return self.text
pages=[Page('') for _ in range(16)]
for d in review['selectionDecisions']: pages[d['page']-1].text+=d['raw']+'\n'
assert len(selection_decisions(pages))==len(review['selectionDecisions'])
original=pages[12].text
for edited in [original+'\nFreagair do rogha ceann amháin as (a), (b) nó (c).\n',original.replace('dhá cheann as (a), (b) nó (c) thíos','dhá cheann as (a) nó (b) thíos')]:
 pages[12].text=edited
 try: selection_decisions(pages)
 except AssertionError: pass
 else: raise AssertionError('Accepted an unknown/stale directive')
print('source guard passed')
`], { encoding: 'utf8', input: JSON.stringify(sourceReview) });
    expect(result).toContain('source guard passed');
  });

  it('records the visual sweep and reconciles the component without claiming archive completion', () => {
    expect(added.review.reviewedPaperPages).toEqual(Array.from({ length: 16 }, (_, i) => i + 1));
    expect(added.review.reviewedSchemePages).toEqual(Array.from({ length: 17 }, (_, i) => i + 14));
    expect(added.review.examStructure).toEqual({ readingA: 50, readingB: 50, prose: 50, poetry: 50, total: 200 });
    const row = inventory.papers.find(p => p.key === '2025|ordinary|LC001GLP200IV.pdf')!;
    expect(row.markBankCardIds.slice().sort()).toEqual(cards.map(c => c.id).sort());
    expect(row).toMatchObject({ fullVisualReview: 'complete', bankAtlasTaskParity: 'complete', partAndSelectionReconciliation: 'complete' });
    expect(inventory.summary.papersPendingFullReview).toBe(63);
    expect(inventory.summary.orphanCardIds).toEqual([]);
  });
});
