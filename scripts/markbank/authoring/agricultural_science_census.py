#!/usr/bin/env python3
"""Independent, incrementally reviewed task denominator for Agricultural Science.

Read from the SEC paper/scheme boundary review, not from authored cards. The
generic leaf parser loses Q1 and the two Q3 options in legacy Higher papers;
it also splits pooled marking scales. Every unaudited edition stays OPEN.
This module must not import the authoring modules, reviewed-task output or deck.
"""
import argparse
import hashlib
import itertools
import json
import re
from pathlib import Path
import fitz

ROOT = Path(__file__).resolve().parents[3]
OUTPUT = ROOT / 'scripts/markbank/authored/agricultural-science-census.json'

# ref | marks | paper PDF page | scheme PDF page | distinctive scheme wording
# A marks field describes one practice response, never all choice routes added.
HIGHER_2010 = '''
Q1(a)|10|2|5|It is a species which shows the conditions in the habitat.
Q1(b)|10|2|5|Crown/root/enamel/
Q1(c)|10|2|5|High dry matter /high dmd
Q1(d)(i)|4|2|5|acid-alkali scale
Q1(d)(ii)|6|2|5|sour milk 4-5, rumen 7, abomasum 2
Q1(e)|10|2|5|Refractometer= estimate sugar%
Q1(f)|10|2|5|Asteraceae/Compositae
Q1(g)|10|2|5|114 DAYS
Q1(h)|10|2|5|Food store
Q1(i)|10|2|5|Not as high in N as urea or CAN
Q1(j)|10|2|5|leaves have holes
Q2(a)|16|2|6|Activity of soil animals
Q2(b)|16|2|6|Blanket =caused by high local rainfall
Q2(c)|16|2|6|Loss in wt divided by wt of sample
Q3 Option One (a)(i)|4|3|7|because it’s a good dairy
Q3 Option One (a)(ii)|4|3|7|beef calves for sale
Q3 Option One (a)(iii)|4|3|7|easy calving
Q3 Option One (a)(iv)|4|3|7|15-20%
Q3 Option One (b)|16|3|7|MILK LET-DOWN
Q3 Option One (c)|16|3|7|WITHDRAWAL
Q3 Option Two (a)(i)|4|3|8|Lime(stone)
Q3 Option Two (a)(ii)|8|3|8|Weathering of limestone
Q3 Option Two (b) — parasitic disease|6|3|8|parasitic means caused by a parasite
Q3 Option Two (b) — deficiency disease|6|3|8|deficiency disease caused by a lack
Q3 Option Two (b)|12|3|8|Grass-Tetany
Q3 Option Two (c)|12|3|8|not certified seed
Q4(a)|24|3|9|SOIL TEXTURE
Q4(b)|24|3|9|EARTHWORMS
Q4(c)|24|3|9|TRANSPIRATION RATE
Q4(d)|24|3|9|BARLEY DIGESTIBILITY
Q5(a)(i)|8|4|9|RADDLING HARNESS
Q5(a)(ii)|8|4|9|FOOTROT
Q5(b)(i)|16|4|9|RESEEDING WHY?
Q5(b)(ii)|8|4|9|perennial ryegrass
Q5(c)|8|4|9|LEAF:STEM
Q6(a)|12|4|10|BLIGHT
Q6(b)|12|4|10|SCUTCH
Q6(c)(i)|6|4|10|PLOUGH PAN
Q6(c)(ii)|6|4|10|First point compulsory in (ii)
Q6(d)|12|4|10|1000 grain weight
Q7(a)|12|4|11|ANY THREE
Q7(b)(i)|4|4|11|Parents phenotypes
Q7(b)(ii)|9|4|11|Punnett square:
Q7(b)(iii)|3|4|11|Test cross or back cross
Q7(c)(i)|6|4|11|occurs when cell division goes wrong
Q7(c)(ii)|6|4|11|Name of ploidy
Q7(d)|8|4|11|CALVING DIFFICULTY INDEX
Q8(a)|24|5|12|At least one point from either
Q8(b)|24|5|12|Photosynthesis:
Q8(c)|24|5|12|Two points from each alternative
Q9(a)|12|5|13|At least one reference each to fasting and hanging
Q9(b)|12|5|13|oxygen is more soluble in cold
Q9(c)|12|5|13|highest yielding breed
Q9(d)|12|5|13|protein rich
Q9(e)|12|5|13|conifers do well
'''

ORDINARY_2010 = '''
Q1(a)|4|2|5|A: Air
Q1(b)|12|2|5|Accept “sand” alone for 3 marks
Q1(c)|4|2|5|Earthworm, fungus, bacteria
Q2 — activity 2|4|3|5|2. Harvesting barley
Q2 — activity 3|4|3|5|3. Making hay
Q2 — activity 4|4|3|5|4. Harvesting potatoes
Q2 — activity 5|4|3|5|5. Sowing seed
Q2 — activity 6|4|3|5|6. Breaking up compacted soil
Q3(a)|2|3|5|Accept “Simmental”.
Q3(b)|6|3|5|Wedge(triangular) shaped
Q3(c) — lactation|3|3|5|Lactation – production of milk
Q3(c) — colostrum|3|3|5|Colostrum – first milk
Q3(d)|6|3|5|305 days
Q4 — Mastitis|4|4|6|Mastitis
Q4 — Swine fever|4|4|6|Swine fever
Q4 — Brucellosis|4|4|6|Brucellosis
Q4 — Liverfluke|4|4|6|Liverfluke
Q4 — Tuberculosis (TB)|4|4|6|Tuberculosis (TB)
Q5|20|4|6|6(3) + 2
Q6(a)|12|5|6|A: Cell Wall B: Vacuole
Q6(b)|4|5|6|Chlorophyll
Q6(c)|4|5|6|Photosynthesis or to make food
Q7|20|5|6|The first five correct answers 5(1); the next five correct answers 5(3)
Q8(a)(i)|6|6|7|A: Strip Grazing / B: Paddock Grazing
Q8(a)(ii) — strip|6|6|7|Strip Grazing: Land divided into strips
Q8(a)(ii) — paddock|6|6|7|Paddock Grazing: Land divided into paddocks
Q8(a)(iii) — strip advantage|3|6|7|Fresh grass always available
Q8(a)(iii) — strip disadvantage|3|6|7|High labour or hard to contain stock
Q8(a)(iii) — paddock advantage|3|6|7|Fresh grass every day
Q8(a)(iii) — paddock disadvantage|3|6|7|Expensive or need to create roads
Q8(a)(iv)|3|6|7|Set stocking or block grazing
Q8(b)(i)|6|6|7|Perennial ryegrass (PRG)
Q8(b)(ii)|6|6|7|PRG – good productivity
Q8(c)|9|6|8|Description: Three points.
Q8(d) — tillering|3|6|8|Tillering – the growth of side shoots
Q8(d) — topping|3|6|8|Topping – cutting the grass
Q9(a)|4|7|9|Liming
Q9(b)|6|7|9|Any two correct elements
Q9(c)|2|7|9|Crop named
Q9(d)|4|7|9|Correct Fertilizer
Q9(e)(i)|6|7|9|Preparation of seedbed
Q9(e)(ii)|2|7|9|Spring sowing
Q9(e)(iii)|6|7|9|Blight/potato cyst nematode
Q9(e)(iv)|4|7|9|Spray (fungicide)
Q9(e)(v)|2|7|9|First earlies: May-June
Q9(e)(vi)|6|7|9|First and second earlies - 7-10 tonnes/Ha.
Q9(f)|18|7|9|Any four relevant points
Q10(a)(i)|9|8|10|A: (Right) atrium
Q10(a)(ii)|9|8|10|White blood cells/Red blood cells
Q10(a)(iii)|9|8|10|Fight infection
Q10(a)(iv)|3|8|10|Iron deficiency
Q10(a)(v)|3|8|10|Iron injection
Q10(b)(i)|9|8|10|A: Ovary/B: Vagina
Q10(b)(ii)|3|8|10|Stock ewes on poor quality pasture
Q10(b)(iii)|9|8|10|More eggs released
Q10(b)(iv)|3|8|10|Artificial insemination
Q10(b)(v)|3|8|10|Better choice of sire
Q11(a)(i)|4|9|11|Shape of an animal
Q11(a)(ii)|8|9|11|Beef animals have muscular shoulders
Q11(a)(iii)|4|9|11|2 - 2 ½ years
Q11(a)(iv)|4|9|11|After this age fat is put on
Q11(b)(i)|8|9|11|Texel/Wicklow
Q11(b)(ii)|4|9|11|3-6 kg
Q11(b)(iii) — feeding|4|9|11|Feeding: Colostrum
Q11(b)(iii) — management|8|9|11|Management: Any two
Q11(c)(i)|4|9|11|Only young animal has access to food
Q11(c)(ii)|12|9|11|Supplements milk from mother
Q12(a)(i)|8|9|12|Any two weeds
Q12(a)(ii)|4|9|12|One piece of equipment
Q12(a)(iii)|18|9|12|Any three points:
Q12(b)(i)|4|9|12|20oC
Q12(b)(ii)|8|9|12|To prevent sow from crushing her bonhams
Q12(b)(iii)|4|9|12|Dry sow house
Q12(b)(iv)|14|9|12|Any three criteria
Q12(c)(i)|14|9|12|Any three advantages
Q12(c)(ii)|10|9|12|Any two ways
Q12(c)(iii)|6|9|12|Organic farming:
Q12(d)(i) — germination|4|9|12|Germination: Seed begins to grow
Q12(d)(i) — establishment|6|9|12|Establishment: new plant puts down roots
Q12(d)(ii)|18|9|12|one tube has all three suitable conditions
Q13(a)|18|10|13|1. dominant
Q13(b)(i)|12|10|13|Gametes E x e
Q13(b)(ii)|21|11|13|Genotype of second parent Ee
Q13(c)(i)|3|11|13|Meiosis
Q13(c)(ii)|6|11|13|L: Spindle (fibre)
'''

HIGHER_2011 = '''
Q1(a)|10|2|5|Rosaceae-large flowers
Q1(b)(i)|4|2|5|Condition scoring
Q1(b)(ii)|6|2|5|Calving 2.5-3.5, service 2-3
Q1(c)|10|2|5|Active = body manufactures antibodies
Q1(d)|10|2|5|Earthworms; adding lime
Q1(e)|10|2|5|Germination; use certified seed
Q1(f)|10|2|5|Mono: glucose
Q1(g)(i)|4|2|5|Platys: liverfluke/tapeworm
Q1(g)(ii)|6|2|5|Platy: liver damage/not thriving
Q1(h)(i)|4|2|5|Symbiosis; accept biology def
Q1(h)(ii)|6|2|5|Examples; Rhizobium
Q1(i)|10|2|5|Add acid to sample
Q1(j)|10|2|5|Stolon; above ground horizontal stem
Q2(a)(i)|4|2|6|Name: plough/iron/compaction
Q2(a)(ii)|4|2|6|Formed; continuous tillage
Q2(a)(iii)|4|2|6|Problem: hard/impervious layer
Q2(a)(iv)|4|2|6|Removal: deep ploughing
Q2(b)(i)|8|2|6|Gleisation: high rainfall
Q2(b)(ii)|8|2|6|Check field colour differences
Q2(c)|16|2|6|Place a sample of soil in flask
Q3 Option One (a)|16|3|7|Summer grazing; involves
Q3 Option One (b)|16|3|7|Replacement heifers;
Q3 Option One (c)(i)|8|3|7|FCE; how efficiently
Q3 Option One (c)(ii)|4|3|7|Body tissues develop in order
Q3 Option One (c)(iii)|4|3|7|Improve FCE;
Q3 Option Two (a)|16|3|7|Grassland management;
Q3 Option Two (b)(i)|2|3|7|Colostrum; /intestine changes
Q3 Option Two (b)(ii)|14|3|7|Nutritious/laxative/good start in life/
Q3 Option Two (c)(i)|4|3|7|Strip grazing;a moveable electric fence
Q3 Option Two (c)(ii) — advantages|6|3|7|Adv; cheap/get fresh material
Q3 Option Two (c)(ii) — disadvantages|6|3|7|Disadv; damage to soil structure
Q4(a)|24|3|8|Take 2 or more different varieties
Q4(b)|24|3|8|Place in sterile test tubes
Q4(c)|24|3|8|Get 2 suitable vessels
Q4(d)|24|3|8|Block off area
Q5(a)(i)|4|4|8|Anaemia
Q5(a)(ii)|4|4|8|Haemoglobin molecule
Q5(a)(iii)|4|4|8|Balanced diet (containing iron)
Q5(b)(i)|16|4|8|A= septum, B= right ventricle
Q5(b)(ii)|8|4|8|X= body(or named part), Y=lungs
Q5(b)(iii)|8|4|8|Blood in X= oxyhaemoglobin
Q5(c)|4|4|8|Haemoglobin in urine
Q6(a)|16|4|9|Crop is bleached
Q6(b)(i)|6|4|9|Soil type:malting
Q6(b)(ii)|6|4|9|Rotation: malting needs low N
Q6(b)(iii)|6|4|9|Fertiliser: Malting needs low N
Q6(b)(iv)|6|4|9|End use: Malting for brewing
Q6(c)|8|4|9|Diagram = 4,2,0 plus 4x1 labels
Q7(a)(i)|4|5|10|Interphase: before prophase
Q7(a)(ii)|4|5|10|Haploid; condition
Q7(a)(iii)|4|5|10|Inbreeding: allowing related
Q7(b) — cross|12|5|10|4 gametes each side
Q7(b)(i)|4|5|10|Hairy = 12/16
Q7(b)(ii)|4|5|10|Short = 4/16
Q7(b)(iii)|4|5|10|Hairy and short = 3/16
Q7(c)|12|5|10|RR = red WW(rr) = white RW(Rr) = roan
Q8(a)|24|5|11|One week before farrowing date
Q8(b)(i)|4|5|11|BOD: Biological
Q8(b)(ii)|4|5|11|Milk/slurry(FYM)/silage effluent
Q8(b)(iii)|8|5|11|Bacteria use up oxygen
Q8(b)(iv)|8|5|11|Strategies; ensure dairy waste
Q8(c)|24|5|11|Non essential; can be made
Q9(a)|12|5|12|Equation may cover all points
Q9(b)|12|5|12|Calves or offspring are tested
Q9(c)|12|5|12|Systemic; chemicals are absorbed
Q9(d)|12|5|12|Caused by wrong soil type
Q9(e)|12|5|12|To attract bonhams away from sow
'''

ORDINARY_2011 = '''
Q1|20|2|5|2(7m) + 1(2m) + 4(1m)
Q2|20|3|5|2(7m) + 2(2m) + 2(1m)
Q3|20|3|5|2(7m) + 3(2m)
Q4|20|4|6|2(6m) + 2(2m) + 4(1m)
Q5 — bullock|4|4|6|A male calf that has been castrated
Q5 — gilt|4|4|6|A female pig that has not had a litter
Q5 — draft ewe|4|4|6|A ewe that is culled from the flock and sold
Q5 — broiler|4|4|6|A chicken that is reared for slaughter
Q5 — suckler calf|4|4|6|A calf (in the beef herd) that sucks milk from its mother
Q6(a)|5|5|7|Crop Rotation:
Q6(b)|5|5|7|Sowing certified seed:
Q6(c)|5|5|7|Applying selective herbicide:
Q6(d)|5|5|7|Planting winter varieties of cereals:
Q7(a)|8|5|7|TB/ pneumonia/ mastitis
Q7(b)|8|5|7|Silage production/ production of dairy products
Q7(c)|4|5|7|Fungus/Phytophthora infestans
Q8(a)(i)|6|6|8|Tail docking : removal of tails
Q8(a)(ii)|6|6|8|Shearing : Removal of fleece
Q8(a)(iii)|6|6|8|Raddling a ram:
Q8(a)(iv)|6|6|8|Dipping sheep:
Q8(a)(v)|6|6|8|Walking the flock through a footbath:
Q8(b)(i)|6|6|8|Isolation pen:
Q8(b)(ii)|6|6|8|Infrared lamp:
Q8(b)(iii)|6|6|8|Creep feeder:
Q8(b)(iv)|6|6|8|Crush:
Q8(b)(v)|6|6|8|Farrowing crate:
Q9(a)(i)|10|6|9|Nitrogen fixation/ rich in protein
Q9(a)(ii)|10|6|9|More palatable/higher yield
Q9(b) — ley|5|6|9|Ley: Grassland sown by farmer
Q9(b) — establishment|5|6|9|Establishment: Becoming a totally independent plant
Q9(b) — heading out|5|6|9|Heading out: Stage when grass flowers
Q9(c)(i)|5|6|9|Undersowing
Q9(c)(ii)|5|6|9|Direct drilling/ stitching- in
Q9(d)(i)|5|6|9|DMD : The proportion
Q9(d)(ii)|5|6|9|70% - 80%
Q9(d)(iii)|5|6|9|Less productivity or low yield
Q10(a)|24|7|10|1: rainfall
Q10(b)(i)|5|7|10|Igneous Granite or Basalt
Q10(b)(ii)|5|7|10|Sedimentary Limestone or Sandstone
Q10(b)(iii)|5|7|10|Metamorphic Marble or
Q10(c)|9|7|10|Weathering: Frost action
Q10(d) — soil A|4|7|10|Soil A : Clay
Q10(d) — soil B|4|7|10|Soil B : Loam
Q10(d) — soil C|4|7|10|Soil C : Sandy Loam
Q11(a)(i)|6|8|11|An organism that lives in or on
Q11(a)(ii)|3|8|11|Example of parasite:
Q11(a)(iii)|3|8|11|Method of removal
Q11(b)|12|8|11|Life cycle of insect
Q11(c)(i)|8|8|11|(Sandy) loam soil
Q11(c)(ii) — date|4|8|11|Sowing date : September - November
Q11(c)(ii) — method|4|8|11|Method : sown with a combine drill
Q11(c)(iii)|4|8|11|10 : 10 : 20/ N,P, K
Q11(c)(iv)|4|8|11|Certified seed/ seed treatment
Q11(c)(v) — method|4|8|12|Method : Combine harvester
Q11(c)(v) — time|4|8|12|Time : Winter barley
Q11(c)(vi)|4|8|12|Yield : Winter barley
Q12(a) — digestive system|15|8|13|Name of monogastric animal
Q12(a) — enzyme experiment|15|8|13|Named enzyme / matching substrate
Q12(b)(i)|6|8|13|Waterlogging /gas exchange
Q12(b)(ii)|6|8|13|Rich in antibodies
Q12(b)(iii)|6|8|13|Habitat for wildlife
Q12(b)(iv)|6|8|13|Optimum conditions for storage
Q12(b)(v)|6|8|13|Poorest trees removed
Q12(c)(i)|9|8|13|Water 87.5%
Q12(c)(ii)|12|8|13|Named component:
Q12(c)(iii)|9|8|13|Wash udders and teats
Q12(d)(i)|12|8|13|Named producer /named primary consumer
Q12(d)(ii)|15|8|13|Quadrat/ throw at random
Q12(d)(iii)|3|8|13|The variety of organisms found in a habitat
Q13(a)(i)|3|9|14|Alleles -
Q13(a)(ii)|3|9|14|Clone -
Q13(a)(iii)|3|9|14|Hybrid Vigour –
Q13(b) — F1|8|9|14|4* x 2m
Q13(b) — F2|22|9|14|11* x 2m
Q13(c)(i)|2|9|14|9* x 1m
Q13(c)(ii)|3|9|14|9* x 1m
Q13(c)(iii)|4|9|14|9* x 1m
Q13(d)(i)|3|9|14|(i) B (3m)
Q13(d)(ii)|3|9|14|(ii) B (3m)
Q13(d)(iii)|3|9|14|Haploid –
Q13(d)(iv)|3|9|14|Ovary /testis/sex organs/gonads
'''

# Irish boundaries independently transcribed from the visually reviewed Irish
# source; canonical English addresses join the same practice identities.
ORDINARY_2011_IRISH = '''
Q1|20|2|5|2(7m) + 1(2m) + 4(1m)
Q2|20|3|5|2(7m) + 2(2m) + 2(1m)
Q3|20|3|6|2(7m) + 3(2m)
Q4|20|4|6|2(6m) + 2(2m) + 4(1m)
Q5 — bullock|4|4|7|Lao fireann atá coillte
Q5 — gilt|4|4|7|Muc bhaineann nach raibh ál aici
Q5 — draft ewe|4|4|7|Caora a dhealaítear ón tréad agus a dhíoltar
Q5 — broiler|4|4|7|Sicín a thógtar le haghaidh marú
Q5 — suckler calf|4|4|7|Lao (i mbólacht na mairteola)
Q6(a)|5|5|7|Uainíocht na mbarr:
Q6(b)|5|5|7|Síol deimhnithe a chur:
Q6(c)|5|5|7|Luibhicíd roghnaíoch a leathadh:
Q6(d)|5|5|7|Cineálacha geimhridh de ghránaigh a phlandú:
Q7(a)|8|5|7|Eitinn/niúmóine/maistíteas
Q7(b)|8|5|7|Táirgeadh sadhlais/táirgeadh táirgí déiríochta
Q7(c)|4|5|7|Fungas/Phytophthora infestans
Q8(a)(i)|6|6|8|Sciotadh eireaball :
Q8(a)(ii)|6|6|8|Bearradh :
Q8(a)(iii)|6|6|8|Breasal a chur ar reithe:
Q8(a)(iv)|6|6|8|Tumadh caorach:
Q8(a)(v)|6|6|8|An tréada a chur ag siúl trí fholcadán crúb:
Q8(b)(i)|6|6|8|Pionna aonraithe:
Q8(b)(ii)|6|6|8|Lampa infridhearg:
Q8(b)(iii)|6|6|8|Beathaitheoir bacphoill:
Q8(b)(iv)|6|6|8|Gabhlach:
Q8(b)(v)|6|6|8|Cliathbhosca breithe:
Q9(a)(i)|10|6|9|Fosú nítrigine/saibhir i bpróitéin
Q9(a)(ii)|10|6|9|Níos blasta/táirgeadh níos airde
Q9(b) — ley|5|6|9|Bán: Talamh féaraigh curtha ag feirmeoir
Q9(b) — establishment|5|6|9|Bunú: Ag éirí ina phlanda
Q9(b) — heading out|5|6|9|Ag teacht i gcraobh (i ndias):
Q9(c)(i)|5|6|9|Fo-chur
Q9(c)(ii)|5|6|9|Druileáil dhíreach/fuáil isteach
Q9(d)(i)|5|6|9|DMD: Comhréir
Q9(d)(ii)|5|6|9|70%-80%
Q9(d)(iii)|5|6|9|Táirgiúlacht níos ísle nó táirgeadh íseal
Q10(a)|24|7|10|1: báisteach
Q10(b)(i)|5|7|10|Bruthach Eibhear nó Basalt
Q10(b)(ii)|5|7|10|Dríodrach Aolchloch nó
Q10(b)(iii)|5|7|10|Meiteamorfach Marmar nó
Q10(c)|9|7|10|Síonchaitheamh: Gníomh seaca
Q10(d) — soil A|4|7|10|Ithir A : Cré
Q10(d) — soil B|4|7|10|Ithir B : Dúrabhán
Q10(d) — soil C|4|7|10|Ithir C : Dúrabhán gainmheach
Q11(a)(i)|6|8|11|Orgánach atá á chothú
Q11(a)(ii)|3|8|11|Eiseamláir seadáin (paraisíte)
Q11(a)(iii)|3|8|11|Modh bainte
Q11(b)|12|8|11|Saolré feithide
Q11(c)(i)|8|8|11|Ithir dhúrabháin (ghainmheach)
Q11(c)(ii) — date|4|8|11|Dáta síolchuir : Meán Fómhair-Samhain
Q11(c)(ii) — method|4|8|11|Modh : curtha le comhdhruilire
Q11(c)(iii)|4|8|11|10 : 10 : 20/N,P, K
Q11(c)(iv)|4|8|11|Síol deimhnithe/cóireáil síl
Q11(c)(v) — method|4|8|11|Modh : Comhbhuainteoir
Q11(c)(v) — time|4|8|11|Am : Eorna gheimhridh
Q11(c)(vi)|4|8|11|Táirgeadh : Eorna gheimhridh
Q12(a) — digestive system|15|8|13|Ainm ainmhí mhonagastraigh
Q12(a) — enzyme experiment|15|8|13|Einsím ainmnithe/substráit chomhfhreagrach
Q12(b)(i)|6|8|13|Leathbhá/malartú gáis
Q12(b)(ii)|6|8|13|Saibhir in antasubstaintí
Q12(b)(iii)|6|8|13|Gnáthóg le haghaidh fiadhúlra
Q12(b)(iv)|6|8|13|Dálaí barrmhaitheasa le haghaidh stórála
Q12(b)(v)|6|8|13|Baintear na crainn is measa
Q12(c)(i)|9|8|13|Uisce 87.5%
Q12(c)(ii)|12|8|13|Comhpháirt ainmnithe
Q12(c)(iii)|9|8|13|Nigh úthanna agus siní
Q12(d)(i)|12|8|13|Táirgeoir ainmnithe/tomhaltóir tosaigh ainmnithe
Q12(d)(ii)|15|8|13|Cuadraí/caith go randamach
Q12(d)(iii)|3|8|13|Bithéagsúlacht: Éagsúlacht na n-orgánach
Q13(a)(i)|3|9|14|Ailléilí –
Q13(a)(ii)|3|9|14|Clón –
Q13(a)(iii)|3|9|14|Fuinneamh Hibrideach –
Q13(b) — F1|8|9|14|4* x 2m
Q13(b) — F2|22|9|14|11* x 2m
Q13(c)(i)|2|9|14|Géinitíopaí na dtuismitheoirí ss* X Ss*
Q13(c)(ii)|3|9|14|Géinitíopaí na ngaiméití s* S* s*
Q13(c)(iii)|4|9|14|Géinitíopaí an tsleachta Ss* ss*
Q13(d)(i)|3|9|14|(i) B (3m)
Q13(d)(ii)|3|9|14|(ii) B (3m)
Q13(d)(iii)|3|9|14|Haplóideach –
Q13(d)(iv)|3|9|14|Ubhagán/uirí/gnéasorgáin/gónaid
'''

HIGHER_2012 = '''
Q1(a)(i)|4|2|5|Grass/ barley/ correct example
Q1(a)(ii)|6|2|5|Monocot: one cotyledon
Q1(b)|10|2|5|Mammalia: Body covered
Q1(c)(i)|4|2|5|Wind/ animals/ water/ self/ farming activity
Q1(c)(ii)|6|2|5|Wind: Dandelion/ thistle
Q1(d)|10|2|5|4 x 2 + 2 x 1
Q1(e)|10|2|5|To develop rumen/ scratch factor
Q1(f)|10|2|5|Tramlines: Parallel unsown tracks
Q1(g)|10|2|5|Limestone: Alkaline
Q1(h)|10|2|5|Meiosis (reduction division)
Q1(i)|10|2|5|Xylem: Transports water
Q1(j)(i)|6|2|5|Average litter size: 11.5
Q1(j)(ii)|4|2|5|Dose/ vaccinate/ inject with iron
Q2(a)(i)|6|2|6|Deep soil/ naturally fertile
Q2(a)(ii)|10|2|6|Diagram: Deep A horizon
Q2(b)|8|2|6|Name: Sandy/ clay/ loam
Q2(c)|24|2|6|Two flasks/ two (suitable) plants
Q3 Option One (a)|11|3|7|Composition: Water 87.8%
Q3 Option One (b)(i)|8|3|7|Health (disease)/ age
Q3 Option One (b)(ii)|8|3|7|Health: mastitis reduces fat and protein
Q3 Option One (c)(i)|6|3|7|Antibiotics/ bacteria/ somatic cells
Q3 Option One (c)(ii)|15|3|7|Two sterile test tubes
Q3 Option Two (a)|12|3|8|Used to find if ewe is pregnant
Q3 Option Two (b)(i)|8|3|8|Terminal Sire: Ram used
Q3 Option Two (b)(ii)|4|3|8|Suffolk/ Texel/ Charollais/ Belclare
Q3 Option Two (b)(iii)|8|3|8|Suffolk: Good carcass quality
Q3 Option Two (c)|16|3|8|Flushing: Ewes placed in low plane
Q4(a)|24|3|9|(Leaf to stem ratio)
Q4(b)|24|3|9|Get a clean glass slide
Q4(c)|24|3|9|Get two potted plants
Q4(d)|24|3|9|Sample of sieved soil
Q5(a)|16|4|10|Barley: grows well in Irish climate
Q5(b)(i)|4|4|10|Speeds up growth
Q5(b)(ii)|4|4|10|Makes harvesting easier
Q5(b)(iii)|4|4|10|Prevents ‘greening’ of tubers
Q5(b)(iv)|4|4|10|Free of disease/ better yield
Q5(c)|16|4|10|Overheating/ sprouting/ rotting
Q6(a)(i)|10|4|11|Labelled axes
Q6(a)(ii)|6|4|11|First winter housing: 200 kg
Q6(a)(iii)|4|4|11|1st winter:
Q6(b)|16|4|11|Hygiene in housing
Q6(c)|12|4|11|Oxytocin/ pituitary gland
Q7(a)|12|4|12|Where a gene (for a non-reproductive trait)
Q7(b)(i)|6|4|12|BB x EE = BE
Q7(b)(ii)|10|4|12|Parents BE x BE
Q7(c)|12|4|12|Stem tubers/ for food storage
Q7(d)|8|4|12|Males are aggressive
Q8(a)|24|5|13|Nitrogen gas/ nitrogen fixation
Q8(b)(i)|12|5|13|Good dry matter source
Q8(b)(ii)|12|5|13|Close off field 6 weeks before cutting
Q8(c)|24|5|13|LUNGWORM Nematode
Q9(a)|12|5|14|Necessary for (sexual) reproduction
Q9(b)|12|5|14|Colder outdoors/ wetter
Q9(c)|12|5|14|Seeding rate is too low
Q9(d)|12|5|14|Protection for animals
Q9(e)|12|5|14|Presence of boar stimulates
'''

# 2026 Higher: Section A Q1-Q12 at 10 marks, Section B Q13-Q18 at 50. Scheme
# pages 1-11 are instructions and the coursework criteria, not paper tasks.
HIGHER_2026 = '''
Q1(a)|8|3|12|Reduced Soil Compaction or weight
Q1(b)|2|3|12|High maintenance or costs or emissions
Q2(a)(i)|8|4|12|Contain chlorophyll which is used to
Q2(a)(ii)|2|4|12|Carbon Sequestration
Q2(b)|10|5|13|Sow crops in rows / correct spacing
Q3(a)(i)|2|6|13|The ability of an organism to remain unaffected
Q3(a)(ii)|2|6|13|High seed production / herbicide resistance
Q3(a)(iii)|6|6|13|crop rotation involving sowing a variety of crops
Q3(b)(i)|4|7|14|there are few patches of wild oats present
Q3(b)(ii)|6|7|14|hand rogueing / mechanical control
Q4(a)|2|8|14|Metabolic disorder caused by low blood calcium
Q4(b)|2|8|14|Staggering - cow has difficulty walking
Q4(c)|6|8|14|Boosts immunity or reduces retained
Q5(a)|4|9|15|Sole ulcers pressure on sole of foot
Q5(b)|3|9|15|Regular hoof trimming / foot baths
Q5(c)|3|9|15|Decreased production (reduced milk yield
Q6(a)(i)|2|10|15|Quantitative measure of how many worm eggs
Q6(a)(ii)|4|10|15|Identify if the parasite is an
Q6(a)(iii)|4|10|15|Rotational Grazing - prevents lambs grazing
Q6(b)(i)|4|11|16|The incidence of barber pole in increasing rapidly
Q6(b)(ii)|2|11|16|As Ireland’s climate is getting milder
Q6(b)(iii)|4|11|16|Weigh animals to ensure accurate weight
Q7|10|12|16|Healthy soil biome prevents nitrate leaching
Q8(a)|5|13|17|A – Limousin
Q8(b)|5|13|17|Lively / excitable
Q9(a)|3|14|17|Used equal amounts of samples
Q9(b)|3|14|17|Water drains fastest in the sand
Q9(c)|4|14|17|Soil type = loam
Q10(a)|5|15|17|A – Ragwort
Q10(b)|5|15|17|seeds can remain viable in soil for many years
Q11(a)(i)|6|16|18|Comfortable lying areas prevent
Q11(a)(ii)|4|16|19|Overcrowding causes competition for feed
Q11(b)(i)|4|17|19|4 x 40 = 160
Q11(b)(ii)|3|17|19|Bulls would have to be split between the two pens
Q11(b)(iii)|3|17|20|slats are not designed to support heavier animals
Q12(a)|6|18|20|Prolificacy (large litter size)
Q12(b)|2|18|20|Increased litter size / fast growth rate
Q12(c)|2|18|20|Greater risk of Inbreeding
Q13(a)(i)|6|21|21|Blueprint for managing nutrient inputs
Q13(a)(ii)|2|21|21|Essential for root development / low P
Q13(b)(i)|4|21|21|Process by which fine soil particles
Q13(b)(ii)|2|22|21|Maintaining a suitable soil pH (pH 6-8)
Q13(b)(iii)|16|22|21|stopper and shake
Q13(c)(i)|12|23|22|Field B has good fertility due to Optimum pH
Q13(c)(ii)|8|23|22|(corrective action) Addition of Lime
Q14(a)(i)|5|24|23|Clover fixes atmospheric nitrogen
Q14(a)(ii)|1|24|23|If soil is too acidic
Q14(a)(iii)|12|24|23|Identify hazards and risks and remove them
Q14(b)(i)|5|25|23|Improves the nutritional value of the diet
Q14(b)(ii)|5|25|23|Risk: Bloat
Q14(b)(iii)|8|25|23|Maintain correct soil pH (around 6.3
Q14(b)(iv)|2|25|24|Identify the average recommended clover
Q14(c)(i)|9|26|24|Direct Drilling/stitching in/slit sowing
Q14(c)(ii)|3|26|24|Identify the ideal post-grazing height
Q14(d)|12|27|24|remove nodules with scalpel or crush root nodules
Q15(a)(i)|5|28|25|36 days
Q15(a)(ii)|5|28|25|3 or 3.2
Q15(a)(iii)|5|28|25|AI accuracy is 36.2 days
Q15(a)(iv)|5|28|25|freemartin
Q15(a)(v)|2|29|25|Knowing the expected calving date
Q15(b)(i)|10|29|25|Draw a labelled diagram of the cow’s reproductive system
Q15(b)(ii)|11|30|25|Y = 275 days
Q15(b)(iii)|2|30|26|1st to 3rd Dec
Q15(b)(iv)|5|30|26|if missed has to wait 21 days
Q16(a)(i)|10|31|26|The radicle and plumule emerge
Q16(a)(ii)|9|31|26|A – Plantain
Q16(a)(iii)|2|32|26|drought tolerance or increased nutrient
Q16(a)(iv)|3|32|26|Identify if a multi-species sward is a monoculture
Q16(a)(v)|6|32|27|Yield reduction - grazing too tightly
Q16(b)(i)|3|33|27|The better the soil fertility
Q16(b)(ii)|8|33|27|If the target yield is 5 tonnes
Q16(b)(iii)|3|33|27|Good quality soil can produce 5 ton DM
Q16(c)|6|33|27|Roll continuously during filling
Q16(d)|6|33|28|Flexibility and scalability
Q17(a)(i)|5|34|28|40 – 50kg
Q17(a)(ii)|6|34|28|200 / 205 = 0.975
Q17(a)(iii)|2|34|28|Maintenance diet in 1st winter
Q17(a)(iv)|11|35|28|correct data plotted (5 plotted points)
Q17(a)(v)|6|36|28|Cattle that fail to reach target daily live-weight gain
Q17(b)(i)|6|36|29|Ireland has a mild, temperate climate
Q17(b)(ii)|8|37|29|In relation to grass-fed beef identify if
Q17(b)(iii)|6|37|29|Food safety - tracked from farm to fork
Q18(a)|4|38|29|Comparison of the performance of an organism’s
Q18(b)(i)|7|38|29|average milk yield or milk solids of the
Q18(b)(ii)|7|38|29|provides farmers with reliable
Q18(b)(iii)|7|39|30|milk yield / fertility / calving difficulty
Q18(c)(i)|5|39|30|Wheat A
Q18(c)(ii)|8|39|30|Matures (9 days) earlier than Wheat B
Q18(c)(iii)|3|39|30|Native cattle or sheep breeds cope better
Q18(d)(i)|2|40|30|Genetic make-up of an organism determined
Q18(d)(ii)|7|40|30|Ensuring low SCC reduces the incidence of mastitis
'''

# Printed finite pools, transcribed from the paper in printed order. A route is
# one complete response, carrying the marks for that response only.
POOLS_2026_HIGHER = {
    'Q2(b)': (3, ['Fertilising the crop', 'Optimising light capture', 'Genetic improvement of crops', 'Grassland management']),
    'Q7': (4, ['Protection from pests and diseases', 'Carbon storage', 'Reduced environmental losses', 'Improve plant resilience', 'Food quality', 'Nutrient provision']),
    'Q10(a)': (2, ['A', 'B', 'C']),
    'Q14(c)(i)': (1, ['A', 'B']),
    'Q18(c)(iii)': (1, ['plants', 'animals']),
}

# 2026 Ordinary: Section A Q1-Q12 at 10 marks, Section B Q13-Q18 at 50. Scheme
# pages 1-11 are instructions and the coursework criteria, not paper tasks.
ORDINARY_2026 = '''
Q1(a)|6|3|12|A – combine harvester
Q1(b)|4|3|12|avoid overhead power lines
Q2(a)|3|4|12|Reduces soil erosion and run off
Q2(b)|3|4|12|polyculture maximises space
Q2(c)|4|4|12|low intensity mowing
Q3(a)(i)|4|5|12|Input: Carbon dioxide / water / light
Q3(a)(ii)|6|5|12|superior seed selection
Q3(b)(i)|3|5|13|Correct placement on diagram
Q3(b)(ii)|3|5|13|N, P, K, S, Mg, Ca
Q3(b)(iii)|4|5|13|Identify two possible
Q4(a)|6|6|13|slurry gases or falling into tank
Q4(b)|2|6|13|have side rails on pit
Q4(c)|2|6|13|ensure machines don’t run into
Q5(a)|7|7|13|C – Shorthorn
Q5(b)|3|7|14|a roan colour, by placing a tick
Q6|10|8|14|1+1+2+2+4
Q7|10|8|14|Complete the breeding
Q8(a)(i)|4|9|14|Bacteria / fungi / actinomycetes
Q8(a)(ii)|6|9|14|Nutrient cycling / nutrient availability
Q8(b)(i)|3|9|14|To stir the mixture of soil and water
Q8(b)(ii)|3|9|14|clear water to see colour change
Q8(b)(iii)|4|9|14|Wash the probe of the meter
Q9(a)|10|10|15|always observe
Q9(b)(i)|5|11|15|Poisonous or toxic
Q9(b)(ii)|5|11|15|quarantine sick animals / closed herd
Q10(a)|6|12|15|White clover – perennial
Q10(b)|4|12|15|herbicide or spot
Q11(a)|4|13|16|monogastric by placing a tick
Q11(b)|6|13|16|C = Rectum
Q12(a)(i)|4|14|16|100 – 95 = 5%
Q12(a)(ii)|6|14|16|try to form thread into a ring
Q12(b)(i)|4|15|16|A – graduated cylinder
Q12(b)(ii)|3|15|16|To form a soil solution
Q12(b)(iii)|3|15|16|use the soil textural
Q13(a)(i)|6|18|17|A – Vegetative
Q13(a)(ii)|2|18|17|A or vegetative
Q13(a)(iii)|4|19|17|digestible sugars are the highest
Q13(a)(iv)|8|19|17|grazing / rest period / sward composition
Q13(b)(i)|8|19|17|5 Cover the pit
Q13(b)(ii)|6|19|17|Identify two tests that determine
Q13(c)(i)|8|20|17|2nd step – D
Q13(c)(ii)|8|20|17|Data driven approach to management
Q14(a)(i)|6|21|18|C – Blackface mountain
Q14(a)(ii)|5|21|18|Blackface mountain or C
Q14(a)(iii)|6|21|18|Rams A and D are classed as terminal sires.
Q14(b)(i)|6|22|18|Correct position of X where finishing is indicated.
Q14(b)(ii)|9|22|18|steaming up – gradual increase of concentrates
Q14(c)(i)|10|23|19|Named grazing system
Q14(c)(ii)|8|23|19|reliance on technology (batteries, connectivity)
Q15(a)(i)|8|24|19|C – Parent rock
Q15(a)(ii)|6|24|19|Soil forms slowly from the breakdown of rocks
Q15(a)(iii)|6|24|19|crumbly texture
Q15(b)(i)|4|25|19|Identify the meaning of the underlined term by placing a tick
Q15(b)(ii)|4|25|19|Poor drainage / low organic matter
Q15(b)(iii)|6|25|20|Decreased yield / poor root penetration
Q15(b)(iv)|10|25|20|reduced lameness rates
Q15(c)|6|26|20|places the slurry on the soil
Q15(d)(i)|5|26|20|Explain why Teagasc included a field with no slurry
Q15(d)(ii)|1|26|20|Trailing shoe or Field 2
Q16(a)(i)|4|27|20|black whitehead
Q16(a)(ii)|1|27|20|dairy or beef farm by placing a tick
Q16(a)(iii)|2|27|20|Identification / traceability
Q16(a)(iv)|8|27|20|know stock ancestors
Q16(a)(v)|8|27|21|No swollen naval
Q16(b)(i)|2|28|21|By age / by size
Q16(b)(ii)|8|28|21|Milk or milk replacer
Q16(b)(iii)|8|28|21|reduced workload
Q16(c)(i)|3|29|21|Identify the disease the calf is likely to be
Q16(c)(ii)|3|29|21|calf jacket
Q16(c)(iii)|3|29|21|Ensure good quality colostrum
Q16(d)(i)|3|29|21|Identify the target weaning weight
Q16(d)(ii)|6|29|21|90 x 5.50 x 10
Q17(a)(i)|2|30|22|Fertiliser that is protected with a urease inhibitor
Q17(a)(ii)|8|30|22|sow multi-species swards
Q17(a)(iii)|4|30|22|Identify inefficiencies
Q17(b)(i)|12|31|22|B / C / D / A
Q17(b)(ii)|2|31|22|Be careful when working near PTO
Q17(c)|22|32|22|Drought conditions will reduce the germination rate
Q18(a)(i)|8|33|23|Feed quality / feed type
Q18(a)(ii)|8|33|23|check for mastitis or CMT
Q18(a)(iii)|4|33|23|To reduce bacteria multiplication
Q18(a)(iv)|4|33|23|Udder infection
Q18(a)(v)|8|33|23|spoiled feed or bedding
Q18(b)(i)|9|34|23|Correct point
Q18(b)(ii)|9|35|23|C – median suspensory ligament
'''

POOLS_2026_ORDINARY = {
    'Q1(a)': (3, ['A', 'B', 'C', 'D']),
    'Q4(a)': (2, ['A', 'B', 'C']),
    'Q4(b)': (1, ['A', 'B', 'C']),
    'Q5(a)': (3, ['A', 'B', 'C', 'D']),
    'Q9(a)': (3, ['Lock cows in a proper calving gate', 'Good handling facilities when moving cows to and from calving pens', 'Have two escape points in a calving pen',
                  'Never turn your back on a freshly calved cow', 'Keep dogs/children away from calving shed']),
    'Q9(b)(i)': (2, ['A', 'B', 'C']),
    'Q10(a)': (2, ['Barley', 'White clover', 'Potato']),
    'Q14(a)(i)': (3, ['A', 'B', 'C', 'D']),
    'Q18(b)(ii)': (3, ['A', 'B', 'C', 'D']),
}

# 2025 Higher: Section A Q1-Q12 at 10 marks, Section B Q13-Q18 at 50. The
# scheme's Q14(b)(i) prints 4x4 plus a separate 1 for the result: 17.
HIGHER_2025 = '''
Q1(a)|6|3|12|A: Aberdeen Angus
Q1(b)|2|3|12|A or Aberdeen Angus
Q1(c)|2|3|12|Does not have horns
Q2(a)|10|4|12|Completes its life cycle in one year
Q2(b)(i)|4|5|12|Intramuscular fat found in meat
Q2(b)(ii)|2|5|12|Animals with good temperament are easier to handle
Q2(b)(iii)|4|5|12|Guaranteed income / no unwanted calves
Q3(a)(i)|6|6|13|Allow cows to groom or scratch
Q3(a)(ii)|4|6|13|Two points on any named valid piece of technology
Q3(b)(i)|5|7|13|Less risk to animals from noxious (harmful) gases
Q3(b)(ii)|5|7|13|Increased nutrient levels in slurry
Q4(a)(i)|5|8|13|disease that can be transmitted from animal to human
Q4(a)(ii)|3|8|13|Sale or movement of infected cattle
Q4(a)(iii)|2|8|13|Stock proof fencing on farm boundaries
Q4(b)(i)|2|9|14|Clostridium chauvoei
Q4(b)(ii)|3|9|14|Soil / animal faeces
Q4(b)(iii)|3|9|14|Swollen joints or muscles
Q4(b)(iv)|2|9|14|Vaccination / remove from infected land
Q5(a)|4|10|14|Reduced feed intake due to stress
Q5(b)|4|10|14|Rapeseed, vegetable oil
Q5(c)|2|10|14|56 x 63 = 3528 kg
Q6(a)|6|11|15|A: Stomach tube / C: heat lamp / D: ropes
Q6(b)|4|11|15|Ropes are tied above the hooves
Q7(a)|5|12|15|Bacteria / fungi / actinomycetes
Q7(b)|5|12|15|Decomposition of OM to humus
Q8(a)|10|13|16|Symbiotic bacteria or Rhizobium
Q9(a)|10|14|16|Put a soil sample in clean beaker
Q9(b)(i)|4|15|16|Field 2 and Field 3
Q9(b)(ii)|4|15|16|Liming the soil to raise pH
Q9(b)(iii)|2|15|16|pH affects nutrient availability
Q10(a)|4|16|16|who is used for producing lambs for
Q10(b)|6|16|16|assessing muscle and fat would allow the farmer to
Q11(a)|6|17|17|Be part of quality assurance scheme
Q11(b)|4|17|17|Contribute to farm income
Q12|10|18|17|Close to surface to maximise photosynthesis
Q13(a)(i)|4|21|18|Sell as beef animals
Q13(a)(ii)|2|21|18|Early calving cows
Q13(a)(iii)|1|21|18|These calves will be used as replacements
Q13(a)(iv)|2|21|18|Calculate the replacement rate for the herd.
Q13(a)(v)|6|22|18|120 – 113 = 7 barren cows
Q13(a)(vi)|6|22|18|Jersey / Norwegian Red / Holstein
Q13(a)(vii)|6|22|18|Disease control / biosecurity
Q13(b)(i)|3|22|18|Keeping data (records) on the milk yield
Q13(b)(ii)|5|22|18|Identify barren cows / predicting calving dates
Q13(b)(iii)|5|23|19|Identify best and worst producing animals
Q13(c)(i)|5|23|19|12 – 18 hours
Q13(c)(ii)|5|23|19|Missed ovulation / inaccurate heat detection
Q13(d)(i)|5|24|19|Oxytocin
Q13(d)(ii)|5|24|19|Sight of the calf
Q14(a)(i)|10|25|19|(Compacted structure or) hard pan
Q14(a)(ii)|6|25|19|30 – 10 = 20%
Q14(a)(iii)|3|26|19|Sand has larger pore spaces
Q14(b)(i)|17|26|19|*Result: valid result for investigation described
Q14(b)(ii)|6|27|20|Compacted and uncompacted soil
Q14(b)(iii)|2|27|20|Record the exact mass
Q14(c)|6|27|20|Ploughing / subsoiling
Q14(d)|6|27|20|Poaching/use of heavy machinery
Q15(a)(i)|8|28|20|The observable characteristics of an organism
Q15(a)(ii)|7|28|20|Disease resistance / yield / early ripening
Q15(a)(iii)|8|29|20|C and D are first two steps in either order
Q15(a)(iv)|8|29|21|Dominant trait: Purple
Q15(b)|3|30|21|D: Oilseed rape
Q15(c)|16|30|21|One point under each heading and the fourth point from any heading
Q16(a)(i)|4|32|22|Identify the animal with the higher intake of feed.
Q16(a)(ii)|4|32|22|Identify which animal had the better food conversion ratio (FCR).
Q16(a)(iii)|4|32|22|Charolais: 725/654 = 1.1 kg
Q16(a)(iv)|3|32|22|Identify the animal with the inferior feed efficiency.
Q16(a)(v)|2|33|22|The amount of feed required to produced (1) kg of liveweight gain
Q16(a)(vi)|9|33|22|Breed / sex / health or disease
Q16(b)|6|33|22|446 x 5.25 = 2341.50
Q16(c)(i)|6|34|22|Presence of oxygen allows anaerobic bacteria
Q16(c)(ii)|6|34|22|Butyric acid – lactic acid
Q16(c)(iii)|3|34|22|Be more specific on the location
Q16(c)(iv)|3|34|22|Teagasc / Department of Agriculture
Q17(a)(i)|2|35|23|A sheep that is 1-2 years old
Q17(a)(ii)|4|35|23|145-150 days
Q17(a)(iii)|6|35|23|Ensure sheep are at the correct BCS
Q17(a)(iv)|6|36|23|udder with no defects
Q17(a)(v)|6|36|23|Could interfere with breeding program
Q17(b)(i)|6|36|23|Good ventilation / good hygiene
Q17(b)(ii)|6|36|23|Sheep crate or race for examining livestock
Q17(c)(i)|10|37|23|6 points plotted for Caledonia
Q17(c)(ii)|4|37|23|Variety: Caledonia
Q18(a)(i)|12|38|24|Anthelminthic properties / drought resistant
Q18(a)(ii)|6|38|24|Direct drilling: Land is grazed bare
Q18(a)(iii)|6|38|24|Do a soil test to establish nutrients
Q18(b)|12|39|24|Throw a quadrat / do a plant count
Q18(c)(i)|2|40|24|The point at which a seedling is able to absorb nutrients
Q18(c)(ii)|12|40|24|Difficulties to cultivate land
'''

POOLS_2025_HIGHER = {
    'Q2(a)': (2, ['Annual', 'Biennial', 'Perennial']),
    'Q2(b)(ii)': (2, ['Meat quality', 'Good growth rates', 'Ease of calving', 'Docility', 'Fertility']),
    'Q6(b)': (1, ['Stomach tube', 'Heat lamp', 'Ropes']),
    'Q7(b)': (1, ['Water retention', 'Plant carbon sink', 'Carbon sequestration', 'Plant growth promotion']),
    'Q12': (4, ['a', 'b', 'c', 'd', 'e']),
    'Q15(b)': (3, ['A', 'B', 'C', 'D']),
}

# 2025 Ordinary: Section A Q1-Q12 at 10 marks, Section B Q13-Q18 at 50.
ORDINARY_2025 = '''
Q1(a)(i)|6|3|12|D: Holstein Friesian
Q1(a)(ii)|4|3|12|Limousin or Charolais
Q1(b)(i)|5|4|12|Easy calving / good conformation / no horns
Q1(b)(ii)|2|4|12|Identify the correct meaning of the term polled
Q1(b)(iii)|3|4|12|Belgian Blue
Q2|10|5|12|Indicate if the following are true or false
Q3|10|5|12|Identify the farm machinery from the descriptions
Q4(a)|5|6|13|Paddocks near yard or yard at the centre
Q4(b)|3|6|13|slurry storage, by placing an X on the structure
Q4(c)|2|6|13|large paddocks could be divided into strips
Q5(a)|5|7|13|seedling is largest in picture B
Q5(b)|2|7|13|It is a clay soil / under continuous grassland
Q5(c)|3|7|13|Identify the conditions
Q6(a)|5|8|13|Act as pollinators or support crop production
Q6(b)|5|8|13|Use of pesticides or herbicides / monoculture
Q7(a)|6|8|14|D: Chicory
Q7(b)|4|8|14|Nettle or C
Q8(a)|5|9|14|Wear gloves / wear goggles
Q8(b)|5|9|14|Symbols 2 and 3
Q9(a)(i)|5|10|14|Fore or front legs first
Q9(a)(ii)|5|10|14|Isolate the cow / clean bedding
Q9(b)(i)|3|11|14|Decreased
Q9(b)(ii)|2|11|14|Means: Costs less to produce
Q9(b)(iii)|3|11|14|Identify which agricultural enterprise output price has increased.
Q9(b)(iv)|2|11|14|Increased profit
Q10(a)|3|12|15|Sperm or male
Q10(b)|3|12|15|Identify which chromosome X or Y is responsible
Q10(c)|4|12|15|90% or better chance of female calf
Q11(a)(i)|3|13|15|Spring calving
Q11(a)(ii)|3|13|15|Walking on uneven or damaged surfaces
Q11(a)(iii)|4|13|15|5000 / 100 = €50 per cow
Q11(b)(i)|5|14|15|Less pressure on joints or improved lying behaviour
Q11(b)(ii)|5|14|15|Easier to clean so more hygienic
Q12(a)(i)|3|15|16|Abortion and stillbirth
Q12(a)(ii)|2|15|16|Bar inserted in graph to height of 20
Q12(a)(iii)|5|15|16|Ensure ewes lamb indoors
Q12(b)(i)|3|16|16|Identify which lamb had a higher growth rate
Q12(b)(ii)|2|16|16|(More) competition for nutrients
Q12(b)(iii)|3|16|16|Predict which lamb will have a higher weight at slaughter.
Q12(b)(iv)|2|16|16|42kg
Q13(a)(i)|9|18|17|Multiple samples (20) taken
Q13(a)(ii)|5|18|17|Advise Mia on how many samples she should take.
Q13(a)(iii)|4|18|17|Soil augur or probe
Q13(b)|8|19|17|Rub soil sample between fingers
Q13(c)(i)|4|20|17|Loam soil
Q13(c)(ii)|4|20|17|Good drainage / good aeration
Q13(c)(iii)|12|20|18|Grass / potatoes / clover
Q13(c)(iv)|4|20|18|Raises soil pH / increases nutrient availability
Q14(a)(i)|5|21|18|February
Q14(a)(ii)|9|21|18|accept valid weather condition with matching valid impact
Q14(a)(iii)|4|22|19|Cattle poach land
Q14(b)(i)|4|22|19|The seeds in the polytunnel will have a higher germination rate
Q14(b)(ii)|4|22|19|Temperature: Independent
Q14(b)(iii)|4|22|19|The polytunnel had a higher germination rate
Q14(b)(iv)|4|23|19|89/100 x 100/1 = 89%
Q14(c)(i)|3|23|19|Choose the correct minimum germination rate for certified seed.
Q14(c)(ii)|5|23|19|Analytical purity of 98%
Q14(c)(iii)|8|23|19|L: Oilseed rape
Q15(a)(i)|4|24|20|The value is increased by undergoing processing
Q15(a)(ii)|5|24|20|Using glass bottles or bottles from the customers
Q15(a)(iii)|4|24|20|Identify the meaning of pasteurisation.
Q15(b)(i)|12|25|20|Diet of cow / breed of cow
Q15(b)(ii)|7|25|20|Mastitis / TB / BVD
Q15(b)(iii)|6|25|20|Identify the nutrients A and B in the chart.
Q15(c)|12|26|20|add 1ml of Resazurin solution
Q15(d)(i)|8|27|20|Place each step in the correct order.
Q15(d)(ii)|4|27|20|Source of fibre to aid digestion
Q16(a)(i)|10|28|21|Slatted floor / rubber mats
Q16(a)(ii)|6|28|21|Good ventilation (to reduce chance of air borne diseases)
Q16(a)(iii)|6|28|21|Secure pens or fencing
Q16(b)|8|29|21|Weigh a sample of silage
Q16(c)(i)|6|30|21|Identify the average DM% of grass silage.
Q16(c)(ii)|6|30|21|Stage of growth / DMD / cutting height
Q16(c)(iii)|8|30|21|Hay / concentrates / kale
Q17(a)(i)|9|31|22|Improve aeration or root growth
Q17(a)(ii)|4|31|22|Add manure or add organic matter
Q17(b)(i)|3|31|22|Identify the statement which best describes flocculation.
Q17(b)(ii)|16|32|22|Arrange the steps that show the order of flocculation.
Q17(b)(iii)|3|32|22|Same amount of soil (clay) or water
Q17(b)(iv)|3|32|22|Qualitative
Q17(c)|12|33|22|Involved in chlorophyll production
Q17(d)|12|33|23|Named breed must be linked to the choice
Q18(a)(i)|3|34|23|The ratio of lean meat to fat
Q18(a)(ii)|5|34|23|BCS: 3
Q18(a)(iii)|4|34|23|More efficient management
Q18(b)(i)|4|35|23|365-285 = 80 days
Q18(b)(ii)|9|35|24|C – mating: April- May
Q18(b)(iii)|9|35|24|2 separate fields indicated
Q18(c)(i)|6|36|24|Infant food
Q18(c)(ii)|6|36|24|265,000 to 275,000
Q18(c)(iii)|4|36|24|Yellow (due to carotene in grass)
'''

POOLS_2025_ORDINARY = {
    'Q1(a)(i)': (3, ['A', 'B', 'C', 'D']),
    'Q7(a)': (3, ['A', 'B', 'C', 'D']),
    'Q14(c)(iii)': (2, ['J', 'K', 'L']),
}

# 2024 Higher: Section A Q1-Q12 at 10 marks, Section B Q13-Q18 at 50 (Q18's
# published allocations total 54; see MODERN_LAYOUTS).
HIGHER_2024 = '''
Q1(a)|6|3|12|C: Head gate / fostering crate
Q1(b)|4|3|12|Filled with colostrum / tube is put down oesophagus
Q2(a)(i)|4|4|12|B: Blue Leicester
Q2(a)(ii)|2|4|12|Produce many offspring
Q2(a)(iii)|4|4|12|Good conformation / high muscle
Q2(b)(i)|3|5|12|Occurs when a cow cannot get sufficient energy
Q2(b)(ii)|3|5|12|Superb quality beef / distinctive flavour
Q2(b)(iii)|4|5|12|Early maturing – steers finish between 20-24 months
Q3(a)(i)|1|6|13|Short (1-2 days)
Q3(a)(ii)|1|6|13|Reduced root growth during grazing
Q3(a)(iii)|8|6|13|Set stocking
Q3(b)|10|7|13|Any 3 factors
Q4|10|8|14|Decreased nutrient store
Q5(a)|7|9|14|Oats Wheat Barley 5+2(1)
Q5(b)|3|9|14|Not certified seed
Q6(a)|10|10|15|Scanning in-lamb ewes
Q6(b)(i)|6|11|15|132 x 12 = €1584
Q6(b)(ii)|4|11|15|Flystrike control
Q7(a)|4|12|16|Integration of trees with either crops or livestock
Q7(b)|6|12|16|enhancing the capacity for on-farm
Q8(a)|2|13|16|A living organism that kills and eats another organism
Q8(b)|2|13|16|Controls the dock leaf without the use of (selective) herbicides
Q8(c)|6|13|16|Aphids (greenfly)
Q9(a)|10|14|16|No ions present / no ion
Q9(b)(i)|6|14|16|A: Good B: Moderate C: Poor
Q9(b)(ii)|4|14|16|Soil particles are predominantly small
Q10(a)|4|15|17|Identify which picture A or B is more likely to be a multi-species sward.
Q10(b)|4|15|17|PRG / red clover / white clover / plantain / chicory / timothy
Q10(c)|2|15|17|increased microbial communities
Q11(a)|4|16|17|= 375.25 or 375 days
Q11(b)|2|16|17|More accurate heat detection
Q11(c)|4|16|17|Cow: 2
Q12(a)|6|17|17|include buffer zones
Q12(b)|4|17|17|farm plastics / nitrogen leaching
Q13(a)(i)|12|21|18|Throw pen at random / place quadrat
Q13(a)(ii)|8|22|18|Primrose Nettle Ragwort Meadow Thistle
Q13(a)(iii)|8|22|18|Reduce the amounts of fertiliser added
Q13(b)(i)|8|23|18|iron pan formation
Q13(b)(ii)|6|23|18|West of Ireland / midlands / any named correct location
Q13(c)|8|24|18|Healthy peat bogs act as
Q13(d)|8|24|18|install bird or bat or owl boxes
Q14(a)(i)|6|25|19|Lactobacillus
Q14(a)(ii)|12|25|19|lactobacillus bacteria feed off sugar
Q14(a)(iii)|6|25|19|Identify the ideal DM % of good quality silage
Q14(b)(i)|12|26|19|repeat weighing until you get a
Q14(b)(ii)|8|27|19|stage of growth at cutting / chop length
Q14(c)|6|27|19|Name: Vegetative
Q14(d)|6|27|20|Palatability / digestibility or leafy / productivity / persistence
Q15(a)(i)|3|28|20|All observable or physical characteristics of the animal
Q15(a)(ii)|9|28|20|Repair / build muscle / milk production
Q15(a)(iii)|4|28|20|State two animal-related factors or two environmental conditions.
Q15(a)(iv)|3|29|20|low energy requirement
Q15(a)(v)|6|29|21|Briefly describe the symptoms and prevention of a named mineral deficiency in
Q15(b)(i)|6|29|21|forecast time of sale of animals
Q15(b)(ii)|9|29|21|Have an escape route
Q15(c)(i)|6|30|21|85/105 = 0.81(kg/day)
Q15(c)(ii)|4|30|22|€20 X 50 = €1000
Q16(a)(i)|2|31|22|Hypothesis must include effect on health or performance
Q16(a)(ii)|7|31|22|It is a fair test (Yes)
Q16(a)(iii)|11|31|22|Independent: Colostrum sample
Q16(a)(iv)|4|32|22|Scales not calibrated
Q16(b)(i)|4|32|22|Pooled colostrum is best
Q16(b)(ii)|4|32|22|has little effect on calf performance
Q16(c)|6|32|22|*Introduce hay or concentrates
Q16(d)|12|33|23|10% bodyweight / 4 litres
Q17(a)|6|34|23|5 (factor) + 1
Q17(b)(i)|5|34|23|diagram must show root with rhizosphere zone
Q17(b)(ii)|3|34|23|Symbiotic relationship
Q17(b)(iii)|6|34|24|Mycorrhizal
Q17(b)(iv)|6|35|24|Enhance water holding capacity
Q17(b)(v)|6|35|24|Reducing tillage operations
Q17(c)(i)|6|36|24|as it is formed from partially decomposed plant
Q17(c)(ii)|6|36|24|55.2/90 X 100 = 61.3(%)
Q17(c)(iii)|6|36|24|61.3 x 0.58 = 35.55 or 36%
Q18(a)(i)|4|37|25|Offspring produced from purebred parents of different breeds
Q18(a)(ii)|8|37|25|A: Hereford
Q18(a)(iii)|8|37|25|Black coat colour / coat pattern / white face
Q18(b)(i)|4|38|25|Genetic make-up (code) of an organism
Q18(b)(ii)|8|38|25|Parent verification
Q18(b)(iii)|6|38|25|Or other valid example and explained importance
Q18(c)|16|39|26|6+6+4
'''

POOLS_2024_HIGHER = {
    'Q2(a)(i)': (2, ['A', 'B', 'C']),
    'Q6(a)': (2, ['Lameness control', "Mineral supplementation of ewe's post mating", "Meal feeding of lamb's post weaning", 'Scanning of in-lamb ewes']),
    'Q6(b)(ii)': (2, ['Mineral supplementation of lambs pre-weaning', 'Flystrike control', 'Genotyping of ram']),
    'Q15(a)(iii)': (1, ['Animal-related factors', 'Environmental conditions']),
}

# 2024 Ordinary: Section A Q1-Q12 at 10 marks, Section B Q13-Q18 at 50.
ORDINARY_2024 = '''
Q1(a)|3|3|12|direction of grazing
Q1(b)|3|3|12|(Moveable)(Electric) Fence
Q1(c)|2|3|12|Strip grazing
Q1(d)|2|3|12|Leafy grass or more digestible grass
Q2(a)|10|4|12|Plate cooler
Q2(b)(i)|3|5|12|Restrain animals or allow treatment
Q2(b)(ii)|3|5|12|natural circling behaviour of cattle
Q2(b)(iii)|2|5|12|Easy to operate
Q2(b)(iv)|2|5|12|Be careful of swinging gates
Q3|10|6|13|Topography refers to the slope of the land
Q4|10|6|13|Red water fever
Q5(a)|6|7|13|A: Omasum
Q5(b)|4|7|13|Identify the first feed required by the calf
Q6(a)(i)|6|8|13|B: Border Leicester
Q6(a)(ii)|4|8|13|large amount of muscle / lean meat
Q6(b)(i)|3|9|14|Explain selective grazers.
Q6(b)(ii)|3|9|14|Allow plants to recover
Q6(b)(iii)|4|9|14|Reduced overgrazing
Q7(a)|6|10|14|Machine size: big heavy machines compact the soil
Q7(b)|4|10|14|Identify the % air in the ideal soil composition.
Q8(a)|6|11|14|Help animals regulate body temperature
Q8(b)|4|11|14|Collars can read the temperature of the cow
Q9(a)(i)|3|12|15|Root(hairs)
Q9(a)(ii)|4|12|15|N / P / K / Ca / Mg / S / other valid answer
Q9(a)(iii)|3|12|15|Identify the bacteria found in clover
Q9(b)|10|12|15|Fertiliser spreading
Q10(a)|2|13|15|Explain artisan product.
Q10(b)|2|13|15|Identify the meaning of niche market.
Q10(c)(i)|3|13|15|Using your knowledge of the composition of cow’s milk
Q10(c)(ii)|3|13|15|Protein or casein or whey
Q11(a)(i)|3|14|16|Egg production
Q11(a)(ii)|3|14|16|In step 2, state which hen A, B or C is the best offspring
Q11(a)(iii)|4|14|16|two characteristics of dairy cattle.
Q11(b)(i)|6|15|16|Double muscled
Q11(b)(ii)|4|15|16|Cow: B or Charolais
Q12(a)|8|16|16|amount of fertiliser
Q12(b)|2|16|16|the plant growth (rate)
Q13(a)(i)|16|19|17|Throw pen at random
Q13(a)(ii)|12|20|17|A: Nettle
Q13(b)(i)|6|20|17|4/10 x 100/1 = 40%
Q13(b)(ii)|4|21|17|State: Quantitative
Q13(b)(iii)|6|21|17|Identify the most suitable chart or graph
Q13(b)(iv)|6|21|17|Quadrat was thrown multiple times
Q14(a)(i)|6|22|18|Fertiliser applied (6 weeks in advance)
Q14(a)(ii)|3|22|18|Identify the best time of the year to cut grass for silage by placing an X on the diagram.
Q14(a)(iii)|3|22|18|Less digestible / poor yield
Q14(b)(i)|2|22|18|Identify the correct stage of cutting the grass for silage
Q14(b)(ii)|2|23|18|Leafy grass / no seed heads / more digestible
Q14(b)(iii)|2|23|18|Identify the growth stage of plant B
Q14(c)(i)|12|23|18|Cut a number of grass samples
Q14(c)(ii)|8|24|19|Allow 2 + 2 for name or description
Q14(d)|12|24|19|Method of preservation
Q15(a)(i)|8|25|20|Flushing or high plane of nutrition
Q15(a)(ii)|12|25|20|Fallopian tube
Q15(b)(i)|8|26|20|Feet or legs / mouth / testicles
Q15(b)(ii)|6|26|20|To mark the ewes that have been served.
Q15(b)(iii)|2|26|20|State how often a raddle colour would be changed
Q15(b)(iv)|6|26|20|Yellow / C
Q15(c)(i)|6|27|20|Identify the average ratio of rams to ewes
Q15(c)(ii)|2|27|20|prevent injury to the ram
Q15(d)|8|27|20|Explain seasonal polyoestrous.
Q16(a)(i)|3|28|21|Explain organic matter.
Q16(a)(ii)|6|28|21|Add FYM / slurry
Q16(a)(iii)|6|28|21|improves water retention
Q16(a)(iv)|6|28|21|Rainfall or soil moisture
Q16(b)|12|29|21|place in a crucible
Q16(c)(i)|6|30|21|25/100 x 100/1 = 25(% OM)
Q16(c)(ii)|5|30|21|Peat soil
Q16(c)(iii)|6|30|21|25 x 0.58 = 14.5(%)
Q17(a)(i)|3|31|22|Farmer gets to choose the sex of the calf
Q17(a)(ii)|3|31|22|Incorporate genetics from years ago
Q17(a)(iii)|12|31|22|Disadvantages: heat detection
Q17(b)(i)|8|32|22|Barley (or another valid crop):
Q17(b)(ii)|8|32|23|Harvested: combine harvester
Q17(b)(iii)|4|32|23|Be careful of PTO
Q17(c)|12|33|23|fans or machine hygiene
Q18(a)(i)|12|34|24|Have all equipment (calving jack etc.)
Q18(a)(ii)|11|34|24|Iodine on navel
Q18(a)(iii)|6|34|24|(Holstein) Friesian
Q18(b)|15|35|24|1st housing
Q18(c)|6|35|24|High plane of nutrition / concentrates
Q18(d)|6|35|24|State the duration of each of the following in dairy cows.
'''

POOLS_2024_ORDINARY = {
    'Q5(a)': (3, ['A', 'B', 'C', 'D']),
    'Q6(a)(i)': (3, ['A', 'B', 'C', 'D']),
    'Q6(a)(ii)': (1, ['Texel', 'Suffolk', 'Charolais', 'Border Leicester']),
    'Q7(a)': (3, ['Machine size', 'Soil water content', 'Tillage system', 'Crop rotation']),
    'Q13(a)(ii)': (3, ['A', 'B', 'C', 'D']),
}

# 2023 Higher: Section A Q1-Q12 at 10 marks, Section B Q13-Q18 at 50.
HIGHER_2023 = '''
Q1(a)(i)|6|3|12|A – Short horn
Q1(a)(ii)|2|3|12|provides at least 2 kinds of resources
Q1(a)(iii)|2|3|12|Better quality offspring
Q1(b)(i)|6|4|12|D – Jersey
Q1(b)(ii)|4|4|12|Industry: Dairy
Q2(a)|6|5|12|Rapid growth of stems
Q2(b)|4|5|12|Shepherd’s purse
Q3(a)|2|6|13|Grass / plant: lime
Q3(b)|2|6|13|Weathering of limestone
Q3(c)|6|6|13|Milk Fever or hypocalcaemia
Q4(a)|6|7|13|To kill any worms (endoparasites)
Q4(b)|4|7|13|Establishing the genetic potential of particular bulls
Q5(a)|6|8|14|take a minimum of 20 soil cores
Q5(b)|2|8|14|soil nutrient levels change slowly over time
Q5(c)|2|8|14|Soil tests allow you to identify the key nutrients
Q6(a)|4|9|14|Scald / foot rot / shelly hoof
Q6(b)|2|9|14|red moist skin between digits
Q6(c)|2|9|15|Antibiotic sprays or footbaths are usually sufficient
Q6(d)|2|9|15|It has a direct effect on production
Q7(a)|10|10|15|280 - 283
Q7(b)|10|10|16|ASSAP (water)
Q8(a)|4|11|17|Independent – Fertiliser type
Q8(b)|3|11|17|Repeating an experiment more than once
Q8(c)|3|11|17|farmers should use protected urea
Q9(a)(i)|2|12|17|Controlling of weeds prior to the germination of the crop
Q9(a)(ii)|6|12|17|Less chemical herbicide required
Q9(a)(iii)|2|12|17|Soil moisture sensors
Q9(b)(i)|6|13|17|Know if the animal is barren or not
Q9(b)(ii)|4|13|18|Be there to assist with calving
Q10(a)(i)|6|14|18|A: Liver
Q10(a)(ii)|4|14|18|Assist in the digestion of feedstuffs
Q10(b)(i)|6|15|18|Accept source of nutrient or function of nutrient
Q10(b)(ii)|2|15|18|As animals get older they don’t grow as fast
Q10(b)(iii)|2|15|18|Cannot breakdown the cellulose in the grass
Q11(a)|6|16|19|Good heat detection
Q11(b)|4|16|19|correct BCS of 3.0 at mating
Q12(a)|3|17|19|1.1(kg/m
Q12(b)|3|17|19|Slurry lagoon is not covered
Q12(c)|2|17|19|As slurry is less dilute there are more nutrients available
Q12(d)|2|17|19|Use a weighted container into tank
Q13(a)(i)|14|20|20|5+5+2+2
Q13(a)(ii)|12|20|20|Any three labels = 3(2) marks
Q13(b)(i)|9|21|20|A: Saturation
Q13(b)(ii)|3|21|21|Plants can remove water from the soil easily
Q13(c)|12|22|21|OR FIELD METHOD
Q13(d)(i)|6|23|21|Assists farmers in deciding when to drain the land
Q13(d)(ii)|6|23|21|Provide water to plants
Q14(a)|3|24|22|the seed is placed without any prior soil cultivation
Q14(b)(i)|5|24|22|Harvest at different times
Q14(b)(ii)|3|24|22|To sow two crops together
Q14(b)(iii)|6|24|22|encourage mycorrhizal fungi
Q14(b)(iv)|3|25|22|Completes its lifecycle in one year.
Q14(b)(v)|3|25|22|Barley / wheat / oats / other valid example
Q14(c)(i)|12|25|22|multiply by 80,000
Q14(c)(ii)|6|26|22|if correct seeding rate was used
Q14(c)(iii)|4|26|22|it is hard to see individual plants
Q14(c)(iv)|5|26|22|certified seed has min
Q15(a)|12|27|23|use soil triangle to find soil texture
Q15(b)(i)|6|28|23|5.5 – 7.5
Q15(b)(ii)|3|28|23|pH probe or meter
Q15(b)(iii)|7|28|23|Increase in earthworm activity
Q15(c)(i)|6|28|23|*6.9
Q15(c)(ii)|8|29|23|The higher the soil pH the lower the
Q15(d)|8|29|24|Sowing certified seed
Q16(a)(i)|5|30|24|*Animal digestion
Q16(a)(ii)|6|30|24|As the average for the enterprise is over 40%
Q16(a)(iii)|6|30|24|their carbon emissions have remained fairly constant
Q16(b)(i)|12|31|24|4+4+2+2
Q16(b)(ii)|6|31|25|Soil cultivation or land reclamation
Q16(c)|15|32|25|Max 12 marks awarded if not shown on diagram
Q16(d)(i)|9|33|25|Increased pests and diseases introduced with warmer temperatures
Q16(d)(ii)|6|33|25|Reduce chemical N usage by sowing clover
Q17(a)(i)|16|34|26|Graze at 2 – 3 leaf stage
Q17(a)(ii)|8|35|26|Adding nitrogen / rolling
Q17(b)(i)|12|35|26|Get the best traits from each seed in his sward
Q17(b)(ii)|4|35|26|Ensures good digestible grass throughout the grazing season
Q17(b)(iii)|4|36|26|C = Chicory
Q17(c)|6|36|27|Pollen grains are light or plentiful
Q18(a)(i)|3|37|27|Median suspensory
Q18(a)(ii)|7|37|27|Hard swollen (udder) quarter
Q18(a)(iii)|4|37|27|Milk out the quarter
Q18(a)(iv)|6|37|28|Disinfect teats pre and post milking
Q18(a)(v)|8|38|28|4(2)
Q18(b)(i)|4|38|28|There is a higher total solid content in the evening
Q18(b)(ii)|18|39|28|F:3(3) +
'''

POOLS_2023_HIGHER = {
    'Q2(a)': (2, ['Germination', 'Stem Elongation', 'Flowering']),
    'Q2(b)': (2, ['Chickweed', 'Charlock', "Shepard's Purse"]),
    'Q4(a)': (3, ['Clipped', 'Worm dosed', 'Treated for lice', 'Sorted into pens based on breed and weight']),
    'Q13(b)(ii)': (2, ['Field capacity', 'Saturation', 'Permanent wilting point']),
    'Q17(b)(iii)': (2, ['A', 'B', 'C']),
    'Q17(c)': (1, ['sexually', 'asexually']),
    'Q18(a)(i)': (3, ['A', 'B', 'C', 'D']),
}

# 2023 Ordinary: Section A Q1-Q12 at 10 marks, Section B Q13-Q18 at 50.
ORDINARY_2023 = '''
Q1(a)|6|3|12|B: Graduated cylinder
Q1(b)|3|3|12|6.5*
Q1(c)|1|3|12|Soil pH is suitable or important for growing
Q2(a)|6|4|12|A: Charolais
Q2(b)|4|4|12|Safety / control bull / easier to handle
Q3(a)|8|5|12|Isolate calves from others for a few days
Q3(b)|2|5|12|Identify the weaning weight of a dairy beef calf at weaning.
Q4|10|6|13|Controlled grazing: increased yield of crop
Q5|10|7|13|Can carry disease
Q6(a)(i)|6|8|13|Body condition score
Q6(a)(ii)|3|8|13|Best quality silage = 76%+ DMD or A
Q6(a)(iii)|1|8|13|<67(%) or D
Q6(b)|10|9|14|Spread fertiliser or slurry 6 weeks before cutting
Q7(a)|6|10|14|(Average mother), not protective and
Q7(b)|4|10|14|So, a predator (e.g. fox / dog) won’t take them
Q8(a)|10|11|14|6+2+1+1
Q8(b)(i)|2|11|14|Identify the bacteria that does not cause mastitis in dairy cows.
Q8(b)(ii)|8|11|14|Wiping the teat with antiseptic wipe
Q9(a)(i)|3|12|15|Abomasum*
Q9(a)(ii)|4|12|15|As the animal gets older the rumen develops
Q9(a)(iii)|3|12|15|Identify the pH of the rumen by placing a tick
Q9(b)(i)|2|13|15|Omasum – absorption of water
Q9(b)(ii)|4|13|15|Sheep / cow
Q9(b)(iii)|4|13|15|4 stomachs or chambers
Q10(a)(i)|4|14|15|Cows calve in a short or defined period of time
Q10(a)(ii)|6|14|15|Fertility check or check for abnormalities
Q10(b)(i)|3|15|16|Bull 4
Q10(b)(ii)|3|15|16|Identify which bull has the best motility.
Q10(b)(iii)|2|15|16|State which bull is the most fertile and best to use with the maiden
Q10(b)(iv)|2|15|16|Crush / headgate
Q11|10|16|16|Labels=3(2)
Q12(a)|5|17|16|Spread (disease) from one organism (plant) to another
Q12(b)|3|17|16|Soil Temperature / air temperature
Q12(c)|2|17|16|Fast results so can treat the disease or pest quickly
Q13(a)(i)|6|20|17|Increased productivity or excess silage
Q13(a)(ii)|12|20|17|Perennial ryegrass
Q13(a)(iii)|6|20|17|Increased grass quality or production
Q13(b)(i)|6|21|17|Disc
Q13(b)(ii)|2|21|17|There is very little difference in the grass growth
Q13(b)(iii)|6|21|17|Cheaper than the conventional ploughing method
Q13(c)(i)|6|22|18|Intended use of grass
Q13(c)(ii)|6|22|18|Department of Agriculture / recommended varieties list
Q13(d)|12|22|18|Good weed control (selective herbicide)
Q14(a)(i)|4|23|18|Ability to prevent or reduce the presence of
Q14(a)(ii)|4|23|18|Element: N, P K, S etc.
Q14(a)(iii)|6|23|18|Factors-
Q14(a)(iv)|8|23|19|Be careful of moving machinery
Q14(b)(i)|8|24|19|Different crops sown
Q14(b)(ii)|4|24|19|Wildlife corridor
Q14(b)(iii)|4|25|19|Less chemicals required or reduce pollution
Q14(b)(iv)|12|25|19|cattle drinking in river
Q15(a)(i)|10|26|20|Random / min 20 samples
Q15(a)(ii)|10|26|20|less (air) spaces or soil particles closer together
Q15(a)(iii)|6|26|20|Reduced crop yield or delayed germination
Q15(a)(iv)|6|26|20|(Mole) plough or subsoil
Q15(a)(v)|6|27|20|Two open ended tubes
Q15(a)(vi)|2|27|20|failure to tap the glass
Q15(b)|10|28|20|A: Top Soil
Q15(c)|10|28|21|Organic matter – 5%
Q16(a)(i)|12|29|21|Total Bacterial Count on the Sample
Q16(a)(ii)|6|29|21|Independent
Q16(a)(iii)|4|30|22|Resazurin test – qualitative
Q16(b)(i)|12|30|22|Teat dipping pre and post milking
Q16(b)(ii)|6|30|22|= €452.17
Q16(c)(i)|2|31|22|balanced carbon footprint
Q16(c)(ii)|8|31|22|Barley: source of carbohydrate or energy
Q17(a)(i)|6|32|23|identify barren
Q17(a)(ii)|4|32|23|Explain the importance of having a good marking system
Q17(a)(iii)|6|32|23|Cull the ewes that are not in lamb
Q17(b)(i)|4|33|23|4 – 8 weeks prior to lambing
Q17(b)(ii)|6|33|23|Allow for early grass
Q17(b)(iii)|6|33|23|Adequate feeding space
Q17(c)|18|33|23|colostrum for antibodies
Q18(a)(i)|6|34|24|Genetic information
Q18(a)(ii)|12|34|24|Blood samples were taken from cow
Q18(a)(iii)|6|34|24|Sexed semen
Q18(b)(i)|4|35|24|Gene responsible for a specific trait is identified
Q18(b)(ii)|4|35|24|disease resistant plants or animals
Q18(b)(iii)|6|36|24|Impact on environment
Q18(c)(i)|4|36|24|Explain selective breeding.
Q18(c)(ii)|8|36|24|(High) crop yields
'''

POOLS_2023_ORDINARY = {
    'Q1(a)': (2, ['A', 'B', 'C']),
    'Q2(a)': (3, ['A', 'B', 'C', 'D', 'E']),
    'Q16(a)(i)': (1, ['Resazurin test', 'Total bacterial count']),
    'Q18(b)(iii)': (2, ['Impact on the environment', 'Effect on food chain', 'Increase in production']),
}

# 2022 Higher: Section A Q1-Q12 at 10 marks (any seven), Section B Q13-Q18 at 50 (any three).
HIGHER_2022 = '''
Q1(a)(i)|2|3|12|Organic matter contains the remains of plants and animals
Q1(a)(ii)|2|3|12|increased water‐holding capacity of the soil
Q1(a)(iii)|6|3|12|Weigh empty crucible
Q1(b)(i)|4|4|12|Rich in nutrients
Q1(b)(ii)|4|4|12|Livestock type / animal diet
Q1(b)(iii)–(iv)|2|4|12|In spring on an overcast and misty day*
Q2(a)|4|5|13|B = Blue Leicester
Q2(b)|6|5|13|Details on next page
Q3(a)|6|6|16|At least 2 trays of 100
Q3(b)|2|6|16|Quantitative*
Q3(c)|2|6|16|Seeds will not germinate at colder temperatures
Q4(a)|2|7|16|Disease causing (organism)
Q4(b)|6|7|16|TB / brucellosis
Q4(c)|2|7|16|Lock up or fence or surround with netting flocks
Q5(a)|6|8|17|genetics or breed / sex
Q5(b)(i)|2|8|17|2020*
Q5(b)(ii)|2|8|17|Improved breeding (genetics)
Q6(a)|6|9|18|Shelter for animals or crops
Q6(b)|2|9|18|Increased use of traditional breeds
Q6(c)|2|9|18|Adapted to local conditions
Q7(a)|4|10|18|333÷698 x 100÷1
Q7(b)|4|10|18|283÷200 = 1.4 kg ADG
Q7(c)|2|10|18|less efficient at
Q8(a)(i)|3|11|19|Crop rotation to prevent build‐up of pests
Q8(a)(ii)|3|11|19|Targeted treatment of cows with high SCC
Q8(b)|4|11|19|niche market commands higher price
Q9(a)(i)|6|12|20|D = 3, 2, 0
Q9(a)(ii)|4|12|20|rumen is not fully developed
Q9(b)(i)|4|13|20|Fibre (cellulose) degradation
Q9(b)(ii)|3|13|20|Majority of feed in Irish system is pasture based
Q9(b)(iii)|3|13|20|To ensure the safety of food
Q10(a)|2|14|21|Miscanthus – perennial
Q10(b)|4|14|21|rhizomes need to be planted at a depth
Q10(c)|4|14|21|renewable source of energy
Q11(a)(i)|4|15|22|Plant structure: Root hairs
Q11(a)(ii)|4|15|22|requiring energy
Q11(a)(iii)|2|15|22|Two organisms living together with mutual benefit
Q11(b)(i)|2|15|22|Growth of side shoots
Q11(b)(ii)|2|15|22|Phosphorus deficiency
Q11(b)(iii)|4|15|22|increased soil:root contact
Q11(b)(iv)|2|15|22|Crop rotation / polycultures
Q12(a)(i)|2|16|23|The portion of the dry matter in a feed that is digested by animals
Q12(a)(ii)|4|16|23|As the harvest date is delayed after 20 May
Q12(a)(iii)|4|16|23|The higher the DMD of the silage the higher LWG
Q12(b)(i)|2|17|23|Chemical fertiliser still present in the grass
Q12(b)(ii)|2|17|23|Low leaf : stem ratio
Q12(b)(iii)|4|17|23|Sugar provides feed for
Q12(b)(iv)|2|17|23|Add molasses or enzymes
Q13(a)(i)|8|20|24|Enabling farmers to determine grass supplies
Q13(a)(ii)|6|20|24|6 x 250 = 1500 kg DM / ha
Q13(a)(iii)|2|20|24|Italian ryegrass
Q13(a)(iv)|6|21|24|Reproductive stage
Q13(b)(i)|12|21|24|Increased grass productivity or liveweight gain or milk yield
Q13(b)(ii)|4|21|24|Two sets of seeds of equal size
Q13(b)(iii)|8|22|25|Less than 85% germinated
Q13(b)(iv)|4|22|25|Less weeds ‐ less chemical herbicides required
Q14(a)(i)|10|23|25|Laxative to clear out the digestive system
Q14(a)(ii)|2|23|25|Colostrum quality decreases (3.7%) every hour after birth
Q14(a)(iii)|3|23|25|Doesn’t contain antibodies to diseases present on the farm
Q14(a)(iv)|3|23|25|Prevent bacteria multiplying
Q14(a)(v)|4|24|25|Quality of the colostrum is very poor
Q14(b)(i)|6|24|26|A = 12 ‐ 13%
Q14(b)(ii)|8|24|26|Increased energy to support metabolism
Q14(c)(i)|9|25|26|Space sheeting or high roof
Q14(c)(ii)|5|25|26|Correct indication of arrows coming in at side
Q14(d)(i)|6|26|26|Flock 1 – medium level of eggs
Q14(d)(ii)|3|26|26|Parasites may have built up a resistance to dose
Q14(d)(iii)|5|26|27|Help to determine the need to treat (dose) animals
Q15(a)(i)|6|27|27|Flush ewes on good quality pasture or tupping dose
Q15(a)(ii)|3|27|27|Beware of bull or ram or boar or cows with calves
Q15(a)(iii)|8|27|27|Choose the sex of the calf
Q15(b)(i)|6|28|28|pH = 6.2 – 7.0
Q15(b)(ii)|3|28|28|Indicates when cow is calving and alerts farmer
Q15(b)(iii)|6|28|28|Duration of oestrus = 18 – 24 hrs
Q15(b)(iv)|6|29|28|Identify cows with high cell count (mastitis)
Q15(c)(i)|9|29|28|Ammonia or NH
Q15(c)(ii)|3|29|28|Rotating brushes – allow animals to scratch
Q16(a)(i)|9|30|28|Sward composition / rate of N application
Q16(a)(ii)|3|30|28|Increase number of cows per treatment
Q16(a)(iii)|3|30|29|as the investigation was carried out over a long period of time
Q16(b)(i)|3|30|29|Treatment 3
Q16(b)(ii)|6|31|29|Highest amount of fat and protein (A + B – C)
Q16(b)(iii)|3|31|29|Efficient use or spreading (spreader calibrated properly)
Q16(c)(i)|11|31|29|Zero grazing is not accepted
Q16(c)(ii)|12|32|29|Wash roots (remove soil)
Q17(a)(i)|9|33|30|D ‐ 6, 3, 0 (showing layers)
Q17(a)(ii)|8|33|30|Creating channels for increased drainage
Q17(a)(iii)|6|34|30|Area of pasture = 98 x 178 = 17444m
Q17(a)(iv)|3|34|30|Area was close to dung pad or higher organic matter
Q17(b)(i)|4|34|30|Continually produce offspring with higher yields
Q17(b)(ii)|6|35|30|genetic make‐up of an organism
Q17(c)(i)|8|35|30|Bazooka*
Q17(c)(ii)|6|35|30|collect pollen from anther
Q17(d)(i)|6|36|31|Gene responsible for a specific trait is identified
Q17(d)(ii)|8|36|31|Disease and pest resistant varieties would lead to increased yields
Q18(a)(i)|13|37|31|4 + 4 + 3 +2
Q18(a)(ii)|8|38|31|use renewable energy sources
Q18(b)(i)|3|38|32|Weed killer used before you see weeds to prevent them growing
Q18(b)(ii)|12|39|32|Cultural control has to be the most important part of the IMS
Q18(c)(i)|7|40|33|Cattle rearing*
Q18(c)(ii)|7|40|33|Dairy*
'''

POOLS_2022_HIGHER = {
    'Q2(a)': (4, ['A', 'B', 'C', 'D', 'E', 'F']),
    'Q10(b)': (1, ['Kale', 'Miscanthus', 'Oilseed rape (OSR)']),
    'Q10(c)': (1, ['Kale', 'Miscanthus', 'Oilseed rape (OSR)']),
    'Q13(a)(iii)': (2, ['A', 'B', 'C']),
    'Q15(a)(i)': (1, ['Ewes', 'Heifers or cows: prostaglandin after natural heats', 'Heifers or cows: two prostaglandin shots', 'Heifers or cows: progesterone (P4) device', 'Sows']),
    'Q18(a)(ii)': (1, ['Animal enterprise', 'Tillage enterprise']),
}

# 2022 Ordinary: Section A Q1-Q12 at 10 marks (any seven), Section B Q13-Q18 at 50 (any three).
ORDINARY_2022 = '''
Q1(a)|8|3|12|Slurry spreader or slurry tanker or trailing shoe or injector
Q1(b)|2|3|12|Don’t wear loose clothing around the PTO
Q2(a)(i)|6|4|12|Blackface mountain or Swaledale
Q2(a)(ii)|4|4|12|Good conformation or well‐muscled
Q2(b)(i)|4|5|12|Texel or Beltex
Q2(b)(ii)|4|5|12|good milk production / prolific
Q2(b)(iii)|2|5|12|Hybrid vigour
Q3(a)|6|6|13|turn on pH meter and calibrate using buffer solutions
Q3(b)|4|6|13|adding lime to the land
Q4(a)(i)|4|7|13|Variety of plant and animal life in a habitat
Q4(a)(ii)|4|7|13|No chemical fertiliser used
Q4(a)(iii)|2|7|13|Minimises the external cost of farming
Q4(b)|10|7|14|Indicate if the following statements are true or false
Q5(a)|2|8|14|Maintenance diet
Q5(b)|8|8|14|Protein: growth or repair
Q6(a)|2|9|14|controls specific (target) weeds
Q6(b)|4|9|14|Health hazard / carcinogenic
Q6(c)|4|9|14|Wear protective gloves (PPE)
Q7(a)(i)|3|10|15|Root hairs / thin outer wall / long length
Q7(a)(ii)|3|10|15|Nitrogen (N) / phosphorus (P)
Q7(a)(iii)|4|10|15|Symptom ‐ 2
Q7(b)(i)|6|10|16|Carbon dioxide
Q7(b)(ii)|4|10|16|waxy cuticle (prevent water loss)
Q8(a)|4|11|16|Inoculating loop
Q8(b)|1|11|16|bacteria will grow on the agar plate
Q8(c)|2|11|16|To kill any micro‐organisms on the outside of the roots
Q8(d)|3|11|16|Rhizobium
Q9(a)|4|12|16|Year = 2021*
Q9(b)|2|12|16|2013*
Q9(c)|3|12|16|42*(kg)
Q9(d)|1|12|16|3 or 3L
Q10(a)|3|13|17|squeeze silage juice into a jar
Q10(b)|4|13|17|20÷85 X 100÷1
Q10(c)|3|13|17|Samples taken at random
Q11(a)(i)|1|14|18|Roundworm or lungworm or nematode
Q11(a)(ii)|3|14|18|Dose or inject cattle (with anthelmintics)
Q11(a)(iii)|2|14|18|Rotational grazing or leader follower grazing
Q11(a)(iv)|3|14|18|less immunity
Q11(a)(v)|1|14|18|Disease that impacts livestock production
Q11(b)(i)|3|15|18|Continental breed
Q11(b)(ii)|2|15|18|Shape or muscle (distribution) of animal
Q11(b)(iii)|4|15|18|788 – 533 = 255kg
Q11(b)(iv)|1|15|18|Increased LWG (ADG)
Q12(a)|4|16|19|Soil is formed by weathering of rock
Q12(b)|6|16|19|Compare the named soil types
Q13(a)(i)|3|19|20|refers to the proportion of sand, silt and clay
Q13(a)(ii)|8|19|20|100 – 87 = 13%
Q13(a)(iii)|4|19|20|Only collecting one sample
Q13(a)(iv)|6|20|20|pour soil and water into a graduated cylinder
Q13(a)(v)|6|21|20|Eileen or sedimentation
Q13(a)(vi)|12|21|20|Padraig’s (loam)
Q13(b)(i)|4|22|21|W shape on photograph
Q13(b)(ii)|4|22|21|Soil sampler or corer / soil auger
Q13(b)(iii)|3|22|21|20 ‐ 25 samples
Q13(c)(i)|4|22|21|Optimise plant health
Q13(c)(ii)|7|22|21|Gateways / pathways / water troughs
Q14(a)|7|23|21|Reduce chance of an animal getting pneumonia
Q14(b)(i)|7|23|21|Allow pasture to recover
Q14(b)(ii)|7|23|21|Easier to handle animals
Q14(c)(i)|8|24|22|House ewes carrying same number of lambs together
Q14(c)(ii)|4|24|22|Steaming up: ewes are fed good quality silage
Q14(c)(iii)|6|24|22|Increased ovulation
Q14(c)(iv)|11|25|22|2(2+2)
Q15(a)(i)|7|26|23|Healthier animals / better animal welfare
Q15(a)(ii)|19|26|23|Zero grazing is not accepted
Q15(b)(i)|6|27|23|26* (litres / day)
Q15(b)(ii)|8|27|23|= 5720 (litres)
Q15(b)(iii)|2|27|23|This cow’s yield was lower (5720 litre)
Q15(b)(iv)|3|28|23|Give cow chance to recover body condition
Q15(b)(v)|2|28|23|60 (2 months)
Q15(b)(vi)|3|28|23|Good quality silage (75+% DMD) or kale
Q16(a)(i)|8|29|24|Month: May or June
Q16(a)(ii)|2|29|24|Shaded area between continous blue line and orange dash line
Q16(a)(iii)|2|29|24|Line graphs are used to track changes
Q16(a)(iv)|2|29|24|Grass that has been dried or fermented
Q16(b)(i)|9|30|24|Sunny / warm / windy / dry
Q16(b)(ii)|15|30|24|3(4)+3
Q16(b)(iii)|4|30|24|18 (%)
Q16(c)(i)|6|31|24|A = Ragwort
Q16(c)(ii)|2|31|24|Noxious plant (harmful to animals)
Q16(d)(i)|6|31|24|C = Thistle
Q16(d)(ii)|2|31|24|Animal feed / human consumption
Q17(a)(i)|6|32|25|Better use of chemicals
Q17(a)(ii)|6|32|25|Reduced labour or easier to use
Q17(a)(iii)|6|32|25|Lack of practical knowledge
Q17(b)(i)|8|33|25|40 X 57
Q17(b)(ii)|6|33|25|2990 + 1056 + 2280 + 57 + 65
Q17(b)(iii)|6|33|25|6992 x 5% = 349.6 (kg)
Q17(b)(iv)|6|34|25|Less chance of N leaching into rivers
Q17(c)|6|34|25|Install windmills
Q18(a)(i)|12|35|26|Heading date / total yield
Q18(a)(ii)|5|35|26|Moyola (105 ton DM/ha)
Q18(a)(iii)|5|35|26|Moyola (107 ton DM/ha)
Q18(b)(i)|6|35|26|Spray with total herbicide
Q18(b)(ii)|2|36|26|Min 85% germination rate
Q18(c)(i)|12|36|26|C ‐ already given
Q18(c)(ii)|4|36|26|Contain more nutrients
Q18(c)(iii)|4|36|26|May cause allergic reactions
'''

POOLS_2022_ORDINARY = {
    'Q2(a)(i)': (3, ['A', 'B', 'C', 'D']),
    'Q2(b)(ii)': (1, ['E', 'F']),
    'Q3(a)': (1, ['pH paper or universal indicator', 'pH meter']),
    'Q7(a)(iii)': (1, ['Nitrogen', 'Phosphorus', 'Potassium', 'Sulphur', 'Calcium', 'Magnesium']),
    'Q12(a)': (3, ['Parent material', 'Topography', 'Time', 'Climate', 'Organisms']),
}

# 2021 Higher: Section A Q1-Q12 at 10 marks (any seven), Section B Q13-Q18 at 50 (any three).
# Q13(a)(iii) keeps its name (4) and advantages (4+2) boundaries; Q14(a) and Q18(a)
# are priced by printed heading (4+2 and 2(2)), one task per heading.
HIGHER_2021 = '''
Q1(a)|6|3|11|Buttercup
Q1(b)|4|3|11|Definition of one of annual or biennial for 2
Q2(a)(i)|2|4|11|does not kill the (targeted) plant
Q2(a)(ii)|4|4|11|minimum cultivation does not disturb dormant seeds
Q2(a)(iii)|4|4|11|Decreased yield (or food production)
Q2(b)(i)|2|5|12|travel up the compacted soil further
Q2(b)(ii)|6|5|12|Put cotton wool or muslin cloth
Q2(b)(iii)|2|5|12|Record the exact mass
Q3(a)(i)|4|6|12|Beware of bull
Q3(a)(ii)|4|6|12|castrating male animals
Q3(a)(iii)|2|6|12|Castrate male animals on the farm
Q3(b)(i)|4|7|13|Seed drill
Q3(b)(ii)|2|7|13|Decreased compaction
Q3(b)(iii)|2|7|13|Reduces water run
Q3(b)(iv)|2|7|13|Stressed animals
Q4(a)|2|8|13|Solar panels
Q4(b)|4|8|13|Sheds are situated close together
Q4(c)|4|8|13|Plant more trees or hedges
Q5(a)|4|9|14|protection of soil structure against soil erosion
Q5(b)|2|9|14|Flea beetle eats holes
Q5(c)|4|9|15|Germination
Q6(a)(i)|2|10|15|Mitochondria*
Q6(a)(ii)|4|10|15|Subsoiler or plough or harrow
Q6(a)(iii)|4|10|15|soil compaction destroys soil aggregates
Q6(b)(i)|2|11|15|Animals eat plants
Q6(b)(ii)|4|11|15|decreased organic matter
Q6(b)(iii)|4|11|15|Grow perennial pasture
Q7(a)|2|12|16|Variety of plant and animal life
Q7(b)|2|12|16|Soil or water conservation
Q7(c)|6|12|16|Leave (whitethorn) tree in hedges
Q8(a)|2|13|16|Shape and muscle distribution
Q8(b)|4|13|16|367 x 415
Q8(c)|4|13|16|Heifer ‐ LM
Q9(a)|2|14|17|selected based on their DNA
Q9(b)|4|14|17|Increased animal performance
Q9(c)|2|14|17|Farmer identifies trait
Q9(d)|2|14|17|Better hygiene or management
Q10(a)|4|15|17|small specialised market
Q10(b)|4|15|17|Ireland has large quantities of grass
Q10(c)|2|15|17|84% water
Q11(a)(i)|4|16|18|21 days
Q11(a)(ii)|2|16|18|Ovary*
Q11(a)(iii)|4|16|18|Increased choice of genetically superior sires
Q11(b)(i)|4|17|18|4 stomach chambers
Q11(b)(ii)|6|17|19|gas build up in rumen
Q12(a)|2|18|19|Anaemia*
Q12(b)|2|18|19|Lack of iron
Q12(c)|2|18|19|Iron injection
Q12(d)|4|18|19|Closed herd
Q13(a)(i)|4|22|20|clover or legumes
Q13(a)(ii)|6|22|20|Rotation grazing or named rotational grazing system
Q13(a)(iii) Name|4|22|20|Rotational or paddock grazing system
Q13(a)(iii) Advantages|6|22|20|Gives the sward time to recover
Q13(a)(iv)|8|23|20|By using multi
Q13(a)(v)|16|24|21|Quadrat
Q13(b)|6|25|21|converts nitrite ions
Q13(c)|6|25|21|Chemical use
Q14(a) Housing|6|26|22|Housing
Q14(a) Nutrition|6|26|22|Nutrition
Q14(a) Production targets|6|26|22|Production Targets
Q14(b)(i)|4|27|25|Suffolk
Q14(b)(ii)|6|27|25|Landrace
Q14(b)(iii)|6|27|26|Housing or freedom from discomfort
Q14(c)(i)|3|29|26|Liver score
Q14(c)(ii)|3|29|27|Lung score
Q14(c)(iii)|4|29|27|There is a lot of liver damage
Q14(c)(iv)|6|30|27|Farmer should get fluke tested
Q15(a)(i)|3|31|28|Applying organic fertiliser in autumn
Q15(a)(ii)|6|31|28|application rates and source of organic fertiliser
Q15(a)(iii)|8|31|28|Trailing shoe or shallow injection
Q15(a)(iv)|12|32|28|Cut a number of grass samples
Q15(a)(v)|3|32|28|Electronic balance not calibrated
Q15(b)(i)|3|33|29|FYM ‐ High
Q15(b)(ii)|5|33|29|Solution 1
Q15(b)(iii)|4|34|29|Advice would be for farmers to put high levels of FYM
Q15(b)(iv)|6|34|29|Applying FYM provides more DM
Q16(a)(i)|6|35|30|9316 + 6830
Q16(a)(ii)|6|35|30|Breeding high EBI cows
Q16(a)(iii)|9|36|30|Reducing TBC
Q16(b)|12|37|31|Place equal amounts of one milk sample
Q16(c)(i)|3|38|32|Low emission slurry spreading
Q16(c)(ii)|2|38|32|unique selling points
Q16(c)(iii)|4|38|32|Creamy yellow butter
Q16(c)(iv)|8|38|32|Quality assurance scheme
Q16(d)(i)|6|39|33|Lower fencing cost
Q16(d)(ii)|4|39|33|Animals can become stressed
Q16(d)(iii)|4|39|33|Rotational grazing (21 day)
Q16(d)(iv)|3|39|33|Wear gloves and mask
Q17(a)|6|40|33|W shape
Q17(b)(i)|3|41|33|both answers must be correct for 3 marks
Q17(b)(ii)|3|41|33|Mainly used for silage production
Q17(b)(iii)|6|41|34|Farmer needs to add 5 ton
Q17(b)(iv)|8|42|34|Calcium
Q17(b)(v)|6|42|34|Spreading slurry
Q17(b)(vi)|6|42|34|Create buffer or riparian zones
Q17(c)|12|43|34|potassium chloride
Q18(a) Soil quality|4|44|35|Drainage and aeration
Q18(a) Crop preservation|4|44|35|Crops should have certain moisture content
Q18(b)|9|44|36|Have to use some of her tillage land
Q18(c)(i)|4|45|37|Period of time when cow is not producing milk
Q18(c)(ii)|4|45|37|Daily requirement of a cow
Q18(c)(iii)|6|46|37|Feeding concentrates
Q18(c)(iv)|4|46|37|reproductive cycle may not have started
Q18(c)(v)|6|46|37|grass only diet
Q18(c)(vi)|4|46|37|305 days
Q18(c)(vii)|5|46|37|Observation
'''
CROPS_2021 = ['Kale or stubble turnips', 'Oilseed rape (OSR)', 'Miscanthus']
SYSTEMS_2021 = ['Liquid milk v creamery milk', 'Calf to beef v suckler beef', 'Mid-season lamb v early lamb']
POOLS_2021_HIGHER = {
    'Q5(a)': (1, CROPS_2021), 'Q5(b)': (1, CROPS_2021), 'Q5(c)': (1, CROPS_2021),
    'Q11(b)(ii)': (1, ['Bloat', 'Acidosis']),
    'Q14(a) Housing': (1, SYSTEMS_2021), 'Q14(a) Nutrition': (1, SYSTEMS_2021), 'Q14(a) Production targets': (1, SYSTEMS_2021),
    'Q14(b)(ii)': (1, ['Pig', 'Poultry', 'Horse']),
    'Q15(b)(ii)': (1, ["Solution 1: each treatment's own November value", 'Solution 2: the November control value for both']),
    'Q16(b)': (1, ['Resazurin test', 'Total bacterial count']),
    'Q18(a) Crop preservation': (1, ['Grain crops (e.g. barley)', 'Potatoes', 'Grass (silage or hay)']),
}
# 2021 Ordinary: Section A Q1-Q12 at 10 marks (any seven), Section B Q13-Q18 at 50 (any three).
# Q1(a)(i)-(iii) and Q6(a)-(e) are one task each under one instruction; Q15(b) and
# Q18(a)(i) are priced by printed heading. Q18(a)(i) carries "Named crop 2" on its
# Seedbed preparation task, which is what makes Question 18 total 50.
ORDINARY_2021 = '''
Q1(a)|6|3|11|Oilseed rape*
Q1(a)(iv)|4|3|11|Biennial – (complete lifecycle) grows in 2 years
Q1(b)(i)|8|4|11|A = Daisy
Q1(b)(ii)|2|4|11|crop rotation to disturb (break) weed cycle
Q2(a)|6|5|11|A = Rumen
Q2(b)|4|5|11|Breakdown food or cellulose or roughage or fibre
Q3(a)(i)|2|6|11|Growth of crops in a defined sequence
Q3(a)(ii)|4|6|11|Manage soil fertility
Q3(a)(iii)|4|6|11|Toxic (harmful to human health)
Q3(b)(i)|2|6|12|Control of a pest by introduction of natural enemy or predator
Q3(b)(ii)|4|6|12|Ladybird (eat) greenfly
Q3(b)(iii)|4|6|12|No chemicals used
Q4(a)|4|7|12|A = Brown earth
Q4(b)|2|7|12|grazing pasture (grassland)
Q4(c)|4|7|12|Poor drainage (due to the impermeable iron pan)
Q5(a)|2|8|12|Infiltration rate or drainage or soil (structure)
Q5(b)|4|8|12|Use (same amount of) soil for each
Q5(c)|2|8|12|Uncompacted soil
Q5(d)|2|8|12|Ploughing
Q6(a)–(e)|10|9|13|Twin lamb disease
Q7(a)|2|9|13|Indicate whether True or False
Q7(b)|2|9|13|(b) False
Q7(c)|2|9|13|(c) True
Q7(d)|2|9|13|(d) True
Q7(e)|2|9|13|(e) True
Q8(a)(i)|2|10|13|Prevent children or animal accessing them
Q8(a)(ii)|2|10|13|Danger overhead power lines
Q8(a)(iii)|4|10|13|respirator or mask
Q8(a)(iv)|2|10|13|Wear gloves or wash hands afterwards
Q8(b)(i)|2|11|13|Caution farm machinery
Q8(b)(ii)|2|11|13|Have a clear exit plan
Q8(b)(iii)|6|11|13|Remove all animals from the shed
Q9(a)|2|12|14|(highest ranking) or most or top
Q9(b)|4|12|14|Animal (respiration)
Q9(c)|4|12|14|Leave tree in hedges
Q10(a)|2|13|14|Ovary*
Q10(b)|2|13|14|(Produces) eggs or ovulation
Q10(c)|4|13|14|Gestation length
Q10(d)|2|13|14|X on the diagram (must reach cervix)
Q11(a)(i)|2|14|15|Silage (pit)
Q11(a)(ii)|4|14|15|Environmental hazard
Q11(a)(iii)|2|14|15|Buildings (structures) are close together
Q11(a)(iv)|2|14|15|Automatic calf feeder
Q11(b)(i)|2|15|15|If animal (cow) is sick or injured
Q11(b)(ii)|2|15|15|Disinfect or clean boots
Q11(b)(iii)|2|15|15|less labour needed
Q11(b)(iv)|4|15|15|passage behind cubicles
Q12(a)|8|16|16|A = Charolais*
Q12(b)|2|16|16|0m for naming breed
Q13(a)(i)|4|19|17|90 million*
Q13(a)(ii)|4|19|17|Waterlogged or wet (poorly drained) areas or excess water
Q13(a)(iii)|5|19|17|Fence off wet areas
Q13(b)(i)|4|20|17|Louth*
Q13(b)(ii)|4|20|17|lower incidence of mud snail
Q13(c)(i)|3|20|17|Disease that must be reported
Q13(c)(ii)|8|20|17|Foot and Mouth
Q13(c)(iii)|3|20|17|may pose threat to humans or zoonosis
Q13(c)(iv)|5|21|17|Operate closed herd (breed own replacements)
Q13(c)(v)|10|21|17|lime on floor
Q14(a)(i)|8|22|18|Holstein Friesian
Q14(a)(ii)|10|22|18|Wash udders
Q14(a)(iii)|7|22|18|thermoduric bacteria
Q14(a)(iv)|7|22|18|use genomic bulls
Q14(b)(i)|3|23|18|same amount of Resazurin
Q14(b)(ii)|9|23|18|Diagram or text showing the following
Q14(b)(iii)|3|24|18|Wrong temperature on water bath
Q14(b)(iv)|3|24|18|colour change not measured numerically
Q15(a)(i)|6|25|19|hybrid rye grass
Q15(a)(ii)|4|25|19|Good yield or fast growing
Q15(a)(iii)|6|25|19|Vegetative stage or leafy stage
Q15(b) Time of year of cutting|4|25|19|Time of cutting
Q15(b) Fertiliser requirements|4|25|19|soil test for nutrient requirement
Q15(b) Harvesting and storage|10|25|19|do not cut during or after rainfall
Q15(c)(i)|4|26|19|29.83%
Q15(c)(ii)|4|26|19|DMD not high enough (67%)
Q15(c)(iii)|6|26|19|Cut at leafy stage to increase sugar for fermentation
Q15(c)(iv)|2|26|19|Lactobacillus or valid named species
Q16(a)|16|27|20|Clay is more fertile (than sandy soil)
Q16(b)(i)|5|27|20|Sowing cover crops
Q16(b)(ii)|6|27|20|Divide the area
Q16(c)(i)|7|28|21|Mix soil sample with (distilled) water
Q16(c)(ii)|5|28|21|Low earthworm numbers
Q16(c)(iii)|3|28|21|58.33%
Q16(c)(iv)|4|28|21|Soil is very wet
Q16(c)(v)|4|28|21|Compaction or poaching
Q16(d)(i)|8|29|21|No GMO
Q16(d)(ii)|7|29|21|Animals reared on land free from chemicals
Q16(d)(iii)|8|29|21|use sheep on land to increase N content through dung
Q17(a)(i)|7|30|22|growth of (plant from) seed
Q17(a)(ii)|4|30|22|By increasing the temperature of the soil
Q17(a)(iii)|7|30|22|Amount or type of seeds
Q17(a)(iv)|3|30|22|if sown too deep
Q17(a)(v)|3|31|22|62+59+61+58
Q17(a)(vi)|3|31|22|To get more accurate results
Q17(a)(vii)|6|31|22|overheat switch on incubator
Q17(b)(i)|6|32|22|Correct bar drawn at 20
Q17(b)(ii)|3|32|22|will give best germination rates
Q17(b)(iii)|8|32|22|water the seeds
Q18(a)(i) Seedbed preparation|9|33|23|Named crop
Q18(a)(i) Weed control|4|33|23|Herbicide or weed killer
Q18(a)(ii)|4|33|23|Beware of machinery
Q18(a)(iii)|6|33|23|Accurate or even spreading
Q18(b)(i)|2|34|23|Process through which populations of living organisms adapt
Q18(b)(ii)|4|34|23|performance or progeny tested bull
Q18(b)(iii)|4|34|23|good conformation (double muscle gene)
Q18(c)(i)|4|35|24|0.42kg / day
Q18(c)(ii)|4|35|24|can be indicated on the graph
Q18(c)(iii)|4|36|24|Lambs are putting weight on in a consistent manner
Q18(c)(iv)|5|36|24|milk (milk replacer)
Q18(d)(i)|1|37|24|More accurate results or more fair result
Q18(d)(ii)|2|37|24|All nutrients (NPK)
Q18(d)(iii)|2|37|24|Cut shoot at base of plant
Q18(d)(iv)|12|38|24|dung stead or manure pit
'''
POOLS_2021_ORDINARY = {
    'Q12(b)': (1, ['Landrace', 'Large White', 'Rhode Island Red', 'Irish Sport Horse']),
    'Q14(b)(iii)': (1, ['Water bath temperature', 'Amount of Resazurin or milk', 'Dirty test tubes or containers', 'Observation of time']),
    'Q14(b)(iv)': (1, ['Qualitative (resazurin test)', 'Quantitative (total bacterial count)']),
    'Q16(c)(v)': (1, ['Compaction or poaching', 'Late or failed germination or lower yields', 'Higher incidence of disease']),
    'Q18(b)(iii)': (1, ['Good conformation', 'Polled (no horns)', 'Smaller calves']),
}
# 2020 Higher (legacy syllabus): Q1 six of ten parts at 10, Q2-Q9 any five more at 48;
# Q4 two of four methods, Q8 two of three parts, Q9 four of five explanations.
HIGHER_2020 = '''
Q1(a)(i)|6|2|3|Physical or economic damage
Q1(a)(ii)|4|2|3|Ragwort/ (creeping) thistle
Q1(b)(i)|6|2|3|Egg-nymph-adult
Q1(b)(ii)|4|2|3|Aphid/ dragonfly/ cockroach
Q1(c)|10|2|3|Poorest trees removed
Q1(d)|10|2|3|Vascular cylinder (stele) and xylem and phloem
Q1(e)|10|2|3|Location of humerus
Q1(f)|10|2|3|Dagging: Cutting away
Q1(g)|10|2|3|Long stamens/ stamens outside flower
Q1(h)|10|2|3|280 ‒ 288 days
Q1(i)|10|2|3|Slate: Metamorphic
Q1(j)|10|2|3|Hard testa (coat) or rolling breaks coat
Q2(a)(i)|4|3|4|Cementation: (Soil) particles pushed together
Q2(a)(ii)|8|3|4|(Small) root activity
Q2(a)(iii)|8|3|4|Freeze-thaw action
Q2(b)(i)|4|3|4|Measure (allow quantity)
Q2(b)(ii)|4|3|4|Sand particles chemically inert
Q2(b)(iii)|4|3|4|Add organic matter (or example)
Q2(c)|16|3|4|Matching reagent
Q3 Option One (a)|16|4|5|Mountain sheep production
Q3 Option One (b)|16|4|5|One selection point based on
Q3 Option One (c)|16|4|5|Bolus: stomach worms
Q3 Option Two (a)(i)|8|4|6|Climate or rainfall or sunshine or temperature
Q3 Option Two (a)(ii)|8|4|6|Sown in September or October
Q3 Option Two (b)(i)|4|4|6|Stone free/ pH 5.5
Q3 Option Two (b)(ii)|4|4|6|Maincrop/ first earlies
Q3 Option Two (b)(iii)|4|4|6|30 ‒ 40 tonne
Q3 Option Two (b)(iv)|4|4|6|Animal feed/ human consumption/ seed potatoes
Q3 Option Two (c)|16|4|6|Herbicide + description
Q4(a)|24|5|7|Grind grass/ in alcohol
Q4(b)|24|5|7|Liver contains catalase
Q4(c)|24|5|7|Two dry soil samples
Q4(d)|24|5|7|Named root crop
Q5(a)(i)|8|5|8|Allows repair of udder tissue
Q5(a)(ii)|8|5|8|Body condition score assessed
Q5(b)(i)|8|5|8|Tail painting or pressure-sensitive paint tag
Q5(b)(ii)|8|5|8|Greater choice of breeds
Q5(c)|16|5|8|Total bacterial count (TBC)
Q6(a)(i)|4|6|9|Ploughing/ harrowing or rotavating/ rolling
Q6(a)(ii)|6|6|9|Seed drill/ seeds and fertiliser
Q6(a)(iii)|6|6|9|Improves structure/ improves aeration
Q6(b)(i)|8|6|9|Maximum grass utilisation
Q6(b)(ii)|8|6|9|Monoculture or loss of biodiversity
Q6(c)|16|6|9|Dehydration or drying
Q7(a)|14|6|10|Prophase—metaphase—anaphase—telophase
Q7(b)(i)|8|6|10|Halves (or reduces) diploid number
Q7(b)(ii)|8|6|10|Homologous chromosomes
Q7(c)(i)|10|6|10|Parental gametes
Q7(c)(ii)|8|6|10|Hairless leaf with spiral petiole
Q8(a)(i)|16|7|11|Carbon cycle
Q8(a)(ii)|8|7|11|Reduction in national cattle herd
Q8(b)(i)|8|7|11|Mastitis/ blackleg/ footrot
Q8(b)(ii)|12|7|11|Overuse of antibiotics/ mutation
Q8(b)(iii)|4|7|11|Milking out or hygiene or vaccination
Q8(c)|24|7|11|Four-chambered stomach
Q9(a)|12|7|12|Exposing potato tubers to light
Q9(b)|12|7|12|Fowl have no teeth
Q9(c)|12|7|12|Cranefly/ active in autumn
Q9(d)|12|7|12|Iron pan/ hard or impermeable layer
Q9(e)|12|7|12|Increased concentrates diet
'''
POOLS_2020_HIGHER = {
    'Q4(b)': (1, ['Catalase', 'Amylase']),
}
# 2020 Ordinary (legacy syllabus): Section One six of Q1-Q7 at 20; Section Two three of Q8-Q13
# at 60, Q13 any two of (a)-(d) at 30. A scale the scheme prints across several parts
# ("4 + 8(2)") is one task over its span.
ORDINARY_2020 = '''
Q1(a)|4|2|3|The % sand, silt and clay
Q1(b)|12|2|3|Finding soil texture:
Q1(c)|4|2|3|Reason for any one step above:
Q2|20|3|4|First milk a young mammal
Q3|20|3|4|Stomata are pores found on the leaves of plants
Q4|20|4|5|Slurry agitator
Q5|20|5|5|Sources of pollution:
Q6|20|5|6|Parts of stomach:
Q7(a)|4|6|6|Vaccination of farm animals:
Q7(b)|4|6|6|Using footbaths:
Q7(c)|4|6|6|Growing certified seed potatoes:
Q7(d)|4|6|6|Subsoiling:
Q7(e)|4|6|6|Maintaining hedgerows:
Q8(a)(i)|9|7|7|Paddock grazing system:
Q8(a)(ii)|12|7|7|Disadvantages
Q8(b)(i)|15|7|7|Steps in making good quality hay
Q8(b)(ii)|12|7|8|A reason for each listed step in silage making:
Q8(c)|12|7|8|Simple on-site silage test:
Q9(a)(i)|3|8|9|Element in ground limestone:
Q9(a)(ii)|5|8|9|How a soil becomes acidic:
Q9(a)(iii)|12|8|9|Finding pH of a soil sample
Q9(b)(i)|12|8|9|The three principal elements in 10-10-20:
Q9(b)(ii)|4|8|9|Function of one of the nutrient elements in 10-10-20:
Q9(c)(i)|8|8|10|How FYM and slurry stored:
Q9(c)(ii)|8|8|10|Differences between composition of FYM and of slurry:
Q9(c)(iii)|8|8|10|Precautions when agitating slurry:
Q10(a)(i)|4|9|11|How many chromosomes in cattle gametes:
Q10(a)(ii)|4|9|11|Organ in which female games produced:
Q10(a)(iii)|4|9|11|Type of cell division that produces gametes:
Q10(b)|16|9|11|Cross 1:
Q10(c)|24|9|11|Cross 2:
Q10(d)(i)|4|9|11|Cross breeding:
Q10(d)(ii)|4|9|11|An advantage of cross breeding:
Q11(a)(i)|8|10|12|Dairy breeds:
Q11(a)(ii)|4|10|12|Why suitable for dairy:
Q11(a)(iii)|8|10|12|Why dairy cows culled:
Q11(b)(i)|8|10|12|Characteristics of replacement heifers:
Q11(b)(ii)|4|10|12|Heifer age at first calving:
Q11(b)(iii)|4|10|12|Target weight at first calving:
Q11(b)(iv)|8|10|12|Signs that indicate calving imminent
Q11(c)|16|10|13|Body condition scoring:
Q12(a)|20|11|14|Leaf adaptations for photosynthesis:
Q12(b)|20|11|14|Excretion:
Q12(c)|20|11|14|Parts of flower:
Q13(a)|30|12|15|Factors affecting soil temperature:
Q13(b)|30|12|15|Barley:
Q13(c)|30|12|16|Management of lowland lambs:
Q13(d)(i)|4|12|16|Functions of dietary protein:
Q13(d)(ii)|12|12|16|Protein test:
Q13(d)(iii)|8|12|16|Bulky feeds v concentrates:
Q13(d)(iv)|3|12|16|Maintenance ration:
Q13(d)(v)|3|12|16|Production ration:
'''
POOLS_2020_ORDINARY = {
    'Q1(b)': (1, ['Sieve method', 'Feel method', 'Sedimentation method']),
    'Q8(c)': (1, ['Colour of silage', 'Smell of silage', 'Squeeze silage (or dry matter or DM test)', 'pH of silage', 'Taste of silage', 'Feel of silage']),
    'Q9(a)(iii)': (1, ['Universal indicator', 'pH meter']),
    'Q9(b)(ii)': (1, ['Nitrogen', 'Phosphorus', 'Potassium']),
    'Q13(b)': (1, ['Winter barley', 'Spring barley']),
}
# The Ordinary question whose lettered parts are a printed any-two choice.
OL_PART_CHOICE = {2012: 'Q12', 2013: 'Q13', 2014: 'Q13', 2015: 'Q13', 2016: 'Q13', 2017: 'Q13', 2018: 'Q13', 2019: 'Q13', 2020: 'Q13'}
# 2019 Higher (legacy syllabus), transcribed from the SEC paper and scheme.
HIGHER_2019 = '''
Q1(a)|10|2|5|Target yields in tonnes per hectare of
Q1(b)|10|2|5|Why dense planting in Irish forests:
Q1(c)|10|2|5|Vegetative reproduction:
Q1(d)|10|2|5|Characteristics of loam:
Q1(e)|10|2|5|Zoonosis: Disease that can be transmitted from animals to humans
Q1(f)|10|2|5|Test for nitrates: Diphenylamine
Q1(g)|10|2|5|Functions of the liver:
Q1(h)(i)|6|2|5|Biological control: Control of pests by predators
Q1(h)(ii)|4|2|5|Rodent or named by cat or dog
Q1(i)|10|2|5|Location of nephron: Kidney
Q1(j)|10|2|5|Value of sheep dipping and pour-on:
Q2(a)(i)|6|3|6|Moisture stress:
Q2(a)(ii)|9|3|6|Available water capacity:
Q2(b)(i)|12|3|6|Causes of increasing soil acidity over time:
Q2(b)(ii)|6|3|6|Detail for any one answer from (i):
Q2(c)|15|3|6|To show flocculation:
Q3 Option One (a)(i)|4|4|7|Breeds used to produce cross-breed sucklers:
Q3 Option One (a)(ii)|6|4|7|Benefits of cross-breeds:
Q3 Option One (a)(iii)|6|4|7|Reproductive efficiency:
Q3 Option One (b)(i)|4|4|7|Comparing calf growth rates
Q3 Option One (b)(ii)|12|4|7|Grazing management:
Q3 Option One (c)|16|4|8|Comparing beef production systems
Q3 Option Two (a)(i)|4|4|8|Photosynthesis equation:
Q3 Option Two (a)(ii)|12|4|8|How leaf structure suited to photosynthesis:
Q3 Option Two (b)|16|4|8|How photosynthesis and microorganism activity affect silage feeding value:
Q3 Option Two (c)|16|4|8|Positive effects of microorganisms:
Q4(a)|24|5|9|Effect of a mineral deficiency on crop growth:
Q4(b)|24|5|9|Percentage water and solids in milk:
Q4(c)|24|5|9|Presence of microorganisms in clover roots:
Q4(d)|24|5|9|Digestibility of silage:
Q5(a)(i)|4|5|10|Soil preparation:
Q5(a)(ii)|4|5|10|Planting:
Q5(a)(iii)|4|5|10|Weed control:
Q5(a)(iv)|4|5|10|Harvesting:
Q5(b)(i)|4|5|10|Catch crops:
Q5(b)(ii)|6|5|10|Rotation with catch crop:
Q5(b)(iii)|6|5|10|Catch crop benefits other than fodder:
Q5(c)(i)|4|5|10|Situations in which to use broad-spectrum weedkillers:
Q5(c)(ii)|12|5|10|Precautions when using sprays:
Q6(a)(i)|4|6|11|Causes of soil compaction:
Q6(a)(ii)|8|6|11|Effects of soil compaction:
Q6(a)(iii)|3|6|11|Remedy for soil compaction:
Q6(b)(i)|9|6|11|Benefits of clover:
Q6(b)(ii)|12|6|11|Why different clovers in different seed mixtures
Q6(c)|12|6|11|Comparing slurry and FYM
Q7(a)(i)|4|6|12|Pedigree herd: All animals descended from a purebreeding line
Q7(a)(ii)|4|6|12|Recessive allele:
Q7(a)(iii)|4|6|12|Natural service:
Q7(a)(iv)|4|6|12|Independent assortment:
Q7(b)|16|6|12|Parental genotype: WwFf
Q7(c)(i)|8|6|12|Why Drosophila used:
Q7(c)(ii)|8|6|12|Lambing percentage:
Q8(a)|24|7|13|Liver fluke life cycle
Q8(b)(i)|12|7|13|Diagram of TS of dicot stem
Q8(b)(ii)|12|7|13|Differences between monocot and dicot stem TSs:
Q8(c)|24|7|13|Distinguish between the members of any three of the pairs
Q9(a)|12|7|14|Change in grass digestibility:
Q9(b)|12|7|14|Culling older dairy cows:
Q9(c)|12|7|14|Low rate of establishment in wet spring:
Q9(d)|12|7|14|Hedgerow conservation:
Q9(e)|12|7|14|Flushing ewes:
'''
POOLS_2019_HIGHER = {'Q2(b)(ii)': (1, ['Rainfall', 'Acid rain', 'Crop production', 'Animal urine', 'Leaching', 'Some fertilisers', 'Cation exchange', 'Manures', 'Pine needles', 'Waterlogging']), 'Q3 Option One (b)(ii)': (1, ['Paddock grazing', 'Strip grazing', 'Block grazing', 'Set stocking', 'Zero grazing', 'Leader-follower', 'Creep grazing', 'Mixed grazing']), 'Q4(a)': (1, ['Flask method', 'Soil method'])}
# 2019 Ordinary (legacy syllabus), transcribed from the SEC paper and scheme.
ORDINARY_2019 = '''
Q1|20|2|5|Beneficial effects of earthworms:
Q2|20|3|5|Shaking out grass (to allow it to dry)
Q3|20|4|5|A gilt is a young female pig:
Q4|20|4|6|Cow with a high butterfat content in milk:
Q5|20|5|6|When cereal A ready for harvest:
Q6(a)|4|6|6|Spraying potatoes with fungicide:
Q6(b)|4|6|6|Housing beef animals in winter:
Q6(c)|4|6|6|Paring sheep’s hooves:
Q6(d)|4|6|6|Agitating slurry:
Q6(e)|4|6|6|Planting shelter belts:
Q7|20|7|7|Clover family:
Q8(a)(i)|8|8|8|Pig housing features:
Q8(a)(ii)|4|8|8|Importance of any feature given in (i):
Q8(a)(iii)|8|8|8|Why farrowing crate:
Q8(b)(i)|4|8|8|Length of gestation for sow:
Q8(b)(ii)|4|8|8|Average litter size:
Q8(b)(iii)|12|8|8|Why iron injection:
Q8(c)|20|8|8|Hill (mountain) sheep production
Q9(a)(i)|6|9|9|Reasons for reseeding grassland:
Q9(a)(ii)|6|9|9|Species commonly used:
Q9(a)(iii)|3|9|9|Reason for any one from (ii):
Q9(a)(iv)|6|9|9|Why grassland topped:
Q9(b)(i)|12|9|9|Making pit silage:
Q9(b)(ii)|6|9|9|Importance of above steps:
Q9(b)(iii)|3|9|9|Dry matter digestibility
Q9(b)(iv)|3|9|9|DMD of good silage:
Q9(c)|15|9|10|Catch crop:
Q10(a)|10|10|10|In-breeding:
Q10(b)|16|10|10|Cross 1
Q10(c)|22|10|10|Cross 2
Q10(d)(i)|6|10|10|Advantages of AI:
Q10(d)(ii)|6|10|10|Disadvantages of AI:
Q11(a)(i)|12|11|11|Sedimentary:
Q11(a)(ii)|4|11|11|Weathering:
Q11(a)(iii)|8|11|11|How weathered:
Q11(b)|16|11|11|How the soil feels:
Q11(c)(i)|8|11|11|Why organic matter important in soil:
Q11(c)(ii)|8|11|11|How OM added to soil:
Q11(c)(iii)|4|11|11|Why plants survive better in clay than in sandy soils in drought:
Q12(a)(i)|6|12|12|Care at birth:
Q12(a)(ii)|6|12|12|Changes in diet:
Q12(a)(iii)|6|12|12|Housing:
Q12(a)(iv)|6|12|12|Disease control:
Q12(b)(i)|9|12|12|Cause of mastitis:
Q12(b)(ii)|3|12|12|Another reason why milking parlour hygiene important:
Q12(b)(iii)|9|12|12|How hygiene maintained:
Q12(c)|15|12|12|To compare hygiene quality of two milk samples:
Q13(a)|30|13|13|Maincrop potato varieties:
Q13(b)|30|13|13|Pulmonary artery
Q13(c)(i)|10|13|13|Why mainly conifers in Irish plantations:
Q13(c)(ii)|5|13|13|Common Irish conifer:
Q13(c)(iii)|5|13|13|Why thinning:
Q13(c)(iv)|10|13|13|Beneficial effects of forestry:
Q13(d)|30|13|14|Transpiration:
'''
POOLS_2019_ORDINARY = {'Q8(c)': (1, ['Hill (mountain) sheep production', 'Lowland sheep production']), 'Q11(b)': (1, ['Sandy soil', 'Clay soil']), 'Q12(c)': (1, ['Resazurin test', 'Agar plates']), 'Q13(d)': (1, ['Plastic bag', 'Potometer', 'Coloured dye'])}
# 2018 Higher (legacy syllabus), transcribed from the SEC paper and scheme.
HIGHER_2018 = '''
Q1(a)|10|2|5|Livestock unit:
Q1(b)|10|2|5|Diagram of wind pollinated flower
Q1(c)|10|2|5|Thyroid location:
Q1(d)|10|2|5|Factors affecting FCR in pigs:
Q1(e)|10|2|5|Function of plant cell types
Q1(f)|10|2|5|Functions in avian digestive system
Q1(g)|10|2|5|Gestation period in days
Q1(h)|10|2|5|Diagram of cow’s reproductive system:
Q1(i)|10|2|5|Qualities of wool as a material:
Q1(j)|10|2|5|Why hedgerow conservation encouraged:
Q2(a)(i)|10|3|6|Soil type: Name of soil type
Q2(a)(ii)|6|3|6|Factors responsible for creating soil horizons:
Q2(b)(i)|4|3|6|Soil texture: Relative proportions
Q2(b)(ii)|16|3|6|Comparing soil texture types:
Q2(c)|12|3|6|Experiment to show earthworm activity in soil:
Q3 Option One (a)(i)|4|4|7|BCS:
Q3 Option One (a)(ii)|6|4|7|At calving: BCS 3.0
Q3 Option One (a)(iii)|6|4|7|BCS high: calving difficulty
Q3 Option One (b)(i)|4|4|7|Bacterial diseases of dairy cows:
Q3 Option One (b)(ii)|4|4|7|Deficiency disorders of dairy cows:
Q3 Option One (b)(iii)|8|4|7|Preventative measures:
Q3 Option One (c)(i)|12|4|7|Changes in beef calf diet, from birth to weaning:
Q3 Option One (c)(ii)|4|4|7|How changes affect ruminant stomach development:
Q3 Option Two (a)|16|4|8|Name of fungus: Phytophthora infestans
Q3 Option Two (b)|16|4|8|Cultivation of a named cereal
Q3 Option Two (c)(i)|4|4|8|Indirect control of weeds:
Q3 Option Two (c)(ii)|12|4|8|Examples of indirect control:
Q4(a)|24|5|9|Percentage sugar in grass:
Q4(b)|24|5|9|Effect of shading on crop growth:
Q4(c)|24|5|9|Enzyme action:
Q4(d)|24|5|9|Botanical composition comparison:
Q5(a)|16|5|10|Hill v. lowland sheep production:
Q5(b)|16|5|10|Management practices at lambing:
Q5(c)|16|5|10|Sheep Welfare Scheme features
Q6(a)(i)|12|6|11|Reseeding grassland:
Q6(a)(ii)|4|6|11|Establishment of newly-sown grass:
Q6(a)(iii)|4|6|11|Practices for successful establishment:
Q6(b)(i)|12|6|11|Productivity features of PRG v. IRG:
Q6(b)(ii)|4|6|11|What are they: Result of crossing
Q6(c)(i)|6|6|11|How better grassland management prevents more cattle parasite infestation:
Q6(c)(ii)|6|6|11|Examples of cattle parasites:
Q7(a)(i)|5|6|12|Polyploidy
Q7(a)(ii)|5|6|12|Freemartin condition
Q7(a)(iii)|5|6|12|Micropropagation
Q7(b)|18|6|12|Parental genotype: GgNn
Q7(c)(i)|6|6|12|Embryo transfer:
Q7(c)(ii)|9|6|12|Benefits of embryo transfer:
Q8(a)(i)|12|7|13|Grass to silage
Q8(a)(ii)|12|7|13|Practical steps related to
Q8(b)(i)|12|7|13|NPK in plants
Q8(b)(ii)|12|7|13|Experiment to show effect of a deficiency:
Q8(c)|24|7|13|Zero grazing: animals are indoors
Q9(a)|12|7|14|Trailing shoe to spread slurry:
Q9(b)|12|7|14|Thinning forestry trees:
Q9(c)|12|7|14|Algal bloom:
Q9(d)|12|7|14|Farrowing crate:
Q9(e)|12|7|14|Rushes in gley soils:
'''
POOLS_2018_HIGHER = {'Q3 Option Two (b)': (1, ['Barley', 'Wheat', 'Oats', 'Maize']), 'Q4(c)': (1, ['Amylase', 'Catalase'])}
# 2018 Ordinary (legacy syllabus), transcribed from the SEC paper and scheme.
ORDINARY_2018 = '''
Q1|20|2|5|Soil component at A:
Q2|20|3|5|Mass of offspring at birth (kg)
Q3|20|3|5|Liver fluke’s primary host: Sheep
Q4|20|4|6|Role of A:
Q5|20|5|6|Cotyledons store food in seeds
Q6|20|6|6|Parts of grass flower:
Q7|20|7|7|Finding soil pH before sowing:
Q8(a)(i)|8|8|8|Differences between composition of slurry and FYM:
Q8(a)(ii)|8|8|8|Steps to reduce water pollution by slurry:
Q8(b)(i)|12|8|8|Elements in 18-6-12:
Q8(b)(ii)|8|8|8|Advantage and disadvantage of artificial fertilisers:
Q8(b)(iii)|4|8|8|Role of one element in 18-6-12:
Q8(c)|20|8|8|Experiment to measure % water content in soil:
Q9(a)(i)|8|8|9|Maincrop potato varieties:
Q9(a)(ii) — soil preparation|8|8|9|1. Soil preparation:
Q9(a)(ii) — fertiliser use|4|8|9|2. Fertiliser use:
Q9(a)(ii) — weed control|4|8|9|3. Weed control:
Q9(a)(ii) — blight control|4|8|9|4. Blight control:
Q9(b)|12|8|9|Why use certified seed potatoes:
Q9(c)|20|8|9|Experiment to estimate yield of potato crop:
Q10(a)(i)|6|9|10|Parts of cell during mitosis:
Q10(a)(ii)|3|9|10|Stage of mitosis shown: Metaphase
Q10(a)(iii)|3|9|10|Stage before metaphase: Prophase
Q10(b)(i)|3|9|10|Clone:
Q10(b)(ii)|3|9|10|Crop that may be produced by cloning:
Q10(c)|18|9|10|Cross 1:
Q10(d)|24|9|10|Cross 2:
Q11(a)|16|10|11|Spring barley v. Winter barley
Q11(b)|4|10|11|Differences between cultivation and harvesting of feeding and malting barley:
Q11(c)|4|10|11|Features that show barley is ready for harvest:
Q11(d)(i)|4|10|11|Click beetle larva: Wireworm
Q11(d)(ii)|4|10|11|Crane fly larva: Leatherjacket
Q11(d)(iii)|8|10|11|Cereal disease and prevention:
Q11(e)|20|10|11|Experiment to find % germination of barley seeds:
Q12(a)(i)|12|10|12|Paddock grazing system
Q12(a)(ii)|3|10|12|Advantage of paddock grazing system:
Q12(a)(iii)|3|10|12|Disadvantage of paddock grazing system:
Q12(b)|18|10|12|Making good quality hay
Q12(c)|9|10|13|Good quality silage:
Q12(d)|15|10|13|Tests to determine silage quality, and their purpose:
Q13(a)(i)|6|11|14|Lowland sheep breeds:
Q13(a)(ii) — flushing|4|11|14|1. Flushing
Q13(a)(ii) — scanning|4|11|14|2. Scanning
Q13(a)(ii) — steaming up|4|11|14|3. Steaming up
Q13(a)(ii) — vaccination|4|11|14|4. Vaccination
Q13(a)(ii) — creep feeding|4|11|14|5. Creep feeding
Q13(a)(ii) — shearing|4|11|14|6. Shearing
Q13(b)(i)|3|11|15|Gas produced in photosynthesis:
Q13(b)(ii)|6|11|15|Factors necessary for photosynthesis:
Q13(b)(iii)|3|11|15|How photosynthesis helps reduce climate change:
Q13(b)(iv)|18|11|15|Testing a leaf for starch:
Q13(c)(i)|6|11|15|Care at birth:
Q13(c)(ii)|6|11|15|Housing: Straw (or dry) bedding
Q13(c)(iii)|6|11|15|Disease prevention:
Q13(c)(iv)|6|11|15|Introducing hay into their diet:
Q13(c)(v)|6|11|15|Use of milk replacer:
Q13(d)(i)|10|11|16|Molar tooth labelled diagram
Q13(d)(ii)|6|11|16|Function of incisor:
Q13(d)(iii)|6|11|16|Two other teeth:
Q13(d)(iv)|8|11|16|Dental formula
'''
POOLS_2018_ORDINARY = {'Q8(b)(iii)': (1, ['Nitrogen', 'Phosphorus', 'Potassium']), 'Q13(d)(iv)': (1, ['Pig', 'Sheep'])}
# 2017 Higher (legacy syllabus), transcribed from the SEC paper and scheme.
HIGHER_2017 = '''
Q1(a)|10|2|5|Species:
Q1(b)|10|2|5|Biological control: Control of pests
Q1(c)|10|2|5|Structural differences:
Q1(d)|10|2|5|Marble: Metamorphic
Q1(e)|10|2|5|What determines amount of animal ration protein:
Q1(f)|10|2|5|Leaf structure for photosynthesis:
Q1(g)|10|2|6|Dental formulae:
Q1(h)|10|2|6|N-fixing bacteria: Rhizobia
Q1(i)|10|2|6|BCS for dairy cow:
Q1(j)|10|2|6|FSH: Promotes follicle development
Q2(a)(i)|10|2|7|How water held in soil:
Q2(a)(ii)|6|2|7|Benefits of artificial drainage:
Q2(b)(i)|6|2|7|How soil acidity increases over time:
Q2(b)(ii)|6|2|7|Matching mechanisms of acid increase:
Q2(b)(iii)|4|2|7|Effects of increased acidity on crops:
Q2(c)|16|2|7|to show cation exchange in soil:
Q3 Option One (a)|16|3|8|Requirements for winter housing for beef weanlings:
Q3 Option One (b)(i)|10|3|8|Winter feeding programmes:
Q3 Option One (b)(ii)|6|3|8|Target weights:
Q3 Option One (c)(i)|4|3|8|Nutrient value:
Q3 Option One (c)(ii)|4|3|8|Storage:
Q3 Option One (c)(iii)|4|3|8|Spreading method:
Q3 Option One (c)(iv)|4|3|8|Disadvantages of spreading:
Q3 Option Two (a)(i)|4|3|9|Soil suitability:
Q3 Option Two (a)(ii)|4|3|9|Sowing:
Q3 Option Two (a)(iii)|4|3|9|Weed control:
Q3 Option Two (a)(iv)|4|3|9|Storage:
Q3 Option Two (b)|16|3|9|Cereal cultivation:
Q3 Option Two (c)(i)|8|3|9|Cereal ripening changes:
Q3 Option Two (c)(ii)|8|3|9|Tests on harvested grain:
Q4(a)|24|4|11|Compare digestibility of whole and rolled cereal grains:
Q4(b)|24|4|11|Determine quality of pit or bale silage:
Q4(c)|24|4|11|Compare capillarity in two soils:
Q4(d)|24|4|11|Measure rate of transpiration:
Q5(a)(i)|8|4|12|Qualitative tests on milk:
Q5(a)(ii)|8|4|12|Description of any one quantitative test:
Q5(b)(i)|10|4|12|Lowland sheep breeds:
Q5(b)(ii)|6|4|12|Why crossbred ewes used in lowland enterprise:
Q5(c)(i)|4|4|13|Reproductive efficiency:
Q5(c)(ii)|12|4|13|Factors affecting reproductive efficiency:
Q6(a)|16|4|13|How DMD changes as grass grows:
Q6(b)|16|4|13|Methods to maintain high grass DMD for longer:
Q6(c)|16|4|13|How ruminant stomach suited to digestion of grassland plants:
Q7(a)(i)|8|5|14|Performance testing:
Q7(a)(ii)|9|5|14|Characteristics for selection of replacement heifers:
Q7(b)(i)|5|5|14|Incomplete dominance:
Q7(b)(ii)|5|5|14|Alleles:
Q7(b)(iii)|5|5|14|Continuous variation:
Q7(c)|16|5|14|All gametes correct
Q8(a)|24|6|15|Carbon cycle:
Q8(b)(i)|12|6|15|Principal structural features of insects:
Q8(b)(ii)|12|6|15|Insect pests and the damage they do:
Q8(c)|24|6|15|Distinguish between terms:
Q9(a)|12|6|16|Environmental temperature and weight gain in pigs:
Q9(b)|12|6|16|Dense conifer planting in forestry:
Q9(c)|12|6|16|Low earthworm population in intensely cultivated soils:
Q9(d)|12|6|16|Grit in free-range poultry digestive tracts:
Q9(e)|12|6|16|Deep ploughing podzolic soils:
'''
POOLS_2017_HIGHER = {'Q3 Option Two (b)': (1, ['Barley', 'Wheat', 'Oats', 'Maize']), 'Q4(a)': (1, ['Feeding trial', 'Test-tube method']), 'Q4(b)': (1, ['Leaf to stem ratio', 'pH test', 'To get DM content', 'For good quality silage (poor quality)']), 'Q5(a)(ii)': (1, ['Gerber butterfat test', 'Adulteration of milk with water (lactometer)', 'Adulteration of milk with water (cryoscope)', '% water or % solids', 'To find the % ash (or % minerals) in milk', 'To find the % lactose in milk', 'To find the % protein'])}
# 2017 Ordinary (legacy syllabus), transcribed from the SEC paper and scheme.
ORDINARY_2017 = '''
Q1|20|3|5|Why dry soil:
Q2|20|4|5|Power harrow
Q3|20|5|6|Diaphragm separates chest from abdomen:
Q4|20|5|6|Foot and mouth disease
Q5|20|6|6|What aspect of germination being tested:
Q6|20|7|7|Cabbage white life cycle stages:
Q7|20|8|7|Shelter belts:
Q8(a)(i)|9|9|8|Functions of cow skeleton:
Q8(a)(ii)|6|9|8|Mineral and vitamin for bone development:
Q8(b)(i)|6|9|8|Teeth: A = Incisor
Q8(b)(ii)|6|9|8|Functions of teeth:
Q8(c)(i)|6|9|8|Cow stomach chambers:
Q8(c)(ii)|6|9|8|Function of chambers:
Q8(d)(i)|12|9|8|Cow heart:
Q8(d)(ii)|6|9|8|Function of septum:
Q8(d)(iii)|3|9|8|Heart location:
Q9(a)(i)|4|10|9|Haploid:
Q9(a)(ii)|4|10|9|Homozygous: Both alleles are the same
Q9(a)(iii)|4|10|9|Locus: Position of a gene on a chromosome
Q9(b)(i)|4|10|9|What about the genes for straw length:
Q9(b)(ii)|12|10|9|Cross 1
Q9(b)(iii)|24|10|9|Cross 2
Q9(c)(i)|4|10|9|Advantage of AI:
Q9(c)(ii)|4|10|9|Disadvantage of AI:
Q10(a)(i)|3|11|10|Grass in picture A:
Q10(a)(ii)|6|11|10|Why use this grass when reseeding:
Q10(a)(iii)|3|11|10|Plant in picture B: Clover
Q10(a)(iv)|6|11|10|Why use clover in seed mixture:
Q10(b)(i)|3|11|10|Why weeds should be controlled in grassland:
Q10(b)(ii)|6|11|10|How weeds controlled in grassland other than with herbicides:
Q10(c)|18|11|10|Strip grazing:
Q10(d)|15|11|10|Experiment - percentage sugar in grass:
Q11(a)(i)|12|11|11|How iron pan formed:
Q11(a)(ii)|8|11|11|Effect of iron pan:
Q11(a)(iii)|4|11|11|Which soil most likely to have iron pan: Podzol
Q11(a)(iv)|4|11|11|How iron pan removed: Deep ploughing or subsoiler
Q11(b)|16|11|11|How to take soil samples for testing:
Q11(c)|16|11|11|How to measure soil pH:
Q12(a)(i)|4|12|12|A = Stoma
Q12(a)(ii)|8|12|12|Functions of stoma (A):
Q12(a)(iii)|4|12|12|Function of cells B: Photosynthesis
Q12(a)(iv)|8|12|12|How leaf structure suited to photosynthesis:
Q12(b)(i)|4|12|12|Type of plant with this stem cross section:
Q12(b)(ii)|4|12|12|X = Vascular bundles
Q12(b)(iii)|8|12|12|Functions of vascular bundles (X):
Q12(b)(iv)|4|12|12|Plant with modified stem:
Q12(c)|16|12|12|To show phototropism in seedlings:
Q13(a)(i)|3|13|13|A = Water
Q13(a)(ii)|3|13|13|Colostrum:
Q13(a)(iii)|6|13|13|Differences between colostrum and milk:
Q13(a)(iv)|6|13|13|How farmer could improve herd milk quality:
Q13(a)(v)|3|13|13|Why milk from mastitis-treated cows
Q13(a)(vi)|3|13|13|Why cull dairy cows:
Q13(a)(vii)|3|13|13|Dual purpose breed: Produces both milk
Q13(a)(viii)|3|13|13|An example of a dual purpose breed:
Q13(b)(i)|6|13|13|Soil type:
Q13(b)(ii)|3|13|13|Sowing time:
Q13(b)(iii)|3|13|13|Sowing method:
Q13(b)(iv)|6|13|13|Weed control:
Q13(b)(v)|6|13|14|Disease control:
Q13(b)(vi)|6|13|14|Harvesting:
Q13(c)(i)|6|13|14|Pollution: Any harmful addition to the environment.
Q13(c)(ii) — silage|6|13|14|When making silage:
Q13(c)(ii) — dairy farm|6|13|14|On a dairy farm:
Q13(c)(ii) — fertiliser|6|13|14|When spreading artificial fertiliser:
Q13(c)(ii) — insecticides|6|13|14|When using insecticides or fungicides:
Q13(d)(i)|9|13|14|Housing:
Q13(d)(ii)|6|13|14|Diet:
Q13(d)(iii)|6|13|14|Parasite and disease control:
Q13(d)(iv)|3|13|14|Turnout target weight: 270-320 kg
Q13(d)(v)|6|13|14|Compensatory growth:
'''
POOLS_2017_ORDINARY = {'Q11(c)': (1, ['Universal indicator', 'pH meter'])}
# 2016 Higher (legacy syllabus), transcribed from the SEC paper and scheme.
HIGHER_2016 = '''
Q1(a)|10|2|5|Spermatophyta or Angiospermae
Q1(b)(i)|4|2|5|The amount of dissolved oxygen needed
Q1(b)(ii)|6|2|5|Slurry application at correct time
Q1(c)|10|2|5|Spores/sporangium/columella
Q1(d)(i)|4|2|5|A disease of national importance
Q1(d)(ii)|6|2|5|Scrapie/ Aujeszky disease
Q1(e)|10|2|5|Rhizomes/ cultivation spreads it
Q1(f)|10|2|5|Small intestine or duodenum or ileum
Q1(g)|10|2|5|Humus more fertile
Q1(h)(i)|4|2|5|A crop grown between two main crops.
Q1(h)(ii)|6|2|5|Provides fodder/ good crop rotation
Q1(i)|10|2|5|Oxygen needed or aerobic respiration
Q1(j)|10|2|5|E. coli scour/ Erysipelas
Q2(a)|18|3|6|Drainage: waterlogged or bad
Q2(b)|12|3|6|Wetting and drying
Q2(c)(i)|12|3|6|Dry soil sample/ crush aggregates
Q2(c)(ii)|3|3|6|Tillage crops or named tillage crop.
Q2(c)(iii)|3|3|6|Early growth or heats up faster
Q3 Option One (a)|16|3|6|Housing/ hygiene specified
Q3 Option One (b)|16|3|6|Named breed/ terminal sires
Q3 Option One (c)|16|3|6|Productivity: yield of grass.
Q3 Option Two (a)|16|4|7|Housing time or type
Q3 Option Two (b)|16|4|7|Rotational grazing system (example strip or paddock)
Q3 Option Two (c)(i)|6|4|7|Is a grading system
Q3 Option Two (c)(ii)|4|4|7|Highly productive: E1 or E2
Q3 Option Two (c)(iii)|6|4|7|Cross breeding/ using high quality beef bulls
Q4(a)|24|4|7|without Mg or soil deficient in Mg
Q4(b)|24|4|7|Named crop*/quadrat
Q4(c)|24|4|7|Dry sample of feed/ weigh sample
Q4(d)|24|4|7|Quadrat or line transect
Q5(a)(i)|6|4|8|A. Jersey.
Q5(a)(ii)|6|4|8|A: Lower yield/ higher solids.
Q5(a)(iii)|4|4|8|Fat: 4 - 7%.
Q5(b)|24|4|8|Age of cow (decreases with age)
Q5(c)|8|4|8|Condition: 2.8-3.2 for heat
Q6(a)(i)|2|5|8|Any method of control that is effective
Q6(a)(ii)|12|5|8|Stubble cleaning (uproots weed seedlings)
Q6(b)|16|5|8|Characteristics: texture/ pH
Q6(c)(i)|10|5|8|Wind/ rain/ excessive N
Q6(c)(ii)|8|5|8|Frost (soggy or rot)
Q7(a)(i)|4|5|9|F1 hybrids: progeny of two purebred parents
Q7(a)(ii)|4|5|9|Continuous variation: Characteristic controlled
Q7(a)(iii)|4|5|9|Back cross: Breeding a cross-breed offspring
Q7(a)(iv)|4|5|9|Incomplete dominance: Neither allele dominant
Q7(b)(i)|4|5|9|(i) BbPp.
Q7(b)(ii)|8|5|9|BbPp, Bbpp, bbPp, bbpp.
Q7(b)(iii)|4|5|9|(iii) 25%
Q7(b)(iv)|4|5|9|50% chance.
Q7(b)(v)|4|5|9|Law of Segregation:
Q7(c)|8|5|9|Production index: fat/ protein/ yield of milk.
Q8(a)(i)|4|6|10|Cranefly or daddy longlegs
Q8(a)(ii)|4|6|10|Leatherjacket: underground stem
Q8(a)(iii)|2|6|10|(iii) Arthropoda.
Q8(a)(iv)|6|6|10|Jointed limbs/ exoskeleton
Q8(a)(v)|8|6|10|Complete (incomplete): larva (nymph)
Q8(b)|24|6|10|Benefits of nitrogen:
Q8(c)|24|6|10|Crossing over: process in which
Q9(a)|12|6|11|Absence of snail/ Lymnaea
Q9(b)|12|6|11|Root hairs/ root xylem
Q9(c)|12|6|11|Cross/ between two named breeds
Q9(d)|12|6|11|Sulphuric acid or formic acid
Q9(e)|12|6|11|CO2 needed for photosynthesis
'''
POOLS_2016_HIGHER = {}
# 2016 Ordinary (legacy syllabus), transcribed from the SEC paper and scheme.
ORDINARY_2016 = '''
Q1|20|2|5|Two sedimentary rocks
Q2|20|3|5|Question 2. (10
Q3|20|4|5|High milk yields or good quality milk
Q4|20|5|6|Soil sieves D
Q5|20|6|6|A = Petal
Q6|20|7|6|A = (Liver)fluke
Q7|20|8|7|Animal feed or meal or concentrate
Q8(a)(i)|6|9|8|Grass: Perennial ryegrass
Q8(a)(ii)|6|9|8|Any one reason for the use of either
Q8(a)(iii)|14|9|8|Named method
Q8(b)(i)|6|9|9|Easier to make in small fields
Q8(b)(ii)|6|9|9|More expensive to make
Q8(c)|22|9|9|Examine the colour of the silage
Q9(a)(i)|9|10|10|A = Trachea or windpipe
Q9(a)(ii)|3|10|10|Gaseous exchange or described
Q9(a)(iii)|9|10|10|Good ventilation/ no draughts
Q9(a)(iv)|12|10|10|Adult (female) worm
Q9(a)(v)|3|10|10|Vaccination or dosing or leader-follower
Q9(b)(i)|3|10|10|Excretion/ getting rid of wastes
Q9(b)(ii)|9|10|10|X = Ureter
Q9(b)(iii)|3|10|10|Urine or salt or urea or water
Q9(c)|9|10|10|Rough grazing or long grass
Q10(a)(i)|3|11|11|Damages leaves or damage described
Q10(a)(ii)|6|11|11|Black or brown spots on leaves
Q10(a)(iii)|6|11|11|Certified seed/ resistant varieties
Q10(b)(i)|9|11|11|(Medium) loam or good texture
Q10(b)(ii)|6|11|11|Potato planter/ seed planted in ridges
Q10(b)(iii)|6|11|11|Spray/ herbicide/ earthing up
Q10(b)(iv)|6|11|11|Elevator digger/ collected by hand
Q10(c)|18|11|11|Wash (soil from) potatoes
Q11(a)(i)|4|11|12|Drainage Well drained
Q11(a)(ii)|4|11|12|Fertility Low fertility
Q11(a)(iii)|4|11|12|Organic matter content Low
Q11(a)(iv)|4|11|12|Soil temperature High
Q11(b)(i)|6|11|12|Add organic matter or named example
Q11(b)(ii)|6|11|12|Create channels or holes
Q11(b)(iii)|3|11|12|Annelida
Q11(b)(iv)|11|11|12|cylindrical shape and segmented body
Q11(c)(i)|3|11|12|Green colour or chlorophyll formation
Q11(c)(ii)|6|11|12|Urea/ C.A.N./ ammonium sulphate
Q11(c)(iii)|6|11|12|Pollution/ eutrophication/ algal bloom
Q11(c)(iv)|3|11|12|Nitrogen fixation or explained
Q12(a)(i)|4|12|13|Nucleus
Q12(a)(ii)|4|12|13|Carry genes
Q12(a)(iii)|4|12|13|(iii) 27
Q12(b)(i)|8|12|13|Gametes (P)
Q12(b)(ii)|4|12|13|Genotype of calf (Pp)
Q12(b)(iii)|4|12|13|Polled (or hornless)
Q12(c)(i)|4|12|13|Genotypes of parents (Pp)
Q12(c)(ii)|8|12|13|Possible gametes (P) (p)
Q12(c)(iii)|6|12|13|(PP) (Pp) (pp)
Q12(c)(iv)|4|12|13|Polled Horned
Q12(d)(i)|4|12|13|Crossing two different breeds
Q12(d)(ii)|6|12|13|Ewes are better mothers
Q13(a)(i)|6|13|14|Suffolk/ Texel/ Border Leicester
Q13(a)(ii)|6|13|14|Terminal sire/ excellent conformation
Q13(a)(iii)|12|13|14|Clear mucus/ navel dip
Q13(a)(iv)|6|13|14|Flushing: Process of moving ewes
Q13(b)(i)|6|13|14|Large white/ Landrace
Q13(b)(ii)|12|13|14|Dry sow house
Q13(b)(iii)|6|13|14|Cause of anaemia
Q13(b)(iv)|6|13|14|Good conformation/ Good feet and legs
Q13(c)(i)|9|13|15|Good hygiene/ adequate supervision
Q13(c)(ii)|6|13|15|Rich in antibodies
Q13(c)(iii)|6|13|15|Clean holding area
Q13(c)(iv)|9|13|15|Old age/ grading up
Q13(d)(i)|3|13|15|To produce glucose or sugar
Q13(d)(ii)|3|13|15|Chlorophyll
Q13(d)(iii)|24|13|15|Method A
'''
POOLS_2016_ORDINARY = {'Q8(a)(iii)': (1, ['Direct sowing', 'Undersowing', 'Direct drilling (or direct seeding)', 'Stitching-in']), 'Q13(a)(ii)': (1, ['Suffolk', 'Texel', 'Border Leicester', 'Bluefaced Leicester', 'Galway']), 'Q13(d)(iii)': (1, ['Method A', 'Method B'])}
# 2015 Higher (legacy syllabus), transcribed from the SEC paper and scheme.
HIGHER_2015 = '''
Q1(a)|10|2|5|Disease/ damaged trees/ harvesting thinnings
Q1(b)|10|2|5|Annelida/ Arthropoda/ Platyhelminthes
Q1(c)|10|2|5|Pollution or damage to wildlife
Q1(d)|10|2|5|High rainfall/ waterlogging or poor drainage
Q1(e)|10|2|5|Monocot or named monocot feature
Q1(f)|10|2|5|Fern: Flowerless
Q1(g)|10|2|5|Environmental temperature at which pigs
Q1(h)|10|2|5|Interdependence: organisms depending on each other
Q1(i)|10|2|5|Maximum two transport points
Q1(j)|10|2|5|Direction in which a field is facing
Q2(a)(i)|6|2|6|High rainfall or low evaporation
Q2(a)(ii)|8|2|6|Sandy soil has more air
Q2(a)(iii)|2|2|6|Soil colour or organic matter content
Q2(b)(i)|12|2|6|Cation: positively charged particle
Q2(b)(ii)|2|2|6|Adding humus or organic matter
Q2(c)|18|2|6|Sieved soil sample
Q3 Option One (a)(i)|8|3|7|Start growing immediately
Q3 Option One (a)(ii)|8|3|7|State or imply that the statement is true
Q3 Option One (b)(i)|8|3|7|Spores airborne
Q3 Option One (b)(ii)|4|3|7|Leaf (or stem) has black spots
Q3 Option One (b)(iii)|4|3|7|Spray fungicide/ plant resistant varieties
Q3 Option One (c)(i)|8|3|7|Disease: Leaf roll
Q3 Option One (c)(ii)|8|3|7|Low numbers of aphids
Q3 Option Two (a)(i)|4|3|8|Management: Isolate or supervise
Q3 Option Two (a)(ii)|4|3|8|Environmental conditions: indoors
Q3 Option Two (a)(iii)|4|3|8|Feeding principles: colostrum
Q3 Option Two (b)(i)|10|3|8|Management: disease prevention
Q3 Option Two (b)(ii)|10|3|8|Feeding principles: introduction to milk
Q3 Option Two (c)(i)|4|3|8|170 – 220 kg
Q3 Option Two (c)(ii)|12|3|8|Target weight reached
Q4(a)|24|3|8|Start with dry grass
Q4(b)|24|3|8|2 areas of equal size
Q4(c)|24|3|8|Name crop/ minimum 2 varieties
Q4(d)|24|3|8|Agar plates/ sterile
Q5(a)(i)|4|4|9|Having several oestrous cycles
Q5(a)(ii)|4|4|9|15-19 days inclusive
Q5(a)(iii)|4|4|9|Shorter days = less light
Q5(b)|12|4|9|Must have ovaries and oviducts
Q5(c)|12|4|9|Insert sponges
Q5(d)|12|4|9|Udders damaged/ barren
Q6(a)|16|4|9|Soil type or sandy or clay or loam
Q6(b)|16|4|9|Variety sown/ certified seed
Q6(c)(i)|4|4|9|Transpiration: the water evaporating
Q6(c)(ii)|12|4|9|Light intensity [more light
Q7(a)(i)|4|4|10|When gametes are formed each
Q7(a)(ii)|12|4|10|Gene located on sex chromosomes
Q7(b)|16|4|10|Red straight/ red curly
Q7(c)|16|4|10|More heifer calves
Q8(a)|24|5|11|Nitrogen gas to useable compounds
Q8(b)(i)|12|5|11|Sowing/ seed mixture used
Q8(b)(ii)|6|5|11|Sheep grazing close to ground
Q8(b)(iii)|6|5|11|Livestock unit (LU) definition
Q8(c)|24|5|11|Topdressing: fertilizer
Q9(a)|12|5|12|Fermentation by clostridia
Q9(b)|12|5|12|Allow light in for photosynthetic activity
Q9(c)|12|5|12|Protection for flora or fauna
Q9(d)|12|5|12|Test for bacteria to show hygiene
Q9(e)|12|5|12|Castration of male animals
'''
POOLS_2015_HIGHER = {}
# 2015 Ordinary (legacy syllabus), transcribed from the SEC paper and scheme.
ORDINARY_2015 = '''
Q1|20|2|5|Male parts of flower
Q2|20|3|5|Nematoda
Q3|20|3|5|Question 3. (10
Q4|20|4|6|A = Barley
Q5|20|5|6|Quadrat
Q6|20|6|7|Microorganism type
Q7|20|7|7|Lameness/ old age/ infertility
Q8(a)(i)|6|8|8|Perennial ryegrass or PRG
Q8(a)(ii)|3|8|8|Heading out stage
Q8(a)(iii)|3|8|8|Dehydration/ enough time
Q8(a)(iv)|3|8|8|Lactobacillus spp.
Q8(b)(i)|12|8|8|Cut or mow/ on dry day
Q8(b)(ii)|9|8|8|Less weather dependent
Q8(b)(iii)|9|8|8|Easier to make in small fields
Q8(c)|15|8|8|Weigh beaker or named suitable container
Q9(a)(i)|12|8|9|Beef breeds: Charolais
Q9(a)(ii)|12|8|9|Block shaped/ thick neck
Q9(b)(i)|8|8|9|Hand pressure applied
Q9(b)(ii)|4|8|9|2.5 to 3
Q9(b)(iii)|8|8|9|Calf too big or calving difficulties
Q9(c)(i)|8|8|9|Known supplier
Q9(c)(ii)|8|8|9|Breed own replacements or closed herd
Q10(a)(i)|9|9|10|Freeze-thaw or frost action
Q10(a)(ii)|9|9|10|Gravel/ sand/ silt/ clay
Q10(b)(i)|6|9|10|The % sand, silt and clay in a soil
Q10(b)(ii)|15|9|10|Feel method
Q10(c)(i)|3|9|10|Earthworm
Q10(c)(ii)|6|9|10|Improve drainage/ improve aeration
Q10(c)(iii)|12|9|10|Mark out area to be sampled
Q11(a)(i)|8|10|11|Sheep/ goat/ deer
Q11(a)(ii)|12|10|11|Reticulum
Q11(a)(iii)|4|10|11|Abomasum/ D
Q11(b)(i)|4|10|11|Cellulose or fibre
Q11(b)(ii)|4|10|11|Further mechanical digestion
Q11(b)(iii)|4|10|11|Food is squeezed or dried
Q11(b)(iv)|4|10|11|Duodenum/ small intestine
Q11(c)(i)|16|10|11|Colostrum/ (whole) milk
Q11(c)(ii)|4|10|11|Build-up of gas
Q12(a)(i)|16|11|12|Award 4 marks if diagram has the correct shape
Q12(a)(ii)|4|11|12|Nucleus
Q12(a)(iii)|4|11|12|Mitosis
Q12(b)(i)|8|11|12|Gametes
Q12(b)(ii)|4|11|12|F1 genotypes
Q12(b)(iii)|4|11|12|F1 phenotype
Q12(c)|20|11|12|Award marks for genotypes only if gametes correct
Q13(a)(i)|2|12|13|145 -155 days
Q13(a)(ii)|9|12|13|Facilitates supervision
Q13(a)(iii)|9|12|13|Good ventilation/ no draughts
Q13(a)(iv)|10|12|13|Warms young lambs
Q13(b)(i)|9|12|13|Home Guard/ Epicure
Q13(b)(ii)|9|12|13|Windy weather/ aphid free
Q13(b)(iii)|6|12|13|Prevents exposure to light
Q13(b)(iv)|6|12|13|Good ventilation/ dry/ frost-proof
Q13(c)(i)|6|12|13|A = Water
Q13(c)(ii)|9|12|13|Breed/ age/ feed quantity
Q13(c)(iii)|9|12|13|Total bacterial count or TBC
Q13(c)(iv)|6|12|14|Clean holding area
Q13(d)(i)|3|12|14|20 °C
Q13(d)(ii)|6|12|14|Dry sow house/ weaner house
Q13(d)(iii)|6|12|14|Allows sow to suckle bonhams
Q13(d)(iv)|6|12|14|Teeth clipping/ tail docking
Q13(d)(v)|3|12|14|28 - 35 days
Q13(d)(vi)|6|12|14|Ratio of food consumed
'''
POOLS_2015_ORDINARY = {'Q4': (1, ['Barley', 'Maize', 'Oats', 'Wheat']), 'Q8(c)': (1, ['Drying in an oven', 'Wringing between hands']), 'Q10(b)(ii)': (1, ['Feel method', 'Sieve method', 'Sedimentation method'])}
# 2014 Higher (legacy syllabus), transcribed from the SEC paper and scheme.
HIGHER_2014 = '''
Q1(a)|10|2|5|find freezing point of sample
Q1(b)|10|2|5|Antibody production / absorbs lipids
Q1(c)|10|2|5|Soil temperature increases sooner in south-facing field
Q1(d)|10|2|5|Scrapie / Aujeszky’s disease
Q1(e)|10|2|5|Flowers / seeds / fruit / endosperm present
Q1(f)|10|2|5|Calcium ions (or magnesium ions)
Q1(g)|10|2|5|nectaries absent (nectaries present)
Q1(h)|10|2|5|Poor growth / leaching / denitrification
Q1(i)(i)|8|2|5|Carbon / hydrogen / oxygen / nitrogen
Q1(i)(ii)|2|2|5|Biuret / sodium hydroxide and copper sulphate
Q1(j)(i)|4|2|5|Oats
Q1(j)(ii)|4|2|5|Gramineae
Q1(j)(iii)|2|2|5|spikelet
Q2(a)(i)|4|2|6|Heat and pressure.
Q2(a)(ii)|8|2|6|Marble from limestone
Q2(a)(iii)|4|2|6|acidic or alkaline / coarse or fine
Q2(b)(i)|4|2|6|Dung / slurry / seaweed
Q2(b)(ii)|16|2|6|Structure and aggregation / erosion prevention
Q2(c)|12|2|6|Soil must be dry at start
Q3 Option One (a)|16|3|6|low temperatures : poor grass growth rates
Q3 Option One (b)(i)|4|3|6|Suitable weather / suitable drying conditions
Q3 Option One (b)(ii)|12|3|6|cut correct stage, not too heavy
Q3 Option One (c)|16|3|6|High quality ryegrass species or clover
Q3 Option Two (a)(i)|4|3|7|Glycogen / vitamins A / D / B12
Q3 Option Two (a)(ii)|12|3|7|skin or adipose tissue : fat
Q3 Option Two (b)(i)|2|3|7|Platyhelminthes
Q3 Option Two (b)(ii)|6|3|7|Flat / triploblastic / acoelomate
Q3 Option Two (b)(iii)|8|3|7|5, 3, 0m
Q3 Option Two (c)|16|3|7|Adult attached to bile duct
Q4(a)|24|3|7|Effect of lime on growth of oats
Q4(b)|24|3|7|Effect of sprouting on the yield of early potatoes
Q4(c)|24|3|7|Butterfat % of a sample of fresh milk
Q4(d)|24|3|7|To show that germinating seeds release heat energy
Q5(a)|18|4|8|Named plant (with tap root)
Q5(b)(i)|4|4|8|amount of water held in the soil after gravitational
Q5(b)(ii)|4|4|8|when all the capillary water is used
Q5(b)(iii)|4|4|8|The portion of water held in soil
Q5(c)|12|4|8|Poor development / low yield
Q5(d)(i)|2|4|8|(i) B
Q5(d)(ii)|4|4|8|most available water
Q6(a)|12|4|8|Good feet / healthy udder
Q6(b)(i)|5|4|8|35-45 kg
Q6(b)(ii)|5|4|8|55-280 kg
Q6(b)(iii)|5|4|8|280-300 kg
Q6(b)(iv)|5|4|8|290-340 kg
Q6(c)(i)|8|4|8|bile : liver or gall bladder
Q6(c)(ii)|8|4|8|beak / crop / proventiculus / gizzard / cloaca
Q7(a)(i)|2|5|9|Chromosomes
Q7(a)(ii)|10|5|9|XX Female
Q7(b)|12|5|9|exact copy of the cell or organism
Q7(c)(i)|4|5|9|NnRr
Q7(c)(ii)|16|5|9|Crinkly leaves 40
Q7(d)|4|5|9|Health & safety / to stop inbreeding
Q8(a)|24|5|10|Sow in farrowing house
Q8(b)|24|5|10|Plough / depth 12-20cm
Q8(c)|24|5|10|alteration of any part of the earth’s surface
Q9(a)|12|6|11|Ruminant / rumen developed
Q9(b)|12|6|11|Break iron pan or hard pan
Q9(c)|12|6|11|Reduce wind speed
Q9(d)|12|6|11|Improves condition prior to mating
Q9(e)|12|6|11|Red water fever / Babesia
'''
POOLS_2014_HIGHER = {'Q1(a)': (1, ['Freezing point', 'Density', 'Total solids']), 'Q8(b)': (1, ['Barley', 'Wheat', 'Oats', 'Maize'])}
# 2014 Ordinary (legacy syllabus), transcribed from the SEC paper and scheme.
ORDINARY_2014 = '''
Q1|20|2|5|Lowland sheep breed
Q2|20|3|5|Combine (harvester)
Q3|20|4|5|Red coloured urine
Q4|20|5|6|Cranefly or daddy-long-legs
Q5|20|6|6|Question 5.
Q6|20|6|6|An animal that feeds on plants
Q7|20|7|7|Eliminates or kills (broad leaved) weeds
Q8(a)|16|8|8|Sire selection / record date
Q8(b)|8|8|8|Rich in antibodies/ provides immunity
Q8(c)(i)|12|8|8|Clean housing or named example
Q8(c)(ii)|8|8|8|Scour / joint-ill / navel ill
Q8(d)(i)|3|8|8|Digestion of cellulose / contains bacteria
Q8(d)(ii)|4|8|8|Feeding of hay or straw
Q8(d)(iii)|9|8|8|Reticulum / omasum / abomasum
Q9(a)(i)|6|8|9|Perennial ryegrass or PRG
Q9(a)(ii)|8|8|9|Nitrogen fixation / protein source
Q9(b)(i)|10|8|9|Any two labels
Q9(b)(ii)|8|8|9|Better grass utilisation
Q9(c)|8|8|9|Increased growth rates in cattle and sheep
Q9(d)(i)|4|8|9|Nitrogen
Q9(d)(ii)|16|8|9|One (or two) plots
Q10(a)|12|9|10|Sound feet or legs
Q10(b)(i)|8|9|10|Ewes on bare pasture
Q10(b)(ii)|8|9|10|Sponge containing hormone
Q10(c)|12|9|10|Colostrum / ewe’s milk
Q10(d)(i)|4|9|10|Miracidium / redia
Q10(d)(ii)|4|9|10|Mud snail / freshwater snail
Q10(d)(iii)|4|9|10|Loss in weight / failure to thrive
Q10(d)(iv)|8|9|10|Drainage / fence off wet land
Q11(a)|12|9|11|Podzols are poor soils with high
Q11(b)(i)|9|9|11|Rich in nutrients or plant food
Q11(b)(ii)|6|9|11|Add FYM / add slurry
Q11(b)(iii)|16|9|11|(Empty) crucible or dish
Q11(c)(i)|5|9|11|% sand, silt and clay in a soil
Q11(c)(ii)|12|9|11|Good drainage
Q12(a)(i)|8|10|12|Prophase
Q12(a)(ii)|3|10|12|Metaphase
Q12(a)(iii)|3|10|12|Chromosomes in centre of cell
Q12(a)(iv)|3|10|12|Meiosis
Q12(b)(i)|3|10|12|Artificial insemination
Q12(b)(ii)|6|10|12|Choice /superior bulls
Q12(c)(i)|8|10|12|Possible gametes:
Q12(c)(ii)|4|10|12|F1 genotype:
Q12(c)(iii)|4|10|12|F1 phenotype:
Q12(d)|18|10|12|Genotypes of parents:
Q13(a)(i)|4|11|13|Without oxygen (air)
Q13(a)(ii)|8|11|13|Lactobacillus / Streptococcus
Q13(a)(iii)|6|11|13|Rolling / quick filling
Q13(a)(iv)|12|11|13|Two sterile agar plates
Q13(b)(i)|3|11|13|Growth of a new plant
Q13(b)(ii)|9|11|13|Warmth or suitable temperature
Q13(b)(iii)|6|11|13|Keeps soil temperature higher
Q13(b)(iv)|12|11|13|Seeds / count / soak seeds
Q13(c)(i)|3|11|14|Annelida
Q13(c)(ii)|9|11|14|Improve aeration / improve drainage
Q13(c)(iii)|6|11|14|Add lime or maintain correct pH
Q13(c)(iv)|12|11|14|Wormery or suitable container
Q13(d)(i)|6|11|14|Carbohydates / lipids or fats
Q13(d)(ii)|8|11|14|Energy / insulation / protection
Q13(d)(iii)|4|11|14|The part of the food that contains nutrients
Q13(d)(iv)|12|11|14|Named foodstuff / suitable container
'''
POOLS_2014_ORDINARY = {}
# 2013 Higher (legacy syllabus), transcribed from the SEC paper and scheme.
HIGHER_2013 = '''
Q1(a)|10|2|5|Two from: (British) Saddle Back
Q1(b)|10|2|5|Increases soil temp/ can be sown earlier
Q1(c)|10|2|5|solution or Benedict
Q1(d)|10|2|5|(i) Metamorphic; (ii) sedimentary
Q1(e)|10|2|5|Leptospirosis
Q1(f)|10|2|5|Tick sucks blood/ from infected cow
Q1(g)|10|2|5|liquid (solid)/ no straw (straw)
Q1(h)(i)|5|2|5|Between aorta and liver
Q1(h)(ii)|5|2|5|Between small intestine (ileum) and liver
Q1(i)|10|2|5|Palea or glume or bract
Q1(j)|10|2|5|Calf = 35-45 kg
Q2(a)(i)|12|2|5|Result A = Field 2
Q2(a)(ii)|4|2|5|(ii) Potassium
Q2(b)(i)|8|2|5|All must pass through sieve 3.35 mm mesh
Q2(b)(ii)|8|2|5|Trace element (copper) uptake diminished
Q2(c)|16|2|5|Small quantity of soil/ add deionised
Q3 Option One (a)(i)|12|3|6|Contaminates cereal sown for seed
Q3 Option One (a)(ii)|4|3|6|Ragwort/ Thistle/ Dock
Q3 Option One (b)(i)|8|3|6|Less use of horses
Q3 Option One (b)(ii)|8|3|6|Animal feed/ human consumption/ new winter varieties
Q3 Option One (c)(i)|12|3|6|each stage is distinct
Q3 Option One (c)(ii)|4|3|6|butterfly/ cranefly/ click beetle
Q3 Option Two (a)(i)|4|3|6|Getting a ewe to accept
Q3 Option Two (a)(ii)|12|3|6|Rub birth-membranes
Q3 Option Two (b)(i)|12|3|6|Not enough feeding space
Q3 Option Two (b)(ii)|4|3|6|Poaching/ disease/ poor grass utilisation
Q3 Option Two (c)(i)|8|3|6|Suffolk (Charolais)
Q3 Option Two (c)(ii)|8|3|6|Early maturing breed needed
Q4(a)|24|3|7|2 samples dry soil or named soil types
Q4(b)|24|3|7|Rinse roots/ cut off roots
Q4(c)|24|3|7|Quadrat or cage
Q4(d)|24|3|7|Stated amount of water/ in calorimeter
Q5(a)|16|4|7|Bull has testosterone or not castrated
Q5(b)|16|4|7|Cow is in-calf/ BCS = 3
Q5(c)|16|4|7|Cows old/ milk machine not serviced
Q6(a)(i)|4|4|8|Prevents soil getting into pit
Q6(a)(ii)|12|4|8|Water-content too high
Q6(b)(i)|4|4|8|Growing different crops in an area
Q6(b)(ii)|12|4|8|breaks pest cycle
Q6(c)(i)|8|4|8|cuticle/ upper epidermis/ palisade
Q6(c)(ii)|8|4|8|Flat shape - exposure to more light
Q7(a)|12|4|9|Alternative form of a gene
Q7(b)(i)|4|4|9|(i) wwLS
Q7(b)(ii)|4|4|9|(ii) wwSS
Q7(b)(iii)|8|4|9|WwLS
Q7(b)(iv)|12|4|9|or 37.5%
Q7(c)|8|4|9|More heifer calves/ expand the herd
Q8(a)(i)|8|5|10|tilling operation/ hand weeding
Q8(a)(ii)|8|5|10|biological control (example given
Q8(a)(iii)|8|5|10|resistant varieties/ burn/ remove infected
Q8(b)(i)|8|5|10|absorbs CO2 from air
Q8(b)(ii)|4|5|10|6CO2 + 6H2O
Q8(b)(iii)|12|5|10|Fossil fuels to CO2
Q8(c)|24|5|10|Clostridium spp./ lameness
Q9(a)|12|5|11|Eat less/ smaller/ higher solids
Q9(b)|12|5|11|high in protein/ good digestibility
Q9(c)|12|5|11|Is a method of rapidly multiplying
Q9(d)|12|5|11|Break crust/ stop crust forming
Q9(e)|12|5|11|Not enough protein in diet
'''
POOLS_2013_HIGHER = {'Q2(c)': (1, ['Universal indicator', 'pH meter'])}
# 2013 Ordinary (legacy syllabus), transcribed from the SEC paper and scheme.
ORDINARY_2013 = '''
Q1|20|2|5|Caused by mange mite
Q2|20|3|5|Breaking large clods
Q3|20|4|5|Kerr Pink/ Rooster
Q4|20|4|6|Question 4.
Q5|20|5|6|Castration (of male animals)
Q6|20|6|6|Produces both milk and beef
Q7|20|7|6|Excludes air/ provides anaerobic conditions
Q8(a)(i)|6|8|7|Wheat/ Oats/ Maize
Q8(a)(ii)|6|8|7|Animal feed/ concentrates/ malting
Q8(b)(i)|4|8|7|(Sandy) loam/ good drainage
Q8(b)(ii)|4|8|7|February – April
Q8(b)(iii)|4|8|7|Spraying/ herbicide/ rotation/ pulling
Q8(b)(iv)|4|8|7|Combine harvester/ one sign of ripeness
Q8(c)|12|8|7|True to type/ (minimum) purity
Q8(d)|20|8|7|Seeds/ count/ soak (for 24 hours)
Q9(a)(i)|6|8|8|Landrace/ Large White/ Duroc
Q9(a)(ii)|8|8|8|Good conformation/ long body
Q9(b)|8|8|8|Teeth clipping/ tail docking
Q9(c)(i)|9|8|8|sows fed on (sow) ration
Q9(c)(ii)|9|8|8|grouped by size/ fattener ration
Q9(d)(i)|5|8|8|Amount of feed needed or eaten
Q9(d)(ii)|5|8|8|(Young) female pig that has not yet farrowed
Q9(d)(iii)|5|8|8|Holds sow during farrowing
Q9(d)(iv)|5|8|8|Treatment to prevent lice infection
Q10(a)(i)|8|9|9|Hereford/ Aberdeen Angus
Q10(a)(ii)|12|9|9|Smaller/ hardier/ ease of calving
Q10(b)(i)|4|9|9|200 - 230 kg
Q10(b)(ii)|4|9|9|470 - 490 kg
Q10(b)(iii)|4|9|9|550-750 kg
Q10(c)|16|9|9|Housed in October-November
Q10(d)|12|9|9|Moderate feeding level in winter
Q11(a)(i)|4|9|10|Segmented body/ triploblastic
Q11(a)(ii)|9|9|10|Improve drainage/ improve aeration/ mix soil
Q11(a)(iii)|15|9|10|Mark out area/ quadrat/ random
Q11(b)(i)|9|9|10|Parent material/climate
Q11(b)(ii)|8|9|10|Deep O horizon
Q11(c)(i)|3|9|10|Raises soil pH/ reduces soil acidity
Q11(c)(ii)|4|9|10|Causes soil particles to clump together
Q11(d)|8|9|10|Increases organic matter content
Q12(a)(i)|6|10|11|Recording of the characteristics
Q12(a)(ii)|6|10|11|Increased performance/ increased growth rates
Q12(b)(i)|10|10|11|Cytoplasm
Q12(b)(ii)|3|10|11|Nucleus / B
Q12(b)(iii)|3|10|11|Contain the genes
Q12(c)(i)|8|10|11|Gametes:
Q12(c)(ii)|4|10|11|Genotype F1:
Q12(c)(iii)|4|10|11|Phenotype F1:
Q12(d)|16|10|11|Genotype of offspring:
Q13(a)(i)|8|11|12|(Sitka) spruce
Q13(a)(ii)|6|11|12|Select healthy plants/ fence off land
Q13(a)(iii)|8|11|12|Reduces competition/ improves growth of trees
Q13(a)(iv)|8|11|12|Removes poorer trees/ increased space
Q13(b)(i)|16|11|12|Meadow foxtail.
Q13(b)(ii)|6|11|12|(red or white) clover. Any two
Q13(b)(iii)|8|11|12|Persistent/ high productivity
Q13(c)(i)|18|11|13|Ewes on bare pasture
Q13(c)(ii)|3|11|13|Blow fly or green bottle
Q13(c)(iii)|9|11|13|Dipping/ pour-on/ spray
Q13(d)(i)|15|11|13|Award full marks if diagram shows trachea
Q13(d)(ii)|3|11|13|Good ventilation/ vaccination/ house only when dry
Q13(d)(iii)|9|11|13|Adult worm in lungs
Q13(d)(iv)|3|11|13|Dosing/ leader- follower system/ vaccination
'''
POOLS_2013_ORDINARY = {'Q13(b)(iii)': (1, ['PRG', 'IRG', 'Clover'])}
# 2012 Ordinary (legacy syllabus), transcribed from the SEC paper and scheme.
ORDINARY_2012 = '''
Q1|20|2|5|Bacteria/ rhizobium
Q2|20|3|5|Arthropoda.
Q3|20|3|5|Question Three.
Q4|20|4|6|Compacts soil/ covers seed
Q5|20|4|6|Above lungs/ in the neck
Q6|20|5|6|Male part of flowers.
Q7|20|5|6|Prevents damage to sow
Q8(a)(i)|9|6|7|Suffolk/ Texel/ Galway
Q8(a)(ii)|6|6|7|Blowfly or maggots or flystrike
Q8(b)(i)|9|6|7|Easier supervision or easier management
Q8(b)(ii)|16|6|7|Ewes on bare pasture/ moved to good pasture
Q8(c)(i)|16|6|7|Colostrum / ewe
Q8(c)(ii)|4|6|7|40-50 kg
Q9(a)(i)|8|6|8|Kerrs Pink/ Rooster
Q9(a)(ii)|20|6|8|Plough/ rotavate or harrow
Q9(b)(i)|8|6|8|Reduced frost risk in south and east
Q9(b)(ii)|8|6|8|Prevents pests/ prevents diseases
Q9(c)|16|6|8|Weigh dish/ cut potatoes
Q10(a)(i)|6|7|9|Holstein/ Friesian/ Jersey
Q10(a)(ii)|6|7|9|Hereford/ Aberdeen Angus/ Charolais
Q10(b)|24|7|9|282 days
Q10(c)|16|7|9|Remove mucus/ iodine on navel
Q10(d)|8|7|9|Clean housing/ clean parlour
Q11(a)|6|7|10|PRG / IRG/ Cocksfoot
Q11(b)(i)|6|7|10|Growth of side-shoot
Q11(b)(ii)|8|7|10|Damage to main stem
Q11(c)|24|7|10|Land divided
Q11(d)|16|7|10|Dehydration or drying or removal of water
Q12(a)(i)|12|8|11|Well ventilated/ free from draughts
Q12(a)(ii)|8|8|11|Weight at first winter
Q12(a)(iii)|10|8|11|Muscle distribution
Q12(b)(i)|6|8|11|Amount or percentage of sand, silt and clay
Q12(b)(ii)|12|8|11|Good drainage/ good aeration/light
Q12(b)(iii)|12|8|11|Oven dry sample/ crush sample
Q12(c)(i)|6|8|12|An animal whose stomach consists of 4 compartments
Q12(c)(ii)|14|8|12|Rumen or paunch
Q12(c)(iii)|6|8|12|Breakdown of cellulose
Q12(c)(iv)|4|8|12|C / abomasum/ true stomach
Q12(d)(i)|6|8|12|Prevents crushing/ easy suckling
Q12(d)(ii)|6|8|12|Calves access to meal only
Q12(d)(iii)|6|8|12|Attractive/ biodiversity
Q12(d)(iv)|6|8|12|Powdery mildew/ fungus
Q12(d)(v)|6|8|12|Mud snail or secondary host
Q13(a)|16|9|13|Two sets of chromosomes
Q13(b)(i)|8|9|13|Gametes (R)
Q13(b)(ii)|4|9|13|F1 genotype (Rr)
Q13(b)(iii)|4|9|13|F1 phenotype round
Q13(c)|14|9|13|Genotypes of parents (rr)
Q13(d)|14|9|13|Easy to keep/ large no of offspring
'''
POOLS_2012_ORDINARY = {'Q10(c)': (1, ['Calf rearing', 'Rearing replacement heifer']), 'Q12(b)(iii)': (1, ['Sieve method', 'Sedimentation method', 'Feel method'])}
MODERN_POOLS = {(2026,'higher'):POOLS_2026_HIGHER, (2026,'ordinary'):POOLS_2026_ORDINARY, (2025,'higher'):POOLS_2025_HIGHER, (2025,'ordinary'):POOLS_2025_ORDINARY, (2024,'higher'):POOLS_2024_HIGHER, (2024,'ordinary'):POOLS_2024_ORDINARY, (2023,'higher'):POOLS_2023_HIGHER, (2023,'ordinary'):POOLS_2023_ORDINARY, (2022,'higher'):POOLS_2022_HIGHER, (2022,'ordinary'):POOLS_2022_ORDINARY, (2021,'higher'):POOLS_2021_HIGHER, (2021,'ordinary'):POOLS_2021_ORDINARY, (2020,'higher'):POOLS_2020_HIGHER, (2020,'ordinary'):POOLS_2020_ORDINARY, (2019,'higher'):POOLS_2019_HIGHER, (2019,'ordinary'):POOLS_2019_ORDINARY, (2018,'higher'):POOLS_2018_HIGHER, (2018,'ordinary'):POOLS_2018_ORDINARY, (2017,'higher'):POOLS_2017_HIGHER, (2017,'ordinary'):POOLS_2017_ORDINARY, (2016,'higher'):POOLS_2016_HIGHER, (2016,'ordinary'):POOLS_2016_ORDINARY, (2015,'higher'):POOLS_2015_HIGHER, (2015,'ordinary'):POOLS_2015_ORDINARY, (2014,'higher'):POOLS_2014_HIGHER, (2014,'ordinary'):POOLS_2014_ORDINARY, (2013,'higher'):POOLS_2013_HIGHER, (2013,'ordinary'):POOLS_2013_ORDINARY, (2012,'ordinary'):POOLS_2012_ORDINARY}

SOURCES = [
    (2012, 'ordinary', 'G', ORDINARY_2012,
     'ca9b4547982ff4a881b82f3930596bccf39345b57e8367461935a729435c12fb',
     '1a0dcbbdd3eed489d6adc380071d68897599fc0d272f4e7dccd5ef83b61316dd'),
    (2013, 'ordinary', 'G', ORDINARY_2013,
     '4681992b7ebd6dc0340ad28122b85dd60f0caf6642481bb1a0f9a123b257d249',
     '35f8630e40044a6434575a758b2e2c26550dedc5dc57020583113b833ab16c79'),
    (2013, 'higher', 'A', HIGHER_2013,
     'd238ab2a28d168a1fe5bbf3c6f47d423964d41bd0d88808e0f82d0bb0402c3d5',
     '031445761b0665780e95b48adc979647bb79153e77c2b75a061e92de59b4a56b'),
    (2014, 'ordinary', 'G', ORDINARY_2014,
     '9b45f4d47b5ce5deb0c1d70a46aea8093f17b3bd9460f05b9a2e04f6a6529958',
     '19a6b5e1223a5cbd18178276d5c8a02ef7147cb85c419a61c081158d7823617a'),
    (2014, 'higher', 'A', HIGHER_2014,
     'c69165b7f74f3a6bd4f5d73343243a1a90ca27c5fa12c9097a0eb11cb8930d85',
     '555f4e5c9084b028cb3281d987f7c4712f78bc1ce46fb5d83a511351e48d2e09'),
    (2015, 'ordinary', 'G', ORDINARY_2015,
     '9b807c836452b0b7fccef5d621b7c808374f284bd4b69236f34ca1a7b5d43ba7',
     'b39d01b60b7f6bfb66d583e5f0f297b49ec018e1860ce7e8d52f5715b638eefa'),
    (2015, 'higher', 'A', HIGHER_2015,
     'd9f65036e827e5b6de193ee0c5a0d825b16ef7e83d3a1698684f82aa6a95304c',
     '59811aee15e026a6bb6013e29d71fc851e71809ae7dc2ef0e96e79fd35cfe5c7'),
    (2016, 'ordinary', 'G', ORDINARY_2016,
     '688b5ed62a73c3b3d1bd877428c18f4843cb071a8b99d1580bd493f101901b38',
     '2490229e979602112b9af92d4f48677e28ab1c4b7f794ee5e730bc5cb6068473'),
    (2016, 'higher', 'A', HIGHER_2016,
     '0d0d58001042c543419ee3edc4acb58c9179f901acee5f8573ae9ae4949b12cd',
     '38b7cf5f6e4504c17f6dd8b6f70dbad197a3c4fe7079e848221750f51eb34502'),
    (2017, 'ordinary', 'G', ORDINARY_2017,
     'ae9d18e016bfddf1e6b24436b60061e647eff4cf954d1e6c63d8a3c236315310',
     '14128fb6c59bd93ed27f29e4ca4f92bddc94ac805206c25eeeaf45c4e58bc443'),
    (2017, 'higher', 'A', HIGHER_2017,
     'f8f371d593303ab2cf6b5ebb216be59009e8b2e90f54e1ddafd85e033efe3fe6',
     'b58e95e957390478fb1eb0654b95b8b1cea59c5cbbefd8871ea5b43266c0ad40'),
    (2018, 'ordinary', 'G', ORDINARY_2018,
     'e5eea810b3bab1e6eaed810445c4bba5c5f82bc82c2ea6749813e9edba0b5092',
     '026ce005742b5f959b269c48e7339ac770d3c9227d6f01cc741b29d9020bd932'),
    (2018, 'higher', 'A', HIGHER_2018,
     'c3f4587b9485b694119190e30e5cae7d3ca80f7879252ba1de545f4a6b99e785',
     '8872670e2cb5e7a56f3894429919359a95db6f9eb34acd36f475418d6c8937de'),
    (2019, 'ordinary', 'G', ORDINARY_2019,
     'd5978d8b8f4ce76f7cafcd14c6be9f7072aef3e0335f12ea1ec1e9d76429b3d8',
     '80e7534cdefcbe5d0d7921ed0ffb5041c5628cce01e910b4c75ab55ba8ef9ca0'),
    (2019, 'higher', 'A', HIGHER_2019,
     '2afa8bbcd1d0c6a2f00808e35eb08dec57f7a078c88a1665c827320b9d273f75',
     '7514b3e21ea16acc7f17e9089eb189576853ce75badcace2e8bd54a92adf08b4'),
    (2020, 'ordinary', 'G', ORDINARY_2020,
     'ad07041e0062736f05423d160ee9bd758976c40ef0911391cb78d06da487f247',
     'e54816cb1236808d572ec878c58e031ab2e533f9d8c4916b3d0fdc45cea99d8e'),
    (2020, 'higher', 'A', HIGHER_2020,
     '18ff9aba31b70f50fd65384ab901a9986a39dd43cc2651474263ed752c3016bb',
     'a82cef8f5c02ace6ac4049496bb08a65edad60ca08732e0ca01f2b727b2f76da'),
    (2021, 'ordinary', 'G', ORDINARY_2021,
     'e4cad5e9b9c5a3bd923da963916baebeaa7d49044bfb856434a318bd1755df59',
     'efec540781423841de14dfde99b9c751e7f04c6240e4f8db7fd8db9e0855ee8c'),
    (2021, 'higher', 'A', HIGHER_2021,
     'd60e656eff0863123d5c8152f114bcd323ed0cf81144676becf1f367c2b9d4e3',
     '6a1ad8c18dcabcd40f63f9b10f28ea23089a29bf4c34cd22ce097c8e988e99a8'),
    (2022, 'ordinary', 'G', ORDINARY_2022,
     '93a3be61e0ec5891f6ac6a2660fc1a98732fc9ff21a4b3c1e50681db1fe14194',
     'cb6dac4e3b45f824dfd75bf82443d62dc807fdbbf1e5406713be32e51c22e916'),
    (2022, 'higher', 'A', HIGHER_2022,
     '690cca40b2798863c397126cac71dc076d4fd3d6cb38395fee63c57625dc8f7f',
     '9e868b6c11ecf6bf71da03b8ced52b3be4aa80bbacb205b5fd418b555abd1a40'),
    (2023, 'ordinary', 'G', ORDINARY_2023,
     '98bdf03549315bcde81f97140f8d530f1081839c7aa7014c1ac8d00fda548510',
     '64da1086feec80a142d752edffcb6104de0a1cd162367ecca6ebdf5d7695b0b1'),
    (2023, 'higher', 'A', HIGHER_2023,
     '059f553f84ee5e11732cc00a8dedb3163785170a8c1b292ec234326ddeb6c118',
     '713384aadabd9a6e520dc5288f9047a929a4e43890e928ee7c957113c9d0581a'),
    (2024, 'ordinary', 'G', ORDINARY_2024,
     'dfdcb939847873c973368e2d59e01a1b9420a160d187398e4fed01131c273275',
     'b728e72363e7d7b7123f38884f637fcfad73adf2e32c6aaf57dce95eae52690e'),
    (2024, 'higher', 'A', HIGHER_2024,
     '6dce8f33e8e14be906d7d48b0585be29982238a2579ab0d1ac1cadb2a2f0cd84',
     'a3ae68c8d965d958bc13054ef527ddf64d8f8991053859aae5b4823d69b3f225'),
    (2025, 'ordinary', 'G', ORDINARY_2025,
     '481fbf4a01b2ed81472ad70745f47b2c413131939a6cc1b42cc1a16e40f458a7',
     'c2170cf98ba10073a7fa35497bc54ba039f807b1985bf616f5556cd57918e624'),
    (2025, 'higher', 'A', HIGHER_2025,
     '5d6ace875795ceeed7f7738b6c137a17f62e7247be067b540907afa71f9880f0',
     '47f040304b88a81e2c6de9783dc71914ac5863ea80416a280cf242c64014ba6d'),
    (2026, 'ordinary', 'G', ORDINARY_2026,
     'b63e7223ff6e0b724984b51db9b1813f37d19496570b7614694abc85f5702e2f',
     '5d408c95790f05c59a313f8b2e30ed789d36ddfbbe23da59474d5db79a7e1e8a'),
    (2026, 'higher', 'A', HIGHER_2026,
     '900dc33c639e740c3e50079caa34400ff62ada89418cc677142eec53335fd990',
     'efc3a2aa5656657aaec9364c23caf927f47078ecd622976e97b10628f8ecf6a6'),
    (2012, 'higher', 'A', HIGHER_2012,
     '9c36dd32194d49ccb00554ebfe7960cc6be0d95e4c2e3e26c9e60df5164b571d',
     'eb8f1a690343c38320680ed8425bdf0365e4ea1e4afe240d478026bf8909fdc1'),
    (2010, 'higher', 'A', HIGHER_2010,
               'fa917bba0b9350bb15cfe355789fa3002515bb6b28561f46ac47acfc1e7fa408',
               '120a5729e8e4d01ea5411df25c54e509c95ea099fb55cb52466f045c72909174'),
    (2010, 'ordinary', 'G', ORDINARY_2010,
                 '4ee8be5bf23d55308b3d08007dad8c0a181c2e7a6cad0e501c4385272fa7e6f0',
                 '42dbd3ca25728ba373226b63a9c1224137705d62fd62a8516faf261a76879ef6'),
    (2011, 'higher', 'A', HIGHER_2011,
     '19975eb5d04e868becd63819eb5a3325929f6c774cff8e6abd4b72a1d3fb4ed9',
     '9979d05e915b789dd55e9ac742066987f4b26c75820485b15b1436ed5d06e9ba'),
    (2011, 'ordinary', 'G', ORDINARY_2011,
     'b7b85bb61a0e55572f8d576f7ad7cdc45d7311496297cf37b8c4b146b5fba748',
     '3b7c1edf3a79a4862bf8fdb65d017c5b770c1b0d25c10df0bb8a22453280834f'),
]


def source_tasks():
    papers = []
    editions = [(*source,'ev') for source in SOURCES] + [(2011,'ordinary','G',ORDINARY_2011_IRISH,
        '0d32fbdb30e5d13ca15b792d48f6cfd9744869bc0d26099188548ebc77e51377',
        '79f95dcf8bcf49c50251496711d020ebcfd4c40bfba83720089e27f28258a837','iv')]
    for year,level,letter,table,paper_hash,scheme_hash,lang in editions:
        fileid = f'LC024{letter}LP000{lang.upper()}.pdf'
        pages = {}
        for kind,digest in [('exampapers',paper_hash),('markingschemes',scheme_hash)]:
            path = ROOT / f'paper-trail-corpus/{kind}/{year}/{fileid}'
            assert hashlib.sha256(path.read_bytes()).hexdigest()==digest, f'Source changed: {path}'
            with fitz.open(path) as pdf:
                pages[kind] = [' '.join(page.get_text().split()) for page in pdf]
        tasks = []
        for line in table.strip().splitlines():
            ref,marks,paper_page,scheme_page,cue = line.split('|')
            paper_page,scheme_page = int(paper_page),int(scheme_page)
            # The seedbed heading is on the paper; its scheme says plough,
            # remove stones, harrow, drills and separately prices it 2 + 4.
            kind,page = ('exampapers',paper_page) if cue=='Preparation of seedbed' else ('markingschemes',scheme_page)
            assert cue in pages[kind][page-1], f'Stale source cue: {level} {ref}: {cue}'
            routes = [ref]
            selection = {'kind':'none'}
            # A printed item choice is ONE practice card (coordinator rule,
            # 2026-10-12): the task keeps its closed pool but a single route.
            if year==2010 and level=='higher' and ref=='Q3 Option Two (b)':
                selection = {'kind':'closed','choose':1,'options':['Hoose','grass-tetany'],'pooled':True}
            elif ref in MODERN_POOLS.get((year,level),{}):
                choose,choices = MODERN_POOLS[(year,level)][ref]
                selection = {'kind':'closed','choose':choose,'options':choices,'pooled':True}
            elif year<2021 and level=='higher' and (ref=='Q8(c)' or year in (2010,2012) and ref=='Q7(a)'):
                selection = {'kind':'closed','choose':3,'options':['i','ii','iii','iv'],'pooled':True}
            tag = 'HL' if level=='higher' else 'OL'
            tasks.append({'ref':f'{year} {tag} {ref}','marksPerResponse':int(marks),
                          'paperPage':paper_page,'schemePage':scheme_page,
                          'sourceCue':{'kind':kind,'page':page,'text':cue},
                          'selection':selection,
                          'routes':[f'{year} {tag} {route}' for route in routes]})
        assert len(tasks)=={(2010,'higher'):55,(2010,'ordinary'):85,(2011,'higher'):67,(2011,'ordinary'):81,(2012,'higher'):56,(2026,'higher'):91,(2026,'ordinary'):85,(2025,'higher'):89,(2025,'ordinary'):91,(2024,'higher'):81,(2024,'ordinary'):82,(2023,'higher'):85,(2023,'ordinary'):81,(2022,'higher'):101,(2022,'ordinary'):98,(2021,'higher'):106,(2021,'ordinary'):113,(2020,'higher'):60,(2020,'ordinary'):52,(2019,'higher'):61,(2019,'ordinary'):54,(2018,'higher'):57,(2018,'ordinary'):60,(2017,'higher'):58,(2017,'ordinary'):71,(2016,'higher'):62,(2016,'ordinary'):69,(2015,'higher'):58,(2015,'ordinary'):63,(2014,'higher'):61,(2014,'ordinary'):61,(2013,'higher'):59,(2013,'ordinary'):62,(2012,'ordinary'):49}[(year,level)]
        papers.append({'year':year,'level':level,'lang':lang,'paperFileid':fileid,
                       'sourceHashes':{'exampapers':paper_hash,'markingschemes':scheme_hash},
                       'status':'boundary-reviewed','baseTasks':tasks})
    return papers


def build():
    papers = source_tasks()
    inventory = json.loads((ROOT / 'scripts/markbank/authored/agricultural-science-inventory.json').read_text())
    # All indexed editions remain visible; a reviewed English denominator does
    # not silently declare the Irish edition or another sitting complete.
    return {'subjectId':'agricultural-science','status':'in-progress',
            'method':'Independent English 2010 and 2011 Higher/Ordinary, English 2012 Higher, plus Irish 2011 Ordinary, paper/scheme boundary review with exact option and semantic-subtask addresses. Finite internal choices are expanded mechanically. Authored cards and their review ledger are not inputs.',
            'papers':papers,
            'boundaryRules':[
                'A diagram labelling exercise stays one task with all required labels and its figure; labels are answer fields, not printed alternative routes.',
                'A matching table can split into complete activity or disease tasks when each row has a published fixed award. Completed examples are not tasks.',
                'Pooled first-correct tariffs stay together: Higher Q1(e/f/g/j), Ordinary Q5 and Q7 must not allocate fixed marks to individual answer positions.',
                'Higher Q3 Option One and Option Two are distinct addresses. Q3 Option Two (b) has two common definitions and one disease task whose hoose and grass-tetany responses are mutually exclusive rows on one card.',
                'Higher Q7(a) and Q8(c) each print a closed three-of-four pool. A printed item choice is one practice card listing every item; it is never split into combination siblings.',
                'Exam choices between independently priced questions/parts do not combine unrelated tasks into extra practice identities.',
                'Ordinary Q3(a) identifies correct dairy breeds rather than choosing arbitrary pairs. Ordinary Q8(c) and Q9(c/e) are open methods/crops; accepted scheme examples are not a finite paper choice.',
                'Ordinary Q12(a)(iii) has inconsistent point-count wording: retain 18 marks and a non-automatic part-score. Q12(d) totals 28 in English versus 30 printed; disclose the discrepancy, never add fictitious marks.',
                '2011 Higher Q7(b): the shared cross receives 2+2 for parents and 8x1 for gametes; three separate offspring proportions receive four marks each. Never duplicate the shared 12 marks into each ratio task.',
                '2011 Higher Q7(a) requires each of three definitions, individually marked at four. Q8(c) alone has a closed three-of-four pool. Q6(c) preserves the 4/2/0 diagram band and four one-mark labels through manual total scoring.',
                '2011 Ordinary Q1–Q4 each have a pooled first-correct tariff across all answer fields and stay whole. Q5 and Q6 split at fixed row awards. Q10(a) is one dependent passage-completion exercise; its word bank is answer identification, not a route pool.',
                '2011 Ordinary Q10(d) has three separately specified soil samples, each with its own four-mark interpretation. Each task carries the common triangle and percentage table; these are independent cases rather than labels of one object.',
                '2011 Ordinary Q11(b/c) and Q12(a/c/d) permit open named insects, crops, animals and investigations. Scheme examples are not a finite question pool. Q11(c) sowing and harvesting each split at the separately published date/method awards.',
                '2011 Ordinary Q13(b) has separate eight-mark F1 and twenty-two-mark F2 completions. Q13(c) splits by its three required headings and printed one-mark asterisks: parents two, gametes three, offspring four. No shared award is repeated.',
            ],
            'inventoryEditionCount':len(inventory['papers']),
            'editionStatus':[
                {'year':p['year'],'level':p['level'],'lang':p['lang'],
                 'paperFileid':p['doc']['fileid'],
                 'independentCensus':'boundary-reviewed' if (p['year'],p['level'],p['lang']) in {(q['year'],q['level'],q['lang']) for q in papers} else 'open'}
                for p in inventory['papers']],
            'questionMarkChecks':question_mark_checks(papers)}


# Outer choices printed on the 2021+ papers, transcribed from each paper's own
# instructions. Section totals are the printed per-question marks.
MODERN_LAYOUTS = {
    (2026,'higher'): {'either':{'Q2','Q3','Q6','Q11'}, 'bothWithEither':{'Q14','Q16'},
                      'marks':lambda n: 10 if n<=12 else 50},
    (2026,'ordinary'): {'either':{'Q3','Q8','Q9','Q12'}, 'bothWithEither':{'Q15','Q16'},
                        'marks':lambda n: 10 if n<=12 else 50},
    (2025,'higher'): {'either':{'Q2','Q3','Q4','Q9'}, 'bothWithEither':{'Q13','Q14'},
                      'marks':lambda n: 10 if n<=12 else 50},
    (2025,'ordinary'): {'either':{'Q1','Q9','Q11','Q12'}, 'bothWithEither':{'Q15','Q17'},
                        'marks':lambda n: 10 if n<=12 else 50},
    (2021,'ordinary'): {'either':{'Q1','Q3','Q8','Q11'}, 'bothWithEither':{'Q16','Q18'},
                        'marks':lambda n: 10 if n<=12 else 50},
    (2021,'higher'): {'either':{'Q2','Q3','Q6','Q11'}, 'bothWithEither':{'Q16'}, 'oneWithEither':{'Q13'},
                      'marks':lambda n: 10 if n<=12 else 50},
    (2022,'ordinary'): {'either':{'Q2','Q4','Q7','Q11'}, 'bothWithEither':{'Q16'}, 'oneWithEither':{'Q13'},
                        'marks':lambda n: 10 if n<=12 else 50},
    (2022,'higher'): {'either':{'Q1','Q9','Q11','Q12'}, 'bothWithEither':{'Q14','Q17'},
                      'marks':lambda n: 10 if n<=12 else 50},
    (2023,'ordinary'): {'either':{'Q6','Q8','Q9','Q10'}, 'bothWithEither':{'Q13'}, 'oneWithEither':{'Q15'},
                        'marks':lambda n: 10 if n<=12 else 50},
    (2023,'higher'): {'either':{'Q1','Q7','Q9','Q10'}, 'bothWithEither':{'Q13','Q16'},
                      'marks':lambda n: 10 if n<=12 else 50},
    (2024,'ordinary'): {'either':{'Q2','Q6','Q9','Q11'}, 'bothWithEither':{'Q15','Q18'},
                        'marks':lambda n: 10 if n<=12 else 50},
    (2024,'higher'): {'either':{'Q2','Q3','Q6','Q9'}, 'bothWithEither':{'Q13','Q14'},
                      'marks':lambda n: 10 if n<=12 else 50,
                      'exceptions':{'Q18':(54,'The published allocations for Q18 total 54, not the printed 50: (a) 4 + (6+2) + (6+2) = 20, (b) 4 + (6+2) + 3(2) = 18, (c) 6+6+4 = 16. Preserve the scheme and disclose the difference.')}},
}


def modern_question_check(paper,question,tasks,layout):
    units = {}
    for task in tasks:
        letter = re.search(r'Q\d+(\([a-z]\))?',task['ref'].split(' ',2)[2]).group(1) or 'all'
        units[letter] = units.get(letter,0)+task['marksPerResponse']
    if question in layout['either']:
        assert sorted(units)==['(a)','(b)'], (question,units)
        totals, rule = sorted(set(units.values())), 'either (a) or (b)'
    elif question in layout['bothWithEither']:
        assert sorted(units)==['(a)','(b)','(c)','(d)'], (question,units)
        totals = sorted({units['(a)']+units['(b)']+units[x] for x in ['(c)','(d)']})
        rule = 'both (a) and (b) with either (c) or (d)'
    elif question in layout.get('oneWithEither',()):
        assert sorted(units)==['(a)','(b)','(c)'], (question,units)
        totals = sorted({units['(a)']+units[x] for x in ['(b)','(c)']})
        rule = '(a) with either (b) or (c)'
    else:
        totals, rule = [sum(units.values())], 'all parts'
    expected = layout['marks'](int(question[1:]))
    published, exception = layout.get('exceptions',{}).get(question,(expected,None))
    assert totals==[published], (paper['year'],paper['level'],question,units,totals)
    return {'year':paper['year'],'level':paper['level'],'lang':paper['lang'],'question':question,'units':units,
            'rule':rule,'candidateTotalsFromScheme':totals,'printedQuestionMarks':expected,'sourceException':exception}


def question_mark_checks(papers):
    """Candidate budgets collapse routes, then apply the printed outer choice.

    These totals use the independently transcribed boundaries above. They do
    not sum every alternative card as though one candidate answered them all.
    """
    checks = []
    for paper in papers:
        groups = {}
        higher = paper['level']=='higher'
        for task in paper['baseTasks']:
            address = task['ref'].split(' ',2)[2]
            question = re.match(r'Q\d+(?: Option (?:One|Two))?',address).group()
            groups.setdefault(question,[]).append(task)
        modern = MODERN_LAYOUTS.get((paper['year'],paper['level']))
        for question,tasks in groups.items():
            if modern:
                checks.append(modern_question_check(paper,question,tasks,modern))
                continue
            units = {}
            choose = None
            if higher and question in ['Q1','Q4','Q8','Q9']:
                choose = {'Q1':6,'Q4':2,'Q8':2,'Q9':4}[question]
            elif not higher and question==OL_PART_CHOICE.get(paper['year'],'Q12'):
                choose = 2
            for task in tasks:
                unit = re.search(r'Q\d+(\([a-z]\))',task['ref']).group(1) if choose else 'all'
                units[unit] = units.get(unit,0)+task['marksPerResponse']
            totals = sorted({sum(values) for values in itertools.combinations(units.values(),choose or 1)})
            expected = (60 if question=='Q1' else 48) if higher else (20 if int(question[1:])<=7 else 60)
            discrepancy = paper['year']==2010 and paper['lang']=='ev' and not higher and question=='Q12'
            assert totals==([58,60] if discrepancy else [expected]), (paper['level'],question,totals)
            checks.append({'year':paper['year'],'level':paper['level'],'lang':paper['lang'],
                           'question':question,'units':units,'choose':choose or 1,
                           'candidateTotalsFromScheme':totals,'printedQuestionMarks':expected,
                           'sourceException':'English Q12(d) totals 28, not the printed 30; selecting it gives 58. Preserve the scheme and disclose the difference.' if discrepancy else None})
    return checks


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--write',action='store_true')
    parser.add_argument('--check',action='store_true')
    args = parser.parse_args()
    data = build()
    if args.write:
        OUTPUT.write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n')
    elif args.check:
        assert json.loads(OUTPUT.read_text())==data, 'Independent census stale'
    print('Source census (one card per base task; printed item choices are single cards): 2010 Higher 55; 2010 Ordinary 85; 2011 Higher 67; 2011 Ordinary English 81; 2011 Ordinary Irish 81; 2012 Higher 56; 2026 Higher 91; 2026 Ordinary 85; 2025 Higher 89; 2025 Ordinary 91; 2024 Higher 81; 2024 Ordinary 82; 2023 Higher 85; 2023 Ordinary 81; 2022 Higher 101; 2022 Ordinary 98; 2021 Higher 106; 2021 Ordinary 113; 2020 Higher 60; 2020 Ordinary 52; 2019 Higher 61; 2019 Ordinary 54; 2018 Higher 57; 2018 Ordinary 60; 2017 Higher 58; 2017 Ordinary 71; 2016 Higher 62; 2016 Ordinary 69; 2015 Higher 58; 2015 Ordinary 63; 2014 Higher 61; 2014 Ordinary 61; 2013 Higher 59; 2013 Ordinary 62; 2012 Ordinary 49. Remaining editions stay open.')


if __name__=='__main__':
    main()
