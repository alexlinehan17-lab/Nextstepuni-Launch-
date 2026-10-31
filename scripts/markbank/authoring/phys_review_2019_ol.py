"""Physics 2019 Ordinary — independently reviewed paper/scheme ledger.

All 12 paper and 20 scheme pages rendered and visually read, 2026-10-31.
The marked unit follows the paper's roman/letter or an explicitly separate
sub-question with its own tariff. Q1(v)'s two force sums jointly verify one law;
Q9(a)(iii)'s graph identification and explanation remain one coherent response.
Q2(iii)(a)/(b), Q3(iii)'s two sentences and Q12(d)(i)'s two questions split at
published six/four-mark boundaries, each with the full necessary context.
Q11(e) naming/sketch and Q11(g) power/focal length remain their holistic 7-mark
answers. Q12(d)(iv) retains its paired advantage/disadvantage response at 4+4.

Q5 best eight of ten and Q12 any two letters: all options are carded, no
combinations. Lists inside tasks retain all alternatives and appropriate slots.
Partial-credit lines are notes, not extra marks. Printed stepped item scales
use their stated increments (7/5/3 or 9/6). Diagram criteria have the official
source illustration where one is supplied. All Cambria missing-glyph first
occurrences were individually cropped and read; fractions are lifted by geometry.
"""
from phys_review_lib import Q, SQ, S, M, G, L, pt, anyn, T
YEAR, LEVEL = 2019, 'ol'
REVIEWED_AT = '2026-10-31'
LETTERED = {5,9,11,12}
SOURCES = {
 'paper':{'path':'examiner-reports/physics/papers/2019-ol-paper.pdf','fileid':'LC021GLP000EV.pdf','sha256':'a514daf3e413fe08c8c149bf71e8ae05e964b1bb179f4eb47f0baa6887fa802e','pages':12},
 'scheme':{'path':'examiner-reports/physics/schemes/2019-ol.pdf','fileid':'LC021GLP000EV.pdf','sha256':'1956ce2b3c7370135b8156ca4e5f6c860258dbc5da692ca1457b14eeb76b3697','pages':20},
}
PAGE_ROLES = {'paper':{1:'cover',**{p:'questions' for p in range(2,12)},12:'back-cover'},
 'scheme':{1:'cover',2:'note',3:'conventions',4:'annotations',5:'irish-language-bonus-instructions',**{p:'marking' for p in range(6,19)},19:'blank',20:'back-cover'}}
# Each missing-glyph id visually read at its first occurrence (three glyph sheets).
_CAMBRIA={2025:'ρ',3019:'R',3002:'A',3039:'l',1847:'U',2877:'9',2870:'2',2871:'3',2876:'8',2873:'5',
 2929:'s',2919:'i',2924:'n',3036:'i',3045:'r',3032:'e',3028:'a',3031:'d',3043:'p',3047:'t',3035:'h',3041:'n',
 2869:'1',3004:'C',3095:'π',3118:'2',2872:'4',3404:'=',2874:'6',3400:'×',2868:'0',3127:'−',3124:'8',2879:'−',
 2251:'ρ',2174:'R',2157:'A',2194:'l',4666:'(',4667:')',1865:'m',1853:'a',3007:'F',3040:'m',3119:'3',1842:'P',
 3023:'V',3050:'w',3042:'o',3038:'k',3046:'s',2875:'7',1874:'v',1858:'f',2245:'λ',2019:'λ',1856:'d',2016:'θ',
 3397:'+',2878:'+',1844:'R',1835:'I',3017:'P',1871:'s',1860:'h',3014:'M',3018:'Q',2177:'U',2786:'9',2779:'2',2780:'3',2785:'8',2782:'5'}
GLYPHS = {'paper':{'Cambria':_CAMBRIA},'scheme':{'Cambria':_CAMBRIA}}
VERIFIED_LINES=[]
QUESTION_TOTALS={**{n:40 for n in range(1,5)},**{n:56 for n in range(5,12)},12:112}
PART_TOTALS={(9,'a'):24,(9,'b'):12,(9,'c'):20,**{(11,x):7 for x in 'abcdefgh'},**{(12,x):28 for x in 'abcd'}}
BEST_OF={5:(8,7)}
GROUP_TOTALS={(1,('i','ii','iii')):18,(1,('iv',)):6,(1,('v','vi')):16,
 (6,('iv','v','vi')):20,(7,('i','ii','iii')):18,(7,('vi','vii')):14,
 (8,('ii','iii')):12,(8,('iv','v')):14,(8,('vii','viii')):12,
 (10,('i','ii','iii','iv','v')):30,(10,('vi','vii','viii','ix','x')):26}
CHECKSUMS={};ROUTES={}
SCAN_PAGES={'paper':range(2,12)}
SELECTION_SCAN=[]
ASK_SCAN_PAGES={'paper':range(2,12)}
ASK_EXEMPT=[]
SEC='State Examinations Commission'
DSL='The scheme’s // separates complete alternative answers; do not mix partial answers from different routes.'
CRIT='The scheme prints this marking criterion rather than a model answer.'
def P(page,start,end=None,**kw):return Q(page,start,end,**kw)
def R(text,marks,end=None,**kw):return pt(S(text,end),marks,**kw)
def C(text,marks,end=None,**kw):return pt(S(text,end),marks,kind='criterion',note=CRIT,**kw)
def partial(full,part,sel='partial answer',end=None,extra=''):
 return dict(note_sel=S(sel,end),note_lead=f'The scheme prices this “{full} or {part}”:',note=f'({part}). '+extra)
def FR(page,clip,expect,marks,**kw):return G('fraction',page=page,clip=clip,expect=expect,marks=marks,**kw)
def menu(text,claim,per,end=None,sep='//',**kw):
 lead=kw.pop('note_lead',None);spec=anyn(S(text,end),claim,per,sep=sep,**kw)
 if lead:spec['note_lead']=lead
 return spec
def items(sel,n,sep=','):return [dict(sel,piece=k,psep=sep) for k in range(1,n+1)]
TASKS=[]
def A(key,ref,page,question,sp,rows,topic,concept,total,end=None,sq=None,**kw):
 TASKS.append(T(key,ref,'A' if int(ref.split('(')[0][1:])<5 else 'B',P(page,question,end),rows,topic,concept,sq or SQ(sp,question,end),total,**kw))

STEM1=P(2,'A student performed an experiment to investigate the laws of equilibrium.','was balanced and level, as below.')
MEASURE1=P(2,'Before setting up the experiment, the student took two measurements.','She found its centre of gravity at the 50 cm mark.')
LAW1=P(2,'The first law of equilibrium states that the sum of the upward forces equals the sum of the','downward forces.')
LAW2=P(2,'The second law of equilibrium states that the sum of the clockwise moments equals the sum','of the anticlockwise moments.')
STEM2=P(3,'A student carried out an experiment to measure the specific latent heat of fusion of ice.','During the experiment, ice at 0 °C was added to a calorimeter containing warm water.')
MEASURE2=P(3,'Mass and temperature were measured in this experiment.')
ASK2=P(3,'Name (a) one mass measured and (b) one temperature measured.')
STEM3=P(3,'A student carried out an experiment to calculate the refractive index, n, of a material.')
ASK3=P(3,'What measurements did the student take during the experiment?')
STEM4=P(3,'A student performed an experiment to measure the resistivity ρ of a piece of nichrome wire','of length l, resistance R and diameter d.')
MASS6=P(5,'Armstrong had a mass of 90 kg.','90 kg.')
GRAV6=P(5,'(acceleration due to gravity, g = 9.8 m s⁻²)')
MOON6=P(5,'Armstrong’s weight on the moon was only 17% of his weight on Earth.','Earth.')
FOOT6=P(5,'The footprints he made during that walk are still on the moon to this day.','his foot onto the surface of the moon.')
STEM7=P(6,'When a musician moves his fingers up and down the strings of a guitar,','The characteristics of a musical note are pitch, loudness and quality.')
DOPPLER7=P(6,'The frequency of a sound wave appears to change when it moves past a stationary observer.','This phenomenon is called the Doppler effect.')
WAVES7=P(6,'Sound can be described as a longitudinal wave, whereas light is a transverse wave.')
POOL7=P(6,'Waves can undergo reflection, refraction, diffraction, interference and polarisation.','four of them.')
BATH8=P(6,'A student measured the temperature of a large bath full of water and a small cup full of','amount of energy”.')
THERM8=P(6,'The thermometric property used by a mercury thermometer is the length of a column of','liquid.')
BRICK8=P(6,'A storage heater consists of an electric heater surrounded by bricks made of a material with','a high specific heat capacity.')
KETTLE8=P(6,'A kettle supplies heat to 1.5 kg of water and raises its temperature from 15 °C to 88 °C.')
HEAT8=P(6,'(specific heat capacity of water = 4200 J kg⁻¹ K⁻¹)')
STATE8=P(6,'If heat energy continues to be supplied, the water will reach its boiling point and change','state.')
CIRCUIT9=P(7,'The circuit on the right is used to','demonstrate Ohm’s law.')
PARALLEL9=P(7,'In the circuit on the right, the resistors are wired','in parallel.')
PLUG9=P(7,'The diagram on the right shows the parts of an electrical plug.')
ELECTRON10=P(8,'The electron was discovered in 1897 by a British scientist, J.J. Thomson, while he was using a','In 1906 Thomson won the Nobel Prize in physics for his discovery.')
XRAY10=P(8,'During the course of his work, and completely','He won the Nobel Prize in physics in 1901.')
PASSAGE11=P(9,'One of the most common sights anywhere in the world are eyeglasses.','Adapted from https://science.howstuffworks.com/innovation/everyday‐innovations/lens6')
CANNON12=P(10,'A cannonball of mass 7 kg is shot from a cannon straight up into the air, with an initial','velocity of 50 m s⁻¹.')
GRAV12=P(10,'(acceleration due to gravity, g = 9.8 m s⁻²)')
CAP12=P(10,'A capacitor is used in the flash of a camera.')
STORE12=P(10,'In the flash circuit of a camera, energy is stored up and then','suddenly released. A capacitor stores energy when it is charged.')
MAGLEV12=P(11,'Magnetically levitated trains (known as maglev trains)','magnetic tracks.')
NUCLEAR12=P(11,'Both nuclear fission and nuclear fusion are processes by which the nuclei of atoms are','altered to create energy.')

# Section A: complete experiments and the measured data they refer to.
A('1i','Q1(i)',2,'How did the student measure the weight of the metre stick?',6,
 [menu('Newton balance // weighed it and multiplied by g',1,6,**partial(6,3))],'phys-u2','measuring-stick-weight',6,stem=[STEM1,MEASURE1],fig='q1-forces')
A('1ii','Q1(ii)',2,'How did she find the centre of gravity of the metre stick?',6,
 [R('suspended from string/thread and moved the string until it balanced',6,**partial(6,3))],'phys-u2','finding-centre-of-gravity',6,stem=[STEM1,MEASURE1],fig='q1-forces')
A('1iii','Q1(iii)',2,'How did she make sure that the metre stick was balanced and level?',6,
 [R('balanced: (hung weights until) no movement',3),R('level: horizontal / used a spirit level / visually level',3)],'phys-u2','balanced-and-level',6,stem=[STEM1],fig='q1-forces')
A('1iv','Q1(iv)',2,'Redraw the above diagram in your answerbook and include the weight of the metre',6,
 [C('copy diagram and show given forces',3),R('2 N shown downwards at 50 cm mark',3)],'phys-u2','adding-stick-weight',6,end='stick.',
 sq=SQ(6,'Redraw the above diagram in your answerbook and include the weight of the','metre stick.'),stem=[STEM1,MEASURE1],qfig='q1iv-question',fig='q1iv-solution')
A('1v','Q1(v)',2,'Using appropriate calculations, show that the first law of equilibrium is verified in this',6,
 [R('(Force up =) 8 + 4 = 12',6,**partial(12,3,extra='This is the partial credit for the whole response, not a third row.')),R('(Force down =) 3 + 2 + 7 = 12',6)],'phys-u2','verifying-first-law',12,end='experiment.',stem=[STEM1,MEASURE1,LAW1],fig='q1-forces')
A('1vi','Q1(vi)',2,'Using the 0 cm mark on the metre stick as the fulcrum, the calculations for the',6,
 [pt(S('(8×40) + (4×90)',nth=2),4,note_sel=S('(8×40) / (4×90)'),note_lead='One of these products earns',note='(2).')],'phys-u2','verifying-second-law',4,end='to verify the second law of equilibrium.',
 sq=SQ(6,'Using the 0 cm mark on the metre stick as the fulcrum, the calculations for the','calculations to verify the second law of equilibrium.'),stem=[STEM1,MEASURE1,LAW2],qfig='q1vi-question',fig='q1vi-solution')
A('2i','Q2(i)',3,'Draw a labelled diagram of the apparatus used in this experiment.',7,
 [R('calorimeter (with water)',3,note_sel=S('incorrect experiment, maximum mark 3 × 3','Note: no labels, deduct 1')),R('thermometer',3),R('ice',3),R('(electronic) balance',3)],'phys-u2','latent-heat-apparatus',12,stem=[STEM2])
A('2ii','Q2(ii)',3,'The ice was crushed before it was added to the water. Why was the ice crushed?',7,
 [menu('helps it to melt faster // reference (to increase in) the surface area',1,6)],'phys-u2','crushing-ice',6,stem=[STEM2])
TASKS.append(T('2iiia','Q2(iii)(a)','A',P(3,'Name (a) one mass measured and (b) one temperature measured.',piece=1,psep=' and '),
 [menu('(a) mass of empty calorimeter / mass of calorimeter and water (and ice) / mass of ice',1,6,sep=' / ')],
 'phys-u2','mass-measured',SQ(7,'Mass and temperature were measured in this experiment.','Name (a) one mass measured and (b) one temperature measured.'),6,stem=[STEM2,MEASURE2],cells='Scheme p7 prices the mass response at 6 within the combined 12/6 reprint.'))
TASKS.append(T('2iiib','Q2(iii)(b)','A',P(3,'Name (a) one mass measured and (b) one temperature measured.',piece=2,psep=' and '),
 [menu('(b) temperature of water initially/finally // temperature of (crushed) ice',1,6)],
 'phys-u2','temperature-measured',SQ(7,'Mass and temperature were measured in this experiment.','Name (a) one mass measured and (b) one temperature measured.'),6,stem=[STEM2,MEASURE2],cells='Scheme p7 prices the temperature response at 6 within the combined 12/6 reprint.'))
A('2iv','Q2(iv)',3,'Name an instrument used to measure one of the quantities listed in (iii) above.',7,
 [menu('(electronic) balance // thermometer',1,6)],'phys-u2','mass-or-temperature-instrument',6,stem=[STEM2,MEASURE2,ASK2])
A('2v','Q2(v)',3,'State one precaution used in this experiment, other than crushing the ice.',7,
 [anyn(None,1,4,options=items(S('Insulate the calorimeter','use lots of ice, avoid splashing, do quickly etc'),7),open_list=True,note_sel=S('any one'),note='4 marks.')],'phys-u2','latent-heat-precaution',4,stem=[STEM2])
# The two method columns in the refractive-index apparatus stay mutually exclusive.
TASKS.append(T('3i','Q3(i)','A',P(3,'Draw a labelled diagram of the apparatus used in this experiment.',nth=2),
 [pt(S('glass/(perspex) plastic block'),6,route='block',note=DSL),pt(S('raybox / laser / (optical) pins'),3,route='block'),pt(S('detail e.g. protractor, sheet of paper, normal, critical angle // mirror, ruler',piece=1,psep='//'),3,route='block',note_sel=S('other valid methods acceptable','Note: no labels, deduct 1')),
 pt(S('// container of liquid',piece=2,psep='//'),6,route='liquid'),pt(S('//(optical) pins',piece=2,psep='//'),3,route='liquid'),pt(S('detail e.g. protractor, sheet of paper, normal, critical angle // mirror, ruler',piece=2,psep='//'),3,route='liquid')],
 'phys-u2','refractive-index-apparatus',SQ(8,'Draw a labelled diagram of the apparatus used in this experiment.'),12,stem=[STEM3]))
A('3ii','Q3(ii)',3,'State the formula used in this experiment to calculate the refractive index, n.',8,
 [FR(8,(84,234,225,260),'sini/(sinr) // (real depth)/(apparent depth) // 1/(sin C)',6)],'phys-u2','refractive-index-formula',6,stem=[STEM3])
A('3iii-measurements','Q3(iii)',3,'What measurements did the student take during the experiment?',8,
 [menu('angles I and r // length of real and apparent depths // critical angle',1,6)],'phys-u2','refractive-index-measurements',6,
 sq=SQ(8,'What measurements did the student take during the experiment?','What instrument was used to take these measurements?'),stem=[STEM3],item=('measurements','Measurements'),cells='Scheme p8 prices measurements and instrument independently at 6 each.')
A('3iii-instrument','Q3(iii)',3,'What instrument was used to take these measurements?',8,
 [menu('protractor // metre stick',1,6,end='// protractor')],'phys-u2','refractive-index-instrument',6,
 sq=SQ(8,'What measurements did the student take during the experiment?','What instrument was used to take these measurements?'),stem=[STEM3,ASK3],item=('instrument','Measuring instrument'),cells='Scheme p8 prices measurements and instrument independently at 6 each.')
A('3iv','Q3(iv)',3,'Why should the experiment be repeated?',8,
 [menu('increase accuracy, take an average, to get data for a graph',1,4,sep=',')],'phys-u2','repeating-refraction',4,stem=[STEM3])
A('3v','Q3(v)',3,'Other than repeating the experiment, state one precaution that the student took to',8,
 [menu('use large angles of incidence // avoid no parallax',1,6)],'phys-u2','refraction-precaution',6,end='improve the accuracy of the experiment.',stem=[STEM3],decision='The official wording “avoid no parallax” is reproduced verbatim; no invented replacement.')
for key,qtext,ans,concept in [
 ('i','Name the instrument used to measure the length l of the wire.','metre stick / ruler','wire-length-instrument'),
 ('ii','Name the instrument used to measure the resistance R of the wire.','ohmmeter / (digital) multimeter','wire-resistance-instrument'),
 ('iii','Name the instrument used to measure the diameter d of the wire.','micrometer (screw gauge) // digital/ Vernier callipers','wire-diameter-instrument')]:
 A('4'+key,'Q4('+key+')',3,qtext,9,[menu(ans,1,6,sep='//' if key=='iii' else ' / ',**(partial(6,3) if key=='iii' else {}))],'phys-u2',concept,6,stem=[STEM4],fig='q4-data')
A('4iv','Q4(iv)',3,'Use the data to calculate the average diameter of the wire.',9,
 [R('d= ( 0.00024 + 0.00028 + 0.00023) ÷ 3 = 0.00025 m',6,**partial(6,3))],'phys-u2','average-wire-diameter',6,stem=[STEM4],fig='q4-data')
A('4v','Q4(v)',3,'Calculate the cross‐sectional area A of the wire.',9,
 [FR(9,(84,407,238,432),'πd²/4 = (19.6×10⁻⁸)/4 =4.9 ×10⁻⁸ m²',6,**partial(6,3,extra='Answer consistent with (iv) above is accepted.'))],
 'phys-u2','wire-cross-section',6,stem=[STEM4],fig='q4-data')
A('4vi','Q4(vi)',3,'Use the formula',9,
 [FR(9,(84,487,285,512),'ρ= RA/l = ((22.8)(4.9×10⁻⁸))/0.98 =1.14 ×10⁻⁶ Ω m',10,note_sel=S('correct substitution of 2 quantities into the equation','partial answer'),note='Correct substitution of two quantities: 7; partial answer: 3. Answer consistent with (v) is accepted.')],
 'phys-u2','wire-resistivity',10,end='to calculate the resistivity of the wire.',sq=SQ(9,'Use the formula ρ=','to calculate the resistivity of the wire.'),stem=[STEM4],qfig='q4vi-question')
FIGURES={}

# Section B: all short options, every long question and all four Q12 choices.
A('5a','Q5(a)',4,'State the principle of conservation of momentum.',10,
 [menu('(in a closed system the total) momentum before (interaction) = (the total )momentum after //',1,7,end='m₁u₁ + m₂u₂ =m₁v₁ + m₂v₂',**partial(7,4))],'phys-1-2','conservation-of-momentum',7)
A('5b','Q5(b)',4,'A force of 2500 N acts on a car of mass 1000 kg.',10,
 [FR(10,(77,176,191,201),'a= F/m = 2500/(10³) = 2.5 m s⁻²',7,**partial(7,4))],'phys-1-2','car-acceleration',7,end='Calculate the acceleration of the car.')
A('5c','Q5(c)',4,'Which of the following is the unit of electrical charge?',10,
 [R('coulomb',7)],'phys-3-1','charge-unit',7,end='volt',sq=SQ(10,'Which of the following is the unit of electrical charge?'))
A('5d','Q5(d)',4,'State Boyle’s law.',10,
 [FR(10,(77,302,340,324),'( for fixed mass at constant temperature) PV = k // P∝ 1/V',7,**partial(7,4))],'phys-1-3','boyles-law',7)
A('5e','Q5(e)',4,'A crane moves a load of weight 7000 N to the top of a',10,
 [FR(10,(77,389,232,414),'P= work/(time) = Fs/t = (7000)(4)/20 = 1400 W',7,**partial(7,4))],'phys-1-4','crane-power',7,end='this work. Calculate the power output of the crane.',sq=SQ(10,'A crane moves a load of weight 7000 N to the top of a roof which is 4 m high.','Calculate the power output of the crane.'))
A('5f','Q5(f)',4,'The boiling point of water is 100 °C. Convert this',10,[R('373(.15) K',7,**partial(7,4))],
 'phys-2-1','kelvin-conversion',7,end='temperature to kelvin (K).',sq=SQ(10,'The boiling point of water is 100 °C. Convert this temperature to kelvin (K).'))
A('5g','Q5(g)',4,'Explain why it is possible to hear around corners but not to see around corners.',10,
 [menu('sound diffracts more // sound has a bigger wavelength',1,7,**partial(7,4))],'phys-2-4','sound-diffraction',7)
A('5h','Q5(h)',4,'Name the three primary colours of light.',10,
 [anyn(None,3,3,steps=[3,2,2],options=[S('red, green and blue',piece=1,psep=','),S('red, green and blue',piece=[2,1],psep=[',',' and ']),S('red, green and blue',piece=[2,2],psep=[',',' and '])],note='Three: 7; any two: 5; any one: 3. When more than three colours are given cancelling may apply.')],
 'phys-2-5','primary-colours',7,decision='One required three-item response; the scheme explicitly supplies the 7/5/3 scale.')
A('5i','Q5(i)',4,'What is a semiconductor?',10,
 [R('material whose resistivity lies between that of an insulator and a conductor',7,**partial(7,4))],'phys-3-4','semiconductor',7)
A('5j','Q5(j)',4,'Name the three forms of nuclear radiation.',10,
 [menu('α, β, γ',3,3,sep=',',steps=[3,2,2],note='Three: 7; any two: 5; any one: 3.')],'phys-4-4','three-nuclear-radiations',7)
A('6i','Q6(i)',5,'A jet starts from rest and accelerates along a runway to a top',11,
 [R('v= u + at ⟹ 28 = 0 + a(7) i.e. a = 4 m s⁻²',9,note_sel=S('one error','partial answer'),note='One error: 6; partial answer: 3.')],'phys-1-1','jet-acceleration',9,end='speed of 28 m s⁻¹ in 7 seconds. What is the acceleration of the jet?',
 sq=SQ(11,'A jet starts from rest and accelerates along a runway to a top speed of 28 m s⁻¹ in','7 seconds. What is the acceleration of the jet?'))
A('6ii','Q6(ii)',5,'Acceleration is a vector quantity, while time is a scalar quantity.',11,
 [R('vector quantities have a direction (scalar quantities don’t)',6,**partial(6,3))],'phys-1-1','vectors-and-scalars',6,end='Distinguish between a vector quantity and a scalar quantity.',sq=SQ(11,'Acceleration is a vector quantity, while time is a scalar quantity. Distinguish between a','vector quantity and a scalar quantity.'))
A('6iii','Q6(iii)',5,'The moon is constantly in motion, orbiting the Earth. Explain why an astronaut',11,
 [R('when the moon orbits it changes its direction of motion so its velocity changes',6,**partial(6,3))],'phys-1-5','orbital-velocity',6,end='standing on the moon has a constant speed but a changing velocity.',sq=SQ(11,'The moon is constantly in motion, orbiting the Earth. Explain why an astronaut standing','on the moon has a constant speed but a changing velocity.'))
A('6iv','Q6(iv)',5,'Armstrong had a mass of 90 kg. Calculate his weight on Earth. Include units in your',11,
 [R('weight = m g = (90)(9.8) = 882 N',9,note_sel=S('one error e.g. incorrect unit','partial answer e.g. correct unit /N'),note='One error: 6; partial answer: 3.')],'phys-1-2','earth-weight',9,end='answer.',sq=SQ(11,'Armstrong had a mass of 90 kg.','Calculate his weight on Earth. Include units in your answer.'),stem=[GRAV6])
A('6v','Q6(v)',5,'What was Armstrong’s mass on the moon?',11,[R('90 kg / the same',6)],'phys-1-2','moon-mass',6,stem=[MASS6])
A('6vi','Q6(vi)',5,'Armstrong’s weight on the moon was only 17% of his weight on Earth.',11,
 [menu('smaller mass of moon // less gravitational force',1,5,**partial(5,3))],'phys-1-5','moon-gravity',5,end='Explain why.')
A('6vii','Q6(vii)',5,'Define pressure.',11,
 [FR(11,(77,551,331,577),'P= F/A // pressure is the force per unit area',6,**partial(6,3))],'phys-1-3','pressure-definition',6,stem=[FOOT6])
A('6viii','Q6(viii)',5,'Calculate the pressure Armstrong exerted on the surface of the moon.',11,
 [FR(11,(77,611,191,635),'P= (882)(0.17)/0.03 = 4998 Pa',9,note_sel=S('one error','partial answer'),note='One error: 6; partial answer: 3.')],'phys-1-3','moon-pressure',9,stem=[MASS6,GRAV6,MOON6,FOOT6])
A('7i','Q7(i)',6,'Which of these characteristics can be quantified as a frequency?',12,[R('pitch',6)],'phys-2-6','pitch-frequency',6,stem=[STEM7])
A('7ii','Q7(ii)',6,'Name the property of a wave that affects its loudness.',12,[R('amplitude',6,**partial(6,3))],'phys-2-6','loudness-amplitude',6,stem=[STEM7])
A('7iii','Q7(iii)',6,'When the musician plays the A string on his guitar, the frequency of the note is 110 Hz.',12,
 [FR(12,(91,242,234,267),'v=fλ ⟹ λ= 340/110 =3.09 m',6,**partial(6,3))],'phys-2-4','sound-wavelength',6,end='The speed of sound in air is 340 m s⁻¹. What is the wavelength of the note?',sq=SQ(12,'When the musician plays the A string on his guitar, the frequency of the note is 110 Hz. The','speed of sound in air is 340 m s⁻¹. What is the wavelength of the note?'))
A('7iv','Q7(iv)',6,'Describe an experiment to show that sound cannot travel through a vacuum.',12,
 [menu('apparatus: (bell) jar, sound source / electric bell',1,3,sep=',',note='Apparatus row: any one, 3 marks.'),R('(vacuum) pump',3),R('procedure: turn on pump / pump out the air',3),R('observation/conclusion: loudness decreases as air is removed /no sound heard',3,note_sel=S('accept valid alternatives','a labelled diagram may merit full marks'))],
 'phys-2-6','sound-vacuum-experiment',12)
A('7v','Q7(v)',6,'Describe how to demonstrate the Doppler effect in a laboratory.',12,
 [R('apparatus: buzzer/sound source',3),menu('with fixed frequency/pitch, string',1,3,sep=','),R('procedure: turn on sound source and rotate using string',3),R('observation/conclusion: frequency /pitch changes (as sound source moves closer/away)',3)],
 'phys-2-4','doppler-demonstration',12,stem=[DOPPLER7])
A('7vi','Q7(vi)',6,'Distinguish between a longitudinal wave and a transverse wave. A labelled diagram',12,
 [anyn(None,2,6,steps=[6,3],options=[S('the disturbance is parallel to the direction of motion for longitudinal waves'),S('the disturbance is perpendicular to the direction of motion for transverse waves')],note_sel=S('transverse waves may be polarised','a labelled diagram may merit full marks'),note='Two correct lines: 9; one: 6. “Transverse waves may be polarised” earns 6; the stated partial answer earns 3.')],
 'phys-2-4','longitudinal-transverse',9,end='may help your answer.',stem=[WAVES7],decision='A paired comparison priced 9/6/3, not two independently priced six-mark tasks.')
A('7vii','Q7(vii)',6,'Which one of these phenomena do sound waves not undergo? Explain why.',12,
 [menu('polarisation as they are not transverse /e.m. waves //',1,5,end='polarisation as they are longitudinal waves',**partial(5,3))],'phys-2-4','sound-polarisation',5,stem=[POOL7])
A('8i','Q8(i)',6,'Is the student’s statement correct? Explain your answer.',13,[R('no, (the bath has) more water/mass',6,**partial(6,3))],'phys-2-2','temperature-versus-heat',6,stem=[BATH8])
A('8ii','Q8(ii)',6,'What is meant by a thermometric property?',13,[R('property which changes (continually) with changing temperature',6,**partial(6,3))],'phys-2-1','thermometric-property',6,stem=[THERM8])
A('8iii','Q8(iii)',6,'Name another example of a thermometric property.',13,
 [anyn(None,1,6,options=items(S('colour, resistance, pressure, volume, emf, voltage, etc'),6),open_list=True,note='The reprinted question prices this 6 or 3; the scheme supplies examples but no separate partial-answer wording here.')],'phys-2-1','thermometric-example',6,stem=[THERM8])
A('8iv','Q8(iv)',6,'Define specific heat capacity.',13,[R('energy required to raise the temperature of 1 kg by 1 K / 1 ⁰C',9,note_sel=S('one error','partial answer'),note='One error: 6; partial answer: 3.')],'phys-2-2','specific-heat-capacity',9,stem=[BRICK8])
A('8v','Q8(v)',6,'Why does the material in the bricks need to have a high specific heat capacity?',13,[R('so that they can store a lot of heat energy',5,**partial(5,3))],'phys-2-2','storage-heater-bricks',5,stem=[BRICK8])
A('8vi','Q8(vi)',6,'Calculate the heat energy gained by the water in the kettle.',13,
 [R('E = m c dθ = (1.5)(4200)(88‐15) = 4.599 × 10⁵ J',12,note_sel=S('one error','partial answer'),note='One error: 9; at least two quantities correctly substituted: 6; partial answer: 3.')],'phys-2-2','kettle-energy',12,stem=[KETTLE8,HEAT8])
A('8vii','Q8(vii)',6,'Apart from boiling, name one other change of state that can happen to water.',13,[menu('freezing, condensing, melting',1,6,sep=',',**partial(6,3))],'phys-2-2','change-of-state',6,stem=[STATE8])
A('8viii','Q8(viii)',6,'What is meant by latent heat?',13,[R('latent heat is the heat required to change the state of a substance without a change in',6,end='temperature',**partial(6,3))],'phys-2-2','latent-heat',6,stem=[STATE8])
A('9ai','Q9(a)(i)',7,'What is meter A?',14,[R('ammeter',6,**partial(6,3))],'phys-3-3','ammeter',6,stem=[CIRCUIT9],fig='q9a-circuit')
A('9aii','Q9(a)(ii)',7,'What is meter V?',14,[R('voltmeter',6,**partial(6,3))],'phys-3-3','voltmeter',6,stem=[CIRCUIT9],fig='q9a-circuit')
A('9aiii','Q9(a)(iii)',7,'Which of the graphs below shows Ohm’s',14,
 [R('Graph 1',6),menu('the straight line through the origin // I ∝ V //',1,6,end='answer consistent with graph',**partial(6,3))],'phys-3-3','ohms-law-graph',12,end='Explain your answer.',sq=SQ(14,'Which of the graphs below shows Ohm’s law being obeyed? Explain your answer.'),fig='q9a-graphs')
A('9bi','Q9(b)(i)',7,'Calculate the total resistance in the circuit.',14,
 [FR(14,(112,365,301,391),'1/R = ⅕ + ¼ = (4+5)/20 ⟹R= 20/9 =2.2 Ω',6,**partial(6,3))],'phys-3-3','parallel-resistance',6,stem=[PARALLEL9],fig='q9b-parallel')
A('9bii','Q9(b)(ii)',7,'Calculate the current flowing through',14,
 [FR(14,(112,439,236,464),'I= V/R =12 ÷ 2.2 =5.4 A',6,note_sel=S('answer consistent with (i) above','partial answer e.g. correct equation'),note='Answer consistent with (i): 6; partial answer: 3.')],'phys-3-3','parallel-current',6,end='the circuit.',stem=[PARALLEL9],fig='q9b-parallel')
A('9ci','Q9(c)(i)',7,'Name the wire labelled A.',14,[R('earth',6,**partial(6,3,sel='partial e.g. green/yellow, live'))],'phys-3-3','earth-wire',6,stem=[PLUG9],fig='q9c-plug')
A('9cii','Q9(c)(ii)',7,'Name the wire labelled B.',14,[R('live',6,**partial(6,3,sel='partial e. g. brown, earth'))],'phys-3-3','live-wire',6,stem=[PLUG9],fig='q9c-plug')
A('9ciii','Q9(c)(iii)',7,'State the function of the fuse.',14,[menu('break the circuit when current too big',1,6,end='fire /damage',**partial(6,3,sel='partial'))],'phys-3-3','fuse-function',6,stem=[PLUG9],fig='q9c-plug')
A('9civ','Q9(c)(iv)',7,'There are two other devices used in the',14,[menu('circuit breaker/ trip switch, RCD , RCB, MCB, ELCB',1,2,sep=',')],'phys-3-3','circuit-safety-device',2,end='these devices.',sq=SQ(14,'There are two other devices used in the distribution box of a domestic circuit that carry out a','Name one of these devices.'),stem=[PLUG9],fig='q9c-plug')
A('10i','Q10(i)',8,'State two properties of an electron.',15,
 [menu('(negative) charge, small mass, orbits outside nucleus, deflected by electric/magnetic fields',2,3,sep=',',note_sel=S('partial answer e.g. one correct property'),note='Two correct properties: 6; one: 3.')],'phys-4-2','electron-properties',6,stem=[ELECTRON10])
A('10ii','Q10(ii)',8,'How are the electrons produced in a cathode ray tube?',15,[R('thermionic emission',6,**partial(6,3))],'phys-4-2','thermionic-emission',6,stem=[ELECTRON10])
A('10iii','Q10(iii)',8,'How could the beam of electrons be deflected?',15,[menu('by electric / XY plates // magnetic fields',1,6,**partial(6,3))],'phys-4-2','electron-beam-deflection',6,stem=[ELECTRON10])
A('10iv','Q10(iv)',8,'What happens when the beam of electrons strikes the screen?',15,[menu('lose energy, fluorescence, KE converted to light energy',1,6,sep=',',**partial(6,3))],'phys-4-2','fluorescent-screen',6,stem=[ELECTRON10])
A('10v','Q10(v)',8,'State one use of a cathode ray tube.',15,[anyn(None,1,6,options=items(S('CRO, old TV monitors, ECG screens, etc.'),3),open_list=True,**{k:v for k,v in partial(6,3).items() if k!='note_lead'})],'phys-4-2','cathode-ray-tube-use',6,stem=[ELECTRON10])
A('10vi','Q10(vi)',8,'What are X‐rays?',15,[menu('high energy electromagnetic radiation // electromagnetic radiation of short wavelength',1,6,**partial(6,3))],'phys-4-2','x-rays',6,stem=[XRAY10])
A('10vii','Q10(vii)',8,'The photograph shows an X‐ray tube.',15,[menu('its large metal target absorbs most of this heat energy // coolant / heat sink',1,6,**partial(6,3))],'phys-4-2','x-ray-tube-cooling',6,end='of heat energy.',sq=SQ(15,'The photograph shows an X‐ray tube. When the electrons strike the target, a large amount of','designed to take account of this large amount of heat energy.'),stem=[XRAY10],fig='q10-xray')
A('10viii','Q10(viii)',8,'Why might an X‐ray tube be surrounded by lead shielding?',15,[R('for protection from ( ionising) radiation',6,**partial(6,3))],'phys-4-2','x-ray-shielding',6,stem=[XRAY10])
A('10ix','Q10(ix)',8,'State one use of X‐rays.',15,[menu('specific use e.g. check for broken bones, locate cracks in metal pipes',1,6,sep=',',**partial(6,3,sel='general use e.g. in medicine /industry'))],'phys-4-2','x-ray-use',6,stem=[XRAY10])
A('10x','Q10(x)',8,'State one hazard associated with X‐rays.',15,[R('can cause skin burns /cancer/ionise cells, death, etc.',2)],'phys-4-2','x-ray-hazard',2,stem=[XRAY10])
A('11a','Q11(a)',9,'Name the part of the eye where an image is formed.',16,[R('retina',7,**partial(7,4))],'phys-2-3','retina',7,stem=[PASSAGE11])
A('11b','Q11(b)',9,'What is the function of the pupil?',16,[R('allows light enter the eye',7,**partial(7,4))],'phys-2-3','pupil',7,stem=[PASSAGE11])
A('11c','Q11(c)',9,'The eye can focus light from both nearby and distant objects. Describe how the eye',16,[menu('the lens has a different power for near and far objects // lens changes shape',1,7,**partial(7,4,end='onto the retina'))],'phys-2-3','eye-focusing',7,end='changes to allow this to happen.',stem=[PASSAGE11])
A('11d','Q11(d)',9,'Name the two most common eye defects.',16,[menu('myopia (short sightedness) and hyperopia (long sightedness)',2,4,sep=' and ',steps=[4,3],**partial(7,4))],'phys-2-3','eye-defects',7,stem=[PASSAGE11])
A('11e','Q11(e)',9,'What type of lens corrects short sightedness? Draw a sketch of this lens.',16,[R('diverging/ concave lens named and sketched',7,**partial(7,4))],'phys-2-3','short-sight-lens',7,stem=[PASSAGE11],fig='q11e-solution',decision='Naming and sketch are one printed seven-mark response; no sub-tariffs are supplied.')
A('11f','Q11(f)',9,'Copy the diagram below into your answerbook and complete the ray diagram to form',16,[R('image formed from 2 or more correct rays',7,**partial(7,4))],'phys-2-3','real-image-ray-diagram',7,end='a real image.',sq=SQ(16,'Copy the diagram below into your answerbook and complete the ray diagram to form a','real image.'),stem=[PASSAGE11],qfig='q11f-question',fig='q11f-solution')
A('11g','Q11(g)',9,'The power required to clearly view a nearby object is 38 m⁻¹. A person with an eye',16,
 [FR(16,(98,702,334,725),'P = 38 – 32 = 6 m⁻¹ f = 1/P = 1/6 m / 16.7 cm',7,**partial(7,4))],'phys-2-3','corrective-lens-power',7,end='correct this defect? What is the focal length of this lens?',sq=SQ(16,'The power required to clearly view a nearby object is 38 m⁻¹. A person with an eye defect has a','What is the focal length of this lens?'),stem=[PASSAGE11],decision='The complete power-plus-focal-length calculation is priced 7, partial 4. No independent seven marks for each result.')
A('11h','Q11(h)',9,'Light undergoes refraction as it passes through a lens. What is meant by refraction?',16,[R('the bending of light when it goes from one medium to another',7,**partial(7,4))],'phys-2-3','refraction',7,end='What is meant by refraction?',stem=[PASSAGE11])
A('12ai','Q12(a)(i)',10,'State the principle of conservation of energy.',17,[R('energy cannot be created or destroyed but can be converted from one form to another',6,**partial(6,3))],'phys-1-4','conservation-of-energy',6,stem=[CANNON12])
A('12aii','Q12(a)(ii)',10,'Calculate the cannonball’s kinetic energy as it is fired.',17,[FR(17,(105,164,249,187),'KE = ½ m v² = ½ (7)(50)² = 8750 J',6,**partial(6,3))],'phys-1-4','cannonball-kinetic-energy',6,stem=[CANNON12])
A('12aiii','Q12(a)(iii)',10,'As the cannonball rises, its kinetic energy is converted into another form of',17,[R('potential (energy)',4)],'phys-1-4','potential-energy',4,end='energy. Name this energy.',sq=SQ(17,'As the cannonball rises, its kinetic energy is converted into another form of energy.','Name this energy.'),stem=[CANNON12])
A('12aiv','Q12(a)(iv)',10,'Calculate the greatest height reached by the cannonball.',17,[R('KE = 8750 = mgh =(7)(9.8) h // v²=u²+ 2as = (50)²+2(‐9.8)s ⟹s/h=127.55 m',6,**partial(6,3))],'phys-1-4','cannonball-height',6,stem=[CANNON12,GRAV12])
A('12av','Q12(a)(v)',10,'The cannonball has a volume of 0.0009 m³.',17,[FR(17,(105,343,246,367),'ρ= M/V = 7/0.0009 = 7777.8 kg m⁻³',6,**partial(6,3))],'phys-1-3','cannonball-density',6,end='Calculate the density of the cannonball.',stem=[CANNON12])
A('12bi','Q12(b)(i)',10,'Define capacitance.',17,[FR(17,(105,428,133,452),'C = Q/V',6,**partial(6,3))],'phys-3-2','capacitance',6,stem=[CAP12])
A('12bii','Q12(b)(ii)',10,'State the unit of capacitance.',17,[R('Farad / F',3)],'phys-3-2','farad',3,stem=[CAP12])
A('12biii','Q12(b)(iii)',10,'The light energy emitted by a flash is supplied by a',17,[FR(17,(105,540,197,564),'C = Q/V = 0.025/250 = 10⁻⁴ F',6,**partial(6,3))],'phys-3-2','flash-capacitance',6,end='Calculate the capacitance.',sq=SQ(17,'The light energy emitted by a flash is supplied by a capacitor. The charge on the capacitor','Calculate the capacitance.'),stem=[CAP12])
A('12biv','Q12(b)(iv)',10,'The circuit shown can be used to',17,
 [anyn(None,2,6,steps=[6,3],options=[S('throw the switch to close the bottom circuit and observe'),S('the bulb lights briefly due to the energy from the capacitor.')],note_sel=S('partial e.g. charge the capacitor'),note='Two lines: 9; one line: 6; partial: 3.')],'phys-3-2','capacitor-stores-energy',9,end='Explain how the circuit is used.',sq=SQ(17,'The circuit shown can be used to demonstrate that a','capacitor stores energy. Explain how the circuit is used.'),stem=[CAP12,STORE12],fig='q12b-capacitor')
A('12bv','Q12(b)(v)',10,'State another use for a capacitor.',17,[anyn(None,1,4,options=items(S('specific use: conducts a.c., (radio) tuning/filtering/smoothing ,timing, phone charger, etc.'),4),open_list=True,note_sel=S('general use: computer, car'),note='General use: 2 marks.')],'phys-3-2','capacitor-use',4,stem=[CAP12])
A('12ci','Q12(c)(i)',11,'Like poles repel, and this is the property of',18,[anyn(None,1,6,options=items(S('unlike poles attract, magnets attract certain metals, magnets are strongest','at the poles, etc.'),3),open_list=True,note_sel=S('partial answer'),note='Partial answer: 3 marks.')],'phys-3-5','magnet-properties',6,end='State one other property of magnets.',sq=SQ(18,'Like poles repel, and this is the property of magnets that is','Used in maglev trains. State one other property of magnets.'),stem=[MAGLEV12])
A('12cii','Q12(c)(ii)',11,'What is meant by a magnetic field?',18,[R('region/space (around a magnet) within which a magnetic force is experienced',6,**partial(6,3))],'phys-3-5','magnetic-field',6,stem=[MAGLEV12])
A('12ciii','Q12(c)(iii)',11,'Describe an experiment to plot the magnetic field of a bar magnet.',18,
 [R('apparatus: magnet',3,note=DSL),pt(S('(plotting) compass'),3,route='compass'),pt(S('procedure: use the apparatus to locate the field lines e.g. (place the compass on','the paper and) mark the dots // sprinkle filings',piece=1,psep='//'),3,route='compass'),pt(S('detail: join the dots/ show field lines / lines go from north to south/ field lines are','// tap filings',piece=1,psep='//'),3,route='compass',note_sel=S('marks may be obtained from a diagram')),
 pt(S('// iron filings',piece=2,psep='//'),3,route='filings'),pt(S('the paper and) mark the dots // sprinkle filings',piece=2,psep='//'),3,route='filings'),pt(S('// tap filings',piece=2,psep='//'),3,route='filings')],
 'phys-3-5','plotting-magnetic-field',12,stem=[MAGLEV12],decision='Magnet common to both methods. Compass procedure/detail and iron-filings procedure/detail remain complete alternatives.')
A('12civ','Q12(c)(iv)',11,'State one other use of magnets.',18,[anyn(None,1,4,options=items(S('compass, to keep a fridge door closed, electric bell, electric motor, transformer,','electromagnet, electromagnetic induction, moving coil meters, etc.'),8),open_list=True,note_sel=S('partial answer'),note='Partial answer: 2 marks.')],'phys-3-5','magnet-use',4,stem=[MAGLEV12])
A('12di-protons','Q12(d)(i)',11,'How many protons are in this uranium atom?',18,[R('92 protons',4)],'phys-4-1','uranium-protons',4,
 sq=SQ(18,'How many protons are in this uranium atom?','How many neutrons are in this uranium atom?'),stem=[NUCLEAR12],fig='q12d-uranium238',item=('protons','Protons'),cells='Scheme p18 prints 4 beside protons and 4 beside neutrons within the combined 8/4 heading.')
A('12di-neutrons','Q12(d)(i)',11,'How many neutrons are in this uranium atom?',18,[R('146 neutrons',4)],'phys-4-1','uranium-neutrons',4,
 sq=SQ(18,'How many protons are in this uranium atom?','How many neutrons are in this uranium atom?'),stem=[NUCLEAR12],fig='q12d-uranium238',item=('neutrons','Neutrons'),cells='Scheme p18 prints 4 beside protons and 4 beside neutrons within the combined 8/4 heading.')
A('12dii','Q12(d)(ii)',11,'U',18,[R('atoms with the same atomic number and with different mass numbers',6,**partial(6,3))],'phys-4-1','isotopes',6,end='is another isotope of uranium. What are isotopes?',sq=SQ(18,'U','is another isotope of uranium. What are isotopes?',nth=2),qfig='q12dii-question')
A('12diii','Q12(d)(iii)',11,'Distinguish between nuclear fission and nuclear fusion.',18,
 [anyn(None,2,3,options=[S('Fission is the breaking up a nucleus'),S('Fusion is the joining of nuclei into one larger nucleus','(with the emission of energy)')],note='Two correct lines: 6; one correct line: 3.')],'phys-4-6','fission-and-fusion',6,stem=[NUCLEAR12])
A('12div','Q12(d)(iv)',11,'State one advantage and one disadvantage of nuclear energy.',18,
 [menu('Advantage: lots of energy, no carbon emissions, no pollution',1,4,sep=','),anyn(None,1,4,options=items(S('Disadvantage: danger of leaked radiation, health risk, etc.'),2),open_list=True,note_sel=S('partial answer e.g. in reverse order'),note='Reverse-order partial answer: 4 for the response; do not add this to correctly labelled rows.')],
 'phys-4-6','nuclear-energy-pros-cons',8,stem=[NUCLEAR12])

SELECTION_SCAN=[
 ('paper',4,'the following','Q5 best eight of ten at 7 each; all ten distinct tasks retained.'),
 ('paper',4,'the following','Q5(c) one answer from the complete four-unit pool; one card.'),
 ('paper',6,'both','Bath/cup quotation describes equal temperatures; not a candidate choice.'),
 ('paper',9,'the following','Read the following passage: retained with its questions.'),
 ('paper',9,'or','Nearby or far away describes eye focusing in the passage.'),
 ('paper',9,'both','Q11(c) describes near and distant objects; one response.'),
 ('paper',10,'any two','Q12 choose two of four letters, each 28; all four retained separately.'),
 ('paper',10,'the following','The same Q12 outer choice; no combinations.'),
 ('paper',11,'both','Fission and fusion description, not a choice.'),
]
FIGURES={
 'q1-forces':('paper',2,(122,306,490,475),SEC,[],'Metre stick: upward forces 8 N at 40 cm and 4 N at 90 cm; downward 3 N at 30 cm and 7 N at 70 cm. The stick’s own weight is not shown.',False),
 'q1iv-question':('paper',2,(82,147,545,512),SEC,[],'Q1 experiment and measured weight 2 N at the 50 cm centre of gravity; the original force diagram and part (iv) asking the student to add the stick’s weight.',False),
 'q1iv-solution':('scheme',6,(82,362,419,497),SEC,[],'Official completed force diagram including a downward red 2 N arrow at 50 cm.',True),
 'q1vi-question':('paper',2,(82,147,546,740),SEC,[],'The complete Q1 force diagram and measured stick weight, both laws, and the moment table to be completed using the 0 cm fulcrum.',False),
 'q1vi-solution':('scheme',6,(115,710,470,740),SEC,[],'Official moment table: clockwise (3×30)+(2×50)+(7×70)=680 N cm; anticlockwise (8×40)+(4×90)=680 N cm.',True),
 'q4-data':('paper',3,(108,494,542,563),SEC,[],'Nichrome-wire data: R=22.8 Ω; l=0.98 m; diameter readings 0.00024, 0.00028 and 0.00023 m. Diagram identifies the circular cross-sectional area.',False),
 'q4vi-question':('paper',3,(82,451,546,706),SEC,[],'Q4 experiment, complete data table and circular wire cross section, ending with the printed formula ρ=RA/l and the request to calculate resistivity.',False),
 'q9a-circuit':('paper',7,(318,56,541,201),SEC,['A','V'],'Ohm’s-law circuit with the labelled A and V meters, battery, variable resistor and test resistor.',False),
 'q9a-graphs':('paper',7,(108,207,541,328),SEC,[],'All three labelled current-versus-voltage options: Graph 1 straight through the origin, Graph 2 curved, Graph 3 curves upward steeply as voltage rises.',False),
 'q9b-parallel':('paper',7,(365,337,553,516),SEC,[],'A 12 V supply connected across 5 Ω and 4 Ω resistors in parallel.',False),
 'q9c-plug':('paper',7,(331,539,565,725),SEC,['A','B'],'Original plug diagram retaining labels A, B, Neutral, Fuse, Cable grip and Cable.',False),
 'q10-xray':('paper',8,(324,322,541,438),SEC,[],'The paper’s photograph of an X-ray tube in its glass envelope, showing the metal target and electrodes.',False),
 'q11e-solution':('scheme',16,(306,516,330,555),SEC,[],'The official concave/diverging-lens sketch.',True),
 'q11f-question':('paper',9,(83,534,545,660),SEC,[],'Part (f) and its unfinished converging-lens diagram: upright object on the left, horizontal axis and both focal points marked f.',False),
 'q11f-solution':('scheme',16,(261,577,470,660),SEC,[],'Official completed ray diagram with red dashed rays forming an inverted real image on the right of the converging lens.',True),
 'q12b-capacitor':('paper',10,(352,556,540,777),SEC,[],'Two-position switch connects a capacitor to a battery for charging or a bulb for discharging; all three components are labelled.',False),
 'q12d-uranium238':('paper',11,(140,315,265,337),SEC,[],'The printed isotope notation: uranium U with mass number 238 and atomic number 92, followed by “is a uranium atom”.',False),
 'q12dii-question':('paper',11,(112,372,425,395),SEC,[],'Part (ii): uranium U with mass number 235 and atomic number 92; “is another isotope of uranium. What are isotopes?”',False),
}
# This ray-construction task is self-contained; its original question figure
# supplies the complete ask and diagram. No passage is needed for constructing rays.
next(t for t in TASKS if t['key']=='11f')['stem']=[]
# Select the second U heading, avoiding the preceding uranium-238 prompt.
next(t for t in TASKS if t['key']=='12dii')['q']=P(11,'U','is another isotope of uranium. What are isotopes?',nth=2)

# Exact, visually checked partial-credit cells. Bracketed alternatives must
# not be summed with the full award by the generic cell cross-check.
_PARTIAL_CELLS={
 '1vi':'The scheme gives the complete moment sum 4, or either single product (2); these are alternatives.',
 '4vi':'The scheme gives the complete resistivity calculation 10, two substitutions (7), or partial (3).',
 '6i':'The scheme prices the acceleration answer 9, one error (6), or partial (3).',
 '6iv':'The weight answer is 9, one error such as incorrect unit (6), or partial such as correct unit (3).',
 '6viii':'The moon pressure calculation is 9, one error (6), or partial (3).',
 '7vi':'Two correct comparison lines earn 9; one line or the polarisation alternative earns (6); partial earns (3).',
 '8iv':'Definition earns 9, one error (6), partial (3).',
 '8vi':'Kettle energy answer earns 12; one error (9), two substitutions (6), or partial (3).',
 '10ix':'A specific X-ray use earns 6; a general use is a partial alternative (3).',
 '12biv':'Both explanation lines earn 9, one earns (6), partial earns (3).',
 '12bv':'Specific capacitor use earns 4; a general use earns (2) instead.',
}
for t in TASKS:
 if t['key'] in _PARTIAL_CELLS:t['cells']=_PARTIAL_CELLS[t['key']]
next(t for t in TASKS if t['key']=='11c')['sq']=SQ(16,'(c ) The eye can focus light from both nearby and distant objects. Describe how the eye','changes to allow this to happen.')
next(t for t in TASKS if t['key']=='12dii')['sq']=SQ(18,'U','is another isotope of uranium. What are isotopes?',after='partial answer e.g. 92 neutrons and 146 protons')
ASK_EXEMPT=[
 (6,'When a musician moves his fingers up and down the strings of a guitar,','Description of changing string frequency; retained in the Q7 stem, not an ask.'),
 (6,'the frequency of the note changes. When the strings are at their','Continuation of the Q7 descriptive stem; not an ask.'),
 (9,'When you look at an object, an image is formed on the retina. The','Sentence inside the Q11 reading passage; not a separate question.'),
]
# Canonical curriculum nodes, checked against the registry-backed crosswalk.
_TOPIC_FIX={
 '5g':'phys-2-3','5h':'phys-2-4','5i':'phys-3-3','6iii':'phys-1-6',
 '6vii':'phys-1-2','6viii':'phys-1-2','7i':'phys-2-5','7ii':'phys-2-5',
 '7iii':'phys-2-2','7iv':'phys-2-5','7v':'phys-2-7','7vi':'phys-2-2','7vii':'phys-2-7',
 **{f'8{x}':'phys-2-1' for x in ['i','ii','iii','iv','v','vi','vii','viii']},
 **{f'10{x}':'phys-4-1' for x in ['i','ii','iii','iv','v']},
 '12av':'phys-1-2',**{f'12c{x}':'phys-3-4' for x in ['i','ii','iii','iv']},
 '12di-protons':'phys-4-4','12di-neutrons':'phys-4-4','12dii':'phys-4-4',
}
for t in TASKS:
 if t['key'] in _TOPIC_FIX:t['topic']=_TOPIC_FIX[t['key']]
next(t for t in TASKS if t['key']=='9bii')['cells']='The current result earns 6, including the consistent-with-(i) alternative (6); partial earns (3). The two full-credit alternatives cannot be added.'
next(t for t in TASKS if t['key']=='11c')['cells']='The focusing answer earns 7; the separate partial answer earns (4) instead.'
next(t for t in TASKS if t['key']=='2iiib')['q']=[P(3,'Name (a) one mass measured and (b) one temperature measured.',piece=1,psep=' (a)'),P(3,'Name (a) one mass measured and (b) one temperature measured.',piece=2,psep=' and ')]

# Mask only neighbouring prose outside the diagram, never an exam label/line.
FIGURES['q11f-solution'] += ([(261,639,294,655)],)
FIGURES['q9c-plug'] += ([(331,629,349,676)],)
# A duplicated protractor in the two method columns denotes the same instrument.
next(t for t in TASKS if t['key']=='3iii-instrument')['rows']=[anyn(None,1,6,options=[S('protractor // metre stick',piece=1,psep='//'),S('protractor // metre stick',piece=2,psep='//')],note='Use the instrument appropriate to the measurements in your method.')]
# The public row must state the complete printed 12/6/3 scale.
next(t for t in TASKS if t['key']=='1v')['rows'][0].update(note_lead='The scheme prices the whole response 12, 6 or 3:',note='Partial answer: 3; do not add it to the two force sums.')
# Retain the original nicely typeset three equivalent formulae on reveal.
FIGURES['q3ii-formulas']=('scheme',8,(83,235.5,226,261),SEC,[],'The official three alternative refractive-index formulae: sin i/sin r; real depth/apparent depth; 1/sin C.',True)
next(t for t in TASKS if t['key']=='3ii')['fig']='q3ii-formulas'
for key in ['12di-protons','12di-neutrons']:
 next(t for t in TASKS if t['key']==key)['notes']='The original combined part allows 4 marks when both proton/neutron labels are reversed. That shared partial award applies only to the combined response, not separately to both practice cards.'

# Named diagram responses carry explicit, source-lifted label bindings.
for key,letter,answer in [('9ci','A','earth'),('9cii','B','live'),('9ai','A','ammeter'),('9aii','V','voltmeter')]:
 next(t for t in TASKS if t['key']==key)['labels']=[L(letter,S(answer,page=14),True)]
# Three separately claimable stages within either complete plotting method.
# A route menu keeps each 3-mark stage while respecting the app's recall-row
# cap; choosing a stage commits the card to that complete method.
next(t for t in TASKS if t['key']=='12ciii')['rows']=[
 R('apparatus: magnet',3,note=DSL),
 anyn(None,3,3,route='compass',options=[S('(plotting) compass'),S('procedure: use the apparatus to locate the field lines e.g. (place the compass on','the paper and) mark the dots // sprinkle filings',piece=1,psep='//'),S('detail: join the dots/ show field lines / lines go from north to south/ field lines are','// tap filings',piece=1,psep='//')],note='Compass method: 3 marks for each stage. Marks may be obtained from a diagram.'),
 anyn(None,3,3,route='filings',options=[S('// iron filings',piece=2,psep='//'),S('the paper and) mark the dots // sprinkle filings',piece=2,psep='//'),S('// tap filings',piece=2,psep='//')],note='Iron-filings method: 3 marks for each stage. Marks may be obtained from a diagram.'),
]
# “Image” in the reading passage is the optical image on the retina, not a
# missing printed illustration. Q11(f), the actual ray diagram, has both crops.
for t in TASKS:
 if t['key'] in ['11a','11b','11c','11d','11g','11h']:
  t['decision'] += ' The passage’s image on the retina is a physical optical image, not a printed figure.'
# Clear source-derived partial-credit notes, without repeating raw note fragments.
_CLEAR_NOTES={
 '4vi':'Correct substitution of two quantities: 7 marks; partial answer: 3. An answer consistent with (v) is accepted.',
 '6i':'One error: 6 marks; partial answer: 3.',
 '6iv':'One error, e.g. incorrect unit: 6 marks. Partial answer, e.g. correct unit N: 3.',
 '6viii':'One error: 6 marks; partial answer: 3.',
 '7vi':'Two correct lines: 9 marks; one correct line: 6. “Transverse waves may be polarised” earns 6. Partial answer, e.g. longitudinal waves need a medium: 3. A labelled diagram may merit full marks.',
 '8iv':'One error: 6 marks; partial answer: 3.',
 '8vi':'One error: 9 marks; at least two quantities correctly substituted: 6; partial answer: 3.',
 '9bii':'Answer consistent with (i): 6 marks. Partial answer, e.g. correct equation: 3.',
 '10i':'Two correct properties: 6 marks; one correct property: 3.',
 '12biv':'Two lines: 9 marks; one line: 6. Partial answer, e.g. charge the capacitor: 3.',
 '12bv':'A general use such as computer or car earns 2 marks.',
 '12ci':'Partial answer: 3 marks.',
 '12civ':'Partial answer: 2 marks.',
}
for t in TASKS:
 if t['key'] in _CLEAR_NOTES:
  t['rows'][0].update(note_sel=None,note_lead=None,note=_CLEAR_NOTES[t['key']])
