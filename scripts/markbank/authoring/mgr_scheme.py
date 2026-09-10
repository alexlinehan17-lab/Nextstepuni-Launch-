#!/usr/bin/env python3
"""Modern Greek marking schemes — the answer, cut off the reprinted question.

    python3 scripts/markbank/authoring/mgr_scheme.py 2024 hl
    python3 scripts/markbank/authoring/mgr_scheme.py --survey

A Modern Greek scheme is the paper again, with the answer set under each
question in the same Greek::

    2. Ποιες γνωστικές προκαταλήψεις … την κλιματική αλλαγή;
       Υπάρχουν διάφορα στοιχεία που οδηγούν τους ανθρώπους στο να
       επιστρατεύσουν ασυνείδητα γνωστικές προκαταλήψεις …

So the two documents are paired without scoring any wording: the scheme is
walked by `MgrPaper`'s own group-and-question walker — the heads, the numbers
and the bullets are identical — and each ask's answer is its scheme block with
the PAPER's printed text taken off the front. Where the two documents disagree
about what was asked, the subtraction fails and `flags()` says so rather than
handing back a question as though it were an answer.

Question 1's five words are the case that makes this worth doing: the scheme
prints "εκτεταμένες  πολύ μεγάλες, διευρυμένες" — the word the paper set,
then its gloss, with nothing but space between them. Cutting the paper's own
word off the front of each row leaves exactly the gloss, and the five become
the five rows of one card.

**2015 is unreadable and is the one exclusion this subject forces.** Its scheme
embeds every font with a broken ToUnicode CMap: 0 of the document's characters
come back as Greek, against 2,365-8,138 in every other scheme in the corpus.
`derive_glyphs.py --subject modern-greek` cannot repair it — the glyph ids in
those subsets appear nowhere in the corpus with a correct mapping, and it
repaired 61 sightings. The paper is fine; the answers are not recoverable, so
that sitting's asks are excluded with the count as their evidence.
"""
import argparse
import difflib
import os
import re
import sys
import unicodedata

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(HERE)))
sys.path.insert(0, HERE)

from mgr_paper import (MgrPaper, SUBJECT, _clean, sittings)   # noqa: E402

GREEK = re.compile(r'[Ͱ-Ͽ]')


# Rows the SEC itself printed wrong, keyed by sitting and matched against the
# whole printed row. The correction is what the PAPER prints at that address.
MISPRINTS = {
    # 2017 numbers Question 1's FIVE underlined words "2." to "6." — the same
    # numbers its six comprehension questions use, in the same group, three
    # lines above them. Read as questions they consumed the run and the real
    # Questions 2 to 6 could not open, so five of that sitting's six answers
    # were filed against the wrong ask. The paper prints these five as
    # Question 1's bullets; the scheme's own text is unchanged apart from the
    # marker.
    (2017, 'hl'): [
        ('2. η συντριπτική πλειοψηφία ο μεγαλύτερος αριθμός αυτών που '
         'αποφασίζουν',
         '• η συντριπτική πλειοψηφία ο μεγαλύτερος αριθμός αυτών που '
         'αποφασίζουν'),
        ('3. η ελεημοσύνη η βοήθεια σε κάποιον που δεν έχει',
         '• η ελεημοσύνη η βοήθεια σε κάποιον που δεν έχει'),
        ('4. παρέχουν δίνουν', '• παρέχουν δίνουν'),
        ('5. αντιξοότητες οι δυσκολίες', '• αντιξοότητες οι δυσκολίες'),
        ('6. διακρίνονται ξεχωρίζουν', '• διακρίνονται ξεχωρίζουν'),
    ],
}


def scheme_path(year, level, subject=SUBJECT):
    path = os.path.join(ROOT, 'examiner-reports', subject, 'schemes',
                        f'{year}-{level}.pdf')
    if not os.path.exists(path):
        raise FileNotFoundError(f'no {subject} scheme for {year} {level}')
    return path


def has_scheme(year, level, subject=SUBJECT):
    return os.path.exists(os.path.join(ROOT, 'examiner-reports', subject,
                                       'schemes', f'{year}-{level}.pdf'))


# Latin letters the SEC types by accident where the Greek homograph belongs.
# 2016 sets Question 5 as "O συγγραφέας" in the paper with a LATIN capital O
# and as "Ο συγγραφέας" with the Greek one in the scheme; nothing on the page
# distinguishes them and the two documents stopped matching at character one.
LOOKALIKE = str.maketrans({
    'A': 'Α', 'B': 'Β', 'E': 'Ε', 'H': 'Η', 'I': 'Ι', 'K': 'Κ', 'M': 'Μ',
    'N': 'Ν', 'O': 'Ο', 'P': 'Ρ', 'T': 'Τ', 'X': 'Χ', 'Y': 'Υ', 'Z': 'Ζ',
    'a': 'α', 'e': 'ε', 'o': 'ο', 'v': 'ν', 'p': 'ρ', 'y': 'υ',
})


def _fold(text):
    """Accents, case and punctuation off — for MATCHING only.

    The scheme RETYPES the paper's question rather than copying it, and the
    differences are always the same kind: a missing accent, a comma moved, a
    Latin O for a Greek one, a word inserted. Folding those out is what lets
    the paper's text be found inside the scheme's block; the text that ships
    is always the ORIGINAL, never the folded form.
    """
    text = text.translate(LOOKALIKE).lower()
    text = ''.join(c for c in unicodedata.normalize('NFD', text)
                   if not unicodedata.combining(c))
    return re.sub(r'[^\w]+', '', text)


def _fold_map(text):
    """(folded text, [original index for each folded character])."""
    out, idx = [], []
    for i, ch in enumerate(text):
        f = _fold(ch)
        for c in f:
            out.append(c)
            idx.append(i)
    return ''.join(out), idx


class MgrScheme(MgrPaper):
    """The scheme, read with the paper's walker."""

    def __init__(self, year, level, subject=SUBJECT):
        self.year, self.level, self.subject = year, level, subject
        self._fixed = False
        self.path = scheme_path(year, level, subject)
        import pymupdf
        self._doc = pymupdf.open(self.path)
        self._runs = None
        self._asks = None
        self.section_marks = {}
        self.passage = ''
        self.passage_pages = []
        self.answer_language = None
        self.flags = []

    def _stream(self):
        runs = super()._stream()
        fixes = MISPRINTS.get((self.year, self.level), [])
        if fixes and not getattr(self, '_fixed', False):
            done = set()
            for i, (pg, text) in enumerate(runs):
                for wrong, right in fixes:
                    if text == wrong and wrong not in done:
                        runs[i] = (pg, right)
                        done.add(wrong)
            missing = [w for w, _r in fixes if w not in done]
            if missing:
                raise AssertionError(
                    f'{self.year} {self.level}: misprint row not found, so '
                    f'the correction is stale: {missing[0]!r}')
            self._fixed = True
        return runs

    def readable(self):
        """Does any Greek survive this scheme's text layer at all?"""
        return sum(len(GREEK.findall(t)) for _, t in self._stream())

    def blocks(self):
        """{key: the scheme's whole printed block for that ask}."""
        return {a.key: a for a in self.asks()}


def answers(year, level, subject=SUBJECT):
    """{key: (answer, item glosses)} for one sitting, plus the faults found."""
    P = MgrPaper(year, level, subject)
    S = MgrScheme(year, level, subject)
    out, faults = {}, []
    if not S.readable():
        return out, [{'type': 'scheme-unreadable',
                      'detail': 'the scheme\'s text layer returns no Greek at '
                                'all — every font is embedded with a broken '
                                'ToUnicode CMap'}]
    blocks = S.blocks()
    # 2021 is printed as "Μέρος πρώτο" and "Μέρος δεύτερο" in the PAPER and as
    # "ΟΜΑΔΑ 1η" and "ΟΜΑΔΑ 2η" in the SCHEME — the same two parts of the same
    # examination under two names. They are paired on printed ORDER, which is
    # safe because both documents print exactly two and in the same sequence.
    paper_secs = [s for s in dict.fromkeys(a.section for a in P.asks())]
    scheme_secs = [s for s in dict.fromkeys(k[0] for k in blocks)]
    remap = {}
    if paper_secs != scheme_secs and len(paper_secs) == len(scheme_secs):
        remap = dict(zip(paper_secs, scheme_secs))
    for ask in P.asks():
        key = ask.key
        if remap:
            key = (remap[key[0]],) + key[1:]
        entry = blocks.get(key)
        if entry is None:
            faults.append({'type': 'scheme-missing-ask',
                           'where': str(ask.key),
                           'detail': 'the paper prints this ask and the '
                                     'scheme prints no block at that address'})
            continue
        answer = _after(entry.raw, ask.text)
        if answer is None and ask.items:
            # Question 1's answer IS its five glosses, and the scheme
            # routinely shortens the instruction above them — 2018 sets
            # "…φράσεων που είναι υπογραμμισμένες στο δοσμένο κείμενο:" in the
            # paper and "…φράσεων:" in the scheme. The instruction not lining
            # up says nothing about the five words underneath it.
            answer = ''
        if answer is None:
            # The scheme's block at this address does NOT contain the question
            # the paper printed there, so the two documents are not talking
            # about the same ask and whatever the block holds is not its
            # answer. Handing the block back regardless is how a wrong pairing
            # ships past every downstream gate (Law 4), so it is a fault.
            faults.append({'type': 'unpaired-ask', 'where': str(ask.key),
                           'detail': 'the scheme block at this address does '
                                     'not reprint the question the paper sets'})
            continue
        items = glosses(entry.items, ask.items) if ask.items else []
        if not answer and not items:
            faults.append({'type': 'unanswered-ask', 'where': str(ask.key),
                           'detail': 'the scheme reprints the question and '
                                     'states nothing under it'})
            continue
        out[ask.key] = (answer, items)
    return out, faults


# The tail of a tariff the paper's own ask text no longer carries: an ask is
# stored with "(5 βαθμοί)" taken off it, so the alignment stops just before the
# scheme's copy of the same tariff and the answer would open "5 βαθμοί)".
LEAD_TARIFF = re.compile(
    r'^\s*\(?\s*\d{1,3}\s*(?:βαθμο[ίύ]|μονάδες|[×xΧ]\s*\d)?\s*\)\s*')
TRAIL_RATE = re.compile(r'\s*\(\s*\d\s*[×xΧ]\s*\d\s*\)\s*$')


def _tidy(text):
    text = LEAD_TARIFF.sub('', text.strip(' :;.,-–—'))
    return TRAIL_RATE.sub('', text).strip(' :;.,-–—')


def _snap(idx, end):
    """Pull `end` back to the start of the word it landed inside.

    An approximate match stops wherever the alignment ran out, which in 2017
    was two letters into "μεγαλύτερος" — and the gloss then shipped as
    "γαλύτερος αριθμός…". A gloss always begins at a word, so the cut is moved
    back to the last one. Folding drops the spaces, so "still inside a word" is
    "this folded character came from the very next character of the original".
    """
    end = min(end, len(idx))
    while 0 < end < len(idx) and idx[end] == idx[end - 1] + 1:
        end -= 1
    return end


def _after(block, question):
    """What the scheme printed AFTER the question it reprinted, or None.

    Aligned rather than matched exactly, because the scheme retypes: 2022 sets
    "Πώς εξηγείται η έλλειψη της αλληλεγγύης την περίοδο της πανδημίας;" in the
    paper and "…μετά την πρώτη περίοδο…" in the scheme. difflib finds the
    longest run of agreement between the two folded texts and the answer is
    everything past its END; a run that covers less than seventy per cent of
    the question is not that question, and the caller is told so rather than
    handed a block to ship.
    """
    block = _clean(block)
    if not question:
        return block
    fb, idx = _fold_map(block)
    fq = _fold(question)
    if not fq:
        return block
    if len(fq) < 12:
        return _tidy(block[idx[fb.index(fq)] + len(fq):]) \
            if fq in fb else None
    sm = difflib.SequenceMatcher(None, fb, fq, autojunk=False)
    matched = sum(b.size for b in sm.get_matching_blocks())
    if matched < 0.7 * len(fq):
        return None
    end = max((b.a + b.size for b in sm.get_matching_blocks() if b.size),
              default=0)
    if end >= len(idx):
        return ''
    return _tidy(block[idx[end]:])


def glosses(rows, words):
    """[(word, gloss)] for Question 1's five items, or [].

    The scheme prints the word the paper set and then its gloss with nothing
    but space between them — "εκτεταμένες  πολύ μεγάλες, διευρυμένες" — and
    wraps them across rows freely, so the rows are joined and each word is
    found in printed ORDER. A word that is not there at all breaks the pairing
    for the whole ask rather than for one row: five glosses or none.
    """
    block = _clean(' '.join(rows))
    fb, idx = _fold_map(block)
    out, pos = [], 0
    spans = []
    for word in words:
        fw = _fold(word)
        if not fw:
            return []
        at, end = fb.find(fw, pos), None
        if at >= 0:
            end = at + len(fw)
        else:
            # Greek retyping differs in the ENDING, not the stem: 2016
            # underlines "Εκφράζει" in its passage and glosses "Εκφράζω" in
            # its scheme. Find the stem, then run to the end of whatever word
            # the scheme actually set — so the gloss starts after its last
            # letter and not in the middle of it.
            stem = fw[:max(5, int(len(fw) * 0.7))]
            at = fb.find(stem, pos)
            if at < 0:
                # The scheme's phrase can also be LONGER than the paper's —
                # 2017 sets "συντριπτική τους πλειοψηφία" and glosses
                # "η συντριπτική πλειοψηφία" — so the last resort is an
                # approximate window, cut back to a word boundary.
                at = _near(fb, fw, pos)
                end = _snap(idx, at + len(fw)) if at >= 0 else None
            else:
                end = at + len(stem)
                # Run to the end of the word the scheme actually set. Folding
                # drops the spaces, so "still inside this word" is "the next
                # folded character came from the very next character of the
                # original" — an isalpha() test walks the whole block.
                while end < len(fb) and idx[end] == idx[end - 1] + 1:
                    end += 1
        if at < 0 or end is None:
            return []
        spans.append((at, end))
        pos = end
    for n, (start, end) in enumerate(spans):
        stop = spans[n + 1][0] if n + 1 < len(spans) else len(idx)
        lo = idx[end] if end < len(idx) else len(block)
        hi = idx[stop] if stop < len(idx) else len(block)
        gloss = _tidy(block[lo:hi].strip(' :;.,-–—•/'))
        if not gloss:
            return []
        out.append((words[n], gloss))
    return out


def _near(haystack, needle, start):
    """Where `needle` almost appears in `haystack` at or after `start`.

    The SEC retypes a word as well as a sentence: 2016 underlines "Εκφράζει" in
    its passage and glosses "Εκφράζω" in its scheme, one letter apart. A window
    is accepted at 0.85 similarity, which is close enough to be the same word
    and far from any other of the five.
    """
    best, at, n = 0.75, -1, len(needle)
    for width in (n, int(n * 1.3) + 1):
        for i in range(start, max(start, len(haystack) - width) + 1):
            r = difflib.SequenceMatcher(None, haystack[i:i + width], needle,
                                        autojunk=False).ratio()
            if r > best:
                best, at = r, i
    return at


def survey():
    print(f"{'sitting':8} {'greek':>7} {'asks':>5} {'answered':>9}  faults")
    for year, level in sittings():
        if not has_scheme(year, level):
            print(f'{year}    no marking scheme published')
            continue
        S = MgrScheme(year, level)
        got, faults = answers(year, level)
        answered = sum(1 for a, _i in got.values() if a)
        print(f'{year:<8} {S.readable():>7} {len(got):>5} {answered:>9}  '
              f'{faults[0]["type"] if faults else ""}')


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('year', nargs='?', type=int)
    ap.add_argument('level', nargs='?', default='hl')
    ap.add_argument('--survey', action='store_true')
    args = ap.parse_args()
    if args.survey:
        survey()
        return 0
    got, faults = answers(args.year, args.level)
    for f in faults:
        print('  FLAG', f)
    for key, (answer, items) in got.items():
        print(f'  {str(key):22} {answer[:78]}')
        for word, gloss in items:
            print(f'        {word:34} -> {gloss[:44]}')
    return 0


if __name__ == '__main__':
    sys.exit(main())
