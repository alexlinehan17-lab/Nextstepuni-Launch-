/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 *
 * Every Technology Mark Bank card resolves to a printed question in the Topic
 * Atlas: its own booklet (the card's paperFileid), its own printed number
 * (Section A's "7", or Sections B and C as "B2" and "C4", the n the Atlas
 * tags use), and at least one Atlas topic of the card's own level. A card
 * whose question the Atlas does not list, or lists under no topic, is a card a
 * student can practise but never reach by topic.
 */

import { describe, expect, it } from 'vitest';
import { CARDS as TECHNOLOGY_HIGHER } from '../components/MarkBank/cards/technology/higher';
import { CARDS as TECHNOLOGY_ORDINARY } from '../components/MarkBank/cards/technology/ordinary';
import { browseTopicIdsForQuestion, topicsForPaper } from '../components/PaperTrail/topics';
import { examTopicDefinition } from '../data/examTopics/registry';

const cards = [...TECHNOLOGY_HIGHER, ...TECHNOLOGY_ORDINARY];

describe('Technology cards in the Topic Atlas', () => {
  it('reads a printed section and question off every card', () => {
    for (const card of cards) {
      expect(card.questionRef, card.id).toMatch(/^\d{4} (?:HL|OL) Section [ABC] Q\d+/);
    }
  });

  it('resolves every card to its own printed question under a topic of its level', () => {
    const missing: string[] = [];
    for (const card of cards) {
      const [, section, q] = card.questionRef.match(/Section ([ABC]) Q(\d+)/)!;
      const n = section === 'A' ? q : `${section}${q}`;
      const fileid = `${String(card.paperFileid).replace(/\.pdf$/i, '')}.pdf`;
      const paper = topicsForPaper('technology', card.year, card.level, 'ev', fileid);
      const question = paper?.q.find(item => item.n === n);
      if (!paper || !question) {
        missing.push(`${card.id}: ${fileid} has no question ${n}`);
        continue;
      }
      const topics = browseTopicIdsForQuestion(paper, question);
      if (!topics.some(id => examTopicDefinition(id)?.level === card.level)) {
        missing.push(`${card.id}: question ${n} has no ${card.level} topic`);
      }
    }
    expect(missing).toEqual([]);
  });
});
