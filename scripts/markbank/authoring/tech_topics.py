#!/usr/bin/env python3
"""Shelve a Technology ask under a syllabus heading.

    python3 scripts/markbank/authoring/tech_topics.py     # self-check

The Leaving Certificate Technology syllabus has twelve areas: seven core, all
examined in Sections A and B, and five options, of which Section C sets one
question each. The five are named on the paper -- "Option 3 - Information and
Communications Technology" -- so Section C needs no guesswork at all and gets
none: `topic_for_option` reads the option number, and all ten sittings in the
corpus number the same five options the same way.

Sections A and B do need a decision, and it is made on the ask's own words
against the syllabus's own sub-heading names. The lists below are the syllabus
vocabulary (curriculum.ts, subject "technology") plus the terms the papers use
for the same things -- "WBS" for production planning, "AC"/"DC" for
electricity. Nothing here decides what a card SAYS; it decides which shelf it
sits on.

Order matters: the first list that matches wins, so the specific areas
(electricity, mechanisms) are consulted before the general ones (materials,
design), which otherwise absorb everything with a material in it.

The keywords are written as plain strings and joined here rather than set in a
re.VERBOSE block: verbose mode strips the spaces INSIDE a pattern, so
"energy efficien" silently became "energyefficien" and matched nothing. Every
multi-word keyword in the first draft of this file was dead.
"""
import re
import sys

# Section C, straight off the paper's own option heading.
OPTION_TOPIC = {
    1: 'tech-opt-control',        # Applied Control Systems
    2: 'tech-opt-electronics',    # Electronics and Control
    3: 'tech-opt-ict',            # Information and Communications Technology
    4: 'tech-opt-manufacturing',  # Manufacturing Systems
    5: 'tech-opt-materials',      # Materials Technology
}

CORE = [
    ('tech-core-energy', [
        r'electricit', r'electronic', r'circuit', r'resistor', r'resistance',
        r'capacitor', r'transistor', r'diode', r'\bled\b', r'light emitting',
        r'voltage', r'\bcurrent\b', r'\bohm', r'ampere', r'\bamp\b', r'\bwatt',
        r'power supply', r'batter(?:y|ies)', r'solar', r'photovoltaic',
        r'wind (?:turbine|energy|power|farm)', r'renewable', r'\bdc\b', r'\bac\b',
        r'energy', r'kilowatt', r'thermistor', r'\bldr\b', r'sensor', r'relay',
        r'logic gate', r'truth table', r'soldering', r'integrated circuit',
        r'\bic\b', r'\bpcb\b', r'printed circuit', r'darlington',
        r'potential divider', r'conductor', r'insulator', r'semi-?conductor',
        r'electrical', r'charging', r'charger', r'inverter', r'generator',
        r'\bfuse\b', r'earthing', r'series and parallel', r'insulation',
        r'u-?value', r'fossil fuel', r'heat pump', r'\bwifi\b', r'e-?bike',
        r'electric (?:bicycle|vehicle|motor|car)', r'\bkwh\b', r'wattage',
        r'\bhybrid\b', r'\buv\b', r'ultra-?violet', r'\blamp\b', r'lighting',
    ]),
    ('tech-core-structures', [
        r'structur', r'mechanism', r'\bgear', r'pulley', r'lever', r'linkage',
        r'\bcam\b', r'crank', r'ratchet', r'mechanical advantage',
        r'velocity ratio', r'torque', r'moment', r'\bforce', r'\bload\b',
        r'effort', r'\bbeam', r'\bstrut', r'\btie\b', r'truss', r'\bframe',
        r'shell', r'centre of gravity', r'stability', r'friction', r'tension',
        r'compression', r'bending', r'stress', r'strain', r'\brpm\b',
        r'angular velocity', r'worm (?:gear|wheel)', r'bearing', r'\baxle',
        r'screw thread', r'hydraulic', r'pneumatic', r'spring',
        r'shock absorb', r'triangulat', r'aerodynamic', r'bridge', r'cantilever',
        r'vibration', r'\btunnel\b', r'transport', r'\broof\b', r'\bpod\b',
        r'\bsuspension\b', r'\bstiff', r'rigidity', r'\bstrength\b',
    ]),
    ('tech-core-ict', [
        r'computer', r'software', r'hardware', r'internet', r'network',
        r'wi-?fi', r'bluetooth', r'broadband', r'website', r'\bweb\b',
        r'e-?mail', r'cloud', r'database', r'spreadsheet', r'\bapp\b',
        r'\bapps\b', r'digital', r'cyber', r'phishing', r'malware',
        r'ransomware', r'\bvirus', r'firewall', r'password', r'encryption',
        r'\bdata\b', r'social media', r'streaming', r'artificial intelligence',
        r'\bai\b', r'augmented reality', r'virtual reality', r'\bqr code',
        r'\bgps\b', r'\bram\b', r'\brom\b', r'processor', r'\bcpu\b', r'\busb\b',
        r'pixel', r'resolution', r'\buhd\b', r'\b4k\b', r'\bbyte',
        r'file (?:type|extension|size|format)', r'smart ', r'home automation',
        r'\biot\b', r'internet of', r'online', r'contactless', r'payment',
        r'\bscan(?:ner|ning)?\b', r'\bcode\b', r'programm', r'\bdrone',
        r'\bapp(?:lication)? software', r'video ?conferenc', r'biometric',
        r'facial recognition', r'\brfid\b', r'\bnfc\b', r'skimming',
        r'e-?commerce', r'purchas', r'satellite', r'cellular', r'mobile phone',
        r'\bphone\b', r'autonom', r'\brobot', r'\bsensor', r'\bwireless\b',
    ]),
    ('tech-core-graphics', [
        r'sketch', r'\bdrawing', r'\bdraw\b', r'orthographic', r'elevation',
        r'plan view', r'isometric', r'pictorial', r'freehand', r'projection',
        r'render', r'scale drawing', r'dimension', r'annotated', r'graphic',
        r'\bcad\b', r'computer aided (?:drawing|design)', r'modelling',
        r'exploded view', r'flow ?chart', r'\bchart\b', r'\bgraph\b',
        r'presentation', r'portfolio', r'\bfolio\b', r'infographic', r'\blogo\b',
    ]),
    ('tech-core-project', [
        r'project management', r'quality', r'gantt', r'critical path',
        r'network diagram', r'work breakdown', r'\bwbs\b', r'deming',
        r'\btqm\b', r'\biso\b', r'kaizen', r'just.in.time', r'\bjit\b',
        r'\blean\b', r'schedul', r'milestone', r'budget', r'time management',
        r'risk assessment', r'conformance', r'durabilit', r'reliabilit',
        r'inspection', r'six sigma', r'benchmark', r'planning tool',
        r'objectives when planning', r'critical to the successful',
    ]),
    ('tech-core-materials', [
        r'material', r'plastic', r'polymer', r'thermoplastic', r'thermoset',
        r'\bmetal', r'steel', r'aluminium', r'timber', r'\bwood', r'hardwood',
        r'softwood', r'\bmdf\b', r'plywood', r'composite', r'carbon fibre',
        r'fabric', r'textile', r'adhesive', r'\bglue', r'epoxy', r'\bfinish',
        r'lacquer', r'varnish', r'\bpaint', r'corrosion', r'galvanis',
        r'recycl', r'upcycl', r'compost', r'biodegradable', r'sustainab',
        r'environment', r'manufactur', r'production', r'injection moulding',
        r'vacuum forming', r'extrusion', r'casting', r'3d print', r'additive',
        r'subtractive', r'machining', r'lathe', r'milling', r'\bjoint\b',
        r'joining', r'welding', r'brazing', r'fastener', r'\bscrew\b',
        r'\brivet', r'packaging', r'cardboard', r'\bpet\b', r'batch',
        r'mass production', r'assembl', r'\bjig\b', r'waste',
        r'circular economy', r'carbon footprint', r'life ?cycle',
        r'raw material', r'hardness', r'ductil', r'malleab', r'elastic',
        r'toughness', r'density', r'safety', r'hazard', r'\bppe\b',
        r'protective equipment', r'first aid', r'workshop', r'sanding',
        r'grit size', r'abrasive', r'\bdrill', r'\bsaw\b', r'\bcut(?:ting)?\b',
        r'\btool\b', r'\bfixture', r'\bmould', r'\bpaper\b', r'\bglass\b',
        r'concrete', r'\brubber\b', r'\bfoam\b', r'\bsander\b', r'\bdust\b',
        r'sporting equipment', r'\bsteril', r'disinfect',
    ]),
    ('tech-core-design', [
        r'design', r'\bbrief\b', r'ergonomic', r'anthropometric', r'aesthetic',
        r'user need', r'needs of', r'target market', r'constraint',
        r'research', r'investigat', r'generat(?:e|ing) idea', r'innovat',
        r'concept', r'iterat', r'evaluat', r'consumer', r'\bmarket',
        r'branding', r'\bbrand', r'product development', r'specification',
        r'\bsales\b', r'advertis', r'prototype', r'\btest(?:ing)?\b',
        r'\bfunction\b', r'\bidea\b', r'space exploration', r'\bdemand\b',
        r'infectious disease', r'\benhanc',
    ]),
]

CORE = [(t, re.compile('|'.join(words), re.I)) for t, words in CORE]

ALL_TOPICS = [t for t, _ in CORE] + [OPTION_TOPIC[i] for i in sorted(OPTION_TOPIC)]


def topic_for_option(option):
    return OPTION_TOPIC.get(option)


def topic_for(*texts):
    """The first syllabus heading the ask's own words name, or None."""
    blob = ' '.join(t for t in texts if t)
    if not blob.strip():
        return None
    for topic, pattern in CORE:
        if pattern.search(blob):
            return topic
    return None


if __name__ == '__main__':
    # Every multi-word keyword must actually be able to match. The first draft
    # of this file set the lists inside a re.VERBOSE block, which strips the
    # spaces inside a pattern, and every one of them was dead.
    bad = [t for t, p in CORE if not p.search('energy efficiency design '
                                              'quality material structure '
                                              'computer sketch')]
    print(f'{len(CORE)} core headings, {len(OPTION_TOPIC)} option headings')
    print('unreachable:', bad or 'none')
    sys.exit(1 if bad else 0)
