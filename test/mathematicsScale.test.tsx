import React from 'react';
import { tariffReconciles } from '../types/markBank';
import { afterAll, beforeAll, describe, expect, it, vi } from 'vitest';
import { fireEvent, render, screen, waitFor, within } from '@testing-library/react';
import SessionScreen, { marksClaimed, showsRowMarks } from '../components/MarkBank/SessionScreen';
import { mathematicsScaleMarks, type MathematicsScaleCard } from '../components/MarkBank/MathematicsScalePanel';
import { CARDS as ORDINARY } from '../components/MarkBank/cards/maths/ordinary';
import { CARDS as FOUNDATION } from '../components/MarkBank/cards/maths/foundation';
import { CARDS } from '../components/MarkBank/cards/maths/higher';
import { vaultPdf } from '../components/PaperTrail/vaultDocs';

vi.mock('../components/PaperTrail/vaultDocs', () => ({
  vaultPdf: vi.fn(() => new Promise(() => {})),
}));

const card = CARDS.find(c => c.id === 'maths-2025-hl-p1-q1-a')! as MathematicsScaleCard & typeof CARDS[number];

describe('Mathematics published credit scale', () => {
  it('reveals the plotting prerequisite beside its single ten-mark award', async () => {
    const observation = ORDINARY.find(c => c.id === 'maths-2011-ol-p1-project-q5-a-iv')!;
    if (observation.kind !== 'question') throw new Error('Expected question');
    const note = observation.mathematicsScale!.markingNote!;
    render(<SessionScreen cards={[observation]} subjectLabel="Mathematics"
      onGrade={vi.fn()} onExit={vi.fn()} onFinish={vi.fn()} />);
    expect(screen.queryByText(note)).not.toBeInTheDocument();
    fireEvent.click(screen.getByRole('button', { name: 'Reveal the marking scheme' }));
    await waitFor(() => expect(screen.getByText(note)).toBeVisible());
    expect(screen.getByRole('radio', { name: 'Full credit, 10 of 10 marks' })).toBeVisible();
    expect(screen.getAllByRole('radio')).toHaveLength(2);
  });
  // jsdom does not implement native dialog methods; browser QA exercises the
  // real top layer, focus trap and Escape behaviour on desktop and mobile.
  const originalShow = Object.getOwnPropertyDescriptor(HTMLDialogElement.prototype, 'showModal');
  const originalClose = Object.getOwnPropertyDescriptor(HTMLDialogElement.prototype, 'close');
  beforeAll(() => {
    Object.defineProperty(HTMLDialogElement.prototype, 'showModal', { configurable: true, writable: true,
      value: function (this: HTMLDialogElement) { this.setAttribute('open', ''); } });
    Object.defineProperty(HTMLDialogElement.prototype, 'close', { configurable: true, writable: true,
      value: function (this: HTMLDialogElement) { this.removeAttribute('open'); fireEvent(this, new Event('close')); } });
  });
  afterAll(() => {
    if (originalShow) Object.defineProperty(HTMLDialogElement.prototype, 'showModal', originalShow);
    else Reflect.deleteProperty(HTMLDialogElement.prototype, 'showModal');
    if (originalClose) Object.defineProperty(HTMLDialogElement.prototype, 'close', originalClose);
    else Reflect.deleteProperty(HTMLDialogElement.prototype, 'close');
  });
  it('shows the full printed choice with its original question before reveal', async () => {
    const selected = ORDINARY.find(c => c.id === 'maths-2013-ol-p1-project-q3-b-ii-abcde')!;
    if (selected.kind !== 'question') throw new Error('Expected question');
    render(<SessionScreen cards={[selected]} subjectLabel="Mathematics"
      onGrade={vi.fn()} onExit={vi.fn()} onFinish={vi.fn()} />);
    expect(screen.getByText(/Choose any five of A–G/)).toBeVisible();
    expect(screen.getByRole('img', { name: selected.questionFigure!.alt })).toBeVisible();
    expect(screen.queryByRole('img', { name: selected.figure!.alt })).not.toBeInTheDocument();
    fireEvent.click(screen.getByRole('button', { name: 'Reveal the marking scheme' }));
    await waitFor(() => expect(screen.getByRole('region', { name: 'SEC scale 5C' })).toBeVisible());
  });
  it('reveals the typeset solution inside the scheme with an enlarged reading view', () => {
    const typeset = CARDS.find(c => c.id === 'maths-2015-hl-p1-q9-e')!;
    if (typeset.kind !== 'question') throw new Error('Expected a question card');
    const show = vi.spyOn(HTMLDialogElement.prototype, 'showModal').mockImplementation(function () {
      this.setAttribute('open', '');
    });
    const close = vi.spyOn(HTMLDialogElement.prototype, 'close').mockImplementation(function () {
      this.removeAttribute('open');
      fireEvent(this, new Event('close'));
    });
    render(<SessionScreen cards={[typeset]} subjectLabel="Mathematics"
      onGrade={vi.fn()} onExit={vi.fn()} onFinish={vi.fn()} />);
    expect(screen.queryByRole('button', { name: 'Enlarge worked solution' })).not.toBeInTheDocument();
    expect(screen.queryByAltText(typeset.figure!.alt)).not.toBeInTheDocument();
    fireEvent.click(screen.getByRole('button', { name: 'Reveal the marking scheme' }));
    const scale = screen.getByRole('region', { name: 'SEC scale 10D' });
    expect(within(scale).getByRole('img', { name: typeset.figure!.alt })).toBeInTheDocument();
    const enlarge = within(scale).getByRole('button', { name: 'Enlarge worked solution' });
    fireEvent.click(enlarge);
    expect(show).toHaveBeenCalledOnce();
    const dialog = screen.getByRole('dialog', { name: 'Worked solution and credit notes' });
    fireEvent.click(within(dialog).getByRole('button', { name: 'Zoom in' }));
    expect(within(dialog).getByRole('button', { name: 'Fit to screen' })).toHaveAttribute('aria-pressed', 'true');
    fireEvent.click(within(dialog).getByRole('button', { name: 'Close solution' }));
    expect(screen.queryByRole('dialog')).not.toBeInTheDocument();
    expect(enlarge).toHaveFocus();
    show.mockRestore(); close.mockRestore();
  });
  it('reveals a source-error clarification with the original solution, including in the enlarged view', () => {
    const corrected = ORDINARY.find(c => c.id === 'maths-2015-ol-p1-q5-a')!;
    if (corrected.kind !== 'question' || !corrected.figure?.sourceNote) throw new Error('Missing verified source note');
    render(<SessionScreen cards={[corrected]} subjectLabel="Mathematics"
      onGrade={vi.fn()} onExit={vi.fn()} onFinish={vi.fn()} />);
    expect(screen.queryByText(corrected.figure.sourceNote)).not.toBeInTheDocument();
    fireEvent.click(screen.getByRole('button', {name:'Reveal the marking scheme'}));
    const note = screen.getAllByText(corrected.figure.sourceNote).find(n => !n.closest('dialog'))!;
    expect(note).toBeInTheDocument();
    fireEvent.click(screen.getByRole('button', {name:'Enlarge worked solution'}));
    expect(within(screen.getByRole('dialog')).getByText(corrected.figure.sourceNote)).toBeInTheDocument();
    expect(within(screen.getByRole('dialog')).getByRole('img')).toHaveAttribute('src', corrected.figure.src);
    fireEvent.click(screen.getByRole('button', {name:'Close solution'}));
  });
  it('scores the proof as one task with three exact scales and only one conditional deduction', () => {
    const proof = CARDS.find(c => c.id === 'maths-2015-hl-p2-q6-b')!;
    if (proof.kind !== 'question' || !proof.mathematicsScale?.components) throw new Error('Missing component proof');
    const mathsProof = proof as MathematicsScaleCard;
    expect(tariffReconciles(proof)).toBe(true);
    const scores = { 'mathematics:diagram-given': 5, 'mathematics:construction': 2, 'mathematics:proof': 8 };
    expect(mathematicsScaleMarks(mathsProof, 20, scores)).toBe(15);
    expect(mathematicsScaleMarks(mathsProof, undefined, {...scores, 'mathematics:deduction': 1})).toBe(15);
    expect(mathematicsScaleMarks(mathsProof, undefined, {...scores, 'mathematics:proof': 9})).toBe(7);
    const full = {...scores, 'mathematics:construction': 5, 'mathematics:proof': 10};
    expect(mathematicsScaleMarks(mathsProof, undefined, full)).toBe(20);
    expect(mathematicsScaleMarks(mathsProof, undefined, {...full, 'mathematics:deduction': 1})).toBe(19);
    for (const components of [
      proof.mathematicsScale.components.slice(1),
      proof.mathematicsScale.components.map(c => ({...c,id:'same'})),
      proof.mathematicsScale.components.map(c => c.id === 'proof' ? {...c,marks:[0,4,10]} : c),
    ]) {
      expect(tariffReconciles({...proof,mathematicsScale:{fullCreditMinusOne:proof.mathematicsScale.fullCreditMinusOne,
        schemeFileid:proof.mathematicsScale.schemeFileid,schemePages:proof.mathematicsScale.schemePages,
        generalNotesPages:proof.mathematicsScale.generalNotesPages,components}})).toBe(false);
    }
  });

  it('lets students award each proof component independently, resets a deduction and saves the combined mark', () => {
    const proof = CARDS.find(c => c.id === 'maths-2015-hl-p2-q6-b')!;
    const onGrade = vi.fn();
    render(<SessionScreen cards={[proof]} subjectLabel="Mathematics" onGrade={onGrade} onExit={vi.fn()} onFinish={vi.fn()} />);
    expect(screen.queryByRole('region',{name:'SEC component scales'})).not.toBeInTheDocument();
    fireEvent.click(screen.getByRole('button',{name:'Reveal the marking scheme'}));
    const diagram = screen.getByRole('group',{name:'Diagram / Given · 5B'});
    const construction = screen.getByRole('group',{name:'Construction · 5B'});
    const proofGroup = screen.getByRole('group',{name:'Proof · 10C'});
    const deduction = screen.getByRole('checkbox',{name:/Apply one minor-error deduction/});
    expect(deduction).toBeDisabled();
    fireEvent.click(within(diagram).getByRole('radio',{name:'Full credit, 5 of 5 marks'}));
    fireEvent.click(within(construction).getByRole('radio',{name:'Full credit, 5 of 5 marks'}));
    fireEvent.click(within(proofGroup).getByRole('radio',{name:'Full credit, 10 of 10 marks'}));
    fireEvent.click(deduction);
    expect(screen.getByText('Total: 19 / 20 marks')).toBeInTheDocument();
    fireEvent.click(within(proofGroup).getByRole('radio',{name:'High partial credit, 8 of 10 marks'}));
    expect(deduction).not.toBeChecked(); expect(deduction).toBeDisabled();
    expect(screen.getByText('Total: 18 / 20 marks')).toBeInTheDocument();
    fireEvent.click(screen.getByRole('button',{name:/^Shaky/}));
    expect(onGrade).toHaveBeenCalledWith(expect.objectContaining({cardId:proof.id,marksClaimed:18,marksAvailable:20,grade:'shaky'}));
  });

  it('restricts a component deduction to the starred graph, including when points receive partial credit', () => {
    const graph = FOUNDATION.find(c => c.id === 'maths-2013-fl-p1-q10-a')!;
    if (graph.kind !== 'question' || !graph.mathematicsScale?.components) throw new Error('Missing graph components');
    const scale = graph.mathematicsScale as Extract<NonNullable<typeof graph.mathematicsScale>, { components: unknown[] }>;
    expect(tariffReconciles(graph)).toBe(true);
    const score = (points: number, graphMark: number) => mathematicsScaleMarks(graph as MathematicsScaleCard, undefined,
      {'mathematics:points': points, 'mathematics:graph': graphMark, 'mathematics:deduction': 1});
    expect(score(12,9)).toBe(21);
    expect(score(25,9)).toBe(34);
    expect(score(25,10)).toBe(35);
    expect(score(24,9)).toBe(9);
    expect(score(12,8)).toBe(12);
    expect(tariffReconciles({...graph, mathematicsScale: {...scale, fullCreditMinusOne: true}})).toBe(false);
    expect(tariffReconciles({...graph, mathematicsScale: {fullCreditMinusOne: false, schemeFileid: scale.schemeFileid,
      schemePages: scale.schemePages, generalNotesPages: scale.generalNotesPages, components: scale.components.map(c => ({...c, fullCreditMinusOne: 'yes' as unknown as boolean}))}})).toBe(false);
  });

  it('lets students choose a graph-only deduction independently and saves the combined award', async () => {
    const graph = FOUNDATION.find(c => c.id === 'maths-2013-fl-p1-q10-a')!;
    const onGrade = vi.fn();
    render(<SessionScreen cards={[graph]} subjectLabel="Mathematics" onGrade={onGrade} onExit={vi.fn()} onFinish={vi.fn()} />);
    fireEvent.click(screen.getByRole('button',{name:'Reveal the marking scheme'}));
    const points = screen.getByRole('group',{name:'Points · 25D'});
    const plot = screen.getByRole('group',{name:'Graph · 10C'});
    expect(within(points).queryByRole('radio',{name:/Full credit −1/})).not.toBeInTheDocument();
    expect(screen.queryByRole('checkbox',{name:/Apply one minor-error deduction/})).not.toBeInTheDocument();
    fireEvent.click(within(points).getByRole('radio',{name:'Mid partial credit, 12 of 25 marks'}));
    const minusOne = within(plot).getByRole('radio',{name:'Full credit −1, 9 of 10 marks'});
    fireEvent.click(minusOne);
    await waitFor(() => expect(screen.getByText('Total: 21 / 35 marks')).toBeVisible());
    fireEvent.click(within(plot).getByRole('radio',{name:'High partial credit, 7 of 10 marks'}));
    expect(minusOne).not.toBeChecked();
    expect(screen.getByText('Total: 19 / 35 marks')).toBeVisible();
    fireEvent.click(minusOne);
    fireEvent.click(screen.getByRole('button',{name:/^Shaky/}));
    expect(onGrade).toHaveBeenCalledWith(expect.objectContaining({cardId:graph.id, marksClaimed:21, marksAvailable:35, grade:'shaky'}));
  });

  it('awards one permitted mark and never adds the old checklist bands', () => {
    expect(card.mathematicsScale.marks).toEqual([0, 2, 4, 6, 10]);
    for (const mark of [0, 2, 4, 6, 9, 10]) expect(mathematicsScaleMarks(card, mark)).toBe(mark);
    for (const mark of [-1, 1, 3, 5, 7, 8, 11]) expect(mathematicsScaleMarks(card, mark)).toBe(0);
    expect(showsRowMarks(card)).toBe(false);
    expect(marksClaimed(card, {}, { [card.rows[0].id]: [0, 1, 2] })).toBe(0);
  });

  it('uses the different Ordinary 15D scales printed in Papers 1 and 2', () => {
    const first = ORDINARY.find(c => c.id === 'maths-2025-ol-p1-q4-c-i')! as MathematicsScaleCard;
    const second = ORDINARY.find(c => c.id === 'maths-2025-ol-p2-q2-b')! as MathematicsScaleCard;
    expect(first.mathematicsScale.marks).toEqual([0, 4, 8, 10, 15]);
    expect(second.mathematicsScale.marks).toEqual([0, 6, 8, 10, 15]);
    expect(mathematicsScaleMarks(first, 6)).toBe(0);
    expect(mathematicsScaleMarks(second, 4)).toBe(0);
    expect(mathematicsScaleMarks(first, 4)).toBe(4);
    expect(mathematicsScaleMarks(second, 6)).toBe(6);
  });

  it('uses Foundation scale marks and labels in a real review session', () => {
    const foundation = FOUNDATION.find(c => c.id === 'maths-2025-fl-q7-c-d')!;
    const onGrade = vi.fn();
    render(<SessionScreen cards={[foundation]} subjectLabel="Mathematics"
      onGrade={onGrade} onExit={vi.fn()} onFinish={vi.fn()} />);
    expect(screen.getByText(/FOUNDATION LEVEL/)).toBeInTheDocument();
    fireEvent.click(screen.getByRole('button', { name: 'Reveal the marking scheme' }));
    expect(screen.queryByRole('radio', { name: 'High partial credit, 6 of 10 marks' })).not.toBeInTheDocument();
    fireEvent.click(screen.getByRole('radio', { name: 'High partial credit, 7 of 10 marks' }));
    fireEvent.click(screen.getByRole('button', { name: /^Shaky/ }));
    expect(onGrade).toHaveBeenCalledWith(expect.objectContaining({
      cardId: foundation.id, marksClaimed: 7, marksAvailable: 10, grade: 'shaky',
    }));
  });

  it('keeps the scheme hidden until reveal, replaces the selected award and saves it', async () => {
    const onGrade = vi.fn();
    render(<SessionScreen cards={[card]} subjectLabel="Mathematics"
      onGrade={onGrade} onExit={vi.fn()} onFinish={vi.fn()} />);
    expect(screen.queryByRole('button', { name: /Open worked solution/ })).not.toBeInTheDocument();
    fireEvent.click(screen.getByRole('button', { name: 'Reveal the marking scheme' }));
    expect(screen.queryByRole('button', { name: /Select all/ })).not.toBeInTheDocument();
    fireEvent.click(screen.getByRole('radio', { name: 'Low partial credit, 2 of 10 marks' }));
    fireEvent.click(screen.getByRole('radio', { name: 'High partial credit, 6 of 10 marks' }));
    expect(screen.getByRole('radio', { name: 'Low partial credit, 2 of 10 marks' })).not.toBeChecked();
    expect(screen.getByRole('radio', { name: 'High partial credit, 6 of 10 marks' })).toBeChecked();
    expect(screen.getByText(/Your SEC scale award is 6 of 10 marks/)).toBeInTheDocument();
    fireEvent.click(screen.getByRole('button', { name: /Open worked solution/ }));
    await waitFor(() => expect(vaultPdf).toHaveBeenCalled());
    expect(decodeURIComponent(vi.mocked(vaultPdf).mock.calls.at(-1)![0]))
      .toContain('papers/lc/mathematics/2025/scheme/LC003ALP000EV.pdf');
    fireEvent.keyDown(screen.getByRole('dialog'), { key: 'Escape' });
    fireEvent.click(screen.getByRole('button', { name: /^Shaky/ }));
    expect(onGrade).toHaveBeenCalledWith(expect.objectContaining({
      cardId: card.id, marksClaimed: 6, marksAvailable: 10, grade: 'shaky',
    }));
  });
});
