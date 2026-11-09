#!/usr/bin/env python3
"""Seven complete original question inputs, with all companion asks intact."""
import fitz,hashlib,json
from he_review_2018_hl_main import ROOT,REVIEW,PAPER,SCHEME,documents,a_regions
ALTS={1:'Complete original Organ, Enzyme, Substrate and Product table with required Pancreas and Small Intestine blank rows.',5:'Complete original gluten-free symbol and question, including the request for two labelled products.',6:'Complete original processed-food table with all three category headings and blank Food/Product fields.',8:'Complete original optimum-growth temperature table with Psychrophiles, Mesophiles and Thermophiles.',9:'Complete original two-textile/property table and companion fire-retardant finish question.'}
def write():
 d=documents();regions=a_regions(d['paper'],range(2,6));specs={}
 def add(key,kind,page,rect,alt):
  specs['home-economics-2018-hl-'+key]=dict(kind=kind,source=PAPER if kind=='paper' else SCHEME,page=page,bounds=list(rect),alt=alt)
 for n,alt in ALTS.items():
  r=regions[n]
  if n in [1,6,8]:
   tables=d['paper'][r['page']-1].find_tables().tables;inside=[t for t in tables if r['rect'][1]<t.bbox[1] and t.bbox[3]<r['rect'][3]];assert len(inside)==1;r['rect'][3]=inside[0].bbox[3]+8
  add(f'sa-q{n}','paper',r['page'],r['rect'],alt)
 p=d['paper'][5];tables=p.find_tables().tables;assert len(tables)==1;rect=fitz.Rect(tables[0].bbox);title=p.search_for('Sample Main Course Menu');assert len(title)==1;rect|=title[0]
 add('sb-q1-menu','paper',6,rect+(-3,-3,3,3),'Complete original six-dish Sample Main Course Menu, all ingredients, accompaniments and calorie totals.')
 p=d['paper'][9];pictures=p.get_image_info();assert len(pictures)==1;rect=fitz.Rect(pictures[0]['bbox']);caption=p.search_for('(Adored Vintage: Runway Report/Sonia Rykiel)');assert len(caption)==1;rect|=caption[0]
 add('sc-q2-outfits','paper',10,rect+(-3,-1,3,1),'Complete original four outfits and Adored Vintage: Runway Report/Sonia Rykiel attribution.')
 p=ROOT/'components/MarkBank/figures-home-economics.json';manifest=json.loads(p.read_text())
 for key,spec in specs.items():
  path=ROOT/f'public/exam-figures/home-economics/{key}.png';d[spec['kind']][spec['page']-1].get_pixmap(matrix=fitz.Matrix(2.5,2.5),clip=fitz.Rect(spec['bounds'])).save(path);sha=hashlib.sha256(path.read_bytes()).hexdigest();spec['sha256']=sha
  manifest[key]=dict(src=f'/exam-figures/home-economics/{key}.png',md5=hashlib.md5(path.read_bytes()).hexdigest(),alt=spec['alt'],attribution=f'SEC Home Economics 2018 Higher Level {"marking scheme" if spec["kind"]=="scheme" else "examination paper"}, page {spec["page"]} — © State Examinations Commission.',sourceNote=f'Original PDF crop, bounds {spec["bounds"]}, rendered at 2.5×. SHA256 {sha}.')
  if spec.get('solution'):manifest[key]['solution']=True
 assert len(specs)==7
 p.write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n');p=ROOT/REVIEW;r=json.loads(p.read_text());r['figures']=specs;p.write_text(json.dumps(r,ensure_ascii=False,indent=2)+'\n')
if __name__=='__main__':write()
