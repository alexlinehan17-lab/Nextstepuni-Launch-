import { cleanup, fireEvent, render, screen, waitFor } from '@testing-library/react';
import { afterEach, describe, expect, it, vi } from 'vitest';
import SessionScreen from '../components/MarkBank/SessionScreen';
import LanguageRubricPanel from '../components/MarkBank/LanguageRubricPanel';
import { REVIEWED_CARDS } from '../components/MarkBank/cards/russian/reviewed';
import { languageMarks, languageScoreId, languageGroupId, languageRowId, languageFlagId, languageLengthId, languageOtherLanguageId } from '../components/MarkBank/languageScoring';
import { isRubricCard, tariffReconciles } from '../types/markBank';

const sitting=REVIEWED_CARDS.filter(c=>c.year===2020&&c.level==='higher');
const get=(suffix:string)=>{const card=sitting.find(c=>c.id===`ru-2020-hl-${suffix}`);if(!card)throw new Error(suffix);return card;};
const points=(suffix:string)=>{const card=get(suffix);if(!isRubricCard(card)||card.rubric.system!=='language-points')throw new Error(suffix);return {...card,rubric:card.rubric};};
const writing=()=>{const card=get('gw');if(!isRubricCard(card)||card.rubric.system!=='language-writing')throw new Error('gw');return {...card,rubric:card.rubric};};
const essay=()=>{const card=get('se');if(!isRubricCard(card)||card.rubric.system!=='language-writing')throw new Error('se');return {...card,rubric:card.rubric};};
const slot=(n:number,value:number)=>({[languageGroupId(`detail-${n}`)]:1,[languageScoreId(`detail-${n}-credit`)]:value});
const row=(id:string)=>({[languageGroupId(id)]:1,[languageRowId(id,'full')]:1});
afterEach(cleanup);

describe('Russian 2020 Higher approved individual questions and source marks',()=>{
  it('represents all 42 printed asks individually with approved marks',()=>{
    expect(sitting).toHaveLength(42);expect(sitting.filter(c=>c.audioMaterial)).toHaveLength(22);
    expect(sitting.every(tariffReconciles)).toBe(true);
    expect(sitting.filter(isRubricCard).reduce((sum,c)=>sum+c.totalMarks,0)).toBe(300);
    expect(sitting.filter(c=>!isRubricCard(c)).reduce((sum,c)=>sum+c.totalMarks,0)).toBe(0);
    expect(sitting.filter(c=>c.answerLanguageRule)).toHaveLength(18);
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
  it('gives one mark per luggage item and keeps each bare pet partial inside its full answer',()=>{
    const luggage=points('l1-2');expect(languageMarks(luggage,row('answer-1'))).toBe(1);expect(languageMarks(luggage,{...row('answer-1'),...row('answer-2')})).toBe(2);
    const pets=points('l4-3-ii');
    for(const g of pets.rubric.groups) {
      const partial={[languageGroupId(g.id)]:1,[languageRowId(g.id,'partial-1')]:1};
      expect(languageMarks(pets,partial)).toBe(1);expect(languageMarks(pets,{...partial,[languageRowId(g.id,'full')]:1})).toBe(2);
    }
    expect(languageMarks(pets,{...row('answer-1'),...row('answer-2')})).toBe(2);
  });
  it('applies the approved essay deduction without changing the original notation or lower scales',()=>{
    const card=essay(),full={[languageScoreId('content')]:10,[languageScoreId('expression')]:20,[languageLengthId('words')]:50};
    expect(languageMarks(card,full)).toBe(30);
    expect(languageMarks(card,{...full,[languageScoreId('soft-sign-penalty')]:1})).toBe(29);
    expect(languageMarks(card,{...full,[languageScoreId('soft-sign-penalty')]:2})).toBe(28);
    expect(languageMarks(card,{...full,[languageFlagId('lower-a')]:1})).toBe(24);
    expect(languageMarks(card,{...full,[languageScoreId('content')]:4})).toBe(18);
    expect(languageMarks(card,{...full,[languageScoreId('content')]:0})).toBe(0);
    expect(languageMarks(card,{...full,[languageLengthId('words')]:24})).toBe(24);
    expect(card.rubric.criteria.at(-1)?.guidance[0]).toContain('Deduct 1/2 marks');
  });
  it.each([false,true])('saves the luggage answer with its two available marks, paper layout=%s',async paperLayout=>{
    const card=points('l1-2'),onGrade=vi.fn();render(<SessionScreen paperLayout={paperLayout} cards={[card]} subjectLabel="Russian" onGrade={onGrade} onFinish={vi.fn()} onExit={vi.fn()}/>);
    fireEvent.click(screen.getByRole('button',{name:'Reveal the marking scheme'}));
    await waitFor(()=>expect(screen.getByText(/The scheme gives one mark for a suitcase/)).toBeVisible());
    fireEvent.click(screen.getByRole('button',{name:'Answer 1'}));fireEvent.click(screen.getByRole('button',{name:/One suitcase.*1m/}));
    fireEvent.click(screen.getByRole('button',{name:'Answer 2'}));fireEvent.click(screen.getByRole('button',{name:/a bag\/purse.*1m/}));
    fireEvent.click(screen.getByRole('button',{name:'Got it'}));
    expect(onGrade).toHaveBeenCalledWith(expect.objectContaining({cardId:card.id,grade:'got',marksClaimed:2,marksAvailable:2}));
  });
});
