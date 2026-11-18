import { describe, expect, it } from 'vitest';
import { REVIEWED_CARDS } from '../components/MarkBank/cards/russian/reviewed';
import { CARDS as ORDINARY } from '../components/MarkBank/cards/russian/ordinary';
import legacy from '../scripts/markbank/authored/russian.json';
import { languageMarks, languageScoreId, languageFlagId, languageGroupId, languageRowId } from '../components/MarkBank/languageScoring';
import { isRubricCard, tariffReconciles } from '../types/markBank';
import { marksClaimed } from '../components/MarkBank/SessionScreen';

const sitting=REVIEWED_CARDS.filter(c=>c.year===2021&&c.level==='ordinary');
const get=(suffix:string)=>{
  const c=sitting.find(c=>c.id===`ru-2021-ol-${suffix}`);
  if(!c)throw new Error(`Missing ${suffix}`);
  return c;
};
const rubric=(suffix:string)=>{
  const c=get(suffix);
  if(!isRubricCard(c)||(c.rubric.system!=='language-writing'&&c.rubric.system!=='language-points'))throw new Error(`Wrong rubric ${suffix}`);
  return {...c,rubric:c.rubric};
};
const selected=(group:string,row='full',value=1)=>({[languageGroupId(group)]:1,[languageRowId(group,row)]:value});

describe('Russian 2021 Ordinary source review',()=>{
  it('covers 47 independently counted tasks and retains all 24 original identities',()=>{
    expect(sitting).toHaveLength(47);
    expect(sitting.filter(c=>!tariffReconciles(c)).map(c=>c.id)).toEqual([]);
    expect(sitting.reduce((sum,c)=>sum+c.totalMarks,0)).toBe(305);
    expect(sitting.filter(c=>c.audioMaterial)).toHaveLength(18);
    expect(sitting.filter(c=>c.audioMaterial).reduce((sum,c)=>sum+c.totalMarks,0)).toBe(100);
    const old=legacy.filter(c=>c.year===2021&&c.level==='ordinary');
    expect(old).toHaveLength(24);
    expect(old.every(c=>sitting.filter(x=>x.id===c.id).length===1)).toBe(true);
    expect(old.every(c=>ORDINARY.filter(x=>x.id===c.id).length===1)).toBe(true);
    expect(sitting.filter(c=>c.qa?.gates.includes('reviewed-card-correction'))).toHaveLength(24);
  });
  it('retains full reading pools, claimable partials and the booklet address',()=>{
    const countries=rubric('ir1-ii'),villa=rubric('ir2-i'),life=rubric('cd-1-iii');
    if(countries.rubric.system!=='language-points'||villa.rubric.system!=='language-points'||life.rubric.system!=='language-points')throw new Error('Wrong rubric');
    expect(countries.rubric.groups).toHaveLength(8);
    expect(countries.rubric.count).toBe(3);
    expect(villa.rubric.groups).toHaveLength(9);
    expect(life.rubric.groups).toHaveLength(5);
    expect(life.rubric.groups.at(-1)?.rows[0].text).toBe('Spent days in IKEA + had nowhere else to go');
    expect(languageMarks(countries,{...selected('answer-1','full',2),...selected('answer-2','full',1)})).toBe(3);
    expect(rubric('ir1-viii').rubric.markingGuideNote).toContain('scheme page4 repeats(vii)');
  });
  it('uses the two-of-four cursive3-mark tariff and six nominative choices',()=>{
    const handwriting=rubric('la1'),nominative=rubric('la2');
    if(handwriting.rubric.system!=='language-writing'||nominative.rubric.system!=='language-points')throw new Error('Wrong rubric');
    expect(handwriting.questionText.split('\n').filter(Boolean)).toHaveLength(5);
    expect(handwriting.rubric.criteria.map(c=>c.permittedMarks)).toEqual([[0,3],[0,3]]);
    expect(languageMarks(handwriting,{[languageScoreId('phrase-1')]:3})).toBe(3);
    expect(languageMarks(handwriting,{[languageScoreId('phrase-1')]:3,[languageScoreId('phrase-2')]:3})).toBe(6);
    expect(nominative.rubric.groups).toHaveLength(6);
    expect(nominative.rubric.groups.every(g=>!g.rows[0].steps)).toBe(true);
    expect(languageMarks(nominative,selected('answer-1'))).toBe(2);
  });
  it('preserves both discourse routes including the printed slash alternative',()=>{
    const discourse=get('sd'),matching=rubric('mm');
    if(isRubricCard(discourse)||matching.rubric.system!=='language-points')throw new Error('Wrong rubric');
    expect(discourse.answerVariants?.map(v=>v.rows.map(r=>r.verbatim))).toEqual([
      ['где','как','кто','почему/как','какие'],['o чём','сколько','что','какую','какие'],
    ]);
    expect(discourse.answerVariants?.map(v=>v.rows.reduce((s,r)=>s+(r.marks??0),0))).toEqual([20,20]);
    expect(matching.rubric.groups).toHaveLength(10);
    expect(languageMarks(matching,Object.assign({},...matching.rubric.groups.map(g=>selected(g.id))))).toBe(40);
    expect(discourse.questionText).not.toContain('Roghnaigh');
  });
  it('uses ordered2+3 awards without assigning specific accepted answers to a price',()=>{
    for(const suffix of ['l2-1-i','l3-4']){
      const c=get(suffix);if(isRubricCard(c))throw new Error('Wrong card');
      expect(c.rows[0].group?.perOptionSteps).toEqual([2,3]);
      expect(c.rows[0].group?.claimMax).toBe(2);
      expect(marksClaimed(c,{}, {answers:[0]})).toBe(2);
      expect(marksClaimed(c,{}, {answers:[0,1]})).toBe(5);
      expect(marksClaimed(c,{}, {answers:[0,1,2]})).toBe(5);
    }
    expect(get('l3-2-i').questionText).toBe('Give one detail about the cabins on the steamboat.');
  });
  it('retains the separately priced guitar partial and original one-answer quota',()=>{
    const c=rubric('l1-2');
    expect(languageMarks(c,selected('guitar-partial','partial'))).toBe(2);
    expect(languageMarks(c,selected('answer-5'))).toBe(5);
    expect(languageMarks(c,{...selected('answer-5'),...selected('guitar-partial','partial')})).toBe(5);
  });
  it('uses only the published2021 extended-writing content cap and cultural15-mark grid',()=>{
    const c=rubric('sa'),e=rubric('ew');
    expect(c.questionText).toContain('Shops in the Russian Federation');
    expect(e.questionText).toContain('Write about a famous person you follow on social media.');
    expect(e.questionText).not.toContain('Níl sna');
    expect(languageMarks(c,{[languageScoreId('content')]:12,[languageScoreId('coherence')]:3})).toBe(15);
    const scores={[languageScoreId('content')]:12,[languageScoreId('expression')]:12,[languageScoreId('coherence')]:6};
    expect(languageMarks(e,scores)).toBe(30);
    expect(languageMarks(e,{...scores,[languageScoreId('content')]:6})).toBe(21);
    expect(languageMarks(e,{...scores,[languageFlagId('fewer-six-sentences')]:1})).toBe(30);
    expect(sitting.every(c=>!c.answerLanguageRule)).toBe(true);
  });
});
