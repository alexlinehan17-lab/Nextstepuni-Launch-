import { cleanup, fireEvent, render, screen, waitFor } from '@testing-library/react';
import { afterEach, describe, expect, it, vi } from 'vitest';
import SessionScreen from '../components/MarkBank/SessionScreen';
import { CARDS } from '../components/MarkBank/cards/lcvp/common';
import { vaultPdf } from '../components/PaperTrail/vaultDocs';
import { paperStoragePath, paperUrl } from '../components/PaperTrail/storage';
import { paperEntry, resolvePaperFileid } from '../scripts/markbank/paperIndex.mjs';

vi.mock('../components/PaperTrail/vaultDocs', () => ({ vaultPdf: vi.fn().mockResolvedValue({}) }));
vi.mock('../components/PaperTrail/CropView', () => ({ default: () => <div>Original source page</div> }));

afterEach(() => { cleanup(); vi.clearAllMocks(); });

describe('LCVP question paper beside a separate case-study booklet', () => {
  it.each([[2015, 'LC462CLP000EV'], [2016, 'LC462CLPO00EV']] as const)(
    'binds every written section to the indexed %i exam paper', (year, fileid) => {
      for (const section of ['A', 'B', 'C']) {
        expect(resolvePaperFileid('lcvp', year, 'common', section)).toBe(fileid);
      }
    },
  );

  it('leaves duplicate exam papers and unknown companion documents unresolved', () => {
    const entry = paperEntry('lcvp', 2016, 'common');
    const original = entry.papers;
    const exam = original.find((paper: { label: string }) => paper.label === 'Exam Paper');
    const companion = original.find((paper: { label: string }) => paper.label === 'Case Study');
    try {
      entry.papers = [...original, exam];
      expect(resolvePaperFileid('lcvp', 2016, 'common', 'C')).toBeNull();
      entry.papers = [exam, { ...companion, label: 'Additional examination paper' }];
      expect(resolvePaperFileid('lcvp', 2016, 'common', 'C')).toBeNull();
    } finally {
      entry.papers = original;
    }
  });

  it('keeps every generated 2016 card attached to the whole question paper', () => {
    const cards = CARDS.filter(card => card.year === 2016);
    expect(cards).toHaveLength(39);
    expect(new Set(cards.map(card => card.paperFileid))).toEqual(new Set(['LC462CLPO00EV']));
  });

  it.each([false, true])('opens the advertisement and its four underlined terms before reveal, paper layout=%s', async paperLayout => {
    const card = CARDS.find(candidate => candidate.id === 'lcvp-2016-cl-c4b')!;
    render(<SessionScreen cards={[card]} paperLayout={paperLayout} subjectLabel="LCVP"
      onGrade={vi.fn()} onFinish={vi.fn()} onExit={vi.fn()} />);
    expect(screen.getByRole('button', { name: 'Reveal the marking scheme' })).toBeVisible();
    expect(screen.queryByText(/Response 1 of 2/)).not.toBeInTheDocument();
    fireEvent.click(screen.getByRole('button', { name: /Choco Ltd — complete original advertisement/ }));
    await screen.findByText('Original source page');
    expect(screen.getByText('PDF page 23')).toBeVisible();
    expect(screen.getByText(/The four underlined terms are interpersonal skills, covering letter, references and Personnel Manager/)).toBeVisible();
    const url = paperUrl(paperStoragePath('lc', 'link-modules', 2016, 'paper', 'LC462CLPO00EV.pdf'));
    expect(vaultPdf).toHaveBeenCalledWith(url);
    expect(screen.getByRole('link', { name: 'Open the original paper' })).toHaveAttribute('href', `${url}#page=23`);
    fireEvent.click(screen.getByRole('button', { name: 'Close source text' }));
    await waitFor(() => expect(screen.queryByText('Original source page')).not.toBeInTheDocument());
    expect(screen.getByRole('button', { name: 'Reveal the marking scheme' })).toBeVisible();
    expect(screen.queryByText(/Response 1 of 2/)).not.toBeInTheDocument();
  });
});
