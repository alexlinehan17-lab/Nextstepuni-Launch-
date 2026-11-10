import { describe, expect, it } from 'vitest';
import { CARDS } from '../components/MarkBank/cards/lcvp/common';
import { tariffReconciles } from '../types/markBank';
import review from '../scripts/markbank/authoring/lcvp/2024-cl-main-review.json';
import anchors from '../scripts/paper-trail/answers/2024/LC462CLP000EV.pdf.json';
import local from '../data/examTopics/link-modules-local-crosswalk.json';
import { PAPER_TOPIC_TAGS } from '../data/paperTrail/topicTags';
import { browseTopicIdsForQuestion } from '../components/PaperTrail/topics';
import { curriculumNodeIdsForExamTopic } from '../data/examTopics/registry';

const all = CARDS.filter(c => c.id.startsWith('lcvp-2024-cl-'));
const get = (suffix: string) => {
  const card = all.find(c => c.id === `lcvp-2024-cl-${suffix}`);
  if (!card || card.kind !== 'question') throw new Error(suffix);
  return card;
};

describe('LCVP 2024: complete source tasks and required components', () => {
  it('reconciles 47 reviewed leaves with 45 coherent tasks and restores all six omissions', () => {
    expect(review.manualOriginalLeaves).toBe(47);
    expect(review.manualSectionLeaves).toEqual({ A: 8, B: 6, C: 33 });
    expect(all).toHaveLength(45);
    expect(['a', 'b', 'c'].map(s => all.filter(c => c.id.startsWith(`lcvp-2024-cl-${s}`)).length)).toEqual([8, 6, 31]);
    expect(all.reduce((sum, c) => sum + c.totalMarks, 0)).toBe(235);
    expect(all.map(c => c.id).sort()).toEqual(review.tasks.map(c => c.id).sort());
    expect(['b3iii', 'c1bi', 'c1bii', 'c1ci', 'c2a', 'c6a'].map(s => get(s).totalMarks)).toEqual([4, 4, 2, 2, 4, 4]);
    for (const c of all) {
      if (c.kind !== 'question') throw new Error(c.id);
      expect(tariffReconciles(c), c.id).toBe(true);
      expect(c.tariffModel.kind).toBe('fixed');
      expect(c.questionText + c.stem).not.toMatch(/Leaving Certificate Vocational Programme 2024|Link Modules Examination/);
    }
  });

  it('binds all eight AV tasks to the original video and preserves expanded-response 0/2 rules', () => {
    const video = get('a1').videoMaterial;
    expect(video?.canonicalUrl).toBe('https://www.examinations.ie/archive/exampapers/2024/LC462CLP031EV.mov');
    expect(video?.kind).toBe('source-video');
    for (const c of all.filter(c => c.id.startsWith('lcvp-2024-cl-a'))) {
      if (c.kind !== 'question') throw new Error(c.id);
      expect(c.videoMaterial).toEqual(video);
      expect(c.audioMaterial).toBeUndefined();
      expect(c.additionalSourceMaterials?.[0].pages).toEqual([3]);
    }
    expect(review.media.fullFileDownloaded).toBe(false);
    for (const suffix of ['a6', 'a7']) {
      const row = get(suffix).rows[0];
      expect(row.group?.claimMax).toBe(3);
      expect(row.group?.perOption).toBe(2);
      expect(row.contextNote).toContain('(0/2), expansion needed');
      expect(row.contextNote).toContain('no 1-mark step');
    }
    expect(get('a6').rows[0].group?.options).toHaveLength(7);
    expect(get('a7').rows[0].group?.options).toHaveLength(4);
    expect(get('a5').rows[0].parts?.map(p => p.permittedMarks)).toEqual([[0, 1, 2], [0, 1, 2]]);
  });

  it('keeps both complete business options within one decision task, with matching reasons', () => {
    for (const c of all.filter(c => c.id.startsWith('lcvp-2024-cl-b'))) {
      if (c.kind !== 'question') throw new Error(c.id);
      expect(c.stem).toContain('Sandra');
      expect(c.stem).toContain('Babyboo');
      expect(c.stem).toContain('Zebra');
      expect(c.sourceMaterial?.pages).toEqual([9]);
    }
    const c = get('b3iii');
    expect(c.totalMarks).toBe(4);
    expect(c.rows.map(r => r.marks)).toEqual([1, 3]);
    expect(c.rows[0].contextNote).toContain('ONE of the two');
    expect(c.rows[1].parts?.map(p => p.permittedMarks)).toEqual([[0, 1], [0, 1], [0, 1]]);
    const pools = c.rows[1].contextNote!.split('preserved: ')[1].split(' | ');
    expect(pools).toHaveLength(2);
    expect(pools[0]).toContain('Sell Babyboo to Zebra');
    expect(pools[0]).toContain('€1 million');
    expect(pools[0]).not.toContain('baby products');
    expect(pools[1]).toContain('Expand into the Department store');
    expect(pools[1]).toContain('baby products');
    expect(pools[1]).toContain('established customer base');
  });

  it('retains the complete growth table and the separately priced research and promotion tasks', () => {
    expect(get('c1bi').rows.map(r => r.marks)).toEqual([1, 3]);
    expect(get('c1bi').rows[0].verbatim).toContain('Desk/Secondary');
    expect(get('c1bi').rows[1].parts).toHaveLength(3);
    for (const suffix of ['c1bi', 'c1bii']) {
      expect(get(suffix).sourceMaterial?.pages).toEqual([16]);
      expect(get(suffix).stem).toContain('www.centralbank.ie, 2023');
    }
    expect(get('c1bii').rows[0].permittedMarks).toEqual([0, 1, 2]);
    expect(get('c1bii').rows[0].contextNote).toContain('MUST refer to the table years or percentages');
    expect(get('c1bii').rows[0].verbatim).toContain('Slowdown in the economy');
    expect(get('c1bii').rows[0].verbatim).toContain('Decrease forecasted');
    for (const suffix of ['c1ci', 'c1cii']) expect(get(suffix).stem).toContain('Promotion is one of the 4Ps');
    expect([get('c1ci').totalMarks, get('c1cii').totalMarks]).toEqual([2, 4]);
  });

  it('requires election of officers and matching visit-in profiles instead of interchangeable categories', () => {
    expect(get('c2a').rows.map(r => r.permittedMarks)).toEqual([[0, 2], [0, 2]]);
    expect(get('c2a').rows[1].contextNote).toContain('SAME business');
    expect(get('c2b').rows.map(r => r.marks)).toEqual([1, 1, 4]);
    expect(get('c2b').rows[0].verbatim).toBe('AGENDA');
    expect(get('c2b').rows[1].verbatim).toContain('Election of Officers');
    expect(get('c2b').rows[1].contextNote).toContain('COMPULSORY');
    expect(get('c2b').rows[2].group?.claimMax).toBe(4);
    expect(get('c2b').rows[2].group?.options).toHaveLength(7);
    expect(get('c2b').rows[2].group?.options.some(option => option.includes('Election of Officers'))).toBe(false);
    expect(get('c2d').rows.map(r => r.parts?.map(p => p.marks))).toEqual([[1, 1, 1], [1, 1, 1], [1, 1, 1]]);
    expect(get('c2d').rows[0].contextNote).toContain('No repetition of reason allowed');
  });

  it('preserves the complete local-area tables and two matching solutions for every selected issue', () => {
    expect(get('c3a').rows[0].group?.options).toHaveLength(17);
    expect(get('c3a').rows[0].group?.claimMax).toBe(4);
    expect(get('c3a').rows[0].group?.options).toContain('Principal economic activities');
    expect(get('c3a').rows[0].group?.options).toContain('Healthcare');
    expect(get('c3a').rows[0].group?.options).toContain('Arts/Culture/Entertainment');
    expect(get('c3a').rows[0].group?.options).toContain('Geographical aspects');
    expect(get('c3b').stem).toContain(get('c3a').questionText);
    expect(get('c3b').rows[0].parts?.map(p => p.permittedMarks)).toEqual([[0, 2], [0, 2], [0, 2]]);
    expect(get('c3b').rows[0].contextNote).toContain('ONE aspect');
    expect(get('c3d').rows.map(r => r.parts?.map(p => p.verbatim))).toEqual(Array(3).fill(['Challenge/Issue', 'First way to overcome', 'Second way to overcome']));
    expect(get('c3d').rows[0].contextNote).toContain('Housing/homelessness → Discussion with council/politicians');
    expect(get('c3d').rows[0].contextNote).toContain('Any other relevant point');
    expect(get('c3d').rows[0].contextNote).toContain('no second model is invented');
  });

  it('keeps compulsory diary, full career pool, inclusive-workplace components and the stable whole activity profile', () => {
    expect(get('c4c').rows[0].group?.claimMax).toBe(6);
    expect(get('c4dii').rows.map(r => r.marks)).toEqual([2, 4]);
    expect(get('c4dii').rows[0].contextNote).toContain('COMPULSORY');
    expect(get('c4dii').rows[1].parts).toHaveLength(2);
    for (const word of ['home', 'school', 'community']) expect(get('c4dii').rows[1].contextNote).toContain(word);
    expect(get('c5a').rows[0].group?.options).toHaveLength(18);
    expect(get('c5a').rows[0].group?.options).toContain('Carpentry');
    expect(get('c5c').rows.map(r => r.parts?.map(p => p.marks))).toEqual([[1, 1], [1, 1], [1, 1]]);
    expect(get('c5c').rows[0].contextNote).toContain('MUST relate to this Apprenticeship Fair');
    expect(get('c6a').rows.map(r => r.marks)).toEqual([1, 3]);
    expect(get('c6a').rows[0].verbatim).toBe('Mix of people');
    expect(get('c6a').rows[1].parts).toHaveLength(3);
    expect(get('c7aii').conceptId).toBe('c7aii');
    expect(get('c7aii').questionRef).toContain('Q7(a)');
    expect(get('c7aii').totalMarks).toBe(4);
    expect(get('c7aii').rows.map(r => r.permittedMarks)).toEqual([[0, 2], [0, 2]]);
    expect(get('c7aii').questionText).toContain('(i)');
    expect(get('c7aii').questionText).toContain('(ii)');
  });

  it('preserves all 18 original Atlas identities and complete multi-page source regions', () => {
    expect(anchors.q.map(q => q.n)).toEqual(Array.from({ length: 18 }, (_, i) => String(i + 1)));
    expect(anchors.q.slice(11).map(q => [q.pP, q.endP])).toEqual([[16, 18], [19, 21], [22, 24], [25, 27], [28, 30], [31, 33], [34, 36]]);
    expect(anchors.q.find(q => q.n === '11')?.region.map(r => r.p)).toEqual([4, 5]);
    expect(anchors.q.find(q => q.n === '13')?.region.map(r => r.p)).toEqual([7, 8, 9]);
    expect(local.reviewedEnglish2024.markBankMappings).toHaveLength(45);
    const paper = PAPER_TOPIC_TAGS.find(p => p.subjectId === 'link-modules' && p.year === 2024 && p.lang === 'ev')!;
    for (const mapping of local.reviewedEnglish2024.markBankMappings) {
      const topics = browseTopicIdsForQuestion(paper, paper.q.find(q => q.n === mapping.n)!);
      expect(topics, mapping.id).toEqual(expect.arrayContaining(mapping.atlasTopicIds));
      expect(topics.some(t => curriculumNodeIdsForExamTopic(t).includes(mapping.topicId)), mapping.id).toBe(true);
    }
  });
});
