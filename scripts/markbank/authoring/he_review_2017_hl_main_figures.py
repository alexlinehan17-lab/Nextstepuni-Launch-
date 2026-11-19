#!/usr/bin/env python3
"""Original question tables/figures and both source answer tables/equations."""
import fitz,hashlib,json
from he_review_2017_hl_main import ROOT,REVIEW,PAPER,SCHEME,documents,a_regions
ALTS={4:'Complete original anaemia table with Cause, Effect of deficiency and Corrective measure blank fields.',6:'Complete original two-bacterium profile table with Food poisoning bacteria, Description/characteristic and Habitat headings and both blank rows.',8:'Complete original Ultra Heat Treatment table with blank Temperature, Time and Effect cells.'}
def write():
 d=documents();regions=a_regions(d['paper'],range(2,6));specs={}
 def add(key,kind,page,rect,alt,solution=False):
  specs['home-economics-2017-hl-'+key]=dict(kind=kind,source=PAPER if kind=='paper' else SCHEME,page=page,bounds=list(rect),alt=alt,**({'solution':True} if solution else {}))
 for n,alt in ALTS.items():
  r=regions[n];tables=d['paper'][r['page']-1].find_tables().tables;inside=[t for t in tables if r['rect'][1]<t.bbox[1] and t.bbox[3]<r['rect'][3]];assert len(inside)==1;r['rect'][3]=inside[0].bbox[3]+8;add(f'sa-q{n}','paper',r['page'],r['rect'],alt)
 # The original chart mixes raster textures, vector bars and text. Crop the
 # whole source frame so the axis, six ages and four-item legend remain.
 p=d['paper'][5];frames=[fitz.Rect(x['rect']) for x in p.get_drawings() if x['rect'].width>400 and x['rect'].height>180];assert len(frames)==1;assert [round(v,2) for v in frames[0]]==[84.48,220.44,516.48,405.78]
 add('sb-q1-bmi','paper',6,frames[0]+(-3,-3,3,3),'Complete original BMI chart: six age groups, four BMI categories, percentage axis, all bars and full legend.')
 for pn,key,caption,alt in [(9,'sc-q1-bungalow','(www.pinterest.com)','Complete original Murphy family bungalow, all room labels including Bedroom 2, doors, windows, title and attribution.'),(10,'sc-q2-outfit','(www.marieclaire.com)','Complete original athleisure outfit photograph and original attribution.')]:
  p=d['paper'][pn-1];pictures=p.get_image_info();assert len(pictures)==1;rect=fitz.Rect(pictures[0]['bbox']);matches=p.search_for(caption);assert len(matches)==1;rect|=matches[0]
  if pn==9:
   matches=p.search_for('Murphy Family Bungalow');assert len(matches)==1;rect|=matches[0]
  add(key,'paper',pn,rect+(-3,0,3,1),alt)
 p=d['paper'][10];tables=[t for t in p.find_tables().tables if t.bbox[1]<200];assert len(tables)==1;rect=fitz.Rect(tables[0].bbox);caption=[w for w in p.get_text('words') if w[1]>rect.y1 and w[1]<rect.y1+30 and w[0]>300];assert caption
 first_line=min(w[1] for w in caption);caption=[w for w in caption if abs(w[1]-first_line)<2]
 for w in caption:rect|=fitz.Rect(w[:4])
 add('sc-q3-unemployment','paper',11,rect+(-3,-3,3,1),'Complete original unemployment table for 2011–2016, all six percentages, row heading and The Irish Times attribution.')
 p=d['scheme'][8];tables=p.find_tables().tables;assert len(tables)==1;add('sb-q1b-carbohydrates','scheme',9,fitz.Rect(tables[0].bbox)+(-3,-3,3,3),'Complete original carbohydrate classification, chemical formula, examples and food-source table, preserving subscripts and all printed alternatives.',True)
 p=d['scheme'][5];words=[w for w in p.get_text('words') if 275<w[1]<295];assert words[0][4]=='yeast' and words[-1][4]=='energy';rect=fitz.Rect(words[0][:4])
 for w in words[1:]:rect|=fitz.Rect(w[:4])
 add('sa-q7-equation','scheme',6,rect+(-3,1,3,3),'Complete original fermentation equation with yeast, glucose, moisture, warmth, reaction arrow, carbon dioxide, alcohol and energy; original subscripts preserved.',True)
 p=ROOT/'components/MarkBank/figures-home-economics.json';manifest=json.loads(p.read_text())
 for key,spec in specs.items():
  path=ROOT/f'public/exam-figures/home-economics/{key}.png';d[spec['kind']][spec['page']-1].get_pixmap(matrix=fitz.Matrix(2.5,2.5),clip=fitz.Rect(spec['bounds'])).save(path);sha=hashlib.sha256(path.read_bytes()).hexdigest();spec['sha256']=sha
  manifest[key]=dict(src=f'/exam-figures/home-economics/{key}.png',md5=hashlib.md5(path.read_bytes()).hexdigest(),alt=spec['alt'],attribution=f'SEC Home Economics 2017 Higher Level {"marking scheme" if spec["kind"]=="scheme" else "examination paper"}, page {spec["page"]} — © State Examinations Commission.',sourceNote=f'Original PDF crop, bounds {spec["bounds"]}, rendered at 2.5×. SHA256 {sha}.')
  if spec.get('solution'):manifest[key]['solution']=True
 assert len(specs)==9
 p.write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n');p=ROOT/REVIEW;r=json.loads(p.read_text());r['figures']=specs;p.write_text(json.dumps(r,ensure_ascii=False,indent=2)+'\n')
if __name__=='__main__':write()
