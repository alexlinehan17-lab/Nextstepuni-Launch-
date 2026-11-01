"""2014 Higher Physics: complete independent paper and marking-scheme review.
All 12 paper and 20 scheme pages visually read; every optional branch retained.
"""
from phys_review_lib import Q, SQ, S, G, pt, anyn, allof, T
YEAR,LEVEL=2014,'hl'
REVIEWED_AT='2026-11-01'
LETTERED={5,11,12}
SOURCES={'paper':{'path':'examiner-reports/physics/papers/2014-hl-paper.pdf','fileid':'LC021ALP000EV.pdf','sha256':'aef0a7bf87759279dd08588d84df37e4b197940884b7c92d7528ec2b79f9cfed','pages':12},'scheme':{'path':'examiner-reports/physics/schemes/2014-hl.pdf','fileid':'LC021ALP000EV.pdf','sha256':'01166938fafb2e2ac0862843995e6afdf238a62576f82fb6462d28f18b4aa7c1','pages':20}}
# SEC archive returned HTTP 403. This is the unmodified SEC document mirrored at
# https://thephysicsteacher.ie/Exam%20Material/LC%20Physics/pdf/Higher%20Level/Marking%20Schemes/2014.pdf
PAGE_ROLES={'paper':{1:'cover',**{p:'questions' for p in range(2,12)},12:'blank'},'scheme':{1:'cover',2:'note',3:'conventions',**{p:'marking' for p in range(4,18)},18:'blank',19:'blank',20:'back-cover'}}
GLYPHS={'SymbolMT':{84:'θ',79:'λ',16:'−',14:'+',111:'→',69:'β',11:'(',12:')',81:'ν'}};VERIFIED_LINES=[]
QUESTION_TOTALS={**{q:40 for q in range(1,5)},**{q:56 for q in range(5,11)},11:112,12:112}
PART_TOTALS={(11,'a'):56,(11,'b'):56,**{(12,l):28 for l in 'abcd'}}
BEST_OF={5:(8,7)};GROUP_TOTALS={};CHECKSUMS={};ROUTES={'Q5(j)':['walton','voltmeter']}
SCAN_PAGES={'paper':range(2,12)};SELECTION_SCAN=[]
ASK_SCAN_PAGES={'paper':range(2,12)};ASK_EXEMPT=[]
SEC='State Examinations Commission';CRIT='The scheme prints this marking criterion rather than a worked answer.'
P=Q

def R(text,marks,end=None,**kw):return pt(S(text,end),marks,**kw)
def C(text,marks,end=None,**kw):return pt(S(text,end),marks,kind='criterion',note=kw.pop('note',CRIT),**kw)
def EQ(page,clip,expect,marks,**kw):return G('equation',page=page,clip=clip,expect=expect,marks=marks,**kw)
TASKS=[];FIGURES={}
def U(ref,slug,label,q,rows,topic,sq,total,**kw):
 TASKS.append(T(ref+':'+slug,ref,'A' if int(ref.split('(')[0][1:])<5 else 'B',q,rows,topic,slug,sq,total,item=(slug,label),**kw))
def B(key,ref,page,start,end,sp,rows,topic,total,**kw):
 sq=kw.pop('sq',SQ(sp,start,end));TASKS.append(T(key,ref,'B',P(page,start,end),rows,topic,key,sq,total,**kw))

STEM1=P(2,'The following is part of a student’s report','collide with body B and they moved off together after the collision.”')
DATA1=P(2,'The following data was recorded:','= 0.41 m s⁻¹')
U('Q1','apparatus','Momentum experiment apparatus',P(2,'Draw a labelled diagram of the apparatus used in the experiment.'),[R('two bodies and track',3),R('labelled means of attaching the two bodies',3),R('timer / motion sensor',3)],'phys-1-2',SQ(4,'Draw a labelled diagram of the apparatus used in the experiment.'),9,stem=[STEM1,DATA1])
U('Q1','measurements','Momentum measurements and velocities',P(2,'State what measurements the student took','the velocities.'),[R('measurements: masses',3),pt(S('time for n gaps // time for body to pass through light gate // approp. time (3)',piece=1,psep=' (3)'),3,note='Use the time measurement for your chosen timer, light-gate or motion-sensor method.'),R('length of n gaps // length of (card)body // approp. distance',3,note='Use the matching distance measurement from the same method.'),R('distance ÷ time // appropriate slope = velocity',3,note='Use matching time and distance readings, or the slope of the distance–time graph.')],'phys-1-2',SQ(4,'State what measurements the student took','the velocities.'),12,stem=[STEM1,DATA1],cells='Four separate 3-mark criteria; the time criterion has its tariff welded into the extracted line.')
U('Q1','verify','Verifying conservation of momentum',P(2,'Using the recorded data, show how the experiment verifies the principle of conservation of','momentum.'),[R('0.3251 × 0.84 = 0.273 kg m s⁻¹',3),R('(0.3251 + 0.3498) × 0.41 = 0.277 kg m s⁻¹',3),R('0.273 kg m s⁻¹ ≈ 0.277 kg m s⁻¹/ or equivalent',3,note='The scheme awards 3 marks for the formula alone, and deducts one for missing or incorrect units.')],'phys-1-2',SQ(4,'Using the recorded data, show how the experiment verifies the principle of conservation of','momentum.'),9,stem=[STEM1,DATA1])
FORCES1=P(2,'When carrying out this experiment','the bodies.')
U('Q1','forces','External forces',P(2,'What are the two forces that the student needs to take account of to ensure this?'),[R('weight (gravitational force)',4),R('friction',4)],'phys-1-2',SQ(4,'What are the two forces that the student needs to take account of to ensure this?'),8,stem=[STEM1,FORCES1])
U('Q1','reduce-forces','Reducing external forces',P(2,'Describe how the student reduced the effects of these forces.'),[R('horizontal (air)track / cushion of air / (small) slope / polish runway / oil wheels',2)],'phys-1-2',SQ(4,'Describe how the student reduced the effects of these forces.'),2,stem=[STEM1,FORCES1,P(2,'What are the two forces that the student needs to take account of to ensure this?')])
STEM2=P(2,'In an experiment to measure the refractive index of a substance','of different values of the angle of incidence and recorded the following data.')
U('Q2','outlier','Inconsistent refraction reading',P(2,'One of the recorded angles of refraction is inconsistent with the others. Which one?'),[R('23 °',4)],'phys-2-3',SQ(5,'One of the recorded angles of refraction is inconsistent with the others. Which one?'),4,stem=[STEM2],fig='q2-data')
U('Q2','method','Measuring the angle of refraction',P(2,'Describe, with the aid of a labelled diagram, how the student found the angle of refraction.'),[anyn(None,4,3,options=[S(x) for x in ['rectangular block','pins / ray box / laser','correct incident, normal and refracted rays drawn','angle of refraction indicated','protractor / trigonometry']],note='Any four of the five published criteria; deduct one mark if the diagram has no label.')],'phys-2-3',SQ(5,'Describe, with the aid of a labelled diagram, how the student found the angle of refraction.'),12,stem=[STEM2],fig='q2-data')
U('Q2','graph','Refractive index from a graph',P(2,'Calculate a value for the refractive index of the substance by drawing a suitable graph based on','the recorded data.'),[C('sin i and sin r calculated',3,note='Deduct one mark for each incorrect value.'),C('axes labelled',3),C('6 points plotted',3,note='Deduct one mark for each incorrect point; all seven printed pairs, including the outlier, are retained in the question.'),C('straight line with good fit',3),C('method for finding slope',3),R('slope = n ≈ 1.44',3,note='Deduct one mark for an inappropriate scale.')],'phys-2-3',SQ(5,'Calculate a value for the refractive index of the substance by drawing a suitable graph based on','the recorded data.'),18,stem=[STEM2],fig='q2-data')
U('Q2','graph-benefits','Why use a graph?',P(2,'Give two reasons for this.'),[anyn(S('outliers can be identified / slope gives weighted mean / reference to origin','/ reference to Tan θ'),2,2,steps=[4,2],sep=' / ')],'phys-2-3',SQ(5,'Give two reasons for this.'),6,stem=[STEM2,P(2,'Using a graph to calculate a value for the refractive index is a more accurate method than','calculating the refractive index for each pair of angles and then finding the mean.')],fig='q2-data')
STEM3=P(3,'A student used a cylindrical column of air closed at one end','in an experiment to measure the speed of sound in air.')
DATA3=P(3,'The following data was recorded:','= 1.15 cm')
U('Q3','apparatus','Resonance apparatus',P(3,'Draw a labelled diagram of the apparatus used in the experiment.',before='Describe how'),[R('(vibrating) tuning fork',3),R('column of air',3),R('means of changing length of column / metre stick and callipers',3,note='Deduct one mark if the diagram has no label.')],'phys-2-5',SQ(6,'Draw a labelled diagram of the apparatus used in the experiment.'),9,stem=[STEM3,DATA3])
U('Q3','resonance','Finding the first resonance',P(3,'Describe how the first position of resonance was found.'),[R('hold (vibrating) fork over column',3),R('increase length of column (from zero)',3,note='The scheme also accepts “change length of column”.'),R('until (loudest) sound is heard (from column)',3)],'phys-2-5',SQ(6,'Describe how the first position of resonance was found.'),9,stem=[STEM3,DATA3])
U('Q3','speed','Speed of sound',P(3,'Using the recorded data, calculate the speed of sound in air.'),[R('v = 4f(l + 0.3d)',3),R('v = 4f(0.16545)',3),R('v = 338.8 m s⁻¹',3)],'phys-2-5',SQ(6,'Using the recorded data, calculate the speed of sound in air.'),9,stem=[STEM3,DATA3])
U('Q3','end-correction','Why measure the diameter?',P(3,'Why was it necessary to measure the diameter of the air column?'),[R('because wave exists partially above the top of the tube',6,note='The scheme accepts “end correction” or “error in length” alone for 3 marks.')],'phys-2-5',SQ(6,'Why was it necessary to measure the diameter of the air column?'),6,stem=[STEM3,DATA3])
U('Q3','two-resonances','Using two resonance positions',P(3,'Explain how this second student would find the speed of sound in air.'),[R('find distance between first two positions of resonance / l₂ – l₁',3),R('double this distance for wavelength / λ = 2(l₂-l₁)',2),R('multiply wavelength by frequency (for speed) / (v =) fλ',2)],'phys-2-5',SQ(6,'Explain how this second student would find the speed of sound in air.'),7,stem=[STEM3,P(3,'Another student carried out the experiment.','of the first two positions of resonance but she did not measure the diameter of the air column.')])
STEM4=P(3,'In an experiment to verify Joule’s law','shown in the table.')
GRAPH4=P(3,'Draw a suitable graph to verify Joule’s law.','Draw a suitable graph to verify Joule’s law.')
U('Q4','apparatus','Joule’s law apparatus',P(3,'Draw a labelled diagram of the apparatus used in the experiment.',after='shown in the table.'),[R('coil in water',3),R('power supply or battery with variable resistor, ammeter',3,kind='point'),R('thermometer',3),C('correct circuit diagram',3,note='Deduct one mark if the diagram has no label.')],'phys-3-3',SQ(7,'Draw a labelled diagram of the apparatus used in the experiment.'),12,stem=[STEM4],fig='q4-data')
U('Q4','graph','Joule’s law graph',GRAPH4,[C('six I² values calculated',3,note='Deduct one for each missing or incorrect value.'),C('axes labelled',3),C('6 points plotted',3,note='Deduct one for each incorrect point.'),C('straight line with good fit',3,note='Deduct one for an inappropriate scale.')],'phys-3-3',SQ(7,'Draw a suitable graph to verify Joule’s law.'),12,stem=[STEM4],fig='q4-data')
U('Q4','verify','How the graph verifies Joule’s law',P(3,'Explain how the graph verifies Joule’s law.'),[R('Explain: straight line through origin / I² proportional to rise in temperature /',6,'P proportional to I²')],'phys-3-3',SQ(7,'Explain how the graph verifies Joule’s law.'),6,stem=[STEM4,GRAPH4],fig='q4-data')
U('Q4','temperature','Temperature at 1.6 amperes',P(3,'Use your graph to estimate the highest temperature of the water when a current of 1.6 A flows','through the coil for 4 minutes.'),[R('I² = 2.56',3),R('highest temperature ≈ 25.3 °C',3,note='Deduct one for failing to add the initial 20 °C, and one for missing or incorrect units.')],'phys-3-3',SQ(7,'Use your graph to estimate the highest temperature of the water if a current of 1.6 A flows','through the coil for 4 minutes.'),6,stem=[STEM4,GRAPH4],fig='q4-data')
U('Q4','fixed-mass','Keeping the water mass fixed',P(3,'Explain why a fixed mass of water was used.'),[R('(power required for) temperature rise is proportional to mass / otherwise there would be',4,'too many variables')],'phys-3-3',SQ(7,'Explain why a fixed mass of water was used.'),4,stem=[STEM4],fig='q4-data')
B('5a','Q5(a)',4,'State Boyle’s law.',None,8,[R('p and V inversely proportional',4),R('for a fixed mass of gas at constant temperature',3)],'phys-2-1',7)
B('5b','Q5(b)',4,'The Martian moon Phobos travels in a circular orbit of','Calculate the mass of Mars.',8,[R('T² = 4π²R³/GM',4),R('6.57 × 10²³ kg',3)],'phys-1-5',7,sq=SQ(8,'The Martian moon Phobos travels in a circular orbit of radius','period of 7.6 hours. Calculate the mass of Mars.'),fig='q5-mars')
B('5c','Q5(c)',4,'On what thermometric properties are the following based:','the mercury-in-glass thermometer?',8,[anyn(None,2,3,steps=[4,3],options=[S('(i) emf; (ii) length/height/volume',piece=1,psep=';'),S('(i) emf; (ii) length/height/volume',piece=2,psep=';')],note='Both specified instruments are required; first correct property earns 4 marks, second 3.')],'phys-2-1',7,sq=SQ(8,'On what thermometric properties are (i) the thermocouple and (ii) the mercury-in-glass','thermometers based?'))
B('5d','Q5(d)',4,'The U-value of the material in a double-glazed window in a house is','is 20 °C and the outside temperature is 11 °C?',8,[R('272160 J',7,note='Partial credit: 4 marks for ΔE/Δt = AUΔθ; 3 marks for 9 °C or 3600 s. Deduct one for missing or incorrect units.')],'phys-2-1',7,sq=SQ(8,'The U-value of the material in a double-glazed window in a house is','the temperature inside the house is 20 °C and the outside temperature is 11 °C?'),fig='q5-window')
B('5e','Q5(e)',4,'List a pair of complementary colours of light.',None,8,[C('any one primary colour',2),C('any one secondary colour',2),R('correct pair: red and cyan / green and magenta / blue and yellow',3)],'phys-2-4',7,decision='One complementary pair is one response; the examples are accepted pairs, not separate cards.')
B('5f','Q5(f)',4,'What are the charge carriers in (i) semiconductors and (ii) metals?',None,8,[pt(S('(i) electrons and holes; (ii) electrons',piece=1,psep=';'),4,units=[2,2]),pt(S('(i) electrons and holes; (ii) electrons',piece=2,psep=';'),3)],'phys-3-3',7,cells='The scheme prices the two semiconductor carriers at 2 marks each and the metal carrier at 3: (2 × 2; 3).')
B('5g','Q5(g)',4,'With reference to domestic electric circuits, what do the letters in the acronyms (i) RCD and','MCB stand for?',8,[R('residual current device; miniature circuit breaker',7,units=[1]*7,note='The six words earn one mark each, with a further mark for the complete response.')],'phys-3-3',7,sq=SQ(8,'With reference to domestic electric circuits, what do the letters in the acronyms RCD and','MCB stand for?'))
B('5h','Q5(h)',4,'The work function of tungsten is 4.50 eV. Calculate the maximum kinetic energy of an','is 5.85 eV shines on the surface.',8,[R('Energy of incident photon = Work function + KE of electron',4),R('1.35 (eV) / 2.16 × 10⁻¹⁹ ( J)',3)],'phys-4-2',7)
B('5i','Q5(i)',4,'Describe Rutherford’s model of the atom.',None,8,[anyn(S('mostly empty space / dense core / positive core / electron cloud'),2,3,steps=[4,3],sep=' / ')],'phys-4-3',7)
B('5j-walton','Q5(j)',4,'ETS Walton is Ireland’s only Nobel Prize winner in','understanding of particle physics.',8,[anyn(S('first experimental verification of E = mc² / first transmutation using artificially','accelerator'),2,3,steps=[4,3],sep=' / ')],'phys-4-5',7,sq=SQ(8,'ETS Walton is Ireland’s only Nobel Prize winner in the sciences.','Cockcroft and Walton experiment was significant to the understanding of particle physics.'),route='walton',fig='q5-walton')
B('5j-voltmeter','Q5(j)',4,'Describe how a galvanometer may be converted into a voltmeter.',None,8,[R('connect a large resistor / multiplier',4),R('in series',3)],'phys-3-3',7,route='voltmeter')
# Section B: retain every separate published task and all required context.
U('Q6','vectors','Vectors and scalars',P(5,'Compare vector and scalar quantities.'),[R('vectors have direction',2),R('scalars have no direction',2)],'phys-1-1',SQ(9,'Compare vector and scalar quantities.'),4)
U('Q6','examples','Examples of vector and scalar quantities',P(5,'Give one example of each.'),[R('e.g. velocity and speed',4,units=[2,2],note='One vector and one scalar are required; each earns 2 marks.')],'phys-1-1',SQ(9,'Give one example of each.'),4,stem=[P(5,'Compare vector and scalar quantities.')])
U('Q6','experiment','Resultant of two vectors',P(5,'Describe an experiment to find the resultant of two vectors.'),[C('apparatus and arrangement e.g. 3 weights and pulleys',3),C('procedure and measurements e.g. adjust and read each force',3),C('observation and result e.g. statement',3,note='Deduct one mark if the correct direction is not shown.')],'phys-1-2',SQ(9,'Describe an experiment to find the resultant of two vectors.'),9)
GOLF=P(5,'A golfer pulls his trolley and bag along a level path.','trolley and bag together is 115 N and the force of friction is 252 N.')
U('Q6','net-force','Force on the golf trolley',P(5,'Calculate the net force acting on the trolley and bag.'),[R('Horizontal force applied by golfer = 277Cos24.53° ≈ 252 N',3),R('Vertical force applied by golfer = 277Sin24.53° ≈ 115 N',3),R('Net force ≈ 0 N',3)],'phys-1-2',SQ(9,'Calculate the net force acting on the trolley and bag.'),9,stem=[GOLF],fig='q6-trolley')
U('Q6','motion','The golfer’s motion',P(5,'What does the net force tell you about the golfer’s motion?'),[R('constant speed',3)],'phys-1-2',SQ(9,'What does the net force tell you about the golfer’s motion?'),3,stem=[GOLF,P(5,'Calculate the net force acting on the trolley and bag.')],fig='q6-trolley')
U('Q6','newton','Deriving Newton’s second-law equation',P(5,'Use Newton’s second law of motion to derive an equation relating','force, mass and acceleration.'),[R('F proportional to (mv – mu)/t',2),R('F proportional to ma',2),R('F = kma',2),R('k = 1 (by definition of the newton)',2),R('F = ma',1)],'phys-1-2',SQ(9,'Use Newton’s second law of motion to derive an equation relating force, mass and acceleration.'),9)
BALL=P(5,'A force of 5.3 kN is applied to a golf ball by a club.','are in contact for 0.54 ms.')
U('Q6','ball-speed','Speed of the golf ball',P(5,'Calculate the speed of the ball as it leaves','the club.'),[R('F = ma // I = Ft // F = (mv – mu)/t',3),C('correct substitution',3),R('v = 63.6 m s⁻¹',3)],'phys-1-2',SQ(9,'Calculate the speed of the ball as it leaves the club.'),9,stem=[BALL],fig='q6-ball')
U('Q6','height','Maximum height of the golf ball',P(5,'The ball leaves the club head at an angle of 15° to','resistance.'),[R('uy = 16.46 m s⁻¹',3),R('v² = u² +2as // ½mv² = mgh',3),R('height = 13.82 m',3)],'phys-1-1',SQ(9,'The ball leaves the club head at an angle of 15° to the horizontal.','reached by the ball. You may ignore the effect of air resistance.'),9,stem=[BALL,P(5,'(acceleration due to gravity, g = 9.8 m s⁻²)')],fig='q6-ball')
DIFF=P(5,'What is meant by the terms (i) diffraction and (ii) interference?')
U('Q7','diffraction','Diffraction',[dict(DIFF,piece=1,psep=' (i)'),dict(DIFF,piece=[2,1],psep=[' (i)',' and (ii)'])],[R('the spreading of a wave',3),R('into the space beyond a barrier/obstacle/gap',3)],'phys-2-3',SQ(10,'What is meant by the terms (i) diffraction and (ii) interference?'),6)
U('Q7','interference','Interference',[dict(DIFF,piece=1,psep=' (i)'),dict(DIFF,piece=2,psep=' (ii)')],[R('the addition/(meeting) of two or more waves (to form a new wave)',3)],'phys-2-6',SQ(10,'What is meant by the terms (i) diffraction and (ii) interference?'),3)
LASER=P(5,'A laser produces a beam of red light with a','central image.')
U('Q7','photon-energy','Energy of a laser photon',P(5,'Calculate the energy of each photon in the laser beam.'),[R('E = hf',3),R('c = fλ',3),R('E = 2.8 × 10⁻¹⁹ J',3)],'phys-4-2',SQ(10,'Calculate the energy of each photon in the laser beam.'),9,stem=[LASER],fig='q7-grating')
U('Q7','retina','Photon sensors in the eye',P(5,'Sensors in the eye can respond to single photons. Where in the eye are these sensors located?'),[R('retina',3)],'phys-2-3',SQ(10,'Sensors in the eye can respond to single photons. Where in the eye are these sensors located?'),3)
U('Q7','laser-lamp','Laser and vapour-lamp light',P(5,'State two differences between the electromagnetic radiation emitted from a laser and the','electromagnetic radiation emitted from a vapour lamp.'),[anyn(S('laser has one frequency/wavelength only / laser light is more powerful','/ laser light is coherent / laser light is collimated'),2,2,steps=[4,2],sep=' / ')],'phys-2-6',SQ(10,'State two differences between the electromagnetic radiation emitted from a laser and the','electromagnetic radiation emitted from a vapour lamp.'),6)
U('Q7','derive','Deriving the grating formula',P(5,'Derive, with the aid of a labelled diagram, the diffraction grating formula.'),[C('diffraction grating, two rays on diagram',3),C('θ and d indicated on diagram',3),C('nλ indicated on diagram',3,note='The scheme gives zero for this criterion if n = 1 is used.'),C('nλ linked to constructive interference',3),R('Sinθ = nλ/d from diagram',3)],'phys-2-6',SQ(10,'Derive, with the aid of a labelled diagram, the diffraction grating formula.'),15)
U('Q7','lines','Lines per millimetre',P(5,'Calculate the number of lines per millimetre on the grating used in the experiment.'),[R('nλ = dSinθ',3),R('d = 0.000002497 m',3),R('i.e. 400 (lines per mm)',3)],'phys-2-6',SQ(10,'Calculate the number of lines per millimetre on the grating used in the experiment.'),9,stem=[LASER],fig='q7-grating')
U('Q7','white-light','Replacing the laser with white light',P(5,'What would be observed on the screen if the laser was replaced by a ray of white light?'),[R('spectra / dispersion / colours',5)],'phys-2-6',SQ(10,'What would be observed on the screen if the laser was replaced by a source of white light?'),5,stem=[LASER],fig='q7-grating')
REACTOR=P(6,'A nuclear reactor is a device in which a sustained chain reaction takes place.','nuclear reaction doesn’t grow, but is constant.')
U('Q8','terms','Chain reaction and nuclear fission',P(6,'Explain the underlined terms.',before='A substance called'),[R('a self-sustaining reaction / a reaction where the release of one or more neutrons causes',3,'further fission'),R('fission is the splitting of a large nucleus',3),pt(S('into two (smaller) nuclei with the release of energy/neutrons (−1 if atom used)',piece=1,psep=' (−1'),3,note='Deduct one mark if “atom” is used in place of nucleus.')],'phys-4-6',SQ(11,'Explain the underlined terms.'),9,stem=[REACTOR],qfig='q8-terms')
MOD=P(6,'A substance called a moderator is mixed with the fuel in a nuclear reactor.','Control rods are used to control the rate of the reaction.')
U('Q8','moderator','An example of a moderator',P(6,'Give an example of a moderator.'),[R('graphite / (heavy) water',3)],'phys-4-6',SQ(11,'Give an example of a moderator.'),3,stem=[MOD])
MODASK=P(6,'Explain (i) why a moderator is needed in a nuclear reactor and (ii) how the control rods affect the','rate of the reaction.')
U('Q8','moderator-role','Why a moderator is needed',[dict(MODASK,piece=1,psep=' (i)'),dict(MODASK,piece=[2,1],psep=[' (i)',' and (ii)'])],[R('to slow down neutrons / so as to increase the probability of fission',6)],'phys-4-6',SQ(11,'Explain (i) why a moderator is needed in a nuclear reactor and (ii) how the control rods affect the','rate of the reaction.'),6,stem=[MOD])
U('Q8','control-rods','How control rods affect the reaction',[dict(MODASK,piece=1,psep=' (i)'),dict(MODASK,piece=2,psep=' (ii)')],[R('by absorbing neutrons',6)],'phys-4-6',SQ(11,'Explain (i) why a moderator is needed in a nuclear reactor and (ii) how the control rods affect the','rate of the reaction.'),6,stem=[MOD])
HEAT=P(6,'A heat exchanger is used in a nuclear reactor.')
U('Q8','heat-exchanger','How the heat exchanger works',P(6,'Explain how the heat exchanger operates.','Explain how the heat exchanger operates.'),[R('heat/energy from reactor',3),R('transfers to liquid/water in heat exchanger (to drive a turbine)',3)],'phys-4-6',SQ(11,'Explain how the heat exchanger operates.'),6,stem=[HEAT])
U('Q8','heat-exchanger-need','Why use a heat exchanger?',P(6,'Why is it necessary to use a heat exchanger?'),[R('the material in a reactor is radioactive / allows the core to reach a higher temperature',4)],'phys-4-6',SQ(11,'Why is it necessary to use a heat exchanger?'),4,stem=[HEAT])
U('Q8','plutonium','Production of plutonium',P(6,'Write an equation for this nuclear reaction.'),[EQ(11,(55,465,146,498),'U²³⁸₉₂ + n¹₀ → Pu²³⁹₉₄ + 2β⁰₋₁',10,units=[1]*10,note='The historical scheme awards ten one-mark components and deducts 3 for extra particles. This is the overall process; the source equation omits the two electron antineutrinos from the beta decays.')],'phys-4-6',SQ(11,'Write an equation for this nuclear reaction.'),10,stem=[P(6,'Plutonium is produced in a fission reactor','converts uranium–238 into plutonium–239 with the emission of two beta-particles.')],fig='q8-nuclear-solution',cells='Ten one-mark components belong to one complete nuclear equation.')
U('Q8','fissions','Fissions needed for one day of electricity',P(6,'Each fission of a uranium–235 nucleus produces 202 MeV of energy.','generate a constant electric power of 1 GW for a day?'),[R('Each fission = (202 ×10⁶)(1.6 × 10⁻¹⁹) / 3.23 × 10⁻¹¹ J',3),R('35% of 202 MeV = 1.13 × 10⁻¹¹ J',3),R('1 GW for a day = 8.64 × 10¹³ J',3),R('7.65 × 10²⁴ nuclei',3)],'phys-4-6',SQ(11,'Each fission of a uranium–235 nucleus produces 202 MeV of energy.','generate a constant electric power of 1 GW for a day?'),12)
TOUCH=P(6,'Most modern electronic devices contain a touchscreen.','capacitance and the electric field at that point.')
U('Q9','terms','Capacitance and electric field',P(6,'Explain the underlined terms.',after='capacitance and the electric field at that point.'),[R('capacitance is the ratio of charge (on a capacitor)',3,'// C = Q/V'),R('to the potential difference (across it)',3,'// correct notation'),R('an electric field is a region (of space)',3),R('where electrostatic forces are experienced / forces experienced by charged particles',3)],'phys-3-2',SQ(12,'Explain the underlined terms.'),12,stem=[TOUCH],qfig='q9-terms')
U('Q9','field-experiment','An electric field pattern',P(6,'Describe an experiment to demonstrate an electric field pattern.'),[R('high voltage',3),R('connected to two plates',3),R('in oil and semolina',3),R('semolina forms electric field pattern',3)],'phys-3-2',SQ(12,'Describe an experiment to demonstrate an electric field pattern.'),12)
CAP=P(6,'Two parallel metal plates are placed a distance d apart in air.','capacitor with a capacitance of 12 µF. A 6 V battery is connected across the plates.')
CAPASK=P(6,'Calculate (i) the charge on each plate and (ii) the energy stored in the capacitor.')
U('Q9','charge','Charge on each capacitor plate',[dict(CAPASK,piece=1,psep=' (i)'),dict(CAPASK,piece=[2,1],psep=[' (i)',' and (ii)'])],[R('C = Q/V',3),R('Q = 72 µC',3)],'phys-3-2',SQ(12,'Calculate (i) the charge on each plate and (ii) the energy stored in the capacitor.'),6,stem=[CAP])
U('Q9','energy','Energy stored in the capacitor',[dict(CAPASK,piece=1,psep=' (i)'),dict(CAPASK,piece=2,psep=' (ii)')],[R('E = ½CV²',3),R('E = 216 µJ',3)],'phys-3-2',SQ(12,'Calculate (i) the charge on each plate and (ii) the energy stored in the capacitor.'),6,stem=[CAP])
U('Q9','separation','Increasing plate separation',P(6,'While the battery is connected the distance d is increased by a factor of three. Calculate the new','capacitance.'),[R('4 (µF)',4)],'phys-3-2',SQ(12,'While the battery is connected the distance d is increased by a factor of three. Calculate the new','capacitance.'),4,stem=[CAP])
U('Q9','battery','Capacitors and batteries',P(6,'A capacitor and a battery are both sources of electrical energy. State two differences between','a capacitor and a battery.'),[anyn(S('capacitor discharges faster than a battery / capacitor stores (electrostatic) potential energy','/ battery stores more energy'),2,2,steps=[4,2],sep=' / ')],'phys-3-2',SQ(12,'A capacitor and a battery are both sources of electrical energy. State two differences between','a capacitor and a battery.'),6)
U('Q9','polarisation','Polarisation of light',P(6,'Touchscreens also contain two polarising filters. What is meant by polarisation of light?'),[R('vibration (of a wave)',3),R('is in one plane',3)],'phys-2-4',SQ(12,'Touchscreens also contain two polarising filters. What is meant by polarisation of light?'),6)
U('Q9','application','Another use for capacitors',P(6,'Give one application of capacitors, other than in touchscreens.'),[R('e.g. flash of a camera / tuning circuits / defibrillator',4)],'phys-3-2',SQ(12,'Give one application of capacitors, other than in touchscreens.'),4)
PRESSURE=P(7,'Blood pressure can be measured in many ways. One technique uses the','bridges.')
U('Q10','doppler','The Doppler effect',P(7,'What is the Doppler effect?'),[R('the (apparent) change in the frequency (of a wave)',3),R('due to the relative motion between the source (of the wave) and the observer',3)],'phys-2-7',SQ(13,'What is the Doppler effect?'),6,stem=[PRESSURE],fig='q10-pressure')
U('Q10','doppler-explanation','How the Doppler effect occurs',P(7,'Explain, with the aid of labelled diagrams, how the Doppler effect occurs.'),[C('source, concentric circles labelled as waves',3),C('source moving towards/away from observer, non-concentric circles',3),R('wavelength shorter moving towards the observer (or equivalent)',3),R('therefore frequency greater (or equivalent)',3)],'phys-2-7',SQ(13,'Explain, with the aid of labelled diagrams, how the Doppler effect occurs.'),12)
AMB=P(7,'An ambulance siren emits a sound of frequency 750 Hz.','towards an observer, the frequency detected by the observer is 820 Hz.')
U('Q10','ambulance','Speed of the ambulance',P(7,'What is the speed of the ambulance?'),[C('Doppler formula',3),C('correct substitution',3),C('correct rearrangement for u',3),R('29 m s⁻¹',3)],'phys-2-7',SQ(13,'What is the speed of the ambulance?'),12,stem=[AMB,P(7,'(speed of sound in air = 340 m s⁻¹)')])
U('Q10','applications','Other Doppler applications',P(7,'State two other practical applications of the Doppler effect.'),[anyn(S('e.g. police “speed guns” / measuring velocities of stars / ultrasound (scan) /','landing aircraft / weather forecasting'),2,2,sep=' / ')],'phys-2-7',SQ(13,'State two other practical applications of the Doppler effect.'),4,stem=[PRESSURE,AMB])
STRAIN=P(7,'The resistance of the conductor in a strain gauge increases when a force is applied to it.','be detected.')
U('Q10','balance','Recognising a balanced bridge',P(7,'How would an observer know that a Wheatstone bridge is balanced?'),[R('zero reading on / no deflection of / no current flowing through',2),R('galvanometer',2)],'phys-3-3',SQ(13,'How would an observer know that a Wheatstone bridge is balanced?'),4,stem=[STRAIN])
U('Q10','resistor','Unknown resistance in the bridge',P(7,'What is the resistance of the unknown resistor?'),[R('R₁ ÷ R₂ = R₃ ÷ R₄',3),R('17.36 Ω',3)],'phys-3-3',SQ(13,'What is the resistance of the unknown resistor?'),6,stem=[P(7,'The Wheatstone bridge in the diagram is balanced.')],fig='q10-bridge')
U('Q10','resistivity','Resistance in terms of diameter',P(7,'Write an expression for the resistance of a wire in terms of its resistivity, length and diameter.'),[R('R = ρl/A',3),R('R = 4ρl/πd²',3)],'phys-3-3',SQ(13,'Write an expression for the resistance of a wire in terms of its resistivity, length and diameter.'),6)
U('Q10','radius','Doubling the wire radius',P(7,'The radius of a wire is doubled. What is the effect of this on the resistance of the wire?'),[R('resistance decreases',3),R('by a factor of 4',3)],'phys-3-3',SQ(13,'The radius of a wire is doubled. What is the effect of this on the resistance of the wire?'),6)
# Both complete passage alternatives, with every illustration and the citation.
PASSAGEA=P(8,'Cyclotrons and PET Scanners','Powsner & Powsner; 1998)')
PASSAGEB=P(9,'Silicon','World”; Browne; 2013)')
for roman,slug,label,start,end,rows,topic,sq in [
 ('i','forces','Forces experienced by electrons','Electrons are leptons. List the three fundamental forces that electrons experience in','increasing order of strength.',[R('gravitational, weak (nuclear) and electromagnetic',6,units=[2,2,2]),C('in correct order',1)],'phys-4-5',None),
 ('ii','annihilation','Pair annihilation equation','Write an equation to represent the pair annihilation described in the text.',None,[R('e⁻ + e⁺',4,'// 2mₑc²'),R('→ 2hf / 2γ',3,'// = 2hf')],'phys-4-5',None),
 ('iii','frequency','Frequency of an annihilation photon','Calculate the frequency of each photon produced in this pair annihilation.',None,[R('hf = mc²',4),R('1.2356 × 10²⁰ Hz',3)],'phys-4-5',None),
 ('iv','opposite','Opposite photon directions','Why do the photons produced in pair annihilation travel in opposite directions?',None,[R('momentum',4),R('is conserved',3)],'phys-4-5',SQ(14,'Why do the photons in pair annihilation travel in opposite directions?')),
 ('v','decay','Carbon-11 decay equation','Write a nuclear equation to represent the decay of carbon–11.',None,[EQ(14,(111,384,256,415),'C¹¹₆ → B¹¹₅ + e⁰₁ ( + νₑ)',7,units=[1]*7,note='The scheme shows the electron neutrino in brackets and deducts 3 marks for extra particles.')],'phys-4-4',None),
 ('vi','decay-constant','Decay constant of carbon-11','What is the value of the decay constant of carbon–11?',None,[R('λ = ln2/T½',4),R('0.000578 s⁻¹',3)],'phys-4-4',SQ(14,'What is the decay constant of carbon–11?')),
 ('vii','hospital','Why produce carbon-11 nearby?','Explain why the carbon–11 nuclei used in the PET scanner must be produced in a','cyclotron in, or close to, the same hospital as the scanner.',[R('short half-life / too many would have decayed before they could be used',7)],'phys-4-4',None),
 ('viii','momentum','Momentum in the cyclotron','Give an expression for the momentum of a particle in the cyclotron in terms of the','path at any instant.',[R('qrB',7,note='Partial credit: 4 for equating centripetal and magnetic force, or qvB, mv²/r or mrω². Deduct one if e replaces the general charge q.')],'phys-3-5',None)
]:
 U('Q11(a)('+roman+')',slug,label,P(8,start,end),rows,topic,sq or SQ(14,start,end),7,stem=[PASSAGEA],fig='q11-pet-passage',cells='Each Q11 passage response has a published tariff of seven marks.')
for roman,slug,label,start,end,rows,topic in [
 ('i','transistor','Structure of a transistor','Draw a labelled diagram to show the basic structure of a transistor.',None,[R('npn / pnp layers',4),C('collector, base and emitter all shown correctly',3)],'phys-3-3'),
 ('ii','currents','Transistor current relationship','State the relationship between the three currents flowing in a transistor.',None,[R('Iₑ = Ib + Ic',7)],'phys-3-3'),
 ('iii','amplifier','Voltage amplifier circuit','Draw a circuit diagram for a voltage amplifier.',None,[C('transistor and resistor in series',4),C('complete circuit with input and output voltages indicated',3)],'phys-3-3'),
 ('iv','and-gate','AND gate and truth table','Draw the symbol and truth table for an AND gate.',None,[C('correct symbol',4),C('correct table',3)],'phys-3-3'),
 ('v','diodes','Photodiode and LED','Give two ways in which the operation of a photodiode differs from that of an LED.',None,[anyn(S('photodiode requires light to allow current to flow, LED produces light when a','does not need a protective resistor, LED does'),2,3,steps=[4,3],sep=' / ')],'phys-3-3'),
 ('vi','photon','Photon emission inside an LED','What event inside an LED causes the release of a photon?',None,[R('electron drops to a lower energy level (combines with a hole)',7)],'phys-3-3'),
 ('vii','fibre','Guiding light along a fibre','Explain, with the aid of a labelled diagram, how a ray of light is guided along an optical','fibre.',[R('angle of incidence greater than critical angle / total internal reflection',4),C('more than once on diagram',3)],'phys-2-3'),
 ('viii','critical-angle','Critical angle and light speed','Give an expression for the critical angle of the glass in an optical fibre in terms of the','speed of light in the glass and the speed of light in air.',[R('Sin C = cglass/cair',4),R('C = Sin⁻¹(cglass/cair)',3)],'phys-2-3')
]:
 U('Q11(b)('+roman+')',slug,label,P(9,start,end),rows,topic,SQ(15,start,end),7,stem=[PASSAGEB],fig='q11-silicon-passage')
SPRING=P(10,'The elastic constant of a spring is 12 N m⁻¹ and it has a length of','25 mm. An object of mass 20 g is attached to the spring.')
SHM=P(10,'The object is then pulled down until the spring’s length is','oscillates with simple harmonic motion.')
GRAV=P(10,'(acceleration due to gravity, g = 9.8 m s⁻²)')
rows=[]
for i,route in enumerate(['extension','restoring-force','equation'],1):
 rows+=[pt(S('extension proportional to // (restoring) force prop. to // F = (−)ks',piece=i,psep='//'),2,route=route),pt(S('(applied )force','// notation',piece=i,psep='//'),2,route=route)]
U('Q12(a)','hooke','Hooke’s law',P(10,'State Hooke’s law.'),rows,'phys-1-3',SQ(16,'State Hooke’s law.'),4,decision='Three complete alternative definitions each retain their own 2+2 tariff; never add routes together.')
U('Q12(a)','length','New length of the spring',P(10,'What is the new length of the spring?'),[R('x = F/k = (0.02 × 9.8)/12 = 0.0163 m',3),R('new length = 41.3 mm',3)],'phys-1-3',SQ(16,'What is the new length of the spring?'),6,stem=[SPRING,GRAV],fig='q12-spring')
U('Q12(a)','graph','Velocity–time graph of the spring',P(10,'Sketch a velocity-time graph of the motion of the object.'),[C('axes labelled',3),C('periodic graph',3),C('correct sinusoidal shape, beginning with v = 0',3)],'phys-1-6',SQ(16,'Sketch a velocity-time graph of the motion of the object.'),9,stem=[SPRING,SHM],fig='q12-spring')
U('Q12(a)','period','Period of the spring',P(10,'Calculate the period of oscillation of the object.'),[R('ω² = k/m (= 600)',3),R('T = 2π/ω',3),R('T = 0.256 s',3)],'phys-1-6',SQ(16,'Calculate the period of oscillation of the object.'),9,stem=[SPRING,SHM],fig='q12-spring')
U('Q12(b)','reflection','Reflection',P(10,'What is reflection?'),[R('light rebounding (off surfaces)',3)],'phys-2-3',SQ(16,'What is reflection?'),3)
U('Q12(b)','ray-diagram','Image in a convex mirror',P(10,'Draw a ray diagram to show the formation of an image in a','convex mirror.'),[C('object, correct mirror',3),C('two correct reflected rays',3),C('correct image',3)],'phys-2-3',SQ(16,'Draw a ray diagram to show the formation of an image in a convex mirror.'),9,stem=[P(10,'Spherical mirrors can be either convex or concave.')])
U('Q12(b)','image','Image in a spherical decoration',P(10,'A person looks at her image in a shiny spherical decoration when','of the decoration is 20 cm. Find the position of the image.'),[R('f = r/2 = 5 cm',3,note='This is the focal-length magnitude. Apply the convex-mirror sign consistently; the image is virtual, behind the mirror. Deduct one if f = 10 cm is used.'),R('1/u + 1/v = 1/f',3),C('substitution',3),R('v = 30/7 = 4.3 cm (behind the mirror)',3)],'phys-2-3',SQ(16,'A person looks at her image in a shiny spherical decoration when her face is 30 cm from the','image.'),12,fig='q12-decoration')
U('Q12(b)','dentist','Why dentists use concave mirrors',P(10,'Concave mirrors, rather than convex mirrors, are used by dentists to','examine teeth. Explain why.'),[R('to give a magnified image',4)],'phys-2-3',SQ(16,'Concave mirrors, rather than convex mirrors, are used by dentists to examine teeth. Explain','why.'),4)
ICE=P(11,'A drinking glass contains 500 g of water at a temperature of 24 °C. Three cubes of ice, of','is –20 °C.')
ICECON=P(11,'density of ice','= 3.3 × 10⁵ J kg⁻¹')
U('Q12(c)','latent-heat','Specific latent heat',P(11,'Define specific latent heat.'),[R('heat needed to change the state',3),R('of 1 kg of a substance (with no change in temperature)',3)],'phys-2-1',SQ(17,'Define specific latent heat.'),6)
U('Q12(c)','ice-mass','Mass of the three ice cubes',P(11,'Calculate the mass of the ice.'),[R('m = ρV',3),R('m = 43.125 g',3,note='All three cubes are required; deduct one if only one cube is used, and one for missing or incorrect units.')],'phys-2-1',SQ(17,'Calculate the mass of the ice.'),6,stem=[ICE,ICECON],fig='q12-ice')
U('Q12(c)','temperature','Minimum water temperature',P(11,'Calculate the minimum temperature of the water when the ice has melted.'),[R('any mcΔθ',3,note='Stated or implied.'),R('ml',3,note='Stated or implied.'),R('(0.043125×2100×20) + (0.043125×3.3×10⁵) + (0.043125×4200×T) = (0.5 × 4200 × (24 – T))',8,units=[2]*4,note='Each of the four energy terms carries 2 marks.'),R('T = 15.06 °C',2)],'phys-2-1',SQ(17,'Calculate the minimum temperature of the water when the ice has melted.'),16,stem=[ICE,ICECON],fig='q12-heat-solution')
U('Q12(d)','faraday','Faraday’s law',P(11,'State Faraday’s law of electromagnetic induction.'),[R('(size of an) induced emf is proportional to',3),R('the rate of change of flux (through a circuit)',3)],'phys-3-6',SQ(17,'State Faraday’s law of electromagnetic induction.'),6)
U('Q12(d)','experiment','Demonstrating Faraday’s law',P(11,'Describe an experiment to demonstrate Faraday’s law.'),[R('coil, meter, magnet',3),R('reading on meter when coil is moved relative to magnet',3),R('faster movement gives larger reading',3)],'phys-3-6',SQ(17,'Describe an experiment to demonstrate Faraday’s law.'),9)
U('Q12(d)','falling-magnet','Magnet falling through copper and glass',P(11,'A hollow copper pipe and a hollow glass pipe, with identical','copper pipe. Explain why.'),[R('(falling) magnet creates changing magnetic flux/field',3),R('emf induced',3),R('current flows in copper (only)',4),R('generating magnetic fields which oppose the motion (of the falling magnet)',3)],'phys-3-6',SQ(17,'A hollow copper pipe and a hollow glass pipe, with identical dimensions, were arranged as','Explain why.'),13,fig='q12-pipes')
SELECTION_SCAN=[
 ('paper',2,'the following','Complete momentum experiment report retained as context.'),
 ('paper',2,'or','Body A or body B refers to the two apparatus bodies, not a question choice.'),
 ('paper',2,'the following','All four momentum measurements retained.'),
 ('paper',2,'the following','All seven refraction pairs retained, including the intended outlier.'),
 ('paper',3,'the following','Both resonance measurements retained.'),
 ('paper',4,'the following','All ten Q5 parts and both j alternatives retained; no best-eight combinations.'),
 ('paper',4,'the following','Both named thermometer properties required in one stepped-tariff response.'),
 ('paper',4,'or','Both Walton and voltmeter alternatives retained with distinct topics and marking structures.'),
 ('paper',6,'both','A comparison of capacitor and battery, not a choice of task.'),
 ('paper',8,'either','Both full Q11 passage alternatives retained with their eight seven-mark tasks.'),
 ('paper',8,'or','Same Q11 outer choice; neither branch omitted.'),
 ('paper',8,'the following','Complete PET passage, both diagrams and citation retained.'),
 ('paper',8,'or','In or close to a hospital is contextual wording, not a task choice.'),
 ('paper',9,'the following','Complete Silicon passage, both illustrations and citation retained.'),
 ('paper',10,'any two','All four 28-mark Q12 alternatives retained without combinations.'),
 ('paper',10,'the following','Same four-way Q12 selection.'),
 ('paper',10,'either','Convex or concave describes mirror types; the diagram task explicitly specifies convex.'),
 ('paper',10,'or','Same description of mirror types, not a question choice.')
]
ASK_EXEMPT=[(2,'When carrying out this experiment the student ensures that there is no net external force acting on','Narrative condition retained with the two external-force tasks; not a separate ask.')]
FIGURES={
 'q2-data':('paper',2,(144,574,450,632),SEC,[],'All seven incidence and refraction pairs, including the 23-degree outlier.',False),
 'q4-data':('paper',3,(86,470,510,528),SEC,[],'All six currents and corresponding highest temperatures, with units.',False),
 'q5-mars':('paper',4,(385,177,541,277),SEC,[],'Original illustration of Mars and Phobos.',False),
 'q5-window':('paper',4,(464,304,531,396),SEC,[],'Original double-glazed window illustration.',False),
 'q5-walton':('paper',4,(355,529,541,619),SEC,[],'Original Cockcroft and Walton photograph.',False),
 'q6-trolley':('paper',5,(408,120,540,242),SEC,[],'Golfer and trolley in the original question.',False),
 'q6-ball':('paper',5,(313,273,540,426),SEC,[],'Golf ball and club in the original question.',False),
 'q7-grating':('paper',5,(317,501,541,576),SEC,[],'Complete laser, diffraction grating, screen and angle diagram.',False),
 'q8-terms':('paper',6,(54,52,542,181),SEC,[],'Full nuclear-reactor stem with chain reaction and nuclear fission underlined and the term-definition ask.',False,[(54,140,437,181),(407,116,431,135)]),
 'q8-nuclear-solution':('scheme',11,(54,462,150,499),SEC,[],'Complete official uranium-to-plutonium equation with every nuclear index.',True),
 'q9-terms':('paper',6,(54,428,542,543),SEC,[],'Touchscreen illustration, complete stem with both underlined terms and their definition ask.',False,[(382,526,410,543)]),
 'q10-pressure':('paper',7,(417,32,541,126),SEC,[],'Original blood-pressure measurement illustration.',False),
 'q10-bridge':('paper',7,(134,377,434,515),SEC,[],'Complete balanced Wheatstone bridge with all three resistances, unknown resistor, galvanometer and cell.',False),
 'q11-pet-passage':('paper',8,(80,110,544,444),SEC,[],'Full Cyclotrons and PET Scanners passage, annihilation diagram, labelled cyclotron and Powsner citation.',False),
 'q11-silicon-passage':('paper',9,(82,82,563,446),SEC,[],'Full Silicon passage, transistor and optical-fibre illustrations and Browne citation.',False),
 'q12-spring':('paper',10,(438,111,583,325),SEC,[],'Original suspended spring, mass and stand.',False),
 'q12-decoration':('paper',10,(429,473,571,648),SEC,[],'Original spherical reflective decoration.',False),
 'q12-ice':('paper',11,(452,192,527,350),SEC,[],'Original glass and three ice cubes.',False),
 'q12-heat-solution':('scheme',17,(82,248,544,364),SEC,[],'Complete official four-term energy balance, substitutions, working and final temperature.',True),
 'q12-pipes':('paper',11,(442,425,534,615),SEC,[],'Both full magnets with north/south labels above the copper and glass cylinders.',False),
}

# These tariffs sit on the line below the answer, beside a units/diagram note.
CELL_NOTES={
 'Q3:speed':'The final 3-mark tariff is printed beside the units note immediately below the numerical answer.',
 'Q4:apparatus':'The fourth 3-mark tariff is printed beside the no-label deduction immediately below the circuit criterion.',
 'Q4:temperature':'The final 3-mark tariff is printed beside the add-20 deduction below the temperature.',
 '5b':'The final 3-mark tariff is printed beside the units note below the mass.',
 'Q6:experiment':'The third 3-mark tariff is printed beside the direction deduction below the observation criterion.',
 'Q6:ball-speed':'The final 3-mark tariff is printed beside the units note below the speed.',
 'Q6:height':'The final 3-mark tariff is printed beside the units note below the height.',
 'Q7:photon-energy':'The final 3-mark tariff is printed beside the units note below the energy.',
 'Q9:charge':'The final 3-mark tariff is printed beside the units note below the charge.',
 'Q9:energy':'The final 3-mark tariff is printed beside the units note below the energy.',
 'Q10:ambulance':'The final 3-mark tariff is printed beside the units note below the speed.',
 'Q10:resistor':'The final 3-mark tariff is printed beside the units note below the resistance.',
 'Q12(a):length':'The final 3-mark tariff is printed beside the units note below the new length.',
 'Q12(a):period':'The final 3-mark tariff is printed beside the units note below the period.',
 'Q12(c):ice-mass':'The final 3-mark tariff is printed beside the units note below the mass.',
 'Q12(c):temperature':'The final 2-mark tariff is printed beside the units note below the temperature; 3+3+4×2+2=16.'
}
for task in TASKS:
 if task['key'] in CELL_NOTES:task['cells']=CELL_NOTES[task['key']]
 if task['key'] in {'Q7:diffraction','Q7:interference','Q9:charge','Q9:energy'}:
  task['sq']['paired']='The scheme reprints both roman parts in one sentence; this card lifts one independently priced part and its shared lead-in.'
ASK_EXEMPT += [
 (2,'“I ensured that no net external forces acted on body A or body B. When I released','Narrative When statement from the experiment report retained in the full Q1 stem.'),
 (7,'An ambulance siren emits a sound of frequency 750 Hz. When the ambulance is travelling','Narrative When condition retained with the ambulance-speed calculation.'),
 (7,'? Ω','Unknown-resistor label in the circuit, retained in the full bridge figure; the separate resistance ask is carded.')
]

# Preserve tabular alignment and original mathematical typesetting.
FIGURES.update({
 'q1-data':('paper',2,(82,258,420,318),SEC,[],'All four labelled momentum measurements with their values and units.',False),
 'q3-data':('paper',3,(82,123,410,156),SEC,[],'Resonance-column length and diameter with their labels and units.',False),
 'q12-heat-question':('paper',11,(82,88,544,350),SEC,[],'Full ice-and-water data, three-cube photograph, four constants and minimum-temperature ask.',False,[(82,141,544,162),(516,171,544,189)]),
 'q11-decay-question':('paper',8,(80,110,544,599),SEC,[],'Full PET passage and both diagrams, citation, and carbon-11 decay ask.',False,[(80,449,544,576)]),
 'q11-decay-solution':('scheme',14,(112,382,200,416),SEC,[],'Official carbon-11 beta-plus equation with every nuclear index and electron neutrino.',True),
 'q11-critical-question':('paper',9,(82,82,563,675),SEC,[],'Full Silicon passage with illustrations and citation, followed by the critical-angle ask.',False,[(82,447,563,639)]),
 'q11-critical-solution':('scheme',15,(111,577,283,612),SEC,[],'Official critical-angle expressions with correctly typeset speed subscripts.',True),
})
for task in TASKS:
 key=task['key']
 if key in {'Q1:apparatus','Q1:measurements','Q1:verify'}:
  task['fig']='q1-data';task['stem']=[STEM1]
 if key in {'Q3:apparatus','Q3:resonance','Q3:speed','Q3:end-correction'}:
  task['fig']='q3-data';task['stem']=[STEM3]
 if key=='Q12(c):temperature':task['qfig']='q12-heat-question'
 if key=='Q11(a)(v):decay':task.update(qfig='q11-decay-question',fig='q11-decay-solution')
 if key=='Q11(b)(viii):critical-angle':task.update(qfig='q11-critical-question',fig='q11-critical-solution')
 if key=='Q11(a)(ii):annihilation':
  task['rows']=[pt(S('e⁻ + e⁺','// 2mₑc²',piece=i,psep='//'),4,route=route) for i,route in [(1,'particles'),(2,'energy')]]
  task['rows']+=[pt(S('→ 2hf / 2γ','// = 2hf',piece=i,psep='//'),3,route=route) for i,route in [(1,'particles'),(2,'energy')]]
 if key=='Q9:terms':
  common=task['rows'][2:]
  task['rows']=[pt(S('capacitance is the ratio of charge (on a capacitor)','// C = Q/V',piece=i,psep='//'),3,route=route) for i,route in [(1,'words'),(2,'formula')]]
  task['rows']+=[pt(S('to the potential difference (across it)','// correct notation',piece=i,psep='//'),3,route=route) for i,route in [(1,'words'),(2,'formula')]]
  task['rows']+=common
