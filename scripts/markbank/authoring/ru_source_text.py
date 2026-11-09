"""Original Russian PDF text with a narrowly bound, glyph-derived font repair.

The 2010 and 2014 Ordinary schemes omit ToUnicode for Identity-H fonts.
Their glyph IDs match the correctly encoded fonts in the same sitting's paper.
Build each mapping from those original glyphs, never guesses.
Only the in-memory document is repaired; neither original PDF is rewritten.
"""
import hashlib
from pathlib import Path
import fitz

ROOT = Path(__file__).resolve().parents[3]
SCHEME_HASH = 'b3186b37ad28e970e617c4c9fc3710628400da21c59a2dd18e51f444799e2d3c'
PAPER_HASH = 'fa8c43f85b8c65aa24a0989c22213a548c729106057965052908d8a887107eef'


def repair_2010(document, path):
    assert hashlib.sha256(path.read_bytes()).hexdigest() == 'a9fa632484624a15aab956313b463260948d60ae1deaeb4f6344ef4dff2da67e'
    paper_path = ROOT / 'examiner-reports/russian/papers/2010-ol-000-paper.pdf'
    assert hashlib.sha256(paper_path.read_bytes()).hexdigest() == '8a4c29e76ab591c9d406b8cb3fcd57f57cbf7f4b178e32ea6c26614f1ac5502d'
    styles = ['TimesNewRomanPSMT', 'TimesNewRomanPS-BoldMT', 'TimesNewRomanPS-ItalicMT']
    mappings = {style: {} for style in styles}
    with fitz.open(paper_path) as paper:
        for page in paper:
            for span in page.get_texttrace():
                if span['font'] not in mappings:
                    continue
                mapping = mappings[span['font']]
                for unicode, glyph, *_ in span['chars']:
                    assert unicode != 65533
                    assert glyph not in mapping or mapping[glyph] == unicode
                    mapping[glyph] = unicode
    used = {style: {glyph for page in document for span in page.get_texttrace()
                   if span['font'] == style for unicode, glyph, *_ in span['chars']
                   if unicode == 65533} for style in styles}
    assert [len(used[style]) for style in styles] == [52, 36, 14]
    for style in styles:
        assert used[style] <= mappings[style].keys(), (style, used[style] - mappings[style].keys())
        fonts = {font[0] for page in document for font in page.get_fonts()
                 if font[3] == style + '-Identity-H'}
        assert len(fonts) == 1
        xref = next(iter(fonts))
        assert document.xref_get_key(xref, 'ToUnicode')[0] == 'null'
        rows = [f'<{glyph:04X}> <{mappings[style][glyph]:04X}>' for glyph in sorted(used[style])]
        cmap = ('/CIDInit /ProcSet findresource begin\n12 dict begin\nbegincmap\n'
                '/CIDSystemInfo << /Registry (Adobe) /Ordering (UCS) /Supplement 0 >> def\n'
                '/CMapName /Russian2010OriginalGlyphs def\n/CMapType 2 def\n'
                '1 begincodespacerange\n<0000> <FFFF>\nendcodespacerange\n'
                + f'{len(rows)} beginbfchar\n' + '\n'.join(rows) + '\nendbfchar\n'
                'endcmap\nCMapName currentdict /CMap defineresource pop\nend\nend')
        cmap_xref = document.get_new_xref()
        document.update_object(cmap_xref, '<<>>')
        document.update_stream(cmap_xref, cmap.encode('ascii'))
        document.xref_set_key(xref, 'ToUnicode', f'{cmap_xref} 0 R')
    repaired = fitz.open(stream=document.tobytes(), filetype='pdf')
    document.close()
    return repaired


def open_scheme(year, level):
    path = ROOT / f'examiner-reports/russian/schemes/{year}-{level}.pdf'
    document = fitz.open(path)
    if (year, level) == (2010, 'ol'):
        return repair_2010(document, path)
    if (year, level) != (2014, 'ol'):
        return document
    assert hashlib.sha256(path.read_bytes()).hexdigest() == SCHEME_HASH
    paper_path = ROOT / 'examiner-reports/russian/papers/2014-ol-000-paper.pdf'
    assert hashlib.sha256(paper_path.read_bytes()).hexdigest() == PAPER_HASH
    mapping = {}
    with fitz.open(paper_path) as paper:
        for page in paper:
            for span in page.get_texttrace():
                if span['font'] != 'TimesNewRomanPSMT':
                    continue
                for unicode, glyph, *_ in span['chars']:
                    assert unicode != 65533
                    assert glyph not in mapping or mapping[glyph] == unicode
                    mapping[glyph] = unicode
    used = {glyph for page in document for span in page.get_texttrace()
            if span['font'] == 'TimesNewRoman' for _, glyph, *_ in span['chars']}
    assert used <= mapping.keys(), sorted(used - mapping.keys())
    fonts = {font[0] for page in document for font in page.get_fonts()
             if font[3] == 'TimesNewRoman-Identity-H'}
    assert len(fonts) == 1
    xref = next(iter(fonts))
    assert document.xref_get_key(xref, 'ToUnicode')[0] == 'null'
    rows = [f'<{glyph:04X}> <{mapping[glyph]:04X}>' for glyph in sorted(used)]
    chunks = [f'{len(rows[i:i+100])} beginbfchar\n' + '\n'.join(rows[i:i+100]) + '\nendbfchar'
              for i in range(0, len(rows), 100)]
    cmap = ('/CIDInit /ProcSet findresource begin\n12 dict begin\nbegincmap\n'
            '/CIDSystemInfo << /Registry (Adobe) /Ordering (UCS) /Supplement 0 >> def\n'
            '/CMapName /Russian2014OriginalGlyphs def\n/CMapType 2 def\n'
            '1 begincodespacerange\n<0000> <FFFF>\nendcodespacerange\n'
            + '\n'.join(chunks) + '\nendcmap\nCMapName currentdict /CMap defineresource pop\nend\nend')
    cmap_xref = document.get_new_xref()
    document.update_object(cmap_xref, '<<>>')
    document.update_stream(cmap_xref, cmap.encode('ascii'))
    document.xref_set_key(xref, 'ToUnicode', f'{cmap_xref} 0 R')
    # Reopen the in-memory bytes to invalidate MuPDF's cached font/text objects.
    repaired = fitz.open(stream=document.tobytes(), filetype='pdf')
    document.close()
    return repaired
