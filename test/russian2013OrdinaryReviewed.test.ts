import { describe, expect, it } from 'vitest';
import { execFileSync } from 'node:child_process';
import { existsSync } from 'node:fs';
import { REVIEWED_CARDS } from '../components/MarkBank/cards/russian/reviewed';
import { languageMarks, languageScoreId, languageGroupId, languageRowId } from '../components/MarkBank/languageScoring';
import { isRubricCard, tariffReconciles } from '../types/markBank';

const sitting=REVIEWED_CARDS.filter(c=>c.year===2013&&c.level==='ordinary');
const get=(suffix:string)=>{
  const c=sitting.find(c=>c.id===`ru-2013-ol-${suffix}`);
  if(!c)throw new Error(suffix);
  return c;
};
const points=(suffix:string)=>{
  const c=get(suffix);if(!isRubricCard(c)||c.rubric.system!=='language-points')throw new Error(suffix);
  return {...c,rubric:c.rubric};
};
const selected=(group:string,row='full',value=1)=>({[languageGroupId(group)]:1,[languageRowId(group,row)]:value});
const canReadSources=(()=>{
  try {
    execFileSync('python3',['-c','import fitz'],{stdio:'ignore'});
    return ['papers/2013-ol-000-paper.pdf','papers/2013-ol-A00-paper.pdf','schemes/2013-ol.pdf'].every(p=>existsSync(`examiner-reports/russian/${p}`));
  } catch { return false; }
})();

describe('Russian 2013 Ordinary source review',()=>{
  it('covers the independent 42-task census with 220 written and 100 listening marks',()=>{
    expect(sitting).toHaveLength(42);
    expect(sitting.filter(c=>!tariffReconciles(c)).map(c=>c.id)).toEqual([]);
    expect(sitting.reduce((sum,c)=>sum+c.totalMarks,0)).toBe(320);
    expect(sitting.filter(c=>c.audioMaterial)).toHaveLength(18);
    expect(sitting.filter(c=>c.audioMaterial).reduce((sum,c)=>sum+c.totalMarks,0)).toBe(100);
    expect(sitting.every(c=>!c.answerLanguageRule)).toBe(true);
  });
  it('discounts only the printed handwriting column and keeps both restaurant subparts',()=>{
    const c=points('ir1-i');
    expect(c.questionText).toContain('handwritten/cursive script');
    expect(c.rubric.groups).toHaveLength(8);
    expect(languageMarks(c,Object.assign({},...c.rubric.groups.map(g=>selected(g.id,'full',2))))).toBe(16);
    expect(c.rubric.taskRequirements.some(t=>t.includes('Discount as majority'))).toBe(true);
    expect(get('ir1-ii-a').questionRef).toBe('2013 OL Section IR1 Q(ii)(a)');
    expect(get('ir1-ii-b').questionRef).toBe('2013 OL Section IR1 Q(ii)(b)');
    expect(points('ir1-ii-a').rubric.groups[0].rows[0].text).toBe('Кавказский дворик / ЛиВуар');
    expect(points('ir1-ii-b').rubric.groups[0].rows[0].text).toBe('Кавказский дворик');
  });
  it('caps learner groups at two details each and five groups overall without splitting slash text',()=>{
    const c=points('ir2-ii');
    expect(c.rubric.count).toBe(5);
    expect(c.rubric.groups.map(g=>g.rows.length)).toEqual([4,4,5,3,4,5,5,6,5]);
    expect(c.rubric.groups.every(g=>g.answerCount===2)).toBe(true);
    expect(c.rubric.groups[1].rows.slice(2).map(r=>r.text)).toEqual(['2 groups // primary/beginners’ school/ 1-4 classes','secondary school (5-11 classes) //']);
    expect(languageMarks(c,selected('group-1','detail-1',1))).toBe(1);
    expect(languageMarks(c,Object.assign({},...c.rubric.groups[0].rows.map(r=>selected('group-1',r.id,2))))).toBe(4);
    expect(languageMarks(c,Object.assign({},...c.rubric.groups.flatMap(g=>g.rows.map(r=>selected(g.id,r.id,2)))))).toBe(20);
    expect(c.rubric.groups[3].rows.at(-1)?.text).toBe('parents of adopted children');
  });
  it('retains form criteria without invented personal answers and the open gender-phrase rule',()=>{
    const form=get('ir1-iii'),grammar=get('la1');
    if(!isRubricCard(form)||form.rubric.system!=='language-writing'||!isRubricCard(grammar)||grammar.rubric.system!=='language-writing')throw new Error('Wrong cards');
    expect(form.rubric.criteria.map(c=>c.maxMarks)).toEqual(Array(8).fill(1));
    expect(languageMarks(form,Object.fromEntries(form.rubric.criteria.map(c=>[languageScoreId(c.id),1])))).toBe(8);
    expect(grammar.rubric.criteria.map(c=>c.permittedMarks)).toEqual([[0,1,2],[0,1,2],[0,1,2]]);
    expect(languageMarks(grammar,{[languageScoreId('masculine')]:1,[languageScoreId('feminine')]:2,[languageScoreId('neuter')]:1})).toBe(4);
    expect(grammar.rubric.taskRequirements[0]).toContain('whether it is in the text or not');
  });
  it('retains all stem choices, eight five-mark matches and all ten mandatory discourse gaps',()=>{
    const stems=points('la2'),matches=points('mm'),discourse=points('sd');
    expect(stems.rubric.groups).toHaveLength(6);
    expect(languageMarks(stems,Object.assign({},...stems.rubric.groups.map(g=>selected(g.id))))).toBe(4);
    expect(matches.rubric.groups.map(g=>g.rows[0].text.split(' — ')[0])).toEqual(['3','4','6','8','7','1','5','2']);
    expect(languageMarks(matches,Object.assign({},...matches.rubric.groups.map(g=>selected(g.id))))).toBe(40);
    expect(matches.questionText?.endsWith('provided beside each interview title.')).toBe(true);
    expect(discourse.rubric.groups).toHaveLength(10);
    expect(discourse.rubric.groups[4].rows[0].text).toBe('Какая/ Кто');
    expect(languageMarks(discourse,Object.assign({},...discourse.rubric.groups.map(g=>selected(g.id))))).toBe(20);
    expect(discourse.questionText).not.toContain('rds что');
  });
  it('retains complete plus-separated details and prevents full/partial double credit',()=>{
    const c=points('cd-1-iii');
    expect(languageMarks(c,selected('answer-1','partial'))).toBe(1);
    expect(languageMarks(c,{...selected('answer-1','full',2),...selected('answer-1','partial')})).toBe(2);
    expect(points('cd-2-i').rubric.groups).toHaveLength(12);
    const benefits=points('cd-3-ii');
    expect(benefits.rubric.groups).toHaveLength(6);
    expect(languageMarks(benefits,Object.assign({},...benefits.rubric.groups.map(g=>selected(g.id,'full',2))))).toBe(4);
    expect(benefits.rubric.markingGuideNote).toContain('Three of');
  });
  it('keeps all writing choices, two independently scored essays and the uncapped expression grid',()=>{
    const c=get('sa'),e=get('ew');if(!isRubricCard(c)||!isRubricCard(e))throw new Error('Wrong cards');
    expect(c.questionText).toContain('7. Education in the Russian Federation');
    expect(e.questionText).toContain('4.  Write a CV in Russian.');
    expect(e.questionText).toContain('ask and answer 5 questions');
    expect(e.questionText).not.toContain('____');
    expect(languageMarks(c,{[languageScoreId('first-content')]:12,[languageScoreId('first-coherence')]:3})).toBe(15);
    expect(languageMarks(e,{[languageScoreId('content')]:6,[languageScoreId('expression')]:12,[languageScoreId('coherence')]:6})).toBe(24);
  });
  it('scopes Russian/excess-material allowances to listening and preserves twenty country alternatives',()=>{
    const countries=points('l3-4'),entertainment=points('l2-2-ii');
    expect(countries.rubric.groups).toHaveLength(20);
    expect(languageMarks(countries,Object.assign({},...countries.rubric.groups.map(g=>selected(g.id))))).toBe(10);
    expect(entertainment.rubric.groups.at(-1)?.rows[0].text).toBe('people dressed in green');
    expect(points('l4-4').rubric.groups[0].rows[0].text).toBe('b. 1971');
    expect(entertainment.rubric.taskRequirements).toContain('There is no penalty for excess material which does not invalidate the answer.');
    expect(entertainment.rubric.taskRequirements.some(t=>t.includes('entirely in Russian'))).toBe(true);
    expect(points('ir2-i').rubric.taskRequirements.some(t=>t.includes('Do not penalise answers supplied in Russian'))).toBe(false);
  });
  it.skipIf(!canReadSources)('binds every source claim, rejects a fabricated answer and distinguishes roman-letter citations',()=>{
    const output=execFileSync('python3',['-c',`
import json,sys
from pathlib import Path
sys.path.insert(0,'scripts/markbank/authoring')
from ru_verify_review import verify
from ru_review_census import reviewed_keys
from reconcile import parse_ref,match_leaves
cards=[c for c in json.loads(Path('scripts/markbank/authored/russian-reviewed.json').read_text()) if c['year']==2013]
verify(cards)
keys=reviewed_keys(2013,'ol')
for letter in ('a','b'):
    matched=match_leaves(parse_ref('2013 OL Section IR1 Q(ii)('+letter+')'),keys,True)
    assert set(matched)=={('IR1',None,letter,'ii')},matched
c=next(c for c in cards if c['id']=='ru-2013-ol-ir2-ii')
c['rubric']['groups'][1]['rows'][2]['text']='Fabricated extra accepted detail'
try: verify([c])
except AssertionError: pass
else: raise AssertionError('Fabricated answer accepted')
print('Source pools and separate subpart citations verified')
`],{encoding:'utf8'});
    expect(output).toContain('Source pools and separate subpart citations verified');
  });
});
