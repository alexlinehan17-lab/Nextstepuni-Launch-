import { describe, expect, it } from 'vitest';
import { REVIEWED_CARDS } from '../components/MarkBank/cards/russian/reviewed';
import { CARDS as HIGHER } from '../components/MarkBank/cards/russian/higher';
import legacy from '../scripts/markbank/authored/russian.json';
import sources from '../scripts/markbank/authoring/russian-reviewed-sources.json';
import { languageMarks, languageScoreId, languageLengthId, languageFlagId, languageGroupId, languageRowId, languageOtherLanguageId } from '../components/MarkBank/languageScoring';
import { isRubricCard, tariffReconciles } from '../types/markBank';

const sitting = REVIEWED_CARDS.filter(card=>card.year===2025 && card.level==='higher');
const get=(suffix:string)=>{
  const card=sitting.find(card=>card.id===`ru-2025-hl-${suffix}`);
  if(!card || !isRubricCard(card))throw new Error(`Missing rubric ${suffix}`);
  if(card.rubric.system!=='language-writing' && card.rubric.system!=='language-points')throw new Error(`Wrong rubric ${suffix}`);
  return {...card,rubric:card.rubric};
};

describe('Russian 2025 Higher original source review',()=>{
  it('covers all43 independently counted tasks and corrects16 original identities in place',()=>{
    expect(sitting).toHaveLength(43);
    expect(sitting.every(tariffReconciles)).toBe(true);
    expect(sitting.reduce((sum,c)=>sum+c.totalMarks,0)).toBe(320);
    expect(sitting.filter(c=>c.audioMaterial)).toHaveLength(22);
    expect(sitting.filter(c=>c.audioMaterial).reduce((sum,c)=>sum+c.totalMarks,0)).toBe(80);
    const old=legacy.filter(c=>c.year===2025 && c.level==='higher');
    expect(old).toHaveLength(16);
    expect(old.every(c=>HIGHER.filter(x=>x.id===c.id).length===1)).toBe(true);
    expect(sources.filter(c=>c.year===2025 && c.level==='higher' && 'correctsExisting' in c && c.correctsExisting)).toHaveLength(16);
    expect(sitting.filter(c=>c.qa?.gates.includes('reviewed-card-correction'))).toHaveLength(16);
  });
  it('retains all35 printed education terms and the actual15-by2 grammar tariff',()=>{
    const education=get('la1-i'), grammar=get('gr');
    if(education.rubric.system!=='language-points'||grammar.rubric.system!=='language-points')throw new Error('Wrong task rubric');
    expect(education.rubric.groups).toHaveLength(35);
    expect(education.rubric.count).toBe(5);
    expect(education.rubric.groups.some(g=>g.rows.some(r=>r.text==='достижения (спортивные, академические)'))).toBe(true);
    expect(education.rubric.groups.some(g=>g.rows.some(r=>r.text==='школьные (дни, двери)'))).toBe(true);
    expect(grammar.rubric.groups).toHaveLength(15);
    const scores:Record<string,number>={};
    for(const group of grammar.rubric.groups){scores[languageGroupId(group.id)]=1;scores[languageRowId(group.id,'full')]=1;}
    expect(languageMarks(grammar,scores)).toBe(30);
  });
  it('prices each summary10 and enforces two details from each named heading',()=>{
    for(const n of [1,2,3,4])expect(get(`c2-${n}`).totalMarks).toBe(10);
    const card=get('c2-2');
    const scores:Record<string,number>={ [languageGroupId('advantages')]:1,[languageScoreId('summary-skills')]:2 };
    for(const n of [1,2,3,4])scores[languageRowId('advantages',`detail-${n}`)]=2;
    expect(languageMarks(card,scores)).toBe(6);
    expect(languageMarks(card,{...scores,[languageFlagId('incomplete-response')]:1})).toBe(5);
    scores[languageGroupId('disadvantages')]=1;
    scores[languageRowId('disadvantages','detail-1')]=2;
    scores[languageRowId('disadvantages','detail-2')]=1;
    expect(languageMarks(card,scores)).toBe(9);
    scores[languageRowId('disadvantages','detail-2')]=2;
    expect(languageMarks(card,scores)).toBe(10);
    expect(languageMarks(card,{...scores,[languageOtherLanguageId('response')]:1})).toBe(0);
    expect(languageMarks(card,{...scores,[languageOtherLanguageId('row:advantages:detail-1')]:1})).toBe(10);
    expect(card.rubric.system==='language-points' && card.rubric.criteria?.[0].guidance).toContain('speaks two languages since early childhood');
  });
  it('keeps named partial answers claimable without double claiming their full equivalent',()=>{
    const ceremony=get('c1-1-iii');
    const date={ [languageGroupId('answer-1')]:1,[languageRowId('answer-1','partial-1')]:1 };
    expect(languageMarks(ceremony,date)).toBe(1);
    expect(languageMarks(ceremony,{...date,[languageRowId('answer-1','full')]:1})).toBe(2);
    const hotel=get('l1-1-ii');
    const services={ [languageGroupId('answer-1')]:1,[languageRowId('answer-1','partial-1')]:1,
      [languageGroupId('partial-restaurant')]:1,[languageRowId('partial-restaurant','partial')]:1 };
    expect(languageMarks(hotel,services)).toBe(2);
    expect(languageMarks(hotel,{...services,[languageRowId('answer-1','full')]:1})).toBe(3);
    expect(hotel.rubric.markingGuideNote).toContain('does not assign it to a particular full answer');
  });
  it('preserves the published writing pools, deduction order and limits',()=>{
    const essay=get('se'), writing=get('gw');
    expect(essay.questionText.split('\n').filter(l=>l.startsWith('• '))).toHaveLength(5);
    expect(essay.questionText).toContain('Климат в России');
    expect(writing.questionText).toContain('professional tour guide');
    expect(writing.sourceMaterial?.pages).toEqual([13]);
    const scores={ [languageScoreId('content')]:6,[languageScoreId('title-penalty')]:1,
      [languageScoreId('expression')]:20,[languageLengthId('words')]:50 };
    expect(languageMarks(essay,scores)).toBe(25);
    expect(languageMarks(essay,{...scores,[languageScoreId('content')]:4})).toBe(17);
    expect(languageMarks(essay,{...scores,[languageLengthId('words')]:24})).toBe(19);
    expect(languageMarks(essay,{...scores,[languageScoreId('content')]:0})).toBe(0);
    const guided={ [languageScoreId('content')]:15,[languageScoreId('expression')]:15,
      [languageScoreId('coherence')]:10,[languageLengthId('words')]:140 };
    expect(languageMarks(writing,guided)).toBe(40);
    expect(languageMarks(writing,{...guided,[languageLengthId('words')]:59})).toBe(35);
    expect(languageMarks(writing,{...guided,[languageScoreId('content')]:7})).toBe(27);
    expect(languageMarks(writing,{...guided,[languageOtherLanguageId('response')]:1})).toBe(0);
  });
  it('follows booklet addresses, retains the bottom-of-page accepted answer and scopes language rules',()=>{
    expect(get('l1-3-ii').rubric.markingGuideNote).toContain('4(ii)');
    expect(get('l2-1').rubric.markingGuideNote).toContain('1(i)');
    const legacyCard=get('l4-3');
    expect(legacyCard.rubric.markingGuideNote).toContain('3(i)');
    expect(legacyCard.rubric.system==='language-points' && legacyCard.rubric.groups.some(g=>g.rows.some(r=>r.text==='ordinary life can be interesting for readers'))).toBe(true);
    expect(sitting.filter(c=>c.answerLanguageRule)).toHaveLength(18);
    expect(get('la1-ii').answerLanguageRule).toBeUndefined();
    expect(get('la2-ii').answerLanguageRule).toBeUndefined();
    expect(get('sd').answerLanguageRule).toBeUndefined();
    expect(sitting.filter(c=>c.audioMaterial).every(c=>!c.answerLanguageRule)).toBe(true);
  });
});
