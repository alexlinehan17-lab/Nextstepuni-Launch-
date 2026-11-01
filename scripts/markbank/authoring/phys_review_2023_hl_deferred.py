"""2023 Higher deferred Physics: independent visual review of all 16 paper and 20 scheme pages.
The terse scheme has no question reprints. Match the visually checked printed
question/part path, retain shared tariffs, and never invent per-response marks.
"""
from phys_review_lib import Q,SQ,S,G,pt,anyn,allof,T,L,M
YEAR,LEVEL,SITTING=2023,'hl','deferred'
REVIEWED_AT='2026-11-01'
LETTERED={6,12,13,14}
SOURCES={'paper': {'path': 'paper-trail-corpus/deferredexams/2023/LC021ALP000EV.pdf', 'fileid': 'LC021ALP000EV.pdf', 'sha256': '03a43dee1fa12ae6f17a3cff6640e07dce70260dd9cfc7c58bea3a10f4e868e3', 'pages': 16}, 'scheme': {'path': 'paper-trail-corpus/deferredmarkingschemes/2023/LC021ALP000EV.pdf', 'fileid': 'LC021ALP000EV.pdf', 'sha256': '6de7c758d0ea1006e85ac3032892eee934e65fbc860bb28147984dc0e120f52e', 'pages': 20}}
PAGE_ROLES={'paper':{1:'cover',**{p:'questions' for p in range(2,16)},16:'back-cover'},'scheme':{1:'cover',2:'deferred-guidance',**{p:'marking' for p in range(3,19)},19:'blank',20:'back-cover'}}
# All 135 first-occurrence special-font/non-ASCII glyphs visually checked.
GLYPHS={'paper': {'Calibri': {386: 'ö', 591: 'Ω', 858: '‘', 859: '’', 882: '‐', 884: '–', 931: '°', 1066: '½', 1087: '×', 1106: 'µ'}, 'Calibri-Italic': {564: 'Δ', 652: 'ρ', 882: '‐', 884: '–', 931: '°', 1086: '−'}, 'Cambria': {514: '–', 1372: '→'}, 'Cambria-Bold': {158: 'á', 239: 'ú', 514: '–'}, 'SymbolMT': {84: 'θ'}, 'TimesNewRomanPS-ItalicMT': {537: 'θ'}}, 'scheme': {'Calibri': {591: 'Ω', 630: 'γ', 637: 'θ', 644: 'λ', 652: 'ρ', 664: 'ω', 859: '’', 884: '–', 931: '°', 1066: '½', 1087: '×', 3512: '°'}, 'Calibri-Italic': {564: 'Δ', 862: '“', 863: '”', 884: '–'}, 'Cambria': {958: '√', 1372: '→', 1503: '∝', 1827: 'A', 1828: 'B', 1829: 'C', 1834: 'H', 1846: 'T', 1847: 'U', 1855: 'c', 1857: 'e', 1858: 'f', 1859: 'g', 1860: 'h', 1865: 'm', 1871: 's', 1872: 't', 1873: 'u', 1878: 'z', 2024: 'π', 2025: 'ρ', 2038: 'φ', 2868: '0', 2869: '1', 2870: '2', 2871: '3', 2872: '4', 2873: '5', 2874: '6', 2875: '7', 2876: '8', 2877: '9', 2878: '+', 2879: '−', 2919: 'i', 2922: 'l', 2924: 'n', 2929: 's', 3002: 'A', 3004: 'C', 3015: 'N', 3019: 'R', 3021: 'T', 3023: 'V', 3028: 'a', 3030: 'c', 3031: 'd', 3032: 'e', 3033: 'f', 3034: 'g', 3038: 'k', 3039: 'l', 3040: 'm', 3041: 'n', 3042: 'o', 3043: 'p', 3046: 's', 3047: 't', 3048: 'u', 3049: 'v', 3050: 'w', 3084: 'ε', 3090: 'λ', 3091: 'µ', 3109: 'ϕ', 3117: '1', 3118: '2', 3119: '3', 3120: '4', 3265: 'P', 3276: 'a', 3279: 'd', 3284: 'i', 3290: 'o', 3293: 'r', 3294: 's', 3295: 't', 3298: 'w', 3300: 'y', 3397: '+', 3399: '±', 3400: '×', 3404: '=', 3406: '≈', 3495: '√', 4593: '′', 4594: '′', 4666: '(', 4667: ')', 4672: '(', 4673: ')'}, 'Cambria-Bold': {158: 'á', 239: 'ú'}, 'SymbolMT': {84: 'θ'}, 'TimesNewRomanPS-ItalicMT': {537: 'θ'}, 'TimesNewRomanPSMT': {537: 'θ'}}}
VERIFIED_LINES=[]
QUESTION_TOTALS={**{q:40 for q in range(1,6)},**{q:56 for q in range(6,12)},12:112,13:56,14:112}
PART_TOTALS={(12,'a'):56,(12,'b'):56,**{(13,l):7 for l in 'abcdefgh'},**{(14,l):28 for l in 'abcd'}}
BEST_OF={6:(8,7)};GROUP_TOTALS={};CHECKSUMS={};ROUTES={'Q6(l)':['neutrino','relay']}
SCAN_PAGES={'paper':range(2,16)};SELECTION_SCAN=[]
ASK_SCAN_PAGES={'paper':range(2,16)};ASK_EXEMPT=[]
P=Q;SEC='State Examinations Commission';CRIT='The scheme prints this criterion rather than a worked example.'
TASKS=[];FIGURES={}
def R(text,marks,end=None,**kw):return pt(S(text,end,**kw.pop('sel',{})),marks,**kw)
def C(text,marks,end=None,**kw):return R(text,marks,end,kind='criterion',note=kw.pop('note',CRIT),**kw)
def FR(page,clip,expect,marks,**kw):return G('fraction',page=page,clip=clip,expect=expect,marks=marks,baseline=True,dedupe=True,glyph_order=True,segments=True,glyph_baselines=True,**kw)
def EQ(page,clip,expect,marks,**kw):return G('equation',page=page,clip=clip,expect=expect,marks=marks,degrees=True,dedupe=True,baseline=True,glyph_baselines=True,**kw)
def A(page,marker,path=(),welded=False):
 return SQ(page,marker,bare=True,path=path,welded=welded,paired='The deferred scheme prints the answer below or beside this numbered marker, without reprinting the ask. Paper and scheme paths independently checked visually.')
def B(key,ref,page,start,end,sp,marker,rows,topic,total,**kw):
 sq=kw.pop('sq',A(sp,marker,kw.pop('path',()),kw.pop('welded',False)))
 TASKS.append(T(key,ref,'A' if int(ref.split('(')[0][1:])<6 else 'B',P(page,start,end,**kw.pop('pkw',{})),rows,topic,key,sq,total,**kw))
def F(key,doc,page,clip,description,solution=False,masks=(),labels=(),credit=SEC):
 FIGURES[key]=(doc,page,clip,credit,list(labels),description,solution,list(masks))
def CP(text,n,marks,sep=', ',note=CRIT):
 return [pt(S(text,piece=i,psep=sep),marks,kind='criterion',note=note) for i in range(1,n+1)]
# Q1: keep the full experiment, original graph and centimetre acceleration axis.
ST1=P(2,'A student carried out a laboratory experiment to investigate the relationship between the force','The data recorded were used to draw the graph shown.')
B('q1i','Q1(i)',2,'Draw a labelled diagram of how the apparatus was arranged in this experiment.',None,3,'(i)',CP('track and trolley, timing system, string and weights',3,3),'phys-1-2',9,stem=[ST1],fig='q1-graph')
B('q1iia','Q1(ii)(a)',2,'what quantities need to be measured so that the acceleration can be calculated',None,3,'(a)',CP('initial and final velocity, displacement/time',2,3,note='Measure initial and final velocity, together with displacement or elapsed time, for the chosen acceleration equation.'),'phys-1-1',6,stem=[ST1,P(2,'Using your diagram or otherwise, explain')],path=['(ii)'],fig='q1-graph')
B('q1iib','Q1(ii)(b)',2,'how the student calculated the acceleration.',None,3,'(b)',[R('v² = u² + 2as // v = u + at',3)],'phys-1-1',3,stem=[ST1,P(2,'Using your diagram or otherwise, explain')],path=['(ii)'],fig='q1-graph')
B('q1iii','Q1(iii)',2,'How did the student measure the applied force?',None,3,'(iii)',[R('using weights',3,note='The accelerating weight provides a known force, F = mg.')],'phys-1-2',3,stem=[ST1],fig='q1-graph')
B('q1iv','Q1(iv)',2,'How did the student ensure that the applied force was the only force accelerating the','system?',3,'(iv)',[R('slope the track / use air track / cleaned the track / oil the wheels of the trolley',4,note='Reduce or compensate for friction so the applied force is the net accelerating force.')],'phys-1-2',4,stem=[ST1],fig='q1-graph')
B('q1v','Q1(v)',2,'Why did the student ensure that the mass of the system was kept constant?',None,3,'(v)',[R('changing mass would introduce a third variable',4)],'phys-1-2',4,stem=[ST1],fig='q1-graph')
B('q1vi','Q1(vi)',2,'How did the student ensure that the mass of the system was kept constant?',None,3,'(vi)',[R('masses transferred from the trolley to the accelerating weight',4)],'phys-1-2',4,stem=[ST1],fig='q1-graph')
PART_TOTALS[(1,'vii')]=7
B('q1vii','Q1(vii)',2,'Using the graph above, calculate the mass of the accelerated system in kilograms.',None,3,'(vii)',[C('slope formula',0,sel={'piece':1,'psep':', '},note='Mass is the gradient of force against acceleration. Convert the acceleration axis from cm s⁻² to m s⁻²; multiply the gradient in N/(cm s⁻²) by 100.'),R('slope formula',0,sel={'piece':2,'psep':', '},note='The brief scheme gives 3 + 3 + 1 marks but names only the slope method and final mass. Assess the complete calculation against the seven-mark allocation.')],'phys-1-2',7,stem=[ST1],fig='q1-graph',welded=True,tariff='questionTotal',decision='Retain the printed 3+3+1 total without inventing an unnamed intermediate criterion.')
# Q2: the six data pairs and 10 °C starting temperature accompany every task.
ST2=P(3,'A student carried out an experiment to measure the specific heat capacity of water. 61 g of water','The data were recorded in the table below.')
B('q2i','Q2(i)',3,'How could the energy have been supplied to the water?',None,4,'(i)',[R('coil // e.g. hot copper',6)],'phys-2-1',6,stem=[ST2],fig='q2-data')
B('q2ii','Q2(ii)',3,'Describe two precautions that the student should have taken to ensure that θ was measured','accurately.',4,'(ii)',[anyn(S('stir water / wait until highest temperature is reached / use a more accurate thermometer'),2,3)],'phys-2-1',6,stem=[ST2],fig='q2-data')
B('q2iii','Q2(iii)',3,'Describe how the container of water might have been insulated.',None,4,'(iii)',[R('lagging / lid',3)],'phys-2-1',3,stem=[ST2],fig='q2-data')
B('q2iv','Q2(iv)',3,'The student used a container of negligible heat capacity.','What is the significance of the fact that the container had negligible heat capacity?',4,'(iv)',[R('it can be ignored in the calculation / does not absorb heat',3)],'phys-2-1',3,stem=[ST2],fig='q2-data')
B('q2v','Q2(v)',3,'Using the data provided, draw a suitable graph on graph paper of E against Δθ, the change in','temperature of the water.',4,'(v)',CP('axes labelled, points plotted, line of best fit',3,3,note='Use E (J) vertically and Δθ (°C or K) horizontally. Plot all six readings, with Δθ = 5, 10, 15, 20, 25 and 30. The scheme illustration extends beyond these source data.'),'phys-2-1',9,stem=[ST2],fig='q2-data')
B('q2vi','Q2(vi)',3,'Calculate the slope of your graph.',None,4,'(vi)',[C('formula, slope = 254.8 J K⁻¹',3,sel={'piece':1,'psep':', '},note='Gradient = change in E divided by change in Δθ.'),R('formula, slope = 254.8 J K⁻¹',3,sel={'piece':2,'psep':', '})],'phys-2-1',6,stem=[ST2,P(3,'Using the data provided, draw a suitable graph on graph paper of E against Δθ, the change in','temperature of the water.')],fig='q2-data')
B('q2vii','Q2(vii)',3,'Use your slope to find the specific heat capacity of water.',None,4,'(vii)',[C('formula, c = (',4,sel={'piece':1,'psep':', '},note='From E = mcΔθ, c = graph gradient / mass. Use 0.061 kg.'),EQ(4,(184,370,268,388),'= 4176.6 J Kg⁻¹K⁻¹',3)],'phys-2-1',7,stem=[ST2,P(3,'Using the data provided, draw a suitable graph on graph paper of E against Δθ, the change in','temperature of the water.')],fig='q2-data',welded=True)
# Q3: four lens readings; a divergent lens gives a virtual image.
ST3=P(3,'A student was given a box that contained both converging lenses and diverging lenses.','values of u and v, which were recorded in the table below.')
B('q3i','Q3(i)',3,'Why would the method described for this experiment not work for a diverging lens?',None,5,'(i)',[R('image cannot be formed on a screen / only a virtual image is formed',3)],'phys-2-3',3,stem=[ST3],fig='q3-data')
B('q3ii','Q3(ii)',3,'How did the student determine which lens was a converging lens?',None,5,'(ii)',[R('shape / check if it formed a magnified/inverted/real image',3)],'phys-2-3',3,stem=[ST3],fig='q3-data')
B('q3iii','Q3(iii)',3,'How did the student find an approximate value for the focal length?',None,5,'(iii)',[pt(S('focus image of a distant object on a screen, measure the distance from the lens to the','screen',piece=1,psep=', '),3),pt(S('focus image of a distant object on a screen, measure the distance from the lens to the','screen',piece=2,psep=', '),3)],'phys-2-3',6,stem=[ST3],fig='q3-data')
B('q3iv','Q3(iv)',3,'Draw a labelled diagram of how the apparatus was set up to measure u and v.',None,5,'(iv)',CP('object and lens and screen, correct arrangement',2,3),'phys-2-3',6,stem=[ST3],fig='q3-data')
B('q3v','Q3(v)',3,'Label the distances u and v on your diagram.',None,5,'(v)',[R('u = object to lens',2),R('v = lens to the screen',2)],'phys-2-3',4,stem=[ST3,P(3,'Draw a labelled diagram of how the apparatus was set up to measure u and v.')],fig='q3-data')
B('q3vi','Q3(vi)',3,'Describe two precautions that the student should have taken to ensure that v was measured','accurately.',5,'(vi)',[anyn(S('avoid error of parallax / measure to/from centre of the lens / sharp image formed'),2,3,sep=' / ')],'phys-2-3',6,stem=[ST3],fig='q3-data')
B('q3vii','Q3(vii)',3,'Use all the data provided to calculate an average value for f.',None,5,'(vii)',[C('formula, first f value, other f values, average',3,sel={'piece':1,'psep':', '},note='Use 1/f = 1/u + 1/v for each pair.'),C('formula, first f value, other f values, average',3,sel={'piece':2,'psep':', '},note='The first pair gives f = 79.5 mm.'),C('formula, first f value, other f values, average',3,sel={'piece':3,'psep':', '},note='The other three values are 80.6, 80.6 and 79.4 mm.'),R('faverage = 80.0 mm',3)],'phys-2-3',12,stem=[ST3],fig='q3-data',welded=True)
# Q4: both tables and the measured length/diameter remain on each derived task.
ST4=P(4,'A student investigated the relationship between the resistance R of a piece of metal wire and its','temperature θ. The data were recorded in the table below.')
MAT4=P(4,'The student carried out research to identify the material that the wire is made from and found','values for the resistivity ρ of various materials at a temperature of 300 K, as shown below.')
SIZE4=P(4,'The wire is found to have a length of 0.221 m and a diameter of 0.46 mm.')
B('q4i','Q4(i)',4,'Draw a labelled diagram of how the apparatus was arranged in this experiment.',None,6,'(i)',CP('heat source, thermometer, ohmmeter',3,3),'phys-3-3',9,stem=[ST4],fig='q4-data')
B('q4ii','Q4(ii)',4,'Draw a suitable graph on graph paper to show the relationship between R and θ.',None,6,'(ii)',CP('axes labelled, points plotted, line of best fit',3,3,note='Plot R (Ω) against θ (°C), using all six readings and a straight line of best fit.'),'phys-3-3',9,stem=[ST4],fig='q4-data')
B('q4iii','Q4(iii)',4,'Convert 300 K to °C.',None,6,'(iii)',[R('reference to 273.15',3,note='Subtract 273.15 from the Kelvin temperature.'),R('θ = 26.85 °C',3)],'phys-2-1',6,stem=[ST4,MAT4],fig='q4-materials')
B('q4iv','Q4(iv)',4,'Use your graph to find the resistance of the wire at 300 K.',None,6,'(iv)',[R('R = 0.199 Ω',3,note='Read the graph at θ = 26.85 °C.')],'phys-3-3',3,stem=[ST4,MAT4,P(4,'Draw a suitable graph on graph paper to show the relationship between R and θ.')],fig='q4-data')
B('q4v','Q4(v)',4,'Name a suitable device that could have been used to measure the diameter of the wire.',None,6,'(v)',[R('micrometer / digital vernier callipers',3)],'phys-3-3',3,stem=[ST4,SIZE4],fig='q4-data')
B('q4vi','Q4(vi)',4,'Use the data to calculate the resistivity of the wire at 300 K.',None,6,'(vi)',[C('resistivity formula',3,note='ρ = RA/l; use the resistance from the graph at 300 K.'),C('area formula',3,note='A = πd²/4, with d = 0.00046 m.'),R('ρ = 150 x 10⁻⁹ Ω m',3)],'phys-3-3',9,stem=[ST4,MAT4,SIZE4],fig='q4-both-tables')
B('q4vii','Q4(vii)',4,'Identify the material that the wire is made from.',None,6,'(vii)',[R('steel',1)],'phys-3-3',1,stem=[ST4,MAT4,SIZE4,P(4,'Use the data to calculate the resistivity of the wire at 300 K.')],fig='q4-both-tables',welded=True)
# Q5: six nonzero diode readings and origin, with their mA and V units.
ST5=P(4,'A student investigated the variation of current I with voltage V for a semiconductor diode in','forward bias. The student set up a suitable circuit and recorded the data shown in the table below.')
B('q5i','Q5(i)',4,'Draw a circuit diagram for this experiment.',None,7,'(i)',CP('diode in forward bias, voltage source, ammeter in series, voltmeter in parallel',4,3),'phys-3-3',12,stem=[ST5],fig='q5-data')
B('q5ii','Q5(ii)',4,'How did the student vary the voltage?',None,7,'(ii)',[R('rheostat was adjusted',6)],'phys-3-3',6,stem=[ST5],fig='q5-data')
B('q5iii','Q5(iii)',4,'How did the student ensure that the diode did not overheat?',None,7,'(iii)',[R('protective resistor put in series with it',4)],'phys-3-3',4,stem=[ST5],fig='q5-data')
B('q5iv','Q5(iv)',4,'Draw a suitable graph on graph paper to show the variation of I with V for the','semiconductor diode.',7,'(iv)',CP('axes labelled, points plotted, curve',3,3,note='Plot all seven paper readings with I in mA and V in volts. Use a smooth curve; the scheme illustration includes additional/interpolated points.'),'phys-3-3',9,stem=[ST5],fig='q5-data')
B('q5v','Q5(v)',4,'Identify the junction voltage of the diode.',None,7,'(v)',[R('V ≈ 0.55 (V)',3)],'phys-3-3',3,stem=[ST5,P(4,'Draw a suitable graph on graph paper to show the variation of I with V for the','semiconductor diode.')],fig='q5-data')
B('q5vi','Q5(vi)',4,'What changes should have been made to the circuit for a diode in reverse bias?',None,7,'(vi)',[anyn(S('reverse the diode/battery connections / use a microammeter / connect the voltmeter across','the diode and (micro)ammeter'),2,3,sep=' / ')],'phys-3-3',6,stem=[ST5,P(4,'The student was then asked to investigate the variation of I with V for a semiconductor diode in','reverse bias.')],fig='q5-data')
# Section B short questions: retain both distinct-topic choices at Q6(l).
B('q6a','Q6(a)',5,'A child drags a box across a horizontal floor with a force of 44 N','floor is 20.5 N. Calculate the net horizontal force on the box.',8,'(a)',[R('FHorizontal = 44 cos 47° = 30.01 (N)',4),R('FNet = 30.01 – 20.5 = 9.51 N',3)],'phys-1-2',7,fig='q6-box')
B('q6b','Q6(b)',5,'Write an expression for the acceleration a of a body oscillating at the end of a spring in','from its equilibrium position.',8,'(b)',[R('F = ma / F = -ks / a = -ω²s',4),FR(8,(83,122,132,148),'a=- k/m s',3)],'phys-1-3',7,cells='The final formula is a separate PDF block below the page text, but its printed (4+3) belongs to Q6(b).')
B('q6c','Q6(c)',5,'When exercising, an athlete loses body heat through perspiration at a rate of 300 W.','minute to account for this heat loss.',8,'(c)',[R('Heat loss for 1 minute = (300 x 60) = 18000 (J)',3),R('E = ml',2),R('mass per minute = 0.0074 kg',2)],'phys-2-1',7,stem=[P(5,'latent heat of vaporisation for perspiration = 2426 kJ kg⁻¹')])
B('q6d','Q6(d)',5,'A stretched string vibrates at a fundamental frequency of 205 Hz when the tension applied is','5 N. Calculate the fundamental frequency of the string when the tension applied is 10 N.',8,'(d)',[FR(8,(83,218,185,246),'f∝√T/f= 1/(2l) √(T/(µ))',4),R('fnew=(√2 ×205)=290 Hz',3)],'phys-2-5',7)
B('q6e','Q6(e)',5,'A person holds a curved metal spoon at arm’s length and rotates it slowly. On one side of','why.',8,'(e)',[R('concave side gives an inverted image',4),R('convex side gives an upright image',3)],'phys-2-3',7)
B('q6f','Q6(f)',5,'The refractive index of a diamond is 2.41. Calculate its critical angle.',None,8,'(f)',[FR(8,(83,311,124,340),'n= 1/(sinC)',4),R('C = 24.4°',3)],'phys-2-3',7)
B('q6g','Q6(g)',5,'Explain the principle of operation of polaroid sunglasses and how they help the wearer.',None,8,'(g)',[R('only allows light in one plane through',4),R('prevents glare',3)],'phys-2-3',7)
B('q6h','Q6(h)',5,'State the colours of (i) the live wire, (ii) the neutral wire and (iii) the earth wire in a plug.',None,8,'(h)',[R('live – brown',3),R('neutral – blue',2),R('earth – yellow and green',2)],'phys-3-3',7)
B('q6i','Q6(i)',5,'Sketch a graph to show how current varies with the voltage applied across the vacuum in a','cathode ray tube.',8,'(i)',[C('axes labelled',4,note='Label current and voltage axes.'),C('shape',3,note='The scheme awards the graph shape but supplies no sketch. Show current rising with positive anode voltage and approaching saturation.')],'phys-4-1',7)
B('q6j','Q6(j)',5,'Explain why a balloon that has been rubbed vigorously on a woolly jumper','can stick to a wall.',8,'(j)',[R('balloon becomes charged',4),R('sticks to opposite charges in the wall',3,note='The charged balloon polarises the wall; nearer opposite charges give a net attraction.')],'phys-3-1',7,fig='q6-balloon')
B('q6k','Q6(k)',5,'Calculate the maximum moment of the couple in a basic d.c. motor when a','magnetic field of 0.22 mT.',8,'(k)',[R('F = BIl / T = Fd',4),R('T = 7.15 x 10⁻⁸ Nm',3)],'phys-3-5',7)
B('q6l-neutrino','Q6(l)',5,'Explain why the existence of the neutrino was first proposed.',None,8,'(l)',[R('to conserve energy / to conserve momentum',7)],'phys-4-5',7,route='neutrino')
B('q6l-relay','Q6(l)',5,'What is an electromagnetic relay? State one use of an electromagnetic relay.',None,8,'(l)',[R('electric switch',4),R('e.g.: car ignition system',3)],'phys-3-4',7,route='relay')
# Buoyancy and the compressed balloon: all mass, volume, depth and constants retained.
STEEL7=P(6,'Steel is denser than water.')
B('q7i','Q7(i)',6,'State Archimedes’ principle.',None,9,'(i)',[R('upthrust on an object is equal to',3),R('the weight of the fluid displaced',3)],'phys-1-5',6,fig='q7-boat')
B('q7ii','Q7(ii)',6,'Describe a laboratory experiment to demonstrate','Archimedes’ principle.',9,'(ii)',CP('apparatus, method, observation',3,3,note='For example, measure an object’s apparent loss of weight on immersion and compare it with the weight of displaced liquid. The scheme supplies the three criteria only.'),'phys-1-5',9,fig='q7-boat')
B('q7iii','Q7(iii)',6,'A steel bar sinks when it is placed in water.','Explain why.',9,'(iii)',[R('the weight of the steel is greater than the upthrust',3)],'phys-1-5',3,stem=[STEEL7],fig='q7-boat')
B('q7iv','Q7(iv)',6,'A boat which is made mostly of steel floats in water. Explain why.',None,9,'(iv)',[R('the density of the boat plus contents is less than the density of water /',6,end='upthrust equals the weight of the boat')],'phys-1-5',6,stem=[STEEL7],fig='q7-boat')
BALLOON7=P(6,'A sealed balloon contains 7.75 g of air and has a volume of 6000 cm³ when it is at the surface of','balloon stays constant at 4 °C.')
CONST7=P(6,'density of seawater at 4 °C = 1028 kg m⁻³; acceleration due to gravity = 9.8 m s⁻²;','atmospheric pressure at sea level = 101.3 kPa')
B('q7v','Q7(v)',6,'Calculate the density of air at the surface of the sea.',None,9,'(v)',[FR(9,(83,177,122,204),'ρ= m/v',3),R('ρ = 1.29 kg m⁻³',3)],'phys-1-5',6,stem=[BALLOON7,CONST7])
B('q7vi','Q7(vi)',6,'Calculate the total pressure acting on the balloon when it is at a depth of 37 m.',None,9,'(vi)',[R('p = ρgh',3),R('pTotal = pₐₜₘ + ρgh = 101300 + 372752.8 = 474052.8 Pa',3)],'phys-1-5',6,stem=[BALLOON7,CONST7])
B('q7vii','Q7(vii)',6,'State Boyle’s law.',None,9,'(vii)',[R('pressure is inversely proportional to volume',3),R('for a fixed mass of gas at constant temperature',3)],'phys-1-5',6,stem=[BALLOON7],welded=True)
B('q7viii','Q7(viii)',6,'Calculate the density of the air in the balloon at a depth of 37 m.',None,9,'(viii)',[R('p₁V₁ = p₂V₂',3),R('v (at 37 m depth) = 1282 cm³ / 0.001282 m³',3),FR(9,(83,348,327,376),'ρ=( m/v )=( 7.75/1282 )=0.006gcm⁻³/6kgm⁻³',2)],'phys-1-5',8,stem=[BALLOON7,CONST7],welded=True)
B('q7ix','Q7(ix)',6,'The balloon is released from the sea floor. Draw a force diagram to show the forces acting','on the balloon as it rises through the water.',9,'(ix)',[C('upthrust arrow > weight arrow + friction arrow',2,sel={'piece':1,'psep':' > '},note='Upwards; the scheme expects it longer than the combined downward weight and friction arrows.'),C('upthrust arrow > weight arrow + friction arrow',2,sel={'piece':[2,1],'psep':[' > ',' + ']},note='Weight acts downwards.'),C('upthrust arrow > weight arrow + friction arrow',2,sel={'piece':[2,2],'psep':[' > ',' + ']},note='Friction/drag acts downwards, opposite the rising motion.')],'phys-1-5',6,stem=[BALLOON7,CONST7])
# Q8: X-rays, spectrometer setup and the observed helium line.
ST8=P(7,'X‐rays and visible light are both part of the electromagnetic spectrum.')
HELIUM8=P(7,'Helium was first observed by the French astronomer Jules Janssen in 1868.','time. It was later found to belong to the spectrum of helium.')
GRATING8=P(7,'A spectrometer and an appropriate light source are used to investigate the line emission spectrum','between the two second order images of the yellow line is found to be 89.67°.')
B('q8i','Q8(i)',7,'What is the electromagnetic spectrum?',None,10,'(i)',[R('range of',3),R('types/frequencies/wavelengths/energies of electromagnetic radiation',3)],'phys-2-4',6,stem=[ST8])
B('q8ii','Q8(ii)',7,'Draw a labelled diagram of an X‐ray tube.',None,10,'(ii)',[anyn(S('high voltage, heat source, cathode, anode, target, vacuum'),4,3,sep=', ',note='Show and label four of the six listed features in an X-ray tube diagram.')],'phys-4-1',12,stem=[ST8])
B('q8iii','Q8(iii)',7,'The working voltage of an X‐ray tube is 65 kV.','Calculate the maximum energy of the X‐rays that can be produced in this X‐ray tube.',10,'(iii)',[R('E = qV',3),R('E = 1.04 x 10⁻¹⁴ J',3)],'phys-4-1',6,stem=[ST8])
B('q8iv','Q8(iv)',7,'What property of X‐rays makes them suitable for use in diagnosing a broken bone?',None,10,'(iv)',[R('penetrating ability',2)],'phys-4-1',2,stem=[ST8])
B('q8v','Q8(v)',7,'Draw a labelled diagram of a spectrometer.',None,10,'(v)',CP('telescope, collimator, table and scale',3,3),'phys-2-6',9,stem=[HELIUM8],fig='q8-janssen')
B('q8vi','Q8(vi)',7,'State three adjustments that should be made when setting up a','spectrometer.',10,'(vi)',[anyn(S('focus the telescope, adjust the collimator, adjust the width of the slit, level the table, focus','the cross hairs'),3,2,sep=', ')],'phys-2-6',6,stem=[HELIUM8],fig='q8-janssen')
B('q8vii','Q8(vii)',7,'Calculate the wavelength of the yellow light.',None,10,'(vii)',[R('nλ = d sinθ',3),R('d = 1.67 x 10⁻⁶ (m)',3),R('θ = 44.835°',3,note='Halve the angle between the two second-order images; n = 2.'),R('λ = 588 nm',3)],'phys-2-6',12,stem=[HELIUM8,GRATING8],welded=True,fig='q8-grating-solution')
B('q8viii','Q8(viii)',7,'Explain why this diffraction grating is not suitable for use with X‐rays.',None,10,'(viii)',[R('width of the slits is too big / wavelength of X-rays too short',3,note='The grating spacing is much larger than an X-ray wavelength, so the diffraction angles are too small to resolve.')],'phys-2-6',3,stem=[GRATING8],welded=True)
# Q9: each decay calculation retains the given sample size/activity and dating context.
FIELD9=P(8,'Alpha radiation and gamma radiation enter a magnetic field together, with their direction of travel','magnetic field are shown below.')
URANIUM9=P(8,'Uranium–235 is an unstable isotope of uranium and decays by alpha emission.')
SAMPLE9=P(8,'A sample of uranium–235 containing 7.69 x 10¹⁵ atoms has an activity of 0.24 Bq.')
CRYSTAL9=P(8,'A sample of uranium–235 was trapped inside a crystal many millions of years ago. The sample is','The sample is found to have 1.5625% of the original sample of uranium–235 remaining.')
B('q9i','Q9(i)',8,'State the law of radioactive decay.',None,11,'(i)',[R('activity is proportional // A = λN',3),R('to the number of nuclei present // notation',3,note='For A = λN, A is activity, λ the decay constant and N the number of undecayed nuclei.')],'phys-4-2',6)
B('q9ii','Q9(ii)',8,'What is meant by the term half‐life?',None,11,'(ii)',[R('time taken',3),R('for half the sample to decay',3)],'phys-4-2',6)
B('q9iii','Q9(iii)',8,'Name the type of radiation that travels in a straight line in the magnetic field.','Justify your answer.',11,'(iii)',[R('gamma radiation',3),R('it is neutral',3)],'phys-4-2',6,stem=[FIELD9],fig='q9-radiation')
B('q9iv','Q9(iv)',8,"Use Fleming's left‐hand rule to determine the direction of the magnetic field.",None,11,'(iv)',[R('into the page / downwards',6,note='The scheme also allows “perpendicular to the page / out of the page / upwards” for 3 marks; this is partial credit, not an additional row.')],'phys-3-4',6,stem=[FIELD9],fig='q9-radiation')
B('q9v','Q9(v)',8,'Explain the term isotope.',None,11,'(v)',[R('atoms with equal numbers of protons / atoms with same atomic number',3),R('different number of neutrons / different mass number',3)],'phys-4-2',6,stem=[URANIUM9])
PART_TOTALS[(9,'vi')]=8
B('q9vi','Q9(vi)',8,'Write a nuclear equation for the decay of uranium–235.',None,11,'(vi)',[EQ(11,(83,266,196,289),'U²³⁵₉₂ → Th²³¹₉₀ + He⁴₂',0,note='The original equation is shown with its nuclear notation. The scheme prints eight one-mark elements without a separate written description of each.')],'phys-4-2',8,stem=[URANIUM9],tariff='questionTotal',welded=True,fig='q9-decay-solution',decision='Retain the eight-mark complete nuclear equation; do not guess which printed elements receive individual marks.')
B('q9vii','Q9(vii)',8,'A sample of uranium–235 containing 7.69 x 10¹⁵ atoms has an activity of 0.24 Bq.','Calculate the half‐life of uranium–235.',11,'(vii)',[R('A = λN',3),FR(11,(83,303,275,332),'T½= ln2/λ /λ=3.12x10⁻¹⁷(s⁻¹)',3),R('T½ = 2.22 x 10¹⁶ s / 7.04 x 10⁸ years',3)],'phys-4-2',9,stem=[URANIUM9],welded=True,fig='q9-halflife-solution')
B('q9viii','Q9(viii)',8,'Calculate how many half‐lives have passed since the uranium was trapped in the crystal.',None,11,'(viii)',[R('6 half lives',3,note='1.5625% = 1/64 = (1/2)⁶.')],'phys-4-2',3,stem=[URANIUM9,CRYSTAL9],welded=True)
B('q9ix','Q9(ix)',8,'How many years ago was the uranium trapped in the crystal?',None,11,'(ix)',[R('4.23 x 10⁹ years',6,note='Multiply six half-lives by the half-life calculated from the supplied activity and number of atoms.')],'phys-4-2',6,stem=[URANIUM9,SAMPLE9,CRYSTAL9])
# Q10: retain complete mains/charger context, with cm², mT and kHz conversions.
ST10=P(9,'Many electronic devices use direct current and relatively low voltages. However the current','coming to our homes and businesses is a 50 Hz alternating current at a voltage of 230 V.')
CHARGER10=P(9,'Many electronic devices use a charger to charge a battery which','transformer.')
COIL10=P(9,'Some newer chargers make use of an electronic circuit to increase the frequency of the voltage.','changing at a frequency of 127 kHz.')
B('q10i','Q10(i)',9,'Electric current can be shown to have a magnetic effect.','State the two other effects of an electric current.',12,'(i)',[R('heating, chemical',3,sel={'piece':1,'psep':', '}),R('heating, chemical',3,sel={'piece':2,'psep':', '})],'phys-3-3',6,stem=[ST10])
B('q10ii','Q10(ii)',9,'Describe a laboratory experiment to demonstrate the magnetic effect of an','electric current.',12,'(ii)',CP('apparatus, method, observation',3,3,note='For example, place a compass near a straight wire connected to a low-voltage supply; close the switch and observe the compass deflect. The scheme supplies the three criteria only.'),'phys-3-4',9,stem=[ST10])
B('q10iii','Q10(iii)',9,'What is meant by voltage?',None,12,'(iii)',[R('work done // V = W/q',3),R('per unit charge // notation',3,note='V is potential difference, W the work done and q the charge moved.')],'phys-3-2',6,stem=[ST10])
B('q10iv','Q10(iv)',9,'Calculate the maximum voltage of a 230 V alternating source.',None,12,'(iv)',[R('Vmax = √2 VRMS',3),R('Vₘₐₓ = 325 V',3)],'phys-3-5',6,stem=[ST10])
B('q10v','Q10(v)',9,'An oscilloscope may be used to show alternating voltage. Draw a diagram to show how','alternating voltage is displayed on the screen of an oscilloscope.',12,'(v)',[C('axes labelled',3,note='Label voltage and time axes.'),C('correct shape',3,note='Show a sinusoidal voltage alternating above and below zero. The scheme gives no worked sketch.')],'phys-3-5',6,stem=[ST10])
B('q10vi','Q10(vi)',9,'Explain the operation of a transformer.',None,12,'(vi)',[R('when the current in a coil of wire changes',3),R('the magnetic field around it changes',3),R('it induces a voltage in a nearby coil',3)],'phys-3-5',9,stem=[ST10,CHARGER10],fig='q10-charger')
B('q10vii','Q10(vii)',9,'Calculate how many turns are needed in the secondary coil to give an output voltage of','5.75 V.',12,'(vii)',[FR(12,(83,288,128,318),'Vₒ/(Vi) = Nₛ/(NP)',3),R('Nₛ = 5',3)],'phys-3-5',6,stem=[ST10,CHARGER10,P(9,'A transformer with a primary coil of 200 turns has an input voltage of 230 V.')],qfig='q10-charger',fig='q10-turns-solution')
B('q10viii','Q10(viii)',9,'Calculate the voltage induced in the coil as the magnetic flux density changes from a','maximum of +2.6 mT to a minimum of –2.6 mT.',12,'(viii)',[R('φ=BA',2),R('T = 1/f',2,note='The maximum-to-minimum change takes half a period: Δt = 1/(2f).'),G('fraction',page=12,clip=(83,379,163,407),expect='Vinduced = -n dϕ/(dt)',marks=2,dedupe=True,segments=True),R('Vinduced = 4.44 V',2,note='Use |ΔB| = 5.2 × 10⁻³ T and A = 4.2 × 10⁻⁵ m²; the result is the magnitude of the average induced voltage over that half-period.')],'phys-3-5',8,stem=[ST10,CHARGER10,COIL10],welded=True,fig='q10-induced-solution')
# Q11: retain the published mass-defect typo with a clearly separated correction.
ST11=P(10,'John Tyndall from Leighlinbridge, Carlow was born in 1820. His major scientific','light from the Sun by particles in the atmosphere.')
DISTANCE11=P(10,'The distance between the Sun and the Earth is often given in astronomical units (au), where','Earth is 1.011 au.')
FUSION11=P(10,'The Sun is often described as the primary source of energy for the Earth. The Sun’s energy comes','nuclear equation:')
GREENHOUSE11=P(10,'As well as by direct heating from the Sun, the Earth can also be heated due to the greenhouse','effect.')
TYNDALL11=P(10,'In honour of John Tyndall, the Tyndall National Institute was established in Cork in 2004.','2 µm in optical fibres.')
B('q11i','Q11(i)',10,'Name the colour in the spectrum of white light that has the longest wavelength.',None,13,'(i)',[R('red',3)],'phys-2-4',3,stem=[ST11],fig='q11-tyndall')
B('q11ii','Q11(ii)',10,'Light from the Sun can give rise to a rainbow. State two conditions necessary for an','observer to see a rainbow.',13,'(ii)',[anyn(S('water droplets, sunlight, correct angle, sun at your back'),2,3,sep=', ')],'phys-2-4',6,stem=[ST11],fig='q11-tyndall')
B('q11iii','Q11(iii)',10,'Calculate, in minutes, the time it takes for light to travel from the Sun to the Earth at that','time of the year.',13,'(iii)',[R('1.011 au = 1.512 x 10¹¹ m',3),R('v = s/t',3),R('t = 8.41 min',2)],'phys-2-4',8,stem=[ST11,DISTANCE11],fig='q11-time-solution')
B('q11iv','Q11(iv)',10,'Calculate the energy released during this reaction.',None,13,'(iv)',[R('E = mc²',3),R('mass of H-2 = 2.014102 u / mass of H-1 = 1.007825 u / mass of He-3 = 3.016029 u',3,note='These are the three masses used together in the mass-defect calculation.'),R('mdifference = 9.794 x 10³⁰ (kg) / 5.898 x 10⁻³ (u)',3,note='Printed-scheme correction: the kg exponent is missing a minus sign. The physically consistent value is 9.794 × 10⁻³⁰ kg, from 0.005898 u; the scheme’s final energy also confirms this.'),C('conversion of u to kg',3,note='Multiply the mass in u by approximately 1.6605 × 10⁻²⁷ kg/u.'),R('E = 8.8 x 10⁻¹³ J',3)],'phys-4-3',15,stem=[ST11,FUSION11],qfig='q11-fusion-question',fig='q11-fusion-solution')
B('q11v','Q11(v)',10,'Explain how the greenhouse effect heats the Earth.',None,13,'(v)',[R('atmosphere / gases',3),R('trap radiation reflected by the Earth',3,note='Physics clarification: greenhouse gases absorb and re-emit infrared radiation emitted by the Earth. The quotation retains the brief scheme’s wording “reflected”.')],'phys-2-1',6,stem=[GREENHOUSE11])
B('q11vi','Q11(vi)',10,'The greenhouse effect has both positive and negative consequences for human life on Earth.','Explain why.',13,'(vi)',[R('the Earth would be too cold for humans without it',3),R('it is causing overheating of the Earth',3,note='The natural greenhouse effect supports a habitable temperature; an enhanced greenhouse effect drives additional warming.')],'phys-2-1',6,stem=[GREENHOUSE11])
B('q11vii','Q11(vii)',10,'Calculate the energy of a photon that has a wavelength of 2 µm.',None,13,'(vii)',[R('c = fλ',3),R('E = hf / f = 1.5 x 10¹⁴ (Hz)',3),R('E = 9.93 x 10⁻²⁰ J',3)],'phys-4-1',9,stem=[TYNDALL11],welded=True,qfig='q11-laboratory',fig='q11-photon-solution')
B('q11viii','Q11(viii)',10,'What phenomenon allows light to travel in an optical fibre without escaping?',None,13,'(viii)',[R('total internal reflection',3)],'phys-2-3',3,stem=[TYNDALL11],welded=True,fig='q11-laboratory')
# Q12(a): particle option, including both separately priced subparts of vi/vii.
ATM12=P(11,'Atmospheric particle physics is a major field of research. Gamma','Earth’s atmosphere.')
CERN12=P(11,'Scientists also investigate high energy collisions using circular','various new particles are detected, as well as the two protons.')
HADRONS12=P(11,'Two of the particles that have been detected after high energy collisions are the sigma','particle and the kaon.')
SIGMA12=P(11,'A particular sigma particle is made of an up quark, a down quark and a strange quark.')
KAON12=P(11,'A particular kaon is made of a down quark and an anti‐strange quark.')
RING12=P(11,'Engineers at CERN are planning to build a new circular accelerator with a greater radius.','charge q and mass m travelling in a circle of radius r.')
B('q12ai','Q12(a)(i)',11,'What is a positron?',None,14,'(i)',[R('anti-electron',3)],'phys-4-5',3,stem=[ATM12],path=['(a)'],fig='q12-balloon')
B('q12aii','Q12(a)(ii)',11,'Name a detector suitable for detecting gamma radiation and','describe the principle of its operation.',14,'(ii)',[R('solid state detector / Geiger Muller tube',3),R('ionisation',3),R('current',3)],'phys-4-2',9,stem=[ATM12],path=['(a)'],fig='q12-balloon')
B('q12aiii','Q12(a)(iii)',11,'Write an equation to represent the creation of an electron‐positron pair by gamma','radiation.',14,'(iii)',[R('γ / hf',3),R('= e⁺ + e⁻ / = 2mc²',3,note='Pair creation: γ → e⁻ + e⁺. The threshold photon energy is 2mc²; additional photon energy becomes kinetic energy.')],'phys-4-5',6,stem=[ATM12],path=['(a)'],fig='q12-pair-solution')
B('q12aiv','Q12(a)(iv)',11,'Electrons and positrons are both leptons. What is a lepton?',None,14,'(iv)',[R('fundamental particle',3),R('that does not feel the strong nuclear force',3)],'phys-4-5',6,stem=[ATM12],path=['(a)'])
B('q12av','Q12(a)(v)',11,'Calculate the maximum total mass these new particles can','have.',14,'(v)',[R('1 eV = 1.6 x 10⁻¹⁹ J',3),R('E = mc²',3,note='Use the combined kinetic energy of both protons: 13.6 TeV.'),R('m = 2.42 x 10⁻²³ kg',2)],'phys-4-5',8,stem=[CERN12],path=['(a)'],qfig='q12-cern',fig='q12-mass-solution')
B('q12avia','Q12(a)(vi)(a)',11,'What type of hadron is this sigma particle?',None,14,'(a)',[R('baryon',3)],'phys-4-5',3,stem=[HADRONS12,SIGMA12],path=['(a)','(vi)'],welded=True)
B('q12avib','Q12(a)(vi)(b)',11,'What charge does this sigma particle have?',None,14,'(b)',[R('neutral',3,note='Up (+2/3), down (−1/3) and strange (−1/3) sum to zero elementary charge.')],'phys-4-5',3,stem=[HADRONS12,SIGMA12],path=['(a)','(vi)'],welded=True)
B('q12aviia','Q12(a)(vii)(a)',11,'What type of hadron is this kaon?',None,14,'(vii)',[R('meson',3)],'phys-4-5',3,stem=[HADRONS12,KAON12],path=['(a)'],welded=True)
B('q12aviib','Q12(a)(vii)(b)',11,'What charge does this kaon have?',None,14,'(b)',[R('neutral',3,note='Down (−1/3) and anti-strange (+1/3) sum to zero elementary charge.')],'phys-4-5',3,stem=[HADRONS12,KAON12],path=['(a)','(vii) (a) meson'],welded=True)
B('q12aviii','Q12(a)(viii)',11,'Write an expression for the tangential velocity v of the particle in terms of B, q, m','and r.',14,'(viii)',[R('F = mv²/r / F = Bqv',3),R('mv²/r = Bqv',3),R('v = Bqr/m',3)],'phys-4-5',9,stem=[RING12],path=['(a)'],welded=True,fig='q12-ring-solution')
B('q12aix','Q12(a)(ix)',11,'Suggest a reason why engineers are planning to build a particle accelerator with a','greater radius.',14,'(ix)',[R('greater velocity/energy',3)],'phys-4-5',3,stem=[RING12],path=['(a)'])
# Q12(b): the source publishes four shared totals, not nine per-roman tariffs.
# WHOLE_GROUPS records the exact roman coverage and must match both the paper
# and scheme allocation. It never turns the shared total into row marks.
WHOLE_GROUPS={
 'q12b-i-ii':{'ref':'Q12(b)','romans':['i','ii'],'total':12},
 'q12b-iii-v':{'ref':'Q12(b)','romans':['iii','iv','v'],'total':16},
 'q12b-vi-vii':{'ref':'Q12(b)','romans':['vi','vii'],'total':15},
 'q12b-viii-ix':{'ref':'Q12(b)','romans':['viii','ix'],'total':13},
}
ST12B=P(12,'The semiconductor industry has grown to become one of','have changed the way people live.')
B('q12b-i-ii','Q12(b)',12,'What is a semiconductor?','semiconductor thermistor.',15,'(i)',[R('resistivity',0),R('between a good conductor and a good insulator',0),C('label axes',0,note='Label resistance and temperature axes.'),C('correct shape',0,note='For the semiconductor thermistor, resistance decreases nonlinearly as temperature rises.')],'phys-3-3',12,stem=[ST12B],item=('i-ii','Parts (i)–(ii)'),tariff='questionTotal',fig='q12-chip',decision='The paper and scheme give a single 12-mark total for i–ii. Assess the whole response without inventing per-part or row marks.')
B('q12b-iii-v','Q12(b)',12,'A semiconductor diode can be used as a half‐wave rectifier. Explain the term ‘half‐','What device can be used to smooth the current from a bridge rectifier?',15,'(iii)',[R('alternating current goes in',0),R('current flowing in one direction is blocked and current flowing in the other direction',0,end='passes through'),C('four diodes',0),C('arrangement',0,note='Draw four diodes in a bridge, with the a.c. supply across one diagonal and the load across the other. Both half-cycles drive load current in the same direction.'),R('capacitor',0)],'phys-3-3',16,stem=[ST12B,P(12,'Rectification is an important process in modern electronics.')],item=('iii-v','Parts (iii)–(v)'),tariff='questionTotal',decision='The paper and scheme give one 16-mark total for iii–v; all three asks and the complete rectifier criteria remain together.')
B('q12b-vi-vii','Q12(b)',12,'Describe with the aid of a labelled diagram the basic structure of a bi‐polar transistor.','happens in the circuit when the thermistor is kept at a low temperature.',15,'(vi)',[C('diagram',0),R('2 layers of p-type material with n-type between the layers',0,note='This describes a pnp transistor. An npn transistor has the opposite layer order; the supplied thermistor circuit uses npn.'),R('collector, base, emitter',0),R('resistance of the thermistor is high',0),R('base current flows',0),R('collector current flows / led lights',0,note='At low temperature the thermistor’s high resistance raises the base voltage, switching on the transistor and LED in the supplied circuit.')],'phys-4-6',15,stem=[ST12B,P(12,'A rectifier can be used to produce the direct current needed by a transistor.')],item=('vi-vii','Parts (vi)–(vii)'),tariff='questionTotal',fig='q12-thermistor',decision='The shared 15-mark transistor block includes the full original thermistor circuit. Do not split an unpublished allocation.')
B('q12b-viii-ix','Q12(b)',12,'Draw a circuit diagram to show how a transistor can be used to make a NOT gate.','Draw the truth table for a NOT gate',15,'(viii)',[R('transistor, two resistors',0),C('arrangement',0,note='Use a common-emitter transistor switch, with a base input resistor and a collector resistor to the positive supply; take the output at the collector.'),C('input voltage, output voltage indicated',0),G('lines',page=15,clip=(122,463,218,524),expect='Input Output — 0 1 — 1 0',marks=0,note='A NOT gate inverts the input: 0 → 1, 1 → 0.')],'phys-4-6',13,stem=[ST12B,P(12,'Logic gates are the basic building blocks of digital electronic circuits.')],item=('viii-ix','Parts (viii)–(ix)'),tariff='questionTotal',welded=True,fig='q12-not-solution',decision='Keep the NOT-gate circuit and truth table together at their published shared 13-mark boundary.')
# Q13: all eight cards retain the entire passage, attribution and illustrations.
PASSAGE13=P(13,'Read the following passage and answer the accompanying questions.','Adapted from: https://www.quantamagazine.org/how‐the‐physics‐of‐resonance‐shapes‐reality‐20220126/')
CONST13=P(13,'acceleration due to gravity = 9.8 m s⁻²; speed of sound in air = 343 m s⁻¹')
B('q13a','Q13(a)',13,'What is meant by resonance?',None,16,'(a)',[R('transfer of energy',4),R('between two bodies with the same natural frequencies',3)],'phys-2-2',7,stem=[PASSAGE13,CONST13],fig='q13-illustrations')
B('q13b','Q13(b)',13,'Describe a laboratory experiment to demonstrate resonance.',None,16,'(b)',[C('apparatus, method, observation',3,sel={'piece':1,'psep':', '},note='For example, use two tuning forks with the same natural frequency on sounding boxes.'),C('apparatus, method, observation',2,sel={'piece':2,'psep':', '},note='Strike the first fork and then damp it.'),C('apparatus, method, observation',2,sel={'piece':3,'psep':', '},note='The second fork is heard vibrating. These are explanatory examples; the scheme gives apparatus, method and observation criteria.')],'phys-2-2',7,stem=[PASSAGE13,CONST13],fig='q13-illustrations')
B('q13c','Q13(c)',13,'The motion of a playground swing can be thought of as a simple','frequency of a swing of length 1.5 m.',16,'(c)',[FR(16,(83,127,147,154),'T=2π√(l/g)',3),FR(16,(83,151,190,178),'T= 1/f /T=2.46(s)',2),R('f = 0.41 Hz',2)],'phys-1-3',7,stem=[PASSAGE13,CONST13],qfig='q13-illustrations',fig='q13-swing-solution')
B('q13d','Q13(d)',13,'A flute acts as a tube open at both ends. Draw a labelled diagram to','produced in a flute.',16,'(d)',[C('two antinodes',4,note='For the displacement standing wave, place an antinode at each open end.'),C('one node',3,note='Place the displacement node at the centre, halfway along the tube.')],'phys-2-5',7,stem=[PASSAGE13,CONST13],fig='q13-illustrations')
B('q13e','Q13(e)',13,'A drinking glass can be modelled as a cylindrical pipe of length 15 cm that is','glass to resonate and possibly even shatter.',16,'(e)',[R('λ = 0.6 (m)',3,note='A pipe closed at one end has L = λ/4 at its fundamental.'),R('c = f λ',2),R('f = 572 Hz',2)],'phys-2-5',7,stem=[PASSAGE13,CONST13],qfig='q13-illustrations',fig='q13-glass-solution')
B('q13f','Q13(f)',13,'Einstein’s explanation of the photoelectric effect depends on the concept of','effect.',16,'(f)',[R('one photon gives all its energy to one electron',3),R('if photon energy is greater than the work function, electron is emitted with kinetic energy',2),R('if photon energy is less than the work function, electron is not emitted',2)],'phys-4-1',7,stem=[PASSAGE13,CONST13],fig='q13-illustrations')
B('q13g','Q13(g)',13,'At the start of the 20th century, both Niels Bohr and Erwin Schrödinger developed their','(A labelled diagram may help your answer.)',16,'(g)',[R('electrons orbit',3),R('around a (positive) nucleus',2),R('at specific energy levels',2)],'phys-4-1',7,stem=[PASSAGE13,CONST13],fig='q13-illustrations')
B('q13h','Q13(h)',13,'Write a nuclear equation for the production of a carbon–12 nucleus, as described in the','passage.',16,'(h)',[EQ(16,(83,427,215,449),'He⁴₂ + He⁴₂ + He⁴₂ → C¹²₆',0,note='The source prints a shared 5 × 1 + 2 allocation. Check conservation of mass number and atomic number using the original equation shown.')],'phys-4-3',7,stem=[PASSAGE13,CONST13],tariff='questionTotal',qfig='q13-illustrations',fig='q13-carbon-solution',decision='Retain the seven-mark complete nuclear equation without inventing named one-mark/two-mark subcriteria.')
# Q14: all four independently selectable 28-mark parts; never choice combinations.
MOTION14=P(14,'The formula s = ut + ½at² is a version of one of the equations describing linear motion.')
B('q14ai','Q14(a)(i)',14,'What is meant by displacement?',None,17,'(i)',[R('distance in a given direction',3)],'phys-1-1',3,path=['(a)'])
B('q14aii','Q14(a)(ii)',14,'Explain what each letter stands for in this equation.',None,17,'(ii)',[R('s = displacement, u = initial velocity, t = time, a = acceleration',1,sel={'piece':i,'psep':', '}) for i in range(1,5)],'phys-1-1',4,stem=[MOTION14],path=['(a)'])
B('q14aiii','Q14(a)(iii)',14,'Derive this equation',None,17,'(iii)',[FR(17,(111,102,301,129),'v=u+at/v²=u²+2as/s= (u+v)/2 t',3),FR(17,(111,129,303,156),'(u+at)²=u²+2as//s= (u+(u+at))/2 t',3,note='Either substitute v = u + at into v² = u² + 2as and simplify, or substitute it into s = (u + v)t/2. Both give s = ut + ½at².')],'phys-1-1',6,stem=[MOTION14],path=['(a)'],fig='q14-derive-solution')
B('q14aiv','Q14(a)(iv)',14,'Describe the assumptions which make this equation valid.',None,17,'(iv)',[anyn(S('acceleration is constant, initial s = 0, initial t = 0'),2,3,sep=', ')],'phys-1-1',6,stem=[MOTION14],path=['(a)'])
B('q14av','Q14(a)(v)',14,'Calculate the time the stone is in the air.',None,17,'(v)',[R('s = -19, u = 6, g = -9.8',3,route='equation'),R('-19 = 6t + ½(-9.8)t²',3,route='equation'),R('t = 2.67 s',3,route='equation',note='Choose the positive root.'),FR(17,(260,176,499,205),'//tuₚ= (0−6)/(−9.8) =0.612(s)/suₚ= (0²−6²)/(2(−9.8)) =1.837(m)',3,route='up-down'),EQ(17,(365,211,425,228),'= 2.062 (s)',3,route='up-down',note='Time down from the highest point: √[2(1.837 + 19)/9.8] = 2.062 s. The full calculation is shown in the original scheme below.'),R('// t = tup + tdown = 2.67 s',3,route='up-down',note='Alternative complete method: add the time to the highest point and the time falling from there to the water. Assess one method, not both.')],'phys-1-1',9,stem=[P(14,'A student throws a small stone off a bridge. She throws the stone vertically upwards with a','speed of 6 m s⁻¹. It lands in the water, which is 19 m below the bridge.'),P(14,'acceleration due to gravity = 9.8 m s⁻²')],path=['(a)'],fig='q14-stone-solution')
BRIDGE14=P(14,'A student set up a Wheatstone bridge to find the resistance of a piece of wire. A series','combination of a variable resistor and the piece of metal wire.')
B('q14bi','Q14(b)(i)',14,'Define resistance.',None,17,'(i)',[R('ratio of potential difference // R = V/I',3),R('to current // notation',3,note='R is resistance, V potential difference and I current.')],'phys-3-3',6,path=['(b)'])
B('q14bii','Q14(b)(ii)',14,'Draw a circuit diagram of this Wheatstone bridge.',None,17,'(ii)',[C('voltage source, 4 resistors',3),C('galvanometer',3),C('arrangement',3,note='Use the two specified series branches in parallel across the supply, with the galvanometer between their midpoints.')],'phys-3-3',9,stem=[BRIDGE14],path=['(b)'])
B('q14biii','Q14(b)(iii)',14,'Describe how the student checked that the Wheatstone bridge was balanced.',None,17,'(iii)',[R('galvanometer reads zero',3)],'phys-3-3',3,stem=[BRIDGE14],path=['(b)'])
B('q14biv','Q14(b)(iv)',14,'Calculate the resistance of the piece of metal wire.',None,17,'(iv)',[FR(17,(111,414,155,444),'R₁/R₂ = R₃/R₄',3),R('Rwire = 7.5 Ω',3)],'phys-3-3',6,stem=[BRIDGE14,P(14,'The Wheatstone bridge was balanced when the variable resistor had a resistance of 5 Ω.')],path=['(b)'],fig='q14-bridge-solution')
B('q14bv','Q14(b)(v)',14,'Apart from measuring resistance, state one other practical use of a Wheatstone','bridge.',17,'(v)',[R('e.g. temperature control, fail safe device',4,note='One valid use is sufficient; the printed examples are alternatives.')],'phys-3-3',4,stem=[BRIDGE14],path=['(b)'])
CAR14=P(14,'A car travels along a road at a constant velocity, emitting an engine','and 272 Hz as the car moves away.')
SOUND14=P(14,'speed of sound in air = 343 m s⁻¹')
B('q14ci','Q14(c)(i)',14,'What is the Doppler effect?',None,18,'(i)',[R('apparent change in frequency',3),R('due to relative motion between the source and the observer',3)],'phys-2-2',6,path=['(c)'])
B('q14cii','Q14(c)(ii)',14,'Describe a laboratory experiment to demonstrate the Doppler effect.',None,18,'(ii)',CP('apparatus, method, observation',3,3,note='For example, move a sounding buzzer towards and away from a stationary listener; its observed pitch is higher while approaching and lower while receding. The scheme gives the three criteria only.'),'phys-2-2',9,path=['(c)'])
B('q14ciii','Q14(c)(iii)',14,'Calculate the speed of the car.',None,18,'(iii)',[FR(18,(111,122,162,149),'f′= fc/(c±u)',3),G('fraction',page=18,clip=(111,144,376,176),expect='(f′away(c+u))/c = (f′towards(c−u))/c / u=c (f′towards−f′away)/(f′towards+f′away)',marks=3,dedupe=True,segments=True),R('u = 18.49 m s⁻¹',3)],'phys-2-2',9,stem=[CAR14,SOUND14],path=['(c)'],qfig='q14-car',fig='q14-doppler-solution')
B('q14civ','Q14(c)(iv)',14,'Calculate the frequency of the engine sound heard by the driver of the car.',None,18,'(iv)',[R('f = 286.7 Hz',4,note='The driver moves with the source and hears its emitted frequency. Use the speed found from the two roadside measurements in the Doppler equation.')],'phys-2-2',4,stem=[CAR14,SOUND14],path=['(c)'],fig='q14-car')
B('q14di','Q14(d)(i)',15,'What is meant by capacitance?',None,18,'(i)',[R('charge',3,route='words'),R('per unit volt',3,route='words'),R('// C = q/V',3,route='formula'),C('// notation',3,route='formula',note='C is capacitance, q stored charge and V the potential difference.')],'phys-3-2',6,path=['(d)'])
B('q14dii','Q14(d)(ii)',15,'Describe a laboratory experiment to demonstrate how the capacitance of a','parallel‐plate capacitor varies with the distance between the plates.',18,'(ii)',CP('apparatus, method, observation',3,3,note='For example, connect parallel metal plates to a capacitance meter; vary their separation while keeping plate area and dielectric fixed. The reading decreases as separation increases. The scheme gives the three criteria only.'),'phys-3-2',9,path=['(d)'])
B('q14diii','Q14(d)(iii)',15,'Draw a diagram of the electric field between the plates of a charged parallel‐plate','capacitor.',18,'(iii)',[C('parallel lines',3,note='Draw evenly spaced straight lines perpendicular to the plates in the central region.'),C('direction indicated',3,note='Arrows point from the positive plate to the negative plate.')],'phys-3-1',6,path=['(d)'])
B('q14div','Q14(d)(iv)',15,'A parallel‐plate capacitor has a capacitance of 0.12 pF','changes to 0.3 mm.',18,'(iv)',[FR(18,(111,346,152,374),'C= εA/d',3),R('C₁d₁ = C₂d₂',2),R('2 pF',2)],'phys-3-2',7,stem=[P(15,'The keys on some modern keyboards act as parallel‐plate','plates is changed.')],path=['(d)'],qfig='q14-keyboard',fig='q14-capacitance-solution')
SELECTION_SCAN=[
 ('paper',2,'or','Diagram or otherwise permits explanatory method; both measured-quantity and acceleration tasks remain.'),
 ('paper',3,'both','The box contains both lens types; this is experiment context, not a choice.'),
 ('paper',5,'the following','All twelve short-question parts retained, including both distinct-topic alternatives in Q6(l).'),
 ('paper',5,'or','Neutrino and relay are distinct-topic seven-mark alternatives; retain both routes and count the tariff once.'),
 ('paper',7,'both','Both X-rays and visible light belong to the spectrum; descriptive context.'),
 ('paper',10,'the following','The supplied fusion equation is required source data, retained as an original crop.'),
 ('paper',10,'both','Positive and negative consequences are both required in one six-mark task.'),
 ('paper',11,'either','Both particle-physics and electronics options retained at their own published mark boundaries.'),
 ('paper',11,'or','Both Q12 options retained; these are alternatives, not a response combination.'),
 ('paper',11,'both','Electrons and positrons are descriptive examples of leptons.'),
 ('paper',13,'the following','Complete passage and attribution retained in all eight Q13 cards.'),
 ('paper',13,'both','The flute is open at both ends; essential physical setup, not a choice.'),
 ('paper',13,'both','Bohr and Schrödinger provide historical context; the task explicitly asks for the Bohr model.'),
 ('paper',14,'any two','All four separately selectable 28-mark options retained; do not generate combinations.'),
 ('paper',14,'the following','The same four Q14 options; each task follows its published tariff.'),
]
# Mark Bank uses its existing canonical practice buckets for mechanics and
# circuits. Atlas also retains the specific outgoing-course pressure and
# Applied Electricity headings, so both syllabus views reach these tasks.
TOPIC_CORRECTIONS={
 **{f'q7{r}':'phys-1-2' for r in ['i','ii','iii','iv','v','vi','vii','viii']},'q7ix':'phys-1-2',
 'q6g':'phys-2-4',
 **{f'q8{r}':'phys-4-2' for r in ['ii','iii','iv']},
 **{f'q9{r}':'phys-4-4' for r in ['i','ii','iii','v','vi','vii','viii','ix']},
 **{f'q10{r}':'phys-3-6' for r in ['iv','v','vi','vii','viii']},
 'q11iv':'phys-4-5','q11vii':'phys-4-2','q12aii':'phys-4-4',
 'q12b-vi-vii':'phys-3-3','q12b-viii-ix':'phys-3-3',
 'q13a':'phys-2-6','q13b':'phys-2-6','q13f':'phys-4-2','q13g':'phys-4-3','q13h':'phys-4-6',
 **{f'q14c{r}':'phys-2-7' for r in ['i','ii','iii','iv']},
 'q14diii':'phys-3-2',
}
for _t in TASKS:
 if _t['key'] in TOPIC_CORRECTIONS:_t['topic']=TOPIC_CORRECTIONS[_t['key']]

ASK_EXEMPT=[(15,'capacitors. When the key is pressed, the distance between the','Descriptive keyboard setup retained in Q14(d)(iv), not an extra ask.'),(15,'State Examinations Commission','Image-credit attribution in the acknowledgements, not an instruction.'),(15,'State Examination Commission','Image-credit attribution in the acknowledgements, not an instruction.')]
# Original source figures. Every crop is rendered and reviewed before writing.
F('q1-graph','paper',2,(96,232,474,521),'Original force–acceleration graph, with N and cm s⁻² axes, ticks, data and best-fit line.')
F('q2-data','paper',3,(55,156,541,201),'All six energy and final-temperature readings, with joule and °C headings.')
F('q3-data','paper',3,(144,505,451,553),'All four object/image distance pairs, with both mm headings.')
F('q4-data','paper',4,(55,91,541,137),'Six temperature/resistance pairs, with °C and Ω headings.')
F('q4-materials','paper',4,(55,217,541,262),'All six candidate materials and their resistivities at 300 K, in nΩ m.')
for _t in TASKS:
 if _t['fig']=='q4-both-tables':_t['qfig']='q4-data';_t['fig']='q4-materials'
F('q5-data','paper',4,(55,445,541,491),'All seven voltage/current pairs, including the origin, in V and mA.')
F('q6-box','paper',5,(435,151,540,198),'Box, floor and angled applied-force arrow from the original paper.')
F('q6-balloon','paper',5,(469,484,540,569),'Original photograph of a balloon attached to a wall.',credit='quora.com; reproduced in the SEC paper')
F('q7-boat','paper',6,(358,53,542,166),'Original steel-boat photograph.',credit='cruisemapper.com; reproduced in the SEC paper')
F('q8-janssen','paper',7,(446,171,542,309),'Original portrait of Jules Janssen.',credit='wikipedia.org; reproduced in the SEC paper')
F('q9-radiation','paper',8,(212,142,455,192),'Both radiation paths and direction arrows entering the magnetic field.')
F('q10-charger','paper',9,(414,236,541,330),'Original mains-charger photograph.',credit='sciencemuseumgroup.org.uk; reproduced in the SEC paper')
F('q11-tyndall','paper',10,(464,54,542,136),'Original John Tyndall portrait.',credit='wikipedia.org; reproduced in the SEC paper')
F('q11-laboratory','paper',10,(55,508,542,658),'Complete two-part Tyndall Institute laboratory photograph.',credit='tyndall.ie; reproduced in the SEC paper')
F('q11-fusion-question','paper',10,(258,320,340,347),'Original hydrogen–hydrogen fusion reaction with all mass and atomic numbers.')
F('q12-balloon','paper',11,(418,95,542,180),'Original atmospheric-research balloon photograph.',credit='donegaldaily.com; reproduced in the SEC paper')
F('q12-cern','paper',11,(421,258,542,383),'Original CERN accelerator location image.',credit='cern.ch; reproduced in the SEC paper')
F('q12-chip','paper',12,(374,53,542,122),'Original semiconductor-chip photograph.',credit='cloudfront.net; reproduced in the SEC paper')
F('q12-thermistor','paper',12,(199,381,420,592),'Complete thermistor/transistor/LED circuit, including both supply rails and component symbols.')
F('q13-illustrations','paper',13,(450,397,542,602),'Original flute and drinking-glass illustrations accompanying the resonance passage.',masks=[(450,496,475,601)],credit='wikimedia.org and freepik.com; reproduced in the SEC paper')
F('q14-car','paper',14,(450,566,542,636),'Original car photograph beside the two Doppler readings.',credit='cloudfront.net; reproduced in the SEC paper')
F('q14-keyboard','paper',15,(408,165,542,251),'Original keyboard illustration beside the capacitor-spacing question.',credit='shutterstock.com; reproduced in the SEC paper')
# Narrow originals preserve stacked fractions, nuclear indices and both routes.
for _key,_page,_clip,_description in [
 ('q8-grating-solution',10,(81,241,179,322),'All four diffraction calculation steps.'),
 ('q9-decay-solution',11,(81,264,197,291),'Uranium–235 alpha decay equation with full nuclear notation.'),
 ('q9-halflife-solution',11,(81,289,318,356),'Activity, decay constant and half-life calculation in seconds and years.'),
 ('q10-turns-solution',12,(81,287,130,338),'Transformer turns-ratio calculation.'),
 ('q10-induced-solution',12,(81,336,171,427),'Flux, period and induced-voltage calculation.'),
 ('q11-time-solution',13,(81,102,216,164),'Astronomical-unit conversion and light-travel time.'),
 ('q11-fusion-solution',13,(81,164,488,267),'Fusion calculation as printed, including the mass-defect exponent typo explicitly corrected in the card guidance.'),
 ('q11-photon-solution',13,(81,351,213,412),'Photon frequency and energy calculation.'),
 ('q12-pair-solution',14,(109,144,204,184),'Pair-creation equation and threshold-energy form.'),
 ('q12-mass-solution',14,(109,226,212,288),'Both-proton collision energy to maximum new-particle mass.'),
 ('q12-ring-solution',14,(109,370,216,433),'Magnetic and centripetal force expressions leading to tangential speed.'),
 ('q12-not-solution',15,(110,460,223,531),'Original NOT-gate truth table with both input/output rows.'),
 ('q13-swing-solution',16,(81,126,191,201),'Pendulum period and resonant frequency calculation.'),
 ('q13-glass-solution',16,(81,243,144,304),'Closed-pipe wavelength and fundamental frequency calculation.'),
 ('q13-carbon-solution',16,(81,425,217,451),'Triple-alpha fusion equation, with all four nuclides and their indices.'),
 ('q14-derive-solution',17,(109,101,305,157),'Both printed derivation methods for s = ut + ½at².'),
 ('q14-stone-solution',17,(109,175,501,250),'Complete algebraic and time-up/time-down methods for the bridge problem.'),
 ('q14-bridge-solution',17,(109,413,179,464),'Wheatstone bridge ratio and wire resistance.'),
 ('q14-doppler-solution',18,(109,121,378,208),'Doppler formula, simultaneous equations, speed and emitted frequency.'),
 ('q14-capacitance-solution',18,(109,345,174,415),'Parallel-plate capacitance formula, constant-area relation and result.'),
]:F(_key,'scheme',_page,_clip,_description,True)

# These are supplementary diagrams/data, not replacements for the printed ask.
# Keep the complete source-lifted question and stem visible beside the image.
for _t in TASKS:
 if _t['qfig']:_t['qfig_prompt']=False
for _task,_key,_page,_clip,_description in [
 ('q1vii','q1-mass-solution',3,(81,194,227,214),'Printed slope-method criterion and mass result.'),
 ('q2vi','q2-slope-solution',4,(81,348,223,365.5),'Printed gradient criterion and numerical slope.'),
 ('q2vii','q2-heat-solution',4,(81,348,271,392),'Specific heat capacity from slope divided by mass, with complete units.'),
 ('q3vii','q3-lens-solution',5,(81,221,308,282),'All four focal lengths and the mean, with the four printed criteria.'),
 ('q4iii','q4-temperature-solution',6,(81,254,189,295),'Kelvin-to-Celsius conversion.'),
 ('q6a','q6-force-solution',8,(81,62,245,96),'Horizontal component and net horizontal force calculation.'),
 ('q6b','q6-spring-solution',8,(81,96,211,149),'Hooke/Newton force relations and the full acceleration expression.'),
 ('q6c','q6-heat-solution',8,(81,153,313,214),'Heat lost in a minute and perspiration mass calculation.'),
 ('q6d','q6-string-solution',8,(81,216,242,272),'String-frequency proportionality, full formula and new frequency.'),
 ('q6f','q6-critical-solution',8,(81,310,132,360),'Refractive-index/critical-angle relation and result.'),
 ('q6k','q6-couple-solution',8,(81,545,179,587),'Motor force, moment and maximum couple.'),
 ('q7v','q7-density-solution',9,(81,175,165,224),'Air density calculation with units.'),
 ('q7vi','q7-pressure-solution',9,(81,225,355,266),'Hydrostatic and total pressure, including atmospheric pressure.'),
 ('q7viii','q7-balloon-solution',9,(81,307,330,378),'Boyle-law volume and air density at depth.'),
]:
 F(_key,'scheme',_page,_clip,_description,True)
 _t=next(t for t in TASKS if t['key']==_task)
 if _t['fig']:_t['qfig']=_t['fig'];_t['qfig_prompt']=False
 _t['fig']=_key

# Remove irrelevant setup references whose table is not needed by these asks.
for _t in TASKS:
 if _t['key']=='q4iii':_t['stem']=[MAT4]
 if _t['key']=='q4iv':_t['stem']=[ST4,P(4,'Draw a suitable graph on graph paper to show the relationship between R and θ.')]

# Keep each jointly assessed printed part on its own line, with its original
# marker. The four shared tariffs remain unchanged.
SHARED_ASKS={
 'i':('What is a semiconductor?',None),
 'ii':('Sketch the graph to show the variation of resistance with temperature for a','semiconductor thermistor.'),
 'iii':('A semiconductor diode can be used as a half‐wave rectifier. Explain the term ‘half‐','wave rectifier’.'),
 'iv':('A bridge rectifier can provide full‐wave rectification. Draw the circuit diagram of a','bridge rectifier.'),
 'v':('What device can be used to smooth the current from a bridge rectifier?',None),
 'vi':('Describe with the aid of a labelled diagram the basic structure of a bi‐polar transistor.',None),
 'vii':('The diagram below shows a thermistor used in a transistor circuit. Explain what','happens in the circuit when the thermistor is kept at a low temperature.'),
 'viii':('Draw a circuit diagram to show how a transistor can be used to make a NOT gate.',None),
 'ix':('Draw the truth table for a NOT gate',None),
}
for _t in TASKS:
 if _t['key'] in WHOLE_GROUPS:
  _t['q']=[]
  for _r in WHOLE_GROUPS[_t['key']]['romans']:
   _start,_end=SHARED_ASKS[_r]
   _t['q'] += [M('('+_r+')',12,br=True),P(12,_start,_end)]
