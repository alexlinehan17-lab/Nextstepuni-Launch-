import { describe, expect, it } from 'vitest';
import { CARDS } from '../components/MarkBank/cards/lcvp/common';
import { tariffReconciles } from '../types/markBank';
import authored from '../scripts/markbank/authored/lcvp.json';
import review from '../scripts/markbank/authoring/lcvp/2018-cl-main-review.json';
import anchors from '../scripts/paper-trail/answers/2018/LC462CLP000EV.pdf.json';
import local from '../data/examTopics/link-modules-local-crosswalk.json';
import { PAPER_TOPIC_TAGS } from '../data/paperTrail/topicTags';
import { browseTopicIdsForQuestion } from '../components/PaperTrail/topics';
import { curriculumNodeIdsForExamTopic } from '../data/examTopics/registry';

const all = CARDS.filter(c => c.id.startsWith('lcvp-2018-cl-'));
const get = (suffix: string) => {
  const card = all.find(c => c.id === `lcvp-2018-cl-${suffix}`);
  if (!card || card.kind !== 'question') throw new Error(suffix);
  return card;
};

describe('LCVP 2018: full source tasks, preserved identities and marketing allocation hold', () => {
  it('reconciles 43 printed leaves to 40 tasks while preserving every existing identity and full emitted content', () => {
    expect(review.manualOriginalLeaves).toBe(43);
    expect(review.manualSectionLeaves).toEqual({ A: 8, B: 8, C: 27 });
    expect(review.manualPricedTasks).toBe(40);
    expect(review.manualSectionTasks).toEqual({ A: 8, B: 5, C: 27 });
    expect(review.rawCensusClassification.rawLeaves).toBe(43);
    expect(review.candidateWrittenMarks).toBe(160);
    expect(all).toHaveLength(40);
    expect(all.reduce((sum, c) => sum + c.totalMarks, 0)).toBe(210);
    expect(review.legacyAudit.originalIds).toHaveLength(32);
    for (const id of review.legacyAudit.originalIds) expect(all.some(c => c.id === id), id).toBe(true);
    expect(['b3i', 'c1c', 'c2a', 'c2bii', 'c2d', 'c4aii', 'c6b', 'c6d'].map(s => get(s).totalMarks)).toEqual([6, 8, 3, 3, 8, 3, 6, 8]);
    const expected = authored.filter(c => c.year === 2018);
    expect(all.map(c => c.id).sort()).toEqual(expected.map(c => c.id).sort());
    for (const source of expected) {
      const emitted = get(source.id.replace('lcvp-2018-cl-', ''));
      expect(tariffReconciles(emitted), source.id).toBe(true);
      expect(emitted.questionText, source.id).toBe(source.questionText);
      expect(`${emitted.questionText} ${emitted.stem ?? ''}`, source.id).not.toMatch(/\bExaminer\b|\bpage running\b|\bonly\b/);
      expect(emitted.stem ?? '', source.id).toBe(source.stem ?? '');
      expect(emitted.rows, source.id).toEqual(source.rows);
      expect(emitted.tariffModel, source.id).toEqual(source.tariffModel);
      expect(emitted.totalMarks, source.id).toBe(source.totalMarks);
      expect(emitted.conceptId, source.id).toBe(source.conceptId);
      expect(emitted.topicId, source.id).toBe(source.topicId);
      expect(emitted.sourceMaterial, source.id).toEqual(source.sourceMaterial);
      expect(emitted.additionalSourceMaterials, source.id).toEqual(source.additionalSourceMaterials);
      expect(emitted.videoMaterial, source.id).toEqual(source.videoMaterial);
    }
  });

  it('keeps all eight original video tasks, binary steps and both components of A8', () => {
    const video = get('a1').videoMaterial;
    expect(video?.canonicalUrl).toBe('https://www.examinations.ie/archive/exampapers/2018/LC462CLP031EV.mp4');
    for (const c of all.filter(c => c.id.startsWith('lcvp-2018-cl-a'))) {
      if (c.kind !== 'question') throw new Error(c.id);
      expect(c.videoMaterial).toEqual(video);
      expect(c.audioMaterial).toBeUndefined();
      expect(c.additionalSourceMaterials?.[0].pages).toEqual([3]);
    }
    expect(get('a2').rows[0].group?.options).toEqual(['Price', 'Promotion', 'Place']);
    expect(get('a4').rows[0].group).toMatchObject({ claimMax: 2, perOption: 2 });
    expect(get('a4').rows[0].group?.options).toHaveLength(3);
    expect(get('a8').rows.map(r => r.marks)).toEqual([2, 4]);
    expect(get('a8').rows[0].group?.options).toHaveLength(2);
    expect(get('a8').rows[1].parts?.map(p => p.permittedMarks)).toEqual([[0, 1, 2], [0, 1, 2]]);
    expect(get('a8').rows[1].contextNote).toContain('creating hyperlinks');
    expect(get('a8').questionText).toContain('How can he ensure that IT development continues to be beneficial?');
  });

  it('retains the whole volunteering case, choice definitions and flexible compare/contrast minima', () => {
    expect(get('b1').stem).toContain('VOLUNTEERING');
    expect(get('b1').stem).toContain('Tommy');
    expect(get('b1').stem).toContain('Sarah');
    expect(get('b1').stem).toContain('success of volunteer agencies in Ireland');
    expect(get('b1').sourceMaterial?.pages).toEqual([9]);
    expect(get('b1').rows[0].group).toMatchObject({ claimMax: 3, perOption: 2 });
    expect(get('b1').rows[0].group?.options).toHaveLength(4);
    expect(get('b1').questionText).toContain('Corporate Social Responsibility');
    expect(get('b2i').rows.map(r => r.marks)).toEqual([4, 4]);
    expect(get('b2i').rows.map(r => r.group?.options.length)).toEqual([6, 6]);
    expect(get('b2ii').rows[0].group?.options).toHaveLength(9);
    expect(get('b3i').rows.map(r => r.marks)).toEqual([2, 2, 2]);
    for (const row of get('b3i').rows) {
      expect(row.parts?.map(p => p.permittedMarks)).toEqual([[0, 1], [0, 1]]);
      expect(row.group).toBeUndefined();
    }
    expect(get('b3i').rows[0].contextNote).toContain('A minimum of 2 in each area');
    expect(get('b3i').rows[0].contextNote).toContain('credited only once');
    expect(get('b3i').rows[2].contextNote).toContain('2+4, 3+3 or 4+2');
    expect(get('b3ii').rows[0].group).toMatchObject({ claimMax: 3, perOption: 2 });
    expect(get('b3ii').rows[0].group?.options).toHaveLength(8);
  });

  it('preserves both original roman IDs, parent instructions, complete agency profiles and all three required enterprise headings', () => {
    expect(get('c1a').rows[0].parts?.map(p => p.permittedMarks)).toEqual([[0, 2], [0, 2]]);
    for (const suffix of ['c1bi', 'c1bii']) {
      expect(get(suffix).totalMarks).toBe(2);
      expect(get(suffix).stem).toContain('Describe two examples of enterprise in action in each of the following.');
      expect(get(suffix).sourceMaterial?.pages).toEqual([16]);
    }
    expect(get('c1bi').conceptId).toBe('household');
    expect(get('c1bii').conceptId).toBe('local-community');
    expect(get('c1bi').rows[0].group?.options).toHaveLength(6);
    expect(get('c1bii').rows[0].group?.options).toHaveLength(5);
    expect(get('c1c').rows).toHaveLength(2);
    for (const row of get('c1c').rows) expect(row.parts?.map(p => p.marks)).toEqual([1, 3]);
    for (const name of ['Local Enterprise Office/LEO/CEB', 'Enterprise Ireland', 'Local Area Partnerships', 'ETB’s/SOLAS/FAS', 'Leader Plus', 'Teagasc', 'Udaras Na Gaeltacha', 'Failte Ireland', 'IDA Ireland', 'Intertrade Ireland', 'Bord Bia', 'Glas']) expect(get('c1c').rows[0].contextNote).toContain(name);
    expect(get('c1d').rows.map(r => r.marks)).toEqual([3, 3, 3]);
    expect(get('c1d').rows.map(r => r.group?.options.length)).toEqual([8, 8, 4]);
  });

  it('keeps the unequal advantages tariff, same-profession routes and complete contextual SWOT requirements', () => {
    expect(get('c2a').rows.map(r => r.marks)).toEqual([1, 2]);
    expect(get('c2bii').rows[0].group?.perOptionSteps).toEqual([2, 1]);
    expect(get('c2bii').rows[0].group?.options).toHaveLength(5);
    expect(get('c2bii').rows[0].contextNote).toContain('ONE of the methods');
    expect(get('c2bii').stem).toContain(get('c2bi').questionText);
    expect(get('c2d').rows.map(r => r.marks)).toEqual([4, 4]);
    expect(get('c2d').rows[1].verbatim).toContain('2 routes to same profession');
    expect(get('c3b').rows.map(r => r.marks)).toEqual([2, 2, 2, 2]);
    for (const row of get('c3b').rows) expect(row.parts?.map(p => p.permittedMarks)).toEqual([[0, 1], [0, 1]]);
    for (const note of ['1 specific point to tidy towns', 'No marks for headings', 'No repetition of points']) expect(get('c3b').rows[0].contextNote).toContain(note);
    expect(get('c3b').stem).toContain('Tidy Towns');
  });

  it('retains historical union models, both industrial-relations components and the exact six-part marketing definition', () => {
    expect(get('c4ai').rows[0].group?.options).toHaveLength(8);
    expect(get('c4ai').rows[0].group?.options[7]).toBe('FORÁS');
    expect(get('c4aii').rows.map(r => r.marks)).toEqual([3]);
    expect(get('c4c').rows.map(r => r.marks)).toEqual([3, 3]);
    expect(get('c4c').rows.map(r => r.group?.options.length)).toEqual([6, 7]);
    expect(get('c5a').rows[0].group).toMatchObject({ claimMax: 2, perOption: 2 });
    expect(get('c5a').stem).toBe('You are part of your LCVP class committee to plan upcoming activities.');
    expect(get('c6b').rows.map(r => r.verbatim)).toEqual(['A combination of', 'Product', 'Price', 'Place', 'Promotion', 'to achieve goals, sell a product/service']);
    expect(get('c6b').rows.map(r => r.marks)).toEqual([1, 1, 1, 1, 1, 1]);
    expect(get('c6d').rows[0].parts).toHaveLength(4);
  });

  it('holds the whole marketing report with every heading and no invented choose-four scoring', () => {
    expect(all.filter(c => c.kind === 'question' && c.tariffModel.kind === 'questionTotal').map(c => c.id)).toEqual(['lcvp-2018-cl-c6c']);
    const card = get('c6c');
    expect(card.totalMarks).toBe(8);
    expect(card.rows.map(r => r.verbatim)).toEqual(['Market research/target market', 'Product/Packaging/USP/design', 'Price', 'Place', 'Promotion']);
    for (const row of card.rows) {
      expect(row.marks).toBeNull();
      expect(row.parts).toBeUndefined();
      expect(row.group).toBeUndefined();
    }
    for (const text of ['2 points under each heading', 'No marks for headings', '4@2(1+1)', 'confidence review only']) expect(card.rows[0].contextNote).toContain(text);
    expect(card.sourceMaterial?.pages).toEqual([32]);
  });

  it('retains all original Atlas identities and restores four missing runtime joins without narrowing canonical topics', () => {
    expect(anchors.q.map(q => q.n)).toEqual(Array.from({ length: 17 }, (_, i) => String(i + 1)));
    expect(anchors.q.slice(11).map(q => [q.pP, q.endP])).toEqual([[16, 18], [19, 21], [22, 24], [25, 27], [28, 30], [31, 33]]);
    expect(anchors.q.find(q => q.n === '10')?.region.map(r => r.p)).toEqual([6, 7]);
    expect(anchors.q.find(q => q.n === '12')?.region.map(r => r.p)).toEqual([9, 10, 11]);
    expect(local.reviewedEnglish2018.markBankMappings).toHaveLength(40);
    expect(Object.keys(local.reviewedEnglish2018.originalAtlasTopicIds)).toHaveLength(13);
    expect(local.reviewedEnglish2018.canonicalTopicIdsByQuestion['12']).toEqual(['lcvp-link-modules-1-0', 'lcvp-link-modules-1-1', 'lcvp-link-modules-1-2']);
    expect(local.reviewedEnglish2018.canonicalTopicIdsByQuestion['13']).toEqual(['lcvp-link-modules-0-0', 'lcvp-link-modules-0-2', 'lcvp-link-modules-0-3']);
    const paper = PAPER_TOPIC_TAGS.find(p => p.subjectId === 'link-modules' && p.year === 2018 && p.lang === 'ev' && p.fileid === 'LC462CLP000EV.pdf')!;
    for (const [n, topics] of Object.entries(local.reviewedEnglish2018.originalAtlasTopicIds)) expect(browseTopicIdsForQuestion(paper, paper.q.find(q => q.n === n)!)).toEqual(expect.arrayContaining(topics));
    for (const mapping of local.reviewedEnglish2018.markBankMappings) {
      const topics = browseTopicIdsForQuestion(paper, paper.q.find(q => q.n === mapping.n)!);
      expect(topics, mapping.id).toEqual(expect.arrayContaining(mapping.atlasTopicIds));
      expect(topics.some(t => curriculumNodeIdsForExamTopic(t).includes(mapping.topicId)), mapping.id).toBe(true);
    }
    for (const n of ['9', '11', '16', '17']) expect(browseTopicIdsForQuestion(paper, paper.q.find(q => q.n === n)!).length).toBeGreaterThan(0);
  });
});
