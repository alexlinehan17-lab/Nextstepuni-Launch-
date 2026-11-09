#!/usr/bin/env python3
"""Ten original question inputs plus the complete three-meal source model."""
import fitz,hashlib,json
from he_review_2016_ol_main import ROOT,REVIEW,PAPER,SCHEME,documents,a_regions
ALTS={1:'Original protein true/false question with all three statements and blank True/False columns.',2:'Original carbohydrate source table with Sugar, Starch and Fibre and all blank dietary-source fields.',6:'Complete original cheese cloze with every blank and the full curds, lactic acid, rennin word bank.',7:'Original freezing true/false question with all three statements, temperature and blank True/False columns.',8:'Original vegetable table with Pulse, Root and Green categories and both blank example columns.',10:'Both original fabric-care symbols, hand-wash and do-not-bleach, with the full question and blank response spaces.',11:'Original appliance table with Kettle, Food processor and Toaster, and blank Element/Motor columns.'}
def write():
 d=documents();regions=a_regions(d['paper'],range(2,6));specs={}
 for n,alt in ALTS.items():
  r=regions[n]
  if n in [1,2,7,8,11]:
   tables=d['paper'][r['page']-1].find_tables().tables;inside=[t for t in tables if r['rect'][1]<t.bbox[1] and t.bbox[3]<r['rect'][3]];assert len(inside)==1;r['rect'][3]=inside[0].bbox[3]+8
  specs[f'home-economics-2016-ol-sa-q{n}']=dict(kind='paper',source=PAPER,page=r['page'],bounds=r['rect'],alt=alt)
 tables=d['paper'][5].find_tables().tables;assert len(tables)==1
 specs['home-economics-2016-ol-sb-q1-meals']=dict(kind='paper',source=PAPER,page=6,bounds=list(fitz.Rect(tables[0].bbox)+(-3,-3,3,3)),alt='Complete original comparison of Fisherman’s pie and Chicken curry with rice: all ingredients, energy and five nutrient values per serving, with original units.')
 for pn,key,caption,alt in [(9,'sc-q1-kitchen','(www.buzhomedesign.com)','Complete original kitchen layout with all visible appliances, storage, worktops, windows and original source attribution.'),(10,'sc-q2-suits','(www. pinterest.com)','Both original office-suit examples, male and female, in full with the original image attribution.')]:
  p=d['paper'][pn-1];pictures=p.get_image_info();assert len(pictures)==1,pictures;rect=fitz.Rect(pictures[0]['bbox']);matches=p.search_for(caption);assert len(matches)==1;rect|=matches[0]
  specs['home-economics-2016-ol-'+key]=dict(kind='paper',source=PAPER,page=pn,bounds=list(rect+(-3,-3,3,0)),alt=alt)
 # The three-meal frame uses filled thin rectangles rather than table
 # strokes; find_tables sees none. All22 original drawing pieces form it.
 drawings=d['scheme'][9].get_drawings();assert len(drawings)==22;rect=fitz.Rect(drawings[0]['rect'])
 for drawing in drawings[1:]:rect|=drawing['rect']
 assert [round(v,2) for v in rect]==[198.17,394.15,404.23,615.94]
 specs['home-economics-2016-ol-sb-q2b-menu']=dict(kind='scheme',source=SCHEME,page=10,bounds=list(rect+(-3,-3,3,3)),alt='Complete original breakfast, lunch and dinner model including every food/drink and the printed Egg Mayonnaise anomaly in the lacto-vegetarian menu.',solution=True)
 p=ROOT/'components/MarkBank/figures-home-economics.json';manifest=json.loads(p.read_text())
 for key,spec in specs.items():
  path=ROOT/f'public/exam-figures/home-economics/{key}.png';d[spec['kind']][spec['page']-1].get_pixmap(matrix=fitz.Matrix(2.5,2.5),clip=fitz.Rect(spec['bounds'])).save(path);sha=hashlib.sha256(path.read_bytes()).hexdigest();spec['sha256']=sha
  manifest[key]=dict(src=f'/exam-figures/home-economics/{key}.png',md5=hashlib.md5(path.read_bytes()).hexdigest(),alt=spec['alt'],attribution=f'SEC Home Economics 2016 Ordinary Level {"marking scheme" if spec["kind"]=="scheme" else "examination paper"}, page {spec["page"]} — © State Examinations Commission.',sourceNote=f'Original PDF crop, bounds {spec["bounds"]}, rendered at 2.5×. SHA256 {sha}.')
  if spec.get('solution'):manifest[key]['solution']=True
 p.write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n');p=ROOT/REVIEW;r=json.loads(p.read_text());r['figures']=specs;p.write_text(json.dumps(r,ensure_ascii=False,indent=2)+'\n')
if __name__=='__main__':write()
