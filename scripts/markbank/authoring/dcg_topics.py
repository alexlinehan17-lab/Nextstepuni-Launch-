#!/usr/bin/env python3
"""Which syllabus heading a Design & Communication Graphics question is under.

    python3 scripts/markbank/authoring/dcg_topics.py --audit

The headings are the CANONICAL curriculum's own (curriculum.ts, subject
'design-and-communication-graphics'), so a card's topicId is a taxonomy already
published rather than one invented here. Two of its three strands are what the
written examination covers:

    strand 0  Plane and Descriptive Geometry (Core)       Sections A and B
    strand 2  Applied Graphics (Optional Areas)           Section C

Strand 1, Communication of Design and Computer Graphics, is the student
assignment and the CAD work; the written paper sets nothing under it, and no
card tags there.

SECTION C NEEDS NO CLASSIFIER. Each of its five questions IS one of the five
optional areas, and the paper prints the area's name as a banner on the
question's own page -- "Geologic Geometry", "Dynamic Mechanisms". dcg_paper
reads that banner, so the topic is lifted rather than guessed, and `--audit`
asserts every Section C question in the corpus carries one.

SECTIONS A AND B ARE CLASSIFIED ON THE PRINTED WORDS of the question and of
the scheme's own priced steps together, by the vocabulary the syllabus heading
names. The rules are ordered most specific first, because the vocabularies
overlap: a skew-lines question is also about lines and planes, and an
interpenetration question also completes an elevation. `--audit` prints the
share of questions each heading takes and the share that reached the fallback.
"""
import argparse
import collections
import glob
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

PREFIX = 'design-and-communication-graphics'

# strand 0 — Plane and Descriptive Geometry (Core)
PROJECTION_SYSTEMS = f'{PREFIX}-0-0'
ORTHOGRAPHIC = f'{PREFIX}-0-1'
AXONOMETRIC = f'{PREFIX}-0-2'
PERSPECTIVE = f'{PREFIX}-0-3'
PLANE_GEOMETRY = f'{PREFIX}-0-4'
CONIC_SECTIONS = f'{PREFIX}-0-5'
LINES_AND_PLANES = f'{PREFIX}-0-6'
DEVELOPMENTS = f'{PREFIX}-0-7'
INTERPENETRATION = f'{PREFIX}-0-8'
SKEW_LINES = f'{PREFIX}-0-9'
OBLIQUE_PLANE = f'{PREFIX}-0-10'
LAMINA_PLANES = f'{PREFIX}-0-11'
SOLIDS_IN_CONTACT = f'{PREFIX}-0-12'
ROTATION = f'{PREFIX}-0-13'
TETRAHEDRON = f'{PREFIX}-0-14'

# strand 2 — Applied Graphics (Optional Areas), by the banner the paper prints
OPTION_TOPIC = {
    'Dynamic Mechanisms': f'{PREFIX}-2-0',
    'Structural Forms': f'{PREFIX}-2-1',
    'Geologic Geometry': f'{PREFIX}-2-2',
    'Surface Geometry': f'{PREFIX}-2-3',
    'Assemblies': f'{PREFIX}-2-4',
}

# Ordered most specific first: the vocabularies overlap, and the first rule
# that fires wins. Every phrase here is one the papers and schemes actually
# print — `--audit` reports what each takes.
RULES = [
    (SKEW_LINES, r'skew lines?'),
    (TETRAHEDRON, r'tetrahedron'),
    (INTERPENETRATION, r'interpenetrat|penetration point|intersecting solids'
                       r'|line of intersection between the|curve of intersection'
                       r'|intersection of the (?:two )?(?:solids|prisms|cylinders)'),
    (DEVELOPMENTS, r'surface development|development of the|envelopment'
                   r'|one-piece development|developed surface'),
    # "are in contact as shown" and "are in mutual contact" are how the
    # Ordinary papers say it; a rule that only read "in contact with" sent
    # both of those questions to the fallback.
    (SOLIDS_IN_CONTACT, r'\bin (?:mutual )?contact\b|solids in contact'
                        r'|point of contact|tangential to the|resting on the'),
    (PERSPECTIVE, r'perspective|vanishing point|picture plane|spectator point'),
    (AXONOMETRIC, r'axonometric|isometric|trimetric|dimetric'),
    (CONIC_SECTIONS, r'parabol|ellips|hyperbol|latus rectum|directrix'
                     r'|eccentricit|conic|focal point|\bfocus\b|\bfoci\b'),
    # The Ordinary logo questions -- the Nintendo Switch outline, the disco
    # projector -- are struck arcs and circles and nothing else: "Draw a
    # circle of radius 10 mm at point P", "Determine centre of arcs", "Draw
    # arcs to complete logo". They reached the fallback without the last two
    # alternatives here.
    (PLANE_GEOMETRY, r'\bcycloid|involute|archimedean|spiral|helix|\blocus\b'
                     r'|\bloci\b|tangent(?:ial)? arc|arcs? of radius'
                     r'|circumscrib|inscribed circle'
                     r'|circle (?:of )?radius|radius \d+\s*mm'
                     r'|centre of arcs|draw arcs\b'),
    (OBLIQUE_PLANE, r'oblique plane|\bVTH\b|horizontal trace|vertical trace'
                    r'|traces of the plane|\bH\.?T\.?\b and \bV\.?T\.?\b'),
    (LAMINA_PLANES, r'dihedral angle|true shape of (?:the )?(?:triangle|plane'
                    r'|surface)|lamina|planes? [A-Z]{3}\b'),
    (ROTATION, r'inclination of|inclined at|angle of inclination|rotat'
               r'|true angle|true length'),
    (LINES_AND_PLANES, r'auxiliary (?:elevation|plan|view)|X1Y1|\bX2Y2\b'
                       r'|projections? of the (?:line|point)|strike|\bdip\b'),
]
FALLBACK = ORTHOGRAPHIC

ALL_TOPICS = ([PROJECTION_SYSTEMS, ORTHOGRAPHIC, AXONOMETRIC, PERSPECTIVE,
               PLANE_GEOMETRY, CONIC_SECTIONS, LINES_AND_PLANES, DEVELOPMENTS,
               INTERPENETRATION, SKEW_LINES, OBLIQUE_PLANE, LAMINA_PLANES,
               SOLIDS_IN_CONTACT, ROTATION, TETRAHEDRON]
              + sorted(OPTION_TOPIC.values()))


def topic_for(section, option, text):
    """The syllabus heading this question sits under, and how it was decided.

    Returns (topicId, 'banner'|'<matched phrase>'|'fallback').
    """
    if section == 'C':
        if option and option in OPTION_TOPIC:
            return OPTION_TOPIC[option], 'banner'
        return None, 'no option banner printed'
    for topic, pattern in RULES:
        m = re.search(pattern, text, re.I)
        if m:
            return topic, m.group(0).lower()
    return FALLBACK, 'fallback'


def concept_for(topic):
    return topic.replace(f'{PREFIX}-', 'dcg-')


def audit():
    from dcg_paper import DcgPaper                             # noqa: E402
    from dcg_scheme import DcgScheme, has_scheme               # noqa: E402
    counts = collections.Counter()
    how = collections.Counter()
    missing = []
    for f in sorted(glob.glob(os.path.join(
            os.path.dirname(os.path.dirname(os.path.dirname(HERE))),
            'examiner-reports', 'dcg', 'schemes', '*.md'))):
        year, level = os.path.basename(f)[:-3].split('-')
        year = int(year)
        P = DcgPaper(year, level)
        S = DcgScheme(year, level) if has_scheme(year, level) else None
        for key, qq in sorted(P.questions.items()):
            words = [qq['stem']] + [t for _lt, _rm, t in qq['parts']]
            if S and key in S.questions:
                for u in S.questions[key].units:
                    words.append(u.title)
                    words += [s.text for s in u.steps]
            topic, why = topic_for(key[0], qq['option'], ' '.join(words))
            if topic is None:
                missing.append((year, level, key, why))
                continue
            counts[topic] += 1
            how[why if why in ('banner', 'fallback') else 'phrase'] += 1
    total = sum(counts.values())
    for topic, n in counts.most_common():
        print(f'  {n:4} ({100 * n // max(total, 1):3}%)  {topic}')
    print(f'{total} questions classified; '
          f'{how["banner"]} by the paper\'s own option banner, '
          f'{how["phrase"]} by a printed phrase, '
          f'{how["fallback"]} by the fallback '
          f'({100 * how["fallback"] // max(total, 1)}%)')
    for row in missing:
        print(f'  UNCLASSIFIED {row}')
    return len(missing)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--audit', action='store_true')
    ap.parse_args()
    return 0 if audit() == 0 else 1


if __name__ == '__main__':
    sys.exit(main())
