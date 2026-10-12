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

MODERN_POOLS = {(2026,'higher'):POOLS_2026_HIGHER, (2026,'ordinary'):POOLS_2026_ORDINARY, (2025,'higher'):POOLS_2025_HIGHER, (2025,'ordinary'):POOLS_2025_ORDINARY, (2024,'higher'):POOLS_2024_HIGHER}

SOURCES = [
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
            if year==2010 and level=='higher' and ref=='Q3 Option Two (b)':
                routes = [ref+' — Hoose',ref+' — grass-tetany']
                selection = {'kind':'closed','choose':1,'options':['Hoose','grass-tetany']}
            elif ref in MODERN_POOLS.get((year,level),{}):
                choose,choices = MODERN_POOLS[(year,level)][ref]
                routes = [ref+' — '+', '.join(parts) for parts in itertools.combinations(choices,choose)]
                selection = {'kind':'closed','choose':choose,'options':choices}
            elif year<2021 and level=='higher' and (ref=='Q8(c)' or year in (2010,2012) and ref=='Q7(a)'):
                choices = ['i','ii','iii','iv']
                routes = [ref+' — '+', '.join(parts) for parts in itertools.combinations(choices,3)]
                selection = {'kind':'closed','choose':3,'options':choices}
            tag = 'HL' if level=='higher' else 'OL'
            tasks.append({'ref':f'{year} {tag} {ref}','marksPerResponse':int(marks),
                          'paperPage':paper_page,'schemePage':scheme_page,
                          'sourceCue':{'kind':kind,'page':page,'text':cue},
                          'selection':selection,
                          'routes':[f'{year} {tag} {route}' for route in routes]})
        assert len(tasks)=={(2010,'higher'):55,(2010,'ordinary'):85,(2011,'higher'):67,(2011,'ordinary'):81,(2012,'higher'):56,(2026,'higher'):91,(2026,'ordinary'):85,(2025,'higher'):89,(2025,'ordinary'):91,(2024,'higher'):81}[(year,level)]
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
                'Higher Q3 Option One and Option Two are distinct addresses. Q3 Option Two (b) has two common definitions and two alternative disease responses.',
                'Higher Q7(a) and Q8(c) each print a closed three-of-four pool. Each complete three-item response is one route.',
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
            elif not higher and question=='Q12':
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
    print('Source census: 2010 Higher 55 base tasks / 62 routes; 2010 Ordinary 85; 2011 Higher 67 / 70; 2011 Ordinary English 81; 2011 Ordinary Irish 81; 2012 Higher 56 / 62; 2026 Higher 91 / 112; 2026 Ordinary 85 / 114; 2025 Higher 89 / 112; 2025 Ordinary 91 / 99; 2024 Higher 81 / 91. Remaining editions stay open.')


if __name__=='__main__':
    main()
