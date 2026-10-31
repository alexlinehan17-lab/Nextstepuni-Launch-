"""Clearly attributed NextStepUni examples for omissions in printed SEC solutions.

These are derived teaching diagrams, never represented as SEC source crops.
The original marking criteria remain attached separately by the publisher.
"""
from decimal import Decimal
from io import BytesIO
from math import exp, cos, pi, sqrt, degrees, acos, log

import fitz
from PIL import Image
from reportlab.pdfgen import canvas


def probability_tree_values():
    rain, wet_walk, dry_walk = map(Decimal, ['0.65', '0.75', '0.98'])
    dry, wet_stay, dry_stay = 1-rain, 1-wet_walk, 1-dry_walk
    outcomes = [rain*wet_walk, rain*wet_stay, dry*dry_walk, dry*dry_stay]
    assert sum(outcomes) == 1
    return [rain,dry,wet_walk,wet_stay,dry_walk,dry_stay], outcomes


def render_supplement(name, dpi=200):
    ordinary_2022 = {
        'balls-plot-2022-ol-deferred':lambda dpi:render_balls_2022_ol(dpi,False),
        'balls-readings-2022-ol-deferred':lambda dpi:render_balls_2022_ol(dpi,True),
        'brendan-2022-ol-deferred':lambda dpi:render_cyclists_2022_ol(dpi,'brendan'),
        'colin-2022-ol-deferred':lambda dpi:render_cyclists_2022_ol(dpi,'colin'),
        'cyclists-meeting-2022-ol-deferred':lambda dpi:render_cyclists_2022_ol(dpi,'meeting')}
    if name in ordinary_2022:
        return ordinary_2022[name](dpi)
    higher_2022 = {'matches-chart-2022-hl-deferred':render_matches_2022,
                   'root-three-construction-2022-hl-deferred':render_root_three_2022,
                   'judges-best-fit-2022-hl-deferred':render_judges_2022,
                   'venn-2022-hl-deferred':render_venn_2022,
                   'car-table-2022-hl-deferred':render_car_table_2022,
                   'linear-model-2022-hl-deferred':lambda dpi:render_visitors_2022(dpi,False),
                   'quadratic-model-2022-hl-deferred':lambda dpi:render_visitors_2022(dpi,True)}
    if name in higher_2022:
        return higher_2022[name](dpi)
    if name == 'confidence-2023-ol-deferred':
        return render_confidence_2023_ol(dpi)
    if name == 'inequality-2023-ol-deferred':
        return render_inequality_2023(dpi)
    higher_2023 = {'sine-proof-2023-hl-deferred':render_sine_proof_2023,
                   'male-proportion-2023-hl-deferred':render_male_proportion_2023,
                   'eyedrops-test-2023-hl-deferred':render_eyedrops_test_2023}
    if name in higher_2023:
        return higher_2023[name](dpi)
    if name in ['trout-2023-hl-deferred','trout-context-2023-hl-deferred']:
        return render_trout_2023(dpi,comparison=name=='trout-2023-hl-deferred')
    ordinary2 = {'parallelogram-2024-ol-deferred':render_parallelogram_2024,
                 'vanilla-test-2024-ol-deferred':render_vanilla_test_2024,
                 'icecream-points-2024-ol-deferred':lambda dpi:render_icecream_2024(dpi,False),
                 'icecream-outlier-2024-ol-deferred':lambda dpi:render_icecream_2024(dpi,True)}
    if name in ordinary2:
        return ordinary2[name](dpi)
    ordinary = {'firework-2024-ol-deferred':render_firework_2024, 'data-growth-2024-ol-deferred':render_data_growth_2024}
    if name in ordinary:
        return ordinary[name](dpi)
    paper2 = {'tangent-2024-hl-deferred':render_tangent_2024,
              'double-angle-2024-hl-deferred':render_double_angle_2024,
              'confidence-2024-hl-deferred':render_confidence_2024,
              'scatter-2024-hl-deferred':render_scatter_2024,
              'wheel-2024-hl-deferred':render_wheel_2024}
    if name in paper2:
        return paper2[name](dpi)
    examples = {'argand-2024-hl-deferred':render_argand_2024, 'shed-2024-hl-deferred':render_shed_2024, 'drying-2024-hl-deferred':render_drying_2024, 'pairs-2024-hl-deferred':render_pairs_2024}
    if name in examples:
        return examples[name](dpi)
    if name == 'skydiver-graph-2025-hl-deferred':
        return render_skydiver_graph(dpi)
    if name != 'probability-tree-2025-ol-deferred':
        raise ValueError('Unreviewed worked supplement: '+name)
    branches, outcomes = probability_tree_values()
    buf=BytesIO()
    c=canvas.Canvas(buf,pagesize=(560,400),invariant=1)
    c.setTitle('NextStepUni worked example — 2025 deferred Ordinary Paper 2 Q10(b)(i)')
    c.setFillColorRGB(.12,.12,.11)
    c.setFont('Times-Bold',21)
    c.drawString(22,369,'A completed probability tree')
    c.setFont('Helvetica',10)
    c.drawString(22,349,'NextStepUni worked example · multiply along each branch')
    c.setStrokeColorRGB(.90,.39,.15);c.setLineWidth(2)
    c.line(22,334,538,334)
    c.setStrokeColorRGB(.18,.18,.16);c.setLineWidth(1)
    root=(48,178);rain=(155,250);dry=(155,106)
    leaves=[(278,286),(278,214),(278,142),(278,70)]
    for a,b in [(root,rain),(root,dry),*( (rain,x) for x in leaves[:2]),*((dry,x) for x in leaves[2:])]:
        c.line(*a,*b)
    for x,y in [root,rain,dry,*leaves]:c.circle(x,y,2.5,stroke=0,fill=1)
    c.setFont('Helvetica-Bold',11)
    c.drawString(125,265,'Rain (R)');c.drawString(125,88,'Dry (D)')
    c.setFont('Helvetica',11)
    for value,x,y in zip(branches,[86,86,205,205,205,205],[229,128,278,218,134,74]):
        c.drawString(x,y,str(value))
    labels=['R, W','R, N','D, W','D, N']
    products=['0.65 × 0.75','0.65 × 0.25','0.35 × 0.98','0.35 × 0.02']
    for ((x,y),label,product,value) in zip(leaves,labels,products,outcomes):
        c.setFont('Helvetica-Bold',12);c.drawString(292,y-4,label)
        c.setFont('Helvetica',11);c.drawString(356,y+5,product)
        c.setFont('Helvetica-Bold',12);c.drawString(356,y-12,'= '+str(value.normalize()))
    c.setFont('Helvetica',10)
    c.drawString(22,34,'W = walk     N = no walk')
    c.drawString(22,17,'Original SEC credit notes are reproduced below.')
    c.save()
    doc=fitz.open(stream=buf.getvalue(),filetype='pdf')
    return Image.open(BytesIO(doc[0].get_pixmap(dpi=dpi).tobytes('png'))).convert('RGB')


def skydiver_speed(t):
    return 54*(1-exp(-0.2*t))


def render_skydiver_graph(dpi=200):
    """Reconstruct the complete printed-domain graph from the paper's formula."""
    buf=BytesIO()
    c=canvas.Canvas(buf,pagesize=(560,490),invariant=1)
    c.setTitle('NextStepUni worked example — 2025 deferred Higher Paper 1 Q10(a)(i)')
    c.setFillColorRGB(.12,.12,.11)
    c.setFont('Times-Bold',21);c.drawString(22,459,'The skydiver’s speed')
    c.setFont('Helvetica',10);c.drawString(22,439,'NextStepUni worked example · table values to 1 decimal place')
    c.setStrokeColorRGB(.90,.39,.15);c.setLineWidth(2);c.line(22,425,538,425)
    left,width=22,516
    c.setStrokeColorRGB(.72,.72,.69);c.setLineWidth(.6)
    for y in [412,388,364]:c.line(left,y,left+width,y)
    for i in range(11):
        x=left+i*width/10;c.line(x,364,x,412)
    c.setFont('Times-Italic',12);c.drawCentredString(left+width/20,396,'t');c.drawCentredString(left+width/20,372,'V(t)')
    c.setFont('Helvetica',11)
    for i,t in enumerate(range(0,33,4),1):
        x=left+(i+.5)*width/10
        c.drawCentredString(x,396,str(t));c.drawCentredString(x,372,f'{skydiver_speed(t):.1f}')
    x0,y0,w,h=78,86,430,228
    c.setFont('Helvetica',10);c.drawString(x0,337,'Speed V(t) (m/s)')
    c.setStrokeColorRGB(.87,.87,.85);c.setLineWidth(.5)
    for t in range(0,33,4):
        x=x0+w*t/32;c.line(x,y0,x,y0+h)
    for v in range(0,61,10):
        y=y0+h*v/60;c.line(x0,y,x0+w,y)
    c.setStrokeColorRGB(.15,.15,.14);c.setLineWidth(1)
    c.line(x0,y0,x0+w+6,y0);c.line(x0,y0,x0,y0+h+6)
    c.setFont('Helvetica',10)
    for t in range(0,33,4):
        x=x0+w*t/32;c.line(x,y0-3,x,y0+3);c.drawCentredString(x,y0-18,str(t))
    for v in range(0,61,10):
        y=y0+h*v/60;c.line(x0-3,y,x0+3,y);c.drawRightString(x0-10,y-3,str(v))
    c.drawRightString(x0+w,44,'Time t (seconds)')
    curve=c.beginPath();curve.moveTo(x0,y0)
    for i in range(1,321):
        t=i/10;curve.lineTo(x0+w*t/32,y0+h*skydiver_speed(t)/60)
    c.setLineWidth(1.7);c.drawPath(curve)
    for t in range(0,33,4):c.circle(x0+w*t/32,y0+h*skydiver_speed(t)/60,2.3,stroke=0,fill=1)
    c.setFont('Helvetica',9);c.drawString(22,18,'Original SEC credit notes are reproduced below. Full original scheme remains available.')
    c.save()
    doc=fitz.open(stream=buf.getvalue(),filetype='pdf')
    return Image.open(BytesIO(doc[0].get_pixmap(dpi=dpi).tobytes('png'))).convert('RGB')


def shed_profit(x):
    return 400*x-5*x*x-0.4*x*x*x-900


def drying_water(t,k=-0.079):
    return 5+20*exp(k*t)


def _example_canvas(title,subtitle,height,footer='NextStepUni worked example. Original SEC credit notes follow below.'):
    buf=BytesIO(); c=canvas.Canvas(buf,pagesize=(560,height),invariant=1)
    c.setTitle('NextStepUni worked example — '+title)
    c.setFillColorRGB(.12,.12,.11)
    c.setFont('Times-Bold',21);c.drawString(22,height-31,title)
    c.setFont('Helvetica',10);c.drawString(22,height-51,subtitle)
    c.setStrokeColorRGB(.90,.39,.15);c.setLineWidth(2);c.line(22,height-65,538,height-65)
    c.setStrokeColorRGB(.18,.18,.16);c.setLineWidth(1)
    c.setFont('Helvetica',9);c.drawString(22,17,footer)
    return buf,c


def _example_image(buf,c,dpi):
    c.save();doc=fitz.open(stream=buf.getvalue(),filetype='pdf')
    return Image.open(BytesIO(doc[0].get_pixmap(dpi=dpi).tobytes('png'))).convert('RGB')


def render_sine_proof_2023(dpi):
    buf,c=_example_canvas('Completing the sine addition proof',
        '2023 deferred Higher Paper 2 · Q4(a)(i) · using the cosine difference identity',336)
    c.setFont('Times-Roman',16)
    c.drawString(28,237,'sin(A + B) = cos[90° - (A + B)]')
    c.drawString(108,201,'= cos[(90° - A) - B]')
    c.drawString(108,165,'= cos(90° - A) cos B + sin(90° - A) sin B')
    c.setFont('Helvetica',10)
    c.drawString(28,125,'Use cos(90° - A) = sin A and sin(90° - A) = cos A:')
    c.setFont('Times-Bold',18)
    c.drawString(28,87,'sin(A + B) = sin A cos B + cos A sin B')
    c.setFont('Helvetica',10)
    c.drawString(28,47,'This supplies the final substitution and conclusion omitted in the printed solution.')
    return _example_image(buf,c,dpi)


def render_inequality_2023(dpi):
    buf,c=_example_canvas('All real solutions on a number line',
        '2023 deferred Ordinary Paper 1 · Q2(a) · include every value from -2 upwards',290)
    c.setFont('Times-Italic',23);c.drawString(28,181,'x ≥ -2')
    left,right,base=58,510,110
    def X(value):return left+(value+4)*(right-left)/7
    c.setStrokeColorRGB(.45,.45,.42);c.setLineWidth(.8);c.line(left-10,base,right+10,base)
    c.setFont('Helvetica',10)
    for value in range(-4,4):
        c.line(X(value),base-4,X(value),base+4);c.drawCentredString(X(value),base-21,str(value))
    c.setStrokeColorRGB(.90,.39,.15);c.setFillColorRGB(.90,.39,.15);c.setLineWidth(2.6)
    c.line(X(-2),base+20,right+8,base+20);c.circle(X(-2),base+20,4.5,stroke=0,fill=1)
    c.line(right+8,base+20,right,base+25);c.line(right+8,base+20,right,base+15)
    c.setFillColorRGB(.12,.12,.11);c.setFont('Helvetica',11)
    c.drawString(28,55,'Closed endpoint: -2 is included. The continuous ray includes non-integers too.')
    return _example_image(buf,c,dpi)


def render_confidence_2023_ol(dpi):
    proportion=740/1276
    error=1/sqrt(1276)
    low,high=100*(proportion-error),100*(proportion+error)
    buf,c=_example_canvas('A confidence interval, with precision',
        '2023 deferred Ordinary Paper 2 · Q10(b)(ii) · round only the final limits',420)
    c.setFont('Helvetica',11);c.drawString(28,326,'Sample proportion')
    c.drawString(300,326,'Margin of error')
    c.setFont('Times-Roman',18)
    c.drawCentredString(63,298,'740');c.line(35,290,91,290);c.drawCentredString(63,270,'1276')
    c.drawString(104,284,'= 0.5799373...')
    c.drawCentredString(338,298,'1');c.line(305,290,371,290)
    c.drawString(323,270,'1276')
    c.line(307,277,312,269);c.line(312,269,317,285);c.line(317,285,366,285)
    c.drawString(382,284,'= 0.0279946...')
    c.setFont('Helvetica',12);c.drawString(28,239,'95% interval = sample proportion ± margin of error')
    c.setFont('Helvetica-Bold',15);c.drawString(28,210,'0.552 to 0.608  (proportions, to 3 decimal places)')
    X=lambda value:58+(value-54)*444/8
    c.setStrokeColorRGB(.6,.6,.57);c.setLineWidth(.7);c.line(X(54),159,X(62),159)
    c.setStrokeColorRGB(.9,.39,.15);c.setLineWidth(4);c.line(X(low),159,X(high),159)
    c.setStrokeColorRGB(.2,.2,.18);c.setLineWidth(1);c.setFont('Helvetica',10)
    for value,label in [(low,f'{low:.3f}%'),(100*proportion,f'{100*proportion:.3f}%'),(high,f'{high:.3f}%')]:
        c.line(X(value),153,X(value),165);c.drawCentredString(X(value),138,label)
    c.setFont('Helvetica',11);c.drawString(28,102,'As percentages: 55.194% to 60.793%, to 3 decimal places.')
    c.setFont('Helvetica',10);c.drawString(28,73,'The SEC example rounds the sample percentage early to 57.99%.')
    c.drawString(28,55,'Its printed interval is 55.191% to 60.789%. The official credit notes follow.')
    return _example_image(buf,c,dpi)


def render_male_proportion_2023(dpi):
    buf,c=_example_canvas('From the ratio to the proportion',
        '2023 deferred Higher Paper 2 · Q9(d) · the share of all candidates',350)
    c.setFont('Times-Roman',18);c.drawString(28,249,'Male : female = 3 : 2')
    c.setFont('Helvetica',11);c.drawString(28,222,'Five equal shares in total. Three of those shares are male.')
    for i in range(5):
        c.setFillColorRGB(*((.16,.16,.15) if i<3 else (.93,.93,.91)))
        c.setStrokeColorRGB(.16,.16,.15);c.rect(28+i*100,160,100,36,stroke=1,fill=1)
    c.setStrokeColorRGB(1,1,1)
    for x in [128,228]:c.line(x,161,x,195)
    c.setStrokeColorRGB(.18,.18,.16)
    c.setFillColorRGB(.12,.12,.11);c.setFont('Helvetica',10)
    c.drawCentredString(178,143,'Male: 3 shares');c.drawCentredString(428,143,'Female: 2 shares')
    c.setFont('Times-Roman',19);c.drawString(28,94,'Proportion male =')
    for x,num,den in [(195,'3','3 + 2'),(294,'3','5')]:
        c.drawCentredString(x,104,num);c.line(x-24,99,x+24,99);c.drawCentredString(x,79,den)
    c.drawString(239,94,'=');c.drawString(335,94,'= 0.6 = 60%')
    c.setFont('Helvetica',10);c.drawString(28,45,'Check: 71 × 0.6 + 73 × 0.4 = 71.8, the overall mean given in the question.')
    return _example_image(buf,c,dpi)


def render_eyedrops_test_2023(dpi):
    z=(9.96-10)/(.18/sqrt(50))
    buf,c=_example_canvas('What the hypothesis test tells us',
        '2023 deferred Higher Paper 2 · Q10(c) · a two-sided test at 5%',440)
    c.setFont('Helvetica',12)
    c.drawString(28,346,'Null hypothesis: population mean = 10 ml.')
    c.drawString(28,323,'Alternative hypothesis: population mean differs from 10 ml.')
    c.setFont('Times-Italic',20);c.drawString(28,269,'z =')
    c.setFont('Times-Roman',18)
    c.drawCentredString(136,290,'9.96 - 10');c.line(76,282,196,282)
    c.drawCentredString(136,265,'0.18');c.line(112,259,160,259)
    c.drawString(130,240,'50')
    # A nested standard-error fraction, with a separate radical over 50.
    c.line(116,247,121,240);c.line(121,240,125,255);c.line(125,255,150,255)
    c.drawString(218,269,'= -1.5713')
    x0,x1,y=65,495,211
    def X(value):return x0+(value+3)*(x1-x0)/6
    c.line(x0,y,x1,y)
    c.setFont('Helvetica',10)
    for value in [-1.96,0,1.96]:
        c.line(X(value),y-4,X(value),y+4);c.drawCentredString(X(value),y-20,str(value))
    c.setFillColorRGB(.90,.39,.15);c.circle(X(z),y,3.5,stroke=0,fill=1)
    c.setFillColorRGB(.12,.12,.11);c.setFont('Helvetica-Bold',10)
    c.drawCentredString(X(z),y+15,'z = -1.57')
    c.setFont('Helvetica',10)
    c.drawCentredString((X(-1.96)+X(1.96))/2,166,'Between the critical values -1.96 and +1.96')
    c.setFont('Times-Bold',18);c.drawString(28,126,'Fail to reject the null hypothesis.')
    c.setFont('Helvetica',12)
    c.drawString(28,97,'There is insufficient evidence of a change in the mean at the 5% level.')
    c.drawString(28,72,'This does not prove that the mean has stayed at 10 ml.')
    c.setFont('Helvetica',10);c.drawString(28,42,'The original scheme’s calculation is correct; its final claim is too strong.')
    return _example_image(buf,c,dpi)


def render_argand_2024(dpi):
    buf,c=_example_canvas('Labelling the four complex numbers','2024 deferred Higher Paper 1 · Q4(b) · schematic, with no numeric scale',435)
    ox,oy,unit=280,157,43
    c.line(90,oy,450,oy);c.line(ox,55,ox,354)
    for x,y,dx,dy in [(450,oy,-7,4),(450,oy,-7,-4),(ox,354,-4,-7),(ox,354,4,-7)]:c.line(x,y,x+dx,y+dy)
    c.setFont('Times-Italic',14);c.drawString(458,oy-4,'Re');c.drawString(ox+10,348,'Im')
    # These proportional vectors reproduce the relationships, not coordinates claimed by the paper.
    for label,x,y,explanation in [('z',-1,2,'z'),('y',-2,4,'y = 2z'),('x',1,-2,'x = -z'),('w',-2,-1,'w = iz')]:
        px,py=ox+x*unit,oy+y*unit;c.circle(px,py,3,stroke=0,fill=1)
        c.setFont('Times-Italic',17);c.drawString(px+10,py-4,explanation)
    c.setFont('Helvetica',10);c.drawString(22,35,'Doubling stretches from the origin; negation turns 180°; multiplying by i turns 90° anticlockwise.')
    return _example_image(buf,c,dpi)


def render_shed_2024(dpi):
    buf,c=_example_canvas('Profit from shed type F','2024 deferred Higher Paper 1 · Q7(a) · corrected table and complete graph',490)
    left,width=22,516
    c.setStrokeColorRGB(.72,.72,.69);c.setLineWidth(.6)
    for y in [412,388,364]:c.line(left,y,left+width,y)
    for i in range(8):
        x=left+i*width/7;c.line(x,364,x,412)
    c.setFont('Times-Italic',12);c.drawCentredString(left+width/14,396,'x');c.drawCentredString(left+width/14,372,'f(x)')
    c.setFont('Helvetica',11)
    for i,x in enumerate(range(0,26,5),1):
        px=left+(i+.5)*width/7;c.drawCentredString(px,396,str(x));c.drawCentredString(px,372,str(round(shed_profit(x))))
    x0,y0,w,h=78,87,430,228
    def X(x):return x0+w*x/25
    def Y(y):return y0+h*(y+1000)/4000
    c.setFont('Helvetica',10);c.drawString(x0,337,'Profit f(x) (euro)')
    c.setStrokeColorRGB(.87,.87,.85);c.setLineWidth(.5)
    for x in range(0,26,5):c.line(X(x),y0,X(x),y0+h)
    for y in range(-1000,3001,1000):c.line(x0,Y(y),x0+w,Y(y))
    c.setStrokeColorRGB(.15,.15,.14);c.setLineWidth(1);c.line(x0,Y(0),x0+w+6,Y(0));c.line(x0,y0,x0,y0+h+6)
    c.setFont('Helvetica',10)
    for x in range(0,26,5):c.drawCentredString(X(x),y0-18,str(x))
    for y in range(-1000,3001,1000):c.drawRightString(x0-10,Y(y)-3,str(y))
    c.drawRightString(x0+w,44,'Number of sheds x')
    path=c.beginPath();path.moveTo(X(0),Y(shed_profit(0)))
    for i in range(1,501):
        x=i/20;path.lineTo(X(x),Y(shed_profit(x)))
    c.setLineWidth(1.7);c.drawPath(path)
    for x in range(0,26,5):c.circle(X(x),Y(shed_profit(x)),2.4,stroke=0,fill=1)
    return _example_image(buf,c,dpi)


def render_drying_2024(dpi):
    buf,c=_example_canvas('A possible faster drying curve','2024 deferred Higher Paper 1 · Q8(e) · one valid example: k = -0.15',430)
    x0,y0,w,h=72,100,430,215
    def X(t):return x0+w*t/60
    def Y(y):return y0+h*y/25
    c.setFont('Helvetica',10);c.drawString(x0,338,'Water content (%)')
    c.setStrokeColorRGB(.87,.87,.85);c.setLineWidth(.5)
    for t in range(0,61,10):c.line(X(t),y0,X(t),y0+h)
    for y in range(0,26,5):c.line(x0,Y(y),x0+w,Y(y))
    c.setStrokeColorRGB(.15,.15,.14);c.setLineWidth(1);c.line(x0,y0,x0+w+6,y0);c.line(x0,y0,x0,y0+h+6)
    c.setFont('Helvetica',10)
    for t in range(0,61,10):c.drawCentredString(X(t),y0-18,str(t))
    for y in range(0,26,5):c.drawRightString(x0-10,Y(y)-3,str(y))
    c.drawRightString(x0+w,58,'Time t (weeks)')
    c.setDash(4,3);c.line(x0,Y(5),x0+w,Y(5));c.setDash()
    for k,col in [(-.079,(.15,.15,.14)),(-.15,(.90,.39,.15))]:
        c.setStrokeColorRGB(*col);c.setLineWidth(1.8)
        path=c.beginPath();path.moveTo(X(0),Y(25))
        for i in range(1,601):path.lineTo(X(i/10),Y(drying_water(i/10,k)))
        c.drawPath(path)
    c.setFont('Times-Italic',13);c.drawString(X(22),Y(10),'w(t)')
    c.setFillColorRGB(.90,.39,.15);c.drawString(X(8),Y(12),'u(t)')
    c.setFillColorRGB(.12,.12,.11);c.setFont('Helvetica',10)
    c.drawString(22,36,'Both start at 25%. For t > 0, u(t) lies below w(t). Both approach 5%.')
    return _example_image(buf,c,dpi)


def render_pairs_2024(dpi):
    buf,c=_example_canvas('The two simultaneous solutions','2024 deferred Higher Paper 1 · Q1(c) · corrected pairings',348)
    c.setFont('Times-Roman',16)
    c.drawString(28,253,'4x + 2y = -7')
    c.drawString(280,253,'y = (-7 - 4x) / 2')
    c.drawString(28,218,'Substitute into the first equation:')
    c.drawString(280,218,'x² + 2x - 24 = 0')
    c.drawString(280,188,'(x - 4)(x + 6) = 0')
    for x,value,numerator in [(28,4,'-23'),(295,-6,'17')]:
        c.setFont('Times-Bold',18);c.drawString(x,144,f'x = {value}')
        c.setFont('Times-Roman',17);c.drawString(x,109,f'y = (-7 - 4({value})) / 2')
        c.drawString(x,68,'y =');c.drawCentredString(x+61,76,numerator)
        c.line(x+43,71,x+79,71);c.drawCentredString(x+61,53,'2')
    return _example_image(buf,c,dpi)


def wheel_height(t):
    return 30-30*cos(5*pi*t)


def render_wheel_2024(dpi):
    buf,c=_example_canvas('The height of the nail','2024 deferred Higher Paper 2 · Q10(a) · correct time scale and complete graph',490)
    left,width=22,516
    c.setStrokeColorRGB(.72,.72,.69);c.setLineWidth(.6)
    for y in [412,388,364]:c.line(left,y,left+width,y)
    for i in range(11):
        x=left+i*width/10;c.line(x,364,x,412)
    c.setFont('Times-Italic',12);c.drawCentredString(left+width/20,396,'t');c.drawCentredString(left+width/20,372,'h(t)')
    c.setFont('Helvetica',11)
    for i in range(9):
        x=left+(i+1.5)*width/10;c.drawCentredString(x,396,f'{i/10:g}');c.drawCentredString(x,372,str(round(wheel_height(i/10))))
    x0,y0,w,h=72,87,430,228
    def X(t):return x0+w*t/.8
    def Y(y):return y0+h*y/70
    c.setFont('Helvetica',10);c.drawString(x0,337,'Height h(t) (cm)')
    c.setStrokeColorRGB(.87,.87,.85);c.setLineWidth(.5)
    for i in range(9):c.line(X(i/10),y0,X(i/10),y0+h)
    for y in range(0,71,10):c.line(x0,Y(y),x0+w,Y(y))
    c.setStrokeColorRGB(.15,.15,.14);c.setLineWidth(1);c.line(x0,y0,x0+w+6,y0);c.line(x0,y0,x0,y0+h+6)
    c.setFont('Helvetica',10)
    for i in range(9):c.drawCentredString(X(i/10),y0-18,f'{i/10:g}')
    for y in range(0,71,10):c.drawRightString(x0-10,Y(y)-3,str(y))
    c.drawRightString(x0+w,44,'Time t (seconds)')
    path=c.beginPath();path.moveTo(X(0),Y(0))
    for i in range(1,801):path.lineTo(X(i/1000),Y(wheel_height(i/1000)))
    c.setLineWidth(1.7);c.drawPath(path)
    for i in range(9):c.circle(X(i/10),Y(wheel_height(i/10)),2.3,stroke=0,fill=1)
    return _example_image(buf,c,dpi)


def render_double_angle_2024(dpi):
    buf,c=_example_canvas('Proving the double-angle identity','2024 deferred Higher Paper 2 · Q4(b)(i) · corrected notation',285)
    c.setFont('Times-Roman',17)
    c.drawString(28,181,'sin(A + B) = sin A cos B + cos A sin B')
    c.setFont('Helvetica',11);c.drawString(28,149,'Set B = A:')
    c.setFont('Times-Roman',17)
    c.drawString(28,112,'sin(2A) = sin A cos A + cos A sin A')
    c.drawString(88,76,'= 2 sin A cos A')
    return _example_image(buf,c,dpi)


def render_confidence_2024(dpi):
    buf,c=_example_canvas('Interpreting the confidence interval','2024 deferred Higher Paper 2 · Q7(c) · a population proportion',285)
    c.setFont('Times-Bold',21);c.drawString(28,179,'Estimated infected proportion: 22.9% to 37.1%')
    c.setFont('Helvetica',12)
    for y,line in zip([143,124,105,74,55],[
        'If we repeatedly took random samples of 160 trees and built an',
        'interval in this way, about 95% of those intervals would contain',
        'the true proportion of infected trees in the forest.',
        'The 95% refers to the long-run success rate of this method.',
        'It does not describe sample means falling inside this one interval.']):c.drawString(28,y,line)
    return _example_image(buf,c,dpi)


def render_tangent_2024(dpi):
    buf,c=_example_canvas('Constructing the tangent at Q','2024 deferred Higher Paper 2 · Q3(a) · compass and straight edge',495)
    # A rotation of the original configuration; no lengths or coordinates are claimed.
    c.saveState();c.translate(260,265);c.rotate(25)
    radius,offset,arc_radius=75,42,62
    c.circle(-radius,0,radius,stroke=1,fill=0)
    c.setDash(3,3);c.setStrokeColorRGB(.48,.48,.45);c.line(-170,0,90,0)
    # Circle centred at Q marks equal distances along PQ, visible as short arcs.
    for start in [-15,165]:c.arc(-offset,-offset,offset,offset,start,30)
    angle=degrees(acos(offset/arc_radius))
    for centre in [-offset,offset]:
        for a in ([angle,-angle] if centre<0 else [180-angle,180+angle]):
            c.arc(centre-arc_radius,-arc_radius,centre+arc_radius,arc_radius,a-22,44)
    c.setDash();c.setStrokeColorRGB(.90,.39,.15);c.setLineWidth(1.7);c.line(0,-116,0,116)
    c.setStrokeColorRGB(.18,.18,.16);c.setLineWidth(1)
    c.line(-radius,0,0,0);c.line(-10,0,-10,10);c.line(-10,10,0,10)
    height=sqrt(arc_radius**2-offset**2)
    for x,y,label,dx,dy in [(-radius,0,'P',-10,-19),(0,0,'Q',8,-15),(-offset,0,'U',-7,-19),(offset,0,'V',0,-19),(0,height,'A',8,1),(0,-height,'B',8,-2)]:
        c.circle(x,y,2.2,stroke=0,fill=1);c.saveState();c.translate(x+dx,y+dy);c.rotate(-25);c.setFont('Times-Italic',13);c.drawString(0,0,label);c.restoreState()
    c.restoreState();c.setFillColorRGB(.12,.12,.11);c.setFont('Helvetica',11)
    for y,t in [(109,'1. Extend PQ; mark U and V at equal compass distances from Q.'),(87,'2. From U and V, draw equal-radius arcs meeting at A and B.'),(65,'3. Draw AB. It passes through Q and is perpendicular to PQ.'),(43,'The perpendicular to a radius at the circle is the tangent.')]:c.drawString(22,y,t)
    return _example_image(buf,c,dpi)


def render_scatter_2024(dpi):
    """Overlay a by-eye example on the exact SEC vector plot, preserving every dot."""
    from pathlib import Path
    import hashlib
    path=Path(__file__).resolve().parents[4]/'paper-trail-corpus/deferredexams/2024/LC003ALP200EV.pdf'
    source=fitz.open(path)
    # The same immutable source hash as the reviewed presentation plan.
    import json
    plan=json.loads((Path(__file__).parent/'2024-hl-p2-deferred-presentation.json').read_text())
    assert hashlib.sha256(path.read_bytes()).hexdigest()==plan['questionSha256']
    copy=fitz.open();copy.insert_pdf(source,from_page=23,to_page=23);page=copy[0]
    def X(weight):return 145.86+(419.69-145.86)*weight/140
    def Y(height):return 272.27-(272.27-135.09)*(height-1.65)/.45
    # A reasonable by-eye line: height = 0.006 * weight + 1.26.
    page.draw_line((X(65),Y(1.65)),(X(140),Y(2.10)),color=(.9,.39,.15),width=1.3)
    page.draw_polyline([(X(0),Y(1.8)),(X(90),Y(1.8)),(X(90),Y(1.65))],color=(.18,.18,.16),width=.8,dashes='[3 3]')
    clip=fitz.Rect(88,118,510,301)
    plot=Image.open(BytesIO(page.get_pixmap(dpi=dpi,clip=clip).tobytes('png'))).convert('RGB')
    buf,c=_example_canvas('Reading a line of best fit','2024 deferred Higher Paper 2 · Q9(a)(ii) · one reasonable by-eye line',390)
    from reportlab.lib.utils import ImageReader
    c.drawImage(ImageReader(plot),22,93,width=516,height=516*clip.height/clip.width)
    c.setFont('Helvetica',11);c.drawString(22,70,'Read across from 1.80 m to the line, then down: approximately 90 kg.')
    c.setFont('Helvetica',9);c.drawString(22,47,'Original scatterplot: © State Examinations Commission. Line and guides: NextStepUni.')
    return _example_image(buf,c,dpi)


def firework_height(t):
    return -4.8*t*t+41.65*t+20


def firework_sea_time():
    return (41.65+sqrt(41.65**2+4*4.8*20))/(2*4.8)


def world_data(t):
    return 64*1.19**t


def world_data_time(amount):
    return log(amount/64)/log(1.19)


def render_firework_2024(dpi):
    buf,c=_example_canvas('Continuing the curve to sea level','2024 deferred Ordinary Paper 1 · Q8(a)(iv)',465)
    x0,y0,w,h=65,95,445,245
    X=lambda t:x0+w*t/10
    Y=lambda height:y0+h*height/120
    c.setFont('Helvetica',10);c.drawString(x0,358,'Height above sea level, h(t) (metres)')
    c.setStrokeColorRGB(.87,.87,.85);c.setLineWidth(.5)
    for t in range(11):c.line(X(t),y0,X(t),y0+h)
    for y in range(0,121,20):c.line(x0,Y(y),x0+w,Y(y))
    c.setStrokeColorRGB(.15,.15,.14);c.setLineWidth(1)
    c.line(x0,y0,x0+w+5,y0);c.line(x0,y0,x0,y0+h+5)
    for t in range(11):c.drawCentredString(X(t),y0-17,str(t))
    for y in range(0,121,20):c.drawRightString(x0-9,Y(y)-3,str(y))
    c.drawRightString(x0+w,55,'Time t (seconds)')
    root=firework_sea_time()
    for a,b,col in [(0,8,(.15,.15,.14)),(8,root,(.90,.39,.15))]:
        c.setStrokeColorRGB(*col);c.setLineWidth(1.8)
        path=c.beginPath();path.moveTo(X(a),Y(firework_height(a)))
        for i in range(1,241):
            t=a+(b-a)*i/240;path.lineTo(X(t),Y(max(0,firework_height(t))))
        c.drawPath(path)
    c.setFillColorRGB(.90,.39,.15);c.circle(X(root),Y(0),3,stroke=0,fill=1)
    c.setFillColorRGB(.12,.12,.11);c.setFont('Helvetica-Bold',12)
    c.setFont('Helvetica',11);c.drawString(22,382,'Extend beyond t = 8 and read the horizontal intercept: about 9.1 seconds.')
    c.setFont('Helvetica',10);c.drawString(22,35,'The orange section extends the curve until h(t) = 0; the flight model ends there.')
    return _example_image(buf,c,dpi)


def render_data_growth_2024(dpi):
    buf,c=_example_canvas('Reading growth from the graph','2024 deferred Ordinary Paper 1 · Q9(d)(ii)–(iii)',510)
    x0,y0,w,h=65,147,445,235
    X=lambda t:x0+w*t/8
    Y=lambda amount:y0+h*amount/280
    c.setFont('Helvetica',10);c.drawString(x0,401,'Amount of data (zettabytes)')
    c.setStrokeColorRGB(.87,.87,.85);c.setLineWidth(.5)
    for t in range(9):c.line(X(t),y0,X(t),y0+h)
    for y in range(0,251,50):c.line(x0,Y(y),x0+w,Y(y))
    c.setStrokeColorRGB(.15,.15,.14);c.setLineWidth(1)
    c.line(x0,y0,x0+w+5,y0);c.line(x0,y0,x0,y0+h+5)
    for t in range(9):c.drawCentredString(X(t),y0-17,str(2021+t))
    for y in range(0,251,50):c.drawRightString(x0-9,Y(y)-3,str(y))
    c.drawRightString(x0+w,110,'Year (ticks show the start of each year)')
    curve=c.beginPath();curve.moveTo(X(0),Y(world_data(0)))
    for i in range(1,801):curve.lineTo(X(i/100),Y(world_data(i/100)))
    c.setLineWidth(1.7);c.drawPath(curve)
    # Exact 200 crossing; the doubling example uses rounded graph readings, as the SEC does.
    for amount in [75,150,200]:
        t=world_data_time(amount)
        c.setStrokeColorRGB(*((.90,.39,.15) if amount==200 else (.43,.43,.40)))
        c.setLineWidth(1);c.setDash(4,3)
        c.lines([(x0,Y(amount),X(t),Y(amount)),(X(t),Y(amount),X(t),y0)])
        c.setDash();c.setFillColorRGB(.12,.12,.11);c.circle(X(t),Y(amount),2.4,stroke=0,fill=1)
        if amount in [75,150]:
            c.setFont('Helvetica',10);c.drawString(X(t)+8,Y(amount)-4,str(amount))
    c.setFont('Helvetica-Bold',12);c.drawString(22,82,'(ii) The curve first reaches 200 during 2027.')
    c.setFont('Helvetica',11);c.drawString(22,61,'(iii) About 75 in 2022 grows to about 150 in 2026: approximately 4 years.')
    c.drawString(22,42,'Both answers are graph readings; the dashed lines show the working.')
    return _example_image(buf,c,dpi)


def parallelogram_2024_vertices():
    return [(0,0),(2,0),(0,4),(-2,4)]


def vanilla_2024_interval(rounded=True):
    proportion,margin=(.23,.056) if rounded else (74/320,1/sqrt(320))
    return proportion-margin,proportion+margin


def render_parallelogram_2024(dpi):
    buf,c=_example_canvas('Completing the parallelogram','2024 deferred Ordinary Paper 2 · Q1(a)(iii)',460)
    X=lambda x:280+45*x
    Y=lambda y:125+45*y
    c.setFont('Helvetica',10);c.setStrokeColorRGB(.86,.86,.84);c.setLineWidth(.5)
    for x in range(-4,5):c.line(X(x),Y(-1),X(x),Y(5))
    for y in range(-1,6):c.line(X(-4),Y(y),X(4),Y(y))
    c.setStrokeColorRGB(.15,.15,.14);c.setLineWidth(.9)
    c.line(X(-4),Y(0),X(4)+10,Y(0));c.line(X(0),Y(-1),X(0),Y(5)+10)
    for x in [-4,-3,-2,-1,1,3,4]:c.drawCentredString(X(x),Y(0)-15,str(x))
    for y in [-1,1,2,3,5]:c.drawRightString(X(0)-8,Y(y)-3,str(y))
    c.drawString(X(4)+14,Y(0)-4,'x');c.drawString(X(0)+10,Y(5)+10,'y')
    vertices=parallelogram_2024_vertices();path=c.beginPath();path.moveTo(X(0),Y(0))
    for x,y in vertices[1:]:path.lineTo(X(x),Y(y))
    path.close();c.setStrokeColorRGB(.90,.39,.15);c.setLineWidth(2);c.drawPath(path)
    c.setFillColorRGB(.12,.12,.11);c.setFont('Helvetica-Bold',11)
    for (x,y),label,dx,dy in zip(vertices,['O (0, 0)','P (2, 0)','Q (0, 4)','R (-2, 4)'],[8,8,8,-65],[-32,-32,10,10]):
        c.circle(X(x),Y(y),2.7,stroke=0,fill=1);c.drawString(X(x)+dx,Y(y)+dy,label)
    c.setFont('Helvetica',11);c.drawString(22,60,'OP and RQ are horizontal and equal; OR is parallel and equal to PQ.')
    c.drawString(22,40,'Therefore R = (-2, 4). The four orange sides complete OPQR.')
    return _example_image(buf,c,dpi)


def render_vanilla_test_2024(dpi):
    buf,c=_example_canvas('Testing whether the proportion changed','2024 deferred Ordinary Paper 2 · Q7(c)(iii)',365)
    c.setFont('Helvetica',11);c.drawString(22,280,'Let p be the proportion of customers whose favourite flavour is vanilla.')
    c.setFont('Helvetica-Bold',13);c.drawString(22,252,'H0: p = 0.30');c.drawString(240,252,'H1: p is not 0.30')
    c.setFont('Helvetica',11);c.drawString(22,224,'Use the rounded answers from (i) and (ii): 23% ± 5.6%.')
    c.setFont('Helvetica-Bold',14);c.drawString(22,197,'95% confidence interval: 17.4% to 28.6%')
    X=lambda value:65+(value-.15)*430/.18
    c.setStrokeColorRGB(.55,.55,.52);c.setLineWidth(1);c.line(X(.15),147,X(.33),147)
    lo,hi=vanilla_2024_interval();c.setStrokeColorRGB(.90,.39,.15);c.setLineWidth(4);c.line(X(lo),147,X(hi),147)
    c.setLineWidth(1);c.setFont('Helvetica',10)
    for value,label in [(lo,'17.4%'),(hi,'28.6%'),(.30,'30%')]:
        c.setStrokeColorRGB(.15,.15,.14);c.line(X(value),141,X(value),153);c.drawCentredString(X(value),127,label)
    c.setFillColorRGB(.12,.12,.11);c.circle(X(.30),147,3,stroke=0,fill=1)
    c.setFont('Helvetica-Bold',12);c.drawString(22,99,'30% is outside the interval. Reject H0 at the 5% level.')
    c.setFont('Helvetica',11);c.drawString(22,77,'There is evidence that the proportion has changed since 2020.')
    c.setFont('Helvetica',10);c.drawString(22,49,'Keeping unrounded values gives approximately 17.5% to 28.7%, as in the scheme.')
    c.drawString(22,31,'Either calculation excludes 30%. Original SEC working and credit notes follow.')
    return _example_image(buf,c,dpi)


def render_icecream_2024(dpi,outlier):
    """Recover the complete embedded SEC plot, clipped by its PDF table cell."""
    import hashlib,json
    from pathlib import Path
    from reportlab.lib.utils import ImageReader
    path=Path(__file__).resolve().parents[4]/'paper-trail-corpus/deferredmarkingschemes/2024/LC003GLP000EV.pdf'
    plan=json.loads((Path(__file__).parent/'2024-ol-p2-deferred-presentation.json').read_text())
    assert hashlib.sha256(path.read_bytes()).hexdigest()==plan['solutionSha256']
    source=fitz.open(path)
    images=source[30].get_images(full=True)
    assert len(images)==1 and images[0][2:4]==(1196,669)
    im=Image.open(BytesIO(source.extract_image(images[0][0])['image'])).convert('RGB')
    title='Recognising the outlier' if outlier else 'Completing the scatterplot'
    part='iv' if outlier else 'i'
    buf,c=_example_canvas(title,f'2024 deferred Ordinary Paper 2 · Q7(a)({part})',475)
    c.drawImage(ImageReader(im),35,115,width=490,height=490*im.height/im.width)
    c.setFont('Helvetica',11)
    if outlier:
        c.drawString(22,91,'The circled point is about 19°C and €147, far below the main trend.')
        c.drawString(22,70,'One possible reason: the stall closed early. This is an illustration, not a fact.')
    else:
        c.drawString(22,91,'Day 1 is the cross at (23, 500); Day 2 is the cross at (17, 400).')
        c.drawString(22,70,'The red circle belongs to part (iv). The graph retains all 14 days.')
    c.setFont('Helvetica',9)
    c.drawString(22,44,'Complete graph extracted unchanged from the SEC scheme; its PDF table clips the right edge.')
    c.drawString(22,29,'Graph: © State Examinations Commission. Explanatory captions: NextStepUni.')
    return _example_image(buf,c,dpi)


def trout_2023(t):
    return 3000/(1+6.5*exp(-.814*t)),2600*(15/13-exp(-.432*t))


def trout_2023_rates(t):
    return 15873*exp(-.814*t)/(1+6.5*exp(-.814*t))**2,1123.2*exp(-.432*t)


def render_trout_2023(dpi,comparison=True):
    height=610 if comparison else 470
    footer=('NextStepUni worked example. Original SEC credit notes follow below.' if comparison else
            'NextStepUni reconstruction from the printed functions. Original question follows below.')
    buf,c=_example_canvas('Two models for the trout population','2023 deferred Higher Paper 1 · Q9(b) · 0 to 8 months',height,footer)
    x0,y0,w,h=66,height-405,462,280
    X=lambda t:x0+t*w/8
    Y=lambda n:y0+n*h/3000
    c.setFont('Helvetica',10);c.setFillColorRGB(.12,.12,.11)
    for j,(label,color) in enumerate([('N(t)',(.12,.12,.11)),('P(t)',(.90,.39,.15))]):
        x=362+j*91;c.setStrokeColorRGB(*color);c.setLineWidth(1.8)
        c.line(x,height-89,x+24,height-89);c.drawString(x+30,height-93,label)
    c.drawString(22,height-93,'Number of trout')
    c.setLineWidth(.5);c.setStrokeColorRGB(.86,.86,.84)
    for n in range(0,3001,500):
        c.line(X(0),Y(n),X(8),Y(n));c.drawRightString(x0-10,Y(n)-3,str(n))
    for t in range(9):
        c.line(X(t),Y(0),X(t),Y(3000));c.drawCentredString(X(t),y0-17,str(t))
    c.setStrokeColorRGB(.2,.2,.18);c.setLineWidth(.8)
    c.line(X(0),Y(0),X(8)+5,Y(0));c.line(X(0),Y(0),X(0),Y(3000)+5)
    c.drawRightString(X(8),y0-37,'Time since stocking (months)')
    for j,color in enumerate([(.12,.12,.11),(.90,.39,.15)]):
        c.setStrokeColorRGB(*color);c.setLineWidth(1.8)
        path=c.beginPath();path.moveTo(X(0),Y(trout_2023(0)[j]))
        for i in range(1,801):path.lineTo(X(i/100),Y(trout_2023(i/100)[j]))
        c.drawPath(path)
    if comparison:
        c.setFillColorRGB(.90,.39,.15)
        for t in range(9):c.circle(X(t),Y(trout_2023(t)[1]),2.6,stroke=0,fill=1)
        c.setFillColorRGB(.12,.12,.11);c.setFont('Helvetica-Bold',11)
        c.drawString(22,142,'Similarity: both populations increase and approach 3000 trout.')
        c.drawString(22,119,'Difference: N initially gets steeper, then flattens.')
        c.setFont('Helvetica',11);c.drawString(22,99,'P flattens throughout: its growth rate decreases from the start.')
        c.setFont('Helvetica',10);c.drawString(22,66,'Height tells us the population. Slope tells us how quickly it is increasing.')
        c.drawString(22,46,'The orange points show the P(t) table values, including the two given values.')
    return _example_image(buf,c,dpi)


def render_venn_2022(dpi):
    buf,c=_example_canvas('Placing all six complex numbers',
        '2022 deferred Higher Paper 1 · Q1(c) · the real and rational-component sets',430)
    c.rect(40,72,480,265,stroke=1,fill=0)
    c.ellipse(68,125,352,305,stroke=1,fill=0)
    c.ellipse(208,125,492,305,stroke=1,fill=0)
    c.setFont('Times-Bold',16)
    c.drawString(65,311,'R');c.drawString(475,311,'X');c.drawString(498,344,'C')
    c.setFont('Times-Roman',18)
    c.drawCentredString(139,207,'√17')
    c.drawCentredString(280,252,'2.5')
    c.setFont('Times-Roman',14)
    c.drawCentredString(280,210,'cos 180° +')
    c.drawCentredString(280,189,'i sin 180°')
    c.setFont('Times-Roman',18)
    c.drawCentredString(417,239,'3i');c.drawCentredString(417,193,'3 + 2i')
    c.drawString(66,90,'π + 5i')
    c.setFont('Helvetica',10)
    c.drawString(22,49,'R = real numbers. X = real and imaginary components both rational. C = complex numbers.')
    return _example_image(buf,c,dpi)


def render_car_table_2022(dpi):
    buf,c=_example_canvas('The first five years start at Year 0',
        '2022 deferred Higher Paper 1 · Q7(a)(i) · multiply each price by 0.75',260)
    labels=['Year','0','1','2','3','4']
    values=['Price (€)','24,000','18,000','13,500','10,125','7,593.75']
    xs=[28,130,218,306,394,482]
    c.setFont('Helvetica-Bold',12)
    for x,label in zip(xs,labels):c.drawString(x,162,label)
    c.line(22,149,538,149)
    c.setFont('Helvetica',12)
    for x,value in zip(xs,values):c.drawString(x,125,value)
    c.setFont('Helvetica',10)
    c.drawString(22,79,'The original scheme shifts the year labels to 1–5. The prices belong to years 0–4.')
    c.drawString(22,56,'The completed values follow the question paper; official credit notes are unchanged.')
    return _example_image(buf,c,dpi)


def render_visitors_2022(dpi,quadratic):
    title='One valid quadratic model' if quadratic else 'A linear model through both weeks'
    part='Q9(a)(ii)' if quadratic else 'Q9(a)(i)'
    buf,c=_example_canvas(title,'2022 deferred Higher Paper 1 · '+part+' · use both observed values',340)
    c.setFont('Times-Roman',18)
    c.drawString(28,243,'V(0) = 2506                 V(1) = 2734')
    if quadratic:
        c.drawString(28,204,'Choose c = 1. Then f = 2506 and d = 227.')
        c.setFont('Times-Bold',23);c.drawString(28,163,'V(x) = x² + 227x + 2506')
        c.setFont('Helvetica',11)
        c.drawString(28,127,'Check: V(1) = 1 + 227 + 2506 = 2734.')
        c.drawString(28,95,'All valid quadratic models have f = 2506 and d = 228 - c, with c ≠ 0.')
        c.drawString(28,66,'The SEC accepts any valid quadratic; this is one worked example.')
    else:
        c.drawString(28,204,'b = 2506                 a = 2734 - 2506 = 228')
        c.setFont('Times-Bold',23);c.drawString(28,163,'V(x) = 228x + 2506')
        c.setFont('Helvetica',11)
        c.drawString(28,127,'Check: V(1) = 228 + 2506 = 2734.')
        c.drawString(28,95,'The source correctly finds a = 228, but its final line prints 288x.')
        c.drawString(28,66,'Use 228x. The original SEC working and credit notes follow.')
    return _example_image(buf,c,dpi)


def render_matches_2022(dpi):
    buf,c=_example_canvas('A labelled frequency chart',
        '2022 deferred Higher Paper 2 · Q1(a) · all 53 boxes',430)
    x0,y0,w,h=70,90,440,235
    c.setFont('Helvetica',10);c.drawString(x0,341,'Number of boxes')
    c.setStrokeColorRGB(.85,.85,.83);c.setLineWidth(.5)
    for v in range(0,19,3):
        yy=y0+h*v/18;c.line(x0,yy,x0+w,yy);c.drawRightString(x0-10,yy-3,str(v))
    c.setStrokeColorRGB(.18,.18,.16);c.setLineWidth(1)
    c.line(x0,y0,x0+w,y0);c.line(x0,y0,x0,y0+h+4)
    for i,(n,freq) in enumerate(zip(range(41,47),[3,8,16,17,8,1])):
        xx=x0+(i+.5)*w/6;hh=h*freq/18
        c.setFillColorRGB(.92,.92,.90);c.rect(xx-18,y0,36,hh,fill=1,stroke=1)
        c.setFillColorRGB(.12,.12,.11);c.drawCentredString(xx,y0-18,str(n));c.drawCentredString(xx,y0+hh+8,str(freq))
    c.drawRightString(x0+w,48,'Number of matches per box')
    return _example_image(buf,c,dpi)


def render_root_three_2022(dpi):
    buf,c=_example_canvas('Constructing a length of √3',
        '2022 deferred Higher Paper 2 · Q6(a) · compass and straightedge example',560)
    u=130;W=(100,300);X=(230,300);Y=(360,300);Z=(295,300+u*sqrt(3)/2)
    c.setStrokeColorRGB(.64,.64,.61);c.setLineWidth(.65);c.setDash(3,3)
    for pt in [X,Y]:c.circle(*pt,u,fill=0,stroke=1)
    c.setDash();c.setStrokeColorRGB(.18,.18,.16);c.setLineWidth(1)
    c.line(78,300,490,300)
    for pt in [X,Y]:c.line(*pt,*Z)
    c.setStrokeColorRGB(.90,.39,.15);c.setLineWidth(2);c.line(*W,*Z)
    c.setFillColorRGB(.12,.12,.11);c.setFont('Times-Italic',15)
    for label,pt,dx,dy in [('W',W,-16,-20),('X',X,-7,-20),('Y',Y,5,-20),('Z',Z,4,10)]:
        c.circle(*pt,2,fill=1,stroke=0);c.drawString(pt[0]+dx,pt[1]+dy,label)
    c.setFont('Times-Roman',14)
    c.drawCentredString(165,312,'1');c.drawCentredString(295,312,'1');c.drawString(328,360,'1')
    c.setFont('Times-Bold',18);c.drawString(170,374,'√3')
    c.setFont('Helvetica',11)
    for yy,txt in [(142,'1. Draw circles centred at X and Y, each with radius XY = 1.'),
                   (121,'2. Mark an intersection Z. Extend YX to meet the X-circle at W.'),
                   (100,'3. Join W to Z and clearly label WZ as the required length.')]:c.drawString(22,yy,txt)
    c.setFont('Times-Roman',14)
    c.drawString(22,64,'XYZ is equilateral, so angle WXZ = 120°.')
    c.drawString(22,42,'WZ² = 1² + 1² - 2(1)(1) cos 120° = 3. Therefore WZ = √3.')
    return _example_image(buf,c,dpi)


def render_judges_2022(dpi):
    buf,c=_example_canvas('A line of best fit and a reading',
        '2022 deferred Higher Paper 2 · Q7(c)(i–ii) · one reasonable by-eye example',480)
    xs=[20,35,6,49,11,19,15,9,14,32];ys=[34,34,27,38,23,33,25,28,30,32]
    x0,y0,w,h=70,145,430,235
    def P(x,y):return x0+w*x/50,y0+h*(y-20)/20
    c.setFont('Helvetica',10);c.drawString(x0,395,'Mike’s score')
    c.setStrokeColorRGB(.85,.85,.83);c.setLineWidth(.5)
    for x in range(0,51,10):
        xx,_=P(x,20);c.line(xx,y0,xx,y0+h);c.drawCentredString(xx,y0-16,str(x))
    for y in range(20,41,5):
        _,yy=P(0,y);c.line(x0,yy,x0+w,yy);c.drawRightString(x0-10,yy-3,str(y))
    c.setStrokeColorRGB(.18,.18,.16);c.setLineWidth(1)
    c.line(x0,y0,x0+w,y0);c.line(x0,y0,x0,y0+h)
    for x,y in zip(xs,ys):c.circle(*P(x,y),2.6,fill=1,stroke=0)
    c.setLineWidth(1.4);c.line(*P(0,24),*P(50,39))
    reading=(35-24)/.3
    c.setStrokeColorRGB(.90,.39,.15);c.setDash(4,3);c.line(*P(0,35),*P(reading,35));c.line(*P(reading,35),*P(reading,20));c.setDash()
    c.setFont('Helvetica',10);c.drawRightString(x0+w,108,'Nuala’s score')
    c.setFont('Helvetica-Bold',11);c.drawString(22,81,'At Mike’s score of 35, this line gives Nuala’s score of about 37.')
    c.setFont('Helvetica',10);c.drawString(22,58,'The example uses y = 0.3x + 24. A different reasonable line can give a different estimate.')
    c.drawString(22,38,'Use points on both sides of your line, and show the reading from your own line.')
    return _example_image(buf,c,dpi)


def render_balls_2022_ol(dpi,readings):
    buf,c=_example_canvas('Reading two height graphs' if readings else 'Plotting Gina’s height graph',
        '2022 deferred Ordinary Paper 1 · Q8(b)' if readings else '2022 deferred Ordinary Paper 1 · Q8(a)(i–ii)',580)
    x0,y0,w,h=65,170,440,300
    def P(t,y):return x0+w*t/4,y0+h*y/25
    c.setFont('Helvetica',10);c.drawString(x0,484,'Height above ground (m)')
    c.setStrokeColorRGB(.85,.85,.83);c.setLineWidth(.5)
    for t in range(9):
        xx,_=P(t/2,0);c.line(xx,y0,xx,y0+h);c.drawCentredString(xx,y0-16,str(t/2).removesuffix('.0'))
    for y in range(0,26,5):
        _,yy=P(0,y);c.line(x0,yy,x0+w,yy);c.drawRightString(x0-10,yy-3,str(y))
    c.setStrokeColorRGB(.18,.18,.16);c.setLineWidth(1);c.line(x0,y0,x0+w,y0);c.line(x0,y0,x0,y0+h)
    hf=lambda t:1+18*t-5*t*t
    gf=lambda t:18+10*t-5*t*t
    for fn,lo,hi,color in [(hf,0,(18+sqrt(344))/10,(.34,.34,.32)),(gf,1,(10+sqrt(460))/10,(.90,.39,.15))]:
        c.setStrokeColorRGB(*color);c.setLineWidth(1.6);path=c.beginPath();path.moveTo(*P(lo,fn(lo)))
        for i in range(1,201):
            t=lo+(hi-lo)*i/200;path.lineTo(*P(t,max(0,fn(t))))
        c.drawPath(path)
    c.setFillColorRGB(.12,.12,.11);c.setFont('Helvetica-Bold',10)
    c.drawString(*P(1.30,23.8),'Gina: g(t)');c.drawString(*P(2.55,18),'Harry: h(t)')
    c.setFont('Helvetica',10);c.drawRightString(x0+w,135,'Time t (seconds, from Harry’s throw)')
    if not readings:
        for t in [1,1.5,2,2.5,3,3.1]:c.circle(*P(t,gf(t)),2.4,fill=1,stroke=0)
        c.setFont('Helvetica-Bold',11);c.drawString(22,105,'Completed table')
        c.setFont('Helvetica',11)
        for i,(t,v) in enumerate(zip(['t','1','1.5','2','2.5','3','3.1'],['g(t)','23','21.75','18','11.75','3','0.95'])):
            xx=46+73*i;c.drawCentredString(xx,82,t);c.drawCentredString(xx,61,v)
        c.setFont('Helvetica',10);c.drawString(22,37,'Plot all six pairs and join with a smooth curve, starting at t = 1.')
    else:
        c.setStrokeColorRGB(.18,.18,.16);c.setLineWidth(1);c.setDash(3,3)
        c.line(*P(1.5,hf(1.5)),*P(1.5,gf(1.5)))
        c.line(*P(1.8,0),*P(1.8,hf(1.8)))
        t=17/8;c.line(*P(0,hf(t)),*P(t,hf(t)));c.setDash()
        c.setFont('Helvetica',10);c.drawString(*P(.15,19.2),'gap ≈ 5 m')
        for t,fn in [(1.5,hf),(1.5,gf),(1.8,hf),(17/8,hf)]:c.circle(*P(t,fn(t)),2.2,fill=1,stroke=0)
        c.setFont('Helvetica',11)
        for yy,txt in [(105,'(i) At t = 1.5, the vertical gap is about 5 m.'),(83,'(ii) Harry’s maximum occurs at about 1.8 seconds.'),(61,'(iii) The curves cross at a height of about 16.7 m.')]:c.drawString(22,yy,txt)
        c.setFont('Helvetica',10);c.drawString(22,37,'Readings are estimates. The original SEC tolerance ranges follow below.')
    return _example_image(buf,c,dpi)


def render_cyclists_2022_ol(dpi,mode):
    title={'brendan':'Plotting Brendan’s journey','colin':'Plotting Colin’s journey','meeting':'Where the two cyclists pass'}[mode]
    part={'brendan':'Q10(c)(i)','colin':'Q10(d)(i)','meeting':'Q10(d)(ii)'}[mode]
    buf,c=_example_canvas(title,'2022 deferred Ordinary Paper 1 · '+part+' · reconstructed from the question',485)
    x0,y0,w,h=65,150,440,230
    def P(t,d):return x0+w*t/5,y0+h*d/64
    c.setFont('Helvetica',10);c.drawString(x0,395,'Distance from P (km)')
    c.setStrokeColorRGB(.85,.85,.83);c.setLineWidth(.5)
    for i in range(11):
        xx,_=P(i/2,0);c.line(xx,y0,xx,y0+h)
        if i%2==0:c.drawCentredString(xx,y0-17,f'{10+i//2}:00')
    for d in range(0,65,8):
        _,yy=P(0,d);c.line(x0,yy,x0+w,yy);c.drawRightString(x0-10,yy-3,str(d))
    c.setStrokeColorRGB(.18,.18,.16);c.setLineWidth(1);c.line(x0,y0,x0+w,y0);c.line(x0,y0,x0,y0+h)
    c.setStrokeColorRGB(.60,.60,.57);path=c.beginPath();path.moveTo(*P(0,0))
    for pt in [(1.5,24),(2.5,24),(5,64)]:path.lineTo(*P(*pt))
    c.drawPath(path);c.setFillColorRGB(.12,.12,.11);c.setFont('Helvetica',10);c.drawString(*P(3.2,44),'Alan')
    if mode in ['brendan','meeting']:
        c.setStrokeColorRGB(.18,.18,.16);c.setLineWidth(1.7);c.line(*P(2,0),*P(14/3,64));c.drawString(*P(3.8,57),'Brendan')
        c.circle(*P(4,48),2,fill=1,stroke=0)
    if mode in ['colin','meeting']:
        c.setStrokeColorRGB(.90,.39,.15);c.setLineWidth(1.7);c.line(*P(0,64),*P(5,0));c.drawString(*P(3.8,18),'Colin')
    if mode=='meeting':
        t=112/36.8;d=24*(t-2);c.setStrokeColorRGB(.18,.18,.16);c.setDash(3,3);c.setLineWidth(1);c.line(*P(t,d),*P(t,0));c.setDash();c.circle(*P(t,d),2.5,fill=1,stroke=0)
        lines=['The intersection is just after 13:00: about 13:03.','The source example is about 13:05; accepted range 13:00–13:20.','Show the reading from the two lines on your graph.']
    elif mode=='brendan':
        lines=['Start at (12:00, 0). Pass Alan at (14:00, 48 km).','Join with a straight line and stop at Q: (14:40, 64 km).','Label the line Brendan. His speed is 48 ÷ 2 = 24 km/h.']
    else:lines=['Join (10:00, 64 km) to (15:00, 0) with one straight line.','The distance from P decreases as Colin travels towards P.','Label the line Colin.']
    c.setFont('Helvetica',10);c.drawRightString(x0+w,112,'Time of day')
    for yy,txt in zip([85,63,41],lines):c.drawString(22,yy,txt)
    return _example_image(buf,c,dpi)
