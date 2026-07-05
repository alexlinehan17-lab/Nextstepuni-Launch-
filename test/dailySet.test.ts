/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 *
 * Guards the Paper Trail "Daily 10" top-up (feature E3): when fewer than the
 * target are due, the set is filled from the weakest topics with real questions
 * added to the FSRS deck; when enough are already due, it's a no-op. Runs against
 * the committed tag data + localStorage stores (jsdom).
 */
import { describe, it, expect, beforeEach } from 'vitest';
import { topUpDaily } from '../components/PaperTrail/dailySet';
import { setMark } from '../components/PaperTrail/attemptStore';
import { addCard, loadDeck, dueCards } from '../components/PaperTrail/reviewStore';
import { PAPER_TOPIC_TAGS } from '../data/paperTrail/topicTags';

const NOW = 1_700_000_000_000;
const p = PAPER_TOPIC_TAGS[0];

describe('Paper Trail — Daily 10 top-up', () => {
  beforeEach(() => localStorage.clear());

  it('tops an empty deck up from the weakest topics', () => {
    // A weak self-mark on a real tagged question makes its topic the weakest.
    setMark(`u1|${p.subjectId}|${p.year}|${p.level}|${p.lang}|${p.fileid}`, p.q[0].n, { score: 2, max: 20, ts: NOW });
    const added = topUpDaily('u1', NOW, 5);
    expect(added).toBeGreaterThan(0);
    expect(added).toBeLessThanOrEqual(5);
    expect(loadDeck('u1').length).toBe(added);
    // The added cards are due now, so they form today's set.
    expect(dueCards('u1', NOW).length).toBe(added);
  });

  it('is a no-op when enough cards are already due', () => {
    for (let i = 0; i < 6; i++) {
      addCard('u1', { subjectId: 'business', year: 2000 + i, level: 'higher', lang: 'ev', fileid: `f${i}`, n: '1' }, undefined, NOW);
    }
    expect(topUpDaily('u1', NOW, 5)).toBe(0);
  });

  it('does nothing for a brand-new student with no weaknesses', () => {
    expect(topUpDaily('u1', NOW, 10)).toBe(0);
    expect(loadDeck('u1')).toHaveLength(0);
  });
});
