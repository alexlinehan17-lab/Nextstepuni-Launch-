"""Source-only, in-memory repair of hash-bound 2010 Higher scheme fonts.

Times glyphs are matched against the same sitting's original paper. The two
short Cambria spans are transcribed from full-size original scheme pages5/10,
with repeated glyphs required to have identical readings. No PDF is rewritten.
"""
import hashlib
import json
from pathlib import Path
import fitz

ROOT=Path(__file__).resolve().parents[3]
REVIEW = json.loads((ROOT/'scripts/markbank/authoring/reviews/russian-2010-hl-font-review.json').read_text())

def open_repaired_scheme():
    paper=ROOT/'examiner-reports/russian/papers/2010-hl-000-paper.pdf'
    source=ROOT/'examiner-reports/russian/schemes/2010-hl.pdf'
    assert hashlib.sha256(paper.read_bytes()).hexdigest()=='b31909e020b82ba2a6748f8b2ff59aa6bc5b0fc2c9351e7290d54c7e2215b475'
    assert hashlib.sha256(source.read_bytes()).hexdigest()=='15607f22c24d4502dee8d28cd319711c880d27d06eac33b1da96fa6554a0672c'
    Q,S=fitz.open(paper),fitz.open(source)
    styles=['TimesNewRomanPSMT','TimesNewRomanPS-BoldMT','TimesNewRomanPS-ItalicMT']
    mapping={style:{} for style in styles}
    for page in Q:
        for span in page.get_texttrace():
            if span['font'] not in mapping:continue
            for unicode,glyph,*_ in span['chars']:
                assert unicode!=65533
                assert glyph not in mapping[span['font']] or mapping[span['font']][glyph]==unicode
                mapping[span['font']][glyph]=unicode
    for reviewed in REVIEW['fonts']:
        expected={r['glyph']:r['unicode'] for r in reviewed['glyphs']}
        assert all(mapping[reviewed['style']][glyph]==unicode for glyph,unicode in expected.items())
        assert hashlib.sha256(Q.extract_font(reviewed['paperFontXref'])[3]).hexdigest()==reviewed['paperFontSha256']
        assert hashlib.sha256(S.extract_font(reviewed['schemeFontXref'])[3]).hexdigest()==reviewed['schemeFontSha256']
    Q.close()
    # These are complete, visually checked printed spans, not inferred rules.
    spans=[s for s in S[4].get_texttrace() if s['font']=='Cambria']
    assert len(spans)==1
    transcription='where reference is made to the language of the traditional folk/oral narrative but where there is no example/illustration'
    glyphs=[g for _,g,*_ in spans[0]['chars']]
    assert len(glyphs)==len(transcription)
    mapping['Cambria']={}
    for glyph,char in zip(glyphs,transcription):
        assert glyph not in mapping['Cambria'] or mapping['Cambria'][glyph]==ord(char)
        mapping['Cambria'][glyph]=ord(char)
    mapping['Cambria-BoldItalic']={3:32}
    for glyphs,word in [([738,714,734,717,726],'языку'),([738,720,709,707,723,712],'январе')]:
        assert len(glyphs)==len(word)
        for glyph,char in zip(glyphs,word):
            assert glyph not in mapping['Cambria-BoldItalic'] or mapping['Cambria-BoldItalic'][glyph]==ord(char)
            mapping['Cambria-BoldItalic'][glyph]=ord(char)
    mapping['TimesNewRomanPS-BoldItal']={623:ord('х')}
    mapping['SymbolMT']={120:ord('•')}
    used={style:{g for p in S for span in p.get_texttrace() if span['font']==style for u,g,*_ in span['chars'] if u==65533} for style in mapping}
    assert [len(used[s]) for s in styles]==[49,31,35]
    font_names={s:s for s in mapping};font_names['TimesNewRomanPS-BoldItal']='TimesNewRomanPS-BoldItalicMT'
    for style,glyphs in used.items():
        assert glyphs<=mapping[style].keys(),(style,glyphs-mapping[style].keys())
        xrefs={f[0] for p in S for f in p.get_fonts() if f[3]==font_names[style]+'-Identity-H'}
        assert len(xrefs)==1,(style,xrefs)
        xref=xrefs.pop();assert S.xref_get_key(xref,'ToUnicode')[0]=='null'
        rows=[f'<{g:04X}> <{mapping[style][g]:04X}>' for g in sorted(glyphs)]
        cmap=('/CIDInit /ProcSet findresource begin\n12 dict begin\nbegincmap\n'
              '/CIDSystemInfo << /Registry (Adobe) /Ordering (UCS) /Supplement 0 >> def\n'
              '/CMapName /Russian2010HigherOriginalGlyphs def\n/CMapType 2 def\n'
              '1 begincodespacerange\n<0000> <FFFF>\nendcodespacerange\n'
              +f'{len(rows)} beginbfchar\n'+'\n'.join(rows)+'\nendbfchar\n'
              'endcmap\nCMapName currentdict /CMap defineresource pop\nend\nend')
        cx=S.get_new_xref();S.update_object(cx,'<<>>');S.update_stream(cx,cmap.encode('ascii'))
        S.xref_set_key(xref,'ToUnicode',f'{cx} 0 R')
    repaired=fitz.open(stream=S.tobytes(),filetype='pdf');S.close()
    assert not any(u==65533 for p in repaired for s in p.get_texttrace() for u,*_ in s['chars'])
    text=' '.join(repaired[4].get_text().split())
    assert transcription in text
    assert 'языку' in repaired[9].get_text() and 'январе' in repaired[9].get_text()
    return repaired

def scheme_page(document, number):
    """Retain full page text and omit only its verified original footer block."""
    expected=REVIEW['footerBlocks'][str(number)]
    blocks=document[number-1].get_text('blocks',sort=False)
    matches=[block for block in blocks if ' '.join(block[4].split())==expected['text']]
    assert len(matches)==1,(number,expected['text'])
    footer=matches[0]
    assert all(abs(actual-bound)<.001 for actual,bound in zip(footer[:4],expected['bbox'])),number
    return ''.join(block[4] for block in blocks if block is not footer).replace('\uf0b7','•').replace('\xa0',' ')
