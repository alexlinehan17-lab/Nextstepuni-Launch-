import { describe, expect, it } from 'vitest';
import { REVIEWED_CARDS } from '../components/MarkBank/cards/russian/reviewed';
import { CARDS } from '../components/MarkBank/cards/russian/ordinary';
import legacy from '../scripts/markbank/authored/russian.json';
import { languageMarks, languageScoreId, languageFlagId, languageGroupId, languageRowId } from '../components/MarkBank/languageScoring';
import { isRubricCard, tariffReconciles } from '../types/markBank';

const sitting=REVIEWED_CARDS.filter(c=>c.year===2025 && c.level==='ordinary');
const get=(suffix:string)=>{
  const card=sitting.find(c=>c.id===`ru-2025-ol-${suffix}`);
  if(!card)throw new Error(suffix);
  return card;
};
const points=(suffix:string)=>{
  const card=get(suffix);
  if(!isRubricCard(card)||card.rubric.system!=='language-points')throw new Error(`Missing points rubric ${suffix}`);
  return {...card,rubric:card.rubric};
};

describe('Russian 2025 Ordinary independent source review',()=>{
  it('covers all56 tasks and preserves26 existing identities through explicit corrections',()=>{
    expect(sitting).toHaveLength(56);
    expect(sitting.every(tariffReconciles)).toBe(true);
    expect(sitting.filter(c=>!c.audioMaterial)).toHaveLength(32);
    expect(sitting.filter(c=>c.audioMaterial)).toHaveLength(24);
    expect(sitting.filter(c=>!c.audioMaterial).reduce((n,c)=>n+c.totalMarks,0)).toBe(220);
    expect(sitting.filter(c=>c.audioMaterial).reduce((n,c)=>n+c.totalMarks,0)).toBe(100);
    const old=legacy.filter(c=>c.year===2025 && c.level==='ordinary');
    expect(old).toHaveLength(26);
    expect(old.every(c=>CARDS.filter(x=>x.id===c.id).length===1)).toBe(true);
    expect(sitting.filter(c=>c.qa?.gates.includes('reviewed-card-correction'))).toHaveLength(26);
    expect(sitting.every(c=>!c.answerLanguageRule)).toBe(true);
  });
  it('keeps the complete eight-mark event table and fourth roman subpart',()=>{
    const card=get('ir2-5');
    if(card.kind!=='question')throw new Error('Missing event table');
    expect(card.rows.map(r=>r.contextNote?.split('\n')[0])).toEqual(['Day of the week','Date','Time','Location']);
    expect(card.rows.map(r=>r.marks)).toEqual([2,2,2,2]);
    expect(card.totalMarks).toBe(8);
    expect(get('cd-4-iv').questionRef).toBe('2025 OL Section CD Q4(iv)');
    expect(sitting.filter(c=>c.section==='CD')).toHaveLength(12);
    expect(sitting.filter(c=>c.section==='CD').reduce((n,c)=>n+c.totalMarks,0)).toBe(40);
  });
  it('retains both complete discourse alternatives and all language-awareness choices',()=>{
    const dialogue=get('sd');
    if(dialogue.kind!=='question')throw new Error('Missing dialogue');
    expect(dialogue.answerVariants).toHaveLength(2);
    for(const route of dialogue.answerVariants??[]) {
      expect(route.rows).toHaveLength(5);
      expect(route.rows.reduce((n,r)=>n+(r.marks??0),0)).toBe(20);
    }
    expect(dialogue.questionText).toContain('Group A');
    expect(dialogue.questionText).toContain('Group B');
    expect(points('la1').rubric.groups).toHaveLength(6);
    expect(points('la1').rubric.count).toBe(3);
    const cursive=get('la2');
    if(!isRubricCard(cursive)||cursive.rubric.system!=='language-writing')throw new Error('Missing cursive rubric');
    expect(cursive.rubric.criteria).toHaveLength(3);
    expect(cursive.questionText).toContain('любимое дело');
    expect(cursive.questionText).toContain('международным статусом');
    expect(languageMarks(cursive,{[languageScoreId('phrase-1')]:2,[languageScoreId('phrase-2')]:1})).toBe(3);
  });
  it('prices the named reading and listening partial alternatives separately',()=>{
    const dishes=points('ir1-4-i');
    expect(languageMarks(dishes,{[languageGroupId('answer-1')]:1,[languageRowId('answer-1','partial-1')]:1})).toBe(1);
    const games=points('cd-4-iv');
    const partial=games.rubric.groups.find(g=>g.rows[0].text==='Playing with friends');
    if(!partial)throw new Error('Missing named one-mark answer');
    expect(languageMarks(games,{[languageGroupId(partial.id)]:1,[languageRowId(partial.id,'full')]:1})).toBe(1);
    const hotel=points('l1-1-ii');
    expect(hotel.rubric.count).toBe(1);
    const hotelPartial=hotel.rubric.groups.find(g=>g.rows[0].text==='Gym / Wi-Fi / restaurant');
    if(!hotelPartial)throw new Error('Missing printed two-mark partial pool');
    expect(languageMarks(hotel,{[languageGroupId(hotelPartial.id)]:1,[languageRowId(hotelPartial.id,'full')]:1})).toBe(2);
    expect(languageMarks(hotel,{[languageGroupId('answer-1')]:1,[languageRowId('answer-1','full')]:1})).toBe(3);
  });
  it('retains every separately printed accepted option under the printed listening quota',()=>{
    const booking=points('l1-1-i'), opportunities=points('l2-2-ii');
    expect(booking.rubric.groups).toHaveLength(7);
    expect(opportunities.rubric.groups).toHaveLength(5);
    expect(booking.rubric.count).toBe(2);
    expect(opportunities.rubric.count).toBe(2);
    expect(booking.rubric.groups.flatMap(g=>g.rows.map(r=>r.text))).toContain('Booked from 10 to 12 of January');
    expect(opportunities.rubric.groups.flatMap(g=>g.rows.map(r=>r.text))).toContain('Travel around the world');
    const scores:Record<string,number>={};
    for(const group of booking.rubric.groups){scores[languageGroupId(group.id)]=1;scores[languageRowId(group.id,'full')]=1;}
    expect(languageMarks(booking,scores)).toBe(6);
    expect(booking.rubric.taskRequirements).toContain('There is no penalty for excess material which does not invalidate the answer.');
  });
  it('includes bottom-of-page answers and original multiple-choice options',()=>{
    const food=points('cd-3-ii').rubric.groups.flatMap(g=>g.rows.map(r=>r.text));
    expect(food).toEqual(expect.arrayContaining(['Meat','Ice cream','Mayonnaise','Carrot']));
    expect(get('l1-3-ii').questionText).toContain('Café ‘Meridian’');
    expect(get('l1-3-ii').questionText).toContain('Main Square');
    expect(get('l3-1-ii').questionText).toContain('19 pm');
    expect(points('l4-3-ii').rubric.markingGuideNote).toContain('2(ii)');
    expect(points('l4-3-ii').questionRef).toBe('2025 OL Section L4 Q3(ii)');
  });
  it('uses the complete writing pools and the actual lower-expression boundaries',()=>{
    const card=get('ew');
    if(!isRubricCard(card)||card.rubric.system!=='language-writing')throw new Error('Missing writing rubric');
    for(const choice of ['Concert','Hobby','Postcard'])expect(card.questionText).toContain(choice);
    const scores={[languageScoreId('content')]:12,[languageScoreId('expression')]:12,[languageScoreId('coherence')]:6};
    expect(languageMarks(card,scores)).toBe(30);
    expect(languageMarks(card,{...scores,[languageScoreId('content')]:6})).toBe(21);
    expect(languageMarks(card,{...scores,[languageFlagId('fewer-six-sentences')]:1})).toBe(27);
    const culture=get('sa');
    if(!isRubricCard(culture)||culture.rubric.system!=='language-writing')throw new Error('Missing cultural rubric');
    expect(culture.rubric.criteria[0].permittedMarks).toEqual([0,4,8,12,16,20,24]);
    expect(culture.rubric.criteria[1].permittedMarks).toEqual([0,2,4,6]);
    for(const topic of ['New Year','Transport','Russian cuisine','Holiday destinations','Sport'])expect(culture.questionText).toContain(topic);
  });
});
