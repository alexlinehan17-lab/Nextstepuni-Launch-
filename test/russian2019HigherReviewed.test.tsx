import { cleanup, fireEvent, render, screen, waitFor } from '@testing-library/react';
import { afterEach, describe, expect, it, vi } from 'vitest';
import SessionScreen from '../components/MarkBank/SessionScreen';
import LanguageRubricPanel from '../components/MarkBank/LanguageRubricPanel';
import { REVIEWED_CARDS } from '../components/MarkBank/cards/russian/reviewed';
import { languageMarks, languageScoreId, languageGroupId, languageRowId, languageFlagId, languageLengthId, languageOtherLanguageId } from '../components/MarkBank/languageScoring';
import { isRubricCard, tariffReconciles } from '../types/markBank';

const sitting=REVIEWED_CARDS.filter(c=>c.year===2019&&c.level==='higher');
const get=(suffix:string)=>{const card=sitting.find(c=>c.id===`ru-2019-hl-${suffix}`);if(!card)throw new Error(suffix);return card;};
const points=(suffix:string)=>{const card=get(suffix);if(!isRubricCard(card)||card.rubric.system!=='language-points')throw new Error(suffix);return {...card,rubric:card.rubric};};
const writing=()=>{const card=get('gw');if(!isRubricCard(card)||card.rubric.system!=='language-writing')throw new Error('gw');return {...card,rubric:card.rubric};};
const essay=()=>{const card=get('se');if(!isRubricCard(card)||card.rubric.system!=='language-writing')throw new Error('se');return {...card,rubric:card.rubric};};
const slot=(n:number,value:number)=>({[languageGroupId(`detail-${n}`)]:1,[languageScoreId(`detail-${n}-credit`)]:value});
const row=(id:string)=>({[languageGroupId(id)]:1,[languageRowId(id,'full')]:1});
afterEach(cleanup);

describe('Russian 2019 Higher approved individual questions and source marks',()=>{
  it('represents all 44 printed asks individually with approved marks',()=>{
    expect(sitting).toHaveLength(44);expect(sitting.filter(c=>c.audioMaterial)).toHaveLength(24);
    expect(sitting.every(tariffReconciles)).toBe(true);
    expect(sitting.filter(isRubricCard).reduce((sum,c)=>sum+c.totalMarks,0)).toBe(300);
    expect(sitting.filter(c=>!isRubricCard(c)).reduce((sum,c)=>sum+c.totalMarks,0)).toBe(0);
    expect(sitting.filter(c=>c.answerLanguageRule)).toHaveLength(17);
  });
  it('caps only a repeated credited detail, preserving the other response and saved raw choices',()=>{
    const card=points('c1-2-ii'),saved={...slot(1,2),...slot(2,2)};
    const first=languageFlagId('detail-1-already-credited'),second=languageFlagId('detail-2-already-credited');
    expect(languageMarks(card,saved)).toBe(4);
    expect(languageMarks(card,{...saved,[first]:1})).toBe(2);
    expect(languageMarks(card,{...saved,[second]:1})).toBe(2);
    expect(languageMarks(card,{...saved,[first]:1,[second]:1})).toBe(0);
    const restored=JSON.parse(JSON.stringify({...saved,[first]:1}));
    expect(languageMarks(card,restored)).toBe(2);
    expect(languageMarks(card,{...restored,[first]:0})).toBe(4);
    expect(languageMarks(points('c1-2-i'),{...saved,...slot(3,2),...slot(4,2)})).toBe(8);
  });
  it('renders both independent repeat controls with the original highest-credit guidance',()=>{
    const onScore=vi.fn();render(<LanguageRubricPanel card={points('c1-2-ii')} scores={{...slot(1,2),...slot(2,2)}} onScore={onScore}/>);
    const controls=screen.getAllByRole('checkbox',{name:'This detail was already credited in Question 2(i).'});
    expect(controls).toHaveLength(2);expect(controls.every(c=>!c.hasAttribute('disabled'))).toBe(true);
    fireEvent.click(controls[0]);expect(onScore).toHaveBeenCalledWith(languageFlagId('detail-1-already-credited'),1);
    expect(screen.getAllByText(/accept the one which gives the candidate the most marks/)[0]).toBeVisible();
    expect(screen.getAllByText(/it cannot be awarded marks again/)[0]).toBeVisible();
  });
  it('keeps the printed intelligible partial and manual discretion exception with the incomplete cap',()=>{
    const card=points('c2-1'),saved={...slot(1,1),...slot(2,2),...slot(3,2),...slot(4,2),[languageScoreId('summary-skills')]:2};
    expect(languageMarks(card,saved)).toBe(9);
    expect(languageMarks(card,{...saved,[languageFlagId('incomplete-response')]:1})).toBe(8);
    const other={...saved,[languageOtherLanguageId('response')]:1};
    expect(languageMarks(card,other)).toBe(2);
    expect(languageMarks(card,{...other,[languageFlagId('incomplete-response')]:1})).toBe(1);
    expect(languageMarks(card,{...other,[languageOtherLanguageId('response')]:0})).toBe(9);
    render(<LanguageRubricPanel card={card} scores={saved} onScore={vi.fn()}/>);
    expect(screen.getAllByText(/Single marks may be awarded for partial details/)[0]).toBeVisible();
    expect(screen.getAllByText(/Discretionary marks \(as opposed to content marks\) may be awarded/)[0]).toBeVisible();
  });
  it('retains six language-permitted case answers and one of three complete cultural topics',()=>{
    const cases=points('la1');expect(cases.rubric.groups).toHaveLength(6);expect(cases.answerLanguageRule).toBeUndefined();
    expect(languageMarks(cases,Object.assign({},...cases.rubric.groups.map(g=>row(g.id))))).toBe(6);
    expect(cases.rubric.taskRequirements.join(' ')).toContain('Irish, English or Russian');
    const culture=points('ca1');expect(culture.rubric.groups).toHaveLength(3);expect(culture.rubric.count).toBe(1);
    expect(culture.answerLanguageRule).toBeUndefined();
    expect(languageMarks(culture,{[languageGroupId('topic-1')]:1,...Object.fromEntries([1,2,3].map(n=>[languageScoreId(`topic-1-detail-${n}`),2]))})).toBe(6);
  });
  it('keeps five infinitives and the complete fifteen-entry semantic pool under a five-answer quota',()=>{
    const verbs=points('la2-1'),family=points('la2-2');
    expect(verbs.rubric.groups).toHaveLength(5);expect(verbs.rubric.groups[0].rows[0].text).toBe('беспокоилась — беспокоиться');
    expect(languageMarks(verbs,Object.assign({},...verbs.rubric.groups.map(g=>row(g.id))))).toBe(5);
    expect(family.rubric.groups).toHaveLength(15);expect(family.rubric.count).toBe(5);
    expect(family.rubric.groups.at(-1)?.rows[0].text).toBe('материально самостоятельная');
    expect(languageMarks(family,Object.assign({},...family.rubric.groups.map(g=>row(g.id))))).toBe(5);
  });
  it('preserves both matching alternatives and all fifteen original grammar forms',()=>{
    const matching=points('sd');expect(matching.rubric.groups).toHaveLength(10);
    expect(matching.rubric.groups[8].rows[0].text).toMatch(/^2\/8 —/);expect(matching.rubric.groups[9].rows[0].text).toMatch(/^8\/2 —/);
    expect(languageMarks(matching,Object.assign({},...matching.rubric.groups.map(g=>row(g.id))))).toBe(20);
    const grammar=points('gr');expect(grammar.rubric.groups).toHaveLength(15);
    expect(grammar.rubric.groups.slice(3,5).map(g=>g.rows[0].text)).toEqual(['современную','музыку']);
    expect(grammar.rubric.groups.slice(10,12).map(g=>g.rows[0].text)).toEqual(['прошлого','годa']);
    expect(languageMarks(grammar,Object.assign({},...grammar.rubric.groups.map(g=>row(g.id))))).toBe(30);
  });
  it('uses the consistent guided-writing range without assigning the overlapping descriptors or a minimum',()=>{
    const card=writing(),scores={[languageScoreId('content')]:15,[languageScoreId('expression')]:15,[languageScoreId('coherence')]:10,[languageLengthId('words')]:140};
    expect(languageMarks(card,scores)).toBe(40);
    expect(languageMarks(card,{...scores,[languageFlagId('lower-a')]:1})).toBe(37);
    expect(languageMarks(card,{...scores,[languageFlagId('lower-a')]:1,[languageScoreId('expression')]:6})).toBe(25);
    expect(languageMarks(card,{...scores,[languageScoreId('soft-sign-penalty')]:2})).toBe(38);
    expect(languageMarks(card,{...scores,[languageScoreId('soft-sign-penalty')]:1})).toBe(40);
    expect(languageMarks(card,{...scores,[languageScoreId('content')]:7})).toBe(27);
    render(<LanguageRubricPanel card={card} scores={{...scores,[languageFlagId('lower-a')]:1}} onScore={vi.fn()}/>);
    expect(screen.getAllByText(/Lower A Expression 11-12/)[0]).toBeVisible();
    expect(screen.getAllByText(/Lower A Expression 11-12/)[0]).toHaveTextContent('9-11');
    expect(card.rubric.criteria[1].limits?.find(l=>l.id==='lower-a')?.bands).toBeUndefined();
  });
  it('keeps full and partial wordings mutually exclusive within the requested detail',()=>{
    for(const suffix of ['l1-5-i','l2-3-ii']) {
      const card=points(suffix),group=card.rubric.groups[0];
      const partial={[languageGroupId(group.id)]:1,[languageRowId(group.id,'partial-1')]:1};
      expect(languageMarks(card,partial)).toBe(1);
      expect(languageMarks(card,{...partial,[languageRowId(group.id,'full')]:1})).toBe(2);
    }
    const whenWhere=points('l3-1-i');
    expect(languageMarks(whenWhere,{...row('answer-1'),...row('answer-2'),[languageRowId('answer-2','full')]:2})).toBe(4);
    expect(languageMarks(whenWhere,{...row('answer-1'),[languageRowId('answer-1','full')]:0,[languageRowId('answer-1','partial-1')]:1,...row('answer-2')})).toBe(2);
  });
  it('applies the approved essay deduction without changing the original notation or lower scales',()=>{
    const card=essay(),full={[languageScoreId('content')]:10,[languageScoreId('expression')]:20,[languageLengthId('words')]:50};
    expect(languageMarks(card,full)).toBe(30);
    expect(languageMarks(card,{...full,[languageScoreId('soft-sign-penalty')]:1})).toBe(29);
    expect(languageMarks(card,{...full,[languageScoreId('soft-sign-penalty')]:2})).toBe(28);
    expect(languageMarks(card,{...full,[languageFlagId('lower-a')]:1})).toBe(24);
    expect(languageMarks(card,{...full,[languageScoreId('content')]:4})).toBe(18);
    expect(languageMarks(card,{...full,[languageScoreId('content')]:0})).toBe(0);
    expect(languageMarks(card,{...full,[languageLengthId('words')]:24})).toBe(24);
    expect(card.rubric.criteria.at(-1)?.guidance[0]).toContain('Deduct 1/2 marks');
  });
  it.each([false,true])('saves an assessed listening answer with its two available marks, paper layout=%s',async paperLayout=>{
    const card=points('l1-5-i'),onGrade=vi.fn();render(<SessionScreen paperLayout={paperLayout} cards={[card]} subjectLabel="Russian" onGrade={onGrade} onFinish={vi.fn()} onExit={vi.fn()}/>);
    fireEvent.click(screen.getByRole('button',{name:'Reveal the marking scheme'}));
    await waitFor(()=>expect(screen.getByText(/Two marks per complete requested detail are inferred/)).toBeVisible());
    fireEvent.click(screen.getByRole('button',{name:'Answer 1'}));
    fireEvent.click(screen.getByRole('button',{name:/Train station.*2m/}));
    fireEvent.click(screen.getByRole('button',{name:'Got it'}));
    expect(onGrade).toHaveBeenCalledWith(expect.objectContaining({cardId:card.id,grade:'got',marksClaimed:2,marksAvailable:2}));
  });
});
