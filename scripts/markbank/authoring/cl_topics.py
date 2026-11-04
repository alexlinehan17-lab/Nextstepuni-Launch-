#!/usr/bin/env python3
"""Which part of the course a Classical Studies ask belongs to.

    python3 scripts/markbank/authoring/cl_topics.py --audit

Two taxonomies, because the corpus straddles a syllabus change and a card is
filed under the course the paper it came from was set on.

**2021-2022 — the ten topics.** The old paper prints the topic over every
question it sets, identically in all four sittings, so nothing has to be
inferred: the topic IS the address. Those ten are the legacy strand.

**2023-2025 — the four strands.** The new specification names four strands and
eighteen subtopics, and the canonical curriculum already carries them
(curriculum.ts, classical-studies-0 .. classical-studies-3). The paper does not
print which strand a question belongs to, so it is matched on the prescribed
material the question NAMES — "Homer's Odyssey", "the Parthenon", "Euripides'
Medea", "Plato's Crito" — which the specification also names. A question that
names nothing is refused rather than filed on a guess, and the refusals are
counted and printed by --audit.
"""
import argparse
import re
import sys

# ------------------------------------------------------ the legacy strand ---
# Printed identically on 2021 and 2022, both levels — checked against all four
# papers before it was written down.
LEGACY_TOPICS = {
    1: ('classical-studies-legacy-1', 'Athens at War'),
    2: ('classical-studies-legacy-2', 'Alexander the Great'),
    3: ('classical-studies-legacy-3', 'Life and Thought in the Late Roman Republic'),
    4: ('classical-studies-legacy-4', 'Roman Historians'),
    5: ('classical-studies-legacy-5', 'Greek Drama'),
    6: ('classical-studies-legacy-6', 'Ancient Epic'),
    7: ('classical-studies-legacy-7', 'Writers of the Augustan Age'),
    8: ('classical-studies-legacy-8', 'Art and Architecture in Greek Society'),
    9: ('classical-studies-legacy-9',
        'The Philosopher in Society: A Study of Socrates and Plato'),
    10: ('classical-studies-legacy-10', 'Roman Art and Architecture'),
}

# ---------------------------------------------- the current specification ---
# Each entry is (subtopic id, the words the SPECIFICATION uses for it that a
# question also prints). Order matters: the first match wins, so the most
# specific prescribed text is tested before the strand's general vocabulary.
CURRENT = [
    ('classical-studies-0-3', r"\bOdyssey\b|\bOdysseus\b|\bPenelope\b"
                              r"|\bTelemachus\b|\bCalypso\b|\bCirce\b"),
    ('classical-studies-0-4', r"\bAeneid\b|\bAeneas\b|\bDido\b|\bLaocoön\b"
                             r"|\bAnchises\b|\bAscanius\b|\bVirgil\b"),
    ('classical-studies-3-3', r"\bCrito\b|\bSocrates\b|\bHorace\b|\bOdes?\b"
                             r"|\bEpodes?\b|\bliving well\b|\bmortality\b"),
    ('classical-studies-1-2', r"\bMedea\b|\bPhiloctetes\b|\bEuripides\b"
                             r"|\bSophocles\b"),
    ('classical-studies-1-3', r"\bColosseum\b|\bCircus Maximus\b|\bgladiator"
                             r"|\bchariot rac|\bspectacle\b|\bamphitheatre"),
    ('classical-studies-1-1', r"\bCity Dionysia\b|\bDionys|\bTheatre of Dionys"
                             r"|\bfestival of\b"),
    ('classical-studies-1-0', r"\bTragedy\b|\btragic\b|\bChorus\b|\bplaywright\b"
                             r"|\btheatre\b|\bstaging\b|\bmask"),
    ('classical-studies-2-1', r"\bstrateg|\bmilitary\b|\bbattle\b|\bsiege\b"
                             r"|\bcampaign\b|\barmy\b|\binfantry\b|\blegion\b"),
    ('classical-studies-2-3', r"\bconquered\b|\bforeign\b|\bbarbarian\b"
                             r"|\bPersian|\bGaul"),
    ('classical-studies-2-4', r"\bArrian\b|\bPlutarch\b|\bSuetonius\b"
                             r"|\bancient (?:authors|sources)\b|\bbias\b"
                             r"|\bbiography\b|\bhistoriograph"),
    ('classical-studies-2-2', r"\bAlexander\b|\bCaesar\b"),
    ('classical-studies-3-1', r"\bParthenon\b|\bErechtheion\b|\bPantheon\b"
                             r"|\bTemple of Vesta\b|\btemple"),
    ('classical-studies-3-2', r"\bfunerar|\bfuneral|\bgrave\b|\bstele\b"
                             r"|\bafterlife\b|\bUnderworld\b|\bmourn|\bburial\b"
                             r"|\bpompa\b|\bprothesis\b"),
    ('classical-studies-3-0', r"\bgod\b|\bgods\b|\bgoddess|\bdeit|\bZeus\b"
                             r"|\bJupiter\b|\bAthena\b|\bmyth|\bVestal\b"
                             r"|\bdivine\b|\bOlympian\b|\bpiety\b"),
    ('classical-studies-0-0', r"\bhero\b|\bheroes\b|\bheroic\b|\bleader"),
    ('classical-studies-0-1', r"\bhospitality\b|\bxenia\b|\bheroic society\b"),
    ('classical-studies-0-2', r"\bepic\b|\bsimile\b|\bepithet\b|\becphrasis\b"
                             r"|\bin medias res\b|\bring composition\b"
                             r"|\bstorytelling\b|\bpoetry\b|\bpoem\b|\bpoet\b"),
    ('classical-studies-2-0', r"\bRome\b|\bRoman\b|\bGreek\b|\bGreece\b"
                             r"|\bAthens\b|\bAthenian\b"),
]
CURRENT_RE = [(tid, re.compile(pat, re.I)) for tid, pat in CURRENT]


def legacy_topic(topic_number):
    return LEGACY_TOPICS[topic_number][0]


def current_topic(text):
    """The subtopic a new-syllabus question names, or None.

    None is a refusal, not a default. Filing an unmatched question under a
    catch-all would put it in a strand a student is not revising and hide the
    fact that the reader never saw what the question was about.
    """
    for tid, pattern in CURRENT_RE:
        if pattern.search(text):
            return tid
    return None


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--audit', action='store_true')
    ap.parse_args()
    sys.path.insert(0, __file__.rsplit('/', 1)[0])
    from cl_paper import ClPaper                                # noqa: E402
    import collections
    hits = collections.Counter()
    misses = []
    for year in (2023, 2024, 2025):
        for level in ('hl', 'ol'):
            P = ClPaper(year, level)
            for ask in P.asks():
                text = f'{ask.stem} {ask.text}'
                tid = current_topic(text)
                if tid:
                    hits[tid] += 1
                else:
                    misses.append(f'{year} {level} Q{ask.q}'
                                  f'({ask.letter or ""}) {text[:90]}')
    for tid, n in sorted(hits.items()):
        print(f'  {tid:24} {n}')
    print(f'  matched {sum(hits.values())}, unmatched {len(misses)}')
    for m in misses:
        print(f'   UNMATCHED {m}')
    return 0


if __name__ == '__main__':
    sys.exit(main())
