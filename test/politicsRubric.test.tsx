import { describe, expect, it, vi } from 'vitest';
import { fireEvent, render, screen, waitFor } from '@testing-library/react';
import PoliticsRubricPanel, { politicsMarks } from '../components/MarkBank/PoliticsRubricPanel';
import SourceMaterialReader from '../components/MarkBank/SourceMaterialReader';
import { tariffReconciles, type PoliticsRubric, type SecRubricCard } from '../types/markBank';
import { vaultPdf } from '../components/PaperTrail/vaultDocs';

vi.mock('../components/PaperTrail/vaultDocs', () => ({ vaultPdf: vi.fn(() => new Promise(() => {})) }));

const range = (max: number) => Array.from({ length: max + 1 }, (_, index) => index);
// The two independently awarded criteria of the 2026 HL Q2(g), scheme p.12.
const card: SecRubricCard & { rubric: PoliticsRubric } = {
  id: 'politics-2026-hl-q2-g', subjectId: 'politics-and-society', level: 'higher',
  topicId: 'politics-and-society-3-4', conceptId: 'perceptions-of-africa',
  source: 'sec', kind: 'rubric', year: 2026, paperFileid: 'LC568ALP000EV.pdf', section: 'B',
  questionRef: '2026 HL Q2(g)',
  questionText: 'Drawing on the data presented in both documents and the quotation below, what conclusions can you draw about the perception of Africa as being peripheral and marginal on the global stage?',
  totalMarks: 50, schemeCitation: 'SEC Politics and Society 2026 HL, p.12',
  specVersion: 'politics-and-society:current', qa: { gates: [], humanReviewedBy: 'test fixture', humanReviewedAt: '2026-10-07' },
  rubric: {
    system: 'politics', taskRequirements: [], schemePages: [12], schemeFileid: 'LC568ALP000EV.pdf',
    markingGuideNote: 'Use the published criteria. The scheme’s examples are not exhaustive.',
    criteria: [
      { id: 'conclusions', label: 'Conclusions', maxMarks: 30, permittedMarks: range(30), guidance: [],
        bands: [
          { label: 'Weak', marks: range(8), guidance: 'confused, inaccurate' },
          { label: 'Fair', marks: range(16).slice(9), guidance: 'limited, flawed' },
          { label: 'Good', marks: range(23).slice(17), guidance: 'coherent, relevant' },
          { label: 'Very good', marks: range(30).slice(24), guidance: 'focused, insightful' },
        ] },
      { id: 'documents', label: 'Use of documents', maxMarks: 20, permittedMarks: range(20), guidance: ['Comprehensive use of documents.'] },
    ],
  },
};

describe('Politics and Society published marking', () => {
  it('adds criterion placements, rejects impossible scores and validates descriptor coverage', () => {
    expect(tariffReconciles(card)).toBe(true);
    expect(politicsMarks(card, { 'politics:conclusions': 24, 'politics:documents': 16 })).toBe(40);
    expect(politicsMarks(card, { 'politics:conclusions': 31, 'politics:documents': 16 })).toBe(16);
    expect(politicsMarks(card, { 'politics:conclusions': -1, 'politics:documents': 1.5 })).toBe(0);
    expect(tariffReconciles({ ...card, totalMarks: 51 })).toBe(false);
    const bad = structuredClone(card);
    bad.rubric.criteria[0].bands![0].marks.push(9);
    expect(tariffReconciles(bad)).toBe(false);
  });

  it('shows the chosen descriptor and opens the marking scheme rather than the same-named paper', async () => {
    const onScore = vi.fn();
    render(<PoliticsRubricPanel card={card} scores={{ 'politics:conclusions': 24, 'politics:documents': 16 }} onScore={onScore} />);
    expect(screen.getByText('40 / 50')).toBeInTheDocument();
    expect(screen.getByText(/focused, insightful/, { selector: '.mb-politics-selected-band' })).toBeVisible();
    fireEvent.change(screen.getByRole('combobox', { name: 'Conclusions mark' }), { target: { value: '30' } });
    expect(onScore).toHaveBeenCalledWith('politics:conclusions', 30);
    fireEvent.click(screen.getByRole('button', { name: /Read the official scheme/ }));
    await waitFor(() => expect(vaultPdf).toHaveBeenCalledWith(expect.stringContaining('%2Fscheme%2FLC568ALP000EV.pdf')));
    expect(screen.getByRole('link', { name: 'Open the original marking scheme' }).getAttribute('href')).toContain('#page=12');
    fireEvent.keyDown(screen.getByRole('dialog'), { key: 'Escape' });
    expect(screen.queryByRole('dialog')).not.toBeInTheDocument();
  });

  it('keeps both source documents and the additional map accessible before marking', async () => {
    render(<SourceMaterialReader subjectId={card.subjectId} year={2026} paperFileid={card.paperFileid!} source={{
      kind: 'source-data', label: 'Documents A and B', title: 'Maps and perceptions of Africa', pages: [8, 9, 12],
      attribution: '© State Examinations Commission', presentationNote: 'Original examination pages.',
    }} />);
    fireEvent.click(screen.getByRole('button', { name: /Read Documents A and B/ }));
    expect(screen.getAllByLabelText(/Source page \d of 3/)).toHaveLength(3);
    await waitFor(() => expect(vaultPdf).toHaveBeenCalledWith(expect.stringContaining('%2Fpaper%2FLC568ALP000EV.pdf')));
    fireEvent.click(screen.getByRole('button', { name: 'Go to source page 3' }));
    expect(screen.getByRole('link', { name: 'Open the original paper' }).getAttribute('href')).toContain('#page=12');
    fireEvent.click(screen.getByRole('button', { name: 'Close source material' }));
    expect(screen.queryByRole('dialog')).not.toBeInTheDocument();
  });
});
