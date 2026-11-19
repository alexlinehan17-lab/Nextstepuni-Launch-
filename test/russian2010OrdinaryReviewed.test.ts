import { describe, expect, it } from 'vitest';
import { execFileSync } from 'node:child_process';
import { existsSync } from 'node:fs';
import { REVIEWED_CARDS } from '../components/MarkBank/cards/russian/reviewed';
import { languageMarks, languageScoreId, languageGroupId, languageRowId } from '../components/MarkBank/languageScoring';
import { isRubricCard, tariffReconciles } from '../types/markBank';

const sitting=REVIEWED_CARDS.filter(c=>c.year===2010&&c.level==='ordinary');
const get=(suffix:string)=>{
  const c=sitting.find(c=>c.id===`ru-2010-ol-${suffix}`);
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
    return ['papers/2010-ol-000-paper.pdf','papers/2010-ol-A00-paper.pdf','schemes/2010-ol.pdf'].every(p=>existsSync(`examiner-reports/russian/${p}`));
  } catch { return false; }
})();

describe('Russian 2010 Ordinary source review',()=>{
  it('covers all 24 written and 18 listening tasks with the printed 220 + 100 marks',()=>{
    expect(sitting).toHaveLength(42);
    expect(sitting.filter(c=>!tariffReconciles(c)).map(c=>c.id)).toEqual([]);
    expect(sitting.reduce((sum,c)=>sum+c.totalMarks,0)).toBe(320);
    expect(sitting.filter(c=>c.audioMaterial)).toHaveLength(18);
    expect(sitting.filter(c=>c.audioMaterial).reduce((sum,c)=>sum+c.totalMarks,0)).toBe(100);
    expect(sitting.every(c=>!c.answerLanguageRule)).toBe(true);
  });
  it('preserves every retrieval and comprehension pool, including the complete long summer answers',()=>{
    expect(['i','ii','iii','iv','v','vi','vii'].map(r=>points(`ir1-${r}`).rubric.groups.length)).toEqual([4,9,9,10,7,4,7]);
    expect(['1-i','1-ii','2-i','3','4'].map(r=>points(`cd-${r}`).rubric.groups.length)).toEqual([5,11,15,18,14]);
    const c=points('cd-3');
    expect(languageMarks(c,Object.assign({},...c.rubric.groups.map(g=>selected(g.id,'full',2))))).toBe(10);
    expect(c.rubric.groups.at(-1)?.rows[0].text).toBe('journey took half and hour');
    expect(points('cd-4').rubric.groups[10].rows[0].text).toBe('with whom she keeps in contact');
  });
  it('retains all three club blanks and independently addressed capacity questions',()=>{
    const c=points('ir2-i');
    expect(c.rubric.groups.map(g=>g.rows[0].text)).toEqual(['club','Moscow','Europe']);
    expect(c.questionText.match(/_+/g)).toHaveLength(3);
    expect(languageMarks(c,Object.assign({},...c.rubric.groups.map(g=>selected(g.id,'full',2))))).toBe(6);
    expect(['a','b','c'].map(l=>points(`ir2-ii-${l}`).rubric.groups[0].rows[0].text)).toEqual(['2000 people','3000 people','10,000 people']);
    expect(['a','b','c'].map(l=>get(`ir2-ii-${l}`).totalMarks)).toEqual([2,2,2]);
  });
  it('requires one answer from each named floor instead of allowing five from one floor',()=>{
    const c=points('ir2-iii');
    expect(c.rubric.count).toBe(5);
    expect(c.rubric.groups.map(g=>g.rows.length)).toEqual([4,4,5,5,3]);
    expect(languageMarks(c,{...selected('floor-1','option-1',2),...selected('floor-1','option-2',2)})).toBe(2);
    expect(languageMarks(c,Object.assign({},...c.rubric.groups.map(g=>selected(g.id,'option-1',2))))).toBe(10);
    expect(languageMarks(c,selected('floor-5','option-3',1))).toBe(1);
  });
  it('keeps the English-word allowance and the seven accepted food and drink words',()=>{
    expect(writing('la1').rubric.criteria.map(c=>c.maxMarks)).toEqual([1,1,1,1]);
    expect(writing('la1').rubric.taskRequirements).toContain('ONE mark per correct answer. Do not penalise students who supply appropriate words in English.');
    const c=points('la2');
    expect(c.rubric.groups.map(g=>g.rows[0].text)).toEqual(['ресторан','суши–бар','(кино–)кафе','пивной (ресторан)','бизнес–ланч','бар','Tuborg']);
    expect(languageMarks(c,Object.assign({},...c.rubric.groups.map(g=>selected(g.id))))).toBe(4);
  });
  it('preserves ten matching answers and the double-gap dialogue exchange',()=>{
    const m=points('mm'),d=points('sd');
    expect(m.rubric.groups.map(g=>g.rows[0].text.split(' — ')[0])).toEqual(['1','10','4','3','6','7','9','5','8','2']);
    expect(languageMarks(m,Object.assign({},...m.rubric.groups.map(g=>selected(g.id))))).toBe(40);
    expect(d.rubric.groups.map(g=>g.rows[0].text)).toEqual(['каком','чем','Какое','Почему','Как','Как','Кто','Когда','как','где']);
    expect(languageMarks(d,Object.assign({},...d.rubric.groups.map(g=>selected(g.id))))).toBe(20);
    expect(d.questionText).toContain('Вас пригласил?');
  });
  it('keeps two cultural responses and the source-specific writing allocation without later quality bands',()=>{
    const c=writing('sa'),e=writing('ew');
    expect(c.questionText).toContain('Российская музыка');
    expect(languageMarks(c,{[languageScoreId('first-content')]:12,[languageScoreId('first-coherence')]:3})).toBe(15);
    expect(e.rubric.criteria.map(c=>c.maxMarks)).toEqual([12,12,6]);
    expect(e.rubric.criteria.slice(0,2).every(c=>!c.bands&&!c.limits)).toBe(true);
    expect(e.rubric.markingGuideNote).toContain('4 x 6 marks');
    expect(e.rubric.taskRequirements[1]).toContain('No marks are awarded for additional information/content');
    expect(languageMarks(e,{[languageScoreId('content')]:12,[languageScoreId('expression')]:12,[languageScoreId('coherence')]:6})).toBe(30);
  });
  it('provides exact fractional awards only under the wholly-Russian listening rule',()=>{
    const c=points('l1-1-ii');
    expect(c.rubric.groups[0].rows.map(r=>r.steps)).toEqual([[0,2.5,5],[0,1,2]]);
    expect(languageMarks(c,selected('answer-1','full',2.5))).toBe(2.5);
    expect(languageMarks(c,selected('answer-1','full',5))).toBe(5);
    expect(languageMarks(c,selected('answer-1','partial',1))).toBe(1);
    expect(languageMarks(c,selected('answer-1','partial',2))).toBe(2);
    expect(languageMarks(c,{...selected('answer-1','full',5),...selected('answer-1','partial',2)})).toBe(5);
    expect(c.rubric.groups.every(g=>g.label.includes('only when the whole answer is in Russian'))).toBe(true);
    expect(c.rubric.markingGuideNote).toContain('Isolated Russian words or expressions do not reduce credit');
    expect(points('ir1-i').rubric.groups[0].rows[0].steps).toEqual([0,1,2]);
    expect(points('ir1-i').rubric.taskRequirements).toContain('Do not penalise answers supplied in Russian.');
  });
  it('retains every listening choice and the two-detail quotas with fractional totals',()=>{
    const c=points('l4-1-i');
    expect(c.rubric.groups).toHaveLength(6);
    expect(languageMarks(c,{...selected('answer-1','full',2.5),...selected('answer-2','full',2.5)})).toBe(5);
    expect(languageMarks(c,Object.assign({},...c.rubric.groups.map(g=>selected(g.id,'full',5))))).toBe(10);
    expect(points('l4-2-ii').rubric.groups.map(g=>g.rows[0].text)).toEqual(['Name','surname','address','post code','phone number']);
  });
  it.skipIf(!canReadSources)('repairs only pinned original glyphs, preserves PDF bytes, and rejects invented answers',()=>{
    const output=execFileSync('python3',['-c',`
import hashlib,json,sys,fitz
from pathlib import Path
sys.path.insert(0,'scripts/markbank/authoring')
from ru_source_text import open_scheme
from ru_verify_review import verify
from ru_review_census import reviewed_keys
from reconcile import parse_ref,match_leaves
p=Path('examiner-reports/russian/schemes/2010-ol.pdf');before=hashlib.sha256(p.read_bytes()).hexdigest()
original=fitz.open(p);repaired=open_scheme(2010,'ol')
assert 'каком' not in original[6].get_text()
for text in ('каком','Вы','давай тебя попробуем'):
    assert text in repaired[6].get_text(),text
assert original[3].get_text()==repaired[3].get_text()
with fitz.open('examiner-reports/russian/schemes/2011-ol.pdf') as untouched:
    assert [p.get_text() for p in untouched]==[p.get_text() for p in open_scheme(2011,'ol')]
assert hashlib.sha256(p.read_bytes()).hexdigest()==before
cards=[c for c in json.loads(Path('scripts/markbank/authored/russian-reviewed.json').read_text()) if c['year']==2010]
verify(cards);keys=reviewed_keys(2010,'ol');assert len(keys)==42
for letter in ('a','b','c'):
    assert set(match_leaves(parse_ref('2010 OL Section IR2 Q(ii)('+letter+')'),keys,True))=={('IR2',None,letter,'ii')}
c=next(c for c in cards if c['id']=='ru-2010-ol-sd');c['rubric']['groups'][0]['rows'][0]['text']='Несуществующий ответ'
try: verify([c])
except AssertionError: pass
else: raise AssertionError('Fabricated answer accepted')
print('Pinned source glyphs, whole pools and independent citations verified')
`],{encoding:'utf8'});
    expect(output).toContain('Pinned source glyphs, whole pools and independent citations verified');
  });
});
