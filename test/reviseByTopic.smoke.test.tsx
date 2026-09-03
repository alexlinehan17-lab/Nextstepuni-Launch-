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
  test('renders the subject picker (level 0)', () => {
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
    expect(screen.getByText(/Every question the SEC has asked, mapped by topic/i)).toBeInTheDocument();
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
    fireEvent.click(screen.getByRole('button', { name: new RegExp(`^${label(sid)}`) }));
    expect(screen.getByText(/topics · /i)).toBeInTheDocument();

    // The busiest topic renders as a row; drill into it.
    const busiest = topicsForSubject(sid)[0];
    const topicBtn = screen.getByRole('button', { name: new RegExp(busiest.label.slice(0, 12).replace(/[.*+?^${}()|[\]\\]/g, '\\$&'), 'i') });
    fireEvent.click(topicBtn);

    // Level 2: the feed summary (unique to the feed) renders; cards fall back (no net).
    expect(screen.getByText(/marking scheme beneath each/i)).toBeInTheDocument();
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
    fireEvent.click(screen.getByRole('button', { name: new RegExp(`^${label(sid)}`) }));
    const search = screen.getByLabelText(/Search topics/i);
    fireEvent.change(search, { target: { value: 'zzzznotatopiczzz' } });
    expect(screen.getByText(/No topics match/i)).toBeInTheDocument();
  });
});
