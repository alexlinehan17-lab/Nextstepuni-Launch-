#!/usr/bin/env python3
"""Reproduce source-pinned chart, summer outfits and chemistry solution crops."""
import hashlib,json,fitz
from he_review_2024_hl_main import ROOT,REVIEW,documents
FIGURES={'home-economics-2024-hl-sb-q1a-chart': {'source': 'examiner-reports/home-economics/papers/2024-hl-039-paper.pdf', 'page': 2, 'bounds': [85, 207, 551, 452], 'alt': 'Original Eurobarometer chart, 2022 (blue) / 2019 (red), percentage of consumers: cost 63 / 57; food safety 52 / 51; origin of food 36 / 44; impact on environment 11 / 0; nutrient content 52 / 52. Both year keys, axes and EFSA caption retained.', 'sha256': '61037c3834e030eacb4996f4327d96db010879fdd09d39b43e0388b776ef0550'}, 'home-economics-2024-hl-sb-q1b-chemistry': {'source': 'paper-trail-corpus/markingschemes/2024/LC098ALP000EV.pdf', 'page': 12, 'bounds': [54, 80, 551, 405], 'solution': True, 'alt': 'Original marking-scheme chemical diagrams: glucose ring structure with atom and hydroxyl-group labels, and two monosaccharide rings joining with loss of H₂O. Includes the corresponding structure and formation guidance.', 'sha256': 'd864a5a04f4edcb13d9c72942c1a7503ab463985806b4b82b59cf80291704208'}, 'home-economics-2024-hl-sc-q2ai-summer-outfits': {'source': 'examiner-reports/home-economics/papers/2024-hl-039-paper.pdf', 'page': 6, 'bounds': [165, 136, 369, 297], 'alt': 'Both original summer outfits: a floral dress with thin straps and an asymmetrical hem, and a denim jacket with white T-shirt, beige trousers and white trainers. Both original source captions retained.', 'sha256': '659ce7703e0241eb2ed0545ceee56eab6b2b65b16b746f3cc6dadd3022025883'}}

def write():
 documents();p=ROOT/'components/MarkBank/figures-home-economics.json';manifest=json.loads(p.read_text())
 for key,spec in FIGURES.items():
  target=ROOT/f'public/exam-figures/home-economics/{key}.png';fitz.open(ROOT/spec['source'])[spec['page']-1].get_pixmap(matrix=fitz.Matrix(2,2),clip=fitz.Rect(spec['bounds'])).save(target);sha=hashlib.sha256(target.read_bytes()).hexdigest();assert sha==spec['sha256'],key
  manifest[key]=dict(src=f'/exam-figures/home-economics/{key}.png',md5=hashlib.md5(target.read_bytes()).hexdigest(),alt=spec['alt'],attribution=f'SEC Home Economics 2024 Higher Level {"marking scheme" if spec.get("solution") else "examination paper"}, page {spec["page"]} — © State Examinations Commission.',sourceNote=f'Original source crop, bounds {spec["bounds"]}, rendered at 2×; visually checked. SHA256 {sha}.')
  if spec.get('solution'):manifest[key]['solution']=True
 p.write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n')
 p=ROOT/REVIEW;review=json.loads(p.read_text());review['figures']=FIGURES;p.write_text(json.dumps(review,ensure_ascii=False,indent=2)+'\n')

if __name__=='__main__':write()
