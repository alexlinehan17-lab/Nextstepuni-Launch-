#!/usr/bin/env python3
"""Complete original Ordinary tables, pie chart, water diagram and uniform."""
import fitz,hashlib,json
from he_review_2012_ol_main import ROOT,REVIEW,PAPER,documents,a_regions
ALTS={1:'Original protein true/false question: three complete statements, True and False columns, all blank tick cells.',2:'Original starch cloze: insoluble, gelatinisation, hygroscopic word bank and all three complete statements with their blank spaces.',5:'Original vegetarian food-source table: Protein, Calcium, Vitamin B, with Source 1 and Source 2 blank cells.',6:'Original fruit table: Class of Fruit and matching Example columns, three paired blank numbered rows.',10:'Original six-property textile pool: Durable, Colourfast, Irritant, Windproof, Flammable, Absorbent; choose three and all blank tick cells retained.',11:'Original renewable/non-renewable energy table and its separately worded request for two energy-reduction methods. Complete blank table and answer rules retained.'}
def write():
 d=documents();regions=a_regions(d['paper'],range(2,6));specs={}
 for n,alt in ALTS.items():
  r=regions[n];specs[f'home-economics-2012-ol-sa-q{n}']=dict(kind='paper',source=PAPER,page=r['page'],bounds=r['rect'],alt=alt)
 specs['home-economics-2012-ol-sb-q1-choice']=dict(kind='paper',source=PAPER,page=6,bounds=[80,127.8,555,359],alt='Original National Adult Nutritional Survey 2011 food-choice pie chart and Irish Universities Nutrition Alliance caption: Taste 41%, Health & Nutrition 36%, Cost 9%, Convenience 7%, Mood 2%, Weight Control 5%. All six sectors and labels retained.')
 specs['home-economics-2012-ol-sc-q1-water']=dict(kind='paper',source=PAPER,page=9,bounds=[86,187,553,361],alt='Original full water-treatment diagram: reservoir, screening, sedimentation, filtration, chlorination and fluoridation, softening and testing, high storage reservoir and to mains. All original diagram labels and border retained; no diagram redrawn.')
 specs['home-economics-2012-ol-sc-q2-uniform']=dict(kind='paper',source=PAPER,page=10,bounds=[208,110,399,319],alt='Original full school uniform photograph: two complete outfits including shirt, cardigan and crest, trousers, skirt and shoes. No garments cropped.')
 p=ROOT/'components/MarkBank/figures-home-economics.json';manifest=json.loads(p.read_text())
 for key,spec in specs.items():
  path=ROOT/f'public/exam-figures/home-economics/{key}.png';d['paper'][spec['page']-1].get_pixmap(matrix=fitz.Matrix(2.5,2.5),clip=fitz.Rect(spec['bounds'])).save(path);sha=hashlib.sha256(path.read_bytes()).hexdigest();spec['sha256']=sha
  manifest[key]=dict(src=f'/exam-figures/home-economics/{key}.png',md5=hashlib.md5(path.read_bytes()).hexdigest(),alt=spec['alt'],attribution=f'SEC Home Economics 2012 Ordinary Level examination paper, page {spec["page"]} — © State Examinations Commission.',sourceNote=f'Original PDF crop, bounds {spec["bounds"]}, rendered at 2.5×. SHA256 {sha}.')
 p.write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n');p=ROOT/REVIEW;r=json.loads(p.read_text());r['figures']=specs;p.write_text(json.dumps(r,ensure_ascii=False,indent=2)+'\n')
if __name__=='__main__':write()
