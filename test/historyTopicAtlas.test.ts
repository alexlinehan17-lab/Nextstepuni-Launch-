/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 *
 * Every History card resolves to a Topic Atlas question of its own, under the
 * topic its content belongs to.
 *
 * "Its own" means its printed block's, for History: the Atlas tags the four
 * essays of a topic block (and an Ordinary Level topic's parts A, B and C) as
 * one question, "I1" to "I6" or "E1" to "E6", because that block is the unit
 * the paper prints under one syllabus topic, and the documents question's
 * parts as "1" to "4" (components/MarkBank/historyAtlas.ts). The coordinator
 * accepted that granularity on 4 Nov 2026: an essay card resolving to its
 * block's question IS resolving to its own.
 *
 * The Atlas does not yet hold most Early Modern papers. Those papers are
 * pinned below by name, so the list can only change on purpose: adding a
 * paper to the Atlas fails this test until the pin drops it, and a paper
 * that went missing fails it too.
 */
import { describe, expect, it } from 'vitest';
import { CARDS as HISTORY_HIGHER } from '../components/MarkBank/cards/history/higher';
import { CARDS as HISTORY_ORDINARY } from '../components/MarkBank/cards/history/ordinary';
import { historyAtlasQuestion } from '../components/MarkBank/historyAtlas';
import { topicsForPaper } from '../components/PaperTrail/topics';
import { isRubricCard } from '../types/markBank';

const cards = [...HISTORY_HIGHER, ...HISTORY_ORDINARY];

/** The Early Modern papers with History cards and no Atlas entry yet (4 Nov 2026). */
const NOT_YET_IN_ATLAS = [
  'history-early-modern 2021 ordinary',
  'history-early-modern 2022 ordinary',
  'history-early-modern 2023 higher',
  'history-early-modern 2023 ordinary',
  'history-early-modern 2024 higher',
  'history-early-modern 2024 ordinary',
  'history-early-modern 2025 higher',
  'history-early-modern 2025 ordinary',
];

/** Early Modern papers whose documents question still carries the Atlas's old
 *  single Early Modern strand (history-early-modern-0-0) rather than its case
 *  study. history_early_modern.py retags each as its sitting is carded. */
const PLACEHOLDER_DBQ = ['history-early-modern 2022 higher'];

/** The syllabus topic a card files under, as the Atlas's canonical tag range for it
 *  (curriculum.ts strands history-0 to history-3): hist-lm-irl-3 is Later Modern
 *  Ireland topic 3, tagged history-2-8 .. history-2-11; hist-em-eur-2 is Early
 *  Modern Europe topic 2, history-1-4 .. history-1-7. */
const AREA: Record<string, number> = { 'em-irl': 0, 'em-eur': 1, 'lm-irl': 2, 'lm-eur': 3 };
const topicRange = (topicId: string) => {
  const m = /^hist-(lm|em)-(irl|eur)-(\d)$/.exec(topicId);
  if (!m) return null;
  const k = Number(m[3]);
  return { area: AREA[`${m[1]}-${m[2]}`], from: (k - 1) * 4, to: (k - 1) * 4 + 3 };
};

describe('History cards in the Topic Atlas', () => {
  it('reads every History citation as an Atlas address', () => {
    const unread = cards.filter(card => !historyAtlasQuestion(card)).map(card => `${card.id} ${card.questionRef}`);
    expect(unread).toEqual([]);
  });

  it('resolves every card to its printed question, except the pinned Early Modern papers', () => {
    const missingPapers = new Set<string>();
    const missingQuestions: string[] = [];
    for (const card of cards) {
      const address = historyAtlasQuestion(card)!;
      const paper = topicsForPaper(address.subjectId, card.year, card.level as 'higher' | 'ordinary', 'ev', address.fileid);
      if (!paper) { missingPapers.add(`${address.subjectId} ${card.year} ${card.level}`); continue; }
      if (!paper.q.some(q => q.n === address.n)) missingQuestions.push(`${card.id} -> ${address.n}`);
    }
    expect(missingQuestions).toEqual([]);
    expect([...missingPapers].sort()).toEqual(NOT_YET_IN_ATLAS);
  });

  it('files each card under the Atlas topic of its own printed question', () => {
    const wrong: string[] = [];
    const placeholders = new Set<string>();
    for (const card of cards) {
      const address = historyAtlasQuestion(card)!;
      const range = topicRange(card.topicId);
      expect(range, card.id).not.toBeNull();
      const paper = topicsForPaper(address.subjectId, card.year, card.level as 'higher' | 'ordinary', 'ev', address.fileid);
      if (!paper) continue;   // a pinned paper not yet in the Atlas
      const tags = paper.q.find(q => q.n === address.n)!;
      if (tags.primary === 'history-early-modern-0-0') {
        placeholders.add(`${address.subjectId} ${card.year} ${card.level}`);
        continue;
      }
      const inRange = [tags.primary, tags.secondary].filter(Boolean).some(tag => {
        const m = /^history-(\d)-(\d+)$/.exec(tag!);
        return Boolean(m) && Number(m![1]) === range!.area && Number(m![2]) >= range!.from && Number(m![2]) <= range!.to;
      });
      if (!inRange) wrong.push(`${card.id} (${card.topicId}) -> ${address.n} tagged ${tags.primary}${tags.secondary ? `/${tags.secondary}` : ''}`);
    }
    expect(wrong).toEqual([]);
    expect([...placeholders].sort()).toEqual(PLACEHOLDER_DBQ);
  });

  it('gives every essay card its block’s question, and the documents question’s Q4 the question "4"', () => {
    const essays = cards.filter(card => isRubricCard(card) && card.rubric.system === 'history-essay');
    expect(essays.length).toBeGreaterThan(0);
    for (const card of essays) {
      const n = historyAtlasQuestion(card)!.n;
      expect(n, card.id).toMatch(card.section === '1' ? /^4$/ : /^[IE][1-6]$/);
    }
  });
});
