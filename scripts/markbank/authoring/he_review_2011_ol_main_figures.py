#!/usr/bin/env python3
"""Original 2011 Ordinary question input tables, label, chart and photographs; no redrawing."""
import fitz,hashlib,json
from he_review_2011_ol_main import ROOT,REVIEW,PAPER,documents,a_regions
ALTS={1:'Original carbohydrate matching table and printed classification choices. Sources: cellulose e.g. vegetables, glucose e.g. fruit, sucrose e.g. table sugar; blank Classification column.',3:'Original B-vitamin cloze with all three complete sentences and the printed word bank: folic acid, thiamine, energy.',4:'Original three-statement True/False table: osteoporosis, lacto-vegetarian dairy produce, and cholesterol transport; both response columns retained.',5:'Original preservation-function matching table and word bank: pectin, blanching, sugar and vinegar; all three function rows retained.',6:'Original raising-agent question, all three dish rows Bread / Sponge Cake / Muffins, blank Raising Agents column, and dependent underlying-principle prompt.',9:'Original appliance energy label and question. Complete A–G efficiency scale, large A rating arrow, energy and washing/spinning performance, capacity, water and noise rows, and EU logo retained.'}

def write():
 d=documents();regions=a_regions(d['paper'],range(2,6));specs={}
 for n,alt in ALTS.items():
  r=regions[n]
  if n==3:r['rect'][3]=690
  specs[f'home-economics-2011-ol-sa-q{n}']=dict(source=PAPER,page=r['page'],bounds=r['rect'],alt=alt)
 specs['home-economics-2011-ol-sb-q1-fish']=dict(source=PAPER,page=6,bounds=[82,145,545,311],alt='Original nutrition table per 100 g for Cod and Salmon. Protein 18.3 g/20.2 g; fat 0.7 g/11.0 g; carbohydrate 0 g/0 g; cod minerals Iron, Phosphorus, Iodine; salmon minerals Phosphorus, Calcium, Iodine; vitamins B group / A,D,B group; energy 80 kcal/180 kcal. Complete headings, units and both rows retained.')
 specs['home-economics-2011-ol-sb-q2-fruit']=dict(source=PAPER,page=7,bounds=[125,105,520,365],alt='Original fooddudes.ie chart: More portions of fruit & veg being eaten in the HOME (%). All six paired bar categories None, One, Two, Three, Four, Five; black children and grey parents legend; full percentage axis 0–35; title and source caption retained. Bars carry no exact printed value labels.')
 specs['home-economics-2011-ol-sc-q1-houses']=dict(source=PAPER,page=9,bounds=[100,176,470,322],alt='All three original housing-style photographs: a multi-storey apartment building, a detached single-storey house and adjoining two-storey houses. Complete images retained, without redrawing or invented labels.')
 specs['home-economics-2011-ol-sc-q3-poverty']=dict(source=PAPER,page=11,bounds=[145,133,475,238],alt='Original Poverty in Ireland 2008 table. Consistent Poverty 4.2% (178,074 people); At Risk of Poverty 14.4% (610,538 people); footnote also known as relative poverty. Complete title, two rows and footnote retained.')
 p=ROOT/'components/MarkBank/figures-home-economics.json';manifest=json.loads(p.read_text())
 for key,spec in specs.items():
  path=ROOT/f'public/exam-figures/home-economics/{key}.png';d['paper'][spec['page']-1].get_pixmap(matrix=fitz.Matrix(2,2),clip=fitz.Rect(spec['bounds'])).save(path);sha=hashlib.sha256(path.read_bytes()).hexdigest();spec['sha256']=sha
  manifest[key]=dict(src=f'/exam-figures/home-economics/{key}.png',md5=hashlib.md5(path.read_bytes()).hexdigest(),alt=spec['alt'],attribution=f'SEC Home Economics 2011 Ordinary Level examination paper, page {spec["page"]} — © State Examinations Commission.',sourceNote=f'Original PDF crop, bounds {spec["bounds"]}, rendered at 2×. SHA256 {sha}.')
 p.write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n');p=ROOT/REVIEW;r=json.loads(p.read_text());r['figures']=specs;p.write_text(json.dumps(r,ensure_ascii=False,indent=2)+'\n')
if __name__=='__main__':write()
