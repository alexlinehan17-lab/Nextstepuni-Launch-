#!/usr/bin/env python3
"""File a Construction Studies part under a syllabus topic from its wording.

Filing is a librarian's decision, not exam content -- the question and the
answer are lifted, and where a card is SHELVED is ours to choose. Doing it by
hand was fine for ten papers and is not for twenty, and a hand-filed corpus
drifts: the same question wording ends up under two topics in different years.

The vocabulary is the syllabus's own, taken from the strand and topic titles in
components/MarkBank/deck.ts. Most specific match wins, so "window cill" beats
"wall". Anything unmatched is reported rather than filed under a default -- a
wrong shelf is worse than an obvious gap.
"""
import re

# (topic id, weight, pattern). Weight breaks ties: a longer, more specific
# phrase should win over a general one that also appears in the sentence.
RULES = [
    ('cons-1-8', 9, r'\b(safety|hazard|risk|ppe|personal protective|accident|'
                    r'injur|safe pass|trench|scaffold|working at height|dumper|'
                    r'safety statement|safety sign|first aid)\b'),
    ('cons-1-3', 9, r'\b(planning permission|site notice|site location|'
                    r'select(?:ing)? (?:a |your |the )?site|choice of site|'
                    r'preferred site|site a or b|building.{0,12}countryside)\b'),
    ('cons-1-2', 8, r'\b(planning authorit|conservation|refurbish|reuse of|'
                    r'protected structure|built environment|heritage)\b'),
    ('cons-1-9', 8, r'\b(building regulation|renewable energy ratio|\brer\b|'
                    r'fire test|part [a-l] of the building)\b'),
    ('cons-1-4', 8, r'\b(construction industry|skilled labour|qualified (?:trades|'
                    r'skilled)|occupation)\b'),
    ('cons-1-5', 7, r'\b(construction term|scale of 1:|standard symbol|notation|'
                    r'freehand sketch of a )\b'),
    ('cons-6-1', 9, r'\b(u-?value|thermal transmittance|thermal resistance|'
                    r'resistivity|heat loss calculation)\b'),
    ('cons-6-6', 9, r'\b(condensation|vapour (?:control|barrier)|interstitial|'
                    r'moisture control layer|breather membrane)\b'),
    ('cons-6-2', 8, r'\b(insulat|thermal bridge|cold bridge|airtight|air leakage|'
                    r'air.?tightness)\b'),
    ('cons-6-4', 8, r'\b(solar (?:gain|overheating|shading)|orientation|sun path|'
                    r'thermal mass|overheat)\b'),
    ('cons-6-5', 8, r'\b(ventilat|indoor air quality|human comfort|wellbeing|'
                    r'healthy indoor|humidity)\b'),
    ('cons-6-3', 6, r'\b(energy (?:use|demand|efficien|rating|upgrade)|\bber\b|'
                    r'passive house|retrofit|environmental impact|carbon|'
                    r'sustainab|running cost)\b'),
    ('cons-7-4', 8, r'\b(daylight|natural light|illuminat|glare|rooflight)\b'),
    ('cons-8-3', 8, r'\b(sound|acoustic|noise|reverberation|impact transmission)\b'),
    ('cons-2-4', 9, r'\b(strip foundation|raft|pad foundation|pile|foundation for)\b'),
    ('cons-2-2', 8, r'\b(foundation|excavat|subsoil|hardcore|bearing capacity)\b'),
    ('cons-2-6', 8, r'\b(concrete mix|batching|water.?cement|ready.?mix)\b'),
    ('cons-3-6', 9, r'\b(window (?:cill|sill|head|jamb|frame)|glazing|glass|'
                    r'window detail)\b'),
    ('cons-3-7', 9, r'\b(door (?:set|frame|threshold|schedule)|front door|'
                    r'ironmongery)\b'),
    ('cons-3-8', 9, r'\b(truss|rafter|wallplate|ridge|roof structure|roof form|'
                    r'purlin)\b'),
    ('cons-3-9', 8, r'\b(roof (?:finish|covering|insulation)|slate|tile|sarking|'
                    r'sloped ceiling|attic)\b'),
    ('cons-3-10', 8, r'\b(eaves|verge|abutment|flat roof|chimney|flashing|'
                    r'parapet|gutter at the eaves)\b'),
    ('cons-3-4', 8, r'\b(\bdpc\b|damp proof|lintel|arch|cavity (?:closer|tray)|'
                    r'rainwater at|ingress of (?:rain|water|moisture))\b'),
    ('cons-3-3', 6, r'\b(external wall|cavity wall|render|cladding|blockwork|'
                    r'wall tie|masonry|timber frame wall)\b'),
    ('cons-4-4', 9, r'\b(stair|riser|going|handrail|baluster|landing|headroom)\b'),
    ('cons-4-2', 8, r'\b(ground floor|solid floor|floor screed|screed|subfloor|'
                    r'floor finish|floor covering)\b'),
    ('cons-4-3', 8, r'\b(suspended (?:timber )?floor|joist|first floor|'
                    r'upper floor|strutting)\b'),
    ('cons-4-5', 8, r'\b(stud partition|internal wall|partition|dry lin)\b'),
    ('cons-4-6', 7, r'\b(plaster|paint|skim|decorat|surface finish|varnish|'
                    r'preserv)\b'),
    ('cons-5-2', 9, r'\b(hot water|cold water|cistern|cylinder|water meter|'
                    r'solar (?:collector|panel)|pipework)\b'),
    ('cons-5-3', 9, r'\b(heating system|radiator|heat pump|stove|boiler|'
                    r'underfloor heating|zoned heating|thermostat)\b'),
    ('cons-5-5', 9, r'\b(drainage|septic|wastewater|waste water|percolation|'
                    r'soakaway|surface water)\b'),
    ('cons-5-6', 8, r'\b(sanitary|toilet|\bwc\b|shower|bathroom|single stack)\b'),
    ('cons-5-7', 8, r'\b(fireplace|flue|hearth|chimney capping)\b'),
    ('cons-5-8', 9, r'\b(electric|wiring|socket|light point|circuit|'
                    r'distribution board|cabling|consumer unit)\b'),
    ('cons-5-4', 7, r'\b(rainwater (?:goods|pipe|harvest)|downpipe|eaves gutter)\b'),
    ('cons-9-4', 8, r'\b(workshop|power tool|edged tool|sharpen|grinding|'
                    r'machine guard)\b'),
    ('cons-10-1', 9, r'\b(mortice|tenon|dovetail|halving joint|housing joint|'
                     r'bridle joint|joint used|notched)\b'),
    ('cons-10-6', 8, r'\b(adhesive|glue|jig|cramp|holding work)\b'),
    ('cons-1-1', 3, r'\b(design|layout|appearance|aesthetic|proportion|'
                    r'vernacular|extension|room|kitchen|garden|porch|garage)\b'),
]
COMPILED = [(t, w, re.compile(p, re.I)) for t, w, p in RULES]


def topic_for(text):
    """(topic id, matched phrase) or (None, None) if nothing in the syllabus fits."""
    best = (0, None, None)
    for tid, weight, rx in COMPILED:
        m = rx.search(text or '')
        if m and weight > best[0]:
            best = (weight, tid, m.group(0))
    return best[1], best[2]


def concept_for(text, fallback='part'):
    """A slug from the question's own opening, for the card's concept id."""
    words = re.sub(r'[^a-z0-9 ]', ' ', (text or '').lower()).split()
    skip = {'using', 'notes', 'and', 'freehand', 'sketches', 'sketch', 'show',
            'discuss', 'in', 'detail', 'the', 'a', 'an', 'of', 'to', 'on',
            'your', 'drawing', 'describe', 'outline', 'state', 'give', 'each',
            'following', 'that', 'with', 'aid', 'draw', 'scale', 'for', 'two',
            'three', 'one', 'any', 'specify', 'suitable'}
    keep = [w for w in words if w not in skip and len(w) > 2][:6]
    return '-'.join(keep) or fallback
