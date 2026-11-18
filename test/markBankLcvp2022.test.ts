import { describe, expect, it } from 'vitest';
import { CARDS } from '../components/MarkBank/cards/lcvp/common';
import { tariffReconciles } from '../types/markBank';
import review from '../scripts/markbank/authoring/lcvp/2022-cl-main-review.json';
import anchors from '../scripts/paper-trail/answers/2022/LC462CLP000EV.pdf.json';
import local from '../data/examTopics/link-modules-local-crosswalk.json';
import { PAPER_TOPIC_TAGS } from '../data/paperTrail/topicTags';
import { browseTopicIdsForQuestion } from '../components/PaperTrail/topics';
import { curriculumNodeIdsForExamTopic } from '../data/examTopics/registry';

const all = CARDS.filter(c => c.id.startsWith('lcvp-2022-cl-'));
const get = (suffix: string) => {
  const card = all.find(c => c.id === `lcvp-2022-cl-${suffix}`);
  if (!card || card.kind !== 'question') throw new Error(suffix);
  return card;
};

describe('LCVP 2022: source-complete COVID-adjusted written tasks', () => {
  it('preserves 46 leaves as 45 coherent tasks and distinguishes 230 offered from 130 candidate marks', () => {
    expect(review.manualOriginalLeaves).toBe(46);
    expect(review.manualSectionLeaves).toEqual({ A: 8, B: 7, C: 31 });
    expect(review.candidateWrittenMarks).toBe(130);
    expect(all).toHaveLength(45);
    expect(all.reduce((sum, c) => sum + c.totalMarks, 0)).toBe(230);
    expect(all.map(c => c.id).sort()).toEqual(review.tasks.map(c => c.id).sort());
    expect(['b2i', 'c1c', 'c2a', 'c2b', 'c2d', 'c5b', 'c6c'].map(s => get(s).totalMarks)).toEqual([2, 8, 4, 4, 9, 4, 8]);
    for (const c of all) {
      if (c.kind !== 'question') throw new Error(c.id);
      expect(tariffReconciles(c), c.id).toBe(true);
      expect(c.tariffModel.kind).toBe('fixed');
      expect(c.questionText + c.stem).not.toMatch(/Leaving Certificate Vocational Programme 2022|Link Modules Examination/);
    }
  });

  it('preserves the original video and all four CSR-area pools inside one six-mark choice', () => {
    const video = get('a1').videoMaterial;
    expect(video?.canonicalUrl).toBe('https://www.examinations.ie/archive/exampapers/2022/LC462CLP031EV.mov');
    for (const c of all.filter(c => c.id.startsWith('lcvp-2022-cl-a'))) {
      if (c.kind !== 'question') throw new Error(c.id);
      expect(c.videoMaterial).toEqual(video);
      expect(c.audioMaterial).toBeUndefined();
      expect(c.additionalSourceMaterials?.[0].pages).toEqual([3]);
    }
    expect(get('a1').rows[0].group?.options).toHaveLength(4);
    expect(get('a2').rows[0].group?.options).toHaveLength(5);
    expect(get('a5').rows[0].group?.claimMax).toBe(4);
    expect(get('a5').rows[0].group?.perOption).toBe(1);
    const c = get('a6');
    expect(c.rows).toHaveLength(1);
    expect(c.rows[0].parts).toHaveLength(6);
    for (const area of ['Community', 'Workplace', 'Environment', 'Marketplace']) {
      expect(c.questionText).toContain(area);
      expect(c.rows[0].contextNote).toContain(area + ':');
    }
    expect(c.rows[0].contextNote).toContain('Do not mix reasons');
    expect(c.rows[0].contextNote).toContain('No separate mark for naming the area');
    expect(c.rows[0].contextNote).toContain('Ensuring high safety standards for consumers');
  });

  it('keeps both diversification categories, complete footer-adjacent duties and all four specification categories', () => {
    expect(get('b2i').rows.map(r => r.marks)).toEqual([1, 1]);
    expect(get('b2i').rows[0].verbatim).toContain('Increased sales and revenue');
    expect(get('b2i').rows[1].verbatim).toContain('Can confuse customers');
    expect(get('b2ii').rows[0].group?.options).toEqual(['Website development and maintenance', 'Digital marketing', 'Product Promotion', 'Cyber Security']);
    expect(get('b2iii').stem).toContain(get('b2ii').questionText);
    expect(get('b2iii').rows.map(r => r.verbatim.split(':')[0])).toEqual(['Skills', 'Qualification', 'Personal attributes', 'Experience']);
    expect(get('b2iii').rows.map(r => r.marks)).toEqual([1, 1, 1, 1]);
    expect(get('b1').stem).toContain('Alex and Rami');
    expect(get('b1').sourceMaterial?.pages).toEqual([10]);
  });

  it('retains the complete running schedule and its distinct event, actions and time-sequence marks', () => {
    expect(get('c1a').rows).toHaveLength(1);
    expect(get('c1a').rows[0].group?.claimMax).toBe(4);
    expect(get('c1a').rows[0].group?.options).toHaveLength(10);
    const c = get('c1c');
    expect(c.rows.map(r => r.marks)).toEqual([2, 5, 1]);
    expect(c.rows[1].parts).toHaveLength(5);
    for (const phrase of ['Nov. 1-5', 'Nov. 8-12', 'Nov. 15-19', 'Nov. 22-26', 'Dec 2nd night of show', 'Dec 6th', 'Hold fashion show', 'Evaluation of activity']) {
      expect(c.rows[1].contextNote).toContain(phrase);
    }
    expect(c.rows[1].contextNote).toContain('FIVE other valid actions');
    expect(c.rows[2].verbatim).toBe('sequence of time');
  });

  it('requires coherent personal profiles and the full four-benefit/four-challenge/extra allocation', () => {
    expect(get('c2a').questionText).toContain('(i)');
    expect(get('c2a').questionText).toContain('(ii)');
    expect(get('c2a').rows.map(r => r.marks)).toEqual([1, 3]);
    expect(get('c2a').rows[1].contextNote).toContain('career you named');
    expect(get('c2b').rows.map(r => r.marks)).toEqual([1, 3]);
    expect(get('c2b').rows[0].contextNote).toContain('College open days');
    const c = get('c2d');
    expect(c.rows.map(r => r.marks)).toEqual([4, 4, 1]);
    expect(c.rows.slice(0, 2).map(r => r.group?.options.length)).toEqual([11, 9]);
    expect(c.rows[0].group?.options[6]).toContain('9 to 5.');
    expect(c.rows[2].contextNote).toContain('Do not repeat');
    expect(get('c3a').rows[0].parts?.map(p => p.permittedMarks)).toEqual([[0, 2], [0, 2]]);
  });

  it('preserves required health-and-safety categories and the challenge2/solution1 allocation', () => {
    expect(get('c4d').rows.map(r => r.verbatim)).toEqual(['Employee benefit', 'Employer benefit', 'other benefit point']);
    expect(get('c4d').rows.map(r => r.marks)).toEqual([3, 3, 3]);
    expect(get('c4d').rows[0].contextNote).toContain('one undivided model pool');
    expect(get('c5b').rows[0].contextNote).toContain('Construction');
    expect(get('c5d').rows.map(r => r.parts?.map(p => p.marks))).toEqual(Array(3).fill([2, 1]));
    expect(get('c5d').rows[0].parts?.[0].permittedMarks).toEqual([0, 1, 2]);
    expect(get('c5d').rows[0].contextNote).toContain('Any local point relevant');
  });

  it('retains all paired comparisons and every distinct email component plus the full original model', () => {
    expect(get('c6b').rows.map(r => r.parts?.map(p => p.verbatim))).toEqual(Array(2).fill(['Voluntary Organisation', 'Commercial Business']));
    expect(get('c6b').rows[0].contextNote).toContain('Benefits the community. → Benefits owners/investors.');
    const email = get('c6c');
    expect(email.rows.map(r => r.verbatim)).toEqual(['To: email address', 'Subject line', 'Salutation', 'Introduction', 'Reason for email', 'Availability', 'Concluding statement', 'Closing']);
    expect(email.rows.map(r => r.marks)).toEqual(Array(8).fill(1));
    for (const phrase of ['paul_d@svp.ie', 'Dear Paul,', 'XXXX Community School', '2-3 hours per week', 'Yours sincerely/Regards,', 'Rebecca O’Sullivan']) expect(email.rows[0].contextNote).toContain(phrase);
    expect(email.rows[0].contextNote).not.toContain('Summary of marks');
    expect([get('c7di').totalMarks, get('c7dii').totalMarks]).toEqual([3, 6]);
  });

  it('retains all 18 Atlas anchors and complete shifted paper/scheme regions', () => {
    expect(anchors.q.map(q => q.n)).toEqual(Array.from({ length: 18 }, (_, i) => String(i + 1)));
    expect(anchors.q.slice(11).map(q => [q.pP, q.endP])).toEqual([[18, 20], [21, 23], [24, 26], [27, 29], [30, 32], [33, 35], [36, 38]]);
    expect(anchors.q.find(q => q.n === '12')?.region.map(r => r.p)).toEqual([8, 9]);
    expect(anchors.q.find(q => q.n === '17')?.region.map(r => r.p)).toEqual([18, 19]);
    expect(local.reviewedEnglish2022.markBankMappings).toHaveLength(45);
    const paper = PAPER_TOPIC_TAGS.find(p => p.subjectId === 'link-modules' && p.year === 2022 && p.lang === 'ev' && p.fileid === 'LC462CLP000EV.pdf')!;
    for (const mapping of local.reviewedEnglish2022.markBankMappings) {
      const topics = browseTopicIdsForQuestion(paper, paper.q.find(q => q.n === mapping.n)!);
      expect(topics, mapping.id).toEqual(expect.arrayContaining(mapping.atlasTopicIds));
      expect(topics.some(t => curriculumNodeIdsForExamTopic(t).includes(mapping.topicId)), mapping.id).toBe(true);
    }
  });
});
