import { cleanup, fireEvent, render, screen, waitFor } from '@testing-library/react';
import { afterEach, describe, expect, it, vi } from 'vitest';
import SessionScreen, { marksClaimed, showsRowMarks } from '../components/MarkBank/SessionScreen';
import { REVIEWED_CARDS } from '../components/MarkBank/cards/russian/reviewed';
import sources from '../scripts/markbank/authoring/russian-reviewed-sources.json';
import { isRubricCard } from '../types/markBank';
const sourceCard=()=>{const c=REVIEWED_CARDS.find(c=>c.id==='ru-2012-hl-c1-2-ii');if(!c||isRubricCard(c))throw new Error('Missing complete confidence task');return c;};
afterEach(cleanup);
describe('Russian 2012 compulsory-feeling allocation conflict',()=>{
  it('preserves the complete two-detail task and all published guidance without numeric allocation',()=>{
    const c=sourceCard();expect(c.questionText).toContain('Give two details. (Section 2)');
    expect(c.totalMarks).toBe(6);expect(c.tariffModel).toEqual({kind:'questionTotal'});expect(c.rows).toHaveLength(1);
    expect(c.rows[0].marks).toBeNull();
    for(const text of ['COMPULSORY:','she is sad / unhappy / not happy','2 x 2 = 6','assign two marks:','assign one mark:','no marks: bitter'])expect(c.rows[0].verbatim).toContain(text);
    expect(c.rows[0].contextNote).toContain('not an agreed scoring maximum');expect(c.rows[0].contextNote).toContain('Do not infer a third requested detail');
    expect(c.answerLanguageRule).toBeUndefined();expect(showsRowMarks(c)).toBe(false);
    expect(marksClaimed(c,{},{})).toBe(0);
    expect(marksClaimed(c,{'published-guidance':'yes'},{})).toBe(0);
    expect(sources.find(s=>s.id===c.id)).toMatchObject({questionPages:[3],paperPages:[2,3,4],schemePages:[6],component:'000'});
  });
  it.each([false,true])('saves confidence with zero numerical denominator in paper layout=%s',async paperLayout=>{
    const c=sourceCard(),onGrade=vi.fn();render(<SessionScreen paperLayout={paperLayout} cards={[c]} subjectLabel="Russian" onGrade={onGrade} onFinish={vi.fn()} onExit={vi.fn()}/>);
    fireEvent.click(screen.getByRole('button',{name:'Reveal the marking scheme'}));
    await waitFor(()=>expect(screen.getByText(/Source allocation ambiguity:/)).toBeVisible());
    expect(screen.getAllByText(/COMPULSORY: reference must be made/)[0]).toBeVisible();
    expect(screen.queryByRole('button',{name:/^Claim \d+ marks/})).not.toBeInTheDocument();
    expect(screen.queryByRole('checkbox',{name:/another language/})).not.toBeInTheDocument();
    fireEvent.click(screen.getByRole('button',{name:'Got it'}));
    expect(onGrade).toHaveBeenCalledWith(expect.objectContaining({cardId:c.id,grade:'got',marksClaimed:0,marksAvailable:0}));
  });
});
// Integration-only requirement: root's validated confidence metadata labels
// must additionally suppress numeric header/badge/Assess-against-total copy
// and exclude this actual card from numeric quiz selection in both layouts.
// The older lane SessionScreen interface must not be migrated to achieve it.
