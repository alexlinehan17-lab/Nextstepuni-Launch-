import { describe, expect, it } from 'vitest';
import { CARDS } from '../components/MarkBank/cards/lcvp/common';
import { tariffReconciles } from '../types/markBank';
import authored from '../scripts/markbank/authored/lcvp.json';
import review from '../scripts/markbank/authoring/lcvp/2015-cl-main-review.json';
import anchors from '../scripts/paper-trail/answers/2015/LC462CLP000EV.pdf.json';
import local from '../data/examTopics/link-modules-local-crosswalk.json';
import { PAPER_TOPIC_TAGS } from '../data/paperTrail/topicTags';
import { browseTopicIdsForQuestion } from '../components/PaperTrail/topics';
import { curriculumNodeIdsForExamTopic } from '../data/examTopics/registry';

const all = CARDS.filter(c => c.id.startsWith('lcvp-2015-cl-'));
const get = (suffix: string) => {
  const card = all.find(c => c.id === `lcvp-2015-cl-${suffix}`);
  if (!card || card.kind !== 'question') throw new Error(suffix);
  return card;
};
const pool = (suffix: string, index = 0) => {
  const row = get(suffix).rows[index];
  return row.group?.options ?? row.contextNote!.split('Complete original guidance: ')[1].split(' | ');
};

describe('LCVP 2015: all original tasks, choices and Atlas identities', () => {
  it('retains all 43 printed tasks and every emitted authored field', () => {
    expect(review.manualOriginalLeaves).toBe(43);
    expect(review.manualPricedTasks).toBe(43);
    expect(review.manualSectionTasks).toEqual({ A: 8, B: 6, C: 29 });
    expect(review.paperPrintedTariffUnits).toBe(35);
    expect(review.rawReaderAudit.capturedTariffSum).toBe(44);
    expect(review.candidateWrittenMarks).toBe(160);
    expect(review.originalMarkBankCards).toBe(0);
    expect(all).toHaveLength(43);
    expect(all.reduce((sum, c) => sum + c.totalMarks, 0)).toBe(210);
    const expected = authored.filter(c => c.year === 2015);
    expect(all.map(c => c.id).sort()).toEqual(expected.map(c => c.id).sort());
    for (const source of expected) {
      const emitted = get(source.id.replace('lcvp-2015-cl-', ''));
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

  it('keeps the original audiovisual binding, binary tariffs and complete compound tasks', () => {
    const video = get('a1').videoMaterial;
    expect(video?.canonicalUrl).toBe('https://www.examinations.ie/archive/exampapers/2015/LC462CLPO31EV.mp4');
    for (const card of all.filter(c => c.section === 'A')) {
      if (card.kind !== 'question') throw new Error(card.id);
      expect(card.videoMaterial).toEqual(video);
      expect(card.audioMaterial).toBeUndefined();
      expect(card.additionalSourceMaterials?.[0].pages).toEqual([2]);
    }
    expect(get('a2').questionText).toBe('Why was this type of business suited to Sylvia?');
    expect(get('a2').rows[0].contextNote).toContain('no prescribed count of reasons');
    expect(pool('a2')).toHaveLength(3);
    expect(get('a3').rows.map(r => r.marks)).toEqual([1, 2]);
    expect(get('a3').rows[1].group).toMatchObject({ claimMax: 1, perOption: 2 });
    expect(pool('a3', 1)).toHaveLength(4);
    expect(get('a7').rows.map(r => [r.group?.claimMax, r.group?.perOption])).toEqual([[1, 2], [2, 2]]);
    expect([pool('a7', 0).length, pool('a7', 1).length]).toEqual([4, 5]);
    expect(get('a5').sourceMaterial?.pages).toEqual([4, 5]);
    for (const [suffix, count] of [['a4', 2], ['a5', 3], ['a6', 4]] as const) {
      expect(get(suffix).rows[0].group).toMatchObject({ claimMax: 2, perOption: 2 });
      expect(pool(suffix)).toHaveLength(count);
    }
    expect(pool('a8')).toHaveLength(4);
    for (const phrase of ['General management', 'Corporate Organisation', 'Finance', 'Business plan', 'Marketing', 'Website planning and design']) expect(pool('a8')[3]).toContain(phrase);
  });

  it('retains the complete case, five-term choice and both policy alternatives without an invented split', () => {
    for (const suffix of ['b1', 'b2i', 'b2ii', 'b2iii', 'b3i', 'b3ii']) {
      const card = get(suffix);
      expect(card.stem).toContain(get('b1').stem);
      expect(card.stem!.length).toBeGreaterThan(3000);
      for (const phrase of ['Robert', 'Maria', 'nominal rent', 'SWOT', 'Careers Programme']) expect(card.stem).toContain(phrase);
      expect(card.sourceMaterial?.pages).toEqual([8]);
    }
    expect(get('b1').questionText.match(/•/g)).toHaveLength(5);
    expect(pool('b1')).toHaveLength(5);
    expect(get('b1').rows[0].parts).toHaveLength(3);
    const held = get('b2ii');
    expect(held.questionText).toBe('Outline a corporate social responsibility policy implemented by Robert and Maria in Recruit Me Ltd.');
    expect(held.tariffModel.kind).toBe('questionTotal');
    expect(held.totalMarks).toBe(4);
    expect(held.rows).toHaveLength(2);
    for (const row of held.rows) {
      expect(row.marks).toBeNull();
      expect(row.parts).toBeUndefined();
      expect(row.group).toBeUndefined();
      expect(row.permittedMarks).toBeUndefined();
    }
    expect(held.rows[0].verbatim).toContain('2m (0/2)');
    expect(held.rows[0].verbatim).toContain('2 @ 1m');
    expect(held.rows[0].contextNote).toContain('no printed internal allocation');
    expect(held.rows[1].verbatim).toMatch(/^They offer support to new start-up enterprises/);
    expect(held.rows[1].contextNote).toMatch(/^or — Complete second policy alternative\./);
    for (const phrase of ['fully serviced desks', 'printing, broadband & communications', 'legal and tax issues']) expect(held.rows[1].verbatim).toContain(phrase);
    for (const suffix of ['b2i', 'b3i']) expect(get(suffix).rows[0].parts?.map(p => p.permittedMarks)).toEqual([[0, 2], [0, 2]]);
    expect(get('b2iii').rows[0].group).toMatchObject({ claimMax: 2, perOption: 2 });
    expect(pool('b2iii')).toHaveLength(4);
    expect(pool('b3ii')).toHaveLength(6);
    const priced = all.filter(c => c.kind === 'question' && c.tariffModel.kind === 'fixed');
    expect(priced).toHaveLength(42);
    expect(priced.reduce((sum, c) => sum + c.totalMarks, 0)).toBe(206);
  });

  it('preserves every paired table cell and all six evaluation methods across the page continuation', () => {
    expect(get('c1c').rows[0].contextNote).toContain('specific to the activity named in part (a)');
    expect(pool('c1d')).toHaveLength(6);
    expect(pool('c1d')[5]).toContain('To measure the results against the aims/objectives.');
    for (const row of get('c1d').rows) expect(row.parts?.map(p => p.verbatim)).toEqual(['Method', 'Explanation', 'Why']);
    expect(get('c2b').questionText).toBe('Explain how a local voluntary body differs from a commercial business.');
    expect(pool('c2b')).toEqual([
      'Rely on people who work for nothing e.g. volunteers. — Employ staff and pay wages to workers.',
      'Non profit making/concerned with social issues. — Motivated by making profit.',
      'They are financed by donations/grants/fundraising. — Raise funds through loans, investors.',
      'They are accountable to those who avail of services/clients. — They are accountable to shareholders/owners.',
      'Aim is to help others. — Aim is to produce a product/supply service.',
      'Benefits the community. — Benefits owners/investors',
    ]);
    expect(get('c2b').rows[0].parts?.map(p => p.permittedMarks)).toEqual([[0, 1, 2], [0, 1, 2], [0, 1, 2]]);
    for (const [suffix, count] of [['c1b', 6], ['c1c', 6], ['c2c', 6], ['c2d', 8], ['c3a', 7], ['c3c', 6], ['c3d', 5], ['c4aii', 9], ['c4b', 7], ['c4cii', 9], ['c4d', 6], ['c5bii', 7], ['c6a', 8], ['c6bii', 8], ['c6c', 9], ['c6d', 9]] as const) expect(pool(suffix), suffix).toHaveLength(count);
  });

  it('keeps compulsory markers, two full pathways and the explicit ICT/questionnaire components', () => {
    const letter = get('c3b').rows[0];
    expect(letter.parts?.map(p => p.marks)).toEqual([1, 1, 1, 2, 1, 2, 2]);
    for (const part of letter.parts!) expect(part.permittedMarks).toEqual([0, part.marks]);
    expect(letter.parts?.[5].verbatim).toBe('Closing paragraph (*CV enc)');
    expect(letter.contextNote).toContain('* compulsory item: CV enclosure');
    expect(get('c4ci').rows[0].contextNote).toContain('* compulsory item');
    expect(get('c4ci').rows[0].contextNote).toContain('A written document*/between an employer and employee');
    expect(get('c5c').rows.map(r => r.marks)).toEqual([3, 3]);
    for (const row of get('c5c').rows) expect(row.parts?.map(p => p.marks)).toEqual([1, 2]);
    expect(get('c5d').rows.map(r => r.marks)).toEqual([6, 6]);
    for (const row of get('c5d').rows) {
      expect(row.parts?.map(p => p.verbatim)).toEqual(['Course Title', 'Duration', 'College name/location', 'Entry points/requirements', 'Details of course', 'End qualification/name of qualification']);
      expect(row.parts?.map(p => p.marks)).toEqual([1, 1, 1, 1, 1, 1]);
    }
    for (const suffix of ['c5bii', 'c5c', 'c5d']) expect(get(suffix).stem).toContain(get('c5bi').questionText);
    expect(get('c6bii').questionText).toContain('other than questionnaires');
    for (const [suffix, labels] of [['c6c', ['Statement', 'Disadvantage']], ['c6d', ['Method', 'Use']]] as const) {
      expect(get(suffix).rows).toHaveLength(4);
      for (const row of get(suffix).rows) expect(row.parts?.map(p => p.verbatim)).toEqual(labels);
    }
    expect(pool('c6d')[6]).toContain('Speadsheets');
    expect(pool('c6d')[6]).toContain('fianancial statements');
  });

  it('retains all 17 physical identities and old memberships while restoring seven missing runtime anchors', () => {
    expect(review.originalAtlasMemberships.preLaneBaseline).toBe('ecd7ff846');
    expect(review.originalAtlasMemberships.preLaneEqualityVerified).toBe(true);
    expect(anchors.paperFileid).toBe('LC462CLP000EV.pdf');
    expect(anchors.schemeFileid).toBe('LC462CLP000EV.pdf');
    expect(anchors.q.map(q => q.n)).toEqual(Array.from({ length: 17 }, (_, i) => String(i + 1)));
    expect(anchors.q.slice(11).map(q => [q.pP, q.endP])).toEqual([[14, 16], [17, 19], [20, 22], [23, 25], [26, 28], [29, 31]]);
    expect(anchors.q.find(q => q.n === '5')?.endP).toBe(5);
    expect(anchors.q.find(q => q.n === '10')?.endP).toBe(11);
    expect(anchors.q.find(q => q.n === '11')?.endP).toBe(12);
    expect(anchors.q.find(q => q.n === '16')?.region.map(r => r.p)).toEqual([14]);
    expect(anchors.q.find(q => q.n === '17')?.region.map(r => r.p)).toEqual([15, 16]);
    const crosswalk = local.reviewedEnglish2015;
    expect(crosswalk.markBankMappings).toHaveLength(43);
    expect(Object.keys(crosswalk.originalAtlasTopicIds)).toHaveLength(10);
    const paper = PAPER_TOPIC_TAGS.find(p => p.subjectId === 'link-modules' && p.year === 2015 && p.lang === 'ev' && p.fileid === 'LC462CLP000EV.pdf')!;
    expect(paper.q).toHaveLength(17);
    for (const [n, topics] of Object.entries(crosswalk.originalAtlasTopicIds)) expect(browseTopicIdsForQuestion(paper, paper.q.find(q => q.n === n)!)).toEqual(expect.arrayContaining(topics));
    for (const [n, nodes] of Object.entries(review.originalAtlasMemberships.canonicalWaveTopics)) expect(crosswalk.canonicalTopicIdsByQuestion[n as keyof typeof crosswalk.canonicalTopicIdsByQuestion]).toEqual(expect.arrayContaining(nodes));
    for (const mapping of crosswalk.markBankMappings) {
      const topics = browseTopicIdsForQuestion(paper, paper.q.find(q => q.n === mapping.n)!);
      expect(topics, mapping.id).toEqual(expect.arrayContaining(mapping.atlasTopicIds));
      expect(topics.some(t => curriculumNodeIdsForExamTopic(t).includes(mapping.topicId)), mapping.id).toBe(true);
    }
  });
});
