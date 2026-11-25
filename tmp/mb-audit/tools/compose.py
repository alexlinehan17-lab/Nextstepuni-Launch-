# Build review sheets + per-subject manifests from shots/all
import json,glob,os,sys
from PIL import Image
OUT='review'; os.makedirs(OUT,exist_ok=True)
plan=json.load(open('plan.json'))
subjects=json.load(open('decks/_subjects.json'))
topic={t['id']:f"{t.get('code','')} {t['title']}".strip() for s in subjects for st in s['strands'] for t in st['topics']}
def cols(path,dst,colh=1900,gap=16):
    im=Image.open(path).convert('RGB'); w,h=im.size
    n=max(1,-(-h//colh)); sheet=Image.new('RGB',(n*w+(n-1)*gap,min(h,colh)),(90,90,90))
    for i in range(n): sheet.paste(im.crop((0,i*colh,w,min(h,(i+1)*colh))),(i*(w+gap),0))
    sheet.save(dst); return n
only=sys.argv[1:] 
for s,cases in plan.items():
    if only and s not in only: continue
    deck={c['id']:c for f in glob.glob(f'decks/{s}__*.json') for c in json.load(open(f))}
    os.makedirs(f'{OUT}/{s}',exist_ok=True); man=[]
    for i,case in enumerate(cases):
        cid=case['id']; c=deck[cid]; base=f'shots/all/{cid}'
        e={'n':i+1,'id':cid,'level':c['level'],'year':c['year'],'questionRef':c['questionRef'],'topic':topic.get(c['topicId'],c['topicId']),'totalMarks':c['totalMarks'],'kind':c['kind'],'why_sampled':case['why'],
           'has':{k:bool(c.get(k)) for k in('figure','questionFigure','sourceMaterial','audioMaterial','mathematicsScale','rubric') if c.get(k)},
           'stem':(c.get('stem') or '')[:500],'questionText':c['questionText'][:700]}
        sm=c.get('sourceMaterial')
        if sm: e['sourceMaterial']={'label':sm['label'],'title':sm['title'],'pages':sm.get('pages'),'cropped_to_region':bool(sm.get('regions')),'kind':sm['kind']}
        imgs={}
        if os.path.exists(base+'__m_a.png'): cols(base+'__m_a.png',f'{OUT}/{s}/{i+1:02d}_phone_answer.png'); imgs['phone_after_reveal']=f'{i+1:02d}_phone_answer.png'
        if os.path.exists(base+'__d_a.png'):
            im=Image.open(base+'__d_a.png').convert('RGB'); 
            if im.height>2400: im=im.crop((0,0,1280,2400))
            im.save(f'{OUT}/{s}/{i+1:02d}_desktop_answer.png'); imgs['desktop_after_reveal']=f'{i+1:02d}_desktop_answer.png'
        if os.path.exists(base+'__src.png'):
            im=Image.open(base+'__src.png').convert('RGB'); im.save(f'{OUT}/{s}/{i+1:02d}_attached_page.png'); imgs['attached_page_reader']=f'{i+1:02d}_attached_page.png'
        if os.path.exists(base+'__m_v.png'): Image.open(base+'__m_v.png').save(f'{OUT}/{s}/{i+1:02d}_phone_first_screen.png'); imgs['phone_first_screen_before_reveal']=f'{i+1:02d}_phone_first_screen.png'
        e['images']=imgs; man.append(e)
    json.dump({'subject':s,'deckSize':len(deck),'cards':man},open(f'{OUT}/{s}/manifest.json','w'),indent=1,ensure_ascii=False)
    print(s,len(man))
