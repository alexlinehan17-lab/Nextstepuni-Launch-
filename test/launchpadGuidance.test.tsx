/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 */
import React from 'react';
import { describe, expect, test, vi } from 'vitest';
import { fireEvent, render, screen } from '@testing-library/react';

import LaunchpadGuidance, { type LaunchpadToolSummary } from '@/components/LaunchpadGuidance';
import {
  availableRecommendationGoals,
  recommendTool,
  type ToolRecommendation,
} from '@/components/launchpadGuidanceData';

const TOOLS: LaunchpadToolSummary[] = [
  { id: 'war-room', title: 'War Room', description: 'Choose a priority.', tag: 'Strategy', needsProfile: true },
  { id: 'planner', title: 'Spaced Repetition Timetable', description: 'Plan the week.', tag: 'Planner', needsProfile: true },
  { id: 'catch-up-lane', title: 'Catch-Up Lane', description: 'Recover a topic.', tag: 'Catch up', needsProfile: false },
  { id: 'paper-trail', title: 'Paper Trail', description: 'Find a paper.', tag: 'Exam archive', needsProfile: false },
];

describe('Launchpad guidance', () => {
  test('recommends only an available tool and uses the declared fallback order', () => {
    expect(recommendTool('priority', 'today', ['planner'])?.toolId).toBe('planner');
    expect(recommendTool('priority', 'today', ['catch-up-lane'])).toBeNull();

    const juniorGoals = availableRecommendationGoals(['catch-up-lane', 'paper-trail']);
    expect(juniorGoals.find(goal => goal.id === 'catch-up')?.options.map(option => option.id)).toContain('topic');
    expect(juniorGoals.find(goal => goal.id === 'points')).toBeUndefined();
  });

  test('explains tools in plain language and opens the selected tool', () => {
    const onOpenTool = vi.fn();
    render(
      <LaunchpadGuidance
        tools={TOOLS}
        recommendation={null}
        onRecommendationChange={vi.fn()}
        onOpenTool={onOpenTool}
      />,
    );

    fireEvent.click(screen.getByRole('button', { name: /Meet the tools/ }));
    expect(screen.getByRole('dialog')).toBeInTheDocument();
    expect(screen.getByText(/You have time to study but are unsure which subject or topic/)).toBeInTheDocument();
    expect(screen.getByText(/One clear priority, the reason it matters/)).toBeInTheDocument();

    fireEvent.click(screen.getByRole('button', { name: 'Open War Room' }));
    expect(onOpenTool).toHaveBeenCalledWith('war-room', true);
  });

  test('asks two questions, returns one decisive recommendation and can restart', () => {
    const onOpenTool = vi.fn();

    const Harness: React.FC = () => {
      const [recommendation, setRecommendation] = React.useState<ToolRecommendation | null>(null);
      return (
        <LaunchpadGuidance
          tools={TOOLS}
          recommendation={recommendation}
          onRecommendationChange={setRecommendation}
          onOpenTool={onOpenTool}
        />
      );
    };

    render(<Harness />);
    fireEvent.click(screen.getByRole('button', { name: /Recommend a tool/ }));
    fireEvent.click(screen.getByRole('button', { name: 'I don’t know what to study' }));
    expect(screen.getByText('Question 2 of 2')).toBeInTheDocument();

    fireEvent.click(screen.getByRole('button', { name: 'Give me one priority for today' }));
    expect(screen.getByRole('heading', { name: 'War Room' })).toBeInTheDocument();
    expect(screen.getByText(/You said/)).toHaveTextContent('Give me one priority for today');
    expect(screen.queryByText(/% match/i)).not.toBeInTheDocument();

    fireEvent.click(screen.getByRole('button', { name: 'Open War Room' }));
    expect(onOpenTool).toHaveBeenCalledWith('war-room', true);
    expect(screen.getByText('Your current recommendation')).toBeInTheDocument();
  });
});

