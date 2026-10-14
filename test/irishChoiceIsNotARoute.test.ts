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

  it('gives an optional film or play one card when both file under one Atlas heading', () => {
    // Choose-one refinement (2026-10-12), decided by the Atlas mapping: the optional film and the
    // optional play share one grid and one heading (irish-4-7), so one card carries both printed
    // alternatives. Prescribed Cáca Milis / An Lasair Choille file under different headings and stay apart.
    expect(raw.filter(c => /-prose-2b-[a-c]-(scannan|drama)$/.test(c.id)).map(c => c.id)).toEqual([]);
    const filmOrPlay = raw.filter(c => /^irish-20\d\d-(hl|ol)-p2-prose-2b-[a-c]$/.test(c.id) && /scannán roghnach/.test(c.questionText));
    expect(filmOrPlay.map(c => c.id).sort()).toEqual(['irish-2021-ol-p2-prose-2b-b', 'irish-2022-hl-p2-prose-2b-a', 'irish-2023-ol-p2-prose-2b-c',
      'irish-2024-hl-p2-prose-2b-a', 'irish-2024-ol-p2-prose-2b-c', 'irish-2026-hl-p2-prose-2b-a', 'irish-2026-ol-p2-prose-2b-a']);
    for (const card of filmOrPlay) expect(card.questionText, card.id).toMatch(/dráma roghnach/);
    // Prescribed Cáca Milis and An Lasair Choille keep a card each (different headings).
    for (const card of raw.filter(c => /-prose-2a-[ac](-caca-milis)?$/.test(c.id) && /^Cáca Milis$/m.test(c.questionText))) {
      expect(card.questionText, card.id).not.toMatch(/^An Lasair Choille$/m);
    }
  });

  it('carries each printed choose-N instruction on every option it governs', () => {
    const governed: [string, Raw[], RegExp][] = [
      ['OL Paper 1 titles', raw.filter(c => /^irish-20(23|24|25|26)-ol-p1-composition-[a-d]-i{1,3}$/.test(c.id)),
        /^Freagair do rogha dhá cheann de A, B, C, D anseo\.$/],
      ['2026 OL Paper 2 routes', raw.filter(c => /^irish-2026-ol-p2-(prose-2[ab]-[a-c](-caca-milis|-an-lasair-choille)?|poetry-3[ab]-[a-c])$/.test(c.id)),
        /^Freagair do rogha dhá cheann as \(a\), \(b\) nó \(c\)\.$/],
      ['2025 OL Paper 2 options and sub-questions', raw.filter(c => /^irish-2025-ol-p2-(prose-2[ab]-[a-c]|poetry-3[ab]-[a-c](-i{1,3}(-[a-c])?)?)$/.test(c.id)),
        /^Freagair do rogha dhá cheann as \(a\), \(b\) nó \(c\)( thíos)?\.$/],
      ['2024 OL Paper 2 options and sub-questions', raw.filter(c => /^irish-2024-ol-p2-(prose-2[ab]-[a-c]|prose-2a-c-an-lasair-choille|prose-2a-[ab]-(i{1,3}|iv|v)|poetry-3[ab]-[a-c](-i{1,3}(-[a-d])?)?)$/.test(c.id)),
        /^Freagair do rogha dhá cheann as \(a\), \(b\) nó \(c\)( thíos)?\.$/],
      ['2023 OL Paper 2 options and sub-questions', raw.filter(c => /^irish-2023-ol-p2-(prose-2[ab]-[a-c]|prose-2a-c-an-lasair-choille|prose-2a-a-(i{1,3}|iv|v)|poetry-3[ab]-[a-c](-i{1,3})?)$/.test(c.id)),
        /^Freagair do rogha dhá cheann as \(a\), \(b\) nó \(c\)( thíos)?\.$/],
      ['Foundation reading parts', raw.filter(c => /^irish-20\d\d-fl-r-[23][a-c]-\d$/.test(c.id)),
        /^Ceist [23] Freagair do rogha dhá cheann de \(a\), \(b\), \(c\) anseo thíos\.$/],
    ];
    expect(governed.map(([name, cards]) => [name, cards.length])).toEqual([
      ['OL Paper 1 titles', 36], ['2026 OL Paper 2 routes', 13], ['2025 OL Paper 2 options and sub-questions', 24], ['2024 OL Paper 2 options and sub-questions', 36], ['2023 OL Paper 2 options and sub-questions', 27],
      ['Foundation reading parts', 510],
    ]);
    for (const [, cards, instruction] of governed) {
      for (const card of cards) expect(card.taskRequirements?.[0], card.id).toMatch(instruction);
    }
  });
});
