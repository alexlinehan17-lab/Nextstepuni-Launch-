import { describe, expect, it } from 'vitest';
import { REVIEWED_CARDS } from '../components/MarkBank/cards/russian/reviewed';
import { CARDS as ORDINARY } from '../components/MarkBank/cards/russian/ordinary';
import legacy from '../scripts/markbank/authored/russian.json';
import { languageMarks, languageScoreId, languageFlagId, languageGroupId, languageRowId } from '../components/MarkBank/languageScoring';
import { isRubricCard, tariffReconciles } from '../types/markBank';

const sitting=REVIEWED_CARDS.filter(c=>c.year===2024&&c.level==='ordinary');
function get(suffix:string){
  const card=sitting.find(c=>c.id===`ru-2024-ol-${suffix}`);
  if(!card)throw new Error(suffix);
  return card;
}
function rubric(suffix:string){
  const card=get(suffix);
  if(!isRubricCard(card)||(card.rubric.system!=='language-points'&&card.rubric.system!=='language-writing'))throw new Error(suffix);
  return {...card,rubric:card.rubric};
}
const selected=(group:string,row='full',value=1)=>({[languageGroupId(group)]:1,[languageRowId(group,row)]:value});

describe('Russian 2024 Ordinary original source review',()=>{
  it('covers all 50 printed tasks and preserves 24 corrected identities',()=>{
    expect(sitting).toHaveLength(50);
    expect(sitting.every(tariffReconciles)).toBe(true);
    expect(sitting.reduce((n,c)=>n+c.totalMarks,0)).toBe(320);
    const old=legacy.filter(c=>c.year===2024&&c.level==='ordinary');
    expect(old).toHaveLength(24);
    expect(old.every(c=>ORDINARY.filter(x=>x.id===c.id).length===1)).toBe(true);
    expect(sitting.filter(c=>c.qa?.gates.includes('reviewed-card-correction'))).toHaveLength(24);
    expect(sitting.filter(c=>c.audioMaterial)).toHaveLength(20);
    for(const [section,totals] of Object.entries({L1:[6,3,6,6,4],L2:[4,3,6,6,6],L3:[4,6,6,6,3],L4:[4,6,6,3,6]})){
      expect(sitting.filter(c=>c.section===section).map(c=>c.totalMarks)).toEqual(totals);
    }
  });
  it('prices partial answers without double claiming their full detail',()=>{
    const friends=rubric('l2-3-ii');
    expect(languageMarks(friends,selected('answer-4','partial'))).toBe(1);
    expect(languageMarks(friends,{...selected('answer-4'),...selected('answer-4','partial')})).toBe(3);
    expect(languageMarks(friends,{...selected('answer-1'),...selected('answer-4','partial')})).toBe(4);
    expect(languageMarks(friends,{...selected('answer-1'),...selected('answer-4'),...selected('answer-4','partial')})).toBe(6);
    const cheap=rubric('ir1-2-i');
    expect(languageMarks(cheap,selected('answer-4','partial-1'))).toBe(1);
    expect(languageMarks(cheap,{...selected('answer-4','full',2),...selected('answer-4','partial-1')})).toBe(2);
    expect(languageMarks(cheap,{...selected('answer-1','full',2),...selected('answer-4','partial-1')})).toBe(3);
  });
  it('retains complete language-awareness pools with the published grids',()=>{
    const cursive=rubric('la1'),nominative=rubric('la2');
    expect(cursive.questionText.split('\n\n')[1].split('\n')).toHaveLength(6);
    expect(cursive.questionText).toContain('носить шлем');
    expect(nominative.questionText).not.toContain('mple');
    expect(nominative.rubric.system==='language-points'&&nominative.rubric.groups).toHaveLength(6);
    expect(languageMarks(cursive,{[languageScoreId('phrase-1')]:2,[languageScoreId('phrase-2')]:1,[languageScoreId('phrase-3')]:2})).toBe(5);
    expect(languageMarks(nominative,Object.assign({},...Array.from({length:6},(_,i)=>selected(`answer-${i+1}`))))).toBe(6);
  });
  it('keeps two complete five-gap routes and the complete multiple-choice pool',()=>{
    const dialogue=get('sd');
    if(isRubricCard(dialogue))throw new Error('Wrong discourse type');
    expect(dialogue.answerVariants?.map(v=>v.rows.map(r=>r.verbatim))).toEqual([
      ['закончили','поступила','хотела','учиться','занимаетесь'],['Как','какое','Что','где','когда'],
    ]);
    expect(dialogue.answerVariants?.every(v=>v.rows.every(r=>r.marks===4))).toBe(true);
    const month=get('l3-3-ii');
    for(const name of ['October','December','September','November'])expect(month.questionText).toContain(name);
  });
  it('retains the source numbering and price discrepancies visibly',()=>{
    expect(rubric('cd-3-iii').rubric.markingGuideNote).toContain('scheme prints 3(iv)');
    expect(rubric('cd-3-iv').rubric.markingGuideNote).toContain('scheme prints 3(v)');
    const price=rubric('l3-2');
    expect(price.rubric.system==='language-points'&&price.rubric.groups.some(g=>g.rows.some(r=>r.text==='8 lessons cost 80 000roubles'))).toBe(true);
    expect(price.rubric.markingGuideNote).toContain('8,000 roubles for 8 lessons');
    expect(price.rubric.markingGuideNote).toContain('discrepancy remains unresolved');
    const reading=sitting.filter(c=>['IR1','IR2','CD'].includes(c.section??''));
    expect(reading).toHaveLength(24);
    expect(reading.every(c=>isRubricCard(c)&&(c.rubric.system==='language-points')&&c.rubric.markingGuideNote.includes('page 2: Do not penalise answers supplied in Russian'))).toBe(true);
    expect(sitting.every(c=>!c.answerLanguageRule)).toBe(true);
  });
  it('uses both complete writing pools and the published sentence/content limits',()=>{
    const short=rubric('sa'),extended=rubric('ew');
    for(const topic of ['Leisure time in Russia','Nature in Russia','Weather in Russia','Schools in Russia','Housing in Russia'])expect(short.questionText).toContain(topic);
    for(const topic of ['Camp','Letter','My favourite teacher'])expect(extended.questionText).toContain(topic);
    expect(languageMarks(short,{[languageScoreId('content')]:20,[languageScoreId('coherence')]:4})).toBe(24);
    const scores={[languageScoreId('content')]:12,[languageScoreId('expression')]:12,[languageScoreId('coherence')]:6};
    expect(languageMarks(extended,scores)).toBe(30);
    expect(languageMarks(extended,{...scores,[languageFlagId('fewer-six-sentences')]:1})).toBe(27);
    expect(languageMarks(extended,{...scores,[languageScoreId('content')]:6})).toBe(21);
    expect(languageMarks(extended,{...scores,[languageScoreId('content')]:0})).toBe(15);
  });
});
