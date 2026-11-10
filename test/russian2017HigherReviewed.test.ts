import { describe, expect, it } from 'vitest';
import { REVIEWED_CARDS } from '../components/MarkBank/cards/russian/reviewed';
import { languageMarks, languageScoreId, languageLengthId, languageFlagId, languageGroupId, languageRowId, languageOtherLanguageId } from '../components/MarkBank/languageScoring';
import { isRubricCard, tariffReconciles } from '../types/markBank';

const sitting=REVIEWED_CARDS.filter(c=>c.year===2017&&c.level==='higher');
const get=(suffix:string)=>{
  const c=sitting.find(c=>c.id===`ru-2017-hl-${suffix}`);
  if(!c||!isRubricCard(c))throw new Error(suffix);
  return c;
};
const points=(suffix:string)=>{const c=get(suffix);if(c.rubric.system!=='language-points')throw new Error(suffix);return {...c,rubric:c.rubric};};
const writing=(suffix:string)=>{const c=get(suffix);if(c.rubric.system!=='language-writing')throw new Error(suffix);return {...c,rubric:c.rubric};};
const selected=(group:string,row='full',value=1)=>({[languageGroupId(group)]:1,[languageRowId(group,row)]:value});

describe('Russian 2017 Higher original source review',()=>{
  it('covers all 20 written and 19 listening tasks and the printed 300 marks',()=>{
    expect(sitting).toHaveLength(39);
    expect(sitting.filter(c=>!tariffReconciles(c)).map(c=>c.id)).toEqual([]);
    expect(sitting.reduce((sum,c)=>sum+c.totalMarks,0)).toBe(300);
    expect(sitting.filter(c=>c.audioMaterial)).toHaveLength(19);
    expect(sitting.filter(c=>c.audioMaterial).reduce((sum,c)=>sum+c.totalMarks,0)).toBe(80);
  });
  it('requires the named reading dimensions and preserves their partials',()=>{
    const reaction=points('c1-1'),police=points('c1-3-ii'),found=points('c1-4-ii');
    expect(languageMarks(reaction,{...selected('reaction','full-1'),...selected('reaction','full-2')})).toBe(2);
    expect(languageMarks(reaction,{...selected('reaction','full-1'),...selected('changed','partial-1')})).toBe(3);
    expect(languageMarks(police,{...selected('policeman-1','full-1'),...selected('policeman-1','full-2'),...selected('policeman-1','full-3')})).toBe(4);
    expect(languageMarks(police,{...selected('policeman-1','full-1'),...selected('policeman-1','full-2'),...selected('policeman-2','full-1'),...selected('policeman-2','full-2')})).toBe(8);
    expect(languageMarks(found,{...selected('where','partial-1'),...selected('what','full-1')})).toBe(3);
    expect(points('c1-4-i').rubric.groups).toHaveLength(4);
    expect(points('c1-4-i').rubric.markingGuideNote).toContain('// two animals//');
    expect(points('c1-4-i').rubric.taskRequirements.join(' ')).toContain('synthesizing skills');
  });
  it('preserves the ten required case prompts with two per correct answer capped at ten',()=>{
    const c=points('la1');expect(c.rubric.groups).toHaveLength(10);expect(c.rubric.count).toBe(10);
    expect(c.rubric.allocationCap).toMatchObject({maxMarks:10,schemePages:[5]});
    expect(c.rubric.allocationCap?.answerCount).toBeUndefined();
    expect(languageMarks(c,Object.assign({},...c.rubric.groups.slice(0,4).map(g=>selected(g.id))))).toBe(8);
    expect(languageMarks(c,Object.assign({},...c.rubric.groups.map(g=>selected(g.id))))).toBe(10);
    expect(c.questionText).toContain('Irish, English or Russian');expect(c.answerLanguageRule).toBeUndefined();
  });
  it('keeps both printed listening-word entries but awards the single passage word once',()=>{
    const c=points('la2');expect(c.rubric.groups).toHaveLength(33);expect(c.rubric.groups.flatMap(g=>g.rows)).toHaveLength(34);
    const overlap=c.rubric.groups[0];expect(overlap.rows.map(r=>r.text)).toEqual(['(по)слушать','послушать']);
    expect(languageMarks(c,{...selected(overlap.id),...selected(overlap.id,'prefixed-form')})).toBe(1);
    expect(languageMarks(c,Object.assign({},...c.rubric.groups.slice(0,10).map(g=>selected(g.id))))).toBe(10);
    expect(c.rubric.markingGuideNote).toContain('one supplied word');
  });
  it('retains the exact matching order and all fifteen underlined grammar forms',()=>{
    expect(points('sd').rubric.groups.map(g=>g.rows[0].text.split(' — ').at(-1))).toEqual(['6','5','2','8','7','1','10','9','3','4']);
    const c=points('gr');expect(c.rubric.groups).toHaveLength(15);expect(c.rubric.groups.flatMap(g=>g.rows)).toHaveLength(16);
    expect(c.rubric.groups.map(g=>g.rows[0].text)).toEqual(['школе','моей','станет','школьной','школьном','ответственной','познавала','природы','историю','химии','уроках','жизненного','литературными','нашла','мне']);
    const lesson=c.rubric.groups[10];expect(lesson.rows[1].text).toBe('урокe');
    expect(languageMarks(c,{...selected(lesson.id,'full-1'),...selected(lesson.id,'accepted-singular')})).toBe(2);
    expect(languageMarks(c,Object.assign({},...c.rubric.groups.map(g=>selected(g.id,'full-1'))))).toBe(30);
    expect(c.rubric.taskRequirements.join(' ')).toContain('do not accept литературным');
  });
  it('distinguishes two-mark secondary details from intelligible one-mark partial details',()=>{
    const c=points('c2-1');expect(c.rubric.groups).toHaveLength(10);
    expect(languageMarks(c,selected('answer-8','full',2))).toBe(2);
    expect(languageMarks(c,selected('answer-8','full',1))).toBe(1);
    const scores={...selected('answer-8','full',2),[languageScoreId('summary-skills')]:2};
    expect(languageMarks(c,scores)).toBe(4);
    expect(languageMarks(c,{...scores,[languageFlagId('incomplete-response')]:1})).toBe(3);
    expect(languageMarks(c,{...scores,[languageOtherLanguageId('response')]:1})).toBe(2);
  });
  it('prevents crowd-general and crowd-specific routes from earning duplicate credit',()=>{
    const c=points('c2-4');
    expect(c.rubric.alternativeSets?.[0]).toMatchObject({id:'crowd-joining',schemePages:[7]});
    expect(c.rubric.groups.find(g=>g.id==='crowd-specific')?.rows).toHaveLength(4);
    const general=selected('crowd-general','full-1',2);
    const specifics={...selected('crowd-specific','full-1',2),...selected('crowd-specific','full-2',2)};
    expect(languageMarks(c,general)).toBe(2);
    expect(languageMarks(c,specifics)).toBe(4);
    expect(languageMarks(c,{...general,...specifics})).toBe(0);
    const others={...selected('answer-1','full',2),...selected('answer-2','full',2),...selected('answer-3','full',2)};
    expect(languageMarks(c,{...specifics,...others,[languageScoreId('summary-skills')]:2})).toBe(10);
    const conflict={...general,...others,...selected('crowd-specific','full-1',1),...selected('crowd-specific','full-2',1)};
    expect(languageMarks(c,conflict)).toBe(6);
    expect(languageMarks(c,{...conflict,[languageGroupId('crowd-specific')]:0})).toBe(8);
    expect(languageMarks(c,{...conflict,[languageGroupId('crowd-general')]:0})).toBe(7);
  });
  it('uses the source Lower A ranges without automatically awarding their minimum',()=>{
    const essay=writing('se'),guided=writing('gw');
    const score={ [languageScoreId('content')]:10,[languageScoreId('expression')]:8,[languageLengthId('words')]:50 };
    expect(languageMarks(essay,{...score,[languageFlagId('lower-a')]:1})).toBe(10);
    expect(languageMarks(essay,score)).toBe(18);
    expect(languageMarks(essay,{...score,[languageScoreId('expression')]:20,[languageFlagId('lower-a')]:1})).toBe(24);
    expect(languageMarks(essay,{...score,[languageScoreId('content')]:0,[languageScoreId('expression')]:20,[languageFlagId('lower-a')]:1})).toBe(0);
    const both={ [languageScoreId('content')]:7,[languageScoreId('expression')]:12,[languageScoreId('coherence')]:10,[languageLengthId('words')]:140,[languageFlagId('lower-a')]:1 };
    expect(languageMarks(guided,both)).toBe(27);
    expect(languageMarks(guided,{...both,[languageScoreId('expression')]:6})).toBe(17);
    for(const c of [essay,guided])expect(c.rubric.criteria.find(x=>x.id==='soft-sign-penalty')?.permittedMarks).toEqual([0,1]);
  });
  it('keeps listening categories, full-credit spellings and the complete wrong-month partial',()=>{
    const event=points('l2-3-i');
    expect(languageMarks(event,{...selected('date','full-1'),...selected('date','full-2')})).toBe(2);
    expect(languageMarks(event,{...selected('date','partial-1'),...selected('location','full-1')})).toBe(3);
    const judo=points('l3-1-i');expect(languageMarks(judo,{...selected('answer-2'),...selected('answer-2','accepted-spelling')})).toBe(2);
    const birth=points('l4-1-i');expect(birth.rubric.groups[0].rows[1].text).toBe('10th + incorrect month');
    expect(languageMarks(birth,{...selected('answer-1'),...selected('answer-1','partial-1')})).toBe(2);
    expect(languageMarks(birth,{...selected('answer-1','partial-1'),...selected('answer-2')})).toBe(3);
    expect(points('l3-2').totalMarks).toBe(8);
    expect(sitting.filter(c=>c.audioMaterial).every(c=>!c.answerLanguageRule)).toBe(true);
  });
  it('retains the published country/detail tariff without deciding the ambiguous slash combination',()=>{
    const c=writing('l3-3-i');expect(c.rubric.criteria.map(x=>x.maxMarks)).toEqual([1,1,1,1]);
    expect(languageMarks(c,Object.fromEntries(c.rubric.criteria.map(x=>[languageScoreId(x.id),1])))).toBe(4);
    expect(c.rubric.taskRequirements.join(' ')).toContain('China /Vietnam');
    expect(c.rubric.markingGuideNote).toContain('does not clarify whether both');
  });
});
