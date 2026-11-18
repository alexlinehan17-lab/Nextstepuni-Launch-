import { describe, expect, it } from 'vitest';
import { execFileSync } from 'node:child_process';
import { existsSync } from 'node:fs';
import { REVIEWED_CARDS } from '../components/MarkBank/cards/russian/reviewed';
import { languageMarks, languageScoreId, languageGroupId, languageRowId } from '../components/MarkBank/languageScoring';
import { isRubricCard, tariffReconciles } from '../types/markBank';

const sitting=REVIEWED_CARDS.filter(c=>c.year===2011&&c.level==='ordinary');
const get=(suffix:string)=>{
  const c=sitting.find(c=>c.id===`ru-2011-ol-${suffix}`);
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
    return ['papers/2011-ol-000-paper.pdf','papers/2011-ol-A00-paper.pdf','schemes/2011-ol.pdf'].every(p=>existsSync(`examiner-reports/russian/${p}`));
  } catch { return false; }
})();

describe('Russian 2011 Ordinary source review',()=>{
  it('covers the independent 26 written and 16 listening tasks with printed totals',()=>{
    expect(sitting).toHaveLength(42);
    expect(sitting.filter(c=>!tariffReconciles(c)).map(c=>c.id)).toEqual([]);
    expect(sitting.reduce((sum,c)=>sum+c.totalMarks,0)).toBe(320);
    expect(sitting.filter(c=>c.audioMaterial)).toHaveLength(16);
    expect(sitting.filter(c=>c.audioMaterial).reduce((sum,c)=>sum+c.totalMarks,0)).toBe(100);
    expect(sitting.every(c=>!c.answerLanguageRule)).toBe(true);
  });
  it('preserves all six festival entries and the unresolved six-mark total without an invented split',()=>{
    const c=get('ir1-i');if(isRubricCard(c))throw new Error('Expected total-only card');
    expect(c.totalMarks).toBe(6);
    expect(c.tariffModel).toEqual({kind:'questionTotal'});
    expect(c.rows.map(r=>r.verbatim)).toEqual(["20.00o'clock",'25th of August','2006',"18.00o'clock",'27th of August','2006']);
    expect(c.rows.every(r=>r.marks===null&&!r.group)).toBe(true);
    expect(c.rows[0].contextNote).toContain('No one-mark allocation or choose-three rule is inferred');
    expect(c.rows[0].contextNote).toContain('numeric self-scoring is unavailable');
  });
  it('retains all retrieval pools and the printed quota rather than inferred semantic exclusions',()=>{
    expect(['ii','iii','iv','v','vi','vii','viii','ix'].map(r=>points(`ir1-${r}`).rubric.groups.length)).toEqual([4,1,6,6,5,2,4,1]);
    expect(['i','ii','iii','iv'].map(r=>points(`ir2-${r}`).rubric.groups.length)).toEqual([7,7,9,9]);
    const c=points('ir2-iv');
    expect(languageMarks(c,Object.assign({},...c.rubric.groups.map(g=>selected(g.id,'full',2))))).toBe(10);
    expect(languageMarks(c,selected('answer-1','full',1))).toBe(1);
    expect(points('ir2-i').rubric.groups.slice(3,5).map(g=>g.rows[0].text)).toEqual(['woods','forest']);
  });
  it('keeps TV as a partial of the mother detail and retains the final answer below the former crop boundary',()=>{
    const c=points('cd-1-i');
    expect(languageMarks(c,selected('answer-3','partial-1'))).toBe(1);
    expect(languageMarks(c,{...selected('answer-3','full',2),...selected('answer-3','partial-1')})).toBe(2);
    expect(languageMarks(c,{...selected('answer-3','partial-1'),...selected('answer-2','full',2)})).toBe(3);
    expect(points('cd-5-ii').rubric.groups.at(-1)?.rows[0].text).toBe('more than James Bond’s films');
    expect(get('cd-2').questionRef).toBe('2011 OL Section CD Q2');
    expect(points('cd-2').rubric.markingGuideNote).toContain('scheme labels it 2.i');
  });
  it('preserves each matching field and both concert gaps without extra answer routes',()=>{
    const m=points('mm'),d=points('sd');
    expect(m.rubric.groups.map(g=>g.rows[0].text.split(' — ')[0])).toEqual(['10','3','9','8','5','4','7','2','6','1']);
    expect(languageMarks(m,Object.assign({},...m.rubric.groups.map(g=>selected(g.id))))).toBe(40);
    expect(d.rubric.groups.map(g=>g.rows[0].text)).toEqual(['как','кто','что','где','когда','сколько','где','какие','сколько','почему']);
    expect(languageMarks(d,Object.assign({},...d.rubric.groups.map(g=>selected(g.id))))).toBe(20);
    expect(d.sourceMaterial?.pages).toEqual([10,11]);
    expect(d.questionText).toContain('Off The Dark');
  });
  it('keeps four open grammar categories, six culture topics and three complete writing choices',()=>{
    expect(writing('la2').rubric.criteria.map(c=>c.maxMarks)).toEqual([2,2,2,2]);
    expect(writing('la2').rubric.markingGuideNote).toContain('no closed answer list');
    const c=writing('sa'),e=writing('ew');
    expect(c.questionText).toContain('6. Российско-Ирландские отношения');
    expect(e.questionText).toContain('suggest when it would be good for him/her to visit and why');
    expect(languageMarks(c,{[languageScoreId('first-content')]:12,[languageScoreId('first-coherence')]:3})).toBe(15);
    expect(languageMarks(e,{[languageScoreId('content')]:6,[languageScoreId('expression')]:12,[languageScoreId('coherence')]:6})).toBe(24);
  });
  it('keeps all three published birthday details under the explicit two-detail quota',()=>{
    const c=points('l4-1');
    expect(c.questionText).toBe('When and where was Dasha born? Give two details.');
    expect(c.rubric.groups.map(g=>g.rows[0].text)).toEqual(['17th of May','1992','Moscow']);
    expect(languageMarks(c,{...selected('answer-1'),...selected('answer-2')})).toBe(10);
    expect(languageMarks(c,{...selected('answer-1'),...selected('answer-3')})).toBe(10);
    expect(languageMarks(c,Object.assign({},...c.rubric.groups.map(g=>selected(g.id))))).toBe(10);
    expect(c.rubric.markingGuideNote).toContain('no separate one-date/one-place restriction is printed');
    expect(points('l3-2').rubric.groups.map(g=>g.rows[0].text)).toEqual(['5 times daily','high in calories','dairy products','meat','fish','vegetables','fruit','juice','freshly baked pastry']);
    expect(points('l2-3-ii').topicId).toBe('russian-2-3');
  });
  it('retains the source-scoped Russian and excess-material rules visibly',()=>{
    expect(points('ir1-ii').rubric.taskRequirements).toContain('Do not penalise answers supplied in Russian.');
    expect(points('ir1-ii').rubric.taskRequirements).toContain('Where a candidate uses the same information in response to two or more questions, accept the first answer only.');
    expect(points('l1-2').rubric.taskRequirements).toContain('There is no penalty for excess material which does not invalidate the answer.');
    expect(points('l1-2').rubric.taskRequirements).toContain('Award five marks for each correct/relevant point.');
  });
  it.skipIf(!canReadSources)('binds all accepted answers to the original sources and rejects a fabricated extra detail',()=>{
    const output=execFileSync('python3',['-c',`
import json,sys
from pathlib import Path
sys.path.insert(0,'scripts/markbank/authoring')
from ru_verify_review import verify
from ru_review_census import reviewed_keys
from reconcile import parse_ref,match_leaves
cards=[c for c in json.loads(Path('scripts/markbank/authored/russian-reviewed.json').read_text()) if c['year']==2011]
verify(cards)
keys=reviewed_keys(2011,'ol');assert len(keys)==42
assert set(match_leaves(parse_ref('2011 OL Section CD Q2'),keys,True))=={('CD',2,None,None)}
c=next(c for c in cards if c['id']=='ru-2011-ol-l4-1')
c['rubric']['groups'][0]['rows'][0]['text']='Fabricated birth date'
try: verify([c])
except AssertionError: pass
else: raise AssertionError('Fabricated answer accepted')
print('Source pools and exact booklet citation verified')
`],{encoding:'utf8'});
    expect(output).toContain('Source pools and exact booklet citation verified');
  });
});
