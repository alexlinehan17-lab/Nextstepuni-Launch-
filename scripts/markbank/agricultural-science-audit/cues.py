"""Print every raw selection cue on a paper with the hash key a review module classifies it under.
usage: python3 scripts/markbank/agricultural-science-audit/cues.py <year> <fileid>"""
import sys,hashlib,fitz
sys.path.insert(0,'scripts/markbank/authoring')
from agricultural_science_inventory import DIRECTIVE
year,fileid=sys.argv[1],sys.argv[2]
path=f'paper-trail-corpus/exampapers/{year}/{fileid}'
digest=hashlib.sha256(open(path,'rb').read()).hexdigest()
with fitz.open(path) as pdf:
    for i,p in enumerate(pdf):
        text=' '.join(p.get_text().split())
        for m in DIRECTIVE.finditer(text):
            ctx=text[max(0,m.start()-90):m.end()+230]
            key=hashlib.sha256(f'{digest}|{i+1}|{m.start()}|{ctx}'.encode()).hexdigest()[:16]
            print(f"{key} p{i+1} [{m.group()}] ...{text[max(0,m.start()-60):m.end()+90]}")
