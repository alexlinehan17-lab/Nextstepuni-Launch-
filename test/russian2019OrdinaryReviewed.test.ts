import { describe, expect, it } from 'vitest';
import { REVIEWED_CARDS } from '../components/MarkBank/cards/russian/reviewed';
import { languageMarks, languageScoreId, languageFlagId, languageGroupId, languageRowId } from '../components/MarkBank/languageScoring';
import { isRubricCard, tariffReconciles } from '../types/markBank';
import { marksClaimed } from '../components/MarkBank/SessionScreen';

const sitting=REVIEWED_CARDS.filter(c=>c.year===2019&&c.level==='ordinary');
const get=(suffix:string)=>{
  const c=sitting.find(c=>c.id===`ru-2019-ol-${suffix}`);
  if(!c)throw new Error(`Missing ${suffix}`);
  return c;
};
const rubric=(suffix:string)=>{
  const c=get(suffix);
  if(!isRubricCard(c)||(c.rubric.system!=='language-writing'&&c.rubric.system!=='language-points'))throw new Error(`Wrong rubric ${suffix}`);
  return {...c,rubric:c.rubric};
};
const selected=(group:string,row='full',value=1)=>({[languageGroupId(group)]:1,[languageRowId(group,row)]:value});

describe('Russian 2019 Ordinary source review',()=>{
  it('covers44 independently counted tasks with all220written and100listening marks',()=>{
    expect(sitting).toHaveLength(44);
    expect(sitting.filter(c=>!tariffReconciles(c)).map(c=>c.id)).toEqual([]);
    expect(sitting.reduce((sum,c)=>sum+c.totalMarks,0)).toBe(320);
    expect(sitting.filter(c=>c.audioMaterial)).toHaveLength(17);
    expect(sitting.filter(c=>c.audioMaterial).reduce((sum,c)=>sum+c.totalMarks,0)).toBe(100);
  });
  it('preserves the theatre partial within one full-answer group and all earlier price options',()=>{
    const places=rubric('ir1-3'),prices=rubric('ir1-7');
    if(places.rubric.system!=='language-points'||prices.rubric.system!=='language-points')throw new Error('Wrong rubric');
    expect(places.rubric.groups).toHaveLength(6);
    expect(languageMarks(places,selected('answer-5','partial-1'))).toBe(1);
    expect(languageMarks(places,{...selected('answer-5','full',2),...selected('answer-5','partial-1')})).toBe(2);
    expect(prices.rubric.groups).toHaveLength(7);
    expect(prices.rubric.groups.at(-1)?.rows[0].text).toBe('детский билет (7‐13 лет) стоит 800 руб');
    expect(languageMarks(prices,{...selected('earlier-price-1','full',2),...selected('earlier-price-4','full',2),...selected('answer-1','full',2)})).toBe(4);
    expect(prices.rubric.markingGuideNote).toContain('if marks have not already been awarded');
  });
  it('keeps English and Russian versions of six adjectives under three accepted details',()=>{
    const c=rubric('cd-3-ii');if(c.rubric.system!=='language-points')throw new Error('Wrong rubric');
    expect(c.rubric.groups).toHaveLength(6);
    expect(c.rubric.groups[0].rows[0].text).toBe('Good — добрая');
    expect(languageMarks(c,Object.assign({},...c.rubric.groups.map(g=>selected(g.id,'full',2))))).toBe(6);
  });
  it('uses both handwriting phrases and all six singular/plural classifications',()=>{
    const handwriting=rubric('la1'),number=rubric('la2'),matching=rubric('mm');
    if(handwriting.rubric.system!=='language-writing'||number.rubric.system!=='language-points'||matching.rubric.system!=='language-points')throw new Error('Wrong rubric');
    expect(handwriting.rubric.criteria.map(c=>c.permittedMarks)).toEqual([[0,3],[0,3]]);
    expect(languageMarks(handwriting,{[languageScoreId('phrase-1')]:3,[languageScoreId('phrase-2')]:3})).toBe(6);
    expect(number.rubric.groups).toHaveLength(6);
    expect(number.rubric.count).toBe(6);
    expect(languageMarks(number,Object.assign({},...number.rubric.groups.map(g=>selected(g.id))))).toBe(6);
    expect(languageMarks(matching,Object.assign({},...matching.rubric.groups.map(g=>selected(g.id))))).toBe(40);
  });
  it('preserves both mandatory dialogues and publishes no invented per-gap or per-detail price',()=>{
    const discourse=get('sd');if(isRubricCard(discourse))throw new Error('Wrong card');
    expect(discourse.answerVariants).toBeUndefined();
    expect(discourse.rows.map(r=>r.verbatim)).toEqual(['Где','кто','кем / где','каком','кем / где','Чем','Какие','Сколько','Когда','какой']);
    for(const suffix of ['sd','l2-2','l3-1','l4-1-i']){
      const c=get(suffix);if(isRubricCard(c))throw new Error('Wrong card');
      expect(c.tariffModel).toEqual({kind:'questionTotal'});
      expect(c.rows.every(r=>r.marks===null)).toBe(true);
      expect(c.rows[0].contextNote).toContain('numeric self-scoring is unavailable');
      expect(marksClaimed(c,Object.fromEntries(c.rows.map(r=>[r.id,1])))).toBe(0);
    }
  });
  it('retains the museum2 partial without double-crediting the full5 detail',()=>{
    const c=rubric('l2-3');
    expect(languageMarks(c,selected('answer-1','museum-partial'))).toBe(2);
    expect(languageMarks(c,selected('answer-1'))).toBe(5);
    expect(languageMarks(c,{...selected('answer-1'),...selected('answer-1','museum-partial')})).toBe(5);
    expect(get('l4-3').questionText).not.toContain('Rúisis');
  });
  it('scores two cultural essays independently and uses only the printed content-driven expression cap',()=>{
    const c=rubric('sa'),e=rubric('ew');
    expect(c.questionText).toContain('TWO of the following topics');
    expect(languageMarks(c,{[languageScoreId('first-content')]:12,[languageScoreId('first-coherence')]:3})).toBe(15);
    expect(languageMarks(c,{[languageScoreId('first-content')]:12,[languageScoreId('first-coherence')]:3,[languageScoreId('second-content')]:12,[languageScoreId('second-coherence')]:3})).toBe(30);
    const scores={[languageScoreId('content')]:12,[languageScoreId('expression')]:12,[languageScoreId('coherence')]:6};
    expect(languageMarks(e,scores)).toBe(30);
    expect(languageMarks(e,{...scores,[languageScoreId('content')]:6})).toBe(21);
    expect(languageMarks(e,{...scores,[languageFlagId('fewer-six-sentences')]:1})).toBe(30);
    expect(sitting.every(c=>!c.answerLanguageRule)).toBe(true);
  });
});
