#!/usr/bin/env python3
"""Ten complete original question/model crops after independent source review."""
import fitz,hashlib,json
from he_review_2015_hl_main import ROOT,REVIEW,PAPER,SCHEME,documents,a_regions
ALTS={2:'Original carbohydrate table: all three named classes, Example and Food source columns, and every blank cell.',5:'Original wheat-grain table: complete Bran/Endosperm/Germ inputs and nutritional-significance cells.',7:'Original sauce-classification question and TWO blank classification/example rows, preserving the printed response quota.',8:'Original enzymic-spoilage question asking TWO of THREE named treatments: Blanching, Cold temperatures and Acids.'}
def write():
 d=documents();regions=a_regions(d['paper'],range(2,6));specs={}
 for n,alt in ALTS.items():
  r=regions[n];specs[f'home-economics-2015-hl-sa-q{n}']=dict(kind='paper',source=PAPER,page=r['page'],bounds=r['rect'],alt=alt)
 boxes=[x['rect'] for x in d['paper'][5].get_drawings() if x['type']=='s'];assert len(boxes)==1
 specs['home-economics-2015-hl-sb-q1-survey']=dict(kind='paper',source=PAPER,page=6,bounds=list(boxes[0]+(-3,-3,3,3)),alt='Complete original school-food survey quotation, including every outlet percentage and all nine food/drink categories and percentages.')
 models=[(4,'sa-q2-answer-table','Original complete carbohydrate answer table, preserving each class and the aligned example/food-source associations.'),(12,'sb-q3b-moulds','Original four-mould table with every name, characteristic and applicable reproduction method; complete general reproduction guidance remains in the answer rows.'),(13,'sb-q4b-budget','Original ten-area family budget, preserving all percentages, euro amounts and reasons, including underlined compulsory Housing, Food and Savings.'),(14,'sb-q4c-savings','Original complete six-model savings table: institution/scheme, historical interest, access and tax remain aligned in their original cells.'),(16,'sc-q1aii-plastics','Original Thermoplastic/Thermosetting comparison table, retaining both properties and all matching example/use pairs.')]
 for page,key,alt in models:
  tables=d['scheme'][page-1].find_tables().tables;assert len(tables)==1,(page,len(tables))
  specs['home-economics-2015-hl-'+key]=dict(kind='scheme',source=SCHEME,page=page,bounds=list(fitz.Rect(tables[0].bbox)+(-3,-3,3,3)),alt=alt,solution=True)
 p=ROOT/'components/MarkBank/figures-home-economics.json';manifest=json.loads(p.read_text())
 for key,spec in specs.items():
  path=ROOT/f'public/exam-figures/home-economics/{key}.png';d[spec['kind']][spec['page']-1].get_pixmap(matrix=fitz.Matrix(2.5,2.5),clip=fitz.Rect(spec['bounds'])).save(path);sha=hashlib.sha256(path.read_bytes()).hexdigest();spec['sha256']=sha
  manifest[key]=dict(src=f'/exam-figures/home-economics/{key}.png',md5=hashlib.md5(path.read_bytes()).hexdigest(),alt=spec['alt'],attribution=f'SEC Home Economics 2015 Higher Level {"marking scheme" if spec["kind"]=="scheme" else "examination paper"}, page {spec["page"]} — © State Examinations Commission.',sourceNote=f'Original PDF crop, bounds {spec["bounds"]}, rendered at 2.5×. SHA256 {sha}.')
  if spec.get('solution'):manifest[key]['solution']=True
 p.write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n');p=ROOT/REVIEW;r=json.loads(p.read_text());r['figures']=specs;p.write_text(json.dumps(r,ensure_ascii=False,indent=2)+'\n')
if __name__=='__main__':write()
