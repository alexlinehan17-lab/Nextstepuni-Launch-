import { describe, expect, it } from 'vitest';
import { CARDS } from '../components/MarkBank/cards/lcvp/common';
import { tariffReconciles } from '../types/markBank';
import review from '../scripts/markbank/authoring/lcvp/2023-cl-main-review.json';
import anchors from '../scripts/paper-trail/answers/2023/LC462CLP000EV.pdf.json';
import local from '../data/examTopics/link-modules-local-crosswalk.json';
import { PAPER_TOPIC_TAGS } from '../data/paperTrail/topicTags';
import { browseTopicIdsForQuestion } from '../components/PaperTrail/topics';
import { curriculumNodeIdsForExamTopic } from '../data/examTopics/registry';

const all = CARDS.filter(c => c.id.startsWith('lcvp-2023-cl-'));
const get = (suffix: string) => {
  const card = all.find(c => c.id === `lcvp-2023-cl-${suffix}`);
  if (!card || card.kind !== 'question') throw new Error(suffix);
  return card;
};

describe('LCVP 2023: complete tasks and source-specific allocations', () => {
  it('covers all 43 independent source leaves and restores both missing profiles', () => {
    expect(review.manualOriginalLeaves).toBe(43);
    expect(review.manualSectionLeaves).toEqual({ A: 8, B: 6, C: 29 });
    expect(all).toHaveLength(43);
    expect(all.reduce((sum, c) => sum + c.totalMarks, 0)).toBe(235);
    expect(all.map(c => c.id).sort()).toEqual(review.tasks.map(c => c.id).sort());
    expect([get('c6a').totalMarks, get('c7b').totalMarks]).toEqual([4, 7]);
    for (const c of all) {
      if (c.kind !== 'question') throw new Error(c.id);
      expect(tariffReconciles(c), c.id).toBe(true);
      expect(c.questionText + c.stem).not.toMatch(/Leaving Certificate Vocational Programme 2023|Link Modules Examination/);
    }
  });

  it('retains the universal six-mark award visibly without answer-dependent scoring', () => {
    const c = get('a6');
    expect(c.tariffModel.kind).toBe('questionTotal');
    expect(c.totalMarks).toBe(6);
    expect(c.rows).toHaveLength(9);
    expect(c.rows.every(r => r.marks == null && !r.parts?.length && !r.group)).toBe(true);
    expect(c.rows[0].verbatim).toContain('Award 6 marks to all candidates');
    expect(c.rows[0].verbatim).toContain('Part 2 rather than for Part 3.');
    expect(c.rows[0].verbatim).toContain('Three valid reasons 2 x 3 marks (0/3)');
    expect(c.rows[0].contextNote).toContain('confidence only');
    expect(c.rows[1].verbatim).toContain('Sending on Job spec');
    expect(c.rows[8].verbatim).toContain('broaden the experience');
    expect(all.filter(c => c.kind === 'question' && c.tariffModel.kind === 'fixed').reduce((sum, c) => sum + c.totalMarks, 0)).toBe(229);
  });

  it('binds all AV tasks to the 2023 original video with its printed instructions', () => {
    const video = get('a1').videoMaterial;
    expect(video?.canonicalUrl).toBe('https://www.examinations.ie/archive/exampapers/2023/LC462CLP031EV.mov');
    expect(video?.kind).toBe('source-video');
    for (const c of all.filter(c => c.id.startsWith('lcvp-2023-cl-a'))) {
      if (c.kind !== 'question') throw new Error(c.id);
      expect(c.videoMaterial).toEqual(video);
      expect(c.audioMaterial).toBeUndefined();
      expect(c.additionalSourceMaterials?.[0].pages).toEqual([3]);
    }
    expect(get('a2').rows[0].group?.options).toHaveLength(4);
    expect(get('a3').rows[0].group?.options).toHaveLength(6);
    expect(get('a7').rows[0].parts?.map(p => p.permittedMarks)).toEqual([[0, 1, 2, 3], [0, 1, 2, 3]]);
    expect(get('a7').rows[0].contextNote).toContain('Any relevant stakeholder');
  });

  it('retains the whole case and both compulsory remote-work and Brexit categories', () => {
    for (const c of all.filter(c => c.id.startsWith('lcvp-2023-cl-b'))) {
      if (c.kind !== 'question') throw new Error(c.id);
      expect(c.stem).toContain('Ballyfert');
      expect(c.stem).toContain('320');
      expect(c.stem).toContain('National Broadband Plan');
      expect(c.sourceMaterial?.pages).toEqual([9]);
    }
    expect(get('b2ii').rows.map(r => r.verbatim)).toEqual(['Advantages', 'Disadvantages', 'one other']);
    expect(get('b2ii').rows.map(r => r.marks)).toEqual([2, 2, 2]);
    expect(get('b2ii').rows[0].contextNote).toContain('Avoid office politics');
    expect(get('b2ii').rows[0].contextNote).toContain('eye strain/too much screen time');
    expect(get('c1d').rows.map(r => r.verbatim)).toEqual(['Business', 'Consumers', 'one other']);
    expect(get('c1d').rows.map(r => r.marks)).toEqual([3, 3, 3]);
    expect(get('c1d').rows[0].contextNote).toContain('Mobile phone roaming charges');
    expect(get('c1d').rows[0].contextNote).toContain('one from EACH required category');
  });

  it('keeps both distinct research profiles and the complete original table columns', () => {
    const c = get('b3i');
    expect(c.rows.map(r => r.verbatim)).toEqual(['Primary/Field', 'Secondary/Desk']);
    expect(c.rows.map(r => r.parts?.map(p => [p.verbatim, p.marks]))).toEqual(Array(2).fill([['type', 1], ['example', 1], ['advantage', 1]]));
    expect(c.rows[0].contextNote).toContain('Postal surveys');
    expect(c.rows[0].contextNote).not.toContain('Publications/census');
    expect(c.rows[1].contextNote).toContain('Press releases etc.');
    expect(c.rows[1].contextNote).not.toContain('Postal surveys');
    expect(c.rows[0].contextNote).toContain('Do not repeat the advantage');
    expect(get('b3ii').rows[0].contextNote).toContain('No marks for headings');
    expect(get('b3ii').rows[0].contextNote).toContain('Infrastructure/facilities');
  });

  it('requires all non-Forming stages and two applications for every marketing P', () => {
    expect(get('c2d').rows).toHaveLength(3);
    expect(get('c2d').rows.map(r => r.verbatim.split(' –')[0])).toEqual(['Storming', 'Norming', 'Performing']);
    expect(get('c2d').rows.every(r => r.marks === 3)).toBe(true);
    const marketing = get('c4c');
    expect(marketing.rows).toHaveLength(4);
    expect(marketing.rows.map(r => r.parts?.map(p => p.marks))).toEqual(Array(4).fill([1, 1]));
    expect(marketing.rows.every(r => r.contextNote?.includes('NO marks for headings'))).toBe(true);
    expect(marketing.rows[0].contextNote).toContain('Good design');
    expect(marketing.rows[1].contextNote).toContain('Be in line with competitors');
    expect(marketing.rows[3].contextNote).toContain('giving back to local community');
    expect(get('c4d').rows.map(r => r.parts?.map(p => p.marks))).toEqual(Array(3).fill([1, 1, 1]));
    expect(get('c4d').rows[0].contextNote).toContain('NO repetition of reasons');
  });

  it('preserves separate contract components and coherent subject and CSR profiles', () => {
    expect(get('c5ci').rows.map(r => r.marks)).toEqual([1, 1, 1]);
    expect(get('c5ci').rows[1].verbatim).toContain('between the employer and the employee');
    expect(get('c5cii').rows[0].group?.options).toHaveLength(13);
    expect(get('c5cii').rows[0].group?.claimMax).toBe(3);
    expect(get('c6a').rows.map(r => r.parts?.map(p => p.marks))).toEqual([[1, 1], [1, 1]]);
    expect(get('c6a').rows[0].contextNote).toContain('THAT subject');
    expect(get('c7a').rows[0].parts).toHaveLength(4);
    expect(get('c7b').rows.map(r => r.marks)).toEqual([1, 6]);
    expect(get('c7b').rows[0].contextNote).toContain('SAME enterprise');
    for (const stakeholder of ['Customers', 'Employees', 'Suppliers', 'Community', 'Environment', 'Government', 'Shareholders']) {
      expect(get('c7b').rows[1].contextNote).toContain(stakeholder);
    }
  });

  it('preserves all 18 Atlas identities with complete source regions and canonical mappings', () => {
    expect(anchors.q.map(q => q.n)).toEqual(Array.from({ length: 18 }, (_, i) => String(i + 1)));
    expect(anchors.q.slice(11).map(q => [q.pP, q.endP])).toEqual([[16, 18], [19, 21], [22, 24], [25, 27], [28, 30], [31, 33], [34, 36]]);
    expect(anchors.q.find(q => q.n === '10')?.region.map(r => r.p)).toEqual([6, 7]);
    expect(anchors.q.find(q => q.n === '11')?.region.map(r => r.p)).toEqual([7, 8]);
    expect(anchors.q.find(q => q.n === '18')?.region.map(r => r.p)).toEqual([20, 21]);
    expect(local.reviewedEnglish2023.markBankMappings).toHaveLength(43);
    const paper = PAPER_TOPIC_TAGS.find(p => p.subjectId === 'link-modules' && p.year === 2023 && p.lang === 'ev' && p.fileid === 'LC462CLP000EV.pdf')!;
    for (const mapping of local.reviewedEnglish2023.markBankMappings) {
      const topics = browseTopicIdsForQuestion(paper, paper.q.find(q => q.n === mapping.n)!);
      expect(topics, mapping.id).toEqual(expect.arrayContaining(mapping.atlasTopicIds));
      expect(topics.some(t => curriculumNodeIdsForExamTopic(t).includes(mapping.topicId)), mapping.id).toBe(true);
    }
  });
});
