import { describe, expect, it } from 'vitest';
import { CARDS } from '../components/MarkBank/cards/lcvp/common';
import { tariffReconciles } from '../types/markBank';
import review from '../scripts/markbank/authoring/lcvp/2021-cl-main-review.json';
import anchors from '../scripts/paper-trail/answers/2021/LC462CLP000EV.pdf.json';
import local from '../data/examTopics/link-modules-local-crosswalk.json';
import { PAPER_TOPIC_TAGS } from '../data/paperTrail/topicTags';
import { browseTopicIdsForQuestion } from '../components/PaperTrail/topics';
import { curriculumNodeIdsForExamTopic } from '../data/examTopics/registry';

const all = CARDS.filter(c => c.id.startsWith('lcvp-2021-cl-'));
const get = (suffix: string) => {
  const card = all.find(c => c.id === `lcvp-2021-cl-${suffix}`);
  if (!card || card.kind !== 'question') throw new Error(suffix);
  return card;
};

describe('LCVP 2021: complete original tasks and contextual source pools', () => {
  it('reconciles 49 printed leaves with 45 whole tasks and the adjusted 130-mark candidate route', () => {
    expect(review.manualOriginalLeaves).toBe(49);
    expect(review.manualSectionLeaves).toEqual({ A: 10, B: 8, C: 31 });
    expect(review.candidateWrittenMarks).toBe(130);
    expect(all).toHaveLength(45);
    expect(all.reduce((sum, c) => sum + c.totalMarks, 0)).toBe(230);
    expect(all.map(c => c.id).sort()).toEqual(review.tasks.map(c => c.id).sort());
    expect(['a6i', 'a6ii', 'c2a', 'c2b', 'c5c'].map(s => get(s).totalMarks)).toEqual([4, 2, 4, 6, 6]);
    for (const c of all) {
      if (c.kind !== 'question') throw new Error(c.id);
      expect(tariffReconciles(c), c.id).toBe(true);
      expect(c.tariffModel.kind).toBe('fixed');
      expect(c.questionText + c.stem).not.toMatch(/Leaving Certificate Vocational Programme 2021|Link Modules Examination/);
    }
  });

  it('binds all ten audiovisual tasks to the original video and preserves skill/quality dependence', () => {
    const video = get('a1').videoMaterial;
    expect(video?.canonicalUrl).toBe('https://www.examinations.ie/archive/exampapers/2021/LC462CLP031EV.mov');
    for (const c of all.filter(c => c.id.startsWith('lcvp-2021-cl-a'))) {
      if (c.kind !== 'question') throw new Error(c.id);
      expect(c.videoMaterial).toEqual(video);
      expect(c.audioMaterial).toBeUndefined();
      expect(c.additionalSourceMaterials?.[0].pages).toEqual([3]);
    }
    expect(get('a6i').rows.map(r => r.marks)).toEqual([2, 2]);
    expect(get('a6i').rows[0].contextNote).toContain('Ability to work under pressure.');
    expect(get('a6i').rows[1].contextNote).toContain('Dependable');
    expect(get('a6ii').stem).toContain(get('a6i').questionText);
    expect(get('a6ii').rows[0].contextNote).toContain('SAME skill or quality');
    expect(get('a5').rows[0].group?.perOption).toBe(2);
    expect(get('a5').rows[0].group?.claimMax).toBe(2);
    expect(get('a5').rows[0].group?.options).toHaveLength(5);
    expect([get('a8i').totalMarks, get('a8ii').totalMarks]).toEqual([2, 4]);
  });

  it('keeps complete case definitions/marketing sections and restores matching challenge-solution marks', () => {
    expect(get('b1').rows[0].parts).toHaveLength(3);
    for (const name of ['Market research:', 'To invest:', 'Diversification:', 'Unique selling point:']) expect(get('b1').rows[0].contextNote).toContain(name);
    for (const name of ['Market Research Results:', 'Advertising/Promotion:', 'Marketing Budget:', 'Marketing Personnel:', 'Product:', 'Price', 'Place:']) expect(get('b2ii').rows[0].contextNote).toContain(name);
    expect(get('b2ii').rows[0].contextNote).toContain('Situated in a historic town');
    expect(get('b3i').totalMarks).toBe(4);
    expect(get('b3i').rows.map(r => r.parts?.map(p => p.marks))).toEqual([[1, 1], [1, 1]]);
    expect(get('b3i').rows[0].contextNote).toContain('Recession');
    expect(get('b1').stem).toContain('Grosvenor Hotel');
    expect(get('b1').sourceMaterial?.pages).toEqual([10]);
  });

  it('retains the whole personal placement profile and six-component original email', () => {
    expect(get('c2a').questionText).toContain('(i)');
    expect(get('c2a').questionText).toContain('(ii)');
    expect(get('c2a').rows.map(r => r.marks)).toEqual([2, 2]);
    expect(get('c2a').rows[1].parts).toHaveLength(2);
    expect(get('c2a').rows[1].contextNote).toContain('SAME named employer');
    const email = get('c2b');
    expect(email.rows.map(r => r.verbatim)).toEqual(['To: email address', 'Subject line', 'Salutation', 'Introduction', 'Reason for email', 'Closing']);
    expect(email.rows.map(r => r.marks)).toEqual(Array(6).fill(1));
    for (const value of ['principal@stsenansns.ie', 'Dear Mrs Murphy', 'XXXX School', 'Please find my CV attached.', 'Mark Doyle']) expect(email.rows[0].contextNote).toContain(value);
    expect(email.rows[0].contextNote).not.toContain('Summary of marks');
  });

  it('keeps the required questionnaire categories, layout components and complete eight-question model', () => {
    expect(get('c3b').rows.map(r => r.group?.claimMax)).toEqual([2, 2]);
    expect(get('c3b').rows.map(r => r.group?.options.length)).toEqual([6, 9]);
    expect(get('c3c').rows.map(r => r.marks)).toEqual([1, 1, 1, 5]);
    expect(get('c3c').rows[3].parts).toHaveLength(5);
    const guide = get('c3c').rows[3].contextNote;
    for (const phrase of ['Questionnaire', 'Male', 'Female', '12-15', '16-18', '>18', 'Any further comments']) expect(guide).toContain(phrase);
    expect(guide).toContain('Q.1 Male');
    expect(guide).toContain('Q.2 What age are you? 12-15');
    expect(guide).toContain('Q.6 What facilities');
    expect(guide).toContain('Q.7 Are you willing');
    expect(guide).toContain('Yes');
    expect(guide).toContain('No');
  });

  it('preserves the required diversity phrase, source-only definition units and all comparison columns', () => {
    expect(get('c4a').rows.map(r => r.marks)).toEqual([2, 2]);
    expect(get('c4a').rows[0].verbatim).toBe('mix of people');
    expect(get('c4a').rows[0].contextNote).toContain('underlines');
    expect(get('c4b').rows[0].parts?.map(p => p.permittedMarks)).toEqual([[0, 2], [0, 2]]);
    expect(get('c5b').rows.map(r => r.parts?.map(p => p.verbatim))).toEqual(Array(3).fill(['Entrepreneur', 'Business manager']));
    expect(get('c5b').rows[0].contextNote).toContain('long term → Focused on now and getting the job done/ short term');
    expect(get('c5b').rows[0].contextNote).toContain('Long working hours/difficult to take holidays → set holidays/hours of work');
  });

  it('retains all four enterprise-skill pools and the explicit all-or-nothing leadership reasons', () => {
    const c = get('c5c');
    expect(c.rows[0].parts).toHaveLength(3);
    for (const phrase of ['Communication skills', 'Time management skills', 'Decision-making skills', 'Creative skills', 'validity of a potential opportunity', 'Thinking of novel ways']) expect(c.rows[0].contextNote).toContain(phrase);
    expect(get('c6a').rows[0].parts?.map(p => p.permittedMarks)).toEqual([[0, 2], [0, 2]]);
    expect(get('c7a').rows[0].group?.perOption).toBe(2);
    expect(get('c7a').rows[0].group?.options).toHaveLength(10);
  });

  it('preserves all 18 Atlas identities, complete case regions and each canonical mapping', () => {
    expect(anchors.q.map(q => q.n)).toEqual(Array.from({ length: 18 }, (_, i) => String(i + 1)));
    expect(anchors.q.slice(11).map(q => [q.pP, q.endP])).toEqual([[18, 20], [21, 23], [24, 26], [27, 29], [30, 32], [33, 35], [36, 38]]);
    expect(anchors.q.find(q => q.n === '10')?.region.map(r => r.p)).toEqual([7, 8, 9]);
    expect(anchors.q.find(q => q.n === '16')?.region.map(r => r.p)).toEqual([18, 19]);
    expect(local.reviewedEnglish2021.markBankMappings).toHaveLength(45);
    expect(['c1a', 'c1b', 'c1c'].map(s => get(s).topicId)).toEqual(Array(3).fill('lcvp-link-modules-1-1'));
    expect([get('c1di').topicId, get('c1dii').topicId]).toEqual(Array(2).fill('lcvp-link-modules-0-4'));
    expect(['c2a', 'c2b', 'c2d'].map(s => get(s).topicId)).toEqual(Array(3).fill('lcvp-link-modules-0-3'));
    expect(get('c2c').topicId).toBe('lcvp-link-modules-0-0');
    expect(['c5a', 'c5b', 'c5c', 'c5di', 'c5dii'].map(s => get(s).topicId)).toEqual(Array(5).fill('lcvp-link-modules-1-0'));
    const paper = PAPER_TOPIC_TAGS.find(p => p.subjectId === 'link-modules' && p.year === 2021 && p.lang === 'ev' && p.fileid === 'LC462CLP000EV.pdf')!;
    for (const [n, rejected] of [['12', 'link-modules-common-2-an-enterprise-activity'], ['13', 'link-modules-common-1-career-investigation'], ['16', 'link-modules-common-2-local-business-enterprises']]) {
      const topics = browseTopicIdsForQuestion(paper, paper.q.find(q => q.n === n)!);
      expect(topics).not.toContain(rejected);
      expect(topics).toEqual(expect.arrayContaining(local.reviewedEnglish2021.originalAtlasTopicIds[n as keyof typeof local.reviewedEnglish2021.originalAtlasTopicIds]));
    }
    for (const mapping of local.reviewedEnglish2021.markBankMappings) {
      const topics = browseTopicIdsForQuestion(paper, paper.q.find(q => q.n === mapping.n)!);
      expect(topics, mapping.id).toEqual(expect.arrayContaining(mapping.atlasTopicIds));
      expect(topics.some(t => curriculumNodeIdsForExamTopic(t).includes(mapping.topicId)), mapping.id).toBe(true);
    }
  });
});
