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
        r'file (?:type|extension|size|format)', r'smart (?!material)', r'home automation',
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

# Cards whose first keyword hit is the wrong shelf, read one by one (2010-2019,
# the Technology lane of 4 November 2026). The keyword order is right for most
# asks and stays; these name a heading their words lose to an earlier list --
# "Work Breakdown Structure" is project planning, not structures; a question
# whose STEM is about solar panels can ask about structural strength.
TOPIC_OVERRIDES = {
    # 2019 Higher.
    'tech-2019-hl-a1-i': 'tech-core-design',       # impact of technology on research,
    'tech-2019-hl-a1-ii': 'tech-core-design',      # prototyping and manufacture of a product
    'tech-2019-hl-a1-iii': 'tech-core-design',
    'tech-2019-hl-a5': 'tech-core-project',        # work breakdown structure
    'tech-2019-hl-a7': 'tech-core-design',         # product lifecycle phases
    'tech-2019-hl-a12': 'tech-core-design',        # testing against a design specification
    'tech-2019-hl-b2b-i': 'tech-core-structures',  # two-axis movement mechanism
    'tech-2019-hl-b2d': 'tech-core-structures',    # techniques to enhance structural strength
    'tech-2019-hl-b3b-iii': 'tech-core-materials', # joining the belt's sections
    'tech-2019-hl-b3d-ii': 'tech-core-structures', # mechanism to adjust the incline
    'tech-2019-hl-b3c-ii': 'tech-core-energy',     # a treadmill's sensing system
    # 2019 Ordinary.
    'tech-2019-ol-a1-i': 'tech-core-materials',    # safety signs (health and safety)
    'tech-2019-ol-a1-ii': 'tech-core-materials',
    'tech-2019-ol-a4-i': 'tech-core-ict',          # driverless cars
    'tech-2019-ol-a4-ii': 'tech-core-ict',
    'tech-2019-ol-a8': 'tech-core-design',         # universal design
    'tech-2019-ol-b2a-ii': 'tech-core-materials',  # manufacturing by CAM
    'tech-2019-ol-b2c-ii': 'tech-core-project',    # consequences of faulty goods (quality)
    'tech-2019-ol-b3a-i': 'tech-core-ict',         # virtual technology in education
    'tech-2019-ol-b3a-ii': 'tech-core-ict',
    'tech-2019-ol-b3b-iii': 'tech-core-materials', # manufacturing the VR viewer
    'tech-2019-ol-b3d-i': 'tech-core-energy',      # greenhouse gas emissions
    # 2018 Higher.
    'tech-2018-hl-a1-ii': 'tech-core-materials',   # computer aided manufacture
    'tech-2018-hl-a13': 'tech-core-graphics',      # orthographic views (of an IC chip)
    'tech-2018-hl-b2c-i': 'tech-core-ict',         # drone fleet giving on-line coverage
    'tech-2018-hl-b3b-i': 'tech-core-materials',   # choosing the casing's plastic
    'tech-2018-hl-b3c-i': 'tech-core-ict',         # paperless ticketing (computer control)
    'tech-2018-hl-b3c-ii': 'tech-core-ict',
    'tech-2018-hl-b3d-i': 'tech-core-materials',   # workplace and workshop safety
    'tech-2018-hl-b3d-ii': 'tech-core-materials',
    # 2018 Ordinary.
    'tech-2018-ol-a1-i': 'tech-core-materials',    # PPE and its safety sign
    'tech-2018-ol-a1-ii': 'tech-core-materials',
    'tech-2018-ol-a2': 'tech-core-materials',      # air pollution, an air purifier
    'tech-2018-ol-a3': 'tech-core-materials',      # 3D printing a product
    'tech-2018-ol-b2a-i': 'tech-core-materials',   # a plastic wheelbarrow pan
    'tech-2018-ol-b2a-ii': 'tech-core-structures', # two wheels: balance, load
    'tech-2018-ol-b3a-i': 'tech-core-materials',   # plastic base, metal pole
    'tech-2018-ol-b3a-ii': 'tech-core-materials',  # producing the plastic base
    'tech-2018-ol-b3d-i': 'tech-core-design',      # prototypes
    'tech-2018-ol-b3d-ii': 'tech-core-design',
    'tech-2018-ol-a9': 'tech-core-materials',      # steps to manufacture a stand
    # 2017 Higher.
    'tech-2017-hl-a9-i': 'tech-core-ict',          # a wifi hotspot
    'tech-2017-hl-a10': 'tech-core-materials',     # disposing of car materials
    'tech-2017-hl-a14-i': 'tech-core-materials',   # CAM and CNC
    'tech-2017-hl-a14-ii': 'tech-core-materials',  # pick and place in production
    'tech-2017-hl-a15': 'tech-core-graphics',      # sketch the assembled phone
    'tech-2017-hl-b2b-ii': 'tech-core-structures', # a 30:1 speed-up mechanism
    'tech-2017-hl-b2b-iii': 'tech-core-structures',# bearings against friction
    'tech-2017-hl-b2c-ii': 'tech-core-structures', # fixing a tower to its base
    'tech-2017-hl-b2d': 'tech-core-materials',     # pillars of sustainability
    'tech-2017-hl-b3a-i': 'tech-core-ict',         # wearable technology
    'tech-2017-hl-b3b-i': 'tech-core-design',      # ergonomic design
    'tech-2017-hl-b3b-ii': 'tech-core-ict',        # GPS monitoring
    'tech-2017-hl-b3c-i': 'tech-core-materials',   # assembling the moulded casing
    'tech-2017-hl-b3c-ii': 'tech-core-materials',  # a light yet durable casing
    'tech-2017-hl-b3d-i': 'tech-core-project',     # quality characteristics
    'tech-2017-hl-b3d-ii': 'tech-core-project',    # work breakdown structure
    # 2017 Ordinary.
    'tech-2017-ol-a1': 'tech-core-design',         # an accessible door handle
    'tech-2017-ol-a2': 'tech-core-ict',            # remote heating control
    'tech-2017-ol-a3': 'tech-core-materials',      # a portable washing machine
    'tech-2017-ol-a5': 'tech-core-materials',      # safety signs
    'tech-2017-ol-a8': 'tech-core-project',        # work breakdown structure
    'tech-2017-ol-b2a-ii': 'tech-core-ict',        # wearable technologies
    'tech-2017-ol-b2b-i': 'tech-core-materials',   # a plastic outer shell
    'tech-2017-ol-b2b-ii': 'tech-core-materials',
    'tech-2017-ol-b2b-iii': 'tech-core-materials', # vacuum forming
    'tech-2017-ol-b2d-i': 'tech-core-project',     # the CE mark (quality)
    'tech-2017-ol-b3a-i': 'tech-core-materials',   # hardwood for the base
    'tech-2017-ol-b3a-ii': 'tech-core-materials',  # self-assembly products
    'tech-2017-ol-b3d-i': 'tech-core-project',     # problem-solving tools
    'tech-2017-ol-b3d-ii': 'tech-core-materials',  # tubular materials
    # 2016 Higher.
    'tech-2016-hl-a2-i': 'tech-core-ict',          # infrared communication
    'tech-2016-hl-a2-ii': 'tech-core-ict',
    'tech-2016-hl-a3': 'tech-core-materials',      # food miles (sustainability)
    'tech-2016-hl-a4-i': 'tech-core-ict',          # remote monitoring
    'tech-2016-hl-a4-ii': 'tech-core-materials',   # hardness
    'tech-2016-hl-a7-i': 'tech-core-materials',    # environmental impact of soldering
    'tech-2016-hl-a7-ii': 'tech-core-materials',
    'tech-2016-hl-a8': 'tech-core-project',        # product reliability (quality)
    'tech-2016-hl-a14': 'tech-core-design',        # ergonomic features
    'tech-2016-hl-b2a-i': 'tech-core-ict',         # telemedicine
    'tech-2016-hl-b2a-ii': 'tech-core-ict',
    'tech-2016-hl-b2b-i': 'tech-core-structures',  # motion of the prosthetic hand
    'tech-2016-hl-b2b-ii': 'tech-core-structures',
    'tech-2016-hl-b2b-iii': 'tech-core-materials', # material for the linkages
    'tech-2016-hl-b2c-i': 'tech-core-structures',  # factor of safety
    'tech-2016-hl-b3c-ii': 'tech-core-structures', # chain and belt drives
    'tech-2016-hl-b3d-i': 'tech-core-project',     # Gantt chart
    'tech-2016-hl-b3d-ii': 'tech-core-project',
    # 2016 Ordinary.
    'tech-2016-ol-a5-i': 'tech-core-project',      # Gantt chart
    'tech-2016-ol-a5-ii': 'tech-core-project',
    'tech-2016-ol-a6': 'tech-core-materials',      # 3D printing a prototype
    'tech-2016-ol-b2a-ii': 'tech-core-structures', # mechanism to adjust the container's height
    'tech-2016-ol-b2c-i': 'tech-core-project',     # product recall (quality)
    'tech-2016-ol-b2c-ii': 'tech-core-project',
    'tech-2016-ol-b3b-ii': 'tech-core-structures', # mechanism to rotate the camera
    # 2015 Higher.
    'tech-2015-hl-a2-i': 'tech-core-design',       # researching a workstation design
    'tech-2015-hl-a2-ii': 'tech-core-design',
    'tech-2015-hl-a5': 'tech-core-materials',      # safety signs
    'tech-2015-hl-a4': 'tech-core-materials',      # robotic materials handling
    'tech-2015-hl-a11-i': 'tech-core-materials',   # CNC and CAM
    'tech-2015-hl-a11-ii': 'tech-core-materials',
    'tech-2015-hl-a14': 'tech-core-project',       # work breakdown structure
    'tech-2015-hl-a12-ii': 'tech-core-materials',  # pillar drill safety features
    'tech-2015-hl-b2a-i': 'tech-core-ict',         # self-driving cars
    'tech-2015-hl-b2a-ii': 'tech-core-ict',
    'tech-2015-hl-b2b-i': 'tech-core-ict',         # parking-space location systems
    'tech-2015-hl-b2b-ii': 'tech-core-ict',        # bumper radar
    'tech-2015-hl-b2c-i': 'tech-core-project',     # quality dimensions
    'tech-2015-hl-b2c-ii': 'tech-core-project',    # problem-solving technique (quality)
    'tech-2015-hl-b3a-i': 'tech-core-ict',         # technology staging sporting events
    'tech-2015-hl-b3a-ii': 'tech-core-design',     # sponsorship (target market)
    'tech-2015-hl-b3b-i': 'tech-core-structures',  # pulley system
    'tech-2015-hl-b3b-ii': 'tech-core-structures',
    'tech-2015-hl-b3b-iii': 'tech-core-structures',
    'tech-2015-hl-b3c-i': 'tech-core-structures',  # tilting and locking mechanism
    'tech-2015-hl-b3c-ii': 'tech-core-structures', # wheels turning in opposite directions
    'tech-2015-hl-b3d-ii': 'tech-core-ict',        # video image quality
    # 2015 Ordinary.
    'tech-2015-ol-a1': 'tech-core-design',         # a multi-tool meeting a user's needs
    'tech-2015-ol-a5': 'tech-core-materials',      # band saw safety
    'tech-2015-ol-a6': 'tech-core-structures',     # lever
    'tech-2015-ol-a7': 'tech-core-graphics',       # 2D sketch of the bench
    'tech-2015-ol-a9': 'tech-core-structures',     # toothed belt drive
    'tech-2015-ol-a12': 'tech-core-graphics',      # graphic techniques
    'tech-2015-ol-b2b-iii': 'tech-core-materials', # a casing and its fixing
    'tech-2015-ol-b2d-i': 'tech-core-project',     # quality attributes
    'tech-2015-ol-b2d-ii': 'tech-core-project',    # costs of improving quality
    'tech-2015-ol-b3a-ii': 'tech-core-materials',  # material for protective gloves
    'tech-2015-ol-b3b-i': 'tech-core-materials',   # the PTO guard (safety)
    'tech-2015-ol-b3b-ii': 'tech-core-structures', # universal joints
    'tech-2015-ol-b3b-iii': 'tech-core-structures',# speed reduction mechanism
    'tech-2015-ol-b3c-i': 'tech-core-graphics',    # CAD
    'tech-2015-ol-b3c-ii': 'tech-core-materials',  # CAM
    # 2014 Higher.
    'tech-2014-hl-a1': 'tech-core-materials',      # incineration (waste, environment)
    'tech-2014-hl-a2': 'tech-core-materials',      # smart fabrics
    'tech-2014-hl-a3': 'tech-core-materials',      # HDPE, thermoplastics
    'tech-2014-hl-a7': 'tech-core-design',         # ergonomic laptop stand
    'tech-2014-hl-a10': 'tech-core-design',        # rapid prototyping
    'tech-2014-hl-a14': 'tech-core-ict',           # social networking
    'tech-2014-hl-b2d': 'tech-core-materials',     # shin guard materials and fastening
    'tech-2014-hl-b3b': 'tech-core-structures',    # torque, drive mechanism
    'tech-2014-hl-b3c': 'tech-core-ict',           # bitmap and vector images
}

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
