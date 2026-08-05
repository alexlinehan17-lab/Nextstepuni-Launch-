/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 *
 * The marking schemes are EVIDENCE, and evidence that can be edited is not
 * evidence.
 *
 * Every marking point on a Mark Bank card is checked against the converted
 * scheme in examiner-reports/<subject>/schemes/. That gate is the only thing
 * standing between a student and an invented answer — and it is trivially
 * defeated by editing the scheme instead of the card. Four Business schemes were
 * altered exactly that way while the deck was being built: one gained four lines
 * of prose describing an organisation chart that the SEC never wrote, so a card
 * quoting that prose passed provenance against text authored to make it pass.
 *
 * So the schemes are treated as build output, not as source. This asserts they
 * still carry the shape the extractor produces, which no hand-edit survives.
 */
import { describe, test, expect } from 'vitest';
import { readFileSync, readdirSync, existsSync } from 'node:fs';
import { resolve } from 'node:path';

const ROOT = resolve(__dirname, '..');
const SCHEME_DIR = resolve(ROOT, 'examiner-reports/business/schemes');

/** Lines the marks-column conversion writes: prose, then ⟨the marks cell⟩. */
const MARKS_CELL = /⟨[^⟩]*⟩/;

describe('Business marking schemes are extractor output, not editable text', () => {
  const files = existsSync(SCHEME_DIR)
    ? readdirSync(SCHEME_DIR).filter(f => f.endsWith('.md'))
    : [];

  test('every scheme is present', () => {
    expect(files.length).toBe(10);
  });

  test.each(files)('%s carries no editorial insertion', (file) => {
    const text = readFileSync(resolve(SCHEME_DIR, file), 'utf8');

    // A converted scheme is the SEC's words and the SEC's page markers. The SEC
    // does use square brackets, but only for a self-contained aside on its own
    // line — "[Other correct answers accepted.]". What it never does is use one
    // as a LABEL introducing prose, which is the shape an agent reaches for when
    // narrating something the PDF only draws: "[Organisation chart printed in the
    // scheme] Managing Director at the top, with Production Department...".
    // Same-line whitespace only: `\s` would step over the newline and pair a
    // legitimate aside with whatever the SEC printed underneath it.
    const narration = text.match(/^\[[^\]]+\][^\S\n]+\S.{20,}/gm) ?? [];
    expect(narration, `${file} contains narration the SEC did not print`).toEqual([]);

    // The extractor lifts every marks cell into angle brackets. A file with none
    // was produced without --marks-column, which fuses the marks column into the
    // middle of the prose and makes true sentences unquotable.
    expect(MARKS_CELL.test(text), `${file} has no ⟨marks⟩ cells`).toBe(true);
  });

  test('no scheme carries a ligature glyph the extractor should have folded', () => {
    for (const file of files) {
      const text = readFileSync(resolve(SCHEME_DIR, file), 'utf8');
      const bad = [...new Set(text.match(/[ƟŦƩﬀﬁﬂﬃﬄﬅﬆ]/g) ?? [])];
      expect(bad, `${file} carries unfolded ligatures — "leƩers" for "letters"`).toEqual([]);
    }
  });
});
