/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 *
 * Every Spanish Mark Bank card resolves to a printed question in the Topic
 * Atlas: its own booklet, the Atlas question whose anchor begins where the
 * card's ask is printed (scripts/markbank/authoring/es_atlas.py), and at
 * least one Atlas topic of the card's own level. The Higher Atlas numbers a
 * paper in its own running order, not the paper's, so the join is generated
 * from the paper's geometry and committed (spanish-atlas.json); this test
 * holds the deck to it.
 *
 * Two Higher Atlas faults (2020-2025) predate the map and are pinned here so
 * they can only shrink: cards whose paper has no Atlas question of their own,
 * and cards whose Atlas question is tagged under another topic than the
 * card's. No Ordinary card and no 2026 card has either.
 */

import { describe, expect, it } from 'vitest';
import { CARDS as SPANISH_HIGHER } from '../components/MarkBank/cards/spanish/higher';
import { CARDS as SPANISH_ORDINARY } from '../components/MarkBank/cards/spanish/ordinary';
import { browseTopicIdsForQuestion, topicsForPaper } from '../components/PaperTrail/topics';
import { examTopicDefinition } from '../data/examTopics/registry';
import atlas from '../scripts/markbank/authoring/spanish-atlas.json';

const cards = [...SPANISH_HIGHER, ...SPANISH_ORDINARY];
const map = atlas as {
  cards: Record<string, { fileid: string; n: string }>;
  gaps: Record<string, string>;
  topicResidue: string[];
};

describe('Spanish cards in the Topic Atlas', () => {
  it('files every card under an Atlas question, or names it as a known gap', () => {
    const unfiled = cards.filter(card => !map.cards[card.id] && !map.gaps[card.id]).map(card => card.id);
    expect(unfiled).toEqual([]);
    expect(Object.keys(map.cards).filter(id => !cards.some(card => card.id === id))).toEqual([]);
  });

  it('pins the known Higher Atlas faults so they can only shrink', () => {
    // The Higher Atlas of 2020-2025 predates this map: some printed questions
    // have no Atlas entry of their own (2022 Question 2; 2020 A1b Q4), and some
    // entries are tagged one task over (the literature Q5 as journalism, the
    // journalistic Q3/Q4 as short texts, Question 2 as journalism). Every card
    // they touch is named here; a repair moves it out, nothing moves it in.
    expect(Object.keys(map.gaps).sort()).toEqual([
      'es-2020-hl-a1b-4',
      ...['a-i', 'a-ii', 'a-iii', 'b-i', 'b-ii', 'b-iii'].map(part => `es-2022-hl-a2-${part}`),
    ]);
    expect(map.topicResidue.length).toBeLessThanOrEqual(49);
    for (const id of [...Object.keys(map.gaps), ...map.topicResidue]) {
      expect(id, id).toMatch(/^es-20(2[0-5])-hl-/);
    }
  });

  it('resolves every filed card to its own printed question under a topic of its level', () => {
    const missing: string[] = [];
    for (const card of cards) {
      const entry = map.cards[card.id];
      if (!entry) continue;
      expect(`${String(card.paperFileid).replace(/\.pdf$/i, '')}.pdf`, card.id).toBe(entry.fileid);
      const paper = topicsForPaper('spanish', card.year, card.level, 'ev', entry.fileid);
      const question = paper?.q.find(item => item.n === entry.n);
      if (!paper || !question) {
        missing.push(`${card.id}: ${entry.fileid} has no question ${entry.n}`);
        continue;
      }
      const topics = browseTopicIdsForQuestion(paper, question);
      if (!topics.some(id => examTopicDefinition(id)?.level === card.level)) {
        missing.push(`${card.id}: question ${entry.n} has no ${card.level} topic`);
      }
      const tagged = [question.primary, question.secondary].filter(Boolean);
      if (!map.topicResidue.includes(card.id) && !tagged.includes(card.topicId)) {
        missing.push(`${card.id}: question ${entry.n} is tagged ${tagged.join(', ')}, the card ${card.topicId}`);
      }
    }
    expect(missing).toEqual([]);
  });
});
