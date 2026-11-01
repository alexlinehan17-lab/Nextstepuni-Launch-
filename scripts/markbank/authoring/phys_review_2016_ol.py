"""2016 Ordinary Physics: independent review of all 12 paper and 20 scheme pages.
Twelve first-occurrence mathematical glyph crops visually checked; the raised
Times New Roman figure-dash in Q12(a) was checked against the rendered page. All printed
options retained, with each task bounded by the official marking allocation.
"""
from phys_review_lib import Q, SQ, S, G, pt, anyn as _anyn, T, L
YEAR,LEVEL=2016,'ol'
REVIEWED_AT='2026-11-01'
LETTERED={5,11,12}
SOURCES={'paper':{'path':'examiner-reports/physics/papers/2016-ol-paper.pdf','fileid':'LC021GLP000EV.pdf','sha256':'c3de271bb5e816edfaca05b0ce05fb139b4c8a7b115ea22fb8b7736872e0eb78','pages':12},'scheme':{'path':'examiner-reports/physics/schemes/2016-ol.pdf','fileid':'LC021GLP000EV.pdf','sha256':'12d4feae32ab7ea1926e6c9a67bd07f771a88e850ccda5dac5fc58d01388abf4','pages':20}}
PAGE_ROLES={'paper':{1:'cover',**{p:'questions' for p in range(2,11)},11:'blank',12:'blank'},'scheme':{1:'cover',2:'note',3:'conventions',**{p:'marking' for p in range(4,17)},**{p:'blank' for p in range(17,20)},20:'back-cover'}}
GLYPHS={'CambriaMath':{1436:'⇒'},'TimesNewRomanPS-ItalicMT':{2259:'−'},'SymbolMT':{14:'+',16:'−',32:'=',113:'°',117:'×',167:'⎛',168:'⎜',169:'⎝',183:'⎞',184:'⎟',185:'⎠'}}
VERIFIED_LINES=[]
QUESTION_TOTALS={**{q:40 for q in range(1,5)},**{q:56 for q in range(5,12)},12:112}
PART_TOTALS={**{(11,l):7 for l in 'abcdefgh'},**{(12,l):28 for l in 'abcd'}}
BEST_OF={5:(8,7)};GROUP_TOTALS={};CHECKSUMS={};ROUTES={}
SCAN_PAGES={'paper':range(2,11)};SELECTION_SCAN=[]
ASK_SCAN_PAGES={'paper':range(2,11)};ASK_EXEMPT=[]
SEC='State Examinations Commission'
CRIT='The scheme prints this marking criterion rather than a worked answer.'
DSL='The scheme’s // separates complete alternative methods; use one complete method.'
P=Q
def anyn(*args,**kw):
 lead=kw.pop("note_lead",None);row=_anyn(*args,**kw)
 if lead:row["note_lead"]=lead
 return row
def R(text,marks,end=None,**kw):return pt(S(text,end),marks,**kw)
def C(text,marks,end=None,**kw):return pt(S(text,end),marks,kind='criterion',note=kw.pop('note',CRIT),**kw)
def FR(page,clip,expect,marks,**kw):return G('fraction',page=page,clip=clip,expect=expect,marks=marks,**kw)
def EQ(page,clip,expect,marks,**kw):return G('equation',page=page,clip=clip,expect=expect,marks=marks,**kw)
def partial(full,part,sel='partial answer',end=None,extra=''):
 return dict(note_sel=S(sel,end),note_lead=f'The scheme prices this “{full} or {part}”:',note=f'({part}). '+extra)
def menu(text,claim,per,end=None,sep=',',**kw):return anyn(S(text,end),claim,per,sep=sep,**kw)
TASKS=[];FIGURES={}
def A(key,ref,page,question,sp,rows,topic,total,end=None,sq=None,**kw):
 TASKS.append(T(key,ref,'A' if int(ref.split('(')[0][1:])<5 else 'B',P(page,question,end),rows,topic,key,sq or SQ(sp,question,end),total,**kw))
def U(ref,slug,label,q,rows,topic,sq,total,**kw):
 TASKS.append(T(ref+':'+slug,ref,'B',q,rows,topic,slug,sq,total,item=(slug,label),**kw))
STEM1=P(2,'A student carried out an experiment to verify the principle of conservation of momentum.','During the experiment, the student took measurements to find mass and velocity.')
STEM2=P(2,'An experiment was set up to determine the refractive index of a material.')
STEM3=P(3,'A student carried out a laboratory experiment to find the speed of sound in air.')
STEM4=P(3,'In an experiment to verify Joule’s law, a heating coil was placed in a fixed mass of water.','The table below shows the data recorded.')
APP='Draw a labelled diagram of the arrangement of the apparatus used in this experiment.'
APP_S='Draw a labelled diagram of the arrangement of the apparatus used in this'
A('1i','Q1(i)',2,APP,4,[anyn(None,4,3,options=[S(x) for x in ['2 trolleys / 2 riders','runway / air-track','timer e.g. photo-gates (and timer) / tickertape (and timer)','means of trolleys joining','detail e.g. sloped runway, means of measuring mass / time / distance,']],note_sel=S('NOTE:','accept valid alternatives e.g. data logging methods'))],'phys-1-2',12,sq=SQ(4,APP_S,'experiment.'),stem=[STEM1])
A('1ii','Q1(ii)',2,'How was mass measured?',4,[R('used (electronic) balance / used weighing scales / weighed them',6,**partial(6,3,'partial answer e.g. mentions spiral spring'))],'phys-1-2',6,stem=[STEM1])
A('1iii-measurements','Q1(iii)',2,'What measurements were taken to calculate velocity?',4,[R('(relevant) distance specified',3),R('(relevant) time specified',3,note='A relevant time/distance detail or reference to a datalogger merits at least 3 marks.')],'phys-1-1',6,stem=[STEM1],item=('measurements','Measurements for velocity'))
A('1iii-calculation','Q1(iii)',2,'How were these measurements used to calculate velocity?',4,[FR(4,(91,340,295,379),'velocity=distance/time / s/t',3)],'phys-1-1',3,stem=[STEM1,P(2,'What measurements were taken to calculate velocity?')],item=('calculation','Calculating velocity'),fig='q1-velocity')
A('1iv','Q1(iv)',2,'How did the student determine the momentum?',4,[R('mv',6,**partial(6,3,'partial answer e.g. using the equation / m / v'))],'phys-1-2',6,stem=[STEM1])
A('1v','Q1(v)',2,'How did the student verify the principle of conservation of momentum?',4,[R('momentum before = momentum after / m₁u = (m₁ + m₂ )v /',7,'m₁u₁ + m₂u₂ = m₁v₁ + m₂v₂',**partial(7,4))],'phys-1-2',7,stem=[STEM1])
_rows=[]
for idx,route in [(1,'block'),(2,'liquid')]:
 _rows += [pt(S('glass/plastic block','// container of liquid',piece=idx,psep='//'),6,route=route,note=DSL),pt(S('ray box / laser / optical pins','// optical pins',piece=idx,psep='//'),3,route=route),pt(S('detail e.g. protractor','// metre stick / mirror',piece=idx,psep='//'),3,route=route,note_sel=S('other valid methods acceptable','accept valid alternatives'))]
TASKS.append(T('2i','Q2(i)','A',P(2,APP,nth=2),_rows,'phys-2-3','2i',SQ(5,APP_S,'experiment.'),12,stem=[STEM2]))
_rows=[anyn(None,2,6,steps=[6,3],options=[S('angle of incidence / i','// real depth',piece=1,psep='//'),S('angle of refraction / r','// apparent depth',piece=1,psep='//')],route='angles',note=DSL+' Both: 9; one: 6; partial: 3.'),anyn(None,2,6,steps=[6,3],options=[S('angle of incidence / i','// real depth',piece=2,psep='//'),S('angle of refraction / r','// apparent depth',piece=2,psep='//')],route='depth',note=DSL+' Both: 9; one: 6; partial: 3.'),R('critical angle',9,route='critical-angle',units=[6,3],note='The scheme also accepts measuring the critical angle for the full 9 marks.')]
A('2ii','Q2(ii)',2,'Indicate on your diagram the measurements that were taken.',5,_rows,'phys-2-3',9,stem=[STEM2,P(2,APP,nth=2)],cells='Three alternative methods. The standalone 6 and 6+3 are alternative scores, not additional marks.')
A('2iii','Q2(iii)',2,'What instrument was used to take these measurements?',5,[R('protractor',6,'// metre stick / ruler',**partial(6,3,'partial answer e.g. describes how to measure'))],'phys-2-3',6,stem=[STEM2])
A('2iv','Q2(iv)',2,'How was the refractive index calculated?',5,[FR(5,(90,422,433,461),'n=sin i/sin r // n=real depth/apparent depth // n=1/sin c',7,note='Use the formula for the experimental method chosen. Complete: 7; one error or the listed partial expression: 4. All three complete routes appear below.')],'phys-2-3',7,stem=[STEM2],fig='q2-formulae')
A('2v','Q2(v)',2,'Why should the experiment be repeated?',5,[R('for increased accuracy / to get average / to draw a graph',6,**partial(6,3))],'phys-2-3',6,stem=[STEM2])
A('3i','Q3(i)',3,APP,6,[R('(resonance) tube',3),R('tuning fork / signal generator',3),R('means of measuring length e.g. ruler / metre stick / means of changing length',3),R('detail e.g. fork over the mouth of tube',3,note_sel=S('NOTE:','accept valid alternatives e.g. data logging methods'))],'phys-2-5',12,sq=SQ(6,APP_S,'experiment.'),stem=[STEM3])
A('3ii','Q3(ii)',3,'How did the student find the frequency of the sound wave used?',6,[R('(read it) from the tuning fork / signal generator // used tuning forks of',6,'known frequency',**partial(6,3))],'phys-2-5',6,stem=[STEM3])
A('3iii','Q3(iii)',3,'What other measurements did the student take?',6,[anyn(None,2,6,steps=[6,3],options=[S('measure length of vibrating air'),S('measure diameter of tube','// measure length for next resonance'),S('detail e.g. equation λ = 4(l + 0.3d) // λ = 2(l₂ – l₁) // end-correction')],note='Two lines: 9; one: 6; partial e.g. using a ruler: 3. Marks may be obtained from a diagram. Keep the diameter/end-correction method or the two-resonance method internally consistent.')],'phys-2-5',9,stem=[STEM3])
A('3iv','Q3(iv)',3,'How did the student calculate the speed of sound in air?',6,[R('c = 4f (l+0.3d) / c =f λ',9,units=[3]*3,note_sel=S('one error','partial answer e.g. λ = 2(l₂ – l₁) / substituted measurements into the formula'),note='Complete: 9; one error: 6; partial: 3.')],'phys-2-5',9,stem=[STEM3])
A('3v','Q3(v)',3,'State one precaution which the student might have taken to get an accurate result.',6,[menu('use a vernier callipers to find the diameter of the tube, quiet background,',1,4,'get the second resonance position to eliminate the end-correction, etc.',open_list=True,note_sel=S('partial answer e.g. use more sensitive instruments, repeat the experiment to get a more','accurate result'),note='Partial: 2. The printed phrase “avoid no parallax” means avoid parallax error.')],'phys-2-5',4,sq=SQ(6,'State one precaution which the student might have taken to get an','accurate result.'),stem=[STEM3])
TASKS.append(T('4i','Q4(i)','A',P(3,APP,nth=2),[C('ammeter / multimeter, heating coil, calorimeter',6,units=[3,3],note='All three: 6; any one: 3. The scheme gives one combined apparatus criterion, not 3 marks for each of the three items.'),R('(variable) power supply',3),R('detail e.g. closed circuit, stop watch, insulation, variable resistance, thermometer',3,note_sel=S('NOTE:','accept valid alternatives methods'))],'phys-3-3','4i',SQ(7,APP_S,'experiment.'),12,stem=[STEM4]))
A('4ii','Q4(ii)',3,'How was the current changed during the experiment?',7,[R('adjust the (variable) power supply / (variable) resistor',4)],'phys-3-3',4,stem=[STEM4])
A('4iii','Q4(iii)',3,'Copy the table below and complete it in your answerbook.',7,[C('all correct',6,units=[1]*6,note='One mark for each of the six missing squared-current values; the 2.25 entry was already supplied. The completed table is shown below.')],'phys-3-3',6,stem=[STEM4],qfig='q4-table-question',fig='q4-table-solution')
A('4iv','Q4(iv)',3,'Using the data in the completed table, draw a graph on graph paper of Δθ',7,[C('label axes correctly (name / symbol / unit acceptable)',3),C('plot three points correctly',3),C('plot another three points correctly',3),C('straight line',3,note_sel=S('if graph paper is not used, maximum mark 3 × 3'))],'phys-3-3',12,end='against I ².',sq=SQ(7,'Using the data in the completed table, draw a graph on graph paper of','Δθ against I ².'),stem=[STEM4],qfig='q4-graph-question',fig='q4-graph-solution',notes='All seven printed readings are retained. The scheme groups plotting marks as three points plus another three.')
A('4v','Q4(v)',3,'Explain how your graph verifies Joule’s law.',7,[R('(straight) line through origin',6,'// Δθ α I ² / P α I ²',note='Complete: 6; partial proportionality statement: 3. Answer must be consistent with the graph drawn.')],'phys-3-3',6,stem=[STEM4],fig='q4-data')

A('5a','Q5(a)',4,'State the principle of Archimedes.',8,[R('(when a body is immersed in a liquid) the upthrust is equal to the weight',7,'of the displaced liquid',**partial(7,4,'partial answer e.g. upthrust'))],'phys-1-2',7)
A('5b','Q5(b)',4,'A tractor applies a force of 500 N to pull a trailer a distance',8,[R('(W = Fs = 500 ×3000 =) 1.5 × 10⁶ (J)',7,**partial(7,4))],'phys-1-4',7,end='of 3 km. Calculate the work done by the tractor.',sq=SQ(8,'A tractor applies a force of 500 N to pull a trailer a distance of 3 km.','Calculate the work done by the tractor.'),fig='q5-tractor')
TASKS.append(T('5c','Q5(c)','B',[P(4,'Choose from the list below the instrument used to measure (i) pressure, and (ii) energy.'),P(4,'opisometer','joulemeter',br=True)],[anyn(None,2,4,steps=[4,3],options=[S('(i) barometer'),S('(ii) joulemeter')],note='Both required matches: 7; one correct: 4.')],'phys-1-1','5c',SQ(8,'Choose from the list below the instrument used to measure (i) pressure,','and (ii) energy.'),7,decision='The full four-instrument pool stays with both required matches in one stepped response.'))
A('5d','Q5(d)',4,'State two uses for a concave mirror.',8,[menu('headlights, makeup, shaving mirrors, etc.',2,4,steps=[4,3],open_list=True,note_sel=S('partial answer e.g. 2 uses of a convex mirror','one correct'),note='Two uses: 7; one correct: 4.')],'phys-2-3',7)
A('5e','Q5(e)',4,'Conduction is one method of heat transfer. Name the other two methods.',8,[menu('convection, radiation',2,4,steps=[4,3],note='Both required methods: 7; one correct: 4.')],'phys-2-1',7)
A('5f','Q5(f)',4,'What is the function of a lightning conductor?',8,[R('to earth / protect building / safety / point discharge',7,**partial(7,4,'partial answer e.g. metal rod'))],'phys-3-1',7)
A('5g','Q5(g)',4,'There are 150 turns in the primary coil of a transformer and 3000 turns in the',8,[pt(S('// 240 (V)',piece=2,psep='//'),7,**partial(7,4,'partial answer e.g. correct equation'))],'phys-3-6',7,end='the primary coil.',fig='q5-transformer-solution')
A('5h','Q5(h)',4,'State one common use of the electroscope.',8,[menu('test for charge, identify charge, measure potential etc.',1,7,open_list=True,**partial(7,4))],'phys-3-1',7,fig='q5-electroscope')
A('5i','Q5(i)',4,'What is the photoelectric effect?',8,[R('emission of electrons when light (radiation) is incident',7,**partial(7,4,'partial answer e.g. emission of electrons'))],'phys-4-2',7)
A('5j','Q5(j)',4,'What are alpha-particles?',8,[R('helium nucleus / He⁺⁺ / two protons and two neutrons',7,**partial(7,4,'partial answer e.g. helium, protons and neutrons, (nuclear) radiation'))],'phys-4-4',7)

PLUTO=P(5,'The New Horizons spacecraft visited the minor planet Pluto in 2015.','for example Pluto and the New Horizons spacecraft.')
GQUESTION=P(5,'Pluto has a mass of 1.3 × 10²² kg and a radius of 1186 km. Use the equation below, which is','gravity on the surface of Pluto.')
GIVEN_MASS=P(5,'The mass of the New Horizons spacecraft is 450 kg. Calculate the weight it would have','on the surface of Pluto.')
U('Q6','force','Force and its unit',P(5,'Define the term force and state the unit of force.'),[R('force is anything that causes a body to accelerate',6,'// F=ma',note_sel=S('partial e.g. relevant force equation'),note='Definition: 6; partial force equation: 3.'),R('newton / N',3)],'phys-1-2',SQ(9,'Define the term force and state the unit of force.'),9)
U('Q6','vector','Another vector quantity',P(5,'Force is a vector quantity. Name another example of a vector quantity.'),[menu('displacement, velocity, acceleration, etc.',1,6,open_list=True,**partial(6,3))],'phys-1-1',SQ(9,'Force is a vector quantity. Name another example of a vector quantity.'),6)
U('Q6','factors','Gravitational-force factors',P(5,'State the factors which affect the size of the gravitational force between two bodies.'),[anyn(None,3,3,options=[S(x) for x in ['mass of first body','mass of second body','distance','G']],note='Any three: 9; the word “masses” can earn 6; partial answer: 3.')],'phys-1-5',SQ(9,'State the factors which affect the size of the gravitational force','between two bodies.'),9,stem=[PLUTO],fig='q6-pluto')
U('Q6','gravity','Gravity at Pluto’s surface',GQUESTION,[R('= 0.62 (m s⁻²)',12,units=[3]*4,note='Full calculation: 12; one error: 9; two errors: 6; partial: 3. Complete official substitution and working are shown below.')],'phys-1-5',SQ(9,'Pluto has a mass of 1.3 × 10²² kg and a radius of 1186 km. Use the equation below,','acceleration due to gravity on the surface of Pluto.'),12,stem=[PLUTO],qfig='q6-gravity-question',fig='q6-gravity-solution')
U('Q6','weight','Spacecraft weight',GIVEN_MASS,[R('(weight = mg = 450 × 0.62 =) 279 (N)',6,'// answer consistent with g above',**partial(6,3))],'phys-1-5',SQ(9,'The mass of the New Horizons spacecraft is 450 kg. Calculate the weight it would have','on the surface of Pluto.'),6,stem=[PLUTO,GQUESTION],fig='q6-gravity-data')
U('Q6','weight-distance','Weight farther from Pluto',P(5,'The closest the spacecraft got to Pluto was 11000 km from the surface of the planet.','surface? Explain your answer.'),[R('less',3),R('further away (from Pluto)',3)],'phys-1-5',SQ(9,'The closest the spacecraft got to Pluto was 11000 km from the surface of the','surface? Explain your answer.'),6,stem=[PLUTO,GQUESTION,GIVEN_MASS],fig='q6-gravity-data')
U('Q6','atmosphere','Pluto’s atmospheric pressure',P(5,'The Earth is surrounded by a layer of air, called its atmosphere, which exerts a pressure on the','surface.'),[menu('small g, little atmosphere, Pluto has a small mass (relative to the earth), etc.',1,3,open_list=True)],'phys-1-5',SQ(9,'The Earth is surrounded by a layer of air, called its atmosphere, which exerts a','pressure on its surface.'),3,stem=[PLUTO],fig='q6-pluto')
U('Q6','solar','Solar panels near Pluto',P(5,'Suggest a reason why solar panels','were unsuitable in this case.'),[R('Pluto is too far from the sun, they wouldn’t generate much energy',5,**partial(5,3))],'phys-2-4',SQ(9,'Suggest a reason why solar panels were','unsuitable in this case.'),5,stem=[PLUTO,P(5,'The New Horizons spacecraft used a','used on most spacecraft.')],fig='q6-orbits')

WAVES=P(6,'Sound and light travel as waves. Sound travels as a longitudinal wave whereas light travels','as a transverse wave.')
FIBRE=P(6,'Total internal reflection is the basis of operation of optical fibres.')
METER=P(6,'The picture shows a sound-level meter, which is used to measure','sound intensity level.')
U('Q7','waves','Longitudinal and transverse waves',P(6,'Explain the underlined terms.'),[R('longitudinal waves: the vibration (of the medium) is in the same direction of motion',4,'of the wave',**partial(4,2)),R('transverse waves: the vibration (of the medium) is perpendicular to the direction of motion',4,'of the wave',**partial(4,2))],'phys-2-2',SQ(10,'Explain the underlined terms.'),8,stem=[WAVES],qfig='q7-waves-question')
U('Q7','medium','Sound needs a medium',P(6,'Describe a laboratory experiment which demonstrates that sound requires a medium','to travel through.'),[menu('apparatus: bell jar, electric bell / phone, battery, vacuum pump',2,3),R('procedure: turn on pump / remove the air',3),R('observation/conclusion: no sound heard when air removed, so sound needs a medium',3)],'phys-2-5',SQ(10,'Describe a laboratory experiment which demonstrates that sound requires a medium to','travel through.'),12,stem=[WAVES])
A('7i','Q7(i)',6,'With the aid of a labelled diagram, explain how total internal reflection occurs.',10,[C('diagram with explanation of TIR',9,units=[6,3],note_sel=S('diagram / explanation','no labels, deduct 2'),note='Diagram and explanation: 9; either alone: 6; partial: 3; deduct 2 for no labels.')],'phys-2-3',9,stem=[FIBRE],fig='q7-tir-solution',cells='Complete response nine; six and three are alternative partial scores.')
A('7ii','Q7(ii)',6,'State two uses of optical fibres.',10,[menu('telecommunications, endoscope, correct specific ornament/toy, to supply light to',2,3,'inaccessible places, etc.',open_list=True,note_sel=S('partial answer e.g. cars, medicine, decorations, toys'),note='Partial: 3.')],'phys-2-3',6,stem=[FIBRE])
A('7iii','Q7(iii)',6,'The refractive index of a material in an optical fibre is 1.44. Calculate the',10,[EQ(10,(358,552,430,580),'C=43.98°',9,units=[3]*3,note='Full calculation: 9; one error: 6; correct equation: 3. Full working is shown below.')],'phys-2-3',9,end='transmitted through the fibre.',stem=[FIBRE],fig='q7-angle-solution')
A('7iv','Q7(iv)',6,'What is the unit of sound intensity level?',10,[R('Bel / B // decibel / dB',6,**partial(6,3,'partial answer e.g. defines sound intensity level'))],'phys-2-5',6,stem=[METER],fig='q7-meter')
A('7v','Q7(v)',6,'Why might a sound-level meter be used in a workplace?',10,[R('to ensure the sound level is below (permitted) limit, to protect hearing',6,**partial(6,3,'partial answer e.g. to measure the sound level, to measure loudness'))],'phys-2-5',6,stem=[METER],fig='q7-meter')

DEFS8=P(6,'Define voltage and resistance.')
CIRCUIT=P(6,'The diagram above shows a circuit with a 12 V d.c. power supply, an ammeter, and two 4 Ω','resistors connected in parallel.')
EFFECTS=P(6,'One effect of an electric current is the heating effect. Name the two other effects of an electric','current.')
U('Q8','definitions','Voltage and resistance',DEFS8,[anyn(None,2,6,steps=[6,3],options=[S('potential energy between two points on a circuit / potential difference / W/Q / electromotive force'),S('the ratio of the potential difference to the current / V/I')],note='Both definitions: 9; one correct: 6; partial answer: 3.')],'phys-3-3',SQ(11,'Define voltage and resistance.'),9)
U('Q8','instruments','Measuring voltage and resistance',P(6,'Name an instrument used to measure each of these quantities.'),[R('voltmeter / multimeter',3),R('ohmmeter / multimeter',3,note_sel=S('partial answer e.g. ammeter'),note='The printed partial score is 3.')],'phys-3-3',SQ(11,'Name an instrument used to measure each of these quantities.'),6,stem=[DEFS8])
U('Q8','source','Voltage source',P(6,'Name a source of voltage.'),[R('battery / cell /power supply /generator / thermocouple / solar panel',6,**partial(6,3,'partial answer e.g. wall socket'))],'phys-3-3',SQ(11,'Name a source of voltage.'),6)
for roman,slug,ask,ans,marks in [('i','resistance','the total resistance of the circuit','⇒ R = 2 (Ω)',9),('ii','ammeter','the current flowing through the ammeter','6 (A)',6),('iii','each-resistor','the current flowing through each resistor.','3 (A)',6)]:
 TASKS.append(T('8'+roman,'Q8('+roman+')','B',[P(6,'Calculate',after='resistors connected in parallel.'),P(6,ask)],[R(ans,marks,units=[3]*(marks//3),note='Full working is shown below. '+('One error: 6; correct equation: 3.' if marks==9 else 'Complete: 6; correct equation: 3; accept an answer consistent with the previous result.'))],'phys-3-3','8'+roman,SQ(11,ask.rstrip('.')),marks,stem=[CIRCUIT],qfig='q8-'+slug+'-question',fig='q8-'+slug+'-solution'))
U('Q8','effects','Other effects of current',EFFECTS,[R('chemical',3),R('magnetic',3)],'phys-3-3',SQ(11,'One effect of an electric current is the heating effect. Name the two other effects of an','electric current.'),6)
U('Q8','experiment','Demonstrating a current effect',P(6,'Describe an experiment to demonstrate one of these two effects.'),[C('apparatus: power source, closed circuit, solenoid, compasses / iron filings',3,note='The scheme gives one 3-mark criterion for any two of these apparatus entries.'),R('procedure: turn on the current',3),R('observation/conclusion: compass direction changes / iron filings rearrange etc.',2,note_sel=S('accept valid alternatives e.g. Hofmann voltameter','a labelled diagram may merit full marks'))],'phys-3-5',SQ(11,'Describe an experiment to demonstrate one of these two effects.'),8,stem=[EFFECTS],decision='Open choice of one demonstrated current effect. The magnetic method and explicit acceptance of a chemical Hofmann-voltameter alternative stay together; no combinations.')

WATER=P(7,'A glass bottle is filled with 0.75 kg of water at a temperature of 20 °C. The bottle is then','placed in a freezer, which freezes the water and cools it to −15 °C.')
CONSTANTS=P(7,'specific heat capacity of water','= 2200 J kg⁻¹ K⁻¹',br=True)
U('Q9','latent','Latent heat',P(7,'What is meant by latent heat?'),[R('heat required to change state (without changing its temperature)',6,**partial(6,3))],'phys-2-1',SQ(12,'What is meant by latent heat?'),6)
U('Q9','thermometer','Temperature instrument',P(7,'Name an instrument used to measure temperature.'),[R('thermometer',3)],'phys-2-1',SQ(12,'Name an instrument used to measure temperature.'),3)
for roman,ask,answer,m in [('i','reduce its temperature to 0 °C','(E = mcΔθ = 0.75 × 4200 × 20 =) 63000 (J)',9),('ii','convert the water at 0 °C to ice at 0 °C','(E = ml = 0.75 × 3.3 × 10⁵ =) 247500 (J)',9),('iii','to cool the ice at 0 °C to ice at −15 °C.','(E = mcΔθ = 0.75 × 2200 × 15 =) 24750 (J)',6)]:
 TASKS.append(T('9'+roman,'Q9('+roman+')','B',[P(7,'Calculate the energy removed from the water to'),P(7,ask)],[R(answer,m,units=[3]*(m//3),note=('Complete: 9; one error: 6; correct equation: 3.' if m==9 else 'Complete: 6; one error or correct equation: 3.'))],'phys-2-1','9'+roman,SQ(12,ask),m,stem=[WATER,CONSTANTS],fig='q9-bottle'))
U('Q9','time','Freezer time',P(7,'The power rating of the freezer is 300 W. How long will it take for the freezer to remove','9000 J of energy from the water?'),[R('(t = W ÷ P = 9000 ÷ 300 =) 30 s',5,**partial(5,3,'partial answer e.g. correct equation'))],'phys-2-1',SQ(12,'The power rating of the freezer is 300 W. How long will it take for the freezer to','remove 9000 J of energy from the water?'),5,stem=[WATER],fig='q9-bottle')
U('Q9','cracks','Why the bottle cracks',P(7,'As the water freezes, the glass bottle cracks and shatters.','Explain why this occurs.'),[R('water expands / glass contracts',6,**partial(6,3))],'phys-2-1',SQ(12,'As the water freezes, the glass bottle cracks and shatters.','Explain why this occurs.'),6,stem=[WATER],fig='q9-bottle')
U('Q9','heat-pump','Heat-pump operation',P(7,'The freezer is an example of a heat pump. Outline the operation of a heat pump.'),[anyn(None,3,6,steps=[6,3,3],options=[S('liquid evaporates'),S('liquid needs heat to evaporate','// takes heat from fridge contents'),S('releases heat (at back)'),S('gas condenses'),S('reference to latent heat')],note='Three lines: 12; two: 9; one: 6; partial: 3.')],'phys-2-1',SQ(12,'The freezer is an example of a heat pump.','Outline the operation of a heat pump.'),12)

CRT=P(7,'X-ray tubes and cathode ray tubes are practical applications of thermionic emission.','thermionic emission.',end_nth=2)
A('10i-properties','Q10(i)',7,'State two properties of the electron.',13,[menu('(negatively) charged, deflected by electric fields, deflected by magnetic fields,',2,3,'fundamental particle, small mass, outside nucleus, etc.',open_list=True)],'phys-4-1',6,end='State two properties of the electron.',sq=SQ(13,'State two properties of the electron.'),stem=[CRT],fig='q10-crt',item=('properties','Electron properties'))
A('10i-particle','Q10(i)',7,'Name another sub-atomic particle.',13,[menu('proton, neutron, neutrino, quark, etc.',1,3,open_list=True)],'phys-4-1',3,stem=[CRT],fig='q10-crt',item=('particle','Another subatomic particle'))
A('10ii','Q10(ii)',7,'Name the parts labelled A, B, and C in the diagram.',13,[R('A: cathode',3),R('B: anode',3),R('C: screen',3,note_sel=S('three correct labels, incorrect order','partial answer e.g. 2 correct labels in incorrect order'),note='All three correct names in the wrong order: 6; two names in the wrong order: 3.')],'phys-4-1',9,stem=[CRT],fig='q10-crt',labels=[L(x,S(x+': '+meaning,page=13),True) for x,meaning in [('A','cathode'),('B','anode'),('C','screen')]])
A('10iii','Q10(iii)',7,'State the function of any two of these parts.',13,[anyn(None,2,6,steps=[6,3],options=[S('cathode emits electrons / particles'),S('anode attracts / focuses /accelerates (electrons)'),S('screen lights up / shows presence (of electrons)')],note='Two correct functions: 9; one: 6; partial: 3.')],'phys-4-1',9,stem=[CRT,P(7,'Name the parts labelled A, B, and C in the diagram.')],fig='q10-crt',decision='Any two of the complete three-part pool is one stepped card, not three combinations.')
for roman,ask,ans,m in [('iv','How could the beam of electrons be deflected?','electric field / electrode / magnetic field / magnet / X-Y plates',6),('v','Why is it important to have a vacuum inside a cathode ray tube?','electrons not blocked / easier to pass through / electrons not absorbed',6),('vi','State one use of a cathode ray tube.','monitors, TV (screen), computer screen, etc.',3)]:
 A('10'+roman,'Q10('+roman+')',7,ask,13,[R(ans,m,**(partial(6,3) if m==6 else {}))],'phys-4-1',m,stem=[CRT],fig='q10-crt')
U('Q10','xray','X-ray tube sketch',P(7,'Draw a sketch of an X-ray tube.'),[menu('heater, cathode, anode, target, high voltage',3,3),R('detail e.g. correct arrangement, coolant, shielding, vacuum, window',2,note_sel=S('partial answer'),note='Partial: 3. The official labelled sketch is shown below.')],'phys-4-2',SQ(13,'Draw a sketch of an X-ray tube.'),11,stem=[P(7,'Electrons are produced by thermionic emission in an X-ray tube also.')],fig='q10-xray-solution')
U('Q10','aprons','Lead aprons',P(7,'Why are lead aprons often worn when using an X-ray tube?'),[R('protect body, safety',3)],'phys-4-2',SQ(13,'Why are lead aprons often worn when using an X-ray tube?'),3)

PASSAGE=P(8,'Experimentum crucis','Brian Clegg, Icon Books, 2015)')
for letter,ask,ans,kind in [
 ('a','What word is used to describe the bending of light by a prism?','refraction','point'),
 ('b','What does the spectrum of light consist of?','range of colours, seven colours','point'),
 ('c','Which colour of light is bent the most?','violet / blue','point'),
 ('d','Draw a diagram to show how a spectrum can be produced using a prism.','diagram to include white light source, prism and screen/spectrum','criterion'),
 ('e','What was the significance of Newton’s experiment?','light is made up of colours','point'),
 ('f','Without using a prism, how else can a spectrum be produced?','(diffraction) grating, CD, etc.','point'),
 ('g','Why is a spectrum not produced by an ordinary block of glass?','because it splits (on entering) and recombines (on leaving) //','point'),
 ('h','Name another field of physics for which Newton is famous.','mechanics / gravitation / heat','point')]:
 A('11'+letter,'Q11('+letter+')',8,ask,14,[R(ans,7,'faces not triangular / sides parallel' if letter=='g' else None,kind=kind,**(partial(7,4,'partial answer e.g wave theory' if letter=='e' else 'partial answer') if letter!='c' else {}))],'phys-2-3',7,stem=[PASSAGE],fig='q11-passage')

EGG=P(9,'Students carried out an experiment to investigate how to protect a falling egg','when protected and unprotected.')
GRAV=P(9,'(acceleration due to gravity, g = 9.8 m s⁻²)')
MAGNET=P(9,'The diagram shows a bar magnet.')
EARTH=P(10,'Earthing is a safety measure included in domestic circuits.')
SUN=P(10,'Nuclear fusion is the source of the Sun’s energy.')
U('Q12(a)','definitions','Kinetic and potential energy',P(9,'Define kinetic energy and potential energy.'),[R('energy due to motion / ½ mv²',3),R('energy due to position / energy due to state / mgh',3,note_sel=S('partial answer e.g. definition of energy'),note='Partial definition of energy: 3.')],'phys-1-4',SQ(15,'Define kinetic energy and potential energy.'),6)
A('12ai','Q12(a)(i)',9,'Calculate the potential energy of the egg before it was dropped.',15,[R('(PE = mgh = 0.052 × 9.8 × 2 =) 1.02 (J)',6,**partial(6,3,'partial answer e.g. correct equation'))],'phys-1-4',6,stem=[EGG,GRAV],fig='q12-egg')
A('12aii','Q12(a)(ii)',9,'Calculate the velocity of the egg as it hit the ground.',15,[R('(½mv² = mgh ⇒ v² = 2gh = 2 × 9.8 × 2 = 39.2 ⇒ v =) 6.26 (m s⁻¹)',6,**partial(6,3,'partial answer e.g. correct equation'))],'phys-1-4',6,stem=[EGG,GRAV],fig='q12-egg')
U('Q12(a)','protect','Protecting the egg',P(9,'Suggest how the egg could be protected from breaking when it hits the ground.'),[R('place balls of paper on the ground under it to give it a soft landing, etc.',6,**partial(6,3))],'phys-1-2',SQ(15,'Suggest how the egg could be protected from breaking when it hits the ground.'),6,stem=[EGG],fig='q12-egg')
U('Q12(a)','application','Everyday protection',P(9,'State one everyday application of the principal behind the protection of the egg.'),[menu('air bags in cars, lunar landing, on the ground for safety when workers are up on a',1,4,'height, etc.',open_list=True,**partial(4,2))],'phys-1-2',SQ(15,'State one everyday application of the principle behind the protection','of the egg.'),4,stem=[EGG,P(9,'Suggest how the egg could be protected from breaking when it hits the ground.')],fig='q12-egg')
A('12bi','Q12(b)(i)',9,'Copy the diagram and show on it the magnetic field lines around the magnet.',15,[C('diagram to show: magnet, two field lines,',6,'correct direction on lines',**partial(6,3,'partial answer e.g. incomplete diagram'))],'phys-3-4',6,sq=SQ(15,'Copy the diagram and show on it the magnetic field','lines around the magnet.'),stem=[MAGNET],qfig='q12-field-question',fig='q12-field-solution')
A('12bii','Q12(b)(ii)',9,'Describe an experiment to plot the magnetic field lines around the magnet.',15,[R('apparatus: magnet',3),R('(plotting) compass // iron filings',3),R('procedure: use the apparatus to locate the field lines e.g. (place the compass on the',3,'paper and) mark the dots and repeat // sprinkle filings'),R('detail: e.g. join the dots / show field lines / the lines go from north to south /',3,'field lines are concentrated at the magnet’s poles / tap filings',note='Marks may be obtained from a diagram. Use the compass procedure or the filings procedure consistently.')],'phys-3-4',12,stem=[MAGNET],fig='q12-magnet')
A('12biii','Q12(b)(iii)',9,'Name a metal that is attracted to a magnet.',15,[menu('nickel, iron, cobalt, steel, alnico, named magnetic alloy, etc.',1,4,open_list=True,**partial(4,2,'partial answer e.g. alloy'))],'phys-3-4',4,stem=[MAGNET],fig='q12-magnet')
A('12biv','Q12(b)(iv)',9,'State two practical uses of a magnet.',15,[menu('compass, keep fridge door closed, electric bell, electric motor,',2,3,'transformers, electromagnets, moving coil meters, loudspeakers, etc.',open_list=True)],'phys-3-4',6,stem=[MAGNET],fig='q12-magnet')
A('12ci','Q12(c)(i)',10,'State one advantage of using of a ring circuit when wiring a house.',16,[menu('fewer sockets, fewer safety devices, cables carry less current, etc.',1,6,open_list=True,**partial(6,3))],'phys-3-3',6,stem=[P(10,'A ring circuit is used in domestic wiring.')])
A('12cii-earthing','Q12(c)(ii)',10,'What is meant by earthing?',16,[R('(wire) connecting (the metal body of appliances) to the earth / ground',3)],'phys-3-3',3,end='What is meant by earthing?',stem=[EARTH],item=('earthing','Meaning of earthing'))
A('12cii-safety','Q12(c)(ii)',10,'How does earthing contribute to safety?',16,[R('in the event of a fault occurring the current will flow to earth',6,**partial(6,3))],'phys-3-3',6,stem=[EARTH],item=('safety','How earthing protects'))
A('12ciii','Q12(c)(iii)',10,'Name one other safety device used in domestic wiring.',16,[menu('fuse, circuit breaker, MCB, RCD',1,4)],'phys-3-3',4,stem=[EARTH])
A('12civ','Q12(c)(iv)',10,'In a standard domestic three-pin plug, the live wire is covered in brown plastic.',16,[R('neutral',3),R('earth',3),R('neutral is blue and the earth is green-yellow',3,note_sel=S('partial answer'),note='Partial answer: 3. Both colours share one printed 3-mark row; no invented per-colour tariff.')],'phys-3-3',9,end='Name the other two wires and state the colour associated with each of them.')
A('12di','Q12(d)(i)',10,'What is meant by nuclear fusion?',16,[R('combining of two nuclei with the release of energy / radiation',6,**partial(6,3))],'phys-4-6',6,stem=[SUN])
A('12dii','Q12(d)(ii)',10,'Name the other type of nuclear reaction used in nuclear power stations.',16,[R('fission',6,**partial(6,3))],'phys-4-6',6,stem=[SUN])
A('12diii','Q12(d)(iii)',10,'State one advantage and one disadvantage of each of these sources of nuclear',16,[R('fusion advantage: H and He atoms are plentiful, fusion produces lots of energy,',3,'little waste, etc.'),R('fusion disadvantage: very high temperatures needed, uneconomical at present,',3,'more difficult to control and sustain, etc.'),R('fission advantage: (breeder reactors) can make their own fuel,',3,'can generate radioisotopes (for medicine), etc.'),R('fission disadvantage: dangerous raw material, dangerous waste,',3,'waste storage, security problems, etc.')],'phys-4-6',12,end='energy.',stem=[SUN,P(10,'Name the other type of nuclear reaction used in nuclear power stations.')],decision='Both sources each require one advantage and one disadvantage: one four-heading response, not alternative source combinations.')
A('12div','Q12(d)(iv)',10,'Name the scientist whose equation E = mc² explained why a large amount of',16,[R('Einstein',4,**partial(4,2,'partial answer e.g. named nuclear scientist'))],'phys-4-5',4,end='energy is available from a small mass of fuel in nuclear reactions.',stem=[SUN])

# The displayed answer menus retain source examples without an empty “etc.” option.
_by={t['key']:t for t in TASKS}
for key,count in {'3v':5,'5d':3,'Q6:vector':3,'Q6:atmosphere':3,'7ii':4,'10i-properties':6,'10i-particle':4,'Q12(a):application':3,'12biii':6,'12biv':8,'12ci':3}.items():
 row=_by[key]['rows'][0];sel=row['sel'];row['options']=[dict(sel,piece=i,psep=',') for i in range(1,count+1)];row['sel']=None
SELECTION_SCAN=[
 ('paper',4,'the following','All ten Q5 options retained, without best-eight combinations.'),
 ('paper',4,'choose','All four instruments and both required matches stay in one stepped Q5(c) response.'),
 ('paper',5,'or','Greater or less is one comparison with explanation, not alternative task cards.'),
 ('paper',7,'any two','Q10(iii) retains all three parts and a single any-two response with 6+3 marks.'),
 ('paper',8,'or','Narrative qualification in the complete Newton passage, not a choice.'),
 ('paper',8,'both','Narrative description of both prism faces, retained with all passage cards.'),
 ('paper',9,'any two','All four Q12 options retained; no combinations.'),
 ('paper',9,'the following','Same Q12 instruction; all four options retained.')]
FIGURES={
 'q1-velocity':('scheme',4,(91,413,215,443),SEC,[],'Velocity equals distance divided by time, with the symbolic s/t alternative.',True),
 'q2-formulae':('scheme',5,(91,409,336,442),SEC,[],'All three refractive-index equations: sine ratio, real-to-apparent depth ratio and critical-angle expression.',True),
 'q4-data':('paper',3,(120,504,530,591),SEC,[],'All seven current and temperature-rise readings, with the supplied squared-current entry.',False),
 'q4-table-question':('paper',3,(82,295,550,593),SEC,[],'Complete Joule experiment context, seven-column table and table-completion instruction.',False,[(82,413,550,461)]),
 'q4-table-solution':('scheme',7,(120,300,371,361),SEC,[],'Completed seven-column current, squared-current and temperature-rise table.',True),
 'q4-graph-question':('paper',3,(82,295,550,643),SEC,[],'Complete Joule experiment context, all seven data readings and graph instruction.',False,[(82,413,550,485)]),
 'q4-graph-solution':('scheme',7,(96,475,451,674),SEC,[],'Official Joule-law graph with squared-current and temperature-rise axes, units and all plotted readings.',True),
 'q5-tractor':('paper',4,(420,230,555,286),SEC,[],'Tractor and trailer pictured alongside Q5(b).',False),
 'q5-transformer-solution':('scheme',8,(91,508,318,541),SEC,[],'Transformer turns-ratio substitution and 240-volt output.',True),
 'q5-electroscope':('paper',4,(330,561,402,655),SEC,[],'Electroscope shown in the question paper.',False),
 'q6-pluto':('paper',5,(209,100,423,248),SEC,[],'Pluto and New Horizons pictured in the question.',False),
 'q6-gravity-data':('paper',5,(291,402,336,439),SEC,[],'The supplied gravitational acceleration equation g equals GM divided by d squared.',False),
 'q6-gravity-question':('paper',5,(82,349,550,440),SEC,[],'Complete Pluto mass and radius, printed equation and acceleration calculation question.',False),
 'q6-gravity-solution':('scheme',9,(54,385,355,422),SEC,[],'Full Pluto gravity substitution, powers of ten, fractions and 0.62 metres per second squared.',True),
 'q6-orbits':('paper',5,(273,607,543,749),SEC,[],'Complete Solar System orbit diagram showing Pluto, the Sun and labelled planets.',False),
 'q7-waves-question':('paper',6,(82,55,550,110),SEC,[],'Wave context, both underlined terms and instruction to explain them.',False),
 'q7-tir-solution':('scheme',10,(265,315,405,367),SEC,[],'Official total-internal-reflection diagram with the glass-air interface, normal, rays and critical-angle condition.',True),
 'q7-angle-solution':('scheme',10,(91,550,327,582),SEC,[],'Complete critical-angle formula and working giving 43.98 degrees.',True),
 'q7-meter':('paper',6,(403,265,536,404),SEC,[],'The sound-level meter pictured in the question.',False),
 'q8-resistance-solution':('scheme',11,(91,348,278,383),SEC,[],'Complete parallel-resistance equation and two-ohm result.',True),
 'q8-ammeter-solution':('scheme',11,(91,448,194,487),SEC,[],'Total-current working: twelve volts divided by two ohms equals six amps.',True),
 'q8-each-resistor-solution':('scheme',11,(91,518,200,550),SEC,[],'Branch-current working: twelve volts divided by four ohms equals three amps.',True),
 'q9-bottle':('paper',7,(408,149,560,230),SEC,[],'The frozen glass bottle pictured in Question 9.',False),
 'q10-crt':('paper',7,(141,450,465,541),SEC,list('ABC'),'Complete cathode-ray tube with A, B and C, supply polarity, beam of electrons and vacuum labels.',False),
 'q10-xray-solution':('scheme',13,(100,582,412,679),SEC,[],'Official X-ray tube sketch including heater, cathode, anode, target, high voltage and cooling fins.',True),
 'q11-passage':('paper',8,(82,82,545,449),SEC,[],'Complete Experimentum crucis passage, Newton illustration and Brian Clegg 2015 attribution.',False),
 'q12-egg':('paper',9,(481,180,537,310),SEC,[],'The falling egg illustration from the experiment.',False),
 'q12-magnet':('paper',9,(240,561,400,598),SEC,[],'Complete bar magnet with north and south poles labelled.',False),
 'q12-field-question':('paper',9,(110,529,550,636),SEC,[],'Original bar magnet, north and south pole labels and instruction to add its field lines.',False),
 'q12-field-solution':('scheme',15,(67,488,191,555),SEC,[],'Official magnetic field diagram with north-to-south arrows and closed lines.',True),
}
for slug,keep in [('resistance',(676,692)),('ammeter',(697,714)),('each-resistor',(718,736))]:
 masks=[]
 for lo,hi in [(675,694),(697,715),(718,737)]:
  if not (lo<=keep[0]<=hi):masks.append((82,lo,550,hi))
 masks.append((518,718,550,738))
 FIGURES['q8-'+slug+'-question']=('paper',6,(82,480,550,738),SEC,[],'Complete parallel circuit, 12-volt supply, two 4-ohm resistors, ammeter and the '+slug+' calculation question.',False,masks)
_by['1iii-calculation']['rows'][0].update(clip=(91,413,215,443),expect='(velocity=) distance/(time) / s/t')
_by['2iv']['rows'][0].update(clip=(91,409,336,442),expect='(n=) sini/(sinr) //(n=) (real depth)/(apparent depth) // (n=) 1/(sinc)')
_by['7iii']['rows'][0].update(clip=(273,556,325,574),expect='C =43.98°')

for key,reason in {
 '3iv':'Complete formula nine; six and three are alternative partial scores.',
 '3v':'Complete precaution four; two is the alternative partial score.',
 '4i':'Apparatus trio six, power supply three, detail three. The inline any-one three is partial credit for the trio, not the whole apparatus tariff.',
 '10ii':'All three correct labels nine; six and three are alternative wrong-order partial scores.'
}.items():_by[key]['cells']=reason
_by['10i-properties']['sq']=SQ(13,'State two properties of the electron.',end='Name another sub-atomic particle.',paired='The paper asks for two electron properties and then a different particle. This card keeps the separately published 2×3 property tariff.')
_by['10i-particle']['sq']=SQ(13,'State two properties of the electron.',end='Name another sub-atomic particle.',paired='The separately published three-mark particle name is split from the six-mark property task in the same printed line.')
ASK_EXEMPT=[(8,'prism. For good measure, his experiment explained why a prism worked at all. When a beam of light','Narrative When-clause in the complete Newton passage, retained with all eight cards; not a separate exam ask.')]

# Follow-up from the rendered cards: preserve context, avoid neighbouring answer text,
# and expose each missing square in the table at its real one-mark boundary.
_by['5d']['rows'][0]['note_sel']=S('partial answer e.g. 2 uses of a convex mirror')
_by['4iii']['rows']=[pt(S(value,after='I² (A²)'),1,note=f'Squared current for I = {current} A.') for value,current in [('1','1.0'),('4','2.0'),('6.25','2.5'),('9','3.0'),('12.25','3.5'),('16','4.0')]]
for key in ['4i','4ii']:_by[key]['fig']='q4-data'
_by['4v']['stem'].append(P(3,'Using the data in the completed table, draw a graph on graph paper of Δθ','against I ².'))
for key in ['2iii','2iv']:_by[key]['stem'].append(P(2,'Indicate on your diagram the measurements that were taken.'))
_by['3iii']['stem'].append(P(3,'How did the student find the frequency of the sound wave used?'))
_by['9iii']['q'][0]=P(7,'Calculate the energy removed from the water to',piece=1,psep=' to')
_by['Q6:gravity']['rows'][0]['sel']=S('= 0.62 (m s⁻²)',piece=2,psep='= ')
_by['10ii']['labels']=[L(x,S(x+': '+meaning,page=13,piece=2,psep=': '),True) for x,meaning in [('A','cathode'),('B','anode'),('C','screen')]]
for key,rect in {
 'q1-velocity':(91,414,215,443),
 'q4-table-solution':(120,298,371,361),
 'q4-graph-solution':(91,476,458,673),
 'q5-transformer-solution':(91,512,318,541),
 'q7-angle-solution':(91,551,327,582),
 'q7-meter':(380,265,536,404),
 'q7-tir-solution':(202,313,363,373),
 'q8-ammeter-solution':(91,452,194,484),
 'q8-each-resistor-solution':(91,522,200,554),
 'q12-field-solution':(64,485,191,564),
}.items():
 f=list(FIGURES[key]);f[2]=rect;FIGURES[key]=tuple(f)
for key,masks in {
 'q12-egg':[(481,217,502,310),(518,217,537,310)],
 'q7-meter':[(380,270,403,288),(527,310,536,348)],
}.items():
 f=list(FIGURES[key]);f=f[:7]+[masks];FIGURES[key]=tuple(f)
f=list(FIGURES['q12-egg']);f[2]=(481,180,518,310);f[7]=[(481,217,502,310)];FIGURES['q12-egg']=tuple(f)
f=list(FIGURES['q12-field-solution']);f[7:]=[[(175,485,191,489)]];FIGURES['q12-field-solution']=tuple(f)
f=list(FIGURES['q4-table-solution']);f[2]=(120,299.5,371,361);FIGURES['q4-table-solution']=tuple(f)
f=list(FIGURES['q7-meter']);f[7]=[(380,270,403,288),(524,310,536,350),(380,331,391,349)];FIGURES['q7-meter']=tuple(f)
f=list(FIGURES['q12-egg']);f[2]=(481,180,524,310);FIGURES['q12-egg']=tuple(f)
FIGURES['q12-sun']=('paper',10,(226,375,398,548),SEC,[],'The Sun illustration accompanying the nuclear-fusion questions.',False)
for key in ['12di','12dii','12diii','12div']:_by[key]['fig']='q12-sun'
