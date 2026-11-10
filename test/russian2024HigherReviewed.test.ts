import { describe, expect, it } from 'vitest';
import { REVIEWED_CARDS } from '../components/MarkBank/cards/russian/reviewed';
import { CARDS as HIGHER } from '../components/MarkBank/cards/russian/higher';
import legacy from '../scripts/markbank/authored/russian.json';
import { languageMarks, languageScoreId, languageLengthId, languageFlagId, languageGroupId, languageRowId, languageOtherLanguageId } from '../components/MarkBank/languageScoring';
import { isRubricCard, tariffReconciles } from '../types/markBank';

const sitting = REVIEWED_CARDS.filter(card=>card.year===2024 && card.level==='higher');
const get=(suffix:string)=>{
  const card=sitting.find(card=>card.id===`ru-2024-hl-${suffix}`);
  if(!card || !isRubricCard(card))throw new Error(`Missing rubric ${suffix}`);
  if(card.rubric.system!=='language-writing' && card.rubric.system!=='language-points')throw new Error(`Wrong rubric ${suffix}`);
  return {...card,rubric:card.rubric};
};
const selected=(group:string,row='full',value=1)=>({[languageGroupId(group)]:1,[languageRowId(group,row)]:value});

describe('Russian 2024 Higher original source review',()=>{
  it('covers the independent 48-task census and preserves 20 corrected identities',()=>{
    expect(sitting).toHaveLength(48);
    expect(sitting.every(tariffReconciles)).toBe(true);
    expect(sitting.reduce((sum,c)=>sum+c.totalMarks,0)).toBe(320);
    const audio=sitting.filter(c=>c.audioMaterial);
    expect(audio).toHaveLength(24);
    expect(audio.reduce((sum,c)=>sum+c.totalMarks,0)).toBe(80);
    const old=legacy.filter(c=>c.year===2024 && c.level==='higher');
    expect(old).toHaveLength(20);
    expect(old.every(c=>HIGHER.filter(x=>x.id===c.id).length===1)).toBe(true);
    expect(sitting.filter(c=>c.qa?.gates.includes('reviewed-card-correction'))).toHaveLength(20);
  });
  it('retains all 31 employment terms, the repeated-case restriction and 15-by-2 grammar',()=>{
    const employment=get('la2-i'),grammar=get('gr');
    if(employment.rubric.system!=='language-points'||grammar.rubric.system!=='language-points')throw new Error('Wrong task rubric');
    expect(employment.rubric.groups).toHaveLength(31);
    expect(employment.rubric.count).toBe(5);
    expect(employment.rubric.groups.some(g=>g.rows.some(r=>r.text==='оплата (без оплаты)'))).toBe(true);
    expect(employment.rubric.taskRequirements.join(' ')).toContain('do not award marks for the same word provided in different cases');
    expect(grammar.rubric.groups).toHaveLength(15);
    const scores=Object.assign({},...grammar.rubric.groups.map(g=>selected(g.id)));
    expect(languageMarks(grammar,scores)).toBe(30);
    expect(languageMarks(grammar,{...scores,[languageOtherLanguageId('row:answer-1:full')]:1})).toBe(28);
  });
  it('prices whole summaries with intelligible partials, discretion and source limits',()=>{
    const card=get('c2-2');
    const scores={...selected('answer-1','full',2),...selected('answer-2','full',2),
      ...selected('answer-3','full',2),...selected('answer-4','full',1),[languageScoreId('summary-skills')]:2};
    expect(languageMarks(card,scores)).toBe(9);
    expect(languageMarks(card,{...scores,[languageRowId('answer-4','full')]:2})).toBe(10);
    expect(languageMarks(card,{...scores,[languageFlagId('incomplete-response')]:1})).toBe(8);
    expect(languageMarks(card,{...scores,[languageOtherLanguageId('response')]:1})).toBe(2);
    for(const n of [1,2,3,4])expect(get(`c2-${n}`).totalMarks).toBe(10);
  });
  it('keeps the distinct shed partial under its two-detail quota and retains page continuations',()=>{
    const card=get('c1-3-iii');
    const scores={...selected('answer-1'),...selected('partial-shed','partial')};
    expect(languageMarks(card,scores)).toBe(3);
    expect(languageMarks(card,{...scores,...selected('answer-2')})).toBe(4);
    const change=get('c1-3-ii');
    expect(languageMarks(change,selected('answer-3','partial-1'))).toBe(1);
    expect(languageMarks(change,{...selected('answer-3','partial-1'),...selected('answer-3')})).toBe(2);
    const after=get('c1-3-iv');
    expect(after.rubric.system==='language-points' && after.rubric.groups).toHaveLength(9);
    expect(after.rubric.system==='language-points' && after.rubric.groups.at(-1)?.rows[0].text).toBe('the cat behaved as if it was the owner / master and the watchman / guard');
  });
  it('keeps day-plus-time bullets intact and uses the printed listening quota',()=>{
    const card=get('l1-2-ii');
    if(card.rubric.system!=='language-points')throw new Error('Wrong listening rubric');
    expect(card.rubric.count).toBe(2);
    expect(card.rubric.groups.map(g=>g.rows)).toEqual([
      [{id:'full',text:'on weekdays + after 6 pm',marks:2}],
      [{id:'full',text:'on Saturday + before lunch',marks:2}],
    ]);
    expect(languageMarks(card,selected('answer-1'))).toBe(2);
    expect(languageMarks(card,{...selected('answer-1'),...selected('answer-2')})).toBe(4);
    expect(card.rubric.taskRequirements.join(' ')).toContain('incorrect contradictory answer nullifies the correct answer');
    expect(card.rubric.taskRequirements.join(' ')).toContain('no penalty for excess material which does not invalidate the answer');
  });
  it('uses the 2024 writing grids without the later one-topic cap',()=>{
    const essay=get('se'),writing=get('gw');
    expect(essay.questionText.split('\n').filter(l=>l.startsWith('• '))).toHaveLength(5);
    expect(essay.questionText).toContain('Растительный и животный мир');
    expect(writing.questionText).toContain('having a pet animal');
    expect(writing.questionText).toContain('replicate word  for word');
    expect(essay.rubric.system==='language-writing' && essay.rubric.criteria.find(c=>c.id==='content')?.limits).toBeUndefined();
    const scores={ [languageScoreId('content')]:6,[languageScoreId('title-penalty')]:1,
      [languageScoreId('expression')]:20,[languageLengthId('words')]:50 };
    expect(languageMarks(essay,scores)).toBe(25);
    expect(languageMarks(essay,{...scores,[languageScoreId('content')]:4})).toBe(17);
    expect(languageMarks(essay,{...scores,[languageLengthId('words')]:24})).toBe(19);
    expect(languageMarks(essay,{...scores,[languageScoreId('content')]:0})).toBe(0);
    const guided={ [languageScoreId('content')]:15,[languageScoreId('expression')]:15,
      [languageScoreId('coherence')]:10,[languageLengthId('words')]:140 };
    expect(languageMarks(writing,guided)).toBe(40);
    expect(languageMarks(writing,{...guided,[languageLengthId('words')]:59})).toBe(35);
    expect(languageMarks(writing,{...guided,[languageScoreId('content')]:7})).toBe(27);
  });
  it('applies the verified language rule to 21 mandated written tasks only',()=>{
    expect(sitting.filter(c=>c.answerLanguageRule)).toHaveLength(21);
    for(const suffix of ['la1-ii','la2-ii','sd'])expect(get(suffix).answerLanguageRule).toBeUndefined();
    expect(get('la2-ii').questionText).toContain('Irish, English or Russian');
    expect(get('c1-1-i').rubric.markingGuideNote).toContain('English or Irish');
    expect(sitting.filter(c=>c.audioMaterial).every(c=>!c.answerLanguageRule)).toBe(true);
  });
});
