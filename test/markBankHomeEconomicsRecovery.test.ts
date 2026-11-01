import { describe, expect, it } from 'vitest';
import { CARDS } from '../components/MarkBank/cards/home-economics/higher';
import { isPointCard, tariffReconciles } from '../types/markBank';
import runtime from '../data/examTopics/home-economics-s-and-s-question-runtime.json';
import crosswalk from '../data/examTopics/home-economics-s-and-s-curriculum-crosswalk.json';
import anchors from '../scripts/paper-trail/answers/2023/LC098ALP039EV.pdf.json';
import { browseTopicIdsForQuestion } from '../components/PaperTrail/topics';
import { PAPER_TOPIC_TAGS } from '../data/paperTrail/topicTags';
import { preferredAnswersUrl } from '../components/PaperTrail/vaultResolve';
import { paperRegionFor, schemeRegionFor } from '../components/PaperTrail/paperRegion';
import type { PaperAnswerMap } from '../types/paperTrail';

const get = (id: string) => {
  const card = CARDS.find(candidate => candidate.id === id);
  expect(card, id).toBeDefined();
  if (!card || !isPointCard(card)) throw new Error(`Missing point card: ${id}`);
  return card;
};

describe('2023 Higher Home Economics recovered tasks', () => {
  it('keeps fish preservation as one open choice with every published process', () => {
    const card = get('he-2023-hl-sb-q2b');
    expect(card.totalMarks).toBe(18);
    expect(card.questionText).toContain('one process');
    expect(card.questionText).toContain('underlying principle');
    expect(card.answerVariants?.map(v => v.label)).toEqual([
      'Freezing', 'Salting/Brining', 'Smoking', 'Canning', 'Vacuum packing', 'Another valid process',
    ]);
    for (const variant of card.answerVariants ?? []) {
      expect(tariffReconciles({ ...card, rows: variant.rows })).toBe(true);
      expect(variant.rows.map(row => row.marks)).toEqual([3, 9, 6]);
      expect(variant.rows[1].parts).toHaveLength(3);
      expect(variant.rows[2].parts).toHaveLength(2);
      for (const row of variant.rows.slice(1)) {
        for (const part of row.parts ?? []) expect(part.permittedMarks).toEqual([0, 2, 3]);
      }
    }
    expect(card.answerVariants?.find(v => v.id === 'canning')?.rows[2].contextNote).toContain('canned in brine');
    expect(card.answerVariants?.find(v => v.id === 'vacuum-packing')?.rows[2].contextNote).toContain('increased salt and/or fat');
  });

  it('retains all six production points and the complete packaging guidance', () => {
    const card = get('he-2023-hl-sb-q3b');
    expect(card.questionText).toMatch(/^Profile an added value food/);
    expect(card.totalMarks).toBe(26);
    expect(card.answerVariants?.map(v => v.id)).toEqual(['cheese', 'margarine', 'another-food']);
    for (const variant of card.answerVariants ?? []) {
      expect(tariffReconciles({ ...card, rows: variant.rows })).toBe(true);
      expect(variant.rows.map(row => row.marks)).toEqual([2, 18, 6]);
      expect(variant.rows[1].parts).toHaveLength(6);
      expect(variant.rows[2].contextNote).toContain('wrapped in foil');
      expect(variant.rows[2].contextNote).toContain('allergen information');
    }
    expect(card.answerVariants?.[0].rows[1].contextNote).toContain('stored in controlled conditions for 3-12 months');
    expect(card.answerVariants?.[1].rows[1].contextNote).toContain('votator');
  });

  it('keeps the career detail criterion and its printed partial credit', () => {
    const card = get('he-2023-hl-sc-q2cii');
    expect(card.totalMarks).toBe(6);
    expect(tariffReconciles(card)).toBe(true);
    expect(card.rows[0].group?.options).toHaveLength(11);
    expect(card.rows[0].group?.claimMax).toBe(1);
    expect(card.rows[1].permittedMarks).toEqual([0, 2, 4]);
    expect(card.rows[1].contextNote).toContain('does not print an example detail answer');
  });

  it('opens Section C Q2 on page 6 and its own scheme pages, never Section B Q2', () => {
    const question = anchors.q.find(q => q.n === '7')!;
    expect(question.label).toBe('Section C · Q2');
    expect(question.pP).toBe(6);
    expect(question.region.map(r => r.p)).toEqual([21, 22]);
    expect(paperRegionFor((anchors as PaperAnswerMap).q, '7')?.map(r => r.p)).toEqual([6]);
    expect(preferredAnswersUrl('home-economics-s-and-s', 2023, 'LC098ALP039EV.pdf', 'stale-storage-url'))
      .toBe('/paper-answers/2023/LC098ALP039EV.pdf.json');
    expect(anchors.q.find(q => q.n === '2')?.pP).toBe(3);
    expect(schemeRegionFor((anchors as PaperAnswerMap).q.find(q => q.n === '5')!).map(r => r.p)).toEqual([17]);
    expect(anchors.q.map(q => q.n)).toEqual(['1', '2', '3', '4', '5', '6', '7', '8', '9']);
  });

  it('places every 2023 Higher B/C Mark Bank card in its own Atlas question and canonical topic', () => {
    const paper = PAPER_TOPIC_TAGS.find(p => p.subjectId === 'home-economics-s-and-s'
      && p.year === 2023 && p.level === 'higher' && p.lang === 'ev' && p.fileid === 'LC098ALP039EV.pdf')!;
    const cards = CARDS.filter(c => /^2023 HL Section [BC] /.test(c.questionRef));
    expect(cards).toHaveLength(43);
    for (const card of cards) {
      const match = card.questionRef.match(/Section ([BC]) (?:E\d )?Q(\d+)/)!;
      const n = String(Number(match[2]) + (match[1] === 'C' ? 5 : 0));
      const question = paper.q.find(q => q.n === n)!;
      const topics = browseTopicIdsForQuestion(paper, question);
      expect(topics.some(t => (crosswalk as Record<string, string[]>)[t]?.includes(card.topicId)), card.id).toBe(true);
    }
    const b2 = runtime.questionMappings.find(q => q[0] === 'h' && q[1] === 'e' && q[2] === 2023
      && q[4] === 'LC098ALP039EV.pdf' && q[5] === '2')!;
    expect((b2[6] as number[]).map(i => runtime.topicIds[i])).not.toContain('home-economics-s-and-s-higher-elective-2-patterns-fashion');
  });
});
