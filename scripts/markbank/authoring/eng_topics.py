#!/usr/bin/env python3
"""File an Engineering part under a syllabus topic from its wording.

    python3 scripts/markbank/authoring/eng_topics.py     # unmatched report

The topics ARE the syllabus's own headings, in its own order. The Leaving
Certificate Engineering syllabus has two sections, and the written examination
is the second of them: "2. Materials and Technology", whose fourteen headings
are HEALTH AND SAFETY, CLASSIFICATION AND ORIGIN OF METALS, STRUCTURE OF
METALS, IRON AND STEEL, NON-FERROUS METALS, HEAT TREATMENT OF METALS,
CORROSION OF METALS, MATERIALS TESTING, PLASTICS, JOINING OF MATERIALS,
MACHINING, METROLOGY, MANUFACTURING PROCESSES and TECHNOLOGY.

Every term below is lifted from the prose printed under those headings. The
syllabus is a SCAN with no text layer, so it was read by rendering the pages
and looking at them; the phrases are quoted from what is printed there. Nothing
is invented vocabulary, and where a term could sit under two headings the
syllabus's own placement decides it:

  * the EQUILIBRIUM DIAGRAM appears under three headings. Structure of metals
    has "equilibrium diagrams for simple eutectics and solid solutions", Iron
    and steel has "influence of carbon content; equilibrium diagrams", and Heat
    treatment has "heat treatment of plain carbon steels; equilibrium diagram".
    Carbon content decides between them, and the bare phrase files under
    structure, which is where the syllabus introduces it.
  * CUTTING FLUID is Machining ("types of cutting fluid, lubricant and methods
    of application"), not Health and safety, even though the papers ask about
    handling it safely.
  * WELDING is Joining of materials, and the transformer and AC/DC printed
    beside it there belong to it too -- "Differentiation between AC and DC
    electricity; principle of the transformer. Electrode classification."

Anything unmatched is REPORTED, never filed under a default: a wrong shelf
sends a student to revise the wrong thing, and a gap only asks a person to
look.
"""
import collections
import os
import re
import sys

DIR = os.path.dirname(os.path.abspath(__file__))

# (topic id, weight, pattern). Most specific wins on the highest weight.
RULES = [
    # ── Materials ─────────────────────────────────────────────────────────
    ('eng-1-4', 12, r'\b(cast iron|carbon steel|plain carbon|mild steel|'
                    r'pig iron|blast furnace|basic oxygen|electric arc furnace|'
                    r'steel ?making|alloy steel|tool steel|stainless steel|'
                    r'carbon content|(?<!non-)(?<!non )ferrous metal|'
                    r'cupola|converter|open hearth|metal production|'
                    r'production of cast iron)\b'),
    # "The important steel making processes" is where a furnace belongs when
    # nothing says otherwise -- but "Types of furnace and methods of
    # temperature measurement" is ALSO printed under heat treatment, so a bare
    # furnace is filed here only weakly and anything more specific takes it.
    ('eng-1-4', 6, r'\b(furnace|\bcharge\b|tuyere|refractory lining)\b'),
    # "ferrous metal" must not claim "NON-ferrous metal", which is the
    # opposite shelf and the next rule's. They tie on weight, so without the
    # lookbehind the one written first simply wins.
    ('eng-1-5', 12, r'\b(non[- ]ferrous|copper|aluminium|brass|bronze|gunmetal|'
                    r'bearing metal|zinc|\btin\b|lead\b|silver|titanium|'
                    r'anodis\w+|bauxite)\b'),
    ('eng-1-3', 11, r'\b(microstructure|grain size|recrystallis\w+|dendritic|'
                    r'solidification|atomic lattice|crystal structure|'
                    r'eutectic|eutectoid|solid solution|equilibrium diagram|'
                    r'\bingot\b|allotrop\w+|austenit\w+|martensit\w+|'
                    r'pearlit\w+|ferrite|cementite|crystalline|amorphous|'
                    r'body centred cubic|face centred cubic|\bbcc\b|\bfcc\b|'
                    r'cooling curve|metallic bond|close packed)\b'),
    ('eng-1-2', 10, r'\b(periodic table|table of the elements|chemical symbol|'
                    r'metals and non[- ]metals|importance of alloys|'
                    r'physical properties of metals|mining|\bores?\b|'
                    r'ore dressing|\w*metallurgy|extraction of metals|'
                    r'properties of metals|electrical conduct\w+|alloys?\b)\b'),
    ('eng-1-9', 11, r'\b(plastics?|thermoplastic|thermosetting|polyethylene|'
                    r'polypropylene|\bpvc\b|polystyrene|acrylic|\bptfe\b|'
                    r'cellulose acetate|nylon|phenolic resin|polyester resin|'
                    r'epoxy resin|polyurethane|injection moulding|extrusion|'
                    r'vacuum forming|blow moulding|compression moulding|'
                    r'calendaring|laminating|polymer\w*|polylactic acid|'
                    r'\bpla\b|rubber|elastomer|monomer|copolymer\w*|'
                    r'polymerisation|\bresin\b|composite|carbon fibre)\b'),
    # ── Processes ─────────────────────────────────────────────────────────
    ('eng-2-6', 13, r'\b(heat treat\w*|quench\w*|tempering|annealing|'
                    r'normalis\w+|case harden\w+|carburis\w+|nitriding|'
                    r'flame hardening|induction hardening|age hardening|'
                    r'stress relieving|critical point|hardening|'
                    # "Types of furnace and methods of temperature
                    # measurement" sits under this heading. The furnace itself
                    # is left out: a blast furnace is steel making, not heat
                    # treatment, and both would match it.
                    r'pyrometer|thermocouple|critical temperature|'
                    r'\buct\b|\blct\b)\b'),
    ('eng-2-10', 12, r'\b(joining of materials|adhesive|adhesion|'
                     r'mechanical fastening|soldering|brazing|'
                     r'fusion welding|oxy-?acetylene|electric arc|\bweld\w*|'
                     r'\bflux(es)?\b|electrode|inert gas|\bmig\b|\btig\b|'
                     r'resistance welding|spot welding|transformer|'
                     r'\bac\b and \bdc\b|riveted?|rivets?|'
                     r'permanent joint|non[- ]permanent joint|'
                     r'temporary join\w*|mechanical fasten\w*|thumb ?screw|'
                     r'lock ?nut|\bsolder\w*|\bbraz\w+)\b'),
    ('eng-2-11', 11, r'\b(machining|\blathe\b|shaping machine|milling machine|'
                     r'grinding (?:machine|wheel)|work holding|cutting tool|'
                     r'rake angle|chip formation|machinability|tool life|'
                     r'cutting speed|cutting fluid|lubricant|taper turning|'
                     r'screw thread|indexing|surface finish|swarf|'
                     r'\bchuck\b|tailstock|knurling|drill\w*|tapping size|'
                     r'clearance hole|bandsaw|built[- ]up edge|reamer|'
                     r'counterbor\w+|countersink\w*|\bmill\w*|parting off|'
                     r'plug tap|tapered tap|\btaps?\b|\btapping\b|blind hole|'
                     r'screwcutting|boring|undercutting|eccentric turning|'
                     r'parallel turning|deburr\w+|internal thread|\bgrinding\b|cutting tip|tungsten carbide|surface finish)\b'),
    # The syllabus's OTHER Technology heading, in section 1: "Dismantling and
    # assembling a range of engineering components derived from prime movers,
    # power transmission systems, brakes and other mechanisms to achieve an
    # appreciation of the technical details of assembly, operation and basic
    # design concepts." The papers ask about these constantly -- toggle
    # mechanisms, leadscrews, single- and double-acting cylinders -- and with
    # no heading for them 40-odd asks a year filed nowhere.
    ('eng-2-15', 11, r'\b(mechanism|gear ?(?:train|box|wheel|s)?\b|pulley|'
                     r'belt drive|chain drive|\blever\b|\bcams?\b|crank\w*|'
                     r'linkage|toggle|leadscrew|lead screw|screw jack|ratchet|'
                     r'\bbearings?\b|clutch|\bbrakes?\b|prime mover|'
                     r'power transmission|\btorque\b|single[- ]acting|'
                     r'double[- ]acting|pneumatic|hydraulic|cylinder|piston|'
                     r'lubricat\w+|\bgrease\b|\bvice\b|jig\b|fixture|universal joint|reciprocating|oscillat\w+|timing belt|timing chain|\bfulcrum\b|lifting platform|rotary motion|drive system)\b'),
    ('eng-2-13', 10, r'\b(manufacturing process|fabrication|casting|forging|'
                     r'rolling|drawing|extruding|pressing|quality control|'
                     r'sand cast\w*|die cast\w*|3-?d print\w*|'
                     r'additive manufactur\w+|prototyp\w+|cnc\b)\b'),
    # ── Properties, measurement and practice ──────────────────────────────
    ('eng-3-8', 12, r'\b(tensile|compression|\bshear\b|torsion|bending|'
                    # The papers print it with spaces around the hyphen --
                    # "plot the stress - strain diagram" -- so a bare hyphen
                    # class never matched it.
                    r'stress\s*[-–]?\s*strain|young\'?s modulus|proof stress|'
                    # "Non-destructive tests using liquids, magnetism, sound,
                    # and radiation" is the syllabus's own list.
                    r'liquid penetrant|dye penetrant|ultrasonic|radiograph\w+|'
                    r'magnetic particle|safety factor|factor of safety|'
                    r'\bhardness\b|brinell|vickers|rockwell|izod|charpy|'
                    r'impact test|ductility|fatigue|non[- ]destructive|'
                    r'\bcreep\b|thermal conductivity|specific heat capacity|'
                    r'brittleness|malleab\w+|toughness|elasticity|'
                    r'ultimate tensile strength|\buts\b)\b'),
    # "The mechanism of corrosion, electrolytic action" and "Methods of
    # minimising corrosion; protective coatings". The papers write the
    # mechanism as OXIDATION as often as they name corrosion.
    ('eng-3-7', 12, r'\b(corrosion|rust\w*|oxidation|electrolytic action|'
                    r'protect\w*\s+(?:steel|metal|iron)|galvanis\w+|'
                    r'protective coating|anodic protection|cathodic protection|'
                    r'sacrificial\s+\w+)\b'),
    ('eng-3-12', 11, r'\b(metrology|limits and tolerances|systems of limits|'
                     r'types of fit|interchangeability|selective assembly|'
                     r'limit gauge|vernier|micrometer|sine bar|slip gauge|'
                     r'profile projector|thread form gauge|'
                     r'grades of accuracy|standards of measurement|'
                     r'clearance fit|interference fit|transition fit|'
                     r'type of fit|limits and fits|toleranc\w+|allowance|'
                     r'nominal (?:size|diameter)|parallax|dimensioning|'
                     r'upper limit|lower limit|\bfits\b)\b'),
    ('eng-3-1', 11, r'\b(health and safety|first aid|personal protection|'
                    r'personal protective equipment|\bppe\b|safety precaution|'
                    r'safeguarding machinery|colour code|work space clearance|'
                    r'electrical hazard|earthing|chemical hazard|corrosive|'
                    r'combustible|explosive|fire protection|fire extinguisher|'
                    r'accident|statutory safety|guard\w*\b|ear protection|'
                    r'eye protection|goggles|ventilat\w+|safety glasses)\b'),
    # Appendix 1's CONTROL TECHNOLOGY, which the fourteen Materials-and-
    # Technology headings do not cover and the papers examine every year in
    # Q7(c): "understand the function of and use electrical power supplies,
    # circuit components and devices"; "understand and use diodes, resistors
    # and transistors in the construction of basic electronic control
    # circuits"; "investigate the role of electronics in the design of
    # fundamental computer hardware"; "understand and use basic pneumatic
    # circuits for simple control applications".
    ('eng-2-16', 11, r'\b(electronic\w*|electronics|circuit component|'
                     r'control circuit|\bcircuits?\b|\bdiodes?\b|'
                     r'resistors?|transistors?|capacitors?|solenoids?|'
                     r'light emitting diode|\bleds?\b|'
                     r'light dependent resistor|\bldr\b|thermistor|'
                     r'printed circuit board|\bpcb\b|electromagnet|'
                     r'\brelays?\b|integrated circuit|microcontroller|'
                     r'micro:?bit|\bsensors?\b|heatsink|micro ?chip|'
                     r'electrical power supply|\bbatter(?:y|ies)\b)\b'),
    # TECHNOLOGY is the syllabus's own catch-all and is weighted LOWEST on
    # purpose: "Outline history of technology. Research into principles and
    # processes. Use of research into possible solutions to problems. The
    # design function: selection of materials, shapes, sizes and processes.
    # *Specialised study of a prescribed topic. ... Careers in engineering."
    # Any heading with a term of its own beats it, so the general asks that
    # open every paper -- smart glasses, HEPA filters, extended reality --
    # land here without pulling anything else off its shelf.
    ('eng-3-14', 9, r'\b(history of technology|design function|'
                    r'careers in engineering|research into principles|'
                    r'hybrid vehicle|solar cell|photovoltaic|renewable energy|'
                    r'wind turbine|robotic?s?\b|automation|'
                    r'artificial intelligence|voice recognition|'
                    r'smart material|sustainab\w+|recycl\w+|'
                    r'environmental impact|carbon footprint|'
                    r'contribution[^.]{0,60}technolog\w+|'
                    r'selection of materials|suitable materials?|'
                    r'research and development|\br ?& ?d\b|prescribed topic|'
                    r'extended reality|\bxr\b|upcycl\w+|smart\b|wireless|'
                    r'drone|bluetooth|autonomous|hydrogen|fuel cell|'
                    r'container ship|\bcad\b|computer aided|'
                    r'remote[- ]control\w*|energy conversion|selection of each material|sanitiser|air purifier|\bhepa\b|co.\s*monitor|facial recognition|standing desk|telescopic|selfie stick|thermostatic|home heating|contribution[^.]{0,40}industry)\b'),
]
# Every rule above is written singular and hyphenated, the way the syllabus
# prints it, and the papers write neither. Three things were silently costing
# matches -- so the relaxation is applied ONCE here rather than smeared over
# ninety alternatives, where it would have to be remembered every time a term
# is added:
#
#   * the trailing \b refuses a plural. "crystal structure" is a rule and the
#     paper asks about "the crystal structures A, B and C", where the \b falls
#     between "e" and "s" and there is no boundary there;
#   * the papers set their hyphen as U+2010, not ASCII "-", so "non[- ]ferrous"
#     did not match the printed "non-ferrous" at all. Only the eye can tell
#     them apart.
#
# A compound is NOT relaxed. Opening the boundary would file any word that
# ends in a term under that term, and the attested compounds are few enough to
# be listed where they belong.
DASHES = re.compile(r'[\u2010-\u2015\u2212]')
COMPILED = [(t, w, re.compile(p[:-2] + r'(?:e?s)?\b', re.I))
            for t, w, p in RULES]


def _normalise(text):
    return DASHES.sub('-', text or '')


def topic_for(text):
    """(topic id, the phrase that decided it) — or (None, None)."""
    best = (0, None, None)
    haystack = _normalise(text)
    for tid, weight, rx in COMPILED:
        m = rx.search(haystack)
        if m and weight > best[0]:
            best = (weight, tid, m.group(0))
    return best[1], best[2]


def concept_for(text, fallback='part'):
    """A slug for the card's concept, from the ask's own first words."""
    words = re.findall(r"[a-z0-9']+", (text or '').lower())
    stop = {'the', 'a', 'an', 'of', 'in', 'to', 'and', 'for', 'is', 'are',
            'was', 'were', 'this', 'that', 'with', 'from', 'by', 'on', 'at',
            'as', 'it', 'what', 'which', 'state', 'give', 'name', 'write',
            'explain', 'outline', 'describe', 'list', 'two', 'one', 'three'}
    keep = [w for w in words if w not in stop][:6]
    return '-'.join(keep) or fallback


def main():
    sys.path.insert(0, DIR)
    import paper as PP                                       # noqa: E402
    import reconcile as R                                    # noqa: E402
    from paper_census import census_subject                  # noqa: E402
    from eng_scheme import EngScheme                         # noqa: E402
    idx = R.leaf_index(census_subject('engineering'))
    hit, miss = collections.Counter(), []
    for (yr, lv, _), leaves in sorted(idx.items()):
        P = PP.Paper('engineering', yr, lv)
        S = EngScheme(yr, lv)
        for leaf in sorted(leaves):
            q, letter, roman = leaf[0], leaf[1], leaf[2]
            try:
                ask = P.text(q, letter, roman) or ''
            except Exception:                                # noqa: BLE001
                ask = ''
            lead = S.lead(q, letter, roman) or S.lead(q, letter) or ''
            tid, _ = topic_for(f'{ask} {lead}')
            if tid:
                hit[tid] += 1
            else:
                miss.append(f'{yr} {lv} Q{q}: {" ".join(ask.split())[:66]}')
    total = sum(hit.values()) + len(miss)
    print(f'{total} asks: {sum(hit.values())} filed, {len(miss)} unmatched')
    for tid, n in sorted(hit.items()):
        print(f'   {tid:10} {n}')
    print('\nunmatched (first 20):')
    for m in miss[:20]:
        print(f'   {m}')


if __name__ == '__main__':
    main()
