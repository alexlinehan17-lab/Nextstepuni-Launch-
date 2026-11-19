#!/usr/bin/env python3
"""Reproduce the four visually checked original question crops."""
import hashlib
import json
import fitz
from he_review_2021_ol_main import ROOT, REVIEW, PAPER_A, PAPER_BC, documents

FIGURES={'home-economics-2021-ol-sa-q14-symbols': {'source': 'examiner-reports/home-economics/papers/2021-ol-014-paper.pdf', 'page': 7, 'bounds': [72, 110, 185, 380], 'alt': 'Two original care symbols, top to bottom: a hand in a wash tub; an iron with two dots. Original Woolmark and Omo source captions retained.', 'sha256': '7b76ffc580bb5a2c7c7e8c82c619cb8090a49e1d00206dac9b93513d18d1929d'}, 'home-economics-2021-ol-sb-q1a-yoghurt': {'source': 'examiner-reports/home-economics/papers/2021-ol-039-paper.pdf', 'page': 2, 'bounds': [82, 247, 535, 448], 'alt': 'Original nutrition table per 100 g: full fat / low fat / fat free natural yoghurt. Energy: 133 / 65 / 54 kcal; fat: 9.4 / 1.8 / 0.4 g; saturates: 5.5 / 1.1 / 0.2 g; carbohydrate: 5.9 / 6.9 / 7.6 g; sugars: 3.2 / 6.8 / 7.3 g; fibre: 0.3 / 0.5 / 0.5 g; protein: 6.0 / 4.8 / 4.8 g; salt: 0.20 / 0.20 / 0.19 g.', 'sha256': 'ff4896f57205f1504b1a8b95db16d374de2260435e5f3a9a6e323c2715354a10'}, 'home-economics-2021-ol-sc-q1a-heat-loss': {'source': 'examiner-reports/home-economics/papers/2021-ol-039-paper.pdf', 'page': 5, 'bounds': [128, 214, 428, 360], 'alt': 'Original heat-loss diagram for a family home: roof 25%, walls 35%, windows 15%, doors 10%, floor 15%. Original ORS caption retained.', 'sha256': '8fc9b53fecb8121c0305f10120c69356798051eb2248aed3f32433ca78800ea8'}, 'home-economics-2021-ol-sc-q2a-occasion-wear': {'source': 'examiner-reports/home-economics/papers/2021-ol-039-paper.pdf', 'page': 6, 'bounds': [160, 130, 395, 332], 'alt': 'The two original occasion-wear outfits: a red lace dress with fitted bodice and flared skirt, and a grey suit with shirt, tie and pocket square. Original Pinterest and The Black Tux captions retained.', 'sha256': 'bf829a5626fa7b6c2725c6fb583b0b6dd46f2306f81b7a5dda1c536a76c41ab2'}}


def write():
 documents();p=ROOT/'components/MarkBank/figures-home-economics.json';manifest=json.loads(p.read_text())
 for key,spec in FIGURES.items():
  target=ROOT/f'public/exam-figures/home-economics/{key}.png';fitz.open(ROOT/spec['source'])[spec['page']-1].get_pixmap(matrix=fitz.Matrix(2,2),clip=fitz.Rect(spec['bounds'])).save(target);sha=hashlib.sha256(target.read_bytes()).hexdigest();assert sha==spec['sha256'],key
  manifest[key]=dict(src=f'/exam-figures/home-economics/{key}.png',md5=hashlib.md5(target.read_bytes()).hexdigest(),alt=spec['alt'],attribution=f'SEC Home Economics 2021 Ordinary Level examination paper, page {spec["page"]} — © State Examinations Commission.',sourceNote=f'Original source crop, bounds {spec["bounds"]}, rendered at 2×; visually checked. SHA256 {sha}.')
 p.write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n')
 p=ROOT/REVIEW;review=json.loads(p.read_text());review['figures']=FIGURES;p.write_text(json.dumps(review,ensure_ascii=False,indent=2)+'\n')


if __name__=='__main__':write()
