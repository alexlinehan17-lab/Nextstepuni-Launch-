import { beforeEach, describe, expect, it, vi } from 'vitest';
import { fireEvent, render, screen } from '@testing-library/react';
import VaultQuestionCard from '../components/PaperTrail/VaultQuestionCard';
import answerMap from '../public/paper-answers/2010/LC024ALP000IV.pdf.json';

vi.mock('../components/PaperTrail/vaultDocs', () => ({ vaultPdf: vi.fn(async () => ({})) }));
vi.mock('../components/PaperTrail/CropView', () => ({ default: () => <div>Original PDF crop</div> }));

beforeEach(() => {
  vi.stubGlobal('IntersectionObserver', undefined);
  // An absent observer makes this card visible immediately in jsdom.
  delete (window as unknown as Record<string, unknown>).IntersectionObserver;
  vi.stubGlobal('fetch', vi.fn(async () => ({ ok:true, json:async () => answerMap })));
});

describe('reviewed source discrepancies', () => {
  it('reveals the actual Irish genetics source note with the scheme and hides it again', async () => {
    const note = answerMap.q.find(q => q.n === '7')!.schemeNote!;
    render(<VaultQuestionCard
      sibling={{ subjectId:'agricultural-science',year:2010,level:'higher',lang:'iv',fileid:'LC024ALP000IV.pdf',paperKey:'single',n:'7' }}
      saved={false} onToggleReview={vi.fn()} onOpenInPaper={vi.fn()}
    />);
    const toggle = await screen.findByRole('button', { name:'Show the marking scheme' });
    expect(screen.queryByText(note)).not.toBeInTheDocument();
    fireEvent.click(toggle);
    expect(screen.getByText(note)).toBeInTheDocument();
    expect(toggle).toHaveAttribute('aria-expanded','true');
    fireEvent.click(toggle);
    expect(screen.queryByText(note)).not.toBeInTheDocument();
    expect(toggle).toHaveAttribute('aria-expanded','false');
  });
});
