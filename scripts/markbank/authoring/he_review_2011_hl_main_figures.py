#!/usr/bin/env python3
"""Original question tables, two symbols and complete four-product chart; no redrawing."""
import fitz,hashlib,json
from he_review_2011_hl_main import ROOT,REVIEW,PAPER,documents,a_regions
ALTS={1:'Original carbohydrate question and blank table: Classification, Example, Food Source. Rows: Monosaccharides, Disaccharides, Polysaccharides.',4:'Original protein question and blank table: Food / Type of Protein, with Fish, Eggs and Wheat in the food column.',6:'Original food-additives question and blank antioxidant table: Example, Function, Example of use.',12:'Original consumer-symbol question with the CE marking and the double-square insulation symbol, both numbered labels and answer spaces retained.'}

def write():
 d=documents();regions=a_regions(d['paper'],range(2,6));specs={}
 for n,alt in ALTS.items():
  r=regions[n]
  if n==12:r['rect'][3]=300
  specs[f'home-economics-2011-hl-sa-q{n}']=dict(source=PAPER,page=r['page'],bounds=r['rect'],alt=alt)
 specs['home-economics-2011-hl-sb-q1-dairy']=dict(source=PAPER,page=6,bounds=[90,185,530,458],alt='Original bar chart: Retail Dairy Market in Republic of Ireland 2009. Milk 39%, Yogurts 26%, Cheese 18%, Cream and fats 17%. Complete four bars, percentage axis, product labels, title, legend and NDC source caption retained. The paper excludes independent/doorstep sales.')
 p=ROOT/'components/MarkBank/figures-home-economics.json';manifest=json.loads(p.read_text())
 for key,spec in specs.items():
  path=ROOT/f'public/exam-figures/home-economics/{key}.png';d['paper'][spec['page']-1].get_pixmap(matrix=fitz.Matrix(2,2),clip=fitz.Rect(spec['bounds'])).save(path);sha=hashlib.sha256(path.read_bytes()).hexdigest();spec['sha256']=sha
  manifest[key]=dict(src=f'/exam-figures/home-economics/{key}.png',md5=hashlib.md5(path.read_bytes()).hexdigest(),alt=spec['alt'],attribution=f'SEC Home Economics 2011 Higher Level examination paper, page {spec["page"]} — © State Examinations Commission.',sourceNote=f'Original PDF crop, bounds {spec["bounds"]}, rendered at 2×. SHA256 {sha}.')
 p.write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n');p=ROOT/REVIEW;r=json.loads(p.read_text());r['figures']=specs;p.write_text(json.dumps(r,ensure_ascii=False,indent=2)+'\n')
if __name__=='__main__':write()
