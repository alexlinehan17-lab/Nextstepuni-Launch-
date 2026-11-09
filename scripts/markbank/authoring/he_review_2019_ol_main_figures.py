#!/usr/bin/env python3
"""Ten original question inputs; full vector chart, photographs and attribution lines."""
import fitz,hashlib,json
from he_review_2019_ol_main import ROOT,REVIEW,PAPER,documents,a_regions
ALTS={1:'Complete original three-statement water True/False table.',2:'Complete original vitamin cloze task and rhodopsin, rickets, ascorbic acid word pool.',5:'Complete original fruit-class table with two blank fruit fields EACH for citrus, dried and stone fruit.',7:'Complete original two-pastry and matching suitable-dish table.',8:'Complete original grilling, deep-frying and poaching True/False table.',9:'Complete original household-textile cloze task and shrink, static, proban word pool.',12:'Complete original universal recycling and European Union eco-label symbols and explanation question.'}
def write():
 d=documents();regions=a_regions(d['paper'],range(2,6));specs={}
 def add(key,page,rect,alt):specs['home-economics-2019-ol-'+key]=dict(kind='paper',source=PAPER,page=page,bounds=list(rect),alt=alt)
 for n,alt in ALTS.items():
  r=regions[n]
  if n in [1,5,7,8]:
   inside=[t for t in d['paper'][r['page']-1].find_tables().tables if r['rect'][1]<t.bbox[1] and t.bbox[3]<r['rect'][3]];assert len(inside)==1;r['rect'][3]=inside[0].bbox[3]+8
  add(f'sa-q{n}',r['page'],r['rect'],alt)
 def with_caption(page,rect,token):
  hits=page.search_for(token);assert len(hits)==1
  for block in page.get_text('dict')['blocks']:
   for line in block.get('lines',[]):
    if fitz.Rect(line['bbox']).intersects(hits[0]):rect|=fitz.Rect(line['bbox'])
  return rect+(-3,-3,3,3)
 p=d['paper'][5];boxes=[fitz.Rect(v['rect']) for v in p.get_drawings() if 150<v['rect'].y0<250 and v['rect'].height>100 and v['rect'].width>300];assert len(boxes)==2;rect=boxes[0]|boxes[1]
 add('sb-q1-bread',6,with_caption(p,rect,'Bord Bia'),'Complete original Types of Baked Goods Purchased Weekly chart: white sliced bread 71, French bread 45, soda/brown bread 43, wraps 37, rolls/buns/baps 26; all category labels, percentage legend and Bord Bia 2017 attribution.')
 for pn,key,token,alt in [(9,'sc-q1-house','cbaarchitecture','Complete original house photograph and cbaarchitecture.ie attribution.'),(10,'sc-q2-leisure','lidl','Complete original four runners and their leisurewear, with full Lidl attribution; used for both suitability and matching-jacket tasks.')]:
  p=d['paper'][pn-1];pictures=p.get_image_info();assert len(pictures)==1;add(key,pn,with_caption(p,fitz.Rect(pictures[0]['bbox']),token),alt)
 p=ROOT/'components/MarkBank/figures-home-economics.json';manifest=json.loads(p.read_text())
 for key,spec in specs.items():
  path=ROOT/f'public/exam-figures/home-economics/{key}.png';d['paper'][spec['page']-1].get_pixmap(matrix=fitz.Matrix(2.5,2.5),clip=fitz.Rect(spec['bounds'])).save(path);sha=hashlib.sha256(path.read_bytes()).hexdigest();spec['sha256']=sha
  manifest[key]=dict(src=f'/exam-figures/home-economics/{key}.png',md5=hashlib.md5(path.read_bytes()).hexdigest(),alt=spec['alt'],attribution=f'SEC Home Economics 2019 Ordinary Level examination paper, page {spec["page"]} — © State Examinations Commission.',sourceNote=f'Original PDF crop, bounds {spec["bounds"]}, rendered at 2.5×. SHA256 {sha}.')
 assert len(specs)==10;p.write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n');p=ROOT/REVIEW;r=json.loads(p.read_text());r['figures']=specs;p.write_text(json.dumps(r,ensure_ascii=False,indent=2)+'\n')
if __name__=='__main__':write()
