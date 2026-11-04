"""Reassemble words split across overlapping PDF text tiles.

The 2011 Ordinary paper repeats boundary glyphs at identical positions in
adjacent clipping tiles. Work from glyph coordinates: remove only identical
characters at the same position, retaining actual spaces and all other text.
Used only on individually reviewed pages; normal PDF extraction is unchanged.
"""


def fragmented_words(page):
    rows = []
    for block in page.get_text('rawdict')['blocks']:
        for line in block.get('lines', []):
            for span in line['spans']:
                for char in span['chars']:
                    x, baseline = char['origin']
                    glyph = (x, char['c'], char['bbox'])
                    for row in rows:
                        if abs(row[0] - baseline) < 0.5:
                            row[1].append(glyph)
                            break
                    else:
                        rows.append([baseline, [glyph]])
    words = []
    for _baseline, characters in sorted(rows):
        unique = []
        for x, char, box in sorted(characters):
            if any(abs(x - other[0]) < 0.12 and char == other[1] for other in unique[-4:]):
                continue
            unique.append((x, char, box))
        current = None
        for x, char, box in unique:
            if char.isspace():
                if current:
                    words.append(tuple(current))
                    current = None
                continue
            # A real inter-word gap is about 3 points in this printed type.
            # Adjacent fragments meet at their original character boundary.
            if current and x - current[2] > 1.5:
                words.append(tuple(current))
                current = None
            if current:
                current[1] = min(current[1], box[1])
                current[2] = max(current[2], box[2])
                current[3] = max(current[3], box[3])
                current[4] += char
            else:
                current = [*box, char]
        if current:
            words.append(tuple(current))
    return words
