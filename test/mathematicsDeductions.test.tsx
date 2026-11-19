import React from 'react';
import { describe, expect, it, vi } from 'vitest';
import { fireEvent, render, screen, waitFor } from '@testing-library/react';
import sourceReview from '../scripts/markbank/authoring/maths/2012-hl-p1-source-review.json';
import { CARDS } from '../components/MarkBank/cards/maths/higher';
import { tariffReconciles, type SecPointCard } from '../types/markBank';
import { mathematicsScaleMarks, type MathematicsScaleCard } from '../components/MarkBank/MathematicsScalePanel';
import { deductionAwards } from '../components/MarkBank/MathematicsDeductionsPanel';
import SessionScreen from '../components/MarkBank/SessionScreen';
import { validReviewedMathematicsMarking } from '../scripts/markbank/mathematics/marking-rules.mjs';

vi.mock('../components/PaperTrail/vaultDocs', () => ({ vaultPdf: vi.fn(() => new Promise(() => {})) }));

function fixture(suffix: string): SecPointCard & MathematicsScaleCard {
  const task = sourceReview.tasks.find(t => t.suffix === suffix)!;
  const base = CARDS.find(c => c.kind === 'question') as SecPointCard;
  return { ...base, id: `maths-2012-hl-p1-q${suffix}`, year: 2012, totalMarks: task.totalMarks,
    questionRef: `2012 HL Paper 1 ${task.printedParts.join(', ')}`, questionText: task.questionText,
    stem: 'stem' in task ? task.stem : undefined, figure: undefined, questionFigure: undefined,
    schemeCitation: 'SEC marking scheme, Mathematics 2012 Higher Level — © State Examinations Commission.', paperFileid: 'LC003ALP100EV', sourceMaterial: undefined,
    mathematicsScale: { methods: structuredClone(task.methods), fullCreditMinusOne: false,
      schemeFileid: 'LC003ALP000EV.pdf', schemePages: task.schemePages, generalNotesPages: [4,5],
      markingNote: 'markingNote' in task ? task.markingNote : undefined },
  } as SecPointCard & MathematicsScaleCard;
}

describe('Older SEC Mathematics step marks and deductions', () => {
  it('excludes marks below each attempt floor, and makes hit-or-miss binary', () => {
    expect(deductionAwards({id:'step',label:'Integral',maximum:10,attempt:3})).toEqual([0,3,4,5,6,7,8,9,10]);
    const card=fixture('8-a');
    for (const invalid of [-1,1,2,2.5,11,NaN,Infinity])
      expect(mathematicsScaleMarks(card, undefined, {'mathematics:main:step-1':invalid})).toBe(0);
    expect(mathematicsScaleMarks(card, undefined, {'mathematics:main:step-1':3})).toBe(3);
    const binary=fixture('7-c-iii');
    for (const invalid of [1,2,3,4])
      expect(mathematicsScaleMarks(binary, undefined, {'mathematics:main:step-1':invalid})).toBe(0);
    expect(mathematicsScaleMarks(binary, undefined, {'mathematics:main:step-1':5})).toBe(5);
  });
  it('counts only the selected method and rejects stale or invalid method indices', () => {
    const card=fixture('1-b-i');
    const scores = {'mathematics:factorisation:step-1':5,'mathematics:factorisation:step-2':5,
      'mathematics:factorisation:step-3':5,'mathematics:testing:step-1':2,
      'mathematics:testing:step-2':4,'mathematics:testing:step-3':5};
    expect(mathematicsScaleMarks(card,undefined,scores)).toBe(15);
    expect(mathematicsScaleMarks(card,undefined,{...scores,'mathematics:method':1})).toBe(11);
    for (const index of [-1,0.5,2,NaN])
      expect(mathematicsScaleMarks(card,undefined,{...scores,'mathematics:method':index})).toBe(0);
  });
  it('honours explicit old-scheme awards and rejects scores between them', async () => {
    const card=fixture('8-a');
    const step=card.mathematicsScale.methods![0].components[0];
    step.permittedMarks=[0,3,10];
    expect(deductionAwards(step)).toEqual([0,3,10]);
    for (const invalid of [1,2,4,5,6,7,8,9,11])
      expect(mathematicsScaleMarks(card,undefined,{'mathematics:main:step-1':invalid})).toBe(0);
    const onGrade=vi.fn();
    render(<SessionScreen cards={[card]} subjectLabel="Mathematics" onGrade={onGrade} onExit={vi.fn()} onFinish={vi.fn()} />);
    fireEvent.click(screen.getByRole('button',{name:'Reveal the marking scheme'}));
    await waitFor(()=>expect(screen.getByText('The scheme awards only 0, 3, 10 marks for this step.')).toBeVisible());
    expect(screen.getAllByRole('radio')).toHaveLength(3);
    expect(screen.queryByText(/A mathematical error normally/)).not.toBeInTheDocument();
    fireEvent.click(screen.getByRole('radio',{name:'Integral: 3 of 10 marks'}));
    fireEvent.click(screen.getByRole('button',{name:/^Missed/}));
    expect(onGrade).toHaveBeenCalledWith(expect.objectContaining({marksClaimed:3,marksAvailable:10}));
  });
  it('validates explicit award lists at runtime and during deck generation', () => {
    const card=fixture('8-a');
    const step=card.mathematicsScale.methods![0].components[0];
    for (const awards of [[0,3,10],[0,3,7,10]]) {
      step.permittedMarks=awards;
      expect(tariffReconciles(card)).toBe(true);
      expect(validReviewedMathematicsMarking({methods:card.mathematicsScale.methods,totalMarks:10,schemePages:[39]},
        {fullCreditMinusOne:false,generalNotesPages:[4,5]})).toBe(true);
    }
    for (const awards of [[],[3,10],[0,10],[0,2,3,10],[0,3,3,10],[0,3,7],[0,3,7.5,10],[0,3,11,10]]) {
      step.permittedMarks=awards;
      expect(tariffReconciles(card)).toBe(false);
      expect(validReviewedMathematicsMarking({methods:card.mathematicsScale.methods,totalMarks:10,schemePages:[39]},
        {fullCreditMinusOne:false,generalNotesPages:[4,5]})).toBe(false);
    }
  });
  it.each([[5,4],[10,9]])('keeps the SEC restricted %i-mark award without inventing attempt credit', async (maximum, partial) => {
    const card=fixture('8-a');card.totalMarks=maximum;
    const step=card.mathematicsScale.methods![0].components[0];
    step.maximum=maximum;step.attempt=0;step.permittedMarks=[0,partial,maximum];
    expect(tariffReconciles(card)).toBe(true);
    expect(validReviewedMathematicsMarking({methods:card.mathematicsScale.methods,totalMarks:maximum,schemePages:[39]},
      {fullCreditMinusOne:false,generalNotesPages:[4,5]})).toBe(true);
    expect(deductionAwards(step)).toEqual([0,partial,maximum]);
    for(let invalid=1;invalid<partial;invalid++)
      expect(mathematicsScaleMarks(card,undefined,{'mathematics:main:step-1':invalid})).toBe(0);
    const onGrade=vi.fn();
    render(<SessionScreen cards={[card]} subjectLabel="Mathematics" onGrade={onGrade} onExit={vi.fn()} onFinish={vi.fn()} />);
    fireEvent.click(screen.getByRole('button',{name:'Reveal the marking scheme'}));
    await waitFor(()=>expect(screen.getByText(`The scheme awards only 0, ${partial}, ${maximum} marks for this step.`)).toBeVisible());
    expect(screen.getAllByRole('radio')).toHaveLength(3);
    expect(screen.queryByText(/All or nothing|Attempt mark:/)).not.toBeInTheDocument();
    expect(screen.queryByText('Attempt')).not.toBeInTheDocument();
    fireEvent.click(screen.getByRole('radio',{name:`Integral: ${partial} of ${maximum} marks`}));
    fireEvent.click(screen.getByRole('button',{name:/^Shaky/}));
    expect(onGrade).toHaveBeenCalledWith(expect.objectContaining({marksClaimed:partial,marksAvailable:maximum}));
  });
  it('requires every alternative method to reconcile, with valid unique step identities', () => {
    const card=fixture('1-b-i');
    expect(tariffReconciles(card)).toBe(true);
    const invalid = (mutate: (c: typeof card) => void) => {
      const changed=structuredClone(card);mutate(changed);expect(tariffReconciles(changed)).toBe(false);
    };
    invalid(c=>{c.mathematicsScale.methods![1].components.pop();});
    invalid(c=>{c.mathematicsScale.methods![0].components[0].attempt=5;});
    invalid(c=>{c.mathematicsScale.methods![0].components[0].attempt=-1;});
    invalid(c=>{c.mathematicsScale.methods![0].components[1].id='step-1';});
    invalid(c=>{c.mathematicsScale.methods![1].id='factorisation';});
    invalid(c=>{c.mathematicsScale.fullCreditMinusOne=true;});
  });
  it('builds the inspected deduction boundaries and rejects mixed or incomplete source rules', () => {
    const paper={fullCreditMinusOne:false,generalNotesPages:[4,5]};
    for (const task of sourceReview.tasks) expect(validReviewedMathematicsMarking(task,paper)).toBe(true);
    const task=sourceReview.tasks.find(t=>t.suffix==='1-b-i')!;
    expect(validReviewedMathematicsMarking({...task,scale:'15C',permittedMarks:[0,5,12,15]},paper)).toBe(false);
    expect(validReviewedMathematicsMarking({...task,totalMarks:20},paper)).toBe(false);
    expect(validReviewedMathematicsMarking({...task,schemePages:[]},paper)).toBe(false);
    expect(validReviewedMathematicsMarking(task,{...paper,fullCreditMinusOne:true})).toBe(false);
    const invalid=structuredClone(task);invalid.methods[0].components[0].attempt=5;
    expect(validReviewedMathematicsMarking(invalid,paper)).toBe(false);
  });
  it('restricts per-task guidance to distinct reviewed source pages', () => {
    const paper={fullCreditMinusOne:false,generalNotesPages:[61,62,67,68]};
    const task={scale:'5C',permittedMarks:[0,3,4,5],totalMarks:5,schemePages:[48,69]};
    for(const generalNotesPages of [undefined,[61,62],[67,68]])
      expect(validReviewedMathematicsMarking({...task,generalNotesPages},paper)).toBe(true);
    for(const generalNotesPages of [[],[67,67],[0],[69],[67.5],['67'],null])
      expect(validReviewedMathematicsMarking({...task,generalNotesPages},paper)).toBe(false);
  });
  it('hides marking rules until reveal, switches methods exclusively and saves only the chosen score', async () => {
    const card=fixture('1-b-i');const onGrade=vi.fn();
    render(<SessionScreen cards={[card]} subjectLabel="Mathematics" onGrade={onGrade} onExit={vi.fn()} onFinish={vi.fn()} />);
    expect(screen.queryByText('Mark the steps in your working.')).not.toBeInTheDocument();
    expect(screen.queryByRole('radio')).not.toBeInTheDocument();
    fireEvent.click(screen.getByRole('button',{name:'Reveal the marking scheme'}));
    await waitFor(()=>expect(screen.getByRole('region',{name:'SEC step marks and deductions'})).toBeVisible());
    expect(screen.getByText(/Testing incorrect values with no other work/)).toBeVisible();
    for (const label of ['Root','Quadratic factor','Roots'])
      fireEvent.click(screen.getByRole('radio',{name:`${label}: 5 of 5 marks`}));
    expect(screen.getByText('Total: 15 / 15 marks')).toBeVisible();
    fireEvent.click(screen.getByRole('radio',{name:'Testing the three roots'}));
    expect(screen.getByRole('radio',{name:'Factorisation'})).not.toBeChecked();
    expect(screen.getByText('Total: 0 / 15 marks')).toBeVisible();
    for (const [label,award] of [['First root',2],['Second root',4],['Third root',5]])
      fireEvent.click(screen.getByRole('radio',{name:`${label}: ${award} of 5 marks`}));
    expect(screen.queryByRole('radio',{name:'First root: 1 of 5 marks'})).not.toBeInTheDocument();
    expect(screen.getByText('Total: 11 / 15 marks')).toBeVisible();
    fireEvent.click(screen.getByRole('button',{name:/^Shaky/}));
    expect(onGrade).toHaveBeenCalledWith(expect.objectContaining({cardId:card.id,marksClaimed:11,marksAvailable:15,grade:'shaky'}));
  });
  it('presents the SEC hit-or-miss conclusion without invented intermediate credit', async () => {
    const card=fixture('7-c-iii');const onGrade=vi.fn();
    render(<SessionScreen cards={[card]} subjectLabel="Mathematics" onGrade={onGrade} onExit={vi.fn()} onFinish={vi.fn()} />);
    fireEvent.click(screen.getByRole('button',{name:'Reveal the marking scheme'}));
    await waitFor(()=>expect(screen.getByRole('radio',{name:'Conclusion: 5 of 5 marks'})).toBeVisible());
    expect(screen.getAllByRole('radio')).toHaveLength(2);
    fireEvent.click(screen.getByRole('radio',{name:'Conclusion: 5 of 5 marks'}));
    fireEvent.click(screen.getByRole('button',{name:/^Got it/}));
    expect(onGrade).toHaveBeenCalledWith(expect.objectContaining({marksClaimed:5,marksAvailable:5,grade:'got'}));
  });
});
