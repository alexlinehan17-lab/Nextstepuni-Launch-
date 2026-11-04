/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 *
 * Render smoke for the Topic Vault surface (ReviseByTopic) — the 3-level
 * navigator: subject picker → topic list (type-to-filter) → question feed
 * (level + year filters). Reads the real committed tags; `fetch` is stubbed to
 * reject so the feed's VaultQuestionCards degrade to their honest fallback row
 * (no network / pdf.js in jsdom). Guards the feature additions (search, year
 * chips, per-level counts, filter-aware header) against render regressions.
 */
import { describe, test, expect, beforeEach, vi } from 'vitest';
import { render, screen, fireEvent } from '@testing-library/react';
import ReviseByTopic from '@/components/PaperTrail/ReviseByTopic';
import { taggedSubjects, topicsForSubject } from '@/components/PaperTrail/topics';

const label = (id: string) => id.charAt(0).toUpperCase() + id.slice(1);
const noop = vi.fn();

// A subject with the most topics — exercises the type-to-filter search path.
const richestSubject = () =>
  [...taggedSubjects()].sort((a, b) => topicsForSubject(b).length - topicsForSubject(a).length)[0];

beforeEach(() => {
  localStorage.clear();
  vi.stubGlobal('fetch', vi.fn(() => Promise.reject(new Error('no network in jsdom'))));
});

describe('Topic Vault — ReviseByTopic', () => {
  test('opens directly on a topic map with a subject picker', () => {
    render(
      <ReviseByTopic
        subjects={[{ id: richestSubject(), label: label(richestSubject()) }]}
        mineIds={[]}
        subjectLabel={label}
        onOpenQuestion={noop}
        onBack={noop}
      />,
    );
    expect(screen.getByText(/Topic Atlas/i)).toBeInTheDocument();
    expect(screen.getByRole('button', { name: 'Choose a subject' })).toBeInTheDocument();
  });

  test('drills subject → topic list → question feed without crashing', () => {
    const sid = richestSubject();
    render(
      <ReviseByTopic
        subjects={[{ id: sid, label: label(sid) }]}
        mineIds={[]}
        subjectLabel={label}
        onOpenQuestion={noop}
        onBack={noop}
      />,
    );
    // Level 0 → 1: pick the subject tile.
    // The volume header band prints real stats: questions, topics, and a sane year span.
    expect(screen.getByText(/[\d,]+ questions · \d{4}–\d{4}/)).toBeInTheDocument();

    // The first topic renders as a row; drill into its first course-specific
    // occurrence. Overlapping specifications may intentionally reuse a label.
    const busiest = topicsForSubject(sid)[0];
    const topicBtn = screen.getAllByRole('button', { name: new RegExp(busiest.label.slice(0, 12).replace(/[.*+?^${}()|[\]\\]/g, '\\$&'), 'i') })[0];
    expect(topicBtn).toBeDefined();
    fireEvent.click(topicBtn);

    // Level 2: the feed summary (unique to the feed) renders; cards fall back (no net).
    expect(screen.getByText('Levels')).toBeInTheDocument();
  });

  test('type-to-filter narrows the topic list when a subject has many topics', () => {
    const sid = richestSubject();
    if (topicsForSubject(sid).length <= 8) return; // search only shows past 8 topics
    render(
      <ReviseByTopic
        subjects={[{ id: sid, label: label(sid) }]}
        mineIds={[]}
        subjectLabel={label}
        onOpenQuestion={noop}
        onBack={noop}
      />,
    );
    const search = screen.getByLabelText(/Search topics/i);
    fireEvent.change(search, { target: { value: 'zzzznotatopiczzz' } });
    expect(screen.getByText(/No topics match/i)).toBeInTheDocument();
  });

  test('explains a retained reference topic whose official source is unavailable', () => {
    render(
      <ReviseByTopic
        subjects={[{ id: 'japanese', label: 'Japanese' }]}
        mineIds={[]}
        subjectLabel={label}
        restore={{ subjectId: 'japanese', subtopicId: 'japanese-common-oral-exam' }}
        onOpenQuestion={noop}
        onBack={noop}
      />,
    );
    expect(screen.getByText(/2 reference entries · official source files pending/i)).toBeInTheDocument();
    expect(screen.getByText(/official question material is not available in the local SEC corpus yet/i)).toBeInTheDocument();
    expect(screen.queryByRole('button', { name: /Show all/i })).not.toBeInTheDocument();
  });
});
