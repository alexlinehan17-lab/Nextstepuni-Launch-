#!/usr/bin/env python3
"""Close the Physics paper-census gaps from the published papers and schemes.

The 2016--2019 Higher papers price their experimental and long questions at
the whole-question boundary, while their two short-question menus price each
letter separately.  The 2020 paper prints smaller tariff runs.  Later papers
mostly print one roman-major task per scheme boundary.  This generator keeps
those distinctions: it groups only at a printed boundary, lifts the complete
question wording from the paper reader, joins that wording back to the scheme,
and leaves row marks blank where the scheme gives only a common total.

It owns only the ids in physics-completion-ids.json.  Existing reviewed cards
remain byte-for-byte untouched by physics_all.py.
"""
from __future__ import annotations

import json
import os
import re
import subprocess
import sys
import unicodedata
from collections import defaultdict

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import paper as paper_reader  # noqa: E402
import mathtext  # noqa: E402
from paper import Paper, unligature  # noqa: E402
from paper_census import (  # noqa: E402
    ROMANS, census_merged, census_subject, key_label, leaves_of,
)
from reconcile import reconcile_subject  # noqa: E402


DIR = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(DIR)))
TARGETS_PATH = os.path.join(
    ROOT, 'scripts', 'markbank', 'authored', 'physics-completion-targets.json')
VERIFY = os.path.join(DIR, 'verify-claims.mjs')

TOKEN = re.compile(r"[^\W_]+(?:['’][^\W_]+)?", re.UNICODE)
PAPER_MARK = re.compile(r'\((\d{1,2})\s*(?:marks?)?\)', re.I)
MARK_TOKEN = re.compile(
    r'⟨\s*\(?\s*([^⟩]*?\d[^⟩]*?)\s*\)?\s*⟩'
    r'|\[\s*([^\]]*?\d[^\]]*?)\s*\]')
TRAILING_TARIFF = re.compile(
    r'\s+(?:\(?\d{1,2}\s*(?:or|\/|\+|[x×])\s*\d{1,2}'
    r'(?:\s*[+x×]\s*\d{1,2})*\)?|\d{1,2}\s+or\s+\d{1,2})\s*$')
PAGE = re.compile(
    r'^(?:##\s*Page|Page\s+\d+|page\s+\d+\s+of\s+\d+|Leaving Certificate|'
    r'Physics\s*[–-]\s*(?:Higher|Ordinary)|Marking Scheme|SECTION\s+[AB]|'
    r'Answer (?:any|three|five)|Blank Page|Copyright notice|Acknowledgements)',
    re.I)
QUESTIONISH = re.compile(
    r'^(?:\([a-zivx]+\)\s*)?(?:what|why|how|when|where|which|who|name|state|'
    r'give|list|define|explain|describe|identify|suggest|outline|calculate|'
    r'draw|sketch|compare|distinguish|account|match|complete|write|find|show|'
    r'determine|derive|verify|copy|plot|use|indicate|select|choose)\b', re.I)
GRADING = re.compile(
    r'^(?:partial answer|accept partial|one line|two lines|three lines|four lines|'
    r'one correct|two correct|correct (?:shape|direction|answer|arrangement)|'
    r'any (?:one|two|three|four)|marks? may be|note:|deduct|award|maximum mark|'
    r'no labels?|incorrect arrangement|other valid|e\.g\.\s*$)', re.I)
CONTENT_FREE = re.compile(
    r'^(?:apparatus|method|observation|conclusion|diagram|labelled diagram|'
    r'formula|substitution|answer|reason|explanation|calculation|value|unit|'
    r'correct answer|relevant detail|partial answer)[\s,;/&-]*$', re.I)
MARK_ONLY = re.compile(
    r'^[\[\]⟨⟩()\d\s+x×:;,.\-/]*(?:marks?)?[\[\]⟨⟩()\d\s+x×:;,.\-/]*$',
    re.I)
FURNITURE_CUT = re.compile(
    r'\b(?:SECTION\s+[AB]\s*\(|Leaving Certificate(?: Examination)?[–,—\s]|'
    r'Blank Page|Acknowledgements|Copyright notice|This document will not be returned)\b',
    re.I)
DOUBLED_MATHS_DIGIT = re.compile(
    r'([\U0001D7CE-\U0001D7FF])\1')
DOUBLED_MATHS_LETTER = re.compile(
    r'([\U0001D400-\U0001D7CD])\1')
# Symbol-font code points whose meaning is fixed by the Physics wording.  One
# of these (U+F06C) is a Wingdings bullet in another subject, so it cannot be a
# global character-only glyph-map entry; the subject context is essential.
PHYSICS_GLYPHS = str.maketrans({
    '\uf066': '\u03b8',  # "the angle ..., theta"
    '\uf06c': '\u03bb',  # wavelength / decay constant
    '\uf06d': '\u03bc',  # microfarad/microamp or linear density mu
})

# Rows checked directly against the rendered SEC scheme pages where the normal
# extractor cannot produce a safe line.  Equation rows are also copied into a
# named verified-visual-maths appendix in the corresponding scheme markdown,
# so the ordinary provenance gate still proves every student-facing claim.
MANUAL_ROWS = {
    (2016, 'ol', 10, None, 'ii'): [
        'A: cathode', 'B: anode', 'C: screen',
    ],
    (2016, 'ol', 10, None, 'iii'): [
        'cathode emits electrons / particles',
        'anode attracts / focuses / accelerates electrons',
        'screen lights up / shows the presence of electrons',
    ],
    (2016, 'ol', 4, None, 'iii'): [
        'I2 (A2) 1 2.25 4 6.25 9 12.25 16',
    ],
    (2017, 'ol', 3, None, 'iv'): [
        '1/f = 1/u + 1/v',
        'f1 = 10 cm; f2 = 10.12 cm; f3 = 10.086 cm',
        'average focal length = 10.07 cm',
    ],
    (2017, 'ol', 5, 'j', None): [
        'Geiger-Muller tube', 'Geiger counter', 'solid state detector',
        'cloud chamber', 'bubble chamber', 'GLE', 'photographic film',
        'radiometer', 'radiation sensor',
    ],
    (2017, 'ol', 7, None, 'iii'): [
        'two mirrors / prisms facing each other', 'mirrors at 45°',
        'correct ray path (in either direction)', 'tubing',
    ],
    (2017, 'ol', 12, 'a', 'iv'): ['70 s'],
    (2017, 'ol', 11, 'f', None): [
        'A – neutral; B – live; C – earth',
    ],

    (2018, 'hl', 5, 'b', None): ['M = Fd', 'x = 6.25 N'],
    (2018, 'hl', 5, 'd', None): [
        'f′ = fc / (c − u)', 'f′ = (2300)(340) / (340 − 30)',
        'f′ = 2523 Hz',
    ],
    (2018, 'hl', 5, 'e', None): [
        'n = c/v', '2.4 = (3 × 10^8)/v', 'v = 1.25 × 10^8 m s−1',
    ],
    (2018, 'hl', 5, 'g', None): ['E = Q/(4πεd²)'],
    (2018, 'hl', 10, 'a', None): [
        'neutrino', 'had the missing energy and momentum',
        '¹₀n → ¹₁H + ⁰₋₁e + ν', 'no charge', 'very small mass',
        '⁰₋₁e + ⁰₁e → 2γ', 'to conserve momentum',
        'since particle and antiparticle have equal and opposite charges, charge before = 0',
        'photons have no charge', 'E = mc²', 'E = hf', 'hf = mc²',
        'f = 1.24 × 10^20 Hz', 'muon, tau',
        'electromagnetic, weak, gravitational', 'in correct order',
    ],
    (2018, 'hl', 10, 'b', None): [
        'axes labelled for at least one graph', 'correct shape for a.c.',
        'correct shape for d.c.', 'diode',
        'correct arrangement including input and output voltages',
        'correct shape', 'coil and d.c. power supply in primary circuit',
        'coil with more turns in secondary circuit',
        'labelled make and break mechanism and iron core',
        'primary coil switches off',
        'changing magnetic field cutting the secondary coil',
        'emf induced in secondary coil', 'transformer',
        'a.c. input and primary coil', 'secondary coil and output',
        'both coils on common iron core',
        'current in primary coil always changing',
        'changing magnetic field from primary coil cutting the secondary coil',
        'induced emf is larger due to greater number of turns in secondary coil',
    ],
    (2018, 'hl', 11, 'a', None): [
        'λ = 30 m', 'v = fλ', 'f = 1 × 10^7 Hz',
    ],
    (2018, 'hl', 11, 'b', None): [
        'correct shape of field lines around the Earth',
        'correct direction of field lines',
    ],
    (2018, 'hl', 11, 'g', None): [
        'v = 2πr/T', 'v = 7650 m s−1',
    ],

    (2018, 'ol', 5, 'c', 'i'): ['joulemeter', 'ohmmeter'],
    (2018, 'ol', 5, 'f', None): ['C = q/V'],
    (2018, 'ol', 6, None, 'iv'): [
        '½mv² = ½(500)(6)² = 9000 J', '½mv² = ½(300)(0)² = 0 J',
    ],
    (2018, 'ol', 7, None, 'viii'): [
        'ensure that there is only one independent variable',
        'ensure there is an equal amount of heat for each metal',
        'ensure that the metal strips are the same length / diameter',
        'ensure to have the same amount of wax',
    ],
    (2018, 'ol', 12, 'a', 'i'): [
        'displacement per second', 'change in velocity per unit time',
    ],

    (2019, 'hl', 5, 'a', None): [
        's = vt', 's = (3.00 × 10^8)(3.15 × 10^7)',
        's = 9.45 × 10^15 m',
    ],
    (2019, 'hl', 5, 'i', None): ['²²²₈₆Rn → ²¹⁸₈₄Po + ⁴₂He'],
    (2019, 'hl', 11, 'd', None): [
        'F = Δ(mv)/Δt', 'F = ((0.11)(4) − (0.11)(−4))/0.2',
        'F = 4.4 N',
    ],

    (2019, 'ol', 4, None, 'vi'): [
        'ρ = RA/l', 'ρ = ((22.8)(4.9 × 10−8))/0.98 = 1.14 × 10−6 Ω m',
    ],
    (2019, 'ol', 5, 'b', None): ['2.5 m s‐2'],
    (2019, 'ol', 5, 'e', None): ['1400 W'],
    (2019, 'ol', 9, 'b', 'i'): ['2.2 Ω'],
    (2019, 'ol', 9, 'c', 'i'): ['earth'],
    (2019, 'ol', 9, 'c', 'ii'): ['live'],
    (2019, 'ol', 10, None, 'i'): [
        '(negative) charge', 'small mass', 'orbits outside nucleus',
        'deflected by electric/magnetic fields',
    ],
    (2019, 'ol', 12, 'a', 'iv'): [
        'KE = 8750 = mgh = (7)(9.8)h',
        'v² = u² + 2as = (50)² + 2(−9.8)s', 'h = 127.55 m',
    ],
    (2019, 'ol', 12, 'd', 'i'): ['92 protons', '146 neutrons'],
    (2019, 'ol', 12, 'd', 'ii'): [
        'atoms with the same atomic number and with different mass numbers',
    ],

    (2020, 'ol', 5, 'c', None): ['farad'],
    (2020, 'ol', 12, 'd', None): [
        'gamma', 'radioactive sources', 'barriers', 'detector/GM tube',
        'place different barriers between the sources and the detector',
        'alpha is stopped first', 'gamma penetrates best',
    ],
    (2020, 'ol', 12, 'd', 'vi'): [
        '84', '216', 'Polonium / Po', 'sterilise food',
        'sterilise medical equipment', 'cancer therapy', 'energy source',
    ],

    (2021, 'hl', 7, None, 'ix'): [
        'downward arrow, labelled as weight',
        'labelled tension arrow in correct direction',
    ],
    (2021, 'ol', 9, None, 'vi'): ['R= 1.05 Ω'],
    (2021, 'ol', 9, None, 'vii'): ['RT = 3 + 1.05 = 4.05 Ω'],
    (2021, 'ol', 11, None, 'vii'): ['54 m2'],

    (2023, 'ol', 3, None, 'i'): ['thermometer', 'lagging/insulation'],
    (2024, 'ol', 10, None, 'iii'): ['X = antinode', 'Y = node'],

    (2025, 'hl', 8, None, 'v'): [
        'nλ = d sin θ', 'θ = 24.5°', 'number of lines/mm = 300',
    ],
    (2025, 'hl', 11, None, 'ii'): [
        'Itot = I1 + I2', 'I = V/R', '1/Rtot = 1/R1 + 1/R2',
    ],
    (2025, 'hl', 11, None, 'iii'): [
        'Rparallel = 2.67 (Ω)', 'Rcircuit = 10.67 Ω',
    ],
    (2025, 'hl', 11, None, 'iv'): [
        'I = ( V/R = 12/10.67 ) =1.125 (A)',
        'VXY = ( R × I = 2.67 x 1.125 ) = 3 V',
    ],
    (2025, 'hl', 11, None, 'v'): ['potential difference increases'],
    (2025, 'hl', 11, None, 'vii'): [
        'R2/R1 = V2/V1', 'R2 = 5000( 8/4 )', 'R2 = 10000 Ω',
    ],

    (2025, 'ol', 7, None, 'ix'): ['positive slope'],
    (2025, 'ol', 7, None, 'x'): ['it is constant'],
    (2025, 'ol', 7, None, 'xi'): ['C'],
    (2025, 'ol', 7, None, 'xii'): ['as they have a small velocity'],
    (2025, 'ol', 14, 'c', 'i'): ['gold / leaf'],
}

MANUAL_TOTALS = {
    (2016, 'ol', 10, None, 'ii'): 9,
    (2016, 'ol', 10, None, 'iii'): 9,
    (2016, 'ol', 4, None, 'iii'): 6,
    (2017, 'ol', 3, None, 'iv'): 12,
    (2017, 'ol', 5, 'j', None): 7,
    (2017, 'ol', 7, None, 'iii'): 9,
    (2017, 'ol', 12, 'a', 'iv'): 6,
    (2017, 'ol', 11, 'f', None): 7,
    **{(2018, 'hl', 5, part, None): 7 for part in ('b', 'd', 'e', 'g')},
    (2018, 'hl', 10, 'a', None): 56,
    (2018, 'hl', 10, 'b', None): 56,
    **{(2018, 'hl', 11, part, None): 7 for part in ('a', 'b', 'g')},
    (2018, 'ol', 5, 'c', 'i'): 7,
    (2018, 'ol', 5, 'f', None): 7,
    (2018, 'ol', 6, None, 'iv'): 9,
    (2018, 'ol', 7, None, 'viii'): 8,
    (2018, 'ol', 12, 'a', 'i'): 10,
    (2019, 'hl', 5, 'a', None): 7,
    (2019, 'hl', 5, 'i', None): 7,
    (2019, 'hl', 11, 'd', None): 7,
    (2019, 'ol', 4, None, 'vi'): 10,
    (2019, 'ol', 5, 'b', None): 7,
    (2019, 'ol', 5, 'e', None): 7,
    (2019, 'ol', 9, 'b', 'i'): 6,
    (2019, 'ol', 9, 'c', 'i'): 6,
    (2019, 'ol', 9, 'c', 'ii'): 6,
    (2019, 'ol', 10, None, 'i'): 6,
    (2019, 'ol', 12, 'a', 'iv'): 6,
    (2019, 'ol', 12, 'd', 'i'): 8,
    (2019, 'ol', 12, 'd', 'ii'): 6,
    (2020, 'ol', 5, 'c', None): 7,
    (2020, 'ol', 12, 'd', None): 15,
    (2020, 'ol', 12, 'd', 'vi'): 13,
    (2021, 'hl', 7, None, 'ix'): 6,
    (2021, 'ol', 9, None, 'vi'): 6,
    (2021, 'ol', 9, None, 'vii'): 6,
    (2021, 'ol', 11, None, 'vii'): 4,
    (2023, 'ol', 3, None, 'i'): 6,
    (2024, 'ol', 10, None, 'iii'): 6,
    (2025, 'hl', 8, None, 'v'): 12,
    (2025, 'hl', 11, None, 'ii'): 9,
    (2025, 'hl', 11, None, 'iii'): 6,
    (2025, 'hl', 11, None, 'iv'): 6,
    (2025, 'hl', 11, None, 'v'): 4,
    (2025, 'hl', 11, None, 'vii'): 9,
    (2025, 'ol', 7, None, 'ix'): 6,
    (2025, 'ol', 7, None, 'x'): 5,
    (2025, 'ol', 7, None, 'xi'): 3,
    (2025, 'ol', 7, None, 'xii'): 3,
    (2025, 'ol', 14, 'c', 'i'): 6,
}

MANUAL_QUESTIONS = {
    (2017, 'ol', 5, 'j', None): 'Name one method of detecting radiation?',
    (2018, 'hl', 10, 'a', None): (
        '(a) Momentum, energy and charge are conserved in all nuclear reactions. '
        'In beta‐decay an unstable nucleus emits an electron. In the early 20th '
        'century it was found that momentum and energy did not appear to be '
        'conserved during beta‐decay. To solve this apparent problem, Wolfgang '
        'Pauli predicted the existence of an unknown particle, about which he '
        'said: I have done a terrible thing. I have postulated a particle that '
        'cannot be detected. Name the particle which Pauli predicted and explain '
        'how it solved the problem. Write a nuclear equation for beta‐decay. Why '
        'did Pauli think that the particle could not be detected? (21) The '
        'conservation laws also apply to pair annihilation. Pair annihilation can '
        'be described using the following equation for an electron and a positron '
        'at rest: ⁰₋₁e + ⁰₁e → 2γ. Why are two gamma‐ray photons produced? Explain '
        'how charge is conserved in the annihilation. Calculate the maximum '
        'frequency of each emitted photon. (23) Electrons are negatively charged '
        'leptons. List the two other negatively charged leptons. List the three '
        'forces that these leptons can experience, in decreasing order of '
        'strength. (12)'),
    (2018, 'ol', 5, 'c', 'i'):
        'Choose from the list below the instrument used to measure (i) energy and (ii) resistance. barometer joulemeter lens ohmmeter',
    (2018, 'ol', 12, 'a', 'i'):
        'Define (i) velocity and (ii) acceleration. (10)',
    (2019, 'ol', 4, None, 'vi'):
        'Use the formula ρ = RA/l to calculate the resistivity of the wire. (10)',
    (2019, 'ol', 12, 'd', 'i'):
        '²³⁸₉₂U is a uranium atom. How many protons are in this uranium atom? How many neutrons are in this uranium atom? (8)',
    (2019, 'ol', 12, 'd', 'ii'):
        '²³⁵₉₂U is another isotope of uranium. What are isotopes? (6)',
    (2020, 'ol', 5, 'c', None):
        'Which of the following is the SI unit of capacitance? ampere coulomb farad volt',
    (2020, 'ol', 12, 'd', None):
        'Which type of radiation is the most penetrating? Describe an experiment to compare the penetrating power of alpha, beta and gamma radiation. (15)',
    (2020, 'ol', 12, 'd', 'vi'):
        'The nuclear equation ²²⁰₈₆Rn → ²¹⁶₈₄X + ⁴₂α shows alpha decay. Calculate the atomic number and mass number of X, name X, and state one use of nuclear radiation. (13)',
    (2025, 'ol', 7, None, 'xii'):
        'Why is it safe for the skydiver to land after D?',
}

# Replace flattened diagram-label soup only where the inspected paper crop now
# carries the layout.  The question wording itself already supplies the force
# names, so no prose stem is needed on these cards.
MANUAL_STEMS = {
    (2022, 'ol', 14, 'c', 'i'): '',
    (2022, 'ol', 14, 'c', 'ii'): '',
    (2022, 'ol', 14, 'c', 'iv'): '',
}

MANUAL_REFS = {
    (2018, 'ol', 12, 'a', 'i'): 'Q12(a)(i), (ii)',
    (2020, 'ol', 12, 'd', None): 'Q12(d)(i)–(ii)',
    (2020, 'ol', 12, 'd', 'vi'): 'Q12(d)(iii)–(vi)',
    (2023, 'ol', 3, None, 'i'): 'Q3(i), (ii)',
}

QUESTION_FIGURES = {
    (2016, 'hl', 1, None, None):
        'physics-2016-HL-paper-p02-art-q1-meter-stick',
    (2016, 'hl', 10, None, None):
        'physics-2016-HL-paper-p08-art-q10-circuit',
    **{
        (2016, 'ol', 4, None, roman):
            'physics-2016-OL-paper-p03-art-q4-table'
        for roman in ('iii', 'iv', 'v')
    },
    **{
        (2016, 'ol', 8, None, roman):
            'physics-2016-OL-paper-p06-art-q8-circuit'
        for roman in ('i', 'ii', 'iii')
    },
    (2016, 'ol', 10, None, 'ii'):
        'physics-2016-OL-paper-p07-art-q10-crt',
    (2016, 'ol', 10, None, 'iii'):
        'physics-2016-OL-paper-p07-art-q10-crt',
    **{
        (2016, 'ol', 10, None, roman):
            'physics-2016-OL-paper-p07-art-q10-crt'
        for roman in ('i', 'iv', 'v', 'vi')
    },
    (2016, 'ol', 12, 'b', 'i'):
        'physics-2016-OL-paper-p09-art-q12-magnet',
    (2017, 'hl', 12, 'a', None):
        'physics-2017-HL-paper-p10-art-q12-sign',
    (2017, 'ol', 5, 'b', None):
        'physics-2017-OL-paper-p04-art-q5b-handle',
    (2017, 'ol', 5, 'e', None):
        'physics-2017-OL-paper-p04-art-q5e-micrometer',
    (2017, 'ol', 11, 'f', None):
        'physics-2017-OL-paper-p09-art-q11-plug',
    **{
        (2017, 'ol', 12, 'd', roman):
            'physics-2017-OL-paper-p11-art-q12d-capacitor'
        for roman in ('ii', 'iii')
    },
    (2018, 'ol', 5, 'b', None):
        'physics-2018-OL-paper-p04-art-q5b-refraction',
    (2018, 'ol', 5, 'e', None):
        'physics-2018-OL-paper-p04-art-q5e-instrument',
    **{
        (2018, 'ol', 10, None, roman):
            'physics-2018-OL-paper-p08-art-q10-xray'
        for roman in ('i', 'ii', 'iii', 'iv', 'v', 'vi', 'vii', 'viii', 'ix')
    },
    (2018, 'ol', 11, 'h', None):
        'physics-2018-OL-paper-p09-art-q11-surfer',
    (2018, 'ol', 12, 'd', 'ii'):
        'physics-2018-OL-paper-p11-art-q12d-induction',
    (2019, 'ol', 9, 'c', 'i'):
        'physics-2019-OL-paper-p07-art-q9-plug',
    (2019, 'ol', 9, 'c', 'ii'):
        'physics-2019-OL-paper-p07-art-q9-plug',
    (2019, 'ol', 1, None, 'iv'):
        'physics-2019-OL-paper-p02-art-q1-meter-stick',
    (2019, 'ol', 10, None, 'vii'):
        'physics-2019-OL-paper-p08-art-q10-xray-photo',
    (2019, 'ol', 11, 'f', None):
        'physics-2019-OL-paper-p09-art-q11-ray',
    (2019, 'ol', 12, 'b', 'iv'):
        'physics-2019-OL-paper-p10-art-q12b-capacitor',
    (2020, 'hl', 5, 'i', None):
        'physics-2020-HL-paper-p04-art-q5i-photocell',
    (2020, 'ol', 6, None, None):
        'physics-2020-OL-paper-p05-art-q6-forces',
    (2020, 'ol', 12, 'c', 'v'):
        'physics-2020-OL-paper-p10-art-q12c-circuit',
    (2022, 'hl', 9, 'c', 'ii'):
        'physics-2022-HL-paper-p08-art-q9c-circuit',
    **{
        (2022, 'ol', 14, 'c', roman):
            'physics-2022-OL-paper-p14-art-q14c-meter-stick'
        for roman in ('i', 'ii', 'iv')
    },
    (2023, 'ol', 3, None, 'i'):
        'physics-2023-OL-paper-p03-art-q3-calorimeter',
    **{
        (2023, 'ol', 8, None, roman):
            'physics-2023-OL-paper-p07-art-q8-glass-block'
        for roman in ('ii', 'iii')
    },
    (2024, 'hl', 6, 'a', None):
        'physics-2024-HL-paper-p05-art-q6a-meter-stick',
    (2024, 'ol', 10, None, 'iii'):
        'physics-2024-OL-paper-p09-art-q10-stationary-wave',
    **{
        (2025, 'ol', 7, None, roman):
            'physics-2025-OL-paper-p07-art-q7-skydiver-graph'
        for roman in ('ix', 'x', 'xi', 'xii')
    },
    (2025, 'ol', 14, 'c', 'i'):
        'physics-2025-OL-paper-p15-art-q14-electroscope',
    (2025, 'hl', 11, None, 'ii'):
        'physics-2025-HL-paper-p13-art-q11ii-parallel',
    **{
        (2025, 'hl', 11, None, roman):
            'physics-2025-HL-paper-p13-art-q11iii-circuit'
        for roman in ('iii', 'iv', 'v')
    },
    (2025, 'hl', 11, None, 'vii'):
        'physics-2025-HL-paper-p13-art-q11vii-divider',
    (2025, 'hl', 13, None, 'vii'):
        'physics-2025-HL-paper-p16-art-q13vii-current-graph',
}

QUESTION_LABEL_KEYS = {
    **{
        (2016, 'ol', 8, None, roman): [
            {'letter': 'A', 'meaning': 'ammeter symbol',
             'askedInThisQuestion': roman in ('ii', 'iii')},
        ]
        for roman in ('i', 'ii', 'iii')
    },
    (2016, 'ol', 10, None, 'ii'): [
        {'letter': 'A', 'meaning': 'cathode', 'askedInThisQuestion': True},
        {'letter': 'B', 'meaning': 'anode', 'askedInThisQuestion': True},
        {'letter': 'C', 'meaning': 'screen', 'askedInThisQuestion': True},
    ],
    (2016, 'ol', 10, None, 'iii'): [
        {'letter': 'A', 'meaning': 'cathode', 'askedInThisQuestion': True},
        {'letter': 'B', 'meaning': 'anode', 'askedInThisQuestion': True},
        {'letter': 'C', 'meaning': 'screen', 'askedInThisQuestion': True},
    ],
    (2017, 'ol', 11, 'f', None): [
        {'letter': 'A', 'meaning': 'neutral pin', 'askedInThisQuestion': True},
        {'letter': 'B', 'meaning': 'live pin', 'askedInThisQuestion': True},
        {'letter': 'C', 'meaning': 'earth pin', 'askedInThisQuestion': True},
    ],
    (2017, 'hl', 12, 'a', None): [
        {'letter': 'X', 'meaning': "the rod's wall contact and moment pivot",
         'askedInThisQuestion': True},
    ],
    **{
        (2018, 'ol', 10, None, roman): [
            {'letter': 'A',
             'meaning': 'heated filament or cathode where thermionic emission occurs',
             'askedInThisQuestion': roman == 'ii'},
            {'letter': 'B', 'meaning': 'metal target or anode',
             'askedInThisQuestion': roman == 'iii'},
            {'letter': 'C', 'meaning': 'lead casing that prevents X-rays escaping',
             'askedInThisQuestion': roman == 'iv'},
        ]
        for roman in ('i', 'ii', 'iii', 'iv', 'v', 'vi', 'vii', 'viii', 'ix')
    },
    (2019, 'ol', 9, 'c', 'i'): [
        {'letter': 'A', 'meaning': 'earth wire', 'askedInThisQuestion': True},
        {'letter': 'B', 'meaning': 'live wire', 'askedInThisQuestion': False},
    ],
    (2019, 'ol', 9, 'c', 'ii'): [
        {'letter': 'A', 'meaning': 'earth wire', 'askedInThisQuestion': False},
        {'letter': 'B', 'meaning': 'live wire', 'askedInThisQuestion': True},
    ],
    (2023, 'ol', 3, None, 'i'): [
        {'letter': 'A', 'meaning': 'thermometer', 'askedInThisQuestion': True},
        {'letter': 'B', 'meaning': 'lagging or insulation', 'askedInThisQuestion': True},
    ],
    (2022, 'hl', 9, 'c', 'ii'): [
        {'letter': 'X', 'meaning': 'the 1 ohm series resistor',
         'askedInThisQuestion': True},
        {'letter': 'Y', 'meaning': 'the 6 ohm parallel-branch resistor',
         'askedInThisQuestion': True},
        {'letter': 'Z', 'meaning': 'the 3 ohm parallel-branch resistor',
         'askedInThisQuestion': False},
    ],
    (2023, 'ol', 8, None, 'ii'): [
        {'letter': 'A', 'meaning': 'incident ray', 'askedInThisQuestion': True},
        {'letter': 'B', 'meaning': 'refracted ray', 'askedInThisQuestion': True},
        {'letter': 'C', 'meaning': 'normal', 'askedInThisQuestion': True},
    ],
    (2023, 'ol', 8, None, 'iii'): [
        {'letter': 'A', 'meaning': 'incident ray', 'askedInThisQuestion': False},
        {'letter': 'B', 'meaning': 'refracted ray', 'askedInThisQuestion': False},
        {'letter': 'C', 'meaning': 'normal', 'askedInThisQuestion': False},
    ],
    (2024, 'ol', 10, None, 'iii'): [
        {'letter': 'X', 'meaning': 'antinode', 'askedInThisQuestion': True},
        {'letter': 'Y', 'meaning': 'node', 'askedInThisQuestion': True},
    ],
    **{
        (2025, 'ol', 7, None, roman): [
            {'letter': 'A', 'meaning': 'start of the plotted fall',
             'askedInThisQuestion': roman == 'ix'},
            {'letter': 'B', 'meaning': 'start of the first constant-velocity interval',
             'askedInThisQuestion': roman in ('ix', 'x')},
            {'letter': 'C', 'meaning': 'the skydiver opens the parachute',
             'askedInThisQuestion': roman in ('x', 'xi')},
            {'letter': 'D', 'meaning': 'start of the low landing-velocity interval',
             'askedInThisQuestion': roman == 'xii'},
        ]
        for roman in ('ix', 'x', 'xi', 'xii')
    },
    (2025, 'ol', 14, 'c', 'i'): [
        {'letter': 'X', 'meaning': 'gold leaf', 'askedInThisQuestion': True},
    ],
    (2025, 'hl', 11, None, 'ii'): [
        {'letter': 'R1', 'meaning': 'upper parallel-branch resistor',
         'askedInThisQuestion': True},
        {'letter': 'R2', 'meaning': 'lower parallel-branch resistor',
         'askedInThisQuestion': True},
    ],
    **{
        (2025, 'hl', 11, None, roman): [
            {'letter': 'X', 'meaning': 'upper potential-difference junction',
             'askedInThisQuestion': roman in ('iv', 'v')},
            {'letter': 'Y', 'meaning': 'lower potential-difference junction',
             'askedInThisQuestion': roman in ('iv', 'v')},
        ]
        for roman in ('iii', 'iv', 'v')
    },
    (2025, 'hl', 11, None, 'vii'): [
        {'letter': 'Vout', 'meaning': 'output potential difference',
         'askedInThisQuestion': True},
    ],
}

# An inspected figure card already covers each of these initial completion
# targets.  Re-emitting a figureless duplicate only creates a deliberate
# supersession drop; keep the reviewed winner and generate nothing here.
SKIP_LEAVES = {
    (2020, 'ol', 8, None, 'i'),
    (2021, 'ol', 11, None, 'vii'),
    (2021, 'hl', 13, 'a', 'v'),
    (2022, 'ol', 3, None, 'i'), (2022, 'ol', 3, None, 'ii'),
    (2022, 'ol', 3, None, 'vii'), (2022, 'ol', 3, None, 'viii'),
}


def fold(text: str) -> str:
    return unicodedata.normalize('NFKD', text).encode(
        'ascii', 'ignore').decode().casefold()


def token_offsets(text: str):
    return [(fold(m.group()), m.start(), m.end()) for m in TOKEN.finditer(text)
            if fold(m.group())]


def natural(key):
    q, letter, roman = key
    return (q, letter or '', ROMANS.index(roman) if roman in ROMANS else 99)


def clean_paper_text(text):
    text = unligature(text or '')
    text = text.translate(PHYSICS_GLYPHS)
    text = FURNITURE_CUT.split(text, maxsplit=1)[0]
    text = re.sub(r'\bpage\s+\d+\s+of\s+\d+\b', ' ', text, flags=re.I)
    text = re.sub(r'_{3,}', ' ', text)
    return ' '.join(text.split()).strip()


def key_suffix(key):
    q, letter, roman = key
    return f'q{q}' + (letter or '') + (f'-{roman}' if roman else '')


def refresh_targets():
    census = census_subject('physics')
    audit = reconcile_subject('physics', census)
    payload = {
        'paperLeafCount': audit['leaves'],
        'targetCount': audit['open'],
        'censusCounts': {
            f"{p['year']}-{p['level']}": p['leafCount']
            for p in census['papers']
        },
        'targets': [
            {'year': p['year'], 'level': p['level'], 'label': label}
            for p in audit['papers'] for label in p['open']
        ],
    }
    with open(TARGETS_PATH, 'w', encoding='utf-8') as fh:
        json.dump(payload, fh, ensure_ascii=False, indent=1)
        fh.write('\n')
    print(f'wrote {TARGETS_PATH}', file=sys.stderr)


def load_targets():
    payload = json.load(open(TARGETS_PATH, encoding='utf-8'))
    out = defaultdict(set)
    for row in payload['targets']:
        out[(row['year'], row['level'])].add(row['label'])
    if sum(map(len, out.values())) != payload['targetCount']:
        raise AssertionError('Physics completion target count is stale')
    return payload, out


def printed_total(text):
    values = [int(v) for v in PAPER_MARK.findall(text or '')
              if 0 < int(v) <= 80]
    return values[-1] if values else None


def boundary_for_legacy_hl(key):
    q, letter, _ = key
    if q in (1, 2, 3, 4, 6, 7, 8, 9, 10):
        return (q, None, None)
    if q == 12:
        return (q, letter, None)
    return key


def groups_for(year, level, leaves, texts):
    """[(published boundary, [census leaves])], in paper order."""
    leaves = sorted(leaves, key=natural)
    if level == 'hl' and year <= 2019:
        grouped = defaultdict(list)
        order = []
        for key in leaves:
            # The 2018 Q10 instruction is "Answer either part (a) or part
            # (b)" and each route carries the full 56 marks.  They are finite
            # selectable routes, so publish one card per route rather than a
            # single card that asks the student to answer both.
            boundary = key if year == 2018 and key[0] == 10 \
                else boundary_for_legacy_hl(key)
            if boundary not in grouped:
                order.append(boundary)
            grouped[boundary].append(key)
        return [(key, grouped[key]) for key in order]

    # The 2020 redesign numbers every component but still prints common totals
    # at the end of small roman runs.  Preserve those runs.  Its Q5 and Q11 are
    # short-question menus: the final 8×7/letter tariff belongs to every letter,
    # not to one ten-letter mega-card.
    if year == 2020:
        out = []
        by_parent = defaultdict(list)
        parent_order = []
        for key in leaves:
            parent = key[:2]
            if parent not in by_parent:
                parent_order.append(parent)
            by_parent[parent].append(key)
        for q, letter in parent_order:
            members = by_parent[(q, letter)]
            if q in (5, 11) or not any(k[2] for k in members):
                out.extend((k, [k]) for k in members)
                continue
            run = []
            for key in members:
                run.append(key)
                if printed_total(texts.get(key, '')) is not None:
                    boundary = (q, letter, None) if len(run) > 1 else key
                    # More than one tariff run can sit under the same letter;
                    # give later ones the last roman so ids remain distinct.
                    if any(g == boundary for g, _ in out):
                        boundary = run[-1]
                    out.append((boundary, list(run)))
                    run = []
            if run:
                out.extend((k, [k]) for k in run)
        return sorted(out, key=lambda item: natural(item[1][0]))

    # A common tariff printed after the second roman prices these pairs as one
    # selectable task.  Joining them also restores the first 2018 wording,
    # whose PDF block is only the fragment "velocity and" on its own.
    pair = None
    if (year, level) == (2018, 'ol'):
        pair = {(12, 'a', 'i'), (12, 'a', 'ii')}
    elif (year, level) == (2023, 'ol'):
        pair = {(3, None, 'i'), (3, None, 'ii')}
    if pair and pair <= set(leaves):
        out, inserted = [], False
        members = [key for key in leaves if key in pair]
        for key in leaves:
            if key in pair:
                if not inserted:
                    out.append((members[0], members))
                    inserted = True
                continue
            out.append((key, [key]))
        return out

    return [(key, [key]) for key in leaves]


def _question_blocks(paper, q):
    blocks = list(paper._all_blocks())
    starts = []
    for i, block in enumerate(blocks):
        text = paper_reader.RUBRIC_HEAD.sub('', block, count=1)
        m = paper_reader.QHEAD.match(text)
        if m:
            starts.append((int(m.group(1) or m.group(2)), i, text[m.end():].strip()))
    start = next(((i, rest) for found, i, rest in starts if found == q), None)
    if start is None:
        return []
    i, rest = start
    end = next((j for found, j, _ in starts if j > i and found > q), len(blocks))
    return ([rest] if rest else []) + blocks[i + 1:end]


def legacy_group_question(paper, boundary, members):
    q, letter, _ = boundary
    blocks = _question_blocks(paper, q)
    if letter is None:
        return clean_paper_text(' '.join(blocks))

    # Q12 is priced by its printed (a)--(d) alternatives.  Slice the exact
    # paper block stream at those top-level markers so each card carries its
    # own full route, including its stimulus and internal romans.
    start = None
    end = len(blocks)
    for i, block in enumerate(blocks):
        found_letter, found_roman, _ = paper_reader._leading(block)
        if found_letter == letter and found_roman is None and start is None:
            start = i
            continue
        if start is not None and found_letter and found_roman is None \
                and found_letter > letter:
            end = i
            break
    if start is not None:
        return clean_paper_text(' '.join(blocks[start:end]))

    pieces = [paper.text(q, letter), paper.stem(q, letter)]
    pieces.extend(paper.text(*key) for key in members if key != boundary)
    return clean_paper_text(' '.join(p for p in pieces if p))


def question_for(year, level, paper, boundary, members, texts):
    if level == 'hl' and year <= 2019:
        return legacy_group_question(paper, boundary, members), ''

    asks = []
    for key in members:
        text = clean_paper_text(texts.get(key, ''))
        # A sealed ask can be followed in the same PDF block by the next
        # table/stimulus.  Its own printed tariff is a safe end boundary.
        m = PAPER_MARK.search(text)
        if m:
            text = text[:m.end()].strip()
        label = ''.join(f'({x})' for x in key[1:] if x)
        asks.append(f'{label} {text}'.strip() if len(members) > 1 else text)
    question = clean_paper_text(' '.join(asks))
    q, letter, _ = members[0]
    stem = clean_paper_text(paper.stem(q, letter) or paper.stem(q) or '')
    # A grouped run needs its setup in the question itself because one common
    # stem may contain an earlier/later tariff run.  Exact leaves keep the
    # conventional separate stem field.
    if len(members) > 1 and stem:
        question, stem = clean_paper_text(f'{stem} {question}'), ''
    return question, stem


def scheme_raw(year, level):
    path = os.path.join(
        ROOT, 'examiner-reports', 'physics', 'schemes', f'{year}-{level}.md')
    raw = open(path, encoding='utf-8', errors='ignore').read()
    # Repair appendices remain available to the provenance matcher, but are a
    # second copy of the document and must not participate in question order.
    raw = raw.split('<!-- markbank:', 1)[0].split('<!-- pdf-block-order', 1)[0]
    return raw, path


def candidates(question, haystack):
    qwords = [x[0] for x in token_offsets(question)]
    words = [x[0] for x in haystack]
    if not qwords:
        return []
    floor = min(3, len(qwords))
    for width in range(min(12, len(qwords)), floor - 1, -1):
        for offset in range(0, min(70, len(qwords) - width + 1)):
            needle = qwords[offset:offset + width]
            found = [i for i in range(len(words) - width + 1)
                     if words[i:i + width] == needle]
            if found:
                return [(i, width, offset) for i in found]
    return []


def locate_groups(groups, questions, raw, texts):
    haystack = token_offsets(raw)
    locations = {}
    previous = -1
    for boundary, members in groups:
        # A grouped tariff repeats the shared paper stem on the card, but the
        # scheme prints that stem only once.  Searching it for every later run
        # finds the first group again.  Anchor on the first leaf ask instead;
        # it is the wording printed at this exact scheme boundary.
        searches = [clean_paper_text(texts.get(key, '')) for key in members]
        searches.append(questions[boundary])
        forward = []
        for search in searches:
            found = candidates(search, haystack)
            forward = [item for item in found
                       if haystack[item[0]][1] > previous]
            if forward:
                break
        if not forward:
            continue
        index, _, _ = forward[0]
        at = haystack[index][1]
        locations[boundary] = at
        previous = at
    return locations


def mark_value(text):
    """Maximum-credit value represented by one printed mark expression."""
    nums = [int(n) for n in re.findall(r'\d{1,2}', text)]
    if not nums:
        return None
    mult = re.search(r'(\d{1,2})\s*[x×]\s*(\d{1,2})', text)
    if mult:
        return int(mult.group(1)) * int(mult.group(2))
    if re.search(r'\d\s*\+\s*\d', text):
        return sum(int(n) for n in re.findall(r'\d{1,2}', text))
    return max(nums)


def _strip_marks(text):
    text = MARK_TOKEN.sub(' ', text)
    text = TRAILING_TARIFF.sub(' ', text)
    text = re.sub(r'\s+\(?[–-]\d+[^)]*\)?\s*$', ' ', text)
    return ' '.join(text.split()).strip(' •;,:')


def answer_rows(question, chunk):
    """Return (traceable candidate rows, full-credit marks seen)."""
    qfold = ' '.join(x[0] for x in token_offsets(question))
    rows, scores, buffer = [], [], []

    def flush(score=None):
        nonlocal buffer
        claim = _strip_marks(' '.join(buffer))
        buffer = []
        if (not claim or len(claim) > 620 or CONTENT_FREE.fullmatch(claim)
                or MARK_ONLY.fullmatch(claim)
                or GRADING.match(claim)
                or sum(ch.isalnum() for ch in claim) < 2):
            return
        if claim not in rows:
            rows.append(claim)
            scores.append(score)

    for raw_line in chunk.splitlines():
        line = ' '.join(raw_line.split()).strip()
        if not line:
            continue
        if PAGE.match(line):
            flush()
            continue
        lower = fold(line)
        if ('accept partial' in lower or lower.startswith('partial answer')
                or GRADING.match(line)):
            flush()
            continue

        marks = list(MARK_TOKEN.finditer(line))
        score = None
        if marks:
            score = mark_value(next(
                (m.group(1) or m.group(2) for m in marks
                 if 'partial' not in fold(m.group(0))),
                marks[0].group(1) or marks[0].group(2)))
        elif re.search(r'\b\d{1,2}\s+or\s+\d{1,2}\s*$', line):
            score = mark_value(line.rsplit(' ', 3)[-3] + ' or ' + line.rsplit(' ', 1)[-1])

        clean = _strip_marks(line)
        words = ' '.join(x[0] for x in token_offsets(clean))
        appears_in_question = len(words.split()) >= 4 and words in qfold
        is_question = (appears_in_question or QUESTIONISH.match(clean)
                       or ('?' in clean and not re.search(r'=|→|⇒', clean)))
        if is_question:
            flush()
            continue
        if not clean or MARK_ONLY.fullmatch(clean):
            if score is not None:
                flush(score)
            continue
        buffer.append(clean)
        if score is not None:
            flush(score)
    flush()
    return rows, scores


def display_text(text):
    """Return the build-equivalent glyph repair, or None if it is unsafe.

    The build repairs every proven subset-glyph mapping.  Mirror that repair
    here so one corrupt equation row does not discard an otherwise sound
    40/56-mark legacy card.  A doubled mathematical digit is deliberately
    rejected before demangling: the PDF can map two different digits to the
    same repeated character, so collapsing it would manufacture a value.
    """
    text = text.translate(PHYSICS_GLYPHS)
    for _ in range(4):
        repaired = DOUBLED_MATHS_LETTER.sub(r'\1', text)
        if repaired == text:
            break
        text = repaired
    text = ''.join(mathtext.GLYPH.get(char, char) for char in text)
    if DOUBLED_MATHS_DIGIT.search(text) or mathtext.unreadable(text):
        return None
    return text


def traceable(scheme_path, claims):
    if not claims:
        return set()
    proc = subprocess.run(
        ['node', VERIFY], cwd=ROOT, text=True, capture_output=True,
        input=json.dumps({
            'scheme': os.path.relpath(scheme_path, ROOT), 'claims': claims,
        }))
    if proc.returncode:
        raise RuntimeError(proc.stderr.strip() or 'verify-claims failed')
    return set(json.loads(proc.stdout)['ok'])


def total_for(year, level, boundary, members, questions, scores):
    q, _, _ = boundary
    if level == 'hl' and year <= 2019:
        if q <= 4:
            return 40
        if q in (5, 11):
            return 7
        if q == 12:
            return 28
        return 56
    if year <= 2020 and q in (5, 11):
        return 7
    total = printed_total(questions[boundary])
    if total:
        return total
    full = [score for score in scores if score]
    return sum(full) if full else None


def topic_for(question, q):
    text = fold(question)
    if q <= 4 or re.search(r'\bexperiment|apparatus|measurements?|plot a graph|graph paper', text):
        return 'phys-u2'
    rules = [
        (r'projectile|velocity|acceleration|newton.s law|momentum', 'phys-1-1'),
        (r'force|equilibrium|moment\b|friction|weight', 'phys-1-2'),
        (r'hooke|spring|elastic|simple harmonic', 'phys-1-3'),
        (r'work|power|kinetic|potential energy|conservation of energy', 'phys-1-4'),
        (r'gravitation|gravity|satellite|planet|moon', 'phys-1-5'),
        (r'circular|centripetal|angular velocity', 'phys-1-6'),
        (r'heat|temperature|latent|specific heat|thermometric', 'phys-2-1'),
        (r'transverse|longitudinal|wave speed|frequency|wavelength', 'phys-2-2'),
        (r'refraction|critical angle|total internal|lens|mirror', 'phys-2-3'),
        (r'light|electromagnetic|colour|spectrum|polarisation', 'phys-2-4'),
        (r'sound|resonance|stretched string|pipe|intensity', 'phys-2-5'),
        (r'diffraction grating|interference|coherent|superposition', 'phys-2-6'),
        (r'doppler|diffraction', 'phys-2-7'),
        (r'coulomb|charge|electroscope|induction|point discharge', 'phys-3-1'),
        (r'electric field|capacitor|capacitance|potential divider', 'phys-3-2'),
        (r'current|resistance|resistivity|diode|transistor|circuit|fuse', 'phys-3-3'),
        (r'magnetic field|magnet\b', 'phys-3-4'),
        (r'current.carrying|motor|galvanometer|loudspeaker', 'phys-3-5'),
        (r'induc|faraday|lenz|transformer|generator|eddy current', 'phys-3-6'),
        (r'electron|cathode ray|thermionic', 'phys-4-1'),
        (r'photoelectric|x.ray|work function|photon', 'phys-4-2'),
        (r'rutherford|bohr|gold foil|atomic model|line spectrum', 'phys-4-3'),
        (r'radioactiv|half.life|decay|radiation|isotope', 'phys-4-4'),
        (r'mass defect|pair annihilation|particle|quark|hadron|mev|ev\b', 'phys-4-5'),
        (r'fission|fusion|reactor|moderator|control rod', 'phys-4-6'),
    ]
    for pattern, topic in rules:
        if re.search(pattern, text):
            return topic
    return 'phys-u1'


def slug(question):
    stop = {'a', 'an', 'and', 'the', 'of', 'to', 'in', 'for', 'on', 'with',
            'each', 'following', 'one', 'two', 'three', 'what', 'how', 'why',
            'give', 'state', 'explain', 'describe', 'calculate', 'draw', 'show'}
    words = [fold(m.group()) for m in TOKEN.finditer(question)]
    words = [w for w in words if w and w not in stop][:10]
    return '-'.join(words) or 'paper-task'


def make_card(year, level, boundary, question, stem, total, rows,
              question_ref=None):
    q, _, _ = boundary
    card = {
        'id': f'phys-{year}-{level}-completion-{key_suffix(boundary)}',
        'topicId': topic_for(f'{stem} {question}', q),
        'conceptId': slug(question),
        'level': 'higher' if level == 'hl' else 'ordinary',
        'year': year,
        'subjectId': 'physics',
        'section': 'A' if q <= 4 else 'B',
        'questionRef': (f'{year} {level.upper()} {question_ref}'
                        if question_ref else
                        f'{year} {level.upper()} {key_label(boundary)}'),
        'questionText': question,
        'tariffModel': {'kind': 'questionTotal'},
        'totalMarks': total,
        'rows': [
            {'id': f'r-{i}', 'kind': 'point', 'verbatim': row, 'marks': None}
            for i, row in enumerate(rows, 1)
        ],
        'notes': ('Question wording is lifted from the SEC paper and the answer '
                  'rows from its marking scheme. The scheme prices this printed '
                  'task as a whole, so row-level marks are not inferred.'),
    }
    if stem:
        card['stem'] = stem
    return card


def build():
    payload, target_sets = load_targets()
    census = census_subject('physics')
    paper_records = {(p['year'], p['level']): p for p in census['papers']}
    cards, held = [], []
    observed = 0

    for year in range(2016, 2026):
        for level in ('hl', 'ol'):
            record = paper_records[(year, level)]
            parts, texts, _ = census_merged('physics', year, level)
            leaves = leaves_of(parts)
            expected = payload['censusCounts'][f'{year}-{level}']
            if len(leaves) != expected or record['leafCount'] != expected:
                raise AssertionError(
                    f'{year} {level}: census drifted {expected} -> {len(leaves)}')
            lookup = {key_label(key): key for key in leaves}
            wanted_labels = target_sets.get((year, level), set())
            missing = wanted_labels - set(lookup)
            if missing:
                raise AssertionError(
                    f'{year} {level}: target(s) absent {sorted(missing)[:5]}')
            targets = {lookup[label] for label in wanted_labels}
            observed += len(targets)

            paper = Paper('physics', year, level)
            groups = groups_for(year, level, leaves, texts)
            questions, stems = {}, {}
            for boundary, members in groups:
                question, stem = question_for(
                    year, level, paper, boundary, members, texts)
                manual_key = (year, level, *boundary)
                question = MANUAL_QUESTIONS.get(manual_key, question)
                questions[boundary], stems[boundary] = question, stem

            raw, scheme_path = scheme_raw(year, level)
            locations = locate_groups(groups, questions, raw, texts)
            located = sorted(set(locations.values()))
            following = {
                at: located[i + 1] if i + 1 < len(located) else len(raw)
                for i, at in enumerate(located)
            }
            proposals, score_map, claims = {}, {}, []
            for boundary, members in groups:
                if not (set(members) & targets):
                    continue
                if all((year, level, *key) in SKIP_LEAVES for key in members):
                    continue
                if not set(members) <= targets:
                    held.append((year, level, boundary,
                                 'published group is only partly open'))
                    continue
                manual_key = (year, level, *boundary)
                if manual_key in MANUAL_ROWS:
                    rows = MANUAL_ROWS[manual_key]
                    proposals[boundary], score_map[boundary] = rows, []
                    claims.extend(rows)
                    continue
                at = locations.get(boundary)
                if at is None:
                    held.append((year, level, boundary, 'scheme prompt not located'))
                    continue
                rows, scores = answer_rows(
                    questions[boundary], raw[at:following[at]])
                proposals[boundary], score_map[boundary] = rows, scores
                claims.extend(rows)

            good = traceable(scheme_path, list(dict.fromkeys(claims)))
            display_proposals = {
                boundary: [display_text(row) for row in rows if row in good]
                for boundary, rows in proposals.items()
            }
            display_claims = list(dict.fromkeys(
                row for rows in display_proposals.values() for row in rows
                if row is not None))
            display_good = traceable(scheme_path, display_claims)
            made = 0
            for boundary, members in groups:
                if boundary not in proposals:
                    continue
                manual_key = (year, level, *boundary)
                question = display_text(questions[boundary])
                stem = display_text(MANUAL_STEMS.get(
                    manual_key, stems[boundary]))
                rows = [row for row in display_proposals[boundary]
                        if row is not None and row in display_good]
                # The largest historical task is a 56-mark question. Thirty
                # concise scheme rows preserve its full marking content while
                # preventing layout appendices from turning into a wall.
                rows = rows[:30]
                total = total_for(
                    year, level, boundary, members, questions,
                    score_map[boundary])
                total = MANUAL_TOTALS.get(manual_key, total)
                if not question or stem is None:
                    held.append((year, level, boundary,
                                 'no safe paper wording'))
                elif total is None or total <= 0:
                    held.append((year, level, boundary, 'no printed total'))
                elif not rows:
                    held.append((year, level, boundary,
                                 'no traceable content-bearing answer row'))
                else:
                    card = make_card(
                        year, level, boundary, question, stem,
                        total, rows,
                        MANUAL_REFS.get(manual_key))
                    figure_key = QUESTION_FIGURES.get(manual_key)
                    if figure_key:
                        card['figureKey'] = figure_key
                        card['labelKey'] = QUESTION_LABEL_KEYS.get(
                            manual_key, [])
                    cards.append(card)
                    made += 1
            wanted_groups = sum(
                bool(set(members) & targets) for _, members in groups)
            print(f'{year} {level}: {made}/{wanted_groups} cards', file=sys.stderr)

    if observed != payload['targetCount']:
        raise AssertionError(
            f'target total drifted {payload["targetCount"]} -> {observed}')
    for year, level, key, why in held:
        print(f'HELD {year} {level} {key_label(key)} — {why}', file=sys.stderr)
    return cards


if __name__ == '__main__':
    if '--refresh-targets' in sys.argv:
        refresh_targets()
    else:
        print(json.dumps(build(), ensure_ascii=False, indent=1))
