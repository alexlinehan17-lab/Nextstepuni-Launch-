import { describe, expect, it } from 'vitest';
import { REVIEWED_CARDS } from '../components/MarkBank/cards/russian/reviewed';
import { languageMarks, languageScoreId, languageLengthId, languageFlagId, languageGroupId, languageRowId, languageOtherLanguageId } from '../components/MarkBank/languageScoring';
import { isRubricCard, tariffReconciles } from '../types/markBank';

const sitting=REVIEWED_CARDS.filter(c=>c.year===2016&&c.level==='higher');
const get=(suffix:string)=>{const c=sitting.find(c=>c.id===`ru-2016-hl-${suffix}`);if(!c||!isRubricCard(c))throw new Error(suffix);return c;};
const points=(suffix:string)=>{const c=get(suffix);if(c.rubric.system!=='language-points')throw new Error(suffix);return {...c,rubric:c.rubric};};
const writing=(suffix:string)=>{const c=get(suffix);if(c.rubric.system!=='language-writing')throw new Error(suffix);return {...c,rubric:c.rubric};};
const row=(group:string,id='full',value=1)=>({[languageGroupId(group)]:1,[languageRowId(group,id)]:value});
const credit=(group:string,value=2)=>({[languageGroupId(group)]:1,[languageScoreId(`${group}-credit`)]:value});

describe('Russian 2016 Higher published allocations',()=>{
  it('covers all 40 independent tasks and the printed 220 plus 80 marks',()=>{
    expect(sitting).toHaveLength(40);expect(sitting.filter(c=>!tariffReconciles(c)).map(c=>c.id)).toEqual([]);
    expect(sitting.reduce((sum,c)=>sum+c.totalMarks,0)).toBe(300);
    expect(sitting.filter(c=>c.audioMaterial)).toHaveLength(20);
    expect(sitting.filter(c=>c.audioMaterial).reduce((sum,c)=>sum+c.totalMarks,0)).toBe(80);
  });
  it('enforces food and reason limits and the actual second-meal partial',()=>{
    const c=points('c1-1-ii');
    expect(c.rubric.allocationCap).toMatchObject({maxMarks:6,answerCount:3,schemePages:[4]});
    expect(languageMarks(c,{...row('food','full-1'),...row('food','full-2'),...row('food','full-3',2)})).toBe(4);
    expect(languageMarks(c,{...row('food','full-1'),...row('food','full-3',1),...row('reasons','full-1')})).toBe(5);
    expect(languageMarks(c,{...row('food','full-1'),...row('food','full-3',2),...row('reasons','full-1'),...row('reasons','full-2')})).toBe(6);
    expect(c.rubric.markingGuideNote).toContain('second meal');
  });
  it('keeps question-level snow partials without inventing a pairing',()=>{
    const c=writing('c1-3-i');expect(c.rubric.criteria.map(x=>x.permittedMarks)).toEqual([[0,1,2],[0,1,2]]);
    expect(languageMarks(c,{[languageScoreId('answer-1')]:1,[languageScoreId('answer-2')]:2})).toBe(3);
    expect(c.rubric.taskRequirements.join(' ')).toContain('plays in the snow + plays with snow flakes');
    expect(c.rubric.markingGuideNote).toContain('no exclusive partial-to-activity mapping');
  });
  it('counts the single smoking event once and enforces the delayed-return discretion rule',()=>{
    const c=points('c2-4'),g=c.rubric.groups.find(x=>x.label==='One smoking event');if(!g)throw new Error('smoking');
    expect(g.rows.map(x=>x.text)).toEqual(['friends were smoking','smoking']);
    const score={...row(g.id,'full',2),...row(g.id,'other-published-wording',2),[languageScoreId('summary-skills')]:2};
    expect(languageMarks(c,score)).toBe(4);
    expect(languageMarks(c,{...score,[languageFlagId('missed-return-delay')]:1})).toBe(2);
    expect(languageMarks(c,{...score,[languageFlagId('incomplete-response')]:1})).toBe(3);
    expect(languageMarks(c,{...score,[languageOtherLanguageId('response')]:1})).toBe(0);
  });
  it('keeps five chosen phrases with independently priced adjective and noun forms',()=>{
    const c=points('la1');expect(c.rubric.groups).toHaveLength(6);expect(c.rubric.count).toBe(5);
    expect(languageMarks(c,row('phrase-1','full-1'))).toBe(1);
    expect(languageMarks(c,{...row('phrase-1','full-1'),...row('phrase-1','full-2')})).toBe(2);
    expect(languageMarks(c,Object.assign({},...c.rubric.groups.flatMap(g=>g.rows.map(r=>row(g.id,r.id)))))).toBe(10);
    expect(c.rubric.taskRequirements.join(' ')).toContain('Penalise the use of и instead of й');
  });
  it('retains all circus words, exact infinitives and original matching order',()=>{
    expect(points('la2-i').rubric.groups).toHaveLength(16);
    expect(points('la2-i').rubric.taskRequirements.join(' ')).toContain('aкробат(ы)');
    expect(points('la2-ii').rubric.groups.map(g=>g.rows[0].text)).toEqual(['пойти','ложиться','спросить','мочь','купить']);
    expect(points('la2-ii').rubric.taskRequirements.join(' ')).toContain('wrong aspect');
    expect(points('sd').rubric.groups.map(g=>g.rows[0].text.split(' — ').at(-1))).toEqual(['1','8','5','7','9','4','10','3','6','2']);
  });
  it('retains all fifteen boxed grammar forms and both printed alternative spellings',()=>{
    const c=points('gr');expect(c.rubric.groups).toHaveLength(15);expect(c.rubric.groups.flatMap(g=>g.rows)).toHaveLength(17);
    expect(c.rubric.groups[1].rows.map(x=>x.text)).toEqual(['мной','мною']);
    expect(c.rubric.groups[3].rows.map(x=>x.text)).toEqual(['пароходе','пароходах']);
    expect(c.rubric.groups[12].rows[0].text).toBe('времени');
    expect(languageMarks(c,{...row('form-2','full-1'),...row('form-2','full-2')})).toBe(2);
    expect(languageMarks(c,Object.assign({},...c.rubric.groups.map(g=>row(g.id,'full-1'))))).toBe(30);
  });
  it('preserves source expression ranges and the one-mark soft-sign deductions',()=>{
    const essay=writing('se'),guided=writing('gw');
    const scores={[languageScoreId('content')]:10,[languageScoreId('expression')]:8,[languageLengthId('words')]:50,[languageFlagId('lower-a')]:1};
    expect(languageMarks(essay,scores)).toBe(10);
    expect(languageMarks(essay,{...scores,[languageScoreId('expression')]:20})).toBe(24);
    expect(languageMarks(guided,{[languageScoreId('content')]:7,[languageScoreId('expression')]:12,[languageLengthId('words')]:140,[languageFlagId('lower-a')]:1})).toBe(17);
    for(const c of [essay,guided])expect(c.rubric.criteria.find(x=>x.id==='soft-sign-penalty')?.maxMarks).toBe(1);
    expect(essay.rubric.criteria[0].guidance.join(' ')).toContain('many Russian words sounds like Irish words');
    expect(guided.rubric.criteria[0].guidance.join(' ')).toContain('at least ONE');
  });
  it('keeps the general sporting route exclusive with named sports under five total details',()=>{
    const c=points('l2-2');expect(c.rubric.alternativeSets?.[0].schemePages).toEqual([16]);
    expect(languageMarks(c,row('sports-general','full-1'))).toBe(2);
    const specifics=Object.assign({},...[1,2,3,4].map(n=>row('sports-specific',`full-${n}`)));
    expect(languageMarks(c,specifics)).toBe(8);
    expect(languageMarks(c,{...specifics,...row('answer-1')})).toBe(10);
    expect(languageMarks(c,{...specifics,...row('sports-general','full-1'),...row('answer-1')})).toBe(2);
  });
  it('keeps Kira travel overlap manual and the singer partial scoped to one concept',()=>{
    const c=points('l1-2');expect(c.rubric.count).toBe(3);expect(c.totalMarks).toBe(6);
    expect(languageMarks(c,{...row('singer-songwriter','full-1'),...row('singer-songwriter','partial-1')})).toBe(2);
    expect(languageMarks(c,{...row('singer-songwriter','partial-1'),...credit('other-detail-1'),...credit('other-detail-2')})).toBe(5);
    expect(languageMarks(c,{...credit('other-detail-1'),...credit('other-detail-2'),...credit('other-detail-3')})).toBe(6);
    expect(languageMarks(c,credit('other-detail-1',1))).toBe(0);
    expect(c.rubric.markingGuideNote).toContain('festival and solo-concert context');
  });
  it('keeps the three camp categories and published cross-question allowances',()=>{
    const c=points('l2-3');expect(c.rubric.groups.map(g=>g.id)).toEqual(['timetable','location','price']);
    expect(languageMarks(c,{...row('price','full-1'),...row('price','full-2')})).toBe(2);
    expect(languageMarks(c,{...row('price','full-2'),...row('location','full-1'),...row('timetable','full-1')})).toBe(6);
    expect(points('l1-4-i').rubric.groups).toHaveLength(7);
    expect(writing('l4-2-i').rubric.taskRequirements.join(' ')).toContain('signed a contract with Universal Music');
    expect(writing('l4-2-ii').rubric.criteria.every(x=>x.permittedMarks?.join(',')==='0,2')).toBe(true);
    expect(languageMarks(points('l3-3-ii'),credit('cross-section'))).toBe(2);
    expect(sitting.filter(c=>c.answerLanguageRule)).toHaveLength(19);
    expect(sitting.filter(c=>c.audioMaterial).every(c=>!c.answerLanguageRule)).toBe(true);
  });
});
