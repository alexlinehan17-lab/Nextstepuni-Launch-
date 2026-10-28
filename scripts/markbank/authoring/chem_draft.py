#!/usr/bin/env python3
"""Draft a sitting's Chemistry generator: one call per scheme mark cell, for review.

    python3 scripts/markbank/authoring/chem_draft.py 2024 hl > /tmp/draft.py

Writes nothing into the repo. It prints a first draft of chem_audit_<year>_<lvl>.py
(a sitting with pre-audit cards) or chem_<year>_<lvl>.py (one without), which a
person then reads card by card, corrects and commits. Nothing in the draft is
exam content: every call names a PART, and the generator lifts the words from
the paper and the scheme when it runs.

What the draft decides, and how:

  * Card boundaries follow the scheme's mark cells. Walking the paper's parts
    in order, a part whose scheme answer has no cell of its own joins the next
    part of the same letter (and alternative) whose answer closes with one:
    that cell prices them together, so they are one task (C.ordered). A part
    closed by a single-valued cell is C.fixed; by a split cell ("[4 + 2]") is
    C.ordered; by an "[any N]" menu whose cell prices N answers is C.menu.
  * A part whose scheme answer is a cell with no words is marked DRAWN: the
    scheme answers it with a picture, which needs a solution crop.
  * Pre-audit ids (read from the audit's base commit) are mapped by citation:
    a pre-audit card whose first part opens a draft card keeps its id there;
    one that opened inside a draft card is WITHDRAWN to the card that holds its
    part; a later part of a pre-audit card that joined several cells gets a
    new id. Where two pre-audit cards open on the same part, the one the base
    build shipped keeps the id and the other is withdrawn as a duplicate.
  * A kept id inherits its topic and concept (None, None) unless the draft card
    holds a different set of parts, when the concept is marked TODO with the
    old one beside it. A new card takes the topic of the pre-audit card that
    covered its part, else TODO; its concept is a slug of its ask, to review.

Every TODO is a judgement the draft could not make. The review output of the
finished generator (letter totals against the paper's printed marks, the
PAPER≠REPRINT list) is what says the judgements were right.
"""
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import chem_print as cp  # noqa: E402

ROMANS = cp.ROMAN_ORDER
STOP = {'the', 'a', 'an', 'of', 'in', 'to', 'and', 'or', 'for', 'is', 'are', 'was', 'were', 'that',
        'this', 'which', 'what', 'how', 'why', 'state', 'name', 'give', 'identify', 'explain',
        'describe', 'write', 'calculate', 'define', 'by', 'with', 'on', 'be', 'your', 'from', 'at',
        'as', 'it', 'its', 'one', 'two', 'three', 'used', 'answer', 'answerbook', 'following',
        'shown', 'would', 'could', 'should', 'you', 'there', 'these', 'those', 'has', 'have'}


def slug(text, n=6):
    words = [w for w in re.findall(r'[a-z0-9]+', cp.norm_words(text) if hasattr(cp, 'norm_words')
                                    else text.lower()) if w not in STOP and len(w) > 1]
    return '-'.join(words[:n]) or 'part'


def leaves(segs):
    keys = [s.key for s in segs]
    out = []
    for i, k in enumerate(keys):
        below = [j for j in keys if j != k and j[0] == k[0]
                 and (k[1] is None or j[1] == k[1]) and (k[2] is None or j[2] == k[2])
                 and (k[3] is None or j[3] == k[3])]
        if not below and k not in out:
            out.append(k)
    return out


REF = re.compile(r'^(\d{4}) (HL|OL) Q(\d{1,2})(.*)$')


def ref_keys(ref, paper_leaves):
    """The paper leaves a pre-audit citation names, in paper order."""
    m = REF.match(ref.split(' — ')[0].strip())
    if not m:
        return []
    q, rest = m.group(3), m.group(4)
    rest = rest.replace('–', '-').replace(' part ', '').replace(' ', '')
    lm = re.match(r'^\(([a-l])\)([AB])?(.*)$', rest)
    if not lm:
        return [k for k in paper_leaves if k[0] == q] if not rest else []
    letter, alt, tail = lm.group(1), lm.group(2), lm.group(3)
    rs = re.findall(r'\(([ivx]+)\)', tail)
    pool = [k for k in paper_leaves if k[0] == q and k[1] == letter and (alt is None or k[3] == alt)]
    if not rs:
        return pool
    if '-' in tail and len(rs) == 2:
        lo, hi = ROMANS.index(rs[0]), ROMANS.index(rs[1])
        want = set(ROMANS[lo:hi + 1])
    else:
        want = set(rs)
    return [k for k in pool if k[2] in want]


def deep_in_scheme(P, k):
    """True where the scheme files a paper leaf's answers under markers of its
    own below it ("(i) 2 (ii) 1" under Q4(a))."""
    return any(s.key != k and s.key[:2] == k[:2] and s.key[3] == k[3] and k[2] is None
               for s in P.sseg)


def classify(P, keys):
    """('fixed'|'ordered'|'menu'|'drawn'|'none', note)."""
    items = []
    for k in keys:
        try:
            items += P.items(k, deep=deep_in_scheme(P, k))
        except KeyError:
            return 'none', f'no scheme part for {k}'
    cells = [it.cell for it in items if it.cell]
    if not cells:
        return 'none', 'no mark cell'
    if len(keys) > 1:
        return 'ordered', ''
    its = [it for it in items if it.cell]
    if len(its) == 1 and not its[0].text.strip():
        return 'drawn', 'the cell prices no words: a drawing?'
    if any(cp.ANY.match(a) for it in items for a in it.asides):
        it = next(it for it in items if any(cp.ANY.match(a) for a in it.asides))
        claim = cp.WORDS[next(cp.ANY.match(a) for a in it.asides if cp.ANY.match(a)).group(1).lower()]
        if it.cell and len(cp.mark_terms(it.cell)) == claim and len(items) == 1:
            return 'menu', ''
        return 'ordered', 'an [any N] menu inside a split'
    if any('+' in c and '×' not in c.split('+')[0] for c in cells) or any('+' in c for c in cells):
        return 'ordered', ''
    return 'fixed', ''


def draft(year, lvl):
    P = cp.Printed(year, lvl, figures=True)
    C = cp.Cards(P)
    pl = leaves(P.pseg)
    prefix = f'chem-{year}-{lvl}-'
    prior = {i: c for i, c in cp.prior_deck().items() if i.startswith(prefix)}
    import chem_apply_print
    shipped = chem_apply_print.base_built_ids()

    # Group the paper's leaves by the scheme's cells.
    groups, pending = [], []
    for k in pl:
        if k[1] is None and k[0] != '4':
            # A question with no letters: one card for the whole.
            groups.append([k])
            continue
        pending.append(k)
        try:
            its = P.items(k, deep=deep_in_scheme(P, k))
        except KeyError:
            its = []
        if any(it.cell for it in its):
            groups.append(pending)
            pending = []
            continue
        nxt = pl[pl.index(k) + 1] if pl.index(k) + 1 < len(pl) else None
        if not nxt or nxt[:2] != k[:2] or nxt[3] != k[3]:
            groups.append(pending)        # the letter ends with no cell: flag it
            pending = []
    if pending:
        groups.append(pending)

    # Map pre-audit ids.
    prior_keys = {i: ref_keys(c['questionRef'], pl) for i, c in prior.items()}
    opens = {}
    for i, ks in prior_keys.items():
        if ks:
            opens.setdefault(ks[0], []).append(i)
    unmapped = [i for i, ks in prior_keys.items() if not ks]
    withdrawn, used = {}, set()
    plan = []
    for g in groups:
        first = g[0]
        cands = opens.get(first, [])
        keep = None
        if cands:
            # The shipped one keeps the id; a figure breaks a tie.
            cands = sorted(cands, key=lambda i: (i not in shipped, not prior[i].get('figureKey'), i))
            keep = cands[0]
            for dup in cands[1:]:
                withdrawn[dup] = (keep, 'duplicate')
        inner = [i for k in g[1:] for i in opens.get(k, [])]
        plan.append((g, keep, inner))
        for i in inner:
            withdrawn.setdefault(i, (None, 'joined'))
    # Point a joined withdrawal at the id that holds its part.
    for g, keep, inner in plan:
        for i in inner:
            withdrawn[i] = (keep or ('<new ' + C.cid(g) + '>'), 'joined')

    out = []
    w = out.append
    w(f'# ── DRAFT {year} {lvl.upper()} ── {len(pl)} paper leaves, {len(groups)} draft cards')
    for i in unmapped:
        w(f'# UNMAPPED pre-audit {i}: {prior[i]["questionRef"]!r}')
    last_q = None
    for g, keep, inner in plan:
        q = g[0][0]
        if q != last_q:
            w(f'\n# ── Q{q} ' + '─' * 60)
            last_q = q
        kind, note = classify(P, g)
        keys = ', '.join(_k(k) for k in g)
        cid = ''
        topic = concept = None
        if keep:
            short = keep[len(prefix):]
            if short != C.cid(g):
                cid = f", cid='{short}'"
            if prior_keys[keep] != g:
                concept = f"TODO concept (was {prior[keep]['conceptId']})"
                topic = prior[keep]['topicId']
        else:
            cover = [i for i, ks in prior_keys.items() if set(ks) & set(g)]
            topic = prior[cover[0]]['topicId'] if cover else 'TODO'
            try:
                concept = slug(P.ask(g[0]))
            except Exception:        # noqa: BLE001
                concept = 'TODO'
        fig = ''
        if keep and prior[keep].get('figureKey'):
            fig = f", figure='{prior[keep]['figureKey']}'"
        tc = 'None, None' if topic is None else f"'{topic}', '{concept}'"
        comment = f'  # {note}' if note else ''
        if len(g) == 1 and deep_in_scheme(P, g[0]):
            cid += ', deep=True'
        if kind == 'drawn':
            w(f"C.drawn([{keys}], {tc}, S + 'TODO'{cid}){comment}")
        elif kind == 'menu':
            w(f'C.menu([{keys}], {tc}{cid}{fig}){comment}')
        elif kind == 'ordered':
            w(f'C.ordered([{keys}], {tc}{cid}{fig}){comment}')
        elif kind == 'fixed':
            w(f'C.fixed([{keys}], {tc}{cid}{fig}){comment}')
        else:
            w(f'# TODO {keys}: {note}  (keep={keep})')
    w('\nWITHDRAWN = {')
    for old, (new, why) in sorted(withdrawn.items()):
        w(f"    '{old}': ('{new}', '{why}: {prior[old]['questionRef']}'),")
    w('}')
    return '\n'.join(out)


def _k(k):
    q, letter, roman, alt = k
    if alt:
        return f"ka('{q}', {_q(letter)}, {_q(roman)}, '{alt}')"
    parts = [f"'{q}'"] + ([f"'{letter}'"] if letter or roman else []) + ([f"'{roman}'"] if roman else [])
    if roman and not letter:
        parts = [f"'{q}'", 'None', f"'{roman}'"]
    return 'k(' + ', '.join(parts) + ')'


def _q(x):
    return f"'{x}'" if x else 'None'


if __name__ == '__main__':
    print(draft(int(sys.argv[1]), sys.argv[2]))
