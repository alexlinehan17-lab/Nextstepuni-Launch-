import { describe, expect, it } from 'vitest';
import { CARDS } from '../components/MarkBank/cards/lcvp/common';
import { tariffReconciles } from '../types/markBank';
import authored from '../scripts/markbank/authored/lcvp.json';
import review from '../scripts/markbank/authoring/lcvp/2014-cl-main-review.json';
import anchors from '../scripts/paper-trail/answers/2014/LC462CLP000EV.pdf.json';
import local from '../data/examTopics/link-modules-local-crosswalk.json';
import { PAPER_TOPIC_TAGS } from '../data/paperTrail/topicTags';
import { browseTopicIdsForQuestion } from '../components/PaperTrail/topics';
import { curriculumNodeIdsForExamTopic } from '../data/examTopics/registry';

const all = CARDS.filter(c => c.id.startsWith('lcvp-2014-cl-'));
const get = (suffix: string) => {
  const card = all.find(c => c.id === `lcvp-2014-cl-${suffix}`);
  if (!card || card.kind !== 'question') throw new Error(suffix);
  return card;
};
const pool = (suffix: string, index = 0) => {
  const row = get(suffix).rows[index];
  return row.group?.options ?? row.contextNote!.split('Complete original guidance: ')[1].split(' | ');
};

describe('LCVP 2014: all original tasks, choices and Atlas identities', () => {
  it('retains all 39 printed tasks and every emitted authored field', () => {
    expect(review.manualOriginalLeaves).toBe(39);
    expect(review.manualPricedTasks).toBe(39);
    expect(review.manualSectionTasks).toEqual({ A: 8, B: 5, C: 26 });
    expect(review.paperPrintedTariffUnits).toBe(35);
    expect(review.rawReaderAudit.capturedTariffSum).toBe(44);
    expect(review.candidateWrittenMarks).toBe(160);
    expect(review.originalMarkBankCards).toBe(0);
    expect(all).toHaveLength(39);
    expect(all.reduce((sum, c) => sum + c.totalMarks, 0)).toBe(210);
    const expected = authored.filter(c => c.year === 2014);
    expect(all.map(c => c.id).sort()).toEqual(expected.map(c => c.id).sort());
    for (const source of expected) {
      const emitted = get(source.id.replace('lcvp-2014-cl-', ''));
      expect(tariffReconciles(emitted), source.id).toBe(true);
      expect(emitted.questionText, source.id).toBe(source.questionText);
      expect(emitted.stem ?? '', source.id).toBe(source.stem ?? '');
      expect(`${emitted.questionText} ${emitted.stem ?? ''}`, source.id).not.toMatch(/Office use|For Examiner|Page \d+ of 32|\uf0b7|\. \. 4/);
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

  it('retains exact video identity, all audiovisual models and binary two-mark responses', () => {
    const video = get('a1').videoMaterial;
    expect(video?.canonicalUrl).toBe('https://www.examinations.ie/archive/exampapers/2014/LC462CLP031EV.mp4');
    for (const card of all.filter(c => c.section === 'A')) {
      if (card.kind !== 'question') throw new Error(card.id);
      expect(card.videoMaterial).toEqual(video);
      expect(card.audioMaterial).toBeUndefined();
      expect(card.additionalSourceMaterials?.[0].pages).toEqual([2]);
    }
    expect(get('a1').rows[0]).toMatchObject({ verbatim: 'Student Social Enterprise Awards', marks: 2 });
    for (const [suffix, count] of [['a2', 3], ['a3', 4], ['a4', 5], ['a5', 6], ['a6', 8], ['a7', 4], ['a8', 6]] as const) expect(pool(suffix)).toHaveLength(count);
    expect(get('a6').rows[0].group).toMatchObject({ claimMax: 2, perOption: 2 });
    expect(get('a7').rows[0].group).toMatchObject({ claimMax: 3, perOption: 2 });
    expect(pool('a4')[1]).toContain('€2,000');
    expect(pool('a8')[3]).toContain('career options + valid expansion');
    expect(pool('a8')[4]).toContain('team, financial, marketing');
    expect(get('a5').sourceMaterial?.pages).toEqual([4, 5]);
  });

  it('keeps the complete case and chart before reveal, distinct population/visitor figures and all model pools', () => {
    for (const suffix of ['b1', 'b2i', 'b2ii', 'b3i', 'b3ii']) {
      const card = get(suffix);
      expect(card.stem).toBe(get('b1').stem);
      for (const phrase of ['COROBAWN SUMMER FESTIVAL', 'population of 4,000', 'nearly 5,000 visitors',
        'The committee, representing the local community,', 'Exploring Your Roots in Corobawn',
        'Great Western Greenway', 'Wild Atlantic Way', 'Visiting Family 6%', 'Hiking/Hill Walking 38%', 'Golf 24%', 'Gathering Festival 32%']) expect(card.stem).toContain(phrase);
      expect(card.sourceMaterial?.pages).toEqual([8]);
      expect(card.sourceMaterial?.title).toContain('chart');
    }
    expect(review.caseBookletMatchesPaper).toBe(false);
    for (const [suffix, count] of [['b1', 5], ['b2i', 6], ['b2ii', 8], ['b3i', 8], ['b3ii', 7]] as const) expect(pool(suffix)).toHaveLength(count);
    expect(pool('b2ii')[2]).toContain('special promotions');
    expect(pool('b2ii')[2]).toContain('packed lunches for walkers');
    expect(get('b1').topicId).toBe('lcvp-link-modules-1-1');
  });

  it('preserves whole matched profiles and indivisible explanation components', () => {
    for (const suffix of ['c1c', 'c2c', 'c6c']) {
      expect(get(suffix).rows.map(r => r.marks)).toEqual([3, 3, 3]);
      for (const row of get(suffix).rows) expect(row.parts?.map(p => p.permittedMarks)).toEqual([[0, 1], [0, 1, 2]]);
    }
    expect(pool('c1c')).toHaveLength(2);
    expect(pool('c1c')[1]).toContain('Must be relevant to the career.');
    expect(get('c2c').rows[0].contextNote).toContain('OTHER THAN Link Modules');
    for (const suffix of ['c1d', 'c3d']) {
      expect(get(suffix).rows).toHaveLength(3);
      for (const row of get(suffix).rows) expect(row.parts?.map(p => p.permittedMarks)).toEqual([[0, 1], [0, 2]]);
    }
    expect(get('c5a').rows[0].parts?.map(p => p.permittedMarks)).toEqual([[0, 1], [0, 2]]);
    for (const suffix of ['c1b', 'c1c', 'c1d']) expect(get(suffix).stem).toContain(get('c1a').questionText);
    for (const suffix of ['c2b', 'c2c', 'c2d']) expect(get(suffix).stem).toContain(get('c2a').questionText);
    for (const [suffix, count] of [['c1b', 6], ['c1d', 7], ['c2b', 7], ['c2d', 7], ['c3b', 10], ['c3c', 7], ['c3d', 10], ['c4b', 8], ['c4c', 4], ['c5b', 7], ['c5di', 4], ['c5dii', 5], ['c6b', 8], ['c6c', 8]] as const) expect(pool(suffix)).toHaveLength(count);
  });

  it('keeps compulsory agenda election, every nested resource example and complete feedback task', () => {
    const rows = get('c4a').rows;
    expect(rows.map(r => r.marks)).toEqual([1, 1, 4]);
    expect(rows[0].verbatim).toBe('Heading');
    expect(rows[1].verbatim).toBe('Election of officers* (Chairperson/Managing Director/Secretary/Treasurer)');
    expect(rows[1].contextNote).toContain('* Compulsory item');
    expect(rows[2].group).toMatchObject({ claimMax: 4, perOption: 1 });
    expect(rows[2].group?.options).toEqual(['Draw up a plan of work', 'Finance', 'Permission from Principal', 'Assigning tasks/roles', 'Date/time of the next meeting', 'AOB']);
    for (const row of get('c4c').rows) expect(row.parts?.map(p => p.verbatim)).toEqual(['Resource', 'Explanation']);
    for (const phrase of ['Skilled team members', 'Teachers', 'Parents', 'General public']) expect(pool('c4c')[0]).toContain(phrase);
    for (const phrase of ['Wood, glue nails', 'Tools & Equipment', 'Specialist rooms']) expect(pool('c4c')[1]).toContain(phrase);
    expect(get('c4d').totalMarks).toBe(9);
    expect(get('c4d').rows.map(r => r.marks)).toEqual([3, 6]);
    expect(pool('c4d', 1)).toHaveLength(6);
    expect(pool('c4d', 1)[5]).toContain('Brainstorming in the class');
  });

  it('requires all four SWOT categories and explained traits while retaining literal source spelling', () => {
    const swot = get('c5cii');
    expect(swot.questionText).toBe('Complete a SWOT analysis of the voluntary group/organisation referred to in part (a).');
    expect(swot.rows.map(r => r.id)).toEqual(['strengths', 'weaknesses', 'opportunities', 'threats']);
    expect(swot.rows.map(r => r.marks)).toEqual([2, 2, 2, 2]);
    expect([0, 1, 2, 3].map(i => pool('c5cii', i).length)).toEqual([4, 3, 4, 3]);
    for (const row of swot.rows) {
      expect(row.permittedMarks).toEqual([0, 1, 2]);
      expect(row.contextNote).toContain('No marks for headings. No repetition of points.');
      expect(row.contextNote).toContain('EACH category');
    }
    expect(pool('c5cii', 3)[2]).toBe('Immigration/no volunteers');
    expect(swot.stem).toContain(get('c5a').questionText);
    expect(pool('c6a')).toEqual(['Hard working', 'Innovative/creative', 'Risk taker', 'Communicator', 'Adaptible', 'Flexible', 'Self Confident']);
    expect(get('c6a').rows[0].contextNote).toContain('Each must be explained for the mark');
    expect(get('c6a').rows[0].contextNote).toContain('A bare trait name receives no mark');
    expect(get('c6a').rows[0].parts?.map(p => p.permittedMarks)).toEqual([[0, 1], [0, 1], [0, 1], [0, 1]]);
    expect(get('c6a').rows[0].group).toBeUndefined();
  });

  it('retains both full cells of all six entrepreneur/manager contrasts', () => {
    expect(pool('c6d')).toEqual([
      'Comes up with an idea/sets up the business — Implements entrepeneur’s idea/runs the business on a daily basis',
      'Owns the business — Is an employee of the business',
      'Takes a risk — Manages the risk/takes no personal/monetary risk',
      'May make a large profit or make a loss — Earns a set salary',
      'May not have specific skills — Usually have a skill or qualification in management',
      'Long term planning — Implements short term plan',
    ]);
    expect(get('c6d').rows[0].parts?.map(p => p.permittedMarks)).toEqual([[0, 1, 2], [0, 1, 2], [0, 1, 2]]);
    expect(all.every(c => c.kind === 'question' && c.tariffModel.kind === 'fixed')).toBe(true);
    expect(review.heldWholeTaskMarks).toBe(0);
    expect(review.pricedMarks).toBe(210);
  });

  it('preserves every Atlas identity and direct bucket with only the approved B1 taxonomy correction', () => {
    expect(review.originalAtlasMemberships.preLaneBaseline).toBe('ecd7ff846');
    expect(review.originalAtlasMemberships.preLaneEqualityVerified).toBe(true);
    expect(anchors.q.map(q => q.n)).toEqual(Array.from({ length: 17 }, (_, i) => String(i + 1)));
    expect(anchors.q.slice(11).map(q => [q.pP, q.endP])).toEqual([[14, 16], [17, 19], [20, 22], [23, 25], [26, 28], [29, 31]]);
    expect(anchors.q.find(q => q.n === '5')?.endP).toBe(5);
    expect(anchors.q.find(q => q.n === '10')?.endP).toBe(11);
    expect(anchors.q.find(q => q.n === '11')?.endP).toBe(12);
    expect(anchors.q.slice(11).map(q => q.region.map(r => r.p))).toEqual([[8], [9], [10], [11, 12], [12, 13], [14]]);
    const crosswalk = local.reviewedEnglish2014;
    expect(crosswalk.markBankMappings).toHaveLength(39);
    expect(Object.keys(crosswalk.originalAtlasTopicIds)).toHaveLength(17);
    expect(crosswalk.atlasTopicCorrections).toEqual(review.atlasTopicCorrections);
    expect(review.originalAtlasMemberships.canonicalWaveTopics['9']).toEqual(['lcvp-link-modules-1-4']);
    expect(crosswalk.canonicalTopicIdsByQuestion['9']).toEqual(['lcvp-link-modules-1-1']);
    const paper = PAPER_TOPIC_TAGS.find(p => p.subjectId === 'link-modules' && p.year === 2014 && p.lang === 'ev' && p.fileid === 'LC462CLP000EV.pdf')!;
    expect(paper.q).toHaveLength(17);
    for (const [n, topics] of Object.entries(crosswalk.originalAtlasTopicIds)) expect(browseTopicIdsForQuestion(paper, paper.q.find(q => q.n === n)!)).toEqual(expect.arrayContaining(topics));
    for (const [n, nodes] of Object.entries(review.originalAtlasMemberships.canonicalWaveTopics)) {
      if (n !== '9') expect(crosswalk.canonicalTopicIdsByQuestion[n as keyof typeof crosswalk.canonicalTopicIdsByQuestion]).toEqual(expect.arrayContaining(nodes));
    }
    for (const mapping of crosswalk.markBankMappings) {
      const topics = browseTopicIdsForQuestion(paper, paper.q.find(q => q.n === mapping.n)!);
      expect(topics, mapping.id).toEqual(expect.arrayContaining(mapping.atlasTopicIds));
      expect(topics.some(t => curriculumNodeIdsForExamTopic(t).includes(mapping.topicId)), mapping.id).toBe(true);
    }
  });
});

