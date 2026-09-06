import React from 'react';
import { beforeEach, describe, expect, it, vi } from 'vitest';
import { fireEvent, render, screen, within } from '@testing-library/react';
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
vi.mock('../components/PaperTrail/Viewer', () => ({ default: (props: ReaderProps) => {
  reader.props = props;
  return <div aria-label="Paper Trail reader">
    <button onClick={() => props.onPosition('paper', 4)}>Read paper page 4</button>
    <button onClick={() => props.onPosition('scheme', 7)}>Read scheme page 7</button>
    <button onClick={props.onClose}>Close reader</button>
  </div>;
} }));
vi.mock('../components/PaperTrail/PaperCover', () => ({ default: () => <span>Cover</span> }));
vi.mock('../firebase', () => ({ db: {} }));
vi.mock('../contexts/ProgressContext', () => ({ useProgress: () => ({ updateDemoProgress: () => {} }) }));
vi.mock('../hooks/useFreshProgress', () => ({ useFreshProgress: () => ({ loaded: true, doc: null }) }));
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
  beforeEach(() => { localStorage.clear(); reader.props = null; });

  it('opens the paper preview in the paired reader with Answers and Topics', () => {
    start(); click('Mathematics Higher level'); click('Open Paper 1 preview');
    expect(screen.getByLabelText('Paper Trail reader')).toBeInTheDocument();
    expect(reader.props?.paper.url).toContain(encodeURIComponent('papers/lc/mathematics/2026/paper/one.pdf'));
    expect(reader.props?.scheme?.url).toContain(encodeURIComponent('papers/lc/mathematics/2026/scheme/one.pdf'));
    expect(reader.props?.initialSide).toBe('paper');
    expect(reader.props?.answersUrl).toBeTruthy();
    expect(reader.props?.topics).toBeTruthy();
  });

  it('opens the matching scheme and restores each side’s latest position through Continue', () => {
    start(); click('Mathematics Higher level');
    fireEvent.click(paperOne().getByRole('button', { name: /Marking scheme/ }));
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
    expect(screen.getByRole('button', { name: '2018 · All years' })).toHaveAttribute('aria-pressed', 'true');
    click('Paper Trail');
    expect(screen.getByRole('button', { name: 'Continue' })).toBeInTheDocument();
  });

  it('keeps unavailable-year explanations, level/language filters and accessible formats', () => {
    start(); click('Mathematics Higher level'); click('All years'); click(/2020 unavailable/);
    expect(screen.getByRole('status')).toHaveTextContent('The exams were cancelled.');
    click('2026');
    fireEvent.change(screen.getByRole('combobox', { name: 'Level' }), { target: { value: 'ordinary' } });
    fireEvent.change(screen.getByRole('combobox', { name: 'Paper language' }), { target: { value: 'iv' } });
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

  it('offers the archive with an empty profile and keeps non-LCA search in the correct cycle', () => {
    render(<PaperTrail />);
    click('Browse all subjects');
    expect(screen.getAllByRole('button', { name: /Mathematics\s*Higher level/ })).toHaveLength(1);
    fireEvent.change(screen.getByRole('searchbox'), { target: { value: 'maths 2018 hl' } });
    expect(screen.queryByRole('button', { name: /LCA/ })).not.toBeInTheDocument();
    click('Mathematics 2018 · Higher');
    expect(screen.getByRole('button', { name: '2018 · All years' })).toHaveAttribute('aria-pressed', 'true');
  });
});
