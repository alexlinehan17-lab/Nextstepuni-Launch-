/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 *
 * Irish parts whose scheme pays two pieces in a printed order (cards/irish/tariffs.ts printedOrder, coordinator rulings
 * of 12 Nov): what each claim scores, through the app's own scoring (irishScoring.ts).
 */
import { describe, expect, test } from 'vitest';
import { irishCriterionMarks, irishPartCount, irishRowScoreId } from '@/components/MarkBank/irishScoring';
import { PRINTED_ORDER_KEYS } from '@/components/MarkBank/cards/irish/tariffs';
import { isRubricCard, type IrishCriterion } from '@/types/markBank';
import { CARDS as IRISH_ORDINARY } from '@/components/MarkBank/cards/irish/ordinary';

const criterionOf = (key: string): IrishCriterion => {
  const [cardId, criterionId] = key.split('::');
  const card = IRISH_ORDINARY.find(candidate => candidate.id === cardId);
  if (!card || !isRubricCard(card) || card.rubric.system !== 'irish') throw new Error(`no Irish card ${cardId}`);
  return card.rubric.criteria.find(criterion => criterion.id === criterionId)!;
};

/** The criterion's mark when exactly these rows (by printed text) are claimed. */
const score = (criterion: IrishCriterion, texts: string[]) => {
  const part = criterion.allocation!.parts[0];
  const ids = texts.map(text => {
    const row = part.rows.find(candidate => candidate.text === text);
    if (!row) throw new Error(`no row "${text}" in ${criterion.id}`);
    return row.id;
  });
  return irishCriterionMarks(criterion, Object.fromEntries(ids.map(id => [irishRowScoreId(criterion.id, part.id, id), 1])));
};

describe('two pieces with a full row of both: the part counts up to two claimed rows, capped at 5', () => {
  // "Nóta: Má tá dhá phointe eolais i gceist, tá 3 mharc ar an gcéad cheann atá ceart agus 2 mharc ar an dara ceann atá ceart."
  test.each(['irish-2025-ol-deferred-p2-reading-a-q1::a', 'irish-2025-ol-deferred-p2-reading-a-q1-a::a'])('%s', key => {
    const criterion = criterionOf(key);
    expect(criterion.allocation!.parts).toHaveLength(1);
    expect(irishPartCount(criterion.allocation!.parts[0])).toBe(2);
    const full = 'Ionadaithe ó chlub píobairí Shráid Thomáis i mBaile Átha Cliath agus daoine as Contae na hIarmhí a raibh baint mhór acu leis an gceol traidisiúnta';
    const first = 'Ionadaithe ó chlub píobairí Shráid Thomáis i mBaile Átha Cliath';
    const second = 'Daoine as Contae na hIarmhí a raibh baint mhór acu leis an gceol traidisiúnta';
    expect(score(criterion, [full])).toBe(5);
    expect(score(criterion, [first])).toBe(3);
    expect(score(criterion, [second])).toBe(3);
    // Before the ruling the part counted one row, so both pieces paid 3.
    expect(score(criterion, [first, second])).toBe(5);
    expect(score(criterion, [full, first])).toBe(5);
    expect(score(criterion, [full, first, second])).toBe(5);
    // The scheme's own part-right answer keeps its printed 2.
    expect(score(criterion, ['Daoine as Contae na hIarmhí'])).toBe(2);
  });

  // "Dúil mhór sa tsaoirse = 3 mharc", "Creideamh láidir (i nDia) = 2 mharc", "An chéad mhír atá ceart = 3 mharc"
  test.each(['irish-2013-ol-p2-reading-a-q5::a', 'irish-2013-ol-p2-reading-a-q5-a::a'])('%s', key => {
    const criterion = criterionOf(key);
    expect(irishPartCount(criterion.allocation!.parts[0])).toBe(2);
    const full = 'D’fhág Patrick Kennedy an ché sin i rith an Ghorta Mhóir agus thóg sé dhá rud thábhachtacha leis go Meiriceá-dúil mhór sa tsaoirse agus creideamh láidir i nDia';
    expect(score(criterion, [full])).toBe(5);
    expect(score(criterion, ['Dúil mhór sa tsaoirse'])).toBe(3);
    expect(score(criterion, ['Dúil mhór sa tsaoirse', 'Creideamh láidir (i nDia)'])).toBe(5);
    expect(score(criterion, [full, 'Dúil mhór sa tsaoirse'])).toBe(5);
    expect(score(criterion, [full, 'Dúil mhór sa tsaoirse', 'Creideamh láidir (i nDia)'])).toBe(5);
  });
});

describe('two printed lists, one item from each: a ladder [3, 5] over points, each list one point', () => {
  // "Rud amháin a rinne sé mar Uachtarán", "Rud amháin nár éirigh leis a dhéanamh = 2 mharc", "An chéad mhír atá ceart = 3 mharc"
  test.each(['irish-2013-ol-p2-reading-a-q4::b', 'irish-2013-ol-p2-reading-a-q4-b::b'])('%s', key => {
    const criterion = criterionOf(key);
    const [part] = criterion.allocation!.parts;
    expect(criterion.allocation!.parts).toHaveLength(1);
    expect(part).toMatchObject({ tariff: 5, ladder: [3, 5] });
    expect(new Set(part.rows.map(row => row.group))).toEqual(new Set(['list-1', 'list-2']));
    const did = '“Thosaigh sé cainteanna.”';
    const didAlso = '“Chabhraigh sé leis na daoine gorma.”';
    const failed = '“Ní raibh sé dílis dá bhean.”';
    const failedAlso = '“Níor éirigh leis Meiriceá a choimeád amach as an gcogadh.”';
    // The first right item earns 3, whichever list it is from.
    expect(score(criterion, [did])).toBe(3);
    expect(score(criterion, [failed])).toBe(3);
    // An item from the other list makes 5.
    expect(score(criterion, [did, failed])).toBe(5);
    // Two from the same list stay at 3.
    expect(score(criterion, [did, didAlso])).toBe(3);
    expect(score(criterion, [failed, failedAlso])).toBe(3);
    expect(score(criterion, [did, didAlso, failed])).toBe(5);
  });
});

test('the overrides are exactly the six ruled criteria', () => {
  expect([...PRINTED_ORDER_KEYS].sort()).toEqual([
    'irish-2013-ol-p2-reading-a-q4-b::b', 'irish-2013-ol-p2-reading-a-q4::b', 'irish-2013-ol-p2-reading-a-q5-a::a',
    'irish-2013-ol-p2-reading-a-q5::a', 'irish-2025-ol-deferred-p2-reading-a-q1-a::a', 'irish-2025-ol-deferred-p2-reading-a-q1::a',
  ]);
});
