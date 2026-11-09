import { cleanup, fireEvent, render, screen, waitFor } from '@testing-library/react';
import { afterEach, describe, expect, it, vi } from 'vitest';
import SessionScreen from '../components/MarkBank/SessionScreen';
import { REVIEWED_CARDS } from '../components/MarkBank/cards/russian/reviewed';

afterEach(cleanup);

function reveal(suffix:string, level='hl', year=2026) {
  const card=REVIEWED_CARDS.find(c=>c.id===`ru-${year}-${level}-${suffix}`);
  if(!card)throw new Error(suffix);
  render(<SessionScreen cards={[card]} subjectLabel="Russian" onGrade={vi.fn()} onFinish={vi.fn()} onExit={vi.fn()} />);
  fireEvent.click(screen.getByRole('button',{name:'Reveal the marking scheme'}));
}

describe('Russian source directions visible in the practice session',()=>{
  it('shows the unresolved 2024 Ordinary eight-lesson price discrepancy',async()=>{
    reveal('l3-2','ol',2024);
    const note=screen.getByText(/The answer list on marking scheme page 17 prints/);
    await waitFor(()=>expect(note).toBeVisible());
    expect(note).toHaveTextContent('80 000roubles');
    expect(note).toHaveTextContent('8,000 roubles for 8 lessons');
    expect(note).toHaveTextContent('recording has not been used to adjudicate');
  });
  it('shows both listening exceptions and the complete 2024 viewing-time answers',async()=>{
    reveal('l1-2-ii','hl',2024);
    await waitFor(()=>expect(screen.getByText('There is no penalty for excess material which does not invalidate the answer.')).toBeVisible());
    expect(screen.getByText(/incorrect contradictory answer nullifies the correct answer/)).toBeVisible();
    expect(screen.getByText('on weekdays + after 6 pm')).toBeVisible();
    expect(screen.getByText('on Saturday + before lunch')).toBeVisible();
  });
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
  it.each(['ir1-1-i','ir2-1'])('shows the Ordinary Russian-language exception for %s',async suffix=>{
    reveal(suffix,'ol');
    const direction=screen.getByText(/Marking scheme page 3: Do not penalise answers supplied in Russian/);
    await waitFor(()=>expect(direction).toBeVisible());
    expect(direction).toHaveTextContent('English or Irish');
  });
});
