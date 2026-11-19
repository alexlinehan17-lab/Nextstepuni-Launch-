#!/usr/bin/env python3
"""Five original question figures plus the original carbohydrate answer diagrams."""
import fitz,hashlib,json
from he_review_2012_hl_main import ROOT,REVIEW,PAPER,SCHEME,documents,a_regions
ALTS={5:'Original alternative (novel) protein question table. Plant and Micro-organisms rows, Source and Product columns; all blank input cells retained.',6:'Original heat-transfer question table. Complete Method of Heat Transfer and Cooking Method columns, three blank rows and the printed paired-response prompt.',8:'Original mould diagram and question. All labelled A, B and C pointers, intact spore structures and hyphal network retained; blank answer spaces remain.'}
def write():
 d=documents();regions=a_regions(d['paper'],range(2,6));specs={}
 for n,alt in ALTS.items():
  r=regions[n];specs[f'home-economics-2012-hl-sa-q{n}']=dict(kind='paper',source=PAPER,page=r['page'],bounds=r['rect'],alt=alt)
 specs['home-economics-2012-hl-sb-q1-servings']=dict(kind='paper',source=PAPER,page=6,bounds=[82,234,557,401],alt='Original daily food-group servings table. Age groups 5–13, 14–18, 19–50 and 51+, each Male/Female. Bread/Cereals moderately active: 3–5/3–4, 5–7/4, 5–7/4–5, 4–5/3–4; sedentary: 3–5/3–4, 4–5/3, 4–6/3–4, 4/3. Fruit & Vegetables: 5/5, 5–6/5, 5–7/5–6, 5/5. All original headings, gender/activity labels and cells retained.')
 specs['home-economics-2012-hl-sc-q3-unemployment']=dict(kind='paper',source=PAPER,page=11,bounds=[103,165,546,257],alt='Original unemployment table for Ireland, with full Central Statistics Office caption. Years 2006, 2007, 2008, 2009, 2010, 2011: 4.4%, 4.5%, 6.4%, 11.8%, 13.7%, 14.2%. The original PAPER value for 2010 is 13.7%; scheme repeats 13.6%.')
 specs['home-economics-2012-hl-sb-q1b-carbohydrates']=dict(kind='scheme',source=SCHEME,page=8,bounds=[76,106,575,404],alt='Original carbohydrate answer models: labelled glucose chemical structure, disaccharide formation equation and ring diagram with water eliminated, plus hydrolysis and inversion explanation. Complete source diagrams, symbols and printed eight-mark allocations retained.',solution=True)
 p=ROOT/'components/MarkBank/figures-home-economics.json';manifest=json.loads(p.read_text())
 for key,spec in specs.items():
  path=ROOT/f'public/exam-figures/home-economics/{key}.png';d[spec['kind']][spec['page']-1].get_pixmap(matrix=fitz.Matrix(2.5,2.5),clip=fitz.Rect(spec['bounds'])).save(path);sha=hashlib.sha256(path.read_bytes()).hexdigest();spec['sha256']=sha
  manifest[key]=dict(src=f'/exam-figures/home-economics/{key}.png',md5=hashlib.md5(path.read_bytes()).hexdigest(),alt=spec['alt'],attribution=f'SEC Home Economics 2012 Higher Level {"marking scheme" if spec["kind"]=="scheme" else "examination paper"}, page {spec["page"]} — © State Examinations Commission.',sourceNote=f'Original PDF crop, bounds {spec["bounds"]}, rendered at 2.5×. SHA256 {sha}.')
  if spec.get('solution'):manifest[key]['solution']=True
 p.write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n');p=ROOT/REVIEW;r=json.loads(p.read_text());r['figures']=specs;p.write_text(json.dumps(r,ensure_ascii=False,indent=2)+'\n')
if __name__=='__main__':write()
