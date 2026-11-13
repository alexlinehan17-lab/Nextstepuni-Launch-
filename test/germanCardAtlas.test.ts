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
 * The 2010-2018 written booklets number their reading questions straight
 * through instead ("1" to "14"); no card of those sittings is in the bank yet.
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

describe('German cards in the Topic Atlas', () => {
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
      const question = paper?.q.find(item => item.n === n);
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
      .filter(card => !/^LC011[AG]LPA00[BE]V$/.test(String(card.paperFileid)))
      .map(card => `${card.id}: ${card.paperFileid}`);
    expect(wrong).toEqual([]);
  });
});
