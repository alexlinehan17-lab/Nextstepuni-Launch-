/** @license SPDX-License-Identifier: Apache-2.0 */
import { execFileSync } from 'node:child_process';
import { existsSync, readFileSync, readdirSync } from 'node:fs';
import { resolve } from 'node:path';
import { describe, expect, it } from 'vitest';
import { CARDS as HIGHER } from '../components/MarkBank/cards/business/higher';
import { CARDS as ORDINARY } from '../components/MarkBank/cards/business/ordinary';
import authored from '../scripts/markbank/authored/business.json';
import supplement from '../components/MarkBank/cards/business/rubric-authored.json';
import routePools from '../components/MarkBank/cards/business/route-pools.json';
import glyphIds from '../scripts/markbank/authoring/glyph_ids.json';
import corpusInventory from '../scripts/markbank/authored/business-corpus-inventory.json';

// What a broken subset font leaves in a PDF's text layer: Latin Extended
// ("seƫng" for setting, "ouƞlows", "aŌer"), Greek ("Certiϐicate"), the blocks a
// subset borrows, private use (Wingdings ticks and numbered markers), the
// ligature presentation forms and U+FFFD. A Business scheme prints none of them,
// so any one in a card or a scheme .md is an extraction fault, not content.
// Built from code points so this file itself carries none of them.
const span = (a: number, b: number) => `${String.fromCodePoint(a)}-${String.fromCodePoint(b)}`;
// A CID font with no ToUnicode leaves its glyph ids instead: control characters
// ("\x03" for a space) and plain ASCII ("/($9,1*" for "LEAVING"). The control
// characters are caught here too; the ASCII is caught by the glyph-id check below.
const MANGLED = new RegExp(`[${span(0x0100, 0x1fff)}${span(0xe000, 0xf8ff)}${span(0xfb00, 0xfb4f)}${String.fromCodePoint(0xfffd)}`
  + `${span(0x00, 0x08)}${span(0x0b, 0x0c)}${span(0x0e, 0x1f)}${String.fromCodePoint(0x7f)}]`, 'gu');
const hasPdfParser = (() => {
  try { execFileSync('python3', ['-c', 'import pymupdf'], { stdio: 'ignore' }); return true; }
  catch { return false; }
})();
// The SEC PDFs are local-only (never committed, never on CI). The glyph scan
// runs only when every English Business paper and scheme is on disk.
const englishDocuments = corpusInventory.documents.filter(document => document.language === 'ev');
const hasBusinessCorpus = existsSync(resolve(__dirname, '../paper-trail-corpus')) && englishDocuments.length === 48
  && englishDocuments.every(document => existsSync(resolve(__dirname, `../paper-trail-corpus/exampapers/${document.year}/${document.paperFileid}`))
    && existsSync(resolve(__dirname, `../paper-trail-corpus/markingschemes/${document.year}/${document.schemeFileid}`)));

const SCHEME_DIR = resolve(__dirname, '../examiner-reports/business/schemes');
const label = (ch: string) => `U+${ch.codePointAt(0)!.toString(16).toUpperCase().padStart(4, '0')}`;

/** Every string anywhere in a value, with the path that reaches it. */
function strings(value: unknown, path: string, out: [string, string][] = []): [string, string][] {
  if (typeof value === 'string') out.push([path, value]);
  else if (Array.isArray(value)) value.forEach((item, i) => strings(item, `${path}[${i}]`, out));
  else if (value && typeof value === 'object') {
    for (const [key, item] of Object.entries(value)) strings(item, `${path}.${key}`, out);
  }
  return out;
}

function offenders(value: unknown, path: string) {
  return strings(value, path).flatMap(([where, text]) => {
    const hits = [...new Set(text.match(MANGLED) ?? [])];
    return hits.length ? [`${where}: ${hits.map(label).join(' ')}`] : [];
  });
}

describe('Business text carries no broken-font glyph', () => {
  it('no shipped Business card, in either deck, carries one in any field', () => {
    expect(offenders([...HIGHER, ...ORDINARY], 'deck')).toEqual([]);
  });

  it('no Business card source carries one: reviewed cards, route pools, or the legacy cards and their notes', () => {
    expect(offenders(supplement, 'rubric-authored')).toEqual([]);
    expect(offenders(routePools, 'route-pools')).toEqual([]);
    expect(offenders(authored, 'business.json')).toEqual([]);
  });

  it('no Business scheme .md carries one', () => {
    const files = readdirSync(SCHEME_DIR).filter(file => file.endsWith('.md'));
    expect(files.length).toBeGreaterThan(0);
    const found = files.flatMap(file => {
      const hits = [...new Set(readFileSync(resolve(SCHEME_DIR, file), 'utf8').match(MANGLED) ?? [])];
      return hits.length ? [`${file}: ${hits.map(label).join(' ')}`] : [];
    });
    expect(found, 'repair with scripts/markbank/authoring/repair_scheme_glyphs.py; extract with --glyph-ids').toEqual([]);
  });

  it.skipIf(!(hasPdfParser && hasBusinessCorpus))('reads every glyph a CID font draws with no Unicode, in every English Business paper and scheme, by its glyph id', () => {
    // rawdict reports such a glyph's id as its character, so a stand-in like
    // "/($9,1*" is plain ASCII that no character gate can see. Every one must
    // resolve in glyph_ids.json, so the scheme extractor (--unnamed-glyphs) and
    // the card generators (bus_lib) read the printed words.
    const result = JSON.parse(execFileSync('python3', ['-c', `
import glob,json,sys
sys.path.insert(0,'scripts/markbank')
import pymupdf
from glyph_ids import load_table,page_glyphs,page_unnamed
table=load_table()
pymupdf.TOOLS.mupdf_display_errors(False)
# The Business card corpus: June sittings from 2010. The shared local corpus
# also holds the 1995-2009 archive papers, which no card is drawn from.
files=sorted(f for f in glob.glob('paper-trail-corpus/markingschemes/*/LC033*EV.pdf')+glob.glob('paper-trail-corpus/exampapers/*/LC033*EV.pdf') if int(f.split('/')[2])>=2010)
seen,missing=0,{}
for f in files:
    with pymupdf.open(f) as d:
        for n,page in enumerate(d,1):
            unnamed=page_unnamed(page)
            if not unnamed: continue
            origin=page_glyphs(page)
            for key in unnamed:
                seen+=1
                fam,gid=origin.get(key,('?',-1))
                if f'{fam}|{gid}' not in table['gid'] and f'{fam}|{gid}' not in table['cid']: missing.setdefault(f'{fam}|{gid}',f'{f} p{n}')
print(json.dumps({'files':len(files),'seen':seen,'missing':missing}))
`], { encoding: 'utf8' }));
    expect(result.files).toBeGreaterThanOrEqual(80);
    expect(result.seen).toBeGreaterThan(0);
    expect(result.missing).toEqual({});
  }, 120_000);

  it('reads every repaired glyph by its font and glyph id or a settled code point, never a bare character', () => {
    const keys = [...glyphIds.byGlyphId.map(e => `${e.font}|${e.gid}`), ...glyphIds.byCodePoint.map(e => `${e.font}|${e.code}`),
      ...glyphIds.byCidGlyphId.map(e => `${e.font}|${e.gid}`)];
    expect(new Set(keys).size).toBe(keys.length);
    for (const entry of [...glyphIds.byGlyphId, ...glyphIds.byCodePoint, ...glyphIds.byCidGlyphId]) {
      expect(entry.text.length, JSON.stringify(entry)).toBeGreaterThan(0);
      expect(entry.text.match(MANGLED), JSON.stringify(entry)).toBeNull();
      expect(entry.evidence, JSON.stringify(entry)).toMatch(/^(derived: \d+ sane sighting|settled by crop: )/);
    }
    // The Calibri ligatures that Business schemes mangle, as their glyphs read.
    const gid = Object.fromEntries(glyphIds.byGlyphId.filter(e => e.font === 'Calibri').map(e => [e.gid, e.text]));
    expect([gid[332], gid[414], gid[415], gid[425], gid[427]]).toEqual(['ft', 'tf', 'ti', 'tt', 'tti']);
  });
});
