import React from 'react';
import { beforeEach, describe, expect, it, vi } from 'vitest';
import { act, fireEvent, render, screen, within } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import PaperTrail from '../components/PaperTrail';
import { NavigationProvider, useNavigation } from '../contexts/NavigationContext';
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
  onSave?: () => void;
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
vi.mock('../contexts/AuthContext', () => ({ useAuth: () => ({ user: { uid: 'student-1' }, authResolved: true }) }));
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

// The top bar's one Back (area 0, the frame) replaces Paper Trail's own
// "← Paper Trail" crumb: a step inside the archive registers with the app's
// navigation, and Back goes back through it first.
const FrameBack = () => { const nav = useNavigation(); return <button onClick={nav.goBack}>Back</button>; };
const start = () => render(<NavigationProvider><FrameBack /><PaperTrail studentSubjects={['Mathematics', 'Biology']} studentLevels={[{ name: 'Mathematics', level: 'Higher' }]} /></NavigationProvider>);
const click = (name: string | RegExp) => fireEvent.click(screen.getByRole('button', { name: typeof name === 'string' ? new RegExp('^' + name.replaceAll(' ', '\\s*') + '$') : name }));
const paperOne = () => within(screen.getByRole('article', { name: 'Paper 1' }));
// Level and year are selection bars and the language a menu (area 6a, the agreed design).
const radio = (group: string, name: string) => within(screen.getByRole('radiogroup', { name: group })).getByRole('radio', { name });
async function tap(element: Element) {
  fireEvent.pointerDown(element, { pointerType: 'mouse', pointerId: 1, isPrimary: true, button: 0, buttons: 1 });
  fireEvent.pointerUp(element, { pointerType: 'mouse', pointerId: 1, isPrimary: true, button: 0, buttons: 0 });
  fireEvent.mouseDown(element, { button: 0 });
  fireEvent.mouseUp(element, { button: 0 });
  fireEvent.click(element, { button: 0, detail: 1 });
  await act(async () => { await new Promise(resolve => setTimeout(resolve, 20)); });
}

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
    expect(radio('Level', 'Ordinary')).toHaveAttribute('aria-checked', 'true');
    expect(screen.getByRole('button', { name: /Paper language/ })).toHaveTextContent('Gaeilge');
  });

  // The real cover opens its document (the preview pop-up went with the agreed page).
  it('opens the paper from its real cover in the paired reader with Answers and Topics', () => {
    start(); click('Mathematics Higher level');
    fireEvent.click(paperOne().getByRole('button', { name: 'Open the 2026 Paper 1' }));
    expect(screen.getByLabelText('Paper Trail reader')).toBeInTheDocument();
    expect(reader.props?.paper.url).toContain(encodeURIComponent('papers/lc/mathematics/2026/paper/one.pdf'));
    expect(reader.props?.scheme?.url).toContain(encodeURIComponent('papers/lc/mathematics/2026/scheme/one.pdf'));
    expect(reader.props?.initialSide).toBe('paper');
    expect(reader.props?.answersUrl).toBeTruthy();
    expect(reader.props?.topics).toBeTruthy();
  });


  it('opens the matching document from the scheme’s real cover', () => {
    start(); click('Mathematics Higher level');
    fireEvent.click(paperOne().getByRole('button', { name: 'Open the 2026 marking scheme for Paper 1' }));
    expect(screen.queryByRole('dialog')).not.toBeInTheDocument();
    expect(reader.props?.initialSide).toBe('scheme');
    expect(reader.props?.scheme?.url).toContain(encodeURIComponent('/2026/scheme/one.pdf'));
  });

  it('opens the matching scheme and restores each side’s latest position through Continue', () => {
    start(); click('Mathematics Higher level');
    fireEvent.click(paperOne().getByRole('button', { name: /Open marking scheme/ }));
    expect(reader.props?.initialSide).toBe('scheme');
    click('Read paper page 4'); click('Read scheme page 7'); click('Close reader'); click('Back');
    click('Continue');
    expect(reader.props?.initialSide).toBe('scheme');
    expect(reader.props?.initialPaperPage).toBe(4);
    expect(reader.props?.initialSchemePage).toBe(7);
  });

  it('saves the full identity and returns to the correct older year after a saved open', () => {
    // 2018 is past the year bar's newest three: open it from All years and save it from the reader's Tools.
    start(); click('Mathematics Higher level'); fireEvent.click(radio('Year', 'All years')); click('Open the 2018 Paper 1');
    act(() => { reader.props?.onSave?.(); });
    expect(listPins()).toHaveLength(1);
    expect(listPins()[0].key).toBe('mathematics|2018|higher|ev|one.pdf');
    click('Close reader'); click('Back'); click('Back'); click('Saved');
    // Saved first, then Recently opened (the reader opened it once already).
    fireEvent.click(screen.getAllByRole('button', { name: /Mathematics · Paper 1\s*2018/ })[0]);
    expect(reader.props?.paper.url).toContain(encodeURIComponent('/2018/paper/one.pdf'));
    click('Close reader');
    expect(radio('Year', '2018')).toHaveAttribute('aria-checked', 'true');
    click('Back');
    expect(screen.getByRole('button', { name: 'Continue' })).toBeInTheDocument();
  });

  it('keeps unavailable-year explanations, level/language filters and accessible formats', async () => {
    start(); click('Mathematics Higher level'); fireEvent.click(radio('Year', 'All years'));
    expect(within(screen.getByRole('list', { name: 'Every paper' })).getByText('The exams were cancelled.')).toBeInTheDocument();
    fireEvent.click(radio('Year', '2026'));
    fireEvent.click(radio('Level', 'Ordinary'));
    await tap(screen.getByRole('button', { name: /Paper language/ }));
    await tap(await screen.findByRole('menuitemradio', { name: 'Gaeilge' }));
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
    expect(radio('Year', '2018')).toHaveAttribute('aria-checked', 'true');
  });
});
