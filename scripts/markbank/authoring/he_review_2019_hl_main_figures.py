#!/usr/bin/env python3
"""Two original question-input figures, including every chart bar and attribution."""
import fitz,hashlib,json
from he_review_2019_hl_main import ROOT,REVIEW,PAPER,documents,a_regions
def write():
 d=documents();regions=a_regions(d['paper'],range(2,6));specs={}
 def add(key,page,rect,alt):specs['home-economics-2019-hl-'+key]=dict(kind='paper',source=PAPER,page=page,bounds=list(rect),alt=alt)
 r=regions[3];p=d['paper'][r['page']-1];inside=[t for t in p.find_tables().tables if r['rect'][1]<t.bbox[1] and t.bbox[3]<r['rect'][3]];assert len(inside)==1;r['rect'][3]=inside[0].bbox[3]+8
 add('sa-q3',r['page'],r['rect'],'Complete original mineral-deficiency table with Osteomalacia, Dry flaky skin and Goitre rows and blank Mineral answers.')
 p=d['paper'][5];pictures=p.get_image_info();assert len(pictures)==1;rect=fitz.Rect(pictures[0]['bbox']);caption=p.search_for('Bord Bia');assert len(caption)==1
 # Expand to the complete source attribution line, not only its first words.
 for block in p.get_text('dict')['blocks']:
  for line in block.get('lines',[]):
   if fitz.Rect(line['bbox']).intersects(caption[0]):rect|=fitz.Rect(line['bbox'])
 add('sb-q1-survey',6,rect+(-4,-4,4,4),'Complete original Healthy Snacking Survey chart: low sugar 66%, low fat 56%, calories 54%, low salt 36%, high protein 35%, additive free 26%, clean 23%, raw 5%, with full Bord Bia attribution.')
 p=ROOT/'components/MarkBank/figures-home-economics.json';manifest=json.loads(p.read_text())
 for key,spec in specs.items():
  path=ROOT/f'public/exam-figures/home-economics/{key}.png';d['paper'][spec['page']-1].get_pixmap(matrix=fitz.Matrix(2.5,2.5),clip=fitz.Rect(spec['bounds'])).save(path);sha=hashlib.sha256(path.read_bytes()).hexdigest();spec['sha256']=sha
  manifest[key]=dict(src=f'/exam-figures/home-economics/{key}.png',md5=hashlib.md5(path.read_bytes()).hexdigest(),alt=spec['alt'],attribution=f'SEC Home Economics 2019 Higher Level examination paper, page {spec["page"]} — © State Examinations Commission.',sourceNote=f'Original PDF crop, bounds {spec["bounds"]}, rendered at 2.5×. SHA256 {sha}.')
 assert len(specs)==2;p.write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n');p=ROOT/REVIEW;r=json.loads(p.read_text());r['figures']=specs;p.write_text(json.dumps(r,ensure_ascii=False,indent=2)+'\n')
if __name__=='__main__':write()
