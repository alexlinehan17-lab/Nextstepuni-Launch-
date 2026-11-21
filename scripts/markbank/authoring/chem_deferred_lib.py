"""Row builders the deferred Chemistry sittings share (chem_<year>_<lvl>_deferred.py).

The deferred schemes set several cells in one part (a definition priced [4 + 3], then a list [3 × 3]), menus
inside them, and cells printed at the end of the answer text, which chem_print's one-cell builders (fixed,
ordered, menu) refuse. These build the rows from the reader's own items, lifting every text, and leave the
June builders as they are.
"""
from chem_print import anyN, mark_terms, point, tidy


def pieces_of(C, items, key, notes=None):
    """Each "//"-separated point of the items' cells, in order. A cell whose terms are equal ("[3 × 3]") prices
    each point at that term; one whose terms differ ("[4 + 3]") does not say which point earns which term, so its
    points are one row claimed in steps (the first one right earns the first term), as June's two-curve card
    chem-2016-hl-q3-b is."""
    rows, notes = [], notes or {}
    for it in items:
        if it.cell is None:
            continue
        terms = mark_terms(it.cell)
        texts = [C._verbatim(t.strip(), {}, key)[0] for t in it.text.split('//') if t.strip()]
        assert len(texts) == len(terms), (key, it.cell, texts)
        asides = ' '.join(it.asides)
        if len(set(terms)) == 1:
            for text in texts:
                note = ' '.join(x for x in [f'The scheme prices these points {it.cell}.' if len(terms) > 1 else '',
                                            asides, notes.get(len(rows), '')] if x)
                rows.append(point(f'r-{len(rows) + 1}', text, terms[0], note))
        else:
            note = ' '.join(x for x in [f'These {len(terms)} points, as the scheme prices them together, {it.cell}.',
                                        asides, notes.get(len(rows), '')] if x)
            rows.append(anyN(f'r-{len(rows) + 1}', texts[0], sum(terms), len(terms), terms[0], texts, note,
                             steps=terms))
    return rows


def pieces(P, C, key, notes=None):
    """pieces_of over one part's own items."""
    return pieces_of(C, P.items(key), key, notes)


def menu_of(P, C, key, item, claim, note):
    """One printed "[any N]" menu among a part's cells: its "//"-separated options, the cell's terms as the
    steps (the first answers earn the larger marks: "[6 + 3]")."""
    it = P.items(key)[item]
    terms = mark_terms(it.cell)
    assert len(terms) == claim, (key, it.cell)
    opts = [C._verbatim(o.strip(), {}, key)[0] for o in it.text.split('//') if o.strip()]
    return anyN(f'r-{item + 1}', opts[0], sum(terms), claim, terms[0], opts,
                ' '.join(x for x in [note, ' '.join(it.asides)] if x), steps=terms if len(set(terms)) > 1 else None)


def split_words(P, C, key, tail, notation, total, topic, concept, note=''):
    """A part whose points the scheme prices together in one cell set at the end of its last answer line, which
    the reader takes as answer text: its "//"-separated points as rows, priced as the split."""
    its = P.items(key)
    assert len(its) == 1 and its[0].cell is None and its[0].text.endswith(tail), its
    words = [w.strip() for w in its[0].text[:-len(tail)].split('//')]
    return C.add([key], topic, concept, [C.lifted(f'r-{i}', w, None) for i, w in enumerate(words, 1)],
                 kind='orderedSplit', notation=notation, total=total,
                 notes=tidy(' '.join(x for x in [f'The scheme prices these points together as {notation} without '
                                                 'saying which point earns which part, so no per-point value is '
                                                 'shown.', ' '.join(its[0].asides), note] if x)))
