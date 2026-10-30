"""Clearly attributed NextStepUni examples for omissions in printed SEC solutions.

These are derived teaching diagrams, never represented as SEC source crops.
The original marking criteria remain attached separately by the publisher.
"""
from decimal import Decimal
from io import BytesIO

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
