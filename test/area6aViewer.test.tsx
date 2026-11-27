/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 *
 * Area 6a: the paper viewer's controls in the agreed places. Paper or Scheme
 * is a selection bar and Answers a switch in the bar; zoom, Go to page, save,
 * download and the study tools are rows in Tools (a sheet on a phone). Each row
 * does what its old control did.
 */
import React from 'react';
import { afterEach, beforeEach, describe, expect, it, vi } from 'vitest';
import { cleanup, fireEvent, render, screen, within } from '@testing-library/react';
import Viewer from '../components/PaperTrail/Viewer';

vi.mock('../components/PaperTrail/pdfjsLoader', () => ({ loadPdfjs: () => new Promise(() => {}) }));
vi.mock('../components/PaperTrail/pdfCache', () => ({ fetchPdfCached: vi.fn(() => Promise.resolve(null)) }));

const paper = { url: '/test-paper.pdf', label: 'Paper', bytes: 1363423 };
const scheme = { url: '/test-scheme.pdf', label: 'Scheme', bytes: 600924 };
const timing = { totalMinutes: 180, totalMarks: 400 } as unknown as React.ComponentProps<typeof Viewer>['timing'];
const openTools = () => fireEvent.click(screen.getByRole('button', { name: 'Study tools for this paper' }));
const toolsSheet = () => within(screen.getByRole('dialog', { name: 'Tools' }));

beforeEach(() => {
  localStorage.clear();
  vi.stubGlobal('fetch', vi.fn(() => Promise.resolve({ ok: true, json: () => Promise.resolve({ v: 1, q: [] }) })));
});
afterEach(() => { cleanup(); vi.unstubAllGlobals(); vi.restoreAllMocks(); });

describe('the paper viewer in the agreed look', () => {
  it('names the paper in the bar with its small line, and switches Paper or Scheme', () => {
    render(<Viewer title="Physics · 2025" subtitle="Exam Paper · Higher" barName="Physics" barOver="2025 · Higher · Exam Paper" paper={paper} scheme={scheme} onClose={() => {}} />);
    expect(screen.getByRole('heading', { name: 'Physics' })).toBeInTheDocument();
    expect(screen.getByText('2025 · Higher · Exam Paper')).toBeInTheDocument();
    const paperTab = screen.getByRole('radio', { name: 'Paper' });
    expect(paperTab).toHaveAttribute('aria-checked', 'true');
    fireEvent.click(screen.getByRole('radio', { name: 'Scheme' }));
    expect(screen.getByRole('radio', { name: 'Scheme' })).toHaveAttribute('aria-checked', 'true');
    expect(screen.getByText(/Opening the marking scheme/)).toBeInTheDocument();
  });

  it('toggles Answers from the bar and hides it on the scheme, as before', async () => {
    render(<Viewer title="T" paper={paper} scheme={scheme} answersUrl="/answers.json" onClose={() => {}} />);
    const answers = screen.getByRole('switch', { name: 'Show the marking scheme beside each question' });
    fireEvent.click(answers);
    expect(answers).toHaveAttribute('aria-checked', 'true');
    expect(fetch).toHaveBeenCalledWith('/answers.json');
    fireEvent.click(screen.getByRole('radio', { name: 'Scheme' }));
    expect(screen.queryByRole('switch', { name: 'Show the marking scheme beside each question' })).not.toBeInTheDocument();
  });

  it('keeps every study tool in Tools, each doing what its old control did', () => {
    const onSave = vi.fn();
    render(<Viewer title="T" paper={paper} scheme={scheme} answersUrl="/answers.json" storageNs="student|tools-rows" timing={timing}
      topics={{ subjectId: 'physics', year: 2025, level: 'higher', lang: 'ev', fileid: 'LC021ALP000EV.pdf', paperKey: 'physics|2025', q: [] }}
      saved={false} onSave={onSave} onClose={() => {}} />);
    openTools();
    const sheet = toolsSheet();
    // Save this paper: the page's Save, from the reader.
    fireEvent.click(sheet.getByRole('switch', { name: 'Save this paper' }));
    expect(onSave).toHaveBeenCalledTimes(1);
    // Download: the same link the bar had, opening in the browser.
    const download = sheet.getByRole('link', { name: /Download the paper/ });
    expect(download).toHaveAttribute('href', '/test-paper.pdf');
    expect(download).toHaveAttribute('target', '_blank');
    expect(download).toHaveTextContent('PDF · 1.3 MB');
    // Command words and Topics switch on and leave Tools open.
    fireEvent.click(sheet.getByRole('switch', { name: 'Command words' }));
    expect(toolsSheet().getByRole('switch', { name: 'Command words' })).toHaveAttribute('aria-checked', 'true');
    fireEvent.click(toolsSheet().getByRole('switch', { name: 'Topics & frequency' }));
    expect(toolsSheet().getByRole('switch', { name: 'Topics & frequency' })).toHaveAttribute('aria-checked', 'true');
    expect(screen.getByText('2 on')).toBeInTheDocument();
    // Exam mode starts the clock and puts Tools away.
    fireEvent.click(toolsSheet().getByRole('switch', { name: 'Exam mode' }));
    expect(screen.getByRole('timer')).toHaveTextContent('3:00:00');
    // Self-mark turns Answers on with it, as it did.
    openTools();
    fireEvent.click(toolsSheet().getByRole('switch', { name: 'Self-mark' }));
    expect(screen.getByRole('switch', { name: 'Show the marking scheme beside each question' })).toHaveAttribute('aria-checked', 'true');
    // Triage opens its sheet.
    openTools();
    fireEvent.click(toolsSheet().getByRole('button', { name: /Triage/ }));
    expect(screen.getByRole('dialog', { name: 'Triage — plan your attack' })).toBeInTheDocument();
  });

  it('offers what the scheme side had: zoom, Go to page, save, its download and Attempt first', () => {
    render(<Viewer title="T" paper={paper} scheme={scheme} answersUrl="/answers.json" storageNs="student|scheme-side" initialSide="scheme" onSave={() => {}} onClose={() => {}} />);
    openTools();
    const sheet = toolsSheet();
    expect(sheet.getByRole('button', { name: 'Zoom in' })).toBeInTheDocument();
    expect(sheet.getByRole('spinbutton', { name: 'Go to page' })).toBeInTheDocument();
    expect(sheet.getByRole('link', { name: /Download the scheme/ })).toHaveAttribute('href', '/test-scheme.pdf');
    expect(sheet.getByRole('switch', { name: 'Attempt first' })).toBeInTheDocument();
    expect(sheet.queryByRole('switch', { name: 'Command words' })).not.toBeInTheDocument();
    expect(sheet.queryByRole('button', { name: /Triage/ })).not.toBeInTheDocument();
  });

  it('closes with Close at the top left', () => {
    const onClose = vi.fn();
    render(<Viewer title="T" paper={paper} onClose={onClose} />);
    fireEvent.click(screen.getByRole('button', { name: 'Close viewer' }));
    expect(onClose).toHaveBeenCalledTimes(1);
  });
});
