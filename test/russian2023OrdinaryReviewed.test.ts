import { describe, expect, it } from 'vitest';
import { REVIEWED_CARDS } from '../components/MarkBank/cards/russian/reviewed';
import { CARDS as ORDINARY } from '../components/MarkBank/cards/russian/ordinary';
import legacy from '../scripts/markbank/authored/russian.json';
import { languageMarks, languageScoreId, languageFlagId, languageGroupId, languageRowId } from '../components/MarkBank/languageScoring';
import { isRubricCard, tariffReconciles } from '../types/markBank';

const sitting=REVIEWED_CARDS.filter(c=>c.year===2023&&c.level==='ordinary');
const get=(suffix:string)=>{
  const c=sitting.find(c=>c.id===`ru-2023-ol-${suffix}`);
  if(!c)throw new Error(`Missing ${suffix}`);
  return c;
};
const rubric=(suffix:string)=>{
  const c=get(suffix);
  if(!isRubricCard(c)||(c.rubric.system!=='language-writing'&&c.rubric.system!=='language-points'))throw new Error(`Wrong rubric ${suffix}`);
  return {...c,rubric:c.rubric};
};
const selected=(group:string,row='full',value=1)=>({[languageGroupId(group)]:1,[languageRowId(group,row)]:value});

describe('Russian 2023 Ordinary source review',()=>{
  it('covers the independent 47-task census with all 23 original addresses retained',()=>{
    expect(sitting).toHaveLength(47);
    expect(sitting.filter(c=>!tariffReconciles(c)).map(c=>c.id)).toEqual([]);
    expect(sitting.reduce((sum,c)=>sum+c.totalMarks,0)).toBe(320);
    expect(sitting.filter(c=>c.audioMaterial)).toHaveLength(18);
    expect(sitting.filter(c=>c.audioMaterial).reduce((sum,c)=>sum+c.totalMarks,0)).toBe(100);
    const old=legacy.filter(c=>c.year===2023&&c.level==='ordinary');
    expect(old).toHaveLength(23);
    expect(old.every(c=>sitting.filter(x=>x.id===c.id).length===1)).toBe(true);
    expect(old.every(c=>ORDINARY.filter(x=>x.id===c.id).length===1)).toBe(true);
    expect(sitting.filter(c=>c.qa?.gates.includes('reviewed-card-correction'))).toHaveLength(23);
  });
  it('keeps summer and all-year camps as separately required answers with source-defined partials',()=>{
    const c=rubric('ir1-3');
    if(c.rubric.system!=='language-points')throw new Error('Wrong rubric');
    expect(c.rubric.groups.map(g=>g.rows[0].text)).toEqual(['Summer: Olympic / Olympic Village / Sun','All-year: Star / Ambitious / Storm']);
    expect(languageMarks(c,selected('answer-1','full',2))).toBe(2);
    expect(languageMarks(c,{...selected('answer-1','full',2),...selected('answer-2','full',1)})).toBe(3);
    expect(languageMarks(c,{...selected('answer-1','full',2),...selected('answer-2','full',2)})).toBe(4);
    expect(rubric('ir1-1').rubric.taskRequirements.join(' ')).toContain('same information is used to answer more than one question');
  });
  it('retains six number choices, six handwriting choices and both complete discourse routes',()=>{
    const number=rubric('la1'),handwriting=rubric('la2'),discourse=get('sd');
    if(number.rubric.system!=='language-points'||handwriting.rubric.system!=='language-writing'||isRubricCard(discourse))throw new Error('Wrong rubric');
    expect(number.rubric.groups).toHaveLength(6);
    expect(number.rubric.count).toBe(3);
    expect(number.rubric.groups.map(g=>g.rows[0].text)).toContain('Черное море — Singular');
    expect(handwriting.questionText).toContain('российских республик');
    expect(handwriting.rubric.criteria).toHaveLength(3);
    expect(languageMarks(handwriting,{[languageScoreId('phrase-1')]:2,[languageScoreId('phrase-2')]:1,[languageScoreId('phrase-3')]:2})).toBe(5);
    expect(discourse.answerVariants?.map(v=>v.rows.map(r=>r.marks))).toEqual([[4,4,4,4,4],[4,4,4,4,4]]);
    expect(discourse.answerVariants?.map(v=>v.rows.map(r=>r.verbatim))).toEqual([
      ['думаю','предпочел','нравятся','стоила','увлекаешься'],
      ['выпить','предпочитаю','находится','нравится','спорят'],
    ]);
  });
  it('keeps the explicitly accepted vegetarian detail and independent surname partial',()=>{
    const emily=rubric('l2-1-i'),parents=rubric('l4-2');
    expect(languageMarks(emily,selected('vegetarian'))).toBe(3);
    expect(languageMarks(emily,{...selected('vegetarian'),...selected('answer-1')})).toBe(6);
    expect(languageMarks(parents,selected('surname','partial'))).toBe(1);
    expect(languageMarks(parents,{...selected('surname','partial'),...selected('answer-1')})).toBe(3);
    expect(parents.rubric.taskRequirements.join(' ')).toContain('no penalty for excess material');
  });
  it('prices cross-segment biography alternatives at each question’s own rate',()=>{
    const fame=rubric('l4-1'),success=rubric('l4-4'),hobbies=rubric('l4-3');
    expect(languageMarks(fame,selected('other-segment-1'))).toBe(3);
    expect(languageMarks(success,selected('other-segment-1'))).toBe(4);
    expect(languageMarks(success,{...selected('other-segment-1'),...selected('answer-1')})).toBe(8);
    expect(fame.rubric.taskRequirements.join(' ')).toContain('Accept relevant details from Segment 4');
    expect(success.rubric.taskRequirements.join(' ')).toContain('Accept relevant details from Segment 1');
    expect(hobbies.rubric.taskRequirements.join(' ')).not.toContain('at least two hobbies');
    expect(languageMarks(hobbies,{...selected('answer-1'),...selected('answer-3')})).toBe(8);
  });
  it('uses the printed cultural and extended-writing grids',()=>{
    const c=rubric('sa'),e=rubric('ew');
    expect(c.questionText).toContain('Cinematography');
    expect(e.questionText).toContain('Autumn holidays');
    expect(e.questionText).toContain('My favourite Russian book');
    expect(languageMarks(c,{[languageScoreId('content')]:24,[languageScoreId('coherence')]:6})).toBe(30);
    const scores={[languageScoreId('content')]:12,[languageScoreId('expression')]:12,[languageScoreId('coherence')]:6};
    expect(languageMarks(e,scores)).toBe(30);
    expect(languageMarks(e,{...scores,[languageFlagId('fewer-six-sentences')]:1})).toBe(27);
    expect(languageMarks(e,{...scores,[languageScoreId('content')]:6})).toBe(21);
  });
  it('shows the verified accepted-Russian exception without inheriting Higher penalties',()=>{
    expect(sitting.every(c=>!c.answerLanguageRule)).toBe(true);
    for(const c of sitting.filter(c=>['IR1','IR2','CD'].includes(c.section??''))){
      if(!isRubricCard(c)||(c.rubric.system!=='language-points'))throw new Error('Wrong reading rubric');
      expect(c.rubric.markingGuideNote).toContain('page 2: Do not penalise answers supplied in Russian');
    }
  });
});
