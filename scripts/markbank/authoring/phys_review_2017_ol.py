"""2017 Ordinary Physics — independently reviewed paper/scheme ledger.
All 12 paper and 20 scheme pages rendered and visually read, 2026-10-31.
87 first-occurrence Cambria/Symbol glyph crops inspected. All printed options
retained; required heading sets and stepped marks remain together.
"""
from phys_review_lib import Q, SQ, S, G, pt, anyn as _anyn, T
YEAR, LEVEL = 2017, 'ol'
REVIEWED_AT='2026-10-31'
LETTERED={5,11,12}
SOURCES={
 'paper':{'path':'examiner-reports/physics/papers/2017-ol-paper.pdf','fileid':'LC021GLP000EV.pdf','sha256':'918a5a2b1d6ce774cc40a9b0452a7ce11dc2ff4ffb271e1a05cb4d37a761e962','pages':12},
 'scheme':{'path':'examiner-reports/physics/schemes/2017-ol.pdf','fileid':'LC021GLP000EV.pdf','sha256':'52edb2df4e641d707e1270c131c685bbf5efd3a7258b09625cb543c505579720','pages':20}}
PAGE_ROLES={'paper':{1:'cover',**{p:'questions' for p in range(2,12)},12:'blank'},'scheme':{1:'cover',2:'note',3:'conventions',**{p:'marking' for p in range(4,17)},**{p:'blank' for p in range(17,20)},20:'back-cover'}}
GLYPHS={'SymbolMT':{14:'+',16:'−',32:'=',39:'Δ',79:'λ',83:'π',84:'θ',113:'°',117:'×',118:'∝',159:'⇒'},'Calibri,Italic':{3451:'−'},'Calibri-Bold':{3381:'−'},'Calibri':{3381:'−'}}
VERIFIED_LINES=[]
QUESTION_TOTALS={**{q:40 for q in range(1,5)},**{q:56 for q in range(5,12)},12:112}
PART_TOTALS={**{(11,l):7 for l in 'abcdefgh'},**{(12,l):28 for l in 'abcd'}}
BEST_OF={5:(8,7)}
GROUP_TOTALS={};CHECKSUMS={};ROUTES={}
SCAN_PAGES={'paper':range(2,12)};SELECTION_SCAN=[]
ASK_SCAN_PAGES={'paper':range(2,12)};ASK_EXEMPT=[]
SEC='State Examinations Commission'
CRIT='The scheme prints this marking criterion rather than a worked answer.'
DSL='The scheme’s // separates complete alternative methods; do not mix partial answers across methods.'
P=Q
def anyn(*args,**kw):
 lead=kw.pop('note_lead',None);row=_anyn(*args,**kw)
 if lead:row['note_lead']=lead
 return row
def R(text,marks,end=None,**kw):return pt(S(text,end),marks,**kw)
def C(text,marks,end=None,**kw):return pt(S(text,end),marks,kind='criterion',note=kw.pop('note',CRIT),**kw)
def FR(page,clip,expect,marks,**kw):return G('fraction',page=page,clip=clip,expect=expect,marks=marks,**kw)
def EQ(page,clip,expect,marks,**kw):return G('equation',page=page,clip=clip,expect=expect,marks=marks,**kw)
def partial(full,part,sel='partial answer',end=None,extra=''):
 return dict(note_sel=S(sel,end),note_lead=f'The scheme prices this “{full} or {part}”:',note=f'({part}). '+extra)
def menu(text,claim,per,end=None,sep='//',**kw):return anyn(S(text,end),claim,per,sep=sep,**kw)
def pieces(sel,marks,sep):return [pt(dict(sel,piece=i+1,psep=sep),m) for i,m in enumerate(marks)]
TASKS=[];FIGURES={}
def A(key,ref,page,question,sp,rows,topic,total,end=None,sq=None,**kw):
 TASKS.append(T(key,ref,'A' if int(ref.split('(')[0][1:])<5 else 'B',P(page,question,end),rows,topic,key,sq or SQ(sp,question,end),total,**kw))

STEM1=P(2,'An experiment was set up to measure g, the acceleration due to gravity.')
STEM2=P(2,'An experiment was set up to measure the specific heat capacity of a substance.')
STEM3=P(3,'An experiment was set up to measure the focal length of a concave mirror.','The table shows the data recorded during the experiment.')
STEM4=P(3,'An experiment was set up to investigate the variation of the resistance R','of a metallic conductor with its temperature θ.')
SLING=P(5,'A fairground sling-shot is shown below.','causes the pod to fall back towards the ground.')
POD=P(5,'The mass of the pod is 400 kg.','It reaches a maximum height of 50 m above its point of release.')
GRAV=P(5,'(acceleration due to gravity, g = 9.8 m s⁻²)')
PERISCOPE=P(6,'The periscope, like the one in the diagram, is an application of','the reflection of light that allows a person to see over objects.')
AMBULANCE=P(6,'The diagram shows the word AMBULANCE written so that','a driver can read it correctly in a car mirror.')
FIBRE=P(6,'Total internal reflection of light occurs in optical fibres which are used to transmit','information.')
DOPPLER=P(6,'The diagram shows a person standing near an ambulance as it','person observes a change in the frequency of the siren.')
SPRINT=P(6,'When timing a 100 m sprint, a person stands at the finishing line and starts','the stopwatch when he hears the starting gun fired at the starting line.')
WIRE=P(7,'The diagram below shows a wire placed between the poles of a U-shaped magnet.')
INDUCTION=P(7,'The wire is then disconnected from the battery and connected to a sensitive voltmeter.')
REACTOR=P(8,'Radioactive fuels are used to generate power in a nuclear fission reactor like the one','shown in the diagram.')
PASSAGE=P(9,'The Electricity Connection to your Home','(Adapted from The Safe Use of Electricity in the Home, ESB Networks)')
CAR=P(10,'A car started from rest and accelerated at 0.4 m s⁻² to reach a top speed of','to bring it to a stop in 30 s.')
FRIDGE=P(10,'A fridge lowers the temperature of 2 kg of water from 30 °C to 5 °C in 840 s.')
SHC=P(10,'(specific heat capacity of water = 4200 J kg⁻¹ K⁻¹)')
BALLOON=P(11,'A weather balloon is released to test the weather at the height of Mount Everest,','The balloon has a volume of 2 litres when it is released from sea level.')
PRESSURE=P(11,'(atmospheric pressure at sea level = 10.1 × 10⁴ Pa)')
CAPACITOR=P(11,'A capacitor can be used to store electric charge.','with a bulb, a switch and a 12 V d.c. power supply as shown.')

# Section A: the three permitted g apparatus routes retain their own rows.
_rows=[]
for route,body,timer,detail in [
 ('falling-object',S('(falling) object/ball'),S('timer: timer shown in diagram // stop-watch',piece=1,psep='//'),S('detail: stop/start mechanism // fixed point/retort stand // calculator/computer',piece=1,psep='//')),
 ('pendulum',S('// pendulum bob',piece=2,psep='//'),S('timer: timer shown in diagram // stop-watch',piece=2,psep='//'),S('detail: stop/start mechanism // fixed point/retort stand // calculator/computer',piece=2,psep='//')),
 ('picket-fence',S('// picket fence',piece=2,psep='//'),S('// photogate (and timer) 3',piece=[2,1],psep=['//',' 3']),S('detail: stop/start mechanism // fixed point/retort stand // calculator/computer',piece=3,psep='//'))]:
 _rows += [pt(body,6,route=route,note=DSL),anyn(None,2,3,route=route,options=[timer,detail],note_sel=S('NOTE: no labels, deduct 2','all valid methods are acceptable e.g. data logging methods, which fit the scheme'))]
A('1i','Q1(i)',2,'Draw a labelled diagram of the apparatus used in this experiment.',4,_rows,'phys-1-5',12,stem=[STEM1])
for key,question,sets,label in [
 ('measurements','What measurements were taken to calculate g?',[
 ('falling-object',S('distance /s'),S('time /t')),
 ('pendulum',S('// length (of pendulum)',piece=2,psep='//'),S('//period /time',piece=2,psep='//')),
 ('picket-fence',S('// selected v versus t',piece=2,psep='//'),S('// slope of graph',piece=2,psep='//'))],'Measurements'),
 ('methods','How were these measurements taken?',[
 ('falling-object',S('measure length using a metre stick'),S('measure the time using a stop watch /timer')),
 ('pendulum',S('measure length using a metre stick'),S('measure the time using a stop watch /timer')),
 ('picket-fence',S('// start program / datagate',piece=2,psep='//'),S('// drop picket fence',piece=2,psep='//'))],'Measurement methods')]:
 A('1ii-'+key,'Q1(ii)',2,question,4,[row for route,a,b in sets for row in [pt(a,3,route=route,note=DSL),pt(b,3,route=route)]],'phys-1-5',6,stem=[STEM1],item=(key,label))
A('1iii','Q1(iii)',2,'How were these measurements used to calculate g?',4,[C('substitute (for t and s) into the equation',9,units=[3,3,3],note='Use the complete equation shown for the apparatus chosen. The scheme allows 6 for one error and 3 for a partial substitution or detail.')],'phys-1-5',9,stem=[STEM1],fig='q1-equations',cells='The complete equation/substitution earns 9; the separate 6 and 3 scores are partial credit, not additional marks.')
A('1iv','Q1(iv)',2,'State two precautions which the student might have taken',4,[
 anyn(None,2,4,steps=[4,3],route='falling-object',options=[S('avoid parallax error, etc.'),S('use the smallest time value recorded for t, etc. // use accurate digital timer, etc.',piece=1,psep='//')],note='Both full precautions: 7; one full and one partial: 6; one full: 4; a partial: 2.'),
 anyn(None,2,4,steps=[4,3],route='pendulum',options=[S('// swing through small angle, etc.',piece=2,psep='//'),S('use the smallest time value recorded for t, etc. // use accurate digital timer, etc.',piece=2,psep='//')],note=DSL+' Both full: 7; one full and one partial: 6; one full: 4; a partial: 2.')],
 'phys-1-5',7,end='to get an accurate result.',sq=SQ(4,'State two precautions which the student might have taken to get an','accurate result.'),stem=[STEM1])
TASKS.append(T('2i','Q2(i)','A',P(2,'Draw a labelled diagram of the apparatus used in this experiment.',nth=2),[R('liquid / water in a calorimeter',6,end='// block of metal'),anyn(None,2,3,options=[S(x) for x in ['method of heating','stirrer','thermometer','joulemeter','insulation']],note_sel=S('incorrect experiment, maximum mark 6 + 3','NOTE: no labels, deduct 2'))],'phys-2-1','2i',SQ(5,'Draw a labelled diagram of the apparatus used in this experiment.'),12,stem=[STEM2]))
A('2ii','Q2(ii)',2,'What measurements were taken during this experiment?',5,[R('mass',3,note_sel=S('accept weight 3-1 marks')),R('temperature',3),R('detail e.g. specific mass / temperature // energy',3,note_sel=S('inconsistency between the apparatus and the measurements maximum mark 3'))],'phys-2-1',9,sq=SQ(5,'What measurements were taken during the experiment.'),stem=[STEM2])
A('2iii','Q2(iii)',2,'How was the mass of the substance determined?',5,[R('mass of calorimeter and water - mass of calorimeter //',6,end='(using an electronic) balance plus detail e.g. tare',**partial(6,3,'partial answer e.g. weigh it, by subtraction'))],'phys-2-1',6,stem=[STEM2])
A('2iv','Q2(iv)',2,'How was the specific heat capacity of the substance determined?',5,[C('any formula consistent with method e.g.',9,units=[3,3,3],note='Either complete formula shown: 9; one error: 6; one part or an attempted word version: 3.')],'phys-2-1',9,stem=[STEM2],fig='q2-equations',cells='The full formula earns 9; the separately printed 6 and 3 are alternative partial-credit scores.')
A('2v','Q2(v)',2,'State one precaution which the student might have taken',5,[menu('lagging, use sensitive thermometer / use a thermometer graduated to 0.1°C,',1,4,end='large temperature change, no parallax when reading the thermometer etc.',sep=',',open_list=True,note_sel=S('the precaution can be implied from the diagram if it has not already been','partial answer e.g. repeat / average / no parallax'),note='Partial credit: 2. Do not award the same precaution twice.')],'phys-2-1',4,end='to get an accurate result.',sq=SQ(5,'State one precaution which the student might have taken to get','an accurate result'),stem=[STEM2])
A('3i','Q3(i)',3,'Draw a labelled diagram of the apparatus used in this experiment.',6,[anyn(None,4,3,options=[S(x) for x in ['concave mirror','object e.g. crosswire','image / screen','correct arrangement','detail e.g. optical bench, metre-stick, ray-box, etc.']],note_sel=S('approximate method maximum mark 3×3','accept valid alternatives'))],'phys-2-3',12,stem=[STEM3],fig='q3-data')
A('3ii','Q3(ii)',3,'How did the observer know that the apparatus was correctly arranged',6,[R('the (inverted) image was in (sharp) focus (on the screen) // inverted image',6,**partial(6,3,'partial answer e.g. mentions screen'))],'phys-2-3',6,end='to record the data?',sq=SQ(6,'How did the observer know that the apparatus was correctly','arranged to record the data?'),stem=[STEM3],fig='q3-data')
A('3iii','Q3(iii)',3,'Indicate on your diagram the measurements that were taken.',6,[R('distance from the object/crosswire to the mirror',3),R('distance from the image/screen to the mirror',3,**partial(6,3))],'phys-2-3',6,sq=SQ(6,'Indicate on your diagram the measurements that were taken?'),stem=[STEM3,P(3,'Draw a labelled diagram of the apparatus used in this experiment.')],fig='q3-data')
A('3iv','Q3(iv)',3,'Calculate the value of the focal length f of the mirror, using the data above.',6,[EQ(6,(251,449,312,465),'=)10.07 cm',12,units=[3]*4,note='Complete calculation and average: 12. Formula: 6; first calculation: 8; each further calculation adds 1; inversion adds 1; average adds 1. Partial answer: 3. Full printed working is shown below.')],'phys-2-3',12,sq=SQ(6,'Calculate the value for the focal length f of the mirror, using the data','data above'),stem=[STEM3],qfig='q3iv-question',fig='q3iv-solution',cells='The complete calculation earns 12; the intermediate 6, 8 and 3 annotations are alternative partial scores.')
A('3v','Q3(v)',3,'Why might it be an advantage to use a darkened room when carrying out',6,[menu('greater accuracy, more reliable result, minimise errors, the image',1,4,end='might be clearer, helps to get a sharp image etc.',sep=',',open_list=True,**partial(4,2))],'phys-2-3',4,end='this experiment?',sq=SQ(6,'Why might it be an advantage to use a darkened room when carrying','out this experiment.'),stem=[STEM3],fig='q3-data')
TASKS.append(T('4i','Q4(i)','A',P(3,'Draw a labelled diagram of the apparatus used in this experiment.',nth=2),[*[pt(S('ohmmeter/multimeter, heating-source, conductor/resistor each one (3) all three3 × 3',piece=[1,i],psep=[' each one',',']),3) for i in [1,2,3]],R('detail e.g. insulation, container, thermometer',3,note_sel=S('NOTE: no labels deduct 2','accept valid alternatives methods'))],'phys-3-3','4i',SQ(7,'Draw a labelled diagram of the apparatus used in this experiment.'),12,stem=[STEM4]))
A('4ii','Q4(ii)',3,'How was the value of the resistance of the metallic conductor measured?',7,[R('ohmmeter / multimeter (set to read ohms)',6,**partial(6,3,'partial answer e.g. reference to measuring voltage or current / resistance meter'))],'phys-3-3',6,stem=[STEM4])
A('4iii','Q4(iii)',3,'Using the data in the table draw a graph, on graph paper, to show the variation of',7,[C('label axes correctly, (name / symbol / unit acceptable)',3),C('plot six points correctly',6,units=[1]*6,note_sel=S('-1 for each error thereafter')),C('straight line',3,note_sel=S('if graph paper is not used, maximum mark 3 × 3'))],'phys-3-3',12,end='the resistance of the metallic conductor with temperature.',sq=SQ(7,'Using the data in the table, draw a graph on graph paper to show the','variation of resistance of the metallic conductor with temperature.'),stem=[STEM4],qfig='q4iii-question',fig='q4-graph',notes='The paper provides seven readings; all seven are retained even though the scheme prices plotting six points.')
A('4iv','Q4(iv)',3,'What does the graph tell you about the relationship between the resistance of',7,[R('resistance increases with temperature // linear // ∝ (on kelvin scale)',6,**partial(6,3,'partial'))],'phys-3-3',6,end='a metallic conductor and its temperature?',sq=SQ(7,'What does the graph tell you about the relationship between the resistance','of a metallic conductor and its temperature?'),stem=[STEM4],fig='q4-data')
A('4v','Q4(v)',3,'Use your graph to find the temperature of the metallic conductor when it has',7,[R('47 – 50 (°C) // answer consistent with graph',4,note_sel=S('evidence of using the graph at 22.8 Ω'),note='Partial credit: 2.')],'phys-3-3',4,end='a resistance of 22.8 Ω.',sq=SQ(7,'Use your graph to find the temperature of the metallic conductor when it has a','resistance of 22.8 Ω.'),stem=[STEM4],fig='q4-data')

A('5a','Q5(a)',4,'Name an example of (i) a vector quantity and (ii) a scalar quantity.',8,[C('correct examples of each',7,units=[4,3],note_sel=S('partial answer e.g. examples in reverse order, definitions given'),note='Both required examples earn 7; the printed partial-credit score is 4.')],'phys-1-1',7,sq=SQ(8,'Name an example of (i) a vector quantity (ii) a scalar quantity.'))
A('5b','Q5(b)',4,'A door handle is used to open a door.',8,[R('( M = Fd = 40 ×0.12 = 40 × 0.12 =) 4.8 N m',7,**partial(7,4))],'phys-1-2',7,end='Calculate the moment of the force applied in the diagram.',fig='q5b-handle')
A('5c','Q5(c)',4,'Choose from the list below the instrument used to measure (i) electrical current',8,[anyn(None,2,4,steps=[4,3],options=[S('ammeter'),S('metre stick barometer',piece=1,psep=' barometer')],note_sel=S('one correct'),note='Both instruments: 7; one: 4.')],'phys-1-1',7,end='ammeter protractor metre stick barometer',sq=SQ(8,'Choose from the list below the instrument used to measure','(i) electrical current and (ii) length.'),decision='Two required instrument matches from the full printed four-instrument list, assessed together on the scheme’s seven/four scale.')
A('5d','Q5(d)',4,'Conduction is one method of heat transfer. Name the other two methods.',8,[menu('convection, radiation',2,4,sep=',',steps=[4,3],note='Both required methods: 7; one: 4.')],'phys-2-1',7)
A('5e','Q5(e)',4,'Name the instrument shown.',8,[R('micrometer /screw gauge',7,**partial(7,4))],'phys-1-1',7,sq=SQ(8,'Name the instrument shown'),fig='q5e-micrometer')
A('5f','Q5(f)',4,'State one common use for a convex lens.',8,[menu('magnification, (eye) glasses, binoculars, contact lenses, camera, etc.',1,7,sep=',',open_list=True,**partial(7,4,'partial answer e.g. use of convex mirror'))],'phys-2-3',7,sq=SQ(8,'State one common use of a convex lens.'))
A('5g','Q5(g)',4,'Resonance can cause a wine glass to shatter. What is resonance?',8,[anyn(None,2,4,steps=[4,3],options=[S('transfer of energy'),S('between bodies at the same frequency // at natural frequency')],note_sel=S('partial answer e.g. refers to natural frequency'),note='Both lines: 7; one line: 4.')],'phys-2-5',7)
A('5h','Q5(h)',4,'Name one source of voltage.',8,[menu('cell, battery, power supply,(charged) capacitor, etc.',1,7,sep=',',open_list=True,**partial(7,4))],'phys-3-3',7)
A('5i','Q5(i)',4,'What sub-atomic particle is released by the photoelectric effect?',8,[R('electron',7,**partial(7,4))],'phys-4-2',7)
A('5j','Q5(j)',4,'Name one method of detecting radiation.',8,[menu('Geiger-Muller tube, Geiger counter, solid state detector, cloud chamber,',1,7,end='bubble chamber, GLE, photographic film, radiometer, radiation sensor, etc.',sep=',',open_list=True,**partial(7,4))],'phys-4-4',7,sq=SQ(8,'Name one method of detecting radiation?'))

A('6i','Q6(i)',5,'Explain the underlined terms.',9,[R('force: causes an object to accelerate',6,**partial(6,3)),R('acceleration: rate of change of velocity',6,**partial(6,3)),R('gravity: force of attraction between masses',6,**partial(6,3))],'phys-1-2',18,stem=[SLING],qfig='q6i-question',fig='q6i-solutions',decision='One printed response requires all three underlined headings. Each retains its six-mark row; complete alternative mathematical definitions are visible in the source solution.')
A('6ii','Q6(ii)',5,'What form of energy does the pod have due to its motion?',9,[R('kinetic (energy)',6,**partial(6,3))],'phys-1-4',6,stem=[SLING],fig='q6-sling')
A('6iii','Q6(iii)',5,'What form of energy does the pod have at its highest point?',9,[R('potential (energy)',6,**partial(6,3))],'phys-1-4',6,stem=[SLING],fig='q6-sling')
A('6iv','Q6(iv)',5,'Why do the occupants experience apparent weightlessness at the pod’s highest',9,[R('freefall / no reaction force / no support force',3)],'phys-1-2',3,end='point?',sq=SQ(9,'Why do the occupants experience apparent weightlessness at the pod’s','highest point?'),stem=[SLING],fig='q6-sling')
A('6v','Q6(v)',5,'Calculate the potential energy stored in the springs before the pod is released.',9,[R('(PE = mgh = 400 × 9.8 × 50 = ) 196 000 J',6,**partial(6,3,'partial answer e.g. correct equation'))],'phys-1-4',6,sq=SQ(9,'Calculate the potential energy stored in the springs before the pod is','released.'),stem=[SLING,POD,GRAV],fig='q6-sling')
A('6vi','Q6(vi)',5,'Draw a diagram to show the forces acting on the pod when it is released.',9,[pt(S('diagram to show: downward force/ weight, upward force / tension',piece=2,psep=':'),6,kind='criterion',units=[3,3],note_sel=S('partial answer e.g. any one'),note='Both forces: 6; either one: 3.')],'phys-1-2',6,stem=[SLING],fig='q6-sling')
A('6vii','Q6(vii)',5,'Calculate the momentum of the pod when it has a speed of 8 m s⁻¹.',9,[R('( p = mv = 400 × 8 = ) 3200 kg m s⁻¹',6,**partial(6,3,'partial answer e.g. correct equation'))],'phys-1-2',6,stem=[SLING,POD],fig='q6-sling')
A('6viii','Q6(viii)',5,'State one energy loss that might prevent the pod from reaching its',9,[R('friction / air resistance',5,**partial(5,3))],'phys-1-4',5,end='maximum height.',sq=SQ(9,'State one energy loss that might prevent the pod from reaching its maximum','height.'),stem=[SLING],fig='q6-sling')

A('7i','Q7(i)',6,'What is meant by reflection of light?',10,[R('rebounding / bouncing of light from a surface',6,**partial(6,3))],'phys-2-3',6)
A('7ii','Q7(ii)',6,'State the laws of reflection.',10,[anyn(None,2,6,steps=[6,3],options=[S('angle of incidence is equal to the angle of reflection'),S('incident ray, the normal, and the reflected ray are coplanar two lines correct',piece=1,psep=' two lines correct')],note_sel=S('partial answer'),note='Both laws: 9; either one: 6; partial: 3.')],'phys-2-3',9,cells='Both laws earn 9; the standalone (6) and (3) are partial-credit scores.')
A('7iii','Q7(iii)',6,'Draw a diagram to show how a periscope works.',10,[anyn(None,3,3,options=[S(x) for x in ['two mirrors/ prisms facing each other','mirrors at 45°','correct ray path (in either direction)','tubing']],note='Any three diagram criteria earn nine marks.')],'phys-2-3',9,stem=[PERISCOPE],qfig='q7iii-question',fig='q7iii-solution')
A('7iv','Q7(iv)',6,'Explain why the driver can read the word correctly',10,[R('(the mirror causes an apparent) left to right reversal // lateral inversion',6,**partial(6,3))],'phys-2-3',6,end='in the mirror.',sq=SQ(10,'Explain why the driver can read the word correctly in the mirror.'),stem=[AMBULANCE],fig='q7-ambulance')
A('7v','Q7(v)',6,'Draw a labelled diagram to show how total internal reflection occurs.',10,[C('diagram showing indication of 2 media, i > C / i = r, internal reflection',9,units=[6,3],note_sel=S('diagram with one omission','Note: no labels deduct 2'),note='Complete: 9; one omission: 6; partial: 3; deduct 2 for no labels.')],'phys-2-3',9,stem=[FIBRE],fig='q7v-solution')
A('7vi','Q7(vi)',6,'Draw a labelled diagram to show how an optical fibre transmits light along its',10,[C('diagram showing fibre, multiple internal reflections',9,units=[3]*3,note_sel=S('diagram with one omission','Note: no labels deduct 2'),note='Complete: 9; one omission: 6; partial: 3; deduct 2 for no labels.')],'phys-2-3',9,end='length.',sq=SQ(10,'Draw a labelled diagram to show how an optical fibre transmits light','along its length.'),stem=[FIBRE],fig='q7vi-solution')
A('7vii','Q7(vii)',6,'An optical fibre cable has a refractive index of 1.5.',10,[EQ(10,(287,725,327,744),'C = 41.8°',8,note='Full calculation: 8; one error: 6; correct equation: 4. The full working is shown below.')],'phys-2-3',8,end='Calculate the angle at which total internal reflection occurs.',fig='q7vii-solution',cells='The complete calculation is eight marks; standalone six and four cells are alternative partial scores.')

A('8i','Q8(i)',6,'What is meant by the frequency of a wave?',11,[R('number of waves passing per second',6,**partial(6,3))],'phys-2-2',6)
A('8ii','Q8(ii)',6,'State the relationship between the frequency of a wave and its wavelength.',11,[pt(S('// c = fλ',piece=2,psep='//'),6,note='Either of the three equivalent printed equations is accepted. Partial credit: 3.')],'phys-2-2',6,fig='q8ii-equations')
A('8iii','Q8(iii)',6,'What name is given to this effect?',11,[R('Doppler',6,**partial(6,3,'partial answer e.g. example'))],'phys-2-7',6,stem=[DOPPLER],fig='q8-ambulance')
A('8iv','Q8(iv)',6,'Explain, with the aid of a labelled diagram, how this phenomenon occurs.',11,[C('moving wave source',3),C('wave fronts',3),R('as the moving wave source approaches',3,route='approaching'),R('the waves get closer together',3,route='approaching'),pt(S('// conversely as the wave','source moves away the waves are further apart (2× 3)',piece=[2,1],psep=['//',' (2× 3)']),6,units=[3,3],route='receding',note_sel=S('accept valid alternatives','Note: no labels deduct 2, no diagram maximum mark 3 × 3'),note='Use either approaching or receding explanation, together with both diagram criteria.')],'phys-2-7',12,stem=[DOPPLER],qfig='q8iv-question',fig='q8iv-solution',cells='The first two diagram criteria are three each. Either the approaching explanation (3+3) or the converse receding explanation (2×3) completes twelve marks.')
A('8v','Q8(v)',6,'Name one practical application of this phenomenon.',11,[menu('speed gun, (measuring) red shift, ultrasonic scanners, imaging',1,5,end='used to study blood flow, used to study heart beat, weather forecasting, etc.',sep=',',open_list=True,**partial(5,3,'partial answer e.g. general application such as medicine, radar, sonar'))],'phys-2-7',5,stem=[DOPPLER],fig='q8-ambulance')
STORM=P(6,'An electrical storm is seen before it is heard. What does this indicate about the','difference between sound waves and light waves?')
A('8vi','Q8(vi)',6,'An electrical storm is seen before it is heard. What does this indicate about the',11,[R('light travels faster than sound',6,**partial(6,3,'partial answer e.g. reversed'))],'phys-2-2',6,end='difference between sound waves and light waves?')
A('8vii','Q8(vii)',6,'State one other difference between sound waves and light waves.',11,[menu('sound waves are longitudinal // light waves are transverse //',1,6,end='sound waves need a medium // light waves may be polarised',**partial(6,3))],'phys-2-2',6,stem=[STORM])
A('8viii','Q8(viii)',6,'Calculate the difference in time the runner would receive if the stopwatch was',11,[FR(11,(84,731,195,755),'(t= s/v = 100/330 =)0.3 s',9,units=[3]*3,note='Complete: 9; one error: 6; partial: 3.')],'phys-2-5',9,end='delay caused by the time taken for the sound to travel 100 m.',sq=SQ(11,'Calculate the difference in time the runner would receive if the stopwatch','without any delay caused by the time taken for the sound to travel 100 m .9 or 6 or 3'),stem=[SPRINT,P(6,'(speed of sound in air = 330 m s⁻¹)')],fig='q8viii-solution',cells='The full calculation earns nine; the separate six and three are partial scores.')

A('9i','Q9(i)',7,'What is a magnetic field?',12,[R('a region/space where a magnetic force is felt / it effects a compass',6,**partial(6,3,'partial answer e.g. draws magnetic field'))],'phys-3-4',6)
A('9ii','Q9(ii)',7,'State one example of a good conductor and one example of a good insulator.',12,[C('one example of a good conductor',3),C('one example of a good insulator',3)],'phys-3-3',6,sq=SQ(12,'State one example of a good conductor and one example of a good','insulator.'))
A('9iii','Q9(iii)',7,'Name the unit of voltage.',12,[R('volt / V',6,**partial(6,3))],'phys-3-3',6)
A('9iv','Q9(iv)',7,'What happens to the wire when current flows through it?',12,[R('it moves // it experiences a force // gets hot',6,**partial(6,3))],'phys-3-5',6,stem=[WIRE],fig='q9-battery')
A('9v','Q9(v)',7,'What happens when the direction of the current is reversed?',12,[R('wire moves in the other direction',6,**partial(6,3,'partial answer e.g. wire moves'))],'phys-3-5',6,stem=[WIRE],fig='q9-battery')
A('9vi','Q9(vi)',7,'Name one device based on this effect.',12,[menu('electric motor, speaker, (moving coil) galvanometer, etc.',1,6,sep=',',open_list=True,**partial(6,3))],'phys-3-5',6,stem=[WIRE,P(7,'What happens to the wire when current flows through it?')],fig='q9-battery')
A('9vii','Q9(vii)',7,'What is observed on the voltmeter when neither the wire nor the magnet',12,[R('no reading / no deflection / nothing',4)],'phys-3-6',4,end='move?',sq=SQ(12,'What is observed on the voltmeter when neither the wire nor the magnet move?'),stem=[WIRE,INDUCTION],fig='q9-voltmeter')
A('9viii','Q9(viii)',7,'What is observed on the voltmeter when either the wire or the magnet',12,[R('deflection / pointer moves / reading',4)],'phys-3-6',4,end='is moved?',sq=SQ(12,'What is observed on the voltmeter when either the wire or the magnet is moved?'),stem=[WIRE,INDUCTION],fig='q9-voltmeter')
A('9ix','Q9(ix)',7,'Name a scientist whose law is associated with this phenomenon?',12,[R('Faraday / Lenz',6,**partial(6,3))],'phys-3-6',6,stem=[WIRE,INDUCTION,P(7,'What is observed on the voltmeter when either the wire or the magnet','is moved?')],fig='q9-voltmeter')
A('9x','Q9(x)',7,'Magnetism is one effect associated with an electric current.',12,[R('heating // chemical',6,**partial(6,3))],'phys-3-3',6,end='Name one other effect.',sq=SQ(12,'Magnetism is one effect associated with an electric current. Name one','other effect.'))

A('10i','Q10(i)',8,'Name three types of radiation.',13,[menu('alpha / α, beta / β, gamma / γ',3,3,sep=',')],'phys-4-4',9,stem=[P(8,'Radiation is released when radioactive elements decay.')])
A('10ii','Q10(ii)',8,'Which type of radiation has no charge?',13,[R('gamma / γ',3)],'phys-4-4',3)
A('10iii','Q10(iii)',8,'Which type of radiation is the least penetrating?',13,[R('alpha / α',3)],'phys-4-4',3)
A('10iv','Q10(iv)',8,'Which type of radiation is not deflected by magnetic fields?',13,[R('gamma / γ',3)],'phys-4-4',3)
A('10v','Q10(v)',8,'State one danger associated with nuclear radiation.',13,[menu('leukaemia, cancer, skin burns, hair loss, kills cells, damage DNA, etc.',1,6,sep=',',open_list=True,**partial(6,3))],'phys-4-4',6)
A('10vi','Q10(vi)',8,'State one precaution that should be taken when handling',13,[menu('protective clothing, tongs, etc.',1,3,sep=',',open_list=True)],'phys-4-4',3,end='radioactive substances.',sq=SQ(13,'State one precaution that should be taken when handling radioactive substances.'))
A('10vii','Q10(vii)',8,'What is nuclear fission?',13,[R('splitting (of a large nucleus)',3),R('into two (smaller nuclei) // with release of energy / neutrons',3,note_sel=S('partial answer e.g. defines fusion'),note='Partial credit for a fusion definition: 3.')],'phys-4-6',6,stem=[REACTOR],fig='q10-reactor')
A('10viii','Q10(viii)',8,'Name a fuel used in nuclear reactors.',13,[menu('plutonium / Pu, (enriched) uranium / U, thorium / Th',1,5,sep=',',**partial(5,3))],'phys-4-6',5,stem=[REACTOR],fig='q10-reactor')
_defs=P(8,'State the function of (a) the control rods and (b) the shielding in a reactor.')
TASKS.append(T('10ixa','Q10(ix)(a)','B',[dict(_defs,piece=1,psep=' (a)'),dict(_defs,piece=[2,1],psep=[' (a)',' and (b)'])],[R('control rate of reaction // absorbs neutrons',6,**partial(6,3,'partial answer e.g. refers to boron rods'))],'phys-4-6','control-rods',SQ(13,'State the function of (a) the control rods and','(b) the shielding in a reactor.'),6,stem=[REACTOR],fig='q10-reactor'))
TASKS.append(T('10ixb','Q10(ix)(b)','B',[dict(_defs,piece=1,psep=' (a)'),dict(_defs,piece=2,psep=' (b)')],[R('prevents escape of radiation',6,**partial(6,3,'partial answer e.g. protection / safety'))],'phys-4-6','reactor-shielding',SQ(13,'State the function of (a) the control rods and','(b) the shielding in a reactor.'),6,stem=[REACTOR],fig='q10-reactor'))
A('10x','Q10(x)',8,'What is the purpose of the heat exchanger?',13,[R('converts (kinetic energy) energy to heat // brings energy to the generator',6,**partial(6,3))],'phys-4-6',6,stem=[REACTOR],fig='q10-reactor')

for key,question,rows in [
 ('a','What is the function of the electricity meter?',[R('to measure the (electrical) energy used',7,**partial(7,4))]),
 ('b','What is meant by the term a.c.?',[R('alternating current',7,**partial(7,4))]),
 ('c','Name three safety devices found in domestic circuits.',[pt(S('fuse, earth, miniature circuit breaker/ (trip) switch, residual current device any 3 7',piece=1,psep=' any 3'),7,kind='point',note='Name any three of these devices for seven marks. The scheme gives four marks for a partial answer; it does not allocate marks to individual devices.')]),
 ('d','What is the cause of most accidents associated with electrical appliances?',[R('damaged flexes // wrongly-wired plugs',7,**partial(7,4))]),
 ('e','What is the function of the test button on an RCD?',[R('to check that the mechanism is working properly',7,**partial(7,4))]),
 ('f','Name the pins labelled A, B and C in the diagram.',[menu('A – neutral; B – live; C – earth',3,3,steps=[3,2,2],sep=';',note_sel=S('1st named pin matched correctly 3 marks, others matched correctly 2 marks each','1st named mismatched pin by label/ colour 2 marks, others 1 mark each'))]),
 ('g','State one precaution that should be taken when wiring a plug.',[menu('no loose strands of wire are exposed // all the screw connections are',1,7,end='tightened // leave a little extra slack on the green/yellow wire within the plug.',**partial(7,4))])]:
 A('11'+key,'Q11('+key+')',9,question,14,rows,'phys-3-3',7,stem=[PASSAGE],fig='q11-plug')
A('11h','Q11(h)',9,'What is the maximum power that an appliance with a 13 A plug can use',14,[R('(P=IV= 13 × 220= ) 2860 W',7,**partial(7,4))],'phys-3-3',7,end='when connected to a 220 V supply?',sq=SQ(14,'What is the maximum power that an appliance with a 13 A plug can use when','connected to a 220 V supply?'),stem=[PASSAGE],fig='q11-plug')

A('12ai','Q12(a)(i)',10,'Define (i) velocity and (ii) friction.',15,[anyn(None,2,6,steps=[6,3],options=[S('rate of change of displacement // distance over time (in a given direction)'),S('force (between 2 bodies in contact) which opposes motion two correct 6 + 3',piece=1,psep=' two correct')],note_sel=S('partial'),note='Both required definitions: 9; either one: 6; partial: 3.')],'phys-1-1',9,sq=SQ(15,'Define (i) velocity and (ii) friction.'),decision='Both inline definitions stay together because the published tariff is nine for both and six for either one.',cells='Nine for both definitions, six for one, three for partial; these are alternatives.')
A('12aiii','Q12(a)(iii)',10,'Draw a diagram indicating the main forces acting on the car',15,[anyn(S('Weight/W, reaction force/R, force from engine/Fₑ, friction/Fr two correct',piece=1,psep=' two correct'),2,3,sep=',',note='Two correct forces: 6; one: 3.')],'phys-1-2',6,end='when it was accelerating.',sq=SQ(15,'Draw a diagram indicating the main forces acting on the car when it','was accelerating.'),stem=[CAR],fig='q12a-forces')
A('12aiv','Q12(a)(iv)',10,'Calculate how long it took the car to reach its top speed.',15,[R('70 s',6,**partial(6,3,'partial answer e.g. v = u + at'))],'phys-1-1',6,stem=[CAR],fig='q12a-time')
A('12av','Q12(a)(v)',10,'Sketch the velocity-time graph for the journey.',15,[C('correct velocity-time graph',7,**partial(7,4,'partial'))],'phys-1-1',7,stem=[CAR],fig='q12a-graph')
TASKS.append(T('12bi','Q12(b)(i)','B',P(10,'Explain the underlined terms.'),[R('heat pump: means of transferring heat from a cold region to a warm region',6,**partial(6,3,'partial answer e.g. device to transfer heat')),R('specific latent heat : heat needed to change the state of 1 kg of a substance',6,**partial(6,3,'partial answer e.g. refers to no change in temperature'))],'phys-2-1','heat-pump-latent-heat',SQ(15,'Explain the underlined terms.'),12,stem=[P(10,'The heat pump in a fridge uses a fluid with a high specific latent heat.')],qfig='q12bi-question',decision='One printed response requires both underlined headings, each separately assessed at six marks.'))
TASKS.append(T('12bii','Q12(b)(ii)','B',[P(10,'Calculate',after='A fridge lowers'),P(10,'the energy removed from the water')],[R('(E = mcΔθ = 2 × 4200 × 25 = ) 210 000 J',12,units=[3]*4,note_sel=S('one error','partial answer e.g. incomplete formula'),note='Full calculation: 12; one error: 9; two errors: 6; incomplete formula: 3.')],'phys-2-1','fridge-energy',SQ(15,'the energy removed from the water'),12,stem=[FRIDGE,SHC],cells='Twelve for a complete calculation; nine, six and three are successive alternative partial scores.'))
TASKS.append(T('12biii','Q12(b)(iii)','B',[P(10,'Calculate',after='A fridge lowers'),P(10,'the power of the fridge.')],[R('250 W // answer consistent with (ii)',4,**partial(4,2,'partial answer e.g. correct formula'))],'phys-1-4','fridge-power',SQ(15,'the power of the fridge.'),4,stem=[FRIDGE,SHC],fig='q12b-power'))
A('12ci','Q12(c)(i)',11,'Define pressure and state its unit.',16,[R('force',3),R('per unit area',3,note_sel=S('partial e.g. P = ρgh')),R('pascal / N m⁻²',4)],'phys-1-2',10,decision='Definition and its unit remain one required response with the published 3+3+4 rows.')
A('12cii','Q12(c)(ii)',11,'Describe an experiment to demonstrate that the atmosphere exerts',16,[R('apparatus: e.g. can of water and heat source',3),R('procedure: e.g. boil water and put on lid',3),R('observation: e.g. can collapses',3,note_sel=S('accept valid alternatives e.g. sucking out air methods','marks may be obtained from a diagram'))],'phys-1-2',9,end='pressure.',sq=SQ(16,'Describe an experiment to demonstrate that the atmosphere exerts pressure.'))
A('12ciii','Q12(c)(iii)',11,'Calculate the volume of the balloon when it reaches the height of',16,[R('= 6.7 L',9,units=[3]*3,note_sel=S('one error','partial answer e.g. P₁V₁ = P₂V₂ / PV=k / Boyle’s law'),note='Full calculation: 9; one error: 6; correct equation: 3. Full substituted working is shown below.')],'phys-2-1',9,end='Mount Everest.',stem=[BALLOON,PRESSURE],fig='q12c-volume',cells='Nine is the full score; six and three are alternative partial scores.')
A('12di','Q12(d)(i)',11,'State Coulomb’s law of force between electric charges.',16,[R('force proportional to the product of charges / F ∝ q₁q₂',3),pt(S('inversely proportional to the distance between the charges squared /',piece=1,psep=' /'),3)],'phys-3-1',6,fig='q12d-law')
A('12dii','Q12(d)(ii)',11,'What is observed when the switch is closed?',16,[R('bulb flashes',6,**partial(6,3,'partial e.g. bulb lights, current flows, etc.'))],'phys-3-2',6,stem=[CAPACITOR],fig='q12d-circuit')
A('12diii','Q12(d)(iii)',11,'What would be observed if a 12 V a.c. power supply had been used',16,[R('bulb lights (continuously)',4,**partial(4,2,'partial e.g. bulb flashes'))],'phys-3-2',4,end='instead?',sq=SQ(16,'What would be observed if a 12 V a.c. power supply had been used instead?'),stem=[CAPACITOR],fig='q12d-circuit')
A('12div','Q12(d)(iv)',11,'Calculate the charge stored on the capacitor when it is connected to the',16,[R('= ) 0.72 C',9,units=[3]*3,note_sel=S('one error','partial answer'),note='Complete calculation: 9; one error: 6; partial: 3.')],'phys-3-2',9,end='12 V d.c. power supply.',sq=SQ(16,'Calculate the charge stored on the capacitor when it is connected to the 12 V d.c.','power supply.'),stem=[CAPACITOR],qfig='q12div-question',fig='q12div-solution',cells='Nine for the complete calculation; six and three are alternatives for partial answers.')
A('12dv','Q12(d)(v)',11,'State one application of a capacitor.',16,[R('store charge / conducts a.c. /(radio) tuning / filtering / smoothing / timing /',3,end='store energy / flash camera / phone charger, etc.')],'phys-3-2',3)

SELECTION_SCAN=[
 ('paper',4,'the following','All ten Q5 short questions retained; no best-eight combinations.'),
 ('paper',4,'choose','Q5(c) retains all four instruments and both required matches in one stepped card.'),
 ('paper',6,'both','Reflection/refraction statement, no selection.'),
 ('paper',7,'or','Two possible sources of a magnetic field, narrative not selection.'),
 ('paper',7,'either','Either moving component produces the same observation; one question.'),
 ('paper',7,'or','Same observation when either component moves; no expansion.'),
 ('paper',9,'the following','All eight questions carry the complete passage.'),
 ('paper',9,'or','Passage lists alternative protection devices, not task choices.'),
 ('paper',9,'or','Electric shock or fire in passage, not task choices.'),
 ('paper',9,'or','Damage/fault examples in passage, not task choices.'),
 ('paper',9,'either','Causes of accidents in passage, not task choices.'),
 ('paper',9,'or','Same accident causes, no expansion.'),
 ('paper',10,'any two','All four Q12 options retained; no combinations.'),
 ('paper',10,'the following','Same Q12 instruction; all four retained.')]

# Exact visual tariff review and coordinate-based equation readings.
_by={t['key']:t for t in TASKS}
_by['3iv']['rows'][0].update(clip=(221,448,269,464),expect='=)10.07cm')
_by['7vii']['rows'][0].update(clip=(282,727,325,743),expect='C=41.8°')
_by['8viii']['rows']=[EQ(11,(151,734,172,750),'0.3s',9,units=[3]*3,note='Complete: 9; one error: 6; partial: 3. The exact fractional calculation is shown below.')]
_by['10ixb']['sq']=SQ(13,'State the function of (a) the control rods and','(b) the shielding in a reactor.',paired='The paper’s separately priced shielding function is part (b) of this exact reprinted question; only its six-mark answer is selected.')
_by['12ai'].update(ref='Q12(a)',item=('definitions','Velocity and friction'),sq=SQ(15,'Part (a) Define (i) velocity and (ii) friction.'))
_by['12div']['rows'][0]['sel']=S(') 0.72 C')
for key,reason in {
 '4v':'The full graph reading earns four; the separate two is partial credit for evidence of using the graph.',
 '5c':'The required instrument pair earns seven; the separate four is partial credit for one correct instrument.',
 '7v':'Complete diagram nine, one omission six, partial three. These are alternative scores.',
 '7vi':'Complete diagram nine, one omission six, partial three. These are alternative scores.'
}.items():_by[key]['cells']=reason
ASK_EXEMPT=[
 (5,'a form of potential energy. When the pod and springs are released, this potential energy','When-clause is narrative sling-shot context, retained in each relevant stem and the definitions source image.'),
 (6,'When timing a 100 m sprint, a person stands at the finishing line and starts','Narrative timing context retained in Q8(viii), not a separate ask.'),
 (9,'pin/terminal in the plug. When you connect each wire to','Narrative passage instructions retained in all eight passage cards, not another exam ask.'),
 (10,'When the car approached its destination, the driver applied the brakes uniformly','Car-motion context retained in every relevant Q12(a) task, not a separate ask.')]
FIGURES={
 'q1-equations':('scheme',4,(92,469,342,554),SEC,[],'Both official gravity equations with complete fractions, radical and partial-credit examples.',True),
 'q2-equations':('scheme',5,(106,498,441,515),SEC,[],'The two accepted specific-heat-capacity equations, including every subscript and temperature change.',True),
 'q3-data':('paper',3,(133,95,454,153),SEC,[],'All three object-distance and image-distance pairs, with centimetre headings.',False),
 'q3iv-question':('paper',3,(82,55,523,278),SEC,[],'Concave-mirror experiment, complete data table and focal-length calculation question.',False,[(82,171,523,255)]),
 'q3iv-solution':('scheme',6,(110,440,419,643),SEC,[],'Full mirror calculation: formula, all three focal lengths, reciprocal working and average.',True),
 'q4-data':('paper',3,(106,566,513,630),SEC,[],'All seven temperature and resistance pairs, with degree Celsius and ohm units.',False),
 'q4iii-question':('paper',3,(82,435,523,679),SEC,[],'Metallic conductor experiment, seven readings and graph question.',False,[(82,473,523,517)]),
 'q4-graph':('scheme',7,(91,420,481,650),SEC,[],'Official resistance-versus-temperature graph with axes, units, points and graph-reading guides.',True),
 'q5b-handle':('paper',4,(219,331,390,416),SEC,[],'Door handle with force forty newtons and perpendicular distance 0.12 metres.',False),
 'q5e-micrometer':('paper',4,(394,536,493,581),SEC,[],'The measuring instrument shown in Q5(e).',False),
 'q6-sling':('paper',5,(191,155,423,354),SEC,[],'The fairground sling-shot pictured in the paper.',False),
 'q6i-question':('paper',5,(82,55,523,393),SEC,[],'Complete sling-shot paragraph, the three underlined terms, photograph and instruction to explain them.',False),
 'q6i-solutions':('scheme',9,(110,249,443,318),SEC,[],'Official definitions of force, acceleration and gravity with all three alternative mathematical expressions.',True),
 'q7iii-question':('paper',6,(82,113,524,173),SEC,[],'Periscope context, illustration and diagram question.',False),
 'q7iii-solution':('scheme',10,(243,261,354,380),SEC,[],'Official periscope ray path with both mirrors and tubing labelled.',True),
 'q7-ambulance':('paper',6,(395,179,497,237),SEC,[],'Ambulance photograph showing its mirror-reversed lettering.',False),
 'q7v-solution':('scheme',10,(274,539,416,585),SEC,[],'Total internal reflection at the glass–air boundary, with normal, rays and angle condition.',True),
 'q7vi-solution':('scheme',10,(184,643,447,698),SEC,[],'Light ray undergoing repeated internal reflections along an optical fibre.',True),
 'q7vii-solution':('scheme',10,(98,718,329,751),SEC,[],'Critical-angle calculation with the sine fraction, inverse calculation and 41.8-degree result.',True),
 'q8ii-equations':('scheme',11,(86,146,218,173),SEC,[],'The three accepted frequency–wavelength equations with lambda and fractions.',True),
 'q8-ambulance':('paper',6,(401,483,496,551),SEC,[],'Ambulance approaching the person, with sound wavefronts.',False),
 'q8iv-question':('paper',6,(82,483,523,575),SEC,[],'Complete moving-ambulance context and Doppler-explanation question.',False,[(82,537,395,555)]),
 'q8iv-solution':('scheme',11,(25,308,193,470),SEC,[],'Official moving-source Doppler diagram, with direction and both wavelengths.',True),
 'q8viii-solution':('scheme',11,(84,727,176,758),SEC,[],'Time-delay calculation showing distance divided by sound speed and 0.3 seconds.',True),
 'q9-battery':('paper',7,(211,192,414,281),SEC,[],'Complete wire, U-shaped magnet and battery circuit with component labels.',False),
 'q9-voltmeter':('paper',7,(211,403,414,486),SEC,[],'Wire and U-shaped magnet connected to a sensitive voltmeter.',False),
 'q10-reactor':('paper',8,(161,274,465,462),SEC,[],'Full labelled reactor: control rods, shielding, moderator, fuel, steam, heat exchanger and cold water.',False),
 'q11-plug':('paper',9,(392,214,541,385),SEC,[],'The three-pin plug photograph with all A, B and C markers.',False),
 'q12a-forces':('scheme',15,(202,239,353,322),SEC,[],'Official car-force diagram with weight, reaction, engine force and friction.',True),
 'q12a-time':('scheme',15,(122,376,354,405),SEC,[],'Acceleration-time working, including the velocity difference divided by acceleration and seventy-second result.',True),
 'q12a-graph':('scheme',15,(285,429,414,478),SEC,[],'Official velocity–time graph with acceleration, constant speed and braking to rest.',True),
 'q12bi-question':('paper',10,(109,471,524,619),SEC,[],'The underlined heat-pump and specific-latent-heat terms, fridge illustration and instruction.',False),
 'q12b-power':('scheme',15,(105,734,329,758),SEC,[],'Official power calculation, energy over time, giving 250 watts.',True),
 'q12c-volume':('scheme',16,(96,336,433,364),SEC,[],'Complete Boyle’s-law substitution and balloon volume 6.7 litres.',True),
 'q12d-law':('scheme',16,(95,436,451,475),SEC,[],'Both parts of Coulomb’s law, retaining the product and inverse-square formulae.',True),
 'q12d-circuit':('paper',11,(235,553,378,639),SEC,[],'Capacitor, bulb, switch and twelve-volt direct-current supply circuit.',False),
 'q12div-question':('paper',11,(109,485,524,727),SEC,[],'Complete capacitor context, capacitance and circuit with the charge calculation question.',False,[(109,644,524,694)]),
 'q12div-solution':('scheme',16,(95,668,293,696),SEC,[],'Charge calculation with capacitance fraction, power of ten and 0.72-coulomb result.',True),
}

# Inspect every emitted crop, then correct enclosure edges, labels and adjacent type.
for key,rect in {
 'q1-equations':(92,467,370,553),
 'q10-reactor':(130,265,513,464),
 'q11-plug':(379,217,572,378),
 'q12a-forces':(218,242,386,323),
 'q12a-time':(120,371,351,400),
 'q12a-graph':(264,433,421,493),
 'q12b-power':(106,737,371,764),
 'q12bi-question':(109,471,524,629),
 'q12c-volume':(96,340,433,364),
 'q12d-circuit':(180,550,380,640),
 'q12d-law':(95,434,451,483),
 'q3iv-solution':(110,440,419,638),
 'q4-graph':(68,420,487,652),
 'q5e-micrometer':(269,531,396,581),
 'q6-sling':(146,172,429,363),
 'q6i-solutions':(90,202,392,303),
 'q7-ambulance':(429,169,519,237),
 'q7iii-question':(82,84,524,169),
 'q7iii-solution':(238,264,354,386),
 'q7vi-solution':(206,643,450,698),
 'q7vii-solution':(98,722,329,751),
 'q8ii-equations':(86,149,218,173),
 'q8-ambulance':(406,478,542,560),
 'q8iv-question':(82,478,543,575),
 'q8viii-solution':(84,730,176,758),
 'q9-battery':(159,195,394,288),
 'q9-voltmeter':(159,397,425,493),
}.items():
 f=list(FIGURES[key]);f[2]=rect;FIGURES[key]=tuple(f)
for key,masks in {
 'q7iii-question':[(82,84,433,115)],
 'q7iii-solution':[(238,282,259,296),(238,308,250,323)],
 'q8iv-question':[(82,537,406,555)],
}.items():
 f=list(FIGURES[key]);f=f[:7]+[masks];FIGURES[key]=tuple(f)
# The source criterion is all three devices as a whole, not invented per-device marks.
_by['11c']['decision']='Open request for three safety devices: one seven-mark response, complete four-device guidance, and the published four-mark partial score. No invented per-device tariff.'
# Source line pieces preserve clean numeric results while exact working remains visible.
_by['3iv']['rows'][0].update(clip=(230,448,269,464),expect='10.07cm')
_by['12div']['rows'][0]['sel']=S(') 0.72 C',piece=2,psep=') ')
# Remove the non-answer “etc.” from open answer menus, without changing source wording.
for key in ['5f','5h','5j','8v','9vi','10v','10vi']:
 row=_by[key]['rows'][0];sel=row['sel']
 # The printed commas separate the examples, with the final “etc.” as a continuation.
 # Exact option counts come from the visually read list, not generated combinations.
 n={'5f':5,'5h':4,'5j':9,'8v':6,'9vi':3,'10v':6,'10vi':2}[key]
 row['options']=[dict(sel,piece=i,psep=',') for i in range(1,n+1)];row['sel']=None
for key,rect in {
 'q1-equations':(91,470,370,553),
 'q11-plug':(379,210,572,378),
 'q12a-forces':(218,246,386,323),
 'q12a-graph':(264,432,421,493),
 'q12d-law':(90,437,451,486),
 'q7iii-question':(82,53,524,169),
 'q8ii-equations':(86,149,218,177),
}.items():
 f=list(FIGURES[key]);f[2]=rect;FIGURES[key]=tuple(f)
f=list(FIGURES['q7iii-question']);f[7]=[(82,53,433,115),(504,53,524,115)];FIGURES['q7iii-question']=tuple(f)
f=list(FIGURES['q8iv-question']);f[7]=[(82,537,409,555)];FIGURES['q8iv-question']=tuple(f)
# Calibri's figure-dash glyph is the visually confirmed minus in a raised unit
# exponent. Mapping locally allows the source reader to retain the superscript.
_by['1ii-methods']['stem'].append(P(2,'What measurements were taken to calculate g?'))
_by['1iii']['stem'].append(P(2,'What measurements were taken to calculate g?'))
_by['5c']['q']=[P(4,'Choose from the list below the instrument used to measure (i) electrical current','and (ii) length.'),P(4,'ammeter protractor metre stick barometer',br=True)]
_by['6v']['q']['end']='Calculate the potential energy stored in the springs before the pod is released.'
_by['12ciii']['rows'][0]['sel']=S('= 6.7 L',piece=2,psep='= ')
for row in _by['6i']['rows']:row['note']=(row.get('note') or '')+' The complete alternative equation is shown in the official solution.'
f=list(FIGURES['q12d-law']);f[2]=(90,437,451,485);FIGURES['q12d-law']=tuple(f)
f=list(FIGURES['q12a-graph']);f[2]=(264,429,421,493);f=f[:7]+[[(264,429,277,432),(286,429,339,432)]];FIGURES['q12a-graph']=tuple(f)
# The plug-identification card explicitly decodes every visible label; this is
# required by the deck's labelled-diagram gate and preserves the stepped 3/2/2.
from phys_review_lib import L
_by['11f']['labels']=[L(letter,S('A – neutral; B – live; C – earth',piece=[i,2],psep=[';',' – '],page=14),True) for i,letter in enumerate('ABC',1)]
f=list(FIGURES['q11-plug']);f[4]=list('ABC');FIGURES['q11-plug']=tuple(f)
