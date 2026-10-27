/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 *
 * Irish exact answers as claimable rows (cards/irish/answers.ts): the shapes
 * the parser reads, the cards it must leave alone, and how the rows score,
 * including on the combined listening sheet.
 */
import { fireEvent, render, screen } from '@testing-library/react';
import { describe, expect, it, vi } from 'vitest';
import { CARDS as HIGHER } from '../components/MarkBank/cards/irish/higher';
import { CARDS as ORDINARY } from '../components/MarkBank/cards/irish/ordinary';
import { parseIrishAnswers } from '../components/MarkBank/cards/irish/answers';
import SessionScreen, { irishMarks } from '../components/MarkBank/SessionScreen';
import { irishRowScoreId } from '../components/MarkBank/irishScoring';
import type { IrishAllocation, SecRubricCard } from '../types/markBank';

vi.mock('../components/PaperTrail/vaultDocs', () => ({ vaultPdf: vi.fn(() => new Promise(() => {})) }));

const cards = [...HIGHER, ...ORDINARY];
const byId = (id: string): SecRubricCard => {
  const card = cards.find(candidate => candidate.id === id);
  if (!card) throw new Error(`no card ${id}`);
  return card;
};
const allocationOf = (id: string): IrishAllocation => {
  const card = byId(id);
  const allocation = card.rubric.system === 'irish' ? card.rubric.criteria[0].allocation : undefined;
  if (!allocation) throw new Error(`${id} is not structured`);
  return allocation;
};
const parts = (allocation: IrishAllocation) =>
  allocation.parts.map(part => [part.prompt, part.tariff, part.ladder, part.rows.map(row => [row.text, row.marks])]);

describe('Irish scheme text becomes sub-questions and rows', () => {
  it('cuts a Higher listening fógra at its prices: prompt + tariff, answers at "= N mharc"', () => {
    expect(parts(allocationOf('irish-2021-hl-p1-listening-a-f1'))).toEqual([
      ['1. Cad atá á lorg ag Ollscoil na hÉireann, Gaillimh?', 2, undefined, [['Oifigeach Gaeilge', 2], ['Oifigeach', 1]]],
      ['2. Cén dualgas a bheidh ar an duine a cheapfar?', 2, undefined, [
        ['Imeachtaí a eagrú a chuirfidh an Ghaeilge chun cinn', 2], ['Imeachtaí a eagrú', 1],
        ['Imeachtaí Gaeilge (Gaelacha) a eagrú', 1], ['An Ghaeilge a chur chun cinn', 1],
      ]],
      ['3. Scríobh síos dhá cháilíocht atá riachtanach don phost seo.', 4, undefined, [
        ['Gaeilge líofa (den scoth/an-mhaith)', 2], ['Scileanna maithe cumarsáide', 2], ['Cumas maith eagrúcháin', 2],
        ['Gaeilge', 1], ['Scileanna cumarsáide', 1], ['Cumas eagrúcháin', 1],
      ]],
    ]);
  });

  it('reads an Ordinary grid where the answer comes before its tariff', () => {
    expect(parts(allocationOf('irish-2021-ol-p1-listening-a-f1'))).toEqual([
      ['Líon isteach an t-eolas atá á lorg sa ghreille anseo. Cén ollscoil a chuir amach an fógra seo?', 3, undefined,
        [['(Ollscoil) na hÉireann, Gaillimh', 3], ['Gaillimh', 3], ['Éireann/Éirinn/Éire', 2]]],
      ['Cén cineál Gaeilge atá riachtanach don phost seo?', 3, undefined, [['Líofa', 3]]],
      ['Cén tuarastal a gheobhaidh an duine a cheapfar?', 3, undefined, [['€30,000', 3], ['Tríocha míle', 3], ['30,000', 3]]],
      ['Cén seoladh ríomhphoist ar chóir litir iarratais a chur chuige?', 3, undefined, [['oifig@gaeilge.ie', 3]]],
    ]);
  });

  it('reads reading braces: "{3 mharc}" prices bullets, "3 mharc + 2 mharc = 5 mharc" is a ladder with rules as directions', () => {
    const higher = allocationOf('irish-2021-hl-p2-reading-a-q1');
    expect(higher.parts.map(part => [part.tariff, part.rows.length])).toEqual([[3, 2], [2, 4], [2, 2]]);
    expect(higher.parts[0].rows[0]).toMatchObject({ marks: 3 });
    const ordinary = allocationOf('irish-2021-ol-p2-reading-b-q1');
    expect(ordinary.parts.map(part => [part.tariff, part.ladder, part.rows.length])).toEqual([[5, [3, 5], 2], [5, [3, 5], 4]]);
    expect(ordinary.directions).toEqual([
      'An chéad ghaisce atá ceart', 'an dara gaisce atá ceart', 'An chéad chúis mhórtais atá ceart', 'an dara cúis mhórtais atá ceart',
    ]);
  });

  it('keeps the language rule as a direction and stops where the excerpt runs into the next section', () => {
    const allocation = allocationOf('irish-2022-hl-p1-listening-c-p2');
    expect(allocation.directions).toEqual(['Bainfear ó 0 go 3 ar chaighdeán na Gaeilge.']);
    expect(allocation.parts).toHaveLength(3);
    expect(allocation.parts.flatMap(part => part.rows).some(row => /Roinn ar an bpáipéar/.test(row.text))).toBe(false);
  });

  it('leaves alone an excerpt that starts mid-question, and the Q6 composite tariff', () => {
    const card = byId('irish-2022-hl-p2-reading-a-q2');
    if (card.rubric.system !== 'irish') throw new Error('not irish');
    expect(card.rubric.criteria[0].allocation).toBeUndefined();
    expect(parseIrishAnswers({ id: card.id, totalMarks: 7, questionRef: card.questionRef, questionText: card.questionText, guidance: card.rubric.criteria[0].guidance }))
      .toEqual({ ok: false, reason: 'tariffs add to 2, criterion is 7' });
    const q6 = byId('irish-2021-hl-p2-reading-a-q6');
    if (q6.rubric.system !== 'irish') throw new Error('not irish');
    expect(q6.rubric.criteria[0].allocation).toBeUndefined();
  });
});

describe('Irish rows score', () => {
  it('adds the highest claims per sub-question up to its tariff, and ladders by rows ticked', () => {
    const card = byId('irish-2021-hl-p1-listening-a-f1');
    const criterion = card.rubric.system === 'irish' ? card.rubric.criteria[0] : undefined;
    if (!criterion) throw new Error('not irish');
    const claim = (ids: [string, string][]) => Object.fromEntries(ids.map(([part, row]) => [irishRowScoreId(criterion.id, part, row), 1]));
    expect(irishMarks(card, claim([['p1', 'r1']]))).toBe(2);
    expect(irishMarks(card, claim([['p1', 'r2'], ['p2', 'r2']]))).toBe(2);
    expect(irishMarks(card, claim([['p3', 'r1'], ['p3', 'r2'], ['p3', 'r3']]))).toBe(4);
    expect(irishMarks(card, claim([['p1', 'r1'], ['p2', 'r1'], ['p3', 'r1'], ['p3', 'r4']]))).toBe(7);
    const ladder = byId('irish-2021-ol-p2-reading-b-q1');
    const ladderCriterion = ladder.rubric.system === 'irish' ? ladder.rubric.criteria[0] : undefined;
    if (!ladderCriterion) throw new Error('not irish');
    expect(irishMarks(ladder, { [irishRowScoreId(ladderCriterion.id, 'p1', 'r1')]: 1 })).toBe(3);
    expect(irishMarks(ladder, { [irishRowScoreId(ladderCriterion.id, 'p1', 'r1')]: 1, [irishRowScoreId(ladderCriterion.id, 'p1', 'r2')]: 1 })).toBe(5);
    // The legacy placed mark is ignored on a structured criterion.
    expect(irishMarks(card, { 'irish:eolas': 8 })).toBe(0);
  });

  it('claims rows on the combined listening sheet and grades each extract by its own rows', () => {
    const first = byId('irish-2021-hl-p1-listening-b-c1-first');
    const second = byId('irish-2021-hl-p1-listening-b-c1-second');
    const onGrade = vi.fn();
    render(<SessionScreen cards={[first, second]} subjectLabel="Irish" onGrade={onGrade} onFinish={vi.fn()} onExit={vi.fn()} />);
    fireEvent.click(screen.getByRole('button', { name: /Reveal the marking scheme/i }));
    fireEvent.click(screen.getByRole('button', { name: 'Gan taisteal thar lear · 2m' }));
    fireEvent.click(screen.getByRole('button', { name: 'Ghlac siad rothair ar cíos · 2m' }));
    fireEvent.click(screen.getByRole('button', { name: 'Got it' }));
    expect(onGrade).toHaveBeenCalledWith(expect.objectContaining({ cardId: first.id, marksClaimed: 2, marksAvailable: 8 }));
    expect(onGrade).toHaveBeenCalledWith(expect.objectContaining({ cardId: second.id, marksClaimed: 2, marksAvailable: 6 }));
  });
});
