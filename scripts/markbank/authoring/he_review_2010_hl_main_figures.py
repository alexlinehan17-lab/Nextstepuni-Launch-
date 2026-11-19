#!/usr/bin/env python3
"""Original question tables, labels and full seven-sector graph; no redrawing."""
import fitz,hashlib,json
from he_review_2010_hl_main import ROOT,REVIEW,PAPER,documents,a_regions
ALTS={1:'Original protein-digestion question and table. Given cells: Organ / Gland, Pancreas; Secretion, Pancreatic Juice. Blank answer columns: Enzyme, Substrate and Product.',2:'Original question and three-row blank sugar-properties table. Columns: Property and Culinary use. The student selects three properties and a matching use for each.',7:'Original question and conditioning-agent table. Required choice: two of Humectants, Polyphosphates and Stabilisers; blank Function column.',12:'Original consumer-symbol question. Green Dot logo with two interlocking circular arrows and Eco Label flower logo with EU stars; both printed captions and answer spaces retained.'}

def write():
 d=documents();regions=a_regions(d['paper'],range(2,6));specs={}
 for n,alt in ALTS.items():
  r=regions[n];specs[f'home-economics-2010-hl-sa-q{n}']=dict(source=PAPER,page=r['page'],bounds=r['rect'],alt=alt)
 specs['home-economics-2010-hl-sb-q1-exports']=dict(source=PAPER,page=6,bounds=[150,150,505,475],alt='Original Bord Bia pie chart, Breakdown of Irish food and drink exports, 2008 (%). Dairy Products 29%, Beef 21%, Prepared Foods 18%, Beverages 15%, Pigmeat 4%, Seafood 4%, Other 9%. Complete title, seven sectors, labels and source caption retained.')
 p=ROOT/'components/MarkBank/figures-home-economics.json';manifest=json.loads(p.read_text())
 for key,spec in specs.items():
  path=ROOT/f'public/exam-figures/home-economics/{key}.png';d['paper'][spec['page']-1].get_pixmap(matrix=fitz.Matrix(2,2),clip=fitz.Rect(spec['bounds'])).save(path);sha=hashlib.sha256(path.read_bytes()).hexdigest();spec['sha256']=sha
  manifest[key]=dict(src=f'/exam-figures/home-economics/{key}.png',md5=hashlib.md5(path.read_bytes()).hexdigest(),alt=spec['alt'],attribution=f'SEC Home Economics 2010 Higher Level examination paper, page {spec["page"]} — © State Examinations Commission.',sourceNote=f'Original PDF crop, bounds {spec["bounds"]}, rendered at 2×. SHA256 {sha}.')
 p.write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n');p=ROOT/REVIEW;r=json.loads(p.read_text());r['figures']=specs;p.write_text(json.dumps(r,ensure_ascii=False,indent=2)+'\n')
if __name__=='__main__':write()
