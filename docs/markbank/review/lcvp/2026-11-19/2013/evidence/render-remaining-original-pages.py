from pathlib import Path
import datetime,hashlib,json,re,shutil,subprocess
import fitz
review=Path('/Users/alexlinehan/Documents/NextStepUni-MarkBank-Lanes-20261104/REVIEW/2026-11-19-lcvp-2013-source-reading')
output=review/'remaining-original-pages';output.mkdir(exist_ok=True)
source=Path('/Users/alexlinehan/Documents/Nextstepuni-Maths-Launch-Integration-20261030/paper-trail-corpus')
manifest=json.loads((review/'cached-source-inventory.json').read_text())
records=[]
for kind,archive,fileid,pages in [('paper','exampapers','LC462CLP000EV.pdf',[13,14,15,16,17,18,19,22,23,24,25,26,28,29,31,32]),('scheme','markingschemes','LC462CLP000EV.pdf',[1,2,3,4,5,6,7,8,9,10,11,14,16,18,19,20]),('case','exampapers','LC462CLP016EV.pdf',[1,2])]:
 pdf=source/archive/'2013'/fileid
 source_hash=hashlib.sha256(pdf.read_bytes()).hexdigest()
 expected=next(r for r in manifest['sources'] if r['kind']==archive and r['fileid']==fileid)
 assert source_hash==expected['sha256']
 for page in pages:
  batt=subprocess.check_output(['pmset','-g','batt'],text=True);free=shutil.disk_usage(output).free
  assert free>10*1024**3 and ('AC Power' in batt or int(re.search(r'(\d+)%',batt)[1])>=25)
  prefix=output/f'{kind}-{page:02d}'
  image=prefix.with_suffix('.png')
  # Poppler is unavailable on this Mac; render the original PDF with PyMuPDF.
  with fitz.open(pdf) as document:
   document[page-1].get_pixmap(matrix=fitz.Matrix(160/72,160/72),alpha=False).save(image)
  records.append({'kind':kind,'physicalPage':page,'sourcePath':str(pdf),'sourceSha256':source_hash,'imagePath':str(image),'sha256':hashlib.sha256(image.read_bytes()).hexdigest(),'visualReview':'Awaiting first source reading; rendering alone is not a source review'})
(output/'manifest.json').write_text(json.dumps({'createdAt':datetime.datetime.now(datetime.timezone.utc).isoformat(),'records':records},indent=2)+'\n')
print('Rendered34remaining2013originalpages for first source reading:',output,flush=True)
