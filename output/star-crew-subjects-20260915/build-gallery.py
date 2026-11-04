"""Build the artwork manifest and measure ink framing without editing image pixels."""
from pathlib import Path
from PIL import Image
import json, math

root = Path(__file__).resolve().parent
catalogue = json.loads((root / 'catalogue.json').read_text())
prompt_set = json.loads((root / 'prompts.json').read_text())
concepts = {x['id']: x for x in prompt_set['subjects']}
concepts['music'] = {'character': 'The Performer', 'detail': 'A dedicated subject character playing an acoustic guitar.'}
overrides_path = root / 'artwork-overrides.json'
overrides = json.loads(overrides_path.read_text()) if overrides_path.exists() else {}
new_subjects = [
    {'id': 'climate-action-and-sustainable-development', 'name': 'Climate Action and Sustainable Development', 'category': 'social-environmental', 'programme': 'leaving-certificate-established', 'source': 'https://www.curriculumonline.ie/senior-cycle/senior-cycle-subjects/climate-action-and-sustainable-development/'},
    {'id': 'drama-film-and-theatre-studies', 'name': 'Drama, Film and Theatre Studies', 'category': 'arts', 'programme': 'leaving-certificate-established', 'source': 'https://www.curriculumonline.ie/senior-cycle/senior-cycle-subjects/drama-film-and-theatre-studies/'}
]
# The canonical catalogue supplies subject IDs; display aliases below only shorten gallery labels.
names = {'irish':'Irish (Gaeilge)', 'art':'Art', 'lithuanian':'Lithuanian', 'polish':'Polish', 'portuguese':'Portuguese', 'physics-and-chemistry':'Physics & Chemistry', 'design-and-communication-graphics':'Design & Communication Graphics', 'construction-studies':'Construction Studies', 'lcvp-link-modules':'LCVP / Life, Community & Work'}
aliases = {'design-and-communication-graphics':'DCG Applied Graphics and Design', 'construction-studies':'Construction Technology', 'physics-and-chemistry':'Chemical and Physical Science combined', 'agricultural-science':'Ag Science', 'physical-education':'PE', 'lcvp-link-modules':'Link Modules vocational', 'mathematics':'Maths', 'applied-mathematics':'Applied Maths'}
items=[]
for subject in catalogue+new_subjects:
    key=subject['id']
    item={**subject,'name':names.get(key,subject['name']),'aliases':aliases.get(key,''),'character':concepts[key]['character'],'direction':concepts[key]['detail'],'file':key+'.png'}
    if key=='irish' and (root/'irish-v2.png').exists(): item['file']='irish-v2.png'
    item.update(overrides.get(key, {}))
    path=root/item['file']
    item['ready']=path.exists()
    if path.exists():
        im=Image.open(path).convert('RGB')
        w,h=im.size
        # Orange and black ink, excluding the white canvas and soft near-white pixels.
        mask=im.convert('L').point(lambda p:255 if p<180 else 0)
        x0,y0,x1,y1=mask.getbbox()
        cx,cy=(x0+x1)/2,(y0+y1)/2
        scale=.78*min(w/(x1-x0),h/(y1-y0))
        pixels=mask.load()
        radius=max(math.hypot((x-cx)/w,(y-cy)/h) for y in range(y0,y1) for x in range(x0,x1) if pixels[x,y])
        scale=min(scale,.45/radius)
        item['frame']={'width':round(scale*100,6),'left':round(50-cx/w*scale*100,6),'top':round(50-cy/h*scale*100,6),'bounds':[x0,y0,x1,y1],'sourceSize':[w,h],'maxRadius':round(radius*scale,4)}
    items.append(item)
items.sort(key=lambda x:x['name'].casefold())
(root/'gallery.json').write_text(json.dumps(items,ensure_ascii=False,indent=2)+'\n')
print(json.dumps({'subjects':len(items),'ready':sum(x['ready'] for x in items),'missing':[x['id'] for x in items if not x['ready']]}))
