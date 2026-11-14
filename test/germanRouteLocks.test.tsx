/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 *
 * German answers the scheme pays only on a route of their own (coordinator
 * ruling, 14 Nov 2026; menu route locks, #363). Each card offers route a, the
 * scheme's list or parts, and route b, the alternative it prints at its own
 * price, its condition quoted in the row note. A student who claims route b
 * cannot then claim from route a: the scheme pays one or the other.
 */

import { afterEach, describe, expect, test, vi } from 'vitest';
import { cleanup, fireEvent, render, screen } from '@testing-library/react';

import SessionScreen from '@/components/MarkBank/SessionScreen';
import { ROUTE_LOCKED_NOTE } from '@/components/MarkBank/RouteHeading';
import { CARDS as GERMAN_HIGHER } from '@/components/MarkBank/cards/german/higher';
import { CARDS as GERMAN_ORDINARY } from '@/components/MarkBank/cards/german/ordinary';
import { tariffReconciles } from '@/types/markBank';
import type { SecCard, SecQuestionCard } from '@/types/markBank';

vi.mock('@/components/PaperTrail/vaultDocs', () => ({ vaultPdf: vi.fn(() => new Promise(() => {})) }));
vi.mock('@/components/PaperTrail/CropView', () => ({ default: () => <div>Official PDF page</div> }));

afterEach(() => cleanup());

const deck: SecCard[] = [...GERMAN_HIGHER, ...GERMAN_ORDINARY];
const card = (id: string) => {
  const found = deck.find(c => c.id === id);
  if (!found) throw new Error(`no live card ${id}`);
  return found as SecQuestionCard;
};
const reveal = () => fireEvent.click(screen.getByRole('button', { name: /Reveal the marking scheme/i }));
const guidance = () => (document.getElementById('mark-bank-grade-guidance')?.textContent ?? '').split('You decide')[0];
/** The claim button of a row or menu option, or a part's 1-mark button ("Award 1 marks for Father/Husband/ Richard · Family"). */
const button = (text: string) => screen.getAllByRole('button')
  .find(b => b.getAttribute('aria-pressed') !== null && (b.textContent?.includes(text)
    || (b.getAttribute('aria-label') ?? '').startsWith(`Award 1 marks for ${text} · `))) as HTMLButtonElement;

/** card id, route b's claim, one claim on route a, route b's marks, the condition quoted. */
const ROUTED: Array<[string, string, string, number, string]> = [
  ['de-2021-hl-t2-2-b', 'everything', '… their day', 2, '“if only answer given”'],
  ['de-2022-ol-l4-3-ii', 'Triathlon', 'swimming', 2, '“if other answers are not given”'],
  ['de-2026-hl-l2-2', 'He repeats the word ‘help’', 'Sie müssen mir helfen!', 2, '“if no other marks are awarded”'],
  ['de-2020-hl-l1-3-ii', 'everyone', 'men and women', 1, '“if it is the only answer given”'],
  ['de-2016-ol-l4-1-ii', 'On Tuesday', 'Two', 2, '“N.B.: On Tuesday: 2 marks only”'],
  ['de-2013-hl-l1-3-i', 'From all over the world', 'Asia', 1, '“if only answer given”'],
  ['de-2012-ol-t2-1', 'Family — Parents', 'Father/Husband/ Richard', 2, '“Mother / Wife/ Helene (1) OR Parents (2)”'],
];

describe('German route locks: route b ticked, route a locked', () => {
  test.each(ROUTED)('%s: route b "%s" locks route a', (id, routeB, routeA, marks, condition) => {
    const c = card(id);
    // The data: route b holds the alternative at its printed price, its
    // condition quoted (on 2012 OL beside the field's other part, "Daughter").
    const b = c.rows.filter(r => r.route === 'b' && r.verbatim === routeB);
    expect(b).toHaveLength(1);
    expect(b[0].marks).toBe(marks);
    expect(b[0].contextNote).toContain(condition);
    expect(c.rows.some(r => r.route === 'a')).toBe(true);
    expect(tariffReconciles(c)).toBe(true);

    render(<SessionScreen cards={[c]} subjectLabel="German" onGrade={vi.fn()} onFinish={vi.fn()} onExit={vi.fn()} />);
    reveal();
    fireEvent.click(button(routeB));
    expect(button(routeB)).toHaveAttribute('aria-pressed', 'true');
    expect(guidance()).toContain(`You claimed ${marks} of ${c.totalMarks} marks`);
    const a = button(routeA);
    expect(a).toBeDisabled();
    fireEvent.click(a);
    expect(button(routeA)).toHaveAttribute('aria-pressed', 'false');
    expect(guidance()).toContain(`You claimed ${marks} of ${c.totalMarks} marks`);
    // Said once under each route not taken.
    expect(screen.getAllByText(ROUTE_LOCKED_NOTE)).toHaveLength(new Set(c.rows.map(r => r.route).filter(Boolean)).size - 1);
  });

  test('de-2012-ol-t2-1: route c "3 (people)" locks routes a and b, and claims 3', () => {
    const c = card('de-2012-ol-t2-1');
    const routeC = c.rows.filter(r => r.route === 'c');
    expect(routeC.map(r => [r.verbatim, r.marks, r.alone])).toEqual([['Family — 3 (people)', 3, undefined]]);
    expect(routeC[0].contextNote).toContain('“N.B: Accept 3 (people) for 3 marks”');
    // "Daughter" is paid on routes a and b, never beside route c: no route pays more than the field's 3.
    expect(c.rows.filter(r => r.verbatim === 'Family — Daughter').map(r => [r.id, r.route]))
      .toEqual([['r-4', 'a'], ['r-4-b', 'b']]);
    expect(tariffReconciles(c)).toBe(true);

    render(<SessionScreen cards={[c]} subjectLabel="German" onGrade={vi.fn()} onFinish={vi.fn()} onExit={vi.fn()} />);
    reveal();
    fireEvent.click(button('Family — 3 (people)'));
    expect(button('Family — 3 (people)')).toHaveAttribute('aria-pressed', 'true');
    expect(guidance()).toContain(`You claimed 3 of ${c.totalMarks} marks`);
    for (const other of ['Father/Husband/ Richard', 'Family — Parents', 'Family — Daughter']) {
      for (const b of screen.getAllByRole('button').filter(x => x.getAttribute('aria-pressed') !== null
        && (x.textContent?.includes(other) || (x.getAttribute('aria-label') ?? '').startsWith(`Award 1 marks for ${other} · `)))) {
        expect(b).toBeDisabled();
        fireEvent.click(b);
        expect(b).toHaveAttribute('aria-pressed', 'false');
      }
    }
    expect(guidance()).toContain(`You claimed 3 of ${c.totalMarks} marks`);
    expect(screen.getAllByText(ROUTE_LOCKED_NOTE)).toHaveLength(2);
  });
});
