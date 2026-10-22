"""Compare each module's REGIONS (hand-set lines excluded) with a fresh regions.py draft.
usage: regioncheck.py <census-dir> year:fileid:tag:module ...   (census-dir holds <tag>-census.txt)"""
import subprocess, sys, re
S = sys.argv[1]
for spec in sys.argv[2:]:
    year, fileid, tag, module = spec.split(':')
    draft = subprocess.run(['python3', 'scripts/markbank/agricultural-science-audit/draft_regions.py', year, fileid, f'{S}/{tag}-census.txt'],
                           capture_output=True, text=True).stdout.splitlines()
    src = open(f'scripts/markbank/authoring/{module}.py').read()
    block = src[src.index('REGIONS = {'):src.index('\n}\n', src.index('REGIONS = {'))].splitlines()[1:]
    mod = {re.match(r"\s*'([^']+)'", l).group(1): l.split('  #')[0].rstrip() for l in block if re.match(r"\s*'", l)}
    hand = {re.match(r"\s*'([^']+)'", l).group(1) for l in block if '  #' in l and re.match(r"\s*'", l)}
    diffs = []
    for l in draft:
        m = re.match(r"\s*'([^']+)'", l)
        if not m:
            continue
        ref = m.group(1)
        if mod.get(ref) != l.rstrip():
            diffs.append((ref, ref in hand, mod.get(ref), l.strip()))
    print(f'== {tag}: {len(diffs)} differ')
    for ref, h, old, new in diffs:
        print(f'  {ref} {"(hand-set in module)" if h else ""}\n    module: {old and old.strip()}\n    draft:  {new}')
