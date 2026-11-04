/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 *
 * The archive-outage notice in the Paper Trail archive: one probe of the
 * first indexed paper, the notice on the home screen AND the subject view when
 * the archive refuses, and silence when the probe is inconclusive or the
 * archive answers. The probe itself is unit-tested in ptArchiveHealth.test.ts.
 */
import React from 'react';
import { afterEach, beforeEach, describe, expect, it, vi } from 'vitest';
import { act, cleanup, fireEvent, render, screen, waitFor } from '@testing-library/react';
import PaperTrail from '../components/PaperTrail';
import { resetArchiveHealthForTests } from '../components/PaperTrail/archiveHealth';
import type { PaperEntry } from '../types/paperTrail';

vi.mock('../components/PaperTrail/Viewer', () => ({ default: () => <div aria-label="Paper Trail reader" /> }));
vi.mock('../components/PaperTrail/PaperCover', () => ({ default: () => <span>Cover</span> }));
vi.mock('../firebase', () => ({ db: {} }));
vi.mock('../contexts/ProgressContext', () => ({ useProgress: () => ({ updateDemoProgress: () => {} }) }));
vi.mock('../hooks/useFreshProgress', () => ({ useFreshProgress: () => ({ loaded: true, doc: null }) }));
vi.mock('../components/PaperTrail/topics', () => ({
  taggedSubjects: () => ['mathematics'],
  topicsForPaper: () => null,
}));
vi.mock('../paperTrailData', () => {
  const entry = (year: number): PaperEntry => ({
    year, level: 'higher', lang: 'ev', papers: [
      { label: 'Paper 1', doc: { f: 'one.pdf', b: 12345 }, scheme: { f: 'one.pdf', b: 65432 } },
    ],
  });
  return {
    PAPER_TRAIL_SUBJECTS: [
      { id: 'mathematics', name: 'Mathematics', cycle: 'lc', levels: ['higher'] },
    ],
    PAPER_TRAIL_INDEX: { mathematics: [entry(2026), entry(2025)] },
    PAPER_TRAIL_GAPS: [],
  };
});

const NOTICE = 'Some papers may be temporarily unavailable.';
const start = () => render(<PaperTrail studentSubjects={['Mathematics']} />);
/** Let the probe's promise chain and any resulting state update settle. */
const settle = () => act(() => new Promise<void>(resolve => setTimeout(resolve, 0)));

describe('Paper Trail archive-outage notice', () => {
  beforeEach(() => {
    localStorage.clear();
    resetArchiveHealthForTests();
  });
  afterEach(() => {
    cleanup();
    vi.unstubAllGlobals();
  });

  it('probes the first indexed paper once and shows the notice on home and the subject view when the archive refuses', async () => {
    const fetchMock = vi.fn().mockResolvedValue({ status: 402 });
    vi.stubGlobal('fetch', fetchMock);
    start();

    expect(await screen.findByText(NOTICE)).toBeInTheDocument();
    expect(fetchMock).toHaveBeenCalledTimes(1);
    expect(fetchMock.mock.calls[0][0]).toContain(encodeURIComponent('papers/lc/mathematics/2026/paper/one.pdf'));
    expect(fetchMock.mock.calls[0][1]).toEqual({ headers: { Range: 'bytes=0-1' }, signal: expect.any(AbortSignal) });

    fireEvent.click(screen.getByRole('button', { name: /^Mathematics\s*Higher\s*level$/ }));
    expect(screen.getByRole('region', { name: 'Mathematics exam papers' })).toBeInTheDocument();
    expect(screen.getByText(NOTICE)).toBeInTheDocument();
  });

  it('stays silent when the student’s own connection fails the probe', async () => {
    const fetchMock = vi.fn().mockRejectedValue(new Error('offline'));
    vi.stubGlobal('fetch', fetchMock);
    start();

    await waitFor(() => expect(fetchMock).toHaveBeenCalledTimes(1));
    await settle();
    expect(screen.queryByText(NOTICE)).not.toBeInTheDocument();
  });

  it('stays silent when the archive answers', async () => {
    const fetchMock = vi.fn().mockResolvedValue({ status: 206 });
    vi.stubGlobal('fetch', fetchMock);
    start();

    await waitFor(() => expect(fetchMock).toHaveBeenCalledTimes(1));
    await settle();
    expect(screen.queryByText(NOTICE)).not.toBeInTheDocument();
  });
});
