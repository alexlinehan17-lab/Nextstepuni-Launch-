"""Shared authoring helpers, for any Mark Bank subject.

These began as he_lib.py and every guard in them is here because it caught a real
bug while Home Economics was being authored. Lifting them out rather than copying
them into a second subject's library is the same call this repo has already made
for schemeText.mjs and contentFree.mjs: two copies of a rule drift, and the drift
is invisible until a card ships wrong.

`he_lib` and `econ_lib` bind these to their own subject id, scheme directory and
page furniture. Nothing subject-specific belongs in this file.

Option text is always SLICED from the scheme markdown, never retyped: the build's
provenance gate requires every marking point to appear in its own scheme, and both
historical scheme corruptions in this repo entered through hand transcription.
"""
import json
import re

VALID_KINDS = {'point', 'alt', 'allOf', 'anyN', 'criterion', 'gate'}


def tidy(s):
    return ' '.join(s.split())


def make_load(subject_id):
    """A loader for one subject's scheme markdown.

    Page markers and bare-number lines are dropped exactly as the build's
    comparableScheme() drops them, so a slice taken here lines up with what the
    provenance gate searches.
    """
    def load(year, level):
        lvl = 'hl' if level == 'higher' else 'ol'
        raw = open(f'examiner-reports/{subject_id}/schemes/{year}-{lvl}.md').read()
        keep = [l for l in raw.split('\n')
                if not re.match(r'^##\s*Page\s*\d+\s*$', l) and not re.match(r'^\s*\d+\s*$', l)]
        return '\n'.join(keep)
    return load


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


def make_semis(junk):
    """A splitter on semicolons, skipping this subject's page furniture."""
    def semis(chunk, drop_prefix=None):
        """Semicolon-separated marking points, in scheme order, 'etc.' removed."""
        t = tidy(chunk)
        if drop_prefix and t.startswith(drop_prefix):
            t = t[len(drop_prefix):]
        out = []
        for x in t.split(';'):
            # "etc." also appears mid-list, where the examiner closes one cluster
            # and opens another without a new heading: "...career breaks; etc.
            # high standard of living; ...". Strip it from either end.
            x = tidy(re.sub(r'^\s*etc\.?\s+', '', re.sub(r'\s*etc\.?\s*$', '', tidy(x))))
            if not x or x.lower() in ('etc', 'etc.') or junk.match(x):
                continue
            out.append(x)
        return out
    return semis


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


def anyN(rid, verbatim, marks, claim, per, options, note, steps=None):
    """A bounded menu.

    `steps` is for a scheme that does not pay the same for every option claimed
    -- Economics prices "two economic consequences" at 6 then 4 -- and must have
    exactly `claim` entries. `per` stays the first step, so anything reading only
    `perOption` is never wrong by more than the tail.
    """
    group = {"claimMax": claim, "perOption": per, "options": options}
    if steps:
        if len(steps) != claim:
            raise ValueError(f'{rid}: {len(steps)} mark steps for {claim} claimable options')
        group["perOptionSteps"] = steps
    return {"id": rid, "kind": "anyN", "verbatim": verbatim, "marks": marks,
            "openList": True, "contextNote": note, "group": group}


def point(rid, verbatim, marks, note, accepts=None):
    r = {"id": rid, "kind": "point", "verbatim": verbatim, "marks": marks,
         "openList": True, "contextNote": note}
    if accepts:
        r["accepts"] = accepts
    return r


def make_card(subject_id, default_section='B'):
    """A card constructor bound to one subject."""
    def card(cid, year, level, topic, concept, ref, qtext, notation, total, rows, notes,
             stem="", tariff_kind="bestNofParts", answer=None, of_parts=None, per_part=None,
             section=default_section, figure_key="", label_key=None):
        # A best-of tariff must state answer x perPart, and the build checks it
        # makes the total. Derive from the row when the caller has not said
        # otherwise, so a forgotten argument cannot ship a card whose tariff
        # reads "null x null".
        if tariff_kind == 'bestNofParts':
            g = next((r['group'] for r in rows if r.get('group')), None)
            # A descending tariff cannot be a best-of: "answer x perPart" is one
            # value per option by definition, and 2 x 6 is not the 10 that 6-then-4
            # pays. Caught here rather than at the build, where it reads as an
            # arithmetic error with no hint of the cause.
            if g and g.get('perOptionSteps'):
                raise ValueError(
                    f"{cid}: a descending tariff ({'+'.join(map(str, g['perOptionSteps']))}) "
                    f"is not a best-of — pass tariff_kind='fixed'")
            if answer is None and g:
                answer, per_part, of_parts = g['claimMax'], g['perOption'], len(g['options'])
        return {"id": cid, "topicId": topic, "conceptId": concept, "level": level, "year": year,
                "subjectId": subject_id, "section": section, "questionRef": ref,
                "questionText": qtext, "stem": stem,
                # A figure is named by KEY only. The build resolves the key against
                # the manifest bind-figures.mjs wrote, checks the file is still on
                # disk and that its bytes still hash to what the inspecting agent
                # saw, and refuses otherwise -- both historical figure corruptions
                # in this repo came in through a hand-transcribed path.
                "figureKey": figure_key, "labelKey": label_key or [],
                "tariffModel": {"kind": tariff_kind, "notation": notation, "answer": answer,
                                "ofParts": of_parts, "perPart": per_part},
                "totalMarks": total, "rows": rows, "notes": notes}
    return card


# An option this long is a slice that ran past the end of its question and took
# the next one with it. The provenance gate cannot object -- the text really is
# in the scheme, contiguously -- so it shipped: one Economics option reached
# 9,047 characters and ended in the examiner instructions of a later question.
# The longest legitimate marking point across every subject here is ~620.
MAX_OPTION_CHARS = 700


def make_audit(max_options, max_option_chars=MAX_OPTION_CHARS):
    """An auditor for one subject's option cap."""
    def audit(cards):
        """Catch what the build would drop, before writing anything."""
        problems = []
        for c in cards:
            rowsum = sum(
                (sum(r['group']['perOptionSteps'][:r['group']['claimMax']])
                 if r.get('group', {}).get('perOptionSteps') else r['marks'])
                for r in c['rows'])
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
                if len(g['options']) > max_options:
                    problems.append(f"{c['id']} {r['id']}: {len(g['options'])} options, cap is {max_options}")
                worth = (sum(g['perOptionSteps'][:g['claimMax']]) if g.get('perOptionSteps')
                         else g['claimMax'] * g['perOption'])
                if worth > c['totalMarks']:
                    problems.append(f"{c['id']} {r['id']}: group is worth {worth} on a {c['totalMarks']}-mark question")
                for i, o in enumerate(g['options']):
                    if len(o) > max_option_chars:
                        problems.append(
                            f"{c['id']} {r['id']}: option {i} is {len(o)} chars -- the slice ran "
                            f"past its question. Bound it with an end anchor.")
        return problems
    return audit


def make_emit(audit):
    def emit(cards, held=None):
        """Print the cards as JSON, with an audit report on stderr."""
        import sys
        for p in audit(cards):
            print('AUDIT', p, file=sys.stderr)
        print(json.dumps(cards, ensure_ascii=False, indent=1))
    return emit
