import { fireEvent, render, screen, within } from '@testing-library/react';
import { describe, it, expect, vi } from 'vitest';
import FrenchRubricPanel from '../components/MarkBank/FrenchRubricPanel';
import SessionScreen from '../components/MarkBank/SessionScreen';
import { FRENCH_WRITING_CARDS as cards } from '../components/MarkBank/cards/french/writing';
import { FRENCH_READING_CARDS } from '../components/MarkBank/cards/french/reading';
import type { FrenchRubric, SecRubricCard } from '../types/markBank';
import { FRENCH_ATTEMPT_ID } from '../components/MarkBank/frenchRubric';

vi.mock('../components/PaperTrail/vaultDocs', () => ({ vaultPdf: vi.fn(() => new Promise(() => {})) }));

describe('French writing presentation', () => {
  it('lets the student select one printed MCQ option without revealing the answer', () => {
    const card = FRENCH_READING_CARDS.find(card => card.id === 'fr-2026-ol-reading-a3-q6')!;
    render(<SessionScreen cards={[card]} subjectLabel="French" onGrade={vi.fn()} onFinish={vi.fn()} onExit={vi.fn()} />);
    expect(screen.getAllByRole('radio')).toHaveLength(4);
    fireEvent.click(screen.getByRole('radio', { name: 'gagner de l’argent' }));
    expect(screen.getByRole('radio', { name: 'gagner de l’argent' })).toBeChecked();
    fireEvent.click(screen.getByRole('radio', { name: 'finir le Vendée Globe' }));
    expect(screen.getByRole('radio', { name: 'finir le Vendée Globe' })).toBeChecked();
    expect(screen.getByRole('radio', { name: 'gagner de l’argent' })).not.toBeChecked();
    expect(screen.queryByText('SEC French marking scheme')).not.toBeInTheDocument();
  });
  it('keeps reading answers behind reveal and records the chosen partial-credit mark', () => {
    const card = FRENCH_READING_CARDS.find(card => card.id === 'fr-2026-ol-reading-a1-q5')!;
    render(<SessionScreen cards={[card]} subjectLabel="French" onGrade={vi.fn()} onFinish={vi.fn()} onExit={vi.fn()} />);
    expect(screen.queryByText(/Psychology and Law/)).not.toBeInTheDocument();
    fireEvent.click(screen.getByRole('button', { name: /Read Reading Comprehension 1/i }));
    fireEvent.click(within(screen.getByRole('dialog')).getByRole('button', { name: /close/i }));
    fireEvent.click(screen.getByRole('button', { name: /reveal/i }));
    expect(screen.getByText(/Psychology and Law/)).toBeInTheDocument();
    expect(screen.getByText('Accepted answers and partial credit')).toBeInTheDocument();
    fireEvent.change(screen.getByLabelText('Response mark'), { target: { value: '2' } });
    expect(screen.getByLabelText('Response mark')).toHaveValue('2');
    expect(screen.getAllByText('2 / 4').length).toBeGreaterThan(0);
  });
  it('renders the actual language bands and an explicit attempt control for the form', () => {
    const card = cards.find(c => c.id.endsWith('b1b-route-678'))! as SecRubricCard & { rubric: FrenchRubric };
    const onScore = vi.fn();
    const { rerender } = render(<FrenchRubricPanel card={card} scores={{}} onScore={onScore} />);
    expect(screen.getByLabelText('Language mark')).toBeDisabled();
    fireEvent.click(screen.getByRole('button', { name: 'Confirm a communicative task was attempted' }));
    expect(onScore).toHaveBeenCalledWith(FRENCH_ATTEMPT_ID, 1);
    rerender(<FrenchRubricPanel card={card} scores={{ [FRENCH_ATTEMPT_ID]: 1 }} onScore={onScore} />);
    expect(screen.getByLabelText('Language mark')).toBeEnabled();
    fireEvent.change(screen.getByLabelText('Language mark'), { target: { value: '8' } });
    expect(onScore).toHaveBeenCalledWith('french:language', 8);
    expect(screen.getByText('Top · 6–8 marks')).toBeInTheDocument();
    expect(screen.queryByText(/PCLM/)).not.toBeInTheDocument();
  });

  it('keeps our practice guidance apart from the SEC scheme under its own label', () => {
    const card = cards.find(c => c.id === 'fr-2014-ol-writing-b3b-route-123')! as SecRubricCard & { rubric: FrenchRubric };
    render(<FrenchRubricPanel card={card} scores={{}} onScore={vi.fn()} />);
    const notes = screen.getByRole('region', { name: 'NextStepUni practice notes' });
    expect(within(notes).getByText('Not part of the SEC marking scheme.', { exact: false })).toBeInTheDocument();
    expect(within(notes).getByText('Use the formal letter layout and the supplied addresses.')).toBeInTheDocument();
    expect(screen.getByText('Top of page - 3 marks (France not necessary in address)')).toBeInTheDocument();
    expect(screen.getByText('Rédigez vos réponses en français.')).toBeInTheDocument();
    // The empty legacy note no longer renders as scheme text.
    expect(document.querySelector('.mb-french-note')).toBeNull();
  });

  it('opens and closes required source material before revealing the marking grid', () => {
    const card = cards.find(c => c.id.endsWith('hl-writing-b1a'))!;
    render(<SessionScreen cards={[card]} subjectLabel="French" onGrade={vi.fn()} onFinish={vi.fn()} onExit={vi.fn()} />);
    expect(screen.queryByText('SEC French marking scheme')).not.toBeInTheDocument();
    const triggers = screen.getAllByRole('button', { name: /^Read Section/i });
    expect(triggers).toHaveLength(2);
    fireEvent.click(triggers[1]);
    const reader = screen.getByRole('dialog');
    expect(within(reader).getByText('Reading passage referenced by this task')).toBeInTheDocument();
    fireEvent.click(within(reader).getByRole('button', { name: /close/i }));
    expect(screen.queryByRole('dialog')).not.toBeInTheDocument();
    fireEvent.click(screen.getByRole('button', { name: /reveal/i }));
    expect(screen.getByText('SEC French marking scheme')).toBeInTheDocument();
    expect(screen.getByLabelText('Communication mark')).toBeInTheDocument();
  });
});
