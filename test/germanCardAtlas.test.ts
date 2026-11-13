/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 *
 * Every German Mark Bank card resolves to a printed question in the Topic
 * Atlas: its own booklet, the Atlas question its printed address names, and
 * at least one Atlas topic of the card's own level, with the card's topic
 * among that question's tags.
 *
 * The German Atlas names its questions by what the paper prints, so the join
 * is the address itself, read from the card's citation:
 *   TEXT I Question 2     -> "I2"   (TEXT II -> "II2", TEXT III -> "III2")
 *   Angewandte Grammatik  -> "G"
 *   Listening, Part 3     -> "3" in the listening booklet
 *   Äußerung (a), Schriftliche Produktion (b) -> "T-A", "P-B"
 * The 2010-2018 written booklets are named straight through in the Atlas
 * instead ("1" to "13"), though the paper restarts its numbering under each
 * text, as the cards cite it: TEXT II Question 1 of a sitting whose TEXT I
 * prints four questions is Atlas question "5". The offset is the number of
 * questions the earlier texts print, read from the sitting's own cards, which
 * carry every printed reading question; a guard checks the texts' questions
 * add to the Atlas's numbered ones.
 */

import { describe, expect, it } from 'vitest';
import { CARDS as GERMAN_HIGHER } from '../components/MarkBank/cards/german/higher';
import { CARDS as GERMAN_ORDINARY } from '../components/MarkBank/cards/german/ordinary';
import { browseTopicIdsForQuestion, topicsForPaper } from '../components/PaperTrail/topics';
import { examTopicDefinition } from '../data/examTopics/registry';

const cards = [...GERMAN_HIGHER, ...GERMAN_ORDINARY];
const TEXT = { T1: 'I', T2: 'II', T3: 'III' } as Record<string, string>;
const REF = /^\d{4} (?:HL|OL) Section (\w+) Q(\d*)(?:\(([ab])\))?/;

/** The Atlas question a card's printed address names. */
function atlasQuestion(questionRef: string): string | null {
  const m = REF.exec(questionRef);
  if (!m) return null;
  const [, section, q, letter] = m;
  if (TEXT[section]) return `${TEXT[section]}${q}`;
  if (section === 'AG') return 'G';
  // Written production: Äußerung zum Thema (a)/(b) -> "T-A"/"T-B",
  // Schriftliche Produktion (a)/(b) -> "P-A"/"P-B".
  if ((section === 'AT' || section === 'SP') && letter) return `${section === 'AT' ? 'T' : 'P'}-${letter.toUpperCase()}`;
  if (/^L[1-4]$/.test(section)) return section.slice(1);
  return null;
}

/** For each sitting, how many questions each text prints (its highest
 *  question number on a card). */
const printedPerText = new Map<string, Record<string, number>>();
for (const card of cards) {
  const m = REF.exec(card.questionRef);
  if (!m || !TEXT[m[1]] || !m[2]) continue;
  const key = `${card.year}|${card.level}|${card.paperFileid}`;
  const counts = printedPerText.get(key) ?? {};
  counts[m[1]] = Math.max(counts[m[1]] ?? 0, Number(m[2]));
  printedPerText.set(key, counts);
}

/** The straight-through Atlas name of a reading card's question (2010-2018). */
function straightThrough(card: (typeof cards)[number]): string | null {
  const m = REF.exec(card.questionRef);
  if (!m || !TEXT[m[1]] || !m[2]) return null;
  const counts = printedPerText.get(`${card.year}|${card.level}|${card.paperFileid}`) ?? {};
  const before = ['T1', 'T2', 'T3'].slice(0, ['T1', 'T2', 'T3'].indexOf(m[1]));
  return String(before.reduce((sum, unit) => sum + (counts[unit] ?? 0), 0) + Number(m[2]));
}

describe('German cards in the Topic Atlas', () => {
  it('reads a straight-through Atlas paper only where its texts add up to it', () => {
    const wrong: string[] = [];
    for (const [key, counts] of printedPerText) {
      const [year, level, fileid] = key.split('|');
      const paper = topicsForPaper('german', Number(year), level as 'higher' | 'ordinary', 'ev',
        `${fileid.replace(/\.pdf$/i, '')}.pdf`);
      const numbered = paper?.q.filter(item => /^\d+$/.test(item.n)).length ?? 0;
      const printed = Object.values(counts).reduce((sum, n) => sum + n, 0);
      if (numbered && numbered !== printed) wrong.push(`${key}: Atlas ${numbered}, texts ${printed}`);
    }
    expect(wrong).toEqual([]);
  });


  it('names an Atlas question for every card', () => {
    expect(cards.filter(card => !atlasQuestion(card.questionRef)).map(card => card.id)).toEqual([]);
  });

  it('resolves every card to its own printed question under a topic of its level', () => {
    const missing: string[] = [];
    for (const card of cards) {
      const n = atlasQuestion(card.questionRef);
      if (!n) continue;
      const fileid = `${String(card.paperFileid).replace(/\.pdf$/i, '')}.pdf`;
      const paper = topicsForPaper('german', card.year, card.level, 'ev', fileid);
      const question = paper?.q.find(item => item.n === n)
        ?? (paper?.q.some(item => item.n === '1') ? paper.q.find(item => item.n === straightThrough(card)) : undefined);
      if (!paper || !question) {
        missing.push(`${card.id}: ${fileid} has no question ${n}`);
        continue;
      }
      const topics = browseTopicIdsForQuestion(paper, question);
      if (!topics.some(id => examTopicDefinition(id)?.level === card.level)) {
        missing.push(`${card.id}: question ${n} has no ${card.level} topic`);
      }
      const tagged = [question.primary, question.secondary].filter(Boolean);
      if (!tagged.includes(card.topicId)) {
        missing.push(`${card.id}: question ${n} is tagged ${tagged.join(', ')}, the card ${card.topicId}`);
      }
    }
    expect(missing).toEqual([]);
  });

  it('files every listening card in the listening booklet, never the written paper', () => {
    const wrong = cards
      .filter(card => /^L[1-4]$/.test(card.section))
      .filter(card => !/^LC011[AG]LPA00[BE]V(?:-deferred)?$/.test(String(card.paperFileid)))
      .map(card => `${card.id}: ${card.paperFileid}`);
    expect(wrong).toEqual([]);
  });
});
