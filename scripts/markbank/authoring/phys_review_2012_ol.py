"""2012 Ordinary Physics: all 12 paper and 20 scheme pages visually reviewed.
Retain every published task and source-dependent data, diagram and choice.
"""
from phys_review_lib import Q,SQ,S,G,pt,anyn,allof,T,L
YEAR,LEVEL=2012,'ol'
REVIEWED_AT='2026-11-01'
LETTERED={5,11,12}
SOURCES={'paper':{'path':'examiner-reports/physics/papers/2012-ol-paper.pdf','fileid':'LC021GLP000EV.pdf','sha256':'e7f46ff6afa24789dfaae192cd22f7aa966761a58a6b5cbb290ec9eda3f2a87e','pages':12},'scheme':{'path':'examiner-reports/physics/schemes/2012-ol.pdf','fileid':'LC021GLP000EV.pdf','sha256':'77b8f95ea2e3d91ad82af08e907bafe379d299f39503f06aa7ee6b212bfb1147','pages':20}}
PAGE_ROLES={'paper':{1:'cover',**{p:'questions' for p in range(2,11)},11:'blank',12:'blank'},'scheme':{1:'cover',2:'blank',3:'conventions',**{p:'marking' for p in range(4,17)},17:'blank',18:'blank',19:'blank',20:'back-cover'}}
# All 96 first-occurrence special-font glyphs checked against source images.
GLYPHS={'TimesNewRomanPS-BoldMT': {131: '°'}, 'TimesNewRoman,Italic': {537: 'θ', 18: '/', 70: 'c', 507: 'Δ'}, 'TimesNewRoman,Bold': {126: 'ú', 105: 'á', 177: '–', 237: '−', 86: 's', 87: 't', 88: 'u', 71: 'd', 72: 'e', 81: 'n', 3: ' ', 70: 'c', 68: 'a', 85: 'r', 76: 'i', 82: 'o', 91: 'x', 83: 'p', 80: 'm', 89: 'v', 73: 'f', 92: 'y', 54: 'S', 79: 'l', 182: '’', 90: 'w', 17: '.', 55: 'T', 75: 'h', 58: 'W', 69: 'b', 181: '‘', 74: 'g', 34: '?', 21: '2', 19: '0', 541: 'μ', 41: 'F', 38: 'C'}, 'TimesNewRomanPSMT': {131: '°', 147: '±', 238: '×', 242: '½'}, 'TimesNewRoman': {131: '°', 182: '’', 181: '‘', 237: '−', 177: '–', 70: 'c', 82: 'o', 81: 'n', 87: 't', 72: 'e', 91: 'x', 3: ' ', 76: 'i', 75: 'h', 68: 'a', 71: 'd', 86: 's', 90: 'w', 85: 'r', 80: 'm', 74: 'g', 78: 'k', 17: '.', 21: '2', 24: '5', 159: 'Ω', 15: ',', 73: 'f', 79: 'l', 25: '6', 20: '1', 18: '/', 179: '“', 89: 'v', 180: '”', 84: 'q', 88: 'u', 92: 'y', 11: '(', 83: 'p', 507: 'Δ'}, 'Symbol': {4: '×', 3: '°', 2: 'μ', 117: '×', 32: '=', 16: '−', 14: '+'}}
VERIFIED_LINES=[]
QUESTION_TOTALS={**{q:40 for q in range(1,5)},**{q:56 for q in range(5,12)},12:112}
PART_TOTALS={**{(11,l):7 for l in 'abcdefgh'},**{(12,l):28 for l in 'abcd'}}
BEST_OF={5:(8,7)};GROUP_TOTALS={};CHECKSUMS={};ROUTES={}
SCAN_PAGES={'paper':range(2,11)};SELECTION_SCAN=[]
ASK_SCAN_PAGES={'paper':range(2,11)};ASK_EXEMPT=[]
P=Q;SEC='State Examinations Commission';CRIT='The scheme prints this marking criterion rather than a worked answer.'
def R(text,marks,end=None,**kw):
 kw.setdefault('kind','point')
 return pt(S(text,end),marks,**kw)
def C(text,marks,end=None,**kw):return pt(S(text,end),marks,kind='criterion',note=kw.pop('note',CRIT),**kw)
def FR(page,clip,expect,marks,**kw):return G('fraction',page=page,clip=clip,expect=expect,marks=marks,**kw)
def EQ(page,clip,expect,marks,**kw):return G('equation',page=page,clip=clip,expect=expect,marks=marks,degrees=True,**kw)
TASKS=[];FIGURES={}
def U(ref,slug,label,q,rows,topic,sq,total,**kw):
 TASKS.append(T(ref+':'+slug,ref,'A' if int(ref.split('(')[0][1:])<5 else 'B',q,rows,topic,slug,sq,total,item=(slug,label),**kw))
def B(key,ref,page,start,end,sp,rows,topic,total,**kw):
 sq=kw.pop('sq',SQ(sp,start,end));TASKS.append(T(key,ref,'A' if int(ref.split('(')[0][1:])<5 else 'B',P(page,start,end),rows,topic,key,sq,total,**kw))
STEM1=P(2,'A student carried out an experiment to measure the acceleration of a moving trolley.','find the acceleration of the trolley.')
B('1i','Q1(i)',2,'Draw a diagram to show how the student got the trolley to accelerate.',None,4,[R('trolley and runway',9,units=[6,3],route='trolley',note='Both trolley and runway: 9; one: 6.'),pt(S('// air track and glider',piece=2,psep='//'),9,units=[6,3],route='air-track',note='Both air track and glider: 9; one: 6.'),R('detail e.g. tilt runway, apply force, ticker timer, motion sensor',3,note='A relevant detail for the selected apparatus. Other valid methods, including data logging, are accepted.')],'phys-1-1',12,stem=[STEM1])
B('1ii','Q1(ii)',2,'Describe how the student measured the final velocity of the trolley.',None,4,[pt(S('using a motion sensor // distance between (eleven) dots over time',piece=1,psep=' // '),6,units=[3,3],route='sensor',note='A motion sensor is an accepted complete method; explain how it gives the final velocity.'),R('measure the distance between (eleven) dots',3,route='ticker-tape'),R('divide by time (taken) / details how the time was measured',3,route='ticker-tape')],'phys-1-1',6,stem=[STEM1],fig='q1-velocity-solution')
B('1iii','Q1(iii)',2,'What other measurement did the student take?',None,4,[R('distance / time',6,note='Use the distance or time matching your acceleration method. A partial force/mass answer earns 3.')],'phys-1-1',6,stem=[STEM1])
B('1iv','Q1(iv)',2,'How did the student use the measurements to calculate the acceleration of the','trolley?',4,[FR(4,(93,434,374,468),'(acceleration=) (changein velocity)/(change in time) / (v₂−v₁)/(t₂−t₁) // v² = u² + 2as',10,note='Use the equation matching your measurements. One equation error: 7; partial answer: 4.')],'phys-1-1',10,sq=SQ(4,'How did the student use the measurements to calculate the','acceleration of the trolley?'),stem=[STEM1],fig='q1-acceleration-solution')
B('1v','Q1(v)',2,'Give a precaution the student took to ensure an accurate result.',None,4,[R('oil the wheels, clean the runway, ignore the initial tickertape dots,',6,'reduce the friction, etc.',note='One valid specific precaution earns 6. Repeating and averaging is the scheme’s example of a partial answer for 3.')],'phys-1-1',6,stem=[STEM1])
STEM2=P(2,'You carried out an experiment to establish the calibration curve of a thermometer.')
B('2i','Q2(i)',2,'Describe, with the aid of a diagram, the procedure you used in the experiment.',None,5,[anyn(None,4,3,options=[S('container and water'),S('thermometer (in water)','// temperature sensor'),S('heat source; hot plate / Bunsen'),S('record at least two thermometric property measurements'),S('detail e.g. stirrer, ruler, 2nd thermometer, means of recording thermometric','property, datalogger, etc.')],note='Any four of the five published criteria, 3 each. No diagram: maximum 9. A labelled diagram may earn full marks; the detail is one criterion, not one mark for every example.')],'phys-2-1',12,stem=[STEM2])
rows2=[]
for route,line in [('mercury','length of column of mercury – measure length with ruler //'),('thermistor','resistance (of thermistor) – measure resistance with ohmmeter etc.')]:
 rows2 += [pt(S(line,piece=1,psep=' – '),7,route=route),pt(S(line,piece=[2,1] if route=='mercury' else 2,psep=[' – ',' //'] if route=='mercury' else ' – '),3,route=route,note='Name a thermometric property and its matching measurement method. Partial answer: 3.')]
B('2ii','Q2(ii)',2,'Name the thermometric property of the thermometer you calibrated and','describe how the value of this property was measured.',5,rows2,'phys-2-1',10,sq=SQ(5,'Name the thermometric property of the thermometer you calibrated and','describe how the value of this property was measured?'),stem=[STEM2])
B('2iii','Q2(iii)',2,'Using the data in the table, draw a graph on graph paper to establish the','calibration curve. Put temperature on the horizontal axis.',5,[C('temp on the horizontal axis',3),C('plot three points correctly',3),C('plot another three points correctly',3),C('plot (smooth) curve',3,note='Use all six pairs. Without graph paper: maximum 9.')],'phys-2-1',12,sq=SQ(5,'Using the data in the table, draw a graph on graph paper to establish the','calibration curve. Put temperature on the horizontal axis'),stem=[STEM2],qfig='q2-graph-question',fig='q2-graph-solution')
B('2iv','Q2(iv)',2,'Use your calibration curve to determine the temperature when the value of the','thermometric property is 60.',5,[R('70 ± 3 °C or value consistent with graph',6,note='Read the temperature at thermometric property 60 on your own curve. Evidence of graph use: 3.')],'phys-2-1',6,sq=SQ(5,'Use your graph to estimate the temperature when the value of the','thermometric property is 60.'),stem=[STEM2],qfig='q2-reading-question',fig='q2-graph-solution')
STEM3=P(3,'A student carried out an experiment to verify Snell’s law of refraction. The student measured','The data recorded by the student are shown in the table.')
B('3i','Q3(i)',3,'Draw a labelled diagram of the apparatus used in the experiment.',None,6,[R('glass block',3),R('laser / ray box / pins',3),R('protractor / ruler / sheet of paper',3,note='No labels: deduct 2. Other valid apparatus is accepted.')],'phys-2-3',9,stem=[STEM3],fig='q3-data')
B('3ii','Q3(ii)',3,'Describe how the student found the path of the ray of light passing through','the glass block.',6,[R('refracted ray described or drawn',6),R('detail e.g. refers to the incident ray / emerging ray',3,note='A diagram may earn full marks; partial answer: 3.')],'phys-2-3',9,stem=[STEM3],fig='q3-data')
B('3iii','Q3(iii)',3,'Indicate on the diagram the angles i and r.',None,6,[C('correct angle i',3,note='Mark the angle between the incident ray and normal.'),C('correct angle r',3,note='Mark the angle between the refracted ray and normal. Mismatched angle labels: 3 total. The angles may appear on your apparatus diagram.')],'phys-2-3',6,stem=[STEM3],qfig='q3-angle-question',fig='q3-angle-solution')
B('3iv','Q3(iv)',3,'Copy this table into your answerbook and complete it.',None,6,[C('> 9 calculations correct',9,note='Complete all twelve empty cells in the four-row table. The source prints “> 9 calculations correct” for 9 marks; any six correct earn 6, any three earn 3. The original completed table is shown; retain the whole task, without inventing per-cell marks.')],'phys-2-3',9,stem=[STEM3],qfig='q3-table-question',fig='q3-table-solution')
B('3v','Q3(v)',3,'How does the data in the completed table verify Snell’s law of refraction?',None,6,[FR(6,(92,701,261,735),'(sin i)/(sin r) is constant /1.536',7,note='The ratio is approximately constant for the four observations. Partial answer: 4.')],'phys-2-3',7,sq=SQ(6,'How does the data in the completed table verify Snell’s law of refraction'),stem=[STEM3],fig='q3-data')
STEM4=P(3,'In an experiment to investigate the variation of current I with potential difference V','for a copper sulfate solution, the following apparatus was used.')
for roman,start,rows,total,sq in [
 ('i','Name the instrument X.',[R('milliammeter / ammeter /galvanometer / multimeter',6,note='“Meter” alone earns 3.')],6,None),
 ('ii','Name the apparatus Y and give its function in the experiment.',[R('rheostat / (variable) resistor / potential divider / potentiometer',3),R('change in one of: resistance, voltage, potential, current, power, /',3,'answer consistent with named apparatus',note='The function must match the named apparatus; a resistor limiting current is accepted.')],6,SQ(7,'Name the apparatus Y and give its function in the experiment')),
 ('iii','How was the potential difference measured in the experiment?',[R('using a voltmeter/ with Z',6,note='Partial answer such as using a multimeter or V = IR: 3.')],6,None),
]:
 kw={'sq':sq} if sq else {}
 B('4'+roman,'Q4('+roman+')',3,start,None,7,rows,'phys-3-3',total,stem=[STEM4],fig='q4-apparatus',**kw)
U('Q4','graph','Current–voltage graph',P(3,'Using the data in the table, draw a graph on graph paper to show the variation of','current with potential difference.'),[C('label one axis correctly- name/symbol/unit acceptable',3),C('plot three points correctly',3),C('plot another three points correctly',3),C('draw line of best fit',3,note='Plot all seven pairs; the original scheme graph shown omits the last point (2.4 A, 6 V). No graph paper: maximum 9. Either axis orientation is accepted if used consistently.')],'phys-3-3',SQ(7,'The following table shows the values recorded for the current I and the','potential difference.'),12,stem=[STEM4],qfig='q4-graph-question',fig='q4-graph-solution')
U('Q4','resistance','Slope and resistance',P(3,'Calculate the slope of your graph.','Use this value to determine the resistance of the copper sulfate solution.'),[C('2.5 // answer consistent with graph e.g. 0.4',7,note='V plotted against I gives slope 2.5 V/A; I plotted against V gives 0.4 A/V.'),R('= 2.5 Ω',3,note='Resistance is 2.5 Ω: use the slope for V against I, or its reciprocal for I against V. Partial method/evidence of graph use: 3.')],'phys-3-3',SQ(7,'Calculate the slope of your graph.','Use this value to determine the resistance of the copper sulfate solution.'),10,stem=[STEM4],qfig='q4-resistance-question',fig='q4-resistance-solution')
for l,start,end,rows,topic in [
 ('a','A tow-truck pulls a car with a net horizontal force of 500 N.','Calculate the work done in towing the car a distance of 2 km to a garage.',[R('(500)(2000) = 10⁶ J',7,note='W = Fs, with 2 km converted to 2000 m. Partial method: 4.')],'phys-1-4'),
 ('b','Give one factor on which the potential energy of a body depends.',None,[R('m/g /h , etc.',7,note='Any one of mass, gravitational field strength or height for gravitational potential energy. Partial answer: 4.')],'phys-1-4'),
 ('c','Which one of the following instruments is used to measure atmospheric pressure?','joulemeter',[R('barometer',7)],'phys-1-5'),
 ('d','The Tacoma Narrows Bridge collapsed, soon after','construction, due to resonance. What is resonance?',[R('(the tendency of a body to oscillate at a) greater amplitude at some',7,'(forced) frequencies // refers to energy transfer at certain frequencies',note='Large response when driven near a natural frequency. The Tacoma sentence is the historical paper’s framing; the definition is the marked task. Partial reference to natural frequency or a valid example: 4.')],'phys-2-6'),
 ('e','A building has a low U-value. What is the advantage of this?',None,[R('low energy loss, etc.',7,note='Partial answer: 4.')],'phys-2-1'),
 ('f','Why is a lightning conductor made of copper?',None,[R('good conductor, doesn’t corrode, cheaper than silver, etc.',7,note='Any valid advantage; partial answer: 4.')],'phys-3-3'),
 ('g','Why does a magnet that is free to rotate point north?',None,[R('earth’s magnetic field',7,note='Partial answer: 4.')],'phys-3-4'),
 ('h','A transformer is used to change the voltage of an electrical supply.','What is the principle of operation of a transformer?',[pt(S('change in magnetic flux induces an emf // correct reference to coils // e.m. induction 7',piece=1,psep=' 7'),7,note='Electromagnetic induction. Partial reference to Faraday, magnetic field or emf: 4.')],'phys-3-6'),
 ('i','The photo shows an LDR. Draw the electrical circuit symbol for an LDR.',None,[pt(S('The photo shows an LDR. Draw the electrical circuit symbol for an LDR. 7 or 4',piece=1,psep=' 7 or 4',after='Question 5'),7,kind='criterion',note='Draw the LDR symbol shown in the original scheme: resistor inside a circle with two arrows pointing towards it. Partial answer: 4.')],'phys-3-3'),
 ('j','What is the main source of energy in the sun?',None,[R('hydrogen /nuclear / fusion',7,note='Hydrogen nuclei fuse, releasing energy. The historical scheme gives 4 for fission; fission is not the Sun’s main energy source.')],'phys-4-6'),
]:
 sq=SQ(8,start,end)
 if l=='b':sq=SQ(8,start.rstrip('.'))
 if l=='c':sq=SQ(8,'Which of the following instruments can be used to measure','atmospheric pressure?')
 if l=='d':sq=SQ(8,'The Tacoma Narrows Bridge collapsed, soon after construction,','due to resonance. What is resonance?')
 B('5'+l,'Q5('+l+')',4,start,end,8,rows,topic,7,sq=sq,fig={'a':'q5-tow','d':'q5-bridge','i':'q5-ldr-solution'}.get(l),qfig='q5-ldr-question' if l=='i' else None)
U('Q6','gravity','Acceleration due to gravity',P(5,'What is meant by the term ‘acceleration due to gravity’?'),[R('(acceleration) caused by the (gravitational pull of the) earth /moon /planet',6,note='Partial reference to Earth, falling or 9.8: 3.')],'phys-1-5',SQ(9,'What is meant by the term ‘acceleration due to gravity’?'),6)
SPACE=P(5,'A spacecraft of mass 800 kg is on the surface of the moon,','where the acceleration due to gravity is 1.6 m s⁻².')
U('Q6','weights','Earth and Moon weights',P(5,'Compare the weight of the spacecraft on the surface of the','gravity is 9.8 m s⁻².'),[anyn(None,2,3,steps=[6,3],options=[S('weight on moon = mgₘ= (800)(1.6) = 1280 N'),S('weight on earth = mgₑ = (800)(9.8) = 7840 N')],note='Both weights: 9; one: 6. A comparison of about 6.1 times heavier on Earth earns 6; a correct mg method earns 3.')],'phys-1-5',SQ(9,'Compare the weight of the spacecraft on the surface of the moon with its weight','on earth where the acceleration due to gravity is 9.8 m s⁻²'),9,stem=[SPACE],fig='q6-module')
MODULE=P(5,'The module of the spacecraft has a mass of 600 kg, when it is launched vertically','from the surface of the moon with its engine exerting an upward force of 2000 N.')
for roman,start,end,rows,topic,total in [
 ('i','Draw a diagram showing the forces acting on the module at lift-off.',None,[R('(weight)',3,note='Draw weight vertically downwards: 600 × 1.6 = 960 N.'),R('(Thrust)',3,note='Draw engine thrust upwards: 2000 N. The original scheme shows both arrows.')],'phys-1-2',6),
 ('ii','What is the resultant force on the module?',None,[R('F – mgₘ = 2000 – (600)(1.6) = 1040 N',6,note='Resultant force is upwards. Partial answer: 3.')],'phys-1-2',6),
 ('iii','Calculate the acceleration of the module during lift-off.',None,[R('(F=ma ) 1040 = (600)(a) a = 1.73 m s⁻²',6,note='Use the resultant force. Accept follow-through from part (ii). F = ma alone: 3. Unrounded acceleration is 1.7333… m/s².')],'phys-1-1',6),
 ('iv','Calculate the velocity of the module, 20 seconds after lift-off.',None,[R('(v = u + at ) i.e. v = 0 + (1.73)(20) = 34.6 m s⁻¹',6,note='The module starts from rest. Using unrounded acceleration gives 34.67 m/s. Accept follow-through; v = u + at alone: 3.')],'phys-1-1',6),
 ('v','Would the engine of the module be able to lift it off the earth’s surface?','Justify your answer in terms of the forces acting on the module.',[R('no',3),R('force required to overcome the earth’s gravity (5880 N) is greater than the',6,'upward force (2000) // 5880 > 2000',note='Earth weight = 600 × 9.8 = 5880 N exceeds the 2000 N thrust. Partial explanation: 3.')],'phys-1-2',9),
 ('vi','Why is the acceleration due to gravity on the moon less than the acceleration','due to gravity on earth?',[R('because the mass of the moon is less than the mass of the earth',5,note='The scheme accepts the smaller mass. More fully, surface gravity depends on M/R², so radius also matters. Partial mass/distance reference: 3.')],'phys-1-5',5),
 ('vii','Suggest a reason why the module of the spacecraft when launched from the moon','does not need a streamlined shape like those that are launched from earth.',[R('no atmosphere // no drag // no friction',3,note='Negligible atmospheric drag on the Moon.')],'phys-1-2',3),
]:
 sq=SQ(9,start,end)
 if roman=='vi':sq=SQ(9,'Why is the acceleration due to gravity on the moon less than the','acceleration due to gravity on the earth?')
 if roman=='vii':sq=SQ(9,'Suggest a reason why the module of the spacecraft when launched from','from earth.')
 B('6'+roman,'Q6('+roman+')',5,start,end,9,rows,topic,total,sq=sq,stem=[SPACE,MODULE,P(5,'Compare the weight of the spacecraft on the surface of the','gravity is 9.8 m s⁻².')],fig='q6-forces-solution' if roman=='i' else 'q6-module',qfig='q6-forces-question' if roman=='i' else None)
WAVES=P(5,'Under certain conditions, light can undergo diffraction and interference.')
for slug,answer,end in [('diffraction','diffraction is the spreading out of waves around a barrier / the edges of an opening','// correct diagram'),('interference','interference occurs when two waves meet and add // correct diagram',None)]:
 U('Q7(i)',slug,slug.capitalize(),P(5,'Explain the underlined terms.'),[R(answer,6,end,note='Answer the named definition. A correct diagram is accepted; partial answer: 3. Both definitions are separate 6-mark allocations in the scheme.')],'phys-2-6',SQ(10,'Explain the underlined terms.'),6,stem=[WAVES],qfig='q7-terms-question')
B('7ii','Q7(ii)',5,'Describe an experiment to demonstrate the wave nature of light.',None,10,[R('apparatus: (light) source, (diffraction) grating / slits, screen',6,units=[3,3],note='All three apparatus pieces: 6; one piece: 3. These are fixed components of one apparatus criterion, not a choose-two pool.'),R('procedure: shine the (narrow beam of) light through the grating',3),R('observation/conclusion; pattern on screen',3,note='A diagram may earn marks. Valid alternative experiments accepted; an incorrect experiment is capped at 6.')],'phys-2-6',12,sq=SQ(10,'Describe an experiment to demonstrate the wave nature of light'),stem=[WAVES])
POLAROID=P(5,'The photograph shows Polaroid sunglasses','which reduce glare caused by sunlight.')
for roman,start,end,rows,total in [
 ('iii','Explain the term ‘polarisation’.',None,[R('polarisation is the restriction of (vibrating electromagnetic) waves to a single plane',6,note='A diagram is accepted. Partial answer: 3.')],6),
 ('iv','Describe an experiment to demonstrate the polarisation of light.',None,[R('apparatus: (two pieces of a) polaroid sheet',3),R('procedure: look at the light through the two pieces of polaroid',3),R('cross/rotate one of the polaroid pieces',3),R('observation/conclusion; the crossed pieces stops the light',3,note='A diagram may earn full marks; valid alternatives accepted.')],12),
 ('v','What type of wave motion does light have as indicated by the experiment in','part (iv)?',[R('transverse',9,note='Polarisation shows transverse wave motion. “Electromagnetic” earns 6; a partial reference to longitudinal earns 3 in the historical scheme.')],9),
 ('vi','Why are Polaroid sunglasses more effective than non-Polaroid sunglasses at','reducing glare?',[R('polaroid sunglasses remove most of the polarised reflected light (which',5,'causes the glare) while ordinary sunglasses doesn’t // reflected light is polarised',note='Partial reduction-of-intensity answer: 3.')],5),
]:
 sq=SQ(10,start.rstrip('.'),end)
 if roman=='iii':sq=SQ(10,'Explain the term polarisation')
 if roman=='v':sq=SQ(10,'What type of wave motion does light have as indicated by the experiment','in part (iv)?')
 if roman=='vi':sq=SQ(10,'Why are Polaroid sunglasses more effective than non-Polaroid','sunglasses at reducing glare?')
 B('7'+roman,'Q7('+roman+')',5,start,end,10,rows,'phys-2-3',total,sq=sq,stem=[POLAROID]+([P(5,'Describe an experiment to demonstrate the polarisation of light.')] if roman=='v' else []),fig='q7-glasses')
PLUG=P(6,'A plug is used to connect an electrical appliance in the home to the 230 volt mains supply.','The electrical energy supplied to the home is measured in kW h (kilowatt-hour).')
VACUUM=P(6,'A vacuum cleaner has a power rating of 900 W.')
for roman,start,end,rows,total in [
 ('i','What is the colour of the wire that should be connected to the fuse in a plug?',None,[R('brown',6,note='Brown is the live wire. The historical scheme’s other-colour partial answers are not correct live-wire identifications.')],6),
 ('ii','Why is there a fuse in a plug?',None,[R('protection // to prevent current overload // prevent fire, etc.',6,note='Partial answer: 3.')],6),
 ('iii','Explain how a fuse works.',None,[anyn(None,2,3,steps=[6,3],options=[S('when the current exceeds a certain value'),S('the wire breaks / fuse burns out / circuit breaks')],note='Both parts of the explanation: 9; one: 6; partial answer: 3.')],9),
 ('iv','A vacuum cleaner has a power rating of 900 W.','of the vacuum cleaner?',[R('5 A',9,units=[3,3,3],note='The full answer is a 5 A fuse. I = P/V = 900/230 ≈ 3.9 A, so choose the next available rating above the normal current. Correct current or a fuse consistent with the calculated current earns 6; 13 A earns 3 in the historical scheme.')],9),
 ('v','Why is a fuse of a lower rating unsuitable?',None,[R('it might melt/break /blow / current will be too big',6,note='The normal operating current would exceed the fuse rating. Partial “appliance won’t work” answer: 3.')],6),
 ('vi','Name a device found in modern domestic circuits that','has the same function as a fuse.',[R('(miniature) circuit breakers / MCBs // trip switches //',6,'residual current devices / RCDs // trip switch / RCB / ELCB, etc.',note='An MCB is the overcurrent-protection counterpart. The historical scheme also accepts RCDs; an RCD detects an imbalance between live and neutral currents, so its protection differs from a fuse. See IET: https://electrical.theiet.org/bs-7671-18th-edition-wiring-regulations/faqs/consumer-units-and-protective-devices-faqs')],6),
 ('vii','the number of units of electricity used;',None,[R('P× t = (0.9)( 1.5) = 1.35',8,note='1.35 kWh = 1.35 units. Correct joule conversion earns 6; a correct kW or hour conversion earns 3. Use 90 minutes = 1.5 h.')],8),
 ('viii','the cost of the energy used if the price of each unit of electricity is 22 cent.',None,[R('((1.35)( 22) =) 29.7 cent / 30 cent',6,note='Use the tariff printed in this 2012 problem. Accept follow-through from your energy answer; partial answer: 3.')],6),
]:
 sq=SQ(11,start,end)
 if roman=='i':sq=SQ(11,'What is the colour of the wire that should be connected to the fuse','in a plug?')
 if roman=='iv':sq=SQ(11,'A vacuum cleaner has a power rating of 900 W. What is the most','suitable fuse to use in the plug of the vacuum cleaner?')
 if roman=='vi':sq=SQ(11,'Name a device found in modern domestic circuits that has the','same function as a fuse.')
 if roman=='viii':sq=SQ(11,'cost of the energy used if the price of each unit of electricity is 22 cent')
 B('8'+roman,'Q8('+roman+')',6,start,end,11,rows,'phys-3-3' if roman not in ('vii','viii') else 'phys-1-4',total,sq=sq,stem=[PLUG]+([VACUUM] if roman in ('v','vii','viii') else [])+([P(6,'If the vacuum cleaner is used for 90 minutes, calculate')] if roman in ('vii','viii') else []),fig='q8-vacuum' if roman in ('iv','v','vii','viii') else None)
TEMP=P(6,'The temperature of an object is a measure of its hotness or coldness.')
HEAT=P(6,'When heat is transferred to a substance, it causes a rise in temperature or a change in','state of the substance, or both.')
ICE=P(6,'20 g of ice cubes at 0 °C are added to a glass of warm water.','calculate:')
CONSTANTS=P(6,'(specific heat capacity of water = 4180 J kg⁻¹ K⁻¹ ;','specific latent heat of fusion of ice = 3.34 × 10⁵ J kg⁻¹)')
for roman,start,end,rows,total in [
 ('i','What is the SI unit of temperature?',None,[R('K',6,note='Kelvin, symbol K. Partial answer: 3.')],6),
 ('ii','The Celsius scale is the practical temperature scale.','How is the degree Celsius (°C) related to the SI unit of temperature?',[R('θ/t = T – 273(.15)',6,note='Celsius temperature = kelvin temperature − 273.15; the scheme also accepts 273. The printed θ/t means alternative symbols for Celsius temperature, not division. Partial answer: 3.')],6),
 ('iii','What is heat?',None,[R('(a form of) energy / mcΔθ /ml',6,note='Heat is energy transferred because of a temperature difference. Partial answer: 3.')],6),
 ('iv','Name the three methods of heat transfer.',None,[R('conduction, convection, radiation',6,note='All three methods: 6; incomplete answer: 3. The scheme gives one collective tariff, not 2 marks per method.')],6),
 ('v','What is meant by the change in state of a substance?',None,[R('any change between solid, liquid or gas',3)],3),
 ('vi','Define specific latent heat.',None,[R('(amount of )energy required to change 1 kg of the substance from one state',6,'to another (without a change in temperature)',note='Partial answer: 3.')],6),
 ('vii','The energy required to melt the ice.',None,[R('(E = ml = (20×10⁻³)(3.34 ×10⁵) = ) 6.68 ×10³ J',9,units=[3,3,3],note='Correct formula: 3; correct substitution: 6; final answer 6680 J: 9. Convert 20 g to 0.020 kg.')],9),
 ('viii','The energy required to warm the melted ice to 5 °C.',None,[R('(E = mcΔθ = (20×10⁻³)(4.18 ×10³)(5) = ) 418 J',9,units=[3,3,3],note='Correct formula: 3; two correctly substituted quantities: 6; final answer: 9. The melted ice warms from 0 to 5 °C.')],9),
 ('ix','Why is it important to stir the mixture?',None,[R('to ensure temperature equilibrium // to ensure the ice melts quickly',5,note='Partial answer: 3.')],5),
]:
 sq=SQ(12,start,end)
 if roman=='vii':sq=SQ(12,start.rstrip('.'))
 B('9'+roman,'Q9('+roman+')',6,start,end,12,rows,'phys-2-1',total,sq=sq,stem=([TEMP] if roman in ('i','ii') else [HEAT])+([ICE,CONSTANTS] if roman in ('vii','viii','ix') else []),fig='q9-ice' if roman in ('vii','viii','ix') else None)
TUBE=P(7,'A cathode ray tube and an X-ray tube are practical applications of thermionic emission. In','these tubes thermionic emission releases electrons, which are then accelerated into a beam.')
# One freely chosen particle plus any two matching properties; no combination expansion.
U('Q10','particle','Subatomic particle and properties',P(7,'Name another subatomic particle and give two of its properties.'),[pt(S('correct particle 3',piece=1,psep=' 3'),3,kind='criterion',note='Choose a subatomic particle other than the electron. The scheme table gives proton and neutron examples.'),anyn(None,2,3,options=[S('mass'),S('charge'),S('location')],note='Any two matching properties, 3 each. Proton: mass approximately 1 u, charge +1e, inside nucleus. Neutron: mass approximately 1 u, charge zero, inside nucleus. The complete original table is shown; other valid particles/properties are accepted.')],'phys-4-3',SQ(13,'Name another subatomic particle and give two of its properties.'),9,stem=[TUBE,P(7,'An electron is a subatomic particle.')],fig='q10-particle-solution')
CRT=P(7,'The diagram shows a simple cathode ray tube.')
for roman,start,rows,total,sq in [
 ('i','Name the parts labelled A, B, C.',[R('A–cathode / hot metal',3),R('B– anode',3),R('C – screen',3,note='Three correct names with labels mismatched: 6; two correct names in incorrect order: 3.')],9,SQ(13,'Name the parts labelled A, B, and C in the diagram.')),
 ('ii','Give the function of any two of these labelled parts.',[anyn(None,2,3,steps=[6,3],options=[S('cathode emits (electrons)'),S('anode attracts/focuses /accelerates (electrons)'),S('screen (lights up to) show presence (of electrons)')],note='Choose any two of A, B and C. First correct function: 6; second: 3. Partial answer: 3.')],9,None),
 ('iii','How can the beam of electrons be deflected?',[R('electric field/electrode/magnetic field/magnet/X-Y plates',6,note='Partial answer: 3.')],6,None),
 ('iv','What happens at C when the electrons hit it?',[R('lights up / fluorescence / spot',6,note='Partial answer: 3.')],6,None),
 ('v','Why is a vacuum needed in a cathode ray tube?',[R('electrons not blocked / easier to pass through / electrons not absorbed',3)],3,None),
]:B('10'+roman,'Q10('+roman+')',7,start,None,13,rows,'phys-4-1',total,sq=sq or SQ(13,start),stem=[TUBE,CRT],fig='q10-crt')
U('Q10','xray','X-ray tube diagram',P(7,'Draw a sketch of an X-ray tube.'),[anyn(S('heater, cathode, anode, target, high voltage'),3,3,sep=', ',note='Any three components from the five printed examples, 3 each.'),R('detail e.g. correct arrangement / coolant / shielding/vacuum/extra item from previous line',2,note='An additional unused component can count as the detail. Partial answer: 3 overall.')],'phys-4-2',SQ(13,'Draw a sketch of an X-ray tube.'),11,stem=[TUBE,P(7,'In an X-ray tube, a beam of electrons is used to produce X-rays.')],fig='q10-xray-solution')
U('Q10','safety','X-ray safety precaution',P(7,'Give one safety precaution taken by a radiographer when using an X-ray machine.'),[R('use a lead shield, protective clothing, lead glass, monitor dosage, reduce dosage, etc.',3)],'phys-4-2',SQ(13,'Give one safety precaution taken by a radiographer when using an X-ray machine.'),3,stem=[TUBE])
for l,start,answer,end,topic in [
 ('a','What is meant by nuclear fission?','splitting nuclei // splitting (large) atoms',None,'phys-4-6'),
 ('b','What is radioactivity?','decay/splitting of a nucleus with the emission of particles/radiation',None,'phys-4-4'),
 ('c','What is a nuclear chain reaction?','a chain reaction is when the neutrons released during fission go on to split','more atoms / or produce more neutrons','phys-4-6'),
 ('d','What is the function of the control rods?','adjust the power output // absorb neutrons, etc.',None,'phys-4-6'),
 ('e','What type of material are control rods made of?','boron / steel / silver / indium / cadmium, etc. // neutron absorber',None,'phys-4-6'),
 ('f','Why did the reactor still generate heat even though the chain reaction had stopped?','because of the radioactive decay of the isotopes created during nuclear','fission','phys-4-4'),
 ('g','Why is it important to remove the heat generated?','to avoid over heating/ explosions / release of radiation',None,'phys-4-6'),
 ('h','Give one advantage of nuclear energy.','use less fuel for energy produced // does not pollute the air // fuel can be','produced (in a breeder reactor) //no greenhouse gases, etc.','phys-4-6'),
]:
 sq=SQ(14,start) if l!='f' else SQ(14,'Why did the reactor still generate heat even though the chain reaction','had stopped?')
 B('11'+l,'Q11('+l+')',8,start,None,14,[R(answer,7,end,note='Partial answer: 4. '+('“No greenhouse gases” refers to electricity generation during operation; the full lifecycle is not emission-free. See IPCC: https://archive.ipcc.ch/publications_and_data/ar4/wg3/en/ch4-ens4-3-2.html' if l=='h' else 'The full historical passage and source illustration remain available.'))],topic,7,sq=sq,fig='q11-passage')
CANNON=P(9,'A cannon of mass 1500 kg containing a cannonball of mass 80 kg was at rest','with an initial horizontal velocity of 60 m s⁻¹ and the cannon recoiled.')
U('Q12(a)','momentum','Conservation of momentum',P(9,'State the principle of conservation of momentum.'),[R('momentum before = momentum after // m₁ u₁ + m₂ u₂ = m₁ v₁ + m₂ v₂',6,note='Total momentum is conserved in an isolated system with no net external force. Partial equation or closed-system reference: 3.')],'phys-1-2',SQ(15,'Part (a) State the principle of conservation of momentum.'),6)
B('12ai','Q12(a)(i)',9,'the recoil velocity of the cannon',None,15,[R('v₁ = (–) 3.2 m s⁻¹',6,units=[3,3],note='0 = 1500v + 80(60), so v = −3.2 m/s, opposite to the cannonball. Correct momentum equation: 3.')],'phys-1-2',6,stem=[CANNON,P(9,'Calculate')],fig='q12-cannon')
B('12aii','Q12(a)(ii)',9,'the kinetic energy of the cannon as it recoils.',None,15,[R('(½(1500)(3.2)²= ) 7680 J / answer consistent with (i)',6,units=[3,3],note='E = ½mv². Accept follow-through from your recoil velocity; correct formula alone: 3.')],'phys-1-4',6,stem=[CANNON,P(9,'Calculate')],fig='q12-cannon')
U('Q12(a)','recoil','Why the cannon recoils',P(9,'Why did the cannon recoil?'),[R('to conserve momentum / to balance the cannon ball going forward',4)],'phys-1-2',SQ(15,'Why did the cannon recoil?'),4,stem=[CANNON],fig='q12-cannon')
U('Q12(a)','stopping','Cannon stopping distance',P(9,'Why will the cannon come to a stop in a shorter distance that the cannonball?'),[R('bigger mass / resistance of ground bigger than that of air / small recoil velocity',6,note='Ground resistance and the smaller recoil speed explain the shorter stopping distance in this scenario. Mass alone does not generally determine stopping distance. Partial answer: 3.')],'phys-1-2',SQ(15,'Why will the cannon come to a stop in a shorter distance that the cannonball?'),6,stem=[CANNON],fig='q12-cannon')
U('Q12(b)','laws','Laws of reflection',P(9,'State the laws of reflection of light.'),[R('the incident ray the normal and the reflected ray are all in the one plane',3),R('the angle of incidence is equal to the angle of reflection // i = r',3,note='Both reflection laws, 3 each.')],'phys-2-3',SQ(15,'Part (b) State the laws of reflection of light.'),6)
U('Q12(b)','focus','Estimate focal length',P(9,'How would you estimate the focal length of a concave mirror?'),[R('(reflect image of ) distant object',3),R('(onto) screen (and adjust screen until the image is sharp)',3),R('distance from screen to mirror is (approximate) focal length',3,note='A partial mirror-equation or centre-of-curvature reference earns 3.')],'phys-2-3',SQ(15,'How would you estimate the focal length of a concave mirror?'),9)
U('Q12(b)','rays','Concave mirror ray diagram',P(9,'Copy and complete the diagram to show the formation of the image of the object O.'),[pt(S('2 complete rays and image correctly drawn 3 × 3',piece=1,psep=' 3 × 3'),9,units=[3,3,3],kind='criterion',note='Draw two complete rays and the virtual, upright, enlarged image behind the mirror. At least one complete ray: 6; partial answer: 3. Original scheme diagram shown.')],'phys-2-3',SQ(15,'Copy and complete the diagram to show the formation of the image of the object O'),9,stem=[P(9,'The diagram shows an object O in front of a concave mirror, whose focus is at F.')],qfig='q12-mirror-question',fig='q12-mirror-solution')
U('Q12(b)','use','Concave mirror use',P(9,'Give one use for a concave mirror.'),[R('torch / headlights /searchlight, dentist mirror, cosmetic / shaving mirror,',4,'solar furnace, (reflecting) telescopes, etc.',note='One valid use. A use of a convex mirror/lens earns 2 in the historical scheme.')],'phys-2-3',SQ(15,'Give one use for a concave mirror.'),4)
FIRE=P(10,'The pitch of the sound emitted by the siren of a moving fire engine appears to change','as it passes a stationary observer.')
for roman,start,end,rows,total in [
 ('i','Name this phenomenon.',None,[R('Doppler effect',6,note='Partial answer: 3.')],6),
 ('ii','Explain, with the aid of a diagram, how this phenomenon occurs.',None,[R('moving wave source',3),R('wave fronts',3),R('as the moving wave source approaches',6,'the waves get closer together',units=[3,3],route='approaching',note='Approaching source: wavefronts bunch up, giving higher observed frequency.'),pt(S('// conversely as the wave','source moves away the waves are further apart',piece=2,psep='//'),6,units=[3,3],route='receding',note='Receding source: wavefronts spread out, giving lower observed frequency. Choose one complete explanation route. No diagram: maximum 9.')],12),
 ('iii','Will the crew in the fire engine notice this phenomenon?','Give a reason for your answer.',[R('no as there is no relative motion between the sound source and the crew',4,note='“No” alone earns 2. The crew move with the siren.')],4),
 ('iv','Give an application of this phenomenon.',None,[R('measuring speed / speed gun, (measuring) red shift, ultrasonic scanners, imaging',6,'used to study blood flow, used to study heart beat, weather forecasting, etc.',note='One specific valid use. General medicine/radar/sonar reference: 3.')],6),
]:B('12c'+roman,'Q12(c)('+roman+')',10,start,end,16,rows,'phys-2-7',total,stem=[FIRE],fig='q12-doppler-solution' if roman=='ii' else 'q12-fire',qfig='q12-doppler-question' if roman=='ii' else None)
CAP=P(10,'A capacitor is connected to a switch, a battery and a bulb as shown in the diagram.','When the switch is changed from position A to position B, the bulb lights briefly.')
for roman,start,end,rows,total in [
 ('i','What happens to the capacitor when the switch is in position A?',None,[R('it charges / short-lived current flows / stores energy',6,note='Partial current-flow answer: 3.')],6),
 ('ii','Why does the bulb light when the switch is in position B?',None,[R('capacitor discharges / current flows // (switch) closes the circuit',6,note='Partial answer: 3.')],6),
 ('iii','Why does the bulb light only briefly?',None,[R('capacitor discharges quickly / p.d. fades / current transient / capacitor only',6,'holds small charge / capacitor only stores a small amount of energy',note='Partial answer: 3.')],6),
 ('iv','The capacitor has a capacitance of 200 μF. Calculate its charge when','connected to a 6 V battery.',[R('(Q = CV = (200×10⁻⁶ )(6)= ) 1.2 ×10⁻³ C',6,note='Q = CV = 200 × 10⁻⁶ × 6 = 0.0012 C. Correct formula alone: 3.')],6),
 ('v','Give a use for a capacitor.',None,[R('store charge / (radio) tuning / filtering / smoothing / timing / coupling /',4,'store energy / flash camera / phone charger, etc.',note='One valid use. A partial “storing electric current” answer earns 2 historically; a capacitor stores charge and energy.')],4),
]:B('12d'+roman,'Q12(d)('+roman+')',10,start,end,16,rows,'phys-3-2',total,stem=[CAP],fig='q12-capacitor')
SELECTION_SCAN=[
 ('paper',2,'the following','The complete calibration data table is retained.'),
 ('paper',3,'the following','Apparatus context retained with all related tasks.'),
 ('paper',3,'the following','All seven I/V pairs retained.'),
 ('paper',4,'the following','All ten Q5 options retained; no best-eight combinations.'),
 ('paper',4,'one of the following','One choose-one card retaining all four named instruments.'),
 ('paper',6,'or','Complete list of five fuse ratings remains in context.'),
 ('paper',6,'or','Hotness/coldness definition, not an option pool.'),
 ('paper',6,'or','Temperature/state-change narrative, not an option pool.'),
 ('paper',6,'or','Same heat-transfer narrative.'),
 ('paper',6,'both','Same heat-transfer narrative.'),
 ('paper',6,'or','Both no-heat-loss assumptions remain in calculation context.'),
 ('paper',7,'any two','One cathode-ray-tube function card with two slots and all three options, first6 then3.'),
 ('paper',8,'or','Historical narrative about grid/diesel supply; full passage retained.'),
 ('paper',9,'any two','All four complete 28-mark Q12 options retained, without combinations.'),
 ('paper',9,'the following','Same Q12 outer selection.'),
]
FIGURES={
 'q1-velocity-solution':('scheme',4,(90,267,398,311),SEC,[],'Complete accepted final-velocity methods and distance/time formula.',True),
 'q1-acceleration-solution':('scheme',4,(92,437,375,468),SEC,[],'Both acceleration formulas with the original fraction layout.',True),
 'q2-graph-question':('paper',2,(83,518,542,683),SEC,[],'Complete calibration context, all six pairs and graph request.',False,[(517,652,542,683)]),
 'q2-reading-question':('paper',2,(83,518,542,718),SEC,[],'Complete six-point calibration table and property-60 reading request.',False,[(83,652,542,683),(517,689,542,718)]),
 'q2-graph-solution':('scheme',5,(90,507,408,725),SEC,[],'Original calibration curve with both axes, all six points and reading guides.',True),
 'q3-data':('paper',3,(110,245,473,360),SEC,[],'All four incidence/refraction pairs and three empty calculation columns.',False),
 'q3-angle-question':('paper',3,(83,70,548,360),SEC,[],'Complete Snell experiment context and angle-identification task.',False,[(83,149,548,202),(517,204,548,219),(83,226,548,241)]),
 'q3-angle-solution':('scheme',6,(142,357,361,454),SEC,[],'Original incident and refracted ray diagram with angles measured from the normal.',True),
 'q3-table-question':('paper',3,(83,70,548,360),SEC,[],'Complete experiment context, all given angles and the table-completion task.',False,[(83,149,548,219),(517,226,548,241)]),
 'q3-table-solution':('scheme',6,(90,534,406,632),SEC,[],'Complete official four-row table of sines and ratios.',True),
 'q4-apparatus':('paper',3,(323,452,545,573),SEC,['X','Y','Z'],'Complete copper-sulfate circuit, labelled instruments, copper electrodes and solution.',False),
 'q4-graph-question':('paper',3,(83,419,545,722),SEC,['X','Y','Z'],'Full circuit context, seven I/V pairs and graph request.',False,[(83,551,321,567),(83,571,545,607),(517,692,545,722)]),
 'q4-resistance-question':('paper',3,(83,419,545,755),SEC,['X','Y','Z'],'Full circuit context and all seven data pairs with slope/resistance request.',False,[(83,551,321,567),(83,571,545,607),(83,692,545,722),(517,740,545,755)]),
 'q4-graph-solution':('scheme',7,(73,380,408,584),SEC,[],'Original V-against-I graph, axes and straight-line fit.',True),
 'q4-resistance-solution':('scheme',7,(78,689,395,750),SEC,[],'Original gradient and resistance calculations, with both permitted axis orientations.',True),
 'q5-tow':('paper',4,(201,249,326,284),SEC,[],'Original tow-truck and car illustration.',False),
 'q5-bridge':('paper',4,(403,390,509,463),SEC,[],'Original Tacoma bridge photograph.',False),
 'q5-ldr-question':('paper',4,(111,619,552,693),SEC,[],'LDR symbol request with its full photograph.',False,[(111,619,471,628)]),
 'q5-ldr-solution':('scheme',8,(141,604,204,652),SEC,[],'Original LDR circuit symbol with incoming light arrows.',True,[(141,646,154,652)]),
 'q6-module':('paper',5,(419,37,574,207),SEC,[],'Original lunar module photograph and caption.',False),
 'q6-forces-question':('paper',5,(83,37,574,262),SEC,[],'Moon gravity, spacecraft context, full module data/photo and force-diagram request.',False,[(83,70,411,87),(83,129,411,176),(517,246,574,262)]),
 'q6-forces-solution':('scheme',9,(260,299,421,385),SEC,[],'Original module diagram with downward weight and upward thrust arrows.',True,[(260,299,299,303)]),
 'q7-terms-question':('paper',5,(83,501,543,545),SEC,[],'Both original underlined wave terms and the definition request.',False,[(517,529,543,545)]),
 'q7-glasses':('paper',5,(329,565,548,687),SEC,[],'Original Polaroid sunglasses photograph.',False,[(329,672,430,687),(517,670,548,687)]),
 'q8-vacuum':('paper',6,(437,151,584,297),SEC,[],'Original vacuum-cleaner photograph.',False),
 'q9-ice':('paper',6,(452,599,552,754),SEC,[],'Original ice-and-water glass illustration.',False),
 'q10-particle-solution':('scheme',13,(83,134,471,193),SEC,[],'Full proton/neutron table with mass, charge and location.',True),
 'q10-crt':('paper',7,(137,188,455,282),SEC,['A','B','C'],'Complete cathode ray tube, A/B/C labels, power connection and polarity.',False),
 'q10-xray-solution':('scheme',13,(129,616,414,710),SEC,[],'Original labelled X-ray tube including heater, cathode, anode/target and high voltage.',True),
 'q11-passage':('paper',8,(83,85,575,456),SEC,[],'Complete Fukushima passage, annotated reactor illustration and June2011 attribution.',False),
 'q12-cannon':('paper',9,(412,193,556,322),SEC,[],'Complete before/after cannon and cannonball illustration.',False),
 'q12-mirror-question':('paper',9,(111,507,543,704),SEC,['O','F','C'],'Complete object/focus context, original mirror diagram and image-formation request.',False,[(522,687,543,704)]),
 'q12-mirror-solution':('scheme',15,(129,570,399,704),SEC,[],'Original ray construction with two full rays and the virtual image.',True,[(239,683,399,704)]),
 'q12-fire':('paper',10,(215,94,398,243),SEC,[],'Original fire-engine siren illustration with emitted wavefronts.',False,[(215,94,279,99)]),
 'q12-doppler-question':('paper',10,(111,70,544,293),SEC,[],'Complete moving-fire-engine context, illustration and diagram/explanation task.',False,[(111,256,544,272),(517,277,544,293)]),
 'q12-doppler-solution':('scheme',16,(82,150,216,269),SEC,[],'Original moving-source wavefront diagram and wavelength spacing.',True),
 'q12-capacitor':('paper',10,(183,470,410,567),SEC,['A','B'],'Complete battery/capacitor/bulb circuit, both switch positions and 6V supply.',False),
}
# Mark figure labels as questions only where their identities are actually asked.
for t in TASKS:
 if t['fig']=='q4-apparatus' or t['qfig'] in ('q4-graph-question','q4-resistance-question'):
  t['labels']=[L('X',S('milliammeter / ammeter /galvanometer / multimeter',page=7),True),L('Y',S('rheostat / (variable) resistor / potential divider / potentiometer',page=7),True),L('Z',S('using a voltmeter/ with Z',page=7),True)]
 if t['fig']=='q10-crt':t['labels']=[L('A',S('A–cathode / hot metal',page=13),True),L('B',S('B– anode',page=13),True),L('C',S('C – screen',page=13),True)]
 if t['qfig']=='q12-mirror-question':t['labels']=[L(l,P(9,'The diagram shows an object O in front of a concave mirror, whose focus is at F.'),False) for l in 'OFC']
 if t['fig']=='q12-capacitor':t['labels']=[L(l,CAP,False) for l in 'AB']

# The printed full tariffs are separate cells from the partial-credit note.
for t in TASKS:
 if t['key']=='1i':t['cells']='Trolley/runway or air-track/glider pair earns6+3, plus one apparatus detail3; the extraction associates only the partial6 cell.'
 if t['key']=='7ii':t['cells']='All three apparatus pieces collectively6, method3, observation3; the isolated3 beside one piece is partial credit.'
ASK_EXEMPT=[
 (6,'When heat is transferred to a substance, it causes a rise in temperature or a change in','Narrative context retained in all related heat tasks; no additional ask.'),
 (8,'When the reactor was shut down due to the earthquake, the pumps to keep the cooling','Narrative in the complete passage, which is retained on all eight passage cards.'),
 (9,'Calculate','Shared command retained in both recoil-velocity and kinetic-energy cards; both calculations are separately carded.'),
 (10,'When the switch is changed from position A to position B, the bulb lights briefly.','Narrative circuit context retained in all five capacitor cards.'),
]
