"""Physics 2019 Higher — source-reviewed task ledger.

All 12 paper pages and all 24 scheme pages visually inspected on 2026-10-31.
Most asks are unnumbered. Descriptive item suffixes distinguish independently
marked tasks without inventing printed part numbers. The numbered roman
sub-asks keep the paper's numbering, including repeated (i)/(ii) in Q12(b).
Every optional branch is retained; Q5 best-eight and Q12 best-two choices
remain visible in the source evidence. No Irish editions are in this scope.

The scheme's Cambria glyph IDs repeat the verified 2020 font; each additional
mathematical letter was checked against its rendered first occurrence. Stacked
fractions and nuclides are lifted geometrically, never guessed from linear OCR.
"""
from phys_review_lib import Q, SQ, S, M, G, pt, anyn, T
YEAR, LEVEL = 2019, 'hl'
REVIEWED_AT = '2026-10-31'
LETTERED = {5, 9, 11, 12}
SOURCES = {
 'paper': {'path':'examiner-reports/physics/papers/2019-hl-paper.pdf','fileid':'LC021ALP000EV.pdf',
           'sha256':'8c3dc1203ad17cc96558b9911695a8c921656745c1fdf0cb27828a7d0a90295f','pages':12},
 'scheme': {'path':'examiner-reports/physics/schemes/2019-hl.pdf','fileid':'LC021ALP000EV.pdf',
            'sha256':'9f966f25ff366a276b7281bfda2b2e93231fb7a6d1abc9a831c26715355bf0b3','pages':24},
}
PAGE_ROLES = {
 'paper': {1:'cover', **{p:'questions' for p in range(2,12)},12:'back-cover'},
 'scheme': {1:'cover',2:'note',3:'conventions',4:'annotations',5:'irish-language-bonus-instructions',
            **{p:'marking' for p in range(6,21)},**{p:'blank' for p in range(21,24)},24:'back-cover'},
}
GLYPHS = {'scheme': {'Cambria': {1788: 'N',
                        1803: 'c',
                        1807: 'g',
                        1809: 'i',
                        1811: 'k',
                        1812: 'l',
                        1813: 'm',
                        1814: 'n',
                        1815: 'o',
                        1818: 'r',
                        1819: 's',
                        1861: 'i',
                        1870: 'r',
                        2157: 'A',
                        2159: 'C',
                        2161: 'E',
                        2162: 'F',
                        2163: 'G',
                        2164: 'H',
                        2165: 'I',
                        2169: 'M',
                        2170: 'N',
                        2172: 'P',
                        2173: 'Q',
                        2174: 'R',
                        2176: 'T',
                        2177: 'U',
                        2178: 'V',
                        2183: 'a',
                        2184: 'b',
                        2185: 'c',
                        2186: 'd',
                        2187: 'e',
                        2188: 'f',
                        2190: 'h',
                        2191: 'i',
                        2193: 'k',
                        2194: 'l',
                        2195: 'm',
                        2196: 'n',
                        2197: 'o',
                        2198: 'p',
                        2200: 'r',
                        2201: 's',
                        2202: 't',
                        2203: 'u',
                        2204: 'v',
                        2206: 'x',
                        2207: 'y',
                        2237: 'γ',
                        2242: 'θ',
                        2246: 'μ',
                        2250: 'π',
                        2251: 'ρ',
                        2261: 'ϵ',
                        2743: 'Ω',
                        2777: '0',
                        2778: '1',
                        2779: '2',
                        2780: '3',
                        2781: '4',
                        2782: '5',
                        2783: '6',
                        2784: '7',
                        2785: '8',
                        2786: '9',
                        3406: '≈',
                        3415: '/',
                        3495: '√',
                        2189: 'g',
                        2205: 'w',
                        2179: 'W',
                        2259: 'ω',
                        2199: 'q',
                        2158: 'B',
                        1820: 't',
                        1801: 'a',
                        2171: 'O',
                        2180: 'X',
                        2182: 'Z',
                        1784: 'J'}},
 'paper': {'SymbolMT': {83: 'π'}}}
VERIFIED_LINES = []
QUESTION_TOTALS = {**{n:40 for n in range(1,5)},**{n:56 for n in range(5,12)},12:140}
# Q12(d) offers two distinct 28-mark routes, each retained, so authored Q12 totals 140.
PART_TOTALS = {(9,'a'):18,(9,'b'):21,(9,'c'):17,
               **{(11,x):7 for x in 'abcde'},(11,'f'):21,
               **{(12,x):28 for x in 'abc'},(12,'d'):56}
BEST_OF = {5:(8,7)}
GROUP_TOTALS = {}
CHECKSUMS = {}
ROUTES = {'Q5(j)':['neutrinos','ammeter']}
SCAN_PAGES = {'paper':range(2,12)}
SELECTION_SCAN = [
 ('paper',2,'the following','Q1 recorded data table, retained.'),
 ('paper',2,'the following','Q2 recorded data table, retained.'),
 ('paper',3,'the following','Q3 recorded measurements, retained.'),
 ('paper',3,'the following','Q4 recorded data table, retained.'),
 ('paper',4,'the following','Q5 answer any eight: all ten parts retained; BEST_OF counts eight.'),
 ('paper',4,'or','Q5(j) neutrino and ammeter alternatives: both carded as routes.'),
 ('paper',5,'both','Q6 satellite description: visible and infrared images, not candidate selection.'),
 ('paper',5,'or','Q6 asks which wavelength is longer: one comparison.'),
 ('paper',7,'both','Q9 lead-in describes two experiences of magnetic force.'),
 ('paper',7,'the following','Q9 recorded data table, retained.'),
 ('paper',9,'the following','Q11 source passage, retained in full.'),
 ('paper',9,'or','Q11 passage contrasts a.c. and d.c.; no candidate selection.'),
 ('paper',10,'any two','Q12 choose two lettered parts; every part and both d alternatives retained.'),
 ('paper',10,'the following','The same Q12 instruction.'),
 ('paper',11,'or','Q12(d)(i) particle physics or (ii) applied electricity: both 28-mark branches retained.'),
]
ASK_SCAN_PAGES = {'paper':range(2,12)}
ASK_EXEMPT = [
 (6,'When current is passed through the vapour in a sodium lamp,','A descriptive when-clause, not an ask; carried in both spectrum cards’ stems.'),
 (10,'A diver is 12 m below the surface in a pool of water.','The following when-clause describes the diver looking up; carried in the relevant cards’ stems.'),
]
SEC = 'State Examinations Commission'
CRIT = 'The scheme prints the marking criterion rather than a worked answer.'
DSL = 'The scheme’s // separates complete alternative methods; do not mix partial answers across methods.'
P = Q

def R(text, marks, end=None, **kw):
    return pt(S(text,end),marks,**kw)

def C(text, marks, end=None, **kw):
    return pt(S(text,end),marks,kind='criterion',note=CRIT,**kw)

def FR(page,clip,expect,marks,**kw):
    return G('fraction',page=page,clip=clip,expect=expect,marks=marks,**kw)

def EQ(page,clip,expect,marks,**kw):
    return G('equation',page=page,clip=clip,expect=expect,marks=marks,**kw)

def pieces(sel,marks,sep):
    return [pt(dict(sel,piece=i+1,psep=sep),m) for i,m in enumerate(marks)]

TASKS=[]
def U(ref,slug,label,q,rows,topic,sq,total,**kw):
    TASKS.append(T(ref+':'+slug,ref,'A' if int(ref.split('(')[0][1:])<5 else 'B',
                   q,rows,topic,slug,sq,total,item=(slug,label),**kw))

STEM1=P(2,'In an experiment to determine the acceleration due to gravity','The following data were recorded.')
STEM2=P(2,'In an experiment to determine the focal length of a concave mirror','The following data were recorded.')
STEM3=P(3,'In an experiment to determine the specific latent heat of fusion of ice','calorimeter.')
DATA3=P(3,'(specific heat capacity of water = 4180 J kg⁻¹ K⁻¹, specific heat capacity of copper = 390 J kg⁻¹ K⁻¹)')
STEM4=P(3,'In an experiment to investigate the variation of current I with potential difference V','semiconductor diode the following data were recorded.')

# Section A: 25 separately priced tasks, all four 40-mark experiments.
U('Q1','apparatus','Apparatus',P(2,'Draw a labelled diagram of the apparatus used in the experiment.'),
  pieces(S('timer, ball and release mechanism, pressure plate'),[3,3,3],','),
  'phys-1-1',SQ(6,'Draw a labelled diagram of the apparatus used in the experiment.'),9,stem=[STEM1])
U('Q1','distance','Measuring distance',P(2,'Between which points was the distance s measured?'),
  [R('bottom of ball and (top of) pressure plate',3)],'phys-1-1',SQ(6,'Between which points was the distance s measured?'),3,stem=[STEM1])
U('Q1','time','Measuring time',P(2,'Describe how the time t was measured.'),
  [R('timer started when ball released and stopped when it hit plate',3)],'phys-1-1',SQ(6,'Describe how the time t was measured.'),3,stem=[STEM1])
U('Q1','graph','Graph',P(2,'Draw a suitable graph that can be used to determine the acceleration due to gravity g.'),
  [C('values for t² (–1 for each incorrect value)',3),C('labelled axes',3),C('points plotted (–1 for each incorrect point)',3),C('straight line of good fit',3)],
  'phys-1-1',SQ(6,'Draw a suitable graph that can be used to determine the acceleration due to gravity g.'),12,
  stem=[STEM1],qfig='q1-graph-question',fig='q1-squared-times')
U('Q1','gravity','Acceleration due to gravity',P(2,'Hence determine g.'),
  [FR(6,(70,517,406,546),'slope formula: (m=) (y₂−y₁)/(x₂−x₁) / correct substitution into slope formula',3),
   R('slope calculated: m≈5',3),R('acceleration due to gravity calculated: g≈10 m s⁻²',3)],
  'phys-1-1',SQ(6,'Hence determine g.'),9,stem=[STEM1,P(2,'Draw a suitable graph that can be used to determine the acceleration due to gravity g.')],fig='q1-data')
U('Q1','dense-ball','Small dense ball',P(2,'A small, dense ball was used as the object in this experiment.','of ball.'),
  [R('less air resistance',4)],'phys-1-1',SQ(6,'A small, dense ball was used as the object in this experiment.','of ball.'),4,stem=[STEM1])

U('Q2','approximation','Approximate focal length',P(2,'How did the student find the approximate focal length?'),
  [R('found image of a distant object',6)],'phys-2-3',SQ(7,'How did the student find the approximate focal length?'),6,stem=[STEM2])
U('Q2','starting-distance','Why find it first?',P(2,'Why did the student find the approximate focal length at the start of the experiment?'),
  [R('to ensure object was placed outside of focal point',6,'/ image formed on a screen / to compare with later answer')],
  'phys-2-3',SQ(7,'Why did the student find the approximate focal length at the start of the experiment?'),6,stem=[STEM2])
U('Q2','image-position','Finding the image',P(2,'Describe, with the aid of a labelled diagram, how the position of the image was found.'),
  [R('concave mirror, screen and object',3),C('correct arrangement',3),R('move screen (and/or object and/or mirror) until (sharpest) image is formed',3)],
  'phys-2-3',SQ(7,'Describe, with the aid of a labelled diagram, how the position of the image was found.'),9,stem=[STEM2],cells='Scheme p7 prices apparatus, arrangement and moving the screen at 3 each. The last (3) is embedded in the answer text object.')
U('Q2','precautions','Two precautions',P(2,'State two precautions that should be taken when measuring v.'),
  [anyn(S('error of parallax','sharp image formed'),2,None,steps=[4,2],sep=',')],
  'phys-2-3',SQ(7,'State two precautions that should be taken when measuring v.'),6,stem=[STEM2])
U('Q2','focal-length','Calculating focal length',P(2,'Use all of the data to calculate the focal length of the mirror.'),
  [FR(7,(69,455,120,483),'1/u + 1/v = 1/f',6),C('one correct substitution',3),
   anyn(S('three values of f from: 15.1, 14.9, 15.0, 14.5 (cm)',piece=2,psep='from:'),3,1,sep=','),R('correct average: 14.9 cm',1)],
  'phys-2-3',SQ(7,'Use all of the data to calculate the focal length of the mirror.'),13,stem=[STEM2],fig='q2-data')

# Inline printed romans share their leading words but each is separately priced.
WHY3=P(3,'Why did the student (i) crush the ice, (ii) dry the ice?')
HOW3=P(3,'How was the ice (iii) crushed, (iv) dried?')
WARM3=P(3,'Why did she (v) use warm water, (vi) use melting ice?')
for roman,question,anchor,answer,end in [
 ('i',[dict(WHY3,piece=1,psep=' (i)'),dict(WHY3,piece=[2,1],psep=[' (i)',', (ii)'])],
  SQ(8,'Why did the student (i) crush the.ice, (ii) dry the.ice?'),'to ensure it was all at the same temperature','/ so that it would melt faster / to give a greater surface area'),
 ('ii',[dict(WHY3,piece=1,psep=' (i)'),dict(WHY3,piece=2,psep=', (ii)')],
  SQ(8,'Why did the student (i) crush the.ice, (ii) dry the.ice?'),'to ensure that only ice was added to the calorimeter',None),
 ('iii',[dict(HOW3,piece=1,psep=' (iii)'),dict(HOW3,piece=[2,1],psep=[' (iii)',', (iv)'])],
  SQ(8,'How was the ice (iii) crushed, (iv) dried?'),'e.g ice crusher',None),
 ('iv',[dict(HOW3,piece=1,psep=' (iii)'),dict(HOW3,piece=2,psep=', (iv)')],
  SQ(8,'How was the ice (iii) crushed, (iv) dried?'),'using a towel',None),
 ('v',[dict(WARM3,piece=1,psep=' (v)'),dict(WARM3,piece=[2,1],psep=[' (v)',', (vi)'])],
  SQ(8,'Why did she (v) use warm water, (vi) use melting ice?'),'ice would melt more quickly / so that energy lost = energy gained',None),
 ('vi',[dict(WARM3,piece=1,psep=' (v)'),dict(WARM3,piece=2,psep=', (vi)')],
  SQ(8,'Why did she (v) use warm water, (vi) use melting ice?'),'to ensure that the ice was at 0°C',None),
]:
 TASKS.append(T('3'+roman,'Q3('+roman+')','A',question,[R(answer,3,end)],'phys-2-1','latent-heat-method-'+roman,anchor,3,stem=[STEM3]))
U('Q3','latent-heat','Specific latent heat',P(3,'Use the data to calculate the specific latent heat of fusion of ice.'),
  [*pieces(S('∆θi=8, ∆θw=21.5, mw=52.2'),[3,3,3],','),R('(∆E=)ml and (∆E=)mc∆θ',3),
   R('(14.4)li+(14.4)(4180)(8)=(56.3)(390)(21.5)+(52.2)(4180)(21.5)',3),R('l =3.25 ×10⁵ J Kg⁻¹',3)],
  'phys-2-1',SQ(8,'Use the data to calculate the specific latent heat of fusion of ice.'),18,stem=[STEM3,DATA3],fig='q3-data')
U('Q3','water-mass','Large mass of water',P(3,'Why could using a very large mass of water lead to a less accurate result in this experiment?'),
  [R('smaller change in temperature / greater percentage error',4)],'phys-2-1',SQ(8,'Why could using a very large mass of water lead to a less accurate result in this experiment?'),4,stem=[STEM3])

U('Q4','circuit','Circuit diagram',P(3,'Draw a circuit diagram for this experiment.'),
  [*pieces(S('source of varying voltage, diode, ammeter, voltmeter'),[3,3,3,3],','),C('correct arrangement',3)],
  'phys-3-3',SQ(9,'Draw a circuit diagram for this experiment.'),15,stem=[STEM4])
U('Q4','graph','Current–voltage graph',P(3,'Use the data to draw a graph of current against potential difference.'),
  [C('labelled axes',3),C('points plotted',3),C('curve of good fit',3)],'phys-3-3',SQ(9,'Use the data to draw a graph of current against potential difference.'),9,stem=[STEM4],fig='q4-data')
U('Q4','junction-voltage','Junction voltage',P(3,'Use your graph to determine the junction voltage.'),
  [R('≈ 0.2 V',3)],'phys-3-3',SQ(9,'Use your graph to determine the junction voltage.'),3,
  stem=[STEM4,P(3,'Use the data to draw a graph of current against potential difference.')],fig='q4-data')
U('Q4','conduction','Exceeding the junction voltage',P(3,'What happened in the diode when the junction voltage was exceeded?'),
  [R('depletion layer broke down / low resistance / current flows',3)],'phys-3-3',SQ(9,'What happened in the diode when the junction voltage was exceeded?'),3,stem=[STEM4])
U('Q4','ohms-law','Ohm’s law',P(3,'Is Ohm’s law obeyed for the diode? Justify your answer.'),
  [R('no',3),R('not a straight line through the origin',3)],'phys-3-3',SQ(9,'Is Ohm’s law obeyed for the diode? Justify your answer.'),6,stem=[STEM4],fig='q4-data')
U('Q4','reverse-bias','Reverse-bias changes',P(3,'The diode is now reversed and data is recorded.','circuit before recording data for a diode in reverse bias.'),
  [anyn(S('replace ammeter with a microammeter,','remove (protective) resistor if already included [any two]'),2,2,sep=',')],
  'phys-3-3',SQ(9,'The diode is now reversed and data is recorded.','circuit before recording data for a diode in reverse bias.'),4,stem=[STEM4])

FIGURES={
 'q1-data':('paper',2,(138,252,457,303),SEC,[],'Recorded distances s in cm and fall times t in ms.',False),
 'q1-graph-question':('paper',2,(52,188,543,403),SEC,[],'The falling-ball experiment, recorded data and graph task.',False),
 'q1-squared-times':('scheme',6,(127,338,468,388),SEC,[],'Scheme table: s in m and t squared in square seconds.',True),
 'q2-data':('paper',2,(190,587,405,639),SEC,[],'Recorded object distances u and image distances v in cm.',False),
 'q3-data':('paper',3,(80,133,478,248),SEC,[],'Calorimeter masses and temperatures before and after adding ice.',False),
 'q4-data':('paper',3,(138,477,458,529),SEC,[],'Diode potential difference V in mV and current I in mA.',False),
}

# Section B. Q5: every short part, including both alternatives of (j).
for ref,question,rows,topic,anchor,stem in [
 ('Q5(a)',P(4,'Calculate this distance in metres.'),[R('s=vt',3),R('s=(3.00×10⁸)(3.15×10⁷)',2),R('s=9.45×10¹⁵ (m)',2)],'phys-1-1',SQ(10,'Calculate this distance in metres.'),[P(4,'A light‐year is the distance travelled by light in a vacuum in one year.')]),
 ('Q5(b)',P(4,'Calculate the density of the apple.'),[R('W=mg / m = 0.102',3),FR(10,(98,165,135,191),'ρ= m/V',2),R('ρ=843 kg m⁻³',2)],'phys-1-2',SQ(10,'An apple has a weight of 1 N','Calculate the density of the apple.'),[P(4,'An apple has a weight of 1 N and its volume is 121 cm³.'),P(4,'(acceleration due to gravity = 9.8 m s⁻²)')]),
 ('Q5(c)',P(4,'Draw a labelled diagram to show the forces acting on the book','moves on the table.'),[R('force up',3,note_sel=S('(–1 for each incorrect force)')),R('(equal) force down',2),R('net horizontal force to the left',2)],'phys-1-2',SQ(10,'A book is decelerating','to show the forces acting on the book as it moves on the table.'),[P(4,'A book is decelerating as it moves to the right on a horizontal table.')]),
 ('Q5(d)',P(4,'What is meant by polarisation of light?'),[R('vibrating',4),R('in one plane',3)],'phys-2-3',SQ(10,'What is meant by polarisation of light?'),[]),
 ('Q5(e)',P(4,'What is the thermometric property of (i) a mercury thermometer, (ii) a thermocouple?'),[R('length/height/volume',4),R('emf/voltage',3)],'phys-2-1',SQ(10,'What is the thermometric property of (i) a mercury thermometer, (ii) a thermocouple?'),[]),
 ('Q5(f)',P(4,'Sketch a graph to show the relationship between resistance R and temperature T (in °C) for a','metallic conductor.'),[C('labelled axes',4),C('straight line (–1 if through origin)',3)],'phys-3-3',SQ(10,'Sketch a graph to show the relationship between resistance R and temperature T (in °C) for a','metallic conductor.'),[]),
 ('Q5(g)',P(4,'Power P is generated in a resistor of resistance R','across it. Write P in terms of R and V.'),[FR(10,(98,509,116,541),'V²/R',7,note_sel=S('(allow 4 marks for VI or I²R or V=IR)'))],'phys-3-3',SQ(10,'Power P is generated in a resistor of resistance R','across it. Write P in terms of R and V.'),[]),
 ('Q5(h)',P(4,'Polonium–218 has a half‐life of 3 minutes.','sample of polonium–218 that contains 75000 nuclei.'),[FR(10,(97,570,237,597),'λ= ln2/(T1/2) / λ=0.00385',3),R('A=λN / A=(0.00385)(75000)',2),R('A=289 Bq',2)],'phys-4-4',SQ(10,'Polonium was discovered by Marie and Pierre Curie in 1898.','3 minutes. Calculate the activity of a sample of polonium–218 that contains 75000 nuclei.'),[P(4,'Polonium was discovered by Marie and Pierre Curie in 1898.')]),
 ('Q5(i)',P(4,'Polonium–218 is produced as the daughter nucleus in the','alpha‐decay of radon–222. Write a nuclear equation for this reaction.'),[EQ(10,(98,662,220,686),'Rn²²²₈₆ → Po²¹⁸₈₄ + He⁴₂',7)],'phys-4-4',SQ(10,'Polonium–218 is produced as the daughter nucleus of the','a nuclear equation for this reaction.'),[]),
]:
 TASKS.append(T(ref,ref,'B',question,rows,topic,ref.lower().replace('(','-').replace(')',''),anchor,7,stem=stem))
TASKS.extend([
 T('5j-neutrinos','Q5(j)','B',P(4,'Neutrinos are sometimes called ghost particles.','hard to detect?'),
   [R('very small mass',4),R('no charge',3)],'phys-4-5','neutrino-detection',SQ(10,'Neutrinos are sometimes called ghost particles. Why are they very hard to detect?'),7,route='neutrinos'),
 T('5j-ammeter','Q5(j)','B',P(4,'Describe how a galvanometer can be converted into an ammeter.'),
   [R('small resistance',4),R('in parallel',3)],'phys-3-3','galvanometer-to-ammeter',SQ(10,'Describe how a galvanometer can be converted into an ammeter.'),7,route='ammeter'),
])

STEM6=P(5,'Satellites, which play an increasing role in the information age','of orbit.')
MET6=P(5,'The METEOSAT 11 weather satellite provides MET Éireann','orbit above the equator.')
GPS6=P(5,'A global positioning satellite is not in geostationary orbit.','It orbits the Earth with a speed of 14000 km hr⁻¹.')
DATA6=P(5,'(mass of Earth = 6.0 × 10²⁴ kg, radius of Earth = 6400 km)')
U('Q6','gravitation','Law of gravitation',P(5,'State Newton’s law of universal gravitation.'),
 [R('force is proportional to product of masses',3,route='words',note=DSL),R('force is inversely proportional to distance squared',3,route='words'),
  FR(11,(338,130,416,156),'// F=G m₁m₂/d²',3,route='formula'),pt(S('// notation',piece=2,psep='//'),3,kind='criterion',route='formula')],
 'phys-1-5',SQ(11,'State Newton’s law of universal gravitation.'),6,stem=[STEM6])
U('Q6','period-radius','Period and radius',P(5,'What is the relationship between the period T and radius of orbit r of a satellite?'),
 [R('T²∝ r³',3)],'phys-1-5',SQ(11,'What is the relationship between the period T and radius of orbit r of a satellite?'),3,stem=[STEM6],
 cells='Scheme p11 prints (3) on the same baseline as its Relationship? [3] summary, outside the answer cell.')
U('Q6','infrared-wavelength','Infrared wavelength',P(5,'Which has a longer wavelength, visible or infrared radiation?'),
 [R('infrared',3)],'phys-2-4',SQ(11,'Which has a longer wavelength, visible or infrared radiation?'),3,stem=[MET6])
U('Q6','infrared-detection','Detecting infrared',P(5,'Describe how infrared radiation can be detected in the school','laboratory.'),
 [R('heating effect / thermometer',6)],'phys-2-4',SQ(11,'Describe how infrared radiation can be detected in the school laboratory.'),6,stem=[MET6])
U('Q6','geostationary-period','Geostationary period',P(5,'What is the period of METEOSAT 11?'),
 [R('24 hours',6)],'phys-1-5',SQ(11,'What is the period of METEOSAT 11?'),6,stem=[MET6])
U('Q6','satellite-height','Satellite height',P(5,'Calculate its height above the surface of the Earth.'),
 [FR(11,(69,355,311,383),'T²= 4π²R³/(Gm) / (86400)²= 4π²R³/((6.67×10⁻¹¹)(6.0×10²⁴))',3),
 R('h= 3.596 × 10⁷ m / 36000 km',3,note_sel=S('(–1 if answer left as R= 4.236 × 10⁷ m / 42360 km)'))],
 'phys-1-5',SQ(11,'Calculate its height above the surface of the Earth.'),6,stem=[MET6,DATA6])
CALC6=P(5,'Calculate (i) its radius of orbit, (ii) its angular velocity.')
TASKS.extend([
 T('6i','Q6(i)','B',dict(CALC6,piece=1,psep=', (ii)'),
  [R('v = 3889 (m s⁻¹)',3),FR(11,(69,467,403,494),'v²= Gm/R / 3889²= ((6.67×10⁻¹¹)(6.0×10²⁴))/R / F=G m₁m₂/d² / F= mv²/R',3),R('R= 2.65 × 10⁷ m / 26500 km',3)],
  'phys-1-5','gps-radius',SQ(11,'Calculate (i) its radius of orbit,'),9,stem=[GPS6,DATA6]),
 T('6ii','Q6(ii)','B',[dict(CALC6,piece=1,psep=' (i)'),dict(CALC6,piece=2,psep=', (ii)')],
  [R('v=rω / 3889=(2.65 × 10⁷)ω',3),R('ω= 1.47 × 10⁻⁴ (rad) s⁻¹',3)],'phys-1-6','gps-angular-velocity',SQ(11,'its angular velocity.'),6,stem=[GPS6,DATA6]),
])
U('Q6','signal-time','Signal travel time',P(5,'Calculate the minimum time it takes a signal to travel','from the global positioning satellite to the Earth.'),
 [FR(11,(69,593,295,621),'v= s/t / (3.00 ×10⁸)= (2.65 × 10⁷−6.4 × 10⁶)/t',3),R('t= 0.067 s',3)],
 'phys-1-1',SQ(11,'Calculate the minimum time it takes a signal to travel','Earth.'),6,stem=[GPS6,DATA6])
U('Q6','remaining-in-orbit','Remaining in orbit',P(5,'Explain why satellites remain in orbit and do not fall to Earth.'),
 [R('(horizontal) velocity',5)],'phys-1-5',SQ(11,'Explain why satellites remain in orbit and do not fall and crash into the Earth.'),5,stem=[STEM6])

STEM7=P(6,'In a thunderstorm different parts of a cloud become positively and negatively','between different parts of the cloud and between the cloud and the ground.')
SPHERE7=P(6,'A spherical conductor has a diameter of 12 cm. It is charged positively by induction.')
U('Q7','potential-difference','Potential difference and unit',P(6,'What is meant by potential difference? State its unit.'),
 [R('work done',3,route='words',note=DSL),R('per unit charge',3,route='words'),FR(12,(249,130,264,157),'W/Q',3,route='formula'),
 pt(S('// notation',piece=2,psep='//'),3,kind='criterion',route='formula'),R('volt',3)],
 'phys-3-2',SQ(12,'What is meant by potential difference? State its unit.'),9,stem=[STEM7])
U('Q7','field-strength','Electric field strength',P(6,'Define electric field strength.'),
 [R('force',3,route='words',note=DSL),R('per unit charge',3,route='words'),FR(12,(249,221,262,248),'F/Q',3,route='formula'),pt(S('// notation',piece=2,psep='//'),3,kind='criterion',route='formula')],
 'phys-3-2',SQ(12,'Define electric field strength.'),6,stem=[STEM7])
U('Q7','induction','Charging by induction',P(6,'Describe how an insulated spherical conductor can be charged positively by induction.'),
 [R('(negatively) charged rod close to it',3),R('earth sphere',3),R('remove earth',3)],'phys-3-1',SQ(12,'Describe how an insulated spherical conductor can be charged positively by induction.'),9)
U('Q7','field-pattern','Electric field pattern',P(6,'Draw the electric field around the charged conductor.'),
 [R('radial field lines',4),R('away from positive charge',2)],'phys-3-2',SQ(12,'Draw the electric field around the charged conductor.'),6,stem=[SPHERE7])
U('Q7','charge','Charge on the conductor',P(6,'There is an electric field strength of 2.3 N C⁻¹','this spherical conductor. Calculate the charge on the conductor.'),
 [FR(12,(69,467,371,495),'E= Q/(4π∈d²) / 2.3= Q/(4π(8.9 × 10⁻¹²)(0.11)²) / E= F/Q / F= q₁q₂/(4π∈d²)',3),R('Q= 3.1 × 10⁻¹² C',3)],
 'phys-3-2',SQ(12,'There is an electric field intensity of 2.3 N C⁻¹','spherical conductor. Calculate the charge on the conductor.'),6,stem=[SPHERE7])
U('Q7','point-discharge','Point discharge',P(6,'Explain how point discharge occurs.'),
 [R('charge accumulates at a point',3),R('air around point is ionised',3),R('opposite charges attracted / like charges repelled',6)],'phys-3-1',SQ(12,'Explain how point discharge occurs.'),12)
U('Q7','point-discharge-experiment','Demonstrating point discharge',P(6,'Describe how point discharge can be demonstrated in the laboratory.'),
 [R('charged point',3),R('candle at point',3),R('flame is blown away from the point',2)],'phys-3-1',SQ(12,'Describe how point discharge can be demonstrated in the laboratory.'),8,
 cells='Scheme p12 prints 3, 3 and (2) against the three steps. The (2) shares a text object with Demonstration [8].')

SODIUM8=P(6,'When current is passed through the vapour in a sodium lamp, light is emitted as a line spectrum.')
GRAPH8=P(6,'The graph shows the relationship between the kinetic energy Eₖ','photoemission and the frequency f of the incident radiation.')
U('Q8','emission-types','Photoelectric and thermionic emission',P(6,'Electrons are emitted from metals during photoelectric emission, thermionic emission and','radioactive decay. Distinguish between photoelectric and thermionic emission.'),
 pieces(S('photoelectric: light; thermionic: heat'),[3,3],';'),'phys-4-2',SQ(13,'Electrons are emitted from metals during photoelectric emission, thermionic emission and','radioactive decay. Distinguish between photoelectric and thermionic emission'),6)
U('Q8','beta','Radioactive electrons',P(6,'What name is given to electrons emitted during radioactive decay?'),
 [R('beta',3)],'phys-4-4',SQ(13,'What name is given to electrons emitted during radioactive decay?'),3)
U('Q8','line-spectrum','Line emission spectrum',P(6,'What is a line emission spectrum?','What is a line emission spectrum?'),
 [R('(specific) frequencies/colours (of e.m. radiation) emitted by a material',3)],'phys-4-3',SQ(13,'What is a line emission spectrum?'),3,stem=[SODIUM8],
 cells='Scheme p13 prints (3) on the answer line at x442, inside the same text object, followed by What [3].')
U('Q8','atomic-levels','Producing the spectrum',P(6,'Explain, in terms of the structure of the atom, how this','spectrum is produced.'),
 [R('energy given to electron',3),R('electron changes energy levels',3),R('photon emitted / light emitted / (e.m.) radiation emitted',3)],
 'phys-4-3',SQ(13,'Explain, in terms of the structure of the atom, how this spectrum is produced.'),9,stem=[SODIUM8])
U('Q8','einstein','Einstein’s equation',P(6,'Write down Einstein’s photoelectric equation.'),
 [FR(13,(69,309,158,336),'hf=∅+ ½ mv²',3)],'phys-4-2',SQ(13,'Write down Einstein’s photoelectric equation.'),3,stem=[GRAPH8],fig='q8-graph')
WHAT8=P(6,'What physical quantity is represented by (i) point A,','(ii) the slope of the graph?')
TASKS.extend([
 T('8i','Q8(i)','B',dict(WHAT8,piece=1,psep=', (ii)'),[R('threshold frequency',3)],'phys-4-2','threshold-frequency',SQ(13,'What physical quantity is represented by (i) point A'),3,stem=[GRAPH8],fig='q8-graph'),
 T('8ii','Q8(ii)','B',[dict(WHAT8,piece=1,psep=' (i)'),dict(WHAT8,piece=2,psep=', (ii)')],[R('Planck constant',3)],'phys-4-2','planck-constant',SQ(13,'the slope of the graph?'),3,stem=[GRAPH8],fig='q8-graph'),
])
U('Q8','electron-speed','Maximum electron velocity',P(6,'The work function of magnesium is 3.68 eV.','energy 4.15 eV are incident on magnesium.'),
 [R('Eₖ=0.47 (eV) / 7.5×10⁻²⁰ (J)',3),FR(13,(69,450,328,476),'Eₖ= ½ mv² / 7.5×10⁻²⁰ = ½ (9.1×10⁻³¹) v²',3),R('v=4.1×10⁵ m s⁻¹',3)],
 'phys-4-2',SQ(13,'The work function of magnesium is 3.68 eV.','electrons when photons of energy 4.15 eV are incident on magnesium.'),9)
U('Q8','xray-electrons','Electron source in an X-ray tube',P(6,'Electrons are produced in an X‐ray tube by thermionic emission.','electrons produced?'),
 [R('cathode',3)],'phys-4-2',SQ(13,'Electrons are produced in an X‐ray tube by thermionic emission.','electrons produced?'),3)
U('Q8','xray-wavelength','Minimum X-ray wavelength',P(6,'The electrons are then accelerated to high velocities.','converted into X‐rays. What is the minimum wavelength of an X‐ray produced in a 50 kV tube?'),
 [R('eV / hf',3),R('eV=hf / (1.6×10⁻¹⁹)(50×10³)=(6.6×10⁻³⁴)f',3),R('λ= 2.5×10⁻¹¹ m',3,note_sel=S('(–1 if answer left as f = 1.2×10¹⁹ Hz)'))],
 'phys-4-2',SQ(13,'The electrons are then accelerated to high velocities.','converted into X‐rays. What is the minimum wavelength of an X‐ray produced in a 50 kV tube?'),9)
U('Q8','xray-cooling','Managing heat in an X-ray tube',P(6,'The kinetic energy of each of the other electrons is converted into heat energy.','features of an X‐ray tube that take account of this.'),
 [anyn(S('tungsten target, cooling fluid'),2,None,steps=[3,2],sep=',')],'phys-4-2',SQ(13,'The kinetic energies of the other electrons are converted into heat energy.','features of an X‐ray tube that take account of this.'),5)
FIGURES['q8-graph']=('paper',6,(414,480,544,586),SEC,[],'Kinetic energy versus frequency graph, with horizontal intercept A.',False)
GLYPHS['scheme']['SymbolMT']={58:'Ω',79:'λ',80:'μ',83:'π'}

STEM9A=P(7,'Both a moving charge and a conductor carrying an electric current experience a force in a','magnetic field.')
STEM9B=P(7,'A straight wire of length 3 cm was placed perpendicular to a magnetic field of uniform','current I flowing in the wire. The following data were recorded.')
U('Q9(a)','terms','Force and magnetic field',P(7,'Explain the underlined terms.'),
 [R('force is what causes acceleration',3),R('magnetic field is a region where magnetic forces are felt',3)],
 'phys-3-5',SQ(14,'Explain the underlined terms.'),6,stem=[STEM9A],fig='q9-underlined-terms')
U('Q9(a)','experiment','Force on a conductor',P(7,'Describe an experiment to demonstrate that a current‐carrying conductor experiences a','force in a magnetic field.'),
 [R('power supply, aluminium foil, magnets',3),C('correct arrangement',3),R('foil moves',3)],
 'phys-3-5',SQ(14,'Describe an experiment to demonstrate that a current‐carrying conductor experiences a force','in a magnetic field.'),9,stem=[STEM9A])
U('Q9(a)','no-force','When there is no force',P(7,'When would a current‐carrying conductor in a magnetic field not experience a force?'),
 [R('it is parallel to the field',3)],'phys-3-5',SQ(14,'When would a current‐carrying conductor in a magnetic field not experience a force?'),3)
U('Q9(b)','force-expression','Force expression',P(7,'Write down an expression for the force F on the current‐carrying wire in terms of I, B and','the length l of the wire.'),
 [R('(F=)BIl',3)],'phys-3-5',SQ(14,'Write down an expression for the force F on the current‐carrying wire.'),3,stem=[STEM9B])
U('Q9(b)','graph','Force–current graph',P(7,'Plot a graph on graph paper of force against current.','Plot a graph on graph paper of force against current.'),
 [C('labelled axes',3),C('points plotted correctly',3),C('line of good fit',3)],'phys-3-5',SQ(14,'Plot a graph on graph paper of force against current.'),9,stem=[STEM9B],fig='q9-data')
U('Q9(b)','flux-density','Magnetic flux density',P(7,'Calculate the slope of the graph and','use it to calculate the magnetic flux density of the field.'),
 [FR(14,(83,457,214,485),'slope: (m= (y₂−y₁)/(x₂−x₁) ) = 0.02',3),R('m=Bl / 0.02=B(0.03)',3),R('B= 0.67 T',3)],
 'phys-3-5',SQ(14,'Calculate the slope of graph and use it to calculate the magnetic flux density of the field.'),9,
 stem=[STEM9B,P(7,'Plot a graph on graph paper of force against current.','Plot a graph on graph paper of force against current.')],fig='q9-data',
 cells='Scheme p14 allocates 3 for slope, 3 for m=Bl and 3 for B=0.67 T; the final (3) shares the total-summary text object.')
U('Q9(c)','derivation','Force on a moving charge',P(7,'Starting with the expression for the force that you wrote in part (b)','magnetic field of flux density B.'),
 [FR(14,(76,567,169,593),'I= q/t and v= l/t',3),FR(14,(76,590,165,616),'F=B( q/t )(vt)',3),R('F=qvB',3)],
 'phys-3-5',SQ(14,'Starting with the expression for the force that you gave in part (b)','magnetic field of flux density B.'),9,
 stem=[STEM9B,P(7,'Write down an expression for the force F on the current‐carrying wire in terms of I, B and','the length l of the wire.')])
U('Q9(c)','proton-speed','Proton speed',P(7,'In a nuclear detector a proton enters a magnetic field of flux density 0.5 T at right angles to','the proton as it enters the field.'),
 [FR(14,(76,680,188,709),'F=qvB / F= mv²/r',3),FR(14,(76,706,341,733),'qvB= mv²/r / (1.60×10⁻¹⁹)(0.5)= ((1.67×10⁻²⁷)v)/(2.3×10⁻³)',3),R('v= 1.1×10⁵ m s⁻¹',2)],
 'phys-3-5',SQ(14,'In a nuclear detector a proton enters a magnetic field of flux density 0.5 T at right angles to','the proton on entry.'),8)

YOUNG10=P(8,'In 1801 Thomas Young performed an experiment to demonstrate that light','series of bright and dark fringes on a screen.')
LAB10=P(8,'The experiment was repeated in the school','be 1.65 cm.')
PIPE10=P(8,'A certain musical instrument can be modelled as a cylindrical pipe that is closed at one end and','whose length can be changed. The air column in the pipe vibrates at a frequency of 512 Hz.')
LENGTH10=P(8,'The lengths of the pipe at the first two positions of resonance are 16.7 cm and 49.8 cm.')
U('Q10','wave-terms','Diffraction and interference',P(8,'Explain the terms diffraction and interference.'),
 [R('the spreading out of a wave',3,label=S('diffraction:')),R('after it passes an obstacle/gap',3),R('occurs when two waves meet',3,label=S('interference:'))],
 'phys-2-6',SQ(15,'Explain the terms diffraction and interference.'),9,
 cells='Scheme p15 prints three 3-mark definition rows; the final (3) is in the Explain terms [9] text object.')
U('Q10','fringes','Producing fringes',P(8,'Explain, with the aid of a labelled diagram, how a series of bright and dark','fringes were produced.'),
 [R('slits',3),R('diffraction at slits',3),R('interference',3)],'phys-2-6',SQ(15,'Explain, with the aid of a labelled diagram, how a series of bright and dark fringes are produced.'),9,stem=[YOUNG10])
U('Q10','wave-evidence','Evidence that light is a wave',P(8,'How does this experiment demonstrate that light is a wave?'),
 [R('result can only be explained using interference',3)],'phys-2-6',SQ(15,'How does this experiment demonstrate that light is a wave?'),3,stem=[YOUNG10])
U('Q10','light-wavelength','Wavelength of light',P(8,'Calculate the wavelength of the monochromatic light.'),
 [R('distance between n equals zero and n equals six = 0.825 cm',3),FR(15,(69,350,278,377),'tanθ= O/A / tanθ= 0.825/125 / θ=0.378',3),
  R('nλ=dsinθ / 6λ=(0.5 × 10⁻³)sin(0.378)',3),R('λ= 5.5 × 10 ⁻⁷m',3)],
 'phys-2-6',SQ(15,'The distance across 13 bright fringes on the screen was found to be 1.65 cm. Calculate the','wavelength of the monochromatic light.'),12,stem=[YOUNG10,LAB10],fig='q10-fringes')
U('Q10','fringe-spacing','Increasing fringe spacing',P(8,'List two adjustment to the apparatus that could be made to increase the distance between the','bright fringes.'),
 [anyn(S('move screen from slits, decrease distance between slits, increase λ'),2,3,sep=',')],
 'phys-2-6',SQ(15,'List two adjustment to the apparatus that could be made to increase the distance between the','bright fringes?'),6,stem=[YOUNG10,LAB10],
 cells='Scheme p15 prints (2×3) on the answer line within the same text object; List two [6] confirms six marks.')
U('Q10','lens-power','Lens power',P(8,'When the ciliary muscles contract the lens in the eye becomes thinner.','on the power of the lens?'),
 [R('decreases power',3)],'phys-2-3',SQ(15,'When the ciliary muscles contract the lens in the eye becomes thinner.','on the power of the lens?'),3,
 decision='The paper’s stated contraction/thinner premise is retained verbatim; the scheme answers the consequence of a thinner lens.')
U('Q10','harmonics','First two resonances',P(8,'Draw diagrams to show the first two harmonics of this instrument.'),
 [C('correct diagram for first harmonic',3),C('correct diagram for third harmonic',3)],'phys-2-6',SQ(15,'Draw diagrams to show the first two harmonics of this instrument.'),6,stem=[PIPE10],
 decision='The paper says first two harmonics; the official scheme explicitly prices first and third harmonics of a closed pipe. Both rows are retained.')
CALC10=P(8,'Calculate (i) the wavelength of the sound wave, (ii) the speed of sound in air.')
TASKS.extend([
 T('10i','Q10(i)','B',dict(CALC10,piece=1,psep=', (ii)'),[R('λ=2×(0.498−0.167)=0.66 m',3)],'phys-2-5','sound-wavelength',SQ(15,'Calculate (i) the wavelength of the sound wave,'),3,stem=[PIPE10,LENGTH10]),
 T('10ii','Q10(ii)','B',[dict(CALC10,piece=1,psep=' (i)'),dict(CALC10,piece=2,psep=', (ii)')],[R('c=fλ / c=(512)(0.66)',3),R('c=339 m s⁻¹',2)],'phys-2-5','speed-of-sound',SQ(15,'the speed of sound in air.'),5,stem=[PIPE10,LENGTH10]),
])

PASSAGE11=P(9,'Physics Rivalries','Element (Jeremy Bernstein)')
for ref,q,rows,topic,anchor in [
 ('Q11(a)',P(9,'Explain why the transmission of electricity using low voltage is not economical.'),[R('high current',4),R('heat/energy loss',3)],'phys-3-6',SQ(16,'Explain why transmission of electricity using low voltage is not economical.')),
 ('Q11(b)',P(9,'Name the device used to (i) reduce a.c. voltage, (ii) convert current from a.c. to d.c.'),[R('transformer',4),R('rectifier/diode',3)],'phys-3-6',SQ(16,'Name the device used to (i) reduce a.c. voltage, (ii) convert current from a.c. to d.c.')),
 ('Q11(c)',P(9,'State Hooke’s law.'),[pt(S('(restoring) force is proportional to // F=−ks',piece=1,psep='//'),4,route='words',note=DSL),R('displacement',3,route='words'),pt(S('(restoring) force is proportional to // F=−ks',piece=2,psep='//'),4,route='formula'),pt(S('// correct notation',piece=2,psep='//'),3,kind='criterion',route='formula')],'phys-1-3',SQ(16,'State Hooke’s law.')),
 ('Q11(d)',P(9,'A ball of mass 110 g is travelling at a speed of 4 m s⁻¹.','the wall on the ball.'),[FR(16,(97,296,152,323),'F= ∆(mv)/(∆t)',3),FR(16,(97,322,209,350),'F= ((0.11)(4)−(0.11)(−4))/0.2',2),R('F=4.4 N',2)],'phys-1-2',SQ(16,'A ball of mass 110 g is travelling at a speed of 4 m s⁻¹.','the wall on the ball.')),
 ('Q11(e)',P(9,'A magnifying glass is a basic microscope.','an upright image in a magnifying glass.'),[R('object inside focal point of converging lens',3),C('two correct rays through lens',2),C('correct image',2)],'phys-2-3',SQ(16,'A magnifying glass is a basic microscope.','an upright image in a magnifying glass.')),
]:
 TASKS.append(T(ref,ref,'B',q,rows,topic,ref.lower().replace('(','-').replace(')',''),anchor,7,stem=[PASSAGE11]))
FISSION11=P(9,'A plutonium–239 nucleus undergoes fission when a neutron collides with it.','Xenon–134 and zirconium–103 are produced together with some neutrons.')
MASSES11=P(9,'(masses of: Pu–239 = 239.052163 u, Xe–134 = 133.905395 u, Zr–103 = 102.926599 u)')
U('Q11(f)','equation','Fission equation',P(9,'Write a nuclear equation for this fission reaction.'),
 [EQ(16,(97,518,290,540),'Pu²³⁹₉₄ + n¹₀ → Xe¹³⁴₅₄ + Zr¹⁰³₄₀ + 3n¹₀',5)],'phys-4-6',SQ(16,'A plutonium–239 nucleus undergoes nuclear fission','nuclear equation for this fission reaction.'),5,stem=[PASSAGE11,FISSION11])
U('Q11(f)','energy','Energy released',P(9,'Calculate the energy released in this reaction.'),
 [R('loss in mass = 3.3682×10⁻²⁸ kg',3),R('E=mc²',3),R('E=(3.3682×10⁻²⁸)(2.9979×10⁸)²',3),R('E= 3.0271×10⁻¹¹ J',3)],
 'phys-4-5',SQ(16,'Calculate the energy released in this reaction.'),12,stem=[PASSAGE11,FISSION11,MASSES11])
U('Q11(f)','energy-form','Form of released energy',P(9,'In what form is this energy released?'),
 [R('kinetic energy / heat',4)],'phys-4-6',SQ(16,'In what form is this energy released?'),4,stem=[PASSAGE11,FISSION11])

MASS12=P(10,'A mass hanging at the end of a string of length 80 cm is given an initial','horizontal velocity of 4 m s⁻¹.')
G12=P(10,'(acceleration due to gravity = 9.8 m s⁻²)')
U('Q12(a)','conservation','Conservation of energy',P(10,'State the principle of conversation of energy.'),
 [R('energy cannot be created or destroyed',3,note_sel=S('(Due to typographical error, award 3 marks to all candidates who attempt Q12 (a))'))],
 'phys-1-4',SQ(17,'State the principle of conversation of energy.'),3,
 decision='The paper’s conversation typo and the scheme’s automatic three-mark instruction are retained visibly.')
U('Q12(a)(i)','velocity','Velocity at B',[P(10,'Calculate',nth=1),P(10,'the velocity of the mass at position B,')],
 [R('h=0.8−0.8cos35 / 0.145',3),FR(17,(97,218,172,244),'mgh / ½ mv²',3),
  FR(17,(97,241,415,266),'mgh+ ½ mv²=mgh+ ½ mv² / ½ (4)²=(9.8)(0.145)+ ½ v²',3),R('v= 3.63 m s⁻¹',3)],
 'phys-1-4',SQ(17,'the velocity of the mass at position B,'),12,stem=[MASS12,G12],fig='q12a-pendulum',
 cells='Scheme p17 prints four allocations of 3. The final (3) shares the Calculate (i) [12] text object.')
U('Q12(a)(ii)','centripetal-acceleration','Centripetal acceleration',[P(10,'Calculate',nth=1),P(10,'its centripetal acceleration at position B.')],
 [FR(17,(97,296,139,325),'a= v²/r',3),FR(17,(97,322,149,350),'a= 3.63²/0.8',3),R('a=16.5 m s⁻² (towards the centre)',3)],
 'phys-1-6',SQ(17,'its centripetal acceleration at position B.'),9,stem=[MASS12,G12],fig='q12a-pendulum',
 cells='Scheme p17 prints three allocations of 3. The final (3) shares the Calculate (ii) [9] text object.')
U('Q12(a)','forces','Forces at B',dict(P(10,'Draw a labelled diagram to show the forces acting on the mass when it is at position B.'),piece=1,psep=' (25)'),
 pieces(S('weight, tension (–1 for each incorrect force)'),[2,2],','),'phys-1-2',SQ(17,'Draw a labelled diagram to show the forces acting on the mass when it is at position B.'),4,stem=[MASS12,G12],fig='q12a-pendulum')

RAM12=P(10,'A RAM (random access memory) integrated chip contains transistors, in which there are','doped semiconductors, and capacitors.')
CAP12=P(10,'The capacitance of a capacitor in a RAM chip is 90 fF. It operates at','a voltage of 1.2 V.')
U('Q12(b)','semiconductor','Semiconductor',P(10,'What is a semiconductor?','What is a semiconductor?'),
 [R('material with a resistivity between that of a conductor and an insulator',3)],'phys-3-3',SQ(18,'What is a semiconductor?'),3,stem=[RAM12],
 cells='The answer is priced by a separate (3) on the immediately following line on scheme p18; What (i)? [3] confirms it.')
U('Q12(b)','doping','Doping',P(10,'What is meant by doping a semiconductor?'),
 [R('adding an impurity (to change its conductivity)',3)],'phys-3-3',SQ(18,'What is meant by doping a semiconductor?'),3,stem=[RAM12],
 cells='Scheme p18 prints (3) in the same text object as b What (ii)? [3].')
DOPING12=P(10,'How can a semiconductor be doped so that (i) its majority charge carriers are electrons,','(ii) its majority charge carriers are holes?')
U('Q12(b)(i)','n-type','Electron majority carriers',dict(DOPING12,piece=1,psep=', (ii)'),
 [R('add an element with more outer electrons / add e.g. phosphorus',3)],'phys-3-3',SQ(18,'How can a semiconductor be doped so that (i) its majority charge carriers are electrons,'),3,stem=[RAM12],
 cells='Scheme p18 prints (3) at the end of the answer text object, followed by b How (i)? [3].')
U('Q12(b)(ii)','p-type','Hole majority carriers',[dict(DOPING12,piece=1,psep=' (i)'),dict(DOPING12,piece=2,psep=', (ii)')],
 [R('add an element with fewer outer electrons/ add e.g. boron',3)],'phys-3-3',SQ(18,'its majority charge carriers are holes?'),3,stem=[RAM12])
U('Q12(b)(i)','capacitor-energy','Stored energy',[P(10,'Calculate',nth=2),P(10,'the energy stored in the capacitor when it is fully charged,')],
 [FR(18,(97,300,155,326),'E= ½ CV²',3),FR(18,(97,323,238,348),'E= ½ (90×10⁻¹⁵)(1.2)²',3),R('E=6.5×10⁻¹⁴ J',3)],
 'phys-3-2',SQ(18,'the energy stored in the capacitor when it is fully charged,'),9,stem=[CAP12])
U('Q12(b)(ii)','capacitor-electrons','Additional electrons',[P(10,'Calculate',nth=2),P(10,'the number of additional electrons that are on the negative plate of the','capacitor as a result of it being fully charged.')],
 [R('Q=CV / Q=(90×10⁻¹⁵)(1.2)',3),R('Q=1.08×10⁻¹³ (C)',2),FR(18,(97,431,382,460),'number of additional electrons = (1.08×10⁻¹³)/(1.6×10⁻¹⁹) =675000',2)],
 'phys-3-2',SQ(18,'the number of additional electrons that are on the negative plate of the capacitor as a','result of it being fully charged.'),7,stem=[CAP12],
 cells='Scheme p18 prices Q=CV at 3, charge at 2, electron count at 2. Final (2) shares the Calculate (ii) [7] summary.')

LIGHT12=P(10,'As light passes from water into air the critical angle may be exceeded and','total internal reflection may occur.')
DIVER12=P(10,'A diver is 12 m below the surface in a pool of water.','water.',end_nth=2)
INDEX12=P(10,'(refractive index of water = 1.33)')
U('Q12(c)','terms','Critical angle and total internal reflection',P(10,'Explain the underlined terms.'),
 [R('critical angle: angle of incidence',3),R('corresponding to an angle of refraction of 90°',3),R('angle of incidence > critical angle (and all light is reflected)',3,label=S('t.i.r.:'))],
 'phys-2-3',SQ(19,'Explain the underlined terms.'),9,stem=[LIGHT12],fig='q12c-underlined-terms',
 cells='Scheme p19 prints three 3-mark rows; the last (3) is embedded in the total-internal-reflection answer line.')
U('Q12(c)','disc-area','Area of the disc of light',P(10,'Calculate the area of this disc of light.'),
 [FR(19,(97,199,290,226),'n= 1/(sinC) / 1.33= 1/(sinC) / C=48.8°',3),FR(19,(97,220,339,246),'tanθ= r/d / tan48.8° = r/12 / r=13.7 (m)',3),R('A=πr²',3),R('A=590 m²',3)],
 'phys-2-3',SQ(19,'Calculate the area of this disc of light.'),12,stem=[DIVER12,INDEX12],fig='q12c-diver')
U('Q12(c)','apparent-depth','Apparent depth',P(10,'Use a labelled diagram to explain why the diver does not appear to be at a depth of 12 m','when viewed by an observer outside the pool.'),
 [C('correct refracted ray',4),C('correct apparent ray / correct position of image',3)],'phys-2-3',SQ(19,'Use a labelled diagram to explain why the diver does not appear to be at a depth of 12 m','when viewed by an observer outside the pool.'),7,stem=[DIVER12,INDEX12])

LHC12=P(11,'The new Swiss 200‐franc note honours proton‐proton collisions in the Large Hadron','Collider (LHC) at CERN.')
COLLISION12=P(11,'Two protons, each with a velocity of 0.9c, travelling in opposite','after the collision.')
ACCELERATOR12=P(11,'The large hadron collider is a circular accelerator.')
U('Q12(d)(i)','hadrons','Hadron families',P(11,'There are two families of hadrons. Name the two families and','distinguish between them.'),
 [R('baryon and meson',3),R('baryon has three quarks and meson has a quark and an antiquark',3)],'phys-4-5',SQ(20,'There are two families of hadrons. Name the two families and distinguish between them.'),6,stem=[LHC12])
U('Q12(d)(i)','pion-charge','Neutral pion',P(11,'The single pion produced must be neutral. Explain why.'),
 [R('conservation of charge',3)],'phys-4-5',SQ(20,'The single pion produced must be neutral. Explain why.'),3,stem=[LHC12,COLLISION12])
U('Q12(d)(i)','collision-energy','Energy after the collision',P(11,'Calculate the total kinetic energy of the three particles after the','collision.'),
 [FR(20,(111,250,178,276),'E= ½ mv²',3),R('Eb=(1.6726 ×10⁻²⁷)((0.9)(2.9979×10⁸))²/ Eb=1.2176×10⁻¹⁰',3),
  R('E=mc² / Eₐ=Eb−mπc²',3,'/ Eₐ=1.2176×10⁻¹⁰−(264)(9.1094×10⁻³¹)(2.9979×10⁸)²'),R('Eₐ=1.00×10⁻¹⁰ J',3)],
 'phys-4-5',SQ(20,'Calculate the total kinetic energy of the three particles after the collision.'),12,stem=[LHC12,COLLISION12])
U('Q12(d)(i)','circular-path','Maintaining circular motion',P(11,'How are the protons maintained in circular motion?'),
 [R('magnetic fields (provide the centripetal force)',3)],'phys-3-5',SQ(20,'How are the protons maintained in circular motion?'),3,stem=[LHC12,ACCELERATOR12])
U('Q12(d)(i)','accelerator-advantage','Circular accelerator advantage',P(11,'State the principal advantage of a circular accelerator over a','linear accelerator.'),
 [R('greater energy can be created / longer path available for particles / more compact',4)],'phys-4-5',SQ(20,'State the principal advantage of a circular accelerator over a linear accelerator'),4,stem=[LHC12,ACCELERATOR12],
 cells='Scheme p20 prices the long answer with a separate (4) on the following line; d i State [4] confirms it.')

AMP12=P(11,'Transistors and resistors can be used to construct voltage amplifier circuits.','Transistors and resistors can be used to construct voltage amplifier circuits.')
CIRCUIT12=P(11,'Draw a','circuit diagram of a voltage amplifier circuit.')
U('Q12(d)(ii)','transistor','Transistor symbol and structure',P(11,'Draw the symbol for a transistor and a diagram of its structure.'),
 [C('symbol',3),C('correct diagram of structure',3),C('fully labelled',3)],'phys-3-3',SQ(20,'Draw the symbol for a transistor and a diagram of its structure.'),9,
 cells='Scheme p20 prints 3 for symbol, 3 for structure and (3) for labels in the Draw and diagram [9] summary object.')
U('Q12(d)(ii)','amplifier','Voltage amplifier circuit',CIRCUIT12,
 [R('transistor, bias resistor, load resistor',3),C('correct arrangement',3)],'phys-3-3',SQ(20,'Draw a','circuit diagram of a voltage amplifier circuit.'),6,stem=[AMP12])
U('Q12(d)(ii)','amplifier-labels','Labelling the amplifier',P(11,'Label the bias resistor, the load resistor','and the input and output voltages.'),
 [C('labelled bias resistor and labelled load resistor',3),R('labelled input voltage between base and emitter',3),R('labelled output voltage across load resistor',3,'or between collector, emitter')],
 'phys-3-3',SQ(20,'Label the bias, the load resistor and the input and output voltages.'),9,stem=[AMP12,CIRCUIT12])
U('Q12(d)(ii)','bias-resistor','Purpose of the bias resistor',P(11,'What is the purpose of the bias resistor?'),
 [R('ensures base emitter junction is always forward biased',2)],'phys-3-3',SQ(20,'What is the purpose of the bias resistor?'),2,stem=[AMP12,CIRCUIT12],
 cells='Scheme p20 prints (2) at the end of the answer text, before d ii Purpose i [2].')
U('Q12(d)(ii)','load-resistor','Purpose of the load resistor',P(11,'What is the purpose of the load resistor?'),
 [R('converts changes in collector current to',2,'changes in voltage across load')],'phys-3-3',SQ(20,'What is the purpose of the load resistor?'),2,stem=[AMP12,CIRCUIT12])

FIGURES.update({
 'q8-graph':('paper',6,(368,502,497,619),SEC,[],'Kinetic energy Eₖ versus frequency f, with horizontal intercept A.',False),
 'q9-underlined-terms':('paper',7,(80,54,530,115),SEC,[],'The paper underlines force and magnetic field and asks for explanations.',False),
 'q9-data':('paper',7,(149,265,446,317),SEC,[],'Current I in A and magnetic force F in mN.',False),
 'q10-fringes':('paper',8,(317,265,540,363),SEC,[],'The bright and dark fringes shown in the question paper.',False),
 'q12a-pendulum':('paper',10,(451,109,539,231),SEC,[],'String of length 80 cm, with position B at 35 degrees from the downward vertical.',False),
 'q12c-underlined-terms':('paper',10,(80,550,452,610),SEC,[],'Critical angle and total internal reflection underlined in the original paper.',False),
 'q12c-diver':('paper',10,(419,612,541,695),SEC,[],'Photograph of a diver looking towards the light at the water surface.',False),
})

# The sphere photograph provides the apparatus context without including adjacent question text.
FIGURES['q7-sphere']=('paper',6,(484,154,551,271),SEC,[],
                     'A spherical metal conductor mounted on an insulating stand.',False)
for task in TASKS:
    if task['key'] in {'Q7:field-pattern','Q7:charge'}:
        task['fig']='q7-sphere'

# Separate embedded mark text from answer text without rewriting either source.
# These seven answer objects carry the trailing mark inside the PDF text object.
_INLINE_MARKS={
 'move screen (and/or object and/or mirror) until (sharpest) image is formed':' (3)',
 'ice would melt more quickly / so that energy lost = energy gained':' (3)',
 '(specific) frequencies/colours (of e.m. radiation) emitted by a material':' (3)',
 'add an element with more outer electrons / add e.g. phosphorus':' (3)',
 'angle of incidence > critical angle (and all light is reflected)':' (3)',
 'ensures base emitter junction is always forward biased':' (2)',
 'move screen from slits, decrease distance between slits, increase λ':' (2×3)',
}
for task in TASKS:
    for row in task['rows']:
        sel=row.get('sel',{})
        if sel.get('start') in _INLINE_MARKS:
            sel.update(piece=1,psep=_INLINE_MARKS[sel['start']])
    # A stem referring to recorded data always carries that source table.
    if not task['fig'] and not task['qfig']:
        root=task['ref'].split('(')[0]
        if root in {'Q1','Q2','Q4'}:
            task['fig']={'Q1':'q1-data','Q2':'q2-data','Q4':'q4-data'}[root]
        elif task['ref'] in {'Q9(b)','Q9(c)'} and task['key']!='Q9(c):proton-speed':
            task['fig']='q9-data'
