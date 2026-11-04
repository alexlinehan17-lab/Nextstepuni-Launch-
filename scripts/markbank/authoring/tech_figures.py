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
import tech_crops as TC                                      # noqa: E402

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
    'technology-2022-HL-paper-secA-q15-art':
        'Outline line drawing of a handheld cordless vacuum cleaner in '
        'pictorial view, drawn unshaded in a ruled box: the tapered nozzle and '
        'dust bowl at the front, the body with its switch and slide control, '
        'and the loop handle at the rear.',
    'technology-2022-OL-paper-secA-q12-art':
        'Outline line drawing of a USB flash drive in pictorial view, drawn '
        'unshaded in a ruled box, with its cap lying separately to the right '
        'and the metal connector exposed.',
    'technology-2023-OL-paper-secA-q12-art':
        'Outline line drawing of an electric kettle in pictorial view, drawn '
        'unshaded in a ruled box: the tapered jug with its spout, hinged lid, '
        'handle and water-level window, standing on its power base.',
    'technology-2024-OL-paper-secA-q12-art':
        'Outline line drawing of an angle-poise desk lamp in pictorial view, '
        'drawn unshaded in a ruled box: the conical shade, the two-part '
        'jointed arm and the weighted domed base.',
    'technology-2025-OL-paper-secA-q12-art':
        'Line drawing of a disposable takeaway coffee cup, drawn in outline on '
        'a lightly hatched square inside a ruled box: a domed lid with a '
        'drinking hole, a sleeve carrying a coffee-bean motif, and the tapered '
        'cup below it.',
    'technology-2022-OL-paper-secA-q6-art':
        'Colour photograph of a pair of blue plastic bevel gears in mesh: a '
        'small pinion standing at right angles above a much larger bevel wheel '
        'with a keyed centre bore.',
    'technology-2022-OL-paper-secA-q11-art':
        'A circuit diagram: a battery, a single-pole switch, a resistor '
        'labelled R and a light emitting diode with two emission arrows, all '
        'in one series loop.',
    'technology-2022-OL-paper-secC-q1b-art':
        'Colour photograph of a robotic deck-cleaning machine in side view: a '
        'low black wedge-shaped body with a vented top, running on wheels over '
        'timber decking, with a rotary brush turning underneath its front.',
    'technology-2023-HL-paper-secA-q2-art':
        'Colour photograph of a table lamp made from three upright copper '
        'pipes of different heights set into a solid timber base, each pipe '
        'topped with a brass lampholder and an exposed-filament bulb.',
    'technology-2023-HL-paper-secA-q4-art':
        'Pictorial drawing of a single-digit seven-segment LED display: a '
        'black rectangular body with all seven red segments and the decimal '
        'point lit, and five connection pins projecting from each long side.',
    'technology-2023-OL-paper-secC-q5b-art':
        'Colour photograph looking up at a suspension bridge from beneath. A '
        'red leader line labels the thin hangers running down from the main '
        'cable as Vertical cables, and a second labels the roadway box girder '
        'as Deck; a tower stands in the water in the background.',
    'technology-2025-OL-paper-secA-q11-art':
        'Rendered pictorial view of a chain drive: a small toothed sprocket '
        'above and a much larger toothed sprocket below, both with keyed '
        'bores, joined by a roller chain running around them.',
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
        'A circuit diagram of a 555 timer between two supply rails: R1 and R2 in series from the top rail to pins 7 and 6/2, a capacitor C from pin 2 to the bottom rail, pins 4 and 8 to the top rail, pin 1 to the bottom rail and the output at pin 3.',
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
    # 2026 Higher: the rectangles are tech_crops.BY_EYE, each measured on the
    # rendered page and opened at 150 dpi before it was written down.
    'technology-2026-HL-paper-secA-q3-art':
        'A circuit diagram: a 12V battery feeding two 10 Ω resistors in '
        'series, with a 40 Ω resistor and a voltmeter V in parallel with each '
        'other between them.',
    'technology-2026-HL-paper-secA-q8-art':
        'Outline line drawing of a cordless drill in pictorial view, drawn '
        'unshaded in a ruled box: the chuck and bit at the front, the motor '
        'body, the pistol grip with its trigger, and the battery pack below.',
    'technology-2026-HL-paper-secA-q9-art':
        'A lever diagram: a horizontal bar on a triangular fulcrum at its left '
        'end, a 250 N load 50 mm from the fulcrum, and an upward effort arrow '
        '200 mm beyond the load at the right end.',
    'technology-2026-HL-paper-secA-q10-art':
        'Colour photograph of a hand holding a blue jigsaw by its handle, the '
        'blade below the base plate, with a red double-headed arrow along the '
        'blade showing its up-and-down motion.',
    'technology-2026-HL-paper-secA-q11-art':
        'A fishbone (cause and effect) diagram: a grey fish skeleton with four '
        'cause boxes on its ribs labelled People, Material, Method and '
        'Environment, each with an empty dashed box beside it except Material, '
        'whose box reads Oxidised.',
    'technology-2026-HL-paper-secA-q13-art':
        'Two panels: on the left a ruled drawing box with a black dot at the '
        'crossing of two dashed centre lines; on the right a colour photograph '
        'of a wooden fishing automaton, a seated figure holding a rod over a '
        'wave, labelled Fishing rod, Drive shaft, Cam and Handle.',
    'technology-2026-HL-paper-secA-q15-art':
        'Colour photograph of a child\u2019s climbing arch: a curved wooden '
        'frame with a round hand-hole at each foot and pastel-coloured rungs '
        'across the top.',
    'technology-2026-HL-paper-secC-q2b-art':
        'An op-amp circuit diagram: a triangle labelled IC with inverting (-) '
        'and non-inverting (+) inputs on the left, between an upper and a lower '
        'supply rail, with the output to the right and no components fitted.',
    'technology-2026-HL-paper-secC-q4b-art':
        'A two-row table: Day 1 to 12 across the top and Defects 2, 3, 4, 5, '
        '3, 2, 6, 4, 3, 7, 5, 4 beneath.',
    'technology-2026-HL-paper-secC-q5b-art':
        'Colour photograph of a petrol multi-function gardening tool, the '
        'engine at the top of a long shaft, with an inset of its orange '
        'strimmer head labelled Safety guard by a red arrow.',
    'technology-2026-HL-paper-secC-q5c-art':
        'Three colour photographs of the gardening tool\u2019s modular heads: '
        'a hedge-trimmer blade, a chainsaw bar and the orange strimmer head.',
    # In-window parts, 2026-10-28: the cropper's own cuts, looked at.
    'technology-2022-HL-paper-secC-q2b-art':
        'A circuit diagram between +V and -V rails: a variable resistor A above '
        'a thermistor B form a potential divider feeding a transistor through a '
        'resistor; a push switch C and the transistor output feed an OR gate D '
        'that drives a buzzer.',
    'technology-2022-OL-paper-secC-q2b-art':
        'A circuit diagram between 6V and 0V rails with a switch in the top '
        'rail: a variable resistor A above a thermistor B form a potential '
        'divider feeding a transistor through a resistor, with a buzzer C in '
        'the collector line.',
    'technology-2023-OL-paper-secC-q2b-art':
        'Colour photograph of a red miniature toggle switch with six pins, '
        'above its circuit symbol: a double-pole double-throw switch drawn as '
        'two linked blades each able to meet either of two contacts.',
    'technology-2023-OL-paper-secC-q4b-art':
        'Colour photograph of a white S-Works road bicycle with deep-section '
        'black wheels, standing on a road in front of desert hills.',
    'technology-2024-HL-paper-secC-q4b-art':
        'Colour photograph of three laser-cut plywood trophies, each a '
        'latticed football on a tapered tower bearing a Fantasy Champion 2017 '
        'shield.',
    'technology-2025-HL-paper-secC-q4b-art':
        'A cost graph: cost from 0 to 8000 against Quantity from 0 to 400, a '
        'steep blue line A from the origin and a shallower red line B from '
        '3000, crossing at point C above 200, with the region X between them '
        'before C shaded green and the region Y after it shaded pink.',
    # 2020 Higher (2026-10-28): the cropper's cuts, and by-eye rects for the rest.
    'technology-2020-HL-paper-secA-q4-art':
        'Colour photograph of a worm and worm wheel in a blue housing, the '
        'steel worm above meshing with the brass wheel below.',
    'technology-2020-HL-paper-secA-q7-art':
        'Colour photograph of a clear acrylic table menu holder, a folded '
        'sheet forming an upright sleeve on a flat base.',
    'technology-2020-HL-paper-secA-q10-art':
        'A table headed Part, Material and Reason for choice of material, with '
        'rows Composite layer (filled in: Fibreglass, Strong/flexible material), '
        'Wooden core, Metal edge and Plastic coversheet left blank.',
    'technology-2020-HL-paper-secA-q13-art':
        'Colour photograph of an LED bulb in exploded view: the frosted dome, '
        'the LED board, the finned heatsink body with its driver and the '
        'screw cap, stacked apart vertically.',
    'technology-2020-HL-paper-secA-q15-art':
        'Outline line drawing of an all-in-one printer in pictorial view: the '
        'document feeder on top, the control panel at the front right and the '
        'paper tray below.',
    'technology-2020-HL-paper-secB-q2b-art':
        'Colour photograph of the Lightcycle lamp, a tall white post with a '
        'horizontal arm, arrows A (vertical, at the arm) and B (rotation, at '
        'the base), with a circle marking the joint.',
    'technology-2020-HL-paper-secB-q2b-ii-art':
        'Close-up inset of the lamp\u2019s roller-and-groove joint, a roller '
        'running in a slotted channel, cut at its left edge where the prose '
        'column runs into it.',
    'technology-2020-HL-paper-secB-q3b-art':
        'Colour photograph of a food processor drive unit: a motor with two '
        'white gears labelled A and B, captioned Each gear has 50 teeth and '
        'Food processor drive unit.',
    'technology-2020-HL-paper-secB-q3c-art':
        'Colour photograph of a red and silver hand blender standing upright, '
        'its cable coiled beside the handle.',
    'technology-2020-HL-paper-secB-q3d-art':
        'Two photographs of food boxes: Box A, a clamshell made from expanded '
        'polystyrene, and Box B, a red folding carton made from cardboard, '
        'each captioned.',
    'technology-2020-HL-paper-secC-q1d-art':
        'Colour photograph of a sheet metal cutter with a double acting '
        'pneumatic cylinder mounted on top, labelled by an arrow.',
    'technology-2020-HL-paper-secC-q2b-art':
        'An incomplete op-amp circuit between +9 V and 0 V rails: a 66 kΩ and '
        'a 33 kΩ resistor in series as a potential divider to point A on the '
        'inverting input of an IC, the non-inverting input and output open.',
    'technology-2020-HL-paper-secC-q2b-iii-art':
        'Colour photograph of a black surface-mount integrated circuit with '
        'eight bent legs.',
    'technology-2020-HL-paper-secC-q2d-art':
        'Drawing of an automated gate between two pillars with keypads A and '
        'B, a house behind with the master switch S and gate switch C.',
    'technology-2020-HL-paper-secC-q5c-art':
        'Shaded drawing of a flat circular disc with a square hole through '
        'its centre.',
    'technology-2020-HL-paper-secA-q12-art':
        'A one-row table of website analytics: Sessions 624,935, Users 299,488, '
        'Page Views 5,826,244 and Pages per Session 9.32.',
    # 2026 Ordinary (2026-10-28): the cropper's cuts for Q9 and Q12, and by-eye
    # rects (tech_crops.BY_EYE) for the rest, each opened at 150 dpi.
    'technology-2026-OL-paper-secA-q1-art':
        'Colour photograph of a green floor-standing pillar drill: the motor '
        'and chuck at the top of a steel column, a machine vice on the table '
        'and a heavy cast base.',
    'technology-2026-OL-paper-secA-q3-art':
        'A yellow triangular warning sign with a black border showing a '
        'figure tripping over a raised step.',
    'technology-2026-OL-paper-secA-q4-art':
        'Colour photograph of a three-tiered wooden planter box on grass, '
        'three stepped troughs on a diagonal frame, with a white arrow '
        'labelled A pointing at its front.',
    'technology-2026-OL-paper-secA-q6-ii-art':
        'A lever diagram: a horizontal bar on a triangular fulcrum, a 40 N '
        'downward arrow at the left end 1 M from the fulcrum and a downward '
        'force F at the right end 4 M from it.',
    'technology-2026-OL-paper-secA-q9-art':
        'A circuit diagram: a battery feeding a motor M through a '
        'double-pole double-throw switch outlined in a red dashed box and '
        'labelled Switch A, with its two blades linked by a dashed line.',
    'technology-2026-OL-paper-secA-q11-art':
        'Shaded drawing of a ratchet and pawl: a toothed wheel with a keyed '
        'bore and a red arrow showing its rotation, with a pawl on a pivot '
        'above it and a red arrow showing the pawl lifting.',
    'technology-2026-OL-paper-secA-q12-art':
        'Outline line drawing of a pump-action soap dispenser in a ruled box: '
        'a tapered bottle with a collar and a pump head whose nozzle points '
        'to the right.',
    'technology-2026-OL-paper-secB-q2b-art':
        'Colour photograph of a clear phone cover with a magnetic ring on its '
        'back, seen from behind.',
    # By-eye rects (tech_crops.BY_EYE) for in-window parts.
    'technology-2021-HL-paper-secB-q3b-art':
        'A circuit diagram: a variable resistor R1 and a thermistor R2 in series '
        'as a potential divider feeding a transistor through R3, with a diode '
        'across a relay coil in the collector line and the relay contacts '
        'switching a motor M.',
    'technology-2021-HL-paper-secC-q2b-art':
        'A circuit diagram of a 555 timer between two supply rails: R1 and R2 '
        'in series to pins 7, 6 and 2, C1 from pin 2 to 0V, C2 on pin 5, pins 4 '
        'and 8 to +V and pin 1 to 0V, with the output at pin 3.',
    'technology-2021-HL-paper-secC-q4c-art':
        'A control chart: Sample Value from 38 to 42 against Time from 0 to '
        '25, with a UCL line at 41.5, an Average line at 40 and an LCL line at '
        '38.5, and the plotted samples scattered about the average.',
    'technology-2021-OL-paper-secC-q2b-art':
        'A circuit diagram between two supply rails with a switch in the top '
        'rail: a resistor above an electrolytic capacitor A in series, the '
        'junction feeding a transistor B through a resistor, with an LED and '
        'resistor in the collector line.',
    'technology-2023-HL-paper-secC-q4d-art':
        'An assembly sequence in six captioned pictures joined by arrows: '
        'Assemble chassis, Install circuit board, Install flat screen, Install '
        'speakers, Final assembly and Inspection.',
    'technology-2024-OL-paper-secC-q2b-art':
        'A circuit diagram of a 555 monostable between +V and 0V rails: two '
        'resistors from +V, a push switch, the 555 with pins 8, 4, 6, 7, 2 and '
        '1 marked and its output at pin 3, and an electrolytic capacitor C.',
}

# The residue authors' crops (2026-10-28), each opened at 150 dpi.
REVIEWED.update({
    'technology-2021-HL-paper-secA-q11-art':
        'Line drawing of a belt drive: a smaller pulley on the left labelled Driven pulley and a larger pulley on the right labelled Driver pulley, joined by a belt, with a curved arrow beside each pulley showing its direction of rotation, and a spring-loaded pulley labelled Jockey pulley pressing up against the lower run of the belt between them.',
    'technology-2021-HL-paper-secA-q12-art':
        'Two drawings. Left: a rendered compound gear, a small gear fixed to the face of a larger gear, with arrows labelled 20 teeth and 50 teeth, captioned Compound gear. Right: a schematic of a gearbox frame with a blue DC motor driving a small red gear labelled Initial driver gear, which meshes through a train of compound gears on parallel vertical shafts ending at the shaft labelled Output shaft.',
    'technology-2021-HL-paper-secA-q6-art':
        'Colour photograph of a Voronoi mushroom lamp lit from inside: a glowing orange dome-shaped shade, a thin skin set in a web of irregular cell-shaped frame ribs, standing on a white flared stem and round base.',
    'technology-2021-HL-paper-secA-q8-art':
        'Colour photograph of a bench-mounted belt and disc sander: a black motor housing driving a disc faced with red-brown abrasive, a horizontal sanding belt arm above it, a slotted metal work table with an angle fence in front of the disc, and a black base carrying a red and green on/off switch.',
    'technology-2021-HL-paper-secC-q1b-art':
        'Colour photograph of an automated pet-food dispenser, a black unit with a clear food hopper and a tray of dry food at its base, with a golden retriever and a tabby cat beside it. Below it, the start of a flowchart: a green Start box, an arrow to a blue parallelogram Power on, then a blue decision diamond Is hopper empty ? with one arrow leaving its right corner and one leaving its bottom.',
    'technology-2021-HL-paper-secC-q1d-art':
        'Colour photograph of a pneumatic bottle-capping machine: a pneumatic cylinder with air lines and a pressure regulator mounted on a vertical column above a capping head, with a row of blue bottles standing on the base plate beneath it.',
    'technology-2021-HL-paper-secC-q3c-art':
        'Two colour photographs. Top: a black laptop power supply brick with its cable and laptop connector, and a separate mains lead with a three-pin plug, captioned 240 V laptop power supply. Bottom: a smartphone lying on a black wireless charging power bank, blue rings drawn around it to show the charging field, captioned Wireless charging device.',
    'technology-2021-OL-paper-secA-q11-i-art':
        'Colour photograph of a garden spade lying diagonally: a flat grey-green steel blade at the lower left, a dark green shaft, and a yellow handle ending in a D-shaped grip at the upper right. Nothing on the picture is labelled.',
    'technology-2021-OL-paper-secA-q11-ii-art':
        'Lever diagram: a yellow horizontal beam resting on a yellow triangular fulcrum at its right end. A red arrow labelled 50 N pushes down on the left end, and a red arrow labelled F pushes up from below at a point 0.3 M from the left end and 0.5 M from the fulcrum, the two distances marked with dimension arrows above the beam.',
    'technology-2021-OL-paper-secA-q12-art':
        'Black-and-white line drawing of a citrus juicer: a ribbed cone-shaped reamer rising from the centre of a round bowl, a slotted strainer ring around the base of the cone, a pouring lip on the left rim and a short handle on the right.',
    'technology-2021-OL-paper-secA-q5-art':
        'Colour photograph of two meshing gear components: a black shaft with a spiral screw thread, labelled A, lying across the top of a brass toothed wheel, labelled B.',
    'technology-2021-OL-paper-secA-q7-art':
        'Colour photograph of a small wooden birdhouse with a pitched roof, a round entrance hole and a perch peg on its front. An arrow labelled B points straight down onto the roof from above, and an arrow labelled A points up and to the right at the front of the birdhouse from the lower left.',
    'technology-2021-OL-paper-secC-q1b-art':
        "The start of a flowchart: a green Start box with an arrow down to a white decision diamond labelled On. A line runs from the diamond's right corner out to the right, up, and back into the right side of the Start box, and an arrow leaves the bottom of the diamond. The top of a purple capsule box from the neighbouring photograph shows at the bottom right. the top 11 pt of the purple Nespresso capsule-box photograph (x 444.6-462, y 339.6-351) shows in the bottom-right corner: the flowchart's return loop reaches x 461.2 and its exit arrow reaches y 350.2, so no rectangle holding the whole flowchart can drop it. The coffee-machine photograph was left out because the (iii) ask line 'Describe how you would indicate, on the machine, that the' runs into its column.",
    'technology-2021-OL-paper-secC-q1c-art':
        "Colour photograph of a pneumatic shuttle valve: a silver valve body with three blue push-in air fittings, on a black mounting base. Below it, the shuttle valve's circuit symbol: a rectangle containing a circle between two angled seats, a port line labelled A entering the left side, one labelled B entering the right side, and one labelled C leaving the top from a dot at the centre. the last letters 's.' of the stem line 'The image shows a shuttle valve used in pneumatic circuits.' (ink to x 382.7, y 484.5-492.3) sit at the crop's left edge, level with the photograph; the label A starts at x 378.2, so no rectangle that keeps A can drop them. A symbol-only crop is no cleaner: the photograph's base reaches down into the symbol's top-right corner.",
    'technology-2021-OL-paper-secC-q4d-art':
        'A black-and-white barcode of vertical bars of varying widths, with the number 0 36000 29145 2 printed beneath it.',
    'technology-2021-OL-paper-secC-q5a-art':
        'A three-column table headed Body part, Material Classification and Material. Seat: Fabric, Material blank. Tyre: Material Classification blank, Steel-reinforced rubber. Headlight lens: Ceramic, Material blank.',
    'technology-2022-HL-paper-secA-q10-art':
        "A table titled 'Risk Assessment – Technology Room – Soldering iron' with six columns: Hazards; Is the hazard present? Y/N; What is the risk?; Risk rating (H = High, M = Medium, L = Low); Control measures; Is this control in place? Y/N. The first row is filled in: Hot soldering iron, Y, Burns, H, 'Use soldering iron stand. Warning signs present.', Y, Y. The next two rows, Damaged power lead (Y) and Fumes (Y), have every other cell blank.",
    'technology-2022-HL-paper-secA-q5-art':
        "Two pictures stacked one above the other. Top: a photograph of a beige resistor with wire leads and several coloured bands; a red arrow points to the band at its right-hand end, labelled 'Tolerance band'. Bottom: a circuit diagram in which a 5 Ω resistor in series leads to a junction, two 8 Ω resistors connected in parallel between two junction dots, then a 6 Ω resistor in series, with open wire ends at the left.",
    'technology-2022-HL-paper-secA-q6-art':
        "A rendered picture of a mechanism made of two components: a vertical blue rod passes down through a grey round plate, with a black coil spring around the rod below the plate, and the rod's lower end rests on a green pear-shaped disc mounted on a short purple shaft. A red arrow labelled A points to the lower end of the rod just under the spring; a red arrow labelled B points to the green disc.",
    'technology-2022-HL-paper-secB-q2c-art':
        "A photograph of the Adibot UV-C disinfection robot: a tall white robot with a wide wheeled base and a body with side panels, topped by a column of vertical ultraviolet lamp tubes held between round plates. A red arrow points to the bottom of the robot, labelled 'Base'.",
    'technology-2022-HL-paper-secB-q3a-art':
        "A photograph of a black Urban Movement folding e-scooter seen from the side, with a tall handlebar stem, a low deck and small wheels. A red arrow labelled 'Foldable frame' points to the hinge low on the stem, and a framed inset close-up labelled 'Electronic display' shows the small screen with a blue readout on the handlebar.",
    'technology-2022-HL-paper-secB-q3b-art':
        "A photograph of a black Urban Movement folding e-scooter seen from the side, with a tall handlebar stem, a low deck and small wheels. A red arrow labelled 'Foldable frame' points to the hinge low on the stem, and a framed inset close-up labelled 'Electronic display' shows the small screen with a blue readout on the handlebar.",
    'technology-2022-HL-paper-secC-q5c-art':
        "A photograph of a round robotic vacuum cleaner on a tiled floor, its glossy dark top lit with blue light and blue light trails fanning out around its base. A red arrow points to its upper surface, labelled 'Top cover'.",
    'technology-2022-OL-paper-secA-q8-art':
        'An incomplete Work Breakdown Structure drawn as three rows of boxes joined by arrows. Top row: Back, then Cut out, then Sand, then Paint. Second row: Sides, followed by three empty boxes. Third row: Roller, followed by three empty boxes. Arrows from the end of all three rows lead into one empty box on the right.',
    'technology-2022-OL-paper-secB-q3b-art':
        "A photograph of a black fabric battery pack holder with a Swytch logo, mounted on the front of a turquoise bicycle's handlebars between the brake levers and tan grips. A red arrow points up to the holder from the label 'Battery pack holder' printed beneath the photograph.",
    'technology-2022-OL-paper-secB-q3d-art':
        'A photograph of a bare pale blue road-bicycle frame with no wheels or components: top tube, down tube and seat tube forming the main triangle, thin rear stays forming a second triangle, and a dark blue front fork, with brand lettering on the tubes.',
    'technology-2022-OL-paper-secC-q2a-art':
        'A photograph of a beige axial resistor lying diagonally, with a wire lead at each end and four coloured bands: brown, black and red, then a gold band set apart nearer one end. The letter R is printed beside it.',
    'technology-2023-HL-paper-secA-q13-art':
        'Colour cutaway render of a blue gearbox housing with one quarter cut away to show the inside: a horizontal shaft with a spiral thread along it sits above, and meshes with, a toothed wheel below it. A flared, flanged housing on the right carries the output, with a shaft bore in its centre.',
    'technology-2023-HL-paper-secA-q8-art':
        "A cause and effect (fishbone) diagram. A thick horizontal spine arrow points right to an oval labelled 'Drone will not lift'. Four diagonal bones join the spine: 'Machine' and 'Environment' above it, 'User' and 'Materials' below it. Under Machine a box reads 'Propellers' in red, with a black arrow to its bone; each of the other three bones has an empty box beside it with a dashed red arrow pointing to the bone.",
    'technology-2023-HL-paper-secB-q2c-art':
        "A product lifecycle graph with 'Sales' on the vertical axis and 'Time' on the horizontal axis. A red curve starts low, rises slowly, then steeply, levels off to a peak and then falls away. Three dashed vertical lines divide the graph into four stages, numbered 1, 2, 3 and 4 across the top.",
    'technology-2023-HL-paper-secC-q2b-art':
        "A circuit diagram between a +9 V rail at the top and a 0 V rail at the bottom, with a switch on the +9 V line. On the left, a component labelled A, drawn as a rectangle with a diagonal arrow through it, sits above a component labelled B, drawn as a rectangle crossed by a bent line; their junction feeds the minus input of a triangular amplifier marked IC. Beside them two 10kΩ resistors in series set the voltage on the IC's plus input. The IC's output passes through a resistor to the base of a transistor, which drives a buzzer connected down to the 0 V rail.",
    'technology-2023-OL-paper-secA-q7-art':
        'Colour photograph of a bamboo cookbook stand: a large flat bamboo board leaning back on a stand, with a ledge along its bottom edge held by two black clips, and a slotted support rack visible behind it. A black arrow labelled A at the lower right points at the stand from the right-hand side.',
    'technology-2023-OL-paper-secB-q2a-art':
        "Colour photograph of a hurler's legs, in blue and yellow socks, standing on grass and holding a hurley upright with its taped handle at the top. A red arrow from the label 'Grip', on the left, points to the taped handle. the letter 'y' that ends 'environmentally' in the 2(a) stem line shows at the top-left corner: that glyph runs from x 399.6 to 405.0 and the 'Grip' label starts at x 400.0, beside a photo whose top is y 134.7, so no rectangle keeps the label and drops the letter",
    'technology-2023-OL-paper-secC-q1c-art':
        'Colour photograph of a long black dual in-line integrated circuit chip, white lettering printed on its top, with a row of silver pins along each long side.',
    'technology-2023-OL-paper-secC-q4a-art':
        "A perceptual map. A vertical red double-headed arrow runs from 'Low quality' at the bottom to 'High quality' at the top; it crosses a horizontal red double-headed arrow running from 'Low cost' on the left to 'High cost' on the right. Three circled letters mark products: A in the upper-left quarter (low cost, high quality), B in the upper-right quarter (high cost, high quality), and C just below the centre on the left (low cost, low quality).",
    'technology-2024-HL-paper-secA-q10-art':
        'Colour photograph of a small pink GPS luggage tag, a rounded rectangle seen at an angle, with the brand name nut printed in magenta on its face above a grid of small pin holes.',
    'technology-2024-HL-paper-secA-q11-art':
        "Colour photograph of an orange and grey counterbalance forklift truck: the driver's seat under a roll cage, a vertical mast at the front carrying two long forks lowered to the ground, and a heavy counterweight at the rear.",
    'technology-2024-HL-paper-secA-q12-art':
        'Colour photograph of a car alternator with a white 3D-printed mounting bracket bolted to its front, the pulley at the centre, with a red arrow pointing at the bracket.',
    'technology-2024-HL-paper-secA-q15-art':
        'Colour photograph of a small solid-timber fireside stool in a thin black frame: a rectangular top over a front rail, two splayed slab legs each with an arched cut-out at the foot, and a shelf spanning between the legs near the floor.',
    'technology-2024-HL-paper-secA-q3-art':
        'Colour photograph of the lower right-hand corner of an interactive touch screen: a teal abstract wallpaper on the display inside a thin black bezel, a dark bar along the bottom edge, and grey concentric rings drawn over the bottom right of that bar to mark where the proximity sensor sits.',
    'technology-2024-HL-paper-secA-q7-art':
        'Rendered pictorial view of a compound gear train in brown: a small gear labelled Gear A drives a large gear that shares its shaft with a second small gear, which drives a second large gear labelled Driven Gear. Red leader lines label the two small gears 15 Teeth and the two large gears 75 Teeth, and curved red arrows show the direction each gear turns.',
    'technology-2024-HL-paper-secC-q2a-art':
        'Colour photograph of a black three-in-one wireless charging stand: a smartphone propped upright on it showing a green charging symbol, a smartwatch on a raised arm to the right, and a pair of earbuds in a white case lying on the charging base.',
    'technology-2024-HL-paper-secC-q2d-art':
        'A logic gate diagram: inputs A and B feed a two-input AND gate; input A also branches down through a NOT gate, whose output meets input C at a second AND gate; the outputs of the two AND gates feed an OR gate whose output is labelled O.',
    'technology-2024-HL-paper-secC-q4d-art':
        'A product lifecycle graph drawn in red: Sales on the vertical axis against Time on the horizontal, divided by vertical lines into stages A, B, C and D. The curve rises slowly through A, climbs steeply through B, levels off across C and falls away sharply in D.',
    'technology-2024-HL-paper-secC-q4d-ii-art':
        'An updated product lifecycle graph drawn in green, on the same Sales against Time axes and stages A, B, C and D: the curve rises through A and B and levels off across C as before, but in D it dips briefly and then turns upward again.',
    'technology-2024-HL-paper-secC-q5c-art':
        'Colour photograph of an open presentation box finished in striped walnut veneer: the hinged lid raised, and inside a black lined tray holding a gold pen and a small gold crest badge.',
    'technology-2024-OL-paper-secA-q1-art':
        'A round blue mandatory safety sign showing, in white, water running from a tap over a pair of hands being washed.',
    'technology-2024-OL-paper-secA-q6-art':
        'Colour photograph of a sliding bevel: a black steel blade with a long slot, locked by a brass wing nut at the end of a polished hardwood stock with brass end caps.',
    'technology-2024-OL-paper-secA-q7-art':
        'Colour photograph of a blue steel machine tool stand with a plywood top and a plywood lower shelf on four splayed legs with black feet; a black arrow labelled A at the bottom right points diagonally up at the stand, giving the direction of view.',
    'technology-2024-OL-paper-secA-q8-art':
        'Colour photograph of a toothed belt drive: two flanged toothed pulleys of equal size joined by a black toothed timing belt whose teeth mesh with the pulleys.',
    'technology-2024-OL-paper-secB-q3c-art':
        'Outline side view of a model tilt-rotor aircraft on a stand: a 50 N upward force at the rear rotor 3 m from the nose, an arrow at the nose marking the fulcrum, and the rear motor labelled Motor.',
    'technology-2024-OL-paper-secC-q1b-art':
        'The start of a flowchart for the student to complete: a green Start box with an arrow down to a purple diamond decision labelled Button, whose right-hand exit loops back up to Start and whose lower exit is an open arrow pointing down.',
    'technology-2024-OL-paper-secC-q2d-art':
        'A partial resistor circuit: an 8 Ω resistor in series with a pair of 10 Ω resistors connected in parallel, with a lead at each end.',
    'technology-2025-HL-paper-secA-q12-art':
        'A resistor circuit between two open terminals on the left: R1 = 6 kΩ sits in series on the top wire, which then splits into two parallel branches down to the bottom wire, one holding R2 = 8 kΩ above R3 = 4 kΩ in series, the other holding R4 = 12 kΩ alone.',
    'technology-2025-HL-paper-secA-q15-art':
        'A photograph of a brass butt hinge opened flat: two rectangular leaves, each drilled with four countersunk screw holes, joined by a knuckle down the middle. A red arrow labelled pin points to the top of the pin that runs through the knuckle.',
    'technology-2025-HL-paper-secA-q7-art':
        "A photograph of Ireland's two-person skiff racing on blue water: a tall sail in green, white and orange bands, a dark jib marked IRL with the Olympic rings, and the crew leaning out from the hull. Beneath it three labels send red leader arrows into the photo: Mast (to the mast), Hull (to the hull) and Sail (to the striped sail).",
    'technology-2025-HL-paper-secB-q3b-art':
        'A cut-away model of a compound gearbox: four yellow spur gears on shafts in an open green housing. Red leader arrows label them: A, a small gear on the right on the shaft labelled Motor; B, the large gear beside it; C, a smaller gear in front of B; D, a large gear on the left on the shaft labelled Output.',
    'technology-2025-HL-paper-secC-q2b-art':
        "An op-amp circuit between a +9 V rail at the top and a 0 V rail at the bottom. A potential divider of R1 above R2 runs between the rails, its junction wired to the + input labelled B of a triangle labelled IC. A wire labelled Input enters from the left, hops over the divider wire and reaches the - input labelled A. The IC's output end is labelled output; no input or output device is drawn.",
    'technology-2025-HL-paper-secC-q2d-art':
        'A series circuit: a 12V battery (cells drawn with a dashed link) on the left drives current through R1 and then R2 on the right and back along the bottom wire through a circle marked A (the ammeter); a circle marked V (the voltmeter) is wired across R1 alone.',
    'technology-2025-OL-paper-secA-q1-art':
        'A photograph of a tall floor-standing workshop machine with a blue and white body: an upper and a lower cabinet, a vertical blade guide with a yellow guard above a square work table, a handwheel at the top right and the model mark BP-430A printed down the lower cabinet.',
    'technology-2025-OL-paper-secA-q3-art':
        'A round safety sign on white: a black camera symbol inside a thick red circle with a red diagonal bar struck through it from top left to bottom right.',
    'technology-2025-OL-paper-secA-q4-art':
        "A photograph of a child's wooden ride-on toy: a curved wooden seat on a front leg and a rear support, four black wheels with red hubs, and a red T-shaped handlebar at the front. At the lower right a black arrow labelled A points in towards the toy, giving the direction of view.",
    'technology-2025-OL-paper-secC-q2c-art':
        'A combination of two logic gates: inputs A and B enter a D-shaped gate (flat input side, rounded output side) labelled X; its output, labelled C, enters a triangle with a small circle at its tip labelled Y, whose output is labelled D. Below it, a truth table headed A, B, C, D with the A and B columns filled 0 0, 0 1, 1 0, 1 1 and the C and D columns left blank.',
    'technology-2025-OL-paper-secC-q5b-art':
        'A diagram of a fused deposition 3D printer: green filament runs from a reel on the right, over the top and down between a pair of grey rollers, through a grey housing to a red-and-yellow block and a nozzle above a green printed block standing on a flat grey plate. Red arrows mark A (the reel), B (the filament entering the rollers), C (the red-and-yellow block), D (the green block) and E (the plate).',
})

# The residue authors' crops (2026-10-28), each opened at 150 dpi.
REVIEWED.update({
})

# The whole-bank audit's crops (2026-10-28), each opened at 150 dpi.
REVIEWED.update({
    'technology-2020-HL-paper-secA-q13-art':
        'Exploded view of an LED light bulb, its parts separated along a slanted axis: a white frosted dome at the top, a round circuit disc carrying a grid of yellow LED chips, a ribbed white housing with a green circuit board inside, and a metal screw base at the bottom.',
    'technology-2020-HL-paper-secA-q14-art':
        "Photo of an e-scooter's rear wheel, a red spoked wheel with a knobbly tyre, driven by a chain; a red arrow points to the large sprocket on the wheel hub, labelled Gear A.",
    'technology-2020-HL-paper-secA-q5-art':
        'A voltage divider circuit: a 6 V terminal at the top feeds resistor R1 = 120 Ω, then resistor R2 down to a 0 V terminal; output terminal A is taken from the junction between R1 and R2, with a matching 0 V output terminal below.',
    'technology-2020-HL-paper-secB-q2b-art':
        "Photo of the Lightcycle desk lamp: a tall white upright with a horizontal arm whose end shines light downward. A red double-headed arrow labelled A marks the arm's up-and-down height adjustment and a curved red arrow labelled B at the round base marks its rotary movement. An orange circle around the arm's joint leads by an orange line to a large circular close-up on the left of the roller-and-groove system: a slotted metal bracket carrying small black rollers that run above and below the arm where it crosses the grooved upright.",
    'technology-2020-HL-paper-secB-q2b-ii-art':
        "Circular close-up, ringed in orange, of the lamp's roller-and-groove system: a metal bracket with a slot carries small black rollers that run above and below the lamp's horizontal arm where it crosses the grooved vertical upright; a short stub of the orange leader line leaves the ring on the right.",
    'technology-2020-HL-paper-secB-q2d-art':
        'A circular diagram of four curved arrows chasing each other clockwise around a purple centre labelled Product Life Cycle: red Introduction at the top left, blue Growth at the top right, yellow Maturity at the bottom right and green Decline at the bottom left.',
    'technology-2020-HL-paper-secB-q3b-art':
        "Photo of a food processor drive unit: an electric motor with copper windings in a metal frame, its shaft ending in a worm that meshes with two white nylon gears, A above and B below, with a yellow cooling fan on the left. Red arrows from the label 'Each gear has 50 teeth' point to both gears; the caption reads Food processor drive unit.",
    'technology-2020-HL-paper-secB-q3c-art':
        'Photo of a hand blender standing upright: a dark grey grip with a curved top, a red motor body, a long stainless-steel shaft ending in a domed blade guard, and a coiled white power cord with a plug hanging to the right.',
    'technology-2020-HL-paper-secB-q3d-art':
        "Two fast-food boxes side by side. Left: a cream hinged clamshell box, captioned 'Box A. Made from expanded polystyrene.' Right: an open red folding carton with white inner flaps, captioned 'Box B. Made from cardboard.'",
    'technology-2020-HL-paper-secC-q1d-art':
        "Photo of a bench-mounted sheet metal cutter: a grey steel base plate with a hinged cutting blade along its top edge, worked by a linkage from a horizontal pneumatic cylinder mounted above it; small cut metal pieces lie on the base. A red arrow from the label 'Double acting pneumatic cylinder' points to the cylinder.",
    'technology-2020-HL-paper-secC-q2b-art':
        "An incomplete op-amp circuit between a +9 V rail at the top and a 0 V rail at the bottom. A 66 kΩ resistor above a 33 kΩ resistor form a potential divider whose midpoint feeds the + input of a triangle marked IC. A loose wire from the left hops over the divider wire and connects to the − input, at point A. The IC's supply pins join both rails and its output line runs off to the right, unconnected.",
    'technology-2020-HL-paper-secC-q2b-iii-art':
        "Photo of a small black surface-mount integrated circuit chip with four short gull-wing metal leads along each long side, captioned 'Surface mount IC'.",
    'technology-2020-HL-paper-secC-q2c-art':
        "Exploded view of a photovoltaic panel's layers floating one above another: a clear glass sheet on top, then a thin film, a grid of dark blue solar cells, another film and a backing sheet. A red arrow from the label 'Outer layer of glass' points to the top sheet.",
    'technology-2020-HL-paper-secC-q5b-art':
        "Photo of the e-Palette shuttle's interior: a bright cabin with large windows, yellow-green grab rails running along the walls and ceiling, and a row of dark fold-down seats against the far side. Red arrows point to a rail, labelled holding rails, and to the seats, labelled plastic seats.",
    'technology-2021-HL-paper-secA-q10-art':
        "A cut-away photograph of a blue cast-iron gearbox with part of its casing removed, showing the helical-cut gears, bearings and shafts inside and the output shaft projecting to the right. old crop ran past the photo's right edge into the question box border",
    'technology-2021-HL-paper-secC-q2c-art':
        'A table of four transistors with columns Transistor, Name and Current gain: A, BFY50, 30; B, 2N3053, 50; C, BC107, 100; D, TIP31, 20.',
    'technology-2021-HL-paper-secC-q4a-art':
        'Two logos stacked: above, the CE mark (the letters C and E in black); below, the Fairtrade mark, a black, blue and green circular figure with the words FAIRTRADE INTERNATIONAL beneath it and a registered-trademark symbol at top right.',
    'technology-2021-HL-paper-secC-q4b-art':
        "A photograph of a blue electric water pump: a round pump housing with a white-lined inlet on its side and an outlet on top, joined to a ribbed electric motor with a black terminal box, on a flat mounting foot. x0 sits just right of the colon ending the (i) ask line 'manufacturer:' (x 415.7)",
    'technology-2021-HL-paper-secC-q5b-art':
        'The hands-free door opener: top left, a line drawing of its parts exploded, a curved arm with two clamp pieces and the screws and nuts that join them; top right, a line drawing of the arm clamped onto a lever door handle; below, a photograph of a person opening a door by pressing the arm with their forearm, hand held clear of the handle.',
    'technology-2021-OL-paper-secA-q10-art':
        'A photograph of a white USB memory stick with its cap pulled off beside the metal connector, printed with the words The Photo Stick.',
    'technology-2021-OL-paper-secA-q2-art':
        'Two photographs of the Connacht GAA air dome: above, an aerial view of a huge white inflated dome beside a two-storey building, car parks and green pitches; below, the inside of the dome, a full-size pitch under a curved, ribbed white fabric roof.',
    'technology-2021-OL-paper-secA-q3-art':
        'Two photographs: a yellow and black DeWalt random orbital sander with its dust bag, and below it a stack of round red-brown sanding discs punched with dust-extraction holes.',
    'technology-2021-OL-paper-secA-q4-art':
        'Two safety signs: above, a red circle with a red diagonal bar across a black walking figure (a prohibition sign, no pedestrians); below, a yellow triangle with a black border and a black exclamation mark (a warning sign).',
    'technology-2021-OL-paper-secA-q8-art':
        'An electronic circuit symbol: a rectangle (resistor) with a lead on each side, crossed by a diagonal line that ends in a short horizontal hook at the top right (the thermistor symbol).',
    'technology-2021-OL-paper-secB-q2a-art':
        "A photograph of a black folding laptop stand holding an open laptop on a desk, a woman's hand on the keyboard; an arrow points to its hinged lower arms, labelled Support legs.",
    'technology-2021-OL-paper-secB-q2b-art':
        'A photograph of a woman sitting up in bed reading a book held open on the folding stand, its arm angled over the bed beside her.',
    'technology-2021-OL-paper-secB-q3c-art':
        'A photograph of a black and blue electric mountain bicycle with front suspension, disc brakes and a battery pack mounted on the frame.',
    'technology-2021-OL-paper-secC-q1a-art':
        'A photograph of a black capsule coffee machine with a clear water tank at the back and a glass cup of coffee on its drip tray.',
    'technology-2021-OL-paper-secC-q1b-art':
        'A part-drawn flowchart beside a photograph: a green Start box leads down to a decision diamond labelled On, whose side exit loops back up above it, and an arrow continues down from the diamond, unfinished. To the right, a white Nespresso capsule coffee machine with a glass of coffee, and below it a purple capsule box and three coffee capsules.',
    'technology-2021-OL-paper-secC-q1c-art':
        'A photograph of a pneumatic shuttle valve block with blue push-in fittings, and below it the shuttle valve symbol: a box containing a ball between two seats, with port A entering at the left, port B at the right and port C leaving from the top.',
    'technology-2021-OL-paper-secC-q1d-art':
        'A photograph of an industrial pick-and-place robot arm mounted on a long linear rail on a workshop floor, with rows of small orange blocks on the floor beside it.',
    'technology-2021-OL-paper-secC-q2a-art':
        'A photograph of a yellow-cased digital multimeter with a rotary selector dial and a display reading 0.00, its red and black test leads coiled beside it.',
    'technology-2021-OL-paper-secC-q2b-art':
        'A timer circuit diagram: a switch on the top supply rail; a resistor down to a junction and a capacitor marked + and labelled A down to the bottom rail; from the junction a resistor feeds the base of a transistor labelled B, whose collector connects through an LED (with light arrows) and a resistor up to the top rail and whose emitter goes to the bottom rail.',
    'technology-2021-OL-paper-secC-q2c-art':
        'A photograph of a tall bladeless fan heater in blue and grey, and beside it a three-pin plug opened to show its fuse, with an arrow to the callout Fuse in holder.',
    'technology-2021-OL-paper-secC-q3c-art':
        'A photograph of a black Nikon digital SLR camera with a zoom lens, standing on a wooden table.',
    'technology-2021-OL-paper-secC-q4b-art':
        "A photograph of a thin flat-screen smart television on two splayed feet, its screen showing yellow lilies against orange petals. x0 sits right of the stem word 'factory.' (ends x 447.4), which overlaps the photo's image box",
    'technology-2022-HL-paper-secA-q12-art':
        'A tower crane drawn side-on on the ground: a lattice mast with a horizontal lattice jib labelled Jib (red arrow). A yellow counterweight labelled 9850 kg sits on the short left arm; a dimension arrow gives 4.1m from the counterweight to the mast and another gives 7.6m from the mast to the hook line, from which a load hangs on a cable.',
    'technology-2022-HL-paper-secA-q15-art':
        'Outline line drawing of a handheld cordless vacuum cleaner in pictorial view, unshaded: the tapered nozzle and dust bowl at the front, a round motor housing, a button and slide switch on top, and a loop handle at the rear.',
    'technology-2022-HL-paper-secA-q7-art':
        "A colour photograph of a concrete road bridge under construction, in its own thin black frame: a long deck with a metal railing along the top, carried on a row of square concrete pillars, with bare earth and rubble banked beneath it. the photo sits in the top-right corner of the answer box; its own frame coincides with the box's top rule, which is the crop's top edge",
    'technology-2022-HL-paper-secA-q9-art':
        'Two colour photographs side by side: on the left a hard disk drive with its cover removed, showing the gold platter, spindle and read-head arm; on the right a solid-state drive with its case partly open, showing the memory chips on its circuit board.',
    'technology-2022-HL-paper-secB-q2c-art':
        "A photograph of the Adibot UV-C disinfection robot: a tall white robot with a wide wheeled base and a body with side panels, topped by a column of vertical ultraviolet lamp tubes held between round plates. A red arrow points to the bottom of the robot, labelled 'Base'. existing key and rect, re-rendered and verified whole and clean; the picture is printed for 2(b) ('The base of the Adibot UV-C robot, shown') and 2(c)(i) points back to it, so the cards list widens to the three 2(b) cards",
    'technology-2022-HL-paper-secC-q1b-art':
        'A colour graphic of a desktop inkjet printer: a grey and blue body with a paper tray standing up at the back and a printed sheet with lines of text coming out of the front onto the output tray.',
    'technology-2022-HL-paper-secC-q1c-art':
        "A colour photograph of a 3D printer seen from the front, in a thin black frame: a black frame with a red carriage on top, a print bed carrying a blue 3D-printed '3D' model, and a yellow arrow from the label 'Print head module' pointing to the print head above the bed.",
    'technology-2022-HL-paper-secC-q2b-art':
        'A circuit diagram between a +V rail at the top and a −V rail at the bottom: a variable resistor A above a thermistor B form a potential divider whose midpoint feeds a transistor through a resistor; a push switch C hangs from the top rail; the transistor output and switch C feed the two inputs of an OR gate D, which drives a buzzer.',
    'technology-2022-HL-paper-secC-q3b-art':
        'A colour photograph of a black Logitech high-definition webcam: a wide flat bar with a central lens ring and two small sensors, mounted on a folding clip-style stand.',
    'technology-2022-HL-paper-secC-q4a-art':
        "Two drawings side by side joined by a red arrow. Left, labelled 'Original bracket design': an exploded line drawing of a roll-bar bracket made of several bent metal plates, a long bolt across the top and many nuts, washers and screws. Right, labelled 'Modified bracket design': a single lime-green folded sheet bracket with two upright sides and one orange rod across the top held by two collars.",
    'technology-2022-HL-paper-secC-q4b-art':
        'A colour photograph of the Slant 3D headphone stand: a dark grey 3D-printed stand with a slanted upright and a flat base, with a pair of black over-ear headphones hanging over its top.',
    'technology-2022-HL-paper-secC-q4c-art':
        'A control chart: Samples up the vertical axis marked 39.6, 39.8, 40.0, 40.2 and 40.4, Time along the horizontal axis. A solid red line at 40.4 is labelled UCL, a solid red line at 39.6 is labelled LCL, and a dashed red centre line sits at 40.0. Ten plotted points start near 39.8, rise across the centre line in the middle and level off at about 40.25, below the UCL.',
    'technology-2022-HL-paper-secC-q4d-art':
        'A bathtub curve: Failure rate up the vertical axis, Time along the horizontal axis. An orange curve falls steeply at the start, runs low and flat through the middle and rises steeply at the end. Two dashed vertical lines divide it into three phases labelled A (the falling start), B (the flat middle) and C (the rising end).',
    'technology-2022-HL-paper-secC-q5a-art':
        "A cut-away render of a round robotic vacuum cleaner seen from below at an angle, showing its brush, dust bin and two black wheels inside a translucent casing. A red arrow from the label 'Cleaner - outer casing' points to the rim of the body, and a red arrow from the label 'wheel' points to one of the wheels.",
    'technology-2022-OL-paper-secA-q1-art':
        "A round blue mandatory safety sign: a white outline of a shoe covered by a gathered disposable overshoe, with two lines rising from its elasticated top like a lower leg. the (ii) ask line ends 'life.' at x 443.5 just under the sign's lower-left; the rect starts at 441.3 and stops at 240.5 so the 'e.' (y 241-243) stays out while the whole circle stays in",
    'technology-2022-OL-paper-secA-q12-art':
        'Outline line drawing of a USB flash drive in pictorial view, unshaded: the rounded body with the metal USB connector exposed at one end, and its cap lying separately to the right.',
    'technology-2022-OL-paper-secA-q7-art':
        "A colour photograph of a Stockholm toddler chair made of pale plywood: two side panels with cut-out hand holes, a back panel printed 'stockholm', and a seat panel across the middle; the same lettering appears upside down below the seat. A black arrow labelled A points up and to the right at the front of the chair from the lower left.",
    'technology-2022-OL-paper-secA-q9-art':
        "A colour photograph of a blue plastic waste bin, slightly tapered and open at the top, with a white recycling symbol of three chasing arrows in a triangle on its front. the (ii) ask line ('... a thermoplastic material.') ends at x 456.2 just under the bin; the rect stops at y 652.5, above its ink",
    'technology-2022-OL-paper-secB-q2a-art':
        "A render of a Modpool: a dark grey corrugated steel shipping container made into a swimming pool, filled with blue water, with a large glass viewing window in its side and stainless-steel ladders at the left end and over the right end. the italic descenders of 'upcycled' in the lead-in line (ink to y ~148.1) hang over the image top; y0 148.4 keeps them out at the cost of ~0.3 pt off the top of the right-hand ladder's rail",
    'technology-2022-OL-paper-secB-q2b-art':
        "A colour photograph of a Modpool installed in a garden: a blue container pool set into a paved patio beside sun loungers and a timber fence, with plants along its side; a red arrow points to the container's glass end, labelled 'Modpool'.",
    'technology-2022-OL-paper-secB-q3c-art':
        'An exploded view of a hub DC motor: from left to right, the end cover with its axle and screws, a red planetary gear set in a black carrier, a stator ring wound with yellow-gold copper coils, and the silver outer hub shell with spoke flanges.',
    'technology-2022-OL-paper-secC-q1b-i-art':
        "The start of a flowchart to be completed: a green Start box with an arrow down to a purple decision diamond labelled On. A line leaves the diamond's right corner, runs right and up, and returns with an arrow into the right side of the Start box; an arrow leaves the bottom of the diamond, pointing down to nothing. bind in place of q1b-art on this card; q1b-art (the Robo-Deck photo, whole and clean) stays on c1b-ii and c1b-iii",
    'technology-2022-OL-paper-secC-q1c-art':
        "A colour photograph of a pneumatic paint spray gun: a black pistol-grip gun with a trigger and a nozzle, mounted on top of a silver aluminium paint cup. the stem line '... used to paint decks.' ends at x 466.0 beside the photo's top; x0 467 keeps it out",
    'technology-2022-OL-paper-secC-q1d-art':
        "A framed photograph of a white desktop robot arm with several jointed segments ending in a black two-fingered gripper; a black arrow from the label 'Mechanical Gripper' below the frame points up to the gripper.",
    'technology-2022-OL-paper-secC-q2a-i-art':
        "Two code tables side by side. 'Colour code': 0 Black, 1 Brown, 2 Red, 3 Orange, 4 Yellow, 5 Green, 6 Blue, 7 Violet, 8 Grey, 9 White. 'Tolerance code': 1% Brown, 2% Red, 5% Gold, 10% Silver. bind in place of q2a-art on this card; q2a-art (the resistor photo, whole and clean) stays on c2a-ii",
    'technology-2022-OL-paper-secC-q2c-art':
        'A colour photograph of a black cylindrical electrolytic capacitor marked 47 µF 450 V, with a light stripe down one side and two wire legs of unequal length.',
    'technology-2022-OL-paper-secC-q4a-art':
        "Colour photograph of corrugated cardboard packaging: a stack of flat die-cut carton blanks behind three small assembled cube-shaped boxes, one of them open. the (ii) ask line ends 'environmentally' at x 456.0 just under the photo; y1 171.2 stops above its ink (from 171.4)",
    'technology-2022-OL-paper-secC-q4c-art':
        'A colour photograph of a business meeting: a woman stands at the head of a long table presenting to seated colleagues with laptops and papers, in a bright room with large windows.',
    'technology-2022-OL-paper-secC-q5d-art':
        'A colour photograph of two thermochromic mugs: on the left coffee is being poured from a jug into a black mug printed OFF; on the right a white mug printed ON is full of hot coffee with steam rising.',
    'technology-2023-HL-paper-secA-q11-art':
        'Colour photograph of a white vented cycle helmet with a black peak at the back and a black action camera in a protective case strapped to its top with black straps.',
    'technology-2023-HL-paper-secA-q15-art':
        "Colour photograph of Eileen Gray's non-conformist chair: a tan upholstered seat with stitched ribs, one curved padded armrest on the left only, a padded cylindrical backrest, all carried on a chrome tubular steel frame with a diagonal strut on the right.",
    'technology-2023-HL-paper-secA-q6-art':
        'Colour photograph of a red and silver cordless right-angle drill: the motor body and red battery handle run horizontally, a black side handle sticks out at the front, and the chuck points straight down at 90 degrees to the motor.',
    'technology-2023-HL-paper-secA-q7-art':
        'Colour photograph of a dark grey ergonomic keyboard whose key layout is split and curved, raised in the middle, with a padded palm rest along its front edge.',
    'technology-2023-HL-paper-secB-q2b-art':
        "Colour photograph of the underside of the yellow Pixy drone: a camera lens at the top edge and four propellers set into the casing, with a red arrow from the label 'Replaceable battery pack' pointing to a panel at the centre.",
    'technology-2023-HL-paper-secB-q3b-art':
        "Colour photograph of a white mobile charging robot beside a white electric car, its jointed grey robot arm reaching up to the car's charging point. Red arrows run from the labels 'Robot casing' to the robot's body and 'Robot arm' to the arm.",
    'technology-2023-HL-paper-secC-q4b-art':
        "A two-row table of daily product defects. Day: Mon, Tue, Wed, Thurs, Fri, Sat, Sun. No. of defects: 9, 11, 8, 9, 10, 8, 8. The 4(b) helmet photo the stem calls 'The helmet shown' (x 380-547, y 386-514) is not in this rect: no rectangle holds both it and the table without the stem text beside the helmet. The table carries the data the asks need.",
    'technology-2023-HL-paper-secC-q5b-art':
        "Colour photograph of a white gaming mouse whose shell is perforated with hexagonal honeycomb holes. A red arrow from the label 'Honeycomb vents' points to the holes on top, and a red line from the label 'Mouse buttons' points to the side buttons.",
    'technology-2023-OL-paper-secA-q1-art':
        "Two workplace safety signs side by side. Left, labelled A: a square green sign with a white cross. Right, labelled B: a round sign with a red border and red diagonal bar over a black raised hand and a worker's head in a hard hat. Each letter is followed by the paper's ruled answer lines. The letters A and B are printed only at the start of the answer lines ('A: ____', 'B: ____'), and A's lines sit between the two signs, so no rectangle holding both signs can drop the lines; kept whole so the letters the row uses are shown.",
    'technology-2023-OL-paper-secA-q11-art':
        'Colour photograph of a person in jeans and wellington boots pushing a muddy single-wheeled wheelbarrow across grass by its two handles, the wheel at the front.',
    'technology-2023-OL-paper-secA-q6-art':
        'Colour photograph of a metal spur gear with a central bore meshing with the teeth of a long straight toothed bar (a rack) beneath it.',
    'technology-2023-OL-paper-secA-q8-art':
        'Colour photograph of a rotary potentiometer: a slotted metal shaft on a threaded bush above a round body on a brown board, with three pins below; the letter A labels the middle pin.',
    'technology-2023-OL-paper-secA-q9-art':
        'Rendering of a reading chair made from a dark brown curved bent-wood band that sweeps up and over in a large arc ending in a lamp above the seat, with a green cushioned seat and backrest on rocker-shaped legs.',
    'technology-2023-OL-paper-secB-q3a-art':
        "The Leinster Model Flying Club logo: a blue ring lettered LEINSTER MODEL round the top and FLYING CLUB round the bottom, a gold stag's head on a white shield at the centre, and grey feathered wings spreading out to each side.",
    'technology-2023-OL-paper-secB-q3b-art':
        'Colour photograph of a yellow and grey high-wing model aeroplane, the Hobbyzone Carbon Cub, with a black propeller and large black tyres, beside a black handheld radio controller with two sticks and an aerial.',
    'technology-2023-OL-paper-secB-q3c-art':
        'A pair of long grey model-aeroplane floats lying side by side, joined by a frame of thin black wire struts that would fix them under the plane.',
    'technology-2023-OL-paper-secC-q1b-art':
        "Colour photograph of a round novelty night light, a translucent dome printed with sea creatures glowing in colours on a black base with three buttons. Below it, the start of a flowchart: a green Start box with an arrow down to a purple Button? decision diamond, a line from the diamond's right corner looping up and back into the Start box, and an arrow leaving the bottom of the diamond downwards.",
    'technology-2023-OL-paper-secC-q2a-art':
        'Colour close-up photograph of a green printed circuit board populated with a square black surface-mount chip with pins on all four sides, small resistors and capacitors, and white printed component labels.',
    'technology-2023-OL-paper-secC-q5b-ii-art':
        "Grey rendering of a metal angle bracket labelled Bracket: a flat base plate with two bolt holes and an upright plate with one hole at its top, joined at a right angle. Roman-level key for 5(b)(ii) only. It cannot share a rect with the 5(b) bridge photo (technology-2023-OL-paper-secC-q5b-art) because the (i) ask 'difference ... jointing methods.' runs between them; if the card can carry only one question figure, the bracket is the one its ask names ('a bracket like that shown').",
    'technology-2024-HL-paper-secA-q12-art':
        "Photograph of a car alternator with a white 3D-printed mounting bracket bolted across its face; a red arrowhead at the left edge points to the bracket. Old crop started left of the photo and showed a cut stub of the caption arrow on white. The caption 'alternator bracket for a vintage car' cannot be included without the ask text's line ends (x up to 355).",
    'technology-2024-HL-paper-secA-q5-art':
        "Resistor colour-code material printed for the question: on the left the list 'Resistor bands: Brown, Black, Red, Gold' beside a photograph of a resistor with brown, black, red and gold bands; in the middle a Tolerance code table (Brown 1%, Red 2%, Gold 5%, Silver 10%) with a colour swatch beside each; on the right a Colour code table with swatches giving Black 0, Brown 1, Red 2, Orange 3, Yellow 4, Green 5, Blue 6, Violet 7, Grey 8, White 9.",
    'technology-2024-HL-paper-secA-q8-art':
        'Exploded view of a garden lantern, its parts stacked vertically: a wire carrying handle and small finial at the top, a small green cap, a wide green conical lid, a yellow translucent glass shade, a green threaded collar ring, a grey cylindrical light unit and a green dome-shaped base. Old crop took in the ruled answer-box border and the empty sketch area; the new rect sits inside the box around the exploded parts only.',
    'technology-2024-HL-paper-secA-q9-art':
        'Table headed Light Emitting Diode with a small picture of each LED: Red LED, Orange LED, Yellow LED and Green LED. The row Voltage drop at 20 mA reads 1.8 V for red, 2.0 V for orange, 2.3 V for yellow and 3.0 V for green.',
    'technology-2024-HL-paper-secB-q2b-art':
        'Photograph of a white wall-mounted smart-home controller hub: a small touchscreen on the left showing lighting and temperature sliders, and three vertical touch-slider switches on the right being pressed by a finger.',
    'technology-2024-HL-paper-secB-q3d-art':
        'Rendering of a prototype cycling helmet in pale grey with an orange-tinted face shield visor at the front, a band of red LED light segments along the side, and a mesh inner liner with chin straps.',
    'technology-2024-HL-paper-secC-q1b-art':
        'Photograph of a green solar-powered animal deterrent on a ground spike: a small solar panel on top, a motion sensor between two round speakers on the front, and curved lines either side showing sound being emitted.',
    'technology-2024-HL-paper-secC-q1d-art':
        "Photograph of a pneumatic can crusher: a silver pneumatic cylinder pushes a ram into a box holding a drinks can, with a red arrow labelled 'Crush stroke' pointing in the ram's direction of travel; below, a crushed can and a white basket of crushed cans.",
    'technology-2024-HL-paper-secC-q2c-art':
        "Graph of a thermistor's characteristic curve: Resistance (kΩ) from 0 to 50 on the vertical axis against Temperature (°C) from -10 to 50 on the horizontal axis. The blue curve falls steeply from about 50 kΩ at -10°C through about 8 kΩ at 0°C and flattens to almost 0 kΩ above 20°C.",
    'technology-2024-HL-paper-secC-q4a-art':
        "Photograph of a personalised laser-cut wooden presentation piece shaped like a graduation cap, engraved '2020 Congrats!' with the name 'EMILY' on a raised plaque, standing on a wooden base.",
    'technology-2024-HL-paper-secC-q4c-art':
        'Graph titled Bathtub Curve: Failure rate on the vertical axis against Time on the horizontal axis. The purple curve starts high and falls quickly in region A, stays low and flat across the long region B, then rises sharply in region C; dashed orange lines divide A, B and C.',
    'technology-2024-HL-paper-secC-q5b-art':
        "Photograph of a grey handheld barcode scanner with a pistol grip and an orange trigger; a red arrow labelled 'Casing' points to its moulded plastic body.",
    'technology-2024-OL-paper-secA-q10-art':
        'Screenshot of a CAD software window: toolbars across the top, a feature tree down the left side, and a grey 3D model of a triangular flanged bearing housing with a central boss and three bolt holes.',
    'technology-2024-OL-paper-secA-q11-art':
        'Graph of the bathtub curve: Failure Rate on the vertical axis against Time on the horizontal axis. The blue curve falls steeply from a high point A to B, runs low and flat from B to C, then rises steeply from C to a high point D.',
    'technology-2024-OL-paper-secA-q12-art':
        'Line drawing, without shading, of an adjustable desk lamp: a bell-shaped shade with the bulb visible, two parallel arms joined at a pivot, and a hinged joint on a domed base. Old crop took in the ruled answer-box border and the empty space either side of the lamp; the new rect sits inside the box around the drawing only.',
    'technology-2024-OL-paper-secA-q2-art':
        'Photograph of a slim dark-grey RFID-blocking wallet with a strap closure; a fanned stack of grey payment cards rises out of the top of its metal card case.',
    'technology-2024-OL-paper-secA-q4-art':
        'Photograph of a small black rectangular DC buzzer with a slotted top and mounting tabs, with a red and a black wire lead coming from it.',
    'technology-2024-OL-paper-secA-q5-art':
        'Exploded, cut-away graphic of a digital SLR camera: the lens, lens hood, grip, top dials and internal circuit boards are pulled apart from the body to show how the parts fit together.',
    'technology-2024-OL-paper-secA-q9-art':
        'Photograph of a compact hairdryer in a turquoise-to-lilac gradient finish, with a black nozzle at the front, a short angled handle with a side switch, and a looped black cord at the base.',
    'technology-2024-OL-paper-secB-q2b-art':
        "Photograph of the underside of a skateboard deck held up in the air, showing one wheel set: two cream wheels on an axle mounted in a metal truck bolted to the deck, with an arrow labelled 'Truck' pointing to it.",
    'technology-2024-OL-paper-secB-q3c-art':
        "Line drawing in plan of the JA1 aircraft's wing with two rotor pods. An arrow labelled 'Fulcrum' points to the wing root at the left; a blue dimension line marks 3 m from there to the outer motor pod, where an upward arrow is labelled 50 N; an arrow labelled 'Motor' points to the outer pod.",
    'technology-2024-OL-paper-secC-q1a-art':
        'Photograph of a pale blue and lilac automated bubble-blower toy with a carry handle on top, a fan opening at the front with bubble wands, and a stream of bubbles floating out to the left.',
    'technology-2024-OL-paper-secC-q1c-art':
        'Photograph of a white robotic vacuum cleaner, a round disc with a side brush and a top sensor, docked at the base of its tall white charging and self-emptying station.',
    'technology-2024-OL-paper-secC-q1d-art':
        'Pneumatic symbol for a single-acting cylinder: a rectangular cylinder body with a piston on the left, a return spring drawn as a zigzag inside, a piston rod extending out to the right, and a single air port line below the left end. Old crop clipped the air port line below the cylinder and the end of the piston rod.',
    'technology-2024-OL-paper-secC-q2a-art':
        'Photograph of a red 5 mm LED with two straight metal legs, one longer (anode) than the other (cathode).',
    'technology-2024-OL-paper-secC-q2b-art':
        "Part of a 555 monostable circuit: two resistors from the +V rail, a push switch to pin 2, capacitor C (with + marked) from pins 6 and 7 to the 0 V rail, pins 8 and 4 tied to +V through a switch, pin 1 to 0 V, and pin 3 marked as the output with nothing connected. Old crop began left of x 341.6 and carried the full stop of the stem's 'diagram.'",
    'technology-2024-OL-paper-secC-q3a-art':
        'Photograph of a man wearing a white virtual reality headset strapped over his eyes, lit in pink and blue, with another person blurred in the background.',
    'technology-2024-OL-paper-secC-q4b-art':
        'Graph of a projected product lifecycle: Sales on the vertical axis against Time on the horizontal axis, divided by orange lines into years 1, 2, 3 and 4. Sales start low and rise slowly in year 1, climb steeply in year 2, peak in year 3 and decline in year 4.',
    'technology-2024-OL-paper-secC-q5c-art':
        'Photograph of a black three-spoke sports steering wheel with a padded rim and a central hub plate.',
    'technology-2024-OL-paper-secC-q5d-art':
        'Photograph looking through a car windscreen with a wiper blade across it; the glass is tinted blue-purple where the sunlight falls on it.',
    'technology-2025-HL-paper-secA-q10-art':
        'Colour photograph of the X Series workstation. A man reclines in a black, angular lounge chair on a splayed metal base, facing a wheeled desk frame that holds two laptops, two small speakers and a wide monitor raised on an upright stand.',
    'technology-2025-HL-paper-secC-q1d-art':
        'Colour photograph of Sophia, the humanoid robot, from the chest up: a realistic female face with a smile, a transparent cap at the back of the head showing grey machinery, and a pale grey blazer over a black top with small lights at the chest.',
    'technology-2025-HL-paper-secC-q4b-art':
        'A cost graph: Cost (€) from 0 to 8000 against Quantity from 0 to 400. A steep blue line A rises from the origin, and a shallower red line B starts at 3000. They cross at point C, at a quantity of 200 and a cost of 4000. The region X between them before C is shaded green, and the region Y after C is shaded pink.',
    'technology-2025-HL-paper-secC-q4d-art':
        'The Product-Process Matrix: Volume of Product on the vertical axis (High at the top) against Standardisation on the horizontal axis (High at the right). Four coloured boxes climb as a staircase from bottom left to top right: A in blue at the bottom, then B in pale green, C in bright green and D in orange at the top.',
    'technology-2025-HL-paper-secC-q5d-art':
        'Colour photograph of a red Hegner scroll saw: a grey square work table over a red motor housing, with a long overhead arm holding the thin vertical blade at the front, a blue flexible air line beside the blade and a hold-down foot above the table.',
    'technology-2025-OL-paper-secA-q5-art':
        'Colour photograph of a single axial resistor lying diagonally: a beige body with brown, black, brown and gold colour bands and a thin wire lead from each end.',
    'technology-2025-OL-paper-secA-q6-art':
        'Colour photograph, in a thin black frame, looking up at the corner of an unclad steel warehouse frame against a blue sky: grey steel columns and beams on several levels, with lighter purlins and rails running between them.',
    'technology-2025-OL-paper-secA-q7-art':
        'Colour photograph of a small wooden box with rounded edges and a curved, sloping front, finished in a high-gloss clear lacquer that shows the figured grain and reflects the light.',
    'technology-2025-OL-paper-secA-q8-art':
        'Colour photograph of a light-coloured wooden cup holder clamped over the arm of a dark grey sofa: a square top with a round hole holding a white mug, and a side panel running down the outside of the arm, fixed with small screws.',
    'technology-2025-OL-paper-secA-q9-art':
        'Colour photograph of a simple circuit laid out on white: a small DC motor with red end cap at the top, a white two-cell battery box with springs below it, and a black push-to-make switch at the bottom, joined by green and red wires.',
    'technology-2025-OL-paper-secC-q1b-art':
        "Above, a colour photograph of a hand pointing a remote control at a brown sliding metal gate, with radio waves drawn from the remote. Below, the start of a flowchart for the student to complete: a green Start box with an arrow down to a purple diamond decision labelled Button. The diamond's right-hand exit loops back up to Start, and its lower exit is an open arrow pointing down.",
    'technology-2025-OL-paper-secC-q1c-art':
        'A rendered CAD model of a six-axis robotic arm in orange and grey: a round grey base, a rotating waist, upper and lower arm links joined at orange joints, and a wrist ending in a small magenta tool.',
    'technology-2025-OL-paper-secC-q1d-art':
        'Colour photograph of a gloved hand holding a grey and blue pneumatic hand drill as it drills down into a board, throwing up sawdust. A red coiled air hose is connected to the base of the handle.',
    'technology-2025-OL-paper-secC-q2a-art':
        'Colour photograph, in a thin black frame, of rows of dark blue solar photovoltaic panels mounted on a sloping tiled house roof under a blue sky with white clouds.',
    'technology-2025-OL-paper-secC-q2b-art':
        'Colour photograph of a miniature DC motor: a silver cylindrical can with a thin output shaft at the front, a cut-out window in its side, and a small solder tab at the back.',
    'technology-2025-OL-paper-secC-q2d-art':
        'Colour photograph of a phototransistor: a small metal can with a clear glass lens in its end and three long gold-coloured leads.',
    'technology-2025-OL-paper-secC-q3d-art':
        'A wedding photograph of a couple standing by a mountain lake, split down the middle to show a brightness adjustment. The left half is dark and underexposed; the right half is brightened, so the grass, hills and sky are clearly lit.',
    'technology-2025-OL-paper-secC-q4a-art':
        'The CE marking: the two letters C and E in heavy black, each drawn as an open circle, the E with a short middle bar.',
    'technology-2025-OL-paper-secC-q5c-art':
        "Colour photograph, in a thin black frame, of a black driver club head resting on the grass behind a white golf ball on a tee, with the golfer's legs and shoes standing behind it.",
    'technology-2026-HL-paper-secA-q15-art':
        "A photograph of a child's wooden climbing arch: two curved plywood sides, each ending in a looped foot at both ends, joined across the top of the arch by rungs painted cream, blue, pink, yellow, light pink and orange.",
    'technology-2026-HL-paper-secA-q3-art':
        'A series circuit: a 12 V cell at the bottom feeds a 10 ohm resistor on the left, then a 40 ohm resistor with a voltmeter V connected in parallel across it, then a second 10 ohm resistor on the right, back to the cell.',
    'technology-2026-HL-paper-secA-q8-art':
        'A plain black outline drawing of a cordless drill seen from the side: the screwdriver bit and chuck at the left, the motor body, the trigger and grip, and the battery pack at the base, with no shading or colour.',
    'technology-2026-HL-paper-secC-q5a-art':
        'A photograph of a dark grey cast-iron outdoor pizza oven: a ribbed dome with a lid on top, a chimney collar and an arched front opening, inside which logs lie on a pale stone floor that extends out as a lip in front.',
    'technology-2026-HL-paper-secC-q5b-art':
        "A photograph of a petrol multi-function gardening tool: an orange two-stroke engine at the top of a long straight shaft with a loop handle and a trigger grip, ending at the bottom right in a cutting head with an orange guard over a four-point blade. An inset, labelled 'Safety guard' with a red arrow, shows a close-up of the orange plastic guard over the blade.",
    'technology-2026-HL-paper-secC-q5c-art':
        'Three framed photographs of interchangeable attachments for the multi-function gardening tool: top left a hedge-trimmer head with a long toothed double-sided cutter bar; top right a pole-saw head, a grey and orange gearbox driving a chainsaw bar and chain; bottom right a brush-cutter head with an orange guard over a trimmer-line spool.',
    'technology-2026-OL-paper-secA-q12-art':
        'A plain black outline drawing of a soap dispenser: a tapered round bottle with a collar at the shoulder and a pump head on top with a long angled spout pointing right, with no shading or colour.',
    'technology-2026-OL-paper-secA-q5-art':
        'A photograph of a small electronic component: a round disc with a red-brown edge and a pale face crossed by a dark zig-zag track, standing on two long thin wire legs.',
    'technology-2026-OL-paper-secA-q6-art':
        'A photograph of a playground see-saw: a long yellow beam with a green middle section pivoting on a central yellow stand with four splayed feet, a green seat and an upright yellow handle with a green grip near each end.',
    'technology-2026-OL-paper-secA-q7-art':
        "A photograph of a polished stainless-steel saucepan with a glass lid and a looped lid handle, and a looped metal handle on each side; a red arrow points to the right-hand side handle, labelled 'Handle'. The tip of the left-hand handle (about 5 pt) is clipped: it overhangs the right edge of the ruled answer box below it.",
    'technology-2026-OL-paper-secA-q8-art':
        'A photograph of a home-gym weights bench: a black padded seat and inclined back rest with red edging on a black steel frame, two tall uprights with bar rests at the back, and padded leg-curl rollers at the front.',
    'technology-2026-OL-paper-secB-q2b-art':
        "A photograph of a clear plastic phone cover seen from the back, with a dark rim, a cut-out for the camera at the top left, side button covers and a printed white ring for magnetic charging in the middle. The caption 'Phone cover' and the shaft of its arrow are left out (the caption shares its x-range with the ask's word 'cover'); the arrow's red tip shows at the cover's lower left edge.",
    'technology-2026-OL-paper-secB-q3d-art':
        'A photograph of a small silver cylindrical DC motor with a thin metal output shaft at the left end and two solder tabs (its terminals) on the plastic end cap at the right.',
    'technology-2026-OL-paper-secC-q1b-art':
        "A photograph of a motorised turntable display: a red sports car on a round black turntable inside a clear acrylic case on a black base, lit by four small spotlights on stalks, one at each corner; a red arrow labelled 'LED light' points to one of the spotlights.",
    'technology-2026-OL-paper-secC-q1c-art':
        'A photograph of an orange industrial robot arm in a factory, its jointed arm reaching down with a gripper over a cardboard box on a conveyor line.',
    'technology-2026-OL-paper-secC-q1d-art':
        "A photograph of a worker's hands using a green and black pneumatic nail gun on timber boards, with a coiled blue air hose attached to its handle and a red air compressor behind.",
    'technology-2026-OL-paper-secC-q2b-art':
        'A circuit diagram: a battery on the left and a push switch in the top rail; a variable resistor labelled A above a light dependent resistor labelled B (in a circle with two arrows pointing at it) form a potential divider whose middle point feeds, through a resistor, the base of an NPN transistor; the transistor switches a bulb in the right-hand branch.',
    'technology-2026-OL-paper-secC-q2d-art':
        "A photograph of a diode: a small black cylindrical body with a grey band at one end, and a long straight silver wire lead coming out of each end, lying on a diagonal. The lower-left lead's tip loses about 3 pt so the crop leaves out the end of the word 'circuits.' printed beside it.",
    'technology-2026-OL-paper-secC-q4b-art':
        'A graph of a product lifecycle: Sales on the vertical axis against Time on the horizontal axis. A curve rises slowly, then steeply, levels off at a peak and falls away; orange vertical lines divide it into four stages numbered 1, 2, 3 and 4 along the top.',
    'technology-2026-OL-paper-secC-q5a-art':
        "A photograph of a rustic coffee table in a living room: a plank top of warm brown timber on a dark metal frame with four large cast-iron wheels, holding plants and ornaments; a red arrow labelled 'Hardwood' points to the table top.",
    'technology-2026-OL-paper-secC-q5b-art':
        "A close-up photograph of one corner of the coffee table, captioned 'Leg assembly': a dark steel bracket fixed under the corner of the timber top holds a large spoked cast wheel on an axle.",
})

# Looked at and turned down, with what is wrong with each.
REJECTED = {
    'technology-2021-OL-paper-secA-q11-art': 'an empty ruled answer box, not a picture',
    'technology-2023-HL-paper-secA-q7-art': 'a ruled answer line is clipped along the bottom edge',
    'technology-2023-HL-paper-secA-q13-art': 'the empty two-row answer box, not a picture',
    'technology-2024-HL-paper-secC-q4d-art': 'the axis titles of the lifecycle graph are clipped',
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
    # Superseded by a by-eye rect of the whole circuit (tech_crops.BY_EYE).
    # 'technology-2021-HL-paper-secC-q2b-art': the 555 chip alone, no circuit
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
    if len(rules) >= 3:
        return True
    # A wordless box drawn ENTIRELY from horizontal and vertical strokes, with
    # no image inside it, is ruling: the two-row box a candidate writes an
    # answer in. Grouping the artwork by cluster made this the largest thing
    # in a dozen bands and it published as the picture. A real drawing gives
    # itself away -- a photograph is an image, a flowchart has arrowheads, a
    # pneumatic symbol has diagonal hatching, a gate has curves.
    for im in page.get_images(full=True):
        for r in page.get_image_rects(im[0]):
            if not (r.x1 < x0 or r.x0 > x1 or r.y1 < y0 or r.y0 > y1):
                return False
    for d in page.get_drawings():
        r = d['rect']
        if r.x1 < x0 - 2 or r.x0 > x1 + 2 or r.y1 < y0 - 2 or r.y0 > y1 + 2:
            continue
        for item in d.get('items', []):
            if item[0] in ('c', 'qu'):
                return False                     # a curve: a real drawing
            if item[0] == 'l':
                (ax, ay), (bx, by) = item[1], item[2]
                if abs(ax - bx) > 2 and abs(ay - by) > 2:
                    return False                 # a diagonal: a real drawing
    return True


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


def clusters(art):
    """The artwork in a band, grouped into the separate PICTURES it holds.

    The union of every drawing in a band is not one picture. Technology's
    short questions print the answer boxes on the left and the photograph on
    the right, both inside the same band, and a box drawn around the whole
    question welds them together -- so the union spans the page and takes the
    ask with it. Rects that touch or nest belong to one picture; rects with
    clear air between them do not.

    Tried largest first, because the biggest cluster in a band is the picture
    far more often than not, and each is tested on its own merits anyway.
    """
    groups = []
    for a in sorted(art, key=lambda r: (r[1], r[0])):
        for g in groups:
            if any(not (a[2] < b[0] - 6 or a[0] > b[2] + 6
                        or a[3] < b[1] - 6 or a[1] > b[3] + 6) for b in g):
                g.append(a)
                break
        else:
            groups.append([a])
    # One pass of merging, because a rect added late can join two groups.
    merged = True
    while merged:
        merged = False
        for i in range(len(groups)):
            for j in range(i + 1, len(groups)):
                if any(not (a[2] < b[0] - 6 or a[0] > b[2] + 6
                            or a[3] < b[1] - 6 or a[1] > b[3] + 6)
                       for a in groups[i] for b in groups[j]):
                    groups[i] += groups.pop(j)
                    merged = True
                    break
            if merged:
                break
    def area(g):
        return ((max(a[2] for a in g) - min(a[0] for a in g))
                * (max(a[3] for a in g) - min(a[1] for a in g)))
    return sorted(groups, key=area, reverse=True)


def _fit(page, art, top, bottom, grow):
    """The publishable rectangle around `art`, or None.

    `grow` says whether the box may take in the lines printed INSIDE the
    artwork's own columns -- the labels and the caption. It is tried both
    ways: with growth first, because a label belongs with its picture, and
    without it second, because Technology's two-column spread means the
    grown box sometimes reaches a line of the ask and the ungrown one does
    not. Nineteen crops were refused outright for a label the picture could
    have done without.
    """
    x0 = min(a[0] for a in art)
    y0 = min(a[1] for a in art)
    x1 = max(a[2] for a in art)
    y1 = max(a[3] for a in art)
    art_top, art_bottom = y0, y1
    if (x1 - x0) < 46 or (y1 - y0) < 34:
        return None
    if grow:
        for _ in range(6):
            grew = False
            for (bx0, by0, bx1, by1), t in lines(page):
                if bx1 <= x0 or bx0 >= x1 or by1 <= y0 or by0 >= y1:
                    continue
                if x0 - 1 <= bx0 and bx1 <= x1 + 1 \
                        and y0 - 1 <= by0 and by1 <= y1 + 1:
                    continue
                if bx0 < x0 - 2 or bx1 > x1 + 2:
                    continue                  # reaches out of the columns
                y0, y1 = min(y0, by0), max(y1, by1)
                grew = True
            if not grew:
                break
    # Rendering shows whatever the rectangle covers, so a line still crossing
    # it has to be got out of the way. The prose column runs BESIDE the
    # picture and its first or last line often reaches into the picture's top
    # or bottom corner, so the box is clipped back off it. A line crossing the
    # MIDDLE cannot be clipped away, and that crop is refused.
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
    # What survives has to still BE the picture, not a strip of it: the clip
    # may take the labels, never the artwork.
    if y0 > art_top + 4 or y1 < art_bottom - 4:
        return None
    if (x1 - x0) < 46 or (y1 - y0) < 34:
        return None
    if y1 - y0 > page.rect.height * 0.66:
        return None
    if y0 < top - 8 or y1 > bottom + 8:
        return None
    return (x0 - 4, y0 - 4, x1 + 4, y1 + 4)


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
                    # The WHOLE band's artwork first: where it fits, it is
                    # the most complete picture -- 2024 Higher Q5 prints the
                    # resistor beside its own list of colour bands, and either
                    # half alone is a worse crop than the two together. Only
                    # where the union cannot be published are the separate
                    # pictures inside it tried.
                    for group in [art] + clusters(art):
                        for grow in (True, False):
                            rect = _fit(page, group, top, bottom, grow)
                            if rect:
                                return path, n, rect
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
    cards, refused, examples, verdicts, stats = TA.author(bind_figures=False)
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


def _whiteout(page, key):
    """Blank the prose fragments tech_crops.WHITEOUT lists for this crop:
    the ends of lines the paper wraps around the picture, on white ground."""
    for r in TC.WHITEOUT.get(key, []):
        shape = page.new_shape()
        shape.draw_rect(pymupdf.Rect(*r))
        shape.finish(color=(1, 1, 1), fill=(1, 1, 1))
        shape.commit()


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
    items = worklist()
    for key in TC.BY_EYE:
        yr, lv, sec, qq, le, _roman = TC.parse_key(key)
        if (yr, lv, sec, qq, le) not in items:
            items.append((yr, lv, sec, qq, le))
    for year, level, section, q, letter in items:
        paths = sorted(
            os.path.join(PAPERS, f)
            for f in os.listdir(PAPERS)
            if re.fullmatch(rf'{year}-{level}(-\d+)?-paper\.pdf', f))
        key = key_for(year, level, section, q, letter)
        if key in TC.BY_EYE:
            booklet, page_no, rect = TC.BY_EYE[key]
            got = (TC.paper_path(year, level, booklet), page_no, tuple(rect))
        else:
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
        seen[stamp] = key
        if args.write:
            with pymupdf.open(path) as doc:
                doc[page].get_pixmap(clip=pymupdf.Rect(*rect), dpi=200).save(
                    os.path.join(args.dir, f'{key}.png'))
        cut.append((year, level, section, q, letter, key, rect, False, path, page))

    # By-eye rects the worklist loop could not reach: one keyed to a single
    # roman ("q6-ii", the lever diagram that only (ii) asks about).
    done = {c[5] for c in cut}
    for key, (booklet, page_no, rect) in TC.BY_EYE.items():
        if key in done:
            continue
        yr, lv, sec, qq, le, _roman = TC.parse_key(key)
        path = TC.paper_path(yr, lv, booklet)
        if args.write:
            with pymupdf.open(path) as doc:
                _whiteout(doc[page_no], key)
                doc[page_no].get_pixmap(clip=pymupdf.Rect(*rect), dpi=200).save(
                    os.path.join(args.dir, f'{key}.png'))
        cut.append((yr, lv, sec, qq, le, key, tuple(rect), False, path, page_no))
    # By-eye rects the worklist loop could not reach: one keyed to a single
    # roman ("q6-ii", the lever diagram that only (ii) asks about).
    done = {c[5] for c in cut}
    for key, (booklet, page_no, rect) in TC.BY_EYE.items():
        if key in done:
            continue
        yr, lv, sec, qq, le, _roman = TC.parse_key(key)
        path = TC.paper_path(yr, lv, booklet)
        if args.write:
            with pymupdf.open(path) as doc:
                _whiteout(doc[page_no], key)
                doc[page_no].get_pixmap(clip=pymupdf.Rect(*rect), dpi=200).save(
                    os.path.join(args.dir, f'{key}.png'))
        cut.append((yr, lv, sec, qq, le, key, tuple(rect), False, path, page_no))
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
                _whiteout(doc[page], key)
                doc[page].get_pixmap(clip=pymupdf.Rect(*rect), dpi=200).save(
                    os.path.join(dest, f'{key}.png'))
            catalogue.append({
                'file': f'{key}.png', 'kind': 'figure', 'truncated': False,
                'description': REVIEWED[key],
                'questionRef': (f'{year} {level.upper()} Section {section} '
                                f'Q{q}' + (f'({letter})' if letter else '')),
                # Where the crop was cut, so tech_crops.paper_labels can take
                # the picture's own lettering (a chart's cells, a caption)
                # off the ask the walker read it into.
                'booklet': os.path.basename(path).split('-')[2],
                'page': page, 'rect': [round(v, 1) for v in rect],
            })
        for key, (page_no, rect, description) in TC.SOLUTIONS.items():
            yr, lv, sec, qq, le, roman = TC.parse_key(key)
            dest = os.path.join(ROOT, 'exam-papers', 'technology', 'figures',
                                f'{yr}-{lv}')
            os.makedirs(dest, exist_ok=True)
            with pymupdf.open(TC.scheme_path(yr, lv)) as doc:
                _whiteout(doc[page_no], key)
                doc[page_no].get_pixmap(clip=pymupdf.Rect(*rect), dpi=200).save(
                    os.path.join(dest, f'{key}.png'))
            catalogue.append({
                'file': f'{key}.png', 'kind': 'figure', 'truncated': False,
                'description': description,
                # The scheme's own answer: held back until the student has
                # committed to one of their own (chem_figures.py's rule).
                'solution': True,
                'questionRef': (f'{yr} {lv.upper()} Section {sec} Q{qq}'
                                + (f'({le})' if le else '')
                                + (f'({roman})' if roman else '')),
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
