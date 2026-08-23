#!/usr/bin/env python3
"""File a Mathematics part under a syllabus topic from its wording.

Vocabulary taken from the strand and topic titles in components/MarkBank/deck.ts,
which are the 2015 syllabus's own. Most specific match wins. Anything unmatched
is reported rather than filed under a default: a wrong shelf is worse than a gap.
"""
import re

RULES = [
    ('maths-5-2', 9, r'\b(derivative|differentiat\w*|integrat\w*|rate of change|'
                     r'tangent to the curve|maximum|minimum|turning point|'
                     r'limit|d[xy]/d[xy])\b|∫|[A-Za-z]\^?′\s*\(|′\('),
    ('maths-4-4', 9, r'\b(complex number|argand|modulus of z|conjugate|de moivre|'
                     r'\bz\s*=|imaginary)(?!\w)'),
    ('maths-2-3', 9, r'\b(sin|cos|tan|trigonometr\w*|radian|triangle|bearing|'
                     r'unit circle|period|amplitude)(?!\w)'),
    ('maths-2-2', 9, r'\b(co-?ordinate\w*|the line l|on the line|the point [A-Z]\(|slope|midpoint|equation of the '
                     r'(?:line|circle)|centre and radius|perpendicular distance)(?!\w)'),
    # A bare circle is weaker than either shelf that names one: "the area of
    # the circle" is mensuration, "the equation of the circle" is co-ordinate
    # geometry, and only a circle named with neither lands here.
    ('maths-2-2', 6, r'\b(circles?|centre \()'),
    ('maths-2-1', 8, r'\b(theorem|proof|congruen\w*|similar(?: triangles)?|parallelogram|'
                     r'circumcircle|incircle)(?!\w)'),
    ('maths-2-4', 8, r'\b(enlargement|scale factor|transformation)(?!\w)'),
    ('maths-1-2', 9, r'\b(probabilit\w*|at random|expected value|independent events|'
                     r'mutually exclusive)(?!\w)'),
    ('maths-1-1', 8, r'\b(how many (?:ways|arrangements)|permutation|combination|'
                     r'\bfactorial\b|counting)(?!\w)'),
    ('maths-1-6', 8, r'\b(histogram|box ?plot|stem[- ]and[- ]leaf|scatter\w*|mean|median|'
                     r'standard deviation|interquartile)(?!\w)'),
    ('maths-1-7', 8, r'\b(hypothesis|confidence interval|margin of error|p-?value|'
                     r'correlation|inference|sample proportion)(?!\w)'),
    ('maths-1-5', 7, r'\b(survey|questionnaire|sampl(?:e|ing)|population|bias)(?!\w)'),
    ('maths-1-3', 7, r'\b(random process|outcome\w*|relative frequency|dice|coin)(?!\w)'),
    ('maths-3-4', 9, r'\b(volume|surface area|area of|perimeter|cylinder|sphere|'
                     r'cone|prism|frustum)(?!\w)'),
    ('maths-3-2', 8, r'\b(ind(?:ex|ices)|surd|√|power of|exponent|logarithm|\bln\b)(?!\w)'),
    ('maths-3-3', 8, r'\b(compound interest|\bapr\b|\baer\b|depreciat\w*|percentage|'
                     r'currency|loan|annuity|instal?ment|exchange rate|discount|'
                     r'\bvat\b|price|cost|speed|km/h|per hour)(?!\w)|[€$£]'),
    ('maths-3-1', 7, r'\b(natural number|integer|rational|irrational|prime|'
                     r'number system|ℝ|ℕ|ℤ|ℚ)(?!\w)'),
    ('maths-4-2', 9, r'\b(solve|solutions?\b|simultaneous|quadratic|'
                     r'root[s]? of|factoris\w*|equation h?\(|has exactly one)(?!\w)'),
    # More specific than "solve": every inequality is also solved.
    ('maths-4-3', 10, r'\b(inequalit\w*|≤|≥|greater than or equal|less than or equal)(?!\w)'),
    ('maths-4-1', 7, r'\b(simplify|multiply out|expand|expression|sequence|'
                     r'\bterms?\b|arithmetic sequence|geometric series|pattern|'
                     r'values in the table|\bnth\b|show that [A-Z]\()(?!\w)'),
    # Evaluating a named function. Its own rule because the guard the others
    # carry refuses a digit straight after the bracket, and "Find f(0.67)"
    # is exactly that.
    ('maths-5-1', 6, r'\bfind [fgh]\s*\('),
    ('maths-5-1', 6, r'\b(function|[fgh]\(x\)|graph of|domain|range|'
                     r'injective|surjective|inverse)(?!\w)'),
]
COMPILED = [(t, w, re.compile(p, re.I)) for t, w, p in RULES]


def topic_for(text):
    best = (0, None, None)
    for tid, weight, rx in COMPILED:
        m = rx.search(text or '')
        if m and weight > best[0]:
            best = (weight, tid, m.group(0))
    return best[1], best[2]


def concept_for(text, fallback='part'):
    words = re.sub(r'[^a-z0-9 ]', ' ', (text or '').lower()).split()
    skip = {'the', 'a', 'an', 'of', 'to', 'in', 'for', 'and', 'is', 'are', 'by',
            'find', 'show', 'that', 'this', 'your', 'answer', 'give', 'use',
            'hence', 'above', 'below', 'following', 'where', 'with', 'from'}
    keep = [w for w in words if w not in skip and len(w) > 2][:6]
    return '-'.join(keep) or fallback
