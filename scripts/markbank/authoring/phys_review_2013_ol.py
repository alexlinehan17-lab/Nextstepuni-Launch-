"""2013 Ordinary Physics: all 12 paper and 20 scheme pages independently read.
Retain complete experimental methods, data, passages, diagrams and marking choices.
"""
from phys_review_lib import Q,SQ,S,G,pt,anyn,allof,T,L
YEAR,LEVEL=2013,'ol'
REVIEWED_AT='2026-11-01'
LETTERED={5,7,8,11,12}
SOURCES={'paper':{'path':'examiner-reports/physics/papers/2013-ol-paper.pdf','fileid':'LC021GLP000EV.pdf','sha256':'323bea11e3f2ea2598ecd62bde828d0d17215042f19f860ece9f3d8a08b1f6c0','pages':12},'scheme':{'path':'examiner-reports/physics/schemes/2013-ol.pdf','fileid':'LC021GLP000EV.pdf','sha256':'8b7d03ed3157d70986acf9946532b71b55453917fbbc0f0530271c6b18ed8eb8','pages':20}}
PAGE_ROLES={'paper':{1:'cover',**{p:'questions' for p in range(2,12)},12:'blank'},'scheme':{1:'cover',2:'note',3:'conventions',**{p:'marking' for p in range(4,17)},17:'blank',18:'blank',19:'blank',20:'back-cover'}}
# All seven first-occurrence special-font glyphs checked against rendered source.
GLYPHS={'Symbol':{2:'×'},'SymbolMT':{32:'=',83:'π',117:'×',113:'°',16:'−',118:'∝'}}
VERIFIED_LINES=[]
QUESTION_TOTALS={**{q:40 for q in range(1,5)},**{q:56 for q in range(5,12)},12:112}
PART_TOTALS={(7,'a'):37,(7,'b'):19,(8,'a'):29,(8,'b'):27,**{(11,l):7 for l in 'abcdefgh'},**{(12,l):28 for l in 'abcd'}}
BEST_OF={5:(8,7)};GROUP_TOTALS={};CHECKSUMS={};ROUTES={}
SCAN_PAGES={'paper':range(2,12)};SELECTION_SCAN=[]
ASK_SCAN_PAGES={'paper':range(2,12)};ASK_EXEMPT=[]
P=Q;SEC='State Examinations Commission';CRIT='The scheme prints this marking criterion rather than a worked answer.'
def R(text,marks,end=None,**kw):return pt(S(text,end),marks,**kw)
def C(text,marks,end=None,**kw):return pt(S(text,end),marks,kind='criterion',note=kw.pop('note',CRIT),**kw)
def FR(page,clip,expect,marks,**kw):return G('fraction',page=page,clip=clip,expect=expect,marks=marks,**kw)
TASKS=[];FIGURES={}
def U(ref,slug,label,q,rows,topic,sq,total,**kw):
 TASKS.append(T(ref+':'+slug,ref,'A' if int(ref.split('(')[0][1:])<5 else 'B',q,rows,topic,slug,sq,total,item=(slug,label),**kw))
def B(key,ref,page,start,end,sp,rows,topic,total,**kw):
 sq=kw.pop('sq',SQ(sp,start,end));TASKS.append(T(key,ref,'A' if int(ref.split('(')[0][1:])<5 else 'B',P(page,start,end),rows,topic,key,sq,total,**kw))
STEM1=P(2,'You carried out an experiment to measure g, the acceleration due to gravity.')
rows1=[]
for route,obj,timer,detail in [('falling-ball','falling object; ball','timer; timer shown in diagram','detail;stop/start mechanism'),('pendulum','pendulum bob','stop-watch','fixed point/split cork'),('picket-fence','picket fence','photogate (and timer)','calculator/computer')]:
 rows1 += [pt(S('falling object; ball','//picket fence',piece={'falling-ball':1,'pendulum':2,'picket-fence':3}[route],psep='//'),6,route=route),anyn(None,2,3,options=[S('timer; timer shown in diagram','//photogate (and timer)',piece={'falling-ball':1,'pendulum':2,'picket-fence':3}[route],psep='//'),S('detail;stop/start mechanism //fixed point/split cork //calculator/computer',piece={'falling-ball':1,'pendulum':2,'picket-fence':3}[route],psep='//')],route=route,note='Both remaining apparatus details are required, 3 marks each. Use one complete method. Deduct 1 if no labels; other valid methods are accepted.')]
B('1i','Q1(i)',2,'Draw a labelled diagram of the apparatus you used.',None,4,rows1,'phys-1-5',12,stem=[STEM1],decision='Three complete 12-mark methods, each object 6 plus two required details at 3 each; routes never added.')
rows1m=[]
for route,i in [('falling-ball',1),('pendulum',2),('data-logging',3)]:
 rows1m.append(anyn(None,2,3,options=[S('distance','// selected v versus t /s',piece=i,psep='//'),S('time','/t',piece=i,psep='//')],route=route,note='Both matching measurements are required. For data logging the source accepts velocity against time and its gradient, or distance and time.'))
B('1ii','Q1(ii)',2,'State the measurements you took during the experiment.',None,4,rows1m,'phys-1-5',6,stem=[STEM1])
B('1iii','Q1(iii)',2,'Describe how you took these measurements.',None,4,[C('1st correct instrument',6,note='Describe the instrument and method for the first measurement in your chosen experiment.'),C('2nd correct instrument',3,note='Describe the instrument and method for the second measurement in the same experiment.')],'phys-1-5',9,stem=[STEM1,P(2,'State the measurements you took during the experiment.')])
B('1iv','Q1(iv)',2,'How did you calculate a value for g from your measurements?',None,4,[FR(4,(185,358,268,392),'g= 2s/t² /s= ½ gt²',9,glyph_order=True,route='free-fall',note='Substitute your measured distance and time. One equation error: 6; partial substitution: 3. Other valid methods fitting the scheme are accepted.'),FR(4,(305,358,347,392),'g= 4π²l/T²',9,glyph_order=True,route='pendulum',note='Substitute the pendulum length and period. The equivalent T = 2π√(l/g) is accepted. One equation error: 6; partial substitution or a T²-versus-l graph: 3.')],'phys-1-5',9,stem=[STEM1],fig='q1-g-solution',cells='The printed full route tariff is 3×3; both complete methods each earn 9, never their sum.')
B('1v','Q1(v)',2,'Give one precaution that you took to get an accurate result.',None,4,[pt(S('e.g. use the smallest time value recorded for t // swing through small angle',piece=2,psep='e.g. '),4,note='Any valid specific precaution not already credited earns 4. A general precaution such as repetition earns 2; use the precaution for your chosen method.')],'phys-1-5',4,stem=[STEM1])
STEM2=P(2,'A student carried out an experiment to measure the specific latent heat of fusion of ice.','specific latent heat of fusion of ice.”')
for roman,start,rows,total in [
 ('i','Draw a labelled diagram of the apparatus used in the experiment.',[R('calorimeter (with water)',3),R('thermometer',3,'// temperature sensor'),R('ice',3),R('other detail e.g. insulation/(electronic) balance/stirrer, etc.',3,note='No labels: deduct 1; incorrect experiment is capped at 9.')],12),
 ('ii','How did the student prepare the ice for the experiment?',[anyn(S('crushed, dried, melting ice used'),1,6,sep=', ',note='Any one preparation; it may be inferred from the diagram. A partial answer such as “in the fridge” earns 3.')],6),
 ('iii','How did the student know that the ice was at 0 °C?',[R('stand in ice-water mixture / (use) melting (ice)',3)],3),
 ('iv','How did the student find the mass of the ice?',[R('subtract',3),R('initial mass (of calorimeter and water)',3),R('from final mass (of calorimeter and water and melted ice)',3,note='A partial answer such as using weighing scales earns 3.')],9),
 ('v','Why did the student use warm water in the experiment?',[R('increase accuracy //ice melts faster // less heat loss // heat lost = heat gained',6,note='Partial answer: 3 marks.')],6),
 ('vi','What precaution did the student take when adding the ice to the water?',[R('avoid splashing//did it quickly//ensured the ice was dry//added lots of ice//stir, etc.',4,note='Partial answer such as wearing gloves: 2 marks.')],4),
]:B('2'+roman,'Q2('+roman+')',2,start,None,5,rows,'phys-2-1',total,stem=[STEM2])
STEM3=P(3,'An experiment to measure the refractive index','The student repeated the experiment a number of times.')
rows3=[]
for i,route in [(1,'block'),(2,'liquid-depth')]:
 rows3 += [pt(S('glass/plastic block','// container of liquid',piece=i,psep='//'),6,route=route),pt(S('ray box / laser / optical pins','// optical pins',piece=i,psep='//'),3,route=route),pt(S('detail; protractor // mirror','// metre stick',piece=i,psep='//',skip_marks=True),3,route=route,note='Use apparatus matching one method; other valid methods are accepted. No labels: deduct 1. Incorrect experiment: maximum 9.')]
# The middle double solidus in the detail row separates protractor/mirror
# alternatives within the block method; the final column belongs to liquid depth.
rows3[2]=pt(S('detail; protractor // mirror',piece=2,psep='detail; '),3,route='block',note='A protractor or mirror for the chosen block method. No labels: deduct 1; incorrect experiment: maximum 9.')
rows3[5]=pt(S('// metre stick',piece=2,psep='//'),3,route='liquid-depth',note='No labels: deduct 1; incorrect experiment: maximum 9.')
B('3i','Q3(i)',3,'Draw a labelled diagram of the apparatus that the student used in the experiment.',None,6,rows3,'phys-2-3',12,sq=SQ(6,'Draw a labelled diagram of the apparatus that the student used in the','experiment.'),stem=[STEM3])
rows3m=[]
for i,route in [(1,'angles'),(2,'depths')]:
 rows3m += [pt(S('angle of incidence / i','// real depth',piece=i,psep='//'),6,route=route),pt(S('angle of refraction / r','// apparent depth',piece=i,psep='//'),6,route=route)]
rows3m.append(R('critical angle',12,route='critical-angle',units=[6,6],note='Critical angle alone is a complete accepted 12-mark method. General reference to angles or height earns 6. Measurements may be inferred from the diagram.'))
B('3ii','Q3(ii)',3,'What measurements did the student take?',None,6,rows3m,'phys-2-3',12,stem=[STEM3])
B('3iii','Q3(iii)',3,'How were these measurements used to calculate the refractive index of the','substance?',6,[FR(6,(92,459,333,493),'(n=) sini/(sinr) //(n=) (real depth)/(apparent depth) // (n=) 1/(sinc)',10,note='Choose the formula matching your experiment. One equation error: 7; partial substitution: 4.')],'phys-2-3',10,stem=[STEM3],fig='q3-index-solution')
B('3iv','Q3(iv)',3,'Why did the student repeat the experiment?',None,6,[R('for increased accuracy / to get average / to draw a graph',6,note='Partial answer: 3 marks.')],'phys-2-3',6,stem=[STEM3])
STEM4=P(3,'In an experiment to investigate the variation of the resistance R of a thermistor with','temperature θ a student measured the resistance of a thermistor at different temperatures.')
for roman,start,end,rows,total in [
 ('i','Draw a labelled diagram of the apparatus used in the experiment.',None,[R('thermistor (in waterbath)',3),R('thermometer',3,'// temperature sensor'),R('ohmmeter',3,'// datalogger'),R('detail e.g. heat source, used hot water, test tube containing glycerol, etc.',3,note='No labels: deduct 1.')],12),
 ('ii','How did the student measure the resistance of the thermistor?',None,[pt(S('ohmmeter/(digital) multimeter (set to ohms)//measure V and I and hence determine R 6',piece=1,psep=' 6'),6,note='Partial answer such as “meter”: 3 marks.')],6),
 ('iii','Plot a graph on graph paper to show the relationship between resistance R of the','thermistor and the temperature θ. (Put θ on the X-axis.)',[C('label axes correctly, (name / symbol / unit acceptable)',3),C('plot three points correctly',3),C('plot another three points correctly',3,note='All seven data pairs remain available; the historical scheme awards the plotting marks in two groups of three.'),R('(smooth) curve',3,note='Without graph paper or with θ on the Y-axis, maximum 9. The historical guide curve is approximate and misses some plotted readings; use a smooth best-fit curve based on your plotted data.')],12),
 ('iv','Use the graph to estimate the temperature of the thermistor when its resistance is','500 Ω.',[R('34 °C to 37 °C // value consistent with the graph',4,note='Evidence of using the graph at R = 500 Ω: 2 marks.')],4),
 ('v','What can you tell from the graph about the relationship between the resistance of','a thermistor and its temperature?',[R('resistance goes down with increased temperature // non linear // not proportional',6,note='Partial answer: 3 marks.')],6),
]:
 sq=SQ(7,start,end)
 if roman=='iv':sq=SQ(7,'Use the graph to estimate the temperature of the thermistor when its resistance','is 500 Ω')
 if roman=='v':sq=SQ(7,'What can you tell from the graph about the relationship between the','resistance of a thermistor and its temperature?')
 B('4'+roman,'Q4('+roman+')',3,start,end,7,rows,'phys-3-3',total,sq=sq,stem=[STEM4],fig='q4-data')
for l,start,end,rows,topic in [
 ('a','Give an example of (i) a vector quantity, (ii) a scalar quantity.',None,[C('correct examples of each',7,units=[4,3],note='Give one correctly identified vector and one scalar, for 4+3. Examples for guidance: force is a vector; mass is a scalar. The scheme allows 4 for reversed examples or definitions.')],'phys-1-1'),
 ('b','The spanner shown in the diagram','the force applied by the spanner to the nut.',[R('5 (N m)',7,note='Moment = force × perpendicular distance = 50 × 0.10. Partial method: 4 marks.')],'phys-1-2'),
 ('c','Which of the following scientists','Einstein Rutherford Faraday Coulomb',[R('Rutherford',7)],'phys-4-3'),
 ('d','What is meant by the threshold of hearing?',None,[R('minimum sound (intensity) audible // quietest sound that can be heard',7,note='Partial answer: 4 marks.')],'phys-2-5'),
 ('e','How does light travel through an optical fibre?',None,[R('(by) total internal reflection stated or shown by diagram',7,note='Reflection alone: 4 marks.')],'phys-2-3'),
 ('f','Give a common use for a convex lens.',None,[R('magnification, (eye) glasses, binoculars, contact lenses, camera, etc.',7,note='Partial answer: 4 marks.')],'phys-2-3'),
 ('g','What colour is the wire that is connected to the fuse in a standard three-pin plug?',None,[R('brown (red-brown)',7,note='The historical scheme awards 4 for blue or green-yellow, but those are not the live-wire colour.')],'phys-3-3'),
 ('h','Give a common use for a capacitor.',None,[R('store charge / conducts a.c. /(radio) tuning / filtering / smoothing / timing /',7,'store energy / flash camera / phone charger, etc.',note='Partial answer such as “radio”: 4 marks.')],'phys-3-2'),
 ('i','What is the photoelectric effect?',None,[R('emission of electrons when light (radiation) is incident',7,note='Emission of electrons alone: 4 marks.')],'phys-4-2'),
 ('j','Name one method for detecting radioactive particles.',None,[R('Geiger-Muller tube, Geiger counter, solid state detector, cloud chamber,',7,'bubble chamber, GLE, photographic film, radioactive sensor, etc.',note='Partial answer: 4 marks.')],'phys-4-4'),
]:
 sq=SQ(8,start,end)
 if l=='b':sq=SQ(8,'The spanner shown in the diagram is used to turn a nut. Calculate the moment','of the force applied by the spanner to the nut.')
 if l=='c':sq=SQ(8,'Which of the following scientists is associated with the discovery of the','Einstein Rutherford Faraday Coulomb ?')
 if l=='g':sq=SQ(8,'What colour is the wire that is connected to the fuse in a standard','three-pin plug?')
 B('5'+l,'Q5('+l+')',4,start,end,8,rows,topic,7,sq=sq,fig='q5-spanner' if l=='b' else None)
for slug,label,piece,answer in [('momentum','Momentum',1,'mass (multiplied by) velocity'),('force','Force',2,'mass (multiplied by) acceleration')]:
 q=[P(5,'Define (a) momentum, (b) force.',piece=1,psep=' (a)'),P(5,'Define (a) momentum, (b) force.',piece=[piece,2],psep=[', ','(a) ' if piece==1 else '(b) '])]
 U('Q6',slug,label,q,[R(answer,6,'// mv' if piece==1 else '// ma // causes acceleration',note='Partial answer: 3 marks.')],'phys-1-2',SQ(9,'Define (a) momentum, (b) force',paired='The scheme combines both definitions in one heading, then awards 6 to each definition separately.'),6)
U('Q6','conservation','Conservation of momentum',P(5,'State the principle of conservation of momentum.'),[R('(total) momentum before (interaction) // m₁u₁ + m₂u₂',3),R('equal to (total) momentum after (interaction) // = m₁v₁ + m₂v₂',3,note='For an isolated system with no net external force; use matching words or formula on both rows.')],'phys-1-2',SQ(9,'State the principle of conservation of momentum'),6)
U('Q6','jet','Jet-engine momentum',P(5,'Explain how the principle of conservation of momentum','applies in the case of a jet engine moving an aircraft.'),[R('(backward) momentum of air equal to',3),R('(forward) momentum of aircraft',3,note='A correct diagram may earn marks; partial answer: 3.')],'phys-1-2',SQ(9,'Explain how the principle of conservation of momentum applies in the case of a','jet engine moving an aircraft.'),6,fig='q6-aircraft')
TRUCK=P(5,'A truck of mass 5000 kg','stationary car with a mass of 1000 kg. The truck and the car then move off together.')
for roman,start,end,rows,total in [
 ('i','Calculate the momentum of the truck and the car before the collision.',None,[R('50 000 (kg m s⁻¹)',6,note='The truck contributes 50,000 kg m s⁻¹ and the stationary car contributes zero. Partial method mv: 3 marks.')],6),
 ('ii','What is the momentum of the combined vehicles after the collision?',None,[R('50 000 (kg m s⁻¹) / 6000v // the same as the momentum before collision',4,note='An answer consistent with your before-collision momentum is accepted; partial answer: 2.')],4),
 ('iii','Calculate the velocity of the combined vehicles after the collision.',None,[FR(9,(90,484,197,518),'( 50000/6000 =) 8.3 (m s⁻¹)',6,note='An answer consistent with the preceding momentum is accepted; partial answer: 3. Retain the unrounded 8⅓ m s⁻¹ for later calculations.')],6),
 ('iv','What is the momentum of the truck after the collision?',None,[R('(8.3 × 5000 =) 41 500 (kg m s⁻¹)',4,note='The printed value uses rounded 8.3 m s⁻¹. The unrounded result is 41,666.7 kg m s⁻¹. An answer consistent with the preceding velocity is accepted; partial answer: 2.')],4),
 ('v','If the collision between the truck and the car takes 0.3 seconds, calculate the force','exerted by the truck on the car.',[FR(9,(90,633,319,666),'(F = (50000−41500)/0.3 // 8300/0.3 =) 27.8 ± 0.2 (kN)',6,glyph_order=True,note='Use unrounded momentum: (50,000 − 41,666.7)/0.3 ≈ 27.8 kN. The historical first substitution uses 41,500 and would give 28.3 kN, outside its printed range; the alternative 8,300/0.3 gives 27.7 kN. Correct equation alone: 3 marks.')],6),
 ('vi','When the truck hits the back of the car the driver’s airbag inflates.','risk of injury to the driver.',[R('longer time reduced force on driver’s head',6,note='Any relevant explanation is accepted; a partial reference to force earns 3.')],6),
]:
 sq=SQ(9,start,end)
 if roman=='i':sq=SQ(9,'Calculate the momentum of the truck and the car before the collision')
 if roman=='v':sq=SQ(9,'If the collision between the truck and the car takes 0.3 seconds, calculate the','force exerted by the truck on the car.')
 if roman=='vi':sq=SQ(9,'When the truck hits the back of the car the driver’s airbag inflates. The','reduces the risk of injury to the driver.?')
 B('6'+roman,'Q6('+roman+')',5,start,end,9,rows,'phys-1-2',total,sq=sq,stem=[TRUCK],fig='q6-collision')
U('Q7(a)','frequency','Frequency',P(6,'What is meant by the frequency of a wave?'),[R('number of waves per second',6,note='Number of waves alone: 3 marks.')],'phys-2-2',SQ(10,'What is meant by the frequency of a wave?'),6)
U('Q7(a)','relationship','Frequency and wavelength',P(6,'Give the relationship between the frequency and the wavelength of a wave.'),[R('c = fλ // f and λ inversely proportional',6,note='The inverse relationship applies for constant wave speed. Partial answer: 3 marks.')],'phys-2-2',SQ(10,'Give the relationship between the frequency and the wavelength of a wave.'),6)
SPEAKERS=P(6,'The diagram shows a student walking in front of two loudspeakers along the path','between A and B. A signal generator set at 500 Hz is connected to the loudspeakers.')
for roman,start,end,rows,total in [
 ('i','What will the student notice as he moves from A to B?',None,[R('loudness varies // increasing and decreasing sound',6,note='The frequency remains 500 Hz. The historical scheme allows 3 for the incorrect suggestion that the frequency varies.')],6),
 ('ii','Name this phenomenon.',None,[R('Interference',4,note='Partial answer: 2 marks.')],4),
 ('iii','Explain with the aid of a diagram how this phenomenon occurs.',None,[C('full marks may be obtained from a diagram',9,units=[6,3],note='Show constructive interference when the waves reinforce and destructive interference when they cancel. The original scheme diagrams are shown. A correct explanation alone earns 6; a partial example earns 3.')],9),
 ('iv','Why should this phenomenon be taken into account in the placing of speakers','in theatres or auditoriums?',[R('to ensure that all areas have equal loudness',6,note='Partial answer: 3 marks.')],6),
]:
 sq=SQ(10,start,end)
 if roman=='ii':sq=SQ(10,'Name this phenomenon')
 if roman=='iv':sq=SQ(10,'Why should this phenomenon be taken into account in the placing of','speakers in theatres or auditoriums?')
 B('7a'+roman,'Q7(a)('+roman+')',6,start,end,10,rows,'phys-2-6',total,sq=sq,stem=[SPEAKERS],fig='q7-speakers')
GUITAR=P(6,'The note produced by a guitar string depends on the fundamental frequency of the','loudness of a note is increased by resonance in the body of a guitar.')
B('7bi','Q7(b)(i)',6,'Explain the underlined terms.',None,10,[anyn(None,2,3,steps=[6,3],options=[S('fundamental frequency is the lowest / main frequency of an object'),S('overtones are multiples of fundamental // higher frequencies produced // harmonics')],note='Both definitions are required: first correct definition 6, second 3. Overtones lie above the fundamental; for the ideal string they are higher harmonics. Partial answer: 3.')],'phys-2-6',9,sq=SQ(10,'Explain the underlined terms'),stem=[GUITAR],qfig='q7-terms-question',fig='q7-guitar')
B('7bii','Q7(b)(ii)',6,'How can the note produced by a guitar string be changed?',None,10,[R('change tension / (effective) length / amplitude',4,note='Tension or effective length changes pitch; amplitude changes loudness. Partial answer: 2 marks.')],'phys-2-6',4,stem=[GUITAR],fig='q7-guitar')
B('7biii','Q7(b)(iii)',6,'What is resonance?',None,10,[R('transfer of energy',3),R('between two objects of similar natural frequency',3)],'phys-2-6',6,stem=[GUITAR],fig='q7-guitar')
CURRENT=P(7,'An electric current is the flow of charge in a conductor when there is a potential','difference between its ends.')
for roman,start,end,rows,total in [
 ('i','Name the unit of current.',None,[R('amp / A',6,note='Partial answer: 3 marks.')],6),
 ('ii','Give an example of a conductor.',None,[R('named metal',3,note='Any correct conductor is accepted; copper is an example of a named metal.')],3),
 ('iii','Name a source of potential difference.',None,[R('cell / battery / power supply, etc.',6,note='Partial answer: 3 marks.')],6),
 ('iv','What are the charge carriers in semiconductors?',None,[anyn(S('electrons, holes'),2,2,steps=[6,2],sep=', ',note='Both charge carriers: 8; one: 6. A partial reference to semiconductor types or doping: 4.')],8),
 ('v','What type of conductor does the I-V graph in the','diagram represent?',[R('ohmic / metallic / wire',6,note='Partial answer: 3 marks.')],6),
]:
 sq=SQ(11,start.rstrip('.'),end)
 if roman=='iii':sq=SQ(11,start)
 if roman=='v':sq=SQ(11,'What type of conductor does the I-V graph in the diagram represent?')
 B('8a'+roman,'Q8(a)('+roman+')',7,start,end,11,rows,'phys-3-3',total,sq=sq,stem=[CURRENT],fig='q8-iv' if roman=='v' else None)
MAGNET=P(7,'A magnetic field exists about a current-carrying conductor.')
B('8bi','Q8(b)(i)',7,'What is a magnetic field?',None,11,[R('region / area /space',3),R('where iron is attracted / magnetic effect is felt',3)],'phys-3-4',6,sq=SQ(11,'What is a magnetic field?.'),stem=[MAGNET])
rows8=[R('apparatus; source of current / battery / power supply',3),R('procedure; complete the circuit / turn on the current',3),R('sketch the circular field (with correct direction)',3)]
for i,route in [(1,'compass'),(2,'iron-filings')]:
 rows8.append(anyn(None,2,3,options=[S('(plotting) compass // iron filings',piece=i,psep='//'),S('observation/conclusion: compass direction changes / iron filings rearrange',piece=[2,i],psep=[': ',' / '])],route=route,note='Both apparatus and its matching observation are required. Other valid methods are accepted; a labelled diagram can earn full marks.'))
B('8bii','Q8(b)(ii)',7,'Describe an experiment to show that a long straight wire carrying a current','has a magnetic field. Sketch the magnetic field.',11,rows8,'phys-3-4',15,sq=SQ(11,'Describe an experiment to show that a long straight wire carrying a','current has a magnetic field. Sketch the magnetic field.'),stem=[MAGNET],decision='One 15-mark experiment-plus-field task: three common criteria and one matching two-criterion apparatus/observation route.')
B('8biii','Q8(b)(iii)',7,'Give an application of the magnetic field due to a current.',None,11,[R('electromagnet, speaker, motor, induction coil, transformer, etc',6,note='Partial answer: 3 marks.')],'phys-3-4',6,sq=SQ(11,'Give an application of the magnetic field due to a current'),stem=[MAGNET])
HEAT=P(7,'When heat is transferred to or from an object the temperature of the object changes.')
KETTLE=P(7,'The water in an electric kettle is heated by the element and its handle is made from an','insulating material.')
KDATA=P(7,'A kettle contains 1.3 kg of water','temperature of the water rises from 10 °C to 80 °C during a three-minute period.')
for roman,start,end,rows,total in [
 ('i','What is heat?',None,[R('(a form of) energy / mcΔθ /ml',6,note='More precisely, heat is energy transferred because of a temperature difference. The paper’s opening statement assumes no change of state. Partial answer: 3.')],6),
 ('ii','Name the three ways in which heat can be transferred.',None,[R('conduction',3),R('convection',3),R('radiation',3)],9),
 ('iii','Describe an experiment to show how heat is transferred in a liquid.',None,[R('apparatus; liquid in glass beaker, heat source, (solid) dye',3,kind='criterion',note='Any two of these three apparatus items are required for this single 3-mark criterion.'),R('procedure; put the dye in the liquid and heat',3),R('observation/conclusion; the dye can be seen rising to the top of the liquid /',3,'convection currents visible',note='A diagram may earn full marks; other valid experiments are accepted. Incorrect experiment: maximum 6; incomplete description: 3.')],9),
 ('iv','How does the method of heat transfer in a liquid affect','the positioning of the heating element in a kettle?',[R('heating element at the bottom of the kettle',6,note='Partial answer: 3 marks.')],6),
 ('v','Why is the handle of a kettle made of an insulating','material?',[R('insulator doesn’t conduct heat // safe to touch',4,note='Partial answer: 2 marks.')],4),
 ('vi','Name an insulator suitable for use in the handle of a','kettle.',[R('plastic, wood, ceramic, etc.',4,note='Any suitable insulator is accepted; partial answer: 2 marks.')],4),
]:
 sq=SQ(12,start,end)
 if roman=='iii':sq=SQ(12,start.rstrip('.'))
 if roman=='iv':sq=SQ(12,'How does the method of heat transfer in a liquid affect the positioning','of the heating element in a kettle?')
 if roman=='v':sq=SQ(12,'Why is the handle of a kettle made of an insulating material?')
 if roman=='vi':sq=SQ(12,'Name an insulator suitable for use in the handle of a kettle.')
 B('9'+roman,'Q9('+roman+')',7,start,end,12,rows,'phys-2-1',total,sq=sq,stem=[HEAT]+([KETTLE] if roman in ('iv','v','vi') else []),fig='q9-kettle' if roman in ('iv','v','vi') else None)
B('9vii','Q9(vii)',7,'the energy gained by the water',None,12,[R('(E = mcΔθ = (1.3)(4200)(80-10) = ) 3.8 ×10⁵ (J)',9,units=[3,3,3],note='The unrounded result is 382,200 J. Two correctly substituted quantities: 6; mcΔθ alone: 3.')],'phys-2-1',9,stem=[KDATA,P(7,'Calculate',after='temperature of the water rises from 10 °C to 80 °C during a three-minute period.')],fig='q9-energy-solution')
B('9viii','Q9(viii)',7,'the power rating of the kettle, assuming all of the electrical energy is used to','heat the water.',12,[R('P = 2123.3 (W) // answer consistent with (vii)',9,units=[3,3,3],note='Use E/t = 382,200/180 ≈ 2123.3 W. The printed 3.8 × 10⁵ J is rounded and gives 2111.1 W; answers consistent with the preceding energy are accepted. Correct substitution: 6; E = Pt alone: 3.')],'phys-1-4',9,sq=SQ(12,'the power rating of the kettle, assuming all of the electrical energy is used','to heat the water.'),stem=[KDATA,P(7,'Calculate',after='temperature of the water rises from 10 °C to 80 °C during a three-minute period.')],fig='q9-power-solution')
XRAY=P(8,'X-rays are used to diagnose and treat medical conditions.','photograph.')
TUBE=P(8,'In an X-ray tube a beam of electrons is used to produce X-rays.')
rows10e=[]
for i,route in [(1,'heating-metal'),(2,'thermionic-emission')]:
 rows10e += [pt(S('heating // thermionic',piece=i,psep='//'),3,route=route),pt(S('metal // emission',piece=i,psep='//'),3,route=route)]
for roman,start,end,rows,total in [
 ('i','What are X-rays?',None,[R('electromagnetic radiation // photons',3),R('high energy/frequency (low wavelength)',3)],6),
 ('ii','State a property of X-rays that makes them suitable for','medical use.',[R('highly penetrating // selective absorbance',6,note='Partial answer, such as seeing broken bones: 3 marks.')],6),
 ('iii','Give a use, other than medical, for X-rays.',None,[pt(S('airport security, X-ray telescopes/astronomy, weld/art inspection, thickness of metal, etc 6',piece=1,psep=' 6'),6,note='A general industry/agriculture answer earns 3.')],6),
 ('iv','Draw a labelled diagram showing the main parts of an X-ray tube.',None,[anyn(S('heater, cathode, anode, target, high voltage'),3,3,sep=', ',note='Any three of the five named components, at 3 each.'),R('detail e.g. correct arrangement / coolant / shielding/vacuum/extra item from previous line',3,note='An additional, unused component can count as the detail. No labels: deduct 1; partial answer: 3.')],12),
 ('v','How are electrons produced in an X-ray tube?',None,rows10e,6),
 ('vi','What is the purpose of the high voltage in an X-ray tube?',None,[R('accelerate electrons // give energy to electrons // give enough energy to',6,'produce X-rays',note='Partial answer: 3 marks.')],6),
 ('vii','What happens when the electrons hit the target in an X-ray tube?',None,[R('X-rays produced // target heats',6,note='Partial answer: 3 marks.')],6),
 ('viii','Name a suitable material for use as the target.',None,[R('tungsten',4,note='Any other named metal is a partial answer for 2.')],4),
 ('ix','Give one safety precaution required when using X-rays.',None,[pt(S('use a lead shield, protective clothing, lead glass, monitor dosage, reduce dosage, etc. 4',piece=1,psep=' 4'),4,note='One suitable precaution; partial answer: 2 marks.')],4),
]:
 sq=SQ(13,start,end)
 if roman=='ii':sq=SQ(13,'State a property of X-rays that makes them suitable for medical use.')
 if roman in ('iii','iv','ix'):sq=SQ(13,start.rstrip('.'))
 B('10'+roman,'Q10('+roman+')',8,start,end,13,rows,'phys-4-2',total,sq=sq,stem=[XRAY]+([TUBE] if roman in ('iv','v','vi','vii','viii','ix') else []),fig='q10-hand')
PASSAGE=P(9,'The National Grid - Ireland’s Transmission System','(Adapted from EIRGRID AT A GLANCE, Eirgrid information publication.)')
for letter,start,end,rows,topic in [
 ('a','What are the key components of the national grid?',None,[R('(network of high voltage) transmission stations and (high voltage) power lines',7,kind='point',note='Partial answer such as cables, low-voltage lines or transformers: 4 marks.')],'phys-3-3'),
 ('b','Why are high voltages used to transmit power over the national grid?',None,[R('to avoid power/energy losses // cheaper',7,note='Partial answer: 4 marks.')],'phys-3-3'),
 ('c','Why is the power supplied to domestic customers at lower voltages?',None,[R('safety // more suitable for home uses',7,note='Partial answer: 4 marks.')],'phys-3-3'),
 ('d','Name two renewable and two non-renewable energy sources used to generate','electricity.',[allof([(S('renewable'),S(': wind, solar, wave, hydroelectric, biomass, geothermal etc.',piece=2,psep=': ')),(S('non-renewable'),S(': coal, oil, peat, gas, nuclear etc',piece=2,psep=': '))],7,note='Give two renewable sources from the first set and two non-renewable sources from the second. All four classifications form one 7-mark answer; incomplete answer: 4. Other valid examples are accepted.')],'phys-4-6'),
 ('e','The national grid uses alternating current (a.c.) rather than direct current (d.c.). What is','the difference between them?',[R('a.c. changes direction // d.c. flows in one direction // direction // frequency',7,note='Compare the two currents: a.c. reverses direction, while d.c. flows in one direction. Partial answer: 4 marks.')],'phys-3-3'),
 ('f','Name the device used to convert high voltages to lower voltages.',None,[R('(step down) transformer',7,note='A partial answer such as voltage converter: 4 marks.')],'phys-3-6'),
 ('g','Give the principle of operation of the device named in part (f).',None,[R('electromagnetic induction // answer consistent with named device in (f)',7,note='Partial reference to the device’s use or magnetic field: 4 marks.')],'phys-3-6'),
 ('h','Name the unit of electrical energy that is used in the delivery of electricity to homes and','businesses.',[R('kilowatt-hour / kWh',7,note='Joule alone is a partial answer for 4 marks.')],'phys-1-4'),
]:
 sq=SQ(14,start,end)
 if letter=='d':sq=SQ(14,'Name two renewable and two non-renewable energy sources used to','generate electricity')
 if letter=='e':sq=SQ(14,'The national grid uses alternating current (a.c.) rather than direct','current (d.c.). What is the difference between them?')
 if letter=='f':sq=SQ(14,'Name the device used to convert high voltages to lower voltages?')
 if letter=='h':sq=SQ(14,'Name the unit of electrical energy that is used in the delivery of','electricity to homes and businesses.')
 B('11'+letter,'Q11('+letter+')',9,start,end,14,rows,topic,7,sq=sq,stem=[PASSAGE]+([P(9,'Name the device used to convert high voltages to lower voltages.')] if letter=='g' else []),fig='q11-passage')
U('Q12(a)','pressure','Pressure',P(10,'Define pressure.'),[pt(S('pressure is the force per unit area //',piece=1,psep=' //'),6,note='P = F/A is also accepted. Partial answer: 3 marks.')],'phys-1-5',SQ(15,'Part (a) Define pressure.'),6)
rows12a=[]
for route,apparatus,procedure,obs in [
 ('water-can',S('apparatus: can (containing water)','// glass of water',piece=1,psep='//'),[S('procedure: boil water in can','// cardboard / lid',piece=1,psep='//'),S('seal / invert in cold water','// invert',piece=1,psep='//')],S('observation/conclusion: can crushes / collapses','// lid supported',piece=1,psep='//')),
 ('air-can',S('apparatus: can (containing water)','// glass of water',piece=2,psep='//'),[S('procedure: boil water in can','// cardboard / lid',piece=2,psep='//'),S('seal / invert in cold water','// invert',piece=2,psep='//')],S('observation/conclusion: can crushes / collapses','// lid supported',piece=1,psep='//')),
 ('water-glass',S('apparatus: can (containing water)','// glass of water',piece=3,psep='//'),[S('procedure: boil water in can','// cardboard / lid',piece=3,psep='//'),S('seal / invert in cold water','// invert',piece=3,psep='//')],S('observation/conclusion: can crushes / collapses','// lid supported',piece=2,psep='//')),
]:
 # One procedure criterion is printed over two lines; each complete method
 # retains its apparatus, complete procedure, and observation (3+3+3).
 proc=allof([(None,x) for x in procedure],3,note='Both actions belong to one 3-mark procedure criterion.');proc['route']=route
 rows12a += [anyn(None,2,3,options=[apparatus,obs],route=route,note='Both apparatus and observation are required. Use the matching procedure; other valid methods are accepted.'),proc]
U('Q12(a)','experiment','Atmospheric-pressure experiment',P(10,'Describe an experiment to show that the atmosphere exerts pressure.'),rows12a,'phys-1-5',SQ(15,'Describe an experiment to show that the atmosphere exerts pressure.'),9,decision='Three complete 9-mark methods; each method keeps its matching apparatus, two-action procedure and observation.')
DIVER=P(10,'A diver swims upwards from a depth of 50 m to a depth','of 20 m below the surface of the water.')
U('Q12(a)','diver','Decrease in water pressure',P(10,'Calculate the decrease in pressure on the diver as she','swims upwards.'),[R('decrease in pressure due to water: = 4.9 ×10⁵ – 1.96 ×10⁵ = 2.94 ×10⁵ (Pa)',13,note='Use p = ρgh at both depths, then subtract, or use ρgΔh directly. Correct substitution for either depth earns 9; P = hρg alone earns 4.')],'phys-1-5',SQ(15,'Calculate the decrease in pressure on the diver as she swims upwards.'),13,stem=[DIVER,P(10,'(density of the water = 1000 kg m⁻³;','acceleration due to gravity, g = 9.8 m s⁻²)')],fig='q12-diver')
PRISM=P(10,'The diagram shows a beam of white light undergoing refraction and dispersion as','it passes through a prism.')
for roman,start,rows,total in [
 ('i','What is meant by dispersion?',[R('splitting/separating of light',3),R('into colours/frequencies/wavelengths',3)],6),
 ('ii','What is observed on the screen between X and Y?',[R('spectrum // different colours',6,note='Naming two colours alone earns 3 marks.')],6),
 ('iii','What information does dispersion give about the nature of white light?',[R('it consists of different colours // that it is a wave',4,note='Partial answer: 2 marks.')],4),
 ('iv','Give another method for the dispersion of light.',[R('(shine light through a) diffraction grating // (reflection from a) CD/DVD/oil',6,note='The historical scheme accepts these colour-separation examples. CD/DVD colours arise from diffraction and interference; oil-film colours arise from thin-film interference. Partial answer: 3.')],6),
 ('v','Give an everyday example of the dispersion of light.',[R('rainbow, reflection of light from a CD/DVD/oil',6,note='A rainbow is a dispersion example. The scheme also accepts CD/DVD/oil colours, although their mechanisms include diffraction or thin-film interference. Partial answer: 3.')],6),
]:B('12b'+roman,'Q12(b)('+roman+')',10,start,None,15,rows,'phys-2-4',total,sq=SQ(15,start.rstrip('.') if roman in ('iv','v') else start),stem=[PRISM],fig='q12-prism')
U('Q12(c)','law','Coulomb’s law',P(11,'State Coulomb’s law of force between electric charges.'),[pt(S('force proportional to product of charges // F α Q₁Q₂',piece=1,psep=' //'),3),pt(S('inversely proportional to square of distance between them //',piece=1,psep=' //'),3,note='Equivalent mathematical statements with correct notation are accepted.')],'phys-3-1',SQ(16,'Part (c) State Coulomb’s law of force between electric charges'),6)
ELECTROSCOPE=P(11,'The diagram shows a positively-charged electroscope.')
rows12c=[]
for i,route in [(1,'contact'),(2,'induction')]:
 rows12c += [pt(S('contact with','// brought close to negative charge',piece=i,psep='//'),3,route=route),pt(S('positive conductor','// and earthed',piece=i,psep='//'),3,route=route,note='For induction, disconnect the earth while the negative rod is still nearby, then remove the rod. This completes the charging sequence abbreviated in the scheme.' if i==2 else None)]
for roman,start,end,rows,total in [
 ('i','Give a use for an electroscope.',None,[R('detecting (measuring) charge / potential difference / capacitance',6,note='“Measures electricity” alone: 3 marks.')],6),
 ('ii','How can an electroscope be given a positive charge?',None,rows12c,6),
 ('iii','What is observed if you touch the cap of the','electroscope with your finger?',[R('leaves collapse',4,note='Partial answer: 2 marks.')],4),
 ('iv','Explain why this happens.',None,[R('(negative) charge flows from earth // earthing',6,note='A partial reference to charge: 3 marks.')],6),
]:
 sq=SQ(16,'What is observed if you touch the cap of the electroscope with your finger?') if roman=='iii' else SQ(16,start,end)
 B('12c'+roman,'Q12(c)('+roman+')',11,start,end,16,rows,'phys-3-1',total,sq=sq,stem=[ELECTROSCOPE]+([P(11,'What is observed if you touch the cap of the','electroscope with your finger?')] if roman=='iv' else []),fig='q12-electroscope')
NUCLEAR=P(11,'Nuclear fission occurs in the reactor of a nuclear power station like the one shown in the','photograph.')
for roman,start,rows,total in [
 ('i','What is nuclear fission?',[R('splitting (of large) nucleus',3),R('into (two) smaller nuclei // with release of energy/radiation // release of neutrons',3)],6),
 ('ii','Name a fuel used in a nuclear reactor.',[R('plutonium / P, (enriched) uranium / U',6,note='One fuel is required. The source prints P for plutonium; its correct chemical symbol is Pu. A named reactor part alone earns 3.')],6),
 ('iii','How can the reaction in a nuclear reactor be controlled?',[R('correct reference to (control/boron) rods // refers to absorbing neutrons // vary (U) fuel',6,note='Partial answer: 3 marks.')],6),
 ('iv','How is the energy produced in a reactor used to generate electricity?',[R('heat exchanger // produces steam // turbine',6,note='The energy heats water to steam, which drives a turbine and generator. Generator alone is a partial answer for 3.')],6),
 ('v','State a hazard of nuclear reactors.',[R('pollution /risk of nuclear contamination / fallout / difficulty of dealing',4,'with waste / health risk, dangerous, etc',note='Partial answer: 2 marks.')],4),
]:B('12d'+roman,'Q12(d)('+roman+')',11,start,None,16,rows,'phys-4-6',total,sq=SQ(16,start.rstrip('.') if roman=='ii' else start),stem=[NUCLEAR],fig='q12-nuclear')
SELECTION_SCAN=[
 ('paper',2,'the following','Complete ice-experiment report retained.'),
 ('paper',4,'the following','All ten Q5 parts retained; no best-eight combinations.'),
 ('paper',4,'the following','All four named scientists remain in one choose-one question.'),
 ('paper',6,'or','Theatres/auditoriums are alternative settings of one application task.'),
 ('paper',7,'or','Heat transferred to or from an object is context, not a choice.'),
 ('paper',9,'or','Fuel or energy sources are narrative passage context.'),
 ('paper',10,'any two','All four 28-mark Q12 alternatives retained without combination expansion.'),
 ('paper',10,'the following','Same Q12 outer selection.'),
]
FIGURES={
 'q1-g-solution':('scheme',4,(184,359.4,407,392),SEC,[],'Both complete gravity formulas, including the original square-root pendulum expression.',True),
 'q3-index-solution':('scheme',6,(92,459,334,493),SEC,[],'Three accepted refractive-index formulas with proper fraction layout.',True),
 'q4-data':('paper',3,(111,494,484,538),SEC,[],'All seven thermistor temperature and resistance pairs with units.',False),
 'q4-graph-question':('paper',3,(83,346,544,592),SEC,[],'Full thermistor context, all seven measured pairs and graph request with θ on the horizontal axis.',False,[(83,396,544,435),(517,575,544,592)]),
 'q4-graph-solution':('scheme',7,(78,346,462,582),SEC,[],'Original thermistor graph, all seven points, both labelled axes and 500-ohm reading guide; approximation note retained in guidance.',True),
 'q5-spanner':('paper',4,(228,280,435,357),SEC,[],'Spanner with the 50-newton force and 0.10-metre lever arm.',False),
 'q6-aircraft':('paper',5,(407,58,551,157),SEC,[],'Aircraft illustration accompanying the jet-engine momentum question.',False),
 'q6-collision':('paper',5,(85,209,534,292),SEC,[],'Before and after truck/car collision, initial 10 m/s speed and direction arrows.',False),
 'q6-speed-question':('paper',5,(83,163,545,370),SEC,[],'Full truck/car masses and initial speeds, before/after diagram and combined-velocity question.',False,[(83,300,545,344),(523,352,545,370)]),
 'q6-speed-solution':('scheme',9,(90,487.8,197,516.7),SEC,[],'Combined velocity as total momentum divided by total mass.',True),
 'q6-force-question':('paper',5,(83,163,545,435),SEC,[],'Full collision data and diagram with the 0.3-second interaction time and force question.',False,[(83,300,545,395),(523,418,545,435)]),
 'q6-force-solution':('scheme',9,(90,636,319,665.2),SEC,[],'Original impulse calculation and tolerance, with its rounding inconsistency explained in the card guidance.',True),
 'q7-speakers':('paper',6,(103,140,526,224),SEC,['A','B'],'Both loudspeakers, 500 Hz signal generator, connecting wires and full A-to-B walking path.',False),
 'q7-interference-question':('paper',6,(103,111,545,288),SEC,['A','B'],'Full two-speaker interference context, diagram and diagram/explanation task.',False,[(103,251,545,268),(523,231,545,248),(523,272,545,288)]),
 'q7-interference-solution':('scheme',10,(77,356,342,449),SEC,[],'Both official wave-addition diagrams showing reinforcement and cancellation.',True),
 'q7-guitar':('paper',6,(438,364,533,459),SEC,[],'Guitar illustration accompanying the note, overtone and resonance tasks.',False,[(438,364,511,374),(438,374,444,388),(523,391,533,449)]),
 'q7-terms-question':('paper',6,(112,344,545,459),SEC,[],'Full guitar context with the two underlined terms, original illustration and definition request.',False,[(112,411,436,448),(523,391,545,449)]),
 'q8-iv':('paper',7,(400,148,499,232),SEC,[],'Original straight-line current–voltage graph through the origin, both I and V axes retained.',False),
 'q9-kettle':('paper',7,(411,498,525,613),SEC,[],'Kettle photograph supplied with the heat-transfer questions.',False),
 'q9-energy-solution':('scheme',12,(90,605.8,309,621),SEC,[],'Original heat-energy formula, full numerical substitution and rounded result.',True),
 'q9-power-solution':('scheme',12,(90,682,316,725),SEC,[],'Power result, accepted follow-through and partial-method guidance.',True),
 'q10-hand':('paper',8,(415,94,511,208),SEC,[],'Original X-ray photograph of a hand.',False),
 'q10-tube-question':('paper',8,(83,70,545,277),SEC,[],'Complete X-ray context, hand photograph and labelled-tube-diagram request.',False,[(83,108,413,212),(517,108,545,212),(517,260,545,277)]),
 'q10-tube-solution':('scheme',13,(158,316,407,408),SEC,[],'Official labelled X-ray tube, cathode/filament, anode/target, cooling and high voltage.',True),
 'q11-passage':('paper',9,(83,102,545,476),SEC,[],'Complete National Grid passage, control-room photograph and caption, and Eirgrid attribution.',False),
 'q12-diver-question':('paper',10,(112,162,542,330),SEC,[],'Full diver depth change, density, gravity constant, photograph and pressure-decrease task.',False,[(383,235,410,250)]),
 'q12-diver-solution':('scheme',15,(83,300.8,486,370),SEC,[],'Both depth pressures and their difference, scientific notation, units and the published partial-credit methods.',True),
 'q12-prism':('paper',10,(196,435,432,520),SEC,['X','Y'],'Complete white-light prism and spectrum screen with endpoints X and Y.',False),
 'q12-electroscope':('paper',11,(409,123,513,226),SEC,[],'Positively charged electroscope, separated leaves and earthed case.',False),
 'q12-nuclear':('paper',11,(215,484,383,589),SEC,[],'Nuclear power-station photograph supplied with all five reactor tasks.',False),
}
for t in TASKS:
 if t['key']=='4iii':t.update(qfig='q4-graph-question',fig='q4-graph-solution')
 if t['key']=='6iii':t.update(qfig='q6-speed-question',fig='q6-speed-solution')
 if t['key']=='6v':t.update(qfig='q6-force-question',fig='q6-force-solution')
 if t['key']=='7aiii':t.update(qfig='q7-interference-question',fig='q7-interference-solution')
 if t['key']=='10iv':t.update(qfig='q10-tube-question',fig='q10-tube-solution')
 if t['key']=='Q12(a):diver':t.update(qfig='q12-diver-question',fig='q12-diver-solution')

ASK_EXEMPT=[
 (2,'ice which was at 0 °C to the warm water. I found the mass of the ice. When all','Narrative condition in the complete ice-experiment report, retained in each stem.'),
 (3,'student. When the apparatus had been set up the student made a series of measurements.','Narrative description of the experiment, retained in each stem.'),
 (7,'When heat is transferred to or from an object the temperature of the object changes.','Context statement, retained in the heat tasks with its no-phase-change assumption explained.')
]
for t in TASKS:
 if t['key']=='10iv':t['cells']='The scheme prints any three 3×3 for the five-component pool, then 3 for the detail. Total 12; the isolated menu tariff is not on the component-text baseline.'
 if t['key'] in ('9vii','9viii'):
  t['q']=[t['stem'].pop(),t['q']]

for t in TASKS:
 if t['key'] in ('4iv','4v'):
  t['stem'].append(P(3,'Plot a graph on graph paper to show the relationship between resistance R of the','thermistor and the temperature θ. (Put θ on the X-axis.)'))
 if t['key'] in ('7aii','7aiii','7aiv'):
  t['stem'].append(P(6,'What will the student notice as he moves from A to B?'))
