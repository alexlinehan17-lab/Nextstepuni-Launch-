#!/usr/bin/env python3
"""Reproduce the two required question tables and complete snack comparison."""
import hashlib,json,fitz
from he_review_2026_hl_main import ROOT,REVIEW,documents,PAPER_A,PAPER_BC,SCHEME
FIGURES={
 'home-economics-2026-hl-sa-q1-carbohydrate-table':dict(source=PAPER_A,page=3,bounds=[83,171,544,280],alt='Original blank carbohydrate table. Columns: Monosaccharide, Disaccharide, Polysaccharide. Required rows: Chemical formula and Example; all six cells retained.'),
 'home-economics-2026-hl-sa-q5-uht-table':dict(source=PAPER_A,page=4,bounds=[83,339,544,462],alt='Original blank milk-processing table. Process: Ultra Heat Treatment; required answer columns: Temperature, Time and Effect.'),
 'home-economics-2026-hl-sb-q1a-protein-snacks':dict(source=PAPER_BC,page=2,bounds=[78,214,539,414],alt='Original high-protein snack table per 100 g/100 ml, including the adjacent product photograph and source caption. Protein bar / high-protein fruit yogurt: energy 523/122 kcal, protein 17/12 g, fat 37/2.9 g, saturates 7.6/1.3 g, carbohydrate 24/10 g, sugars 16/8 g, calcium 60/190 mg, fibre 13/3.5 g, salt 0.8/0.2 g.'),
}

def write():
 documents();p=ROOT/'components/MarkBank/figures-home-economics.json';manifest=json.loads(p.read_text())
 for key,spec in FIGURES.items():
  target=ROOT/f'public/exam-figures/home-economics/{key}.png';fitz.open(ROOT/spec['source'])[spec['page']-1].get_pixmap(matrix=fitz.Matrix(2,2),clip=fitz.Rect(spec['bounds'])).save(target);sha=hashlib.sha256(target.read_bytes()).hexdigest();spec['sha256']=sha
  manifest[key]=dict(src=f'/exam-figures/home-economics/{key}.png',md5=hashlib.md5(target.read_bytes()).hexdigest(),alt=spec['alt'],attribution=f'SEC Home Economics 2026 Higher Level {"marking scheme" if spec.get("solution") else "examination paper"}, page {spec["page"]} — © State Examinations Commission.',sourceNote=f'Original source crop, bounds {spec["bounds"]}, rendered at 2×. SHA256 {sha}.')
  if spec.get('solution'):manifest[key]['solution']=True
 p.write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n');p=ROOT/REVIEW;r=json.loads(p.read_text());r['figures']=FIGURES;p.write_text(json.dumps(r,ensure_ascii=False,indent=2)+'\n')

if __name__=='__main__':write()
