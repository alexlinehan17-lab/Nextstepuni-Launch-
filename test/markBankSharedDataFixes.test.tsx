/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 *
 * Shared content and data fixes (13 November 2026), each pinned on the live
 * card or index entry it changed:
 *  - two Engineering deferred cards filed under the topic their content is;
 *  - the 2021-2025 Higher Engineering OR cards priced as a whole, and
 *    Technology 2021 HL C4(a)(ii), carry one route per branch;
 *  - the eight Engineering rows held back from menus are menus;
 *  - Paper Trail names the Technology and DCG -015- booklets for the two
 *    sections they hold.
 */

import { afterEach, describe, expect, test, vi } from 'vitest';
import { cleanup, fireEvent, render, screen } from '@testing-library/react';

import SessionScreen from '@/components/MarkBank/SessionScreen';
import { CARDS as ENGINEERING_HIGHER } from '@/components/MarkBank/cards/engineering/higher';
import { CARDS as TECHNOLOGY_HIGHER } from '@/components/MarkBank/cards/technology/higher';
import { PAPER_TRAIL_INDEX } from '@/paperTrailData';
import type { SecCard, SecQuestionCard } from '@/types/markBank';

vi.mock('@/components/PaperTrail/vaultDocs', () => ({ vaultPdf: vi.fn(() => new Promise(() => {})) }));
vi.mock('@/components/PaperTrail/CropView', () => ({ default: () => <div>Official PDF page</div> }));

afterEach(() => cleanup());

const card = (deck: SecCard[], id: string) => {
  const found = deck.find(c => c.id === id);
  if (!found) throw new Error(`no live card ${id}`);
  return found as SecQuestionCard;
};
const renderSession = (c: SecCard) => render(
  <SessionScreen cards={[c]} subjectLabel="Mark Bank" onGrade={vi.fn()} onFinish={vi.fn()} onExit={vi.fn()} />,
);
const reveal = () => fireEvent.click(screen.getByRole('button', { name: /Reveal the marking scheme/i }));
const guidance = () => (document.getElementById('mark-bank-grade-guidance')?.textContent ?? '').split('You decide')[0];

describe('two Engineering deferred cards are filed under the topic their content is', () => {
  test('elastic against plastic deformation in metals is Properties and testing of materials, as the rest of Q3', () => {
    expect(card(ENGINEERING_HIGHER, 'eng-2022-hl-deferred-q3-b-ii').topicId).toBe('eng-3-8');
    expect(card(ENGINEERING_HIGHER, 'eng-2022-hl-deferred-q3-b-i').topicId).toBe('eng-3-8');
  });

  test('a transformer in a mobile phone charger is Electricity and electronics, as Q9(c)', () => {
    expect(card(ENGINEERING_HIGHER, 'eng-2023-hl-deferred-q9-b-iv').topicId).toBe('eng-2-16');
    expect(card(ENGINEERING_HIGHER, 'eng-2023-hl-deferred-q9-c-i').topicId).toBe('eng-2-16');
  });
});

const OR_CARDS = [
  'eng-2021-hl-q8-c-i', 'eng-2021-hl-q8-c-ii', 'eng-2021-hl-q9-c-i', 'eng-2021-hl-q9-c-ii',
  'eng-2022-hl-q6-c-i', 'eng-2022-hl-q6-c-ii', 'eng-2022-hl-q8-c-i', 'eng-2022-hl-q8-c-ii',
  'eng-2022-hl-q9-c-i', 'eng-2022-hl-q9-c-ii', 'eng-2023-hl-q6-c-i', 'eng-2023-hl-q6-c-ii',
  'eng-2023-hl-q8-c-i', 'eng-2023-hl-q8-c-ii', 'eng-2023-hl-q9-c-i', 'eng-2023-hl-q9-c-ii',
  'eng-2024-hl-q8-c-i', 'eng-2024-hl-q8-c-ii', 'eng-2024-hl-q9-c-i', 'eng-2024-hl-q9-c-ii',
  'eng-2025-hl-q8-c-i', 'eng-2025-hl-q8-c-ii',
];

describe('an OR card priced as a whole carries one route per branch', () => {
  test('all 22 Engineering cards: every row on route a, then route b', () => {
    for (const id of OR_CARDS) {
      const routes = card(ENGINEERING_HIGHER, id).rows.map(r => r.route).join('');
      expect(routes, id).toMatch(/^a+b+$/);
    }
  });

  test('eng-2022-hl-q6-c-i: the weld branch answered in full suggests Got it, and the AMR branch locks', () => {
    const c = card(ENGINEERING_HIGHER, 'eng-2022-hl-q6-c-i');
    renderSession(c);
    reveal();
    expect(screen.getByRole('heading', { name: 'Route A' })).toBeInTheDocument();
    expect(screen.getByRole('heading', { name: 'Route B' })).toBeInTheDocument();
    for (const r of c.rows.filter(row => row.route === 'a')) {
      fireEvent.click(screen.getByRole('button', { name: new RegExp(r.verbatim.slice(0, 24).replace(/[.*+?^${}()|[\]\\]/g, '\\$&')) }));
    }
    expect(guidance()).toContain('That looks like Got it.');
    expect(screen.getByRole('button', { name: /^Automatic charging zones/ })).toBeDisabled();
  });

  test('eng-2024-hl-q8-c-ii opens with the lubricants branch the scheme prints', () => {
    const rows = card(ENGINEERING_HIGHER, 'eng-2024-hl-q8-c-ii').rows;
    expect(rows[0]).toMatchObject({ id: 'r-5', route: 'a', verbatim: 'Lubricating materials: Oil, grease, graphite, PTFE, etc.' });
    expect(rows.slice(1).map(r => [r.id, r.route])).toEqual([['r-1', 'b'], ['r-2', 'b'], ['r-3', 'b'], ['r-4', 'b']]);
  });

  test('tech-2021-hl-c4a-ii: Fairtrade or CE, one branch each', () => {
    const c = card(TECHNOLOGY_HIGHER, 'tech-2021-hl-c4a-ii');
    expect(c.rows.map(r => [r.id, r.route])).toEqual([['r-1', 'a'], ['r-2', 'b']]);
    renderSession(c);
    reveal();
    fireEvent.click(screen.getByRole('button', { name: /^Fairtrade seeks/ }));
    expect(guidance()).toContain('That looks like Got it.');
    expect(screen.getByRole('button', { name: /^CE products must/ })).toBeDisabled();
  });
});

describe('the rows held back from menus are menus', () => {
  test('a route row: eng-2016-hl-q8-c-i offers its three energy conversions as one pick, on route b', () => {
    const row = card(ENGINEERING_HIGHER, 'eng-2016-hl-q8-c-i').rows.find(r => r.id === 'r-2')!;
    expect(row).toMatchObject({ kind: 'anyN', route: 'b', group: { claimMax: 1, perOption: 8 } });
    expect(row.group!.options[0]).toBe('Light energy to chemical energy.');
    renderSession(card(ENGINEERING_HIGHER, 'eng-2016-hl-q8-c-i'));
    reveal();
    expect(screen.queryByRole('button', { name: 'I had something like this' })).not.toBeInTheDocument();
  });

  test('a row priced with its question: eng-2023-hl-deferred-q9-b-iii has two one-pick menus with no price of their own', () => {
    const rows = card(ENGINEERING_HIGHER, 'eng-2023-hl-deferred-q9-b-iii').rows;
    expect(rows.map(r => [r.kind, r.marks, r.group?.claimMax, r.group?.options[0]])).toEqual([
      ['anyN', null, 1, 'Positive drive'], ['anyN', null, 1, 'Needs lubrication'],
    ]);
    renderSession(card(ENGINEERING_HIGHER, 'eng-2023-hl-deferred-q9-b-iii'));
    reveal();
    expect(screen.getAllByText('One of these')).toHaveLength(2);
  });

  test('all eight held rows are menus now', () => {
    const held: [string, string][] = [
      ['eng-2016-hl-q8-c-i', 'r-2'], ['eng-2017-hl-q7-c-ii', 'r-1'], ['eng-2017-hl-q7-c-ii', 'r-2'],
      ['eng-2019-hl-q8-c-ii', 'r-3'], ['eng-2020-hl-q8-c-ii', 'r-2'], ['eng-2020-hl-q8-c-ii', 'r-3'],
      ['eng-2023-hl-deferred-q9-b-iii', 'r-1'], ['eng-2023-hl-deferred-q9-b-iii', 'r-2'],
    ];
    for (const [id, rowId] of held) {
      expect(card(ENGINEERING_HIGHER, id).rows.find(r => r.id === rowId)?.kind, `${id} ${rowId}`).toBe('anyN');
    }
  });
});

describe('Paper Trail names the -015- booklet for both sections it holds', () => {
  const label = (subject: string, year: number, level: string, fileid: string) =>
    PAPER_TRAIL_INDEX[subject]
      ?.find(e => e.year === year && e.level === level && e.papers.some(p => p.doc?.f === fileid))
      ?.papers.find(p => p.doc?.f === fileid)?.label;

  test('Technology 2010-2018 and DCG 2012-2018 read "Section B&C", as 2019 onwards do', () => {
    expect(label('technology', 2018, 'higher', 'LC065ALP015EV.pdf')).toBe('Section B&C');
    expect(label('technology', 2009, 'ordinary', 'LC065GLP015IV.pdf')).toBe('Section B&C');
    expect(label('technology', 2019, 'higher', 'LC065ALP039EV.pdf')).toBe('Section B&C');
    expect(label('design-and-communication-graphics', 2018, 'higher', 'LC562ALP015EV.pdf')).toBe('Section B&C');
  });

  test('a booklet with no cover on disk to read keeps its label, and Spanish\'s loose sheet is Section B', () => {
    expect(label('design-and-communication-graphics', 2014, 'ordinary', 'LC562GLP015EV.pdf')).toBe('Section B');
    expect(label('spanish', 2018, 'higher', 'LC012ALP015EV.pdf')).toBe('Section B');
  });
});
