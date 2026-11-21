/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 *
 * The sixteen small languages in the Topic Atlas: Part I is Atlas 1-6, and Parts II and III, which each restart at
 * Q1, are numbered by the part ("II1", "III2"; "II" for a part printed as one unnumbered question). Every card reaches
 * its own printed question (test/atlasModelChecks.test.ts checks all of them); these pin the rule's own cases and
 * the label a student sees for such a row before its crop loads.
 */
import { describe, expect, it } from 'vitest';
import { addressContext, atlasAddress } from '../scripts/atlas-model/cardAtlasAddress';
import { questionLabel, topicsForPaper } from '../components/PaperTrail/topics';
import type { SecCard } from '../types/markBank';
import { CARDS as CZECH } from '../components/MarkBank/cards/czech/higher';
import { CARDS as DANISH } from '../components/MarkBank/cards/danish/higher';
import { CARDS as DUTCH } from '../components/MarkBank/cards/dutch/higher';
import { CARDS as MALTESE } from '../components/MarkBank/cards/maltese/higher';
import { CARDS as MODERN_GREEK } from '../components/MarkBank/cards/modern-greek/higher';
import { CARDS as SLOVENIAN } from '../components/MarkBank/cards/slovenian/higher';

const rowOf = (cards: SecCard[], id: string) => {
  const card = cards.find(c => c.id === id);
  expect(card, id).toBeDefined();
  const a = atlasAddress(card!, card!.subjectId, addressContext(cards));
  expect('fail' in a, id).toBe(false);
  return 'fail' in a ? null : a.cands[0];
};

describe('small languages: the Atlas row of each part', () => {
  it('numbers Parts II and III by the part', () => {
    expect(rowOf(DUTCH, 'nld-2019-hl-ii-1')).toBe('II1');
    expect(rowOf(DUTCH, 'nld-2019-hl-iii-2')).toBe('III2');
    // Modern Greek prints its parts as 1, 2, 3.
    expect(rowOf(MODERN_GREEK, 'mgr-2014-hl-3-1')).toBe('III1');
    // Czech prints Part II as one unnumbered question.
    expect(rowOf(CZECH, 'cs-2010-hl-ii')).toBe('II');
    // Part I keeps its printed number.
    expect(rowOf(DUTCH, 'nld-2019-hl-i-3')).toBe('3');
  });

  it('keeps the older rows that list a whole part, rather than renumbering them', () => {
    expect(rowOf(DANISH, 'dan-2018-hl-ii-1')).toBe('7');
    expect(rowOf(DANISH, 'dan-2018-hl-iii-1')).toBe('8');
    expect(rowOf(SLOVENIAN, 'slv-2018-hl-ii-1')).toBe('7');
    expect(rowOf(SLOVENIAN, 'slv-2024-hl-ii-1')).toBe('7');
    expect(rowOf(SLOVENIAN, 'slv-2018-hl-iii-2')).toBe('III2');
  });

  it('follows the scheme\'s Part I numbering where Maltese 2019 prints a question with no number', () => {
    expect(rowOf(MALTESE, 'mlt-2019-hl-i-1-a')).toBe('1');
    expect(rowOf(MALTESE, 'mlt-2019-hl-i-1a')).toBe('2');
    expect(rowOf(MALTESE, 'mlt-2019-hl-i-2')).toBe('3');
    expect(rowOf(MALTESE, 'mlt-2019-hl-i-5')).toBe('6');
  });

  it('lists the rows on the Atlas paper, and a sitting that had no Atlas paper now has one', () => {
    const dutch2019 = topicsForPaper('dutch', 2019, 'higher', 'ev', 'LC017ALP000EV.pdf');
    expect(dutch2019?.q.map(q => q.n)).toEqual(['1', '2', '3', '4', '5', '6', 'II1', 'III1', 'III2']);
  });
});

describe('small languages: the label of a part row', () => {
  it('names the part and its question', () => {
    expect(questionLabel({ subjectId: 'dutch', fileid: 'LC017ALP000EV.pdf', n: 'II1' })).toBe('Part II · Question 1');
    expect(questionLabel({ subjectId: 'modern-greek', fileid: 'LC013ALP000EV.pdf', n: 'III2' }, { short: true }))
      .toBe('Part III Q2');
    expect(questionLabel({ subjectId: 'czech', fileid: 'LC043ALP000EV.pdf', n: 'II' })).toBe('Part II');
    expect(questionLabel({ subjectId: 'dutch', fileid: 'LC017ALP000EV.pdf', n: '4' })).toBe('Question 4');
    // Only these sixteen: German numbers its texts I-III the same way and keeps its own label.
    expect(questionLabel({ subjectId: 'german', fileid: 'LC006ALP000EV.pdf', n: 'II3' })).toBe('Question II3');
  });
});
