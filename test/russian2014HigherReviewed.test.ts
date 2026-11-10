import { describe, expect, it } from 'vitest';
import { REVIEWED_CARDS } from '../components/MarkBank/cards/russian/reviewed';
import { languageMarks, languageScoreId, languageLengthId, languageFlagId, languageGroupId, languageRowId, languageOtherLanguageId } from '../components/MarkBank/languageScoring';
import { isRubricCard, tariffReconciles } from '../types/markBank';
const sitting=REVIEWED_CARDS.filter(c=>c.year===2014&&c.level==='higher');
const get=(suffix:string)=>{const c=sitting.find(c=>c.id===`ru-2014-hl-${suffix}`);if(!c||!isRubricCard(c))throw new Error(suffix);return c;};
const points=(suffix:string)=>{const c=get(suffix);if(c.rubric.system!=='language-points')throw new Error(suffix);return {...c,rubric:c.rubric};};
const writing=(suffix:string)=>{const c=get(suffix);if(c.rubric.system!=='language-writing')throw new Error(suffix);return {...c,rubric:c.rubric};};
const row=(group:string,id='full',value=1)=>({[languageGroupId(group)]:1,[languageRowId(group,id)]:value});
const slot=(id:string,value:number)=>({[languageGroupId(id)]:1,[languageScoreId(id)]:value});

describe('Russian 2014 Higher source allocations',()=>{
  it('retains forty tasks and every local allocation inside the published three hundred',()=>{
    expect(sitting).toHaveLength(40);expect(sitting.filter(c=>!tariffReconciles(c)).map(c=>c.id)).toEqual([]);
    expect(sitting.reduce((s,c)=>s+c.totalMarks,0)).toBe(300);
    expect(sitting.filter(c=>c.audioMaterial)).toHaveLength(20);
    expect(sitting.filter(c=>c.audioMaterial).reduce((s,c)=>s+c.totalMarks,0)).toBe(80);
    expect(sitting.filter(c=>c.id.startsWith('ru-2014-hl-c1-')).reduce((s,c)=>s+c.totalMarks,0)).toBe(38);
    expect(get('la1').totalMarks+get('ca1').totalMarks).toBe(12);
  });
  it('reserves exactly two neighbours-did-not slots while retaining independent partial assessment',()=>{
    const c=points('c1-3-i');expect(c.rubric.count).toBe(3);
    expect(c.rubric.groups.filter(g=>g.id.startsWith('neighbour-'))).toHaveLength(2);
    expect(c.rubric.groups.filter(g=>g.id.startsWith('other-')).every(g=>g.label.includes('exclude the four neighbours-did-not actions'))).toBe(true);
    expect(languageMarks(c,{...slot('neighbour-1',2),...slot('neighbour-2',2)})).toBe(4);
    expect(languageMarks(c,{...slot('neighbour-1',2),...slot('neighbour-2',2),...slot('other-1',1)})).toBe(5);
    expect(languageMarks(c,{...slot('neighbour-1',2),...slot('neighbour-2',2),...slot('other-1',2),...slot('other-2',2)})).toBe(6);
    expect(languageMarks(c,{...slot('other-1',1),...slot('other-2',2)})).toBe(3);
    expect(languageMarks(c,slot('neighbour-1',1))).toBe(0);
    expect(c.rubric.markingGuideNote).toContain('bad/boring partial association is not uniquely specified');
  });
  it('keeps the pool-level good evaluation unpaired and limits the friends partial to one answer',()=>{
    const c=points('c1-1-i');expect(languageMarks(c,{...slot('detail-1',1),...slot('detail-2',2)})).toBe(3);
    expect(c.rubric.markingGuideNote).toContain('Do not count one detail twice');
    const friends=points('c1-1-ii');expect(friends.rubric.count).toBe(1);
    expect(languageMarks(friends,{...row('answer-1'),...row('independent-partial-1','full-1')})).toBe(2);
  });
  it('keeps noun and modifier independent and makes each translation an exclusive phrase route',()=>{
    const c=points('la1');expect(c.rubric.alternativeSets).toHaveLength(6);
    const form={[languageGroupId('phrase-1-russian')]:1,[languageScoreId('phrase-1-modifier')]:1,[languageScoreId('phrase-1-noun')]:0};
    const translation=slot('phrase-1-translation',2);
    expect(languageMarks(c,form)).toBe(1);expect(languageMarks(c,translation)).toBe(2);
    expect(languageMarks(c,{...form,...translation})).toBe(0);
    expect(languageMarks(c,{...translation,...slot('phrase-2-translation',2),...slot('phrase-3-translation',2),...slot('phrase-4-translation',2)})).toBe(6);
    expect(c.answerLanguageRule).toBeUndefined();
  });
  it('keeps cultural detail rates separate from all three permitted response languages',()=>{
    const c=writing('ca1');expect(c.rubric.criteria.map(x=>x.permittedMarks)).toEqual([[0,2],[0,2],[0,2]]);
    expect(languageMarks(c,{[languageScoreId('detail-1')]:2,[languageScoreId('detail-2')]:2,[languageScoreId('detail-3')]:2})).toBe(6);
    expect(c.rubric.markingGuideNote).toContain('English, Irish and Russian are permitted');expect(c.answerLanguageRule).toBeUndefined();
  });
  it('retains all school words, infinitives and matching alternatives without duplicate row credit',()=>{
    expect(points('la2-i').rubric.groups).toHaveLength(13);
    expect(points('la2-ii').rubric.groups.map(g=>g.rows[0].text)).toEqual(['поставить','ответить','стараться','есть','решить']);
    const c=points('sd');expect(c.rubric.groups.map(g=>g.rows.map(r=>r.text))).toEqual([['10','2'],['2','10'],['6'],['1','4'],['7'],['3','4'],['5'],['9'],['4','3','1'],['8']]);
    expect(languageMarks(c,{...row('answer-1','option-1'),...row('answer-1','option-2')})).toBe(2);
    expect(languageMarks(c,{...row('answer-1','option-1'),...row('answer-2','option-2')})).toBe(4);
  });
  it('preserves all fifteen exact original grammar forms',()=>{
    const c=points('gr');expect(c.rubric.groups.map(g=>g.rows[0].text)).toEqual(['отмечают','рождения','был','дня','бабушек','придумывала','кремом','шоколадом','организовываю','моей','целую','Мне','люблю','выбирают','приятных']);
    expect(languageMarks(c,Object.assign({},...c.rubric.groups.map(g=>row(g.id))))).toBe(30);
  });
  it('retains distinct summary slots, intelligible partials, discretion and the explicit names exception',()=>{
    const c=points('c2-2');const score={...slot('detail-1',1),...slot('detail-2',2),[languageScoreId('summary-skills')]:2};
    expect(languageMarks(c,score)).toBe(5);
    expect(languageMarks(c,{...score,[languageFlagId('incomplete-response')]:1})).toBe(4);
    expect(languageMarks(c,{...score,[languageOtherLanguageId('response')]:1})).toBe(2);
    expect(c.rubric.taskRequirements.join(' ')).toContain('Do not deduct a discretionary mark if names are not mentioned');
    expect(c.rubric.markingGuideNote).toContain('an identical fact printed in both lists earns once');
  });
  it('uses the actual non-overlapping Lower A grids and the year-specific soft sign deductions',()=>{
    const se=writing('se'),gw=writing('gw');
    expect(se.rubric.criteria.find(x=>x.id==='soft-sign-penalty')?.permittedMarks).toEqual([0,1,2]);
    expect(gw.rubric.criteria.find(x=>x.id==='soft-sign-penalty')?.permittedMarks).toEqual([0,2]);
    expect(gw.rubric.criteria.find(x=>x.id==='expression')?.limits?.find(x=>x.id==='lower-a')?.bands?.map(b=>b.marks)).toEqual([[11,12],[9,10],[7,8]]);
    const score={[languageScoreId('content')]:15,[languageScoreId('expression')]:6,[languageLengthId('words')]:140,[languageFlagId('lower-a')]:1};
    expect(languageMarks(gw,score)).toBe(15);expect(languageMarks(gw,{...score,[languageScoreId('expression')]:11})).toBe(26);
    expect(gw.rubric.taskRequirements.join(' ')).toContain('When the best time to visit would be');
    expect(gw.rubric.taskRequirements.join(' ')).toContain('Question and Answer 7');
    expect(gw.rubric.markingGuideNote).toContain('does not fully match those lists');
  });
  it('preserves clear place/percentage partials without full-plus-partial double credit',()=>{
    const c=points('l1-2');expect(c.rubric.groups).toHaveLength(5);
    expect(languageMarks(c,row('answer-1','partial-1'))).toBe(1);
    expect(languageMarks(c,{...row('answer-1'),...row('answer-1','partial-1')})).toBe(2);
    expect(languageMarks(c,{...row('answer-1','partial-1'),...row('answer-2','partial-1')})).toBe(2);
  });
  it('keeps the anomalous concert partial under its published band question and the complete event times intact',()=>{
    const c=writing('l1-3-i');expect(c.rubric.taskRequirements.join(' ')).toContain('concert + May + 8:00');
    expect(c.rubric.markingGuideNote).toContain('before the separate upcoming-event question');
    expect(languageMarks(c,{[languageScoreId('detail-1')]:1,[languageScoreId('detail-2')]:2})).toBe(3);
    const event=points('l1-3-ii');expect(event.rubric.groups).toHaveLength(6);
    expect(event.rubric.groups.every(g=>g.rows.every(r=>r.marks===2&&!r.steps))).toBe(true);
  });
  it('retains the open other-section allowance inside the two-detail quota',()=>{
    const c=points('l3-4');expect(c.rubric.groups.filter(g=>g.criteria)).toHaveLength(2);expect(c.rubric.count).toBe(2);
    expect(languageMarks(c,{...row('answer-1'),...slot('other-section-1',2)})).toBe(4);
    expect(languageMarks(c,{...slot('other-section-1',2),...slot('other-section-2',2)})).toBe(4);
    expect(c.rubric.markingGuideNote).toContain('do not repeat a detail already claimed');
    expect(points('l4-3-ii').rubric.groups).toHaveLength(6);
  });
  it('shows the original Russian-answer exception on every listening card',()=>{
    expect(sitting.filter(c=>c.answerLanguageRule)).toHaveLength(17);
    for(const c of sitting.filter(c=>c.audioMaterial)){
      expect(c.answerLanguageRule).toBeUndefined();
      if(!isRubricCard(c)||!['language-writing','language-points'].includes(c.rubric.system))throw new Error(c.id);
      if(c.rubric.system==='language-writing'||c.rubric.system==='language-points')expect(c.rubric.taskRequirements.join(' ')).toContain('Accept answers written in Russian.');
    }
  });
});
