import { cleanup, fireEvent, render, screen, waitFor } from '@testing-library/react';
import { afterEach, describe, expect, it, vi } from 'vitest';
import SessionScreen, { marksClaimed, showsRowMarks } from '../components/MarkBank/SessionScreen';
import LanguageRubricPanel from '../components/MarkBank/LanguageRubricPanel';
import { REVIEWED_CARDS } from '../components/MarkBank/cards/russian/reviewed';
import { languageMarks, languageScoreId, languageGroupId, languageRowId, languageFlagId, languageLengthId, languageOtherLanguageId } from '../components/MarkBank/languageScoring';
import { isRubricCard, tariffReconciles } from '../types/markBank';

const sitting=REVIEWED_CARDS.filter(c=>c.year===2020&&c.level==='higher');
const get=(suffix:string)=>{const card=sitting.find(c=>c.id===`ru-2020-hl-${suffix}`);if(!card)throw new Error(suffix);return card;};
const points=(suffix:string)=>{const card=get(suffix);if(!isRubricCard(card)||card.rubric.system!=='language-points')throw new Error(suffix);return {...card,rubric:card.rubric};};
const writing=()=>{const card=get('gw');if(!isRubricCard(card)||card.rubric.system!=='language-writing')throw new Error('gw');return {...card,rubric:card.rubric};};
const confidence=(suffix:string)=>{const card=get(suffix);if(isRubricCard(card))throw new Error(suffix);return card;};
const slot=(n:number,value:number)=>({[languageGroupId(`detail-${n}`)]:1,[languageScoreId(`detail-${n}-credit`)]:value});
const row=(id:string)=>({[languageGroupId(id)]:1,[languageRowId(id,'full')]:1});
afterEach(cleanup);

describe('Russian 2020 Higher original questions and explicit holds',()=>{
  it('represents 42 asks in 24 tasks, keeping the five complete confidence tasks unpriced',()=>{
    expect(sitting).toHaveLength(24);expect(sitting.filter(c=>c.audioMaterial)).toHaveLength(4);
    expect(sitting.every(tariffReconciles)).toBe(true);
    expect(sitting.filter(isRubricCard).reduce((sum,c)=>sum+c.totalMarks,0)).toBe(190);
    expect(sitting.filter(c=>!isRubricCard(c)).reduce((sum,c)=>sum+c.totalMarks,0)).toBe(110);
    expect(sitting.filter(c=>c.answerLanguageRule)).toHaveLength(17);
  });
  it('keeps source detail quotas without inventing partial credit in comprehension',()=>{
    for(const suffix of ['c1-1-i','c1-1-ii','c1-2-i','c1-2-ii','c1-2-iii','c1-3-i','c1-3-ii','c1-4-i','c1-4-ii']) {
      const card=points(suffix);
      expect(languageMarks(card,Object.assign({},...card.rubric.groups.map(g=>row(g.id))))).toBe(card.totalMarks);
      expect(card.rubric.groups.every(g=>g.rows[0].marks===2&&!g.rows[0].steps)).toBe(true);
      expect(card.rubric.taskRequirements.join(' ')).toContain('accept the one which gives the candidate the most marks');
    }
  });
  it('keeps the printed intelligible partial and manual discretion exception with the incomplete cap',()=>{
    const card=points('c2-1'),saved={...slot(1,1),...slot(2,2),...slot(3,2),...slot(4,2),[languageScoreId('summary-skills')]:2};
    expect(languageMarks(card,saved)).toBe(9);
    expect(languageMarks(card,{...saved,[languageFlagId('incomplete-response')]:1})).toBe(8);
    const other={...saved,[languageOtherLanguageId('response')]:1};
    expect(languageMarks(card,other)).toBe(2);
    expect(languageMarks(card,{...other,[languageFlagId('incomplete-response')]:1})).toBe(1);
    expect(languageMarks(card,{...other,[languageOtherLanguageId('response')]:0})).toBe(9);
    render(<LanguageRubricPanel card={card} scores={saved} onScore={vi.fn()}/>);
    expect(screen.getAllByText(/Single marks may be awarded for partial details/)[0]).toBeVisible();
    expect(screen.getAllByText(/A modicum of/)[0]).toBeVisible();
    expect(screen.getAllByText(/Discretionary marks \(as opposed to content marks\) may be awarded/)[0]).toBeVisible();
  });
  it('retains all ten case prompts and their explicit language permission',()=>{
    const card=points('la2');expect(card.rubric.groups).toHaveLength(10);
    expect(card.answerLanguageRule).toBeUndefined();
    expect(languageMarks(card,Object.assign({},...card.rubric.groups.map(g=>row(g.id))))).toBe(10);
    expect(card.rubric.taskRequirements.join(' ')).toContain('Irish, English or Russian');
    expect(card.rubric.taskRequirements.join(' ')).toContain('translate the phrases into English');
    expect(card.rubric.groups.filter(g=>g.rows[0].text.includes('предожный'))).toHaveLength(2);
  });
  it('keeps the original aspect and all eighteen travel entries under the five-answer quota',()=>{
    const verbs=points('la1-1'),travel=points('la1-2');
    expect(verbs.rubric.groups).toHaveLength(5);
    expect(verbs.rubric.groups.map(g=>g.rows[0].text)).toEqual(['планируют — планировать','надели — надеть','наслаждались — наслаждаться','отправились — отправиться','иди — идти']);
    expect(languageMarks(verbs,Object.assign({},...verbs.rubric.groups.map(g=>row(g.id))))).toBe(5);
    expect(verbs.rubric.taskRequirements.join(' ')).toContain('Do not change the aspect');
    expect(travel.rubric.groups).toHaveLength(18);expect(travel.rubric.count).toBe(5);
    expect(languageMarks(travel,Object.assign({},...travel.rubric.groups.map(g=>row(g.id))))).toBe(5);
    expect(travel.rubric.markingGuideNote).toContain('Q.1.3');expect(travel.rubric.markingGuideNote).toContain('Q.2.2');
  });
  it('preserves the ten original matches and separately priced fifteen grammar forms',()=>{
    const matching=points('sd');expect(matching.rubric.groups).toHaveLength(10);
    expect(matching.rubric.groups.map(g=>g.rows[0].text.split(' — ')[0])).toEqual(['8','3','5','7','9','6','4','1','2','10']);
    expect(languageMarks(matching,Object.assign({},...matching.rubric.groups.map(g=>row(g.id))))).toBe(20);
    const grammar=points('gr');expect(grammar.rubric.groups).toHaveLength(15);
    expect(grammar.rubric.groups.map(g=>g.rows[0].text)).toEqual(['Мою','бабушку','многодетной','семье','лыжах','среднюю','Моего','дедушку','восьми','главным','помощником','дому','зимой /зимою','природе','края']);
    expect(languageMarks(grammar,Object.assign({},...grammar.rubric.groups.map(g=>row(g.id))))).toBe(30);
  });
  it('uses the consistent guided-writing range without assigning the overlapping descriptors or a minimum',()=>{
    const card=writing(),scores={[languageScoreId('content')]:15,[languageScoreId('expression')]:15,[languageScoreId('coherence')]:10,[languageLengthId('words')]:140};
    expect(languageMarks(card,scores)).toBe(40);
    expect(languageMarks(card,{...scores,[languageFlagId('lower-a')]:1})).toBe(37);
    expect(languageMarks(card,{...scores,[languageFlagId('lower-a')]:1,[languageScoreId('expression')]:6})).toBe(25);
    expect(languageMarks(card,{...scores,[languageScoreId('soft-sign-penalty')]:2})).toBe(38);
    expect(languageMarks(card,{...scores,[languageScoreId('soft-sign-penalty')]:1})).toBe(40);
    expect(languageMarks(card,{...scores,[languageScoreId('content')]:7})).toBe(27);
    render(<LanguageRubricPanel card={card} scores={{...scores,[languageFlagId('lower-a')]:1}} onScore={vi.fn()}/>);
    expect(screen.getAllByText(/Lower A Expression 11-12/)[0]).toBeVisible();
    expect(screen.getAllByText(/Lower A Expression 11-12/)[0]).toHaveTextContent('9-11');
    expect(card.rubric.criteria[1].limits?.find(l=>l.id==='lower-a')?.bands).toBeUndefined();
  });
  it('keeps all five unresolved tasks entirely unpriced while retaining known source allocations',()=>{
    for(const suffix of ['se','l1','l2','l3','l4']) {
      const card=confidence(suffix);expect(card.tariffModel).toEqual({kind:'questionTotal'});
      expect(card.rows.every(r=>r.marks===null)).toBe(true);expect(card.answerLanguageRule).toBeUndefined();
      expect(showsRowMarks(card)).toBe(false);
      expect(marksClaimed(card,Object.fromEntries(card.rows.map(r=>[r.id,'yes'])),{})).toBe(0);
    }
    expect(confidence('se').rows.map(r=>r.verbatim).join(' ')).toContain('Deduct 1/2 marks');
    expect(confidence('l1').rows.find(r=>r.id==='l1-2')?.verbatim).toBe('• One suitcase (1 mark) and a bag/purse (1 mark)');
    expect(sitting.some(c=>c.id==='ru-2020-hl-l1-2')).toBe(false);
    expect(confidence('l4').rows.map(r=>r.verbatim).join(' ')).toContain('Dog: 1 mark');
    expect(confidence('l4').rows.map(r=>r.verbatim).join(' ')).toContain('Cat: 1 mark');
    expect(confidence('l1').rows[0].contextNote).toContain('18-mark remainder');
    expect(confidence('l2').rows[0].contextNote).toContain('50 minutes');
    expect(confidence('l2').rows[0].contextNote).toContain('40 minutes');
  });
  it.each(['se','l1','l2','l3','l4'].flatMap(suffix=>[false,true].map(paperLayout=>({suffix,paperLayout}))))('saves $suffix confidence0/0 in paper layout=$paperLayout',async({suffix,paperLayout})=>{
    const card=confidence(suffix),onGrade=vi.fn();render(<SessionScreen paperLayout={paperLayout} cards={[card]} subjectLabel="Russian" onGrade={onGrade} onFinish={vi.fn()} onExit={vi.fn()}/>);
    fireEvent.click(screen.getByRole('button',{name:'Reveal the marking scheme'}));
    await waitFor(()=>expect(screen.getByText(suffix==='se'?/Neither interpretation is selected/:/The scheme does not provide complete full-answer allocations/)).toBeVisible());
    expect(screen.queryByRole('button',{name:/^Claim \d+ marks/})).not.toBeInTheDocument();
    fireEvent.click(screen.getByRole('button',{name:'Got it'}));
    expect(onGrade).toHaveBeenCalledWith(expect.objectContaining({cardId:card.id,grade:'got',marksClaimed:0,marksAvailable:0}));
  });
});
// Current-root confidence header and numeric-quiz exclusion require root integration QA.
