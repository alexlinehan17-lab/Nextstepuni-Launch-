/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 *
 * Smoke tests for the shared immersive-deck primitives (pure — no Firebase).
 */
import { describe, test, expect } from 'vitest';
import { render, screen } from '@testing-library/react';
import { CountUp } from '@/components/immersiveDeck/CountUp';
import { WORLDS, world } from '@/components/immersiveDeck/colorWorlds';

describe('immersiveDeck primitives', () => {
  test('CountUp renders the final formatted value', () => {
    render(<CountUp to={70} from={70} format={(n) => `€${n}k`} />);
    expect(screen.getByText('€70k')).toBeInTheDocument();
  });

  test('colour worlds are defined and white-text-safe', () => {
    expect(WORLDS.teal.bg).toMatch(/^#[0-9A-Fa-f]{6}$/);
    expect(world('teal').onBg).toBe('#FFFFFF');
    // every world exposes the full token set
    for (const w of Object.values(WORLDS)) {
      expect(w).toMatchObject({ bg: expect.any(String), deep: expect.any(String), glow: expect.any(String) });
    }
  });
});
