"""2015 Higher Physics: independent complete paper/scheme review.
All 12 paper pages and 20 scheme pages visually read; all optional branches retained.
"""
from phys_review_lib import Q, SQ, S, G, pt, anyn, allof, T
YEAR,LEVEL=2015,'hl'
REVIEWED_AT='2026-11-01'
LETTERED={5,10,11,12}
SOURCES={'paper':{'path':'examiner-reports/physics/papers/2015-hl-paper.pdf','fileid':'LC021ALP000EV.pdf','sha256':'fb8e384a4a1f07432a5c07b0d624aabd0027c55502f6d1d8f2bd36139e6dd452','pages':12},'scheme':{'path':'examiner-reports/physics/schemes/2015-hl.pdf','fileid':'LC021ALP000EV.pdf','sha256':'2e176646ae231a86afdd48c641f30e53f042813633a1b7cfb7c823dd5a1bf022','pages':20}}
PAGE_ROLES={'paper':{1:'cover',**{p:'questions' for p in range(2,12)},12:'blank'},'scheme':{1:'cover',2:'note',3:'conventions',**{p:'marking' for p in range(4,18)},18:'blank',19:'blank',20:'back-cover'}}
GLYPHS={'SymbolMT':{39:'Δ',58:'Ω',72:'ε',73:'φ',79:'λ',81:'ν',83:'π',84:'θ',111:'→',118:'∝',120:'•'}}
VERIFIED_LINES=[]
QUESTION_TOTALS={**{q:40 for q in range(1,5)},**{q:56 for q in range(5,10)},10:112,11:56,12:112}
PART_TOTALS={(10,'a'):56,(10,'b'):56,**{(11,l):7 for l in 'abcdefgh'},**{(12,l):28 for l in 'abcd'}}
BEST_OF={5:(8,7)};GROUP_TOTALS={};CHECKSUMS={};ROUTES={'Q5(j)':['quarks','not-gate']}
SCAN_PAGES={'paper':range(2,12)};SELECTION_SCAN=[]
ASK_SCAN_PAGES={'paper':range(2,12)};ASK_EXEMPT=[(10,'When light passes through a lens, it is refracted at both faces of the lens.','Narrative When statement retained in the refraction card’s stem; not an independent ask.')]
SEC='State Examinations Commission';CRIT='The scheme prints this marking criterion rather than a worked answer.'
DSL='Each complete alternative method retains the stated marks; do not add the methods together.'
P=Q
def R(text,marks,end=None,**kw):return pt(S(text,end),marks,**kw)
def C(text,marks,end=None,**kw):return pt(S(text,end),marks,kind='criterion',note=kw.pop('note',CRIT),**kw)
def EQ(page,clip,expect,marks,**kw):return G('equation',page=page,clip=clip,expect=expect,marks=marks,**kw)
TASKS=[];FIGURES={}
def U(ref,slug,label,q,rows,topic,sq,total,**kw):
 TASKS.append(T(ref+':'+slug,ref,'A' if int(ref.split('(')[0][1:])<5 else 'B',q,rows,topic,slug,sq,total,item=(slug,label),**kw))
def B(key,ref,page,start,end,sp,rows,topic,total,**kw):
 sq=kw.pop('sq',SQ(sp,start,end));TASKS.append(T(key,ref,'B',P(page,start,end),rows,topic,key,sq,total,**kw))
STEM1=P(2,'In an experiment to verify Boyle’s law','The temperature of the gas was the same for each measurement.')
GRAPH1=P(2,'Draw a suitable graph to show the relationship between the pressure of the gas and its volume.')
U('Q1','method','Boyle’s law apparatus and measurements',P(2,'Describe, with the aid of a labelled diagram, how the student obtained the data.'),[R('Diagram:',3,'method of changing volume/pressure',note='The three apparatus features share 3 marks; deduct one for each missing or incorrect part.'),R('Labelled column of air/gas',3),R('Read pressure (from gauge) and volume (from scale)',3),R('Change pressure/volume (and repeat measurements)',3)],'phys-2-1',SQ(4,'Describe, with the aid of a labelled diagram, how the student obtained the data.'),12,stem=[STEM1],fig='q1-data')
U('Q1','graph','Boyle’s law graph',GRAPH1,[C('Reciprocal values for p or V',3),C('Label axes',3),C('5 points correctly plotted',3,note='The scheme deducts one mark for each missing or incorrect point; the paper supplies six pairs, all retained.'),C('Straight line with good fit',3)],'phys-2-1',SQ(4,'Draw a suitable graph to show the relationship between the pressure of the gas and its volume.'),12,stem=[STEM1],fig='q1-data')
U('Q1','verify','Verifying Boyle’s law',P(2,'Explain how the graph verifies Boyle’s law.'),[R('Statement: Straight line through origin',3,'// p ∝ 1/V')],'phys-2-1',SQ(4,'Explain how the graph verifies Boyle’s law.'),3,stem=[STEM1,GRAPH1],fig='q1-data')
U('Q1','pressure','Pressure at 250 cubic centimetres',P(2,'Use your graph to estimate the pressure of the gas at a volume of 250 cm³.'),[C('Correct use of graph',3),R('p ≈ 108 kPa',3)],'phys-2-1',SQ(4,'Use your graph to estimate the pressure of the gas at a volume of 250 cm³.'),6,stem=[STEM1,GRAPH1],fig='q1-data')
U('Q1','temperature-change','Temperature change',P(2,'Why might the temperature of the gas have changed significantly during the experiment?'),[C('Correct reference to change in volume/pressure',3)],'phys-2-1',SQ(4,'Why might the temperature of the gas have changed significantly during the experiment?'),3,stem=[STEM1])
U('Q1','temperature-control','Keeping temperature constant',P(2,'How did the student ensure that the temperature of the gas was the same for each','measurement?'),[R('Wait (to make readings after changing volume/pressure)',4)],'phys-2-1',SQ(4,'How did the student ensure that the temperature of the gas was the same for each measurement?'),4,stem=[STEM1])
STEM2=P(3,'In an experiment to measure the specific latent heat of vaporisation of water','in a polystyrene cup. Dry steam was then added to the water.')
DATA2=P(3,'Mass of polystyrene cup','= 87.2 g')
CONST2=P(3,'(specific heat capacity of water = 4180 J kg⁻¹ K⁻¹)')
U('Q2','apparatus','Steam experiment apparatus',P(3,'Draw a labelled diagram of the apparatus used in the experiment.',before='A student used these data'),[R('Polystyrene cup with water',3),R('Steam generator',3),R('Point of detail (thermometer, steam trap, lagging, lid, mass balance, delivery tube)',3)],'phys-2-1',SQ(5,'Draw a labelled diagram of the apparatus used in the experiment.'),9,stem=[STEM2,DATA2])
U('Q2','assumptions','Assumptions about the cup',P(3,'State two assumptions that the student made about the polystyrene cup when carrying out this','calculation.'),[R('That it is a good/perfect insulator',2),pt(S('That it has a low/negligible heat capacity / specific heat capacity / that it does not gain heat (2)',piece=1,psep=' (2)'),2)],'phys-2-1',SQ(5,'State two assumptions that the student made about the polystyrene cup when carrying out this','calculation.'),4,stem=[STEM2,DATA2,P(3,'A student used these data to calculate the specific latent heat of vaporisation of water.')])
U('Q2','latent-heat','Specific latent heat of vaporisation',P(3,'Use the data given above to calculate the specific latent heat of vaporisation of water.'),[anyn(S('Δθₛ = 70 K; Δθw = 19 K; mₛ = 0.0026 kg; mw = 0.0834 kg'),4,2,sep=';',note='All four data conversions are required, 2 marks each.'),R('ml + mcΔθ = mcΔθ',6,units=[2,2,2],note='The three heat terms each carry 2 marks.'),R('(0.0026 × l) + (0.0026 × 4180 × 70) = 0.0834 × 4180 × 19',2),R('l = 2.25 × 10⁶ J kg⁻¹',2)],'phys-2-1',SQ(5,'Use the data given above to calculate the specific latent heat of vaporisation of water.'),18,stem=[STEM2,DATA2,CONST2],fig='q2-calculation')
U('Q2','accuracy','Dry steam and cooled water',P(3,'The student ensured that (i) the steam had been dried','How did each of these steps improve the accuracy of the experiment?'),[anyn(None,2,3,steps=[6,3],options=[S('(Calculations assume that) only steam is added','Otherwise the steam would have lost its latent heat (of vaporisation)'),S('Energy/heat gained = energy/heat lost')],note='Both specified steps must be explained. The first correct explanation earns 6 marks and the second 3, in either order.')],'phys-2-1',SQ(5,'The student ensured that (i) the steam had been dried','had been cooled. How did each of these steps improve the accuracy of the experiment?'),9,stem=[STEM2,DATA2],decision='Both required headings stay together because the scheme assigns a stepped 6+3 tariff in either order.')
STEM3=P(3,'In an experiment to measure the wavelength of monochromatic light','measured. This was repeated for higher order images.')
rows3=[]
for route,i in [('laser',1),('spectrometer',2)]:
 rows3 += [pt(S('Diagram: • diffraction grating'),3,route=route),pt(S('• laser labelled','// • (vapour) lamp labelled',piece=i,psep='//'),3,route=route),pt(S('• screen (+ metre stick)','// • spectrometer (with scale/protractor)',piece=i,psep='//'),3,route=route)]
U('Q3','apparatus','Diffraction apparatus',P(3,'Draw a labelled diagram of the apparatus used in the experiment.',after='The angle φ'),rows3,'phys-2-6',SQ(6,'Draw a labelled diagram of the apparatus used in the experiment.'),9,stem=[STEM3],fig='q3-data',notes=DSL)
U('Q3','first-order','Identifying first-order images',P(3,'How were the first order images identified?'),[R('They were (immediately) to either side of the image observed when no grating was present /',3,'zero order image / straight through image / central image / brightest image')],'phys-2-6',SQ(6,'How were the first order images identified?'),3,stem=[STEM3],fig='q3-data')
U('Q3','beam','Producing a beam',P(3,'How was a beam of light produced?'),[R('Laser',3,'// Collimator')],'phys-2-6',SQ(6,'How was a beam of light produced?'),3,stem=[STEM3])
U('Q3','accuracy','Most accurate diffraction angle',P(3,'Which of the four φ angles is the most accurate? Suggest a reason for your answer.'),[],'phys-2-6',SQ(6,'Which of the four φ angles is the most accurate? Suggest a reason for your answer.'),6,stem=[STEM3],fig='q3-data')
TASKS[-1]['rows']=[r for route,i in [('largest-angle',1),('sharpest-image',2)] for r in [pt(S('n = 4','// n = 1',piece=i,psep='//'),3,route=route),pt(S('Largest angle / smallest (%) error','// Sharpest image',piece=i,psep='//'),3,route=route)]]
TASKS[-1]['notes']='The chosen order and its reason must be linked. Each complete answer is worth 6 marks.'
U('Q3','wavelength','Wavelength from diffraction angles',P(3,'Calculate the wavelength of the monochromatic light.'),[R('d = 1/80000 = 1.25 × 10⁻⁵ m',3),R('nλ = dSinθ',6),C('Correct substitution',3),R('λ ≈ 5.0 × 10⁻⁷ m',3)],'phys-2-6',SQ(6,'Calculate the wavelength of the monochromatic light.'),15,stem=[STEM3],fig='q3-data',notes='The measured φ is the angle between matching images on both sides; use θ = φ/2 in the diffraction formula.')
U('Q3','denser-grating','Replacing the grating',P(3,'What would be the effect on the pattern produced if this diffraction grating was replaced with','a diffraction grating of 500 lines per mm?'),[R('Fewer images seen / images more spread out / larger angles',4)],'phys-2-6',SQ(6,'What would be the effect on the pattern produced if this diffraction grating was replaced with','a diffraction grating of 500 lines per mm?'),4,stem=[STEM3])
STEM4=P(4,'In an experiment to measure the variation of the resistance R','temperature θ, a student recorded the following data.')
GRAPH4=P(4,'Using the recorded data, plot a graph to show the variation of the resistance of the metallic','conductor with its temperature.')
SECOND4=P(4,'The student then completed an experiment','for the thin metallic filament of a bulb. Data were recorded and the following graph plotted.')
U('Q4','graph','Resistance–temperature graph',GRAPH4,[C('Correctly labelled axes',3),C('7 points correctly plotted',5,note='Deduct one mark for each missing or incorrect point. All eight pairs printed in the paper are retained.'),C('Straight line with good fit',3)],'phys-3-3',SQ(7,'Using the recorded data, plot a graph to show the variation of the resistance of the metallic','conductor with its temperature.'),11,stem=[STEM4],fig='q4-data')
U('Q4','slope','Rate of resistance change',[P(4,'Use your graph to estimate'),P(4,'the rate of change of resistance with respect to temperature for the metallic conductor')],[R('Correct rate/slope from graph ≈ 0.033 Ω K⁻¹',3,note='The scheme also accepts Ω °C⁻¹.')],'phys-3-3',SQ(7,'the rate of change of resistance with respect to temperature for the metallic conductor'),3,stem=[STEM4,GRAPH4],fig='q4-data')
U('Q4','ice-resistance','Resistance in melting ice',[P(4,'Use your graph to estimate'),P(4,'the resistance of the metallic conductor when it is immersed in melting ice.')],[C('Correct intercept',3,'// Correct use of rate/slope'),R('R ≈ 5.5 Ω',3)],'phys-3-3',SQ(7,'the resistance of the metallic conductor when it is immersed in melting ice.'),6,stem=[STEM4,GRAPH4],fig='q4-data')
U('Q4','bulb-experiment','Filament-bulb experiment',P(4,'Describe, with the aid of a circuit diagram, how the student carried out this second experiment.'),[C('• circuit',6,'• filament bulb',note='Six required circuit features; deduct one mark for each missing or incorrect part.'),R('Correct arrangement – voltmeter across filament bulb, ammeter in series',4,units=[2,2]),R('Measure voltage and current',3),R('Vary voltage (and repeat measurements)',3)],'phys-3-3',SQ(7,'Describe, with the aid of a circuit diagram, how the student carried out this second experiment.'),16,stem=[STEM4,SECOND4],fig='q4-curve')
U('Q4','curve-explanation','Explaining the bulb curve',P(4,'Use the findings of the first experiment to explain the shape of the graph in the second','experiment.'),[R('Temperature increases as current increases',2),R('Resistance increases as temperature increases',2)],'phys-3-3',SQ(7,'Use the findings of the first experiment to explain the shape of the graph in the second experiment.'),4,stem=[STEM4,GRAPH4,SECOND4],qfig='q4-context')
CONST5=P(5,'(speed of sound in air = 340 m s⁻¹; solar constant = 1.36 kW m⁻²)')
B('5a','Q5(a)',5,'A hurler strikes a sliotar','horizontally in three seconds?',8,[R('vH = 41Cos30 = 35.51 m s⁻¹',4),R('s (= vt) = 35.51 × 3 = 106.52 m',3)],'phys-1-1',7,sq=SQ(8,'A hurler strikes a sliotar','horizontal. How far does the ball travel horizontally in three seconds?'),fig='q5-hurler')
B('5b','Q5(b)',5,'Describe the movement of a particle','harmonic motion.',8,[R('Acceleration is proportional to',4,'// Formula'),R('Displacement (from a point on the path) // Notation',3)],'phys-1-6',7,sq=SQ(8,'Describe the movement of a particle that is undergoing simple harmonic motion.'))
B('5c','Q5(c)',5,'The refractive index of haematite is 3.2. What is its critical angle?',None,8,[R('n = 1/SinC',4),R('C = 18.21°',3)],'phys-2-3',7)
B('5d','Q5(d)',5,'What frequency would be detected by an observer','emitting a sound of frequency 512 Hz approaches at a velocity of 28 m s⁻¹?',8,[R('f’ = fc/(c – u)',4),R('f’ = 557.95 Hz',3)],'phys-2-7',7,stem=[CONST5],sq=SQ(8,'What frequency would be detected by an observer','frequency 512 Hz approaches at a velocity of 28 m s⁻¹?'))
B('5e','Q5(e)',5,'Calculate the energy from the Sun','90 minutes.',8,[R('90 × 60 = 5400 s',4,'// 106 × 68 = 7208 m²'),R('E = 5.3 × 10¹⁰ J',3)],'phys-1-4',7,stem=[CONST5],fig='q5-pitch')
B('5f','Q5(f)',5,'Write an expression for the charge stored on one','permittivity of the dielectric.',8,[R('C = Q/V or C = εA/d',4),R('Q = εAV/d',3)],'phys-3-2',7,sq=SQ(8,'Write an expression for the charge stored on one plate','the permittivity of the dielectric.'))
B('5g','Q5(g)',5,'Define the ampere, the SI unit of current.',None,8,[R('Current which in two (parallel) conductors',2),R('Placed one metre apart (in a vacuum)',2),R('Causes a force of 2 × 10⁻⁷ N m⁻¹',3,note='Deduct one mark for missing or incorrect units.')],'phys-3-5',7,notes='This is the SI definition examined in the 2015 paper.')
B('5h','Q5(h)',5,'Name the wire that contains the fuse in a three-pin plug.','What colour is this wire?',8,[R('Live',4),R('Brown',3,note='The scheme accepts red.')],'phys-3-3',7,fig='q5-plug')
B('5i','Q5(i)',5,'The first artificial transmutation of an atom was achieved by','equation for this transmutation.',8,[EQ(8,(83,622,195,645),'N¹⁴₇ + He⁴₂ → O¹⁷₈ + H¹₁',7,note='Deduct one mark for each missing or incorrect part.')],'phys-4-5',7,sq=SQ(8,'The first artificial transmutation of an atom was achieved by Rutherford','proton. Write a nuclear equation for this transmutation.'),fig='q5-nuclear-solution')
B('5j-quarks','Q5(j)',5,'Give the quark composition of (i) the proton and (ii) the anti-neutron.',None,8,[R('up, up, down',4),R('anti-up, anti-down, anti-down',3)],'phys-4-5',7,route='quarks',notes='Symbols are accepted.')
B('5j-not','Q5(j)',5,'Draw the symbol and truth table for a NOT gate.',None,8,[C('Symbol',4),R('0 → 1 and 1 → 0',3)],'phys-3-3',7,route='not-gate',fig='q5-not-solution')
STEM6=P(6,'In the circular orbit of a satellite around the Earth','universal gravitation.')
GPS6=P(6,'A Global Positioning Systems (GPS) receiver','a period of 12 hours.')
CONST6=P(6,'(mass of Earth = 5.97 × 10²⁴ kg; radius of Earth = 6371 km)')
U('Q6','centripetal','Centripetal force',P(6,'Explain what is meant by centripetal force.'),[R('Force (towards centre) required to maintain circular motion',3)],'phys-1-6',SQ(9,'Explain what is meant by centripetal force.'),3,stem=[STEM6])
U('Q6','gravitation','Newton’s law of gravitation',P(6,'State Newton’s law of universal gravitation.'),[R('F = Gm₁m₂/d²',3,'// Force ∝ product of two masses'),R('Notation',3,'// Force ∝ 1/(distance between masses)²')],'phys-1-5',SQ(9,'State Newton’s law of universal gravitation.'),6,stem=[STEM6])
U('Q6','period-derivation','Satellite period derivation',P(6,'Derive the relationship between the period of a satellite,','the radius of its orbit and the mass of the Earth.'),[R('Centripetal force = gravitational force',3),R('mv²/r = Gm₁m₂/r²',3),R('v² = Gm/r',3),R('T = 2πr/v',3),R('T² = 4π²r³/Gm',3)],'phys-1-6',SQ(9,'Derive the relationship between the period of a satellite,','Earth.'),15,stem=[STEM6],fig='q6-derivation')
for slug,label,ask,rows,total in [
 ('height','GPS satellite height','the height of a GPS satellite above the Earth’s surface',[R('T² = 4π²r³/Gm',3),C('Correct substitution',3),R('r = 2.66 × 10⁷ m',3),R('h = 2.023 × 10⁷ m',3)],12),
 ('speed','GPS satellite speed','the speed of a GPS satellite',[R('v² = Gm/r',3),R('v = 3.869 × 10³ m s⁻¹',3)],6),
 ('signal-time','Minimum GPS signal travel time','the minimum time it takes a GPS signal to travel from the satellite to a receiver on the',[R('v = s/t',3),R('t = 0.067 s',3)],6)]:
 end='surface of the Earth.' if slug=='signal-time' else None
 U('Q6',slug,label,[P(6,'Calculate',after='a period of 12 hours.'),P(6,ask,end)],rows,'phys-1-5' if slug!='signal-time' else 'phys-2-4',SQ(9,ask,end),total,stem=[STEM6,GPS6,CONST6],fig='q6-globe')
U('Q6','geostationary','Why GPS satellites are not geostationary',P(6,'Explain why GPS satellites are not classed as geostationary satellites.'),[R('Periodic time is not 24 hours',4,'// Not in the same place above the Earth')],'phys-1-6',SQ(9,'Explain why GPS satellites are not classed as geostationary satellites.'),4,stem=[GPS6],fig='q6-globe')
U('Q6','spectrum','Next electromagnetic band',P(6,'Radio-waves, such as those used by GPS satellites,','radiation types. What type of electromagnetic radiation has the next lowest frequency?'),[R('Microwaves',4,note='The scheme also accepts infrared.')],'phys-2-4',SQ(9,'Radio-waves, such as those used by GPS satellites,','radiation types. What type of electromagnetic radiation has the next lowest frequency?'),4)
STEM7=P(6,'X-rays have two important uses in medicine: imaging and radiation therapy.')
VOLT7=P(6,'A potential difference of 50 kV is applied across an X-ray tube.')
PHOTO7=P(6,'The large atoms found in bones','The X-ray photons absorbed by large atoms can cause the photoelectric effect to occur.')
U('Q7','xray-production','Producing X-rays',P(6,'Describe, with the aid of a labelled diagram of an X-ray tube, how X-rays are','produced.'),[C('Diagram: cathode, anode, tube, vacuum',4,note='Deduct one mark for each missing or incorrect part.'),R('Electrons produced by thermionic emission at cathode / heating of cathode',4),R('High voltage applied to electrons',3),R('Electrons strike target and produce X-rays',3)],'phys-4-2',SQ(10,'Describe, with the aid of a labelled diagram of an X-ray tube, how X-rays are produced.'),14,stem=[STEM7],fig='q7-hand')
U('Q7','electron-speed','Maximum electron speed',[P(6,'Calculate',after='A potential difference of 50 kV'),P(6,'the maximum velocity of an electron in the tube')],[R('½mv² or eV',3),R('½mv² = eV',3),R('v = 1.3 × 10⁸ m s⁻¹',3)],'phys-4-2',SQ(10,'the maximum velocity of an electron in the tube'),9,stem=[STEM7,VOLT7],fig='q7-hand')
U('Q7','wavelength','Minimum X-ray wavelength',[P(6,'Calculate',after='A potential difference of 50 kV'),P(6,'the minimum wavelength of the X-rays produced by the tube.')],[R('½mv² or eV = hc/λ',3),R('½(9.1 × 10⁻³¹)(1.3 × 10⁸ )² or 1.6 × 10⁻¹⁹ × 50000 = (6.6 × 10⁻³⁴ × 3.0 × 10⁸)/λ',3),R('λ = 2.5 × 10⁻¹¹ m',3)],'phys-4-2',SQ(10,'the minimum wavelength of the X-rays produced by the tube.'),9,stem=[STEM7,VOLT7],fig='q7-wavelength-solution')
U('Q7','photoelectric','Photoelectric effect',P(6,'What is the photoelectric effect?'),[R('Emission of electrons',3),R('Using electromagnetic radiation / photons / light (of suitable frequency)',3)],'phys-4-2',SQ(10,'What is the photoelectric effect?'),6,stem=[STEM7,PHOTO7],fig='q7-hand')
U('Q7','photoelectric-demo','Demonstrating the photoelectric effect',P(6,'Describe a laboratory experiment to demonstrate the photoelectric effect.'),[R('Apparatus: Gold leaf electroscope',3),R('Shine (uv) light',3),R('The leaves collapse',3)],'phys-4-2',SQ(10,'Describe a laboratory experiment to demonstrate the photoelectric effect.'),9,stem=[PHOTO7])
U('Q7','einstein','Einstein’s explanation',P(6,'Outline Einstein’s explanation of the photoelectric effect.'),[anyn(None,3,3,options=[S('• Correct reference to photon(s)'),S('• Each photon gives all its energy to one electron'),S('• Correct reference to work function / threshold frequency'),S('Correct equation')])],'phys-4-2',SQ(10,'Outline Einstein’s explanation of the photoelectric effect.'),9,stem=[PHOTO7,P(6,'Albert Einstein received a Nobel Prize in 1921 for his explanation of the photoelectric effect.')],decision='One response with any three of all four scheme points; no combinations.')
STATIC8=P(7,'Both Van de Graaff generators and gold leaf electroscopes','in the laboratory.')
POINT8=P(7,'A Van de Graaff generator can be used to demonstrate point discharge.')
DOME8=P(7,'The polished spherical dome of a Van de Graaff generator has a diameter of','40 cm and a charge of +3.8 µC.')
U('Q8','field-definition','Electric field strength',P(7,'Define electric field strength.'),[R('E = F/q',3,'// Force per'),R('Notation',3,'// Unit charge')],'phys-3-2',SQ(11,'Define electric field strength.'),6)
U('Q8','electroscope','Gold-leaf electroscope',P(7,'Draw a labelled diagram of a gold leaf electroscope.'),[R('Metal cap attached to gold leaves',3),R('Metal case (and glass window)',3),R('Insulation between case and leaves + cap',3)],'phys-3-1',SQ(11,'Draw a labelled diagram of a gold leaf electroscope.'),9,stem=[STATIC8])
U('Q8','induction','Charging by induction',P(7,'Describe how it can be given a negative charge by induction.'),[R('Positively charged rod',3),R('Bring rod close to cap',3),R('Earth cap',3),R('Remove earth (and then remove rod)',2)],'phys-3-1',SQ(11,'Describe how it can be given a negative charge by induction.'),11,stem=[STATIC8,P(7,'Draw a labelled diagram of a gold leaf electroscope.')])
U('Q8','point-discharge','Explaining point discharge',P(7,'Explain, with the aid of a labelled diagram, how point discharge occurs.'),[C('Diagram with concentration of charge at point',3),R('Air/gas near the point is ionised (by large electric field)',3),R('Opposite charges neutralise the charge at the point',3)],'phys-3-1',SQ(11,'Explain, with the aid of a labelled diagram, how point discharge occurs.'),9,stem=[POINT8])
U('Q8','discharge-demo','Demonstrating point discharge',P(7,'Describe an experiment to demonstrate point discharge.'),[C('Apparatus',3),R('Charge pointed conductor',3),R('Observe point discharge / ionic wind using e.g. candle',3)],'phys-3-1',SQ(11,'Describe an experiment to demonstrate point discharge.'),9,stem=[POINT8])
U('Q8','dome-field','Field outside a charged dome',P(7,'What is the electric field strength at a point 4 cm from the surface','of the dome?'),[R('d = 24 cm',3),R('E = Q/4πεd²',6,note='The denominator is 4πεd². The scheme also allows F = q₁q₂/(4πεd²) and E = F/q, worth 3 marks each.'),R('E = 5.9 × 10⁵ N C⁻¹ away (from the centre of the dome)',3,note='Deduct one mark if the direction is missing or incorrect.')],'phys-3-2',SQ(11,'What is the electric field strength at a point 4 cm from the surface of the dome?'),12,stem=[DOME8],fig='q8-dome',cells='Distance 3, field formula 6 (or two linked formulae 3+3), result and direction 3; the alternative six marks are not added twice.')
STEM9=P(7,'Musical instruments produce stationary (standing) waves.','Resonance also occurs in many instruments.')
GUITAR9=P(7,'A guitar is a string instrument.','string and on two other factors.')
for slug,label,ask,rows,total in [
 ('standing','Stationary waves','What are stationary waves?',[R('The amplitude of the wave at any point is constant',3,'// There is no net transfer of energy')],3),
 ('production','Producing stationary waves','How are they produced?',[R('Waves with same frequency and amplitude',3),R('Travelling in opposite directions meet',3)],6),
 ('resonance','Resonance','What is resonance?',[R('Transfer of energy',3),R('Between two bodies with the same/similar (natural) frequency',3)],6),
 ('resonance-demo','Demonstrating resonance','Describe a laboratory experiment to demonstrate resonance.',[C('Apparatus',3),C('Method',3),C('Observation',3)],9)]:
 U('Q9',slug,label,P(7,ask,ask),rows,'phys-2-6',SQ(12,ask),total,stem=[STEM9])
U('Q9','string-factors','Other string-frequency factors',P(7,'What are the two other factors?'),[R('Length',3),R('Mass per unit length / linear density',3)],'phys-2-6',SQ(12,'What are the two other factors?'),6,stem=[GUITAR9],fig='q9-guitar',notes='The scheme accepts symbols for both factors.')
U('Q9','tension','Effect of increasing string tension',P(7,'What effect does increasing the tension of the string from','36 N to 81 N have on the frequency of the string?'),[R('Increase by',3),R('Factor of 1.5',3)],'phys-2-6',SQ(12,'What effect does increasing the tension of the string from 36 N to 81 N have on the frequency of the','string?'),6,stem=[GUITAR9],fig='q9-guitar')
U('Q9','harmonics','Open and closed pipe harmonics',P(7,'Explain, with the aid of labelled diagrams, why a pipe open at only one','end produces half the number of harmonics as a pipe open at both ends.'),[C('Diagram of first harmonic for open pipe',3),C('Diagram of other harmonic for same open pipe',3),C('Diagram of first harmonic for closed pipe',3),C('Diagram of other harmonic for same closed pipe',3),R('All harmonics for open pipe, only odd harmonics for closed pipe',2)],'phys-2-6',SQ(12,'Explain, with the aid of labelled diagrams, why a pipe open at only one end produces half the','number of harmonics as a pipe open at both ends.'),14,stem=[STEM9])
U('Q9','whistle-length','Tin whistle length',P(7,'How long is the pipe?'),[R('v = fλ',3),R('l = λ/2 = 0.29 m',3)],'phys-2-6',SQ(12,'How long is the pipe?'),6,stem=[P(7,'A tin whistle consists of a pipe which is open at both ends.','on it are covered.'),P(7,'(speed of sound in air = 340 m s⁻¹)')],fig='q9-whistle')
NEUTRINO10=P(8,'There are about a trillion neutrinos from the Sun','Leptons are not subject to the strong nuclear force.')
PAULI10=P(8,'Pauli proposed that a neutrino is emitted during beta-decay.')
BETA10=P(8,'During beta-decay, a neutron decays with the emission of a proton, an electron and a neutrino.')
FIELD10=P(8,'In a cloud chamber an electron travels perpendicular','electron has a speed of 1.45 × 10⁸ m s⁻¹.')
U('Q10(a)','weak-force','Force experienced by neutrinos',P(8,'What is the principal force that neutrinos experience?'),[R('Weak (nuclear force)',3)],'phys-4-5',SQ(13,'What is the principal force that neutrinos experience?'),3,stem=[NEUTRINO10],fig='q10-hand')
U('Q10(a)','leptons','Two other leptons',P(8,'Electrons are also members of the lepton family. Name two other leptons.'),[anyn(S('Muon, tau, positron, anti-muon, anti-tau'),2,3,sep=',')],'phys-4-5',SQ(13,'Electrons are also members of the lepton family. Name two other leptons.'),6,stem=[NEUTRINO10],fig='q10-hand',decision='One two-of-five choice response with every accepted lepton retained.')
U('Q10(a)','strong-force','Particle subject to the strong force',P(8,'Name one fundamental particle that is subject to the strong nuclear force.'),[R('Quark',3,note='The scheme awards 2 marks for a non-fundamental hadron, for example a proton.')],'phys-4-5',SQ(13,'Name one fundamental particle that is subject to the strong nuclear force.'),3,stem=[NEUTRINO10])
U('Q10(a)','pauli','Pauli’s neutrino proposal',P(8,'Why did he make this proposal?'),[R('Momentum/energy',2),R('Not conserved',2)],'phys-4-5',SQ(13,'Why did he make this proposal?'),4,stem=[PAULI10])
U('Q10(a)','beta-equation','Beta-decay equation',P(8,'Write a nuclear equation to represent beta-decay.'),[EQ(13,(84,343,159,368),'n¹₀ → H¹₁ + e⁰₋₁ + ν',10,units=[1]*10)],'phys-4-4',SQ(13,'Write a nuclear equation to represent beta-decay.'),10,stem=[BETA10],fig='q10-beta-solution',cells='The scheme awards ten one-mark components to the complete equation, not ten separate tasks.',notes='The 2015 paper and scheme call the emitted particle a neutrino and show ν. In modern notation beta-minus decay emits an electron antineutrino; the original SEC equation is retained in the source image.')
U('Q10(a)','beta-energy','Energy released in beta decay',P(8,'Calculate the energy released, in MeV, during beta-decay.'),[R('Loss in mass = 1.395 × 10⁻³⁰ kg',3),R('E = mc²',3),R('E = 1.25 × 10⁻¹³ J',3),R('E = 0.78 (MeV)',3)],'phys-4-5',SQ(13,'Calculate the energy released, in MeV, during beta-decay.'),12,stem=[BETA10])
U('Q10(a)','detection','Detecting neutrinos',P(8,'An electron can be detected in a cloud chamber.','neutrino. Explain why.'),[R('No charge / very small mass / does not ionise matter / interacts weakly with matter',6,note='The historical scheme also accepts “no mass”; neutrinos have nonzero mass.')],'phys-4-5',SQ(13,'An electron can be detected in a cloud chamber.','neutrino. Explain why.'),6,stem=[NEUTRINO10])
U('Q10(a)','radius','Electron path radius',FIELD10,[R('Bqv or mv²/r',3),R('Bqv = mv²/r',3),R('r = 9.16 × 10⁻³ m',3)],'phys-3-5',SQ(13,'In a cloud chamber an electron travels perpendicular','electron has a speed of 1.45 × 10⁸ m s⁻¹.'),9,fig='q10-radius-solution')
U('Q10(a)','neutrino-path','Neutrino path in the field',P(8,'Describe the path of a neutrino in the same magnetic field.'),[R('No deviation',3)],'phys-3-5',SQ(13,'Describe the path of a neutrino in the same magnetic field.'),3,stem=[FIELD10])
MOTOR10=P(8,'Loudspeakers, d.c. motors and galvanometers are all based on the principle that a','current-carrying conductor in a magnetic field experiences a force.')
U('Q10(b)','motor-demo','Force on a current-carrying conductor',P(8,'Describe a laboratory experiment to demonstrate this principle.'),[R('Metal foil across d.c. source in a magnetic field',3),R('Close switch / introduce magnetic field',3),R('Foil moves',3)],'phys-3-5',SQ(14,'Describe a laboratory experiment to demonstrate this principle.'),9,stem=[MOTOR10])
U('Q10(b)','loudspeaker','Moving-coil loudspeaker',P(8,'Describe, with the aid of a labelled diagram, the principle of operation','of the moving-coil loudspeaker.'),[R('Coil, magnet, cone',3,note='Deduct one mark for each missing or incorrect part.'),R('A.c. signal',3),R('Force on coil which changes direction',3),R('Coil and cone vibrate',3)],'phys-3-5',SQ(14,'Describe, with the aid of a labelled diagram, the principle of operation of a moving-coil','loudspeaker.'),12,stem=[MOTOR10],fig='q10-speaker')
U('Q10(b)','motor-energy','Motor energy conversion',P(8,'What is the principal energy conversion that takes place in a d.c. motor?'),[R('Electrical energy to kinetic energy',3)],'phys-1-4',SQ(14,'What is the principal energy conversion that takes place in a d.c. motor?'),3,stem=[MOTOR10])
COMM=P(8,'State the function of (i) the commutator and (ii) the carbon brushes in a','d.c. motor.')
U('Q10(b)','commutator','Function of the commutator',[dict(COMM,piece=1,psep=' (i)'),dict(COMM,piece=[2,1],psep=[' (i)',' and (ii)'])],[R('To change the direction of the',3,'// To keep the torque from'),R('Current',3,'// Changing direction')],'phys-3-5',SQ(14,'State the function of (i) the commutator;'),6,stem=[MOTOR10],notes='The commutator reverses the coil current so the torque continues in the same rotational direction.')
U('Q10(b)','brushes','Function of carbon brushes',[dict(COMM,piece=1,psep=' (i)'),dict(COMM,piece=2,psep=' (ii)')],[R('Electrical contact between power supply and commutator/coil',3)],'phys-3-5',SQ(14,'the carbon brushes in a d.c. motor.'),3,stem=[MOTOR10])
U('Q10(b)','torque','Maximum motor torque',P(8,'The magnetic flux density of the field in a d.c. motor is 5.5 T','has 500 turns. Calculate the maximum torque exerted by the motor.'),[R('F = length × I × B',3,'// BIA'),R('F = 264 N',3,'// × 500'),R('Torque = F × 0.08 = 21.12 N m',3)],'phys-3-5',SQ(14,'The magnetic flux density of the field in a d.c. motor is 5.5 T','exerted by the motor.'),9,stem=[MOTOR10],fig='q10-torque-solution')
U('Q10(b)','voltmeter','Converting a galvanometer to a voltmeter',P(8,'A galvanometer has an internal resistance of 90 Ω','deflection 5 V.'),[R('Place a resistor',2),R('In series with the galvanometer',3),R('V = IR + Ir',3),R('5 = (0.01 × R) + (0.01 × 90)',3),R('R = 410 Ω',3)],'phys-3-3',SQ(14,'A galvanometer has an internal resistance of 90 Ω','deflection 5 V.'),14)
PASSAGE11=P(9,'In the years since his death','(Adapted from Tesla: Inventor of the Electrical Age, W Bernard Carlson, Princeton University Press, 2013)')
for letter,ask,rows,topic,sq in [
 ('a','Define the tesla.',[R('Force of 1 N when',4),R('1 A flows through a wire of length 1 m',3,'// 1 C moves with a velocity of 1 m s⁻¹')],'phys-3-4',None),
 ('b','Sketch voltage-time graphs for (i) an a.c. supply and (ii) a d.c. supply.',[C('Labelled axes and correct sine wave',4),C('Labelled axes and correct shape',3)],'phys-3-3','Sketch a voltage-time graph for (i) an a.c. supply and (ii) a d.c. supply.'),
 ('c','Explain the term electromagnetic induction.',[R('Emf induced by',4),R('Changing magnetic flux / magnetic field',3)],'phys-3-6',None),
 ('d','Why does a transformer not work with direct current?',[R('Current not changing',4),R('Magnetic flux / magnetic field not changing',3)],'phys-3-6',None),
 ('e','Why is it inefficient to use low voltage when transmitting electricity?',[R('Large current',4),R('More heat lost',3)],'phys-3-3',None),
 ('f','The peak voltage of an a.c. supply is 321 V. Calculate the rms voltage.',[R('Use of √2',4),R('227 V',3)],'phys-3-3',None),
 ('g','Explain why it is necessary to use rms values when comparing a.c. and d.c. electricity.',[R('So as to make the power output',4,'// Mean/average'),R('Equivalent between a.c. and d.c.',3,'// Correct explanation')],'phys-3-3','Explain why it is necessary to use the rms voltage when comparing a.c. and d.c. electricity.'),
 ('h','Give one advantage and one disadvantage of electric cars.',[R('e.g. fewer carbon emissions',4),R('Disadvantage: e.g. short range / expensive batteries',3)],'phys-1-4',None)]:
 B('11'+letter,'Q11('+letter+')',9,ask,None,15,rows,topic,7,stem=[PASSAGE11],fig='q11-passage',sq=SQ(15,sq or ask))
SKIER12=P(10,'A downhill skier of mass 71 kg started from rest','ski course. Her loss of elevation was 90 m.')
CONST12=P(10,'(acceleration due to gravity = 9.8 m s⁻²)')
STOP12=P(10,'She then ploughed into a snow drift and came to a stop in a time of 0.8 seconds.')
U('Q12(a)','newton','Newton’s second law',P(10,'State Newton’s second law of motion.'),[R('Force is proportional to',3,'// F = ma'),R('Rate of change of momentum',3,'// Notation')],'phys-1-2',SQ(16,'State Newton’s second law of motion.'),6)
U('Q12(a)','conversion','Skier’s energy conversion',P(10,'What is the principal energy conversion that is','course?'),[R('(Gravitational) potential (energy) to',2),R('Kinetic (energy)',2)],'phys-1-4',SQ(16,'What is the principal energy conversion that is taking place as the skier travels along the','course.'),4,stem=[SKIER12],fig='q12-skier')
U('Q12(a)','speed','Skier’s maximum speed',P(10,'Ignoring friction, calculate her maximum','velocity when she has travelled 400 m.'),[R('mgh = ½mv²',6,'// v² = u² + 2as',note='If no other marks are awarded, the scheme allows 3 marks for a correct energy formula.'),R('v = 42 m s⁻¹',3)],'phys-1-4',SQ(16,'Ignoring friction, calculate her maximum velocity when she has travelled 400 m.'),9,stem=[SKIER12,CONST12],fig='q12-skier')
U('Q12(a)','snow-force','Force on the snow drift',P(10,'What is the force that she exerts on the snow drift?'),[R('F = Δmv/Δt',3),R('F = 3727.5 N',3)],'phys-1-2',SQ(16,'What is the force that she exerts on the snow drift?'),6,stem=[SKIER12,CONST12,STOP12],fig='q12-skier')
U('Q12(a)','reaction','Force on the skier',P(10,'What force does the snow drift exert on her?'),[R('F = 3727.5 (N) in opposite direction',3,note='Deduct one mark if direction is missing or incorrect.')],'phys-1-2',SQ(16,'What force did the snow drift exert on her?'),3,stem=[SKIER12,CONST12,STOP12,P(10,'What is the force that she exerts on the snow drift?')],fig='q12-skier')
U('Q12(b)','refraction','Ray through a lens section',P(10,'Copy the diagram on the right into your answer book and','lens. Include the normal at both faces.'),[C('First correct refraction',3),C('Second correct refraction',3)],'phys-2-3',SQ(16,'Copy the diagram on the right into your answer book and complete the path of the light','ray through the section of the lens. Include the normal to the ray at both faces.'),6,stem=[P(10,'When light passes through a lens, it is refracted at both faces of the lens.')],fig='q12-lens')
U('Q12(b)','virtual','Virtual image in a converging lens',P(10,'Draw a ray diagram to show the formation of a virtual image','in a converging lens.'),[R('Object inside focal point',3),C('Two correct rays through converging lens',3),C('Correct position of image at apparent point of intersection of emerging rays',3)],'phys-2-3',SQ(16,'Draw a ray diagram to show the formation of a virtual image in a converging lens.'),9)
U('Q12(b)','power','Power of combined lenses',P(10,'A converging lens of focal length 20 cm and a diverging lens','Calculate the power of the combination.'),[R('P₁ = 1/0.2 or P₂ = 1/–0.08',3),R('P = P₁ + P₂',3),R('P = –7.5 m⁻¹',3)],'phys-2-3',SQ(16,'A converging lens of focal length 20 cm and a diverging lens of focal length 8 cm are','placed in contact. Calculate the power of the combination.'),9)
U('Q12(b)','eye','Eye defect corrected by converging lenses',P(10,'What eye defect can be corrected using converging lenses?'),[R('Long-sightedness / hyperopia',4)],'phys-2-3',SQ(16,'What eye defect can be corrected using converging lenses?'),4)
THERMO12=P(11,'A thermometer uses a thermometric property to','thermocouple thermometer is emf.')
U('Q12(c)','terms','Thermometric property and emf',P(11,'Explain the underlined terms.'),[R('Thermometric property: one that changes (measurably)',3),R('with temperature',3),R('Emf: voltage / work done in moving unit charge / electromotive force',3)],'phys-2-1',SQ(17,'Explain the underlined terms.'),9,stem=[THERMO12],qfig='q12-thermometric-question',fig='q12-thermocouple',decision='One comparison of the two underlined terms; all 6+3 marks retained with the original underlining.')
U('Q12(c)','unit','SI temperature unit',P(11,'What is the SI unit of temperature?','What is the SI unit of temperature?'),[R('Kelvin / K',3)],'phys-2-1',SQ(17,'What is the SI unit of temperature?','What is the SI unit of temperature?'),3,stem=[THERMO12])
U('Q12(c)','unit-advantage','Advantage of the SI temperature unit',P(11,'What is the SI unit of temperature?','of using this unit in scientific measurements.',piece=2,psep='? '),[R('Always positive / reference to gas laws',3)],'phys-2-1',SQ(17,'What is the SI unit of temperature? Give an advantage of using this unit in scientific','measurements.'),3,stem=[THERMO12,P(11,'What is the SI unit of temperature?','What is the SI unit of temperature?')])
U('Q12(c)','thermocouple','Thermocouple experiment',P(11,'Describe a laboratory experiment to demonstrate the','principle of operation of a thermocouple.'),[R('Two different metals',3),R('Two junctions held at different temperatures',3),R('Voltage/emf measured',3)],'phys-2-1',SQ(17,'Describe a laboratory experiment to demonstrate the principle of operation of a thermocouple.'),9,stem=[THERMO12],fig='q12-thermocouple')
U('Q12(c)','advantage','Thermocouple advantage',P(11,'Give an advantage of using a thermocouple thermometer instead of a mercury-in-glass','thermometer.'),[anyn(S('Less fragile, wider temperature range, mercury is toxic etc.'),1,4,sep=',',open_list=True)],'phys-2-1',SQ(17,'Give an advantage of using a thermocouple thermometer instead of a mercury-in-glass','thermometer.'),4,stem=[THERMO12],fig='q12-thermocouple')
RADON12=P(11,'Radon is a radioactive gas which is present in some rocks.','houses and cause health concerns.')
U('Q12(d)','radioactive','Radioactivity',P(11,'What is meant by the term radioactive?'),[R('(Spontaneous) disintegration of a nucleus',3,note='Deduct one mark for “atom” instead of “nucleus”.'),R('With the emission of radiation',3)],'phys-4-4',SQ(17,'What is meant by the term radioactive?'),6,stem=[RADON12],fig='q12-radon')
rows12=[]
for route,i in [('geiger-muller',1),('solid-state',2)]:
 parts=[S('Diagram: • cathode','// Diagram: • cathode',piece=i,psep='//'),S('• wire anode','• anode',piece=i,psep='//'),S('• (low pressure inert) gas','• semiconductor material',piece=i,psep='//'),S('• case','• housing',piece=i,psep='//')]
 diagram=allof([(None,x) for x in parts],4,note='All four features belong to this detector. Deduct one mark for each missing item.')
 diagram['route']=route
 rows12 += [pt(S('Geiger-Müller tube/counter','// Solid-state detector',piece=i,psep='//'),6,route=route),diagram,pt(S('Ionisation of gas','// Free electrons + holes produced',piece=i,psep='//'),3,route=route)]
U('Q12(d)','detector','Radiation detector',P(11,'Name a detector of radiation and describe, with the aid of a','labelled diagram, its principle of operation.'),rows12,'phys-4-4',SQ(17,'Name a detector of radiation and describe, with the aid of a labelled diagram, its principle of','operation.'),13,stem=[RADON12],fig='q12-detector-solution',notes=DSL)
U('Q12(d)','remaining','Radon atoms after one day',P(11,'How many radon–210 atoms will remain after one day?'),[R('10 half lives',3),R('½¹⁰ / use factor of 2 correctly',3),R('4.4 × 10¹²',3)],'phys-4-4',SQ(17,'How many radon–210 atoms will remain after 1 day?'),9,stem=[RADON12,P(11,'Radon–210 decays by alpha-emission with a half-life of','of this isotope.')],fig='q12-radon')
FIGURES={
 'q1-data':('paper',2,(158,212,440,276),SEC,[],'All six gas volume and pressure readings.',False),
 'q2-calculation':('scheme',5,(54,361,545,421),SEC,[],'All latent-heat data conversions, heat balance, substitution and result.',True),
 'q3-data':('paper',3,(191,556,407,617),SEC,[],'All four diffraction orders and measured angles between matching left and right images.',False),
 'q4-data':('paper',4,(91,117,541,175),SEC,[],'All eight temperature and resistance readings.',False),
 'q4-curve':('paper',4,(132,346,444,540),SEC,[],'Complete filament-bulb current–voltage graph with both axes and scales.',False),
 'q4-context':('paper',4,(54,54,547,620),SEC,[],'Both experiment contexts, all eight resistance readings and the complete filament-bulb graph.',False,[(54,198,547,303),(54,553,547,582),(514,599,547,620)]),
 'q5-hurler':('paper',5,(416,109,540,314),SEC,[],'Hurler striking a sliotar.',False),
 'q5-pitch':('paper',5,(343,342,542,488),SEC,[],'Football pitch accompanying the solar-energy question.',False),
 'q5-plug':('paper',5,(423,489,541,616),SEC,[],'Three-pin plug accompanying the fuse question.',False),
 'q5-nuclear-solution':('scheme',8,(82,625,545,646),SEC,[],'Official complete nitrogen–alpha transmutation equation with isotope indices.',True),
 'q5-not-solution':('scheme',8,(82,722,545,755),SEC,[],'Official NOT-gate symbol and truth-table entries.',True),
 'q6-globe':('paper',6,(405,110,562,263),SEC,[],'GPS satellite orbits around the Earth.',False),
 'q6-derivation':('scheme',9,(54,237,545,312),SEC,[],'Complete derivation of the satellite period–radius relationship.',True),
 'q7-hand':('paper',6,(448,492,550,635),SEC,[],'Hand X-ray illustrating medical imaging.',False),
 'q7-wavelength-solution':('scheme',10,(68,277,545,327),SEC,[],'Official photon-energy equation, substitution and minimum wavelength.',True),
 'q8-dome':('paper',7,(455,101,563,314),SEC,[],'Van de Graaff generator and charged spherical dome.',False),
 'q9-guitar':('paper',7,(56,454,222,582),SEC,[],'Guitar player accompanying the string-frequency tasks.',False),
 'q9-whistle':('paper',7,(411,580,547,780),SEC,[],'Tin-whistle player accompanying the pipe-length question.',False),
 'q10-hand':('paper',8,(445,56,573,201),SEC,[],'Hand illustrating the incident solar neutrinos.',False),
 'q10-beta-solution':('scheme',13,(83,344,545,368),SEC,[],'Original SEC beta-decay equation with all isotope indices and neutrino symbol.',True,[(83,344,132,347),(162,344,545,347)]),
 'q10-radius-solution':('scheme',13,(83,572,545,618),SEC,[],'Official magnetic-force and centripetal-force calculation.',True),
 'q10-speaker':('paper',8,(444,526,541,690),SEC,[],'Moving-coil loudspeaker.',False),
 'q10-torque-solution':('scheme',14,(83,430,545,475),SEC,[],'Both accepted torque calculation routes and result.',True),
 'q11-passage':('paper',9,(54,80,573,464),SEC,[],'Complete Tesla passage, portrait, Roadster photograph and W Bernard Carlson 2013 attribution.',False),
 'q12-skier':('paper',10,(321,150,548,295),SEC,[],'Downhill skier.',False),
 'q12-lens':('paper',10,(402,487,586,633),SEC,[],'Complete incoming ray and lens section for refraction at both faces.',False,[(402,487,454,505)]),
 'q12-thermometric-question':('paper',11,(81,53,353,130),SEC,[],'Full thermometric-property and emf statements with original underlining and definitions ask.',False,[(331,109,353,130)]),
 'q12-thermocouple':('paper',11,(354,50,566,235),SEC,[],'Thermocouple thermometer.',False,[(354,222,510,235)]),
 'q12-radon':('paper',11,(388,440,542,577),SEC,[],'Radon periodic-table tile.',False),
 'q12-detector-solution':('scheme',17,(83,539,545,655),SEC,[],'Both full detector methods: Geiger–Müller tube and solid-state detector.',True)}

SELECTION_SCAN=[
 ('paper',2,'the following','All six Boyle’s-law data pairs retained.'),
 ('paper',3,'the following','All six steam-experiment measurements retained.'),
 ('paper',3,'the following','All four diffraction orders and angle pairs retained.'),
 ('paper',4,'the following','All eight temperature and resistance pairs retained.'),
 ('paper',4,'the following','Full printed bulb current–voltage graph retained.'),
 ('paper',5,'the following','All ten Q5 parts and both j options retained; no best-eight combinations.'),
 ('paper',5,'or','Both quarks and NOT-gate alternatives retained with separate topic/answer structures.'),
 ('paper',7,'both','Both named apparatus types are context; no selection.'),
 ('paper',7,'both','Both ends of an open pipe: physical description, not a choice.'),
 ('paper',7,'both','Both tin-whistle ends: physical description, not a choice.'),
 ('paper',8,'either','Both Q10 alternatives fully carded with their independent 56-mark tariffs.'),
 ('paper',8,'or','Same Q10 outer selection; no omitted branch.'),
 ('paper',9,'the following','Complete Tesla passage and all eight responses retained.'),
 ('paper',10,'any two','All four Q12 alternatives retained; no combinations.'),
 ('paper',10,'the following','Same Q12 selection.'),
 ('paper',10,'both','Both lens faces are required physical context.'),
 ('paper',10,'both','Both surface normals are required in one diagram task.')]

for task in TASKS:
 if task['key'] in {'Q2:assumptions','5g','Q7:xray-production','Q8:point-discharge','Q9:string-factors','Q12(c):thermocouple'}:
  task['cells']={'Q2:assumptions':'Both assumptions are priced at 2; the second tariff is inline.', '5g':'The final 3-mark cell shares its line with the separate unit deduction; two earlier cells are 2 each.', 'Q7:xray-production':'Diagram 4, thermionic emission 4, high voltage 3 and target impact 3; the latter tariffs follow state/imply notes.', 'Q8:point-discharge':'Three 3-mark criteria; the latter two cells follow state/imply notes.', 'Q9:string-factors':'Length 3 and linear density 3; the second tariff follows the accept-symbols note.', 'Q12(c):thermocouple':'Three 3-mark criteria; the voltage-measurement tariff follows a state/imply note.'}[task['key']]

# Read alongside the historical scheme when writing the neutrino clarifications:
# https://www.energy.gov/science/doe-explainsbeta-decay
# https://neutrinos.fnal.gov/mysteries/mass/
FIGURES['q2-data']=('paper',3,(81,101,405,191),SEC,[],'All six steam-experiment measurements with their original labels and units.',False)
FIGURES['q2-latent-question']=('paper',3,(54,54,541,393),SEC,[],'Full steam-experiment context, all six measurements, latent-heat ask and water heat-capacity constant.',False,[(54,198,541,279),(508,280,541,299),(54,310,541,369)])
for task in TASKS:
 if task['ref']=='Q2':
  if task['concept']=='latent-heat':task['qfig']='q2-latent-question'
  else:
   task['fig']='q2-data'
   task['stem']=[x for x in task['stem'] if x!=DATA2]
 if task['key']=='Q9:production':task['stem'].append(P(7,'What are stationary waves?','What are stationary waves?'))
 if task['key'] in {'Q12(a):snow-force','Q12(a):reaction'}:
  task['stem'].insert(2,P(10,'Ignoring friction, calculate her maximum','velocity when she has travelled 400 m.'))

# Explanatory guidance must appear in the student-facing reveal. The audit-only
# task notes do not survive deck generation, so retain the same explanation in
# the first marking row as well.
for task in TASKS:
 if task['notes'] and task['rows']:
  row=task['rows'][0]
  row['note']=' '.join(x for x in [row.get('note'),task['notes']] if x)
