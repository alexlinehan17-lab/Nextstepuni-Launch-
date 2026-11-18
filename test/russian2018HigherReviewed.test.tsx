import { cleanup, fireEvent, render, screen, waitFor } from '@testing-library/react';
import { afterEach, describe, expect, it, vi } from 'vitest';
import SessionScreen from '../components/MarkBank/SessionScreen';
import LanguageRubricPanel from '../components/MarkBank/LanguageRubricPanel';
import { REVIEWED_CARDS } from '../components/MarkBank/cards/russian/reviewed';
import { languageMarks, languageScoreId, languageGroupId, languageRowId, languageFlagId, languageLengthId, languageOtherLanguageId } from '../components/MarkBank/languageScoring';
import { isRubricCard, tariffReconciles, UNPRINTED_ANSWER } from '../types/markBank';

const sitting=REVIEWED_CARDS.filter(c=>c.year===2018&&c.level==='higher');
const get=(suffix:string)=>{const c=sitting.find(c=>c.id===`ru-2018-hl-${suffix}`);if(!c)throw new Error(suffix);return c;};
const points=(suffix:string)=>{const c=get(suffix);if(!isRubricCard(c)||c.rubric.system!=='language-points')throw new Error(suffix);return {...c,rubric:c.rubric};};
const writing=()=>{const c=get('gw');if(!isRubricCard(c)||c.rubric.system!=='language-writing')throw new Error('gw');return {...c,rubric:c.rubric};};
const essay=()=>{const c=get('se');if(!isRubricCard(c)||c.rubric.system!=='language-writing')throw new Error('se');return {...c,rubric:c.rubric};};
const slot=(n:number,value:number)=>({[languageGroupId(`detail-${n}`)]:1,[languageScoreId(`detail-${n}-credit`)]:value});
const row=(id:string)=>({[languageGroupId(id)]:1,[languageRowId(id,'full')]:1});
afterEach(cleanup);

describe('Russian 2018 Higher original tasks',()=>{
  it('represents all 39 asks with the printed writing grids available for scoring',()=>{
    expect(sitting).toHaveLength(39);expect(sitting.filter(c=>c.audioMaterial)).toHaveLength(20);
    expect(sitting.reduce((sum,c)=>sum+c.totalMarks,0)).toBe(300);
    expect(sitting.filter(c=>c.id!=='ru-2018-hl-se').reduce((sum,c)=>sum+c.totalMarks,0)).toBe(270);
    expect(sitting.every(tariffReconciles)).toBe(true);
    expect(sitting.filter(c=>c.answerLanguageRule)).toHaveLength(18);
    expect(sitting.filter(c=>c.audioMaterial).every(c=>!c.answerLanguageRule)).toBe(true);
  });
  it('retains named partials manually without inventing associations or broader partial tariffs',()=>{
    const partial=points('c1-3-i'),full=points('c1-3-ii');
    expect(languageMarks(partial,{...slot(1,1),...slot(2,2)})).toBe(3);
    expect(languageMarks(full,slot(1,1))).toBe(0);
    expect(partial.rubric.markingGuideNote).toContain('literal partial wording');
    expect(full.rubric.markingGuideNote).toContain('original source position');
  });
  it('keeps summary discretion available under the explicit Russian-word exception and source caps',()=>{
    const c=points('c2-4'),saved={...slot(1,2),...slot(2,2),...slot(3,2),...slot(4,2),[languageScoreId('summary-skills')]:2};
    expect(languageMarks(c,saved)).toBe(10);
    const wrong={...saved,[languageOtherLanguageId('response')]:1};
    expect(languageMarks(c,wrong)).toBe(2);
    expect(languageMarks(c,{...wrong,[languageFlagId('incomplete-response')]:1})).toBe(1);
    expect(languageMarks(c,{...wrong,[languageFlagId('sequence-not-understood')]:1})).toBe(1);
    expect(languageMarks(c,{...wrong,[languageOtherLanguageId('response')]:0})).toBe(10);
    expect(languageMarks(c,{...slot(1,1),[languageScoreId('summary-skills')]:2})).toBe(2);
    expect(c.answerLanguageRule?.manualCriterionExceptions?.criterionIds).toEqual(['summary-skills']);
  });
  it('renders the discretion exception, original sequence cap and website discrepancy',()=>{
    const c=points('c2-4');render(<LanguageRubricPanel card={c} scores={{}} onScore={vi.fn()}/>);
    expect(screen.getAllByText(/Discretionary marks \(as opposed to content marks\) may be awarded/)[0]).toBeVisible();
    expect(screen.getByRole('checkbox',{name:/Do not give 2 bonus marks/})).toBeVisible();
    expect(screen.getByText(/Source discrepancy: original paper page 8/)).toHaveTextContent('www.scherbackov.ru');
    expect(screen.getByText(/Source discrepancy: original paper page 8/)).toHaveTextContent('www.scherbakov.ru');
    expect(screen.getAllByText(/Answer in English or Irish/)[0]).toBeVisible();
  });
  it('keeps five of nine infinitives and ten of all 29 music entries',()=>{
    const infinitives=points('la1'),music=points('la2');
    expect(infinitives.rubric.groups).toHaveLength(9);expect(infinitives.rubric.count).toBe(5);
    expect(languageMarks(infinitives,Object.assign({},...infinitives.rubric.groups.map(g=>row(g.id))))).toBe(10);
    expect(music.rubric.groups).toHaveLength(29);expect(music.rubric.count).toBe(10);
    expect(music.rubric.groups.map(g=>g.rows[0].text).slice(7,9)).toEqual(['записать','звезда']);
    expect(music.rubric.groups.filter(g=>g.rows[0].text==='петь/спеть (спою)')).toHaveLength(1);
    expect(languageMarks(music,Object.assign({},...music.rubric.groups.map(g=>row(g.id))))).toBe(10);
  });
  it('keeps all ten matching rows and both published slash alternatives',()=>{
    const c=points('sd');expect(c.rubric.groups).toHaveLength(10);
    expect(c.rubric.groups[2].rows[0].text).toMatch(/^1\/ 2 —/);
    expect(c.rubric.groups[5].rows[0].text).toMatch(/^6\/ 10 —/);
    expect(languageMarks(c,Object.assign({},...c.rubric.groups.map(g=>row(g.id))))).toBe(20);
  });
  it('prices fifteen source forms, including two words in one printed grammar prompt',()=>{
    const c=points('gr');expect(c.rubric.groups).toHaveLength(15);
    expect(c.rubric.groups.slice(5,7).map(g=>g.rows[0].text)).toEqual(['школьных','занятий']);
    expect(c.rubric.taskRequirements.join(' ')).toContain('Latin letters are treated as errors');
    expect(languageMarks(c,Object.assign({},...c.rubric.groups.map(g=>row(g.id))))).toBe(30);
  });
  it('applies both writing ranges and the one-or-two soft-sign deduction without minimum awards',()=>{
    const c=writing(),scores={[languageScoreId('content')]:15,[languageScoreId('expression')]:15,[languageScoreId('coherence')]:10,[languageLengthId('words')]:140};
    expect(languageMarks(c,scores)).toBe(40);
    expect(languageMarks(c,{...scores,[languageFlagId('lower-a')]:1})).toBe(37);
    expect(languageMarks(c,{...scores,[languageFlagId('lower-a')]:1,[languageScoreId('expression')]:6})).toBe(25);
    expect(languageMarks(c,{...scores,[languageScoreId('soft-sign-penalty')]:1})).toBe(39);
    expect(languageMarks(c,{...scores,[languageScoreId('soft-sign-penalty')]:2})).toBe(38);
    expect(languageMarks(c,{...scores,[languageScoreId('content')]:7})).toBe(27);
    expect(c.questionText).toContain('military or civilian national service');
    expect(c.rubric.criteria[0].guidance.join(' ')).toContain('at least ONE detail');
  });
  it('keeps the combined listening half-details in one manual two-mark response',()=>{
    const c=points('l4-1-ii');expect(languageMarks(c,slot(1,2))).toBe(2);
    expect(languageMarks(c,{...slot(1,2),...slot(2,2)})).toBe(4);
    expect(languageMarks(c,slot(1,1))).toBe(0);
    expect(c.rubric.taskRequirements.join(' ')).toContain('no marks for museums');
    expect(c.rubric.markingGuideNote).toContain('does not fill both two-mark slots');
  });
  it('retains every essay choice and both conflicting Lower A statements alongside the printed grid',()=>{
    const c=essay();expect(c.answerLanguageRule?.otherLanguageMultiplier).toBe(0);
    expect(c.questionText).toContain('5.');expect(c.questionText).toContain('Cities in the Russian Federation');
    expect(c.rubric.taskRequirements[0]).toContain('between 9 and 14 (9-11; 12-14; 15-16)');
    expect(c.rubric.taskRequirements[1]).toContain('lower A 15-16');
    expect(c.rubric.criteria.flatMap(x=>x.limits??[]).some(x=>x.id==='lower-a')).toBe(false);
    expect(c.rubric.markingGuideNote).toContain(UNPRINTED_ANSWER);
    expect(writing().rubric.markingGuideNote).toContain(UNPRINTED_ANSWER);
  });
  it('scores 10+20, title and explicit soft-sign deductions, and only the unambiguous source limits',()=>{
    const c=essay(),full={[languageScoreId('content')]:10,[languageScoreId('expression')]:20,[languageLengthId('words')]:50};
    expect(languageMarks(c,full)).toBe(30);
    expect(languageMarks(c,{...full,[languageScoreId('title-penalty')]:1})).toBe(29);
    expect(languageMarks(c,{...full,[languageScoreId('soft-sign-penalty')]:1})).toBe(29);
    expect(languageMarks(c,{...full,[languageScoreId('soft-sign-penalty')]:2})).toBe(28);
    expect(languageMarks(c,{...full,[languageLengthId('words')]:24})).toBe(24);
    expect(languageMarks(c,{...full,[languageScoreId('content')]:4})).toBe(18);
    expect(languageMarks(c,{...full,[languageScoreId('content')]:6,[languageScoreId('title-penalty')]:1})).toBe(25);
    expect(languageMarks(c,{...full,[languageScoreId('content')]:0})).toBe(0);
    expect(languageMarks(c,{...full,[languageOtherLanguageId('response')]:1})).toBe(0);
    expect(languageMarks(c,{...full,[languageScoreId('expression')]:16})).toBe(26);
  });
  it.each([false,true])('renders both literal limits and saves the printed essay maximum in paper layout=%s',async paperLayout=>{
    const c=essay(),onGrade=vi.fn();render(<SessionScreen paperLayout={paperLayout} cards={[c]} subjectLabel="Russian" onGrade={onGrade} onFinish={vi.fn()} onExit={vi.fn()}/>);
    fireEvent.click(screen.getByRole('button',{name:'Reveal the marking scheme'}));
    await waitFor(()=>expect(screen.getByText(/The scheme prints no answer for this part\./)).toBeVisible());
    expect(screen.getAllByText(/between 9 and 14 \(9-11; 12-14; 15-16\)/)[0]).toBeVisible();
    await waitFor(()=>expect(screen.getAllByText(/lower A 15-16 lower E 12-14/)[0]).toBeVisible());
    expect(screen.getByText('Communication/content (C)')).toBeVisible();
    expect(screen.getByText('Language/expression (E)')).toBeVisible();
    fireEvent.click(screen.getByRole('button',{name:'Got it'}));
    expect(onGrade).toHaveBeenCalledWith(expect.objectContaining({cardId:c.id,grade:'got',marksClaimed:0,marksAvailable:30}));
  });
});
