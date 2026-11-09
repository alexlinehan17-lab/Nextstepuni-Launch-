#!/usr/bin/env python3
"""Eleven complete original question figures for the independently reviewed sitting."""
import fitz,hashlib,json
from he_review_2017_ol_main import ROOT,REVIEW,PAPER,documents,a_regions
ALTS={1:'Original lipid true/false question with all three statements and blank True/False columns.',3:'Original protein table with Eggs, Peas and Fish and blank High Biological Value/Low Biological Value columns.',6:'Original cooking-method table with Grilling, Steaming and Roasting and both blank example columns.',7:'Complete original cereal cloze, with all three blank sentences and the bran, endosperm, staple word bank.',8:'Original food-additives true/false question with all three statements and blank True/False columns.',11:'Complete original historical refrigerator energy label, including A–G bands, rating A, annual 325 kWh, storage volumes, noise field and attribution, with the original question and answer space.',12:'Original pollution table with Air pollution, Water pollution and Noise pollution and all blank example fields.'}
def write():
 d=documents();regions=a_regions(d['paper'],range(2,6));specs={}
 for n,alt in ALTS.items():
  r=regions[n]
  if n in [1,3,6,8,12]:
   tables=d['paper'][r['page']-1].find_tables().tables;inside=[t for t in tables if r['rect'][1]<t.bbox[1] and t.bbox[3]<r['rect'][3]];assert len(inside)==1;r['rect'][3]=inside[0].bbox[3]+8
  specs[f'home-economics-2017-ol-sa-q{n}']=dict(kind='paper',source=PAPER,page=r['page'],bounds=r['rect'],alt=alt)
 p=d['paper'][5];frames=[fitz.Rect(v['rect']) for v in p.get_drawings() if v['rect'].width>350 and v['rect'].height>150];assert frames;frame=max(frames,key=lambda r:r.width*r.height);assert 120<frame.y0<frame.y1<500
 specs['home-economics-2017-ol-sb-q1-chart']=dict(kind='paper',source=PAPER,page=6,bounds=list(frame+(-3,-3,3,3)),alt='Complete original fruit-and-vegetable consumption chart: all three age groups 15–34, 35–54 and 55+, both men/women bars, full legend, percent axis and title.')
 tables=d['paper'][6].find_tables().tables;menu=tables[0];assert 100<menu.bbox[1]<110 and 310<menu.bbox[3]<320
 specs['home-economics-2017-ol-sb-q2-menu']=dict(kind='paper',source=PAPER,page=7,bounds=list(fitz.Rect(menu.bbox)+(-3,-3,3,3)),alt='Complete original Paul and Lisa school-day menu: breakfast, morning break, lunch and dinner, retaining every food and drink.')
 for pn,key,count,alt in [(9,'sc-q1-housing',3,'All three original housing-style images in full, with their original source attributions.'),(10,'sc-q2-outfits',2,'Both original Debs outfits, suit and dress, shown completely with both original source attributions.')]:
  p=d['paper'][pn-1];pictures=p.get_image_info();assert len(pictures)==count;rect=fitz.Rect(pictures[0]['bbox'])
  for picture in pictures[1:]:rect|=fitz.Rect(picture['bbox'])
  captions=[w for w in p.get_text('words') if w[4].startswith('(www.') and rect.y1<=w[1]<rect.y1+25];assert len(captions)==count,captions
  for word in captions:rect|=fitz.Rect(word[:4])
  specs['home-economics-2017-ol-'+key]=dict(kind='paper',source=PAPER,page=pn,bounds=list(rect+(-4,-3,4,3)),alt=alt)
 p=ROOT/'components/MarkBank/figures-home-economics.json';manifest=json.loads(p.read_text())
 for key,spec in specs.items():
  path=ROOT/f'public/exam-figures/home-economics/{key}.png';d[spec['kind']][spec['page']-1].get_pixmap(matrix=fitz.Matrix(2.5,2.5),clip=fitz.Rect(spec['bounds'])).save(path);sha=hashlib.sha256(path.read_bytes()).hexdigest();spec['sha256']=sha
  manifest[key]=dict(src=f'/exam-figures/home-economics/{key}.png',md5=hashlib.md5(path.read_bytes()).hexdigest(),alt=spec['alt'],attribution=f'SEC Home Economics 2017 Ordinary Level examination paper, page {spec["page"]} — © State Examinations Commission.',sourceNote=f'Original PDF crop, bounds {spec["bounds"]}, rendered at 2.5×. SHA256 {sha}.')
 p.write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n');p=ROOT/REVIEW;r=json.loads(p.read_text());r['figures']=specs;p.write_text(json.dumps(r,ensure_ascii=False,indent=2)+'\n')
 print('Rendered 11 original question figures.')
if __name__=='__main__':write()
