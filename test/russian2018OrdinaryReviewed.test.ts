import { describe, expect, it } from 'vitest';
import { REVIEWED_CARDS } from '../components/MarkBank/cards/russian/reviewed';
import { languageMarks, languageScoreId, languageFlagId, languageGroupId, languageRowId } from '../components/MarkBank/languageScoring';
import { isRubricCard, tariffReconciles } from '../types/markBank';
import { marksClaimed } from '../components/MarkBank/SessionScreen';

const sitting=REVIEWED_CARDS.filter(c=>c.year===2018&&c.level==='ordinary');
const get=(suffix:string)=>{
  const c=sitting.find(c=>c.id===`ru-2018-ol-${suffix}`);
  if(!c)throw new Error(`Missing ${suffix}`);
  return c;
};
const rubric=(suffix:string)=>{
  const c=get(suffix);
  if(!isRubricCard(c)||(c.rubric.system!=='language-writing'&&c.rubric.system!=='language-points'))throw new Error(`Wrong rubric ${suffix}`);
  return {...c,rubric:c.rubric};
};
const selected=(group:string,row='full',value=1)=>({[languageGroupId(group)]:1,[languageRowId(group,row)]:value});

describe('Russian 2018 Ordinary source review',()=>{
  it('covers43 independently counted tasks including both listening roman asks',()=>{
    expect(sitting).toHaveLength(43);
    expect(sitting.filter(c=>!tariffReconciles(c)).map(c=>c.id)).toEqual([]);
    expect(sitting.reduce((sum,c)=>sum+c.totalMarks,0)).toBe(320);
    expect(sitting.filter(c=>c.audioMaterial)).toHaveLength(17);
    expect(sitting.filter(c=>c.audioMaterial).reduce((sum,c)=>sum+c.totalMarks,0)).toBe(100);
    expect(get('l3-1-ii').questionText).toBe('Name two of the cities in which the Festival will be run.');
    expect(get('l4-3-ii').questionText).toBe('What does Tatyana do apart from painting? Give one detail.');
  });
  it('retains complete source pools while preventing duplicate credit for an identical staff detail',()=>{
    const staff=rubric('ir2-2'),family=rubric('cd-3');
    if(staff.rubric.system!=='language-points'||family.rubric.system!=='language-points')throw new Error('Wrong rubric');
    expect(staff.rubric.groups).toHaveLength(12);
    expect(staff.rubric.groups.flatMap(g=>g.rows).filter(r=>r.text==='work experience with children')).toHaveLength(1);
    expect(languageMarks(staff,{...selected('answer-1','full',2),...selected('answer-2','full',2),...selected('answer-3','full',1)})).toBe(5);
    expect(family.rubric.groups).toHaveLength(17);
    expect(languageMarks(family,Object.assign({},...family.rubric.groups.map(g=>selected(g.id,'full',2))))).toBe(10);
  });
  it('retains all unpriced handwriting targets and both mandatory discourse dialogues',()=>{
    for(const suffix of ['la1','sd']){
      const c=get(suffix);if(isRubricCard(c))throw new Error('Wrong card');
      expect(c.tariffModel).toEqual({kind:'questionTotal'});
      expect(c.rows.every(r=>r.marks===null)).toBe(true);
      expect(c.answerVariants).toBeUndefined();
      expect(c.rows[0].contextNote).toContain('numeric self-scoring is unavailable');
      expect(marksClaimed(c,Object.fromEntries(c.rows.map(r=>[r.id,1])))).toBe(0);
    }
    const c=get('sd');if(isRubricCard(c))throw new Error('Wrong card');
    expect(c.rows.map(r=>r.verbatim)).toEqual(['cлушаю','забронировать','интересуют','скажите','приедете','Добрый','Kонечно','Приятно','Hе за что','большое']);
  });
  it('uses the explicit5-mark listening rate and separate2-mark Dublin option within the two-city quota',()=>{
    const c=rubric('l3-1-ii');if(c.rubric.system!=='language-points')throw new Error('Wrong rubric');
    expect(c.rubric.groups).toHaveLength(8);
    expect(c.rubric.taskRequirements).toContain('Award five marks for each correct/relevant point.');
    expect(languageMarks(c,selected('dublin-partial','partial'))).toBe(2);
    expect(languageMarks(c,{...selected('dublin-partial','partial'),...selected('answer-1')})).toBe(7);
    expect(languageMarks(c,{...selected('dublin-partial','partial'),...selected('answer-1'),...selected('answer-2')})).toBe(10);
    expect(rubric('l1-4').rubric.taskRequirements).toContain('no marks: seat downstairs, ticket for coupe wagon, wagon P');
  });
  it('uses all six1-mark classifications and ten4-mark CV matches',()=>{
    const number=rubric('la2'),matching=rubric('mm');
    if(number.rubric.system!=='language-points'||matching.rubric.system!=='language-points')throw new Error('Wrong rubric');
    expect(languageMarks(number,Object.assign({},...number.rubric.groups.map(g=>selected(g.id))))).toBe(6);
    expect(languageMarks(matching,Object.assign({},...matching.rubric.groups.map(g=>selected(g.id))))).toBe(40);
    expect(rubric('cd-1-iv').rubric.markingGuideNote).toContain('scheme physical page8 prints1.vi');
  });
  it('scores two cultural essays independently and does not inherit the later expression cap',()=>{
    const c=rubric('sa'),e=rubric('ew');
    expect(c.questionText).toContain('Irish‐Russian links');
    expect(languageMarks(c,{[languageScoreId('first-content')]:12,[languageScoreId('first-coherence')]:3})).toBe(15);
    expect(languageMarks(c,{[languageScoreId('first-content')]:12,[languageScoreId('first-coherence')]:3,[languageScoreId('second-content')]:12,[languageScoreId('second-coherence')]:3})).toBe(30);
    const scores={[languageScoreId('content')]:6,[languageScoreId('expression')]:12,[languageScoreId('coherence')]:6};
    expect(languageMarks(e,scores)).toBe(24);
    expect(languageMarks(e,{...scores,[languageFlagId('fewer-six-sentences')]:1})).toBe(24);
    expect(rubric('ir1-i').rubric.markingGuideNote).not.toContain('Do not penalise answers supplied in Russian');
    expect(sitting.every(c=>!c.answerLanguageRule)).toBe(true);
  });
});
