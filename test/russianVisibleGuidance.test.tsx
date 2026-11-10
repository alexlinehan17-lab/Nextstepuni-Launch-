import { cleanup, fireEvent, render, screen, waitFor, within } from '@testing-library/react';
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
  it('shows all four 2011 summary prompts and preserves manual language discretion beside the literal rules',async()=>{
    reveal('c2','hl',2011);
    await waitFor(()=>expect(screen.getByRole('button',{name:'Set Section 1 content (manual assessment) to 10 marks'})).toBeVisible());
    expect(screen.getAllByText(/How did the writer end up spending two years/)[0]).toBeVisible();
    expect(screen.getAllByText(/What benefits has Anna derived/)[0]).toBeVisible();
    expect(screen.getAllByText(/award NO marks/)[0]).toBeVisible();
    expect(screen.getAllByText(/Russian-\s*language words/)[0]).toBeVisible();
    expect(screen.getByText(/no numerical or wholly\/mixed-language threshold/)).toBeVisible();
    expect(screen.queryByRole('checkbox',{name:'All answers answered in another language'})).not.toBeInTheDocument();
    fireEvent.click(screen.getByRole('button',{name:'Assess the complete four-section response'}));
    fireEvent.click(screen.getByRole('button',{name:'Set Section 1 discretionary marks to 2 marks'}));
    await waitFor(()=>expect(screen.getByText(/placement is 2 of 45 marks/)).toBeVisible());
    for(const n of [1,2,3,4]){
      fireEvent.click(screen.getByRole('button',{name:`Set Section ${n} content (manual assessment) to 10 marks`}));
      if(n!==1)fireEvent.click(screen.getByRole('button',{name:`Set Section ${n} discretionary marks to 2 marks`}));
    }
    await waitFor(()=>expect(screen.getByText(/placement is 45 of 45 marks/)).toBeVisible());
    const incomplete=screen.getByRole('checkbox',{name:/If a candidate fails to answer all sections/});
    fireEvent.click(incomplete);
    await waitFor(()=>expect(screen.getByText(/placement is 40 of 45 marks/)).toBeVisible());
    fireEvent.click(incomplete);
    await waitFor(()=>expect(screen.getByText(/placement is 45 of 45 marks/)).toBeVisible());
  });
  it('shows the 2012 derived both-girls ceiling without automatically awarding five',async()=>{
    reveal('c1-1-ii','hl',2012);
    await waitFor(()=>expect(screen.getByText(/not a printed award or a fixed one-mark deduction/)).toBeVisible());
    for(const n of [1,2,3]){
      fireEvent.click(screen.getByRole('button',{name:`Distinct detail ${n}`}));
      fireEvent.click(screen.getByRole('button',{name:`Set Distinct detail ${n} to 2 marks`}));
    }
    await waitFor(()=>expect(screen.getByText(/placement is 6 of 6 marks/)).toBeVisible());
    fireEvent.click(screen.getByRole('checkbox',{name:'The response refers to only one girl’s feelings.'}));
    await waitFor(()=>expect(screen.getByText(/placement is 5 of 6 marks/)).toBeVisible());
    fireEvent.click(screen.getByRole('checkbox',{name:'The response refers to only one girl’s feelings.'}));
    await waitFor(()=>expect(screen.getByText(/placement is 6 of 6 marks/)).toBeVisible());
  });
  it('shows and scores both 2012 summary routes with the scoped incomplete cap',async()=>{
    reveal('c2-3','hl',2012);
    await waitFor(()=>expect(screen.getByRole('button',{name:'Four details plus discretionary marks'})).toBeVisible());
    const standard=screen.getByRole('button',{name:'Four details plus discretionary marks'}),five=screen.getByRole('button',{name:'Five details without discretionary marks'});
    const standardSection=standard.closest('section'),fiveSection=five.closest('section');
    if(!standardSection||!fiveSection)throw new Error('routes');
    fireEvent.click(standard);
    for(const n of [1,2,3,4])fireEvent.click(within(standardSection).getByRole('button',{name:`Set Distinct detail ${n} to 2 marks`}));
    fireEvent.click(within(standardSection).getByRole('button',{name:'Set Discretionary marks to 2 marks'}));
    await waitFor(()=>expect(screen.getByText(/placement is 10 of 10 marks/)).toBeVisible());
    const flag=screen.getByRole('checkbox',{name:/If a candidate fails to answer all sections/});fireEvent.click(flag);
    await waitFor(()=>expect(screen.getByText(/placement is 9 of 10 marks/)).toBeVisible());
    fireEvent.click(standard);expect(flag).toBeDisabled();fireEvent.click(five);
    for(const n of [1,2,3,4,5])fireEvent.click(within(fiveSection).getByRole('button',{name:`Set Distinct detail ${n} to 2 marks`}));
    await waitFor(()=>expect(screen.getByText(/placement is 10 of 10 marks/)).toBeVisible());
    expect(screen.getByText(/BOTH the exhibits and their importance/)).toBeVisible();
    expect(screen.queryByRole('checkbox',{name:'All answers answered in another language'})).not.toBeInTheDocument();
  });
  it('shows the original 2012 category compensation and keeps an invalid increase clearable',async()=>{
    reveal('l2-4','hl',2012);
    await waitFor(()=>expect(screen.getByRole('button',{name:'Venue'})).toBeVisible());
    const sections=['Venue','Time','Price'].map(name=>{
      const button=screen.getByRole('button',{name}),section=button.closest('section');if(!section)throw new Error(name);
      fireEvent.click(button);fireEvent.click(within(section).getByRole('button',{name:/^Claim 2 marks for/}));return section;
    });
    expect(within(sections[0]).getByRole('button',{name:/^Claim 3 marks for/})).toBeDisabled();
    fireEvent.click(within(sections[2]).getByRole('button',{name:/^Claim 1 marks for/}));
    fireEvent.click(within(sections[0]).getByRole('button',{name:/^Claim 3 marks for/}));
    await waitFor(()=>expect(screen.getByText(/placement is 6 of 6 marks/)).toBeVisible());
    fireEvent.click(within(sections[2]).getByRole('button',{name:/^Clear 1 marks for/}));
    await waitFor(()=>expect(screen.getByText(/placement is 4 of 6 marks/)).toBeVisible());
    expect(screen.getByText(/Review the increased category marks/)).toBeVisible();
    expect(within(sections[0]).getByRole('button',{name:/^Clear 3 marks for/})).toBeEnabled();
    expect(screen.getByText(/No per-word or per-line allocation is inferred/)).toBeVisible();
  });
  it('shows the 2012 cultural language exception and holiday tense discrepancy',async()=>{
    reveal('ca1','hl',2012);
    await waitFor(()=>expect(screen.getByText(/English column asks for English; the Irish column asks for Irish/)).toBeVisible());
    expect(screen.queryByRole('checkbox',{name:'All answers answered in another language'})).not.toBeInTheDocument();
    cleanup();reveal('gw','hl',2012);
    await waitFor(()=>expect(screen.getByText(/holiday blog prompt uses present-tense requirements/)).toBeVisible());
    expect(screen.getAllByText(/What you did/)[0]).toBeVisible();
  });
  it('shows 2013 two-places wording alongside three independent detail placements',async()=>{
    reveal('c1-3-ii','hl',2013);
    await waitFor(()=>expect(screen.getByText(/The question requires details about TWO PLACES/)).toBeVisible());
    fireEvent.click(screen.getByRole('button',{name:'Set Distinct detail 1 to 2 marks'}));
    fireEvent.click(screen.getByRole('button',{name:'Set Distinct detail 2 to 2 marks'}));
    fireEvent.click(screen.getByRole('button',{name:'Set Distinct detail 3 to 2 marks'}));
    await waitFor(()=>expect(screen.getByText(/placement is 6 of 6 marks/)).toBeVisible());
    expect(screen.getByText(/no per-place split or numeric incomplete-place cap/)).toBeVisible();
  });
  it('shows the complete 2013 recovered restriction and applies incomplete-response discretion',async()=>{
    reveal('c2-2','hl',2013);
    await waitFor(()=>expect(screen.getByText(/mother AND one about the father/)).toBeVisible());
    expect(screen.getAllByText(/she collected photographs of artists \/ of famous people \+ she took photos of artists/)[0]).toBeVisible();
    fireEvent.click(screen.getByRole('button',{name:'Distinct detail 1'}));
    fireEvent.click(screen.getByRole('button',{name:'Set Distinct detail 1 to 2 marks'}));
    fireEvent.click(screen.getByRole('button',{name:'Set Discretionary marks to 2 marks'}));
    await waitFor(()=>expect(screen.getByText(/placement is 4 of 10 marks/)).toBeVisible());
    fireEvent.click(screen.getByRole('checkbox',{name:/If a candidate fails to answer all sections/}));
    await waitFor(()=>expect(screen.getByText(/placement is 3 of 10 marks/)).toBeVisible());
    const languageFlag=screen.getByRole('checkbox',{name:'All answers answered in another language'});
    fireEvent.click(languageFlag);
    await waitFor(()=>expect(screen.getByText(/placement is 1 of 10 marks/)).toBeVisible());
    expect(screen.getByText('Assess Discretionary marks separately under the source guidance.')).toBeVisible();
    expect(screen.getAllByText(/Discretionary marks may be awarded/)[0]).toBeVisible();
    fireEvent.click(languageFlag);
    await waitFor(()=>expect(screen.getByText(/placement is 3 of 10 marks/)).toBeVisible());
    fireEvent.click(screen.getByRole('checkbox',{name:/If a candidate fails to answer all sections/}));
    await waitFor(()=>expect(screen.getByText(/placement is 4 of 10 marks/)).toBeVisible());
  });
  it('shows 2013 essay content bands and the literal guided Lower A overlap',async()=>{
    reveal('se','hl',2013);
    await waitFor(()=>expect(screen.getByRole('heading',{name:'Communication/content (C)'})).toBeVisible());
    const content=screen.getByRole('heading',{name:'Communication/content (C)'}).closest('section');
    if(!content)throw new Error('content');
    expect(within(content).getByText(/Excellent response. Extremely clear/)).toBeVisible();
    cleanup();reveal('gw','hl',2013);
    await waitFor(()=>expect(screen.getByRole('button',{name:'Set Communication/content (C) to 15 marks'})).toBeVisible());
    fireEvent.click(screen.getByRole('button',{name:'Set Communication/content (C) to 15 marks'}));
    fireEvent.change(screen.getByRole('spinbutton',{name:/Response length \(words\)/}),{target:{value:'140'}});
    fireEvent.click(screen.getByRole('checkbox',{name:/If the expression is very fluent/}));
    const expression=screen.getByRole('heading',{name:'Language + expression (E)'}).closest('section');
    if(!expression)throw new Error('expression');
    expect(within(expression).getByText(/9\s*[-–]\s*11 Vocabulary/)).toBeVisible();
    expect(within(expression).queryByText(/11–15 marks/)).not.toBeInTheDocument();
    expect(screen.getByText(/The choice-specific category letters/)).toBeVisible();
  });
  it('shows the 2014 reserved neighbour slots and applies independent full and partial marks',async()=>{
    reveal('c1-3-i','hl',2014);
    await waitFor(()=>expect(screen.getByRole('button',{name:'Neighbours did not: distinct detail 1'})).toBeVisible());
    fireEvent.click(screen.getByRole('button',{name:'Neighbours did not: distinct detail 1'}));
    fireEvent.click(screen.getByRole('button',{name:'Set Neighbours did not: detail 1 to 2 marks'}));
    fireEvent.click(screen.getByRole('button',{name:'Neighbours did not: distinct detail 2'}));
    fireEvent.click(screen.getByRole('button',{name:'Set Neighbours did not: detail 2 to 2 marks'}));
    fireEvent.click(screen.getByRole('button',{name:'Other distinct detail 1 — exclude the four neighbours-did-not actions'}));
    fireEvent.click(screen.getByRole('button',{name:'Set Other detail 1, excluding the four neighbours-did-not actions to 1 marks'}));
    await waitFor(()=>expect(screen.getByText(/placement is 5 of 6 marks/)).toBeVisible());
    expect(screen.getByRole('button',{name:'Other distinct detail 2 — exclude the four neighbours-did-not actions'})).toBeDisabled();
    expect(screen.getByText(/The bad\/boring partial association is not uniquely specified/)).toBeVisible();
    expect(screen.getByText(/the paper reading heading gives 40 marks/)).toBeVisible();
  });
  it('shows the 2014 full-translation exception without allowing two routes for one phrase',async()=>{
    reveal('la1','hl',2014);
    await waitFor(()=>expect(screen.getByRole('button',{name:'русские студенты — Russian form'})).toBeVisible());
    fireEvent.click(screen.getByRole('button',{name:'русские студенты — Russian form'}));
    const russian=screen.getByRole('button',{name:'русские студенты — Russian form'}).closest('section');
    if(!russian)throw new Error('Russian phrase');
    fireEvent.click(within(russian).getByRole('button',{name:'Set Modifier to 1 marks'}));
    expect(screen.getByRole('button',{name:'русские студенты — correct translation'})).toBeDisabled();
    await waitFor(()=>expect(screen.getByText(/placement is 1 of 6 marks/)).toBeVisible());
    fireEvent.click(screen.getByRole('button',{name:'русские студенты — Russian form'}));
    fireEvent.click(screen.getByRole('button',{name:'русские студенты — correct translation'}));
    const translated=screen.getByRole('button',{name:'русские студенты — correct translation'}).closest('section');
    if(!translated)throw new Error('Translated phrase');
    fireEvent.click(within(translated).getByRole('button',{name:'Set Correct translation of the complete phrase to 2 marks'}));
    await waitFor(()=>expect(screen.getByText(/placement is 2 of 6 marks/)).toBeVisible());
    expect(screen.getByText(/Correct translations receive full credit/)).toBeVisible();
    expect(screen.queryByRole('checkbox',{name:/another language/})).not.toBeInTheDocument();
  });
  it('shows the 2014 cultural language allowance and the anomalous concert partial placement',async()=>{
    reveal('ca1','hl',2014);
    await waitFor(()=>expect(screen.getByText(/English, Irish and Russian are permitted/)).toBeVisible());
    cleanup();reveal('l1-3-i','hl',2014);
    await waitFor(()=>expect(screen.getByText(/Source placement: the one-mark concert/)).toBeVisible());
    expect(screen.getByText(/Source placement:/)).toHaveTextContent('before the separate upcoming-event question');
    expect(screen.getByText(/Accept answers written in Russian/)).toBeVisible();
    fireEvent.click(screen.getByRole('button',{name:'Set Distinct detail 1 to 1 marks'}));
    await waitFor(()=>expect(screen.getByText(/placement is 1 of 4 marks/)).toBeVisible());
  });
  it('shows 2014 choice-specific guided-writing categories and both named accuracy scales',async()=>{
    reveal('gw','hl',2014);
    await waitFor(()=>expect(screen.getByText(/When the best time to visit would be/,{selector:'li'})).toBeVisible());
    expect(screen.getByText(/Question and Answer 7/)).toBeVisible();
    expect(screen.getByText(/does not fully match those lists/)).toBeVisible();
    fireEvent.click(screen.getByRole('button',{name:'Set Communication/content (C) to 7 marks'}));
    fireEvent.change(screen.getByRole('spinbutton',{name:/Response length \(words\)/}),{target:{value:'140'}});
    fireEvent.click(screen.getByRole('checkbox',{name:/If the expression is very fluent/}));
    const expression=screen.getByRole('heading',{name:'Language + expression (E)'}).closest('section');
    if(!expression)throw new Error('expression');
    expect(within(expression).getByText('Lower E')).toBeVisible();expect(within(expression).getByText('Lower A')).toBeVisible();
    expect(within(expression).getByText(/Both source scales apply/)).toBeVisible();
    expect(screen.getByRole('button',{name:'Set Language + expression (E) to 7 marks'})).toBeEnabled();
    expect(screen.queryByRole('button',{name:'Set Language + expression (E) to 11 marks'})).not.toBeInTheDocument();
  });
  it('shows fractional 2016 handwriting controls and the global joining condition',async()=>{
    reveal('la1','ol',2016);
    await waitFor(()=>expect(screen.getByRole('button',{name:'Set For everyday life to 2.5 marks'})).toBeVisible());
    fireEvent.click(screen.getByRole('button',{name:'Set For everyday life to 2.5 marks'}));
    fireEvent.click(screen.getByRole('button',{name:'Set Joining letters together to 1 marks'}));
    await waitFor(()=>expect(screen.getByText(/placement is 3.5 of 10 marks/)).toBeVisible());
    fireEvent.click(screen.getByRole('checkbox',{name:/Where candidates omit the loop/}));
    await waitFor(()=>expect(screen.getByText(/placement is 2.5 of 10 marks/)).toBeVisible());
    expect(screen.getByText(/Do not penalise for repeat errors/)).toBeVisible();
  });
  it('resets 2016 dimensions when changing the chosen pool',async()=>{
    const card=REVIEWED_CARDS.find(c=>c.id==='ru-2016-ol-ir2-v');
    if(!card)throw new Error('Missing pool card');
    render(<SessionScreen cards={[card]} subjectLabel="Russian" onGrade={vi.fn()} onFinish={vi.fn()} onExit={vi.fn()} />);
    fireEvent.click(screen.getByRole('button',{name:'Big pool'}));
    fireEvent.click(screen.getByRole('button',{name:'Reveal the marking scheme'}));
    fireEvent.click(screen.getByRole('button',{name:'Award 2 marks for length: 50 m'}));
    await waitFor(()=>expect(screen.getByText(/You claimed 2 of 4 marks/)).toBeVisible());
    fireEvent.click(screen.getByRole('button',{name:'kids’ pool'}));
    expect(screen.getByRole('button',{name:'Award 2 marks for length: 10m'})).toHaveAttribute('aria-pressed','false');
    expect(screen.queryByRole('button',{name:'Award 2 marks for length: 50 m'})).not.toBeInTheDocument();
    expect(screen.getByText(/do not combine dimensions from different pools/)).toBeVisible();
  });
  it('shows the 2016 whole-exercise dialogue limit and already-complete question',async()=>{
    reveal('sd','ol',2016);
    await waitFor(()=>expect(screen.getByText(/Complete all three interviews/)).toBeVisible());
    expect(screen.getByText(/numeric self-scoring is unavailable/)).toHaveTextContent('Question 4 in the first interview is already complete');
    await waitFor(()=>expect(screen.getByText('скольки/ скольких')).toBeVisible());
  });
  it('shows both the 2016 Russian exception and the repeated-information condition',async()=>{
    reveal('cd-2-i','ol',2016);
    await waitFor(()=>expect(screen.getByText(/only if it was not already rewarded in Q1\(i\)/)).toBeVisible());
    expect(screen.getByText(/Marking scheme page 3: Do not penalise answers supplied in Russian/)).toBeVisible();
    cleanup();reveal('l4-4-ii','ol',2016);
    await waitFor(()=>expect(screen.getByText(/only if it was not already rewarded in Q1\(iii\) or Q3\(i\)/)).toBeVisible());
    expect(screen.getByText(/If an answer is written entirely in Russian/)).toHaveTextContent('do not penalise');
  });
  it('applies the actual 2015 employment-reference cap and restores selected answers',async()=>{
    reveal('l3-1','hl',2015);
    await waitFor(()=>expect(screen.getByRole('button',{name:'Answer 4'})).toBeVisible());
    fireEvent.click(screen.getByRole('button',{name:'Answer 4'}));
    fireEvent.click(screen.getByRole('button',{name:'he was invited to the interview · 2m'}));
    fireEvent.click(screen.getByRole('button',{name:'Answer 5'}));
    fireEvent.click(screen.getByRole('button',{name:'he was successful at interview · 2m'}));
    await waitFor(()=>expect(screen.getByText(/placement is 4 of 4 marks/)).toBeVisible());
    const flag=screen.getByRole('checkbox',{name:'No detail refers to work, employment, boxing, a trainer, a position or a post.'});
    fireEvent.click(flag);
    await waitFor(()=>expect(screen.getByText(/placement is 3 of 4 marks/)).toBeVisible());
    expect(screen.getByText('These answers earn up to 3 marks altogether.')).toBeVisible();
    fireEvent.click(flag);
    await waitFor(()=>expect(screen.getByText(/placement is 4 of 4 marks/)).toBeVisible());
  });
  it('shows the 2015 literal Lower A overlap without relabelling the normal grid',async()=>{
    reveal('gw','hl',2015);
    await waitFor(()=>expect(screen.getByRole('button',{name:'Set Communication/content (C) to 15 marks'})).toBeVisible());
    fireEvent.click(screen.getByRole('button',{name:'Set Communication/content (C) to 15 marks'}));
    fireEvent.change(screen.getByRole('spinbutton',{name:/Response length \(words\)/}),{target:{value:'140'}});
    const expression=screen.getByRole('heading',{name:'Language + expression (E)'}).closest('section');
    if(!expression)throw new Error('expression');
    expect(within(expression).getByText(/11–15 marks/)).toBeVisible();
    fireEvent.click(screen.getByRole('checkbox',{name:/If the expression is very fluent/}));
    expect(within(expression).queryByText(/11–15 marks/)).not.toBeInTheDocument();
    expect(within(expression).getByText(/9\s*[-–]\s*11 Vocabulary/)).toBeVisible();
    expect(within(expression).getByText('Lower A')).toBeVisible();
    expect(screen.getByRole('button',{name:'Set Language + expression (E) to 0 marks'})).toHaveAttribute('aria-pressed','true');
    fireEvent.click(screen.getByRole('button',{name:'Set Communication/content (C) to 7 marks'}));
    expect(within(expression).getByText('Lower E')).toBeVisible();
    expect(within(expression).getByText(/Both source scales apply/)).toBeVisible();
    expect(screen.getByRole('button',{name:'Set Language + expression (E) to 7 marks'})).toBeEnabled();
    expect(screen.queryByRole('button',{name:'Set Language + expression (E) to 11 marks'})).not.toBeInTheDocument();
    expect(within(expression).getByText(/9\s*[-–]\s*11 Vocabulary/)).toBeVisible();
  });
  it('shows both 2015 printed job questions under the published joint allocation',async()=>{
    reveal('l3-3','hl',2015);
    await waitFor(()=>expect(screen.getByText(/Both printed questions are practised together/)).toBeVisible());
    expect(screen.getByText(/Give one detail/)).toHaveTextContent('Give three details');
    expect(screen.getByText(/single eight-mark maximum/)).toBeVisible();
  });
  it('keeps each 2015 complete admission explanation as one four-mark claim',async()=>{
    reveal('c1-2-i','hl',2015);
    await waitFor(()=>expect(screen.getByRole('button',{name:'Complete admission explanation'})).toBeVisible());
    fireEvent.click(screen.getByRole('button',{name:'Complete admission explanation'}));
    const claims=screen.getAllByRole('button',{name:/· 4m$/});
    expect(claims).toHaveLength(2);fireEvent.click(claims[0]);
    expect(claims[1]).toBeDisabled();
    await waitFor(()=>expect(screen.getByText(/placement is 4 of 4 marks/)).toBeVisible());
  });
  it('shows the 2016 food partial beside its constrained score control',async()=>{
    reveal('c1-1-ii','hl',2016);
    await waitFor(()=>expect(screen.getByText(/one-mark step on the main-course row/)).toBeVisible());
    fireEvent.click(screen.getByRole('button',{name:'What Pavel eats'}));
    fireEvent.click(screen.getByRole('button',{name:'Claim 1 marks for main course/ second course/ second dish'}));
    await waitFor(()=>expect(screen.getByText(/placement is 1 of 6 marks/)).toBeVisible());
  });
  it('shows Kira’s unresolved source travel span and only full-credit generic slots',async()=>{
    reveal('l1-2','hl',2016);
    await waitFor(()=>expect(screen.getByText(/festival and solo-concert context/)).toBeVisible());
    fireEvent.click(screen.getByRole('button',{name:'Other distinct detail 1'}));
    expect(screen.getByRole('button',{name:'Set Other distinct detail 1 to 2 marks'})).toBeEnabled();
    expect(screen.queryByRole('button',{name:'Set Other distinct detail 1 to 1 marks'})).not.toBeInTheDocument();
  });
  it('keeps the 2016 cross-question partial visibly unassessed',async()=>{
    reveal('l4-2-ii','hl',2016);
    await waitFor(()=>expect(screen.getByText(/leave that cross-question partial unassessed here/)).toBeVisible());
    expect(screen.getByRole('button',{name:'Set First distinct detail to 2 marks'})).toBeVisible();
    expect(screen.queryByRole('button',{name:'Set First distinct detail to 1 marks'})).not.toBeInTheDocument();
    expect(screen.getAllByText(/started doing music/).length).toBeGreaterThan(1);
  });
  it('shows both general and specific 2016 sports routes without duplicate credit',async()=>{
    reveal('l2-2','hl',2016);
    await waitFor(()=>expect(screen.getByRole('button',{name:'Sporting activities'})).toBeVisible());
    fireEvent.click(screen.getByRole('button',{name:'Sporting activities'}));
    expect(screen.getByRole('button',{name:'Named sporting activities'})).toBeDisabled();
  });
  it('uses the 2017 general or specific crowd route without duplicate credit',async()=>{
    reveal('c2-4','hl',2017);
    await waitFor(()=>expect(screen.getByRole('button',{name:'General description'})).toBeVisible());
    fireEvent.click(screen.getByRole('button',{name:'General description'}));
    expect(screen.getByRole('button',{name:'Specific crowd actions'})).toBeDisabled();
    fireEvent.click(screen.getByRole('button',{name:'Claim 2 marks for everyone was joining in'}));
    await waitFor(()=>expect(screen.getByText(/placement is 2 of 10 marks/)).toBeVisible());
    fireEvent.click(screen.getByRole('button',{name:'General description'}));
    fireEvent.click(screen.getByRole('button',{name:'Specific crowd actions'}));
    fireEvent.click(screen.getByRole('button',{name:'Claim 2 marks for dancing'}));
    fireEvent.click(screen.getByRole('button',{name:'Claim 2 marks for shouting'}));
    expect(screen.getByRole('button',{name:'Claim 2 marks for singing along'})).toBeDisabled();
    await waitFor(()=>expect(screen.getByText(/placement is 4 of 10 marks/)).toBeVisible());
  });
  it('shows the 2017 duplicate-entry explanation and only claims that passage word once',async()=>{
    reveal('la2','hl',2017);
    await waitFor(()=>expect(screen.getByText(/one supplied word, послушать/)).toBeVisible());
    fireEvent.click(screen.getByRole('button',{name:'One passage word: accepted forms'}));
    fireEvent.click(screen.getByRole('button',{name:'(по)слушать · 1m'}));
    expect(screen.getByRole('button',{name:'послушать · 1m'})).toBeDisabled();
    await waitFor(()=>expect(screen.getByText(/placement is 1 of 10 marks/)).toBeVisible());
  });
  it('shows both 2017 guided-writing source scales and keeps their shared numeric range',async()=>{
    reveal('gw','hl',2017);
    await waitFor(()=>expect(screen.getByRole('button',{name:'Set Communication/content (C) to 7 marks'})).toBeVisible());
    fireEvent.click(screen.getByRole('button',{name:'Set Communication/content (C) to 7 marks'}));
    fireEvent.change(screen.getByRole('spinbutton',{name:/Response length \(words\)/}),{target:{value:'140'}});
    fireEvent.click(screen.getByRole('checkbox',{name:/If the expression is very fluent/}));
    expect(screen.getByText('Lower A')).toBeVisible();expect(screen.getByText('Lower E')).toBeVisible();
    expect(screen.getByText(/Both source scales apply/)).toBeVisible();
    expect(screen.getByRole('button',{name:'Set Language + expression (E) to 7 marks'})).toBeEnabled();
    expect(screen.queryByRole('button',{name:'Set Language + expression (E) to 6 marks'})).not.toBeInTheDocument();
    expect(screen.queryByRole('button',{name:'Set Language + expression (E) to 11 marks'})).not.toBeInTheDocument();
  });
  it('shows the unresolved 2017 China/Vietnam combination beside the published country/detail scoring',async()=>{
    reveal('l3-3-i','hl',2017);
    await waitFor(()=>expect(screen.getByText(/does not clarify whether both may be used/)).toBeVisible());
    expect(screen.getByRole('button',{name:'Set First country to 1 marks'})).toBeVisible();
    expect(screen.getByRole('button',{name:'Set Detail about the second country to 1 marks'})).toBeVisible();
  });
  it('shows the 2023 hockey-only limit and preserves all listed details',async()=>{
    reveal('l4-3','hl',2023);
    await waitFor(()=>expect(screen.getByText(/Candidates must mention at least two hobbies/)).toBeVisible());
    expect(screen.getByText('Trained in Czech Republic for a year')).toBeVisible();
    expect(screen.getByText('Injured at 16')).toBeVisible();
  });
  it('shows why the 2023 grammar phrase contains two priced forms',async()=>{
    reveal('gr','hl',2023);
    await waitFor(()=>expect(screen.getByText(/The paper has 14 bracketed gaps/)).toBeVisible());
    expect(screen.getByText('Олимпийском')).toBeVisible();
    expect(screen.getByText('музеe')).toBeVisible();
  });
  it('shows the 2010 Russian-only listening condition and keeps fractional full/partial awards',async()=>{
    reveal('l1-1-ii','ol',2010);
    await waitFor(()=>expect(screen.getByText(/Isolated Russian words or expressions do not reduce credit/)).toBeVisible());
    fireEvent.click(screen.getByRole('button',{name:'Answer 1 · Half credit only when the whole answer is in Russian'}));
    fireEvent.click(screen.getByRole('button',{name:'Claim 2.5 marks for President of Russian Federation/Russia'}));
    await waitFor(()=>expect(screen.getByText(/placement is 2.5 of 5 marks/)).toBeVisible());
    fireEvent.click(screen.getByRole('button',{name:'Clear 2.5 marks for President of Russian Federation/Russia'}));
    fireEvent.click(screen.getByRole('button',{name:'Claim 1 marks for President'}));
    await waitFor(()=>expect(screen.getByText(/placement is 1 of 5 marks/)).toBeVisible());
  });
  it('shows the 2010 grammar English exception and original four-times-six writing guidance',async()=>{
    reveal('la1','ol',2010);
    await waitFor(()=>expect(screen.getByText(/Do not penalise students who supply appropriate words in English/)).toBeVisible());
    cleanup();reveal('ew','ol',2010);
    await waitFor(()=>expect(screen.getByText(/The scheme prints 4 x 6 marks for each choice/)).toBeVisible());
    expect(screen.queryByText(/Almost flawless in terms of accuracy/)).not.toBeInTheDocument();
  });
  it('shows the 2011 unresolved festival allocation and the complete accepted answer',async()=>{
    reveal('ir1-i','ol',2011);
    await waitFor(()=>expect(screen.getByText(/Source allocation conflict: the scheme gives 6 marks/)).toBeVisible());
    expect(screen.getByText(/numeric self-scoring is unavailable/)).toHaveTextContent('No one-mark allocation or choose-three rule is inferred');
    expect(screen.getByText("20.00o'clock")).toBeVisible();
    await waitFor(()=>expect(screen.getByText("18.00o'clock")).toBeVisible());
    await waitFor(()=>expect(screen.getByText('27th of August')).toBeVisible());
  });
  it('shows the 2011 date/place wording and all three printed accepted details',async()=>{
    reveal('l4-1','ol',2011);
    await waitFor(()=>expect(screen.getByText(/no separate one-date\/one-place restriction is printed/)).toBeVisible());
    expect(screen.getByText('17th of May')).toBeVisible();
    expect(screen.getByText('1992')).toBeVisible();
    expect(screen.getByText('Moscow')).toBeVisible();
  });
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
