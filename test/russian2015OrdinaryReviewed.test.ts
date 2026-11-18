import { describe, expect, it } from 'vitest';
import { REVIEWED_CARDS } from '../components/MarkBank/cards/russian/reviewed';
import { languageMarks, languageScoreId, languageGroupId, languageRowId } from '../components/MarkBank/languageScoring';
import { isRubricCard, tariffReconciles } from '../types/markBank';
import { marksClaimed } from '../components/MarkBank/SessionScreen';

const sitting=REVIEWED_CARDS.filter(c=>c.year===2015&&c.level==='ordinary');
const get=(suffix:string)=>{
  const c=sitting.find(c=>c.id===`ru-2015-ol-${suffix}`);
  if(!c)throw new Error(suffix);
  return c;
};
const points=(suffix:string)=>{
  const c=get(suffix);if(!isRubricCard(c)||c.rubric.system!=='language-points')throw new Error(suffix);
  return {...c,rubric:c.rubric};
};
const selected=(group:string,row='full',value=1)=>({[languageGroupId(group)]:1,[languageRowId(group,row)]:value});

describe('Russian 2015 Ordinary source review',()=>{
  it('covers 54 independently counted tasks and all three priced matching exercises',()=>{
    expect(sitting).toHaveLength(54);
    expect(sitting.filter(c=>!tariffReconciles(c)).map(c=>c.id)).toEqual([]);
    expect(sitting.reduce((sum,c)=>sum+c.totalMarks,0)).toBe(320);
    expect(sitting.filter(c=>c.audioMaterial)).toHaveLength(19);
    expect(sitting.filter(c=>c.audioMaterial).reduce((sum,c)=>sum+c.totalMarks,0)).toBe(100);
    expect(['i','ii','iii'].map(r=>get(`mm-${r}`).totalMarks)).toEqual([12,16,12]);
  });
  it('keeps when and where as separately claimable requirements',()=>{
    const c=points('ir1-vi');
    expect(languageMarks(c,{...selected('where','option-1',2),...selected('where','option-2',2)})).toBe(2);
    expect(languageMarks(c,{...selected('where','option-2',2),...selected('when','option-1',2)})).toBe(4);
    expect(languageMarks(c,{...selected('where','option-2',1),...selected('when','option-1',2)})).toBe(3);
    const d=points('cd-2-i');
    expect(languageMarks(d,{...selected('discussion','option-1',2),...selected('discussion','option-2',2)})).toBe(2);
    expect(languageMarks(d,{...selected('discussion','option-2',2),...selected('where','option-1',2)})).toBe(4);
  });
  it('preserves fractional handwriting and gender/number scoring without per-phrase handwriting prices',()=>{
    const c=get('la1'),d=get('la2');if(isRubricCard(c)||isRubricCard(d))throw new Error('Wrong cards');
    expect(c.rows[0].permittedMarks).toEqual([0,.5,1,1.5,2,2.5,3,3.5,4,4.5,5,5.5,6]);
    expect(c.rows.slice(1).every(r=>r.marks===null)).toBe(true);
    expect(marksClaimed(c,{handwriting:5.5})).toBe(5.5);
    expect(marksClaimed(d,{'phrase-2':.5,'phrase-3':1,'phrase-6':.5})).toBe(2);
    expect(marksClaimed(d,{'phrase-1':.5})).toBe(0);
    expect(d.rows[4].verbatim).toContain('feminine singular / мужской род');
    expect(d.rows[4].contextNote).toContain('labels disagree');
  });
  it('retains source matching differences and the original answer-in-Russian exception',()=>{
    const c=get('mm-ii'),d=get('mm-iii');if(isRubricCard(c)||isRubricCard(d))throw new Error('Wrong cards');
    expect(c.rows[2].verbatim).toContain('Погода ненормальная');
    expect(c.rows[2].contextNote).toContain('Сюрпризы погоды');
    expect(d.rows.map(r=>r.verbatim)).toEqual(['B — на 2 этаж','A — на 3 этаж','B — на 6 этаж']);
    expect(d.rows.every(r=>r.contextNote==='Assign full marks if candidates name the correct floor.')).toBe(true);
    expect(points('ir1-i').rubric.taskRequirements).toContain('Do not penalise answers supplied in Russian.');
    expect(sitting.every(c=>!c.answerLanguageRule)).toBe(true);
  });
  it('scores all ten mandatory discourse gaps at the printed two marks each',()=>{
    const c=points('sd');
    expect(c.rubric.groups).toHaveLength(10);
    expect(languageMarks(c,Object.assign({},...c.rubric.groups.map(g=>selected(g.id))))).toBe(20);
    expect(c.questionText).toContain('Grúpa A / Group A');
    expect(c.questionText).toContain('Grúpa B / Group B');
  });
  it('preserves complete listening pools and original multiple-choice options',()=>{
    const c=points('l4-3');
    expect(c.rubric.groups).toHaveLength(11);
    expect(languageMarks(c,Object.assign({},...c.rubric.groups.map(g=>selected(g.id))))).toBe(10);
    expect(points('l3-4').rubric.groups.map(g=>g.rows[0].text)).toEqual(['Brother','sister','father']);
    expect(get('l1-1').questionText).toContain('d. at a summer camp');
    expect(c.rubric.taskRequirements).toContain('Award FIVE marks for each correct/relevant point.');
  });
  it('scores two cultural essays independently without inheriting a later expression cap',()=>{
    const c=get('sa'),e=get('ew');if(!isRubricCard(c)||!isRubricCard(e))throw new Error('Wrong cards');
    expect(languageMarks(c,{[languageScoreId('first-content')]:12,[languageScoreId('first-coherence')]:3})).toBe(15);
    expect(languageMarks(c,{[languageScoreId('first-content')]:12,[languageScoreId('first-coherence')]:3,[languageScoreId('second-content')]:12,[languageScoreId('second-coherence')]:3})).toBe(30);
    expect(languageMarks(e,{[languageScoreId('content')]:6,[languageScoreId('expression')]:12,[languageScoreId('coherence')]:6})).toBe(24);
  });
});
