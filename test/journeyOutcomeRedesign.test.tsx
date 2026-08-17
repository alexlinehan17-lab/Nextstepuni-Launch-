/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 */
import React from 'react';
import { describe, expect, test, vi } from 'vitest';
import { fireEvent, render, screen } from '@testing-library/react';

import { JourneyOutcomeReport } from '@/components/AcademicJourneyGame';
import { STORY_DATA } from '@/components/journeySimulatorData';

describe('Academic Journey outcome dashboard', () => {
  const finalStats = {
    energy: 44,
    academicCap: 62,
    socialSupport: 74,
    systemSavvy: 58,
    resilience: 82,
  };

  test('presents a brand-native decision readout without decorative imagery', () => {
    const onRestart = vi.fn();
    const onSelectModule = vi.fn();
    const { container } = render(
      <JourneyOutcomeReport
        endingId="END_PATHFINDER"
        gameState={finalStats}
        history={[]}
        decisionsCount={12}
        onRestart={onRestart}
        onSelectModule={onSelectModule}
      />,
    );

    expect(screen.getByRole('heading', { name: 'The Adaptive Pathfinder' })).toBeInTheDocument();
    expect(screen.getByRole('heading', { name: 'Your decision profile' })).toBeInTheDocument();
    expect(screen.getByRole('img', { name: 'Academic journey decision profile' })).toBeInTheDocument();
    expect(screen.getByRole('heading', { name: 'Build Practical Planning' })).toBeInTheDocument();
    expect(screen.getByText('Four capability readout')).toBeInTheDocument();
    expect(screen.getAllByText('Energy reserve').length).toBeGreaterThan(0);
    expect(screen.getByText('A reflection, not a forecast.')).toBeInTheDocument();
    expect(screen.getByText('12')).toBeInTheDocument();
    expect(container.querySelector('img')).toBeNull();
    expect(screen.queryByText('Your five scores')).not.toBeInTheDocument();
    expect(screen.queryByText('How you got here')).not.toBeInTheDocument();
    expect(screen.queryByText('Paths not taken')).not.toBeInTheDocument();

    fireEvent.click(screen.getByRole('button', { name: 'Start with The Leaving Cert Points Protocol' }));
    expect(onSelectModule).toHaveBeenCalledWith('leaving-cert-strategy-protocol');

    fireEvent.click(screen.getByRole('button', { name: 'Explore another route' }));
    expect(onRestart).toHaveBeenCalledTimes(1);
  });

  test('shows only the decisions that materially shaped a completed playthrough', () => {
    render(
      <JourneyOutcomeReport
        endingId="END_PATHFINDER"
        gameState={finalStats}
        history={[
          {
            scene: STORY_DATA.FIRST_BAD_GRADE,
            choiceText: 'Ask for feedback and make a recovery plan.',
            effects: { resilience: 15, energy: -5 },
          },
        ]}
        onRestart={vi.fn()}
      />,
    );

    expect(screen.getByRole('heading', { name: 'Decisions that shaped the result' })).toBeInTheDocument();
    expect(screen.getByText('Ask for feedback and make a recovery plan.')).toBeInTheDocument();
    expect(screen.getByText('+2 Recovery Skills · -3 Energy Reserve')).toBeInTheDocument();
  });
});
