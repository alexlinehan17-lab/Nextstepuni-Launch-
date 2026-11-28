/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 *
 * Area 0, the frame: the phone's tab bar. Five places, always the same five in
 * the same order; the current one marked in ink (aria-current) for every
 * screen of the app; nothing that comes up over a screen is a place; the bar
 * steps aside while the on-screen keyboard is up (navigation.md, "Tab bar").
 */
import { readFileSync } from 'node:fs';
import { join } from 'node:path';
import { act, cleanup, fireEvent, render, screen } from '@testing-library/react';
import { afterEach, describe, expect, it, vi } from 'vitest';
import { Compass, House } from 'lucide-react';
import { TabBar } from '@/components/ui/Bars';
import { PLACE_IDS, isPlace, parentOf, placeOf, type PlaceId } from '@/utils/places';

afterEach(() => { cleanup(); vi.restoreAllMocks(); });

/** Every ViewState the app has (contexts/NavigationContext.tsx), plus Settings. */
const SCREENS: Array<[string, string | null, PlaceId | null]> = [
  ['tree', null, 'tree'],
  ['modules', null, 'tree'],
  ['category', null, 'tree'],
  ['module', null, 'tree'],
  ['learning-paths', null, 'tree'],
  ['year-plans', null, 'tree'],
  ['your-setup', null, 'tree'],
  ['accreditation', null, 'tree'],
  ['settings', null, 'tree'],
  ['my-direction', null, 'tree'],
  ['cut-content', null, 'tree'],
  ['wip-tools', null, 'tree'],
  ['jc-coming-soon', null, 'tree'],
  ['dashboard', null, 'dashboard'],
  ['insights', null, 'dashboard'],
  ['study-session', null, 'study-session'],
  ['my-journey', null, 'my-journey'],
  ['innovation-zone', null, 'innovation-zone'],
  ['innovation-zone', 'paper-trail', 'innovation-zone'],
  ['innovation-zone', 'planner', 'innovation-zone'],
  ['innovation-zone', 'mark-bank', 'innovation-zone'],
  ['onboarding', null, null],
];

describe('which place a screen belongs to', () => {
  it.each(SCREENS)('%s (tool %s) marks %s', (viewState, activeTool, place) => {
    expect(placeOf({ viewState, activeTool })).toBe(place);
  });

  it('has the five places in the agreed order', () => {
    expect(PLACE_IDS).toEqual(['tree', 'dashboard', 'study-session', 'my-journey', 'innovation-zone']);
  });

  it('knows a place from a page: the Launchpad is a place, a tool in it is a page', () => {
    for (const place of PLACE_IDS) expect(isPlace({ viewState: place })).toBe(true);
    expect(isPlace({ viewState: 'innovation-zone', activeTool: 'paper-trail' })).toBe(false);
    for (const page of ['modules', 'category', 'module', 'settings', 'year-plans', 'your-setup', 'insights', 'learning-paths']) {
      expect(isPlace({ viewState: page })).toBe(false);
    }
  });

  it('gives every page a parent and no place a parent', () => {
    for (const place of PLACE_IDS) expect(parentOf({ viewState: place })).toBeNull();
    expect(parentOf({ viewState: 'innovation-zone', activeTool: 'paper-trail' })).toEqual({ viewState: 'innovation-zone', activeTool: null });
    expect(parentOf({ viewState: 'module', currentCategory: 'exam-zone' })).toEqual({ viewState: 'category', currentCategory: 'exam-zone' });
    expect(parentOf({ viewState: 'module' })).toEqual({ viewState: 'modules' });
    expect(parentOf({ viewState: 'module', cameFromJourney: true })).toEqual({ viewState: 'innovation-zone', activeTool: 'journey' });
    expect(parentOf({ viewState: 'category', currentCategory: 'exam-zone' })).toEqual({ viewState: 'modules' });
    expect(parentOf({ viewState: 'insights' })).toEqual({ viewState: 'dashboard' });
    expect(parentOf({ viewState: 'settings' })).toEqual({ viewState: 'tree' });
    expect(parentOf({ viewState: 'year-plans' })).toEqual({ viewState: 'tree' });
  });
});

describe('the tab bar part', () => {
  const items = [
    { id: 'tree' as const, label: 'Home', icon: House },
    { id: 'innovation-zone' as const, label: 'Launch', icon: Compass, coach: 'launchpad' },
  ];

  it('marks only the current place and moves on a tap', () => {
    const onSelect = vi.fn();
    render(<TabBar label="Main navigation" items={items} current="innovation-zone" onSelect={onSelect} />);
    const bar = screen.getByRole('navigation', { name: 'Main navigation' });
    expect(bar.className).toContain('frame-foot');
    expect(screen.getByRole('button', { name: 'Launch' })).toHaveAttribute('aria-current', 'page');
    expect(screen.getByRole('button', { name: 'Home' })).not.toHaveAttribute('aria-current');
    expect(screen.getByRole('button', { name: 'Launch' })).toHaveAttribute('data-coach', 'launchpad');
    fireEvent.click(screen.getByRole('button', { name: 'Home' }));
    expect(onSelect).toHaveBeenCalledWith('tree');
  });

  it('steps aside while the keyboard is up on a touch screen', () => {
    vi.useFakeTimers();
    vi.spyOn(window, 'matchMedia').mockImplementation(query => ({
      matches: query.includes('pointer: coarse'), media: query, onchange: null,
      addEventListener: vi.fn(), removeEventListener: vi.fn(), addListener: vi.fn(), removeListener: vi.fn(), dispatchEvent: () => false,
    } as unknown as MediaQueryList));
    render(<><input aria-label="Search" /><TabBar label="Main navigation" items={items} current="tree" onSelect={vi.fn()} /></>);
    const field = screen.getByRole('textbox', { name: 'Search' });
    act(() => { field.focus(); vi.runAllTimers(); });
    expect(screen.queryByRole('navigation', { name: 'Main navigation' })).toBeNull();
    act(() => { field.blur(); vi.runAllTimers(); });
    expect(screen.getByRole('navigation', { name: 'Main navigation' })).toBeInTheDocument();
    vi.useRealTimers();
  });

  it('is drawn as agreed: ink mark, no orange, a 50px row over the home indicator', () => {
    const css = readFileSync(join(process.cwd(), 'components/ui/parts.css'), 'utf8');
    const tab = css.match(/\.ui-tab\[aria-current='page'\]::before\s*\{([^}]*)\}/)?.[1] ?? '';
    expect(tab).toContain('background: var(--ink-primary)');
    expect(css).toMatch(/\.ui-tabbar\[hidden\]\s*\{\s*display:\s*none;/);
    const frame = readFileSync(join(process.cwd(), 'components/ui/frame.css'), 'utf8');
    expect(frame).toMatch(/html\[data-tabbar\]\s*\{\s*--tabbar-h:\s*50px;/);
  });
});

describe('the app shell uses the shared tab bar', () => {
  const app = readFileSync(join(process.cwd(), 'App.tsx'), 'utf8');
  it('draws the phone bar with TabBar and marks the place from utils/places', () => {
    expect(app).toMatch(/<TabBar label="Main navigation" items=\{places\} current=\{placeOf\(\{ viewState, activeTool \}\)\}/);
    expect(app).not.toContain('editorial-nav-rule');
    expect(app).toMatch(/label: 'Home'[\s\S]*label: 'Progress'[\s\S]*label: 'Study'[\s\S]*label: 'Journey'[\s\S]*label: 'Launch'/);
  });
});
