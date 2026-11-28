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
import type { SecCard, SecPointCard } from '../types/markBank';
import type { DeckState } from '../components/MarkBank/store';
import { ClaimRow, marksChip, marksLabel } from '../components/MarkBank/ClaimRows';
import SessionScreen from '../components/MarkBank/SessionScreen';

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

describe('changing subject', () => {
  // Rendered through MarkBank, as the Launchpad mounts it; jsdom is narrower than a laptop, so the button opens the sheet.
  afterEach(() => localStorage.clear());

  it('lists only the subjects the student takes, and switching subject keeps the level', async () => {
    const { default: MarkBank } = await import('../components/MarkBank/MarkBank');
    render(<MarkBank studentSubjects={[{ subjectName: 'Biology', level: 'higher' }, { subjectName: 'Chemistry', level: 'higher' }]} />);
    const button = () => screen.getByRole('button', { name: /^Change subject or level: / });
    expect(button()).toHaveTextContent('Biology');
    fireEvent.click(button());
    const sheet = await screen.findByRole('dialog', { name: 'Change subject or level' });
    const subjects = within(within(sheet).getByRole('radiogroup', { name: 'Your subjects' })).getAllByRole('radio');
    expect(subjects.map(subject => subject.textContent)).toEqual(['Biology', 'Chemistry']);
    expect(within(sheet).getByRole('radio', { name: 'Biology' })).toHaveAttribute('aria-checked', 'true');
    // The level first: Ordinary applies at once.
    fireEvent.click(within(sheet).getByRole('radio', { name: 'Ordinary' }));
    expect(await screen.findByText(/^Ordinary level/)).toBeInTheDocument();
    fireEvent.click(button());
    fireEvent.click(within(await screen.findByRole('dialog', { name: 'Change subject or level' })).getByRole('radio', { name: 'Chemistry' }));
    expect(button()).toHaveTextContent('Chemistry');
    expect(button()).toHaveTextContent('Ordinary level');
  });

  it('offers every subject to a student who has not set their subjects', async () => {
    const { default: MarkBank } = await import('../components/MarkBank/MarkBank');
    const { SUBJECTS } = await import('../components/MarkBank/deck');
    render(<MarkBank studentSubjects={[]} />);
    fireEvent.click(screen.getByRole('button', { name: /^Change subject or level: / }));
    const sheet = await screen.findByRole('dialog', { name: 'Change subject or level' });
    expect(within(within(sheet).getByRole('radiogroup', { name: 'Subjects' })).getAllByRole('radio')).toHaveLength(SUBJECTS.length);
  });
});

describe('a claimed scheme row (the board\'s claim row)', () => {
  it('reads its marks as the board does: "3 marks", "1 mark", "−1 mark", from one helper', () => {
    expect(marksLabel(3)).toBe('3 marks');
    expect(marksLabel(1)).toBe('1 mark');
    expect(marksLabel(0)).toBe('0 marks');
    expect(marksLabel(-1)).toBe('−1 mark');
    expect(marksChip(3)).toBe('3m');
  });

  it('a rubric row, claimed, carries the chosen state the shared choice draws: pressed, the mark on, no fill', () => {
    const { rerender } = render(<ClaimRow text="Glucose is built up" marks={3} claimed={false} onToggle={vi.fn()} />);
    const row = screen.getByRole('button', { name: 'Glucose is built up · 3m' });
    expect(row).toHaveClass('ui-choice', 'mb-claim-row');
    expect(row).toHaveAttribute('aria-pressed', 'false');
    expect(row.querySelector('.ui-mark--square')).not.toHaveClass('ui-mark--on');
    expect(row.querySelector('.mb-claim-chip')).toHaveTextContent(/^3 marks$/);
    rerender(<ClaimRow text="Glucose is built up" marks={1} claimed onToggle={vi.fn()} />);
    expect(row).toHaveAttribute('aria-pressed', 'true');
    expect(row).toHaveAttribute('data-claimed', 'true');
    expect(row.querySelector('.ui-mark--square')).toHaveClass('ui-mark--on');
    expect(row.querySelector('.mb-claim-chip')).toHaveTextContent(/^1 mark$/);
  });

  it('a science row in the practice card claims the same way, and its marks read "N marks"', () => {
    const card = biology.find((entry): entry is SecPointCard => entry.kind === 'question' && entry.rows.length === 1
      && entry.rows[0].kind === 'point' && !entry.rows[0].permittedMarks && entry.rows[0].marks === 3)!;
    render(<SessionScreen paperLayout cards={[card]} subjectLabel="Biology" onGrade={vi.fn()} onFinish={vi.fn()} onExit={vi.fn()} />);
    fireEvent.click(screen.getByRole('button', { name: /Reveal the marking scheme/i }));
    const row = document.querySelector('button.mb-pt') as HTMLButtonElement;
    expect(row).toHaveClass('ui-choice', 'mb-claim-row');
    expect(row.querySelector('.mb-claim-chip')).toHaveTextContent(/^3 marks$/);
    fireEvent.click(row);
    expect(row).toHaveAttribute('aria-pressed', 'true');
    expect(row).toHaveAttribute('data-claimed', 'true');
    expect(row.querySelector('.ui-mark--square')).toHaveClass('ui-mark--on');
  });
});
