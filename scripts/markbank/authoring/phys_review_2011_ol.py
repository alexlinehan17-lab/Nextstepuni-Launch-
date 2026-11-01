"""2011 Ordinary Physics: independent visual review of all 12 paper and 16 scheme pages.
Preserve every question option, practical dataset, source diagram and marking boundary.
"""
from phys_review_lib import Q,SQ,S,G,pt,anyn,allof,T,L
YEAR,LEVEL=2011,'ol'
REVIEWED_AT='2026-11-01'
LETTERED={5,8,9,11,12}
SOURCES={'paper': {'path': 'examiner-reports/physics/papers/2011-ol-paper.pdf', 'sha256': '4c550d82994eb92fa024c95a135f227ce760f66c4e1be964876efd1b256abaa6', 'pages': 12, 'fileid': 'LC021GLP000EV.pdf'}, 'scheme': {'path': 'examiner-reports/physics/schemes/2011-ol.pdf', 'sha256': '189ada90ad67a87f023b0b62b109746b270eed4ef5e732d8a45f11d041a3d62f', 'pages': 16, 'fileid': 'LC021GLP000EV.pdf'}}
PAGE_ROLES={'paper':{1:'cover',**{p:'questions' for p in range(2,11)},11:'blank',12:'blank'},'scheme':{1:'cover',2:'conventions',**{p:'marking' for p in range(3,16)},16:'back-cover'}}
# All 49 special-font/non-ASCII first occurrences visually checked.
GLYPHS={'paper': {'SymbolMT': {113: '°', 117: '×'}, 'TimesNewRomanPS-BoldMT': {105: 'á', 126: 'ú', 177: '–'}, 'TimesNewRomanPSMT': {179: '“', 180: '”', 181: '‘', 182: '’', 237: '−', 238: '×'}, 'Verdana': {177: '–', 181: '‘', 182: '’'}}, 'scheme': {'SymbolMT': {16: '−', 32: '=', 77: 'φ', 113: '°', 117: '×', 118: '∝'}, 'Times-Roman': {19: 'á', 20: 'ú'}, 'TimesNewRomanPS-BoldMT': {70: '‘', 71: '’', 72: '×', 167: '≈', 237: '−', 302: 'α', 533: 'β', 534: 'γ'}, 'TimesNewRomanPS-ItalicMT': {537: 'θ', 540: 'λ'}, 'TimesNewRomanPSMT': {73: '‘', 74: '’', 75: '“', 76: '”', 77: '−', 78: '°', 79: '±', 80: '°', 81: '½', 82: '×', 83: '÷', 159: 'Ω', 237: '−', 302: 'α', 507: 'Δ', 533: 'β', 534: 'γ'}}}
VERIFIED_LINES=[]
QUESTION_TOTALS={**{q:40 for q in range(1,5)},**{q:56 for q in range(5,12)},12:112}
PART_TOTALS={(8,'a'):34,(8,'b'):22,(9,'a'):32,(9,'b'):24,**{(11,l):7 for l in 'abcdefgh'},**{(12,l):28 for l in 'abcd'}}
BEST_OF={5:(8,7)};GROUP_TOTALS={};CHECKSUMS={};ROUTES={}
SCAN_PAGES={'paper':range(2,11)};SELECTION_SCAN=[]
ASK_SCAN_PAGES={'paper':range(2,11)};ASK_EXEMPT=[]
P=Q;SEC='State Examinations Commission';CRIT='The scheme prints this marking criterion rather than a worked answer.'
def R(text,marks,end=None,**kw):
 kw.setdefault('kind','point')
 return pt(S(text,end),marks,**kw)
def C(text,marks,end=None,**kw):return pt(S(text,end),marks,kind='criterion',note=kw.pop('note',CRIT),**kw)
def FR(page,clip,expect,marks,**kw):return G('fraction',page=page,clip=clip,expect=expect,marks=marks,**kw)
def EQ(page,clip,expect,marks,**kw):return G('equation',page=page,clip=clip,expect=expect,marks=marks,degrees=True,dedupe=True,**kw)
def BE(page,clip,expect,marks,**kw):return EQ(page,clip,expect,marks,baseline=True,**kw)
def BF(page,clip,expect,marks,**kw):return FR(page,clip,expect,marks,baseline=True,dedupe=True,glyph_order=True,segments=True,**kw)
TASKS=[];FIGURES={}
def U(ref,slug,label,q,rows,topic,sq,total,**kw):
 TASKS.append(T(ref+':'+slug,ref,'A' if int(ref.split('(')[0][1:])<5 else 'B',q,rows,topic,slug,sq,total,item=(slug,label),**kw))
def B(key,ref,page,start,end,sp,rows,topic,total,**kw):
 sq=kw.pop('sq',SQ(sp,start,end));TASKS.append(T(key,ref,'A' if int(ref.split('(')[0][1:])<5 else 'B',P(page,start,end),rows,topic,key,sq,total,**kw))
STEM1=P(2,'The following is an extract from a student’s report of an experiment to verify the principle','I used my measurements to verify the principle of conservation of momentum.”')
B('1i','Q1(i)',2,'Draw a labelled diagram of the apparatus used in the experiment.',None,3,[anyn(None,3,3,options=[S('2 trolleys / 2 riders'),S('runway / air-track'),S('timer: photo- gates (and timer)// tickertape (and timer) /other valid variation'),S('detail e.g. means of measuring mass/ distance')],note='Three correctly drawn and labelled components, 3 each. A motion sensor/data logger can earn 6 for measuring velocity; use the matching apparatus route. Deduct 2 if there are no labels.')],'phys-1-2',9,stem=[STEM1],fig='q1-apparatus-solution')
B('1ii','Q1(ii)',2,'How did the student measure the mass of a trolley?',None,3,[R('used (electronic) balance / (weighing) scales / weighed them',6,note='Partial answer: 3.')],'phys-1-2',6,stem=[STEM1])
B('1iii','Q1(iii)',2,'How did the student determine the velocity of a moving trolley?',None,3,[BF(3,(89,525,220,556),'(velocity=) distance/(time) / s/t',12,units=[3,3,3,3],note='Measure a distance and its corresponding elapsed time, then divide distance by time. The source gives 12 for the complete method, 6 for two method elements and 3 for a partial answer; a motion sensor/data logger reference earns at least 6.')],'phys-1-1',12,stem=[STEM1],fig='q1-velocity-solution')
B('1iv','Q1(iv)',2,'How was the momentum of a trolley determined?',None,3,[R('mv',6,note='Momentum = mass × velocity. Partial answer: 3.')],'phys-1-2',6,stem=[STEM1])
B('1v','Q1(v)',2,'How did the student verify the principle of conservation of momentum?',None,3,[R('(upon repeating the experiment a number of times) the value for momentum',7,'experimental error) // m₁ u₁ + m₂u₂ = m₁ v₁ + m₂v₂ / m₁ u = (m₁ + m₂)v',note='Compare total momentum before and after the collision; repeat to check agreement within experimental uncertainty. Partial answer: 4.')],'phys-1-2',7,stem=[STEM1])
STEM2=P(2,'During an experiment to measure the specific latent heat of vaporisation of water, cold water','a rise in temperature of the water and the calorimeter. The following data were recorded.')
CONST2=P(2,'(specific heat capacity of copper = 390 J Kg⁻¹ K⁻¹ ; specific heat capacity of water = 4180 J Kg⁻¹ K⁻¹)')
for roman,start,rows,total in [
 ('i','Draw a labelled diagram of the apparatus used in the experiment.',[anyn(None,3,3,options=[S('calorimeter (containing water)'),S('thermometer (in water) / temperature sensor'),S('steam source'),S('detail e.g. insulation, steam delivery tube, stirrer, etc.')],note='Any three apparatus components, 3 each. Deduct 2 for no labels.')],9),
 ('ii','What was the rise in temperature of the water in the experiment?',[R('(19 −10 = ) 9 (°C)',6,note='Final minus initial temperature: 19 − 10 = 9 °C. Partial answer: 3.')],6),
 ('iii','Describe how the mass of the cold water was found.',[R('(mass of calorimeter and cold water) − (mass of calorimeter)',7,note='Weigh the filled and empty calorimeter and subtract. Partial answer: 4.')],7),
 ('iv','How was the steam dried?',[R('steam trap / delivery tube sloping up',6,note='Partial answer: 3.')],6),
]:
 q=P(2,start,nth=2 if roman=='i' else 1)
 TASKS.append(T('2'+roman,'Q2('+roman+')','A',q,rows,'phys-2-1','2'+roman,SQ(4,start),total,stem=[STEM2,CONST2],fig='q2-data'))
for l,start,rows,total in [
 ('a','the heat gained by the water and the calorimeter',[R('2797 (J)',6,units=[3,3],note='Water: 0.0675 × 4180 × 9 = 2539.4 J; calorimeter: 0.0734 × 390 × 9 = 257.6 J; sum ≈2797 J. Each correct contribution earns 3.')],6),
 ('b','the heat lost by the condensed steam',[R('( mcs cw Δθcs = (0.00103)(4180)(81) =) 348.7 (J)',3,note='Condensed water cools from 100 to 19 °C, a fall of 81 °C; 1.03 g = 0.00103 kg.')],3),
 ('c','the latent heat of vaporisation of water.',[R('lv = 2.37 ×10⁶ (J kg⁻¹)',3,note='Subtract the condensed-water cooling contribution: 2797 − 348.7 ≈2448 J. Divide by 0.00103 kg to get the specific latent heat ≈2.37 ×10⁶ J/kg. The source also accepts the intermediate latent heat 2448 J for this 3-mark part.')],3),
]:
 B('2v'+l,'Q2(v)('+l+')',2,start,None,4,rows,'phys-2-1',total,sq=SQ(4,'('+l+') '+start.rstrip('.')),stem=[STEM2,P(2,'Calculate:'),CONST2],fig='q2-calculation-solution',qfig='q2-'+l+'-question')
STEM3=P(3,'You carried out an experiment to measure the speed of sound in air by measuring the','frequency and wavelength of a sound wave.')
for roman,start,end,rows,total,sq in [
 ('i','Draw a labelled diagram of the apparatus that you used.',None,[R('frequency source e.g. tuning fork / signal generator',3),R('tube, resonance, interference',3),R('detail e.g. means of altering length',3,note='Deduct 2 for no labels. Valid alternative apparatus accepted.')],9,None),
 ('ii','How did you find the frequency of the sound wave?',None,[R('(read it) from the tuning fork / signal generator // used tuning forks',6,'of known frequency',note='Partial answer: 3.')],6,None),
 ('iii','How was the wavelength of the sound wave measured?',None,[R('equation λ = 4(l + (0.3d))',9,'// λ = 2(l₂ − l₁)',units=[3,3,3],note='Either measure resonant air-column length l and tube diameter d, then use the end correction; or measure two successive resonance lengths l₁ and l₂, then λ = 2(l₂ − l₁). Complete method: 9; two measurements/resonance: 6; partial: 3.')],9,None),
 ('iv','How did you use the measurements to calculate the speed of the sound wave?',None,[R('c=f λ // c = 4f (l+(0.3d)) // c = 2f (l₂ − l₁)',12,units=[3,3,3,3],note='Use the measured frequency and wavelength in c = fλ. Full calculation: 12; substituting both measured values: 9; partial answer: 3. These are alternative complete methods, not additive answers.')],12,SQ(5,'How did you use the measurements to calculate the speed of','the sound wave?')),
 ('v','Why should you repeat the experiment?',None,[R('greater accuracy',4,note='Averaging/reducing random variation supports the improvement. Partial answer: 2.')],4,None),
]:B('3'+roman,'Q3('+roman+')',3,start,end,5,rows,'phys-2-5',total,sq=sq or SQ(5,start,end),stem=[STEM3],fig='q3-'+roman+'-solution' if roman in ('iii','iv') else None)
STEM4=P(3,'The diagram shows a circuit used to investigate the variation of current with potential','difference for a filament lamp.')
for roman,start,end,rows,total,sq in [
 ('i','Name the instrument X. What does it measure?',None,[R('voltmeter/multimeter measures voltage',4,note='Instrument and measured quantity together: 4; one correct component: 2.')],4,None),
 ('ii','Name the component Y. What does it do?',None,[R('rheostat / (variable) resistor / potential divider / potentiometer',3),R('change in one of: resistance, voltage, potential, current, power, /',3,'answer consistent with named apparatus',note='Name and function must match; a resistor limiting current is also accepted for 6.')],6,None),
 ('iii','Draw a graph, on graph paper, of the current against the potential difference.',None,[C('label one axis correctly- name/symbol/unit acceptable',3),C('plot four points correctly',3),C('plot another three points correctly',3),C('plot (smooth) curve',3,note='Use all seven given pairs. The original sample graph omits the 6 V point and its red guides are not the requested 5.5 V reading. No graph paper: maximum 9.')],12,None),
 ('iv','What does your graph tell you about the variation of current with potential','difference for a filament lamp?',[R('current rises with voltage (rise) // non linear / not proportional // non ohmic',9,units=[3,3,3],note='The current rises nonlinearly; it is not proportional to potential difference. Incomplete explanation consistent with the graph: 6; partial answer: 3.')],9,SQ(6,'What does your graph tell you about the variation of current with the','potential difference for a filament lamp?')),
 ('v','Using your graph, calculate the resistance of the lamp when the potential','difference across the lamp is 5.5 V.',[R('( R = 5.5 ÷ 2.9 = ) 1.9 ± 0.2 (Ω)',9,units=[3,3,3],note='Read I ≈2.9 A at V = 5.5 V; R = V/I ≈1.9 Ω (accepted ±0.2 Ω). Correct formula or current: 6; evidence of graph use/partial formula: 3. Do not use the sample graph’s misplaced red guides.')],9,SQ(6,'Using your graph, calculate the resistance of the lamp when the potential','difference across the lamp is 5.5 V')),
]:
 B('4'+roman,'Q4('+roman+')',3,start,end,6,rows,'phys-3-3',total,sq=sq or SQ(6,start,end),stem=[STEM4],fig='q4-apparatus' if roman in ('i','ii') else 'q4-graph-solution',qfig='q4-'+roman+'-question' if roman in ('iii','iv','v') else None,labels=[L('X',S('voltmeter/multimeter measures voltage',page=6),roman=='i'),L('Y',S('rheostat / (variable) resistor / potential divider / potentiometer',page=6),roman=='ii')] if roman in ('i','ii') else [])
for l,start,end,rows,topic,sq in [
 ('a','What is friction?',None,[R('force that resists motion // force between two bodies in contact // example',7,note='Friction opposes relative motion or its tendency between surfaces. Partial answer: 4.')],'phys-1-2',None),
 ('b','What is the relationship between G, the gravitational constant','and g, the acceleration due to gravity?',[BF(7,(83,239,148,274),'g= GM/R²',7,note='M is the attracting body’s mass; R is distance from its centre. Partial answer: 4.')],'phys-1-5',None),
 ('c','A crowbar is an example of a lever. Give another example of a lever.',None,[R('any other lever e.g. door handle, scissors, wheelbarrow, tongs etc',7,note='One correct example other than the crowbar. Partial answer: 4.')],'phys-1-2',SQ(7,'A crowbar is an example of a lever; give another example of a lever.')),
 ('d','Which one of the following terms is associated with a wave motion?','half-life interference induction doping',[pt(S('half-life interference induction doping',piece=2,psep=' '),7)],'phys-2-6',SQ(7,'Which one of the following terms is associated with wave motion?')),
 ('e','Name the three ways by which heat can travel from one place to another.',None,[R('conduction, convection, radiation',7,note='All three methods earn 7; the historical scheme gives 4 for one correct method/partial answer. This is one collective tariff, not three independent awards.')],'phys-2-1',SQ(7,'Name the three ways by which heat can travel from one place to','another.')),
 ('f','Give two uses of a concave mirror.',None,[anyn(S('headlights, makeup, shaving mirrors, etc.',piece=1,psep=', etc.'),2,1,steps=[6,1],sep=', ',open_list=True,note='First correct use: 6; second: 1. The historical scheme gives 4 for a partial answer.')],'phys-2-3',None),
 ('g','What is the colour of the earth cable in a standard 3-pin plug?',None,[R('yellow & green',7,note='Both colours are needed for full marks. Partial answer: 4.')],'phys-3-3',None),
 ('h','How does a miniature circuit breaker (MCB) improve safety in a domestic circuit?',None,[R('prevent too high current flowing // turns off current',7,note='It interrupts the circuit when current is excessive. Partial answer: 4.')],'phys-3-3',SQ(7,'How does a miniature circuit breaker (MCB) improve safety in a','domestic circuit?')),
 ('i','Give a use for an electroscope.',None,[R('test for charge, identify charge, measure potential, etc',7,note='One correct use. Partial answer: 4.')],'phys-3-1',SQ(7,'Give a use for an electroscope')),
 ('j','Give a disadvantage of a named renewable source of energy.',None,[R('biomass/ tide /sun / wind is not always there',7,note='Name a source and a disadvantage that applies to it; for example, wind output varies with wind conditions. The list gives examples, not a requirement to answer every source. Other valid source/disadvantage pairs accepted; naming a source alone: 4.')],'phys-1-4',SQ(7,'Give a disadvantage of a named renewable source of energy?')),
]:B('5'+l,'Q5('+l+')',4,start,end,7,rows,topic,7,sq=sq or SQ(7,start,end),fig={'b':'q5-gravity-solution','c':'q5-crowbar','i':'q5-electroscope'}.get(l))
U('Q6','newton','Newton’s first law',P(5,'State Newton’s first law of motion.'),[R('A body will remain at rest or moving at a constant velocity unless acted on',6,'by an (external) force',note='More precisely, a nonzero resultant external force changes the velocity. Partial answer: 3.')],'phys-1-2',SQ(8,'State Newton’s first law of motion.'),6)
CAR=P(5,'A car of mass 1400 kg was travelling with a constant speed of 15 m s⁻¹','when it struck a tree and came to a complete stop in 0.4 s.')
for roman,start,rows,total in [
 ('i','Draw a diagram of the forces acting on the car before it hit the tree.',[anyn(None,3,3,options=[S('gravity /weight'),S('friction',after='diagram to show'),S('(normal) reaction'),S('engine (force)'),S('air resistance'),S('brakes',after='air resistance')],note='Any three correctly named forces with directions, 3 each: 2 for the force and 1 for its direction. Weight acts down, normal reaction up; driving force forward and resistive forces backward.')],9),
 ('ii','Calculate the acceleration of the car during the collision.',[BF(8,(77,357,277,390),'(a= (v−u)/t = (0−15)/0.4 =−)37.5(ms⁻²)',9,units=[3,3,3],note='a = (0 − 15)/0.4 = −37.5 m s⁻² when forward is positive. The deceleration magnitude is 37.5 m s⁻². Correct formula: 6; partial method: 3.')],9),
 ('iii','Calculate the net force acting on the car during the collision.',[R('(F=1400 × 37.5 = ) 52500 (N) // answer consistent with (ii)',6,note='Magnitude 52500 N, opposite the original motion. Signed force is −52500 N for forward-positive coordinates. Correct formula or partial answer: 3; allow consistent follow-through.')],6),
 ('iv','Calculate the kinetic energy of the moving car before it struck the tree.',[R('(E = 0.5 × 1 400 × 15² =) 157500 (J))',6,units=[3,3],note='E = ½mv² = 157500 J. Correct formula: 3.')],6),
 ('v','What happened to the kinetic energy of the moving car?',[anyn(None,2,3,steps=[6,3],options=[S('converted to heat'),S('converted to sound'),S('converted to potential energy'),S('used to deform car / tree')],note='Two valid energy destinations, first 6 then 3. Partial answer: 3. Avoid counting deformation and its stored energy twice as the same destination.')],9),
]:B('6'+roman,'Q6('+roman+')',5,start,None,8,rows,'phys-1-4' if roman in ('iv','v') else 'phys-1-2' if roman!='ii' else 'phys-1-1',total,stem=[CAR],fig='q6-'+roman+'-solution' if roman in ('i','ii') else 'q6-car',qfig='q6-'+roman+'-question' if roman in ('i','ii') else None)
PASSENGER=P(5,'A back seat passenger could injure other occupants during a collision.')
U('Q6(vi)','injury','Passenger motion',P(5,'Explain, with reference to Newton’s laws of motion, how this could occur.'),[C('states or implies use of Newton’s law(s) in explanation',4,note='When the car stops, an unrestrained passenger continues moving forward through inertia and can strike another occupant. Explain using Newton’s first law; partial explanation: 2.')],'phys-1-2',SQ(8,'A back seat passenger could injure other occupants during a collision.','occur. How is this risk of injury minimised?'),4,stem=[CAR,PASSENGER],fig='q6-car')
U('Q6(vi)','belt','Reducing passenger injury',P(5,'How is this risk of injury minimised?'),[R('by wearing a seat belt.',7,note='A seat belt restrains the passenger during the stop.')],'phys-1-2',SQ(8,'A back seat passenger could injure other occupants during a collision.','occur. How is this risk of injury minimised?'),7,stem=[CAR,PASSENGER],fig='q6-car')
LIGHT=P(5,'Light rays can undergo reflection and refraction. Both of these can occur when light is','travelling from a denser medium, such as glass, to a less dense medium, such as air.')
for slug,start,end in [('reflection','reflection is the bouncing of a wave off an obstacle / mirror // correct diagram',None),('refraction','refraction is the bending of a wave when it enters a different substance //','correct diagram')]:
 U('Q7(i)',slug,slug.capitalize(),P(5,'Explain the underlined terms.'),[R(start,6,end,note='Explain the named term. A correct diagram is accepted; partial answer: 3. The scheme separately prices each definition at 6.')],'phys-2-3',SQ(9,'Explain the underlined terms.'),6,stem=[LIGHT],qfig='q7-terms-question')
FIBRE=P(5,'The photo shows an optical fibre which is used for the','transmission of data using light waves.')
for roman,start,end,rows,total,sq in [
 ('ii','Give a practical application of the reflection of light.',None,[R('mirrors / optic fibres / binoculars, etc',3)],3,None),
 ('iii','State the laws of reflection of light.',None,[anyn(None,2,3,steps=[6,3],options=[S('angle of incidence is equal to the angle of reflection'),S('incident ray, the normal, and the reflected ray are coplanar')],note='Both laws: 9; one: 6; partial answer: 3. This is a two-of-two checklist, not a choice to omit a required law.')],9,SQ(9,'State the laws of reflection of light?')),
 ('iv','Explain, with the aid of a diagram, how total internal reflection can occur.',None,[C('correct diagram and explanation',9,units=[3,3,3],note='Light travels from higher to lower refractive index with incidence above the critical angle; it is reflected back into the first medium. Complete explanation and diagram: 9; correct explanation without a diagram or the relevant single source diagram: 6; partial: 3.')],9,SQ(9,'Explain, with the aid of a diagram how total internal reflection','can occur.')),
 ('v','What is meant by the ‘critical angle’ in total internal reflection?',None,[R('the angle of incidence above which total internal reflection occurs /',6,'the angle of incidence where the angle of refraction is 90°',note='Measured in the higher-refractive-index medium. Partial answer: 3.')],6,None),
 ('vi','Draw a diagram to show how light waves travel along','an optical fibre.',[C('correct diagram to include fibre, indication of two media, multiple reflections',9,units=[3,3,3],note='Show repeated total internal reflections at the core boundary. One omission: 6; partial answer: 3.')],9,SQ(9,'Draw a diagram to show how light waves travel along an optical fibre.')),
 ('vii','Give two advantages of using optical fibres instead of','copper wires when transmitting data.',[anyn(S('cheaper, can carry more signals, faster, less power consumption, etc',piece=1,psep=', etc'),2,2,steps=[3,2],sep=', ',open_list=True,note='Two distinct advantages, first 3 then 2. “Faster” here concerns data transmission capacity, not a claim that light travels faster in glass than in vacuum.')],5,SQ(9,'Give two advantages of using optical fibres instead of copper wires when','transmitting data.')),
 ('viii','Optical fibres are also used in medicine.','Give an example of their use in medicine.',[R('endoscope / to look inside body /( keyhole) surgery , etc',3)],3,SQ(9,'Optical fibres are also used in medicine. Give an example of their use in medicine')),
]:B('7'+roman,'Q7('+roman+')',5,start,end,9,rows,'phys-2-3',total,sq=sq or SQ(9,start,end),stem=[LIGHT]+([FIBRE] if roman in ('vi','vii','viii') else []),fig={'iv':'q7-tir-solution','v':'q7-tir-solution','vi':'q7-fibre-solution','vii':'q7-fibre','viii':'q7-fibre'}.get(roman),qfig='q7-fibre-question' if roman=='vi' else None)
for roman,start,rows,total in [
 ('i','What is meant by a thermometric property?',[R('a property that changes with temperature /heat (change)',6,note='A measurable property that varies with temperature. Partial answer: 3.')],6),
 ('ii','Name two different thermometric properties.',[anyn(S('length of mercury column, colour, E, V, R , etc.',piece=1,psep=' , etc.'),2,1,steps=[5,1],sep=', ',open_list=True,note='Any two properties: first 5, second 1. Examples include liquid-column length, colour, thermocouple e.m.f. E, volume V and resistance R. Partial answer: 3.')],6),
 ('iii','Name two different thermometers.',[anyn(S('mercury, alcohol, thermocouple/thermopile, pyrometer, resistance,','constant volume gas, digital thermometer, etc.',piece=1,psep=', etc.'),2,2,sep=', ',open_list=True,note='Two different thermometer types, 2 each.')],4),
 ('iv','Describe how to calibrate a thermometer.',[R('apparatus: container of water, heat source, un-calibrated thermometer',6,'calibrated thermometer, marker',units=[3,3],note='Any three suitable apparatus pieces earn 6; one earns 3. The source does not assign 2 marks to each item.'),R('procedure: place the thermometers in water, heat to different temperatures',3),R('and mark / plot calibration curve',3,note='Compare the uncalibrated thermometer with the calibrated thermometer at several temperatures. Diagrams and valid alternative methods accepted.')],12),
 ('v','Why is there a need for a standard thermometer?',[R('because different thermometric properties give different results //',6,'for calibration, etc.',note='A standard gives a consistent temperature reference because thermometric properties respond differently. Partial answer: 3.')],6),
]:B('8a'+roman,'Q8(a)('+roman+')',6,start,None,10,rows,'phys-2-1',total,sq=SQ(10,start.rstrip('.') if roman=='iii' else start))
KETTLE=P(6,'An electric kettle is filled with 500 g of water and is initially at a temperature of 15 °C.','The kettle has a power rating of 2 kW.')
CONST8=P(6,'(specific heat capacity of water = 4180 J Kg⁻¹ K⁻¹)')
for roman,start,rows,total,sq in [
 ('i','Calculate the energy required to raise the temperature of the water to 100 °C.',[R('1.78 × 10⁵(J)',9,units=[3,3,3],note='Q = mcΔT = 0.500 × 4180 × (100 − 15) = 177650 J ≈1.78 ×10⁵ J. At least two quantities substituted correctly: 6; one: 3.')],9,SQ(10,'Calculate the energy required to raise the temperature of the water to 100 °C')),
 ('ii','How much energy is supplied by the kettle every second?',[R('2000 (J)',3,note='2 kW = 2000 J each second.')],3,None),
 ('iii','How long will it take the kettle to heat the water to 100 °C?',[R('89 (s) // answer consistent with (i) and (ii)',6,note='t = Q/P = 177650/2000 ≈88.8 s, assuming all the supplied heat warms the water. Formula/partial method: 3; allow consistent follow-through.')],6,None),
 ('iv','Name a suitable material for the handle of the kettle. Justify your answer.',[R('plastic / wood',2),R('good insulators / will not burn hand',2,note='The reason must match the chosen material’s low thermal conductivity.')],4,None),
]:B('8b'+roman,'Q8(b)('+roman+')',6,start,None,10,rows,'phys-2-1',total,sq=sq or SQ(10,start),stem=[KETTLE,CONST8],fig='q8-kettle',qfig='q8-energy-question' if roman=='i' else None)
U('Q9(a)','faraday','Faraday’s law',P(6,'State Faraday’s law of electromagnetic induction.'),[pt(S('induced emf / E',piece=1,psep=' / '),3),pt(S('is directly proportional to / ∝',piece=1,psep=' / '),3),pt(S('rate of change of magnetic flux /',piece=1,psep=' /'),3,note='Induced e.m.f. is proportional to the rate of change of magnetic flux linkage. Partial answer: 3.')],'phys-3-6',SQ(11,'State Faraday’s law of electromagnetic induction.'),9,cells='Three printed 3-mark cells. The third sits beside the separately drawn derivative fraction; all three verbal criteria are retained.')
COIL=P(6,'A coil of wire is connected to a sensitive','meter, as shown in the diagram.')
for roman,start,rows,total,sq in [
 ('i','What is observed on the meter when the magnet is moved towards the coil?',[R('needle deflected / moves',6,note='Partial answer: 3.')],6,None),
 ('ii','What is observed on the meter when the magnet is stationary in the coil?',[R('no movement of needle',3)],3,None),
 ('iii','Explain these observations.',[pt(S('emf'),3,route='emf'),pt(S('induced',after='emf'),3,route='emf'),pt(S('when change in magnetic field // needle moves',piece=1,psep=' // '),3,route='emf'),pt(S('// when current',piece=2,psep='// '),3,route='current'),pt(S('// flows / induced',piece=2,psep='// '),3,route='current'),pt(S('when change in magnetic field // needle moves',piece=2,psep=' // '),3,route='current',note='Choose one complete explanation route, 9 marks. A moving magnet changes magnetic flux through the coil and induces e.m.f./current; a stationary magnet does not.')],9,SQ(11,'Explain these observations')),
 ('iv','How would changing the speed of the magnet affect the observations?',[R('more deflection if faster / less deflection if slower',5,note='Faster motion changes flux more rapidly. Partial answer: 3.')],5,None),
]:B('9a'+roman,'Q9(a)('+roman+')',6,start,None,11,rows,'phys-3-6',total,sq=sq or SQ(11,start),stem=[COIL]+([P(6,'What is observed on the meter when the magnet is moved towards the coil?'),P(6,'What is observed on the meter when the magnet is stationary in the coil?')] if roman=='iii' else []),fig='q9-coil')
TRANS=P(6,'Transformers are used to step up or step down a.c. voltages.')
B('9bi','Q9(b)(i)',6,'What is meant by a.c.?',None,11,[R('alternating',3),R('current',3,note='An electric current that changes direction at regular intervals is also accepted for 6; partial answer: 3.')],'phys-3-6',6,stem=[TRANS])
B('9bii','Q9(b)(ii)',6,'Draw a labelled diagram showing the structure of a transformer.',None,11,[R('(primary) coil',3),R('(secondary) coil',3),R('(soft iron) core',3,note='Three correctly positioned, labelled components. Deduct 2 for no labels.')],'phys-3-6',9,stem=[TRANS],fig='q9-transformer-solution')
B('9biii','Q9(b)(iii)',6,'The input coil of a transformer has 200 turns of wire and is','What is the voltage across the output coil, when it has 600 turns?',11,[R('690 (V)',9,units=[3,3,3],note='Vs/Vp = Ns/Np, so Vs = 230 × 600/200 = 690 V. At least two correctly substituted quantities: 6; correct formula/partial method: 3.')],'phys-3-6',9,sq=SQ(11,'The input coil of a transformer has 200 turns of wire and is connected to a 230 V a.c.','supply. What is the voltage across the output coil when it has 600 turns?'),stem=[TRANS],fig='q9-voltage-solution')
RADON=P(7,'Radon is a radioactive gas which emits alpha particles. Radon gas comes into houses','through gaps in the floors. Exposure to radon gas can cause lung cancer.')
HALF=P(7,'The most stable isotope of radon has a half-life of 4 days.')
for roman,start,end,rows,total,sq in [
 ('i','What is radioactivity?',None,[R('( the spontaneous) breakup of the nucleus /atom',3),R('(with the) emission of radiation/ α / β / γ / energy',3,note='Spontaneous nuclear decay with emission of radiation. Partial answer: 3.')],6,None),
 ('ii','Name the other two types of radiation emitted by radioactive sources.',None,[anyn(S('beta / β, gamma / γ'),2,1,steps=[5,1],sep=', ',note='Both beta and gamma are required: first 5, second 1. Partial answer: 3.')],6,SQ(12,'Name the other two types of radiation emitted by radioactive sources')),
 ('iii','Describe an experiment to distinguish between the three types of radiation.',None,[anyn(None,2,3,options=[S('apparatus: radioactive source (in lead container), magnetic / electric field,',piece=[2,1],psep=['apparatus: ', ', magnetic']),S('apparatus: radioactive source (in lead container), magnetic / electric field,',piece=[2,1],psep=[', ',',']),S('photographic (plate)')],note='Two suitable apparatus components, 3 each.'),R('procedure: place the radioactive source in the electric/magnetic field',3),R('observation: note three different marks on the photographic plate',3,note='Alpha and beta deflect in opposite directions; gamma is undeflected. Valid alternative methods, including absorption experiments, are accepted.')],12,None),
 ('iv','List three properties of one of these radiations.',None,[anyn(None,3,3,options=[S('nature'),S('charge'),S('ionising'),S('range'),S('mass')],note='Choose one radiation and give any three matching properties, 3 each. Alpha: helium nucleus, +2e, strong ionisation, few cm in air, about 4 u. Beta-minus: electron, −e, moderate ionisation, few mm in aluminium, about 1/2000 u. Gamma: electromagnetic radiation, uncharged, weak ionisation, high penetration, zero rest mass. All three source rows are shown; do not mix properties of different radiations.')],9,SQ(12,'List three properties of any one of the radiations.')),
 ('v','What are isotopes?',None,[R('atoms of the same elements',3,'/ same number of protons'),R('with different mass numbers',3,'/ different number of neutrons',note='Same proton number, different neutron number. Each printed pair gives alternative phrasings for one criterion.')],6,None),
 ('vi','Why is it important to prevent radon gas entering your home?',None,[R('because it causes (lung) cancer / causes disease',5,note='The answer sought is the health risk stated in the passage. Partial answer: 3.')],5,None),
 ('vii','If no more radon gas entered your home, how long would it be','until one eight of the radon gas was left?',[R('12 (days)',6,note='One eighth is (½)³: three half-lives ×4 days =12 days. Use the rounded half-life in this question. Partial method: 3.')],6,SQ(12,'If no more radon gas entered your home, how long would it be until one','eighth of the radon gas was left?')),
 ('viii','Give two uses of radioisotopes.',None,[anyn(S('medical, industrial, agriculture, smoke detectors, energy source, etc',piece=1,psep=', etc'),2,1,steps=[5,1],sep=', ',open_list=True,note='Two distinct uses, first 5 then 1. Partial answer: 3.')],6,None),
]:B('10'+roman,'Q10('+roman+')',7,start,end,12,rows,'phys-4-4',total,sq=sq or SQ(12,start,end),stem=[RADON]+([HALF] if roman in ('v','vii') else []),fig='q10-properties-solution' if roman=='iv' else 'q10-radon')
PASSAGE=P(8,'Einstein explained the photoelectric effect','shining on the metal is increased.')
for l,start,answer,end,topic,sq in [
 ('a','Who discovered the photoelectric effect?','Hertz',None,'phys-4-2',None),
 ('b','Who explained the photoelectric effect?','Einstein',None,'phys-4-2',None),
 ('c','What happens when light shines on certain metals?','it transfers its energy to metal/ electrons // electrons are emitted',None,'phys-4-2',None),
 ('d','Why is a metal a good conductor of electricity?','electrons are only loosely bound',None,'phys-3-3',None),
 ('e','Why does your skin feel warm when light shines on it?','energy transferred from the light/radiation',None,'phys-2-1',None),
 ('f','In the photoelectric effect, what happens when the intensity of the light is increased?','number of electrons released increases.',None,'phys-4-2',SQ(13,'In the photoelectric effect, what happens when the intensity of light','is increased?')),
 ('g','How can the speed of electrons emitted in the photoelectric effect be controlled?','change the frequency of the radiation',None,'phys-4-2',SQ(13,'How can the speed of electrons emitted in the photoelectric effect','be controlled?')),
 ('h','Give one application of the photoelectric effect.','photocell, alarms, photocopiers, light meters, photodiodes, etc',None,'phys-4-2',SQ(13,'Give one application of the photoelectric effect?')),
]:B('11'+l,'Q11('+l+')',8,start,None,13,[R(answer,7,end,note=('At a fixed frequency above the threshold, higher intensity releases more electrons; it does not increase their maximum kinetic energy. Partial answer: 4.' if l=='f' else 'Change frequency: a higher frequency gives greater maximum kinetic energy above threshold. Partial answer: 4.' if l=='g' else 'Partial answer: 4.' if l!='a' else None))],topic,7,sq=sq or SQ(13,start),stem=[PASSAGE],fig='q11-passage')
U('Q12(a)','boyle','Boyle’s law',P(9,'State Boyle’s law.'),[R('(for a fixed mass of gas kept at a constant temperature) the pressure is',6,'inversely proportional to the volume // PV = k (when T and m are fixed)',note='Include fixed mass and constant temperature. Partial answer: 3.')],'phys-2-1',SQ(14,'State Boyle’s law.'),6)
# Three complete 12-mark alternatives; no mixing steps between methods.
pressure_rows=[]
for route,options in [
 ('steam',[S('apparatus: can (containing water)'),S('procedure: boil water in can'),S('seal / invert in cold water'),S('observation/conclusion: can crushes / collapses')]),
 ('pump',[S('// can (of air)',piece=2,psep='// '),S('// pump',piece=2,psep='// '),S('// air out',piece=2,psep='// '),S('observation/conclusion: can crushes / collapses')]),
 ('glass',[S('// glass of water',piece=2,psep='// '),S('// cardboard / lid',piece=2,psep='// '),S('// invert',piece=2,psep='// '),S('// lid supported',piece=2,psep='// ')]),
]:pressure_rows.append(anyn(None,4,3,options=options,route=route,note='One complete four-step method, 3 marks per step. Use matching apparatus, procedure and observation; diagrams and other valid methods accepted.'))
U('Q12(a)','atmosphere','Atmospheric pressure demonstration',P(9,'Describe an experiment to demonstrate that the atmosphere exerts a pressure.'),pressure_rows,'phys-1-5',SQ(14,'Describe an experiment to demonstrate that the atmosphere exerts a','pressure.'),12,fig='q12-pressure-solution')
TANK=P(9,'Atmospheric pressure at the top of Mount Everest is very low at 3.0 × 10⁴ Pa,','to supply oxygen.')
U('Q12(a)','volume','Released gas volume',P(9,'What volume of gas will be available at the top of Mount Everest, when','the gas is released from the tank?'),[R('(V=) 700 (litres)',10,note='At constant temperature, P₁V₁ = P₂V₂: V₂ = (4.2 ×10⁶ ×5.0)/(3.0 ×10⁴) =700 litres. At least two correctly substituted quantities: 7; correct law/partial method: 4.')],'phys-2-1',SQ(14,'What volume of gas will be available at the top of Mount Everest, when the gas is','released from the tank?'),10,stem=[TANK],qfig='q12-volume-question',fig='q12-volume-solution')
U('Q12(b)','characteristics','Musical-note characteristics',P(9,'Loudness, pitch and quality are characteristics of a musical note. Name the','physical property of a sound wave on which each characteristic depends.'),[anyn(None,3,3,steps=[6,3,3],options=[S('loudness depends on amplitude / frequency'),S('pitch depends on frequency'),S('quality depends on overtones / harmonics')],note='All three named characteristics are required. First correct association: 6; each additional: 3. Loudness is principally associated here with amplitude; the historical scheme also accepts frequency because perceived loudness varies with frequency.')],'phys-2-5',SQ(14,'Loudness, pitch and quality are characteristics of a musical note.','Name the physical property of the sound wave on which each characteristic depends.'),12)
BAT=P(9,'A bat detector allows us to hear the sounds emitted by bats. The detector is','our frequency limits of audibility.')
for roman,start,end,rows,total,sq in [
 ('i','What is meant by the frequency limits of audibility?',None,[R('are the lowest and highest frequencies which humans can hear //',6,'range of frequencies which we can hear // 20 − 20 000 Hz',note='The conventional range given here is about 20 Hz to 20 kHz; individual hearing ranges vary. Partial answer: 3.')],6,None),
 ('ii','What name is given to a sound whose frequency is greater than','our upper frequency limit of audibility?',[R('ultrasonic',4,note='“Supersonic” concerns speed and is not the correct term; the source gives 2 for a partial answer.')],4,SQ(14,'What name is given to a sound whose frequency is greater than our','upper frequency limit of audibility')),
 ('iii','A bat emitted a sound wave and detected its','Calculate the distance of the bat from the wall.',[R('3.4 (m)',6,note='The 0.02 s is a round trip: distance = vt/2 =340 ×0.02/2 =3.4 m. Correct method/partial answer: 3.')],6,SQ(14,'A bat emitted a sound wave and detected its reflection from a wall','0.02 s later. Calculate the distance of the bat from the wall.')),
]:B('12b'+roman,'Q12(b)('+roman+')',9,start,end,14,rows,'phys-2-5',total,sq=sq or SQ(14,start,end),stem=[BAT]+([P(9,'(speed of sound in air = 340 m s⁻¹)')] if roman=='iii' else []),fig='q12-bat' if roman=='iii' else None)
U('Q12(c)','current','Electric current and unit',P(10,'What is an electric current, and give its unit of measurement?'),[R('flow / movement',3),R('of charge / electrons',3),R('amp /A',3,note='Electric current is the rate of flow of charge; its SI unit is the ampere, A.')],'phys-3-3',SQ(15,'What is an electric current, and give its unit of measurement?'),9)
U('Q12(c)','effects','Effects of electric current',P(10,'State the three effects of an electric current.'),[R('magnetic, heating/lighting, chemical',4,note='The paper asks for all three effects. The historical scheme awards the full 4 for two correct effects and 2 for one; do not invent three separate tariffs.')],'phys-3-3',SQ(15,'State the three effects of an electric current.'),4)
U('Q12(c)','demonstration','Demonstrating an effect of current',P(10,'How would you demonstrate one of the effects?'),[R('apparatus; e.g. filament bulb, battery, leads',3),R('procedure; e.g. connect up circuit and pass current through the bulb',3),R('observation / conclusion; e.g. the bulb lights / gets hot',3,note='This is the heating-effect example. A valid demonstration of the magnetic or chemical effect is also accepted using the same apparatus/procedure/observation structure. Partial answer: 3.')],'phys-3-3',SQ(15,'How would you demonstrate one of these effects?'),9,stem=[P(10,'State the three effects of an electric current.')])
DRILL=P(10,'An electric screwdriver has a power rating of 120 W when connected to','its 24 V battery.')
U('Q12(c)','battery','Screwdriver current',P(10,'Calculate the current supplied by the battery when the screwdriver is turned on.'),[R('(120= I(24)) = 5 (A)',6,note='P = IV, so I =120/24 =5 A. Correct formula/partial method: 3.')],'phys-3-3',SQ(15,'Calculate the current supplied by the battery when the screwdriver is turned on.'),6,stem=[DRILL],fig='q12-screwdriver')
GOLD=P(10,'The diagram shows an arrangement used to investigate the structure of the atom.','vacuum.')
for roman,start,rows,total,sq in [
 ('i','What are alpha-particles?',[R('consist of two protons and two neutrons // helium (nucleus)',6,note='An alpha particle is a helium-4 nucleus, not a neutral helium atom. Partial answer: 3.')],6,SQ(15,'What are alpha particles?')),
 ('ii','What happened to the alpha-particles in the experiment?',[anyn(S('some deflected, some un-deviated, some reflected'),2,3,sep=', ',note='Any two observations, 3 each. Most pass straight through; some deflect and a very small fraction scatter back.')],6,SQ(15,'What happened to the alpha particles in the experiment?')),
 ('iii','What did the experiment reveal about the structure of the atom?',[R('mainly empty space // (positive) nucleus at centre',6,note='The atom is mostly empty space with a small, positively charged nucleus. Either printed conclusion is accepted for 6; partial answer: 3.')],6,SQ(15,'What did the experiment reveal about the structure of the atom?')),
 ('iv','Name the scientist who designed the experiment.',[R('Rutherford',6,note='The historical scheme names Rutherford. Partial answer: 3.')],6,SQ(15,'Name the scientist who designed the experiment?')),
 ('v','Name a suitable detector of alpha-particles.',[R('GM tube, solid state detector, cloud chamber, ionisation tube, ZnS screen,',4,'gold leaf electroscope, photographic film, etc.',note='A detector must be suitable for alpha particles; a thin entrance window is required where applicable. Partial answer: 2.')],4,None),
]:B('12d'+roman,'Q12(d)('+roman+')',10,start,None,15,rows,'phys-4-3',total,sq=sq or SQ(15,start),stem=[GOLD],fig='q12-gold')
FIGURES={
 'q1-apparatus-solution':('scheme',3,(83,290,519,444),SEC,[],'Complete apparatus criteria, alternate data-logger allocation and labelling guidance.',True),
 'q1-velocity-solution':('scheme',3,(90,525,218,556),SEC,[],'Original distance/time and displacement/time fractions.',True),
 'q2-data':('paper',2,(159,486,445,578),SEC,[],'All six recorded mass and temperature values.',False),
 'q2-calculation-solution':('scheme',4,(86,507,440,650),SEC,[],'Original water/calorimeter heat contributions, condensed-steam cooling and specific latent heat.',True),
 'q3-iii-solution':('scheme',5,(89,312,443,353),SEC,[],'Both complete wavelength methods, end correction and resonance-length difference.',True),
 'q3-iv-solution':('scheme',5,(89,484,353,518),SEC,[],'Original speed-of-sound formula and both equivalent methods.',True),
 'q4-apparatus':('paper',3,(177,293,418,389),SEC,['X','Y'],'Complete lamp circuit, rheostat, ammeter, voltmeter and supply polarity.',False),
 'q4-graph-solution':('scheme',6,(44,363,457,615),SEC,[],'Original sample I–V graph with axes. Guidance identifies its omitted 6 V point and misplaced reading guides.',True),
 'q5-gravity-solution':('scheme',7,(84,240,134,275),SEC,[],'Original gravitational-field-strength fraction and squared radius.',True),
 'q5-crowbar':('paper',4,(425,295,514,366),SEC,[],'Original crowbar illustration.',False,[(425,313,449,332),(425,355,444,366)]),
 'q5-electroscope':('paper',4,(348,578,404,645),SEC,[],'Original electroscope photograph.',False),
 'q6-car':('paper',5,(214,110,365,230),SEC,[],'Original car and tree illustration.',False),
 'q6-i-solution':('scheme',8,(228,215,425,284),SEC,[],'Original force arrows and labels around the car.',True),
 'q6-ii-solution':('scheme',8,(77,357,277,390),SEC,[],'Original signed acceleration calculation with numerator and denominator intact.',True),
 'q7-terms-question':('paper',5,(83,442,550,505),SEC,[],'Both underlined optical terms, their context and definition request.',False,[(517,484,550,505)]),
 'q7-tir-solution':('scheme',9,(89,355,443,433),SEC,[],'Original below-critical, critical and above-critical ray diagrams, angle labels and both media.',True,[(89,355,135,361)]),
 'q7-fibre-solution':('scheme',9,(77,570,444,629),SEC,[],'Original fibre diagram with both media, entering/exiting rays and repeated reflections.',True),
 'q7-fibre':('paper',5,(423,614,576,730),SEC,[],'Original optical-fibre photograph.',False),
 'q7-fibre-question':('paper',5,(83,606,576,738),SEC,[],'Full fibre context, photograph and ray-diagram task.',False,[(83,674,418,738),(397,651,417,673)]),
 'q8-kettle':('paper',6,(256,202,379,320),SEC,[],'Original electric-kettle photograph.',False),
 'q8-energy-question':('paper',6,(111,167,560,423),SEC,[],'Full 500 g, 15 °C, 2 kW context, photograph, specific heat capacity and energy request.',False,[(111,340,560,404),(533,322,560,338)]),
 'q9-coil':('paper',6,(354,501,517,579),SEC,[],'Complete magnet, both poles, coil and connected sensitive meter.',False),
 'q9-transformer-solution':('scheme',11,(83,543,322,658),SEC,[],'Original labelled primary, secondary and core diagram.',True),
 'q9-voltage-solution':('scheme',11,(104,716,371,779),SEC,[],'Original output voltage and turns-ratio fraction.',True),
 'q10-radon':('paper',7,(155,151,475,285),SEC,[],'Complete radon entry/airway illustrations and all labels.',False),
 'q10-properties-solution':('scheme',12,(76,419,454,481),SEC,[],'All five properties for alpha, beta and gamma in the original table.',True),
 'q11-passage':('paper',8,(83,101,535,416),SEC,[],'Full photoelectric passage, Hertz photograph/caption and source attribution.',False),
 'q12-pressure-solution':('scheme',14,(83,169,448,222),SEC,[],'All three complete atmosphere-pressure demonstration methods.',True),
 'q12-volume-question':('paper',9,(111,143,559,398),SEC,[],'Climber photograph, tank volume, both pressures and full gas-volume question.',False,[(530,377,559,398)]),
 'q12-volume-solution':('scheme',14,(83,333,229,362),SEC,[],'Original Boyle-law substitution and 700 litre result.',True),
 'q12-bat':('paper',9,(447,619,520,681),SEC,[],'Original bat and reflected sound illustration.',False),
 'q12-screwdriver':('paper',10,(227,119,363,263),SEC,[],'Original electric-screwdriver photograph.',False),
 'q12-gold':('paper',10,(166,504,449,594),SEC,[],'Complete gold-foil arrangement, alpha source, scattered paths and detector labels.',False),
}
for l,y0,y1 in [('a',691,704),('b',704,718),('c',718,731)]:
 masks=[(83,585,545,674),(517,676,545,734)]
 for other,o0,o1 in [('a',690,704),('b',704,718),('c',718,734)]:
  if other!=l:masks.append((125,o0,401,o1))
 FIGURES['q2-'+l+'-question']=('paper',2,(83,431,545,753),SEC,[],'Full calorimetry context, six data values, both specific heat capacities and selected calculation.',False,masks)
for roman,y0,y1 in [('iii',541,558),('iv',561,592),('v',594,626)]:
 masks=[(83,400,545,441),(517,y0,545,y1)]
 for other,o0,o1 in [('iii',540,559),('iv',560,593),('v',594,627)]:
  if other!=roman:masks.append((83,o0,545,o1))
 FIGURES['q4-'+roman+'-question']=('paper',3,(83,251,545,629),SEC,['X','Y'],'Complete lamp apparatus, seven I/V pairs and selected graph-related request.',False,masks)
for roman,y0,y1 in [('i',237,254),('ii',257,273)]:
 masks=[(517,y0,545,y1)]
 if roman=='ii':masks.append((83,236,545,254))
 FIGURES['q6-'+roman+'-question']=('paper',5,(83,73,545,y1+2),SEC,[],'Complete car mass, initial speed, collision time, illustration and selected task.',False,masks)
SELECTION_SCAN=[
 ('paper',2,'the following','Complete momentum report retained as context.'),
 ('paper',2,'the following','All six calorimetry measurements retained.'),
 ('paper',4,'the following','All ten independently priced Q5 options retained; no best-eight combinations.'),
 ('paper',4,'one of the following','One choose-one wave-term card retains all four printed options.'),
 ('paper',5,'both','Reflection/refraction context, not an optional response pool; each definition has its own published 6 marks.'),
 ('paper',6,'or','Transformer step-up/step-down description, not a selection.'),
 ('paper',9,'any two','All four 28-mark Q12 alternatives retained, with their independently priced tasks.'),
 ('paper',9,'the following','Same four Q12 alternatives; no answer-pair combinations.'),
]
ASK_EXEMPT=[]

ASK_EXEMPT=[(2,'Calculate:','Shared command retained in all three Q2(v) calculation cards; each has a separately priced target.'),(8,'such good conductors of electricity. When','Narrative inside the complete photoelectric passage, not an independent ask.')]
for t in TASKS:
 if t['key'] in ('8aiv','10iii'):t['cells']='The printed 2×3 apparatus allocation includes its parenthesised 3-mark partial alternative; count 6 for apparatus, then 3+3 for procedure and observation, not 15.'
