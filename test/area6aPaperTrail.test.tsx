/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 *
 * Area 6a: Paper Trail in the agreed look. The level and the years are
 * selection bars (the year was a dropdown); All years lists every paper once,
 * newest first; a cover and its Open button open the same document; the
 * reader can save the paper it shows.
 */
import React from 'react';
import { beforeEach, describe, expect, it, vi } from 'vitest';
import { act, fireEvent, render, screen, within } from '@testing-library/react';
import PaperTrail from '../components/PaperTrail';
import { NavigationProvider, useNavigation } from '../contexts/NavigationContext';
import { listPins } from '../components/PaperTrail/recentsStore';
import type { PaperEntry } from '../types/paperTrail';

interface ReaderProps {
  paper: { url: string };
  scheme?: { url: string };
  initialSide: string;
  saved?: boolean;
  onSave?: () => void;
  barName?: string;
  barOver?: string;
  onClose: () => void;
}
const reader = vi.hoisted(() => ({ props: null as ReaderProps | null }));
vi.mock('../utils/bootParams', () => ({ getBootParam: () => null }));
vi.mock('../components/PaperTrail/Viewer', () => ({ default: (props: ReaderProps) => {
  reader.props = props;
  return <div aria-label="Paper Trail reader"><button onClick={props.onClose}>Close reader</button></div>;
} }));
vi.mock('../components/PaperTrail/PaperCover', () => ({ default: ({ url }: { url: string }) => <span data-cover={url}>Cover</span> }));
vi.mock('../components/PaperTrail/archiveHealth', () => ({ archiveHealth: () => Promise.resolve('ok') }));
vi.mock('../contexts/AuthContext', () => ({ useAuth: () => ({ user: { uid: 'student-1' }, authResolved: true }) }));
vi.mock('../firebase', () => ({ db: {} }));
vi.mock('../contexts/ProgressContext', () => ({ useProgress: () => ({ updateDemoProgress: () => {} }) }));
vi.mock('../hooks/useFreshProgress', () => ({ useFreshProgress: () => ({ loaded: true, doc: null }) }));
vi.mock('../components/PaperTrail/topics', () => ({ taggedSubjects: () => ['mathematics'], topicsForPaper: () => null }));
vi.mock('../paperTrailData', () => {
  const entry = (year: number, level: 'higher' | 'ordinary' = 'higher'): PaperEntry => ({
    year, level, lang: 'ev', papers: [
      { label: 'Paper 1', doc: { f: `one-${year}.pdf`, b: 12345 }, scheme: { f: `one-${year}.pdf`, b: 65432 } },
      { label: 'Paper 2', doc: { f: `two-${year}.pdf`, b: 23456 } },
    ],
  });
  return {
    PAPER_TRAIL_SUBJECTS: [{ id: 'mathematics', name: 'Mathematics', cycle: 'lc', levels: ['higher', 'ordinary'] }],
    PAPER_TRAIL_INDEX: { mathematics: [entry(2026), entry(2025), entry(2024), entry(2018), entry(2026, 'ordinary')] },
    PAPER_TRAIL_GAPS: [{ subjectId: 'mathematics', year: 2020, reason: 'The exams were cancelled.' }],
  };
});

const FrameBack = () => { const nav = useNavigation(); return <button onClick={nav.goBack}>Back</button>; };
const start = () => render(<NavigationProvider><FrameBack /><PaperTrail studentSubjects={['Mathematics']} studentLevels={[{ name: 'Mathematics', level: 'Higher' }]} /></NavigationProvider>);
const openMaths = () => fireEvent.click(screen.getByRole('button', { name: 'Mathematics Higher level' }));
const radio = (group: string, name: string) => within(screen.getByRole('radiogroup', { name: group })).getByRole('radio', { name });

describe('Paper Trail in the agreed look', () => {
  beforeEach(() => { localStorage.clear(); reader.props = null; });

  it('chooses the level in a bar, as the toggle did, and the year in a bar, as the dropdown did', () => {
    start(); openMaths();
    expect(radio('Level', 'Higher')).toHaveAttribute('aria-checked', 'true');
    expect(radio('Year', '2026')).toHaveAttribute('aria-checked', 'true');
    expect(within(screen.getByRole('radiogroup', { name: 'Year' })).getAllByRole('radio').map(r => r.textContent)).toEqual(['All years', '2026', '2025', '2024']);
    fireEvent.click(radio('Year', '2024'));
    expect(screen.getByRole('heading', { name: '2024 papers' })).toBeInTheDocument();
    fireEvent.click(within(screen.getByRole('article', { name: 'Paper 1' })).getByRole('button', { name: 'Open paper' }));
    expect(reader.props?.paper.url).toContain(encodeURIComponent('/2024/paper/one-2024.pdf'));
    fireEvent.click(screen.getByRole('button', { name: 'Close reader' }));
    fireEvent.click(radio('Level', 'Ordinary'));
    expect(radio('Level', 'Ordinary')).toHaveAttribute('aria-checked', 'true');
    expect(within(screen.getByRole('radiogroup', { name: 'Year' })).getAllByRole('radio').map(r => r.textContent)).toEqual(['All years', '2026']);
  });

  it('opens the same documents from a cover and from its Open button', () => {
    start(); openMaths();
    const paper = within(screen.getByRole('article', { name: 'Paper 1' }));
    fireEvent.click(paper.getByRole('button', { name: 'Open the 2026 Paper 1' }));
    expect(reader.props?.initialSide).toBe('paper');
    expect(reader.props?.paper.url).toContain(encodeURIComponent('/2026/paper/one-2026.pdf'));
    fireEvent.click(screen.getByRole('button', { name: 'Close reader' }));
    fireEvent.click(within(screen.getByRole('article', { name: 'Paper 1' })).getByRole('button', { name: 'Open the 2026 marking scheme for Paper 1' }));
    expect(reader.props?.initialSide).toBe('scheme');
    expect(reader.props?.scheme?.url).toContain(encodeURIComponent('/2026/scheme/one-2026.pdf'));
    fireEvent.click(screen.getByRole('button', { name: 'Close reader' }));
    fireEvent.click(within(screen.getByRole('article', { name: 'Paper 1' })).getByRole('button', { name: 'Open marking scheme for Paper 1' }));
    expect(reader.props?.initialSide).toBe('scheme');
    expect(reader.props?.scheme?.url).toContain(encodeURIComponent('/2026/scheme/one-2026.pdf'));
  });

  it('lists every paper once in All years, newest first, with a year the SEC did not publish explained in place', () => {
    start(); openMaths();
    fireEvent.click(radio('Year', 'All years'));
    const list = within(screen.getByRole('list', { name: 'Every paper' }));
    const rows = list.getAllByRole('listitem').map(item => item.textContent ?? '');
    expect(rows.filter(text => /2026 · Paper 1/.test(text))).toHaveLength(1);
    expect(rows.map(text => text.match(/(\d{4}) · (Paper \d|Unavailable)/)?.slice(1).join(' '))).toEqual([
      '2026 Paper 1', '2026 Paper 2', '2025 Paper 1', '2025 Paper 2', '2024 Paper 1', '2024 Paper 2', '2020 Unavailable', '2018 Paper 1', '2018 Paper 2',
    ]);
    expect(list.getByText('The exams were cancelled.')).toBeInTheDocument();
    expect(rows[0]).toMatch(/Paper and marking scheme/);
    expect(rows[1]).toMatch(/No marking scheme published/);
    fireEvent.click(list.getByRole('button', { name: 'Open the 2018 Paper 1' }));
    expect(reader.props?.paper.url).toContain(encodeURIComponent('/2018/paper/one-2018.pdf'));
    // Closing the reader returns to the list it was opened from.
    fireEvent.click(screen.getByRole('button', { name: 'Close reader' }));
    expect(radio('Year', 'All years')).toHaveAttribute('aria-checked', 'true');
    expect(screen.getByRole('list', { name: 'Every paper' })).toBeInTheDocument();
  });

  it('saves the paper the reader shows, under the same identity as the page’s Save', () => {
    start(); openMaths();
    fireEvent.click(radio('Year', 'All years'));
    fireEvent.click(screen.getByRole('button', { name: 'Open the 2018 Paper 1' }));
    expect(reader.props?.saved).toBe(false);
    expect(reader.props?.barName).toBe('Mathematics');
    expect(reader.props?.barOver).toBe('2018 · Higher · Paper 1');
    act(() => { reader.props?.onSave?.(); });
    expect(listPins()).toHaveLength(1);
    expect(listPins()[0].key).toBe('mathematics|2018|higher|ev|one-2018.pdf');
    expect(reader.props?.saved).toBe(true);
  });
});
