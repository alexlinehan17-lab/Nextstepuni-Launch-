import sys,fitz
"""Check a transcribed census table (ref|marks|paperPage|schemePage|cue): every cue occurs on its scheme page; prints per-question totals.
usage: python3 scripts/markbank/agricultural-science-audit/cuecheck.py census.txt scheme.pdf paper.pdf"""
lines=[l for l in open(sys.argv[1]).read().strip().splitlines()]
S=[' '.join(p.get_text().split()) for p in fitz.open(sys.argv[2])]
P=[' '.join(p.get_text().split()) for p in fitz.open(sys.argv[3])]
tot={}
for l in lines:
    ref,m,pp,sp,cue=l.split('|')
    if cue not in S[int(sp)-1]: print('MISS',ref,sp,repr(cue))
    q=ref.split('(')[0].split(' ')[0]; tot[q]=tot.get(q,0)+int(m)
print(len(lines),tot)
