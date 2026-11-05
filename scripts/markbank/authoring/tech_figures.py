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

# 2019 Higher (Technology lane, 4 November 2026).
REVIEWED.update({
    'technology-2019-HL-paper-secA-q2-art':
        'Photograph of a hand writing beside an open silver laptop, a black '
        'USB-C cable plugged into the side of the laptop and lying across the desk.',
    'technology-2019-HL-paper-secA-q4-art':
        'Cutaway rendering of a gearbox: a threaded shaft, labelled Part A is '
        'attached to a motor, meshing with a toothed bronze gear on the output '
        'shaft, labelled Gear B has 50 teeth.',
    'technology-2019-HL-paper-secA-q5-art':
        'Rendering of a student-built buggy: a flat chassis frame of coloured rods '
        'and linkages carrying four chunky wheels on two axles, with a curved wire '
        'roll bar over a round platform.',
    'technology-2019-HL-paper-secA-q6-art':
        'Drawing of an electronic component: a red wire coil on an iron core '
        'connected to + and − terminals through a switch, a hinged L-shaped '
        'arm above the core, and three upright contact strips beside it.',
    'technology-2019-HL-paper-secA-q7-art':
        'Product lifecycle graph: sales on the vertical axis against time, a '
        'curve rising slowly, climbing steeply, levelling off and then falling, '
        'divided by dashed lines into stages lettered A, B, C and D.',
    'technology-2019-HL-paper-secA-q8-art':
        'Photograph of a recumbent exercise bike with a console screen, a mesh '
        'seat back and handles, its pedal labelled Pedal.',
    'technology-2019-HL-paper-secA-q11-art':
        'Drawing of a pulley system hanging from a beam: two fixed pulleys at '
        'the top and a moving pulley below them carrying a 90 KG weight, the '
        'rope ending in a downward pull F, with a 500 mm rise marked beside it.',
    'technology-2019-HL-paper-secA-q13-art':
        'Photograph of a stepper motor with a toothed belt running round the '
        'pulley wheel on its shaft, the pulley ringed in red and linked to a '
        'large empty red circle drawn for the sketch.',
    'technology-2019-HL-paper-secA-q14-art':
        'Circuit diagram: a 12 V supply with current IT through R1 = 6 Ω, then '
        'two parallel branches to 0 V, one of R2 = 8 Ω in series with R3 = 4 Ω '
        'and the other R4 = 12 Ω.',
    'technology-2019-HL-paper-secA-q15-art':
        'Outline line drawing of a USB flash drive in pictorial view, unshaded, '
        'with a slide button on top and the metal connector at the front.',
    'technology-2019-HL-paper-secB-q2b-art':
        'Small drawing of a solar panel on a post, with curved blue arrows '
        'showing it turning about a vertical axis and tilting about a horizontal one.',
    'technology-2019-HL-paper-secB-q2b-iii-art':
        'Graph of power output (0 to 100%) against time from 5:00 to 19:00: the '
        'orange Tracked curve reaches full output early and holds it until late '
        'afternoon, while the blue Fixed curve rises to a single peak around midday.',
    'technology-2019-HL-paper-secB-q3b-art':
        'Photograph of the treadmill belt mechanism opened up: a green belt of '
        'jointed slats running over end rollers on a metal frame.',
    'technology-2019-HL-paper-secC-q1c-art':
        'Photograph of a silver double-acting pneumatic cylinder with its piston '
        'rod extended and two air ports on the barrel.',
    'technology-2019-HL-paper-secC-q3b-art':
        'Network diagram of a small business LAN: an internet cloud, components '
        'lettered A and B in line from it, a server, a component C joining rows '
        'of networked computers, and a component D with wireless links to two '
        'laptops.',
    'technology-2019-HL-paper-secC-q3d-i-art':
        'A browser address bar with a padlock symbol and the URL '
        'https://www.rugbyworldcup.com/supporters.',
})

# 2016 Ordinary (Technology lane, 5 November 2026).
REVIEWED.update({
    'technology-2016-OL-paper-secA-q1-art':
        'Photographs of an orange wristband activity tracker, one showing its '
        'digital display.',
    'technology-2016-OL-paper-secA-q2-art':
        'Photograph of a bike rack carved like a giant wooden comb, lying on a '
        'pavement with bicycles parked in its teeth.',
    'technology-2016-OL-paper-secA-q4-art':
        'Drawing of the inside of a 3-pin plug: the three coloured wires '
        'screwed to the pins, the cable grip, and an arrow lettered A to the '
        'fuse.',
    'technology-2016-OL-paper-secA-q6-art':
        'Photograph of a bicycle whose frame is a white 3D-printed lattice, '
        'with bright green tyres.',
    'technology-2016-OL-paper-secA-q7-art':
        'Photograph of a child\'s chair cut from two dark panels with round '
        'holes, joined by a wooden seat and a yellow horned backrest, with an '
        'arrow lettered A pointing at its side.',
    'technology-2016-OL-paper-secA-q8-art':
        'Photograph of a green LED mounted on a printed circuit board beside a '
        'chip and resistors.',
    'technology-2016-OL-paper-secA-q9-art':
        'Photograph of two toothed wheels, a small one and a large one, joined '
        'by a loop of roller chain.',
    'technology-2016-OL-paper-secA-q10-art':
        'Photograph of a blue bench-top machine with a C-shaped arm over a '
        'round cutting table, a clear guard and a hold-down foot.',
    'technology-2016-OL-paper-secA-q12-art':
        'Line drawing in pictorial view of a claw hammer.',
    'technology-2016-OL-paper-secB-q2b-art':
        'Photograph of a green pet water and food dispenser: a base lettered A, '
        'a water container lettered B on an upright column lettered C, and a '
        'food bowl.',
    'technology-2016-OL-paper-secB-q2d-art':
        'Photograph of a model aeroplane made from card.',
    'technology-2016-OL-paper-secB-q3b-art':
        'Photograph of a white drone with a camera attached beneath it, and an '
        'enlarged view of the camera on its rotating mount.',
    'technology-2016-OL-paper-secC-q1a-art':
        'Photograph of a purple furry toy with large ears and eyes.',
    'technology-2016-OL-paper-secC-q1b-art':
        'Photograph of a grey jointed robotic arm on a round base, with a '
        'gripper at its end.',
    'technology-2016-OL-paper-secC-q1c-art':
        'A robotic arm holding its hand out, the load of 25 N at the hand and '
        'the distance 0.35 m from the elbow to the hand marked below it.',
    'technology-2016-OL-paper-secC-q1d-i-art':
        'Two drawings headed Shuttle Valve, each a ball in a horizontal pipe '
        'between inlets marked Source 1 and Source 2, with an outlet marked Out '
        'below: in the first the ball is pushed to the right, in the second to '
        'the left.',
    'technology-2016-OL-paper-secC-q1d-ii-art':
        'Photograph of a small black air compressor with a pressure gauge and a '
        'car-socket plug.',
    'technology-2016-OL-paper-secC-q2a-art':
        'Photographs of a black plug-in power adapter, front and side, with a '
        'yellow voltage selector dial.',
    'technology-2016-OL-paper-secC-q2b-art':
        'Circuit: a switch, a variable resistor and a sensor position lettered A '
        'feeding a transistor through a resistor; the transistor switches a '
        'relay with a protective diode, and the relay contacts switch a motor M '
        'on a separate battery.',
    'technology-2016-OL-paper-secC-q2c-art':
        'Two resistors, 200 ohms and 100 ohms, connected in parallel between +V '
        'and 0V.',
    'technology-2016-OL-paper-secC-q2d-art':
        'A logic circuit, inputs A and B into gate X giving C, and C into gate Y '
        'giving D; beside it a truth table with columns A, B, C and D, A and B '
        'filled in (00, 01, 10, 11) and C and D blank.',
    'technology-2016-OL-paper-secC-q4a-art':
        'Photographs of a packet of crisps and of a bronze statue of a sports '
        'player.',
    'technology-2016-OL-paper-secA-q3-art':
        'A photograph of a folding Solar Paper charger, two panels of solar '
        'cells on a table, connected by a cable to a smart phone, with an arrow '
        'to the panels labelled Solar Paper.',
    'technology-2016-OL-paper-secC-q4b-art':
        'A table of the percentage of customers giving each reason: Overpriced '
        '50, Wait time 30, Unfriendly staff 9, Food not fresh 7, Too noisy 4.',
    'technology-2016-OL-paper-secC-q4c-art':
        'A perceptual map: a vertical axis from Low Quality to High Quality '
        'crossing a horizontal axis from Low Price to High Price, with five '
        'products plotted as dots and a New Product? label in the high quality, '
        'low price quarter.',
    'technology-2016-OL-paper-secC-q5a-art':
        'Photograph of a round wooden bowl turned from a single piece of timber.',
    'technology-2016-OL-paper-secC-q5b-art':
        'Two magazine racks: a Metal Rack of scrolled black bars with its Main '
        'body and Leg labelled, and a red bent-acrylic Plastic Rack with a slot '
        'lettered A and its outline shown as Detail of slot A.',
    'technology-2016-OL-paper-secC-q5d-art':
        'Photograph of a pack of brightly coloured baby feeding spoons.',
})

# 2016 Higher (Technology lane, 5 November 2026).
REVIEWED.update({
    'technology-2016-HL-paper-secA-q6-art':
        'A resistor with coloured bands, and a circuit: R1 in series with R2 '
        '= 5 ohms and R3 = 20 ohms connected in parallel.',
    'technology-2016-HL-paper-secA-q8-art':
        "A 'bathtub' graph of Failure rate against Time: a high early failure "
        'rate falling into a long flat middle and rising again at the end, '
        'divided into Phase 1, 2 and 3.',
    'technology-2016-HL-paper-secA-q9-art':
        'Photograph of a testing machine: a red frame with a vertical plunger '
        'resting on a cam on a shaft with gears.',
    'technology-2016-HL-paper-secA-q10-i-art':
        'Photograph of a hand on a bicycle handlebar squeezing the black brake '
        'lever.',
    'technology-2016-HL-paper-secA-q10-ii-art':
        'Lever diagram: a beam with the fulcrum (an orange triangle) at the '
        'right end, a Load of 300 N 20 mm from the fulcrum, and the Effort at '
        'the left end 120 mm from the fulcrum.',
    'technology-2016-HL-paper-secA-q13-art':
        'Exploded rendering of a hairdryer: the nozzle, a mesh grille, the '
        'heater core, the fan and motor housing with its rear grille, and the '
        'handle with its switch and cable.',
    'technology-2016-HL-paper-secA-q14-art':
        'Photograph of a blue wind-up torch with a black folding crank handle, '
        'a textured grip and a wrist strap.',
    'technology-2016-HL-paper-secA-q15-art':
        'Line drawing in pictorial view of a remote control with a round '
        'four-way pad and a group of rounded buttons.',
    'technology-2016-HL-paper-secB-q2b-art':
        'Photograph of a prosthetic hand with jointed finger linkages, a double '
        'arrow at the thumb and finger, and an arrow to the palm labelled '
        'motors and battery housing.',
    'technology-2016-HL-paper-secC-q1c-art':
        'Rendering of a robot arm on an upright column, arrows showing it moving '
        'up and down and its two arm sections turning.',
    'technology-2016-HL-paper-secC-q1d-art':
        'Drawing of a table tennis ball dispenser: a hopper of yellow balls, '
        'labelled Table tennis balls, above a channel, with a horizontal '
        'cylinder labelled Pneumatic actuator.',
    'technology-2016-HL-paper-secC-q2b-art':
        'An incomplete circuit between + and -: a variable resistor above an '
        'LDR, and R1 above R2, feeding the two inputs of an op-amp whose output '
        'goes through a resistor to an LED.',
    'technology-2016-HL-paper-secC-q2c-art':
        'A block diagram, Entry to De-bounce to Count to Display, with Reset '
        'below Count, and a photograph of a digital counter display.',
    'technology-2016-HL-paper-secC-q2d-art':
        'A logic circuit: A into gate 1 giving X; B and C into gate 2 giving Y; '
        'X and Y into gate 3 giving Z.',
    'technology-2016-HL-paper-secC-q4b-art':
        'A control chart: a line of readings wandering about the average '
        'between dotted lines marked UCL above and LCL below, one late reading '
        'above the UCL.',
    'technology-2016-HL-paper-secC-q5b-art':
        'A blue self-balancing scooter with arrows to its Pedal pads with '
        'anti-slip surface and its Plastic housing, and a photograph labelled '
        'Detail of the two-part metal chassis with an arrow to the Central '
        'pivot.',
})

# 2017 Ordinary (Technology lane, 4 November 2026).
REVIEWED.update({
    'technology-2017-OL-paper-secA-q1-art':
        'Graphic of figures at an emergency exit door, one in a wheelchair and '
        'one crawling, with a long vertical bar on the door labelled Handle.',
    'technology-2017-OL-paper-secA-q2-art':
        'Graphic of a wall-mounted heating controller linked to a phone, a '
        'mobile and a laptop.',
    'technology-2017-OL-paper-secA-q3-art':
        'Photographs of a small white and green portable washing machine, closed '
        'and open, with an arrow lettered A to its outer body.',
    'technology-2017-OL-paper-secA-q4-art':
        'Photograph of a light dependent resistor with its two legs, labelled '
        'LDR.',
    'technology-2017-OL-paper-secA-q5-art':
        'Three safety signs: a head wearing a helmet in white on a blue disc; a '
        'lightning arrow in a yellow triangle; a running figure on a red '
        'prohibition disc.',
    'technology-2017-OL-paper-secA-q6-art':
        'Photograph of a pillar drill table mechanism: a toothed bar up the '
        'column, lettered A, and a blue crank handle.',
    'technology-2017-OL-paper-secA-q7-art':
        'Photograph of a silver hand dryer, with an arrow lettered A pointing '
        'at its side.',
    'technology-2017-OL-paper-secA-q8-art':
        'A work breakdown structure: Start leads to tasks A, B and C; A leads '
        'to D, then F and H; B and C lead to E, then G; H and G lead to Finish.',
    'technology-2017-OL-paper-secA-q9-art':
        'Photograph of a red tin of liquid solvent cement.',
    'technology-2017-OL-paper-secA-q10-art':
        'Graphic of a fishing rod hooking a bank card out of a tablet screen.',
    'technology-2017-OL-paper-secA-q11-art':
        'A green wheelbarrow, and under it a lever diagram: a beam with the '
        'load L pressing down between the fulcrum F at one end and the effort '
        'E at the other.',
    'technology-2017-OL-paper-secA-q12-art':
        'Line drawing in pictorial view of a plastering trowel: a flat '
        'rectangular blade with a curved handle along its centre.',
    'technology-2017-OL-paper-secB-q2a-art':
        'Photograph of a woman wearing a yellow neck scarf device, and a '
        'close-up of the yellow and black neck piece.',
    'technology-2017-OL-paper-secB-q2b-art':
        'Photograph of an orange and black neck piece, an arrow to its outer '
        'casing labelled Outer Shell.',
    'technology-2017-OL-paper-secB-q2c-art':
        'Photograph of three USB cable ends labelled Micro-USB, Mini-USB and '
        'USB.',
    'technology-2017-OL-paper-secB-q2d-art':
        'The CE mark: the letters C and E in bold black curves on white.',
    'technology-2017-OL-paper-secB-q3a-art':
        'Photograph of a toy wooden sports utility vehicle with orange parts '
        'and black wheels, its base labelled Base A, and beneath it the kit of '
        'parts it is assembled from.',
    'technology-2017-OL-paper-secB-q3b-art':
        'Circuit between +V and 0V: a variable resistor, an On/Off switch and '
        'a capacitor lettered X feeding a transistor that switches a buzzer.',
    'technology-2017-OL-paper-secB-q3c-art':
        'Photograph of the chain and sprocket drive on an all-terrain vehicle.',
    'technology-2017-OL-paper-secB-q3c-ii-art':
        'A large sprocket labelled Driven joined by a chain to a small '
        'sprocket labelled Driver.',
    'technology-2017-OL-paper-secB-q3d-art':
        'Rendering of an all-terrain vehicle frame with its wheels and red '
        'suspension units.',
    'technology-2017-OL-paper-secC-q1a-art':
        'Photograph of a laptop showing a flowchart program, a cable and a PIC '
        'project board.',
    'technology-2017-OL-paper-secC-q1b-art':
        'Photograph of a long black electric sliding gate closed across an '
        'entrance, its motor housing at the side.',
    'technology-2017-OL-paper-secC-q1b-i-art':
        'The flowchart printed for completion: Start, Button? (N loops back), '
        'Motor Forward, Micro-Switch? (N loops back), Motor Stop, and an arrow '
        'continuing down.',
    'technology-2017-OL-paper-secC-q1c-art':
        'Photograph of a pneumatic nail gun fixing a board, its yellow air hose '
        'behind.',
    'technology-2017-OL-paper-secC-q1d-art':
        'Rendering of a robotic arm inside a shaded cylinder labelled Work '
        'Envelope.',
    'technology-2017-OL-paper-secC-q2a-art':
        'Photograph of an outdoor floodlight with a motion sensor beneath it.',
    'technology-2017-OL-paper-secC-q2b-art':
        'A photograph of a hand opening a window, and a logic circuit: Window '
        '(Window open = 1) and Keypad (Alarm On = 1) feed gate X, whose output '
        'feeds gate Y to the Alarm, Y latched by a push-to-break switch in its '
        'feedback loop.',
    'technology-2017-OL-paper-secC-q2c-art':
        'Photographs of an LED with two legs, labelled LED, and a black piezo '
        'buzzer with red and black wires, labelled Mini-Siren.',
    'technology-2017-OL-paper-secC-q3a-art':
        'Photograph of a boy at a computer rubbing his eyes.',
    'technology-2017-OL-paper-secC-q3b-art':
        'Photograph of a teacher drawing on an interactive whiteboard.',
    'technology-2017-OL-paper-secC-q3c-art':
        'Photograph of hands using an online banking login screen on a tablet.',
    'technology-2017-OL-paper-secC-q3d-art':
        'Photograph of a tablet computer showing its start screen.',
    'technology-2017-OL-paper-secC-q4a-art':
        'A round green and yellow logo reading The Sandwich Shop around a '
        'drawing of a sandwich.',
    'technology-2017-OL-paper-secC-q4b-art':
        'Photographs of a sandwich being made at a counter, captioned '
        'Made-to-order sandwich, and of a sandwich in a plastic pack.',
    'technology-2017-OL-paper-secC-q4c-art':
        'A cause and effect diagram, Cause on the left and Effect on the right, '
        'with branches Equipment, Process, Staff, Ingredients, Environment and '
        'Management leading to Poor Quality Bread.',
    'technology-2017-OL-paper-secC-q5a-art':
        'Photograph of a desk lamp with a black metal shade on a jointed '
        'plywood frame shaped like a sitting dog.',
    'technology-2017-OL-paper-secC-q5b-art':
        'Close-up photograph of the desk lamp: its black shade on the jointed '
        'plywood frame.',
    'technology-2017-OL-paper-secC-q5c-art':
        'Three steps of blow moulding: Step 1, a tube of plastic hanging in an '
        'open mould; Step 2, air blown in, arrows pushing outward; Step 3, the '
        'formed bottle.',
    'technology-2017-OL-paper-secC-q5d-art':
        'The ISO logo: the letters ISO in white across a globe, on a blue '
        'square.',
})

# 2017 Higher (Technology lane, 4 November 2026).
REVIEWED.update({
    'technology-2017-HL-paper-secA-q2-art':
        'A worm meshing with a worm wheel, beside a photograph of a white car '
        'on a round showroom turntable.',
    'technology-2017-HL-paper-secA-q3-art':
        'Part of a circuit: a component lettered A connected across a coil '
        'lettered B whose switch contacts lead off to the right, the coil '
        'driven through a transistor with a base resistor.',
    'technology-2017-HL-paper-secA-q8-art':
        'Four safety signs lettered A to D: A, a white fire extinguisher and '
        'flames on red; B, an exclamation mark in a yellow triangle; C, a white '
        'cross on green; D, a white exclamation mark on a blue disc.',
    'technology-2017-HL-paper-secA-q11-art':
        'Two tables: the colour code (0 Black, 1 Brown, 2 Red, 3 Orange, 4 '
        'Yellow, 5 Green, 6 Blue, 7 Violet, 8 Grey, 9 white) and the tolerance '
        'code (1% Brown, 2% Red, 5% Gold, 10% Silver).',
    'technology-2017-HL-paper-secA-q12-art':
        'A small driving gear of 13 teeth meshing with a large gear of 52 '
        'teeth, a second 13-tooth gear on the same shaft meshing with a second '
        '52-tooth driven gear; a curved arrow shows the driving gear turning '
        'anticlockwise. Labelled Driving Gear, Driven Gear, 13 Teeth and 52 '
        'Teeth.',
    'technology-2017-HL-paper-secA-q13-art':
        'Line drawing in pictorial view of a curved smartwatch band with a '
        'display panel.',
    'technology-2017-HL-paper-secA-q15-art':
        'Exploded view of a prototype mobile phone, its layers labelled Touch '
        'screen, Solar charging layer, Display and Circuit.',
    'technology-2017-HL-paper-secC-q1c-art':
        'Photograph of a robot arm sorting through waste on a conveyor.',
    'technology-2017-HL-paper-secC-q1d-art':
        'Two pneumatic symbols: A, a valve with a ball between two inlets and '
        'one outlet; B, a variable restrictor in parallel with a non-return '
        'valve.',
    'technology-2017-HL-paper-secC-q2a-art':
        'Photograph of an analogue chess clock with two dials behind chess '
        'pieces on a board.',
    'technology-2017-HL-paper-secC-q2b-art':
        'Incomplete circuit for a game timer: a 10 k resistor and a variable '
        'resistor R1 above a 100 uF capacitor C1, a push switch, and a 555 IC '
        'drawn as a box.',
    'technology-2017-HL-paper-secC-q2c-art':
        'A table of npn transistors and their current gain (BC107 100-450, '
        'BFY51 40, TIP31 10-60, 2N3055 20-70), and Fig. 1: two transistors '
        'connected together, with base current IB in and collector current IC.',
    'technology-2017-HL-paper-secC-q2d-art':
        'Photograph of a yellow electric cut-off saw on its base.',
    'technology-2017-HL-paper-secC-q4c-art':
        'The Product-Process Matrix: Volume of product (Low to High) against '
        'Standardisation (Low to High), with four blocks stepping up from A at '
        'low volume and standardisation through B and C to D at high.',
    'technology-2017-HL-paper-secC-q4d-art':
        'A table of costs: Solid panels, fixed costs 500 euro and variable costs '
        '3 euro per unit; Stiffened panels, fixed costs 1000 euro and variable '
        'costs 2 euro per unit.',
    'technology-2017-HL-paper-secC-q4b-iii-art':
        'The formula as printed: where Cp = Tolerance Range over 6 sigma.',
    'technology-2017-HL-paper-secC-q5b-art':
        'Photographs of a structure of curved glulam timber arches, and of a '
        'timber roof whose beams meet at a joint labelled metal node.',
    'technology-2017-HL-paper-secC-q5c-art':
        'Exploded view of a panel: two blue outer sheets with an aluminium '
        'honeycomb core between them.',
})

# 2018 Higher (Technology lane, 4 November 2026).
REVIEWED.update({
    'technology-2018-HL-paper-secA-q5-art':
        'Photograph of a floor-standing bandsaw: a tall upright frame with a '
        'table at waist height and control buttons on its side.',
    'technology-2018-HL-paper-secA-q6-art':
        'Circuit: a 500 ohm resistor in series with a 2 kilohm and a 3 kilohm '
        'resistor connected in parallel.',
    'technology-2018-HL-paper-secA-q7-art':
        'Cutaway rendering of a gearbox: shafts carrying several gear wheels and '
        'bearings inside an open casing.',
    'technology-2018-HL-paper-secA-q11-art':
        'Rendering of a cam-operated device: a toothed wheel on a black upright, '
        'a part circled in red and lettered A at the top of the wheel, and a '
        'linkage running down to a cam labelled Cam C.',
    'technology-2018-HL-paper-secA-q12-art':
        'Photograph of a rescue winch mounted above the door of a red '
        'helicopter, an orange hook weight hanging from its cable.',
    'technology-2018-HL-paper-secA-q13-art':
        'Rendering of an eight-pin integrated circuit chip, printed NE555, '
        'standing on its legs.',
    'technology-2018-HL-paper-secA-q14-art':
        'Photograph of a blue gearbox housing with its input shaft labelled '
        'Input shaft A and output shaft labelled Output shaft B, and a close-up '
        'of the input shaft labelled Metal key in groove.',
    'technology-2018-HL-paper-secA-q15-art':
        'Line drawing in pictorial view of a fire extinguisher: a cylinder with '
        'a valve head, gauge, handle and nozzle.',
    'technology-2018-HL-paper-secB-q2c-art':
        'Graphic of a fleet of solar drones at different heights (30,000, 60,000 '
        'and 90,000 ft marked), each beaming a green cone of coverage down onto '
        'the houses and town below.',
    'technology-2018-HL-paper-secB-q2d-art':
        'Circuit of a solar engine: a solar cell, a component lettered A, an '
        'IC, two transistors (one lettered B) and a motor M.',
    'technology-2018-HL-paper-secC-q1c-art':
        'Rendering of a gantry robot: a carriage running on rails along two '
        'axes, with a vertical arm carrying the gripper.',
    'technology-2018-HL-paper-secC-q2b-art':
        'Circuit: an LDR above a 15 kilohm resistor gives point A, and a 20 '
        'kilohm above a 30 kilohm resistor gives point B, the two feeding the '
        'inputs of an op-amp between +6 V and 0 V, with output Vout.',
    'technology-2018-HL-paper-secC-q2d-art':
        'Diagram of a height check: Light 1 and Light 2 shine across to two '
        'sensors, Light 1 at the maximum height, with a child walking between.',
    'technology-2018-HL-paper-secC-q4b-iii-art':
        'An empty cause and effect diagram leading to Problem, with the '
        'headings Equipment, Materials, Personnel, Environmental, Methods and '
        'Machines.',
    'technology-2018-HL-paper-secC-q4c-art':
        'Photograph of a fidget spinner, and a table of seven hole sizes in mm: '
        '3D Printer 16.08, 16.04, 16.10, 15.90, 16.08, 16.04, 15.02, sigma = '
        '.391; Laser Cutter 15.98, 15.96, 16.04, 16.03, 15.98, 16.02, 16.02, '
        'sigma = .030.',
    'technology-2018-HL-paper-secC-q4c-i-art':
        'Photograph of a fidget spinner, the table of hole sizes in mm (3D '
        'Printer 16.08, 16.04, 16.10, 15.90, 16.08, 16.04, 15.02, sigma = .391; '
        'Laser Cutter 15.98, 15.96, 16.04, 16.03, 15.98, 16.02, 16.02, sigma = '
        '.030), and the formula Cp = Tolerance Range over 6 sigma.',
    'technology-2018-HL-paper-secC-q4d-art':
        'Two graphs of sales against time in months: Graph A a smooth rise to a '
        'gentle peak and slight fall; Graph B flat, then a sudden tall spike and '
        'a steep fall.',
})

# 2018 Ordinary (Technology lane, 4 November 2026).
REVIEWED.update({
    'technology-2018-OL-paper-secA-q1-art':
        'A round safety sign: a white outline of a full-body overall on a solid '
        'blue disc.',
    'technology-2018-OL-paper-secA-q2-art':
        'Rendering of the CityTree: a tall upright panel covered in green moss, '
        'set on a curved concrete base with a wooden bench.',
    'technology-2018-OL-paper-secA-q4-art':
        'Photograph of a black plastic case that holds four AA cells side by '
        'side, with metal spring contacts at the ends.',
    'technology-2018-OL-paper-secA-q7-art':
        'Photograph of a wooden bench with crossed X-shaped legs joined by a '
        'stretcher, and an arrow lettered A pointing at its end.',
    'technology-2018-OL-paper-secA-q9-art':
        'Photograph of a bingo machine: a clear blue spherical drum with a '
        'crank handle, held between two uprights on a shaped wooden base, '
        'labelled Drum and Wooden Stand.',
    'technology-2018-OL-paper-secA-q10-art':
        'Photograph of a motorway with a steel truss gantry bridge spanning it.',
    'technology-2018-OL-paper-secA-q11-art':
        'Drawing of a pear-shaped cam labelled Cam, with a roller follower '
        'labelled Follower resting on top of it.',
    'technology-2018-OL-paper-secA-q12-art':
        'Line drawing in pictorial view of a dovetail halving joint: two '
        'lengths of timber shown apart, one with the dovetail cut on its end '
        'and the other with the matching housing.',
    'technology-2018-OL-paper-secB-q2a-art':
        'Photograph of two heavy-duty wheelbarrows, one with two wheels at the '
        'front, with an arrow to the pan labelled Pan.',
    'technology-2018-OL-paper-secB-q3a-art':
        'Photograph of a desk lamp: a lime-green plastic base with storage '
        'compartments and a curved metal pole holding a green shade, with '
        'arrows labelled Metal and Plastic.',
    'technology-2018-OL-paper-secB-q3b-art':
        'Photograph of a rotary variable resistor with a slotted shaft and three '
        'legs.',
    'technology-2018-OL-paper-secB-q3c-art':
        'Photograph of a yellow digital multimeter with a rotary selector dial, '
        'a display and red and black probes.',
    'technology-2018-OL-paper-secB-q3d-art':
        'Photograph of a prototype desk lamp: an orange glowing shade inside a '
        'white lattice shell on a small base.',
    'technology-2018-OL-paper-secC-q1b-art':
        'The start of a flowchart printed for completion: Start, then the '
        'decision Alarm? with N looping back and Y continuing down.',
    'technology-2018-OL-paper-secC-q1d-art':
        'Photographs of a claw gripper on a coiled cable, labelled Mechanical '
        'Gripper, and of a red claw machine full of soft toys.',
    'technology-2018-OL-paper-secC-q2a-art':
        'A resistor lettered R with four colour bands, beside two tables: the '
        'colour code (0 Black, 1 Brown, 2 Red, 3 Orange, 4 Yellow, 5 Green, 6 '
        'Blue, 7 Violet, 8 Grey, 9 White) and the tolerance code (1% Brown, 2% '
        'Red, 5% Gold, 10% Silver).',
    'technology-2018-OL-paper-secC-q2b-art':
        'Circuit of a 555 timer in monostable mode between +V and 0V: two '
        'resistors, a capacitor and a push switch on its inputs, and its output '
        'driving, through a resistor, a transistor lettered A that switches a '
        'buzzer.',
    'technology-2018-OL-paper-secC-q2c-art':
        'Pin diagram of a 14-pin chip holding four AND gates, pins numbered 1 '
        'to 14, with GND at pin 7 and VCC at pin 14.',
    'technology-2018-OL-paper-secC-q3c-art':
        'Photograph of a red graphics card, with an arrow to its fan labelled '
        'Fan.',
    'technology-2018-OL-paper-secC-q4a-art':
        'Three photographs captioned An oil painting, A sports club hat and '
        'Drinks bottles.',
    'technology-2018-OL-paper-secC-q4b-art':
        'A process capability graph: a red bell curve of the process between '
        'two vertical lines marked LSL and USL under the heading Design '
        'Specifications, with the tails outside them labelled Defects.',
    'technology-2018-OL-paper-secC-q5a-art':
        'Four photographs captioned Safety Helmet, Hall Table, Cooking Pot and '
        'Sports Sock.',
    'technology-2018-OL-paper-secC-q5b-art':
        'Photographs of a white folding bicycle, unfolded, and of a rider '
        'carrying it folded in half.',
})

# 2019 Ordinary (Technology lane, 4 November 2026).
REVIEWED.update({
    # Pictures the 2019 stems point at, added after the batch browser check.
    'technology-2019-OL-paper-secA-q1-art':
        'A round safety sign: a white outline of a head wearing ear defenders '
        'on a solid blue disc.',
    'technology-2019-OL-paper-secA-q3-art':
        'Photograph of a lamp: a clear acrylic sheet engraved with a cartoon '
        'panda spinning a basketball, glowing purple above a black base.',
    'technology-2019-OL-paper-secA-q7-art':
        "Photograph of a child's push-car: an oval plywood seat over a lower "
        'oval deck, a wooden handlebar and four grey wheels with red hubs, '
        'with an arrow lettered A pointing at it from the lower right.',
    'technology-2019-OL-paper-secA-q9-art':
        'Photograph of a piece of furniture bent from one continuous sheet of '
        'plywood: a flat top curving down into a side with a hand slot, with a '
        'rack for magazines underneath.',
    'technology-2019-OL-paper-secB-q2a-art':
        'CAD rendering on a grid of a blue open rectangular case with fixing '
        'lugs, beside a flat blue piece with a rectangular cut-out.',
    'technology-2019-OL-paper-secC-q1b-art':
        'Photograph of a cattle gate system: a steel overhead frame carrying a '
        'gate across a pen of cows in a holding yard.',
    'technology-2019-OL-paper-secC-q3b-art':
        'Photograph of the end of a black cable with a USB Type-C plug.',
    'technology-2019-OL-paper-secC-q4b-art':
        'Diagram: grapes labelled Input, an arrow to a factory labelled '
        'Transformation Process, an arrow to a wine bottle labelled Output, '
        'and arrows running back labelled Customer Feedback across the top and '
        'Performance Feedback across the bottom.',
    'technology-2019-OL-paper-secC-q4c-art':
        'Photograph of workers in a vineyard tipping a crate of dark grapes '
        'into a large bin.',
    'technology-2019-OL-paper-secC-q5c-ii-art':
        'Photograph of a small dog fitted with a two-wheeled support '
        'wheelchair strapped to its body, its hind legs resting on the frame.',
    'technology-2019-OL-paper-secC-q5d-art':
        'Photograph of a stack of chipboard panels, each faced with a '
        'different wood-grain veneer, their cut edges showing the chipboard '
        'core.',
    'technology-2019-HL-paper-secC-q2b-art':
        'Circuit diagram: resistors R1 and R2 and capacitor C in series '
        'between a 12 V rail and a 0 V rail, wired to a 555 IC whose output '
        'line ends unconnected.',
    'technology-2019-HL-paper-secC-q4b-art':
        'Picture of the electronic toy, a small blue robot with LED eyes, '
        'beside a table: Cost of machinery €25,000; Cost of tooling €5,000; '
        'Variable Costs €20 per unit; Sales Forecast 20,000 units.',
    'technology-2019-OL-paper-secA-q6-art':
        'Drawing of a mechanism of two parts: a grey toothed wheel lettered A '
        'with a red arrow showing its direction of turning, and a small pivoted '
        'catch lettered B resting against its teeth.',
    'technology-2019-OL-paper-secA-q8-art':
        'Photograph of a long outdoor walkway beside a flight of steps: a level '
        'pale path with green edging strips and green handrails along both sides.',
    'technology-2019-OL-paper-secA-q10-art':
        'Photograph of a desktop computer system: a tower case, a flat-screen '
        'monitor, a keyboard and a mouse.',
    'technology-2019-OL-paper-secA-q11-art':
        'Drawing of a series circuit: a battery, a striped resistor and an LED, '
        'the LED leg marked + joined to the resistor and the leg marked − '
        'returning to the battery.',
    'technology-2019-OL-paper-secA-q12-art':
        'Outline line drawing of a small rectangular table in pictorial view, '
        'unshaded, with four square legs and a rail under the top.',
    'technology-2019-OL-paper-secB-q2b-art':
        'Circuit diagram: a battery and a switch feeding a variable resistor '
        'above a component lettered A, the junction between them joined through '
        'a resistor to the base of a transistor that switches a buzzer.',
    'technology-2019-OL-paper-secC-q1d-art':
        'Photograph of a surgical robot: several robotic arms holding slender '
        'instruments over a patient model on an operating table.',
    'technology-2019-OL-paper-secC-q2a-art':
        'Photograph of a three-core electrical cable with its white outer sheath '
        'stripped back to show blue, brown and green-and-yellow insulated wires '
        'with bare copper ends.',
    'technology-2019-OL-paper-secC-q2c-art':
        'Photograph of a small cylindrical DC motor with its output shaft.',
    'technology-2019-OL-paper-secC-q2c-ii-art':
        'Model of a simple DC motor: a battery on a base board connected by '
        'green wires to a wire loop that sits between the poles of a red '
        'U-shaped magnet, with arrows showing the current.',
    'technology-2019-OL-paper-secB-q3b-art':
        'Photograph of a VR viewer made from coloured foam board: a red front '
        'panel with two eye holes and a nose cut-out between lime-green sides, '
        'a phone slotted in on top, and an arrow labelled A pointing at one side.',
    'technology-2019-OL-paper-secB-q3c-art':
        'Silhouette of a crane: a jib with a hook from which a cable labelled X '
        'holds a yellow box marked Load.',
    'technology-2019-OL-paper-secC-q1c-art':
        'Two pneumatic symbols: a cylinder with a piston and rod, captioned '
        'Double-acting cylinder, and a valve symbol with an adjustable restriction '
        'and a non-return valve, captioned Throttle valve.',
    'technology-2019-OL-paper-secC-q2b-art':
        'Circuit diagram between +V and −V rails: a double-pole switch lettered A '
        'feeding a motor M, with two push switches, one at the top and one '
        'lettered B at the bottom.',
    'technology-2019-OL-paper-secC-q2d-art':
        'Logic circuit: inputs a and b enter gate X, whose output c joins input d '
        'at gate Y, whose output is E.',
    'technology-2019-OL-paper-secC-q5b-art':
        'Photograph of a dog wheelchair with a moulded plastic saddle, aluminium '
        'struts and two wheels, an arrow A pointing at a curved slotted metal '
        'link, with an enlarged view of that link lettered A ringed in red.',
    'technology-2019-OL-paper-secC-q4a-art':
        'Photograph of a clear plastic punnet divided into three compartments '
        'holding red, green and black grapes.',
})

# Looked at and turned down, with what is wrong with each.
# 2015 Higher, each crop rendered and looked at.
REVIEWED.update({
    'technology-2015-HL-paper-secA-q5-art':
        'Three safety signs labelled (i), (ii) and (iii): a falling figure over '
        'wavy lines in a yellow triangle; a running figure, an arrow and a '
        'doorway in white on green; a hand and a figure under a red '
        'prohibition disc.',
    'technology-2015-HL-paper-secA-q9-art':
        'The internal layout of a gearbox: an Input shaft carrying gear A (80 T), '
        'meshing with gear B (40 T) on a lay shaft that also carries gear C '
        '(90 T), which meshes with gear D (50 T) on the Output shaft.',
    'technology-2015-HL-paper-secA-q12-art':
        'A photograph of the open belt guard on top of a pillar drill, showing two '
        'stepped pulleys joined by a belt.',
    'technology-2015-HL-paper-secA-q13-art':
        'A photograph of a stepper motor: a square-bodied motor with a round '
        'shaft at the front and a connector on top.',
    'technology-2015-HL-paper-secA-q15-art':
        'A line drawing of a vintage diving helmet with a round front window, '
        'two side windows, a top window and a collar with bolts.',
    'technology-2015-HL-paper-secB-q3b-art':
        'A pulley system: two pulleys, one above the other, with a rope over '
        'them, an arrow on the free end of the rope, and a 20kg weight hanging '
        'from the lower pulley.',
    'technology-2015-HL-paper-secB-q3c-art':
        'Photographs of a ball launcher: two wheels on a stand, then a strip of '
        'four frames showing a rugby ball fed between the wheels and launched.',
    'technology-2015-HL-paper-secC-q1b-art':
        'A photograph of a wooden test model of a washing machine with its round '
        'door open.',
    'technology-2015-HL-paper-secC-q1b-i-art':
        'The start of a flowchart as the paper prints it: a Start box above a '
        'decision diamond labelled On/Off, with an arrow leaving its foot.',
    'technology-2015-HL-paper-secC-q1d-art':
        'A pneumatic circuit: a push-button valve at each side, a valve labelled '
        '5/2 valve between them, a small valve symbol and a tank labelled '
        'Reservoir in the dotted pilot line, and a cylinder whose rod end is '
        'marked F.',
    'technology-2015-HL-paper-secC-q2b-art':
        'An incomplete circuit diagram between +V and 0V rails: a 555 IC with '
        'pins 4 and 8 to +V and pin 1 to 0V, a resistor R from +V to pins 7 and '
        '6, a capacitor C from there to 0V, a capacitor from pin 5 to 0V, and '
        'short open leads at pins 2 and 3.',
    'technology-2015-HL-paper-secC-q4b-art':
        'A table of furnace temperatures in degrees Celsius for Monday to Friday, '
        'with columns Morning, Midday, Evening and Daily Mean.',
    'technology-2015-HL-paper-secC-q5b-art':
        'A photograph of a modular tram-stop shelter: metal beams with circular '
        'holes supporting a glass roof, and glass side panels.',
    'technology-2015-HL-paper-secC-q5d-art':
        'A photograph of the Ann Devlin Bridge, a low road bridge over a canal '
        'with a Luas tram crossing it.',
})

# 2015 Ordinary, each crop rendered and looked at.
REVIEWED.update({
    'technology-2015-OL-paper-secA-q1-art':
        'Photograph of a folding multi-tool opened out, several tools folding '
        'out of its two handles, with a small inset photograph of a man holding '
        'one.',
    'technology-2015-OL-paper-secA-q2-art':
        'Photograph of six red LEDs, each a domed red head on two thin wire legs.',
    'technology-2015-OL-paper-secA-q5-art':
        'Photograph of a green band saw on a stand, with an arrow labelled A '
        'pointing to the knob on its top.',
    'technology-2015-OL-paper-secA-q6-art':
        'A lever diagram: a beam on a triangular fulcrum, a downward force of '
        '30N at the left end and a downward force F at the right end; 2M from '
        'the left end to the fulcrum and 5M from the fulcrum to the right end.',
    'technology-2015-OL-paper-secA-q7-art':
        'Photograph of a bench, a long wooden seat carried on two rectangular '
        'metal frames, with an arrow labelled A at the lower right pointing '
        'towards it.',
    'technology-2015-OL-paper-secA-q9-art':
        'Drawing of two toothed wheels, a large one and a small one, joined by a '
        'loop of belt with teeth on its inner face.',
    'technology-2015-OL-paper-secA-q10-art':
        'Photograph of a paper towel holder: a wooden back board with a metal '
        'rod on two metal brackets, shown empty and holding a roll of paper '
        'towel.',
    'technology-2015-OL-paper-secA-q11-art':
        'Photograph of a black laptop power adapter: a rectangular block with a '
        'coiled cable ending in a round plug.',
    'technology-2015-OL-paper-secA-q12-art':
        'Line drawing in pictorial view of a pot with a lid, a knob handle on the '
        'lid and a handle on one side.',
    'technology-2015-OL-paper-secB-q2b-art':
        'A moisture sensor circuit diagram: a battery, a switch, a pair of '
        'contacts labelled Probes, a variable resistor, and a transistor '
        'labelled Transistor switching an LED with its resistor.',
    'technology-2015-OL-paper-secB-q2b-iii-art':
        'Photograph of a green plastic water butt on a stand beside a wooden '
        'fence.',
    'technology-2015-OL-paper-secB-q2d-art':
        'Photograph of a T-shaped water pipe fitting: a black body with a blue '
        'screw-on nut at each of its three ends.',
    'technology-2015-OL-paper-secB-q3a-art':
        'Photograph of a yellow safety helmet with other protective equipment and '
        'a pair of gloves, captioned Protective Gloves with an arrow to the '
        'gloves.',
    'technology-2015-OL-paper-secB-q3b-art':
        'Photograph of a PTO shaft: a metal shaft inside an orange plastic guard, '
        'labelled PTO Shaft and Shaft guard.',
    'technology-2015-OL-paper-secB-q3c-art':
        'A CAD rendering of a PTO shaft: a grey shaft with a jointed coupling and '
        'a flange at each end.',
    'technology-2015-OL-paper-secC-q1a-art':
        'Photograph of a microcontroller chip with two rows of legs, beside an '
        'empty chip socket with matching holes.',
    'technology-2015-OL-paper-secC-q1b-art':
        'The start of a flowchart as the paper prints it: Start, a decision '
        'Guard looping back on N, then on Y a decision Switch with an arrow '
        'leaving its foot.',
    'technology-2015-OL-paper-secC-q1c-art':
        'Photograph of a spray gun: a pistol-grip gun with a metal paint cup '
        'underneath.',
    'technology-2015-OL-paper-secC-q1c-ii-art':
        'Drawing of a pneumatic component: a long rectangular body with a rod '
        'coming out of its right end; arrow A points to the lower left of the '
        'body and arrow B to the rod.',
    'technology-2015-OL-paper-secC-q2a-art':
        'Photograph of an orange excavator lifting scrap metal with a round '
        'magnet hung from its arm, labelled Electromagnet.',
    'technology-2015-OL-paper-secC-q2a-ii-art':
        'A circuit diagram: a 12V battery, a switch and a coil connected in a '
        'single loop.',
    'technology-2015-OL-paper-secC-q2b-art':
        'A circuit diagram between +V and -V rails with two components labelled '
        'A and B, a motor M, and switches wired to reverse the motor.',
    'technology-2015-OL-paper-secC-q2c-art':
        'Photograph of a lever microswitch: a black body with a metal lever on '
        'top and three terminals labelled COM, NO and NC.',
    'technology-2015-OL-paper-secC-q2d-art':
        'A logic circuit: input A into gate X giving C, and C with input B into '
        'gate Y giving D; below it a truth table with columns A, B, C and D, A '
        'and B filled in (00, 01, 10, 11) and C and D blank.',
    'technology-2015-OL-paper-secC-q2d-i-art':
        'A logic circuit: input A into gate X giving C, and C with input B into '
        'gate Y giving D.',
    'technology-2015-OL-paper-secC-q3d-art':
        'Photographs of three cable connectors labelled A, B and C: a flat '
        'rectangular metal plug, a slim round plug with bands on its tip, and a '
        'wide flat gold-tipped plug on a black cable.',
    'technology-2015-OL-paper-secC-q4b-art':
        'Photograph of a red stand food mixer with a whisk lowered into a glass '
        'bowl.',
    'technology-2015-OL-paper-secC-q4c-art':
        'A graphic of Quantity against Time: a straight line rising towards '
        'Demand, with Capacity added in yellow steps that sit above the line.',
    'technology-2015-OL-paper-secC-q5b-art':
        'Photograph of a wooden garden playhouse with a green and yellow canopy '
        'roof, swings on an A-frame and a green plastic slide.',
    'technology-2015-OL-paper-secC-q5c-art':
        'The four steps of rotational moulding drawn in a row: 1. Mould Charging '
        '(Powder in the Mould, on a Plate and Support Arm), 2. Heating (Heat '
        'arrows round the turning mould), 3. Cooling (Air/Water arrows round the '
        'turning mould), 4. Removal (the hollow moulding).',
    'technology-2015-OL-paper-secC-q5d-art':
        'Photograph of a welded joint where one round metal tube meets another, '
        'the weld bead around the joint.',
})

# 2014 Higher, each crop rendered and looked at.
REVIEWED.update({
    'technology-2014-HL-paper-secA-q3-art':
        'The plastics recycling logo: three chasing arrows in a triangle round '
        'the number 2, with HDPE printed under it.',
    'technology-2014-HL-paper-secA-q5-art':
        'Part of a transistor circuit: an NPN transistor with an ammeter marked '
        'IB in its base lead and an ammeter marked IC in its collector lead.',
    'technology-2014-HL-paper-secA-q6-art':
        'A critical path node: a box with EST in the top row, Activity Name and '
        'Duration in the middle, LST in the bottom row, and arrows X and Y '
        'pointing to the top-right and bottom-right cells.',
    'technology-2014-HL-paper-secA-q7-art':
        'Photograph of a laptop stand: a sloping platform on a hinged base.',
    'technology-2014-HL-paper-secA-q11-art':
        'A block labelled Load on a level surface, with an arrow F = 300N pushing '
        'it, and a distance of 0.85 m from position A to position B.',
    'technology-2014-HL-paper-secA-q13-art':
        'Photograph of a desktop laser printer with its paper tray open at the front.',
    'technology-2014-HL-paper-secA-q15-art':
        'Line drawing of a universal joint: two shafts joined by two forked yokes '
        'and a cross-shaped piece.',
    'technology-2014-HL-paper-secB-q2a-art':
        'The official emblem of the 2014 FIFA World Cup: a trophy shape formed '
        'by three hands in green and yellow, over FIFA WORLD CUP Brasil.',
    'technology-2014-HL-paper-secB-q3b-art':
        'A robotic arm diagram: a Motor at the left end of a bar, a 2.5 kg mass '
        'at the right end, the two 1.1 m apart; beside it a photograph of the '
        'rover arm with its Turret labelled.',
    'technology-2014-HL-paper-secB-q3c-art':
        'Photograph of the Mars rover camera system: a camera head and its '
        'electronics mounted on a small base plate.',
    'technology-2014-HL-paper-secC-q1b-art':
        'Photograph of a white wall-mounted air conditioning unit.',
    'technology-2014-HL-paper-secC-q2b-art':
        'Photograph of a plug-in ultrasonic pest deterrent with a glowing panel, '
        'and a 555 timer circuit between +V and 0V with resistors R1 and R2 and '
        'a capacitor C on pins 7, 6 and 2, a capacitor on pin 5, and pin 3 left '
        'open.',
    'technology-2014-HL-paper-secC-q2c-art':
        'A cutaway drawing of a DC motor, with arrows labelled A, B and C pointing '
        'to three of its parts.',
    'technology-2014-HL-paper-secC-q2d-art':
        'Photographs of an outdoor weather sensor on a pole and an indoor display '
        'unit, and a truth table captioned truth table with columns Switch, '
        'Night, Temp and Alarm over all eight combinations, Alarm 1 only for '
        'Switch 1, Night 0, Temp 1.',
    'technology-2014-HL-paper-secC-q3c-art':
        'A table with columns Feature and Software package; the features Slide '
        'transition, Use of counters, Mute, play and pause, and Crop, the '
        'package column blank.',
    'technology-2014-HL-paper-secC-q4b-art':
        'Photograph of a small camera lens block.',
    'technology-2014-HL-paper-secC-q4c-art':
        'Above, a product life-cycle graph of Sales against Time: a curve rising, '
        'peaking and falling, divided by vertical lines into stages numbered 1, '
        '2, 3 and 4. Below, two Sales against time graphs: Laptop computer, a '
        'curve rising quickly to a long rounded peak then falling; Electronic '
        'toy, a tall narrow spike.',
    'technology-2014-HL-paper-secC-q4d-art':
        'Photograph of a red alarm casing mounted on a wall, an arrow, and a '
        'drawing of a person on a ladder fixing the casing high on a house wall.',
    'technology-2014-HL-paper-secC-q5b-art':
        'Photograph of a computer workstation: a red seat on a steel frame with '
        'screens on an arm, labelled Steel frame and Adjustable screens.',
    'technology-2014-HL-paper-secC-q5d-art':
        'Photograph of a model hydrogen car beside a small hydrogen refuelling '
        'station and a solar panel.',
})

# 2014 Ordinary, each crop rendered and looked at.
REVIEWED.update({
    'technology-2014-OL-paper-secA-q1-art':
        'Photograph of workers in hard hats and high-visibility vests working on '
        'a large pipe section in a field.',
    'technology-2014-OL-paper-secA-q3-art':
        'A yellow triangular safety sign with a black border, showing black '
        'flames over a line.',
    'technology-2014-OL-paper-secA-q4-art':
        'Photograph at night of a cable-stayed bridge, its two towers lit blue.',
    'technology-2014-OL-paper-secA-q5-art':
        'Photograph of a clear plastic water bottle with a blue cap.',
    'technology-2014-OL-paper-secA-q6-art':
        'Photograph of a hand writing with a stylus on a small screen pad '
        'connected by a cable.',
    'technology-2014-OL-paper-secA-q7-art':
        'An exploded line drawing of a chair: the back and seat above, the frame '
        'pieces and legs separated below, and an arrow labelled A pointing at it '
        'from the lower left.',
    'technology-2014-OL-paper-secA-q8-art':
        'Photograph of an electric jig saw with its blade pointing down.',
    'technology-2014-OL-paper-secA-q9-art':
        'A resistor colour code table, colour bars for the digits 0 to 9, and a '
        'resistor with four coloured bands.',
    'technology-2014-OL-paper-secA-q10-art':
        'A rendering of a heat sensor fan: a blue fan on a curved green acrylic '
        'upright with circular holes, on a round yellow and green base.',
    'technology-2014-OL-paper-secA-q11-art':
        'Photograph of a clear plastic food container with a blue lid, holding '
        'two burgers.',
    'technology-2014-OL-paper-secA-q12-art':
        'Line drawing of a gas cylinder with a valve and a handle on top.',
    'technology-2014-OL-paper-secB-q2a-art':
        'Photograph of a cruise ship lying on its side in the water, with a '
        'crane vessel beside it.',
    'technology-2014-OL-paper-secB-q2b-art':
        'A diagram of the salvage: the ship tilted against the shore with a box '
        'labelled Caisson on its side, and a steel frame under it labelled '
        'Platform.',
    'technology-2014-OL-paper-secB-q2c-art':
        'An illustration of a satellite with solar panels above the Earth.',
    'technology-2014-OL-paper-secB-q2d-art':
        'Photograph of two cupped hands holding a green glass globe.',
    'technology-2014-OL-paper-secB-q3a-art':
        'A rendering of a pizza-slice shaped timer made of stacked layers, with '
        'an arrow captioned Layers of 3 mm Acrylic.',
    'technology-2014-OL-paper-secB-q3b-art':
        'A circuit: a push switch and capacitor feed the base of a transistor '
        'through a resistor; the transistor switches an LED and its resistor; a '
        'battery supplies the circuit.',
    'technology-2014-OL-paper-secB-q3d-art':
        'Photographs of a green printed circuit board, captioned PCB, and a '
        'copper stripboard, captioned Copper Stripboard.',
    'technology-2014-OL-paper-secC-q1a-art':
        'Photograph of a white and pink robotic toy dog with its remote control.',
    'technology-2014-OL-paper-secC-q1b-art':
        'A flowchart: Start, LDR? '
        '(N loops back), Motor Up, Limit Switch? (N loops back), Motor Stop, '
        'Wait 5, Motor Down, Limit Switch? (N loops back), Motor Stop, Stop.',
    'technology-2014-OL-paper-secC-q1c-art':
        'Photograph of a multi-rotor drone with a camera in flight.',
    'technology-2014-OL-paper-secC-q1d-art':
        'A cutaway drawing of a pneumatic valve, a push button at the left, a '
        'spring at the right, with arrows numbered 1 and 2 pointing to a port '
        'and to the spring.',
    'technology-2014-OL-paper-secC-q2a-art':
        'Photograph of a small chip held between a finger and thumb.',
    'technology-2014-OL-paper-secC-q2b-art':
        'Photograph of an eight-pin chip marked NE555N.',
    'technology-2014-OL-paper-secC-q2c-art':
        'Photograph of a small yellow plastic gearbox motor.',
    'technology-2014-OL-paper-secC-q2d-art':
        'A circuit between +V and 0V: a resistor in series with a light emitting '
        'diode.',
    'technology-2014-OL-paper-secC-q3a-art':
        'A weather map of Europe on a globe, with city names and temperatures.',
    'technology-2014-OL-paper-secC-q3b-art':
        'Photograph of an eye close up behind a finger touching a glass screen.',
    'technology-2014-OL-paper-secC-q3c-art':
        'A screenshot of a CAD export dialog: File name, Export type with a '
        'drop-down list of file formats, and Export, Cancel and Options buttons.',
    'technology-2014-OL-paper-secC-q3d-art':
        'A blue wireless signal symbol: a dot under three arcs.',
    'technology-2014-OL-paper-secC-q4a-art':
        'Photographs of a kite surfer in the air and of a black and red water '
        'sports harness, captioned Water Sports Harness.',
    'technology-2014-OL-paper-secC-q4b-art':
        'A control chart with a UCL line at the top and an LCL line at the '
        'bottom, a dashed centre line, and a plotted line of samples, '
        'labelled Samples taken from the process.',
    'technology-2014-OL-paper-secC-q4c-art':
        'An organisational chart: Managing Director above four departments, '
        'Sales and Marketing, Production, Human Resources and Finance.',
    'technology-2014-OL-paper-secC-q4d-art':
        'Photograph of a team of people working at laptops around a table.',
    'technology-2014-OL-paper-secC-q5a-art':
        'Three photographs captioned Engineered Wood - door panels, Medium '
        'Density Fibreboard - (MDF) furniture panels, and Oriented Strand Board '
        '- (OSB) flooring panels.',
    'technology-2014-OL-paper-secC-q5b-art':
        "Photograph of a child's folding scooter, with an arrow labelled A "
        'pointing to its base.',
    'technology-2014-OL-paper-secC-q5d-art':
        'The Forest Stewardship Council logo: a tree drawn as a tick over the '
        'letters FSC.',
})

# 2013 Higher, each crop rendered and looked at.
REVIEWED.update({
    'technology-2013-HL-paper-secA-q1-art':
        'Aerial photograph of a hydro-electric station on a wide river channel '
        'between fields.',
    'technology-2013-HL-paper-secA-q2-art':
        'Photograph of a child\'s bead maze toy: coloured beads on looped wires '
        'over two shaped bases.',
    'technology-2013-HL-paper-secA-q3-art':
        'A rendering of a geodesic dome built from triangular frames.',
    'technology-2013-HL-paper-secA-q4-art':
        'Photograph of a yellow mining helmet with a lamp on the front.',
    'technology-2013-HL-paper-secA-q6-art':
        'Photograph of an electric motor with a shaft at one end and a terminal '
        'box on top.',
    'technology-2013-HL-paper-secA-q7-art':
        'Photograph of a digital camera with a zoom lens.',
    'technology-2013-HL-paper-secA-q8-art':
        'A gear train drawn as pitch circles: Gear A 40 teeth meshing with Gear B '
        '20 teeth; Gear C 60 teeth on the same shaft as Gear B, meshing with '
        'Gear D 15 teeth.',
    'technology-2013-HL-paper-secA-q9-art':
        'A mobile crane lifting a load marked 1000 N, with an arrow showing a '
        'lift of 6 m.',
    'technology-2013-HL-paper-secA-q10-art':
        'Three yellow triangular safety signs: flames; a liquid dripping from '
        'test tubes onto a hand and a surface; a lightning bolt.',
    'technology-2013-HL-paper-secA-q11-art':
        'Photographs of a wall-mounted can crusher being used, and a diagram of '
        'it with parts labelled link arm, main arm, pivot pin and can.',
    'technology-2013-HL-paper-secA-q12-art':
        'A process chart from Start to dress bear (15 mins) through three '
        'parallel lines: cut clothes (10 mins), sew clothes (10 mins), '
        'embroidery (10 mins); cut fur (10 mins), stuff/sew fur (30 mins); cut '
        'accessories (3 mins), sew accessories (10 mins).',
    'technology-2013-HL-paper-secA-q13-art':
        'Photograph of the Dublin Convention Centre, a building with a tilted '
        'glass drum at its front.',
    'technology-2013-HL-paper-secA-q14-art':
        'Photograph of a red schoolbag with its parts labelled Straps, Body and '
        'Fastener.',
    'technology-2013-HL-paper-secA-q15-art':
        'An exploded line drawing of a stool: the seat and two bent legs pulled '
        'apart along dotted lines, captioned Exploded view.',
    'technology-2013-HL-paper-secB-q2a-art':
        'Photograph of a pack of Sugru mouldable glue.',
    'technology-2013-HL-paper-secB-q2b-art':
        'Four photographs of Sugru in use: a moulded grip on a winder handle, on '
        'a hacksaw handle, as a phone stand, and on a tap handle.',
    'technology-2013-HL-paper-secB-q2c-art':
        'A drawing of a relay: a coil on an iron core, a pivoted armature and a '
        'pair of switch contacts, with arrows labelled A, B and C.',
    'technology-2013-HL-paper-secB-q2d-art':
        'A logic circuit: switches A and B into an OR gate; B also through a NOT '
        'gate; the OR and NOT outputs into an AND gate giving C.',
    'technology-2013-HL-paper-secB-q3b-art':
        'Photographs of an athlete on a hand-pedalled tricycle and of the '
        'tricycle, and a drawing of two sprockets joined by a chain, captioned '
        'drive-chain.',
    'technology-2013-HL-paper-secB-q3d-art':
        'Photograph of a skydiver in a pressure suit and helmet in free fall.',
    'technology-2013-HL-paper-secC-q1a-art':
        'Photograph of an orange robotic arm welding, sparks flying.',
    'technology-2013-HL-paper-secC-q1c-art':
        'Photograph of a white humanoid robot waving.',
    'technology-2013-HL-paper-secC-q1d-art':
        'A pneumatic circuit: a push-button valve captioned 5/2 Valve connected '
        'by two lines to a double-acting cylinder.',
    'technology-2013-HL-paper-secC-q2a-art':
        'Photograph of an LED torch, and the note R = (Voltage - Vf) over If, '
        'written as a fraction.',
    'technology-2013-HL-paper-secC-q2b-art':
        'A voltage divider between +6V and 0V: a light dependent resistor R1 '
        'above a fixed resistor R2 = 5600 ohms, with the output V taken between '
        'them.',
    'technology-2013-HL-paper-secC-q2d-art':
        'A garage alarm circuit: switches marked door and window feed a box '
        'marked Logic Gate, whose output drives a transistor switching a buzzer.',
    'technology-2013-HL-paper-secC-q3b-art':
        'An illustration of a wireless router linked to two laptops and a phone.',
    'technology-2013-HL-paper-secC-q3c-art':
        'Photograph of a laptop on a cooling stand, arrows showing air flow.',
    'technology-2013-HL-paper-secC-q4a-art':
        'Photograph of five smartphones standing in a row.',
    'technology-2013-HL-paper-secC-q4b-art':
        'A data table, Day (July 11th to July 19th) and No. of defects (10, 8, '
        '11, 10, 9, 10, 12), above pictures of a production line, a cereal box '
        'and a bowl of cornflakes.',
    'technology-2013-HL-paper-secC-q4c-art':
        'A perceptual map: a vertical axis from Low Cost to Expensive crossing a '
        'horizontal axis from Economy to Performance, with A circled in the low '
        'cost, economy quarter and B in the expensive, performance quarter.',
    'technology-2013-HL-paper-secC-q4d-art':
        'Photographs of croissants on a tray, tablet computers, and cars on an '
        'assembly line.',
    'technology-2013-HL-paper-secC-q5b-art':
        'Photographs of a door wedge, captioned Door wedge with siren is placed '
        'at the bottom of door to limit entry, and a red key fob, captioned Key '
        'fob alarm is activated by pressing button to emit a high-pitched sound.',
    'technology-2013-HL-paper-secC-q5c-art':
        'Photograph of a blue vacuum-formed toy car body.',
    'technology-2013-HL-paper-secC-q5d-art':
        'Photograph of shredded plastic waste in a glass column above a yellow '
        'liquid.',
})

# 2013 Ordinary, each crop rendered and looked at.
REVIEWED.update({
    'technology-2013-OL-paper-secA-q1-art':
        'Two library logos: a figure reading a book on a blue square, captioned '
        '1982, and a figure at a laptop in a blue circle, captioned 2009.',
    'technology-2013-OL-paper-secA-q2-art':
        'Photograph of a racing yacht heeling in the sea, arrows labelled Sail '
        'and Hull.',
    'technology-2013-OL-paper-secA-q3-art':
        'Aerial photograph of a rocket standing on its launch pad.',
    'technology-2013-OL-paper-secA-q4-art':
        'Photograph of a black slide switch with three pins underneath.',
    'technology-2013-OL-paper-secA-q5-art':
        'Photograph of a scroll saw on a bench with a dust hose and a red '
        'stop button.',
    'technology-2013-OL-paper-secA-q6-art':
        "The Saorview logo, captioned Ireland's free digital television service.",
    'technology-2013-OL-paper-secA-q7-art':
        'A rendering of a red two-step footstool with an arrow labelled A '
        'pointing at its side.',
    'technology-2013-OL-paper-secA-q8-art':
        'Photograph of a keyring torch with a small solar panel on top and '
        'three LEDs shining.',
    'technology-2013-OL-paper-secA-q9-art':
        'Photograph of two cone-shaped toothed gears meshing at an angle.',
    'technology-2013-OL-paper-secA-q10-art':
        'A rendering of a blue folded acrylic phone holder with circular holes.',
    'technology-2013-OL-paper-secA-q11-art':
        'A square black and white QR code, three corner markers and a block pattern.',
    'technology-2013-OL-paper-secA-q12-art':
        'Line drawing of a jug-shaped electric kettle with a handle and a switch.',
    'technology-2013-OL-paper-secB-q2a-art':
        'Photograph of a heap of short cylindrical wood pellets.',
    'technology-2013-OL-paper-secB-q2b-art':
        'An exploded view of a carbon monoxide alarm: a cover labelled Casing, a '
        'circuit board labelled PCB and a tray labelled Base.',
    'technology-2013-OL-paper-secB-q2d-art':
        'A diagram of a gas well: a drilling rig above ground and a pipe turning '
        'sideways below a layer labelled Water Table, cracks spreading from it.',
    'technology-2013-OL-paper-secB-q3a-art':
        'Photograph of a tennis racket with a white and red frame.',
    'technology-2013-OL-paper-secB-q3b-art':
        'Photograph of an exercise machine with a padded seat and leg rollers, '
        'an arrow labelled A pointing to its frame.',
    'technology-2013-OL-paper-secB-q3c-art':
        'Two children on a see-saw, labelled Child A and Child B, and the pivot '
        'labelled Fulcrum.',
    'technology-2013-OL-paper-secB-q3d-art':
        'A cause and effect diagram: Causes Materials, Machinery used to '
        'manufacture, People and Methods of assembly leading to the Effect, '
        'Faulty exercise machine.',
    'technology-2013-OL-paper-secC-q1a-art':
        'An 18 pin PIC chip with each pin labelled.',
    'technology-2013-OL-paper-secC-q1b-art':
        'A flowchart: Start, LDR? looping back on N, Motor On, Wait 20, Motor '
        'Off, Stop; beside it a photograph of a window blind, labelled Blind.',
    'technology-2013-OL-paper-secC-q1c-art':
        'Photograph of an air compressor with arrows labelled Electric Motor, '
        'Pump and Reservoir, and below it the symbol of a pneumatic component, '
        'a cylinder with a spring.',
    'technology-2013-OL-paper-secC-q1d-art':
        'A line drawing of a robot inside the outline of the space it can '
        'reach, labelled Work Envelope.',
    'technology-2013-OL-paper-secC-q2a-art':
        'Photographs labelled A, B and C: a yellow box with two sockets, a small '
        'solar panel with leads, and two coin-shaped cells.',
    'technology-2013-OL-paper-secC-q2b-art':
        'A circuit between +V and 0V: a push switch A, a variable resistor and a '
        'resistor charging a capacitor B, feeding a pair of transistors that '
        'drive a motor with a fan.',
    'technology-2013-OL-paper-secC-q2d-art':
        'An integrated circuit marked 4071 with its pins numbered, and an '
        'enlarged balloon detail of one gate with pins 4, 5 and 6.',
    'technology-2013-OL-paper-secC-q3a-art':
        'Photograph of an Irish Rail train with a WiFi logo.',
    'technology-2013-OL-paper-secC-q3b-art':
        'A laptop advertisement: Hard Disk 640GB / 6GB RAM / Operating System '
        'Windows 7, 64 Bit / WiFi Connectivity / Multi Card Reader / 4 USB Ports '
        '/ Screen Resolution 1920x1080 Pixels / Blue Ray Disc Rewritable and DVD '
        'Multi Drive, beside a photograph of the laptop.',
    'technology-2013-OL-paper-secC-q3c-art':
        'An orange button reading Online Booking with a hand cursor.',
    'technology-2013-OL-paper-secC-q3d-art':
        'A yellow sign reading Prevent Cyberbullying!',
    'technology-2013-OL-paper-secC-q4a-art':
        'Photograph of a blue five-door concept car, seen from the front.',
    'technology-2013-OL-paper-secC-q4b-art':
        'Photograph of four glass jars of orange and lemon marmalade.',
    'technology-2013-OL-paper-secC-q4d-art':
        'A box labelled Container with a card circled on its side, and the card '
        'enlarged: Part Description Mirror-Left-Door, Part Number 2542, Qty 200, '
        'Lead Time 1 week, Order Date 11/10, Supplier Ace Car Parts Ltd, Due '
        'Date 18/10, Planner Mary K., Location Rack 2A.',
    'technology-2013-OL-paper-secC-q5a-art':
        'Photographs captioned Pottery vase, rain jacket and Toothbrush bristles.',
    'technology-2013-OL-paper-secC-q5b-art':
        'A rendering of a docking station for an MP3 player, two stacks of '
        'acrylic shelves with arrows labelled A, B and C, and a photograph of a '
        'metal tube captioned Aluminium tube insert.',
    'technology-2013-OL-paper-secC-q5c-art':
        'A diagram of two soldered joints on a board: GOOD JOINT (volcano shape), '
        'shiny solder, and BAD JOINT (dry joint), dull solder, with copper tracks, '
        'component, component lead and PCB or stripboard labelled.',
    'technology-2013-OL-paper-secC-q5d-art':
        'Photograph of a hand holding a Kindle e-book reader.',
})

# 2012 Higher, each crop rendered and looked at.
REVIEWED.update({
    'technology-2012-HL-paper-secA-q1-art':
        'Photograph of a row of wind turbines on green land under a rainbow.',
    'technology-2012-HL-paper-secA-q2-art':
        'Two pieces of corrugated cardboard, shown in section with their wavy '
        'inner layer.',
    'technology-2012-HL-paper-secA-q3-art':
        'Photograph of a sailing dinghy at sea with arrows labelled Sail, Mast '
        'and Hull.',
    'technology-2012-HL-paper-secA-q4-art':
        'Photograph of a red armchair made of stacked rounded cushions on a '
        'curved tubular metal base.',
    'technology-2012-HL-paper-secA-q5-art':
        'Photograph of a tower crane beside a tall building under construction.',
    'technology-2012-HL-paper-secA-q6-art':
        'A computer symbol: a trident shape, an arrow, a circle and a square on '
        'three branches from a single stem ending in a dot.',
    'technology-2012-HL-paper-secA-q8-art':
        'Photograph of a wooden pull-along dog toy with pink ears, tail and '
        'wheels and a pink pull cord.',
    'technology-2012-HL-paper-secA-q9-art':
        'A rendering of a supermarket checkout counter with a scanner and a '
        'conveyor.',
    'technology-2012-HL-paper-secA-q10-art':
        'A yellow gantry crane on wheels, and its diagram: a beam on pillars A '
        'and B with upward arrows, a load of 285 N hanging 1m from A and 2m from '
        'B.',
    'technology-2012-HL-paper-secA-q11-art':
        'A voltage divider between +6V and 0V: an LDR above a resistor R = 1k '
        'ohm, the output Vout taken between them.',
    'technology-2012-HL-paper-secA-q12-art':
        'Photograph of a ball bearing cut away to show its balls between an '
        'inner and an outer ring.',
    'technology-2012-HL-paper-secA-q13-art':
        'Photograph of an open laptop computer, its screen and keyboard seen at an angle.',
    'technology-2012-HL-paper-secA-q14-art':
        'Four safety signs: (i) Yellow - caution, flames in a yellow triangle; '
        '(ii) Blue - mandatory, a head wearing ear defenders on a blue disc; '
        '(iii) Red - fire, an extinguisher and flames on red; (iv) Green - '
        'positive action, a running figure, an arrow and a door on green.',
    'technology-2012-HL-paper-secA-q15-art':
        'Line drawing of a bicycle saddle with a section cut away to show its '
        'padding.',
    'technology-2012-HL-paper-secB-q2a-art':
        'A rendering of a large oval stadium seen from above.',
    'technology-2012-HL-paper-secB-q2b-art':
        'A round green circuit board with LEDs, and three components pointed to '
        'it labelled A (a round black component), B (a small cylinder) and C '
        '(a square push button).',
    'technology-2012-HL-paper-secB-q2c-art':
        'A product life-cycle graph of Product Sales against Time: a curve '
        'rising, peaking and falling, split by dashed lines into stages 1, 2, '
        '3 and 4.',
    'technology-2012-HL-paper-secB-q3a-art':
        'A cutaway drawing of a hybrid car labelled Fuel Tank, Battery Pack, '
        'Engine, Electronic control system and Electric Motor.',
    'technology-2012-HL-paper-secB-q3b-art':
        'A carburettor linkage: an accelerator pedal pivoted at B on a fixed '
        'pivot, its foot end A, linked at C through a spring and a rod to a '
        'lever on the carburettor with its own fixed pivot.',
    'technology-2012-HL-paper-secB-q3c-art':
        'Photograph of a sports car in a wind tunnel, smoke lines flowing over it.',
    'technology-2012-HL-paper-secB-q3d-art':
        'A drawing of an incomplete car steering system: a steering wheel on a '
        'column above two front wheels joined by a bar.',
    'technology-2012-HL-paper-secC-q1a-art':
        'Photograph of a tracked robot with an arm and cameras.',
    'technology-2012-HL-paper-secC-q1b-art':
        'Photograph of a wall-mounted hand dryer with a slot for hands.',
    'technology-2012-HL-paper-secC-q1c-art':
        'A rendering of a gantry robot over a flat bed, its head moving on rails.',
    'technology-2012-HL-paper-secC-q1d-art':
        'Photograph of a machine pressing a tennis ball under a piston.',
    'technology-2012-HL-paper-secC-q2a-art':
        'The RSA logo, white letters on an orange square.',
    'technology-2012-HL-paper-secC-q2b-art':
        'An incomplete 555 astable circuit between 9V and 0V, R1, R2 and C1 on '
        'its pins, output to two LEDs with a resistor R3 marked; beside it a red '
        'triangular warning sign with a row of LEDs.',
    'technology-2012-HL-paper-secC-q2c-art':
        'A circuit between 6V and 0V: a component A across a relay coil in a '
        'dotted box with switch contacts B on a 110V motor circuit, and a '
        'transistor C with ammeters in its base (IB) and collector (IC) leads.',
    'technology-2012-HL-paper-secC-q2d-art':
        'A block diagram: inputs Power (1 = on, 0 = off), Night sensor X (1 = '
        'light, 0 = dark) and Temperature Y (1 = cold, 0 = hot) into a Logic '
        'circuit box, output Heater (1 = on, 0 = off).',
    'technology-2012-HL-paper-secC-q3a-art':
        'Photographs of two tablet computers, one on a stand.',
    'technology-2012-HL-paper-secC-q3b-art':
        'Photograph of the glowing ends of a bundle of optical fibres.',
    'technology-2012-HL-paper-secC-q3c-art':
        'Photograph of a computer motherboard with its slots, sockets and heat sink.',
    'technology-2012-HL-paper-secC-q3d-art':
        'Photograph of a laptop with a padlock and chain on it.',
    'technology-2012-HL-paper-secC-q4a-art':
        'Photograph of crushed and damaged cars piled together after a tsunami.',
    'technology-2012-HL-paper-secC-q4b-art':
        'Photographs of two bearings labelled A and B; below, two graphs, each '
        'headed Design Specifications over Process: 1, a wide flat curve '
        'spreading to the specification lines, and 2, a tall narrow curve well '
        'inside them.',
    'technology-2012-HL-paper-secC-q4d-art':
        'Photographs of three gold medals, one engraved Engrave on the front or '
        'back.',
    'technology-2012-HL-paper-secC-q5b-art':
        'Photographs of three wheelchairs: a manual chair, a powered chair and a '
        'three-wheeled racing chair.',
    'technology-2012-HL-paper-secC-q5c-art':
        'Photograph of a powered wheelchair, the area round its wheel boxed in '
        'red and enlarged, an arrow labelled Casing.',
    'technology-2012-HL-paper-secC-q5d-art':
        'Photograph of three messenger bags made from black inner tube rubber '
        'with coloured edging.',
})

# 2012 Ordinary, each crop rendered and looked at.
REVIEWED.update({
    'technology-2012-OL-paper-secA-q1-art':
        'Photograph of Steve Jobs speaking in front of a large white Apple '
        'logo.',
    'technology-2012-OL-paper-secA-q2-art':
        'Exploded drawing of a smart card, its gold contact chip lifted above '
        'the card.',
    'technology-2012-OL-paper-secA-q3-art':
        'Photograph of a white arched concrete footbridge across a rocky gorge,'
        ' an arrow labelled A pointing at one of its sloping legs.',
    'technology-2012-OL-paper-secA-q4-art':
        'Photograph of a small round sensor with a zig-zag track on its face '
        'and two long wire legs.',
    'technology-2012-OL-paper-secA-q5-art':
        'Photograph of four rechargeable AA batteries.',
    'technology-2012-OL-paper-secA-q6-art':
        'Photograph of a blue pen with a curved, shaped grip.',
    'technology-2012-OL-paper-secA-q7-art':
        '3D drawing of an arrow-shaped hazard warning light, orange on a yellow'
        ' back plate with four screws, an arrow labelled A pointing at its left'
        ' end.',
    'technology-2012-OL-paper-secA-q8-art':
        'Photograph of a hooded figure walking past a burning car.',
    'technology-2012-OL-paper-secA-q9-art':
        'The EPA logo: the letters epa under a swirl of green-blue lines.',
    'technology-2012-OL-paper-secA-q10-art':
        'Photograph of a stone-faced two-storey house with a slate roof.',
    'technology-2012-OL-paper-secA-q11-art':
        'Close-up photograph of brass clockwork gears, an arrow labelled A '
        'pointing at one toothed wheel and the part held against it.',
    'technology-2012-OL-paper-secA-q12-art':
        'Line drawing of a cylindrical electric motor with a short shaft, drawn'
        ' in outline only.',
    'technology-2012-OL-paper-secB-q2a-art':
        '3D drawing of a pencil holder: a bent green plastic part labelled A, '
        'holding a pencil, fixed on a wooden base labelled B.',
    'technology-2012-OL-paper-secB-q2b-art':
        'Drawing of the corner of the wooden base with its top edge rounded, '
        'and a Safety matters warning sign.',
    'technology-2012-OL-paper-secB-q2c-art':
        'A Gantt chart headed Task/Duration: Mark out base, Manufacture base, '
        'Mark out holder, Manufacture holder and Project assembly, each shaded '
        'in later columns.',
    'technology-2012-OL-paper-secB-q2d-art':
        'Screenshot of SolidWorks showing a 3D model of a threaded cylindrical '
        'part.',
    'technology-2012-OL-paper-secB-q3a-art':
        'Rendering of a blue egg timer with a yellow dome and push buttons, an '
        'arrow labelled A pointing at its moulded blue body.',
    'technology-2012-OL-paper-secB-q3b-art':
        'Circuit diagram between +V and -V: potentiometer C, a switch, '
        'capacitor D marked +, a resistor to transistor B, and component A in '
        'series with a resistor.',
    'technology-2012-OL-paper-secB-q3c-art':
        'Simulated printed circuit board for the timer, wired to a PP3 9V '
        'battery and two push switches.',
    'technology-2012-OL-paper-secB-q3d-art':
        'Cause and effect diagram for a Faulty Torch, with the causes Switch?, '
        'Bulb?, People? and Battery?',
    'technology-2012-OL-paper-secC-q1b-art':
        'Photograph of an 18-pin chip; below it, the given flowchart: Start, '
        'then a decision Switch ? with a No exit to the left and a Yes exit '
        'downwards.',
    'technology-2012-OL-paper-secC-q1c-art':
        'Photograph of the Quince robot, a tracked vehicle with an arm, '
        'climbing a kerb.',
    'technology-2012-OL-paper-secC-q1d-art':
        'Three pneumatic circuit symbols labelled A, B and C.',
    'technology-2012-OL-paper-secC-q2a-art':
        'Photograph of an 8-pin 555 IC chip marked NE555N.',
    'technology-2012-OL-paper-secC-q2b-art':
        'Circuit diagram of a 555 IC between +V and 0V: a switch, a resistor, a'
        ' variable resistor and capacitor B on the timing pins, the output '
        'through resistor A to four light-emitting diodes in parallel.',
    'technology-2012-OL-paper-secC-q2c-art':
        'Photograph of cardboard boxes on a roller conveyor.',
    'technology-2012-OL-paper-secC-q3a-art':
        'Drawing of a desktop computer with monitor, tower, keyboard, mouse and'
        ' a disc.',
    'technology-2012-OL-paper-secC-q3b-art':
        'Photograph of a graphics card labelled Memory, Processor Heatsink, '
        'Processor Fan and Motherboard Connection.',
    'technology-2012-OL-paper-secC-q3c-art':
        'A cloud labelled CLOUD above a smartphone, a tablet and a laptop, '
        'wireless signals between them.',
    'technology-2012-OL-paper-secC-q3d-art':
        'Photograph of a meeting room, people round a table with laptops facing'
        ' two screens, one showing a man speaking.',
    'technology-2012-OL-paper-secC-q4a-art':
        'Photographs of a laptop computer and a three-tier wedding cake.',
    'technology-2012-OL-paper-secC-q4b-art':
        'Photograph of a decorated glass Coca-Cola bottle.',
    'technology-2012-OL-paper-secC-q4c-art':
        'Photograph of a heap of discarded computer equipment: monitors, a '
        'keyboard, a tower and cables.',
    'technology-2012-OL-paper-secC-q4d-art':
        'Photograph of a red and black folding hair dryer.',
    'technology-2012-OL-paper-secC-q5a-art':
        'Photographs of a pair of pincers and a metal drinks can.',
    'technology-2012-OL-paper-secC-q5b-art':
        "Photograph of a Boeing 787 Dreamliner flying over Dublin Airport's "
        'Terminal 2.',
    'technology-2012-OL-paper-secC-q5c-art':
        'Exploded drawing of an airliner, sections labelled A to E, and a '
        'table: A Forward fuselage, USA; B Centre fuselage, Italy; C Wing, '
        'Japan; D Wing Tip, South Korea; E Trailing Edge, Australia.',
    'technology-2012-OL-paper-secC-q5d-art':
        'Photograph of aircraft seat backs, an arrow pointing to the moulded '
        'back of a headrest, captioned Back of headrest.',
})

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
    'technology-2019-HL-paper-secC-q3d-art': 'the event logo, which no part asks about; (i) points at the URL box (by-eye rect)',
    'technology-2016-HL-paper-secA-q10-art': "the cropper's whole-band cut; (i) and (ii) each point at their own picture (by-eye rects keyed by roman)",
    'technology-2016-OL-paper-secB-q2a-art': "the cropper's cut of 2(a)'s band; 2(a) points at the dispenser printed at 2(b) (FIGURE_SHARED)",
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
