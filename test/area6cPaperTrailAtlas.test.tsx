/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 *
 * Area 6c: Paper Trail's and Topic Atlas's other pieces on the shared parts.
 * The milestone celebration is a sheet whose own buttons are its way out; a
 * Physical Education task still saves to review, opens the full paper and
 * shows its marking scheme; the Politics practice feed still filters by year
 * and words and opens each marking guide. Each does what its old control did.
 */
import React from 'react';
import { afterEach, describe, expect, it, vi } from 'vitest';
import { act, cleanup, fireEvent, render, screen, within } from '@testing-library/react';
import MilestoneCelebration from '../components/PaperTrail/MilestoneCelebration';
import PhysicalEducationTaskCard from '../components/PaperTrail/PhysicalEducationTaskCard';
import PoliticsTopicFeed from '../components/PaperTrail/PoliticsTopicFeed';
import { PHYSICAL_EDUCATION_TASKS } from '../components/PaperTrail/physicalEducationTasks';
import * as milestones from '../components/PaperTrail/milestones';
import { POLITICS_EXAM_TASKS, politicsExamTopicIdsForTask } from '../data/examTopics/registry';

afterEach(() => { cleanup(); vi.restoreAllMocks(); });

describe('the milestone celebration', () => {
  it('is a sheet with its words and no emoji; Share card downloads, Nice closes', async () => {
    const share = vi.spyOn(milestones, 'downloadMilestoneCard').mockReturnValue(true as never);
    const onClose = vi.fn();
    render(<MilestoneCelebration milestone={{ id: 'streak-7', kind: 'streak', value: 7, title: '7-day streak', blurb: 'Consistency compounds. Keep the run going.' }}
      dateIso="2026-11-27" onClose={onClose} />);
    await act(async () => { await new Promise(r => requestAnimationFrame(() => r(null))); });
    const sheet = within(screen.getByRole('dialog', { name: 'Milestone: 7-day streak' }));
    expect(sheet.getByRole('heading', { name: '7-day streak' })).toBeInTheDocument();
    expect(sheet.getByText('Milestone reached')).toBeInTheDocument();
    expect(screen.getByRole('dialog', { name: 'Milestone: 7-day streak' }).textContent).not.toMatch(/[\u{1F300}-\u{1FAFF}]/u);
    fireEvent.click(sheet.getByRole('button', { name: 'Share card' }));
    expect(share).toHaveBeenCalledWith(expect.objectContaining({ id: 'streak-7' }), '2026-11-27');
    fireEvent.click(sheet.getByRole('button', { name: 'Nice' }));
    expect(onClose).toHaveBeenCalledTimes(1);
  });
});

describe('a Physical Education task in Topic Atlas', () => {
  it('saves to review, opens the full paper and shows its marking scheme', () => {
    const task = PHYSICAL_EDUCATION_TASKS[0];
    const onToggleReview = vi.fn();
    const onOpenInPaper = vi.fn();
    const { rerender } = render(<PhysicalEducationTaskCard task={task} saved={false} onToggleReview={onToggleReview} onOpenInPaper={onOpenInPaper} />);
    const save = screen.getByRole('button', { name: 'Add to daily review' });
    expect(save).toHaveAttribute('aria-pressed', 'false');
    fireEvent.click(save);
    expect(onToggleReview).toHaveBeenCalledTimes(1);
    rerender(<PhysicalEducationTaskCard task={task} saved onToggleReview={onToggleReview} onOpenInPaper={onOpenInPaper} />);
    expect(screen.getByRole('button', { name: 'Saved to daily review' })).toHaveAttribute('aria-pressed', 'true');
    fireEvent.click(screen.getByRole('button', { name: 'Full paper' }));
    expect(onOpenInPaper).toHaveBeenCalledTimes(1);
    const reveal = screen.getByRole('button', { name: 'Show marking scheme' });
    expect(reveal).toHaveAttribute('aria-expanded', 'false');
    fireEvent.click(reveal);
    expect(screen.getByRole('button', { name: 'Hide marking scheme' })).toHaveAttribute('aria-expanded', 'true');
  });
});

describe('the Politics practice feed', () => {
  it('filters by words, opens a marking guide and pages by twenty, on the shared controls', () => {
    const topicId = politicsExamTopicIdsForTask(POLITICS_EXAM_TASKS[0])[0];
    render(<PoliticsTopicFeed topicId={topicId} />);
    const count = () => Number(/(\d+) matching tasks/.exec(document.body.textContent ?? '')?.[1] ?? NaN);
    const all = count();
    expect(all).toBeGreaterThan(0);
    expect(screen.getByRole('button', { name: /Practice year/ })).toBeInTheDocument();
    if (all > 20) {
      expect(screen.getAllByRole('article')).toHaveLength(20);
      fireEvent.click(screen.getByRole('button', { name: 'Show 20 more tasks' }));
      expect(screen.getAllByRole('article').length).toBeGreaterThan(20);
    }
    if (all > 0) {
      fireEvent.click(screen.getAllByRole('button', { name: 'Show marking guide' })[0]);
      expect(screen.getByRole('button', { name: 'Hide marking guide' })).toHaveAttribute('aria-expanded', 'true');
    }
    fireEvent.change(screen.getByRole('searchbox', { name: 'Search practice tasks' }), { target: { value: 'zzzz-no-such-task' } });
    expect(count()).toBe(0);
  });
});
