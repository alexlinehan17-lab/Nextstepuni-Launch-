#!/usr/bin/env python3
"""Five complete original question tables with their printed labels and caption."""
import fitz,hashlib,json
from he_review_2013_hl_main import ROOT,REVIEW,PAPER,SCHEME,documents,a_regions
ALTS={1:'Original protein-function question table with all three protein types and blank function cells.',3:'Original six-row vitamin-deficiency question table: Nightblindness, Rickets, Poor blood clotting, Anaemia, Beri-beri, Neural tube defects; all blank vitamin cells retained.',4:'Original flour and culinary-use table, complete headings and three paired blank rows.',6:'Original food-contamination table with Pesticides and Metal residues, How contamination occurs and Possible effect on the body headings; all blank cells retained.'}
def write():
 d=documents();regions=a_regions(d['paper'],range(2,6));specs={}
 for n,alt in ALTS.items():
  r=regions[n];specs[f'home-economics-2013-hl-sa-q{n}']=dict(kind='paper',source=PAPER,page=r['page'],bounds=r['rect'],alt=alt)
 specs['home-economics-2013-hl-sb-q1-pyramid']=dict(kind='paper',source=PAPER,page=6,bounds=[81,175,541,468],alt='Original five-shelf Food Pyramid daily-servings table with complete SLAN 2007 source caption. 1998/2007 percentages: cereals/breads/potatoes40/26; fruit/vegetables56/65; milk/cheese/yoghurt22/20; meat/fish/poultry/alternatives36/39; top shelf fats/sugar/salt14/14. All original shelf names and daily-serving limits retained.')
 p=ROOT/'components/MarkBank/figures-home-economics.json';manifest=json.loads(p.read_text())
 for key,spec in specs.items():
  path=ROOT/f'public/exam-figures/home-economics/{key}.png';d[spec['kind']][spec['page']-1].get_pixmap(matrix=fitz.Matrix(2.5,2.5),clip=fitz.Rect(spec['bounds'])).save(path);sha=hashlib.sha256(path.read_bytes()).hexdigest();spec['sha256']=sha
  manifest[key]=dict(src=f'/exam-figures/home-economics/{key}.png',md5=hashlib.md5(path.read_bytes()).hexdigest(),alt=spec['alt'],attribution=f'SEC Home Economics 2013 Higher Level {"marking scheme" if spec["kind"]=="scheme" else "examination paper"}, page {spec["page"]} — © State Examinations Commission.',sourceNote=f'Original PDF crop, bounds {spec["bounds"]}, rendered at 2.5×. SHA256 {sha}.')
  if spec.get('solution'):manifest[key]['solution']=True
 p.write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n');p=ROOT/REVIEW;r=json.loads(p.read_text());r['figures']=specs;p.write_text(json.dumps(r,ensure_ascii=False,indent=2)+'\n')
if __name__=='__main__':write()
