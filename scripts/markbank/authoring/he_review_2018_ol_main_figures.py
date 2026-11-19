#!/usr/bin/env python3
"""Nine complete original Ordinary question inputs, including cloze word pools."""
import fitz,hashlib,json
from he_review_2018_ol_main import ROOT,REVIEW,PAPER,SCHEME,documents,a_regions
ALTS={1:'Complete original three-statement iron True/False table and both answer columns.',2:'Complete original vitamin cloze task with all three offered words and all three blank statements.',4:'Complete original lipid-source matching task, all three offered source categories and all three foods.',7:'Complete original food-preservation True/False table with all three statements and both answer columns.',8:'Complete original food spoilage/production cloze task, all three offered words and all three blank statements.',11:'Both complete original textile-care symbols, hot iron and drip dry, and their answer spaces.'}
def write():
 d=documents();regions=a_regions(d['paper'],range(2,6));specs={}
 def add(key,kind,page,rect,alt):
  specs['home-economics-2018-ol-'+key]=dict(kind=kind,source=PAPER if kind=='paper' else SCHEME,page=page,bounds=list(rect),alt=alt)
 for n,alt in ALTS.items():
  r=regions[n]
  if n in [1,4,7]:
   inside=[t for t in d['paper'][r['page']-1].find_tables().tables if r['rect'][1]<t.bbox[1] and t.bbox[3]<r['rect'][3]];assert len(inside)==1;r['rect'][3]=inside[0].bbox[3]+8
  add(f'sa-q{n}','paper',r['page'],r['rect'],alt)
 p=d['paper'][5];tables=p.find_tables().tables;assert len(tables)==1;add('sb-q1-lasagne','paper',6,fitz.Rect(tables[0].bbox)+(-3,-3,3,3),'Complete original pre-prepared beef lasagne table, all ingredients and seven nutrition lines with original values and units per100g.')
 p=d['paper'][8];pictures=p.get_image_info();assert len(pictures)==1;rect=fitz.Rect(pictures[0]['bbox']);add('sc-q1-water','paper',9,rect+(-3,-3,3,3),'Complete original cold-water system diagram: storage tank, ball valve, overflow pipe and stopcock labels, all pipes, fixtures and house outline.')
 p=d['paper'][9];pictures=p.get_image_info();assert len(pictures)==1;rect=fitz.Rect(pictures[0]['bbox']);caption=p.search_for('(www.aldi.ie)');assert len(caption)==1;rect|=caption[0];add('sc-q2-uniforms','paper',10,rect+(-3,-1,3,1),'Complete original photograph of three primary-school uniforms and full www.aldi.ie attribution.')
 p=ROOT/'components/MarkBank/figures-home-economics.json';manifest=json.loads(p.read_text())
 for key,spec in specs.items():
  path=ROOT/f'public/exam-figures/home-economics/{key}.png';d[spec['kind']][spec['page']-1].get_pixmap(matrix=fitz.Matrix(2.5,2.5),clip=fitz.Rect(spec['bounds'])).save(path);sha=hashlib.sha256(path.read_bytes()).hexdigest();spec['sha256']=sha
  manifest[key]=dict(src=f'/exam-figures/home-economics/{key}.png',md5=hashlib.md5(path.read_bytes()).hexdigest(),alt=spec['alt'],attribution=f'SEC Home Economics 2018 Ordinary Level {"marking scheme" if spec["kind"]=="scheme" else "examination paper"}, page {spec["page"]} — © State Examinations Commission.',sourceNote=f'Original PDF crop, bounds {spec["bounds"]}, rendered at 2.5×. SHA256 {sha}.')
  if spec.get('solution'):manifest[key]['solution']=True
 assert len(specs)==9
 p.write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n');p=ROOT/REVIEW;r=json.loads(p.read_text());r['figures']=specs;p.write_text(json.dumps(r,ensure_ascii=False,indent=2)+'\n')
if __name__=='__main__':write()
