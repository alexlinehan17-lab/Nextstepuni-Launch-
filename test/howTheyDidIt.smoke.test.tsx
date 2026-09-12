/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 *
 * Render smoke for the How They Did It deck. The persistence hook is mocked so
 * the tool renders without Firebase — this catches the "tool crashes on mount"
 * class the pre-ship audit found.
 */
import { describe, test, expect, vi } from 'vitest';
import { render, screen } from '@testing-library/react';

vi.mock('@/hooks/useHowTheyDidIt', () => ({
  useHowTheyDidIt: () => ({
    state: { seenIds: [], savedIds: [], updatedAt: '' },
    isLoaded: true,
    markSeen: vi.fn(),
    toggleSaved: vi.fn(),
  }),
}));

import HowTheyDidIt from '@/components/HowTheyDidIt';

describe('How They Did It', () => {
  test('renders the story library and barrier filters without crashing', () => {
    render(<HowTheyDidIt uid="test-uid" />);
    expect(screen.getAllByRole('button', { name: /Read their story/i }).length).toBeGreaterThan(1);
    expect(screen.getByText('Everyone')).toBeInTheDocument();
  });
});
