# squash.py dir : collapse long runs of identical pixel rows in *_q.png/*_a.png, in place
import sys,glob,numpy as np
from PIL import Image
def squash(path,keep=36,minrun=90):
    im=Image.open(path).convert('RGB'); a=np.asarray(im)
    same=np.concatenate([[False],(a[1:]==a[:-1]).all(axis=(1,2))])
    keeprow=np.ones(len(a),bool); i=0; n=len(a)
    while i<n:
        if same[i]:
            j=i
            while j<n and same[j]: j+=1
            if j-i>=minrun: keeprow[i+keep:j]=False
            i=j
        else: i+=1
    Image.fromarray(a[keeprow]).save(path)
for f in glob.glob(sys.argv[1]+'/*__[dm]_[qa].png'): squash(f)
