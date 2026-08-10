/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 */
import React from 'react';
import { describe, expect, test, vi } from 'vitest';
import { fireEvent, render, screen } from '@testing-library/react';

import { JourneyOutcomeReport } from '@/components/AcademicJourneyGame';
import { INITIAL_GAME_STATE } from '@/components/journeySimulatorData';

describe('Academic Journey product-native outcome', () => {
  test('prioritises the result, action and expandable evidence', () => {
    const onRestart = vi.fn();
    const onSelectModule = vi.fn();
    render(
      <JourneyOutcomeReport
        endingId="END_PATHFINDER"
        gameState={{ ...INITIAL_GAME_STATE, resilience: 82, socialSupport: 74, energy: 44 }}
        history={[]}
        onRestart={onRestart}
        onSelectModule={onSelectModule}
      />,
    );

    expect(screen.getByRole('heading', { name: 'The Resilient Pathfinder' })).toBeInTheDocument();
    expect(screen.getByRole('heading', { name: 'What this journey says about you' })).toBeInTheDocument();
    expect(screen.getByRole('button', { name: /Open / })).toBeInTheDocument();
    expect(screen.getByText('Your five scores')).toBeInTheDocument();
    expect(screen.getByText('How you got here')).toBeInTheDocument();
    expect(screen.queryByText('Your Path')).not.toBeInTheDocument();

    fireEvent.click(screen.getByRole('button', { name: 'Try another path' }));
    expect(onRestart).toHaveBeenCalledTimes(1);
  });
});
