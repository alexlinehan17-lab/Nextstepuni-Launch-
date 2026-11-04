/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 *
 * Year islands, client side: the query the rules can verify, the sharing
 * switch, the list and its states, and a classmate's island that can only be
 * looked at.
 */
import React from 'react';
import { act, fireEvent, render, renderHook, screen, waitFor } from '@testing-library/react';
import { afterAll, beforeAll, beforeEach, describe, expect, it, vi } from 'vitest';
import type * as Firestore from 'firebase/firestore';

const fs = vi.hoisted(() => ({
  getDoc: vi.fn(),
  getDocs: vi.fn(),
  setDoc: vi.fn(),
}));
vi.mock('firebase/firestore', async original => ({
  ...(await original<typeof Firestore>()),
  collection: (_db: unknown, path: string) => ({ collection: path }),
  doc: (_db: unknown, ...path: string[]) => ({ path: path.join('/') }),
  where: (field: string, op: string, value: unknown) => ({ where: [field, op, value] }),
  limit: (n: number) => ({ limit: n }),
  query: (source: unknown, ...constraints: unknown[]) => ({ source, constraints }),
  getDoc: fs.getDoc,
  getDocs: fs.getDocs,
  setDoc: fs.setDoc,
}));
vi.mock('../utils/logError', () => ({ logError: vi.fn() }));

import ProgressContext from '../contexts/ProgressContext';
import { useYearIslands } from '../hooks/useYearIslands';
import { YearIslandsBook, type YearIslandsBookProps } from '../components/journey/year/YearIslandsBook';
import { ClassmateIsland } from '../components/journey/year/ClassmateIsland';
import { byName, cohortLabel, islandPieces, parseYearIsland, type YearIsland } from '../components/journey/year/yearIslands';
import { sampleOwnPaperIsland, sampleYearIslands } from '../data/sampleYearIslands';
import JourneyView from '../components/journey/JourneyView';
import { DEMO_STUDENT_UID } from '../data/devStudent';

const projection = (extra: Record<string, unknown> = {}) => ({
  schemaVersion: 2,
  name: 'Cian',
  avatar: 'star-crew:skater',
  school: 'marino',
  yearGroup: '5th',
  tiles: [{ q: 0, r: 0, kind: 'home' }, { q: 1, r: 0, kind: 'meadow', edge: { variant: 'small-bite', seed: 3 } }],
  tileCount: 2,
  ...extra,
});
const snap = (data: Record<string, unknown> | undefined) => ({ data: () => data, exists: () => data !== undefined });

describe('reading a classmate projection', () => {
  it('accepts schema 2 and refuses schema 1 or a missing year', () => {
    expect(parseYearIsland('a', projection())).toMatchObject({ uid: 'a', name: 'Cian', yearGroup: '5th', tileCount: 2 });
    expect(parseYearIsland('a', { ...projection(), schemaVersion: 1 })).toBeNull();
    expect(parseYearIsland('a', projection({ yearGroup: 'graduated' }))).toBeNull();
    expect(parseYearIsland('a', projection({ tiles: [] }))).toBeNull();
  });

  it('draws a tile kind this app does not know yet as meadow, keeping the island’s shape', () => {
    const parsed = parseYearIsland('a', projection({ tiles: [{ q: 0, r: 0, kind: 'home' }, { q: 1, r: 0, kind: 'tile-from-the-future' }] }));
    expect(parsed!.tiles[1]).toEqual({ q: 1, r: 0, kind: 'meadow' });
  });

  it('labels the cohort the way students say it', () => {
    expect(cohortLabel('marino', '5th')).toBe('5th Year at Marino');
    expect(cohortLabel('marino', 'TY')).toBe('Transition Year at Marino');
    expect(cohortLabel('marino', 'LCA1')).toBe('LCA Year 1 at Marino');
    expect(cohortLabel('marino', undefined)).toBe('Marino');
  });

  it('sorts by first name and draws landmarks the island has reached', () => {
    const names = sampleYearIslands().sort(byName).map(c => c.name);
    expect(names).toEqual([...names].sort((a, b) => a.localeCompare(b, 'en-IE')));
    const reached = islandPieces([{ q: 0, r: 0, kind: 'home' }, { q: -4, r: -2, kind: 'meadow' }]);
    expect(reached.some(cell => cell.kind === 'ruins')).toBe(true);
  });
});

describe('useYearIslands', () => {
  beforeEach(() => {
    fs.getDoc.mockReset();
    fs.getDocs.mockReset();
    fs.setDoc.mockReset().mockResolvedValue(undefined);
  });

  it('loads nothing until the panel opens', () => {
    renderHook(() => useYearIslands('me', { enabled: false }));
    expect(fs.getDoc).not.toHaveBeenCalled();
    expect(fs.getDocs).not.toHaveBeenCalled();
  });

  it('queries its own school AND year, from its own profile, and leaves itself out', async () => {
    fs.getDoc.mockResolvedValue(snap({ school: 'marino', yearGroup: '5th' }));
    fs.getDocs.mockResolvedValue({ docs: [
      { id: 'me', data: () => projection({ name: 'Me' }) },
      { id: 'zz', data: () => projection({ name: 'Saoirse' }) },
      { id: 'aa', data: () => projection({ name: 'Aoife' }) },
      { id: 'old', data: () => ({ schemaVersion: 1, school: 'marino' }) },
    ] });
    const { result } = renderHook(() => useYearIslands('me', { enabled: true }));
    await waitFor(() => expect(result.current.status).toBe('ready'));
    expect(fs.getDoc).toHaveBeenCalledWith({ path: 'users/me' });
    expect(fs.getDocs.mock.calls[0][0]).toEqual({
      source: { collection: 'islandPublic' },
      constraints: [{ where: ['school', '==', 'marino'] }, { where: ['yearGroup', '==', '5th'] }, { limit: 300 }],
    });
    expect(result.current.classmates.map(c => c.name)).toEqual(['Aoife', 'Saoirse']);
    expect(result.current.cohort).toEqual({ school: 'marino', yearGroup: '5th' });
    expect(result.current.visibility).toBe('year');
    expect(result.current.visibilityKnown).toBe(true);
  });

  it('copies a year recorded only at onboarding onto the profile, then uses it', async () => {
    fs.getDoc.mockResolvedValue(snap({ school: 'marino' }));
    fs.getDocs.mockResolvedValue({ docs: [] });
    const value = { rawProgressDoc: { subjectProfile: { yearGroup: '6th' } } } as unknown as NonNullable<React.ContextType<typeof ProgressContext>>;
    const wrapper = ({ children }: { children: React.ReactNode }) => <ProgressContext.Provider value={value}>{children}</ProgressContext.Provider>;
    const { result } = renderHook(() => useYearIslands('me', { enabled: true }), { wrapper });
    await waitFor(() => expect(result.current.status).toBe('ready'));
    expect(fs.setDoc).toHaveBeenCalledWith({ path: 'users/me' }, { yearGroup: '6th' }, { merge: true });
    expect(fs.getDocs.mock.calls[0][0].constraints[1]).toEqual({ where: ['yearGroup', '==', '6th'] });
  });

  it.each([
    [{ yearGroup: '5th' }, 'no-school'],
    [{ school: 'marino' }, 'no-year'],
    [{ school: 'marino', yearGroup: 'graduated' }, 'graduated'],
  ])('stops before querying for %o', async (profile, status) => {
    fs.getDoc.mockResolvedValue(snap(profile));
    const { result } = renderHook(() => useYearIslands('me', { enabled: true }));
    await waitFor(() => expect(result.current.status).toBe(status));
    expect(fs.getDocs).not.toHaveBeenCalled();
  });

  it('reports a denied or failed read as an error that can be retried', async () => {
    fs.getDoc.mockResolvedValue(snap({ school: 'marino', yearGroup: '5th' }));
    fs.getDocs.mockRejectedValueOnce(new Error('permission-denied')).mockResolvedValue({ docs: [] });
    const { result } = renderHook(() => useYearIslands('me', { enabled: true }));
    await waitFor(() => expect(result.current.status).toBe('error'));
    act(() => result.current.reload());
    await waitFor(() => expect(result.current.status).toBe('ready'));
  });

  it('moves the sharing switch at once, saves it to the profile, and undoes only a rejected save', async () => {
    fs.getDoc.mockResolvedValue(snap({ school: 'marino', yearGroup: '5th', islandVisibility: 'hidden' }));
    fs.getDocs.mockResolvedValue({ docs: [] });
    const { result } = renderHook(() => useYearIslands('me', { enabled: true }));
    await waitFor(() => expect(result.current.visibility).toBe('hidden'));
    act(() => result.current.setVisibility('year'));
    expect(fs.setDoc).toHaveBeenLastCalledWith({ path: 'users/me' }, { islandVisibility: 'year' }, { merge: true });
    expect(result.current.visibility).toBe('year');
    // Offline: the write never settles, and the switch must not wait for it.
    fs.setDoc.mockReturnValueOnce(new Promise(() => {}));
    act(() => result.current.setVisibility('hidden'));
    expect(result.current.visibility).toBe('hidden');
    // A real rejection puts it back and says so.
    fs.setDoc.mockRejectedValueOnce(new Error('permission-denied'));
    act(() => result.current.setVisibility('year'));
    await waitFor(() => expect(result.current.visibility).toBe('hidden'));
    expect(result.current.visibilityError).toMatch(/did not save/);
  });
});

describe('the Your year panel', () => {
  const classmates = sampleYearIslands().sort(byName).slice(0, 3);
  const props = (extra: Partial<YearIslandsBookProps> = {}): YearIslandsBookProps => ({
    cohort: '5th Year at Marino', school: 'Marino', status: 'ready', classmates,
    visibility: 'year', visibilityKnown: true, visibilityError: '',
    onVisibility: vi.fn(), onVisit: vi.fn(), onRetry: vi.fn(), ...extra,
  });

  it('lists classmates by first name with a visit button each', () => {
    const onVisit = vi.fn();
    render(<YearIslandsBook {...props({ onVisit })} />);
    expect(screen.getByRole('heading', { name: '5th Year at Marino.' })).toBeInTheDocument();
    expect(screen.getByText('3 classmates are sharing an island')).toBeInTheDocument();
    fireEvent.click(screen.getByRole('button', { name: new RegExp(`^Visit ${classmates[1].name}’s island`) }));
    expect(onVisit).toHaveBeenCalledWith(classmates[1]);
  });

  it('shows sharing as a real switch, on by default, that turns off', () => {
    const onVisibility = vi.fn();
    const { rerender } = render(<YearIslandsBook {...props({ onVisibility })} />);
    const toggle = screen.getByRole('switch', { name: 'Show my island to my year' });
    expect(toggle).toHaveAttribute('aria-checked', 'true');
    expect(toggle).toHaveTextContent('On');
    fireEvent.click(toggle);
    expect(onVisibility).toHaveBeenCalledWith('hidden');
    rerender(<YearIslandsBook {...props({ visibility: 'hidden' })} />);
    expect(screen.getByRole('switch')).toHaveAttribute('aria-checked', 'false');
    expect(screen.getByText(/Your island is hidden/)).toBeInTheDocument();
  });

  it('never claims "On" before the real choice is known', () => {
    render(<YearIslandsBook {...props({ status: 'loading', visibilityKnown: false })} />);
    const toggle = screen.getByRole('switch');
    expect(toggle).toBeDisabled();
    expect(toggle).toHaveAttribute('aria-checked', 'false');
    expect(screen.getByRole('status', { name: /Finding your classmates/ })).toBeInTheDocument();
  });

  it('explains an empty year, a missing year and a failed load', () => {
    const onOpenSetup = vi.fn(), onRetry = vi.fn();
    const { rerender } = render(<YearIslandsBook {...props({ classmates: [] })} />);
    expect(screen.getByText('No classmates are sharing an island yet.')).toBeInTheDocument();
    rerender(<YearIslandsBook {...props({ status: 'no-year', onOpenSetup })} />);
    fireEvent.click(screen.getByRole('button', { name: /Set my school year/ }));
    expect(onOpenSetup).toHaveBeenCalled();
    rerender(<YearIslandsBook {...props({ status: 'error', onRetry })} />);
    fireEvent.click(screen.getByRole('button', { name: /Try again/ }));
    expect(onRetry).toHaveBeenCalled();
  });

  it('labels Demo Account classmates as invented', () => {
    render(<YearIslandsBook {...props({ sample: true })} />);
    expect(screen.getByText(/None of these are real students/)).toBeInTheDocument();
  });
});

describe('visiting a classmate’s island', () => {
  const showModal = HTMLDialogElement.prototype.showModal;
  beforeAll(() => { HTMLDialogElement.prototype.showModal = function showModalStub(this: HTMLDialogElement) { this.setAttribute('open', ''); }; });
  afterAll(() => { HTMLDialogElement.prototype.showModal = showModal; });
  const aoife: YearIsland = sampleYearIslands().find(c => c.name === 'Aoife')!;

  it('names the owner and offers only looking and leaving', () => {
    const onBack = vi.fn(), onOpenYear = vi.fn();
    render(<div className="journey-paper"><ClassmateIsland classmate={aoife} cohort="5th Year at Marino" onBack={onBack} onOpenYear={onOpenYear} /></div>);
    expect(screen.getByRole('group', { name: /^Aoife’s island, look only/ })).toBeInTheDocument();
    expect(screen.getByText('Visiting · look only')).toBeInTheDocument();
    expect(screen.getByText(`5th Year at Marino · ${aoife.tileCount} tiles`)).toBeInTheDocument();
    // Whole words: sticker names such as "The lantern keeper" are fine to inspect.
    expect(screen.queryByRole('button', { name: /\b(build|place|undo|swap|remove|keep)\b|open the chest/i })).toBeNull();
    expect(document.querySelectorAll('[data-open-corner]')).toHaveLength(0);
    fireEvent.click(screen.getByRole('button', { name: 'Back to your island' }));
    fireEvent.click(screen.getByRole('button', { name: 'Your year' }));
    expect(onBack).toHaveBeenCalled();
    expect(onOpenYear).toHaveBeenCalled();
  });

  it('describes a tile without offering to build one', () => {
    render(<div className="journey-paper"><ClassmateIsland classmate={aoife} cohort="5th Year at Marino" onBack={vi.fn()} onOpenYear={vi.fn()} /></div>);
    fireEvent.click(screen.getAllByRole('button', { name: /^Inspect / })[0]);
    expect(screen.getByText('ON AOIFE’S ISLAND')).toBeInTheDocument();
    expect(screen.queryByRole('button', { name: /Build another/ })).toBeNull();
  });
});

describe('year islands inside Journey (Demo Account, sample classmates)', () => {
  const showModal = HTMLDialogElement.prototype.showModal;
  const scrollTo = HTMLElement.prototype.scrollTo;
  beforeAll(() => {
    HTMLDialogElement.prototype.showModal = function showModalStub(this: HTMLDialogElement) { this.setAttribute('open', ''); };
    HTMLElement.prototype.scrollTo = vi.fn();
  });
  afterAll(() => {
    HTMLDialogElement.prototype.showModal = showModal;
    if (scrollTo) HTMLElement.prototype.scrollTo = scrollTo;
    else Reflect.deleteProperty(HTMLElement.prototype, 'scrollTo');
  });

  function Journey() {
    const [doc, setDoc] = React.useState<Record<string, unknown>>(() => ({ pointsData: { totalEarned: 1460, totalSpent: 0 }, paperIsland: sampleOwnPaperIsland() }));
    const update = React.useCallback((updater: (current: Record<string, unknown>) => Record<string, unknown>) => setDoc(current => updater(current)), []);
    const reload = React.useCallback(() => {}, []);
    const value = React.useMemo(() => ({ rawProgressDoc: doc, updateDemoProgress: update, reloadProgress: reload }) as unknown as NonNullable<React.ContextType<typeof ProgressContext>>, [doc, update, reload]);
    return (
      <ProgressContext.Provider value={value}>
        <JourneyView user={{ uid: DEMO_STUDENT_UID, name: 'Demo Student', avatar: 'star-crew:maker', school: 'marino', yearGroup: '5th' }}
          hasSeenWelcome onDismissWelcome={vi.fn()} onBack={vi.fn()} northStar={null} onOpenNorthStar={vi.fn()} pointsBalance={0} onPointsReload={vi.fn()} />
      </ProgressContext.Provider>
    );
  }

  it('opens Your year from the island, visits a classmate, and comes home', async () => {
    render(<Journey />);
    fireEvent.click(await screen.findByRole('button', { name: /^Your year: see your classmates' islands in 5th Year at Marino/ }));
    fireEvent.click(await screen.findByRole('button', { name: /^Visit Aoife’s island/ }));
    expect(screen.getByText('Aoife’s island')).toBeInTheDocument();
    expect(screen.queryByRole('button', { name: 'Build your island' })).toBeNull();
    fireEvent.click(screen.getByRole('button', { name: 'Back to your island' }));
    expect(screen.queryByText('Visiting · look only')).toBeNull();
    expect(screen.getByRole('button', { name: 'Build your island' })).toBeInTheDocument();
  });

  it('ends the visit when the student starts building from their own fieldbook', async () => {
    render(<Journey />);
    fireEvent.click(await screen.findByRole('button', { name: /^Your year:/ }));
    fireEvent.click(await screen.findByRole('button', { name: /^Visit Cian’s island/ }));
    expect(screen.getByText('Visiting · look only')).toBeInTheDocument();
    fireEvent.click(screen.getByRole('button', { name: 'Your character · open fieldbook' }));
    fireEvent.click(screen.getAllByText('Show me the way')[0].closest('button')!);
    await waitFor(() => expect(screen.queryByText('Visiting · look only')).toBeNull());
    expect(document.querySelector('.journey-paper.is-building')).not.toBeNull();
  });
});
