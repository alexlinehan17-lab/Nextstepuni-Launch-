"""Wire a legacy paper into census.py, completion.py and vaultResolve.ts.
usage: wire.py <year> <hl|ol> <census.txt> <count> <reviewedAt> [pools-python-literal] [ol-part-choice]"""
import sys, re, hashlib
year, lvl, census, count, reviewed = sys.argv[1], sys.argv[2], sys.argv[3], int(sys.argv[4]), sys.argv[5]
pools = sys.argv[6] if len(sys.argv) > 6 else '{}'
partq = sys.argv[7] if len(sys.argv) > 7 else None
level = 'higher' if lvl == 'hl' else 'ordinary'
Level = level.title()
letter = 'A' if lvl == 'hl' else 'G'
fileid = f'LC024{letter}LP000EV.pdf'
h = {k: hashlib.sha256(open(f'paper-trail-corpus/{k}/{year}/{fileid}', 'rb').read()).hexdigest() for k in ('exampapers', 'markingschemes')}
NAME = f'{level.upper()}_{year}'
POOLS = f'POOLS_{year}_{level.upper()}'
p = 'scripts/markbank/authoring/agricultural_science_census.py'
s = open(p).read()
table = open(census).read().strip()
anchor = 'MODERN_POOLS = {'
s = s.replace(anchor, f"# {year} {Level} (legacy syllabus), transcribed from the SEC paper and scheme.\n{NAME} = '''\n{table}\n'''\n{POOLS} = {pools}\n" + anchor, 1)
s = re.sub(r"(MODERN_POOLS = \{.*?)\}\n", lambda m: m.group(1) + f", ({year},'{level}'):{POOLS}}}\n", s, count=1, flags=re.S)
s = s.replace("SOURCES = [\n", f"SOURCES = [\n    ({year}, '{level}', '{letter}', {NAME},\n     '{h['exampapers']}',\n     '{h['markingschemes']}'),\n", 1)
s = re.sub(r"(assert len\(tasks\)==\{.*?)\}\[\(year,level\)\]", lambda m: m.group(1) + f",({year},'{level}'):{count}}}[(year,level)]", s, count=1)
s = re.sub(r"(\d+)\. Remaining editions stay open\.'\)", lambda m: f"{m.group(1)}; {year} {Level} {count}. Remaining editions stay open.')", s, count=1)
if partq:
    s = re.sub(r"OL_PART_CHOICE = \{", f"OL_PART_CHOICE = {{{year}: '{partq}', ", s, count=1)
open(p, 'w').write(s)
p = 'scripts/markbank/authoring/agricultural_science_completion.py'
s = open(p).read()
imp = f"from agricultural_science_{year}_{lvl} import reviewed_tasks as reviewed_{year}_{lvl}, paper_review as {level}_{year}_review\n"
last = [m.end() for m in re.finditer(r"from agricultural_science_20\d\d_(hl|ol) import reviewed_tasks as reviewed_20\d\d_(hl|ol), paper_review as \w+\n", s)][-1]
s = s[:last] + imp + s[last:]
s = re.sub(r"(for legacy, legacy_review, reviewed_on in \[.*?)\]:", lambda m: m.group(1) + f",\n                                               (reviewed_{year}_{lvl}, {level}_{year}_review, '{reviewed}')]:", s, count=1, flags=re.S)
open(p, 'w').write(s)
p = 'components/PaperTrail/vaultResolve.ts'
s = open(p).read()
a = "  'agricultural-science|2020|LC024ALP000EV.pdf',\n"
s = s.replace(a, a + f"  'agricultural-science|{year}|{fileid}',\n", 1)
open(p, 'w').write(s)
print('wired', year, level)
