#!/usr/bin/env python3
"""Eight original 2010 Ordinary input figures; preserve complete source content."""
import fitz,hashlib,json
from he_review_2010_ol_main import ROOT,REVIEW,PAPER,documents,a_regions
ALTS={2:'Original carbohydrate cloze question with word bank: liver, energy, cellulose. All three sentences and answer blanks retained.',4:'Original vitamin true/false table with all three statements and empty answer columns. Statements concern night blindness and vitamin A, vitamin C and iron absorption, and whether vitamin B is fat-soluble.',7:'Original three-row flour and culinary-use table. Each row asks for a type of flour and one different matching culinary use.',8:'Original food-additive matching table. Given options: herbs and spices, vitamin E, turmeric. Given classes: Colourings, Flavourings, Antioxidants; answer cells blank.'}
def write():
 d=documents();regions=a_regions(d['paper'],range(2,6));specs={}
 for n,alt in ALTS.items():
  r=regions[n];specs[f'home-economics-2010-ol-sa-q{n}']=dict(source=PAPER,page=r['page'],bounds=r['rect'],alt=alt)
 for key,page,bounds,alt in [
  ('sa-q9-symbol',4,[98,390,201,498],'Original household-cleaning hazard symbol: a bold black diagonal cross inside a square; the identification and explanation are left to the student.'),
  ('sb-q1-milk',6,[45,180,550,462],'Original nutritional information per 100g: Whole Milk / Semi-skimmed Milk. Energy kcal 66 / 46; Protein (g) 3.3 / 3.5; Carbohydrates (g) 4.6 / 4.7; Fat (g) 3.9 / 1.7; Saturated fatty acids (g) 2.5 / 1.1; Calcium 118 / 120; Iron (mg) 0.03 / 0.02; Vitamin A (Retinol) 30 / 19; Folate 8 / 9; Vitamin C 2 / 2. All source rows and units retained; no missing units inferred.'),
  ('sc-q1-plan',9,[130,170,505,444],'Original two-bedroom house floor plan, with both bedrooms, bathroom, corridor, hall, lounge and kitchen/dining labels, walls, doors and windows intact. Blueprint Home Plans attribution retained.'),
  ('sc-q2-fashion',10,[199,85,382,350],'Original black-and-white photograph of two adults wearing formal outfits. Complete photograph retained: dress, suit, patterned shirt and neckwear, hat, sunglasses, belt and jewellery are visible.')]:
  specs['home-economics-2010-ol-'+key]=dict(source=PAPER,page=page,bounds=bounds,alt=alt)
 p=ROOT/'components/MarkBank/figures-home-economics.json';manifest=json.loads(p.read_text())
 for key,spec in specs.items():
  path=ROOT/f'public/exam-figures/home-economics/{key}.png';d['paper'][spec['page']-1].get_pixmap(matrix=fitz.Matrix(2,2),clip=fitz.Rect(spec['bounds'])).save(path);sha=hashlib.sha256(path.read_bytes()).hexdigest();spec['sha256']=sha
  manifest[key]=dict(src=f'/exam-figures/home-economics/{key}.png',md5=hashlib.md5(path.read_bytes()).hexdigest(),alt=spec['alt'],attribution=f'SEC Home Economics 2010 Ordinary Level examination paper, page {spec["page"]} — © State Examinations Commission.',sourceNote=f'Original PDF crop, bounds {spec["bounds"]}, rendered at2×. SHA256 {sha}.')
 p.write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n');p=ROOT/REVIEW;r=json.loads(p.read_text());r['figures']=specs;p.write_text(json.dumps(r,ensure_ascii=False,indent=2)+'\n')
if __name__=='__main__':write()
