/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 *
 * Mark Bank in the agreed look (area 6b, 27 Nov 2026; Structure A, boards
 * c-markbank-flow and r5-mark-bank). The library became short pages; these pin
 * what each page does and that it starts the same practice as before.
 */
import React from 'react';
import { afterEach, beforeAll, describe, expect, it, vi } from 'vitest';
import { cleanup, fireEvent, render, screen, within } from '@testing-library/react';
import MarkBankLibrary, { type LibraryPage } from '../components/MarkBank/MarkBankLibrary';
import { loadCards } from '../components/MarkBank/deck';
import { loadAtlasModel } from '../components/PaperTrail/atlasModel';
import { cardsForMenuTopic, markBankCurriculumMenu } from '../components/MarkBank/curriculumMenu';
import { resolveSessionQueue } from '../components/MarkBank/sessionPlanning';
import type { SecCard } from '../types/markBank';
import type { DeckState } from '../components/MarkBank/store';

afterEach(cleanup);
const NOW = Date.UTC(2026, 10, 27, 12);
let biology: SecCard[] = [];
let maths: SecCard[] = [];
beforeAll(async () => {
  await Promise.all([loadAtlasModel('biology'), loadAtlasModel('maths')]);
  biology = (await loadCards('biology', 'higher')).filter(card => !card.audioMaterial);
  maths = (await loadCards('maths', 'higher')).filter(card => !card.audioMaterial);
}, 60000);

function library(subjectId: string, cards: SecCard[], options: { state?: DeckState; pages?: LibraryPage[] } = {}) {
  const onStart = vi.fn();
  const onPagesChange = vi.fn();
  const props = {
    subjectId, level: 'higher' as const, cards, state: options.state ?? { v: 1, cards: {}, updatedAt: 0 }, now: () => NOW,
    chooseSubject: vi.fn(), chooseLevel: vi.fn(), canSelectSubject: () => true, onStart, busy: false, ready: true,
    loading: false, error: false, onRetry: vi.fn(), online: true,
  };
  const view = render(<MarkBankLibrary {...props} pages={options.pages} onPagesChange={onPagesChange} />);
  const go = (pages: LibraryPage[]) => view.rerender(<MarkBankLibrary {...props} pages={pages} onPagesChange={onPagesChange} />);
  return { onStart, onPagesChange, go };
}

describe('the subject home', () => {
  it('leads with what to practise now: one charcoal button that starts the whole subject\'s next sitting', () => {
    const { onStart } = library('biology', biology);
    expect(screen.getByRole('heading', { name: 'A little practice.' })).toBeInTheDocument();
    const practise = screen.getByRole('button', { name: /^Practise 12 questions/ });
    expect(practise).toHaveClass('ui-btn--main', 'ui-btn--lg');
    fireEvent.click(practise);
    const expected = resolveSessionQueue(biology, {}, NOW, undefined).map(card => card.id);
    expect(onStart).toHaveBeenCalledWith(undefined, expect.any(Array));
    expect((onStart.mock.calls[0][1] as SecCard[]).map(card => card.id)).toEqual(expected);
  });

  it('lists the strands as rows with a bar and a count, and the subject as one button', () => {
    library('biology', biology);
    const strands = within(screen.getByRole('list', { name: 'All topics' })).getAllByRole('button');
    const menu = markBankCurriculumMenu('biology', 'higher', undefined, biology);
    expect(strands).toHaveLength(menu.strands.length);
    expect(strands[0].querySelector('.ui-row-lead')).toHaveTextContent('01');
    expect(strands[0].querySelector('.ui-row-bar')).not.toBeNull();
    expect(screen.getByRole('button', { name: /^Change subject or level: Biology, Higher level · [\d,]+ questions$/ })).toBeInTheDocument();
    expect(screen.queryByRole('combobox')).not.toBeInTheDocument();
  });

  it('puts a subject with no strands under one row, with the real count of its topics', () => {
    library('maths', maths);
    const menu = markBankCurriculumMenu('maths', 'higher', undefined, maths);
    expect(menu.strands).toHaveLength(1);
    const count = menu.strands[0].topics.length;
    const row = within(screen.getByRole('list', { name: 'All topics' })).getByRole('button');
    expect(row).toHaveTextContent(`All ${count} topics`);
  });

  it('shows Jump back in with the topics practised most recently', () => {
    const menu = markBankCurriculumMenu('biology', 'higher', undefined, biology);
    const topic = menu.strands[1].topics.find(item => cardsForMenuTopic(item.id, biology, menu).length > 1)!;
    const card = cardsForMenuTopic(topic.id, biology, menu)[0];
    const yesterday = NOW - 24 * 3600_000;
    library('biology', biology, { state: { v: 1, updatedAt: yesterday, cards: { [card.id]: { s: 2, d: 5, last: yesterday, reps: 1, lapses: 0, state: 2 } } } });
    const recent = screen.getByRole('list', { name: 'Jump back in' });
    const row = within(recent).getByRole('button', { name: new RegExp(topic.title.replace(/[.*+?^${}()|[\]\\]/g, '\\$&')) });
    expect(row).toHaveTextContent(`Yesterday · 1 of ${cardsForMenuTopic(topic.id, biology, menu).length} tried`);
  });
});

describe('a strand and a topic', () => {
  const menu = () => markBankCurriculumMenu('biology', 'higher', undefined, biology);

  it('a strand opens its topics, each with its number, a thin bar and a count', () => {
    const { onPagesChange, go } = library('biology', biology);
    const strand = menu().strands[1];
    fireEvent.click(within(screen.getByRole('list', { name: 'All topics' })).getAllByRole('button')[1]);
    const pages = onPagesChange.mock.calls.at(-1)![0] as LibraryPage[];
    expect(pages.at(-1)).toEqual({ at: 'strand', strandId: strand.id, topicId: undefined });
    go(pages);
    const topics = within(screen.getByRole('list', { name: new RegExp(`^Topics in `) })).getAllByRole('button');
    expect(topics).toHaveLength(strand.topics.length);
    for (const row of topics) {
      expect(row.querySelector('.ui-row-lead')?.textContent).toMatch(/^(\d+(\.\d+)*|[A-Z]\d|\d{2})$/);
      expect(row.querySelector('.ui-row-chev')).not.toBeNull();
    }
    expect(topics[0].querySelector('.ui-row-value')?.textContent).toMatch(/^0 \/ \d+$/);
  });

  it('a topic is its own page: Practise in charcoal and Browse white with a line, the same height', () => {
    const strand = menu().strands[1];
    const topic = strand.topics.find(item => cardsForMenuTopic(item.id, biology, menu()).length > 12)!;
    const { onStart } = library('biology', biology, { pages: [{ at: 'home' }, { at: 'strand', strandId: strand.id }, { at: 'topic', topicId: topic.id }] });
    expect(screen.getByRole('heading', { level: 1, name: topic.title })).toBeInTheDocument();
    const practise = screen.getByRole('button', { name: /^Practise 6 questions$/ });
    const browse = screen.getByRole('button', { name: /^Browse all [\d,]+ questions$/ });
    expect(practise).toHaveClass('ui-btn--main');
    expect(browse).not.toHaveClass('ui-btn--main');
    for (const button of [practise, browse]) { expect(button).not.toHaveClass('ui-btn--lg'); expect(button).not.toHaveClass('ui-btn--sm'); }
    // Practise starts the same sitting as today's Start for that topic: the topic's queue at the chosen size.
    fireEvent.click(practise);
    const expected = resolveSessionQueue(cardsForMenuTopic(topic.id, biology, menu()), {}, NOW, undefined, 6).map(card => card.id);
    expect(onStart).toHaveBeenCalledWith(topic.id, expect.any(Array));
    expect((onStart.mock.calls[0][1] as SecCard[]).map(card => card.id)).toEqual(expected);
    fireEvent.click(screen.getByRole('radio', { name: '3' }));
    expect(screen.getByRole('button', { name: /^Practise 3 questions$/ })).toBeInTheDocument();
  });

  it('Browse lists every question of the topic, and one starts the practice with it first', () => {
    const strand = menu().strands[1];
    const topic = strand.topics.find(item => cardsForMenuTopic(item.id, biology, menu()).length > 3)!;
    const cards = cardsForMenuTopic(topic.id, biology, menu());
    const { onStart } = library('biology', biology, { pages: [{ at: 'home' }, { at: 'topic', topicId: topic.id }, { at: 'browse', topicId: topic.id }] });
    const rows = within(screen.getByRole('list', { name: 'Questions' })).getAllByRole('button');
    expect(rows).toHaveLength(cards.length);
    fireEvent.click(rows[2]);
    expect(onStart).toHaveBeenCalledOnce();
    expect(onStart.mock.calls[0][0]).toBe(topic.id);
    expect((onStart.mock.calls[0][1] as SecCard[])[0].id).toBe(cards[2].id);
  });
});
