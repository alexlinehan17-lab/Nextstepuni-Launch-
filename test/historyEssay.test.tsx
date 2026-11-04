/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 *
 * History essays, marked the way the SEC marks them: by paragraph.
 *
 * The cards under test are the SHIPPED 2025 Higher Later Modern cards, not
 * fixtures, so a regeneration that changed a ladder or a NOTE shows up here.
 * The two cases the earlier renderers got wrong are pinned by name: seven
 * paragraphs at 12 plus an OE of 34 is 94 (a sum capped only at the card total
 * gave 118, shown as 100), and one paragraph is worth at most 12 however its
 * marks are entered (two bands claimed in one Geography unit gave 22).
 */
import { describe, expect, it, vi } from 'vitest';
import { fireEvent, render, screen, within } from '@testing-library/react';
import { CARDS as HISTORY_HIGHER } from '../components/MarkBank/cards/history/higher';
import { CARDS as HISTORY_ORDINARY } from '../components/MarkBank/cards/history/ordinary';
import HistoryEssayPanel from '../components/MarkBank/HistoryEssayPanel';
import SessionScreen, { rubricMarks, suggestRubricGrade } from '../components/MarkBank/SessionScreen';
import {
  historyAddParagraph,
  historyCmTally,
  historyEssayMarks,
  historyOeId,
  historyOneElementId,
  historyParagraphCountId,
  historyParagraphId,
  historyRemoveParagraph,
  type HistoryEssayScores,
} from '../components/MarkBank/historyEssayScoring';
import {
  HISTORY_ESSAY_NO_MODEL_ANSWER, isRubricCard, tariffReconciles,
  type HistoryEssayRubric, type SecRubricCard,
} from '../types/markBank';

vi.mock('../components/PaperTrail/vaultDocs', () => ({ vaultPdf: vi.fn(() => new Promise(() => {})) }));

type EssayCard = SecRubricCard & { rubric: HistoryEssayRubric };
const essays = [...HISTORY_HIGHER, ...HISTORY_ORDINARY]
  .filter((card): card is EssayCard => isRubricCard(card) && card.rubric.system === 'history-essay');
const byId = (id: string) => essays.find(card => card.id === id)!;
const famine = byId('hist-2025-hl-lm-s2t1-q1');       // prints a NOTE: Max. CM = 50 for one element
const science = byId('hist-2025-hl-lm-s2t1-q4');      // prints no NOTE
const jarrow = byId('hist-2025-hl-lm-s1-q4');         // the documents question's Q4: CM 24, OE 16

/** Scores for paragraphs placed at `marks`, in order, and an OE. */
const placed = (marks: number[], oe?: number, extra: HistoryEssayScores = {}): HistoryEssayScores => ({
  [historyParagraphCountId]: marks.length,
  ...Object.fromEntries(marks.map((mark, index) => [historyParagraphId(index + 1), mark])),
  ...(oe === undefined ? {} : { [historyOeId]: oe }),
  ...extra,
});

describe('the shipped History essay cards', () => {
  it('cards 2025 Higher Later Modern whole: 44 essays and Q4, and nothing else yet', () => {
    expect(essays).toHaveLength(45);
    expect(essays.every(card => card.year === 2025 && card.level === 'higher' && /Later Modern/.test(card.questionRef))).toBe(true);
    expect(essays.filter(card => card.totalMarks === 100)).toHaveLength(44);
    expect(essays.filter(card => card.rubric.cm.elementRule)).toHaveLength(27);
    expect(jarrow.totalMarks).toBe(40);
  });

  it('reconciles every ladder with its card, and refuses a broken one', () => {
    for (const card of essays) expect(tariffReconciles(card), card.id).toBe(true);
    const gap = structuredClone(famine);
    gap.rubric.cm.bands[1].marks = [8, 9];               // drops 10 from "Very good: 8-10 marks"
    expect(tariffReconciles(gap)).toBe(false);
    const overlap = structuredClone(famine);
    overlap.rubric.oe.bands[0].marks = [33, ...overlap.rubric.oe.bands[0].marks];
    expect(tariffReconciles(overlap)).toBe(false);
    expect(tariffReconciles({ ...famine, totalMarks: 99 })).toBe(false);
    const looseNote = structuredClone(famine);
    looseNote.rubric.cm.elementRule!.max = 60;
    expect(tariffReconciles(looseNote)).toBe(false);
  });

  it('lifts each ladder per question: Q4 has its own bands and descriptors', () => {
    const fair = (card: EssayCard) => card.rubric.cm.bands.find(band => band.label === 'Fair')!.descriptor;
    expect(fair(jarrow)).toBe('Limited information/barely expressed.');
    expect(fair(famine)).toBe('Limited information/barely stated.');
    expect(jarrow.rubric.oe.bands.map(band => band.printed)).toEqual([
      'Excellent: 14-16 marks', 'Very good: 11-13 marks', 'Good: 6-10 marks',
      'Fair: 4-5 marks', 'Weak: 2-3 marks', 'Very weak: 0-1 mark',
    ]);
    expect(jarrow.rubric.oe.bands.every(band => band.descriptor === undefined)).toBe(true);
    expect(famine.rubric.oe.bands.map(band => band.printed)).toEqual([
      'Excellent: 34-40 marks', 'Very good: 28-33 marks', 'Good: 22-27 marks',
      'Fair: 16-21 marks', 'Weak: 10-15 marks', 'Very weak: 0-9 marks',
    ]);
    expect(famine.rubric.cm.elementRule).toEqual({ note: 'NOTE: TWO elements (during + after) If only ONE, Max. CM = 50', max: 50 });
    expect(science.rubric.cm.elementRule).toBeUndefined();
    // The summation cap is a direction, and the scheme's own "open mind" sentence is on every essay.
    expect(famine.rubric.cm.directions).toContain('(Summation which is mere repetition = max. 4 marks)');
    expect(jarrow.rubric.cm.directions).toContain('(Summation which is mere repetition = max 4 marks)');
    expect(famine.rubric.schemeGuidance.join(' ')).toMatch(/^To mark the answer, the examiner will approach the material with an open mind as to the range of valid answers/);
    for (const card of essays) {
      expect(JSON.stringify(card.rubric)).not.toContain(HISTORY_ESSAY_NO_MODEL_ANSWER);
      expect(card.rubric.schemeFileid).toBe('LC004ALP000EV');
    }
  });
});

describe('scoring by paragraph', () => {
  it('caps the CM at its printed maximum: seven paragraphs at 12 and an OE of 34 is 94, not 118', () => {
    const scores = placed([12, 12, 12, 12, 12, 12, 12], 34);
    expect(historyCmTally(famine.rubric, scores).cm).toBe(60);
    expect(historyEssayMarks(famine, scores)).toBe(94);
    expect(rubricMarks(famine, scores)).toBe(94);
  });

  it('holds one mark per paragraph: a paragraph is never worth more than 12', () => {
    // Geography's repeated unit let one paragraph be claimed at 12 AND 10 (22).
    // Here a paragraph is one score: placing it again replaces the mark.
    let scores = placed([12]);
    scores = { ...scores, [historyParagraphId(1)]: 10 };
    expect(historyCmTally(famine.rubric, scores).cm).toBe(10);
    expect(historyEssayMarks(famine, placed([22]))).toBe(0);
    const tally = historyCmTally(famine.rubric, placed([12, 12, 12]));
    expect(Math.max(...tally.paragraphs.map(p => p.counted))).toBe(12);
  });

  it('counts paragraphs in order and gives an excess paragraph zero', () => {
    const tally = historyCmTally(famine.rubric, placed([12, 12, 12, 12, 9, 10, 8]));
    expect(tally.paragraphs.map(p => [p.placed, p.counted])).toEqual([
      [12, 12], [12, 12], [12, 12], [12, 12], [9, 9], [10, 3], [8, 0],
    ]);
    expect(tally.cm).toBe(60);
  });

  it('applies the NOTE ceiling only when the student says the answer covers one element, and only where a NOTE is printed', () => {
    const one = { [historyOneElementId]: 1 };
    expect(historyEssayMarks(famine, placed([12, 12, 12, 12, 12], 30))).toBe(90);
    expect(historyEssayMarks(famine, placed([12, 12, 12, 12, 12], 30, one))).toBe(80);
    expect(historyCmTally(famine.rubric, placed([], undefined, one)).ceiling).toBe(50);
    // No NOTE: the same switch value changes nothing.
    expect(historyEssayMarks(science, placed([12, 12, 12, 12, 12], 30, one))).toBe(90);
    expect(historyCmTally(science.rubric, placed([], undefined, one)).ceiling).toBe(60);
  });

  it('places the OE at one mark inside one band', () => {
    expect(historyEssayMarks(famine, placed([], 28))).toBe(28);
    expect(historyEssayMarks(famine, placed([], 0))).toBe(0);
    expect(historyEssayMarks(famine, placed([12], 40))).toBe(52);
  });

  it('rejects saved values the scheme does not permit', () => {
    for (const bad of [13, -1, 2.5, 11.5, Number.NaN]) {
      expect(historyEssayMarks(famine, placed([bad])), String(bad)).toBe(0);
    }
    for (const bad of [41, 9.5, -1, 100]) {
      expect(historyEssayMarks(famine, placed([], bad)), String(bad)).toBe(0);
    }
    // Q4's ladders are its own: 16 is its OE top, 17 is off it.
    expect(historyEssayMarks(jarrow, placed([], 16))).toBe(16);
    expect(historyEssayMarks(jarrow, placed([], 17))).toBe(0);
    // A non-integer or negative paragraph count holds no paragraphs.
    expect(historyCmTally(famine.rubric, { [historyParagraphCountId]: 2.5, [historyParagraphId(1)]: 12 }).cm).toBe(0);
    expect(historyCmTally(famine.rubric, { [historyParagraphCountId]: -3 }).paragraphs).toEqual([]);
  });

  it('marks Q4 at its own maxima: CM 24, OE 16', () => {
    expect(historyEssayMarks(jarrow, placed([10, 10, 10], 14))).toBe(38);
    expect(historyCmTally(jarrow.rubric, placed([12, 12, 12])).paragraphs.map(p => p.counted)).toEqual([12, 12, 0]);
  });

  it('adds and removes paragraphs without leaving a stale mark behind', () => {
    const start = placed([12, 9, 6]);
    expect(historyAddParagraph(start)).toEqual([[historyParagraphId(4), -1], [historyParagraphCountId, 4]]);
    const apply = (scores: HistoryEssayScores, writes: Array<[string, number]>) =>
      writes.reduce((next, [id, value]) => ({ ...next, [id]: value }), scores);
    const removed = apply(start, historyRemoveParagraph(start, 1));
    expect(historyCmTally(famine.rubric, removed).paragraphs.map(p => p.placed)).toEqual([9, 6]);
    const regrown = apply(removed, historyAddParagraph(removed));
    expect(historyCmTally(famine.rubric, regrown).paragraphs.map(p => p.placed)).toEqual([9, 6, null]);
  });

  it('suggests a grade from the placement against the card total', () => {
    expect(suggestRubricGrade(famine, placed([12, 12, 12, 12, 12], 34))).toBe('got');
    expect(suggestRubricGrade(famine, placed([8, 8, 8], 16))).toBe('shaky');
    expect(suggestRubricGrade(famine, placed([], undefined))).toBe('missed');
  });
});

describe('the History essay panel', () => {
  it('says the scheme prints no model answer, in the scheme’s own terms', () => {
    render(<HistoryEssayPanel card={famine} scores={{}} onScore={vi.fn()} />);
    expect(screen.getByText(HISTORY_ESSAY_NO_MODEL_ANSWER)).toBeInTheDocument();
    expect(screen.getByText(/^To mark the answer, the examiner will approach the material with an open mind/)).toBeInTheDocument();
    expect(screen.getByText('(Summation which is mere repetition = max. 4 marks)')).toBeInTheDocument();
  });

  it('shows the element switch only where the question prints a NOTE, worded as the student’s judgement', () => {
    const onScore = vi.fn();
    const { unmount } = render(<HistoryEssayPanel card={famine} scores={{}} onScore={onScore} />);
    expect(screen.getByText('NOTE: TWO elements (during + after) If only ONE, Max. CM = 50')).toBeInTheDocument();
    const toggle = screen.getByRole('button', { name: /In my judgement, my answer deals with only one of these elements/ });
    expect(toggle).toHaveAttribute('aria-pressed', 'false');
    fireEvent.click(toggle);
    expect(onScore).toHaveBeenCalledWith(historyOneElementId, 1);
    unmount();
    render(<HistoryEssayPanel card={science} scores={{}} onScore={vi.fn()} />);
    expect(screen.queryByRole('button', { name: /only one of these elements/ })).not.toBeInTheDocument();
  });

  it('starts with no paragraph slots and adds one at a time', () => {
    const onScore = vi.fn();
    render(<HistoryEssayPanel card={famine} scores={{}} onScore={onScore} />);
    expect(screen.queryByText(/^Paragraph \d/)).not.toBeInTheDocument();
    fireEvent.click(screen.getByRole('button', { name: 'Add a paragraph' }));
    expect(onScore).toHaveBeenCalledWith(historyParagraphCountId, 1);
  });

  it('places an open paragraph on one band at one mark, with the scheme’s descriptor beside it', () => {
    const onScore = vi.fn();
    render(<HistoryEssayPanel card={famine} scores={{ [historyParagraphCountId]: 1, [historyParagraphId(1)]: -1 }} onScore={onScore} />);
    const ladder = screen.getByRole('group', { name: 'Bands for paragraph 1' });
    expect(within(ladder).getByText('Very good material, accurately and clearly expressed.')).toBeInTheDocument();
    fireEvent.click(within(ladder).getByRole('button', { name: 'Claim 9 marks for Very good: 8-10 marks' }));
    expect(onScore).toHaveBeenCalledWith(historyParagraphId(1), 9);
  });

  it('shows an excess paragraph at zero and the CM at its maximum', () => {
    render(<HistoryEssayPanel card={famine} scores={placed([12, 12, 12, 12, 12, 10], 30)} onScore={vi.fn()} />);
    expect(screen.getByText('Very good · 10m · past the CM maximum, counts 0m')).toBeInTheDocument();
    expect(screen.getByText('60 / 60')).toBeInTheDocument();
    expect(screen.getByText(/Your CM has reached its maximum of 60/)).toBeInTheDocument();
    expect(screen.getByText('90 / 100')).toBeInTheDocument();
  });

  it('uses Q4’s own ladder when the documents question is marked', () => {
    render(<HistoryEssayPanel card={jarrow} scores={{ [historyParagraphCountId]: 1, [historyParagraphId(1)]: -1 }} onScore={vi.fn()} />);
    expect(screen.getByText('Limited information/barely expressed.')).toBeInTheDocument();
    expect(screen.queryByText('Limited information/barely stated.')).not.toBeInTheDocument();
    expect(screen.getByText('(Summation which is mere repetition = max 4 marks)')).toBeInTheDocument();
  });
});

describe('an essay in a Mark Bank session', () => {
  it('reveals the paragraph marking, not the point-card "complete response" check', () => {
    render(<SessionScreen cards={[famine]} subjectLabel="History" onGrade={vi.fn()} onFinish={vi.fn()} onExit={vi.fn()} />);
    // The question is set with its command words emphasised, so it spans elements.
    expect(screen.getByText(/What was the impact of the Great Famine on life/)).toBeInTheDocument();
    expect(screen.queryByText(HISTORY_ESSAY_NO_MODEL_ANSWER)).not.toBeInTheDocument();
    fireEvent.click(screen.getByRole('button', { name: /Reveal the marking scheme/i }));
    expect(screen.getByText(HISTORY_ESSAY_NO_MODEL_ANSWER)).toBeInTheDocument();
    expect(screen.queryByText('Check your complete response.')).not.toBeInTheDocument();
    expect(screen.getByText(/No History essay placement selected yet/)).toBeInTheDocument();
  });
});
