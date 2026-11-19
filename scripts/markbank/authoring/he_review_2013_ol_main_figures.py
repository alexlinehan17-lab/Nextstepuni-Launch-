#!/usr/bin/env python3
"""Eight original question figure groups with complete input labels and captions."""
import fitz,hashlib,json
from he_review_2013_ol_main import ROOT,REVIEW,PAPER,SCHEME,documents,a_regions
ALTS={1:'Original fat-classification question with the complete avocado, sardines, cheese choice pool and blank Animal, Vegetable (Plant), Marine table.',3:'Original coronary-heart-disease true/false question table, all three full statements and blank True/False columns.',4:'Original cooking-method question table with Moist cooking methods, Dry cooking methods and Frying columns, two blank example rows for each.',6:'Original soup true/false question table, all three full statements and blank True/False columns.',8:'Original complete textile-care symbols: hand in wash tub and crossed-out tumble-dryer symbol, both with full blank response spaces.',11:'Original electrical-appliance safety-feature and example-of-use table, full prompt and both blank paired rows.'}
def write():
 d=documents();regions=a_regions(d['paper'],range(2,6));specs={}
 for n,alt in ALTS.items():
  r=regions[n];specs[f'home-economics-2013-ol-sa-q{n}']=dict(kind='paper',source=PAPER,page=r['page'],bounds=r['rect'],alt=alt)
 specs['home-economics-2013-ol-sb-q1-pyramid']=dict(kind='paper',source=PAPER,page=6,bounds=[82,110,548,427],alt='Original complete food pyramid illustration and its Food Safety Authority, 2012 caption. Every pictured food and shelf, top and base, retained from the original examination paper.')
 specs['home-economics-2013-ol-sc-q1-heat-loss']=dict(kind='paper',source=PAPER,page=9,bounds=[198,179,405,384],alt='Original house heat-loss diagram. Complete house and arrows, roof25%, windows15%, walls35%, doors10%, floors15%, and Average heat loss from a house caption retained.')
 p=ROOT/'components/MarkBank/figures-home-economics.json';manifest=json.loads(p.read_text())
 for key,spec in specs.items():
  path=ROOT/f'public/exam-figures/home-economics/{key}.png';d[spec['kind']][spec['page']-1].get_pixmap(matrix=fitz.Matrix(2.5,2.5),clip=fitz.Rect(spec['bounds'])).save(path);sha=hashlib.sha256(path.read_bytes()).hexdigest();spec['sha256']=sha
  manifest[key]=dict(src=f'/exam-figures/home-economics/{key}.png',md5=hashlib.md5(path.read_bytes()).hexdigest(),alt=spec['alt'],attribution=f'SEC Home Economics 2013 Ordinary Level {"marking scheme" if spec["kind"]=="scheme" else "examination paper"}, page {spec["page"]} — © State Examinations Commission.',sourceNote=f'Original PDF crop, bounds {spec["bounds"]}, rendered at 2.5×. SHA256 {sha}.')
  if spec.get('solution'):manifest[key]['solution']=True
 p.write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n');p=ROOT/REVIEW;r=json.loads(p.read_text());r['figures']=specs;p.write_text(json.dumps(r,ensure_ascii=False,indent=2)+'\n')
if __name__=='__main__':write()
