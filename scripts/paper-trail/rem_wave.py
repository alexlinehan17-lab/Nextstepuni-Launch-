#!/usr/bin/env python3
"""Remaining wave: precise-map BV (bilingual) + Foundation papers, additively."""
import importlib.util, json, os, sys
spec=importlib.util.spec_from_file_location("am","anchor-map.py")
am=importlib.util.module_from_spec(spec); spec.loader.exec_module(am)
am.UNIVERSAL_FALLBACK=False
LANGS=set(sys.argv[1].split(",")); LEVELS=set(sys.argv[2].split(",")) if len(sys.argv)>2 else None
if LEVELS: am.SCOPE_LEVELS = set(am.SCOPE_LEVELS) | LEVELS  # build_pairs checks the global, not the arg
rows,seen=[],set()
for line in open(am.MANIFEST,encoding="utf-8"):
    line=line.strip()
    if not line: continue
    r=json.loads(line); k=(r["view"],r["year"],r["fileid"])
    if k in seen or not r["fileid"].lower().endswith(".pdf"): continue
    seen.add(k); rows.append(r)
pairs=am.build_pairs(rows, include_done=True, langs=LANGS, levels=LEVELS)
mapped=0; by=__import__("collections").Counter()
mani={json.loads(l)['fileid'][:6]:json.loads(l)['subjectName'] for l in open("out/manifest.jsonl")}
for prow,srow,strat,level in pairs:
    year=int(prow["year"]); pfile,sfile=prow["fileid"],srow["fileid"]
    pp=am.corpus_path("exampapers",year,pfile); sp=am.corpus_path("markingschemes",year,sfile)
    if not (os.path.exists(pp) and os.path.exists(sp)): continue
    if os.path.exists(os.path.join(am.ANSWERS_DIR,str(year),f"{pfile}.json")): continue  # never overwrite
    sc,st=am.map_paper(pp,sp,strat)
    if sc is None: continue
    ydir=os.path.join(am.ANSWERS_DIR,str(year)); os.makedirs(ydir,exist_ok=True)
    json.dump(sc,open(os.path.join(ydir,f"{pfile}.json"),"w"),ensure_ascii=False,sort_keys=True,separators=(",",":"))
    mapped+=1; by[mani.get(pfile[:6],pfile[:5])+" "+{'A':'HL','G':'OL','C':'C','B':'Found'}.get(pfile[5],'?')]+=1
print(f"langs={LANGS} levels={LEVELS}: mapped={mapped}")
for s,c in by.most_common(40): print(f"  {s}: {c}")
