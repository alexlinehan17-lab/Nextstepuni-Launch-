#!/usr/bin/env python3
"""Original 2020 Higher inputs from both booklets, including every table cell/caption."""
import fitz,hashlib,json
from he_review_2020_hl_main import ROOT,REVIEW,PAPER_A,PAPER_BC,documents,a_regions
ALTS={1:'Complete original carbohydrate table: required formula and example fields for monosaccharides, disaccharides and polysaccharides.',4:'Complete original vitamin-deficiency table: poor blood clotting, neural tube defects and night blindness.',8:'Complete original artificial-sweetener class/type and matching-example table.',9:'Both complete original consumer symbols: Green Dot and PET identification 1 recycling symbol, with repak.ie and clearpak.com source captions.'}
def write():
 d=documents();regions=a_regions(d['a'],range(3,7));specs={}
 def add(key,kind,page,rect,alt):specs['home-economics-2020-hl-'+key]=dict(kind=kind,source=PAPER_A if kind=='a' else PAPER_BC,page=page,bounds=list(rect),alt=alt)
 for n,alt in ALTS.items():
  r=regions[n]
  if n in [1,4,8]:
   ts=[t for t in d['a'][r['page']-1].find_tables().tables if r['rect'][1]<t.bbox[1] and t.bbox[3]<r['rect'][3]];assert len(ts)==1;r['rect'][3]=ts[0].bbox[3]+8
  add(f'sa-q{n}','a',r['page'],r['rect'],alt)
 p=d['bc'][1];ts=p.find_tables().tables;assert len(ts)==1;rect=fitz.Rect(ts[0].bbox);hits=p.search_for('safefood.eu/media/safefoodlibrary');assert len(hits)==1
 for block in p.get_text('dict')['blocks']:
  for line in block.get('lines',[]):
   if fitz.Rect(line['bbox']).intersects(hits[0]):rect|=fitz.Rect(line['bbox'])
 add('sb-q1-portions','bc',2,rect+(-4,-4,4,4),'Complete original safefood portion-size table: all ten situations and three percentage columns (sometimes, always and never difficult), with complete safefood.eu/media/safefoodlibrary attribution.')
 p=ROOT/'components/MarkBank/figures-home-economics.json';manifest=json.loads(p.read_text())
 for key,spec in specs.items():
  path=ROOT/f'public/exam-figures/home-economics/{key}.png';d[spec['kind']][spec['page']-1].get_pixmap(matrix=fitz.Matrix(2.5,2.5),clip=fitz.Rect(spec['bounds'])).save(path);spec['sha256']=hashlib.sha256(path.read_bytes()).hexdigest()
  manifest[key]=dict(src=f'/exam-figures/home-economics/{key}.png',md5=hashlib.md5(path.read_bytes()).hexdigest(),alt=spec['alt'],attribution=f'SEC Home Economics 2020 Higher Level examination paper, '+('Section A' if spec['kind']=='a' else 'Sections B/C')+f' booklet page {spec["page"]} — © State Examinations Commission.',sourceNote=f'Original PDF crop, bounds {spec["bounds"]}, rendered at 2.5×. SHA256 {spec["sha256"]}.')
 assert len(specs)==5;p.write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n');p=ROOT/REVIEW;r=json.loads(p.read_text());r['figures']=specs;p.write_text(json.dumps(r,ensure_ascii=False,indent=2)+'\n')
if __name__=='__main__':write()
