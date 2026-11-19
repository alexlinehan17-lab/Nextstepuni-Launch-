"""Physics 2018 Higher — independently source-reviewed task ledger.

All 12 paper and 20 scheme pages rendered and read on 2026-10-31.
Every marked ask is kept, including both Q5(j) and Q10 alternatives and all
four Q12 letters. Unnumbered tasks have descriptive item labels; no invented
paper numbering. Source figures retain required data and geometry.
First occurrences of all missing glyphs were visually checked in 103 crops.
"""
from phys_review_lib import Q, SQ, S, M, G, pt, anyn, T
YEAR, LEVEL = 2018, 'hl'
REVIEWED_AT = '2026-10-31'
LETTERED = {5,6,10,11,12}
SOURCES = {
 'paper':{'path':'examiner-reports/physics/papers/2018-hl-paper.pdf','fileid':'LC021ALP000EV.pdf','sha256':'88fb4b04086dce87adf24edcb7bbf9a6c8d2334db532e9c9d798dfe0974d5eb3','pages':12},
 'scheme':{'path':'examiner-reports/physics/schemes/2018-hl.pdf','fileid':'LC021ALP000EV.pdf','sha256':'26dc1c8c662bbc3f05b20f629100f5adc9421cae965f2cad90bc8b4ac20be92a','pages':20}}
PAGE_ROLES={'paper':{1:'cover',**{p:'questions' for p in range(2,12)},12:'back-cover'},'scheme':{1:'cover',2:'note',3:'conventions',**{p:'marking' for p in range(4,20)},20:'back-cover'}}
_FONT_GLYPHS={'Cambria': {1775: 'A',
             1782: 'H',
             1784: 'J',
             1787: 'M',
             1788: 'N',
             1796: 'V',
             1801: 'a',
             1803: 'c',
             1804: 'd',
             1805: 'e',
             1807: 'g',
             1809: 'i',
             1811: 'k',
             1812: 'l',
             1813: 'm',
             1814: 'n',
             1815: 'o',
             1816: 'p',
             1818: 'r',
             1819: 's',
             1825: 'y',
             1826: 'z',
             1831: 'E',
             1843: 'Q',
             1856: 'd',
             1857: 'e',
             2011: 'γ',
             2157: 'A',
             2158: 'B',
             2159: 'C',
             2161: 'E',
             2162: 'F',
             2164: 'H',
             2165: 'I',
             2167: 'K',
             2169: 'M',
             2170: 'N',
             2172: 'P',
             2173: 'Q',
             2174: 'R',
             2176: 'T',
             2177: 'U',
             2178: 'V',
             2183: 'a',
             2185: 'c',
             2186: 'd',
             2187: 'e',
             2188: 'f',
             2189: 'g',
             2190: 'h',
             2191: 'i',
             2193: 'k',
             2194: 'l',
             2195: 'm',
             2196: 'n',
             2198: 'p',
             2200: 'r',
             2201: 's',
             2202: 't',
             2203: 'u',
             2204: 'v',
             2206: 'x',
             2207: 'y',
             2242: 'θ',
             2246: 'μ',
             2250: 'π',
             2259: 'ω',
             2261: 'ϵ',
             2777: '0',
             2778: '1',
             2779: '2',
             2780: '3',
             2781: '4',
             2782: '5',
             2783: '6',
             2784: '7',
             2785: '8',
             2786: '9',
             2868: '0',
             2869: '1',
             2879: '−',
             3127: '−',
             3397: '+',
             3398: '−',
             3400: '×',
             3404: '=',
             3495: '√',
             4593: '′',
             4666: '(',
             4667: ')'},
 'SymbolMT': {79: 'λ', 73: 'φ', 84: 'θ', 58: 'Ω', 81: 'ν'}}
GLYPHS={"paper":_FONT_GLYPHS,"scheme":_FONT_GLYPHS}
VERIFIED_LINES=[]
QUESTION_TOTALS={**{n:40 for n in range(1,5)},**{n:56 for n in range(5,10)},10:112,11:56,12:112}
PART_TOTALS={(6,'a'):21,(6,'b'):12,(6,'c'):23,**{(10,x):56 for x in 'ab'},**{(11,x):7 for x in 'abcdefgh'},**{(12,x):28 for x in 'abcd'}}
BEST_OF={5:(8,7)}
GROUP_TOTALS={};CHECKSUMS={};ROUTES={'Q5(j)':['quarks','and-gate']}
SCAN_PAGES={'paper':range(2,12)}
SELECTION_SCAN=[]
ASK_SCAN_PAGES={'paper':range(2,12)};ASK_EXEMPT=[]
SEC='State Examinations Commission'
CRIT='The scheme prints this marking criterion rather than a worked answer.'
DSL='The scheme’s // separates complete alternative methods; do not mix partial answers across methods.'
P=Q
def R(text,marks,end=None,**kw):return pt(S(text,end),marks,**kw)
def C(text,marks,end=None,**kw):return pt(S(text,end),marks,kind='criterion',note=CRIT,**kw)
def FR(page,clip,expect,marks,**kw):return G('fraction',page=page,clip=clip,expect=expect,marks=marks,**kw)
def EQ(page,clip,expect,marks,**kw):return G('equation',page=page,clip=clip,expect=expect,marks=marks,**kw)
def pieces(sel,marks,sep):return [pt(dict(sel,piece=i+1,psep=sep),m) for i,m in enumerate(marks)]
TASKS=[]
def U(ref,slug,label,q,rows,topic,sq,total,**kw):
 TASKS.append(T(ref+':'+slug,ref,'A' if int(ref.split('(')[0][1:])<5 else 'B',q,rows,topic,slug,sq,total,item=(slug,label),**kw))
FIGURES={}

STEM1=P(2,'In an experiment to verify the principle of conservation of momentum','The following data were recorded.')
FORCE1=P(2,'External forces were minimised in the experiment.')
STEM2=P(2,'A student measured the angle of incidence i and the angle of refraction r','The following data were recorded.')
STEM3=P(3,'A student used a narrow beam of monochromatic light','The following data were recorded.')
COMPARE3=P(3,'Describe the effect on the size of the angle φ','diffraction grating above was replaced with a diffraction grating of 80 lines per mm.')
STEM4=P(3,'In an experiment to verify Joule’s law','The following data were recorded.')
HEAT4=P(3,'(specific heat capacity of water = 4180 J kg⁻¹ K⁻¹)')
# Section A: independently marked tasks; all measurements retained in source crops.
U('Q1','apparatus','Apparatus',P(2,'Draw a labelled diagram of the apparatus used in the experiment.'),
 pieces(S('two bodies, means of coalescing bodies, timing apparatus'),[3,3,3],','),'phys-u2',SQ(4,'Draw a labelled diagram of the apparatus used in the experiment.'),9,stem=[STEM1],fig='q1-data')
U('Q1','external-forces','External forces',P(2,'State the two principal external forces that were minimised.','minimised.'),
 pieces(S('gravitational, frictional'),[3,3],','),'phys-u2',SQ(4,'State the two principal external forces that were minimised.','How were they minimised?'),6,stem=[STEM1,FORCE1])
U('Q1','minimising-forces','Minimising forces',P(2,'How were they minimised?'),
 [R('horizontal track',3,route='horizontal',note=DSL),R('correct reference to air track',3,route='horizontal'),pt(S('// slope track',piece=2,psep='//'),3,route='sloped'),pt(S('// gravitational force = frictional force','/ method of reducing friction',piece=2,psep='//'),3,route='sloped')],
 'phys-u2',SQ(4,'State the two principal external forces that were minimised.','How were they minimised?'),6,stem=[STEM1,FORCE1,P(2,'State the two principal external forces that were minimised.','minimised.')])
U('Q1','velocities','Velocities',P(2,'Calculate velocities u and v.'),pieces(S('u= 1.342 m s⁻¹, v = 0.692 m s⁻¹'),[2,2],','),'phys-u2',SQ(4,'Calculate velocities u and v.'),4,stem=[STEM1],fig='q1-data')
U('Q1','momentum','Conservation of momentum',P(2,'Use the data to verify the principle of conservation of momentum.'),
 [R('p=mv',2),*pieces(S('p₁=0.484 kg m s⁻¹, p₂=0.485 kg m s⁻¹'),[2,2],','),R('p₁≅p₂ statement',3)],'phys-u2',SQ(4,'Use the data to verify the principle of conservation of momentum.'),9,stem=[STEM1],fig='q1-data')
U('Q1','energy-loss','Loss of kinetic energy',P(2,'Calculate the loss of kinetic energy in the bodies during the collision.'),
 [FR(4,(84,555,147,582),'E= ½ mv²',2),R('∆E=0.325−0.168=0.157 J',2)],'phys-u2',SQ(4,'Calculate the loss of kinetic energy in the bodies during the collision.'),4,stem=[STEM1],fig='q1-data')
U('Q1','energy-form','Form of energy',P(2,'What form of energy could account for this loss of kinetic energy?'),
 [anyn(S('sound/heat'),1,2,sep='/')],'phys-u2',SQ(4,'What form of energy could account for this loss of kinetic energy?'),2,stem=[STEM1,P(2,'Calculate the loss of kinetic energy in the bodies during the collision.')])
U('Q2','refraction-measurement','Measuring refraction',P(2,'Describe, with the aid of a labelled diagram','the angle of refraction.'),
 [R('diagram of block, pins / ray box / laser (labelled)',3),C('correct method of finding refracted ray (state/imply)',3),R('draw normal in block at point of incidence',3),R('measure angle between normal and refracted ray with a protractor',3)],
 'phys-u2',SQ(5,'Describe, with the aid of a labelled diagram, how the student determined the angle of refraction.'),12,stem=[STEM2])
U('Q2','graph','Refraction graph',P(2,'Draw a suitable graph to show the relationship between the angle of incidence and','the angle of refraction.'),
 [C('12 calculations of sin i and sin r',3),C('labelled axes',3),C('6 points plotted',3),C('straight line with good fit',3)],'phys-u2',SQ(5,'Draw a suitable graph to show the relationship between the angle of incidence and','the angle of refraction.'),12,stem=[STEM2],fig='q2-data')
U('Q2','relationship','Relationship between the angles',P(2,'State this relationship and explain how your graph verifies it.'),
 [R('sini∝sinr',3),R('straight line through origin',3)],'phys-u2',SQ(5,'State this relationship and explain how your graph verifies it.'),6,stem=[STEM2,P(2,'Draw a suitable graph to show the relationship between the angle of incidence and','the angle of refraction.')],fig='q2-data')
U('Q2','index','Refractive index',P(2,'Use your graph to determine the refractive index of the material used.'),
 [FR(5,(84,544,185,572),'slope=n= (y₂−y₁)/(x₂−x₁)',3),R('n=1.50',3)],'phys-u2',SQ(5,'Use your graph to determine the refractive index of the material used.'),6,stem=[STEM2,P(2,'Draw a suitable graph to show the relationship between the angle of incidence and','the angle of refraction.')],fig='q2-data')
U('Q2','normal-incidence','Normal incidence',P(2,'What would be observed if the incident ray was perpendicular to the block?'),
 [R('ray passes straight through',4)],'phys-u2',SQ(5,'What would be observed if the incident ray was perpendicular to the block?'),4,stem=[STEM2])
U('Q3','apparatus','Diffraction apparatus',P(3,'Draw a labelled diagram of the apparatus that the student used in this experiment.'),
 [anyn(S('screen, diffraction grating, laser // spectrometer, diffraction grating, sodium lamp(3×2)',piece=1,psep='//'),3,2,sep=',',route='laser',note=DSL),anyn(S('screen, diffraction grating, laser // spectrometer, diffraction grating, sodium lamp(3×2)',piece=[2,1],psep=['//','(3×2)']),3,2,sep=',',route='spectrometer')],
 'phys-u2',SQ(6,'Draw a labelled diagram of the apparatus that the student used in this experiment.'),6,stem=[STEM3],fig='q3-data',cells='Scheme p6 prints the inline (3×2) after the two complete apparatus routes.')
U('Q3','angle','Measuring the diffraction angle',P(3,'Describe how the angle between the two first order images was obtained.'),
 [pt(S('s₁ between grating and screen // record θₗ at n=1 to left',piece=1,psep='//'),3,route='screen',note=DSL),R('s₂ between first order images',3,route='screen'),pt(S('s₁ between grating and screen // record θₗ at n=1 to left',piece=2,psep='//'),3,route='spectrometer'),pt(S('// record θr at n=1 to right',piece=2,psep='//'),3,route='spectrometer'),C('correct method of calculating φ or θ',3)],
 'phys-u2',SQ(6,'Describe how the angle between the two first order images was obtained.'),9,stem=[STEM3],fig='q3-data')
U('Q3','wavelength','Wavelength',P(3,'Calculate the wavelength of the beam of light.'),
 [R('d=2×10⁻⁶',3),R('θ=17.05°',3),R('nλ=dsinθ',3),R('λ=5.86×10⁻⁷m',3)],'phys-u2',SQ(6,'Calculate the wavelength of the beam of light.'),12,stem=[STEM3],fig='q3-data')
U('Q3','grating-angle','Effect of changing the grating',COMPARE3,[R('φ decreases',3)],'phys-u2',SQ(6,'Describe the effect on the size of the angle φ','the diffraction grating above was replaced with a diffraction grating of 80 lines per mm.'),3,stem=[STEM3],fig='q3-data')
U('Q3','accuracy','Choosing the more accurate grating',P(3,'Hence determine which grating would give a more accurate value for λ.','Justify your answer.'),
 [R('500 lines per mm grating',3),R('larger measurements give smaller percentage error',3)],'phys-u2',SQ(6,'Hence determine which grating would give a more accurate value for λ.','Justify your answer.'),6,stem=[STEM3,COMPARE3],fig='q3-data')
U('Q3','white-light','Replacing the light source',P(3,'What would the student observe if the source of monochromatic light was replaced with a source','of white light?'),
 [R('spectrum',4)],'phys-u2',SQ(6,'What would the student observe if the source of monochromatic light was replaced with a','source of white light?'),4,stem=[STEM3])
U('Q4','apparatus','Joule’s law apparatus',P(3,'Draw a diagram of the apparatus used in this experiment.'),
 [*pieces(S('power supply, means of varying voltage, coil, ammeter in series'),[3,3,3,3],','),R('thermometer and coil in water',3)],'phys-u2',SQ(7,'Draw a diagram of the apparatus used in this experiment.'),15,stem=[STEM4])
U('Q4','graph','Verifying Joule’s law',P(3,'Draw a suitable graph to verify Joule’s law.'),
 [C('6 calculations of I²and 6 calculations of ∆θ',3),C('labelled axes',3),C('6 points plotted',3),C('straight line with good fit',3),C('through origin',3)],'phys-u2',SQ(7,'Draw a suitable graph to verify Joule’s law.'),15,stem=[STEM4],fig='q4-data',notes='The paper supplies seven readings. The published scheme awards the calculation and plotting marks for six; all seven source readings are retained.',decision='Seven data values versus six calculations/points is the published scheme, not a missing source reading.')
U('Q4','resistance','Finding the coil resistance',P(3,'Calculate the slope of the graph and hence calculate the resistance of the heating coil.'),
 [FR(7,(84,526,162,554),'slope= (y₂−y₁)/(x₂−x₁)',3),R('slope=1.04',3),FR(7,(84,574,150,600),'slope= Rt/(mc)',2),R('R=2.2 Ω',2)],'phys-u2',SQ(7,'Calculate the slope of the graph and hence calculate the resistance of the heating coil.'),10,stem=[STEM4,HEAT4],fig='q4-data')

def B(key,ref,page,start,end,sp,rows,topic,total,**kw):
 sq=kw.pop('sq',SQ(sp,start,end));TASKS.append(T(key,ref,'B',P(page,start,end),rows,topic,key,sq,total,**kw))
# Q5 fixed required headings stay together; its two separately themed j routes remain alternatives.
B('5a','Q5(a)',4,'Draw a labelled diagram to show the forces acting','on a skydiver falling with a constant velocity.',8,
 [C('labelled force arrow down',2),C('labelled force arrow up',2),C('arrows of equal length',3)],'phys-1-2',7,sq=SQ(8,'Draw a labelled diagram to show the forces acting on a skydiver falling with a constant velocity.'))
B('5b','Q5(b)',4,'A horizontal metre stick is in equilibrium when a','The metre stick is supported at its centre of gravity, 50 cm. Calculate X.',8,
 [R('M=Fd',4),R('x=6.25 N',3)],'phys-1-2',7,fig='q5b-metre-stick',sq=SQ(8,'A horizontal metre stick is in equilibrium when a weight','The metre stick is supported at its centre of gravity, 50 cm. Calculate X.'))
B('5c','Q5(c)',4,'Distinguish between the three methods of heat transfer.',None,8,
 [R('conduction: no net movement of medium',3),R('convection: circulation of a fluid',2),R('radiation: electromagnetic / photons / through a vacuum',2)],'phys-2-1',7,stem=[P(4,'Heat energy can be transferred by conduction, convection and radiation.')],decision='Three required headings, not a candidate-choice pool; printed 3+2+2 retained.')
B('5d','Q5(d)',4,'Calculate the frequency observed.',None,8,
 [FR(8,(98,299,147,324),'f′= fc/(c−u)',3),FR(8,(98,320,180,345),'f′= (2300)(340)/(340−30)',2),R('f′=2523 Hz',2)],'phys-2-7',7,
 stem=[P(4,'A fire‐engine travelling at a speed of 30 m s⁻¹ emits a sound','of frequency 2.3 kHz as it approaches an observer.'),P(4,'(speed of sound in air = 340 m s⁻¹)')])
B('5e','Q5(e)',4,'The refractive index of a material is 2.4. Calculate the speed of','light in this material.',8,
 [FR(8,(98,369,134,394),'n= c/v',3),FR(8,(98,389,162,417),'2.4= (3×10⁸)/v',2),R('v=1.25×10⁸ m s⁻¹',2)],'phys-2-3',7,sq=SQ(8,'The refractive index of a material is 2.4. Calculate the speed of light in this material.'))
B('5f','Q5(f)',4,'Explain how electrons are (i) produced, (ii) accelerated in an X‐ray tube.',None,8,
 [R('produced by thermionic emission (at cathode)',4),R('accelerated through a high voltage',3)],'phys-4-1',7,sq=SQ(8,'Explain how electrons are (i) produced and (ii) accelerated in an X‐ray tube.'),decision='Required paired production/acceleration headings remain one seven-mark response.')
B('5g','Q5(g)',4,'Write an expression for the electric field intensity E at a distance d','from a charge Q.',8,
 [FR(8,(98,485,132,511),'Q/(4πϵd²)',7,note='The scheme allows 4 marks for Coulomb’s force formula or E = F/Q.')],'phys-3-1',7,fig='q5g-charge',sq=SQ(8,'Write an expression for the electric field intensity E at a distance d from a charge Q.'))
B('5h','Q5(h)',4,'What are the charge carriers in (i) metals, (ii) gases, (iii) semiconductors?',None,8,
 [R('metals: electrons',3),R('gases: ions/electrons',2),R('semiconductors: electrons/holes',2)],'phys-3-3',7,decision='Three required material headings share the 3+2+2 tariff; no choice expansion.')
B('5i','Q5(i)',4,'Calculate the effective resistance of a 5 Ω resistor and a 7 Ω resistor when they are','connected in parallel.',8,
 [FR(8,(98,594,166,621),'1/(RT) = 1/R₁ + 1/R₂',3),FR(8,(98,617,156,644),'1/(RT) = ⅕ + 1/7',2),R('RT=2.9 Ω',2)],'phys-3-3',7,
 sq=SQ(8,'Calculate the effective resistance of a 5 Ω resistor and a 7 Ω resistor when they are connected in','parallel.'))
B('5j-quarks','Q5(j)',4,'State (i) a physical quantity that is the same for a quark and its anti‐quark and (ii) a physical','quantity that is different for a quark and its anti‐quark.',8,
 [R('same: mass/magnitude of charge',4),R('different: (sign of) charge',3)],'phys-4-5',7,route='quarks')
B('5j-and-gate','Q5(j)',4,'Draw the truth table for an AND gate.',None,8,
 [R('0+0→0',3),R('0+1→0',2),R('1+1→1',2)],'phys-3-3',7,route='and-gate',notes='The published scheme lists these three combinations at 3+2+2. The symmetric 1+0 input is not a separate marked row in the scheme.',decision='Three published truth-table rows; no invented fourth marking point.')

DISCUS6=P(5,'During the discus event, Ashton swings a discus of mass','when Ashton releases it.')
JUMP6=P(5,'During the long','seconds after he takes off.')
VAULT6=P(5,'During the pole vault event, Ashton has a horizontal','maximum height he has a horizontal speed of 1.1 m s⁻¹.')
GRAV6=P(5,'(acceleration due to gravity = 9.8 m s⁻²)')
B('6ai','Q6(a)(i)',5,'Derive an expression to show the relationship','an object moving in uniform circular motion.',9,
 [FR(9,(73,137,120,163),'θ= s/r',6),FR(9,(83,160,120,186),'θ/t = s/(rt)',3),FR(9,(73,181,122,207),'ω= v/r',3)],'phys-1-6',12,stem=[DISCUS6],sq=SQ(9,'Derive an expression to show the relationship between the radius, velocity and angular','velocity of an object moving in uniform circular motion.'))
B('6aii','Q6(a)(ii)',5,'Calculate the angular velocity of the discus immediately prior to its release.',None,9,
 [FR(9,(73,221,206,247),'ω= 20.4/1.2 =17 rad s⁻¹',3)],'phys-1-6',3,stem=[DISCUS6])
U('Q6(a)(iii)','force','Centripetal force',P(5,'Calculate the centripetal force acting on the discus just before Ashton releases it.'),
 [R('F=mrω²=(2)(1.2)(17)²=693.6 N',3)],'phys-1-6',SQ(9,'Calculate the centripetal force acting on the discus just before Ashton releases it.'),3,stem=[DISCUS6])
U('Q6(a)(iii)','direction','Force direction',P(5,'In what direction does this force apply?'),
 [R('towards the centre',3)],'phys-1-6',SQ(9,'In what direction does this force apply?'),3,stem=[DISCUS6,P(5,'Calculate the centripetal force acting on the discus just before Ashton releases it.')])
B('6bi','Q6(b)(i)',5,'his velocity in the horizontal direction,',None,9,
 [R('vH=vcosθ',3),R('vH=10.9cos43° =7.97 m s⁻¹',3)],'phys-1-1',6,stem=[JUMP6,P(5,'Calculate',after='seconds after he takes off.')],sq=SQ(9,'his velocity in the horizontal direction'),fig='q6b-jump')
B('6bii','Q6(b)(ii)',5,'the length of the jump.',None,9,
 [R('s=vt',3),R('s=(7.97)(1.03)=8.21 m',3)],'phys-1-1',6,stem=[JUMP6,P(5,'Calculate',after='seconds after he takes off.')],fig='q6b-jump')
B('6ci','Q6(c)(i)',5,'State the principle of conservation of energy.',None,9,[R('energy cannot be created or destroyed',3,kind='point')],'phys-1-4',3,stem=[VAULT6])
B('6cii','Q6(c)(ii)',5,'What is meant by the centre of gravity of a body?',None,9,[R('the point of a body where its weight appears to act',3)],'phys-1-2',3,stem=[VAULT6])
B('6ciii','Q6(c)(iii)',5,'Ashton’s centre of gravity when he is standing is 98 cm above the ground. During the','gravity?',9,
 [FR(9,(73,615,159,641),'mgh / ½ mv²',3),R('gain in potential energy = loss in kinetic energy',3),FR(9,(73,655,208,683),'h= (9.2²−1.1²)/(2(9.8)) =4.26 m',3),R('height above ground = 4.26+0.98=5.24 m',3)],'phys-1-4',12,stem=[VAULT6,GRAV6],sq=SQ(9,'Ashton’s centre of gravity when he is standing is 98 cm above the ground. During the vault,','what is the maximum height above the ground to which he can raise his centre of gravity?'))
B('6civ','Q6(c)(iv)',5,'Draw a diagram to show any forces acting on Ashton when he is at his highest point, as','shown in the photograph.',9,
 [C('one labelled arrow downwards',5)],'phys-1-2',5,stem=[VAULT6],fig='q6c-vault',sq=SQ(9,'Draw a diagram to show any forces acting on Ashton when he is at his highest point, as shown','in the photograph.'))

STRING7=P(6,'A stretched string of a violin has a length of 328 mm and a','at its fundamental frequency.')
DIST7=P(6,'A source emits sound in all directions.','Describe the effect of doubling the distance from the source to an observer on')
U('Q7','resonance','Resonance',P(6,'What is resonance?'),[R('transfer of energy',3),R('between two bodies of the same natural frequency',3)],'phys-2-5',SQ(10,'What is resonance?'),6,stem=[P(6,'Resonance is a phenomenon that is associated with musical instruments.','instruments.')])
U('Q7','resonance-experiment','Demonstrating resonance',P(6,'Describe an experiment to demonstrate resonance.'),
 [R('e.g. two tuning forks of the same frequency on a wooden board',3),R('set one tuning fork vibrating',3),R('second tuning fork starts vibrating',3)],'phys-2-5',SQ(10,'Describe an experiment to demonstrate resonance.'),9)
B('7i','Q7(i)',6,'the tension in the string,',None,10,
 [FR(10,(84,240,244,268),'μ= (0.126×10⁻³)/0.328 =3.84×10⁻⁴',3),FR(10,(84,270,138,296),'f= 1/(2l) √(T/μ)',3),R('T=72 N',3)],'phys-2-5',9,stem=[STRING7,P(6,'Calculate')],sq=SQ(10,'the tension in the string'))
B('7ii','Q7(ii)',6,'the speed of sound in the string.',None,10,[R('λ=2(0.328)=0.656',3),R('v=fλ',3),R('v=433 m s⁻¹',3)],'phys-2-5',9,stem=[STRING7,P(6,'Calculate')])
U('Q7','closed-pipe','Stationary wave in a closed pipe',P(6,'Draw a labelled diagram to represent the fundamental frequency of a stationary wave in a pipe','that is closed at one end.'),
 [R('node at closed end',3,note_sel=S('(–1 if neither node nor antinode labelled)')),R('antinode at open end with no other nodes',3)],'phys-2-5',SQ(10,'Draw a labelled diagram to represent the fundamental frequency of a stationary wave in a pipe','that is closed at one end.'),6)
U('Q7','intensity','Sound intensity',P(6,'Define sound intensity.'),
 [FR(10,(84,482,126,508),'I= P/A',3,route='formula',note=DSL),C('notation',3,route='formula'),pt(S('// power',piece=2,psep='//'),3,route='words'),pt(S('// per unit area',piece=2,psep='//'),3,route='words')],'phys-2-5',SQ(10,'Define sound intensity.'),6)
B('7iii','Q7(iii)',6,'the sound intensity measured,',None,10,[FR(10,(84,572,126,598),'I∝ 1/d²',3),R('4 times',2),R('smaller',2)],'phys-2-5',7,stem=[DIST7],sq=SQ(10,'the sound intensity measured'))
B('7iv','Q7(iv)',6,'the sound intensity level measured.',None,10,[R('idea of 3 decibel change',2),R('6 decibels lower',2)],'phys-2-5',4,stem=[DIST7])

WATER8=P(6,'In a nuclear reactor core, 5000 kg of water is heated so that its','temperature increases by 70 K and it is converted into steam.')
THERM8=[P(6,'(specific heat capacity of water = 4180 J kg⁻¹ K⁻¹)'),P(6,'(specific latent heat of vaporisation of water = 2.23 × 10⁶ J kg⁻¹)')]
FISSION8=P(6,'In a fission reaction a neutron is absorbed by a uranium–235 nucleus.','nuclei are released as well as some neutrons.')
MASSES8=P(6,'(mass of barium–139 nucleus = 138.90884 u, mass of krypton–94 nucleus = 93.93436 u,','mass of uranium–235 nucleus = 235.04393 u)')
FUSION8=P(6,'Nuclear fusion reactors could supply more energy than fission reactors.','fission reactors.')
U('Q8','definitions','Fission and heat capacity',P(6,'Explain the terms nuclear fission and specific heat capacity.'),
 [R('splitting of a (large) nucleus into two (similar sized) nuclei',3,note_sel=S('(–1 for atom instead of nucleus)')),R('with the emission of energy/neutrons',3),R('the energy required to change the temperature',3),R('of 1 kg by 1 K',3)],'phys-4-4',SQ(11,'Explain the terms nuclear fission and specific heat capacity.'),12,decision='Both required definitions form the printed 12-mark task; retain both terms and add the heat topic to its Atlas question.')
U('Q8','moderator-effect','Moderator effect',P(6,'What effect does a moderator have on the rate of fission?'),[R('increases the rate of fission',3)],'phys-4-4',SQ(11,'What effect does a moderator have on the rate of fission?'),3,stem=[P(6,'Water can act as both a moderator and a coolant in a nuclear fission reactor.')])
U('Q8','moderator-mechanism','How moderation works',P(6,'How does a moderator have this effect?'),[R('slows down neutrons',3)],'phys-4-4',SQ(11,'How does a moderator have this effect?'),3,stem=[P(6,'Water can act as both a moderator and a coolant in a nuclear fission reactor.'),P(6,'What effect does a moderator have on the rate of fission?')])
U('Q8','heat','Energy absorbed by water',P(6,'Calculate the energy absorbed by the water.'),[R('E=ml+mc∆θ',6,units=[3,3]),R('E=(5000)(2.23×10⁶)+(5000)(4180)(70)',3),R('E=1.26 × 10¹⁰ J',3)],'phys-2-1',SQ(11,'Calculate the energy absorbed by the water.'),12,stem=[WATER8,*THERM8])
U('Q8','nuclear-equation','Fission equation',P(6,'Write a nuclear equation for this reaction.'),
 [EQ(11,(84,412,265,433),'²³⁵₉₂U + ¹₀n → ¹³⁹₅₆Ba + ⁹⁴₃₆Kr + 3¹₀n',10,units=[1]*10)],'phys-4-4',SQ(11,'Write a nuclear equation for this reaction.'),10,stem=[FISSION8],fig='q8-fission-solution',decision='Scheme prints 10×1 for one nuclear equation; preserve ten one-mark claims without inventing a finer component allocation.')
U('Q8','fission-energy','Energy released in fission',P(6,'Calculate the energy released, in MeV, in this reaction.'),
 [R('loss in mass =3.0×10⁻²⁸ kg',3),R('E=mc²',3),R('E=2.74×10⁻¹¹ J',3),R('E=171 MeV',2,note_sel=S('(unit not required)'))],'phys-4-4',SQ(11,'Calculate the energy released, in MeV, in this reaction.'),11,stem=[FISSION8,MASSES8])
U('Q8','fusion-limitation','Practical limit of fusion',P(6,'Explain why fusion','reactors are not yet a practical source of energy on Earth.'),[R('too much energy is required (to overcome force of repulsion between nuclei)',3)],'phys-4-4',SQ(11,'Explain why fusion','reactors are not yet a practical source of energy on Earth.'),3,stem=[FUSION8])
U('Q8','fusion-advantage','Fusion advantage',P(6,'Give one other advantage that a fusion','reactor would have over a fission reactor.'),
 [anyn(S('raw material readily available / less radioactive waste'),1,2,sep=' / ')],'phys-4-4',SQ(11,'Give one other advantage that a fusion reactor would have over a fission reactor.'),2,stem=[FUSION8,P(6,'Explain why fusion','reactors are not yet a practical source of energy on Earth.')])

COLOUR9=P(7,'Maxwell created a colour triangle to illustrate the relationship','between primary and secondary colours of light.')
MAGNET9=P(7,'Maxwell later published equations that describe how electric charges and currents create electric','magnetic field.')
FARADAY9=P(7,'One of Maxwell’s equations is equivalent to Faraday’s law of','electromagnetic induction.')
COIL9=P(7,'A square coil of 40 turns with a side of length 20 cm is perpendicular to','a magnetic field of flux density 50 mT.')
B('9i','Q9(i)',7,'Using his triangle or otherwise (i) list the primary colours of light,',None,12,
 pieces(S('red, green, blue'),[1,1,1],','),'phys-2-4',3,stem=[COLOUR9],sq=SQ(12,'Using his triangle or otherwise (i) list the primary colours of light,','of complementary colours of light.'))
B('9ii','Q9(ii)',7,'name a pair of complementary colours of light.',None,12,[C('any primary and secondary colour',3),C('correct combination',3)],'phys-2-4',6,stem=[COLOUR9],sq=SQ(12,'Using his triangle or otherwise (i) list the primary colours of light,','of complementary colours of light.',paired='The scheme reprints both colour asks together; this second roman is independently priced 3+3 for the complementary pair.'))
U('Q9','magnetic-field','Magnetic field',P(7,'What is a magnetic field?'),[R('region where magnetic forces are felt',3)],'phys-3-4',SQ(12,'What is a magnetic field?'),3,stem=[MAGNET9])
TASKS.append(T('9iii','Q9(iii)','B',P(7,'Draw labelled diagrams to show the magnetic field about (iii) a long straight current‐carrying wire,'),
 [C('circle(s) with wire at centre',3),C('arrow on circle(s) indicating direction',3)],'phys-3-4','wire-magnetic-field',SQ(12,'Draw labelled diagrams to show the magnetic field about (iii) a long straight current‐carrying','wire, (iv) a current‐carrying solenoid.'),6,stem=[MAGNET9]))
TASKS.append(T('9iv','Q9(iv)','B',[P(7,'Draw labelled diagrams to show the magnetic field about (iii) a long straight current‐carrying wire,',piece=1,psep=' (iii)'),P(7,'a current‐carrying solenoid.')],
 [C('correct shape of field lines with arrows',3)],'phys-3-4','solenoid-magnetic-field',SQ(12,'Draw labelled diagrams to show the magnetic field about (iii) a long straight current‐carrying','wire, (iv) a current‐carrying solenoid.'),3,stem=[MAGNET9]))
U('Q9','faraday-law','Faraday’s law',P(7,'State Faraday’s law of electromagnetic induction.'),
 [R('emf induced is proportional to',3,route='words',note=DSL),R('the rate of change of magnetic flux',3,route='words'),FR(12,(326,392,375,418),'E=− ∆∅/(∆t)',3,route='formula'),pt(S('// notation',piece=2,psep='//'),3,kind='criterion',route='formula')],
 'phys-3-4',SQ(12,'State Faraday’s law of electromagnetic induction.'),6,stem=[FARADAY9])
U('Q9','faraday-experiment','Demonstrating Faraday’s law',P(7,'Describe an experiment to demonstrate this law.'),
 [R('coil, galvanometer and magnet in correct arrangement',3),R('move magnet relative to coil and note current',3),R('move magnet more quickly and note larger current',3)],'phys-3-4',SQ(12,'Describe an experiment to demonstrate this law.'),9,stem=[FARADAY9])
U('Q9','induced-emf','Induced emf in the coil',P(7,'What is the average emf induced in the coil when it is rotated through 90°','sides of the square, as shown.)'),
 [R('∅=BA',3),R('∅=(50×10⁻³)(0.2)²=2×10⁻³',3),FR(12,(84,584,136,609),'E=− ∆∅/(∆t)',3),FR(12,(84,607,224,635),'E=(40) (2×10⁻³)/0.25 =0.32 V',2)],'phys-3-4',SQ(12,'What is the average emf induced in the coil when it is rotated through 90° in ¼ of','a second?'),11,stem=[COIL9],fig='q9-coil')
U('Q9','eye','Detecting light',P(7,'The eye is the sense organ that detects light. Where in the eye is light detected?'),[R('retina',3)],'phys-2-3',SQ(12,'The eye is the sense organ that detects light. Where in the eye is light detected?'),3)
U('Q9','invisible-spectrum','Invisible electromagnetic waves',P(7,'List two invisible parts of the electromagnetic spectrum that have a shorter wavelength than','visible light.'),
 [anyn(S('ultraviolet, X‐rays, gamma rays'),2,3,sep=',')],'phys-2-4',SQ(12,'List two invisible parts of the electromagnetic spectrum that have a shorter wavelength than','visible light.'),6,decision='Any two from all three accepted spectral regions; one card with two claim slots.')

PAULI10=P(8,'Momentum, energy and charge are conserved in all nuclear reactions.','I have done a terrible thing. I have postulated a particle that cannot be detected.')
ANNIHILATION10=P(8,'The conservation laws also apply to pair annihilation.','a positron at rest.')
INDUCTION10=P(8,'An induction coil is used to increase the magnitude of d.c. voltage.')
AC10=P(8,'An induction coil is not used to increase a.c. voltage.')
DEVICE10=P(8,'Name the device used to increase a.c. voltage.')
U('Q10(a)','pauli','Pauli’s predicted particle',P(8,'Name the particle which Pauli predicted and explain how it solved the problem.'),[R('neutrino',2),R('had the missing energy and momentum',3)],'phys-4-5',SQ(13,'Name the particle which Pauli predicted and explain how it solved the problem.'),5,stem=[PAULI10])
U('Q10(a)','beta-equation','Beta-decay equation',P(8,'Write a nuclear equation for beta‐decay.'),
 [EQ(13,(77,267,182,287),'¹₀n → ¹₁H + ⁰₋₁e + ν',10,units=[1]*10)],'phys-4-4',SQ(13,'Write a nuclear equation for beta‐decay.'),10,stem=[PAULI10],fig='q10a-beta-solution',decision='The equation retains the scheme’s 10×1 allocation and printed H and neutrino notation.')
U('Q10(a)','detection','Detecting the particle',P(8,'Why did Pauli think that the particle could not be detected?'),[R('no charge',3),R('very small mass',3)],'phys-4-5',SQ(13,'Why did Pauli think that the particle could not be detected?'),6,stem=[PAULI10])
U('Q10(a)','two-photons','Two gamma-ray photons',P(8,'Why are two gamma‐ray photons produced?'),[R('to conserve momentum',3)],'phys-4-5',SQ(13,'Why are two gamma‐ray photons produced?'),3,stem=[ANNIHILATION10],fig='q10a-annihilation')
U('Q10(a)','charge','Conservation of charge',P(8,'Explain how charge is conserved in the annihilation.'),[R('since particle and antiparticle have equal and opposite charges, charge before = 0',3),R('photons have no charge',3)],'phys-4-5',SQ(13,'Explain how charge is conserved in the annihilation.'),6,stem=[ANNIHILATION10],fig='q10a-annihilation')
U('Q10(a)','frequency','Frequency of each photon',P(8,'Calculate the maximum frequency of each emitted photon.'),[R('E=mc²',2),R('E=hf',3),R('hf=mc²',3),C('substitution',3),R('f= 1.24×10²⁰ Hz',3)],'phys-4-5',SQ(13,'Calculate the maximum frequency of each emitted photon.'),14,stem=[ANNIHILATION10],fig='q10a-annihilation')
U('Q10(a)','leptons','Other negative leptons',P(8,'Electrons are negatively charged leptons. List the two other negatively charged leptons.'),pieces(S('muon, tau'),[3,3],','),'phys-4-5',SQ(13,'Electrons are negatively charged leptons. List the two other negatively charged leptons.'),6)
U('Q10(a)','forces','Forces on leptons',P(8,'List the three forces that these leptons can experience, in decreasing order of strength.','strength.'),
 [*pieces(S('electromagnetic, weak, gravitational'),[1,1,1],','),C('in correct order',3)],'phys-4-5',SQ(13,'List the three forces that these leptons experience, in decreasing order of strength.'),6,stem=[P(8,'Electrons are negatively charged leptons. List the two other negatively charged leptons.')])
U('Q10(b)','current-graphs','Alternating and direct current',P(8,'Sketch current‐time graphs to compare alternating current and direct current.'),[C('axes labelled for at least one graph',3),C('correct shape for a.c.',3),C('correct shape for d.c.',3)],'phys-3-3',SQ(14,'Sketch current‐time graphs to compare alternating current and direct current.'),9)
U('Q10(b)','rectifier','Half-wave rectifier circuit',P(8,'Draw a circuit diagram of a half‐wave rectifier circuit.'),[R('diode',3),C('correct arrangement including input and output voltages',3)],'phys-3-3',SQ(14,'Draw a circuit diagram of a','half‐wave rectifier circuit.'),6,stem=[P(8,'A rectifier circuit converts alternating current to direct current.')])
U('Q10(b)','rectified-output','Rectifier output',P(8,'Sketch a graph to illustrate the output current from a half‐wave rectifier.'),[C('correct shape',3)],'phys-3-3',SQ(14,'Sketch a graph to illustrate the output current from a half‐wave rectifier.'),3,stem=[P(8,'A rectifier circuit converts alternating current to direct current.')])
U('Q10(b)','induction-coil','Induction coil diagram',P(8,'Draw a labelled diagram of an induction coil.'),[R('coil and d.c. power supply in primary circuit',3),R('coil with more turns in secondary circuit',3),R('labelled make and break mechanism and iron core',3)],'phys-3-4',SQ(14,'Draw a labelled diagram of an induction coil.'),9,stem=[INDUCTION10])
U('Q10(b)','induction-process','Increasing direct voltage',P(8,'Describe how the induction coil can be used to increase d.c. voltage.'),[R('primary coil switches off',3),R('changing magnetic field cutting the secondary coil',3),R('emf induced in secondary coil',3)],'phys-3-4',SQ(14,'Describe how the induction coil can be used to increase d.c. voltage.'),9,stem=[INDUCTION10])
U('Q10(b)','transformer-name','Increasing alternating voltage',DEVICE10,[R('transformer',3)],'phys-3-4',SQ(14,'Name the device used to increase a.c. voltage.'),3,stem=[AC10])
U('Q10(b)','transformer-diagram','Alternating-voltage device diagram',P(8,'Draw a labelled diagram of this device.'),[R('a.c. input and primary coil',3),R('secondary coil and output',3),R('both coils on common iron core',3)],'phys-3-4',SQ(14,'Draw a labelled diagram of this device.'),9,stem=[AC10,DEVICE10])
U('Q10(b)','transformer-process','How the device increases voltage',P(8,'Describe how this device can be used to increase a.c. voltage.'),[R('current in primary coil always changing',2),R('changing magnetic field from primary coil cutting the secondary coil',2),R('emf induced in secondary coil',2),R('induced emf is larger due to greater number of turns in secondary coil',2)],'phys-3-4',SQ(14,'Describe how this device can be used to increase a.c. voltage.'),8,stem=[AC10,DEVICE10])

PASSAGE11=P(9,'The Irish Low Frequency Array, or I‐LOFAR, is part of a','Adapted from rte.ie and nasa.gov')
EARTH11=P(9,'(radius of the Earth = 6400 km)')
B('11a','Q11(a)',9,'Calculate the minimum frequency of the radio waves detected by I‐LOFAR.',None,15,[R('λ=30 m',2),R('v=fλ',2),R('f=1×10⁷ Hz',3)],'phys-2-4',7,stem=[PASSAGE11])
B('11b','Q11(b)',9,'Draw a diagram of the magnetic field around the Earth.',None,15,[C('correct shape of field lines around the Earth',4),C('correct direction of field lines',3)],'phys-3-4',7,stem=[PASSAGE11])
B('11c','Q11(c)',9,'Explain how information is transmitted using optical fibres.',None,15,[R('angle of incidence (always) greater than critical angle',4),R('total internal reflection',3)],'phys-2-3',7,stem=[PASSAGE11])
B('11d','Q11(d)',9,'Calculate the position of the image of a person standing 75 cm from the Leviathan mirror.',None,15,[FR(15,(84,257,136,283),'1/u + 1/v = 1/f',3),R('79 cm',2),R('behind the mirror',2)],'phys-2-3',7,stem=[PASSAGE11])
B('11e','Q11(e)',9,'Where, with respect to the concave mirror, will an image of the moon be formed?','Justify your answer.',15,[R('at its focal point',4),R('incoming rays are parallel',3)],'phys-2-3',7,stem=[PASSAGE11])
B('11f','Q11(f)',9,'A concave mirror can also be used as a microscope to magnify images. Draw a ray diagram to','show the formation of an upright, magnified image in a concave mirror.',15,[R('object inside focal point of concave mirror',3),C('two correct reflected rays',2),C('correct image at apparent intersection of rays',2)],'phys-2-3',7,stem=[PASSAGE11],sq=SQ(15,'A concave mirror can also be used as a microscope to magnify images. Draw a ray diagram','to show the formation of an upright, magnified image in a concave mirror.'))
B('11g','Q11(g)',9,'Calculate the velocity of the Hubble telescope as it orbits the Earth.',None,15,[FR(15,(84,484,129,510),'v= 2πr/T',4),R('v=7650 m s⁻¹',3)],'phys-1-6',7,stem=[PASSAGE11,EARTH11])
B('11h','Q11(h)',9,'Name one optical phenomenon which reduced the effectiveness of the Leviathan and which','Hubble telescope eliminate this problem?',15,[R('refraction',4),R('Hubble is above the atmosphere',3)],'phys-2-3',7,stem=[PASSAGE11],sq=SQ(15,'Name one optical phenomenon which reduced the effectiveness of the Leviathan and','Hubble telescope eliminate this problem?'))

PENDULUM12=P(10,'A simple pendulum can execute simple harmonic motion.')
SPRING12=P(10,'A stretched spring can also execute simple harmonic motion.','It has a period of oscillation of 0.85 seconds.')
GRAV12=P(10,'(acceleration due to gravity = 9.8 m s⁻²)')
RADON12=P(10,'The radioactivity of an isotope of radon was measured each day for a week and the following','data were recorded.')
CURVE12=P(10,'On graph paper, draw a decay curve (a graph of activity against time).')
CAP12=P(11,'A capacitor is an important component of a','of 4.0 kV is applied across it.')
SOLAR12=P(11,'A typical solar panel consists of a sandwich made of a p‐n','flows.')
U('Q12(a)','shm','Simple harmonic motion',P(10,'Explain the underlined term.'),
 [R('acceleration is proportional to',3,route='words',note=DSL),R('displacement',3,route='words'),pt(S('// correct equation',piece=2,psep='//'),3,kind='criterion',route='equation'),pt(S('// notation',piece=2,psep='//'),3,kind='criterion',route='equation')],
 'phys-1-3',SQ(16,'Explain the underlined term.'),6,stem=[PENDULUM12],qfig='q12a-underlined')
U('Q12(a)','small-angle','Pendulum condition',P(10,'When does a simple pendulum execute simple harmonic motion?'),[R('oscillating at a small angle',3)],'phys-1-3',SQ(16,'When does a simple pendulum execute simple harmonic motion?'),3,stem=[PENDULUM12])
U('Q12(a)','period-length','Period and length',P(10,'What is the relationship between the period and the length of','a simple pendulum?'),[R('period squared proportional to length / correct equation',3)],'phys-1-3',SQ(16,'What is the relationship between the period of a simple pendulum and its length?'),3,stem=[PENDULUM12])
B('12ai','Q12(a)(i)',10,'the spring constant,',None,16,[FR(16,(84,324,133,350),'T= 2π/ω',2),R('ω=7.39',2),FR(16,(84,364,133,390),'ω²= k/m',2),R('k=3.28 N m⁻¹',2)],'phys-1-3',8,stem=[SPRING12,P(10,'Calculate')],sq=SQ(16,'the spring constant'))
B('12aii','Q12(a)(ii)',10,'the length of the spring when the mass is at rest.',None,16,[R('F=−ks',3),R('s=0.18',3),R('l=0.68 m',2)],'phys-1-3',8,stem=[SPRING12,GRAV12,P(10,'Calculate')])
U('Q12(b)','definition','Radioactivity',P(10,'What is meant by radioactivity?'),[R('(spontaneous) disintegration of a nucleus',3),R('with the emission of radiation',3)],'phys-4-4',SQ(17,'What is meant by radioactivity?'),6,stem=[RADON12])
U('Q12(b)','curve','Decay curve',CURVE12,[C('8 points plotted correctly',3),C('curve with good fit',3)],'phys-4-4',SQ(17,'On graph paper, draw a decay curve (a graph of activity against time).'),6,stem=[RADON12],fig='q12b-data')
U('Q12(b)','half-life','Half-life',P(10,'Use the decay curve to determine the half‐life of the isotope.'),[FR(17,(84,257,192,282),'time measured for A/2',2),FR(17,(84,280,166,306),'T½ =3.3 days',2)],'phys-4-4',SQ(17,'Use the decay curve to determine the half‐life of the isotope.'),4,stem=[RADON12,CURVE12],fig='q12b-data')
U('Q12(b)','nuclei','Initial number of nuclei',P(10,'Calculate the number of nuclei in the sample at the beginning of the investigation.'),[FR(17,(83,320,124,354),'λ= ln2/(T½)',3),R('λ=2.4 ×10⁻⁶',3),R('A=λN',3),R('N=2.5 ×10¹⁴',3)],'phys-4-4',SQ(17,'Calculate the number of nuclei in the sample at the beginning of the investigation.'),12,stem=[RADON12],fig='q12b-data')
U('Q12(c)','capacitance','Capacitance and its unit',P(11,'Define capacitance and state its unit.'),[FR(18,(84,71,304,97),'ratio of charge to voltage / Q/V with notation',3),R('farad',3)],'phys-3-2',SQ(18,'Define capacitance and state its unit.'),6)
U('Q12(c)','energy','Energy stored in a capacitor',P(11,'Calculate the energy stored in the capacitor.'),[R('C=2.75 ×10⁻⁵',3),FR(18,(84,219,143,245),'E= ½ CV²',3),R('E=220 J',3)],'phys-3-2',SQ(18,'Calculate the energy stored in the capacitor.'),9,stem=[CAP12],fig='q12c-defibrillator')
U('Q12(c)','net-charge','Net capacitor charge',P(11,'What is the net charge of the capacitor when it stores this energy?'),[R('0 C',3,note_sel=S('(unit not needed)'))],'phys-3-2',SQ(18,'What is the net charge of the capacitor when it stores this energy?'),3,stem=[CAP12],fig='q12c-defibrillator')
U('Q12(c)','discharge','Discharge current',P(11,'The capacitor discharges in a time of 15 ms. Calculate the average current flowing as the','capacitor discharges.'),[FR(18,(84,332,118,358),'I= Q/t',3),R('I=7.3 A',3)],'phys-3-3',SQ(18,'The capacitor discharges in a time of 15 ms. Calculate the average current flowing as the','capacitor discharges.'),6,stem=[CAP12],fig='q12c-defibrillator')
U('Q12(c)','electric-field','Field between capacitor plates',P(11,'Draw a diagram of the electric field between the charged plates of a parallel plate','capacitor.'),[R('plates with charges indicated',2),C('field lines in correct direction',2)],'phys-3-1',SQ(18,'Draw a diagram of the electric field between the charged plates of a parallel plate','capacitor.'),4)
U('Q12(d)','junction','p–n junction',P(11,'What is a p‐n junction?'),[R('where a p–type semiconductor and an n‐type semiconductor meet',3)],'phys-3-3',SQ(19,'What is a p‐n junction?'),3,stem=[SOLAR12])
U('Q12(d)','einstein','Einstein’s explanation',P(11,'In 1921, Albert Einstein was awarded the Nobel Prize in Physics for his explanation of the','photoelectric effect. Outline his explanation.'),[FR(19,(84,195,173,221),'hf=φ+ ½ mv²',3),R('light travels in photons',3),R('each photon gives all of its energy to one electron',3),R('if energy is greater than work function, electron is emitted',3)],'phys-4-1',SQ(19,'In 1921, Albert Einstein was awarded the Nobel Prize in Physics for his explanation of the','photoelectric effect. Outline his explanation.'),12,stem=[SOLAR12])
U('Q12(d)','kinetic-energy','Photoelectron kinetic energy',P(11,'The work function of iron is 4.7 eV. Calculate the maximum kinetic energy of an emitted','electron when ultraviolet radiation of wavelength 200 nm is incident on iron.'),[R('c=fλ',3),R('f= 1.5 ×10¹⁵',3),FR(19,(84,370,173,396),'hf=φ+ ½ mv²',3),FR(19,(84,393,214,419),'½ mv²= 2.4 ×10⁻¹⁹ J',4)],'phys-4-1',SQ(19,'The work function of iron is 4.7 eV.','of wavelength 200 nm is incident on iron.'),13)

SELECTION_SCAN=[
 ('paper',2,'the following','Q1 complete recorded measurements, retained.'),
 ('paper',2,'the following','Q2 complete incidence/refraction table, retained.'),
 ('paper',3,'the following','Q3 recorded angle and line density, retained.'),
 ('paper',3,'the following','Q4 all seven readings, retained.'),
 ('paper',4,'the following','Q5 best eight of ten parts; every part retained, both j routes.'),
 ('paper',4,'or','Q5(j) particle physics or logic gate: distinct topics and criteria, both retained.'),
 ('paper',6,'both','Water is moderator and coolant, a description not candidate selection.'),
 ('paper',7,'or','Using his triangle or otherwise: open method choice, one task per printed roman ask.'),
 ('paper',8,'either','Q10 choose a or b; both whole branches and every marked task retained.'),
 ('paper',8,'or','The same Q10 outer choice; no combinations.'),
 ('paper',8,'the following','Annihilation equation, retained as a source crop.'),
 ('paper',9,'the following','Q11 source passage retained in full with each card.'),
 ('paper',9,'or','I-LOFAR is an abbreviation, not a candidate choice.'),
 ('paper',10,'any two','Q12 choose two of four letters; all four retained, no pairs.'),
 ('paper',10,'the following','The same Q12 outer choice.'),
 ('paper',10,'the following','Q12(b) complete activity table, retained.'),
]
FIGURES={
 'q1-data':('paper',2,(80,245,462,326),SEC,[],'Both masses and the distances travelled in 0.12 seconds, before and after the collision.',False),
 'q2-data':('paper',2,(148,597,439,652),SEC,[],'Six measured incidence and refraction angle pairs, in degrees.',False),
 'q3-data':('paper',3,(80,94,462,138),SEC,[],'Angle between first-order images 34.1 degrees; 500 grating lines per millimetre.',False),
 'q4-data':('paper',3,(128,480,461,536),SEC,[],'All seven current and final-temperature readings for the Joule’s law experiment.',False),
 'q5b-metre-stick':('paper',4,(96,311,530,384),SEC,[],'Metre stick supported at 50 cm with 8 N at 10 cm, 12 N at 60 cm, and X at 82 cm.',False),
 'q5g-charge':('paper',4,(445,550,526,626),SEC,[],'Charge Q and a point at distance d.',False),
 'q6b-jump':('paper',5,(191,314,540,414),SEC,[],'Long-jump photograph and the 43-degree launch angle.',False),
 'q6c-vault':('paper',5,(370,521,541,637),SEC,[],'Pole vaulter at the highest point above the bar.',False),
 'q8-fission-solution':('scheme',11,(83,412,266,434),SEC,[],'Official uranium-235 fission equation with all mass and atomic numbers.',True),
 'q9-coil':('paper',7,(433,353,541,534),SEC,[],'Square coil rotating about an axis through midpoints of opposite sides.',False),
 'q10a-beta-solution':('scheme',13,(77,267,182,287),SEC,[],'Official beta-decay equation with neutron, hydrogen nucleus, electron and neutrino.',True),
 'q10a-annihilation':('paper',8,(259,347,337,367),SEC,[],'The printed electron–positron annihilation equation producing two gamma-ray photons.',False),
 'q12a-underlined':('paper',10,(83,103,372,136),SEC,[],'The source underlines simple harmonic motion and asks for its meaning.',False),
 'q12b-data':('paper',10,(109,550,484,605),SEC,[],'All eight daily radon activity readings, with activity in megabecquerels.',False),
 'q12c-defibrillator':('paper',11,(360,65,555,169),SEC,[],'The source defibrillator circuit, including the charged capacitor, switch and coil.',False,[(523,64,555,75)]),
}

# Canonical-topic review against the shared Physics curriculum crosswalk.
# Higher Level's reference set has no unifying-strand Atlas heading, so lab
# cards use their physical content node, as the preceding Higher ledgers do.
for _t in TASKS:
 _q=int(_t['ref'].split('(')[0][1:])
 if _q in (1,2,3,4):_t['topic']={1:'phys-1-2',2:'phys-2-3',3:'phys-2-6',4:'phys-3-3'}[_q]
 if _t['key']=='5g':_t['topic']='phys-3-2'
 if _t['key']=='5f' or _t['key'] in ('Q12(d):einstein','Q12(d):kinetic-energy'):_t['topic']='phys-4-2'
 if _q==8 and _t['topic']=='phys-4-4':_t['topic']='phys-4-5' if _t['key']=='Q8:fission-energy' else 'phys-4-6'
 if _t['key'] in ('Q7:resonance','Q7:resonance-experiment','7i','7ii','Q7:closed-pipe'):_t['topic']='phys-2-6'
 if _t['key'] in ('Q9:faraday-law','Q9:faraday-experiment','Q9:induced-emf') or (_t['ref']=='Q10(b)' and _t['topic']=='phys-3-4'):_t['topic']='phys-3-6'
 if _t['key']=='Q12(c):electric-field':_t['topic']='phys-3-2'
 # Put split tasks' shared imperative directly in the displayed question.
 if _t['key'] in ('6bi','6bii','7i','7ii','12ai','12aii'):
  _prefix=next(x for x in _t['stem'] if x.get('start')=='Calculate')
  _t['stem'].remove(_prefix);_t['q']=[_prefix,_t['q']]
 if _t['key'] in ('7iii','7iv'):
  _t['stem']=[P(6,'A source emits sound in all directions.')]
  _t['q']=[P(6,'Describe the effect of doubling the distance from the source to an observer on'),_t['q']]
ASK_EXEMPT=[(11,'junction surrounded by a pair of conductors. When light falls on','When-clause describes the solar panel; retained in SOLAR12, not a question.')]

# Final presentation review: keep every referenced data table visible even on
# conceptual experiment cards; preserve the printed subscript and radical layouts.
FIGURES.update({
 'q5i-solution':('scheme',8,(97,594,166,658),SEC,[],'Official parallel-resistance working, with the total-resistance subscript and stacked fractions.',True),
 'q6bi-solution':('scheme',9,(73,379,264,415),SEC,[],'Official horizontal-velocity calculation, with the H subscript and cosine component.',True),
 'q7i-solution':('scheme',10,(83,240,244,314),SEC,[],'Official mass-per-unit-length, string-frequency and tension working with the square root and stacked fractions.',True),
})
for _t in TASKS:
 _q=int(_t['ref'].split('(')[0][1:])
 if _q in (1,2,3,4) and not _t['fig']:_t['fig']=f'q{_q}-data'
 if _t['key']=='Q12(b):definition':_t['fig']='q12b-data'
 if _t['key']=='5i':_t['fig']='q5i-solution'
 if _t['key']=='7i':_t['fig']='q7i-solution'
 # The jump already has a question-side photograph. Its calculation keeps the
 # source's H subscript in a solution image; the full launch data remain in text.
 if _t['key']=='6bi':_t['fig']='q6bi-solution'
# Pointer scan false positives: Q10(b) asks the candidate to DRAW the circuit,
# with no source circuit supplied; Q11(d)'s image is an optical image, not a figure.
