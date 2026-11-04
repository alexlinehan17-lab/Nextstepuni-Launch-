/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 *
 * Paper Trail — deferred sittings, sample papers and earlier-syllabus years in
 * the archive UI. The deferred sitting shares its June year entry but never
 * its documents: each deferred item carries its own "-deferred" fileids, so it
 * opens its own scheme and its own Storage objects.
 */

import React from 'react';
import { beforeEach, describe, expect, it, vi } from 'vitest';
import { fireEvent, render, screen, within } from '@testing-library/react';
import PaperTrail from '../components/PaperTrail';
import type { PaperEntry } from '../types/paperTrail';

interface ReaderProps {
  title: string;
  subtitle: string;
  paper: { url: string };
  scheme?: { url: string };
  answersUrl?: string;
  onClose: () => void;
}
const reader = vi.hoisted(() => ({ props: null as ReaderProps | null }));
vi.mock('../utils/bootParams', () => ({ getBootParam: () => null }));
vi.mock('../components/PaperTrail/Viewer', () => ({ default: (props: ReaderProps) => {
  reader.props = props;
  return <div aria-label="Paper Trail reader"><button onClick={props.onClose}>Close reader</button></div>;
} }));
vi.mock('../components/PaperTrail/PaperCover', () => ({ default: () => <span>Cover</span> }));
vi.mock('../components/PaperTrail/archiveHealth', () => ({ archiveHealth: () => Promise.resolve('ok') }));
vi.mock('../firebase', () => ({ db: {} }));
vi.mock('../contexts/ProgressContext', () => ({ useProgress: () => ({ updateDemoProgress: () => {} }) }));
vi.mock('../hooks/useFreshProgress', () => ({ useFreshProgress: () => ({ loaded: true, doc: null }) }));
vi.mock('../components/PaperTrail/topics', () => ({ taggedSubjects: () => [], topicsForPaper: () => null }));
vi.mock('../paperTrailData', () => {
  const june = (year: number): PaperEntry => ({
    year, level: 'higher', lang: 'ev', papers: [
      { label: 'Paper 1', doc: { f: 'one.pdf', b: 100 }, scheme: { f: 'one.pdf', b: 200 }, answers: 1 },
    ],
  });
  // The deferred sitting is its own entry, right after June's for the year.
  const deferred: PaperEntry = {
    year: 2023, level: 'higher', lang: 'ev', sitting: 'deferred', papers: [
      { label: 'Deferred · Paper 1', sitting: 'deferred', doc: { f: 'one-deferred.pdf', b: 300 }, scheme: { f: 'one-deferred.pdf', b: 400 } },
    ],
  };
  const sample = (f: string): PaperEntry => ({
    year: 2027, level: 'higher', lang: 'ev', sitting: 'sample',
    note: 'Official SEC sample papers for the new specification, first examined in 2027. No marking schemes were published with them.',
    papers: [{ label: 'Sample Paper 1', sitting: 'sample', doc: { f, b: 500 } }],
  });
  return {
    PAPER_TRAIL_SUBJECTS: [
      { id: 'accounting', name: 'Accounting', cycle: 'lc', levels: ['higher'] },
      { id: 'biology', name: 'Biology', cycle: 'lc', levels: ['higher'] },
      { id: 'climate-action-and-sustainable-development', name: 'Climate Action and Sustainable Development', cycle: 'lc', levels: ['higher'] },
    ],
    PAPER_TRAIL_INDEX: {
      accounting: [june(2026), june(2023), deferred, june(1996)],
      biology: [sample('bio-sample.pdf'), june(2026)],
      'climate-action-and-sustainable-development': [sample('casd-sample.pdf')],
    },
    PAPER_TRAIL_GAPS: [],
  };
});

const start = () => render(<PaperTrail studentSubjects={['Accounting', 'Biology', 'Climate Action and Sustainable Development']} />);
const click = (name: string | RegExp) => fireEvent.click(screen.getByRole('button', {
  name: typeof name === 'string' ? new RegExp('^' + name.replaceAll(' ', '\\s*') + '$') : name,
}));

describe('Paper Trail sittings and syllabus eras', () => {
  beforeEach(() => { localStorage.clear(); reader.props = null; });

  it('lists the deferred sitting under its own heading with its own scheme', () => {
    start(); click(/^Accounting/); click('All years');
    click('2023, With deferred');
    expect(screen.getByRole('heading', { name: '2023 · Deferred sitting' })).toBeInTheDocument();
    const deferred = within(screen.getByRole('article', { name: 'Deferred · Paper 1' }));
    fireEvent.click(deferred.getByRole('button', { name: /Open marking scheme/ }));
    expect(reader.props?.paper.url).toContain(encodeURIComponent('papers/lc/accounting/2023/paper/one-deferred.pdf'));
    expect(reader.props?.scheme?.url).toContain(encodeURIComponent('papers/lc/accounting/2023/scheme/one-deferred.pdf'));
    // The deferred paper has no answer map of its own — never the June one's.
    expect(reader.props?.answersUrl).toBeUndefined();
    expect(reader.props?.subtitle).toBe('Deferred · Paper 1 · Higher');
    click('Close reader');
    const juneCard = within(screen.getByRole('article', { name: 'Paper 1' }));
    fireEvent.click(juneCard.getByRole('button', { name: /Open marking scheme/ }));
    expect(reader.props?.scheme?.url).toContain(encodeURIComponent('papers/lc/accounting/2023/scheme/one.pdf'));
    expect(reader.props?.answersUrl).toBeTruthy();
  });

  it('names the deferred sitting in the paper-and-scheme dialog', async () => {
    start(); click(/^Accounting/); click('All years'); click('2023, With deferred');
    fireEvent.click(within(screen.getByRole('article', { name: 'Deferred · Paper 1' }))
      .getByRole('button', { name: 'Paper & marking scheme' }));
    const dialog = within(await screen.findByRole('dialog'));
    expect(dialog.getByText('Accounting · 2023 · Deferred sitting · Higher level · English')).toBeInTheDocument();
  });

  it('saves and reopens a deferred paper as itself, not as the June paper', () => {
    start(); click(/^Accounting/); click('All years'); click('2023, With deferred');
    click('Save Deferred · Paper 1');
    click('Paper Trail'); click('Saved');
    click(/Accounting · Deferred · Paper 1\s*2023/);
    expect(reader.props?.paper.url).toContain(encodeURIComponent('/2023/paper/one-deferred.pdf'));
  });

  it('tags and explains a paper set on an earlier syllabus', () => {
    start(); click(/^Accounting/); click('All years');
    expect(screen.getByText('Years marked “Earlier syllabus” were set before the 1997 syllabus change.')).toBeInTheDocument();
    click('1996, Earlier syllabus');
    expect(screen.getByText('Earlier syllabus. The current Accounting syllabus was first examined in 1997.')).toBeInTheDocument();
    fireEvent.click(within(screen.getByRole('article', { name: 'Paper 1' })).getByRole('button', { name: 'Open paper' }));
    expect(reader.props?.subtitle).toBe('Paper 1 · Higher · Earlier syllabus');
    expect(reader.props?.title).toBe('Accounting · 1996');
  });

  it('keeps the newest June sitting as the default when sample papers exist', () => {
    start(); click(/^Biology/);
    expect(screen.getByRole('combobox', { name: 'Choose a year' })).toHaveTextContent('2026');
    expect(screen.getByText('Earlier syllabus. A new Biology specification is first examined in 2027.')).toBeInTheDocument();
  });

  it('shows a new subject’s official sample papers as samples, without a scheme', () => {
    start(); click(/^Climate Action and Sustainable Development/);
    expect(screen.getByRole('heading', { name: 'Sample papers' })).toBeInTheDocument();
    expect(screen.getByRole('combobox', { name: 'Choose a year' })).toHaveTextContent('2027 · Sample');
    expect(screen.getByText(/No marking schemes were published with them/)).toBeInTheDocument();
    const card = within(screen.getByRole('article', { name: 'Sample Paper 1' }));
    expect(card.getByText('Marking scheme not published')).toBeInTheDocument();
    fireEvent.click(card.getByRole('button', { name: 'Open paper' }));
    expect(reader.props?.title).toBe('Climate Action and Sustainable Development · 2027 sample');
    expect(reader.props?.scheme).toBeUndefined();
  });
});
