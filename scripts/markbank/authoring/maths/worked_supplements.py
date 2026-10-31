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
