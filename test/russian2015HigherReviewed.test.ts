import { describe, expect, it } from 'vitest';
import { REVIEWED_CARDS } from '../components/MarkBank/cards/russian/reviewed';
import { languageMarks, languageScoreId, languageLengthId, languageFlagId, languageGroupId, languageRowId, languageOtherLanguageId } from '../components/MarkBank/languageScoring';
import { isRubricCard, tariffReconciles } from '../types/markBank';
const sitting=REVIEWED_CARDS.filter(c=>c.year===2015&&c.level==='higher');
const get=(suffix:string)=>{const c=sitting.find(c=>c.id===`ru-2015-hl-${suffix}`);if(!c||!isRubricCard(c))throw new Error(suffix);return c;};
const points=(suffix:string)=>{const c=get(suffix);if(c.rubric.system!=='language-points')throw new Error(suffix);return {...c,rubric:c.rubric};};
const writing=(suffix:string)=>{const c=get(suffix);if(c.rubric.system!=='language-writing')throw new Error(suffix);return {...c,rubric:c.rubric};};
const row=(group:string,id='full',value=1)=>({[languageGroupId(group)]:1,[languageRowId(group,id)]:value});

describe('Russian 2015 Higher published allocations',()=>{
  it('preserves 43 priced tasks, all 44 printed asks and the original 300 marks',()=>{
    expect(sitting).toHaveLength(43);expect(sitting.filter(c=>!tariffReconciles(c)).map(c=>c.id)).toEqual([]);
    expect(sitting.reduce((sum,c)=>sum+c.totalMarks,0)).toBe(300);
    expect(sitting.filter(c=>c.audioMaterial)).toHaveLength(19);
    expect(sitting.filter(c=>c.audioMaterial).reduce((sum,c)=>sum+c.totalMarks,0)).toBe(80);
  });
  it('preserves the complete four-mark admission explanations inside the question maximum',()=>{
    const c=points('c1-2-i');
    expect(c.rubric.groups.find(g=>g.id==='admission-explanation')?.rows.map(r=>r.marks)).toEqual([4,4]);
    expect(languageMarks(c,row('admission-explanation','full-1'))).toBe(4);
    expect(languageMarks(c,{...row('answer-1'),...row('answer-2')})).toBe(4);
    expect(languageMarks(c,row('independent-partial-1','full-1'))).toBe(1);
    expect(languageMarks(c,{...row('admission-explanation','full-1'),...row('admission-explanation','full-2'),...row('answer-1')})).toBe(4);
    expect(languageMarks(c,{...row('independent-partial-1','full-1'),...row('independent-partial-2','full-1')})).toBe(2);
    expect(languageMarks(c,{...row('answer-2'),...row('answer-2','partial-1')})).toBe(2);
  });
  it('keeps complete and partial family advice in the same semantic answer',()=>{
    const c=points('c1-1-ii');expect(c.rubric.groups).toHaveLength(4);
    expect(languageMarks(c,{...row('answer-1'),...row('answer-1','partial-1'),...row('answer-1','partial-2')})).toBe(2);
    expect(languageMarks(c,{...row('answer-1','partial-1'),...row('answer-2','partial-2')})).toBe(2);
    expect(points('c1-1-i').rubric.groups.filter(g=>g.id.startsWith('independent-partial'))).toHaveLength(3);
  });
  it('retains numeric word-class matching, accepted old infinitive and all seven school words',()=>{
    expect(points('la1').rubric.groups).toHaveLength(5);expect(points('la1').answerLanguageRule).toBeUndefined();
    const verbs=points('la2-i'),g=verbs.rubric.groups[2];expect(g.rows.map(r=>r.text)).toEqual(['прийти','придти']);
    expect(languageMarks(verbs,{...row(g.id),...row(g.id,'old-form')})).toBe(1);
    expect(verbs.rubric.taskRequirements.join(' ')).toContain('but not прийдти or прити');
    expect(points('la2-ii').rubric.groups).toHaveLength(7);
    expect(points('la2-ii').rubric.taskRequirements.join(' ')).toContain('first section');
    expect(points('sd').rubric.groups.map(g=>g.rows[0].text.split(' — ').at(-1))).toEqual(['5','7','6','8','4','3','2','10','9','1']);
  });
  it('matches all fifteen original grammar gaps including every published verb alternative',()=>{
    const c=points('gr');expect(c.rubric.groups).toHaveLength(15);expect(c.rubric.groups.flatMap(g=>g.rows)).toHaveLength(18);
    expect(c.rubric.groups[2].rows.map(r=>r.text)).toEqual(['говорят','говорили','сказали']);
    expect(c.rubric.groups[5].rows.map(r=>r.text)).toEqual(['решил','решал']);
    expect(languageMarks(c,Object.assign({},...c.rubric.groups.flatMap(g=>g.rows.map(r=>row(g.id,r.id)))))).toBe(30);
  });
  it('keeps summary partials, incomplete discretion and whole-language zero distinct',()=>{
    const c=points('c2-1'),g=c.rubric.groups.find(g=>g.label==='Secondary detail');if(!g)throw new Error('secondary');
    const score={...row(g.id,'full',2),[languageScoreId('summary-skills')]:2};
    expect(languageMarks(c,score)).toBe(4);
    expect(languageMarks(c,{...score,[languageRowId(g.id,'full')]:1})).toBe(3);
    expect(languageMarks(c,{...score,[languageFlagId('incomplete-response')]:1})).toBe(3);
    expect(languageMarks(c,{...score,[languageOtherLanguageId('response')]:1})).toBe(0);
  });
  it('uses the source essay deductions without importing the later unsubstantiated-fact rule',()=>{
    const c=writing('se');const score={[languageScoreId('content')]:10,[languageScoreId('expression')]:20,[languageLengthId('words')]:50};
    expect(languageMarks(c,{...score,[languageScoreId('soft-sign-penalty')]:1})).toBe(29);
    expect(languageMarks(c,{...score,[languageScoreId('soft-sign-penalty')]:2})).toBe(28);
    expect(languageMarks(c,{...score,[languageScoreId('content')]:6,[languageScoreId('title-penalty')]:1})).toBe(25);
    expect(c.rubric.criteria[0].guidance.join(' ')).not.toContain('single mark for a fact');
  });
  it('preserves both conflicting Lower A descriptor versions and its consistent numeric range',()=>{
    const c=writing('gw'),expression=c.rubric.criteria.find(x=>x.id==='expression');if(!expression)throw new Error('expression');
    expect(expression.bands).toHaveLength(3);
    const lower=expression.limits?.find(x=>x.id==='lower-a');expect(lower).toMatchObject({minMarks:7,maxMarks:12});expect(lower?.bands).toBeUndefined();
    expect(lower?.guidance.join(' ')).toContain('9/10');expect(lower?.guidance.join(' ')).toContain('9 -11');
    const base={[languageScoreId('content')]:15,[languageScoreId('expression')]:6,[languageLengthId('words')]:140,[languageFlagId('lower-a')]:1};
    expect(languageMarks(c,base)).toBe(15);expect(languageMarks(c,{...base,[languageScoreId('expression')]:11})).toBe(26);
    expect(languageMarks(c,{...base,[languageScoreId('expression')]:15})).toBe(27);
    expect(languageMarks(c,{...base,[languageScoreId('content')]:7,[languageScoreId('expression')]:12})).toBe(17);
    expect(c.rubric.criteria.find(x=>x.id==='soft-sign-penalty')?.permittedMarks).toEqual([0,2]);
  });
  it('applies the explicit employment-reference cap once and restores raw choices',()=>{
    const c=points('l3-1'),flag=languageFlagId('missing-employment-reference');
    expect(c.rubric.groups).toHaveLength(6);expect(c.rubric.count).toBe(2);
    expect(c.rubric.allocationCap?.limits?.[0]).toMatchObject({maxMarks:3,schemePages:[16]});
    const two={...row('answer-4'),...row('answer-5')};
    expect(languageMarks(c,two)).toBe(4);expect(languageMarks(c,{...two,[flag]:1})).toBe(3);expect(languageMarks(c,{...two,[flag]:0})).toBe(4);
    expect(languageMarks(c,{...row('answer-4'),[flag]:1})).toBe(2);expect(languageMarks(c,{[flag]:1})).toBe(0);
    expect(c.rubric.groups.every(g=>g.rows.every(r=>r.marks===2&&!r.steps))).toBe(true);
    expect(c.answerLanguageRule).toBeUndefined();
  });
  it('keeps both printed Q3 asks inside the one four-detail, eight-mark allocation',()=>{
    const c=points('l3-3');expect(c.questionRef).toBe('2015 HL Section L3 Q3(i), (ii)');expect(c.totalMarks).toBe(8);expect(c.rubric.count).toBe(4);
    expect(c.questionText).toContain('Give one detail');expect(c.questionText).toContain('Give three details');
    expect(languageMarks(c,Object.assign({},...[3,4,5,6].map(i=>row(`answer-${i}`))))).toBe(8);
    expect(sitting.some(c=>['ru-2015-hl-l3-3-i','ru-2015-hl-l3-3-ii'].includes(c.id))).toBe(false);
  });
  it('retains the announcement instructions and the question-level championship partial',()=>{
    const announcements=sitting.filter(c=>c.id.startsWith('ru-2015-hl-l1-'));
    expect(announcements).toHaveLength(5);
    expect(announcements.every(c=>c.questionText.includes('Give two details about each'))).toBe(true);
    const c=writing('l3-2');expect(c.rubric.criteria.map(x=>x.permittedMarks)).toEqual([[0,1,2],[0,1,2]]);
    expect(c.rubric.taskRequirements.join(' ')).toContain('Assign one mark: world championship');
    expect(languageMarks(c,{[languageScoreId('detail-1')]:1,[languageScoreId('detail-2')]:2})).toBe(3);
    expect(sitting.filter(c=>c.answerLanguageRule)).toHaveLength(22);
    expect(sitting.filter(c=>c.audioMaterial).every(c=>!c.answerLanguageRule)).toBe(true);
  });
});
