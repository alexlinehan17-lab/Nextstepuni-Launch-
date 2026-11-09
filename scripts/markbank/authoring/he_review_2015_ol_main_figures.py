#!/usr/bin/env python3
"""Six original question crops, preserving tables, choice pools and companion prompts."""
import fitz,hashlib,json
from he_review_2015_ol_main import ROOT,REVIEW,PAPER,SCHEME,documents,a_regions
ALTS={1:'Original calcium true/false table with all three complete statements and blank True/False columns.',6:'Original food-spoilage true/false table with all three complete statements and blank True/False columns.',7:'Original cheese matching question: all three supplied choices and complete Hard/Soft/Processed cheese blank rows.'}
def write():
 d=documents();regions=a_regions(d['paper'],range(2,6));specs={}
 for n,alt in ALTS.items():
  r=regions[n];tables=d['paper'][r['page']-1].find_tables().tables;inside=[t for t in tables if r['rect'][1]<t.bbox[1] and t.bbox[3]<r['rect'][3]];assert len(inside)==1;r['rect'][3]=inside[0].bbox[3]+8
  specs[f'home-economics-2015-ol-sa-q{n}']=dict(kind='paper',source=PAPER,page=r['page'],bounds=r['rect'],alt=alt)
 for page,key,alt in [(6,'sb-q1-meats','Original four-meat nutritional table: Beef, Chicken, Liver and Pork, all five nutrient columns, every value and original unit.'),(11,'sc-q3-school','Original school-leaver table: every year group and count1,500/1,777/1,064/3,299 from2009/2010, preserving the chart input.')]:
  tables=d['paper'][page-1].find_tables().tables;assert len(tables)==1
  specs['home-economics-2015-ol-'+key]=dict(kind='paper',source=PAPER,page=page,bounds=list(fitz.Rect(tables[0].bbox)+(-3,-3,3,3)),alt=alt)
 pictures=d['paper'][8].get_image_info();assert len(pictures)==1,pictures
 specs['home-economics-2015-ol-sc-q1-plan']=dict(kind='paper',source=PAPER,page=9,bounds=list(fitz.Rect(pictures[0]['bbox'])+(-3,-3,3,3)),alt='Complete original floor plan for Sean and Julie: all four bedrooms, bathroom, ensuite, WC, kitchen/dining, utility, garage and lounge, with every door/wall and original label.')
 p=ROOT/'components/MarkBank/figures-home-economics.json';manifest=json.loads(p.read_text())
 for key,spec in specs.items():
  path=ROOT/f'public/exam-figures/home-economics/{key}.png';d[spec['kind']][spec['page']-1].get_pixmap(matrix=fitz.Matrix(2.5,2.5),clip=fitz.Rect(spec['bounds'])).save(path);sha=hashlib.sha256(path.read_bytes()).hexdigest();spec['sha256']=sha
  manifest[key]=dict(src=f'/exam-figures/home-economics/{key}.png',md5=hashlib.md5(path.read_bytes()).hexdigest(),alt=spec['alt'],attribution=f'SEC Home Economics 2015 Ordinary Level {"marking scheme" if spec["kind"]=="scheme" else "examination paper"}, page {spec["page"]} — © State Examinations Commission.',sourceNote=f'Original PDF crop, bounds {spec["bounds"]}, rendered at 2.5×. SHA256 {sha}.')
  if spec.get('solution'):manifest[key]['solution']=True
 p.write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n');p=ROOT/REVIEW;r=json.loads(p.read_text());r['figures']=specs;p.write_text(json.dumps(r,ensure_ascii=False,indent=2)+'\n')
if __name__=='__main__':write()
