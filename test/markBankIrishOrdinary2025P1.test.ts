import { describe, expect, it } from 'vitest';
import { readFileSync } from 'node:fs';
import { execFileSync } from 'node:child_process';
import review from '../scripts/markbank/authored/irish-ordinary-2025-p1-component-review.json';
import authored from '../components/MarkBank/cards/irish/authored.json';
import sourceReview from '../scripts/markbank/authored/irish-ordinary-2025-p1-source-review.json';
import inventory from '../scripts/markbank/authored/irish-archive-inventory.json';
import { CARDS as ORDINARY } from '../components/MarkBank/cards/irish/ordinary';
import { listeningQuestionGroups } from '../components/MarkBank/SessionScreen';
import { sessionExerciseCount } from '../components/MarkBank/sessionPlanning';
import { examTopicIdsForQuestion, curriculumNodeIdsForExamTopic } from '../data/examTopics/registry';
import { tariffReconciles } from '../types/markBank';

type Card = { id: string; atlasQuestionId?: string; totalMarks: number; topicId: string; schemePages?: number[]; questionText: string;
  reviewedPaperPages?: number[]; markingGuideNote: string; criteria: { id: string; label: string; maxMarks: number; permittedMarks: number[]; guidance: string[] }[] };
const cards = ORDINARY.filter(c => c.year === 2025 && c.paperFileid === 'LC001GLP100IV');
const legacy = (authored.cards as unknown as (Card & { year: number; level: string; paper: number })[])
  .filter(c => c.year === 2025 && c.level === 'ordinary' && c.paper === 1);
const all = legacy;
const get = (n: string) => all.find(c => c.atlasQuestionId === n)!;
const AUDIO = 'https://www.examinations.ie/archive/exampapers/2025/LC001ZLP017IV.mp3';

describe('2025 Ordinary Paper 1 source reconciliation (15 retained cards)', () => {
  it('marks all 20 printed listening questions at 3 marks inside the six retained segment cards', () => {
    expect(cards).toHaveLength(15);
    for (const card of cards) expect(tariffReconciles(card), card.id).toBe(true);
    expect(legacy.map(c => c.id).sort()).toEqual([...review.cardIds].sort());
    const segments = review.listeningSegmentCardIds.map(id => legacy.find(c => c.id === id)!);
    expect(segments.map(c => [c.atlasQuestionId, c.totalMarks, c.criteria.length])).toEqual([
      ['L-A-F1', 12, 4], ['L-A-F2', 12, 4], ['L-B-C1', 12, 4], ['L-B-C2', 12, 4], ['L-C-P1', 6, 2], ['L-C-P2', 6, 2]]);
    expect(segments.flatMap(c => c.criteria).every(r => r.maxMarks === 3)).toBe(true);
    expect(get('L-B-C1').criteria.map(r => r.label)).toEqual([
      'An Chéad Mhír · Ceist 1', 'An Chéad Mhír · Ceist 2', 'An Dara Mír · Ceist 1', 'An Dara Mír · Ceist 2']);
    // Printed partials only: RTÉ = 1, San ionad = 1, Nócha = 2, Sa chlub = 1, Léargas … = 1.
    expect(get('L-A-F1').criteria.map(r => r.permittedMarks)).toEqual([[0, 1, 3], [0, 3], [0, 3], [0, 3]]);
    expect(get('L-B-C1').criteria.map(r => r.permittedMarks)).toEqual([[0, 1, 3], [0, 3], [0, 3], [0, 2, 3]]);
    expect(get('L-A-F1').criteria[3].guidance[0]).not.toContain('Siombailí Anótála');
    expect(get('L-A-F1').schemePages).toEqual([7]);
    for (const c of segments) {
      expect(c.markingGuideNote).toContain('Bainfear ó 0 go 6 ar chaighdeán na Gaeilge');
      expect((c as unknown as { audioMaterial: object }).audioMaterial).toMatchObject({ playbackUrl: AUDIO, canonicalUrl: AUDIO });
    }
    const listening = cards.filter(c => Boolean(c.audioMaterial));
    expect(sessionExerciseCount(listening)).toBe(3);
    expect(listening.flatMap(c => listeningQuestionGroups(c.questionText).flatMap(g => g.prompts))).toHaveLength(20);
  });

  it('lifts the 2025 composition scheme and keeps the full 0–40 language scale', () => {
    const titles = review.compositionRouteCardIds.map(id => legacy.find(c => c.id === id)!);
    expect(titles.map(c => c.atlasQuestionId)).toEqual(['W-A-i', 'W-A-ii', 'W-A-iii', 'W-B-i', 'W-B-ii', 'W-C-i', 'W-C-ii', 'W-D-i', 'W-D-ii']);
    for (const c of titles) {
      expect(c.criteria.map(r => [r.id, r.maxMarks])).toEqual([['tasc', 2], ['abhar', 8], ['gaeilge', 40]]);
      expect(c.criteria[0].permittedMarks).toEqual([0, 2]);
      expect(c.criteria[2].permittedMarks).toHaveLength(41);
      expect(c.criteria[2].guidance.join(' ')).toContain('38 34 29 19 10');
      expect(c.schemePages).toEqual([10, 11, 12, 13]);
    }
    expect(get('W-C-ii').questionText).toContain('Thit sneachta trom i do cheantar le déanaí.');
    expect(get('W-B-i').questionText).toContain('An rogha don chárta seo: B(i).');
  });

  it('publishes each title once and carries the choose-two instruction, with no combination cards', () => {
    expect(cards.filter(c => / \+ /.test(c.questionRef))).toEqual([]);
    for (const id of review.compositionRouteCardIds) {
      const card = legacy.find(c => c.id === id)! as Card & { taskRequirements: string[] };
      expect(card.taskRequirements[0]).toBe('Freagair do rogha dhá cheann de A, B, C, D anseo.');
      expect(card.totalMarks).toBe(50);
    }
  });

  it('joins all 15 cards to Atlas with pages, audio and writing-form topics', () => {
    const map = JSON.parse(readFileSync('public/paper-answers/2025/LC001GLP100IV.pdf.json', 'utf8'));
    const q = (n: string) => map.q.find((q: { n: string }) => q.n === n);
    expect(map.schemeFileid).toBe('LC001GLP000IV.pdf');
    for (const c of all) {
      const n = c.atlasQuestionId!;
      const topics = examTopicIdsForQuestion('irish', 'ordinary', 2025, 'main', n, 'p1', 'iv', 'LC001GLP100IV.pdf');
      expect(topics.flatMap(curriculumNodeIdsForExamTopic), c.id).toContain(c.topicId);
      expect(q(n).paperRegion.map((r: { p: number }) => r.p), c.id).toEqual(c.reviewedPaperPages);
      expect(q(n).region.map((r: { p: number }) => r.p), c.id).toEqual(c.schemePages);
    }
    for (const n of ['1', '2', '3', '4']) expect(q(n), n).toBeDefined();
    expect(q('L-B-C2').audioMaterial.playbackUrl).toBe(AUDIO);
    expect(examTopicIdsForQuestion('irish', 'ordinary', 2025, 'main', 'W-D-ii', 'p1', 'iv', 'LC001GLP100IV.pdf'))
      .toEqual(['irish-ordinary-write-a-conversation']);
  });

  it('rejects unknown and stale raw selection directives', () => {
    const result = execFileSync('python3', ['-c', String.raw`
import sys,json
sys.path.insert(0,'scripts/markbank/authoring')
from irish_ordinary_2025_p1 import selection_decisions
review=json.load(sys.stdin)
class Page:
 def __init__(self,text): self.text=text
 def get_text(self): return self.text
pages=[Page('') for _ in range(16)]
for d in review['selectionDecisions']: pages[d['page']-1].text+=d['raw']+'\n'
assert len(selection_decisions(pages))==len(review['selectionDecisions'])
original=pages[6].text
for edited in [original+'\nFreagair do rogha trí cinn de A, B, C, D anseo.\n',original.replace('dhá cheann de A, B, C, D','dhá cheann de A, B, C')]:
 pages[6].text=edited
 try: selection_decisions(pages)
 except AssertionError: pass
 else: raise AssertionError('Accepted an unknown/stale directive')
print('source guard passed')
`], { encoding: 'utf8', input: JSON.stringify(sourceReview) });
    expect(result).toContain('source guard passed');
  });

  it('records the visual sweep and reconciles the component without claiming archive completion', () => {
    expect(review.reviewedPaperPages).toEqual(Array.from({ length: 16 }, (_, i) => i + 1));
    expect(review.examStructure).toEqual({ listening: 60, composition: 100, total: 160 });
    const row = inventory.papers.find(p => p.key === '2025|ordinary|LC001GLP100IV.pdf')!;
    expect(row.markBankCardIds.slice().sort()).toEqual(cards.map(c => c.id).sort());
    expect(row).toMatchObject({ fullVisualReview: 'complete', bankAtlasTaskParity: 'complete', partAndSelectionReconciliation: 'complete' });
    expect(inventory.summary.papersPendingFullReview).toBe(61);
    expect(inventory.summary.orphanCardIds).toEqual([]);
  });
});
