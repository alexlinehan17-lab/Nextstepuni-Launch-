import { describe, expect, it } from 'vitest';
import { REVIEWED_CARDS } from '../components/MarkBank/cards/russian/reviewed';
import { CARDS as HIGHER } from '../components/MarkBank/cards/russian/higher';
import legacy from '../scripts/markbank/authored/russian.json';
import { languageMarks, languageScoreId, languageLengthId, languageFlagId, languageGroupId, languageRowId, languageOtherLanguageId } from '../components/MarkBank/languageScoring';
import { isRubricCard, tariffReconciles } from '../types/markBank';

const sitting=REVIEWED_CARDS.filter(card=>card.year===2022 && card.level==='higher');
const get=(suffix:string)=>{
  const card=sitting.find(card=>card.id===`ru-2022-hl-${suffix}`);
  if(!card || !isRubricCard(card))throw new Error(`Missing rubric ${suffix}`);
  if(card.rubric.system!=='language-writing' && card.rubric.system!=='language-points')throw new Error(`Wrong rubric ${suffix}`);
  return {...card,rubric:card.rubric};
};
const selected=(group:string,row='full',value=1)=>({[languageGroupId(group)]:1,[languageRowId(group,row)]:value});

describe('Russian 2022 Higher original source review',()=>{
  it('covers the independent 44-task census and preserves all 14 corrected identities',()=>{
    expect(sitting).toHaveLength(44);
    expect(sitting.every(tariffReconciles)).toBe(true);
    expect(sitting.reduce((sum,c)=>sum+c.totalMarks,0)).toBe(320);
    const listening=sitting.filter(c=>c.audioMaterial);
    expect(listening).toHaveLength(23);
    expect(listening.reduce((sum,c)=>sum+c.totalMarks,0)).toBe(80);
    const old=legacy.filter(c=>c.year===2022 && c.level==='higher');
    expect(old).toHaveLength(14);
    expect(old.every(c=>HIGHER.filter(x=>x.id===c.id).length===1)).toBe(true);
    expect(sitting.filter(c=>c.qa?.gates.includes('reviewed-card-correction'))).toHaveLength(14);
    expect(get('c1-1-i').sourceMaterial?.presentationNote).toContain('170 written marks');
    expect(get('c1-1-i').sourceMaterial?.presentationNote).toContain('choose Question 1 or Question 2');
  });
  it('retains each printed comprehension pool and no-credit wording',()=>{
    const pools=['c1-1-i','c1-1-ii','c1-1-iii','c1-2-i','c1-2-ii','c1-3-i','c1-3-ii','c1-3-iii','c1-4'].map(suffix=>get(suffix));
    expect(pools.map(c=>c.rubric.system==='language-points' ? c.rubric.groups.length : 0)).toEqual([9,11,3,6,4,7,1,5,6]);
    const budget=get('c1-3-iii');
    if(budget.rubric.system!=='language-points')throw new Error('Wrong rubric');
    expect(budget.rubric.groups[0].rows[0].text).toBe('He looks for an answer to 3 questions: when/where from/who to fly with');
    expect(languageMarks(budget,selected('answer-1'))).toBe(2);
    expect(budget.rubric.taskRequirements.join(' ')).toContain('assign no marks: flies without luggage');
    expect(languageMarks(budget,Object.assign({},...budget.rubric.groups.map(g=>selected(g.id))))).toBe(6);
  });
  it('prices summaries as four details plus discretion with real source caps',()=>{
    const cards=[1,2,3,4].map(n=>get(`c2-${n}`));
    expect(cards.map(c=>c.rubric.system==='language-points' ? c.rubric.groups.length : 0)).toEqual([18,16,15,22]);
    const card=cards[0],scores={...selected('answer-1','full',2),...selected('answer-2','full',2),
      ...selected('answer-3','full',2),...selected('answer-4','full',1),[languageScoreId('summary-skills')]:2};
    expect(languageMarks(card,scores)).toBe(9);
    expect(languageMarks(card,{...scores,[languageRowId('answer-4','full')]:2})).toBe(10);
    expect(languageMarks(card,{...scores,[languageFlagId('incomplete-response')]:1})).toBe(8);
    expect(languageMarks(card,{...scores,[languageOtherLanguageId('response')]:1})).toBe(0);
  });
  it('preserves the 33-term vocabulary pool and both five-row case/matching tables',()=>{
    const vocabulary=get('la2-i'),matching=get('la1-ii'),cases=get('la2-ii');
    if(vocabulary.rubric.system!=='language-points'||matching.rubric.system!=='language-points'||cases.rubric.system!=='language-points')throw new Error('Wrong rubric');
    expect(vocabulary.rubric.groups).toHaveLength(33);
    expect(vocabulary.rubric.groups.at(-1)?.rows[0].text).toBe('Факультет');
    expect(languageMarks(vocabulary,Object.assign({},...vocabulary.rubric.groups.map(g=>selected(g.id))))).toBe(10);
    expect(matching.rubric.groups).toHaveLength(5);
    expect(matching.rubric.taskRequirements).toContain('You may write your answer in Irish, English or Russian.');
    expect(cases.rubric.groups).toHaveLength(5);
    expect(cases.rubric.groups[2].rows[0].text).toContain('(выучить) алфавит — Accusative case/винительный падеж');
    expect(get('sd').questionText).toContain('newspaper section');
  });
  it('keeps 14 grammar gaps but 15 separately priced forms including both words in one phrase',()=>{
    const grammar=get('gr');
    if(grammar.rubric.system!=='language-points')throw new Error('Wrong rubric');
    expect(grammar.rubric.groups).toHaveLength(14);
    expect(grammar.rubric.groups.flatMap(g=>g.rows)).toHaveLength(15);
    const phrase=grammar.rubric.groups[10];
    expect(phrase.answerCount).toBe(2);
    expect(phrase.rows.map(r=>r.text)).toEqual(['близкими','людьми']);
    const scores=Object.assign({},...grammar.rubric.groups.flatMap(g=>g.rows.map(r=>selected(g.id,r.id))));
    expect(languageMarks(grammar,scores)).toBe(30);
    expect(languageMarks(grammar,{...scores,[languageOtherLanguageId('row:answer-11:form-1')]:1})).toBe(28);
    expect(languageMarks(grammar,selected('answer-11','form-1'))).toBe(2);
    expect(languageMarks(grammar,{...selected('answer-11','form-1'),...selected('answer-11','form-2')})).toBe(4);
  });
  it('retains the listening NB qualifications, printed quota and Russian exception',()=>{
    const school=get('l2-1-ii');
    if(school.rubric.system!=='language-points')throw new Error('Wrong rubric');
    expect(school.rubric.groups).toHaveLength(6);
    expect(school.rubric.groups[3].rows[0].text).toContain('must mention ‘liked’');
    expect(school.rubric.groups[4].rows[0].text).toContain('not enough just to mention that there were Russian speaking children');
    expect(school.rubric.taskRequirements).toContain('Award no marks: Russian school');
    expect(languageMarks(school,Object.assign({},...school.rubric.groups.map(g=>selected(g.id))))).toBe(6);
    for(const card of sitting.filter(c=>c.audioMaterial)) {
      if(!isRubricCard(card)||card.rubric.system!=='language-points')throw new Error('Wrong listening rubric');
      expect(card.rubric.taskRequirements).toContain('Accept answers written in Russian.');
      expect(card.rubric.taskRequirements.join(' ')).toContain('no penalty for excess material');
      expect(card.rubric.taskRequirements.join(' ')).not.toContain('contradictory');
      expect(card.answerLanguageRule).toBeUndefined();
    }
    expect(get('l4-3-ii').questionText).not.toContain('Rúisis');
  });
  it('uses the full writing choices and the source expression limits',()=>{
    const essay=get('se'),writing=get('gw');
    expect(essay.questionText.split('\n').filter(l=>l.startsWith('• '))).toHaveLength(5);
    expect(essay.questionText).toContain('Русский язык в Ирландии');
    expect(writing.questionText).toContain('being an influencer as a career');
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
  });
  it('applies wrong-language controls only to 18 source-mandated written tasks',()=>{
    expect(sitting.filter(c=>c.answerLanguageRule)).toHaveLength(18);
    for(const suffix of ['la1-ii','la2-ii','sd'])expect(get(suffix).answerLanguageRule).toBeUndefined();
    expect(get('c1-1-i').rubric.markingGuideNote).toContain('English or Irish');
  });
});
