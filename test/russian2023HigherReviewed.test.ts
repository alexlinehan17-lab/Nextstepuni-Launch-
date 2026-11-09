import { execFileSync } from 'node:child_process';
import { existsSync } from 'node:fs';
import { describe, expect, it } from 'vitest';
import { REVIEWED_CARDS } from '../components/MarkBank/cards/russian/reviewed';
import { CARDS as HIGHER } from '../components/MarkBank/cards/russian/higher';
import legacy from '../scripts/markbank/authored/russian.json';
import { languageMarks, languageScoreId, languageLengthId, languageFlagId, languageGroupId, languageRowId, languageOtherLanguageId } from '../components/MarkBank/languageScoring';
import { isRubricCard, tariffReconciles } from '../types/markBank';

const sitting=REVIEWED_CARDS.filter(c=>c.year===2023 && c.level==='higher');
const get=(suffix:string)=>{
  const c=sitting.find(c=>c.id===`ru-2023-hl-${suffix}`);
  if(!c||!isRubricCard(c))throw new Error(`Missing ${suffix}`);
  if(c.rubric.system!=='language-points'&&c.rubric.system!=='language-writing')throw new Error(`Wrong rubric ${suffix}`);
  return {...c,rubric:c.rubric};
};
const selected=(group:string,row='full',value=1)=>({[languageGroupId(group)]:1,[languageRowId(group,row)]:value});

const canReadSources=(()=>{
  try {
    execFileSync('python3',['-c','import fitz'],{stdio:'ignore'});
    return ['papers/2023-hl-000-paper.pdf','papers/2023-hl-A00-paper.pdf','schemes/2023-hl.pdf'].every(p=>existsSync(`examiner-reports/russian/${p}`));
  } catch { return false; }
})();

describe('Russian 2023 Higher original source review',()=>{
  it('covers 41 tasks, preserves all 16 original identities and reconciles the printed totals',()=>{
    expect(sitting).toHaveLength(41);
    expect(sitting.filter(c=>!tariffReconciles(c)).map(c=>c.id)).toEqual([]);
    expect(sitting.reduce((s,c)=>s+c.totalMarks,0)).toBe(320);
    const audio=sitting.filter(c=>c.audioMaterial);
    expect(audio).toHaveLength(20);
    expect(audio.reduce((s,c)=>s+c.totalMarks,0)).toBe(80);
    const old=legacy.filter(c=>c.year===2023&&c.level==='higher');
    expect(old).toHaveLength(16);
    expect(old.every(c=>HIGHER.filter(x=>x.id===c.id).length===1)).toBe(true);
    expect(sitting.filter(c=>c.qa?.gates.includes('reviewed-card-correction'))).toHaveLength(16);
  });
  it('retains the complete printed reading pools and one full-or-partial bike detail',()=>{
    const kolya=get('c1-2-i'),visit=get('c1-4-ii');
    expect(kolya.rubric.system==='language-points'&&kolya.rubric.groups).toHaveLength(11);
    expect(languageMarks(visit,selected('answer-2','partial-1'))).toBe(1);
    expect(languageMarks(visit,{...selected('answer-2','partial-1'),...selected('answer-2')})).toBe(2);
    expect(languageMarks(visit,{...selected('answer-2','partial-1'),...selected('answer-2'),...selected('answer-1')})).toBe(4);
    expect(get('c1-1-i').rubric.taskRequirements.join(' ')).toContain('assign no marks: good');
    expect(get('c1-1-ii').rubric.taskRequirements.join(' ')).toContain('assign no marks: bored');
  });
  it('keeps all plus-separated summary details and applies discretion and intelligible partial rules',()=>{
    expect([1,2,3,4].map(n=>{const c=get(`c2-${n}`);return c.rubric.system==='language-points'?c.rubric.groups.length:0;})).toEqual([16,21,15,16]);
    const c=get('c2-2');
    const scores={...selected('answer-1','full',2),...selected('answer-2','full',2),...selected('answer-3','full',2),...selected('answer-4','full',1),[languageScoreId('summary-skills')]:2};
    expect(languageMarks(c,scores)).toBe(9);
    expect(languageMarks(c,{...scores,[languageFlagId('incomplete-response')]:1})).toBe(8);
    expect(languageMarks(c,{...scores,[languageOtherLanguageId('response')]:1})).toBe(0);
    expect(c.rubric.taskRequirements.join(' ')).toContain('Supply additional details');
  });
  it('keeps 18 music terms and prices 15 forms within 14 grammar gaps',()=>{
    const music=get('la2-ii'),grammar=get('gr');
    if(music.rubric.system!=='language-points'||grammar.rubric.system!=='language-points')throw new Error('Wrong rubric');
    expect(music.rubric.groups).toHaveLength(18);
    expect(music.rubric.count).toBe(5);
    expect(music.rubric.groups.at(-1)?.rows[0].text).toBe('разогрев');
    expect(grammar.rubric.groups).toHaveLength(14);
    expect(grammar.rubric.groups.flatMap(g=>g.rows)).toHaveLength(15);
    const phrase=grammar.rubric.groups[5];
    expect(phrase.rows.map(r=>r.text)).toEqual(['Олимпийском','музеe']);
    expect(languageMarks(grammar,selected(phrase.id,'form-1'))).toBe(2);
    expect(languageMarks(grammar,{...selected(phrase.id,'form-1'),...selected(phrase.id,'form-2')})).toBe(4);
    const scores=Object.assign({},...grammar.rubric.groups.flatMap(g=>g.rows.map(r=>selected(g.id,r.id))));
    expect(languageMarks(grammar,scores)).toBe(30);
    expect(languageMarks(grammar,{...scores,[languageOtherLanguageId('row:answer-6:form-1')]:1})).toBe(28);
  });
  it('enforces the collective country limit and the hockey-only ceiling',()=>{
    const travel=get('l3-1-ii'),hobbies=get('l4-3');
    const countries=Object.assign({},...[1,2,3,4].map(n=>selected('countries',`country-${n}`)));
    expect(languageMarks(travel,countries)).toBe(2);
    expect(languageMarks(travel,{...countries,...selected('answer-1'),...selected('answer-2')})).toBe(6);
    if(hobbies.rubric.system!=='language-points')throw new Error('Wrong rubric');
    expect(hobbies.rubric.allocationCap).toMatchObject({maxMarks:6,answerCount:3,schemePages:[20]});
    const hockey=Object.assign({},...[3,5,6,7,8,9].map(n=>selected('hockey',`detail-${n}`)));
    expect(languageMarks(hobbies,hockey)).toBe(4);
    expect(languageMarks(hobbies,{...hockey,...selected('answer-1')})).toBe(6);
    expect(languageMarks(hobbies,{...hockey,...selected('answer-1'),...selected('answer-2'),...selected('answer-4')})).toBe(6);
    expect(languageMarks(hobbies,{...selected('answer-1'),...selected('answer-2'),...selected('answer-4')})).toBe(6);
    expect(hobbies.rubric.allocationCap?.sourceText).toContain('at least two hobbies');
    expect(travel.rubric.taskRequirements.join(' ')).toContain('Maximum 2 marks can be achieved for naming countries');
  });
  it('keeps the vegetarian context condition and this sitting’s listening guidance',()=>{
    const c=get('l2-2-ii');
    if(c.rubric.system!=='language-points')throw new Error('Wrong rubric');
    expect(c.rubric.groups.at(-1)?.rows[0].text).toBe("she is vegetarian so she doesn't know much yet");
    expect(languageMarks(c,selected('vegetarian-context'))).toBe(2);
    expect(languageMarks(c,{...selected('vegetarian-context'),...selected('answer-2')})).toBe(4);
    const guidance=c.rubric.taskRequirements.join(' ');
    expect(guidance).toContain('if correct context is provided');
    expect(guidance).toContain('no penalty for excess material which does not invalidate the answer');
    expect(guidance).not.toContain('contradictory');
  });
  it('uses normal-first guided bands and the printed writing thresholds',()=>{
    const essay=get('se'),guided=get('gw');
    expect(essay.questionText.split('\n').filter(l=>l.startsWith('• '))).toHaveLength(5);
    expect(essay.questionText).toContain('Транспорт в Российской Федерации');
    expect(guided.questionText).toContain('gifted children face');
    expect(guided.questionText.replace(/\s+/g,' ')).toContain('Russian (140 words) in answer to ONE');
    expect(guided.questionText.replace(/\s+/g,' ')).toContain('graduation. You want to organise a get-together to mark the occasion.');
    if(guided.rubric.system!=='language-writing')throw new Error('Wrong rubric');
    const expression=guided.rubric.criteria.find(c=>c.id==='expression');
    expect(expression?.bands?.map(b=>b.marks.at(-1))).toEqual([15,10,5]);
    expect(expression?.limits?.[0].bands?.map(b=>b.marks.at(-1))).toEqual([10,6,3]);
    const scores={ [languageScoreId('content')]:15,[languageScoreId('expression')]:15,[languageScoreId('coherence')]:10,[languageLengthId('words')]:140 };
    expect(languageMarks(guided,scores)).toBe(40);
    expect(languageMarks(guided,{...scores,[languageLengthId('words')]:59})).toBe(35);
    expect(languageMarks(guided,{...scores,[languageScoreId('content')]:7})).toBe(27);
    const short={ [languageScoreId('content')]:6,[languageScoreId('title-penalty')]:1,[languageScoreId('expression')]:20,[languageLengthId('words')]:50 };
    expect(languageMarks(essay,short)).toBe(25);
    expect(languageMarks(essay,{...short,[languageScoreId('content')]:4})).toBe(17);
    expect(languageMarks(essay,{...short,[languageLengthId('words')]:24})).toBe(19);
    expect(languageMarks(essay,{...short,[languageScoreId('content')]:0})).toBe(0);
  });
  it.skipIf(!canReadSources)('verifies the hockey cap against the original scheme and rejects an invented rule',()=>{
    execFileSync('python3',['-c',`
import copy,sys
sys.path.insert(0,'scripts/markbank/authoring')
from ru_review_2023_hl import build
from ru_verify_review import verify
cards=build();verify(cards)
c=copy.deepcopy(next(c for c in cards if c['id']=='ru-2023-hl-l4-3'))
c['rubric']['allocationCap']['sourceText']='Invented source tariff without documentary support'
try: verify([c])
except AssertionError: pass
else: raise AssertionError('Invented allocation-cap source text was accepted')
`],{stdio:'pipe',timeout:30000});
  });
  it('binds the language rule to the 18 mandated written tasks and preserves exceptions',()=>{
    expect(sitting.filter(c=>c.answerLanguageRule)).toHaveLength(18);
    for(const suffix of ['la1-ii','la2-i','sd'])expect(get(suffix).answerLanguageRule).toBeUndefined();
    expect(get('la1-ii').questionText).toContain('Irish, English or Russian');
    expect(get('la2-ii').answerLanguageRule?.otherLanguageMultiplier).toBe(0);
    expect(get('c1-1-i').rubric.markingGuideNote).toContain('English or Irish');
    expect(sitting.filter(c=>c.audioMaterial).every(c=>!c.answerLanguageRule)).toBe(true);
  });
});
