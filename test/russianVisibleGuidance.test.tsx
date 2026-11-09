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
  it('shows the 2012 handwriting allocation and its printed bilingual total discrepancy',async()=>{
    reveal('ir1-iv-a','ol',2012);
    await waitFor(()=>expect(screen.getByText(/The two dish names carry 5 marks each and the drink name 3/)).toBeVisible());
    expect(screen.getByText(/its Irish heading gives 30/)).toHaveTextContent('original paper total 35');
    fireEvent.click(screen.getByRole('button',{name:'Set Dish one to 5 marks'}));
    fireEvent.click(screen.getByRole('button',{name:'Set Drink to 3 marks'}));
    await waitFor(()=>expect(screen.getByText(/placement is 8 of 13 marks/)).toBeVisible());
  });
  it('shows the 2012 question-level hotel partial and source repeat-information rule',async()=>{
    reveal('ir2-ii','ol',2012);
    await waitFor(()=>expect(screen.getByText('one mark: hotel')).toBeVisible());
    expect(screen.getByText(/Hotel alone is one partial detail/)).toHaveTextContent('counted once within the six-detail quota');
    expect(screen.getByText(/Where a candidate uses the same information/)).toBeVisible();
    expect(screen.getByText('Maldron Hotel/Tallaght')).toBeVisible();
    expect(screen.getByText('comfortable/stylish hotel')).toBeVisible();
  });
  it('shows the 2013 handwriting discount and the published benefits-count discrepancy',async()=>{
    reveal('ir1-i','ol',2013);
    await waitFor(()=>expect(screen.getByText(/The scheme discounts the handwriting column/)).toBeVisible());
    expect(screen.getByText(/Discount as majority/)).toBeVisible();
    cleanup();reveal('cd-3-ii','ol',2013);
    await waitFor(()=>expect(screen.getByText(/Source discrepancy: the booklet asks for two benefits/)).toBeVisible());
    expect(screen.getByText(/The two-answer quota and four-mark total are retained/)).toHaveTextContent('Three of');
  });
  it('shows the 2013 learner-group quotas and the open gender-phrase allowance',async()=>{
    reveal('ir2-ii','ol',2013);
    await waitFor(()=>expect(screen.getByText(/Choose five learner groups and two details in each/)).toBeVisible());
    expect(screen.getByText('2 groups // primary/beginners’ school/ 1-4 classes')).toBeVisible();
    cleanup();reveal('la1','ol',2013);
    await waitFor(()=>expect(screen.getByText(/The printed example банкетный зал cannot be used/)).toBeVisible());
    expect(screen.getAllByText(/whether it is in the text or not/).length).toBeGreaterThan(0);
  });
  it('renders both complete 2014 matching routes with ten four-mark answers',async()=>{
    const card=REVIEWED_CARDS.find(c=>c.id==='ru-2014-ol-mm');
    if(!card)throw new Error('Missing matching card');
    render(<SessionScreen cards={[card]} subjectLabel="Russian" onGrade={vi.fn()} onFinish={vi.fn()} onExit={vi.fn()} />);
    fireEvent.click(screen.getByRole('button',{name:'Profession then position'}));
    fireEvent.click(screen.getByRole('button',{name:'Reveal the marking scheme'}));
    await waitFor(()=>expect(screen.getAllByRole('button',{name:/4m$/})).toHaveLength(10));
    const lawyer=screen.getByRole('button',{name:/^Юрист /});
    fireEvent.click(lawyer);
    expect(lawyer).toHaveAttribute('aria-pressed','true');
    await waitFor(()=>expect(screen.getByText(/You claimed 4 of 40 marks/)).toBeVisible());
    fireEvent.click(screen.getByRole('button',{name:'Position then profession'}));
    await waitFor(()=>expect(screen.getByRole('button',{name:/^Юрист /})).toHaveAttribute('aria-pressed','false'));
    expect(screen.getAllByRole('button',{name:/4m$/})).toHaveLength(10);
  });

  it('shows the 2014 paper handwriting split and total-only classification limit',async()=>{
    reveal('la1','ol',2014);
    await waitFor(()=>expect(screen.getByText(/The original paper supplies this 3 \+ 3 allocation/)).toBeVisible());
    expect(screen.getByText('Letter formation')).toBeVisible();
    expect(screen.getByText('Accurate transcription')).toBeVisible();
    cleanup();reveal('la2','ol',2014);
    await waitFor(()=>expect(screen.getByText(/numeric self-scoring is unavailable/)).toBeVisible());
    expect(screen.getByText(/The scheme gives 10 marks/)).toHaveTextContent('no per-word allocation');
  });
  it('shows the 2014 explicit partial-answer guidance and scoped writing requirements',async()=>{
    reveal('sd','ol',2014);
    await waitFor(()=>expect(screen.getByText(/gap 3 accepts “Кто”/)).toBeVisible());
    expect(screen.getByText(/gap 3 accepts “Кто”/)).toHaveTextContent('“Сколько” for 1 mark');
    cleanup();reveal('ew','ol',2014);
    await waitFor(()=>expect(screen.getByText(/Choice 3: Opening\/greeting; congratulations/)).toBeVisible());
    expect(screen.getByText(/Choice 3: Opening\/greeting; congratulations/)).toHaveTextContent('Small talk; Signing off');
  });

  it('shows the 2015 half-credit rule and conflicting published labels',async()=>{
    reveal('la2','ol',2015);
    await waitFor(()=>expect(screen.getByText(/Source discrepancy: the scheme prints/)).toBeVisible());
    expect(screen.getByText(/The English and Russian labels disagree/)).toHaveTextContent('feminine singular / мужской род');
    expect(screen.getAllByText(/Assign half the available marks/).length).toBe(6);
    expect(screen.getAllByRole('button',{name:/^Award 0\.5 marks for/}).length).toBe(4);
  });
  it('shows the 2015 matching headline discrepancy and complete handwritten targets',async()=>{
    reveal('mm-ii','ol',2015);
    await waitFor(()=>expect(screen.getByText(/Source wording differs/)).toBeVisible());
    expect(screen.getByText(/Source wording differs/)).toHaveTextContent('Сюрпризы погоды');
    cleanup();reveal('la1','ol',2015);
    await waitFor(()=>expect(screen.getByText(/no per-phrase allocation is inferred/)).toBeVisible());
    expect(screen.getByRole('button',{name:/^Award 5\.5 marks for/})).toBeVisible();
  });
  it('shows the2018 handwriting allocation limitation',async()=>{
    reveal('la1','ol',2018);
    await waitFor(()=>expect(screen.getByText(/The scheme gives 6 marks for both phrases/)).toBeVisible());
    expect(screen.getByText(/numeric self-scoring is unavailable/)).toHaveTextContent('without per-phrase allocations or a handwritten exemplar');
  });
  it('shows the2018 listening rate and no-credit examples',async()=>{
    reveal('l1-4','ol',2018);
    await waitFor(()=>expect(screen.getByText('Award five marks for each correct/relevant point.')).toBeVisible());
    expect(screen.getByText('no marks: seat downstairs, ticket for coupe wagon, wagon P')).toBeVisible();
    expect(screen.getByText(/If an answer is written entirely in Russian/)).toBeVisible();
  });
  it('shows the2019 mandatory dialogues and overall-only allocation',async()=>{
    reveal('sd','ol',2019);
    await waitFor(()=>expect(screen.getByText(/Complete both Group A and Group B/)).toBeVisible());
    expect(screen.getByText(/numeric self-scoring is unavailable/)).toHaveTextContent('20 marks');
  });
  it('shows the2019 accepted earlier prices and no-repeat condition',async()=>{
    reveal('ir1-7','ol',2019);
    await waitFor(()=>expect(screen.getByText(/Accept answers referring to price options from earlier in the text/)).toBeVisible());
    expect(screen.getByText(/Accept answers referring to price options from earlier in the text/)).toHaveTextContent('if marks have not already been awarded');
    expect(screen.getByText('детский билет (7‐13 лет) стоит 800 руб')).toBeVisible();
  });
  it('shows the2021 ordered listening tariff and explicit Russian exception',async()=>{
    reveal('l3-4','ol',2021);
    await waitFor(()=>expect(screen.getByText(/Any 2 of these.*2 then 3 marks/)).toBeVisible());
    expect(screen.getByText(/Published tariff: 2 marks \+ 3 marks/)).toHaveTextContent('If an answer is written entirely in Russian – do not penalise');
    expect(screen.getByText('Tretyakov Gallery')).toBeVisible();
  });
  it('shows the claimable 2022 Ordinary festival-name maximum',async()=>{
    reveal('cd-6','ol',2022);
    await waitFor(()=>expect(screen.getByText('Max 2 marks for mentioning the name of a festival')).toBeVisible());
    expect(screen.getByText('mentioning the name of a festival')).toBeVisible();
    expect(screen.getByText(/Marking scheme page 3: Do not penalise answers supplied in Russian/)).toBeVisible();
  });
  it('shows the 2022 Higher Russian listening exception and explicit qualifications',async()=>{
    reveal('l2-1-ii','hl',2022);
    await waitFor(()=>expect(screen.getByText('Accept answers written in Russian.')).toBeVisible());
    expect(screen.getByText(/must mention ‘liked’/)).toBeVisible();
    expect(screen.getByText('Award no marks: Russian school')).toBeVisible();
  });
  it('shows both 2022 forms within their original grammar gap',async()=>{
    reveal('gr','hl',2022);
    await waitFor(()=>expect(screen.getByText(/The paper has 14 bracketed gaps/)).toBeVisible());
    expect(screen.getByText('близкими')).toBeVisible();
    expect(screen.getByText('людьми')).toBeVisible();
    expect(screen.getByText('15 x 2 marks')).toBeVisible();
  });
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
