"""Integrate the validated 2012 Higher Q1-Q10 (and alternative Q10) draft. NOT replay-safe (construction_paper.integrate)."""
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[4] / 'scripts/markbank/authoring'))
import construction_2012_higher as paper  # noqa: E402
import construction_paper as cp  # noqa: E402

ALT = {
    'q1-original': 'Original SEC 2012 Higher Construction Studies Question 1: the printed question with a sketch of the triple-glazed bay window under its lean-to roof.',
    'q2-original': 'Original SEC 2012 Higher Construction Studies Question 2: the printed question with the plan of the bedroom, the 2.3 m × 2.9 m bathroom and the hot press.',
    'q3-original': 'Original SEC 2012 Higher Construction Studies Question 3: the printed question with the elevation and plan of the semi-detached house and storeroom, walls A-A and B-B marked.',
    'q4-original': 'Original SEC 2012 Higher Construction Studies Question 4: the printed question with the layout of an on-site septic tank and percolation area.',
    'q5-original': 'Original SEC 2012 Higher Construction Studies Question 5: the printed question with a sketch of the floor and all the thermal data.',
    'q6-original': 'Original SEC 2012 Higher Construction Studies Question 6: the printed question with the elevation and ground floor plan of the house.',
    'q7-original': 'Original SEC 2012 Higher Construction Studies Question 7: the printed question with an outline drawing of the door, the timber frame wall and the first floor joists.',
    'q8-original': 'Original SEC 2012 Higher Construction Studies Question 8: the printed question on a ring mains circuit, its safety and saving electricity.',
    'q9-original': 'Original SEC 2012 Higher Construction Studies Question 9: the printed question with an outline section of the timber frame house, four locations circled, and a sketch of a service cavity.',
    'q10-original': 'Original SEC 2012 Higher Construction Studies Question 10: the printed question with the plan of the Passive House, the MHRV unit M in the utility room.',
    'q10-alt-original': 'Original SEC 2012 Higher Construction Studies alternative Question 10: the printed quotation from The Green Vitruvius on a sustainable ethos in building, and the task.',
    'q1-section': 'SEC model sections through the bay window and lean-to roof at the abutment with the house wall, with a list of specifications.',
    'q2-requirements': 'SEC 2012 Higher marking scheme notes and sketches on the main entrance and internal corridors for lifetime use.',
    'q2-layout': 'SEC model layouts of the wheelchair-accessible bathroom with a clear turning circle.',
    'q2-locations': 'SEC 2012 Higher marking scheme notes on locating the window, shower, toilet, basin and grab rails.',
    'q3-design': 'SEC 2012 Higher marking scheme notes and sketches on redesigning the layout and glazing and on insulating the external walls (two pages).',
    'q3-reasons': 'SEC 2012 Higher marking scheme notes and sketch on the reasons for the design choices.',
    'q4-scheme': 'SEC 2012 Higher marking scheme notes and sketches on the septic tank, the percolation area and unsuitable sites.',
    'q5-calculation': 'SEC worked solution: the U-value table giving a total resistance of 1.421 and U = 0.704 W/m²K, and the annual heat-loss cost of €183.13.',
    'q5-floor': 'SEC model detail of a Passive standard insulated ground floor with a radon barrier.',
    'q6-features': 'SEC 2012 Higher marking scheme notes and sketches on the features that do more with less for longer (two pages).',
    'q6-importance': 'SEC 2012 Higher marking scheme notes and sketches on orientation, flexibility of design and sourcing materials (two pages).',
    'q7-section': 'SEC model sections through the entrance door head and the timber frame wall carrying the first floor, with a specification list.',
    'q8-wiring': 'SEC ring main diagram with two sockets and the consumer unit, with the cable size and colour coding.',
    'q8-safety': 'SEC 2012 Higher marking scheme notes and sketches on earthing, fuses, MCBs and RCDs.',
    'q8-economy': 'SEC 2012 Higher marking scheme notes on economical use of electricity in lighting, heating and appliances (two pages).',
    'q9-airtightness': 'SEC 2012 Higher marking scheme notes and sketches on design detailing for airtightness.',
    'q9-locations': 'SEC 2012 Higher marking scheme notes and sketches for all four circled locations — the ground floor, the window cill, light fittings and the trapdoor.',
    'q9-service': 'SEC 2012 Higher marking scheme notes on the advantages of a service cavity.',
    'q10-principles': 'SEC 2012 Higher marking scheme notes and sketches for all three items — building form, indoor environment and energy performance, with additional Passive House information (three pages).',
    'q10-mhrv': 'SEC MHRV ducting plan with supply and extract zones, and notes on how the system works and its performance criteria (two pages).',
    'q10-passive': 'SEC 2012 Higher marking scheme notes on the advantages and disadvantages of Passive House construction.',
}
cp.integrate(paper, HERE, ALT)
