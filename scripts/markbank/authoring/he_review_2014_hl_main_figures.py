#!/usr/bin/env python3
"""Seven original crops, preserving question data and image-only source allowance."""
import fitz,hashlib,json
from he_review_2014_hl_main import ROOT,REVIEW,PAPER,SCHEME,documents,a_regions
ALTS={2:'Original lipid-digestion question table, complete Small Intestine row and blank Secretion, Enzyme and Product cells.',6:'Original cheese-classification question table with three blank classification/example pairs and the complete prompt.',8:'Original micro-organism/use question table: Lactic acid bacteria, Lactobacillus bulgaricus and Yeast; all blank use cells retained.'}
def write():
 d=documents();regions=a_regions(d['paper'],range(2,6));specs={}
 for n,alt in ALTS.items():
  r=regions[n];specs[f'home-economics-2014-hl-sa-q{n}']=dict(kind='paper',source=PAPER,page=r['page'],bounds=r['rect'],alt=alt)
 tables=d['paper'][5].find_tables().tables;assert len(tables)==1
 rect=fitz.Rect(tables[0].bbox)+(-3,-3,3,3)
 specs['home-economics-2014-hl-sb-q1-costs']=dict(kind='paper',source=PAPER,page=6,bounds=list(rect),alt='Original four-household, three-outlet food-cost table: every household description, euro value, percentage and daily calorie requirement retained; complete multiple-supermarket, low-cost-shop and local-shop headings.')
 pictures=d['paper'][9].get_image_info();assert len(pictures)==1,pictures
 rect=fitz.Rect(pictures[0]['bbox'])+(-2,-2,2,2)
 specs['home-economics-2014-hl-sc-q2-dress']=dict(kind='paper',source=PAPER,page=10,bounds=list(rect),alt='Complete original examination photograph for the Imelda May dress-design question, including the striped dress, belt, arms and shoes; full original frame retained.')
 rect=fitz.Rect(d['scheme'][8].find_tables().tables[0].bbox)+(-3,-3,3,3)
 specs['home-economics-2014-hl-sb-q1d-protein']=dict(kind='scheme',source=SCHEME,page=9,bounds=list(rect),alt='Original complete protein-classification answer table, preserving merged Simple/Animal/Plant and Conjugated groups, subgroups, all examples and aligned food sources.',solution=True)
 pictures=d['scheme'][18].get_image_info();assert len(pictures)==1
 rect=fitz.Rect(pictures[0]['bbox'])
 specs['home-economics-2014-hl-sc-q1aii-allowance']=dict(kind='scheme',source=SCHEME,page=19,bounds=list(rect),alt='Original image-only marking note: Due to an inconsistency between the English and Irish versions of the examination paper, non-renewable sources of energy were also accepted.',solution=True)
 p=ROOT/'components/MarkBank/figures-home-economics.json';manifest=json.loads(p.read_text())
 for key,spec in specs.items():
  path=ROOT/f'public/exam-figures/home-economics/{key}.png';d[spec['kind']][spec['page']-1].get_pixmap(matrix=fitz.Matrix(2.5,2.5),clip=fitz.Rect(spec['bounds'])).save(path);sha=hashlib.sha256(path.read_bytes()).hexdigest();spec['sha256']=sha
  manifest[key]=dict(src=f'/exam-figures/home-economics/{key}.png',md5=hashlib.md5(path.read_bytes()).hexdigest(),alt=spec['alt'],attribution=f'SEC Home Economics 2014 Higher Level {"marking scheme" if spec["kind"]=="scheme" else "examination paper"}, page {spec["page"]} — © State Examinations Commission.',sourceNote=f'Original PDF crop, bounds {spec["bounds"]}, rendered at 2.5×. SHA256 {sha}.')
  if spec.get('solution'):manifest[key]['solution']=True
 p.write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n');p=ROOT/REVIEW;r=json.loads(p.read_text());r['figures']=specs;p.write_text(json.dumps(r,ensure_ascii=False,indent=2)+'\n')
if __name__=='__main__':write()
