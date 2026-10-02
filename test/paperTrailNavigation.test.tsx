import React from 'react';
import { beforeEach, describe, expect, it, vi } from 'vitest';
import { fireEvent, render, screen, within } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import PaperTrail from '../components/PaperTrail';
import { listPins } from '../components/PaperTrail/recentsStore';
import type { PaperEntry } from '../types/paperTrail';

interface ReaderProps {
  paper: { url: string };
  scheme?: { url: string };
  answersUrl?: string;
  topics?: unknown;
  initialSide: string;
  initialPaperPage: number;
  initialSchemePage: number;
  onPosition: (side: 'paper' | 'scheme', page: number) => void;
  onClose: () => void;
}
const reader = vi.hoisted(() => ({ props: null as ReaderProps | null }));
const boot = vi.hoisted(() => ({ params: {} as Record<string, string>, loaded: true }));
vi.mock('../utils/bootParams', () => ({ getBootParam: (name: string) => boot.params[name] ?? null }));
vi.mock('../components/PaperTrail/Viewer', () => ({ default: (props: ReaderProps) => {
  reader.props = props;
  return <div aria-label="Paper Trail reader">
    <button onClick={() => props.onPosition('paper', 4)}>Read paper page 4</button>
    <button onClick={() => props.onPosition('scheme', 7)}>Read scheme page 7</button>
    <button onClick={props.onClose}>Close reader</button>
  </div>;
} }));
vi.mock('../components/PaperTrail/PaperCover', () => ({ default: () => <span>Cover</span> }));
// The archive-outage probe would otherwise make a real network request (and a
// live outage would add a second status region); it has its own tests.
vi.mock('../components/PaperTrail/archiveHealth', () => ({ archiveHealth: () => Promise.resolve('ok') }));
vi.mock('../firebase', () => ({ db: {} }));
vi.mock('../contexts/ProgressContext', () => ({ useProgress: () => ({ updateDemoProgress: () => {} }) }));
vi.mock('../hooks/useFreshProgress', () => ({ useFreshProgress: () => ({ loaded: boot.loaded, doc: null }) }));
vi.mock('../components/PaperTrail/topics', () => ({
  taggedSubjects: () => ['mathematics'],
  topicsForPaper: () => ({ paperKey: 'mathematics|2026|higher|ev|one.pdf' }),
}));
vi.mock('../paperTrailData', () => {
  const entry = (year: number, level: 'higher' | 'ordinary' = 'higher', lang: 'ev' | 'iv' = 'ev'): PaperEntry => ({
    year, level, lang, papers: [
      { label: 'Paper 1', doc: { f: 'one.pdf', b: 12345 }, scheme: { f: 'one.pdf', b: 65432 }, answers: 1 },
      { label: 'Paper 2', doc: { f: 'two.pdf', b: 23456 } },
      { label: 'Paper 1 modified', modified: true, doc: { f: 'accessible.pdf', b: 56789 } },
    ],
  });
  return {
    PAPER_TRAIL_SUBJECTS: [
      { id: 'mathematics', name: 'Mathematics', cycle: 'lc', levels: ['higher', 'ordinary'] },
      { id: 'biology', name: 'Biology', cycle: 'lc', levels: ['higher', 'ordinary'] },
      { id: 'jc-mathematics', name: 'Mathematics', cycle: 'jc', levels: ['higher', 'ordinary'] },
      { id: 'lca-mathematics', name: 'Mathematics', cycle: 'lca', levels: ['common'] },
    ],
    PAPER_TRAIL_INDEX: { mathematics: [entry(2026), entry(2025), entry(2024), entry(2018), entry(2026, 'ordinary'), entry(2026, 'ordinary', 'iv')] },
    PAPER_TRAIL_GAPS: [{ subjectId: 'mathematics', year: 2020, reason: 'The exams were cancelled.' }],
  };
});

const start = () => render(<PaperTrail studentSubjects={['Mathematics', 'Biology']} studentLevels={[{ name: 'Mathematics', level: 'Higher' }]} />);
const click = (name: string | RegExp) => fireEvent.click(screen.getByRole('button', { name: typeof name === 'string' ? new RegExp('^' + name.replaceAll(' ', '\\s*') + '$') : name }));
const paperOne = () => within(screen.getByRole('article', { name: 'Paper 1' }));

describe('Paper Trail archive → existing reader', () => {
  beforeEach(() => { localStorage.clear(); reader.props = null; boot.params = {}; boot.loaded = true; });

  it('opens a document link straight in the reader and returns to the selected archive filters', () => {
    boot.params = { subject: 'mathematics', year: '2026', level: 'ordinary', lang: 'iv', paper: 'one.pdf', side: 'scheme' };
    boot.loaded = false;
    const { rerender } = render(<PaperTrail />);
    const loading = screen.getByRole('status');
    expect(loading).toHaveTextContent('Opening your paper');
    expect(loading).toHaveClass('z-[200]');
    expect(loading.parentElement).toBe(document.body);
    expect(screen.queryByRole('combobox', { name: 'Level' })).not.toBeInTheDocument();
    boot.loaded = true;
    rerender(<PaperTrail />);
    expect(screen.getByLabelText('Paper Trail reader')).toBeInTheDocument();
    expect(screen.queryByText('Opening your paper')).not.toBeInTheDocument();
    expect(reader.props?.initialSide).toBe('scheme');
    expect(reader.props?.answersUrl).toBeTruthy();
    click('Close reader');
    expect(screen.getByRole('button', { name: 'Ordinary level' })).toHaveAttribute('aria-pressed', 'true');
    expect(screen.getByRole('combobox', { name: 'Paper language' })).toHaveTextContent('Gaeilge');
  });

  it('opens the real-cover preview in the paired reader with Answers and Topics', async () => {
    start(); click('Mathematics Higher level'); click('Preview Paper 1');
    const preview = within(await screen.findByRole('dialog'));
    expect(preview.getByRole('heading', { name: 'Paper 1' })).toBeInTheDocument();
    fireEvent.click(preview.getByRole('button', { name: 'Open paper' }));
    expect(screen.getByLabelText('Paper Trail reader')).toBeInTheDocument();
    expect(reader.props?.paper.url).toContain(encodeURIComponent('papers/lc/mathematics/2026/paper/one.pdf'));
    expect(reader.props?.scheme?.url).toContain(encodeURIComponent('papers/lc/mathematics/2026/scheme/one.pdf'));
    expect(reader.props?.initialSide).toBe('paper');
    expect(reader.props?.answersUrl).toBeTruthy();
    expect(reader.props?.topics).toBeTruthy();
  });


  it('shows the paper and scheme attachment previews and opens the matching document', async () => {
    start(); click('Mathematics Higher level');
    fireEvent.click(paperOne().getByRole('button', { name: 'Paper & marking scheme' }));
    const files = within(await screen.findByRole('dialog'));
    expect(files.getByRole('heading', { name: 'The paper. The points.' })).toBeInTheDocument();
    expect(files.getByRole('button', { name: 'Inspect Paper 1' })).toBeInTheDocument();
    fireEvent.click(files.getByRole('button', { name: 'Inspect Marking scheme' }));
    expect(files.getByRole('heading', { name: 'Marking scheme' })).toBeInTheDocument();
    fireEvent.click(files.getByRole('button', { name: 'Open paper' }));
    expect(screen.queryByRole('dialog')).not.toBeInTheDocument();
    expect(reader.props?.initialSide).toBe('scheme');
    expect(reader.props?.scheme?.url).toContain(encodeURIComponent('/2026/scheme/one.pdf'));
  });

  it('opens the matching scheme and restores each side’s latest position through Continue', () => {
    start(); click('Mathematics Higher level');
    fireEvent.click(paperOne().getByRole('button', { name: /Open marking scheme/ }));
    expect(reader.props?.initialSide).toBe('scheme');
    click('Read paper page 4'); click('Read scheme page 7'); click('Close reader'); click('Paper Trail');
    click('Continue');
    expect(reader.props?.initialSide).toBe('scheme');
    expect(reader.props?.initialPaperPage).toBe(4);
    expect(reader.props?.initialSchemePage).toBe(7);
  });

  it('saves the full identity and returns to the correct older year after a saved open', () => {
    start(); click('Mathematics Higher level'); click('All years'); click('2018'); click('Save Paper 1');
    expect(listPins()).toHaveLength(1);
    expect(listPins()[0].key).toBe('mathematics|2018|higher|ev|one.pdf');
    click('Paper Trail'); click('Saved'); click(/Mathematics · Paper 1\s*2018/);
    expect(reader.props?.paper.url).toContain(encodeURIComponent('/2018/paper/one.pdf'));
    click('Close reader');
    expect(screen.getByRole('combobox', { name: 'Choose a year' })).toHaveTextContent('2018');
    click('Paper Trail');
    expect(screen.getByRole('button', { name: 'Continue' })).toBeInTheDocument();
  });

  it('keeps unavailable-year explanations, level/language filters and accessible formats', async () => {
    start(); click('Mathematics Higher level'); click('All years'); click(/2020 unavailable/);
    expect(screen.getByRole('status')).toHaveTextContent('The exams were cancelled.');
    click('2026');
    click('Ordinary level');
    fireEvent.click(screen.getByRole('combobox', { name: 'Paper language' }));
    fireEvent.click(await screen.findByRole('option', { name: 'Gaeilge' }));
    click('Paper 1 modified · accessible format');
    expect(reader.props?.paper.url).toContain('accessible.pdf');
    expect(reader.props?.answersUrl).toBeUndefined();
    expect(reader.props?.topics).toBeUndefined();
  });

  it('opens a paper without a scheme without inventing Answers or Topics', () => {
    start(); click('Mathematics Higher level');
    fireEvent.click(within(screen.getByRole('article', { name: 'Paper 2' })).getByRole('button', { name: 'Open paper' }));
    expect(reader.props?.paper.url).toContain('two.pdf');
    expect(reader.props?.scheme).toBeUndefined();
    expect(reader.props?.answersUrl).toBeUndefined();
    expect(reader.props?.topics).toBeUndefined();
  });

  it('offers the archive with an empty profile and keeps non-LCA search in the correct cycle', async () => {
    render(<PaperTrail />);
    click('Browse all subjects');
    expect(screen.getAllByRole('button', { name: /Mathematics\s*Higher level/ })).toHaveLength(1);
    const user = userEvent.setup();
    await user.click(screen.getByRole('combobox', { name: 'Find a subject or paper' }));
    await user.type(screen.getByRole('combobox', { name: 'Find a subject or paper' }), 'maths 2018 hl');
    expect(screen.queryByRole('button', { name: /LCA/ })).not.toBeInTheDocument();
    fireEvent.click(await screen.findByRole('option', { name: 'Mathematics · 2018 · Higher' }));
    expect(screen.getByRole('combobox', { name: 'Choose a year' })).toHaveTextContent('2018');
  });
});
