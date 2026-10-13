import { describe, expect, it } from 'vitest';
import { readFileSync } from 'node:fs';
import { execFileSync } from 'node:child_process';
import review from '../scripts/markbank/authored/irish-higher-2023-p1-component-review.json';
import sourceReview from '../scripts/markbank/authored/irish-higher-2023-p1-source-review.json';
import inventory from '../scripts/markbank/authored/irish-archive-inventory.json';
import authored from '../components/MarkBank/cards/irish/authored.json';
import { CARDS as HIGHER } from '../components/MarkBank/cards/irish/higher';
import { irishMarks, irishScoreId } from '../components/MarkBank/SessionScreen';
import { examTopicIdsForQuestion, curriculumNodeIdsForExamTopic } from '../data/examTopics/registry';
import { tariffReconciles } from '../types/markBank';

type Authored = (typeof authored.cards)[number] & {
  atlasQuestionId?: string; schemePages?: number[]; reviewedPaperPages?: number[];
};
const cards = HIGHER.filter(c => c.year === 2023 && c.paperFileid === 'LC001ALP100IV');
const source = (authored.cards as Authored[]).filter(c => c.year === 2023 && c.level === 'higher' && c.paper === 1);
const get = (id: string) => source.find(c => c.id === `irish-2023-hl-p1-${id}`)!;
const guide = (id: string) => get(id).criteria.map(c => c.guidance.join(' ')).join(' ');
const AUDIO = 'https://www.examinations.ie/archive/exampapers/2023/LC001ZLP017IV.mp3';

describe('2023 Higher Paper 1 source reconciliation (retained legacy cards)', () => {
  it('keeps the 17 legacy IDs and marks all 25 printed listening questions at their own tariffs', () => {
    expect(cards.map(c => c.id).sort()).toEqual([...review.cardIds].sort());
    expect(cards).toHaveLength(17);
    for (const card of cards) expect(tariffReconciles(card), card.id).toBe(true);
    const segments = review.listeningSegmentCardIds.map(id => source.find(c => c.id === id)!);
    expect(segments.map(c => [c.atlasQuestionId, c.totalMarks, c.criteria.map(r => [r.label, r.maxMarks])])).toEqual([
      ['L-A-F1', 10, [['Ceist 1(a)', 2], ['Ceist 1(b)', 2], ['Ceist 2', 2], ['Ceist 3', 4]]],
      ['L-A-F2', 8, [['Ceist 1', 2], ['Ceist 2', 4], ['Ceist 3', 2]]],
      ['L-B-C1-M1', 8, [['Ceist 1', 2], ['Ceist 2', 4], ['Ceist 3', 2]]],
      ['L-B-C1-M2', 6, [['Ceist 1', 2], ['Ceist 2', 2], ['Ceist 3', 2]]],
      ['L-B-C2-M1', 8, [['Ceist 1', 2], ['Ceist 2', 4], ['Ceist 3', 2]]],
      ['L-B-C2-M2', 6, [['Ceist 1', 2], ['Ceist 2', 2], ['Ceist 3', 2]]],
      ['L-C-P1', 8, [['Ceist 1', 2], ['Ceist 2', 2], ['Ceist 3', 4]]],
      ['L-C-P2', 6, [['Ceist 1', 2], ['Ceist 2', 2], ['Ceist 3', 2]]],
    ]);
    expect(segments.reduce((sum, c) => sum + c.totalMarks, 0)).toBe(60);
    expect(review.printedListeningQuestions).toBe(25);
    for (const card of segments) {
      for (const c of card.criteria.filter(r => r.maxMarks === 4)) expect(c.guidance.join(' '), card.id).toContain('2 mharc + 2 mharc');
      expect(card.markingGuideNote).toContain('Bainfear ó 0 go 3 ar chaighdeán na Gaeilge');
      expect(card.audioMaterial).toMatchObject({ playbackUrl: AUDIO, canonicalUrl: AUDIO });
    }
    // Printed partial answers allow 1; a question with only full-mark answers stays 0/2.
    expect(get('listening-a-f1').criteria.map(c => c.permittedMarks)).toEqual([[0, 2], [0, 1, 2], [0, 2], [0, 2, 4]]);
    expect(guide('listening-a-f1')).toContain('Gaelchultúr = 2 mharc');
    // Scheme PDF 7 stores its annotation-symbol table after Fógra a hAon Q3; it is not part of that key.
    expect(guide('listening-a-f1')).toMatch(/Seoladh ríomhphoist = 2 mharc$/);
    for (const card of segments) expect(card.criteria.map(c => c.guidance.join(' ')).join(' '), card.id).not.toMatch(/Siombailí|Anótála|Tic bán/);
    expect(get('listening-c-p2').criteria.map(c => c.permittedMarks)).toEqual([[0, 2], [0, 2], [0, 1, 2]]);
    // The Píosa a Dó key stops at the listening language note; no composition text follows it.
    expect(guide('listening-c-p2')).not.toContain('Roinn ar an bpáipéar');
    expect(guide('listening-c-p2')).toContain('(Obair) in aghaidh an chiníochais = 2 mharc');
    expect(guide('listening-b-c1-second')).toContain('An bruscar a bhí (fágtha) san áit = 1 mharc');
    const scores = Object.fromEntries(get('listening-a-f1').criteria.map(c => [irishScoreId(c.id), c.maxMarks]));
    const runtime = cards.find(c => c.id === 'irish-2023-hl-p1-listening-a-f1')!;
    expect(irishMarks(runtime, scores)).toBe(10);
  });

  it('lifts the 2023 composition scheme, including where S4 applies', () => {
    const titles = review.compositionRouteCardIds.map(id => source.find(c => c.id === id)!);
    expect(titles.map(c => c.atlasQuestionId)).toEqual(['W-A-a', 'W-A-b', 'W-A-c', 'W-A-d', 'W-A-e', 'W-B-a', 'W-B-b', 'W-C-a', 'W-C-b']);
    for (const card of titles) {
      expect(card.criteria.map(c => [c.id, c.maxMarks])).toEqual([['stil', 5], ['abhar', 15], ['gaeilge', 80]]);
      expect(card.schemePages).toEqual([12, 13, 14, 15, 16, 17]);
      const text = card.criteria.map(c => c.guidance.join(' ')).join(' ');
      for (const fragment of ['B (a), ní mór don iarrthóir Scéal', '13, 14, 15', '76-80 marc', '0-7 marc', 'S1', 'Gaeilge (68)']) {
        expect(text, card.id).toContain(fragment);
      }
      expect(card.questionText).toContain('Freagair do rogha CEANN AMHÁIN de A, B nó C anseo thíos.');
    }
    const s4 = titles.filter(c => c.criteria[2].guidance.some(g => g.startsWith('S4 applies to this title')));
    expect(s4.map(c => c.atlasQuestionId)).toEqual(['W-A-c', 'W-A-e']);
    expect(get('composition-c-b').questionText).toContain('An dea-obair a dhéanann cumainn charthanachta.');
    expect(get('composition-b-b').questionText).toContain('Níl aon tinteán mar do thinteán féin.');
    expect(get('composition-c-a').questionText).toContain('An rogha don chárta seo: C(a).');
  });

  it('joins every retained card to Atlas with its paper page, scheme pages and same-level topic', () => {
    const map = JSON.parse(readFileSync('public/paper-answers/2023/LC001ALP100IV.pdf.json', 'utf8'));
    const q = (n: string) => map.q.find((q: { n: string }) => q.n === n);
    expect(map.schemeFileid).toBe('LC001ALP000IV.pdf');
    for (const c of source) {
      const n = c.atlasQuestionId!;
      const topics = examTopicIdsForQuestion('irish', 'higher', 2023, 'main', n, 'p1', 'iv', 'LC001ALP100IV.pdf');
      expect(topics.flatMap(curriculumNodeIdsForExamTopic), c.id).toContain(c.topicId);
      expect(q(n).paperRegion.map((r: { p: number }) => r.p), c.id).toEqual(c.reviewedPaperPages);
      expect(q(n).region.map((r: { p: number }) => r.p), c.id).toEqual(c.schemePages);
      expect(c.sourceMaterial?.pages, c.id).toEqual(c.reviewedPaperPages);
    }
    for (const n of ['1', '2', '3', '4']) expect(q(n), n).toBeDefined();
    expect(examTopicIdsForQuestion('irish', 'higher', 2023, 'main', 'L-B-C1-M2', 'p1', 'iv', 'LC001ALP100IV.pdf'))
      .toEqual(['irish-higher-aural-comhra-conversation']);
  });

  it('rejects unknown and stale raw selection directives', () => {
    const result = execFileSync('python3', ['-c', String.raw`
import sys,json
sys.path.insert(0,'scripts/markbank/authoring')
from irish_higher_2023_p1 import selection_decisions
review=json.load(sys.stdin)
class Page:
 def __init__(self,text): self.text=text
 def get_text(self): return self.text
pages=[Page('') for _ in range(20)]
for d in review['selectionDecisions']: pages[d['page']-1].text+=d['raw']+'\n'
assert len(selection_decisions(pages))==len(review['selectionDecisions'])
original=pages[6].text
for edited in [original+'\nFreagair do rogha DHÁ CHEANN de A, B nó C anseo thíos.\n',original.replace('CEANN AMHÁIN de A, B nó C','CEANN AMHÁIN de A nó B')]:
 pages[6].text=edited
 try: selection_decisions(pages)
 except AssertionError: pass
 else: raise AssertionError('Accepted an unknown/stale directive')
print('source guard passed')
`], { encoding: 'utf8', input: JSON.stringify(sourceReview) });
    expect(result).toContain('source guard passed');
    // The 2023 scan catches every "dhá" count line, including those the 2024 pattern missed.
    const raws = sourceReview.selectionDecisions.map(d => d.raw);
    expect(raws).toContain('3. Scríobh síos dhá mhír eolais atá le líonadh isteach ar an bhfoirm chlárúcháin ar líne.');
    expect(raws).toContain('Cloisfidh tú dhá fhógra raidió sa chuid seo. Cloisfidh tú gach fógra díobh faoi dhó. Beidh sos');
    expect(sourceReview.sourceFindings.join(' ')).toContain('COVID-19');
  });

  it('records the visual sweep and reconciles the component without claiming archive completion', () => {
    expect(review.reviewedPaperPages).toEqual(Array.from({ length: 20 }, (_, i) => i + 1));
    expect(review.reviewedSchemePages).toEqual([...Array.from({ length: 17 }, (_, i) => i + 1), 50]);
    expect(review.examStructure).toEqual({ listening: 60, composition: 100, total: 160 });
    const row = inventory.papers.find(p => p.key === '2023|higher|LC001ALP100IV.pdf')!;
    expect(row.markBankCardIds.slice().sort()).toEqual([...review.cardIds].sort());
    expect(row).toMatchObject({ fullVisualReview: 'complete', bankAtlasTaskParity: 'complete', partAndSelectionReconciliation: 'complete' });
    expect(inventory.summary.papersPendingFullReview).toBe(58);
    expect(inventory.summary.orphanCardIds).toEqual([]);
  });
});
