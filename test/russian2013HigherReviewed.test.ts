import { describe, expect, it } from 'vitest';
import { REVIEWED_CARDS } from '../components/MarkBank/cards/russian/reviewed';
import { languageMarks, languageScoreId, languageLengthId, languageFlagId, languageGroupId, languageRowId, languageOtherLanguageId } from '../components/MarkBank/languageScoring';
import { isRubricCard, tariffReconciles } from '../types/markBank';
const sitting=REVIEWED_CARDS.filter(c=>c.year===2013&&c.level==='higher');
const get=(suffix:string)=>{const c=sitting.find(c=>c.id===`ru-2013-hl-${suffix}`);if(!c||!isRubricCard(c))throw new Error(suffix);return c;};
const points=(suffix:string)=>{const c=get(suffix);if(c.rubric.system!=='language-points')throw new Error(suffix);return {...c,rubric:c.rubric};};
const writing=(suffix:string)=>{const c=get(suffix);if(c.rubric.system!=='language-writing')throw new Error(suffix);return {...c,rubric:c.rubric};};
const row=(group:string,id='full',value=1)=>({[languageGroupId(group)]:1,[languageRowId(group,id)]:value});
const slot=(id:string,value:number)=>({[languageGroupId(id)]:1,[languageScoreId(id)]:value});

describe('Russian 2013 Higher supported source tasks',()=>{
  it('publishes thirty-nine supported tasks without hiding the cultural allocation conflict',()=>{
    expect(sitting).toHaveLength(39);expect(sitting.some(c=>c.id==='ru-2013-hl-ca1')).toBe(false);
    expect(sitting.filter(c=>!tariffReconciles(c)).map(c=>c.id)).toEqual([]);
    expect(sitting.reduce((s,c)=>s+c.totalMarks,0)).toBe(292);
    expect(sitting.filter(c=>c.audioMaterial)).toHaveLength(19);
    expect(sitting.filter(c=>c.audioMaterial).reduce((s,c)=>s+c.totalMarks,0)).toBe(80);
  });
  it('preserves three detail placements and the original requirement to describe two places',()=>{
    const c=writing('c1-3-ii');expect(c.rubric.criteria.map(x=>x.permittedMarks)).toEqual([[0,1,2],[0,1,2],[0,1,2]]);
    expect(c.questionText).toContain('details about two places');expect(c.rubric.markingGuideNote).toContain('TWO PLACES');
    expect(languageMarks(c,{[languageScoreId('detail-1')]:2,[languageScoreId('detail-2')]:2,[languageScoreId('detail-3')]:2})).toBe(6);
    expect(languageMarks(c,{[languageScoreId('detail-1')]:1,[languageScoreId('detail-2')]:2})).toBe(3);
  });
  it('retains the shared reading pool and explicit cross-question repeated-information rule',()=>{
    const a=writing('c1-2-i'),b=writing('c1-2-ii');
    expect(a.rubric.taskRequirements).toEqual(b.rubric.taskRequirements);
    expect(a.rubric.taskRequirements.join(' ')).toContain('Accept any details listed below in answer to either question.');
    expect(a.rubric.markingGuideNote).toContain('reward the best answer once');
    expect(languageMarks(a,{[languageScoreId('detail-1')]:1,[languageScoreId('detail-2')]:2})).toBe(3);
  });
  it('caps collection examples at two and all summary details at four while keeping postage half credit',()=>{
    const c=points('c2-1'),g=c.rubric.groups.find(g=>g.rows.some(r=>r.text.startsWith('stamps')));if(!g)throw new Error('collections');
    expect(g.answerCount).toBe(2);expect(g.rows).toHaveLength(4);expect(c.rubric.allocationCap).toMatchObject({maxMarks:8,answerCount:4});
    expect(languageMarks(c,row(g.id,'example-1',1))).toBe(1);
    expect(languageMarks(c,row(g.id,'example-1',2))).toBe(2);
    expect(languageMarks(c,{...row(g.id,'example-1',2),...row(g.id,'example-2',2),...row(g.id,'example-3',2)})).toBe(4);
    const all={...row(g.id,'example-1',2),...row(g.id,'example-2',2),...row('answer-1','full',2),...row('answer-2','full',2),...row('answer-3','full',2),[languageScoreId('summary-skills')]:2};
    expect(languageMarks(c,all)).toBe(10);expect(languageMarks(c,{...all,[languageOtherLanguageId('response')]:1})).toBe(0);
  });
  it('preserves the complete no-full-credit sentence and both-parent requirement with the explicit discretion cap',()=>{
    const c=points('c2-2');expect(c.rubric.taskRequirements.join(' ')).toContain('she collected photographs of artists / of famous people + she took photos of artists');
    expect(c.rubric.markingGuideNote).toContain('mother AND one about the father');
    const score={...slot('detail-1',1),...slot('detail-2',2),[languageScoreId('summary-skills')]:2};
    expect(languageMarks(c,score)).toBe(5);expect(languageMarks(c,{...score,[languageFlagId('incomplete-response')]:1})).toBe(4);
    expect(languageMarks(c,{...score,[languageOtherLanguageId('response')]:1})).toBe(0);
  });
  it('retains exact infinitives and multilingual word-class labels',()=>{
    expect(points('la1').rubric.groups.map(g=>g.rows[0].text)).toEqual(['появиться','ходить','переезжать','зазвонить','заниматься','предложить']);
    expect(points('la1').rubric.groups.every(g=>g.rows[0].marks===1)).toBe(true);
    const c=points('la2');expect(c.rubric.groups.map(g=>g.rows[0].text.split(' / ')[0])).toEqual(['5','1','4','3','2']);
    expect(c.answerLanguageRule).toBeUndefined();expect(c.rubric.groups[0].rows[0].text).toContain('briathar/verb/ глагол');
  });
  it('keeps bracketed matching partials within their own answer and allows the printed four-or-two option',()=>{
    const c=points('sd');expect(c.rubric.groups[0].rows.map(r=>[r.text,r.marks])).toEqual([['9',2],['1',1]]);
    expect(c.rubric.groups[6].rows.map(r=>[r.text,r.marks])).toEqual([['4',2],['2',2]]);
    expect(languageMarks(c,{...row('answer-1','full-1'),...row('answer-1','partial-1')})).toBe(2);
    expect(languageMarks(c,row('answer-1','partial-1'))).toBe(1);
  });
  it('keeps all fifteen grammar positions, the two distinct pronoun answers and only the published capitalization partial',()=>{
    const c=points('gr');expect(c.rubric.groups).toHaveLength(15);
    expect(c.rubric.groups[10].rows[0].text).toBe('нас');expect(c.rubric.groups[12].rows[0].text).toBe('нам');
    expect(languageMarks(c,Object.assign({},...c.rubric.groups.map(g=>row(g.id,'full',2))))).toBe(30);
    expect(languageMarks(c,row('answer-1','full',1))).toBe(1);expect(languageMarks(c,row('answer-1','full',1.5))).toBe(0);
    expect(c.rubric.markingGuideNote).toContain('only the printed half-credit rule');
  });
  it('retains the original essay content descriptors and all seven essay choices',()=>{
    const c=writing('se');expect(c.rubric.criteria.find(x=>x.id==='content')?.bands).toHaveLength(6);
    expect(c.questionText).toContain('7.');expect(c.rubric.criteria.find(x=>x.id==='soft-sign-penalty')?.permittedMarks).toEqual([0,1,2]);
    const score={[languageScoreId('content')]:6,[languageScoreId('title-penalty')]:1,[languageScoreId('expression')]:20,[languageLengthId('words')]:50};
    expect(languageMarks(c,score)).toBe(25);
  });
  it('keeps overlapping guided Lower A descriptors literal within their consistent numeric range',()=>{
    const c=writing('gw'),lower=c.rubric.criteria.find(x=>x.id==='expression')?.limits?.find(x=>x.id==='lower-a');
    expect(lower).toMatchObject({minMarks:7,maxMarks:12});expect(lower?.bands).toBeUndefined();expect(lower?.guidance.join(' ')).toContain('9 -11');
    expect(c.rubric.taskRequirements.join(' ')).toContain('What your interests/ hobbies are?');
    const score={[languageScoreId('content')]:15,[languageScoreId('expression')]:6,[languageLengthId('words')]:140,[languageFlagId('lower-a')]:1};
    expect(languageMarks(c,score)).toBe(15);expect(languageMarks(c,{...score,[languageScoreId('expression')]:11})).toBe(26);
  });
  it('keeps each one-of occupational pool inside one detail',()=>{
    const c=points('l3-1');expect(c.rubric.count).toBe(2);
    expect(languageMarks(c,{...row('translator-requirement','full-1'),...row('translator-requirement','full-2'),...row('translator-requirement','full-3')})).toBe(2);
    expect(languageMarks(c,{...row('translator-requirement','full-1'),...row('interpreter-requirement','full-2')})).toBe(4);
  });
  it('reserves two distinct country slots under the three-detail website maximum',()=>{
    const c=points('l3-4');expect(c.rubric.groups.filter(g=>g.id.startsWith('country-'))).toHaveLength(2);expect(c.rubric.count).toBe(3);
    expect(languageMarks(c,{...slot('country-1',2),...slot('country-2',2)})).toBe(4);
    expect(languageMarks(c,{...slot('country-1',2),...slot('country-2',2),...row('answer-1')})).toBe(6);
    expect(languageMarks(c,slot('country-1',1))).toBe(0);
  });
  it('keeps the missing partial line explicit and listening language-exempt',()=>{
    const c=points('l2-2');expect(c.rubric.groups.every(g=>g.rows.every(r=>r.marks===2&&!r.steps))).toBe(true);
    expect(c.rubric.markingGuideNote).toContain('without supplying a partial answer');
    expect(languageMarks(points('l4-4-i'),{...row('answer-1'),...row('answer-1','partial-1')})).toBe(2);
    expect(sitting.filter(c=>c.answerLanguageRule)).toHaveLength(18);
    expect(sitting.filter(c=>c.audioMaterial).every(c=>!c.answerLanguageRule)).toBe(true);
  });
});
