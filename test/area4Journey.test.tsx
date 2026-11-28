/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 *
 * Area 4, Journey and the island welcome in the agreed look (c-world.html,
 * r5-b2.html "r5-journey-mode", "r5-island-welcome"): the one selection bar
 * (Island, Build, Fieldbook, Your year) under the name, "?" and the points; the
 * Fieldbook and Your year open in place and Island takes you back; a tile's card
 * is the shared sheet with one Close; the shared parts extended for it. The map's
 * drawing, panning and zooming and the island's points are not exercised here:
 * their own suites (paperIsland*, journey*) cover them, unchanged.
 */
import React from 'react';
import { act, cleanup, fireEvent, render, screen, within } from '@testing-library/react';
import { afterAll, afterEach, beforeAll, beforeEach, describe, expect, it, vi } from 'vitest';
import type * as Firestore from 'firebase/firestore';

const device = vi.hoisted(() => ({ phone: true }));
vi.mock('@/hooks/useMobileAppDesign', () => ({ useMobileAppDesign: () => device.phone, isMobileAppDesign: () => device.phone }));
vi.mock('firebase/firestore', async original => ({
  ...(await original<typeof Firestore>()),
  collection: (_db: unknown, path: string) => ({ collection: path }),
  doc: (_db: unknown, ...path: string[]) => ({ path: path.join('/') }),
  where: (field: string, op: string, value: unknown) => ({ where: [field, op, value] }),
  limit: (n: number) => ({ limit: n }),
  query: (source: unknown, ...constraints: unknown[]) => ({ source, constraints }),
  getDoc: vi.fn(), getDocs: vi.fn(), setDoc: vi.fn(),
}));
vi.mock('@/utils/logError', () => ({ logError: vi.fn() }));

import ProgressContext from '@/contexts/ProgressContext';
import { NavigationProvider } from '@/contexts/NavigationContext';
import JourneyView from '@/components/journey/JourneyView';
import JourneyWelcome from '@/components/journey/JourneyWelcome';
import { TopBar } from '@/components/ui/Bars';
import { Sheet } from '@/components/ui/Sheet';
import { DEMO_STUDENT_UID } from '@/data/devStudent';
import { sampleOwnPaperIsland } from '@/data/sampleYearIslands';

const scrollTo = HTMLElement.prototype.scrollTo;
beforeAll(() => { HTMLElement.prototype.scrollTo = vi.fn(); });
afterAll(() => { if (scrollTo) HTMLElement.prototype.scrollTo = scrollTo; else Reflect.deleteProperty(HTMLElement.prototype, 'scrollTo'); });
beforeEach(() => { device.phone = true; window.history.replaceState(null, '', '/?view=my-journey'); });
afterEach(cleanup);
const settle = (ms = 400) => act(async () => { await new Promise(resolve => setTimeout(resolve, ms)); });

function Journey({ welcome = true }: { welcome?: boolean }) {
  const [doc, setDoc] = React.useState<Record<string, unknown>>(() => ({ pointsData: { totalEarned: 1460, totalSpent: 0 }, paperIsland: sampleOwnPaperIsland() }));
  const update = React.useCallback((updater: (current: Record<string, unknown>) => Record<string, unknown>) => setDoc(current => updater(current)), []);
  const reload = React.useCallback(() => {}, []);
  const value = React.useMemo(() => ({ rawProgressDoc: doc, updateDemoProgress: update, reloadProgress: reload }) as unknown as NonNullable<React.ContextType<typeof ProgressContext>>, [doc, update, reload]);
  // The island is one of the five places: in the app's navigation it has no leave control.
  return (
    <NavigationProvider><ProgressContext.Provider value={value}>
      <JourneyView user={{ uid: DEMO_STUDENT_UID, name: 'Demo Student', avatar: 'star-crew:maker', school: 'marino', yearGroup: '5th' }}
        hasSeenWelcome={welcome} onDismissWelcome={vi.fn()} onBack={vi.fn()} northStar={null} onOpenNorthStar={vi.fn()} pointsBalance={0} onPointsReload={vi.fn()} />
    </ProgressContext.Provider></NavigationProvider>
  );
}
const bar = () => within(screen.getByRole('radiogroup', { name: 'Journey sections' }));
const isChosen = (name: string) => expect(bar().getByRole('radio', { name })).toHaveAttribute('aria-checked', 'true');

describe('Journey, the frame', () => {
  it('a place with the name, "?" and the points in one row, and no wordmark, Home link or floating second bar', async () => {
    render(<Journey />);
    expect(await screen.findByRole('heading', { level: 1, name: 'My Island' })).toBeInTheDocument();
    expect(screen.getByRole('button', { name: 'How Journey works' })).toBeInTheDocument();
    expect(screen.getByRole('button', { name: /^Your balance: \d+ Journey Points$/ })).toBeInTheDocument();
    expect(bar().getAllByRole('radio').map(item => item.textContent)).toEqual(['Island', 'Build', 'Fieldbook', 'Your year']);
    isChosen('Island');
    expect(screen.queryByRole('button', { name: /^Back/ })).toBeNull();
    expect(screen.queryByRole('button', { name: /^(← )?Home$/ })).toBeNull();
    expect(screen.queryByText('nextstepuni')).toBeNull();
    expect(document.querySelector('.island-dock, .year-entry, .coast-done, .journey-build-heading')).toBeNull();
  });

  it('the Fieldbook, Build and Your year open from the bar, and Island takes you back', async () => {
    render(<Journey />);
    fireEvent.click(await screen.findByRole('radio', { name: 'Fieldbook' }));
    isChosen('Fieldbook');
    const page = screen.getByRole('region', { name: 'Your fieldbook' });
    expect(within(page).getByRole('heading', { name: /Things found\s*along the way\./ })).toBeInTheDocument();
    expect(within(page).getByText('along the way.').tagName).toBe('EM');
    // Stories, Visitors and Wonder tiles are words with an ink line.
    const words = within(page).getByRole('radiogroup', { name: 'Fieldbook sections' });
    fireEvent.click(within(words).getByRole('radio', { name: 'Visitors' }));
    expect(within(words).getByRole('radio', { name: 'Visitors' })).toHaveAttribute('aria-checked', 'true');
    // No pop-up: the Fieldbook opens in place, with no Close of its own.
    expect(screen.queryByRole('dialog')).toBeNull();

    fireEvent.click(bar().getByRole('radio', { name: 'Build' }));
    isChosen('Build');
    expect(document.querySelector('.journey-paper.is-building')).not.toBeNull();
    expect(screen.getByRole('heading', { name: 'A little more of your world.' })).toBeInTheDocument();
    expect(screen.queryByText('Done building')).toBeNull();

    fireEvent.click(bar().getByRole('radio', { name: 'Your year' }));
    isChosen('Your year');
    expect(document.querySelector('.journey-paper.is-building')).toBeNull();
    expect(document.querySelector('.jm-page .year-book')).not.toBeNull();

    fireEvent.click(bar().getByRole('radio', { name: 'Island' }));
    isChosen('Island');
    expect(document.querySelector('.jm-page')).toBeNull();
    expect(screen.queryByRole('region', { name: 'Your fieldbook' })).toBeNull();
  });

  it('a story in the Fieldbook still finds its way: it takes you into Build at the right corner', async () => {
    render(<Journey />);
    fireEvent.click(await screen.findByRole('radio', { name: 'Fieldbook' }));
    fireEvent.click(screen.getAllByText('Show me the way')[0].closest('button')!);
    isChosen('Build');
    expect(screen.getByText('Your next discovery.')).toBeInTheDocument();
  });

  it('a tile’s card is a sheet that closes from its one Close, at its top left', async () => {
    render(<Journey />);
    fireEvent.click((await screen.findAllByRole('button', { name: /^Inspect / }))[0]);
    const card = await screen.findByRole('dialog');
    const buttons = within(card).getAllByRole('button');
    expect(buttons[0]).toHaveAccessibleName('Close');
    expect(within(card).getAllByRole('button', { name: /Close/ })).toHaveLength(1);
    expect(within(card).getByText('Part of your world')).toBeInTheDocument();
    fireEvent.click(buttons[0]);
    await settle();
    expect(screen.queryByRole('dialog')).toBeNull();
    isChosen('Island');
  });

  it('on a laptop: "How it works" at the left end of the one bar, the selection bar in the middle, the points at the right', async () => {
    device.phone = false;
    render(<Journey />);
    const header = (await screen.findByRole('radiogroup', { name: 'Journey sections' })).closest('header')!;
    const [lead, middle, end] = Array.from(header.querySelectorAll('.ui-bar-row > *'));
    expect(lead).toHaveTextContent('How it works');
    expect(middle).toHaveClass('ui-bar-mid--control');
    expect(within(middle as HTMLElement).getByRole('radiogroup')).toBeInTheDocument();
    expect(end).toHaveTextContent(/JP$/);
    expect(screen.getByRole('heading', { level: 1, name: 'My Island' })).toHaveClass('sr-only');
  });
});

describe('the island welcome', () => {
  it('is the shared sheet: Close first at its top left, the bold headline, "Explore my island" charcoal', async () => {
    const dismiss = vi.fn();
    render(<JourneyWelcome hasSeenWelcome={false} onDismissWelcome={dismiss} />);
    const sheet = await screen.findByRole('dialog', { name: 'How it works' });
    expect(within(sheet).getAllByRole('button')[0]).toHaveAccessibleName('Close Journey introduction');
    expect(within(sheet).getByRole('heading', { name: /Your effort\.\s*A world of\s*your own\./ })).toHaveClass('jw-title');
    const explore = within(sheet).getByRole('button', { name: 'Explore my island' });
    expect(explore).toHaveClass('ui-btn--main');
    fireEvent.click(explore);
    expect(dismiss).toHaveBeenCalledOnce();
  });

  it('on a laptop it is a wide window in two columns with the reminder under the button', async () => {
    device.phone = false;
    render(<JourneyWelcome hasSeenWelcome={false} onDismissWelcome={vi.fn()} trigger="text" />);
    const sheet = await screen.findByRole('dialog', { name: 'How it works' });
    expect(sheet).toHaveClass('journey-welcome-sheet--wide');
    expect(within(sheet).getByText('Here’s how it works')).toBeInTheDocument();
    expect(within(sheet).getByText('Revisit this guide any time with “How it works”.')).toBeInTheDocument();
    expect(screen.getByRole('button', { name: 'How Journey works' })).toHaveTextContent('How it works');
  });
});

describe('shared parts extended for Journey', () => {
  it('TopBar: a lead at the left end and a control in the middle, with the action at the right', () => {
    render(<TopBar lead={<button type="button">How it works</button>} center={<div role="radiogroup" aria-label="Sections" />} action={<button type="button">5 JP</button>} />);
    const row = document.querySelector('.ui-bar-row')!;
    expect(row.children[0]).toHaveTextContent('How it works');
    expect(row.children[1]).toHaveClass('ui-bar-mid--control');
    expect(within(row.children[1] as HTMLElement).getByRole('radiogroup')).toBeInTheDocument();
    expect(row.children[2]).toHaveTextContent('5 JP');
    expect(row.querySelector('h1')).toBeNull();
  });

  it('Sheet: hideTitle keeps the title as the sheet\'s name and shows only Close in its head', () => {
    render(<Sheet open onClose={() => {}} title="The branch library" hideTitle><p>Books above the bustle.</p></Sheet>);
    const sheet = screen.getByRole('dialog', { name: 'The branch library' });
    expect(within(sheet).getByRole('heading', { name: 'The branch library' })).toHaveClass('sr-only');
    expect(within(sheet).getAllByRole('button')).toHaveLength(1);
  });
});
