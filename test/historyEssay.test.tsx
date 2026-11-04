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
  historyCapId,
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
/** The papers whose essays are carded so far (lane batch 2 adds one sitting a commit). */
const CARDED_ESSAY_PAPERS = ['2010 higher em', '2010 higher lm', '2010 ordinary em', '2010 ordinary lm', '2011 higher em', '2011 higher lm', '2011 ordinary em', '2011 ordinary lm', '2012 higher em', '2012 higher lm', '2012 ordinary em', '2012 ordinary lm', '2013 higher em', '2013 higher lm', '2013 ordinary em', '2013 ordinary lm', '2014 higher em', '2014 higher lm', '2014 ordinary em', '2014 ordinary lm', '2015 higher em', '2015 higher lm', '2015 ordinary em', '2015 ordinary lm', '2016 higher em', '2016 higher lm', '2016 ordinary em', '2016 ordinary lm', '2017 higher em', '2017 higher lm', '2017 ordinary em', '2017 ordinary lm', '2018 higher em', '2018 higher lm', '2018 ordinary em', '2018 ordinary lm', '2019 higher em', '2019 higher lm', '2019 ordinary em', '2019 ordinary lm', '2020 higher lm', '2020 ordinary lm', '2021 higher em', '2021 higher lm', '2021 ordinary em', '2021 ordinary lm', '2022 higher em', '2022 higher lm', '2022 ordinary em', '2022 ordinary lm', '2023 higher em', '2023 higher lm', '2023 higher lm deferred', '2023 ordinary em', '2023 ordinary lm', '2024 higher em', '2024 higher lm', '2024 ordinary em', '2024 ordinary lm', '2025 higher em', '2025 higher lm', '2025 ordinary em', '2025 ordinary lm', '2026 higher em', '2026 higher lm', '2026 ordinary em', '2026 ordinary lm'];
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
  it('cards every essay of each carded paper: Higher 44 essays + Q4, Ordinary parts B and C + Q4', () => {
    const byPaper = new Map<string, EssayCard[]>();
    for (const card of essays) {
      const paper = `${card.year} ${card.level} ${/Early Modern/.test(card.questionRef) ? 'em' : 'lm'}${card.id.includes('-deferred-') ? ' deferred' : ''}`;
      byPaper.set(paper, [...(byPaper.get(paper) ?? []), card]);
    }
    expect([...byPaper.keys()].sort()).toEqual(CARDED_ESSAY_PAPERS);
    for (const [paper, cards] of byPaper) {
      const higher = paper.includes('higher');
      expect(cards, paper).toHaveLength(higher ? 45 : 23);
      expect(cards.filter(card => card.section === '1').map(card => card.totalMarks), paper).toEqual([higher ? 40 : 20]);
      expect(new Set(cards.filter(card => card.section !== '1').map(card => card.totalMarks)), paper)
        .toEqual(new Set(higher ? [100] : [30, 40]));
      expect(cards.every(card => card.rubric.cm.mode === (higher ? 'paragraph' : 'core-statement')), paper).toBe(true);
    }
    // 2025 Higher Later Modern prints a NOTE on 27 of its 44 essays.
    expect(byPaper.get('2025 higher lm')!.filter(card => card.rubric.cm.elementRule)).toHaveLength(27);
    expect(jarrow.totalMarks).toBe(40);
  });

  it('reconciles every ladder with its card, and refuses a broken one', () => {
    for (const card of essays) expect(tariffReconciles(card), card.id).toBe(true);
    const gap = structuredClone(famine);
    if (gap.rubric.cm.mode === 'paragraph') gap.rubric.cm.bands[1].marks = [8, 9]; // drops 10 from "Very good: 8-10 marks"
    expect(tariffReconciles(gap)).toBe(false);
    const overlap = structuredClone(famine);
    overlap.rubric.oe!.bands[0].marks = [33, ...overlap.rubric.oe!.bands[0].marks];
    expect(tariffReconciles(overlap)).toBe(false);
    expect(tariffReconciles({ ...famine, totalMarks: 99 })).toBe(false);
    const looseNote = structuredClone(famine);
    looseNote.rubric.cm.elementRule!.caps[0].max = 60;
    expect(tariffReconciles(looseNote)).toBe(false);
  });

  it('lifts each ladder per question: Q4 has its own bands and descriptors', () => {
    const fair = (card: EssayCard) => card.rubric.cm.mode === 'paragraph'
      ? card.rubric.cm.bands.find(band => band.label === 'Fair')!.descriptor : undefined;
    expect(fair(jarrow)).toBe('Limited information/barely expressed.');
    expect(fair(famine)).toBe('Limited information/barely stated.');
    expect(jarrow.rubric.oe!.bands.map(band => band.printed)).toEqual([
      'Excellent: 14-16 marks', 'Very good: 11-13 marks', 'Good: 6-10 marks',
      'Fair: 4-5 marks', 'Weak: 2-3 marks', 'Very weak: 0-1 mark',
    ]);
    expect(jarrow.rubric.oe!.bands.every(band => band.descriptor === undefined)).toBe(true);
    expect(famine.rubric.oe!.bands.map(band => band.printed)).toEqual([
      'Excellent: 34-40 marks', 'Very good: 28-33 marks', 'Good: 22-27 marks',
      'Fair: 16-21 marks', 'Weak: 10-15 marks', 'Very weak: 0-9 marks',
    ]);
    expect(famine.rubric.cm.elementRule).toEqual({ note: 'NOTE: TWO elements (during + after) If only ONE, Max. CM = 50', caps: [{ when: 'If only ONE', max: 50 }] });
    expect(science.rubric.cm.elementRule).toBeUndefined();
    // The summation cap is a direction, and the scheme's own "open mind" sentence is on every essay.
    expect(famine.rubric.cm.directions).toContain('(Summation which is mere repetition = max. 4 marks)');
    expect(jarrow.rubric.cm.directions).toContain('(Summation which is mere repetition = max 4 marks)');
    expect(famine.rubric.schemeGuidance.join(' ')).toMatch(/^To mark the answer, the examiner will approach the material with an open mind as to the range of valid answers/);
    for (const card of essays) {
      expect(JSON.stringify(card.rubric)).not.toContain(HISTORY_ESSAY_NO_MODEL_ANSWER);
      // A deferred sitting's essays open its own scheme, indexed beside June's.
      expect(card.rubric.schemeFileid).toBe(`${card.level === 'higher' ? 'LC004ALP000EV' : 'LC004GLP000EV'}${card.id.includes('-deferred-') ? '-deferred' : ''}`);
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

  it('applies the NOTE ceiling only when the student says it applies, and only where a NOTE is printed', () => {
    const one = { [historyCapId]: 1 };
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

describe('scoring by Core Statement and by a NOTE with several ceilings', () => {
  // Built from the shipped Q4's own strings so only the mode is synthetic; the
  // Ordinary decks that ship this mode are pinned in their own sitting tests.
  const core: EssayCard = {
    ...jarrow, id: 'synthetic-ol-b', totalMarks: 30,
    rubric: {
      ...jarrow.rubric,
      cm: {
        mode: 'core-statement', max: 20, definition: 'CM', directions: [],
        statementLead: 'lead', statementKinds: ['a', 'b', 'c'], procedureLead: 'procedure',
        procedure: ['Each completed Core Statement is awarded 5 marks.', 'An incomplete Core Statement at the end of an answer may merit 1-4 marks.'],
        perStatement: 5, incomplete: [1, 2, 3, 4],
      },
      oe: { max: 10, bands: [
        { label: 'Excellent', marks: [9, 10], printed: 'Excellent: 9-10 marks' },
        { label: 'Very good', marks: [7, 8], printed: 'Very good: 7-8 marks' },
        { label: 'Good', marks: [5, 6], printed: 'Good: 5-6 marks' },
        { label: 'Fair', marks: [3, 4], printed: 'Fair: 3-4 marks' },
        { label: 'Poor', marks: [0, 1, 2], printed: 'Poor: 0-2 marks' },
      ], directions: [] },
    },
  };
  const cs = (completed: number, incomplete?: number, oe?: number): HistoryEssayScores => ({
    'history:cm:statements': completed,
    ...(incomplete === undefined ? {} : { 'history:cm:incomplete': incomplete }),
    ...(oe === undefined ? {} : { [historyOeId]: oe }),
  });

  it('counts completed Core Statements at the printed value, an incomplete one at its printed marks, capped', () => {
    expect(tariffReconciles(core)).toBe(true);
    expect(historyEssayMarks(core, cs(3, 2, 7))).toBe(15 + 2 + 7);
    expect(historyEssayMarks(core, cs(6, 4, 10))).toBe(20 + 10);
    expect(historyCmTally(core.rubric, cs(6, 4)).statements).toEqual({ completed: 6, completedMarks: 30, incomplete: 4, raw: 34 });
    // An incomplete Core Statement is worth less than a complete one; 5 is not printed for it.
    expect(historyEssayMarks(core, cs(0, 5))).toBe(0);
    expect(historyEssayMarks(core, cs(2.5, undefined, 8))).toBe(8);
    expect(tariffReconciles({ ...core, rubric: { ...core.rubric, cm: { ...core.rubric.cm, incomplete: [1, 2, 5] } as typeof core.rubric.cm } })).toBe(false);
  });

  it('marks an Ordinary Q4 with no OE as placed once the CM is', () => {
    const q4 = { ...core, totalMarks: 20, rubric: { ...core.rubric, oe: undefined } };
    expect(tariffReconciles(q4)).toBe(true);
    expect(historyEssayMarks(q4, cs(4))).toBe(20);
    expect(historyEssayMarks(q4, cs(1, 3, 10))).toBe(8);
  });

  it('applies the one ceiling the student picks from a NOTE that prints several', () => {
    const three = structuredClone(famine);
    three.rubric.cm.elementRule = { note: 'NOTE: THREE elements (why + how + outcome) If only ONE, Max. CM = 40 If only TWO, Max. CM = 50',
      caps: [{ when: 'If only ONE', max: 40 }, { when: 'If only TWO', max: 50 }] };
    const full = placed([12, 12, 12, 12, 12], 30);
    expect(historyEssayMarks(three, full)).toBe(90);
    expect(historyEssayMarks(three, { ...full, [historyCapId]: 1 })).toBe(70);
    expect(historyEssayMarks(three, { ...full, [historyCapId]: 2 })).toBe(80);
    expect(historyEssayMarks(three, { ...full, [historyCapId]: 3 })).toBe(90);
  });
});

describe('the documents question’s own note on Q4 (2018, 2019 Higher)', () => {
  it('carries 2018’s elements and its one-element ceiling as the question’s element rule', () => {
    const rte = byId('hist-2018-hl-lm-s1-q4');
    expect(rte.rubric.cm.max).toBe(24);
    expect(rte.rubric.cm.elementRule?.caps).toEqual([{ when: 'if only one element is treated', max: 20 }]);
    expect(rte.rubric.cm.elementRule?.note.split('\n')).toEqual([
      'There are two elements in this question:',
      'To what extent did RTÉ entertain and to what extent did it challenge its viewers?',
      'Entertaining = music, comedy, etc',
      'Challenging = provocative current affairs, documentaries, etc',
      'There were also programmes, such as the Late Late Show, which combined the entertaining and the challenging.',
      'Max of 20 marks CM if only one element is treated',
    ]);
    expect(tariffReconciles(rte)).toBe(true);
  });

  it('reads 2017’s NOTE on Q4 as an essay’s, and its OE direction as printed', () => {
    const jarrow2017 = byId('hist-2017-hl-lm-s1-q4');
    expect(jarrow2017.rubric.cm.elementRule).toEqual({
      note: 'NOTE: TWO elements (What were the aims + to what extent were they achieved) If only ONE, Max. CM = 20',
      caps: [{ when: 'If only ONE', max: 20 }],
    });
    expect(jarrow2017.rubric.oe?.directions).toContain(
      'Material which narrates the day-to-day events of the Jarrow March without reference to the question’s two elements = no more than Fair on OE');
    // The maxima the scheme restates above its NOTE are not a statement of how it marks.
    expect(jarrow2017.rubric.schemeGuidance).toEqual([
      'In question 4, marking by paragraph begins.',
      'The examiner will divide the answer into paragraphs or paragraph equivalents.',
    ]);
  });

  it('keeps 2019’s elements, which print no ceiling, as a direction', () => {
    const laois = byId('hist-2019-hl-em-s1-q4');
    expect(laois.rubric.cm.elementRule).toBeUndefined();
    expect(laois.rubric.cm.directions[0].split('\n')).toEqual([
      'There are two elements in this question:',
      'What was the policy of plantation in Laois/Offaly?',
      'To what extent was it successful?',
    ]);
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
    const toggle = screen.getByRole('button', { name: /In my judgement, the note’s “If only ONE” applies to my answer/ });
    expect(toggle).toHaveAttribute('aria-pressed', 'false');
    fireEvent.click(toggle);
    expect(onScore).toHaveBeenCalledWith(historyCapId, 1);
    unmount();
    render(<HistoryEssayPanel card={science} scores={{}} onScore={vi.fn()} />);
    expect(screen.queryByRole('button', { name: /In my judgement, the note’s/ })).not.toBeInTheDocument();
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

  it('suggests no grade until the whole answer is placed on an OE band', () => {
    render(<SessionScreen cards={[famine]} subjectLabel="History" onGrade={vi.fn()} onFinish={vi.fn()} onExit={vi.fn()} />);
    fireEvent.click(screen.getByRole('button', { name: /Reveal the marking scheme/i }));
    for (const mark of [12, 10]) {
      fireEvent.click(screen.getByRole('button', { name: /^Add (a|another) paragraph$/ }));
      const ladders = screen.getAllByRole('group', { name: /^Bands for paragraph/ });
      fireEvent.click(within(ladders.at(-1)!).getByRole('button', { name: new RegExp(`^Claim ${mark} marks for`) }));
    }
    // Two paragraphs, no OE: a running total, not a placement.
    expect(screen.getByText(/Your History essay placement is not finished/)).toBeInTheDocument();
    expect(screen.queryByText(/that looks like/)).not.toBeInTheDocument();
    expect(document.querySelector('[data-suggested]')).toBeNull();
    const oe = screen.getByRole('group', { name: 'Overall Evaluation bands' });
    fireEvent.click(within(oe).getByRole('button', { name: 'Claim 30 marks for Very good: 28-33 marks' }));
    expect(screen.getByText(/Your History essay placement is 52 of 100 marks/)).toBeInTheDocument();
    expect(document.querySelector('[data-suggested]')).not.toBeNull();
  });
});
