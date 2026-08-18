"""Shared helpers for authoring Home Economics Mark Bank cards.

Option text is always SLICED from the scheme markdown, never retyped: the build's
provenance gate requires every marking point to appear in its own scheme, and both
historical scheme corruptions in this repo entered through hand transcription.
"""
import json, re

MAX_OPTIONS = 14          # optionCapFor('B') in scripts/markbank/optionCap.mjs
VALID_KINDS = {'point', 'alt', 'allOf', 'anyN', 'criterion', 'gate'}


# A segment that is not a marking point. The provenance gate cannot catch these
# -- they ARE in the scheme -- but a running page footer or a note to the
# examiner rendered as a student-facing option is worse than a missing option.
JUNK = re.compile(
    r'^(?:[\u2022\-\u2013\u2014\s]*$'                   # bullets / dashes only
    r'|Accept\b'                                       # note to the examiner
    r'|.*(?:Leaving Certificate|Home Economics \u2013|Coimisi\u00fan|Marcanna Breise))',
    re.IGNORECASE)


def load(year, level):
    """Scheme text with page markers and bare-number lines removed, as the
    build's comparableScheme() does, so slices line up with what it searches."""
    lvl = 'hl' if level == 'higher' else 'ol'
    raw = open(f'examiner-reports/home-economics/schemes/{year}-{lvl}.md').read()
    keep = [l for l in raw.split('\n')
            if not re.match(r'^##\s*Page\s*\d+\s*$', l) and not re.match(r'^\s*\d+\s*$', l)]
    return '\n'.join(keep)


def tidy(s):
    return ' '.join(s.split())


def block(text, start, end=None, occ=None):
    """Slice from `start` to `end`.

    Refuses an ambiguous start anchor. A heading almost always appears twice --
    once in the question's own bullet list, once over the marking points -- and
    taking the first match silently returns the question text plus everything
    after it. Pass occ= to choose deliberately.
    """
    hits = [m.start() for m in re.finditer(re.escape(start), text)]
    if not hits:
        raise ValueError(f'anchor not found: {start!r}')
    if len(hits) > 1 and occ is None:
        raise ValueError(
            f'ambiguous anchor {start!r}: {len(hits)} matches at {hits}. '
            f'Lengthen it, or pass occ=')
    a = hits[occ or 0]
    return text[a:text.index(end, a)] if end else text[a:]


def semis(chunk, drop_prefix=None):
    """Semicolon-separated marking points, in scheme order, 'etc.' removed."""
    t = tidy(chunk)
    if drop_prefix and t.startswith(drop_prefix):
        t = t[len(drop_prefix):]
    out = []
    for x in t.split(';'):
        # "etc." also appears mid-list, where the examiner closes one cluster and
        # opens another without a new heading: "...career breaks; etc. high
        # standard of living; ...". Strip it from either end, not just the tail.
        x = tidy(re.sub(r'^\s*etc\.?\s+', '', re.sub(r'\s*etc\.?\s*$', '', tidy(x))))
        if not x or x.lower() in ('etc', 'etc.') or JUNK.match(x):
            continue
        out.append(x)
    return out


def heads(chunk, hs):
    """Split a chunk at named headings, keeping each heading with its text.

    The chunk is tidied first: the PDF extraction wraps lines mid-heading
    ("Same sex\nmarriage:"), so indexing the raw text misses headings that are
    plainly there once the line breaks are collapsed.
    """
    chunk = tidy(chunk)
    idx = [(h, chunk.index(h)) for h in hs]
    # A short heading can match inside an earlier word -- "age" inside "mortgage"
    # -- which silently empties one block and fills the next with the wrong text.
    # The headings are given in scheme order, so their positions must increase.
    for (h, a), (h2, b) in zip(idx, idx[1:]):
        if b <= a:
            raise ValueError(
                f"heading {h2!r} found at {b}, at or before {h!r} at {a} -- "
                f"{h2!r} is matching inside earlier text; use a longer anchor")
    return [tidy(chunk[p:(idx[i + 1][1] if i + 1 < len(idx) else len(chunk))])
            for i, (h, p) in enumerate(idx)]


def anyN(rid, verbatim, marks, claim, per, options, note):
    return {"id": rid, "kind": "anyN", "verbatim": verbatim, "marks": marks,
            "openList": True, "contextNote": note,
            "group": {"claimMax": claim, "perOption": per, "options": options}}


def point(rid, verbatim, marks, note, accepts=None):
    r = {"id": rid, "kind": "point", "verbatim": verbatim, "marks": marks,
         "openList": True, "contextNote": note}
    if accepts:
        r["accepts"] = accepts
    return r


def card(cid, year, level, topic, concept, ref, qtext, notation, total, rows, notes,
         stem="", tariff_kind="bestNofParts", answer=None, of_parts=None, per_part=None,
         section="B"):
    # A best-of tariff must state answer x perPart, and the build checks it makes
    # the total. Derive from the row when the caller has not said otherwise, so a
    # forgotten argument cannot ship a card whose tariff reads "null x null".
    if tariff_kind == 'bestNofParts' and answer is None:
        g = next((r['group'] for r in rows if r.get('group')), None)
        if g:
            answer, per_part, of_parts = g['claimMax'], g['perOption'], len(g['options'])
    return {"id": cid, "topicId": topic, "conceptId": concept, "level": level, "year": year,
            "subjectId": "home-economics", "section": section, "questionRef": ref,
            "questionText": qtext, "stem": stem, "figureKey": "", "labelKey": [],
            "tariffModel": {"kind": tariff_kind, "notation": notation, "answer": answer,
                            "ofParts": of_parts, "perPart": per_part},
            "totalMarks": total, "rows": rows, "notes": notes}


def audit(cards):
    """Catch what the build would drop, before writing anything."""
    problems = []
    for c in cards:
        rowsum = sum(r['marks'] for r in c['rows'])
        if rowsum != c['totalMarks']:
            problems.append(f"{c['id']}: rows sum to {rowsum}, tariff is {c['totalMarks']}")
        tm = c['tariffModel']
        if tm['kind'] == 'bestNofParts':
            a, pp = tm.get('answer'), tm.get('perPart')
            if not a or not pp:
                problems.append(f"{c['id']}: best-of tariff is missing answer/perPart")
            elif a * pp != c['totalMarks']:
                problems.append(f"{c['id']}: best-of tariff {a}x{pp} does not make {c['totalMarks']}")
        for r in c['rows']:
            if r['kind'] not in VALID_KINDS:
                problems.append(f"{c['id']} {r['id']}: invalid kind {r['kind']}")
            g = r.get('group')
            if not g:
                continue
            if len(g['options']) < g['claimMax']:
                problems.append(f"{c['id']} {r['id']}: claims {g['claimMax']} from {len(g['options'])} option(s)")
            if len(g['options']) > MAX_OPTIONS:
                problems.append(f"{c['id']} {r['id']}: {len(g['options'])} options, cap is {MAX_OPTIONS}")
            if g['claimMax'] * g['perOption'] > c['totalMarks']:
                problems.append(f"{c['id']} {r['id']}: {g['claimMax']}x{g['perOption']} on a {c['totalMarks']}-mark question")
    return problems


def emit(cards, held=None):
    """Print the cards as JSON, with an audit report on stderr."""
    import sys
    for p in audit(cards):
        print('AUDIT', p, file=sys.stderr)
    print(json.dumps(cards, ensure_ascii=False, indent=1))
