#!/usr/bin/env python3
"""Ten complete original inputs: tables, cloze, symbols, chart, floorplan and photo."""
import fitz,hashlib,json,sys
from he_review_2020_ol_main import ROOT,REVIEW,PAPER_A,PAPER_BC,documents,a_regions
ALTS={1:'Complete original three-statement carbohydrate True/False table.',3:'Complete original milk-processing cloze task, all three blanks and spray drying, pasteurised, homogenisation word pool.',4:'Complete original two egg culinary-use and matching food/dish blank table.',5:'Complete original three-statement sauce True/False table.',7:'Complete original three-row diet-effect table: high saturated fat, low fibre and low calcium.',9:'Complete original three-statement USC, utility bills and child benefit True/False table.',12:'Both complete original textile-care symbols, their response spaces and full goodhousekeeping.com attribution.'}
def write(preview=False):
 d=documents();regions=a_regions(d['a'],range(3,7));specs={}
 def add(key,kind,page,rect,alt):specs['home-economics-2020-ol-'+key]=dict(kind=kind,source=PAPER_A if kind=='a' else PAPER_BC,page=page,bounds=list(rect),alt=alt)
 def with_label(page,rect,token):
  hits=page.search_for(token);assert len(hits)==1,(token,hits)
  for block in page.get_text('dict')['blocks']:
   for line in block.get('lines',[]):
    if fitz.Rect(line['bbox']).intersects(hits[0]):rect|=fitz.Rect(line['bbox'])
  return rect+(-4,-4,4,4)
 for n,alt in ALTS.items():
  r=regions[n]
  if n in [1,4,5,7,9]:
   ts=[t for t in d['a'][r['page']-1].find_tables().tables if r['rect'][1]<t.bbox[1] and t.bbox[3]<r['rect'][3]];assert len(ts)==1,(n,ts);r['rect'][3]=ts[0].bbox[3]+8
  add(f'sa-q{n}','a',r['page'],r['rect'],alt)
 p=d['bc'][1];caption=p.search_for('Thinking House');quote=p.search_for('1 in 3 people');end=p.search_for('(a)');assert len(caption)==len(quote)==len(end)==1
 rect=fitz.Rect(55,quote[0].y0-4,545,end[0].y0-6)
 add('sb-q1-red-meat','bc',2,rect,'Complete original Reduction in red meat consumption chart: all six reasons and percentages (11, 17, 27, 30, 30, 67), with the full Dietary Lifestyles Report / Thinking House / Bord Bia attribution.')
 p=d['bc'][4];images=p.get_image_info();assert len(images)>100
 rect=fitz.Rect(images[0]['bbox'])
 for im in images[1:]:rect|=fitz.Rect(im['bbox'])
 add('sc-q1-floor-plan','bc',5,with_label(p,rect,'Front door'),'Complete original ground-floor plan with all rooms, patio, garage, stairs and front-door label, retained for both suitability and accessibility-modification tasks.')
 p=d['bc'][5];images=p.get_image_info();assert len(images)==1
 add('sc-q2-clothing','bc',6,with_label(p,fitz.Rect(images[0]['bbox']),'dunnesstores'),'Complete original children’s clothing photograph and full dunnesstores.com attribution; retained for suitability and matching fabric tasks.')
 assert len(specs)==10
 manifest_path=ROOT/'components/MarkBank/figures-home-economics.json';manifest=json.loads(manifest_path.read_text())
 for key,spec in specs.items():
  path=ROOT/(f'tmp/pdfs/home-economics-review/2020-ol-main/crops/{key}.png' if preview else f'public/exam-figures/home-economics/{key}.png');path.parent.mkdir(parents=True,exist_ok=True)
  d[spec['kind']][spec['page']-1].get_pixmap(matrix=fitz.Matrix(2.5,2.5),clip=fitz.Rect(spec['bounds'])).save(path);sha=hashlib.sha256(path.read_bytes()).hexdigest();spec['sha256']=sha
  manifest[key]=dict(src=f'/exam-figures/home-economics/{key}.png',md5=hashlib.md5(path.read_bytes()).hexdigest(),alt=spec['alt'],attribution=f'SEC Home Economics 2020 Ordinary Level examination paper, '+('Section A' if spec['kind']=='a' else 'Sections B/C')+f' booklet page {spec["page"]} — © State Examinations Commission.',sourceNote=f'Original PDF crop, bounds {spec["bounds"]}, rendered at 2.5×. SHA256 {sha}.')
 if preview:(ROOT/'tmp/he-2020-ol-figures-preview.json').write_text(json.dumps(specs,ensure_ascii=False,indent=2)+'\n')
 else:
  manifest_path.write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n');p=ROOT/REVIEW;r=json.loads(p.read_text());r['figures']=specs;p.write_text(json.dumps(r,ensure_ascii=False,indent=2)+'\n')
if __name__=='__main__':write('--preview' in sys.argv)
