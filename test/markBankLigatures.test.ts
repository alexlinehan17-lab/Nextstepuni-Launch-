/** @license SPDX-License-Identifier: Apache-2.0 */
import { readFileSync, readdirSync, existsSync } from 'node:fs';
import { resolve } from 'node:path';
import { describe, expect, it } from 'vitest';
import glyphIds from '../scripts/markbank/authoring/glyph_ids.json';
import glyphMap from '../scripts/markbank/authoring/glyphmap.json';
import ligatureWords from '../scripts/markbank/authoring/ligature_words.json';

/*
 * Calibri draws "tt", "tti", "ti", "tf" and "tí" as single ligature glyphs.
 * Broken subsets report them as U+01A9, U+01AB, U+019F, U+019E and U+01A1,
 * and honest ones as the presentation forms U+FB00-U+FB06. None of them is a
 * letter a card should show, and for two of them the shared character map had
 * the wrong letters: it turned "seƫng" into "settng" and "boƩles" into
 * "botles" in shipped cards. Built from code points so this file carries none.
 */
const cp = (n: number) => String.fromCodePoint(n);
const LIGATURE_CODEPOINTS = new RegExp(
  `[${cp(0x019e)}${cp(0x019f)}${cp(0x01a1)}${cp(0x01a9)}${cp(0x01ab)}${cp(0xfb00)}-${cp(0xfb06)}]`, 'gu');

const CARDS = resolve(__dirname, '../components/MarkBank/cards');
const decks = readdirSync(CARDS, { withFileTypes: true })
  .filter(entry => entry.isDirectory())
  .flatMap(entry => ['higher.ts', 'ordinary.ts']
    .map(file => resolve(CARDS, entry.name, file))
    .filter(existsSync)
    .map(path => ({ subject: entry.name, path, text: readFileSync(path, 'utf8') })));
// Decks generated at runtime (Art, English, Geography, ...) keep their card text in
// JSON beside the module, so the code-point scan reads those sources too.
const jsonSources = readdirSync(CARDS, { withFileTypes: true })
  .filter(entry => entry.isDirectory())
  .flatMap(entry => readdirSync(resolve(CARDS, entry.name))
    .filter(file => file.endsWith('.json'))
    .map(file => resolve(CARDS, entry.name, file)))
  .map(path => ({ path, text: readFileSync(path, 'utf8') }));

// Identifier fields are keys, never shown; a concept id coined from a misread
// stem stays as it is so nothing that refers to it is orphaned.
const IDENTIFIER = /\b(?:id|conceptId|topicId|figureKey|questionFigureKey|labelKey): "(?:[^"\\]|\\.)*"/g;
const printed = (text: string) => text.replace(IDENTIFIER, '');

const label = (ch: string) => `U+${ch.codePointAt(0)!.toString(16).toUpperCase().padStart(4, '0')}`;
const escape = (word: string) => word.replace(/[.*+?^${}()|[\]\\]/g, '\\$&');

describe('Mark Bank ligature glyphs', () => {
  it('no deck, in any subject, ships a ligature glyph code point', () => {
    expect(decks.length).toBeGreaterThan(40);
    expect(jsonSources.map(({ path }) => path.split('/cards/')[1])).toContain('art/authored.json');
    const found = [...decks, ...jsonSources].flatMap(({ path, text }) => {
      const hits = [...new Set(text.match(LIGATURE_CODEPOINTS) ?? [])];
      return hits.length ? [`${path.split('/cards/')[1]}: ${hits.map(label).join(' ')}`] : [];
    });
    expect(found).toEqual([]);
  });

  it('no repaired subject ships a word its text layer misread', () => {
    const words = ligatureWords as Record<string, Record<string, string>>;
    // Every subject whose deck shipped a misread word before the repair. Applied
    // Maths cannot be rebuilt locally, so its deck was repaired in place
    // (patch_deck_ligatures.py) and its authored card through card-corrections.json.
    for (const subject of ['applied-maths', 'business', 'chemistry', 'latin', 'physics', 'portuguese',
      'religious-education', 'technology']) {
      expect(Object.keys(words[subject] ?? {}).length, subject).toBeGreaterThan(0);
    }
    const found = decks.flatMap(({ subject, path, text }) => Object.keys(words[subject] ?? {})
      .filter(word => new RegExp(`(?<![\\p{L}\\p{N}_])${escape(word)}(?![\\p{L}\\p{N}_])`, 'u').test(printed(text)))
      .map(word => `${path.split('/cards/')[1]}: "${word}" (printed "${words[subject][word]}")`));
    expect(found).toEqual([]);
  });

  it('ships Applied Maths 2024 Higher with the printed words and a correction its build will keep', () => {
    const deck = readFileSync(resolve(CARDS, 'applied-maths/higher.ts'), 'utf8');
    for (const word of ['labelled with the letters A to L', 'The letters used to label the edges', 'is attached to one end',
      'is attached to the other end', 'The algebraic formula below is written in terms of']) {
      expect(deck, word).toContain(word);
    }
    const corrections = JSON.parse(readFileSync(resolve(__dirname, '../scripts/markbank/card-corrections.json'), 'utf8'));
    const text = corrections['applied-maths']['am-2024-hl-8-b'].set.questionText as string;
    expect(text).toContain('is written in terms of');
    expect(deck).toContain(`questionText: ${JSON.stringify(text)}`);
  });

  it('reads the tt and tti ligatures by glyph id, and the character map agrees', () => {
    const gid = Object.fromEntries(glyphIds.byGlyphId.filter(e => e.font === 'Calibri').map(e => [e.gid, e.text]));
    expect(gid[425]).toBe('tt');
    expect(gid[427]).toBe('tti');
    const map = glyphMap as Record<string, string>;
    // Every U+01A9 and U+01AB in the corpus is Calibri gid 425 and 427.
    expect(map[cp(0x01a9)]).toBe('tt');
    expect(map[cp(0x01ab)]).toBe('tti');
  });
});
