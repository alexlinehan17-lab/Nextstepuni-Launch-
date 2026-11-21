"""Integrate the validated 2022 Higher deferred Q1-Q10 (and alternative Q10) draft. NOT replay-safe (construction_paper.integrate)."""
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[4] / 'scripts/markbank/authoring'))
import construction_2022_higher_deferred as paper  # noqa: E402
import construction_paper as cp  # noqa: E402

ALT = {
    "q1-original": "Original SEC 2022 Higher Construction Studies deferred Question 1: the printed question with a sketch of a triple-glazed wooden window in a rendered cavity wall above a suspended timber floor.",
    "q2-original": "Original SEC 2022 Higher Construction Studies deferred Question 2: the printed question with a sketch of four construction workers in hard hats and high-visibility vests reading a drawing.",
    "q3-original": "Original SEC 2022 Higher Construction Studies deferred Question 3: the printed question with the ground-floor plan of a semi-detached house and its rear garden, the proposed study space marked and wall A-A at the front.",
    "q4-original": "Original SEC 2022 Higher Construction Studies deferred Question 4: the printed question with a sketch of a stove standing on a hearth under a mantel shelf.",
    "q5-original": "Original SEC 2022 Higher Construction Studies deferred Question 5: the printed question with a sketch of the tiled solid ground floor layers and all the construction and thermal data.",
    "q6-original": "Original SEC 2022 Higher Construction Studies deferred Question 6: the printed question with the elevation and ground-floor plan of a stone and timber-clad house.",
    "q7-original": "Original SEC 2022 Higher Construction Studies deferred Question 7: the printed question with a sketch of a sheeted wooden door below the tiled eaves of a rendered wall.",
    "q8-original": "Original SEC 2022 Higher Construction Studies deferred Question 8: the printed question with a sketch of a two-storey house with a large glazed ground-floor extension.",
    "q9-original": "Original SEC 2022 Higher Construction Studies deferred Question 9: the printed question with an outline section through a cavity wall, slated truss roof and chimney, three locations circled.",
    "q10-original": "Original SEC 2022 Higher Construction Studies deferred Question 10: the printed question with a sketch of the preliminary design of a Passive House with a deck and rooflights.",
    "q10-alt-original": "Original SEC 2022 Higher Construction Studies deferred alternative Question 10: the printed quotation on embodied energy from The Green Self-Build Book and its two parts.",
    "q1-section": "SEC model vertical section from the strip foundation through the suspended timber floor, cavity wall and window cill, with the detail lists for each area (two pages).",
    "q1-ventilation": "SEC model detail of the suspended floor ventilation, labelled “(b) Ø100 mm vent pipe + gasket (Fall towards outside)”.",
    "q2-procedures": "SEC 2022 Higher deferred marking scheme notes on two safety procedures for each of the use of vehicles, the use of ladders and demolition work, with sketches of warning signs, a ladder at 74° and safe step-ladder use.",
    "q3-design": "SEC model external design and plan for the garden study: south, north, west and east elevations, a covered timber deck linking it to the house, and the furnished plan, with notes (two pages).",
    "q4-system": "SEC model single-line diagram of a stove heating two zones of three radiators each and a cylinder, with header tanks, zone controls and valves, and the typical pipe sizes.",
    "q5-u-value": "SEC worked solution for the U-value of the solid ground floor: the resistance table giving a total resistance of 3.145 and U = 0.318 W/m²°C.",
    "q5-thickness": "SEC worked solution for the additional floor insulation: required resistance 8.333, difference 5.190, giving 0.114 m (114/115 mm).",
    "q5-cost": "SEC worked solution for the annual cost of heat lost through the upgraded floor: 132.3 W, 7,459,200 seconds, 986,852 kJ and 26.422 litres, giving €25.63 by two methods.",
    "q5-scheme": "SEC worked solutions for Question 5: the U-value table (U = 0.318 W/m²°C), the additional insulation (114/115 mm) and the annual heat-loss cost (€25.63) (two pages).",
    "q6-low-impact": "SEC 2022 Higher deferred marking scheme notes on low-environmental-impact features, with sketches of the south elevation, timber cladding and the ground-floor plan.",
    "q7-section": "SEC model vertical section through the door head, cavity wall and tiled eaves of a trussed roof, with the detail lists for the wall, door and eaves (two pages).",
    "q7-thermal-bridge": "SEC model detail of the door head, labelled “(b) Thermally broken door frame and high density insulation used as a cavity closer”.",
    "q8-requirements": "SEC 2022 Higher deferred marking scheme notes on the functional requirements of an external wall, with sketches of wall sections, an airtight membrane and a fire-resistance symbol.",
    "q8-walls": "SEC model external wall sections for nZEB: concrete block cavity, timber frame with a block outer leaf, single-leaf timber frame, externally insulated block and ICF, each with notes (two pages).",
    "q9-locations": "SEC model details for all three circled locations: the lead back gutter and front apron flashing at the chimney, and the stepped DPC at the window head.",
    "q9-materials": "SEC 2022 Higher deferred marking scheme notes on lead, DPC, breather membrane and slate, with sketches of a lead roll, a DPC roll and a slated roof on battens.",
    "q10-items": "SEC 2022 Higher deferred marking scheme notes and sketches for all three Question 10(a) items: building form, continuity of insulation, and windows and glazing (two pages).",
    "q10-orientation": "SEC model sketches of the sun path over the house and its preferred orientation within 30° of south, with notes on thermal performance.",
    "q10-overheating": "SEC 2022 Higher deferred marking scheme reasons for overheating and modifications to prevent it, with sketches of a brise-soleil and an overhang shading the glazing (two pages).",
    "q10-scheme": "SEC marking-scheme notes and sketches for Question 10: building form, continuity of insulation, windows and glazing, orientation and sun path, and overheating (four pages).",
}
# The deferred sitting's anchor (public/paper-anchors/2022/LC029ALP000EV-deferred.pdf.json) is drawn from the paper itself;
# the tracked sidecar in scripts/paper-trail/answers/2022/ is June's.
cp.integrate(paper, HERE, ALT, anchor_from_sidecar=False)
