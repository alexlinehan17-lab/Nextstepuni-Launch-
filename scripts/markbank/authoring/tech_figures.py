#!/usr/bin/env python3
"""Cut the picture a Technology ask points at, part by part.

    python3 scripts/markbank/authoring/tech_figures.py            # report
    python3 scripts/markbank/authoring/tech_figures.py --write    # render for review

Technology sets a photograph, a circuit or a flowchart BESIDE the prose and
then asks about it in a sentence that names nothing: "Name the type of gear
train shown in the image." A hundred and twelve census leaves are refused by
the authoring pass for exactly that -- they point at printed matter the card
cannot carry.

The geometry here is this subject's own, not Engineering's. Technology numbers
Section A's short questions in a LEFT GUTTER ("7." at x=46, its question at
x=58) and Sections B and C address every part as "2(a)" with no dot, so the
band a part owns is found from those markers rather than from "Question 4.".
Otherwise the argument is the same one eng_figures.py makes: a part owns the
vertical band between its own marker and the next, the artwork inside that
band is what the ask points at, and the crop is the union of that artwork with
whatever is printed on it.

WHAT IT REFUSES TO CUT, each because the alternative is a card showing the
wrong picture:

  * an answer box -- a ruled rectangle with nothing in it. It draws one stroke
    per line and counts as ink on every test that measures ink, and this
    subject prints one under nearly every short question;
  * a crop that reaches outside its own band;
  * a crop that swallows the ASK, which would show the student the question
    twice;
  * the page's own furniture: the SEC logo, the barcode, the header rules.

Every crop it makes is still opened and looked at before it is bound. The tool
finds candidates; it does not decide.
"""
import argparse
import json
import os
import re
import sys

import pymupdf

DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, DIR)
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(DIR)))
PAPERS = os.path.join(ROOT, 'examiner-reports', 'technology', 'papers')

import paper as PP                                           # noqa: E402
import paper_census as PC                                    # noqa: E402
import cardlint                                              # noqa: E402
import tech_all as TA                                        # noqa: E402
from tech_scheme import TechScheme                           # noqa: E402

# The page's own furniture, measured on the pages rather than assumed. A
# question's first line sits at y=38 and the running footer starts at y=766 of
# an 842-point page, so a header band of 92 -- Engineering's -- swallowed the
# head of every question on every page and the bands came out one question out
# of step.
HEADER = 30.0
FOOTER = 85.0

A_MARK = re.compile(r'^(\d{1,2})\.(?:\s|$)')
BC_MARK = re.compile(r'^(\d{1,2})\(([a-d])\)')
ROMAN_MARK = re.compile(r'^\((i{1,3}|iv|v)\)')
OPTION_MARK = re.compile(r'^Option\s+(\d)\b')
QUESTION_MARK = re.compile(r'^Question\s+(\d{1,2})\b')
SECTION_MARK = re.compile(r'^Section\s+([ABC])\b')

# An instruction, as opposed to a caption. A caption belongs with the picture;
# an ask belongs on the card as text, and a crop carrying it shows the student
# the question twice.
ASK_LINE = re.compile(
    r'^\(?[a-z0-9]{0,3}\)?\s*(?:briefly\s+)?(?:calculate|compare|complete'
    r'|define|describe|determine|differentiate|discuss|distinguish|draw'
    r'|explain|give|identify|indicate|label|list|name|outline|redraw|sketch'
    r'|state|suggest|show|answer|select|using|use|what|why|write)\b', re.I)


# WHAT WAS SEEN. Every crop below was rendered at 200 dpi and opened. The
# accepted ones carry the description that ships as the figure's alt text; the
# rejected ones name what is wrong with them, so a later run cannot quietly
# publish a crop a person has already turned down.
#
# The commonest fault by far is a crop that reaches across the page and takes
# the ask with it. Technology sets its short questions as a two-column spread
# -- prose and answer boxes on the left, the picture on the right -- and where
# the picture's own columns overlap the prose's, the rectangle cannot separate
# them. Those are refused, not trimmed.
REVIEWED = {
    'technology-2021-HL-paper-secA-q4-art':
        'Colour photograph of a mechanic using a digital torque wrench on a V8 '
        'engine cylinder head. A red double-headed arrow runs along the length '
        'of the wrench between two white end bars and is labelled X.',
    'technology-2021-HL-paper-secA-q5-art':
        'Rendered image of a face shield worn on a grey mannequin head: a blue '
        'headband with side pivots holds a clear transparent visor that covers '
        'the face from forehead to chin.',
    'technology-2021-HL-paper-secA-q9-art':
        'A four-column table headed Category, Material, Electrical Property '
        'and Use. The Conductor row is filled in with Copper, "Allows current '
        'to pass through" and Electrical wire; the Insulator and '
        'Semiconductor rows are blank.',
    'technology-2021-HL-paper-secA-q10-art':
        'Colour photograph of an industrial gearbox with its blue cast housing '
        'cut away, showing a train of steel spur gears of different diameters '
        'on parallel shafts, with the output shaft projecting to the right.',
    'technology-2021-HL-paper-secA-q13-art':
        'Exploded pictorial view of a handheld games console in teal green: '
        'from the top, the front casing with screen aperture and button holes, '
        'the printed circuit board, the button and joypad assembly, the rear '
        'casing, a cylindrical battery and the battery cover.',
    'technology-2021-HL-paper-secA-q15-art':
        'Black-and-white line drawing of a desk stapler in pictorial view, '
        'showing the hinged top arm, the magazine body and the flat base with '
        'its anvil.',
    'technology-2021-OL-paper-secB-q2d-art':
        'Colour photograph of four identical flat-pack cardboard cartons '
        'standing upright on a steel bench, with a person reaching between two '
        'of them.',
    'technology-2022-HL-paper-secA-q2-art':
        'The EU rescaled energy label for a Samsung television: the ENERGY '
        'heading with a QR code, the A-to-G coloured arrow scale with a black '
        'G marker, 98 kWh/1000h for standard mode, a second HDR panel reading '
        '112 kWh/1000h, and a screen-size diagram giving 3840 x 2160 px and a '
        '108 cm (43 inch) diagonal.',
    'technology-2022-HL-paper-secA-q8-art':
        'Exploded pictorial view of a castor wheel assembly, its parts '
        'numbered 1 to 5 with leader lines: the top mounting plate (1), the '
        'axle bolt (2), two side brackets (3), two bearing washers (4) and the '
        'wheel itself (5).',
    'technology-2022-HL-paper-secA-q9-art':
        'Two colour photographs side by side: on the left a hard disk drive '
        'with its cover removed, showing the gold platter, spindle and read '
        'head arm; on the right a solid-state drive with its case partly open, '
        'showing the memory chips on the circuit board.',
    'technology-2022-HL-paper-secC-q2a-art':
        'Colour photograph of a small push-type solenoid: a plated steel frame '
        'holding a blue-wrapped coil, with a cylindrical plunger projecting '
        'from the left face and red and black flying leads with a white '
        'connector at the top.',
    'technology-2022-OL-paper-secC-q2d-art':
        'A logic circuit diagram drawn with two gates. Inputs A and B enter an '
        'OR gate labelled X; its output, labelled C, feeds a NOT gate '
        '(inverter) labelled Y, whose output is labelled D.',
    'technology-2022-OL-paper-secC-q4a-art':
        'Colour photograph of corrugated cardboard packaging: a stack of flat '
        'die-cut carton blanks behind three small assembled cube-shaped boxes, '
        'one of them open.',
    'technology-2022-OL-paper-secC-q5b-art':
        'Colour photograph of a prefabricated timber-framed facade panel with '
        'a window and cladding being craned into place on a partly built '
        'timber-frame building. The panel is labelled A and the concrete floor '
        'slab beneath it is labelled B; two workers in helmets and harnesses '
        'guide it in.',
    'technology-2023-HL-paper-secA-q9-art':
        'Line drawing of a three-blade horizontal-axis wind turbine, drawn in '
        'a ruled box. Leader lines label the rotor blades as Rotor, the housing '
        'behind the hub as Nacelle (contains gears and generator), and the mast '
        'as Cylindrical tower.',
    'technology-2023-HL-paper-secA-q10-art':
        'Diagram of a compound gear train of four spur gears. Gear A, the '
        'driver, has 8 teeth and turns at 450 RPM; it meshes with Gear B, 24 '
        'teeth; Gear C, 8 teeth, shares B\'s shaft and meshes with Gear D, 24 '
        'teeth. Each gear is named by a red leader line.',
    'technology-2023-HL-paper-secA-q11-art':
        'Colour photograph of a white vented cycling helmet with a black rear '
        'section, an action camera strapped to the top of it by a black '
        'harness.',
    'technology-2023-HL-paper-secC-q2b-art':
        'A circuit diagram between +9 V and 0 V rails. A switch feeds two '
        'potential-divider branches: component A, a variable resistor, in '
        'series with a 10 kilohm resistor, and component B, a thermistor, in '
        'series with a second 10 kilohm resistor. The two junctions feed the '
        'inverting and non-inverting inputs of an IC comparator, whose output '
        'drives a resistor, a transistor and a buzzer back to the 0 V rail.',
    'technology-2023-OL-paper-secC-q2c-art':
        'Colour photograph of a black aluminium LED pocket torch lying at an '
        'angle, with a knurled grip band, a pocket clip and a reflector lens '
        'at the left end.',
    'technology-2024-HL-paper-secA-q4-art':
        'Colour photograph of a small Fender practice guitar amplifier: a '
        'black cabinet with a silver grille cloth, a carrying handle and a row '
        'of control knobs and input sockets across the top panel.',
    'technology-2024-HL-paper-secA-q5-art':
        'A carbon-film resistor photographed at an angle beside the caption '
        '"Resistor bands:" and the list Brown, Black, Red, Gold, which are the '
        'four bands printed on it from left to right.',
    'technology-2024-HL-paper-secA-q6-art':
        'A network-diagram node drawn as a six-cell box: the top row is '
        'labelled EST on the left and EFT on the right, the middle row is a '
        'blank cell labelled Task:, and the bottom row is labelled LST on the '
        'left and LFT on the right.',
    'technology-2024-HL-paper-secA-q8-art':
        'Exploded pictorial view of a garden lantern, its parts spaced out '
        'vertically: the wire carrying handle, a small finial, the domed green '
        'top cover, the yellow cylindrical glass shade, a green collar, a grey '
        'cylindrical candle unit and the domed green base.',
    'technology-2024-HL-paper-secA-q13-art':
        'Two images joined by an arrow: on the left a square side table with a '
        'black top and a chrome tubular frame; on the right, at the end of the '
        'arrow, a smartphone lying on that black surface showing a green '
        'charging indicator.',
    'technology-2024-HL-paper-secC-q2b-art':
        'The pin layout of an eight-pin integrated circuit drawn as a plain '
        'rectangle with four leads on each side. The pin numbers read 7, 4 and '
        '8 across the top, 6 and 3 in the middle, and 2, 1 and 5 across the '
        'bottom.',
    'technology-2024-HL-paper-secC-q5d-art':
        'Colour photograph of a transparent rigid plastic punnet of '
        'strawberries with a hinged clip-shut lid.',
    'technology-2024-OL-paper-secC-q1d-art':
        'The pneumatic symbol for a double-acting cylinder: a rectangular '
        'barrel containing a piston and a piston rod that passes out through '
        'the right-hand end, with hatching drawn inside the barrel and a port '
        'stub beneath the left-hand end.',
    'technology-2025-HL-paper-secA-q4-art':
        'Colour photograph of five capacitors standing side by side: a large '
        'black 1000 microfarad 50 V electrolytic can, two orange disc '
        'capacitors, a red boxed 104K 250 V film capacitor and a blue 10 '
        'microfarad 35 V electrolytic, each with two wire legs.',
    'technology-2025-HL-paper-secA-q5-art':
        'Illustration of a yellow mobile crane with its telescopic boom raised '
        'to the left, its hook carrying a pale trapezoidal load labelled '
        '1200 N.',
    'technology-2025-HL-paper-secA-q8-art':
        'Outline line drawing of a games controller, drawn in a ruled box: the '
        'symmetrical body with two shoulder buttons, a left thumbstick and a '
        'four-way directional pad on the left, minus and plus buttons and two '
        'small buttons in the centre, and four round face buttons with a right '
        'thumbstick on the right.',
    'technology-2025-HL-paper-secA-q11-art':
        'Colour rendering of a park bench with white precast concrete end legs '
        'and armrests and horizontal timber slats forming the seat and the '
        'backrest.',
    'technology-2025-HL-paper-secA-q13-art':
        'Rendered diagram of a diving springboard in a ruled box. A leader '
        'line labels the tubular handrail assembly Ladder and the blue board '
        'Springboard, and an angle drawn between the board and its fulcrum '
        'mounting is labelled Tilt Angle.',
}

# Looked at and turned down, with what is wrong with each.
REJECTED = {
    'technology-2021-OL-paper-secA-q12-art': 'the juicer drawing is cut off along its bottom edge',
    'technology-2022-HL-paper-secA-q10-art': 'only the header row of the risk-assessment table; its rows are cut off',
    'technology-2022-HL-paper-secA-q5-art': 'carries both asks and their answer boxes',
    'technology-2022-HL-paper-secA-q6-art': 'carries the second ask and the answer boxes',
    'technology-2022-OL-paper-secA-q11-art': 'carries the second ask and the answer boxes',
    'technology-2022-OL-paper-secA-q6-art': 'carries both asks and their answer boxes',
    'technology-2022-OL-paper-secA-q8-art': 'carries the ask above the work breakdown structure',
    'technology-2022-OL-paper-secB-q3b-art': 'the arrow points to a label outside the crop',
    'technology-2023-HL-paper-secA-q2-art': 'carries both asks and their answer boxes',
    'technology-2023-HL-paper-secA-q4-art': 'carries both asks and their answer boxes',
    'technology-2023-HL-paper-secA-q8-art': 'the fishbone diagram is cut off along its left edge',
    'technology-2023-HL-paper-secB-q2c-art': 'the lifecycle graph is cut off; neither axis label survives',
    'technology-2023-HL-paper-secC-q4d-art': 'the last row of the assembly sequence is clipped',
    'technology-2023-OL-paper-secA-q1-art': 'carries the second ask and the answer blanks',
    'technology-2024-HL-paper-secA-q3-art': 'clips a line of the ask along its bottom edge',
    'technology-2024-HL-paper-secC-q2d-art': 'the gate inputs and the output label are cut off',
    'technology-2024-OL-paper-secA-q1-art': 'carries both asks and their answer boxes',
    'technology-2024-OL-paper-secA-q6-art': 'carries the second ask and the answer boxes',
    'technology-2024-OL-paper-secA-q8-art': 'carries both asks and their answer boxes',
    'technology-2024-OL-paper-secB-q3c-art': 'clips a ruled line of the ask along its top edge',
    'technology-2025-HL-paper-secB-q3b-art': 'the leader arrows point to labels outside the crop',
    'technology-2025-OL-paper-secA-q1-art': 'carries both asks and their answer boxes',
    'technology-2025-OL-paper-secA-q11-art': 'carries both asks and their answer boxes',
    'technology-2025-OL-paper-secA-q3-art': 'carries both asks and their answer boxes',
}


def lines(page):
    out = []
    for block in page.get_text('dict')['blocks']:
        for line in block.get('lines', []):
            text = ' '.join(PP._repair(
                ''.join(s['text'] for s in line['spans']), 'technology').split())
            if text:
                out.append((line['bbox'], text))
    out.sort(key=lambda r: (round(r[0][1], 1), r[0][0]))
    return out


def artwork(page):
    """Every picture on the page: raster images and drawn shapes alike.

    Technology draws as often as it photographs -- a circuit, a flowchart, a
    gear train -- and a drawing has no image rect at all.
    """
    out = []
    for im in page.get_images(full=True):
        for r in page.get_image_rects(im[0]):
            out.append((r.x0, r.y0, r.x1, r.y1))
    for d in page.get_drawings():
        r = d['rect']
        if r.width > 16 and r.height > 16:
            out.append((r.x0, r.y0, r.x1, r.y1))
    return [a for a in out
            if a[1] > HEADER and a[3] < page.rect.height - FOOTER
            and a[2] - a[0] > 22 and a[3] - a[1] > 22]


def is_answer_box(page, rect):
    """A ruled box the candidate writes in, which is not a picture."""
    x0, y0, x1, y1 = rect
    inside = [t for (bx0, by0, bx1, by1), t in lines(page)
              if x0 - 2 < bx0 and bx1 < x1 + 2 and y0 - 2 < by0 and by1 < y1 + 2
              and len(t) > 2]
    # A ruled box whose only content is its own prompt -- "Calculation:",
    # "Answer:" -- is where the candidate writes, not a picture. It has no
    # rules inside it at all, so the stroke test below never sees it, and it
    # shipped beside the torque-wrench photograph as half the crop.
    if inside and all(re.fullmatch(r'[^.?!]{1,24}:', t.strip()) for t in inside):
        return True
    if inside:
        return False
    rules = [d['rect'] for d in page.get_drawings()
             if d['rect'].width > (x1 - x0) * 0.6 and d['rect'].height < 3
             and x0 - 4 < d['rect'].x0 and d['rect'].x1 < x1 + 4
             and y0 - 4 < d['rect'].y0 and d['rect'].y1 < y1 + 4]
    return len(rules) >= 3


def page_bands(page, state, seen_here):
    """[(section, q, letter, top, bottom)] for every part opened on this page.

    `state` carries (section, q, letter) across the page break, because a
    question runs over pages and prints its address only once. `seen_here` is
    the set of sections that have actually opened a part, which is what stops
    the cover page's own contents list ("Section B ... Section C ...") walking
    the tracker to C before the paper has begun -- with that, every Section A
    band on every Higher paper was filed under Section C and matched nothing.
    """
    section, q, letter = state
    opened = []
    for (bx0, by0, bx1, by1), text in lines(page):
        if by0 < HEADER or by1 > page.rect.height - FOOTER:
            continue
        sm = SECTION_MARK.match(text)
        if sm and len(text) < 90 and sm.group(1) > section \
                and section in seen_here:
            section, q, letter = sm.group(1), None, None
            continue
        om = OPTION_MARK.match(text)
        if om:
            q, letter = int(om.group(1)), None
            continue
        qm = QUESTION_MARK.match(text)
        if qm:
            q, letter = int(qm.group(1)), None
            continue
        bm = BC_MARK.match(text)
        if bm:
            q, letter = int(bm.group(1)), bm.group(2)
        else:
            am = A_MARK.match(text)
            # A gutter number, and only a gutter number: the answerbook's
            # ruled lines and a numbered list inside an answer are set in the
            # body column, so the left margin separates a head from them.
            if not (am and bx0 < 80):
                continue
            q, letter = int(am.group(1)), None
        opened.append((by0, section, q, letter))
        seen_here.add(section)
    out = []
    for i, (y, sec, qq, le) in enumerate(opened):
        bottom = opened[i + 1][0] if i + 1 < len(opened) else \
            page.rect.height - FOOTER
        out.append((sec, qq, le, y - 4, bottom))
    return out, (section, q, letter)


def crop_for(paths, section, q, letter):
    """(pdf path, page number, rect) for the picture this part points at."""
    for path in paths:
        # The booklet says which section it is: 014 carries Section A, 039
        # Sections B and C. Reading it off the page instead let the cover's
        # own contents list ("Section B ... Section C ...") walk the tracker
        # to C before the paper began, and every Section A band was filed
        # under C.
        opening = 'A' if '-014-' in os.path.basename(path) else 'B'
        with pymupdf.open(path) as doc:
            state, seen_here = (opening, None, None), set()
            for n in range(doc.page_count):
                page = doc[n]
                bands, state = page_bands(page, state, seen_here)
                for sec, qq, le, top, bottom in bands:
                    if (sec, qq, le) != (section, q, letter):
                        continue
                    art = [a for a in artwork(page)
                           if a[1] >= top - 6 and a[3] <= bottom + 6
                           and not is_answer_box(page, a)]
                    if not art:
                        continue
                    x0 = min(a[0] for a in art)
                    y0 = min(a[1] for a in art)
                    x1 = max(a[2] for a in art)
                    y1 = max(a[3] for a in art)
                    if (x1 - x0) < 46 or (y1 - y0) < 34:
                        continue
                    # The crop is X-BOUNDED to the artwork's own columns, and
                    # grows only into lines that sit INSIDE those columns --
                    # the labels printed on the picture. Technology sets the
                    # picture beside the prose, so a crop that grows into
                    # every line it touches reaches across the page and takes
                    # the question with it: fifteen crops came back carrying
                    # their own ask, which shows the student the question
                    # twice.
                    for _ in range(6):
                        grew = False
                        for (bx0, by0, bx1, by1), t in lines(page):
                            if bx1 <= x0 or bx0 >= x1 or by1 <= y0 or by0 >= y1:
                                continue
                            if x0 - 1 <= bx0 and bx1 <= x1 + 1 \
                                    and y0 - 1 <= by0 and by1 <= y1 + 1:
                                continue
                            if bx0 < x0 - 2 or bx1 > x1 + 2:
                                continue          # reaches out of the columns
                            y0, y1 = min(y0, by0), max(y1, by1)
                            grew = True
                        if not grew:
                            break
                    # Rendering shows whatever the rectangle covers, so a line
                    # still crossing it has to be got out of the way. The
                    # prose column runs BESIDE the picture and its first or
                    # last line often reaches into the picture's top or bottom
                    # corner -- "The torque wrench shown is set to deliver a
                    # torque of 206 Nm." crosses the photograph's own band --
                    # so the box is clipped back off it. A line crossing the
                    # MIDDLE cannot be clipped away, and that crop is refused.
                    art_top = min(a[1] for a in art)
                    art_bottom = max(a[3] for a in art)
                    for _ in range(4):
                        crossing = None
                        for (bx0, by0, bx1, by1), t in lines(page):
                            if bx1 <= x0 + 1 or bx0 >= x1 - 1 \
                                    or by1 <= y0 + 1 or by0 >= y1 - 1:
                                continue
                            if x0 - 2 <= bx0 and bx1 <= x1 + 2 \
                                    and y0 - 2 <= by0 and by1 <= y1 + 2:
                                continue
                            crossing = (by0, by1)
                            break
                        if crossing is None:
                            break
                        by0, by1 = crossing
                        mid = (y0 + y1) / 2
                        if by1 <= mid:
                            y0 = by1 + 1
                        elif by0 >= mid:
                            y1 = by0 - 1
                        else:
                            return None
                    else:
                        return None
                    # What survives has to still BE the picture, not a strip
                    # of it: the clip may take the labels, never the artwork.
                    if y0 > art_top + 4 or y1 < art_bottom - 4:
                        return None
                    if (x1 - x0) < 46 or (y1 - y0) < 34:
                        return None
                    if y1 - y0 > page.rect.height * 0.66:
                        return None
                    if y0 < top - 8 or y1 > bottom + 8:
                        return None
                    return path, n, (x0 - 4, y0 - 4, x1 + 4, y1 + 4)
    return None


def crop_text(path, page, rect):
    with pymupdf.open(path) as doc:
        return PP._repair(doc[page].get_textbox(pymupdf.Rect(*rect)), 'technology')


def faults(path, page, rect, ask):
    """What the crop is warned about, for the reviewer's eye.

    get_textbox reports any character the rectangle so much as touches, which
    is a looser test than the line-bbox geometry crop_for already applies, so
    this is a WARNING and not a refusal: every crop is opened and looked at
    before it is bound, and a warning that refused the crop outright took
    thirteen correct pictures off the worklist before anyone saw them.
    """
    text = crop_text(path, page, rect)
    bad = []
    for line in text.split('\n'):
        t = ' '.join(line.split())
        if len(t) > 40 and len(t.split()) > 6 and ASK_LINE.match(t):
            bad.append(f'may carry the ask: {t[:44]!r}')
            break
    return bad


def key_for(year, level, section, q, letter):
    return (f'technology-{year}-{level.upper()}-paper-sec{section}-q{q}'
            + (letter or '') + '-art')


def worklist():
    """Every card the authoring pass refuses for pointing at printed matter.

    Read from tech_all's own verdicts rather than re-derived, so the cropper's
    worklist and the author's refusals cannot drift: a crop for a part nobody
    is refusing helps no one, and a refusal the cropper never hears about is a
    card that stays lost.
    """
    cards, refused, examples, verdicts, stats = TA.author()
    want = []
    for v in verdicts:
        if v['reason'] != 'points at printed matter the card cannot carry':
            continue
        m = re.match(r'(\d{4}) (HL|OL) Section ([ABC]) Q(\d{1,2})(?:\(([a-d])\))?',
                     v['ref'])
        if m:
            want.append((int(m.group(1)), m.group(2).lower(), m.group(3),
                         int(m.group(4)), m.group(5)))
    # One crop per PART, not per roman: the picture is printed once and every
    # roman under it shows the same one.
    seen, out = set(), []
    for item in want:
        if item not in seen:
            seen.add(item)
            out.append(item)
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--write', action='store_true',
                    help='render every crop for review')
    ap.add_argument('--publish', action='store_true',
                    help='write the REVIEWED crops where bind-figures reads '
                         'them, with the catalogue')
    ap.add_argument('--dir', default=os.path.join(ROOT, 'figures-review-technology'))
    args = ap.parse_args()

    if args.write:
        os.makedirs(args.dir, exist_ok=True)
    cut, missed, warned = [], [], []
    seen = {}
    for year, level, section, q, letter in worklist():
        paths = sorted(
            os.path.join(PAPERS, f)
            for f in os.listdir(PAPERS)
            if re.fullmatch(rf'{year}-{level}(-\d+)?-paper\.pdf', f))
        got = crop_for(paths, section, q, letter)
        if not got:
            missed.append((year, level, section, q, letter))
            continue
        path, page, rect = got
        bad = faults(path, page, rect, '')
        if bad:
            warned.append((year, level, section, q, letter, bad[0]))
        stamp = (os.path.basename(path), page, tuple(round(v) for v in rect))
        if stamp in seen:
            cut.append((year, level, section, q, letter, seen[stamp], rect,
                        True, path, page))
            continue
        key = key_for(year, level, section, q, letter)
        seen[stamp] = key
        if args.write:
            with pymupdf.open(path) as doc:
                doc[page].get_pixmap(clip=pymupdf.Rect(*rect), dpi=200).save(
                    os.path.join(args.dir, f'{key}.png'))
        cut.append((year, level, section, q, letter, key, rect, False, path, page))

    fresh = [c for c in cut if not c[7]]
    unreviewed = [c[5] for c in fresh
                  if c[5] not in REVIEWED and c[5] not in REJECTED]
    print(f'{len(fresh)} crops for {len(cut)} parts; {len(missed)} with nothing '
          f'to cut; {len(warned)} warned')
    print(f'{sum(1 for c in fresh if c[5] in REVIEWED)} accepted after review, '
          f'{sum(1 for c in fresh if c[5] in REJECTED)} rejected after review, '
          f'{len(unreviewed)} NOT YET LOOKED AT')
    for key in unreviewed:
        print(f'   UNREVIEWED {key}')
    for w in warned:
        print(f'   WARN    {w[0]} {w[1].upper()} {w[2]}Q{w[3]}{w[4] or ""} — {w[5]}')
    for m in missed:
        print(f'   nothing  {m[0]} {m[1].upper()} {m[2]}Q{m[3]}{m[4] or ""}')

    if args.publish:
        if unreviewed:
            print('refusing to publish: some crops have not been looked at')
            return 1
        catalogue = []
        for year, level, section, q, letter, key, rect, shared, path, page in fresh:
            if key not in REVIEWED:
                continue
            dest = os.path.join(ROOT, 'exam-papers', 'technology', 'figures',
                                f'{year}-{level}')
            os.makedirs(dest, exist_ok=True)
            with pymupdf.open(path) as doc:
                doc[page].get_pixmap(clip=pymupdf.Rect(*rect), dpi=200).save(
                    os.path.join(dest, f'{key}.png'))
            catalogue.append({
                'file': f'{key}.png', 'kind': 'figure', 'truncated': False,
                'description': REVIEWED[key],
                'questionRef': (f'{year} {level.upper()} Section {section} '
                                f'Q{q}' + (f'({letter})' if letter else '')),
            })
        out = os.path.join(ROOT, 'scripts', 'markbank', 'authored',
                           'technology-figures.json')
        with open(out, 'w', encoding='utf-8') as fh:
            json.dump(catalogue, fh, ensure_ascii=False, indent=1)
        print(f'wrote {out}: {len(catalogue)} inspected crops')
    if args.write:
        with open(os.path.join(args.dir, 'crops.json'), 'w') as fh:
            json.dump([{'year': c[0], 'level': c[1], 'section': c[2], 'q': c[3],
                        'letter': c[4], 'key': c[5],
                        'rect': [round(v, 1) for v in c[6]], 'shared': c[7]}
                       for c in cut], fh, indent=1)
        print(f'wrote {args.dir}')
    return 0


if __name__ == '__main__':
    sys.exit(main())
