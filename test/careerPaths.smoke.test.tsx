/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 *
 * Render smoke for the Career Paths deck. The persistence hook and the shared
 * InnovationData context are mocked so the tool renders without Firebase.
 */
import { describe, test, expect, vi } from 'vitest';
import { render, screen } from '@testing-library/react';

vi.mock('@/hooks/useCareerPaths', () => ({
  useCareerPaths: () => ({
    state: { seenIds: [], savedIds: [], updatedAt: '' },
    isLoaded: true,
    markSeen: vi.fn(),
    toggleSaved: vi.fn(),
  }),
}));
vi.mock('@/contexts/InnovationDataContext', () => ({
  useInnovationData: () => ({ futureFinderPicks: [] }),
}));

import CareerPaths from '@/components/CareerPaths';

describe('Career Paths', () => {
  test('renders the deck intro without crashing', () => {
    render(<CareerPaths uid="test-uid" />);
    expect(screen.getByText(/Swipe through real careers/i)).toBeInTheDocument();
  });
});
