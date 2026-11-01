#!/usr/bin/env python3
"""Reproduce the two visually checked original question crops."""
import hashlib
import json
import fitz
from he_review_2021_hl_main import ROOT, REVIEW, PAPER_A, PAPER_BC, documents

FIGURES={
 'home-economics-2021-hl-sb-q1a-chart':dict(source=PAPER_BC,page=2,bounds=[135,216,477,357],sha256='e60964c51bcabe973965b499b0bc118abfa33e0af6066aeabce054f2209d5f65',alt='Original two-ring infographic: Health and Wellbeing 42%; Responsible Living 27%. Influences on evening meal consumption. Source: What Ireland Ate Last Night, Report 2020, Bord Bia Thinking House.'),
 'home-economics-2021-hl-sc-q2ai-athleisure':dict(source=PAPER_BC,page=6,bounds=[169,157,414,313],sha256='d2bcadde4d98f244fb25af1744c0bd3384817e1ee9694f0dce286dfae43c91c7',alt='Original four athleisure outfits: dark jacket and light trousers; green sweatshirt and shorts; black outfit and white trainers; white top, scarf and black leggings. The complete three-photo montage and Pinterest source caption are visible.'),
}


def write():
 documents();p=ROOT/'components/MarkBank/figures-home-economics.json';manifest=json.loads(p.read_text())
 for key,spec in FIGURES.items():
  target=ROOT/f'public/exam-figures/home-economics/{key}.png';fitz.open(ROOT/spec['source'])[spec['page']-1].get_pixmap(matrix=fitz.Matrix(2,2),clip=fitz.Rect(spec['bounds'])).save(target);sha=hashlib.sha256(target.read_bytes()).hexdigest();assert sha==spec['sha256'],key
  manifest[key]=dict(src=f'/exam-figures/home-economics/{key}.png',md5=hashlib.md5(target.read_bytes()).hexdigest(),alt=spec['alt'],attribution=f'SEC Home Economics 2021 Higher Level examination paper, page {spec["page"]} — © State Examinations Commission.',sourceNote=f'Original source crop, bounds {spec["bounds"]}, rendered at 2×; visually checked. SHA256 {sha}.')
 p.write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n')
 p=ROOT/REVIEW;review=json.loads(p.read_text());review['figures']=FIGURES;p.write_text(json.dumps(review,ensure_ascii=False,indent=2)+'\n')


if __name__=='__main__':write()
