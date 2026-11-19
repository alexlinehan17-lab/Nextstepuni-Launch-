"""2015 Ordinary Physics: all 12 paper and 20 scheme pages independently read.
All eight first-occurrence SymbolMT glyphs visually checked. Retain every
printed option and full apparatus/data context at each published mark boundary.
"""
from phys_review_lib import Q, SQ, S, G, pt, anyn, allof, T, L
YEAR,LEVEL=2015,'ol'
REVIEWED_AT='2026-11-01'
LETTERED={5,11,12}
SOURCES={'paper':{'path':'examiner-reports/physics/papers/2015-ol-paper.pdf','fileid':'LC021GLP000EV.pdf','sha256':'203bf43f15ee3a7edbf46ee3a50f28bc731f80f181f761a529c8b972f98621bc','pages':12},'scheme':{'path':'examiner-reports/physics/schemes/2015-ol.pdf','fileid':'LC021GLP000EV.pdf','sha256':'602101c33d2c838205900e19d524d3233028f1b1c0129600ddf51321e44f8ca9','pages':20}}
PAGE_ROLES={'paper':{1:'cover',**{p:'questions' for p in range(2,11)},11:'blank',12:'blank'},'scheme':{1:'cover',2:'note',3:'conventions',**{p:'marking' for p in range(4,17)},17:'blank',18:'blank',19:'blank',20:'back-cover'}}
GLYPHS={'SymbolMT':{14:'+',16:'−',32:'=',79:'λ',85:'ρ',114:'±',117:'×',118:'∝'}}
VERIFIED_LINES=[]
QUESTION_TOTALS={**{q:40 for q in range(1,5)},**{q:56 for q in range(5,12)},12:112}
PART_TOTALS={**{(11,l):7 for l in 'abcdefgh'},**{(12,l):28 for l in 'abcd'}}
BEST_OF={5:(8,7)};GROUP_TOTALS={};CHECKSUMS={};ROUTES={}
SCAN_PAGES={'paper':range(2,11)};SELECTION_SCAN=[]
ASK_SCAN_PAGES={'paper':range(2,11)};ASK_EXEMPT=[]
SEC='State Examinations Commission';CRIT='The scheme prints this marking criterion rather than a worked answer.'
DSL='Each complete alternative method retains the stated marks; do not add the methods together.'
P=Q

def R(text,marks,end=None,**kw):return pt(S(text,end),marks,**kw)
def C(text,marks,end=None,**kw):return pt(S(text,end),marks,kind='criterion',note=kw.pop('note',CRIT),**kw)
def FR(page,clip,expect,marks,**kw):return G('fraction',page=page,clip=clip,expect=expect,marks=marks,**kw)
def partial(full,part,sel='partial answer',end=None,extra=''):
 return dict(note_sel=S(sel,end),note_lead=f'The scheme prices this “{full} or {part}”:',note=f'({part}). '+extra)
def menu(text,claim,per,end=None,sep=',',**kw):return anyn(S(text,end),claim,per,sep=sep,**kw)
TASKS=[];FIGURES={}
def A(key,ref,page,question,sp,rows,topic,total,end=None,sq=None,**kw):
 TASKS.append(T(key,ref,'A' if int(ref.split('(')[0][1:])<5 else 'B',P(page,question,end),rows,topic,key,sq or SQ(sp,question,end),total,**kw))
def U(ref,slug,label,q,rows,topic,sq,total,**kw):
 TASKS.append(T(ref+':'+slug,ref,'A' if int(ref.split('(')[0][1:])<5 else 'B',q,rows,topic,slug,sq,total,item=(slug,label),**kw))

STEM1=P(2,'A student carried out an experiment to investigate the relationship between force and','shows measurements recorded during the experiment.')
STEM2=P(2,'During an experiment to measure the specific latent heat of vaporisation of water, cold water','measurements that were recorded.')
DATA2=P(2,'Mass of calorimeter + water','92.3 g',br=True)
CONST2=P(2,'(specific latent heat of vaporisation of water = 2.3 × 10⁶ J kg⁻¹)')
STEM3=P(3,'In an experiment to measure the focal length of a concave mirror, a student placed an object','The table shows the data recorded by the student.')
STEM4=P(3,'In an experiment to find the resistivity of the material of a wire, a student took a sample of the','wire and measured its length l, diameter d, and resistance R.')
APP='Draw a labelled diagram of the apparatus used in the experiment.'
A('1i','Q1(i)',2,APP,4,[R('trolley and runway',3,'// air track and rider'),R('means of applying force correctly',3),R('timer e.g. ticker timer / photogate(s) / motion sensor',3,note_sel=S('NOTE:','accept valid alternatives, e.g. data logging methods, which fit the scheme'))],'phys-1-2',9,stem=[STEM1],fig='q1-data')
A('1ii','Q1(ii)',2,'State what measurements were taken during the experiment.',4,[menu('force // distance / velocity / acceleration // time',2,6,sep='//',steps=[6,3],note='Two measurement groups: 9; one: 6. Distance, velocity and acceleration are alternatives within the same group.')],'phys-1-2',9,stem=[STEM1],fig='q1-data')
A('1iii','Q1(iii)',2,'How were the effects of friction reduced in this experiment?',4,[R('slant/clean the runway / oil (the trolley) wheels / frictionless wheels',6,**partial(6,3,extra='May be inferred from the apparatus diagram.'))],'phys-1-2',6,stem=[STEM1])
A('1iv','Q1(iv)',2,'Plot a graph, on graph paper, of the acceleration against the force.',4,[C('labelled axes',3),C('three points plotted correctly',3),C('three more points plotted correctly',3),C('straight line with good fit',3,note_sel=S('if graph paper is not used maximum mark'),note='All seven supplied data pairs are retained. The scheme awards plotting marks for six correctly plotted points.')],'phys-1-2',12,stem=[STEM1],qfig='q1-graph-question',fig='q1-graph-solution')
A('1v','Q1(v)',2,'What does your graph tell you about the relationship between the acceleration',4,[R('(they are ) proportional /',4,'/ straight line through the origin',**partial(4,2,'partial answer e.g. inversely proportional'))],'phys-1-2',4,end='of the body and the force applied to it?',sq=SQ(4,'What does your graph tell you about the relationship between','the acceleration of the body and the force applied to it?'),stem=[STEM1,P(2,'Plot a graph, on graph paper, of the acceleration against the force.')],fig='q1-data')
TASKS.append(T('2i','Q2(i)','A',P(2,APP,nth=2),[menu('water in calorimeter, means of adding steam, thermometer,',2,6,'mass balance, insulation, steam trap',steps=[6,3],note_sel=S('incorrect experiment, maximum 6 marks','accept valid alternatives'),note='Any two apparatus items: 9; one: 6.')],'phys-2-1','2i',SQ(5,APP),9,stem=[STEM2,DATA2]))
A('2ii','Q2(ii)',2,'How was the steam dried?',5,[R('steam trap',6,**partial(6,3))],'phys-2-1',6,stem=[STEM2])
A('2iii','Q2(iii)',2,'What other measurements should be taken during this experiment?',5,[menu('mass of calorimeter, initial temperature, final temperature, mass of',2,6,'steam, mass of water',steps=[6,3],note_sel=S('rise in temperature','partial answer e.g. temperature'),note='Any two: 9; one: 6; temperature rise: 6; unspecified temperature: 3.')],'phys-2-1',9,stem=[STEM2,DATA2])
A('2iv','Q2(iv)',2,'Calculate the mass of steam used.',5,[R('(92.3 – 90.7 = ) 1.6 (g)',3)],'phys-2-1',3,stem=[STEM2,DATA2])
A('2v','Q2(v)',2,'Calculate the latent heat released when the steam condensed.',5,[R('3680 (J )',9,units=[3,3,3],note='Complete: 9; both quantities correctly substituted: 8; one quantity: 6; a relevant heat equation: 3. Use the steam mass in kilograms. The original working and partial-credit rules are shown below.')],'phys-2-1',9,stem=[STEM2,DATA2,CONST2],fig='q2-heat-solution')
A('2vi','Q2(vi)',2,'State one safety precaution required for this experiment.',5,[R('gloves / tongs / safety glasses / etc.',4,**partial(4,2,extra='May be inferred from the apparatus diagram.'))],'phys-2-1',4,stem=[STEM2])

APP3='Draw a labelled diagram showing the arrangement of the apparatus used.'
A('3i','Q3(i)',3,APP3,6,[menu('object, concave mirror, screen / search pin',2,6,steps=[6,3]),C('correct arrangement',3,note_sel=S('approximate method maximum 9 marks','accept valid alternatives'))],'phys-2-3',12,sq=SQ(6,'Draw a labelled diagram showing the arrangement of the apparatus used'),stem=[STEM3],fig='q3-data')
A('3ii','Q3(ii)',3,'How was the position of the image located?',6,[R('move screen / object / mirror /pin // sharpest image formed // there is',6,'no parallax',**partial(6,3))],'phys-2-3',6,stem=[STEM3])
A('3iii','Q3(iii)',3,'Show the distances u and v on your diagram.',6,[R('distance from the object/crosswire to the mirror shown as u',3),R('distance from the image/screen to the mirror shown as v',3,note_sel=S('partial answer e.g. reversed'),note='Reversed labels: 3 marks in total.')],'phys-2-3',6,stem=[STEM3,P(3,APP3)],fig='q3-data')
A('3iv','Q3(iv)',3,'Calculate the value of f, the focal length of the mirror.',6,[R('(average value for f =) 15 ±0.1 (cm)',12,units=[3]*4,note='Average focal length: 12; one focal length calculated: 9; reciprocal result: 8; one correct substitution for u and v: 6; correct lens equation: 3. Use all four readings to find the average; the source working is shown below.')],'phys-2-3',12,stem=[STEM3],qfig='q3-focal-question',fig='q3-focal-solution')
A('3v','Q3(v)',3,'Why did the student repeat the experiment?',6,[R('greater accuracy / more reliable result / minimise errors, to get an average etc.',4,**partial(4,2))],'phys-2-3',4,stem=[STEM3])
A('4i','Q4(i)',3,'Describe how the student found the resistance of the wire.',7,[R('ohmmeter / (digital) multimeter / measure V and I and hence determine R',6,**partial(6,3,'partial answer e.g. measure I / ammeter / meter',extra='For the voltage/current method, use R = V/I.'))],'phys-3-3',6,stem=[STEM4])
A('4ii','Q4(ii)',3,'What instrument did the student use to measure the diameter of the wire?',7,[R('micrometer // digital/vernier callipers',6,**partial(6,3,'partial answer e.g. callipers'))],'phys-3-3',6,stem=[STEM4])
A('4iii','Q4(iii)',3,'Use the data to calculate the cross-sectional area of the wire.',7,[R('A = 0.042 ± 0.001 (mm²)',12,units=[3]*4,note='Area: 12; correct substituted expression: 9; mean diameter or radius substituted: 6; any valid area equation: 3. Average the three diameters first.')],'phys-3-3',12,stem=[STEM4],qfig='q4-area-question',fig='q4-area-solution')
A('4iv','Q4(iv)',3,'Find the resistivity of the material in the wire.',7,[R('ρ = 1.56 ± 0.01 × 10⁻⁶ (Ω m)',10,units=[4,3,3],note='Result: 10; all three quantities substituted: 9; two: 7; valid equation: 4. An answer consistent with the preceding area calculation is accepted. Full original working is shown below.')],'phys-3-3',10,stem=[STEM4],qfig='q4-resistivity-question',fig='q4-resistivity-solution')
A('4v','Q4(v)',3,'State two precautions which should be taken in order to obtain an accurate result.',7,[menu('make sure that the wire is taut, measure length from inside of clips,',2,3,'measure diameter in number of places / get average diameter, etc.',open_list=True)],'phys-3-3',6,sq=SQ(7,'State two precautions which should be taken in order to obtain an','accurate result.'),stem=[STEM4])

A('5a','Q5(a)',4,'State Newton’s law of universal gravitation.',8,[R('force is proportional to product of masses and is inversely proportional to',7,'square of distance between them //',**partial(7,4,'partial answer e.g. any other of Newton’s laws'))],'phys-1-5',7,fig='q5-gravity-solution')
A('5b','Q5(b)',4,'A small stone is thrown straight up from the ground with an initial speed of 20 m s⁻¹.',8,[R('s = 20.4 (m)',7,**partial(7,4,'partial answer e.g s = ut + ½ at². / any valid equation'))],'phys-1-1',7,end='Calculate the height it has reached after two seconds.',sq=SQ(8,'A small stone is thrown straight up from the ground with an initial speed','of 20 m s⁻¹. Calculate the height it has reached after two seconds.'),stem=[P(4,'(acceleration due to gravity, g = 9.8 m s⁻²)')])
TASKS.append(T('5c','Q5(c)','B',[P(4,'From the list below, identify (i) the scientist associated with the law of refraction','of light and (ii) the scientist associated with the laws of electromagnetic induction.'),P(4,'Faraday Snell Joule Archimedes')],[anyn(None,2,4,steps=[4,3],options=[S('(i) Snell'),S('(ii) Faraday')],note='Both required matches: 7; one: 4.')],'phys-2-3','5c',SQ(8,'From the list below, identify (i) the scientist associated with the law of','electromagnetic induction.'),7,decision='All four printed scientists remain in one required matching response, not combinations.'))
A('5d','Q5(d)',4,'A glass block has a critical angle of 42°. Calculate the refractive index of the glass',8,[R('n = 1.49 ± 0.05',7,note='Complete: 7; a valid equation such as n = 1/sin c: 4. Original formula shown below.')],'phys-2-3',7,end='used in the block.',sq=SQ(8,'A glass block has a critical angle of 42°. Calculate the refractive index','of the glass used in the block.'),fig='q5-index-solution')
A('5e','Q5(e)',4,'Calculate the effective resistance of the resistors shown in this',8,[R('RT = 4 (Ω)',7,note='Result: 7; both resistances correctly substituted: 6; valid parallel-resistance equation: 4. Full source working shown below.')],'phys-3-3',7,end='circuit diagram.',sq=SQ(8,'Calculate the effective resistance of the resistors','shown in this circuit diagram.'),qfig='q5-circuit-question',fig='q5-resistance-solution')
A('5f','Q5(f)',4,'State Boyle’s law.',8,[R('(for a fixed mass of gas kept at a constant temperature) the pressure is',7,'inversely proportional to the volume // PV = k (when T and m are fixed)',**partial(7,4,'partial answer e.g. incomplete statement'))],'phys-1-2',7)
A('5g','Q5(g)',4,'State one use of the device shown on the right.',8,[R('investigating static electricity // create high voltage // stores charge',7,**partial(7,4,'partial answer e.g. Van de Graaff'))],'phys-3-1',7,fig='q5-generator')
A('5h','Q5(h)',4,'Name an electronic component that has a p-n junction.',8,[R('diode // transistor // LED etc.',7,**partial(7,4,'partial answer e.g. TV/computer/equipment containing a p-n junction/symbol'))],'phys-3-3',7)
A('5i','Q5(i)',4,'What is the purpose of a transformer in a mobile phone charger?',8,[R('changes voltage',7,**partial(7,4,'partial answer e.g. reference to voltage'))],'phys-3-6',7)
A('5j','Q5(j)',4,'What is meant by the half-life of a radioactive substance?',8,[R('time taken for the radioactivity to reduce by half //',7,**partial(7,4))],'phys-4-4',7,fig='q5-half-life-solution')

COASTER=P(5,'A roller-coaster car of mass 850 kg is released from rest at point A','of the track, as shown in the diagram.')
G6=P(5,'(acceleration due to gravity, g = 9.8 m s⁻²)')
ASSUME6=P(5,'Write down the kinetic energy of the car at point B, assuming there is no friction and','no air resistance. Calculate its velocity at point B.',piece=1,psep=' Calculate')
BRAKES=P(5,'The brakes are applied at point B and the car comes to a stop at point C.')
U('Q6','energies','Potential and kinetic energy',P(5,'Define (i) potential energy and (ii) kinetic energy.'),[anyn(None,2,6,steps=[6,3],options=[S('(i) energy due to position/ energy due to state / mgh'),S('(ii) energy due to motion / ½mv²')],note='Both definitions: 9; one: 6; partial definition of energy: 3.')],'phys-1-4',SQ(9,'Define (i) potential energy and (ii) kinetic energy.'),9)
U('Q6','conservation','Conservation of energy',P(5,'State the principle of conservation of energy.'),[R('energy is not created / destroyed (but changes form)',3)],'phys-1-4',SQ(9,'State the principle of conservation of energy.'),3)
U('Q6','application','Energy in a roller-coaster',P(5,'Explain how the principle applies to a roller-coaster.'),[R('potential energy at top of roller-coaster/ A / rest',3),R('converted into kinetic energy as speed increases / height decreases',3,note_sel=S('partial answer e.g. energy at top= energy at bottom'),note='A valid equality of top and bottom energies merits 3 marks.')],'phys-1-4',SQ(9,'Explain how the principle applies to a roller-coaster.'),6,stem=[P(5,'State the principle of conservation of energy.'),COASTER],fig='q6-track')
A('6i','Q6(i)',5,'Calculate the difference in height between point A and point B.',9,[R('75 (m)',5,**partial(5,3,'partial answer e.g. one relevant step'))],'phys-1-1',5,stem=[COASTER],fig='q6-track')
A('6ii','Q6(ii)',5,'Calculate the change in the potential energy of the car between A and B.',9,[R('624750 (J)',6,'// answer consistent with part (i)',**partial(6,3,'partial answer e.g. mgh / any valid equation'))],'phys-1-4',6,sq=SQ(9,'Calculate the change in the potential energy of the car between A and B'),stem=[COASTER,G6],fig='q6-track')
TASKS.append(T('6iii-energy','Q6(iii)','B',ASSUME6,[R('624750 ( J)',6,'// answer consistent with part (ii)',note_sel=S('correct equation e.g. ½mv²'),note='A correct kinetic-energy equation: 3.')],'phys-1-4','6iii-energy',SQ(9,'Write down the kinetic energy of the car at point B, assuming there is no','friction and no air resistance. Calculate its velocity at point B.'),6,item=('energy','Kinetic energy at B'),stem=[COASTER,G6],fig='q6-track'))
TASKS.append(T('6iii-velocity','Q6(iii)','B',P(5,'no air resistance. Calculate its velocity at point B.',piece=2,psep='. '),[R('v = 38.3 (m s⁻¹)',6,note_sel=S('v² = 1470'),note='Correct squared velocity: 3.')],'phys-1-4','6iii-velocity',SQ(9,'Write down the kinetic energy of the car at point B, assuming there is no','friction and no air resistance. Calculate its velocity at point B.'),6,item=('velocity','Velocity at B'),stem=[COASTER,ASSUME6,G6],fig='q6-track'))
A('6iv','Q6(iv)',5,'Calculate the deceleration of the car between B and C.',9,[R('deceleration = 7.7 ( m s⁻²)',9,units=[3]*3,note='Complete: 9; one correct substitution in a relevant equation: 6; a valid equation such as v² = u² + 2as: 3.')],'phys-1-1',9,stem=[COASTER,ASSUME6,BRAKES,G6],fig='q6-track')
A('6v','Q6(v)',5,'Calculate the average force required to bring the car to a stop.',9,[R('F = 6576 (N)',6,**partial(6,3,'partial answer e.g. correct equation /F = ma'))],'phys-1-2',6,stem=[COASTER,ASSUME6,BRAKES,G6],fig='q6-track')

U('Q7','resonance','Resonance',P(6,'Explain the term resonance.'),[R('transfer of energy between objects of similar natural frequency',6,**partial(6,3,'partial answer e.g. example'))],'phys-2-5',SQ(10,'Explain the term resonance.'),6)
rows=[]
for idx,route in [(1,'pendulums'),(2,'air-column')]:
 apparatus=S('apparatus: Barton’s pendulums plus detail // tuning fork and adjustable length of air',piece=idx,psep='//')
 procedure=S('procedure: hang the pendulums (vertically) from a horizontal string // hold the','vibrating tuning fork near air column',piece=idx,psep='//')
 action=S('set one of the pendulums swinging // adjust the length of the air column',piece=idx,psep='//')
 combined=anyn(None,2,3,options=[procedure,action],route=route,note='Both listed steps are required; each earns 3 marks.')
 obs=S('observation/conclusion: the pendulum of the same length also swings // at a certain','energy occurs / resonance occurs',piece=idx,psep='//')
 rows += [pt(apparatus,6,units=[3,3],route=route,note=DSL),combined,pt(obs,2,route=route,note='A correct transfer-of-energy or resonance conclusion is also accepted. Marks may be obtained from a diagram.')]
U('Q7','experiment','Demonstrating resonance',P(6,'Describe a laboratory experiment to demonstrate resonance.'),rows,'phys-2-5',SQ(10,'Describe a laboratory experiment to demonstrate resonance'),14)
WAVE=P(6,'The diagram shows a waveform.')
LABS=[L('A',S('wavelength / λ',page=10),True),L('B',S('amplitude/ height /depth',page=10),True)]
for r,q,a in [('i','What is length A called?','wavelength / λ'),('ii','What is length B called?','amplitude/ height /depth')]:
 A('7'+r,'Q7('+r+')',6,q,10,[R(a,3,note='The scheme permits 3 marks across the two label questions if both are reversed.')],'phys-2-2',3,stem=[WAVE],fig='q7-wave',labels=LABS)
A('7iii','Q7(iii)',6,'What is meant by the frequency of a wave?',10,[R('number (of waves) per second',6,**partial(6,3))],'phys-2-2',6)
A('7iv','Q7(iv)',6,'List three characteristics of a musical note.',10,[menu('loudness, quality, pitch',3,6,steps=[6,2,1],note='Three: 9; two: 8; one: 6.')],'phys-2-5',9)
A('7v','Q7(v)',6,'What is meant by the term natural frequency of an object?',10,[R('frequency at which it tends to vibrate (if free to do so) // frequency at',6,'which resonance occurs',**partial(6,3,'partial answer e.g. reference to resonance'))],'phys-2-5',6)
A('7vi','Q7(vi)',6,'The natural frequency of a stretched string is 250 Hz.',10,[R('λ = 1.36 (m )',9,units=[3]*3,note='Result: 9; both quantities correctly substituted: 8; one: 6; a valid equation such as c = fλ: 3.')],'phys-2-2',9,end='Calculate the wavelength of the sound wave produced.',stem=[P(6,'(speed of sound in air = 340 m s⁻¹)')],fig='q7-wavelength-solution')

CAP=P(6,'The diagram above shows a circuit with a bulb, switch, capacitor and a 12 V a.c. power','supply.')
U('Q8','capacitance','Capacitance',P(6,'Define capacitance. Name the unit of capacitance.',piece=1,psep='. '),[pt(S('charge per volt / V',piece=1,psep=' / '),6,**partial(6,3))],'phys-3-2',SQ(11,'Define capacitance. Name the unit of capacitance.'),6)
U('Q8','unit','Unit of capacitance',P(6,'Define capacitance. Name the unit of capacitance.',piece=2,psep='. '),[R('farad / F /microfarad',3)],'phys-3-2',SQ(11,'Define capacitance. Name the unit of capacitance.'),3)
A('8i','Q8(i)',6,'What is observed when the switch is closed?',11,[R('bulb lights // bulb goes on and off',6,**partial(6,3,'partial answer e.g. bulb goes out'))],'phys-3-2',6,stem=[CAP],fig='q8-circuit')
A('8ii','Q8(ii)',6,'What would be observed if a 12 V d.c. supply were used instead of the a.c. supply?',11,[R('bulb would not light',6,**partial(6,3,'partial answer e.g. bulb flashes'))],'phys-3-2',6,sq=SQ(11,'What would be observed if a 12 V d.c. supply were used instead of the','a.c. supply?'),stem=[CAP,P(6,'What is observed when the switch is closed?')],fig='q8-circuit')
A('8iii','Q8(iii)',6,'What do these observations tell us about capacitors?',11,[R('capacitors allow a.c. to flow but not d.c. // capacitors store charge',6,**partial(6,3))],'phys-3-2',6,stem=[CAP,P(6,'What is observed when the switch is closed?'),P(6,'What would be observed if a 12 V d.c. supply were used instead of the a.c. supply?')],fig='q8-circuit')
A('8iv','Q8(iv)',6,'The capacitor has a charge of 0.8 C when connected to the 12 V d.c. supply.',11,[R('(C =) 0.07 ± 0.005 (F)',9,units=[3]*3,note='Result within the printed tolerance: 9; both quantities correctly substituted: 8; one: 6; a valid equation such as C = Q/V: 3. Exact quotient 0.8/12 = 0.0667 F.')],'phys-3-2',9,end='Calculate its capacitance.',stem=[CAP],fig='q8-capacitance-solution')
rows=[]
for idx,route in [(1,'bulb'),(2,'leads')]:
 rows += [pt(S('Apparatus: (charged) capacitor, bulb','// capacitor, leads',piece=idx,psep='//'),6,units=[3,3],route=route,note=DSL),pt(S('procedure: connect the capacitor to the bulb','bring close together',piece=idx,psep='//'),3,route=route),R('observation/conclusion: bulb flashes/ leads spark /charged capacitor stores energy',3,route=route,note='Use the observation corresponding to the chosen apparatus.')]
U('Q8','energy','Energy stored by a capacitor',P(6,'Describe an experiment to show that energy is stored in a charged capacitor.'),rows,'phys-3-2',SQ(11,'Describe an experiment to show that energy is stored in a charged capacitor'),12)
DEVICES=P(6,'The photographs show a radio and a camera flash. Each of these devices makes use of','a property of capacitors. Name the property used in each case.')
for slug,label,answer in [('radio','Radio','radio: tuning // smoothing'),('flash','Camera flash','camera flash: storage of energy')]:
 U('Q8',slug,label,DEVICES,[R(answer,4,**partial(4,2))],'phys-3-2',SQ(11,'The photographs show a radio and a camera flash. Each of these devices makes','use of a property of capacitors. Name the property used in each case.'),4,fig='q8-devices')

KETTLE=P(7,'The diagram shows a kettle which is filled with 500 g of water','We assume all the heat is transferred to the water.')
CONST9=P(7,'(specific heat capacity of water = 4180 J kg⁻¹ K⁻¹)')
U('Q9','heat-temperature','Heat and temperature',P(7,'Distinguish between heat and temperature.'),[anyn(None,2,6,steps=[6,3],options=[S('heat is a form of energy','/ heat is measured in joules'),S('temperature is a measure of hotness / temperature is measured in °C /K')],note='Both lines: 9; one correct or definitions reversed: 6; partial: 3.')],'phys-2-1',SQ(12,'Distinguish between heat and temperature.'),9)
A('9i','Q9(i)',7,'Find the energy required to raise the temperature of the water to 100 °C.',12,[R('167 200 (J)',12,units=[3]*4,note='Result: 12; all quantities correctly substituted: 11; two: 9; one: 6; a valid equation or relevant calculation: 3.')],'phys-2-1',12,sq=SQ(12,'Find the energy required to raise the temperature of the water to 100 °C'),stem=[KETTLE,CONST9],fig='q9-heat-solution')
A('9ii','Q9(ii)',7,'What is the energy supplied by the element per second?',12,[R('800 ( J s⁻¹)',6,**partial(6,3,'partial answer e.g. any valid equation'))],'phys-1-4',6,stem=[KETTLE],fig='q9-kettle')
A('9iii','Q9(iii)',7,'How long will it take the kettle to heat the water to 100 °C?',12,[R('209 (s)',6,'// answer consistent with (ii)',note='Result: 6; correct substitution: 5; a valid equation such as t = Q/P: 3.')],'phys-2-1',6,stem=[KETTLE,CONST9],fig='q9-time-solution')
for r,q,a,m,part in [('iv','Why are handles of kettles often made of plastic?','plastic is a good insulator of heat // prevent burning',6,'partial answer'),('v','How is the heat transferred throughout the liquid in the kettle?','convection',6,'partial answer e.g. conduction // radiation'),('vi','Why is the heating element of a kettle made of metal?','good conductor (of heat / electricity)',6,'partial answer'),('vii','The heat source for a kettle is placed at the bottom. Suggest why this is the case.','hot water rises (because it is less dense than cold water) / convection',5,'partial answer')]:
 A('9'+r,'Q9('+r+')',7,q,12,[R(a,m,**partial(m,3,part))],'phys-2-1',m,sq=SQ(12,'The heat source for a kettle is placed at the bottom. Suggest why this','is the case.') if r=='vii' else SQ(12,q),stem=[KETTLE],fig='q9-kettle')

XRAY=P(7,'X-rays are produced when a beam of high speed electrons collides with a target','in an X-ray tube, as shown below.')
CRT=P(7,'A cathode ray tube, like the one used in the cathode ray oscilloscope, also uses a beam of high','speed electrons.')
U('Q10','xrays','X-rays',P(7,'What are X-rays? State two properties of X-rays.',piece=1,psep=' State'),[R('electromagnetic rays/waves (of high energy/frequency)',6,**partial(6,3))],'phys-4-2',SQ(13,'What are X-rays? State two properties of X-rays.'),6,stem=[XRAY],fig='q10-tube',labels=[L('A',S('shielding / protection',page=13),True)])
U('Q10','properties','Properties of X-rays',P(7,'What are X-rays? State two properties of X-rays.',piece=2,psep='? '),[menu('high energy, high frequency/ low wavelength, no mass, travel at speed of light,',2,3,'no charge, correct reference to penetrating power etc.',open_list=True)],'phys-4-2',SQ(13,'What are X-rays? State two properties of X-rays.'),6,stem=[XRAY],fig='q10-tube',labels=[L('A',S('shielding / protection',page=13),True)])
for r,q,a,m,part in [('i','What process occurs at the cathode?','thermionic emission // emission of electrons',6,'partial answer'),('ii','Name a substance commonly used as the target.','tungsten / any suitable metal',6,'partial answer e.g. metal'),('iii','State the function of the part marked A.','shielding / protection',6,'partial answer e.g. housing / lead'),('iv','State one use of X-rays.','specific medical/ industrial use e.g. check for broken bones, etc.',5,'partial answer e.g. property // general use such as medicine')]:
 A('10'+r,'Q10('+r+')',7,q,13,[R(a,m,**partial(m,3,part))],'phys-4-2',m,stem=[XRAY],fig='q10-tube',labels=[L('A',S('shielding / protection',page=13),True)])
A('10v','Q10(v)',7,'Draw a sketch of a cathode ray tube suitable for use in an oscilloscope.',13,[R('anode / cathode',3),R('electric deflecting plates',3),R('(fluorescent) screen',3),R('(heated) filament // vacuum tube // relevant detail',3)],'phys-4-1',12,stem=[CRT])
A('10vi','Q10(vi)',7,'Why is a vacuum needed in both the X-ray tube and the cathode ray tube?',13,[R('so the electrons do not hit gas particles / electrons are not stopped',6,**partial(6,3))],'phys-4-1',6,stem=[XRAY,CRT])
A('10vii','Q10(vii)',7,'State one use of a cathode ray oscilloscope.',13,[R('one suitable use e.g. (early) TV screens, ECG, checking for voltage/signal etc.',3)],'phys-4-1',3,stem=[CRT])

PASSAGE=P(8,'Ernest Rutherford (1871–1937, Nobel Prize 1908) was a','(Adapted from A Zeptospace Odyssey, Gian Francesco Giudice, Oxford University Press, 2010)')
for l,q,a,part in [('a','What are alpha-particles?','positively charged helium ions // two protons and two neutrons','partial answer e.g. property of alpha particles'),('b','Name a source of alpha-particles.','radium bromide, uranium, thorium, actinium, radium, etc.','partial answer e.g. other named radioactive substance'),('c','What material was used as the target in the experiment?','gold','partial answer e.g. named metal'),('d','How did Geiger and Marsden detect the alpha-particles?','flashes of light / scintillations','partial answer e.g. charge detector'),('e','What was the surprising result they observed?','some alpha-particles were bouncing back','partial answer'),('f','What force caused the deflection of the alpha-particles?','electric // magnetic','partial answer'),('h','For what invention is Hans Geiger most famous?','Geiger-Muller tube /G-M tube /Geiger counter','partial answer')]:
 row=R(a,7,**partial(7,4,part))
 if l=='f':
  row['note']+=' The force in this gold-foil experiment is electric repulsion between the positive alpha particle and the nucleus. The 2015 scheme also prints magnetic as an accepted alternative; that is retained here as a historical marking allowance.'
 A('11'+l,'Q11('+l+')',8,q,14,[row],'phys-4-3' if l in 'cdef' else 'phys-4-4',7,stem=[PASSAGE],fig='q11-passage')
# Rutherford 1911 paper excerpt reproduced by AIP establishes the central electric field:
# https://history.aip.org/exhibits/rutherford/sections/alpha-particles-atom.html
A('11g','Q11(g)',8,'Outline what the Geiger-Marsden experiment revealed about the structure of the atom.',14,[anyn(None,2,4,steps=[4,3],options=[S('(central) nucleus'),S('much smaller than atom, positive charge, with orbiting electrons etc.')],note='Both lines: 7; one: 4.')],'phys-4-3',7,sq=SQ(14,'Outline what the Geiger-Marsden experiment revealed about the','structure of the atom.'),stem=[PASSAGE],fig='q11-passage')

BIKE=P(9,'A bicycle can be steered by applying a pair of equal but','opposite forces to the handlebars, which act as a lever.')
A('12ai','Q12(a)(i)',9,'What is meant by the term lever?',15,[R('rigid body',3),R('free to rotate',3,note_sel=S('partial answer e.g. mention of fulcrum'),note='A relevant fulcrum reference: 3.')],'phys-1-2',6,stem=[BIKE],fig='q12-bike')
A('12aii','Q12(a)(ii)',9,'What is the name given to the turning effect of a force?',15,[R('moment//torque',6,**partial(6,3,'partial answer e.g. reference to perpendicular distance'))],'phys-1-2',6,stem=[BIKE],fig='q12-bike')
A('12aiii','Q12(a)(iii)',9,'What is the name given to a pair of equal but opposite forces?',15,[R('couple',6,**partial(6,3))],'phys-1-2',6,stem=[BIKE],fig='q12-bike')
U('Q12(a)','torque','Handlebar torque',P(9,'Calculate the turning effect of the force.'),[R('M = 8 (N m)',10,units=[4,2,4],note='Result: 10; both quantities correctly substituted: 9; one: 6; a valid equation such as M = Fd: 4.')],'phys-1-2',SQ(15,'Calculate the turning effect of the force.'),10,stem=[BIKE,P(9,'A cyclist’s hands are placed 40 cm apart on the ends of the handlebars.','To turn the bicycle, he applies a force of 20 N through each hand.')],fig='q12-bike')
U('Q12(b)','dispersion','Dispersion',P(9,'What is meant by dispersion of light?'),[R('separation of light into different colours/frequencies/wavelengths',6,**partial(6,3))],'phys-2-3',SQ(15,'Part (b) What is meant by dispersion of light?'),6)
U('Q12(b)','white-light','Nature of white light',P(9,'What does dispersion of light indicate about the nature of white light?'),[R('it is made of different colours/frequencies/wavelengths // spectrum',6,**partial(6,3,'partial answer e.g. wave nature'))],'phys-2-3',SQ(15,'What does dispersion of light indicate about the nature of white light?'),6)
U('Q12(b)','techniques','Laboratory dispersion techniques',P(9,'Name two laboratory techniques that can be used to cause dispersion of light.'),[R('refraction / using a (transparent/glass/perspex) prism',3),R('diffraction / using a (diffraction) grating/CD disc',3)],'phys-2-3',SQ(15,'Name two laboratory techniques that can be used to cause dispersion','of light.'),6)
U('Q12(b)','natural-example','Natural dispersion',P(9,'Describe one example of dispersion of light occurring in nature.'),[R('rainbow, diamond reflection, reflection off of oil film, etc.',4,note='A rainbow is a clear dispersion example. The scheme also lists oil films; their colours are normally explained by thin-film interference rather than dispersion.')],'phys-2-3',SQ(15,'Describe one example of dispersion of light occurring in nature.'),4)
U('Q12(b)','colours','Primary colours of light',P(9,'Explain why this is so.'),[R('all other coloured lights can be made from',6,'three primary colours',**partial(6,3,extra='A diagram may merit full marks.'))],'phys-2-4',SQ(15,'Explain why this is so.',paired='The short reprint has its alternative 6-or-3 tariff welded to the same line.'),6,stem=[P(9,'The diagram shows stage lighting similar to that found in most theatres.','Only red, green and blue lights are needed to create all the colours needed on stage.')],fig='q12-stage')
U('Q12(c)','resistance','Resistance',P(10,'Define resistance. What is the unit of resistance?',piece=1,psep='. '),[FR(16,(87,89,139,115),'R= V/I',6,note='The scheme adds “when temperature is constant”; any relevant equation is allowed 3 marks.')],'phys-3-3',SQ(16,'Part (c) Define resistance. What is the unit of resistance?',paired='The scheme reprints both asks together but assigns definition 6 and unit 3 separately.'),6,fig='q12-resistance-solution')
U('Q12(c)','unit','Unit of resistance',P(10,'Define resistance. What is the unit of resistance?',piece=2,psep='. '),[R('ohms / Ω',3)],'phys-3-3',SQ(16,'Part (c) Define resistance. What is the unit of resistance?',paired='The scheme reprints both asks together but assigns definition 6 and unit 3 separately.'),3)
U('Q12(c)','heating','Heating effect of current',P(10,'Describe an experiment to demonstrate the heating effect of an electric current.'),[R('apparatus: battery, resistance wire // toaster /(electric) heater/ hairdryer',3),R('procedure: complete the circuit / close the switch',3),R('observation/conclusion: (wire) gets hot',3)],'phys-3-3',SQ(16,'Describe an experiment to demonstrate the heating effect of an electric','current.'),9)
U('Q12(c)','carriers','Charge carriers',P(10,'State the charge carriers that are responsible for conduction in each of the following.','solutions',br=True),[anyn(None,4,6,steps=[6,2,1,1],options=[S(x,y,after=z) for x,y,z in [('gases','ions','6+2+1+1'),('semiconductors','electrons and holes','gases'),('metals','electrons','semiconductors'),('solutions','ions','metals')]],note='All four matches stay in one response: first correct 6; second 2; third and fourth 1 each.')],'phys-3-3',SQ(16,'Electrical conduction in different materials is due to the movement of charge','in each of the following.'),10,stem=[P(10,'Electrical conduction in different materials is due to the movement of charge carriers.')],decision='Four required material–carrier matches share one stepped 10-mark tariff; no four-card split.')
SOLENOID=P(10,'A solenoid (long coil of wire) is connected to a battery as shown.')
A('12di','Q12(d)(i)',10,'Copy the diagram into your answer book and draw the magnetic field in and',16,[C('correct shape of field',6,**partial(6,3))],'phys-3-4',6,end='around the solenoid.',sq=SQ(16,'Copy the diagram into your answer book and draw the magnetic field in','and around the solenoid.'),stem=[SOLENOID],qfig='q12-field-question',fig='q12-field-solution')
A('12dii','Q12(d)(ii)',10,'Explain the term electromagnetic induction.',16,[R('voltage/emf/current induced due to changing magnetic flux/field',6,**partial(6,3,'partial answer e.g. voltage created'))],'phys-3-6',6)
U('Q12(d)','generation','Generating electricity',P(10,'Describe, with the aid of a diagram, how this can be done.'),[menu('magnet, (galvano)meter, solenoid',2,4),R('magnet moves relative to solenoid',4),R('observation/conclusion:the (galvano)meter/needle deflects /emf / voltage',4,'/ electricity produced')],'phys-3-6',SQ(16,'Describe, with the aid of a diagram, how this can be done.'),16,stem=[P(10,'A magnet and a solenoid can together be used to produce electricity.')])

# Oil-film clarification checked against the publisher's own physics text:
# https://openstax.org/books/university-physics-volume-3/pages/3-4-interference-in-thin-films
for task in TASKS:
 if task['fig']=='q12-bike':task['fig']=None  # This paper has no bicycle illustration.
 if task['key']=='Q12(c):resistance':task['rows'][0]['clip']=(113,53,144,88)
FIGURES={
 'q1-data':('paper',2,(90,218,526,263),SEC,[],'All seven force and acceleration data pairs with units.',False),
 'q1-graph-question':('paper',2,(83,156,543,344),SEC,[],'Complete experiment context, seven data pairs and graph ask.',False,[(83,279,543,327),(513,327,543,344)]),
 'q1-graph-solution':('scheme',4,(90,455,441,679),SEC,[],'Official acceleration–force graph with labelled axes, scales and straight line.',True),
 'q2-heat-solution':('scheme',5,(111,511,477,571),SEC,[],'Latent-heat answer, substitution and partial-mark rules.',True),
 'q3-data':('paper',3,(162,147,424,190),SEC,[],'All four object and image distance pairs.',False),
 'q3-focal-question':('paper',3,(83,55,543,284),SEC,[],'Complete mirror experiment, four distance pairs and focal-length ask.',False,[(83,207,543,264),(512,266,543,284)]),
 'q3-focal-solution':('scheme',6,(90,462,477,556),SEC,[],'Average focal length and original reciprocal equation with partial-mark rules.',True),
 'q4-area-question':('paper',3,(83,430,543,684),SEC,[],'Full resistivity experiment, intact diameter table and area ask.',False,[(83,488,543,525),(512,667,543,684)]),
 'q4-resistivity-question':('paper',3,(83,430,543,703),SEC,[],'Full resistivity experiment and correct paper table with resistivity ask.',False,[(83,488,543,525),(83,666,543,684),(512,686,543,703)]),
 'q4-area-solution':('scheme',7,(90,377,478,441),SEC,[],'Area calculation using mean diameter, full answer and partial-mark rules.',True),
 'q4-resistivity-solution':('scheme',7,(90,479,478,579),SEC,[],'Original resistivity equation, substitution, result and consistency allowance.',True),
 'q5-gravity-solution':('scheme',8,(105,113,478,157),SEC,[],'Universal gravitation in words and its proportionality equation.',True),
 'q5-index-solution':('scheme',8,(105,339,478,384),SEC,[],'Refractive index result and critical-angle formula.',True),
 'q5-circuit-question':('paper',4,(83,434,558,505),SEC,[],'Full parallel circuit, 20 ohm and 5 ohm labels, and resistance ask.',False),
 'q5-resistance-solution':('scheme',8,(104,415,478,503),SEC,[],'Full parallel-resistance circuit, substitution and result.',True),
 'q5-generator':('paper',4,(450,522,544,693),SEC,[],'Van de Graaff generator from the paper.',False),
 'q5-half-life-solution':('scheme',8,(105,711,478,742),SEC,[],'Half-life definition and original decay-constant formula.',True),
 'q6-track':('paper',5,(37,269,565,463),SEC,[],'Full roller-coaster track with points A, B, C and dimensions 100 m, 55 m, 30 m and 95 m.',False),
 'q7-wave':('paper',6,(208,126,438,211),SEC,['A','B'],'Complete waveform and labelled lengths A and B.',False),
 'q7-wavelength-solution':('scheme',10,(83,700,478,770),SEC,[],'Wavelength calculation, fraction and partial-mark rules.',True),
 'q8-circuit':('paper',6,(200,414,398,507),SEC,[],'Entire capacitor, switch and bulb circuit with the 12 V a.c. label.',False),
 'q8-capacitance-solution':('scheme',11,(111,451,478,542),SEC,[],'Capacitance result, Q/V substitution and partial-mark rules.',True),
 'q8-devices':('paper',6,(184,649,463,745),SEC,[],'Both radio and camera-flash photographs.',False),
 'q9-kettle':('paper',7,(410,47,505,161),SEC,[],'Kettle photograph.',False),
 'q9-heat-solution':('scheme',12,(111,279,479,346),SEC,[],'Water-heating energy calculation, substitution and partial-mark rules.',True),
 'q9-time-solution':('scheme',12,(111,431,478,508),SEC,[],'Heating-time calculation, quotient and consistency allowance.',True),
 'q10-tube':('paper',7,(168,411,452,564),SEC,['A'],'Entire X-ray tube including voltage supplies, cathode, target and part A.',False),
 'q11-passage':('paper',8,(83,85,543,441),SEC,[],'Complete Rutherford passage, photograph and Gian Francesco Giudice 2010 attribution.',False),
 'q12-stage':('paper',9,(239,484,372,655),SEC,[],'Stage lighting illustration.',False),
 'q12-resistance-solution':('scheme',16,(112,53,478,101),SEC,[],'Original resistance definition as V/I and partial-mark allowance.',True),
 'q12-field-question':('paper',10,(83,459,543,598),SEC,[],'Complete battery and solenoid, context and magnetic-field drawing ask.',False,[(513,579,543,598)]),
 'q12-field-solution':('scheme',16,(111,396,478,482),SEC,[],'Official solenoid magnetic-field pattern.',True),
}
SELECTION_SCAN=[
 ('paper',2,'the following','Both steam mass measurements retained as context.'),
 ('paper',4,'the following','All ten Q5 parts retained; no best-eight combinations.'),
 ('paper',7,'both','Both tube types are required context for one explanation, not a choice.'),
 ('paper',8,'the following','Full Rutherford passage and all eight responses retained.'),
 ('paper',9,'any two','All four Q12 options retained; no combinations.'),
 ('paper',9,'the following','Same Q12 outer selection.'),
 ('paper',10,'the following','All four material–carrier matches remain one stepped ten-mark response.')]
ASK_EXEMPT=[(8,'bounced back instead of going through the film. Why should a thin metal film reflect heavy','Rhetorical question in the quoted passage, retained in full on every passage card.')]

ASK_EXEMPT.append((8,'high-speed bullets, like the alpha-particles produced by a radioactive source? Geiger and','Continuation of the rhetorical passage question; kept in every complete passage.'))
for task in TASKS:
 if task['key'] in {'3i','6iii-energy','6iii-velocity'}:
  task['cells']={'3i':'Two apparatus items 6+3 and arrangement 3. The parenthesised 6 is the alternative one-item partial score.', '6iii-energy':'Kinetic energy and velocity each have their own 6-or-3 tariff. This card retains only the energy tariff.', '6iii-velocity':'Kinetic energy and velocity each have their own 6-or-3 tariff. This card retains only the velocity tariff.'}[task['key']]

for task in TASKS:
 if task['key'] in {'2i','2iii'}:
  task['cells']='Any two items earn 6+3. Parenthesised sixes are alternative partial scores, not additional marks.'

# Final source-crop review: keep complete formula glyphs and remove adjacent
# question/tariff fragments without masking any answer or data.
for key,rect in {
 'q1-graph-solution':(90,455,449,679),
 'q3-focal-solution':(90,463,478,568),
 'q4-area-solution':(90,378,478,446),
 'q4-resistivity-solution':(90,479,481,583),
 'q5-gravity-solution':(105,113,478,157),
 'q5-resistance-solution':(104,413,478,508),
 'q5-half-life-solution':(105,704,478,742),
 'q11-passage':(83,82,543,441),
 'q12-field-solution':(266,499,400,630),
}.items():
 f=list(FIGURES[key]);f[2]=rect;FIGURES[key]=tuple(f)
for key,masks in {
 'q3-focal-solution':[(90,463,478,465)],
 'q4-area-solution':[(90,378,478,381.7)],
 'q4-resistivity-solution':[(90,479,478,482.9)],
 'q5-gravity-solution':[(105,113,478,114.5)],
 'q5-index-solution':[(440,339,478,340.5)],
 'q5-half-life-solution':[(105,704,336,708),(388,704,478,708)],
 'q6-track':[(365,269,540,330)],
 'q7-wavelength-solution':[(83,700,478,702.4)],
 'q8-capacitance-solution':[(111,451,478,453.4)],
 'q9-heat-solution':[(111,279,479,281.9)],
 'q9-time-solution':[(111,431,478,433.7)],
 'q12-resistance-solution':[(112,53,132,56.2),(144,53,478,56.2)],
}.items():
 f=list(FIGURES[key]);f=f[:7]+[masks];FIGURES[key]=tuple(f)
FIGURES.update({
 'q2-data':('paper',2,(111,525,460,558),SEC,[],'Both measured masses with labels and units.',False),
 'q2-heat-question':('paper',2,(83,430,543,713),SEC,[],'Complete steam-experiment context, measured masses, latent-heat ask and constant.',False,[(83,586,543,650),(518,650,543,666),(83,666,543,683)]),
 'q8-capacitance-question':('paper',6,(83,414,543,624),SEC,[],'Full 12 V capacitor circuit, context, 0.8 C charge and capacitance ask.',False,[(83,551,543,594),(518,608,543,624)]),
 'q9-heat-question':('paper',7,(83,47,543,324),SEC,[],'Complete kettle picture, water mass, temperatures, power, energy-transfer assumption, heat-capacity constant and energy ask.',False,[(83,47,405,74),(512,47,543,74),(512,162,543,180),(83,181,543,304)]),
 'q9-time-question':('paper',7,(83,47,543,324),SEC,[],'Complete kettle picture and data, time ask and heat-capacity constant.',False,[(83,47,405,74),(512,47,543,74),(83,162,543,200),(518,204,543,220),(83,222,543,304)]),
})
for task in TASKS:
 key=task['key']
 if key=='1iii':task['fig']='q1-data'
 if key in {'3ii','3v'}:task['fig']='q3-data'
 if key=='10vi':task.update(fig='q10-tube',labels=[L('A',S('shielding / protection',page=13),True)])
 if task['ref'].startswith('Q2('):
  if key=='2v':task['qfig']='q2-heat-question'
  else:
   task['fig']='q2-data';task['stem']=[x for x in task['stem'] if x!=DATA2]
 if key=='8iv':task['qfig']='q8-capacitance-question'
 if key=='9i':task['qfig']='q9-heat-question'
 if key=='9iii':task['qfig']='q9-time-question'
 if key=='4v':task['rows']=[anyn(None,2,3,options=[S('make sure that the wire is taut, measure length from inside of clips,','measure diameter in number of places / get average diameter, etc.',piece=i,psep=',') for i in [1,2,3]],open_list=True)]
 if key=='Q7:experiment':
  for row in task['rows']:
   if row['type']=='allof':row['note']='Both listed steps are required; each earns 3 marks.'
 # Remove only the welded printed tariff from the paper's a.c./d.c. ask.
 for sel in [task['q']] if isinstance(task['q'],dict) else task['q']:
  if sel.get('start')=='What would be observed if a 12 V d.c. supply were used instead of the a.c. supply?':sel.update(piece=1,psep=' (6)')
 for sel in task.get('stem',[]):
  if sel.get('start')=='What would be observed if a 12 V d.c. supply were used instead of the a.c. supply?':sel.update(piece=1,psep=' (6)')
# 'solutions' itself ends in 'ions'; explicitly select the following answer line.
for task in TASKS:
 if task['key']=='Q12(c):carriers':task['rows'][0]['options'][-1]['end_nth']=2
 if task['key']=='Q12(b):colours':task['rows'][0]['note']='A diagram may merit full marks.'
for key,masks in {
 'q5-gravity-solution':[(105,113,478,116)],
 'q5-index-solution':[(105,339,478,342)],
 'q5-resistance-solution':[(439,504,478,508)],
}.items():
 f=list(FIGURES[key]);f=f[:7]+[masks];FIGURES[key]=tuple(f)

f=list(FIGURES['q5-resistance-solution']);f[7]+=[(104,505,260,508)];FIGURES['q5-resistance-solution']=tuple(f)
