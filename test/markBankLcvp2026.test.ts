import { describe, expect, it } from 'vitest';
import { CARDS } from '../components/MarkBank/cards/lcvp/common';
import { tariffReconciles } from '../types/markBank';
import review from '../scripts/markbank/authoring/lcvp/2026-cl-main-review.json';
import anchors from '../scripts/paper-trail/answers/2026/LC462CLP000EV.pdf.json';
import local from '../data/examTopics/link-modules-local-crosswalk.json';
import { PAPER_TOPIC_TAGS } from '../data/paperTrail/topicTags';
import { browseTopicIdsForQuestion } from '../components/PaperTrail/topics';
import { curriculumNodeIdsForExamTopic } from '../data/examTopics/registry';

const all = CARDS.filter(c => c.id.startsWith('lcvp-2026-cl-'));
const get = (suffix: string) => {
  const card = all.find(c => c.id === `lcvp-2026-cl-${suffix}`);
  if (!card || card.kind !== 'question') throw new Error(suffix);
  return card;
};

describe('LCVP 2026: independently reviewed original sources', () => {
  it('preserves 45 source leaves as 44 coherent tasks, offering 235 marks', () => {
    expect(review.manualOriginalLeaves).toBe(45);
    expect(review.manualSectionLeaves).toEqual({ A: 8, B: 7, C: 30 });
    expect(all).toHaveLength(44);
    expect(['a', 'b', 'c'].map(s => all.filter(c => c.id.startsWith(`lcvp-2026-cl-${s}`)).length)).toEqual([8, 7, 29]);
    expect(all.reduce((sum, c) => sum + c.totalMarks, 0)).toBe(235);
    expect(all.map(c => c.id).sort()).toEqual(review.tasks.map(c => c.id).sort());
    for (const c of all) {
      if (c.kind !== 'question') throw new Error(c.id);
      expect(tariffReconciles(c), c.id).toBe(true);
      expect(c.level).toBe('common');
      expect(c.questionText + c.stem).not.toMatch(/Leaving Certificate Vocational Programme 2026|Link Modules Examination/);
    }
  });

  it('binds all eight audiovisual tasks to the verified original video with sound', () => {
    const video = get('a1').videoMaterial;
    expect(video?.kind).toBe('source-video');
    expect(video?.canonicalUrl).toBe('https://www.examinations.ie/archive/exampapers/2026/LC462CLP031EV.mov');
    expect(video?.secFileid).toBe('LC462CLP031EV.mov');
    for (let i = 1; i <= 8; i++) {
      expect(get(`a${i}`).videoMaterial).toEqual(video);
      expect(get(`a${i}`).audioMaterial).toBeUndefined();
      expect(get(`a${i}`).additionalSourceMaterials?.[0].pages).toEqual([3]);
    }
    expect(review.video.sha256).toBe('a53c8a8f51e7c4f6817c4528c99ad5fb0d9a6b1f87e7acc5e01b15a563d3eeaa');
    expect(get('a8').questionText).toBe('Describe the factors that contribute to the success of a business.');
    expect(get('a8').stem ?? '').not.toContain('Slí Abhaile');
  });

  it('retains total-only and conflicting numeric allocations without fabricated row marks', () => {
    expect(all.filter(c => c.kind === 'question' && c.tariffModel.kind === 'questionTotal').map(c => c.id)).toEqual(review.heldNumericScoring);
    for (const suffix of ['a2', 'c5d']) expect(get(suffix).rows.every(r => r.marks === null)).toBe(true);
    expect(get('a2').totalMarks).toBe(2);
    expect(get('a2').rows).toHaveLength(3);
    expect(get('a2').rows[0].contextNote).toContain('no response quota');
    const c = get('c5d');
    expect(c.totalMarks).toBe(8);
    expect(c.rows).toHaveLength(6);
    expect(c.rows[0].contextNote).toContain('Type of Training 2@2m (1+1)');
    expect(c.rows[0].contextNote).toContain('2 Benefits 2@1m');
    expect(c.rows[0].contextNote).toContain('6, not 8');
    expect(c.rows.every(r => /Benefits?:/i.test(r.verbatim))).toBe(true);
  });

  it('keeps the complete case study and makes plan content claimable without paying headings', () => {
    for (const c of all.filter(c => c.id.startsWith('lcvp-2026-cl-b'))) {
      if (c.kind !== 'question') throw new Error(c.id);
      expect(c.stem).toContain('manufacturing technician');
      expect(c.stem).toContain('develop and execute these plans successfully');
      expect(c.sourceMaterial?.pages).toEqual([9]);
    }
    const row = get('b3iii').rows[0];
    expect(row.marks).toBe(2);
    expect(row.parts?.map(p => p.marks)).toEqual([1, 1]);
    expect(row.contextNote).toContain('NO MARKS FOR HEADINGS');
    for (const heading of ['Aims/Objectives', 'Research methods', 'Analysis of research', 'Resources', 'Action steps', 'Schedule of time', 'Costings/finance', 'Evaluation methods']) expect(row.contextNote).toContain(heading);
  });

  it('keeps all open choices, source examples and exact partial component ladders', () => {
    expect(get('a3').rows[0].group?.options).toHaveLength(5);
    expect(get('a3').rows[0].group?.claimMax).toBe(3);
    expect(get('a5').rows[0].group?.options).toHaveLength(6);
    expect(get('b3i').rows[0].group?.options).toHaveLength(15);
    expect(get('c6b').rows[0].group?.options).toHaveLength(16);
    expect(get('c6b').rows[0].contextNote).toContain('Etc.');
    expect(get('a7').rows[0].parts?.map(p => p.permittedMarks)).toEqual([[0, 1, 2], [0, 1, 2], [0, 1, 2]]);
    expect(get('a8').rows[0].contextNote).toContain('No repetition of expansions');
    expect(get('c1c').rows[0].contextNote).toContain('Mentally prepare');
    expect(get('c6c').rows[0].contextNote).toContain('Provides a service/product that was not available previously');
  });

  it('retains the full advertisement and separately required coherent response components', () => {
    for (const letter of 'abcd') {
      expect(get(`c1${letter}`).stem).toContain('careers@beautybylola.ie');
      expect(get(`c1${letter}`).stem).toContain('examples of your work');
    }
    expect(get('c2c').rows).toHaveLength(3);
    expect(get('c2c').rows.map(r => r.parts?.map(p => p.marks))).toEqual([[1, 2], [1, 2], [1, 2]]);
    expect(get('c2c').rows[0].contextNote).toContain('Cultural differences');
    expect(get('c3b').rows.map(r => r.marks)).toEqual([1, 3]);
    expect(get('c3b').rows[0].contextNote).toContain('OR “Not discriminated”');
    expect(get('c4c').rows.map(r => r.marks)).toEqual(Array(8).fill(1));
    expect(get('c4c').rows.map(r => r.verbatim)).toEqual(['To: email address', 'Subject line', 'Salutation', 'Introduction', 'Reason for email', 'Dates', 'CV attached', 'Closing']);
    expect(get('c5a').rows.map(r => r.permittedMarks)).toEqual([[0, 2], [0, 2]]);
    expect(get('c5c').stem).toContain('What job would you like to do when you leave school?');
    expect(get('c5c').rows.map(r => r.marks)).toEqual([1, 2, 6]);
  });

  it('keeps one group, one personal and one other evaluation response', () => {
    const row = get('c7d').rows[0];
    expect(row.parts?.map(p => p.verbatim)).toEqual(['Group method', 'Personal method', 'Other group or personal method']);
    expect(row.parts?.map(p => p.marks)).toEqual([3, 3, 3]);
    expect(row.contextNote).toContain('ONE other (group OR personal)');
    expect(row.contextNote).toContain('Review of portfolio item');
    expect(get('c7bi').totalMarks).toBe(2);
    expect(get('c7bii').totalMarks).toBe(4);
  });

  it('preserves all 18 physical Atlas IDs and complete question/scheme ranges', () => {
    expect(anchors.q.map(q => q.n)).toEqual(Array.from({ length: 18 }, (_, i) => String(i + 1)));
    expect(anchors.q.slice(11).map(q => [q.pP, q.endP])).toEqual([[16, 18], [19, 21], [22, 24], [25, 27], [28, 30], [31, 33], [34, 36]]);
    expect(anchors.q.find(q => q.n === '11')?.region.map(r => r.p)).toEqual([7, 8]);
    expect(anchors.q.find(q => q.n === '16')?.region.map(r => r.p)).toEqual([16, 17]);
    expect(local.reviewedEnglish2026.markBankMappings).toHaveLength(44);
    const paper = PAPER_TOPIC_TAGS.find(p => p.subjectId === 'link-modules' && p.year === 2026 && p.lang === 'ev')!;
    expect(paper.q).toHaveLength(18);
    for (const mapping of local.reviewedEnglish2026.markBankMappings) {
      const topics = browseTopicIdsForQuestion(paper, paper.q.find(q => q.n === mapping.n)!);
      expect(topics, mapping.id).toEqual(expect.arrayContaining(mapping.atlasTopicIds));
      expect(topics.some(t => curriculumNodeIdsForExamTopic(t).includes(mapping.topicId)), mapping.id).toBe(true);
    }
  });
});
