import { describe, expect, it } from 'vitest';
import { execFileSync } from 'node:child_process';
import { existsSync } from 'node:fs';
import { REVIEWED_CARDS } from '../components/MarkBank/cards/russian/reviewed';
import { languageMarks, languageScoreId, languageGroupId, languageRowId } from '../components/MarkBank/languageScoring';
import { isRubricCard, tariffReconciles } from '../types/markBank';
import { marksClaimed } from '../components/MarkBank/SessionScreen';

const sitting=REVIEWED_CARDS.filter(c=>c.year===2014&&c.level==='ordinary');
const get=(suffix:string)=>{
  const c=sitting.find(c=>c.id===`ru-2014-ol-${suffix}`);
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
    return ['papers/2014-ol-000-paper.pdf','schemes/2014-ol.pdf','schemes/2015-ol.pdf'].every(p=>existsSync(`examiner-reports/russian/${p}`));
  } catch { return false; }
})();

describe('Russian 2014 Ordinary source review',()=>{
  it('covers the independent 50-task census with 220 written and 100 listening marks',()=>{
    expect(sitting).toHaveLength(50);
    expect(sitting.filter(c=>!tariffReconciles(c)).map(c=>c.id)).toEqual([]);
    expect(sitting.reduce((sum,c)=>sum+c.totalMarks,0)).toBe(320);
    expect(sitting.filter(c=>c.audioMaterial)).toHaveLength(20);
    expect(sitting.filter(c=>c.audioMaterial).reduce((sum,c)=>sum+c.totalMarks,0)).toBe(100);
    expect(sitting.every(c=>!c.answerLanguageRule)).toBe(true);
  });
  it('retains full and partial reading pools under their printed quotas',()=>{
    const c=points('ir2-i');
    expect(c.rubric.groups).toHaveLength(7);
    expect(languageMarks(c,selected('partial-1','partial'))).toBe(1);
    expect(languageMarks(c,{...selected('answer-1','full',2),...selected('partial-1','partial')})).toBe(2);
    expect(points('ir1-iii').rubric.groups).toHaveLength(16);
    const dates=points('ir2-iii');
    expect(dates.rubric.groups).toHaveLength(3);
    expect(dates.rubric.groups[1].rows[0].text).toBe('1/12/2014-1/04/2015-submission of the posters');
    expect(languageMarks(dates,Object.assign({},...dates.rubric.groups.map(g=>selected(g.id,'full',2))))).toBe(4);
  });
  it('keeps the school starting time as one two-mark answer with the general partial scale',()=>{
    const c=points('cd-2-i');
    expect(c.rubric.groups).toHaveLength(1);
    expect(c.rubric.groups[0].rows[0].text).toBe('half past + eight');
    expect(languageMarks(c,selected('answer-1','full',1))).toBe(1);
    expect(languageMarks(c,selected('answer-1','full',2))).toBe(2);
  });
  it('scores the paper’s explicit 3 + 3 handwriting allocation without invented classification prices',()=>{
    const c=get('la1'),d=get('la2');
    if(!isRubricCard(c)||c.rubric.system!=='language-writing'||isRubricCard(d))throw new Error('Wrong card');
    expect(c.rubric.criteria.map(r=>r.maxMarks)).toEqual([3,3]);
    expect(languageMarks(c,{[languageScoreId('formation')]:3,[languageScoreId('transcription')]:2})).toBe(5);
    expect(d.rows.map(r=>r.verbatim)).toEqual(['Адрес','Категории','Поколение','Почта','Язык','возрастные','домашний','молодое','русский','электронная']);
    expect(d.tariffModel).toEqual({kind:'questionTotal'});
    expect(d.rows.every(r=>r.marks===null)).toBe(true);
    expect(marksClaimed(d,Object.fromEntries(d.rows.map(r=>[r.id,1])))).toBe(0);
  });
  it('keeps the source’s swapped final matching answers as two complete routes',()=>{
    const c=get('mm');if(isRubricCard(c))throw new Error('Wrong card');
    expect(c.answerVariants).toHaveLength(2);
    expect(c.tariffModel).toEqual({kind:'fixed'});
    expect(c.taskGroups).toHaveLength(10);
    expect(c.taskGroups?.every(g=>g.marks===4&&g.rowIds.length===1)).toBe(true);
    const [a,b]=c.answerVariants!;
    expect(a.rows.slice(-2).map(r=>r.verbatim)).toEqual(['Юрист','Президент России']);
    expect(b.rows.slice(-2).map(r=>r.verbatim)).toEqual(['Президент России','Юрист']);
    for(const route of c.answerVariants!){
      expect(route.rows).toHaveLength(10);
      expect(route.rows.some(r=>r.verbatim==='Стать пилотом')).toBe(false);
      expect(marksClaimed({...c,rows:route.rows},Object.fromEntries(route.rows.map(r=>[r.id,1])))).toBe(40);
    }
  });
  it('retains the one-mark discourse alternative and three-mark listening partial without double credit',()=>{
    const discourse=points('sd'),listening=points('l2-2-ii');
    expect(languageMarks(discourse,selected('answer-3','partial-1'))).toBe(1);
    expect(languageMarks(discourse,{...selected('answer-3'),...selected('answer-3','partial-1')})).toBe(2);
    expect(languageMarks(discourse,Object.assign({},...discourse.rubric.groups.map(g=>selected(g.id))))).toBe(20);
    expect(languageMarks(listening,selected('answer-1','partial'))).toBe(3);
    expect(languageMarks(listening,{...selected('answer-1'),...selected('answer-1','partial')})).toBe(5);
    expect(listening.questionText).toContain('d. A helmet');
    expect(listening.rubric.taskRequirements).toContain('There is no penalty for excess material which does not invalidate the answer.');
  });
  it('keeps all cultural/writing choices and the original unmodified expression tariff',()=>{
    const c=get('sa'),e=get('ew');if(!isRubricCard(c)||!isRubricCard(e))throw new Error('Wrong cards');
    expect(c.questionText).toContain('TWO of the following questions');
    expect(c.questionText).toContain('Name three famous');
    expect(e.questionText).toContain('Write him/her a birthday card.');
    expect(languageMarks(c,{[languageScoreId('first-content')]:12,[languageScoreId('first-coherence')]:3})).toBe(15);
    expect(languageMarks(e,{[languageScoreId('content')]:6,[languageScoreId('expression')]:12,[languageScoreId('coherence')]:6})).toBe(24);
  });
  it.skipIf(!canReadSources)('derives Cyrillic from original glyph IDs and rejects a fabricated source answer',()=>{
    const output=execFileSync('python3',['-c',`
import hashlib, json, sys, fitz
from pathlib import Path
sys.path.insert(0,'scripts/markbank/authoring')
from ru_source_text import open_scheme, SCHEME_HASH
from ru_verify_review import verify
path=Path('examiner-reports/russian/schemes/2014-ol.pdf')
with open_scheme(2014,'ol') as doc:
    assert 'Ленинградский государственный университет им. А. А. Жданова' in doc[5].get_text()
    assert 'assign one mark for Сколько' in doc[6].get_text()
assert hashlib.sha256(path.read_bytes()).hexdigest()==SCHEME_HASH
with open_scheme(2015,'ol') as repaired, fitz.open('examiner-reports/russian/schemes/2015-ol.pdf') as raw:
    assert [p.get_text() for p in repaired]==[p.get_text() for p in raw]
c=next(c for c in json.loads(Path('scripts/markbank/authored/russian-reviewed.json').read_text()) if c['id']=='ru-2014-ol-sd')
verify([c])
c['rubric']['groups'][2]['rows'][1]['text']='Невозможный выдуманный ответ'
try: verify([c])
except AssertionError: pass
else: raise AssertionError('Fabricated answer accepted')
print('Original glyphs verified; fabricated answer rejected')
`],{encoding:'utf8'});
    expect(output).toContain('Original glyphs verified; fabricated answer rejected');
  });
});
