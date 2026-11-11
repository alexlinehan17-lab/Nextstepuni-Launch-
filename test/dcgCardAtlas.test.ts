/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 *
 * Design & Communication Graphics in the Topic Atlas, and the booklet each
 * card links to.
 *
 * DCG is sat as two booklets: Section A (an A3 sheet, "A-1" to "A-4") and
 * Sections B and C together ("B-1" to "C-5"). The SEC's component codes do not
 * say which is which (2011 swaps 000 and 014) and Paper Trail's labels say so
 * only from 2019, so paperIndex.mjs identifies the booklet by the questions it
 * prints. Every card must then reach its own printed question in the Atlas --
 * Section A numbered 1-4 in its booklet, Sections B and C numbered 1-8 in
 * theirs -- under a topic of the card's level. A card the Atlas does not list
 * is a card a student can practise but never reach by topic.
 */

import fs from 'node:fs';
import { describe, expect, it } from 'vitest';
import { CARDS as DCG_HIGHER } from '../components/MarkBank/cards/dcg/higher';
import { CARDS as DCG_ORDINARY } from '../components/MarkBank/cards/dcg/ordinary';
import { browseTopicIdsForQuestion, topicsForPaper } from '../components/PaperTrail/topics';
import { examTopicDefinition } from '../data/examTopics/registry';

const ATLAS_SUBJECT = 'design-and-communication-graphics';
const cards = [...DCG_HIGHER, ...DCG_ORDINARY];

interface TagPaper {
  level: 'higher' | 'ordinary'; lang: string; year: number; fileid: string; paperKey: string;
  q: Array<{ n: string; primary: string; secondary?: string }>;
}
const tags: TagPaper[] = JSON.parse(fs.readFileSync(
  'scripts/paper-trail/topic-tags/tags/design-and-communication-graphics.json', 'utf8'));

/** The Atlas's own address for a printed DCG question. */
const atlasAddress = (section: string, q: number) => (section === 'A'
  ? { paperKey: 'section-a', n: String(q) }
  : { paperKey: 'single', n: String(section === 'B' ? q : q + 3) });

describe('DCG booklets', () => {
  it('resolves each section to the booklet the Atlas files it under, 2010-2026', async () => {
    const { resolvePaperFileid } = await import('../scripts/markbank/paperIndex.mjs');
    const wrong: string[] = [];
    for (const paper of tags.filter(p => p.lang === 'ev' && !p.fileid.includes('deferred'))) {
      const sections = paper.paperKey === 'section-a' ? ['A'] : ['B', 'C'];
      for (const section of sections) {
        const got = resolvePaperFileid('dcg', paper.year, paper.level, section);
        if (`${got}.pdf` !== paper.fileid) wrong.push(`${paper.year} ${paper.level} ${section}: ${got} vs ${paper.fileid}`);
      }
    }
    expect(wrong).toEqual([]);
  });

  it('follows the 2011 swap rather than the labels', async () => {
    const { resolvePaperFileid } = await import('../scripts/markbank/paperIndex.mjs');
    // Paper Trail labels 2011's 000 "Exam Paper" and 014 "Section A"; the
    // booklets print the reverse.
    expect(resolvePaperFileid('dcg', 2011, 'higher', 'A')).toBe('LC562ALP000EV');
    expect(resolvePaperFileid('dcg', 2011, 'higher', 'C')).toBe('LC562ALP014EV');
    expect(resolvePaperFileid('dcg', 2018, 'ordinary', 'C')).toBe('LC562GLP015EV');
  });
});

describe('DCG Geologic Geometry carries its contour map', () => {
  it('opens the back page of the Section A booklet on every C-1 card, and on no other', () => {
    // "This Contour Map is part of Section C and should only be used for the
    // answering of the Geologic Geometry Option": printed on page 3 of the
    // Section A booklet in every sitting, never with the question itself.
    const wrong: string[] = [];
    for (const card of cards) {
      const source = card.sourceMaterial;
      const isC1 = /Section C Q1\b/.test(card.questionRef);
      if (!isC1) { if (source) wrong.push(`${card.id}: unexpected source`); continue; }
      const booklet = tags.find(p => p.lang === 'ev' && p.year === card.year && p.level === card.level && p.paperKey === 'section-a');
      if (!source || source.kind !== 'source-illustration' || JSON.stringify(source.pages) !== '[3]'
          || `${source.sourceFileid}.pdf` !== booklet?.fileid) {
        wrong.push(`${card.id}: ${JSON.stringify(source)}`);
      }
    }
    expect(wrong).toEqual([]);
    // Every C-1 card of every carded sitting: 75 for 2018-2026, then per
    // sitting added (2017 Higher 6, 2017 Ordinary 3).
    expect(cards.filter(c => c.sourceMaterial).length).toBe(84);
  });
});

describe('DCG cards in the Topic Atlas', () => {
  it('reads a printed section and question off every card', () => {
    for (const card of cards) {
      expect(card.questionRef, card.id).toMatch(/^\d{4} (?:HL|OL) Section [ABC] Q[1-5]/);
    }
  });

  it('resolves every card to its own printed question under a topic of its level', () => {
    const missing: string[] = [];
    for (const card of cards) {
      const [, section, q] = card.questionRef.match(/Section ([ABC]) Q(\d)/)!;
      const { n } = atlasAddress(section, Number(q));
      const fileid = `${String(card.paperFileid).replace(/\.pdf$/i, '')}.pdf`;
      const paper = topicsForPaper(ATLAS_SUBJECT, card.year, card.level, 'ev', fileid);
      const question = paper?.q.find(item => item.n === n);
      if (!paper || !question) {
        missing.push(`${card.id}: ${fileid} has no question ${n}`);
        continue;
      }
      if (!browseTopicIdsForQuestion(paper, question).some(id => examTopicDefinition(id)?.level === card.level)) {
        missing.push(`${card.id}: question ${n} has no ${card.level} topic`);
      }
    }
    expect(missing).toEqual([]);
  });

  it('files every card under a topic its Atlas question carries', () => {
    const index = new Map<string, string[]>(tags.filter(p => p.lang === 'ev').flatMap(p => p.q.map(
      (q): [string, string[]] => [`${p.year}|${p.level}|${p.paperKey}|${q.n}`, [q.primary, ...(q.secondary ? [q.secondary] : [])]],
    )));
    const disagree: string[] = [];
    for (const card of cards) {
      const [, section, q] = card.questionRef.match(/Section ([ABC]) Q(\d)/)!;
      const { paperKey, n } = atlasAddress(section, Number(q));
      const topics = index.get(`${card.year}|${card.level}|${paperKey}|${n}`) ?? [];
      if (!topics.includes(card.topicId)) disagree.push(`${card.id}: ${card.topicId} not in ${topics.join(', ')}`);
    }
    expect(disagree).toEqual([]);
  });
});
