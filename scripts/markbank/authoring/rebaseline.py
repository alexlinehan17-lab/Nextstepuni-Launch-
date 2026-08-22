#!/usr/bin/env python3
"""Verify no Mark Bank card was lost, then update the preservation baseline.

The baseline test's own header: "update the affected count/hash only after
checking that all previous IDs remain present. Never refresh this baseline to
conceal a deletion." This does the checking, and refuses if anything vanished.
"""
import hashlib, os, re, subprocess, sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
try:
    from econ_refs import WITHDRAWN
except ImportError:                       # every other subject
    WITHDRAWN = set()

SUBJECT = sys.argv[1] if len(sys.argv) > 1 else 'home-economics'
# These MUST match the id prefix the deck actually uses. 'phy' and 'ag' did not
# -- the ids are "phys-" and "agsci-" -- so ids() matched nothing, old and new
# were both empty, "lost=0" passed, and the baseline was rewritten to 0 cards
# with the SHA of the empty string. The guard against losing cards recorded a
# total wipe as a clean run. The empty-deck check below is the backstop.
PREFIX = {'home-economics': 'he', 'biology': 'bio', 'business': 'bus',
          'chemistry': 'chem', 'physics': 'phys', 'agricultural-science': 'agsci',
          'economics': 'econ'}[SUBJECT]
TEST = 'test/markBankCardPreservation.test.ts'
KEY = {'home-economics': 'home-economics', 'agricultural-science': 'agricultural-science'}.get(SUBJECT, SUBJECT)

def ids(text):
    return re.findall(rf'id:\s*"({PREFIX}-[^"]+)"', text)

src = open(TEST).read()
ok = True
for level in ('higher', 'ordinary'):
    path = f'components/MarkBank/cards/{SUBJECT}/{level}.ts'
    old = ids(subprocess.run(['git', 'show', f'HEAD:{path}'], capture_output=True, text=True).stdout)
    new = ids(open(path).read())
    if not new and old:
        print(f'    REFUSING: found no {PREFIX}-* ids in {path}, and HEAD has '
              f'{len(old)}. That is a wipe, not a rebuild.')
        ok = False
        continue
    if not new:
        # Empty at HEAD and empty now: a level nobody has authored yet. The
        # backstop above exists because a total WIPE once recorded itself as a
        # clean run, and it still catches that — but a subject's first Higher
        # paper cannot be blocked on its Ordinary deck not existing.
        print(f'{SUBJECT}:{level}  not authored yet, skipped')
        continue
    # A withdrawal is allowed only if someone wrote down why: see
    # econ_refs.WITHDRAWN. Everything else that vanishes is an accident.
    lost = sorted(set(old) - set(new) - WITHDRAWN)
    pulled = sorted((set(old) - set(new)) & WITHDRAWN)
    for w in pulled:
        print(f'    withdrawn on purpose (econ_refs.WITHDRAWN): {w}')
    added = sorted(set(new) - set(old))
    dupes = len(new) != len(set(new))
    print(f'{SUBJECT}:{level}  {len(old)} -> {len(new)}   +{len(added)}  lost={len(lost)}  dupes={dupes}')
    for a in added:
        print('    +', a)
    if lost:
        print('    REFUSING: previous IDs missing:', lost)
        ok = False
        continue
    if dupes:
        print('    REFUSING: duplicate IDs')
        ok = False
        continue
    h = hashlib.sha256('\n'.join(sorted(new)).encode()).hexdigest()
    pat = re.compile(rf"\['{KEY}:{level}', ([A-Z_]+), (\d+), '([0-9a-f]{{64}})'\]")
    m = pat.search(src)
    if not m:
        print('    REFUSING: baseline row not found'); ok = False; continue
    src = src[:m.start()] + f"['{KEY}:{level}', {m.group(1)}, {len(new)}, '{h}']" + src[m.end():]

if not ok:
    sys.exit('baseline NOT updated')

# total across every deck
total = 0
for m in re.finditer(r"', [A-Z_]+, (\d+), '", src):
    total += int(m.group(1))
src = re.sub(r'toBe\(\d[\d_]*\);', f'toBe({total:,}'.replace(',', '_') + ');', src)
open(TEST, 'w').write(src)
print(f'baseline updated; bank total now {total}')
