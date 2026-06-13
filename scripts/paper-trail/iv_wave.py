#!/usr/bin/env python3
"""IV (Irish-medium) precise wave: map every IV paper that reconciles cleanly to its
IV marking scheme. Reuses the engine's map_paper (precise only — no fallback). Writes
sidecars WITHOUT clearing (additive; never touches the committed EV maps)."""
import importlib.util, json, os
spec=importlib.util.spec_from_file_location("am","anchor-map.py")
am=importlib.util.module_from_spec(spec); spec.loader.exec_module(am)
am.UNIVERSAL_FALLBACK=False
rows,seen=[],set()
for line in open(am.MANIFEST,encoding="utf-8"):
    line=line.strip()
    if not line: continue
    r=json.loads(line); k=(r["view"],r["year"],r["fileid"])
    if k in seen or not r["fileid"].lower().endswith(".pdf"): continue
    seen.add(k); rows.append(r)
pairs=am.build_pairs(rows, include_done=True, langs={"IV"})
mapped=dropped=0; by=__import__("collections").Counter()
mani={json.loads(l)['fileid'][:6]:json.loads(l)['subjectName'] for l in open("out/manifest.jsonl")}
for prow,srow,strat,level in pairs:
    year=int(prow["year"]); pfile,sfile=prow["fileid"],srow["fileid"]
    pp=am.corpus_path("exampapers",year,pfile); sp=am.corpus_path("markingschemes",year,sfile)
    if not (os.path.exists(pp) and os.path.exists(sp)): continue
    sc,st=am.map_paper(pp,sp,strat)
    if sc is None or st.get("pagejump",0)>len(sc["q"]): 
        dropped+=1; continue
    ydir=os.path.join(am.ANSWERS_DIR,str(year)); os.makedirs(ydir,exist_ok=True)
    json.dump(sc,open(os.path.join(ydir,f"{pfile}.json"),"w"),ensure_ascii=False,sort_keys=True,separators=(",",":"))
    mapped+=1; by[mani.get(pfile[:6],pfile[:5])]+=1
print(f"IV mapped={mapped} dropped={dropped}")
for s,c in by.most_common(40): print(f"  {s}: {c}")
