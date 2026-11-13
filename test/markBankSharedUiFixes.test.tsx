/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 *
 * Shared Mark Bank session fixes (13 November 2026), each pinned on the live
 * card that showed the defect:
 *  - a one-pick menu reads "One of these — 2 marks" (Spanish 2010 HL Section L Q2(b));
 *  - a menu pick commits its route and a menu on the other route is locked
 *    (Engineering 2015 HL Q7(c)(i), in both orders);
 *  - printed line breaks and bullets inside a row are kept (Economics 2021 HL
 *    Q16(a)(i), Engineering 2013 HL Q1(p)), History's rows exactly as before;
 *  - a menu shows its own label (Economics 2020 HL Section B Q7(b)(iii));
 *  - the question's mark stops at the first printed line break (Spanish 2010
 *    HL Section B Q5);
 *  - on a card priced only as a whole, menu picks count towards the grade
 *    suggestion, within the chosen route (Economics 2010 OL Section A Q9).
 */

import { afterEach, describe, expect, test, vi } from 'vitest';
import { cleanup, fireEvent, render, screen, within } from '@testing-library/react';

import SessionScreen, { suggestGrade } from '@/components/MarkBank/SessionScreen';
import { splitForEmphasis } from '@/components/MarkBank/questionEmphasis';
import { menuLabel } from '@/components/MarkBank/sessionText';
import { CARDS as ECONOMICS_HIGHER } from '@/components/MarkBank/cards/economics/higher';
import { CARDS as ECONOMICS_ORDINARY } from '@/components/MarkBank/cards/economics/ordinary';
import { CARDS as ENGINEERING_HIGHER } from '@/components/MarkBank/cards/engineering/higher';
import { CARDS as SPANISH_HIGHER } from '@/components/MarkBank/cards/spanish/higher';
import { CARDS as HISTORY_HIGHER } from '@/components/MarkBank/cards/history/higher';
import type { MarkRow, SecCard, SecQuestionCard } from '@/types/markBank';

vi.mock('@/components/PaperTrail/vaultDocs', () => ({ vaultPdf: vi.fn(() => new Promise(() => {})) }));
vi.mock('@/components/PaperTrail/CropView', () => ({ default: () => <div>Official PDF page</div> }));

afterEach(() => cleanup());

const card = (deck: SecCard[], id: string): SecCard => {
  const found = deck.find(c => c.id === id);
  if (!found) throw new Error(`no live card ${id}`);
  return found;
};
const renderSession = (c: SecCard) => render(
  <SessionScreen cards={[c]} subjectLabel="Mark Bank" onGrade={vi.fn()} onFinish={vi.fn()} onExit={vi.fn()} />,
);
const reveal = () => fireEvent.click(screen.getByRole('button', { name: /Reveal the marking scheme/i }));
const guidance = () => (document.getElementById('mark-bank-grade-guidance')?.textContent ?? '').split('You decide')[0];
const option = (name: string) => screen.getByRole('button', { name }) as HTMLButtonElement;
/** The answer text of the row that starts with `start` (the row's own span, not the summary band). */
const rowText = (start: string) => {
  const spans = [...document.querySelectorAll<HTMLElement>('button[aria-pressed] span[dir="auto"]')].filter(span => span.textContent?.startsWith(start));
  expect(spans).toHaveLength(1);
  return spans[0];
};

describe('es-2010-hl-l-2-b: a one-pick menu', () => {
  test('reads "One of these — 2 marks", not "Any 1 of these — 2 marks each"', () => {
    renderSession(card(SPANISH_HIGHER, 'es-2010-hl-l-2-b'));
    reveal();
    expect(screen.getByText('One of these — 2 marks')).toBeInTheDocument();
    expect(screen.queryByText(/Any 1 of these/)).not.toBeInTheDocument();
  });

  test('the generic "The answers the scheme accepts" label is not shown above it', () => {
    renderSession(card(SPANISH_HIGHER, 'es-2010-hl-l-2-b'));
    reveal();
    expect(screen.queryByText('The answers the scheme accepts')).not.toBeInTheDocument();
  });
});

describe('eng-2015-hl-q7-c-i: a menu on an answer route', () => {
  const chip = /A – Continuous chip/;
  const menuOption = 'They repeatability produce parts to maximum accuracy';

  test('a route A tick locks route B\'s menus, which would score nothing', () => {
    renderSession(card(ENGINEERING_HIGHER, 'eng-2015-hl-q7-c-i'));
    reveal();
    fireEvent.click(screen.getByRole('button', { name: chip }));
    expect(option(menuOption)).toBeDisabled();
    expect(option('More expensive to purchase and repair.')).toBeDisabled();
    expect(screen.getAllByText('The examiner marks one route or the other — not a mix of both.').length).toBeGreaterThanOrEqual(2);
    fireEvent.click(option(menuOption));
    expect(option(menuOption)).toHaveAttribute('aria-pressed', 'false');
    expect(guidance()).toContain('You claimed 2 of 8 marks');
  });

  test('a route B pick commits route B and locks route A\'s rows', () => {
    renderSession(card(ENGINEERING_HIGHER, 'eng-2015-hl-q7-c-i'));
    reveal();
    fireEvent.click(option(menuOption));
    expect(option(menuOption)).toHaveAttribute('aria-pressed', 'true');
    const routeA = screen.getByRole('button', { name: chip });
    expect(routeA).toBeDisabled();
    fireEvent.click(routeA);
    expect(routeA).toHaveAttribute('aria-pressed', 'false');
    // Before: the tick was taken, route A was committed and the pick was dropped (2 of 8).
    expect(guidance()).toContain('You claimed 2 of 8 marks');
    fireEvent.click(option('More expensive to purchase and repair.'));
    expect(guidance()).toContain('You claimed 4 of 8 marks');
  });
});

describe('printed line breaks inside a row', () => {
  test('econ-2021-hl-q16-a-i-trend keeps its two printed paragraphs', () => {
    const c = card(ECONOMICS_HIGHER, 'econ-2021-hl-q16-a-i-trend') as SecQuestionCard;
    renderSession(c);
    reveal();
    const text = rowText(c.rows[0].verbatim.slice(0, 40));
    expect(text).toHaveStyle({ whiteSpace: 'pre-line' });
    expect(text.textContent).toBe(c.rows[0].verbatim);
  });

  test('eng-2013-hl-q1-p puts each printed bullet on its own line, text otherwise unchanged', () => {
    const c = card(ENGINEERING_HIGHER, 'eng-2013-hl-q1-p') as SecQuestionCard;
    renderSession(c);
    reveal();
    const text = rowText('Engine efficiency:');
    expect(text).toHaveStyle({ whiteSpace: 'pre-line' });
    expect(text.textContent).toContain('Advantages:\n• Any available heat source can be used\n• Can be used');
    expect(text.textContent!.replace(/\n• /g, ' • ')).toBe(c.rows[0].verbatim);
  });

  test('History rows keep exactly the text and pre-line they had (hist-2010-hl-lm-s1-q2b)', () => {
    const c = card(HISTORY_HIGHER, 'hist-2010-hl-lm-s1-q2b') as SecQuestionCard;
    renderSession(c);
    reveal();
    const text = rowText('This phrase suggests a lack of the confidence');
    expect(text).toHaveStyle({ whiteSpace: 'pre-line' });
    expect(text.textContent).toBe(c.rows[2].verbatim);
  });
});

describe('econ-2020-hl-sb-q7-b-iii: a menu shows its own label', () => {
  test('"For — any one" and "Against — any one" head their menus, exactly as printed', () => {
    renderSession(card(ECONOMICS_HIGHER, 'econ-2020-hl-sb-q7-b-iii'));
    reveal();
    expect(screen.getByText('For — any one')).toBeInTheDocument();
    expect(screen.getByText('Against — any one')).toBeInTheDocument();
    expect(screen.getAllByText('One of these — 5 marks')).toHaveLength(2);
  });

  test('a label is shown only where it is one', () => {
    const group = (options: string[]) => ({ claimMax: 1, perOption: 2, options });
    expect(menuLabel({ verbatim: 'For — any one', group: group(['a', 'b']) })).toBe('For — any one');
    expect(menuLabel({ verbatim: 'Any TWO', group: group(['a', 'b']) })).toBe('Any TWO');
    // The row's text is one of its options, or the options run together: the menu shows them already.
    expect(menuLabel({ verbatim: 'Price', group: group(['Price', 'Quantity']) })).toBeNull();
    expect(menuLabel({ verbatim: 'Extent of knowledge / basis of investigation', group: group(['Extent of knowledge', 'basis of investigation']) })).toBeNull();
    // Generic wording repeats the heading.
    expect(menuLabel({ verbatim: 'The answers the scheme accepts in full', group: group(['a', 'b']) })).toBeNull();
    expect(menuLabel({ verbatim: 'Any 3 of the answers the scheme states', group: group(['a', 'b']) })).toBeNull();
    // A real label that ends in the generic words is still a label.
    expect(menuLabel({ verbatim: 'What: the answers the scheme accepts', group: group(['a', 'b']) })).toBe('What: the answers the scheme accepts');
  });
});

describe('es-2010-hl-b-5: the mark stops at the first printed line break', () => {
  test('only the first statement is underlined; the printed "O" and the second statement read plain', () => {
    renderSession(card(SPANISH_HIGHER, 'es-2010-hl-b-5'));
    const question = screen.getByTestId('mark-bank-question-text');
    const marked = [...question.querySelectorAll('span')].filter(span => span.style.textDecorationLine === 'underline' || span.style.backgroundImage);
    expect(marked.map(span => span.textContent)).toEqual(['El invento más importante del siglo pasado.']);
    expect(question.textContent).toContain('El invento más importante del siglo pasado.\nO\nEl silencio no existe en el mundo moderno.');
  });

  test('the split never drops or adds a character', () => {
    for (const text of [
      'El invento más importante del siglo pasado.\nO\nEl silencio no existe en el mundo moderno.',
      'Explain the term inflation.\nGive an example.',
      '\nName the part labelled A.',
      'Describe the process.',
    ]) {
      const { before, marked, after } = splitForEmphasis(text);
      expect(before + marked + after).toBe(text);
      expect(marked.trim()).not.toContain('\n');
      expect(marked.trim()).not.toBe('');
    }
  });
});

describe('econ-2010-ol-sa-q9: menu picks count on a card priced only as a whole', () => {
  test('both effects picked suggests Got it; one suggests Shaky (was "Missed it")', () => {
    renderSession(card(ECONOMICS_ORDINARY, 'econ-2010-ol-sa-q9'));
    reveal();
    const options = screen.getAllByRole('button').filter(b => b.getAttribute('aria-pressed') !== null && /^(Taxation revenue falls|Unemployment)/.test(b.textContent ?? ''));
    expect(options).toHaveLength(2);
    fireEvent.click(options[0]);
    expect(guidance()).toContain('That looks like Shaky.');
    fireEvent.click(options[1]);
    expect(guidance()).toContain('That looks like Got it.');
    const suggested = screen.getAllByRole('button').find(b => b.hasAttribute('data-suggested'));
    expect(suggested && within(suggested).getByText('Got it')).toBeTruthy();
  });

  test('only the chosen route counts: one branch answered in full is Got it', () => {
    const row = (o: Partial<MarkRow>): MarkRow => ({ id: 'r', kind: 'point', verbatim: 'x', marks: null, ...o });
    const c = {
      ...card(ECONOMICS_ORDINARY, 'econ-2010-ol-sa-q9'),
      rows: [
        row({ id: 'a1', verbatim: 'weld cracks', route: 'a' }),
        row({ id: 'a2', verbatim: 'slag inclusions', route: 'a' }),
        row({ id: 'b1', verbatim: 'charging zones', route: 'b' }),
        row({ id: 'm', kind: 'anyN', verbatim: 'Monitoring — any one', route: 'b', group: { claimMax: 1, perOption: 0, options: ['remote', 'planned'] } }),
      ],
    } as SecQuestionCard;
    expect(suggestGrade(c, {})).toBe('missed');
    expect(suggestGrade(c, { a1: 'yes' })).toBe('shaky');
    expect(suggestGrade(c, { a1: 'yes', a2: 'yes' })).toBe('got');
    expect(suggestGrade(c, { b1: 'yes' }, { m: [1] })).toBe('got');
    expect(suggestGrade(c, {}, { m: [0] })).toBe('shaky');
  });
});
