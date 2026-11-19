"""2014 Ordinary Physics: every page independently reviewed against the scheme.
All 12 paper and 20 scheme pages visually read; five first-use SymbolMT glyphs
checked. Keep full experimental data, passages, alternatives and diagram labels.
"""
from phys_review_lib import Q,SQ,S,G,pt,anyn,allof,T,L
YEAR,LEVEL=2014,'ol'
REVIEWED_AT='2026-11-01'
LETTERED={5,7,11,12}
SOURCES={'paper':{'path':'examiner-reports/physics/papers/2014-ol-paper.pdf','fileid':'LC021GLP000EV.pdf','sha256':'3407ac46166bebbff21c67d30d618a082d8330207462532b707d05f4a446f5f3','pages':12},'scheme':{'path':'examiner-reports/physics/schemes/2014-ol.pdf','fileid':'LC021GLP000EV.pdf','sha256':'b3a9b22cb91b0f825adb50b22f07f6c243e1c58349a5e672c0385f2e8eb007c1','pages':20}}
# SEC archive returned HTTP 403. Unmodified SEC scheme mirrored at:
# https://www.thephysicsteacher.ie/Exam%20Material/LC%20Physics/pdf/Ordinary%20Level/Marking%20Schemes/2014.pdf
PAGE_ROLES={'paper':{1:'cover',**{p:'questions' for p in range(2,11)},11:'blank',12:'blank'},'scheme':{1:'cover',2:'note',3:'conventions',**{p:'marking' for p in range(4,17)},17:'blank',18:'blank',19:'blank',20:'back-cover'}}
GLYPHS={'SymbolMT':{113:'°',117:'×',118:'∝',16:'−',32:'='}};VERIFIED_LINES=[]
QUESTION_TOTALS={**{q:40 for q in range(1,5)},**{q:56 for q in range(5,12)},12:112}
PART_TOTALS={(7,'a'):30,(7,'b'):26,**{(11,l):7 for l in 'abcdefgh'},**{(12,l):28 for l in 'abcd'}}
BEST_OF={5:(8,7)};GROUP_TOTALS={};CHECKSUMS={};ROUTES={}
SCAN_PAGES={'paper':range(2,11)};SELECTION_SCAN=[]
ASK_SCAN_PAGES={'paper':range(2,11)};ASK_EXEMPT=[]
P=Q;SEC='State Examinations Commission';CRIT='The scheme prints this marking criterion rather than a worked answer.'
def R(text,marks,end=None,**kw):return pt(S(text,end),marks,**kw)
def C(text,marks,end=None,**kw):return pt(S(text,end),marks,kind='criterion',note=kw.pop('note',CRIT),**kw)
def EQ(page,clip,expect,marks,**kw):return G('equation',page=page,clip=clip,expect=expect,marks=marks,**kw)
def FR(page,clip,expect,marks,**kw):return G('fraction',page=page,clip=clip,expect=expect,marks=marks,**kw)
TASKS=[];FIGURES={}
def U(ref,slug,label,q,rows,topic,sq,total,**kw):
 TASKS.append(T(ref+':'+slug,ref,'A' if int(ref.split('(')[0][1:])<5 else 'B',q,rows,topic,slug,sq,total,item=(slug,label),**kw))
def B(key,ref,page,start,end,sp,rows,topic,total,**kw):
 sq=kw.pop('sq',SQ(sp,start,end));TASKS.append(T(key,ref,'A' if int(ref.split('(')[0][1:])<5 else 'B',P(page,start,end),rows,topic,key,sq,total,**kw))
STEM1=P(2,'A student investigated the laws of equilibrium','equilibrium.')
for roman,slug,start,end,rows,total in [
 ('i','measure','How did the student measure the upward forces?',None,[R('newton balance',4,note='A partial answer such as “balance” earns 2 marks.')],4),
 ('ii','forces','Copy the diagram and show all the forces acting on the metre stick.',None,[C('copy diagram and show given forces',3),R('shows weight /1.5 N downward at 50 cm mark',3)],6),
 ('iii)(a','upward','Find the total upward force acting on the metre stick.',None,[R('( 9 + 12.5 = ) 21.5 (N)',6,note='Partial answer: 3 marks.')],6),
 ('iii)(b','downward','Find the total downward force acting on the metre stick.',None,[R('(5 + 15 + 1.5 =) 21.5 (N)',6,note='Partial answer, such as omitting the metre stick’s weight: 3 marks.')],6),
 ('iii)(c','force-balance','Explain how these values verify one of the laws of equilibrium.',None,[R('forces are equal // sum of acting forces is zero // forces up = forces down',3)],3),
 ('iv)(a','anticlockwise','Find the sum of the anticlockwise moments of the upward forces about the 0 mark.',None,[R('((9)(0.2) + (12.5)(0.9) = 1.8 + 11.25 =) 13.05 (N m)',6,note='Partial answer such as one correct moment or F × d: 3 marks.')],6),
 ('iv)(b','clockwise','Find the sum of the clockwise moments of the downward forces about the 0 mark.',None,[R('((5)(0.36) + (1.5)(0.5) + (0.7)(15) = 1.8 + 0.75 + 10.5 =) 13.05 (N m )',6,note='Read the 5 N force at the 36 cm tick on the original scale. Partial answer: 3 marks.')],6),
 ('iv)(c','moment-balance','Explain how these values verify the other law of equilibrium.',None,[R('moments are equal // sum of the moments equals zero',3)],3),
]:
 sq=SQ(4,start,end)
 if roman=='iv)(a':sq=SQ(4,'Find the sum of the anticlockwise moments of the upward forces','about the 0 mark.')
 if roman=='iv)(b':sq=SQ(4,'Find the sum of the clockwise moments of the downward forces','about the 0 mark.')
 B('1'+roman,'Q1('+roman+')',2,start,end,4,rows,'phys-1-2',total,sq=sq,stem=[STEM1],fig='q1-forces')
STEM2=P(2,'A student carried out an experiment to measure the specific latent heat','specific latent heat of fusion of ice. I then repeated my experiment.”')
for roman,start,rows,total in [
 ('i','Draw a labelled diagram of the apparatus used in this experiment.',[R('calorimeter (with water)',3),R('thermometer',3,'// temperature sensor'),R('ice',3),R('other detail e.g. insulation/(electronic) balance/stirrer, etc.',3,note='Deduct one mark if no labels. An incorrect experiment is capped at 9 marks.')],12),
 ('ii','What measurements would the student have taken for this experiment?',[anyn(None,3,3,steps=[6,3,3],options=[S('mass of empty calorimeter'),S('mass of calorimeter and water','// mass of water'),S('mass of calorimeter with water and ice','// mass of (dried) ice'),S('initial temperature of water'),S('final temperature of water (and melted ice)','// temperature difference')],note='Any three measurement lines; 6+3+3. Measurements may be inferred from the diagram. General reference to masses and temperatures earns 6; partial answer earns 3.')],12),
 ('iii','How was the ice crushed?',[R('any valid method e.g. (place in a plastic bag/towel and hit) with a hammer // blended',4,note='A diagram may merit full marks; partial answer earns 2.')],4),
 ('iv','Why was the ice crushed?',[pt(S('crushed ice melts faster // reference to larger surface area // to ensure all the ice is 0 °C 6',piece=1,psep=' 6'),6,note='Partial answer such as less heat loss: 3 marks.')],6),
 ('v','Why was the experiment repeated?',[R('increase accuracy // to get average',6,note='Partial answer: 3 marks.')],6),
]:
 sq=SQ(5,'Draw a labelled diagram of the apparatus used in the experiment.') if roman=='i' else SQ(5,'How was the ice crushed ?') if roman=='iii' else SQ(5,start)
 B('2'+roman,'Q2('+roman+')',2,start,None,5,rows,'phys-2-1',total,sq=sq,stem=[STEM2])
STEM3=P(3,'An experiment was set up to investigate','recorded. The procedure was repeated for different values of f and l.')
rows=[R('sonometer and string',3)]
for i,route in enumerate(['tuning-fork','signal-generator'],1):
 rows += [pt(S('tuning fork(s)','// signal generator',piece=i,psep='//'),3,route=route),pt(S('bridge(s) and metre stick / detail','// bridges and magnet / detail',piece=i,psep='//'),3,route=route,note='Use the apparatus for the same method. Deduct one mark for no labels.')]
B('3i','Q3(i)',3,'Draw a labelled diagram of the apparatus used in the experiment.',None,6,rows,'phys-2-6',9,stem=[STEM3],decision='Two complete apparatus routes share the sonometer criterion. Each totals 9 marks; never add both routes.')
B('3ii','Q3(ii)',3,'Indicate on your diagram the length of the string that was measured.',None,6,[R('distance between bridges indicated',6,note='Partial answer: 3 marks.')],'phys-2-6',6,sq=SQ(6,'Indicate on your diagram the length of the string that was measured'),stem=[STEM3])
B('3iii','Q3(iii)',3,'Describe how the string could have been set vibrating.',None,6,[R('place a vibrating tuning fork on bridge // send signal from signal generator through it',3)],'phys-2-6',3,stem=[STEM3])
B('3iv','Q3(iv)',3,'How was the frequency determined?',None,6,[R('read off the tuning fork',6,'// read off the signal generator',note='Use the frequency source for your chosen method. Partial answer: 3 marks.')],'phys-2-6',6,stem=[STEM3])
B('3v','Q3(v)',3,'Copy and complete the table into your answer book. Draw a graph on graph paper of f','graph?',6,[R('1/l (m⁻¹) 1.25 1.41 1.56 1.67 1.89 2.33',5,kind='point',units=[1]*5,note='Five missing reciprocals, 1 mark each; 1.41 was already supplied. Keep all six data pairs.'),C('labelled axes – names/ symbol / unit acceptable',3),C('plot five points correctly',3),C('straight line graph',3,note='Without graph paper, or with f on the Y-axis, the graph is capped at 6 marks.'),pt(S('conclusion; f and l are inversely proportional // f l = constant // linear relationship //',piece=1,psep=' //'),2,note='The source also accepts f × l = constant, an appropriate linear relationship, f proportional to 1/l, or an answer consistent with the graph.')],'phys-2-6',16,sq=SQ(6,'Copy and complete the table into your answer book. Draw a graph on graph paper of','graph?'),stem=[STEM3],qfig='q3-graph-question',fig='q3-graph-solution')
STEM4=P(3,'A student carried out an experiment to investigate the variation of current','plotted a graph of my results, as shown below.”')
for roman,start,rows,total in [
 ('i','How was the voltage changed in this experiment?',[R('using the potential divider // by varying the resistance/the battery/power supply',6,note='Partial answer: 3 marks.')],6),
 ('ii','What is the function of part X?',[R('measure current',6,note='Naming the ammeter without its function earns 3 marks.')],6),
 ('iii','What is the function of part Y?',[R('measure voltage',6,note='Naming the voltmeter without its function earns 3 marks.')],6),
 ('iv','What does the graph tell you about conduction in a diode?',[R('current varies linearly with voltage until 0.6 V',6,'below 0.6 V, etc',note='The plotted curve shows very little current below 0.6 V; the source accepts that description. Partial description earns 3.'),R('after 0.6 V the current increases (rapidly) with voltage, etc',6,note='Partial description earns 3. An incomplete description of the whole graph may earn 9.')],12),
 ('v','How would a student connect the diode in reverse bias?',[R('switch the polarity of battery / diode',6,note='Partial answer: 3 marks.')],6),
 ('vi','What is the function of the 330 Ω resistor?',[R('protection / limit the current',4,note='Partial answer: 2 marks.')],4),
]:B('4'+roman,'Q4('+roman+')',3,start,None,7,rows,'phys-3-3',total,stem=[STEM4],fig='q4-circuit-graph')
for l,start,end,rows,topic in [
 ('a','A crane, powered by an electric motor, has a bucket that weighs','the crane’s motor.',[R('((540 + 800)(75) = ) 1.005 × 10⁵ (N m)',7)],'phys-1-4'),
 ('b','Which of the following are vector quantities and which are scalar quantities?','time force mass velocity',[allof([(None,S('force and velocity are vectors quantities')),(None,S('time and mass are scalar quantities'))],7,note='All four classifications are required for the published seven marks.')],'phys-1-1'),
 ('c','Which of the following is used in the flash of a camera?','electroscope hydrometer capacitor barometer',[R('capacitor',7)],'phys-3-2'),
 ('d','What is the Doppler effect?',None,[R('(apparent) change in (wave) frequency due to motion (of the wave source)',7)],'phys-2-7'),
 ('e','Name the lens shown and give an application of it.',None,[anyn(None,2,3,steps=[4,3],options=[S('(bi) convex / converging'),S('used as a magnifying glass/(eye) glasses /binoculars/camera/etc.','used as a magnifying glass/(eye) glasses /binoculars/camera/etc.')],note='Both the correct name and an application are required; either line alone earns 4 marks.')],'phys-2-3'),
 ('f','What is meant by the U-value of a material?',None,[R('measure of the heat flow through 1 m² of material each second (perpendicular to',7,'the two sides',note='Partial answer: 4 marks.')],'phys-2-1'),
 ('g','Name the component with the symbol shown in the diagram.',None,[R('light dependent resistor / LDR',7)],'phys-3-3'),
 ('h','Name a piece of laboratory equipment used to separate white light into its colours.',None,[R('(glass) prism // (diffraction) grating',7)],'phys-2-4'),
 ('i','How are X-rays produced?',None,[R('(when high speed) electrons hit a metal target',7)],'phys-4-2'),
 ('j','In the Sun, a mass of 4 × 10⁹ kg is converted into energy every second.','(speed of light, c = 3 × 10⁸ m s⁻¹)',[R('(E = m c² = (4× 10⁹)(3 × 10⁸) ² =) 3.6 × 10²⁶ (J)',7)],'phys-4-5'),
]:
 sq=SQ(8,start,end)
 if l=='a':sq=SQ(8,'A crane, powered by an electric motor, has a bucket that weighs 540 N when','building site. Calculate the work done by the crane’s motor.')
 if l=='b':sq=SQ(8,start)
 if l=='c':sq=SQ(8,'Which of the following is used in the flash of a camera ?','electroscope hydrometer capacitor barometer')
 if l=='h':sq=SQ(8,'Name a piece of laboratory equipment used to separate white light into','its colours.')
 if l=='j':sq=SQ(8,'In the Sun, a mass of 4 × 10⁹ kg is converted into energy every second. Calculate the','energy released each second.')
 B('5'+l,'Q5('+l+')',4,start,end,8,rows,topic,7,sq=sq,fig={'a':'q5-crane','e':'q5-lens','g':'q5-ldr'}.get(l))
# The scheme prices force at 6 and its unit at 3. Keep the three definitions as
# complete alternatives, then a separately practicable unit task.
rows=[]
for route,first,second in [
 ('acceleration',S('(force) causes / changes // (F=) m',piece=1,psep='//'),S('acceleration')),
 ('equation',S('(force) causes / changes // (F=) m',piece=2,psep='//'),S('acceleration')),
 ('momentum',S('// (rate of ) change of',piece=2,psep='//'),S('// momentum',piece=2,psep='//'))]:
 rows.extend([pt(first,3,route=route),pt(second,3,route=route)])
U('Q6','force','Definition of force',P(5,'Define force','Define force'),rows,'phys-1-2',SQ(9,'Define force and give the unit of force',paired='The first six marks define force; the separate unit is three marks.'),6,decision='Three complete six-mark definitions, never summed together.')
U('Q6','unit','Unit of force',P(5,'give the unit of force.'),[R('Unit: newton / N / kg m s⁻²',3)],'phys-1-2',SQ(9,'Define force and give the unit of force'),3)
U('Q6','gravitation','Newton’s law of gravitation',P(5,'State Newton’s law of universal gravitation.'),[R('force proportional / F ∝',3),R('product of masses / m₁m₂',3),pt(S('inversely proportional to the square of the distance between them /',piece=1,psep=' /'),3,note='Partial answer such as a reference to G earns 3 marks.')],'phys-1-5',SQ(9,'State Newton’s law of universal gravitation.'),9)
MARS=P(5,'Use the equation below, which is from page 56 of the Formulae and Tables booklet, to','is 3.4 × 10⁶ m and the mass of Mars is 6.4 × 10²³ kg.')
U('Q6','mars-g','Gravity on Mars',MARS,[EQ(9,(65,341,290,375),'(g = GM/d² = (6.67 × 10⁻¹¹)(6.4 × 10²³)/(3.4 × 10⁶)² =)3.7 (ms⁻²)',10,note='One error earns 7; a correct constant or substitution earns 4. Answer to one decimal place.')],'phys-1-5',SQ(9,'Use the equation below, which is from page 56 of the Formulae and Tables booklet, to','is 3.4 × 10⁶ m and the mass of Mars is 6.4 × 10²³ kg.'),10,qfig='q6-gravity-question',fig='q6-gravity-solution')
ROVER=P(5,'The Curiosity rover was built on Earth to travel on the','surface of Mars. The rover has a mass of 899 kg.')
EARTHG=P(5,'(acceleration due to gravity, g = 9.8 m s⁻²)')
U('Q6','wheels','Strength of the rover’s wheels',P(5,'Give a reason for this.'),[R('weighs less on Mars // gravity is less on Mars // the mass of Mars is smaller than',6,'mass of Earth',note='Partial answer: 3 marks.')],'phys-1-5',SQ(9,'Give a reason for this.'),6,stem=[P(5,'In August 2012 the Curiosity rover landed on Mars.','that would be needed if the rover was to be used on Earth.')],fig='q6-rover')
for roman,start,answer,total in [('i','the weight of Curiosity on Earth','W = mg = (899)(9.8) = 8.8 × 10³ (N)',6),('ii','the mass of Curiosity on Mars','899 (kg) // the same as on Earth',6),('iii','the weight of Curiosity on Mars.','W = mg = (899)(3.7) = 3.3 × 10³ (N)',4)]:
 B('6'+roman,'Q6('+roman+')',5,start,None,9,[R(answer,total,note='The scheme accepts a value consistent with your calculated Martian g or mass. Partial answer: 2 marks.' if roman=='iii' else 'Partial answer: 3 marks.')],'phys-1-5',total,sq=SQ(9,start.rstrip('.')),stem=[MARS,ROVER,EARTHG,P(5,'Find','Find')],fig='q6-rover')
U('Q6','spectrum','Other electromagnetic waves',P(5,'Name one other part of the electromagnetic spectrum.'),[anyn(S('microwaves, infra-red, visible light, ultra-violet, X-rays, gamma rays'),1,6,sep=', ',note='One part other than radio waves. Partial answer: 3 marks.')],'phys-2-4',SQ(9,'Name one other part of the electromagnetic spectrum.'),6,stem=[P(5,'The Curiosity rover communicates with Earth using radio waves, which are part of the','electromagnetic spectrum.')])
STEM7A=P(5,'The temperature of an object can be measured using a thermometer which is','based on a suitable thermometric property.')
for roman,start,rows in [
 ('i','What is heat?',[R('(a form of) energy / mcΔθ /ml',6,note='Partial answer: 3 marks.')]),
 ('ii','What is meant by temperature?',[R('degree of hotness // measurement of hotness/coldness',6,note='Partial answer: 3 marks.')]),
 ('iii','Give an example of a thermometric property.',[R('length (of a liquid column), resistance (of a thermistor / conductor), emf /',6,'volume (of a gas at constant pressure), pressure (of a constant volume of gas), etc',kind='point',note='Give one of these properties. A definition alone earns 3 marks.')]),
 ('iv','The SI unit of temperature is the kelvin. Give another temperature scale.',[R('Celsius /°C // Fahrenheit /°F',6,note='Partial answer: 3 marks.')]),
 ('v','Express 310 K in the units of the scale you have named in part (iv).',[R('310 – 273 = 37± 0.2 (°C)',6,note='The scheme illustrates Celsius. If you chose Fahrenheit, 310 K is 98.33 °F (about 98.6 °F using 273 in the Celsius conversion). Partial answer: 3 marks.')]),
]:B('7a'+roman,'Q7(a)('+roman+')',5,start,None,10,rows,'phys-2-1',6,stem=[STEM7A]+([P(5,'The SI unit of temperature is the kelvin. Give another temperature scale.')] if roman=='v' else []),fig='q7-thermometer')
STEM7B=P(5,'The photograph shows an experiment to compare the heat','used to heat the metals at the centre of the apparatus.')
for roman,start,end,rows,total in [
 ('i','How is heat transferred in metals?',None,[R('conduction // vibrating atoms (transfer energy)',6,note='Partial answer: 3 marks.')],6),
 ('ii','Name the two other methods of heat transfer.',None,[R('convection',4),R('radiation',4)],8),
 ('iii','How can this experiment be used to find out which of the metals is best at','allowing heat transfer?',[pt(S('(heat under the centre) the piece of wood which falls first indicates the best conductor 6',piece=1,psep=' 6'),6,note='Partial answer: 3 marks.')],6),
 ('iv','State one way to make sure that this is a fair test.',None,[R('ensure that there is only one (independent) variable // heat in the centre /ensure',6,'are the same length // ensure to have the same amount of wax, etc',note='One valid control; partial answer: 3 marks.')],6),
]:B('7b'+roman,'Q7(b)('+roman+')',5,start,end,10,rows,'phys-2-1',total,sq=SQ(10,start.rstrip('.') if roman=='ii' else start,end),stem=[STEM7B],fig='q7-metals')
STEM8=P(6,'A ray of light can undergo both reflection and refraction.')
REFRACT=P(6,'The diagram shows a ray of light travelling from glass','to air. The ray of light undergoes refraction at B.')
ANGLE=P(6,'In the diagram the value of the angle i is 38°.')
B('8i','Q8(i)',6,'Explain what is meant by reflection of light.',None,11,[R('sending back / returning / bouncing',3),R('from a mirror / (shiny) surface',3,note='A diagram may merit full marks.')],'phys-2-3',6,stem=[STEM8])
B('8ii','Q8(ii)',6,'State the laws of reflection of light.',None,11,[anyn(None,2,3,steps=[6,3],options=[S('the incident ray, (the normal) and the reflected ray are all in the same plane'),S('the angle of incidence is equal to the angle of reflection // i = r','the angle of incidence is equal to the angle of reflection // i = r')],note='Both laws: 9 marks. Either correct law alone: 6. Partial answer: 3.')],'phys-2-3',9,stem=[STEM8])
B('8iii','Q8(iii)',6,'Give an application of reflection of light.',None,11,[anyn(S('mirror images, optic fibres, binoculars, endoscope, specific toys, etc'),1,5,sep=', ',open_list=True,note='Partial answer: 3 marks.')],'phys-2-3',5,stem=[STEM8])
rows=[R('apparatus; raybox /laser',3,'// drawing pins'),R('mirror',3)]
for i,route in enumerate(['same-plane','equal-angles'],1):
 rows.extend([pt(S('procedure; mark position of rays / pins // measure i and r',piece=i,psep='//'),3,route=route),pt(S('observation/conclusion; incident ray, reflected ray and normal in same plane // i = r',piece=i,psep='//'),3,route=route,note='Keep procedure and conclusion from the same method. Valid alternatives and labelled diagrams are accepted.')])
B('8iv','Q8(iv)',6,'Describe an experiment to demonstrate one of the laws of reflection of light.',None,11,rows,'phys-2-3',12,stem=[STEM8],decision='Two full 12-mark routes share six apparatus marks; never add routes.')
B('8v','Q8(v)',6,'Explain what is meant by refraction of light.',None,11,[R('bending of light at the boundary when going from one medium to another',6,note='A labelled diagram may earn full marks; partial answer earns 3.')],'phys-2-3',6,sq=SQ(11,'Explain what is meant by the refraction of light'),stem=[REFRACT],fig='q8-refraction')
B('8vi','Q8(vi)',6,'What special name is given to the angle of','diagram occurs?',11,[R('critical angle / C',6,note='Partial answer: 3 marks.')],'phys-2-3',6,sq=SQ(11,'What special name is given to the angle of incidence, i, when the effect','shown in the diagram occurs?'),stem=[REFRACT],fig='q8-refraction')
B('8vii','Q8(vii)',6,'Calculate the value of the refractive index of the glass.',None,11,[EQ(11,(91,588,201,621),'n = 1/sinC = 1/sin38 = 1.62',6,note='Use degrees. A correct equation or intermediate step earns 3. The scheme deducts one for a radians/gradians-mode result.')],'phys-2-3',6,stem=[REFRACT,ANGLE],qfig='q8-index-question',fig='q8-index-solution')
B('8viii','Q8(viii)',6,'Draw a diagram to show what happens to the ray of light when the angle of incidence is','increased to 40°.',11,[R('reflection at boundary',6,note='At 40°, beyond the 38° critical angle, show total internal reflection. Partial answer: 3 marks.')],'phys-2-3',6,stem=[REFRACT,ANGLE],qfig='q8-reflection-question',fig='q8-reflection-solution')
STEM9=P(6,'A magnetic field exists around a current-carrying conductor.')
COIL=P(6,'A coil of wire is connected as shown in the diagram to','a galvanometer. A bar magnet is placed near the coil.')
B('9i','Q9(i)',6,'What is a magnetic field?',None,12,[R('region ( where) / space',3),R('magnetism is experienced // force is detected',3)],'phys-3-4',6,stem=[STEM9])
B('9ii','Q9(ii)',6,'How does a compass indicate the direction of a magnetic field?',None,12,[R('(experiences a force in a magnetic field and) points in the direction of the field lines',6,note='Partial answer: 3 marks.')],'phys-3-4',6,stem=[STEM9])
B('9iii','Q9(iii)',6,'Describe an experiment to show that there is a magnetic field around a','current-carrying conductor and sketch the field lines around the conductor.',12,[C('apparatus; power supply/ battery / voltage, conductor, compass',3,note='Any two listed items earn these three marks; power supply/battery/voltage are alternatives for one item.'),R('procedure; set up the circuit / turn on the power supply / current',3),R('observation/conclusion; compass deflects',3),R('field lines; circular lines (with correct direction)',3,note='Labelled diagrams and valid alternatives such as iron filings are accepted. An incorrect experiment is capped at 6 marks.')],'phys-3-4',12,sq=SQ(12,'Describe an experiment to show that there is a magnetic field around a','current-carrying conductor and sketch the field lines around the conductor'),stem=[STEM9],fig='q9-field-solution')
B('9iv','Q9(iv)',6,'Sketch the magnetic field around a bar magnet.',None,12,[C('magnet, field lines and correct direction',6,note='Partial diagram: 3 marks.')],'phys-3-4',6,fig='q9-magnet-solution')
rows=[]
for i,route in enumerate(['galvanometer','current'],1):rows.extend([pt(S('needle / pointer / galvanometer','// current',piece=i,psep='//'),3,route=route),pt(S('deflects','// induced',piece=i,psep='//'),3,route=route)])
B('9v','Q9(v)',6,'What is observed when the magnet is moved towards the coil?',None,12,rows,'phys-3-6',6,stem=[COIL],fig='q9-coil',decision='Two complete 3+3 descriptions of the same observation, not additive.')
B('9vi','Q9(vi)',6,'What is observed when the magnet is stationary?',None,12,[R('needle / pointer / galvanometer does not deflect // no current, etc',6,note='Partial answer: 3 marks.')],'phys-3-6',6,stem=[COIL],fig='q9-coil')
B('9vii','Q9(vii)',6,'Explain these observations.',None,12,[R('emf / voltage / current / electromagnetic induction',6),R('due to changing magnetic field (around the coil)',3)],'phys-3-6',9,stem=[COIL,P(6,'What is observed when the magnet is moved towards the coil?'),P(6,'What is observed when the magnet is stationary?')],fig='q9-coil')
B('9viii','Q9(viii)',6,'How would increasing the speed of movement of the magnet alter the observations?',None,12,[R('greater deflection/ emf // current is greater',5,note='Partial answer: 3 marks.')],'phys-3-6',5,sq=SQ(12,'How would increasing the speed of movement of the magnet alter the','observations?'),stem=[COIL],fig='q9-coil')
RAD=P(7,'In an experiment, the radiation from a radioactive source is passed through an electric field,','as shown in the diagram.')
FISSION=P(7,'Nuclear fission occurs in a nuclear power station such as the one shown in the photograph.')
B('10i','Q10(i)',7,'What is meant by radioactivity?',None,13,[R('(spontaneous) emission of (one or more types of) particles/energy / α / β / γ',3),R('from the nuclei (of atoms)',3)],'phys-4-4',6)
B('10ii','Q10(ii)',7,'What does this experiment indicate about radiation?',None,13,[R('there are three different types // there is positive, negative and neutral radiation',6,note='Partial answer: 3 marks.')],'phys-4-4',6,sq=SQ(13,'What does this experiment indicate about radiation.'),stem=[RAD],fig='q10-radiation')
for roman,start,answer in [('iii','is unaffected by electric fields','2 / gamma / γ'),('iv','is positively charged','1 / alpha / α'),('v','is negatively charged.','3 / beta / β')]:
 B('10'+roman,'Q10('+roman+')',7,start,None,13,[R(answer,3)],'phys-4-4',3,sq=SQ(13,start.rstrip('.')),stem=[RAD,P(7,'State which type of radiation (1, 2 or 3)')],fig='q10-radiation')
B('10vi','Q10(vi)',7,'Give the name of radiation types 1, 2 and 3, in that order.',None,13,[R('alpha, gamma, beta',9,kind='point',note='All three in the stated order: 9. Correct names in the wrong order: 6. Any one correct: 3.')],'phys-4-4',9,stem=[RAD],fig='q10-radiation')
B('10vii','Q10(vii)',7,'Name a suitable fuel for nuclear fission.',None,13,[anyn(S('(enriched) uranium/ U, plutonium / Pu, thorium / Th'),1,6,sep=', ',note='Partial answer naming a reactor part: 3 marks.')],'phys-4-6',6,stem=[FISSION],fig='q10-station')
B('10viii','Q10(viii)',7,'Explain the role of neutrons in nuclear fission.',None,13,[R('hit nucleus, are absorbed, cause fission / chain reaction',6,note='Partial answer: 3 marks.')],'phys-4-6',6,stem=[FISSION],fig='q10-station')
B('10ix','Q10(ix)',7,'Explain how the control rods can control the rate of fission, or stop the reaction','completely.',13,[R('absorb neutrons // raise to increase // lower to decrease/stop',6,note='Partial answer: 3 marks.')],'phys-4-6',6,sq=SQ(13,'Explain how the control rods can control the rate of fission, or stop the','reaction completely'),stem=[FISSION],fig='q10-station')
B('10x','Q10(x)',7,'Iodine–131 is a product of nuclear fission. The half-life of iodine–131 is 8 days.','What fraction of iodine–131 remains after 24 days?',13,[FR(13,(86,723,97,753),'1/8',8,note='24 ÷ 8 = 3 half-lives; remaining fraction = (1/2)³. A partial answer earns 4 marks.')],'phys-4-4',8,fig='q10-half-life-solution')
PASSAGE=P(8,'Lightning is one of the most deadly natural phenomena','(Adapted from ‘howstuffworks.com’)')
for l,start,answer,topic in [
 ('a','Explain the term evaporation.','process by which a liquid absorbs heat and changes to a gas','phys-2-1'),
 ('b','What effect does the addition of heat have on the molecules of a liquid?','they move around faster','phys-2-1'),
 ('c','What happens to the temperature of a gas rising through the atmosphere?','it drops','phys-2-1'),
 ('d','What part does gravity play in the water cycle?','causes the liquid to fall back down to the earth','phys-1-5'),
 ('e','Explain the term convection.','transfer of heat/energy by the movement of atoms/molecules / currents','phys-2-1'),
 ('f','What helps create the conductive path needed for lightning to occur?','cloud’s (strong) electric field','phys-3-2'),
 ('g','Name an instrument used in the laboratory to study static electricity.','electroscope / GLE // Van De Graaff generator // capacitor, etc','phys-3-1'),
 ('h','Why do we see the flash of lightning before we hear the thunder?','sound travels (much) slower than light','phys-2-5'),
]:B('11'+l,'Q11('+l+')',8,start,None,14,[R(answer,7,note='Partial answer: 4 marks.')],topic,7,sq=SQ(14,'Why effect does the addition of heat have on the molecules of a liquid?' if l=='b' else start),stem=[PASSAGE],fig='q11-passage')
U('Q12(a)','speed-velocity','Speed and velocity',P(9,'Explain the distinction between speed and velocity.'),[R('velocity is speed in a given direction // velocity is a vector // sound is a scalar',6,note='The source’s “sound is a scalar” is a typographical error: speed is scalar, while velocity includes direction. Partial answer: 3 marks.')],'phys-1-1',SQ(15,'Explain the distinction between speed and velocity.'),6)
BUS=P(9,'A bus leaves a bus stop and accelerates from rest at 0.5 m s⁻² to reach a speed of','stop, the driver applies the brakes uniformly to bring the bus to a stop in 20 seconds.')
for roman,start,answer in [('i','the time it took the bus to reach its top speed','( t = (v-u)/a = (15 – 0 ) / 0.5 = ) 30 (s)'),('ii','the distance it travelled while at its top speed','( s = vt = (15)(100)= ) 1500 (m)'),('iii','the acceleration required to bring the bus to a stop.','(a= (v – u ) / t = (0– 15 ) / 20 = ) (–) 0.75 (m s ⁻²)')]:
 B('12a'+roman,'Q12(a)('+roman+')',9,start,None,15,[R(answer,5,note='A valid equation or partial answer earns 3 marks.')],'phys-1-1',5,stem=[BUS,P(9,'Calculate','Calculate')],fig='q12-bus')
U('Q12(a)','graph','Velocity–time graph of the bus',P(9,'Sketch a velocity-time graph of the bus journey.'),[C('v increasing, v constant, v decreasing',7,note='Show 0–30 s acceleration to 15 m s⁻¹, 30–130 s constant velocity, and 130–150 s deceleration to rest. Partial answer: 4 marks.')],'phys-1-1',SQ(15,'Sketch a velocity-time graph of the bus journey.'),7,stem=[BUS],qfig='q12-bus-graph-question',fig='q12-bus-graph-solution')
U('Q12(b)','pressure-unit','Unit of pressure',P(9,'State the unit of pressure.'),[R('Pa / N m⁻² / bar',5,note='Partial answer: 3 marks.')],'phys-1-2',SQ(15,'State the unit of pressure.'),5)
rows=[]
for i,route in enumerate(['inverted-glass','collapsing-can'],1):
 for start,end in [('apparatus: glass of water and cardboard','// can of water and heat source'),('procedure: place cardboard over glass and invert // boil water and put on lid',None),('observation/conclusion: water remains in glass // can collapses',None)]:rows.append(pt(S(start,end,piece=i,psep='//'),3,route=route,note='Use all three steps from one method; valid alternatives and diagrams are accepted.'))
U('Q12(b)','pressure-experiment','Demonstrating atmospheric pressure',P(9,'Describe an experiment to demonstrate that the atmosphere exerts pressure.'),rows,'phys-1-2',SQ(15,'Describe an experiment to demonstrate that the atmosphere exerts pressure'),9,decision='Two complete 9-mark experiment routes, never added together.')
U('Q12(b)','archimedes','Archimedes’ principle',P(9,'State Archimedes’ principle.'),[R('The upthrust (on a body immersed in a liquid) is equal to the weight of the',6,'liquid displaced',note='Partial answer: 3 marks.')],'phys-1-2',SQ(15,'State Archimedes’ principle'),6)
BUOY=P(9,'The diagram shows the reading on a','on a balance.')
B('12bi','Q12(b)(i)',9,'What is the upthrust (buoyancy force) on','the object caused by the liquid?',15,[R('3 (N)',4,note='Partial answer: 2 marks.')],'phys-1-2',4,sq=SQ(15,'What is the upthrust (buoyancy force) on the object caused by the liquid?'),stem=[BUOY],fig='q12-buoyancy')
B('12bii','Q12(b)(ii)',9,'Will the object float in the liquid if','Explain your answer.',15,[R('no / it won’t / it will sink',2),R('the upthrust is less than the weight, it is more dense, diagram shows it immersed',2,note='Use the force comparison: 3 N upthrust is smaller than the object’s 10 N weight.')],'phys-1-2',4,sq=SQ(15,'Will the object float in the liquid if released? Explain your answer.'),stem=[BUOY],fig='q12-buoyancy')
WAVE=P(10,'The diagram shows a transverse wave.')
B('12ci','Q12(c)(i)',10,'Name the distances labelled A and B.',None,16,[R('A = wavelength / λ',5,note='Partial answer: 3 marks.'),R('B = amplitude / height of wave',5,note='Partial answer: 3 marks.')],'phys-2-2',10,stem=[WAVE],fig='q12-wave',labels=[L('A',S('A = wavelength / λ',page=16),True),L('B',S('B = amplitude / height of wave',page=16),True)])
B('12cii','Q12(c)(ii)',10,'20 waves pass a fixed point every second. What is the frequency of the wave?',None,16,[R('20 (Hz)',6,note='Partial answer: 3 marks.')],'phys-2-2',6,stem=[WAVE],fig='q12-wave')
B('12ciii','Q12(c)(iii)',10,'Calculate the velocity of the wave if distance A = 1.5 m.',None,16,[R('(v = f λ = (20)(1.5) = ) 30 ( m s⁻¹)',6,note='A correct equation earns 3 marks.')],'phys-2-2',6,stem=[WAVE,P(10,'20 waves pass a fixed point every second.','20 waves pass a fixed point every second.')],fig='q12-wave')
B('12civ','Q12(c)(iv)',10,'Transverse waves can be polarised. Name a type of wave that cannot be','polarised.',16,[R('longitudinal // sound // pressure',6,note='Partial answer: 3 marks.')],'phys-2-4',6)
CIRCUIT=P(10,'The circuit diagram shows a resistor and a thermistor connected in series with a 6 V','battery. At a certain temperature the resistance of the thermistor is 450 Ω.')
for roman,start,end,rows,total in [
 ('i','State Ohm’s law.',None,[R('Vα I // V = IR',6,note='At constant temperature, voltage is proportional to current. The source uses α for the proportionality sign. Partial answer: 3 marks.')],6),
 ('ii','What is the total resistance of the circuit?',None,[R('500 (Ω)',4,note='The series resistance is 50 + 450 = 500 Ω. Partial answer: 2 marks.')],4),
 ('iii','What is the current in the circuit?',None,[EQ(16,(93,616,226,649),'(I = V/R = 6/500 =) 1.2 × 10⁻³ (A)',6,note='The source has an exponent typo. Correct calculation: I = 6/500 = 0.012 A = 1.2 × 10⁻² A. The scheme accepts an answer consistent with the preceding resistance; a correct equation earns 3 marks.')],6),
 ('iv','What is the potential difference across the 50 Ω resistor?',None,[R('(V = IR = (1.2 × 10⁻³)(50) = ) 0.6 (V)',6,note='The source repeats the current exponent typo. Use I = 0.012 A: V = 0.012 × 50 = 0.6 V, matching its final voltage. A consistent prior-current answer is accepted; a correct equation earns 3 marks.')],6),
 ('v','What would happen to the resistance of the circuit if the temperature were','increased?',[R('it would decrease',6,'// depends on the thermistor',note='For the usual negative-temperature-coefficient thermistor, resistance decreases. The scheme also accepts a response qualified by thermistor type. Partial answer: 3 marks.')],6),
]:B('12d'+roman,'Q12(d)('+roman+')',10,start,end,16,rows,'phys-3-3',total,stem=[CIRCUIT],fig='q12-circuit')
# All crops retain source geometry. Solution figures appear only after reveal.
for key,doc,page,rect,alt,solution in [
 ('q1-forces','paper',2,(165,216,415,338),'Original metre-stick scale and four labelled applied forces.',False),
 ('q1-forces-solution','scheme',4,(154,250,409,368),'All five forces including the 1.5 N metre-stick weight.',True),
 ('q3-data','paper',3,(90,229,482,296),'All six frequency and length pairs, with the supplied reciprocal and five blanks.',False),
 ('q3-graph-question','paper',3,(84,56,534,348),'Full string experiment, six-row data table and graph task.',False),
 ('q3-graph-solution','scheme',6,(84,386,479,775),'Completed reciprocal table, labelled graph and published graph criteria.',True),
 ('q4-circuit-graph','paper',3,(74,488,508,606),'Complete 9 V diode circuit with 330 Ω resistor, X/Y meters and I–V curve.',False),
 ('q5-crane','paper',4,(443,168,529,268),'Original crane illustration.',False),
 ('q5-lens','paper',4,(397,464,534,525),'Converging rays through the pictured lens.',False),
 ('q5-ldr','paper',4,(411,546,535,596),'Complete component symbol including incident light arrows.',False),
 ('q6-rover','paper',5,(352,150,559,357),'Original Curiosity rover illustration.',False),
 ('q6-gravity-question','paper',5,(84,129,556,211),'Full Martian radius and mass with the original g = GM/d² equation.',False),
 ('q6-gravity-solution','scheme',9,(63,340,345,403),'Complete gravitational equation, substitution, units and partial-credit criteria.',True),
 ('q7-thermometer','paper',5,(400,505,547,585),'Original laboratory thermometer.',False),
 ('q7-metals','paper',5,(433,621,557,709),'Original metal-rod heat transfer experiment.',False),
 ('q8-refraction','paper',6,(354,148,535,276),'Complete glass–air critical-angle diagram with B, i and right-angle indicator.',False),
 ('q8-index-question','paper',6,(84,147,556,314),'Full critical-angle context, diagram, 38-degree value and refractive-index ask.',False),
 ('q8-index-solution','scheme',11,(91,589,320,649),'Original n = 1/sin C equation and worked index.',True),
 ('q8-reflection-question','paper',6,(84,147,556,349),'Full original glass–air diagram, critical angle and 40-degree reflection task.',False),
 ('q8-reflection-solution','scheme',11,(98,682,261,754),'Original total internal reflection solution diagram.',True),
 ('q9-field-solution','scheme',12,(312,259,491,366),'Original circular magnetic-field diagram with current and field direction.',True),
 ('q9-magnet-solution','scheme',12,(77,382,228,462),'Original bar-magnet field lines with N/S poles and direction arrows.',True),
 ('q9-coil','paper',6,(372,544,529,616),'Complete magnet, coil and galvanometer diagram.',False),
 ('q10-radiation','paper',7,(199,147,395,331),'All three radiation paths, electric-field plates, charges and number labels.',False),
 ('q10-station','paper',7,(208,524,411,647),'Original nuclear power-station photograph.',False),
 ('q10-half-life-solution','scheme',13,(84,722,318,784),'Original one-eighth fraction and partial-credit guidance.',True),
 ('q11-passage','paper',8,(84,79,538,416),'Complete lightning passage, photograph and attribution.',False),
 ('q12-bus','paper',9,(112,124,486,171),'Original bus illustration.',False),
 ('q12-bus-graph-question','paper',9,(112,124,530,351),'Full bus data and velocity–time graph ask.',False),
 ('q12-bus-graph-solution','scheme',15,(63,330,300,423),'Original velocity–time graph with every time, velocity and unit label.',True),
 ('q12-buoyancy','paper',9,(370,527,547,742),'Full balance apparatus and all three readings: 10 N, 7 N and 3 N.',False),
 ('q12-wave','paper',10,(207,88,386,187),'Complete transverse-wave diagram with A and B arrows.',False),
 ('q12-circuit','paper',10,(193,449,411,588),'Full 6 V series circuit with 50 Ω resistor and 450 Ω thermistor.',False),
 ('q12-current-solution','scheme',16,(93,615,425,664),'Original current equation, including the historical exponent typo, with visible correction supplied in the answer guidance.',True),
 ('q12-voltage-solution','scheme',16,(83,678,428,708),'Original voltage calculation with repeated exponent typo; corrected working is supplied in the answer guidance.',True),
]:FIGURES[key]=(doc,page,rect,SEC,[],alt,solution)
# Question-figure masks remove other tasks while retaining the entire context.
for key,masks in {
 'q3-graph-question':[(84,110,534,193)],
 'q6-rover':[(352,150,375,212),(352,229,378,291),(352,299,375,331)],
 'q6-gravity-question':[(531,190,556,211)],
 'q8-index-question':[(84,211,351,276),(532,211,556,276),(532,297,556,314)],
 'q8-reflection-question':[(84,211,351,276),(532,211,556,276),(84,297,556,315),(532,334,556,349)],
 'q12-bus-graph-question':[(112,235,530,313)],
}.items():
 f=list(FIGURES[key]);f.append(masks);FIGURES[key]=tuple(f)
for task in TASKS:
 key=task['key']
 if key=='1ii':task.update(fig='q1-forces-solution',qfig='q1-forces-question')
 if key in {'3i','3ii','3iii','3iv'}:task['fig']='q3-data'
 if key=='12diii':task.update(fig='q12-current-solution',qfig='q12-current-question')
 if key=='12div':task.update(fig='q12-voltage-solution',qfig='q12-voltage-question')
FIGURES['q1-forces-question']=('paper',2,(84,157,555,395),SEC,[],'Full equilibrium context, scale, all applied forces and diagram task.',False,[(84,349,555,369),(532,379,555,395)])
for key,y0,y1 in [('q12-current-question',629,642),('q12-voltage-question',646,660)]:
 FIGURES[key]=('paper',10,(112,384,556,y1+2),SEC,[],'Full series-circuit values, context and target calculation.',False,[(112,591,556,y0-1),(531,y0-1,556,y1+2)])
SELECTION_SCAN=[
 ('paper',2,'the following','Full ice-experiment report retained.'),
 ('paper',3,'the following','All six frequency and length pairs retained.'),
 ('paper',3,'the following','Full diode-experiment report, circuit and graph retained.'),
 ('paper',4,'the following','All ten Q5 parts retained, without best-eight combinations.'),
 ('paper',4,'the following','All four classifications required in one seven-mark response.'),
 ('paper',4,'the following','One choice from all four printed instruments; one card.'),
 ('paper',6,'both','Reflection and refraction are shared context, not a choice.'),
 ('paper',7,'or','Three numbered radiation paths are the answer pool for each separately priced identification.'),
 ('paper',7,'or','Control and stopping are alternative outcomes of one control-rod explanation.'),
 ('paper',9,'any two','All four Q12 options retained at 28 marks each, no combinations.'),
 ('paper',9,'the following','Same outer Q12 selection.'),
]
# Final source selectors: distinguish the paper's Ohm glyph from the scheme's,
# and preserve shared verbs when a priced subtask is lifted on its own.
CELL_NOTES={
 '3v':'The table tariff is 5×1, graph 3×3 and conclusion 2. The graph-axis tariff appears beside a floating axis label; the 16-mark total is printed beside the question.',
 'Q6:force':'Two 3-mark definition rows per alternative. The following separately priced unit earns three and is a different card.',
 'Q6:unit':'Unit row is explicitly three marks; the preceding definition is a separate six-mark task.',
 '9vii':'The final three-mark tariff is printed alone below the changing-field row.',
 '10i':'The second three-mark tariff is printed alone below the nuclei row.',
}
for task in TASKS:
 k=task['key']
 if k in CELL_NOTES:task['cells']=CELL_NOTES[k]
 for sel in ([task['q']] if isinstance(task['q'],dict) else task['q'])+task.get('stem',[]):
  if sel.get('src')=='paper':
   for field in ['start','end']:
    if sel.get(field):sel[field]=sel[field].replace('Ω','Ω')
 if k=='Q6:force':task['q']=P(5,'Define force and give the unit of force.',piece=1,psep=' and ')
 if k=='Q6:unit':task['q']=P(5,'Define force and give the unit of force.',piece=2,psep=' and ')
 if k in {'6i','6ii','6iii'}:task['q']=[P(5,'Find','Find'),task['q']]
 if k in {'10iii','10iv','10v'}:task['q']=[P(7,'State which type of radiation (1, 2 or 3)'),task['q']]
 if k in {'12ai','12aii','12aiii'}:task['q']=[P(9,'Calculate','Calculate'),task['q']]
 if k=='Q6:mars-g':task['rows'][0].update(kind='fraction',glyph_order=True,expect='(g= GM/d² = ((6.67 ×10⁻¹¹)(6.4 ×10²³))/(3.4 ×10⁶)² =)3.7 (ms⁻²)')
 if k=='8ii':task['rows'][0]['options'][1]=S('the angle of incidence is equal to the angle of reflection // i = r two lines correct',piece=1,psep=' two lines correct')
 if k=='8vii':task['rows'][0].update(kind='fraction',expect='n= 1/(sinC) = 1/(sin38) =1.62')
 if k=='8viii':task['sq']=SQ(11,'Draw a diagram to show what happens to the ray of light when the angle of incidence','is increased to 40°.')
 if k=='10x':task['rows'][0]['expect']='⅛'
 if k=='Q12(a):speed-velocity':task['sq']=SQ(15,'Part (a) Explain the distinction between speed and velocity.')
 if k=='Q12(b):pressure-unit':task['sq']=SQ(15,'Part (b) State the unit of pressure.')
 if k=='12diii':task['rows'][0].update(kind='fraction',glyph_order=True,expect='(I= V/R = 6/500 =) 1.2 ×10⁻³(A)')
ASK_EXEMPT=[
 (8,'and changes to a gas. When a liquid is heated its molecules','Narrative condition inside the full lightning passage; retained on every passage card.'),
 (9,'15 m s⁻¹. It then maintains this speed for 100 seconds. When it approaches the next','Narrative condition in the full bus data, retained on every bus calculation and graph card.'),
]
for task in TASKS:
 if task['key']=='Q12(b):pressure-unit':task['sq']['paired']='The scheme prefixes this exact pressure-unit question with Part (b); the five-mark row is separate from the experiment.'
 if task['key']=='12dii':task['rows'][0]['sel']['start']='500 (Ω)'
# Visual crop pass: retain every label and remove neighbouring question text.
for key,rect in {
 'q12-buoyancy':(370,527,570,742),
 'q6-rover':(352,176,559,357),
 'q12-current-solution':(80,617,425,664),
 'q3-graph-solution':(84,386,491,775),
 'q8-refraction':(354,163,535,276),
}.items():
 f=list(FIGURES[key]);f[2]=rect;FIGURES[key]=tuple(f)
for key,masks in {
 'q6-rover':[(352,249,369,266),(532,190,559,211),(537,264,559,281)],
 'q6-gravity-question':[(352,176,556,212),(531,190,556,211)],
 'q7-thermometer':[(400,503,486,517)],
 'q8-index-question':[(84,147,556,162),(84,211,351,276),(532,211,556,276),(532,297,556,314)],
 'q8-reflection-question':[(84,147,556,162),(84,211,351,276),(532,211,556,276),(84,297,556,315),(532,334,556,349)],
 'q12-bus-graph-solution':[(275,350,300,381)],
 'q12-current-solution':[(80,617,107,619),(142,617,425,619)],
 'q3-graph-question':[(84,110,534,193),(531,332,534,348)],
 'q4-circuit-graph':[(74,488,359,490)],
 'q9-field-solution':[(469,259,491,280),(466,301,491,333),(451,359,491,366)],
}.items():
 f=list(FIGURES[key]);f=f[:7]+[masks];FIGURES[key]=tuple(f)
for task in TASKS:
 k=task['key']
 if k=='1iii)(c':task['stem'] += [P(2,'Find the total upward force acting on the metre stick.'),P(2,'Find the total downward force acting on the metre stick.')]
 if k=='1iv)(c':task['stem'] += [P(2,'Find the sum of the anticlockwise moments of the upward forces about the 0 mark.'),P(2,'Find the sum of the clockwise moments of the downward forces about the 0 mark.')]
 if k=='3ii':task['stem'] += [P(3,'Draw a labelled diagram of the apparatus used in the experiment.')]
 if k in {'6i','6ii'}:task['stem']=[ROVER,EARTHG]
 if k=='6iii':task['fig']='q6-gravity-question'
for task in TASKS:
 k=task['key']
 if k=='12civ':
  task['q']['end_nth']=2
  task['sq']['end_nth']=2
 if k in {'6iii','12ai','12aii','12aiii','10iii','10iv','10v'}:
  task['stem']=[s for s in task['stem'] if s.get('start') not in {'Find','Calculate','State which type of radiation (1, 2 or 3)'}]
 if k=='8iii':task['rows'][0]['options']=[S('mirror images, optic fibres, binoculars, endoscope, specific toys, etc',piece=i,psep=', ') for i in range(1,6)];task['rows'][0]['sel']=None
 if k=='4ii':task['labels']=[L('X',S('measure current',page=7),True)]
 if k=='4iii':task['labels']=[L('Y',S('measure voltage',page=7),True)]
