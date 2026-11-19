#!/usr/bin/env python3
"""Reproduce all six original 2025 Ordinary figure groups, including captions."""
import hashlib,json,fitz
from he_review_2025_ol_main import ROOT,REVIEW,documents,PAPER_A,PAPER_BC,SCHEME
FIGURES={
 'home-economics-2025-ol-sa-q14-care-symbols':dict(source=PAPER_A,page=7,bounds=[96,366,225,610],alt='Both original fabric-care symbols in printed order: hand in a wash tub, then an iron with two dots; original Woolmark and OMO source captions retained.'),
 'home-economics-2025-ol-sb-q1a-soups':dict(source=PAPER_BC,page=2,bounds=[89,218,520,499],alt='Original comparison per 100 g. Soup A cook-chill costs €2.89; Soup B canned costs €2.00. A/B: energy 27/32 kcal, protein 1.1/0.8 g, carbohydrates 4.3/5.6 g, sugars 2.2/1.0 g, fibre 3.0/0.5 g, fat 0.6/0.5 g, saturates 0.1/0.3 g, salt 0.2/0.8 g. Both product images and source captions retained.'),
 'home-economics-2025-ol-sc-q1a-heat-loss':dict(source=PAPER_BC,page=5,bounds=[177,228,489,361],alt='Original house heat-loss diagram with the five printed percentages: 25%, 35%, 10%, 15% and 15% and the Synergy Files source caption.'),
 'home-economics-2025-ol-sc-q2a-wedding-outfits':dict(source=PAPER_BC,page=6,bounds=[168,149,475,333],alt='All three original wedding outfits in printed order: a black one-shoulder jumpsuit, a dark grey suit with black top, and a blue floral dress. Original image-source caption retained.'),
 'home-economics-2025-ol-sc-q3a-classroom':dict(source=PAPER_BC,page=7,bounds=[208,132,404,291],alt='Original classroom photograph with children and their teacher, with the Logo Leisurewear source caption.'),
 'home-economics-2025-ol-sc-q4a-yoghurt':dict(source=PAPER_BC,page=8,bounds=[102,140,514,267],alt='Both original yoghurt photographs and their source captions: multiple retail tubs on the left and jars and small yoghurt pots on the right.'),
}

def write():
 documents();p=ROOT/'components/MarkBank/figures-home-economics.json';manifest=json.loads(p.read_text())
 for key,spec in FIGURES.items():
  target=ROOT/f'public/exam-figures/home-economics/{key}.png';fitz.open(ROOT/spec['source'])[spec['page']-1].get_pixmap(matrix=fitz.Matrix(2,2),clip=fitz.Rect(spec['bounds'])).save(target);sha=hashlib.sha256(target.read_bytes()).hexdigest();spec['sha256']=sha
  manifest[key]=dict(src=f'/exam-figures/home-economics/{key}.png',md5=hashlib.md5(target.read_bytes()).hexdigest(),alt=spec['alt'],attribution=f'SEC Home Economics 2025 Ordinary Level {"marking scheme" if spec.get("solution") else "examination paper"}, page {spec["page"]} — © State Examinations Commission.',sourceNote=f'Original source crop, bounds {spec["bounds"]}, rendered at 2×. SHA256 {sha}.')
  if spec.get('solution'):manifest[key]['solution']=True
 p.write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n');p=ROOT/REVIEW;r=json.loads(p.read_text());r['figures']=FIGURES;p.write_text(json.dumps(r,ensure_ascii=False,indent=2)+'\n')

if __name__=='__main__':write()
