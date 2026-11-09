#!/usr/bin/env python3
"""Original 2016 question inputs and the complete source disease table."""
import fitz,hashlib,json
from he_review_2016_hl_main import ROOT,REVIEW,PAPER,SCHEME,documents,a_regions
ALTS={1:'Original protein table: Casein, Actin and Albumin, with all three blank food-source cells.',7:'Original labelled yeast diagram with A, B and C, every pointer, blank answer field and the original image attribution.',11:'Original upholstered-furniture question with both property answer spaces and the complete fire/flame-resistant label and companion question.'}
def write():
 d=documents();regions=a_regions(d['paper'],range(2,6));specs={}
 for n,alt in ALTS.items():
  r=regions[n]
  if n==1:r['rect'][3]=d['paper'][r['page']-1].find_tables().tables[0].bbox[3]+8
  specs[f'home-economics-2016-hl-sa-q{n}']=dict(kind='paper',source=PAPER,page=r['page'],bounds=r['rect'],alt=alt)
 tables=d['paper'][5].find_tables().tables;assert len(tables)==1
 specs['home-economics-2016-hl-sb-q1-fibre']=dict(kind='paper',source=PAPER,page=6,bounds=list(fitz.Rect(tables[0].bbox)+(-3,-3,3,3)),alt='Original fibre-intake table: all six food groups and total, both 18–64 and ≥65 age categories, percentages and gram values including 19.2 and 19.0 totals.')
 tables=d['scheme'][10].find_tables().tables;assert len(tables)==1
 specs['home-economics-2016-hl-sb-q1d-diseases']=dict(kind='scheme',source=SCHEME,page=11,bounds=list(fitz.Rect(tables[0].bbox)+(-3,-3,3,3)),alt='Complete original five-model bowel-disease table with all names, matching accounts and symptoms/effects; no table row or continuation is omitted.',solution=True)
 p=ROOT/'components/MarkBank/figures-home-economics.json';manifest=json.loads(p.read_text())
 for key,spec in specs.items():
  path=ROOT/f'public/exam-figures/home-economics/{key}.png';d[spec['kind']][spec['page']-1].get_pixmap(matrix=fitz.Matrix(2.5,2.5),clip=fitz.Rect(spec['bounds'])).save(path);sha=hashlib.sha256(path.read_bytes()).hexdigest();spec['sha256']=sha
  manifest[key]=dict(src=f'/exam-figures/home-economics/{key}.png',md5=hashlib.md5(path.read_bytes()).hexdigest(),alt=spec['alt'],attribution=f'SEC Home Economics 2016 Higher Level {"marking scheme" if spec["kind"]=="scheme" else "examination paper"}, page {spec["page"]} — © State Examinations Commission.',sourceNote=f'Original PDF crop, bounds {spec["bounds"]}, rendered at 2.5×. SHA256 {sha}.')
  if spec.get('solution'):manifest[key]['solution']=True
 p.write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n');p=ROOT/REVIEW;r=json.loads(p.read_text());r['figures']=specs;p.write_text(json.dumps(r,ensure_ascii=False,indent=2)+'\n')
if __name__=='__main__':write()
