#!/usr/bin/env python3
"""Reproduce source-pinned food-choice and sportswear crops."""
import hashlib,json,fitz
from he_review_2024_ol_main import ROOT,REVIEW,documents
FIGURES={'home-economics-2024-ol-sb-q1a-food-choice': {'page': 2, 'bounds': [60, 193, 528, 419], 'alt': 'Original diagram showing seven factors affecting food choice: food availability, work patterns, emotions, cooking skills, time, money, and likes and dislikes. All seven photographs and labels are retained.', 'source': 'examiner-reports/home-economics/papers/2024-ol-039-paper.pdf', 'sha256': '9120990a0a57b54ac42c6a0e7bb6211f4c9176ec470994deb1eb52d98c89b0cd'}, 'home-economics-2024-ol-sc-q2a-sportswear': {'page': 6, 'bounds': [190, 132, 393, 305], 'alt': 'Both original sportswear outfits: a man in a white and dark jacket with a green shoulder stripe and dark tracksuit bottoms; a woman in a dark jacket, yellow top, dark leggings with a yellow stripe and bright trainers. The original Pinterest caption is retained.', 'source': 'examiner-reports/home-economics/papers/2024-ol-039-paper.pdf', 'sha256': '7d345a91a3d526711e0c5dfdfb36eb121e297ef795eca5f904189864bf74686d'}}

def write():
 documents();p=ROOT/'components/MarkBank/figures-home-economics.json';manifest=json.loads(p.read_text())
 for key,spec in FIGURES.items():
  target=ROOT/f'public/exam-figures/home-economics/{key}.png';fitz.open(ROOT/spec['source'])[spec['page']-1].get_pixmap(matrix=fitz.Matrix(2,2),clip=fitz.Rect(spec['bounds'])).save(target);sha=hashlib.sha256(target.read_bytes()).hexdigest();assert sha==spec['sha256'],key
  manifest[key]=dict(src=f'/exam-figures/home-economics/{key}.png',md5=hashlib.md5(target.read_bytes()).hexdigest(),alt=spec['alt'],attribution=f'SEC Home Economics 2024 Ordinary Level {"marking scheme" if spec.get("solution") else "examination paper"}, page {spec["page"]} — © State Examinations Commission.',sourceNote=f'Original source crop, bounds {spec["bounds"]}, rendered at 2×; visually checked. SHA256 {sha}.')
  if spec.get('solution'):manifest[key]['solution']=True
 p.write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n')
 p=ROOT/REVIEW;review=json.loads(p.read_text());review['figures']=FIGURES;p.write_text(json.dumps(review,ensure_ascii=False,indent=2)+'\n')

if __name__=='__main__':write()
