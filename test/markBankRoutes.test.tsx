/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 *
 * Answer routes on a point card: labelled from the card data, introduced by OR, and
 * selected one route at a time (components/MarkBank/routes.ts, RouteHeading.tsx).
 */

import { describe, expect, test, vi } from 'vitest';
import { fireEvent, render, screen } from '@testing-library/react';

import SessionScreen, { marksClaimed } from '@/components/MarkBank/SessionScreen';
import { routeDisplayOrder, routeHeads, routeSelection } from '@/components/MarkBank/routes';
import type { MarkRow, SecQuestionCard } from '@/types/markBank';

vi.mock('@/components/PaperTrail/vaultDocs', () => ({ vaultPdf: vi.fn(() => new Promise(() => {})) }));

const row = (o: Partial<MarkRow> = {}): MarkRow => ({ id: 'r0', kind: 'point', verbatim: 'Oesophagus', marks: 2, ...o });
const card = (o: Partial<SecQuestionCard> = {}): SecQuestionCard => ({
  source: 'sec', kind: 'question',
  id: 'chem-2021-hl-q5-b-ii', subjectId: 'chemistry', level: 'higher',
  topicId: 'chemistry-1', conceptId: 'radius',
  year: 2021, paperFileid: 'LC022ALP000EV', section: 'A',
  questionRef: '2021 HL Q5(b)(ii)',
  questionText: 'How is atomic (covalent) radius defined?',
  tariffModel: { kind: 'fixed' }, totalMarks: 6,
  rows: [
    row({ id: 'a1', verbatim: 'half the internuclear distance of two atoms of same element', marks: 3, route: 'a' }),
    row({ id: 'a2', verbatim: 'joined by a single covalent bond', marks: 3, route: 'a' }),
    row({ id: 'b1', verbatim: 'half the internuclear distance between two atoms', marks: 3, route: 'b' }),
    row({ id: 'b2', verbatim: 'joined by a single homonuclear bond', marks: 3, route: 'b' }),
  ],
  schemeCitation: 'SEC marking scheme, Chemistry 2021 Higher Level',
  specVersion: 'lc-chemistry',
  qa: { gates: [], humanReviewedBy: 'al', humanReviewedAt: '2026-11-04' },
  ...o,
} as SecQuestionCard);

const renderSession = (c: SecQuestionCard) => render(
  <SessionScreen cards={[c]} subjectLabel="Chemistry" onGrade={vi.fn()} onFinish={vi.fn()} onExit={vi.fn()} />,
);
const reveal = () => fireEvent.click(screen.getByRole('button', { name: /Reveal the marking scheme/i }));

describe('answer routes are labelled from the card data', () => {
  test('a lettered route reads "Route A" and every later route is introduced by OR', () => {
    renderSession(card());
    reveal();
    expect(screen.getByRole('heading', { name: 'Route A' })).toBeInTheDocument();
    expect(screen.getByRole('heading', { name: 'Route B' })).toBeInTheDocument();
    expect(screen.getAllByText('or')).toHaveLength(1);
  });

  test('one-row routes are told apart by OR alone: the row is the branch', () => {
    // Agricultural Science 2023 HL Q6(b): Scald, Footrot, Shelly hoof, CODD.
    const c = card({
      totalMarks: 2,
      rows: ['Scald — Inflammation', 'Footrot — red moist skin', 'Shelly hoof — Overgrown feet'].map((verbatim, i) =>
        row({ id: `r${i}`, kind: 'alt', verbatim, marks: 2, route: verbatim.split(' — ')[0].toLowerCase() })),
    });
    renderSession(c);
    reveal();
    expect(screen.getAllByText('or')).toHaveLength(2);
    expect(screen.queryByRole('heading', { name: 'Footrot' })).not.toBeInTheDocument();
    expect(screen.queryByRole('button', { name: /^Select all/ })).not.toBeInTheDocument();
  });

  test('a locked row offers no "I had something like this", which would switch routes', () => {
    renderSession(card({ rows: card().rows.map(r => ({ ...r, kind: 'alt' as const })) }));
    reveal();
    expect(screen.getAllByRole('button', { name: 'I had something like this' })).toHaveLength(4);
    fireEvent.click(screen.getByRole('button', { name: /single covalent bond/ }));
    expect(screen.getAllByRole('button', { name: 'I had something like this' })).toHaveLength(1);
  });

  test('a printed heading the route rows share is the label', () => {
    const heads = routeHeads([
      row({ id: 'r1', verbatim: 'Method A diagram — (potted) plant and plastic bag', route: 'method-a' }),
      row({ id: 'r2', verbatim: 'Method A labels — plant/ plastic bag', route: 'method-a' }),
      row({ id: 'r3', verbatim: 'Method B diagram — pond weed and suitable container', route: 'method-b' }),
      row({ id: 'r4', verbatim: 'Method B labels — pond weed or Elodea', route: 'method-b' }),
    ]);
    expect([...heads.values()].map(h => h.label)).toEqual(['Method A', 'Method B']);
  });

  test('where any route lacks a printed heading, no route is given one; slug ids are numbered', () => {
    // History 2013 OL: three priced items OR "A free Constitution" for all six marks.
    const heads = routeHeads([
      row({ id: 'r1', verbatim: 'The spirit', route: 'priced-items' }),
      row({ id: 'r2', verbatim: 'content', route: 'priced-items' }),
      row({ id: 'r4', verbatim: 'A free Constitution', marks: 6, route: 'alternative' }),
    ]);
    expect([...heads.values()].map(h => h.label)).toEqual(['Route 1', 'Route 2']);
    const mixed = routeHeads([
      row({ id: 'r1', verbatim: 'chemical equilibrium: forward and reverse reactions', route: 'a' }),
      row({ id: 'r2', verbatim: 'concentrations of reactants and products', route: 'b' }),
    ]);
    expect([...mixed.values()].map(h => h.label)).toEqual(['Route A', 'Route B']);
  });

  test('a route the scheme interleaves is shown under one heading, row ids unchanged', () => {
    const rows = [
      row({ id: 'c', verbatim: 'magnet, (plotting) compass' }),
      row({ id: 'a1', verbatim: 'mark the dots', route: 'a' }),
      row({ id: 'b1', verbatim: 'sprinkle filings', route: 'b' }),
      row({ id: 'a2', verbatim: 'join the dots', route: 'a' }),
      row({ id: 'b2', verbatim: 'tap filings', route: 'b' }),
    ];
    expect(routeDisplayOrder(rows)).toEqual([0, 1, 3, 2, 4]);
    expect(routeDisplayOrder([row({ id: 'x' }), row({ id: 'y' })])).toEqual([0, 1]);
  });
});

describe('"Select all" acts on one route only', () => {
  test('the card-wide "Select all" is not offered on a route card', () => {
    renderSession(card());
    reveal();
    expect(screen.queryByRole('button', { name: /^Select all — I had them all$/ })).not.toBeInTheDocument();
  });

  test('each route selects itself and clears the other', () => {
    renderSession(card());
    reveal();
    fireEvent.click(screen.getByRole('button', { name: 'Select all in Route B' }));
    expect(screen.getByRole('button', { name: /between two atoms/ })).toHaveAttribute('aria-pressed', 'true');
    expect(screen.getByRole('button', { name: /homonuclear/ })).toHaveAttribute('aria-pressed', 'true');
    expect(screen.getByRole('button', { name: /of same element/ })).toHaveAttribute('aria-pressed', 'false');
    expect(screen.getByRole('button', { name: /single covalent bond/ })).toHaveAttribute('aria-pressed', 'false');
    expect(screen.getByText(/You claimed 6 of 6 marks/)).toBeInTheDocument();
    // Switching routes moves every tick across; nothing is left on route B.
    fireEvent.click(screen.getByRole('button', { name: 'Select all in Route A' }));
    expect(screen.getByRole('button', { name: /of same element/ })).toHaveAttribute('aria-pressed', 'true');
    expect(screen.getByRole('button', { name: /homonuclear/ })).toHaveAttribute('aria-pressed', 'false');
  });

  test('rows outside every route are claimed with whichever route is chosen', () => {
    const c = card({
      totalMarks: 9,
      rows: [...card().rows, row({ id: 'v', verbatim: 'v = l/t', marks: 3 })],
    });
    const { claims } = routeSelection(c.rows, 'a');
    expect(claims).toEqual({ a1: 'yes', a2: 'yes', b1: 'no', b2: 'no', v: 'yes' });
    expect(marksClaimed(c, claims)).toBe(9);
  });
});

