import { describe, expect, it } from 'vitest';
import { execFileSync } from 'node:child_process';
import { existsSync } from 'node:fs';
import { REVIEWED_CARDS } from '../components/MarkBank/cards/russian/reviewed';
import { languageMarks, languageScoreId, languageGroupId, languageRowId } from '../components/MarkBank/languageScoring';
import { isRubricCard, tariffReconciles } from '../types/markBank';

const sitting=REVIEWED_CARDS.filter(c=>c.year===2012&&c.level==='ordinary');
const get=(suffix:string)=>{
  const c=sitting.find(c=>c.id===`ru-2012-ol-${suffix}`);
  if(!c)throw new Error(suffix);
  return c;
};
const points=(suffix:string)=>{
  const c=get(suffix);if(!isRubricCard(c)||c.rubric.system!=='language-points')throw new Error(suffix);
  return {...c,rubric:c.rubric};
};
const writing=(suffix:string)=>{
  const c=get(suffix);if(!isRubricCard(c)||c.rubric.system!=='language-writing')throw new Error(suffix);
  return {...c,rubric:c.rubric};
};
const selected=(group:string,row='full',value=1)=>({[languageGroupId(group)]:1,[languageRowId(group,row)]:value});
const canReadSources=(()=>{
  try {
    execFileSync('python3',['-c','import fitz'],{stdio:'ignore'});
    return ['papers/2012-ol-000-paper.pdf','papers/2012-ol-A00-paper.pdf','schemes/2012-ol.pdf'].every(p=>existsSync(`examiner-reports/russian/${p}`));
  } catch { return false; }
})();

describe('Russian 2012 Ordinary source review',()=>{
  it('covers all 42 independently counted tasks with the printed 220 + 100 marks',()=>{
    expect(sitting).toHaveLength(42);
    expect(sitting.filter(c=>!tariffReconciles(c)).map(c=>c.id)).toEqual([]);
    expect(sitting.reduce((sum,c)=>sum+c.totalMarks,0)).toBe(320);
    expect(sitting.filter(c=>c.audioMaterial)).toHaveLength(19);
    expect(sitting.filter(c=>c.audioMaterial).reduce((sum,c)=>sum+c.totalMarks,0)).toBe(100);
    expect(sitting.every(c=>!c.answerLanguageRule)).toBe(true);
  });
  it('keeps the 5 + 5 + 3 handwriting grid and four separately priced menu subparts',()=>{
    const c=writing('ir1-iv-a');
    expect(c.rubric.criteria.map(r=>r.maxMarks)).toEqual([5,5,3]);
    expect(c.rubric.criteria[2].bands?.map(b=>[b.marks,b.guidance.length])).toEqual([[[3],2],[[2],2],[[1],1]]);
    expect(languageMarks(c,{[languageScoreId('dish-1')]:4,[languageScoreId('dish-2')]:3,[languageScoreId('drink')]:3})).toBe(10);
    expect(['a','b','c','d'].map(letter=>get(`ir1-iv-${letter}`).totalMarks)).toEqual([13,8,4,2]);
    expect(c.questionText).toContain('no more than one from any section');
    expect(c.rubric.markingGuideNote).toContain('No handwritten exemplar');
  });
  it('scores each selected ingredient and the complete bill without invented examples or item splits',()=>{
    const ingredients=writing('ir1-iv-b'),bill=writing('ir1-iv-c');
    expect(ingredients.rubric.criteria.map(r=>r.maxMarks)).toEqual([2,2,2,2]);
    expect(languageMarks(ingredients,{[languageScoreId('dish-1-ingredient-1')]:2,[languageScoreId('dish-1-ingredient-2')]:1,[languageScoreId('dish-2-ingredient-1')]:2})).toBe(5);
    expect(bill.rubric.criteria).toHaveLength(1);
    expect(bill.rubric.criteria[0].permittedMarks).toEqual([0,1,4]);
    expect(languageMarks(bill,{[languageScoreId('bill')]:4})).toBe(4);
    expect(writing('la2').rubric.criteria.map(c=>c.maxMarks)).toEqual([1,1,1,1,1]);
    expect(writing('la2').rubric.markingGuideNote).toContain('no closed answer list');
  });
  it('retains every outing detail and the pool-level hotel partial without an extra answer slot',()=>{
    const c=points('ir2-ii');
    expect(c.rubric.groups).toHaveLength(20);
    expect(c.rubric.count).toBe(6);
    expect(c.rubric.taskRequirements).toContain('one mark: hotel');
    expect(c.rubric.groups.some(g=>g.rows.some(r=>r.text==='hotel'))).toBe(false);
    expect(languageMarks(c,selected('answer-3','full',1))).toBe(1);
    expect(languageMarks(c,{...selected('answer-3','full',2),...selected('answer-9','full',2)})).toBe(4);
    expect(languageMarks(c,Object.assign({},...c.rubric.groups.map(g=>selected(g.id,'full',2))))).toBe(12);
    expect(points('ir2-iii').rubric.groups).toHaveLength(8);
  });
  it('keeps the named comprehension partials in the same answer group as their full versions',()=>{
    const mother=points('cd-2-i'),uncle=points('cd-2-ii');
    expect(languageMarks(mother,selected('answer-1','partial-1'))).toBe(1);
    expect(languageMarks(mother,{...selected('answer-1','full',2),...selected('answer-1','partial-1')})).toBe(2);
    expect(languageMarks(uncle,{...selected('answer-3','full',2),...selected('answer-3','partial-1')})).toBe(2);
    expect(points('cd-3').rubric.groups).toHaveLength(20);
    expect(points('cd-4').rubric.groups).toHaveLength(14);
  });
  it('preserves full and half matching alternatives under one answer per headline',()=>{
    const c=points('mm');
    expect(c.rubric.groups).toHaveLength(10);
    expect(c.rubric.groups[6].rows.map(r=>r.text)).toEqual(['5 / строительство','2 / выставки']);
    expect(c.rubric.groups[8].rows.map(r=>r.text)).toEqual(['10 / религия','7/ праздники']);
    expect(languageMarks(c,selected('answer-6','partial'))).toBe(2);
    expect(languageMarks(c,{...selected('answer-6'),...selected('answer-6','partial')})).toBe(4);
    expect(languageMarks(c,{...selected('answer-7'),...selected('answer-7','alternative-1')})).toBe(4);
    expect(languageMarks(c,Object.assign({},...c.rubric.groups.map(g=>selected(g.id))))).toBe(40);
  });
  it('retains every discourse partial and the independently priced listening music partial',()=>{
    const c=points('sd'),l=points('l4-3');
    for(const group of ['answer-1','answer-4','answer-9']){
      expect(languageMarks(c,selected(group,'partial-1'))).toBe(1);
      expect(languageMarks(c,{...selected(group),...selected(group,'partial-1')})).toBe(2);
    }
    expect(c.rubric.groups[2].rows[0].text).toBe('Как (/когда)');
    expect(languageMarks(c,Object.assign({},...c.rubric.groups.map(g=>selected(g.id))))).toBe(20);
    expect(languageMarks(l,selected('partial','music'))).toBe(3);
    expect(languageMarks(l,{...selected('answer-1'),...selected('partial','music')})).toBe(5);
    expect(points('l1-4').rubric.groups).toHaveLength(12);
  });
  it('keeps all eight cultural topics, three writing choices and source-scoped language guidance',()=>{
    const c=writing('sa'),e=writing('ew');
    expect(c.questionText).toContain('8. Culture in Russia today');
    expect(e.questionText).toContain('3.  Write a profile for your school year book.');
    expect(languageMarks(c,{[languageScoreId('first-content')]:12,[languageScoreId('first-coherence')]:3})).toBe(15);
    expect(languageMarks(e,{[languageScoreId('content')]:6,[languageScoreId('expression')]:12,[languageScoreId('coherence')]:6})).toBe(24);
    expect(points('ir1-i').rubric.taskRequirements).toContain('Do not penalise answers supplied in Russian.');
    expect(points('ir1-i').rubric.taskRequirements).toContain('Where a candidate uses the same information in response to two or more questions, accept the first answer only.');
    expect(points('l2-3').rubric.taskRequirements).toContain('There is no penalty for excess material which does not invalidate the answer.');
  });
  it.skipIf(!canReadSources)('binds all original claims and keeps each menu subpart citation separate',()=>{
    const output=execFileSync('python3',['-c',`
import json,sys
from pathlib import Path
sys.path.insert(0,'scripts/markbank/authoring')
from ru_verify_review import verify
from ru_review_census import reviewed_keys
from reconcile import parse_ref,match_leaves
cards=[c for c in json.loads(Path('scripts/markbank/authored/russian-reviewed.json').read_text()) if c['year']==2012]
verify(cards)
keys=reviewed_keys(2012,'ol')
for letter in ('a','b','c','d'):
    matched=match_leaves(parse_ref('2012 OL Section IR1 Q(iv)('+letter+')'),keys,True)
    assert set(matched)=={('IR1',None,letter,'iv')},matched
c=next(c for c in cards if c['id']=='ru-2012-ol-mm')
c['rubric']['groups'][5]['rows'][1]['text']='Fabricated accepted matching alternative'
try: verify([c])
except AssertionError: pass
else: raise AssertionError('Fabricated answer accepted')
print('Source pools and menu citations verified')
`],{encoding:'utf8'});
    expect(output).toContain('Source pools and menu citations verified');
  });
});
