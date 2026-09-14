import React from 'react';
import { afterEach, describe, expect, it } from 'vitest';
import { cleanup, fireEvent, render, screen, within } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import JourneyIsland from '../components/landing/journey/JourneyIsland';
import { INITIAL_ISLAND, openEdges, placePreviewTile, previewView } from '../components/landing/journey/islandPreview';

afterEach(cleanup);

describe('Journey landing preview', () => {
  it('places the chosen artwork, supports undo and restores the starting island', () => {
    render(<JourneyIsland />);
    expect(screen.getByRole('button', { name: 'Undo' })).toBeDisabled();
    fireEvent.click(screen.getByRole('button', { name: 'Choose The orange lantern' }));
    expect(screen.getByRole('button', { name: 'Choose The orange lantern' })).toHaveAttribute('aria-pressed', 'true');
    fireEvent.click(screen.getByRole('button', { name: 'Place The orange lantern at open edge 6' }));
    expect(screen.getByText('4 tiles. Plenty of room to grow.')).toBeInTheDocument();
    expect(within(screen.getByRole('group', { name: 'Your island preview' })).getByText(/On your island:/)).toHaveTextContent('The orange lantern');
    fireEvent.click(screen.getByRole('button', { name: 'Choose Wild meadow' }));
    fireEvent.click(screen.getAllByRole('button', { name: /Place Wild meadow/ })[0]);
    expect(screen.getByText('5 tiles. Plenty of room to grow.')).toBeInTheDocument();
    fireEvent.click(screen.getByRole('button', { name: 'Undo' }));
    expect(screen.getByText('4 tiles. Plenty of room to grow.')).toBeInTheDocument();
    expect(within(screen.getByRole('group', { name: 'Your island preview' })).getByText(/On your island:/)).not.toHaveTextContent('Wild meadow');
    fireEvent.click(screen.getByRole('button', { name: 'Start again' }));
    expect(screen.getByText('3 tiles. Plenty of room to grow.')).toBeInTheDocument();
    expect(screen.getByRole('button', { name: 'Undo' })).toBeDisabled();
    expect(INITIAL_ISLAND).toHaveLength(3);
  });

  it('lets the keyboard select, place and continue building without losing focus', async () => {
    const user = userEvent.setup();
    render(<JourneyIsland />);
    screen.getByRole('button', { name: 'Choose Stillwater pond' }).focus();
    await user.keyboard('{Enter}');
    expect(document.activeElement).toHaveAccessibleName('Place Stillwater pond at open edge 1');
    await user.keyboard('{Enter}');
    expect(screen.getByText('4 tiles. Plenty of room to grow.')).toBeInTheDocument();
    expect(document.activeElement).toHaveAccessibleName('Place Stillwater pond at open edge 1');
    await user.keyboard(' ');
    expect(screen.getByText('5 tiles. Plenty of room to grow.')).toBeInTheDocument();
  });

  it('rejects disconnected cells, occupied cells and a rapid duplicate placement', () => {
    expect(placePreviewTile(INITIAL_ISLAND, '0,0', 'meadow')).toBe(INITIAL_ISLAND);
    expect(placePreviewTile(INITIAL_ISLAND, '100,100', 'meadow')).toBe(INITIAL_ISLAND);
    const built = placePreviewTile(INITIAL_ISLAND, '-2,0', 'treehouse');
    expect(built).toHaveLength(4);
    expect(placePreviewTile(built, '-2,0', 'water')).toBe(built);
  });

  it('keeps adding buildable neighbours to the left and fits all targets on narrow screens', () => {
    let island = INITIAL_ISLAND;
    for (let q = -2; q >= -8; q--) {
      expect(openEdges(island).some(cell => cell.key === `${q},0`)).toBe(true);
      island = placePreviewTile(island, `${q},0`, 'woodland');
    }
    const edges = openEdges(island);
    expect(edges.some(cell => cell.key === '-9,0')).toBe(true);
    expect(new Set(edges.map(cell => cell.key)).size).toBe(edges.length);
    for (const aspect of [390 / 420, 1440 / 580]) {
      const view = previewView(island, aspect);
      for (const edge of edges) {
        expect(edge.x - 84).toBeGreaterThanOrEqual(view.x);
        expect(edge.x + 84).toBeLessThanOrEqual(view.x + view.width);
        expect(edge.y - 56).toBeGreaterThanOrEqual(view.y);
        expect(edge.y + 56).toBeLessThanOrEqual(view.y + view.height);
      }
    }
  });
});
