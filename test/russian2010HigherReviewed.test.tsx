import { cleanup, fireEvent, render, screen, waitFor, within } from '@testing-library/react';
import { afterEach, describe, expect, it, vi } from 'vitest';
import LanguageRubricPanel from '../components/MarkBank/LanguageRubricPanel';
import SessionScreen from '../components/MarkBank/SessionScreen';
import { REVIEWED_CARDS } from '../components/MarkBank/cards/russian/reviewed';
import { languageFlagId, languageGroupId, languageLengthId, languageMarks, languageOtherLanguageId, languageRowId, languageScoreId, type LanguageScores } from '../components/MarkBank/languageScoring';
import { isRubricCard, tariffReconciles } from '../types/markBank';
import sources from '../scripts/markbank/authoring/russian-reviewed-sources.json';

const sitting=REVIEWED_CARDS.filter(c=>c.year===2010&&c.level==='higher');
const card=(suffix:string)=>{const c=sitting.find(c=>c.id===`ru-2010-hl-${suffix}`);if(!c)throw new Error(suffix);return c;};
const rubric=(suffix:string)=>{const c=card(suffix);if(!isRubricCard(c))throw new Error(suffix);return c;};
const points=(suffix:string)=>{const c=rubric(suffix);if(c.rubric.system!=='language-points')throw new Error(suffix);return {...c,rubric:c.rubric};};
const writing=(suffix:string)=>{const c=rubric(suffix);if(c.rubric.system!=='language-writing')throw new Error(suffix);return {...c,rubric:c.rubric};};
const row=(group:string,id='full',value=1)=>({[languageGroupId(group)]:1,[languageRowId(group,id)]:value});
afterEach(cleanup);

describe('Russian 2010 Higher original-source tasks',()=>{
  it('represents all 38 original asks while separating 296 scored marks and the derived four-mark unpriced task',()=>{
    expect(sitting).toHaveLength(38);expect(sitting.filter(c=>!tariffReconciles(c)).map(c=>c.id)).toEqual([]);
    expect(sitting.filter(c=>c.id!=='ru-2010-hl-l1-1-i').reduce((s,c)=>s+c.totalMarks,0)).toBe(296);
    expect(sitting.filter(c=>c.audioMaterial)).toHaveLength(18);
    expect(sitting.filter(c=>c.audioMaterial).reduce((s,c)=>s+c.totalMarks,0)).toBe(80);
    expect(sources.filter(s=>s.year===2010&&s.level==='higher')).toHaveLength(38);
  });

  it('keeps all six LA1 prompts and awards the fixed two for blank, saved zero, reset and invalid saved values',()=>{
    const c=writing('la1'),fixed='section2-dative-plural';
    expect(c.sourceMaterial?.pages).toEqual([2,5]);expect(c.rubric.criteria).toHaveLength(6);
    expect(c.rubric.criteria.map(k=>k.permittedMarks)).toEqual([[0,2],[0,2],[0,2],[2],[0,2],[0,2]]);
    expect(c.answerLanguageRule).toBeUndefined();
    expect(c.rubric.taskRequirements.join(' ')).toContain('translated and supplied in English OR');
    for(const scores of [{},...[0,1,2,99,-1].map(value=>({[languageScoreId(fixed)]:value}))])expect(languageMarks(c,scores)).toBe(2);
    const all=Object.fromEntries(c.rubric.criteria.filter(k=>!k.automaticAward).map(k=>[languageScoreId(k.id),2]));
    expect(languageMarks(c,all)).toBe(12);expect(languageMarks(c,{})).toBe(2);
  });

  it('renders the actual universal-award source without a manual claim control',()=>{
    const c=writing('la1');render(<LanguageRubricPanel card={c} scores={{}} onScore={vi.fn()}/>);
    const fixed=c.rubric.criteria.find(k=>k.automaticAward)!;
    const section=screen.getByRole('heading',{name:fixed.label}).closest('section')!;
    expect(within(section).getByText('2 marks awarded to all candidates')).toBeVisible();
    expect(within(section).getAllByText('award 2 marks to all (there is no noun in the dative case)')[0]).toBeVisible();
    expect(within(section).queryByRole('button')).not.toBeInTheDocument();
    expect(screen.queryByRole('checkbox',{name:/another language/})).not.toBeInTheDocument();
  });

  it.each([false,true])('saves the actual source award for blank LA1 in paper layout=%s',async paperLayout=>{
    const c=writing('la1'),onGrade=vi.fn();
    render(<SessionScreen paperLayout={paperLayout} cards={[c]} subjectLabel="Russian" onGrade={onGrade} onFinish={vi.fn()} onExit={vi.fn()}/>);
    fireEvent.click(screen.getByRole('button',{name:'Reveal the marking scheme'}));
    await waitFor(()=>expect(screen.getByText('2 marks awarded to all candidates')).toBeVisible());
    fireEvent.click(screen.getByRole('button',{name:'Got it'}));
    expect(onGrade).toHaveBeenCalledWith(expect.objectContaining({cardId:c.id,marksClaimed:2,marksAvailable:12}));
  });

  it('retains seven cultural slots with the two traditional/two modern requirement and only the named one-mark partial',()=>{
    const c=writing('c1-5');expect(c.rubric.criteria).toHaveLength(7);
    expect(c.questionRef).toBe('2010 HL Section C1 Q5');expect(c.topicId).toBe('russian-2-0');
    expect(c.rubric.taskRequirements.join(' ')).toContain('minimum of two details from each category');
    expect(languageMarks(c,{[languageScoreId('traditional-1')]:1})).toBe(1);
    expect(languageMarks(c,{[languageScoreId('modern-1')]:1})).toBe(0);
    expect(languageMarks(c,Object.fromEntries(c.rubric.criteria.map(k=>[languageScoreId(k.id),2])))).toBe(14);
  });

  it.each([1,2,3,4,5])('retains source-permitted discretion and incomplete cap for summary %s',number=>{
    const c=points(`c2-${number}`),scores:LanguageScores={[languageScoreId('summary-skills')]:2};
    for(const g of c.rubric.groups){scores[languageGroupId(g.id)]=1;for(const r of g.rows)scores[languageRowId(g.id,r.id)]=r.steps?.at(-1)??1;for(const k of g.criteria??[])scores[languageScoreId(k.id)]=k.maxMarks;}
    expect(languageMarks(c,scores)).toBe(8);
    expect(c.answerLanguageRule?.manualCriterionExceptions).toMatchObject({criterionIds:['summary-skills'],schemePages:[7]});
    const wrong={...scores,[languageOtherLanguageId('response')]:1};expect(languageMarks(c,wrong)).toBe(2);
    expect(languageMarks(c,{...wrong,[languageFlagId('incomplete-response')]:1})).toBe(1);
    expect(languageMarks(c,{...wrong,[languageOtherLanguageId('response')]:0})).toBe(8);
    expect(languageMarks(c,{[languageOtherLanguageId('response')]:1})).toBe(0);
  });

  it('keeps all five infinitives, the unscored original example and the open swimming-word rule',()=>{
    const c=points('la2-1');expect(c.questionText).toContain('Sampla/Example: получила получить');
    expect(c.rubric.groups.map(g=>g.label)).toEqual(['имеют','выбрались','поняла','создалось','стали']);
    expect(c.rubric.groups.map(g=>g.rows[0].text)).toEqual(['иметь','выбраться','понять','создаться','стать']);
    expect(languageMarks(c,Object.assign({},...c.rubric.groups.map(g=>row(g.id))))).toBe(5);
    const words=points('la2-2');expect(words.rubric.groups).toHaveLength(5);
    expect(words.rubric.groups.every(g=>g.rows.length===0&&g.criteria?.length===1)).toBe(true);
    expect(words.rubric.taskRequirements.join(' ')).toContain('no indication is given as to where');
    expect(words.rubric.taskRequirements.join(' ')).toContain('(but not sailing/boating)');
  });

  it('retains ten original matching answers and fifteen context-bound grammar forms without capitalization partials',()=>{
    const sd=points('sd');expect(sd.rubric.groups.map(g=>g.rows[0].text)).toEqual(['7','8','3','5','1','4','2','10','9','6']);
    expect(languageMarks(sd,Object.assign({},...sd.rubric.groups.map(g=>row(g.id))))).toBe(20);
    const gr=points('gr');expect(gr.rubric.groups).toHaveLength(15);expect(gr.sourceMaterial?.pages).toEqual([11,12]);
    expect(gr.rubric.groups[0].rows[0].text).toBe('университете');expect(gr.rubric.groups[10].rows[0].text).toBe('университета/университетов');
    expect(gr.rubric.groups.every(g=>g.rows[0].marks===2&&!g.rows[0].steps)).toBe(true);
    expect(gr.rubric.taskRequirements.join(' ')).toContain('Do not award marks if Upper Case or Lower Case are used inappropriately');
    expect(languageMarks(gr,Object.assign({},...gr.rubric.groups.map(g=>row(g.id))))).toBe(30);
  });

  it('retains every writing choice, source Lower A ranges and the title-deduction exception',()=>{
    const se=writing('se');for(const text of ['Как русские школьники проводят летние каникулы','Русский язык в Ирландии'])expect(se.questionText).toContain(text);
    expect(se.questionText).toContain('viii.');
    expect(languageMarks(se,{[languageScoreId('content')]:6,[languageScoreId('title-penalty')]:1,[languageScoreId('expression')]:20,[languageLengthId('words')]:50})).toBe(25);
    const gw=writing('gw'),lower=gw.rubric.criteria.find(k=>k.id==='expression')?.limits?.find(l=>l.id==='lower-a');
    for(const text of ['book a place in a summer school','dream that came true','famous fairy tale','visit a relative','Is English enough?','Should animals be kept','School holidays are too long!'])expect(gw.questionText).toContain(text);
    expect(lower).toMatchObject({minMarks:7,maxMarks:12});expect(lower?.bands).toBeUndefined();expect(lower?.guidance.join(' ')).toContain('9 -11');
    expect(languageMarks(gw,{[languageScoreId('content')]:15,[languageScoreId('expression')]:6,[languageFlagId('lower-a')]:1,[languageLengthId('words')]:140})).toBe(15);
    expect(gw.rubric.markingGuideNote).toContain('both original statements remain visible');
  });

  it('keeps partial/full versions exclusive and the international two-country phrase as one detail',()=>{
    const sofa=points('l1-3');expect(sofa.rubric.groups[1].rows[1].text).toBe('8?? M long');
    expect(languageMarks(sofa,{...row('answer-2'),[languageRowId('answer-2','partial')]:1})).toBe(2);
    expect(languageMarks(sofa,{...row('answer-2'),...row('answer-3','partial')})).toBe(3);
    const event=points('l1-2');expect(event.rubric.groups).toHaveLength(5);expect(event.rubric.groups[3].rows[0].text).toContain('from ANY TWO OF:');
    expect(languageMarks(event,row('answer-4'))).toBe(2);
    const cost=points('l3-3-ii');expect(languageMarks(cost,row('answer-1','partial'))).toBe(1);
    expect(sitting.filter(c=>c.audioMaterial).every(c=>!c.answerLanguageRule)).toBe(true);
  });

  it('saves the missing city task as confidence only while showing the source gap and derived total',async()=>{
    const c=card('l1-1-i');if(isRubricCard(c))throw new Error('Expected unpriced city task');
    expect(c.tariffModel).toEqual({kind:'questionTotal'});expect(c.rows.every(r=>r.marks===null)).toBe(true);
    expect(c.rows[0].contextNote).toContain('not a separately printed task total');
    const onGrade=vi.fn();render(<SessionScreen cards={[c]} subjectLabel="Russian" onGrade={onGrade} onFinish={vi.fn()} onExit={vi.fn()}/>);
    fireEvent.click(screen.getByRole('button',{name:'Reveal the marking scheme'}));
    await waitFor(()=>expect(screen.getByText(/No accepted city-answer pool is printed/)).toBeVisible());
    fireEvent.click(screen.getByRole('button',{name:'Got it'}));
    expect(onGrade).toHaveBeenCalledWith(expect.objectContaining({cardId:c.id,marksClaimed:0,marksAvailable:0}));
  });
});
