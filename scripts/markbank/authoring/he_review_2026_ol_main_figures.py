#!/usr/bin/env python3
"""Retain every original 2026 Ordinary figure and its complete printed caption."""
import hashlib,json,fitz
from he_review_2026_ol_main import ROOT,REVIEW,documents,PAPER_A,PAPER_BC,SCHEME
FIGURES={
 'home-economics-2026-ol-sa-q7-pastry':dict(source=PAPER_A,page=5,bounds=[207,76,490,184],alt='Original photograph of flour being sifted into a bowl, with the printed Freepik source caption.'),
 'home-economics-2026-ol-sa-q12-energy-label':dict(source=PAPER_A,page=6,bounds=[55,449,542,718],alt='Original fridge-freezer EU energy label and source caption. Rating D on the A–G scale; 265 kWh/annum; frozen compartment 208 L, fresh-food compartment 372 L; noise 41 dB, class C; QR code at the top. The adjacent original answer space is retained.'),
 'home-economics-2026-ol-sa-q14-fabrics':dict(source=PAPER_A,page=7,bounds=[115,313,506,538],alt='Original collage of colourful cushions, fabric swatches, upholstery and patterned household textiles, with the printed source caption.'),
 'home-economics-2026-ol-sb-q1a-lasagne':dict(source=PAPER_BC,page=2,bounds=[76,210,565,433],alt='Original vegetarian-lasagne nutrition table per 100 g with adjacent food photograph and source caption. Energy 117 kcal; protein 4.8 g; carbohydrate 9.0 g, sugars 4.4 g; fibre 6.0 g; fats 3.5 g, saturates 0.0 g; iron printed as 1.0 g; salt 0.3 g. The iron unit is reproduced exactly as printed.'),
 'home-economics-2026-ol-sb-q3a-food-pyramid':dict(source=PAPER_BC,page=3,bounds=[53,326,565,634],alt='Original six-shelf Food Pyramid for adults, teenagers and children aged five and over, with source caption. Top foods high in fat, sugar and salt: not every day, maximum once or twice a week. Fats/spreads/oils: very small amounts. Meat/poultry/fish/eggs/beans/nuts: 2 servings; milk/yogurt/cheese: 3 servings; wholemeal cereals/breads/potatoes/pasta/rice: 3–5 servings; vegetables/salad/fruit: 5–7 servings a day.'),
 'home-economics-2026-ol-sb-q4a-microwave':dict(source=PAPER_BC,page=4,bounds=[157,104,525,278],alt='Original photograph of a white microwave oven with a dark front window and two rotary controls, and the printed Powercity source caption.'),
 'home-economics-2026-ol-sc-q1-house-plan':dict(source=PAPER_BC,page=5,bounds=[44,204,535,367],alt='Original family-house floor plan. Left: utility, playroom and sitting room above an open kitchen/dining room with patio doors to the garden. Centre: entrance hall, coat and bag storage, bathroom and ensuite. Right: main bedroom, walk-in wardrobe, two further bedrooms including a cot, and garage and gym. Doors, circulation and all room labels retained.'),
 'home-economics-2026-ol-sc-q2-uniforms':dict(source=PAPER_BC,page=6,bounds=[159,120,538,297],alt='Original photograph of four health care uniforms: a white coat, blue tunic and trousers, black tunic and trousers, and green tunic and trousers, with source caption.'),
 'home-economics-2026-ol-sc-q3-workers':dict(source=PAPER_BC,page=7,bounds=[209,124,526,265],alt='Original photograph of three construction workers wearing hard hats and high-visibility vests while consulting a plan, with the printed Building source caption.'),
 'home-economics-2026-ol-sc-q4-pregnancy':dict(source=PAPER_BC,page=8,bounds=[173,126,535,278],alt='Original photograph of a pregnant woman preparing vegetables at a kitchen counter, with the printed source caption.'),
}

def write():
 documents();p=ROOT/'components/MarkBank/figures-home-economics.json';manifest=json.loads(p.read_text())
 for key,spec in FIGURES.items():
  target=ROOT/f'public/exam-figures/home-economics/{key}.png';fitz.open(ROOT/spec['source'])[spec['page']-1].get_pixmap(matrix=fitz.Matrix(2,2),clip=fitz.Rect(spec['bounds'])).save(target);sha=hashlib.sha256(target.read_bytes()).hexdigest();spec['sha256']=sha
  manifest[key]=dict(src=f'/exam-figures/home-economics/{key}.png',md5=hashlib.md5(target.read_bytes()).hexdigest(),alt=spec['alt'],attribution=f'SEC Home Economics 2026 Ordinary Level {"marking scheme" if spec.get("solution") else "examination paper"}, page {spec["page"]} — © State Examinations Commission.',sourceNote=f'Original source crop, bounds {spec["bounds"]}, rendered at 2×. SHA256 {sha}.')
  if spec.get('solution'):manifest[key]['solution']=True
 p.write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n');p=ROOT/REVIEW;r=json.loads(p.read_text());r['figures']=FIGURES;p.write_text(json.dumps(r,ensure_ascii=False,indent=2)+'\n')

if __name__=='__main__':write()
