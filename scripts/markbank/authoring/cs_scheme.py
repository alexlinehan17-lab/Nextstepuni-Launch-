#!/usr/bin/env python3
"""The Construction Studies marking scheme, read as its two halves.

    python3 scripts/markbank/authoring/cs_scheme.py 2025 hl        # summary
    python3 scripts/markbank/authoring/cs_scheme.py 2025 hl --dump # every part

An SEC Construction Studies scheme is two documents in one file:

  1. INDICATIVE CONTENT (pages 3-36) — for each part, the details an answer
     should contain, set as bullets under named sub-headings:

         Foundation and solid concrete ground floor - typical detailing
         - R.C. strip foundation
         - Dead blockwork and cavity wall above foundation
         ...

  2. THE MARK TABLE (pages 37+) — the same bullets again, this time under
     "PERFORMANCE CRITERIA / MAXIMUM MARK", with the tariff printed on the
     group heading rather than the bullet:

         Foundation + Solid ground floor   External wall   Window detail
         5 x 4 marks                       4 x 4 marks     3 x 4 marks

     "5 x 4 marks" against an eleven-bullet list is a best-N-of tariff: name
     any five of the eleven and each is worth 4. That is the tariff kind the
     bank already has, and it is why this subject cards well — the bullets ARE
     the answer, and which details a student omits is exactly what costs marks.

The mark table is the authority, because it is the half that prices. The
indicative half is kept because it carries sub-headings the mark table
sometimes drops, and because two independent copies of the same list is a
provenance check nothing else in this subject offers.

The two halves are separated by the mark table restarting the question
numbering. Nothing else in the file does that.
"""
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(
    os.path.abspath(__file__)))))
SCHEMES = os.path.join(ROOT, 'examiner-reports/construction-studies/schemes')

# Case varies inside one document: the 2024 Higher scheme prints "QUESTION 3"
# and "Question 4" on facing pages. Matching case-sensitively lost three of the
# ten mark tables and made the file look half-parsed.
QHEAD = re.compile(r'^(?:Leaving Certificate Examination,?\s*\d{4}\s+)?'
                   r'Question\s+(\d{1,2})\b\.?\s*(\(Alternative\))?\s*$', re.I)
# "(a)" at Higher Level, "Part (a)" at Ordinary. Without the prefix the whole
# Ordinary mark half parsed to zero parts, and the subject read as Higher-only.
PART = re.compile(r'^(?:Part\s+)?\(([a-h])\)\s*(.*)$', re.I)
BULLET = re.compile(r'^[•\-•]\s*')
# "5 x 4 marks", "4 × 4 marks (3 for drawing, 1 for annotation)"
GROUP_TARIFF = re.compile(r'(\d{1,2})\s*[x×]\s*(\d{1,3})\s*marks?', re.I)
# "(12 marks)", "(3 + 2 marks)", "(8 + 8 marks)"
PART_TARIFF = re.compile(r'\(\s*((?:\d{1,3}\s*\+\s*)*\d{1,3})\s*marks?\s*\)', re.I)
FOLD = re.compile(r'^<!--\s*markbank:')
PRACTICAL = re.compile(r'^Practical Test\b', re.I)
# A line that is only a tariff, so it is never mistaken for a group heading.
TARIFF_ONLY = re.compile(r'^[\d\s×x+•()\-]*marks?\b.*$', re.I)
# The drafting/scale band printed under every drawing question, and its numbers.
SCALE_TAIL = re.compile(r'^(Scale\s*[-–]|Drafting\s*[-–]|[\d\s]+$)', re.I)
# The presentation band every drawing question closes with. Priced, but not a
# named answer, so it is never one of a card's options.
DRAFTING = re.compile(r'\b(draughting|drafting)\b|\bexcellent, ?good, ?fair\b', re.I)
# The mark column bleeding onto the end of a bullet: "R.C. strip foundation 4".
MARK_TAIL = re.compile(r'\s+\d{1,3}\s*$')
TOTAL_ONLY = re.compile(r'^(total|sub-?total|notes?|sketches?'
                        r'|\(?\d+\s+for\s+\w+)\b', re.I)
TOTALS = re.compile(r'\b(sub-?\s*total|total)\b', re.I)
# "(8 + 5 marks)", "(3 + 3 marks)" printed inside a row's label.
MARK_EXPR = re.compile(r'\(\s*\d{1,3}(?:\s*\+\s*\d{1,3})*\s*marks?\s*\)', re.I)
# A row that names nothing: the scheme's way of saying "N interchangeable
# answers go here". "Advantage 1", "Reason 2", "Design Consideration 3".
SCAFFOLD_ROW = re.compile(
    r'^(advantage|disadvantage|reason|risk|feature|guideline|point|method|'
    r'consideration|answer|discussion point|benefit|way|factor|use|example|'
    r'design consideration|safety precaution|precaution|approach|'
    r'functional requirement|requirement|area|aspect|task|option|step|'
    r'stage|element|item)s?\s*\d*$', re.I)
# A group heading: short, title-ish, no closing punctuation, no bullet.
HEADING_LOOK = re.compile(r'^[A-Z][^.:;•]{0,58}$')
# Lines that sit where a heading sits but name nothing. The question's own text
# wraps onto a line ending in a full stop ("...requirements.", "...the house."),
# and the SEC closes most lists with a catch-all. Both became group names.
NOT_A_HEADING = re.compile(r'^(any other relevant|note\b|n\.?b\.?\b|alternative\b'
                           r'|.*[a-z]\.\s*$)', re.I)
# A heading in this scheme is always title-case. A line opening lower-case is a
# bullet that wrapped -- "available for immediate contact" became a fourth group
# of 2021 Higher Q2(c), which has three, and a group count that is wrong by one
# breaks the tariff split that depends on it dividing evenly.
LOWER_START = re.compile(r'^[a-z]')
FURNITURE = re.compile(
    r'^(##\s*Page|Leaving Certificate|Coimisi|State Examinations|-\s*\d+\s*-'
    r'|\d{1,3}\s*$|PERFORMANCE CRITERIA|MAXIMUM|MARK\s*$|TOTAL\b'
    r'|Construction Studies|Theory\s*[-–]|Marking Scheme\s*$)', re.I)


def _lines(year, level):
    """Document lines only — the appended fold blocks are a different text.

    The four append-scheme-*.py tools add re-extractions of the same pages at
    the end of the file. They are there for provenance, not structure, and
    reading them as document reported question heads that do not exist.
    """
    path = os.path.join(SCHEMES, f'{year}-{level}.md')
    out = []
    for line in open(path, errors='ignore'):
        t = line.strip()
        if FOLD.match(t):
            break
        # The Practical Test scheme is bound into the same PDF and marks a
        # coursework project, not the written paper. Left in, its pages ran on
        # under the last theory part and turned Question 10(b) into 55 groups.
        if PRACTICAL.match(t):
            break
        out.append(line.rstrip())
    return out


def split_halves(lines):
    """(indicative, marks) — the mark table restarts the question numbering."""
    ones = [i for i, l in enumerate(lines)
            if (m := QHEAD.match(l.strip())) and m.group(1) == '1']
    if len(ones) < 2:
        raise SystemExit('cannot find the mark table: expected two Question 1 heads')
    return lines[ones[0]:ones[-1]], lines[ones[-1]:]


def _rewrap(src):
    """Join a bullet to the lines it wrapped onto.

    The indicative half sets its bullets in a narrow column, so one point runs
    over two or three lines — "Use of a trench box or shuttering to strengthen
    and stabilise the / sides of the trench to prevent a collapse happening".
    Read line by line, that is two answers and neither is one the SEC printed.
    A line continues the bullet above it when it does not open a bullet and
    does not look like a heading: headings are short and unpunctuated, wrapped
    text is neither, or begins lower-case.
    """
    out = []
    for line in src:
        t = line.strip()
        if not t:
            continue
        if BULLET.match(t) or not out:
            out.append(t)
            continue
        prev = out[-1]
        continues = (t[0].islower()
                     or (BULLET.match(prev) and not prev.rstrip().endswith(('.', ':'))
                         and len(t.split()) > 2 and not HEADING_LOOK.match(t)))
        if continues and BULLET.match(prev):
            out[-1] = prev.rstrip() + ' ' + t
        else:
            out.append(t)
    return out


def blocks(lines):
    """{(question, letter): [line, ...]} for one half."""
    out, q, letter = {}, None, None
    for raw in lines:
        line = raw.strip()
        if not line:
            continue
        m = QHEAD.match(line)
        if m:
            # "Question 10 (Alternative)" is a DIFFERENT question a candidate
            # may answer instead, with its own parts and its own marks. Merged
            # into Question 10 it silently doubled that question's content.
            q = f'{m.group(1)}alt' if m.group(2) else int(m.group(1))
            letter = None
            continue
        if FURNITURE.match(line):
            continue
        p = PART.match(line)
        if p and q is not None:
            letter = p.group(1)
            rest = p.group(2).strip()
            out.setdefault((q, letter), [])
            if rest:
                out[(q, letter)].append(rest)
            continue
        if q is not None and letter is not None:
            out[(q, letter)].append(line)
    return out


class Scheme:
    def __init__(self, year, level):
        self.year, self.level = year, level
        lines = _lines(year, level)
        ind, mark = split_halves(lines)
        self.indicative = blocks(ind)
        self.marks = blocks(mark)

    def parts(self):
        # Question keys are ints except the alternative questions, which are
        # '10alt' — sort on a normalised pair so the two kinds can coexist.
        def order(k):
            q, letter = k
            return (int(str(q).replace('alt', '')), str(q).endswith('alt'), letter or '')
        return sorted(set(self.indicative) | set(self.marks), key=order)

    def bullets(self, q, letter, half='marks'):
        """Every answer item the scheme lists for this part.

        Two columns are frequently set on one line — "19 mm external render
        Cavity closer" — so a line is split on its bullet characters as well as
        broken at line ends.
        """
        src = (self.marks if half == 'marks' else self.indicative).get((q, letter), [])
        out = []
        for line in src:
            for piece in re.split(r'\s*[••]\s*', line):
                piece = BULLET.sub('', piece).strip()
                if piece:
                    out.append(piece)
        return out

    def groups(self, q, letter, half='marks'):
        """[(name, (n, per), bullets)] — the unit a card is actually made from.

        A drawing part is priced per GROUP, not per part. Question 1 of the
        2025 Higher paper prices one vertical section three ways:

            Foundation + Solid ground floor  External wall   Window detail
            5 x 4 marks                      4 x 4 marks     3 x 4 marks

        and then repeats each group name as a heading above its own bullets.
        Reading the part as one list loses that, and a card asking for "five
        details" off a 37-item list of three different things is wrong twice
        over. The tariff row and the repeated headings are paired by ORDER,
        which is what the flattened column layout preserves.

        Where the part names no groups, the whole part is one group.
        """
        src = (self.marks if half == 'marks' else self.indicative).get((q, letter), [])
        if not src:
            return []
        src = _rewrap(src)
        # Headings: a non-bullet line with at least one bullet under it.
        heads = []
        for i, line in enumerate(src):
            if (BULLET.match(line) or TARIFF_ONLY.match(line)
                    or NOT_A_HEADING.match(line.strip())
                    or LOWER_START.match(line.strip())):
                continue
            nxt = src[i + 1] if i + 1 < len(src) else ''
            if BULLET.match(nxt):
                heads.append((i, line.strip().rstrip(':').strip()))
        tariffs = [(int(a), int(b)) for a, b in GROUP_TARIFF.findall(' '.join(src))]

        def items(lo, hi):
            out = []
            for line in src[lo + 1:hi]:
                if not BULLET.match(line):
                    if SCALE_TAIL.match(line.strip()):
                        break
                    continue
                for piece in re.split(r'\s*[•●]\s*', BULLET.sub('', line)):
                    piece = MARK_TAIL.sub('', piece).strip(' .;')
                    if len(piece) > 2:
                        out.append(piece)
            return out

        if not heads:
            # One unnamed group: the bullets sit straight under the tariff line.
            first = next((i for i, l in enumerate(src) if BULLET.match(l)), None)
            if first is None:
                return []
            b = items(first - 1, len(src))
            return [(None, tariffs[0] if tariffs else None, b)] if b else []

        out = []
        for n, (i, name) in enumerate(heads):
            hi = heads[n + 1][0] if n + 1 < len(heads) else len(src)
            b = items(i, hi)
            if not b:
                continue
            t = tariffs[n] if n < len(tariffs) else (tariffs[0] if len(tariffs) == 1 else None)
            out.append((name, t, b))
        return out

    def mark_rows(self, q, letter):
        """[(label, marks)] — the mark table's priced rows for this part.

        Totals are excluded. Leaving "Sub-total 10" in was why the tariff
        inference failed on most of Ordinary Level: the rows read [5, 5, 10],
        which is not "every row carries the same mark", so a part the scheme
        prices plainly as two answers at five was reported as having no tariff
        at all. Eighty-seven parts were refused on that.
        """
        out = []
        for line in _rewrap(self.marks.get((q, letter), [])):
            t = BULLET.sub('', line).strip()
            # A total or a tariff is not an answer row wherever it sits on the
            # line. "Any 7 x 5 marks Sub-total 35" closes every Ordinary Level
            # vertical section; counted as a row its 35 broke the "every row
            # carries the same mark" test and lost the richest question in the
            # paper, five times over.
            if not t or SCALE_TAIL.match(t) or TOTALS.search(t) or GROUP_TARIFF.search(t):
                continue
            m = re.search(r'^(.*?)\s+(\d{1,3})\s*$', t)
            if not m:
                continue
            label = MARK_EXPR.sub('', m.group(1)).strip(' .;:')
            if label:
                out.append((label, int(m.group(2))))
        return out

    def mark_items(self, q, letter, question=None):
        """The mark table's own answer rows, where IT is the fuller list.

        For most parts the indicative half carries the content and the mark
        table only prices it. For the services and wiring layouts it is the
        other way round: the 2021 Higher Q9(b) mark table names the six things
        a ring main drawing must show, and the indicative half lists something
        else entirely under "Ring main circuit - typical detailing".
        """
        out = []
        for line in _rewrap(self.marks.get((q, letter), [])):
            t = BULLET.sub('', line).strip()
            if (not t or TARIFF_ONLY.match(t) or SCALE_TAIL.match(t)
                    or TOTALS.search(t) or GROUP_TARIFF.search(t) or DRAFTING.search(t)):
                continue
            t = MARK_TAIL.sub('', t).strip(' .;')
            if len(t) > 2 and not TOTAL_ONLY.match(t):
                out.append(t)
        # The block usually opens by restating the question, and that line is
        # not an answer. But not always: the Ordinary vertical sections open
        # straight into "Slates 600 mm x 300 mm on battens", and dropping it
        # unconditionally lost a real detail off every one of them. Dropped only
        # when it actually reads as the question.
        if out and question:
            a, b = PCS(out[0]), PCS(question)
            if a and b and (a[:30] in b or b[:30] in a):
                return out[1:]
        return out

    def tariff(self, q, letter):
        """(kind, n, per) from the mark table, or None if it prints none."""
        text = ' '.join(self.marks.get((q, letter), []))
        g = GROUP_TARIFF.search(text)
        if g:
            return ('bestNofParts', int(g.group(1)), int(g.group(2)))
        p = PART_TARIFF.search(text)
        if p:
            vals = [int(v) for v in re.split(r'\s*\+\s*', p.group(1))]
            return ('fixed', len(vals), vals[0]) if len(vals) > 1 else ('total', 1, vals[0])
        return None


if __name__ == '__main__':
    year, level = int(sys.argv[1]), sys.argv[2]
    S = Scheme(year, level)
    dump = '--dump' in sys.argv
    half = 'indicative' if '--indicative' in sys.argv else 'marks'
    print(f'{year} {level.upper()}  indicative parts {len(S.indicative)}   '
          f'mark-table parts {len(S.marks)}')
    for key in S.parts():
        q, letter = key
        gs = S.groups(q, letter, half)
        print(f'  Q{q}({letter})  {len(gs)} group(s)')
        for name, t, b in gs:
            print(f'      [{name or "-"}]  tariff={t}  items={len(b)}')
            if dump:
                for x in b[:6]:
                    print(f'          * {x[:100]}')


# A numbered answer slot, with or without a trailing mark and with or without
# the rest of the sentence: "Functional Requirement 2", "Method 1 to reduce
# solar overheating", "Guideline 3". Read off the RAW block, because a slot is
# frequently priced on the lines beneath it rather than on its own line and so
# never reaches mark_rows() at all.
SLOT_LINE = re.compile(
    r'^(advantage|disadvantage|reason|risk|feature|guideline|point|method|'
    r'consideration|answer|discussion point|benefit|way|factor|use|example|'
    r'design consideration|safety precaution|safety procedure|precaution|'
    r'approach|functional requirement|requirement|item|element|area|aspect|'
    r'section|task|option|type|material|detail|step|stage|part)s?\s+(\d{1,2})\b',
    re.I)


def slot_labels(lines):
    """The numbered answer slots a part's mark block sets out, by name.

    "Functional Requirement 1/2/3" is the scheme saying three answers of the
    same kind go here. Where they all share a name and the part prints a total,
    the count and the total are both printed and the per-answer mark is
    arithmetic on them rather than a guess.
    """
    out = []
    for line in lines:
        m = SLOT_LINE.match(line.strip())
        if m:
            out.append(m.group(1).lower())
    return out


def PCS(t):
    """Squashed to letters and digits, for comparing two printings of one line."""
    return re.sub(r'[^a-z0-9]+', '', (t or '').lower())
