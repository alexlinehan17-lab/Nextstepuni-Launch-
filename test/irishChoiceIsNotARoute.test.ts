/**
 * Choice is not a route (coordinator rule, 2026-10-12).
 *
 * When the candidate chooses which printed options to answer — "Freagair do
 * rogha dhá cheann …", "Freagair dhá cheist ar bith …", "(a) NÓ (b)" — the
 * Bank publishes one card per printed option and carries the instruction in
 * its task requirements. Sessions do not collapse route siblings, so a card
 * per COMBINATION of options floods the deck (300 had accumulated across the
 * Irish papers). This guard keeps them from coming back.
 */
import { describe, expect, it } from 'vitest';
import { readdirSync, readFileSync } from 'node:fs';
import { CARDS as HIGHER } from '../components/MarkBank/cards/irish/higher';
import { CARDS as ORDINARY } from '../components/MarkBank/cards/irish/ordinary';
import { CARDS as FOUNDATION } from '../components/MarkBank/cards/irish/foundation';

type Raw = { id: string; questionText: string; questionRef: string; atlasQuestionId?: string; memberCardIds?: string[]; taskRequirements?: string[] };
const DIR = 'components/MarkBank/cards/irish';
const files = readdirSync(DIR).filter(name => name.endsWith('.json'));
const raw: Raw[] = files.flatMap(name => (JSON.parse(readFileSync(`${DIR}/${name}`, 'utf8')) as { cards: Raw[] }).cards);

describe('Irish: choice is not a route', () => {
  it('publishes no per-combination card in any Irish card file', () => {
    expect(files.length).toBeGreaterThan(20);
    expect(raw.filter(c => c.memberCardIds).map(c => c.id)).toEqual([]);
    // A card that joins two printed options ("A(i) + B(i)", "R-2-AB", "--b") is a combination even without member ids.
    const joined = raw.filter(c => /An rogha don chárta seo:[^\n]*\+/.test(c.questionText)
      || / \+ /.test(c.questionRef) || /--|^R-\d-[A-C]{2}$|^W-\d[AB]-\d[AB]/.test(c.atlasQuestionId ?? ''));
    expect(joined.map(c => c.id)).toEqual([]);
  });

  it('keeps the runtime decks free of combination cards too', () => {
    const deck = [...HIGHER, ...ORDINARY, ...FOUNDATION];
    expect(deck.filter(c => / \+ /.test(c.questionRef)).map(c => c.id)).toEqual([]);
    expect(deck.length).toBe(raw.length);
  });

  it('carries each printed choose-N instruction on every option it governs', () => {
    const governed: [string, Raw[], RegExp][] = [
      ['OL Paper 1 titles', raw.filter(c => /^irish-20(25|26)-ol-p1-composition-[a-d]-i{1,3}$/.test(c.id)),
        /^Freagair do rogha dhá cheann de A, B, C, D anseo\.$/],
      ['2026 OL Paper 2 routes', raw.filter(c => /^irish-2026-ol-p2-(prose-2[ab]-[a-c](-caca-milis|-an-lasair-choille|-scannan|-drama)?|poetry-3[ab]-[a-c])$/.test(c.id)),
        /^Freagair do rogha dhá cheann as \(a\), \(b\) nó \(c\)\.$/],
      ['Foundation reading parts', raw.filter(c => /^irish-20\d\d-fl-r-[23][a-c]-\d$/.test(c.id)),
        /^Ceist [23] Freagair do rogha dhá cheann de \(a\), \(b\), \(c\) anseo thíos\.$/],
    ];
    expect(governed.map(([name, cards]) => [name, cards.length])).toEqual([
      ['OL Paper 1 titles', 18], ['2026 OL Paper 2 routes', 14], ['Foundation reading parts', 510],
    ]);
    for (const [, cards, instruction] of governed) {
      for (const card of cards) expect(card.taskRequirements?.[0], card.id).toMatch(instruction);
    }
  });
});
