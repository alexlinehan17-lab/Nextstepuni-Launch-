import { describe, expect, it } from 'vitest';
import { REVIEWED_CARDS } from '../components/MarkBank/cards/russian/reviewed';
import { CARDS as ORDINARY } from '../components/MarkBank/cards/russian/ordinary';
import legacy from '../scripts/markbank/authored/russian.json';
import { languageMarks, languageScoreId, languageFlagId, languageGroupId, languageRowId } from '../components/MarkBank/languageScoring';
import { isRubricCard, tariffReconciles } from '../types/markBank';

const sitting=REVIEWED_CARDS.filter(c=>c.year===2022&&c.level==='ordinary');
const get=(suffix:string)=>{
  const c=sitting.find(c=>c.id===`ru-2022-ol-${suffix}`);
  if(!c)throw new Error(`Missing ${suffix}`);
  return c;
};
const rubric=(suffix:string)=>{
  const c=get(suffix);
  if(!isRubricCard(c)||(c.rubric.system!=='language-writing'&&c.rubric.system!=='language-points'))throw new Error(`Wrong rubric ${suffix}`);
  return {...c,rubric:c.rubric};
};
const selected=(group:string,row='full',value=1)=>({[languageGroupId(group)]:1,[languageRowId(group,row)]:value});

describe('Russian 2022 Ordinary source review',()=>{
  it('covers the independent 42-task census with all 19 original identities retained',()=>{
    expect(sitting).toHaveLength(42);
    expect(sitting.filter(c=>!tariffReconciles(c)).map(c=>c.id)).toEqual([]);
    expect(sitting.reduce((sum,c)=>sum+c.totalMarks,0)).toBe(305);
    expect(sitting.filter(c=>c.audioMaterial)).toHaveLength(18);
    expect(sitting.filter(c=>c.audioMaterial).reduce((sum,c)=>sum+c.totalMarks,0)).toBe(100);
    const old=legacy.filter(c=>c.year===2022&&c.level==='ordinary');
    expect(old).toHaveLength(19);
    expect(old.every(c=>sitting.filter(x=>x.id===c.id).length===1)).toBe(true);
    expect(old.every(c=>ORDINARY.filter(x=>x.id===c.id).length===1)).toBe(true);
    expect(sitting.filter(c=>c.qa?.gates.includes('reviewed-card-correction'))).toHaveLength(19);
    expect(get('ir1-1').sourceMaterial?.presentationNote).toContain('175 written marks');
  });
  it('keeps all printed reading alternatives, partials and the festival-name maximum',()=>{
    const subjects=rubric('ir1-3'),festivals=rubric('cd-6');
    if(subjects.rubric.system!=='language-points'||festivals.rubric.system!=='language-points')throw new Error('Wrong rubric');
    expect(subjects.rubric.groups).toHaveLength(10);
    expect(subjects.rubric.count).toBe(3);
    expect(languageMarks(subjects,{...selected('answer-1','full',2),...selected('answer-2','full',1)})).toBe(3);
    expect(languageMarks(festivals,selected('festival-name'))).toBe(2);
    expect(languageMarks(festivals,{...selected('festival-name'),...selected('answer-1','full',2),...selected('answer-2','full',2)})).toBe(6);
    expect(festivals.rubric.taskRequirements).toContain('Max 2 marks for mentioning the name of a festival');
    expect(get('cd-4-i').questionText).toBe('Give two details about the Winter Olympics in Sochi.');
    expect(rubric('ir2-1-iv').rubric.system==='language-points' && rubric('ir2-1-iv').rubric).toBeTruthy();
  });
  it('uses the two-mark cursive tariff and the explicit nominative spelling partial',()=>{
    const handwriting=rubric('la1'),nominative=rubric('la2');
    if(handwriting.rubric.system!=='language-writing'||nominative.rubric.system!=='language-points')throw new Error('Wrong rubric');
    expect(handwriting.questionText.split('\n').filter(Boolean)).toHaveLength(7);
    expect(handwriting.questionText).toContain('handwritten/cursive script.');
    expect(handwriting.questionText).not.toContain('lámhscríbhneoireacht');
    expect(handwriting.rubric.criteria.map(c=>c.permittedMarks)).toEqual([[0,2],[0,2],[0,2]]);
    expect(languageMarks(handwriting,{[languageScoreId('phrase-1')]:2,[languageScoreId('phrase-2')]:2,[languageScoreId('phrase-3')]:2})).toBe(6);
    expect(nominative.rubric.groups).toHaveLength(6);
    expect(languageMarks(nominative,selected('answer-1','full',1))).toBe(1);
    expect(nominative.rubric.taskRequirements).toContain('1 mark if nominative correctly identified but spelled incorrectly');
    expect(nominative.questionText).toBe('Put three of the expressions below into the nominative case.');
  });
  it('preserves both five-gap discourse routes and the complete matching task',()=>{
    const discourse=get('sd'),matching=rubric('mm');
    if(isRubricCard(discourse)||matching.rubric.system!=='language-points')throw new Error('Wrong rubric');
    expect(discourse.answerVariants?.map(v=>v.rows.map(r=>r.marks))).toEqual([[4,4,4,4,4],[4,4,4,4,4]]);
    expect(discourse.answerVariants?.map(v=>v.rows.map(r=>r.verbatim))).toEqual([
      ['где','Кем','какое','почему','чем'],['какой','где','почему','что','чего'],
    ]);
    expect(discourse.questionText).not.toContain('L      i  C');
    expect(matching.rubric.groups).toHaveLength(10);
    expect(languageMarks(matching,Object.assign({},...matching.rubric.groups.map(g=>selected(g.id))))).toBe(40);
  });
  it('scores the explicitly split school/day answer as 3 plus 2 within one five-mark question',()=>{
    const school=rubric('l2-2');
    expect(languageMarks(school,selected('school-and-day','school'))).toBe(3);
    expect(languageMarks(school,selected('school-and-day','day'))).toBe(2);
    expect(languageMarks(school,{...selected('school-and-day','school'),...selected('school-and-day','day')})).toBe(5);
    expect(rubric('l1-3-i').totalMarks).toBe(3);
    expect(rubric('l1-3-ii').totalMarks).toBe(2);
    expect(rubric('l1-3-ii').rubric.markingGuideNote).toContain('scheme labels it 4');
    expect(rubric('l4-2-i').rubric.markingGuideNote).toContain('scheme labels it 2(ii)');
  });
  it('uses the reduced 15-mark cultural grid and the complete extended-writing grid',()=>{
    const c=rubric('sa'),e=rubric('ew');
    expect(c.totalMarks).toBe(15);
    expect(c.questionText).toContain('Your favourite Russian writer');
    expect(e.questionText).toContain('Describe a recent camping trip.');
    expect(e.questionText).toContain('My role-model');
    expect(languageMarks(c,{[languageScoreId('content')]:12,[languageScoreId('coherence')]:3})).toBe(15);
    expect(languageMarks(c,{[languageScoreId('content')]:10,[languageScoreId('coherence')]:2})).toBe(12);
    const scores={[languageScoreId('content')]:12,[languageScoreId('expression')]:12,[languageScoreId('coherence')]:6};
    expect(languageMarks(e,scores)).toBe(30);
    expect(languageMarks(e,{...scores,[languageFlagId('fewer-six-sentences')]:1})).toBe(27);
    expect(languageMarks(e,{...scores,[languageScoreId('content')]:6})).toBe(21);
  });
  it('keeps the written and listening Russian-language exceptions visible',()=>{
    expect(sitting.every(c=>!c.answerLanguageRule)).toBe(true);
    for(const c of sitting.filter(c=>['IR1','IR2','CD'].includes(c.section??''))){
      if(!isRubricCard(c)||c.rubric.system!=='language-points')throw new Error('Wrong reading rubric');
      expect(c.rubric.markingGuideNote).toContain('page 3: Do not penalise answers supplied in Russian');
    }
    expect(rubric('l1-1').rubric.taskRequirements.join(' ')).toContain('If an answer is written entirely in Russian – do not penalise');
    expect(get('l4-3').questionText).not.toContain('Rúisis');
  });
});
