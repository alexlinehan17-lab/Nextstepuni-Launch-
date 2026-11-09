#!/usr/bin/env python3
"""Eight original question crops, preserving tables, choice pools and companion prompts."""
import fitz,hashlib,json
from he_review_2014_ol_main import ROOT,REVIEW,PAPER,SCHEME,documents,a_regions
ALTS={1:'Original fats true/false table, all three full statements and blank True/False columns.',2:'Original two-row vitamin-classification and example table, complete question and paired blank cells.',4:'Original diet/health true/false table, all three full statements and blank True/False columns.',5:'Original cheese nutrient tick table, all Protein/Vitamin C/Calcium choices and the complete companion cooking-effects question.',9:'Original microwave part/function matching question, complete wave guide/turntable/magnetron choice pool and all three function rows.',11:'Original natural/synthetic fibre table and complete companion question asking why natural fibres are used in household textiles.'}
def write():
 d=documents();regions=a_regions(d['paper'],range(2,6));specs={}
 for n,alt in ALTS.items():
  r=regions[n];specs[f'home-economics-2014-ol-sa-q{n}']=dict(kind='paper',source=PAPER,page=r['page'],bounds=r['rect'],alt=alt)
 tables=d['paper'][5].find_tables().tables;assert len(tables)==1
 rect=fitz.Rect(tables[0].bbox)+(-3,-3,3,3)
 specs['home-economics-2014-ol-sb-q1-nutrients']=dict(kind='paper',source=PAPER,page=6,bounds=list(rect),alt='Original three-dish carbohydrate/protein/fat table: Beef Lasagne11.8g/8.1g/8.9g; Sweet & Sour Chicken & Rice20.0g/6.8g/0.4g; Cheese Burger27.1g/14.2g/3.2g. All original headings, dish names and units retained; FSAI attribution remains in the source stem.')
 pictures=d['paper'][8].get_image_info();assert len(pictures)==2,pictures
 rect=fitz.Rect(pictures[0]['bbox'])|fitz.Rect(pictures[1]['bbox'])
 captions=[b for b in d['paper'][8].get_text('blocks') if 'Meter Box' in b[4] and 'Miniature Circuit Breakers' in b[4]];assert len(captions)==1
 rect=rect|fitz.Rect(captions[0][:4]);rect=rect+(-3,-3,3,3)
 specs['home-economics-2014-ol-sc-q1-electricity']=dict(kind='paper',source=PAPER,page=9,bounds=list(rect),alt='Both original electricity-supply pictures, complete Meter Box and Miniature Circuit Breakers, with their original captions.')
 p=ROOT/'components/MarkBank/figures-home-economics.json';manifest=json.loads(p.read_text())
 for key,spec in specs.items():
  path=ROOT/f'public/exam-figures/home-economics/{key}.png';d[spec['kind']][spec['page']-1].get_pixmap(matrix=fitz.Matrix(2.5,2.5),clip=fitz.Rect(spec['bounds'])).save(path);sha=hashlib.sha256(path.read_bytes()).hexdigest();spec['sha256']=sha
  manifest[key]=dict(src=f'/exam-figures/home-economics/{key}.png',md5=hashlib.md5(path.read_bytes()).hexdigest(),alt=spec['alt'],attribution=f'SEC Home Economics 2014 Ordinary Level {"marking scheme" if spec["kind"]=="scheme" else "examination paper"}, page {spec["page"]} — © State Examinations Commission.',sourceNote=f'Original PDF crop, bounds {spec["bounds"]}, rendered at 2.5×. SHA256 {sha}.')
  if spec.get('solution'):manifest[key]['solution']=True
 p.write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n');p=ROOT/REVIEW;r=json.loads(p.read_text());r['figures']=specs;p.write_text(json.dumps(r,ensure_ascii=False,indent=2)+'\n')
if __name__=='__main__':write()
