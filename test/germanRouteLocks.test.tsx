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
    // The data: two routes, b the alternative alone at its printed price.
    const b = c.rows.filter(r => r.route === 'b');
    expect(b).toHaveLength(1);
    expect(b[0].verbatim).toBe(routeB);
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
    expect(screen.getAllByText(ROUTE_LOCKED_NOTE)).toHaveLength(1);
  });
});
