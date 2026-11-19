#!/usr/bin/env python3
"""Reproduce the original eight-category chart, both outfits and complete answer table."""
import hashlib,json,fitz
from he_review_2025_hl_main import ROOT,REVIEW,documents,PAPER_BC,SCHEME
FIGURES={
 'home-economics-2025-hl-sb-q1a-chart':dict(source=PAPER_BC,page=2,bounds=[126,192,555,429],alt='Original 2024 survey chart: bread, potatoes, pasta, rice and grains 23%; sugar, drinks, biscuits and cakes 21%; others 16%; meat and meat products 14%; fruit and vegetables 9%; milk and yogurt 7%; breakfast cereals 5%; soups and sauces 3%. National Adult Nutrition Survey II, Summary Report, 2024 caption retained.'),
 'home-economics-2025-hl-sc-q2a-outfits':dict(source=PAPER_BC,page=6,bounds=[152,127,475,348],alt='Both original blazer outfits: first, grey blazer, printed white T-shirt, blue wide-leg jeans, boots and yellow handbag; second, navy blazer, white top, dark trousers and trainers, with suitcase. Original picture-source caption retained.'),
 'home-economics-2025-hl-sb-q3a-scheme-table':dict(source=SCHEME,page=15,bounds=[30,195,576,760],solution=True,alt='Complete original marking table for Salmonella, Listeria, E. coli, Clostridium botulinum and Staphylococcus aureus, with sources, high-risk foods, growth factors and symptoms. The additional Clostridium perfringens and Campylobacter acceptance is retained below the table.'),
}

def write():
 documents();p=ROOT/'components/MarkBank/figures-home-economics.json';manifest=json.loads(p.read_text())
 for key,spec in FIGURES.items():
  target=ROOT/f'public/exam-figures/home-economics/{key}.png';fitz.open(ROOT/spec['source'])[spec['page']-1].get_pixmap(matrix=fitz.Matrix(2,2),clip=fitz.Rect(spec['bounds'])).save(target);sha=hashlib.sha256(target.read_bytes()).hexdigest();spec['sha256']=sha
  manifest[key]=dict(src=f'/exam-figures/home-economics/{key}.png',md5=hashlib.md5(target.read_bytes()).hexdigest(),alt=spec['alt'],attribution=f'SEC Home Economics 2025 Higher Level {"marking scheme" if spec.get("solution") else "examination paper"}, page {spec["page"]} — © State Examinations Commission.',sourceNote=f'Original source crop, bounds {spec["bounds"]}, rendered at 2×. SHA256 {sha}.')
  if spec.get('solution'):manifest[key]['solution']=True
 p.write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n');p=ROOT/REVIEW;r=json.loads(p.read_text());r['figures']=FIGURES;p.write_text(json.dumps(r,ensure_ascii=False,indent=2)+'\n')

if __name__=='__main__':write()
