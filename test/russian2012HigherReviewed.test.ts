import { describe, expect, it } from 'vitest';
import { REVIEWED_CARDS } from '../components/MarkBank/cards/russian/reviewed';
import { languageMarks, languageScoreId, languageLengthId, languageFlagId, languageGroupId, languageRowId } from '../components/MarkBank/languageScoring';
import { isRubricCard, tariffReconciles } from '../types/markBank';
const sitting=REVIEWED_CARDS.filter(c=>c.year===2012&&c.level==='higher');
const get=(suffix:string)=>{const c=sitting.find(c=>c.id===`ru-2012-hl-${suffix}`);if(!c||!isRubricCard(c))throw new Error(suffix);return c;};
const points=(suffix:string)=>{const c=get(suffix);if(c.rubric.system!=='language-points')throw new Error(suffix);return {...c,rubric:c.rubric};};
const writing=(suffix:string)=>{const c=get(suffix);if(c.rubric.system!=='language-writing')throw new Error(suffix);return {...c,rubric:c.rubric};};
const row=(group:string,id='full',value=1)=>({[languageGroupId(group)]:1,[languageRowId(group,id)]:value});
const slot=(id:string,value:number)=>({[languageGroupId(id)]:1,[languageScoreId(id)]:value});

describe('Russian 2012 Higher supported source tasks',()=>{
  it('keeps the arithmetic-conflict task open and publishes all thirty-nine supported tasks',()=>{
    expect(sitting).toHaveLength(39);expect(sitting.some(c=>c.id==='ru-2012-hl-c1-2-ii')).toBe(false);
    expect(sitting.filter(c=>!tariffReconciles(c)).map(c=>c.id)).toEqual([]);
    expect(sitting.reduce((s,c)=>s+c.totalMarks,0)).toBe(296);
    expect(sitting.filter(c=>c.audioMaterial)).toHaveLength(20);
    expect(sitting.filter(c=>c.audioMaterial).reduce((s,c)=>s+c.totalMarks,0)).toBe(80);
  });
  it('uses the source prohibition as a derived ceiling without a fixed deduction or automatic award',()=>{
    const c=points('c1-1-ii'),all={...slot('detail-1',2),...slot('detail-2',2),...slot('detail-3',2)};
    expect(languageMarks(c,all)).toBe(6);expect(languageMarks(c,{...all,[languageFlagId('missing-both-girls')]:1})).toBe(5);
    expect(languageMarks(c,{...slot('detail-1',2),...slot('detail-2',2),[languageFlagId('missing-both-girls')]:1})).toBe(4);
    expect(languageMarks(c,{[languageFlagId('missing-both-girls')]:1})).toBe(0);
    expect(c.rubric.markingGuideNote).toContain('not a printed award or a fixed one-mark deduction');
  });
  it('keeps both literal furniture rules in manual full and partial assessment',()=>{
    const c=points('c1-1-i'),guide=c.rubric.taskRequirements.join(' ');
    expect(guide).toContain('(other) furniture');expect(guide).toContain('furniture');
    expect(languageMarks(c,slot('detail-1',1))).toBe(1);expect(languageMarks(c,slot('detail-1',2))).toBe(2);
  });
  it('preserves both complete summary routes and the scoped discretionary cap',()=>{
    const c=points('c2-3');
    const standard={ [languageGroupId('standard')]:1, ...Object.fromEntries([1,2,3,4].map(n=>[languageScoreId(`standard-detail-${n}`),2])),[languageScoreId('standard-discretion')]:2 };
    expect(languageMarks(c,standard)).toBe(10);expect(languageMarks(c,{...standard,[languageFlagId('standard-incomplete')]:1})).toBe(9);
    const five={...standard,[languageGroupId('standard')]:0,[languageGroupId('five-details')]:1,...Object.fromEntries([1,2,3,4,5].map(n=>[languageScoreId(`five-details-detail-${n}`),2])),[languageFlagId('standard-incomplete')]:1};
    expect(languageMarks(c,five)).toBe(10);expect(languageMarks(c,{...five,[languageGroupId('standard')]:1})).toBe(0);
    expect(c.answerLanguageRule).toBeUndefined();expect(c.rubric.markingGuideNote).toContain('BOTH the exhibits and their importance');
  });
  it('keeps only the source instrumental partial and no invented case examples',()=>{
    const c=writing('la1');expect(c.rubric.criteria.map(x=>x.permittedMarks)).toEqual([[0,2],[0,2],[0,1,2]]);
    expect(languageMarks(c,{[languageScoreId('instrumental')]:1})).toBe(1);
    expect(languageMarks(c,{[languageScoreId('accusative')]:1})).toBe(0);
    expect(c.rubric.taskRequirements.join(' ')).toContain('одним');
  });
  it('keeps the cultural two-topic quota and literal unnamed language exception',()=>{
    const c=points('ca1');expect(c.rubric.count).toBe(2);expect(c.rubric.groups.map(g=>g.label)).toEqual(['электричка','дача','Арбат','метро']);
    expect(c.answerLanguageRule).toBeUndefined();expect(c.rubric.taskRequirements.join(' ')).toContain('both/either language');
    const all=Object.assign({},...c.rubric.groups.map(g=>({[languageGroupId(g.id)]:1,...Object.fromEntries(g.criteria!.map(k=>[languageScoreId(k.id),1]))})));
    expect(languageMarks(c,all)).toBe(4);
  });
  it('retains all exact infinitives and all accepted matching numbers without unique-use restrictions',()=>{
    expect(points('la2-2').rubric.groups.map(g=>g.rows[0].text)).toEqual(['хотеть','найти','лежать','казаться','стоять']);
    const c=points('sd');expect(c.rubric.groups.map(g=>g.rows.map(r=>r.text))).toEqual([['4','6','9'],['8'],['4','6','9'],['7'],['10'],['5'],['4','6','9'],['2'],['1'],['3']]);
    expect(languageMarks(c,{...row('answer-1','option-1'),...row('answer-3','option-1'),...row('answer-7','option-1')})).toBe(6);
  });
  it('keeps fifteen original grammar gaps and all three congratulation alternatives without a new partial tariff',()=>{
    const c=points('gr');expect(c.rubric.groups).toHaveLength(15);
    expect(c.rubric.groups[1].rows[0].text).toBe('поздравил/ поздравлял / поздравляет');
    expect(c.rubric.groups[3].rows[0].text).toBe('университетом');expect(c.rubric.groups[10].rows[0].text).toBe('университет');
    expect(c.rubric.groups.every(g=>g.rows.every(r=>r.marks===2&&!r.steps))).toBe(true);
    expect(languageMarks(c,Object.assign({},...c.rubric.groups.map(g=>row(g.id))))).toBe(30);
  });
  it('preserves all six essay choices and the title exception to Lower E',()=>{
    const c=writing('se');expect(c.questionText).toContain('6.');expect(c.questionText).toContain('Жильё в РФ');
    const score={[languageScoreId('content')]:6,[languageScoreId('title-penalty')]:1,[languageScoreId('expression')]:20,[languageLengthId('words')]:50};
    expect(languageMarks(c,score)).toBe(25);expect(c.rubric.criteria.find(x=>x.id==='soft-sign-penalty')?.permittedMarks).toEqual([0,1,2]);
  });
  it('preserves the holiday prompt discrepancy and literal overlapping Lower A descriptors',()=>{
    const c=writing('gw'),lower=c.rubric.criteria.find(x=>x.id==='expression')?.limits?.find(x=>x.id==='lower-a');
    expect(c.questionText).toContain('What you are doing');expect(c.rubric.taskRequirements.join(' ')).toContain('What you did');
    expect(lower).toMatchObject({minMarks:7,maxMarks:12});expect(lower?.bands).toBeUndefined();expect(lower?.guidance.join(' ')).toContain('9 -11');
    const s={[languageScoreId('content')]:15,[languageScoreId('expression')]:6,[languageFlagId('lower-a')]:1,[languageLengthId('words')]:140};
    expect(languageMarks(c,s)).toBe(15);expect(languageMarks(c,{...s,[languageScoreId('expression')]:11})).toBe(26);
  });
  it('permits source compensation only against another exactly-one category and keeps six overall',()=>{
    const c=points('l2-4'),scores=(venue:number,time:number,price:number)=>({...row('venue','response',venue),...row('time','response',time),...row('price','response',price)});
    expect(languageMarks(c,scores(2,2,2))).toBe(6);expect(languageMarks(c,scores(3,1,2))).toBe(6);
    expect(languageMarks(c,scores(3,1,0))).toBe(4);expect(languageMarks(c,scores(3,2,0))).toBe(4);
    expect(languageMarks(c,scores(3,3,3))).toBe(6);expect(languageMarks(c,scores(3,1,3))).toBe(5);
    expect(languageMarks(c,scores(0,0,0))).toBe(0);
    expect(c.rubric.allocationCap?.categoryCompensation).toEqual({normalMarks:2,reducedMarks:1,increasedMarks:3});
  });
  it('keeps bracketed two-component responses and named partials under the three-response career quota',()=>{
    const c=points('l2-2');expect(c.rubric.groups).toHaveLength(3);
    expect(c.rubric.taskRequirements.join(' ')).toContain('[2 details of:');expect(c.rubric.taskRequirements.join(' ')).toContain('[full marks for any two of:');
    expect(c.rubric.taskRequirements.join(' ')).toContain('No marks: Pauline is 27 years old');
    expect(languageMarks(c,{...slot('detail-1',2),...slot('detail-2',1),...slot('detail-3',2)})).toBe(5);
    expect(c.rubric.markingGuideNote).toContain('One mark is available only for a named source partial');
  });
  it('scopes language penalties to thirteen written tasks and exempts all summaries and listening',()=>{
    expect(sitting.filter(c=>c.answerLanguageRule)).toHaveLength(13);
    expect(sitting.filter(c=>c.audioMaterial||c.section==='C2').every(c=>!c.answerLanguageRule)).toBe(true);
    expect(get('c1-1-i').answerLanguageRule?.sourceText).not.toContain('red pen');
  });
});
