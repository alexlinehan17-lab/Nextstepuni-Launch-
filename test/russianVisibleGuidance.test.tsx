import { cleanup, fireEvent, render, screen, waitFor } from '@testing-library/react';
import { afterEach, describe, expect, it, vi } from 'vitest';
import SessionScreen from '../components/MarkBank/SessionScreen';
import { REVIEWED_CARDS } from '../components/MarkBank/cards/russian/reviewed';

afterEach(cleanup);

function reveal(suffix:string) {
  const card=REVIEWED_CARDS.find(c=>c.id===`ru-2026-hl-${suffix}`);
  if(!card)throw new Error(suffix);
  render(<SessionScreen cards={[card]} subjectLabel="Russian" onGrade={vi.fn()} onFinish={vi.fn()} onExit={vi.fn()} />);
  fireEvent.click(screen.getByRole('button',{name:'Reveal the marking scheme'}));
}

describe('Russian source directions visible in the practice session',()=>{
  it.each(['c1-1-i','c2-1'])('shows both permitted response languages for %s',async suffix=>{
    reveal(suffix);
    await waitFor(()=>expect(screen.getByText(/Answer in English or Irish\. Both languages are permitted/)).toBeVisible());
  });
  it('shows the whole-exercise grammar allocation and wrong-language direction',async()=>{
    reveal('gr');
    const note=screen.getByText(/The complete exercise is marked out of 30/);
    await waitFor(()=>expect(note).toBeVisible());
    expect(note).toHaveTextContent('When it should be Russian: award NO marks.');
    expect(note).toHaveTextContent('does not print separate marks for individual forms');
  });
  it('shows the unresolved July1/July7 source discrepancy',async()=>{
    reveal('l4-1-i');
    const note=screen.getByText(/The answer list prints “7th July 1939”/);
    await waitFor(()=>expect(note).toBeVisible());
    expect(note).toHaveTextContent('1 июля 1939 года');
    expect(note).toHaveTextContent('source discrepancy remains under review');
  });
});
