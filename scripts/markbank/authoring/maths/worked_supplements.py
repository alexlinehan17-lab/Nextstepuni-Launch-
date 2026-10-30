"""Clearly attributed NextStepUni examples for omissions in printed SEC solutions.

These are derived teaching diagrams, never represented as SEC source crops.
The original marking criteria remain attached separately by the publisher.
"""
from decimal import Decimal
from io import BytesIO
from math import exp

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
