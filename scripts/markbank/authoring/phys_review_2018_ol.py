"""Physics 2018 Ordinary — independently reviewed paper/scheme ledger.

All 12 paper and 16 scheme pages rendered and visually read, 2026-10-31.
Every printed option is retained. Q5 best-eight and Q12 any-two are not
combination-expanded. Required paired measurements retain their stepped scales.
Q6's inline definitions and Q12(a)'s inline definitions split at their explicit
roman and scheme boundaries; Q10(i)'s definition/properties split at six each.
Q8(i)'s underlined definitions remain one response with both required headings.
Partial credit is guidance, never additional credit. Every missing Cambria glyph
was visually read in first-occurrence crops; fractions are read by geometry.
"""
from phys_review_lib import Q, SQ, S, M, G, L, pt, anyn as _anyn, T
YEAR, LEVEL = 2018, 'ol'
REVIEWED_AT='2026-10-31'
LETTERED={5,9,11,12}
SOURCES={
 'paper':{'path':'examiner-reports/physics/papers/2018-ol-paper.pdf','fileid':'LC021GLP000EV.pdf','sha256':'ee7d3000ac3604387d4a12f669cd1884fcbde930f836542b02a757d5fab4fb91','pages':12},
 'scheme':{'path':'examiner-reports/physics/schemes/2018-ol.pdf','fileid':'LC021GLP000EV.pdf','sha256':'09c42866ecd6660a6bb5f93c00e6011ab92c969d7ab24b991c14283f06cf67a5','pages':16}}
PAGE_ROLES={'paper':{1:'cover',**{p:'questions' for p in range(2,12)},12:'back-cover'},'scheme':{1:'cover',2:'note',**{p:'marking' for p in range(3,16)},16:'back-cover'}}
GLYPHS={'scheme':{'Cambria':{2174:'R',2157:'A',2194:'l',2929:'s',2919:'i',2924:'n',3036:'i',3045:'r',4666:'(',2872:'4',2868:'0',4667:')',2870:'2',2873:'5',1829:'C',3404:'=',3044:'q',3023:'V',2869:'1',1865:'m',1874:'v',3019:'R',3046:'s',3047:'t',3049:'v',2879:'−',3048:'u',3028:'a',3006:'E',3017:'P',2876:'8',2871:'3'}}}
# SymbolMT glyphs 117 and 118 visually read as multiplication and proportionality.
GLYPHS['scheme']['SymbolMT']={117:'×',118:'∝'}
VERIFIED_LINES=[]
QUESTION_TOTALS={**{n:40 for n in range(1,5)},**{n:56 for n in range(5,12)},12:112}
PART_TOTALS={(9,'a'):28,(9,'b'):28,**{(11,x):7 for x in 'abcdefgh'},**{(12,x):28 for x in 'abcd'}}
BEST_OF={5:(8,7)}
GROUP_TOTALS={};CHECKSUMS={};ROUTES={}
SCAN_PAGES={'paper':range(2,12)};SELECTION_SCAN=[]
ASK_SCAN_PAGES={'paper':range(2,12)};ASK_EXEMPT=[]
SEC='State Examinations Commission'
DSL='The scheme’s // separates complete alternative answers; do not mix partial answers from different routes.'
CRIT='The scheme prints this marking criterion rather than a model answer.'
def anyn(*args,**kw):
 lead=kw.pop('note_lead',None);row=_anyn(*args,**kw)
 if lead:row['note_lead']=lead
 return row
def P(page,start,end=None,**kw):return Q(page,start,end,**kw)
def R(text,marks,end=None,**kw):return pt(S(text,end),marks,**kw)
def C(text,marks,end=None,**kw):
 note=kw.pop('note','');return pt(S(text,end),marks,kind='criterion',note=CRIT+' '+note,**kw)
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
STEM1=P(2,'An experiment was set up to verify Boyle’s law.')
STEM2=P(2,'An experiment was set up to establish the calibration curve of a thermometer.')
STEM3=P(3,'An experiment was set up to investigate how the fundamental frequency of a stretched','The length l and the frequency f of the string were recorded.')
STEM4=P(3,'An experiment was set up to find the resistivity of the material of a wire.')
CANNON=P(5,'The cannon recoils when a cannon ball is shot','from it.')
CARS=P(5,'Bumper car A of mass 500 kg is moving with a speed of 6 m s⁻¹ when it collides with','stationary bumper car B of mass 300 kg. After the collision the cars move together.')
HEAT=P(6,'The temperature of an object can be measured using a thermometer.')
RODS=P(6,'The diagram shows an apparatus used to compare heat transfer in different metals.')
WAVE=P(6,'Diffraction and interference are properties associated with waves.')
LCD=P(6,'The photograph shows a liquid crystal display (LCD) monitor, which may require a','polaroid panel to allow the image on the screen to be seen clearly.')
COLOURS=P(6,'Monitors of the kind shown use only three colours to form any image.')
SCOPE=P(7,'The diagram shows a positively charged gold leaf electroscope.')
EARTH=P(7,'What is observed when the cap of a charged electroscope is earthed?')
CIRCUIT=P(7,'The circuit diagram shows two resistors connected in series with a 3 V battery.')
XRAY=P(8,'X‐rays are produced when a beam of high speed electrons collides with a target in a tube','like the one shown.')
DEVICE=P(8,'Name another device that uses a beam of high speed electrons.')
PASSAGE=P(9,'The Physics of Surfing','Adapted from http://illumin.usc.edu/index/article/193/the‐engineering‐behind‐surfing/ (University of Southern California)')
TRAIN=P(10,'A train left a station and accelerated from rest at 0.4 m s⁻² to reach its top speed of','55 m s⁻¹. The train then travelled for 300 seconds at this speed.')
SUN=P(10,'Sunlight is made up of visible light of different colours as well as many types of','invisible radiation.')
BOILER=P(11,'The diagram shows a water boiler which is filled with 0.7 kg of','of 3 kW.')
SHC=P(11,'(specific heat capacity of water = 4200 J kg⁻¹ K⁻¹)')
COIL=P(11,'Explain how you would use a magnet and a coil, as shown above, to produce','electricity.')
FIGURES={}

# Section A: independently priced laboratory tasks and complete data tables.
A('1i','Q1(i)',2,'Draw a labelled diagram of the apparatus used in this experiment.',3,
 [R('enclosed volume of gas / air',6),anyn(None,2,3,options=[S('method of measuring volume e.g. volume scale'),S('method of measuring pressure e.g. pressure gauge'),S('method of varying pressure / volume')],note_sel=S('NOTE: no labels, deduct 2, incorrect experiment maximum mark 3× 3'))],
 'phys-u2','boyle-apparatus',12,stem=[STEM1])
A('1ii','Q1(ii)',2,'How were the pressure and volume measured?',3,
 [anyn(None,2,6,steps=[6,3],options=[S('measure the pressure from the pressure gauge'),S('measure the volume of trapped air from the scale on the tube')],note_sel=S('partial answer'),note='Both correct: 9; one: 6; partial: 3.')],'phys-u2','boyle-measurements',9,stem=[STEM1],fig='q1-data')
A('1iii','Q1(iii)',2,'Copy and complete the table.',3,
 [C('one mark for filling in each 1/volume including value given',6,units=[1]*6)],'phys-u2','reciprocal-volume-table',6,stem=[STEM1],qfig='q1iii-question',fig='q1iii-solution',notes='The scheme gives one mark for each of the six reciprocal values, including the 0.25 already printed in the paper.')
A('1iv','Q1(iv)',2,'Explain how the data can be used to verify Boyle’s law.',3,
 [pt(S('use the data to draw a graph of p versus 1/V'),3,route='graph',note=DSL),pt(S('(straight) line through origin /shows that pressure ∝ 1/volume // =constant',piece=1,psep='//'),3,route='graph'),pt(S('// pV',piece=2,psep='//'),3,route='product'),pt(S('(straight) line through origin /shows that pressure ∝ 1/volume // =constant',piece=2,psep='//'),3,route='product')],
 'phys-u2','verifying-boyle-law',6,stem=[STEM1],fig='q1-data')
A('1v','Q1(v)',2,'State two precautions which the student might have taken to improve the',3,
 [anyn(None,2,4,steps=[4,3],options=[S(t) for t in ['after changing pressure wait a short time','ensure constant temperature','read the volume of the oil from the bottom of the meniscus','read the volume scale at eye level/no parallax','take many readings','safety precaution e.g. do not exceed the pressure limit of the apparatus, etc.']],open_list=True,note='Any two: 7; any one: 4.')],
 'phys-u2','boyle-precautions',7,end='accuracy of this experiment.',stem=[STEM1])
TASKS.append(T('2i','Q2(i)','A',P(2,'Draw a labelled diagram of the apparatus used in this experiment.',nth=2),
 [anyn(None,4,3,options=[S(t) for t in ['beaker of water','standard thermometer','uncalibrated thermometer','heat source','means of recording thermometric property','detail to improve the accuracy e.g. stirrer']],note_sel=S('NOTE: no labels, deduct 2, incorrect experiment maximum mark 3× 3'))],
 'phys-u2','calibration-apparatus',SQ(4,'Draw a labelled diagram of the apparatus used in this experiment'),12,stem=[STEM2]))
A('2ii','Q2(ii)',2,'What measurements were taken during this experiment?',4,
 [anyn(None,2,6,steps=[6,3],options=[S('thermometric property'),S('temperature')],note_sel=S('partial answer e.g. using ohmmeter / multimeter / metre stick, etc.'),note='Both correct: 9; one: 6; partial: 3.')],'phys-u2','calibration-measurements',9,stem=[STEM2])
A('2iii','Q2(iii)',2,'Use the data in the table to draw a graph, on graph paper, to establish the',4,
 [C('label axes correctly, (name / symbol / unit acceptable)',3),C('plot three points correctly',3),C('plot another three points correctly',3),pt(S('smooth curve'),3,kind='criterion',note_sel=S('if graph paper is not used, maximum mark 3 × 3','if temperature is on the Y‐axis, maximum mark 3 × 3'))],
 'phys-u2','calibration-graph',12,end='calibration curve. Put temperature on the horizontal (X) axis.',stem=[STEM2],qfig='q2iii-question',fig='q2-graph')
A('2iv','Q2(iv)',2,'Use your graph to determine the temperature when the value of the',4,
 [R('answer consistent with graph e.g. 48( °C )',7,note_sel=S('partial e.g. evidence of using the graph (at thermometric property 75)'),note='Partial credit: 4.')],
 'phys-u2','reading-calibration-graph',7,end='thermometric property is 75.',stem=[STEM2,P(2,'Use the data in the table to draw a graph, on graph paper, to establish the','calibration curve. Put temperature on the horizontal (X) axis.')],fig='q2-data')
A('3i','Q3(i)',3,'Draw a labelled diagram of the apparatus used in this experiment.',5,
 [anyn(None,4,3,options=[S(t) for t in ['string','means of tightening','means of changing frequency e.g. tuning forks / frequency generator','means of varying length e.g. bridge','means of measuring length','means of detecting resonance /paper rider /magnet','detail e.g. sonometer']],note_sel=S('NOTE: no labels, deduct 2, incorrect experiment maximum mark 3× 3'))],
 'phys-u2','string-apparatus',12,stem=[STEM3])
A('3ii','Q3(ii)',3,'Indicate on your diagram the length of the string that was measured.',5,
 [R('distance between bridges',6,**partial(6,3))],'phys-u2','string-length',6,stem=[STEM3,P(3,'Draw a labelled diagram of the apparatus used in this experiment.')],sq=SQ(5,'Indicate on your diagram the length of the string that was measured'))
A('3iii','Q3(iii)',3,'Describe how the string was set vibrating.',5,
 [menu('placed a vibrating tuning fork on the bridge // turned on frequency generator',1,6,**partial(6,3))],'phys-u2','vibrating-string',6,stem=[STEM3])
A('3iv','Q3(iv)',3,'How was the frequency of the string determined?',5,
 [R('(read the value) from the tuning fork/ frequency generator',7,**partial(7,4))],'phys-u2','string-frequency',7,stem=[STEM3])
A('3v','Q3(v)',3,'Sketch a graph to show the relationship between l and f that you would expect to',5,
 [anyn(None,1,9,options=[S('f versus 1/l'),S('f versus l')],note_sel=S('graph with one error','partial answer e.g. graph with one axis correctly labelled'),note='Either correctly shaped and labelled graph: 9; one error: 6; partial: 3.')],
 'phys-u2','string-frequency-graph',9,end='obtain.',sq=SQ(5,'Sketch a graph to show the relationship between l and f that you would','expect to obtain.'),stem=[STEM3],fig='q3-graphs')
TASKS.append(T('4i','Q4(i)','A',P(3,'Draw a labelled diagram of the apparatus used in this experiment.',nth=2),
 [R('length of wire',6),R('means of measuring resistance',3),R('means of measuring length/diameter/cross‐sectional area',3,note_sel=S('NOTE: no labels, deduct 2, incorrect experiment maximum mark 3× 3'))],
 'phys-u2','resistivity-apparatus',SQ(6,'Draw a labelled diagram of the apparatus used in this experiment.'),12,stem=[STEM4]))
A('4ii','Q4(ii)',3,'What measurements were taken during this experiment?',6,
 [anyn(None,3,6,steps=[6,3,3],options=[S('length'),S('resistance'),S('diameter /cross‐sectional area')],note_sel=S('partial answer e.g. ohmmeter / micrometer'),note='Three correct: 12; two: 9; one: 6; partial: 3.')],
 'phys-u2','resistivity-measurements',12,stem=[STEM4])
A('4iii','Q4(iii)',3,'How were these measurements used to calculate the resistivity?',6,
 [FR(6,(94,380,112,404),'RA/l',9,note_sel=S('one error in formula','partial answer e.g. substitute the measurements into the formula'),note='Correct formula: 9; one error: 6; partial: 3.')],
 'phys-u2','resistivity-calculation',9,stem=[STEM4,P(3,'What measurements were taken during this experiment?')],fig='q4-formula')
A('4iv','Q4(iv)',3,'State two precautions which the student might have taken to improve the',6,
 [anyn(None,2,4,steps=[4,3],options=[S(t) for t in ['remove kinks from wire','repeat the diameter measurement / take many readings (and get an average)','use a long length','ensure the resistance of the leads connecting to the ohmmeter is low','check for zero error in micrometer, etc.']],open_list=True,note='Any two: 7; one: 4.')],
 'phys-u2','resistivity-precautions',7,end='accuracy of this experiment.',stem=[STEM4])

# Every Q5 option, including the complete instrument list in (c).
A('5a','Q5(a)',4,'State Newton’s first law of motion.',7,[R('a body will remain at rest or moving at a constant velocity unless an external',7,end='force acts on it.',kind='point',**partial(7,4))],'phys-1-2','newton-first-law',7)
A('5b','Q5(b)',4,'Calculate the refractive index of the glass block shown in the diagram.',7,[G('tokens',page=7,clip=(178,197,204,219),expect='1.52',marks=7,**partial(7,4))],'phys-2-3','glass-refraction',7,qfig='q5b-question',fig='q5b-solution')
A('5c','Q5(c)',4,'Choose from the list below the instrument used to measure (i) energy and',7,
 [anyn(None,2,4,steps=[4,3],options=[G('tokens',page=7,clip=(177,319,260,333),expect='(i) joulemeter'),G('tokens',page=7,clip=(304,319,373,333),expect='(ii) ohmmeter')],note_sel=S('one correct.'),note='Both correct: 7; one: 4.')],
 'phys-3-3','measuring-instruments',7,end='barometer joulemeter lens ohmmeter',sq=SQ(7,'Choose from the list below the instrument used to measure (i) energy and','(ii) resistance.'),decision='Two required headings under one stepped 7/4 tariff; retain the full four-instrument choice list in one card.')
A('5d','Q5(d)',4,'State one use for a semiconductor diode.',7,[menu('allows current flow in one direction, rectifier, LED, switches, p.s.u., etc.',1,7,sep=',',open_list=True,**partial(7,4))],'phys-3-3','diode-use',7)
A('5e','Q5(e)',4,'State one use for the instrument shown.',7,[menu('measure angles/ measure wavelength of light /',1,7,end='demonstrate spectra / demonstrate monochromatic light , etc.',sep='/',open_list=True,**partial(7,4))],'phys-2-4','spectrometer-use',7,fig='q5e-spectrometer')
A('5f','Q5(f)',4,'Define capacitance.',7,[FR(7,(93,481,126,503),'C= q/V',7,**partial(7,4))],'phys-3-2','capacitance-definition',7,fig='q5f-capacitance')
A('5g','Q5(g)',4,'State two characteristics of a musical note.',7,[menu('loudness, amplitude, pitch, frequency, overtone, timbre/quality',2,4,sep=',',steps=[4,3],note='Any two: 7; one: 4.')],'phys-2-5','musical-note-properties',7)
A('5h','Q5(h)',4,'Sketch the magnetic field around a bar magnet.',7,[C('magnet, two field lines, correct direction on lines',7,**partial(7,4))],'phys-3-4','bar-magnet-field',7,fig='q5h-field')
A('5i','Q5(i)',4,'Name two sources of ionising radiation.',7,[anyn(None,2,4,steps=[4,3],options=items(S('sun, cosmic, named radioactive element, nuclear weapons,','nuclear power plants, etc.'),5),open_list=True,note='Any two: 7; one: 4.')],'phys-4-4','ionising-sources',7)
A('5j','Q5(j)',4,'State one application of the photoelectric effect.',7,[anyn(None,1,7,options=items(S('solar panels, burglar alarms, automatic doors, control of burners in central','heating, soundtrack in films, etc.'),5),open_list=True,**partial(7,4))],'phys-4-2','photoelectric-application',7)

# Q6: separately priced definitions; each-car calculations remain paired at 6+3.
for key,piece,ans,concept in [('momentum',1,'mass(multiplied) by velocity / p = mv','momentum-definition'),('kinetic-energy',2,'kinetic energy: energy due to motion //½mv²','kinetic-energy-definition')]:
 TASKS.append(T('6def-'+key,'Q6','B',P(5,'Define (i) momentum and (ii) kinetic energy.',piece=piece,psep=' and '),
 [R(ans,6,whole=True,**partial(6,3))],'phys-1-2' if key=='momentum' else 'phys-1-4',concept,SQ(8,'Define (i) momentum and (ii) kinetic energy.',paired='The scheme reprints both separately priced six-mark definitions together.'),6,item=(key+'-definition',key.replace('-',' ').capitalize()+' definition'),cells='The joint reprint is 2(6 or 3); each definition has its own six-mark answer cell.'))
A('6recoil','Q6',5,'Use the principle of conservation of momentum',8,[menu('cannon recoils to ensure the momentum after is zero //to conserve momentum',1,6,end='/momentum before collision = momentum after collision',**partial(6,3))],'phys-1-2','cannon-recoil',6,end='to explain why the cannon recoils.',sq=SQ(8,'Use the principle of conservation of momentum to explain why the cannon recoils.'),stem=[CANNON],fig='q6-cannon',item=('recoil','Cannon recoil'))
A('6i','Q6(i)',5,'Calculate the momentum of each car before the collision.',8,
 [anyn(None,2,6,steps=[6,3],options=[S('pA= mAvA= (500)(6) = 3000 kg m s⁻¹'),S('pB= mBvB= (300)(0) = 0 kg m s⁻¹')],**partial(9,3,extra='Either complete car calculation earns 6; both earn 9.'))],'phys-1-2','car-momenta-before',9,stem=[CARS],fig='q6-cars')
A('6ii','Q6(ii)',5,'What is the momentum of the combined cars after the collision?',8,[R('(mA + mB)V = mAvA + mBvB = 3000 kg m s⁻¹',6,**partial(6,3))],'phys-1-2','combined-momentum',6,stem=[CARS],fig='q6-cars')
A('6iii','Q6(iii)',5,'Calculate the speed of the two cars after the collision.',8,[R('(mA + mB)V = mAvA + mBvB = 3000 kg m s⁻¹',6,end='⇒ V = 3.75 m s⁻¹',**partial(6,3))],'phys-1-2','collision-speed',6,stem=[CARS],fig='q6-cars')
A('6iv','Q6(iv)',5,'Calculate the kinetic energy of each car before the collision.',8,
 [anyn(None,2,6,steps=[6,3],options=[G('tokens',page=8,clip=(177,573,214,592),expect='9000 J'),G('tokens',page=8,clip=(184,596,201,614),expect='0 J')],**partial(9,3,extra='Either complete car calculation earns 6; both earn 9.'))],
 'phys-1-4','car-energies-before',9,stem=[CARS],fig='q6iv-solutions')
A('6v','Q6(v)',5,'Calculate the kinetic energy of the cars after the collision.',8,[FR(8,(97,657,256,678),'½ MV² = ½ (500+300)(3.75)² = 5625 J',5,**partial(5,3))],'phys-1-4','car-energy-after',5,stem=[CARS],fig='q6v-solution')
A('6vi','Q6(vi)',5,'What conclusion can be drawn from the change in kinetic energy that happens',8,[R('kinetic energy is not conserved / kinetic energy is lost // answer consistent',3,end='with (iv) and (v)')],'phys-1-4','collision-energy-change',3,end='during the collision?',sq=SQ(8,'What conclusion can be drawn from the change in kinetic energy that','happens during the collision?'),stem=[CARS,P(5,'Calculate the kinetic energy of each car before the collision.'),P(5,'Calculate the kinetic energy of the cars after the collision.')],fig='q6-cars')

# Q7–Q8: heat investigations and complete wave demonstrations.
for key,q,ans,concept,part in [
 ('i','What is heat?','(a form of) energy / mcΔθ /ml','heat-definition',3),
 ('ii','What is meant by the temperature of an object?','degree of hotness // measurement of hotness/coldness','temperature-definition',3),
 ('iii','What is the unit of temperature on the SI scale?','kelvin / K','kelvin-unit',3),
 ('iv','Express 20 °C in the units you have named in part (iii).','273+20 = 293 K','celsius-kelvin',3)]:
 A('7'+key,'Q7('+key+')',6,q,9,[R(ans,6,**partial(6,part))],'phys-2-1',concept,6,stem=[HEAT]+([P(6,'What is the unit of temperature on the SI scale?')] if key=='iv' else []))
A('7v','Q7(v)',6,'Name the method by which heat is transferred in metals.',9,[R('conduction // vibrating atoms (transfer energy)',6,**partial(6,3))],'phys-2-1','metal-conduction',6,stem=[RODS],fig='q7-rods')
A('7vi','Q7(vi)',6,'Name the two other methods of heat transfer.',9,[pt(S('convection, radiation',piece=1,psep=','),3),pt(S('convection, radiation',piece=2,psep=','),3,note_sel=S('partial answer e.g. example'),note='Partial credit: 3.')],'phys-2-1','other-heat-transfer',6,stem=[RODS,P(6,'Name the method by which heat is transferred in metals.')],fig='q7-rods')
A('7vii','Q7(vii)',6,'How can this experiment be used to find out which metal is the best at allowing',9,[R('the pin which falls first indicates the best conductor',6,**partial(6,3))],'phys-2-1','best-conductor',6,end='heat transfer?',sq=SQ(9,'How can this experiment be used to find out which metal is the best at','allowing heat transfer?'),stem=[RODS],fig='q7-rods')
A('7viii','Q7(viii)',6,'State two ways of making sure that this investigation is fair.',9,[anyn(None,2,4,options=[S(t) for t in ['ensure that there is only one independent variable','ensure there is an equal amount of heat for each metal','ensure that the metal strips are the same length / diameter','ensure to have the same amount of wax, etc.']],open_list=True)],'phys-2-1','fair-conduction-test',8,stem=[RODS],fig='q7-rods')
A('7ix','Q7(ix)',6,'Metals are good conductors. Name a good insulator.',9,[R('any named insulator e.g. paper, plastic, wood, etc.',6,**partial(6,3))],'phys-2-1','thermal-insulator',6,stem=[RODS],fig='q7-rods')
A('8i','Q8(i)',6,'Explain the underlined terms.',10,[R('diffraction is the bending/spreading out of waves around a barrier / the',6,end='edges of an opening // correct diagram',**partial(6,3)),R('interference occurs when two waves meet and add // correct diagram',6,note_sel=S('reversed explanations'),note='Reversed explanations: 6 for this task.')],'phys-2-6','diffraction-interference',12,stem=[WAVE],qfig='q8i-question',decision='Both required underlined terms share one printed roman task, 6 each; no finite choice.')
A('8ii','Q8(ii)',6,'Describe an experiment to demonstrate the wave nature of light.',10,[R('apparatus: (diffraction) grating / Young’s slits / CD',6),R('procedure: shine the light through the grating /Young’s slits / CD',3),R('observation/conclusion; pattern on screen / pattern observed',3,note_sel=S('incorrect experiment maximum mark 2 × 3','accept valid alternatives'))],'phys-2-6','wave-nature-demonstration',12,stem=[WAVE])
A('8iii','Q8(iii)',6,'What is meant by polarisation?',10,[R('polarisation is the restriction of (vibrating electromagnetic) waves to',6,end='a single plane',note_sel=S('marks may be obtained from a diagram','partial answer'),note='Partial credit: 3.')],'phys-2-6','polarisation-definition',6,stem=[LCD],fig='q8-monitor')
A('8iv','Q8(iv)',6,'Describe an experiment to demonstrate the polarisation of light.',10,[R('apparatus: (two pieces of a) polaroid sheet',3),R('procedure: look at the light through the two pieces of polaroid',3),R('rotate one of the polaroid pieces',3),R('observation/conclusion; the crossed pieces stop the light',3,note_sel=S('marks may be obtained from a diagram','accept valid alternatives'))],'phys-2-6','polarisation-demonstration',12,stem=[LCD],fig='q8-monitor')
A('8v','Q8(v)',6,'What three colours are used?',10,[menu('red, green, blue',3,3,sep=',',note_sel=S('partial answer e.g. the primary colours'),note='Partial credit: 3.')],'phys-2-4','primary-colours',9,stem=[LCD,COLOURS],fig='q8-monitor')
A('8vi','Q8(vi)',6,'Describe how these colours can be used to create any image.',10,[R('these colours may be mixed (to give white light/ other colours)',5,**partial(5,3))],'phys-2-4','mixing-colours',5,stem=[LCD,COLOURS,P(6,'What three colours are used?')],fig='q8-monitor')

# Q9: every charge and circuit task carries its labelled source apparatus.
A('9ai','Q9(a)(i)',7,'State Coulomb’s law of force between charges.',11,[R('force proportional to the product of charges / F ∝ Q₁Q₂',3),pt(S('inversely proportional to the distance between the charges squared /',piece=1,psep=' /'),3,kind='point',note_sel=S('partial answer'),note='Partial credit: 3. The source equation is shown with the complete inverse-square relation.')],'phys-3-2','coulomb-law',6,stem=[SCOPE],fig='q9ai-law')
A('9aii','Q9(a)(ii)',7,'State one use of an electroscope.',11,[anyn(None,1,3,options=items(S('test for charge, identify charge, measure potential, etc.'),3),open_list=True)],'phys-3-2','electroscope-use',3,stem=[SCOPE],fig='q9a-electroscope')
A('9aiii','Q9(a)(iii)',7,'How can an electroscope be given a positive charge?',11,[menu('touch the cap with a positively charged conductor //',1,6,end='earth before removing the rod',note_sel=S('accept valid alternatives e.g. Van De Graaff','partial answer'),note='Partial credit: 3.')],'phys-3-2','positive-electroscope',6,stem=[SCOPE],fig='q9a-electroscope')
A('9aiv','Q9(a)(iv)',7,'What is observed when the cap of a charged electroscope is earthed?',11,[R('the leaves collapse/converge / fall',3)],'phys-3-2','earthing-observation',3,stem=[SCOPE],fig='q9a-electroscope')
A('9av','Q9(a)(v)',7,'Explain this observation.',11,[R('charges move ( between the earth and the cap) // no (excess) charge',6,**partial(6,3))],'phys-3-2','earthing-explanation',6,stem=[SCOPE,EARTH],fig='q9a-electroscope')
A('9avi','Q9(a)(vi)',7,'How could the cap of the electroscope be earthed?',11,[R('by touching with a conductor / finger',4)],'phys-3-2','earthing-method',4,stem=[SCOPE],fig='q9a-electroscope')
A('9bi','Q9(b)(i)',7,'State Ohm’s law.',11,[R('the current through a conductor is directly proportional to the voltage /',6,end='V=IR',**partial(6,3))],'phys-3-3','ohm-law',6,stem=[CIRCUIT],fig='q9b-circuit')
A('9bii','Q9(b)(ii)',7,'Calculate the total resistance of the circuit.',11,[R('(6 + 12 = ) 18 Ω',6,**partial(6,3))],'phys-3-3','series-resistance',6,stem=[CIRCUIT],fig='q9b-circuit')
A('9biii','Q9(b)(iii)',7,'Calculate the current in the circuit.',11,[FR(11,(111,639,195,663),'I = V/R = 0.166 A',6,note='The printed scheme gives 6 for the complete calculation and 3 for the partial formula I = V/R.')],'phys-3-3','series-current',6,stem=[CIRCUIT],fig='q9b-circuit')
A('9biv','Q9(b)(iv)',7,'Calculate the potential difference across the 6 Ω resistor.',11,[R('( V = IR = (0.166)(6) = ) 1 V',6,**partial(6,3))],'phys-3-3','resistor-voltage',6,stem=[CIRCUIT],fig='q9b-circuit')
A('9bv','Q9(b)(v)',7,'Name an instrument used to measure potential difference.',11,[R('voltmeter /multimeter',4,**partial(4,2))],'phys-3-3','voltmeter',4,stem=[CIRCUIT],fig='q9b-circuit')

# Q10's two separately priced sentences are independent six-mark tasks.
A('10i-definition','Q10(i)',8,'What are X‐rays?',12,[R('electromagnetic waves // high energy radiation',6,**partial(6,3))],'phys-4-2','xray-definition',6,end='What are X‐rays?',sq=SQ(12,'What are X‐rays? State two properties of X‐rays.'),stem=[XRAY],fig='q10-tube',item=('definition','X-ray definition'),cells='Scheme p12 prints separate six-mark definition and properties answers under the combined reprint.')
A('10i-properties','Q10(i)',8,'State two properties of X‐rays.',12,[anyn(None,2,3,options=items(S('short wavelength, cause ionisation, affect photographic plates, absorbed','by bone/metal, no charge, etc.'),5),open_list=True,note_sel=S('partial answer e.g. reference to photograph / medicine / industry, etc.'),note='Partial credit: 3.')],'phys-4-2','xray-properties',6,sq=SQ(12,'What are X‐rays? State two properties of X‐rays.'),stem=[XRAY],fig='q10-tube',item=('properties','Two X-ray properties'),cells='Scheme p12 prints any two at 3 each, independently of the six-mark definition.')
for key,q,ans,total,topic,concept,end,sep in [
 ('ii','What process occurs at part A?','thermionic emission // release of electrons // heating',6,'phys-4-1','thermionic-emission',None,'//'),
 ('iii','Name a substance used in part B.','tungsten, molybydenium, named metal',4,'phys-4-2','xray-target',None,','),
 ('iv','State the function of part C.','prevent escape of X‐rays, shielding, protect (from X‐rays), etc.',6,'phys-4-2','xray-shield',None,','),
 ('v','State one use of X‐rays.','to photograph bones/ internal organs, to treat cancer, to detect flaws',4,'phys-4-2','xray-use','in materials, to determine the thickness of materials, etc.',','),
 ('vi','Why is a vacuum needed inside an X‐ray tube?','so the electrons won’t collide and lose energy // allow electrons to',6,'phys-4-2','xray-vacuum','speed up more efficiently','//'),
 ('vii','Name another device that uses a beam of high speed electrons.','cathode ray tube, fluorescent light',6,'phys-4-1','electron-beam-device',None,','),
 ('viii','State one use for the device you have named in part (vii).','CRO, medical devices, (old) TVs/screens',6,'phys-4-1','electron-beam-use',None,','),
 ('ix','State one difference between X‐rays and gamma‐rays.','different ways of production, different energy / wavelength /frequency',6,'phys-4-4','xray-gamma-difference','/ penetration / ionising/ etc.',' / ')]:
 A('10'+key,'Q10('+key+')',8,q,12,[menu(ans,1,total,end=end,sep=sep,open_list=True,**partial(total,2 if total==4 else 3))],topic,concept,total,stem=[XRAY]+([DEVICE] if key=='viii' else []),fig='q10-tube')

# Q11 retains the entire source passage on every card, including the stance image.
for key,q,ans,end,topic,concept in [
 ('a','What physical quantity is transmitted in a wave?','energy',None,'phys-2-6','wave-energy'),
 ('b','Why do waves break close to the shore?','the wavelength decreases and the wave height (amplitude) increases //','waves move into shallow water until the wave becomes unstable and breaks','phys-2-6','breaking-waves'),
 ('d',"State Archimedes' principle.",'when a body is immersed in a fluid , the upthrust it experiences is equal','it displaces its own weight of the fluid','phys-1-4','archimedes-principle'),
 ('e','What is meant by the term buoyancy (upthrust)?','an upward force exerted by a fluid',None,'phys-1-4','buoyancy-definition'),
 ('f','How does buoyancy help the surfer to stay afloat?','counterbalances the weight',None,'phys-1-4','floating-surfer'),
 ('h','Explain how the stance of the surfer shown helps her to balance.','low centre of gravity // wide stance',None,'phys-1-3','surfer-balance')]:
 A('11'+key,'Q11('+key+')',9,q,13,[R(ans,7,end=end,**partial(7,4))],topic,concept,7,stem=[PASSAGE],fig='q11-surfer')
A('11c','Q11(c)',9,'Draw a diagram to show the main features of a wave.',13,[C('diagram to include',7,end='wavelength /amplitude /crest /trough etc.',**partial(7,4))],'phys-2-6','wave-features',7,stem=[PASSAGE],fig='q11c-wave')
A('11g','Q11(g)',9,'Draw a labelled diagram to show the forces acting on a floating object.',13,[anyn(None,2,4,steps=[4,3],options=items(S('diagram to show: weight down, upthrust up, forward force',piece=2,psep=':'),3),note_sel=S('partial answer e.g. one force shown'),note='Draw and label any two forces: 7; one: 4.')],'phys-1-4','floating-force-diagram',7,stem=[PASSAGE],fig='q11-surfer',decision='The scheme explicitly accepts any two of its three listed forces; preserve three options and the stepped 7/4 tariff.')

# Q12: all four options, each 28 marks, with complete physical quantities.
for key,piece,clip,expect,concept in [
 ('i',1,(88,107,253,128),'displacement per second / v = s/t','velocity-definition'),
 ('ii',2,(88,138,283,159),'change in velocity per unit time /a = (v−u)/t','acceleration-definition')]:
 TASKS.append(T('12a'+key,'Q12(a)('+key+')','B',P(10,'Define (i) velocity and (ii) acceleration.',piece=piece,psep=' and '),[FR(14,clip,expect,5,**partial(5,3))],'phys-1-1',concept,SQ(14,'Define (i) velocity and (ii) acceleration.',paired='The scheme reprints the two separately numbered and priced definitions together.'),5,cells='Each definition is explicitly five marks in the 2(5 or 3) scheme.'))
A('12aiii','Q12(a)(iii)',10,'Calculate how long it took the train to reach its top speed.',14,[FR(14,(91,222,218,244),'( t = (v−u)/a = (55−0)/0.4 = ) 137.5 s',6,**partial(6,3))],'phys-1-1','train-acceleration-time',6,stem=[TRAIN],fig='q12aiii-solution')
A('12aiv','Q12(a)(iv)',10,'How far did the train travel while at its top speed?',14,[R('[ s=vt =(300)(55) =] 16500 m',6,note_sel=S('partial mark e.g. s= vt'),note='Partial credit: 3.')],'phys-1-1','train-distance',6,stem=[TRAIN])
A('12av','Q12(a)(v)',10,'Draw a velocity‐time graph of the train’s journey.',14,[C('correct shape with axes',6,**partial(6,3))],'phys-1-1','train-velocity-time-graph',6,stem=[TRAIN],fig='q12av-graph')
A('12bi','Q12(b)(i)',10,'How could you show the different colours present in visible light?',14,[R('apparatus: (white light source, screen), prism/CD/grating',6),R('shine the light through the prism/CD/grating',3,note_sel=S('partial answer','accept valid alternatives'),note='Partial credit: 3.')],'phys-2-4','spectrum-demonstration',9,stem=[SUN])
A('12bii','Q12(b)(ii)',10,'UV radiation is also present in sunlight.',14,[R('ultraviolet',6,**partial(6,3))],'phys-2-4','uv-meaning',6,end='What do the letters U and V stand for?',stem=[SUN])
A('12biii','Q12(b)(iii)',10,'Compare the wavelength of UV radiation to the wavelength of',14,[R('ultraviolet has a shorter wavelength',3)],'phys-2-4','uv-infrared-wavelength',3,end='infra‐red (IR) radiation.',stem=[SUN])
A('12biv','Q12(b)(iv)',10,'Describe how to detect UV radiation.',14,[R('florescent material will fluoresce/glow',6,note_sel=S('partial answer','a labelled diagram may merit full marks'),note='Partial credit: 3.')],'phys-2-4','uv-detection',6,stem=[SUN])
A('12bv','Q12(b)(v)',10,'State one use of UV radiation.',14,[anyn(None,1,4,options=items(S('detect forged currency, disco lights, used in insect removal device,','sterilisation, suntan, forensics, etc.'),6),open_list=True,**partial(4,2))],'phys-2-4','uv-use',4,stem=[SUN])
A('12ci','Q12(c)(i)',11,'Calculate the energy needed to raise the temperature of',15,[R('E = mcΔθ = (0.7)(4200)(90‐20) = 205800 J',12,note_sel=S('one error','partial answer e.g. correct formula'),note='One error: 9; two errors: 6; partial: 3.')],'phys-2-1','boiler-heat',12,end='the water from 20 °C to 90 °C.',sq=SQ(15,'Calculate the energy needed to raise the temperature of','the water from 20 °C to 90 °C.'),stem=[BOILER,SHC],fig='q12c-boiler')
A('12cii','Q12(c)(ii)',11,'How many joules of energy are supplied per second by',15,[R('3000',4,**partial(4,2))],'phys-1-4','boiler-power',4,end='the boiler?',sq=SQ(15,'How many joules of energy are supplied per second by the boiler?'),stem=[BOILER],fig='q12c-boiler')
A('12ciii','Q12(c)(iii)',11,'Calculate how long it will take the boiler to heat the',15,[FR(15,(90,240,240,262),'E = Pt ⇒ t = E/P = 205800/3000 = 68.6 s',6,**partial(6,3))],'phys-2-1','boiler-heating-time',6,end='water to 90 °C.',sq=SQ(15,'Calculate how long it will take the boiler to heat the water to 90 °C.'),stem=[BOILER,SHC],fig='q12ciii-solution')
A('12civ','Q12(c)(iv)',11,'Where should the manufacturer place the heating',15,[R('at the bottom',3),R('hot water (is less dense and) rises',3,**partial(6,3))],'phys-2-1','boiler-element-location',6,end='element of the boiler? Explain your answer.',sq=SQ(15,'Where should the manufacturer place the heating element of the','boiler? Explain your answer.'),stem=[BOILER],fig='q12c-boiler',decision='Location with its reason is one six-mark paired response, priced 3+3.')
A('12di','Q12(d)(i)',11,'What is electromagnetic induction?',15,[R('emf / voltage / potential difference / current is induced',3),R('(due to)changing (magnetic) flux / field // moving magnet',3,note_sel=S('partial answer','a diagram or example may merit full marks'),note='Partial credit: 3.')],'phys-3-6','induction-definition',6)
A('12dii','Q12(d)(ii)',11,'Explain how you would use a magnet and a coil, as shown above, to produce',15,[R('move the magnet into/out of the coil',6,**partial(6,3))],'phys-3-6','induction-procedure',6,end='electricity.',sq=SQ(15,'Explain how you would use a magnet and a coil, as shown above,','to produce electricity.'),fig='q12d-coil')
A('12diii','Q12(d)(iii)',11,'How would you know that electricity is being produced?',15,[R('deflection /pointer moves / from the meter',6,**partial(6,3))],'phys-3-6','induction-observation',6,stem=[COIL],fig='q12d-coil')
A('12div','Q12(d)(iv)',11,'How could you increase the magnitude of the electricity produced?',15,[menu('move faster / use a stronger magnet / use more coils',1,6,sep=' / ',**partial(6,3))],'phys-3-6','stronger-induced-current',6,stem=[COIL],fig='q12d-coil')
A('12dv','Q12(d)(v)',11,'The apparatus in the diagram can be used to produce a.c. electricity.',15,[R('alternating current',4,**partial(4,2))],'phys-3-6','alternating-current',4,end='What is meant by a.c.?',fig='q12d-coil')

SELECTION_SCAN=[
 ('paper',4,'the following','Best eight of ten separately carded short questions; all ten retained.'),
 ('paper',4,'choose','Q5(c): two required instruments from the complete four-instrument list, one stepped 7/4 card.'),
 ('paper',9,'the following','Passage instruction; all eight questions carry the complete passage.'),
 ('paper',9,'both','Passage description of the surfboard and surfer; no choice.'),
 ('paper',9,'both','Passage description of the surfboard and surfer; no choice.'),
 ('paper',10,'any two','All four differently marked/topic Q12 options carded independently; no combinations.'),
 ('paper',10,'the following','Same Q12 any-two directive; all four options retained.')]

# Source crops retain table headings, axes, all labels and required context.
FIGURES={
 'q1-data':('paper',2,(145,300,456,352),SEC,[],'Boyle’s law pressure and volume table with six readings and the supplied reciprocal value.',False),
 'q1iii-question':('paper',2,(82,202,537,408),SEC,[],'Boyle’s law context, full six-reading table and instruction to copy and complete it.',False,[(82,238,537,257),(82,369,537,387)]),
 'q1iii-solution':('scheme',3,(141,419,450,471),SEC,[],'Complete pressure, volume and reciprocal-volume table, including all six scheme values.',True),
 'q2-data':('paper',2,(94,650,514,687),SEC,[],'Temperature and thermometric-property readings for calibration.',False),
 'q2iii-question':('paper',2,(82,528,537,735),SEC,[],'Thermometer calibration context, full data table and graph instruction with temperature on the horizontal axis.',False,[(82,569,537,608)]),
 'q2-graph':('scheme',4,(86,466,491,731),SEC,[],'Official calibration curve, temperature in degrees Celsius horizontally and thermometric property vertically.',True),
 'q3-graphs':('scheme',5,(72,521,410,660),SEC,[],'Both accepted frequency–length graphs: frequency against reciprocal length, or frequency against length.',True),
 'q4-formula':('scheme',6,(94,379,112,404),SEC,[],'Resistivity calculated using the printed resistance times area divided by length formula.',True),
 'q5b-glass':('paper',4,(243,285,331,407),SEC,[],'Refraction at an air–glass boundary with 40-degree incidence and 25-degree refraction.',False),
 'q5e-spectrometer':('paper',4,(402,495,541,592),SEC,[],'The instrument shown in Q5(e).',False),
 'q5f-capacitance':('scheme',7,(91,479,127,504),SEC,[],'Capacitance equals charge divided by voltage.',True),
 'q5h-field':('scheme',7,(82,584,170,653),SEC,[],'Official magnetic-field sketch around the labelled south and north poles.',True),
 'q6-cannon':('paper',5,(326,89,541,174),SEC,[],'Cannon and cannonball illustrating recoil.',False),
 'q6-cars':('paper',5,(145,234,450,351),SEC,[],'The two bumper cars before collision.',False),
 'q6iv-solutions':('scheme',8,(90,567,215,615),SEC,[],'Both official kinetic-energy calculations before collision, retaining fractional coefficients and powers.',True),
 'q6v-solution':('scheme',8,(97,655,258,679),SEC,[],'Official calculation of the combined cars’ kinetic energy after collision.',True),
 'q7-rods':('paper',6,(179,185,410,291),SEC,[],'Hot-water apparatus with copper, aluminium, brass and iron rods, wax and pins labelled.',False),
 'q8i-question':('paper',6,(82,453,537,492),SEC,[],'The underlined terms diffraction and interference and the instruction to explain them.',False),
 'q8-monitor':('paper',6,(214,551,352,656),SEC,[],'The liquid-crystal display monitor shown in the paper.',False),
 'q9a-electroscope':('paper',7,(246,76,325,193),SEC,[],'Positively charged gold-leaf electroscope with charge signs and separated leaves.',False),
 'q9ai-law':('scheme',11,(97,118,441,176),SEC,[],'Both parts of Coulomb’s law, with the printed charge product and inverse-square fraction.',True),
 'q9b-circuit':('paper',7,(203,391,415,521),SEC,[],'Three-volt battery with six-ohm and twelve-ohm resistors connected in series.',False),
 'q10-tube':('paper',8,(136,98,428,240),SEC,[],'Complete X-ray tube with low and high voltages and parts A, B and C.',False),
 'q11-surfer':('paper',9,(419,126,541,306),SEC,[],'The surfer’s stance as shown beside the source passage.',False),
 'q11c-wave':('scheme',13,(350,414,397,486),SEC,[],'Official wave sketch indicating amplitude and wavelength.',True),
 'q12aiii-solution':('scheme',14,(90,221,220,245),SEC,[],'Time to reach top speed, with the velocity difference divided by acceleration.',True),
 'q12av-graph':('scheme',14,(256,322,352,382),SEC,[],'Official velocity–time graph: acceleration from rest followed by constant speed.',True),
 'q12c-boiler':('paper',11,(429,48,541,250),SEC,[],'The water boiler shown in Q12(c).',False),
 'q12ciii-solution':('scheme',15,(90,239,240,262),SEC,[],'Official heating-time calculation: energy divided by power equals 68.6 seconds.',True),
 'q12d-coil':('paper',11,(218,376,363,491),SEC,[],'Magnet, coil and galvanometer apparatus for electromagnetic induction.',False),
}
# Q9(a)(i) asks a general law: its solution image is sufficient without the
# decorative electroscope image. Its stem does not point at an omitted figure.
next(t for t in TASKS if t['key']=='9ai')['stem']=[]

# Final source and curriculum review corrections.
_by={t['key']:t for t in TASKS}
_by['1i']['sq']=SQ(3,'Draw a labelled diagram of the apparatus used in this experiment')
_by['2iii']['sq']=SQ(4,'Use the data in the table to draw a graph, on graph paper, to establish','the calibration curve. Put temperature on the horizontal (X) axis.')
for key,reason in {
 '1ii':'The complete two-measurement response is 9; the standalone (6) is partial credit for any one measurement.',
 '2ii':'The two measurements jointly earn 9; the standalone (6) is partial credit for one measurement.',
 '3v':'Either complete graph is 9; graph with one error is (6), and partial labelling is (3). These are alternative scores.',
 '4ii':'The whole three-measurement response is 12. Standalone (9), (6) and (3) are successive alternative partial scores.',
 '4iii':'The complete formula is 9. One error in the formula earns the separate partial score (6).',
 '8i':'Each of the two definitions earns 6; the separate (6) for reversed explanations is an alternative whole-response score.',
 '12ci':'The correct calculation earns 12. Standalone (9), (6) and (3) are alternative partial scores for one error, two errors and a partial answer.'
}.items():_by[key]['cells']=reason
for t in TASKS:
 q=int(t['ref'].split('(')[0][1:])
 if q<5:t['topic']={1:'phys-1-2',2:'phys-2-1',3:'phys-2-6',4:'phys-3-3'}[q]
for key in ['11d','11e','11f','11g','11h']:_by[key]['topic']='phys-1-2'
for key in ['11a','11b','11c']:_by[key]['topic']='phys-2-2'
_by['9ai']['topic']='phys-3-1'
for key in ['8iii','8iv']:_by[key]['topic']='phys-2-3'
FIGURES.pop('q5b-glass')
FIGURES['q5b-question']=('paper',4,(82,256,461,407),SEC,[],'The refraction question and complete glass diagram with both angles.',False)
FIGURES['q5b-solution']=('scheme',7,(91,195,204,219),SEC,[],'Official refractive-index calculation with the full sine fractions and result 1.52.',True)
_by['5c']['cells']='The instrument pair earns 7. The standalone (4) is the explicitly printed partial score for one correct instrument.'

# Visual crop review: complete enclosure/circuit edges and remove adjacent type.
for key,rect in {
 'q9a-electroscope':(238,76,334,181),
 'q9b-circuit':(196,391,418,521),
 'q3-graphs':(72,521,455,660),
 'q11c-wave':(345,414,430,486),
 'q5f-capacitance':(91,484,127,504),
 'q6v-solution':(97,658,258,679),
 'q12aiii-solution':(90,223,220,245),
 'q12ciii-solution':(90,241,240,263),
}.items():
 f=list(FIGURES[key]);f[2]=rect;FIGURES[key]=tuple(f)
# Each separated inline definition keeps its printed imperative.
_by['6def-kinetic-energy']['q']=[P(5,'Define (i) momentum and (ii) kinetic energy.',piece=1,psep=' (i) '),_by['6def-kinetic-energy']['q']]
_by['12aii']['q']=[P(10,'Define (i) velocity and (ii) acceleration.',piece=1,psep=' (i) '),_by['12aii']['q']]
# An open list's trailing “etc.” is not a selectable answer.
for key,n in [('5d',5),('10iv',3),('10v',4)]:
 row=_by[key]['rows'][0];row['options']=items(row['sel'],n);row['sel']=None
# Preserve the whole explanation menu without presenting a fragment as an answer.
_by['10ix']['rows']=[R('different ways of production, different energy / wavelength /frequency',6,end='/ penetration / ionising/ etc.',**partial(6,3))]
# Car labels printed as subscripts remain visible in the official working.
for key,rect,alt in [
 ('6i',(90,359,291,388),'The two official momentum calculations, with car A and B subscripts.'),
 ('6ii',(90,440,292,455),'The combined momentum equation and result, with car A and B subscripts.'),
 ('6iii',(90,494,321,526),'The complete momentum-conservation calculation leading to 3.75 metres per second.')]:
 fig='q'+key+'-solution';_by[key]['fig']=fig
 FIGURES[fig]=('scheme',8,rect,SEC,[],alt,True)
# Correct nested source slicing for the force-option list.
_by['11g']['rows'][0]['options']=[S('diagram to show: weight down, upthrust up, forward force',piece=[2,i],psep=[':',',']) for i in [1,2,3]]
for key,rect in {'q1-data':(145,300,461,352),'q1iii-solution':(138,419,456,471),'q9a-electroscope':(238,76,345,186)}.items():
 f=list(FIGURES[key]);f[2]=rect;FIGURES[key]=tuple(f)
_by['12ciii']['qfig']='q12ciii-question'
FIGURES['q12ciii-question']=('paper',11,(82,48,541,267),SEC,[],'Boiler illustration, mass, initial temperature, power, specific heat capacity and the heating-time question.',False,[(110,108,429,174),(110,213,429,246)])
# The first fractional equation has a nonstandard word-box grouping. Its exact
# printed working is retained as an image, with the independently read numeric
# results used for the two stepped claim slots; no broken fraction is shipped.
_by['6iv']['decision']='Two required car calculations, with either complete one earning 6 and both 9. Source working is retained visibly; final results are read by position.'
_by['5b']['decision']='The complete official sine-fraction working is retained visibly; its final result is read by position to avoid malformed bracket extraction.'
for key in ['6i','6iv']:
 _by[key]['rows'][0]['note_lead']='The scheme also allows partial credit:'
