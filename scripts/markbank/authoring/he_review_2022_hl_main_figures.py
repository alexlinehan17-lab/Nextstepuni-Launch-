#!/usr/bin/env python3
"""Reproduce the three visually checked original question crops."""
import hashlib
import json
import fitz
from he_review_2022_hl_main import ROOT, REVIEW, PAPER_A, PAPER_BC, documents

FIGURES={
 'home-economics-2022-hl-sa-q14-symbols':dict(source=PAPER_A,page=7,bounds=[42,265,143,537],sha256='174d909296ee3b9b21897737cbce37cf720688f3e304826629e3ca2608817a82',alt='Two original symbols in vertical order: Green dot, then Eco label. Original source captions retained.'),
 'home-economics-2022-hl-sb-q1a-chart':dict(source=PAPER_BC,page=2,bounds=[88,224,528,436],sha256='b9f185b143e06326d16de7bf6aa3333fc2ac2556161ed06cdcbd1e23a08ac5db',alt='Factors that make it difficult for teenagers to eat a healthy diet. Percentage agreeing: likes/dislikes 57; convenience 52; availability 35; cost 29; advertising 25; other 3. Source: National Teens Food Survey II, adapted from iuna.net.'),
 'home-economics-2022-hl-sc-q2ai-outfits':dict(source=PAPER_BC,page=6,bounds=[173,144,398,304],sha256='9350cdadd30b7be3472830c09d95ae0ae3d8ea3eca8c8b1fb9e3e6a4a51daf49',alt='Original smart-casual outfits: one person wears a navy blazer, dark top, beige trousers and trainers; the other wears a light shirt, grey trousers and trainers. Both complete outfits and the source caption are visible.'),
}


def write():
 documents();p=ROOT/'components/MarkBank/figures-home-economics.json';manifest=json.loads(p.read_text())
 for key,spec in FIGURES.items():
  target=ROOT/f'public/exam-figures/home-economics/{key}.png';fitz.open(ROOT/spec['source'])[spec['page']-1].get_pixmap(matrix=fitz.Matrix(2,2),clip=fitz.Rect(spec['bounds'])).save(target);sha=hashlib.sha256(target.read_bytes()).hexdigest();assert sha==spec['sha256'],key
  manifest[key]=dict(src=f'/exam-figures/home-economics/{key}.png',md5=hashlib.md5(target.read_bytes()).hexdigest(),alt=spec['alt'],attribution=f'SEC Home Economics 2022 Higher Level examination paper, page {spec["page"]} — © State Examinations Commission.',sourceNote=f'Original source crop, bounds {spec["bounds"]}, rendered at 2×; visually checked. SHA256 {sha}.')
 p.write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n')
 p=ROOT/REVIEW;review=json.loads(p.read_text());review['figures']=FIGURES;p.write_text(json.dumps(review,ensure_ascii=False,indent=2)+'\n')


if __name__=='__main__':write()
