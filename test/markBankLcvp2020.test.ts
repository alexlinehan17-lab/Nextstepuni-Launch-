import { describe, expect, it } from 'vitest';
import { CARDS } from '../components/MarkBank/cards/lcvp/common';
import { tariffReconciles } from '../types/markBank';
import review from '../scripts/markbank/authoring/lcvp/2020-cl-main-review.json';
import anchors from '../scripts/paper-trail/answers/2020/LC462CLP000EV.pdf.json';
import local from '../data/examTopics/link-modules-local-crosswalk.json';
import { PAPER_TOPIC_TAGS } from '../data/paperTrail/topicTags';
import { browseTopicIdsForQuestion } from '../components/PaperTrail/topics';
import { curriculumNodeIdsForExamTopic } from '../data/examTopics/registry';

const all = CARDS.filter(c => c.id.startsWith('lcvp-2020-cl-'));
const get = (suffix: string) => {
  const card = all.find(c => c.id === `lcvp-2020-cl-${suffix}`);
  if (!card || card.kind !== 'question') throw new Error(suffix);
  return card;
};

describe('LCVP 2020: original task pools, explicit held allocations and restored Atlas routes', () => {
  it('distinguishes 49 visual leaves from the 46 raw boundaries and 46 whole practice tasks', () => {
    expect(review.manualOriginalLeaves).toBe(49);
    expect(review.manualSectionLeaves).toEqual({ A: 11, B: 8, C: 30 });
    expect(review.rawCensusClassification.rawLeaves).toBe(46);
    expect(review.rawCensusClassification.manualOptions).toHaveLength(4);
    expect(review.candidateWrittenMarks).toBe(160);
    expect(all).toHaveLength(46);
    expect(all.reduce((sum, c) => sum + c.totalMarks, 0)).toBe(210);
    expect(all.map(c => c.id).sort()).toEqual(review.tasks.map(c => c.id).sort());
    expect(['c5c', 'c6di', 'c6dii'].map(s => get(s).totalMarks)).toEqual([8, 6, 3]);
    expect(get('c4ai').rows.map(r => r.marks)).toEqual([1, 1]);
    for (const c of all) {
      if (c.kind !== 'question') throw new Error(c.id);
      expect(tariffReconciles(c), c.id).toBe(true);
      expect(c.questionText + c.stem).not.toMatch(/Leaving Certificate Vocational Programme 2020|Link Modules Examination/);
    }
  });

  it('binds all eleven audiovisual tasks to the original MP4 and preserves both A1 alternatives', () => {
    const video = get('a1').videoMaterial;
    expect(video?.canonicalUrl).toBe('https://www.examinations.ie/archive/exampapers/2020/LC462CLP031EV.mp4');
    for (const c of all.filter(c => c.id.startsWith('lcvp-2020-cl-a'))) {
      if (c.kind !== 'question') throw new Error(c.id);
      expect(c.videoMaterial).toEqual(video);
      expect(c.audioMaterial).toBeUndefined();
      expect(c.additionalSourceMaterials?.[0].pages).toEqual([3]);
    }
    expect(get('a1').rows[0].group?.options).toEqual([
      'She knows a lot about the danger bees are facing.',
      'She is a member of the ‘Save the Bees Committee’.',
    ]);
    expect(get('a6ii').stem).toContain(get('a6i').questionText);
    expect(get('a8i').rows[0].contextNote).toContain('Makes decisions.');
    expect(get('a8i').rows[0].contextNote).toContain('comparison requirement');
  });

  it('retains all four B1 choices, the complete case and the paired promotion models', () => {
    expect(get('b1').rows[0].parts).toHaveLength(3);
    for (const name of ['Mentor:', 'Bookkeeping:', 'Sole trader:', 'Upskill:']) expect(get('b1').rows[0].contextNote).toContain(name);
    for (const term of ['(i) mentor', '(ii) bookkeeping', '(iii) sole trader', '(iv) upskill']) expect(get('b1').questionText).toContain(term);
    expect(get('b1').stem).toContain('Climate Entrepreneur');
    expect(get('b1').stem).toContain('600,000');
    expect(get('b1').sourceMaterial?.pages).toEqual([9]);
    const guide = get('b2ii').rows[0].contextNote;
    expect(guide).toContain('Visit trade shows → allows for public to view the product and get information.');
    expect(guide).toContain('Local sponsorship → local people will become more aware of his business/more likely to support his business.');
    expect(guide).toContain('Etc.');
    for (const name of ['Sole trader or PLC:', 'Professional indemnity:', 'Employers insurance:', 'Health and safety legislation:', 'Location:', 'Staff requirements:']) expect(get('b3i').rows[0].contextNote).toContain(name);
    expect(get('b3i').rows[0].contextNote).toContain('OTHER THAN promotion');
  });

  it('keeps all four underlined advert terms and the shared interview presentation context', () => {
    expect(get('c1a').rows[0].parts).toHaveLength(2);
    for (const term of ['Problem Solving:', 'Flexible Working Hours:', 'Referees:', 'Equal Opportunities Employer:']) expect(get('c1a').rows[0].contextNote).toContain(term);
    for (const suffix of ['c1a', 'c1b', 'c1c', 'c1di', 'c1dii']) {
      expect(get(suffix).sourceMaterial?.pages).toEqual([16]);
      expect(get(suffix).stem).toContain('hr@manraytechnologies.ie');
    }
    for (const suffix of ['c1di', 'c1dii']) expect(get(suffix).stem).toContain('As part of the interview process');
  });

  it('preserves the two-column quality pool, required category mix and binary explanation ladders', () => {
    expect(get('c2aii').rows[0].group?.options).toEqual(['Willing to take a risk.', 'Focused.', 'Determined.', 'Constantly learning.', 'Hard working.', 'Motivated.', 'Persistent.', 'Decisive.']);
    expect(get('c2b').rows[0].group?.perOption).toBe(2);
    expect(get('c2b').rows[0].group?.claimMax).toBe(2);
    expect(get('c2c').rows[0].contextNote).toContain('advantages AND disadvantages');
    expect(get('c2c').rows[0].contextNote).toContain('no fixed category quota');
    expect(get('c4d').rows.map(r => r.parts?.map(p => p.permittedMarks))).toEqual(Array(3).fill([[0, 1], [0, 2]]));
  });

  it('keeps both contradictory tasks whole and entirely unpriced instead of inventing a quota', () => {
    expect(all.filter(c => c.kind === 'question' && c.tariffModel.kind === 'questionTotal').map(c => c.id).sort()).toEqual(['lcvp-2020-cl-c3a', 'lcvp-2020-cl-c5ai']);
    expect(get('c3a').rows).toHaveLength(8);
    expect(get('c5ai').rows).toHaveLength(7);
    for (const suffix of ['c3a', 'c5ai']) {
      const card = get(suffix);
      expect(card.tariffModel.kind).toBe('questionTotal');
      for (const row of card.rows) {
        expect(row.marks).toBeNull();
        expect(row.parts).toBeUndefined();
        expect(row.group).toBeUndefined();
      }
      expect(card.rows[0].contextNote).toContain('confidence review only');
    }
    expect(get('c3a').rows[0].contextNote).toContain('Four valid points; 2 x 2 mark (1+1)');
    expect(get('c5ai').rows[0].contextNote).toContain('Three points; 2 x 1 mark');
    expect(review.scoringScope).toMatchObject({ pricedTaskMarks: 204, heldWholeTaskMarks: 6, heldTasks: 2 });
  });

  it('restores the full email and separately priced plan tasks with all coherent source profiles', () => {
    expect(get('c5c').rows.map(r => r.verbatim)).toEqual(['To: email address', 'Subject line', 'Opening salutation', 'Purpose of email', 'Three points of information about the visit', 'Closing: Yours sincerely']);
    expect(get('c5c').rows.map(r => r.marks)).toEqual([1, 1, 1, 1, 3, 1]);
    expect(get('c5d').rows[0].contextNote).toContain('Review Aims/Objectives:');
    expect(get('c5d').rows[0].contextNote).toContain('Did they get the information they needed?');
    expect(get('c6c').rows[0].contextNote).toContain('Evaluate the success by comparing your business plan to your progress.');
    expect(get('c6dii').stem).toContain(get('c6di').questionText);
    for (const suffix of ['c6di', 'c6dii']) {
      for (const label of ['Marketing/Market Research:', 'Finance:', 'Staff/Personnel/HR:', 'Production:', 'Location/Premises:']) expect(get(suffix).rows[0].contextNote).toContain(label);
    }
    expect(get('c6dii').rows[0].contextNote).toContain('SAME THREE items');
    expect(get('c3dii').stem).toContain(get('c3di').questionText);
  });

  it('retains all 17 original anchors and restores the three absent direct-runtime identities', () => {
    expect(anchors.q.map(q => q.n)).toEqual(Array.from({ length: 17 }, (_, i) => String(i + 1)));
    expect(anchors.q.slice(11).map(q => [q.pP, q.endP])).toEqual([[16, 18], [19, 21], [22, 24], [25, 27], [28, 30], [31, 33]]);
    expect(anchors.q.find(q => q.n === '11')?.region.map(r => r.p)).toEqual([8, 9]);
    expect(anchors.q.find(q => q.n === '16')?.region.map(r => r.p)).toEqual([17, 18, 19]);
    expect(review.originalAtlasMemberships.existingRuntimeIdentities).toBe(14);
    expect(review.originalAtlasMemberships.restoredRuntimeIdentities).toEqual(['10', '11', '16']);
    expect(local.reviewedEnglish2020.markBankMappings).toHaveLength(46);
    const paper = PAPER_TOPIC_TAGS.find(p => p.subjectId === 'link-modules' && p.year === 2020 && p.lang === 'ev' && p.fileid === 'LC462CLP000EV.pdf')!;
    for (const [n, original] of Object.entries(local.reviewedEnglish2020.originalAtlasTopicIds)) {
      expect(browseTopicIdsForQuestion(paper, paper.q.find(q => q.n === n)!)).toEqual(expect.arrayContaining(original));
    }
    for (const mapping of local.reviewedEnglish2020.markBankMappings) {
      const topics = browseTopicIdsForQuestion(paper, paper.q.find(q => q.n === mapping.n)!);
      expect(topics, mapping.id).toEqual(expect.arrayContaining(mapping.atlasTopicIds));
      expect(topics.some(t => curriculumNodeIdsForExamTopic(t).includes(mapping.topicId)), mapping.id).toBe(true);
    }
    expect(['c3a', 'c3b', 'c3c', 'c3di', 'c3dii'].map(s => get(s).topicId)).toEqual(Array(5).fill('lcvp-link-modules-0-3'));
    expect(['c4ai', 'c4aii', 'c4b'].map(s => get(s).topicId)).toEqual(Array(3).fill('lcvp-link-modules-0-2'));
    expect(['c6a', 'c6b', 'c6c', 'c6di', 'c6dii'].map(s => get(s).topicId)).toEqual(Array(5).fill('lcvp-link-modules-1-3'));
  });
});
