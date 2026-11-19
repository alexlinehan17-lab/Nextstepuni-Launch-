import { describe, expect, it } from 'vitest';
import { REVIEWED_CARDS } from '../components/MarkBank/cards/russian/reviewed';
import { languageMarks, languageScoreId, languageFlagId, languageGroupId, languageRowId } from '../components/MarkBank/languageScoring';
import { isRubricCard, tariffReconciles } from '../types/markBank';
import { marksClaimed } from '../components/MarkBank/SessionScreen';
const sitting=REVIEWED_CARDS.filter(c=>c.year===2016&&c.level==='ordinary');
const get=(suffix:string)=>{const c=sitting.find(c=>c.id===`ru-2016-ol-${suffix}`);if(!c)throw new Error(suffix);return c;};
const points=(suffix:string)=>{const c=get(suffix);if(!isRubricCard(c)||c.rubric.system!=='language-points')throw new Error(suffix);return {...c,rubric:c.rubric};};
const writing=(suffix:string)=>{const c=get(suffix);if(!isRubricCard(c)||c.rubric.system!=='language-writing')throw new Error(suffix);return {...c,rubric:c.rubric};};
const row=(group:string,id='full',value=1)=>({[languageGroupId(group)]:1,[languageRowId(group,id)]:value});

describe('Russian 2016 Ordinary original-source allocations',()=>{
  it('preserves all 73 tasks and the 220+100 original totals',()=>{
    expect(sitting).toHaveLength(73);expect(sitting.filter(c=>!tariffReconciles(c)).map(c=>c.id)).toEqual([]);
    expect(sitting.reduce((n,c)=>n+c.totalMarks,0)).toBe(320);
    const listening=sitting.filter(c=>c.audioMaterial);expect(listening).toHaveLength(39);expect(listening.reduce((n,c)=>n+c.totalMarks,0)).toBe(100);
    expect(sitting.every(c=>!c.answerLanguageRule)).toBe(true);
  });
  it('retains the explicit answer4 previously lost at the page bottom',()=>{
    const c=points('ir1-v');expect(c.rubric.groups.map(g=>g.rows[0].text)).toEqual(['4']);
    expect(c.questionText).toBe('How many days a week do students attend classes?');
    expect(languageMarks(c,row('answer-1','full',2))).toBe(2);
  });
  it('keeps three half-mark handwriting placements plus one global joining mark',()=>{
    const c=writing('la1');expect(c.rubric.criteria).toHaveLength(4);
    expect(c.rubric.criteria.slice(0,3).map(x=>x.permittedMarks)).toEqual(Array(3).fill([0,.5,1,1.5,2,2.5,3]));
    const score={[languageScoreId('phrase-1')]:2.5,[languageScoreId('phrase-2')]:3,[languageScoreId('phrase-3')]:3,[languageScoreId('joining')]:1};
    expect(languageMarks(c,score)).toBe(9.5);
    expect(languageMarks(c,{...score,[languageFlagId('missing-initial-loop')]:1})).toBe(8.5);
    expect(languageMarks(c,{...score,[languageFlagId('missing-initial-loop')]:0})).toBe(9.5);
    expect(c.rubric.taskRequirements.join(' ')).toContain('Do not penalise for repeat errors');
    expect(c.rubric.taskRequirements.join(' ')).toContain('even if it is not the corresct phrase');
  });
  it('keeps the two complete pool-dimension routes separate',()=>{
    const c=get('ir2-v');if(isRubricCard(c))throw new Error('fixed variants');
    expect(c.answerVariants?.map(x=>x.label)).toEqual(['Big pool','kids’ pool']);
    expect(c.answerVariants?.map(x=>x.rows.map(r=>r.verbatim))).toEqual([['length: 50 m','width: 21 m'],['length: 10m','width: 6m']]);
    expect(marksClaimed(c,{'dimension-1':2,'dimension-2':1})).toBe(3);
    expect(c.rows[0].contextNote).toContain('do not combine dimensions from different pools');
  });
  it('preserves four one-mark classifications and twenty two-mark matches',()=>{
    const c=points('la2'),d=points('mm');expect(c.rubric.groups).toHaveLength(4);expect(d.rubric.groups).toHaveLength(20);
    expect(languageMarks(c,Object.assign({},...c.rubric.groups.map(g=>row(g.id))))).toBe(4);
    expect(languageMarks(d,Object.assign({},...d.rubric.groups.map(g=>row(g.id))))).toBe(40);
    expect(d.rubric.groups.map(g=>g.rows[0].text.split(' — ').at(-1))).toEqual(['4','19','16','17','14','9','3','8','11','15','6','1','5','2','10','12','18','20','7','13']);
  });
  it('retains all ten dialogue answers without inventing a per-gap tariff',()=>{
    const c=get('sd');if(isRubricCard(c))throw new Error('unpriced task');
    expect(c.tariffModel).toEqual({kind:'questionTotal'});expect(c.totalMarks).toBe(20);expect(c.rows).toHaveLength(10);
    expect(c.rows.every(r=>r.marks===null)).toBe(true);expect(c.rows[0].contextNote).toContain('Complete all three interviews');
    expect(c.rows[0].contextNote).toContain('numeric self-scoring is unavailable');
    expect(c.rows[0].contextNote).toContain('Question 4 in the first interview is already complete');
    expect(c.rows[2].verbatim).toBe('скольки/ скольких');
  });
  it('uses the explicit number/sisters split and preserves the repeated-information conditions',()=>{
    const c=points('cd-1-i');expect(c.rubric.groups.map(g=>g.rows[0].text)).toEqual(['2','sisters']);
    expect(languageMarks(c,row('answer-1'))).toBe(1);
    expect(languageMarks(c,{...row('answer-1'),...row('answer-2')})).toBe(2);
    const d=points('cd-2-i');expect(d.rubric.groups[1].rows.map(r=>r.text)).toEqual(['finishing 4th form/class','4th class/form']);
    expect(languageMarks(d,{...row('answer-2','full',2),...row('answer-2','partial-1')})).toBe(2);
    expect(d.rubric.markingGuideNote).toContain('only if it was not already rewarded in Q1(i)');
    expect(points('l4-4-ii').rubric.markingGuideNote).toContain('only if it was not already rewarded in Q1(iii) or Q3(i)');
  });
  it('keeps date and place full/partial alternatives inside their own answer',()=>{
    const c=points('l1-4-i');expect(c.rubric.groups.map(g=>g.label)).toEqual(['When','Where']);
    expect(languageMarks(c,{...row('answer-1'),...row('answer-1','partial-1')})).toBe(2);
    expect(languageMarks(c,{...row('answer-1','partial-1'),...row('answer-2','partial-1')})).toBe(2);
    expect(languageMarks(c,{...row('answer-1'),...row('answer-2')})).toBe(4);
  });
  it('keeps each explicit singing partial within its full concept and all stunt options',()=>{
    const c=points('l4-4-i');expect(c.rubric.groups).toHaveLength(3);
    expect(c.rubric.groups[1].rows.map(r=>r.text)).toEqual(['song “New Russian Kalinka”','New Russian']);
    expect(c.rubric.groups[2].rows.map(r=>r.text)).toEqual(['the song became a worldwide hit','worldwide']);
    expect(languageMarks(c,{...row('answer-2'),...row('answer-2','partial-1')})).toBe(2);
    expect(points('l4-4-iii').rubric.groups).toHaveLength(3);
    expect(points('l2-2').rubric.groups).toHaveLength(9);
    expect(languageMarks(points('l2-2'),Object.assign({},...[1,2,3,4,5].map(n=>row(`answer-${n}`))))).toBe(8);
  });
  it('retains both cultural essays and the source-specific extended-writing grid',()=>{
    const c=writing('sa');expect(c.rubric.criteria.map(x=>x.maxMarks)).toEqual([12,3,12,3]);
    expect(c.questionText).toContain('Housing in the Russian Federation');
    expect(languageMarks(c,{[languageScoreId('first-content')]:8,[languageScoreId('first-coherence')]:3,[languageScoreId('second-content')]:12,[languageScoreId('second-coherence')]:3})).toBe(26);
    const d=writing('ew');expect(d.rubric.criteria.map(x=>x.maxMarks)).toEqual([12,12,6]);
    expect(d.rubric.criteria.some(x=>x.limits?.length)).toBe(false);
    expect(d.questionText).toContain('What plans he/she has for the summer');
    expect(d.rubric.taskRequirements.join(' ')).toContain('No marks are awarded for additional information/content');
  });
});
