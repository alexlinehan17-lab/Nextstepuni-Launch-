import React from 'react';
import { existsSync } from 'node:fs';
import path from 'node:path';
import { fireEvent, render, screen } from '@testing-library/react';
import { afterAll, beforeAll, describe, expect, it, vi } from 'vitest';
import { TileShelf } from '../components/journey/paper/MapControls';
import { TilePortrait } from '../components/journey/paper/TileArt';
import { vertices } from '../components/journey/paper/geometry';
import { applyPaperCommand, createPaperIsland, type PaperProgress } from '../functions/src/paperIslandModel';

describe('The quiet capybara in Journey', () => {
  const scrollTo = HTMLElement.prototype.scrollTo;
  beforeAll(() => { HTMLElement.prototype.scrollTo = vi.fn(); });
  afterAll(() => {
    if (scrollTo) HTMLElement.prototype.scrollTo = scrollTo;
    else Reflect.deleteProperty(HTMLElement.prototype, 'scrollTo');
  });

  it('can be selected from Little places with the shared price', () => {
    const choose = vi.fn();
    render(<TileShelf balance={300} credits={0} chosen="meadow" onChoose={choose} group="Little places" setGroup={vi.fn()} orientation="row" />);
    const capybara = screen.getByRole('button', { name: 'Choose The quiet capybara' });
    expect(capybara).toHaveTextContent('120 JP');
    fireEvent.click(capybara);
    expect(choose).toHaveBeenCalledWith('capybara');
  });

  it('saves the capybara, charges once, retains it when reopened, and refunds on undo', () => {
    const account: PaperProgress = {
      pointsData: { totalEarned: 300, totalSpent: 0 },
      paperIsland: createPaperIsland(),
    };
    const command = { action: 'place', kind: 'capybara', q: -2, r: 0, revision: 0, requestId: 'capybara-purchase-001' } as const;
    const placed = applyPaperCommand(account, command);
    expect(placed.totalSpent).toBe(120);
    expect(placed.state.tiles.at(-1)).toMatchObject({ kind: 'capybara', q: -2, r: 0, cost: 120 });
    const saved = { paperIsland: placed.state, pointsData: { totalEarned: placed.totalEarned, totalSpent: placed.totalSpent } };
    expect(applyPaperCommand(saved, command).totalSpent).toBe(120);
    expect(applyPaperCommand(saved, { action: 'open' }).state.tiles).toEqual(placed.state.tiles);
    const undo = applyPaperCommand(saved, { action: 'undo', revision: 1, requestId: 'capybara-undo-001' });
    expect(undo.totalSpent).toBe(0);
    expect(undo.state.tiles).toEqual(account.paperIsland!.tiles);
  });

  it('reduces the sprite and contains its base at the real tile edges without clipping its head', () => {
    const { container } = render(<TilePortrait kind="capybara" />);
    const sprite = container.querySelector('image')!;
    const source = sprite.getAttribute('href');
    const assetPath = path.join(process.cwd(), 'public', source!);
    expect(existsSync(assetPath), assetPath).toBe(true);
    const size = Number(sprite.getAttribute('width'));
    expect(size).toBeCloseTo(153.52);
    const clip = container.querySelector('clipPath')!;
    expect(sprite.getAttribute('clip-path')).toBe(`url(#${clip.id})`);
    const boundary = clip.querySelector('polygon')!.getAttribute('points')!.split(' ').map(point => {
      const [x, y] = point.split(',').map(Number);
      return { x, y };
    });
    expect(boundary.slice(2)).toEqual(vertices().slice(2, 5));
    expect(boundary[0].y).toBeLessThan(Number(sprite.getAttribute('y')));
  });
});
