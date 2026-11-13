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
 *  - the question's mark stops at the first printed line break, and a choice
 *    printed either side of a line holding only "O"/"or"/"nó" marks each
 *    alternative (Spanish 2010 HL Section B Q5);
 *  - a route not taken says so once, under its heading; a route that is a
 *    menu gets a heading (Engineering 2015 HL Q7(c)(i), 2014 HL Q5(c)(i));
 *  - an equal split ("4 + 4") is not said to mark the first answers higher
 *    (Engineering 2024 HL Q8(c)(ii));
 *  - on a card priced only as a whole, menu picks count towards the grade
 *    suggestion, within the chosen route (Economics 2010 OL Section A Q9).
 */

import { afterEach, describe, expect, test, vi } from 'vitest';
import { cleanup, fireEvent, render, screen, within } from '@testing-library/react';

import SessionScreen, { suggestGrade } from '@/components/MarkBank/SessionScreen';
import { emphasisSegments, splitForEmphasis } from '@/components/MarkBank/questionEmphasis';
import { menuLabel, splitSteps, uniformSplit } from '@/components/MarkBank/sessionText';
import { ROUTE_LOCKED_NOTE } from '@/components/MarkBank/RouteHeading';
import { CARDS as ECONOMICS_HIGHER } from '@/components/MarkBank/cards/economics/higher';
import { CARDS as ECONOMICS_ORDINARY } from '@/components/MarkBank/cards/economics/ordinary';
import { CARDS as ENGINEERING_HIGHER } from '@/components/MarkBank/cards/engineering/higher';
import { CARDS as SPANISH_HIGHER } from '@/components/MarkBank/cards/spanish/higher';
import { CARDS as HISTORY_HIGHER } from '@/components/MarkBank/cards/history/higher';
import { CARDS as BIOLOGY_HIGHER } from '@/components/MarkBank/cards/biology/higher';
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
    // Said once, under route B's heading, not under each of its menus.
    expect(screen.getAllByText(ROUTE_LOCKED_NOTE)).toHaveLength(1);
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
    // Route A's four rows are locked, and say so once.
    expect(screen.getAllByText(ROUTE_LOCKED_NOTE)).toHaveLength(1);
  });

  test('eng-2014-hl-q5-c-i: a route that is one menu gets its heading, with no "Select all" for one row', () => {
    renderSession(card(ENGINEERING_HIGHER, 'eng-2014-hl-q5-c-i'));
    reveal();
    expect(screen.getByRole('heading', { name: 'Route A' })).toBeInTheDocument();
    expect(screen.getByRole('heading', { name: 'Route B' })).toBeInTheDocument();
    expect(screen.queryByRole('button', { name: /^Select all in/ })).not.toBeInTheDocument();
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
  test('each of the two statements is underlined; the printed "O" between them reads plain', () => {
    renderSession(card(SPANISH_HIGHER, 'es-2010-hl-b-5'));
    const question = screen.getByTestId('mark-bank-question-text');
    const marked = [...question.querySelectorAll('span')].filter(span => span.style.textDecorationLine === 'underline' || span.style.backgroundImage);
    expect(marked.map(span => span.textContent)).toEqual(['El invento más importante del siglo pasado.', 'El silencio no existe en el mundo moderno.']);
    expect(question.textContent).toContain('El invento más importante del siglo pasado.\nO\nEl silencio no existe en el mundo moderno.');
  });

  test('an either/or choice: one mark per alternative, the lead-in and the connector plain', () => {
    const marks = (text: string) => emphasisSegments(text).filter(s => s.marked).map(s => s.text);
    // es-2010-hl-a1b-4: the instruction stays plain, both phrases are marked.
    expect(marks('Explica (o expresa de otro modo) en ESPAÑOL una de las frases siguientes:\n...es de suma importancia... (paragraph 1)\nO\n…los voluntarios se encargan de que los ancianos se alimenten correctamente. (paragraph 5)'))
      .toEqual(['...es de suma importancia... (paragraph 1)', '…los voluntarios se encargan de que los ancianos se alimenten correctamente. (paragraph 5)']);
    // An alternative of two lines is marked on its first; the other branch takes as many lines.
    expect(marks('Lead-in.\nAlpha first.\nAlpha second.\nnó\nBeta first.\nBeta second.')).toEqual(['Alpha first.', 'Beta first.']);
    // A command word in an alternative is marked by the usual rule.
    expect(marks('Explain any two of the following metal properties: (i) Toughness.\nOR\n(i) Describe one application for robotics.'))
      .toEqual(['Explain any two of the following metal properties:', 'Describe one application for robotics.']);
    // No connector line: one mark, as before.
    expect(marks('El invento.\nEl silencio.')).toEqual(['El invento.']);
    // A connector with nothing after it is not a choice.
    expect(marks('A Private Company Limited by shares (LTD company).\nor')).toEqual(['A Private Company Limited by shares (LTD company).']);
    for (const text of ['A.\nO\nB.', 'x\n\nnó\n\ny\nz', 'Lead.\nA\nOR\nB\nor\nC']) {
      expect(emphasisSegments(text).map(s => s.text).join('')).toBe(text);
    }
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

describe('the falling-split sentence is said only of a split that falls', () => {
  test('eng-2024-hl-q8-c-ii ("4 + 4") no longer says the first answers are marked higher', () => {
    renderSession(card(ENGINEERING_HIGHER, 'eng-2024-hl-q8-c-ii'));
    reveal();
    expect(screen.queryByText(/higher than the rest/)).not.toBeInTheDocument();
  });

  test('a falling split keeps it (bio-2023-hl-q2-f, "2(5) + 5(2)")', () => {
    renderSession(card(BIOLOGY_HIGHER, 'bio-2023-hl-q2-f'));
    reveal();
    expect(screen.getByText(/higher than the rest/)).toBeInTheDocument();
  });

  test('reading the notation', () => {
    expect(splitSteps('2(5) + 5(2)')).toEqual([5, 5, 2, 2, 2, 2, 2]);
    expect(splitSteps('5 + (5 + 5)')).toEqual([5, 5, 5]);
    expect(splitSteps('[2 × 3]')).toEqual([3, 3]);
    expect(splitSteps('5+5.')).toEqual([5, 5]);
    expect(splitSteps('5+5 (two examples)')).toBeNull();
    expect(['4 + 4', '10 + 10 + 10', '5 × 1', '[3 + 3]'].map(uniformSplit)).toEqual([true, true, true, true]);
    expect(['4 + 3', '2(5) + 5(2)', '6(3) + 2', '4 + 2 + 2', '5 + 5 (two examples)'].map(uniformSplit)).toEqual([false, false, false, false, false]);
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
