/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 *
 * Area 6c: what a student meets inside a paper, after its controls moved onto
 * the shared parts. The Full Loop runs from its first question to its summary;
 * the marking scheme opens on the shared Sheet with self-mark's choices; the
 * place is saved and resumed; the exam clock counts, pauses and closes. Each
 * still does what its old control did, and what it saves is unchanged.
 */
import React from 'react';
import { afterEach, beforeEach, describe, expect, it, vi } from 'vitest';
import { act, cleanup, fireEvent, render, screen, within } from '@testing-library/react';
import Viewer from '../components/PaperTrail/Viewer';
import { loadAttempt } from '../components/PaperTrail/attemptStore';
import { loadLoopPlace } from '../components/PaperTrail/loopResume';
import { readAnswer } from '../components/PaperTrail/answerDeskStore';

vi.mock('../components/PaperTrail/pdfjsLoader', () => ({ loadPdfjs: () => new Promise(() => {}) }));
vi.mock('../components/PaperTrail/pdfCache', () => ({ fetchPdfCached: vi.fn(() => Promise.resolve(null)) }));

const paper = { url: '/test-paper.pdf', label: 'Paper', bytes: 1363423 };
const scheme = { url: '/test-scheme.pdf', label: 'Scheme', bytes: 600924 };
const timing = { totalMinutes: 180, totalMarks: 400 } as unknown as React.ComponentProps<typeof Viewer>['timing'];
const q = (n: string, pP: number) => ({ n, pP, pY: [0.1, 0.9], mode: 'crop', conf: 1, region: [{ p: pP, r: [0, 0, 1, 1] }] });
const MAP = { v: 1, copyright: '© State Examinations Commission', q: [q('1', 2), q('2', 4), q('3', 6)] };
const NS = 'student|area6c-loop';

const openTools = () => fireEvent.click(screen.getByRole('button', { name: 'Study tools for this paper' }));
const toolsSheet = () => within(screen.getByRole('dialog', { name: 'Tools' }));
const flush = async () => { await act(async () => { await Promise.resolve(); await Promise.resolve(); }); };

beforeEach(() => {
  localStorage.clear();
  vi.stubGlobal('fetch', vi.fn(() => Promise.resolve({ ok: true, json: () => Promise.resolve(MAP) })));
});
afterEach(() => { cleanup(); vi.unstubAllGlobals(); vi.restoreAllMocks(); });

const renderViewer = () => render(<Viewer title="Accounting · 2025" paper={paper} scheme={scheme} answersUrl="/answers.json" storageNs={NS} timing={timing} onClose={() => {}} />);

async function startLoop() {
  openTools();
  fireEvent.click(toolsSheet().getByRole('button', { name: /The Full Loop/ }));
  await flush();
}

describe('the Full Loop on the shared parts', () => {
  it('runs from the first question to the summary, marking each against the scheme', async () => {
    renderViewer();
    await startLoop();
    // The loop bar: where you are, and one main action.
    expect(screen.getByText(/1 of 3/)).toBeInTheDocument();
    for (let i = 0; i < 3; i += 1) {
      fireEvent.click(screen.getByRole('button', { name: 'Reveal & mark' }));
      const sheet = within(screen.getByRole('dialog', { name: /marking scheme/i }));
      // Self-mark's bands: a button that stays pressed, chosen with the ink outline.
      const half = sheet.getByRole('button', { name: 'Half' });
      fireEvent.click(half);
      expect(half).toHaveAttribute('aria-pressed', 'true');
      fireEvent.click(sheet.getByRole('button', { name: 'Wrong method' }));
      expect(sheet.getByRole('button', { name: 'Wrong method' })).toHaveAttribute('aria-pressed', 'true');
      fireEvent.click(sheet.getByRole('button', { name: 'Close' }));
      await act(async () => { await new Promise(r => setTimeout(r, 340)); });
      fireEvent.click(screen.getByRole('button', { name: i < 2 ? /^Next/ : 'Finish' }));
    }
    // What was saved is what it always was: one mark per question, score and reason.
    const marks = loadAttempt(NS).marks ?? {};
    expect(Object.keys(marks).sort()).toEqual(['1', '2', '3']);
    expect(marks['1']).toMatchObject({ score: 50, max: 100, gap: 'process' });
    // The summary, on a sheet: the average, the receipt, Save image and Done.
    const summary = within(screen.getByRole('dialog', { name: /full loop/i }));
    expect(summary.getAllByText('50%').length).toBeGreaterThan(0);
    expect(summary.getByText(/3 of 3 questions self-marked/)).toBeInTheDocument();
    expect(summary.getByRole('button', { name: /Save image/ })).toBeInTheDocument();
    fireEvent.click(summary.getByRole('button', { name: 'Done' }));
    await act(async () => { await new Promise(r => setTimeout(r, 340)); });
    expect(screen.queryByRole('dialog', { name: /full loop/i })).not.toBeInTheDocument();
  });

  it('saves the place when the loop is ended, and resumes it from the card', async () => {
    renderViewer();
    await startLoop();
    fireEvent.click(screen.getByRole('button', { name: 'Reveal & mark' }));
    fireEvent.click(within(screen.getByRole('dialog', { name: /marking scheme/i })).getByRole('button', { name: 'Full' }));
    fireEvent.click(within(screen.getByRole('dialog', { name: /marking scheme/i })).getByRole('button', { name: 'Close' }));
    await act(async () => { await new Promise(r => setTimeout(r, 340)); });
    fireEvent.click(screen.getByRole('button', { name: /^Next/ }));
    fireEvent.click(screen.getByRole('button', { name: 'End the loop — your place is saved' }));
    expect(loadLoopPlace(NS, Date.now())).toMatchObject({ idx: 1, total: 3 });
    expect(screen.getByText(/You were on question 2 of 3/)).toBeInTheDocument();
    expect(screen.getByRole('button', { name: 'Start over' })).toBeInTheDocument();
    fireEvent.click(screen.getByRole('button', { name: 'Resume' }));
    expect(screen.getByText(/2 of 3/)).toBeInTheDocument();
    expect(screen.getByRole('button', { name: 'Reveal & mark' })).toBeInTheDocument();
  });
});

describe('the exam clock', () => {
  it('counts in the readout, pauses, resets and closes as before', async () => {
    vi.useFakeTimers();
    try {
      renderViewer();
      openTools();
      fireEvent.click(toolsSheet().getByRole('switch', { name: 'Exam mode' }));
      const clock = screen.getByRole('timer');
      expect(clock).toHaveTextContent('3:00:00');
      expect(clock.querySelector('.ui-readout')).not.toBeNull();
      act(() => { vi.advanceTimersByTime(3000); });
      expect(screen.getByRole('timer')).toHaveTextContent('2:59:57');
      fireEvent.click(screen.getByRole('button', { name: 'Pause timer' }));
      act(() => { vi.advanceTimersByTime(3000); });
      expect(screen.getByRole('timer')).toHaveTextContent('2:59:57');
      fireEvent.click(screen.getByRole('button', { name: 'Reset timer' }));
      expect(screen.getByRole('timer')).toHaveTextContent('3:00:00');
      fireEvent.click(screen.getByRole('button', { name: 'Close exam mode' }));
      expect(screen.queryByRole('timer')).not.toBeInTheDocument();
    } finally {
      vi.useRealTimers();
    }
  });
});

describe('the Answer Desk on the shared parts', () => {
  it('chooses how to answer, how sure you are and the pen, each saved as before', () => {
    render(<Viewer title="Accounting · 2025" paper={paper} scheme={scheme} storageNs="student|area6c-desk" onClose={() => {}} />);
    openTools();
    fireEvent.click(toolsSheet().getByRole('switch', { name: 'Attempt first' }));
    const desk = within(screen.getByRole('complementary', { name: 'Your answer desk' }));
    // How to answer: three buttons that stay pressed, chosen with the ink outline.
    expect(desk.getByRole('button', { name: 'Type' })).toHaveAttribute('aria-pressed', 'true');
    fireEvent.change(desk.getByLabelText('Your attempt'), { target: { value: 'Gross profit 318,650.' } });
    fireEvent.click(desk.getByRole('button', { name: 'Nearly there' }));
    expect(desk.getByRole('button', { name: 'Nearly there' })).toHaveAttribute('aria-pressed', 'true');
    const saved = readAnswer('student|area6c-desk', 'page:1').record;
    expect(saved.draft.text).toBe('Gross profit 318,650.');
    expect(saved.confidence).toBe('Nearly there');
    // Write on paper: the pen is chosen, the other tools are there, Undo waits for a stroke.
    fireEvent.click(desk.getByRole('button', { name: 'Write on paper' }));
    expect(readAnswer('student|area6c-desk', 'page:1').record.mode).toBe('ink');
    expect(desk.getByRole('button', { name: 'Pen' })).toHaveAttribute('aria-pressed', 'true');
    fireEvent.click(desk.getByRole('button', { name: 'Move page' }));
    expect(desk.getByRole('button', { name: 'Move page' })).toHaveAttribute('aria-pressed', 'true');
    expect(desk.getByRole('button', { name: 'Undo last stroke on this page' })).toHaveAttribute('aria-disabled', 'true');
    // The main action of the step is the one charcoal button.
    expect(desk.getByRole('button', { name: 'Keep my attempt & reveal' })).toHaveClass('ui-btn--main');
  });
});
