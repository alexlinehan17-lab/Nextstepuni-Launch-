"""Replace a module's REGIONS block body with a drafted one: swap_regions.py <module.py> <draft.txt>"""
import sys
path, draft = sys.argv[1:3]
lines = open(path).read().split('\n')
start = lines.index('REGIONS = {')
end = next(i for i in range(start + 1, len(lines)) if lines[i] == '}')
body = open(draft).read().rstrip('\n').split('\n')
lines[start + 1:end] = body
open(path, 'w').write('\n'.join(lines))
