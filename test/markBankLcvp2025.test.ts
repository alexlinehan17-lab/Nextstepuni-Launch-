import { describe, expect, it } from 'vitest';
import { CARDS } from '../components/MarkBank/cards/lcvp/common';
import { tariffReconciles } from '../types/markBank';
import review from '../scripts/markbank/authoring/lcvp/2025-cl-main-review.json';
import anchors from '../scripts/paper-trail/answers/2025/LC462CLP000EV.pdf.json';
import local from '../data/examTopics/link-modules-local-crosswalk.json';
import { PAPER_TOPIC_TAGS } from '../data/paperTrail/topicTags';
import { browseTopicIdsForQuestion } from '../components/PaperTrail/topics';
import { curriculumNodeIdsForExamTopic } from '../data/examTopics/registry';

const all = CARDS.filter(c => c.id.startsWith('lcvp-2025-cl-'));
const get = (suffix: string) => {
  const card = all.find(c => c.id === `lcvp-2025-cl-${suffix}`);
  if (!card || card.kind !== 'question') throw new Error(suffix);
  return card;
};

describe('LCVP 2025: original task boundaries and allocations', () => {
  it('preserves 46 independently reviewed leaves as 45 whole tasks, including all three omissions', () => {
    expect(review.manualOriginalLeaves).toBe(46);
    expect(review.manualSectionLeaves).toEqual({ A: 9, B: 7, C: 30 });
    expect(all).toHaveLength(45);
    expect(['a', 'b', 'c'].map(s => all.filter(c => c.id.startsWith(`lcvp-2025-cl-${s}`)).length)).toEqual([9, 7, 29]);
    expect(all.reduce((sum, c) => sum + c.totalMarks, 0)).toBe(235);
    expect(all.map(c => c.id).sort()).toEqual(review.tasks.map(c => c.id).sort());
    expect(get('a6ii').totalMarks).toBe(4);
    expect(get('c2a').totalMarks).toBe(4);
    expect(get('c4d').totalMarks).toBe(9);
    for (const c of all) {
      if (c.kind !== 'question') throw new Error(c.id);
      expect(tariffReconciles(c), c.id).toBe(true);
      expect(c.questionText + c.stem).not.toMatch(/Leaving Certificate Vocational Programme 2025|Link Modules Examination/);
    }
  });

  it('keeps the nine AV tasks bound to the original video and A2 whole-response 0/2 ladder', () => {
    const video = get('a1').videoMaterial;
    expect(video?.kind).toBe('source-video');
    expect(video?.canonicalUrl).toBe('https://www.examinations.ie/archive/exampapers/2025/LC462CLP031EV.mov');
    expect(video?.secFileid).toBe('LC462CLP031EV.mov');
    for (const c of all.filter(c => c.id.startsWith('lcvp-2025-cl-a'))) {
      if (c.kind !== 'question') throw new Error(c.id);
      expect(c.videoMaterial).toEqual(video);
      expect(c.audioMaterial).toBeUndefined();
      expect(c.additionalSourceMaterials?.[0].pages).toEqual([3]);
    }
    expect(review.media.fullFileDownloaded).toBe(false);
    expect(get('a6i').questionText).toBe('What resources are needed for the presentation?');
    expect(get('a6i').rows[0].group?.options).toEqual(['Laptop', 'Data projector', 'USB', 'Notes']);
    expect(get('a2').tariffModel.kind).toBe('fixed');
    expect(get('a2').rows[0].permittedMarks).toEqual([0, 2]);
    expect(get('a2').rows[0].verbatim).toContain('going back into the local community');
    expect(get('a2').rows[0].verbatim).toContain('already had people in from local businesses');
    expect(get('a2').rows[0].contextNote).toContain('going back into the local community');
    expect(get('a2').rows[0].contextNote).toContain('already had people in from local businesses');
    expect(get('a8').stem ?? '').not.toContain('Glenhale');
  });

  it('retains the four required SWOT categories and literal unresolved allocation without guessing weights', () => {
    const c = get('b1');
    expect(c.totalMarks).toBe(6);
    expect(c.tariffModel.kind).toBe('questionTotal');
    expect(c.rows.map(r => r.marks)).toEqual([null, null, null, null]);
    expect(c.rows.map(r => r.verbatim.split(':')[0])).toEqual(['Strength', 'Weakness', 'Opportunity', 'Threat']);
    expect(c.rows[0].contextNote).toContain('6 marks (2+2+1+1)');
    expect(c.rows[0].contextNote).toContain('allocation ambiguity');
    expect(c.rows[0].contextNote).toContain('ONE strength, ONE weakness, ONE opportunity and ONE threat');
    expect(c.rows[2].verbatim).toContain('apprenticeships');
    expect(c.rows[3].verbatim).toContain('uncertain economic conditions');
    expect(all.filter(c => c.kind === 'question' && c.tariffModel.kind === 'questionTotal').map(c => c.id)).toEqual(review.heldNumericScoring);
  });

  it('carries the complete case and dependent asks while paying action-plan content instead of headings', () => {
    for (const c of all.filter(c => c.id.startsWith('lcvp-2025-cl-b'))) {
      if (c.kind !== 'question') throw new Error(c.id);
      expect(c.stem).toContain('a market town');
      expect(c.stem).toContain('sustain and revive the town centre');
      expect(c.sourceMaterial?.pages).toEqual([9]);
    }
    expect(get('b2iii').stem).toContain(get('b2ii').questionText);
    expect(get('b2iii').rows[0].group?.claimMax).toBe(3);
    expect(get('b2iii').rows[0].group?.options).toHaveLength(9);
    const plan = get('b3ii');
    expect(plan.totalMarks).toBe(6);
    expect(plan.rows.map(r => r.marks)).toEqual([1, 5]);
    expect(plan.rows[0].contextNote).toContain('Relocate the schools outside the town');
    expect(plan.rows[1].parts?.map(p => p.marks)).toEqual([1, 1, 1, 1, 1]);
    expect(plan.rows[1].contextNote).toContain('NO MARKS FOR HEADINGS');
    for (const h of ['Aims/Objectives', 'Research methods', 'Analysis of research', 'Resources/action steps', 'Schedule of time', 'Costings/finance', 'Evaluation methods']) expect(plan.rows[1].contextNote).toContain(h);
  });

  it('requires the complete questionnaire, matched subject profiles and source-description-reason profiles', () => {
    expect(get('c1c').rows.map(r => r.marks)).toEqual([1, 1, 1, 5]);
    expect(get('c1c').rows.slice(0, 3).map(r => r.verbatim)).toEqual(['Heading', 'variety of question styles', 'instructions']);
    expect(get('c1c').rows[3].parts).toHaveLength(5);
    expect(get('c1d').stem).toContain(get('c1c').questionText);
    expect(get('c2a').questionText).toContain('(i) Name two Leaving Certificate subjects');
    expect(get('c2a').questionText).toContain('(ii) Outline how these subjects');
    expect(get('c2a').rows.map(r => r.parts?.map(p => p.marks))).toEqual([[1, 1], [1, 1]]);
    expect(get('c2a').rows.map(r => r.parts?.map(p => p.verbatim))).toEqual(Array(2).fill(['Subject', 'Outline for this subject']));
    expect(get('c2d').rows.map(r => r.parts?.map(p => p.verbatim))).toEqual(Array(3).fill(['Source', 'Description', 'Reason']));
    expect(get('c2d').rows[0].contextNote).toContain('Self-assessment/aptitude tests');
  });

  it('keeps coherent visited-business and challenge profiles, with the complete eight-cell table', () => {
    expect(get('c4a').rows.map(r => r.permittedMarks)).toEqual([[0, 2], [0, 2]]);
    expect(get('c4a').rows[1].contextNote).toContain('SAME business');
    expect(get('c4b').rows[0].parts).toHaveLength(4);
    expect(get('c4b').rows[0].contextNote).toContain('No marks for headings');
    expect(get('c4b').rows[0].contextNote).toContain('Production/Manufacturing process');
    const challenge = get('c4d');
    expect(challenge.rows.map(r => r.parts?.map(p => p.marks))).toEqual([[1, 2], [1, 2], [1, 2]]);
    const profiles = challenge.rows[0].contextNote!.split('each cell kept intact: ')[1].split(' | ');
    expect(profiles).toHaveLength(8);
    expect(profiles.map(p => p.split(' ')[0])).toEqual(['1.', '2.', '3.', '4.', '5.', '6.', '7.', '8.']);
    expect(profiles[0]).toContain('Funding cashflow/securing funding/managing debt');
    expect(profiles[0]).toMatch(/make workers redundant$/);
    expect(profiles[1]).toMatch(/necessary skills$/);
    expect(profiles[2]).toMatch(/services option$/);
    expect(profiles[3]).toMatch(/other countries$/);
    expect(profiles[4]).toContain('Brexit/ U.S. Tariffs');
    expect(profiles[4]).toMatch(/locally where possible$/);
    expect(profiles[5]).toMatch(/more efficient$/);
    expect(profiles[6]).toMatch(/good customer service$/);
    expect(profiles[7]).toMatch(/stay informed$/);
  });

  it('restores the Agenda heading and retains required category quotas and historical source guidance', () => {
    expect(get('c5a').totalMarks).toBe(4);
    expect(get('c5a').rows.map(r => r.marks)).toEqual([1, 3]);
    expect(get('c5a').rows[1].group?.claimMax).toBe(3);
    expect(get('c5a').rows[1].group?.options).toHaveLength(10);
    expect([get('c5c').totalMarks, get('c5d').totalMarks]).toEqual([9, 8]);
    expect(get('c6c').rows.map(r => r.verbatim)).toEqual(['Advantages', 'Disadvantages']);
    expect(get('c6c').rows.map(r => r.parts?.map(p => p.permittedMarks))).toEqual([[[0, 1, 2], [0, 1, 2]], [[0, 1, 2], [0, 1, 2]]]);
    expect(get('c6c').rows[0].contextNote).toContain('Saving money/fuel cost/childcare cost/lunch costs');
    expect(get('c6c').rows[1].contextNote).toContain('Cost of equipment and infrastructure/potential energy bill');
    expect(get('c3d').rows[0].contextNote).toContain('€9.45');
    expect(get('c7ai').rows[0].permittedMarks).toEqual([0, 1, 2]);
    expect(get('c7aii').rows[0].group?.claimMax).toBe(1);
    expect(get('c7aii').rows[0].group?.perOption).toBe(2);
    expect(get('c7aii').rows[0].group?.options).toHaveLength(6);
  });

  it('retains all original 18 Atlas identities, complete ranges and canonical subject topics', () => {
    expect(anchors.q.map(q => q.n)).toEqual(Array.from({ length: 18 }, (_, i) => String(i + 1)));
    expect(anchors.q.slice(11).map(q => [q.pP, q.endP])).toEqual([[16, 18], [19, 21], [22, 24], [25, 27], [28, 30], [31, 33], [34, 36]]);
    expect(anchors.q.find(q => q.n === '9')?.region.map(r => r.p)).toEqual([6]);
    expect(anchors.q.find(q => q.n === '15')?.region.map(r => r.p)).toEqual([13, 14]);
    expect(anchors.q.find(q => q.n === '17')?.region.map(r => r.p)).toEqual([16, 17, 18]);
    expect(local.reviewedEnglish2025.markBankMappings).toHaveLength(45);
    const paper = PAPER_TOPIC_TAGS.find(p => p.subjectId === 'link-modules' && p.year === 2025 && p.lang === 'ev')!;
    expect(paper.q).toHaveLength(18);
    for (const mapping of local.reviewedEnglish2025.markBankMappings) {
      const topics = browseTopicIdsForQuestion(paper, paper.q.find(q => q.n === mapping.n)!);
      expect(topics, mapping.id).toEqual(expect.arrayContaining(mapping.atlasTopicIds));
      expect(topics.some(t => curriculumNodeIdsForExamTopic(t).includes(mapping.topicId)), mapping.id).toBe(true);
    }
  });
});
