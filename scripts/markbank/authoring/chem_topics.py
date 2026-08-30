#!/usr/bin/env python3
"""SUGGEST a syllabus topic for a Chemistry part. A suggestion, not a verdict.

Measured against the 873 cards already carrying a hand-assigned topic, these
rules fire on 769 and are right on 416 of them -- **54%**. That is far too low
to file a card by, and it does not improve when the question's opening stem is
fed in as well. The reason is in the disagreements: the commonest by a distance
is a part the deck files under chem-u2 "Investigating in chemistry" that reads,
in its own words, as organic chemistry or rates of reaction. Whether a part is
about the EXPERIMENT or about the CHEMISTRY IN it is a judgement the wording
does not carry, and Q4 and Q11 are deliberately multi-topic besides -- 2023 HL
Q11 alone spans six shelves.

So this exists to put a first guess in front of a person, and every card it
suggests for is reviewed before it ships. Run this file to re-measure; if a
rule is added, the number here has to be updated with it.

The original intent:

    python3 scripts/markbank/authoring/chem_topics.py     # score against the deck

Vocabulary taken from the strand and topic titles in components/MarkBank/deck.ts,
which are the syllabus's own. Most specific match wins. Anything unmatched is
REPORTED rather than filed under a default: a wrong shelf sends a student to
revise the wrong thing, and a gap only asks a human to look.

The rules are scored against the 873 cards already in the authored deck, which
carry a topic assigned by hand. That is a real test set, and running this file
prints the agreement and every disagreement, so a rule cannot be tuned into
looking right without the number moving.
"""
import collections
import json
import os
import re
import sys

DIR = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(DIR)))

RULES = [
    # ── Strand 4: the mandatory experiments, most specific of all ──────────
    ('chem-4-1', 11, r'\b(titrat\w*|volumetric flask|pipette|burette|conical flask|'
                     r'standard solution|primary standard|end[- ]?point|indicator|'
                     r'aliquot|molarity of the|deionised water|rough titration)\b'),
    ('chem-4-3', 10, r'\b(water hardness|dissolved oxygen|\bbod\b|\bph\b of the (?:river|water)|'
                     r'chlorination|fluoridation|sewage|effluent|water treatment|'
                     r'atmospher\w*|ozone|greenhouse|acid rain|pollut\w*|'
                     r'instrumental|chromatograph\w*|spectroscop\w*|colorimet\w*)\b'),
    ('chem-4-2', 10, r'\b(recrystallis\w*|melting point of the|reflux|distillat\w*|'
                     r'soxhlet|filtration under|ester(?:ification)?|'
                     r'oxidation of an alcohol|prepar\w+ of (?:soap|aspirin|ethene))\b'),
    # ── Strand 3: energy and change ────────────────────────────────────────
    ('chem-3-1', 10, r'\b(heat of (?:combustion|formation|reaction|neutralisation)|'
                     r'enthalp\w*|exothermic|endothermic|calorimet\w*|bond energy|'
                     r'hess|ΔH|kJ mol)\b'),
    ('chem-3-2', 10, r'\b(rate of (?:the )?reaction|catalys\w*|activation energy|'
                     r'collision theory|reaction rate|initial rate|'
                     r'effect of (?:temperature|concentration) on the rate)\b'),
    ('chem-3-3', 10, r'\b(equilibri\w*|le ch[aâ]telier|\bkc\b|reversible reaction|'
                     r'forward reaction|position of equilibrium)\b'),
    ('chem-3-4', 10, r'\b(acid|base|alkal\w*|\bph\b|\bka\b|\bkw\b|conjugate|'
                     r'br[oø]nsted|neutralis\w*|amphoteric|buffer|hydronium|'
                     r'\bh\+\b|hydroxide ion|proton donor|proton acceptor)\b'),
    ('chem-3-5', 10, r'\b(oxidation number|oxidising agent|reducing agent|redox|'
                     r'electroly\w*|electrode|anode|cathode|half[- ]equation|'
                     r'electrochemical|galvanic|voltaic|electron transfer)\b'),
    # ── Strand 2: bonding and organic ──────────────────────────────────────
    ('chem-2-4', 10, r'\b(alkane|alkene|alkyne|ethene|ethyne|benzene|aromatic|'
                     r'hydrocarbon|isomer|homologous series|structural formula|'
                     r'addition reaction|substitution reaction|polymer|'
                     r'crude oil|octane number|cracking|reforming|petrol)\b'),
    ('chem-2-2', 10, r'\b(intermolecular|van der waals|hydrogen bond|dipole|'
                     r'molecular shape|bond angle|electronegativit\w*|'
                     r'polar (?:molecule|bond)|london dispersion|tetrahedral|'
                     r'linear|trigonal)\b'),
    ('chem-2-1', 9, r'\b(covalent|ionic bond|metallic bond|dot and cross|'
                    r'lone pair|bond pair|octet|valenc\w*|lewis|'
                    r'sigma bond|pi bond|double bond|triple bond)\b'),
    ('chem-2-3', 10, r'\b(boyle|charles|gay[- ]lussac|avogadro|ideal gas|'
                     r'kinetic theory|gas law|molar volume|\bstp\b|\bs\.t\.p)\b'),
    # ── Strand 1: matter and the atom ──────────────────────────────────────
    ('chem-1-2', 10, r'\b(atomic (?:number|structure|orbital)|electron configuration|'
                     r'isotop\w*|mass number|orbital|sub[- ]?level|'
                     r'quantum|heisenberg|energy level|emission spectr\w*|'
                     r'flame test|bohr|rutherford|radioactiv\w*|nuclear equation|'
                     r'alpha particle|beta particle|half[- ]life)\b'),
    ('chem-1-3', 10, r'\b(periodic table|periodic trend|group \d|period \d|'
                     r'atomic radius|ionisation energy|electronegativity trend|'
                     r'mendeleev|transition (?:metal|element)|noble gas|'
                     r'alkali metal|halogen)\b'),
    ('chem-1-4', 10, r'\b(mole[s]?\b|molar mass|relative (?:atomic|molecular) mass|'
                     r'avogadro constant|empirical formula|percentage by mass|'
                     r'balanced equation|stoichiometr\w*|concentration in|'
                     r'grams per|mol l|\bm solution)\b'),
    ('chem-1-1', 8, r'\b(state of matter|solid|liquid|gas\b|solution|solvent|solute|'
                    r'mixture|compound|element\b|physical change|chemical change|'
                    r'solubilit\w*|filtrat\w*|evaporat\w*)\b'),
    # ── The unifying strands, weakest: they describe HOW, not WHAT ─────────
    ('chem-u2', 5, r'\b(apparatus|safety|hazard|precaution|why is it (?:necessary|important)|'
                   r'describe how|state one use|rins\w+|source of error|'
                   r'accura\w*|experiment\w*)\b'),
    ('chem-u3', 5, r'\b(industrial|manufactur\w*|environment\w*|everyday|'
                   r'renewable|sustainab\w*|society|medicine|food)\b'),
]
COMPILED = [(t, w, re.compile(p, re.I)) for t, w, p in RULES]


def topic_for(text):
    """(topic id, the phrase that decided it) — or (None, None)."""
    best = (0, None, None)
    for tid, weight, rx in COMPILED:
        m = rx.search(text or '')
        if m and weight > best[0]:
            best = (weight, tid, m.group(0))
    return best[1], best[2]


def concept_for(text, fallback='part'):
    """A slug for the card's concept, from the ask's own first words."""
    words = re.findall(r"[a-z0-9']+", (text or '').lower())
    stop = {'the', 'a', 'an', 'of', 'in', 'to', 'and', 'for', 'is', 'are', 'was',
            'were', 'this', 'that', 'with', 'from', 'by', 'on', 'at', 'as', 'it'}
    keep = [w for w in words if w not in stop][:6]
    return '-'.join(keep) or fallback


def main():
    """Score the rules against the topics already assigned by hand."""
    path = os.path.join(ROOT, 'scripts/markbank/authored/chemistry.json')
    cards = json.load(open(path))
    agree = disagree = silent = 0
    wrong = collections.Counter()
    misses = []
    for c in cards:
        text = ' '.join(filter(None, [c.get('questionText'), c.get('stem')]))
        got, _ = topic_for(text)
        want = c.get('topicId')
        if got is None:
            silent += 1
            if len(misses) < 12:
                misses.append((want, text[:88]))
        elif got == want:
            agree += 1
        else:
            disagree += 1
            wrong[(want, got)] += 1
    total = agree + disagree + silent
    print(f'{total} cards with a hand-assigned topic')
    print(f'   agree    {agree:4} ({100 * agree // max(total, 1)}%)')
    print(f'   disagree {disagree:4}')
    print(f'   silent   {silent:4}  (reported, never guessed)')
    print('\nmost common disagreements (hand -> rule):')
    for (want, got), n in wrong.most_common(12):
        print(f'   {n:4}  {want} -> {got}')
    print('\nunmatched samples:')
    for want, text in misses:
        print(f'   [{want}] {text}')


if __name__ == '__main__':
    sys.exit(main())
